"""Bloque 3e: diagnostico decisivo — ¿el limite de XOR en v13 es la REGLA o la SELECCION DE RASGOS?
Ejecuta PREREGISTRO_xor_3e.md. REGLA 10: log desde el arranque. REGLA 11: lista los python vivos antes del Pool.
Instrumento: organismo_v13q3.py (enmendado en 3e con lectura='oraculo01' y 'oraculo01_ruido'; la enmienda es INERTE
para las lecturas de 3d y se comprueba en ETAPA 1b contra los numeros ya publicados de 3d).

ETAPA 1a identidad (obligatoria, se para si falla): v13q3(dos_canales, constante=False) == organismo_v13q en TODAS las
claves del original (semillas 1-3, xor01 y px0, lecturas lineal y cuadratica).
ETAPA 1b inercia de la enmienda: CUAD_DELTA xor01 en 3 semillas de 3d debe dar EXACTAMENTE el acc/acc_lenta guardado en
datos/xor_3d_s41-60_*.json (si el JSON no esta, se salta con aviso; no es bloqueante).

NO hay --rapido: el gemelo compilado no tiene estos knobs.

Uso:  python experimentos/nivel7_xor_lectura/corre_xor_3e.py [--desde N]   (por defecto semillas 61-80; lo corre el coordinador)
      python experimentos/nivel7_xor_lectura/corre_xor_3e.py --humo        (UN proceso, sin Pool: identidad + ORACULO_DELTA y RUIDO_DELTA, 1 semilla)
"""
import sys, os, json, time, glob, hashlib, platform, subprocess
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
import numpy as np

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
sys.path[:0] = [AQUI, os.path.join(RAIZ, 'experimentos', 'v13_dos_vias'), os.path.join(RAIZ, 'organismo')]
_desde = int(sys.argv[sys.argv.index('--desde') + 1]) if '--desde' in sys.argv else 61
SEEDS = list(range(_desde, _desde + 20))
HUMO = '--humo' in sys.argv

BASE = dict(T=100000, mundo='regla', eta_s=0.015, puerta=3, lam_lenta=0.002)   # identica a 3d: un solo cambio por experimento (los rasgos)
BRAZOS = {
    'ORACULO_2C':     dict(lectura='oraculo01',       regla_lenta='dos_canales', constante=False),  # la regla ORIGINAL con los rasgos exactos
    'ORACULO_2C_CTE': dict(lectura='oraculo01',       regla_lenta='dos_canales', constante=True),   # idem + constante (separa regla de constante)
    'ORACULO_DELTA':  dict(lectura='oraculo01',       regla_lenta='delta_signo', constante=True),   # la regla de 3d con los rasgos exactos
    'RUIDO_DELTA':    dict(lectura='oraculo01_ruido', regla_lenta='delta_signo', constante=True),   # CONTROL: mismo tamano, producto equivocado
    'CUAD_DELTA':     dict(lectura='cuadratica',      regla_lenta='delta_signo', constante=True),   # referencia: el brazo refutado en 3d
}
REGLAS = ['xor01', 'px0']
IDX_PROD = {'cuadratica': 6, 'oraculo01': 2, 'oraculo01_ruido': 2}   # donde vive el producto en phi
ES_PROD = {'cuadratica': 'P0*P1', 'oraculo01': 'P0*P1', 'oraculo01_ruido': 'P2*P3'}
N_PARALELO = 14
CLASES = ['00', '01', '10', '11']
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
    """Acierto BALANCEADO por signo sobre los nunca vistos (el test de xor01 es 8 comida / 4 veneno). Empate exacto = 0.5."""
    f = [1.0 if Wd[k] > 0 else (0.5 if Wd[k] == 0 else 0.0) for k in test if vr[k] == 'comida']
    p = [1.0 if Wd[k] < 0 else (0.5 if Wd[k] == 0 else 0.0) for k in test if vr[k] == 'veneno']
    if not f or not p:
        return None
    return 0.5 * float(np.mean(f)) + 0.5 * float(np.mean(p))


def metricas(r, vr):
    test = r['test']
    pf = [r['primer'][k]['pb'] for k in test if r['primer'].get(k) is not None and vr[k] == 'comida']
    pp = [1 - r['primer'][k]['pb'] for k in test if r['primer'].get(k) is not None and vr[k] == 'veneno']
    return dict(acc=signo_acc(r['W_apriori'], test, vr), acc_lenta=signo_acc(r['W_lenta_apriori'], test, vr),
                ba=(0.5 * float(np.mean(pf)) + 0.5 * float(np.mean(pp))) if (pf and pp) else None,
                cobertura=sum(v is not None for v in r['primer'].values()), n_test=len(test))


def mecanismo(r, lectura):
    """Pesos EN LA SONDA (Ws_apriori). Con oraculo el producto es el indice 2; con cuadratica el 6; en lineal/random15 no existe."""
    v = r.get('Ws_apriori')
    if not v:
        return dict(Ws_P0=None, Ws_P1=None, Ws_prod=None, prod_es=None, Ws_cte=None, max_abs_Ws=None)
    i = IDX_PROD.get(lectura)
    return dict(Ws_P0=float(v[0]), Ws_P1=float(v[1]),
                Ws_prod=(float(v[i]) if (i is not None and len(v) > i) else None), prod_es=ES_PROD.get(lectura),
                Ws_cte=(float(v[-1]) if r.get('constante') else None), max_abs_Ws=float(max(abs(x) for x in v)))


def muestreo(r):
    """Mordidas ANTES de la sonda por clase P0P1 (cuartos 0 y 1 = t < T/2 = fase2_en por defecto) y clases con CERO."""
    pre = {c: 0 for c in CLASES}
    for k, m in r['mord'].items():
        pre[k[:2]] += int(m[0]) + int(m[1])
    return dict(mord_pre=pre, clases_sin_morder=sum(1 for c in CLASES if pre[c] == 0))


def tarea(args):
    tipo = args[0]
    if tipo == 'I':
        _, regla, lectura, seed = args
        import organismo_v13q as a_, organismo_v13q3 as b_
        kw = dict(T=60000, mundo='regla', regla=regla, eta_s=0.015, puerta=3, lectura=lectura)
        a, b = a_.run(seed, **kw), b_.run(seed, regla_lenta='dos_canales', constante=False, **kw)
        dif = [kk for kk in a if N(a[kk]) != N(b[kk])]
        return dict(tipo=tipo, esc=f"{regla}/{lectura}", seed=seed, identico=not dif, difieren=dif,
                    claves_nuevas=[kk for kk in b if kk not in a])
    _, brazo, regla, seed = args
    import organismo_v13q3 as m
    kw = dict(BASE); kw.update(BRAZOS[brazo]); kw['regla'] = regla
    if 'fase2_en' in kw:
        raise SystemExit("fase2_en fijado a mano: el conteo pre-sonda por cuartos dejaria de valer.")
    r = m.run(seed, **kw)
    vr = m.split_regla(seed, regla)[3]
    return dict(tipo='T', brazo=brazo, regla=regla, seed=seed, splits=r['splits'], celdas=r['celdas'], deaths=r['deaths'],
                **metricas(r, vr), **mecanismo(r, BRAZOS[brazo]['lectura']), **muestreo(r))


def med(xs):
    xs = [x for x in xs if x is not None]
    if not xs:
        return None, None, None
    return float(np.median(xs)), float(min(xs)), float(max(xs))


def f3(x, n=3):
    return '  n/a' if x is None else f"{x:.{n}f}"


def fs(x):
    return '  n/a' if x is None else f"{x:+.2f}"


SEM_INERCIA = (41, 42, 43)


def inercia_3d(nuevos):
    """ETAPA 1b: la enmienda de 3e debe ser INERTE para las lecturas de 3d. Compara las corridas CUAD_DELTA xor01 recien
    hechas contra los numeros ya publicados en datos/xor_3d_s*.json (el instrumento de 3d era sha b71bbe41a7326aaf)."""
    fs_ = sorted(glob.glob(os.path.join(RAIZ, 'datos', 'xor_3d_s*_*.json')))
    if not fs_:
        return dict(hay=False, nota='no se encontro datos/xor_3d_s*.json: se salta (no bloqueante)')
    d = json.load(open(fs_[-1], encoding='utf-8'))
    viejo = {c['seed']: c for c in d['corridas'] if c['brazo'] == 'CUAD_DELTA' and c['regla'] == 'xor01'}
    filas = []
    for n in nuevos:
        s = n['seed']
        if s not in viejo:
            continue
        filas.append(dict(seed=s, acc_3d=viejo[s]['acc'], acc_3e=n['acc'], lenta_3d=viejo[s]['acc_lenta'], lenta_3e=n['acc_lenta'],
                          igual=bool(viejo[s]['acc'] == n['acc'] and viejo[s]['acc_lenta'] == n['acc_lenta'])))
    return dict(hay=True, archivo=os.path.basename(fs_[-1]), sha_instrumento_3d=d['meta'].get('sha_instrumento'),
                filas=filas, inerte=bool(filas) and all(f['igual'] for f in filas))


def humo():
    """UN proceso, sin Pool (EQUIPO regla 3): identidad contra organismo_v13q + ORACULO_DELTA y RUIDO_DELTA en 1 semilla,
    T=100000. La INERCIA de la enmienda 3e sobre los brazos de 3d NO se comprueba aqui: la hace la ETAPA 1b del runner."""
    stamp = time.strftime('%Y%m%d_%H%M%S')
    _log['f'] = open(os.path.join(RAIZ, 'datos', f'xor_3e_humo_{stamp}.log'), 'w', encoding='utf-8', newline='\n')
    log("HUMO 3e (un proceso, sin Pool). identidad semilla 1 + ORACULO_DELTA y RUIDO_DELTA xor01 semilla 1, T=100000.")
    log(f"sha organismo_v13q3 {h16(os.path.join(AQUI, 'organismo_v13q3.py'))}  organismo_v13q {h16(os.path.join(AQUI, 'organismo_v13q.py'))}"
        f"  construye {h16(os.path.join(AQUI, 'construye_xor_3d.py'))}  script {h16(os.path.abspath(__file__))}")
    ide = [tarea(('I', rg, lec, 1)) for rg in ('xor01', 'px0') for lec in ('lineal', 'cuadratica')]
    for x in ide:
        log(f"   identidad {x['esc']:18s} s{x['seed']}: {'IDENTICO' if x['identico'] else 'DIFIERE ' + str(x['difieren'])}")
    if not all(x['identico'] for x in ide):
        log("*** IDENTIDAD FALLIDA: el instrumento no sirve."); _log['f'].close(); sys.exit(1)
    log(f"   identidad: {sum(x['identico'] for x in ide)}/{len(ide)} (T=60000)")
    corr = {}
    for b in ('ORACULO_DELTA', 'RUIDO_DELTA'):
        r = tarea(('T', b, 'xor01', 1)); corr[b] = r
        log(f"   {b:14s} xor01 s1: acc {f3(r['acc'])}  acc_lenta {f3(r['acc_lenta'])}  ba {f3(r['ba'])}  cobertura {r['cobertura']}/{r['n_test']}")
        log(f"                    sonda: Ws(P0) {fs(r['Ws_P0'])}  Ws(P1) {fs(r['Ws_P1'])}  Ws({r['prod_es']}) {fs(r['Ws_prod'])}"
            f"  Ws(cte) {fs(r['Ws_cte'])}  max|Ws| {f3(r['max_abs_Ws'], 2)} (clip_s=3)")
        log(f"                    muestreo: {r['mord_pre']}  clases sin morder {r['clases_sin_morder']}/4")
    log("   (3d, mismas semillas 41-60: CUAD_DELTA xor01 acc_lenta mediana 0.500. Nada se ajusta con este humo.)")
    dj = os.path.join(RAIZ, 'datos', f'xor_3e_humo_{stamp}.json')
    json.dump(dict(meta=dict(fecha=time.strftime('%Y-%m-%dT%H:%M:%S'), base=BASE, semilla=1,
                             sha_instrumento=h16(os.path.join(AQUI, 'organismo_v13q3.py')), sha_script=h16(os.path.abspath(__file__)),
                             python=platform.python_version(), numpy=np.__version__),
                   identidad=ide, corridas=corr), open(dj, 'w', encoding='utf-8'), ensure_ascii=False, default=str)
    log(f"datos -> {os.path.basename(dj)}  sha256_16 = {h16(dj)}")
    _log['f'].close()


if __name__ == '__main__':
    if HUMO:
        humo(); sys.exit(0)
    import multiprocessing as mp
    mp.set_start_method('spawn', force=True)
    stamp = time.strftime('%Y%m%d_%H%M%S')
    _log['f'] = open(os.path.join(RAIZ, 'datos', f'xor_3e_s{SEEDS[0]}-{SEEDS[-1]}_{stamp}.log'), 'w', encoding='utf-8', newline='\n')
    pre = os.path.join(AQUI, 'PREREGISTRO_xor_3e.md')
    log(f"ARRANQUE bloque 3e (¿regla o seleccion de rasgos?). brazos {list(BRAZOS)}, reglas {REGLAS}, semillas {SEEDS[0]}-{SEEDS[-1]}. Pool({N_PARALELO}).")
    log(f"BASE {BASE}  (identica a 3d: el UNICO cambio entre ORACULO_DELTA y CUAD_DELTA son los rasgos de phi)")
    log(f"sha preregistro {h16(pre)}  script {h16(os.path.abspath(__file__))}  construye {h16(os.path.join(AQUI, 'construye_xor_3d.py'))}"
        f"  organismo_v13q3 {h16(os.path.join(AQUI, 'organismo_v13q3.py'))}  organismo_v13q {h16(os.path.join(AQUI, 'organismo_v13q.py'))}")
    try:
        ps = subprocess.run(['powershell', '-NoProfile', '-Command',
                             "Get-CimInstance Win32_Process | Where-Object { $_.Name -like 'python*' } | ForEach-Object { \"$($_.ProcessId) $($_.CommandLine)\" }"],
                            capture_output=True, text=True, timeout=60).stdout.strip().splitlines()
    except Exception as e:
        ps = [f"(no se pudo listar: {e})"]
    log(f"REGLA 11 — procesos python vivos ({len(ps)}), este es pid {os.getpid()}")
    V = {}
    with mp.Pool(N_PARALELO) as pool:
        ctrl = [('I', rg, lec, s) for rg in ('xor01', 'px0') for lec in ('lineal', 'cuadratica') for s in (1, 2, 3)]
        log(f"ETAPA 1a/4 — identidad: v13q3(dos_canales, constante=False) == organismo_v13q ({len(ctrl)} corridas, T=60000)...")
        rc = pool.map(tarea, ctrl, chunksize=1)
        log(f"  identicos: {sum(x['identico'] for x in rc)}/{len(rc)}   claves nuevas: {rc[0]['claves_nuevas']}")
        for x in rc:
            if not x['identico']: log(f"      DIFIERE {x['esc']} s{x['seed']}: {x['difieren']}")
        V['IDENTIDAD'] = all(x['identico'] for x in rc)
        if not V['IDENTIDAD']:
            log("*** IDENTIDAD FALLIDA: se para."); sys.exit(1)
        log(f"ETAPA 1b/4 — inercia de la enmienda 3e sobre los numeros ya publicados de 3d (CUAD_DELTA xor01, semillas {SEM_INERCIA})...")
        inc = inercia_3d(pool.map(tarea, [('T', 'CUAD_DELTA', 'xor01', s) for s in SEM_INERCIA], chunksize=1))
        V['INERCIA_3D'] = inc
        if inc['hay']:
            for f in inc['filas']:
                log(f"      s{f['seed']}: 3d acc {f['acc_3d']:.3f} lenta {f['lenta_3d']:.3f} | 3e acc {f['acc_3e']:.3f} lenta {f['lenta_3e']:.3f}  -> {'IGUAL' if f['igual'] else '*** DISTINTO'}")
            log(f"      inerte: {inc['inerte']}  (contra {inc['archivo']}, instrumento de 3d {inc['sha_instrumento_3d']})")
            if not inc['inerte']:
                log("*** LA ENMIENDA 3e NO ES INERTE: se para (los numeros de 3d dejarian de ser reproducibles)."); sys.exit(1)
        else:
            log(f"      {inc['nota']}")
        tr = [('T', b, rg, s) for b in BRAZOS for rg in REGLAS for s in SEEDS]
        log(f"ETAPA 2/4 — {len(tr)} corridas de T={BASE['T']}...")
        res = []
        for i, r in enumerate(pool.imap_unordered(tarea, tr, chunksize=1), 1):
            res.append(r)
            if i % 25 == 0 or i == len(tr):
                log(f"          {i}/{len(tr)}")
    log("ETAPA 3/4 — tabla. acc = valor total a priori en nunca vistos; acc_lenta = via lenta sola; Ws(.) = pesos EN LA SONDA.")
    G = lambda b, rg: {r['seed']: r for r in res if r['brazo'] == b and r['regla'] == rg}
    for b in BRAZOS:
        for rg in REGLAS:
            g = list(G(b, rg).values())
            al = med([r['acc_lenta'] for r in g])
            log(f"   {b:15s} {rg:5s} acc {f3(med([r['acc'] for r in g])[0])}  acc_lenta {f3(al[0])} [{f3(al[1], 2)},{f3(al[2], 2)}]"
                f"  ba {f3(med([r['ba'] for r in g])[0])}  cobertura {f3(med([r['cobertura'] for r in g])[0], 0)}"
                f"  celdas {f3(med([r['celdas'] for r in g])[0], 0)}  muertes {f3(med([r['deaths'] for r in g])[0], 0)}"
                f"  Ws(P0) {fs(med([r['Ws_P0'] for r in g])[0])}  Ws(P1) {fs(med([r['Ws_P1'] for r in g])[0])}"
                f"  Ws({g[0]['prod_es']}) {fs(med([r['Ws_prod'] for r in g])[0])}  Ws(cte) {fs(med([r['Ws_cte'] for r in g])[0])}"
                f"  max|Ws| {f3(med([r['max_abs_Ws'] for r in g])[0], 2)}")
    log("ETAPA 4/4 — criterio.")
    A = lambda b, rg, s, k: G(b, rg).get(s, {}).get(k)
    def par(b1, b2, rg, k):
        n = 0
        for s in SEEDS:
            x, y = A(b1, rg, s, k), A(b2, rg, s, k)
            n += int(x is not None and y is not None and x > y)
        return n
    def M(b, rg, k):
        return med([A(b, rg, s, k) for s in SEEDS])[0]

    o1p = par('ORACULO_DELTA', 'RUIDO_DELTA', 'xor01', 'acc_lenta')
    m_or = M('ORACULO_DELTA', 'xor01', 'acc_lenta')
    O1 = (m_or is not None and m_or >= 0.80) and o1p >= 15
    r1 = M('ORACULO_DELTA', 'px0', 'acc_lenta')
    R1 = r1 is not None and r1 >= 0.65
    V.update(O1=bool(O1), O1_mediana=m_or, O1_pareado=o1p, R1_px0_lenta=r1, R1=bool(R1),
             ES_SELECCION_DE_RASGOS=bool(O1))
    log(f"   O1 (UNICO criterio) ORACULO_DELTA xor01 acc_lenta {f3(m_or)} >= .80 y > RUIDO_DELTA en {o1p}/20   {'OK' if O1 else 'NO'}")
    log(f"   R1 (lectura obligatoria, NO decide) px0 acc_lenta {f3(r1)} >= .65   {'OK' if R1 else 'NO — el instrumento esta roto, no se lee O1'}")
    log(f"VEREDICTO 3e: {'EL LIMITE DE XOR EN v13 ES DE SELECCION DE RASGOS (sesgo inductivo), NO DE REGLA' if V['ES_SELECCION_DE_RASGOS'] else 'NO: con los rasgos exactos la regla TAMPOCO puede -> el cuello esta en la dinamica (mordidas, error, puerta)'}")
    comp = {b: {rg: dict(acc=M(b, rg, 'acc'), acc_lenta=M(b, rg, 'acc_lenta'), Ws_prod=M(b, rg, 'Ws_prod'),
                         max_abs_Ws=M(b, rg, 'max_abs_Ws')) for rg in REGLAS} for b in BRAZOS}
    V['medianas'] = comp
    meta = dict(fecha=time.strftime('%Y-%m-%dT%H:%M:%S'), semillas=SEEDS, base=BASE, brazos=BRAZOS, reglas=REGLAS, veredictos=V,
                identidades=rc, procesos_python=ps, sha_preregistro=h16(pre), sha_script=h16(os.path.abspath(__file__)),
                sha_constructor=h16(os.path.join(AQUI, 'construye_xor_3d.py')), sha_instrumento=h16(os.path.join(AQUI, 'organismo_v13q3.py')),
                sha_origen=h16(os.path.join(AQUI, 'organismo_v13q.py')), python=platform.python_version(), numpy=np.__version__)
    dj = os.path.join(RAIZ, 'datos', f'xor_3e_s{SEEDS[0]}-{SEEDS[-1]}_{stamp}.json')
    json.dump(dict(meta=meta, corridas=res), open(dj, 'w', encoding='utf-8'), ensure_ascii=False, default=str)
    log(f"datos -> {os.path.basename(dj)}  sha256_16 = {h16(dj)}")
    _log['f'].close()
