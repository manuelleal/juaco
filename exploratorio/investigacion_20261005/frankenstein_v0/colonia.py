# -*- coding: utf-8 -*-
"""COLONIA / MEMORIA VIVA con CUARENTENA (reglas locales, sin gradiente, sin tocar el cuerpo).

Una CÉLULA = una afirmación oída: (frases, valor que el cuerpo extrajo, fuentes que la dijeron).
  - Nace como HIPÓTESIS cuando una fuente enseña algo: no tiene derecho a hablar por el sistema.
  - Otra frase CONFIRMA a la célula si dice lo mismo (parecido de la frase entera >= UMBRAL_IGUAL, el
    valor de cada una aparece en la otra y los nombres propios coinciden). Cada fuente DISTINTA que
    confirma es una confirmación independiente; la misma fuente repitiendo no suma.
  - VALIDADA: soporte (fuentes distintas) >= K. K = 2.
  - Al PREGUNTAR, las células parecidas a la pregunta (>= UMBRAL_Q) compiten: tiene VOZ la validada
    cuyo soporte supera al de toda rival (otra célula candidata, que por construcción dice otra cosa).
    Si hay candidatas y ninguna tiene voz: DUDA. Si no hay candidatas: NADA.

Puesto a mano (declarado): la clave es LÉXICA (palabras pesadas por rareza), no el estado interno del
cuerpo (el servidor de un solo proceso no da estados internos y texto a la vez); UMBRAL_Q y
UMBRAL_IGUAL elegidos en la semilla 0 de calibración; K = 2. Sin energía, sin muerte y sin sueño en v0.
"""
import difflib
import math
import re

from mundo import norm

VACIAS = set("""el la los las un una unos unas de del al a en y o que es son se fue por con para su sus lo
le como cual cuales quien quienes cuanto cuanta cuantos cuantas donde cuando este esta ese esa esto eso
mi me te tu ya no si mas muy tambien pero porque llama llamada llamado nombre toda todo tiene tienen
hay era ser estan sobre entre desde hasta sin alrededor que""".split())
K = 2
UMBRAL_Q = 0.66        # compuerta pregunta -> célula (semilla 0: frase ajena <= 0.64, frase propia >= 0.68; margen fino)
UMBRAL_IGUAL = 0.77    # compuerta frase -> célula que dice lo mismo (semilla 0: mismo valor >= 0.81, distinto <= 0.72)


def tokens(s):
    return [t for t in norm(s).split() if (t not in VACIAS and len(t) > 1) or t.isdigit()]


def propios(s):
    """Nombres propios: palabras con mayúscula inicial que no son palabras vacías."""
    return {norm(w) for w in re.findall(r"[A-ZÁÉÍÓÚÑ][\wáéíóúñü]+", s) if norm(w) not in VACIAS and len(norm(w)) > 2}


def _igual(a, b):
    if a == b:
        return True
    if a.isdigit() or b.isdigit() or min(len(a), len(b)) < 5:
        return False
    return difflib.SequenceMatcher(None, a, b).ratio() >= 0.84


def _esta(t, conj):
    return any(_igual(t, u) for u in conj)


class Indice:
    """Rareza de las palabras en lo oído (idf). Las no vistas pesan como las más raras."""
    def __init__(self):
        self.df, self.n = {}, 0

    def agrega(self, toks):
        self.n += 1
        for t in set(toks):
            self.df[t] = self.df.get(t, 0) + 1

    def peso(self, t):
        d = self.df.get(t)
        if d is None:
            d = max((v for u, v in self.df.items() if _igual(t, u)), default=0)
        return math.log(1.0 + (self.n + 1.0) / (d + 0.5))


def cubre(idx, a, b):
    """Fracción (pesada por rareza) de las palabras de a que están en b."""
    a = set(a)
    if not a:
        return 0.0
    tot = sum(idx.peso(t) for t in a)
    return sum(idx.peso(t) for t in a if _esta(t, b)) / tot


def parecido_pregunta(idx, pregunta, frase):
    """Compuerta de recuperación, la MISMA para la memoria ingenua y para la colonia."""
    tf = tokens(frase)
    s = cubre(idx, tokens(pregunta), tf)
    if not all(_esta(p, tf) for p in propios(pregunta)):
        return min(s, 0.5)       # la pregunta nombra (con mayúscula) algo que la frase no nombra
    return s


class Celula:
    __slots__ = ("id", "valor", "frases", "fuentes", "t_nace", "t_valida")

    def __init__(self, i, valor, t):
        self.id, self.valor = i, valor
        self.frases, self.fuentes, self.t_nace, self.t_valida = [], [], t, None

    @property
    def soporte(self):
        return len(set(self.fuentes))


class Colonia:
    def __init__(self, k=K):
        self.k = k
        self.celulas, self.idx, self.t = [], Indice(), 0
        self.registro = []      # (t, fuente, suceso, id): nace / confirma / repite / valida

    def estado(self, c):
        return "VALIDADA" if c.soporte >= self.k else "HIPOTESIS"

    def _dice_lo_mismo(self, c, frase, tv):
        tf, pf = tokens(frase), propios(frase)
        mejor = 0.0
        for _, f in c.frases:
            tg = tokens(f)
            s = 0.5 * (cubre(self.idx, tf, tg) + cubre(self.idx, tg, tf))
            pg = propios(f)
            if pf and pg and not (all(_esta(p, tg) for p in pf) and all(_esta(p, tf) for p in pg)):
                continue                                   # nombres propios distintos: no es lo mismo
            cv = set(tokens(c.valor))
            if tv and cv:
                if not (all(_esta(t, tg) for t in tv) and all(_esta(t, tf) for t in cv)):
                    continue                               # el dato de una no aparece en la otra
                umbral = UMBRAL_IGUAL
            else:
                umbral = 0.90                              # sin dato extraído: sólo frases casi idénticas
            if s >= umbral:
                mejor = max(mejor, s)
        return mejor

    # ---------- enseñar ----------
    def ensena(self, fuente, frase, valor):
        """valor = lo que el cuerpo extrajo como dato afirmado ('' si falló). Devuelve (sucesos, célula)."""
        self.t += 1
        self.idx.agrega(tokens(frase))
        tv = set(tokens(valor))
        cel, ms = None, 0.0
        for c in self.celulas:
            s = self._dice_lo_mismo(c, frase, tv)
            if s > ms:
                cel, ms = c, s
        suc = []
        if cel is None:
            cel = Celula(len(self.celulas), norm(valor), self.t)
            self.celulas.append(cel)
            suc.append("nace")
        else:
            suc.append("confirma" if fuente not in cel.fuentes else "repite")
        antes = cel.soporte
        cel.frases.append((fuente, frase))
        cel.fuentes.append(fuente)
        if antes < self.k <= cel.soporte:
            cel.t_valida = self.t
            suc.append("valida")
        self.registro += [(self.t, fuente, s, cel.id) for s in suc]
        return suc, cel

    # ---------- consultar ----------
    def candidatas(self, texto, umbral=UMBRAL_Q):
        out = []
        for c in self.celulas:
            s = max(parecido_pregunta(self.idx, texto, f) for _, f in c.frases)
            if s >= umbral:
                out.append((s, c))
        return sorted(out, key=lambda x: (-x[0], x[1].id))

    def consulta(self, pregunta):
        """Devuelve (estado, con_voz, sin_voz, parecido). estado: VALIDADO / DUDA / NADA."""
        cand = self.candidatas(pregunta)
        if not cand:
            return "NADA", [], [], 0.0
        cs = [c for _, c in cand]
        voz = [c for c in cs if c.soporte >= self.k and all(c.soporte > o.soporte for o in cs if o is not c)]
        return ("VALIDADO" if voz else "DUDA"), voz, [c for c in cs if c not in voz], cand[0][0]

    def resumen(self):
        v = sum(c.soporte >= self.k for c in self.celulas)
        return {"celulas": len(self.celulas), "validadas": v, "hipotesis": len(self.celulas) - v}


class MemoriaIngenua:
    """El rival convencional: guarda todo lo que le dicen y recupera las 3 frases más parecidas
    (misma medida de parecido y misma compuerta que la colonia). Cree todo."""
    def __init__(self, top=3):
        self.frases, self.idx, self.top = [], Indice(), top

    def ensena(self, fuente, frase):
        self.idx.agrega(tokens(frase))
        self.frases.append((fuente, frase))

    def consulta(self, pregunta):
        p = [(parecido_pregunta(self.idx, pregunta, f), i) for i, (_, f) in enumerate(self.frases)]
        p = sorted([x for x in p if x[0] >= UMBRAL_Q], key=lambda x: (-x[0], x[1]))[: self.top]
        return [self.frases[i] for _, i in sorted(p, key=lambda x: x[1])]
