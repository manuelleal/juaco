"""Etapa 5, N1-ASIMETRICO: experto (hereda el estado de un progenitor del tronco) y novato; senal de CONDUCTA.
Ejecuta PREREGISTRO_N1_asimetrico.md (19d500c6994a0ebb).

REGLA 10: log desde el arranque (datos/N1asim_<fecha>.log). REGLA 11: procesos vivos. Igualdades NUMERICAS.
Precisiones escritas ANTES de correr:
- BASE = organismo_v10 si esta en CONGELADOS de manifiesto.py, si no organismo_v9 (mundo_social usa mu_norm acorde).
- Progenitor del experto: mundo_social.run(seed, n=1, devolver_estado=True) en E1 (identico al tronco por K1), T=100000.
- Novato = organismo 0 (rng seed), experto = organismo 1 (rng seed+100000, estado heredado).
- PAR-BAR usa senal='barajada_conducta' (mismo numero de senales que 'conducta', signo al azar).
- n_crit censurado = total de mordidas propias de B. t_B_ok / t_ext_B censurados = T.
- K2: avisos '-' sobre B recibidos por el novato ANTES de su criterio (avisos_B_antes_crit) >= 5 en >=15/20.
Uso:  python experimentos/etapa5_comunicacion/corre_N1_asim.py
"""
import sys, os, json, time, hashlib, platform, subprocess, re
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
import numpy as np

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
sys.path[:0] = [AQUI, os.path.join(RAIZ, 'organismo')]
SEEDS = list(range(1, 21)); T = 100000
_man = open(os.path.join(RAIZ, 'manifiesto.py'), encoding='utf-8').read()
BASE = 'organismo_v13' if "'./organismo/organismo_v13.py'" in _man else 'organismo_v11'   # el tronco; mundo_social replica v13 por defecto
KW_BASE = dict() if BASE == 'organismo_v13' else dict(eta_s=0.0, puerta=None)
CONDS = {'NOV-SOLO': dict(n=1), 'PAR-N0': dict(n=2), 'PAR-N1': dict(n=2, senal='conducta'), 'PAR-BAR': dict(n=2, senal='barajada_conducta')}
MUNDOS = {'E1': dict(), 'INV': dict(invertir_en=0)}
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
        import importlib
        base = importlib.import_module(BASE)
        kw = dict() if mundo == 'E1' else dict(invertir_en=50000)
        a = base.run(seed, **kw); b = ms.run(seed, n=1, **KW_BASE, **kw)[0]
        claves = ['W', 'comp', 'mord', 'vis', 'deaths', 'splits', 'split_t', 'celdas']
        return dict(tipo=tipo, mundo=mundo, seed=seed, identico=all(N(a[k]) == N(b[k]) for k in claves), difieren=[k for k in claves if N(a[k]) != N(b[k])])
    if tipo == 'P':
        _, seed = args
        r = ms.run(seed, n=1, T=T, devolver_estado=True, **KW_BASE)[0]
        return dict(tipo=tipo, seed=seed, estado=r['estado'], W=r['W'])
    _, cond, mundo, seed, estado = args
    kw = CONDS[cond]
    estados = None if kw['n'] == 1 else [None, estado]
    out = ms.run(seed, T=T, estados=estados, **KW_BASE, **kw, **MUNDOS[mundo])
    for o in out:
        o.pop('estado', None)
    return dict(tipo='R', cond=cond, mundo=mundo, seed=seed, orgs=out)


def crit_B(o):
    return o['n_crit']['B'] if 'B' in o['n_crit'] else o['veneno_propio']['B']


if __name__ == '__main__':
    import multiprocessing as mp
    mp.set_start_method('spawn', force=True)
    stamp = time.strftime('%Y%m%d_%H%M%S')
    _log['f'] = open(os.path.join(RAIZ, 'datos', f'N1asim_{stamp}.log'), 'w', encoding='utf-8', newline='\n')
    pre = os.path.join(AQUI, 'PREREGISTRO_N1_asimetrico.md')
    log(f"ARRANQUE N1-asimetrico. BASE={BASE} (kw {KW_BASE}). Pool({N_PARALELO}).")
    log(f"sha preregistro {h16(pre)}  script {h16(os.path.abspath(__file__))}  mundo_social {h16(os.path.join(AQUI, 'mundo_social.py'))}"
        f"  base {h16(os.path.join(RAIZ, 'organismo', BASE + '.py'))}")
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
        k1 = pool.map(tarea, [('K1', m, s) for m in ('E1', 'E2') for s in range(1, 4)], chunksize=1)
        V['K1'] = all(x['identico'] for x in k1)
        log(f"ETAPA 1/4 — K1 mundo_social(n=1) == {BASE}: {sum(x['identico'] for x in k1)}/{len(k1)} -> {'OK' if V['K1'] else 'FALLA'}")
        for x in k1:
            if not x['identico']:
                log(f"      DIFIERE {x}")
        if not V['K1']:
            log("*** K1 FALLIDO: se para."); sys.exit(1)
        log("ETAPA 2/4 — progenitores del experto (20)...")
        prog = {r['seed']: r for r in pool.map(tarea, [('P', s) for s in SEEDS], chunksize=1)}
        log(f"  W progenitores: W_A mediana {np.median([prog[s]['W']['A'] for s in SEEDS]):+.2f}, W_B {np.median([prog[s]['W']['B'] for s in SEEDS]):+.2f}")
        trabajos = [('R', c, m, s, prog[s]['estado']) for c in CONDS for m in MUNDOS for s in SEEDS]
        log(f"ETAPA 3/4 — {len(trabajos)} corridas...")
        res = []
        for i, r in enumerate(pool.imap_unordered(tarea, trabajos, chunksize=1), 1):
            res.append(r)
            if i % 20 == 0 or i == len(trabajos):
                log(f"          {i}/{len(trabajos)}")
    log("ETAPA 4/4 — analisis.")
    G = lambda c, m: {r['seed']: r['orgs'] for r in res if r['cond'] == c and r['mundo'] == m}
    nov = lambda c, m: [G(c, m)[s][0] for s in SEEDS]
    exp = lambda c, m: [G(c, m)[s][1] for s in SEEDS]
    rec = {c: [G(c, 'E1')[s][0]['senales_recibidas'] for s in SEEDS] for c in ('PAR-N0', 'PAR-N1', 'PAR-BAR')}
    avisos = [o['avisos_B_antes_crit'] for o in nov('PAR-N1', 'E1')]
    V['K2'] = sum(a >= 5 for a in avisos) >= 15
    V['K3'] = abs(np.median(rec['PAR-BAR']) - np.median(rec['PAR-N1'])) <= 0.5 * np.median(rec['PAR-N1'])
    log(f"  K2 avisos '-' sobre B al novato antes de su criterio (PAR-N1, E1): mediana {np.median(avisos):.0f}, >=5 en {sum(a >= 5 for a in avisos)}/20 -> {'OK' if V['K2'] else 'NO EVALUABLE'}")
    log(f"  K3 senales recibidas por el novato: N0 {np.median(rec['PAR-N0']):.0f}, N1 {np.median(rec['PAR-N1']):.0f}, BAR {np.median(rec['PAR-BAR']):.0f} -> {'OK' if V['K3'] else 'FALLA'}")
    log()
    for m in MUNDOS:
        for c in CONDS:
            n_ = nov(c, m)
            lin = (f"  {m:3s} {c:8s} NOVATO: crit B {np.median([crit_B(o) for o in n_]):5.1f}  veneno Q1 {np.median([o['mord']['B' if m == 'E1' else 'A'][0] for o in n_]):5.1f}"
                   f"  muertes {np.median([o['deaths'] for o in n_]):6.1f}  W_B fin {np.median([o['W']['B'] for o in n_]):+.2f}"
                   f"  t_B_ok {np.median([o['t_B_ok'] if o['t_B_ok'] is not None else T for o in n_]):7.0f}")
            if CONDS[c]['n'] == 2:
                e_ = exp(c, m)
                lin += (f" | EXPERTO: W_B fin {np.median([o['W']['B'] for o in e_]):+.2f}  mordidas B {np.median([sum(o['mord']['B']) for o in e_]):4.0f}"
                        f"  muertes {np.median([o['deaths'] for o in e_]):6.1f}  t_ext_B {np.median([o['t_ext_B'] if o['t_ext_B'] is not None else T for o in e_]):7.0f}")
            log(lin)
    c0, c1, cb = [crit_B(o) for o in nov('PAR-N0', 'E1')], [crit_B(o) for o in nov('PAR-N1', 'E1')], [crit_B(o) for o in nov('PAR-BAR', 'E1')]
    V['A1'] = np.median(c1) <= 0.7 * np.median(c0)
    V['A2'] = sum(b < a for a, b in zip(c0, c1)) >= 15
    V['A3'] = np.median(cb) >= np.median(c0)
    V['A3b_sin_voto'] = sum(o['W']['B'] <= -2.5 for o in exp('PAR-N1', 'E1')) >= 18
    tb = lambda o: o['t_B_ok'] if o['t_B_ok'] is not None else T
    te = lambda o: o['t_ext_B'] if o['t_ext_B'] is not None else T
    a4 = sum(tb(b) > tb(a) for a, b in zip(nov('PAR-N0', 'INV'), nov('PAR-N1', 'INV')))
    a5 = sum(te(b) < te(a) for a, b in zip(exp('PAR-N0', 'INV'), exp('PAR-N1', 'INV')))
    V['A4'] = a4 >= 13; V['A5'] = a5 >= 13
    log()
    log(f"  A1 novato aprende del rechazo del experto: N1 {np.median(c1):.1f} <= 0.7 x N0 {np.median(c0):.1f} = {0.7*np.median(c0):.1f}: {'SOSTENIDA' if V['A1'] else 'REFUTADA'}")
    log(f"  A2 pareado N1<N0 en {sum(b < a for a, b in zip(c0, c1))}/20 (>=15): {'SOSTENIDA' if V['A2'] else 'REFUTADA'}")
    log(f"  A3 contenido: BAR {np.median(cb):.1f} >= N0 {np.median(c0):.1f}: {'SOSTENIDA' if V['A3'] else 'REFUTADA'}")
    log(f"  A3b (sin voto) el experto no se degrada en E1: {sum(o['W']['B'] <= -2.5 for o in exp('PAR-N1', 'E1'))}/20")
    log(f"  A4 INV coste de la confianza (novato N1 tarda mas) en {a4}/20 (>=13): {'SOSTENIDA' if V['A4'] else 'REFUTADA'}")
    log(f"  A5 INV simbiosis inversa (experto N1 extingue antes) en {a5}/20 (>=13): {'SOSTENIDA' if V['A5'] else 'REFUTADA'}")
    V['TRANSMISION'] = bool(V['K1'] and V['K2'] and V['K3'] and V['A1'] and V['A2'] and V['A3'])
    V['SIMBIOSIS'] = bool(V['TRANSMISION'] and V['A4'] and V['A5'])
    log(); log("VEREDICTO N1asim: " + " ".join(f"{k}={v}" for k, v in V.items()))
    meta = dict(fecha=time.strftime('%Y-%m-%dT%H:%M:%S'), base=BASE, semillas=SEEDS, veredictos=V, K1=k1, procesos_python=ps,
                sha_preregistro=h16(pre), sha_script=h16(os.path.abspath(__file__)), sha_mundo_social=h16(os.path.join(AQUI, 'mundo_social.py')),
                sha_base=h16(os.path.join(RAIZ, 'organismo', BASE + '.py')), python=platform.python_version(), numpy=np.__version__)
    dj = os.path.join(RAIZ, 'datos', f'N1asim_{stamp}.json')
    json.dump(dict(meta=meta, corridas=res), open(dj, 'w', encoding='utf-8'), ensure_ascii=False, default=str)
    log(f"datos -> {os.path.basename(dj)}  sha256_16 = {h16(dj)}")
    _log['f'].close()
