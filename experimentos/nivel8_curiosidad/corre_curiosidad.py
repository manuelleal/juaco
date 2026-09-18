"""Bloque 2: curiosidad por progreso de error contra el canje del mapa, en el mundo largo. Ejecuta PREREGISTRO_curiosidad.md.
REGLA 10: log desde el arranque. Identidad: mundo_largo_c con gamma_C=0 == mundo_largo (todas las claves, mundo completo).
Uso:  python experimentos/nivel8_curiosidad/corre_curiosidad.py [--desde N]   (por defecto semillas 41-60)
"""
import sys, os, json, time, hashlib, platform, subprocess
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
import numpy as np

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
sys.path[:0] = [AQUI, os.path.join(RAIZ, 'experimentos', 'nivel8_mundo_largo'), os.path.join(RAIZ, 'experimentos', 'nivel6_mapa'), os.path.join(RAIZ, 'organismo')]
from corre_mundo_largo import pool_de, sitios_de, recuperacion, T, T_NUEVO, T_INV
_desde = int(sys.argv[sys.argv.index('--desde') + 1]) if '--desde' in sys.argv else 41
SEEDS = list(range(_desde, _desde + 20))
BRAZOS = {
    'V13':          dict(usa_M=False),
    'MAPA':         dict(usa_M=True),
    'MAPA_CUR':     dict(usa_M=True, gamma_C=1.0),
    'MAPA_CUR_BAR': dict(usa_M=True, gamma_C=1.0, cur_barajada=True),
}
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


def mundo_kw(seed):
    pool = pool_de(seed)
    return dict(T=T, r_vis=3, sitios=sitios_de(pool, seed), pool=pool, T_nuevo=T_NUEVO, invertir_largo=T_INV)


def tarea(args):
    tipo = args[0]
    if tipo == 'I':
        _, seed = args
        import mundo_largo as a_, mundo_largo_c as b_
        kw = mundo_kw(seed); kw.update(usa_M=True)
        a, b = a_.run(seed, **kw), b_.run(seed, **kw)
        dif = [kk for kk in a if N(a[kk]) != N(b[kk])]
        return dict(tipo=tipo, esc='ident', seed=seed, identico=not dif, difieren=dif)
    _, brazo, seed = args
    import mundo_largo_c as m
    kw = mundo_kw(seed); kw.update(BRAZOS[brazo])
    r = m.run(seed, **kw)
    cv = r['curva']
    hasta30 = [c[2] for c in cv if c[1] <= 30]; fin = cv[-1] if cv else (None, None, None, None)
    vf = r['val_final']; vs = r['vistos']; W = r['W']
    ok = lambda n: (W[n] > 0) == (vf[n] == 'comida')
    return dict(tipo='T', brazo=brazo, seed=seed, curva=cv, adq_hasta30=float(np.median(hasta30)) if hasta30 else None, adq_final=fin[2],
                ret_no_inv=float(np.mean([ok(n) for n in vs[4:10]])) if len(vs) >= 10 else None, comida_q4=int(sum(r['mord'][k][3] for k in r['mord'] if vf.get(k) == 'comida')),
                deaths=r['deaths'], celdas=r['celdas'], splits=r['splits'], **recuperacion(r['comida_bin'], r['muertes_bin']))


def med(xs):
    xs = [x for x in xs if x is not None]
    return float(np.median(xs)), float(min(xs)), float(max(xs))


if __name__ == '__main__':
    import multiprocessing as mp
    mp.set_start_method('spawn', force=True)
    stamp = time.strftime('%Y%m%d_%H%M%S')
    _log['f'] = open(os.path.join(RAIZ, 'datos', f'curiosidad_s{SEEDS[0]}-{SEEDS[-1]}_{stamp}.log'), 'w', encoding='utf-8', newline='\n')
    pre = os.path.join(AQUI, 'PREREGISTRO_curiosidad.md')
    log(f"ARRANQUE bloque 2 (curiosidad por progreso contra el canje del mapa), mundo largo. brazos {list(BRAZOS)}, semillas {SEEDS[0]}-{SEEDS[-1]}. Pool({N_PARALELO}).")
    log(f"sha preregistro {h16(pre)}  script {h16(os.path.abspath(__file__))}  mundo_largo_c {h16(os.path.join(AQUI, 'mundo_largo_c.py'))}  mundo_largo {h16(os.path.join(RAIZ, 'experimentos', 'nivel8_mundo_largo', 'mundo_largo.py'))}  v13 {h16(os.path.join(RAIZ, 'organismo', 'organismo_v13.py'))}")
    try:
        ps = subprocess.run(['powershell', '-NoProfile', '-Command',
                             "Get-CimInstance Win32_Process | Where-Object { $_.Name -like 'python*' } | ForEach-Object { \"$($_.ProcessId) $($_.CommandLine)\" }"],
                            capture_output=True, text=True, timeout=60).stdout.strip().splitlines()
    except Exception as e:
        ps = [f"(no se pudo listar: {e})"]
    log(f"REGLA 11 — procesos python vivos ({len(ps)}), este es pid {os.getpid()}")
    V = {}
    with mp.Pool(N_PARALELO) as pool:
        ctrl = [('I', s) for s in (1, 2, 3)]
        log(f"ETAPA 1/3 — identidad gamma_C=0 == mundo_largo, mundo completo con mapa ({len(ctrl)})...")
        rc = pool.map(tarea, ctrl, chunksize=1)
        log(f"  identicos: {sum(x['identico'] for x in rc)}/{len(rc)}")
        for x in rc:
            if not x['identico']: log(f"      DIFIERE {x['esc']} s{x['seed']}: {x['difieren']}")
        V['IDENTIDAD'] = all(x['identico'] for x in rc)
        if not V['IDENTIDAD']:
            log("*** IDENTIDAD FALLIDA: se para."); sys.exit(1)
        tr = [('T', b, s) for b in BRAZOS for s in SEEDS]
        log(f"ETAPA 2/3 — {len(tr)} corridas...")
        res = []
        for i, r in enumerate(pool.imap_unordered(tarea, tr, chunksize=1), 1):
            res.append(r)
            if i % 20 == 0 or i == len(tr):
                log(f"          {i}/{len(tr)}")
    log("ETAPA 3/3 — analisis.")
    G = lambda b: {r['seed']: r for r in res if r['brazo'] == b}
    A = lambda b, s: (G(b)[s]['adq_hasta30'] if G(b)[s]['adq_hasta30'] is not None else 0.0)
    for b in BRAZOS:
        g = list(G(b).values())
        log(f"   {b:12s} adq(<=30) {med([r['adq_hasta30'] for r in g])[0]:.3f} [{med([r['adq_hasta30'] for r in g])[1]:.2f},{med([r['adq_hasta30'] for r in g])[2]:.2f}]  adq(final) {med([r['adq_final'] for r in g])[0]:.3f}"
            f"  ret_no_inv {med([r['ret_no_inv'] for r in g])[0]:.2f}  comida_q4 {med([r['comida_q4'] for r in g])[0]:.0f}  muertes {med([r['deaths'] for r in g])[0]:.0f}"
            f"  recup {med([r['rec'] for r in g])[0]:.0f}  celdas {med([r['celdas'] for r in g])[0]:.0f}  divisiones {med([r['splits'] for r in g])[0]:.0f}")
    par = lambda b1, b2: sum(A(b1, s) > A(b2, s) for s in SEEDS)
    cur, mapa, bar = G('MAPA_CUR'), G('MAPA'), G('MAPA_CUR_BAR')
    P1 = med([A('MAPA_CUR', s) for s in SEEDS])[0] >= 0.85 and par('MAPA_CUR', 'MAPA') >= 15
    p2n = sum(cur[s]['comida_q4'] >= 0.9 * mapa[s]['comida_q4'] for s in SEEDS)
    P2 = med([cur[s]['comida_q4'] for s in SEEDS])[0] >= 450 and p2n >= 15
    P3 = par('MAPA_CUR', 'MAPA_CUR_BAR') >= 15 and par('MAPA_CUR_BAR', 'MAPA') < 15
    V.update(P1=P1, P2=P2, P3=P3, cur_gt_mapa=par('MAPA_CUR', 'MAPA'), cur_gt_bar=par('MAPA_CUR', 'MAPA_CUR_BAR'), bar_gt_mapa=par('MAPA_CUR_BAR', 'MAPA'), P2_n=p2n,
             DEVUELVE_EXPLORACION=bool(P1 and P2 and P3))
    log(f"   P1 CUR adq>=.85 y >MAPA en {V['cur_gt_mapa']}/20 {'OK' if P1 else 'NO'} | P2 comida_q4>=450 y >=0.9xMAPA en {p2n}/20 {'OK' if P2 else 'NO'}"
        f" | P3 CUR>BARAJADA en {V['cur_gt_bar']}/20 y BARAJADA>MAPA en {V['bar_gt_mapa']}/20 {'OK' if P3 else 'NO'}")
    log(f"VEREDICTO curiosidad: {'DEVUELVE la exploracion sin cobrar la comida' if V['DEVUELVE_EXPLORACION'] else 'NO (refutado o control caido)'}")
    meta = dict(fecha=time.strftime('%Y-%m-%dT%H:%M:%S'), semillas=SEEDS, brazos=BRAZOS, veredictos=V, identidades=rc, procesos_python=ps,
                sha_preregistro=h16(pre), sha_script=h16(os.path.abspath(__file__)), sha_mundo=h16(os.path.join(AQUI, 'mundo_largo_c.py')),
                python=platform.python_version(), numpy=np.__version__)
    dj = os.path.join(RAIZ, 'datos', f'curiosidad_s{SEEDS[0]}-{SEEDS[-1]}_{stamp}.json')
    json.dump(dict(meta=meta, corridas=res), open(dj, 'w', encoding='utf-8'), ensure_ascii=False, default=str)
    log(f"datos -> {os.path.basename(dj)}  sha256_16 = {h16(dj)}")
    _log['f'].close()
