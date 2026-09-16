"""v9 = v8 + memoria de trabajo de rechazo. CONFIRMATORIO en semillas nuevas 21-40. Ejecuta PREREGISTRO_v9.md.

REGLA 10: log con marca de tiempo desde el arranque (datos/v9_confirmatorio_<fecha>.log). REGLA 11: procesos vivos.

Precisiones de implementacion escritas ANTES de correr:
- Brazo v8 = organismo_v9.run(memoria_rechazo=0), que es v8 exacto por M0, para medir con la misma instrumentacion.
- Metricas en la 2a mitad = cuartos 3 y 4 (indices 2 y 3); porcentajes sobre 50.000 pasos.
- Comida en E1 = mordidas de A en cuartos 3-4. Criterios E1/E2 = los de bateria_v8.py.
- Igualdades NUMERICAS (ida y vuelta JSON + ==), leccion de ERR-13.

Uso:  python experimentos/v9_memoria_rechazo/corre_v9_confirmatorio.py
"""
import sys, os, json, time, hashlib, platform, csv, subprocess
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
import numpy as np

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
EXPL = os.path.join(os.path.dirname(RAIZ), 'exploracion', 'organos_20260916')
sys.path[:0] = [AQUI, os.path.join(RAIZ, 'organismo'), EXPL]
SEEDS = list(range(21, 41))
ESC = {'E1': dict(), 'E2': dict(invertir_en=50000)}
ESC_ID = {'BUG': dict(plast=False, solap_AB=3), 'E1': dict(), 'E2': dict(invertir_en=50000),
          'E2I': dict(nuevo='C'), 'E2J': dict(nuevo='D', nuevo_val='comida', solap_B=1),
          'E2K': dict(nuevo='D', nuevo_val='comida', solap_B=2), 'E2L': dict(solap_AB=3)}
BRAZOS = ['v8', 'v9', 'C1', 'C2']
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


def tarea_m0(args):
    cual, esc, seed = args
    import organismo_v8 as v8, organismo_v9 as v9, organismo_v9c as v9c
    if cual == 'v9_0_vs_v8':
        a, b = v8.run(seed, **ESC_ID[esc]), v9.run(seed, memoria_rechazo=0, **ESC_ID[esc]); claves = list(a)
    elif cual == 'v9c_vs_v9':
        a, b = v9.run(seed, **ESC[esc]), v9c.run(seed, memoria_modo='rechazado', **ESC[esc]); claves = list(a)
    else:
        import organismo_v8x as x
        a, b = x.run(seed, o3_tau=20, **ESC[esc]), v9.run(seed, **ESC[esc]); claves = ['W', 'mord', 'vis', 'deaths', 'splits']
    dif = [k for k in claves if N(a[k]) != N(b[k])]
    return dict(cual=cual, esc=esc, seed=seed, identico=not dif, difieren=dif)


def tarea(args):
    brazo, esc, seed = args
    import organismo_v9 as v9, organismo_v9c as v9c
    if brazo == 'v8':
        r = v9.run(seed, memoria_rechazo=0, **ESC[esc])
    elif brazo == 'v9':
        r = v9.run(seed, **ESC[esc])
    elif brazo == 'C1':
        r = v9c.run(seed, memoria_modo='azar', **ESC[esc])
    else:
        r = v9.run(seed, memoria_rechazo=1, **ESC[esc])
    return dict(brazo=brazo, esc=esc, seed=seed, W=r['W'], mord=r['mord'], deaths=r['deaths'], sobre=r['sobre'],
                llegadas=r['llegadas'], sin_objetivo=r['sin_objetivo'], splits=r['splits'])


pct_ven = lambda r: 100 * (r['sobre']['veneno'][2] + r['sobre']['veneno'][3]) / 50000
pct_com = lambda r: 100 * (r['sobre']['comida'][2] + r['sobre']['comida'][3]) / 50000
sin_obj = lambda r: 100 * (r['sin_objetivo'][2] + r['sin_objetivo'][3]) / 50000
comida_E1 = lambda r: r['mord']['A'][2] + r['mord']['A'][3]
crit_E1 = lambda r: r['mord']['B'][3] < r['mord']['B'][0] and abs(r['W']['A'] - 1) < .15 and abs(r['W']['B'] + 3) < .3
crit_E2 = lambda r: abs(r['W']['A'] + 3) < .3 and abs(r['W']['B'] - 1) < .15 and r['mord']['B'][3] >= 50


def med(xs):
    return float(np.median(xs)), float(min(xs)), float(max(xs))


if __name__ == '__main__':
    import multiprocessing as mp
    mp.set_start_method('spawn', force=True)
    stamp = time.strftime('%Y%m%d_%H%M%S')
    _log['f'] = open(os.path.join(RAIZ, 'datos', f'v9_confirmatorio_{stamp}.log'), 'w', encoding='utf-8', newline='\n')
    pre = os.path.join(AQUI, 'PREREGISTRO_v9.md')
    log(f"ARRANQUE v9 confirmatorio, semillas {SEEDS[0]}..{SEEDS[-1]}, brazos {BRAZOS}, Pool({N_PARALELO}).")
    log(f"sha preregistro {h16(pre)}  script {h16(os.path.abspath(__file__))}  v9 {h16(os.path.join(RAIZ, 'organismo', 'organismo_v9.py'))}"
        f"  v9c {h16(os.path.join(AQUI, 'organismo_v9c.py'))}  v8 {h16(os.path.join(RAIZ, 'organismo', 'organismo_v8.py'))}"
        f"  v8x {h16(os.path.join(EXPL, 'organismo_v8x.py'))}")
    try:
        ps = subprocess.run(['powershell', '-NoProfile', '-Command',
                             "Get-CimInstance Win32_Process | Where-Object { $_.Name -like 'python*' } | "
                             "ForEach-Object { \"$($_.ProcessId) $($_.CommandLine)\" }"],
                            capture_output=True, text=True, timeout=60).stdout.strip().splitlines()
    except Exception as e:
        ps = [f"(no se pudo listar: {e})"]
    log(f"REGLA 11 — procesos python vivos ({len(ps)}), este es pid {os.getpid()}:")
    for l in ps:
        log(f"    {l[:160]}")
    V = {}

    with mp.Pool(N_PARALELO) as pool:
        trabajos = ([('v9_0_vs_v8', e, s) for e in ESC_ID for s in range(1, 7)]
                    + [('v9c_vs_v9', e, s) for e in ESC for s in range(1, 4)]
                    + [('v9_vs_v8x', e, s) for e in ESC for s in range(1, 4)])
        log(f"ETAPA 1/4 — M0 identidades ({len(trabajos)} comparaciones)...")
        m0 = pool.map(tarea_m0, trabajos, chunksize=1)
        for c in ('v9_0_vs_v8', 'v9c_vs_v9', 'v9_vs_v8x'):
            g = [x for x in m0 if x['cual'] == c]
            log(f"  {c:12s}: {sum(x['identico'] for x in g)}/{len(g)}")
            for x in g:
                if not x['identico']:
                    log(f"      DIFIERE {x['esc']} s{x['seed']}: {x['difieren']}")
        V['M0'] = all(x['identico'] for x in m0)
        if not V['M0']:
            log("*** M0 FALLIDO: se para. No se corre nada mas."); sys.exit(1)

        trabajos = [(b, e, s) for b in BRAZOS for e in ESC for s in SEEDS]
        log(f"ETAPA 2/4 — {len(trabajos)} corridas...")
        res = []
        for i, r in enumerate(pool.imap_unordered(tarea, trabajos, chunksize=1), 1):
            res.append(r)
            if i % 40 == 0 or i == len(trabajos):
                log(f"          {i}/{len(trabajos)}")

    log("ETAPA 3/4 — analisis.")
    G = lambda b, e: {r['seed']: r for r in res if r['brazo'] == b and r['esc'] == e}
    log()
    for e in ESC:
        for b in BRAZOS:
            g = list(G(b, e).values())
            log(f"  {e} {b:3s} veneno {med([pct_ven(r) for r in g])[0]:6.2f}% [{med([pct_ven(r) for r in g])[1]:.2f},{med([pct_ven(r) for r in g])[2]:.2f}]"
                f"  comida-sobre {med([pct_com(r) for r in g])[0]:5.2f}%  sin_obj {med([sin_obj(r) for r in g])[0]:5.2f}%"
                f"  muertes {med([r['deaths'] for r in g])[0]:6.1f}  E1ok {sum(crit_E1(r) for r in g)}/20  E2ok {sum(crit_E2(r) for r in g)}/20"
                + (f"  comidaA 2a {med([comida_E1(r) for r in g])[0]:.1f}" if e == 'E1' else ""))

    # M1
    m1 = True; det1 = {}
    for e in ESC:
        a, v = G('v8', e), G('v9', e)
        mv8 = med([pct_ven(r) for r in a.values()])[0]; mv9 = med([pct_ven(r) for r in v.values()])[0]
        dif = [pct_ven(v[s]) - pct_ven(a[s]) for s in SEEDS]
        ok = 16 <= mv8 <= 24 and 8 <= mv9 <= 12 and sum(d <= -6 for d in dif) >= 18
        det1[e] = dict(v8=mv8, v9=mv9, bajan6=sum(d <= -6 for d in dif), mediana_dif=float(np.median(dif)))
        m1 &= ok
    V['M1'] = m1
    log(); log(f"  M1 efecto (v8 en [16,24], v9 en [8,12], -6pp en >=18/20, E1 y E2): {'SOSTENIDA' if m1 else 'REFUTADA'}  {det1}")
    # M2
    comb = [(G('v9', 'E1')[s]['deaths'] + G('v9', 'E2')[s]['deaths']) - (G('v8', 'E1')[s]['deaths'] + G('v8', 'E2')[s]['deaths']) for s in SEEDS]
    V['M2'] = float(np.median(comb)) < 0 and sum(c <= 0 for c in comb) >= 14
    log(f"  M2 muertes combinadas pareadas (mediana <0 y <=0 en >=14/20): {'SOSTENIDA' if V['M2'] else 'REFUTADA'}"
        f"  mediana {np.median(comb):+.1f}, <=0 en {sum(c <= 0 for c in comb)}/20")
    # M3
    dc = [comida_E1(G('v9', 'E1')[s]) - comida_E1(G('v8', 'E1')[s]) for s in SEEDS]
    V['M3'] = float(np.median(dc)) >= 0
    log(f"  M3 comida E1 2a mitad pareada (mediana >=0): {'SOSTENIDA' if V['M3'] else 'REFUTADA'}  mediana {np.median(dc):+.1f}")
    # M4
    so = {e: med([sin_obj(r) for r in G('v9', e).values()])[0] for e in ESC}
    V['M4'] = all(v < 5 for v in so.values())
    log(f"  M4 fallback (mediana <5%): {'SOSTENIDA' if V['M4'] else 'REFUTADA'}  {so}")
    # M5
    e1ok = sum(crit_E1(r) for r in G('v9', 'E1').values()); e2ok = sum(crit_E2(r) for r in G('v9', 'E2').values())
    V['M5'] = e1ok >= 18 and e2ok >= 18
    log(f"  M5 no-regresion v9 (E1 >=18/20, E2 >=18/20): {'SOSTENIDA' if V['M5'] else 'REFUTADA'}  E1 {e1ok}/20, E2 {e2ok}/20"
        f"  (v8: E1 {sum(crit_E1(r) for r in G('v8', 'E1').values())}/20, E2 {sum(crit_E2(r) for r in G('v8', 'E2').values())}/20)")
    # M6
    a = G('v8', 'E1')
    d_v9 = float(np.median([pct_ven(G('v9', 'E1')[s]) - pct_ven(a[s]) for s in SEEDS]))
    d_c1 = float(np.median([pct_ven(G('C1', 'E1')[s]) - pct_ven(a[s]) for s in SEEDS]))
    d_c2 = float(np.median([pct_ven(G('C2', 'E1')[s]) - pct_ven(a[s]) for s in SEEDS]))
    V['M6'] = d_c2 > -2 and d_c1 > -3 and (d_v9 <= d_c1 - 4)
    log(f"  M6 controles (C2 > -2pp; C1 > -3pp; v9 al menos 4pp mas bajo que C1): {'SOSTENIDA' if V['M6'] else 'REFUTADA'}"
        f"  v9 {d_v9:+.2f}, C1 {d_c1:+.2f}, C2 {d_c2:+.2f}")

    PASA = all(V[k] for k in ('M0', 'M1', 'M2', 'M3', 'M4', 'M5', 'M6'))
    V['PASA_CONFIRMATORIO'] = PASA
    log(); log("VEREDICTO v9_confirmatorio: " + " ".join(f"{k}={v}" for k, v in V.items()))

    log("ETAPA 4/4 — escritura.")
    meta = dict(fecha=time.strftime('%Y-%m-%dT%H:%M:%S'), semillas=SEEDS, brazos=BRAZOS, veredictos=V, M1=det1,
                muertes_combinadas_pareadas=comb, comida_E1_pareada=dc, M6=dict(v9=d_v9, C1=d_c1, C2=d_c2), M0=m0,
                procesos_python=ps, sha_preregistro=h16(pre), sha_script=h16(os.path.abspath(__file__)),
                sha_constructor=h16(os.path.join(AQUI, 'construye_v9.py')),
                sha_v9=h16(os.path.join(RAIZ, 'organismo', 'organismo_v9.py')), sha_v9c=h16(os.path.join(AQUI, 'organismo_v9c.py')),
                sha_v8=h16(os.path.join(RAIZ, 'organismo', 'organismo_v8.py')), sha_v8x=h16(os.path.join(EXPL, 'organismo_v8x.py')),
                python=platform.python_version(), numpy=np.__version__, plataforma=platform.platform())
    dj = os.path.join(RAIZ, 'datos', f'v9_confirmatorio_{stamp}.json')
    json.dump(dict(meta=meta, corridas=res), open(dj, 'w', encoding='utf-8'), ensure_ascii=False, default=str)
    dcsv = os.path.join(RAIZ, 'datos', f'v9_confirmatorio_{stamp}.csv')
    with open(dcsv, 'w', encoding='utf-8', newline='') as f:
        w = csv.writer(f); w.writerow(['brazo', 'esc', 'seed', 'pct_ven', 'pct_com', 'sin_obj', 'deaths', 'comidaA_2a', 'W_A', 'W_B', 'E1ok', 'E2ok'])
        for r in sorted(res, key=lambda r: (r['brazo'], r['esc'], r['seed'])):
            w.writerow([r['brazo'], r['esc'], r['seed'], round(pct_ven(r), 3), round(pct_com(r), 3), round(sin_obj(r), 3), r['deaths'],
                        comida_E1(r), r['W']['A'], r['W']['B'], crit_E1(r), crit_E2(r)])
    log(f"datos -> {os.path.basename(dj)}  sha256_16 = {h16(dj)}")
    log(f"         {os.path.basename(dcsv)}  sha256_16 = {h16(dcsv)}")
    _log['f'].close()
