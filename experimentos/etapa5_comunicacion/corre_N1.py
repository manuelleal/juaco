"""Etapa 5, N1: senal innata honesta y aprendizaje vicario entre dos organismos v9. Ejecuta PREREGISTRO_N1.md (ed4c995020f9ff4a).

REGLA 10: log con marca de tiempo desde el arranque (datos/N1_<fecha>.log). REGLA 11: procesos vivos.
Precisiones escritas ANTES de correr:
- "Veneno propio hasta el criterio" de un organismo en E1 = n_crit['B']. Si nunca alcanza W_B <= -2.5 (censurado), se
  usa su total de mordidas propias de B en la corrida (cota conservadora) y se reporta cuantos censurados hay.
- S2 empareja organismo i de N1 con el organismo i de N0 de la misma semilla (mismo generador: mismo Kenyon y patas
  iniciales). Mejora = estrictamente menor.
- S4: t_ext_B censurado (nunca W_B >= 0 tras invertir) = T.
- Igualdades NUMERICAS (ida y vuelta JSON + ==).

Uso:  python experimentos/etapa5_comunicacion/corre_N1.py
"""
import sys, os, json, time, hashlib, platform, csv, subprocess
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
import numpy as np

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
sys.path[:0] = [AQUI, os.path.join(RAIZ, 'organismo')]
SEEDS = list(range(1, 21)); T = 100000
CONDS = {'SOLO': dict(n=1), 'N0': dict(n=2), 'N1': dict(n=2, senal='honesta'), 'BAR': dict(n=2, senal='barajada')}
MUNDOS = {'E1': dict(), 'E2': dict(invertir_en=50000)}
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
    import mundo_social as ms
    if tipo == 'K1':
        _, mundo, seed = args
        import organismo_v9 as v9
        a = v9.run(seed, **MUNDOS[mundo]); b = ms.run(seed, n=1, **MUNDOS[mundo])[0]
        claves = ['W', 'comp', 'mord', 'vis', 'deaths', 'splits', 'split_t', 'celdas']
        return dict(tipo=tipo, mundo=mundo, seed=seed, identico=all(N(a[k]) == N(b[k]) for k in claves),
                    difieren=[k for k in claves if N(a[k]) != N(b[k])])
    _, cond, mundo, seed = args
    out = ms.run(seed, T=T, **CONDS[cond], **MUNDOS[mundo])
    return dict(tipo='R', cond=cond, mundo=mundo, seed=seed, orgs=out)


def crit_B(o):
    return (o['n_crit']['B'], False) if 'B' in o['n_crit'] else (o['veneno_propio']['B'], True)


if __name__ == '__main__':
    import multiprocessing as mp
    mp.set_start_method('spawn', force=True)
    stamp = time.strftime('%Y%m%d_%H%M%S')
    _log['f'] = open(os.path.join(RAIZ, 'datos', f'N1_{stamp}.log'), 'w', encoding='utf-8', newline='\n')
    pre = os.path.join(AQUI, 'PREREGISTRO_N1.md')
    log(f"ARRANQUE Etapa 5 N1 (comunicacion). Pool({N_PARALELO}).")
    log(f"sha preregistro {h16(pre)}  script {h16(os.path.abspath(__file__))}  mundo_social {h16(os.path.join(AQUI, 'mundo_social.py'))}"
        f"  v9 {h16(os.path.join(RAIZ, 'organismo', 'organismo_v9.py'))}")
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
        k1 = pool.map(tarea, [('K1', m, s) for m in MUNDOS for s in range(1, 4)], chunksize=1)
        V['K1'] = all(x['identico'] for x in k1)
        log(f"ETAPA 1/3 — K1 mundo_social(n=1) == v9: {sum(x['identico'] for x in k1)}/{len(k1)} -> {'OK' if V['K1'] else 'FALLA'}")
        for x in k1:
            if not x['identico']:
                log(f"      DIFIERE {x}")
        if not V['K1']:
            log("*** K1 FALLIDO: se para."); sys.exit(1)
        trabajos = [('R', c, m, s) for c in CONDS for m in MUNDOS for s in SEEDS]
        log(f"ETAPA 2/3 — {len(trabajos)} corridas...")
        res = []
        for i, r in enumerate(pool.imap_unordered(tarea, trabajos, chunksize=1), 1):
            res.append(r)
            if i % 20 == 0 or i == len(trabajos):
                log(f"          {i}/{len(trabajos)}")

    log("ETAPA 3/3 — analisis.")
    G = lambda c, m: {r['seed']: r['orgs'] for r in res if r['cond'] == c and r['mundo'] == m}
    rec = {c: [sum(o['senales_recibidas'] for o in G(c, 'E1')[s]) for s in SEEDS] for c in ('N0', 'N1', 'BAR')}
    V['K2'] = all(x == 0 for x in rec['N0']) and all(x > 0 for x in rec['N1']) and all(x > 0 for x in rec['BAR'])
    mN1, mBAR = float(np.median(rec['N1'])), float(np.median(rec['BAR']))
    V['K3'] = mN1 > 0 and abs(mBAR - mN1) <= 0.5 * mN1
    log(f"  K2 senales recibidas (E1, por semilla): N0 max {max(rec['N0'])}; N1 mediana {mN1:.0f} (min {min(rec['N1'])}); BAR mediana {mBAR:.0f}"
        f" -> {'OK' if V['K2'] else 'FALLA'};  K3 BAR dentro de +-50% de N1: {'OK' if V['K3'] else 'FALLA'}")
    log()
    for m in MUNDOS:
        for c in CONDS:
            g = G(c, m)
            orgs = [o for s in SEEDS for o in g[s]]
            cb = [crit_B(o) for o in orgs]
            log(f"  {m} {c:4s}  veneno propio hasta criterio (B) mediana {np.median([x for x, _ in cb]):5.1f} (censurados {sum(z for _, z in cb)}/{len(cb)})"
                f"  veneno Q1 {np.median([o['mord']['B'][0] for o in orgs]):5.1f}  muertes/org {np.median([o['deaths'] for o in orgs]):6.1f}"
                f"  W_B {np.median([o['W']['B'] for o in orgs]):+.2f}  vicarias B {np.median([o['vicarias']['B'] for o in orgs]):5.0f}"
                + (f"  t_ext_B {np.median([o['t_ext_B'] if o['t_ext_B'] is not None else T for o in orgs]):.0f}" if m == 'E2' else ""))
    n0, n1, bar = G('N0', 'E1'), G('N1', 'E1'), G('BAR', 'E1')
    med_n0 = float(np.median([crit_B(o)[0] for s in SEEDS for o in n0[s]]))
    med_n1 = float(np.median([crit_B(o)[0] for s in SEEDS for o in n1[s]]))
    med_bar = float(np.median([crit_B(o)[0] for s in SEEDS for o in bar[s]]))
    V['S1'] = med_n1 <= 0.7 * med_n0
    ambos = sum(all(crit_B(n1[s][i])[0] < crit_B(n0[s][i])[0] for i in range(2)) for s in SEEDS)
    V['S2'] = ambos >= 15
    V['S3'] = med_bar >= med_n0
    e2n0, e2n1 = G('N0', 'E2'), G('N1', 'E2')
    te0 = float(np.median([o['t_ext_B'] if o['t_ext_B'] is not None else T for s in SEEDS for o in e2n0[s]]))
    te1 = float(np.median([o['t_ext_B'] if o['t_ext_B'] is not None else T for s in SEEDS for o in e2n1[s]]))
    V['S4_sin_voto'] = te1 < te0
    log()
    log(f"  S1 aprende del asco del otro: N1 {med_n1:.1f} <= 0.7 x N0 {med_n0:.1f} = {0.7*med_n0:.1f}: {'SOSTENIDA' if V['S1'] else 'REFUTADA'}")
    log(f"  S2 simbiosis (los dos mejoran frente a N0) en {ambos}/20 (>=15): {'SOSTENIDA' if V['S2'] else 'REFUTADA'}")
    log(f"  S3 contenido, no cantidad: BAR {med_bar:.1f} >= N0 {med_n0:.1f}: {'SOSTENIDA' if V['S3'] else 'REFUTADA'}")
    log(f"  S4 (sin voto) E2 extincion: t_ext_B N1 {te1:.0f} < N0 {te0:.0f}: {V['S4_sin_voto']}")
    V['N1_DEMOSTRADO'] = bool(V['K1'] and V['K2'] and V['K3'] and V['S1'] and V['S2'] and V['S3'])
    log(); log("VEREDICTO N1: " + " ".join(f"{k}={v}" for k, v in V.items()))

    meta = dict(fecha=time.strftime('%Y-%m-%dT%H:%M:%S'), semillas=SEEDS, veredictos=V, K1=k1, procesos_python=ps,
                sha_preregistro=h16(pre), sha_script=h16(os.path.abspath(__file__)), sha_mundo_social=h16(os.path.join(AQUI, 'mundo_social.py')),
                sha_v9=h16(os.path.join(RAIZ, 'organismo', 'organismo_v9.py')),
                python=platform.python_version(), numpy=np.__version__, plataforma=platform.platform())
    dj = os.path.join(RAIZ, 'datos', f'N1_{stamp}.json')
    json.dump(dict(meta=meta, corridas=res), open(dj, 'w', encoding='utf-8'), ensure_ascii=False, default=str)
    log(f"datos -> {os.path.basename(dj)}  sha256_16 = {h16(dj)}")
    _log['f'].close()
