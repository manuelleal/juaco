"""
mundo_social_n3_rapido — gemelo COMPILADO (numba) de experimentos/etapa5_comunicacion/mundo_social_n3.py.
NO es un mundo nuevo: misma regla, mismo flujo de azar, mismas salidas (todas las claves de cada organismo). Existe
para correr mas rapido. Solo vale si es BIT A BIT identico al original: arnes identidad_social_rapido.py
(regla: si no es identico, no se usa para confirmar). Modelo: organismo/organismo_v13_rapido.py.

Decisiones repetidas del gemelo del tronco (organismo_v13_rapido.py):
  - Generator: se pasan al bucle compilado LOS MISMOS objetos rng creados en Python (uno por organismo,
    rngs[i]=default_rng(seed+100000*i), mas rng_mundo, rng_senal y rngs_q). Se pasan como TUPLA homogenea (numba
    permite indexarla con un entero de runtime). Con n=1 y compat=True rng_mundo ES rngs[0]: dos referencias al
    mismo objeto comparten estado dentro de numba (comprobado).
  - productos con @ (llaman al mismo BLAS); nada de .sum() sobre >= 8 elementos (aqui: 6 pixeles, 2 patas, K_sim
    simbolos -> se rechaza K_sim >= 8, que activaria la suma por pares de NumPy).
  - argsort con EMPATES: guardia en _code; si hay empate en la frontera del top-K manda NumPy (objmode). Con
    mascaras un patron puede quedar en el vector nulo (todo empate) -> esa guardia es la que se dispara.
  - clip / outer / where escritos como bucles elementales (misma aritmetica IEEE).
  - dicts como arrays con el MISMO orden de iteracion: objs y pend del Mundo en orden de insercion; _rech por
    organismo como vector sobre las L posiciones; s_ult, ultimo, traza y las pendientes de N2 como arrays con marca
    de tiempo (-1 = ausente).
  - la lectura final (W, comp, W_lenta, simbolos) se hace en Python con las mismas lineas del original, para que el
    redondeo y el argsort del cierre sean exactamente los del original.

Lo que NO esta cubierto (lanza NotImplementedError / ValueError / TypeError, nunca un resultado distinto en silencio):
  - K_sim >= 8 (suma por pares de NumPy en Pq/M).
  - senal o estado_emisor desconocidos (el original trataria la senal desconocida como None en silencio).
  - parametros de semantica entera pasados con parte fraccionaria (ENTEROS): el gemelo los guarda como int64.
  - kwargs que el Organismo no reconoce (el original daria TypeError; aqui tambien).
Todo lo demas de la firma de mundo_social_n3.run esta cubierto: senal None/honesta/conducta/barajada/
barajada_conducta/simbolo/simbolo_barajado, mascaras, kw_por_org, regen, tipos_fijos, mudo_desde, estado_emisor
(conducta/valor/valor_rapido), estados heredados, devolver_estado, mundo AB y regla, y las TRES perillas de N2f:
  - regen_rota: al reaparecer (regenerar y rama "nunca vacio" de retirar) el tipo se vuelve a sortear con el RNG del
    mundo sobre la lista COMPLETA de tipos; apagada no toca el RNG (cortocircuito del condicional del original).
  - vida: sello de nacimiento por sitio (nace, con mundo.t) en spawn/regenerar/"nunca vacio"; caducar(t) retira lo
    que lleva `vida` pasos sin morderse por el MISMO camino que una mordida (retirar -> pend/spawn), sobre una foto
    de objs en orden de insercion, y cuenta `caducados` (del MUNDO: va en la salida de cada organismo).
  - escucha_si_no_sabe: el empujon vicario del simbolo no se aplica si abs(valor(kk)) >= abs(R_hat); cuenta
    `no_desensena`. valor() no toca RNG ni estado, y con la perilla apagada ni se evalua.
"""
import numpy as np
from numba import njit, objmode

L = 40; NK = 30; NKMAX = 90; K = 3
PAT = {'A': np.array([1, 1, 0, 1, 0, 0.]), 'B': np.array([1, 0, 1, 0, 1, 0.]),
       'C': np.array([0, 1, 1, 0, 0, 1.]), 'D': np.array([0, 0, 1, 0, 1, 1.])}
R_VAL = {'comida': 1.0, 'veneno': -3.0}; E_VAL = {'comida': +0.8, 'veneno': -0.4}
SIMBOLOS = ('simbolo', 'simbolo_barajado')
MAXSPLIT = NKMAX - NK + 1

# --- parametros por organismo: indices de fpar (float) e ipar (entero/booleano) ---
(F_ETA, F_TAU_E, F_ALPHA, F_HAMBRE_BOCA, F_AVERSION, F_COSTO, F_THETA, F_EMA, F_PASO, F_LAM, F_ETA_S, F_CLIP_S,
 F_BETA_Q, F_ETA_Q, F_ETA_M, F_U_M, F_GAMMA_SIM, F_RHO_B, F_GAMMA_SOC) = range(19)
NF = 19
(I_PLAST, I_MEM_RECH, I_LEARN, I_MU_NORM, I_DIV_SIGNO, I_PUERTA, I_TAU_M, I_BASELINE_Q, I_ALINEA, I_TAU_SOC,
 I_ESCUCHA, I_ESC_NO_SABE) = range(12)
NI = 12
# --- contadores por organismo: indices de cnt (int64) y est (float64) ---
(C_POS, C_PREV_ON, C_DEATHS, C_SPLITS, C_NST, C_AVISOS_B, C_TEXTB, C_TBOK, C_NSESGO, C_SIMREC, C_DECOD, C_ALIN,
 C_SEMIT, C_SRECIB, C_NODES) = range(15)
NC = 15
(E_E, E_HAMBRE, E_R, E_RP) = range(4)
NE = 4
# --- codigos de senal y de estado_emisor ---
S_NONE, S_HONESTA, S_CONDUCTA, S_BARAJADA, S_BARAJADA_CONDUCTA, S_SIMBOLO, S_SIMBOLO_BARAJADO = range(7)
COD_SENAL = {None: S_NONE, 'honesta': S_HONESTA, 'conducta': S_CONDUCTA, 'barajada': S_BARAJADA,
             'barajada_conducta': S_BARAJADA_CONDUCTA, 'simbolo': S_SIMBOLO, 'simbolo_barajado': S_SIMBOLO_BARAJADO}
COD_EMISOR = {'conducta': 0, 'valor': 1, 'valor_rapido': 2}

DEFAULTS = dict(eta=.03, tau_e=.85, alpha=1.2, hambre_boca=2.0, aversion=1.0, costo=.002, plast=True, theta=0.6,
                ema=0.02, paso=0.5, lam=0.05, memoria_rechazo=20, learn=True, mu_norm=True, div_signo=True,
                eta_s=0.015, clip_s=3.0, puerta=3, beta_q=2.0, eta_q=0.1, eta_m=0.1, tau_m=200, u_m=0.5,
                gamma_sim=0.0, baseline_q=False, rho_b=0.05, alinea=False, gamma_soc=0.0, tau_soc=400, escucha=True,
                escucha_si_no_sabe=False)   # N2f
# parametros que el gemelo guarda como enteros; si llegan con parte fraccionaria el original los usaria como float
# (comparaciones de plazo y de distancia) y el gemelo los truncaria: se rechaza en vez de diferir en silencio.
ENTEROS = ('T', 'n', 'd_senal', 'tau_s', 'K_sim', 'regen', 'mudo_desde', 'invertir_en', 'nobj_por_org', 'vida',
           'memoria_rechazo', 'tau_m', 'tau_soc', 'puerta')


def _ent(v, nombre):
    if v is None: return
    if int(v) != v:
        raise NotImplementedError(f"mundo_social_n3_rapido: {nombre}={v!r} no es entero; el gemelo lo truncaria")


# ------------------------------------------------------------------ Kenyon
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


# ------------------------------------------------------------------ Mundo (objs y pend como arrays en orden de insercion)
@njit(cache=True)
def _reaparece(rng, kk, tipos, ntipos, regen_rota):
    """Mundo._reaparece (N2f): con regen_rota apagado devuelve el MISMO tipo y NO toca el RNG (cortocircuito)."""
    if regen_rota: return tipos[rng.integers(0, ntipos)]
    return kk


@njit(cache=True)
def _spawn(rng, opos, otip, nobjs, ppos, npend, nobj, tipos, ntipos, fijos, ifij, nfij, nace, t):
    """Mundo.spawn: while len(objs)+len(pend) < nobj. Con fijos, el tipo sale de la lista (sin tocar el rng).
    N2f-v3: sello de nacimiento nace[x] = mundo.t (aqui t, que es el mundo.t del paso)."""
    while nobjs + npend < nobj:
        x = rng.integers(0, L)
        dup = False
        for i in range(nobjs):
            if opos[i] == x:
                dup = True; break
        if not dup:
            for i in range(npend):
                if ppos[i] == x:
                    dup = True; break
        if not dup:
            if ifij < nfij:
                otip[nobjs] = fijos[ifij]; ifij += 1
            else:
                otip[nobjs] = tipos[rng.integers(0, ntipos)]
            opos[nobjs] = x; nobjs += 1; nace[x] = t
    return nobjs, ifij


@njit(cache=True)
def _retirar(rng, opos, otip, nobjs, ppos, ptip, pt, npend, x, t, regen, nobj, tipos, ntipos, fijos, ifij, nfij,
             nace, regen_rota):
    """Mundo.retirar: saca x de objs (conservando el orden de insercion); con regen lo deja pendiente y, si objs
    quedo vacio, devuelve YA el pendiente mas antiguo (primero en orden de insercion ante empate; N2f: con el tipo
    rotado y sello de nacimiento nuevo). Luego spawn."""
    j = -1
    for i in range(nobjs):
        if opos[i] == x:
            j = i; break
    kk = otip[j]
    for i in range(j, nobjs - 1):
        opos[i] = opos[i + 1]; otip[i] = otip[i + 1]
    nobjs -= 1; opos[nobjs] = -1; otip[nobjs] = -1
    if regen >= 0:
        ppos[npend] = x; ptip[npend] = kk; pt[npend] = t + regen; npend += 1
        if nobjs == 0:
            b = 0
            for i in range(1, npend):
                if pt[i] < pt[b]: b = i
            x0 = ppos[b]; kk0 = ptip[b]
            for i in range(b, npend - 1):
                ppos[i] = ppos[i + 1]; ptip[i] = ptip[i + 1]; pt[i] = pt[i + 1]
            npend -= 1
            opos[nobjs] = x0; otip[nobjs] = _reaparece(rng, kk0, tipos, ntipos, regen_rota); nobjs += 1
            nace[x0] = t
    nobjs, ifij = _spawn(rng, opos, otip, nobjs, ppos, npend, nobj, tipos, ntipos, fijos, ifij, nfij, nace, t)
    return nobjs, npend, ifij


@njit(cache=True)
def _regenerar(rng, opos, otip, nobjs, ppos, ptip, pt, npend, t, tipos, ntipos, regen_rota, nace):
    """Mundo.regenerar: los pendientes vencidos vuelven a objs en orden de insercion (N2f: con el tipo rotado, un
    sorteo por vencido y en ese mismo orden; N2f-v3: sello de nacimiento t)."""
    w = 0
    for i in range(npend):
        if pt[i] <= t:
            opos[nobjs] = ppos[i]; otip[nobjs] = _reaparece(rng, ptip[i], tipos, ntipos, regen_rota); nobjs += 1
            nace[ppos[i]] = t
        else:
            ppos[w] = ppos[i]; ptip[w] = ptip[i]; pt[w] = pt[i]; w += 1
    return nobjs, w


@njit(cache=True)
def _caducar(rng, opos, otip, nobjs, ppos, ptip, pt, npend, t, regen, nobj, tipos, ntipos, fijos, ifij, nfij, nace,
             regen_rota, vida, foto):
    """Mundo.caducar (N2f-v3): sobre una FOTO de objs en orden de insercion, lo que lleva `vida` pasos sin morderse
    se retira por el mismo camino que una mordida. Devuelve tambien cuantos caducaron."""
    nf = 0
    for i in range(nobjs):
        if t - nace[opos[i]] >= vida:
            foto[nf] = opos[i]; nf += 1
    cad = 0
    for i in range(nf):
        x = foto[i]
        hay = False
        for z in range(nobjs):
            if opos[z] == x:
                hay = True; break
        if hay:
            nobjs, npend, ifij = _retirar(rng, opos, otip, nobjs, ppos, ptip, pt, npend, x, t, regen, nobj, tipos,
                                          ntipos, fijos, ifij, nfij, nace, regen_rota)
            cad += 1
    return nobjs, npend, ifij, cad


@njit(cache=True)
def _see(pos, t, opos, otip, nobjs, rech, memoria_rechazo):
    """Organismo.see: el objeto mas cercano en orden de insercion, con la memoria de trabajo de rechazo."""
    best_d = 0; best_k = -1; best_left = False; found = False
    for i in range(nobjs):
        x = opos[i]
        if memoria_rechazo > 0 and rech[x] > t: continue
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


# ------------------------------------------------------------------ valor (las dos vias + puerta)
@njit(cache=True)
def _valor(i, kk, KW, activa, Wp, Wn, Wps, Wns, PATM, ipar):
    """Organismo.valor(kk) = _total(P_[kk], kenyon(P_[kk]), Wp-Wn)[0]."""
    P = PATM[i, kk]
    kc = _code(KW[i], activa[i], P)
    Wb = Wp[i] - Wn[i]
    _wf = Wb @ kc; _ws = (Wps[i] - Wns[i]) @ P
    puerta = ipar[i, I_PUERTA]
    if puerta < 0: return _wf + _ws
    nfam = 0
    for c in range(NKMAX):
        if kc[c] > 0 and abs(Wb[c]) > 0.2: nfam += 1
    return _wf if nfam >= puerta else _ws


@njit(cache=True)
def _criterios(i, t, invertir_en, es_AB, valc, KW, activa, Wp, Wn, Wps, Wns, PATM, ipar, n_crit_v, n_crit_ok,
               veneno_propio, cnt):
    """Organismo._criterios (solo en el mundo 'AB'; A=0, B=1). Respeta los cortocircuitos del original."""
    if not es_AB: return
    for kk in range(2):
        if (not n_crit_ok[i, kk]) and valc[kk] == -1:
            if _valor(i, kk, KW, activa, Wp, Wn, Wps, Wns, PATM, ipar) <= -2.5:
                n_crit_ok[i, kk] = True; n_crit_v[i, kk] = veneno_propio[i, kk]
    if invertir_en >= 0 and t >= invertir_en and cnt[i, C_TEXTB] < 0:
        if _valor(i, 1, KW, activa, Wp, Wn, Wps, Wns, PATM, ipar) >= 0: cnt[i, C_TEXTB] = t
    if cnt[i, C_TBOK] < 0:
        if _valor(i, 1, KW, activa, Wp, Wn, Wps, Wns, PATM, ipar) >= 0.5: cnt[i, C_TBOK] = t


# ------------------------------------------------------------------ aprendizaje (bloque de organismo_v13)
@njit(cache=True)
def _aprender(i, kk, P, kc, Wb, R, factor, t, dividir, KW, activa, Wp, Wn, Wps, Wns, err, mu, st_t, st_k, cnt,
              fpar, ipar):
    """Organismo._aprender: una experiencia con refuerzo R sobre el patron kk (propia factor 1, vicaria factor
    f_vicaria y sin dividir). Wb es la FOTO de Wp-Wn de antes de tocar nada (como en el original)."""
    eta = fpar[i, F_ETA] * factor; lam = fpar[i, F_LAM]; aversion = fpar[i, F_AVERSION]
    eta_s = fpar[i, F_ETA_S]; clip_s = fpar[i, F_CLIP_S]; puerta = ipar[i, I_PUERTA]
    _wf = Wb @ kc; _ws = (Wps[i] - Wns[i]) @ P
    if puerta < 0:
        _wt = _wf + _ws
    else:
        nfam = 0
        for c in range(NKMAX):
            if kc[c] > 0 and abs(Wb[c]) > 0.2: nfam += 1
        _wt = _wf if nfam >= puerta else _ws
    dlt = (R - _wt) if puerta < 0 else (R - _wf)
    if eta_s != 0.0:
        _ds = dlt if puerta < 0 else (R - _ws)
        if lam != 0.0:
            for j in range(6):
                if P[j] > 0:
                    _mcs = min(Wps[i, j], Wns[i, j]); Wps[i, j] = Wps[i, j] - lam * _mcs; Wns[i, j] = Wns[i, j] - lam * _mcs
                else:
                    Wps[i, j] = Wps[i, j] - lam * 0.0; Wns[i, j] = Wns[i, j] - lam * 0.0
        if _ds > 0:
            for j in range(6): Wps[i, j] = min(max(Wps[i, j] + eta_s * factor * _ds * P[j], 0.0), clip_s)
        else:
            for j in range(6): Wns[i, j] = min(max(Wns[i, j] + eta_s * factor * aversion * (-_ds) * P[j], 0.0), clip_s)
    if lam != 0.0:
        for c in range(NKMAX):
            if kc[c] > 0:
                mcom = min(Wp[i, c], Wn[i, c]); Wp[i, c] -= lam * mcom; Wn[i, c] -= lam * mcom
    if dlt > 0:
        for c in range(NKMAX): Wp[i, c] = min(max(Wp[i, c] + eta * dlt * kc[c], 0.0), 3.0)
    else:
        for c in range(NKMAX): Wn[i, c] = min(max(Wn[i, c] + eta * aversion * (-dlt) * kc[c], 0.0), 3.0)
    if dividir and ipar[i, I_PLAST] != 0:
        ema = fpar[i, F_EMA]; paso = fpar[i, F_PASO]; theta = fpar[i, F_THETA]
        mu_norm = ipar[i, I_MU_NORM]; div_signo = ipar[i, I_DIV_SIGNO]
        nidx = 0; idxs = np.zeros(K, np.int64)
        for c in range(NKMAX):
            if kc[c] > 0:
                idxs[nidx] = c; nidx += 1
        for a in range(nidx):
            c = idxs[a]
            err[i, c] = (1 - ema) * err[i, c] + ema * abs(dlt)
            for j in range(6): mu[i, c, j] = (1 - ema) * mu[i, c, j] + ema * P[j]
        sP = 0.0
        for j in range(6): sP += P[j]
        for a in range(nidx):
            c = idxs[a]
            if div_signo != 0:
                smu = 0.0
                for j in range(6): smu += mu[i, c, j]
                dist = np.empty(6); kj = np.empty(6)
                for j in range(6):
                    dist[j] = P[j] - (mu[i, c, j] * (sP / max(smu, 1e-9)) if mu_norm != 0 else mu[i, c, j])
                    kj[j] = min(max(KW[i, c, j] * (1 - 0.05) + paso * dist[j], 0.0), 5.0) * (1.0 if P[j] > 0 else 0.0)
                libre = -1
                for z in range(NKMAX):
                    if not activa[i, z]:
                        libre = z; break
                if Wb[c] * R < 0 and abs(Wb[c]) > 0.2 and (kj @ P) > (KW[i, c] @ P) and libre >= 0:
                    jn = libre; activa[i, jn] = True
                    for j in range(6): KW[i, jn, j] = kj[j]
                    if R > 0:
                        Wp[i, jn] = Wp[i, c]; Wn[i, jn] = 0.; Wp[i, c] = 0.
                    else:
                        Wn[i, jn] = Wn[i, c]; Wp[i, jn] = 0.; Wn[i, c] = 0.
                    for j in range(6): mu[i, jn, j] = P[j] * (smu / sP)
                    err[i, c] = 0.0; err[i, jn] = 0.0
                    cnt[i, C_SPLITS] += 1; st_t[i, cnt[i, C_NST]] = t; st_k[i, cnt[i, C_NST]] = kk; cnt[i, C_NST] += 1
            elif err[i, c] > theta:
                libre = -1
                for z in range(NKMAX):
                    if not activa[i, z]:
                        libre = z; break
                if libre >= 0:
                    jn = libre; activa[i, jn] = True
                    smu = 0.0
                    for j in range(6): smu += mu[i, c, j]
                    for j in range(6):
                        dj = P[j] - (mu[i, c, j] * (sP / max(smu, 1e-9)) if mu_norm != 0 else mu[i, c, j])
                        KW[i, jn, j] = min(max(KW[i, c, j] + paso * dj, 0.0), 5.0)
                        KW[i, c, j] = min(max(KW[i, c, j] - paso * dj, 0.0), 5.0)
                    Wp[i, jn] = Wp[i, c]; Wn[i, jn] = Wn[i, c]
                    for j in range(6): mu[i, jn, j] = mu[i, c, j]
                    err[i, c] = 0.0; err[i, jn] = 0.0
                    cnt[i, C_SPLITS] += 1; st_t[i, cnt[i, C_NST]] = t; st_k[i, cnt[i, C_NST]] = kk; cnt[i, C_NST] += 1


# ------------------------------------------------------------------ canales sociales
@njit(cache=True)
def _recibir(i, kk, signo, f_vicaria, t, invertir_en, es_AB, valc, KW, activa, Wp, Wn, Wps, Wns, err, mu, PATM,
             st_t, st_k, cnt, fpar, ipar, n_crit_v, n_crit_ok, veneno_propio, vicarias, vicarias_signo,
             s_ult_v, s_ult_t):
    """Organismo.recibir: aprendizaje vicario (escala innata + -> +1, - -> -3), sin divisiones."""
    if fpar[i, F_GAMMA_SOC] != 0.0:
        s_ult_v[i, kk] = 1.0 if signo > 0 else -1.0; s_ult_t[i, kk] = t
    if ipar[i, I_LEARN] == 0: return
    P = PATM[i, kk]
    kc = _code(KW[i], activa[i], P); Wb = Wp[i] - Wn[i]
    _aprender(i, kk, P, kc, Wb, 1.0 if signo > 0 else -3.0, f_vicaria, t, False, KW, activa, Wp, Wn, Wps, Wns,
              err, mu, st_t, st_k, cnt, fpar, ipar)
    vicarias[i, kk] += 1; vicarias_signo[i, kk, 0 if signo > 0 else 1] += 1
    if es_AB and kk == 1 and signo < 0 and not n_crit_ok[i, 1]: cnt[i, C_AVISOS_B] += 1
    _criterios(i, t, invertir_en, es_AB, valc, KW, activa, Wp, Wn, Wps, Wns, PATM, ipar, n_crit_v, n_crit_ok,
               veneno_propio, cnt)


@njit(cache=True)
def _recibir_simbolo(i, kk, s, f_vicaria, t, invertir_en, es_AB, valc, KW, activa, Wp, Wn, Wps, Wns, err, mu, PATM,
                     st_t, st_k, cnt, fpar, ipar, n_crit_v, n_crit_ok, veneno_propio, vicarias, vicarias_signo,
                     M, traza_t, ultimo_s, ultimo_t, K_sim):
    """Organismo.recibir_simbolo (N2): traza, alineacion opcional (N2e) y aprendizaje por CONTRASTE M[s]-mean(M)."""
    traza_t[i, s, kk] = t; cnt[i, C_SIMREC] += 1; ultimo_s[i, kk] = s; ultimo_t[i, kk] = t
    learn = ipar[i, I_LEARN]
    P = PATM[i, kk]
    if ipar[i, I_ALINEA] != 0 and learn != 0:
        _kc = _code(KW[i], activa[i], P); _Wb = Wp[i] - Wn[i]
        nfam = 0
        for c in range(NKMAX):
            if _kc[c] > 0 and abs(_Wb[c]) > 0.2: nfam += 1
        if nfam >= 3:
            M[i, s] += fpar[i, F_ETA_M] * ((_Wb @ _kc) - M[i, s]); cnt[i, C_ALIN] += 1
    sm = 0.0
    for z in range(K_sim): sm += M[i, z]
    R_hat = M[i, s] - sm / K_sim
    # N2f: el que ya sabe del patron mas de lo que el simbolo dice no se deja desensenar (con la perilla apagada
    # valor(kk) ni se evalua; valor/kenyon/code no tocan estado ni RNG)
    _sabe_mas = ipar[i, I_ESC_NO_SABE] != 0 and abs(_valor(i, kk, KW, activa, Wp, Wn, Wps, Wns, PATM, ipar)) >= abs(R_hat)
    if _sabe_mas and abs(R_hat) >= fpar[i, F_U_M]: cnt[i, C_NODES] += 1
    if learn != 0 and abs(R_hat) >= fpar[i, F_U_M] and not _sabe_mas:
        kc = _code(KW[i], activa[i], P); Wb = Wp[i] - Wn[i]
        _aprender(i, kk, P, kc, Wb, R_hat, f_vicaria, t, False, KW, activa, Wp, Wn, Wps, Wns, err, mu, st_t, st_k,
                  cnt, fpar, ipar)
        cnt[i, C_DECOD] += 1; vicarias[i, kk] += 1; vicarias_signo[i, kk, 0 if R_hat > 0 else 1] += 1
    _criterios(i, t, invertir_en, es_AB, valc, KW, activa, Wp, Wn, Wps, Wns, PATM, ipar, n_crit_v, n_crit_ok,
               veneno_propio, cnt)


@njit(cache=True)
def _emitir(i, st, t, q, rngs_q, Pq, emis, emis_q4, fpar, K_sim):
    """Organismo.emitir: softmax(beta_q*Pq[st]) y un sorteo del RNG propio. rng.choice(K,p=p) consume UN random():
    cdf=cumsum(p); cdf/=cdf[-1]; idx=searchsorted(cdf,u,'right') (replicado y comprobado contra NumPy)."""
    p = np.empty(K_sim); tot = 0.0
    for z in range(K_sim):
        p[z] = np.exp(fpar[i, F_BETA_Q] * Pq[i, st, z]); tot += p[z]
    for z in range(K_sim): p[z] = p[z] / tot
    u = rngs_q[i].random()
    cdf = np.cumsum(p)
    for z in range(K_sim): cdf[z] = cdf[z] / cdf[K_sim - 1]
    s = K_sim - 1
    for z in range(K_sim):
        if u < cdf[z]:
            s = z; break
    emis[i, st, s] += 1
    if q == 3: emis_q4[i, st, s] += 1
    return s


@njit(cache=True)
def _reforzar(i, st, s, r, Pq, b, refuerzos, fpar, ipar):
    """Organismo.reforzar: ventaja sobre la linea base del estado (N2b) y clip de la preferencia."""
    if ipar[i, I_BASELINE_Q] != 0:
        adv = r - b[i, st]
        b[i, st] += fpar[i, F_RHO_B] * (r - b[i, st])
    else:
        adv = r
    Pq[i, st, s] = min(max(Pq[i, st, s] + fpar[i, F_ETA_Q] * adv, -3.0), 3.0)
    refuerzos[i, 0 if r > 0 else 1] += 1


# ------------------------------------------------------------------ bucle principal
@njit(cache=True)
def _bucle(rngs, rng_mundo, rng_senal, rngs_q, n, T, nobj, tipos, ntipos_ini, ntipos, fijos, nfij, regen, senal,
           d_senal, f_vicaria, tau_s, K_sim, cod_emisor, u_v, mudo_desde, invertir_en, es_AB, valc, NPAT, PATM,
           fpar, ipar, Wl, KW, activa, Wp, Wn, err, mu, Wps, Wns, Pq, maxpend, regen_rota, vida):
    el = np.zeros((n, 2, 9)); tr = np.zeros((n, 9))
    M = np.zeros((n, K_sim)); b = np.zeros((n, 2))
    emis = np.zeros((n, 2, K_sim), np.int64); emis_q4 = np.zeros((n, 2, K_sim), np.int64)
    refuerzos = np.zeros((n, 2), np.int64)
    rech = np.full((n, L), -1, np.int64)
    cnt = np.zeros((n, NC), np.int64); est = np.zeros((n, NE))
    st_t = np.zeros((n, MAXSPLIT), np.int64); st_k = np.zeros((n, MAXSPLIT), np.int64)
    mord = np.zeros((n, NPAT, 4), np.int64); vis = np.zeros((n, NPAT, 4), np.int64); dq = np.zeros((n, 4), np.int64)
    veneno_propio = np.zeros((n, NPAT), np.int64)
    n_crit_v = np.zeros((n, NPAT), np.int64); n_crit_ok = np.zeros((n, NPAT), np.bool_)
    vicarias = np.zeros((n, NPAT), np.int64); vicarias_signo = np.zeros((n, NPAT, 2), np.int64)
    traza_t = np.full((n, K_sim, NPAT), -1, np.int64)
    ultimo_s = np.zeros((n, NPAT), np.int64); ultimo_t = np.full((n, NPAT), -1, np.int64)
    s_ult_v = np.zeros((n, NPAT)); s_ult_t = np.full((n, NPAT), -1, np.int64)
    for i in range(n):
        cnt[i, C_PREV_ON] = -1; cnt[i, C_TEXTB] = -1; cnt[i, C_TBOK] = -1
        est[i, E_E] = 1.0
    # Mundo
    opos = np.full(nobj + 2, -1, np.int64); otip = np.full(nobj + 2, -1, np.int64); nobjs = 0
    ppos = np.full(nobj + 2, -1, np.int64); ptip = np.full(nobj + 2, -1, np.int64); pt = np.zeros(nobj + 2, np.int64)
    nace = np.zeros(L, np.int64); foto = np.zeros(nobj + 2, np.int64); caducados = 0   # N2f-v3
    npend = 0; ifij = 0
    # el spawn inicial ocurre con mundo.t = 0 (Mundo.__init__), antes del primer paso
    nobjs, ifij = _spawn(rng_mundo, opos, otip, nobjs, ppos, npend, nobj, tipos, ntipos_ini, fijos, ifij, nfij, nace, 0)
    # N2: emisiones pendientes de resolucion (lista en orden de insercion)
    pe_i = np.zeros(maxpend, np.int64); pe_kk = np.zeros(maxpend, np.int64); pe_st = np.zeros(maxpend, np.int64)
    pe_s = np.zeros(maxpend, np.int64); pe_t = np.zeros(maxpend, np.int64); pe_ok = np.zeros(maxpend, np.bool_)
    npe = 0
    # emisiones del paso
    em_i = np.zeros(n, np.int64); em_px = np.zeros(n, np.int64); em_kk = np.zeros(n, np.int64)
    em_sg = np.zeros(n, np.int64); nem = 0
    x = np.empty(9); m = np.zeros(2)
    q_div = T // 4
    for t in range(T):
        if npend > 0:
            nobjs, npend = _regenerar(rng_mundo, opos, otip, nobjs, ppos, ptip, pt, npend, t, tipos, ntipos,
                                      regen_rota, nace)
        if vida >= 0:   # N2f-v3
            nobjs, npend, ifij, _cad = _caducar(rng_mundo, opos, otip, nobjs, ppos, ptip, pt, npend, t, regen, nobj,
                                                tipos, ntipos, fijos, ifij, nfij, nace, regen_rota, vida, foto)
            caducados += _cad
        if invertir_en >= 0 and t == invertir_en and es_AB:
            valc[0] = -1; valc[1] = 1
        q = min(t // q_div, 3)
        nem = 0
        for oi in range(n):
            i = oi if t % 2 == 0 else n - 1 - oi
            # ---------------- fase A ----------------
            mem_rech = ipar[i, I_MEM_RECH]; learn = ipar[i, I_LEARN]; puerta = ipar[i, I_PUERTA]
            hambre = min(max(1 - est[i, E_E], 0.0), 1.0); est[i, E_HAMBRE] = hambre
            pos = cnt[i, C_POS]
            d, k, left = _see(pos, t, opos, otip, nobjs, rech[i], mem_rech)
            pat = PATM[i, k]
            for j in range(6): x[j] = pat[j] * 1.2
            x[6] = 1.5 if left else 0.0; x[7] = 0.0 if left else 1.5; x[8] = 1.0 if d == 0 else 0.0
            noise = .15 + .5 * hambre
            V = Wl[i] @ x
            p = 1 / (1 + np.exp(-(V - .8) / noise))
            u = p + rngs[i].normal(0, .3, 2)
            m[0] = 0.0; m[1] = 0.0
            if u.max() > .5: m[np.argmax(u)] = 1
            for j in range(9): tr[i, j] = tr[i, j] * .7 + x[j]
            if learn != 0:
                for a in range(2):
                    for j in range(9): el[i, a, j] = el[i, a, j] * fpar[i, F_TAU_E] + (m[a] - p[a]) * tr[i, j]
            pos = (pos + int(m[1] - m[0])) % L; cnt[i, C_POS] = pos
            d2, _k2, _l2 = _see(pos, t, opos, otip, nobjs, rech[i], mem_rech)
            est[i, E_RP] = .2 if d2 < d else 0.0
            est[i, E_R] = 0.0
            hay = -1
            for z in range(nobjs):
                if opos[z] == pos:
                    hay = z; break
            if hay >= 0:
                kk = otip[hay]; P = PATM[i, kk]
                kc = _code(KW[i], activa[i], P); Wb = Wp[i] - Wn[i]
                _wf = Wb @ kc; _ws = (Wps[i] - Wns[i]) @ P
                if puerta < 0:
                    _wt = _wf + _ws
                else:
                    nfam = 0
                    for c in range(NKMAX):
                        if kc[c] > 0 and abs(Wb[c]) > 0.2: nfam += 1
                    _wt = _wf if nfam >= puerta else _ws
                if fpar[i, F_GAMMA_SIM] != 0.0 and ultimo_t[i, kk] >= 0 and t - ultimo_t[i, kk] <= ipar[i, I_TAU_M]:
                    sm = 0.0
                    for z in range(K_sim): sm += M[i, z]
                    _wt = _wt + fpar[i, F_GAMMA_SIM] * (M[i, ultimo_s[i, kk]] - sm / K_sim)
                if fpar[i, F_GAMMA_SOC] != 0.0 and s_ult_t[i, kk] >= 0 and t - s_ult_t[i, kk] <= ipar[i, I_TAU_SOC]:
                    _wt = _wt + fpar[i, F_GAMMA_SOC] * s_ult_v[i, kk]; cnt[i, C_NSESGO] += 1
                Vb = fpar[i, F_ALPHA] * _wt + fpar[i, F_HAMBRE_BOCA] * hambre + .5
                pb = 1 / (1 + np.exp(-Vb / .3)); mordio = rngs[i].random() < pb
                vis[i, kk, q] += 1
                if mem_rech > 0 and not mordio: rech[i, pos] = t + mem_rech
                emitida = True; R = 0.0
                if mordio:
                    R = 1.0 if valc[kk] == 1 else -3.0
                    est[i, E_R] = R
                    est[i, E_E] = min(est[i, E_E] + (0.8 if valc[kk] == 1 else -0.4), 1.5)
                    mord[i, kk, q] += 1
                    if valc[kk] == -1: veneno_propio[i, kk] += 1
                    nobjs, npend, ifij = _retirar(rng_mundo, opos, otip, nobjs, ppos, ptip, pt, npend, pos, t, regen,
                                                  nobj, tipos, ntipos, fijos, ifij, nfij, nace, regen_rota)
                    rech[i, pos] = -1
                    if learn != 0:
                        _aprender(i, kk, P, kc, Wb, R, 1.0, t, True, KW, activa, Wp, Wn, Wps, Wns, err, mu, st_t,
                                  st_k, cnt, fpar, ipar)
                        for z in range(K_sim):   # _actualizar_M (no-op sin simbolos: la traza esta vacia)
                            if traza_t[i, z, kk] >= 0 and t - traza_t[i, z, kk] <= ipar[i, I_TAU_M]:
                                M[i, z] += fpar[i, F_ETA_M] * (R - M[i, z])
                _criterios(i, t, invertir_en, es_AB, valc, KW, activa, Wp, Wn, Wps, Wns, PATM, ipar, n_crit_v,
                           n_crit_ok, veneno_propio, cnt)
            else:
                emitida = False; kk = -1; R = 0.0; mordio = False
            hay2 = -1
            for z in range(nobjs):
                if opos[z] == pos:
                    hay2 = z; break
            cnt[i, C_PREV_ON] = pos if hay2 >= 0 else -1
            est[i, E_E] -= fpar[i, F_COSTO]
            # ---------------- senal emitida por la visita ----------------
            if not emitida: continue
            px = pos
            if (senal == S_SIMBOLO or senal == S_SIMBOLO_BARAJADO) and n > 1:
                st = -1
                if cod_emisor == 1:   # N2c: el estado es lo que el emisor SABE; si no sabe, calla
                    _v = _valor(i, kk, KW, activa, Wp, Wn, Wps, Wns, PATM, ipar)
                    if _v >= u_v: st = 1
                    elif _v <= -u_v: st = 0
                elif cod_emisor == 2:   # N2d: habla solo de lo que su via RAPIDA conoce
                    _P = PATM[i, kk]; _kc = _code(KW[i], activa[i], _P); _Wb = Wp[i] - Wn[i]
                    nfam = 0
                    for c in range(NKMAX):
                        if _kc[c] > 0 and abs(_Wb[c]) > 0.2: nfam += 1
                    _v = _Wb @ _kc
                    if nfam >= 3 and _v >= u_v: st = 1
                    elif nfam >= 3 and _v <= -u_v: st = 0
                else:
                    st = 1 if mordio else 0
                _c = 1 if mordio else 0
                w = 0
                for z in range(npe):
                    if pe_i[z] != i and pe_kk[z] == kk and t - pe_t[z] <= tau_s and not pe_ok[z]:
                        _reforzar(pe_i[z], pe_st[z], pe_s[z], 1.0 if _c == pe_st[z] else -1.0, Pq, b, refuerzos,
                                  fpar, ipar)
                        pe_ok[z] = True
                    if (not pe_ok[z]) and t - pe_t[z] <= tau_s:
                        pe_i[w] = pe_i[z]; pe_kk[w] = pe_kk[z]; pe_st[w] = pe_st[z]; pe_s[w] = pe_s[z]
                        pe_t[w] = pe_t[z]; pe_ok[w] = False; w += 1
                npe = w
                if st >= 0:
                    sim_s = _emitir(i, st, t, q, rngs_q, Pq, emis, emis_q4, fpar, K_sim)
                    em_i[nem] = i; em_px[nem] = px; em_kk[nem] = kk; em_sg[nem] = sim_s; nem += 1
                    cnt[i, C_SEMIT] += 1
                    if npe >= maxpend: raise ValueError("mundo_social_n3_rapido: desborde del buffer de pendientes")
                    pe_i[npe] = i; pe_kk[npe] = kk; pe_st[npe] = st; pe_s[npe] = sim_s; pe_t[npe] = t; pe_ok[npe] = False
                    npe += 1
            elif senal == S_HONESTA or senal == S_BARAJADA:
                if mordio:
                    em_i[nem] = i; em_px[nem] = px; em_kk[nem] = kk; em_sg[nem] = 1 if R > 0 else -1; nem += 1
                    cnt[i, C_SEMIT] += 1
            elif senal == S_CONDUCTA or senal == S_BARAJADA_CONDUCTA:
                em_i[nem] = i; em_px[nem] = px; em_kk[nem] = kk; em_sg[nem] = 1 if mordio else -1; nem += 1
                cnt[i, C_SEMIT] += 1
        # ---------------- entrega de senales ----------------
        if senal != S_NONE and n > 1 and (mudo_desde < 0 or t < mudo_desde):
            for z in range(nem):
                i = em_i[z]; px = em_px[z]; kk = em_kk[z]; signo = em_sg[z]
                if senal == S_SIMBOLO:
                    sig = signo
                elif senal == S_SIMBOLO_BARAJADO:
                    sig = rng_senal.integers(0, K_sim)
                elif senal == S_HONESTA or senal == S_CONDUCTA:
                    sig = signo
                else:
                    sig = 1 if rng_senal.random() < .5 else -1
                for j in range(n):
                    if j == i: continue
                    dl = (cnt[j, C_POS] - px) % L; dist = min(dl, L - dl)
                    if dist <= d_senal:
                        if senal == S_SIMBOLO or senal == S_SIMBOLO_BARAJADO:
                            _recibir_simbolo(j, kk, sig, f_vicaria, t, invertir_en, es_AB, valc, KW, activa, Wp, Wn,
                                             Wps, Wns, err, mu, PATM, st_t, st_k, cnt, fpar, ipar, n_crit_v,
                                             n_crit_ok, veneno_propio, vicarias, vicarias_signo, M, traza_t,
                                             ultimo_s, ultimo_t, K_sim)
                        elif ipar[j, I_ESCUCHA] != 0:
                            _recibir(j, kk, sig, f_vicaria, t, invertir_en, es_AB, valc, KW, activa, Wp, Wn, Wps, Wns,
                                     err, mu, PATM, st_t, st_k, cnt, fpar, ipar, n_crit_v, n_crit_ok, veneno_propio,
                                     vicarias, vicarias_signo, s_ult_v, s_ult_t)
                        cnt[j, C_SRECIB] += 1
        # ---------------- olvido del mundo ----------------
        if rng_mundo.random() < .003 and nobjs > 0:
            _dx = opos[rng_mundo.integers(0, nobjs)]
            nobjs, npend, ifij = _retirar(rng_mundo, opos, otip, nobjs, ppos, ptip, pt, npend, _dx, t, regen, nobj,
                                          tipos, ntipos, fijos, ifij, nfij, nace, regen_rota)
            for i in range(n): rech[i, _dx] = -1
        # ---------------- fase B ----------------
        for oi in range(n):
            i = oi if t % 2 == 0 else n - 1 - oi
            if ipar[i, I_LEARN] != 0:
                lr = fpar[i, F_ETA] * (1 + 2 * est[i, E_HAMBRE]) * (max(est[i, E_R], 0.0) + est[i, E_RP])
                for a in range(2):
                    for j in range(9): Wl[i, a, j] = min(max(Wl[i, a, j] + lr * el[i, a, j], 0.0), 1.5)
            if est[i, E_E] <= 0:
                cnt[i, C_DEATHS] += 1; est[i, E_E] = .6; cnt[i, C_POS] = rngs[i].integers(0, L)
                dq[i, q] += 1
    return (Wp, Wn, Wps, Wns, KW, activa, err, mu, Wl, M, Pq, b, emis, emis_q4, refuerzos, cnt, mord, vis, dq,
            veneno_propio, n_crit_v, n_crit_ok, vicarias, vicarias_signo, st_t, st_k, caducados)


def run(seed, n=1, T=100000, invertir_en=None, senal=None, d_senal=5, f_vicaria=1 / 3, nobj_por_org=4, compat=True,
        estados=None, devolver_estado=False, mundo='AB', regla='azar', tau_s=200, K_sim=2, estado_emisor='conducta', u_v=0.5,
        mascaras=None, kw_por_org=None, regen=None, tipos_fijos=None, mudo_desde=None, regen_rota=False, vida=None, **kw_org):
    """Misma firma y misma salida que mundo_social_n3.run (lista de dicts, uno por organismo)."""
    if senal not in COD_SENAL:
        raise ValueError(f"mundo_social_n3_rapido: senal desconocida {senal!r} (el original la trataria como None)")
    if K_sim >= 8:
        raise NotImplementedError("mundo_social_n3_rapido: K_sim>=8 activa la suma por pares de NumPy; no cubierto")
    if estado_emisor not in COD_EMISOR:
        raise ValueError(f"mundo_social_n3_rapido: estado_emisor desconocido {estado_emisor!r}")
    for _k, _v in (('T', T), ('n', n), ('d_senal', d_senal), ('tau_s', tau_s), ('K_sim', K_sim), ('regen', regen),
                   ('mudo_desde', mudo_desde), ('invertir_en', invertir_en), ('nobj_por_org', nobj_por_org),
                   ('vida', vida)):
        _ent(_v, _k)
    if n < 1: return []
    # --- patrones, valencias y particion: EXACTAMENTE las lineas del original ---
    if mundo == 'AB':
        pats, tren, test, val = PAT, ['A', 'B'], [], {'A': 'comida', 'B': 'veneno'}
    else:
        import os as _os, sys as _sys
        _sys.path.insert(0, _os.path.join(_os.path.dirname(_os.path.dirname(_os.path.abspath(__file__))), 'v13_dos_vias'))
        from organismo_v13g import split_regla
        pats, tren, test, val = split_regla(seed, regla); val = dict(val)
    nombres = list(pats)                      # orden de insercion del dict de patrones
    ind = {k: j for j, k in enumerate(nombres)}
    NPAT = len(nombres)
    es_AB = (mundo == 'AB')
    if es_AB and (nombres[0] != 'A' or nombres[1] != 'B'):
        raise AssertionError("mundo_social_n3_rapido: se esperaba A,B como primeros patrones")
    rngs = [np.random.default_rng(seed + 100000 * i) for i in range(n)]
    rngs_q = [np.random.default_rng(seed + 500000 * i + 7) if senal in SIMBOLOS else None for i in range(n)]
    _pats_i = lambda i: pats if (mascaras is None or mascaras[i] is None) else {k: v * np.asarray(mascaras[i], float) for k, v in pats.items()}
    _kw_i = lambda i: dict(kw_org, **(kw_por_org[i] if kw_por_org else {}))
    # --- parametros por organismo ---
    fpar = np.zeros((n, NF)); ipar = np.zeros((n, NI), np.int64)
    PATM = np.zeros((n, NPAT, 6))
    for i in range(n):
        kwi = _kw_i(i)
        malas = [k for k in kwi if k not in DEFAULTS]
        if malas:
            raise TypeError(f"mundo_social_n3_rapido: argumento(s) no reconocido(s) {malas}")
        P = dict(DEFAULTS, **kwi)
        for _k in ('memoria_rechazo', 'tau_m', 'tau_soc', 'puerta'): _ent(P[_k], _k)
        fpar[i, F_ETA] = P['eta']; fpar[i, F_TAU_E] = P['tau_e']; fpar[i, F_ALPHA] = P['alpha']
        fpar[i, F_HAMBRE_BOCA] = P['hambre_boca']; fpar[i, F_AVERSION] = P['aversion']; fpar[i, F_COSTO] = P['costo']
        fpar[i, F_THETA] = P['theta']; fpar[i, F_EMA] = P['ema']; fpar[i, F_PASO] = P['paso']; fpar[i, F_LAM] = P['lam']
        fpar[i, F_ETA_S] = P['eta_s']; fpar[i, F_CLIP_S] = P['clip_s']; fpar[i, F_BETA_Q] = P['beta_q']
        fpar[i, F_ETA_Q] = P['eta_q']; fpar[i, F_ETA_M] = P['eta_m']; fpar[i, F_U_M] = P['u_m']
        fpar[i, F_GAMMA_SIM] = P['gamma_sim']; fpar[i, F_RHO_B] = P['rho_b']; fpar[i, F_GAMMA_SOC] = P['gamma_soc']
        ipar[i, I_PLAST] = bool(P['plast']); ipar[i, I_MEM_RECH] = int(P['memoria_rechazo'])
        ipar[i, I_LEARN] = bool(P['learn']); ipar[i, I_MU_NORM] = bool(P['mu_norm'])
        ipar[i, I_DIV_SIGNO] = bool(P['div_signo']); ipar[i, I_PUERTA] = -1 if P['puerta'] is None else int(P['puerta'])
        ipar[i, I_TAU_M] = int(P['tau_m']); ipar[i, I_BASELINE_Q] = bool(P['baseline_q'])
        ipar[i, I_ALINEA] = bool(P['alinea']); ipar[i, I_TAU_SOC] = int(P['tau_soc']); ipar[i, I_ESCUCHA] = bool(P['escucha'])
        ipar[i, I_ESC_NO_SABE] = bool(P['escucha_si_no_sabe'])   # N2f
        pi = _pats_i(i)
        for k, j in ind.items(): PATM[i, j] = pi[k]
    # --- inicializacion de cada organismo: EXACTAMENTE las lineas del original (mismo flujo de azar) ---
    Wl = np.zeros((n, 2, 9)); KW = np.zeros((n, NKMAX, 6)); activa = np.zeros((n, NKMAX), np.bool_)
    Wp = np.zeros((n, NKMAX)); Wn = np.zeros((n, NKMAX)); err = np.zeros((n, NKMAX)); mu = np.zeros((n, NKMAX, 6))
    Wps = np.zeros((n, 6)); Wns = np.zeros((n, 6)); Pq = np.zeros((n, 2, K_sim))
    for i in range(n):
        rng = rngs[i]
        Wl[i] = rng.uniform(.1, .4, (2, 9))
        KW[i, :NK] = rng.uniform(0, 1, (NK, 6)); activa[i, :NK] = True

        def code(P, i=i):
            v = KW[i] @ P; v = np.where(activa[i], v, -1e9); return set(np.argsort(v)[-K:])
        while mundo == 'AB' and not (len(code(PAT['A']) & code(PAT['B'])) == 0):
            KW[i, 0:NK] = rng.uniform(0, 1, (NK, 6))
        if rngs_q[i] is not None: Pq[i] = rngs_q[i].uniform(-0.1, 0.1, (2, K_sim))
        if estados is not None and estados[i] is not None:
            e = estados[i]
            KW[i] = e['KW']; activa[i] = e['activa']; Wp[i] = e['Wp']; Wn[i] = e['Wn']
            err[i] = e['err']; mu[i] = e['mu']; Wl[i] = e['Wl']
            Wps[i] = e.get('Wps', 0.); Wns[i] = e.get('Wns', 0.)
    rng_mundo = rngs[0] if (n == 1 and compat) else np.random.default_rng(seed + 900000)
    rng_senal = np.random.default_rng(seed + 300000)
    # --- mundo: tipos (tren al sortear el mundo; test entra en t=0, tras el sorteo inicial) ---
    tipos = np.array([ind[k] for k in list(tren) + list(test)], np.int64)
    ntipos_ini = len(tren); ntipos = len(tipos)
    fijos = np.array([ind[k] for k in tipos_fijos], np.int64) if tipos_fijos else np.zeros(0, np.int64)
    valc = np.zeros(NPAT, np.int64)
    for k, v in val.items(): valc[ind[k]] = 1 if v == 'comida' else -1
    inv = -1 if (invertir_en is None or not ('A' in val and 'B' in val)) else int(invertir_en)
    maxpend = 2 * (int(tau_s) + 2) * n + 16
    dummy = np.random.default_rng(0)
    out = _bucle(tuple(rngs), rng_mundo, rng_senal, tuple(r if r is not None else dummy for r in rngs_q), int(n),
                 int(T), int(nobj_por_org * n), tipos, int(ntipos_ini), int(ntipos), fijos, len(fijos),
                 -1 if regen is None else int(regen), COD_SENAL[senal], int(d_senal), float(f_vicaria), int(tau_s),
                 int(K_sim), COD_EMISOR[estado_emisor], float(u_v), -1 if mudo_desde is None else int(mudo_desde),
                 inv, es_AB, valc, NPAT, PATM, fpar, ipar, Wl, KW, activa, Wp, Wn, err, mu, Wps, Wns, Pq, maxpend,
                 bool(regen_rota), -1 if vida is None else int(vida))
    (Wp, Wn, Wps, Wns, KW, activa, err, mu, Wl, M, Pq, b, emis, emis_q4, refuerzos, cnt, mord, vis, dq,
     veneno_propio, n_crit_v, n_crit_ok, vicarias, vicarias_signo, st_t, st_k, caducados) = out
    # --- lectura final: las mismas lineas del original (mismo redondeo, mismo argsort) ---
    res = []
    for i in range(n):
        P_ = {k: PATM[i, ind[k]] for k in nombres}

        def code(P, i=i):
            v = KW[i] @ P; v = np.where(activa[i], v, -1e9); return set(np.argsort(v)[-K:])

        def kenyon(P, i=i):
            k = np.zeros(NKMAX); k[list(code(P))] = 1; return k

        def valor(kk, i=i):
            kc = kenyon(P_[kk]); Wb = Wp[i] - Wn[i]
            _wf = float(Wb @ kc); _ws = float((Wps[i] - Wns[i]) @ P_[kk])
            if ipar[i, I_PUERTA] < 0: return _wf + _ws
            return _wf if int((np.abs(Wb[kc > 0]) > 0.2).sum()) >= ipar[i, I_PUERTA] else _ws
        W = {k: round(valor(k), 2) for k in P_}
        comp = {k: (round(float(Wp[i] @ kenyon(P_[k])), 2), round(float(Wn[i] @ kenyon(P_[k])), 2)) for k in P_}
        W_lenta = {k: round(float((Wps[i] - Wns[i]) @ P_[k]), 3) for k in P_}
        sim = None
        if senal in SIMBOLOS:
            pref = [int(np.argmax(Pq[i, st])) for st in (0, 1)]
            tot4 = int(emis_q4[i].sum()); cons = (int(emis_q4[i, 0, pref[0]] + emis_q4[i, 1, pref[1]]) / tot4) if tot4 else None
            sim = dict(Pq=[[round(float(z), 3) for z in fila] for fila in Pq[i]], simbolo_rechazo=pref[0],
                       simbolo_muerde=pref[1], distintos=pref[0] != pref[1], consistencia_q4=cons,
                       emis=emis[i].tolist(), emis_q4=emis_q4[i].tolist(), refuerzos=[int(z) for z in refuerzos[i]],
                       b=[round(float(z), 3) for z in b[i]], alineaciones=int(cnt[i, C_ALIN]))
        nst = int(cnt[i, C_NST])
        r = dict(W=W, comp=comp, W_lenta=W_lenta,
                 mord={k: [int(z) for z in mord[i, ind[k]]] for k in nombres},
                 vis={k: [int(z) for z in vis[i, ind[k]]] for k in nombres},
                 deaths=int(cnt[i, C_DEATHS]), splits=int(cnt[i, C_SPLITS]),
                 split_t=[(int(st_t[i, z]), nombres[int(st_k[i, z])]) for z in range(nst)],
                 n_sesgo_soc=int(cnt[i, C_NSESGO]), celdas=int(activa[i].sum()), dq=[int(z) for z in dq[i]],
                 n_crit={k: int(n_crit_v[i, ind[k]]) for k in nombres if n_crit_ok[i, ind[k]]},
                 veneno_propio={k: int(veneno_propio[i, ind[k]]) for k in nombres},
                 vicarias={k: int(vicarias[i, ind[k]]) for k in nombres},
                 vicarias_signo={k: [int(z) for z in vicarias_signo[i, ind[k]]] for k in nombres},
                 avisos_B_antes_crit=int(cnt[i, C_AVISOS_B]),
                 t_ext_B=None if cnt[i, C_TEXTB] < 0 else int(cnt[i, C_TEXTB]),
                 t_B_ok=None if cnt[i, C_TBOK] < 0 else int(cnt[i, C_TBOK]),
                 M=[round(float(z), 3) for z in M[i]], simbolos_recibidos=int(cnt[i, C_SIMREC]),
                 no_desensena=int(cnt[i, C_NODES]),   # N2f
                 decodificados=int(cnt[i, C_DECOD]), simbolos=sim)
        r['senales_emitidas'] = int(cnt[i, C_SEMIT]); r['senales_recibidas'] = int(cnt[i, C_SRECIB])
        r['caducados'] = int(caducados)   # N2f-v3: contador del MUNDO, igual en los n organismos
        if devolver_estado:
            r['estado'] = dict(KW=KW[i].copy(), activa=activa[i].copy(), Wp=Wp[i].copy(), Wn=Wn[i].copy(),
                               err=err[i].copy(), mu=mu[i].copy(), Wl=Wl[i].copy(), Wps=Wps[i].copy(), Wns=Wns[i].copy())
        res.append(r)
    return res
