"""
organismo_f9 RAPIDO — gemelo COMPILADO (numba) de experimentos/nivel09_cuerpo_nuevo/organismo_f9.py
(3a821884394d66c9; cadena organismo_alma2 4fd616aeaf535e61 <- organismo_alma 7c09cec391daa879 <-
organismo_vivo_h1 9e99ff87b5e2db1e <- organismo_vivo_rep2 96feb4918dc5d694 <- organismo_vivo_rep
aa823d56c2d4213c <- organismo_vivo 20c0961c79de8825 <- TRONCO CONGELADO organismo_v14 v14.1 feefc88b1fd8d434).

NO es un organismo nuevo: misma regla, mismo flujo de azar, mismas salidas (TODAS las claves). Existe para que
el bloque 2 de la fase 9 quepa en el dia. Solo vale si es BIT A BIT identico: arnes identidad_f9_rapido.py
(regla 9 de EQUIPO.md: si no es identico, no se usa para confirmar).

Partida: organismo/organismo_v14c_rapido.py (gemelo de v14c, 196/196) — de el vienen _code, _clave, _pos_cod,
_ev, _famil, _spawn, _borrar, _idx_en, _see y el esqueleto del paso. Sobre el se anaden, en el MISMO orden en
que los inyectan sus constructores: MUNDO VIVO (n_nec, cuatro estimulos, dS vectorial, CUELLO/CUELLO_MIN),
REPRODUCCION (ventana de viabilidad), REP2 (vidas, regalo del renacer), H-1 (muerte real, cola de dotes,
fundadores, _nace con el rng del hijo), ALMA (nodo central, curitas, exposicion sin consecuencia al nacer),
ALMA2 (menu, nodo barajado) y las CUATRO PERILLAS DE LA FASE 9 (nodo_rel, con_desde, rep_acum, f9).

QUE SE DELEGA EN NUMPY / PYTHON Y POR QUE (regla 9)
  - `Generator`: el del mundo se crea en Python y se pasa al bucle; los rng PROPIOS del control de acceso
    (870000+) y del barajado del nodo (860000+) tambien. El rng del HIJO (700000+1000000*seed+k) no se puede
    construir en nopython (numba no tiene np.random.default_rng): se construye en un bloque `objmode` en el
    momento del parto (una vez por nacimiento, no por paso).
  - `argsort` con EMPATES en la frontera del top-K (codigo de Kenyon): a NumPy por `objmode` (heredado).
  - `Generator.choice(n, size, replace=False)` (nodo_rel=2, CONTROL DE ACCESO): numba no la implementa -> a
    NumPy por `objmode`, una vez por nacimiento conectado. `Generator.permutation` si esta implementada y da
    el mismo flujo, asi que el barajado del nodo (REL_BAR) NO sale del codigo compilado.
  - el ALMA es un invocable de Python: se llama por `objmode` en cada muerte (y solo en cada muerte), con el
    resumen construido en Python exactamente como en el original; la curita vuelve como indice y el codigo
    compilado la aplica. La validacion del MENU CERRADO se hace en Python, con los mismos mensajes.
  - `np.lexsort` de la seleccion por relevancia NO se delega: sus claves son (-puntaje, -indice) con indices
    UNICOS, es decir un orden TOTAL, y el original solo usa el primer elemento (relevancia viva) o los
    primeros nodo_lee (relevancia fija). Se reproduce con una seleccion por maximo (empate -> indice mayor =
    mas reciente), que es exacta y no depende del algoritmo de ordenacion.
  - sumas de n >= 8: el unico sitio nuevo donde podian aparecer es el puntaje de relevancia
    `((Wps[N]-Wns[N])*P).sum(1)`, que suma 6 elementos: NumPy no usa suma por pares con n < 8 (suma de
    izquierda a derecha desde 0.0) y el bucle elemental la reproduce (comprobado). Los productos escalares
    (`@`) se dejan como `@`/`np.dot` para que numba llame al MISMO BLAS que NumPy.
  - ninguna funcion es recursiva (cache=True; regla 9: la recursion con cache segmenta el proceso que lee el
    cache y mataria a cada worker de un Pool).

EL BLOQUE 2 EN EL MISMO BUCLE (como organismo_f9c.py hace con organismo_f9.py): la firma lleva ademas
nodo_via, nodo_or, sesgo_fijo y f9c, APAGADAS por defecto. Con las cuatro apagadas esto es el gemelo de
organismo_f9.py y nada mas (arnes identidad_f9_rapido.py, 138/138); con ellas encendidas es el gemelo de
organismo_f9c.py (9dd1fb91ecec35ae), al que se llega por experimentos/nivel09_cuerpo_nuevo_b2/
organismo_f9c_rapido.py, que solo cambia los defaults y NO copia el bucle (una sola cache de numba, una sola
copia del kernel que pueda divergir; es lo que organismo_v14_rapido.py hace con organismo_v14c_rapido.py).

FUERA DE ALCANCE (el gemelo ABORTA en vez de callar; el original si los admite):
  log_cada, nec_shuf, el predictor de dS (eta_pred / k_sorp), la tercera necesidad (n_nec=3 / rep_nec),
  hereda='M1+pares' y hereda='baraja', e `invertir_en`/`nuevo` con vivo=1. Nada de eso lo usa corre_f9.py.

Arnes: identidad_f9_rapido.py. NO editar a mano sin volver a correr el arnes.
"""
import numpy as np
import numba
from numba import njit, objmode

L=40; NK=30; NKMAX=90; K=3
NCODMAX=4096
PAT={'A':np.array([1,1,0,1,0,0.]),'B':np.array([1,0,1,0,1,0.]),'C':np.array([0,1,1,0,0,1.]),'D':np.array([0,0,1,0,1,1.])}
R_VAL={'comida':1.0,'veneno':-3.0}; E_VAL={'comida':+0.8,'veneno':-0.4}
NEC=('hambre','sed')
VAL_VIVO={'A':'comida','B':'veneno','C':'agua','D':'sal'}
EFECTO={'comida':(+0.8,0.0),'veneno':(-0.4,0.0),'agua':(0.0,+0.8),'sal':(0.0,-0.4)}
NOMBRES=['A','B','C','D']
VALENCIAS=['comida','veneno','agua','sal']
HEREDA=['nada','M1','M1+pares','baraja']
PATM=np.array([PAT[k] for k in NOMBRES])
GENT=numba.typeof(np.random.default_rng(1))   # tipo numba del Generator (para los bloques objmode)

# --- contexto de Python que leen los bloques `objmode` (el alma es un invocable: no entra en nopython).
#     Un proceso, una corrida a la vez (los agentes no corren Pool; regla 3). run() lo fija antes del bucle.
_CTX = {'alma': None, 'menu': 'abcdef', 'motivo': '', 'cur': []}


def _alma_llama(cuerpo, t, causa_idx, edad, hijos, fundador, conectado, nodo_n, dote, rep_umbral, hereda_idx,
                ex_t, ex_k, ex_n, ex_m, mo_t, mo_k, mo_n, mo_r, desc, muertes, fundadores, nodo_baraja):
    """El resumen del original, construido en Python, y la validacion del MENU CERRADO con sus mensajes."""
    causa = None if causa_idx < 0 else ('energia' if causa_idx == 0 else 'agua')
    menu = _CTX['menu']
    _res = dict(cuerpo=int(cuerpo), t=int(t), causa=causa, edad=int(edad), hijos=int(hijos), fundador=int(fundador),
                conectado=int(conectado), nodo_n=int(nodo_n), dote=round(float(dote), 4),
                rep_umbral=round(float(rep_umbral), 4), hereda=HEREDA[int(hereda_idx)],
                exposiciones=[[int(a), NOMBRES[int(b)], int(c), int(d)] for a, b, c, d in
                              zip(ex_t[-20:], ex_k[-20:], ex_n[-20:], ex_m[-20:])],
                mordidas=[[int(a), NOMBRES[int(b)], int(c), float(d)] for a, b, c, d in
                          zip(mo_t[-20:], mo_k[-20:], mo_n[-20:], mo_r[-20:])],
                descendientes=int(desc), muertes=int(muertes), fundadores=int(fundadores),
                R0=round(int(desc) / max(int(muertes), 1), 4), menu=[_z1 for _z1 in menu],
                nodo_baraja=int(nodo_baraja))
    _r9 = _CTX['alma'](_res) or {}
    _c9 = _r9.get('curita', 'f')
    if _c9 not in ('a', 'b', 'c', 'd', 'e', 'f'):
        raise SystemExit(f'ALMA: curita {_c9!r} fuera del MENU CERRADO (a,b,c,d,e,f)')
    if _c9 not in menu:
        raise SystemExit(f'ALMA2: curita {_c9!r} fuera del menu OFRECIDO {menu!r} (el runner es quien tolera y registra (f))')
    _CTX['motivo'] = str(_r9.get('motivo', ''))[:240]
    return 'abcdef'.index(_c9)


def _reg_curita(nmu, c9, dote, rep_umbral, hereda_idx, con, nodo_n, causa_idx, edad, hijos):
    """La fila de `curitas` del original (lleva el motivo, que es texto: se acumula en Python)."""
    causa = None if causa_idx < 0 else ('energia' if causa_idx == 0 else 'agua')
    _CTX['cur'].append([int(nmu), 'abcdef'[int(c9)], _CTX['motivo'], round(float(dote), 4),
                        round(float(rep_umbral), 4), HEREDA[int(hereda_idx)], int(con), int(nodo_n), causa,
                        int(edad), int(hijos)])
    return 0


# ------------------------------------------------------------------ utilidades compiladas (de v14c_rapido)
@njit(cache=True)
def _code(KW, activa, P):
    """Codigo de Kenyon como vector 0/1: top-K de KW@P entre las celdas activas. Con empate en la frontera manda NumPy."""
    v = KW @ P
    w = np.empty(NKMAX)
    for i in range(NKMAX):
        w[i] = v[i] if activa[i] else -1e9
    idx = np.argsort(w)
    if w[idx[NKMAX - K]] == w[idx[NKMAX - K - 1]]:
        with objmode(idx='int64[:]'):
            idx = np.argsort(w)
    out = np.zeros(NKMAX)
    for i in range(NKMAX - K, NKMAX):
        out[idx[i]] = 1.0
    return out


@njit(cache=True)
def _clave(kc):
    """B: frozenset(np.flatnonzero(kc)) -> entero unico (indices ascendentes en base NKMAX+1)."""
    key = 0
    for i in range(NKMAX):
        if kc[i] > 0:
            key = key * (NKMAX + 1) + (i + 1)
    return key


@njit(cache=True)
def _pos_cod(ncod_key, n_cod, key):
    for i in range(n_cod):
        if ncod_key[i] == key:
            return i
    return -1


@njit(cache=True)
def _ev(ncod_key, ncod_cnt, n_cod, key, pat_shuf):
    i = _pos_cod(ncod_key, n_cod, key)
    if pat_shuf == 0:
        if i < 0:
            return 0
        return ncod_cnt[i]
    if i < 0 or n_cod < 2:
        return 0
    return ncod_cnt[(i + 1) % n_cod]


@njit(cache=True)
def _famil(Wb, kc, puerta, puerta_pat, pat_min, pat_shuf, ncod_key, ncod_cnt, n_cod):
    ncons = 0
    for i in range(NKMAX):
        if kc[i] > 0 and abs(Wb[i]) > 0.2:
            ncons += 1
    if puerta_pat != 0:
        return _ev(ncod_key, ncod_cnt, n_cod, _clave(kc), pat_shuf) >= puerta_pat and ncons >= pat_min
    return ncons >= puerta


@njit(cache=True)
def _spawn(rng, opos, otip, nobjs, nobj, tipos, ntipos):
    while nobjs < nobj:
        x = rng.integers(0, L)
        dup = False
        for i in range(nobjs):
            if opos[i] == x:
                dup = True; break
        if not dup:
            opos[nobjs] = x; otip[nobjs] = tipos[rng.integers(0, ntipos)]; nobjs += 1
    return nobjs


@njit(cache=True)
def _borrar(opos, otip, nobjs, x):
    """del objs[x] conservando el orden de insercion del dict del original."""
    j = -1
    for i in range(nobjs):
        if opos[i] == x:
            j = i; break
    for i in range(j, nobjs - 1):
        opos[i] = opos[i + 1]; otip[i] = otip[i + 1]
    opos[nobjs - 1] = -1; otip[nobjs - 1] = -1
    return nobjs - 1


@njit(cache=True)
def _idx_en(opos, nobjs, x):
    for i in range(nobjs):
        if opos[i] == x: return i
    return -1


@njit(cache=True)
def _see(pos, t, opos, otip, nobjs, rech, memoria_rechazo):
    """(d, k, left, hallado_en_el_primer_pase): el objeto mas cercano en orden de insercion, con la memoria de rechazo de v9."""
    best_d = 0; best_k = -1; best_left = False; found = False
    for i in range(nobjs):
        x = opos[i]
        if memoria_rechazo > 0 and rech[x] > t: continue
        dl = (pos - x) % L; dr = (x - pos) % L; d = min(dl, dr)
        if (not found) or d < best_d:
            best_d = d; best_k = otip[i]; best_left = dl < dr; found = True
    primer = found
    if not found:
        for i in range(nobjs):
            x = opos[i]
            dl = (pos - x) % L; dr = (x - pos) % L; d = min(dl, dr)
            if (not found) or d < best_d:
                best_d = d; best_k = otip[i]; best_left = dl < dr; found = True
    return best_d, best_k, best_left, primer


# ------------------------------------------------------------------ crecimiento de los buffers (sin recursion)
@njit(cache=True)
def _cap1f(a, n):
    if n <= a.size: return a
    m = a.size * 2
    while m < n: m *= 2
    b = np.zeros(m)
    for i in range(a.size): b[i] = a[i]
    return b


@njit(cache=True)
def _cap1i(a, n):
    if n <= a.size: return a
    m = a.size * 2
    while m < n: m *= 2
    b = np.zeros(m, np.int64)
    for i in range(a.size): b[i] = a[i]
    return b


@njit(cache=True)
def _cap2f(a, n):
    if n <= a.shape[0]: return a
    m = a.shape[0] * 2
    while m < n: m *= 2
    b = np.zeros((m, a.shape[1]))
    for i in range(a.shape[0]):
        for j in range(a.shape[1]): b[i, j] = a[i, j]
    return b


@njit(cache=True)
def _cond(KW, activa, objetivo_AB, nuevo_idx, solap_B, PATM):
    """La condicion `cond()` del original (solapamiento de codigos), para el nacimiento de H-1."""
    cA = _code(KW, activa, PATM[0]); cB = _code(KW, activa, PATM[1])
    n = 0
    for i in range(NKMAX):
        if cA[i] > 0 and cB[i] > 0: n += 1
    if n != objetivo_AB: return False
    if nuevo_idx >= 0 and solap_B >= 0:
        cN = _code(KW, activa, PATM[nuevo_idx])
        nb = 0; na = 0
        for i in range(NKMAX):
            if cN[i] > 0 and cB[i] > 0: nb += 1
            if cN[i] > 0 and cA[i] > 0: na += 1
        if nb != solap_B or na != 0: return False
    return True


# ------------------------------------------------------------------ EL BUCLE
@njit(cache=True)
def _bucle(rng, rrel, rbn, T, learn, invertir_en, nuevo_idx, nuevo_en, nuevo_valc,
           eta, tau_e, alpha, hambre_boca, aversion, costo, nobj, plast, theta, ema, paso, lam,
           memoria_rechazo, mu_norm, div_signo, eta_s, clip_s, puerta, Wl, KW, activa, PATM,
           mask_rel, del_s, del_c, ema_c, puerta_pat, pat_shuf, pat_min,
           vivo, n_nec, tipos, ntipos, costo_a, A_ini, val_esc, hereda_nec, EFEC, valc, crit_exp,
           rep_mide, rep_X, rep_umbral, rep_coste, rep_cuello, rep2, rep2_regalo,
           muerte_real, hereda, dote, cola_max, h1, tiene_alma, alma_muertes,
           nodo, conectado, nodo_k, nodo_lee, miedo_n, miedo_R, d_dote, d_umbral,
           nodo_baraja, nodo_rel, con_desde, rep_acum, f9, seed, objetivo_AB, solap_AB, solap_B,
           nodo_via, nodo_or, sesgo_fijo, f9c):
    Wp = np.zeros((n_nec, NKMAX)); Wn = np.zeros((n_nec, NKMAX)); err = np.zeros(NKMAX); mu = np.zeros((NKMAX, 6)); splits = 0
    el = np.zeros((2, 9)); tr = np.zeros(9)
    Wps = np.zeros((n_nec, 6)); Wns = np.zeros((n_nec, 6))
    _na = 0; _nm = 0
    ncod_key = np.zeros(NCODMAX, np.int64); ncod_cnt = np.zeros(NCODMAX, np.int64); n_cod = 0; desborde = 0
    mup = np.zeros((NKMAX, 6)); mun = np.zeros((NKMAX, 6)); zp = np.zeros(NKMAX); zn = np.zeros(NKMAX)
    _sbE = np.zeros(n_nec)
    umb_c = 1.0 - del_c
    _enc = np.zeros(4, np.int64); _exp = np.full((n_nec, 4), -1, np.int64)
    _mnec = np.zeros(2, np.int64); _bxor = np.zeros((n_nec, 4), np.int64); _exor = np.zeros((n_nec, 4), np.int64)
    # --- REP
    _gv = 0; _desc = 0; _pv = 0; _tdesc = np.zeros(200, np.int64); ntd = 0
    _dq = np.zeros(4, np.int64); _bsac = np.zeros(4, np.int64); _dsac = np.zeros(4, np.int64); _cue2 = False
    # --- REP2
    _tmu = 0; _vidas = np.zeros(400, np.int64); nvi = 0; _dreg = 0; _gv0 = 0
    # --- H1
    co_dote = np.zeros(cola_max); co_has = np.zeros(cola_max, np.int64)
    co_Wps = np.zeros((cola_max, n_nec, 6)); co_Wns = np.zeros((cola_max, n_nec, 6))
    co_ini = 0; co_n = 0
    _nac = 0; _fund = 0; _dfund = 0; _dv = 0; _cdes = 0; _svid = 0; _esfund = True; _nbar = 0
    _dpv = np.zeros(256, np.int64); ndp = 0
    _vh = np.zeros(256, np.int64); nvh = 0
    _org = np.zeros(256, np.int64); nor = 0
    _tfund = np.zeros(200, np.int64); ntf = 0
    # --- ALMA
    nd_P = np.zeros((1024, 6)); nd_R = np.zeros(1024); nd_N = np.zeros(1024, np.int64); nd_n = 0
    ex_t = np.zeros(256, np.int64); ex_k = np.zeros(256, np.int64); ex_n = np.zeros(256, np.int64)
    ex_m = np.zeros(256, np.int64); nex = 0
    mo_t = np.zeros(256, np.int64); mo_k = np.zeros(256, np.int64); mo_n = np.zeros(256, np.int64)
    mo_r = np.zeros(256); nmo = 0
    _con = conectado != 0; _nmu = 0; _causa = -1; _Tef = T; _inerte = 0; _nbar_n = 0
    _ldiv = 0; _nlec = 0; _chk = 0
    _nvia = 0; _fam9 = np.zeros(400, np.int64); nfa = 0; _gpa = 0; _gpn = 0   # F9B/F9C
    _p1 = np.zeros(256, np.int64); _c1 = np.zeros(256, np.int64)
    _tok = np.zeros(256, np.int64); _ncu = np.zeros(256, np.int64); n91 = 0
    # --- mundo
    pos = 0; E = 1.0; Ag = A_ini
    err_max = 0.0; t_conflicto = -1; t_techo = -1; n_techo = 0
    rech = np.full(L, -1, np.int64); prev_on = -1
    sobre = np.zeros((4, 4), np.int64); llegadas = np.zeros((4, 4), np.int64); sin_objetivo = np.zeros(4, np.int64)
    opos = np.full(nobj, -1, np.int64); otip = np.full(nobj, -1, np.int64); nobjs = 0
    nobjs = _spawn(rng, opos, otip, nobjs, nobj, tipos, ntipos)
    deaths = 0
    mord = np.zeros((4, 4), np.int64); vis = np.zeros((4, 4), np.int64)
    st_t = np.zeros(256, np.int64); st_k = np.zeros(256, np.int64); nst = 0
    q_div = T // 4
    x = np.empty(9); m = np.zeros(2)
    w6 = np.empty(6); Pv = np.empty(6)
    Wb = np.empty(NKMAX); Wx = np.empty(NKMAX); Rv = np.zeros(n_nec)
    for t in range(T):
        if invertir_en >= 0 and t == invertir_en:
            valc[0] = 1; valc[1] = 0
        if nuevo_idx >= 0 and t == nuevo_en:
            tipos[ntipos] = nuevo_idx; ntipos += 1; valc[nuevo_idx] = nuevo_valc
        q = min(t // q_div, 3)
        hambre = min(max(1 - E, 0.0), 1.0)
        _sac = rep_mide != 0 and E >= rep_umbral and Ag >= rep_umbral
        if n_nec > 1:   # VIVO: deficit por necesidad; manda la ACTIVA (la mas deficitaria)
            _dfa = min(max(1 - Ag, 0.0), 1.0); _na = 1 if _dfa > hambre else 0
            if _na: hambre = _dfa
            if rep_cuello == 1 and hambre == 0 and _dfa == 0: _na = 0 if E <= Ag else 1
            _cue2 = rep_cuello == 2 and hambre == 0 and _dfa == 0
            _nm = 0 if val_esc else _na
        d, k, left, primer = _see(pos, t, opos, otip, nobjs, rech, memoria_rechazo)
        if not primer: sin_objetivo[q] += 1
        pat = PATM[k]
        for i in range(6): x[i] = pat[i] * 1.2
        x[6] = 1.5 if left else 0.0; x[7] = 0.0 if left else 1.5; x[8] = 1.0 if d == 0 else 0.0
        noise = .15 + .5 * hambre
        V = Wl @ x
        p = 1 / (1 + np.exp(-(V - .8) / noise))
        u = p + rng.normal(0, .3, 2)
        m[0] = 0.0; m[1] = 0.0
        if u.max() > .5: m[np.argmax(u)] = 1
        for j in range(9): tr[j] = tr[j] * .7 + x[j]
        if learn:
            for i in range(2):
                for j in range(9): el[i, j] = el[i, j] * tau_e + (m[i] - p[i]) * tr[j]
        pos = (pos + int(m[1] - m[0])) % L
        d2, _k2, _l2, _p2 = _see(pos, t, opos, otip, nobjs, rech, memoria_rechazo)
        Rp = .2 if d2 < d else 0.0
        R = 0.0
        io = _idx_en(opos, nobjs, pos)
        if io >= 0:
            kk = otip[io]; P = PATM[kk]; kc = _code(KW, activa, P)
            for i in range(NKMAX): Wb[i] = Wp[_nm, i] - Wn[_nm, i]
            _wf = Wb @ kc
            for i in range(6): w6[i] = Wps[_nm, i] - Wns[_nm, i]
            _ws = np.dot(w6, P)
            _fa9 = False
            if puerta >= 0: _fa9 = _famil(Wb, kc, puerta, puerta_pat, pat_min, pat_shuf, ncod_key, ncod_cnt, n_cod)
            if puerta < 0:
                _wt = _wf + _ws
            else:
                _wt = _wf if _fa9 else _ws
            if f9c:   # F9C: encuentros con la PUERTA DE v14 abierta / encuentros totales (SOLO LECTURA)
                _gpn += 1
                if _fa9: _gpa += 1
            if _cue2:   # CUELLO_MIN (control que puede ganar): la lectura PESIMISTA de las dos filas
                _o = 1 - _na
                for i in range(NKMAX): Wx[i] = Wp[_o, i] - Wn[_o, i]
                _f2 = Wx @ kc
                for i in range(6): w6[i] = Wps[_o, i] - Wns[_o, i]
                _s2 = np.dot(w6, P)
                if puerta < 0:
                    _v2 = _f2 + _s2
                else:
                    _v2 = _f2 if _famil(Wx, kc, puerta, puerta_pat, pat_min, pat_shuf, ncod_key, ncod_cnt, n_cod) else _s2
                _wt = min(_wt, _v2)
            Vb = alpha * _wt + hambre_boca * hambre + .5
            if sesgo_fijo != 0.0: Vb += sesgo_fijo   # F9C: CAUTELA -- empujon CONSTANTE en la boca, SIN informacion
            pb = 1 / (1 + np.exp(-Vb / .3)); mordio = rng.random() < pb
            vis[kk, q] += 1
            if _sac: _dsac[kk] += 1
            vk = valc[kk]
            sobre[vk, q] += 1; llegadas[vk, q] += 1 if prev_on != pos else 0
            if vivo and prev_on != pos:   # VIVO: EXPOSICIONES y EXPOSICIONES HASTA CRITERIO, por necesidad
                _enc[kk] += 1; _exor[_na, kk] += 1
                if tiene_alma:
                    nex += 1
                    if nex > ex_t.size:
                        ex_t = _cap1i(ex_t, nex); ex_k = _cap1i(ex_k, nex)
                        ex_n = _cap1i(ex_n, nex); ex_m = _cap1i(ex_m, nex)
                    ex_t[nex - 1] = t; ex_k[nex - 1] = kk; ex_n[nex - 1] = _na; ex_m[nex - 1] = 1 if mordio else 0
                for _n in range(n_nec):
                    _s0 = EFEC[vk, _n]
                    if _s0 != 0.0 and _exp[_n, kk] < 0:
                        for i in range(NKMAX): Wx[i] = Wp[_n, i] - Wn[_n, i]
                        _f3 = Wx @ kc
                        for i in range(6): w6[i] = Wps[_n, i] - Wns[_n, i]
                        _s3 = np.dot(w6, P)
                        if puerta < 0:
                            _v0 = _f3 + _s3
                        else:
                            _v0 = _f3 if _famil(Wx, kc, puerta, puerta_pat, pat_min, pat_shuf, ncod_key, ncod_cnt, n_cod) else _s3
                        if _v0 * _s0 > 0 and abs(_v0) >= crit_exp: _exp[_n, kk] = _enc[kk]
            if memoria_rechazo > 0 and not mordio: rech[pos] = t + memoria_rechazo
            if mordio:
                if vivo:   # VIVO: la mordida tiene consecuencia VECTORIAL
                    dS0 = EFEC[vk, 0]; dS1 = EFEC[vk, 1]
                    for _n in range(n_nec):
                        _xv = EFEC[vk, _n]
                        Rv[_n] = 1.0 if _xv > 0 else (-3.0 if _xv < 0 else 0.0)
                    R = Rv[_na]; E = min(E + dS0, 1.5); Ag = min(Ag + dS1, 1.5); _bxor[_na, kk] += 1
                else:
                    dS0 = 0.8 if vk == 0 else -0.4
                    R = 1.0 if vk == 0 else -3.0
                    Rv[0] = R
                    E = min(E + dS0, 1.5)
                mord[kk, q] += 1
                if tiene_alma:
                    nmo += 1
                    if nmo > mo_t.size:
                        mo_t = _cap1i(mo_t, nmo); mo_k = _cap1i(mo_k, nmo)
                        mo_n = _cap1i(mo_n, nmo); mo_r = _cap1f(mo_r, nmo)
                    mo_t[nmo - 1] = t; mo_k[nmo - 1] = kk; mo_n[nmo - 1] = _na; mo_r[nmo - 1] = R
                if _sac: _bsac[kk] += 1
                _ky = _clave(kc); _ic = _pos_cod(ncod_key, n_cod, _ky)
                if _ic < 0:
                    if n_cod < NCODMAX:
                        ncod_key[n_cod] = _ky; ncod_cnt[n_cod] = 1; n_cod += 1
                    else:
                        desborde += 1
                else:
                    ncod_cnt[_ic] += 1
                nobjs = _borrar(opos, otip, nobjs, pos); nobjs = _spawn(rng, opos, otip, nobjs, nobj, tipos, ntipos)
                rech[pos] = -1
                if learn:
                    dlt = (R - _wt) if puerta < 0 else (R - _wf)
                    if eta_s != 0.0:
                        _ds = dlt if puerta < 0 else (R - _ws)
                        if lam != 0.0:
                            for i in range(6):
                                if P[i] > 0:
                                    _mcs = min(Wps[_nm, i], Wns[_nm, i])
                                    Wps[_nm, i] = Wps[_nm, i] - lam * _mcs; Wns[_nm, i] = Wns[_nm, i] - lam * _mcs
                                else:
                                    Wps[_nm, i] = Wps[_nm, i] - lam * 0.0; Wns[_nm, i] = Wns[_nm, i] - lam * 0.0
                        if _ds > 0:
                            for i in range(6): Wps[_nm, i] = min(max(Wps[_nm, i] + eta_s * _ds * P[i], 0.0), clip_s)
                        else:
                            for i in range(6): Wns[_nm, i] = min(max(Wns[_nm, i] + eta_s * aversion * (-_ds) * P[i], 0.0), clip_s)
                    if lam != 0.0:
                        for i in range(NKMAX):
                            if kc[i] > 0:
                                mcom = min(Wp[_nm, i], Wn[_nm, i]); Wp[_nm, i] -= lam * mcom; Wn[_nm, i] -= lam * mcom
                    _trunca = False
                    for i in range(NKMAX):
                        if kc[i] > 0:
                            if dlt > 0:
                                if (Wp[_nm, i] + eta * dlt) > 3.0: _trunca = True
                            else:
                                if (Wn[_nm, i] + eta * aversion * (-dlt)) > 3.0: _trunca = True
                    if _trunca:
                        n_techo += 1
                        if t_techo < 0: t_techo = t
                    if dlt > 0:
                        for i in range(NKMAX): Wp[_nm, i] = min(max(Wp[_nm, i] + eta * dlt * kc[i], 0.0), 3.0)
                    else:
                        for i in range(NKMAX): Wn[_nm, i] = min(max(Wn[_nm, i] + eta * aversion * (-dlt) * kc[i], 0.0), 3.0)
                    if t_conflicto < 0:
                        for i in range(NKMAX):
                            if kc[i] > 0 and min(Wp[_nm, i], Wn[_nm, i]) > 0:
                                t_conflicto = t; break
                    if n_nec > 1:   # VIVO: las OTRAS necesidades aprenden de SU componente del MISMO bocado
                        for _n in range(n_nec):
                            if _n == _nm: continue
                            _Rn = Rv[_n]
                            for i in range(NKMAX): Wx[i] = Wp[_n, i] - Wn[_n, i]
                            _wfn = Wx @ kc
                            for i in range(6): w6[i] = Wps[_n, i] - Wns[_n, i]
                            _wsn = np.dot(w6, P)
                            _dn = (_Rn - (_wfn + _wsn)) if puerta < 0 else (_Rn - _wfn)
                            if eta_s != 0.0:
                                _dsn = _dn if puerta < 0 else (_Rn - _wsn)
                                if lam != 0.0:
                                    for i in range(6):
                                        if P[i] > 0:
                                            _mn2 = min(Wps[_n, i], Wns[_n, i])
                                            Wps[_n, i] = Wps[_n, i] - lam * _mn2; Wns[_n, i] = Wns[_n, i] - lam * _mn2
                                        else:
                                            Wps[_n, i] = Wps[_n, i] - lam * 0.0; Wns[_n, i] = Wns[_n, i] - lam * 0.0
                                if _dsn > 0:
                                    for i in range(6): Wps[_n, i] = min(max(Wps[_n, i] + eta_s * _dsn * P[i], 0.0), clip_s)
                                else:
                                    for i in range(6): Wns[_n, i] = min(max(Wns[_n, i] + eta_s * aversion * (-_dsn) * P[i], 0.0), clip_s)
                            if lam != 0.0:
                                for i in range(NKMAX):
                                    if kc[i] > 0:
                                        _mc2 = min(Wp[_n, i], Wn[_n, i]); Wp[_n, i] -= lam * _mc2; Wn[_n, i] -= lam * _mc2
                            if _dn > 0:
                                for i in range(NKMAX): Wp[_n, i] = min(max(Wp[_n, i] + eta * _dn * kc[i], 0.0), 3.0)
                            else:
                                for i in range(NKMAX): Wn[_n, i] = min(max(Wn[_n, i] + eta * aversion * (-_dn) * kc[i], 0.0), 3.0)
                    if plast:
                        nidx = 0; idxs = np.zeros(K, np.int64)
                        for i in range(NKMAX):
                            if kc[i] > 0:
                                idxs[nidx] = i; nidx += 1
                        for a in range(nidx):
                            c = idxs[a]; err[c] = (1 - ema) * err[c] + ema * abs(dlt)
                            for j in range(6): mu[c, j] = (1 - ema) * mu[c, j] + ema * P[j]
                            if R > 0:   # D: medias de P condicionadas al signo de R
                                for j in range(6): mup[c, j] = (1 - ema_c) * mup[c, j] + ema_c * P[j]
                                zp[c] = (1 - ema_c) * zp[c] + ema_c
                            elif R < 0:
                                for j in range(6): mun[c, j] = (1 - ema_c) * mun[c, j] + ema_c * P[j]
                                zn[c] = (1 - ema_c) * zn[c] + ema_c
                            if err[c] > err_max: err_max = err[c]
                        sP = 0.0
                        for j in range(6): sP += P[j]
                        for a in range(nidx):
                            c = idxs[a]
                            if div_signo:
                                smu = 0.0
                                for j in range(6): smu += mu[c, j]
                                dist = np.empty(6); kj = np.empty(6)
                                disp = mask_rel == 2 and zp[c] > 1e-6 and zn[c] > 1e-6   # D: HIJA DISPERSA
                                for j in range(6):
                                    dist[j] = P[j] - (mu[c, j] * (sP / max(smu, 1e-9)) if mu_norm else mu[c, j])
                                    if disp:
                                        _mp = mup[c, j] / zp[c]; _mn = mun[c, j] / zn[c]
                                        _rel = P[j] > 0 and (abs(_mp - _mn) > del_s or min(_mp, _mn) > umb_c)
                                    else:
                                        _rel = P[j] > 0
                                    kj[j] = min(max(KW[c, j] * (1 - 0.05) + paso * dist[j], 0.0), 5.0) * (1.0 if _rel else 0.0)
                                libre = -1
                                for i in range(NKMAX):
                                    if not activa[i]:
                                        libre = i; break
                                if Wb[c] * R < 0 and abs(Wb[c]) > 0.2 and (kj @ P) > (KW[c] @ P) and libre >= 0:
                                    jn = libre; activa[jn] = True
                                    for j in range(6): KW[jn, j] = kj[j]
                                    if R > 0:
                                        Wp[_nm, jn] = Wp[_nm, c]; Wn[_nm, jn] = 0.; Wp[_nm, c] = 0.
                                    else:
                                        Wn[_nm, jn] = Wn[_nm, c]; Wp[_nm, jn] = 0.; Wn[_nm, c] = 0.
                                    if n_nec > 1 and hereda_nec:   # VIVO: la hija HEREDA el valor de las OTRAS necesidades
                                        for _n in range(n_nec):
                                            if _n != _nm:
                                                Wp[_n, jn] = Wp[_n, c]; Wn[_n, jn] = Wn[_n, c]
                                    for j in range(6): mu[jn, j] = P[j] * (smu / sP)
                                    err[c] = 0.0; err[jn] = 0.0; splits += 1
                                    nst += 1
                                    if nst > st_t.size:
                                        st_t = _cap1i(st_t, nst); st_k = _cap1i(st_k, nst)
                                    st_t[nst - 1] = t; st_k[nst - 1] = kk
                                    for j in range(6):
                                        mup[jn, j] = mup[c, j]; mun[jn, j] = mun[c, j]
                                    zp[jn] = zp[c]; zn[jn] = zn[c]
                            elif err[c] > theta:
                                libre = -1
                                for i in range(NKMAX):
                                    if not activa[i]:
                                        libre = i; break
                                if libre >= 0:
                                    jn = libre; activa[jn] = True
                                    smu = 0.0
                                    for j in range(6): smu += mu[c, j]
                                    for j in range(6):
                                        dj = P[j] - (mu[c, j] * (sP / max(smu, 1e-9)) if mu_norm else mu[c, j])
                                        KW[jn, j] = min(max(KW[c, j] + paso * dj, 0.0), 5.0)
                                        KW[c, j] = min(max(KW[c, j] - paso * dj, 0.0), 5.0)
                                    for _n in range(n_nec):
                                        Wp[_n, jn] = Wp[_n, c]; Wn[_n, jn] = Wn[_n, c]
                                    for j in range(6): mu[jn, j] = mu[c, j]
                                    err[c] = 0.0; err[jn] = 0.0; splits += 1
                                    nst += 1
                                    if nst > st_t.size:
                                        st_t = _cap1i(st_t, nst); st_k = _cap1i(st_k, nst)
                                    st_t[nst - 1] = t; st_k[nst - 1] = kk
        prev_on = pos if _idx_en(opos, nobjs, pos) >= 0 else -1
        E -= costo
        if vivo: Ag -= costo_a
        if rng.random() < .003 and nobjs > 0:
            i = rng.integers(0, nobjs); _dx = opos[i]
            nobjs = _borrar(opos, otip, nobjs, _dx); nobjs = _spawn(rng, opos, otip, nobjs, nobj, tipos, ntipos); rech[_dx] = -1
        if learn:
            s = eta * (1 + 2 * hambre) * (max(R, 0.0) + Rp)
            for i in range(2):
                for j in range(9): Wl[i, j] = min(max(Wl[i, j] + s * el[i, j], 0.0), 1.5)
        # ---------------------------------------------------------------- LA MUERTE
        if E <= 0 or (vivo and Ag <= 0):
            if tiene_alma: _causa = 0 if E <= 0 else 1
            deaths += 1; _mnec[0 if E <= 0 else 1] += 1; E = .6
            if vivo: Ag = .6
            pos = rng.integers(0, L)
            if rep_acum: _gv = 0   # F9: la ventana ACUMULADA es DENTRO de un cuerpo
            if h1:   # H1: se cierra el cuerpo que muere (solo lectura)
                _svid += t - _tmu
                nvh += 1
                if nvh > _vh.size: _vh = _cap1i(_vh, nvh)
                _vh[nvh - 1] = t - _tmu
                nor += 1
                if nor > _org.size: _org = _cap1i(_org, nor)
                _org[nor - 1] = 0 if _esfund else 1
                ndp += 1
                if ndp > _dpv.size: _dpv = _cap1i(_dpv, ndp)
                _dpv[ndp - 1] = _dv; _dv = 0
            if tiene_alma:   # ALMA: el nodo se llena y el alma elige UNA curita del MENU CERRADO
                _nmu += 1
                if con_desde and nodo and _nmu >= con_desde: _con = True   # F9: CONEXION TARDIA
                if nodo:
                    _i0 = nmo - nodo_k
                    if _i0 < 0: _i0 = 0
                    for _j9 in range(_i0, nmo):
                        _n2 = nd_n + 1
                        if _n2 > nd_R.size:
                            nd_P = _cap2f(nd_P, _n2); nd_R = _cap1f(nd_R, _n2); nd_N = _cap1i(nd_N, _n2)
                        for _z9 in range(6): nd_P[nd_n, _z9] = PATM[mo_k[_j9], _z9]
                        nd_R[nd_n] = mo_r[_j9]; nd_N[nd_n] = mo_n[_j9]; nd_n = _n2
                _edad = _vh[nvh - 1]; _hijos = _dpv[ndp - 1]
                _fu = 1 if _esfund else 0; _co = 1 if _con else 0
                _ca = _causa
                _ext = ex_t[:nex]; _exk = ex_k[:nex]; _exn = ex_n[:nex]; _exm = ex_m[:nex]
                _mot = mo_t[:nmo]; _mok = mo_k[:nmo]; _mon = mo_n[:nmo]; _mor = mo_r[:nmo]
                with objmode(_c9='int64'):
                    _c9 = _alma_llama(_nmu, t, _ca, _edad, _hijos, _fu, _co, nd_n, dote, rep_umbral, hereda,
                                      _ext, _exk, _exn, _exm, _mot, _mok, _mon, _mor, _desc, deaths, _fund, nodo_baraja)
                if _c9 == 0: _con = True   # (a) CONECTAR AL NODO
                elif _c9 == 1:   # (b) SUBIR EL MIEDO escribiendolo en el nodo
                    _uk = -1; _un = -1
                    if nmo > 0:
                        _uk = mo_k[nmo - 1]; _un = mo_n[nmo - 1]
                    elif nex > 0:
                        _uk = ex_k[nex - 1]; _un = ex_n[nex - 1]
                    if _uk >= 0 and nodo:
                        for _ in range(miedo_n):
                            _n2 = nd_n + 1
                            if _n2 > nd_R.size:
                                nd_P = _cap2f(nd_P, _n2); nd_R = _cap1f(nd_R, _n2); nd_N = _cap1i(nd_N, _n2)
                            for _z9 in range(6): nd_P[nd_n, _z9] = PATM[_uk, _z9]
                            nd_R[nd_n] = miedo_R; nd_N[nd_n] = _un; nd_n = _n2
                    else:
                        _inerte += 1
                elif _c9 == 2: dote = round(min(dote + d_dote, rep_umbral - 0.05), 6)          # (c) DOTE MAYOR
                elif _c9 == 3: rep_umbral = round(max(rep_umbral - d_umbral, dote + 0.05), 6)  # (d) BAJAR EL UMBRAL
                elif _c9 == 4: hereda = 1                                                     # (e) HEREDAR VALORES (M1)
                _co = 1 if _con else 0
                with objmode(_du='int64'):
                    _du = _reg_curita(_nmu, _c9, dote, rep_umbral, hereda, _co, nd_n, _ca, _edad, _hijos)
                _chk += _du   # _reg_curita devuelve 0 (objmode exige que la salida se use)
                if f9:   # F9: LAS MEDIDAS DEL CUERPO QUE MUERE (p1 y c1 SIEMPRE juntas)
                    _v1 = -1; _v2 = -1; _v3 = -1
                    for _j9 in range(nex):
                        if ex_k[_j9] == (1 if ex_n[_j9] == 0 else 3):
                            _v1 = 1 - ex_m[_j9]; break
                    for _j9 in range(nex):
                        if ex_k[_j9] == (0 if ex_n[_j9] == 0 else 2):
                            _v2 = ex_m[_j9]; break
                    for _j9 in range(nmo):
                        if mo_r[_j9] > 0:
                            _v3 = mo_t[_j9] - _tmu; break
                    n91 += 1
                    if n91 > _p1.size:
                        _p1 = _cap1i(_p1, n91); _c1 = _cap1i(_c1, n91)
                        _tok = _cap1i(_tok, n91); _ncu = _cap1i(_ncu, n91)
                    _p1[n91 - 1] = _v1; _c1[n91 - 1] = _v2; _tok[n91 - 1] = _v3; _ncu[n91 - 1] = 1 if _con else 0
                nex = 0; nmo = 0
            if muerte_real:   # H1: LA MUERTE BORRA AL INDIVIDUO; nace el siguiente de la cola
                _nac += 1
                _hay = co_n > 0
                _md = dote; _mhas = 0
                _mWps = np.zeros((n_nec, 6)); _mWns = np.zeros((n_nec, 6))
                if _hay:
                    _md = co_dote[co_ini]; _mhas = co_has[co_ini]
                    for _n in range(n_nec):
                        for j in range(6):
                            _mWps[_n, j] = co_Wps[co_ini, _n, j]; _mWns[_n, j] = co_Wns[co_ini, _n, j]
                    co_ini = (co_ini + 1) % cola_max; co_n -= 1
                _esfund = not _hay
                if _esfund:
                    _fund += 1
                    if ntf < 200:
                        _tfund[ntf] = t; ntf += 1
                # --- _nace(_nac, _m): memoria vacia + lo que `hereda` deje pasar; rng PROPIO del hijo (ERR-60)
                with objmode(_rh=GENT):
                    _rh = np.random.default_rng(700000 + 1000000 * seed + _nac)
                Wl[:] = _rh.uniform(.1, .4, (2, 9))
                for i in range(2):
                    for j in range(9): el[i, j] = 0.0
                for j in range(9): tr[j] = 0.0
                for _n in range(n_nec):
                    for i in range(NKMAX):
                        Wp[_n, i] = 0.0; Wn[_n, i] = 0.0
                    for j in range(6):
                        Wps[_n, j] = 0.0; Wns[_n, j] = 0.0
                    _sbE[_n] = 0.0
                for i in range(NKMAX):
                    err[i] = 0.0; zp[i] = 0.0; zn[i] = 0.0
                    for j in range(6):
                        mu[i, j] = 0.0; mup[i, j] = 0.0; mun[i, j] = 0.0
                n_cod = 0
                for i in range(L): rech[i] = -1
                prev_on = -1
                KW[:] = 0.0
                for i in range(NKMAX): activa[i] = False
                KW[:NK] = _rh.uniform(0, 1, (NK, 6))
                for i in range(NK): activa[i] = True
                if solap_AB > 0:
                    KW[:solap_AB] = 0.0
                    for i in range(solap_AB): KW[i, 0] = 5.0
                while not _cond(KW, activa, objetivo_AB, nuevo_idx, solap_B, PATM):
                    KW[objetivo_AB:NK] = _rh.uniform(0, 1, (NK - objetivo_AB, 6))
                if _hay and _mhas:
                    for _n in range(n_nec):
                        for j in range(6):
                            Wps[_n, j] = _mWps[_n, j]; Wns[_n, j] = _mWns[_n, j]
                E = _md; Ag = E
                # --- ALMA: el cuerpo CONECTADO nace leyendo el nodo (EXPOSICIONES SIN CONSECUENCIA)
                if tiene_alma and _con and nodo and nd_n > 0:
                    if nodo_rel == 1 or nodo_rel == 3:   # F9: el ALCANCE es TODO el nodo
                        nms = nd_n
                        ms_i = np.arange(nd_n)
                    elif nodo_rel == 2:   # F9: CONTROL DE ACCESO (mismo alcance, orden cronologico, al azar)
                        _kk9 = min(nodo_lee, nd_n)
                        with objmode(ms_i='int64[:]'):
                            ms_i = np.sort(rrel.choice(nd_n, size=_kk9, replace=False)).astype(np.int64)
                        nms = ms_i.size
                    else:
                        _i0 = nd_n - nodo_lee
                        if _i0 < 0: _i0 = 0
                        nms = nd_n - _i0
                        ms_i = np.arange(_i0, nd_n)
                    ms_P = np.empty((nms, 6)); ms_R = np.empty(nms); ms_N = np.empty(nms, np.int64)
                    for _j9 in range(nms):
                        _s9 = ms_i[_j9]
                        for _z9 in range(6): ms_P[_j9, _z9] = nd_P[_s9, _z9]
                        ms_R[_j9] = nd_R[_s9]; ms_N[_j9] = nd_N[_s9]
                    if nodo_or:   # F9C: NODO ORACULO (cota superior). La TABLA VERDADERA (patron, necesidad) -> R del
                        #   mundo, armada de PATM y EFEC, que YA existian. Memoria nueva: CERO (se arma y se tira).
                        #   El pool son nodo_lee COPIAS de la tabla (8*nodo_lee = 400 con nodo_lee=50): el recien
                        #   nacido lee sus nodo_lee mensajes con LA MISMA regla de relevancia que los demas brazos.
                        _nor = 4 * min(n_nec, 2); _rp9 = max(1, nodo_lee); nms = _nor * _rp9
                        ms_P = np.empty((nms, 6)); ms_R = np.empty(nms); ms_N = np.empty(nms, np.int64)
                        _q9 = 0
                        for _ in range(_rp9):
                            for _n9 in range(min(n_nec, 2)):
                                for _k9 in range(4):
                                    for _z9 in range(6): ms_P[_q9, _z9] = PATM[_k9, _z9]
                                    _e9 = EFEC[valc[_k9], _n9]
                                    ms_R[_q9] = 1.0 if _e9 > 0 else (-3.0 if _e9 < 0 else 0.0)
                                    ms_N[_q9] = _n9; _q9 += 1
                    if nodo_baraja:   # ALMA2: CONTROL DE CONTENIDO (las recompensas se permutan ENTRE mensajes)
                        _pn = rbn.permutation(nms)
                        _ident = True
                        for _j9 in range(nms):
                            if _pn[_j9] != _j9:
                                _ident = False; break
                        if _ident: _nbar_n += 1
                        _rr = np.empty(nms)
                        for _j9 in range(nms): _rr[_j9] = ms_R[_pn[_j9]]
                        ms_R = _rr
                    sel = np.zeros(nms, np.int64); nsel = 0; ordenado = True
                    if nodo_rel == 3:   # RELEVANCIA FIJA (control): UNA sola vez, con el vector del recien nacido
                        sc = np.empty(nms)
                        for _j9 in range(nms):
                            _n7 = ms_N[_j9]; _s7 = 0.0
                            for _z9 in range(6): _s7 += (Wps[_n7, _z9] - Wns[_n7, _z9]) * ms_P[_j9, _z9]
                            sc[_j9] = abs(ms_R[_j9] - _s7)
                        usado = np.zeros(nms, np.int64)
                        _kk9 = min(nodo_lee, nms)
                        for _ in range(_kk9):   # lexsort((-indice,-puntaje))[:k]: maximo, empate -> indice mayor
                            _b9 = -1; _bs = -1.0e308
                            for _j9 in range(nms):
                                if usado[_j9] == 0 and sc[_j9] >= _bs:
                                    _bs = sc[_j9]; _b9 = _j9
                            usado[_b9] = 1; sel[nsel] = _b9; nsel += 1
                        for a in range(nsel):   # sorted(...)
                            for b in range(a + 1, nsel):
                                if sel[b] < sel[a]:
                                    _tm = sel[a]; sel[a] = sel[b]; sel[b] = _tm
                        ms_P2 = np.empty((nsel, 6)); ms_R2 = np.empty(nsel); ms_N2 = np.empty(nsel, np.int64)
                        for a in range(nsel):
                            for _z9 in range(6): ms_P2[a, _z9] = ms_P[sel[a], _z9]
                            ms_R2[a] = ms_R[sel[a]]; ms_N2[a] = ms_N[sel[a]]
                        ms_P = ms_P2; ms_R = ms_R2; ms_N = ms_N2; nms = nsel; nsel = 0
                    rst = np.arange(nms); nrst = nms
                    _nit = min(nodo_lee, nms) if nodo_rel == 1 else nms
                    for _it9 in range(_nit):
                        if nodo_rel == 1:   # RELEVANCIA VIVA: el puntaje se recalcula DESPUES de cada mensaje
                            _b9 = -1; _bs = -1.0e308
                            for _j9 in range(nrst):
                                _i7 = rst[_j9]; _n7 = ms_N[_i7]; _s7 = 0.0
                                for _z9 in range(6): _s7 += (Wps[_n7, _z9] - Wns[_n7, _z9]) * ms_P[_i7, _z9]
                                _sc = abs(ms_R[_i7] - _s7)
                                if _sc >= _bs:
                                    _bs = _sc; _b9 = _j9
                            _i7 = rst[_b9]
                            if nsel > 0 and _i7 < sel[nsel - 1]: ordenado = False
                            sel[nsel] = _i7; nsel += 1
                            for _j9 in range(_b9, nrst - 1): rst[_j9] = rst[_j9 + 1]
                            nrst -= 1
                        else:
                            _i7 = _it9
                        _n7 = ms_N[_i7]
                        for _z9 in range(6): Pv[_z9] = ms_P[_i7, _z9]
                        _R7 = ms_R[_i7]
                        if lam != 0.0:
                            for _z9 in range(6):
                                if Pv[_z9] > 0:
                                    _mc7 = min(Wps[_n7, _z9], Wns[_n7, _z9])
                                    Wps[_n7, _z9] = Wps[_n7, _z9] - lam * _mc7
                                    Wns[_n7, _z9] = Wns[_n7, _z9] - lam * _mc7
                                else:
                                    Wps[_n7, _z9] = Wps[_n7, _z9] - lam * 0.0
                                    Wns[_n7, _z9] = Wns[_n7, _z9] - lam * 0.0
                        for _z9 in range(6): w6[_z9] = Wps[_n7, _z9] - Wns[_n7, _z9]
                        _ds7 = _R7 - np.dot(w6, Pv)
                        if _ds7 > 0:
                            for _z9 in range(6): Wps[_n7, _z9] = min(max(Wps[_n7, _z9] + eta_s * _ds7 * Pv[_z9], 0.0), clip_s)
                        else:
                            for _z9 in range(6): Wns[_n7, _z9] = min(max(Wns[_n7, _z9] + eta_s * aversion * (-_ds7) * Pv[_z9], 0.0), clip_s)
                        if nodo_via:   # F9B/F9C: el mensaje entra TAMBIEN por la VIA RAPIDA, con la MISMA regla local de la mordida
                            _kc7 = _code(KW, activa, Pv)
                            if nodo_via == 1:   # la lectura CUENTA como evidencia del codigo exacto (organismo_f9b)
                                _ky7 = _clave(_kc7); _ic7 = _pos_cod(ncod_key, n_cod, _ky7)
                                if _ic7 < 0:
                                    if n_cod < NCODMAX:
                                        ncod_key[n_cod] = _ky7; ncod_cnt[n_cod] = 1; n_cod += 1
                                    else:
                                        desborde += 1
                                else:
                                    ncod_cnt[_ic7] += 1
                            for i in range(NKMAX): Wx[i] = Wp[_n7, i] - Wn[_n7, i]
                            _df7 = _R7 - np.dot(Wx, _kc7)
                            if lam != 0.0:
                                for i in range(NKMAX):
                                    if _kc7[i] > 0:
                                        _mf7 = min(Wp[_n7, i], Wn[_n7, i])
                                        Wp[_n7, i] -= lam * _mf7; Wn[_n7, i] -= lam * _mf7
                            if _df7 > 0:
                                for i in range(NKMAX): Wp[_n7, i] = min(max(Wp[_n7, i] + eta * _df7 * _kc7[i], 0.0), 3.0)
                            else:
                                for i in range(NKMAX): Wn[_n7, i] = min(max(Wn[_n7, i] + eta * aversion * (-_df7) * _kc7[i], 0.0), 3.0)
                            _nvia += 1   # LEER NO DIVIDE: div_signo no se dispara al leer
                    _nlec += 1
                    if nodo_via:   # F9B/F9C: cuantos de los 4 estimulos le son FAMILIARES al recien nacido RECIEN leido (SOLO LECTURA)
                        _nf9 = 0
                        for i in range(NKMAX): Wx[i] = Wp[_nm, i] - Wn[_nm, i]
                        for _z9 in range(4):
                            if _famil(Wx, _code(KW, activa, PATM[_z9]), puerta, puerta_pat, pat_min, pat_shuf,
                                      ncod_key, ncod_cnt, n_cod): _nf9 += 1
                        if nfa < 400:
                            _fam9[nfa] = _nf9; nfa += 1
                    if nodo_rel:   # F9: la seleccion NO PUDO ser la de recencia (si _ldiv=0 la perilla es INERTE)
                        if nd_n > nodo_lee or (nodo_rel == 1 and not ordenado): _ldiv += 1
            if rep2:   # REP2: longitud de la vida que termina y marca del renacer
                if nvi < 400:
                    _vidas[nvi] = t - _tmu; nvi += 1
                _tmu = t
            if tiene_alma and _nmu >= alma_muertes:
                _Tef = t + 1; break
        # ---------------------------------------------------------------- LA VENTANA DE VIABILIDAD
        if rep_mide:
            if E >= rep_umbral and Ag >= rep_umbral:
                if rep2 and _gv == 0: _gv0 = t
                _gv += 1; _pv += 1
            else:
                _gv = _gv if rep_acum else 0   # F9: rep_acum=1 -> cuenta pasos saciados aunque no sean seguidos
            if _gv >= rep_X:
                _desc += 1; _dq[q] += 1; _gv = 0
                if rep2 and _gv0 - _tmu < rep2_regalo: _dreg += 1
                if ntd < 200:
                    _tdesc[ntd] = t; ntd += 1
                if rep_coste != 0.0:
                    E -= rep_coste; Ag -= rep_coste
                if h1: _dv += 1
                if muerte_real:   # H1: el padre PAGA la dote y pone al hijo en la cola (la memoria se congela AQUI)
                    E -= dote; Ag -= dote
                    if _esfund and _gv0 - _tmu < rep2_regalo: _dfund += 1
                    if co_n >= cola_max:
                        co_ini = (co_ini + 1) % cola_max; co_n -= 1; _cdes += 1
                    _pp = (co_ini + co_n) % cola_max
                    co_dote[_pp] = dote
                    co_has[_pp] = 1 if hereda > 0 else 0
                    for _n in range(n_nec):
                        for j in range(6):
                            co_Wps[_pp, _n, j] = Wps[_n, j]; co_Wns[_pp, _n, j] = Wns[_n, j]
                    co_n += 1
    return (Wp, Wn, Wps, Wns, KW, activa, splits, st_t[:nst], st_k[:nst], mord, vis, sobre, llegadas, sin_objetivo,
            deaths, err_max, t_conflicto, t_techo, n_techo, ncod_key[:n_cod], ncod_cnt[:n_cod], n_cod, desborde,
            _nm, Ag, _mnec, _exp, _enc, _bxor, _exor, _sbE,
            _desc, _pv, _dq, _tdesc[:ntd], _bsac, _dsac,
            _dreg, _vidas[:nvi], _tmu,
            _nac, _fund, _dfund, _dpv[:ndp], _dv, _vh[:nvh], _org[:nor], _svid, co_n, _cdes, _tfund[:ntf], _nbar,
            _nmu, _con, dote, rep_umbral, hereda, _Tef, _inerte,
            nd_P[:nd_n], nd_R[:nd_n], nd_N[:nd_n], nd_n, _nbar_n, _ldiv, _nlec,
            _p1[:n91], _c1[:n91], _tok[:n91], _ncu[:n91], _esfund, _chk,
            _nvia, _fam9[:nfa], _gpa, _gpn)


def run(seed,T=100000,learn=True,invertir_en=None,nuevo=None,nuevo_en=50000,nuevo_val='veneno',solap_B=None,
        eta=.03,tau_e=.85,alpha=1.2,hambre_boca=2.0,aversion=1.0,costo=.002,nobj=4,log_cada=None,plast=True,theta=0.6,ema=0.02,paso=0.5,solap_AB=None,lam=0.05,memoria_rechazo=20,mu_norm=True,div_signo=True,eta_s=0.15,clip_s=10.0,puerta=3,mask_rel=2,del_s=0.25,del_c=0.25,ema_c=0.05,puerta_pat=5,pat_shuf=0,pat_min=1,vivo=0,n_nec=1,estims=None,costo_a=0.002,A_ini=1.0,val_esc=0,nec_shuf=0,hereda_nec=1,tabla=None,eta_pred=0.0,ema_pred=0.05,clip_e=3.0,k_sorp=0.0,crit_exp=0.5,reproduccion=0,rep_mide=1,rep_X=500,rep_umbral=1.0,rep_coste=0.0,rep_nec=0,rep_cuello=0,rep2=0,rep2_regalo=600,muerte_real=0,hereda='nada',dote=0.6,cola_max=200,h1=0,alma=None,alma_muertes=0,nodo=1,conectado=0,nodo_k=20,nodo_lee=50,miedo_n=5,miedo_R=-3.0,d_dote=0.1,d_umbral=0.1,menu='abcdef',nodo_baraja=0,nodo_rel=0,con_desde=0,rep_acum=0,f9=0,nodo_via=0,nodo_or=0,sesgo_fijo=0.0,f9c=0):
    # ---- LAS GUARDIAS DEL ORIGINAL, VERBATIM (incluidas las que APAGAN perillas detras de su maestra)
    if n_nec>1 and not vivo: raise SystemExit('MUNDO VIVO: n_nec>1 exige vivo=1 (la mordida debe tener consecuencia vectorial)')
    if not reproduccion: rep_mide=0; rep_nec=0; rep_cuello=0; rep_coste=0.0
    if not reproduccion: rep2=0
    if rep2 and not rep_mide: raise SystemExit('REP2: rep2=1 exige rep_mide=1 (la ventana es el nacimiento)')
    if not reproduccion: muerte_real=0; h1=0; hereda='nada'
    if not muerte_real: alma=None; alma_muertes=0
    if alma is not None and not callable(alma): raise SystemExit('ALMA: alma es None o un invocable (resumen -> {curita, motivo})')
    if alma is not None and not alma_muertes: raise SystemExit('ALMA: alma exige alma_muertes>=1 (la serie de cuerpos ES la medida)')
    if alma is not None and not nodo and conectado: raise SystemExit('ALMA: conectado=1 exige nodo=1 (no hay a que conectarse)')
    if alma is None: nodo_baraja=0
    if alma is not None and (not menu or len(set(menu))!=len(menu) or any(_z0 not in 'abcdef' for _z0 in menu)):
        raise SystemExit(f'ALMA2: menu={menu!r} debe ser un subconjunto no vacio y sin repeticiones de abcdef')
    if alma is not None and nodo_baraja and not nodo: raise SystemExit('ALMA2: nodo_baraja=1 exige nodo=1 (no hay nodo que barajar)')
    if alma is None: nodo_rel=0; con_desde=0; f9=0
    if alma is None: nodo_via=0; nodo_or=0; f9c=0   # F9C: perillas del NODO y sus medidas, detras de la maestra
    if not f9: f9c=0   # F9C: las medidas pa/pn viven en el dict f9 (solo lectura, detras de f9)
    if nodo_via not in (0,1,2): raise SystemExit('F9C: nodo_via es 0 (solo la via lenta = organismo_f9), 1 (las DOS vias CON evidencia = organismo_f9b) o 2 (las dos vias SIN evidencia: leer llena la memoria, morder abre la puerta)')
    if nodo_via and not nodo: raise SystemExit('F9C: nodo_via exige nodo=1 (no hay nodo que leer)')
    if nodo_or and not nodo: raise SystemExit('F9C: nodo_or exige nodo=1 (el oraculo sustituye el CONTENIDO del nodo, no el canal)')
    if nodo_or and not vivo: raise SystemExit('F9C: nodo_or exige vivo=1 (la tabla verdadera es la del mundo vivo: ABCD x 2 necesidades)')
    if not rep_mide: rep_acum=0
    if nodo_rel not in (0,1,2,3): raise SystemExit('F9: nodo_rel es 0 (recencia), 1 (relevancia viva), 2 (azar sobre todo el nodo) o 3 (relevancia fija)')
    if nodo_rel and not nodo: raise SystemExit('F9: nodo_rel exige nodo=1 (no hay nodo que leer)')
    if con_desde and not nodo: raise SystemExit('F9: con_desde exige nodo=1 (no hay a que conectarse)')
    if con_desde and conectado: raise SystemExit('F9: con_desde y conectado=1 son EXCLUYENTES (o nace conectado o se conecta despues)')
    if f9 and not (h1 and rep2): raise SystemExit('F9: f9=1 exige h1=1 y rep2=1 (las medidas del cuerpo usan su nacimiento y su vida)')
    if muerte_real and not h1: raise SystemExit('H1: muerte_real=1 exige h1=1 (los diagnosticos del linaje SON la medida)')
    if h1 and not rep2: raise SystemExit('H1: h1=1 exige rep2=1 (la marca del nacimiento y las vidas vienen de rep2)')
    if hereda not in ('nada','M1','M1+pares','baraja'): raise SystemExit("H1: hereda es 'nada', 'M1', 'M1+pares' o 'baraja'")
    if hereda!='nada' and not muerte_real: raise SystemExit('H1: hereda exige muerte_real=1 (sin muerte no hay parto)')
    if muerte_real and rep_coste: raise SystemExit('H1: dote y rep_coste son EXCLUYENTES (el padre paga una sola vez)')
    if muerte_real and not (0<dote<rep_umbral): raise SystemExit('H1: la dote debe cumplir 0 < dote < rep_umbral (pagarla no puede matar al padre)')
    if rep_nec and n_nec!=3: raise SystemExit('REP: rep_nec=1 exige n_nec=3 (la tercera fila de valor ES la necesidad de reproducirse)')
    if n_nec==3 and not rep_nec: raise SystemExit('REP: n_nec=3 exige rep_nec=1 (sin la tercera necesidad no hay tercera componente de dS)')
    if n_nec>3: raise SystemExit('REP: n_nec maximo 3')
    if rep_cuello not in (0,1,2): raise SystemExit('REP: rep_cuello es 0, 1 (CUELLO) o 2 (CUELLO_MIN)')
    if rep_cuello and (n_nec!=2 or rep_nec): raise SystemExit('REP: rep_cuello (control) exige n_nec=2 y rep_nec=0')
    if rep_cuello==2 and puerta is None: raise SystemExit('REP: rep_cuello=2 exige puerta (con puerta=None el valor de la boca entra en el aprendizaje)')
    # ---- LO QUE ESTE GEMELO NO COMPILA (aborta en vez de callar)
    if log_cada: raise ValueError("organismo_f9_rapido: log_cada no esta compilado; usa organismo_f9 para eso")
    if puerta is not None and puerta < 0: raise ValueError("organismo_f9_rapido: puerta negativa no se admite (usa None o >= 0)")
    if nec_shuf: raise ValueError("organismo_f9_rapido: nec_shuf no esta compilado (usa organismo_f9)")
    if eta_pred or k_sorp: raise ValueError("organismo_f9_rapido: el predictor de dS (eta_pred/k_sorp) no esta compilado (usa organismo_f9)")
    if n_nec == 3 or rep_nec: raise ValueError("organismo_f9_rapido: la tercera necesidad no esta compilada (usa organismo_f9)")
    if hereda in ('M1+pares', 'baraja'): raise ValueError(f"organismo_f9_rapido: hereda={hereda!r} no esta compilado (usa organismo_f9)")
    if vivo and (invertir_en is not None or nuevo is not None):
        raise ValueError("organismo_f9_rapido: invertir_en/nuevo con vivo=1 no esta compilado (usa organismo_f9)")
    if nuevo is not None and nuevo_val not in ('comida', 'veneno'):
        raise ValueError("organismo_f9_rapido: nuevo_val debe ser comida o veneno")
    if cola_max < 1: raise ValueError("organismo_f9_rapido: cola_max debe ser >= 1")
    rng=np.random.default_rng(seed)
    # --- inicializacion: EXACTAMENTE las lineas del original (mismo flujo de azar)
    Wl=rng.uniform(.1,.4,(2,9)); KW=np.zeros((NKMAX,6)); activa=np.zeros(NKMAX,bool); KW[:NK]=rng.uniform(0,1,(NK,6)); activa[:NK]=True
    def code(P):
        v=KW@P; v=np.where(activa,v,-1e9); return set(np.argsort(v)[-K:])
    objetivo_AB=0 if solap_AB is None else solap_AB
    if solap_AB: KW[:solap_AB]=0; KW[:solap_AB,0]=5.0
    cond=lambda: len(code(PAT['A'])&code(PAT['B']))==objetivo_AB and (nuevo is None or solap_B is None or (len(code(PAT[nuevo])&code(PAT['B']))==solap_B and len(code(PAT[nuevo])&code(PAT['A']))==0))
    while not cond(): KW[objetivo_AB:NK]=rng.uniform(0,1,(NK-objetivo_AB,6))
    if invertir_en is not None and nuevo is not None and nuevo_en < invertir_en:
        raise ValueError("el original no admite nuevo antes de invertir (val se reemplaza)")
    # --- el mundo: tipos, valencias y la tabla de efectos
    tipos_py = (list(estims) if estims else ['A', 'B'])
    tipos = np.zeros(len(tipos_py) + 2, np.int64)
    for _i, _k in enumerate(tipos_py): tipos[_i] = NOMBRES.index(_k)
    ntipos = len(tipos_py)
    _EF = dict(EFECTO) if tabla is None else dict(tabla)
    EFEC = np.zeros((4, 2))
    for _i, _v in enumerate(VALENCIAS):
        if _v in _EF: EFEC[_i, 0] = float(_EF[_v][0]); EFEC[_i, 1] = float(_EF[_v][1])
    val_py = (dict(VAL_VIVO) if vivo else {'A': 'comida', 'B': 'veneno'})
    valc = np.full(4, -1, np.int64)
    for _k, _v in val_py.items(): valc[NOMBRES.index(_k)] = VALENCIAS.index(_v)
    # --- los rng PROPIOS (ERR-60), creados en Python y pasados al bucle
    _rrel = np.random.default_rng(870000+1000000*seed) if (alma is not None and nodo_rel==2) else np.random.default_rng(0)
    _rbn = np.random.default_rng(860000+1000000*seed) if (alma is not None and nodo_baraja) else np.random.default_rng(0)
    _CTX['alma'] = alma; _CTX['menu'] = menu; _CTX['motivo'] = ''; _CTX['cur'] = []
    hereda_i = HEREDA.index(hereda)
    sal = _bucle(rng, _rrel, _rbn, int(T), bool(learn),
                 -1 if invertir_en is None else int(invertir_en), -1 if nuevo is None else NOMBRES.index(nuevo),
                 int(nuevo_en), 0 if nuevo_val == 'comida' else 1,
                 float(eta), float(tau_e), float(alpha), float(hambre_boca), float(aversion), float(costo), int(nobj),
                 bool(plast), float(theta), float(ema), float(paso), float(lam), int(memoria_rechazo), bool(mu_norm),
                 bool(div_signo), float(eta_s), float(clip_s), -1 if puerta is None else int(puerta),
                 Wl, KW, activa, PATM,
                 int(mask_rel), float(del_s), float(del_c), float(ema_c), int(puerta_pat), int(pat_shuf), int(pat_min),
                 int(bool(vivo)), int(n_nec), tipos, int(ntipos), float(costo_a), float(A_ini), int(val_esc),
                 int(hereda_nec), EFEC, valc, float(crit_exp),
                 int(rep_mide), int(rep_X), float(rep_umbral), float(rep_coste), int(rep_cuello), int(rep2), int(rep2_regalo),
                 int(muerte_real), int(hereda_i), float(dote), int(cola_max), int(h1), alma is not None, int(alma_muertes),
                 int(nodo), int(conectado), int(nodo_k), int(nodo_lee), int(miedo_n), float(miedo_R), float(d_dote), float(d_umbral),
                 int(nodo_baraja), int(nodo_rel), int(con_desde), int(rep_acum), int(f9),
                 int(seed), int(objetivo_AB), 0 if not solap_AB else int(solap_AB), -1 if solap_B is None else int(solap_B),
                 int(nodo_via), int(nodo_or), float(sesgo_fijo), int(f9c))
    (Wp, Wn, Wps, Wns, KW, activa, splits, st_t, st_k, mord, vis, sobre, llegadas, sin_objetivo,
     deaths, err_max, t_conflicto, t_techo, n_techo, ncod_key, ncod_cnt, n_cod, desborde,
     _nm, Ag, _mnec, _exp, _enc, _bxor, _exor, _sbE,
     _desc, _pv, _dq, _tdesc, _bsac, _dsac,
     _dreg, _vidas, _tmu,
     _nac, _fund, _dfund, _dpv, _dv, _vh, _org, _svid, _colan, _cdes, _tfund, _nbar,
     _nmu, _con, dote_f, umbral_f, hereda_f, _Tef, _inerte,
     nd_P, nd_R, nd_N, nd_n, _nbar_n, _ldiv, _nlec, _p1, _c1, _tok, _ncu, _esfund, _chk, _nvia, _fam9, _gpa, _gpn) = sal
    if _chk:
        raise RuntimeError('organismo_f9_rapido: el registro de curitas devolvio algo distinto de 0')
    if desborde:
        raise RuntimeError(f"organismo_f9_rapido: mas de {NCODMAX} codigos distintos (sube NCODMAX)")
    hereda_fin = HEREDA[int(hereda_f)]
    # --- las lecturas finales, con las mismas expresiones del original
    def kenyon(P): k=np.zeros(NKMAX); k[list(code(P))]=1; return k
    def _clave_py(_k):
        key=0
        for i in np.flatnonzero(_k): key=key*(NKMAX+1)+(int(i)+1)
        return key
    def _ev_py(_k):
        _q=_clave_py(_k); i=-1
        for j in range(int(n_cod)):
            if ncod_key[j]==_q: i=j; break
        if not pat_shuf: return int(ncod_cnt[i]) if i>=0 else 0
        if i<0 or n_cod<2: return 0
        return int(ncod_cnt[(i+1)%int(n_cod)])
    def _fam(_k,_n=None):
        _w=Wp[_nm if _n is None else _n]-Wn[_nm if _n is None else _n]
        if puerta_pat: return _ev_py(_k)>=puerta_pat and int((np.abs(_w[_k>0])>0.2).sum())>=pat_min
        return int((np.abs(_w[_k>0])>0.2).sum())>=puerta
    def valor(P):
        _k=kenyon(P); _f=float((Wp[_nm]-Wn[_nm])@_k); _s=float((Wps[_nm]-Wns[_nm])@P)
        return _f+_s if puerta is None else (_f if _fam(_k) else _s)
    def _vnec(_n,P,_k):
        _f=float((Wp[_n]-Wn[_n])@_k); _s=float((Wps[_n]-Wns[_n])@P)
        return _f+_s if puerta is None else (_f if _fam(_k,_n) else _s)
    W={k:round(valor(PAT[k]),2) for k in PAT}
    W_lenta={k:round(float((Wps[_nm]-Wns[_nm])@PAT[k]),3) for k in PAT}
    comp={k:(round(float(Wp[_nm]@kenyon(PAT[k])),2),round(float(Wn[_nm]@kenyon(PAT[k])),2)) for k in PAT}
    tipos_fin = list(tipos_py) + ([nuevo] if nuevo is not None and int(T) > int(nuevo_en) else [])
    if nuevo is not None and int(T) > int(nuevo_en): val_py = dict(val_py); val_py[nuevo] = nuevo_val
    if invertir_en is not None and int(T) > int(invertir_en): val_py = {'A': 'veneno', 'B': 'comida'}
    _ext = {}
    if vivo:
        _ext = dict(n_nec=n_nec, estims=list(tipos_fin), agua=round(float(Ag),3), muertes_nec=[int(v) for v in _mnec],
                    exp_hasta=[{k: (None if _exp[_n, NOMBRES.index(k)] < 0 else int(_exp[_n, NOMBRES.index(k)])) for k in PAT} for _n in range(n_nec)],
                    exposiciones={k: int(_enc[NOMBRES.index(k)]) for k in PAT},
                    W_nec=[{_k3: round(_vnec(_n, PAT[_k3], kenyon(PAT[_k3])), 2) for _k3 in PAT} for _n in range(n_nec)],
                    xor_mord=[[int(v) for v in _bxor[_n]] for _n in range(n_nec)],
                    xor_enc=[[int(v) for v in _exor[_n]] for _n in range(n_nec)],
                    sorp_nec=[round(float(_x),4) for _x in _sbE])
    if reproduccion:
        _ext.update(descendientes=int(_desc), pasos_viables=int(_pv), desc_q=[int(v) for v in _dq],
                    t_desc=[int(v) for v in _tdesc],
                    sac_mord={k: int(_bsac[NOMBRES.index(k)]) for k in PAT},
                    sac_dec={k: int(_dsac[NOMBRES.index(k)]) for k in PAT},
                    rep=dict(mide=int(rep_mide), X=rep_X, umbral=float(umbral_f), coste=rep_coste,
                             nec=int(rep_nec), cuello=int(rep_cuello)))
    if rep2:
        _ext.update(desc_regalo=int(_dreg), vidas=[int(v) for v in _vidas], vida_final=int(T)-int(_tmu),
                    rep2=dict(regalo=rep2_regalo))
    if h1:
        _ext.update(muerte_real=int(muerte_real), hereda=hereda_fin, dote=float(dote_f),
                    nacimientos=int(_nac), fundadores=int(_fund), desc_fund=int(_dfund),
                    desc_por_vida=[int(v) for v in _dpv]+[int(_dv)], vidas_h1=[int(v) for v in _vh]+[int(T)-int(_tmu)],
                    origen_cuerpo=[int(v) for v in _org]+[0 if _esfund else 1], suma_vidas=int(_svid),
                    cola_final=int(_colan), cola_desborde=int(_cdes), t_fund=[int(v) for v in _tfund],
                    baraja_identidad=int(_nbar),
                    h1=dict(cola_max=cola_max, sem_hijo='700000+1000000*seed+k', sem_baraja='800000+1000000*seed'))
    if alma is not None:
        _ext.update(alma_muertes=alma_muertes, curitas=[list(_c) for _c in _CTX['cur']], nodo_n=int(nd_n),
                    conectado_final=int(_con), dote_final=round(float(dote_f),4), umbral_final=round(float(umbral_f),4),
                    hereda_final=hereda_fin, T_efectivo=int(_Tef), miedo_inerte=int(_inerte),
                    vidas_cuerpo=[int(v) for v in _vh], desc_cuerpo=[int(v) for v in _dpv],
                    nodo_cola=[[[float(z) for z in nd_P[_i]], float(nd_R[_i]), int(nd_N[_i])]
                               for _i in range(max(int(nd_n)-60, 0), int(nd_n))],
                    alma_cfg=dict(nodo=int(nodo), nodo_k=nodo_k, nodo_lee=nodo_lee, miedo_n=miedo_n, miedo_R=miedo_R,
                                  d_dote=d_dote, d_umbral=d_umbral, conectado_ini=int(conectado)))
        _ext.update(alma2=dict(menu=''.join(menu), nodo_baraja=int(nodo_baraja),
                               baraja_nodo_identidad=int(_nbar_n), sem_baraja_nodo='860000+1000000*seed'))
    if alma is not None and f9:
        _ext.update(f9=dict(nodo_rel=int(nodo_rel), con_desde=int(con_desde), lect_div=int(_ldiv), lecturas=int(_nlec),
                            sem_rel='870000+1000000*seed', p1=[int(v) for v in _p1], c1=[int(v) for v in _c1],
                            t_ok=[int(v) for v in _tok], con_cuerpo=[int(v) for v in _ncu]))
    if alma is not None and f9 and nodo_via:
        _ext['f9'].update(nodo_via=int(nodo_via), via_msg=int(_nvia), fam_nac=[int(v) for v in _fam9])
    if alma is not None and f9 and f9c: _ext['f9'].update(pa=int(_gpa), pn=int(_gpn))
    if alma is not None and f9 and nodo_or: _ext['f9'].update(nodo_or=1)
    if sesgo_fijo: _ext.update(sesgo_fijo=float(sesgo_fijo))
    if rep_acum: _ext.update(rep_acum=1)
    _sob = {}; _lle = {}
    for _v in ('veneno', 'comida'):
        _i = VALENCIAS.index(_v); _sob[_v] = [int(x) for x in sobre[_i]]; _lle[_v] = [int(x) for x in llegadas[_i]]
    if vivo:
        for _v in ('agua', 'sal'):
            if _v in [val_py[_t] for _t in tipos_fin]:
                _i = VALENCIAS.index(_v); _sob[_v] = [int(x) for x in sobre[_i]]; _lle[_v] = [int(x) for x in llegadas[_i]]
    return dict(sobre=_sob, llegadas=_lle, sin_objetivo=[int(v) for v in sin_objetivo], memoria_rechazo=memoria_rechazo,
                err_max=float(err_max), t_conflicto=None if t_conflicto<0 else int(t_conflicto),
                t_techo=None if t_techo<0 else int(t_techo), n_techo=int(n_techo),
                split_t=[(int(a),NOMBRES[int(b)]) for a,b in zip(st_t,st_k)],
                mord={k:[int(v) for v in mord[i]] for i,k in enumerate(NOMBRES)},
                vis={k:[int(v) for v in vis[i]] for i,k in enumerate(NOMBRES)},
                W=W,comp=comp,deaths=int(deaths),log=[],splits=int(splits),celdas=int(activa.sum()),
                puerta_pat=puerta_pat,pat_shuf=pat_shuf,pat_min=pat_min,n_cod=int(n_cod),
                solap={'AB':len(code(PAT['A'])&code(PAT['B'])),'nB':len(code(PAT[nuevo])&code(PAT['B'])) if nuevo else None},
                W_lenta=W_lenta,Wps=[round(float(x),3) for x in Wps[_nm]],Wns=[round(float(x),3) for x in Wns[_nm]],**_ext)
