"""Nivel 7, experimento 1 del plan: 3T con profundidad k in {1,2,3} sobre v13 (el organismo NO cambia; cambia el mundo).
Ejecuta PREREGISTRO_3T_k.md. REGLA 10: log desde el arranque. Identidad k=1 == mundo_temporal_v13, todas las claves.
Uso:  python experimentos/nivel7_3T_k/corre_3T_k.py [--desde N]
"""
import sys, os, json, time, hashlib, platform, subprocess
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
import numpy as np

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
sys.path[:0] = [AQUI, os.path.join(RAIZ, 'experimentos', 'v13_reverificacion'), os.path.join(RAIZ, 'organismo')]
_desde = int(sys.argv[sys.argv.index('--desde') + 1]) if '--desde' in sys.argv else 1
SEEDS = list(range(_desde, _desde + 20))
ARMS = ['C1', 'C1p', 'C2b', 'C3', 'C3C']
KS = [int(v) for v in sys.argv[sys.argv.index('--ks') + 1].split(',')] if '--ks' in sys.argv else [1, 2, 3]   # enmienda 2: --ks 4,5
V13 = dict(mu_norm=True, div_signo=True, eta_s=0.015, puerta=3)
UMBRAL_SEP = {1: 1.0, 2: 3.0, 3: 2.0, 4: 1.5, 5: 1.0}   # enmienda 2
N_PARALELO = 14
RAPIDO = '--rapido' in sys.argv   # gemelo compilado (mundo_temporal_k_rapido, identidad 146/146): solo si su etapa de identidad da 3/3
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


def tarea(args):
    tipo = args[0]
    if tipo == 'I':
        _, arm, seed = args
        import mundo_temporal_v13 as a_, mundo_temporal_k as b_
        a, b = a_.run(seed, arm=arm, **V13), b_.run(seed, arm=arm, kprof=1, **V13)
        dif = [kk for kk in a if N(a[kk]) != N(b[kk])]
        return dict(tipo=tipo, esc=arm, seed=seed, identico=not dif, difieren=dif)
    if tipo == 'R':   # identidad del gemelo compilado contra el original (C3, k=3)
        _, seed = args
        import mundo_temporal_k as a_, mundo_temporal_k_rapido as b_
        a, b = a_.run(seed, arm='C3', kprof=3, T=30000, **V13), b_.run(seed, arm='C3', kprof=3, T=30000, **V13)
        dif = [kk for kk in a if N(a[kk]) != N(b[kk])]
        return dict(tipo=tipo, esc='rapido', seed=seed, identico=not dif, difieren=dif)
    _, k, arm, seed = args
    if RAPIDO:
        import mundo_temporal_k_rapido as m
    else:
        import mundo_temporal_k as m
    r = m.run(seed, arm=arm, kprof=k, **V13)
    return dict(tipo='T', k=k, arm=arm, seed=seed, W=r['W'], sep=r['sep'], solap_A=r['solap_A'], lift=r['lift'],
                deaths=r['deaths'], splits=r['splits'], celdas=r.get('celdas'))


def med(xs):
    return float(np.median(xs)), float(min(xs)), float(max(xs))


if __name__ == '__main__':
    import multiprocessing as mp
    mp.set_start_method('spawn', force=True)
    stamp = time.strftime('%Y%m%d_%H%M%S')
    _log['f'] = open(os.path.join(RAIZ, 'datos', f'3T_k{"".join(map(str, KS))}_s{SEEDS[0]}-{SEEDS[-1]}_{stamp}.log'), 'w', encoding='utf-8', newline='\n')
    pre = os.path.join(AQUI, 'PREREGISTRO_3T_k.md')
    log(f"ARRANQUE 3T-k sobre v13. k en {KS}, brazos {ARMS}, semillas {SEEDS[0]}-{SEEDS[-1]}. Pool({N_PARALELO}). {'GEMELO COMPILADO (--rapido)' if RAPIDO else 'Python puro'}")
    log(f"sha preregistro {h16(pre)}  script {h16(os.path.abspath(__file__))}  mundo_temporal_k {h16(os.path.join(AQUI, 'mundo_temporal_k.py'))}  v13 {h16(os.path.join(RAIZ, 'organismo', 'organismo_v13.py'))}")
    try:
        ps = subprocess.run(['powershell', '-NoProfile', '-Command',
                             "Get-CimInstance Win32_Process | Where-Object { $_.Name -like 'python*' } | ForEach-Object { \"$($_.ProcessId) $($_.CommandLine)\" }"],
                            capture_output=True, text=True, timeout=60).stdout.strip().splitlines()
    except Exception as e:
        ps = [f"(no se pudo listar: {e})"]
    log(f"REGLA 11 — procesos python vivos ({len(ps)}), este es pid {os.getpid()}")
    V = {}
    with mp.Pool(N_PARALELO) as pool:
        ctrl = [('I', a, s) for a in ARMS + ['C2'] for s in (1, 2, 3)]
        log(f"ETAPA 1/3 — identidad k=1 == mundo_temporal_v13 ({len(ctrl)})...")
        rc = pool.map(tarea, ctrl, chunksize=1)
        log(f"  identicos: {sum(x['identico'] for x in rc)}/{len(rc)}")
        for x in rc:
            if not x['identico']: log(f"      DIFIERE {x['esc']} s{x['seed']}: {x['difieren']}")
        V['IDENTIDAD'] = all(x['identico'] for x in rc)
        if not V['IDENTIDAD']:
            log("*** IDENTIDAD FALLIDA: se para."); sys.exit(1)
        if RAPIDO:
            rr = pool.map(tarea, [('R', s) for s in (1, 2, 3)], chunksize=1)
            log(f"  identidad gemelo compilado == original (C3, k=3, T=30000): {sum(x['identico'] for x in rr)}/3")
            if not all(x['identico'] for x in rr):
                log('*** GEMELO NO IDENTICO: se para (corre sin --rapido).'); sys.exit(1)
            V['IDENTIDAD_RAPIDO'] = True
        tr = [('T', k, a, s) for k in KS for a in ARMS for s in SEEDS]
        log(f"ETAPA 2/3 — {len(tr)} corridas...")
        res = []
        for i, r in enumerate(pool.imap_unordered(tarea, tr, chunksize=1), 1):
            res.append(r)
            if i % 30 == 0 or i == len(tr):
                log(f"          {i}/{len(tr)}")
    log("ETAPA 3/3 — analisis.")
    G = lambda k, a: {r['seed']: r for r in res if r['k'] == k and r['arm'] == a}
    for k in KS:
        log(); log(f"  k = {k}")
        for a in ARMS:
            g = list(G(k, a).values())
            log(f"   {a:4s} sep {med([r['sep'] for r in g])[0]:+.2f} [{med([r['sep'] for r in g])[1]:+.2f},{med([r['sep'] for r in g])[2]:+.2f}]"
                f"  lift_q4 {med([r['lift'][3] if r['lift'][3] is not None else 0 for r in g])[0]:+.3f}  solap_A {med([r['solap_A'] for r in g])[0]:.2f}"
                f"  divisiones {med([r['splits'] for r in g])[0]:.0f}  celdas {med([r['celdas'] if r['celdas'] is not None else 0 for r in g])[0]:.0f}  muertes {med([r['deaths'] for r in g])[0]:.0f}")
        c3 = G(k, 'C3'); c3c = G(k, 'C3C')
        t1 = med([c3[s]['solap_A'] for s in SEEDS])[0] <= 1 and sum(c3[s]['solap_A'] <= 1 for s in SEEDS) >= 15
        t2 = med([c3[s]['sep'] for s in SEEDS])[0] >= UMBRAL_SEP[k]
        t3 = med([c3[s]['lift'][3] if c3[s]['lift'][3] is not None else 0 for s in SEEDS])[0] >= 0.15
        t4 = med([c3c[s]['sep'] for s in SEEDS])[0] < 1.0 and med([c3c[s]['lift'][3] if c3c[s]['lift'][3] is not None else 0 for s in SEEDS])[0] < 0.15
        t5n = sum(c3[s]['sep'] - c3c[s]['sep'] >= 1.0 for s in SEEDS); t5 = t5n >= 15
        t6 = med([G(k, 'C2b')[s]['sep'] for s in SEEDS])[0] < 1.0 and med([G(k, 'C1p')[s]['sep'] for s in SEEDS])[0] < 1.0
        V[f'k{k}'] = dict(T1=t1, T2=t2, T3=t3, T4=t4, T5=t5, T6=t6, compone=bool(t1 and t2 and t3 and t4 and t5 and t6))
        log(f"   T1 solap<=1 {'OK' if t1 else 'NO'} | T2 sep>={UMBRAL_SEP[k]} {'OK' if t2 else 'NO'} | T3 lift>=.15 {'OK' if t3 else 'NO'} | T4 C3C {'OK' if t4 else 'NO'}"
            f" | T5 C3-C3C>=1 en {t5n}/20 {'OK' if t5 else 'NO'} | T6 C2b,C1p<1 {'OK' if t6 else 'NO'}  -> {'COMPONE' if V[f'k{k}']['compone'] else 'NO COMPONE'} a profundidad {k}")
    log(); log("VEREDICTO 3T_k: " + " ".join(f"k{k}={'COMPONE' if V[f'k{k}']['compone'] else 'NO'}" for k in KS))
    meta = dict(fecha=time.strftime('%Y-%m-%dT%H:%M:%S'), semillas=SEEDS, ks=KS, veredictos=V, identidades=rc, procesos_python=ps,
                sha_preregistro=h16(pre), sha_script=h16(os.path.abspath(__file__)), sha_mundo=h16(os.path.join(AQUI, 'mundo_temporal_k.py')),
                python=platform.python_version(), numpy=np.__version__)
    dj = os.path.join(RAIZ, 'datos', f'3T_k{"".join(map(str, KS))}_s{SEEDS[0]}-{SEEDS[-1]}_{stamp}.json')
    json.dump(dict(meta=meta, corridas=res), open(dj, 'w', encoding='utf-8'), ensure_ascii=False, default=str)
    log(f"datos -> {os.path.basename(dj)}  sha256_16 = {h16(dj)}")
    _log['f'].close()
