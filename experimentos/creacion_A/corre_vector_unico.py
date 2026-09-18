"""PAQUETE A-3 del CREADOR A — ¿la via LENTA puede ser UN vector con signo, sin perder nada?

Ejecuta `PREREGISTRO_vector_unico.md`. REGLA 10: log desde el arranque. REGLA 11: lista los python vivos antes del Pool.

TESIS (algebra, en `registro/investigacion/PUENTE_creacion.md` §A3). Por celda/rasgo, con `W = Wp-Wn` y
`m = min(Wp,Wn)`, la aplicacion `(Wp,Wn) <-> (W,m)` es una biyeccion y en esas coordenadas:
  drenaje `lam`  ==>  `m <- (1-lam)*m`, **W sin cambio**      (el drenaje NO toca el valor)
  refuerzo/castigo ==> `W <- W +- min(eta*|g(d)|, C - m - W^-+)`   (el tope actua sobre W como `|W| <= C - m`)
Luego, con `aversion = 1.0` y mientras NINGUN canal toque `clip_s`, la via lenta de dos canales con drenaje es
**exactamente** la regla delta sobre un solo vector con signo. La via RAPIDA no: la fision de v11 lee `m`.

Brazos (unico cambio entre ellos: la parametrizacion de la via lenta):
  DOS_CANALES    `organismo_v13q3` por defecto  (== organismo_v13q == la via lenta del tronco v13)
  VECTOR_UNICO   `regla_lenta='delta_signo'`, `lam_lenta=0.0`   (un solo vector con signo, sin decaimiento)
Montaje: el de `organismo/bateria_generaliza.py` (mundo de regla, `lectura='lineal'`, T=200000, sonda a priori en
T/2, reglas px0 y azar, criterios G1/G2/K con sus umbrales sin tocar), mas `xor01` como lectura adicional.

ETAPA 1 identidad (obligatoria, se para si falla): `organismo_v13q3(dos_canales, constante=False, lectura='lineal')`
== `organismo_v13q` == `organismo_v13g` en TODAS las claves.

Uso:  python experimentos/creacion_A/corre_vector_unico.py [--desde N]   (por defecto semillas 101-120; lo corre el coordinador)
      python experimentos/creacion_A/corre_vector_unico.py --humo        (UN proceso, sin Pool: identidad + 1 semilla por brazo)
"""
import sys, os, json, time, hashlib, platform, subprocess
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
import numpy as np

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
sys.path[:0] = [AQUI, os.path.join(RAIZ, 'experimentos', 'nivel7_xor_lectura'),
                os.path.join(RAIZ, 'experimentos', 'v13_dos_vias'), os.path.join(RAIZ, 'organismo')]
_desde = int(sys.argv[sys.argv.index('--desde') + 1]) if '--desde' in sys.argv else 101
SEEDS = list(range(_desde, _desde + 20))
HUMO = '--humo' in sys.argv

T_HUMO = 60000
BASE = dict(T=200000, mundo='regla', lectura='lineal', eta_s=0.015, puerta=3, clip_s=3.0)   # el punto del tronco v13
BRAZOS = {
    'DOS_CANALES':  dict(regla_lenta='dos_canales', constante=False),                 # la via lenta de v13, sin tocar
    'VECTOR_UNICO': dict(regla_lenta='delta_signo', constante=False, lam_lenta=0.0),  # un solo vector con signo
}
REGLAS = ['px0', 'azar', 'xor01']
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


def tarea(args):
    """ETAPA 1 ('I') identidad del instrumento; ('T') una corrida de un brazo. Importa dentro: vale para Pool spawn."""
    tipo = args[0]
    if tipo == 'I':
        _, regla, seed, T = args
        import organismo_v13q as a_, organismo_v13q3 as b_
        kw = dict(T=T, mundo='regla', regla=regla, lectura='lineal', eta_s=0.015, puerta=3)
        a, b = a_.run(seed, **kw), b_.run(seed, regla_lenta='dos_canales', constante=False, **kw)
        dif = [k for k in a if N(a[k]) != N(b[k])]
        return dict(tipo='I', esc=f'{regla}/lineal', seed=seed, identico=not dif, difieren=dif,
                    claves_nuevas=[k for k in b if k not in a])
    _, brazo, regla, seed, T = args
    import organismo_v13q3 as m
    kw = dict(BASE); kw['T'] = T; kw.update(BRAZOS[brazo]); kw['regla'] = regla
    r = m.run(seed, **kw)
    vr = m.split_regla(seed, regla)[3]
    test = r['test']; Wa = r['W_apriori']
    f = [1.0 if Wa[k] > 0 else (0.5 if Wa[k] == 0 else 0.0) for k in test if vr[k] == 'comida']
    p = [1.0 if Wa[k] < 0 else (0.5 if Wa[k] == 0 else 0.0) for k in test if vr[k] == 'veneno']
    pf = [r['primer'][k]['pb'] for k in test if r['primer'][k] is not None and vr[k] == 'comida']
    pp = [1 - r['primer'][k]['pb'] for k in test if r['primer'][k] is not None and vr[k] == 'veneno']
    Wps = np.array(r['Wps']); Wns = np.array(r['Wns'])
    return dict(tipo='T', brazo=brazo, regla=regla, seed=seed,
                acc=0.5 * float(np.mean(f)) + 0.5 * float(np.mean(p)),                       # G1, formula de bateria_generaliza
                ba=(0.5 * float(np.mean(pf)) + 0.5 * float(np.mean(pp))) if (pf and pp) else None,   # G2
                cobertura=sum(v is not None for v in r['primer'].values()),                  # K
                Ws_apriori=[float(x) for x in (r['Ws_apriori'] or [])],                      # el vector con signo EN LA SONDA (sin redondear)
                W_lenta_apriori={k: float(v) for k, v in (r['W_lenta_apriori'] or {}).items()},
                n_techo=int(r['n_techo']),                                                   # veces que el tope de la via RAPIDA apreto
                max_Wps=float(Wps.max()) if Wps.size else None, max_Wns=float(Wns.max()) if Wns.size else None,
                max_m=float(np.minimum(Wps, Wns).max()) if Wps.size else None,
                splits=r['splits'], celdas=r['celdas'], deaths=r['deaths'])


def compara(res, seeds):
    """Pareo semilla a semilla de los dos brazos: acc identica y |dW_lenta| por debajo de 1e-9."""
    G = {(r['brazo'], r['regla'], r['seed']): r for r in res if r['tipo'] == 'T'}
    filas = []
    for rg in REGLAS:
        for s in seeds:
            a, b = G.get(('DOS_CANALES', rg, s)), G.get(('VECTOR_UNICO', rg, s))
            if not a or not b:
                continue
            dW = max(abs(a['W_lenta_apriori'][k] - b['W_lenta_apriori'][k]) for k in a['W_lenta_apriori'])
            dV = max(abs(x - y) for x, y in zip(a['Ws_apriori'], b['Ws_apriori'])) if a['Ws_apriori'] and b['Ws_apriori'] else None
            filas.append(dict(regla=rg, seed=s, acc_2c=a['acc'], acc_vu=b['acc'], acc_igual=a['acc'] == b['acc'],
                              ba_2c=a['ba'], ba_vu=b['ba'], dW_lenta=dW, dWs=dV,
                              tope_toca=bool(max(a['max_Wps'], a['max_Wns']) >= BASE['clip_s'] - 1e-9),
                              max_canal=max(a['max_Wps'], a['max_Wns']), max_m=a['max_m'],
                              n_techo_2c=a['n_techo'], n_techo_vu=b['n_techo'],
                              celdas_igual=a['celdas'] == b['celdas'], splits_igual=a['splits'] == b['splits']))
    return filas


def criterios(res, filas, seeds):
    """G1/G2/K de bateria_generaliza por brazo (umbrales sin tocar) + los criterios propios de A-3."""
    S = len(seeds); V = {}
    for b in BRAZOS:
        g = lambda rg, k: [r[k] for r in res if r['tipo'] == 'T' and r['brazo'] == b and r['regla'] == rg and r[k] is not None]
        px, az = g('px0', 'acc'), g('azar', 'acc')
        bpx, baz = g('px0', 'ba'), g('azar', 'ba')
        par1 = sum(1 for s in seeds
                   if any(r['seed'] == s and r['regla'] == 'px0' for r in res if r['tipo'] == 'T' and r['brazo'] == b)
                   and _v(res, b, 'px0', s, 'acc') is not None and _v(res, b, 'azar', s, 'acc') is not None
                   and _v(res, b, 'px0', s, 'acc') > _v(res, b, 'azar', s, 'acc'))
        par2 = sum(1 for s in seeds if _v(res, b, 'px0', s, 'ba') is not None and _v(res, b, 'azar', s, 'ba') is not None
                   and _v(res, b, 'px0', s, 'ba') > _v(res, b, 'azar', s, 'ba'))
        cob = sum(1 for s in seeds if (_v(res, b, 'px0', s, 'cobertura') or 0) >= 6)
        mpx = float(np.median(px)) if px else None; maz = float(np.median(az)) if az else None
        V[b] = dict(G1=bool(px and az and mpx >= 0.65 and 0.35 <= maz <= 0.65 and par1 >= 0.7 * S),
                    G2=bool(bpx and baz and float(np.median(bpx)) >= 0.55 and 0.42 <= float(np.median(baz)) <= 0.58 and par2 >= 0.7 * S),
                    K=bool(cob >= 0.9 * S), px0=mpx, azar=maz,
                    ba_px0=float(np.median(bpx)) if bpx else None, ba_azar=float(np.median(baz)) if baz else None,
                    par1=par1, par2=par2, cobertura=cob)
    n = len(filas)
    V['A1_acc_identica'] = bool(n and all(f['acc_igual'] for f in filas))
    V['A1_n'] = sum(f['acc_igual'] for f in filas)
    V['A2_dW_menor_1e-9'] = bool(n and all(f['dW_lenta'] < 1e-9 for f in filas if not f['tope_toca']))
    V['A2_max_dW'] = max((f['dW_lenta'] for f in filas), default=None)
    V['A3_tope_nunca_toca'] = bool(n and not any(f['tope_toca'] for f in filas))
    V['A3_max_canal'] = max((f['max_canal'] for f in filas), default=None)
    V['A3_max_m'] = max((f['max_m'] for f in filas), default=None)
    V['A4_n_techo_cero'] = bool(n and all(f['n_techo_2c'] == 0 and f['n_techo_vu'] == 0 for f in filas))
    V['EQUIVALENTES'] = bool(V['A1_acc_identica'] and V['A2_dW_menor_1e-9'])
    return V


def _v(res, brazo, regla, seed, k):
    for r in res:
        if r['tipo'] == 'T' and r['brazo'] == brazo and r['regla'] == regla and r['seed'] == seed:
            return r[k]
    return None


def informe(res, filas, V, seeds):
    log("TABLA — G1/G2/K por brazo (montaje y umbrales de bateria_generaliza).")
    for b in BRAZOS:
        v = V[b]
        log(f"   {b:13s} G1 px0 {f3(v['px0'])} azar {f3(v['azar'])} px0>azar {v['par1']}/{len(seeds)}  {'PASA' if v['G1'] else 'FALLA'}"
            f"  |  G2 px0 {f3(v['ba_px0'])} azar {f3(v['ba_azar'])} {v['par2']}/{len(seeds)}  {'PASA' if v['G2'] else 'FALLA'}"
            f"  |  K {v['cobertura']}/{len(seeds)}  {'OK' if v['K'] else 'FALLA'}")
    log("CRITERIOS A-3 (los mios).")
    log(f"   A1 acc identica semilla a semilla: {V['A1_n']}/{len(filas)}   {'OK' if V['A1_acc_identica'] else 'NO'}")
    log(f"   A2 max|dW_lenta| = {V['A2_max_dW']:.3e} (< 1e-9 donde el tope no toca)   {'OK' if V['A2_dW_menor_1e-9'] else 'NO'}")
    log(f"   A3 el tope nunca aprieta en la via lenta: max canal {f3(V['A3_max_canal'])} < clip_s={BASE['clip_s']}, "
        f"max masa de conflicto {f3(V['A3_max_m'])}   {'OK' if V['A3_tope_nunca_toca'] else 'NO'}")
    log(f"   A4 n_techo (via rapida) = 0 en todas: {'OK' if V['A4_n_techo_cero'] else 'NO'}")
    log(f"VEREDICTO A-3: {'LA VIA LENTA DE DOS CANALES ES, EXACTAMENTE, UN VECTOR CON SIGNO (y el drenaje lam no toca el valor)' if V['EQUIVALENTES'] else 'NO SON EQUIVALENTES: hay que mirar donde (tope? aversion? drenaje?)'}")


def humo():
    """UN proceso, sin Pool (EQUIPO regla 3): identidad + 1 semilla por brazo y regla, T corto."""
    stamp = time.strftime('%Y%m%d_%H%M%S')
    _log['f'] = open(os.path.join(RAIZ, 'datos', f'vector_unico_humo_{stamp}.log'), 'w', encoding='utf-8', newline='\n')
    log(f"HUMO A-3 (un proceso, sin Pool). identidad + {len(BRAZOS)}x{len(REGLAS)} corridas de T={T_HUMO}, semilla {_desde}.")
    log(f"sha organismo_v13q3 {h16(os.path.join(RAIZ,'experimentos','nivel7_xor_lectura','organismo_v13q3.py'))}"
        f"  organismo_v13q {h16(os.path.join(RAIZ,'experimentos','nivel7_xor_lectura','organismo_v13q.py'))}"
        f"  script {h16(os.path.abspath(__file__))}")
    ide = [tarea(('I', rg, _desde, 20000)) for rg in ('px0', 'xor01')]
    for x in ide:
        log(f"   identidad {x['esc']:12s} s{x['seed']}: {'IDENTICO' if x['identico'] else 'DIFIERE ' + str(x['difieren'])}"
            f"  (claves nuevas: {x['claves_nuevas']})")
    if not all(x['identico'] for x in ide):
        log("*** IDENTIDAD FALLIDA: el instrumento no sirve."); _log['f'].close(); sys.exit(1)
    res = [tarea(('T', b, rg, _desde, T_HUMO)) for b in BRAZOS for rg in REGLAS]
    for r in res:
        log(f"   {r['brazo']:13s} {r['regla']:6s} s{r['seed']}: acc {f3(r['acc'])}  ba {f3(r['ba'])}  cobertura {r['cobertura']}"
            f"  celdas {r['celdas']}  splits {r['splits']}  n_techo {r['n_techo']}"
            f"  max(Wps,Wns) {f3(max(r['max_Wps'], r['max_Wns']))}  max m {f3(r['max_m'])}")
    filas = compara(res, [_desde])
    for f in filas:
        log(f"   PAREO {f['regla']:6s} s{f['seed']}: acc {f3(f['acc_2c'])} vs {f3(f['acc_vu'])} "
            f"{'IGUAL' if f['acc_igual'] else '*** DISTINTA'}   max|dW_lenta| {f['dW_lenta']:.3e}   "
            f"max|dWs| {f['dWs']:.3e}   tope toca: {'SI' if f['tope_toca'] else 'no'}   "
            f"celdas/splits iguales: {f['celdas_igual']}/{f['splits_igual']}")
    log(f"HUMO: acc igual en {sum(f['acc_igual'] for f in filas)}/{len(filas)}; "
        f"max|dW_lenta| global {max(f['dW_lenta'] for f in filas):.3e}; "
        f"tope toca en {sum(f['tope_toca'] for f in filas)}/{len(filas)}.")
    dj = os.path.join(RAIZ, 'datos', f'vector_unico_humo_{stamp}.json')
    json.dump(dict(meta=dict(fecha=time.strftime('%Y-%m-%dT%H:%M:%S'), base=dict(BASE, T=T_HUMO), brazos=BRAZOS,
                             semilla=_desde, sha_script=h16(os.path.abspath(__file__)),
                             python=platform.python_version(), numpy=np.__version__),
                   identidades=ide, corridas=res, pareo=filas),
              open(dj, 'w', encoding='utf-8'), ensure_ascii=False, default=str)
    log(f"datos -> {os.path.basename(dj)}  sha256_16 = {h16(dj)}")
    _log['f'].close()


if __name__ == '__main__':
    if HUMO:
        humo(); sys.exit(0)
    import multiprocessing as mp
    mp.set_start_method('spawn', force=True)
    stamp = time.strftime('%Y%m%d_%H%M%S')
    _log['f'] = open(os.path.join(RAIZ, 'datos', f'vector_unico_s{SEEDS[0]}-{SEEDS[-1]}_{stamp}.log'), 'w', encoding='utf-8', newline='\n')
    pre = os.path.join(AQUI, 'PREREGISTRO_vector_unico.md')
    log(f"ARRANQUE A-3 (¿la via lenta puede ser un vector con signo?). brazos {list(BRAZOS)}, reglas {REGLAS}, "
        f"semillas {SEEDS[0]}-{SEEDS[-1]}. Pool({N_PARALELO}).")
    log(f"BASE {BASE}   (unico cambio entre brazos: la parametrizacion de la via lenta)")
    log(f"sha preregistro {h16(pre) if os.path.exists(pre) else '(falta)'}  script {h16(os.path.abspath(__file__))}"
        f"  organismo_v13q3 {h16(os.path.join(RAIZ,'experimentos','nivel7_xor_lectura','organismo_v13q3.py'))}"
        f"  organismo_v13q {h16(os.path.join(RAIZ,'experimentos','nivel7_xor_lectura','organismo_v13q.py'))}"
        f"  bateria_generaliza {h16(os.path.join(RAIZ,'organismo','bateria_generaliza.py'))}")
    try:
        ps = subprocess.run(['powershell', '-NoProfile', '-Command',
                             "Get-CimInstance Win32_Process | Where-Object { $_.Name -like 'python*' } | ForEach-Object { \"$($_.ProcessId) $($_.CommandLine)\" }"],
                            capture_output=True, text=True, timeout=60).stdout.strip().splitlines()
    except Exception as e:
        ps = [f"(no se pudo listar: {e})"]
    log(f"REGLA 11 — procesos python vivos ({len(ps)}), este es pid {os.getpid()}")
    with mp.Pool(N_PARALELO) as pool:
        ctrl = [('I', rg, s, 60000) for rg in ('px0', 'xor01') for s in SEEDS[:3]]
        log(f"ETAPA 1/3 — identidad: v13q3(dos_canales, lineal) == organismo_v13q ({len(ctrl)} corridas, T=60000)...")
        rc = pool.map(tarea, ctrl, chunksize=1)
        log(f"   identicos: {sum(x['identico'] for x in rc)}/{len(rc)}   claves nuevas: {rc[0]['claves_nuevas']}")
        for x in rc:
            if not x['identico']:
                log(f"      DIFIERE {x['esc']} s{x['seed']}: {x['difieren']}")
        if not all(x['identico'] for x in rc):
            log("*** IDENTIDAD FALLIDA: se para."); sys.exit(1)
        tr = [('T', b, rg, s, BASE['T']) for b in BRAZOS for rg in REGLAS for s in SEEDS]
        log(f"ETAPA 2/3 — {len(tr)} corridas de T={BASE['T']}...")
        res = []
        for i, r in enumerate(pool.imap_unordered(tarea, tr, chunksize=1), 1):
            res.append(r)
            if i % 20 == 0 or i == len(tr):
                log(f"          {i}/{len(tr)}")
    log("ETAPA 3/3 — pareo y criterios.")
    filas = compara(res, SEEDS)
    V = criterios(res, filas, SEEDS)
    informe(res, filas, V, SEEDS)
    meta = dict(fecha=time.strftime('%Y-%m-%dT%H:%M:%S'), semillas=SEEDS, base=BASE, brazos=BRAZOS, reglas=REGLAS,
                veredictos=V, identidades=rc, procesos_python=ps,
                sha_preregistro=h16(pre) if os.path.exists(pre) else None, sha_script=h16(os.path.abspath(__file__)),
                sha_instrumento=h16(os.path.join(RAIZ, 'experimentos', 'nivel7_xor_lectura', 'organismo_v13q3.py')),
                sha_origen=h16(os.path.join(RAIZ, 'experimentos', 'nivel7_xor_lectura', 'organismo_v13q.py')),
                python=platform.python_version(), numpy=np.__version__)
    dj = os.path.join(RAIZ, 'datos', f'vector_unico_s{SEEDS[0]}-{SEEDS[-1]}_{stamp}.json')
    json.dump(dict(meta=meta, corridas=res, pareo=filas), open(dj, 'w', encoding='utf-8'), ensure_ascii=False, default=str)
    log(f"datos -> {os.path.basename(dj)}  sha256_16 = {h16(dj)}")
    _log['f'].close()
