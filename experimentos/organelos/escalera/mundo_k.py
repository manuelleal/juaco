"""mundo_k.py — VARIANTE del mundo del tramo C SOLO para el humo 3 de P9: la letra nueva (K) tiene VIDA UTIL. 30-sep-2026, MODO RAFAGA.
Por que: en los humos 1 y 2 de P9 la K neutra (nadie la come tras probarla una vez) se ACUMULA y desplaza la comida (mundo A+C 4.0 contra ~7):
una letra que nadie consume tapa el mundo. Aqui el mundo retira cada K con mas de K_VIDA pasos (regla determinista, sin rng; la reposicion
normal la reemplaza en la siguiente mordida/olvido). Con K_VIDA 0 es mundo_tramo_c bit a bit (misma clase, mismo codigo transformado).
Se construye con las MISMAS anclas de mundo_tramo_c (que NO se toca: su sha esta fijado en P7 y P10); solo cambia la clase del oasis.
"""
import os, sys
AQUI = os.path.dirname(os.path.abspath(__file__))
if AQUI not in sys.path: sys.path.insert(0, AQUI)
import mundo_tramo_c as MC
P = MC.P; ME = MC.ME

K_VIDA = 500
_RUN = [None]


class OasisK(MC.OasisC):
    def __init__(self, *a, **k):
        super().__init__(*a, **k)
        self.k_vida = int(K_VIDA); self.t_nace = {}; self.retiradas = 0

    def paso(self, lin, objs):
        if self.X and self.k_vida:
            for x in list(objs):
                if objs[x] == self.X:
                    if x not in self.t_nace: self.t_nace[x] = self.t
                    elif self.t - self.t_nace[x] > self.k_vida: del objs[x]; self.t_nace.pop(x); self.retiradas += 1
            for x in list(self.t_nace):
                if objs.get(x) != self.X: self.t_nace.pop(x)
        super().paso(lin, objs)

    def info(self):
        d = super().info()
        if self.X: d.update(k_vida=self.k_vida, k_retiradas=self.retiradas)
        return d


def construye():
    if _RUN[0] is not None: return _RUN[0]
    MC.construye()   # verifica shas y anclas
    rp = os.path.join(MC.PISTA_D, 'pista.py')
    txt = open(rp, encoding='utf-8').read()
    a = txt.index("def run(seed, carros,"); b = txt.index("\n\n\n# claves de primer nivel")
    src = txt[a:b] + "\n"
    for viejo, nuevo in ME.ANCLAS + MC.ANCLAS_C:
        if src.count(viejo) != 1: raise SystemExit(f"MUNDO_K: ancla {viejo[:60]!r}")
        src = src.replace(viejo, nuevo)
    ns = dict(vars(P)); ns.update(Oasis=ME.Oasis, OasisC=OasisK, EXTRA=ME.EXTRA, POBRE=ME.POBRE, D_LLAVE=MC.D_LLAVE, IDX=dict(P.IDX, **{x: MC.IDX_X for x in MC.LETRAS_X}))
    exec(compile(src, '<mundo_k.run = mundo_tramo_c con OasisK>', 'exec'), ns)
    _RUN[0] = (ns['run'], dict(MC.construye()[1], oasis='OasisK', k_vida=K_VIDA))
    return _RUN[0]


def run(*a, **k):
    return construye()[0](*a, **k)
