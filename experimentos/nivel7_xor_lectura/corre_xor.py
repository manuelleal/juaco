"""Bloque 3: XOR como limite de lectura. Ejecuta PREREGISTRO_xor_lectura.md. REGLA 10: log desde el arranque.
Identidad: organismo_v13q(lectura='lineal') == organismo_v13g (xor01 y px0, semillas 1-3, todas las claves).
Uso:  python experimentos/nivel7_xor_lectura/corre_xor.py [--desde N]
"""
import sys, os, json, time, hashlib, platform, subprocess
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
import numpy as np

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
sys.path[:0] = [AQUI, os.path.join(RAIZ, 'experimentos', 'v13_dos_vias'), os.path.join(RAIZ, 'organismo')]
_desde = int(sys.argv[sys.argv.index('--desde') + 1]) if '--desde' in sys.argv else 1
SEEDS = list(range(_desde, _desde + 20))
BASE = dict(T=200000, mundo='regla', eta_s=0.015, puerta=3)
BRAZOS = {'LINEAL': dict(lectura='lineal'), 'CUADRATICA': dict(lectura='cuadratica'), 'RANDOM15': dict(lectura='random15')}
REGLAS = ['xor01', 'px0', 'azar']
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


def metricas(r, vr):
    """Las de bateria_generaliza: acc = signo a priori sobre nunca vistos; ba = conducta al primer encuentro."""
    test = r['test']
    f = [1.0 if r['W_apriori'][k] > 0 else (0.5 if r['W_apriori'][k] == 0 else 0.0) for k in test if vr[k] == 'comida']
    p = [1.0 if r['W_apriori'][k] < 0 else (0.5 if r['W_apriori'][k] == 0 else 0.0) for k in test if vr[k] == 'veneno']
    pf = [r['primer'][k]['pb'] for k in test if r['primer'][k] is not None and vr[k] == 'comida']
    pp = [1 - r['primer'][k]['pb'] for k in test if r['primer'][k] is not None and vr[k] == 'veneno']
    return dict(acc=0.5 * float(np.mean(f)) + 0.5 * float(np.mean(p)), ba=(0.5 * float(np.mean(pf)) + 0.5 * float(np.mean(pp))) if (pf and pp) else None,
                cobertura=sum(v is not None for v in r['primer'].values()))


def tarea(args):
    tipo = args[0]
    if tipo == 'I':
        _, regla, seed = args
        import organismo_v13g as a_, organismo_v13q as b_
        kw = dict(T=60000, mundo='regla', regla=regla, eta_s=0.015, puerta=3)
        a, b = a_.run(seed, **kw), b_.run(seed, lectura='lineal', **kw)
        dif = [kk for kk in a if N(a[kk]) != N(b[kk])]
        return dict(tipo=tipo, esc=regla, seed=seed, identico=not dif, difieren=dif)
    _, brazo, regla, seed = args
    import organismo_v13q as m
    kw = dict(BASE); kw.update(BRAZOS[brazo]); kw['regla'] = regla
    r = m.run(seed, **kw)
    vr = m.split_regla(seed, regla)[3]
    out = dict(tipo='T', brazo=brazo, regla=regla, seed=seed, splits=r['splits'], celdas=r['celdas'], deaths=r['deaths'], **metricas(r, vr))
    if regla == 'xor01' and brazo == 'CUADRATICA':
        out['W_lenta_prod01'] = round(float(r['Wps'][6] - r['Wns'][6]), 3)   # peso neto del producto P0*P1 (indice 6 = primer par (0,1))
    return out


def med(xs):
    xs = [x for x in xs if x is not None]
    return float(np.median(xs)), float(min(xs)), float(max(xs))


if __name__ == '__main__':
    import multiprocessing as mp
    mp.set_start_method('spawn', force=True)
    stamp = time.strftime('%Y%m%d_%H%M%S')
    _log['f'] = open(os.path.join(RAIZ, 'datos', f'xor_lectura_s{SEEDS[0]}-{SEEDS[-1]}_{stamp}.log'), 'w', encoding='utf-8', newline='\n')
    pre = os.path.join(AQUI, 'PREREGISTRO_xor_lectura.md')
    log(f"ARRANQUE bloque 3 (XOR como limite de lectura). brazos {list(BRAZOS)}, reglas {REGLAS}, semillas {SEEDS[0]}-{SEEDS[-1]}. Pool({N_PARALELO}).")
    log(f"sha preregistro {h16(pre)}  script {h16(os.path.abspath(__file__))}  organismo_v13q {h16(os.path.join(AQUI, 'organismo_v13q.py'))}  organismo_v13g {h16(os.path.join(RAIZ, 'experimentos', 'v13_dos_vias', 'organismo_v13g.py'))}")
    try:
        ps = subprocess.run(['powershell', '-NoProfile', '-Command',
                             "Get-CimInstance Win32_Process | Where-Object { $_.Name -like 'python*' } | ForEach-Object { \"$($_.ProcessId) $($_.CommandLine)\" }"],
                            capture_output=True, text=True, timeout=60).stdout.strip().splitlines()
    except Exception as e:
        ps = [f"(no se pudo listar: {e})"]
    log(f"REGLA 11 — procesos python vivos ({len(ps)}), este es pid {os.getpid()}")
    V = {}
    with mp.Pool(N_PARALELO) as pool:
        ctrl = [('I', rg, s) for rg in ('xor01', 'px0') for s in (1, 2, 3)]
        log(f"ETAPA 1/3 — identidad lectura=lineal == organismo_v13g ({len(ctrl)})...")
        rc = pool.map(tarea, ctrl, chunksize=1)
        log(f"  identicos: {sum(x['identico'] for x in rc)}/{len(rc)}")
        for x in rc:
            if not x['identico']: log(f"      DIFIERE {x['esc']} s{x['seed']}: {x['difieren']}")
        V['IDENTIDAD'] = all(x['identico'] for x in rc)
        if not V['IDENTIDAD']:
            log("*** IDENTIDAD FALLIDA: se para."); sys.exit(1)
        tr = [('T', b, rg, s) for b in BRAZOS for rg in REGLAS for s in SEEDS]
        log(f"ETAPA 2/3 — {len(tr)} corridas...")
        res = []
        for i, r in enumerate(pool.imap_unordered(tarea, tr, chunksize=1), 1):
            res.append(r)
            if i % 30 == 0 or i == len(tr):
                log(f"          {i}/{len(tr)}")
    log("ETAPA 3/3 — analisis (acc = signo a priori en nunca vistos; ba = conducta al primer encuentro).")
    G = lambda b, rg: {r['seed']: r for r in res if r['brazo'] == b and r['regla'] == rg}
    for b in BRAZOS:
        for rg in REGLAS:
            g = list(G(b, rg).values())
            log(f"   {b:10s} {rg:5s} acc {med([r['acc'] for r in g])[0]:.3f} [{med([r['acc'] for r in g])[1]:.2f},{med([r['acc'] for r in g])[2]:.2f}]"
                f"  ba {med([r['ba'] for r in g])[0]:.3f}  cobertura {med([r['cobertura'] for r in g])[0]:.0f}/10  celdas {med([r['celdas'] for r in g])[0]:.0f}  muertes {med([r['deaths'] for r in g])[0]:.0f}"
                + (f"  W_lenta(P0*P1) {med([r['W_lenta_prod01'] for r in g])[0]:+.2f}" if (b == 'CUADRATICA' and rg == 'xor01') else ''))
    A = lambda b, rg, s: G(b, rg)[s]['acc']
    Bc = lambda b, rg, s: (G(b, rg)[s]['ba'] if G(b, rg)[s]['ba'] is not None else 0.5)
    par = lambda b1, b2, rg, f: sum(f(b1, rg, s) > f(b2, rg, s) for s in SEEDS)
    X0 = med([A('LINEAL', 'xor01', s) for s in SEEDS])[0] <= 0.60
    X1 = med([A('CUADRATICA', 'xor01', s) for s in SEEDS])[0] >= 0.80 and par('CUADRATICA', 'LINEAL', 'xor01', A) >= 15
    X2 = med([A('RANDOM15', 'xor01', s) for s in SEEDS])[0] <= 0.60
    X3 = med([A('CUADRATICA', 'px0', s) for s in SEEDS])[0] >= 0.65 and 0.35 <= med([A('CUADRATICA', 'azar', s) for s in SEEDS])[0] <= 0.65
    X4 = med([Bc('CUADRATICA', 'xor01', s) for s in SEEDS])[0] >= 0.55 and par('CUADRATICA', 'LINEAL', 'xor01', Bc) >= 15
    V.update(X0=X0, X1=X1, X2=X2, X3=X3, X4=X4, cuad_gt_lin_acc=par('CUADRATICA', 'LINEAL', 'xor01', A), cuad_gt_lin_ba=par('CUADRATICA', 'LINEAL', 'xor01', Bc),
             LIMITE_DE_LECTURA=bool(X0 and X1 and X2 and X3 and X4))
    log(f"   X0 LINEAL xor<=.60 {'OK' if X0 else 'NO'} | X1 CUADRATICA xor>=.80 y >LINEAL en {V['cuad_gt_lin_acc']}/20 {'OK' if X1 else 'NO'} | X2 RANDOM15<=.60 {'OK' if X2 else 'NO'}"
        f" | X3 regresion px0/azar {'OK' if X3 else 'NO'} | X4 conducta ba>=.55 y >LINEAL en {V['cuad_gt_lin_ba']}/20 {'OK' if X4 else 'NO'}")
    log(f"VEREDICTO xor_lectura: {'XOR ERA UN LIMITE DE LECTURA' if V['LIMITE_DE_LECTURA'] else 'NO (refutado o control caido)'}")
    meta = dict(fecha=time.strftime('%Y-%m-%dT%H:%M:%S'), semillas=SEEDS, base=BASE, brazos=BRAZOS, reglas=REGLAS, veredictos=V, identidades=rc, procesos_python=ps,
                sha_preregistro=h16(pre), sha_script=h16(os.path.abspath(__file__)), sha_instrumento=h16(os.path.join(AQUI, 'organismo_v13q.py')),
                python=platform.python_version(), numpy=np.__version__)
    dj = os.path.join(RAIZ, 'datos', f'xor_lectura_s{SEEDS[0]}-{SEEDS[-1]}_{stamp}.json')
    json.dump(dict(meta=meta, corridas=res), open(dj, 'w', encoding='utf-8'), ensure_ascii=False, default=str)
    log(f"datos -> {os.path.basename(dj)}  sha256_16 = {h16(dj)}")
    _log['f'].close()
