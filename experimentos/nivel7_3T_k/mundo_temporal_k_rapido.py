"""mundo_temporal_k RAPIDO — gemelo COMPILADO (numba) de mundo_temporal_k.py (68736baafe7c8cdb). NO es un mundo nuevo:
misma regla, mismo flujo de azar (rng y rng2), mismas salidas (todas las claves). Existe para correr ~20-80x mas rapido.
Solo vale si es BIT A BIT identico al original: arnes experimentos/nivel7_3T_k/identidad_temporal_rapido.py
(regla: si no es identico, no se usa para confirmar). Mismo modelo que organismo/organismo_v13_rapido.py.

Donde numba y NumPy podian diferir, y como se evita:
  - Generator: se pasan los MISMOS objetos rng y rng2 (seed+100000, canal falso) al bucle compilado.
  - Productos (KW@P, Wb@kc, (Wps-Wns)@P, Wl@x, kj@P, KW[c]@P): numba @ llama al mismo BLAS. Verificado bit a bit
    para NIN in {6,12,18,24,30,36} (ddot, dgemv y filas de una 2D): 0 diferencias en 500 sorteos por tamano.
  - argsort con EMPATES: el orden de NumPy no es reproducible en numba -> si hay empate en la frontera del top-K se
    llama a NumPy (objmode). Sin empate el conjunto top-K es unico.
  - SUMAS LARGAS: este mundo si las tiene (NIN >= 8 desde k=1 en los brazos de 12 columnas): P.sum(), mu[c].sum(),
    np.abs(dist).sum(), np.abs(dist[6:]).sum(). NumPy suma POR PARES desde n >= 8 y numba no. Se reproduce el
    algoritmo exacto de NumPy (`_psum`: 8 acumuladores, bloque 128, mitades multiplo de 8). Verificado bit a bit
    contra np.sum para n in {6,12,18,24,30,36,40,90,128,129,180,270,540,900,1080,3240}: 0 diferencias en 400 sorteos
    por tamano (la suma ingenua falla en 20-98 % de los casos, por eso no se usa).
  - clip/outer/where/concatenate: escritos como bucles elementales (misma aritmetica IEEE).
  - Los snapshots (`hitos`) NO se compilan: el bucle de pasos se compila POR TRAMOS entre hitos y el snapshot se hace
    en Python con las MISMAS funciones del original (code/kenyon/valor_tot/inp/hist_de). Asi `KW[activa,:6].sum()`,
    `KW[idx,6:].sum()`, `np.mean` y `round` son literalmente los de NumPy/Python. El estado (KW, activa, Wp, Wn, Wps,
    Wns, err, mu, Wl, tr, el, objetos, rechazo, contadores) vive en arrays que el tramo compilado muta en sitio.
  - round(): todos los redondeos de la salida (incluido el `ft` de split_t) se hacen en Python, no en numba.
  - enteros: los contadores salen de arrays int64 y se convierten a int() de Python (np.int64 no es JSON-serializable
    y el arnes compara tras ida y vuelta por JSON).
Restriccion: misma firma que el original. NIN = 6 (C1/C1p) o 6*(kprof+1) (C2/C2b/C3/C3C).
"""
import sys, numpy as np
import itertools
from numba import njit, objmode
try: sys.stdout.reconfigure(encoding='utf-8', errors='replace')
except Exception: pass

L = 40; NK = 30; NKMAX = 90; K = 3
PAT = {'A': np.array([1, 1, 0, 1, 0, 0.]), 'B': np.array([1, 0, 1, 0, 1, 0.])}
R_VAL = {'comida': 1.0, 'veneno': -3.0, 'neutro': 0.0}
E_VAL = {'comida': +0.8, 'veneno': -0.4, 'neutro': +0.1}
SIT = [('A', 'A'), ('A', 'B'), ('B', 'A'), ('B', 'B')]   # (actual, anterior)

ARMS = {
    #        nin  temporal_visible  plast  init        canal_falso
    'C1':  dict(nin=6,  plast=False, init='v6',    falso=False),
    'C1p': dict(nin=6,  plast=True,  init='v6',    falso=False),
    'C2':  dict(nin=12, plast=False, init='full',  falso=False),
    'C2b': dict(nin=12, plast=False, init='ciego', falso=False),
    'C3':  dict(nin=12, plast=True,  init='ciego', falso=False),
    'C3C': dict(nin=12, plast=True,  init='ciego', falso=True),
}

NOM = ['A', 'B']                                   # 0 -> 'A', 1 -> 'B' (mismo orden que tipos = ['A','B'])
PATM = np.array([PAT[k] for k in NOM])
PW_BLOCKSIZE = 128


def valor(cur, last):
    """3T-k: last es la historia (h1..hk); manda el slot MAS PROFUNDO. Con k=1 es la regla original."""
    if cur == 'B': return 'neutro'
    hk = last[-1] if isinstance(last, tuple) else last
    return 'comida' if hk == 'B' else 'veneno'


# ---------------------------------------------------------------- piezas compiladas

@njit(cache=True)
def _psum_bloque(a, off, n):
    """Las dos ramas NO recursivas de la suma por pares de NumPy (n <= 128): ingenua bajo 8, 8 acumuladores encima."""
    if n < 8:
        res = 0.
        for i in range(n):
            res += a[off + i]
        return res
    r0 = a[off + 0]; r1 = a[off + 1]; r2 = a[off + 2]; r3 = a[off + 3]
    r4 = a[off + 4]; r5 = a[off + 5]; r6 = a[off + 6]; r7 = a[off + 7]
    i = 8
    lim = n - (n % 8)
    while i < lim:
        r0 += a[off + i + 0]; r1 += a[off + i + 1]; r2 += a[off + i + 2]; r3 += a[off + i + 3]
        r4 += a[off + i + 4]; r5 += a[off + i + 5]; r6 += a[off + i + 6]; r7 += a[off + i + 7]
        i += 8
    res = ((r0 + r1) + (r2 + r3)) + ((r4 + r5) + (r6 + r7))
    while i < n:
        res += a[off + i]; i += 1
    return res


@njit(cache=True)
def _psum(a, off, n):
    """Suma por pares de NumPy, bit a bit, SIN recursion (una funcion njit recursiva corrompe el cache de numba y
    segmenta al releerlo; comprobado). Mismo arbol de sumas: mitades multiplo de 8, hojas de <= 128, izquierda+derecha.
    En este mundo n <= NIN = 36, asi que siempre entra por la hoja; el recorrido explicito esta por generalidad."""
    if n <= PW_BLOCKSIZE:
        return _psum_bloque(a, off, n)
    D = 64
    o_st = np.empty(D, np.int64); n_st = np.empty(D, np.int64); e_st = np.empty(D, np.int64); a_st = np.empty(D)
    top = 0; o_st[0] = off; n_st[0] = n; e_st[0] = 0
    ret = 0.0
    while top >= 0:
        if e_st[top] == 0:
            nn = n_st[top]
            if nn <= PW_BLOCKSIZE:
                ret = _psum_bloque(a, o_st[top], nn); top -= 1; continue
            n2 = nn // 2; n2 -= n2 % 8
            e_st[top] = 1; top += 1
            o_st[top] = o_st[top - 1]; n_st[top] = n2; e_st[top] = 0
        elif e_st[top] == 1:
            a_st[top] = ret
            nn = n_st[top]; n2 = nn // 2; n2 -= n2 % 8
            e_st[top] = 2; top += 1
            o_st[top] = o_st[top - 1] + n2; n_st[top] = nn - n2; e_st[top] = 0
        else:
            ret = a_st[top] + ret; top -= 1
    return ret


@njit(cache=True)
def _code(KW, activa, P):
    """Codigo de Kenyon como vector 0/1: top-K de KW@P entre las celdas activas. Con empate en la frontera manda NumPy."""
    n = activa.shape[0]
    v = KW @ P
    w = np.empty(n)
    for i in range(n):
        w[i] = v[i] if activa[i] else -1e9
    idx = np.argsort(w)
    if w[idx[n - K]] == w[idx[n - K - 1]]:
        with objmode(idx='int64[:]'):
            idx = np.argsort(w)
    out = np.zeros(n)
    for i in range(n - K, n):
        out[idx[i]] = 1.0
    return out


@njit(cache=True)
def _spawn(rng, opos, otip, nobjs, nobj):
    """tipos = ['A','B'] -> 0/1; el sorteo del tipo solo se consume si la posicion no estaba ocupada."""
    while nobjs < nobj:
        x = rng.integers(0, L)
        dup = False
        for i in range(nobjs):
            if opos[i] == x:
                dup = True; break
        if not dup:
            opos[nobjs] = x; otip[nobjs] = rng.integers(0, 2); nobjs += 1
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
    """(d, k, left): el objeto mas cercano en orden de insercion, con la memoria de trabajo de rechazo de v9."""
    best_d = 0; best_k = -1; best_left = False; found = False
    for i in range(nobjs):
        x = opos[i]
        if memoria_rechazo != 0 and rech[x] > t: continue
        dl = (pos - x) % L; dr = (x - pos) % L; d = min(dl, dr)
        if (not found) or d < best_d:
            best_d = d; best_k = otip[i]; best_left = dl < dr; found = True
    if not found:
        for i in range(nobjs):
            x = opos[i]
            dl = (pos - x) % L; dr = (x - pos) % L; d = min(dl, dr)
            if (not found) or d < best_d:
                best_d = d; best_k = otip[i]; best_left = dl < dr; found = True
    return best_d, best_k, best_left


@njit(cache=True)
def _iniciar(rng, opos, otip, nobj):
    return _spawn(rng, opos, otip, 0, nobj)


@njit(cache=True)
def _tramo(rng, rng2, t0, t1, T, learn, eta, tau_e, alpha, hambre_boca, aversion, costo, nobj,
           plast, theta, ema, paso, early, wclip, lam, memoria_rechazo, mu_norm, div_signo, eta_s, clip_s,
           puerta, kprof, falso,
           Wl, KW, activa, Wp, Wn, Wps, Wns, err, mu, el, tr, opos, otip, rech, last,
           n_AB, n_AA, n_B, prevB, nbit, vis, st_t, st_kk, st_prev, st_ft, SI, SF, PATM):
    """Pasos t0..t1-1 del bucle del original. Todo el estado entra y sale por los arrays (mutados en sitio)."""
    nk = activa.shape[0]; NIN = KW.shape[1]
    pos = SI[0]; nobjs = SI[1]; splits = SI[2]; deaths = SI[3]; t_pool = SI[4]; t_techo = SI[5]
    n_techo = SI[6]; nst = SI[7]
    e_AB = SI[8]; e_AA = SI[9]; e_B = SI[10]; e_prevB = SI[11]; e_nbit = SI[12]
    E = SF[0]; Rtot = SF[1]
    q_div = T // 4
    x = np.empty(9); m = np.zeros(2)
    P = np.zeros(NIN); psent = np.zeros(kprof, np.int64)
    dist = np.empty(NIN); kj = np.empty(NIN); adist = np.empty(NIN)
    idxs = np.zeros(K, np.int64)
    for t in range(t0, t1):
        q = min(t // q_div, 3)
        hambre = min(max(1.0 - E, 0.0), 1.0)
        d, k, left = _see(pos, t, opos, otip, nobjs, rech, memoria_rechazo)
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
        d2, _k2, _l2 = _see(pos, t, opos, otip, nobjs, rech, memoria_rechazo)
        Rp = .2 if d2 < d else 0.0
        R = 0.0
        io = _idx_en(opos, nobjs, pos)
        if io >= 0:
            kk = otip[io]
            if falso:
                for i in range(kprof): psent[i] = rng2.integers(0, 2)
            else:
                for i in range(kprof): psent[i] = last[i]
            for j in range(6): P[j] = PATM[kk, j]
            if NIN > 6:
                for h in range(kprof):
                    for j in range(6): P[6 + 6 * h + j] = PATM[psent[h], j]
            kc = _code(KW, activa, P)
            Wb = Wp - Wn
            _wf = Wb @ kc
            _ws = (Wps - Wns) @ P
            nfam = 0
            for i in range(nk):
                if kc[i] > 0 and abs(Wb[i]) > 0.2: nfam += 1
            _wt = (_wf + _ws) if puerta < 0 else (_wf if nfam >= puerta else _ws)
            Vb = alpha * _wt + hambre_boca * hambre + .5
            pb = 1 / (1 + np.exp(-Vb / .3)); mordio = rng.random() < pb
            vis[kk, q] += 1
            if memoria_rechazo != 0 and not mordio: rech[pos] = t + memoria_rechazo
            if mordio:
                hk = last[kprof - 1]
                if kk == 1: R = 0.0; dE = 0.1                    # B -> neutro
                elif hk == 1: R = 1.0; dE = 0.8                  # A con hk = B -> comida
                else: R = -3.0; dE = -0.4                        # A con hk = A -> veneno
                E = min(E + dE, 1.5); Rtot += R
                nbit[q] += 1
                if hk == 1: prevB[q] += 1
                if kk == 0:
                    if hk == 1: n_AB[q] += 1
                    else: n_AA[q] += 1
                else:
                    n_B[q] += 1
                if t < early:
                    e_nbit += 1
                    if hk == 1: e_prevB += 1
                    if kk == 0:
                        if hk == 1: e_AB += 1
                        else: e_AA += 1
                    else: e_B += 1
                for i in range(kprof - 1, 0, -1): last[i] = last[i - 1]
                last[0] = kk
                nobjs = _borrar(opos, otip, nobjs, pos); nobjs = _spawn(rng, opos, otip, nobjs, nobj)
                rech[pos] = -1
                if learn:
                    dlt = (R - _wt) if puerta < 0 else (R - _wf)
                    if eta_s != 0.0:
                        _ds = dlt if puerta < 0 else (R - _ws)
                        if lam != 0.0:
                            for i in range(NIN):
                                if P[i] > 0:
                                    _mcs = min(Wps[i], Wns[i]); Wps[i] = Wps[i] - lam * _mcs; Wns[i] = Wns[i] - lam * _mcs
                                else:
                                    Wps[i] = Wps[i] - lam * 0.0; Wns[i] = Wns[i] - lam * 0.0
                        if _ds > 0:
                            for i in range(NIN): Wps[i] = min(max(Wps[i] + eta_s * _ds * P[i], 0.0), clip_s)
                        else:
                            for i in range(NIN): Wns[i] = min(max(Wns[i] + eta_s * aversion * (-_ds) * P[i], 0.0), clip_s)
                    if lam != 0.0:
                        for i in range(nk):
                            if kc[i] > 0:
                                mcom = min(Wp[i], Wn[i]); Wp[i] -= lam * mcom; Wn[i] -= lam * mcom
                    _trunca = False
                    for i in range(nk):
                        if kc[i] > 0:
                            if dlt > 0:
                                if (Wp[i] + eta * dlt) > wclip: _trunca = True
                            else:
                                if (Wn[i] + eta * aversion * (-dlt)) > wclip: _trunca = True
                    if _trunca:
                        n_techo += 1
                        if t_techo < 0: t_techo = t
                    if dlt > 0:
                        for i in range(nk): Wp[i] = min(max(Wp[i] + eta * dlt * kc[i], 0.0), wclip)
                    else:
                        for i in range(nk): Wn[i] = min(max(Wn[i] + eta * aversion * (-dlt) * kc[i], 0.0), wclip)
                    if plast:
                        nidx = 0
                        for i in range(nk):
                            if kc[i] > 0:
                                idxs[nidx] = i; nidx += 1
                        for a in range(nidx):
                            c = idxs[a]
                            err[c] = (1 - ema) * err[c] + ema * abs(dlt)
                            for j in range(NIN): mu[c, j] = (1 - ema) * mu[c, j] + ema * P[j]
                        sP = _psum(P, 0, NIN)
                        for a in range(nidx):
                            c = idxs[a]
                            libre = -1
                            for i in range(nk):
                                if not activa[i]:
                                    libre = i; break
                            if div_signo:
                                smu = _psum(mu[c], 0, NIN)
                                for j in range(NIN):
                                    dist[j] = P[j] - (mu[c, j] * (sP / max(smu, 1e-9)) if mu_norm else mu[c, j])
                                    kj[j] = min(max(KW[c, j] * (1 - 0.05) + paso * dist[j], 0.0), 5.0) * (1.0 if P[j] > 0 else 0.0)
                                if Wb[c] * R < 0 and abs(Wb[c]) > 0.2 and (kj @ P) > (KW[c] @ P) and libre >= 0:
                                    for j in range(NIN): adist[j] = abs(dist[j])
                                    a1 = _psum(adist, 0, NIN)
                                    ft = (_psum(adist, 6, NIN - 6) / a1) if (a1 > 0 and NIN > 6) else 0.0
                                    jn = libre; activa[jn] = True
                                    for j in range(NIN): KW[jn, j] = kj[j]
                                    if R > 0:
                                        Wp[jn] = Wp[c]; Wn[jn] = 0.; Wp[c] = 0.
                                    else:
                                        Wn[jn] = Wn[c]; Wp[jn] = 0.; Wn[c] = 0.
                                    for j in range(NIN): mu[jn, j] = P[j] * (smu / sP)
                                    err[c] = 0.; err[jn] = 0.; splits += 1
                                    st_t[nst] = t; st_kk[nst] = kk; st_ft[nst] = ft
                                    for i in range(kprof): st_prev[nst, i] = psent[i]
                                    nst += 1
                                    lib2 = -1
                                    for i in range(nk):
                                        if not activa[i]:
                                            lib2 = i; break
                                    if lib2 < 0 and t_pool < 0: t_pool = t
                            elif err[c] > theta and libre >= 0:
                                jn = libre; activa[jn] = True
                                smu = _psum(mu[c], 0, NIN)
                                for j in range(NIN):
                                    dist[j] = P[j] - (mu[c, j] * (sP / max(smu, 1e-9)) if mu_norm else mu[c, j])
                                    adist[j] = abs(dist[j])
                                a1 = _psum(adist, 0, NIN)
                                ft = (_psum(adist, 6, NIN - 6) / a1) if (a1 > 0 and NIN > 6) else 0.0
                                for j in range(NIN):
                                    KW[jn, j] = min(max(KW[c, j] + paso * dist[j], 0.0), 5.0)
                                    KW[c, j] = min(max(KW[c, j] - paso * dist[j], 0.0), 5.0)
                                Wp[jn] = Wp[c]; Wn[jn] = Wn[c]
                                for j in range(NIN): mu[jn, j] = mu[c, j]
                                err[c] = 0.; err[jn] = 0.; splits += 1
                                st_t[nst] = t; st_kk[nst] = kk; st_ft[nst] = ft
                                for i in range(kprof): st_prev[nst, i] = psent[i]
                                nst += 1
                                lib2 = -1
                                for i in range(nk):
                                    if not activa[i]:
                                        lib2 = i; break
                                if lib2 < 0 and t_pool < 0: t_pool = t
        E -= costo
        if rng.random() < .003 and nobjs > 0:
            i = rng.integers(0, nobjs); _dx = opos[i]
            nobjs = _borrar(opos, otip, nobjs, _dx); nobjs = _spawn(rng, opos, otip, nobjs, nobj); rech[_dx] = -1
        if learn:
            s = eta * (1 + 2 * hambre) * (max(R, 0.0) + Rp)
            for i in range(2):
                for j in range(9): Wl[i, j] = min(max(Wl[i, j] + s * el[i, j], 0.0), 1.5)
        if E <= 0:
            deaths += 1; E = .6; pos = rng.integers(0, L)
    SI[0] = pos; SI[1] = nobjs; SI[2] = splits; SI[3] = deaths; SI[4] = t_pool; SI[5] = t_techo
    SI[6] = n_techo; SI[7] = nst
    SI[8] = e_AB; SI[9] = e_AA; SI[10] = e_B; SI[11] = e_prevB; SI[12] = e_nbit
    SF[0] = E; SF[1] = Rtot


# ---------------------------------------------------------------- envoltorio en Python (identico al original)

def run(seed, arm='C1', T=100000, learn=True, eta=.03, tau_e=.85, alpha=1.2,
        hambre_boca=2.0, aversion=1.0, costo=.002, nobj=4,
        theta=0.6, ema=0.02, paso=0.5, early=5000, nkmax=NKMAX, wclip=3.0, lam=0.05, memoria_rechazo=20, mu_norm=False, div_signo=False, eta_s=0.0, clip_s=3.0, puerta=None, kprof=1):
    cfg = ARMS[arm]; NIN = cfg['nin'] if cfg['nin'] == 6 else 6 * (kprof + 1); plast = cfg['plast']; falso = cfg['falso']   # 3T-k
    FILL = list(itertools.product('AB', repeat=kprof - 1))   # rellenos de los distractores (k=1: uno, vacio)
    def hist_de(p, fill=None): return (tuple('A' * (kprof - 1)) if fill is None else tuple(fill)) + (p,)   # h1..hk con hk = p
    rng = np.random.default_rng(seed)
    rng2 = np.random.default_rng(seed + 100000)        # canal falso, flujo separado

    Wl = rng.uniform(.1, .4, (2, 9))
    KW = np.zeros((nkmax, NIN)); activa = np.zeros(nkmax, bool); activa[:NK] = True

    def inp(cur, prev):
        if NIN == 6: return PAT[cur]
        h = prev if isinstance(prev, tuple) else hist_de(prev)   # una letra = slot profundo con relleno canonico 'A'
        return np.concatenate([PAT[cur]] + [PAT[x] for x in h])

    def code(P):
        v = KW @ P; v = np.where(activa, v, -1e9); return set(np.argsort(v)[-K:])

    # --- inicializacion (muestreo por rechazo): EXACTAMENTE las lineas del original ---
    if cfg['init'] == 'full':                     # C2: 12 columnas aleatorias
        KW[:NK] = rng.uniform(0, 1, (NK, NIN))
        while len(code(inp('A', 'A')) & code(inp('A', 'B'))) != 0:
            KW[:NK] = rng.uniform(0, 1, (NK, NIN))
    else:                                         # C1/C1p/C2b/C3/C3C: mismo flujo que v6
        KW[:NK, :6] = rng.uniform(0, 1, (NK, 6))
        while len(code(inp('A', 'A')) & code(inp('B', 'B'))) != 0:
            KW[:NK, :6] = rng.uniform(0, 1, (NK, 6))

    def kenyon(P):
        k = np.zeros(nkmax); k[list(code(P))] = 1; return k

    Wp = np.zeros(nkmax); Wn = np.zeros(nkmax)
    Wps = np.zeros(NIN); Wns = np.zeros(NIN)
    def valor_tot(P):
        _k = kenyon(P); _f = float((Wp - Wn) @ _k); _s = float((Wps - Wns) @ P)
        return _f + _s if puerta is None else (_f if int((np.abs((Wp - Wn)[_k > 0]) > 0.2).sum()) >= puerta else _s)
    err = np.zeros(nkmax); mu = np.zeros((nkmax, NIN))
    el = np.zeros_like(Wl); tr = np.zeros(9)

    # --- estado del bucle en arrays (el tramo compilado lo muta en sitio) ---
    opos = np.full(nobj, -1, np.int64); otip = np.full(nobj, -1, np.int64)
    rech = np.full(L, -1, np.int64)
    last = np.ones(kprof, np.int64)                  # ('B',)*kprof
    n_AB = np.zeros(4, np.int64); n_AA = np.zeros(4, np.int64); n_B = np.zeros(4, np.int64)
    prevB = np.zeros(4, np.int64); nbit = np.zeros(4, np.int64); visa = np.zeros((2, 4), np.int64)
    st_t = np.zeros(nkmax, np.int64); st_kk = np.zeros(nkmax, np.int64)
    st_prev = np.zeros((nkmax, kprof), np.int64); st_ft = np.zeros(nkmax)
    SI = np.zeros(13, np.int64); SF = np.zeros(2)
    SI[4] = -1; SI[5] = -1                           # t_pool, t_techo
    SF[0] = 1.0                                      # E
    SI[1] = _iniciar(rng, opos, otip, int(nobj))     # spawn() inicial

    def snapshot(t, splits):
        cods = {f'{c}|{p}': code(inp(c, p)) for c, p in SIT}   # relleno canonico (k=1: exacto)
        _ov = lambda c: [len(code(inp(c, hist_de('A', f))) & code(inp(c, hist_de('B', f)))) for f in FILL]
        _sA = _ov('A'); _sB = _ov('B')
        union = set().union(*cods.values())
        wi = float(KW[activa, :6].sum()); wt = float(KW[activa, 6:].sum()) if NIN > 6 else 0.0
        idx = sorted(union)
        wi_c = float(KW[idx, :6].sum()); wt_c = float(KW[idx, 6:].sum()) if NIN > 6 else 0.0
        return dict(t=t, solap_A=(_sA[0] if kprof == 1 else round(float(np.mean(_sA)), 3)),
                    solap_B=(_sB[0] if kprof == 1 else round(float(np.mean(_sB)), 3)),
                    w_inst=round(wi, 3), w_temp=round(wt, 3),
                    rho=round(wt / (wt + wi), 4) if (wt + wi) > 0 else 0.0,
                    w_inst_cod=round(wi_c, 3), w_temp_cod=round(wt_c, 3),
                    rho_cod=round(wt_c / (wt_c + wi_c), 4) if (wt_c + wi_c) > 0 else 0.0,
                    celdas=int(activa.sum()), splits=splits,
                    W={f'{c}|{p}': (round(valor_tot(inp(c, p)), 3) if kprof == 1 else round(float(np.mean([valor_tot(inp(c, hist_de(p, f))) for f in FILL])), 3)) for c, p in SIT})   # 3T-k: media sobre rellenos

    args = (int(T), bool(learn), float(eta), float(tau_e), float(alpha), float(hambre_boca), float(aversion),
            float(costo), int(nobj), bool(plast), float(theta), float(ema), float(paso), int(early), float(wclip),
            float(lam), int(memoria_rechazo), bool(mu_norm), bool(div_signo), float(eta_s), float(clip_s),
            -1 if puerta is None else int(puerta), int(kprof), bool(falso))
    estado = (Wl, KW, activa, Wp, Wn, Wps, Wns, err, mu, el, tr, opos, otip, rech, last,
              n_AB, n_AA, n_B, prevB, nbit, visa, st_t, st_kk, st_prev, st_ft, SI, SF, PATM)

    hitos = {0, T // 4, T // 2, 3 * T // 4}
    snaps = []; prev_t = 0
    for h in sorted(hitos):                          # el original hace snapshot al ENTRAR en el paso t del hito
        if h > prev_t:
            _tramo(rng, rng2, int(prev_t), int(h), *args, *estado); prev_t = h
        snaps.append(snapshot(h, int(SI[2])))
    _tramo(rng, rng2, int(prev_t), int(T), *args, *estado)

    snaps.append(snapshot(T, int(SI[2])))
    fin = snaps[-1]
    splits = int(SI[2]); deaths = int(SI[3]); nst = int(SI[7]); E = float(SF[0]); Rtot = float(SF[1])
    t_pool = None if SI[4] < 0 else int(SI[4]); t_techo = None if SI[5] < 0 else int(SI[5]); n_techo = int(SI[6])
    n_AB = [int(v) for v in n_AB]; n_AA = [int(v) for v in n_AA]; n_B = [int(v) for v in n_B]
    prevB = [int(v) for v in prevB]; nbit = [int(v) for v in nbit]
    vis = {'A': [int(v) for v in visa[0]], 'B': [int(v) for v in visa[1]]}
    e_AB = int(SI[8]); e_AA = int(SI[9]); e_B = int(SI[10]); e_prevB = int(SI[11]); e_nbit = int(SI[12])
    split_t = [(int(st_t[i]), NOM[int(st_kk[i])],
                (NOM[int(st_prev[i, 0])] if kprof == 1 else tuple(NOM[int(st_prev[i, j])] for j in range(kprof))),
                round(float(st_ft[i]), 3)) for i in range(nst)]
    acc = [ (n_AB[i] / (n_AB[i] + n_AA[i])) if (n_AB[i] + n_AA[i]) > 0 else None for i in range(4) ]
    base = [ (prevB[i] / nbit[i]) if nbit[i] > 0 else None for i in range(4) ]
    lift = [ (round(acc[i] - base[i], 4) if acc[i] is not None and base[i] is not None else None) for i in range(4) ]
    e_acc = (e_AB / (e_AB + e_AA)) if (e_AB + e_AA) > 0 else None
    e_base = (e_prevB / e_nbit) if e_nbit > 0 else None
    return dict(
        seed=seed, arm=arm, k=kprof,
        W=fin['W'], sep=round(fin['W']['A|B'] - fin['W']['A|A'], 3),
        comp={f'{c}|{p}': (round(float(Wp @ kenyon(inp(c, p))), 3),
                           round(float(Wn @ kenyon(inp(c, p))), 3)) for c, p in SIT},
        solap_A=fin['solap_A'], solap_B=fin['solap_B'],
        solap_A_q=[s['solap_A'] for s in snaps],
        rho_q=[s['rho'] for s in snaps], rho_cod_q=[s['rho_cod'] for s in snaps],
        w_temp_q=[s['w_temp'] for s in snaps], w_inst_q=[s['w_inst'] for s in snaps],
        n_AB=n_AB, n_AA=n_AA, n_B=n_B, vis=vis, nbit=nbit, prevB=prevB,
        acc=[round(a, 4) if a is not None else None for a in acc],
        base=[round(b, 4) if b is not None else None for b in base], lift=lift,
        early=dict(n_AB=e_AB, n_AA=e_AA, n_B=e_B, nbit=e_nbit,
                   acc=round(e_acc, 4) if e_acc is not None else None,
                   base=round(e_base, 4) if e_base is not None else None,
                   lift=round(e_acc - e_base, 4) if (e_acc is not None and e_base is not None) else None),
        splits=splits, celdas=fin['celdas'], t_pool=t_pool, split_t=split_t,
        deaths=deaths, Rtot=round(Rtot, 2), E_fin=round(float(E), 3), snaps=snaps,
        t_techo=t_techo, n_techo=n_techo, lam=lam)


if __name__ == '__main__':
    import json
    print(json.dumps({k: run(1, k, T=20000)['W'] for k in ARMS}, indent=1))
