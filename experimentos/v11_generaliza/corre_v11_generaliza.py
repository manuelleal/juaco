"""Re-verificacion sobre v11: Etapa 3 (generalizacion) y 3T (composicion temporal). Ejecuta
PREREGISTRO_v11_generaliza.md. Umbrales reutilizados sin tocar de PREREGISTRO_etapa3_v9.md (5a2af284ee73ae76) y
PREREGISTRO_reverificacion_v9.md (2708cb73ab8531e8). REGLA 10: log desde el arranque. REGLA 11: procesos vivos.

Metricas copiadas literalmente de corre_etapa3_v9.py (acc_signo, ba_pb) y corre_reverificacion.py (sep, lift, solap_A).
Precisiones escritas ANTES de correr:
- Los tres brazos usan el MISMO instrumento; solo cambian mu_norm y div_signo.
- Cobertura K: >= 6 de los 10 patrones de test con primer encuentro registrado, en >= 18/20 semillas (brazo v11).
- Comparaciones pareadas estrictas por semilla.
Uso:  python experimentos/v11_generaliza/corre_v11_generaliza.py
"""
import sys, os, json, time, hashlib, platform, subprocess
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
import numpy as np

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
sys.path[:0] = [AQUI, os.path.join(RAIZ, 'organismo'), os.path.join(RAIZ, 'experimentos', 'etapa3_v9'),
                os.path.join(RAIZ, 'experimentos', 'v9_reverificacion')]
SEEDS = list(range(41, 61))
R = {'comida': 1.0, 'veneno': -3.0}
REGLAS = ['px0', 'azar', 'xor01']
BRAZOS = {'v9': dict(mu_norm=False, div_signo=False), 'v10': dict(mu_norm=True, div_signo=False), 'v11': dict(mu_norm=True, div_signo=True)}
ARMS_T = ['C1', 'C1p', 'C2', 'C2b', 'C3', 'C3C']
ESC_ID = {'E1': dict(), 'E2': dict(invertir_en=50000), 'E2L': dict(solap_AB=3)}
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
    if tipo == 'K':
        _, cual, esc, seed = args
        import organismo_v11g as g
        if cual == 'v11':
            import organismo_v11 as ref
            a, b = ref.run(seed, **ESC_ID[esc]), g.run(seed, **ESC_ID[esc])
            dif = [k for k in a if N(a[k]) != N(b[k])]
        else:
            import organismo_v9g as g9
            kw = dict(T=40000, mundo='regla', regla=esc) if esc in REGLAS else ESC_ID[esc]
            a, b = g9.run(seed, **kw), g.run(seed, mu_norm=False, div_signo=False, **kw)
            dif = [k for k in a if N(a[k]) != N(b[k])]
        return dict(tipo=tipo, cual=cual, esc=esc, seed=seed, identico=not dif, difieren=dif)
    if tipo == 'KT1':
        _, arm, seed = args
        import mundo_temporal_v9 as m9, mundo_temporal_v11 as m11
        a, b = m9.run(seed, arm=arm), m11.run(seed, arm=arm)
        dif = [k for k in a if N(a[k]) != N(b[k])]
        return dict(tipo=tipo, esc=arm, seed=seed, identico=not dif, difieren=dif)
    if tipo == 'G':
        _, brazo, regla, seed = args
        import organismo_v11g as g
        r = g.run(seed, T=200000, mundo='regla', regla=regla, **BRAZOS[brazo])
        return dict(tipo='G', brazo=brazo, regla=regla, seed=seed, tren=r['tren'], test=r['test'],
                    W_apriori=r['W_apriori'], primer=r['primer'], splits=r['splits'], celdas=r['celdas'],
                    deaths=r['deaths'], n_techo=r['n_techo'], W_final=r['W_final'])
    _, brazo, arm, seed = args
    import mundo_temporal_v11 as m
    r = m.run(seed, arm=arm, **BRAZOS[brazo])
    return dict(tipo='T', brazo=brazo, arm=arm, seed=seed, W=r['W'], sep=r['sep'], solap_A=r['solap_A'], lift=r['lift'],
                n_AB=r['n_AB'], n_AA=r['n_AA'], n_B=r['n_B'], deaths=r['deaths'], Rtot=r['Rtot'], splits=r['splits'])


def valencia(regla, seed):
    import organismo_v11g as g
    return g.split_regla(seed, regla)[3]


def acc_signo(r, vr):
    f = []; p = []
    for k in r['test']:
        w = r['W_apriori'][k]
        s = 0.5 if w == 0 else (1.0 if w > 0 else 0.0)
        (f if vr[k] == 'comida' else p).append(s if vr[k] == 'comida' else 1 - s)
    return 0.5 * np.mean(f) + 0.5 * np.mean(p)


def ba_pb(r, vr):
    f = [r['primer'][k]['pb'] for k in r['test'] if r['primer'][k] is not None and vr[k] == 'comida']
    p = [1 - r['primer'][k]['pb'] for k in r['test'] if r['primer'][k] is not None and vr[k] == 'veneno']
    if not f or not p:
        return None
    return 0.5 * np.mean(f) + 0.5 * np.mean(p)


def med(xs):
    return float(np.median(xs)), float(min(xs)), float(max(xs))


if __name__ == '__main__':
    import multiprocessing as mp
    mp.set_start_method('spawn', force=True)
    stamp = time.strftime('%Y%m%d_%H%M%S')
    _log['f'] = open(os.path.join(RAIZ, 'datos', f'v11_generaliza_{stamp}.log'), 'w', encoding='utf-8', newline='\n')
    pre = os.path.join(AQUI, 'PREREGISTRO_v11_generaliza.md')
    shas = {n: h16(p) for n, p in [('preregistro', pre), ('script', os.path.abspath(__file__)),
            ('v11g', os.path.join(AQUI, 'organismo_v11g.py')), ('mundo_temporal_v11', os.path.join(AQUI, 'mundo_temporal_v11.py')),
            ('v11', os.path.join(RAIZ, 'organismo', 'organismo_v11.py')),
            ('v9g', os.path.join(RAIZ, 'experimentos', 'etapa3_v9', 'organismo_v9g.py'))]}
    log(f"ARRANQUE re-verificacion sobre v11 (Etapa 3 + 3T). semillas {SEEDS[0]}..{SEEDS[-1]}. Pool({N_PARALELO}).")
    log("sha " + "  ".join(f"{k} {v}" for k, v in shas.items()))
    try:
        ps = subprocess.run(['powershell', '-NoProfile', '-Command',
                             "Get-CimInstance Win32_Process | Where-Object { $_.Name -like 'python*' } | ForEach-Object { \"$($_.ProcessId) $($_.CommandLine)\" }"],
                            capture_output=True, text=True, timeout=60).stdout.strip().splitlines()
    except Exception as e:
        ps = [f"(no se pudo listar: {e})"]
    log(f"REGLA 11 — procesos python vivos ({len(ps)}), este es pid {os.getpid()}:")
    for l in ps:
        log(f"    {l[:160]}")
    V = {}
    with mp.Pool(N_PARALELO) as pool:
        ctrl = ([('K', 'v11', e, s) for e in ESC_ID for s in (1, 2, 3)]
                + [('K', 'v9g', e, s) for e in ('px0', 'azar') for s in (1, 2, 3)]
                + [('KT1', a, s) for a in ARMS_T for s in (1, 2, 3)])
        log(f"ETAPA 1/4 — identidades ({len(ctrl)})...")
        rc = pool.map(tarea, ctrl, chunksize=1)
        for t, cual, nombre in (('K', 'v11', "v11g(mundo='AB') == v11"), ('K', 'v9g', 'v11g(F,F) == v9g (mundo de regla)'),
                                ('KT1', None, 'mundo_temporal_v11(F,F) == v9')):
            g = [x for x in rc if x['tipo'] == t and (cual is None or x.get('cual') == cual)]
            log(f"  {nombre:34s}: {sum(x['identico'] for x in g)}/{len(g)}")
            for x in g:
                if not x['identico']:
                    log(f"      DIFIERE {x['esc']} s{x['seed']}: {x['difieren']}")
        V['K_identidad'] = all(x['identico'] for x in rc)
        if not V['K_identidad']:
            log("*** IDENTIDAD FALLIDA: se para."); sys.exit(1)
        trabajos = ([('G', b, rg, s) for b in BRAZOS for rg in REGLAS for s in SEEDS]
                    + [('T', b, a, s) for b in ('v9', 'v11') for a in ARMS_T for s in SEEDS])
        log(f"ETAPA 2/4 — {len(trabajos)} corridas (G: 3 brazos x 3 reglas x 20, T=200k; 3T: 2 x 6 x 20)...")
        res = []
        for i, r in enumerate(pool.imap_unordered(tarea, trabajos, chunksize=1), 1):
            res.append(r)
            if i % 20 == 0 or i == len(trabajos):
                log(f"          {i}/{len(trabajos)}")
    log("ETAPA 3/4 — analisis.")
    GG = lambda b, rg: {r['seed']: r for r in res if r['tipo'] == 'G' and r['brazo'] == b and r['regla'] == rg}
    VR = {rg: {s: valencia(rg, s) for s in SEEDS} for rg in REGLAS}
    cob = sum(sum(v is not None for v in GG('v11', 'px0')[s]['primer'].values()) >= 6 for s in SEEDS)
    V['K_cobertura'] = cob >= 18
    log(); log(f"  BLOQUE G (Etapa 3, mundo de regla)   cobertura del primer encuentro (v11, px0): {cob}/20 (>=18)")
    acc = {b: {rg: {s: acc_signo(GG(b, rg)[s], VR[rg][s]) for s in SEEDS} for rg in REGLAS} for b in BRAZOS}
    ba = {b: {rg: {s: ba_pb(GG(b, rg)[s], VR[rg][s]) for s in SEEDS} for rg in REGLAS} for b in BRAZOS}
    for b in BRAZOS:
        for rg in REGLAS:
            a = list(acc[b][rg].values()); bb = [x for x in ba[b][rg].values() if x is not None]
            log(f"   {b:4s} {rg:5s} valor {med(a)[0]:.3f} [{med(a)[1]:.3f}, {med(a)[2]:.3f}]   conducta BA_pb "
                f"{med(bb)[0]:.3f} [{med(bb)[1]:.3f}, {med(bb)[2]:.3f}]   divisiones {np.median([GG(b, rg)[s]['splits'] for s in SEEDS]):.0f}"
                f"  celdas {np.median([GG(b, rg)[s]['celdas'] for s in SEEDS]):.0f}  muertes {np.median([GG(b, rg)[s]['deaths'] for s in SEEDS]):.0f}")
    mpx = float(np.median(list(acc['v11']['px0'].values()))); maz = float(np.median(list(acc['v11']['azar'].values())))
    par1 = sum(acc['v11']['px0'][s] > acc['v11']['azar'][s] for s in SEEDS)
    V['G1'] = mpx >= 0.65 and 0.35 <= maz <= 0.65 and par1 >= 14
    bpx = [x for x in ba['v11']['px0'].values() if x is not None]; baz = [x for x in ba['v11']['azar'].values() if x is not None]
    par2 = sum(1 for s in SEEDS if ba['v11']['px0'][s] is not None and ba['v11']['azar'][s] is not None and ba['v11']['px0'][s] > ba['v11']['azar'][s])
    V['G2'] = bool(bpx) and bool(baz) and float(np.median(bpx)) >= 0.55 and 0.42 <= float(np.median(baz)) <= 0.58 and par2 >= 14
    mxo = float(np.median(list(acc['v11']['xor01'].values()))); par3 = sum(acc['v11']['xor01'][s] < acc['v11']['px0'][s] for s in SEEDS)
    V['G3_sin_voto'] = mxo <= 0.60 and par3 >= 14
    a9 = float(np.median(list(acc['v9']['px0'].values()))); b9 = float(np.median([x for x in ba['v9']['px0'].values() if x is not None]))
    V['G4_no_inferioridad'] = mpx >= a9 - 0.05 and float(np.median(bpx)) >= b9 - 0.03
    log(f"  G1 valor: px0 {mpx:.3f} (>=0.65), azar {maz:.3f} (en [0.35,0.65]), px0>azar {par1}/20 (>=14): {'SOSTENIDA' if V['G1'] else 'REFUTADA'}")
    log(f"  G2 conducta 1er encuentro: px0 {np.median(bpx):.3f} (>=0.55), azar {np.median(baz):.3f} (en [0.42,0.58]), px0>azar {par2}/20 (>=14): "
        f"{'SOSTENIDA' if V['G2'] else 'REFUTADA'}")
    log(f"  G3 frontera XOR (sin voto): xor {mxo:.3f} (<=0.60), xor<px0 {par3}/20 (>=14): {'SOSTENIDA' if V['G3_sin_voto'] else 'REFUTADA'}")
    log(f"  G4 no-inferioridad v11 vs v9: valor {mpx:.3f} vs {a9:.3f} (>= {a9-0.05:.3f}), conducta {np.median(bpx):.3f} vs {b9:.3f} "
        f"(>= {b9-0.03:.3f}): {'SOSTENIDA' if V['G4_no_inferioridad'] else 'REFUTADA'}")
    GT = lambda b, a: {r['seed']: r for r in res if r['tipo'] == 'T' and r['brazo'] == b and r['arm'] == a}
    log(); log("  BLOQUE T (3T, composicion temporal)")
    kt2 = sum(all(N(GT('v11', 'C1')[s][k]) == N(GT('v11', 'C2b')[s][k]) for k in ('W', 'sep', 'n_AB', 'n_AA', 'n_B', 'deaths', 'Rtot')) for s in SEEDS)
    V['KT2'] = kt2 == 20
    log(f"   KT2 C2b == C1 con la regla de v11: {kt2}/20")
    for b in ('v9', 'v11'):
        for a in ARMS_T:
            g = list(GT(b, a).values())
            log(f"   {b:4s} {a:4s} sep {med([r['sep'] for r in g])[0]:+.2f} [{med([r['sep'] for r in g])[1]:+.2f},{med([r['sep'] for r in g])[2]:+.2f}]"
                f"  lift_q4 {med([r['lift'][3] for r in g])[0]:+.3f}  solap_A {med([r['solap_A'] for r in g])[0]:.0f}"
                f"  divisiones {med([r['splits'] for r in g])[0]:.0f}  muertes {med([r['deaths'] for r in g])[0]:.0f}")
    c3 = list(GT('v11', 'C3').values()); c3c = list(GT('v11', 'C3C').values()); c3_9 = list(GT('v9', 'C3').values())
    V['T1'] = med([r['solap_A'] for r in c3])[0] <= 1 and sum(r['solap_A'] <= 1 for r in c3) >= 15
    V['T2'] = med([r['sep'] for r in c3])[0] >= 1.0
    V['T3'] = med([r['lift'][3] for r in c3])[0] >= 0.15
    V['T4'] = med([r['sep'] for r in c3c])[0] < 1.0 and med([r['lift'][3] for r in c3c])[0] < 0.15
    V['T5_no_inferioridad'] = med([r['sep'] for r in c3])[0] >= med([r['sep'] for r in c3_9])[0] - 1.0
    for k in ('T1', 'T2', 'T3', 'T4', 'T5_no_inferioridad'):
        log(f"   {k}: {'SOSTENIDA' if V[k] else 'REFUTADA'}")
    V['ETAPA3_SOBREVIVE'] = bool(V['K_identidad'] and V['K_cobertura'] and V['G1'] and V['G2'] and V['G4_no_inferioridad'])
    V['3T_SOBREVIVE'] = bool(V['K_identidad'] and V['KT2'] and V['T1'] and V['T2'] and V['T3'] and V['T4'] and V['T5_no_inferioridad'])
    log(); log("VEREDICTO v11_generaliza: " + " ".join(f"{k}={v}" for k, v in V.items()))
    log("ETAPA 4/4 — escritura.")
    meta = dict(fecha=time.strftime('%Y-%m-%dT%H:%M:%S'), semillas=SEEDS, veredictos=V, identidades=rc, shas=shas,
                procesos_python=ps, python=platform.python_version(), numpy=np.__version__)
    dj = os.path.join(RAIZ, 'datos', f'v11_generaliza_{stamp}.json')
    json.dump(dict(meta=meta, corridas=res), open(dj, 'w', encoding='utf-8'), ensure_ascii=False, default=str)
    log(f"datos -> {os.path.basename(dj)}  sha256_16 = {h16(dj)}")
    _log['f'].close()
