"""
VALORES_SIM (5-oct-2026). Laboratorio de SIMULACION con datos historicos. Cero dinero real, cero cuentas, cero ordenes,
cero claves. NO es consejo de inversion. Instrumento y criterio: PREREGISTRO.md (escrito antes de calcular nada).

Brazos: (a) comprar y mantener; (b1) momento simple; (b2) reversion simple; (c) azar con la misma frecuencia;
(d) Colonia de ..\\mini_llm\\mini_llm.py sin modificar; (e) Cuarentena del mismo archivo sin modificar.
Un proceso, numpy puro, sin Pool.

  python valores.py --humo                 humo de un proceso con sintetica chica; escribe datos/humo.json
  python valores.py --etapa valida         elige perillas en validacion (datos cortados en 2014-12-31)
  python valores.py --etapa auditoria      truncado bit a bit + barajada (fuga del futuro)
  python valores.py --etapa sintetica      serie sintetica sin y con senal plantada
  python valores.py --congela              escribe datos/CONGELADO.json (sha del codigo y perillas)
  python valores.py --abrir-sellado        UNA sola vez: evalua 2015-2017 y escribe datos/sellado.json
"""
import numpy as np, os, sys, json, csv, time, argparse, hashlib

AQUI = os.path.dirname(os.path.abspath(__file__))
DATOS = os.path.join(AQUI, 'datos')
CSV = os.path.join(DATOS, 'csv', 'all_stocks_2006-01-01_to_2018-01-01.csv')
SHA_CSV = 'd796906ae3797b950d23cea8e4839072c4bde60a6b97886ee6fede9b793e191c'
sys.path.insert(0, os.path.join(AQUI, '..', 'mini_llm'))
import mini_llm as ML                                   # la colonia original, importada sin tocar
ML.L = 155                                              # unica adaptacion (PREREGISTRO 5e): independencia = 5 dias x 31 pasos

FIN_VALID = '2014-12-31'; INI_VALID = '2012-01-03'
CALENT = 250
PB = 1e-4
COSTO = 7.5 * PB; CORTO_DIA = 1.0 * PB; U = 2 * COSTO  # por lado; por dia en corto; umbral de clase (ida y vuelta)
BLOQUE, NBOOT, SEM_BOOT = 20, 5000, 12345
N_AZAR = 500
BAJA, SUBE, NADA = 0, 1, 2
POS_DE = np.array([-1.0, 1.0, 0.0])
P_BASE = np.array([0.0, 1.0, 0.0])                      # el pan congelado: siempre SUBE (= comprar y mantener)
REJ_MOM = [20, 60, 120, 250]; REJ_REV = [1, 5]
REJ_D = [dict(theta=th, c_exist=ce, adaptativa=ad) for th in (0.8, 0.9, 0.95) for ce in (0.002, 0.01) for ad in (False, True)]
REJ_E = [dict(k=k, theta=th) for k in (2, 5, 10) for th in (0.8, 0.9, 0.95)]
C_CUPO = 200; PLAZO = 60 * 31


def sha256(f):
    h = hashlib.sha256()
    with open(f, 'rb') as fh:
        for b in iter(lambda: fh.read(1 << 20), b''): h.update(b)
    return h.hexdigest()


# ================================================================ datos
def carga_real(abrir=False):
    """devuelve dict(fechas, nombres, C[T,N], V[T,N], errores). Sin abrir: corta FISICAMENTE en FIN_VALID."""
    assert sha256(CSV) == SHA_CSV, 'el CSV no es el anotado'
    filas = {}
    for r in csv.DictReader(open(CSV, encoding='utf-8')):
        if not abrir and r['Date'] > FIN_VALID: continue
        filas.setdefault(r['Name'], {})[r['Date']] = (r['Close'], r['Volume'])
    nombres = sorted(filas); fechas = sorted(set(d for n in nombres for d in filas[n]))
    T, N = len(fechas), len(nombres); C = np.full((T, N), np.nan); V = np.full((T, N), np.nan); relleno = 0
    for j, n in enumerate(nombres):
        for i, d in enumerate(fechas):
            v = filas[n].get(d)
            if v and v[0] not in ('', None):
                C[i, j] = float(v[0]); V[i, j] = float(v[1]) if v[1] not in ('', None) else np.nan
        for i in range(T):                                # relleno hacia adelante (causal)
            if np.isnan(C[i, j]):
                relleno += 1; C[i, j] = C[i - 1, j] if i else np.nan
            if np.isnan(V[i, j]) or V[i, j] <= 0: V[i, j] = V[i - 1, j] if i else 1.0
        if np.isnan(C[0, j]):                             # sin primer dia: rellena hacia atras solo el arranque
            k = int(np.argmax(~np.isnan(C[:, j]))); C[:k, j] = C[k, j]
    return dict(fechas=fechas, nombres=nombres, C=C, V=V, relleno=relleno, meses=[d[:7] for d in fechas])


def sintetica(senal, seed=20261005, T=3020, N=31):
    rng = np.random.default_rng(seed); deriva = 4 * PB; sm, si = 0.009, 0.012; sig = np.sqrt(sm ** 2 + si ** 2)
    R = np.zeros((T, N)); m = rng.normal(0, sm, T); e = rng.normal(0, si, (T, N))
    for t in range(1, T):
        mu = np.full(N, deriva)
        if senal and t >= 6:
            z5 = R[t - 5:t].sum(0) / (sig * np.sqrt(5)); mu = mu - 15 * PB * np.clip(z5, -2, 2)
        R[t] = mu + m[t] + e[t]
    C = 100 * np.cumprod(1 + R, 0); V = np.exp(rng.normal(14, 0.4, (T, N)))
    return dict(fechas=['d%05d' % i for i in range(T)], nombres=['S%02d' % i for i in range(N)], C=C, V=V, relleno=0,
                meses=['m%04d' % (i // 21) for i in range(T)])


def rend(C):
    R = np.zeros_like(C); R[1:] = C[1:] / C[:-1] - 1; err = np.abs(R) > 0.40
    lista = [(int(a), int(b), float(R[a, b])) for a, b in zip(*np.where(err))]; R[err] = 0.0
    return R, lista


# ------------------------------------------------ rasgos causales (solo sumas acumuladas hacia atras: prefijo-estables)
def rsum(a, n):
    cs = np.cumsum(a, 0); out = cs.copy(); out[n:] = cs[n:] - cs[:-n]; return out
def rcnt(T, n): return np.minimum(np.arange(1, T + 1), n).astype(float)
def rmean(a, n): return rsum(a, n) / rcnt(len(a), n).reshape((-1,) + (1,) * (a.ndim - 1))
def rstd(a, n):
    m = rmean(a, n); v = rmean(a * a, n) - m * m; return np.sqrt(np.maximum(v, 1e-12))
def rret(R, n): return rsum(np.log1p(R), n)              # rendimiento log de los ultimos n dias (hasta t incluido)


def rasgos(R, V):
    """X[T,N,12] unitario; cada X[t] usa solo datos <= t."""
    T, N = R.shape; Rm = R.mean(1, keepdims=True)
    v20, v250 = rstd(R, 20), rstd(R, 250); vm20, vm250 = rstd(Rm, 20), rstd(Rm, 250)
    Cl = np.cumsum(np.log1p(R), 0); mx = np.empty_like(Cl)
    for t in range(T): mx[t] = Cl[max(0, t - 249):t + 1].max(0)
    F = [R / v20, rret(R, 5) / (v20 * np.sqrt(5)), rret(R, 20) / (v250 * np.sqrt(20)), rret(R, 60) / (v250 * np.sqrt(60)),
         np.repeat(Rm / vm20, N, 1), np.repeat(rret(Rm, 5) / (vm20 * np.sqrt(5)), N, 1), np.repeat(rret(Rm, 20) / (vm250 * np.sqrt(20)), N, 1),
         (rret(R, 5) - rret(Rm, 5)) / (v20 * np.sqrt(5)), (rret(R, 20) - rret(Rm, 20)) / (v250 * np.sqrt(20)),
         np.log(v20 / v250), np.log(V / rmean(V, 20)), Cl - mx]
    Z = []
    for f in F:
        z = (f - rmean(f, 250)) / np.maximum(rstd(f, 250), 1e-9); Z.append(np.clip(z, -3, 3))
    X = np.stack(Z, 2); X = X / (np.linalg.norm(X, axis=2, keepdims=True) + 1e-12)
    return X


def clase(r): return SUBE if r > U else (BAJA if r < -U else NADA)


# ================================================================ brazos -> matriz de posiciones pos[T,N] (decidida al cierre de t)
def pos_mantener(R): return np.ones_like(R)
def pos_momento(R, n): p = np.sign(rret(R, n)); p[:CALENT] = 0; return p
def pos_reversion(R, n): p = -np.sign(rret(R, n)); p[:CALENT] = 0; return p


def pos_colonia(R, X, tipo, perillas, barajar=False, seed=0):
    """tipo 'd' = Colonia, 'e' = Cuarentena (clases originales). Cada dia: primero aprende lo de ayer (resultado ya
    conocido al cierre de hoy), luego decide hoy para los N instrumentos SIN aprender."""
    T, N = R.shape; kw = dict(perillas)
    if tipo == 'd':
        th = kw.pop('theta'); col = ML.Colonia(None, C_CUPO, seed, theta=th, th0=th, barajar=barajar, **kw)
    else:
        th = kw.pop('theta'); col = ML.Cuarentena(None, C_CUPO, seed, theta=th, th0=th, plazo=PLAZO, barajar=barajar, **kw)
    col.W = np.zeros((0, X.shape[2]))
    pos = np.zeros((T, N))
    for t in range(CALENT, T):
        if t > CALENT:
            for i in range(N): col.paso(X[t - 1, i], P_BASE, clase(R[t, i]), aprender=True, maestro=i)
        for i in range(N):
            out = col.paso(X[t, i], P_BASE, None, aprender=False); pos[t, i] = POS_DE[int(np.argmax(out))]
    est = dict(nac=col.nac, mue=col.mue, pisadas=col.pisadas, pisadas_ok=col.pisadas_ok, vivas=col.N)
    if tipo == 'e': est.update(validadas_total=col.validadas_total, reversiones=col.reversiones, sombra_ok=col.sombra_ok,
                               sombra_mal=col.sombra_mal, murio_sin_validar=col.murio_sin_validar, **col.estado())
    return pos, est


# ================================================================ cobro
def cobra(pos, R, a, b, escala=1.0, retardo=0):
    """dias de decision a..b-1; la posicion de t cobra R[t+1]. Devuelve neto por dia-instrumento [D,N] (fraccion)."""
    P = pos[a - retardo:b - retardo]; ret = R[a + 1:b + 1]
    ant = np.vstack([np.zeros((1, P.shape[1])), P[:-1]]); lados = np.abs(P - ant); lados[-1] += np.abs(P[-1])
    return P * ret - lados * COSTO * escala - (P < 0) * CORTO_DIA * escala


def n_oper(P):
    ant = np.vstack([np.zeros((1, P.shape[1])), P[:-1]]); return int(((P != ant) & (P != 0)).sum())


def caida(d):
    eq = np.cumprod(1 + d); return float((1 - eq / np.maximum.accumulate(eq)).max())


def medidas(pos, R, a, b, meses, escala=1.0, retardo=0):
    M = cobra(pos, R, a, b, escala, retardo); d = M.mean(1); P = pos[a - retardo:b - retardo]; ret = R[a + 1:b + 1]
    ms = meses[a + 1:b + 1]; pm = {}
    for x, m in zip(d, ms): pm[m] = pm.get(m, 0.0) + x
    no = n_oper(P); act = P != 0
    return dict(anual=float(d.mean() * 252), sharpe=float(d.mean() / (d.std() + 1e-12) * np.sqrt(252)), caida_max=caida(d),
                meses_pos=float(np.mean([v > 0 for v in pm.values()])), n_meses=len(pm), n_oper=no,
                centavos_por_oper=float(M.sum() * 1e4 / max(no, 1)), total_centavos_por_100=float(M.sum() * 1e4 / P.shape[1]),
                frac_larga=float((P > 0).mean()), frac_corta=float((P < 0).mean()), frac_fuera=float((P == 0).mean()),
                acierto_signo=float((np.sign(P[act]) == np.sign(ret[act])).mean()) if act.any() else None), d


def idx_boot(D, rng):
    nb = int(np.ceil(D / BLOQUE)); ini = rng.integers(0, D, (NBOOT, nb))
    return ((ini[:, :, None] + np.arange(BLOQUE)[None, None, :]) % D).reshape(NBOOT, -1)[:, :D]


def ic(x, idx, niveles=(95.0, 98.75)):
    """intervalo por remuestreo en bloques de la media diaria anualizada de la serie x."""
    b = x[idx].mean(1) * 252; out = dict(est=float(x.mean() * 252))
    for nv in niveles:
        lo, hi = np.percentile(b, [(100 - nv) / 2, 100 - (100 - nv) / 2]); out['ic%g' % nv] = [float(lo), float(hi)]
    return out


def ic_sharpe(x, y, idx):
    sx = x[idx]; sy = y[idx]; f = lambda s: s.mean(1) / (s.std(1) + 1e-12) * np.sqrt(252); b = f(sx) - f(sy)
    g = lambda s: s.mean() / (s.std() + 1e-12) * np.sqrt(252)
    return dict(est=float(g(x) - g(y)), ic95=[float(v) for v in np.percentile(b, [2.5, 97.5])],
                **{'ic98.75': [float(v) for v in np.percentile(b, [0.625, 99.375])]})


def azar(pos, R, a, b, seed, escala=1.0):
    """misma matriz de posiciones con instrumentos permutados y cada columna desplazada circularmente: misma frecuencia."""
    rng = np.random.default_rng(seed); P = pos[a:b]; D, N = P.shape; tot = np.zeros(N_AZAR); media = np.zeros(D)
    falso = np.zeros((b + 1, N))
    for s in range(N_AZAR):
        Q = P[:, rng.permutation(N)].copy()
        for j in range(N): Q[:, j] = np.roll(Q[:, j], int(rng.integers(20, D - 20)))
        falso[a:b] = Q; d = cobra(falso, R, a, b, escala).mean(1); tot[s] = d.mean() * 252; media += d / N_AZAR
    return media, tot


# ================================================================ evaluacion de un tramo
def posiciones(R, X, per, con_control=True, log=print):
    t0 = time.time(); P = {}; E = {}
    P['a_mantener'] = pos_mantener(R); P['b1_momento'] = pos_momento(R, per['mom']); P['b2_reversion'] = pos_reversion(R, per['rev'])
    P['d_colonia'], E['d_colonia'] = pos_colonia(R, X, 'd', per['d'])
    P['e_cuarentena'], E['e_cuarentena'] = pos_colonia(R, X, 'e', per['e'])
    if con_control: P['d_barajada'], E['d_barajada'] = pos_colonia(R, X, 'd', per['d'], barajar=True)
    log('  posiciones en %.0f s' % (time.time() - t0)); return P, E


def evalua(R, X, meses, per, a, b, log=print, P=None, E=None):
    if P is None: P, E = posiciones(R, X, per, log=log)
    rng = np.random.default_rng(SEM_BOOT); idx = idx_boot(b - a, rng); out = dict(brazos={}, colonia=E, comparaciones={}, dias=b - a)
    S = {}
    for nom, pos in P.items():
        out['brazos'][nom] = {}
        for etq, esc in (('costo0', 0.0), ('costo_base', 1.0), ('costo_doble', 2.0)):
            m, d = medidas(pos, R, a, b, meses, esc); out['brazos'][nom][etq] = m
            if esc == 1.0: S[nom] = d; S0 = None
        m, _ = medidas(pos, R, a, b, meses, 1.0, retardo=1); out['brazos'][nom]['retardo1_costo_base'] = m
        out['brazos'][nom]['costo_base']['ic_anual'] = ic(S[nom], idx)
    for nom in ('d_colonia', 'e_cuarentena'):
        pos = P[nom]; seg = pos[a:b]; ret = R[a + 1:b + 1]; pis = seg != 1
        out['brazos'][nom]['frac_pisada'] = float(pis.mean())
        ok = ((seg == -1) & (ret < -U)) | ((seg == 0) & (np.abs(ret) <= U))
        out['brazos'][nom]['acierto_clase_al_pisar'] = float(ok[pis].mean()) if pis.any() else None
        out['brazos'][nom]['base_falla_al_pisar'] = float((ret[pis] <= U).mean()) if pis.any() else None
        out['brazos'][nom]['base_falla_global'] = float((ret <= U).mean())
        for etq, esc in (('costo0', 0.0), ('costo_base', 1.0), ('costo_doble', 2.0)):
            med, tot = azar(pos, R, a, b, 777, esc); m, d = medidas(pos, R, a, b, meses, esc)
            c = dict(azar_media_anual=float(tot.mean()), azar_p5_p95=[float(v) for v in np.percentile(tot, [5, 95])],
                     p_azar=float((tot >= d.mean() * 252).mean()))
            if esc == 1.0:
                c['menos_mantener'] = ic(d - S['a_mantener'], idx); c['menos_azar'] = ic(d - med, idx)
                c['sharpe_menos_mantener'] = ic_sharpe(d, S['a_mantener'], idx); c['sharpe_menos_azar'] = ic_sharpe(d, med, idx)
            else:
                _, da = medidas(P['a_mantener'], R, a, b, meses, esc)
                c['menos_mantener'] = ic(d - da, idx, (95.0,)); c['menos_azar'] = ic(d - med, idx, (95.0,))
            out['comparaciones'][nom + '|' + etq] = c
    for nom in P:
        if nom not in ('a_mantener', 'd_colonia', 'e_cuarentena'):
            out['comparaciones'][nom + '|costo_base'] = dict(menos_mantener=ic(S[nom] - S['a_mantener'], idx, (95.0,)))
    return out


def elige(R, X, meses, a, b, log=print):
    """perillas por rendimiento medio diario NETO al costo base en el tramo de validacion [a, b)."""
    tabla = {}; per = {}
    f = lambda pos: float(cobra(pos, R, a, b).mean() * 252)
    for clave, rej, fn in (('mom', REJ_MOM, pos_momento), ('rev', REJ_REV, pos_reversion)):
        v = [f(fn(R, n)) for n in rej]; tabla[clave] = dict(zip(map(str, rej), v)); per[clave] = rej[int(np.argmax(v))]
    for clave, rej in (('d', REJ_D), ('e', REJ_E)):
        v = []
        for p in rej:
            t0 = time.time(); pos, est = pos_colonia(R, X, clave, p); v.append(f(pos))
            log('  %s %s -> %+.4f  pisa %.3f  (%.0f s)' % (clave, p, v[-1], float((pos[a:b] != 1).mean()), time.time() - t0))
        tabla[clave] = [dict(perillas=p, anual_neto=x) for p, x in zip(rej, v)]; per[clave] = rej[int(np.argmax(v))]
    tabla['a_mantener'] = f(pos_mantener(R))
    return per, tabla


def prepara(dat):
    R, err = rend(dat['C']); X = rasgos(R, dat['V']); return R, X, err


def guarda(nombre, obj):
    os.makedirs(DATOS, exist_ok=True); f = os.path.join(DATOS, nombre)
    json.dump(obj, open(f, 'w', encoding='utf-8'), indent=1, ensure_ascii=False); print('escrito', f)


def tramo_valid(dat):
    f = dat['fechas']; a = max(i for i, d in enumerate(f) if d < INI_VALID); b = max(i for i, d in enumerate(f) if d <= FIN_VALID)
    return a, b                                         # decisiones a..b-1 cobran rendimientos fechados INI_VALID..FIN_VALID


# ================================================================ etapas
def etapa_valida():
    dat = carga_real(False); R, X, err = prepara(dat); a, b = tramo_valid(dat)
    assert dat['fechas'][-1] <= FIN_VALID
    print('datos hasta', dat['fechas'][-1], R.shape, 'validacion', dat['fechas'][a + 1], '->', dat['fechas'][b], 'relleno', dat['relleno'], 'errores', err)
    per, tabla = elige(R, X, dat['meses'], a, b); print('perillas', per)
    ev = evalua(R, X, dat['meses'], per, a, b)
    guarda('validacion.json', dict(perillas=per, rejilla=tabla, evaluacion_en_validacion=ev, ultima_fecha=dat['fechas'][-1],
                                   T=len(dat['fechas']), N=len(dat['nombres']), nombres=dat['nombres'], relleno=dat['relleno'],
                                   errores_dato=[(dat['fechas'][i], dat['nombres'][j], r) for i, j, r in err], tramo=[dat['fechas'][a + 1], dat['fechas'][b]]))


def etapa_auditoria():
    per = json.load(open(os.path.join(DATOS, 'validacion.json'), encoding='utf-8'))['perillas']
    dat = carga_real(False); R, X, _ = prepara(dat); T, N = R.shape; out = {}
    # --- 1. truncado bit a bit
    Tc = T - 150; Rc, lc = rend(dat['C'][:Tc]); Xc = rasgos(Rc, dat['V'][:Tc])
    P, _ = posiciones(R, X, per, con_control=False); Pc, _ = posiciones(Rc, Xc, per, con_control=False)
    out['truncado'] = dict(corte=dat['fechas'][Tc - 1], rasgos_identicos=bool(np.array_equal(X[:Tc], Xc)),
                           posiciones_identicas={k: bool(np.array_equal(P[k][:Tc], Pc[k])) for k in P},
                           posiciones_no_nulas={k: int((P[k][:Tc] != 0).sum()) for k in P})
    print('truncado', out['truncado'])
    # --- 1b. control positivo de la auditoria: una regla CON fuga (mira r de manana) debe ser detectada
    fuga = np.zeros_like(R); fuga[:-1] = np.sign(R[1:]); fc = np.zeros_like(Rc); fc[:-1] = np.sign(Rc[1:])
    out['truncado']['control_con_fuga_detectado'] = bool(not np.array_equal(fuga[:Tc], fc))
    # --- 2. barajada: dias permutados por instrumento, media restada -> bruto esperado 0
    series = {}; a = CALENT
    for s in range(5):
        rng = np.random.default_rng(1000 + s); Rb = np.zeros_like(R); Vb = np.zeros_like(R)
        for j in range(N):
            p = rng.permutation(T - 1) + 1; Rb[1:, j] = R[p, j]; Vb[1:, j] = dat['V'][p, j]; Vb[0, j] = dat['V'][0, j]
        Rb[1:] -= Rb[1:].mean(0, keepdims=True); Xb = rasgos(Rb, Vb)
        Pb, _ = posiciones(Rb, Xb, per, con_control=False)
        for k, pos in Pb.items(): series.setdefault(k, []).append(cobra(pos, Rb, a, T - 1, 0.0).mean(1))
        print('  barajada', s, {k: round(float(v[-1].mean() * 252), 4) for k, v in series.items()})
    out['barajada'] = {}
    for k, v in series.items():
        d = np.concatenate(v); t = float(d.mean() / (d.std() / np.sqrt(len(d)) + 1e-18))
        out['barajada'][k] = dict(bruto_anual=float(d.mean() * 252), t=t, por_semilla=[float(x.mean() * 252) for x in v],
                                  pasa=bool(abs(t) < 3 and abs(d.mean() * 252) < 0.03))
    # control positivo: la regla con fuga en la barajada debe dar ganancia enorme (la auditoria ve)
    out['barajada']['control_con_fuga_bruto_anual'] = float(cobra(np.vstack([np.sign(Rb[1:]), np.zeros((1, N))]), Rb, a, T - 1, 0.0).mean() * 252)
    out['pasa'] = bool(out['truncado']['rasgos_identicos'] and all(out['truncado']['posiciones_identicas'].values())
                       and all(v['pasa'] for k, v in out['barajada'].items() if isinstance(v, dict)))
    print(json.dumps(out['barajada'], indent=1)); print('AUDITORIA PASA:', out['pasa']); guarda('auditoria.json', out)


def etapa_sintetica(chica=False):
    out = {}
    for senal in (False, True):
        dat = sintetica(senal, T=900 if chica else 3020, N=8 if chica else 31); R, X, err = prepara(dat); T = len(R)
        a, b, fin = (int(T * 0.5), int(T * 0.75), T - 1)
        global REJ_D, REJ_E
        if chica: rd, re_ = REJ_D, REJ_E; REJ_D, REJ_E = REJ_D[:2], REJ_E[:2]
        per, tabla = elige(R, X, dat['meses'], a, b)
        if chica: REJ_D, REJ_E = rd, re_
        print('sintetica senal=%s perillas %s' % (senal, per))
        ev = evalua(R, X, dat['meses'], per, b, fin); out['con_senal' if senal else 'sin_senal'] = dict(perillas=per, rejilla=tabla, sellado_sintetico=ev)
        resumen(ev)
    return out


def resumen(ev):
    print('%-14s %9s %9s %9s %7s %7s %7s %7s %9s' % ('brazo', 'anual0', 'anual', 'anual2x', 'sharpe', 'caida', 'meses+', 'n_oper', 'cent/oper'))
    for k, v in ev['brazos'].items():
        m = v['costo_base']
        print('%-14s %+9.4f %+9.4f %+9.4f %+7.2f %7.3f %7.2f %7d %+9.2f' % (k, v['costo0']['anual'], m['anual'], v['costo_doble']['anual'],
              m['sharpe'], m['caida_max'], m['meses_pos'], m['n_oper'], m['centavos_por_oper']))
    for k, c in ev['comparaciones'].items():
        if k.endswith('costo_base'):
            print(' ', k, {x: (round(y['est'], 4), [round(z, 4) for z in y.get('ic98.75', y['ic95'])]) for x, y in c.items() if isinstance(y, dict)},
                  'p_azar', c.get('p_azar'))


def congela():
    assert os.path.exists(os.path.join(DATOS, 'auditoria.json')) and os.path.exists(os.path.join(DATOS, 'sintetica.json'))
    v = json.load(open(os.path.join(DATOS, 'validacion.json'), encoding='utf-8'))
    aud = json.load(open(os.path.join(DATOS, 'auditoria.json'), encoding='utf-8'))
    guarda('CONGELADO.json', dict(fecha=time.strftime('%Y-%m-%d %H:%M:%S'), perillas=v['perillas'], sha_valores_py=sha256(os.path.abspath(__file__)),
                                  sha_mini_llm_py=sha256(ML.__file__), sha_preregistro=sha256(os.path.join(AQUI, 'PREREGISTRO.md')),
                                  sha_csv=SHA_CSV, sha_validacion=sha256(os.path.join(DATOS, 'validacion.json')), auditoria_pasa=aud['pasa']))


def abrir_sellado():
    fs = os.path.join(DATOS, 'sellado.json')
    if os.path.exists(fs): sys.exit('el tramo sellado YA se abrio una vez: no se reabre')
    cg = json.load(open(os.path.join(DATOS, 'CONGELADO.json'), encoding='utf-8'))
    assert cg['sha_valores_py'] == sha256(os.path.abspath(__file__)), 'el codigo cambio despues de congelar'
    assert cg['sha_mini_llm_py'] == sha256(ML.__file__) and cg['sha_preregistro'] == sha256(os.path.join(AQUI, 'PREREGISTRO.md'))
    assert cg['sha_validacion'] == sha256(os.path.join(DATOS, 'validacion.json'))
    per = cg['perillas']; dat = carga_real(True); R, X, err = prepara(dat); _, a = tramo_valid(dat); b = len(R) - 1
    print('SELLADO', dat['fechas'][a + 1], '->', dat['fechas'][b], 'dias', b - a, 'perillas', per)
    ev = evalua(R, X, dat['meses'], per, a, b); resumen(ev)
    guarda('sellado.json', dict(abierto=time.strftime('%Y-%m-%d %H:%M:%S'), congelado=cg, tramo=[dat['fechas'][a + 1], dat['fechas'][b]],
                                errores_dato=[(dat['fechas'][i], dat['nombres'][j], r) for i, j, r in err], relleno=dat['relleno'], evaluacion=ev))


if __name__ == '__main__':
    ap = argparse.ArgumentParser(); ap.add_argument('--humo', action='store_true'); ap.add_argument('--etapa')
    ap.add_argument('--congela', action='store_true'); ap.add_argument('--abrir-sellado', action='store_true'); a = ap.parse_args()
    t0 = time.time()
    if a.humo: guarda('humo.json', etapa_sintetica(chica=True))
    elif a.etapa == 'valida': etapa_valida()
    elif a.etapa == 'auditoria': etapa_auditoria()
    elif a.etapa == 'sintetica': guarda('sintetica.json', etapa_sintetica())
    elif a.congela: congela()
    elif a.abrir_sellado: abrir_sellado()
    print('%.0f s' % (time.time() - t0))
