"""Bloque 3b: ¿la puerta esconde la via lenta? Lectura de la via lenta a priori (W_lenta_apriori) y puerta=None.
Ejecuta PREREGISTRO_xor_lectura_3b.md. REGLA 10: log desde el arranque. Identidad: organismo_v13q(lectura='lineal') == organismo_v13g.
Uso:  python experimentos/nivel7_xor_lectura/corre_xor_3b.py [--desde N]   (por defecto semillas 21-40)
"""
import sys, os, json, time, hashlib, platform, subprocess
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
import numpy as np

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
sys.path[:0] = [AQUI, os.path.join(RAIZ, 'experimentos', 'v13_dos_vias'), os.path.join(RAIZ, 'organismo')]
_desde = int(sys.argv[sys.argv.index('--desde') + 1]) if '--desde' in sys.argv else 21
SEEDS = list(range(_desde, _desde + 20))
BASE = dict(T=200000, mundo='regla', eta_s=0.015)
BRAZOS = {'CUAD_P3': dict(lectura='cuadratica', puerta=3), 'CUAD_SINP': dict(lectura='cuadratica', puerta=None), 'LIN_P3': dict(lectura='lineal', puerta=3)}
REGLAS = ['xor01', 'px0']
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


def signo_acc(Wd, test, vr):
    f = [1.0 if Wd[k] > 0 else (0.5 if Wd[k] == 0 else 0.0) for k in test if vr[k] == 'comida']
    p = [1.0 if Wd[k] < 0 else (0.5 if Wd[k] == 0 else 0.0) for k in test if vr[k] == 'veneno']
    return 0.5 * float(np.mean(f)) + 0.5 * float(np.mean(p))


def tarea(args):
    tipo = args[0]
    if tipo == 'I':
        _, regla, seed = args
        import organismo_v13g as a_, organismo_v13q as b_
        kw = dict(T=60000, mundo='regla', regla=regla, eta_s=0.015, puerta=3)
        a, b = a_.run(seed, **kw), b_.run(seed, lectura='lineal', **kw)
        dif = [kk for kk in a if N(a[kk]) != N(b[kk])]
        return dict(tipo=tipo, esc=regla, seed=seed, identico=not dif, difieren=dif)
    _, brazo, regla, seed = args
    import organismo_v13q as m
    kw = dict(BASE); kw.update(BRAZOS[brazo]); kw['regla'] = regla
    r = m.run(seed, **kw)
    vr = m.split_regla(seed, regla)[3]; test = r['test']
    fam = [r['familiar_apriori'][k] for k in test]
    return dict(tipo='T', brazo=brazo, regla=regla, seed=seed, acc=signo_acc(r['W_apriori'], test, vr), acc_lenta=signo_acc(r['W_lenta_apriori'], test, vr),
                familiar=float(np.mean(fam)) if fam else None, splits=r['splits'], celdas=r['celdas'], deaths=r['deaths'],
                W_lenta_prod01=(round(float(r['Wps'][6] - r['Wns'][6]), 3) if len(r['Wps']) > 6 else None))


def med(xs):
    xs = [x for x in xs if x is not None]
    return float(np.median(xs)), float(min(xs)), float(max(xs))


if __name__ == '__main__':
    import multiprocessing as mp
    mp.set_start_method('spawn', force=True)
    stamp = time.strftime('%Y%m%d_%H%M%S')
    _log['f'] = open(os.path.join(RAIZ, 'datos', f'xor_3b_s{SEEDS[0]}-{SEEDS[-1]}_{stamp}.log'), 'w', encoding='utf-8', newline='\n')
    pre = os.path.join(AQUI, 'PREREGISTRO_xor_lectura_3b.md')
    log(f"ARRANQUE bloque 3b (¿la puerta esconde la via lenta?). brazos {list(BRAZOS)}, reglas {REGLAS}, semillas {SEEDS[0]}-{SEEDS[-1]}. Pool({N_PARALELO}).")
    log(f"sha preregistro {h16(pre)}  script {h16(os.path.abspath(__file__))}  organismo_v13q {h16(os.path.join(AQUI, 'organismo_v13q.py'))}  organismo_v13g {h16(os.path.join(RAIZ, 'experimentos', 'v13_dos_vias', 'organismo_v13g.py'))}")
    try:
        ps = subprocess.run(['powershell', '-NoProfile', '-Command',
                             "Get-CimInstance Win32_Process | Where-Object { $_.Name -like 'python*' } | ForEach-Object { \"$($_.ProcessId) $($_.CommandLine)\" }"],
                            capture_output=True, text=True, timeout=60).stdout.strip().splitlines()
    except Exception as e:
        ps = [f"(no se pudo listar: {e})"]
    log(f"REGLA 11 — procesos python vivos ({len(ps)}), este es pid {os.getpid()}")
    V = {}
    with mp.Pool(N_PARALELO) as pool:
        ctrl = [('I', rg, s) for rg in ('xor01', 'px0') for s in (1, 2, 3)]
        log(f"ETAPA 1/3 — identidad lectura=lineal == organismo_v13g ({len(ctrl)})...")
        rc = pool.map(tarea, ctrl, chunksize=1)
        log(f"  identicos: {sum(x['identico'] for x in rc)}/{len(rc)}")
        for x in rc:
            if not x['identico']: log(f"      DIFIERE {x['esc']} s{x['seed']}: {x['difieren']}")
        V['IDENTIDAD'] = all(x['identico'] for x in rc)
        if not V['IDENTIDAD']:
            log("*** IDENTIDAD FALLIDA: se para."); sys.exit(1)
        tr = [('T', b, rg, s) for b in BRAZOS for rg in REGLAS for s in SEEDS]
        log(f"ETAPA 2/3 — {len(tr)} corridas...")
        res = []
        for i, r in enumerate(pool.imap_unordered(tarea, tr, chunksize=1), 1):
            res.append(r)
            if i % 30 == 0 or i == len(tr):
                log(f"          {i}/{len(tr)}")
    log("ETAPA 3/3 — analisis (acc = valor total a priori en nunca vistos; acc_lenta = via lenta sola; familiar = fraccion de test que la puerta lee en la rapida).")
    G = lambda b, rg: {r['seed']: r for r in res if r['brazo'] == b and r['regla'] == rg}
    for b in BRAZOS:
        for rg in REGLAS:
            g = list(G(b, rg).values())
            log(f"   {b:9s} {rg:5s} acc {med([r['acc'] for r in g])[0]:.3f}  acc_lenta {med([r['acc_lenta'] for r in g])[0]:.3f} [{med([r['acc_lenta'] for r in g])[1]:.2f},{med([r['acc_lenta'] for r in g])[2]:.2f}]"
                f"  familiar {med([r['familiar'] for r in g])[0]:.2f}  celdas {med([r['celdas'] for r in g])[0]:.0f}"
                + (f"  W_lenta(P0*P1) {med([r['W_lenta_prod01'] for r in g])[0]:+.2f}" if g[0]['W_lenta_prod01'] is not None else ''))
    A = lambda b, rg, s, k: G(b, rg)[s][k]
    par = lambda b1, b2, rg, k: sum(A(b1, rg, s, k) > A(b2, rg, s, k) for s in SEEDS)
    Y1 = med([A('CUAD_P3', 'xor01', s, 'acc_lenta') for s in SEEDS])[0] >= 0.75 and par('CUAD_P3', 'LIN_P3', 'xor01', 'acc_lenta') >= 15
    y2n = sum(A('CUAD_P3', 'xor01', s, 'acc_lenta') - A('CUAD_P3', 'xor01', s, 'acc') >= 0.20 for s in SEEDS)
    Y2 = y2n >= 15 and med([A('CUAD_P3', 'xor01', s, 'familiar') for s in SEEDS])[0] >= 0.60
    Y3 = (med([A('CUAD_SINP', 'xor01', s, 'acc') for s in SEEDS])[0] >= 0.65 and par('CUAD_SINP', 'CUAD_P3', 'xor01', 'acc') >= 15
          and med([A('CUAD_SINP', 'px0', s, 'acc') for s in SEEDS])[0] >= 0.65)
    V.update(Y1=Y1, Y2=Y2, Y2_n=y2n, Y3=Y3, lenta_gt_lin=par('CUAD_P3', 'LIN_P3', 'xor01', 'acc_lenta'), sinp_gt_p3=par('CUAD_SINP', 'CUAD_P3', 'xor01', 'acc'),
             LA_PUERTA_TAPA=bool(Y1 and Y2 and Y3))
    log(f"   Y1 lenta sabe XOR (acc_lenta>=.75, >lineal en {V['lenta_gt_lin']}/20) {'OK' if Y1 else 'NO'} | Y2 la puerta tapa (lenta-acc>=.20 en {y2n}/20, familiar>=.60) {'OK' if Y2 else 'NO'}"
        f" | Y3 sin puerta se ve (acc>=.65, >con puerta en {V['sinp_gt_p3']}/20, px0 ok) {'OK' if Y3 else 'NO'}")
    log(f"VEREDICTO 3b: {'LA PUERTA TAPA LA VIA LENTA: la lectura cuadratica generaliza XOR' if V['LA_PUERTA_TAPA'] else 'NO (alguna de Y1-Y3 cayo: ver cual)'}")
    meta = dict(fecha=time.strftime('%Y-%m-%dT%H:%M:%S'), semillas=SEEDS, base=BASE, brazos=BRAZOS, reglas=REGLAS, veredictos=V, identidades=rc, procesos_python=ps,
                sha_preregistro=h16(pre), sha_script=h16(os.path.abspath(__file__)), sha_instrumento=h16(os.path.join(AQUI, 'organismo_v13q.py')),
                python=platform.python_version(), numpy=np.__version__)
    dj = os.path.join(RAIZ, 'datos', f'xor_3b_s{SEEDS[0]}-{SEEDS[-1]}_{stamp}.json')
    json.dump(dict(meta=meta, corridas=res), open(dj, 'w', encoding='utf-8'), ensure_ascii=False, default=str)
    log(f"datos -> {os.path.basename(dj)}  sha256_16 = {h16(dj)}")
    _log['f'].close()
