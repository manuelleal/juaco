"""Candidato v15c: la memoria de un golpe por pares en la VIA LENTA DEL TRONCO. Ejecuta PREREGISTRO_v15c.md.
REGLA 10: log desde el arranque. REGLA 11: lista los python vivos antes del Pool.

ETAPA 1  identidad interna (`identidad_v15c.py` como SUBPROCESO): I1 v15c(None) == v14.1, I2 el rng no se consume,
         I3 v15gc(None) == v14g, I4 la ganadora coincide con organismo_g3A (la equivalencia exacta NO se reclama).
ETAPA 2  V1 examen del criterio v3' (`bateria_v15c.py 20 --desde 101 --log`, SUBPROCESO; trae su propio Pool).
ETAPA 3  V2a generalizacion (`bateria_generaliza_v15c.py organismo_v15c_on 20 --desde 101 --log`, SUBPROCESO).
ETAPA 4  V2b mundo de regla 121-140 con la memoria ENCENDIDA: xor01 (DOS puntuaciones), px0 y azar. Pool aqui.
ETAPA 5  umbrales del preregistro.
Los subprocesos van SECUENCIALES: nunca hay dos Pool a la vez (regla 11).

Uso:  python experimentos/creacion_A/corre_v15c.py [--desde N]
      python experimentos/creacion_A/corre_v15c.py --humo   (UN proceso, sin Pool: identidad corta + 1 semilla)
"""
import sys, os, json, time, hashlib, platform, subprocess
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
import numpy as np

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
sys.path[:0] = [AQUI, os.path.join(RAIZ, 'organismo')]
_desde = int(sys.argv[sys.argv.index('--desde') + 1]) if '--desde' in sys.argv else 121
SEEDS = list(range(_desde, _desde + 20))
HUMO = '--humo' in sys.argv
REGLAS = ['xor01', 'px0', 'azar']
N_PARALELO = 14
_log = {'f': None, 't0': time.time()}


def log(msg=""):
    linea = f"[{time.strftime('%H:%M:%S')} +{time.time()-_log['t0']:7.1f}s] {msg}"
    print(linea, flush=True)
    if _log['f']:
        _log['f'].write(linea + "\n"); _log['f'].flush(); os.fsync(_log['f'].fileno())


def h16(p):
    return hashlib.sha256(open(p, 'rb').read()).hexdigest()[:16]


def f3(x, n=3):
    return '  n/a' if x is None else f"{x:.{n}f}"


def med(xs):
    xs = [x for x in xs if x is not None]
    if not xs:
        return None, None, None
    return float(np.median(xs)), float(min(xs)), float(max(xs))


def acc_dos(Wd, test, vr):
    """(registro, ESTRICTA). Registro: valor 0 exacto = 0.5. Estricta: valor 0 = FALLO (la abstencion no puntua)."""
    out = []
    for medio in (0.5, 0.0):
        f = [1.0 if Wd[k] > 0 else (medio if Wd[k] == 0 else 0.0) for k in test if vr[k] == 'comida']
        p = [1.0 if Wd[k] < 0 else (medio if Wd[k] == 0 else 0.0) for k in test if vr[k] == 'veneno']
        out.append(None if (not f or not p) else 0.5 * float(np.mean(f)) + 0.5 * float(np.mean(p)))
    return out[0], out[1]


def tarea(args):
    """Una corrida del mundo de regla con la memoria de pares ENCENDIDA (y su gemela APAGADA, pareada)."""
    regla, seed, mem = args
    import organismo_v15gc as m
    r = m.run(seed, T=200000, mundo='regla', regla=regla, eta_s=0.15, puerta=3, memoria_pares=mem)
    vr = m.split_regla(seed, regla)[3]; test = r['test']
    a_reg, a_est = acc_dos(r['W_apriori'], test, vr)
    pf = [r['primer'][k]['pb'] for k in test if r['primer'].get(k) is not None and vr[k] == 'comida']
    pp = [1 - r['primer'][k]['pb'] for k in test if r['primer'].get(k) is not None and vr[k] == 'veneno']
    return dict(regla=regla, seed=seed, memoria=mem, acc=a_reg, acc_estricta=a_est,
                ba=(0.5 * float(np.mean(pf)) + 0.5 * float(np.mean(pp))) if (pf and pp) else None,
                cobertura_test=sum(v is not None for v in r['primer'].values()),
                ganadora=r['mem_ganadora'], cobertura=r['mem_cobertura'], vistas=r['mem_vistas'],
                celdas=r['celdas'], splits=r['splits'], deaths=r['deaths'])


def sub(cmd, etq):
    log(f"   -> SUBPROCESO ({etq}): {' '.join(cmd[1:])}")
    t0 = time.time()
    p = subprocess.run([sys.executable] + cmd[1:], capture_output=True, text=True, cwd=AQUI)
    cola = [l for l in (p.stdout or '').strip().splitlines()[-14:]]
    for l in cola: log(f"      | {l}")
    if p.returncode != 0:
        log(f"      *** codigo {p.returncode}; stderr: {(p.stderr or '')[-400:]}")
    log(f"      ({time.time()-t0:.0f}s)")
    return dict(etq=etq, cmd=cmd[1:], returncode=p.returncode, cola=cola)


if __name__ == '__main__':
    stamp = time.strftime('%Y%m%d_%H%M%S')
    nom = f"v15c_humo_{stamp}" if HUMO else f"v15c_s{SEEDS[0]}-{SEEDS[-1]}_{stamp}"
    _log['f'] = open(os.path.join(RAIZ, 'datos', nom + '.log'), 'w', encoding='utf-8', newline='\n')
    pre = os.path.join(AQUI, 'PREREGISTRO_v15c.md')
    log(f"ARRANQUE v15c ({'HUMO, un proceso, sin Pool' if HUMO else f'semillas {SEEDS[0]}-{SEEDS[-1]}'}).")
    log(f"sha preregistro {h16(pre) if os.path.exists(pre) else '(falta)'}  script {h16(os.path.abspath(__file__))}"
        f"  construye_v15c {h16(os.path.join(AQUI,'construye_v15c.py'))}"
        f"  organismo_v15c {h16(os.path.join(AQUI,'organismo_v15c.py'))}"
        f"  organismo_v15c_on {h16(os.path.join(AQUI,'organismo_v15c_on.py'))}"
        f"  organismo_v15gc {h16(os.path.join(AQUI,'organismo_v15gc.py'))}"
        f"  organismo_v15gc_on {h16(os.path.join(AQUI,'organismo_v15gc_on.py'))}"
        f"  bateria_v15c {h16(os.path.join(AQUI,'bateria_v15c.py'))}"
        f"  bateria_generaliza_v15c {h16(os.path.join(AQUI,'bateria_generaliza_v15c.py'))}"
        f"  ORIGEN organismo_v14 {h16(os.path.join(RAIZ,'organismo','organismo_v14.py'))}"
        f"  organismo_v14g {h16(os.path.join(RAIZ,'organismo','organismo_v14g.py'))}")
    V = {}
    if HUMO:
        log("ETAPA 1/3 — identidad corta (T=20000, un proceso).")
        r1 = sub([sys.executable, os.path.join(AQUI, 'identidad_v15c.py'), '20000'], 'identidad')
        V['identidad'] = r1['cola'][-1] if r1['cola'] else None
        log("ETAPA 2/3 — mundo de regla, 1 semilla, memoria ON y OFF (pareado).")
        res = [tarea((rg, _desde, mem)) for rg in REGLAS for mem in ('combi', None)]
        for r in res:
            log(f"   {r['regla']:6s} memoria={str(r['memoria']):5s} s{r['seed']}: registro {f3(r['acc'])}  "
                f"ESTRICTA {f3(r['acc_estricta'])}  ba {f3(r['ba'])}  ganadora {r['ganadora']}  "
                f"cobertura {r['cobertura']}/4  celdas {r['celdas']}  splits {r['splits']}  muertes {r['deaths']}")
        log("ETAPA 3/3 — las baterias NO se corren en el humo (traen su propio Pool). Comandos para el coordinador:")
        log("   python experimentos/creacion_A/bateria_v15c.py 20 --desde 101 --log")
        log("   python experimentos/creacion_A/bateria_generaliza_v15c.py organismo_v15c_on 20 --desde 101 --log")
        dj = os.path.join(RAIZ, 'datos', nom + '.json')
        json.dump(dict(meta=dict(fecha=time.strftime('%Y-%m-%dT%H:%M:%S'), humo=True, semilla=_desde,
                                 python=platform.python_version(), numpy=np.__version__),
                       identidad=r1, corridas=res), open(dj, 'w', encoding='utf-8'), ensure_ascii=False, default=str)
        log(f"datos -> {os.path.basename(dj)}  sha256_16 = {h16(dj)}")
        _log['f'].close(); sys.exit(0)

    try:
        ps = subprocess.run(['powershell', '-NoProfile', '-Command',
                             "Get-CimInstance Win32_Process | Where-Object { $_.Name -like 'python*' } | ForEach-Object { \"$($_.ProcessId) $($_.CommandLine)\" }"],
                            capture_output=True, text=True, timeout=60).stdout.strip().splitlines()
    except Exception as e:
        ps = [f"(no se pudo listar: {e})"]
    log(f"REGLA 11 — procesos python vivos ({len(ps)}), este es pid {os.getpid()}")
    log("ETAPA 1/5 — identidad interna (subproceso).")
    r1 = sub([sys.executable, os.path.join(AQUI, 'identidad_v15c.py'), '30000'], 'identidad')
    if r1['returncode'] != 0 or not any('32/32' in l or 'IDENTIDAD' in l for l in r1['cola']):
        log("*** la identidad no se pudo leer; se para."); _log['f'].close(); sys.exit(1)
    log("ETAPA 2/5 — V1: examen del criterio v3' con la perilla APAGADA (subproceso, trae su Pool).")
    r2 = sub([sys.executable, os.path.join(AQUI, 'bateria_v15c.py'), '20', '--desde', '101', '--log'], 'V1 examen')
    log("ETAPA 3/5 — V2a: generalizacion con la memoria ENCENDIDA (subproceso, trae su Pool).")
    r3 = sub([sys.executable, os.path.join(AQUI, 'bateria_generaliza_v15c.py'),
              'organismo_v15c_on', '20', '--desde', '101', '--log'], 'V2a generalizacion')
    log(f"ETAPA 4/5 — V2b: mundo de regla {SEEDS[0]}-{SEEDS[-1]}, memoria ON y OFF, {len(REGLAS)} reglas.")
    import multiprocessing as mp
    mp.set_start_method('spawn', force=True)
    tr = [(rg, s, mem) for rg in REGLAS for s in SEEDS for mem in ('combi', None)]
    with mp.Pool(N_PARALELO) as pool:
        res = []
        for i, r in enumerate(pool.imap_unordered(tarea, tr, chunksize=1), 1):
            res.append(r)
            if i % 30 == 0 or i == len(tr): log(f"          {i}/{len(tr)}")
    G = lambda rg, mem: [r for r in res if r['regla'] == rg and r['memoria'] == mem]
    for rg in REGLAS:
        for mem in ('combi', None):
            g = G(rg, mem)
            ar = med([r['acc'] for r in g]); ae = med([r['acc_estricta'] for r in g])
            log(f"   {rg:6s} memoria={str(mem):5s}  registro {f3(ar[0])} [{f3(ar[1],2)},{f3(ar[2],2)}]  "
                f"ESTRICTA {f3(ae[0])}  ba {f3(med([r['ba'] for r in g])[0])}  "
                f"gana(0,1) {sum(1 for r in g if r['ganadora'] == [0, 1])}/{len(g)}  "
                f"cobertura {f3(med([r['cobertura'] for r in g])[0],1)}/4  "
                f"celdas {f3(med([r['celdas'] for r in g])[0],0)}  muertes {f3(med([r['deaths'] for r in g])[0],0)}")
    log("ETAPA 5/5 — umbrales del preregistro.")
    x = med([r['acc_estricta'] for r in G('xor01', 'combi')])[0]
    p0 = med([r['acc'] for r in G('px0', 'combi')])[0]
    az = med([r['acc'] for r in G('azar', 'combi')])[0]
    c14 = med([r['celdas'] for r in G('xor01', None)])[0]; c15 = med([r['celdas'] for r in G('xor01', 'combi')])[0]
    V['V2b_xor01_estricta'] = x; V['V2b_px0'] = p0; V['V2b_azar'] = az
    V['V2b'] = bool(x is not None and x >= 0.75 and p0 is not None and p0 >= 1.0 - 1e-9 and az is not None and 0.35 <= az <= 0.65)
    V['V4_celdas'] = dict(v14=c14, v15=c15, delta=(None if not c14 else round((c15 - c14) / c14, 3)))
    V['V4'] = bool(c14 and abs((c15 - c14) / c14) <= 0.10)
    log(f"   V2b xor01 ESTRICTA {f3(x)} >= .75 · px0 {f3(p0)} = 1.000 · azar {f3(az)} en [.35,.65]   {'OK' if V['V2b'] else 'NO'}")
    log(f"   V4 (lo medible) celdas v14.1 {f3(c14,1)} vs v15c {f3(c15,1)} (±10 %)                   {'OK' if V['V4'] else 'NO'}")
    log("   V1 y V2a: leer el veredicto de las dos baterias en sus propios logs (ETAPAS 2 y 3).")
    log("   V3: NO MEDIBLE con los instrumentos de hoy (el mundo largo deriva de v13). Declarado en el preregistro §4.")
    log("RECORDATORIO (clausula del preregistro §5): si V1 o V2a caen, la memoria por pares NO entra al tronco; "
        "queda como ORGANO DEL MUNDO DE REGLA.")
    meta = dict(fecha=time.strftime('%Y-%m-%dT%H:%M:%S'), semillas=SEEDS, reglas=REGLAS, veredictos=V,
                etapas=[r1, r2, r3], procesos_python=ps,
                sha_preregistro=h16(pre) if os.path.exists(pre) else None, sha_script=h16(os.path.abspath(__file__)),
                sha_v15c=h16(os.path.join(AQUI, 'organismo_v15c.py')),
                sha_v15gc=h16(os.path.join(AQUI, 'organismo_v15gc.py')),
                sha_origen_v14=h16(os.path.join(RAIZ, 'organismo', 'organismo_v14.py')),
                python=platform.python_version(), numpy=np.__version__)
    dj = os.path.join(RAIZ, 'datos', nom + '.json')
    json.dump(dict(meta=meta, corridas=res), open(dj, 'w', encoding='utf-8'), ensure_ascii=False, default=str)
    log(f"datos -> {os.path.basename(dj)}  sha256_16 = {h16(dj)}")
    _log['f'].close()
