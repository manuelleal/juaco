"""mundo_tramo_c.py — EL MUNDO DEL TRAMO C de la escalera (peldanos 7-10) = mundo_escalera (P1: oasis) + CUATRO perillas, cada una
apagada deja el mundo anterior BIT A BIT (30-sep-2026, ingeniero genetico Fable, MODO RAFAGA). Plan: ESCALERA.md. Arnes: identidad_c.py.

MISION: llegar a la AGI por este camino (organismo minimo con reglas locales, sin retropropagacion, peldanos preregistrados con
controles y replicas).

QUE ES: pista.py (sha SHA_PISTA) transformada por las 9 anclas de mundo_escalera.py (sha SHA_ME, que NO se toca: se importan sus anclas y
su clase Oasis) y despues por las anclas de ESTE modulo. Con todas las perillas nuevas apagadas run() ES mundo_escalera.run bit a bit
(arnes M0); con oasis 0 ademas ES pista.run bit a bit (por el arnes de P1). Las perillas (una por peldano):
  c_e      (P7, 0.0 = apagada): COSTO DE EMITIR: cada escritura aceptada en la pizarra cuesta c_e de E al cuerpo que escribe (en el acto,
           fase A). Evitar (no escribir) es gratis para el emisor; hablar cuesta. Se cuenta por linaje (cobros).
  letra_x  (P8 / P9, None = apagada): UNA LETRA NUEVA en el mundo con efecto nominal efecto_x = (dE, dAg) y probabilidad p_x de nacer en
           cada reposicion (si no, una de ABCD uniforme: con p_x 0 el sorteo es el de la pista). Exige oasis 1. Dentro del oasis, una
           letra que ALIMENTA una necesidad recibe +extra en la OTRA (la misma regla que A y C); una letra neutra (0, 0) no recibe nada;
           fuera, su efecto nominal (no se empobrece: declarado). P8: 'E' (sal dulce: (+0.3, -0.1): mixta fuera, buena dentro).
           P9: 'K' (la llave: (0, 0): no da ni quita; evitarla es gratis). Contabilidad: la letra entra en mord/vis/enc/... del linaje
           (claves nuevas; las de ABCD no cambian) y el juez la ve como una letra mas.
  cerrojo  (P9, 0 = apagado): el oasis SOLO paga (extra) si el cuerpo lleva LLAVE = mordio letra_x hace <= d_llave pasos (por cuerpo; la
           muerte la borra). Sin llave, dentro A y C valen lo pobre (como fuera). Exige letra_x.
  mueve    (P10, 0 = apagado): cada `mueve` pasos el oasis SE MUDA a un arco nuevo (rng de la zona [seed, 0, 18, 0], la MISMA corriente
           que sorteo el primero; se re-sortea hasta que no se solape con el anterior). Lo recordado caduca.
SALIDA NUEVA (solo con alguna perilla): pista['oasis'] agrega c_e, letra_x, cerrojo, mueve, mudanzas [(t, z0)]; por linaje
d['_carrera']['oasis'] agrega cobros (P7), x = exposiciones/mordidas de la letra nueva y las exposiciones FRIAS (P8), llave = mordidas A+C
dentro con/sin llave (P9), latencias = pasos hasta el primer bocado A+C dentro de cada oasis nuevo (P10). Todo es fisica de solo lectura.
"""
import hashlib, os, sys
import numpy as np

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(AQUI)))
PISTA_D = os.path.join(RAIZ, 'experimentos', 'carrera_escuderias')
for _d in (AQUI, PISTA_D):
    if _d not in sys.path: sys.path.insert(0, _d)
import pista as P
import mundo_escalera as ME

SHAS_FIJOS = dict(mundo_escalera='4f28b372207ba0a6')   # mundo_escalera.py commiteado en 76dc3d11 (P1); si P1 cambia, re-fijar aqui
D_LLAVE = 1500
LETRAS_X = ('E', 'K')
CAT_X = {'E': 'dulce', 'K': 'llave'}
IDX_X = 4

FIRMA_ME = ME.FIRMA_NUEVA
FIRMA_C = FIRMA_ME[:-2] + ", c_e=0.0, letra_x=None, efecto_x=(0.0, 0.0), p_x=0.0, cerrojo=0, d_llave=D_LLAVE, mueve=0, cerrojo_pobre=1):"
# cerrojo_pobre (P9, humo 2; 1 = humo 1, bit a bit): con 1, dentro SIN llave A y C valen lo pobre (como fuera); con 0 valen lo NOMINAL (0.8 en su
# necesidad, sin el extra): la llave sigue pagando el doble, pero el oasis sin llave ya no mata (humo 1: los tres brazos colapsaban, vida 200).
ANCLAS_C = [
    (FIRMA_ME, FIRMA_C),
    ("    _oz = (Oasis(seed, L, n, T, extra, pobre, dens, vista_r) if oasis else None)\n",
     "    _oz = (OasisC(seed, L, n, T, extra, pobre, dens, vista_r, c_e, letra_x, efecto_x, p_x, cerrojo, d_llave, mueve, cerrojo_pobre) if oasis else None)\n"
     "    if _oz is None and (c_e or letra_x is not None or cerrojo or mueve): raise SystemExit('MUNDO_TRAMO_C: las perillas del tramo C exigen oasis 1')\n"
     "    if _oz is not None and _oz.X: VAL_VIVO, EFECTO = _oz.extiende(lin, VAL_VIVO, EFECTO)\n"),
    # P8/P9: la letra nueva nace con probabilidad p_x (consume sorteos SOLO con p_x > 0)
    ("            if x not in objs: objs[x] = TIPOS[int(rng.integers(len(TIPOS)))]\n",
     "            if x not in objs: objs[x] = (TIPOS[int(rng.integers(len(TIPOS)))] if (_oz is None or not _oz.px) else _oz.letra(rng))\n"),
    # P7: el costo de emitir (solo escrituras aceptadas)
    ("                if pizarra: pend.append((t, l.id, _valida_escritura(es)))\n",
     "                if pizarra:\n"
     "                    pend.append((t, l.id, _valida_escritura(es)))\n"
     "                    if _oz is not None and _oz.c_e: _oz.cobra(l)\n"),
    # P8: exposicion (llegada a una celda con la letra nueva, mordida o no) ANTES de que la pista actualice prev_on
    ("            c.resultado(res)\n            l.prev_on = pos if pos in objs else -1\n",
     "            c.resultado(res)\n"
     "            if _oz is not None and _oz.X: _oz.expone(l, res, pos)\n"
     "            l.prev_on = pos if pos in objs else -1\n"),
    # P9: la muerte borra la llave (y cierra la vida para las exposiciones frias)
    ("                l.deaths += 1; l.mnec[0 if por_E else 1] += 1; l.E = .6; l.Ag = .6\n",
     "                l.deaths += 1; l.mnec[0 if por_E else 1] += 1; l.E = .6; l.Ag = .6\n"
     "                if _oz is not None: _oz.muere(l)\n"),
    ("    comp = {k: 0 for k in TIPOS}           # SOLO LECTURA: composicion del mundo al inicio de cada paso\n",
     "    comp = {k: 0 for k in TIPOS + ((_oz.X,) if (_oz is not None and _oz.X) else ())}           # SOLO LECTURA: composicion del mundo al inicio de cada paso\n"),
    ("    comp_q = [{k: 0 for k in TIPOS} for _ in range(4)]   # idem por cuarto de T (composicion EN EL TIEMPO)\n",
     "    comp_q = [{k: 0 for k in TIPOS + ((_oz.X,) if (_oz is not None and _oz.X) else ())} for _ in range(4)]   # idem por cuarto de T (composicion EN EL TIEMPO)\n"),
]
_RUN = [None]


def h16(p): return hashlib.sha256(open(p, 'rb').read()).hexdigest()[:16]
def h16s(s): return hashlib.sha256(s.encode('utf-8')).hexdigest()[:16]


class OasisC(ME.Oasis):
    """El oasis de P1 + las perillas del tramo C. Con todas apagadas se comporta EXACTAMENTE como ME.Oasis (mismos metodos, sin rng)."""

    def __init__(self, seed, L, n, T, extra, pobre, dens, vista, c_e=0.0, X=None, efecto_x=(0.0, 0.0), px=0.0, cerrojo=0, d_llave=D_LLAVE, mueve=0, cerrojo_pobre=1):
        super().__init__(seed, L, n, T, extra, pobre, dens, vista)
        self.c_e = float(c_e); self.X = X; self.ex = (float(efecto_x[0]), float(efecto_x[1])); self.px = float(px)
        self.cerrojo = int(bool(cerrojo)); self.d_llave = int(d_llave); self.mueve = int(mueve); self.n = n; self.cerrojo_pobre = int(bool(cerrojo_pobre))
        if self.c_e < 0 or not 0 <= self.px <= 1 or self.d_llave <= 0 or self.mueve < 0: raise SystemExit("MUNDO_TRAMO_C: c_e >= 0, p_x en [0, 1], d_llave > 0, mueve >= 0")
        if X is not None and (X not in LETRAS_X or not self.px): raise SystemExit(f"MUNDO_TRAMO_C: letra_x en {LETRAS_X} y p_x > 0 (hay {X!r}, {px})")
        if self.cerrojo and X is None: raise SystemExit("MUNDO_TRAMO_C: cerrojo exige letra_x (la llave)")
        self.t = 0
        self.cobros = [0] * n
        # P8: exposiciones a la letra nueva por linaje: [n, mordidas] dentro / fuera, y FRIAS (dentro, el linaje ya mordio X en algun
        # sitio y A/C dentro, y NUNCA X dentro): el primer encuentro de cada vida cuenta una vez; B dentro (control de 'regla de lugar')
        self.mx = [0] * n; self.mx_dentro = [0] * n
        self.ex_in = [[0, 0] for _ in range(n)]; self.ex_out = [[0, 0] for _ in range(n)]; self.ex_frio = [[0, 0] for _ in range(n)]
        self.ex_out_conoce = [[0, 0] for _ in range(n)]; self.ex_b_in = [[0, 0] for _ in range(n)]
        self.vida_in = [False] * n; self.vida_out = [False] * n; self.vida_b = [False] * n
        # P9: llave por cuerpo
        self.t_llave = [-10 ** 9] * n; self.con_llave = [0] * n; self.sin_llave = [0] * n; self.llaves = [0] * n
        # P10: mudanzas
        self.zr = np.random.default_rng([int(seed), 0, ME.ETQ_ZONA, 0]); _z = int(self.zr.integers(L))
        if _z != self.z0: raise SystemExit("MUNDO_TRAMO_C: la corriente de la zona no reproduce z0")
        self.mudanzas = [(0, self.z0)]; self.t_primero = [[None] for _ in range(n)]
        self.z0_0 = self.z0; self.celdas_0 = self.celdas
        # P7 (mecanismo "llega antes"): por VIDA, pasos desde el nacimiento (l.tmu de la pista) hasta el primer bocado A+C dentro
        self.vida_dentro = [False] * n; self.lat_vida = [[] for _ in range(n)]
        self.activo = bool(self.c_e or self.X or self.cerrojo or self.mueve)
        if self.X:   # la letra nueva entra en la contabilidad del oasis (composicion y mordidas dentro/fuera)
            self.comp_dentro[self.X] = 0; self.comp_fuera[self.X] = 0
            for i in range(n): self.m_dentro[i][self.X] = 0; self.m_fuera[i][self.X] = 0

    # ---------------------------------------------------------------- alta
    def extiende(self, lin, VAL_VIVO, EFECTO):
        cat = CAT_X[self.X]
        for l in lin:
            l.mord[self.X] = [0] * 4; l.vis[self.X] = [0] * 4; l.enc[self.X] = 0; l.bsac[self.X] = 0; l.dsac[self.X] = 0
            for _n in range(2): l.exp[_n][self.X] = None; l.bxor[_n].append(0); l.exor[_n].append(0)
            l.sobre[cat] = [0] * 4; l.llegadas[cat] = [0] * 4
        return dict(VAL_VIVO, **{self.X: cat}), dict(EFECTO, **{cat: self.ex})

    def letra(self, rng):
        if rng.random() < self.px: return self.X
        return P.TIPOS[int(rng.integers(len(P.TIPOS)))]

    # ---------------------------------------------------------------- por paso
    def paso(self, lin, objs):
        if self.mueve and self.t > 0 and self.t % self.mueve == 0: self.muda()
        super().paso(lin, objs)
        self.t += 1

    def muda(self):
        L = self.L; viejo = self.celdas
        while True:
            z = int(self.zr.integers(L)); c = frozenset((z + j) % L for j in range(self.W))
            if not (c & viejo): break
        self.z0 = z; self.celdas = c; self.mudanzas.append((self.t, z))
        for i in range(self.n): self.t_primero[i].append(None)

    def muerde(self, l, kk, pos, dS):
        dentro = pos in self.celdas
        if kk == self.X:
            (self.m_dentro if dentro else self.m_fuera)[l.i][kk] += 1
            self.mx[l.i] += 1
            if dentro: self.mx_dentro[l.i] += 1
            if self.cerrojo: self.t_llave[l.i] = self.t; self.llaves[l.i] += 1
            if dentro:
                if dS[0] > 0 and not dS[1] > 0: return (dS[0], dS[1] + self.extra)
                if dS[1] > 0 and not dS[0] > 0: return (dS[0] + self.extra, dS[1])
            return dS
        if self.cerrojo and dentro and kk in ('A', 'C'):
            if self.t - self.t_llave[l.i] <= self.d_llave: self.con_llave[l.i] += 1
            else:
                self.sin_llave[l.i] += 1
                self.m_dentro[l.i][kk] += 1
                return (dS[0] * self.pobre, dS[1] * self.pobre) if self.cerrojo_pobre else dS
        r = super().muerde(l, kk, pos, dS)
        if dentro and kk in ('A', 'C'):
            if self.mueve and self.t_primero[l.i][-1] is None: self.t_primero[l.i][-1] = self.t - self.mudanzas[-1][0]
            if not self.vida_dentro[l.i]: self.vida_dentro[l.i] = True; self.lat_vida[l.i].append(self.t - l.tmu)
        return r

    def cobra(self, l):
        l.E -= self.c_e; self.cobros[l.i] += 1

    def expone(self, l, res, pos):
        """P8: llegada (prev_on != pos) a una celda con letra: el primer encuentro de la VIDA con X dentro / X fuera / B dentro."""
        k = res['letra']
        if k is None or l.prev_on == pos: return
        i = l.i; dentro = pos in self.celdas; m = int(res['mordio'])
        if k == self.X:
            if dentro and not self.vida_in[i]:
                self.vida_in[i] = True; self.ex_in[i][0] += 1; self.ex_in[i][1] += m
                ac_in = sum(self.m_dentro[i][z] for z in ('A', 'C'))
                # frio: X ya mordida en algun sitio (ANTES de esta), A/C ya mordidas dentro, X NUNCA mordida dentro antes de esta
                if (self.mx[i] - (m if dentro else 0)) > 0 and ac_in > 0 and (self.mx_dentro[i] - m) == 0:
                    self.ex_frio[i][0] += 1; self.ex_frio[i][1] += m
            elif not dentro and not self.vida_out[i]:
                self.vida_out[i] = True; self.ex_out[i][0] += 1; self.ex_out[i][1] += m
                if (self.mx[i] - m) > 0: self.ex_out_conoce[i][0] += 1; self.ex_out_conoce[i][1] += m
        elif k == 'B' and dentro and not self.vida_b[i]:
            self.vida_b[i] = True; self.ex_b_in[i][0] += 1; self.ex_b_in[i][1] += m

    def muere(self, l):
        i = l.i; self.t_llave[i] = -10 ** 9; self.vida_in[i] = self.vida_out[i] = self.vida_b[i] = False; self.vida_dentro[i] = False

    # ---------------------------------------------------------------- salida
    def salida(self, i):
        d = super().salida(i)
        if self.activo: d['latencia_vida'] = list(self.lat_vida[i][:400])
        if self.c_e: d['cobros'] = self.cobros[i]
        if self.X:
            d['x'] = dict(letra=self.X, mord=self.mx[i], mord_dentro=self.mx_dentro[i], exp_dentro=list(self.ex_in[i]), exp_fuera=list(self.ex_out[i]),
                          exp_frio=list(self.ex_frio[i]), exp_fuera_conoce=list(self.ex_out_conoce[i]), exp_b_dentro=list(self.ex_b_in[i]))
        if self.cerrojo: d['llave'] = dict(con=self.con_llave[i], sin=self.sin_llave[i], llaves=self.llaves[i])
        if self.mueve: d['latencias'] = list(self.t_primero[i])
        return d

    def info(self):
        d = super().info()
        if self.activo:   # solo con alguna perilla encendida (apagadas: la salida es la de mundo_escalera, bit a bit)
            d.update(c_e=self.c_e, letra_x=self.X, efecto_x=list(self.ex) if self.X else None, p_x=self.px, cerrojo=self.cerrojo,
                     d_llave=(self.d_llave if self.cerrojo else None), cerrojo_pobre=(self.cerrojo_pobre if self.cerrojo else None), mueve=self.mueve, mudanzas=list(self.mudanzas),
                     bins30_final=self.bins(30))
            if self.mueve:   # z0 / oasis / bins30 = el INICIAL (lo que P1 reporta); el final va en bins30_final
                d.update(z0=self.z0_0, oasis=[self.z0_0, (self.z0_0 + self.W - 1) % self.L], bins30=sorted({(x * 30) // self.L for x in self.celdas_0}))
        return d


def construye():
    """-> (run, info). Aborta si un sha o un ancla no calzan. Las 9 anclas de mundo_escalera se aplican primero (sin tocarlas)."""
    if _RUN[0] is not None: return _RUN[0]
    rp = os.path.join(PISTA_D, 'pista.py'); rj = os.path.join(PISTA_D, 'juez.py'); rm = os.path.join(AQUI, 'mundo_escalera.py')
    sp, sj, sm = h16(rp), h16(rj), h16(rm)
    if sp != ME.SHA_PISTA: raise SystemExit(f"MUNDO_TRAMO_C: pista.py sha {sp} != fijado {ME.SHA_PISTA}")
    if sj != ME.SHA_JUEZ: raise SystemExit(f"MUNDO_TRAMO_C: juez.py sha {sj} != fijado {ME.SHA_JUEZ}")
    if sm != SHAS_FIJOS['mundo_escalera']: raise SystemExit(f"MUNDO_TRAMO_C: mundo_escalera.py sha {sm} != fijado {SHAS_FIJOS['mundo_escalera']} (P1 cambio: re-fijar y re-correr identidad_c)")
    if os.path.abspath(P.__file__) != os.path.abspath(rp): raise SystemExit(f"MUNDO_TRAMO_C: 'pista' importado de {P.__file__}")
    txt = open(rp, encoding='utf-8').read()
    a = txt.index("def run(seed, carros,"); b = txt.index("\n\n\n# claves de primer nivel")
    src = txt[a:b] + "\n"
    for viejo, nuevo in ME.ANCLAS + ANCLAS_C:
        k = src.count(viejo)
        if k != 1: raise SystemExit(f"MUNDO_TRAMO_C: el ancla aparece {k} veces (debe ser 1): {viejo[:70]!r}")
        src = src.replace(viejo, nuevo)
    ns = dict(vars(P)); ns.update(Oasis=ME.Oasis, OasisC=OasisC, EXTRA=ME.EXTRA, POBRE=ME.POBRE, D_LLAVE=D_LLAVE, IDX=dict(P.IDX, **{x: IDX_X for x in LETRAS_X}))
    exec(compile(src, '<mundo_tramo_c.run desde pista.py + mundo_escalera>', 'exec'), ns)
    _RUN[0] = (ns['run'], dict(sha_pista=sp, sha_juez=sj, sha_mundo_escalera=sm, sha_fuente_transformada=h16s(src), anclas=len(ME.ANCLAS) + len(ANCLAS_C)))
    return _RUN[0]


def run(*a, **k):
    return construye()[0](*a, **k)


if __name__ == '__main__':
    print(construye()[1])
