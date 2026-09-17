"""Re-verificacion sobre v13: 3T (composicion temporal) y capacidad (mundo grande). Ejecuta
PREREGISTRO_reverificacion_v13.md. REGLA 10: log desde el arranque. REGLA 11: procesos vivos.
Brazos: v11 = perillas apagadas (eta_s=0, puerta=None); v13 = eta_s=0.015, puerta=3 (el tronco).
Uso:  python experimentos/v13_reverificacion/corre_reverificacion_v13.py
"""
import sys, os, json, time, hashlib, platform, subprocess
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
import numpy as np

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
sys.path[:0] = [AQUI, os.path.join(RAIZ, 'experimentos', 'v11_generaliza'), os.path.join(RAIZ, 'experimentos', 'capacidad_grande'),
                os.path.join(RAIZ, 'experimentos', 'v11_evo_division'), os.path.join(RAIZ, 'organismo')]
import mundo_grande as G
SEEDS = list(range(41, 61))
ARMS = ['C1', 'C1p', 'C2', 'C2b', 'C3', 'C3C']
BRAZOS = {'v11': dict(mu_norm=True, div_signo=True), 'v13': dict(mu_norm=True, div_signo=True, eta_s=0.015, puerta=3)}
D_PIX, N_EST = 10, 60
PASOS = (20000, 60000)
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


def tarea(args):
    tipo = args[0]
    if tipo == 'IT':
        _, arm, seed = args
        import mundo_temporal_v11 as a_, mundo_temporal_v13 as b_
        a, b = a_.run(seed, arm=arm), b_.run(seed, arm=arm)
        dif = [k for k in a if N(a[k]) != N(b[k])]
        return dict(tipo=tipo, esc=arm, seed=seed, identico=not dif, difieren=dif)
    if tipo == 'IK':
        _, esc, seed = args
        import organismo_capD as a_, organismo_capD13 as b_
        if esc == 'corto6':
            nom, pats, val, R = G.mundo(6, 6); pt = 20000
        else:
            nom, pats, val, R = G.mundo(10, 20); pt = 3000
        kw = dict(T=G.T_de(pt, len(nom)), plan=G.plan_de(pt, nom, val), pats=pats, chk=G.chks(pt, len(nom)), lam=0.05, mu_norm=True, div_signo=True)
        a, b = a_.run(seed, **kw), b_.run(seed, **kw)
        dif = [k for k in a if N(a[k]) != N(b[k])]
        return dict(tipo=tipo, esc=esc, seed=seed, identico=not dif, difieren=dif)
    if tipo == 'T':
        _, brazo, arm, seed = args
        import mundo_temporal_v13 as m
        kw = dict(BRAZOS[brazo])
        r = m.run(seed, arm=arm, **kw)
        return dict(tipo='T', brazo=brazo, arm=arm, seed=seed, W=r['W'], sep=r['sep'], solap_A=r['solap_A'], lift=r['lift'],
                    n_AB=r['n_AB'], n_AA=r['n_AA'], n_B=r['n_B'], deaths=r['deaths'], Rtot=r['Rtot'], splits=r['splits'])
    _, brazo, pt, seed = args
    import organismo_capD13 as o
    nom, pats, val, R = G.mundo(D_PIX, N_EST)
    r = o.run(seed, T=G.T_de(pt, N_EST), plan=G.plan_de(pt, nom, val), pats=pats, chk=G.chks(pt, N_EST), plast=True, lam=0.05,
              memoria_rechazo=20, **BRAZOS[brazo])
    for h in r['hist']:
        h['dev'] = {k: round(abs(v - R[k]), 3) for k, v in h['W'].items()}
    hist = [dict(t=h['t'], n=h['n'], celdas=h['celdas'], splits=h['splits'], dev=h['dev']) for h in r['hist']]
    return dict(tipo='K', brazo=brazo, pt=pt, seed=seed, hist=hist, deaths=r['deaths'], t_agot=r['t_agot'], splits=r['splits'],
                celdas=r['celdas'], nofam_fin=r['nofam_fin'], W_fin={k: round(float(v), 4) for k, v in r['W'].items()})


def med(xs):
    return float(np.median(xs)), float(min(xs)), float(max(xs))


if __name__ == '__main__':
    import multiprocessing as mp
    mp.set_start_method('spawn', force=True)
    stamp = time.strftime('%Y%m%d_%H%M%S')
    _log['f'] = open(os.path.join(RAIZ, 'datos', f'reverificacion_v13_{stamp}.log'), 'w', encoding='utf-8', newline='\n')
    pre = os.path.join(AQUI, 'PREREGISTRO_reverificacion_v13.md')
    shas = {n_: h16(p) for n_, p in [('preregistro', pre), ('script', os.path.abspath(__file__)),
            ('mundo_temporal_v13', os.path.join(AQUI, 'mundo_temporal_v13.py')), ('capD13', os.path.join(AQUI, 'organismo_capD13.py')),
            ('v13', os.path.join(RAIZ, 'organismo', 'organismo_v13.py'))]}
    log(f"ARRANQUE re-verificacion sobre v13 (3T + capacidad grande). semillas {SEEDS[0]}-{SEEDS[-1]}. Pool({N_PARALELO}).")
    log("sha " + "  ".join(f"{k} {v}" for k, v in shas.items()))
    try:
        ps = subprocess.run(['powershell', '-NoProfile', '-Command',
                             "Get-CimInstance Win32_Process | Where-Object { $_.Name -like 'python*' } | ForEach-Object { \"$($_.ProcessId) $($_.CommandLine)\" }"],
                            capture_output=True, text=True, timeout=60).stdout.strip().splitlines()
    except Exception as e:
        ps = [f"(no se pudo listar: {e})"]
    log(f"REGLA 11 — procesos python vivos ({len(ps)}), este es pid {os.getpid()}")
    V = {}
    with mp.Pool(N_PARALELO) as pool:
        ctrl = [('IT', a, s) for a in ARMS for s in (1, 2, 3)] + [('IK', e, s) for e in ('corto6', 'grande20') for s in (1, 2)]
        log(f"ETAPA 1/4 — inercia ({len(ctrl)})...")
        rc = pool.map(tarea, ctrl, chunksize=1)
        for t, nombre in (('IT', 'mundo_temporal_v13(0,None) == v11'), ('IK', 'capD13(0,None) == capD')):
            g = [x for x in rc if x['tipo'] == t]
            log(f"  {nombre:36s}: {sum(x['identico'] for x in g)}/{len(g)}")
            for x in g:
                if not x['identico']:
                    log(f"      DIFIERE {x['esc']} s{x['seed']}: {x['difieren']}")
        V['INERCIA'] = all(x['identico'] for x in rc)
        if not V['INERCIA']:
            log("*** INERCIA FALLIDA: se para y se arregla el instrumento."); sys.exit(1)
        trabajos = ([('K', b, pt, s) for pt in sorted(PASOS, reverse=True) for b in BRAZOS for s in SEEDS]
                    + [('T', b, a, s) for b in BRAZOS for a in ARMS for s in SEEDS])
        log(f"ETAPA 2/4 — {len(trabajos)} corridas (K: 80 largas primero; T: 240)...")
        res = []
        for i, r in enumerate(pool.imap_unordered(tarea, trabajos, chunksize=1), 1):
            res.append(r)
            if i % 20 == 0 or i == len(trabajos):
                log(f"          {i}/{len(trabajos)}")
    log("ETAPA 3/4 — analisis.")
    GT = lambda b, a: {r['seed']: r for r in res if r['tipo'] == 'T' and r['brazo'] == b and r['arm'] == a}
    log(); log("  BLOQUE T (3T sobre v13)")
    kt2 = sum(all(N(GT('v13', 'C1')[s][k]) == N(GT('v13', 'C2b')[s][k]) for k in ('W', 'sep', 'n_AB', 'n_AA', 'n_B', 'deaths', 'Rtot')) for s in SEEDS)
    V['KT2'] = kt2 == 20
    log(f"   KT2 C2b == C1 bajo v13: {kt2}/20")
    for b in BRAZOS:
        for a in ARMS:
            g = list(GT(b, a).values())
            log(f"   {b:4s} {a:4s} sep {med([r['sep'] for r in g])[0]:+.2f} [{med([r['sep'] for r in g])[1]:+.2f},{med([r['sep'] for r in g])[2]:+.2f}]"
                f"  lift_q4 {med([r['lift'][3] for r in g])[0]:+.3f}  solap_A {med([r['solap_A'] for r in g])[0]:.0f}"
                f"  divisiones {med([r['splits'] for r in g])[0]:.0f}  muertes {med([r['deaths'] for r in g])[0]:.0f}")
    c3, c3c = list(GT('v13', 'C3').values()), list(GT('v13', 'C3C').values()); c3_11 = list(GT('v11', 'C3').values())
    V['T1'] = med([r['solap_A'] for r in c3])[0] <= 1 and sum(r['solap_A'] <= 1 for r in c3) >= 15
    V['T2'] = med([r['sep'] for r in c3])[0] >= 1.0
    V['T3'] = med([r['lift'][3] for r in c3])[0] >= 0.15
    V['T4'] = med([r['sep'] for r in c3c])[0] < 1.0 and med([r['lift'][3] for r in c3c])[0] < 0.15
    V['T5_no_inferioridad'] = med([r['sep'] for r in c3])[0] >= med([r['sep'] for r in c3_11])[0] - 1.0
    V['T6_sin_otra_puerta'] = med([r['sep'] for r in GT('v13', 'C2b').values()])[0] < 1.0 and med([r['sep'] for r in GT('v13', 'C1p').values()])[0] < 1.0
    for k in ('T1', 'T2', 'T3', 'T4', 'T5_no_inferioridad', 'T6_sin_otra_puerta'):
        log(f"   {k}: {'SOSTENIDA' if V[k] else 'REFUTADA'}")
    GK = lambda b, pt: {r['seed']: r for r in res if r['tipo'] == 'K' and r['brazo'] == b and r['pt'] == pt}
    log(); log("  BLOQUE K (capacidad, mundo grande 10 px / 60 estimulos)")
    tab = {}
    for pt in PASOS:
        for b in BRAZOS:
            g = GK(b, pt)
            Ns = [G.techo(g[s]['hist']) for s in SEEDS]; Ms = [G.m_max(g[s]['hist']) for s in SEEDS]
            fin = [v for s in SEEDS for v in g[s]['W_fin'].values()]
            ceros = sum(abs(v) < 0.0005 for v in fin)
            tab[(b, pt)] = dict(N=med(Ns)[0], M=med(Ms)[0], ceros=ceros, nfin=len(fin))
            log(f"   {pt//1000}k {b:4s}: N* {med(Ns)[0]:.1f} [{med(Ns)[1]:.0f},{med(Ns)[2]:.0f}]  M_max {med(Ms)[0]:.1f} [{med(Ms)[1]:.0f},{med(Ms)[2]:.0f}]"
                f"  W=0 {ceros}/{len(fin)}  agotan {sum(g[s]['t_agot'] is not None for s in SEEDS)}/20  celdas {med([g[s]['celdas'] for s in SEEDS])[0]:.0f}"
                f"  divisiones {med([g[s]['splits'] for s in SEEDS])[0]:.0f}  muertes {med([g[s]['deaths'] for s in SEEDS])[0]:.0f}"
                f"  no-familiares al final {med([g[s]['nofam_fin'] for s in SEEDS])[0]:.0f}/60")
    V['K1'] = tab[('v13', 20000)]['ceros'] <= 0.05 * tab[('v13', 20000)]['nfin']
    V['K2_no_inferioridad'] = all(tab[('v13', pt)]['M'] >= tab[('v11', pt)]['M'] - 3 for pt in PASOS)
    V['K3_no_inferioridad'] = all(tab[('v13', pt)]['N'] >= tab[('v11', pt)]['N'] - 5 for pt in PASOS)
    for k in ('K1', 'K2_no_inferioridad', 'K3_no_inferioridad'):
        log(f"   {k}: {'SOSTENIDA' if V[k] else 'REFUTADA'}")
    V['3T_SOBREVIVE'] = bool(V['KT2'] and all(V[k] for k in ('T1', 'T2', 'T3', 'T4', 'T5_no_inferioridad', 'T6_sin_otra_puerta')))
    V['CAPACIDAD_SOBREVIVE'] = bool(V['K1'] and V['K2_no_inferioridad'] and V['K3_no_inferioridad'])
    log(); log("VEREDICTO reverificacion_v13: " + " ".join(f"{k}={v}" for k, v in V.items()))
    log("ETAPA 4/4 — escritura.")
    meta = dict(fecha=time.strftime('%Y-%m-%dT%H:%M:%S'), semillas=SEEDS, veredictos=V, identidades=rc, tabla_K={f"{b}_{pt}": v for (b, pt), v in tab.items()},
                shas=shas, procesos_python=ps, python=platform.python_version(), numpy=np.__version__)
    dj = os.path.join(RAIZ, 'datos', f'reverificacion_v13_{stamp}.json')
    json.dump(dict(meta=meta, corridas=res), open(dj, 'w', encoding='utf-8'), ensure_ascii=False, default=str)
    log(f"datos -> {os.path.basename(dj)}  sha256_16 = {h16(dj)}")
    _log['f'].close()
