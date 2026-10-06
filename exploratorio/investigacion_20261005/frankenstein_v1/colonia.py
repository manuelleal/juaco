# -*- coding: utf-8 -*-
"""COLONIA v1: cuarentena + REPUTACIÓN por fuente aprendida en uso + RECENCIA entre validadas.

Una CÉLULA = una afirmación oída: (sujeto, atributo, valor) + frases + fuentes.
  - Nace como HIPÓTESIS. Otra frase la CONFIRMA si afirma lo mismo: mismo sujeto (nombres propios sin el
    valor), mismo valor (uno contenido en el otro) y mismo atributo (la palabra de propiedad que el cuerpo
    extrajo de una aparece en la otra, por raíz) o atributo desconocido. Ya NO se exige parecido de la frase
    entera (v0 pedía 0.77): es lo que permite frases libres.
  - RIVAL = mismo sujeto, mismo atributo (conocido en ambas) y valor distinto. Un GRUPO = componente conexa
    de rivales (en este mundo: las células de un mismo hecho).
  - PESO de una célula W = suma de la REPUTACIÓN de sus fuentes distintas. VALIDADA si W >= K.
    Sin reputación, rep = 1 para todas y W = número de fuentes distintas (= v0).
  - REPUTACIÓN (derivada del estado, recalculada a punto fijo tras cada enseñanza):
      rep(f) = recorte a [0, 1] de  1 − CASTIGO · (células de f que hoy PIERDEN) + PREMIO · (células de f que hoy GANAN).
      En un grupo GANA la célula con W >= K que supera ESTRICTAMENTE a toda rival; las demás PIERDEN. Si nadie
      domina, nadie gana ni pierde. Para juzgar un grupo se usa la reputación que cada fuente tiene FUERA de
      ese grupo (dejar-uno-fuera): lo que dijiste aquí no cuenta a tu favor ni en tu contra aquí. Así una pareja
      de mentirosos que termina de hablar antes que los honestos no condena al honesto, y la decisión no depende
      del orden. Efecto buscado: el cómplice de un mentiroso atrapado en otros hechos suma menos de 1 y la pareja
      no llega a K. Ganar sólo cuenta en grupos con rival (mentir al unísono sobre lo que nadie discute no paga).
  - RECENCIA: si al preguntar dos VALIDADAS rivales empatan en W, habla la validada más tarde (la verdad que
    cambia se corrige). Precio declarado: dos mentirosos frescos que llegan después de la verdad ganan.
  - Al PREGUNTAR: las células recuperadas por la compuerta léxica compiten; habla la validada con mayor W que
    toda otra candidata (desempate por recencia sólo entre rivales); si hay candidatas y nadie habla: DUDA;
    si no hay candidatas: NADA.
Puesto a mano (declarado): clave LÉXICA (palabras pesadas por rareza) con raíces de 4 letras para las
palabras de propiedad (nunca para nombres propios); UMBRAL_Q de v0; K = 2; CASTIGO 0.5; PREMIO 0.25;
tope de 10 pasadas para el punto fijo (se registra si no converge). Decisión de calibración (semilla 0, juego A,
sin cuerpo): la primera versión castigaba al vuelo e invertía la reputación cuando la pareja mentirosa hablaba
antes que la segunda fuente honesta; se cambió a la regla derivada con dejar-uno-fuera ANTES del preregistro.
"""
import difflib
import math
import re

from mundo import norm

VACIAS = set("""el la los las un una unos unas de del al a en y o que es son se fue por con para su sus lo
le como cual cuales quien quienes cuanto cuanta cuantos cuantas donde cuando este esta ese esa esto eso
mi me te tu ya no si mas muy tambien pero porque llama llamada llamado nombre toda todo tiene tienen
hay era ser estan sobre entre desde hasta sin alrededor que""".split())
# palabras que al empezar frase llevan mayúscula y NO son nombres propios (sólo para detectar propios)
ARRANQUES = set("""aunque hablando sabias pocos poca hace sobre resulta cuando respecto hoy ayer nada cualquier
dicen segun color toda todos nadie alguien antes despues ademas tambien ahora luego entonces asi aqui alli
cada otra otro mira oye atencion importante dato recuerda confirmo repito insisto efectivamente exacto claro
bueno pues vaya fijate imagina acerca tras mientras incluso obviamente curiosamente oficialmente actualmente
antiguamente historicamente quien quienes alrededor son por para con desde hasta los las unos unas una un
el la de del al en lo le mi me te tu ya no si mas muy pero porque siempre nunca creo pienso parece
cuentan dice cuenta ojo nota leeria lei leer sabia sabes sabe ojala quizas tal vez""".split())
K = 2
UMBRAL_Q = 0.66        # compuerta pregunta -> célula (heredada de v0; semilla 0 juego A: ajena <= 0.66, propia >= 0.75)
CASTIGO = 0.5
PREMIO = 0.25
MAX_PASADAS = 10


def tokens(s):
    return [t for t in norm(s).split() if (t not in VACIAS and len(t) > 1) or t.isdigit()]


def propios(s):
    """Nombres propios: palabras con mayúscula inicial que no son vacías ni arranques de frase."""
    out = set()
    for w in re.findall(r"[A-ZÁÉÍÓÚÑ][\wáéíóúñü]+", s):
        n = norm(w)
        if n in VACIAS or n in ARRANQUES or len(n) <= 2:
            continue
        out.add(n)
    return out


def raiz(t):
    return t[:4] if len(t) >= 5 and not t.isdigit() else t


def _igual(a, b, raices=False):
    if a == b:
        return True
    if a.isdigit() or b.isdigit() or min(len(a), len(b)) < 5:
        return False
    if raices and raiz(a) == raiz(b):
        return True
    return difflib.SequenceMatcher(None, a, b).ratio() >= 0.84


def _esta(t, conj, raices=False):
    return any(_igual(t, u, raices) for u in conj)


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


def cubre(idx, a, b, sin_raiz=()):
    """Fracción (pesada por rareza) de las palabras de a que están en b. Raíces de 4 letras para las
    palabras que no son nombres propios (sin_raiz)."""
    a = set(a)
    if not a:
        return 0.0
    tot = sum(idx.peso(t) for t in a)
    return sum(idx.peso(t) for t in a if _esta(t, b, raices=(t not in sin_raiz))) / tot


def parecido_pregunta(idx, pregunta, frase):
    """Compuerta de recuperación, la MISMA para todas las memorias."""
    tf = tokens(frase)
    pq = propios(pregunta)
    s = cubre(idx, tokens(pregunta), tf, sin_raiz=pq)
    if not all(_esta(p, tf) for p in pq):
        return min(s, 0.5)       # la pregunta nombra (con mayúscula) algo que la frase no nombra
    return s


# ---------------- afirmación: sujeto / atributo / valor ----------------
class Afirmacion:
    __slots__ = ("frase", "valor", "tv", "sujeto", "atrib", "resto", "sig", "pf")

    def __init__(self, frase, valor, atributo=""):
        self.frase = frase
        self.valor = norm(valor)
        self.tv = set(tokens(valor))
        pf = propios(frase)
        self.sujeto = {p for p in pf if not _esta(p, self.tv)}
        tf = set(tokens(frase))
        self.resto = {t for t in tf if t not in pf and not _esta(t, self.tv)}
        # atributo: palabras de propiedad que dijo el cuerpo y que de verdad están en la frase
        self.atrib = {t for t in tokens(atributo) if _esta(t, tf, raices=True)} if atributo else set()
        # FIRMA de la afirmación: las entidades que relaciona (nombres propios + dato). Es la misma aunque el
        # cuerpo invierta cuál es el sujeto y cuál el valor (semilla 0: "Por X pasa el río Y" -> valor X).
        self.sig = pf | self.tv
        self.pf = pf


def _subconjunto(a, b):
    return all(_esta(t, b) for t in a)


def misma_firma(a, b):
    """Las mismas entidades (una firma contenida en la otra: 'ingeniero Kozan' ~ 'Kozan')."""
    if not a.tv or not b.tv or not a.sig or not b.sig:
        return False
    return _subconjunto(a.sig, b.sig) or _subconjunto(b.sig, a.sig)


def comparten_entidad(a, b):
    """Comparten un NOMBRE PROPIO (no un token del valor: 'rojo', '48' o 'ingeniero' no hacen rivales)."""
    return any(_esta(t, b.pf) for t in a.pf)


def mismo_valor(a, b):
    if not a.tv or not b.tv:
        return False
    if all(t.isdigit() for t in a.tv | b.tv):
        return a.tv == b.tv
    return all(_esta(t, b.tv) for t in a.tv) or all(_esta(t, a.tv) for t in b.tv)


def mismo_sujeto(a, b):
    return bool(a.sujeto) and bool(b.sujeto) and any(_esta(p, b.sujeto) for p in a.sujeto)


def mismo_atributo(a, b):
    """Conocido para ambas y coincide: la palabra de propiedad de una aparece (por raíz) en la otra."""
    if not a.atrib or not b.atrib:
        return None                                   # desconocido
    return (any(_esta(t, b.resto | b.atrib, raices=True) for t in a.atrib) or
            any(_esta(t, a.resto | a.atrib, raices=True) for t in b.atrib))


def es_misma(a, b):
    """Misma afirmación: misma firma de entidades y atributo compatible (o desconocido)."""
    return misma_firma(a, b) and mismo_atributo(a, b) is not False


def es_rival(a, b):
    """Rival: comparten alguna entidad, NO son la misma afirmación y el atributo coincide (conocido en ambas)."""
    return (bool(a.tv) and bool(b.tv) and not misma_firma(a, b) and comparten_entidad(a, b)
            and mismo_atributo(a, b) is True)


class Celula:
    __slots__ = ("id", "af", "frases", "fuentes", "t_nace", "t_valida", "estado_grupo")

    def __init__(self, i, af, t):
        self.id, self.af = i, af
        self.frases, self.fuentes, self.t_nace, self.t_valida = [], [], t, None
        self.estado_grupo = None          # 'gana' / 'pierde' / None (sólo con reputación)

    @property
    def soporte(self):
        return len(set(self.fuentes))

    @property
    def valor(self):
        return self.af.valor


class Colonia:
    def __init__(self, k=K, reputacion=False, recencia=False, castigo=CASTIGO, premio=PREMIO):
        self.k, self.reputacion, self.recencia, self.castigo, self.premio = k, reputacion, recencia, castigo, premio
        self.celulas, self.idx, self.t = [], Indice(), 0
        self.rep = {}
        self.adj = {}           # id -> conjunto de ids rivales (incremental)
        self.registro = []      # (t, fuente, suceso, id)
        self.no_convergio = 0

    # ---------- reputación / peso ----------
    def rep_de(self, f):
        return self.rep.get(f, 1.0) if self.reputacion else 1.0

    def W(self, c, rep=None):
        if rep is None:
            return sum(self.rep_de(f) for f in set(c.fuentes))
        return sum(rep.get(f, 1.0) for f in set(c.fuentes))

    def validada(self, c):
        return self.W(c) >= self.k - 1e-9

    def estado(self, c):
        return "VALIDADA" if self.validada(c) else "HIPOTESIS"

    def rivales(self, c):
        return [self.celulas[i] for i in sorted(self.adj.get(c.id, ()))]

    def _recalcula_adj(self, c):
        for i in self.adj.get(c.id, set()):
            self.adj[i].discard(c.id)
        self.adj[c.id] = set()
        for o in self.celulas:
            if o is not c and es_rival(o.af, c.af):
                self.adj[c.id].add(o.id)
                self.adj.setdefault(o.id, set()).add(c.id)

    def _grupos(self):
        vistos, grupos = set(), []
        for c in self.celulas:
            if c.id in vistos or not self.adj.get(c.id):
                continue
            pila, comp = [c.id], []
            while pila:
                i = pila.pop()
                if i in vistos:
                    continue
                vistos.add(i)
                comp.append(self.celulas[i])
                pila.extend(self.adj[i] - vistos)
            grupos.append(comp)
        return grupos

    def _rep_desde(self, estados, excluir=()):
        """Reputación de cada fuente a partir de qué células suyas ganan o pierden (sin las de `excluir`)."""
        pierde, gana = {}, {}
        for c in self.celulas:
            if c.id in excluir or estados.get(c.id) is None:
                continue
            d = pierde if estados[c.id] == "pierde" else gana
            for f in set(c.fuentes):
                d[f] = d.get(f, 0) + 1
        return {f: min(1.0, max(0.0, 1.0 - self.castigo * pierde.get(f, 0) + self.premio * gana.get(f, 0))) for f in self.rep}

    def _recalcula(self):
        """Punto fijo de (estados de grupo -> reputación -> estados de grupo). Devuelve sucesos de cambio."""
        grupos = self._grupos()
        # SIEMPRE desde cero: la reputación es función de la evidencia actual, no una cicatriz acumulada
        # (arrancar del estado anterior hacía que un veredicto prematuro se autorreforzara: visto en la semilla 0)
        estados = {c.id: None for c in self.celulas}
        for _ in range(MAX_PASADAS):
            nuevo = {}
            for G in grupos:
                ids = {c.id for c in G}
                rep_fuera = self._rep_desde(estados, excluir=ids)
                pesos = {c.id: self.W(c, rep_fuera) for c in G}
                gana = [c for c in G if pesos[c.id] >= self.k - 1e-9
                        and all(pesos[c.id] > pesos[o.id] + 1e-9 for o in G if o is not c)]
                if gana:
                    for c in G:
                        nuevo[c.id] = "gana" if c is gana[0] else "pierde"
            if nuevo == {i: e for i, e in estados.items() if e is not None}:
                break
            estados = dict.fromkeys(estados, None)
            estados.update(nuevo)
        else:
            self.no_convergio += 1
        suc = []
        for c in self.celulas:
            e = estados.get(c.id)
            if e != c.estado_grupo:
                c.estado_grupo = e
                for f in set(c.fuentes):
                    suc.append(f"{'castiga' if e == 'pierde' else ('premia' if e == 'gana' else 'absuelve')}:{f}")
                    self.registro.append((self.t, f, "castiga" if e == "pierde" else ("premia" if e == "gana" else "absuelve"), c.id))
        self.rep = self._rep_desde(estados)
        for c in self.celulas:
            if self.validada(c) and c.t_valida is None:
                c.t_valida = self.t
        return suc

    # ---------- enseñar ----------
    def ensena(self, fuente, frase, valor, atributo=""):
        """valor/atributo = lo que el cuerpo extrajo ('' si falló). Devuelve (sucesos, célula)."""
        self.t += 1
        self.idx.agrega(tokens(frase))
        self.rep.setdefault(fuente, 1.0)
        af = Afirmacion(frase, valor, atributo)
        cel = None
        if af.tv:
            for c in self.celulas:
                if c.af.tv and es_misma(c.af, af):
                    cel = c
                    break
        else:
            for c in self.celulas:                        # sin dato extraído: sólo frases casi idénticas
                if self._casi_identica(c, frase):
                    cel = c
                    break
        suc = []
        if cel is None:
            cel = Celula(len(self.celulas), af, self.t)
            self.celulas.append(cel)
            self._recalcula_adj(cel)
            suc.append("nace")
        else:
            suc.append("confirma" if fuente not in cel.fuentes else "repite")
            cambia = False
            if af.tv and len(af.valor) < len(cel.af.valor):
                cel.af.valor, cel.af.tv = af.valor, af.tv      # valor canónico: el más corto
                cambia = True
            if not cel.af.atrib and af.atrib:
                cel.af.atrib = af.atrib
                cambia = True
            if cambia:
                self._recalcula_adj(cel)
        antes = self.validada(cel)
        cel.frases.append((fuente, frase))
        cel.fuentes.append(fuente)
        if not antes and self.validada(cel):
            cel.t_valida = self.t
            suc.append("valida")
        self.registro += [(self.t, fuente, s, cel.id) for s in suc]
        if self.reputacion:
            suc += self._recalcula()
        return suc, cel

    def _casi_identica(self, c, frase):
        tf = tokens(frase)
        for _, f in c.frases:
            tg = tokens(f)
            if 0.5 * (cubre(self.idx, tf, tg) + cubre(self.idx, tg, tf)) >= 0.90:
                return True
        return False

    def baraja_reputacion(self, rng):
        """CONTROL que puede fallar: la reputación aprendida se reparte al azar entre las fuentes."""
        fs = sorted(self.rep)
        vals = [self.rep[f] for f in fs]
        rng.shuffle(vals)
        self.rep = dict(zip(fs, vals))

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
        pesos = {c.id: self.W(c) for c in cs}
        voz = []
        for c in cs:
            if not self.validada(c):
                continue
            otras = [o for o in cs if o is not c]
            if all(pesos[c.id] > pesos[o.id] + 1e-9 for o in otras):
                voz.append(c)
            elif self.recencia:
                empatan = [o for o in otras if abs(pesos[o.id] - pesos[c.id]) <= 1e-9]
                if (all(pesos[c.id] > pesos[o.id] + 1e-9 for o in otras if o not in empatan)
                        and all(es_rival(o.af, c.af) and (o.t_valida or 0) < (c.t_valida or 0) for o in empatan)):
                    voz.append(c)
        return ("VALIDADO" if voz else "DUDA"), voz, [c for c in cs if c not in voz], cand[0][0]

    def resumen(self):
        v = sum(self.validada(c) for c in self.celulas)
        return {"celulas": len(self.celulas), "validadas": v, "hipotesis": len(self.celulas) - v,
                "rep": {f: round(r, 2) for f, r in sorted(self.rep.items())}, "no_convergio": self.no_convergio}


class MemoriaIngenua:
    """Rival (b) de v0: guarda todo y recupera las 3 frases más parecidas. Cree todo."""
    def __init__(self, top=3):
        self.frases, self.idx, self.top = [], Indice(), top

    def ensena(self, fuente, frase, valor="", atributo=""):
        self.idx.agrega(tokens(frase))
        self.frases.append((fuente, frase, norm(valor)))

    def consulta(self, pregunta):
        p = [(parecido_pregunta(self.idx, pregunta, f), i) for i, (_, f, _) in enumerate(self.frases)]
        p = sorted([x for x in p if x[0] >= UMBRAL_Q], key=lambda x: (-x[0], x[1]))[: self.top]
        return [(self.frases[i][0], self.frases[i][1]) for _, i in sorted(p, key=lambda x: x[1])]


class MemoriaVoto(MemoriaIngenua):
    """Rival FUERTE: recuperación + VOTO POR MAYORÍA DE FUENTES. Agrupa las frases recuperadas por el valor
    que el cuerpo extrajo (un valor contenido en otro es el mismo voto); gana el valor con más fuentes
    DISTINTAS (empate: el más reciente). Si el ganador tiene menos de `minimo` fuentes, DUDA
    (minimo=1: cree a cualquiera; minimo=3: exige tres)."""
    def __init__(self, minimo=1, top=8):
        super().__init__(top=top)
        self.minimo = minimo

    def consulta(self, pregunta):
        p = [(parecido_pregunta(self.idx, pregunta, f), i) for i, (_, f, _) in enumerate(self.frases)]
        p = sorted([x for x in p if x[0] >= UMBRAL_Q], key=lambda x: (-x[0], x[1]))[: self.top]
        if not p:
            return "NADA", [], {}
        grupos = []                                        # [{valor, sig, fuentes, frases, t}]
        for _, i in sorted(p, key=lambda x: x[1]):
            fuente, frase, valor = self.frases[i]
            g = None
            sig = (propios(frase) | set(tokens(valor))) if valor else set()   # misma firma de entidades = mismo voto
            if sig:
                for g2 in grupos:
                    if g2["sig"] and (_subconjunto(sig, g2["sig"]) or _subconjunto(g2["sig"], sig)):
                        g = g2
                        break
            if g is None:
                g = {"valor": valor or f"#{i}", "sig": sig, "fuentes": set(), "frases": [], "t": -1}
                grupos.append(g)
            g["fuentes"].add(fuente)
            g["frases"].append((fuente, frase))
            g["t"] = max(g["t"], i)
        orden = sorted(grupos, key=lambda g: (-len(g["fuentes"]), -g["t"]))
        mejor = orden[0]
        votos = {g["valor"]: len(g["fuentes"]) for g in grupos}
        if len(mejor["fuentes"]) < self.minimo:
            return "DUDA", [], votos
        return "VOTO", mejor["frases"][-3:], votos
