"""corre_examen_v143.py -- EXAMEN DEL CRITERIO DE TRONCO v4 (registro/CRITERIO_TRONCO_v4.md) sobre v14.3 = v14.2 + N.
Ejecuta experimentos/tronco_v14_3_examen/PREREGISTRO_examen_v143.md. Umbrales, semillas y predicciones: umbrales_examen_v143.py.

MISION: llegar a la AGI por este camino. El examen v4 es la puerta de NO REGRESION del organismo comun, no un puntaje: v14.3
entra al tronco si no empeora en nada de lo que el tronco ya hace (T-A..T-F) y si su reparacion (componer en 3T-k) se ve en
semillas nuevas (T-G).

Lo que se REUSA por import (sha fijado en ANCLAS; nada se copia):
  corre_criterio_v4   la letra calibrada de T-A / T-C (ii) / T-F vivo (letra_TA, letra_TC, letra_TF, juzga) y las tareas del
                      tronco en el mundo vivo (tarea_vivo, tarea_rev: OFF, TRONCO_B = semilla s+100000, PLACEBO = placebo 1)
  corre_dE5_v2        la letra de T-B, T-C (i), T-E y T-F examen (UMB, conducta, coste_examen; v2 = v3 = v4 "sin cambio")
  corre_codigo        C1, C2, C6 de B-5 (T-D) ; corre_sal: BASE (sal muda) y resumen
  bateria_v142 / bateria_generaliza_v142 (CONGELADAS) y sus copias por anclas v143: la `tarea` de cada una
  corre_n7            la tarea y la letra de 3T-k (T-G)
El candidato: organismo_v143 (examen), organismo_v143g (T-B), organismo_v143cal (mundo vivo), construidos por construye_v143.py.

ENMIENDA ERR-122 (23-sep-2026 ~21:10, antes de la serie; decision del director "corrige la banda", PREREGISTRO §7): T-B se
calcula aqui desde los valores CRUDOS de bateria_generaliza (acc, ba, cobertura por semilla), nunca desde el veredicto interno
de la bateria CONGELADA (que conserva su banda [0.42, 0.58]). La banda de azar G2 que DECIDE es [0.31, 0.60]
(umbrales_examen_v143.NUM['TB_azar2'] = ERR122['banda_nueva']); la de la letra importada (corre_dE5_v2.UMB['T-B']['azar2'] =
[0.42, 0.58]) se calcula para CAND y TRONCO y SOLO SE REPORTA. Todo lo demas de T-B (G1, G2, azar G1 [0.35, 0.65], K) y de las
otras puertas: sin cambio. regla14() registra TB_azar2 como diferencia DECLARADA por ERR-122, no como falla.

ETAPAS (serie y replica; regla 10: una linea por etapa con hora, log a disco desde el arranque, fsync):
  0  anclas (sha), semillas de T-D recalculadas, regla 14 (kwargs campo a campo), procesos python vivos (regla 11)
  1  identidad (subproceso de UN proceso): identidad_v143ex.py -> 'RESULTADO: N/N' == umbrales.ARNES_ESPERADO; si no, se para
  2  T-B   generalizacion: {CAND, TRONCO} x {px0, azar} x 20 semillas (T = 200 000)                     80 corridas
  3  EX    examen v3', seis etapas: {CAND, TRONCO} x 6 x 20 semillas -> T-C (i), T-E, T-F examen         240 corridas
  4  T-D   sal muda: {OFF, CAND} x (9 ALIAS + 9 LIMPIAS)                                                  36 corridas
  5  T-C (ii) reversion en el mundo vivo: {OFF, CAND, TRONCO_B, PLACEBO} x 80                          320 corridas
  6  T-A   {VIVO, CUELLO_MIN} x {OFF, CAND, TRONCO_B, PLACEBO} x 80                                       640 corridas
  7  T-G   3T-k: {T142, N, NC3C} x k 1..8 x 20 semillas                                                   480 corridas
  8  veredicto: UNA linea por puerta con su umbral (ERR-89); inercia medida (CAND == tronco bit a bit); VEREDICTO
Crudos a disco ANTES del analisis y releidos (ERR-54). JSON de subproceso por prefijo + sello exacto (ERR-87).

Uso (SOLO el coordinador corre --serie/--replica/--reserva; los agentes solo --humo; ERR-115):
  python experimentos/tronco_v14_3_examen/corre_examen_v143.py --humo                  (UN proceso, 6 corridas, < 5 min)
  python experimentos/tronco_v14_3_examen/corre_examen_v143.py --serie --pool 6        (PC)   | --pool 3 en la nube
  python experimentos/tronco_v14_3_examen/corre_examen_v143.py --replica --pool 6 --con <JSON de la serie>
  python experimentos/tronco_v14_3_examen/corre_examen_v143.py --reserva --pool 6      (solo si TRONCO_B no pasa en una serie)
  python experimentos/tronco_v14_3_examen/corre_examen_v143.py --combina <serie.json> <replica.json> [<reserva.json>]
Opcional: --solo TB,EX,TD,TC,TA,TG (subconjunto; el veredicto queda INCOMPLETO). Banderas desconocidas o abreviadas: aborta.
Recuperacion (ERR-54; no corre nada): --analiza <datos/examen_v143_<modo>_<sello>> relee los crudos de esa corrida y rehace el
veredicto (por si el analisis se cayo despues de las corridas); escribe <nombre>_reanalisis.json.
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
N7 = os.path.join(EXP, 'subida_n7')
C14 = os.path.join(EXP, 'nivel10_composicion_v14')
DATOS_HUMO = os.path.join(RAIZ, 'datos', 'humo')
DATOS_EX = os.path.join(AQUI, 'datos')
for _p in reversed([AQUI, ORG, VIVO_DIR, V3_DIR, V4_DIR, CREB, DE5, N7, C14]):
    if _p not in sys.path:
        sys.path.insert(0, _p)

import umbrales_examen_v143 as U


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
C7 = _importa_sin_argv('corre_n7')              # T-G (3T-k)
CS = _importa_sin_argv('corre_sal')             # T-D: BASE (sal muda) y resumen
CR2 = _importa_sin_argv('corre_vivo_rep2')
MV = _importa_sin_argv('mini_vivo')
B142 = _importa_sin_argv('bateria_v142')
B143 = _importa_sin_argv('bateria_v143')
G142 = _importa_sin_argv('bateria_generaliza_v142')
G143 = _importa_sin_argv('bateria_generaliza_v143')
sys.path.insert(0, AQUI)   # las baterias importadas anteponen sus carpetas: la nuestra queda primera otra vez


def h16(p):
    return hashlib.sha256(open(p, 'rb').read()).hexdigest()[:16]


# ------------------------------------------------------------------ ANCLAS: lo reusado (sha fijo) y lo construido aqui
ANCLAS = {
    os.path.join(ORG, 'organismo_v142.py'): '17528d767fcebaf6',
    os.path.join(ORG, 'organismo_v142g.py'): '9e5f566cd6a7a4d2',
    os.path.join(ORG, 'bateria_v142.py'): '6375d90e531b06e6',
    os.path.join(ORG, 'bateria_generaliza_v142.py'): 'e5929942647756a5',
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
    os.path.join(N7, 'corre_n7.py'): '746e9c70f7beef45',
    os.path.join(N7, 'mundo_n7.py'): '429667c8a334aa48',
    os.path.join(C14, 'mundo_composicion_v14.py'): 'a9098933b1950e3d',
}
CONSTRUIDOS = ('organismo_v143.py', 'organismo_v143g.py', 'organismo_v143cal.py', 'bateria_v143.py', 'bateria_generaliza_v143.py')


def verifica_anclas():
    malas = [(os.path.relpath(p, RAIZ), h16(p), s) for p, s in ANCLAS.items() if h16(p) != s]
    if malas:
        raise SystemExit(f'*** ANCLA CAMBIADA (lo reusado no es lo que se calibro/midio): {malas}')
    r = subprocess.run([sys.executable, os.path.join(AQUI, 'construye_v143.py'), '--verifica'], capture_output=True, text=True,
                       encoding='utf-8', errors='replace')
    if r.returncode != 0:
        raise SystemExit(f'*** los archivos construidos NO son la construccion por anclas:\n{r.stdout[-1500:]}')
    return {n: h16(os.path.join(AQUI, n)) for n in CONSTRUIDOS}


# ------------------------------------------------------------------ los kwargs de cada brazo: LO UNICO que los distingue
def kw_vivo_cand(brazo):
    return dict(C4.kw_vivo(brazo, 'OFF'), norm_lenta=1)


def kw_rev_cand(Ti):
    return dict(C4.kw_rev('OFF', Ti), norm_lenta=1)


def kw_sal(arm):
    kw = dict(CS.BASE, desambiguar=1, placebo=0)
    if arm == 'CAND':
        kw['norm_lenta'] = 1
    return kw


# ------------------------------------------------------------------ tareas (top-level, aptas para Pool con spawn)
def tarea_vivo(args):
    """T-A. OFF/TRONCO_B/PLACEBO = EXACTAMENTE la tarea calibrada de V4-CAL; CAND = organismo_v143cal con los mismos kwargs."""
    brazo, seed, arm, Ti = args
    if arm != 'CAND':
        o = C4.tarea_vivo((brazo, seed, arm, Ti))
        o['org'] = 'organismo_v3cal'
        return o
    import organismo_v143cal as V143C
    kw = kw_vivo_cand(brazo)
    t0 = time.time()
    r = V143C.run(seed, T=Ti, **kw)
    o = CR2.resumen2(brazo, seed, r, kw, Ti)
    o.update(seed=seed, seed_real=seed, arm=arm, placebo=r['placebo'], des_splits=r['des_splits'], seg=round(time.time() - t0, 2),
             org='organismo_v143cal')
    return o


def tarea_rev(args):
    """T-C (ii). Mismo formato que corre_criterio_v4.tarea_rev."""
    seed, arm, Ti = args
    if arm != 'CAND':
        o = C4.tarea_rev((seed, arm, Ti))
        o['org'] = 'organismo_v3cal'
        return o
    import organismo_v143cal as V143C
    t0 = time.time()
    r = V143C.run(seed, T=Ti, **kw_rev_cand(Ti))
    return dict(seed=seed, seed_real=seed, arm=arm, mordA=r['mord']['A'], mordB=r['mord']['B'], visA=r['vis']['A'],
                visB=r['vis']['B'], rev=r['mord']['B'][3] - r['mord']['A'][3], deaths=r['deaths'],
                muertes_nec=r['muertes_nec'], celdas=r['celdas'], splits=r['splits'], placebo=r['placebo'],
                seg=round(time.time() - t0, 2), org='organismo_v143cal')


def tarea_sal(args):
    """T-D (sal muda). OFF = el tronco v14.2 en el mundo vivo (organismo_v3cal, B-5 encendido)."""
    brazo, seed, arm, Ti = args
    import organismo_v3cal as CAL, organismo_v143cal as V143C
    m = V143C if arm == 'CAND' else CAL
    t0 = time.time()
    r = m.run(seed, T=Ti, **kw_sal(arm))
    o = CS.resumen(brazo, seed, r)
    o.update(arm=arm, des_splits=r['des_splits'], seg=round(time.time() - t0, 2), org=m.__name__)
    return o


def tarea_ex(args):
    """Examen v3' (seis etapas): la `tarea` de la bateria (CONGELADA para el tronco; copia por anclas para el candidato)."""
    org, etapa, seed = args
    t0 = time.time()
    o = (B143 if org == 'CAND' else B142).tarea((etapa, seed))
    o.update(org=org, seg=round(time.time() - t0, 2))
    return o


def tarea_tb(args):
    """T-B: la `tarea` de bateria_generaliza (CONGELADA para el tronco; copia con UNA entrada nueva para el candidato)."""
    org, regla, seed = args
    t0 = time.time()
    o = (G143.tarea(('organismo_v143', regla, seed)) if org == 'CAND' else G142.tarea(('organismo_v142', regla, seed)))
    o.update(org=org, seg=round(time.time() - t0, 2))
    return o


def tarea_tg(args):
    """T-G: la tarea de subida_n7 (brazo, k, semilla, T), sin tocar."""
    return C7.tarea(args)


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
    """La seleccion estructural de T-D se RECALCULA: si no coincide con umbrales_examen_v143.SEMILLAS, no se corre."""
    import diagnostico_codigos as DC
    S = U.SEMILLAS[modo]
    lo, hi = S['TD_rango']
    a = [s for s in range(lo, hi + 1) if DC.solapamientos(s)['D&B'] >= 3][:9]
    l = [s for s in range(lo, hi + 1) if DC.solapamientos(s)['D&B'] == 0][:9]
    return a == S['ALIAS'] and l == S['LIMPIAS'], dict(alias=a, limpias=l)


def regla14():
    """(nombre, ok) por comprobacion. Kwargs campo a campo contra el montaje del tronco; baterias copiadas contra las
    congeladas; letra restada en umbrales_examen_v143 contra los modulos de donde se importa; semillas disjuntas."""
    import inspect, organismo_v142 as V142, organismo_v143 as V143, organismo_v142g as V142G, organismo_v143g as V143G
    import corre_codigo as CC
    R = []
    dif = lambda a, b: sorted({k for k in set(a) | set(b) if a.get(k, '<falta>') != b.get(k, '<falta>')})
    for b in U.BRAZOS_TA:
        off = C4.kw_vivo(b, 'OFF')
        R.append((f'R1 T-A {b}: OFF == corre_vivo_rep2.BRAZOS[{b}] + desambiguar=1 + placebo=0 (el montaje de V4-CAL)',
                  off == dict(CR2.BRAZOS[b], desambiguar=1, placebo=0)))
        R.append((f'R1 T-A {b}: CAND difiere de OFF SOLO en norm_lenta=1', dif(kw_vivo_cand(b), off) == ['norm_lenta']
                  and kw_vivo_cand(b)['norm_lenta'] == 1))
        R.append((f'R1 T-A {b}: TRONCO_B == OFF campo a campo', C4.kw_vivo(b, 'TRONCO_B') == off))
        R.append((f'R1 T-A {b}: PLACEBO difiere de OFF SOLO en placebo=1', dif(C4.kw_vivo(b, 'PLACEBO'), off) == ['placebo']
                  and C4.kw_vivo(b, 'PLACEBO')['placebo'] == 1))
    off = C4.kw_rev('OFF', U.T_VIVO)
    R.append(('R1 T-C ii: OFF == mini_vivo.BRAZOS[VIVO] + desambiguar=1 + invertir_vivo_en=T/2 + placebo=0',
              off == dict(MV.BRAZOS['VIVO'], desambiguar=1, invertir_vivo_en=U.T_VIVO // 2, placebo=0)))
    R.append(('R1 T-C ii: CAND difiere de OFF SOLO en norm_lenta=1', dif(kw_rev_cand(U.T_VIVO), off) == ['norm_lenta']))
    R.append(('R1 T-C ii: TRONCO_B == OFF', C4.kw_rev('TRONCO_B', U.T_VIVO) == off))
    R.append(('R1 T-D: OFF == corre_sal.BASE (sal muda) + desambiguar=1 + placebo=0; CAND == OFF + norm_lenta=1',
              kw_sal('OFF') == dict(CS.BASE, desambiguar=1, placebo=0) and dif(kw_sal('CAND'), kw_sal('OFF')) == ['norm_lenta']))
    R.append(('R1 TRONCO_B = semilla s + 100000 (umbrales_v4)', C4.DESPL == U.DESPL_TRONCO_B
              and C4.semilla_real(43101, 'TRONCO_B') == 143101 and C4.semilla_real(43101, 'OFF') == 43101))
    # R2 examen v3'
    R.append(('R2 bateria_v143.ETAPAS == bateria_v142.ETAPAS (campo a campo)', N_(B143.ETAPAS) == N_(B142.ETAPAS)))
    R.append(('R2 bateria_v143: SEIS, ESC_ID, EVENTO == bateria_v142', B143.SEIS == B142.SEIS == U.SEIS == D5.SEIS
              and N_(B143.ESC_ID) == N_(B142.ESC_ID) and B143.EVENTO == B142.EVENTO))
    R.append(('R2 bateria_v143.CRIT: mismas etapas y mismos nombres que bateria_v142',
              {e: list(c) for e, c in B143.CRIT.items()} == {e: list(c) for e, c in B142.CRIT.items()}))
    # R3 generalizacion
    R.append(('R3 bateria_generaliza_v143: organismo_v143 -> (organismo_v143g, kwargs CAMPO A CAMPO == organismo_v142)',
              G143.INSTRUMENTOS['organismo_v143'][0] == 'organismo_v143g'
              and G143.INSTRUMENTOS['organismo_v143'][1] == G142.INSTRUMENTOS['organismo_v142'][1]))
    R.append(('R3 bateria_generaliza_v143: la entrada organismo_v142 intacta; REGLAS == [px0, azar]',
              G143.INSTRUMENTOS['organismo_v142'] == G142.INSTRUMENTOS['organismo_v142'] and G143.REGLAS == G142.REGLAS == U.REGLAS_TB))
    R.append(('R3 los defectos del instrumento de regla NO son los del tronco (por eso los kwargs van explicitos, ERR-38)',
              inspect.signature(V143G.run).parameters['eta_s'].default == 0.0
              and inspect.signature(V143G.run).parameters['norm_lenta'].default == 1))
    # R4 3T-k: el brazo N ES v14.3 (defectos de organismo_v143.run) y T142 ES v14.2
    s142 = inspect.signature(V142.run).parameters; s143 = inspect.signature(V143.run).parameters
    R.append(('R4 corre_n7.TRONCO == defectos de organismo_v142.run (25 campos)',
              all(c in s142 and s142[c].default == v for c, v in C7.TRONCO.items())))
    R.append(('R4 corre_n7.TRONCO == defectos de organismo_v143.run y norm_lenta por defecto == 1 == brazo N',
              all(c in s143 and s143[c].default == v for c, v in C7.TRONCO.items()) and s143['norm_lenta'].default == 1
              and C7.BRAZOS['N'] == ('C3', dict(norm_lenta=1))))
    R.append(('R4 brazos T142 = (C3, {}) y NC3C = (C3C, norm_lenta=1); NKMAX 90',
              C7.BRAZOS['T142'] == ('C3', {}) and C7.BRAZOS['NC3C'] == ('C3C', dict(norm_lenta=1))
              and C7.MUNDO['nkmax'] == V142.NKMAX == V143.NKMAX == 90))
    R.append(('R4 organismo_v143 y organismo_v142: mismas constantes de modulo (L, NK, NKMAX, K, PAT, R_VAL, E_VAL)',
              all(N_(getattr(V142, c).tolist() if hasattr(getattr(V142, c), 'tolist') else getattr(V142, c)) ==
                  N_(getattr(V143, c).tolist() if hasattr(getattr(V143, c), 'tolist') else getattr(V143, c))
                  for c in ('L', 'NK', 'NKMAX', 'K', 'R_VAL', 'E_VAL'))
              and all(np.array_equal(V142.PAT[k], V143.PAT[k]) for k in V142.PAT)))
    # R5 la letra restada aqui == la de los modulos de donde se importa (ERR-31)
    u4 = C4.U.V4; n = U.NUM
    R.append(('R5 T-A == umbrales_v4.V4[T-A] (1.10, 10, margen 10, z 1.645, n 80)',
              (u4['T-A']['muertes'], u4['T-A']['r_delta'], u4['T-A']['margen'], u4['T-A']['z'], u4['T-A']['n'])
              == (n['TA_muertes'], n['TA_r_delta'], n['TA_margen'], n['z'], n['n_vivo'])))
    R.append(('R5 T-C ii == umbrales_v4.V4[T-C_ii] (margen 12.5, n 80); T-F == 1.25',
              (u4['T-C_ii']['margen'], u4['T-C_ii']['n'], u4['T-F_vivo']['razon']) == (n['TC_margen'], n['n_vivo'], n['TF_razon'])))
    ub = D5.UMB['T-B']
    R.append(('R5 T-B == corre_dE5_v2.UMB[T-B] en G1, G2 y azar G1 (0.80, 0.85, [0.35, 0.65]): sin cambio',
              (ub['g1'], ub['g2'], tuple(ub['azar'])) == (n['TB_g1'], n['TB_g2'], n['TB_azar'])))
    # ERR-122: la UNICA diferencia con la letra importada, DECLARADA (no es falla): decide [0.31, 0.60]; el origen dice
    # [0.42, 0.58], que es la banda vieja que el runner sigue calculando y SOLO reporta.
    R.append(('R5 T-B azar G2: diferencia DECLARADA por ERR-122 (no es falla): decide [0.31, 0.60]; el origen corre_dE5_v2 '
              '[0.42, 0.58] == la banda vieja, que solo se reporta',
              tuple(n['TB_azar2']) == tuple(U.ERR122['banda_nueva']) == (0.31, 0.60)
              and tuple(ub['azar2']) == tuple(U.ERR122['banda_vieja']) == (0.42, 0.58)))
    R.append(('R5 T-E / T-C i / T-F examen == corre_dE5_v2 (TOL 1.10, TOL_COME 0.8, PUERTA_E 18, factor 1.25)',
              (D5.TOL, D5.TOL_COME, D5.PUERTA_E, D5.UMB['T-F']['factor']) == (n['tol'], n['tol_come'], n['puerta_E'], n['TF_razon'])
              and 'come B Q4 >= 50 (T-C i)' in [c for c, _ in D5.CLAUSULAS['E2']]))
    R.append(('R5 T-D: C1, C2, C6 existen en creacion_B/corre_codigo.UMBRALES (se importan, no se copian)',
              all(k in CC.UMBRALES for k in ('C1', 'C2', 'C6'))))
    R.append(('R5 T-G: G-3 == U[T4_sep], U[T4_lift] de corre_n7; T1..T5 sin tocar',
              (U.TG['G3_sep'], U.TG['G3_lift']) == (C7.U['T4_sep'], C7.U['T4_lift'])
              and (C7.U['T1_n'], C7.U['T2_sep'], C7.U['T3_lift'], C7.U['T5_dif'], C7.U['T5_n']) == (15, 1.5, 0.15, 1.0, 15)))
    # R6 semillas: disjuntas entre papeles y fuera de lo ya usado por los bloques que se reusan
    todas = []
    for modo in ('serie', 'replica', 'reserva'):
        S = U.SEMILLAS[modo]
        for k in ('EX', 'VIVO', 'TG', 'ALIAS', 'LIMPIAS'):
            todas += [(s, modo, k) for s in S.get(k, [])]
    todas += [(s, 'humo', '') for s in U.SEMILLAS['humo']] + [(s, 'identidad', '') for s in U.SEMILLAS['identidad']]
    ss = [s for s, _, _ in todas]
    usadas = set(range(2841, 2941)) | set(range(2361, 2441)) | set(range(7701, 7741)) | set(range(14281, 14341))
    R.append(('R6 semillas: todas distintas entre papeles, ninguna de V4-CAL, subida_n7 ni tronco_v14_3; TRONCO_B s+100000 libre',
              len(ss) == len(set(ss)) and not (set(ss) & usadas) and all(43000 <= s <= 44600 for s in ss)))
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


def iguales(a, b, fuera=('arm', 'org', 'seg', 'modulo', 'seed_real', '_lado')):
    ks = sorted((set(a) | set(b)) - set(fuera))
    return N_({k: a.get(k) for k in ks}) == N_({k: b.get(k) for k in ks})


def inercia(res, clave, cand, ref):
    """Cuantas corridas del candidato son IDENTICAS (bit a bit, todas las claves medidas) a las del tronco en la misma semilla."""
    A = {clave(r): r for r in res if r['_lado'] == cand}; B = {clave(r): r for r in res if r['_lado'] == ref}
    comun = sorted(set(A) & set(B), key=str)
    return sum(iguales(A[k], B[k]) for k in comun), len(comun)


def banda_TB():
    """Los umbrales con los que el examen DECIDE T-B. G1, G2, azar G1: la letra importada (corre_dE5_v2.UMB['T-B'], sin cambio).
    azar G2: ENMIENDA ERR-122 -> U.NUM['TB_azar2'] = [0.31, 0.60]. 'azar2_vieja' = la de la letra importada [0.42, 0.58]: SOLO
    INFORME (no entra en ninguna decision)."""
    u = D5.UMB['T-B']
    return dict(g1=u['g1'], g2=u['g2'], azar=tuple(u['azar']), azar2=tuple(U.NUM['TB_azar2']), azar2_vieja=tuple(u['azar2']))


def veredicto_TB(res):
    """T-B desde los valores CRUDOS de bateria_generaliza (acc, ba, cobertura por semilla), NO desde el veredicto interno de la
    bateria CONGELADA (que conserva su banda [0.42, 0.58]). ERR-122: decide azar G2 en [0.31, 0.60]; la banda vieja se calcula
    para CAND y TRONCO (v14.2 congelado en las MISMAS semillas; en T-B no hay TRONCO_B) y SOLO se reporta."""
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
        # SOLO INFORME (ERR-122): la misma puerta con la banda vieja [0.42, 0.58]. No entra en c['pasa'] ni en V['pasa'].
        c['c_azar2_banda_vieja'] = dentro(g2az, u['azar2_vieja'])
        c['pasa_banda_vieja'] = bool(c['c_G1'] and c['c_G2'] and c['c_azar1'] and c['c_azar2_banda_vieja'] and c['c_K'])
        V[org] = c
    for r in res:
        r['_lado'] = r['org']
    V['inercia'] = inercia(res, lambda r: (r['regla'], r['seed']), 'CAND', 'TRONCO')
    V['pasa'] = V['CAND']['pasa']   # decide el CANDIDATO con la banda de ERR-122
    V['banda_azar2'] = dict(err='ERR-122', decide=list(u['azar2']), vieja_solo_informe=list(u['azar2_vieja']))
    log(f"   T-B: CAND = v14.3 (bateria_generaliza_v143) y TRONCO = v14.2 (bateria_generaliza_v142, CONGELADA) en las MISMAS "
        f"semillas; azar G2 decide con {list(u['azar2'])} (ERR-122) para los dos")
    for org in U.ORGS_EX:
        c = V[org]
        log(f"   T-B [{org:6s}] G1 {_n(c['G1'])} (>= {u['g1']}) G2 {_n(c['G2'])} (>= {u['g2']}) azar G1 {_n(c['G1_azar'])} "
            f"(en {list(u['azar'])}) azar G2 {_n(c['G2_azar'])} (en {list(u['azar2'])}, ERR-122) K {c['K']}/{c['n']} -> "
            f"{'PASA' if c['pasa'] else 'NO'}   [G1 {c['c_G1']} G2 {c['c_G2']} azar1 {c['c_azar1']} azar2 {c['c_azar2']} K {c['c_K']}]")
    log(f"   T-B banda VIEJA de azar G2 {list(u['azar2_vieja'])} (letra v2-v4; SOLO INFORME, NO decide; ERR-122): "
        + ' | '.join(f"{org} azar G2 {_n(V[org]['G2_azar'])} {'dentro' if V[org]['c_azar2_banda_vieja'] else 'FUERA'} -> T-B "
                     f"{'PASA' if V[org]['pasa_banda_vieja'] else 'NO'}" for org in U.ORGS_EX))
    log(f"   T-B inercia medida: CAND == TRONCO bit a bit en {V['inercia'][0]}/{V['inercia'][1]} corridas (regla x semilla)")
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
             inercia=inercia(res, lambda r: (r['etapa'], r['seed']), 'CAND', 'TRONCO'))
    for e in U.SEIS:
        log(f"      T-E {e:4s} {con[e]['todas']}/{con[e]['n']} {'PASA' if con[e]['pasa'] else 'NO'}  {con[e]['detalle']}  "
            f"pesos (reportados) {con[e]['pesos_reportados']}")
    log(f"   T-C (i) [{U.LETRA['T-C_i']}] -> {ci}/{con['E2']['n']} -> {'PASA' if V['T_C_i']['pasa'] else 'NO'}")
    log(f"   T-E [{U.LETRA['T-E']}] -> " + ' '.join(f"{e} {con[e]['todas']}/{con[e]['n']}" for e in U.SEIS)
        + f" -> {'PASA' if V['T_E']['pasa'] else 'NO'}")
    log(f"   T-F examen [<= {D5.UMB['T-F']['factor']} x tronco] -> " + ' '.join(f"{q} {cost[q]['cand']}/{cost[q]['tronco']} ({cost[q]['razon']}x)" for q in cost)
        + f" -> {'PASA' if V['T_F']['pasa'] else 'NO'}")
    log(f"   examen: el TRONCO contra las clausulas absolutas: E2 come B >= 50 {V['tronco_letra_absoluta']['E2_comeB']}/20, "
        f"E2I tasa {V['tronco_letra_absoluta']['E2I_tasa']}/20; inercia CAND == TRONCO {V['inercia'][0]}/{V['inercia'][1]}")
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
    log(f"   T-D inercia medida: CAND == OFF bit a bit en {V['inercia'][0]}/{V['inercia'][1]}")
    return V


def veredicto_vivo(res_vivo, res_rev):
    """T-A, T-C (ii), T-F vivo con la letra CALIBRADA (corre_criterio_v4.juzga; v3 y v2 al lado, sin decidir)."""
    C4._log.update(f=_log['f'], t0=_log['t0'])   # que las lineas de la letra calibrada caigan en ESTE log
    V = {c: C4.juzga(res_vivo, res_rev, c) for c in ('CAND', 'TRONCO_B', 'PLACEBO')}
    C4._log.update(f=None)
    for r in res_vivo:
        r['_lado'] = r['arm']
    for r in res_rev:
        r['_lado'] = r['arm']
    V['inercia_TA'] = inercia(res_vivo, lambda r: (r['brazo'], r['seed']), 'CAND', 'OFF')
    V['inercia_TC'] = inercia(res_rev, lambda r: r['seed'], 'CAND', 'OFF')
    V['legible'] = bool(V['TRONCO_B']['v4'])
    log(f"   inercia medida en el mundo vivo: CAND == OFF bit a bit en T-A {V['inercia_TA'][0]}/{V['inercia_TA'][1]}, "
        f"T-C (ii) {V['inercia_TC'][0]}/{V['inercia_TC'][1]}")
    log(f"   TRONCO_B (el tronco contra si mismo, s+100000) {'PASA' if V['legible'] else '*** NO PASA: la serie del mundo vivo NO SE LEE'} | "
        f"PLACEBO (reportado) {'PASA' if V['PLACEBO']['v4'] else 'NO'}")
    return V


def veredicto_TG(res, n):
    ks = U.TG['ks']
    V, kmax = C7.criterios(res, ks, n)
    g1 = kmax.get('N', 0) >= U.TG['G1_kmax']
    g2d = {k: V[k].get('N', {}).get('lift_N>T142') for k in U.TG['G2_ks']}
    g2 = all(x is not None and x >= U.TG['G2_n'] for x in g2d.values())
    g3d = {k: (V[k].get('NC3C', {}).get('sep'), V[k].get('NC3C', {}).get('lift_q4')) for k in ks}
    g3 = all(s is not None and l is not None and s < U.TG['G3_sep'] and l < U.TG['G3_lift'] for s, l in g3d.values())
    for k in ks:
        log('      T-G k=%d  ' % k + '  '.join(f"{b} sep {_n(V[k][b]['sep'], '+.2f')} lift {_n(V[k][b]['lift_q4'])} celdas {V[k][b]['celdas']} "
                                              f"{'compone' if V[k][b]['compone'] else '-'}" for b in U.TG['brazos'] if b in V[k])
            + f"  N>T142 {V[k].get('N', {}).get('lift_N>T142')}  T5 {V[k].get('N', {}).get('T5_n')}")
    log(f"   T-G [{U.LETRA['T-G']}] -> K_max {kmax} ; G-1 {g1} | G-2 {g2d} {g2} | G-3 {g3} -> {'PASA' if (g1 and g2 and g3) else 'NO'}")
    return dict(K_max=kmax, G1=bool(g1), G2=dict(n=g2d, pasa=bool(g2)), G3=dict(nc3c=g3d, pasa=bool(g3)),
                pasa=bool(g1 and g2 and g3), por_k={str(k): V[k] for k in ks})


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
    sustituye T-A, T-C (ii) y T-F vivo de la serie cuyo mundo vivo no se leyo (--sustituye)."""
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
            for k in ('T-A', 'T-C_ii', 'T-F_vivo'):
                sub[k] = r['sub'][k]
            nota = f" (mundo vivo sustituido por la reserva {n})"
        P = puertas_de(sub)
        caen = [k for k in PUERTAS if P[k] is False]; faltan = [k for k in PUERTAS if P[k] is None]
        estado[modo] = ('NO SE LEE' if leg is False else ('NO PASA' if caen else ('INCOMPLETO' if faltan else 'PASA')))
        lineas.append(f"   {modo} [{nombre}]{nota}: legible {leg}; " + ' '.join(
            f"{k} {'PASA' if P[k] else ('NO' if P[k] is False else 'sin medir')}" for k in PUERTAS) + f" -> {estado[modo]}")
        tb = (j.get('veredictos') or {}).get('TB') or {}
        if tb.get('banda_azar2'):   # ERR-122: lo que decide y, al lado, la banda vieja SOLO como informe
            pv = lambda o, c: 'PASA' if (tb.get(o) or {}).get(c) else 'NO'
            lineas.append(f"      T-B {modo}: azar G2 CAND {_n((tb.get('CAND') or {}).get('G2_azar'))} TRONCO "
                          f"{_n((tb.get('TRONCO') or {}).get('G2_azar'))}; decide {tb['banda_azar2']['decide']} (ERR-122): "
                          f"CAND {pv('CAND', 'pasa')} TRONCO {pv('TRONCO', 'pasa')} | banda vieja "
                          f"{tb['banda_azar2']['vieja_solo_informe']} SOLO INFORME: CAND {pv('CAND', 'pasa_banda_vieja')} "
                          f"TRONCO {pv('TRONCO', 'pasa_banda_vieja')}")
    e = set(estado.values())
    if e == {'PASA'}:
        return ("VEREDICTO DEL EXAMEN: PASA -- v14.3 cruza la letra de CRITERIO_TRONCO_v4 en serie y replica, en semillas nuevas. "
                "Por el permiso escrito del director (23-sep 19:30) el coordinador puede congelarlo (PREREGISTRO §10)."), lineas
    if 'NO PASA' in e:
        return ("VEREDICTO DEL EXAMEN: NO PASA -- v14.3 no se congela; v14.2 sigue siendo el tronco. Si la puerta que cae cae "
                "igual en el tronco (inercia medida), se registra con ERR como defecto de la letra, no de N (PREREGISTRO §6)."), lineas
    if 'NO SE LEE' in e:
        return ("VEREDICTO DEL EXAMEN: NO SE LEE -- una serie del mundo vivo no se lee ni con la reserva; decide el coordinador "
                "con ERR (PREREGISTRO §6)."), lineas
    return "VEREDICTO DEL EXAMEN: INCOMPLETO -- faltan puertas por medir.", lineas


# ------------------------------------------------------------------ crudos SINTETICOS (humo: cablear la etapa 8 sin simular)
def sinteticos(n_vivo, n_ex, alias, limpias, malo=False):
    """Numeros INVENTADOS con los formatos reales. No son evidencia; prueban que la etapa 8 llega al final y dice NO cuando
    el candidato es malo (malo=True: CAND con r y rev 40 peor, azar G2 fuera de banda, W[sal] 1.45 y N sin componer)."""
    g = np.random.default_rng(20260923)
    seeds_v = list(range(1, n_vivo + 1)); seeds_e = list(range(1, n_ex + 1))
    RV, RR = [], []
    for b, (mr, sr) in (('VIVO', (-75.0, 12.0)), ('CUELLO_MIN', (-8.0, 13.5))):
        for s in seeds_v:
            base = dict(r=float(g.normal(mr, sr)), deaths=float(g.normal(94, 10)), celdas=37.0, splits=float(g.integers(4, 10)))
            for arm in U.ARMS_VIVO:
                x = dict(base) if arm in ('OFF', 'CAND') else dict(r=float(g.normal(mr, sr)), deaths=float(g.normal(94, 10)), celdas=37.0,
                                                                     splits=float(g.integers(4, 10)))
                if malo and arm == 'CAND':
                    x['r'] -= 40.0
                RV.append(dict(x, brazo=b, seed=s, arm=arm, seed_real=s + (100000 if arm == 'TRONCO_B' else 0)))
    for s in seeds_v:
        base = dict(rev=float(g.normal(42, 20)), deaths=float(g.normal(97, 10)), celdas=37.0, splits=float(g.integers(4, 10)),
                    visA=[0, 0, 0, 1700], visB=[0, 0, 0, 220])
        for arm in U.ARMS_VIVO:
            x = dict(base) if arm in ('OFF', 'CAND') else dict(base, rev=float(g.normal(42, 20)))
            if malo and arm == 'CAND':
                x['rev'] -= 40.0
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
    TG = []
    for k in U.TG['ks']:
        for s in seeds_e:
            for b in U.TG['brazos']:
                if b == 'N' and not malo:
                    sep, lf = 3.9, 0.37
                elif b == 'T142' or (b == 'N' and malo):
                    sep, lf = (3.9, 0.38) if k == 1 else (1.0, 0.0)
                else:
                    sep, lf = 0.05, 0.0
                TG.append(dict(brazo=b, k=k, seed=s, sep=sep + 0.01 * s, lift_q4=lf, lift_q4_none=False, solap_A=0, celdas=40,
                               splits=5, n_des=0, deaths=100, mordidas=1500))
    return RV, RR, TB, EXr, TD, TG


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
            tb = V['TB']   # ERR-122: decide la banda nueva; el TRONCO y la banda vieja van al lado, SOLO como informe
            det = (f"[{U.LETRA[k]}] | TRONCO (mismas semillas, banda ERR-122) {dl(tb['TRONCO']['pasa'])} | banda VIEJA "
                   f"{tb['banda_azar2']['vieja_solo_informe']} (SOLO INFORME): CAND {dl(tb['CAND']['pasa_banda_vieja'])}, "
                   f"TRONCO {dl(tb['TRONCO']['pasa_banda_vieja'])}")
        else:
            det = f"[{U.LETRA[k]}]"
        log(f"   {k}: {dl(P[k])}   {det}")
    log(f"   T-H: NO MEDIDA — {U.LETRA['T-H']}")
    frase = frase_serie(P, legible, modo)
    log(f"VEREDICTO: {frase}")
    return sub, P, legible, frase


# ------------------------------------------------------------------ principal
def argumentos():
    ap = argparse.ArgumentParser(prog='corre_examen_v143.py', allow_abbrev=False,
                                 description='Examen del criterio de tronco v4 sobre v14.3 (ver PREREGISTRO_examen_v143.md).')
    m = ap.add_mutually_exclusive_group(required=True)
    m.add_argument('--humo', action='store_true', help='UN proceso, 6 corridas cortas, cableado sintetico, JSON en datos/humo/')
    m.add_argument('--serie', action='store_true', help='la serie (semillas de umbrales_examen_v143.SEMILLAS["serie"])')
    m.add_argument('--replica', action='store_true', help='la replica (semillas nuevas, SEMILLAS["replica"])')
    m.add_argument('--reserva', action='store_true', help='SOLO si TRONCO_B no paso en una serie: mundo vivo en SEMILLAS["reserva"]')
    m.add_argument('--combina', nargs='+', metavar='JSON', help='no corre nada: veredicto del examen con los JSON de serie, replica [y reserva]')
    m.add_argument('--analiza', metavar='PREFIJO', help='no corre nada: relee los crudos <PREFIJO>_crudo_*.json y rehace el veredicto')
    ap.add_argument('--pool', type=int, default=None, help='procesos del Pool (1..6); obligatorio en serie/replica/reserva')
    ap.add_argument('--solo', default=None, help='subconjunto de etapas: TB,EX,TD,TC,TA,TG (veredicto INCOMPLETO)')
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
        malas = set(a.solo.split(',')) - {'TB', 'EX', 'TD', 'TC', 'TA', 'TG'}
        if malas:
            ap.error(f'--solo: etapas desconocidas {sorted(malas)}')
    return a


def reanaliza(prefijo):
    """ERR-54: los crudos estan en disco ANTES del analisis; si el analisis se cae, esto lo rehace sin correr nada."""
    base = os.path.basename(prefijo)
    m = re.match(r'examen_v143_(serie|replica|reserva)_\d{8}_\d{6}$', base)
    if not m:
        raise SystemExit(f'*** --analiza espera examen_v143_<serie|replica|reserva>_<AAAAMMDD_HHMMSS>, no {base!r}')
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
    c = lee('TG')
    if c is not None:
        V['TG'] = veredicto_TG(c, len({r['seed'] for r in c}))
    meta = dict(modo=modo, reanalisis_de=base, fecha=time.strftime('%Y-%m-%dT%H:%M:%S'), letra=U.LETRA, err122=U.ERR122,
                shas=dict(runner=h16(os.path.abspath(__file__)), umbrales=h16(os.path.join(AQUI, 'umbrales_examen_v143.py'))))
    if modo == 'reserva':
        sub = subpuertas(V); leg = None if V.get('vivo') is None else bool(V['vivo']['legible'])
        out = dict(meta=meta, legible=leg, sub=sub, veredictos=V)
        log(f"VEREDICTO (reserva, reanalisis): legible {leg}; T-A {sub['T-A']} T-C (ii) {sub['T-C_ii']} T-F vivo {sub['T-F_vivo']}")
    else:
        sub, P, leg, frase = etapa8(V, modo)
        out = dict(meta=meta, legible=leg, sub=sub, puertas=P, frase=frase, veredictos=V)
    dj = os.path.join(carpeta, _log['nom'] + '.json')
    json.dump(out, open(dj, 'w', encoding='utf-8'), ensure_ascii=False, default=str)
    log(f'datos -> {dj}  sha256_16 = {h16(dj)}  (para --combina, usar ESTE json; lleva meta.modo = {modo})')
    _log['f'].close()
    return 0


def main():
    a = argumentos()
    if a.analiza:
        return reanaliza(a.analiza)
    if a.combina:
        frase, lineas = combina(a.combina)
        for l in lineas:
            print(l)
        print(frase)
        return 0
    modo = 'humo' if a.humo else ('serie' if a.serie else ('replica' if a.replica else 'reserva'))
    POOL = 1 if a.humo else a.pool
    SOLO = set(a.solo.split(',')) if a.solo else None
    hacer = lambda e: SOLO is None or e in SOLO
    stamp = time.strftime('%Y%m%d_%H%M%S')
    nom = f'examen_v143_{modo}_{stamp}'
    _log['nom'] = nom
    SAL = DATOS_HUMO if a.humo else DATOS_EX
    os.makedirs(SAL, exist_ok=True)
    _log['f'] = open(os.path.join(SAL, nom + '.log'), 'w', encoding='utf-8', newline='\n')
    log(f"ARRANQUE examen v4 sobre v14.3 — modo {modo}, {'UN proceso, sin Pool' if a.humo else f'Pool {POOL}'}, python "
        f"{platform.python_version()}, numpy {np.__version__}, {platform.platform()}")
    log('MISION: llegar a la AGI por este camino; el examen v4 es la puerta de NO REGRESION del organismo comun.')
    # ---------------------------------------------------------------- ETAPA 0
    log('ETAPA 0 — anclas, construccion por anclas, regla 14, semillas de T-D recalculadas.')
    shas_const = verifica_anclas()
    pre = os.path.join(AQUI, 'PREREGISTRO_examen_v143.md')
    SHAS = dict(construidos=shas_const, anclas={os.path.relpath(p, RAIZ).replace(os.sep, '/'): s for p, s in ANCLAS.items()},
                runner=h16(os.path.abspath(__file__)), umbrales=h16(os.path.join(AQUI, 'umbrales_examen_v143.py')),
                identidad=h16(os.path.join(AQUI, 'identidad_v143ex.py')) if os.path.exists(os.path.join(AQUI, 'identidad_v143ex.py')) else None,
                construye=h16(os.path.join(AQUI, 'construye_v143.py')),
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
                procesos_python=ps, letra=U.LETRA, err122=U.ERR122, predicciones=U.PRED, sustituye=a.sustituye)
    log(f"   ERR-122 (enmienda antes de la serie): T-B decide azar G2 con {list(U.NUM['TB_azar2'])}; la banda vieja "
        f"{list(U.ERR122['banda_vieja'])} se reporta para CAND y TRONCO y NO decide.")

    # ================================================================ HUMO
    if a.humo:
        h = U.SEMILLAS['humo']; Th = U.T_HUMO
        log(f'HUMO 1/3 — 6 corridas de un proceso (T-A VIVO OFF y CAND s{h[0]} T={Th}; T-C ii CAND s{h[1]} T={Th}; '
            f'T-D CAND ALIAS 326 T={Th}; examen E2 CAND s{h[2]} T=100000; T-G N k=5 s{h[3]} T={Th}).')
        t0 = time.time()
        o_off = tarea_vivo(('VIVO', h[0], 'OFF', Th)); o_cand = tarea_vivo(('VIVO', h[0], 'CAND', Th))
        o_rev = tarea_rev((h[1], 'CAND', Th)); o_sal = tarea_sal(('S1-ALIAS', 326, 'CAND', Th))
        o_ex = tarea_ex(('CAND', 'E2', h[2])); o_tg = tarea_tg(('N', 5, h[3], Th))
        iner = iguales(o_off, o_cand)
        log(f"   T-A VIVO OFF  s{h[0]}: r {o_off['r']} desc {o_off['descendientes']} muertes {o_off['deaths']} celdas {o_off['celdas']} "
            f"splits {o_off['splits']} ({o_off['seg']} s)")
        log(f"   T-A VIVO CAND s{h[0]}: r {o_cand['r']} desc {o_cand['descendientes']} muertes {o_cand['deaths']} celdas {o_cand['celdas']} "
            f"splits {o_cand['splits']} ({o_cand['seg']} s)  -> CAND == OFF bit a bit: {iner} (DEBE ser True: N inerte, masa 3)")
        log(f"   T-C ii CAND s{h[1]}: rev {o_rev['rev']} visB {o_rev['visB']} muertes {o_rev['deaths']} ({o_rev['seg']} s)")
        log(f"   T-D CAND ALIAS 326: |W[sal]| {o_sal['w_sal']} W[veneno] {o_sal['w_veneno']} exp sal {o_sal['exp_sal']} "
            f"des_splits {o_sal['des_splits']} ({o_sal['seg']} s)")
        log(f"   examen E2 CAND s{h[2]}: come B Q4 {o_ex['mord']['B'][3]} (>= 50) W {o_ex['W']} ({o_ex['seg']} s)")
        log(f"   T-G N k=5 s{h[3]}: sep {o_tg['sep']} lift_q4 {o_tg['lift_q4']} celdas {o_tg['celdas']} ({o_tg['seg']} s)")
        seg = dict(vivo=(o_off['seg'] + o_cand['seg']) / 2 * (U.T_VIVO / Th), rev=o_rev['seg'] * (U.T_VIVO / Th),
                   sal=o_sal['seg'] * (U.T_VIVO / Th), ex=o_ex['seg'], tg=o_tg['seg'] * (U.TG['T'] / Th), tb=2.0 * o_ex['seg'])
        n = dict(tb=2 * 2 * 20, ex=2 * 6 * 20, sal=2 * 18, rev=4 * 80, vivo=2 * 4 * 80, tg=3 * 8 * 20)
        cpu = sum(seg[k] * n[k] for k in n)
        log(f"   DURACION por corrida (T completo, lineal desde T={Th}; T-B supuesto 2 x examen): "
            + ' '.join(f"{k} {seg[k]:.1f}s" for k in seg))
        log(f"   COSTO por serie: {sum(n.values())} corridas ~ {cpu/3600:.1f} h de CPU de ESTE proceso -> Pool 6 ~ {cpu/6/60:.0f} min "
            f"(+ identidad ~5 min); nube Pool 3 (nucleo 1.3-2.2x mas rapido) ~ {cpu/3/1.75/60:.0f} min. Serie + replica: el doble.")
        log('HUMO 2/3 — CABLEADO de la etapa 8 con crudos SINTETICOS (n reales: 80 vivo, 20 examen, 9+9 sal, 20 x 8 k). NO son evidencia.')
        S = U.SEMILLAS['serie']
        cab = {}
        for malo in (False, True):
            RV, RR, TB, EXr, TD, TG = sinteticos(80, 20, S['ALIAS'], S['LIMPIAS'], malo=malo)
            Vs = dict(TB=veredicto_TB(TB), EX=veredicto_EX(EXr), TD=veredicto_TD(TD), vivo=veredicto_vivo(RV, RR), TG=veredicto_TG(TG, 20))
            sub, P, leg, frase = etapa8(Vs, 'humo-sintetico-' + ('MALO' if malo else 'bueno'))
            cab['malo' if malo else 'bueno'] = dict(sub=sub, puertas=P, legible=leg, frase=frase)
        # ERR-122: la banda nueva DECIDE y la vieja solo se reporta. azar G2 0.36 en CAND y TRONCO (dentro de [0.31, 0.60],
        # fuera de [0.42, 0.58]): T-B debe PASAR y la banda vieja debe decir NO sin decidir.
        TB122 = [dict(r, ba=0.36) if r['regla'] == 'azar' else r for r in sinteticos(80, 20, S['ALIAS'], S['LIMPIAS'])[2]]
        v122 = veredicto_TB(TB122)
        b122 = bool(v122['pasa'] and all(v122[o]['pasa'] and not v122[o]['pasa_banda_vieja'] for o in U.ORGS_EX))
        cab['ERR122'] = dict(azar_G2=0.36, decide=v122['banda_azar2'], pasa=v122['pasa'],
                             pasa_banda_vieja={o: v122[o]['pasa_banda_vieja'] for o in U.ORGS_EX}, ok=b122)
        log(f"   cableado ERR-122 (azar G2 0.36 en CAND y TRONCO): T-B {'PASA' if v122['pasa'] else 'NO'} con {v122['banda_azar2']['decide']}; "
            f"la banda vieja dice {'NO' if not v122['CAND']['pasa_banda_vieja'] else 'PASA'} y no decide -> {'OK' if b122 else '*** revisar'}")
        cab_ok = bool(all(cab['bueno']['puertas'].values()) and cab['bueno']['legible']
                      and not any(cab['malo']['puertas'][k] for k in ('T-A', 'T-B', 'T-C', 'T-D', 'T-G')) and b122)
        log(f"   cableado: bueno {cab['bueno']['puertas']} | malo {cab['malo']['puertas']} | ERR-122 {b122} -> "
            f"{'OK' if cab_ok else '*** revisar'} (el bueno DEBE pasar todo; el malo DEBE caer T-A, T-B, T-C, T-D y T-G; "
            f"con azar G2 0.36 T-B DEBE pasar por la banda nueva)")
        log('HUMO 3/3 — JSON.')
        dj = os.path.join(SAL, nom + '.json')
        json.dump(dict(meta=dict(meta, humo=True, corridas=6, pasos=5 * Th + 100000, semillas=dict(humo=h, alias_historica=326),
                                 regla14=[(n_, ok) for n_, ok in R14], inercia_TA_VIVO=iner, duracion_s=seg,
                                 costo=dict(corridas_por_serie=sum(n.values()), cpu_h=round(cpu / 3600, 2), pool6_min=round(cpu / 6 / 60),
                                            nube_pool3_min=round(cpu / 3 / 1.75 / 60)),
                                 cableado=cab, cableado_ok=cab_ok, seg_total=round(time.time() - t0, 1)),
                       vivo=[o_off, o_cand], reversion=o_rev, sal=o_sal, examen=o_ex, tg=o_tg),
                  open(dj, 'w', encoding='utf-8'), ensure_ascii=False, default=str)
        log(f'datos -> {os.path.relpath(dj, RAIZ)}  sha256_16 = {h16(dj)}')
        ok = bool(iner and cab_ok and r14ok)
        log(f"VEREDICTO DEL HUMO: {'OK' if ok else '*** FALLA'} (no es evidencia; prueba que el examen mide y que el juez puede decir NO)")
        _log['f'].close()
        return 0 if ok else 1

    # ================================================================ SERIE / REPLICA / RESERVA
    S = U.SEMILLAS[modo]
    if modo != 'reserva':
        ok, sel = guarda_semillas_TD(modo)
        log(f"   T-D {modo}: ALIAS {sel['alias']} LIMPIAS {sel['limpias']} recalculadas -> {'coinciden' if ok else '*** NO COINCIDEN'}")
        if not ok:
            log('*** la seleccion estructural de T-D no se reproduce: se para.'); _log['f'].close(); return 1
    log(f"ETAPA 1 — identidad (subproceso, un proceso): identidad_v143ex.py -> debe dar '{U.ARNES_ESPERADO}'.")
    t1 = time.time()
    p = subprocess.run([sys.executable, os.path.join(AQUI, 'identidad_v143ex.py')], capture_output=True, text=True, cwd=AQUI,
                       encoding='utf-8', errors='replace')
    cola = (p.stdout or '').strip().splitlines()
    for l in cola[-8:]:
        log(f'      | {l}')
    ultima = cola[-1] if cola else ''
    mj = re.findall(r'identidad_v143ex_(\d{8}_\d{6})\.json', p.stdout or '')   # ERR-87: prefijo + sello exacto
    meta['identidad'] = dict(ultima=ultima, returncode=p.returncode, json=(f'identidad_v143ex_{mj[-1]}.json' if mj else None),
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
        t = [(b, s, arm, U.T_VIVO) for b in U.BRAZOS_TA for s in S['VIVO'] for arm in U.ARMS_VIVO]
        log(f"ETAPA 6 — T-A supervivencia: {len(t)} corridas, Pool {POOL}.")
        res_vivo = crudos['TA'] = crudo('TA', pool_map(tarea_vivo, t, 'T-A', POOL), SAL, extra=dict(semillas=S['VIVO']))
    if res_rev is not None and res_vivo is not None:
        log('   letra v4 calibrada (corre_criterio_v4.juzga) sobre CAND, TRONCO_B y PLACEBO contra OFF:')
        V['vivo'] = veredicto_vivo(res_vivo, res_rev)
    if modo != 'reserva' and hacer('TG'):
        t = [(b, k, s, U.TG['T']) for k in U.TG['ks'] for b in U.TG['brazos'] for s in S['TG']]
        log(f"ETAPA 7 — T-G composicion 3T-k: {len(t)} corridas, semillas {S['TG'][0]}-{S['TG'][-1]}, Pool {POOL}.")
        crudos['TG'] = crudo('TG', pool_map(tarea_tg, t, 'T-G', POOL), SAL, extra=dict(semillas=S['TG']))
        V['TG'] = veredicto_TG(crudos['TG'], len(S['TG']))
    # ---------------------------------------------------------------- ETAPA 8
    if modo == 'reserva':
        sub = subpuertas(V)
        leg = None if V.get('vivo') is None else bool(V['vivo']['legible'])
        log(f"VEREDICTO (reserva; sustituye el mundo vivo de la {a.sustituye}): legible {leg}; T-A {sub['T-A']} "
            f"T-C (ii) {sub['T-C_ii']} T-F vivo {sub['T-F_vivo']}")
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
