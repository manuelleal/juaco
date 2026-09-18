"""Bloque 6 (RAMA exploratoria) — ejecuta PREREGISTRO_allostasis.md: modelo de si mismo minimo (predictor de dE) y
sorpresa que modula eta, contra la inversion de regla en T/2. REGLA 10: log desde el arranque.

    python experimentos/nivel9_allostasis/corre_allostasis.py [--desde N] [--sin-generaliza] [--sin-bateria]
    python experimentos/nivel9_allostasis/corre_allostasis.py --humo      (UN proceso, sin Pool: lo corre el disenador)

Etapas con Pool (las corre el COORDINADOR, reglas 3 y 11):
  1/4 identidades I1 (apagado == v13), I2 (predictor encendido sin modular == v13, "solo mide") e I3 (modo regla == v13g)
  2/4 experimento principal: 4 brazos x 10 semillas, T=200000, invertir_en=100000
  3/4 retencion M4: los SEIS escenarios de organismo/bateria_v13.py con SUS criterios, 4 brazos x 10 semillas
  4/4 generalizacion M5: G1/G2 px0/azar con organismo_v13ag.py (formula copiada de organismo/bateria_generaliza.py)

Nada se cierra con 10 semillas: la rama pide replica preregistrada en semillas nuevas antes de cualquier afirmacion.
Vocabulario (regla 6): "predictor", "error de prediccion" y "sorpresa" son las tres cantidades del preregistro; nada mas.
"""
import sys, os, json, time, hashlib, platform, subprocess
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
import numpy as np

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
sys.path[:0] = [AQUI, os.path.join(RAIZ, 'organismo'), os.path.join(RAIZ, 'experimentos', 'v13_dos_vias')]

T = 200000
T_INV = T // 2
T_BAT = 100000              # el T por defecto de bateria_v13
VENT = 2000                 # vent_sorpresa
N_PARALELO = 14
REGLAS = ['px0', 'azar']

BRAZOS = {
    'V13':          dict(eta_pred=0.0,  k_sorpresa=0.0),
    'V13+PRED':     dict(eta_pred=0.03, k_sorpresa=0.0),
    'V13+SORPRESA': dict(eta_pred=0.03, k_sorpresa=1.0),
    'V13+RUIDO':    dict(eta_pred=0.03, k_sorpresa=1.0, sorpresa_barajada=True, buf_sorpresa=10),   # ENMIENDA 2
}
ESC_ID = {'base': dict(), 'invertir': dict(invertir_en=50000), 'nuevo': dict(nuevo='C')}
SEMILLAS_ID = [1, 2, 3, 4, 5, 6]

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


# ---------------------------------------------------------------- guardias None
def mediana(xs):
    """Mediana ignorando None. Devuelve None si no queda nada (guardia de la regla: None nunca se compara)."""
    xs = [x for x in xs if x is not None]
    return float(np.median(xs)) if xs else None


def pareado(a, b, semillas, clave, menor_es_mejor=True):
    """Cuenta en cuantas semillas a es mejor que b en `clave`. None cuenta como NO mejor (nunca como victoria)."""
    n = 0
    for s in semillas:
        x, y = a.get(s, {}).get(clave), b.get(s, {}).get(clave)
        if x is None or y is None:
            continue
        n += (x < y) if menor_es_mejor else (x > y)
    return n


def razon(x, y):
    """x/y con guardias: None o y==0 -> None."""
    if x is None or y is None or y == 0:
        return None
    return x / y


def rec(o):
    """Pasos de recuperacion = t_ext_B - invertir_en, censurado a T-invertir_en si nunca ocurre."""
    te = o.get('t_ext_B')
    return (T - T_INV) if te is None else (te - T_INV)


# ---------------------------------------------------------------- tareas
def tarea(args):
    tipo = args[0]

    if tipo == 'I':                                   # I1 / I2: v13a apagado / con el predictor sin modular == v13
        _, cual, esc, seed = args
        import organismo_v13 as v13, organismo_v13a as v13a
        kw = dict(ESC_ID[esc])
        a = v13.run(seed, **kw)
        b = v13a.run(seed, **kw, **(dict(eta_pred=0.0, k_sorpresa=0.0) if cual == 'I1' else dict(eta_pred=0.03, k_sorpresa=0.0)))
        dif = [k for k in a if N(a[k]) != N(b[k])]
        return dict(tipo='I', cual=cual, esc=esc, seed=seed, identico=not dif, difieren=dif)

    if tipo == 'I3':                                  # modo regla: v13ag apagado == v13g
        _, regla, seed = args
        import organismo_v13g as g, organismo_v13ag as ag
        kw = dict(T=T, mundo='regla', regla=regla, eta_s=0.015, puerta=3)
        a = g.run(seed, **kw)
        b = ag.run(seed, **kw, eta_pred=0.0, k_sorpresa=0.0)
        dif = [k for k in a if N(a[k]) != N(b[k])]
        return dict(tipo='I3', cual='I3', esc=regla, seed=seed, identico=not dif, difieren=dif)

    if tipo == 'T':                                   # experimento principal
        _, brazo, seed = args
        import organismo_v13a as v13a
        r = v13a.run(seed, T=T, invertir_en=T_INV, vent_sorpresa=VENT, **BRAZOS[brazo])
        return dict(tipo='T', brazo=brazo, seed=seed, t_ext_B=r['t_ext_B'], recup=rec(r),
                    censurado=r['t_ext_B'] is None, veneno_post=r['mord_post']['veneno'], comida_post=r['mord_post']['comida'],
                    deaths=r['deaths'], deaths_post=r['deaths_post'], W=r['W'], W_lenta=r['W_lenta'], W_pred=r['W_pred'],
                    sorpresa_media=r['sorpresa_media'], error_pred=r['error_pred'], eta_media=r['eta_media'], bocados=r['bocados'],
                    sorpresa_pre=r['sorpresa_pre'], sorpresa_post=r['sorpresa_post'], eta_pre=r['eta_pre'], eta_post=r['eta_post'],
                    n_pre=r['n_pre'], n_post=r['n_post'], splits=r['splits'], celdas=r['celdas'])

    if tipo == 'B':                                   # M4: retencion con los criterios de bateria_v13
        _, brazo, etapa, seed = args
        import organismo_v13a as v13a, bateria_v13 as bv13
        kw = dict(bv13.ETAPAS[etapa]); kw.update(BRAZOS[brazo])
        r = v13a.run(seed, T=T_BAT, **kw)
        crit = {nombre: bool(f(r)) for nombre, f in bv13.CRIT[etapa].items()}
        return dict(tipo='B', brazo=brazo, etapa=etapa, seed=seed, crit=crit, pasa=all(crit.values()),
                    W=r['W'], celdas=r['celdas'], splits=r['splits'], deaths=r['deaths'])

    # G: generalizacion. Formula G1/G2/cobertura COPIADA de organismo/bateria_generaliza.py (46772f5a582872c8), tarea().
    _, brazo, regla, seed = args
    import organismo_v13ag as ag
    r = ag.run(seed, T=T, mundo='regla', regla=regla, eta_s=0.015, puerta=3, **BRAZOS[brazo])
    vr = ag.split_regla(seed, regla)[3]
    test = r['test']
    f = [1.0 if r['W_apriori'][k] > 0 else (0.5 if r['W_apriori'][k] == 0 else 0.0) for k in test if vr[k] == 'comida']
    p = [1.0 if r['W_apriori'][k] < 0 else (0.5 if r['W_apriori'][k] == 0 else 0.0) for k in test if vr[k] == 'veneno']
    pf = [r['primer'][k]['pb'] for k in test if r['primer'][k] is not None and vr[k] == 'comida']
    pp = [1 - r['primer'][k]['pb'] for k in test if r['primer'][k] is not None and vr[k] == 'veneno']
    return dict(tipo='G', brazo=brazo, regla=regla, seed=seed,
                acc=(0.5 * float(np.mean(f)) + 0.5 * float(np.mean(p))) if (f and p) else None,
                ba=(0.5 * float(np.mean(pf)) + 0.5 * float(np.mean(pp))) if (pf and pp) else None,
                cobertura=sum(v is not None for v in r['primer'].values()), splits=r['splits'], celdas=r['celdas'], deaths=r['deaths'])


# ---------------------------------------------------------------- humo (UN proceso, sin Pool)
def humo():
    import organismo_v13 as v13, organismo_v13a as v13a
    stamp = time.strftime('%Y%m%d_%H%M%S')
    _log['f'] = open(os.path.join(RAIZ, 'datos', f'allostasis_humo_{stamp}.log'), 'w', encoding='utf-8', newline='\n')
    log("HUMO del disenador, UN proceso, sin Pool (regla 3). Preregistro PREREGISTRO_allostasis.md, seccion 11.")
    log(f"sha preregistro {h16(os.path.join(AQUI, 'PREREGISTRO_allostasis.md'))}  constructor {h16(os.path.join(AQUI, 'construye_allostasis.py'))}"
        f"  v13a {h16(os.path.join(AQUI, 'organismo_v13a.py'))}  v13ag {h16(os.path.join(AQUI, 'organismo_v13ag.py'))}"
        f"  v13 {h16(os.path.join(RAIZ, 'organismo', 'organismo_v13.py'))}  script {h16(os.path.abspath(__file__))}")
    Th = 40000
    esc_h = {'base': dict(), 'invertir': dict(invertir_en=Th // 2), 'nuevo': dict(nuevo='C', nuevo_en=Th // 2)}
    log(f"1/2 IDENTIDAD semilla 1, 3 escenarios, T={Th} (9 simulaciones = 360 000 pasos).")
    ident = []
    for esc, kw in esc_h.items():
        a = v13.run(1, T=Th, **kw)
        for cual, kk in (('I1', dict(eta_pred=0.0, k_sorpresa=0.0)), ('I2', dict(eta_pred=0.03, k_sorpresa=0.0))):
            b = v13a.run(1, T=Th, **kw, **kk)
            dif = [k for k in a if N(a[k]) != N(b[k])]
            ident.append(dict(cual=cual, esc=esc, seed=1, identico=not dif, difieren=dif))
            log(f"    {cual} {esc:9s} {'IDENTICO' if not dif else 'DIFIERE ' + str(dif)}")
    log(f"  identicos {sum(x['identico'] for x in ident)}/{len(ident)}")
    log(f"2/2 UNA corrida V13+SORPRESA con inversion: T={T}, invertir_en={T_INV}, semilla 1 (200 000 pasos).")
    r = tarea(('T', 'V13+SORPRESA', 1))
    log(f"    t_ext_B {r['t_ext_B']}  recuperacion {r['recup']} pasos  censurado {r['censurado']}")
    log(f"    sorpresa_media por cuarto {r['sorpresa_media']}   error_pred por cuarto {r['error_pred']}")
    log(f"    eta_media por cuarto {r['eta_media']}   bocados por cuarto {r['bocados']}")
    log(f"    ventana +-{VENT}: sorpresa_pre {r['sorpresa_pre']} -> sorpresa_post {r['sorpresa_post']} | eta_pre {r['eta_pre']} -> eta_post {r['eta_post']} (n {r['n_pre']}/{r['n_post']})")
    log(f"    veneno_post {r['veneno_post']}  comida_post {r['comida_post']}  muertes {r['deaths']} (tras la inversion {r['deaths_post']})")
    log(f"    W {r['W']}   W_lenta {r['W_lenta']}   W_pred {r['W_pred']}   celdas {r['celdas']}  divisiones {r['splits']}")
    log("HUMO: numeros observados, sin ajustar nada. No son evidencia de la hipotesis (n=1); sirven para ver que el instrumento mide.")
    dj = os.path.join(RAIZ, 'datos', f'allostasis_humo_{stamp}.json')
    json.dump(dict(meta=dict(fecha=time.strftime('%Y-%m-%dT%H:%M:%S'), tipo='humo', T_identidad=Th, T=T, invertir_en=T_INV,
                             sha_preregistro=h16(os.path.join(AQUI, 'PREREGISTRO_allostasis.md')), sha_script=h16(os.path.abspath(__file__)),
                             sha_v13a=h16(os.path.join(AQUI, 'organismo_v13a.py')), sha_v13ag=h16(os.path.join(AQUI, 'organismo_v13ag.py')),
                             python=platform.python_version(), numpy=np.__version__),
                   identidades=ident, corrida=r), open(dj, 'w', encoding='utf-8'), ensure_ascii=False, default=str)
    log(f"datos -> {os.path.basename(dj)}  sha256_16 = {h16(dj)}")
    _log['f'].close()


# ---------------------------------------------------------------- principal
if __name__ == '__main__':
    if '--humo' in sys.argv:
        humo(); sys.exit(0)

    import multiprocessing as mp
    mp.set_start_method('spawn', force=True)
    import bateria_v13 as bv13
    desde = int(sys.argv[sys.argv.index('--desde') + 1]) if '--desde' in sys.argv else 1
    SEEDS = list(range(desde, desde + 10))
    stamp = time.strftime('%Y%m%d_%H%M%S')
    _log['f'] = open(os.path.join(RAIZ, 'datos', f'allostasis_s{SEEDS[0]}-{SEEDS[-1]}_{stamp}.log'), 'w', encoding='utf-8', newline='\n')
    pre = os.path.join(AQUI, 'PREREGISTRO_allostasis.md')
    log(f"ARRANQUE bloque 6 (RAMA): modelo de si mismo minimo. brazos {list(BRAZOS)}, semillas {SEEDS[0]}-{SEEDS[-1]}, T={T}, invertir_en={T_INV}. Pool({N_PARALELO}).")
    log("RAMA exploratoria: 10 semillas no cierran nada. Solo se mide, no se declara (regla 6).")
    log(f"sha preregistro {h16(pre)}  script {h16(os.path.abspath(__file__))}  constructor {h16(os.path.join(AQUI, 'construye_allostasis.py'))}")
    log(f"sha v13a {h16(os.path.join(AQUI, 'organismo_v13a.py'))}  v13ag {h16(os.path.join(AQUI, 'organismo_v13ag.py'))}"
        f"  v13 {h16(os.path.join(RAIZ, 'organismo', 'organismo_v13.py'))}  v13g {h16(os.path.join(RAIZ, 'experimentos', 'v13_dos_vias', 'organismo_v13g.py'))}"
        f"  bateria_v13 {h16(os.path.join(RAIZ, 'organismo', 'bateria_v13.py'))}  bateria_generaliza {h16(os.path.join(RAIZ, 'organismo', 'bateria_generaliza.py'))}")
    try:
        ps = subprocess.run(['powershell', '-NoProfile', '-Command',
                             "Get-CimInstance Win32_Process | Where-Object { $_.Name -like 'python*' } | ForEach-Object { \"$($_.ProcessId) $($_.CommandLine)\" }"],
                            capture_output=True, text=True, timeout=60).stdout.strip().splitlines()
    except Exception as e:
        ps = [f"(no se pudo listar: {e})"]
    log(f"REGLA 11 — procesos python vivos ({len(ps)}), este es pid {os.getpid()}")

    V = {}
    res_T, res_B, res_G = [], [], []
    with mp.Pool(N_PARALELO) as pool:
        # ---- 1/4 identidades
        ctrl = [('I', c, e, s) for c in ('I1', 'I2') for e in ESC_ID for s in SEMILLAS_ID] + [('I3', r, s) for r in REGLAS for s in (1, 2, 3)]
        log(f"ETAPA 1/4 — identidades I1 (apagado == v13), I2 (predictor sin modular == v13) e I3 (modo regla == v13g): {len(ctrl)} comprobaciones...")
        rc = pool.map(tarea, ctrl, chunksize=1)
        for cual in ('I1', 'I2', 'I3'):
            g = [x for x in rc if x['cual'] == cual]
            log(f"    {cual}: {sum(x['identico'] for x in g)}/{len(g)}")
            for x in g:
                if not x['identico']:
                    log(f"        DIFIERE {x['esc']} s{x['seed']}: {x['difieren']}")
        V['I1'] = all(x['identico'] for x in rc if x['cual'] == 'I1')
        V['I2'] = all(x['identico'] for x in rc if x['cual'] == 'I2')
        V['I3'] = all(x['identico'] for x in rc if x['cual'] == 'I3')
        V['G_a_IDENTIDAD'] = bool(V['I1'] and V['I2'] and V['I3'])
        if not V['G_a_IDENTIDAD']:
            log("*** GUARDA G-a FALLIDA: el instrumento no es v13 con las perillas apagadas (o el predictor toca la dinamica). Se para.")
            sys.exit(1)

        # ---- 2/4 experimento principal
        tr = [('T', b, s) for b in BRAZOS for s in SEEDS]
        log(f"ETAPA 2/4 — experimento principal: {len(tr)} corridas de {T} pasos...")
        for i, r in enumerate(pool.imap_unordered(tarea, tr, chunksize=1), 1):
            res_T.append(r)
            if i % 10 == 0 or i == len(tr):
                log(f"          {i}/{len(tr)}")

        # ---- 3/4 retencion
        if '--sin-bateria' not in sys.argv:
            tb = [('B', b, e, s) for b in BRAZOS for e in bv13.SEIS for s in SEEDS]
            log(f"ETAPA 3/4 — retencion M4 (los SEIS de bateria_v13, sus criterios): {len(tb)} corridas de {T_BAT} pasos...")
            for i, r in enumerate(pool.imap_unordered(tarea, tb, chunksize=1), 1):
                res_B.append(r)
                if i % 40 == 0 or i == len(tb):
                    log(f"          {i}/{len(tb)}")

        # ---- 4/4 generalizacion
        if '--sin-generaliza' not in sys.argv:
            tg = [('G', b, rg, s) for b in BRAZOS for rg in REGLAS for s in SEEDS]
            log(f"ETAPA 4/4 — generalizacion M5 (G1/G2 px0/azar, modo regla): {len(tg)} corridas de {T} pasos...")
            for i, r in enumerate(pool.imap_unordered(tarea, tg, chunksize=1), 1):
                res_G.append(r)
                if i % 20 == 0 or i == len(tg):
                    log(f"          {i}/{len(tg)}")

    # ---------------------------------------------------------------- analisis
    log("ANALISIS — guardas primero (regla: una guarda caida anula el contraste, no lo reinterpreta).")
    Gb = {b: {r['seed']: r for r in res_T if r['brazo'] == b} for b in BRAZOS}
    for b in BRAZOS:
        g = list(Gb[b].values())
        log(f"   {b:13s} recuperacion {mediana([r['recup'] for r in g])}  censuradas {sum(r['censurado'] for r in g)}/{len(g)}"
            f"  veneno_post {mediana([r['veneno_post'] for r in g])}  comida_post {mediana([r['comida_post'] for r in g])}"
            f"  muertes(post) {mediana([r['deaths'] for r in g])}({mediana([r['deaths_post'] for r in g])})"
            f"  eta_post {mediana([r['eta_post'] for r in g])}  sorpresa pre/post {mediana([r['sorpresa_pre'] for r in g])}/{mediana([r['sorpresa_post'] for r in g])}")
        for q in range(4):
            log(f"        Q{q+1}  sorpresa_media {mediana([r['sorpresa_media'][q] for r in g])}  error_pred {mediana([r['error_pred'][q] for r in g])}"
                f"  eta_media {mediana([r['eta_media'][q] for r in g])}  bocados {mediana([r['bocados'][q] for r in g])}")

    v13m = mediana([r['recup'] for r in Gb['V13'].values()])
    sorm = mediana([r['recup'] for r in Gb['V13+SORPRESA'].values()])
    ruim = mediana([r['recup'] for r in Gb['V13+RUIDO'].values()])
    cens = sum(r['censurado'] for r in Gb['V13'].values())
    V['G_c_MARGEN'] = bool(v13m is not None and 500 <= v13m <= T_INV - 1 and cens <= 2)
    log(f"   G-c margen: V13 recuperacion mediana {v13m}, censuradas {cens}/10 -> {'OK' if V['G_c_MARGEN'] else 'NO (M1 no sirve en este mundo; ERR y mundo nuevo)'}")

    # G-b sobre eta_media[Q3] = el cuarto INMEDIATAMENTE POSTERIOR a la inversion (50.000 pasos, ~190 bocados): ancho de
    # sobra para contener el retraso de la ventana barajada (<=10 bocados), luego compara CANTIDAD de aprendizaje, no promptitud.
    epS, epR = mediana([r['eta_media'][2] for r in Gb['V13+SORPRESA'].values()]), mediana([r['eta_media'][2] for r in Gb['V13+RUIDO'].values()])
    rz = razon(epR - 1.0 if epR is not None else None, epS - 1.0 if epS is not None else None)   # el exceso sobre eta, que es lo que se reparte
    V['G_b_etaQ3_SORPRESA'], V['G_b_etaQ3_RUIDO'], V['G_b_razon'] = epS, epR, rz
    V['G_b_LECTURA'] = ('limpio' if (rz is not None and rz >= 1.0) else 'valido' if (rz is not None and rz >= 0.95)
                        else 'inconcluso' if rz is not None else 'sin dato')
    log(f"   G-b (ENMIENDA 1+2) eta_media[Q3] SORPRESA {epS} vs RUIDO {epR}; razon del exceso {None if rz is None else round(rz, 4)} -> lectura del contraste: {V['G_b_LECTURA']}")
    log(f"        diagnostico de promptitud (ventana +-{VENT}): eta_post SORPRESA {mediana([r['eta_post'] for r in Gb['V13+SORPRESA'].values()])}"
        f" vs RUIDO {mediana([r['eta_post'] for r in Gb['V13+RUIDO'].values()])}  (NO es guarda: el retraso es justamente lo que el control introduce)")

    sp = [r['sorpresa_pre'] for r in Gb['V13+PRED'].values()]
    q12 = sum(1 for r in Gb['V13+PRED'].values() if r['sorpresa_media'][1] is not None and r['sorpresa_media'][0] is not None and r['sorpresa_media'][1] < r['sorpresa_media'][0])
    V['G_d_predictor_aprende'] = bool(q12 >= 7)
    log(f"   G-d: sorpresa_media Q2<Q1 en {q12}/10 -> {'OK' if V['G_d_predictor_aprende'] else 'NO'}")

    log("ANALISIS — predicciones preregistradas.")
    p1n = pareado(Gb['V13+SORPRESA'], Gb['V13'], SEEDS, 'recup')
    r1 = razon(sorm, v13m)
    P1 = bool(r1 is not None and r1 <= 0.70 and p1n >= 8)
    log(f"   P1 recuperacion SORPRESA/V13 = {None if r1 is None else round(r1, 3)} (<=0.70) y pareado {p1n}/10 (>=8)  -> {'OK' if P1 else 'NO'}")

    p2n = pareado(Gb['V13+SORPRESA'], Gb['V13+RUIDO'], SEEDS, 'recup')
    r2 = razon(ruim, v13m)
    P2 = bool(r2 is not None and r2 >= 0.85 and p2n >= 8 and V['G_b_LECTURA'] in ('limpio', 'valido'))
    log(f"   P2 RUIDO/V13 = {None if r2 is None else round(r2, 3)} (>=0.85), pareado SORPRESA<RUIDO {p2n}/10 (>=8), G-b {V['G_b_LECTURA']}  -> {'OK' if P2 else 'NO'}")

    # ENMIENDA 2: ademas del salto relativo se exige un salto ABSOLUTO >= 0.20, porque con sorpresa_pre = 0 el "x2" es gratis.
    # 0.20 sale de la estructura del mundo (al invertir, dE salta 1.2 = 0.8-(-0.4)), no de ningun numero observado.
    p3n = sum(1 for r in Gb['V13+PRED'].values()
              if r['sorpresa_pre'] is not None and r['sorpresa_post'] is not None
              and r['sorpresa_post'] >= 0.20 and r['sorpresa_post'] >= 2 * r['sorpresa_pre'])
    spm = mediana(sp)
    P3 = bool(spm is not None and spm <= 0.25 and p3n >= 8)
    log(f"   P3 (PRED) sorpresa_pre mediana {None if spm is None else round(spm, 4)} (<=0.25) y post>=max(0.20, 2xpre) en {p3n}/10 (>=8)  -> {'OK' if P3 else 'NO'}")

    ret = {}
    if res_B:
        for b in BRAZOS:
            ret[b] = {e: sum(1 for r in res_B if r['brazo'] == b and r['etapa'] == e and r['pasa']) for e in bv13.SEIS}
            log(f"   M4 {b:13s} " + "  ".join(f"{e} {ret[b][e]}/10" for e in bv13.SEIS))
        peor = [e for e in bv13.SEIS if ret['V13+SORPRESA'][e] < ret['V13'][e] - 1]
        wb = sum(1 for r in res_B if r['brazo'] == 'V13+SORPRESA' and r['etapa'] == 'E2I' and r['W']['B'] <= -2.8)
        P4 = bool(not peor and wb >= 9)
        log(f"   P4 retencion: etapas que pierden mas de 1 semilla {peor or 'ninguna'}; E2I W_B<=-2.8 en {wb}/10 (>=9)  -> {'OK' if P4 else 'NO'}")
    else:
        P4 = None; log("   P4 retencion: NO CORRIDA (--sin-bateria)")

    gen = {}
    if res_G:
        for b in BRAZOS:
            gen[b] = {rg: dict(acc=mediana([r['acc'] for r in res_G if r['brazo'] == b and r['regla'] == rg]),
                               ba=mediana([r['ba'] for r in res_G if r['brazo'] == b and r['regla'] == rg]),
                               cob=mediana([r['cobertura'] for r in res_G if r['brazo'] == b and r['regla'] == rg])) for rg in REGLAS}
            log(f"   M5 {b:13s} " + "  ".join(f"{rg}: G1 {gen[b][rg]['acc']} G2 {gen[b][rg]['ba']} cob {gen[b][rg]['cob']}" for rg in REGLAS))
        a_s, a_v, a_z = gen['V13+SORPRESA']['px0']['acc'], gen['V13']['px0']['acc'], gen['V13+SORPRESA']['azar']['acc']
        P5 = bool(a_s is not None and a_v is not None and a_z is not None and a_s >= 0.65 and a_s >= a_v - 0.10 and 0.35 <= a_z <= 0.65)
        log(f"   P5 generalizacion: G1 px0 SORPRESA {a_s} (>=0.65 y >= V13 {a_v} -0.10), azar {a_z} en [0.35,0.65]  -> {'OK' if P5 else 'NO'}")
    else:
        P5 = None; log("   P5 generalizacion: NO CORRIDA (--sin-generaliza)")

    vs, vv = mediana([r['veneno_post'] for r in Gb['V13+SORPRESA'].values()]), mediana([r['veneno_post'] for r in Gb['V13'].values()])
    cs, cv = mediana([r['comida_post'] for r in Gb['V13+SORPRESA'].values()]), mediana([r['comida_post'] for r in Gb['V13'].values()])
    P6 = bool(vs is not None and vv is not None and cs is not None and cv is not None and vs <= vv and cs >= 0.90 * cv)
    log(f"   P6 no gana por pasividad: veneno_post {vs} <= {vv} y comida_post {cs} >= 0.90x{cv}  -> {'OK' if P6 else 'NO'}")

    V.update(P1=P1, P2=P2, P3=P3, P4=P4, P5=P5, P6=P6, recup_V13=v13m, recup_SORPRESA=sorm, recup_RUIDO=ruim,
             pareado_SORPRESA_vs_V13=p1n, pareado_SORPRESA_vs_RUIDO=p2n, retencion=ret, generaliza=gen)
    if not V['G_c_MARGEN']:
        ver = "NULO por G-c (no hay margen o la medida esta censurada): hace falta otro mundo. ERR."
    elif not P1:
        ver = "REFUTADO: la sorpresa no acelera la recuperacion tras la inversion."
    elif not P6:
        ver = "NULO por P6: la 'recuperacion' es dejar de comer; M1 no mide lo que dice."
    elif not P2:
        ver = ("INCONCLUSO en P2 por G-b (" + V['G_b_LECTURA'] + "): hace falta el control V13+ETA_FIJA en semillas nuevas."
               if V['G_b_LECTURA'] == 'inconcluso' else
               "ACELERA, pero el control barajado tambien: lo que acelera es la CANTIDAD de actualizacion tras el cambio, no la sorpresa.")
    elif P4 is False or P5 is False:
        ver = "ACELERA y el control no, pero a COSTA de retencion o generalizacion: canje medido, no mejora."
    else:
        ver = "ACELERA, el control barajado no, y no cobra retencion ni generalizacion. RAMA: pide replica preregistrada en semillas nuevas antes de cualquier afirmacion."
    log(f"VEREDICTO (rama, 10 semillas, no cierra nada): {ver}")

    meta = dict(fecha=time.strftime('%Y-%m-%dT%H:%M:%S'), semillas=SEEDS, brazos=BRAZOS, T=T, invertir_en=T_INV, vent_sorpresa=VENT,
                veredicto=ver, veredictos=V, identidades=rc, procesos_python=ps,
                sha_preregistro=h16(pre), sha_script=h16(os.path.abspath(__file__)),
                sha_v13a=h16(os.path.join(AQUI, 'organismo_v13a.py')), sha_v13ag=h16(os.path.join(AQUI, 'organismo_v13ag.py')),
                sha_v13=h16(os.path.join(RAIZ, 'organismo', 'organismo_v13.py')),
                sha_bateria_v13=h16(os.path.join(RAIZ, 'organismo', 'bateria_v13.py')),
                sha_bateria_generaliza=h16(os.path.join(RAIZ, 'organismo', 'bateria_generaliza.py')),
                python=platform.python_version(), numpy=np.__version__)
    dj = os.path.join(RAIZ, 'datos', f'allostasis_s{SEEDS[0]}-{SEEDS[-1]}_{stamp}.json')
    json.dump(dict(meta=meta, principal=res_T, retencion=res_B, generaliza=res_G), open(dj, 'w', encoding='utf-8'), ensure_ascii=False, default=str)
    log(f"datos -> {os.path.basename(dj)}  sha256_16 = {h16(dj)}")
    _log['f'].close()
