"""A-CAL — CALIBRACION DEL CRITERIO DE TRONCO (ERR-91). Ejecuta PREREGISTRO_calibracion_v3.md.

MISION: llegar a la AGI por este camino. Este bloque no mide un organo: mide EL INSTRUMENTO que decide si un organo
entra al tronco. Corre T-A y T-C (ii) con TRES brazos del MISMO organismo (v14.2):
    OFF      = el tronco v14.2 (placebo = 0)
    PLACEBO  = el tronco con la perilla `placebo = 1`: consume 1 sorteo por paso y lo DESCARTA (misma LEY, otra
               trayectoria). Es "el tronco disfrazado de candidato": el NULO exacto.
    PEOR     = el tronco con COSTE DE VIDA mayor (costo = costo_a = 0.001 x m, m declarado en umbrales_v3.PEOR):
               un candidato genuinamente peor. Es el control que DEBE ser rechazado.
y juzga cada puerta con LA LETRA v2 Y LA LETRA v3, LADO A LADO, sobre los mismos numeros.

Por anclas desde experimentos/tronco_v15_dE5/corre_dE5_v2.py (estructura de nueve etapas, log con fsync, ERR-43/54/86/87/89).
Reutiliza POR IMPORT (sin copiar): corre_vivo_rep2 (BRAZOS, resumen2) y mini_vivo (BRAZOS). Umbrales en umbrales_v3.py
(ERR-31). Regla 14: regla14_campo_a_campo.py compara los kwargs de cada brazo contra el montaje del tronco.

  ETAPA 1  identidad (`identidad_criterio_v3.py`, subproceso, un proceso): 47 identidades + 7 controles que DEBEN
           fallar = 54/54, o se para sin veredicto. Escribe su JSON; se lee por PREFIJO + SELLO EXACTO (ERR-87).
  ETAPA 2  regla 14 campo a campo (subproceso). Si falla, se para.
  ETAPA 3  T-C (ii): reversion en el mundo vivo (invertir_vivo_en = T/2), 40 semillas x {OFF, PLACEBO, PEOR}.
  ETAPA 4  T-A: mundo vivo de rep2, brazos VIVO y CUELLO_MIN, 40 semillas x {OFF, PLACEBO, PEOR}.
  ETAPA 5  veredicto de las dos letras (v2 y v3) sobre PLACEBO y sobre PEOR: una linea por puerta y por letra.
  ETAPA 6  CALIBRACION: P(pasa) del PLACEBO por REPARTO de las 80 corridas del nulo (40 OFF + 40 PLACEBO, misma
           ley) en dos brazos de n, B repeticiones; y CAL-3a, el desplazamiento EXACTO de delta = -20 en r.
           -> CAL-1..CAL-5 con su prediccion al lado.

Uso:  python experimentos/criterio_v3/corre_criterio_v3.py
      python experimentos/criterio_v3/corre_criterio_v3.py --humo        (UN proceso, sin Pool, 6 corridas; escribe su JSON)
      python experimentos/criterio_v3/corre_criterio_v3.py --replica     (semillas de replica de umbrales_v3.SEMILLAS)
      python experimentos/criterio_v3/corre_criterio_v3.py --solo TA,TC
      JUACO_POOL=10 python experimentos/criterio_v3/corre_criterio_v3.py (tamano del Pool, ERR-86)
"""
import sys, os, json, time, hashlib, platform, subprocess, re
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
import numpy as np

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
ORG = os.path.join(RAIZ, 'organismo')
VIVO = os.path.join(RAIZ, 'experimentos', 'nivel11_mundo_vivo')
DATOS = os.path.join(RAIZ, 'datos')
DATOS_HUMO = os.path.join(DATOS, 'humo')
sys.path[:0] = [ORG, VIVO, AQUI]   # organismo/ PRIMERO (ERR-28)

import umbrales_v3 as U

HUMO = '--humo' in sys.argv
REPLICA = '--replica' in sys.argv
SOLO = (sys.argv[sys.argv.index('--solo') + 1].split(',') if '--solo' in sys.argv else None)

T = 100000
SEEDS_TA = U.SEMILLAS['TA_replica'] if REPLICA else U.SEMILLAS['TA']
SEEDS_REV = U.SEMILLAS['TCii_replica'] if REPLICA else U.SEMILLAS['TCii']
BRAZOS_TA = ('VIVO', 'CUELLO_MIN')
K_PLACEBO = 1                      # la dosis de la perilla: 1 sorteo por paso, descartado
M_PEOR = U.PEOR['m']               # el multiplicador del coste de vida del brazo PEOR (fijado en el humo)
C0 = U.PEOR['costo_base']
ARMS = ('OFF', 'PLACEBO', 'PEOR')
N_PARALELO = int(os.environ.get('JUACO_POOL', 10))   # ERR-86
B_REP = 4000                       # repeticiones del reparto en la etapa de calibracion
SHA_TRONCO = '17528d767fcebaf6'
ARNES_ESPERADO = 'ARNES TOTAL: 54/54'
_log = {'f': None, 't0': time.time()}


def perillas(arm):
    """Lo UNICO que distingue a los tres brazos. Nada mas se toca (lo verifica regla14_campo_a_campo.py)."""
    if arm == 'OFF':
        return dict(placebo=0)
    if arm == 'PLACEBO':
        return dict(placebo=K_PLACEBO)
    if arm == 'PEOR':
        return dict(placebo=0, costo=C0 * M_PEOR, costo_a=C0 * M_PEOR)
    raise SystemExit(f'brazo desconocido: {arm}')


def kw_vivo(brazo, arm):
    import corre_vivo_rep2 as CR2
    return dict(CR2.BRAZOS[brazo], desambiguar=1, **perillas(arm))


def kw_rev(arm):
    import mini_vivo as MV
    return dict(MV.BRAZOS['VIVO'], desambiguar=1, invertir_vivo_en=T // 2, **perillas(arm))


def hacer(etapa):
    return SOLO is None or etapa in SOLO


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
    return None if not xs else float(np.median(xs))


def a12(xs, ys):
    """A12 PAREADO por semilla: P(x > y) + 0.5 P(x == y) sobre los pares. Formula IDENTICA a corre_dE5_v2.a12."""
    pares = [(x, y) for x, y in zip(xs, ys) if x is not None and y is not None]
    return None if not pares else round(float(np.mean([1.0 if x > y else (0.5 if x == y else 0.0) for x, y in pares])), 3)


def a12_np(xs, ys):
    """A12 NO pareado (todas las parejas): el marginal de CAL-4."""
    xs = [x for x in xs if x is not None]; ys = [y for y in ys if y is not None]
    if not xs or not ys:
        return None
    return round(float(np.mean([[1.0 if x > y else (0.5 if x == y else 0.0) for y in ys] for x in xs])), 3)


def no_inferior(xs, ys, margen, z):
    """NO INFERIORIDAD pareada de UNA COLA al 95 %: d = x - y por semilla; LI = media(d) - z * EE(d).
    Pasa si LI > -margen. z = 1.645 (declarado en umbrales_v3.py). Devuelve el detalle completo."""
    d = [x - y for x, y in zip(xs, ys) if x is not None and y is not None]
    n = len(d)
    if n < 3:
        return dict(n=n, media=None, ee=None, LI=None, pasa=False)
    m = float(np.mean(d)); sd = float(np.std(d, ddof=1)); ee = sd / np.sqrt(n)
    li = m - z * ee
    return dict(n=n, media=round(m, 3), sd=round(sd, 3), ee=round(ee, 3), LI=round(li, 3),
                margen=margen, pasa=bool(li > -margen))


# ------------------------------------------------------------------ tareas (importan dentro: aptas para Pool)
def tarea_vivo(args):
    brazo, seed, arm = args
    import corre_vivo_rep2 as CR2, organismo_v3cal as CAL
    kw = kw_vivo(brazo, arm)
    r = CAL.run(seed, T=T, **kw)
    o = CR2.resumen2(brazo, seed, r, kw, T); o.update(arm=arm, placebo=r['placebo'], des_splits=r['des_splits'])
    return o


def tarea_rev(args):
    seed, arm = args
    import organismo_v3cal as CAL
    r = CAL.run(seed, T=T, **kw_rev(arm))
    return dict(seed=seed, arm=arm, mordA=r['mord']['A'], mordB=r['mord']['B'], visA=r['vis']['A'], visB=r['vis']['B'],
                rev=r['mord']['B'][3] - r['mord']['A'][3], deaths=r['deaths'], muertes_nec=r['muertes_nec'],
                W_nec=r['W_nec'], celdas=r['celdas'], splits=r['splits'], placebo=r['placebo'])


# ------------------------------------------------------------------ veredictos: LAS DOS LETRAS, lado a lado
def juzga_TA(off, cand):
    """off y cand: listas ORDENADAS POR SEMILLA del mismo brazo del mundo vivo."""
    mu_c, mu_o = med([r['deaths'] for r in cand]), med([r['deaths'] for r in off])
    r_c, r_o = med([r['r'] for r in cand]), med([r['r'] for r in off])
    rc, ro = [r['r'] for r in cand], [r['r'] for r in off]
    a = a12(rc, ro)
    u2, u3 = U.V2['T-A'], U.V3['T-A']
    c_mu = bool(mu_c <= u2['muertes'] * mu_o if mu_o > 0 else mu_c <= u2['muertes'])
    c_r = bool(r_c >= r_o - u2['r_delta'])
    ni = no_inferior(rc, ro, u3['margen'], u3['z'])
    return dict(n=len(cand), muertes_cand=mu_c, muertes_tronco=mu_o,
                razon_muertes=(None if not mu_o else round(mu_c / mu_o, 3)),
                r_cand=r_c, r_tronco=r_o, r_delta=round(r_c - r_o, 1), A12_r=a,
                A12_menos_muertes=a12([-r['deaths'] for r in cand], [-r['deaths'] for r in off]),
                clausula_muertes=c_mu, clausula_r_mediana=c_r, no_inferioridad=ni,
                pasa_v2=bool(c_mu and c_r and a is not None and a >= u2['a12']),
                pasa_v3=bool(c_mu and c_r and ni['pasa']))


def juzga_TCii(off, cand):
    rc, ro = [r['rev'] for r in cand], [r['rev'] for r in off]
    a = a12(rc, ro)
    u2, u3 = U.V2['T-C_ii'], U.V3['T-C_ii']
    ni = no_inferior(rc, ro, u3['margen'], u3['z'])
    return dict(n=len(cand), rev_cand=med(rc), rev_tronco=med(ro), A12_rev=a, no_inferioridad=ni,
                # trampa 3 (el mundo que se come la comida): las EXPOSICIONES por cuarto se reportan al lado de rev
                expB_Q4_cand=med([r['visB'][3] for r in cand]), expB_Q4_tronco=med([r['visB'][3] for r in off]),
                expA_Q4_cand=med([r['visA'][3] for r in cand]), expA_Q4_tronco=med([r['visA'][3] for r in off]),
                comeB_Q4_cand=med([r['mordB'][3] for r in cand]), muerdeA_Q4_cand=med([r['mordA'][3] for r in cand]),
                muertes_cand=med([r['deaths'] for r in cand]), muertes_tronco=med([r['deaths'] for r in off]),
                pasa_v2=bool(a is not None and a >= u2['a12']), pasa_v3=bool(ni['pasa']))


# ------------------------------------------------------------------ ETAPA 6: calibracion por REPARTO del nulo
def reparto(vals_nulo, n, letra, margen_z, delta=0.0, B=B_REP, semilla=20260921, extra=None):
    """vals_nulo: lista de TUPLAS con las medidas de cada corrida del NULO (todas la misma ley).
    Se barajan, se parten en dos brazos de n (candidato y tronco) y se aplica `letra`. Devuelve P(pasa).
    `delta` se SUMA a la medida principal del brazo candidato (CAL-3a: delta = -20)."""
    rng = np.random.default_rng(semilla)
    v = list(vals_nulo)
    if len(v) < 2 * n:
        return None
    ok = 0
    for _ in range(B):
        idx = rng.permutation(len(v))
        A = [v[i] for i in idx[:n]]; Bm = [v[i] for i in idx[n:2 * n]]
        ok += bool(letra(Bm, A, delta, margen_z, extra))
    return round(ok / B, 3)


def reparto_TA(res_vivo, n, letra, delta=0.0, B=B_REP, semilla=20260921):
    """T-A es UNA puerta con DOS brazos (VIVO y CUELLO_MIN): la letra pide que pasen los dos. El reparto tiene que
    ser CONJUNTO — la misma particion de etiquetas (semilla, arm) se aplica a los dos brazos — o se pierde la
    correlacion por semilla entre brazos y P(pasa) sale mal (asi se calculo el 0.316 de ERR-91: puerta entera)."""
    etq = sorted({(r['seed'], r['arm']) for r in res_vivo if r['arm'] in ('OFF', 'PLACEBO')})
    por = {b: {(r['seed'], r['arm']): r for r in res_vivo if r['brazo'] == b and r['arm'] in ('OFF', 'PLACEBO')}
           for b in BRAZOS_TA}
    if len(etq) < 2 * n or any(len(por[b]) < len(etq) for b in BRAZOS_TA):
        return None
    rng = np.random.default_rng(semilla)
    ok = 0
    for _ in range(B):
        p = rng.permutation(len(etq))
        A = [etq[i] for i in p[:n]]; Bm = [etq[i] for i in p[n:2 * n]]
        ok += all(letra([por[b][k] for k in Bm], [por[b][k] for k in A], delta, None, None) for b in BRAZOS_TA)
    return round(ok / B, 3)


def letra_TA_v2(off, cand, delta, mz, extra):
    rc = [x['r'] + delta for x in cand]; ro = [x['r'] for x in off]
    mu_c, mu_o = med([x['deaths'] for x in cand]), med([x['deaths'] for x in off])
    u = U.V2['T-A']
    return (((mu_c <= u['muertes'] * mu_o) if mu_o > 0 else (mu_c <= u['muertes']))
            and med(rc) >= med(ro) - u['r_delta'] and (a12(rc, ro) or 0) >= u['a12'])


def letra_TA_v3(off, cand, delta, mz, extra):
    rc = [x['r'] + delta for x in cand]; ro = [x['r'] for x in off]
    mu_c, mu_o = med([x['deaths'] for x in cand]), med([x['deaths'] for x in off])
    u = U.V3['T-A']
    return (((mu_c <= u['muertes'] * mu_o) if mu_o > 0 else (mu_c <= u['muertes']))
            and med(rc) >= med(ro) - u['r_delta'] and no_inferior(rc, ro, u['margen'], u['z'])['pasa'])


def letra_TC_v2(off, cand, delta, mz, extra):
    rc = [x['rev'] + delta for x in cand]; ro = [x['rev'] for x in off]
    return (a12(rc, ro) or 0) >= U.V2['T-C_ii']['a12']


def letra_TC_v3(off, cand, delta, mz, extra):
    rc = [x['rev'] + delta for x in cand]; ro = [x['rev'] for x in off]
    u = U.V3['T-C_ii']
    return no_inferior(rc, ro, u['margen'], u['z'])['pasa']


# ------------------------------------------------------------------ subprocesos y lectura de sus JSON (ERR-87)
def sub(cmd, etq, cwd=None):
    log(f"   -> SUBPROCESO ({etq}): {' '.join(os.path.basename(x) if os.path.sep in x else x for x in cmd[1:])}")
    t0 = time.time()
    p = subprocess.run([sys.executable] + cmd[1:], capture_output=True, text=True, cwd=cwd or AQUI,
                       encoding='utf-8', errors='replace')
    salida = (p.stdout or '')
    for l in salida.strip().splitlines()[-14:]:
        log(f"      | {l}")
    if p.returncode != 0:
        log(f"      *** codigo {p.returncode}; stderr: {(p.stderr or '')[-800:]}")
    log(f"      ({time.time()-t0:.0f}s)")
    return dict(etq=etq, cmd=cmd[1:], returncode=p.returncode, cola=salida.strip().splitlines()[-14:], stdout=salida)


def lee_json(prefijo, res, carpeta=None):
    """ERR-87: el JSON se localiza por PREFIJO + SELLO EXACTO (AAAAMMDD_HHMMSS) leido de la salida del subproceso.
    Nunca 'el ultimo del prefijo'. Si el sello no aparece, NO se adivina: la etapa queda SIN MEDIR."""
    m = re.findall(re.escape(prefijo) + r'_(\d{8}_\d{6})\.json', res.get('stdout', ''))
    if not m:
        log(f"      *** no aparece el sello de {prefijo}_*.json en la salida del subproceso: SIN MEDIR (ERR-87)")
        return None, None
    f = os.path.join(carpeta or DATOS, f"{prefijo}_{m[-1]}.json")
    if not os.path.exists(f):
        log(f"      *** el sello {m[-1]} no existe: {os.path.basename(f)}")
        return None, None
    log(f"      JSON leido por prefijo+sello: {os.path.basename(f)}  sha256_16 = {h16(f)}")
    return f, json.load(open(f, encoding='utf-8'))


CRUDO = {}


def crudo(etq, res, extra=None):
    """ERR-54: los datos crudos se guardan ANTES del analisis, y el analisis los RELEE del disco."""
    f = os.path.join(DATOS, f"{_log['nom']}_crudo_{etq}.json")
    json.dump(dict(meta=dict(etapa=etq, fecha=time.strftime('%Y-%m-%dT%H:%M:%S'), n=len(res), extra=extra), corridas=res),
              open(f, 'w', encoding='utf-8'), ensure_ascii=False, default=str)
    log(f"   CRUDO ({len(res)} corridas) -> {os.path.basename(f)}  sha256_16 = {h16(f)}")
    leido = json.load(open(f, encoding='utf-8'))['corridas']
    CRUDO[etq] = leido
    return leido


def pool_map(fn, tareas, etq):
    import multiprocessing as mp
    try:
        mp.set_start_method('spawn', force=True)
    except RuntimeError:
        pass
    res = []
    with mp.Pool(N_PARALELO) as pool:
        for i, r in enumerate(pool.imap_unordered(fn, tareas, chunksize=1), 1):
            res.append(r)
            if i % 20 == 0 or i == len(tareas): log(f"          {etq} {i}/{len(tareas)}")
    return res


def nada(motivo):
    return dict(pasa_v2=False, pasa_v3=False, medido=False, nota=motivo)


# ------------------------------------------------------------------ etapas 3 y 4 como FUNCIONES (se pueden probar
# sin correr ninguna simulacion: prueba_wiring.py les pasa crudos sinteticos y verifica que el runner no se cae
# despues de 15 minutos de Pool).
def etapa_TC(res_rev, V):
    G = lambda arm: sorted([r for r in res_rev if r['arm'] == arm], key=lambda r: r['seed'])
    V['T-C_ii'] = dict(medido=True, PLACEBO=juzga_TCii(G('OFF'), G('PLACEBO')), PEOR=juzga_TCii(G('OFF'), G('PEOR')))
    for arm in ('PLACEBO', 'PEOR'):
        d = V['T-C_ii'][arm]
        log(f"   PUERTA T-C (ii) [{arm}] v2 [{U.V2['T-C_ii']['frase']}] -> A12 {d['A12_rev']}  rev {d['rev_cand']} vs {d['rev_tronco']}  "
            f"expB_Q4 {d['expB_Q4_cand']}/{d['expB_Q4_tronco']} (trampa 3)  muertes {d['muertes_cand']}/{d['muertes_tronco']} "
            f"-> {'PASA' if d['pasa_v2'] else 'NO'}")
        log(f"   PUERTA T-C (ii) [{arm}] v3 [{U.V3['T-C_ii']['frase']}] -> media d {d['no_inferioridad']['media']} "
            f"(sd {d['no_inferioridad'].get('sd')}, EE {d['no_inferioridad'].get('ee')}, n {d['no_inferioridad']['n']})  "
            f"LI {d['no_inferioridad']['LI']} > -{U.V3['T-C_ii']['margen']} -> {'PASA' if d['pasa_v3'] else 'NO'}")
    return V


def etapa_TA(res_vivo, V):
    VA = dict(medido=True)
    for b in BRAZOS_TA:
        G = lambda arm: sorted([r for r in res_vivo if r['brazo'] == b and r['arm'] == arm], key=lambda r: r['seed'])
        VA[b] = {arm: juzga_TA(G('OFF'), G(arm)) for arm in ('PLACEBO', 'PEOR')}
        for arm in ('PLACEBO', 'PEOR'):
            d = VA[b][arm]
            log(f"      T-A {b:10s} [{arm}] muertes {d['muertes_cand']} vs {d['muertes_tronco']} (razon {d['razon_muertes']} <= {U.V2['T-A']['muertes']})  "
                f"r {d['r_cand']} vs {d['r_tronco']} (delta {d['r_delta']} >= -{U.V2['T-A']['r_delta']})  A12 {d['A12_r']}  "
                f"NI media {d['no_inferioridad']['media']} sd {d['no_inferioridad'].get('sd')} LI {d['no_inferioridad']['LI']}  "
                f"celdas {med([r['celdas'] for r in G(arm)])} splits {med([r['splits'] for r in G(arm)])} (trampa 4)")
    for arm in ('PLACEBO', 'PEOR'):
        v2 = all(VA[b][arm]['pasa_v2'] for b in BRAZOS_TA); v3 = all(VA[b][arm]['pasa_v3'] for b in BRAZOS_TA)
        VA[f'pasa_v2_{arm}'] = v2; VA[f'pasa_v3_{arm}'] = v3
        log(f"   PUERTA T-A [{arm}] v2 [{U.V2['T-A']['frase']}] -> {'PASA' if v2 else 'NO'}")
        log(f"   PUERTA T-A [{arm}] v3 [{U.V3['T-A']['frase']}] -> {'PASA' if v3 else 'NO'}")
    V['T-A'] = VA
    return V


def etapas_5_6(V, res_vivo, res_rev):
    """ETAPAS 5 y 6 como funcion: veredicto de LAS DOS LETRAS y CALIBRACION. Separada del __main__ para poder
    probar el cableado con crudos sinteticos (prueba_wiring.py) SIN correr ninguna simulacion."""
    # ---------------------------------------------------------------- ETAPA 5: veredicto de las dos letras
    log("ETAPA 5/6 — veredicto de LAS DOS LETRAS sobre los mismos numeros.")
    for arm in ('PLACEBO', 'PEOR'):
        ta2 = V['T-A'].get(f'pasa_v2_{arm}'); ta3 = V['T-A'].get(f'pasa_v3_{arm}')
        tc2 = V['T-C_ii'].get(arm, {}).get('pasa_v2'); tc3 = V['T-C_ii'].get(arm, {}).get('pasa_v3')
        log(f"   {arm:8s} v2: T-A {'PASA' if ta2 else 'NO'} · T-C ii {'PASA' if tc2 else 'NO'} · juntas {'PASA' if (ta2 and tc2) else 'NO'}")
        log(f"   {arm:8s} v3: T-A {'PASA' if ta3 else 'NO'} · T-C ii {'PASA' if tc3 else 'NO'} · juntas {'PASA' if (ta3 and tc3) else 'NO'}")

    # ---------------------------------------------------------------- ETAPA 6: CALIBRACION (CAL-1..CAL-5)
    log(f"ETAPA 6/6 — CALIBRACION por REPARTO del nulo (80 corridas = 40 OFF + 40 PLACEBO, misma ley), B={B_REP}.")
    CALV = {}
    if V['T-A'].get('medido'):
        for b in BRAZOS_TA:
            nulo = [r for r in res_vivo if r['brazo'] == b and r['arm'] in ('OFF', 'PLACEBO')]
            CALV[f'TA_{b}'] = dict(
                n_nulo=len(nulo),
                v3_n40=reparto(nulo, 40, letra_TA_v3, None), v2_n40=reparto(nulo, 40, letra_TA_v2, None),
                v3_n20=reparto(nulo, 20, letra_TA_v3, None), v2_n20=reparto(nulo, 20, letra_TA_v2, None),
                v3_delta20_n40=reparto(nulo, 40, letra_TA_v3, None, delta=-20.0),
                v2_delta20_n40=reparto(nulo, 40, letra_TA_v2, None, delta=-20.0))
            d = CALV[f'TA_{b}']
            log(f"   CAL T-A {b:10s} (brazo suelto, diagnostico; nulo {d['n_nulo']} corridas)  v3 n=40 {f3(d['v3_n40'])} | v2 n=40 {f3(d['v2_n40'])} | "
                f"v3 n=20 {f3(d['v3_n20'])} | v2 n=20 {f3(d['v2_n20'])} || delta=-20: v3 {f3(d['v3_delta20_n40'])} v2 {f3(d['v2_delta20_n40'])}")
        CALV['TA_ENTERA'] = dict(
            nota='T-A ENTERA (los dos brazos a la vez, misma particion): es la puerta, y es lo que juzgan CAL-1/2/3',
            v3_n40=reparto_TA(res_vivo, 40, letra_TA_v3), v2_n40=reparto_TA(res_vivo, 40, letra_TA_v2),
            v3_n20=reparto_TA(res_vivo, 20, letra_TA_v3), v2_n20=reparto_TA(res_vivo, 20, letra_TA_v2),
            v3_delta20_n40=reparto_TA(res_vivo, 40, letra_TA_v3, delta=-20.0),
            v2_delta20_n40=reparto_TA(res_vivo, 40, letra_TA_v2, delta=-20.0))
        d = CALV['TA_ENTERA']
        log(f"   CAL T-A ENTERA (los dos brazos)  v3 n=40 {f3(d['v3_n40'])} | v2 n=40 {f3(d['v2_n40'])} | "
            f"v3 n=20 {f3(d['v3_n20'])} | v2 n=20 {f3(d['v2_n20'])} || delta=-20: v3 {f3(d['v3_delta20_n40'])} v2 {f3(d['v2_delta20_n40'])}")
    if V['T-C_ii'].get('medido'):
        nulo = [r for r in res_rev if r['arm'] in ('OFF', 'PLACEBO')]
        CALV['TCii'] = dict(n_nulo=len(nulo),
                            v3_n40=reparto(nulo, 40, letra_TC_v3, None), v2_n40=reparto(nulo, 40, letra_TC_v2, None),
                            v3_n20=reparto(nulo, 20, letra_TC_v3, None), v2_n20=reparto(nulo, 20, letra_TC_v2, None),
                            v3_delta20_n40=reparto(nulo, 40, letra_TC_v3, None, delta=-20.0),
                            v2_delta20_n40=reparto(nulo, 40, letra_TC_v2, None, delta=-20.0))
        d = CALV['TCii']
        log(f"   CAL T-C ii            (nulo {d['n_nulo']} corridas)  v3 n=40 {f3(d['v3_n40'])} | v2 n=40 {f3(d['v2_n40'])} | "
            f"v3 n=20 {f3(d['v3_n20'])} | v2 n=20 {f3(d['v2_n20'])} || delta=-20: v3 {f3(d['v3_delta20_n40'])} v2 {f3(d['v2_delta20_n40'])}")

    # --- CAL-4: los SEIS marginales, A12 NO pareado del PLACEBO contra el tronco
    marg = {}
    if V['T-A'].get('medido'):
        for b in BRAZOS_TA:
            g = lambda arm, k: [r[k] for r in res_vivo if r['brazo'] == b and r['arm'] == arm]
            marg[f'r_{b}'] = a12_np(g('PLACEBO', 'r'), g('OFF', 'r'))
            marg[f'muertes_{b}'] = a12_np([-x for x in g('PLACEBO', 'deaths')], [-x for x in g('OFF', 'deaths')])
    if V['T-C_ii'].get('medido'):
        g = lambda arm, k: [r[k] for r in res_rev if r['arm'] == arm]
        marg['rev'] = a12_np(g('PLACEBO', 'rev'), g('OFF', 'rev'))
        marg['muertes_rev'] = a12_np([-x for x in g('PLACEBO', 'deaths')], [-x for x in g('OFF', 'deaths')])

    def dentro(x, lo, hi):
        return bool(x is not None and lo <= x <= hi)

    u = U.CAL
    cal1 = CALV.get('TA_ENTERA', {}).get('v3_n40')          # LA PUERTA ENTERA (los dos brazos), no un brazo suelto
    cal2 = CALV.get('TA_ENTERA', {}).get('v2_n20')
    cal3 = max([x for x in [CALV.get('TA_ENTERA', {}).get('v3_delta20_n40'), CALV.get('TCii', {}).get('v3_delta20_n40')] if x is not None] or [None])
    cal5 = CALV.get('TCii', {}).get('v2_n20')
    VEREDICTO_CAL = {
        'CAL-1': dict(frase=u['CAL-1']['frase'], medido=cal1, pasa=dentro(cal1, u['CAL-1']['lo'], u['CAL-1']['hi'])),
        'CAL-2': dict(frase=u['CAL-2']['frase'], medido=cal2, pasa=dentro(cal2, u['CAL-2']['lo'], u['CAL-2']['hi'])),
        'CAL-3': dict(frase=u['CAL-3']['frase'], medido=cal3, pasa=bool(cal3 is not None and cal3 <= u['CAL-3']['hi'])),
        'CAL-4': dict(frase=u['CAL-4']['frase'], medido=marg,
                      pasa=bool(marg) and all(dentro(v, u['CAL-4']['lo'], u['CAL-4']['hi']) for v in marg.values())),
        'CAL-5': dict(frase=u['CAL-5']['frase'], medido=cal5, pasa=dentro(cal5, u['CAL-5']['lo'], u['CAL-5']['hi'])),
    }
    for k in ('CAL-1', 'CAL-2', 'CAL-3', 'CAL-4', 'CAL-5'):
        d = VEREDICTO_CAL[k]
        log(f"   {k} [{d['frase']}] -> {d['medido']} -> {'ACERTADA' if d['pasa'] else 'REFUTADA'}")
    log("   CAL-3b (perilla real): el brazo PEOR, juzgado arriba. Su delta_r MEDIDO se reporta; si |delta_r| < 20 "
        "el brazo PEOR es mas suave que el desplazamiento exacto y CAL-3 se lee solo de CAL-3a.")
    V['calibracion'] = CALV; V['CAL'] = VEREDICTO_CAL; V['marginales_CAL4'] = marg
    return V


if __name__ == '__main__':
    stamp = time.strftime('%Y%m%d_%H%M%S')
    nom = f"critv3_humo_{stamp}" if HUMO else f"critv3_{'rep_' if REPLICA else ''}{stamp}"
    _log['nom'] = nom
    SAL = DATOS_HUMO if HUMO else DATOS
    os.makedirs(SAL, exist_ok=True)
    _log['f'] = open(os.path.join(SAL, nom + '.log'), 'w', encoding='utf-8', newline='\n')
    pre = os.path.join(AQUI, 'PREREGISTRO_calibracion_v3.md')
    crit = os.path.join(RAIZ, 'registro', 'CRITERIO_TRONCO_v3.md')
    log(f"ARRANQUE A-CAL — calibracion del CRITERIO DE TRONCO ({'HUMO, un proceso, sin Pool' if HUMO else 'serie'}). JUACO_POOL={N_PARALELO}")
    log(f"sha preregistro {h16(pre) if os.path.exists(pre) else '(falta)'}  criterio_v3 {h16(crit) if os.path.exists(crit) else '(falta)'}"
        f"  script {h16(os.path.abspath(__file__))}  construye {h16(os.path.join(AQUI,'construye_criterio_v3.py'))}"
        f"  identidad {h16(os.path.join(AQUI,'identidad_criterio_v3.py'))}  umbrales {h16(os.path.join(AQUI,'umbrales_v3.py'))}"
        f"  organismo_v3cal {h16(os.path.join(AQUI,'organismo_v3cal.py'))}"
        f"  ORIGEN organismo_vivo_rep2 {h16(os.path.join(VIVO,'organismo_vivo_rep2.py'))}  organismo_v142 {h16(os.path.join(ORG,'organismo_v142.py'))}")
    log(f"brazos: OFF placebo=0 | PLACEBO placebo={K_PLACEBO} | PEOR costo=costo_a={C0*M_PEOR:g} (m={M_PEOR})")
    log(f"semillas: T-A {SEEDS_TA[0]}-{SEEDS_TA[-1]} (n={len(SEEDS_TA)})  T-C ii {SEEDS_REV[0]}-{SEEDS_REV[-1]} (n={len(SEEDS_REV)})")
    log(f"letra v2: {U.V2['T-A']['frase']} | {U.V2['T-C_ii']['frase']}")
    log(f"letra v3: {U.V3['T-A']['frase']} | {U.V3['T-C_ii']['frase']}")
    V = {}

    # ================================================================ HUMO: un proceso, sin Pool, 6 corridas
    if HUMO:
        log("HUMO 0/3 — identidad (subproceso, T=20000): 47 identidades + 7 controles que DEBEN fallar.")
        r1 = sub([sys.executable, os.path.join(AQUI, 'identidad_criterio_v3.py'), '20000'], 'identidad')
        V['identidad'] = next((l for l in r1['cola'] if 'ARNES TOTAL' in l), None)
        V['identidad_ok'] = bool(r1['returncode'] == 0 and any(ARNES_ESPERADO in l for l in r1['cola']))
        fI, jI = lee_json('identidad_v3cal', r1, DATOS_HUMO)
        V['identidad_json'] = os.path.basename(fI) if fI else None
        log(f"   {V['identidad']}   (esperado {ARNES_ESPERADO})")

        log(f"HUMO 1/3 — T-A, brazo VIVO, semilla {SEEDS_TA[0]}, T={T}: OFF / PLACEBO / PEOR(m=1.25) / PEOR(m=1.50) (4 corridas).")
        rv = []
        for arm, m in (('OFF', None), ('PLACEBO', None), ('PEOR', 1.25), ('PEOR', 1.50)):
            if m is not None:
                M_PEOR = m
            o = tarea_vivo(('VIVO', SEEDS_TA[0], arm)); o['m'] = m
            rv.append(o)
            log(f"   {arm:7s} m={str(m):5s} s{o['seed']}  r {o['r']}  descendientes {o['descendientes']}  muertes {o['deaths']} {o.get('muertes_nec')}  "
                f"celdas {o['celdas']} splits {o['splits']} des_splits {o['des_splits']}  placebo {o['placebo']}")
        M_PEOR = U.PEOR['m']
        r_off = rv[0]['r']
        log(f"   *** la REGLA declarada (PREREGISTRO §6): m = el menor de (1.25, 1.50) con delta_r <= -20 en esta semilla; "
            f"si ninguno, m = 1.50 y se declara que PEOR es mas suave de lo pedido.")
        for o in rv[2:]:
            log(f"       delta_r(m={o['m']}) = {o['r'] - r_off}")
        eleg = [o['m'] for o in rv[2:] if o['r'] - r_off <= -20]
        V['m_propuesto'] = min(eleg) if eleg else 1.50
        V['m_suave'] = not eleg
        log(f"   *** m FIJADO POR EL HUMO = {V['m_propuesto']}{'  (ninguno llego a -20: PEOR es mas suave de lo pedido)' if not eleg else ''}. "
            f"Se escribe en umbrales_v3.PEOR['m'] y en el preregistro §10, y NO se vuelve a tocar.")
        log(f"   AVISO: delta_r de UNA semilla no es el delta_r de la serie (sd de r ~ 11-19). La serie lo mide con n=40.")

        log(f"HUMO 2/3 — T-C (ii), semilla {SEEDS_REV[0]}, invertir_vivo_en={T//2}: OFF / PLACEBO (2 corridas).")
        rr = [tarea_rev((SEEDS_REV[0], arm)) for arm in ('OFF', 'PLACEBO')]
        for o in rr:
            log(f"   {o['arm']:7s} s{o['seed']}  rev {o['rev']}  mordB {o['mordB']} (visB {o['visB']})  mordA {o['mordA']} (visA {o['visA']})  "
                f"muertes {o['deaths']} {o['muertes_nec']}  celdas {o['celdas']} splits {o['splits']}  placebo {o['placebo']}")

        log("HUMO 3/3 — el PLACEBO difiere del tronco en la trayectoria pero NO en la ley (una semilla no lo prueba: lo prueba la serie).")
        log(f"   OFF r {rv[0]['r']} muertes {rv[0]['deaths']}  |  PLACEBO r {rv[1]['r']} muertes {rv[1]['deaths']}  "
            f"|  identicos: {rv[0]['r'] == rv[1]['r'] and rv[0]['deaths'] == rv[1]['deaths']} (DEBE ser False)")

        dj = os.path.join(SAL, nom + '.json')
        json.dump(dict(meta=dict(fecha=time.strftime('%Y-%m-%dT%H:%M:%S'), humo=True, corridas=6,
                                 semillas=[SEEDS_TA[0], SEEDS_REV[0]], python=platform.python_version(), numpy=np.__version__,
                                 K_PLACEBO=K_PLACEBO, m_propuesto=V.get('m_propuesto'), m_suave=V.get('m_suave'),
                                 sha_preregistro=h16(pre) if os.path.exists(pre) else None,
                                 sha_script=h16(os.path.abspath(__file__)),
                                 sha_organismo=h16(os.path.join(AQUI, 'organismo_v3cal.py')), identidad=V['identidad']),
                       identidad=r1, vivo=rv, reversion=rr),
                  open(dj, 'w', encoding='utf-8'), ensure_ascii=False, default=str)
        log(f"datos -> {os.path.basename(dj)}  sha256_16 = {h16(dj)}")
        _log['f'].close(); sys.exit(0)

    # ================================================================ SERIE
    try:
        ps = subprocess.run(['powershell', '-NoProfile', '-Command',
                             "Get-CimInstance Win32_Process | Where-Object { $_.Name -like 'python*' } | ForEach-Object { \"$($_.ProcessId) $($_.CommandLine)\" }"],
                            capture_output=True, text=True, timeout=60).stdout.strip().splitlines()
    except Exception as e:
        ps = [f"(no se pudo listar: {e})"]
    log(f"REGLA 11 — procesos python vivos ({len(ps)}), este es pid {os.getpid()}")

    # ---------------------------------------------------------------- ETAPA 1: identidad (SIEMPRE)
    log("ETAPA 1/6 — identidad (subproceso, un proceso): 47 identidades + 7 controles que DEBEN fallar.")
    r1 = sub([sys.executable, os.path.join(AQUI, 'identidad_criterio_v3.py'), '20000'], 'identidad')
    if r1['returncode'] != 0 or not any(ARNES_ESPERADO in l for l in r1['cola']):
        log(f"*** el arnes no es {ARNES_ESPERADO}; se para sin veredicto."); _log['f'].close(); sys.exit(1)
    fI, _ = lee_json('identidad_v3cal', r1, DATOS_HUMO)
    V['identidad'] = ARNES_ESPERADO + ' (47 identidades + 7 controles que deben fallar)'
    V['identidad_json'] = os.path.basename(fI) if fI else None

    # ---------------------------------------------------------------- ETAPA 2: regla 14 campo a campo
    log("ETAPA 2/6 — regla 14: los kwargs de cada brazo, CAMPO A CAMPO contra el montaje del tronco.")
    r2 = sub([sys.executable, os.path.join(AQUI, 'regla14_campo_a_campo.py')], 'regla 14')
    if r2['returncode'] != 0:
        log("*** REGLA 14 FALLA; se para sin veredicto."); _log['f'].close(); sys.exit(1)
    V['regla14'] = 'OK'

    for k in ('T-C_ii', 'T-A'):
        V[k] = nada('etapa no corrida (--solo)')
    res_rev = res_vivo = []

    # ---------------------------------------------------------------- ETAPA 3: T-C (ii)
    if hacer('TC'):
        log(f"ETAPA 3/6 — T-C (ii) reversion en el mundo vivo (invertir_vivo_en={T//2}), {SEEDS_REV[0]}-{SEEDS_REV[-1]} x {list(ARMS)} (Pool aqui).")
        res_rev = crudo('TCii', pool_map(tarea_rev, [(s, arm) for s in SEEDS_REV for arm in ARMS], 'T-C ii'),
                        extra=dict(semillas=SEEDS_REV, invertir_vivo_en=T // 2, arms=list(ARMS), m_peor=M_PEOR))
        etapa_TC(res_rev, V)

    # ---------------------------------------------------------------- ETAPA 4: T-A
    if hacer('TA'):
        log(f"ETAPA 4/6 — T-A supervivencia (rep2, T={T}), brazos {list(BRAZOS_TA)} x {list(ARMS)}, "
            f"semillas {SEEDS_TA[0]}-{SEEDS_TA[-1]} (Pool aqui).")
        res_vivo = crudo('TA', pool_map(tarea_vivo, [(b, s, arm) for b in BRAZOS_TA for s in SEEDS_TA for arm in ARMS], 'T-A'),
                         extra=dict(brazos=list(BRAZOS_TA), arms=list(ARMS), semillas=SEEDS_TA, T=T, m_peor=M_PEOR))
        etapa_TA(res_vivo, V)

    etapas_5_6(V, res_vivo, res_rev)   # ETAPAS 5 y 6: las dos letras lado a lado + CAL-1..CAL-5 (todo queda en V)

    meta = dict(fecha=time.strftime('%Y-%m-%dT%H:%M:%S'), replica=REPLICA,
                semillas=dict(vivo=SEEDS_TA, reversion=SEEDS_REV), brazos={a: perillas(a) for a in ARMS},
                K_PLACEBO=K_PLACEBO, m_peor=M_PEOR, B_reparto=B_REP,
                umbrales=dict(v2={k: U.V2[k]['frase'] for k in U.V2}, v3={k: U.V3[k]['frase'] for k in U.V3},
                              CAL={k: U.CAL[k]['frase'] for k in U.CAL}),
                veredictos=V, solo=SOLO, etapas=[r1, r2], procesos_python=ps, pool=N_PARALELO,
                sha_preregistro=h16(pre) if os.path.exists(pre) else None,
                sha_criterio_v3=h16(crit) if os.path.exists(crit) else None,
                sha_script=h16(os.path.abspath(__file__)),
                sha_construye=h16(os.path.join(AQUI, 'construye_criterio_v3.py')),
                sha_identidad=h16(os.path.join(AQUI, 'identidad_criterio_v3.py')),
                sha_umbrales=h16(os.path.join(AQUI, 'umbrales_v3.py')),
                sha_organismo_v3cal=h16(os.path.join(AQUI, 'organismo_v3cal.py')),
                python=platform.python_version(), numpy=np.__version__)
    dj = os.path.join(DATOS, nom + '.json')
    json.dump(dict(meta=meta, vivo=res_vivo, reversion=res_rev), open(dj, 'w', encoding='utf-8'), ensure_ascii=False, default=str)
    log(f"datos -> {os.path.basename(dj)}  sha256_16 = {h16(dj)}")
    _log['f'].close()
