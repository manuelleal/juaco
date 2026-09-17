"""Capacidad de v11 en un mundo GRANDE (retina 10 px, 60 estimulos de peso 3). Ejecuta PREREGISTRO_capacidad_grande.md.
REGLA 10: log desde el arranque. REGLA 11: procesos vivos. Metricas identicas a 2K-bis (techo con TOL=0.3, M_max).
Precisiones escritas ANTES de correr:
- N_agot = 1 + t_agot/paso_t (estimulos presentes al agotarse el pool); censurado a n_est si no se agota.
- G3 usa N_agot censurado; una semilla que no agota cuenta como |N*-N_agot| = n_est - N*.
Uso:  python experimentos/capacidad_grande/corre_capacidad_grande.py
"""
import sys, os, json, time, hashlib, platform, subprocess
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
import numpy as np

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
sys.path[:0] = [AQUI, os.path.join(RAIZ, 'experimentos', 'v11_evo_division'), os.path.join(RAIZ, 'organismo'),
                os.path.join(RAIZ, 'experimentos', 'ramas', '2Kbis_capacidad')]
import mundo_grande as G

SEEDS = list(range(41, 61))
D_PIX, N_EST = 10, 60
PASOS = (20000, 60000)
BRAZOS = {'v9': dict(mu_norm=False, div_signo=False), 'v10': dict(mu_norm=True, div_signo=False), 'v11': dict(mu_norm=True, div_signo=True)}
N_PARALELO = 14
_log = {'f': None, 't0': time.time()}


def log(msg=""):
    linea = f"[{time.strftime('%H:%M:%S')} +{time.time()-_log['t0']:7.1f}s] {msg}"
    print(linea, flush=True)
    if _log['f']:
        _log['f'].write(linea + "\n"); _log['f'].flush(); os.fsync(_log['f'].fileno())


def h16(p):
    return hashlib.sha256(open(p, 'rb').read()).hexdigest()[:16]


def tarea(args):
    brazo, pt, seed = args
    import organismo_capD as o
    nom, pats, val, R = G.mundo(D_PIX, N_EST)
    r = o.run(seed, T=G.T_de(pt, N_EST), plan=G.plan_de(pt, nom, val), pats=pats, chk=G.chks(pt, N_EST),
              plast=True, lam=0.05, memoria_rechazo=20, **BRAZOS[brazo])
    for h in r['hist']:
        h['dev'] = {k: round(abs(v - R[k]), 3) for k, v in h['W'].items()}
    hist = [dict(t=h['t'], n=h['n'], celdas=h['celdas'], splits=h['splits'], dev=h['dev'], solap_medio=h['solap_medio']) for h in r['hist']]
    return dict(brazo=brazo, pt=pt, seed=seed, hist=hist, deaths=r['deaths'], t_agot=r['t_agot'], splits=r['splits'],
                celdas=r['celdas'], W_fin={k: round(float(v), 4) for k, v in r['W'].items()})


def med(xs):
    return float(np.median(xs)), float(min(xs)), float(max(xs))


if __name__ == '__main__':
    import multiprocessing as mp
    mp.set_start_method('spawn', force=True)
    stamp = time.strftime('%Y%m%d_%H%M%S')
    _log['f'] = open(os.path.join(RAIZ, 'datos', f'capacidad_grande_{stamp}.log'), 'w', encoding='utf-8', newline='\n')
    pre = os.path.join(AQUI, 'PREREGISTRO_capacidad_grande.md')
    shas = {n: h16(p) for n, p in [('preregistro', pre), ('script', os.path.abspath(__file__)),
            ('capD', os.path.join(AQUI, 'organismo_capD.py')), ('mundo_grande', os.path.join(AQUI, 'mundo_grande.py')),
            ('caph11', os.path.join(RAIZ, 'experimentos', 'v11_evo_division', 'organismo_caph11.py')),
            ('v11', os.path.join(RAIZ, 'organismo', 'organismo_v11.py'))]}
    log(f"ARRANQUE capacidad grande: retina {D_PIX} px, {N_EST} estimulos de peso 3, semillas {SEEDS[0]}..{SEEDS[-1]}, pasos {PASOS}. Pool({N_PARALELO}).")
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
    trabajos = [(b, pt, s) for pt in sorted(PASOS, reverse=True) for b in BRAZOS for s in SEEDS]
    log(f"ETAPA 1/3 — {len(trabajos)} corridas (primero las de {max(PASOS)//1000}k, {G.T_de(max(PASOS), N_EST)//1000}k pasos cada una)...")
    res = []
    with mp.Pool(N_PARALELO) as pool:
        for i, r in enumerate(pool.imap_unordered(tarea, trabajos, chunksize=1), 1):
            res.append(r)
            if i % 6 == 0 or i == len(trabajos):
                log(f"          {i}/{len(trabajos)}")
    log("ETAPA 2/3 — analisis.")
    Gg = lambda b, pt: {r['seed']: r for r in res if r['brazo'] == b and r['pt'] == pt}
    N_agot = lambda r, pt: (1 + r['t_agot'] // pt) if r['t_agot'] is not None else N_EST
    tab = {}
    for pt in PASOS:
        log(); log(f"  paso {pt//1000}k (T = {G.T_de(pt, N_EST)} pasos)")
        for b in BRAZOS:
            g = Gg(b, pt)
            Ns = [G.techo(g[s]['hist']) for s in SEEDS]; Ms = [G.m_max(g[s]['hist']) for s in SEEDS]
            Na = [N_agot(g[s], pt) for s in SEEDS]; agot = sum(g[s]['t_agot'] is not None for s in SEEDS)
            tab[(b, pt)] = dict(N=med(Ns)[0], M=med(Ms)[0], Na=med(Na)[0], agot=agot, Ns=Ns, Na_l=Na)
            log(f"   {b:4s}: N* {med(Ns)[0]:.1f} [{med(Ns)[1]:.0f},{med(Ns)[2]:.0f}]  M_max {med(Ms)[0]:.1f} [{med(Ms)[1]:.0f},{med(Ms)[2]:.0f}]"
                f"  N_agot {med(Na)[0]:.1f}  agotan {agot}/20  celdas {med([g[s]['celdas'] for s in SEEDS])[0]:.0f}"
                f"  divisiones {med([g[s]['splits'] for s in SEEDS])[0]:.0f}  muertes {med([g[s]['deaths'] for s in SEEDS])[0]:.0f}")
    V = {}
    V['G1'] = all(tab[('v11', pt)]['N'] >= 20 for pt in PASOS)
    V['G2'] = all(tab[('v11', pt)]['N'] - tab[('v10', pt)]['N'] >= 5 for pt in PASOS)
    cerca = {pt: sum(abs(tab[('v11', pt)]['Ns'][i] - tab[('v11', pt)]['Na_l'][i]) <= 5 for i in range(len(SEEDS))) for pt in PASOS}
    lejos = {pt: sum(tab[('v10', pt)]['Ns'][i] <= tab[('v10', pt)]['Na_l'][i] - 5 for i in range(len(SEEDS))) for pt in PASOS}
    V['G3'] = all(cerca[pt] >= 14 and lejos[pt] >= 14 for pt in PASOS)
    log()
    g1_txt = " y ".join(f"{tab[('v11', pt)]['N']:.1f}" for pt in PASOS)
    log(f"  G1 mediana N*(v11) >= 20 en los dos pasos: {g1_txt} -> {'SOSTENIDA' if V['G1'] else 'REFUTADA'}")
    log(f"  G2 N*(v11) - N*(v10) >= +5: " + ", ".join(f"{pt//1000}k {tab[('v11', pt)]['N'] - tab[('v10', pt)]['N']:+.1f}" for pt in PASOS)
        + f" -> {'SOSTENIDA' if V['G2'] else 'REFUTADA'}")
    log(f"  G3 el limite de v11 lo pone el POOL: |N*-N_agot|<=5 en " + ", ".join(f"{pt//1000}k {cerca[pt]}/20" for pt in PASOS)
        + "; v10 lejos de su pool en " + ", ".join(f"{pt//1000}k {lejos[pt]}/20" for pt in PASOS) + f" (>=14) -> {'SOSTENIDA' if V['G3'] else 'REFUTADA'}")
    log(); log("VEREDICTO capacidad_grande: " + " ".join(f"{k}={v}" for k, v in V.items()))
    log("ETAPA 3/3 — escritura.")
    meta = dict(fecha=time.strftime('%Y-%m-%dT%H:%M:%S'), D_pix=D_PIX, n_est=N_EST, pasos=list(PASOS), semillas=SEEDS,
                veredictos=V, shas=shas, procesos_python=ps, python=platform.python_version(), numpy=np.__version__)
    dj = os.path.join(RAIZ, 'datos', f'capacidad_grande_{stamp}.json')
    json.dump(dict(meta=meta, corridas=res), open(dj, 'w', encoding='utf-8'), ensure_ascii=False, default=str)
    log(f"datos -> {os.path.basename(dj)}  sha256_16 = {h16(dj)}")
    _log['f'].close()
