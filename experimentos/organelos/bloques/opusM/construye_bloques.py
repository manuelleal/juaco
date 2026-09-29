"""construye_bloques.py — construye motor_bloques.py POR ANCLAS desde experimentos/organelos/frio/motor_frio_rapido.py
(sha ff9d890a5cce9dec; el gemelo numba de ECO_SEL_ING). NO toca el origen. EXPLORATORIO (Opus M, 28-sep-2026, canal BLOQUES).

Mision: llegar a la AGI por este camino (organismo minimo, reglas locales, sin retropropagacion, peldanos preregistrados con
controles y replicas). Principio del director: que la evolucion construya el organo, no nosotros, y solo con seleccion natural.

BLOQUES: un genoma de REGLAS de largo variable (0..NRMAX), cada regla armada con bloques
  (sentido, parametro, comparador, umbral, accion, peso):
  sentidos: 0 hambre, 1 sed, 2 cercania de lo que mira, 3 pixel j del objeto EN FOCO (lo que mira al moverse / lo que tiene
            en la boca al morder), 4 pixel j de la ULTIMA letra mordida (memoria), 5 R de la ultima mordida ((R+3)/4)
  comparador: 1 -> sentido > umbral ; 0 -> sentido < umbral
  acciones: 0 boca (Vb += w: morder / no morder), 1 patas hacia lo que mira (w > 0) o alejarse (w < 0), 2 quedarse (las dos
            neuronas de marcha -= w), 3 parir (umbral de parto efectivo ru - 0.1 * suma(w), recortado a [0.5, 1.5])
Las reglas se SUMAN al cerebro de fabrica como sesgos. Genoma vacio (RN = 0) -> no se evalua nada.
Con BQ apagado (BQ[0] = 0) no hay NINGUNA llamada nueva: motor_frio_rapido bit a bit (arnes). Con BQ prendido la genetica
de las reglas usa rng PROPIOS ([seed, linaje, 7701, k] al nacer; [seed, linaje, 7702, nac] al refundar): con tasas 0 y
genoma vacio, tambien bit a bit (arnes). Memoria nueva por cuerpo: 2 numeros (ultima letra mordida y su R), solo la leen las
reglas; mas el sesgo de parto calculado en el paso.

Uso:  python construye_bloques.py            # escribe motor_bloques.py
      python construye_bloques.py --verifica # reconstruye en memoria y compara con el archivo (IGUAL / DISTINTO)
"""
import hashlib, os, sys

AQUI = os.path.dirname(os.path.abspath(__file__))
ORG = os.path.dirname(os.path.dirname(AQUI))
ORIGEN = os.path.join(ORG, 'frio', 'motor_frio_rapido.py')
SHA_ORIGEN = 'ff9d890a5cce9dec'
DESTINO = os.path.join(AQUI, 'motor_bloques.py')


def h16(p):
    return hashlib.sha256(open(p, 'rb').read()).hexdigest()[:16]


ANCLAS = []   # (nombre, viejo, nuevo): cada viejo debe aparecer EXACTAMENTE una vez

ANCLAS.append(('B0 docstring', '"""motor_frio_rapido.py (CONSTRUIDO por',
'''"""motor_bloques.py (CONSTRUIDO por experimentos/organelos/bloques/opusM/construye_bloques.py desde
experimentos/organelos/frio/motor_frio_rapido.py, sha ff9d890a5cce9dec; NO editar a mano). BLOQUES (Opus M, 28-sep-2026,
EXPLORATORIO): genoma de reglas componibles sumadas como sesgos al cerebro de fabrica; ver construye_bloques.py. Lo que
sigue es el docstring del origen.

motor_frio_rapido.py (CONSTRUIDO por'''))

ANCLAS.append(('B1 ruta FRIO', "FRIO = os.path.dirname(os.path.abspath(__file__))   # F1 FRIO: este archivo vive en experimentos/organelos/frio",
"FRIO = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'frio')   # BLOQUES: vive en bloques/opusM"))

ANCLAS.append(('B2 firma', "FIRMA_GEMELO = 'motor_frio_rapido v1'", "FIRMA_GEMELO = 'motor_bloques v0'"))

ANCLAS.append(('B3 constantes', "NBF = 22\n",
"""NBF = 22
# BLOQUES: el genoma de reglas (RG[s, r] = sentido, parametro, comparador, umbral, accion, peso; RN[s] = largo) y la memoria
# que solo leen las reglas (RM[s] = ultima letra mordida (-1 ninguna), su R, sesgo de parto del paso)
NRMAX = 12; NRC = 6; NRM = 3
BQ_CFG = dict(on=0, donante='padre', p_campo=0.10, p_dup=0.02, p_ins=0.02, p_hgt=0.01, p_del=0.05, banco=200,
              inicial=None, forzada=None)
BQ_OUT = {}
"""))

ANCLAS.append(('B4 BODY_KEYS', "'tbR', 'tbH', 'mdR', 'mdH', 'dado')\n", "'tbR', 'tbH', 'mdR', 'mdH', 'dado', 'RG', 'RN', 'RM')\n"))

ANCLAS.append(('B5 cuerpos vacios', "mdH=np.zeros((S, NNEC, 4), np.bool_), dado=np.zeros((S, DADO), np.int64))",
"mdH=np.zeros((S, NNEC, 4), np.bool_), dado=np.zeros((S, DADO), np.int64),\n"
"                RG=np.zeros((S, NRMAX, NRC)), RN=np.zeros(S, np.int64), RM=np.zeros((S, NRM)))"))

ANCLAS.append(('B6 firma del tramo', "           LFAM, tbR, tbH, mdR, mdH, dado, tn, tk, tR, sce, rst, tni, tnf):",
"           LFAM, tbR, tbH, mdR, mdH, dado, tn, tk, tR, sce, rst, tni, tnf, RG, RN, RM, BQ):"))

ANCLAS.append(('B7 llamada del tramo', "                  st['tni'], st['tnf'])",
"                  st['tni'], st['tnf'], st['RG'], st['RN'], st['RM'], st['BQ'])"))

ANCLAS.append(('B8 patas', "            e0, e1 = _exp2(-(V[0] - .8) / noise, -(V[1] - .8) / noise, lp, xin, xout, dims, adr, mexp)",
"""            if BQ[0] != 0 and RN[s] > 0:   # BLOQUES: sesgos de patas y de parto (foco = lo que mira)
                _reglas_mov(s, RG, RN, RM, V, E, Ag, d, k, left, PATM)
            e0, e1 = _exp2(-(V[0] - .8) / noise, -(V[1] - .8) / noise, lp, xin, xout, dims, adr, mexp)"""))

ANCLAS.append(('B9 boca', "                Vb = bf[s, F_ALPHA] * wt + bf[s, F_HB] * hambre + .5\n",
"""                Vb = bf[s, F_ALPHA] * wt + bf[s, F_HB] * hambre + .5
                if BQ[0] != 0 and RN[s] > 0:   # BLOQUES: sesgo de boca (foco = lo que tiene en la celda)
                    Vb += _reglas_boca(s, RG, RN, RM, E, Ag, d, kk, PATM)
"""))

ANCLAS.append(('B10 memoria de la mordida', "                    R = RV[kk, na]; bf[s, F_R] = R\n",
"""                    R = RV[kk, na]; bf[s, F_R] = R
                    RM[s, 0] = kk; RM[s, 1] = R   # BLOQUES: la memoria que solo leen las reglas
"""))

ANCLAS.append(('B11 refundacion', "                    _consts_fab(s2, bi, bf, C0i, C0f)\n",
"""                    _consts_fab(s2, bi, bf, C0i, C0f)
                RM[s2, 0] = -1.0; RM[s2, 1] = 0.0; RM[s2, 2] = 0.0; RN[s2] = 0   # BLOQUES
                if BQ[0] != 0:
                    _reglas_fund(lin, li[lin, L_NAC], s2, RG, RN)
"""))

ANCLAS.append(('B12 parto (umbral)', "            ru = bf[s, F_RU]\n",
"""            ru = bf[s, F_RU]
            if BQ[0] != 0 and RM[s, 2] != 0.0:   # BLOQUES: accion parir
                ru = _clip(ru - 0.1 * RM[s, 2], 0.5, 1.5)
"""))

ANCLAS.append(('B13 parto (herencia de reglas)', "                    if LFAM[lin] == 2:   # F1 FRIO: BAR0",
"""                    RM[s3, 0] = -1.0; RM[s3, 1] = 0.0; RM[s3, 2] = 0.0; RN[s3] = 0   # BLOQUES
                    if BQ[0] != 0:
                        _reglas_hijo(lin, k, s, s3, RG, RN, bi, cuer, nb, L)
                    if LFAM[lin] == 2:   # F1 FRIO: BAR0"""))

ANCLAS.append(('B14 BQ en el estado', "    st['BEXP'] = _bufs_exp()\n    _CTX.clear(); _CTX.update(seed=seed, E_=E_, ES=ES)\n",
"""    st['BEXP'] = _bufs_exp()
    _CTX.clear(); _CTX.update(seed=seed, E_=E_, ES=ES)
    _bq_arranque(st, n)   # BLOQUES
"""))

ANCLAS.append(('B15 muestra', "            if E_['cada_gen'] and t % E_['cada_gen'] == 0: _muestra_gen(E_, ES, cuerpos, t)\n",
"""            if E_['cada_gen'] and t % E_['cada_gen'] == 0: _muestra_gen(E_, ES, cuerpos, t)
            if BQ_CFG['on'] and E_['cada_gen'] and t % E_['cada_gen'] == 0: _bq_muestra(st, t)   # BLOQUES
"""))

ANCLAS.append(('B16 final', "    if _estado_final is not None:\n        _estado_final.update(",
"""    if BQ_CFG['on']: _bq_final(st, vivos)   # BLOQUES
    if _estado_final is not None:
        _estado_final.update("""))

# ------------------------------------------------------------------ el bloque nuevo (antes de _tramo)
NUEVO = '''
# ================================================================ BLOQUES (anadido por construye_bloques.py)
@njit(cache=True)
def _sentido(sid, par, E, Ag, d, foco, lk, lr, PATM):
    if sid == 0: return _clip(1 - E, 0.0, 1.0)
    if sid == 1: return _clip(1 - Ag, 0.0, 1.0)
    if sid == 2:
        if d < 0: return 0.0
        return 1.0 - (d if d < 10 else 10) / 10.0
    if sid == 3:
        if foco < 0: return 0.0
        return PATM[foco, par]
    if sid == 4:
        if lk < 0: return 0.0
        return PATM[lk, par]
    return (lr + 3.0) / 4.0


@njit(cache=True)
def _cumple(s, r, RG, RM, E, Ag, d, foco, PATM):
    x = _sentido(int(RG[s, r, 0]), int(RG[s, r, 1]), E, Ag, d, foco, int(RM[s, 0]), RM[s, 1], PATM)
    if RG[s, r, 2] > 0.5: return x > RG[s, r, 3]
    return x < RG[s, r, 3]


@njit(cache=True)
def _reglas_mov(s, RG, RN, RM, V, E, Ag, d, k, left, PATM):
    pb = 0.0
    for r in range(RN[s]):
        a = int(RG[s, r, 4])
        if a == 0: continue
        if not _cumple(s, r, RG, RM, E, Ag, d, k, PATM): continue
        w = RG[s, r, 5]
        if a == 1:
            if k >= 0 and d > 0:
                if left: V[0] += w
                else: V[1] += w
        elif a == 2:
            V[0] -= w; V[1] -= w
        else:
            pb += w
    RM[s, 2] = pb


@njit(cache=True)
def _reglas_boca(s, RG, RN, RM, E, Ag, d, kk, PATM):
    b = 0.0
    for r in range(RN[s]):
        if int(RG[s, r, 4]) != 0: continue
        if _cumple(s, r, RG, RM, E, Ag, d, kk, PATM): b += RG[s, r, 5]
    return b


@njit(cache=True)
def _reglas_hijo(lin, k, s, s3, RG, RN, bi, cuer, nb, L):
    """Herencia de reglas en el parto: el vecino VIVO mas cercano en el anillo (sin azar; empate: el primero del turno) da la
    regla de la HGT; la genetica de reglas corre en Python con rng propio."""
    p = bi[s, I_POS]; v = -1; dv = L + 1
    for jj in range(nb):
        u = cuer[jj]
        if u < 0 or u == s or u == s3: continue
        a = bi[u, I_POS] - p
        if a < 0: a = -a
        if L - a < a: a = L - a
        if a < dv:
            dv = a; v = u
    rp = RG[s, :RN[s]].copy()
    if v >= 0: rv = RG[v, :RN[v]].copy()
    else: rv = np.zeros((0, NRC))
    with objmode(ch='float64[:, :]'):
        ch = _py_reglas_hijo(lin, k, rp, rv)
    m = ch.shape[0]
    for r in range(m):
        for c in range(NRC): RG[s3, r, c] = ch[r, c]
    RN[s3] = m


@njit(cache=True)
def _reglas_fund(lin, nac, s2, RG, RN):
    with objmode(ch='float64[:, :]'):
        ch = _py_reglas_fund(lin, nac)
    m = ch.shape[0]
    for r in range(m):
        for c in range(NRC): RG[s2, r, c] = ch[r, c]
    RN[s2] = m


def _regla_azar(rr):
    return [float(rr.integers(0, 6)), float(rr.integers(0, 6)), float(rr.integers(0, 2)), float(rr.random()),
            float(rr.integers(0, 4)), float(rr.uniform(-3.0, 3.0))]


def _muta_reglas(base, vec, rr, C, O):
    """Operadores locales: mutar un bloque o el peso (por regla), DUPLICAR (Ohno), BORRAR, INSERTAR una regla nueva, HGT
    (copiar una regla entera del vecino). Tope NRMAX (lo que sobra se corta al final)."""
    R = [list(map(float, x)) for x in base]
    for x in R:
        if rr.random() < C['p_campo']:
            f = int(rr.integers(0, 6)); O['n_campo'] += 1
            if f == 0: x[0] = float(rr.integers(0, 6))
            elif f == 1: x[1] = float(rr.integers(0, 6))
            elif f == 2: x[2] = 1.0 - x[2]
            elif f == 3: x[3] = float(min(1.0, max(0.0, x[3] + rr.normal(0, 0.15))))
            elif f == 4: x[4] = float(rr.integers(0, 4))
            else: x[5] = float(min(3.0, max(-3.0, x[5] + rr.normal(0, 0.5))))
    if R and rr.random() < C['p_dup']:
        i = int(rr.integers(0, len(R))); R.insert(i + 1, list(R[i])); O['n_dup'] += 1
    if R and rr.random() < C['p_del']:
        del R[int(rr.integers(0, len(R)))]; O['n_del'] += 1
    if rr.random() < C['p_ins']:
        R.append(_regla_azar(rr)); O['n_ins'] += 1
    if len(vec) and rr.random() < C['p_hgt']:
        R.append(list(map(float, vec[int(rr.integers(0, len(vec)))]))); O['n_hgt'] += 1
    if len(R) > NRMAX:
        R = R[:NRMAX]; O['n_tope'] += 1
    return np.ascontiguousarray(np.array(R, np.float64).reshape(len(R), NRC))


def _py_reglas_hijo(lin, k, rp, rv):
    C = _CTX['BQC']; O = BQ_OUT; BR = _CTX['BR']
    rr = np.random.default_rng([_CTX['seed'], int(lin), 7701, int(k)])
    base = rp
    if C['donante'] == 'azar':
        base = BR[int(rr.integers(len(BR)))] if BR else np.zeros((0, NRC))
    ch = _muta_reglas(base, rv, rr, C, O)
    O['n_hijos'] += 1
    if ch.shape == rp.shape and np.array_equal(ch, rp): O['n_igual_padre'] += 1
    if len(rp):
        O['n_hijos_pl'] += 1
        if ch.shape == rp.shape and np.array_equal(ch, rp): O['n_igual_pl'] += 1
    if C['banco']:
        BR.append(rp.copy() if C['donante'] == 'padre' else ch.copy())
        if len(BR) > C['banco']: BR.pop(0)
    return ch


def _py_reglas_fund(lin, nac):
    C = _CTX['BQC']; O = BQ_OUT; BR = _CTX['BR']
    rr = np.random.default_rng([_CTX['seed'], int(lin), 7702, int(nac)])
    base = BR[int(rr.integers(len(BR)))] if BR else np.zeros((0, NRC))
    ch = _muta_reglas(base, np.zeros((0, NRC)), rr, C, O)
    O['n_fund'] += 1
    if C['donante'] == 'azar' and C['banco']:
        BR.append(ch.copy())
        if len(BR) > C['banco']: BR.pop(0)
    return ch


def _bq_arranque(st, n):
    """BQ en el estado; memoria de las reglas en -1; telemetria; genoma inicial de los fundadores (vacio por defecto)."""
    C = dict(BQ_CFG); st['BQ'] = np.array([int(C['on'])], np.int64)
    _CTX.update(BQC=C, BR=[])
    BQ_OUT.clear(); BQ_OUT.update(cfg={k: v for k, v in C.items()}, serie=[], n_hijos=0, n_fund=0, n_igual_padre=0, n_campo=0,
                                  n_dup=0, n_del=0, n_ins=0, n_hgt=0, n_tope=0, n_hijos_pl=0, n_igual_pl=0)
    if '_bq_ok' not in st: st['RM'][:, 0] = -1.0   # arranque fresco (en un checkpoint ya viene)
    st['_bq_ok'] = 1
    if C['on'] and (C['inicial'] or C['forzada'] is not None):
        for i in range(n):
            if C['forzada'] is not None: R = np.array(C['forzada'], np.float64).reshape(-1, NRC)
            else:
                rr = np.random.default_rng([_CTX['seed'], i, 7703, 0])
                R = np.array([_regla_azar(rr) for _ in range(int(C['inicial']))], np.float64).reshape(-1, NRC)
            st['RG'][i, :len(R)] = R; st['RN'][i] = len(R)
    if C['on'] and C['banco']:   # como E9 del original: el banco arranca con (las listas de) los fundadores
        _CTX['BR'][:] = [st['RG'][i, :st['RN'][i]].copy() for i in range(n)][-int(C['banco']):]


def _bq_muestra(st, t):
    v = _vivos(st)
    rn = st['RN'][v] if v else np.zeros(0, np.int64)
    BQ_OUT['serie'].append([int(t), len(v), (round(float(rn.mean()), 4) if len(v) else None), (int(rn.max()) if len(v) else 0),
                            (round(float((rn > 0).mean()), 4) if len(v) else None), len(_CTX['BR'])])


def _bq_final(st, vivos):
    bi = st['bi']
    BQ_OUT['vivos_T'] = [[int(bi[s, I_LIN]), int(bi[s, I_GEN]), int(bi[s, I_FUND]),
                          [[round(float(z), 4) for z in st['RG'][s, r]] for r in range(int(st['RN'][s]))]] for s in vivos]
    BQ_OUT['banco_T'] = [[[round(float(z), 4) for z in x] for x in R] for R in _CTX['BR']]


# ================================================================ EL TRAMO: pasos [t0, t1)'''

ANCLAS.append(('B17 bloque nuevo', "\n# ================================================================ EL TRAMO: pasos [t0, t1)", NUEVO))


def construye():
    if h16(ORIGEN) != SHA_ORIGEN:
        raise SystemExit(f'origen cambio: {h16(ORIGEN)} != {SHA_ORIGEN}')
    txt = open(ORIGEN, encoding='utf-8').read()
    for nom, viejo, nuevo in ANCLAS:
        c = txt.count(viejo)
        if c != 1: raise SystemExit(f'ancla {nom}: aparece {c} veces (debe ser 1)')
        txt = txt.replace(viejo, nuevo)
    return txt


if __name__ == '__main__':
    t = construye()
    if '--verifica' in sys.argv:
        print('IGUAL' if open(DESTINO, encoding='utf-8').read() == t else 'DISTINTO', h16(DESTINO))
    else:
        with open(DESTINO, 'w', encoding='utf-8', newline='\n') as f: f.write(t)
        print('escrito', DESTINO, h16(DESTINO), f'({len(ANCLAS)} anclas, origen {SHA_ORIGEN})')
