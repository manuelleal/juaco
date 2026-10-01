"""mundo_plus.py — SONDA 1 (1-oct-2026, MODO RAFAGA, EXPLORATORIA): mundo con LLAVE NO LETAL. La base vive sin llave (el oasis paga lo
de P1: extra) y la llave K da un PLUS: un bocado A/C DENTRO del oasis paga +plus en las dos necesidades si el cuerpo mordio K hace <= d_plus pasos.

MISION: llegar a la AGI por este camino (organismo minimo con reglas locales, sin retropropagacion, peldanos preregistrados con controles y replicas).

CONSTRUCCION: las MISMAS anclas de mundo_tramo_c (que NO se toca: se importa y su construye() verifica shas); solo cambia la clase del oasis
(patron de mundo_k.py). PERILLAS (dict de modulo, lo fija el runner ANTES de cada corrida; todas apagadas => mundo_tramo_c BIT A BIT, arnes):
  plus       0.0  : lo que la llave agrega (a E y a Ag) a un bocado A/C dentro del oasis
  d_plus     600  : la llave dura d_plus pasos (por cuerpo; la muerte la borra)
  extra_sin  None : si no es None, SIN llave el extra del oasis vale extra_sin (en vez de extra); con llave, extra + plus
  regalo     0    : 1 = el mundo regala la llave (todo bocado dentro cuenta como con llave): la cota dura
  adelanta   0    : (humo 4) con llave, un bocado A/C dentro ADELANTA la ventana de parto del cuerpo en `adelanta` pasos (solo si ya corre:
                    l.gv > 0). Un plus REPRODUCTIVO en vez de energetico: no lo come el tope de niveles (1.5) ni el gasto fijo.
Exige letra_x 'K' y cerrojo 0 (el cerrojo viejo QUITA el extra; aqui la llave solo AGREGA).
MEDIDA (fisica de solo lectura, por linaje): bocados dentro con/sin llave, mordidas de K, ganancia nominal y EFECTIVA (despues del tope 1.5 de la
pista) de todas las mordidas, y la parte efectiva del plus (contrafactual en los mismos niveles: lo que la llave dio de verdad tras el tope).
"""
import os, sys
AQUI = os.path.dirname(os.path.abspath(__file__))
ESC = os.path.dirname(AQUI)
if ESC not in sys.path: sys.path.insert(0, ESC)
import mundo_tramo_c as MC
P = MC.P; ME = MC.ME

SHA_MC = None   # el sha de mundo_tramo_c lo verifica MC.construye() (cadena de shas fijados) y se reporta en info
PERILLAS0 = dict(plus=0.0, d_plus=600, extra_sin=None, regalo=0, adelanta=0)
PERILLAS = dict(PERILLAS0)
TOPE = 1.5      # el tope de niveles de pista.run (min(l.E + dS, 1.5)); solo para la contabilidad de ganancia efectiva
_RUN = [None]


def _ef(l, r):
    return (min(l.E + r[0], TOPE) - l.E) + (min(l.Ag + r[1], TOPE) - l.Ag)


class OasisPlus(MC.OasisC):
    def __init__(self, *a, **k):
        super().__init__(*a, **k)
        p = PERILLAS
        self.plus = float(p['plus']); self.d_plus = int(p['d_plus']); self.regalo = int(bool(p['regalo']))
        self.extra_sin = None if p['extra_sin'] is None else float(p['extra_sin'])
        self.adelanta = int(p['adelanta'])
        self.act_plus = bool(self.plus or self.extra_sin is not None or self.regalo or self.adelanta)
        if self.act_plus and (self.cerrojo or self.X != 'K' or self.mueve): raise SystemExit("MUNDO_PLUS: exige letra_x 'K', cerrojo 0 y mueve 0")
        if self.plus < 0 or self.d_plus <= 0 or self.adelanta < 0: raise SystemExit("MUNDO_PLUS: plus >= 0 y d_plus > 0")
        n = self.n
        self.t_k = [-10 ** 9] * n; self.kp = [0] * n; self.con_p = [0] * n; self.sin_p = [0] * n
        self.adel = [0] * n
        self.g_nom = [0.0] * n; self.g_ef = [0.0] * n; self.plus_nom = [0.0] * n; self.plus_ef = [0.0] * n

    def muerde(self, l, kk, pos, dS):
        r = super().muerde(l, kk, pos, dS)
        if not self.act_plus: return r
        i = l.i
        if kk == self.X:
            self.t_k[i] = self.t; self.kp[i] += 1
        elif kk in ('A', 'C') and pos in self.celdas:
            r_sin = r
            if self.extra_sin is not None:
                j = 1 if kk == 'A' else 0   # la OTRA necesidad (donde cae el extra)
                z = [r[0], r[1]]; z[j] += self.extra_sin - self.extra; r_sin = (z[0], z[1])
            if self.regalo or (self.t - self.t_k[i] <= self.d_plus):
                self.con_p[i] += 1
                r = (r[0] + self.plus, r[1] + self.plus)
                self.plus_nom[i] += (r[0] + r[1]) - (r_sin[0] + r_sin[1]); self.plus_ef[i] += _ef(l, r) - _ef(l, r_sin)
                if self.adelanta and l.gv > 0: l.gv += self.adelanta; self.adel[i] += 1
            else:
                self.sin_p[i] += 1; r = r_sin
        self.g_nom[i] += r[0] + r[1]; self.g_ef[i] += _ef(l, r)
        return r

    def muere(self, l):
        super().muere(l); self.t_k[l.i] = -10 ** 9

    def salida(self, i):
        d = super().salida(i)
        if self.act_plus:
            d['plus'] = dict(con=self.con_p[i], sin=self.sin_p[i], mord_K=self.kp[i], g_nom=round(self.g_nom[i], 4), g_ef=round(self.g_ef[i], 4),
                             plus_nom=round(self.plus_nom[i], 4), plus_ef=round(self.plus_ef[i], 4), adel=self.adel[i])
        return d

    def info(self):
        d = super().info()
        if self.act_plus: d.update(plus=self.plus, d_plus=self.d_plus, extra_sin=self.extra_sin, regalo=self.regalo, adelanta=self.adelanta)
        return d


def fija(**k):
    """fija las perillas para la PROXIMA corrida (las no dadas vuelven a fabrica = apagadas)."""
    for x in k:
        if x not in PERILLAS0: raise SystemExit(f"MUNDO_PLUS: perilla desconocida {x}")
    PERILLAS.clear(); PERILLAS.update(PERILLAS0); PERILLAS.update(k)
    return dict(PERILLAS)


def construye():
    if _RUN[0] is not None: return _RUN[0]
    inf = MC.construye()[1]   # verifica shas (pista, juez, mundo_escalera) y anclas
    rp = os.path.join(MC.PISTA_D, 'pista.py')
    txt = open(rp, encoding='utf-8').read()
    a = txt.index("def run(seed, carros,"); b = txt.index("\n\n\n# claves de primer nivel")
    src = txt[a:b] + "\n"
    for viejo, nuevo in ME.ANCLAS + MC.ANCLAS_C:
        if src.count(viejo) != 1: raise SystemExit(f"MUNDO_PLUS: ancla {viejo[:60]!r}")
        src = src.replace(viejo, nuevo)
    if MC.h16s(src) != inf['sha_fuente_transformada']: raise SystemExit("MUNDO_PLUS: la fuente transformada no es la de mundo_tramo_c")
    ns = dict(vars(P)); ns.update(Oasis=ME.Oasis, OasisC=OasisPlus, EXTRA=ME.EXTRA, POBRE=ME.POBRE, D_LLAVE=MC.D_LLAVE, IDX=dict(P.IDX, **{x: MC.IDX_X for x in MC.LETRAS_X}))
    exec(compile(src, '<mundo_plus.run = mundo_tramo_c con OasisPlus>', 'exec'), ns)
    _RUN[0] = (ns['run'], dict(inf, oasis='OasisPlus', sha_mundo_tramo_c=MC.h16(os.path.join(ESC, 'mundo_tramo_c.py'))))
    return _RUN[0]


def run(*a, **k):
    return construye()[0](*a, **k)


if __name__ == '__main__':
    print(construye()[1])
