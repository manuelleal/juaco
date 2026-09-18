"""Bloque 4 (XOR): ¿el cuello es la REGLA? — dos constantes de la via lenta (`eta_s` 0.015->0.15, `clip_s` 3->10).
Ejecuta PREREGISTRO_xor_4.md. REGLA 10: log desde el arranque. REGLA 11: lista los python vivos antes del Pool.

Instrumento: `experimentos/creacion_A/organismo_v13q5.py` (perillas `seleccion` y `lab`; con las dos apagadas es
`organismo_v13q3` EXACTO, y con `regla_lenta='dos_canales', constante=False` es `organismo_v13q`).

**NO hay --rapido:** el gemelo compilado `organismo_v13q_rapido` no tiene `regla_lenta`, `constante`, `oraculo01`,
`seleccion` ni `lab` (comprobado: 0 apariciones). Todo interpretado.

ETAPA 1 identidad (obligatoria, se para si falla): `organismo_v13q5(seleccion=None, lab=False)` == `organismo_v13q3`
en TODAS las claves del original (3 semillas x 2 escenarios).
ETAPA 2 las 480 corridas. ETAPA 3 tabla + EXPOSICIONES. ETAPA 4 criterios del preregistro.

Las EXPOSICIONES se calculan repitiendo el flujo `(patron, R)` que cada corrida graba con `lab=True` (la
actualizacion de la via lenta queda determinada por ese flujo). El replay esta verificado contra el organismo:
0 diferencias en 20/20 semillas (`banco_lab.py`, seccion A9 de PUENTE_creacion.md).

Uso:  python experimentos/creacion_A/corre_xor_4.py [--desde N]   (por defecto semillas 81-100; lo corre el coordinador)
      python experimentos/creacion_A/corre_xor_4.py --humo        (UN proceso, sin Pool: identidad + 4 brazos, 1 semilla)
"""
import sys, os, json, time, hashlib, platform, subprocess, itertools
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
import numpy as np

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
sys.path[:0] = [AQUI, os.path.join(RAIZ, 'experimentos', 'nivel7_xor_lectura'), os.path.join(RAIZ, 'organismo')]
_desde = int(sys.argv[sys.argv.index('--desde') + 1]) if '--desde' in sys.argv else 81
SEEDS = list(range(_desde, _desde + 20))
HUMO = '--humo' in sys.argv
if '--rapido' in sys.argv:
    raise SystemExit("*** --rapido no existe en el bloque 4: el gemelo no tiene las perillas (ver cabecera).")

BASE = dict(T=100000, mundo='regla', puerta=3, constante=True, regla_lenta='delta_signo', lam_lenta=0.0)
BRAZOS = {
    'TRONCO':       dict(eta_s=0.015, clip_s=3.0),                                    # las constantes de hoy
    'DOS_NUM':      dict(eta_s=0.15, clip_s=10.0),                                    # la propuesta A-4
    'DOS_NUM_WTA':  dict(eta_s=0.15, clip_s=10.0, seleccion='wta', sel_theta=0.3,     # + la seleccion meta-aprendida
                         sel_rho=0.02, sel_cupo=1, sel_estad='cond'),
    'ETA_1':        dict(eta_s=1.0, clip_s=10.0),                                     # CONTROL: debe EMPEORAR
}
LECTURAS = ['oraculo01', 'cuadratica']
REGLAS = ['xor01', 'px0', 'azar']
IDX_PROD = {'cuadratica': 6, 'oraculo01': 2}        # donde vive P0*P1 en phi
REJ = [10, 20, 40, 60, 100, 150, 200, 300, 400, 600]   # cortes para las exposiciones
IJ = [(i, j) for i in range(6) for j in range(i + 1, 6)]
N_PARALELO = 14
_log = {'f': None, 't0': time.time()}


def log(msg=""):
    linea = f"[{time.strftime('%H:%M:%S')} +{time.time()-_log['t0']:7.1f}s] {msg}"
    print(linea, flush=True)
    if _log['f']:
        _log['f'].write(linea + "\n"); _log['f'].flush(); os.fsync(_log['f'].fileno())


def N(x):
    return json.loads(json.dumps(x, default=str))


def h16(p):
    return hashlib.sha256(open(p, 'rb').read()).hexdigest()[:16]


def f3(x, n=3):
    return '  n/a' if x is None else f"{x:.{n}f}"


def med(xs):
    xs = [x for x in xs if x is not None]
    if not xs:
        return None, None, None
    return float(np.median(xs)), float(min(xs)), float(max(xs))


def signo_acc(Wd, test, vr):
    """Acierto BALANCEADO por signo sobre los nunca vistos. Empate exacto = 0.5. La formula del registro."""
    f = [1.0 if Wd[k] > 0 else (0.5 if Wd[k] == 0 else 0.0) for k in test if vr[k] == 'comida']
    p = [1.0 if Wd[k] < 0 else (0.5 if Wd[k] == 0 else 0.0) for k in test if vr[k] == 'veneno']
    if not f or not p:
        return None
    return 0.5 * float(np.mean(f)) + 0.5 * float(np.mean(p))


# ------------------------------------------------------------------ replay (para las EXPOSICIONES)
def phi_de(P, lectura, constante=True):
    if lectura == 'lineal': b = P
    elif lectura == 'cuadratica': b = np.concatenate([P, [P[i] * P[j] for i, j in IJ]])
    elif lectura == 'oraculo01': b = np.array([P[0], P[1], P[0] * P[1]])
    elif lectura == 'oraculo01_ruido': b = np.array([P[0], P[1], P[2] * P[3]])
    else: raise ValueError(lectura)
    return np.concatenate([b, [1.0]]) if constante else b


def replay(X, y, eta, clip, sel=None, theta=0.6, rho=0.05, cupo=1, estad='cond', npx=6, ncj=15):
    """La MISMA regla de la via lenta de organismo_v13q5 (delta con signo, lam_lenta=0), fuera del mundo."""
    n = X.shape[1]; w = np.zeros(n); e = np.zeros(n)
    ab = np.ones(n, bool); cand = np.zeros(n, bool)
    if sel:
        cand[npx:npx + ncj] = True; ab = ~cand
    for i in range(len(y)):
        ph = X[i]; d = y[i] - float(w @ ph)
        if sel:
            act = ph > 0
            if estad == 'cond': e[act] = (1 - rho) * e[act] + rho * d
            else: e = (1 - rho) * e + rho * (d * ph)
            if int((ab & cand).sum()) < cupo:
                c = cand & ~ab
                if c.any():
                    j = int(np.argmax(np.where(c, np.abs(e), -1.0)))
                    if abs(e[j]) > theta: ab[j] = True
            ph = ph * ab
        w = np.clip(w + eta * d * ph, -clip, clip)
    return w


def exposiciones(ev, fase2_en, lectura, kw, pats, test, vr):
    """acc_lenta usando solo los primeros n eventos pre-sonda, para cada n de REJ."""
    pre = [e for e in ev if e[0] < fase2_en]
    if not pre:
        return {n: None for n in REJ}, 0
    P = np.array([np.array([float(c) for c in e[1]]) for e in pre])
    y = np.array([e[2] for e in pre])
    X = np.array([phi_de(p, lectura) for p in P])
    npx = 2 if lectura.startswith('oraculo') else 6
    ncj = 1 if lectura.startswith('oraculo') else 15
    out = {}
    for n in REJ:
        if n > len(y):
            out[n] = None; continue
        w = replay(X[:n], y[:n], kw['eta_s'], kw['clip_s'],
                   sel=kw.get('seleccion'), theta=kw.get('sel_theta', 0.6), rho=kw.get('sel_rho', 0.05),
                   cupo=kw.get('sel_cupo', 1), estad=kw.get('sel_estad', 'cond'), npx=npx, ncj=ncj)
        out[n] = signo_acc({k: float(phi_de(v, lectura) @ w) for k, v in pats.items()}, test, vr)
    return out, len(pre)


# ------------------------------------------------------------------ tarea
def tarea(args):
    tipo = args[0]
    if tipo == 'I':
        _, regla, lectura, seed = args
        import organismo_v13q3 as a_, organismo_v13q5 as b_
        kw = dict(T=60000, mundo='regla', regla=regla, lectura=lectura, eta_s=0.015, puerta=3)
        if lectura != 'lineal':
            kw.update(constante=True, regla_lenta='delta_signo', lam_lenta=0.0)
        a, b = a_.run(seed, **kw), b_.run(seed, seleccion=None, lab=False, **kw)
        dif = [k for k in a if N(a[k]) != N(b[k])]
        return dict(tipo='I', esc=f'{regla}/{lectura}', seed=seed, identico=not dif, difieren=dif,
                    claves_nuevas=[k for k in b if k not in a])
    _, brazo, lectura, regla, seed = args
    import organismo_v13q5 as m
    kw = dict(BASE); kw.update(BRAZOS[brazo]); kw.update(regla=regla, lectura=lectura, lab=True)
    r = m.run(seed, **kw)
    pats, tren, test, vr = m.split_regla(seed, regla)
    expo, npre = exposiciones(r['lenta_eventos'], r['fase2_en'], lectura, BRAZOS[brazo], pats, test, vr)
    ab = r.get('sel_abiertos') or []
    cls = {}
    for e in r['lenta_eventos']:
        if e[0] < r['fase2_en']:
            cls[e[1][:2]] = cls.get(e[1][:2], 0) + 1
    Wsa = r['Ws_apriori'] or []
    return dict(tipo='T', brazo=brazo, lectura=lectura, regla=regla, seed=seed,
                acc=signo_acc(r['W_apriori'], test, vr), acc_lenta=signo_acc(r['W_lenta_apriori'], test, vr),
                abre_prod=bool(IDX_PROD[lectura] in ab), abiertos=[int(x) for x in ab],
                Ws_prod=(float(Wsa[IDX_PROD[lectura]]) if len(Wsa) > IDX_PROD[lectura] else None),
                max_abs_Ws=(float(max(abs(x) for x in Wsa)) if Wsa else None),
                n_pre=npre, clases_pre=cls, clases_sin_morder=4 - len(cls),
                expo={str(k): v for k, v in expo.items()},
                splits=r['splits'], celdas=r['celdas'], deaths=r['deaths'])


# ------------------------------------------------------------------ informe y criterios
def tabla(res, seeds):
    log("ETAPA 3/4 — tabla. acc = valor total a priori en nunca vistos; acc_lenta = via lenta sola.")
    G = lambda b, lec, rg: [r for r in res if r['tipo'] == 'T' and r['brazo'] == b and r['lectura'] == lec and r['regla'] == rg]
    for lec in LECTURAS:
        for b in BRAZOS:
            for rg in REGLAS:
                g = G(b, lec, rg)
                if not g: continue
                al = med([r['acc_lenta'] for r in g])
                log(f"   {lec:11s} {b:12s} {rg:6s} acc {f3(med([r['acc'] for r in g])[0])}"
                    f"  acc_lenta {f3(al[0])} [{f3(al[1], 2)},{f3(al[2], 2)}]"
                    f"  abre P0*P1 {sum(r['abre_prod'] for r in g)}/{len(g)}"
                    f"  Ws(P0*P1) {f3(med([r['Ws_prod'] for r in g])[0], 2)}"
                    f"  max|Ws| {f3(med([r['max_abs_Ws'] for r in g])[0], 2)}"
                    f"  eventos {f3(med([r['n_pre'] for r in g])[0], 0)}"
                    f"  clases sin morder {sum(r['clases_sin_morder'] > 0 for r in g)}/{len(g)}")
    log("EXPOSICIONES — acc_lenta con los primeros n encuentros (mediana); n* = primer n con mediana >= 0.75.")
    expos = {}
    for lec in LECTURAS:
        log(f"   {lec}:  " + ' '.join(f'{n:>6}' for n in REJ) + '   n*(>=0.75) / n*(>=0.65)')
        for b in BRAZOS:
            g = G(b, lec, 'xor01')
            if not g: continue
            v = [med([r['expo'].get(str(n)) for r in g])[0] for n in REJ]
            n75 = next((n for n, x in zip(REJ, v) if x is not None and x >= 0.75), None)
            n65 = next((n for n, x in zip(REJ, v) if x is not None and x >= 0.65), None)
            expos[f'{lec}/{b}'] = dict(curva={str(n): x for n, x in zip(REJ, v)}, n75=n75, n65=n65)
            log(f"      {b:12s} " + ' '.join(f'{f3(x, 3):>6}' for x in v) + f"   {n75 or '>600'} / {n65 or '>600'}")
    return expos


def criterios(res, seeds, expos):
    A = lambda b, lec, rg, s, k: next((r[k] for r in res if r['tipo'] == 'T' and r['brazo'] == b and r['lectura'] == lec
                                       and r['regla'] == rg and r['seed'] == s), None)
    M = lambda b, lec, rg, k: med([A(b, lec, rg, s, k) for s in seeds])[0]
    par = lambda b1, b2, lec, rg, k: sum(1 for s in seeds
                                         if A(b1, lec, rg, s, k) is not None and A(b2, lec, rg, s, k) is not None
                                         and A(b1, lec, rg, s, k) > A(b2, lec, rg, s, k))
    V = {}
    m1 = M('DOS_NUM', 'oraculo01', 'xor01', 'acc_lenta'); p1 = par('DOS_NUM', 'TRONCO', 'oraculo01', 'xor01', 'acc_lenta')
    V['V1'] = bool(m1 is not None and m1 >= 0.90 and p1 >= 15); V['V1_mediana'] = m1; V['V1_pareado'] = p1
    m2 = M('DOS_NUM', 'cuadratica', 'xor01', 'acc_lenta')
    V['V2'] = bool(m2 is not None and m2 <= 0.65); V['V2_mediana'] = m2
    n3 = sum(1 for s in seeds if A('DOS_NUM_WTA', 'cuadratica', 'xor01', s, 'abre_prod'))
    V['V3'] = bool(n3 >= 15); V['V3_abre'] = n3
    p4 = sum(1 for s in seeds
             if A('ETA_1', 'oraculo01', 'xor01', s, 'acc_lenta') is not None
             and A('DOS_NUM', 'oraculo01', 'xor01', s, 'acc_lenta') is not None
             and A('ETA_1', 'oraculo01', 'xor01', s, 'acc_lenta') < A('DOS_NUM', 'oraculo01', 'xor01', s, 'acc_lenta'))
    ev1 = med([A('ETA_1', 'oraculo01', 'xor01', s, 'n_pre') for s in seeds])[0]
    V['V4'] = bool(p4 >= 14); V['V4_pareado'] = p4; V['V4_eventos_ETA_1'] = ev1
    V['V4_comparable'] = bool(ev1 is not None and ev1 >= 100)   # preregistro §7: si ETA_1 deja de morder, no es comparable
    malos = []
    for lec in LECTURAS:
        for b in BRAZOS:
            px = M(b, lec, 'px0', 'acc_lenta'); az = M(b, lec, 'azar', 'acc_lenta')
            if px is None or px < 1.0 - 1e-9: malos.append(f'px0 {lec}/{b}={f3(px)}')
            if az is None or not (0.35 <= az <= 0.65): malos.append(f'azar {lec}/{b}={f3(az)}')
    V['V5'] = not malos; V['V5_fallos'] = malos
    V['EXPO'] = {k: dict(n75=v['n75'], n65=v['n65']) for k, v in expos.items()}
    V['EL_CUELLO_ES_LA_REGLA'] = bool(V['V1'] and V['V4'] and V['V5'])
    log("ETAPA 4/4 — criterios del preregistro.")
    log(f"   V1 oraculo DOS_NUM acc_lenta {f3(m1)} >= .90 y > TRONCO en {p1}/20            {'OK' if V['V1'] else 'NO'}")
    log(f"   V2 cuadratica DOS_NUM acc_lenta {f3(m2)} <= .65 (el techo son los RASGOS)     {'OK' if V['V2'] else 'NO'}")
    log(f"   V3 WTA abre P0*P1 en {n3}/20 (cuadratica) >= 15                               {'OK' if V['V3'] else 'NO'}")
    log(f"   V4 ETA_1 < DOS_NUM en {p4}/20 >= 14 (el control que debe EMPEORAR)            {'OK' if V['V4'] else 'NO'}")
    log(f"      V4 comparable (preregistro §7): ETA_1 mantiene {f3(ev1, 0)} eventos >= 100   "
        f"{'SI' if V['V4_comparable'] else 'NO — ETA_1 no es comparable: cambio la CONDUCTA, no solo el optimizador'}")
    log(f"   V5 px0 = 1.000 y azar en [.35,.65] en todos: {'OK' if V['V5'] else 'NO — ' + '; '.join(malos)}")
    log(f"VEREDICTO bloque 4: {'EL CUELLO DE XOR ES LA REGLA — dos constantes de la via lenta lo abren' if V['EL_CUELLO_ES_LA_REGLA'] else 'NO: las dos constantes no bastan (mirar V1/V4/V5)'}")
    log("RECORDATORIO: este bloque NO autoriza el cambio del tronco. Eso lo decide el CONTROL QUE PUEDE FALLAR: "
        "bateria_v14_e015c10.py (>= 19/20 en las seis etapas) y bateria_generaliza_A.py organismo_v14_e015c10 "
        "(G1 >= 0.80, G2 >= 0.85, K 20/20).")
    return V


def humo():
    """UN proceso, sin Pool (EQUIPO regla 3): identidad + los 4 brazos en oraculo y cuadratica, 1 semilla."""
    stamp = time.strftime('%Y%m%d_%H%M%S')
    _log['f'] = open(os.path.join(RAIZ, 'datos', f'xor_4_humo_{stamp}.log'), 'w', encoding='utf-8', newline='\n')
    log(f"HUMO bloque 4 (un proceso, sin Pool). identidad + {len(BRAZOS)} brazos x {len(LECTURAS)} lecturas, "
        f"xor01, semilla {_desde}, T={BASE['T']}.")
    log(f"sha organismo_v13q5 {h16(os.path.join(AQUI, 'organismo_v13q5.py'))}"
        f"  organismo_v13q4 {h16(os.path.join(AQUI, 'organismo_v13q4.py'))}"
        f"  organismo_v13q3 {h16(os.path.join(RAIZ,'experimentos','nivel7_xor_lectura','organismo_v13q3.py'))}"
        f"  script {h16(os.path.abspath(__file__))}")
    ide = [tarea(('I', rg, lec, _desde)) for rg, lec in (('px0', 'lineal'), ('xor01', 'cuadratica'), ('xor01', 'oraculo01'))]
    for x in ide:
        log(f"   identidad {x['esc']:20s} s{x['seed']}: {'IDENTICO' if x['identico'] else 'DIFIERE ' + str(x['difieren'])}"
            f"  (claves nuevas: {x['claves_nuevas']})")
    if not all(x['identico'] for x in ide):
        log("*** IDENTIDAD FALLIDA: el instrumento no sirve."); _log['f'].close(); sys.exit(1)
    log(f"   identidad: {sum(x['identico'] for x in ide)}/{len(ide)}")
    res = [tarea(('T', b, lec, 'xor01', _desde)) for lec in LECTURAS for b in BRAZOS]
    for r in res:
        n75 = next((n for n in REJ if r['expo'].get(str(n)) is not None and r['expo'][str(n)] >= 0.75), None)
        log(f"   {r['lectura']:11s} {r['brazo']:12s} s{r['seed']}: acc_lenta {f3(r['acc_lenta'])}  acc {f3(r['acc'])}"
            f"  abre P0*P1 {'SI' if r['abre_prod'] else 'no'}  Ws(P0*P1) {f3(r['Ws_prod'], 2)}"
            f"  max|Ws| {f3(r['max_abs_Ws'], 2)}  eventos {r['n_pre']}  clases sin morder {r['clases_sin_morder']}"
            f"  n*(>=.75) {n75 or '>600'}")
    log("   (referencia: TRONCO oraculo = 0.625 y cuadratica = 0.438 en el flujo cosechado de 20 semillas 1-20;"
        " nada se ajusta con este humo.)")
    dj = os.path.join(RAIZ, 'datos', f'xor_4_humo_{stamp}.json')
    json.dump(dict(meta=dict(fecha=time.strftime('%Y-%m-%dT%H:%M:%S'), base=BASE, brazos=BRAZOS, lecturas=LECTURAS,
                             semilla=_desde, sha_instrumento=h16(os.path.join(AQUI, 'organismo_v13q5.py')),
                             sha_script=h16(os.path.abspath(__file__)),
                             python=platform.python_version(), numpy=np.__version__),
                   identidades=ide, corridas=res), open(dj, 'w', encoding='utf-8'), ensure_ascii=False, default=str)
    log(f"datos -> {os.path.basename(dj)}  sha256_16 = {h16(dj)}")
    _log['f'].close()


if __name__ == '__main__':
    if HUMO:
        humo(); sys.exit(0)
    import multiprocessing as mp
    mp.set_start_method('spawn', force=True)
    stamp = time.strftime('%Y%m%d_%H%M%S')
    _log['f'] = open(os.path.join(RAIZ, 'datos', f'xor_4_s{SEEDS[0]}-{SEEDS[-1]}_{stamp}.log'), 'w', encoding='utf-8', newline='\n')
    pre = os.path.join(AQUI, 'PREREGISTRO_xor_4.md')
    log(f"ARRANQUE bloque 4 (¿el cuello de XOR es la regla?). brazos {list(BRAZOS)}, lecturas {LECTURAS}, "
        f"reglas {REGLAS}, semillas {SEEDS[0]}-{SEEDS[-1]}. Pool({N_PARALELO}).")
    log(f"BASE {BASE}")
    for b, kw in BRAZOS.items():
        log(f"   brazo {b:12s} {kw}")
    log(f"sha preregistro {h16(pre) if os.path.exists(pre) else '(falta)'}  script {h16(os.path.abspath(__file__))}"
        f"  organismo_v13q5 {h16(os.path.join(AQUI, 'organismo_v13q5.py'))}"
        f"  construye_v13q5 {h16(os.path.join(AQUI, 'construye_v13q5.py'))}"
        f"  organismo_v13q4 {h16(os.path.join(AQUI, 'organismo_v13q4.py'))}"
        f"  organismo_v13q3 {h16(os.path.join(RAIZ,'experimentos','nivel7_xor_lectura','organismo_v13q3.py'))}")
    try:
        ps = subprocess.run(['powershell', '-NoProfile', '-Command',
                             "Get-CimInstance Win32_Process | Where-Object { $_.Name -like 'python*' } | ForEach-Object { \"$($_.ProcessId) $($_.CommandLine)\" }"],
                            capture_output=True, text=True, timeout=60).stdout.strip().splitlines()
    except Exception as e:
        ps = [f"(no se pudo listar: {e})"]
    log(f"REGLA 11 — procesos python vivos ({len(ps)}), este es pid {os.getpid()}")
    with mp.Pool(N_PARALELO) as pool:
        ctrl = [('I', rg, lec, s) for rg, lec in (('px0', 'lineal'), ('xor01', 'cuadratica'), ('xor01', 'oraculo01'))
                for s in SEEDS[:3]]
        log(f"ETAPA 1/4 — identidad: organismo_v13q5(seleccion=None, lab=False) == organismo_v13q3 ({len(ctrl)} corridas, T=60000)...")
        rc = pool.map(tarea, ctrl, chunksize=1)
        log(f"   identicos: {sum(x['identico'] for x in rc)}/{len(rc)}   claves nuevas: {rc[0]['claves_nuevas']}")
        for x in rc:
            if not x['identico']:
                log(f"      DIFIERE {x['esc']} s{x['seed']}: {x['difieren']}")
        if not all(x['identico'] for x in rc):
            log("*** IDENTIDAD FALLIDA: se para."); sys.exit(1)
        tr = [('T', b, lec, rg, s) for b in BRAZOS for lec in LECTURAS for rg in REGLAS for s in SEEDS]
        log(f"ETAPA 2/4 — {len(tr)} corridas de T={BASE['T']}...")
        res = []
        for i, r in enumerate(pool.imap_unordered(tarea, tr, chunksize=1), 1):
            res.append(r)
            if i % 40 == 0 or i == len(tr):
                log(f"          {i}/{len(tr)}")
    expos = tabla(res, SEEDS)
    V = criterios(res, SEEDS, expos)
    meta = dict(fecha=time.strftime('%Y-%m-%dT%H:%M:%S'), semillas=SEEDS, base=BASE, brazos=BRAZOS,
                lecturas=LECTURAS, reglas=REGLAS, veredictos=V, exposiciones=expos, identidades=rc, procesos_python=ps,
                sha_preregistro=h16(pre) if os.path.exists(pre) else None, sha_script=h16(os.path.abspath(__file__)),
                sha_instrumento=h16(os.path.join(AQUI, 'organismo_v13q5.py')),
                sha_constructor=h16(os.path.join(AQUI, 'construye_v13q5.py')),
                sha_origen=h16(os.path.join(RAIZ, 'experimentos', 'nivel7_xor_lectura', 'organismo_v13q3.py')),
                python=platform.python_version(), numpy=np.__version__)
    dj = os.path.join(RAIZ, 'datos', f'xor_4_s{SEEDS[0]}-{SEEDS[-1]}_{stamp}.json')
    json.dump(dict(meta=meta, corridas=res), open(dj, 'w', encoding='utf-8'), ensure_ascii=False, default=str)
    log(f"datos -> {os.path.basename(dj)}  sha256_16 = {h16(dj)}")
    _log['f'].close()
