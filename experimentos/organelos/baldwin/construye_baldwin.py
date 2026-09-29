"""construye_baldwin.py — construye motor_baldwin.py POR ANCLAS desde experimentos/organelos/bloques/opusM/motor_bloques3.py
(sha 21b5ee28d086b3be; el de UN MUNDO QUE CAMBIA, que con inv = 0 es motor_bloques2 y con kit 1 es motor_bloques, el de la serie
BLOQUES = FUNCIONA x2; cadena de arneses identidad_bloques2 18/18 e identidad_bloques3 10/10). NO toca el origen.

Mision: llegar a la AGI por este camino (organismo minimo con reglas locales, sin retropropagacion, peldanos preregistrados con
controles y replicas). BALDWIN EN BLOQUES (29-sep-2026): la seleccion construye la PLASTICIDAD.

Lo nuevo (BQ_CFG plast; plast = 0 no ejecuta NADA nuevo: motor_bloques3 bit a bit, arnes):
  Cada regla lleva un gen heredable 'plastica' (bit) y su peso GENETICO w0 (RPL[s, r] = [bit, w0]; memoria nueva: 1 bit + 1 float por
  regla). Si la regla es de BOCA y plastica, su peso EN VIDA (RG[s, r, 5], el que suma a Vb) aprende de la consecuencia de SU mordida:
  cuando el cuerpo muerde y la condicion de la regla se cumplia al decidir, w <- clip(w + ETAS*(R - w), -3, 3) si R > w, y
  w <- clip(w + ETAS*AV*(R - w), -3, 3) si no. Es la regla de la via lenta del cerebro (lectura directa de la retina: tasa eta_s y
  asimetria 'aversion' del propio cuerpo, R = RV[letra, necesidad] la misma senal con que aprenden Wp/Wn y Wps/Wns): CERO parametros nuevos.
  El hijo hereda el bit y w0 del padre (NO el w aprendido); la HGT copia bit y w0 del vecino; el banco guarda [.., w0, bit].
  Genetica del bit (rng PROPIO [seed, linaje, 7711, k] al nacer y [seed, linaje, 7712, nac] al refundar: no toca el azar de las reglas):
  regla insertada plastica con prob p_ins_pl; cada regla invierte su bit con prob p_bit en cada nacimiento.
  plast = 1 PLAST_V (bit heredable) · 2 PLAST_AZA (bit sorteado 0/1 al nacer para cada regla: sin herencia) ·
          3 PLAST_RW0 (bit heredable, pero el blanco del aprendizaje es RV[letra seudoazar, necesidad]: w deriva sin la consecuencia).
  Solo kit 1 (el de BLOQUES).

Uso:  python construye_baldwin.py [--verifica]
"""
import hashlib, os, sys

AQUI = os.path.dirname(os.path.abspath(__file__))
ORG = os.path.dirname(AQUI)
ORIGEN = os.path.join(ORG, 'bloques', 'opusM', 'motor_bloques3.py')
SHA_ORIGEN = '21b5ee28d086b3be'
DESTINO = os.path.join(AQUI, 'motor_baldwin.py')


def h16(p):
    return hashlib.sha256(open(p, 'rb').read()).hexdigest()[:16]


A = []
A.append(('W0 docstring', '"""motor_bloques3.py (CONSTRUIDO por',
'''"""motor_baldwin.py (CONSTRUIDO por experimentos/organelos/baldwin/construye_baldwin.py desde
experimentos/organelos/bloques/opusM/motor_bloques3.py, sha 21b5ee28d086b3be; NO editar a mano). BALDWIN EN BLOQUES: gen 'plastica'
(bit) + peso genetico w0 por regla; las reglas plasticas de boca aprenden en vida de la consecuencia de su mordida; el hijo hereda w0.
Con plast = 0 es motor_bloques3 bit a bit. Lo que sigue es el docstring del origen.

motor_bloques3.py (CONSTRUIDO por'''))
A.append(('W1 ruta FRIO', "FRIO = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'frio')   # BLOQUES: vive en bloques/opusM",
          "FRIO = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'frio')   # BALDWIN: vive en organelos/baldwin"))
A.append(('W2 firma', "FIRMA_GEMELO = 'motor_bloques3 v0'", "FIRMA_GEMELO = 'motor_baldwin v0'"))
A.append(('W3 cfg', "tope=12, inv=0, inv_cada=20000)",
          "tope=12, inv=0, inv_cada=20000,\n              plast=0, p_bit=0.01, p_ins_pl=0.5, forzada_bit=None)   # BALDWIN"))
A.append(('W4 BODY_KEYS', "'dado', 'RG', 'RN', 'RM')\n", "'dado', 'RG', 'RN', 'RM', 'RPL')\n"))
A.append(('W5 cuerpos vacios', "RN=np.zeros(S, np.int64), RM=np.zeros((S, NRM)))",
          "RN=np.zeros(S, np.int64), RM=np.zeros((S, NRM)),\n                RPL=np.zeros((S, NRMAX, 2)))   # BALDWIN: [bit plastica, w0 genetico] por regla"))
A.append(('W6 firma del tramo', "tni, tnf, RG, RN, RM, BQ):", "tni, tnf, RG, RN, RM, BQ, RPL, PLC):"))
A.append(('W7 llamada del tramo', "st['RG'], st['RN'], st['RM'], st['BQ'])", "st['RG'], st['RN'], st['RM'], st['BQ'], st['RPL'], st['PLC'])"))
A.append(('W8 aprende en la mordida', "                    RM[s, 0] = kk; RM[s, 1] = R; RM[s, 3 + kk] = R",
"""                    if BQ[2] != 0 and RN[s] > 0:   # BALDWIN: las reglas plasticas de boca aprenden de la consecuencia de SU mordida
                        Rt = R
                        if BQ[2] == 3: Rt = RV[_kk_deriva(t, s), na]   # PLAST_RW0: blanco sin relacion con la consecuencia
                        _reglas_aprende(s, RG, RN, RM, RPL, E, Ag, d, kk, PATM, Rt, bf[s, F_ETAS], bf[s, F_AV], PLC)
                    RM[s, 0] = kk; RM[s, 1] = R; RM[s, 3 + kk] = R"""))
A.append(('W9 refundacion', "                    _reglas_fund(lin, li[lin, L_NAC], s2, RG, RN)\n",
"""                    if BQ[2] != 0: _reglas_fund_pl(lin, li[lin, L_NAC], s2, RG, RN, RPL)   # BALDWIN
                    else: _reglas_fund(lin, li[lin, L_NAC], s2, RG, RN)
"""))
A.append(('W10 parto', "                        _reglas_hijo(lin, k, s, s3, RG, RN, bi, cuer, nb, L)\n",
"""                        if BQ[2] != 0: _reglas_hijo_pl(lin, k, s, s3, RG, RN, RPL, bi, cuer, nb, L)   # BALDWIN
                        else: _reglas_hijo(lin, k, s, s3, RG, RN, bi, cuer, nb, L)
"""))
A.append(('W11 BQ y contadores', "C = dict(BQ_CFG); st['BQ'] = np.array([int(C['on']), int(C.get('kit', 1))], np.int64)\n",
"""C = dict(BQ_CFG); st['BQ'] = np.array([int(C['on']), int(C.get('kit', 1)), int(C.get('plast', 0))], np.int64)
    if 'PLC' not in st: st['PLC'] = np.zeros(4, np.int64)   # BALDWIN: contadores (viajan en el checkpoint como clave del estado)
    if int(C.get('plast', 0)) and (not C['on'] or int(C.get('kit', 1)) != 1): raise ValueError('BALDWIN: plast exige on = 1 y kit 1')
"""))
A.append(('W12 arranque plastico', "        _CTX['BR'][:] = [st['RG'][i, :st['RN'][i]].copy() for i in range(n)][-int(C['banco']):]\n",
"""        _CTX['BR'][:] = [st['RG'][i, :st['RN'][i]].copy() for i in range(n)][-int(C['banco']):]
    if int(C.get('plast', 0)): _bq_arranque_pl(st, n, C)   # BALDWIN
"""))
A.append(('W13 muestra', "                            (round(float((rn > 0).mean()), 4) if len(v) else None), len(_CTX['BR'])])\n",
"""                            (round(float((rn > 0).mean()), 4) if len(v) else None), len(_CTX['BR'])])
    if int(_CTX['BQC'].get('plast', 0)): _bq_muestra_pl(st, t, v)   # BALDWIN
"""))
A.append(('W14 final', "    BQ_OUT['banco_T'] = [[[round(float(z), 4) for z in x] for x in R] for R in _CTX['BR']]\n",
"""    BQ_OUT['banco_T'] = [[[round(float(z), 4) for z in x] for x in R] for R in _CTX['BR']]
    if int(_CTX['BQC'].get('plast', 0)): _bq_final_pl(st, vivos)   # BALDWIN
"""))

NUEVO = '''

# ================================================================ BALDWIN (anadido por construye_baldwin.py)
NRCP = NRC + 1   # en Python, una regla plastica es [sentido, parametro, comparador, umbral, accion, w0, bit]


@njit(cache=True)
def _kk_deriva(t, s):
    """PLAST_RW0: una letra seudoazar que depende solo de (t, cuerpo): no consume azar de nadie y no sabe que se mordio."""
    h = (t * 2654435761 + s * 40503 + 977) % 2147483647
    return (h >> 7) & 3


@njit(cache=True)
def _reglas_aprende(s, RG, RN, RM, RPL, E, Ag, d, kk, PATM, Rt, ETAS, AV, PLC):
    """Rescorla-Wagner LOCAL: cada regla de boca plastica cuya condicion se cumplia al decidir mueve SU peso hacia la consecuencia."""
    nn = 0
    for r in range(RN[s]):
        if int(RG[s, r, 4]) != 0 or RPL[s, r, 0] < 0.5: continue
        if not _cumple(s, r, RG, RM, E, Ag, d, kk, PATM): continue
        w = RG[s, r, 5]; dl = Rt - w
        if dl > 0: w = w + ETAS * dl
        else: w = w + ETAS * AV * dl
        RG[s, r, 5] = _clip(w, -3.0, 3.0); nn += 1
    if nn > 0:
        PLC[0] += nn; PLC[1] += 1


@njit(cache=True)
def _empaca_pl(u, RG, RN, RPL):
    """Las reglas GENETICAS del cuerpo u: el peso es w0 (no el aprendido) y la ultima columna el bit."""
    m = RN[u]; o = np.zeros((m, NRCP))
    for r in range(m):
        for c in range(NRC): o[r, c] = RG[u, r, c]
        o[r, 5] = RPL[u, r, 1]; o[r, NRC] = RPL[u, r, 0]
    return o


@njit(cache=True)
def _instala_pl(s3, ch, RG, RN, RPL):
    m = ch.shape[0]
    for r in range(m):
        for c in range(NRC): RG[s3, r, c] = ch[r, c]   # el peso EN VIDA arranca en w0
        RPL[s3, r, 0] = ch[r, NRC]; RPL[s3, r, 1] = ch[r, 5]
    RN[s3] = m


@njit(cache=True)
def _reglas_hijo_pl(lin, k, s, s3, RG, RN, RPL, bi, cuer, nb, L):
    """Como _reglas_hijo (mismo vecino de la HGT), con las reglas geneticas (w0 y bit) del padre y del vecino."""
    p = bi[s, I_POS]; v = -1; dv = L + 1
    for jj in range(nb):
        u = cuer[jj]
        if u < 0 or u == s or u == s3: continue
        a = bi[u, I_POS] - p
        if a < 0: a = -a
        if L - a < a: a = L - a
        if a < dv:
            dv = a; v = u
    rp = _empaca_pl(s, RG, RN, RPL)
    if v >= 0: rv = _empaca_pl(v, RG, RN, RPL)
    else: rv = np.zeros((0, NRCP))
    with objmode(ch='float64[:, :]'):
        ch = _py_reglas_hijo_pl(lin, k, rp, rv)
    _instala_pl(s3, ch, RG, RN, RPL)


@njit(cache=True)
def _reglas_fund_pl(lin, nac, s2, RG, RN, RPL):
    with objmode(ch='float64[:, :]'):
        ch = _py_reglas_fund_pl(lin, nac)
    _instala_pl(s2, ch, RG, RN, RPL)


def _muta_reglas_pl(base, vec, rr, rb, C, O):
    """_muta_reglas con la MISMA secuencia de llamadas a rr (las reglas evolucionan igual que en BLOQUES), llevando el bit (col. 6) por
    duplicar, borrar y HGT; el bit de la regla insertada y las inversiones del bit salen de rb (rng propio)."""
    R = [list(map(float, x)) for x in base]
    for x in R:
        if rr.random() < C['p_campo']:
            f = int(rr.integers(0, 6)); O['n_campo'] += 1
            if f == 0: x[0] = float(rr.integers(0, _kit()[0]))
            elif f == 1: x[1] = float(rr.integers(0, 6))
            elif f == 2: x[2] = 1.0 - x[2]
            elif f == 3: x[3] = float(min(1.0, max(0.0, x[3] + rr.normal(0, 0.15))))
            elif f == 4: x[4] = float(rr.integers(0, _kit()[1]))
            else: x[5] = float(min(3.0, max(-3.0, x[5] + rr.normal(0, 0.5))))
    if R and rr.random() < C['p_dup']:
        i = int(rr.integers(0, len(R))); R.insert(i + 1, list(R[i])); O['n_dup'] += 1
    if R and rr.random() < C['p_del']:
        del R[int(rr.integers(0, len(R)))]; O['n_del'] += 1
    if rr.random() < C['p_ins']:
        x = _regla_azar(rr); x.append(1.0 if rb.random() < C['p_ins_pl'] else 0.0); R.append(x); O['n_ins'] += 1
    if len(vec) and rr.random() < C['p_hgt']:
        R.append(list(map(float, vec[int(rr.integers(0, len(vec)))]))); O['n_hgt'] += 1
    tp = int(C.get('tope', 12))
    if len(R) > tp:
        R = R[:tp]; O['n_tope'] += 1
    for x in R:
        if rb.random() < C['p_bit']:
            x[6] = 1.0 - x[6]; O['n_flip'] += 1
    if int(C['plast']) == 2:   # PLAST_AZA: el bit se sortea al nacer (sin herencia); la regla si se hereda
        for x in R: x[6] = float(rb.integers(0, 2))
    return np.ascontiguousarray(np.array(R, np.float64).reshape(len(R), NRCP))


def _py_reglas_hijo_pl(lin, k, rp, rv):
    C = _CTX['BQC']; O = BQ_OUT; BR = _CTX['BR']
    rr = np.random.default_rng([_CTX['seed'], int(lin), 7701, int(k)])
    rb = np.random.default_rng([_CTX['seed'], int(lin), 7711, int(k)])
    base = rp
    if C['donante'] == 'azar':
        base = BR[int(rr.integers(len(BR)))] if BR else np.zeros((0, NRCP))
    ch = _muta_reglas_pl(base, rv, rr, rb, C, O)
    O['n_hijos'] += 1
    if ch.shape == rp.shape and np.array_equal(ch, rp): O['n_igual_padre'] += 1
    if len(rp):
        O['n_hijos_pl'] += 1
        if ch.shape == rp.shape and np.array_equal(ch, rp): O['n_igual_pl'] += 1
    if C['banco']:
        BR.append(rp.copy() if C['donante'] == 'padre' else ch.copy())
        if len(BR) > C['banco']: BR.pop(0)
    return ch


def _py_reglas_fund_pl(lin, nac):
    C = _CTX['BQC']; O = BQ_OUT; BR = _CTX['BR']
    rr = np.random.default_rng([_CTX['seed'], int(lin), 7702, int(nac)])
    rb = np.random.default_rng([_CTX['seed'], int(lin), 7712, int(nac)])
    base = BR[int(rr.integers(len(BR)))] if BR else np.zeros((0, NRCP))
    ch = _muta_reglas_pl(base, np.zeros((0, NRCP)), rr, rb, C, O)
    O['n_fund'] += 1
    if C['donante'] == 'azar' and C['banco']:
        BR.append(ch.copy())
        if len(BR) > C['banco']: BR.pop(0)
    return ch


def _bq_arranque_pl(st, n, C):
    """Arranque FRESCO (en --reanuda no se llama: el banco y BQ_OUT viajan en ES): w0 = peso de las reglas iniciales, su bit
    (forzada_bit o 0), el banco en 7 columnas y la telemetria de la plasticidad."""
    for i in range(n):
        m = int(st['RN'][i])
        for r in range(m):
            st['RPL'][i, r, 1] = st['RG'][i, r, 5]
            st['RPL'][i, r, 0] = float(C['forzada_bit'][r]) if C.get('forzada_bit') is not None else 0.0
    if C['banco']:
        _CTX['BR'][:] = [np.ascontiguousarray(np.hstack([st['RG'][i, :st['RN'][i]], st['RPL'][i, :st['RN'][i], :1]]))
                         for i in range(n)][-int(C['banco']):]   # col. 5 = w0 (en t = 0 nadie aprendio), col. 6 = bit
    BQ_OUT.update(n_flip=0, serie_pl=[])


PATM_BQ = ((1, 1, 0, 1, 0, 0), (1, 0, 1, 0, 1, 0), (0, 1, 1, 0, 0, 1), (0, 0, 1, 0, 1, 1))   # A, B, C, D (pista2.cfg_fabrica PAT)


def _discrimina(x):
    """Regla de boca sobre el pixel del foco cuya condicion separa las letras (se cumple en 1, 2 o 3 de las 4)."""
    if int(x[0]) != 3 or int(x[4]) != 0: return False
    c = sum(1 for P_ in PATM_BQ if ((P_[int(x[1])] > x[3]) if x[2] > 0.5 else (P_[int(x[1])] < x[3])))
    return 0 < c < 4


def _bq_muestra_pl(st, t, v):
    """[t, vivos, frac plastica en reglas de boca, frac plastica en reglas de boca que discriminan letras, n de estas, media |w - w0| en
    las plasticas de boca] sobre los cuerpos vivos."""
    nb_ = npl = nd = ndp = 0; dw = []
    for s in v:
        for r in range(int(st['RN'][s])):
            x = st['RG'][s, r]
            if int(x[4]) != 0: continue
            pl = st['RPL'][s, r, 0] > 0.5; nb_ += 1; npl += pl
            if pl: dw.append(abs(float(x[5] - st['RPL'][s, r, 1])))
            if _discrimina(x): nd += 1; ndp += pl
    BQ_OUT['serie_pl'].append([int(t), len(v), (round(npl / nb_, 4) if nb_ else None), (round(ndp / nd, 4) if nd else None), nd,
                               (round(float(np.mean(dw)), 4) if dw else None)])


def _bq_final_pl(st, vivos):
    BQ_OUT['vivos_T_pl'] = [[[int(st['RPL'][s, r, 0] > 0.5), round(float(st['RPL'][s, r, 1]), 4)] for r in range(int(st['RN'][s]))]
                            for s in vivos]
    BQ_OUT['n_aprende'] = int(st['PLC'][0]); BQ_OUT['n_mord_aprende'] = int(st['PLC'][1])


# ================================================================ BLOQUES2 (anadido por construye_bloques2.py): el kit grande'''

A.append(('W15 bloque nuevo', "\n\n# ================================================================ BLOQUES2 (anadido por construye_bloques2.py): el kit grande", NUEVO))


def construye():
    if h16(ORIGEN) != SHA_ORIGEN: raise SystemExit(f'origen cambio: {h16(ORIGEN)} != {SHA_ORIGEN}')
    txt = open(ORIGEN, encoding='utf-8').read()
    for nom, viejo, nuevo in A:
        c = txt.count(viejo)
        if c != 1: raise SystemExit(f'ancla {nom}: aparece {c} veces (debe ser 1)')
        txt = txt.replace(viejo, nuevo)
    return txt


if __name__ == '__main__':
    t = construye()
    if '--verifica' in sys.argv:
        print('IGUAL' if os.path.exists(DESTINO) and open(DESTINO, encoding='utf-8').read() == t else 'DISTINTO', h16(DESTINO) if os.path.exists(DESTINO) else '-')
    else:
        with open(DESTINO, 'w', encoding='utf-8', newline='\n') as f: f.write(t)
        print('escrito', DESTINO, h16(DESTINO), f'({len(A)} anclas, origen {SHA_ORIGEN})')
