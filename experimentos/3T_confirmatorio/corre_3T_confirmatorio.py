"""3T CONFIRMATORIO sobre el tronco v8. Ejecuta PREREGISTRO_3T_confirmatorio.md; no decide nada que no este alli.

REGLA 10: log con marca de tiempo desde el arranque en datos/3T_confirmatorio_<fecha>.log.
REGLA 11: lista los procesos python vivos al arrancar.

Precisiones de implementacion escritas ANTES de correr:
- E compara, por semilla y brazo (C3, C3C), las claves W, sep, lift, solap_A_q, splits, split_t, celdas,
  n_AB, n_AA, n_B, deaths, Rtot, SOLO en semillas donde t_techo es nulo en el brazo v8 Y en la referencia.
  Si no hay ninguna semilla elegible en un brazo, E es "no evaluable" en ese brazo y se reporta.
- K2 compara C2b con C1 bajo v8 en W, sep, n_AB, n_AA, n_B, deaths, Rtot.
- K3 compara la referencia recorrida hoy con PH3_20260915_115229.json en sep, splits y lift.
- "ultima division antes de t=25.000" usa split_t[-1][0]; sin divisiones no cuenta como cumplida.

Uso:  python experimentos/3T_confirmatorio/corre_3T_confirmatorio.py [semillas]
"""
import sys, os, json, time, hashlib, platform, csv, subprocess
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
import numpy as np

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
RAMA = os.path.join(RAIZ, 'experimentos', 'ramas', '3T_temporal')
sys.path[:0] = [AQUI, RAMA]

ARMS = ['C1', 'C1p', 'C2', 'C2b', 'C3', 'C3C']
REF_ARMS = ['C3', 'C3C']
REF_KW = dict(nkmax=90, wclip=30.0)
N_PARALELO = 14
_log = {'f': None, 't0': time.time()}


def log(msg=""):
    linea = f"[{time.strftime('%H:%M:%S')} +{time.time()-_log['t0']:7.1f}s] {msg}"
    print(linea, flush=True)
    if _log['f']:
        _log['f'].write(linea + "\n"); _log['f'].flush(); os.fsync(_log['f'].fileno())


def J(x):
    return json.dumps(x, sort_keys=True, default=str)


def h16(p):
    return hashlib.sha256(open(p, 'rb').read()).hexdigest()[:16]


def tarea_k1(args):
    arm, seed = args
    import mundo_temporal as mt, mundo_temporal_v8 as m8
    a, b = mt.run(seed, arm), m8.run(seed, arm, lam=0.0)
    dif = [k for k in a if J(a[k]) != J(b[k])]
    return dict(arm=arm, seed=seed, identico=not dif, difieren=dif)


def tarea(args):
    cual, arm, seed = args
    import mundo_temporal_v8 as m
    if cual == 'v8':
        r = m.run(seed, arm)                                   # lam=0.05, wclip=3.0, nkmax=90
    else:
        r = m.run(seed, arm, lam=0.0, **REF_KW)                # = mundo_temporal (K1) con wclip=30 (K3 contra PH3)
    r['cual'] = cual
    return r


def med(xs):
    xs = [x for x in xs if x is not None]
    return (float(np.median(xs)), float(min(xs)), float(max(xs))) if xs else (None, None, None)


def fm(t, d=2):
    return 'sin datos' if t[0] is None else f"{t[0]:+.{d}f} [{t[1]:+.{d}f}, {t[2]:+.{d}f}]"


if __name__ == '__main__':
    import multiprocessing as mp
    mp.set_start_method('spawn', force=True)
    S = int(sys.argv[1]) if len(sys.argv) > 1 else 20
    seeds = list(range(1, S + 1))
    stamp = time.strftime('%Y%m%d_%H%M%S')
    _log['f'] = open(os.path.join(RAIZ, 'datos', f'3T_confirmatorio_{stamp}.log'), 'w', encoding='utf-8', newline='\n')
    pre = os.path.join(AQUI, 'PREREGISTRO_3T_confirmatorio.md')
    log(f"ARRANQUE 3T confirmatorio sobre v8. {S} semillas, Pool({N_PARALELO}).")
    log(f"sha preregistro {h16(pre)}  script {h16(os.path.abspath(__file__))}  mundo_v8 {h16(os.path.join(AQUI, 'mundo_temporal_v8.py'))}"
        f"  mundo {h16(os.path.join(RAMA, 'mundo_temporal.py'))}  organismo_v8 {h16(os.path.join(RAIZ, 'organismo', 'organismo_v8.py'))}")
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

    with mp.Pool(N_PARALELO) as pool:
        trabajos = [(a, s) for a in ARMS for s in range(1, 4)]
        log(f"ETAPA 1/4 — K1: mundo_temporal_v8(lam=0) == mundo_temporal ({len(trabajos)} comparaciones)...")
        k1 = pool.map(tarea_k1, trabajos, chunksize=1)
        K1 = all(x['identico'] for x in k1)
        log(f"  K1: {sum(x['identico'] for x in k1)}/{len(k1)} -> {'OK' if K1 else 'FALLA'}")
        for x in k1:
            if not x['identico']:
                log(f"      DIFIERE {x['arm']} s{x['seed']}: {x['difieren']}")
        if not K1:
            log("*** K1 FALLIDO: el instrumento no es el mundo original con lam=0. No se corre nada mas.")
            sys.exit(1)

        trabajos = [('v8', a, s) for a in ARMS for s in seeds] + [('ref', a, s) for a in REF_ARMS for s in seeds]
        log(f"ETAPA 2/4 — {len(trabajos)} corridas (v8: 6 brazos; referencia PH3 wclip=30: C3, C3C)...")
        res = []
        for i, r in enumerate(pool.imap_unordered(tarea, trabajos, chunksize=1), 1):
            res.append(r)
            if i % 40 == 0 or i == len(trabajos):
                log(f"          {i}/{len(trabajos)}")

    log("ETAPA 3/4 — analisis.")
    G = lambda cual, arm: sorted([r for r in res if r['cual'] == cual and r['arm'] == arm], key=lambda r: r['seed'])
    V = dict(K1=K1)

    # K2
    c1, c2b = G('v8', 'C1'), G('v8', 'C2b')
    campos = ['W', 'sep', 'n_AB', 'n_AA', 'n_B', 'deaths', 'Rtot']
    k2 = sum(all(J(a[k]) == J(b[k]) for k in campos) for a, b in zip(c1, c2b))
    V['K2'] = k2 == S
    log(f"  K2 C2b == C1 bajo v8: {k2}/{S} -> {'OK' if V['K2'] else 'FALLA'}")

    # K3
    ph3 = json.load(open(os.path.join(RAMA, 'PH3_20260915_115229.json'), encoding='utf-8'))['corridas']
    k3 = {}
    for arm in REF_ARMS:
        viejo = {r['seed']: r for r in ph3 if r['arm'] == arm}
        k3[arm] = sum(viejo.get(r['seed']) is not None and all(J(r[k]) == J(viejo[r['seed']][k]) for k in ('sep', 'splits', 'lift'))
                      for r in G('ref', arm))
    V['K3'] = all(v == S for v in k3.values())
    log(f"  K3 referencia de hoy == PH3 guardado: {k3} -> {'OK' if V['K3'] else 'FALLA'}")

    # K4
    # ERR-13: igualdad NUMERICA (el texto JSON distingue 0.0 de -0.0, que son el mismo numero)
    k4 = sum(a['comp'] != b['comp'] for a, b in zip(G('v8', 'C3'), G('ref', 'C3')))
    V['K4'] = k4 == S
    log(f"  K4 el drenaje actua (comp C3 v8 != referencia): {k4}/{S} -> {'OK' if V['K4'] else 'FALLA'}")

    # E
    claves_E = ['W', 'sep', 'lift', 'solap_A_q', 'splits', 'split_t', 'celdas', 'n_AB', 'n_AA', 'n_B', 'deaths', 'Rtot']
    E_ok = True; E_det = {}
    for arm in REF_ARMS:
        eleg = [(a, b) for a, b in zip(G('v8', arm), G('ref', arm)) if a['t_techo'] is None and b['t_techo'] is None]
        # ERR-13: igualdad NUMERICA, que es lo que dice el preregistro ("W a 3 decimales"); 0.0 == -0.0
        dif = [(a['seed'], [k for k in claves_E if a[k] != b[k]]) for a, b in eleg]
        dif = [d for d in dif if d[1]]
        E_det[arm] = dict(elegibles=len(eleg), difieren=dif)
        if eleg:
            E_ok &= not dif
        log(f"  E {arm}: elegibles {len(eleg)}/{S}, identicas {len(eleg)-len(dif)}/{len(eleg)}"
            + (f"  DIFIEREN: {dif[:4]}" if dif else ""))
    V['E'] = E_ok and all(E_det[a]['elegibles'] > 0 for a in REF_ARMS)
    trunc = {arm: sum(r['t_techo'] is not None for r in G('v8', arm)) for arm in ARMS}
    trunc_ref = {arm: sum(r['t_techo'] is not None for r in G('ref', arm)) for arm in REF_ARMS}
    V['E_alcance'] = all(trunc[a] == 0 for a in ('C1p', 'C2', 'C3', 'C3C')) and (S - trunc_ref['C3']) >= 18
    log(f"  E-alcance: truncan v8 {trunc}; referencia (techo 30) {trunc_ref}"
        f" -> {'SOSTENIDA' if V['E_alcance'] else 'REFUTADA'}")
    if not V['E']:
        log("*** E REFUTADA o no evaluable: por el preregistro sec. 6 se para la lectura del veredicto.")

    # criterios
    log()
    for arm in ARMS:
        g = G('v8', arm)
        log(f"  {arm:4s} sep {fm(med([r['sep'] for r in g]))}  lift_q4 {fm(med([r['lift'][3] for r in g]),3)}  "
            f"solap_A {fm(med([r['solap_A'] for r in g]),0)}  splits {fm(med([r['splits'] for r in g]),0)}  "
            f"celdas90 {sum(r['celdas'] == 90 for r in g)}/{S}  muertes {fm(med([r['deaths'] for r in g]),0)}  "
            f"W_A|A {fm(med([r['W']['A|A'] for r in g]))}")
    c3, c3c = G('v8', 'C3'), G('v8', 'C3C')
    sA = med([r['solap_A'] for r in c3])[0]
    V['1_representacion'] = sA <= 1 and sum(r['solap_A'] <= 1 for r in c3) >= 15
    V['2_valor'] = med([r['sep'] for r in c3])[0] >= 1.0
    V['3_conducta'] = med([r['lift'][3] for r in c3])[0] >= 0.15
    V['4_no_artefacto'] = med([r['sep'] for r in c3c])[0] < 1.0 and med([r['lift'][3] for r in c3c])[0] < 0.15
    PH = dict(
        sep28=sum(r['sep'] >= 2.8 for r in c3), lift15=sum(r['lift'][3] >= 0.15 for r in c3),
        splits_med=med([r['splits'] for r in c3])[0],
        ultima25k=sum(bool(r['split_t']) and r['split_t'][-1][0] < 25000 for r in c3),
        c3c_agota=sum(r['celdas'] == 90 for r in c3c))
    V['PH_sep28'] = PH['sep28'] >= 18; V['PH_lift15'] = PH['lift15'] >= 18
    V['PH_se_detiene'] = PH['splits_med'] <= 30 and PH['ultima25k'] >= 15
    V['PH_C3C_agota'] = PH['c3c_agota'] >= 15
    log()
    for k in ('1_representacion', '2_valor', '3_conducta', '4_no_artefacto'):
        log(f"  criterio {k:18s}: {'CUMPLE' if V[k] else 'NO CUMPLE'}")
    log(f"  [PH] sep>=2.8 {PH['sep28']}/{S}; lift_q4>=0.15 {PH['lift15']}/{S}; splits mediana {PH['splits_med']}, "
        f"ultima <25k {PH['ultima25k']}/{S}; C3C agota pool {PH['c3c_agota']}/{S}")
    K = V['K1'] and V['K2'] and V['K3'] and V['K4']
    SI = bool(K and V['E'] and V['1_representacion'] and V['2_valor'] and V['3_conducta'] and V['4_no_artefacto'])
    V['VEREDICTO_SI'] = SI
    log()
    log(f"VEREDICTO 3T confirmatorio: {'SI' if SI else 'NO'}  | " + " ".join(f"{k}={v}" for k, v in V.items()))

    log("ETAPA 4/4 — escritura.")
    meta = dict(fecha=time.strftime('%Y-%m-%dT%H:%M:%S'), semillas=S, veredictos=V, E=E_det, PH=PH, K3=k3,
                truncan_v8=trunc, truncan_ref=trunc_ref, ref_kw=REF_KW, procesos_python=ps,
                sha_preregistro=h16(pre), sha_script=h16(os.path.abspath(__file__)),
                sha_constructor=h16(os.path.join(AQUI, 'construye_mundo_v8.py')),
                sha_mundo_temporal_v8=h16(os.path.join(AQUI, 'mundo_temporal_v8.py')),
                sha_mundo_temporal=h16(os.path.join(RAMA, 'mundo_temporal.py')),
                sha_organismo_v8=h16(os.path.join(RAIZ, 'organismo', 'organismo_v8.py')),
                python=platform.python_version(), numpy=np.__version__, plataforma=platform.platform())
    dj = os.path.join(RAIZ, 'datos', f'3T_confirmatorio_{stamp}.json')
    json.dump(dict(meta=meta, K1=k1, corridas=res), open(dj, 'w', encoding='utf-8'), ensure_ascii=False, default=str)
    dc = os.path.join(RAIZ, 'datos', f'3T_confirmatorio_{stamp}.csv')
    with open(dc, 'w', encoding='utf-8', newline='') as f:
        w = csv.writer(f)
        w.writerow(['cual', 'arm', 'seed', 'sep', 'W_AA', 'W_AB', 'solap_A', 'lift_q4', 'splits', 'celdas', 'deaths', 'Rtot', 't_techo'])
        for r in sorted(res, key=lambda r: (r['cual'], r['arm'], r['seed'])):
            w.writerow([r['cual'], r['arm'], r['seed'], r['sep'], r['W']['A|A'], r['W']['A|B'], r['solap_A'],
                        r['lift'][3], r['splits'], r['celdas'], r['deaths'], r['Rtot'], r['t_techo']])
    log(f"datos -> {os.path.basename(dj)}  sha256_16 = {h16(dj)}")
    log(f"         {os.path.basename(dc)}  sha256_16 = {h16(dc)}")
    _log['f'].close()
