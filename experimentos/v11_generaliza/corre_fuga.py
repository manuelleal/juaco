"""Confirmacion del diagnostico "generalizacion = interferencia" en 20 semillas. Ejecuta PREREGISTRO_fuga.md.
REGLA 10: log desde el arranque. Mismas corridas que la re-verificacion (regla px0, T=200k, semillas 41-60, tres brazos
con el mismo instrumento), guardando ademas codigos_f2 para medir la fuga.
Spearman = correlacion de Pearson sobre los rangos (empates promediados), calculada aqui sin scipy.
Uso:  python experimentos/v11_generaliza/corre_fuga.py
"""
import sys, os, json, time, hashlib, platform, subprocess
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
import numpy as np

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
sys.path[:0] = [AQUI, os.path.join(RAIZ, 'organismo')]
SEEDS = list(range(41, 61))
LIMPIAS = list(range(46, 61))
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


def rangos(x):
    x = np.asarray(x, float); orden = np.argsort(x, kind='mergesort'); r = np.empty(len(x), float)
    r[orden] = np.arange(1, len(x) + 1)
    for v in np.unique(x):   # empates: promedio
        m = x == v
        if m.sum() > 1:
            r[m] = r[m].mean()
    return r


def spearman(x, y):
    rx, ry = rangos(x), rangos(y)
    if rx.std() == 0 or ry.std() == 0:
        return float('nan')
    return float(np.corrcoef(rx, ry)[0, 1])


def tarea(args):
    brazo, seed = args
    import organismo_v11g as g
    r = g.run(seed, T=200000, mundo='regla', regla='px0', **BRAZOS[brazo])
    vr = g.split_regla(seed, 'px0')[3]
    cod, tren, test = r['codigos_f2'], r['tren'], r['test']
    fuga = float(np.mean([sum(i >= 30 for i in cod[k]) / 3 for k in test]))
    fuga_tren = float(np.mean([sum(i >= 30 for i in cod[k]) / 3 for k in tren]))
    cod_tren = set().union(*[set(cod[t]) for t in tren])
    comp = float(np.mean([len(set(cod[k]) & cod_tren) for k in test]))
    f = [1.0 if r['W_apriori'][k] > 0 else (0.5 if r['W_apriori'][k] == 0 else 0.0) for k in test if vr[k] == 'comida']
    p = [1.0 if r['W_apriori'][k] < 0 else (0.5 if r['W_apriori'][k] == 0 else 0.0) for k in test if vr[k] == 'veneno']
    acc = 0.5 * float(np.mean(f)) + 0.5 * float(np.mean(p))
    return dict(brazo=brazo, seed=seed, fuga=fuga, fuga_tren=fuga_tren, comp=comp, acc=acc,
                Wmag=float(np.median([abs(r['W_apriori'][k]) for k in test])), splits=r['splits'], celdas=r['celdas'])


if __name__ == '__main__':
    import multiprocessing as mp
    mp.set_start_method('spawn', force=True)
    stamp = time.strftime('%Y%m%d_%H%M%S')
    _log['f'] = open(os.path.join(RAIZ, 'datos', f'fuga_{stamp}.log'), 'w', encoding='utf-8', newline='\n')
    pre = os.path.join(AQUI, 'PREREGISTRO_fuga.md')
    shas = {'preregistro': h16(pre), 'script': h16(os.path.abspath(__file__)), 'v11g': h16(os.path.join(AQUI, 'organismo_v11g.py'))}
    log(f"ARRANQUE confirmacion de la fuga. semillas {SEEDS[0]}..{SEEDS[-1]} (limpias {LIMPIAS[0]}..{LIMPIAS[-1]}). Pool({N_PARALELO}).")
    log("sha " + "  ".join(f"{k} {v}" for k, v in shas.items()))
    try:
        ps = subprocess.run(['powershell', '-NoProfile', '-Command',
                             "Get-CimInstance Win32_Process | Where-Object { $_.Name -like 'python*' } | ForEach-Object { \"$($_.ProcessId) $($_.CommandLine)\" }"],
                            capture_output=True, text=True, timeout=60).stdout.strip().splitlines()
    except Exception as e:
        ps = [f"(no se pudo listar: {e})"]
    log(f"REGLA 11 — procesos python vivos ({len(ps)}), este es pid {os.getpid()}")
    trabajos = [(b, s) for b in BRAZOS for s in SEEDS]
    log(f"ETAPA 1/3 — {len(trabajos)} corridas (regla px0, T=200k)...")
    res = []
    with mp.Pool(N_PARALELO) as pool:
        for i, r in enumerate(pool.imap_unordered(tarea, trabajos, chunksize=1), 1):
            res.append(r)
            if i % 10 == 0 or i == len(trabajos):
                log(f"          {i}/{len(trabajos)}")
    log("ETAPA 2/3 — analisis.")
    G = lambda b, seeds=SEEDS: [r for r in res if r['brazo'] == b and r['seed'] in seeds]
    V = {}
    log()
    for b in BRAZOS:
        g = G(b)
        log(f"   {b:4s} fuga (hijas ajenas en el codigo de patrones NUEVOS, de 3) {np.median([x['fuga'] for x in g]):.2f}"
            f" [{min(x['fuga'] for x in g):.2f}, {max(x['fuga'] for x in g):.2f}]"
            f"  fuga en los ENTRENADOS {np.median([x['fuga_tren'] for x in g]):.2f}"
            f"  acierto {np.median([x['acc'] for x in g]):.3f}  |W| {np.median([x['Wmag'] for x in g]):.2f}"
            f"  compartidas {np.median([x['comp'] for x in g]):.2f}  divisiones {np.median([x['splits'] for x in g]):.0f}")
    f9 = float(np.median([x['fuga'] for x in G('v9')])); f11 = float(np.median([x['fuga'] for x in G('v11')]))
    V['D1'] = f9 >= 0.8 and f11 <= 0.3
    todas = res
    rho = spearman([x['fuga'] for x in todas], [x['acc'] for x in todas])
    V['D2'] = rho >= 0.5
    rho9 = spearman([x['fuga'] for x in G('v9')], [x['acc'] for x in G('v9')])
    rho10 = spearman([x['fuga'] for x in G('v10')], [x['acc'] for x in G('v10')])
    rho11 = spearman([x['fuga'] for x in G('v11')], [x['acc'] for x in G('v11')])
    V['D3'] = (rho9 >= 0.3) if rho9 == rho9 else False
    lim = [r for r in res if r['seed'] in LIMPIAS]
    f9l = float(np.median([x['fuga'] for x in G('v9', LIMPIAS)])); f11l = float(np.median([x['fuga'] for x in G('v11', LIMPIAS)]))
    rhol = spearman([x['fuga'] for x in lim], [x['acc'] for x in lim])
    V['D4'] = f9l >= 0.8 and f11l <= 0.3 and rhol >= 0.5
    log()
    log(f"  D1 fuga mediana v9 {f9:.2f} (>=0.8) y v11 {f11:.2f} (<=0.3): {'SOSTENIDA' if V['D1'] else 'REFUTADA'}")
    log(f"  D2 Spearman(fuga, acierto) sobre 60 corridas: {rho:+.3f} (>=+0.5): {'SOSTENIDA' if V['D2'] else 'REFUTADA'}")
    log(f"  D3 Spearman dentro de v9: {rho9:+.3f} (>=+0.3): {'SOSTENIDA' if V['D3'] else 'REFUTADA'}   [v10 {rho10:+.3f}, v11 {rho11:+.3f}, sin voto]")
    log(f"  D4 solo semillas limpias 46-60: fuga v9 {f9l:.2f}, v11 {f11l:.2f}, Spearman {rhol:+.3f}: {'SOSTENIDA' if V['D4'] else 'REFUTADA'}")
    V['FRASE_AL_HANDOFF'] = bool(V['D1'] and V['D2'] and V['D4'])
    log(); log("VEREDICTO fuga: " + " ".join(f"{k}={v}" for k, v in V.items()))
    log("ETAPA 3/3 — escritura.")
    meta = dict(fecha=time.strftime('%Y-%m-%dT%H:%M:%S'), semillas=SEEDS, limpias=LIMPIAS, veredictos=V, shas=shas,
                rho_total=rho, rho_v9=rho9, rho_v10=rho10, rho_v11=rho11, rho_limpias=rhol,
                procesos_python=ps, python=platform.python_version(), numpy=np.__version__)
    dj = os.path.join(RAIZ, 'datos', f'fuga_{stamp}.json')
    json.dump(dict(meta=meta, corridas=res), open(dj, 'w', encoding='utf-8'), ensure_ascii=False, default=str)
    log(f"datos -> {os.path.basename(dj)}  sha256_16 = {h16(dj)}")
    _log['f'].close()
