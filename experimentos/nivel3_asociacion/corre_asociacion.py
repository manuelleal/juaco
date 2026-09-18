"""experimentos/nivel3_asociacion/corre_asociacion.py -- Ejecuta PREREGISTRO_asociacion.md: ¿la asociación en una
exposición por parecido (propuesta B-4, creador B) reduce `exp_hasta` en el MUNDO DE REGLA, con `px0` (el
parecido predice el valor) contra `azar` (no)?

Brazos (perilla `sem` de organismo_v14gL.py, los valores que define organismo_v14L): v14 (sem=0, apagado),
via_lenta (sem=1), HD (sem=2), grafo (sem=4) -- ver PREREGISTRO_asociacion.md §3 sobre por qué sem=3 (control
barajado de B-4 dentro del mundo AB) no es un brazo aquí. Perillas del tronco ENCENDIDAS siempre (los kwargs de
organismo/bateria_generaliza.py INSTRUMENTOS['organismo_v14']): la pregunta es si el órgano ayuda al tronco v14
tal cual, no a una versión reducida. T=200000 (el de bateria_generaliza.py), semillas 101-120.

REGLA 10 (EQUIPO.md): log desde el arranque, con fsync. REGLA 11: un solo Pool a la vez; lista los procesos
python vivos antes de abrirlo. Los UMBRALES de los veredictos son los de PREREGISTRO_asociacion.md §6-8, NO los
default de bateria_generaliza.py (ERR-31: un runner que decide con los umbrales de bateria_generaliza en vez de
los del preregistro del candidato ya se documentó una vez -- corre_baterias_v13E.py, G1/G2 0.80/0.85).

Identidad interna (3 casos: los tres mundos del mundo de regla a la primera semilla de la corrida, T corto,
perillas ON): repite, más ligera, la que ya corrió identidad_v14gL.py (12/12) -- aborta si no es 3/3. No
reemplaza ese arnés: confirma que el binario que se va a usar AHORA sigue siendo organismo_v14g exacto con
sem=0.

Uso:
    python experimentos/nivel3_asociacion/corre_asociacion.py --humo             (UN proceso, sin Pool, 2 semillas,
                                                                                    T corto; sólo prueba el montaje)
    python experimentos/nivel3_asociacion/corre_asociacion.py [--desde 101]      (Pool(14), 20 semillas; lo corre
                                                                                    el coordinador)
"""
import sys, os, json, time, hashlib, platform, subprocess
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
import numpy as np

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
# organismo/ PRIMERO en sys.path, siempre (ERR-28): experimentos/v13_dos_vias y otras copias por anclas tienen
# sus propios organismo_v1*.py con defaults distintos de los congelados.
sys.path[:0] = [os.path.join(RAIZ, 'organismo'), AQUI]

HUMO = '--humo' in sys.argv
DESDE = int(sys.argv[sys.argv.index('--desde') + 1]) if '--desde' in sys.argv else 101
NSEM = 2 if HUMO else 20
SEEDS = list(range(DESDE, DESDE + NSEM))
T_MAIN = 200000    # el de organismo/bateria_generaliza.py
T_HUMO = 20000     # corto: fase2_en=10000 basta para ejercitar la entrada de los patrones de test
T_ID = 20000       # identidad interna (más ligera que identidad_v14gL.py, que ya corrió a T=40000, 12/12)
N_PARALELO = 14

# kwargs de organismo/bateria_generaliza.py INSTRUMENTOS['organismo_v14']: las perillas del tronco ENCENDIDAS
TRUNK = dict(eta_s=0.015, puerta=3, mask_rel=2, del_s=0.25, del_c=0.25, ema_c=0.05,
             puerta_pat=5, pat_shuf=0, pat_min=1)

BRAZOS = {'v14': 0, 'via_lenta': 1, 'HD': 2, 'grafo': 4}   # sem, tal como lo define organismo_v14L
BRAZOS_PARECIDO = ['via_lenta', 'HD', 'grafo']              # BRAZOS sin la referencia v14
MUNDOS = ['px0', 'azar']                                    # medida principal (PREREGISTRO §4)
REGLAS_ID = ['px0', 'xor01', 'azar']                        # identidad interna (3 casos)
NUEVAS = {'sem', 'exp_hasta', 'n_mord', 'n_sem', 'n_des', 'sem_log', 'rel_arista', 'n_nodos'}

# umbrales de PREREGISTRO_asociacion.md §6-8 (ERR-31: NO son los default de bateria_generaliza.py)
UMBRAL_BAJA30 = 0.70    # exp_hasta(brazo) <= 0.70 * exp_hasta(v14)  =>  baja >= 30%
UMBRAL_PAREO = 14       # de 20 semillas, el brazo le gana a v14
UMBRAL_AZAR10 = 0.90    # exp_hasta(brazo) >= 0.90 * exp_hasta(v14) en azar  =>  no baja mas de 10%
UMBRAL_G1 = 0.80
UMBRAL_G2 = 0.85

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


def f3(x, n=3):
    return '  n/a' if x is None else f"{x:.{n}f}"


def tarea(args):
    """('I', regla, seed, T_): identidad sem=0 == organismo_v14g, perillas ON. ('T', brazo, regla, seed, T_): una
    corrida de un brazo. Importa DENTRO de la función: vale para el spawn de Pool."""
    tipo = args[0]
    if tipo == 'I':
        _, regla, seed, T_ = args
        import organismo_v14g as a_, organismo_v14gL as b_
        kw = dict(T=T_, mundo='regla', regla=regla, **TRUNK)
        a, b = N(a_.run(seed, **kw)), N(b_.run(seed, **kw, sem=0))
        b = {k: v for k, v in b.items() if k not in NUEVAS}
        dif = [k for k in a if a[k] != b.get(k)]
        return dict(tipo='I', regla=regla, seed=seed, identico=not dif, difieren=dif)
    _, brazo, regla, seed, T_ = args
    import organismo_v14gL as m
    r = m.run(seed, T=T_, mundo='regla', regla=regla, sem=BRAZOS[brazo], **TRUNK)
    vr = m.split_regla(seed, regla)[3]
    test = r['test']
    f = [1.0 if r['W_apriori'][k] > 0 else (0.5 if r['W_apriori'][k] == 0 else 0.0) for k in test if vr[k] == 'comida']
    p = [1.0 if r['W_apriori'][k] < 0 else (0.5 if r['W_apriori'][k] == 0 else 0.0) for k in test if vr[k] == 'veneno']
    pf = [r['primer'][k]['pb'] for k in test if r['primer'][k] is not None and vr[k] == 'comida']
    pp = [1 - r['primer'][k]['pb'] for k in test if r['primer'][k] is not None and vr[k] == 'veneno']
    eh = [r['exp_hasta'][k] for k in test if r['exp_hasta'].get(k) is not None]
    return dict(tipo='T', brazo=brazo, regla=regla, seed=seed,
                acc=0.5 * float(np.mean(f)) + 0.5 * float(np.mean(p)),                      # G1, formula de bateria_generaliza
                ba=(0.5 * float(np.mean(pf)) + 0.5 * float(np.mean(pp))) if (pf and pp) else None,   # G2
                cobertura=sum(v is not None for v in r['primer'].values()),                 # K
                exp_hasta_semilla=(float(np.median(eh)) if eh else None), n_asocio=len(eh), n_test=len(test),
                n_sem=r['n_sem'], n_des=r['n_des'], n_nodos=r['n_nodos'],
                celdas=r['celdas'], splits=r['splits'], deaths=r['deaths'])


def _v(res, brazo, regla, seed, k):
    for r in res:
        if r['tipo'] == 'T' and r['brazo'] == brazo and r['regla'] == regla and r['seed'] == seed:
            return r[k]
    return None


def pareo(res, brazo, ref, regla, seeds):
    """Semillas donde `brazo` le gana a `ref`: exp_hasta_semilla MENOR en la MISMA semilla (menos exposiciones =
    asocia mas rapido). Censurado (None) en cualquiera de los dos = no cuenta como victoria (declarado, §5)."""
    gana = 0
    for s in seeds:
        a, b = _v(res, brazo, regla, s, 'exp_hasta_semilla'), _v(res, ref, regla, s, 'exp_hasta_semilla')
        if a is not None and b is not None and a < b:
            gana += 1
    return gana


def resumen(res, seeds):
    """Por (brazo, mundo): mediana de exp_hasta_semilla (censuradas excluidas), n censuradas, mediana acc/ba."""
    T_ = {}
    for b in BRAZOS:
        for rg in MUNDOS:
            eh = [x for x in (_v(res, b, rg, s, 'exp_hasta_semilla') for s in seeds) if x is not None]
            acc = [x for x in (_v(res, b, rg, s, 'acc') for s in seeds) if x is not None]
            ba = [x for x in (_v(res, b, rg, s, 'ba') for s in seeds) if x is not None]
            T_[(b, rg)] = dict(exp_mediana=(float(np.median(eh)) if eh else None), n_ok=len(eh), n_censura=len(seeds) - len(eh),
                               acc_mediana=(float(np.median(acc)) if acc else None), ba_mediana=(float(np.median(ba)) if ba else None))
    return T_


def veredictos(res, seeds, S):
    """Aplica los umbrales de PREREGISTRO_asociacion.md §6-8 (NO los de bateria_generaliza.py -- ERR-31)."""
    Tb = resumen(res, seeds)
    V = {}
    # -- px0: al menos un brazo baja >=30% Y le gana a v14 en >= 14/20 (S/20 si S<20, ver §ADVERTENCIA en informe)
    px0_ok = {}
    for b in BRAZOS_PARECIDO:
        m_b, m_v14 = Tb[(b, 'px0')]['exp_mediana'], Tb[('v14', 'px0')]['exp_mediana']
        baja30 = bool(m_b is not None and m_v14 is not None and m_b <= UMBRAL_BAJA30 * m_v14)
        par = pareo(res, b, 'v14', 'px0', seeds)
        px0_ok[b] = dict(baja30=baja30, mediana=m_b, mediana_v14=m_v14, pareo=par, pareo_ok=par >= min(UMBRAL_PAREO, S))
    V['px0_candidatos'] = [b for b in BRAZOS_PARECIDO if px0_ok[b]['baja30'] and px0_ok[b]['pareo_ok']]
    V['px0_detalle'] = px0_ok
    V['px0_baja_30'] = bool(V['px0_candidatos'])
    # -- azar: NINGUN brazo baja >10% Y el engano cuesta (mediana >= v14) para los TRES brazos
    azar_ok = {}
    for b in BRAZOS_PARECIDO:
        m_b, m_v14 = Tb[(b, 'azar')]['exp_mediana'], Tb[('v14', 'azar')]['exp_mediana']
        no_baja10 = bool(m_b is not None and m_v14 is not None and m_b >= UMBRAL_AZAR10 * m_v14)
        engano_cuesta = bool(m_b is not None and m_v14 is not None and m_b >= m_v14)
        azar_ok[b] = dict(no_baja10=no_baja10, engano_cuesta=engano_cuesta, mediana=m_b, mediana_v14=m_v14)
    V['azar_detalle'] = azar_ok
    V['azar_ok'] = bool(azar_ok) and all(x['no_baja10'] and x['engano_cuesta'] for x in azar_ok.values())
    # -- controles G1 (v14/px0) y G2 (cada brazo con parecido/px0)
    V['G1_v14_px0'] = Tb[('v14', 'px0')]['acc_mediana']
    V['G1_ok'] = bool(V['G1_v14_px0'] is not None and V['G1_v14_px0'] >= UMBRAL_G1)
    V['G2_por_brazo'] = {b: Tb[(b, 'px0')]['ba_mediana'] for b in BRAZOS_PARECIDO}
    V['G2_ok'] = bool(V['G2_por_brazo']) and all(x is not None and x >= UMBRAL_G2 for x in V['G2_por_brazo'].values())
    # -- veredicto narrativo (los tres desenlaces de PREREGISTRO_asociacion.md §8)
    if not V['px0_baja_30']:
        ver = ('REFUTADA EN LOS DOS MUNDOS: en px0 ningún brazo baja exp_hasta >= 30% con pareo >= '
               f'{min(UMBRAL_PAREO, S)}/{S}. "heredar por parecido no acelera la asociación; lo que falta no es la '
               'ligadura sino una relación que prediga el valor" (B-4), medido también en el mundo de regla.')
    elif not V['azar_ok']:
        ver = (f"NO CONFIRMA HB4-regla: {V['px0_candidatos']} baja(n) >= 30% en px0, pero el contraste con azar falla "
               "(algún brazo también baja en azar, o el engaño no cuesta) -> asocia más rápido en general, no "
               "específicamente donde el parecido predice el valor.")
    elif not (V['G1_ok'] and V['G2_ok']):
        ver = (f"{V['px0_candidatos']} pasa(n) exp_hasta y el contraste px0/azar, pero daña la generalización del "
               f"tronco (G1={f3(V['G1_v14_px0'])}, G2={ {b: f3(v) for b, v in V['G2_por_brazo'].items()} }) -> queda "
               "como ÓRGANO DE EXPERIMENTO, coste medido, no se propone tal cual. Nada se recalibra.")
    else:
        ver = (f"HB4-regla SOSTENIDA: {V['px0_candidatos']} reduce(n) exp_hasta >= 30% en px0 (no en azar, donde el "
               "engaño cuesta), sin dañar G1/G2 del tronco.")
    V['veredicto'] = ver
    return Tb, V


def informe(res, seeds, Tb, V):
    S = len(seeds)
    log("TABLA -- exp_hasta por brazo y mundo (mediana de medianas por semilla; censuradas excluidas).")
    for rg in MUNDOS:
        for b in BRAZOS:
            t = Tb[(b, rg)]
            log(f"   {rg:5s} {b:10s} exp_hasta {f3(t['exp_mediana'], 1)}  (n_ok={t['n_ok']}/{S}, censuradas={t['n_censura']})"
                f"   acc {f3(t['acc_mediana'])}  ba {f3(t['ba_mediana'])}")
    log()
    log(f"px0 -- candidatos (baja >=30% Y pareo >= {min(UMBRAL_PAREO, S)}/{S}): {V['px0_candidatos'] or '(ninguno)'}")
    for b, d in V['px0_detalle'].items():
        log(f"   {b:10s} exp {f3(d['mediana'],1)} vs v14 {f3(d['mediana_v14'],1)}  baja30={d['baja30']}"
            f"  pareo {d['pareo']}/{S} {'OK' if d['pareo_ok'] else 'FALLA'}")
    log(f"azar -- ningún brazo debe bajar >10% ni ganar sin que el engaño cueste: {'OK' if V['azar_ok'] else 'FALLA'}")
    for b, d in V['azar_detalle'].items():
        log(f"   {b:10s} exp {f3(d['mediana'],1)} vs v14 {f3(d['mediana_v14'],1)}  no_baja10={d['no_baja10']}  engano_cuesta={d['engano_cuesta']}")
    log(f"G1 (v14, px0) = {f3(V['G1_v14_px0'])} (>= {UMBRAL_G1})  {'OK' if V['G1_ok'] else 'FALLA'}")
    log(f"G2 (por brazo, px0) = { {b: f3(v) for b, v in V['G2_por_brazo'].items()} } (>= {UMBRAL_G2})  {'OK' if V['G2_ok'] else 'FALLA'}")
    log()
    log(f"VEREDICTO: {V['veredicto']}")
    if S < 20:
        log(f"*** {S} semilla(s): NINGÚN criterio de §6-8 vale como evidencia (se preregistraron 20). Esto es diagnóstico de montaje.")


def identidad(seeds0, T_):
    """3 casos: los tres mundos de REGLAS_ID a la primera semilla de la corrida. Devuelve la lista de resultados."""
    return [tarea(('I', rg, seeds0, T_)) for rg in REGLAS_ID]


def humo():
    """UN proceso, sin Pool (regla 3 de EQUIPO.md): identidad (3 casos) + brazos x mundos x 2 semillas, T corto."""
    stamp = time.strftime('%Y%m%d_%H%M%S')
    _log['f'] = open(os.path.join(RAIZ, 'datos', f'asociacion_humo_{stamp}.log'), 'w', encoding='utf-8', newline='\n')
    log(f"HUMO asociación (un proceso, sin Pool). identidad (3 casos, T={T_ID}) + {len(BRAZOS)}x{len(MUNDOS)}x{NSEM} "
        f"corridas de T={T_HUMO}, semillas {SEEDS}.")
    shas = {n_: h16(p) for n_, p in [
        ('preregistro', os.path.join(AQUI, 'PREREGISTRO_asociacion.md')), ('script', os.path.abspath(__file__)),
        ('constructor', os.path.join(AQUI, 'construye_v14gL.py')), ('organismo_v14gL', os.path.join(AQUI, 'organismo_v14gL.py')),
        ('identidad_v14gL', os.path.join(AQUI, 'identidad_v14gL.py')),
        ('origen organismo_v14g (congelado)', os.path.join(RAIZ, 'organismo', 'organismo_v14g.py')),
        ('origen bateria_generaliza (congelada)', os.path.join(RAIZ, 'organismo', 'bateria_generaliza.py'))]}
    log("sha " + "  ".join(f"{k} {v}" for k, v in shas.items()))

    ide = identidad(SEEDS[0], T_ID)
    for x in ide:
        log(f"   identidad regla={x['regla']:6s} s{x['seed']}: {'IDENTICO' if x['identico'] else 'DIFIERE ' + str(x['difieren'][:6])}")
    if not all(x['identico'] for x in ide):
        log("*** IDENTIDAD FALLIDA: el instrumento no sirve, no se corre nada más.")
        _log['f'].close(); sys.exit(1)
    log(f"   identidad interna: {sum(x['identico'] for x in ide)}/{len(ide)}")

    lote = [('T', b, rg, s, T_HUMO) for b in BRAZOS for rg in MUNDOS for s in SEEDS]
    log(f"corridas: {len(lote)} (T={T_HUMO}, fase2_en={T_HUMO // 2})...")
    res = []
    for i, x in enumerate(lote, 1):
        res.append(tarea(x))
        r = res[-1]
        log(f"   {i}/{len(lote)}  {r['brazo']:10s} {r['regla']:5s} s{r['seed']}  exp_hasta_semilla={f3(r['exp_hasta_semilla'],1)}"
            f" ({r['n_asocio']}/{r['n_test']} asociaron)  acc={f3(r['acc'])}  ba={f3(r['ba'])}  n_sem={r['n_sem']} n_des={r['n_des']}")
    Tb, V = veredictos(res, SEEDS, len(SEEDS))
    informe(res, SEEDS, Tb, V)

    dj = os.path.join(RAIZ, 'datos', f'asociacion_humo_{stamp}.json')
    json.dump(dict(meta=dict(fecha=time.strftime('%Y-%m-%dT%H:%M:%S'), humo=True, semillas=SEEDS, T=T_HUMO,
                             brazos=BRAZOS, mundos=MUNDOS, trunk=TRUNK, shas=shas,
                             umbrales=dict(BAJA30=UMBRAL_BAJA30, PAREO=UMBRAL_PAREO, AZAR10=UMBRAL_AZAR10, G1=UMBRAL_G1, G2=UMBRAL_G2),
                             veredictos=V, python=platform.python_version(), numpy=np.__version__),
                   identidad=ide, corridas=res),
              open(dj, 'w', encoding='utf-8'), ensure_ascii=False, default=str, indent=1)
    log(f"datos -> {os.path.basename(dj)}  sha256_16 = {h16(dj)}")
    _log['f'].close()


if __name__ == '__main__':
    if HUMO:
        humo(); sys.exit(0)
    import multiprocessing as mp
    mp.set_start_method('spawn', force=True)
    stamp = time.strftime('%Y%m%d_%H%M%S')
    _log['f'] = open(os.path.join(RAIZ, 'datos', f'asociacion_s{SEEDS[0]}-{SEEDS[-1]}_{stamp}.log'), 'w', encoding='utf-8', newline='\n')
    pre = os.path.join(AQUI, 'PREREGISTRO_asociacion.md')
    shas = {n_: h16(p) for n_, p in [
        ('preregistro', pre), ('script', os.path.abspath(__file__)),
        ('constructor', os.path.join(AQUI, 'construye_v14gL.py')), ('organismo_v14gL', os.path.join(AQUI, 'organismo_v14gL.py')),
        ('identidad_v14gL', os.path.join(AQUI, 'identidad_v14gL.py')),
        ('origen organismo_v14g (congelado)', os.path.join(RAIZ, 'organismo', 'organismo_v14g.py')),
        ('origen bateria_generaliza (congelada)', os.path.join(RAIZ, 'organismo', 'bateria_generaliza.py'))]}
    log(f"ARRANQUE asociación en una exposición (propuesta B-4), mundo de regla px0 vs azar. brazos {list(BRAZOS)}, "
        f"mundos {MUNDOS}, semillas {SEEDS[0]}-{SEEDS[-1]} ({len(SEEDS)}). Pool({N_PARALELO}). T={T_MAIN}.")
    log(f"TRUNK (perillas del tronco ON) {TRUNK}")
    log("sha " + "  ".join(f"{k} {v}" for k, v in shas.items()))
    try:
        ps = subprocess.run(['powershell', '-NoProfile', '-Command',
                             "Get-CimInstance Win32_Process | Where-Object { $_.Name -like 'python*' } | ForEach-Object { \"$($_.ProcessId) $($_.CommandLine)\" }"],
                            capture_output=True, text=True, timeout=60).stdout.strip().splitlines()
    except Exception as e:
        ps = [f"(no se pudo listar: {e})"]
    log(f"REGLA 11 -- procesos python vivos ({len(ps)}), este es pid {os.getpid()}")

    with mp.Pool(N_PARALELO) as pool:
        ctrl = [('I', rg, SEEDS[0], T_ID) for rg in REGLAS_ID]
        log(f"ETAPA 1/2 -- identidad interna: sem=0 == organismo_v14g, perillas ON ({len(ctrl)} casos, T={T_ID})...")
        ide = pool.map(tarea, ctrl, chunksize=1)
        for x in ide:
            log(f"   regla={x['regla']:6s} s{x['seed']}: {'IDENTICO' if x['identico'] else 'DIFIERE ' + str(x['difieren'][:6])}")
        log(f"   identidad interna: {sum(x['identico'] for x in ide)}/{len(ide)}")
        if not all(x['identico'] for x in ide):
            log("*** IDENTIDAD FALLIDA: se para (un instrumento que no es bit a bit con sem=0 no confirma nada).")
            _log['f'].close(); sys.exit(1)

        lote = [('T', b, rg, s, T_MAIN) for b in BRAZOS for rg in MUNDOS for s in SEEDS]
        log(f"ETAPA 2/2 -- {len(lote)} corridas de T={T_MAIN} ({len(BRAZOS)} brazos x {len(MUNDOS)} mundos x {len(SEEDS)} semillas)...")
        res = []
        for i, r in enumerate(pool.imap_unordered(tarea, lote, chunksize=1), 1):
            res.append(r)
            if i % 20 == 0 or i == len(lote):
                log(f"          {i}/{len(lote)}")

    Tb, V = veredictos(res, SEEDS, len(SEEDS))
    informe(res, SEEDS, Tb, V)
    meta = dict(fecha=time.strftime('%Y-%m-%dT%H:%M:%S'), humo=False, semillas=SEEDS, T=T_MAIN,
                brazos=BRAZOS, mundos=MUNDOS, trunk=TRUNK, shas=shas, procesos_python=ps,
                umbrales=dict(BAJA30=UMBRAL_BAJA30, PAREO=UMBRAL_PAREO, AZAR10=UMBRAL_AZAR10, G1=UMBRAL_G1, G2=UMBRAL_G2),
                veredictos=V, python=platform.python_version(), numpy=np.__version__)
    dj = os.path.join(RAIZ, 'datos', f'asociacion_s{SEEDS[0]}-{SEEDS[-1]}_{stamp}.json')
    json.dump(dict(meta=meta, identidad=ide, corridas=res), open(dj, 'w', encoding='utf-8'), ensure_ascii=False, default=str, indent=1)
    log(f"datos -> {os.path.basename(dj)}  sha256_16 = {h16(dj)}")
    _log['f'].close()
