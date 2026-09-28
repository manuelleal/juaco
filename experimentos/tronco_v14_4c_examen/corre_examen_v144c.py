"""corre_examen_v144c.py = corre_examen_v144b.py (9fb2e22a392590c7) con T-C (ii) POR VISITA (ERR-150). MISMO organismo (v14.4b = v14.3 + TERMOP, reusado de tronco_v14_4b_examen con sha), MISMA letra en todo lo demas, semillas nuevas. GENERADO por experimentos/tronco_v14_4c_examen/construye_examen_v144c.py. NO editar a mano."""
"""corre_examen_v144c.py = corre_examen_v144.py (8bb63d3f421040dd) para v14.4b = v14.3 + TERMOP (TERMO con memoria que olvida: media movil a la tasa ema_c del tronco). MISMA letra, mismo juez, misma T-G; semillas nuevas. GENERADO por experimentos/tronco_v14_4b_examen/construye_examen_v144b.py. NO editar a mano."""
"""corre_examen_v144c.py -- EXAMEN DEL CRITERIO DE TRONCO v4 (registro/CRITERIO_TRONCO_v4.md) sobre v14.4b = v14.3 + TERMOP.
Ejecuta experimentos/tronco_v14_4c_examen/PREREGISTRO_examen_v144c.md. Umbrales, semillas y predicciones: umbrales_examen_v144c.py.
Mismo formato y MISMA LETRA que experimentos/tronco_v14_3_examen/corre_examen_v143.py (T-A..T-F y T-H importadas de
umbrales_examen_v143, con la banda de azar G2 de T-B de ERR-122); cambia T-G (la capacidad que declara el candidato).

MISION: llegar a la AGI por este camino. El examen v4 es la puerta de NO REGRESION del organismo comun, no un puntaje: v14.4
entra al tronco si no empeora en nada de lo que el tronco v14.3 ya hace (T-A..T-F) y si su capacidad declarada (T-G: el
termostato sube el crecimiento neto del linaje en el mundo vivo, con su control TERMOINV) se ve en semillas nuevas.

EL TRONCO CONTRA EL QUE SE MIDE ES v14.3:
  examen v3' y T-B: organismo/bateria_v143.py y organismo/bateria_generaliza_v143.py (CONGELADAS) -> organismo_v143(g).
  mundo vivo (T-A, T-C ii, T-D): OFF, TRONCO_B y PLACEBO son EXACTAMENTE las tareas calibradas de V4-CAL (organismo_v3cal = v14.2),
  que en el mundo vivo ES v14.3 bit a bit (masa 3: N inerte; examen de v14.3: 480/480 corridas y arnes (C); identidad_v144cex (A')).
El candidato: organismo_v144b (examen), organismo_v144bg (T-B), organismo_v144bcal (mundo vivo; y el CONTROL TERMOINV, termo = 2).

ETAPAS (serie y replica; regla 10: una linea por etapa con hora, log a disco desde el arranque, fsync):
  0  anclas (sha), construccion por anclas, semillas de T-D recalculadas, regla 14, procesos python vivos (regla 11)
  1  identidad (subproceso de UN proceso): identidad_v144cex.py -> 'RESULTADO: N/N' == umbrales.ARNES_ESPERADO; si no, se para
  2  T-B   generalizacion: {CAND, TRONCO} x {px0, azar} x 20 semillas (T = 200 000)                     80 corridas
  3  EX    examen v3', seis etapas: {CAND, TRONCO} x 6 x 20 semillas -> T-C (i), T-E, T-F examen         240 corridas
  4  T-D   sal muda: {OFF, CAND} x (9 ALIAS + 9 LIMPIAS)                                                  36 corridas
  5  T-C (ii) reversion en el mundo vivo: {OFF, CAND, TRONCO_B, PLACEBO} x 80                          320 corridas
  6  T-A   {VIVO, CUELLO_MIN} x {OFF, CAND, TRONCO_B, PLACEBO, CTRL} x 80                                 800 corridas
  7  T-G   desde los crudos de T-A (CAND, CTRL y OFF en CUELLO_MIN decide; VIVO se reporta)               0 corridas nuevas
  8  veredicto: UNA linea por puerta con su umbral (ERR-89); VEREDICTO
Crudos a disco ANTES del analisis y releidos (ERR-54). JSON de subproceso por prefijo + sello exacto (ERR-87).

Uso (SOLO el coordinador corre --serie/--replica/--reserva; los agentes solo --humo; ERR-115):
  python experimentos/tronco_v14_4c_examen/corre_examen_v144c.py --humo                  (UN proceso, 6 corridas, 200 000 pasos)
  python experimentos/tronco_v14_4c_examen/corre_examen_v144c.py --serie --pool 6        (PC)   | --pool 3 en la nube
  python experimentos/tronco_v14_4c_examen/corre_examen_v144c.py --replica --pool 6 --con <JSON de la serie>
  python experimentos/tronco_v14_4c_examen/corre_examen_v144c.py --reserva --sustituye serie|replica --pool 6   (solo si TRONCO_B no pasa)
  python experimentos/tronco_v14_4c_examen/corre_examen_v144c.py --bloque <serie.json> <replica.json> [<reserva.json>]
Opcional: --solo TB,EX,TD,TC,TA (subconjunto; el veredicto queda INCOMPLETO; T-G sale de TA). Banderas desconocidas o
abreviadas: aborta. Recuperacion (ERR-54; no corre nada): --analiza <datos/examen_v144c_<modo>_<sello>>.
"""
import argparse, hashlib, importlib, json, os, platform, re, subprocess, sys, time

try:
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
except Exception:
    pass
import numpy as np

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
EXP = os.path.join(RAIZ, 'experimentos')
ORG = os.path.join(RAIZ, 'organismo')
VIVO_DIR = os.path.join(EXP, 'nivel11_mundo_vivo')
V3_DIR = os.path.join(EXP, 'criterio_v3')
V4_DIR = os.path.join(EXP, 'criterio_v4')
CREB = os.path.join(EXP, 'creacion_B')
DE5 = os.path.join(EXP, 'tronco_v15_dE5')
V143EX = os.path.join(EXP, 'tronco_v14_3_examen')
TERMO_DIR = os.path.join(EXP, 'organelos', 'termo')
V144B = os.path.join(EXP, 'tronco_v14_4b_examen')   # v14.4c: el ORGANISMO v14.4b y sus baterias, reusados con sha fijado
DATOS_HUMO = os.path.join(RAIZ, 'datos', 'humo')
DATOS_EX = os.path.join(AQUI, 'datos')
for _p in reversed([AQUI, V144B, ORG, VIVO_DIR, V3_DIR, V4_DIR, CREB, DE5]):
    if _p not in sys.path:
        sys.path.insert(0, _p)
for _p in (V143EX, os.path.join(TERMO_DIR, 'carros')):   # AL FINAL: solo organismo_v143cal, umbrales_examen_v143 y los carros
    if _p not in sys.path:
        sys.path.append(_p)

import umbrales_examen_v144c as U


def _importa_sin_argv(nombre):
    """Los runners ajenos LEEN sys.argv al importarse (corre_criterio_v4 parsea '--replica A-B'): se importan con argv limpio."""
    if nombre in sys.modules:
        return sys.modules[nombre]
    a = sys.argv
    sys.argv = [a[0]]
    try:
        return importlib.import_module(nombre)
    finally:
        sys.argv = a


C4 = _importa_sin_argv('corre_criterio_v4')     # la letra v4 calibrada (T-A, T-C ii, T-F vivo) y las tareas del tronco
_importa_sin_argv('corre_criterio_v3')          # C4._v3() lo importa perezoso: aqui, con argv limpio
D5 = _importa_sin_argv('corre_dE5_v2')          # la letra de T-B, T-C (i), T-E, T-F examen
CS = _importa_sin_argv('corre_sal')             # T-D: BASE (sal muda) y resumen
CR2 = _importa_sin_argv('corre_vivo_rep2')
MV = _importa_sin_argv('mini_vivo')
B143 = _importa_sin_argv('bateria_v143')        # organismo/ (CONGELADA): el TRONCO v14.3
B144 = _importa_sin_argv('bateria_v144b')        # esta carpeta: el candidato
G143 = _importa_sin_argv('bateria_generaliza_v143')
G144 = _importa_sin_argv('bateria_generaliza_v144b')
sys.path.insert(0, AQUI)   # las baterias importadas anteponen sus carpetas: la nuestra queda primera otra vez


def h16(p):
    return hashlib.sha256(open(p, 'rb').read()).hexdigest()[:16]


# ------------------------------------------------------------------ ANCLAS: lo reusado (sha fijo) y lo construido aqui
_D143 = os.path.join(V143EX, 'datos')
ANCLAS = {
    os.path.join(ORG, 'organismo_v143.py'): '2cebc0ab0c38b70f',
    os.path.join(ORG, 'organismo_v143g.py'): 'c20fccaa9107fb89',
    os.path.join(ORG, 'bateria_v143.py'): '9daa88a90a2fd7b1',
    os.path.join(ORG, 'bateria_generaliza_v143.py'): 'a894101fd1e6db93',
    os.path.join(ORG, 'organismo_v11.py'): 'f69e24063be1b194',
    os.path.join(ORG, 'organismo_v10.py'): '219d5033fe15b5b9',
    os.path.join(V3_DIR, 'organismo_v3cal.py'): '148014f68cb01785',
    os.path.join(V3_DIR, 'corre_criterio_v3.py'): '7f93eca0e45e167b',
    os.path.join(V4_DIR, 'corre_criterio_v4.py'): 'c70d1c643e78ee88',
    os.path.join(V4_DIR, 'umbrales_v4.py'): '881e2a07245566bb',
    os.path.join(VIVO_DIR, 'corre_vivo_rep2.py'): '10ab45355883d98d',
    os.path.join(VIVO_DIR, 'mini_vivo.py'): 'f3e86cbe6c17e6d7',
    os.path.join(VIVO_DIR, 'organismo_vivo_rep2.py'): '96feb4918dc5d694',
    os.path.join(VIVO_DIR, 'corre_sal.py'): 'bfdc00bb48656337',
    os.path.join(VIVO_DIR, 'diagnostico_codigos.py'): '02905c71a7ac3de8',
    os.path.join(CREB, 'corre_codigo.py'): 'cb91371b77c079d3',
    os.path.join(DE5, 'corre_dE5_v2.py'): 'c042de285398a333',
    os.path.join(V143EX, 'organismo_v143cal.py'): '1169f54ef0a19de1',
    os.path.join(V143EX, 'umbrales_examen_v143.py'): 'c3becf65e9bfd8ec',
    os.path.join(TERMO_DIR, 'carros', 'V143_TERMO.py'): '3db639cab75641fb',
    os.path.join(TERMO_DIR, 'carros', 'V143_TERMOINV.py'): 'da106a995b18bafd',
    os.path.join(TERMO_DIR, 'construye_termo.py'): '23f57933c51c64e8',
    # el examen de v14.3 (el juez de este examen reproduce sus veredictos: identidad_v144cex (J)); y el nulo de T-G
    os.path.join(_D143, 'examen_v143_serie_20260924_124413.json'): 'd39303e1d6ae3949',
    os.path.join(_D143, 'examen_v143_replica_20260924_131427.json'): '55b42f360a51951a',
    os.path.join(_D143, 'examen_v143_serie_20260924_124413_crudo_TA.json'): '764f1768bb82c752',
    os.path.join(_D143, 'examen_v143_replica_20260924_131427_crudo_TA.json'): '150ab1af9d529204',
    os.path.join(RAIZ, 'datos', 'humo', 'potencia_examen_v144_20260928_121917.json'): '4e4df40a5c3cc67d',
    os.path.join(RAIZ, 'experimentos', 'tronco_v14_4_examen', 'umbrales_examen_v144.py'): '0df02bd6a4d548c4',   # T-G y letra (v14.4)
    # v14.4c: el examen v14.4b (organismo, baterias, constructor, carros, umbrales y los ORIGENES de este runner y su arnes)
    os.path.join(V144B, 'organismo_v144b.py'): 'c8f0c25302f20fd9',
    os.path.join(V144B, 'organismo_v144bg.py'): '19106bea564d4a94',
    os.path.join(V144B, 'organismo_v144bcal.py'): 'b9c2cf7b73007a96',
    os.path.join(V144B, 'bateria_v144b.py'): '01e00e0d3c283561',
    os.path.join(V144B, 'bateria_generaliza_v144b.py'): '3bbd29d3d71b022a',
    os.path.join(V144B, 'construye_termop.py'): '81f63fd59d168759',
    os.path.join(V144B, 'carros', 'V143_TERMOP.py'): 'edf5dfc9c5e498da',
    os.path.join(V144B, 'carros', 'V143_TERMOPINV.py'): '63edcafcc569a0d7',
    os.path.join(V144B, 'umbrales_examen_v144b.py'): 'ddc96fa8038c3719',
    os.path.join(V144B, 'corre_examen_v144b.py'): '9fb2e22a392590c7',
    os.path.join(V144B, 'identidad_v144bex.py'): '23f5ed70d42399e0',
    # ERR-150: el analisis del nulo y los crudos del examen de v14.4 (TERMO: la condicion anti-TERMO del arnes (E))
    os.path.join(AQUI, 'analiza_nulo_err150.py'): '29b268b0e1a56a86',
    os.path.join(AQUI, 'datos', 'nulo_err150_20260928_161728.json'): 'a394a03bf9241b40',
    os.path.join(RAIZ, 'experimentos', 'tronco_v14_4_examen', 'datos', 'examen_v144_serie_20260928_123734.json'): '25458f0f470b25e6',
    os.path.join(RAIZ, 'experimentos', 'tronco_v14_4_examen', 'datos', 'examen_v144_serie_20260928_123734_crudo_TCii.json'): 'd7b018cfd63d8eb6',
    os.path.join(RAIZ, 'experimentos', 'tronco_v14_4_examen', 'datos', 'examen_v144_serie_20260928_123734_crudo_TA.json'): '73014ef4831b957b',
}
CONSTRUIDOS = ('organismo_v144b.py', 'organismo_v144bg.py', 'organismo_v144bcal.py', 'bateria_v144b.py', 'bateria_generaliza_v144b.py')


def verifica_anclas():
    malas = [(os.path.relpath(p, RAIZ), h16(p), s) for p, s in ANCLAS.items() if h16(p) != s]
    if malas:
        raise SystemExit(f'*** ANCLA CAMBIADA (lo reusado no es lo que se calibro/midio): {malas}')
    r = subprocess.run([sys.executable, os.path.join(V144B, 'construye_termop.py'), '--verifica'], capture_output=True, text=True,
                       encoding='utf-8', errors='replace')
    if r.returncode != 0:
        raise SystemExit(f'*** los archivos construidos NO son la construccion por anclas:\n{r.stdout[-1500:]}')
    r = subprocess.run([sys.executable, os.path.join(AQUI, 'construye_examen_v144c.py'), '--verifica'], capture_output=True, text=True,
                       encoding='utf-8', errors='replace')
    if r.returncode != 0:
        raise SystemExit(f'*** el runner o el arnes NO son la construccion por anclas desde el examen v14.4b:\n{r.stdout[-1500:]}')
    return {n: h16(os.path.join(V144B, n)) for n in CONSTRUIDOS}


# ------------------------------------------------------------------ los kwargs de cada brazo: LO UNICO que los distingue
PIEZA = dict(norm_lenta=1, termo=1)     # v14.4 = v14.3 (norm_lenta=1, inerte en el mundo vivo) + TERMO
CONTROL = dict(norm_lenta=1, termo=2)   # TERMOINV: la misma regla leyendo la necesidad que el estimulo NO sube


def kw_vivo_cand(brazo):
    return dict(C4.kw_vivo(brazo, 'OFF'), **PIEZA)


def kw_vivo_ctrl(brazo):
    return dict(C4.kw_vivo(brazo, 'OFF'), **CONTROL)


def kw_rev_cand(Ti):
    return dict(C4.kw_rev('OFF', Ti), **PIEZA)


def kw_sal(arm):
    kw = dict(CS.BASE, desambiguar=1, placebo=0)
    if arm == 'CAND':
        kw.update(PIEZA)
    return kw


def telemetria(r):
    """La telemetria de SOLO LECTURA de TERMO (organismo_v144b*: clave 'termo'); None si la pieza no esta encendida."""
    t = r.get('termo')
    return None if t is None else dict(termo=t['termo'], U=t['U'], dec=t['dec'], a_no=t['a_no'], a_si=t['a_si'], mord=t['mord'],
                                       adS=t['adS'])


# ------------------------------------------------------------------ tareas (top-level, aptas para Pool con spawn)
def tarea_vivo(args):
    """T-A (y T-G). OFF/TRONCO_B/PLACEBO = EXACTAMENTE la tarea calibrada de V4-CAL; CAND y CTRL = organismo_v144bcal con los
    mismos kwargs + la pieza (termo 1) o el control (termo 2)."""
    brazo, seed, arm, Ti = args
    if arm not in ('CAND', 'CTRL'):
        o = C4.tarea_vivo((brazo, seed, arm, Ti))
        o['org'] = 'organismo_v3cal'
        return o
    import organismo_v144bcal as V144C
    kw = kw_vivo_cand(brazo) if arm == 'CAND' else kw_vivo_ctrl(brazo)
    t0 = time.time()
    r = V144C.run(seed, T=Ti, **kw)
    o = CR2.resumen2(brazo, seed, r, kw, Ti)
    o.update(seed=seed, seed_real=seed, arm=arm, placebo=r['placebo'], des_splits=r['des_splits'], termo=telemetria(r),
             seg=round(time.time() - t0, 2), org='organismo_v144bcal')
    return o


def tarea_rev(args):
    """T-C (ii). Mismo formato que corre_criterio_v4.tarea_rev (+ la telemetria de TERMO en el candidato)."""
    seed, arm, Ti = args
    if arm != 'CAND':
        o = C4.tarea_rev((seed, arm, Ti))
        o['org'] = 'organismo_v3cal'
        return o
    import organismo_v144bcal as V144C
    t0 = time.time()
    r = V144C.run(seed, T=Ti, **kw_rev_cand(Ti))
    return dict(seed=seed, seed_real=seed, arm=arm, mordA=r['mord']['A'], mordB=r['mord']['B'], visA=r['vis']['A'],
                visB=r['vis']['B'], rev=r['mord']['B'][3] - r['mord']['A'][3], deaths=r['deaths'],
                muertes_nec=r['muertes_nec'], celdas=r['celdas'], splits=r['splits'], placebo=r['placebo'],
                termo=telemetria(r), seg=round(time.time() - t0, 2), org='organismo_v144bcal')


def tarea_sal(args):
    """T-D (sal muda). OFF = el tronco en el mundo vivo (organismo_v3cal, B-5 encendido; == v14.3 ahi)."""
    brazo, seed, arm, Ti = args
    import organismo_v3cal as CAL, organismo_v144bcal as V144C
    m = V144C if arm == 'CAND' else CAL
    t0 = time.time()
    r = m.run(seed, T=Ti, **kw_sal(arm))
    o = CS.resumen(brazo, seed, r)
    o.update(arm=arm, des_splits=r['des_splits'], termo=telemetria(r), seg=round(time.time() - t0, 2), org=m.__name__)
    return o


def tarea_ex(args):
    """Examen v3' (seis etapas): la `tarea` de la bateria (CONGELADA para el tronco v14.3; copia por anclas para el candidato)."""
    org, etapa, seed = args
    t0 = time.time()
    o = (B144 if org == 'CAND' else B143).tarea((etapa, seed))
    o.update(org=org, seg=round(time.time() - t0, 2))
    return o


def tarea_tb(args):
    """T-B: la `tarea` de bateria_generaliza (CONGELADA para el tronco v14.3; copia con UNA entrada nueva para el candidato)."""
    org, regla, seed = args
    t0 = time.time()
    o = (G144.tarea(('organismo_v144b', regla, seed)) if org == 'CAND' else G143.tarea(('organismo_v143', regla, seed)))
    o.update(org=org, seg=round(time.time() - t0, 2))
    return o


# ------------------------------------------------------------------ infraestructura (log, Pool, crudos, subprocesos)
_log = {'f': None, 't0': time.time(), 'nom': None}


def log(msg=''):
    linea = f"[{time.strftime('%H:%M:%S')} +{time.time() - _log['t0']:7.1f}s] {msg}"
    print(linea, flush=True)
    if _log['f']:
        _log['f'].write(linea + '\n'); _log['f'].flush(); os.fsync(_log['f'].fileno())


def pool_map(fn, tareas, etq, n):
    if n <= 1:
        res = []
        for i, t in enumerate(tareas, 1):
            res.append(fn(t))
            if i % 20 == 0 or i == len(tareas):
                log(f'          {etq} {i}/{len(tareas)}')
        return res
    import multiprocessing as mp
    try:
        mp.set_start_method('spawn', force=True)
    except RuntimeError:
        pass
    res = []
    with mp.Pool(n) as pool:
        for i, r in enumerate(pool.imap_unordered(fn, tareas, chunksize=1), 1):
            res.append(r)
            if i % 40 == 0 or i == len(tareas):
                log(f'          {etq} {i}/{len(tareas)}')
    return res


def crudo(etq, res, carpeta, extra=None):
    """ERR-54: crudos a disco ANTES del analisis, y el analisis los RELEE del disco."""
    f = os.path.join(carpeta, f"{_log['nom']}_crudo_{etq}.json")
    json.dump(dict(meta=dict(etapa=etq, fecha=time.strftime('%Y-%m-%dT%H:%M:%S'), n=len(res), extra=extra), corridas=res),
              open(f, 'w', encoding='utf-8'), ensure_ascii=False, default=str)
    log(f'   CRUDO ({len(res)} corridas) -> {os.path.basename(f)}  sha256_16 = {h16(f)}')
    return json.load(open(f, encoding='utf-8'))['corridas']


def procesos_python():
    try:
        if os.name == 'nt':
            cmd = ['powershell', '-NoProfile', '-Command',
                   "Get-CimInstance Win32_Process | Where-Object { $_.Name -like 'python*' } | "
                   "ForEach-Object { \"$($_.ProcessId) $($_.CommandLine)\" }"]
        else:
            cmd = ['ps', '-eo', 'pid,args']
        out = subprocess.run(cmd, capture_output=True, text=True, timeout=60).stdout.strip().splitlines()
        return [l for l in out if 'python' in l.lower()] if os.name != 'nt' else out
    except Exception as e:
        return [f'(no se pudo listar: {e})']


def N_(x):
    return json.dumps(x, sort_keys=True, default=str)


# ------------------------------------------------------------------ REGLA 14 y guardas (sin simular un paso)
def guarda_semillas_TD(modo):
    """La seleccion estructural de T-D se RECALCULA: si no coincide con umbrales_examen_v144c.SEMILLAS, no se corre."""
    import diagnostico_codigos as DC
    S = U.SEMILLAS[modo]
    lo, hi = S['TD_rango']
    a = [s for s in range(lo, hi + 1) if DC.solapamientos(s)['D&B'] >= 3][:9]
    l = [s for s in range(lo, hi + 1) if DC.solapamientos(s)['D&B'] == 0][:9]
    return a == S['ALIAS'] and l == S['LIMPIAS'], dict(alias=a, limpias=l)


def _defectos(f):
    import inspect
    return {k: v.default for k, v in inspect.signature(f).parameters.items() if v.default is not inspect.Parameter.empty}


def regla14():
    """(nombre, ok) por comprobacion. Kwargs campo a campo contra el montaje del tronco; baterias copiadas contra las
    congeladas; letra de este examen == la del examen de v14.3 == la de los modulos de donde se importa; semillas disjuntas."""
    import organismo_v143 as V143, organismo_v144b as V144, organismo_v143g as V143G, organismo_v144bg as V144G
    import organismo_v143cal as V143C, organismo_v144bcal as V144C, organismo_v3cal as CAL
    import corre_codigo as CC, umbrales_examen_v143 as U143
    R = []
    dif = lambda a, b: sorted({k for k in set(a) | set(b) if a.get(k, '<falta>') != b.get(k, '<falta>')})
    for b in U.BRAZOS_TA:
        off = C4.kw_vivo(b, 'OFF')
        R.append((f'R1 T-A {b}: OFF == corre_vivo_rep2.BRAZOS[{b}] + desambiguar=1 + placebo=0 (el montaje de V4-CAL)',
                  off == dict(CR2.BRAZOS[b], desambiguar=1, placebo=0)))
        R.append((f'R1 T-A {b}: CAND difiere de OFF SOLO en norm_lenta=1 y termo=1', dif(kw_vivo_cand(b), off) == ['norm_lenta', 'termo']
                  and kw_vivo_cand(b)['termo'] == 1 and kw_vivo_cand(b)['norm_lenta'] == 1))
        R.append((f'R1 T-A {b}: CTRL (TERMOINV) difiere de OFF SOLO en norm_lenta=1 y termo=2', dif(kw_vivo_ctrl(b), off) == ['norm_lenta', 'termo']
                  and kw_vivo_ctrl(b)['termo'] == 2))
        R.append((f'R1 T-A {b}: TRONCO_B == OFF campo a campo', C4.kw_vivo(b, 'TRONCO_B') == off))
        R.append((f'R1 T-A {b}: PLACEBO difiere de OFF SOLO en placebo=1', dif(C4.kw_vivo(b, 'PLACEBO'), off) == ['placebo']
                  and C4.kw_vivo(b, 'PLACEBO')['placebo'] == 1))
        R.append((f'R1 T-A {b}: la consigna de TERMO es rep_umbral = 1.0 (la de la pista: S = 1.4 con s = 0.8, PREREGISTRO_termo sec. 2)',
                  off['rep_umbral'] == 1.0))
    off = C4.kw_rev('OFF', U.T_VIVO)
    R.append(('R1 T-C ii: OFF == mini_vivo.BRAZOS[VIVO] + desambiguar=1 + invertir_vivo_en=T/2 + placebo=0',
              off == dict(MV.BRAZOS['VIVO'], desambiguar=1, invertir_vivo_en=U.T_VIVO // 2, placebo=0)))
    R.append(('R1 T-C ii: CAND difiere de OFF SOLO en norm_lenta=1 y termo=1', dif(kw_rev_cand(U.T_VIVO), off) == ['norm_lenta', 'termo']))
    R.append(('R1 T-C ii: TRONCO_B == OFF', C4.kw_rev('TRONCO_B', U.T_VIVO) == off))
    R.append(('R1 T-C ii y T-D: sin rep_umbral en los kwargs -> la consigna es el DEFECTO de organismo_v144bcal, 1.0 (declarado)',
              'rep_umbral' not in off and 'rep_umbral' not in kw_sal('CAND') and _defectos(V144C.run)['rep_umbral'] == 1.0))
    R.append(('R1 T-D: OFF == corre_sal.BASE (sal muda) + desambiguar=1 + placebo=0; CAND == OFF + norm_lenta=1 + termo=1',
              kw_sal('OFF') == dict(CS.BASE, desambiguar=1, placebo=0) and dif(kw_sal('CAND'), kw_sal('OFF')) == ['norm_lenta', 'termo']))
    R.append(('R1 TRONCO_B = semilla s + 100000 (umbrales_v4)', C4.DESPL == U.DESPL_TRONCO_B
              and C4.semilla_real(53201, 'TRONCO_B') == 153201 and C4.semilla_real(53201, 'OFF') == 53201))
    R.append(('R1 el OFF del mundo vivo (organismo_v3cal = v14.2) y organismo_v143cal: mismos defectos salvo norm_lenta (v14.3 = v14.2 + N, '
              'inerte con masa 3; la igualdad bit a bit la prueba el arnes (A\'))',
              dif(_defectos(V143C.run), _defectos(CAL.run)) == ['norm_lenta']))
    # R2 examen v3'
    R.append(('R2 bateria_v144b.ETAPAS == bateria_v143.ETAPAS (campo a campo)', N_(B144.ETAPAS) == N_(B143.ETAPAS)))
    R.append(('R2 bateria_v144b: SEIS, ESC_ID, EVENTO == bateria_v143', B144.SEIS == B143.SEIS == U.SEIS == D5.SEIS
              and N_(B144.ESC_ID) == N_(B143.ESC_ID) and B144.EVENTO == B143.EVENTO))
    R.append(('R2 bateria_v144b.CRIT: mismas etapas y mismos nombres que bateria_v143',
              {e: list(c) for e, c in B144.CRIT.items()} == {e: list(c) for e, c in B143.CRIT.items()}))
    # R3 generalizacion
    R.append(('R3 bateria_generaliza_v144b: organismo_v144b -> (organismo_v144bg, kwargs CAMPO A CAMPO == organismo_v143)',
              G144.INSTRUMENTOS['organismo_v144b'][0] == 'organismo_v144bg'
              and G144.INSTRUMENTOS['organismo_v144b'][1] == G143.INSTRUMENTOS['organismo_v143'][1]))
    R.append(('R3 bateria_generaliza_v144b: las entradas anteriores intactas; REGLAS == [px0, azar]',
              all(G144.INSTRUMENTOS[k] == G143.INSTRUMENTOS[k] for k in G143.INSTRUMENTOS)
              and set(G144.INSTRUMENTOS) - set(G143.INSTRUMENTOS) == {'organismo_v144', 'organismo_v144b'} and G144.REGLAS == G143.REGLAS == U.REGLAS_TB))
    d143g, d144g = _defectos(V143G.run), _defectos(V144G.run)
    R.append(('R3 organismo_v144bg: mismos defectos que organismo_v143g + termo=1 y rep_umbral=1.0 (la pieza, encendida por defecto)',
              all(d144g[k] == v for k, v in d143g.items()) and set(d144g) - set(d143g) == {'termo', 'rep_umbral'}
              and d144g['termo'] == 1 and d144g['rep_umbral'] == 1.0))
    # R4 los organismos: lo unico nuevo es la pieza
    d143, d144 = _defectos(V143.run), _defectos(V144.run)
    R.append(('R4 organismo_v144b: mismos defectos que organismo_v143 + termo=1 y rep_umbral=1.0',
              all(d144[k] == v for k, v in d143.items()) and set(d144) - set(d143) == {'termo', 'rep_umbral'}
              and d144['termo'] == 1 and d144['rep_umbral'] == 1.0))
    dc3, dc4 = _defectos(V143C.run), _defectos(V144C.run)
    R.append(('R4 organismo_v144bcal: mismos defectos que organismo_v143cal + termo=1 (rep_umbral ya existia: 1.0)',
              all(dc4[k] == v for k, v in dc3.items()) and set(dc4) - set(dc3) == {'termo'} and dc4['termo'] == 1))
    R.append(('R4 organismo_v144b/v144g/v144cal y sus origenes: mismas constantes de modulo (L, NK, NKMAX, K, PAT, R_VAL, E_VAL)',
              all(N_(getattr(a, c)) == N_(getattr(b, c)) for a, b in ((V143, V144), (V143G, V144G), (V143C, V144C))
                  for c in ('L', 'NK', 'NKMAX', 'K', 'R_VAL', 'E_VAL'))
              and all(np.array_equal(a.PAT[k], b.PAT[k]) for a, b in ((V143, V144), (V143G, V144G), (V143C, V144C)) for k in a.PAT)))
    import inspect
    R.append(('R4 la letra de la pieza (termo_letra) es el MISMO texto en organismo_v144b, v144g y v144cal',
              inspect.getsource(V144.termo_letra) == inspect.getsource(V144G.termo_letra) == inspect.getsource(V144C.termo_letra)))
    # R5 la letra de este examen == la del examen de v14.3 == la de los modulos de donde se importa (ERR-31)
    R.append(('R5 NUM == umbrales_examen_v143.NUM y ERR122 == el de v14.3 (MISMA letra, SIN cambios)',
              N_(U.NUM) == N_(U143.NUM) and N_(U.ERR122) == N_(U143.ERR122)))
    R.append(('R5 LETRA de T-A, T-B, T-C (i), T-D, T-E, T-F y T-H == umbrales_examen_v143.LETRA (texto identico)',
              all(U.LETRA[k] == U143.LETRA[k] for k in ('T-A', 'T-B', 'T-C_i', 'T-D', 'T-E', 'T-F', 'T-H'))))
    R.append(('R5 ERR-150: LETRA[T-C_ii] == la frase de ERR-150; la VIEJA (rev absoluto) == umbrales_examen_v143.LETRA[T-C_ii] '
              '(se reporta) == umbrales_examen_v144b; T-G == la de v14.4b',
              U.LETRA['T-C_ii'] == U.ERR150['frase'] and U.LETRA_TC_ii_REV_V4 == U143.LETRA['T-C_ii'] == U.ERR150['rev_v4_solo_informe']
              and U.LETRA['T-G'] == U.U144B.LETRA['T-G'] and N_(U.TG) == N_(U.U144B.TG)))
    jn150 = json.load(open(os.path.join(RAIZ, U.ERR150['nulo']['fuente']), encoding='utf-8'))
    R.append(('R5 ERR-150: margen 0.125 == el del JSON del nulo (0.30 x (mediana S4 - 0.5)); z == NUM[z]; n == NUM[n_vivo]; '
              'suelo 0.5; el JSON dice que la regla se sostiene y que tumba a TERMO; sha del JSON == el declarado',
              U.ERR150['margen'] == jn150['margen']['C'] and U.ERR150['z'] == U.NUM['z'] == jn150['z'] and U.ERR150['n'] == U.NUM['n_vivo'] == jn150['n']
              and U.ERR150['suelo_S4'] == 0.5 and all(jn150['condiciones'].values()) and jn150['anti_TERMO']['tumba'] is True
              and h16(os.path.join(RAIZ, U.ERR150['nulo']['fuente'])) == U.ERR150['nulo']['sha']))
    u4 = C4.U.V4; n = U.NUM
    R.append(('R5 T-A == umbrales_v4.V4[T-A] (1.10, 10, margen 10, z 1.645, n 80)',
              (u4['T-A']['muertes'], u4['T-A']['r_delta'], u4['T-A']['margen'], u4['T-A']['z'], u4['T-A']['n'])
              == (n['TA_muertes'], n['TA_r_delta'], n['TA_margen'], n['z'], n['n_vivo'])))
    R.append(('R5 T-C ii == umbrales_v4.V4[T-C_ii] (margen 12.5, n 80); T-F == 1.25',
              (u4['T-C_ii']['margen'], u4['T-C_ii']['n'], u4['T-F_vivo']['razon']) == (n['TC_margen'], n['n_vivo'], n['TF_razon'])))
    ub = D5.UMB['T-B']
    R.append(('R5 T-B == corre_dE5_v2.UMB[T-B] en G1, G2 y azar G1 (0.80, 0.85, [0.35, 0.65]): sin cambio',
              (ub['g1'], ub['g2'], tuple(ub['azar'])) == (n['TB_g1'], n['TB_g2'], n['TB_azar'])))
    R.append(('R5 T-B azar G2: [0.31, 0.60] (ERR-122, la letra con la que entro v14.3); el origen corre_dE5_v2 [0.42, 0.58] == la '
              'banda vieja, que solo se reporta',
              tuple(n['TB_azar2']) == tuple(U.ERR122['banda_nueva']) == (0.31, 0.60)
              and tuple(ub['azar2']) == tuple(U.ERR122['banda_vieja']) == (0.42, 0.58)))
    R.append(('R5 T-E / T-C i / T-F examen == corre_dE5_v2 (TOL 1.10, TOL_COME 0.8, PUERTA_E 18, factor 1.25)',
              (D5.TOL, D5.TOL_COME, D5.PUERTA_E, D5.UMB['T-F']['factor']) == (n['tol'], n['tol_come'], n['puerta_E'], n['TF_razon'])
              and 'come B Q4 >= 50 (T-C i)' in [c for c, _ in D5.CLAUSULAS['E2']]))
    R.append(('R5 T-D: C1, C2, C6 existen en creacion_B/corre_codigo.UMBRALES (se importan, no se copian)',
              all(k in CC.UMBRALES for k in ('C1', 'C2', 'C6'))))
    jn = json.load(open(os.path.join(RAIZ, 'datos', 'humo', 'potencia_examen_v144_20260928_121917.json'), encoding='utf-8'))
    bc = jn['brazos'][U.TG['brazo']]
    R.append(('R5 T-G: brazo CUELLO_MIN, z 1.645 (== T-A), n 80 (== n_vivo), m = 1 == el m elegido por analiza_potencia_v144 sobre el '
              'nulo real; P(T-G | nulo) 0.042 y P(T-G) en delta 6: 0.877 == el JSON',
              U.TG['z'] == n['z'] and U.TG['n'] == n['n_vivo'] == jn['n'] and U.TG['m'] == bc['m_elegido'] == 1
              and U.TG['nulo']['P_TG'] == bc['P_TG_nulo'] and U.TG['delta_margen'] == bc['margen_80'] == 6
              and U.TG['nulo']['P_TG_delta6'] == bc['potencia_TG_en_margen']))
    # R6 semillas: disjuntas entre papeles y fuera de lo ya usado
    todas = []
    for modo in ('serie', 'replica', 'reserva'):
        S = U.SEMILLAS[modo]
        for k in ('EX', 'VIVO', 'ALIAS', 'LIMPIAS'):
            todas += [(s, modo, k) for s in S.get(k, [])]
    todas += [(s, 'humo', '') for s in U.SEMILLAS['humo']] + [(s, 'identidad', '') for s in U.SEMILLAS['identidad']]
    ss = [s for s, _, _ in todas]
    usadas = (set(range(2841, 2941)) | set(range(2361, 2441)) | set(range(7701, 7741)) | set(range(14281, 14341))
              | set(range(43000, 44601)) | set(range(39001, 39141)) | set(range(39901, 39915))
              | set(range(47000, 48601)) | set(range(49001, 50000)) | set(range(149000, 150000)))
    R.append(('R6 semillas: todas distintas entre papeles, dentro de 53100-53999 / 153500-153999, ninguna de V4-CAL, subida_n7, tronco_v14_3, los '
              'examenes de v14.3, v14.4 y v14.4b (49xxx y 149xxx enteros), TERMO ni TERMO\'; TRONCO_B s+100000 libre',
              len(ss) == len(set(ss)) and not (set(ss) & usadas) and all(53100 <= s <= 53999 or 153500 <= s <= 153999 for s in ss)))
    for modo in ('serie', 'replica'):
        ok, _ = guarda_semillas_TD(modo)
        R.append((f'R6 T-D {modo}: las 9 ALIAS y 9 LIMPIAS recalculadas == las declaradas', ok))
    return R


# ------------------------------------------------------------------ VEREDICTOS (la letra; una linea por puerta, ERR-89)
def med(xs):
    xs = [x for x in xs if x is not None]
    return None if not xs else float(np.median(xs))


def _n(x, fmt='.3f'):
    """Formato que no se cae con None (una linea de log no puede tumbar un veredicto ya medido)."""
    return 'n/a' if x is None else format(x, fmt)


def iguales(a, b, fuera=('arm', 'org', 'seg', 'modulo', 'seed_real', '_lado', 'termo')):
    ks = sorted((set(a) | set(b)) - set(fuera))
    return N_({k: a.get(k) for k in ks}) == N_({k: b.get(k) for k in ks})


def inercia(res, clave, cand, ref):
    """Cuantas corridas del candidato son IDENTICAS (todas las claves medidas) a las del tronco en la misma semilla. En v14.4 la
    pieza ACTUA: se espera lejos de n/n (es lectura, no puerta)."""
    A = {clave(r): r for r in res if r['_lado'] == cand}; B = {clave(r): r for r in res if r['_lado'] == ref}
    comun = sorted(set(A) & set(B), key=str)
    return sum(iguales(A[k], B[k]) for k in comun), len(comun)


def banda_TB():
    """Los umbrales con los que el examen DECIDE T-B (los del examen de v14.3, ERR-122 incluida)."""
    u = D5.UMB['T-B']
    return dict(g1=u['g1'], g2=u['g2'], azar=tuple(u['azar']), azar2=tuple(U.NUM['TB_azar2']), azar2_vieja=tuple(u['azar2']))


def veredicto_TB(res):
    """T-B desde los valores CRUDOS de bateria_generaliza (acc, ba, cobertura por semilla), como en el examen de v14.3."""
    u = banda_TB()
    dentro = lambda x, b: bool(x is not None and b[0] <= x <= b[1])
    V = {}
    for org in U.ORGS_EX:
        R = [r for r in res if r['org'] == org]
        S = sorted({r['seed'] for r in R})
        px = {r['seed']: r for r in R if r['regla'] == 'px0'}; az = {r['seed']: r for r in R if r['regla'] == 'azar'}
        g1 = med([px[s]['acc'] for s in S]); g1az = med([az[s]['acc'] for s in S])
        g2 = med([px[s]['ba'] for s in S]); g2az = med([az[s]['ba'] for s in S])
        kc = sum(px[s]['cobertura'] >= U.NUM['TB_cob'] for s in S)
        c = dict(G1=g1, G1_azar=g1az, G2=g2, G2_azar=g2az, K=kc, n=len(S),
                 c_G1=bool(g1 is not None and g1 >= u['g1']), c_G2=bool(g2 is not None and g2 >= u['g2']),
                 c_azar1=dentro(g1az, u['azar']),
                 c_azar2=dentro(g2az, u['azar2']),                 # ERR-122: [0.31, 0.60] DECIDE
                 c_K=bool(kc == len(S)))
        c['pasa'] = bool(c['c_G1'] and c['c_G2'] and c['c_azar1'] and c['c_azar2'] and c['c_K'])
        c['c_azar2_banda_vieja'] = dentro(g2az, u['azar2_vieja'])
        c['pasa_banda_vieja'] = bool(c['c_G1'] and c['c_G2'] and c['c_azar1'] and c['c_azar2_banda_vieja'] and c['c_K'])
        V[org] = c
    for r in res:
        r['_lado'] = r['org']
    V['inercia'] = inercia(res, lambda r: (r['regla'], r['seed']), 'CAND', 'TRONCO')
    V['pasa'] = V['CAND']['pasa']
    V['banda_azar2'] = dict(err='ERR-122', decide=list(u['azar2']), vieja_solo_informe=list(u['azar2_vieja']))
    log(f"   T-B: CAND = v14.4 (bateria_generaliza_v144b) y TRONCO = v14.3 (bateria_generaliza_v143, CONGELADA) en las MISMAS "
        f"semillas; azar G2 decide con {list(u['azar2'])} (ERR-122) para los dos")
    for org in U.ORGS_EX:
        c = V[org]
        log(f"   T-B [{org:6s}] G1 {_n(c['G1'])} (>= {u['g1']}) G2 {_n(c['G2'])} (>= {u['g2']}) azar G1 {_n(c['G1_azar'])} "
            f"(en {list(u['azar'])}) azar G2 {_n(c['G2_azar'])} (en {list(u['azar2'])}, ERR-122) K {c['K']}/{c['n']} -> "
            f"{'PASA' if c['pasa'] else 'NO'}   [G1 {c['c_G1']} G2 {c['c_G2']} azar1 {c['c_azar1']} azar2 {c['c_azar2']} K {c['c_K']}]")
    log(f"   T-B banda VIEJA de azar G2 {list(u['azar2_vieja'])} (SOLO INFORME, NO decide; ERR-122): "
        + ' | '.join(f"{org} azar G2 {_n(V[org]['G2_azar'])} {'dentro' if V[org]['c_azar2_banda_vieja'] else 'FUERA'} -> T-B "
                     f"{'PASA' if V[org]['pasa_banda_vieja'] else 'NO'}" for org in U.ORGS_EX))
    log(f"   T-B lectura: CAND == TRONCO (todas las claves) en {V['inercia'][0]}/{V['inercia'][1]} corridas (regla x semilla)")
    return V


def veredicto_EX(res):
    jc = dict(corridas=[r for r in res if r['org'] == 'CAND']); jt = dict(corridas=[r for r in res if r['org'] == 'TRONCO'])
    con = D5.conducta(jc, jt); cost = D5.coste_examen(jc, jt); con_t = D5.conducta(jt, jt)
    ci = con['E2']['detalle']['come B Q4 >= 50 (T-C i)']
    for r in res:
        r['_lado'] = r['org']
    V = dict(conducta=con, coste=cost, T_C_i=dict(comeB_Q4=ci, n=con['E2']['n'], pasa=bool(ci >= D5.PUERTA_E)),
             T_E=dict(pasa=bool(all(con[e]['pasa'] for e in U.SEIS))), T_F=dict(pasa=bool(all(cost[q]['pasa'] for q in cost))),
             tronco_letra_absoluta=dict(E2_comeB=con_t['E2']['detalle']['come B Q4 >= 50 (T-C i)'],
                                        E2I_tasa=con_t['E2I']['detalle']['tasaA Q4 >= 80% Q2']),
             inercia=inercia(res, lambda r: (r['etapa'], r['seed']), 'CAND', 'TRONCO'),
             mordA_Q4_E2=dict(cand=med([r['mord']['A'][3] for r in jc['corridas'] if r['etapa'] == 'E2']),
                              tronco=med([r['mord']['A'][3] for r in jt['corridas'] if r['etapa'] == 'E2'])))
    for e in U.SEIS:
        log(f"      T-E {e:4s} {con[e]['todas']}/{con[e]['n']} {'PASA' if con[e]['pasa'] else 'NO'}  {con[e]['detalle']}  "
            f"pesos (reportados) {con[e]['pesos_reportados']}")
    log(f"   T-C (i) [{U.LETRA['T-C_i']}] -> {ci}/{con['E2']['n']} -> {'PASA' if V['T_C_i']['pasa'] else 'NO'}")
    log(f"   T-E [{U.LETRA['T-E']}] -> " + ' '.join(f"{e} {con[e]['todas']}/{con[e]['n']}" for e in U.SEIS)
        + f" -> {'PASA' if V['T_E']['pasa'] else 'NO'}")
    log(f"   T-F examen [<= {D5.UMB['T-F']['factor']} x tronco] -> " + ' '.join(f"{q} {cost[q]['cand']}/{cost[q]['tronco']} ({cost[q]['razon']}x)" for q in cost)
        + f" -> {'PASA' if V['T_F']['pasa'] else 'NO'}")
    log(f"   examen: el TRONCO contra las clausulas absolutas: E2 come B >= 50 {V['tronco_letra_absoluta']['E2_comeB']}/20, "
        f"E2I tasa {V['tronco_letra_absoluta']['E2I_tasa']}/20; CAND == TRONCO {V['inercia'][0]}/{V['inercia'][1]}; "
        f"E2 muerde A en Q4 (mediana) CAND {V['mordA_Q4_E2']['cand']} / TRONCO {V['mordA_Q4_E2']['tronco']} (la prediccion de sec. 5)")
    return V


def veredicto_TD(res):
    import corre_codigo as CC
    u1, u2, u6 = CC.UMBRALES['C1'], CC.UMBRALES['C2'], CC.UMBRALES['C6']
    V = {'letra': {k: CC.UMBRALES[k]['frase'] for k in ('C1', 'C2', 'C6')}}
    for arm in U.ARMS_SAL:
        A = [r for r in res if r['arm'] == arm and r['brazo'] == 'S1-ALIAS']
        L = [r for r in res if r['arm'] == arm and r['brazo'] == 'S1-LIMPIA']
        if not A or not L:
            continue
        c1 = sum(r['w_sal'] <= u1['w'] for r in A); m1 = med([r['w_sal'] for r in A])
        c2a = sum(r['w_veneno'] <= u2['w1'] for r in A); c2b = sum(r['w_veneno'] <= u2['w2'] for r in A)
        c6a = sum(r['w_sal'] <= u6['w'] for r in L); c6b = sum(r['w_veneno'] <= u6['wv'] for r in L)
        V[arm] = dict(C1=dict(n=c1, med=m1, pasa=bool(c1 >= u1['n_min'] and (m1 if m1 is not None else 9) <= u1['med_max'])),
                      C2=dict(n28=c2a, n25=c2b, med=med([r['w_veneno'] for r in A]), pasa=bool(c2a >= u2['n1'] and c2b == len(A) and len(A) == u2['n2'])),
                      C6=dict(sal=c6a, veneno=c6b, pasa=bool(c6a == u6['n_min'] and c6b == u6['n_min'] and len(L) == u6['n_min'])),
                      exp_sal=med([r['exp_sal'] for r in A]), des_splits=med([r['des_splits'] for r in A]),
                      muertes_alias=med([r['deaths'] for r in A]), muertes_limpias=med([r['deaths'] for r in L]))
        V[arm]['pasa'] = bool(V[arm]['C1']['pasa'] and V[arm]['C2']['pasa'] and V[arm]['C6']['pasa'])
    for r in res:
        r['_lado'] = r['arm']
    V['inercia'] = inercia(res, lambda r: (r['brazo'], r['seed']), 'CAND', 'OFF')
    V['pasa'] = bool(V.get('CAND', {}).get('pasa'))
    for arm in U.ARMS_SAL:
        if arm in V:
            v = V[arm]
            log(f"   T-D [{arm:4s}] C1 {v['C1']}  C2 {v['C2']}  C6 {v['C6']}  exp sal {v['exp_sal']}  des_splits {v['des_splits']}  "
                f"muertes alias/limpias {v['muertes_alias']}/{v['muertes_limpias']} -> {'PASA' if v['pasa'] else 'NO'}")
    log(f"   T-D lectura: CAND == OFF (todas las claves) en {V['inercia'][0]}/{V['inercia'][1]}")
    return V


def _tele(rs):
    t = [r.get('termo') for r in rs if r.get('termo')]
    if not t:
        return None
    return dict(n=len(t), dec=med([x['dec'] for x in t]), a_no=med([x['a_no'] for x in t]), a_si=med([x['a_si'] for x in t]),
                mord=med([x['mord'] for x in t]), actua=sum(1 for x in t if x['a_no'] + x['a_si'] > 0))


# ------------------------------------------------------------------ ERR-150: T-C (ii) POR VISITA (la letra que DECIDE en v14.4c)
def _tasa(m, v):
    """Tasa de mordida por visita con el +1/+2 de Laplace (vis = pasos sobre el objeto = decisiones de la boca)."""
    return (m + 1.0) / (v + 2.0)


def _pref(r, q, bueno, malo):
    pb, pm = _tasa(r['mord' + bueno][q], r['vis' + bueno][q]), _tasa(r['mord' + malo][q], r['vis' + malo][q])
    return pb / (pb + pm)


def S4_visita(r):
    """DESPUES de la reversion (Q4): preferencia por visita por lo que AHORA es bueno (B)."""
    return _pref(r, U.ERR150['cuarto_despues'], 'B', 'A')


def S2_visita(r):
    """ANTES de la reversion (Q2): la misma preferencia por lo que ENTONCES era bueno (A)."""
    return _pref(r, U.ERR150['cuarto_antes'], 'A', 'B')


def C_visita(r):
    """Cuanto se desdice, contra si mismo: 0 = distingue despues tan bien como antes."""
    return S4_visita(r) - S2_visita(r)


def letra_TC_visita(off, cand):
    """ERR-150: (a) NO INFERIORIDAD (corre_criterio_v3.no_inferior, la de v4) sobre C con margen 0.125; (b) mediana S4 > 0.5.
    off, cand: listas ordenadas por semilla-etiqueta (C4.G)."""
    u = U.ERR150
    ni_ = C4.no_inferior([C_visita(r) for r in cand], [C_visita(r) for r in off], u['margen'], u['z'])
    s4 = med([S4_visita(r) for r in cand]); s4o = med([S4_visita(r) for r in off])
    s2 = med([S2_visita(r) for r in cand]); s2o = med([S2_visita(r) for r in off])
    suelo = bool(s4 is not None and s4 > u['suelo_S4'])
    return bool(ni_['pasa'] and suelo and len(cand) == len(off) == u['n']), dict(
        NI_C=ni_, suelo=suelo, S4=(s4, s4o), S2=(s2, s2o), C=(med([C_visita(r) for r in cand]), med([C_visita(r) for r in off])),
        n=(len(cand), len(off)))


def tc_err150(Vc, res_rev, cand):
    """Sustituye la T-C (ii) de corre_criterio_v4.juzga (rev absoluto) por la POR VISITA; la vieja queda como informe."""
    if 'T-C_ii' not in Vc:
        return
    p, det = letra_TC_visita(C4.G(res_rev, 'OFF'), C4.G(res_rev, cand))
    Vc['T-C_ii']['rev_absoluto_v4'] = dict(pasa=Vc['T-C_ii']['v4'], det=Vc['T-C_ii']['det_v4'], solo_informe=True)
    Vc['T-C_ii']['v4'] = p
    Vc['T-C_ii']['det_visita'] = det
    Vc['T-C_ii']['letra'] = 'ERR-150'
    Vc['v4'] = bool(Vc.get('T-A', {}).get('v4', True) and p and Vc.get('T-F_vivo_TA', True) and Vc.get('T-F_vivo_TC', True))
    ni_ = det['NI_C']
    log(f"   T-C ii POR VISITA (ERR-150) [{cand:8s}] S2 {_n(det['S2'][0])}/{_n(det['S2'][1])} S4 {_n(det['S4'][0])}/{_n(det['S4'][1])} "
        f"C {_n(det['C'][0], '+.4f')}/{_n(det['C'][1], '+.4f')} | NI sobre C media {ni_['media']} sd {ni_.get('sd')} LI {ni_['LI']} > "
        f"-{U.ERR150['margen']} -> {ni_['pasa']} | suelo S4 > {U.ERR150['suelo_S4']} -> {det['suelo']} => {'PASA' if p else 'NO'} "
        f"(rev absoluto, SOLO INFORME: {'PASA' if Vc['T-C_ii']['rev_absoluto_v4']['pasa'] else 'NO'})")
    log(f"   >>> {cand}: v4 del mundo vivo con ERR-150 (T-A, T-C ii POR VISITA, T-F vivo) {'PASA' if Vc['v4'] else 'NO PASA'}")


def veredicto_vivo(res_vivo, res_rev):
    """T-A, T-C (ii), T-F vivo con la letra CALIBRADA (corre_criterio_v4.juzga; v3 y v2 al lado, sin decidir). Las filas CTRL de
    T-A (control de T-G) no entran: juzga filtra por brazo y arm."""
    C4._log.update(f=_log['f'], t0=_log['t0'])   # que las lineas de la letra calibrada caigan en ESTE log
    V = {c: C4.juzga(res_vivo, res_rev, c) for c in ('CAND', 'TRONCO_B', 'PLACEBO')}
    log("   (ERR-150) las lineas 'T-C ii' y '>>>' de arriba (corre_criterio_v4.juzga) usan rev ABSOLUTO: SOLO INFORME. "
        "DECIDE la T-C (ii) POR VISITA:")
    for c in ('CAND', 'TRONCO_B', 'PLACEBO'):
        tc_err150(V[c], res_rev, c)
    C4._log.update(f=None)
    for r in res_vivo:
        r['_lado'] = r['arm']
    for r in res_rev:
        r['_lado'] = r['arm']
    V['inercia_TA'] = inercia(res_vivo, lambda r: (r['brazo'], r['seed']), 'CAND', 'OFF')
    V['inercia_TC'] = inercia(res_rev, lambda r: r['seed'], 'CAND', 'OFF')
    V['legible'] = bool(V['TRONCO_B']['v4'])
    V['termo_TA'] = {b: _tele([r for r in res_vivo if r['arm'] == 'CAND' and r['brazo'] == b]) for b in U.BRAZOS_TA}
    V['termo_TC'] = _tele([r for r in res_rev if r['arm'] == 'CAND'])
    log(f"   la pieza en el mundo vivo (medianas por corrida: decisiones gobernadas, a_no, a_si; corridas donde actua): "
        f"T-A {V['termo_TA']} | T-C (ii) {V['termo_TC']}")
    log(f"   lectura: CAND == OFF (todas las claves) en T-A {V['inercia_TA'][0]}/{V['inercia_TA'][1]}, "
        f"T-C (ii) {V['inercia_TC'][0]}/{V['inercia_TC'][1]} (la pieza actua: se espera lejos de n/n)")
    log(f"   TRONCO_B (el tronco contra si mismo, s+100000) {'PASA' if V['legible'] else '*** NO PASA: la serie del mundo vivo NO SE LEE'} | "
        f"PLACEBO (reportado) {'PASA' if V['PLACEBO']['v4'] else 'NO'}")
    return V


def _li(d, z):
    d = np.asarray(d, float)
    if len(d) < 2:
        return None, None, None
    m, s = float(d.mean()), float(d.std(ddof=1))
    return round(m, 3), round(s, 3), round(m - z * s / np.sqrt(len(d)), 3)


def veredicto_TG(res_vivo):
    """T-G (PREREGISTRO sec. 4): en CUELLO_MIN, G-1 LI(r_CAND - r_OFF) > m; G-2 LI(r_CTRL - r_OFF) <= m; G-3 la pieza actua en
    >= 95 % de las corridas del CANDIDATO. VIVO: las mismas cuentas, SOLO INFORME."""
    z, m = U.TG['z'], U.TG['m']
    V = {}
    for b in (U.TG['brazo'], U.TG['informe']):
        g = lambda arm: {r['seed']: r for r in res_vivo if r['brazo'] == b and r['arm'] == arm}
        off, cand, ctrl = g('OFF'), g('CAND'), g(U.TG['ctrl'])
        sc = sorted(set(off) & set(cand)); sk = sorted(set(off) & set(ctrl))
        mc, sdc, lic = _li([cand[s]['r'] - off[s]['r'] for s in sc], z)
        mk, sdk, lik = _li([ctrl[s]['r'] - off[s]['r'] for s in sk], z)
        tc = [cand[s].get('termo') for s in sc]
        act = sum(1 for t in tc if t and t['a_no'] + t['a_si'] > 0)
        x = dict(n_cand=len(sc), n_ctrl=len(sk),
                 r=dict(OFF=med([off[s]['r'] for s in off]), CAND=med([cand[s]['r'] for s in cand]), CTRL=med([ctrl[s]['r'] for s in ctrl])),
                 muertes=dict(OFF=med([off[s]['deaths'] for s in off]), CAND=med([cand[s]['deaths'] for s in cand]),
                              CTRL=med([ctrl[s]['deaths'] for s in ctrl])),
                 descendientes=dict(OFF=med([off[s]['descendientes'] for s in off]), CAND=med([cand[s]['descendientes'] for s in cand]),
                                    CTRL=med([ctrl[s]['descendientes'] for s in ctrl])),
                 G1=dict(media=mc, sd=sdc, LI=lic, pasa=bool(lic is not None and lic > m)),
                 G2=dict(media=mk, sd=sdk, LI=lik, pasa=bool(lik is not None and lik <= m)),
                 G3=dict(actua=act, n=len(sc), frac=(round(act / len(sc), 3) if sc else None),
                         pasa=bool(sc and act / len(sc) >= U.TG['actua_frac'])),
                 termo_CAND=_tele(list(cand.values())), termo_CTRL=_tele(list(ctrl.values())))
        x['pasa'] = bool(x['G1']['pasa'] and x['G2']['pasa'] and x['G3']['pasa'] and len(sc) == len(sk) == U.TG['n'])
        V[b] = x
        log(f"      T-G {b:10s} {'(DECIDE)' if b == U.TG['brazo'] else '(informe)'} r mediana OFF {x['r']['OFF']} CAND {x['r']['CAND']} "
            f"CTRL {x['r']['CTRL']} | muertes {x['muertes']} | desc {x['descendientes']}")
        log(f"      T-G {b:10s} G-1 CAND-OFF media {mc} sd {sdc} LI {lic} > {m} -> {x['G1']['pasa']} | G-2 CTRL-OFF media {mk} sd {sdk} "
            f"LI {lik} <= {m} -> {x['G2']['pasa']} | G-3 actua {act}/{len(sc)} (>= {U.TG['actua_frac']}) -> {x['G3']['pasa']} | n {len(sc)}/{len(sk)}")
    P = V[U.TG['brazo']]
    V['pasa'] = P['pasa']
    log(f"   T-G [{U.LETRA['T-G']}] -> {'PASA' if V['pasa'] else 'NO'}")
    return V


SUB = ('T-A', 'T-B', 'T-C_i', 'T-C_ii', 'T-D', 'T-E', 'T-F_examen', 'T-F_vivo', 'T-G')
PUERTAS = ('T-A', 'T-B', 'T-C', 'T-D', 'T-E', 'T-F', 'T-G')


def subpuertas(V):
    """Las nueve sub-puertas medidas (None = no medida en esta corrida)."""
    viv = V.get('vivo'); c = None if viv is None else viv['CAND']
    return {
        'T-A': None if c is None or 'T-A' not in c else bool(c['T-A']['v4']),
        'T-B': None if 'TB' not in V else bool(V['TB']['pasa']),
        'T-C_i': None if 'EX' not in V else bool(V['EX']['T_C_i']['pasa']),
        'T-C_ii': None if c is None or 'T-C_ii' not in c else bool(c['T-C_ii']['v4']),
        'T-D': None if 'TD' not in V else bool(V['TD']['pasa']),
        'T-E': None if 'EX' not in V else bool(V['EX']['T_E']['pasa']),
        'T-F_examen': None if 'EX' not in V else bool(V['EX']['T_F']['pasa']),
        'T-F_vivo': None if c is None or 'T-A' not in c or 'T-C_ii' not in c else bool(c['T-F_vivo_TA'] and c['T-F_vivo_TC']),
        'T-G': None if 'TG' not in V else bool(V['TG']['pasa']),
    }


def _y(*xs):
    return None if any(x is None for x in xs) else bool(all(xs))


def puertas_de(sub):
    """Las siete puertas eliminatorias de v4 (una caida -> no entra); T-H reportada aparte."""
    return {'T-A': sub['T-A'], 'T-B': sub['T-B'], 'T-C': _y(sub['T-C_i'], sub['T-C_ii']), 'T-D': sub['T-D'],
            'T-E': sub['T-E'], 'T-F': _y(sub['T-F_examen'], sub['T-F_vivo']), 'T-G': sub['T-G']}


VIVAS = ('T-A', 'T-C_ii', 'T-F_vivo', 'T-G')   # lo que la RESERVA sustituye (todo lo que sale del mundo vivo)


def frase_serie(P, legible, modo):
    faltan = [k for k, v in P.items() if v is None]
    caen = [k for k, v in P.items() if v is False]
    if legible is False:
        return (f"NO SE LEE ({modo}): TRONCO_B no pasa la letra en el mundo vivo (4' de v4). Se corre la RESERVA "
                f"{U.SEMILLAS['reserva']['VIVO'][0]}-{U.SEMILLAS['reserva']['VIVO'][-1]} (--reserva --sustituye {modo})"
                + (f"; ya cae {', '.join(caen)} fuera del mundo vivo" if caen else ''))
    if faltan:
        return f"INCOMPLETO ({modo}): puertas sin medir {faltan}" + (f"; ya cae {', '.join(caen)}" if caen else '')
    if not caen:
        return f"PASA ({modo}): las siete puertas eliminatorias pasan (T-H no medida, reportada). Falta la otra serie."
    return f"NO PASA ({modo}): cae {', '.join(caen)} (una sola basta; sin modos intermedios)"


def combina(jsons):
    """El veredicto del EXAMEN por la letra: serie y replica legibles y con las siete puertas. La reserva (si la hay) solo
    sustituye lo del mundo vivo (T-A, T-C (ii), T-F vivo y T-G) de la serie cuyo mundo vivo no se leyo (--sustituye)."""
    por = {}
    for f in jsons:
        j = json.load(open(f, encoding='utf-8'))
        por.setdefault(j['meta']['modo'], []).append((os.path.basename(f), j))
    lineas = []
    if len(por.get('serie', [])) != 1 or len(por.get('replica', [])) != 1:
        return ("VEREDICTO DEL EXAMEN: INCOMPLETO (hace falta UNA serie y UNA replica; hay "
                + str({k: len(v) for k, v in por.items()}) + ")"), lineas
    estado = {}
    for modo in ('serie', 'replica'):
        nombre, j = por[modo][0]
        sub = dict(j['sub']); leg = j['legible']; nota = ''
        res = [(n, r) for n, r in por.get('reserva', []) if r['meta'].get('sustituye') == modo]
        if leg is False and res:
            n, r = res[0]
            leg = r['legible']
            for k in VIVAS:
                sub[k] = r['sub'][k]
            nota = f" (mundo vivo sustituido por la reserva {n})"
        P = puertas_de(sub)
        caen = [k for k in PUERTAS if P[k] is False]; faltan = [k for k in PUERTAS if P[k] is None]
        estado[modo] = ('NO SE LEE' if leg is False else ('NO PASA' if caen else ('INCOMPLETO' if faltan else 'PASA')))
        lineas.append(f"   {modo} [{nombre}]{nota}: legible {leg}; " + ' '.join(
            f"{k} {'PASA' if P[k] else ('NO' if P[k] is False else 'sin medir')}" for k in PUERTAS) + f" -> {estado[modo]}")
    e = set(estado.values())
    if e == {'PASA'}:
        return ("VEREDICTO DEL EXAMEN: PASA -- v14.4b (v14.3 + TERMOP) cruza la letra de CRITERIO_TRONCO_v4 con T-C (ii) POR VISITA (ERR-150) en serie y replica, en "
                "semillas nuevas. Congelarlo lo decide el director (PREREGISTRO sec. 10)."), lineas
    if 'NO PASA' in e:
        return ("VEREDICTO DEL EXAMEN: NO PASA -- v14.4b no se congela; v14.3 sigue siendo el tronco. Se lee DONDE cae "
                "(PREREGISTRO sec. 6)."), lineas
    if 'NO SE LEE' in e:
        return ("VEREDICTO DEL EXAMEN: NO SE LEE -- una serie del mundo vivo no se lee ni con la reserva; decide el coordinador "
                "con ERR (PREREGISTRO sec. 6)."), lineas
    return "VEREDICTO DEL EXAMEN: INCOMPLETO -- faltan puertas por medir.", lineas


# ------------------------------------------------------------------ crudos SINTETICOS (humo y arnes: cablear la etapa 8 sin simular)
def sinteticos(n_vivo, n_ex, alias, limpias, malo=False):
    """Numeros INVENTADOS con los formatos reales. No son evidencia. Bueno: CAND = OFF + 10 en r (gana), CTRL = OFF - 20 (no
    gana), la pieza actua, todo lo demas igual al tronco -> DEBE pasar las siete. MALO: CAND con r y rev 40 peor, azar G2 0.30,
    |W[sal]| 1.45 -> DEBE caer T-A, T-B, T-C, T-D y T-G."""
    g = np.random.default_rng(20260928)
    seeds_v = list(range(1, n_vivo + 1)); seeds_e = list(range(1, n_ex + 1))
    tele = dict(termo=1, U=1.0, dec=500, a_no=40, a_si=12, mord=470, adS={})
    RV, RR = [], []
    for b, (mr, sr) in (('VIVO', (-75.0, 12.0)), ('CUELLO_MIN', (-8.0, 13.5))):
        for s in seeds_v:
            base = dict(r=float(g.normal(mr, sr)), deaths=float(g.normal(94, 10)), celdas=37.0, splits=float(g.integers(4, 10)),
                        descendientes=20.0)
            for arm in U.ARMS_TA:
                if arm in ('OFF', 'CAND', 'CTRL'):
                    x = dict(base)
                else:
                    x = dict(r=float(g.normal(mr, sr)), deaths=float(g.normal(94, 10)), celdas=37.0, splits=float(g.integers(4, 10)),
                             descendientes=20.0)
                if arm == 'CAND':
                    x['r'] += (-40.0 if malo else 10.0); x['termo'] = dict(tele)
                if arm == 'CTRL':
                    x['r'] -= 20.0; x['termo'] = dict(tele, termo=2)
                RV.append(dict(x, brazo=b, seed=s, arm=arm, seed_real=s + (100000 if arm == 'TRONCO_B' else 0)))
    for s in seeds_v:
        base = dict(rev=float(g.normal(42, 20)), deaths=float(g.normal(97, 10)), celdas=37.0, splits=float(g.integers(4, 10)),
                    visA=[210, 210, 1700, 1700], visB=[1600, 1600, 220, 220],
                    mordA=[205, 205, 160, int(g.integers(140, 180))], mordB=[150, 150, 190, int(g.integers(200, 218))])
        for arm in U.ARMS_VIVO:
            x = (dict(base) if arm in ('OFF', 'CAND') else
                 dict(base, rev=float(g.normal(42, 20)), mordA=base['mordA'][:3] + [int(g.integers(140, 180))]))
            if malo and arm == 'CAND':
                x['rev'] -= 40.0
                x['mordA'] = x['mordA'][:3] + [1100]   # ERR-150: en Q4 sigue mordiendo A (ahora veneno): S4 ~ 0.6, C ~ -0.3
            RR.append(dict(x, seed=s, arm=arm))
    TB = []
    for s in seeds_e:
        for org in U.ORGS_EX:
            az = 0.30 if (malo and org == 'CAND') else 0.50
            TB.append(dict(org=org, regla='px0', seed=s, acc=1.0, ba=0.97, cobertura=10, splits=6, celdas=36, deaths=20))
            TB.append(dict(org=org, regla='azar', seed=s, acc=0.5, ba=az, cobertura=10, splits=6, celdas=36, deaths=20))
    EXr = []
    for s in seeds_e:
        for e in U.SEIS:
            mord = {k: [30, 20, 60, 70] for k in 'ABCD'}; vis = {k: [40, 40, 80, 80] for k in 'ABCD'}
            W = {'A': 1.0, 'B': -3.0, 'C': -3.0, 'D': 1.0}
            for org in U.ORGS_EX:
                EXr.append(dict(org=org, etapa=e, seed=s, mord=mord, vis=vis, W=W, deaths=10, splits=4, celdas=34))
    TD = []
    for arm in U.ARMS_SAL:
        for s in alias:
            ws = 1.45 if (malo and arm == 'CAND') else 0.0
            TD.append(dict(brazo='S1-ALIAS', seed=s, arm=arm, w_sal=ws, w_veneno=-3.0, exp_sal=500, des_splits=2, deaths=40))
        for s in limpias:
            TD.append(dict(brazo='S1-LIMPIA', seed=s, arm=arm, w_sal=0.0, w_veneno=-3.0, exp_sal=500, des_splits=0, deaths=40))
    return RV, RR, TB, EXr, TD


def etapa8(V, modo):
    """Veredicto de la serie por la letra: una linea por puerta con su umbral (ERR-89)."""
    sub = subpuertas(V); P = puertas_de(sub)
    viv = V.get('vivo')
    legible = None if viv is None else bool(viv['legible'])
    log(f"ETAPA 8 — VEREDICTO por la letra de CRITERIO_TRONCO_v4 ({modo}); una linea por puerta con su umbral (ERR-89).")
    dl = lambda x: 'PASA' if x else ('NO' if x is False else 'NO MEDIDA')
    for k in PUERTAS:
        if k == 'T-C':
            det = f"(i) {dl(sub['T-C_i'])} [{U.LETRA['T-C_i']}] | (ii) {dl(sub['T-C_ii'])} [{U.LETRA['T-C_ii']}]"
        elif k == 'T-F':
            det = f"examen {dl(sub['T-F_examen'])} | vivo {dl(sub['T-F_vivo'])} [{U.LETRA['T-F']}]"
        elif k == 'T-B' and V.get('TB') is not None:
            tb = V['TB']
            det = (f"[{U.LETRA[k]}] | TRONCO v14.3 (mismas semillas) {dl(tb['TRONCO']['pasa'])} | banda VIEJA "
                   f"{tb['banda_azar2']['vieja_solo_informe']} (SOLO INFORME): CAND {dl(tb['CAND']['pasa_banda_vieja'])}, "
                   f"TRONCO {dl(tb['TRONCO']['pasa_banda_vieja'])}")
        else:
            det = f"[{U.LETRA[k]}]"
        log(f"   {k}: {dl(P[k])}   {det}")
    if viv is not None and 'T-C_ii' in viv['CAND'] and 'rev_absoluto_v4' in viv['CAND']['T-C_ii']:
        rv_ = viv['CAND']['T-C_ii']['rev_absoluto_v4']
        log(f"   T-C (ii) letra VIEJA, rev absoluto (SOLO INFORME, ERR-150): {dl(rv_['pasa'])} [{U.LETRA_TC_ii_REV_V4}] "
            f"rev {rv_['det']['rev_c']}/{rv_['det']['rev_o']} LI {rv_['det']['NI']['LI']}")
    log(f"   T-H: NO MEDIDA — {U.LETRA['T-H']}")
    frase = frase_serie(P, legible, modo)
    log(f"VEREDICTO: {frase}")
    return sub, P, legible, frase


# ------------------------------------------------------------------ principal
def argumentos():
    ap = argparse.ArgumentParser(prog='corre_examen_v144c.py', allow_abbrev=False,
                                 description='Examen v14.4c: criterio de tronco v4 con T-C (ii) POR VISITA (ERR-150) sobre v14.4b = v14.3 + TERMOP (ver PREREGISTRO_examen_v144c.md).')
    m = ap.add_mutually_exclusive_group(required=True)
    m.add_argument('--humo', action='store_true', help='UN proceso, 6 corridas (200 000 pasos), cableado sintetico, JSON en datos/humo/')
    m.add_argument('--serie', action='store_true', help='la serie (semillas de umbrales_examen_v144c.SEMILLAS["serie"])')
    m.add_argument('--replica', action='store_true', help='la replica (semillas nuevas, SEMILLAS["replica"])')
    m.add_argument('--reserva', action='store_true', help='SOLO si TRONCO_B no paso en una serie: mundo vivo en SEMILLAS["reserva"]')
    m.add_argument('--bloque', nargs='+', metavar='JSON', help='no corre nada: veredicto del examen con los JSON de serie, replica [y reserva]')
    m.add_argument('--analiza', metavar='PREFIJO', help='no corre nada: relee los crudos <PREFIJO>_crudo_*.json y rehace el veredicto')
    ap.add_argument('--pool', type=int, default=None, help='procesos del Pool (1..6); obligatorio en serie/replica/reserva')
    ap.add_argument('--solo', default=None, help='subconjunto de etapas: TB,EX,TD,TC,TA (veredicto INCOMPLETO; T-G sale de TA)')
    ap.add_argument('--con', nargs='+', default=None, metavar='JSON', help='JSON de la serie (en --replica): imprime el veredicto del examen')
    ap.add_argument('--sustituye', choices=['serie', 'replica'], default=None, help='en --reserva: que serie no se leyo')
    a = ap.parse_args()
    if a.humo and (a.pool or a.solo or a.con or a.sustituye):
        ap.error('--humo es un proceso sin Pool: no admite --pool/--solo/--con/--sustituye')
    if (a.serie or a.replica or a.reserva) and (a.pool is None or not 1 <= a.pool <= 6):
        ap.error('--pool N obligatorio con 1 <= N <= 6 (PC: 6; nube: 3)')
    if a.reserva and a.sustituye is None:
        ap.error('--reserva exige --sustituye serie|replica (la serie cuyo mundo vivo no se leyo)')
    if a.solo:
        malas = set(a.solo.split(',')) - {'TB', 'EX', 'TD', 'TC', 'TA'}
        if malas:
            ap.error(f'--solo: etapas desconocidas {sorted(malas)}')
    return a


def reanaliza(prefijo):
    """ERR-54: los crudos estan en disco ANTES del analisis; si el analisis se cae, esto lo rehace sin correr nada."""
    base = os.path.basename(prefijo)
    m = re.match(r'examen_v144c_(serie|replica|reserva)_\d{8}_\d{6}$', base)
    if not m:
        raise SystemExit(f'*** --analiza espera examen_v144c_<serie|replica|reserva>_<AAAAMMDD_HHMMSS>, no {base!r}')
    modo = m.group(1)
    carpeta = os.path.dirname(prefijo) or DATOS_EX
    _log['nom'] = base + '_reanalisis'
    _log['f'] = open(os.path.join(carpeta, _log['nom'] + '.log'), 'w', encoding='utf-8', newline='\n')
    log(f'REANALISIS (no corre nada) de {base}: modo {modo}, crudos en {carpeta}')
    lee = lambda etq: (json.load(open(os.path.join(carpeta, f'{base}_crudo_{etq}.json'), encoding='utf-8'))['corridas']
                       if os.path.exists(os.path.join(carpeta, f'{base}_crudo_{etq}.json')) else None)
    V = {}
    c = lee('TB')
    if c is not None:
        V['TB'] = veredicto_TB(c)
    c = lee('EX')
    if c is not None:
        V['EX'] = veredicto_EX(c)
    c = lee('TD')
    if c is not None:
        V['TD'] = veredicto_TD(c)
    rr, rv = lee('TCii'), lee('TA')
    if rr is not None and rv is not None:
        V['vivo'] = veredicto_vivo(rv, rr)
    if rv is not None:
        V['TG'] = veredicto_TG(rv)
    meta = dict(modo=modo, reanalisis_de=base, fecha=time.strftime('%Y-%m-%dT%H:%M:%S'), letra=U.LETRA, err122=U.ERR122, err150=U.ERR150, tg=U.TG,
                shas=dict(runner=h16(os.path.abspath(__file__)), umbrales=h16(os.path.join(AQUI, 'umbrales_examen_v144c.py'))))
    if modo == 'reserva':
        sub = subpuertas(V); leg = None if V.get('vivo') is None else bool(V['vivo']['legible'])
        out = dict(meta=meta, legible=leg, sub=sub, veredictos=V)
        log(f"VEREDICTO (reserva, reanalisis): legible {leg}; " + ' '.join(f"{k} {sub[k]}" for k in VIVAS))
    else:
        sub, P, leg, frase = etapa8(V, modo)
        out = dict(meta=meta, legible=leg, sub=sub, puertas=P, frase=frase, veredictos=V)
    dj = os.path.join(carpeta, _log['nom'] + '.json')
    json.dump(out, open(dj, 'w', encoding='utf-8'), ensure_ascii=False, default=str)
    log(f'datos -> {dj}  sha256_16 = {h16(dj)}  (para --bloque, usar ESTE json; lleva meta.modo = {modo})')
    _log['f'].close()
    return 0


def humo(SAL, nom, meta, R14, r14ok):
    h = U.SEMILLAS['humo']; Th = U.T_HUMO; b = U.TG['brazo']
    log(f'HUMO 1/3 — 6 corridas de un proceso, 200 000 pasos: T-A {b} OFF, CAND y CTRL s{h[0]} T={Th}; T-C ii CAND s{h[1]} T={Th} '
        f'(reversion en T/2); T-D CAND ALIAS 326 T={Th}; examen E2 CAND s{h[2]} T=100000 (la bateria).')
    t0 = time.time()
    o_off = tarea_vivo((b, h[0], 'OFF', Th)); o_cand = tarea_vivo((b, h[0], 'CAND', Th)); o_ctrl = tarea_vivo((b, h[0], 'CTRL', Th))
    o_rev = tarea_rev((h[1], 'CAND', Th)); o_sal = tarea_sal(('S1-ALIAS', 326, 'CAND', Th)); o_ex = tarea_ex(('CAND', 'E2', h[2]))
    for etq, o in (('OFF ', o_off), ('CAND', o_cand), ('CTRL', o_ctrl)):
        log(f"   T-A {b} {etq} s{h[0]}: r {o['r']} desc {o['descendientes']} muertes {o['deaths']} {o['muertes_nec']} celdas {o['celdas']} "
            f"splits {o['splits']} termo {({k: v for k, v in o['termo'].items() if k != 'adS'} if o.get('termo') else None)} ({o['seg']} s)")
    t_c, t_k = o_cand['termo'], o_ctrl['termo']
    actua = bool(t_c and t_k and t_c['a_no'] + t_c['a_si'] > 0 and t_k['a_no'] + t_k['a_si'] > 0)
    difiere = (not iguales(o_off, o_cand)) and (not iguales(o_cand, o_ctrl))
    log(f"   la pieza ACTUA (a_no + a_si > 0 en CAND y en CTRL): {actua}; CAND != OFF y CAND != CTRL: {difiere} (DEBEN ser True)")
    log(f"   T-C ii CAND s{h[1]}: rev {o_rev['rev']} mordA {o_rev['mordA']} mordB {o_rev['mordB']} muertes {o_rev['deaths']} "
        f"termo {({k: v for k, v in o_rev['termo'].items()} if o_rev.get('termo') else None)} ({o_rev['seg']} s)")
    log(f"   T-C ii CAND s{h[1]} POR VISITA (ERR-150; T = {Th}, UNA corrida, no es evidencia): S2 {S2_visita(o_rev):.4f} "
        f"S4 {S4_visita(o_rev):.4f} C {C_visita(o_rev):+.4f}; visitas A {o_rev['visA']} B {o_rev['visB']}")
    log(f"   T-D CAND ALIAS 326: |W[sal]| {o_sal['w_sal']} W[veneno] {o_sal['w_veneno']} exp sal {o_sal['exp_sal']} "
        f"des_splits {o_sal['des_splits']} ({o_sal['seg']} s)")
    log(f"   examen E2 CAND s{h[2]}: come B Q4 {o_ex['mord']['B'][3]} (>= 50) muerde A por cuarto {o_ex['mord']['A']} muertes {o_ex['deaths']} "
        f"W {o_ex['W']} ({o_ex['seg']} s)")
    seg = dict(vivo=(o_off['seg'] + o_cand['seg'] + o_ctrl['seg']) / 3 * (U.T_VIVO / Th), rev=o_rev['seg'] * (U.T_VIVO / Th),
               sal=o_sal['seg'] * (U.T_VIVO / Th), ex=o_ex['seg'], tb=2.0 * o_ex['seg'])
    n = dict(tb=2 * 2 * 20, ex=2 * 6 * 20, sal=2 * 18, rev=4 * 80, vivo=2 * 5 * 80)
    cpu = sum(seg[k] * n[k] for k in n)
    log(f"   DURACION por corrida (T completo, lineal desde T={Th}; T-B supuesto 2 x examen): " + ' '.join(f"{k} {seg[k]:.1f}s" for k in seg))
    log(f"   COSTO por serie: {sum(n.values())} corridas ~ {cpu/3600:.1f} h de CPU de ESTE proceso -> Pool 6 ~ {cpu/6/60:.0f} min "
        f"(+ identidad ~5 min); nube Pool 3 (nucleo 1.3-2.2x mas rapido) ~ {cpu/3/1.75/60:.0f} min. Serie + replica: el doble.")
    log('HUMO 2/3 — CABLEADO de la etapa 8 con crudos SINTETICOS (n reales: 80 vivo, 20 examen, 9+9 sal). NO son evidencia.')
    S = U.SEMILLAS['serie']
    cab = {}
    for malo in (False, True):
        RV, RR, TB, EXr, TD = sinteticos(80, 20, S['ALIAS'], S['LIMPIAS'], malo=malo)
        Vs = dict(TB=veredicto_TB(TB), EX=veredicto_EX(EXr), TD=veredicto_TD(TD), vivo=veredicto_vivo(RV, RR), TG=veredicto_TG(RV))
        sub, P, leg, frase = etapa8(Vs, 'humo-sintetico-' + ('MALO' if malo else 'bueno'))
        cab['malo' if malo else 'bueno'] = dict(sub=sub, puertas=P, legible=leg, frase=frase)
    cab_ok = bool(all(cab['bueno']['puertas'].values()) and cab['bueno']['legible']
                  and not any(cab['malo']['puertas'][k] for k in ('T-A', 'T-B', 'T-C', 'T-D', 'T-G')))
    log(f"   cableado: bueno {cab['bueno']['puertas']} | malo {cab['malo']['puertas']} -> {'OK' if cab_ok else '*** revisar'} "
        f"(el bueno DEBE pasar todo; el malo DEBE caer T-A, T-B, T-C, T-D y T-G)")
    log('HUMO 3/3 — JSON.')
    dj = os.path.join(SAL, nom + '.json')
    json.dump(dict(meta=dict(meta, humo=True, corridas=6, pasos=5 * Th + 100000, semillas=dict(humo=h, alias_historica=326),
                             regla14=[(n_, ok) for n_, ok in R14], pieza_actua=actua, difiere=difiere, duracion_s=seg,
                             costo=dict(corridas_por_serie=sum(n.values()), cpu_h=round(cpu / 3600, 2), pool6_min=round(cpu / 6 / 60),
                                        nube_pool3_min=round(cpu / 3 / 1.75 / 60)),
                             cableado=cab, cableado_ok=cab_ok, seg_total=round(time.time() - t0, 1)),
                   vivo=[o_off, o_cand, o_ctrl], reversion=o_rev, sal=o_sal, examen=o_ex),
              open(dj, 'w', encoding='utf-8'), ensure_ascii=False, default=str)
    log(f'datos -> {os.path.relpath(dj, RAIZ)}  sha256_16 = {h16(dj)}')
    ok = bool(actua and difiere and cab_ok and r14ok)
    log(f"VEREDICTO DEL HUMO: {'OK' if ok else '*** FALLA'} (no es evidencia; prueba que el examen mide, que la pieza actua y que el juez puede decir NO)")
    return 0 if ok else 1


def main():
    a = argumentos()
    if a.analiza:
        return reanaliza(a.analiza)
    if a.bloque:
        frase, lineas = combina(a.bloque)
        for l in lineas:
            print(l)
        print(frase)
        return 0
    modo = 'humo' if a.humo else ('serie' if a.serie else ('replica' if a.replica else 'reserva'))
    POOL = 1 if a.humo else a.pool
    SOLO = set(a.solo.split(',')) if a.solo else None
    hacer = lambda e: SOLO is None or e in SOLO
    stamp = time.strftime('%Y%m%d_%H%M%S')
    nom = f'examen_v144c_{modo}_{stamp}'
    _log['nom'] = nom
    SAL = DATOS_HUMO if a.humo else DATOS_EX
    os.makedirs(SAL, exist_ok=True)
    _log['f'] = open(os.path.join(SAL, nom + '.log'), 'w', encoding='utf-8', newline='\n')
    log(f"ARRANQUE examen v14.4c (v4 con T-C ii POR VISITA, ERR-150) sobre v14.4b = v14.3 + TERMOP — modo {modo}, {'UN proceso, sin Pool' if a.humo else f'Pool {POOL}'}, python "
        f"{platform.python_version()}, numpy {np.__version__}, {platform.platform()}")
    log('MISION: llegar a la AGI por este camino; el examen v4 es la puerta de NO REGRESION del organismo comun.')
    # ---------------------------------------------------------------- ETAPA 0
    log('ETAPA 0 — anclas, construccion por anclas, regla 14, semillas de T-D recalculadas.')
    shas_const = verifica_anclas()
    pre = os.path.join(AQUI, 'PREREGISTRO_examen_v144c.md')
    SHAS = dict(construidos=shas_const, anclas={os.path.relpath(p, RAIZ).replace(os.sep, '/'): s for p, s in ANCLAS.items()},
                runner=h16(os.path.abspath(__file__)), umbrales=h16(os.path.join(AQUI, 'umbrales_examen_v144c.py')),
                identidad=h16(os.path.join(AQUI, 'identidad_v144cex.py')) if os.path.exists(os.path.join(AQUI, 'identidad_v144cex.py')) else None,
                construye=h16(os.path.join(V144B, 'construye_termop.py')),
                construye_v144c=h16(os.path.join(AQUI, 'construye_examen_v144c.py')),
                preregistro=h16(pre) if os.path.exists(pre) else None,
                criterio_v4=h16(os.path.join(RAIZ, 'registro', 'CRITERIO_TRONCO_v4.md')))
    log(f"   sha construidos {shas_const}")
    log(f"   sha runner {SHAS['runner']} umbrales {SHAS['umbrales']} identidad {SHAS['identidad']} preregistro {SHAS['preregistro']} "
        f"criterio_v4 {SHAS['criterio_v4']}")
    R14 = regla14()
    for nombre, ok in R14:
        if not ok:
            log(f'   *** REGLA 14: {nombre} -> FALLA')
    r14ok = all(ok for _, ok in R14)
    log(f"   regla 14: {sum(ok for _, ok in R14)}/{len(R14)} {'OK' if r14ok else '*** FALLA'}")
    if not r14ok:
        log('*** la regla 14 falla: se para sin correr nada.'); _log['f'].close(); return 1
    ps = procesos_python()
    log(f'REGLA 11 — procesos python vivos ({len(ps)}); este es pid {os.getpid()}')
    V = {}
    meta = dict(modo=modo, fecha=time.strftime('%Y-%m-%dT%H:%M:%S'), pool=POOL, solo=sorted(SOLO) if SOLO else None,
                shas=SHAS, python=platform.python_version(), numpy=np.__version__, plataforma=platform.platform(),
                procesos_python=ps, letra=U.LETRA, err122=U.ERR122, err150=U.ERR150, tg=U.TG, predicciones=U.PRED, sustituye=a.sustituye)
    log(f"   letra: la del examen de v14.3 (T-B decide azar G2 con {list(U.NUM['TB_azar2'])}, ERR-122); T-G: {U.LETRA['T-G']}")
    log(f"   T-C (ii) DECIDE: {U.LETRA['T-C_ii']}. La VIEJA se reporta: {U.LETRA_TC_ii_REV_V4}")
    if a.humo:
        r = humo(SAL, nom, meta, R14, r14ok)
        _log['f'].close()
        return r

    # ================================================================ SERIE / REPLICA / RESERVA
    S = U.SEMILLAS[modo]
    if modo != 'reserva':
        ok, sel = guarda_semillas_TD(modo)
        log(f"   T-D {modo}: ALIAS {sel['alias']} LIMPIAS {sel['limpias']} recalculadas -> {'coinciden' if ok else '*** NO COINCIDEN'}")
        if not ok:
            log('*** la seleccion estructural de T-D no se reproduce: se para.'); _log['f'].close(); return 1
    log(f"ETAPA 1 — identidad (subproceso, un proceso): identidad_v144cex.py -> debe dar '{U.ARNES_ESPERADO}'.")
    t1 = time.time()
    p = subprocess.run([sys.executable, os.path.join(AQUI, 'identidad_v144cex.py')], capture_output=True, text=True, cwd=AQUI,
                       encoding='utf-8', errors='replace')
    cola = (p.stdout or '').strip().splitlines()
    for l in cola[-8:]:
        log(f'      | {l}')
    ultima = cola[-1] if cola else ''
    mj = re.findall(r'identidad_v144cex_(\d{8}_\d{6})\.json', p.stdout or '')   # ERR-87: prefijo + sello exacto
    meta['identidad'] = dict(ultima=ultima, returncode=p.returncode, json=(f'identidad_v144cex_{mj[-1]}.json' if mj else None),
                             seg=round(time.time() - t1, 1))
    if p.returncode != 0 or ultima.strip() != U.ARNES_ESPERADO:
        log(f"*** identidad: '{ultima}' != '{U.ARNES_ESPERADO}' (codigo {p.returncode}); se para sin veredicto. stderr: {(p.stderr or '')[-600:]}")
        _log['f'].close(); return 1
    log(f"   identidad OK: {ultima} ({meta['identidad']['seg']} s; JSON {meta['identidad']['json']})")
    crudos = {}
    if modo != 'reserva':
        if hacer('TB'):
            t = [(o, rg, s) for o in U.ORGS_EX for rg in U.REGLAS_TB for s in S['EX']]
            log(f"ETAPA 2 — T-B generalizacion: {len(t)} corridas (T = 200 000), semillas {S['EX'][0]}-{S['EX'][-1]}, Pool {POOL}.")
            crudos['TB'] = crudo('TB', pool_map(tarea_tb, t, 'T-B', POOL), SAL, extra=dict(semillas=S['EX']))
            V['TB'] = veredicto_TB(crudos['TB'])
        if hacer('EX'):
            t = [(o, e, s) for o in U.ORGS_EX for e in U.SEIS for s in S['EX']]
            log(f"ETAPA 3 — examen v3' (seis etapas): {len(t)} corridas, semillas {S['EX'][0]}-{S['EX'][-1]}, Pool {POOL}.")
            crudos['EX'] = crudo('EX', pool_map(tarea_ex, t, 'examen', POOL), SAL, extra=dict(semillas=S['EX']))
            V['EX'] = veredicto_EX(crudos['EX'])
        if hacer('TD'):
            t = [(b, s, arm, U.T_VIVO) for b, ss in (('S1-ALIAS', S['ALIAS']), ('S1-LIMPIA', S['LIMPIAS'])) for s in ss for arm in U.ARMS_SAL]
            log(f"ETAPA 4 — T-D sal muda: {len(t)} corridas (ALIAS {S['ALIAS']}, LIMPIAS {S['LIMPIAS']}), Pool {POOL}.")
            crudos['TD'] = crudo('TD', pool_map(tarea_sal, t, 'T-D', POOL), SAL, extra=dict(alias=S['ALIAS'], limpias=S['LIMPIAS']))
            V['TD'] = veredicto_TD(crudos['TD'])
    res_rev = res_vivo = None
    if hacer('TC'):
        t = [(s, arm, U.T_VIVO) for s in S['VIVO'] for arm in U.ARMS_VIVO]
        log(f"ETAPA 5 — T-C (ii) reversion en el mundo vivo: {len(t)} corridas, semillas {S['VIVO'][0]}-{S['VIVO'][-1]} "
            f"(TRONCO_B {S['VIVO'][0] + U.DESPL_TRONCO_B}-{S['VIVO'][-1] + U.DESPL_TRONCO_B}), Pool {POOL}.")
        res_rev = crudos['TCii'] = crudo('TCii', pool_map(tarea_rev, t, 'T-C ii', POOL), SAL, extra=dict(semillas=S['VIVO']))
    if hacer('TA'):
        t = [(b, s, arm, U.T_VIVO) for b in U.BRAZOS_TA for s in S['VIVO'] for arm in U.ARMS_TA]
        log(f"ETAPA 6 — T-A supervivencia (+ el CONTROL TERMOINV de T-G): {len(t)} corridas, Pool {POOL}.")
        res_vivo = crudos['TA'] = crudo('TA', pool_map(tarea_vivo, t, 'T-A', POOL), SAL, extra=dict(semillas=S['VIVO']))
    if res_rev is not None and res_vivo is not None:
        log('   letra v4 calibrada (corre_criterio_v4.juzga) sobre CAND, TRONCO_B y PLACEBO contra OFF:')
        V['vivo'] = veredicto_vivo(res_vivo, res_rev)
    if res_vivo is not None:
        log(f"ETAPA 7 — T-G desde los crudos de T-A (decide {U.TG['brazo']}; {U.TG['informe']} se reporta).")
        V['TG'] = veredicto_TG(res_vivo)
    # ---------------------------------------------------------------- ETAPA 8
    if modo == 'reserva':
        sub = subpuertas(V)
        leg = None if V.get('vivo') is None else bool(V['vivo']['legible'])
        log(f"VEREDICTO (reserva; sustituye el mundo vivo de la {a.sustituye}): legible {leg}; " + ' '.join(f"{k} {sub[k]}" for k in VIVAS))
        out = dict(meta=meta, legible=leg, sub=sub, veredictos=V)
    else:
        sub, P, leg, frase = etapa8(V, modo)
        out = dict(meta=meta, legible=leg, sub=sub, puertas=P, frase=frase, veredictos=V)
    dj = os.path.join(SAL, nom + '.json')
    json.dump(out, open(dj, 'w', encoding='utf-8'), ensure_ascii=False, default=str)
    log(f'datos -> {os.path.relpath(dj, RAIZ)}  sha256_16 = {h16(dj)}')
    if a.con:
        frase_ex, lineas = combina(list(a.con) + [dj])
        for l in lineas:
            log(l)
        log(frase_ex)
    _log['f'].close()
    return 0


if __name__ == '__main__':
    sys.exit(main())
