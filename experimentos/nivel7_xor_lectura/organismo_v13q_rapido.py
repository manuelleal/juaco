"""
organismo_v13q RAPIDO — gemelo COMPILADO (numba) de experimentos/nivel7_xor_lectura/organismo_v13q.py.
NO es un organismo nuevo: misma regla, mismo flujo de azar, mismas salidas (todas las claves). Existe para correr
~50x mas rapido. Solo vale si es BIT A BIT identico al original: arnes identidad_v13q_rapido.py
(regla: si el arnes no da 100 %, este archivo no se usa para confirmar nada).

Origen: organismo_v13q.py (0b59eb03858df3a8, bloque 3b) = organismo_v13g.py (mundo de regla, sonda a priori W_apriori,
primer encuentro, sonda final) + knob `lectura` de la via lenta ('lineal' | 'cuadratica' | 'random15') + las dos lecturas
puras de la sonda (W_lenta_apriori, familiar_apriori). Modelo del gemelo: organismo/organismo_v13_rapido.py
(gemelo del tronco, 72/72). Se repiten AQUI sus mismas decisiones:
  - Generator: se crea en Python y se pasa el MISMO objeto rng al bucle compilado (uniform/normal/random/integers
    dan el mismo flujo). La inicializacion (Wl, KW, el re-sorteo de cond()) es linea por linea la del original.
  - Productos con @ (KW@P, Wb@kc, Wl@x, (Wps-Wns)@phi): numba llama al mismo BLAS. Verificado tambien para NF=21.
  - NINGUNA suma de >= 8 elementos con .sum() dentro del bucle (NumPy suma por pares desde n=8): solo sumas de 6 y conteos.
  - argsort con EMPATES: si hay empate en la frontera del top-K se delega en NumPy (objmode); sin empate el conjunto
    top-K es unico. clip / outer / where / minimum: escritos como bucles elementales (misma aritmetica IEEE).
  - Estructuras del original como arrays: `objs` (dict, ORDEN DE INSERCION) -> opos/otip + _borrar que desplaza;
    `_rech` (dict) -> vector de L enteros; `tipos` (lista que crece con `nuevo` y con `test`) -> vector + ntipos.
  - Lo que NO cambia de sitio: split_regla vive en Python (RNG propio, no toca el del organismo); la tabla de 64x15
    bits de `random15` (RNG propio seed+900000) se precalcula en Python y entra al bucle como PHIM; la sonda final de
    64 patrones y las lecturas de cierre (W, W_lenta, comp, W_final, sonda, codigos_fin) se hacen en Python con
    EXACTAMENTE el codigo del original.
  - La SONDA de fase2_en tampoco se reimplementa: en t==fase2_en el bucle solo saca una FOTO de (Wp, Wn, Wps, Wns, KW,
    activa) y las cuatro lecturas (W_apriori, W_lenta_apriori, familiar_apriori, codigos_f2) se calculan despues en
    Python con las lineas literales del original sobre esa foto. Asi la sonda usa el argsort de NumPy, no el de numba.
  - phi(P) es fija por patron: se precalcula PHIM (npat x NF) en Python. Con lectura='lineal' PHIM == PATM.

Restricciones (no cubiertas, el original manda):
  - log_cada debe ser None (el log por pasos no esta compilado).
  - invertir_en solo tiene sentido con mundo='AB' (en el original `val` se REEMPLAZA por {'A','B'}: en el mundo de
    regla la corrida siguiente revienta con KeyError). Aqui se levanta ValueError en vez de dejar que reviente.
  - `nuevo` antes de `invertir_en`: el original pierde val[nuevo] al reemplazar el dict (mismo ValueError que el
    gemelo del tronco).
"""
import numpy as np
from numba import njit, objmode

L = 40; NK = 30; NKMAX = 90; K = 3
PAT = {'A': np.array([1, 1, 0, 1, 0, 0.]), 'B': np.array([1, 0, 1, 0, 1, 0.]), 'C': np.array([0, 1, 1, 0, 0, 1.]), 'D': np.array([0, 0, 1, 0, 1, 1.])}
R_VAL = {'comida': 1.0, 'veneno': -3.0}; E_VAL = {'comida': +0.8, 'veneno': -0.4}

import itertools   # v9g


def patrones_regla():
    """v9g: los C(6,3)=20 patrones binarios de 6 px con exactamente 3 px activos. (identico a organismo_v13q)"""
    pats = {}
    for combo in itertools.combinations(range(6), 3):
        v = np.zeros(6); v[list(combo)] = 1.
        pats[''.join('1' if v[j] else '0' for j in range(6))] = v
    return pats


def split_regla(seed, regla):
    """v9g: valencias por regla y particion train/test con RNG propios (no tocan el RNG del organismo). (identico)"""
    pats = patrones_regla(); nombres = sorted(pats)
    if regla == 'px0':
        vr = {k: ('comida' if k[0] == '1' else 'veneno') for k in nombres}; ntr = (5, 5)
    elif regla == 'xor01':
        vr = {k: ('comida' if k[0] != k[1] else 'veneno') for k in nombres}; ntr = (4, 4)
    elif regla == 'azar':
        r0 = np.random.default_rng(30000 + seed); perm = r0.permutation(len(nombres))
        com = set(nombres[i] for i in perm[:10])
        vr = {k: ('comida' if k in com else 'veneno') for k in nombres}; ntr = (5, 5)
    else:
        raise ValueError(regla)
    food = [k for k in nombres if vr[k] == 'comida']; pois = [k for k in nombres if vr[k] == 'veneno']
    r = np.random.default_rng(10000 + seed); fi = r.permutation(len(food)); pi = r.permutation(len(pois))
    food = [food[i] for i in fi]; pois = [pois[i] for i in pi]
    tren = sorted(food[:ntr[0]] + pois[:ntr[1]]); test = sorted(food[ntr[0]:] + pois[ntr[1]:])
    return pats, tren, test, vr


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


@njit(cache=True)
def _bucle(rng, T, learn, invertir_en, iA, iB, nuevo_idx, nuevo_en, nuevo_valc, f2_on, fase2_en, test_idx,
           eta, tau_e, alpha, hambre_boca, aversion, costo, nobj, plast, theta, ema, paso, lam, memoria_rechazo,
           mu_norm, div_signo, eta_s, clip_s, puerta, Wl, KW, activa, PATM, PHIM, valc, tipos, ntipos0):
    npat = PATM.shape[0]; NF = PHIM.shape[1]
    Wp = np.zeros(NKMAX); Wn = np.zeros(NKMAX); err = np.zeros(NKMAX); mu = np.zeros((NKMAX, 6)); splits = 0
    el = np.zeros((2, 9)); tr = np.zeros(9)
    Wps = np.zeros(NF); Wns = np.zeros(NF)                                  # xor: la via lenta vive sobre phi(P), NF = 6 o 21
    pos = 0; E = 1.0
    err_max = 0.0; t_conflicto = -1; t_techo = -1; n_techo = 0
    rech = np.full(L, -1, np.int64); prev_on = -1
    sobre = np.zeros((2, 4), np.int64); llegadas = np.zeros((2, 4), np.int64); sin_objetivo = np.zeros(4, np.int64)   # fila 0 veneno, 1 comida
    ntipos = ntipos0
    opos = np.full(nobj, -1, np.int64); otip = np.full(nobj, -1, np.int64); nobjs = 0
    nobjs = _spawn(rng, opos, otip, nobjs, nobj, tipos, ntipos)
    deaths = 0
    mord = np.zeros((npat, 4), np.int64); vis = np.zeros((npat, 4), np.int64)
    st_t = np.zeros(NKMAX, np.int64); st_k = np.zeros(NKMAX, np.int64); nst = 0
    Wp_f2 = np.zeros(NKMAX); Wn_f2 = np.zeros(NKMAX); Wps_f2 = np.zeros(NF); Wns_f2 = np.zeros(NF)   # v13g/3b: FOTO de la sonda
    KW_f2 = np.zeros((NKMAX, 6)); act_f2 = np.zeros(NKMAX, np.bool_); f2_ok = False                  # (las lecturas se hacen en Python)
    pr_on = np.zeros(npat, np.bool_); pr_set = np.zeros(npat, np.bool_)            # v13g: primer encuentro
    pr_t = np.zeros(npat, np.int64); pr_W = np.zeros(npat); pr_pb = np.zeros(npat)
    pr_h = np.zeros(npat); pr_m = np.zeros(npat, np.bool_)
    q_div = T // 4
    x = np.empty(9); m = np.zeros(2); kc = np.zeros(NKMAX)
    for t in range(T):
        if invertir_en >= 0 and t == invertir_en:
            valc[iA] = -1; valc[iB] = 1
        if nuevo_idx >= 0 and t == nuevo_en:
            tipos[ntipos] = nuevo_idx; ntipos += 1; valc[nuevo_idx] = nuevo_valc
        if f2_on and t == fase2_en:                                         # v13g/3b: foto para la sonda a priori y entrada de los de test
            for i in range(NKMAX):
                Wp_f2[i] = Wp[i]; Wn_f2[i] = Wn[i]; act_f2[i] = activa[i]
                for j in range(6): KW_f2[i, j] = KW[i, j]
            for i in range(NF):
                Wps_f2[i] = Wps[i]; Wns_f2[i] = Wns[i]
            for a in range(test_idx.shape[0]):
                tipos[ntipos] = test_idx[a]; ntipos += 1; pr_on[test_idx[a]] = True
            f2_ok = True
        q = min(t // q_div, 3)
        hambre = min(max(1 - E, 0.0), 1.0)
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
            kk = otip[io]; P = PATM[kk]; ph = PHIM[kk]                       # xor: phi(P_[kk]) precalculado
            kc = _code(KW, activa, P); Wb = Wp - Wn; _wf = Wb @ kc; _ws = (Wps - Wns) @ ph
            nfam = 0
            for i in range(NKMAX):
                if kc[i] > 0 and abs(Wb[i]) > 0.2: nfam += 1
            _wt = (_wf + _ws) if puerta < 0 else (_wf if nfam >= puerta else _ws)
            Vb = alpha * _wt + hambre_boca * hambre + .5; pb = 1 / (1 + np.exp(-Vb / .3)); mordio = rng.random() < pb
            vis[kk, q] += 1
            fila = 1 if valc[kk] == 1 else 0
            sobre[fila, q] += 1; llegadas[fila, q] += 1 if prev_on != pos else 0
            if pr_on[kk] and not pr_set[kk]:                                 # v13g: primer encuentro de un patron de test
                pr_set[kk] = True; pr_t[kk] = t; pr_W[kk] = _wt; pr_pb[kk] = pb; pr_h[kk] = hambre; pr_m[kk] = mordio
            if memoria_rechazo > 0 and not mordio: rech[pos] = t + memoria_rechazo
            if mordio:
                R = 1.0 if valc[kk] == 1 else -3.0; E = min(E + (0.8 if valc[kk] == 1 else -0.4), 1.5); mord[kk, q] += 1
                nobjs = _borrar(opos, otip, nobjs, pos); nobjs = _spawn(rng, opos, otip, nobjs, nobj, tipos, ntipos)
                rech[pos] = -1
                if learn:
                    dlt = (R - _wt) if puerta < 0 else (R - _wf)
                    if eta_s != 0.0:
                        _ds = dlt if puerta < 0 else (R - _ws)
                        if lam != 0.0:
                            for i in range(NF):
                                if ph[i] > 0:
                                    _mcs = min(Wps[i], Wns[i]); Wps[i] = Wps[i] - lam * _mcs; Wns[i] = Wns[i] - lam * _mcs
                                else:
                                    Wps[i] = Wps[i] - lam * 0.0; Wns[i] = Wns[i] - lam * 0.0
                        if _ds > 0:
                            for i in range(NF): Wps[i] = min(max(Wps[i] + eta_s * _ds * ph[i], 0.0), clip_s)
                        else:
                            for i in range(NF): Wns[i] = min(max(Wns[i] + eta_s * aversion * (-_ds) * ph[i], 0.0), clip_s)
                    if lam != 0.0:
                        for i in range(NKMAX):
                            if kc[i] > 0:
                                mcom = min(Wp[i], Wn[i]); Wp[i] -= lam * mcom; Wn[i] -= lam * mcom
                    _trunca = False
                    for i in range(NKMAX):
                        if kc[i] > 0:
                            if dlt > 0:
                                if (Wp[i] + eta * dlt) > 3.0: _trunca = True
                            else:
                                if (Wn[i] + eta * aversion * (-dlt)) > 3.0: _trunca = True
                    if _trunca:
                        n_techo += 1
                        if t_techo < 0: t_techo = t
                    if dlt > 0:
                        for i in range(NKMAX): Wp[i] = min(max(Wp[i] + eta * dlt * kc[i], 0.0), 3.0)
                    else:
                        for i in range(NKMAX): Wn[i] = min(max(Wn[i] + eta * aversion * (-dlt) * kc[i], 0.0), 3.0)
                    if t_conflicto < 0:
                        for i in range(NKMAX):
                            if kc[i] > 0 and min(Wp[i], Wn[i]) > 0:
                                t_conflicto = t; break
                    if plast:
                        nidx = 0; idxs = np.zeros(K, np.int64)
                        for i in range(NKMAX):
                            if kc[i] > 0:
                                idxs[nidx] = i; nidx += 1
                        for a in range(nidx):
                            c = idxs[a]; err[c] = (1 - ema) * err[c] + ema * abs(dlt)
                            for j in range(6): mu[c, j] = (1 - ema) * mu[c, j] + ema * P[j]
                            if err[c] > err_max: err_max = err[c]
                        sP = 0.0
                        for j in range(6): sP += P[j]
                        for a in range(nidx):
                            c = idxs[a]
                            if div_signo:
                                smu = 0.0
                                for j in range(6): smu += mu[c, j]
                                dist = np.empty(6); kj = np.empty(6)
                                for j in range(6):
                                    dist[j] = P[j] - (mu[c, j] * (sP / max(smu, 1e-9)) if mu_norm else mu[c, j])
                                    kj[j] = min(max(KW[c, j] * (1 - 0.05) + paso * dist[j], 0.0), 5.0) * (1.0 if P[j] > 0 else 0.0)
                                libre = -1
                                for i in range(NKMAX):
                                    if not activa[i]:
                                        libre = i; break
                                if Wb[c] * R < 0 and abs(Wb[c]) > 0.2 and (kj @ P) > (KW[c] @ P) and libre >= 0:
                                    jn = libre; activa[jn] = True
                                    for j in range(6): KW[jn, j] = kj[j]
                                    if R > 0:
                                        Wp[jn] = Wp[c]; Wn[jn] = 0.; Wp[c] = 0.
                                    else:
                                        Wn[jn] = Wn[c]; Wp[jn] = 0.; Wn[c] = 0.
                                    for j in range(6): mu[jn, j] = P[j] * (smu / sP)
                                    err[c] = 0.0; err[jn] = 0.0; splits += 1; st_t[nst] = t; st_k[nst] = kk; nst += 1
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
                                    Wp[jn] = Wp[c]; Wn[jn] = Wn[c]
                                    for j in range(6): mu[jn, j] = mu[c, j]
                                    err[c] = 0.0; err[jn] = 0.0; splits += 1; st_t[nst] = t; st_k[nst] = kk; nst += 1
        prev_on = pos if _idx_en(opos, nobjs, pos) >= 0 else -1
        E -= costo
        if rng.random() < .003 and nobjs > 0:
            i = rng.integers(0, nobjs); _dx = opos[i]
            nobjs = _borrar(opos, otip, nobjs, _dx); nobjs = _spawn(rng, opos, otip, nobjs, nobj, tipos, ntipos); rech[_dx] = -1
        if learn:
            s = eta * (1 + 2 * hambre) * (max(R, 0.0) + Rp)
            for i in range(2):
                for j in range(9): Wl[i, j] = min(max(Wl[i, j] + s * el[i, j], 0.0), 1.5)
        if E <= 0:
            deaths += 1; E = .6; pos = rng.integers(0, L)
    return (Wp, Wn, Wps, Wns, KW, activa, splits, st_t[:nst], st_k[:nst], mord, vis, sobre, llegadas, sin_objetivo, deaths,
            err_max, t_conflicto, t_techo, n_techo, Wp_f2, Wn_f2, Wps_f2, Wns_f2, KW_f2, act_f2, f2_ok,
            pr_set, pr_t, pr_W, pr_pb, pr_h, pr_m)


def run(seed,T=100000,learn=True,invertir_en=None,nuevo=None,nuevo_en=50000,nuevo_val='veneno',solap_B=None,
        eta=.03,tau_e=.85,alpha=1.2,hambre_boca=2.0,aversion=1.0,costo=.002,nobj=4,log_cada=None,plast=True,theta=0.6,ema=0.02,paso=0.5,solap_AB=None,lam=0.05,memoria_rechazo=20,mu_norm=True,div_signo=True,eta_s=0.0,clip_s=3.0,puerta=None,mundo='AB',regla='px0',fase2_en=None,sonda_final=False,lectura='lineal'):
    if log_cada:
        raise ValueError("organismo_v13q_rapido: log_cada no esta compilado; usa organismo_v13q para eso")
    if mundo=='AB': P_=PAT; tren=['A','B']; test=[]   # v13g: con 'AB' es v13 exacto
    else: P_,tren,test,val_regla=split_regla(seed,regla); fase2_en=T//2 if fase2_en is None else fase2_en
    rng=np.random.default_rng(seed)
    # --- inicializacion: EXACTAMENTE las lineas del original (mismo flujo de azar) ---
    Wl=rng.uniform(.1,.4,(2,9)); KW=np.zeros((NKMAX,6)); activa=np.zeros(NKMAX,bool); KW[:NK]=rng.uniform(0,1,(NK,6)); activa[:NK]=True
    def code(P):
        v=KW@P; v=np.where(activa,v,-1e9); return set(np.argsort(v)[-K:])
    objetivo_AB=0 if solap_AB is None else solap_AB
    if solap_AB: KW[:solap_AB]=0; KW[:solap_AB,0]=5.0
    cond=lambda: len(code(P_['A'])&code(P_['B']))==objetivo_AB and (nuevo is None or solap_B is None or (len(code(P_[nuevo])&code(P_['B']))==solap_B and len(code(P_[nuevo])&code(P_['A']))==0))
    while mundo=='AB' and not cond(): KW[objetivo_AB:NK]=rng.uniform(0,1,(NK-objetivo_AB,6))
    _NF=6 if lectura=='lineal' else 21   # xor: lineal = 6 px; cuadratica = 6 px + 15 productos de pares; random15 = 6 px + 15 bits fijos al azar por patron
    _IJ=[(i,j) for i in range(6) for j in range(i+1,6)]
    _R15={}
    if lectura=='random15':
        _rr=np.random.default_rng(seed+900000)   # RNG propio: no toca el del organismo
        for _n in range(64):
            _Pb=tuple(float((_n>>(5-_j))&1) for _j in range(6)); _R15[_Pb]=_rr.integers(0,2,15).astype(float)
    def phi(P):
        if lectura=='lineal': return P
        if lectura=='cuadratica': return np.concatenate([P,[P[i]*P[j] for i,j in _IJ]])
        return np.concatenate([P,_R15[tuple(float(v) for v in P)]])
    # --- lo que el bucle compilado necesita como arrays ---
    NOMS=list(P_)                                                  # orden de insercion del dict del original
    IDX={k:i for i,k in enumerate(NOMS)}; npat=len(NOMS)
    PATM=np.array([P_[k] for k in NOMS], float)
    PHIM=np.array([np.asarray(phi(P_[k]), float) for k in NOMS], float)   # phi es fija por patron
    val={'A':'comida','B':'veneno'} if mundo=='AB' else dict(val_regla)
    valc=np.zeros(npat,np.int64)
    for k,v in val.items(): valc[IDX[k]] = 1 if v=='comida' else -1
    tipos=np.zeros(npat+2,np.int64)
    for i,k in enumerate(tren): tipos[i]=IDX[k]
    ntipos0=len(tren)
    test_idx=np.array([IDX[k] for k in test],np.int64) if test else np.zeros(0,np.int64)
    if invertir_en is not None and mundo != 'AB':
        raise ValueError("el original solo invierte en mundo='AB' (val se reemplaza por {'A','B'} y el mundo de regla revienta)")
    if invertir_en is not None and nuevo is not None and nuevo_en < invertir_en:
        raise ValueError("el original no admite nuevo antes de invertir (val se reemplaza)")
    (Wp, Wn, Wps, Wns, KW, activa, splits, st_t, st_k, mord, vis, sobre, llegadas, sin_objetivo, deaths, err_max,
     t_conflicto, t_techo, n_techo, _Wp2, _Wn2, _Wps2, _Wns2, _KW2, _act2, f2_ok, pr_set, pr_t, pr_W, pr_pb, pr_h, pr_m) = _bucle(
        rng, int(T), bool(learn), -1 if invertir_en is None else int(invertir_en),
        IDX.get('A', -1), IDX.get('B', -1), -1 if nuevo is None else IDX[nuevo], int(nuevo_en),
        1 if nuevo_val == 'comida' else -1, bool(mundo != 'AB'), -1 if fase2_en is None else int(fase2_en), test_idx,
        float(eta), float(tau_e), float(alpha), float(hambre_boca), float(aversion), float(costo), int(nobj),
        bool(plast), float(theta), float(ema), float(paso), float(lam), int(memoria_rechazo), bool(mu_norm),
        bool(div_signo), float(eta_s), float(clip_s), -1 if puerta is None else int(puerta),
        Wl, KW, activa, PATM, PHIM, valc, tipos, int(ntipos0))
    # --- lecturas de cierre: EXACTAMENTE el codigo del original ---
    def kenyon(P): k=np.zeros(NKMAX); k[list(code(P))]=1; return k
    def valor(P):   # v13: el valor que usa la boca
        _k=kenyon(P); _f=float((Wp-Wn)@_k); _s=float((Wps-Wns)@phi(P))
        return _f+_s if puerta is None else (_f if int((np.abs((Wp-Wn)[_k>0])>0.2).sum())>=puerta else _s)
    _sonda=None; _cod_fin=None
    if sonda_final:   # v13g: valor TOTAL y codigo de los 64 patrones al final (lectura)
        _sonda={}
        for _n in range(64):
            _P=np.array([(_n>>(5-_j))&1 for _j in range(6)],float); _nm=''.join(str(int(_v)) for _v in _P)
            _sonda[_nm]=dict(W=valor(_P),codigo=sorted(int(_i) for _i in code(_P)))
        _cod_fin={_k:sorted(int(_i) for _i in code(P_[_k])) for _k in P_}
    W={k:round(valor(P_[k]),2) for k in P_}   # v13: valor total
    W_lenta={k:round(float((Wps-Wns)@phi(P_[k])),3) for k in P_}   # v13: lectura de la via lenta sola (xor: phi)
    comp={k:(round(float(Wp@kenyon(P_[k])),2),round(float(Wn@kenyon(P_[k])),2)) for k in P_}
    # --- la sonda de fase2_en, sobre la FOTO que saco el bucle. Alcance propio para no tapar el code/valor de cierre:
    #     dentro son EXACTAMENTE las lineas del original, con el estado del instante t==fase2_en ---
    def _sonda_f2():
        Wp, Wn, Wps, Wns, KW, activa = _Wp2, _Wn2, _Wps2, _Wns2, _KW2, _act2
        def code(P):
            v=KW@P; v=np.where(activa,v,-1e9); return set(np.argsort(v)[-K:])
        def kenyon(P): k=np.zeros(NKMAX); k[list(code(P))]=1; return k
        def valor(P):
            _k=kenyon(P); _f=float((Wp-Wn)@_k); _s=float((Wps-Wns)@phi(P))
            return _f+_s if puerta is None else (_f if int((np.abs((Wp-Wn)[_k>0])>0.2).sum())>=puerta else _s)
        return ({_k:valor(P_[_k]) for _k in P_},
                {_k:float((Wps-Wns)@phi(P_[_k])) for _k in P_},   # 3b: la via lenta sola
                {_k:(bool(int((np.abs((Wp-Wn)[kenyon(P_[_k])>0])>0.2).sum())>=puerta) if puerta is not None else False) for _k in P_},   # 3b: ¿la puerta lee la rapida?
                {_k:sorted(int(_i) for _i in code(P_[_k])) for _k in P_})
    W_apriori=W_lenta_apriori=familiar_apriori=codigos_f2=None   # v13g/3b
    if f2_ok: W_apriori, W_lenta_apriori, familiar_apriori, codigos_f2 = _sonda_f2()
    primer={} if not f2_ok else {k:(dict(t=int(pr_t[IDX[k]]),W=float(pr_W[IDX[k]]),pb=float(pr_pb[IDX[k]]),
                                        hambre=float(pr_h[IDX[k]]),mordio=bool(pr_m[IDX[k]])) if pr_set[IDX[k]] else None)
                                  for k in test}
    return dict(sobre={'veneno':[int(v) for v in sobre[0]],'comida':[int(v) for v in sobre[1]]},
                llegadas={'veneno':[int(v) for v in llegadas[0]],'comida':[int(v) for v in llegadas[1]]},
                sin_objetivo=[int(v) for v in sin_objetivo],memoria_rechazo=memoria_rechazo,err_max=float(err_max),
                t_conflicto=None if t_conflicto<0 else int(t_conflicto),t_techo=None if t_techo<0 else int(t_techo),n_techo=int(n_techo),
                split_t=[(int(a),NOMS[int(b)]) for a,b in zip(st_t,st_k)],
                mord={k:[int(v) for v in mord[IDX[k]]] for k in P_},vis={k:[int(v) for v in vis[IDX[k]]] for k in P_},
                W=W,comp=comp,deaths=int(deaths),log=[],splits=int(splits),celdas=int(activa.sum()),
                solap=None if mundo!='AB' else {'AB':len(code(P_['A'])&code(P_['B'])),'nB':len(code(P_[nuevo])&code(P_['B'])) if nuevo else None},
                W_lenta=W_lenta,Wps=[round(float(x),3) for x in Wps],Wns=[round(float(x),3) for x in Wns],
                mundo=mundo,regla=regla,tren=tren,test=test,W_apriori=W_apriori,W_lenta_apriori=W_lenta_apriori,familiar_apriori=familiar_apriori,codigos_f2=codigos_f2,primer=primer,
                W_final=({_k:valor(P_[_k]) for _k in P_} if mundo!='AB' else None),sonda=_sonda,codigos_fin=_cod_fin)
