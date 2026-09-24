"""motor_eco_rapido.py — GEMELO COMPILADO (numba) de experimentos/juaco_eco/motor_eco.py (run_solapadas) con el cerebro
FABRICA / FABRICA_ECO (carrera_escuderias/carros/FABRICA.py, juaco_eco/carros/FABRICA_ECO.py).

MISION: llegar a la AGI por este camino (organismo minimo, reglas locales, sin retropropagacion, peldanos preregistrados
con controles y replicas). Un gemelo que no sea BIT A BIT identico solo EXPLORA, nunca confirma (regla 9 de
registro/EQUIPO.md). Arnes: identidad_eco_rapido.py (su salida va en identidad_eco_rapido_salida.txt).

NO es un mundo nuevo ni un organismo nuevo: la MISMA fisica de la pista v2 (quimiostato, olvido, costos, ventana, parto
real, fundador limpio, tope) y el MISMO cerebro (FABRICA: dos vias, puerta por codigo, CUELLO_MIN, division por conflicto
con hija dispersa, memoria de rechazo), con el MISMO flujo de azar, y con eco=dict(...) la MISMA plomeria de JUACO-ECO
(genoma de 18 perillas por cuerpo, mutacion, sombras, banco, vivero y corte, refunda, donante padre/azar, muestra de
genes, checkpoint). Misma firma que motor_eco.run_solapadas y la misma salida (TODAS las claves).

COMO SE USA: `import motor_eco_rapido as MR; MR.run_solapadas(...)` con los mismos argumentos. Para correr el runner
corre_eco.py SIN cambiar su letra: corre_eco_rapido.py cambia el motor del modulo (CR.ME) por un envoltorio que llama a
este gemelo y delega en corre_eco.main() (mismas banderas, mismos criterios, mismo veredicto).

QUE SE DELEGA EN NUMPY / PYTHON Y POR QUE (regla 9)
  - np.exp: en ESTA maquina (AVX512) NumPy usa su propio exp vectorial y difiere de libm (el exp de numba) en ~4.6 % de
    los argumentos. El gemelo llama al MISMO bucle 1-D float64 de np.exp (puntero sacado del objeto ufunc por ctypes y
    verificado al importar contra np.exp en 200 000 argumentos). Se usa para p (dos neuronas de marcha) y pb (la boca).
  - productos escalares (@): numba llama a BLAS (ddot / dgemv, OpenBLAS de SciPy) como NumPy (OpenBLAS de NumPy); el
    arnes comprueba que dan lo mismo en las formas usadas (90x6 @ 6, 2x9 @ 9, 90 . 90, 6 . 6).
  - Generator: el del mundo, el de la pista, el de fundadores y el de reaparicion de cada linaje se crean en Python y se
    pasan al bucle. Cada cuerpo tiene SU Generator ([seed, linaje, 12, k]) y su hijo otro ([seed, linaje, 13, k]); numba
    no tiene default_rng/SeedSequence: se crean en `objmode` en el parto (una vez por nacimiento) y viven en una
    numba.typed.List de Generators (un puntero al estado C de NumPy por ranura; los fundadores de un linaje COMPARTEN el
    objeto, como en el original). Todas las extracciones (normal, random, integers, uniform, permutation) las hace numba
    sobre el estado real de NumPy: al volver, el estado de cada Generator es el del original (rng_mundo_estado incluido).
  - JUACO-ECO en el parto y en la refundacion (banco, donante, mutacion del genoma y de las sombras): en `objmode`, con
    las MISMAS lineas del original (ME.muta, la lista ES['banco']), una vez por evento.
  - argsort con EMPATE en la frontera del top-K (codigo de Kenyon): a NumPy (np.argsort) por `objmode`; sin empate el
    top-3 es unico por valor y se toma con un barrido de los 4 mayores.
  - muestra de genes (_muestra_gen), foto del corte, checkpoint, individuos por flujo (ind_cb) y salida() del carro: en
    Python con el codigo del original, en las fronteras de tramo (el nucleo corre por tramos entre eventos de Python).
  - sumas: la unica suma de reales es la de 6 elementos (mu[c].sum(), P.sum()): NumPy suma n < 8 de izquierda a derecha
    desde 0.0 y el bucle lo reproduce (comprobado). No hay sumas de >= 8 reales en el nucleo.
  - ninguna funcion recursiva (cache=True).

FUERA DE ALCANCE (el gemelo ABORTA con ValueError en vez de callar; el original si los admite): cualquier carro que no sea
FABRICA / FABRICA_ECO (APR, O1..O4, ...), la pizarra con escrituras (FABRICA no escribe: pizarra_log queda vacia igual que
en el original), y un checkpoint del ORIGINAL (el formato del estado es propio; la firma lo distingue y aborta).
Si cambian motor_eco.py, FABRICA_ECO.py, FABRICA.py o pista2.py (sha fijados abajo), el gemelo se niega a correr.
"""
import ctypes, hashlib, math, os, pickle, sys, types
import numpy as np
import numba
from numba import njit, objmode, typed

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
GEN = os.path.join(RAIZ, 'experimentos', 'generaciones')
for _d in (GEN, AQUI):
    if _d not in sys.path: sys.path.insert(0, _d)
import motor_eco as ME    # el ORIGINAL (solo se LEE: guardias, _eco_cfg, muta, ctx_genoma, GENES)
import pista2 as P

SHA = {os.path.join(AQUI, 'motor_eco.py'): 'bca3033878b59622',
       os.path.join(AQUI, 'carros', 'FABRICA_ECO.py'): 'f1163009cb5193a2',
       os.path.join(RAIZ, 'experimentos', 'carrera_escuderias', 'carros', 'FABRICA.py'): '2ebee3e99ea5a33a',
       os.path.join(GEN, 'pista2.py'): '4d2bee16e7961261'}
CEREBROS = {'FABRICA.py': '2ebee3e99ea5a33a', 'FABRICA_ECO.py': 'f1163009cb5193a2'}
FIRMA_GEMELO = 'motor_eco_rapido v1'


def _h16(p):
    return hashlib.sha256(open(p, 'rb').read()).hexdigest()[:16]


NKMAX = 90; K = 3; NNEC = 2
NCOD = 4 * (NKMAX + 1)   # codigos distintos por cuerpo: <= 4 x (divisiones + 1) <= 4 x (NKMAX - NK + 1)
RC = 256                 # entradas VIGENTES de la memoria de rechazo por cuerpo (<= memoria_rechazo <= 80 en ECO)
NST = NKMAX + 1          # divisiones por cuerpo (<= NKMAX - NK)
GENT = numba.typeof(np.random.default_rng(1))
_DUMMY = np.random.default_rng(987654321)   # ocupa las ranuras libres de la lista de Generators; NUNCA se extrae de el

# ---------------------------------------------------------------- indices del estado (arrays planos)
# por cuerpo, enteros (bi)
(I_POS, I_GV, I_TB, I_TD, I_VOL, I_HIJ, I_FUND, I_LIN, I_K, I_GEN, I_PADRE, I_TN, I_MR, I_NK, I_SPL, I_TCON, I_TTEC,
 I_NTEC, I_GPA, I_GPN, I_NA, I_NM, I_RN, I_NST, I_NCN, I_SO0) = range(26)
NBI = 30   # I_SO0..I_SO0+3 = sin_objetivo
# por cuerpo, reales (bf)
(F_E, F_AG, F_ETA, F_TAU, F_ALPHA, F_HB, F_AV, F_EMA, F_PASO, F_LAM, F_ETAS, F_CLIPS, F_DELS, F_DELC, F_EMAC, F_DOTE,
 F_RU, F_RX, F_ERRMAX, F_R, F_RP, F_HAMB) = range(22)
NBF = 22
# por linaje (li)
(L_VIVOS, L_DEATHS, L_MN0, L_MN1, L_CZ0, L_CZ1, L_CZ2, L_CZ3, L_MVOL, L_FUND, L_NTF, L_DESC, L_NAC, L_BLOQ, L_PV) = range(15)
NLI = 15
# mundo (wi)
(W_PISOS, W_LLEG, W_PERD, W_OLV, W_NSUMA, W_TOTAL, W_MAXV, W_TTOPE, W_NOBJ, W_NSEQ, W_NCUER, W_NROWS, W_NTZ, W_NTIES,
 W_NFREE, W_ERR, W_COMP0, W_COMP1, W_COMP2, W_COMP3, W_CNT0, W_CNT1, W_CNT2, W_CNT3) = range(24)
NWI = 24
# parametros enteros (pi) y reales (pf)
(P_T, P_L, P_ESC, P_NOBJ, P_INST, P_RACUM, P_TOPE, P_MUESTRA, P_ECO, P_REFUNDA, P_TCORTE, P_N, P_QDIV, P_PPAT, P_PMIN,
 P_WCAUSA, P_TRAZA, P_MEXP, P_MDOT, P_MTURNO, P_C, P_LOG) = range(22)
NPI = 22
(Q_COSTO, Q_COSTOA, Q_OLV, Q_RPASO, Q_DOTEM, Q_AINI) = range(6)
NPF = 6
# estados de salida del tramo
ST_OK, ST_EXT, ST_CRECE, ST_ERR = 0, 1, 2, 3
ERR_NAC, ERR_RECH, ERR_NCOD, ERR_NST = 1, 2, 3, 4
ERR_MSG = {ERR_NAC: 'PISTA2: mas de 100000 cuerpos en un linaje: la semilla colisionaria (ERR-60)',
           ERR_RECH: f'motor_eco_rapido: mas de {RC} entradas vigentes de rechazo en un cuerpo (sube RC)',
           ERR_NCOD: f'motor_eco_rapido: mas de {NCOD} codigos distintos en un cuerpo (sube NCOD)',
           ERR_NST: f'motor_eco_rapido: mas de {NST} divisiones en un cuerpo (sube NST)'}


# ================================================================ np.exp de NumPy (bucle 1-D float64 por ctypes)
def _bucle_exp_numpy():
    """Puntero al bucle 1-D float64 de np.exp que NumPy usa en ESTA maquina (PyUFuncObject: functions, types)."""
    a = id(np.exp)
    rd = lambda off, t: t.from_address(a + off).value
    nargs = rd(24, ctypes.c_int); functions = rd(32, ctypes.c_void_p); data = rd(40, ctypes.c_void_p)
    ntypes = rd(48, ctypes.c_int); name = ctypes.c_char_p(rd(56, ctypes.c_void_p)).value; types_p = rd(64, ctypes.c_void_p)
    if name != b'exp' or nargs != 2 or not functions or not types_p:
        raise RuntimeError('motor_eco_rapido: no se reconoce la estructura PyUFuncObject de np.exp (version de NumPy)')
    tys = ctypes.string_at(types_p, ntypes * nargs); d = np.dtype('f8').num
    idx = [i for i in range(ntypes) if tys[i * nargs] == d and tys[i * nargs + 1] == d]
    if not idx: raise RuntimeError('motor_eco_rapido: np.exp sin bucle float64')
    f = ctypes.c_void_p.from_address(functions + 8 * idx[0]).value
    dat = (ctypes.c_void_p.from_address(data + 8 * idx[0]).value if data else None) or 0
    return ctypes.CFUNCTYPE(None, ctypes.c_int64, ctypes.c_int64, ctypes.c_int64, ctypes.c_int64)(f), int(dat)


EXP_LOOP, EXP_DATA = _bucle_exp_numpy()


def _bufs_exp():
    """Buffers FIJOS del bucle de exp: xin[2], xout[2], args (direcciones), dims, steps; adr = direcciones de los tres."""
    xin = np.zeros(2); xout = np.zeros(2)
    args = np.array([xin.ctypes.data, xout.ctypes.data], np.int64)
    dims = np.array([1], np.int64); steps = np.array([8, 8], np.int64)
    adr = np.array([args.ctypes.data, dims.ctypes.data, steps.ctypes.data, EXP_DATA], np.int64)
    return (xin, xout, args, dims, steps, adr)


def _autoprueba_exp():
    xin, xout, args, dims, steps, adr = B = _bufs_exp()
    r = np.random.default_rng(20260924)
    xs = np.concatenate([r.uniform(-40, 40, 100000), r.normal(0, 3, 100000),
                         np.array([0.0, -0.0, 1e-300, -745.2, 709.7, 710.0, -800.0, 1.0, -1.0, 0.5])])
    with np.errstate(over='ignore'): ref = np.exp(xs)
    out = np.empty_like(xs)
    for i in range(0, xs.size, 2):
        n = min(2, xs.size - i); xin[:n] = xs[i:i + n]; dims[0] = n
        EXP_LOOP(int(adr[0]), int(adr[1]), int(adr[2]), int(adr[3])); out[i:i + n] = xout[:n]
    if not np.array_equal(ref.view(np.int64), out.view(np.int64)):
        raise RuntimeError('motor_eco_rapido: el bucle de np.exp no reproduce np.exp: el gemelo no puede ser identico aqui')
    return B


_BUF_EXP_PRUEBA = _autoprueba_exp()


# ================================================================ utilidades compiladas
@njit(cache=True)
def _clip(x, lo, hi):
    """np.clip de NumPy para reales: min(max(x, lo), hi) con max(a,b) = a>b?a:b y min(a,b) = a<b?a:b."""
    r = x if x > lo else lo
    return r if r < hi else hi


@njit(cache=True)
def _npmin(a, b):
    return a if a < b else b


@njit(cache=True)
def _exp1(x, lp, xin, xout, dims, adr, mexp):
    if mexp != 0: return math.exp(x)   # CONTROL (debe fallar): libm
    xin[0] = x; dims[0] = 1
    lp(adr[0], adr[1], adr[2], adr[3])
    return xout[0]


@njit(cache=True)
def _exp2(x0, x1, lp, xin, xout, dims, adr, mexp):
    if mexp != 0: return math.exp(x0), math.exp(x1)
    xin[0] = x0; xin[1] = x1; dims[0] = 2
    lp(adr[0], adr[1], adr[2], adr[3])
    return xout[0], xout[1]


@njit(cache=True)
def _dot(a, b, n, mdot):
    if mdot == 0: return np.dot(a, b)
    s = 0.0   # CONTROL (debe fallar): suma de izquierda a derecha
    for i in range(n): s += a[i] * b[i]
    return s


# ---------------------------------------------------------------- el mundo: dict en orden de insercion (grid + BIT)
@njit(cache=True)
def _bit_add(bit, C, i, v):
    i += 1
    while i <= C:
        bit[i] += v
        i += i & (-i)


@njit(cache=True)
def _bit_sel(bit, C, LOG, k):
    """seq (0-based) del k-esimo objeto vivo (0-based) en orden de insercion."""
    pos = 0; rem = k + 1; st = LOG
    while st > 0:
        nx = pos + st
        if nx <= C and bit[nx] < rem:
            pos = nx; rem -= bit[nx]
        st >>= 1
    return pos


@njit(cache=True)
def _compacta(oseq, seqpos, bit, wi, C):
    m = 0
    for s in range(wi[W_NSEQ]):
        x = seqpos[s]
        if x >= 0:
            seqpos[m] = x; oseq[x] = m; m += 1
    for s in range(m, C): seqpos[s] = -1
    for i in range(C + 1): bit[i] = 0
    for s in range(m): _bit_add(bit, C, s, 1)
    wi[W_NSEQ] = m


@njit(cache=True)
def _pon(x, tp, grid, oseq, seqpos, bit, wi, C):
    """objs[x] = TIPOS[tp] con x NUEVO (va al final del orden de insercion)."""
    s = wi[W_NSEQ]
    grid[x] = tp; oseq[x] = s; seqpos[s] = x; _bit_add(bit, C, s, 1)
    wi[W_NSEQ] = s + 1; wi[W_CNT0 + tp] += 1; wi[W_NOBJ] += 1
    if wi[W_NSEQ] == C: _compacta(oseq, seqpos, bit, wi, C)


@njit(cache=True)
def _saca(x, grid, oseq, seqpos, bit, wi, C):
    """del objs[x]."""
    tp = grid[x]; s = oseq[x]
    grid[x] = -1; seqpos[s] = -1; _bit_add(bit, C, s, -1)
    wi[W_CNT0 + tp] -= 1; wi[W_NOBJ] -= 1


@njit(cache=True)
def _spawn(rng, L, nobj, grid, oseq, seqpos, bit, wi, C):
    while wi[W_NOBJ] < nobj:
        x = rng.integers(0, L)
        if grid[x] < 0: _pon(x, rng.integers(0, 4), grid, oseq, seqpos, bit, wi, C)


@njit(cache=True)
def _quita(x, inst, rng, L, nobj, grid, oseq, seqpos, bit, wi, C):
    """P7: con 'inmediata' se repone al instante; con 'fija' solo se quita (piso de 1 objeto)."""
    _saca(x, grid, oseq, seqpos, bit, wi, C)
    if inst: _spawn(rng, L, nobj, grid, oseq, seqpos, bit, wi, C)
    elif wi[W_NOBJ] == 0:
        wi[W_PISOS] += 1; x2 = rng.integers(0, L); _pon(x2, rng.integers(0, 4), grid, oseq, seqpos, bit, wi, C)


# ---------------------------------------------------------------- memoria de rechazo (solo las entradas VIGENTES)
@njit(cache=True)
def _rget(rpos, rexp, bi, s, x):
    for i in range(bi[s, I_RN]):
        if rpos[s, i] == x: return rexp[s, i]
    return -1


@njit(cache=True)
def _rset(rpos, rexp, bi, s, x, v, t):
    """_rech[x] = v. Las entradas vencidas (<= t) equivalen a ausentes para todo t' >= t: se purgan aqui."""
    n = bi[s, I_RN]; m = 0
    for i in range(n):
        if rpos[s, i] != x and rexp[s, i] > t:
            rpos[s, m] = rpos[s, i]; rexp[s, m] = rexp[s, i]; m += 1
    if m >= RC: return False
    rpos[s, m] = x; rexp[s, m] = v; bi[s, I_RN] = m + 1
    return True


@njit(cache=True)
def _rpop(rpos, rexp, bi, s, x):
    n = bi[s, I_RN]
    for i in range(n):
        if rpos[s, i] == x:
            rpos[s, i] = rpos[s, n - 1]; rexp[s, i] = rexp[s, n - 1]; bi[s, I_RN] = n - 1
            return


# ---------------------------------------------------------------- vision (FABRICA_ECO._see + _elige)
@njit(cache=True)
def _elige(pos, L, xl, kl, xr, kr, oseq):
    if xl >= 0 and xr >= 0:
        x = xl if oseq[xl] < oseq[xr] else xr   # el primero en el orden del dict
    else:
        x = xl if xl >= 0 else xr
    k = kl if x == xl else kr
    a = pos - x   # (pos - x) % L y (x - pos) % L con 0 <= pos, x < L: sin division (identidad entera exacta)
    if a < 0: a += L
    b = x - pos
    if b < 0: b += L
    return k, a < b


@njit(cache=True)
def _see(s, pos, t, contar, q, L, grid, oseq, rpos, rexp, bi):
    MR = bi[s, I_MR]
    fd = -1; fk = -1; fl = False
    for d in range(L // 2 + 1):
        xl = pos - d   # (pos -+ d) % L con 0 <= pos < L y 0 <= d <= L // 2: sin division (identidad entera exacta)
        if xl < 0: xl += L
        xr = pos + d
        if xr >= L: xr -= L
        kl = grid[xl]
        kr = grid[xr] if xr != xl else -1
        if kl < 0 and kr < 0: continue
        el = kl >= 0 and (MR == 0 or _rget(rpos, rexp, bi, s, xl) <= t)
        er = kr >= 0 and (MR == 0 or _rget(rpos, rexp, bi, s, xr) <= t)
        if el or er:
            k, left = _elige(pos, L, xl if el else -1, kl, xr if er else -1, kr, oseq)
            return d, k, left
        if fd < 0:
            fk, fl = _elige(pos, L, xl if kl >= 0 else -1, kl, xr if kr >= 0 else -1, kr, oseq)
            fd = d
    if contar: bi[s, I_SO0 + q] += 1
    return fd, fk, fl


# ---------------------------------------------------------------- codigo de Kenyon (top-K) y evidencia por codigo
def _py_top(w):
    """EMPATE en la frontera del top-K: manda NumPy (np.argsort, el mismo algoritmo que el original)."""
    return np.sort(np.argsort(w)[-K:]).astype(np.int64)


@njit(cache=True)
def _code3(s, p, KW, act, PATM, ccode, cval, wbuf, mdot, wi):
    """ccode[s, p] = indices (ascendentes) del codigo de PAT[p] con el KW/activa de la ranura s (en cache hasta dividir)."""
    if cval[s, p]: return
    if mdot == 0:
        v = KW[s] @ PATM[p]
    else:
        v = np.zeros(NKMAX)
        for i in range(NKMAX):
            a = 0.0
            for j in range(6): a += KW[s, i, j] * PATM[p, j]
            v[i] = a
    for i in range(NKMAX): wbuf[i] = v[i] if act[s, i] else -1e9
    b0 = -np.inf; b1 = -np.inf; b2 = -np.inf; b3 = -np.inf; i0 = -1; i1 = -1; i2 = -1; i3 = -1
    for i in range(NKMAX):
        x = wbuf[i]
        if x > b3:
            if x > b2:
                b3 = b2; i3 = i2
                if x > b1:
                    b2 = b1; i2 = i1
                    if x > b0:
                        b1 = b0; i1 = i0; b0 = x; i0 = i
                    else:
                        b1 = x; i1 = i
                else:
                    b2 = x; i2 = i
            else:
                b3 = x; i3 = i
    if b2 == b3:
        with objmode(ix='int64[:]'):
            ix = _py_top(wbuf)
        wi[W_NTIES] += 1
        ccode[s, p, 0] = ix[0]; ccode[s, p, 1] = ix[1]; ccode[s, p, 2] = ix[2]
    else:
        a = i0; b = i1; c = i2
        if a > b: a, b = b, a
        if b > c: b, c = c, b
        if a > b: a, b = b, a
        ccode[s, p, 0] = a; ccode[s, p, 1] = b; ccode[s, p, 2] = c
    cval[s, p] = True


@njit(cache=True)
def _clave(c3):
    return (c3[0] + 1) * (NKMAX + 1) * (NKMAX + 1) + (c3[1] + 1) * (NKMAX + 1) + (c3[2] + 1)


@njit(cache=True)
def _ncget(nck, ncc, bi, s, key):
    for i in range(bi[s, I_NCN]):
        if nck[s, i] == key: return ncc[s, i]
    return 0


@njit(cache=True)
def _fam(Wp, Wn, s, n, c3, key, nck, ncc, bi, ppat, pmin):
    if not (_ncget(nck, ncc, bi, s, key) >= ppat): return False
    c = 0
    for a in range(K):
        i = c3[a]
        if abs(Wp[s, n, i] - Wn[s, n, i]) > 0.2: c += 1
    return c >= pmin


@njit(cache=True)
def _cond(s, KW, act, PATM, ccode, cval, wbuf, mdot, wi):
    """len(code(A) & code(B)) == 0."""
    _code3(s, 0, KW, act, PATM, ccode, cval, wbuf, mdot, wi)
    _code3(s, 1, KW, act, PATM, ccode, cval, wbuf, mdot, wi)
    for a in range(K):
        for b in range(K):
            if ccode[s, 0, a] == ccode[s, 1, b]: return False
    return True


# ---------------------------------------------------------------- crea(ctx) y nace(info) del carro
@njit(cache=True)
def _crea(s, r, bi, bf, Wl, el, tr, KW, act, Wp, Wn, Wps, Wns, err, mu, mup, mun, zp, zn, ccode, cval, PATM, wbuf, mdot, wi):
    """Carro.__init__: Wl y KW del rng del cuerpo, con la condicion de codigos A y B disjuntos; todo lo demas a cero."""
    NK = bi[s, I_NK]
    u = r.uniform(.1, .4, (2, 9))
    for a in range(2):
        for b in range(9): Wl[s, a, b] = u[a, b]
    for i in range(NKMAX):
        act[s, i] = False
        for j in range(6): KW[s, i, j] = 0.0
    u2 = r.uniform(0, 1, (NK, 6))
    for i in range(NK):
        act[s, i] = True
        for j in range(6): KW[s, i, j] = u2[i, j]
    for p in range(4): cval[s, p] = False
    while not _cond(s, KW, act, PATM, ccode, cval, wbuf, mdot, wi):
        u2 = r.uniform(0, 1, (NK - 0, 6))
        for i in range(NK):
            for j in range(6): KW[s, i, j] = u2[i, j]
        for p in range(4): cval[s, p] = False
    for a in range(2):
        for b in range(9): el[s, a, b] = 0.0
    for b in range(9): tr[s, b] = 0.0
    for n in range(NNEC):
        for i in range(NKMAX):
            Wp[s, n, i] = 0.0; Wn[s, n, i] = 0.0
        for j in range(6):
            Wps[s, n, j] = 0.0; Wns[s, n, j] = 0.0
    for i in range(NKMAX):
        err[s, i] = 0.0; zp[s, i] = 0.0; zn[s, i] = 0.0
        for j in range(6):
            mu[s, i, j] = 0.0; mup[s, i, j] = 0.0; mun[s, i, j] = 0.0
    bi[s, I_SPL] = 0; bi[s, I_TCON] = -1; bi[s, I_TTEC] = -1; bi[s, I_NTEC] = 0; bi[s, I_GPA] = 0; bi[s, I_GPN] = 0
    bi[s, I_NA] = 0; bi[s, I_NM] = 0; bi[s, I_RN] = 0; bi[s, I_NST] = 0; bi[s, I_NCN] = 0
    for q in range(4): bi[s, I_SO0 + q] = 0
    bf[s, F_ERRMAX] = 0.0; bf[s, F_R] = 0.0; bf[s, F_RP] = 0.0; bf[s, F_HAMB] = 0.0


@njit(cache=True)
def _nace(s, rh, bi, Wl, el, tr, KW, act, ccode, cval, PATM, wbuf, mdot, wi):
    """Carro.nace con hereda='nada': Wl y KW nuevos del rng del hijo (lo demas ya esta a cero; el nodo del cuerpo
    nuevo esta vacio en la pista v2, asi que no se lee nada)."""
    NK = bi[s, I_NK]
    u = rh.uniform(.1, .4, (2, 9))
    for a in range(2):
        for b in range(9):
            Wl[s, a, b] = u[a, b]; el[s, a, b] = 0.0
    for b in range(9): tr[s, b] = 0.0
    bi[s, I_NCN] = 0; bi[s, I_RN] = 0
    for i in range(NKMAX):
        act[s, i] = False
        for j in range(6): KW[s, i, j] = 0.0
    u2 = rh.uniform(0, 1, (NK, 6))
    for i in range(NK):
        act[s, i] = True
        for j in range(6): KW[s, i, j] = u2[i, j]
    for p in range(4): cval[s, p] = False
    while not _cond(s, KW, act, PATM, ccode, cval, wbuf, mdot, wi):
        u2 = rh.uniform(0, 1, (NK - 0, 6))
        for i in range(NK):
            for j in range(6): KW[s, i, j] = u2[i, j]
        for p in range(4): cval[s, p] = False


@njit(cache=True)
def _consts(s, g, GI, bi, bf, fijo):
    """ctx_genoma: las perillas del cerebro y la historia de vida de la ranura s desde el genoma g (enteros con round())."""
    if fijo:
        return
    bf[s, F_ETA] = g[GI[0]]; bf[s, F_TAU] = g[GI[1]]; bf[s, F_ALPHA] = g[GI[2]]; bf[s, F_HB] = g[GI[3]]
    bf[s, F_AV] = g[GI[4]]; bf[s, F_EMA] = g[GI[5]]; bf[s, F_PASO] = g[GI[6]]; bf[s, F_LAM] = g[GI[7]]
    bi[s, I_MR] = int(np.rint(g[GI[8]])); bf[s, F_ETAS] = g[GI[9]]; bf[s, F_CLIPS] = g[GI[10]]
    bf[s, F_DELS] = g[GI[11]]; bf[s, F_DELC] = g[GI[12]]; bf[s, F_EMAC] = g[GI[13]]; bi[s, I_NK] = int(np.rint(g[GI[14]]))
    bf[s, F_DOTE] = g[GI[15]]; bf[s, F_RU] = g[GI[16]]; bf[s, F_RX] = g[GI[17]]


@njit(cache=True)
def _consts_fab(s, bi, bf, C0i, C0f):
    """Sin genoma: las constantes de fabrica (fila plantilla)."""
    for j in range(NBF): bf[s, j] = C0f[j]
    bi[s, I_MR] = C0i[0]; bi[s, I_NK] = C0i[1]


# ================================================================ Python en objmode (una vez por evento)
_CTX = {}


def _py_rng2(i, k):
    seed = _CTX['seed']
    return (np.random.default_rng([seed, i, P.ETQ['cuerpo'], k]), np.random.default_rng([seed, i, P.ETQ['hijo'], k]))


def _py_parto_eco(i, k, gpad, spad):
    """E3/E4 del original, las mismas lineas: donante, mutacion del hijo y de sus sombras, banco. + los rng del cuerpo."""
    E_ = _CTX['E_']; ES = _CTX['ES']; seed = _CTX['seed']
    SE = lambda i, etq, k: np.random.default_rng([seed, i, etq, k])
    _dg, _ds = gpad, spad
    if E_['donante'] == 'azar' and ES['banco']:
        _dg, _ds = ES['banco'][int(SE(i, ME.ETQ_DONANTE, k).integers(len(ES['banco'])))]
    _gh, _nm = ME.muta(_dg, SE(i, ME.ETQ_MUT, k), E_['pv'], float(E_['sigma']), E_['lo'], E_['hi'])
    ES['n_mut'] += _nm; ES['n_nac'] += 1
    _rs = SE(i, ME.ETQ_SOMBRA, k); _sh = _ds.copy()
    for _q in range(_sh.shape[0]):
        _sh[_q], _nm = ME.muta(_ds[_q], _rs, E_['pv'], float(E_['sigma']), E_['lo'], E_['hi']); ES['n_mut_s'] += _nm
    if E_['banco']:
        ES['banco'].append((_dg.copy(), _ds.copy()) if E_['donante'] == 'padre' else (_gh.copy(), _sh.copy()))
        if len(ES['banco']) > E_['banco']: ES['banco'].pop(0)
    gcu, ghi = _py_rng2(i, k)
    return gcu, ghi, np.ascontiguousarray(_gh, np.float64), np.ascontiguousarray(_sh, np.float64)


def _py_refunda_eco(i, nac):
    """E9 del original, las mismas lineas: genoma del fundador desde el banco (mutado) o el inicial."""
    E_ = _CTX['E_']; ES = _CTX['ES']; seed = _CTX['seed']
    SE = lambda i, etq, k: np.random.default_rng([seed, i, etq, k])
    if ES['banco']:
        _gb, _sb = ES['banco'][int(SE(i, ME.ETQ_BANCO, nac).integers(len(ES['banco'])))]
        _gf, _nm = ME.muta(_gb, SE(i, ME.ETQ_MUT, nac), E_['pv'], float(E_['sigma']), E_['lo'], E_['hi']); ES['n_mut'] += _nm
        _rs = SE(i, ME.ETQ_SOMBRA, nac); _sf = _sb.copy()
        for _q in range(_sf.shape[0]): _sf[_q], _nm = ME.muta(_sb[_q], _rs, E_['pv'], float(E_['sigma']), E_['lo'], E_['hi'])
        ES['n_banco'] += 1
    else:
        _gf = E_['gs0'][i].copy(); _sf = np.tile(E_['gs0'][i], (int(E_['n_sombra']), 1))
    ES['n_refund'] += 1
    if E_['donante'] == 'azar' and E_['banco']:
        ES['banco'].append((_gf.copy(), _sf.copy()))
        if len(ES['banco']) > E_['banco']: ES['banco'].pop(0)
    return np.ascontiguousarray(_gf, np.float64), np.ascontiguousarray(_sf, np.float64)


# ---------------------------------------------------------------- partos y fundadores (cada objmode en su funcion, sin ramas)
@njit(cache=True)
def _hijo_eco(lin, k, s, s3, G, SH, GL, GI, bi, bf, Wl, el, tr, KW, act, Wp, Wn, Wps, Wns, err, mu, mup, mun, zp, zn, ccode,
              cval, PATM, wbuf, mdot, wi):
    gpad = G[s]; spad = SH[s]
    with objmode(gcu=GENT, ghi=GENT, gh='float64[:]', sh='float64[:, :]'):
        gcu, ghi, gh, sh = _py_parto_eco(lin, k, gpad, spad)
    for g_ in range(G.shape[1]): G[s3, g_] = gh[g_]
    for a in range(SH.shape[1]):
        for g_ in range(SH.shape[2]): SH[s3, a, g_] = sh[a, g_]
    _consts(s3, gh, GI, bi, bf, False)
    GL[s3] = gcu
    _crea(s3, gcu, bi, bf, Wl, el, tr, KW, act, Wp, Wn, Wps, Wns, err, mu, mup, mun, zp, zn, ccode, cval, PATM, wbuf, mdot, wi)
    _nace(s3, ghi, bi, Wl, el, tr, KW, act, ccode, cval, PATM, wbuf, mdot, wi)


@njit(cache=True)
def _hijo_fab(lin, k, s3, GL, C0i, C0f, bi, bf, Wl, el, tr, KW, act, Wp, Wn, Wps, Wns, err, mu, mup, mun, zp, zn, ccode,
              cval, PATM, wbuf, mdot, wi):
    with objmode(gcu=GENT, ghi=GENT):
        gcu, ghi = _py_rng2(lin, k)
    _consts_fab(s3, bi, bf, C0i, C0f)
    GL[s3] = gcu
    _crea(s3, gcu, bi, bf, Wl, el, tr, KW, act, Wp, Wn, Wps, Wns, err, mu, mup, mun, zp, zn, ccode, cval, PATM, wbuf, mdot, wi)
    _nace(s3, ghi, bi, Wl, el, tr, KW, act, ccode, cval, PATM, wbuf, mdot, wi)


@njit(cache=True)
def _genoma_fundador(lin, nac, s2, G, SH, GI, bi, bf):
    with objmode(gf='float64[:]', sf='float64[:, :]'):
        gf, sf = _py_refunda_eco(lin, nac)
    for g_ in range(G.shape[1]): G[s2, g_] = gf[g_]
    for a in range(SH.shape[1]):
        for g_ in range(SH.shape[2]): SH[s2, a, g_] = sf[a, g_]
    _consts(s2, gf, GI, bi, bf, False)


# ================================================================ EL TRAMO: pasos [t0, t1)
@njit(cache=True)
def _tramo(t0, t1, pi, pf, PATM, EFF, RV, GI, C0i, C0f,
           grid, oseq, seqpos, bit, wi, wf,
           bi, bf, Wl, el, tr, KW, act, Wp, Wn, Wps, Wns, err, mu, mup, mun, zp, zn,
           ccode, cval, nck, ncc, rpos, rexp, stt, stk, G, SH,
           li, mord, vis, tfund, tam, tamtot,
           cuer, nuevos, freel, rows, rowsg, tzi, tzf,
           GL, FUND, MUE, rng, rng_pista, lp, xin, xout, dims, adr, wbuf, dummy):
    T = pi[P_T]; L = pi[P_L]; esc = pi[P_ESC]; nobj = pi[P_NOBJ]; inst = pi[P_INST] != 0; racum = pi[P_RACUM] != 0
    tope = pi[P_TOPE]; muestra = pi[P_MUESTRA]; eco = pi[P_ECO] != 0; refunda = pi[P_REFUNDA] != 0; tcorte = pi[P_TCORTE]
    qdiv = pi[P_QDIV]; ppat = pi[P_PPAT]; pmin = pi[P_PMIN]; wcausa = pi[P_WCAUSA]; traza = pi[P_TRAZA] != 0
    mexp = pi[P_MEXP]; mdot = pi[P_MDOT]; mturno = pi[P_MTURNO]; C = pi[P_C]
    costo = pf[Q_COSTO]; costo_a = pf[Q_COSTOA]; olvido = pf[Q_OLV]; r_paso = pf[Q_RPASO]; dote_m = pf[Q_DOTEM]
    fijo = not eco
    S = bi.shape[0]
    x9 = np.empty(9); Wb = np.empty(NKMAX); wb2 = np.empty(NKMAX); kc = np.zeros(NKMAX); w6 = np.empty(6)
    kj = np.empty(6); dist = np.empty(6); rel = np.zeros(6, np.bool_); ep = np.empty(6); c3 = np.empty(K, np.int64)
    olv = np.empty(esc, np.int64)
    for t in range(t0, t1):
        nb = wi[W_NCUER]; total = wi[W_TOTAL]
        need = nb if nb < tope - total else tope - total
        if wi[W_NFREE] < need or wi[W_NROWS] + nb > rows.shape[0] or (traza and wi[W_NTZ] + nb > tzi.shape[0]):
            return ST_CRECE, t
        if t % muestra == 0:
            ix = t // muestra
            for i in range(li.shape[0]): tam[ix, i] = li[i, L_VIVOS]
            tamtot[ix] = total
        for c in range(4): wi[W_COMP0 + c] += wi[W_CNT0 + c]
        wi[W_NSUMA] += wi[W_NOBJ]
        if nb > 1 and mturno == 0:
            orden = rng_pista.permutation(nb)
        else:
            orden = np.arange(nb)
            if nb > 1: rng_pista.permutation(nb)   # CONTROL (debe fallar): turno fijo, mismo consumo de azar
        q = min(t // qdiv, 3)
        # ------------------------------------------------ fase A (actua, mover, morder, resultado)
        for jj in range(nb):
            s = cuer[orden[jj]]; lin = bi[s, I_LIN]; r = GL[s]
            bi[s, I_VOL] = -1
            E = bf[s, F_E]; Ag = bf[s, F_AG]; pos = bi[s, I_POS]
            hambre = _clip(1 - E, 0.0, 1.0)
            dfa = _clip(1 - Ag, 0.0, 1.0)
            na = 1 if dfa > hambre else 0
            if na: hambre = dfa
            cue2 = hambre == 0 and dfa == 0
            nm = na
            bi[s, I_NA] = na; bi[s, I_NM] = nm
            d, k, left = _see(s, pos, t, True, q, L, grid, oseq, rpos, rexp, bi)
            for j in range(6): x9[j] = PATM[k, j] * 1.2
            x9[6] = 1.5 if left else 0.0; x9[7] = 0.0 if left else 1.5; x9[8] = 1.0 if d == 0 else 0.0
            noise = .15 + .5 * hambre
            if mdot == 0:
                V = Wl[s] @ x9
            else:
                V = np.zeros(2)
                for a in range(2):
                    acc = 0.0
                    for j in range(9): acc += Wl[s, a, j] * x9[j]
                    V[a] = acc
            e0, e1 = _exp2(-(V[0] - .8) / noise, -(V[1] - .8) / noise, lp, xin, xout, dims, adr, mexp)
            p0 = 1 / (1 + e0); p1 = 1 / (1 + e1)
            z = r.normal(0, .3, 2)
            u0 = p0 + z[0]; u1 = p1 + z[1]
            m0 = 0.0; m1 = 0.0
            umax = u1 if u1 > u0 else u0
            if umax > .5:
                if u1 > u0: m1 = 1.0
                else: m0 = 1.0
            TAU = bf[s, F_TAU]
            for j in range(9): tr[s, j] = tr[s, j] * .7 + x9[j]
            dm0 = m0 - p0; dm1 = m1 - p1
            for j in range(9):
                el[s, 0, j] = el[s, 0, j] * TAU + dm0 * tr[s, j]
                el[s, 1, j] = el[s, 1, j] * TAU + dm1 * tr[s, j]
            mov = int(m1 - m0)
            pos2 = pos + mov   # (pos + mov) % L con mov en {-1, 0, 1}
            if pos2 < 0: pos2 += L
            elif pos2 >= L: pos2 -= L
            d2, _k2, _l2 = _see(s, pos2, t, False, q, L, grid, oseq, rpos, rexp, bi)
            Rp = .2 if d2 < d else 0.
            bf[s, F_R] = 0.; bf[s, F_RP] = Rp; bf[s, F_HAMB] = hambre
            mordio = False
            kk = grid[pos2]
            wf_ = 0.0; ws_ = 0.0; key = 0
            if kk >= 0:
                _code3(s, kk, KW, act, PATM, ccode, cval, wbuf, mdot, wi)
                for a in range(K): c3[a] = ccode[s, kk, a]
                key = _clave(c3)
                for i in range(NKMAX): kc[i] = 0.0
                for a in range(K): kc[c3[a]] = 1.0
                for i in range(NKMAX): Wb[i] = Wp[s, nm, i] - Wn[s, nm, i]
                wf_ = _dot(Wb, kc, NKMAX, mdot)
                for j in range(6): w6[j] = Wps[s, nm, j] - Wns[s, nm, j]
                ws_ = _dot(w6, PATM[kk], 6, mdot)
                fa9 = _fam(Wp, Wn, s, nm, c3, key, nck, ncc, bi, ppat, pmin)
                wt = wf_ if fa9 else ws_
                bi[s, I_GPN] += 1
                if fa9: bi[s, I_GPA] += 1
                if cue2:
                    o = 1 - na
                    for i in range(NKMAX): wb2[i] = Wp[s, o, i] - Wn[s, o, i]
                    f2 = _dot(wb2, kc, NKMAX, mdot)
                    for j in range(6): w6[j] = Wps[s, o, j] - Wns[s, o, j]
                    sv2 = _dot(w6, PATM[kk], 6, mdot)
                    v2 = f2 if _fam(Wp, Wn, s, o, c3, key, nck, ncc, bi, ppat, pmin) else sv2
                    wt = v2 if v2 < wt else wt   # min(_wt, _vnec(...))
                Vb = bf[s, F_ALPHA] * wt + bf[s, F_HB] * hambre + .5
                pb = 1 / (1 + _exp1(-Vb / .3, lp, xin, xout, dims, adr, mexp))
                mordio = r.random() < pb
                MRs = bi[s, I_MR]
                if MRs != 0 and not mordio:
                    if not _rset(rpos, rexp, bi, s, pos2, t + MRs, t):
                        wi[W_ERR] = ERR_RECH; return ST_ERR, t
            if traza:
                it = wi[W_NTZ]
                tzi[it, 0] = t; tzi[it, 1] = lin; tzi[it, 2] = pos; tzi[it, 3] = mov; tzi[it, 4] = 1 if mordio else 0
                tzf[it, 0] = E; tzf[it, 1] = Ag; wi[W_NTZ] = it + 1
            # --- la pista: mover y morder
            bi[s, I_POS] = pos2
            if kk >= 0:
                vis[lin, kk, q] += 1
                if mordio:
                    v = bf[s, F_E] + EFF[kk, 0]; bf[s, F_E] = 1.5 if 1.5 < v else v
                    v = bf[s, F_AG] + EFF[kk, 1]; bf[s, F_AG] = 1.5 if 1.5 < v else v
                    mord[lin, kk, q] += 1
                    if kk == 1: bi[s, I_TB] = t
                    elif kk == 3: bi[s, I_TD] = t
                    if kk == 1 or kk == 3:
                        sm = mord[lin, kk, 0] + mord[lin, kk, 1] + mord[lin, kk, 2] + mord[lin, kk, 3]
                        if sm > 1: bi[s, I_VOL] = kk
                    _quita(pos2, inst, rng, L, nobj, grid, oseq, seqpos, bit, wi, C)
                    # --- resultado(res): el aprendizaje de la mordida
                    R = RV[kk, na]; bf[s, F_R] = R
                    hit = -1
                    for i in range(bi[s, I_NCN]):
                        if nck[s, i] == key:
                            hit = i; break
                    if hit >= 0: ncc[s, hit] += 1
                    else:
                        nn = bi[s, I_NCN]
                        if nn >= NCOD:
                            wi[W_ERR] = ERR_NCOD; return ST_ERR, t
                        nck[s, nn] = key; ncc[s, nn] = 1; bi[s, I_NCN] = nn + 1
                    _rpop(rpos, rexp, bi, s, pos2)
                    ETA = bf[s, F_ETA]; ETAS = bf[s, F_ETAS]; AV = bf[s, F_AV]; LAM = bf[s, F_LAM]; CLIPS = bf[s, F_CLIPS]
                    EMA = bf[s, F_EMA]; EMAC = bf[s, F_EMAC]; PASO = bf[s, F_PASO]; DELS = bf[s, F_DELS]; DELC = bf[s, F_DELC]
                    Pk = PATM[kk]
                    dlt = R - wf_
                    ds = R - ws_
                    if LAM != 0.0:
                        for j in range(6):
                            mcs = _npmin(Wps[s, nm, j], Wns[s, nm, j]) * (1.0 if Pk[j] > 0 else 0.0)
                            Wps[s, nm, j] = Wps[s, nm, j] - LAM * mcs; Wns[s, nm, j] = Wns[s, nm, j] - LAM * mcs
                    if ds > 0:
                        cc = ETAS * ds
                        for j in range(6): Wps[s, nm, j] = _clip(Wps[s, nm, j] + cc * Pk[j], 0.0, CLIPS)
                    else:
                        cc = ETAS * AV * (-ds)
                        for j in range(6): Wns[s, nm, j] = _clip(Wns[s, nm, j] + cc * Pk[j], 0.0, CLIPS)
                    if LAM != 0.0:
                        for a in range(K):
                            i = c3[a]; mcom = _npmin(Wp[s, nm, i], Wn[s, nm, i])
                            Wp[s, nm, i] = Wp[s, nm, i] - LAM * mcom; Wn[s, nm, i] = Wn[s, nm, i] - LAM * mcom
                    trunca = False
                    if dlt > 0:
                        cc = ETA * dlt
                        for a in range(K):
                            if (Wp[s, nm, c3[a]] + cc) > 3.0: trunca = True
                    else:
                        cc = ETA * AV * (-dlt)
                        for a in range(K):
                            if (Wn[s, nm, c3[a]] + cc) > 3.0: trunca = True
                    if trunca:
                        bi[s, I_NTEC] += 1
                        if bi[s, I_TTEC] < 0: bi[s, I_TTEC] = t
                    # np.clip(W + c*kc, 0, 3) sobre las 90 celdas: fuera del codigo W + (+-0.0) == W (W >= +0.0 siempre)
                    if dlt > 0:
                        cc = ETA * dlt
                        for a in range(K):
                            i = c3[a]; Wp[s, nm, i] = _clip(Wp[s, nm, i] + cc * 1.0, 0.0, 3.0)
                    else:
                        cc = ETA * AV * (-dlt)
                        for a in range(K):
                            i = c3[a]; Wn[s, nm, i] = _clip(Wn[s, nm, i] + cc * 1.0, 0.0, 3.0)
                    if bi[s, I_TCON] < 0:
                        for a in range(K):
                            i = c3[a]
                            if _npmin(Wp[s, nm, i], Wn[s, nm, i]) > 0:
                                bi[s, I_TCON] = t; break
                    for n in range(NNEC):
                        if n == nm: continue
                        Rn = RV[kk, n]
                        for i in range(NKMAX): wb2[i] = Wp[s, n, i] - Wn[s, n, i]
                        wfn = _dot(wb2, kc, NKMAX, mdot)
                        for j in range(6): w6[j] = Wps[s, n, j] - Wns[s, n, j]
                        wsn = _dot(w6, Pk, 6, mdot)
                        dn = Rn - wfn
                        dsn = Rn - wsn
                        if LAM != 0.0:
                            for j in range(6):
                                mn2 = _npmin(Wps[s, n, j], Wns[s, n, j]) * (1.0 if Pk[j] > 0 else 0.0)
                                Wps[s, n, j] = Wps[s, n, j] - LAM * mn2; Wns[s, n, j] = Wns[s, n, j] - LAM * mn2
                        if dsn > 0:
                            cc = ETAS * dsn
                            for j in range(6): Wps[s, n, j] = _clip(Wps[s, n, j] + cc * Pk[j], 0.0, CLIPS)
                        else:
                            cc = ETAS * AV * (-dsn)
                            for j in range(6): Wns[s, n, j] = _clip(Wns[s, n, j] + cc * Pk[j], 0.0, CLIPS)
                        if LAM != 0.0:
                            for a in range(K):
                                i = c3[a]; mc2 = _npmin(Wp[s, n, i], Wn[s, n, i])
                                Wp[s, n, i] = Wp[s, n, i] - LAM * mc2; Wn[s, n, i] = Wn[s, n, i] - LAM * mc2
                        if dn > 0:
                            cc = ETA * dn
                            for a in range(K):
                                i = c3[a]; Wp[s, n, i] = _clip(Wp[s, n, i] + cc * 1.0, 0.0, 3.0)
                        else:
                            cc = ETA * AV * (-dn)
                            for a in range(K):
                                i = c3[a]; Wn[s, n, i] = _clip(Wn[s, n, i] + cc * 1.0, 0.0, 3.0)
                    # plasticidad (v11 div_signo + hija dispersa D, mask_rel == 2)
                    a1 = 1 - EMA; b1 = EMA * abs(dlt)
                    for j in range(6): ep[j] = EMA * Pk[j]
                    for a in range(K):
                        c = c3[a]; err[s, c] = a1 * err[s, c] + b1
                        for j in range(6): mu[s, c, j] = a1 * mu[s, c, j] + ep[j]
                    if R > 0:
                        a2 = 1 - EMAC
                        for j in range(6): ep[j] = EMAC * Pk[j]
                        for a in range(K):
                            c = c3[a]
                            for j in range(6): mup[s, c, j] = a2 * mup[s, c, j] + ep[j]
                            zp[s, c] = a2 * zp[s, c] + EMAC
                    elif R < 0:
                        a2 = 1 - EMAC
                        for j in range(6): ep[j] = EMAC * Pk[j]
                        for a in range(K):
                            c = c3[a]
                            for j in range(6): mun[s, c, j] = a2 * mun[s, c, j] + ep[j]
                            zn[s, c] = a2 * zn[s, c] + EMAC
                    em = err[s, c3[0]]
                    for a in range(1, K):
                        if err[s, c3[a]] > em: em = err[s, c3[a]]
                    if em > bf[s, F_ERRMAX]: bf[s, F_ERRMAX] = em
                    sP = 0.0
                    for j in range(6): sP += Pk[j]
                    umb = 1.0 - DELC
                    for a in range(K):
                        c = c3[a]
                        smu = 0.0
                        for j in range(6): smu += mu[s, c, j]
                        mx = 1e-9 if 1e-9 > smu else smu
                        sc = sP / mx
                        for j in range(6): dist[j] = Pk[j] - (mu[s, c, j] * sc)
                        if zp[s, c] > 1e-6 and zn[s, c] > 1e-6:
                            for j in range(6):
                                mp_ = mup[s, c, j] / zp[s, c]; mn_ = mun[s, c, j] / zn[s, c]
                                rel[j] = (Pk[j] > 0) and ((abs(mp_ - mn_) > DELS) or (_npmin(mp_, mn_) > umb))
                        else:
                            for j in range(6): rel[j] = Pk[j] > 0
                        for j in range(6):
                            kj[j] = _clip(KW[s, c, j] * (1 - 0.05) + PASO * dist[j], 0.0, 5.0) * (1.0 if rel[j] else 0.0)
                        wbc = Wb[c]
                        if wbc * R < 0 and abs(wbc) > 0.2:
                            if _dot(kj, Pk, 6, mdot) > _dot(KW[s, c], Pk, 6, mdot):
                                j2 = -1
                                for i in range(NKMAX):
                                    if not act[s, i]:
                                        j2 = i; break
                                if j2 >= 0:
                                    act[s, j2] = True
                                    for j in range(6): KW[s, j2, j] = kj[j]
                                    if R > 0:
                                        Wp[s, nm, j2] = Wp[s, nm, c]; Wn[s, nm, j2] = 0.; Wp[s, nm, c] = 0.
                                    else:
                                        Wn[s, nm, j2] = Wn[s, nm, c]; Wp[s, nm, j2] = 0.; Wn[s, nm, c] = 0.
                                    for n in range(NNEC):
                                        if n != nm:
                                            Wp[s, n, j2] = Wp[s, n, c]; Wn[s, n, j2] = Wn[s, n, c]
                                    sc2 = smu / sP
                                    for j in range(6): mu[s, j2, j] = Pk[j] * sc2
                                    err[s, c] = 0.0; err[s, j2] = 0.0; bi[s, I_SPL] += 1
                                    ns_ = bi[s, I_NST]
                                    if ns_ >= NST:
                                        wi[W_ERR] = ERR_NST; return ST_ERR, t
                                    stt[s, ns_] = t; stk[s, ns_] = kk; bi[s, I_NST] = ns_ + 1
                                    for j in range(6):
                                        mup[s, j2, j] = mup[s, c, j]; mun[s, j2, j] = mun[s, c, j]
                                    zp[s, j2] = zp[s, c]; zn[s, j2] = zn[s, c]
                                    for p in range(4): cval[s, p] = False
        # ------------------------------------------------ costos
        for jj in range(nb):
            s = cuer[jj]
            bf[s, F_E] -= costo; bf[s, F_AG] -= costo_a
        # ------------------------------------------------ olvido (ERR-98: esc sorteos por paso)
        nolv = 0
        for _o in range(esc):
            if rng.random() < olvido and wi[W_NOBJ] > 0:
                s_ = _bit_sel(bit, C, pi[P_LOG], rng.integers(0, wi[W_NOBJ]))
                dx = seqpos[s_]
                _quita(dx, inst, rng, L, nobj, grid, oseq, seqpos, bit, wi, C)
                olv[nolv] = dx; nolv += 1; wi[W_OLV] += 1
        if not inst:   # P7 quimiostato
            v = wf[0] + r_paso; lim = 1.0 + r_paso
            wf[0] = lim if lim < v else v
            while wf[0] >= 1.0:
                wf[0] -= 1.0
                if wi[W_NOBJ] < nobj:
                    while True:
                        x2 = rng.integers(0, L)
                        if grid[x2] < 0:
                            _pon(x2, rng.integers(0, 4), grid, oseq, seqpos, bit, wi, C); break
                    wi[W_LLEG] += 1
                else: wi[W_PERD] += 1
        # ------------------------------------------------ fase B (fin_paso, muerte/fundador, ventana/parto)
        nnue = 0; muertos = False
        for jj in range(nb):
            j = orden[jj]; s = cuer[j]; lin = bi[s, I_LIN]
            for a in range(nolv): _rpop(rpos, rexp, bi, s, olv[a])
            R = bf[s, F_R]; mxr = R if R > 0 else 0.0
            sc = bf[s, F_ETA] * (1 + 2 * bf[s, F_HAMB]) * (mxr + bf[s, F_RP])
            if sc != 0.0:
                for a in range(2):
                    for b in range(9): Wl[s, a, b] = _clip(Wl[s, a, b] + sc * el[s, a, b], 0.0, 1.5)
            E = bf[s, F_E]; Ag = bf[s, F_AG]
            if E <= 0 or Ag <= 0:
                porE = E <= 0
                if porE: cz = 2 if t - bi[s, I_TB] < wcausa else 0
                else: cz = 3 if t - bi[s, I_TD] < wcausa else 1
                li[lin, L_CZ0 + cz] += 1
                if bi[s, I_VOL] == (1 if porE else 3): li[lin, L_MVOL] += 1
                li[lin, L_DEATHS] += 1; li[lin, L_MN0 if porE else L_MN1] += 1
                ir = wi[W_NROWS]
                rows[ir, 0] = lin; rows[ir, 1] = bi[s, I_K]; rows[ir, 2] = bi[s, I_GEN]; rows[ir, 3] = bi[s, I_PADRE]
                rows[ir, 4] = bi[s, I_TN]; rows[ir, 5] = t; rows[ir, 6] = bi[s, I_HIJ]; rows[ir, 7] = bi[s, I_FUND]
                rows[ir, 8] = cz; rows[ir, 9] = 0
                if eco:
                    for g_ in range(G.shape[1]): rowsg[ir, g_] = G[s, g_]
                wi[W_NROWS] = ir + 1
                li[lin, L_VIVOS] -= 1; wi[W_TOTAL] -= 1; muertos = True
                cuer[j] = -1; GL[s] = dummy
                freel[wi[W_NFREE]] = s; wi[W_NFREE] += 1
                if li[lin, L_VIVOS] > 0 or (eco and ((not refunda) or (tcorte >= 0 and t >= tcorte))): continue
                # P3: extincion -> fundador limpio en el LUGAR del muerto
                li[lin, L_NAC] += 1
                if li[lin, L_NAC] >= 100000:
                    wi[W_ERR] = ERR_NAC; return ST_ERR, t
                li[lin, L_FUND] += 1
                if li[lin, L_NTF] < 200:
                    tfund[lin, li[lin, L_NTF]] = t; li[lin, L_NTF] += 1
                nac = li[lin, L_NAC]
                wi[W_NFREE] -= 1; s2 = freel[wi[W_NFREE]]
                if eco:
                    _genoma_fundador(lin, nac, s2, G, SH, GI, bi, bf)
                else:
                    _consts_fab(s2, bi, bf, C0i, C0f)
                fr = FUND[lin]; GL[s2] = fr
                _crea(s2, fr, bi, bf, Wl, el, tr, KW, act, Wp, Wn, Wps, Wns, err, mu, mup, mun, zp, zn, ccode, cval, PATM,
                      wbuf, mdot, wi)
                bi[s2, I_POS] = MUE[lin].integers(0, L)
                bf[s2, F_E] = dote_m; bf[s2, F_AG] = dote_m
                bi[s2, I_GV] = 0; bi[s2, I_TB] = -10 ** 9; bi[s2, I_TD] = -10 ** 9; bi[s2, I_VOL] = -1; bi[s2, I_HIJ] = 0
                bi[s2, I_FUND] = 1; bi[s2, I_LIN] = lin; bi[s2, I_K] = nac; bi[s2, I_GEN] = 0; bi[s2, I_PADRE] = -1; bi[s2, I_TN] = t
                cuer[j] = s2; s = s2; li[lin, L_VIVOS] = 1; wi[W_TOTAL] += 1
            # ventana de viabilidad (reproduccion)
            ru = bf[s, F_RU]
            if bf[s, F_E] >= ru and bf[s, F_AG] >= ru:
                bi[s, I_GV] += 1; li[lin, L_PV] += 1
            elif not racum:
                bi[s, I_GV] = 0
            if bi[s, I_GV] >= bf[s, F_RX]:
                if wi[W_TOTAL] >= tope:
                    bi[s, I_GV] = 0; li[lin, L_BLOQ] += 1
                    if wi[W_TTOPE] < 0: wi[W_TTOPE] = t
                else:
                    li[lin, L_DESC] += 1; bi[s, I_GV] = 0; bi[s, I_HIJ] += 1
                    dt_ = bf[s, F_DOTE]
                    bf[s, F_E] -= dt_; bf[s, F_AG] -= dt_
                    li[lin, L_NAC] += 1; k = li[lin, L_NAC]
                    if k >= 100000:
                        wi[W_ERR] = ERR_NAC; return ST_ERR, t
                    wi[W_NFREE] -= 1; s3 = freel[wi[W_NFREE]]
                    if eco:
                        _hijo_eco(lin, k, s, s3, G, SH, GL, GI, bi, bf, Wl, el, tr, KW, act, Wp, Wn, Wps, Wns, err, mu, mup, mun,
                                  zp, zn, ccode, cval, PATM, wbuf, mdot, wi)
                    else:
                        _hijo_fab(lin, k, s3, GL, C0i, C0f, bi, bf, Wl, el, tr, KW, act, Wp, Wn, Wps, Wns, err, mu, mup, mun,
                                  zp, zn, ccode, cval, PATM, wbuf, mdot, wi)
                    bi[s3, I_POS] = bi[s, I_POS]; bf[s3, F_E] = dt_; bf[s3, F_AG] = dt_
                    bi[s3, I_GV] = 0; bi[s3, I_TB] = -10 ** 9; bi[s3, I_TD] = -10 ** 9; bi[s3, I_VOL] = -1; bi[s3, I_HIJ] = 0
                    bi[s3, I_FUND] = 0; bi[s3, I_LIN] = lin; bi[s3, I_K] = k; bi[s3, I_GEN] = bi[s, I_GEN] + 1
                    bi[s3, I_PADRE] = bi[s, I_K]; bi[s3, I_TN] = t
                    nuevos[nnue] = s3; nnue += 1
                    li[lin, L_VIVOS] += 1; wi[W_TOTAL] += 1
                    if wi[W_TOTAL] > wi[W_MAXV]: wi[W_MAXV] = wi[W_TOTAL]
        if muertos or nnue > 0:
            m = 0
            for jj in range(nb):
                if cuer[jj] >= 0:
                    cuer[m] = cuer[jj]; m += 1
            for a in range(nnue):
                cuer[m] = nuevos[a]; m += 1
            wi[W_NCUER] = m
        if eco and wi[W_TOTAL] == 0:
            return ST_EXT, t + 1
    return ST_OK, t1


@njit(cache=True)
def _arranque(n, pi, PATM, GI, C0i, C0f, grid, oseq, seqpos, bit, wi, bi, bf, Wl, el, tr, KW, act, Wp, Wn, Wps, Wns, err,
              mu, mup, mun, zp, zn, ccode, cval, G, li, cuer, freel, GL, FUND, rng, rng_pista, wbuf, a_ini):
    """Los cerebros de los fundadores nacen ANTES del primer spawn; E = 1.0, Ag = A_ini; posiciones del rng de la pista."""
    eco = pi[P_ECO] != 0; mdot = pi[P_MDOT]; L = pi[P_L]; S = bi.shape[0]
    for i in range(n):
        if eco: _consts(i, G[i], GI, bi, bf, False)
        else: _consts_fab(i, bi, bf, C0i, C0f)
        GL[i] = FUND[i]
        _crea(i, FUND[i], bi, bf, Wl, el, tr, KW, act, Wp, Wn, Wps, Wns, err, mu, mup, mun, zp, zn, ccode, cval, PATM, wbuf,
              mdot, wi)
        bi[i, I_GV] = 0; bi[i, I_TB] = -10 ** 9; bi[i, I_TD] = -10 ** 9; bi[i, I_VOL] = -1; bi[i, I_HIJ] = 0
        bi[i, I_FUND] = 1; bi[i, I_LIN] = i; bi[i, I_K] = 0; bi[i, I_GEN] = 0; bi[i, I_PADRE] = -1; bi[i, I_TN] = 0
        li[i, L_VIVOS] = 1
        cuer[i] = i
    for i in range(n):
        bf[i, F_E] = 1.0; bf[i, F_AG] = a_ini
    for i in range(n):
        bi[i, I_POS] = rng_pista.integers(0, L)
    _spawn(rng, L, pi[P_NOBJ], grid, oseq, seqpos, bit, wi, pi[P_C])
    m = 0
    for s in range(S - 1, n - 1, -1):
        freel[m] = s; m += 1
    wi[W_NFREE] = m; wi[W_NCUER] = n; wi[W_TOTAL] = n; wi[W_MAXV] = n; wi[W_TTOPE] = -1


# ================================================================ estado en Python
BODY_KEYS = ('bi', 'bf', 'Wl', 'el', 'tr', 'KW', 'act', 'Wp', 'Wn', 'Wps', 'Wns', 'err', 'mu', 'mup', 'mun', 'zp', 'zn',
             'ccode', 'cval', 'nck', 'ncc', 'rpos', 'rexp', 'stt', 'stk', 'G', 'SH')


def _cuerpos_vacios(S, ng, ns):
    return dict(bi=np.zeros((S, NBI), np.int64), bf=np.zeros((S, NBF)), Wl=np.zeros((S, 2, 9)), el=np.zeros((S, 2, 9)),
                tr=np.zeros((S, 9)), KW=np.zeros((S, NKMAX, 6)), act=np.zeros((S, NKMAX), np.bool_),
                Wp=np.zeros((S, NNEC, NKMAX)), Wn=np.zeros((S, NNEC, NKMAX)), Wps=np.zeros((S, NNEC, 6)),
                Wns=np.zeros((S, NNEC, 6)), err=np.zeros((S, NKMAX)), mu=np.zeros((S, NKMAX, 6)), mup=np.zeros((S, NKMAX, 6)),
                mun=np.zeros((S, NKMAX, 6)), zp=np.zeros((S, NKMAX)), zn=np.zeros((S, NKMAX)),
                ccode=np.zeros((S, 4, K), np.int64), cval=np.zeros((S, 4), np.bool_), nck=np.zeros((S, NCOD), np.int64),
                ncc=np.zeros((S, NCOD), np.int64), rpos=np.zeros((S, RC), np.int64), rexp=np.zeros((S, RC), np.int64),
                stt=np.zeros((S, NST), np.int64), stk=np.zeros((S, NST), np.int64), G=np.zeros((S, ng)), SH=np.zeros((S, ns, ng)))


def _crece(st, S2):
    """Mas ranuras (el tramo lo pide AL EMPEZAR un paso: nada del paso esta hecho)."""
    S = st['bi'].shape[0]
    if S2 <= S: return
    nuevo = _cuerpos_vacios(S2, st['G'].shape[1], st['SH'].shape[1])
    for k in BODY_KEYS:
        nuevo[k][:S] = st[k]; st[k] = nuevo[k]
    fl = np.zeros(S2, np.int64); nf = st['wi'][W_NFREE]; fl[:nf] = st['freel'][:nf]
    for s in range(S2 - 1, S - 1, -1): fl[nf] = s; nf += 1
    st['freel'] = fl; st['wi'][W_NFREE] = nf
    c = np.full(S2, -1, np.int64); c[:S] = st['cuer']; st['cuer'] = c
    st['nuevos'] = np.zeros(S2, np.int64)
    for _ in range(S2 - S): st['GL'].append(_DUMMY)


def _crece_buf(st, nb):
    if st['wi'][W_NROWS] + nb > st['rows'].shape[0]:
        m = max(2 * st['rows'].shape[0], st['wi'][W_NROWS] + nb + 16)
        r = np.zeros((m, 10), np.int64); r[:st['rows'].shape[0]] = st['rows']; st['rows'] = r
        g = np.zeros((m, st['rowsg'].shape[1])); g[:st['rowsg'].shape[0]] = st['rowsg']; st['rowsg'] = g
    if st['pi'][P_TRAZA] and st['wi'][W_NTZ] + nb > st['tzi'].shape[0]:
        m = max(2 * st['tzi'].shape[0], st['wi'][W_NTZ] + nb + 16)
        a = np.zeros((m, 5), np.int64); a[:st['tzi'].shape[0]] = st['tzi']; st['tzi'] = a
        b = np.zeros((m, 2)); b[:st['tzf'].shape[0]] = st['tzf']; st['tzf'] = b


def _llama_tramo(st, t0, t1):
    B = st['BEXP']
    return _tramo(t0, t1, st['pi'], st['pf'], st['PATM'], st['EFF'], st['RV'], st['GI'], st['C0i'], st['C0f'],
                  st['grid'], st['oseq'], st['seqpos'], st['bit'], st['wi'], st['wf'],
                  st['bi'], st['bf'], st['Wl'], st['el'], st['tr'], st['KW'], st['act'], st['Wp'], st['Wn'], st['Wps'],
                  st['Wns'], st['err'], st['mu'], st['mup'], st['mun'], st['zp'], st['zn'],
                  st['ccode'], st['cval'], st['nck'], st['ncc'], st['rpos'], st['rexp'], st['stt'], st['stk'], st['G'], st['SH'],
                  st['li'], st['mord'], st['vis'], st['tfund'], st['tam'], st['tamtot'],
                  st['cuer'], st['nuevos'], st['freel'], st['rows'], st['rowsg'], st['tzi'], st['tzf'],
                  st['GL'], st['FUND'], st['MUE'], st['rng'], st['rng_pista'], EXP_LOOP, B[0], B[1], B[3], B[5],
                  st['wbuf'], _DUMMY)


class _Vista:
    """Lo que el codigo Python del original lee de un cuerpo (g, s, lin, gen, k, tn, vivo)."""
    __slots__ = ('g', 's', 'lin', 'gen', 'k', 'tn', 'vivo')

    def __init__(self, st, s):
        self.g = st['G'][s].copy(); self.s = st['SH'][s].copy(); bi = st['bi']
        self.lin = int(bi[s, I_LIN]); self.gen = int(bi[s, I_GEN]); self.k = int(bi[s, I_K]); self.tn = int(bi[s, I_TN])
        self.vivo = True


def _vivos(st):
    return [int(s) for s in st['cuer'][:st['wi'][W_NCUER]]]


# ---- E4 / E9 del original (mismas lineas; cuerpos = las vistas en el orden de la lista de turno)
def _muestra_gen(E_, ES, cuerpos, tt):
    G0 = E_['G0']; R5 = lambda v: [round(float(x), 5) for x in v]
    if ES['banco']:
        Br = R5(np.log(np.array([x[0] for x in ES['banco']]) / G0).mean(0))
        Bs = ([R5(f) for f in np.log(np.array([x[1] for x in ES['banco']]) / G0).mean(0)] if int(E_['n_sombra']) else [])
    else: Br = None; Bs = None
    vv = [b for b in cuerpos if b.vivo]
    if not vv: ES['gen_t'].append([tt, 0, 0, 0, None, None, Br, Bs]); return
    Gr = np.log(np.array([b.g for b in vv]) / G0).mean(0)
    Sr = (np.log(np.array([b.s for b in vv]) / G0).mean(0) if int(E_['n_sombra']) else np.zeros((0, len(G0))))
    ES['gen_t'].append([tt, len(vv), len(set(b.lin for b in vv)), int(max(b.gen for b in vv)),
                        R5(Gr), [R5(f) for f in Sr], Br, Bs])


def _foto_corte(E_, ES, cuerpos, t):
    _vv = [z for z in cuerpos if z.vivo]
    ES['corte'] = dict(t=t + 1, vivos=len(_vv), n_banco=len(ES['banco']),
                       med_vivos=([float(x) for x in np.median(np.array([z.g for z in _vv]), 0)] if _vv else None),
                       med_banco=([float(x) for x in np.median(np.array([x[0] for x in ES['banco']]), 0)] if ES['banco'] else None),
                       med_sombra_banco=([float(x) for x in np.median(np.array([x[1][0] for x in ES['banco']]), 0)]
                                         if ES['banco'] and int(E_['n_sombra']) else None),
                       banco=[[round(float(x), 9) for x in e[0]] for e in ES['banco']])


def _vacia_filas(st, lin_py, E_):
    """Individuos muertos del tramo -> l.ind (o ind_cb) y l.vidas, en el orden del original."""
    nr = int(st['wi'][W_NROWS])
    if not nr: return
    rows = st['rows'][:nr].tolist(); gs = st['rowsg']
    for ir, rw in enumerate(rows):
        lin = rw[0]; L_ = lin_py[lin]
        _row = rw[1:10]
        if len(L_['vidas']) < 100000: L_['vidas'].append(rw[5] - rw[4])
        if E_ is not None and E_['ind_cb'] is not None: E_['ind_cb'](lin, _row, gs[ir].copy())
        else: L_['ind'].append(_row)
    st['wi'][W_NROWS] = 0


def _estado_blob(st, lin_py, ES, tn, firma):
    """E7 del gemelo: TODO el estado en un pickle (los Generators compartidos siguen compartidos). Solo las ranuras VIVAS,
    renumeradas en el orden de la lista de turno (la ranura es interna: no entra en ninguna salida; arnes (C))."""
    viv = np.array(_vivos(st), np.int64); nl = len(viv)
    d = {k: v for k, v in st.items() if k not in ('GL', 'FUND', 'MUE', 'BEXP') and k not in BODY_KEYS}
    for k in BODY_KEYS: d[k] = st[k][viv].copy()
    d['cuer'] = np.arange(nl, dtype=np.int64); d['nuevos'] = np.zeros(nl, np.int64); d['freel'] = np.zeros(nl, np.int64)
    d['wi'] = st['wi'].copy(); d['wi'][W_NFREE] = 0; d['wi'][W_NCUER] = nl
    d['GL'] = [st['GL'][int(s)] for s in viv]; d['FUND'] = list(st['FUND']); d['MUE'] = list(st['MUE'])
    return pickle.dumps(dict(t=tn, firma=firma, st=d, lin_py=lin_py, ES=ES), protocol=pickle.HIGHEST_PROTOCOL)


def _lista_gen(xs):
    L = typed.List.empty_list(GENT)
    for x in xs: L.append(x)
    return L


# ================================================================ la salida() del carro de un cuerpo vivo
def _salida_carro(st, s, mod, ctx):
    """Una instancia REAL del carro con el ctx de ese cuerpo (rng desechable) y el estado del gemelo: su salida()."""
    c = mod.crea(dict(ctx, rng=np.random.default_rng(0)))
    bi = st['bi']; bf = st['bf']
    for nom in ('Wl', 'el', 'tr', 'KW', 'Wp', 'Wn', 'Wps', 'Wns', 'err', 'mu', 'mup', 'mun', 'zp', 'zn'):
        setattr(c, nom, st[nom][s].copy())
    c.activa = st['act'][s].copy()
    c._na = int(bi[s, I_NA]); c._nm = int(bi[s, I_NM]); c.splits = int(bi[s, I_SPL])
    c.err_max = float(bf[s, F_ERRMAX]); c.t_conflicto = (None if bi[s, I_TCON] < 0 else int(bi[s, I_TCON]))
    c.t_techo = (None if bi[s, I_TTEC] < 0 else int(bi[s, I_TTEC])); c.n_techo = int(bi[s, I_NTEC])
    c._gpa = int(bi[s, I_GPA]); c._gpn = int(bi[s, I_GPN])
    c.sin_objetivo = [int(bi[s, I_SO0 + q]) for q in range(4)]
    c.split_t = [(int(st['stt'][s, i]), P.TIPOS[int(st['stk'][s, i])]) for i in range(int(bi[s, I_NST]))]
    c.ncod = {}; c._ord = []
    for i in range(int(bi[s, I_NCN])):
        key = int(st['nck'][s, i]); b = NKMAX + 1
        fs = frozenset([key // (b * b) - 1, (key // b) % b - 1, key % b - 1])
        c.ncod[fs] = int(st['ncc'][s, i]); c._ord.append(fs)
    c._R = float(bf[s, F_R]); c._Rp = float(bf[s, F_RP]); c._hambre = np.float64(bf[s, F_HAMB])
    c._rech = {int(st['rpos'][s, i]): int(st['rexp'][s, i]) for i in range(int(bi[s, I_RN]))}
    c.rng = st['GL'][s]
    return c


# ================================================================ run_solapadas (misma firma que el original)
def run_solapadas(seed, carros, T=100000, pizarra=1, compat=0, rep_acum=0, escala=1, telem=True, diag=1, mundo_n=None,
                  fundador_limpio=0, tope_cuerpos=ME.TOPE_DEF, muestra=ME.MUESTRA, reposicion='fija', r_rep=ME.R_REP, eco=None,
                  _traza=None, _modo=None, _estado_final=None):
    """= motor_eco.run_solapadas BIT A BIT (arnes identidad_eco_rapido.py). Argumentos privados (SOLO el arnes):
    _traza = lista donde se deja la traza (t, linaje, pos, E, Ag, mov, muerde) de cada actua; _modo = dict(exp=1 | dot=1 |
    turno=1) CONTROLES que deben fallar; _estado_final = dict donde se deja el estado del gemelo al terminar."""
    # ---- LAS GUARDIAS DEL ORIGINAL, VERBATIM
    n = len(carros)
    NMX = P.N_MAX if eco is None else ME.ECO_NMAX
    if not 1 <= n <= NMX: raise SystemExit(f"PISTA2: entre 1 y {P.N_MAX} linajes fundadores (hay {n})")
    if compat: raise SystemExit("PISTA2: solapadas=1 no admite compat=1 (el ancla del monolito es de la pista v1)")
    if diag: raise SystemExit("PISTA2: solapadas=1 exige diag=0 (el diagnostico de v1 no se porto; declarado)")
    if rep_acum not in (0, 1): raise SystemExit("PISTA2: rep_acum es 0 o 1")
    if not (isinstance(tope_cuerpos, int) and tope_cuerpos >= n): raise SystemExit("PISTA2: tope_cuerpos entero >= n")
    if reposicion not in ('inmediata', 'fija'): raise SystemExit("PISTA2: reposicion 'inmediata' (v1) o 'fija' (quimiostato)")
    inst = reposicion == 'inmediata'
    CF = P.cfg_fabrica(); kw = CF['kw']; VAL_VIVO, EFECTO = CF['VAL_VIVO'], CF['EFECTO']
    EMX = P.N_MAX if eco is None else ME.ECO_ESC_MAX
    if mundo_n is not None and (int(mundo_n) != mundo_n or not 1 <= mundo_n <= EMX):
        raise SystemExit(f"PISTA2: mundo_n entre 1 y {P.N_MAX}")
    esc = int(mundo_n) if mundo_n is not None else (n if escala else 1)
    L = CF['L'] * esc
    M = dict(nobj=kw['nobj'] * esc, costo=kw['costo'], costo_a=kw['costo_a'], rep_X=kw['rep_X'],
             rep_umbral=kw['rep_umbral'], dote=kw['dote'], olvido=P.OLVIDO)
    mods = [(c, (P.carga_carro(c) if eco is None else ME.carga_eco(c))) if isinstance(c, str) else c for c in carros]
    E_ = None if eco is None else ME._eco_cfg(eco, CF, n)
    # ---- LO QUE ESTE GEMELO NO COMPILA (aborta en vez de callar)
    for p_, h_ in SHA.items():
        if _h16(p_) != h_:
            raise SystemExit(f"motor_eco_rapido: {os.path.relpath(p_, RAIZ)} cambio (sha {_h16(p_)} != {h_}); rehacer el gemelo y su arnes")
    for e_, m_ in mods:
        f_ = os.path.basename(getattr(m_, '__file__', '') or '')
        if f_ not in CEREBROS or _h16(m_.__file__) != CEREBROS[f_]:
            raise ValueError(f"motor_eco_rapido: solo compila el cerebro FABRICA / FABRICA_ECO (carro {e_!r}: {f_ or m_}); usa motor_eco")
    if (CF['NKMAX'], CF['K'], kw['n_nec'], tuple(P.TIPOS)) != (NKMAX, K, NNEC, ('A', 'B', 'C', 'D')):
        raise ValueError('motor_eco_rapido: NKMAX/K/n_nec/TIPOS de fabrica distintos de los compilados')
    if E_ is not None and E_['estado'] is not None and not isinstance(E_['estado'], (bytes, bytearray)):
        raise ValueError('motor_eco_rapido: estado debe ser el blob (bytes) de un checkpoint del gemelo')
    modo = dict(exp=0, dot=0, turno=0); modo.update(_modo or {})

    ES = dict(t_ext=None, gen_t=[], n_mut=0, n_mut_s=0, n_nac=0, banco=[], n_banco=0, n_refund=0, corte=None)
    etiquetas = [e for e, _ in mods]
    ids = [(e if etiquetas.count(e) == 1 else f"{e}#{i}") for i, e in enumerate(etiquetas)]
    SS = lambda i, etq, k: np.random.default_rng([seed, i, P.ETQ[etq], k])
    firma = (seed, T, n, ids, L, M['nobj'], reposicion, float(r_rep), tope_cuerpos, muestra, FIRMA_GEMELO)

    def ctx_de(i, ident, g=None):
        _d = dict(id=ident, indice=i, n_linajes=n, T=T, L=L, PAT={k: v.copy() for k, v in CF['PAT'].items()},
                  rng=None, dote=M['dote'], rep_umbral=M['rep_umbral'], costo=M['costo'], costo_a=M['costo_a'],
                  rep_X=M['rep_X'], cupo=P.CUPO, ancho=P.ANCHO, fabrica=P.cfg_fabrica())
        return _d if g is None else ME.ctx_genoma(_d, g)

    _vistos = set()
    for i, (e, mod) in enumerate(mods):   # RAMAS del carro (aborta igual que el original si no son las portadas; no dependen del genoma)
        if id(mod) in _vistos: continue
        _vistos.add(id(mod))
        mod.crea(dict(ctx_de(i, ids[i], (None if E_ is None else E_['gs0'][i])), rng=np.random.default_rng(0)))

    # ---- constantes (H-4: todo sale de cfg_fabrica)
    GI = np.array([ME.NOMBRES.index(x) for x in ('eta', 'tau_e', 'alpha', 'hambre_boca', 'aversion', 'ema', 'paso', 'lam',
                                                  'memoria_rechazo', 'eta_s', 'clip_s', 'del_s', 'del_c', 'ema_c', 'NK',
                                                  'dote', 'rep_umbral', 'rep_X')], np.int64)
    if [ME.NOMBRES[j] for j in range(len(ME.GENES)) if ME.GENES[j][2]] != ['memoria_rechazo', 'NK', 'rep_X']:
        raise ValueError('motor_eco_rapido: los genes enteros no son memoria_rechazo, NK, rep_X')
    PATM = np.array([CF['PAT'][x] for x in P.TIPOS], float)
    EFF = np.array([EFECTO[VAL_VIVO[x]] for x in P.TIPOS], float)
    RV = np.array([[(1.0 if v > 0 else (-3.0 if v < 0 else 0.0)) for v in EFECTO[VAL_VIVO[x]]] for x in P.TIPOS], float)
    C0f = np.zeros(NBF)
    for j_, nom in ((F_ETA, 'eta'), (F_TAU, 'tau_e'), (F_ALPHA, 'alpha'), (F_HB, 'hambre_boca'), (F_AV, 'aversion'),
                    (F_EMA, 'ema'), (F_PASO, 'paso'), (F_LAM, 'lam'), (F_ETAS, 'eta_s'), (F_CLIPS, 'clip_s'),
                    (F_DELS, 'del_s'), (F_DELC, 'del_c'), (F_EMAC, 'ema_c')):
        C0f[j_] = float(kw[nom])
    C0f[F_DOTE] = float(M['dote']); C0f[F_RU] = float(M['rep_umbral']); C0f[F_RX] = float(M['rep_X'])
    C0i = np.array([int(kw['memoria_rechazo']), int(CF['NK'])], np.int64)
    ng = len(ME.GENES); ns = 0 if E_ is None else int(E_['n_sombra'])
    nobj = M['nobj']; C = 1024
    while C < 4 * nobj + 8: C *= 2
    LOG = 1
    while LOG * 2 <= C: LOG *= 2
    pi = np.zeros(NPI, np.int64)
    pi[P_T] = T; pi[P_L] = L; pi[P_ESC] = esc; pi[P_NOBJ] = nobj; pi[P_INST] = int(inst); pi[P_RACUM] = int(rep_acum)
    pi[P_TOPE] = tope_cuerpos; pi[P_MUESTRA] = muestra; pi[P_ECO] = int(E_ is not None)
    pi[P_REFUNDA] = int(E_['refunda']) if E_ is not None else 1
    pi[P_TCORTE] = (-1 if (E_ is None or E_['t_corte'] is None) else int(E_['t_corte'])); pi[P_N] = n; pi[P_QDIV] = T // 4
    pi[P_PPAT] = int(kw['puerta_pat']); pi[P_PMIN] = int(kw['pat_min']); pi[P_WCAUSA] = int(P.W_CAUSA)
    pi[P_TRAZA] = int(_traza is not None); pi[P_MEXP] = int(modo['exp']); pi[P_MDOT] = int(modo['dot'])
    pi[P_MTURNO] = int(modo['turno']); pi[P_C] = C; pi[P_LOG] = LOG
    pf = np.zeros(NPF)
    pf[Q_COSTO] = M['costo']; pf[Q_COSTOA] = M['costo_a']; pf[Q_OLV] = M['olvido']; pf[Q_RPASO] = float(r_rep) * esc
    pf[Q_DOTEM] = M['dote']; pf[Q_AINI] = kw['A_ini']
    lin_py = [dict(ind=[], vidas=[]) for _ in range(n)]
    nmu = (T + muestra - 1) // muestra + 1

    if E_ is not None and E_['estado'] is not None:   # E7: reanudar (blob del GEMELO)
        blob = pickle.loads(E_['estado'])
        if not isinstance(blob, dict) or blob.get('firma') != firma:
            raise SystemExit('ECO: el checkpoint es de otra corrida (firma distinta)')
        st = blob['st']; lin_py = blob['lin_py']; ES.clear(); ES.update(blob['ES'])
        st['GL'] = _lista_gen(st['GL']); st['FUND'] = _lista_gen(st['FUND']); st['MUE'] = _lista_gen(st['MUE'])
        st['pi'][P_TRAZA] = int(_traza is not None); st['pi'][P_MEXP] = int(modo['exp']); st['pi'][P_MDOT] = int(modo['dot'])
        st['pi'][P_MTURNO] = int(modo['turno'])
        _t0 = int(blob['t'])
    else:
        S0 = min(tope_cuerpos, max(64, 2 * n))
        st = dict(pi=pi, pf=pf, PATM=PATM, EFF=EFF, RV=RV, GI=GI, C0i=C0i, C0f=C0f,
                  grid=np.full(L, -1, np.int64), oseq=np.zeros(L, np.int64), seqpos=np.full(C, -1, np.int64),
                  bit=np.zeros(C + 1, np.int64), wi=np.zeros(NWI, np.int64), wf=np.zeros(1),
                  li=np.zeros((n, NLI), np.int64), mord=np.zeros((n, 4, 4), np.int64), vis=np.zeros((n, 4, 4), np.int64),
                  tfund=np.zeros((n, 200), np.int64), tam=np.zeros((nmu, n), np.int64), tamtot=np.zeros(nmu, np.int64),
                  cuer=np.full(S0, -1, np.int64), nuevos=np.zeros(S0, np.int64), freel=np.zeros(S0, np.int64),
                  rows=np.zeros((max(64, 2 * n), 10), np.int64), rowsg=np.zeros((max(64, 2 * n), ng)),
                  tzi=np.zeros((64 if _traza is not None else 1, 5), np.int64), tzf=np.zeros((64 if _traza is not None else 1, 2)),
                  wbuf=np.zeros(NKMAX))
        st.update(_cuerpos_vacios(S0, ng, ns))
        st['GL'] = _lista_gen([_DUMMY] * S0)
        st['FUND'] = _lista_gen([SS(i, 'cuerpo', 0) for i in range(n)]); st['MUE'] = _lista_gen([SS(i, 'muerte', 0) for i in range(n)])
        st['rng'] = SS(0, 'mundo', 0); st['rng_pista'] = SS(0, 'pista', 0)
        if E_ is not None:
            for i in range(n):
                st['G'][i] = E_['gs0'][i]; st['SH'][i] = np.tile(E_['gs0'][i], (ns, 1))
        _arranque(n, st['pi'], PATM, GI, C0i, C0f, st['grid'], st['oseq'], st['seqpos'], st['bit'], st['wi'], st['bi'], st['bf'],
                  st['Wl'], st['el'], st['tr'], st['KW'], st['act'], st['Wp'], st['Wn'], st['Wps'], st['Wns'], st['err'],
                  st['mu'], st['mup'], st['mun'], st['zp'], st['zn'], st['ccode'], st['cval'], st['G'], st['li'], st['cuer'],
                  st['freel'], st['GL'], st['FUND'], st['rng'], st['rng_pista'], st['wbuf'], float(kw['A_ini']))
        if E_ is not None and E_['banco']:   # E9: el banco arranca con los fundadores
            ES['banco'] = [(st['G'][i].copy(), st['SH'][i].copy()) for i in range(n)][-int(E_['banco']):]
        _t0 = 0
    st['BEXP'] = _bufs_exp()
    _CTX.clear(); _CTX.update(seed=seed, E_=E_, ES=ES)

    # ---- los tramos: el nucleo corre entre eventos de Python (muestra de genes, corte, checkpoint, fin)
    eventos = []
    if E_ is not None:
        if E_['cada_gen']: eventos.append(int(E_['cada_gen']))
        if E_['ckpt_cada']: eventos.append(int(E_['ckpt_cada']))
    tc_ = None if E_ is None else E_['t_corte']
    t = _t0
    while t < T:
        t1 = T
        for ev in eventos: t1 = min(t1, (t // ev + 1) * ev)
        if tc_ is not None and t < tc_: t1 = min(t1, int(tc_))
        est, tnow = _llama_tramo(st, t, t1)
        if est == ST_CRECE:   # al EMPEZAR el paso tnow (nada de ese paso esta hecho): mas ranuras y se sigue desde tnow
            t = int(tnow)
            nb = int(st['wi'][W_NCUER]); tot = int(st['wi'][W_TOTAL]); need = min(nb, tope_cuerpos - tot)
            S = st['bi'].shape[0]
            if st['wi'][W_NFREE] < need: _crece(st, min(tope_cuerpos, max(2 * S, S + need)))
            _crece_buf(st, nb)
            continue
        if est == ST_ERR:
            raise SystemExit(ERR_MSG[int(st['wi'][W_ERR])])
        _vacia_filas(st, lin_py, E_)
        if _traza is not None:
            nt = int(st['wi'][W_NTZ])
            _traza.extend(zip(st['tzi'][:nt, 0].tolist(), st['tzi'][:nt, 1].tolist(), st['tzi'][:nt, 2].tolist(),
                              st['tzf'][:nt, 0].tolist(), st['tzf'][:nt, 1].tolist(), st['tzi'][:nt, 3].tolist(),
                              st['tzi'][:nt, 4].tolist()))
            st['wi'][W_NTZ] = 0
        t = int(tnow)
        if E_ is not None:
            cuerpos = None
            if (E_['cada_gen'] and t % E_['cada_gen'] == 0) or (E_['t_corte'] is not None and t == E_['t_corte']):
                cuerpos = [_Vista(st, s) for s in _vivos(st)]
            if E_['cada_gen'] and t % E_['cada_gen'] == 0: _muestra_gen(E_, ES, cuerpos, t)
            if E_['t_corte'] is not None and t == E_['t_corte']: _foto_corte(E_, ES, cuerpos, t - 1)
            if est == ST_EXT:
                ES['t_ext'] = t; break
            if E_['ckpt_cada'] and t % E_['ckpt_cada'] == 0 and t < T: E_['ckpt_fn'](t, _estado_blob(st, lin_py, ES, t, firma))

    # ---- salida (ERR-96: fisica ARRIBA, carro en d['carro']) con las mismas expresiones del original
    wi = st['wi']; li = st['li']
    nsamp = (t - 1) // muestra + 1 if t > 0 else 0
    tam = st['tam'][:nsamp]; total = int(wi[W_TOTAL])
    vivos = _vivos(st)
    out = []
    for i in range(n):
        L_ = lin_py[i]
        campo = ME.VOL_DECL.get(etiquetas[i])
        vl = [s for s in vivos if st['bi'][s, I_LIN] == i]
        for s in vl:
            b = st['bi'][s]
            _row = [int(b[I_K]), int(b[I_GEN]), int(b[I_PADRE]), int(b[I_TN]), -1, int(b[I_HIJ]), int(b[I_FUND]), -1, 0]
            if E_ is not None and E_['ind_cb'] is not None: E_['ind_cb'](i, _row, st['G'][s].copy())
            else: L_['ind'].append(_row)
        car = {}
        if vl:
            s0 = vl[0]
            car = dict(_salida_carro(st, s0, mods[i][1], ctx_de(i, ids[i], (None if E_ is None else st['G'][s0].copy()))).salida())
        lv = li[i]
        d = dict(mord={x: [int(v) for v in st['mord'][i, j_]] for j_, x in enumerate(P.TIPOS)},
                 vis={x: [int(v) for v in st['vis'][i, j_]] for j_, x in enumerate(P.TIPOS)},
                 deaths=int(lv[L_DEATHS]), muertes_nec=[int(lv[L_MN0]), int(lv[L_MN1])], descendientes=int(lv[L_DESC]),
                 nacimientos=int(lv[L_DESC]), fundadores=int(lv[L_FUND]), t_fund=[int(x) for x in st['tfund'][i, :lv[L_NTF]]],
                 vetos=0, bloqueados=int(lv[L_BLOQ]), pasos_viables=int(lv[L_PV]), vidas_muertos=list(L_['vidas']),
                 vivos_final=int(lv[L_VIVOS]), tam=[int(x) for x in tam[:, i]] + [int(lv[L_VIVOS])],
                 individuos=L_['ind'], T_efectivo=T, dote=M['dote'], muerte_real=1)
        d['_carrera'] = dict(id=ids[i], indice=i, etiqueta=etiquetas[i],
                             causas={x: int(lv[L_CZ0 + j_]) for j_, x in enumerate(ME.CAUSAS)}, escrituras=0, escr=[],
                             muertes_vol=int(lv[L_MVOL]), muertes_vol_decl=0, vol_decl_vivos_T=0, vol_decl_campo=campo)
        d['carro'] = car
        out.append(d)
    comp = {x: int(wi[W_COMP0 + j_]) for j_, x in enumerate(P.TIPOS)}
    res = dict(linajes=out, pizarra_log=[],
               pista=dict(seed=seed, T=T, n=n, ids=ids, solapadas=1, compat=0, pizarra=int(pizarra), rep_acum=int(rep_acum),
                          escala=int(escala), L=L, nobj=M['nobj'], olvidos=int(wi[W_OLV]), mundo_n=mundo_n,
                          fundador_limpio='siempre (P3)', reposicion=reposicion, r_paso=(None if inst else float(r_rep) * esc),
                          llegadas=int(wi[W_LLEG]), llegadas_perdidas=int(wi[W_PERD]), pisos=int(wi[W_PISOS]),
                          tope_cuerpos=tope_cuerpos, t_tope=(None if wi[W_TTOPE] < 0 else int(wi[W_TTOPE])),
                          max_vivos=int(wi[W_MAXV]), bloqueados=int(li[:, L_BLOQ].sum()), muestra=muestra,
                          tam_total=[int(x) for x in st['tamtot'][:nsamp]] + [total],
                          comp_mundo={x: round(comp[x] / T, 4) for x in P.TIPOS}, nobj_medio=round(int(wi[W_NSUMA]) / T, 3),
                          nobj_final=int(wi[W_NOBJ]), escrituras_descartadas=0, pizarra_n=0, pizarra_final=[],
                          rng_mundo_estado=P._estado(st['rng'])))
    if E_ is not None:
        res['eco'] = dict(
            genes=list(ME.NOMBRES), G0=[float(x) for x in E_['G0']], lo=[float(x) for x in E_['lo']], hi=[float(x) for x in E_['hi']],
            refunda=int(E_['refunda']), t_corte=E_['t_corte'], banco=int(E_['banco']), donante=E_['donante'], n_banco=ES['n_banco'],
            n_refund=ES['n_refund'], corte=ES['corte'], mutables=[x for x, q in zip(ME.NOMBRES, E_['pv']) if q > 0],
            p_mut=float(E_['p_mut']), sigma=float(E_['sigma']), n_sombra=int(E_['n_sombra']),
            cada_gen=int(E_['cada_gen']), t_ext=ES['t_ext'], n_nac=ES['n_nac'], n_mut=ES['n_mut'], n_mut_s=ES['n_mut_s'],
            gen_t=ES['gen_t'], vivos_final=[[int(st['bi'][s, I_LIN]), int(st['bi'][s, I_K]), int(st['bi'][s, I_GEN]),
                                             int(st['bi'][s, I_TN])] + [round(float(x), 6) for x in st['G'][s]] for s in vivos])
    if _estado_final is not None:
        _estado_final.update(st=st, vivos=vivos, ids=ids, mods=mods, ctx_de=ctx_de, t=t)
    return res
