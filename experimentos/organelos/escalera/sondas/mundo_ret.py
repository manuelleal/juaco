"""mundo_ret.py — SONDA 2 (1-oct-2026, MODO RAFAGA, EXPLORATORIA): mundo del tramo C con CELDA RETENIDA: la letra nueva (E) NUNCA nace dentro
del oasis. La letra se aprende solo FUERA; el lugar se aprende solo con A y C. La combinacion (E, dentro) no ocurre nunca en la crianza.

MISION: llegar a la AGI por este camino (organismo minimo con reglas locales, sin retropropagacion, peldanos preregistrados con controles y replicas).

CONSTRUCCION: las anclas de mundo_tramo_c (que NO se toca; su construye() verifica los shas) + UNA ancla sobre la fuente ya transformada: el sorteo de
la letra recibe la celda. RETENIDA (lista de modulo [0/1], la fija el runner): con 0 es mundo_tramo_c BIT A BIT (mismo sorteo, mismo rng: arnes).
Con 1: si la letra sorteada es la nueva y la celda esta dentro del oasis, se re-sortea entre ABCD (un sorteo de rng mas SOLO en ese caso).
Exige mueve 0 (el oasis no se muda: lo retenido es el arco de la corrida).
"""
import os, sys
AQUI = os.path.dirname(os.path.abspath(__file__))
ESC = os.path.dirname(AQUI)
if ESC not in sys.path: sys.path.insert(0, ESC)
import mundo_tramo_c as MC
P = MC.P; ME = MC.ME

RETENIDA = [0]
ANCLA_RET = ("else _oz.letra(rng))\n", "else _oz.letra_en(rng, x))\n")
_RUN = [None]


class OasisRet(MC.OasisC):
    def __init__(self, *a, **k):
        super().__init__(*a, **k)
        self.ret = int(bool(RETENIDA[0])); self.ret_n = 0
        if self.ret and (self.mueve or not self.X): raise SystemExit("MUNDO_RET: retenida exige letra_x y mueve 0")

    def letra_en(self, rng, x):
        k = self.letra(rng)
        if self.ret and k == self.X and x in self.celdas:
            self.ret_n += 1; k = P.TIPOS[int(rng.integers(len(P.TIPOS)))]
        return k

    def info(self):
        d = super().info()
        if self.ret: d.update(retenida=1, ret_n=self.ret_n)
        return d


def construye():
    if _RUN[0] is not None: return _RUN[0]
    inf = MC.construye()[1]
    rp = os.path.join(MC.PISTA_D, 'pista.py')
    txt = open(rp, encoding='utf-8').read()
    a = txt.index("def run(seed, carros,"); b = txt.index("\n\n\n# claves de primer nivel")
    src = txt[a:b] + "\n"
    for viejo, nuevo in ME.ANCLAS + MC.ANCLAS_C:
        if src.count(viejo) != 1: raise SystemExit(f"MUNDO_RET: ancla {viejo[:60]!r}")
        src = src.replace(viejo, nuevo)
    if MC.h16s(src) != inf['sha_fuente_transformada']: raise SystemExit("MUNDO_RET: la fuente transformada no es la de mundo_tramo_c")
    if src.count(ANCLA_RET[0]) != 1: raise SystemExit("MUNDO_RET: el ancla de la celda retenida no aparece exactamente 1 vez")
    src = src.replace(*ANCLA_RET)
    ns = dict(vars(P)); ns.update(Oasis=ME.Oasis, OasisC=OasisRet, EXTRA=ME.EXTRA, POBRE=ME.POBRE, D_LLAVE=MC.D_LLAVE, IDX=dict(P.IDX, **{x: MC.IDX_X for x in MC.LETRAS_X}))
    exec(compile(src, '<mundo_ret.run = mundo_tramo_c con OasisRet + 1 ancla>', 'exec'), ns)
    _RUN[0] = (ns['run'], dict(inf, oasis='OasisRet', anclas=inf['anclas'] + 1, sha_fuente_ret=MC.h16s(src), sha_mundo_tramo_c=MC.h16(os.path.join(ESC, 'mundo_tramo_c.py'))))
    return _RUN[0]


def run(*a, **k):
    return construye()[0](*a, **k)


if __name__ == '__main__':
    print(construye()[1])
