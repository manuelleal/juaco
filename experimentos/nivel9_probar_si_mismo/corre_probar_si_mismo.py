"""C-P1 — ejecuta PREREGISTRO_probar_si_mismo.md: la sorpresa sobre SI MISMO entra en la BOCA (ganas de probar), no
en eta, contra la inversion de regla en T/2. REGLA 10: log desde el arranque, con fsync.

    python experimentos/nivel9_probar_si_mismo/corre_probar_si_mismo.py [--desde N] [--sin-bateria] [--sin-generaliza]
    python experimentos/nivel9_probar_si_mismo/corre_probar_si_mismo.py --humo    (UN proceso, sin Pool: lo corre el disenador)

DOSIS (PREREGISTRO_dosis_dE.md, 18 sep 2026): --brazos V13,dE3,dE5 fija QUE brazos pasan por 2/5 y 3/5 (por
defecto, los ocho de siempre); --baterias V13,dE3,dE5 hace lo mismo para 4/5 y 5/5 (ya existia, ENMIENDA 2). Con
--brazos reducido el veredicto generico P1-P7 no se calcula (harian falta brazos que no corrieron): se listan
medianas/pareado crudos y el veredicto de la dosis lo calcula corre_dosis_dE.py con los umbrales del preregistro.

Etapas con Pool (las corre el COORDINADOR, reglas 3 y 11):
  1/5 identidades J1 (apagado == v13), J2 (las lecturas SOLO MIDEN == v13), J3 (== v13s: continuidad con la
      mini-prueba) y J4 (modo regla == v13g). Si alguna no es 100 %, ABORTA.
  2/5 principal: 5 brazos x 20 semillas, T=200000, invertir_en=100000
  3/5 MOMENTO: 20 corridas con la traza de SELF-TEST de SU MISMA semilla, desplazada un cuarto de corrida
  4/5 retencion M5: los SEIS de organismo/bateria_v13.py con SUS criterios, 3 brazos x 20 semillas
  5/5 generalizacion M6: G1/G2 px0/azar con organismo_v13pg.py (formula copiada de organismo/bateria_generaliza.py)

20 semillas no cierran un nivel del brief: cierran o refutan ESTE mecanismo, y piden replica en 61-80.
Vocabulario (regla 6): "automodelo", "sorpresa sobre si mismo" y "ganas de probar" son las tres cantidades del
preregistro, seccion 2. Nada mas.
"""
import sys, os, json, time, hashlib, platform, subprocess
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
import numpy as np

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
sys.path[:0] = [AQUI, os.path.join(RAIZ, 'organismo'), os.path.join(RAIZ, 'experimentos', 'v13_dos_vias'),
                os.path.join(RAIZ, 'experimentos', 'creacion_C')]

T = 200000
T_INV = T // 2
T_BAT = 100000              # el T por defecto de bateria_v13
NT = 2000                   # cubetas de la traza: T/NT = 100 pasos por cubeta
DESFASE = NT // 4           # un CUARTO de corrida (50 000 pasos). Ver preregistro, seccion 5
K_TEST = 10.0
N_PARALELO = 14
N_SEM = 20
REGLAS = ['px0', 'azar']

BRAZOS = {
    'V13':       dict(),
    'SELF-TEST': dict(eta_b=0.03, ema_auto=0.05, k_test=K_TEST, buf_auto=1000, n_traza=NT),
    'CONST-a':   dict(test_fijo=0.173),
    'CONST-b':   dict(test_fijo=0.31),
    'dE-TEST':   dict(eta_pred=0.03, ema_pred=0.05, k_testE=K_TEST),
    'MOMENTO':   dict(k_testM=K_TEST, desfase=DESFASE, n_traza=NT),   # + traza_ext, que se inyecta en la etapa 3/5
    # ENMIENDA 2 (serie 81-100): dos formas de quitarle el suelo al sesgo del automodelo. Ver la enmienda: el humo de
    # diseno REFUTA las dos (empeoran la razon Q2/Q3 y cuestan recuperacion); van como DIAGNOSTICO, sin criterio.
    'SELF-TEST-R': dict(eta_b=0.03, ema_auto=0.05, k_test=K_TEST, buf_auto=1000, n_traza=NT, resta_cota=True),
    'SELF-TEST-L': dict(eta_b=0.03, ema_auto=0.05, k_test=K_TEST, buf_auto=1000, n_traza=NT, resta_lenta=True),
}
BRAZOS_ACTIVOS = list(BRAZOS)   # que brazos pasan por 2/5 (principal) y 3/5 (MOMENTO, si esta pedido); --brazos lo cambia
# DOSIS (PREREGISTRO_dosis_dE.md, 18 sep 2026): mismo mecanismo de dE-TEST con ganancia menor (k_testE=3 / 5 en vez
# de 10). NO entran en ninguna corrida salvo que se pidan por nombre con --brazos (el default de BRAZOS_ACTIVOS ya
# quedo fijado arriba, ANTES de esta linea, con los ocho brazos de siempre: sin --brazos nada cambia).
BRAZOS['dE3'] = dict(eta_pred=0.03, ema_pred=0.05, k_testE=3.0)
BRAZOS['dE5'] = dict(eta_pred=0.03, ema_pred=0.05, k_testE=5.0)
SIN_TRAZA = [b for b in BRAZOS_ACTIVOS if b != 'MOMENTO']
BRAZOS_BAT = ['V13', 'SELF-TEST', 'CONST-b']     # preregistro, seccion 5: P5/P6 preguntan por la hipotesis
# --baterias V13,dE-TEST,...   cambia que brazos pasan por retencion (4/5) y generalizacion (5/5). ENMIENDA 2.
# --brazos V13,dE3,dE5,...     cambia que brazos pasan por 2/5 y 3/5 (DOSIS); ver BRAZOS_ACTIVOS y REQ_ANALISIS abajo.

APAGADO = dict(eta_b=0.0, k_auto=0.0, k_test=0.0, test_fijo=0.0, eta_e=0.0, eta_pred=0.0, k_testE=0.0, n_traza=0)
SOLO_MIDE = dict(eta_b=0.03, k_auto=0.0, ema_auto=0.05, k_test=0.0, test_fijo=0.0, eta_e=0.05, h_pred=100,
                 eta_pred=0.03, ema_pred=0.05, k_testE=0.0, n_traza=NT)
ESC_ID = {'base': dict(), 'invertir': dict(invertir_en=None), 'nuevo': dict(nuevo='C', nuevo_en=None)}
SEMILLAS_ID = [1, 2, 3]

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


# ---------------------------------------------------------------- guardias None (copiadas del runner del bloque 6)
def mediana(xs):
    xs = [x for x in xs if x is not None]
    return float(np.median(xs)) if xs else None


def pareado(a, b, semillas, clave, menor_es_mejor=True):
    """En cuantas semillas a es mejor que b. None cuenta como NO mejor (nunca como victoria)."""
    n = 0
    for s in semillas:
        x, y = a.get(s, {}).get(clave), b.get(s, {}).get(clave)
        if x is None or y is None:
            continue
        n += (x < y) if menor_es_mejor else (x > y)
    return n


def razon(x, y):
    if x is None or y is None or y == 0:
        return None
    return x / y


def rec_pasos(o):
    """Recuperacion = t_ext_B - invertir_en, censurada a T - invertir_en si nunca ocurre."""
    te = o.get('t_ext_B')
    return (T - T_INV) if te is None else (te - T_INV)


def resumen_T(brazo, seed, r):
    return dict(tipo='T', brazo=brazo, seed=seed, t_ext_B=r['t_ext_B'], recup=rec_pasos(r),
                censurado=r['t_ext_B'] is None,
                veneno_post=r['mord_post']['veneno'], comida_post=r['mord_post']['comida'],
                deaths=r['deaths'], deaths_post=r['deaths_post'], W=r['W'], W_lenta=r['W_lenta'],
                sesgo_boca=r['sesgo_boca'], sorpresa_auto=r['sorpresa_auto'], encuentros=r['encuentros'],
                eta_media=r['eta_media'], bocados_q=r['bocados_q'], sbar=r['sbar'], sbarE=r['sbarE'],
                auto_banda=r['auto_banda'], auto_n=r['auto_n'], auto_ll=r['auto_ll'], auto_ba=r['auto_ba'],
                Wbh=r['Wbh'], Whh=r['Whh'], splits=r['splits'], celdas=r['celdas'],
                t_primer_sesgo=r['t_primer_sesgo'],
                latencia_sesgo=(None if r['t_primer_sesgo'] is None else r['t_primer_sesgo'] - T_INV),
                enc_post_hasta_sesgo=r['enc_post_hasta_sesgo'], mord_post_hasta_sesgo=r['mord_post_hasta_sesgo'],
                fbar=r['fbar'], sbarL=r['sbarL'],
                traza_suma=(round(float(np.sum(r['traza_s'])), 6) if r['traza_s'] else None))


# ---------------------------------------------------------------- tareas
def tarea(args):
    tipo = args[0]

    if tipo == 'J':                                   # J1 / J2: v13p apagado / con las lecturas encendidas == v13
        _, cual, esc, seed, Ti = args
        import organismo_v13 as v13, organismo_v13p as v13p
        kw = {k: (Ti // 2 if v is None else v) for k, v in ESC_ID[esc].items()}
        a = v13.run(seed, T=Ti, **kw)
        b = v13p.run(seed, T=Ti, **kw, **(APAGADO if cual == 'J1' else SOLO_MIDE))
        dif = [k for k in a if N(a[k]) != N(b[k])]
        return dict(tipo='J', cual=cual, esc=esc, seed=seed, identico=not dif, difieren=dif)

    if tipo == 'J3':                                  # continuidad: v13p(SELF-TEST) == v13s(SELF-TEST)
        _, esc, seed, Ti = args
        import organismo_v13s as v13s, organismo_v13p as v13p
        kw = {k: (Ti // 2 if v is None else v) for k, v in ESC_ID[esc].items()}
        st = dict(BRAZOS['SELF-TEST'])
        a = v13s.run(seed, T=Ti, **kw, **{k: v for k, v in st.items() if k != 'n_traza'})
        b = v13p.run(seed, T=Ti, **kw, **st)
        # ENMIENDA 2: `sesgo_boca` es clave de REPORTE, no de conducta. organismo_v13s la acumulaba con el s_barra YA
        # actualizado de ese encuentro; v13p acumula el sesgo REALMENTE aplicado (el causal). J3 compara CONDUCTA e
        # informa aparte el maximo de la diferencia de reporte.
        REPORTE = ('sesgo_boca',)
        dif = [k for k in a if k not in REPORTE and N(a[k]) != N(b[k])]
        dsb = max(abs(float(x) - float(y)) for x, y in zip(a['sesgo_boca'], b['sesgo_boca']))
        return dict(tipo='J', cual='J3', esc=esc, seed=seed, identico=not dif, difieren=dif,
                    claves_reporte=list(REPORTE), max_dif_reporte=round(dsb, 6))

    if tipo == 'J4':                                  # modo regla: v13pg apagado == v13g
        _, regla, seed, Ti = args
        import organismo_v13g as g, organismo_v13pg as pg
        kw = dict(T=Ti, mundo='regla', regla=regla, eta_s=0.015, puerta=3)
        a = g.run(seed, **kw)
        b = pg.run(seed, **kw, **APAGADO)
        dif = [k for k in a if N(a[k]) != N(b[k])]
        return dict(tipo='J', cual='J4', esc=regla, seed=seed, identico=not dif, difieren=dif)

    if tipo == 'T':                                   # principal (todos menos MOMENTO)
        _, brazo, seed = args
        import organismo_v13p as v13p
        r = v13p.run(seed, T=T, invertir_en=T_INV, **BRAZOS[brazo])
        out = resumen_T(brazo, seed, r)
        if brazo == 'SELF-TEST':
            out['traza_s'] = r['traza_s']             # la necesita MOMENTO; NO se vuelca al JSON final
        return out

    if tipo == 'M':                                   # MOMENTO: la traza de SELF-TEST de SU MISMA semilla, desplazada
        _, seed, traza = args
        import organismo_v13p as v13p
        r = v13p.run(seed, T=T, invertir_en=T_INV, traza_ext=list(traza), **BRAZOS['MOMENTO'])
        out = resumen_T('MOMENTO', seed, r)
        out['traza_inyectada_suma'] = round(float(np.sum(traza)), 6)
        return out

    if tipo == 'B':                                   # M5: retencion con los criterios de bateria_v13
        _, brazo, etapa, seed = args
        import organismo_v13p as v13p, bateria_v13 as bv13
        kw = dict(bv13.ETAPAS[etapa]); kw.update(BRAZOS[brazo])
        r = v13p.run(seed, T=T_BAT, **kw)
        crit = {nombre: bool(f(r)) for nombre, f in bv13.CRIT[etapa].items()}
        return dict(tipo='B', brazo=brazo, etapa=etapa, seed=seed, crit=crit, pasa=all(crit.values()),
                    W=r['W'], celdas=r['celdas'], splits=r['splits'], deaths=r['deaths'])

    # G: generalizacion. Formula G1/G2/cobertura COPIADA de organismo/bateria_generaliza.py (46772f5a582872c8).
    _, brazo, regla, seed = args
    import organismo_v13pg as pg
    r = pg.run(seed, T=T, mundo='regla', regla=regla, eta_s=0.015, puerta=3, **BRAZOS[brazo])
    vr = pg.split_regla(seed, regla)[3]
    test = r['test']
    f = [1.0 if r['W_apriori'][k] > 0 else (0.5 if r['W_apriori'][k] == 0 else 0.0) for k in test if vr[k] == 'comida']
    p = [1.0 if r['W_apriori'][k] < 0 else (0.5 if r['W_apriori'][k] == 0 else 0.0) for k in test if vr[k] == 'veneno']
    pf = [r['primer'][k]['pb'] for k in test if r['primer'][k] is not None and vr[k] == 'comida']
    pp = [1 - r['primer'][k]['pb'] for k in test if r['primer'][k] is not None and vr[k] == 'veneno']
    return dict(tipo='G', brazo=brazo, regla=regla, seed=seed,
                acc=(0.5 * float(np.mean(f)) + 0.5 * float(np.mean(p))) if (f and p) else None,
                ba=(0.5 * float(np.mean(pf)) + 0.5 * float(np.mean(pp))) if (pf and pp) else None,
                cobertura=sum(v is not None for v in r['primer'].values()), splits=r['splits'],
                celdas=r['celdas'], deaths=r['deaths'])


SHAS = lambda: dict(
    preregistro=h16(os.path.join(AQUI, 'PREREGISTRO_probar_si_mismo.md')),
    script=h16(os.path.abspath(__file__)),
    constructor=h16(os.path.join(AQUI, 'construye_probar.py')),
    constructor_automodelo=h16(os.path.join(RAIZ, 'experimentos', 'creacion_C', 'construye_selfmodel.py')),
    v13p=h16(os.path.join(AQUI, 'organismo_v13p.py')),
    v13pg=h16(os.path.join(AQUI, 'organismo_v13pg.py')),
    v13s=h16(os.path.join(RAIZ, 'experimentos', 'creacion_C', 'organismo_v13s.py')),
    v13=h16(os.path.join(RAIZ, 'organismo', 'organismo_v13.py')),
    v13g=h16(os.path.join(RAIZ, 'experimentos', 'v13_dos_vias', 'organismo_v13g.py')),
    bateria_v13=h16(os.path.join(RAIZ, 'organismo', 'bateria_v13.py')),
    bateria_generaliza=h16(os.path.join(RAIZ, 'organismo', 'bateria_generaliza.py')))


# ---------------------------------------------------------------- humo (UN proceso, sin Pool)
def humo():
    stamp = time.strftime('%Y%m%d_%H%M%S')
    _log['f'] = open(os.path.join(RAIZ, 'datos', f'probar_si_mismo_humo_{stamp}.log'), 'w', encoding='utf-8', newline='\n')
    log("HUMO del disenador, UN proceso, sin Pool (regla 3). Preregistro PREREGISTRO_probar_si_mismo.md, seccion 11.")
    log("Semilla 1 (ya vista en la mini-prueba): NINGUNA de las 41-60 del experimento queda expuesta.")
    for k, v in SHAS().items():
        log(f"    sha {k:24s} {v}")
    Ti = 10000
    log(f"1/2 IDENTIDADES J1, J2, J3 (3 escenarios) y J4 (2 reglas), semilla 1, T={Ti}.")
    ident, t1 = [], time.time()
    for esc in ESC_ID:
        for cual in ('J1', 'J2'):
            x = tarea(('J', cual, esc, 1, Ti)); ident.append(x)
            log(f"    {cual} {esc:9s} {'IDENTICO' if x['identico'] else 'DIFIERE ' + str(x['difieren'])}")
        x = tarea(('J3', esc, 1, Ti)); ident.append(x)
        log(f"    J3 {esc:9s} {'IDENTICO en conducta' if x['identico'] else 'DIFIERE ' + str(x['difieren'])}"
            f"   (clave de reporte {x['claves_reporte']}: max |dif| {x['max_dif_reporte']})")
    for regla in REGLAS:
        x = tarea(('J4', regla, 1, Ti)); ident.append(x)
        log(f"    J4 {regla:9s} {'IDENTICO' if x['identico'] else 'DIFIERE ' + str(x['difieren'])}")
    log(f"  identicos {sum(x['identico'] for x in ident)}/{len(ident)}   ({round(time.time()-t1,1)} s)")

    log(f"2/2 UNA corrida SELF-TEST + su MOMENTO: T={T}, invertir_en={T_INV}, semilla 1 (2 x 200 000 pasos).")
    t2 = time.time(); a = tarea(('T', 'SELF-TEST', 1)); dt_a = time.time() - t2
    log(f"    SELF-TEST  {round(dt_a,1)} s/corrida   t_ext_B {a['t_ext_B']}  recuperacion {a['recup']}  censurado {a['censurado']}")
    log(f"        sesgo_boca por cuarto {a['sesgo_boca']}   sorpresa_auto {a['sorpresa_auto']}   encuentros {a['encuentros']}")
    log(f"        veneno_post {a['veneno_post']}  comida_post {a['comida_post']}  muertes {a['deaths']} (post {a['deaths_post']})")
    log(f"        banda {a['auto_banda']}  n [dentro,fuera] {a['auto_n']}  ll dentro [S,M,H,ORACULO] {[a['auto_ll'][i][0] for i in range(4)]}")
    log(f"        Wbh {a['Wbh']}  Whh(control) {a['Whh']}  W {a['W']}  suma de la traza {a['traza_suma']}")
    t3 = time.time(); b = tarea(('M', 1, a['traza_s'])); dt_b = time.time() - t3
    log(f"    MOMENTO    {round(dt_b,1)} s/corrida   t_ext_B {b['t_ext_B']}  recuperacion {b['recup']}  censurado {b['censurado']}")
    log(f"        sesgo_boca por cuarto {b['sesgo_boca']}   veneno_post {b['veneno_post']}  muertes {b['deaths']}")
    dsum = abs((b['traza_inyectada_suma'] or 0) - (a['traza_suma'] or 0))
    log(f"    G-d masa de la traza: SELF-TEST {a['traza_suma']} vs inyectada {b['traza_inyectada_suma']}  |dif| {dsum}  -> {'OK' if dsum < 1e-9 else 'FALLA'}")
    log("HUMO: numeros observados, sin ajustar nada. n=1 y semilla vista: NO son evidencia; sirven para ver que el instrumento mide.")
    a = {k: v for k, v in a.items() if k != 'traza_s'}
    dj = os.path.join(RAIZ, 'datos', f'probar_si_mismo_humo_{stamp}.json')
    json.dump(dict(meta=dict(fecha=time.strftime('%Y-%m-%dT%H:%M:%S'), tipo='humo', T_identidad=Ti, T=T,
                             invertir_en=T_INV, n_traza=NT, desfase=DESFASE, shas=SHAS(),
                             segundos_por_corrida=dict(self_test=round(dt_a, 2), momento=round(dt_b, 2)),
                             python=platform.python_version(), numpy=np.__version__),
                   identidades=ident, self_test=a, momento=b), open(dj, 'w', encoding='utf-8'),
              ensure_ascii=False, default=str)
    log(f"datos -> {os.path.basename(dj)}  sha256_16 = {h16(dj)}")
    _log['f'].close()


# ---------------------------------------------------------------- principal
if __name__ == '__main__':
    if '--humo' in sys.argv:
        humo(); sys.exit(0)

    import multiprocessing as mp
    mp.set_start_method('spawn', force=True)
    import bateria_v13 as bv13
    desde = int(sys.argv[sys.argv.index('--desde') + 1]) if '--desde' in sys.argv else 41
    if '--baterias' in sys.argv:                      # ENMIENDA 2: la lista de brazos que pasan por M5 y M6
        BRAZOS_BAT = [b.strip() for b in sys.argv[sys.argv.index('--baterias') + 1].split(',') if b.strip()]
        malos = [b for b in BRAZOS_BAT if b not in BRAZOS]
        if malos:
            raise SystemExit(f"--baterias: brazo(s) desconocido(s) {malos}. Validos: {list(BRAZOS)}")
        if 'MOMENTO' in BRAZOS_BAT:
            raise SystemExit("--baterias: MOMENTO no puede correr en las baterias (necesita una traza de ESTE mundo).")
    if '--brazos' in sys.argv:                        # DOSIS (PREREGISTRO_dosis_dE.md): que brazos pasan por 2/5 y 3/5
        BRAZOS_ACTIVOS = [b.strip() for b in sys.argv[sys.argv.index('--brazos') + 1].split(',') if b.strip()]
        malos = [b for b in BRAZOS_ACTIVOS if b not in BRAZOS]
        if malos:
            raise SystemExit(f"--brazos: brazo(s) desconocido(s) {malos}. Validos: {list(BRAZOS)}")
        if 'V13' not in BRAZOS_ACTIVOS:
            raise SystemExit("--brazos: V13 es la referencia obligatoria (G-c, P1, P2 la necesitan).")
        if 'MOMENTO' in BRAZOS_ACTIVOS and 'SELF-TEST' not in BRAZOS_ACTIVOS:
            raise SystemExit("--brazos: MOMENTO necesita la traza de SELF-TEST en la misma corrida.")
        SIN_TRAZA = [b for b in BRAZOS_ACTIVOS if b != 'MOMENTO']
    SEEDS = list(range(desde, desde + N_SEM))
    stamp = time.strftime('%Y%m%d_%H%M%S')
    _log['f'] = open(os.path.join(RAIZ, 'datos', f'probar_si_mismo_s{SEEDS[0]}-{SEEDS[-1]}_{stamp}.log'),
                     'w', encoding='utf-8', newline='\n')
    log(f"ARRANQUE C-P1 'probar cuando no me reconozco': brazos {BRAZOS_ACTIVOS}, semillas {SEEDS[0]}-{SEEDS[-1]}, "
        f"T={T}, invertir_en={T_INV}, n_traza={NT}, desfase={DESFASE}. Pool({N_PARALELO}).")
    log("20 semillas no cierran un nivel del brief: cierran o refutan ESTE mecanismo, y piden replica en 61-80.")
    for k, v in SHAS().items():
        log(f"    sha {k:24s} {v}")
    try:
        ps = subprocess.run(['powershell', '-NoProfile', '-Command',
                             "Get-CimInstance Win32_Process | Where-Object { $_.Name -like 'python*' } | ForEach-Object { \"$($_.ProcessId) $($_.CommandLine)\" }"],
                            capture_output=True, text=True, timeout=60).stdout.strip().splitlines()
    except Exception as e:
        ps = [f"(no se pudo listar: {e})"]
    log(f"REGLA 11 — procesos python vivos ({len(ps)}), este es pid {os.getpid()}")

    V = {}
    res_T, res_B, res_G = [], [], []
    trazas = {}
    with mp.Pool(N_PARALELO) as pool:
        # ---- 1/5 identidades (guarda G-a: si falla, se ABORTA)
        ctrl = ([('J', c, e, s, 10000) for c in ('J1', 'J2') for e in ESC_ID for s in SEMILLAS_ID]
                + [('J3', e, s, 10000) for e in ESC_ID for s in SEMILLAS_ID]
                + [('J4', r, s, 10000) for r in REGLAS for s in SEMILLAS_ID])
        log(f"ETAPA 1/5 — identidades J1 (apagado == v13), J2 (las lecturas SOLO MIDEN), J3 (== v13s) y J4 (modo regla == v13g): {len(ctrl)} comprobaciones...")
        rc = pool.map(tarea, ctrl, chunksize=1)
        for cual in ('J1', 'J2', 'J3', 'J4'):
            g = [x for x in rc if x['cual'] == cual]
            extra = ("   (clave de reporte ['sesgo_boca'] excluida; max |dif| "
                     f"{max(x.get('max_dif_reporte', 0.0) for x in g)})" if cual == 'J3' else "")
            log(f"    {cual}: {sum(x['identico'] for x in g)}/{len(g)}{extra}")
            for x in g:
                if not x['identico']:
                    log(f"        DIFIERE {x['esc']} s{x['seed']}: {x['difieren']}")
            V[cual] = all(x['identico'] for x in g)
        V['G_a_IDENTIDAD'] = bool(all(V[c] for c in ('J1', 'J2', 'J3', 'J4')))
        if not V['G_a_IDENTIDAD']:
            log("*** GUARDA G-a FALLIDA: el instrumento no es v13 con las perillas apagadas, o las lecturas tocan la dinamica. Se para.")
            sys.exit(1)

        # ---- 2/5 principal (todos menos MOMENTO)
        tr = [('T', b, s) for b in SIN_TRAZA for s in SEEDS]
        log(f"ETAPA 2/5 — principal: {len(tr)} corridas de {T} pasos ({len(SIN_TRAZA)} brazos x {len(SEEDS)} semillas)...")
        for i, r in enumerate(pool.imap_unordered(tarea, tr, chunksize=1), 1):
            if r['brazo'] == 'SELF-TEST':
                trazas[r['seed']] = r.pop('traza_s')
            res_T.append(r)
            if i % 10 == 0 or i == len(tr):
                log(f"          {i}/{len(tr)}")

        # ---- 3/5 MOMENTO (necesita la traza de SELF-TEST de su misma semilla; se omite si no esta en --brazos)
        if 'MOMENTO' in BRAZOS_ACTIVOS:
            tm = [('M', s, trazas[s]) for s in SEEDS]
            log(f"ETAPA 3/5 — MOMENTO: {len(tm)} corridas de {T} pasos con la traza de SELF-TEST desplazada {DESFASE} cubetas (= {DESFASE*T//NT} pasos)...")
            for i, r in enumerate(pool.imap_unordered(tarea, tm, chunksize=1), 1):
                res_T.append(r)
                if i % 10 == 0 or i == len(tm):
                    log(f"          {i}/{len(tm)}")
        else:
            log("ETAPA 3/5 — MOMENTO: omitida (no esta en --brazos).")

        # ---- 4/5 retencion
        if '--sin-bateria' not in sys.argv:
            tb = [('B', b, e, s) for b in BRAZOS_BAT for e in bv13.SEIS for s in SEEDS]
            log(f"ETAPA 4/5 — retencion M5 (los SEIS de bateria_v13, sus criterios), brazos {BRAZOS_BAT}: {len(tb)} corridas de {T_BAT} pasos...")
            for i, r in enumerate(pool.imap_unordered(tarea, tb, chunksize=1), 1):
                res_B.append(r)
                if i % 40 == 0 or i == len(tb):
                    log(f"          {i}/{len(tb)}")

        # ---- 5/5 generalizacion
        if '--sin-generaliza' not in sys.argv:
            tg = [('G', b, rg, s) for b in BRAZOS_BAT for rg in REGLAS for s in SEEDS]
            log(f"ETAPA 5/5 — generalizacion M6 (G1/G2 px0/azar), brazos {BRAZOS_BAT}: {len(tg)} corridas de {T} pasos...")
            for i, r in enumerate(pool.imap_unordered(tarea, tg, chunksize=1), 1):
                res_G.append(r)
                if i % 20 == 0 or i == len(tg):
                    log(f"          {i}/{len(tg)}")

    # ---------------------------------------------------------------- analisis
    # REQ_ANALISIS: brazos que P1-P7/M5/M6 referencian por NOMBRE (guardas G-b/G-d incluidas). Con --brazos
    # completo (default) esto es True y el bloque de siempre corre SIN TOCAR; DOSIS (--brazos reducido) entra
    # por la rama nueva, mas simple, que nunca inventa un veredicto P1-P7 con brazos que no corrieron.
    REQ_ANALISIS = {'V13', 'SELF-TEST', 'CONST-a', 'CONST-b', 'MOMENTO', 'dE-TEST'}
    if REQ_ANALISIS <= set(BRAZOS_ACTIVOS):
        log("ANALISIS — guardas primero (regla: una guarda caida anula el contraste, no lo reinterpreta).")
        Gb = {b: {r['seed']: r for r in res_T if r['brazo'] == b} for b in BRAZOS_ACTIVOS}
        for b in BRAZOS_ACTIVOS:
            g = list(Gb[b].values())
            log(f"   {b:10s} recuperacion {mediana([r['recup'] for r in g])}  censuradas {sum(r['censurado'] for r in g)}/{len(g)}"
                f"  veneno_post {mediana([r['veneno_post'] for r in g])}  comida_post {mediana([r['comida_post'] for r in g])}"
                f"  muertes(post) {mediana([r['deaths'] for r in g])}({mediana([r['deaths_post'] for r in g])})"
                f"  bocados {mediana([sum(r['bocados_q']) for r in g])}")
            log(f"        sesgo_boca por cuarto {[mediana([r['sesgo_boca'][q] for r in g]) for q in range(4)]}"
                f"   sorpresa_auto {[mediana([r['sorpresa_auto'][q] for r in g]) for q in range(4)]}")
            q2q3 = mediana([r['sesgo_boca'][1] / r['sesgo_boca'][2] for r in g
                            if r['sesgo_boca'][1] is not None and r['sesgo_boca'][2]])
            log(f"        [ENMIENDA 2] razon Q2/Q3 {None if q2q3 is None else round(q2q3,3)}"
                f"   latencia del primer sesgo {mediana([r['latencia_sesgo'] for r in g])} pasos"
                f"   (encuentros {mediana([r['enc_post_hasta_sesgo'] for r in g])}, bocados {mediana([r['mord_post_hasta_sesgo'] for r in g])})"
                f"   sin sesgo nunca {sum(r['latencia_sesgo'] is None for r in g)}/{len(g)}")

        v13m = mediana([r['recup'] for r in Gb['V13'].values()])
        stm = mediana([r['recup'] for r in Gb['SELF-TEST'].values()])
        cens = sum(r['censurado'] for r in Gb['V13'].values())
        V['G_c_MARGEN'] = bool(v13m is not None and 500 <= v13m <= T_INV - 1 and cens <= 4)
        log(f"   G-c margen: V13 recuperacion mediana {v13m}, censuradas {cens}/{N_SEM} -> "
            f"{'OK' if V['G_c_MARGEN'] else 'NO (M1 no sirve en este mundo; ERR y mundo nuevo)'}")

        # G-b: la CANTIDAD de sesgo se mide, no se supone (razon de los sesgos de Q3 contra SELF-TEST)
        q3 = {b: mediana([r['sesgo_boca'][2] for r in Gb[b].values()]) for b in BRAZOS_ACTIVOS}
        rz = {b: razon(q3[b], q3['SELF-TEST']) for b in ('CONST-a', 'CONST-b', 'MOMENTO', 'dE-TEST')}
        def lectura(x):
            return 'limpio' if (x is not None and x >= 1.0) else 'valido' if (x is not None and x >= 0.95) else \
                   'inconcluso' if x is not None else 'sin dato'
        V['G_b_sesgoQ3'], V['G_b_razon'] = q3, rz
        V['G_b_LECTURA'] = {b: lectura(rz[b]) for b in rz}
        log(f"   G-b sesgo_boca[Q3] por brazo {[(b, None if q3[b] is None else round(q3[b],4)) for b in BRAZOS_ACTIVOS]}")
        log(f"        razon contra SELF-TEST {[(b, None if rz[b] is None else round(rz[b],3), V['G_b_LECTURA'][b]) for b in rz]}")

        # G-d: el desplazamiento circular conserva la masa exactamente
        dmax = max([abs((r.get('traza_inyectada_suma') or 0) - (Gb['SELF-TEST'].get(r['seed'], {}).get('traza_suma') or 0))
                    for r in Gb['MOMENTO'].values()] or [None])
        V['G_d_masa'] = bool(dmax is not None and dmax < 1e-9)
        log(f"   G-d masa de la traza de MOMENTO == la de SELF-TEST: |dif| max {dmax} -> {'OK' if V['G_d_masa'] else 'NO (control mal construido, ERR)'}")

        log("ANALISIS — predicciones preregistradas.")
        p1n = pareado(Gb['SELF-TEST'], Gb['V13'], SEEDS, 'recup'); r1 = razon(stm, v13m)
        P1 = bool(r1 is not None and r1 <= 0.60 and p1n >= 14)
        log(f"   P1 recuperacion SELF-TEST/V13 = {None if r1 is None else round(r1,3)} (<=0.60) y pareado {p1n}/{N_SEM} (>=14)  -> {'OK' if P1 else 'NO'}")

        pa = pareado(Gb['SELF-TEST'], Gb['CONST-a'], SEEDS, 'recup')
        pb_ = pareado(Gb['SELF-TEST'], Gb['CONST-b'], SEEDS, 'recup')
        P2 = bool(pa >= 14 and pb_ >= 14)
        log(f"   P2 no es la CANTIDAD: SELF-TEST < CONST-a {pa}/{N_SEM} y < CONST-b {pb_}/{N_SEM} (>=14 cada uno; medianas "
            f"{mediana([r['recup'] for r in Gb['CONST-a'].values()])} / {mediana([r['recup'] for r in Gb['CONST-b'].values()])})  -> {'OK' if P2 else 'NO'}")

        pm = pareado(Gb['SELF-TEST'], Gb['MOMENTO'], SEEDS, 'recup')
        P3 = bool(pm >= 14)
        log(f"   P3 es el MOMENTO: SELF-TEST < MOMENTO {pm}/{N_SEM} (>=14; mediana MOMENTO {mediana([r['recup'] for r in Gb['MOMENTO'].values()])})  -> {'OK' if P3 else 'NO'}")

        p4n = sum(1 for r in Gb['SELF-TEST'].values()
                  if r['sesgo_boca'][1] is not None and r['sesgo_boca'][2] is not None and r['sesgo_boca'][3] is not None
                  and r['sesgo_boca'][1] <= 0.10 and r['sesgo_boca'][3] <= 0.10 and r['sesgo_boca'][2] >= 0.20)
        P4 = bool(p4n >= 16)
        log(f"   P4 se apaga solo (Q2<=0.10, Q4<=0.10, Q3>=0.20) en {p4n}/{N_SEM} (>=16)  -> {'OK' if P4 else 'NO'}")

        ret = {}
        if res_B:
            for b in BRAZOS_BAT:
                ret[b] = {e: sum(1 for r in res_B if r['brazo'] == b and r['etapa'] == e and r['pasa']) for e in bv13.SEIS}
                log(f"   M5 {b:10s} " + "  ".join(f"{e} {ret[b][e]}/{N_SEM}" for e in bv13.SEIS))
            malas = [e for e in bv13.SEIS if ret['SELF-TEST'][e] < 18]
            P5 = bool(not malas)
            log(f"   P5 retencion: etapas por debajo de 18/{N_SEM} en SELF-TEST: {malas or 'ninguna'}  -> {'OK' if P5 else 'NO'}")
        else:
            P5 = None; log("   P5 retencion: NO CORRIDA (--sin-bateria)")

        gen = {}
        if res_G:
            for b in BRAZOS_BAT:
                gen[b] = {rg: dict(acc=mediana([r['acc'] for r in res_G if r['brazo'] == b and r['regla'] == rg]),
                                   ba=mediana([r['ba'] for r in res_G if r['brazo'] == b and r['regla'] == rg]),
                                   cob=mediana([r['cobertura'] for r in res_G if r['brazo'] == b and r['regla'] == rg])) for rg in REGLAS}
                log(f"   M6 {b:10s} " + "  ".join(f"{rg}: G1 {gen[b][rg]['acc']} G2 {gen[b][rg]['ba']} cob {gen[b][rg]['cob']}" for rg in REGLAS))
            a_s, a_v, a_z = gen['SELF-TEST']['px0']['acc'], gen['V13']['px0']['acc'], gen['SELF-TEST']['azar']['acc']
            P6 = bool(a_s is not None and a_v is not None and a_z is not None and a_s >= 0.80 and a_s >= a_v - 0.10 and 0.35 <= a_z <= 0.65)
            log(f"   P6 generalizacion: G1 px0 SELF-TEST {a_s} (>=0.80 y >= V13 {a_v} -0.10), azar {a_z} en [0.35,0.65]  -> {'OK' if P6 else 'NO'}")
        else:
            P6 = None; log("   P6 generalizacion: NO CORRIDA (--sin-generaliza)")

        vs, vv = mediana([r['veneno_post'] for r in Gb['SELF-TEST'].values()]), mediana([r['veneno_post'] for r in Gb['V13'].values()])
        ds, dv = mediana([r['deaths'] for r in Gb['SELF-TEST'].values()]), mediana([r['deaths'] for r in Gb['V13'].values()])
        P7 = bool(vs is not None and vv is not None and ds is not None and dv is not None and vs <= 4 * vv and ds <= 1.50 * dv)
        log(f"   P7 probar no es envenenarse: veneno_post {vs} <= 4x{vv} y muertes {ds} <= 1.50x{dv}  -> {'OK' if P7 else 'NO'}")

        de_m = mediana([r['recup'] for r in Gb['dE-TEST'].values()])
        log(f"   [exploratorio, sin criterio] dE-TEST recuperacion {de_m} con sesgo_boca[Q3] {None if q3['dE-TEST'] is None else round(q3['dE-TEST'],4)} "
            f"contra SELF-TEST {stm} con {None if q3['SELF-TEST'] is None else round(q3['SELF-TEST'],4)}")

        V.update(P1=P1, P2=P2, P3=P3, P4=P4, P5=P5, P6=P6, P7=P7, recup_V13=v13m, recup_SELF=stm,
                 recup_CONST_a=mediana([r['recup'] for r in Gb['CONST-a'].values()]),
                 recup_CONST_b=mediana([r['recup'] for r in Gb['CONST-b'].values()]),
                 recup_MOMENTO=mediana([r['recup'] for r in Gb['MOMENTO'].values()]), recup_dE=de_m,
                 pareado_vs_V13=p1n, pareado_vs_CONST_a=pa, pareado_vs_CONST_b=pb_, pareado_vs_MOMENTO=pm,
                 retencion=ret, generaliza=gen)

        if not V['G_c_MARGEN']:
            ver = "NULO por G-c (no hay margen o la medida esta censurada): hace falta otro mundo. ERR."
        elif not V['G_d_masa']:
            ver = "NULO por G-d: el control MOMENTO no conserva la masa del sesgo. El control esta mal construido. ERR."
        elif not P1:
            ver = "REFUTADO: la sorpresa sobre si mismo en la boca no acelera la recuperacion tras la inversion."
        elif not P7:
            ver = "NULO por P7: 'probar' es 'envenenarse'; M1 no mide lo que dice."
        elif not P2:
            ver = "ACELERA, pero el sesgo constante tambien: lo que acelera es la CANTIDAD de sesgo, no la sorpresa."
        elif not P3:
            ver = "ACELERA y no es la cantidad, pero la traza DESPLAZADA hace lo mismo: es el NIVEL, no el momento."
        elif P5 is False or P6 is False:
            ver = "ACELERA y los controles no, pero a COSTA de retencion o generalizacion: canje medido, no mejora."
        elif not P4:
            ver = "ACELERA y los controles no, pero el sesgo NO se apaga solo (lazo sorpresa->morder->sorpresa): limite medido."
        else:
            ver = ("ACELERA, ningun control lo consigue, se apaga solo y no cobra retencion, generalizacion ni muertes. "
                   "RAMA: pide replica preregistrada en semillas 61-80 antes de cualquier afirmacion.")
        log(f"VEREDICTO (20 semillas; no cierra ningun nivel del brief): {ver}")
    else:
        log("ANALISIS SIMPLIFICADO (--brazos): faltan brazos que P1-P7/M5/M6 necesitan por nombre (SELF-TEST, "
            "CONST-a, CONST-b, MOMENTO o dE-TEST no estan en --brazos/--baterias de esta corrida). Se listan "
            "medianas y pareado<V13 por brazo activo, y M5/M6 crudos si corrieron; el veredicto de la DOSIS lo "
            "calcula corre_dosis_dE.py sobre 'principal'/'retencion'/'generaliza' con los umbrales de "
            "PREREGISTRO_dosis_dE.md (ERR-31: nunca los umbrales de una bateria reusada).")
        Gb = {b: {r['seed']: r for r in res_T if r['brazo'] == b} for b in BRAZOS_ACTIVOS}
        v13g = Gb.get('V13', {})
        v13m = mediana([r['recup'] for r in v13g.values()])
        cens = sum(r['censurado'] for r in v13g.values())
        V['G_c_MARGEN'] = bool(v13m is not None and 500 <= v13m <= T_INV - 1 and cens <= 4)
        log(f"   G-c margen: V13 recuperacion mediana {v13m}, censuradas {cens}/{len(v13g)} -> "
            f"{'OK' if V['G_c_MARGEN'] else 'NO (M1 no sirve en este mundo; ERR y mundo nuevo)'}")
        V['G_b_sesgoQ3'] = V['G_b_razon'] = V['G_b_LECTURA'] = None
        V['G_d_masa'] = None
        resumen_brazos = {}
        for b in BRAZOS_ACTIVOS:
            g = Gb.get(b, {})
            rec = mediana([r['recup'] for r in g.values()])
            par = pareado(g, v13g, SEEDS, 'recup') if b != 'V13' else None
            resumen_brazos[b] = dict(n=len(g), recup=rec, razon_V13=razon(rec, v13m), pareado_lt_V13=par,
                                      censuradas=sum(r['censurado'] for r in g.values()))
            log(f"   {b:10s} n={len(g):<3d} recuperacion {rec}  razon/V13 {resumen_brazos[b]['razon_V13']}"
                f"  pareado<V13 {par}  censuradas {resumen_brazos[b]['censuradas']}")

        P1 = P2 = P3 = P4 = P7 = None
        ret = {}
        if res_B:
            for b in BRAZOS_BAT:
                ret[b] = {e: sum(1 for r in res_B if r['brazo'] == b and r['etapa'] == e and r['pasa']) for e in bv13.SEIS}
                log(f"   M5 {b:10s} " + "  ".join(f"{e} {ret[b][e]}/{N_SEM}" for e in bv13.SEIS))
        P5 = None
        gen = {}
        if res_G:
            for b in BRAZOS_BAT:
                gen[b] = {rg: dict(acc=mediana([r['acc'] for r in res_G if r['brazo'] == b and r['regla'] == rg]),
                                   ba=mediana([r['ba'] for r in res_G if r['brazo'] == b and r['regla'] == rg]),
                                   cob=mediana([r['cobertura'] for r in res_G if r['brazo'] == b and r['regla'] == rg])) for rg in REGLAS}
                log(f"   M6 {b:10s} " + "  ".join(f"{rg}: G1 {gen[b][rg]['acc']} G2 {gen[b][rg]['ba']} cob {gen[b][rg]['cob']}" for rg in REGLAS))
        P6 = None

        V.update(P1=P1, P2=P2, P3=P3, P4=P4, P5=P5, P6=P6, P7=P7, recup_V13=v13m, resumen_brazos=resumen_brazos,
                 retencion=ret, generaliza=gen)
        ver = ("CORRIDA --brazos (DOSIS, parcial): sin veredicto generico P1-P7 (brazos de referencia no incluidos "
               "en esta corrida). Datos crudos en 'principal'/'retencion'/'generaliza'; el veredicto de la dosis lo "
               "calcula corre_dosis_dE.py con los umbrales de PREREGISTRO_dosis_dE.md.")
        log(); log(f"VEREDICTO (parcial, --brazos): {ver}")

    for r in res_T:
        r.pop('traza_s', None)
    meta = dict(fecha=time.strftime('%Y-%m-%dT%H:%M:%S'), semillas=SEEDS,
                brazos={b: BRAZOS[b] for b in BRAZOS_ACTIVOS}, T=T, invertir_en=T_INV,
                n_traza=NT, desfase=DESFASE, k_test=K_TEST, brazos_bateria=BRAZOS_BAT,
                veredicto=ver, veredictos=V, identidades=rc, procesos_python=ps, shas=SHAS(),
                python=platform.python_version(), numpy=np.__version__)
    dj = os.path.join(RAIZ, 'datos', f'probar_si_mismo_s{SEEDS[0]}-{SEEDS[-1]}_{stamp}.json')
    json.dump(dict(meta=meta, principal=res_T, retencion=res_B, generaliza=res_G),
              open(dj, 'w', encoding='utf-8'), ensure_ascii=False, default=str)
    log(f"datos -> {os.path.basename(dj)}  sha256_16 = {h16(dj)}")
    _log['f'].close()
