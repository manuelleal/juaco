"""
Organismo v14c RAPIDO — gemelo COMPILADO (numba) de experimentos/nivel10_composicion_v14/organismo_v14c.py.
NO es un organismo nuevo: misma regla, mismo flujo de azar, mismas salidas (TODAS las claves, incluidas las
nuevas puerta_pat/pat_shuf/pat_min/n_cod). Existe para correr ~50-80x mas rapido. Solo vale si es BIT A BIT
identico a organismo_v14c: arnes identidad_v14c_rapido.py (regla 9 de EQUIPO.md: si no es identico, no se usa).

Partida: organismo/organismo_v13_rapido.py (gemelo del tronco v13, 72/72 + 180/180). Sobre el se anaden los
DOS mecanismos de v14c, exactamente como los inyectan sus constructores:

  D) HIJA DISPERSA POR RELEVANCIA (mask_rel, del_s, del_c, ema_c; nivel7_hija_dispersa/construye_v13D.py)
     - estado nuevo: mup/mun (NKMAX x 6) y zp/zn (NKMAX): medias de P condicionadas al signo de R (EMA ema_c
       con normalizador), actualizadas en el mismo bloque de plasticidad que err/mu;
     - al NACER la hija, con mask_rel==2 y zp[c]>1e-6 y zn[c]>1e-6, la mascara deja de ser (P>0) y pasa a ser
       rel = (P>0) & ( |mp-mn| > del_s  |  min(mp,mn) > 1-del_c ), con mp=mup[c]/zp[c], mn=mun[c]/zn[c];
     - la hija HEREDA mup/mun/zp/zn de la madre.
     Con mask_rel != 2 la mascara es (P>0): v13 EXACTO.

  B) PUERTA POR EVIDENCIA DEL CODIGO EXACTO (puerta_pat, pat_shuf, pat_min; nivel4_puerta_codigo/construye_puerta_codigo.py)
     - estado nuevo: ncod (contador de MORDIDAS por codigo exacto) y el orden de primera aparicion;
     - la puerta (_fam) pasa de "celdas consolidadas >= puerta" a "evidencia del codigo >= puerta_pat Y celdas
       consolidadas >= pat_min"; con pat_shuf la evidencia leida es la del codigo VECINO en el orden de
       aparicion (control). Con puerta_pat==0 la puerta es la de v13: v13 EXACTO.
     - actua en el RUTEO (valor de la boca y valor final), NO en el aprendizaje.

Donde numba y NumPy podian diferir, y como se evita (lo mismo que en el gemelo del tronco, mas lo nuevo):
  - Generator: se pasa el MISMO objeto rng al bucle compilado.
  - argsort con EMPATES en la frontera del top-K -> objmode con NumPy (_code, heredado del tronco).
  - sumas largas (n>=8): no hay ninguna nueva. Lo que anade v14c son operaciones ELEMENTALES sobre 6 pixeles
    (mup/mun/zp/zn, mascara de relevancia) y CONTEOS enteros (evidencia del codigo). El unico `@` nuevo no existe.
  - el dict ncod (clave = frozenset de los 3 indices del codigo) se representa como un entero unico por codigo
    (indices ascendentes en base NKMAX+1, la misma biyeccion que np.flatnonzero) en dos arrays paralelos que
    conservan el ORDEN DE PRIMERA APARICION, que es lo que lee pat_shuf. Busqueda lineal (los codigos distintos
    de una corrida son pocas decenas: <= 4 patrones x (splits+1), y splits <= NKMAX-NK = 60).
  - ninguna funcion es recursiva (cache=True).

Restriccion: log_cada debe ser None (el log por pasos no esta compilado). El resto de la firma es la de v14c.
El gemelo del MUNDO DE REGLA es OTRO archivo (organismo_v14gc.py tiene su propia firma con mundo/regla/
fase2_en/sonda_final y sus propias claves): aqui NO se compila.
"""
import numpy as np
from numba import njit, objmode

L=40; NK=30; NKMAX=90; K=3
NCODMAX=4096   # cota amplia para los codigos distintos de una corrida (ver cabecera); si se pasa, run() aborta
PAT={'A':np.array([1,1,0,1,0,0.]),'B':np.array([1,0,1,0,1,0.]),'C':np.array([0,1,1,0,0,1.]),'D':np.array([0,0,1,0,1,1.])}
R_VAL={'comida':1.0,'veneno':-3.0}; E_VAL={'comida':+0.8,'veneno':-0.4}
NOMBRES=['A','B','C','D']
PATM=np.array([PAT[k] for k in NOMBRES])


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
    """Indice del codigo en el orden de PRIMERA APARICION (lo que recorre _ord en el original), o -1."""
    for i in range(n_cod):
        if ncod_key[i] == key:
            return i
    return -1


@njit(cache=True)
def _ev(ncod_key, ncod_cnt, n_cod, key, pat_shuf):
    """B: la evidencia que LEE la puerta: la propia, o (control pat_shuf) la del codigo vecino en el orden de aparicion."""
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
    """B: la puerta. puerta_pat != 0 -> evidencia del codigo exacto; si no, celdas consolidadas (v13 EXACTO)."""
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
    """del objs[x] conservando el orden de insercion del dict del tronco."""
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
def _bucle(rng, T, learn, invertir_en, nuevo_idx, nuevo_en, nuevo_valc, eta, tau_e, alpha, hambre_boca, aversion, costo, nobj,
           plast, theta, ema, paso, lam, memoria_rechazo, mu_norm, div_signo, eta_s, clip_s, puerta, Wl, KW, activa, PATM,
           mask_rel, del_s, del_c, ema_c, puerta_pat, pat_shuf, pat_min):
    Wp = np.zeros(NKMAX); Wn = np.zeros(NKMAX); err = np.zeros(NKMAX); mu = np.zeros((NKMAX, 6)); splits = 0
    el = np.zeros((2, 9)); tr = np.zeros(9)
    Wps = np.zeros(6); Wns = np.zeros(6)
    ncod_key = np.zeros(NCODMAX, np.int64); ncod_cnt = np.zeros(NCODMAX, np.int64); n_cod = 0; desborde = 0   # B
    mup = np.zeros((NKMAX, 6)); mun = np.zeros((NKMAX, 6)); zp = np.zeros(NKMAX); zn = np.zeros(NKMAX)        # D
    umb_c = 1.0 - del_c   # D: el umbral de la rama "contexto", calculado una vez (como en el original)
    pos = 0; E = 1.0
    valc = np.zeros(4, np.int64); valc[0] = 1; valc[1] = -1          # A comida, B veneno
    err_max = 0.0; t_conflicto = -1; t_techo = -1; n_techo = 0
    rech = np.full(L, -1, np.int64); prev_on = -1
    sobre = np.zeros((2, 4), np.int64); llegadas = np.zeros((2, 4), np.int64); sin_objetivo = np.zeros(4, np.int64)   # fila 0 veneno, 1 comida
    tipos = np.zeros(3, np.int64); tipos[0] = 0; tipos[1] = 1; ntipos = 2
    opos = np.full(nobj, -1, np.int64); otip = np.full(nobj, -1, np.int64); nobjs = 0
    nobjs = _spawn(rng, opos, otip, nobjs, nobj, tipos, ntipos)
    deaths = 0
    mord = np.zeros((4, 4), np.int64); vis = np.zeros((4, 4), np.int64)
    st_t = np.zeros(NKMAX, np.int64); st_k = np.zeros(NKMAX, np.int64); nst = 0
    q_div = T // 4
    x = np.empty(9); m = np.zeros(2); kc = np.zeros(NKMAX)
    for t in range(T):
        if invertir_en >= 0 and t == invertir_en:
            valc[0] = -1; valc[1] = 1
        if nuevo_idx >= 0 and t == nuevo_en:
            tipos[ntipos] = nuevo_idx; ntipos += 1; valc[nuevo_idx] = nuevo_valc
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
            kk = otip[io]; P = PATM[kk]; kc = _code(KW, activa, P); Wb = Wp - Wn; _wf = Wb @ kc; _ws = (Wps - Wns) @ P
            if puerta < 0:
                _wt = _wf + _ws
            else:
                _wt = _wf if _famil(Wb, kc, puerta, puerta_pat, pat_min, pat_shuf, ncod_key, ncod_cnt, n_cod) else _ws
            Vb = alpha * _wt + hambre_boca * hambre + .5; pb = 1 / (1 + np.exp(-Vb / .3)); mordio = rng.random() < pb
            vis[kk, q] += 1
            fila = 1 if valc[kk] == 1 else 0
            sobre[fila, q] += 1; llegadas[fila, q] += 1 if prev_on != pos else 0
            if memoria_rechazo > 0 and not mordio: rech[pos] = t + memoria_rechazo
            if mordio:
                R = 1.0 if valc[kk] == 1 else -3.0; E = min(E + (0.8 if valc[kk] == 1 else -0.4), 1.5); mord[kk, q] += 1
                _ky = _clave(kc); _ic = _pos_cod(ncod_key, n_cod, _ky)   # B: evidencia del codigo exacto
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
                                    _mcs = min(Wps[i], Wns[i]); Wps[i] = Wps[i] - lam * _mcs; Wns[i] = Wns[i] - lam * _mcs
                                else:
                                    Wps[i] = Wps[i] - lam * 0.0; Wns[i] = Wns[i] - lam * 0.0
                        if _ds > 0:
                            for i in range(6): Wps[i] = min(max(Wps[i] + eta_s * _ds * P[i], 0.0), clip_s)
                        else:
                            for i in range(6): Wns[i] = min(max(Wns[i] + eta_s * aversion * (-_ds) * P[i], 0.0), clip_s)
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
                                disp = mask_rel == 2 and zp[c] > 1e-6 and zn[c] > 1e-6   # D: HIJA DISPERSA (contexto O discriminador)
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
                                        Wp[jn] = Wp[c]; Wn[jn] = 0.; Wp[c] = 0.
                                    else:
                                        Wn[jn] = Wn[c]; Wp[jn] = 0.; Wn[c] = 0.
                                    for j in range(6): mu[jn, j] = P[j] * (smu / sP)
                                    err[c] = 0.0; err[jn] = 0.0; splits += 1; st_t[nst] = t; st_k[nst] = kk; nst += 1
                                    for j in range(6):   # D: la hija hereda las medias condicionadas
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
            err_max, t_conflicto, t_techo, n_techo, ncod_key[:n_cod], ncod_cnt[:n_cod], n_cod, desborde)


def run(seed,T=100000,learn=True,invertir_en=None,nuevo=None,nuevo_en=50000,nuevo_val='veneno',solap_B=None,
        eta=.03,tau_e=.85,alpha=1.2,hambre_boca=2.0,aversion=1.0,costo=.002,nobj=4,log_cada=None,plast=True,theta=0.6,ema=0.02,paso=0.5,solap_AB=None,lam=0.05,memoria_rechazo=20,mu_norm=True,div_signo=True,eta_s=0.015,clip_s=3.0,puerta=3,mask_rel=0,del_s=0.25,del_c=0.25,ema_c=0.05,puerta_pat=0,pat_shuf=0,pat_min=0):
    if log_cada:
        raise ValueError("organismo_v14c_rapido: log_cada no esta compilado; usa organismo_v14c para eso")
    if puerta is not None and puerta < 0:   # H1 del revisor (heredado del gemelo del tronco): el centinela -1 es None
        raise ValueError("organismo_v14c_rapido: puerta negativa no se admite (usa None o >= 0)")
    if nuevo is not None and nuevo_val not in ('comida', 'veneno'):   # H4 del revisor: el original falla con KeyError; el gemelo no debe callar
        raise ValueError("organismo_v14c_rapido: nuevo_val debe ser comida o veneno")
    rng=np.random.default_rng(seed)
    # --- inicializacion: EXACTAMENTE las lineas del original (mismo flujo de azar) ---
    Wl=rng.uniform(.1,.4,(2,9)); KW=np.zeros((NKMAX,6)); activa=np.zeros(NKMAX,bool); KW[:NK]=rng.uniform(0,1,(NK,6)); activa[:NK]=True
    def code(P):
        v=KW@P; v=np.where(activa,v,-1e9); return set(np.argsort(v)[-K:])
    objetivo_AB=0 if solap_AB is None else solap_AB
    if solap_AB: KW[:solap_AB]=0; KW[:solap_AB,0]=5.0
    cond=lambda: len(code(PAT['A'])&code(PAT['B']))==objetivo_AB and (nuevo is None or solap_B is None or (len(code(PAT[nuevo])&code(PAT['B']))==solap_B and len(code(PAT[nuevo])&code(PAT['A']))==0))
    while not cond(): KW[objetivo_AB:NK]=rng.uniform(0,1,(NK-objetivo_AB,6))
    if invertir_en is not None and nuevo is not None and nuevo_en < invertir_en:
        raise ValueError("el original no admite nuevo antes de invertir (val se reemplaza)")
    (Wp, Wn, Wps, Wns, KW, activa, splits, st_t, st_k, mord, vis, sobre, llegadas, sin_objetivo, deaths, err_max,
     t_conflicto, t_techo, n_techo, ncod_key, ncod_cnt, n_cod, desborde) = _bucle(
        rng, int(T), bool(learn), -1 if invertir_en is None else int(invertir_en), -1 if nuevo is None else NOMBRES.index(nuevo), int(nuevo_en),
        1 if nuevo_val == 'comida' else -1, float(eta), float(tau_e), float(alpha), float(hambre_boca), float(aversion), float(costo), int(nobj),
        bool(plast), float(theta), float(ema), float(paso), float(lam), int(memoria_rechazo), bool(mu_norm), bool(div_signo), float(eta_s), float(clip_s),
        -1 if puerta is None else int(puerta), Wl, KW, activa, PATM,
        int(mask_rel), float(del_s), float(del_c), float(ema_c), int(puerta_pat), int(pat_shuf), int(pat_min))
    if desborde:
        raise RuntimeError(f"organismo_v14c_rapido: mas de {NCODMAX} codigos distintos (sube NCODMAX)")
    def kenyon(P): k=np.zeros(NKMAX); k[list(code(P))]=1; return k
    def _clave_py(_k):
        key=0
        for i in np.flatnonzero(_k): key=key*(NKMAX+1)+(int(i)+1)
        return key
    def _ev_py(_k):   # B: la misma lectura que _ev del original (orden de primera aparicion)
        _q=_clave_py(_k); i=-1
        for j in range(n_cod):
            if ncod_key[j]==_q: i=j; break
        if not pat_shuf: return int(ncod_cnt[i]) if i>=0 else 0
        if i<0 or n_cod<2: return 0
        return int(ncod_cnt[(i+1)%n_cod])
    def _fam(_k):
        if puerta_pat: return _ev_py(_k)>=puerta_pat and int((np.abs((Wp-Wn)[_k>0])>0.2).sum())>=pat_min
        return int((np.abs((Wp-Wn)[_k>0])>0.2).sum())>=puerta
    def valor(P):
        _k=kenyon(P); _f=float((Wp-Wn)@_k); _s=float((Wps-Wns)@P)
        return _f+_s if puerta is None else (_f if _fam(_k) else _s)
    W={k:round(valor(PAT[k]),2) for k in PAT}
    W_lenta={k:round(float((Wps-Wns)@PAT[k]),3) for k in PAT}
    comp={k:(round(float(Wp@kenyon(PAT[k])),2),round(float(Wn@kenyon(PAT[k])),2)) for k in PAT}
    return dict(sobre={'veneno':[int(v) for v in sobre[0]],'comida':[int(v) for v in sobre[1]]},
                llegadas={'veneno':[int(v) for v in llegadas[0]],'comida':[int(v) for v in llegadas[1]]},
                sin_objetivo=[int(v) for v in sin_objetivo],memoria_rechazo=memoria_rechazo,err_max=float(err_max),
                t_conflicto=None if t_conflicto<0 else int(t_conflicto),t_techo=None if t_techo<0 else int(t_techo),n_techo=int(n_techo),
                split_t=[(int(a),NOMBRES[int(b)]) for a,b in zip(st_t,st_k)],
                mord={k:[int(v) for v in mord[i]] for i,k in enumerate(NOMBRES)},vis={k:[int(v) for v in vis[i]] for i,k in enumerate(NOMBRES)},
                W=W,comp=comp,deaths=int(deaths),log=[],splits=int(splits),celdas=int(activa.sum()),
                puerta_pat=puerta_pat,pat_shuf=pat_shuf,pat_min=pat_min,n_cod=int(n_cod),
                solap={'AB':len(code(PAT['A'])&code(PAT['B'])),'nB':len(code(PAT[nuevo])&code(PAT['B'])) if nuevo else None},
                W_lenta=W_lenta,Wps=[round(float(x),3) for x in Wps],Wns=[round(float(x),3) for x in Wns])
