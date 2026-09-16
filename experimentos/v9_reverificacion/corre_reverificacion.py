"""Re-verificacion sobre v9: 3T (bloque T) y 2K-bis (bloque K). Ejecuta PREREGISTRO_reverificacion_v9.md (2708cb73ab8531e8).

REGLA 10: log con marca de tiempo desde el arranque (datos/reverificacion_v9_<fecha>.log). REGLA 11: procesos vivos.
Igualdades NUMERICAS (ida y vuelta JSON + ==).
Precisiones escritas ANTES de correr:
- KK1 compara caph9(lam=0.05, memoria_rechazo=0) con caph(lam=0.05), plast=True, en todas las claves de caph.
- M_max por semilla = maximo sobre checkpoints del numero de estimulos vivos con |W-R| <= 0.3 (como en coste_techo).
- W=0 exacto (K1) sobre el checkpoint final (t=T), |W| < 0.0005, 20 estimulos x 20 semillas.

Uso:  python experimentos/v9_reverificacion/corre_reverificacion.py
"""
import sys, os, json, time, hashlib, platform, csv, subprocess
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
import numpy as np

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
CAPDIR = os.path.join(RAIZ, 'experimentos', 'ramas', '2Kbis_capacidad')
sys.path[:0] = [AQUI, os.path.join(RAIZ, 'experimentos', '3T_confirmatorio'), os.path.join(RAIZ, 'experimentos', 'bug01'),
                CAPDIR, os.path.join(RAIZ, 'experimentos', 'ramas', '3T_temporal')]
SEEDS = list(range(1, 21))
ARMS = ['C1', 'C1p', 'C2', 'C2b', 'C3', 'C3C']
PLAN0 = [(0, 'A', 'comida'), (0, 'B', 'veneno')]
ESC_CAP = {'E1': dict(plan=PLAN0), 'C_veneno_50k': dict(plan=PLAN0 + [(50000, 'C', 'veneno')]),
           'D_comida_50k': dict(plan=PLAN0 + [(50000, 'D', 'comida')])}
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
    if tipo == 'KT1':
        _, arm, seed = args
        import mundo_temporal_v8 as m8, mundo_temporal_v9 as m9
        a, b = m8.run(seed, arm), m9.run(seed, arm, memoria_rechazo=0)
        return dict(tipo=tipo, arm=arm, seed=seed, identico=all(N(a[k]) == N(b[k]) for k in a),
                    difieren=[k for k in a if N(a[k]) != N(b[k])])
    if tipo == 'T':
        _, arm, seed = args
        import mundo_temporal_v9 as m9
        r = m9.run(seed, arm)
        return dict(tipo=tipo, arm=arm, seed=seed, W=r['W'], sep=r['sep'], solap_A=r['solap_A'], lift=r['lift'],
                    splits=r['splits'], split_t=r['split_t'], celdas=r['celdas'], n_AB=r['n_AB'], n_AA=r['n_AA'],
                    n_B=r['n_B'], deaths=r['deaths'], Rtot=r['Rtot'], t_techo=r['t_techo'])
    if tipo == 'KK1':
        _, esc, seed = args
        import organismo_caph as a_, organismo_caph9 as b_, parte2_capacidad as P
        kw = (dict(T=P.T_de(20000, 6), plan=P.plan_de(20000, 6), pats=P.PATS, chk=P.chks(20000, 6)) if esc == 'corto6'
              else ESC_CAP[esc])
        a, b = a_.run(seed, lam=0.05, **kw), b_.run(seed, lam=0.05, memoria_rechazo=0, **kw)
        return dict(tipo=tipo, esc=esc, seed=seed, identico=all(N(a[k]) == N(b[k]) for k in a),
                    difieren=[k for k in a if N(a[k]) != N(b[k])])
    _, pt, mem, seed = args
    import organismo_caph9 as o, parte2_capacidad as P
    r = o.run(seed, T=P.T_de(pt), plan=P.plan_de(pt), pats=P.PATS, chk=P.chks(pt), plast=True, lam=0.05, memoria_rechazo=mem)
    for h in r['hist']:
        h['dev'] = {k: round(abs(v - P.R[k]), 3) for k, v in h['W'].items()}
    return dict(tipo='K', pt=pt, mem=mem, seed=seed, hist=r['hist'], deaths=r['deaths'], t_agot=r['t_agot'],
                splits=r['splits'], celdas=r['celdas'], t_techo=r['t_techo'])


def techo_n(hist):
    import parte2_capacidad as P
    return P.techo(hist)


def m_max(hist):
    return max(sum(1 for v in h['dev'].values() if v <= 0.3) for h in hist)


def med(xs):
    return float(np.median(xs)), float(min(xs)), float(max(xs))


if __name__ == '__main__':
    import multiprocessing as mp
    mp.set_start_method('spawn', force=True)
    stamp = time.strftime('%Y%m%d_%H%M%S')
    _log['f'] = open(os.path.join(RAIZ, 'datos', f'reverificacion_v9_{stamp}.log'), 'w', encoding='utf-8', newline='\n')
    pre = os.path.join(AQUI, 'PREREGISTRO_reverificacion_v9.md')
    log(f"ARRANQUE re-verificacion sobre v9 (3T y 2K-bis). Pool({N_PARALELO}).")
    log(f"sha preregistro {h16(pre)}  script {h16(os.path.abspath(__file__))}  mundo_v9 {h16(os.path.join(AQUI, 'mundo_temporal_v9.py'))}"
        f"  caph9 {h16(os.path.join(AQUI, 'organismo_caph9.py'))}")
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
        ctrl = [('KT1', a, s) for a in ARMS for s in range(1, 4)] + [('KK1', e, s) for e in list(ESC_CAP) + ['corto6'] for s in range(1, 4)]
        log(f"ETAPA 1/4 — controles de identidad ({len(ctrl)})...")
        rc = pool.map(tarea, ctrl, chunksize=1)
        for t in ('KT1', 'KK1'):
            g = [x for x in rc if x['tipo'] == t]
            V[t] = all(x['identico'] for x in g)
            log(f"  {t}: {sum(x['identico'] for x in g)}/{len(g)} -> {'OK' if V[t] else 'FALLA'}")
            for x in g:
                if not x['identico']:
                    log(f"      DIFIERE {x}")
        if not (V['KT1'] and V['KK1']):
            log("*** control de identidad FALLIDO: se para."); sys.exit(1)

        trabajos = ([('K', pt, mem, s) for pt in (60000, 20000) for mem in (0, 20) for s in SEEDS]
                    + [('T', a, s) for a in ARMS for s in SEEDS])
        log(f"ETAPA 2/4 — {len(trabajos)} corridas (K: 80 largas primero; T: 120)...")
        res = []
        for i, r in enumerate(pool.imap_unordered(tarea, trabajos, chunksize=1), 1):
            res.append(r)
            if i % 20 == 0 or i == len(trabajos):
                log(f"          {i}/{len(trabajos)}")

    log("ETAPA 3/4 — analisis.")
    # ---------- bloque T ----------
    GT = lambda a: {r['seed']: r for r in res if r['tipo'] == 'T' and r['arm'] == a}
    c1, c2b = GT('C1'), GT('C2b')
    kt2 = sum(all(N(c1[s][k]) == N(c2b[s][k]) for k in ('W', 'sep', 'n_AB', 'n_AA', 'n_B', 'deaths', 'Rtot')) for s in SEEDS)
    V['KT2'] = kt2 == 20
    log(); log(f"  BLOQUE T (3T sobre v9)   KT2 C2b==C1: {kt2}/20")
    for a in ARMS:
        g = list(GT(a).values())
        log(f"   {a:4s} sep {med([r['sep'] for r in g])[0]:+.2f} [{med([r['sep'] for r in g])[1]:+.2f},{med([r['sep'] for r in g])[2]:+.2f}]"
            f"  lift_q4 {med([r['lift'][3] for r in g])[0]:+.3f}  solap_A {med([r['solap_A'] for r in g])[0]:.0f}"
            f"  splits {med([r['splits'] for r in g])[0]:.0f}  celdas90 {sum(r['celdas'] == 90 for r in g)}/20  muertes {med([r['deaths'] for r in g])[0]:.0f}"
            f"  truncan {sum(r['t_techo'] is not None for r in g)}/20")
    c3, c3c = list(GT('C3').values()), list(GT('C3C').values())
    V['T1'] = med([r['solap_A'] for r in c3])[0] <= 1 and sum(r['solap_A'] <= 1 for r in c3) >= 15
    V['T2'] = med([r['sep'] for r in c3])[0] >= 1.0
    V['T3'] = med([r['lift'][3] for r in c3])[0] >= 0.15
    V['T4'] = med([r['sep'] for r in c3c])[0] < 1.0 and med([r['lift'][3] for r in c3c])[0] < 0.15
    for k in ('T1', 'T2', 'T3', 'T4'):
        log(f"   {k}: {'SOSTENIDA' if V[k] else 'REFUTADA'}")

    # ---------- bloque K ----------
    GK = lambda pt, mem: {r['seed']: r for r in res if r['tipo'] == 'K' and r['pt'] == pt and r['mem'] == mem}
    ct = json.load(open(os.path.join(RAIZ, 'datos', 'coste_techo_20260916_142116.json'), encoding='utf-8'))['bloque_C']
    viejo = {r['seed']: r for r in ct if r['cond'] == 'C_T20' and r['lam'] == 0.05}
    kk2 = sum(techo_n(GK(20000, 0)[s]['hist']) == techo_n(viejo[s]['hist']) and m_max(GK(20000, 0)[s]['hist']) == m_max(viejo[s]['hist'])
              for s in SEEDS)
    V['KK2'] = kk2 == 20
    log(); log(f"  BLOQUE K (2K-bis sobre v9)   KK2 reproduce N* y M_max de coste_techo (v8, 20k): {kk2}/20")
    tab = {}
    for pt in (20000, 60000):
        for mem in (0, 20):
            g = GK(pt, mem)
            Ns = [techo_n(g[s]['hist']) for s in SEEDS]; Ms = [m_max(g[s]['hist']) for s in SEEDS]
            ceros = sum(1 for s in SEEDS for v in sorted(g[s]['hist'], key=lambda h: h['t'])[-1]['W'].values() if abs(v) < 0.0005)
            tab[(pt, mem)] = dict(N=med(Ns)[0], M=med(Ms)[0], ceros=ceros, Ns=Ns, Ms=Ms)
            log(f"   {pt//1000}k {'v9' if mem else 'v8'}: N* {med(Ns)[0]:.1f} [{med(Ns)[1]:.0f},{med(Ns)[2]:.0f}]  M_max {med(Ms)[0]:.1f} [{med(Ms)[1]:.0f},{med(Ms)[2]:.0f}]"
                f"  W=0 {ceros}/400  agotan {sum(g[s]['t_agot'] is not None for s in SEEDS)}/20  muertes {med([g[s]['deaths'] for s in SEEDS])[0]:.0f}"
                f"  splits {med([g[s]['splits'] for s in SEEDS])[0]:.0f}")
    V['K1'] = tab[(20000, 20)]['ceros'] <= 20
    V['K2'] = all(tab[(pt, 20)]['M'] >= tab[(pt, 0)]['M'] - 1 for pt in (20000, 60000))
    V['K3'] = all(tab[(pt, 20)]['N'] >= tab[(pt, 0)]['N'] - 1 for pt in (20000, 60000))
    for k in ('K1', 'K2', 'K3'):
        log(f"   {k}: {'SOSTENIDA' if V[k] else 'REFUTADA'}")
    for pt in (20000, 60000):
        dm = [tab[(pt, 20)]['Ms'][i] - tab[(pt, 0)]['Ms'][i] for i in range(20)]
        dd = [GK(pt, 20)[s]['deaths'] - GK(pt, 0)[s]['deaths'] for s in SEEDS]
        log(f"   (sin voto) {pt//1000}k pareado v9-v8: M_max mediana {np.median(dm):+.1f} (sube {sum(x>0 for x in dm)}, baja {sum(x<0 for x in dm)});"
            f" muertes mediana {np.median(dd):+.1f} (bajan {sum(x<0 for x in dd)})")

    V['T_SOBREVIVE'] = V['KT1'] and V['KT2'] and all(V[k] for k in ('T1', 'T2', 'T3', 'T4'))
    V['K_SOBREVIVE'] = V['KK1'] and V['KK2'] and all(V[k] for k in ('K1', 'K2', 'K3'))
    log(); log("VEREDICTO reverificacion_v9: " + " ".join(f"{k}={v}" for k, v in V.items()))
    log("ETAPA 4/4 — escritura.")
    meta = dict(fecha=time.strftime('%Y-%m-%dT%H:%M:%S'), semillas=SEEDS, veredictos=V, controles=rc,
                tabla_K={f"{pt}_{mem}": v for (pt, mem), v in tab.items()}, procesos_python=ps,
                sha_preregistro=h16(pre), sha_script=h16(os.path.abspath(__file__)),
                sha_constructor=h16(os.path.join(AQUI, 'construye_reverificacion.py')),
                sha_mundo_temporal_v9=h16(os.path.join(AQUI, 'mundo_temporal_v9.py')), sha_caph9=h16(os.path.join(AQUI, 'organismo_caph9.py')),
                python=platform.python_version(), numpy=np.__version__, plataforma=platform.platform())
    dj = os.path.join(RAIZ, 'datos', f'reverificacion_v9_{stamp}.json')
    json.dump(dict(meta=meta, corridas=res), open(dj, 'w', encoding='utf-8'), ensure_ascii=False, default=str)
    log(f"datos -> {os.path.basename(dj)}  sha256_16 = {h16(dj)}")
    _log['f'].close()
