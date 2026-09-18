"""Bloque 3d: la regla fusionada del trio para la via lenta (phi' + Ws con signo + decaimiento).
Ejecuta PREREGISTRO_xor_3d.md. REGLA 10: log desde el arranque. REGLA 11: lista los python vivos antes de abrir el Pool.
Identidad obligatoria (ETAPA 1): organismo_v13q3(regla_lenta='dos_canales', constante=False) == organismo_v13q en TODAS
las claves del original (semillas 1-3, xor01 y px0, lecturas lineal y cuadratica). Si falla, se para.

NO hay --rapido: el gemelo compilado organismo_v13q_rapido.py no tiene los knobs de 3d y correria OTRA cosa en silencio.

Uso:  python experimentos/nivel7_xor_lectura/corre_xor_3d.py [--desde N]   (por defecto semillas 41-60; lo corre el coordinador)
      python experimentos/nivel7_xor_lectura/corre_xor_3d.py --humo        (UN proceso, sin Pool: identidad 1 semilla + 1 corrida CUAD_DELTA xor01)
"""
import sys, os, json, time, hashlib, platform, subprocess
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
import numpy as np

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
sys.path[:0] = [AQUI, os.path.join(RAIZ, 'experimentos', 'v13_dos_vias'), os.path.join(RAIZ, 'organismo')]
_desde = int(sys.argv[sys.argv.index('--desde') + 1]) if '--desde' in sys.argv else 41
SEEDS = list(range(_desde, _desde + 20))
HUMO = '--humo' in sys.argv

# Preregistrado: T y lam_lenta van juntos (lam_lenta esta calibrada en unidades de actualizaciones, ~331 antes de la
# sonda a T=100000; a T=200000 la misma lambda dejaria ~0.25 del vector). NO tocar uno sin el otro.
BASE = dict(T=100000, mundo='regla', eta_s=0.015, puerta=3, lam_lenta=0.002)
BRAZOS = {
    'LINEAL':             dict(lectura='lineal',     regla_lenta='dos_canales', constante=False),   # v13 actual
    'CUAD_2C':            dict(lectura='cuadratica', regla_lenta='dos_canales', constante=False),   # bloque 3b a este T
    'CUAD_DELTA':         dict(lectura='cuadratica', regla_lenta='delta_signo', constante=True),    # la regla fusionada
    'CUAD_DELTA_SIN_CTE': dict(lectura='cuadratica', regla_lenta='delta_signo', constante=False),   # cuanto aporta la constante
    'LIN_DELTA':          dict(lectura='lineal',     regla_lenta='delta_signo', constante=True),    # control: la regla sola no basta
    'RANDOM15_DELTA':     dict(lectura='random15',   regla_lenta='delta_signo', constante=True),    # control de dimension
}
REGLAS = ['xor01', 'px0', 'azar']
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
        return None   # guardia: sin una de las dos clases no hay acierto balanceado (no se inventa 0.5)
    return 0.5 * float(np.mean(f)) + 0.5 * float(np.mean(p))


def metricas(r, vr):
    """acc = valor TOTAL a priori; acc_lenta = via lenta sola; ba = conducta al primer encuentro; cobertura = cuantos de test se vieron."""
    test = r['test']
    pf = [r['primer'][k]['pb'] for k in test if r['primer'].get(k) is not None and vr[k] == 'comida']
    pp = [1 - r['primer'][k]['pb'] for k in test if r['primer'].get(k) is not None and vr[k] == 'veneno']
    return dict(acc=signo_acc(r['W_apriori'], test, vr), acc_lenta=signo_acc(r['W_lenta_apriori'], test, vr),
                ba=(0.5 * float(np.mean(pf)) + 0.5 * float(np.mean(pp))) if (pf and pp) else None,
                cobertura=sum(v is not None for v in r['primer'].values()), n_test=len(test))


def mecanismo(r, lectura):
    """Marginales y producto EN LA SONDA (Ws_apriori), no al final de T (aviso de C). indice 6 = primer par (0,1) = P0*P1.
    Solo tiene ese significado con lectura='cuadratica': en 'random15' el indice 6 es un bit al azar y en 'lineal' no existe."""
    v = r.get('Ws_apriori')
    if not v:
        return dict(Ws_P0=None, Ws_P1=None, Ws_P0P1=None, Ws_cte=None)
    cte = float(v[-1]) if r.get('constante') else None
    prod = float(v[6]) if (lectura == 'cuadratica' and len(v) > 6) else None
    return dict(Ws_P0=float(v[0]), Ws_P1=float(v[1]), Ws_P0P1=prod, Ws_cte=cte)


def muestreo(r):
    """Cota de muestreo de C, por semilla: mordidas ANTES de la sonda por clase P0P1 (cuartos 0 y 1 = t < T/2 = fase2_en
    por defecto), y cuantas de las 4 clases no recibieron NI UNA. Solo los patrones de tren pueden morderse antes."""
    pre = {c: 0 for c in CLASES}
    for k, m in r['mord'].items():
        pre[k[:2]] += int(m[0]) + int(m[1])
    return dict(mord_pre=pre, clases_sin_morder=sum(1 for c in CLASES if pre[c] == 0))


def tarea(args):
    tipo = args[0]
    if tipo == 'I':   # identidad: knobs en su valor original == organismo_v13q, en todas las claves del original
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
    if 'fase2_en' in kw:   # guardia: 'mordidas pre-sonda' se cuenta con los cuartos 0 y 1, que son t < T/2 SOLO con fase2_en por defecto
        raise SystemExit("fase2_en fijado a mano: el conteo pre-sonda por cuartos dejaria de valer.")
    r = m.run(seed, **kw)
    vr = m.split_regla(seed, regla)[3]
    out = dict(tipo='T', brazo=brazo, regla=regla, seed=seed, splits=r['splits'], celdas=r['celdas'], deaths=r['deaths'],
               **metricas(r, vr), **mecanismo(r, BRAZOS[brazo]['lectura']), **muestreo(r))
    return out


def med(xs):
    """Mediana, min y max ignorando None. Con lista vacia devuelve (None, None, None): no se inventa un numero (auditoria, punto 5)."""
    xs = [x for x in xs if x is not None]
    if not xs:
        return None, None, None
    return float(np.median(xs)), float(min(xs)), float(max(xs))


def f3(x, n=3):
    return '  n/a' if x is None else f"{x:.{n}f}"


def fs(x):
    return '  n/a' if x is None else f"{x:+.2f}"


def humo():
    """UN proceso, sin Pool (EQUIPO regla 3): identidad en 1 semilla + UNA corrida CUAD_DELTA xor01. Nada se ajusta."""
    stamp = time.strftime('%Y%m%d_%H%M%S')
    _log['f'] = open(os.path.join(RAIZ, 'datos', f'xor_3d_humo_{stamp}.log'), 'w', encoding='utf-8', newline='\n')
    log("HUMO 3d (un proceso, sin Pool). identidad semilla 1 + 1 corrida CUAD_DELTA xor01 semilla 1, T=100000.")
    log(f"sha organismo_v13q3 {h16(os.path.join(AQUI, 'organismo_v13q3.py'))}  organismo_v13q {h16(os.path.join(AQUI, 'organismo_v13q.py'))}"
        f"  construye {h16(os.path.join(AQUI, 'construye_xor_3d.py'))}  script {h16(os.path.abspath(__file__))}")
    ide = [tarea(('I', rg, lec, 1)) for rg in ('xor01', 'px0') for lec in ('lineal', 'cuadratica')]
    for x in ide:
        log(f"   identidad {x['esc']:18s} s{x['seed']}: {'IDENTICO' if x['identico'] else 'DIFIERE ' + str(x['difieren'])}")
    log(f"   identidad: {sum(x['identico'] for x in ide)}/{len(ide)} (T=60000). claves NUEVAS en v13q3 (no cuentan): {ide[0]['claves_nuevas']}")
    if not all(x['identico'] for x in ide):
        log("*** IDENTIDAD FALLIDA: el instrumento no sirve."); _log['f'].close(); sys.exit(1)
    log("   corrida CUAD_DELTA xor01 semilla 1 (T=100000, lam_lenta=0.002, constante=True)...")
    r = tarea(('T', 'CUAD_DELTA', 'xor01', 1))
    log(f"   acc {f3(r['acc'])}  acc_lenta {f3(r['acc_lenta'])}  ba {f3(r['ba'])}  cobertura {r['cobertura']}/{r['n_test']}"
        f"  celdas {r['celdas']}  muertes {r['deaths']}")
    log(f"   mecanismo EN LA SONDA: Ws(P0) {fs(r['Ws_P0'])}  Ws(P1) {fs(r['Ws_P1'])}  Ws(P0*P1) {fs(r['Ws_P0P1'])}  Ws(cte) {fs(r['Ws_cte'])}")
    log(f"   muestreo: mordidas pre-sonda por clase {r['mord_pre']}  clases sin morder {r['clases_sin_morder']}/4")
    log("   (referencia del piloto de C, misma semilla y lambda, copia exploratoria: acc_lenta 0.312. NO se ajusta nada con esto.)")
    dj = os.path.join(RAIZ, 'datos', f'xor_3d_humo_{stamp}.json')
    json.dump(dict(meta=dict(fecha=time.strftime('%Y-%m-%dT%H:%M:%S'), base=BASE, brazo='CUAD_DELTA', semilla=1,
                             sha_instrumento=h16(os.path.join(AQUI, 'organismo_v13q3.py')), sha_script=h16(os.path.abspath(__file__)),
                             python=platform.python_version(), numpy=np.__version__),
                   identidad=ide, corrida=r), open(dj, 'w', encoding='utf-8'), ensure_ascii=False, default=str)
    log(f"datos -> {os.path.basename(dj)}  sha256_16 = {h16(dj)}")
    _log['f'].close()


if __name__ == '__main__':
    if HUMO:
        humo(); sys.exit(0)
    import multiprocessing as mp
    mp.set_start_method('spawn', force=True)
    stamp = time.strftime('%Y%m%d_%H%M%S')
    _log['f'] = open(os.path.join(RAIZ, 'datos', f'xor_3d_s{SEEDS[0]}-{SEEDS[-1]}_{stamp}.log'), 'w', encoding='utf-8', newline='\n')
    pre = os.path.join(AQUI, 'PREREGISTRO_xor_3d.md')
    log(f"ARRANQUE bloque 3d (regla fusionada del trio: phi' + Ws con signo + decaimiento). brazos {list(BRAZOS)}, reglas {REGLAS}, semillas {SEEDS[0]}-{SEEDS[-1]}. Pool({N_PARALELO}).")
    log(f"BASE {BASE}  (lam_lenta y T van juntos: calibrado en ~331 actualizaciones pre-sonda)")
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
        log(f"ETAPA 1/3 — identidad: v13q3(dos_canales, constante=False) == organismo_v13q en todas las claves ({len(ctrl)} corridas, T=60000)...")
        rc = pool.map(tarea, ctrl, chunksize=1)
        log(f"  identicos: {sum(x['identico'] for x in rc)}/{len(rc)}   claves nuevas de v13q3 (no entran en la identidad): {rc[0]['claves_nuevas']}")
        for x in rc:
            if not x['identico']: log(f"      DIFIERE {x['esc']} s{x['seed']}: {x['difieren']}")
        V['IDENTIDAD'] = all(x['identico'] for x in rc)
        if not V['IDENTIDAD']:
            log("*** IDENTIDAD FALLIDA: se para."); sys.exit(1)
        tr = [('T', b, rg, s) for b in BRAZOS for rg in REGLAS for s in SEEDS]
        log(f"ETAPA 2/3 — {len(tr)} corridas de T={BASE['T']}...")
        res = []
        for i, r in enumerate(pool.imap_unordered(tarea, tr, chunksize=1), 1):
            res.append(r)
            if i % 30 == 0 or i == len(tr):
                log(f"          {i}/{len(tr)}")
    log("ETAPA 3/3 — analisis. acc = valor total a priori en nunca vistos; acc_lenta = via lenta sola; Ws(.) = pesos EN LA SONDA.")
    G = lambda b, rg: {r['seed']: r for r in res if r['brazo'] == b and r['regla'] == rg}
    for b in BRAZOS:
        for rg in REGLAS:
            g = list(G(b, rg).values())
            al = med([r['acc_lenta'] for r in g])
            log(f"   {b:19s} {rg:5s} acc {f3(med([r['acc'] for r in g])[0])}  acc_lenta {f3(al[0])} [{f3(al[1], 2)},{f3(al[2], 2)}]"
                f"  ba {f3(med([r['ba'] for r in g])[0])}  cobertura {f3(med([r['cobertura'] for r in g])[0], 0)}"
                f"  celdas {f3(med([r['celdas'] for r in g])[0], 0)}  muertes {f3(med([r['deaths'] for r in g])[0], 0)}"
                f"  Ws(P0) {fs(med([r['Ws_P0'] for r in g])[0])}  Ws(P1) {fs(med([r['Ws_P1'] for r in g])[0])}"
                f"  Ws(P0*P1) {fs(med([r['Ws_P0P1'] for r in g])[0])}  Ws(cte) {fs(med([r['Ws_cte'] for r in g])[0])}")
    A = lambda b, rg, s, k: G(b, rg).get(s, {}).get(k)
    def par(b1, b2, rg, k):   # pareado por semilla; una semilla sin dato no cuenta a favor
        n = 0
        for s in SEEDS:
            x, y = A(b1, rg, s, k), A(b2, rg, s, k)
            n += int(x is not None and y is not None and x > y)
        return n
    def M(b, rg, k):
        return med([A(b, rg, s, k) for s in SEEDS])[0]
    def le(x, u):
        return x is not None and x <= u
    def ge(x, u):
        return x is not None and x >= u
    def ent(x, a, b):
        return x is not None and a <= x <= b

    z1p = par('CUAD_DELTA', 'CUAD_2C', 'xor01', 'acc_lenta')
    Z1 = ge(M('CUAD_DELTA', 'xor01', 'acc_lenta'), 0.70) and z1p >= 15
    Z2 = le(M('LIN_DELTA', 'xor01', 'acc_lenta'), 0.60) and le(M('RANDOM15_DELTA', 'xor01', 'acc_lenta'), 0.60)
    Z3 = (ge(M('CUAD_DELTA', 'px0', 'acc'), 0.65) and ge(M('CUAD_DELTA', 'px0', 'acc_lenta'), 0.65)
          and ent(M('CUAD_DELTA', 'azar', 'acc'), 0.35, 0.65) and ent(M('CUAD_DELTA', 'azar', 'acc_lenta'), 0.35, 0.65))
    z4n = sum(1 for s in SEEDS if None not in (A('CUAD_DELTA', 'xor01', s, 'Ws_P0'), A('CUAD_DELTA', 'xor01', s, 'Ws_P1'), A('CUAD_DELTA', 'xor01', s, 'Ws_P0P1'))
              and A('CUAD_DELTA', 'xor01', s, 'Ws_P0') > 0 and A('CUAD_DELTA', 'xor01', s, 'Ws_P1') > 0 and A('CUAD_DELTA', 'xor01', s, 'Ws_P0P1') < 0)
    Z4 = z4n >= 15
    V.update(Z1=bool(Z1), Z1_pareado=z1p, Z2=bool(Z2), Z3=bool(Z3), Z4=bool(Z4), Z4_n=z4n,
             LA_REGLA_SEPARA_XOR=bool(Z1 and Z2 and Z3))
    log(f"   Z1 CUAD_DELTA xor01 acc_lenta>=.70 y >CUAD_2C en {z1p}/20  {'OK' if Z1 else 'NO'}")
    log(f"   Z2 controles LIN_DELTA<=.60 y RANDOM15_DELTA<=.60          {'OK' if Z2 else 'NO'}")
    log(f"   Z3 regresion px0>=.65 y azar en [.35,.65] (acc y acc_lenta) {'OK' if Z3 else 'NO'}")
    log(f"   Z4 mecanismo Ws(P0)>0, Ws(P1)>0, Ws(P0*P1)<0 en {z4n}/20    {'OK' if Z4 else 'NO'}  (lectura, no requisito)")
    log(f"VEREDICTO 3d: {'LA REGLA FUSIONADA SEPARA XOR EN NUNCA VISTOS' if V['LA_REGLA_SEPARA_XOR'] else 'NO (ver cual de Z1-Z3 cayo)'}")
    # Curva preregistrada (se reporta pase o no Z1; NO sustituye a Z1): acc_lenta por cota de muestreo del mundo.
    log("   CURVA preregistrada — CUAD_DELTA xor01 por clases XOR sin morder antes de la sonda:")
    estr = {}
    for e in (0, 1, 2, 3):
        g = [r for r in res if r['brazo'] == 'CUAD_DELTA' and r['regla'] == 'xor01' and r['clases_sin_morder'] == e]
        if g:
            m = med([r['acc_lenta'] for r in g]); estr[e] = dict(n=len(g), mediana=m[0], min=m[1], max=m[2])
            log(f"      {e} clase(s) sin morder: n={len(g):2d}  acc_lenta mediana {f3(m[0])} [{f3(m[1], 2)},{f3(m[2], 2)}]")
    cmp2c = {}
    for b in ('CUAD_DELTA', 'CUAD_2C', 'CUAD_DELTA_SIN_CTE'):
        cmp2c[b] = {rg: M(b, rg, 'acc_lenta') for rg in REGLAS}
    V['estratos_muestreo'] = estr; V['acc_lenta_por_brazo'] = cmp2c
    meta = dict(fecha=time.strftime('%Y-%m-%dT%H:%M:%S'), semillas=SEEDS, base=BASE, brazos=BRAZOS, reglas=REGLAS, veredictos=V,
                identidades=rc, procesos_python=ps, sha_preregistro=h16(pre), sha_script=h16(os.path.abspath(__file__)),
                sha_constructor=h16(os.path.join(AQUI, 'construye_xor_3d.py')), sha_instrumento=h16(os.path.join(AQUI, 'organismo_v13q3.py')),
                sha_origen=h16(os.path.join(AQUI, 'organismo_v13q.py')), python=platform.python_version(), numpy=np.__version__)
    dj = os.path.join(RAIZ, 'datos', f'xor_3d_s{SEEDS[0]}-{SEEDS[-1]}_{stamp}.json')
    json.dump(dict(meta=meta, corridas=res), open(dj, 'w', encoding='utf-8'), ensure_ascii=False, default=str)
    log(f"datos -> {os.path.basename(dj)}  sha256_16 = {h16(dj)}")
    _log['f'].close()
