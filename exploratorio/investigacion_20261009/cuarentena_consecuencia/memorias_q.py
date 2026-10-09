# -*- coding: utf-8 -*-
"""Memorias nuevas de la cuarentena por CONSECUENCIA (reglas locales, sin punto fijo global, sin gradiente).

ColoniaQ        (brazo q) hereda de Colonia (v1) la fusión de células y la compuerta; cambia SÓLO el peso y la voz.
  - Por fuente dos contadores: aciertos y fallos VERIFICADOS por el oráculo de consecuencia.
      peso(f) = 0 si fallos(f) >= 1;  si no, min(1.0, PROBACION + SUBE * aciertos(f)).   PROBACION 0.5, SUBE 0.25.
      (caer a 0 es definitivo dentro del experimento: no hay rehabilitación; declarado.)
  - Una célula tiene VOZ si la suma de pesos de sus fuentes distintas >= 2.0, o si su predicción en sombra fue
    verificada por el oráculo. Sin voz predice EN SOMBRA: cuando el mundo revela la verdad de la pregunta, el
    valor de la célula (sus frases) se compara con la verdad.
  - Acierto verificado: la célula queda VERIFICADA (voz propia) y cada fuente suya suma un acierto (una vez por
    fuente y célula). Fallo verificado: la célula queda REFUTADA (si tenía voz vuelve a hipótesis y se anota;
    no vuelve a hablar) y cada fuente suya suma un fallo.
  - La hipótesis sin voz muere a las T rondas sin confirmarse (T = 3): se vacía.
  Perillas apagadas (probacion = 1.0, sin oráculo, sin muerte) = Colonia(k=2) de v1, bit a bit (arnés).
  Controles: sin_reputacion (peso fijo 0.5: sólo probación + verificación propia); perm (los veredictos del
  oráculo se acreditan a OTRA fuente: permutación sin puntos fijos entre las fuentes persistentes).

MemoriaVotoLN   (brazo bv2+LN, RIVAL FUERTE) hereda de MemoriaVoto (v1): voto >= 2 fuentes distintas + LISTA NEGRA
  de la fuente tras una mentira verificada por el oráculo + BORRAR lo refutado. Recibe EXACTAMENTE las mismas
  revelaciones que q y también las usa sobre lo que NO tenía voto (versión fuerte: no espera a equivocarse en
  voz alta). Una fuente en lista negra deja de votar en todo, pasado y futuro.
  guarda_verificado=True (brazo bv2+LN+V, rival MÁS fuerte, diagnóstico): además, lo que el oráculo verificó
  habla aunque tenga una sola fuente (lo mismo que q recibe del oráculo por su "verificación propia").
  Sin revelaciones = MemoriaVoto(minimo=2) de v1, bit a bit (arnés).

MemoriaOraculo  (brazo o, piso) ignora a las fuentes: sólo guarda lo que el oráculo reveló.
CuerpoRegalo    (HUMO 0, sin modelo) el "cuerpo" devuelve las frases que le dan como contexto, o NO LO SÉ.
"""
from colonia import Colonia, MemoriaVoto, UMBRAL_Q, parecido_pregunta, propios, tokens, _subconjunto
from mundo import contiene

PROBACION = 0.5
SUBE = 0.25
UMBRAL_VOZ = 2.0
T_MUERTE = 3
BONO_VERIFICADA = 10.0


class ColoniaQ(Colonia):
    def __init__(self, probacion=PROBACION, sube=SUBE, umbral=UMBRAL_VOZ, T=T_MUERTE, sin_reputacion=False,
                 perm=None):
        super().__init__(k=umbral, reputacion=False, recencia=False)
        self.probacion, self.sube, self.T = probacion, sube, T
        self.sin_reputacion = sin_reputacion
        self.perm = perm or {}
        self.aciertos, self.fallos = {}, {}
        self.meta = {}                 # id -> {verificada, refutada, muerta, ronda_conf, acreditadas}
        self.ronda = 1
        self.gastadas = 0              # revelaciones del oráculo que se compararon con algo guardado
        self.utiles = 0                # ... y que cambiaron el estado (veredicto nuevo)
        self.vuelve = 0                # células con voz que fallaron y volvieron a hipótesis
        self.muertas = 0

    # ---------- peso y voz ----------
    def peso(self, f):
        if self.sin_reputacion:
            return self.probacion
        if self.fallos.get(f, 0) >= 1:
            return 0.0
        return min(1.0, self.probacion + self.sube * self.aciertos.get(f, 0))

    def _m(self, c):
        m = self.meta.get(c.id)
        if m is None:
            m = self.meta[c.id] = {"verificada": False, "refutada": False, "muerta": False,
                                   "ronda_conf": self.ronda, "acreditadas": set()}
        return m

    def W(self, c, rep=None):
        m = self._m(c)
        if m["muerta"] or m["refutada"]:
            return 0.0
        w = sum(self.peso(f) for f in set(c.fuentes))
        return w + (BONO_VERIFICADA if m["verificada"] else 0.0)

    # ---------- enseñar ----------
    def ensena(self, fuente, frase, valor, atributo=""):
        suc, cel = super().ensena(fuente, frase, valor, atributo)
        m = self._m(cel)
        if "nace" in suc or "confirma" in suc:
            m["ronda_conf"] = self.ronda
        return suc, cel

    def candidatas(self, texto, umbral=UMBRAL_Q):
        out = []
        for c in self.celulas:
            if not c.frases:                       # muerta (vaciada)
                continue
            s = max(parecido_pregunta(self.idx, texto, f) for _, f in c.frases)
            if s >= umbral:
                out.append((s, c))
        return sorted(out, key=lambda x: (-x[0], x[1].id))

    # ---------- consecuencia ----------
    def _acredita(self, f, acierto):
        g = self.perm.get(f, f)
        d = self.aciertos if acierto else self.fallos
        d[g] = d.get(g, 0) + 1

    def revela(self, pregunta, verdad):
        """El mundo reveló la verdad de esta pregunta. Devuelve True si se gastó (se comparó con algo guardado)."""
        cand = [c for _, c in self.candidatas(pregunta)]
        if not cand:
            return False
        self.gastadas += 1
        cambio = False
        for c in cand:
            m = self._m(c)
            ok = any(contiene(f, verdad) for _, f in c.frases)
            if ok:
                if not m["verificada"]:
                    m["verificada"], cambio = True, True
                    self.registro.append((self.t, "", "verifica", c.id))
            else:
                if not m["refutada"]:
                    if self.validada(c):
                        self.vuelve += 1
                        self.registro.append((self.t, "", "vuelve_a_hipotesis", c.id))
                    m["refutada"], m["verificada"], cambio = True, False, True
                    self.registro.append((self.t, "", "refuta", c.id))
            for f in sorted(set(c.fuentes) - m["acreditadas"]):
                m["acreditadas"].add(f)
                self._acredita(f, ok)
                cambio = True
        self.utiles += cambio
        return True

    def fin_ronda(self, r):
        for c in self.celulas:
            m = self._m(c)
            if m["muerta"] or not c.frases:
                continue
            if not self.validada(c) and (r - m["ronda_conf"] + 1) >= self.T:
                m["muerta"] = True
                self.muertas += 1
                self.registro.append((self.t, "", "muere", c.id))
                c.frases, c.fuentes = [], []
                c.af.tv = set()                     # no vuelve a fusionar ni a ser rival
                self._recalcula_adj(c)
        self.ronda = r + 1

    def resumen(self):
        fs = sorted(set(self.rep) | set(self.aciertos) | set(self.fallos))
        return {"celulas": len(self.celulas), "con_voz": sum(bool(c.frases) and self.validada(c) for c in self.celulas),
                "verificadas": sum(m["verificada"] for m in self.meta.values()),
                "refutadas": sum(m["refutada"] for m in self.meta.values()), "muertas": self.muertas,
                "vuelve_a_hipotesis": self.vuelve, "gastadas": self.gastadas, "utiles": self.utiles,
                "peso": {f: round(self.peso(f), 2) for f in fs},
                "aciertos": dict(sorted(self.aciertos.items())), "fallos": dict(sorted(self.fallos.items()))}


class MemoriaVotoLN(MemoriaVoto):
    def __init__(self, minimo=2, top=8, guarda_verificado=False):
        super().__init__(minimo=minimo, top=top)
        self.guarda_verificado = guarda_verificado
        self.negra, self.borradas, self.verificadas = set(), set(), set()
        self.gastadas = 0
        self.utiles = 0

    def _vivas(self, pregunta):
        p = [(parecido_pregunta(self.idx, pregunta, f), i) for i, (fu, f, _) in enumerate(self.frases)
             if i not in self.borradas and (fu not in self.negra or (self.guarda_verificado and i in self.verificadas))]
        return sorted([x for x in p if x[0] >= UMBRAL_Q], key=lambda x: (-x[0], x[1]))

    def consulta(self, pregunta):
        p = self._vivas(pregunta)[: self.top]
        if not p:
            return "NADA", [], {}
        grupos = []
        for _, i in sorted(p, key=lambda x: x[1]):
            fuente, frase, valor = self.frases[i]
            g = None
            sig = (propios(frase) | set(tokens(valor))) if valor else set()
            if sig:
                for g2 in grupos:
                    if g2["sig"] and (_subconjunto(sig, g2["sig"]) or _subconjunto(g2["sig"], sig)):
                        g = g2
                        break
            if g is None:
                g = {"valor": valor or f"#{i}", "sig": sig, "fuentes": set(), "frases": [], "t": -1, "ver": False}
                grupos.append(g)
            g["fuentes"].add(fuente)
            g["frases"].append((fuente, frase))
            g["t"] = max(g["t"], i)
            g["ver"] = g["ver"] or (self.guarda_verificado and i in self.verificadas)
        orden = sorted(grupos, key=lambda g: (-int(g["ver"]), -len(g["fuentes"]), -g["t"]))
        mejor = orden[0]
        votos = {g["valor"]: len(g["fuentes"]) for g in grupos}
        if len(mejor["fuentes"]) < self.minimo and not mejor["ver"]:
            return "DUDA", [], votos
        return "VOTO", mejor["frases"][-3:], votos

    def revela(self, pregunta, verdad):
        p = self._vivas(pregunta)               # TODO lo guardado sobre la pregunta, tenga voto o no
        if not p:
            return False
        self.gastadas += 1
        cambio = False
        for _, i in p:
            fuente, frase, _ = self.frases[i]
            if contiene(frase, verdad):
                if i not in self.verificadas:
                    self.verificadas.add(i)
                    cambio = True
            else:
                self.borradas.add(i)
                self.negra.add(fuente)
                cambio = True
        self.utiles += cambio
        return True

    def resumen(self):
        return {"frases": len(self.frases), "borradas": len(self.borradas), "lista_negra": sorted(self.negra),
                "verificadas": len(self.verificadas), "gastadas": self.gastadas, "utiles": self.utiles}


class MemoriaOraculo:
    """Piso: no escucha a nadie; sólo recuerda lo que el mundo reveló."""
    def __init__(self):
        self.sabe = {}
        self.gastadas = 0
        self.utiles = 0

    def ensena(self, fuente, frase, valor="", atributo=""):
        pass

    def consulta(self, pregunta):
        return self.sabe.get(pregunta)

    def revela(self, pregunta, verdad):
        self.gastadas += 1
        if pregunta not in self.sabe:
            self.sabe[pregunta] = verdad
            self.utiles += 1
        return True

    def resumen(self):
        return {"sabe": len(self.sabe), "gastadas": self.gastadas, "utiles": self.utiles}


class CuerpoRegalo:
    """HUMO 0: sin modelo. Con contexto devuelve las frases dadas (el valor se regala); sin contexto, NO LO SÉ."""
    def __init__(self):
        self.n_llamadas = 0
        self.n_cache = 0
        self.seg_carga = 0.0

    def __enter__(self):
        return self

    def __exit__(self, *a):
        return False

    def chat(self, mensajes, max_tokens=48, esquema=None, usar_cache=True):
        self.n_llamadas += 1
        u = mensajes[-1]["content"]
        if u.startswith("Datos que te enseñaron:"):
            datos = u.split("\n\nPregunta:")[0].split("\n")[1:]
            texto = " ".join(d[2:] for d in datos)
        else:
            texto = "NO LO SÉ."
        return {"texto": texto, "seg": 0.0, "p_tokens": [1.0], "p_min": 1.0, "de_cache": False}
