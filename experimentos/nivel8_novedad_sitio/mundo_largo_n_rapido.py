"""
mundo_largo_n RAPIDO — gemelo COMPILADO (numba) de experimentos/nivel8_novedad_sitio/mundo_largo_n.py, que es
mundo_largo (pool de patrones + inyeccion + cambio de regla + lecturas por bloque) + novedad de sitio. NO es un mundo
nuevo: misma regla, mismo flujo de azar, mismas salidas (todas las claves). Lleva las perillas de los tres mundos:
  gamma_N=0                      -> mundo_largo EXACTO
  pool=None,T_nuevo=None,
  invertir_largo=None,gamma_N=0  -> mundo_mapa EXACTO (y con r_vis/sitios/usa_M apagados, organismo_v13)
Solo vale si es BIT A BIT identico: arnes experimentos/nivel8_novedad_sitio/identidad_largo_rapido.py.
Modelo: organismo/organismo_v13_rapido.py y experimentos/nivel6_mapa/mundo_mapa_rapido.py.

Identidad, punto por punto (regla 9 de registro/EQUIPO.md):
  - Los DOS Generator del organismo (rng) y del orden de inyeccion (_rng_l = seed+700000) se crean en Python y se pasan
    al bucle; el tercero (permutacion del control nov_barajada, seed+900000) se consume entero en Python, como el original.
  - Productos con @ (mismo BLAS). Sumas largas: ninguna; las de _sesgo_M/_nov son secuenciales h=1..H_M igual que el
    sum() de Python del original (que NO es np.sum: no hay suma por pares).
  - argsort con empate en la frontera del top-K -> NumPy por objmode (_code, copiado del tronco).
  - clip/outer/where como bucles elementales; np.exp identico.
  - disc_M**h precalculado en Python (DISC[h]).
  - u + _sesgo_M(): el original suma PRIMERO los dos sesgos (gamma_M*b + gamma_N*n) y LUEGO se lo suma a u; aqui igual
    (hacerlo en dos pasos cambiaria el ultimo bit).
  - Los round(...) de la curva NO se hacen en numba (su redondeo decimal no es el de CPython): el bucle devuelve los
    CONTEOS enteros y la division y el round se hacen en Python, exactamente como en el original.
  - Estructuras del mundo como arrays con el MISMO ORDEN DE ITERACION que los dicts: objs (_spawn/_borrar conservan el
    orden de insercion), _SIT (sus claves nunca cambian: _SIT[_x]=_nv solo reescribe un valor), _pend y _rech como
    arrays de L, _Mpat/_Mset como Mk (indice de patron; el original solo guarda filas exactas de PAT_L).
  - _ren, _vistos, _orden, _iny, _curva como arrays; min(_ren,key=(ren[x],x)) y el "primer candidato de _orden no visto"
    son deterministas y no dependen del orden de iteracion.
  - La prueba de teletransporte (<=40x30 pasos) se queda en Python, copiada literal sobre el estado final del bucle.
Restricciones (avisan con ValueError, no divergen en silencio):
  - log_cada debe ser None (el log por pasos no esta compilado).
  - invertir_en junto con pool: el original reemplaza val por {A,B} y luego hace KeyError con cualquier patron del pool.
  - sitios (o nuevo) con un tipo sin valor en val: el original hace KeyError.
"""
import numpy as np
from numba import njit, objmode

L=40; NK=30; NKMAX=90; K=3
PAT={'A':np.array([1,1,0,1,0,0.]),'B':np.array([1,0,1,0,1,0.]),'C':np.array([0,1,1,0,0,1.]),'D':np.array([0,0,1,0,1,1.])}
R_VAL={'comida':1.0,'veneno':-3.0}; E_VAL={'comida':+0.8,'veneno':-0.4}


@njit(cache=True)
def _code(KW, activa, P):
    """Codigo de Kenyon como vector 0/1: top-K de KW@P entre las celdas activas. Con empate en la frontera manda NumPy.
    En vez del argsort completo del gemelo del tronco se seleccionan los K+1 valores mayores (top[K-1] es el K-esimo y
    top[K] el (K+1)-esimo, exactamente w[idx[NKMAX-K]] y w[idx[NKMAX-K-1]] del original): si son distintos el conjunto
    top-K es {i: w[i] > top[K]}, UNICO y sin depender del desempate; si son iguales se cae al argsort de NumPy, igual
    que antes. Mismo resultado, sin el O(n log n) por llamada (es la operacion mas repetida del mundo largo)."""
    v = KW @ P
    w = np.empty(NKMAX)
    for i in range(NKMAX):
        w[i] = v[i] if activa[i] else -1e9
    top = np.full(K + 1, -np.inf)
    for i in range(NKMAX):
        xv = w[i]
        if xv > top[K]:
            j = K
            while j > 0 and xv > top[j - 1]:
                top[j] = top[j - 1]; j -= 1
            top[j] = xv
    out = np.zeros(NKMAX)
    if top[K - 1] == top[K]:
        with objmode(idx='int64[:]'):
            idx = np.argsort(w)
        for i in range(NKMAX - K, NKMAX):
            out[idx[i]] = 1.0
        return out
    for i in range(NKMAX):
        if w[i] > top[K]: out[i] = 1.0
    return out


@njit(cache=True)
def _idx_en(opos, nobjs, x):
    for i in range(nobjs):
        if opos[i] == x: return i
    return -1


@njit(cache=True)
def _spawn(rng, opos, otip, nobjs, nobj, tipos, ntipos, sit_pos, sit_tip, nsit, pend):
    """spawn() del original: con sitios rellena los libres en el orden de _SIT (sin azar); si no, sortea hasta nobj."""
    if nsit > 0:
        for i in range(nsit):
            x = sit_pos[i]
            if _idx_en(opos, nobjs, x) < 0 and pend[x] < 0:
                opos[nobjs] = x; otip[nobjs] = sit_tip[i]; nobjs += 1
        return nobjs
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
def _see(pos, t, opos, otip, nobjs, rech, memoria_rechazo, r_vis):
    """(d, k, left, primer, hallado). left: 1 izquierda, 0 derecha, -1 None. hallado=False es el (None,'vacio',None)."""
    best_d = 0; best_k = -1; best_left = -1; found = False
    for i in range(nobjs):
        x = opos[i]
        if memoria_rechazo > 0 and rech[x] > t: continue
        if r_vis >= 0 and min((pos - x) % L, (x - pos) % L) > r_vis: continue
        dl = (pos - x) % L; dr = (x - pos) % L; d = min(dl, dr)
        if (not found) or d < best_d:
            best_d = d; best_k = otip[i]; best_left = 1 if dl < dr else 0; found = True
    primer = found
    if not found:
        for i in range(nobjs):
            x = opos[i]
            if r_vis >= 0 and min((pos - x) % L, (x - pos) % L) > r_vis: continue
            dl = (pos - x) % L; dr = (x - pos) % L; d = min(dl, dr)
            if (not found) or d < best_d:
                best_d = d; best_k = otip[i]; best_left = 1 if dl < dr else 0; found = True
    return best_d, best_k, best_left, primer, found


@njit(cache=True)
def _valor(KW, activa, Wp, Wn, Wps, Wns, puerta, P):
    """valor(P) del original: sin puerta rapida+lenta; con puerta la rapida si el patron es FAMILIAR, si no la lenta."""
    _k = _code(KW, activa, P)
    Wb = Wp - Wn
    _f = Wb @ _k
    _s = (Wps - Wns) @ P
    if puerta < 0:
        return _f + _s
    nfam = 0
    for i in range(NKMAX):
        if _k[i] > 0 and abs(Wb[i]) > 0.2: nfam += 1
    return _f if nfam >= puerta else _s


@njit(cache=True)
def _sesgo(pos, t, Mk, KW, activa, Wp, Wn, Wps, Wns, puerta, DISC, H_M, PATM, cv, cok,
           gamma_M, gamma_N, tvis, perm_n, nov_cte, tau_N):
    """_sesgo_M() del original, ya multiplicado por gamma_M/gamma_N y SUMADO por direccion (como hace el original antes
    de sumarselo a u). valor(P) es puro dentro de la llamada -> se memoriza por patron (mismos bits, sin repetir argsort)."""
    for i in range(cok.shape[0]): cok[i] = False
    bi = 0.0
    for h in range(1, H_M + 1):
        j = Mk[(pos - h) % L]
        if j >= 0:
            if not cok[j]:
                cv[j] = _valor(KW, activa, Wp, Wn, Wps, Wns, puerta, PATM[j]); cok[j] = True
            bi += DISC[h] * cv[j]
    bd = 0.0
    for h in range(1, H_M + 1):
        j = Mk[(pos + h) % L]
        if j >= 0:
            if not cok[j]:
                cv[j] = _valor(KW, activa, Wp, Wn, Wps, Wns, puerta, PATM[j]); cok[j] = True
            bd += DISC[h] * cv[j]
    if gamma_N != 0.0:   # novedad de sitio: sesgo hacia el sitio CONOCIDO que lleva mas tiempo sin pisarse
        ni = 0.0
        for h in range(1, H_M + 1):
            p = (pos - h) % L
            if Mk[p] >= 0:
                ni += DISC[h] * (1.0 if nov_cte else min(1.0, (t - tvis[perm_n[p]]) / tau_N))
        nd = 0.0
        for h in range(1, H_M + 1):
            p = (pos + h) % L
            if Mk[p] >= 0:
                nd += DISC[h] * (1.0 if nov_cte else min(1.0, (t - tvis[perm_n[p]]) / tau_N))
        return gamma_M * bi + gamma_N * ni, gamma_M * bd + gamma_N * nd
    return gamma_M * bi, gamma_M * bd


@njit(cache=True)
def _bucle(rng, rng_l, T, learn, invertir_en, nuevo_idx, nuevo_en, nuevo_valc, eta, tau_e, alpha, hambre_boca, aversion,
           costo, nobj, plast, theta, ema, paso, lam, memoria_rechazo, mu_norm, div_signo, eta_s, clip_s, puerta,
           Wl, KW, activa, PATM, r_vis, sit_pos, sit_tip, nsit, regen, usa_M, escribe_M, gamma_M, H_M, DISC,
           orden, n_orden, T_nuevo, reciclado, invertir_largo, vistos, nvistos, valc,
           gamma_N, tau_N, perm_n, nov_cte):
    n_pat = PATM.shape[0]
    Wp = np.zeros(NKMAX); Wn = np.zeros(NKMAX); err = np.zeros(NKMAX); mu = np.zeros((NKMAX, 6)); splits = 0
    el = np.zeros((2, 9)); tr = np.zeros(9)
    Wps = np.zeros(6); Wns = np.zeros(6)
    Mk = np.full(L, -1, np.int64)                                    # mapa: posicion -> indice del ultimo patron visto
    tvis = np.zeros(L); nvis = np.zeros(L, np.int64)                 # novedad: ultimo paso pisado, cuantas veces
    pos = 0; E = 1.0
    err_max = 0.0; t_conflicto = -1; t_techo = -1; n_techo = 0
    rech = np.full(L, -1, np.int64); prev_on = -1
    sobre = np.zeros((2, 4), np.int64); llegadas = np.zeros((2, 4), np.int64); sin_objetivo = np.zeros(4, np.int64)   # fila 0 veneno, 1 comida
    tipos = np.zeros(3, np.int64); tipos[0] = 0; tipos[1] = 1; ntipos = 2
    nmax = nobj if nsit == 0 else nsit
    opos = np.full(nmax, -1, np.int64); otip = np.full(nmax, -1, np.int64); nobjs = 0
    pend = np.full(L, -1, np.int64); npend = 0                       # mapa: sitio -> paso en que reaparece
    ren = np.zeros(L, np.int64)                                      # largo: ultima renovacion por sitio
    visto = np.zeros(n_pat, np.bool_)
    for a in range(nvistos): visto[vistos[a]] = True
    nobjs = _spawn(rng, opos, otip, nobjs, nobj, tipos, ntipos, sit_pos, sit_tip, nsit, pend)
    deaths = 0
    mord = np.zeros((n_pat, 4), np.int64); vis = np.zeros((n_pat, 4), np.int64)
    st_t = np.zeros(NKMAX, np.int64); st_k = np.zeros(NKMAX, np.int64); nst = 0
    nbin = T // 1000 + 1
    cbin = np.zeros(nbin, np.int64); dbin = np.zeros(nbin, np.int64)   # largo: comida y muertes por bloque de 1000
    niny_max = (T // T_nuevo + 2) if T_nuevo > 0 else 1
    iny_t = np.zeros(niny_max, np.int64); iny_nv = np.zeros(niny_max, np.int64); iny_x = np.zeros(niny_max, np.int64); niny = 0
    cur_t = np.zeros(niny_max, np.int64); cur_nv = np.zeros(niny_max, np.int64)
    cur_cu = np.zeros(niny_max, np.int64); cur_nu = np.zeros(niny_max, np.int64)
    cur_cp = np.zeros(niny_max, np.int64); cur_np = np.zeros(niny_max, np.int64); ncur = 0
    flip = np.zeros(n_pat, np.bool_)
    q_div = T // 4
    x = np.empty(9); m = np.zeros(2); kc = np.zeros(NKMAX)
    cv = np.zeros(n_pat); cok = np.zeros(n_pat, np.bool_)
    for t in range(T):
        if npend > 0:                                                # mapa: reaparecen en su sitio los objetos maduros
            nm = 0
            for xx in range(L):
                if pend[xx] >= 0 and pend[xx] <= t:
                    pend[xx] = -1; nm += 1
            if nm > 0:
                npend -= nm
                nobjs = _spawn(rng, opos, otip, nobjs, nobj, tipos, ntipos, sit_pos, sit_tip, nsit, pend)
        if invertir_en >= 0 and t == invertir_en:
            for i in range(n_pat): valc[i] = 0                       # el original REEMPLAZA val por {'A','B'}
            valc[0] = -1; valc[1] = 1
        if nuevo_idx >= 0 and t == nuevo_en:
            tipos[ntipos] = nuevo_idx; ntipos += 1; valc[nuevo_idx] = nuevo_valc
        if T_nuevo > 0 and t > 0 and t % T_nuevo == 0:                # largo: entra un patron en el sitio mas viejo
            cand = -1
            for a in range(n_orden):
                if not visto[orden[a]]:
                    cand = orden[a]; break
            if reciclado or cand < 0:
                nv = vistos[rng_l.integers(0, nvistos)]
            else:
                nv = cand
            bx = -1; br = 0                                          # _x = min(_ren, key=lambda x:(_ren[x],x))
            for i in range(nsit):
                xx = sit_pos[i]
                if bx < 0 or ren[xx] < br or (ren[xx] == br and xx < bx):
                    bx = xx; br = ren[xx]
            for i in range(nsit):
                if sit_pos[i] == bx:
                    sit_tip[i] = nv; break
            ren[bx] = t
            io2 = _idx_en(opos, nobjs, bx)
            if io2 >= 0: otip[io2] = nv
            if not visto[nv]:
                vistos[nvistos] = nv; nvistos += 1; visto[nv] = True
            iny_t[niny] = t; iny_nv[niny] = nv; iny_x[niny] = bx; niny += 1
            nu = nvistos if nvistos < 10 else 10                     # _ult = _vistos[-10:]
            cu = 0
            for a in range(nvistos - nu, nvistos):
                nn = vistos[a]
                if (_valor(KW, activa, Wp, Wn, Wps, Wns, puerta, PATM[nn]) > 0) == (valc[nn] == 1): cu += 1
            npr = nvistos if nvistos < 10 else 10                    # _pri = _vistos[:10]
            cp = 0
            for a in range(npr):
                nn = vistos[a]
                if (_valor(KW, activa, Wp, Wn, Wps, Wns, puerta, PATM[nn]) > 0) == (valc[nn] == 1): cp += 1
            cur_t[ncur] = t; cur_nv[ncur] = nvistos
            cur_cu[ncur] = cu; cur_nu[ncur] = nu; cur_cp[ncur] = cp; cur_np[ncur] = npr; ncur += 1
        if invertir_largo >= 0 and t == invertir_largo:               # largo: cambio de regla sin aviso
            for i in range(n_pat): flip[i] = False
            n4 = nvistos if nvistos < 4 else 4
            for a in range(n4): flip[vistos[a]] = True
            for i in range(nsit): flip[sit_tip[i]] = True
            for i in range(n_pat):
                if flip[i]: valc[i] = -valc[i]
        q = min(t // q_div, 3)
        hambre = min(max(1 - E, 0.0), 1.0)
        d, k, left, primer, found = _see(pos, t, opos, otip, nobjs, rech, memoria_rechazo, r_vis)
        if not primer: sin_objetivo[q] += 1
        if found:
            for i in range(6): x[i] = PATM[k, i] * 1.2
        else:
            for i in range(6): x[i] = 0.0                            # mapa: retina en cero cuando no hay nada a la vista
        if left == 1:
            x[6] = 1.5; x[7] = 0.0
        elif left == 0:
            x[6] = 0.0; x[7] = 1.5
        else:
            x[6] = 0.0; x[7] = 0.0
        x[8] = 1.0 if (found and d == 0) else 0.0
        noise = .15 + .5 * hambre
        V = Wl @ x
        p = 1 / (1 + np.exp(-(V - .8) / noise))
        u = p + rng.normal(0, .3, 2)
        m[0] = 0.0; m[1] = 0.0
        if usa_M and not found:                                      # mapa: solo desempata sin senal directa
            s0, s1 = _sesgo(pos, t, Mk, KW, activa, Wp, Wn, Wps, Wns, puerta, DISC, H_M, PATM, cv, cok,
                            gamma_M, gamma_N, tvis, perm_n, nov_cte, tau_N)
            u[0] = u[0] + s0
            u[1] = u[1] + s1
        if u.max() > .5: m[np.argmax(u)] = 1
        for j in range(9): tr[j] = tr[j] * .7 + x[j]
        if learn:
            for i in range(2):
                for j in range(9): el[i, j] = el[i, j] * tau_e + (m[i] - p[i]) * tr[j]
        pos = (pos + int(m[1] - m[0])) % L
        d2, _k2, _l2, _p2, found2 = _see(pos, t, opos, otip, nobjs, rech, memoria_rechazo, r_vis)
        Rp = .2 if (found and found2 and d2 < d) else 0.0
        R = 0.0
        io = _idx_en(opos, nobjs, pos)
        if io >= 0:
            if usa_M and escribe_M:
                Mk[pos] = otip[io]                                   # mapa: recuerda lo que vio aqui
            tvis[pos] = t; nvis[pos] += 1                            # novedad: pisar el sitio lo pone 'visto ahora'
            kk = otip[io]; P = PATM[kk]; kc = _code(KW, activa, P); Wb = Wp - Wn; _wf = Wb @ kc; _ws = (Wps - Wns) @ P
            nfam = 0
            for i in range(NKMAX):
                if kc[i] > 0 and abs(Wb[i]) > 0.2: nfam += 1
            _wt = (_wf + _ws) if puerta < 0 else (_wf if nfam >= puerta else _ws)
            Vb = alpha * _wt + hambre_boca * hambre + .5; pb = 1 / (1 + np.exp(-Vb / .3)); mordio = rng.random() < pb
            vis[kk, q] += 1
            fila = 1 if valc[kk] == 1 else 0
            sobre[fila, q] += 1; llegadas[fila, q] += 1 if prev_on != pos else 0
            if memoria_rechazo > 0 and not mordio: rech[pos] = t + memoria_rechazo
            if mordio:
                R = 1.0 if valc[kk] == 1 else -3.0; E = min(E + (0.8 if valc[kk] == 1 else -0.4), 1.5); mord[kk, q] += 1
                if valc[kk] == 1: cbin[t // 1000] += 1               # largo
                if nsit > 0:
                    pend[pos] = t + regen; npend += 1                # mapa: reaparece en su sitio
                nobjs = _borrar(opos, otip, nobjs, pos)
                nobjs = _spawn(rng, opos, otip, nobjs, nobj, tipos, ntipos, sit_pos, sit_tip, nsit, pend)
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
        _rr = rng.random()
        if _rr < .003 and nobjs > 0:
            i = rng.integers(0, nobjs); _dx = opos[i]
            if nsit > 0:
                pend[_dx] = t + regen; npend += 1                     # mapa
            nobjs = _borrar(opos, otip, nobjs, _dx)
            nobjs = _spawn(rng, opos, otip, nobjs, nobj, tipos, ntipos, sit_pos, sit_tip, nsit, pend)
            rech[_dx] = -1
        if learn:
            s = eta * (1 + 2 * hambre) * (max(R, 0.0) + Rp)
            for i in range(2):
                for j in range(9): Wl[i, j] = min(max(Wl[i, j] + s * el[i, j], 0.0), 1.5)
        if E <= 0:
            deaths += 1; E = .6; pos = rng.integers(0, L); dbin[t // 1000] += 1   # (+largo)
    return (Wp, Wn, Wps, Wns, KW, activa, splits, st_t[:nst], st_k[:nst], mord, vis, sobre, llegadas, sin_objetivo, deaths,
            err_max, t_conflicto, t_techo, n_techo, Mk, opos, otip, nobjs, pend, valc, tipos[:ntipos],
            cbin, dbin, iny_t[:niny], iny_nv[:niny], iny_x[:niny],
            cur_t[:ncur], cur_nv[:ncur], cur_cu[:ncur], cur_nu[:ncur], cur_cp[:ncur], cur_np[:ncur],
            vistos[:nvistos], sit_tip, tvis, nvis)


def run(seed,T=100000,learn=True,invertir_en=None,nuevo=None,nuevo_en=50000,nuevo_val='veneno',solap_B=None,
        eta=.03,tau_e=.85,alpha=1.2,hambre_boca=2.0,aversion=1.0,costo=.002,nobj=4,log_cada=None,plast=True,theta=0.6,ema=0.02,paso=0.5,solap_AB=None,lam=0.05,memoria_rechazo=20,mu_norm=True,div_signo=True,eta_s=0.015,clip_s=3.0,puerta=3,
        r_vis=None,sitios=None,regen=50,usa_M=False,escribe_M=True,gamma_M=0.6,H_M=20,disc_M=0.9,prueba=None,
        pool=None,T_nuevo=None,reciclado=False,invertir_largo=None,
        gamma_N=0.0,tau_N=4000.0,nov_barajada=False,nov_cte=False):   # mapa + largo + novedad de sitio
    if log_cada:
        raise ValueError("mundo_largo_n_rapido: log_cada no esta compilado; usa mundo_largo_n para eso")
    if invertir_en is not None and pool is not None:
        raise ValueError("mundo_largo_n_rapido: invertir_en con pool; el original reemplaza val por {A,B} y luego hace KeyError")
    if T_nuevo and sitios is None:
        raise ValueError("mundo_largo_n_rapido: T_nuevo sin sitios; el original hace min() sobre un _ren vacio")
    rng=np.random.default_rng(seed)
    # --- inicializacion: EXACTAMENTE las lineas del original (mismo flujo de azar en los dos Generator) ---
    PAT_L=PAT if pool is None else dict(PAT,**{n:v for n,v,_ in pool})   # largo: los patrones del pool ademas de A-D
    _rng_l=np.random.default_rng(seed+700000)   # largo: RNG propio para el orden de inyeccion (no toca el del organismo)
    _orden=[] if pool is None else [n for n,_,_ in pool]
    if pool is not None: _orden=[_orden[i] for i in _rng_l.permutation(len(_orden))]
    Wl=rng.uniform(.1,.4,(2,9)); KW=np.zeros((NKMAX,6)); activa=np.zeros(NKMAX,bool); KW[:NK]=rng.uniform(0,1,(NK,6)); activa[:NK]=True
    def code(P):
        v=KW@P; v=np.where(activa,v,-1e9); return set(np.argsort(v)[-K:])
    objetivo_AB=0 if solap_AB is None else solap_AB
    if solap_AB: KW[:solap_AB]=0; KW[:solap_AB,0]=5.0
    cond=lambda: len(code(PAT_L['A'])&code(PAT_L['B']))==objetivo_AB and (nuevo is None or solap_B is None or (len(code(PAT_L[nuevo])&code(PAT_L['B']))==solap_B and len(code(PAT_L[nuevo])&code(PAT_L['A']))==0))
    while not cond(): KW[objetivo_AB:NK]=rng.uniform(0,1,(NK-objetivo_AB,6))
    if invertir_en is not None and nuevo is not None and nuevo_en < invertir_en:
        raise ValueError("el original no admite nuevo antes de invertir (val se reemplaza)")
    NOM=list(PAT_L); IX={n:i for i,n in enumerate(NOM)}; n_pat=len(NOM)
    PATM=np.array([PAT_L[n] for n in NOM])
    valc=np.zeros(n_pat,np.int64); valc[IX['A']]=1; valc[IX['B']]=-1   # val={'A':'comida','B':'veneno'}
    if pool is not None:
        for n,_,vl in pool: valc[IX[n]]=1 if vl=='comida' else -1      # largo: val.update(...)
    _SIT={}; _vistos=[]
    if sitios is not None:
        _F0=int(rng.integers(L)); _SIT={(_F0+i*(L//len(sitios)))%L:kk for i,kk in enumerate(sitios)}
        _vistos=list(dict.fromkeys(sitios))
    for kk in _vistos:
        if kk not in PAT_L or valc[IX[kk]]==0:
            raise ValueError("mundo_largo_n_rapido: sitios con un tipo sin valor en val; el original hace KeyError")
    perm_n=np.arange(L)
    if sitios is not None and nov_barajada:   # control 1: RNG propio, no toca el del organismo
        _ps=np.array(sorted(_SIT)); perm_n[_ps]=_ps[np.random.default_rng(seed+900000).permutation(len(_ps))]
    sit_pos=np.array([int(v) for v in _SIT.keys()],np.int64) if _SIT else np.zeros(0,np.int64)
    sit_tip=np.array([IX[kk] for kk in _SIT.values()],np.int64) if _SIT else np.zeros(0,np.int64)
    DISC=np.array([disc_M**h for h in range(int(H_M)+1)])
    orden=np.array([IX[n] for n in _orden],np.int64) if _orden else np.zeros(0,np.int64)
    vistos=np.zeros(n_pat,np.int64)
    for i,n in enumerate(_vistos): vistos[i]=IX[n]
    (Wp, Wn, Wps, Wns, KW, activa, splits, st_t, st_k, mord, vis, sobre, llegadas, sin_objetivo, deaths, err_max,
     t_conflicto, t_techo, n_techo, Mk, opos, otip, nobjs, pend, valc, tipos_a,
     cbin, dbin, iny_t, iny_nv, iny_x, cur_t, cur_nv, cur_cu, cur_nu, cur_cp, cur_np, vistos_a, sit_tip, tvis, nvis) = _bucle(
        rng, _rng_l, int(T), bool(learn), -1 if invertir_en is None else int(invertir_en), -1 if nuevo is None else IX[nuevo], int(nuevo_en),
        1 if nuevo_val == 'comida' else -1, float(eta), float(tau_e), float(alpha), float(hambre_boca), float(aversion), float(costo), int(nobj),
        bool(plast), float(theta), float(ema), float(paso), float(lam), int(memoria_rechazo), bool(mu_norm), bool(div_signo), float(eta_s), float(clip_s),
        -1 if puerta is None else int(puerta), Wl, KW, activa, PATM,
        -1 if r_vis is None else int(r_vis), sit_pos, sit_tip, len(sit_pos), int(regen), bool(usa_M), bool(escribe_M),
        float(gamma_M), int(H_M), DISC,
        orden, len(orden), 0 if not T_nuevo else int(T_nuevo), bool(reciclado), -1 if invertir_largo is None else int(invertir_largo),
        vistos, len(_vistos), valc,
        float(gamma_N), float(tau_N), perm_n, bool(nov_cte))
    # --- estado del original reconstruido para la prueba (que se corre en Python, copiada literal) ---
    _VACIO=np.zeros(6)
    _Mpat=np.zeros((L,6)); _Mset=np.zeros(L,bool)
    for i in range(L):
        if Mk[i]>=0: _Mpat[i]=PATM[int(Mk[i])]; _Mset[i]=True
    _SIT={int(sit_pos[i]):NOM[int(sit_tip[i])] for i in range(len(sit_pos))}   # los valores cambian con las inyecciones; las claves nunca
    objs={int(opos[i]):NOM[int(otip[i])] for i in range(int(nobjs))}           # mismo orden de insercion que el dict original
    _pend={int(i):int(pend[i]) for i in range(L) if pend[i]>=0}
    _rech={}   # la prueba lo vacia en cada teletransporte antes de mirar
    tipos=[NOM[int(v)] for v in tipos_a]
    _vistos=[NOM[int(v)] for v in vistos_a]
    val={}   # mismo orden de insercion que el original: A, B, el pool, y nuevo al final si entro
    if invertir_en is not None and T > invertir_en:
        _base=['A','B']
    else:
        _base=['A','B']+([n for n,_,_ in pool] if pool is not None else [])
    for n in _base: val[n]='comida' if valc[IX[n]]==1 else 'veneno'
    if nuevo is not None and T > nuevo_en: val[nuevo]='comida' if valc[IX[nuevo]]==1 else 'veneno'
    t=int(T)-1; pos=0; E=1.0; tr=np.zeros(9)
    q=lambda tt:min(tt//(T//4),3)
    def kenyon(P): k=np.zeros(NKMAX); k[list(code(P))]=1; return k
    def valor(P):
        _k=kenyon(P); _f=float((Wp-Wn)@_k); _s=float((Wps-Wns)@P)
        return _f+_s if puerta is None else (_f if int((np.abs((Wp-Wn)[_k>0])>0.2).sum())>=puerta else _s)
    def _nov(p):
        return 1.0 if nov_cte else min(1.0,float(t-tvis[perm_n[p]])/tau_N)
    def spawn():
        if sitios is not None:
            for x,kk in _SIT.items():
                if x not in objs and x not in _pend: objs[x]=kk
            return
        while len(objs)<nobj:
            x=int(rng.integers(L))
            if x not in objs: objs[x]=tipos[int(rng.integers(len(tipos)))]
    def _sesgo_M():
        _bi=sum(disc_M**h*valor(_Mpat[(pos-h)%L]) for h in range(1,H_M+1) if _Mset[(pos-h)%L])
        _bd=sum(disc_M**h*valor(_Mpat[(pos+h)%L]) for h in range(1,H_M+1) if _Mset[(pos+h)%L])
        if gamma_N:
            _ni=sum(disc_M**h*_nov((pos-h)%L) for h in range(1,H_M+1) if _Mset[(pos-h)%L])
            _nd=sum(disc_M**h*_nov((pos+h)%L) for h in range(1,H_M+1) if _Mset[(pos+h)%L])
            return gamma_M*np.array([_bi,_bd])+gamma_N*np.array([_ni,_nd])
        return gamma_M*np.array([_bi,_bd])
    def see(contar=False):
        best=None
        for x,k in objs.items():
            if memoria_rechazo and _rech.get(x,-1)>t: continue
            if r_vis is not None and min((pos-x)%L,(x-pos)%L)>r_vis: continue
            dl=(pos-x)%L; dr=(x-pos)%L; d=min(dl,dr)
            if best is None or d<best[0]: best=(d,k,dl<dr)
        if best is None:
            if contar: sin_objetivo[q(t)]+=1
            for x,k in objs.items():
                if r_vis is not None and min((pos-x)%L,(x-pos)%L)>r_vis: continue
                dl=(pos-x)%L; dr=(x-pos)%L; d=min(dl,dr)
                if best is None or d<best[0]: best=(d,k,dl<dr)
        return best if best is not None else (None,'vacio',None)
    _tel=None
    if prueba is not None:   # mapa: prueba de teletransporte, sin aprendizaje (literal del original)
        _Fs=[x for x,kk in _SIT.items() if val[kk]=='comida']; _F=_Fs[0] if _Fs else int(rng.integers(L))
        if prueba.get('barajar'):
            _pi=rng.permutation(NKMAX); Wp=Wp[_pi]; Wn=Wn[_pi]; _pj=rng.permutation(6); Wps=Wps[_pj]; Wns=Wns[_pj]
        if prueba.get('invertir'): Wp,Wn=Wn,Wp; Wps,Wns=Wns,Wps
        _ac=[]; _nn=0; _ciego=0; _pasos=[]
        for i in range(prueba.get('n_tel',40)):
            _dn=int(rng.integers(r_vis+1,13)); _lado=-1 if i%2==0 else 1
            pos=(_F-_lado*_dn)%L; E=prueba.get('E_test',0.3); tr=np.zeros(9); _rech.clear()
            for x in list(_pend): del _pend[x]
            spawn(); _dir=0
            for _s in range(prueba.get('max_pasos',30)):
                hambre=np.clip(1-E,0,1); d,k,left=see(); pat=PAT_L[k] if k!='vacio' else _VACIO
                if _s==0 and k=='vacio': _ciego+=1
                x=np.concatenate([pat*1.2,[1.5 if left else 0,1.5 if left is False else 0,1.0 if d==0 else 0.]]); noise=.15+.5*hambre
                V=Wl@x; p=1/(1+np.exp(-(V-.8)/noise)); u=p+rng.normal(0,.3,2); m=np.zeros(2)
                if usa_M and k=='vacio': u=u+_sesgo_M()
                if u.max()>.5: m[np.argmax(u)]=1
                if m.any(): _dir=int(m[1]-m[0]); break
            _pasos.append(_s+1)
            if _dir==0: _nn+=1
            else: _ac.append(int(_dir==_lado))
        _tel=dict(acierto=(round(sum(_ac)/len(_ac),3) if _ac else None),n=len(_ac),sin_mover=_nn,ciego_al_llegar=_ciego,
                  pasos_medio=round(sum(_pasos)/len(_pasos),2),F=_F,sitios={int(x):kk for x,kk in _SIT.items()})
    W={k:round(valor(PAT_L[k]),2) for k in PAT_L}
    W_lenta={k:round(float((Wps-Wns)@PAT_L[k]),3) for k in PAT_L}
    comp={k:(round(float(Wp@kenyon(PAT_L[k])),2),round(float(Wn@kenyon(PAT_L[k])),2)) for k in PAT_L}
    # la curva se redondea AQUI: round() de numba no es el de CPython; el bucle devuelve los conteos enteros
    _curva=[(int(cur_t[i]),int(cur_nv[i]),round(int(cur_cu[i])/int(cur_nu[i]),3),round(int(cur_cp[i])/int(cur_np[i]),3)) for i in range(len(cur_t))]
    _iny=[(int(iny_t[i]),NOM[int(iny_nv[i])],int(iny_x[i])) for i in range(len(iny_t))]
    return dict(sobre={'veneno':[int(v) for v in sobre[0]],'comida':[int(v) for v in sobre[1]]},
                llegadas={'veneno':[int(v) for v in llegadas[0]],'comida':[int(v) for v in llegadas[1]]},
                sin_objetivo=[int(v) for v in sin_objetivo],memoria_rechazo=memoria_rechazo,err_max=float(err_max),
                t_conflicto=None if t_conflicto<0 else int(t_conflicto),t_techo=None if t_techo<0 else int(t_techo),n_techo=int(n_techo),
                split_t=[(int(a),NOM[int(b)]) for a,b in zip(st_t,st_k)],
                mord={k:[int(v) for v in mord[IX[k]]] for k in PAT_L},vis={k:[int(v) for v in vis[IX[k]]] for k in PAT_L},
                W=W,comp=comp,deaths=int(deaths),log=[],splits=int(splits),celdas=int(activa.sum()),
                solap={'AB':len(code(PAT_L['A'])&code(PAT_L['B'])),'nB':len(code(PAT_L[nuevo])&code(PAT_L['B'])) if nuevo else None},
                W_lenta=W_lenta,Wps=[round(float(x),3) for x in Wps],Wns=[round(float(x),3) for x in Wns],
                tel=_tel,M_llenas=int(_Mset.sum()),   # mapa
                curva=_curva,inyecciones=_iny,vistos=_vistos,comida_bin=[int(v) for v in cbin],muertes_bin=[int(v) for v in dbin],
                val_final=dict(val),   # largo
                nov_diag=dict(tvis={int(x):int(tvis[int(x)]) for x in sit_pos},visitas={int(x):int(nvis[int(x)]) for x in sit_pos}))   # novedad
