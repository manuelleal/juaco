"""v15f bajo el CRITERIO DE TRONCO v2 (registro/CRITERIO_TRONCO_v2.md). Ejecuta PREREGISTRO_v15f_v2.md.
REGLA 10: log desde el arranque. REGLA 11: un Pool a la vez (subprocesos SECUENCIALES; el Pool propio solo en T-D, T-C ii, T-A y T-G).
ERR-43: los veredictos de las baterias se LEEN de sus JSON, no del log. ERR-54: los datos CRUDOS de cada etapa con Pool se
vuelcan a `datos/` ANTES de analizarlos. Reutiliza por import (sin copiar): corre_vivo_rep2 (BRAZOS, resumen2), corre_sal
(BASE, BRAZOS, ALIAS, LIMPIAS, resumen), mini_vivo (BRAZOS), corre_codigo (UMBRALES C1/C2/C6 de B-5) y corre_v15f (tarea del
mundo de regla, REGLAS, KW14 = los kwargs del tronco, ERR-41).

  ETAPA 1  identidad (`identidad_vivo_relevo.py`, subproceso, un proceso): 28 identidades + 5 controles que DEBEN fallar = 33/33, o se para.
  ETAPA 2  T-B  generalizacion del candidato: `bateria_generaliza_v15f.py organismo_v15f_on 20 --desde 121 --log` (subproceso, Pool propio).
  ETAPA 3  examen v3' del candidato en 121-140: `bateria_v15f.py 20 --desde 121 --log` (subproceso, Pool propio) -> T-C (i), T-E, T-F.
  ETAPA 4  examen v3' del TRONCO en 121-140: se LEE un JSON de v14.1 (sha feefc88b1fd8d434, desde 121, 20 semillas) si existe;
           si no, `organismo/bateria_v14.py 20 --desde 121 --log` (subproceso, Pool propio).
  ETAPA 5  T-D  bloque de la sal con organismo_vivo_relevo: 9 ALIAS + 9 LIMPIAS x {OFF, v15f, v15g} (Pool aqui).
  ETAPA 6  T-C (ii) reversion en el mundo vivo (invertir_vivo_en=50000), semillas 321-340 x {OFF, v15f, v15g} (Pool aqui).
  ETAPA 7  T-A  mundo vivo de rep2, brazos VIVO y CUELLO_MIN, CON y SIN relevo, semillas 301-320 (Pool aqui):
           muertes <= 1.10 x tronco (mediana), r = descendientes - muertes >= tronco - 10, A12 pareado >= 0.50.
  ETAPA 8  T-G  capacidad nueva: xor01 ESTRICTA con 8 ejemplos en el mundo de regla con los kwargs del tronco, 181-200,
           ON/OFF pareado (Pool aqui): xor01 estricta >= 0.75, azar en [0.35, 0.65], px0 ON >= OFF.
  ETAPA 9  veredicto de las SIETE puertas y JSON.

Uso:  python experimentos/creacion_A/corre_v15f_v2.py
      python experimentos/creacion_A/corre_v15f_v2.py --humo     (UN proceso, sin Pool, 3 semillas: 326 ALIAS, 301 vivo, 321 reversion)
      python experimentos/creacion_A/corre_v15f_v2.py --solo TA,TG      (subconjunto de etapas; el resto se salta)
"""
import sys, os, json, time, hashlib, platform, subprocess, glob
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
import numpy as np

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
VIVO = os.path.join(RAIZ, 'experimentos', 'nivel11_mundo_vivo')
CREB = os.path.join(RAIZ, 'experimentos', 'creacion_B')
ORG = os.path.join(RAIZ, 'organismo')
DATOS = os.path.join(RAIZ, 'datos')
sys.path[:0] = [ORG, VIVO, CREB, AQUI]   # organismo/ PRIMERO (ERR-28)
HUMO = '--humo' in sys.argv
SOLO = (sys.argv[sys.argv.index('--solo') + 1].split(',') if '--solo' in sys.argv else None)
T = 100000
SEEDS_EX = list(range(121, 141))     # T-B, T-C (i), T-E, T-F examen
SEEDS_REV = list(range(321, 341))    # T-C (ii)
SEEDS_TA = list(range(301, 321))     # T-A  (NUEVAS: 301-320)
SEEDS_TG = list(range(181, 201))     # T-G  (NUEVAS: 181-200; la medida de 161-180 se repite aqui)
BRAZOS_TA = ('VIVO', 'CUELLO_MIN')
SHA_TRONCO = 'feefc88b1fd8d434'
N_PARALELO = int(os.environ.get('JUACO_POOL', 14))  # ERR-86: el tamano del Pool se fija por JUACO_POOL (21 sep, coordinador)
ARMS = {'OFF': dict(memoria_pares=None), 'v15f': dict(memoria_pares='relevo'), 'v15g': dict(memoria_pares='relevo', relevo_boca=1)}
ARMS_TA = ('OFF', 'v15f')            # T-A: "con y sin relevo" (el brazo exploratorio v15g no es candidato)
# --- umbrales de T-A (letra de CRITERIO_TRONCO_v2.md, tabla T-A) y de T-G (capacidad nueva del preregistro de v15f)
UMB_TA = dict(frase="muertes <= 1.10 x tronco (mediana) y r = descendientes - muertes >= tronco - 10; pareado por semilla A12 >= 0.50",
              muertes=1.10, r_delta=10.0, a12=0.50)
UMB_TG = dict(frase="xor01 ESTRICTA >= 0.75 con 8 ejemplos, kwargs del tronco; azar en [0.35, 0.65]; px0 ON >= OFF",
              xor=0.75, azar=(0.35, 0.65))
TOL = 1.10; TOL_COME = 0.8; PUERTA_E = 18
_log = {'f': None, 't0': time.time()}


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
    """A12 PAREADO por semilla: P(x > y) + 0.5 P(x == y) sobre los pares (misma semilla)."""
    pares = [(x, y) for x, y in zip(xs, ys) if x is not None and y is not None]
    return None if not pares else round(float(np.mean([1.0 if x > y else (0.5 if x == y else 0.0) for x, y in pares])), 3)


# ------------------------------------------------------------------ tareas (importan dentro: aptas para Pool)
def tarea_sal(args):
    brazo, seed, arm = args
    import corre_sal as CS, organismo_vivo_relevo as VR
    kw = dict(CS.BRAZOS[brazo][0])
    r = VR.run(seed, T=T, **kw, **ARMS[arm])
    o = CS.resumen(brazo, seed, r); o.update(arm=arm, W_tabla=r.get('W_tabla'), ganadora=r.get('mem_ganadora'))
    return o


def tarea_rev(args):
    seed, arm = args
    import mini_vivo as MV, organismo_vivo_relevo as VR
    kw = dict(MV.BRAZOS['VIVO'], invertir_vivo_en=T // 2)
    r = VR.run(seed, T=T, **kw, **ARMS[arm])
    return dict(seed=seed, arm=arm, mordA=r['mord']['A'], mordB=r['mord']['B'], rev=r['mord']['B'][3] - r['mord']['A'][3],
                deaths=r['deaths'], muertes_nec=r['muertes_nec'], W_nec=r['W_nec'], W_tabla=r.get('W_tabla'), celdas=r['celdas'], splits=r['splits'])


def tarea_vivo(args):
    brazo, seed, arm = args
    import corre_vivo_rep2 as CR2, organismo_vivo_relevo as VR
    kw = CR2.BRAZOS[brazo]
    r = VR.run(seed, T=T, **kw, **ARMS[arm])
    o = CR2.resumen2(brazo, seed, r, kw, T); o.update(arm=arm, W_tabla=r.get('W_tabla'))
    return o


def tarea_xor(args):
    """T-G: una corrida del mundo de REGLA con los kwargs del tronco. Se reutiliza `corre_v15f.tarea` POR IMPORT
    (ERR-41: los kwargs del tronco viven alli, en KW14, y no se copian aqui)."""
    import corre_v15f as C15
    return C15.tarea(args)


# ------------------------------------------------------------------ examen: CONDUCTA por escenario (T-E, T-C i) y coste (T-F)
def ven_total(r, k): return sum(r['mord'][k])
def tasa(r, k, i): return 100 * r['mord'][k][i] / max(r['vis'][k][i], 1)
CLAUSULAS = {   # (nombre, f(cand, tronco) -> bool); la letra de PREREGISTRO_v15f_v2.md §4
    'E1':  [('veneno B total <= 1.10 x tronco', lambda c, t: ven_total(c, 'B') <= TOL * ven_total(t, 'B')),
            ('come A Q4 >= 0.8 x tronco', lambda c, t: c['mord']['A'][3] >= TOL_COME * t['mord']['A'][3])],
    'E2':  [('come B Q4 >= 50 (T-C i)', lambda c, t: c['mord']['B'][3] >= 50),
            ('muerde A Q4 <= 1.10 x tronco', lambda c, t: c['mord']['A'][3] <= TOL * t['mord']['A'][3])],
    'E2I': [('veneno C total <= 1.10 x tronco', lambda c, t: ven_total(c, 'C') <= TOL * ven_total(t, 'C')),
            ('tasaA Q4 >= 80% Q2', lambda c, t: tasa(c, 'A', 3) >= .8 * tasa(c, 'A', 1))],
    'E2J': [('come D Q4 >= 0.8 x tronco', lambda c, t: c['mord']['D'][3] >= TOL_COME * t['mord']['D'][3]),
            ('veneno B total <= 1.10 x tronco', lambda c, t: ven_total(c, 'B') <= TOL * ven_total(t, 'B'))],
    'E2K': [('come D Q4 >= 0.8 x tronco', lambda c, t: c['mord']['D'][3] >= TOL_COME * t['mord']['D'][3]),
            ('veneno B total <= 1.10 x tronco', lambda c, t: ven_total(c, 'B') <= TOL * ven_total(t, 'B'))],
    'E2L': [('veneno B total <= 1.10 x tronco', lambda c, t: ven_total(c, 'B') <= TOL * ven_total(t, 'B')),
            ('come A Q4 >= 0.8 x tronco', lambda c, t: c['mord']['A'][3] >= TOL_COME * t['mord']['A'][3])],
}
PESOS = {'E1': ('W_B≈-3', lambda r: abs(r['W']['B'] + 3) < .3), 'E2': ('W_A→-3 y W_B→+1', lambda r: abs(r['W']['A'] + 3) < .3 and abs(r['W']['B'] - 1) < .15),
         'E2I': ('W_C≤-2.5', lambda r: r['W']['C'] <= -2.5), 'E2J': ('W_D≥0.85', lambda r: r['W']['D'] >= .85),
         'E2K': ('W_D≥0.8', lambda r: r['W']['D'] >= .8), 'E2L': ('W_B≈-3', lambda r: abs(r['W']['B'] + 3) < .3)}
SEIS = ['E1', 'E2', 'E2I', 'E2J', 'E2K', 'E2L']


def conducta(jc, jt):
    C = {(r['etapa'], r['seed']): r for r in jc['corridas']}; Tr = {(r['etapa'], r['seed']): r for r in jt['corridas']}
    seeds = sorted({s for e, s in C if e == 'E1'})
    out = {}
    for e in SEIS:
        det = {}; todas = 0
        for n, f in CLAUSULAS[e]:
            det[n] = sum(1 for s in seeds if (e, s) in C and (e, s) in Tr and bool(f(C[(e, s)], Tr[(e, s)])))
        for s in seeds:
            if (e, s) in C and (e, s) in Tr and all(bool(f(C[(e, s)], Tr[(e, s)])) for _, f in CLAUSULAS[e]): todas += 1
        nom, fp = PESOS[e]
        out[e] = dict(todas=todas, n=len(seeds), detalle=det, pasa=bool(todas >= PUERTA_E),
                      pesos_reportados={nom: sum(1 for s in seeds if (e, s) in C and bool(fp(C[(e, s)])))},
                      veneno_total_med=(med([ven_total(C[(e, s)], 'B') for s in seeds if (e, s) in C]), med([ven_total(Tr[(e, s)], 'B') for s in seeds if (e, s) in Tr])))
    return out


def coste_examen(jc, jt):
    o = {}
    for q in ('celdas', 'splits', 'deaths'):
        c = med([r[q] for r in jc['corridas'] if r['etapa'] in SEIS]); t = med([r[q] for r in jt['corridas'] if r['etapa'] in SEIS])
        o[q] = dict(cand=c, tronco=t, razon=(None if not t else round(c / t, 3)), pasa=bool(t is not None and (c <= 1.25 * t if t > 0 else c <= 1.25)))
    return o


def sub(cmd, etq, cwd=None):
    log(f"   -> SUBPROCESO ({etq}): {' '.join(cmd[1:])}")
    t0 = time.time()
    p = subprocess.run([sys.executable] + cmd[1:], capture_output=True, text=True, cwd=cwd or AQUI, encoding='utf-8', errors='replace')
    cola = [l for l in (p.stdout or '').strip().splitlines()[-14:]]
    for l in cola: log(f"      | {l}")
    if p.returncode != 0:
        log(f"      *** codigo {p.returncode}; stderr: {(p.stderr or '')[-600:]}")
    log(f"      ({time.time()-t0:.0f}s)")
    return dict(etq=etq, cmd=cmd[1:], returncode=p.returncode, cola=cola, t0=t0)


def json_nuevo(patron, t0):
    cands = [f for f in glob.glob(os.path.join(DATOS, patron)) if os.path.getmtime(f) >= t0 - 1]
    if not cands: return None, None
    f = max(cands, key=os.path.getmtime)
    return f, json.load(open(f, encoding='utf-8'))


def json_tronco_121():
    """Un examen de v14.1 ya corrido en 121-140 (sha del tronco, 20 semillas), si existe."""
    for f in sorted(glob.glob(os.path.join(DATOS, 'examen_v14_*.json')), key=os.path.getmtime, reverse=True):
        try:
            j = json.load(open(f, encoding='utf-8')); m = j['meta']
            if m.get('sha_organismo_v13') == SHA_TRONCO and m.get('semilla_inicial') == 121 and m.get('semillas') == 20: return f, j
        except Exception: pass
    return None, None


CRUDO = {}


def crudo(etq, res, extra=None):
    """ERR-54: los datos crudos se guardan ANTES del analisis; si el analisis revienta, la corrida no se pierde."""
    CRUDO[etq] = res
    f = os.path.join(DATOS, f"{_log['nom']}_crudo_{etq}.json")
    json.dump(dict(meta=dict(etapa=etq, fecha=time.strftime('%Y-%m-%dT%H:%M:%S'), n=len(res), extra=extra), corridas=res),
              open(f, 'w', encoding='utf-8'), ensure_ascii=False, default=str)
    log(f"   CRUDO ({len(res)} corridas) -> {os.path.basename(f)}  sha256_16 = {h16(f)}")
    return res


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
            if i % 18 == 0 or i == len(tareas): log(f"          {etq} {i}/{len(tareas)}")
    return res


# ------------------------------------------------------------------ T-A y T-G: veredictos (la letra de CRITERIO_TRONCO_v2.md)
def veredicto_vivo(res):
    """T-A por brazo: el 'tronco' es el MISMO brazo con la perilla apagada (relevo OFF == organismo_vivo_rep2 == v14.1 en el mundo vivo)."""
    V = {}
    for brazo in BRAZOS_TA:
        G = lambda arm: sorted([r for r in res if r['brazo'] == brazo and r['arm'] == arm], key=lambda r: r['seed'])
        off = G('OFF')
        if not off: continue
        V[brazo] = {}
        for arm in ARMS_TA:
            if arm == 'OFF': continue
            on = G(arm)
            mu_on, mu_off = med([r['deaths'] for r in on]), med([r['deaths'] for r in off])
            r_on, r_off = med([r['r'] for r in on]), med([r['r'] for r in off])
            a_r = a12([r['r'] for r in on], [r['r'] for r in off])
            a_mu = a12([-r['deaths'] for r in on], [-r['deaths'] for r in off])   # A12 de "muere MENOS" (pareado)
            V[brazo][arm] = dict(
                n=len(on), muertes_on=mu_on, muertes_off=mu_off,
                razon_muertes=(None if not mu_off else round(mu_on / mu_off, 3)),
                r_on=r_on, r_off=r_off, r_delta=(None if r_on is None or r_off is None else round(r_on - r_off, 1)),
                A12_r=a_r, A12_menos_muertes=a_mu,
                celdas_on=med([r['celdas'] for r in on]), celdas_off=med([r['celdas'] for r in off]),
                splits_on=med([r['splits'] for r in on]), splits_off=med([r['splits'] for r in off]),
                descendientes_on=med([r['descendientes'] for r in on]), descendientes_off=med([r['descendientes'] for r in off]),
                pasa=bool(mu_on is not None and mu_off is not None and r_on is not None and r_off is not None and a_r is not None
                          and (mu_on <= UMB_TA['muertes'] * mu_off if mu_off > 0 else mu_on <= UMB_TA['muertes'])
                          and r_on >= r_off - UMB_TA['r_delta'] and a_r >= UMB_TA['a12']))
        V[brazo]['pasa'] = bool(all(V[brazo][a]['pasa'] for a in V[brazo] if a in ARMS_TA))
    V['pasa'] = bool(V and all(V[b]['pasa'] for b in BRAZOS_TA if b in V) and all(b in V for b in BRAZOS_TA))
    return V


def veredicto_xor(res):
    """T-G: capacidad nueva. xor01 ESTRICTA (la abstencion NO puntua) con 8 ejemplos, ON contra OFF pareado."""
    G = lambda rg, mem: sorted([r for r in res if r['regla'] == rg and r['memoria'] == mem], key=lambda r: r['seed'])
    x_on = med([r['acc_estricta'] for r in G('xor01', 'relevo')]); x_off = med([r['acc_estricta'] for r in G('xor01', None)])
    p_on = med([r['acc'] for r in G('px0', 'relevo')]); p_off = med([r['acc'] for r in G('px0', None)])
    az = med([r['acc'] for r in G('azar', 'relevo')])
    par_x = sum(1 for a, b in zip(G('xor01', 'relevo'), G('xor01', None)) if a['acc_estricta'] > b['acc_estricta'])
    par_px = sum(1 for a, b in zip(G('px0', 'relevo'), G('px0', None)) if a['acc'] >= b['acc'])
    gana01 = sum(1 for r in G('xor01', 'relevo') if r['ganadora'] == [0, 1])
    lo, hi = UMB_TG['azar']
    return dict(umbral=UMB_TG['frase'], n=len(G('xor01', 'relevo')),
                xor01_estricta_on=x_on, xor01_estricta_off=x_off,
                pareado_xor_on_mayor=par_x, ganadora_0_1=gana01,
                px0_on=p_on, px0_off=p_off, px0_pareado_on_ge_off=par_px, azar=az,
                pasa=bool(x_on is not None and x_on >= UMB_TG['xor'] and az is not None and lo <= az <= hi
                          and p_on is not None and p_off is not None and p_on >= p_off - 1e-9))


def veredicto_sal(res):
    """C1, C2, C6 de B-5 por brazo (OFF, v15f, v15g). Los umbrales se IMPORTAN de creacion_B/corre_codigo.UMBRALES
    (la letra de B-5), no se copian: si B-5 cambia su letra, esto se entera."""
    import corre_codigo as CC
    u1, u2, u6 = CC.UMBRALES['C1'], CC.UMBRALES['C2'], CC.UMBRALES['C6']
    V = {'letra': {k: CC.UMBRALES[k]['frase'] for k in ('C1', 'C2', 'C6')}}
    for arm in ARMS:
        A = [r for r in res if r['arm'] == arm and r['brazo'] == 'S1-ALIAS']; L = [r for r in res if r['arm'] == arm and r['brazo'] == 'S1-LIMPIA']
        c1 = sum(r['w_sal'] <= u1['w'] for r in A); c2a = sum(r['w_veneno'] <= u2['w1'] for r in A); c2b = sum(r['w_veneno'] <= u2['w2'] for r in A)
        c6a = sum(r['w_sal'] <= u6['w'] for r in L); c6b = sum(r['w_veneno'] <= u6['wv'] for r in L)
        V[arm] = dict(C1=dict(n=c1, med=med([r['w_sal'] for r in A]), pasa=bool(c1 >= u1['n_min'] and (med([r['w_sal'] for r in A]) or 0) <= u1['med_max'])),
                      C2=dict(n28=c2a, n25=c2b, med=med([r['w_veneno'] for r in A]), pasa=bool(c2a >= u2['n1'] and c2b == len(A) and len(A) == u2['n2'])),
                      C6=dict(sal=c6a, veneno=c6b, pasa=bool(c6a == u6['n_min'] and c6b == u6['n_min'])),
                      exp_sal=med([r['exp_sal'] for r in A]), muertes_alias=med([r['deaths'] for r in A]), muertes_limpias=med([r['deaths'] for r in L]))
        V[arm]['pasa'] = bool(V[arm]['C1']['pasa'] and V[arm]['C2']['pasa'] and V[arm]['C6']['pasa'])
    return V


def nada(motivo):
    return dict(pasa=False, medido=False, nota=motivo)


if __name__ == '__main__':
    stamp = time.strftime('%Y%m%d_%H%M%S')
    nom = f"v15f_v2_humo_{stamp}" if HUMO else f"v15f_v2_{stamp}"
    _log['nom'] = nom
    _log['f'] = open(os.path.join(DATOS, nom + '.log'), 'w', encoding='utf-8', newline='\n')
    pre = os.path.join(AQUI, 'PREREGISTRO_v15f_v2.md')
    log(f"ARRANQUE v15f bajo el CRITERIO v2 ({'HUMO, un proceso, sin Pool' if HUMO else 'serie'}).")
    log(f"sha preregistro {h16(pre) if os.path.exists(pre) else '(falta)'}  script {h16(os.path.abspath(__file__))}"
        f"  construye_vivo_relevo {h16(os.path.join(AQUI,'construye_vivo_relevo.py'))}  organismo_vivo_relevo {h16(os.path.join(AQUI,'organismo_vivo_relevo.py'))}"
        f"  identidad_vivo_relevo {h16(os.path.join(AQUI,'identidad_vivo_relevo.py'))}  bateria_v15f {h16(os.path.join(AQUI,'bateria_v15f.py'))}"
        f"  bateria_generaliza_v15f {h16(os.path.join(AQUI,'bateria_generaliza_v15f.py'))}  organismo_v15f_on {h16(os.path.join(AQUI,'organismo_v15f_on.py'))}"
        f"  ORIGEN organismo_vivo_rep2 {h16(os.path.join(VIVO,'organismo_vivo_rep2.py'))}  organismo_vivo {h16(os.path.join(VIVO,'organismo_vivo.py'))}"
        f"  organismo_v14 {h16(os.path.join(ORG,'organismo_v14.py'))}  bateria_v14 {h16(os.path.join(ORG,'bateria_v14.py'))}"
        f"  corre_sal {h16(os.path.join(VIVO,'corre_sal.py'))}  corre_vivo_rep2 {h16(os.path.join(VIVO,'corre_vivo_rep2.py'))}  mini_vivo {h16(os.path.join(VIVO,'mini_vivo.py'))}")
    V = {}
    if HUMO:
        # HUMO (regla del encargo): UN proceso, sin Pool, 3 semillas. (a) identidad; (b) 1 semilla ALIAS con relevo
        # ON/OFF (+ el brazo exploratorio v15g); (c) 1 semilla del mundo vivo ON/OFF; (d) 1 de reversion. Escribe JSON (ERR-42).
        log("ETAPA 1/4 — identidad (subproceso, T=20000): 28 identidades + 5 controles que deben fallar.")
        r1 = sub([sys.executable, os.path.join(AQUI, 'identidad_vivo_relevo.py'), '20000'], 'identidad')
        V['identidad'] = next((l for l in r1['cola'] if 'ARNES TOTAL' in l), None)
        V['identidad_ok'] = bool(r1['returncode'] == 0 and any('ARNES TOTAL: 33/33' in l for l in r1['cola']))
        log("ETAPA 2/4 — T-D humo: semilla ALIAS 326 (sal muda), apagada / v15f / v15g.")
        rs = [tarea_sal(('S1-ALIAS', 326, arm)) for arm in ARMS]
        for o in rs:
            log(f"   {o['arm']:5s} s326  |W[sal]| {o['w_sal']} {o['w_sal_por_nec']}  W[veneno] {o['w_veneno']} {o['w_veneno_por_nec']}  exp sal {o['exp_sal']} veneno {o['exp_veneno']}"
                f"  splits {o['splits']} celdas {o['celdas']} muertes {o['deaths']}  tabla {o['W_tabla']}")
        log("ETAPA 3/4 — T-A humo (una semilla, NO es la puerta): mundo vivo rep2, brazo VIVO, semilla 301, apagada / v15f / v15g: r = descendientes - muertes.")
        rv = [tarea_vivo(('VIVO', 301, arm)) for arm in ARMS]
        for o in rv:
            log(f"   {o['arm']:5s} s301  r {o['r']}  descendientes {o['descendientes']}  muertes {o['deaths']} {o.get('muertes_nec')}  exposiciones {o.get('exposiciones')}"
                f"  celdas {o['celdas']} splits {o['splits']}  tabla {o['W_tabla']}")
        log("ETAPA 4/4 — T-C (ii) humo: reversion en el mundo vivo (invertir_vivo_en=50000), semilla 321, apagada / v15f / v15g.")
        rr = [tarea_rev((321, arm)) for arm in ARMS]
        for o in rr:
            log(f"   {o['arm']:5s} s321  rev {o['rev']:+d}  mord A {o['mordA']}  mord B {o['mordB']}  muertes {o['deaths']}  W_nec {o['W_nec']}  tabla {o['W_tabla']}")
        dj = os.path.join(DATOS, nom + '.json')
        json.dump(dict(meta=dict(fecha=time.strftime('%Y-%m-%dT%H:%M:%S'), humo=True, semillas=[326, 301, 321], python=platform.python_version(), numpy=np.__version__,
                                 sha_preregistro=h16(pre) if os.path.exists(pre) else None, sha_script=h16(os.path.abspath(__file__)),
                                 sha_organismo_vivo_relevo=h16(os.path.join(AQUI, 'organismo_vivo_relevo.py')), identidad=V['identidad']),
                       identidad=r1, sal=rs, vivo=rv, reversion=rr), open(dj, 'w', encoding='utf-8'), ensure_ascii=False, default=str)
        log(f"datos -> {os.path.basename(dj)}  sha256_16 = {h16(dj)}")
        _log['f'].close(); sys.exit(0)

    try:
        ps = subprocess.run(['powershell', '-NoProfile', '-Command',
                             "Get-CimInstance Win32_Process | Where-Object { $_.Name -like 'python*' } | ForEach-Object { \"$($_.ProcessId) $($_.CommandLine)\" }"],
                            capture_output=True, text=True, timeout=60).stdout.strip().splitlines()
    except Exception as e:
        ps = [f"(no se pudo listar: {e})"]
    log(f"REGLA 11 — procesos python vivos ({len(ps)}), este es pid {os.getpid()}")
    import corre_sal as CS
    for k in ('T-B', 'T-C_i', 'T-E', 'T-F_examen', 'T-D', 'T-C_ii', 'T-A', 'T-G'):
        V[k] = nada('etapa no corrida (--solo)')
    r2 = r3 = r4 = None
    res_sal = res_rev = res_vivo = res_xor = []
    VS = {}; VRev = {}

    # ---------------------------------------------------------------- ETAPA 1: identidad (siempre)
    log("ETAPA 1/9 — identidad (subproceso, un proceso): 28 identidades + 5 controles que DEBEN fallar.")
    r1 = sub([sys.executable, os.path.join(AQUI, 'identidad_vivo_relevo.py'), '20000'], 'identidad')
    if r1['returncode'] != 0 or not any('ARNES TOTAL: 33/33' in l for l in r1['cola']):
        log("*** el arnes no es 33/33 (28 identidades + 5 controles que fallan); se para."); _log['f'].close(); sys.exit(1)
    V['identidad'] = '33/33 (28 identidades + 5 controles que deben fallar)'

    # ---------------------------------------------------------------- ETAPA 2: T-B
    if hacer('TB'):
        log("ETAPA 2/9 — T-B generalizacion del candidato (121-140; subproceso con su Pool).")
        r2 = sub([sys.executable, os.path.join(AQUI, 'bateria_generaliza_v15f.py'), 'organismo_v15f_on', '20', '--desde', '121', '--log'], 'T-B')
        fB, jB = json_nuevo('regresion_generaliza_v15f_organismo_v15f_on_*.json', r2['t0'])
        if jB is None:
            V['T-B'] = dict(pasa=False, medido=False, nota='sin JSON (ERR-43: el veredicto se lee del JSON, no del log)')
        else:
            C = jB['corridas']; S = jB['meta']['semillas']
            px = {r['seed']: r for r in C if r['regla'] == 'px0'}; az = {r['seed']: r for r in C if r['regla'] == 'azar'}
            g1 = med([px[s]['acc'] for s in S]); g1az = med([az[s]['acc'] for s in S]); g2 = med([px[s]['ba'] for s in S]); g2az = med([az[s]['ba'] for s in S])
            kc = sum(px[s]['cobertura'] >= 6 for s in S)
            V['T-B'] = dict(medido=True, json=os.path.basename(fB), G1=g1, G1_azar=g1az, G2=g2, G2_azar=g2az, K=kc, bateria=jB['meta']['veredictos'],
                            pasa=bool(g1 >= 0.80 and g2 is not None and g2 >= 0.85 and 0.35 <= g1az <= 0.65 and g2az is not None and 0.42 <= g2az <= 0.58 and kc == len(S)))
        log(f"   T-B {V['T-B']}")

    # ---------------------------------------------------------------- ETAPAS 3 y 4: examen del candidato y del tronco -> T-C (i), T-E, T-F
    if hacer('EX'):
        log("ETAPA 3/9 — examen v3' del candidato en 121-140 (subproceso con su Pool): T-C (i), T-E, T-F.")
        r3 = sub([sys.executable, os.path.join(AQUI, 'bateria_v15f.py'), '20', '--desde', '121', '--log'], 'examen candidato')
        fC, jC = json_nuevo('examen_v15f_*.json', r3['t0'])
        log("ETAPA 4/9 — examen v3' del tronco en 121-140: JSON existente o subproceso.")
        fT, jT = json_tronco_121()
        if jT is None:
            r4 = sub([sys.executable, os.path.join(ORG, 'bateria_v14.py'), '20', '--desde', '121', '--log'], 'examen tronco', cwd=ORG)
            fT, jT = json_nuevo('examen_v14_*.json', r4['t0'])
        else:
            log(f"   tronco: se lee {os.path.basename(fT)} (v14.1 en 121-140, ya corrido)")
        if jC is None or jT is None:
            for k in ('T-C_i', 'T-E', 'T-F_examen'):
                V[k] = dict(pasa=False, medido=False, nota='sin JSON del examen')
        else:
            con = conducta(jC, jT); cost = coste_examen(jC, jT)
            V['examen_json'] = dict(candidato=os.path.basename(fC), tronco=os.path.basename(fT), veredicto_v1_candidato=jC['meta']['veredictos'])
            V['T-C_i'] = dict(medido=True, comeB_Q4=con['E2']['detalle']['come B Q4 >= 50 (T-C i)'],
                              pasa=bool(con['E2']['detalle']['come B Q4 >= 50 (T-C i)'] >= PUERTA_E))
            V['T-E'] = dict(medido=True, escenarios=con, pasa=bool(all(con[e]['pasa'] for e in SEIS)))
            V['T-F_examen'] = dict(medido=True, coste=cost, pasa=bool(all(cost[q]['pasa'] for q in cost)))
            for e in SEIS:
                log(f"   T-E {e:4s} {con[e]['todas']}/{con[e]['n']} {'PASA' if con[e]['pasa'] else 'NO'}  {con[e]['detalle']}  pesos {con[e]['pesos_reportados']}  veneno total med cand/tronco {con[e]['veneno_total_med']}")
            log(f"   T-C (i) come B Q4 >= 50: {V['T-C_i']}")
            log(f"   T-F examen: {cost}")

    # ---------------------------------------------------------------- ETAPA 5: T-D bloque de la sal
    if hacer('TD'):
        log("ETAPA 5/9 — T-D bloque de la sal con organismo_vivo_relevo: 9 ALIAS + 9 LIMPIAS x {OFF, v15f, v15g} (Pool aqui).")
        tareas = [(b, s, arm) for b, seeds in (('S1-ALIAS', CS.ALIAS), ('S1-LIMPIA', CS.LIMPIAS)) for s in seeds for arm in ARMS]
        res_sal = crudo('TD', pool_map(tarea_sal, tareas, 'T-D'))
        VS = veredicto_sal(res_sal); V['T-D'] = dict(VS, medido=True, pasa=VS['v15f']['pasa'])
        log(f"   T-D letra (importada de creacion_B/corre_codigo.UMBRALES): {VS['letra']}")
        for arm in ARMS:
            log(f"   T-D {arm:5s} C1 {VS[arm]['C1']}  C2 {VS[arm]['C2']}  C6 {VS[arm]['C6']}  exp sal {VS[arm]['exp_sal']}  muertes alias/limpias {VS[arm]['muertes_alias']}/{VS[arm]['muertes_limpias']}  -> {'PASA' if VS[arm]['pasa'] else 'NO'}")

    # ---------------------------------------------------------------- ETAPA 6: T-C (ii) reversion en el mundo vivo
    if hacer('TC'):
        log("ETAPA 6/9 — T-C (ii) reversion en el mundo vivo (invertir_vivo_en=50000), semillas 321-340 x {OFF, v15f, v15g} (Pool aqui).")
        res_rev = crudo('TCii', pool_map(tarea_rev, [(s, arm) for s in SEEDS_REV for arm in ARMS], 'T-C ii'))
        G = lambda arm: sorted([r for r in res_rev if r['arm'] == arm], key=lambda r: r['seed'])
        for arm in ('v15f', 'v15g'):
            a = a12([r['rev'] for r in G(arm)], [r['rev'] for r in G('OFF')])
            VRev[arm] = dict(A12_rev=a, rev_med=med([r['rev'] for r in G(arm)]), rev_med_off=med([r['rev'] for r in G('OFF')]),
                             comeB_Q4_med=med([r['mordB'][3] for r in G(arm)]), muerdeA_Q4_med=med([r['mordA'][3] for r in G(arm)]),
                             muertes_med=med([r['deaths'] for r in G(arm)]), muertes_off=med([r['deaths'] for r in G('OFF')]),
                             pasa=bool(a is not None and a >= 0.75))
            log(f"   T-C (ii) {arm:5s} A12(rev ON > OFF) {a}  rev med {VRev[arm]['rev_med']} (OFF {VRev[arm]['rev_med_off']})  come B Q4 {VRev[arm]['comeB_Q4_med']}  muerde A Q4 {VRev[arm]['muerdeA_Q4_med']}  muertes {VRev[arm]['muertes_med']}/{VRev[arm]['muertes_off']}  -> {'PASA' if VRev[arm]['pasa'] else 'NO'}")
        V['T-C_ii'] = dict(VRev, medido=True, pasa=VRev['v15f']['pasa'])

    # ---------------------------------------------------------------- ETAPA 7: T-A supervivencia y r en el mundo vivo
    if hacer('TA'):
        log(f"ETAPA 7/9 — T-A supervivencia en el mundo vivo (rep2, T={T}, costo=0.001), brazos {list(BRAZOS_TA)} x {list(ARMS_TA)}, semillas {SEEDS_TA[0]}-{SEEDS_TA[-1]} (Pool aqui).")
        log(f"   letra: {UMB_TA['frase']}  (el 'tronco' de cada brazo es ese mismo brazo con la perilla APAGADA = organismo_vivo_rep2 bit a bit)")
        res_vivo = crudo('TA', pool_map(tarea_vivo, [(b, s, arm) for b in BRAZOS_TA for s in SEEDS_TA for arm in ARMS_TA], 'T-A'),
                         extra=dict(brazos=list(BRAZOS_TA), arms=list(ARMS_TA), semillas=SEEDS_TA, T=T))
        VA = veredicto_vivo(res_vivo); V['T-A'] = dict(VA, medido=True)
        for b in BRAZOS_TA:
            for arm in ARMS_TA:
                if arm == 'OFF' or b not in VA or arm not in VA[b]: continue
                d = VA[b][arm]
                log(f"   T-A {b:10s} {arm:5s} muertes {d['muertes_on']} vs tronco {d['muertes_off']} (razon {d['razon_muertes']} <= {UMB_TA['muertes']})  "
                    f"r {d['r_on']} vs {d['r_off']} (delta {d['r_delta']} >= -{UMB_TA['r_delta']})  A12(r) {d['A12_r']} >= {UMB_TA['a12']}  "
                    f"A12(menos muertes) {d['A12_menos_muertes']}  desc {d['descendientes_on']}/{d['descendientes_off']}  celdas {d['celdas_on']}/{d['celdas_off']}  "
                    f"splits {d['splits_on']}/{d['splits_off']}  -> {'PASA' if d['pasa'] else 'NO'}")
        log(f"   T-A -> {'PASA' if VA['pasa'] else 'NO'}")

    # ---------------------------------------------------------------- ETAPA 8: T-G capacidad nueva (xor01 con 8 ejemplos)
    if hacer('TG'):
        import corre_v15f as C15
        log(f"ETAPA 8/9 — T-G capacidad nueva: mundo de REGLA (T=200000) con los kwargs del tronco, reglas {C15.REGLAS}, "
            f"semillas {SEEDS_TG[0]}-{SEEDS_TG[-1]}, ON/OFF pareado (Pool aqui).")
        log(f"   letra: {UMB_TG['frase']}   kwargs del tronco (importados de corre_v15f.KW14, ERR-41): {C15.KW14}")
        tareas = [(rg, s, mem, 'organismo_v15gf') for rg in C15.REGLAS for s in SEEDS_TG for mem in ('relevo', None)]
        res_xor = crudo('TG', pool_map(tarea_xor, tareas, 'T-G'), extra=dict(kw14=C15.KW14, reglas=C15.REGLAS, semillas=SEEDS_TG, modulo='organismo_v15gf'))
        VG = veredicto_xor(res_xor); V['T-G'] = dict(VG, medido=True)
        log(f"   T-G xor01 ESTRICTA ON {f3(VG['xor01_estricta_on'])} (OFF {f3(VG['xor01_estricta_off'])}; pareado ON>OFF {VG['pareado_xor_on_mayor']}/{VG['n']}; "
            f"gana(0,1) {VG['ganadora_0_1']}/{VG['n']})  px0 ON {f3(VG['px0_on'])} / OFF {f3(VG['px0_off'])} (pareado {VG['px0_pareado_on_ge_off']}/{VG['n']})  "
            f"azar {f3(VG['azar'])}  -> {'PASA' if VG['pasa'] else 'NO'}")

    # ---------------------------------------------------------------- ETAPA 9: veredicto de las SIETE puertas
    log("ETAPA 9/9 — veredicto de las siete puertas del CRITERIO DE TRONCO v2.")
    puertas = {'T-A': V['T-A']['pasa'], 'T-B': V['T-B']['pasa'], 'T-C': bool(V['T-C_i']['pasa'] and V['T-C_ii']['pasa']),
               'T-D': V['T-D']['pasa'], 'T-E': V['T-E']['pasa'], 'T-F': V['T-F_examen']['pasa'], 'T-G': V['T-G']['pasa']}
    medido = {k: bool(v.get('medido')) for k, v in (('T-A', V['T-A']), ('T-B', V['T-B']), ('T-C', V['T-C_i']), ('T-D', V['T-D']),
                                                    ('T-E', V['T-E']), ('T-F', V['T-F_examen']), ('T-G', V['T-G']))}
    V['puertas_v15f'] = puertas; V['puertas_medidas'] = medido
    for k in ('T-A', 'T-B', 'T-C', 'T-D', 'T-E', 'T-F', 'T-G'):
        log(f"   {k}: {'PASA' if puertas[k] else 'NO'}{'' if medido[k] else '  (NO MEDIDA en esta corrida)'}")
    if VS:
        log(f"   Brazo exploratorio v15g (NO candidato): T-D {'PASA' if VS['v15g']['pasa'] else 'NO'}"
            + (f", T-C(ii) {'PASA' if VRev['v15g']['pasa'] else 'NO'}" if VRev else ""))
    todas = all(medido.values())
    if not todas:
        log("VEREDICTO: INCOMPLETO — faltan puertas por medir: " + ', '.join(k for k in medido if not medido[k]))
    elif all(puertas.values()):
        log("VEREDICTO: v15f cruza las SIETE puertas del criterio v2 en semillas nuevas -> candidato a tronco; falta la REPLICA en semillas nuevas antes de congelar (regla 2 de v2). La decision es del director.")
    else:
        log("VEREDICTO: v15f NO ENTRA — cae " + ', '.join(k for k in puertas if not puertas[k]) + ". Una sola puerta caida basta (regla 2 de v2), sin modos intermedios.")
    meta = dict(fecha=time.strftime('%Y-%m-%dT%H:%M:%S'),
                semillas=dict(examen=SEEDS_EX, reversion=SEEDS_REV, alias=CS.ALIAS, limpias=CS.LIMPIAS, vivo=SEEDS_TA, regla=SEEDS_TG),
                umbrales=dict(T_A=UMB_TA['frase'], T_G=UMB_TG['frase']), veredictos=V, solo=SOLO,
                etapas=[r1, r2, r3, r4], procesos_python=ps, sha_preregistro=h16(pre) if os.path.exists(pre) else None, sha_script=h16(os.path.abspath(__file__)),
                sha_organismo_vivo_relevo=h16(os.path.join(AQUI, 'organismo_vivo_relevo.py')),
                sha_identidad_vivo_relevo=h16(os.path.join(AQUI, 'identidad_vivo_relevo.py')),
                sha_construye_vivo_relevo=h16(os.path.join(AQUI, 'construye_vivo_relevo.py')),
                python=platform.python_version(), numpy=np.__version__)
    dj = os.path.join(DATOS, nom + '.json')
    json.dump(dict(meta=meta, sal=res_sal, reversion=res_rev, vivo=res_vivo, regla=res_xor), open(dj, 'w', encoding='utf-8'), ensure_ascii=False, default=str)
    log(f"datos -> {os.path.basename(dj)}  sha256_16 = {h16(dj)}")
    _log['f'].close()
