"""dE5 bajo el CRITERIO DE TRONCO v2 (registro/CRITERIO_TRONCO_v2.md). Ejecuta PREREGISTRO_dE5_v2.md.
dE5 = TRONCO v14.2 + la SORPRESA DEL MUNDO (error del predictor de dE) en la BOCA a dosis k_sorp = 5.

REGLA 10: log desde el arranque, con fsync. REGLA 11: un Pool a la vez (los subprocesos son SECUENCIALES; el Pool
propio solo en T-D, T-C ii, T-A y T-G). ERR-43: los veredictos de las baterias se LEEN de su JSON, no del log.
ERR-54: los datos CRUDOS de cada etapa con Pool se vuelcan a datos/ ANTES de analizarlos. ERR-86: el tamano del Pool
lo fija JUACO_POOL. ERR-87: el JSON de un subproceso se localiza por PREFIJO + SELLO EXACTO leido de su salida, no
por "el ultimo del prefijo". ERR-89: UNA LINEA IMPRESA POR PUERTA, siempre, con su umbral al lado.
Reutiliza POR IMPORT (sin copiar): corre_vivo_rep2 (BRAZOS, resumen2), corre_sal (BASE, ALIAS, LIMPIAS, resumen),
mini_vivo (BRAZOS) y creacion_B/corre_codigo (UMBRALES C1/C2/C6 de B-5).

  ETAPA 1  identidad (`identidad_v15_dE5.py`, subproceso, un proceso): 61 identidades + 7 controles que DEBEN fallar
           = 68/68, o se para sin veredicto.
  ETAPA 2  T-B  generalizacion: `bateria_generaliza_v15_dE5.py organismo_v15_dE5_on 20 --desde 2001 --log`.
  ETAPA 3  examen v3' del CANDIDATO en 2001-2020: `bateria_v15_dE5.py 20 --desde 2001 --log` -> T-C (i), T-E, T-F.
  ETAPA 4  examen v3' del TRONCO v14.2 en 2001-2020: JSON existente (sha 17528d767fcebaf6) o `bateria_v142.py`.
  ETAPA 5  T-D  bloque de la sal: 9 ALIAS + 9 LIMPIAS x {OFF, dE5} (Pool aqui).
  ETAPA 6  T-C (ii) reversion en el mundo vivo (invertir_vivo_en=50000), 2041-2060 x {OFF, dE5} (Pool aqui).
  ETAPA 7  T-A  mundo vivo de rep2, brazos VIVO y CUELLO_MIN, 2021-2040 x {OFF, dE5} (Pool aqui).
  ETAPA 8  T-G  capacidad nueva: RECUPERACION tras el cambio no avisado (T=200000, invertir_en=100000), 2061-2080,
           brazos OFF / dE5 / CONST (control de CANTIDAD) / dE10 (referencia) (Pool aqui).
  ETAPA 9  veredicto de las SIETE puertas y JSON.

Uso:  python experimentos/tronco_v15_dE5/corre_dE5_v2.py
      python experimentos/tronco_v15_dE5/corre_dE5_v2.py --humo          (UN proceso, sin Pool; escribe su JSON)
      python experimentos/tronco_v15_dE5/corre_dE5_v2.py --solo TA,TG    (subconjunto; el resto se salta)
      JUACO_POOL=14 python experimentos/tronco_v15_dE5/corre_dE5_v2.py   (tamano del Pool, ERR-86)
"""
import sys, os, json, time, hashlib, platform, subprocess, glob, re
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
import numpy as np

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
ORG = os.path.join(RAIZ, 'organismo')
VIVO = os.path.join(RAIZ, 'experimentos', 'nivel11_mundo_vivo')
CREB = os.path.join(RAIZ, 'experimentos', 'creacion_B')
DATOS = os.path.join(RAIZ, 'datos')
DATOS_HUMO = os.path.join(DATOS, 'humo')   # convencion 21-sep: los humos de runners nuevos van a datos/humo/
sys.path[:0] = [ORG, VIVO, CREB, AQUI]   # organismo/ PRIMERO (ERR-28)

HUMO = '--humo' in sys.argv
SOLO = (sys.argv[sys.argv.index('--solo') + 1].split(',') if '--solo' in sys.argv else None)

T = 100000
T_TG = 200000
T_INV = T_TG // 2
SEEDS_EX = list(range(2001, 2021))    # T-B, T-C (i), T-E, T-F examen
SEEDS_TA = list(range(2021, 2041))    # T-A
SEEDS_REV = list(range(2041, 2061))   # T-C (ii)
SEEDS_TG = list(range(2061, 2081))    # T-G
BRAZOS_TA = ('VIVO', 'CUELLO_MIN')
SHA_TRONCO = '17528d767fcebaf6'       # organismo/organismo_v142.py (TRONCO v14.2)
ARNES_ESPERADO = 'ARNES TOTAL: 68/68'
N_PARALELO = int(os.environ.get('JUACO_POOL', 14))   # ERR-86

# --- los brazos. La dosis preregistrada y el control de CANTIDAD (PREREGISTRO_dE5_v2.md §2 y §6)
DOSIS = dict(eta_pred=0.03, ema_pred=0.05, clip_e=3.0, k_sorp=5.0)
APAGADO = dict(eta_pred=0.0, ema_pred=0.05, clip_e=3.0, k_sorp=0.0)
# C = el empujon medio que dE5 aplica en la boca tras el cambio no avisado. FIJADO EN EL HUMO (semilla 2061,
# datos/humo/dE5_v2_humo_20260921_145417.json): media de sesgo_q[Q3,Q4] = (0.114829 + 0.000238)/2 = 0.058.
# Es el unico numero que el humo fija (PREREGISTRO_dE5_v2.md §6 y §10). Se puede sobreescribir con JUACO_CONST.
C_CONST = float(os.environ.get('JUACO_CONST', '0.058'))
ARMS = {'OFF': dict(APAGADO), 'dE5': dict(DOSIS)}
ARMS_TG = {'OFF': dict(APAGADO), 'dE5': dict(DOSIS), 'dE10': dict(DOSIS, k_sorp=10.0),
           'CONST': dict(APAGADO, eta_pred=0.03, sesgo_fijo=C_CONST)}

# --- umbrales, COPIADOS de CRITERIO_TRONCO_v2.md y de PREREGISTRO_dosis_dE.md (ninguno inventado aqui)
UMB = {
    'T-A': dict(frase="muertes <= 1.10 x tronco (mediana); r = descendientes - muertes >= tronco - 10; A12(r) >= 0.50 pareado",
                muertes=1.10, r_delta=10.0, a12=0.50),
    'T-B': dict(frase="G1 >= 0.80, G2 >= 0.85, azar en [0.35,0.65] (G2 azar en [0.42,0.58]), K 20/20",
                g1=0.80, g2=0.85, azar=(0.35, 0.65), azar2=(0.42, 0.58)),
    'T-C': dict(frase="(i) come B Q4 >= 50 en >= 18/20;  (ii) A12(rev ON > OFF) >= 0.75", n=18, a12=0.75),
    'T-D': dict(frase="C1, C2, C6 de B-5 (umbrales IMPORTADOS de creacion_B/corre_codigo.UMBRALES)"),
    'T-E': dict(frase="conducta por escenario >= 18/20, pareada con el TRONCO v14.2 (tolerancias 1.10 / 0.8)", n=18),
    'T-F': dict(frase="celdas, divisiones y muertes <= 1.25 x tronco (medianas de las seis etapas) + T-A", factor=1.25),
    'T-G': dict(frase="recuperacion mediana <= 0.60 x OFF; pareado >= 16/20; se apaga sola (P4') >= 16/20; "
                      "CONST no recupera como dE5 (pareado >= 15/20); veneno tras el cambio <= 1.10 x OFF",
                razon=0.60, par=16, apaga=16, par_const=15, veneno=1.10),
}
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
    import corre_sal as CS, organismo_v15_dE5 as D5
    kw = dict(CS.BRAZOS[brazo][0])
    r = D5.run(seed, T=T, **kw, **ARMS[arm])
    o = CS.resumen(brazo, seed, r); o.update(arm=arm, sbarE=r.get('sbarE'), sesgo_q=r.get('sesgo_q'), des_splits=r.get('des_splits'))
    return o


def tarea_rev(args):
    seed, arm = args
    import mini_vivo as MV, organismo_v15_dE5 as D5
    kw = dict(MV.BRAZOS['VIVO'], invertir_vivo_en=T // 2)
    r = D5.run(seed, T=T, **kw, **ARMS[arm])
    return dict(seed=seed, arm=arm, mordA=r['mord']['A'], mordB=r['mord']['B'],
                rev=r['mord']['B'][3] - r['mord']['A'][3], deaths=r['deaths'], muertes_nec=r['muertes_nec'],
                W_nec=r['W_nec'], celdas=r['celdas'], splits=r['splits'], sesgo_q=r.get('sesgo_q'))


def tarea_vivo(args):
    brazo, seed, arm = args
    import corre_vivo_rep2 as CR2, organismo_v15_dE5 as D5
    kw = CR2.BRAZOS[brazo]
    r = D5.run(seed, T=T, **kw, **ARMS[arm])
    o = CR2.resumen2(brazo, seed, r, kw, T); o.update(arm=arm, sesgo_q=r.get('sesgo_q'), des_splits=r.get('des_splits'))
    return o


def tarea_tg(args):
    """T-G: RECUPERACION tras el cambio no avisado, en el mundo AB del tronco (vivo=0, n_nec=1)."""
    seed, arm = args
    import organismo_v15_dE5 as D5
    r = D5.run(seed, T=T_TG, invertir_en=T_INV, **ARMS_TG[arm])
    te = r['t_ext_B']
    return dict(seed=seed, arm=arm, t_ext_B=te, recup=((T_TG - T_INV) if te is None else te - T_INV),
                censurado=te is None, mord_post=r['mord_post'], deaths=r['deaths'], deaths_post=r['deaths_post'],
                W=r['W'], W_lenta=r['W_lenta'], sesgo_q=r['sesgo_q'], enc_q=r['enc_q'], sbarE=r['sbarE'],
                mord=r['mord'], splits=r['splits'], celdas=r['celdas'])


# ------------------------------------------------------------------ examen: CONDUCTA por escenario (T-E, T-C i) y coste (T-F)
def ven_total(r, k): return sum(r['mord'][k])
def tasa(r, k, i): return 100 * r['mord'][k][i] / max(r['vis'][k][i], 1)
CLAUSULAS = {   # la letra de PREREGISTRO_dE5_v2.md §5 (copiada de PREREGISTRO_v15f_v2.md §4)
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
PESOS = {'E1': ('W_B≈-3', lambda r: abs(r['W']['B'] + 3) < .3),
         'E2': ('W_A→-3 y W_B→+1', lambda r: abs(r['W']['A'] + 3) < .3 and abs(r['W']['B'] - 1) < .15),
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
                      veneno_total_med=(med([ven_total(C[(e, s)], 'B') for s in seeds if (e, s) in C]),
                                        med([ven_total(Tr[(e, s)], 'B') for s in seeds if (e, s) in Tr])))
    return out


def coste_examen(jc, jt):
    o = {}
    for q in ('celdas', 'splits', 'deaths'):
        c = med([r[q] for r in jc['corridas'] if r['etapa'] in SEIS]); t = med([r[q] for r in jt['corridas'] if r['etapa'] in SEIS])
        o[q] = dict(cand=c, tronco=t, razon=(None if not t else round(c / t, 3)),
                    pasa=bool(t is not None and (c <= UMB['T-F']['factor'] * t if t > 0 else c <= UMB['T-F']['factor'])))
    return o


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
    return dict(etq=etq, cmd=cmd[1:], returncode=p.returncode, cola=salida.strip().splitlines()[-14:], stdout=salida, t0=t0)


def lee_json(prefijo, res):
    """ERR-87: el JSON se localiza por PREFIJO + SELLO EXACTO (AAAAMMDD_HHMMSS) leido de la salida del subproceso.
    Nunca 'el ultimo del prefijo'. Si el sello no aparece, NO se adivina: se devuelve (None, None) y la puerta
    queda NO MEDIDA."""
    m = re.findall(re.escape(prefijo) + r'_(\d{8}_\d{6})\.json', res.get('stdout', ''))
    if not m:
        log(f"      *** no aparece el sello de {prefijo}_*.json en la salida del subproceso: la puerta queda SIN MEDIR (ERR-87)")
        return None, None
    f = os.path.join(DATOS, f"{prefijo}_{m[-1]}.json")
    if not os.path.exists(f):
        log(f"      *** el sello {m[-1]} no existe en datos/: {os.path.basename(f)}")
        return None, None
    log(f"      JSON leido por prefijo+sello: {os.path.basename(f)}  sha256_16 = {h16(f)}")
    return f, json.load(open(f, encoding='utf-8'))


def json_tronco_examen():
    """Un examen del TRONCO v14.2 ya corrido en 2001-2020 (sha 17528d767fcebaf6, 20 semillas), si existe."""
    for f in sorted(glob.glob(os.path.join(DATOS, 'examen_v142_*.json')), key=os.path.getmtime, reverse=True):
        try:
            j = json.load(open(f, encoding='utf-8')); m = j['meta']
            if m.get('sha_organismo_v13') == SHA_TRONCO and m.get('semilla_inicial') == SEEDS_EX[0] and m.get('semillas') == len(SEEDS_EX):
                return f, j
        except Exception:
            pass
    return None, None


CRUDO = {}


def crudo(etq, res, extra=None):
    """ERR-54: los datos crudos se guardan ANTES del analisis."""
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


# ------------------------------------------------------------------ veredictos
def veredicto_vivo(res):
    """T-A por brazo: el 'tronco' es el MISMO brazo con la dosis APAGADA (= v14.2 en el mundo vivo)."""
    V = {}
    for brazo in BRAZOS_TA:
        G = lambda arm: sorted([r for r in res if r['brazo'] == brazo and r['arm'] == arm], key=lambda r: r['seed'])
        off, on = G('OFF'), G('dE5')
        if not off or not on:
            continue
        mu_on, mu_off = med([r['deaths'] for r in on]), med([r['deaths'] for r in off])
        r_on, r_off = med([r['r'] for r in on]), med([r['r'] for r in off])
        a_r = a12([r['r'] for r in on], [r['r'] for r in off])
        V[brazo] = dict(n=len(on), muertes_on=mu_on, muertes_off=mu_off,
                        razon_muertes=(None if not mu_off else round(mu_on / mu_off, 3)),
                        r_on=r_on, r_off=r_off, r_delta=(None if r_on is None or r_off is None else round(r_on - r_off, 1)),
                        A12_r=a_r, A12_menos_muertes=a12([-r['deaths'] for r in on], [-r['deaths'] for r in off]),
                        descendientes_on=med([r['descendientes'] for r in on]), descendientes_off=med([r['descendientes'] for r in off]),
                        celdas_on=med([r['celdas'] for r in on]), celdas_off=med([r['celdas'] for r in off]),
                        splits_on=med([r['splits'] for r in on]), splits_off=med([r['splits'] for r in off]),
                        pasa=bool(None not in (mu_on, mu_off, r_on, r_off, a_r)
                                  and (mu_on <= UMB['T-A']['muertes'] * mu_off if mu_off > 0 else mu_on <= UMB['T-A']['muertes'])
                                  and r_on >= r_off - UMB['T-A']['r_delta'] and a_r >= UMB['T-A']['a12']))
    V['pasa'] = bool(V and all(b in V for b in BRAZOS_TA) and all(V[b]['pasa'] for b in BRAZOS_TA))
    return V


def veredicto_sal(res):
    """C1, C2, C6 de B-5 por brazo. Los umbrales se IMPORTAN de creacion_B/corre_codigo.UMBRALES (no se copian)."""
    import corre_codigo as CC
    u1, u2, u6 = CC.UMBRALES['C1'], CC.UMBRALES['C2'], CC.UMBRALES['C6']
    V = {'letra': {k: CC.UMBRALES[k]['frase'] for k in ('C1', 'C2', 'C6')}}
    for arm in ARMS:
        A = [r for r in res if r['arm'] == arm and r['brazo'] == 'S1-ALIAS']
        L = [r for r in res if r['arm'] == arm and r['brazo'] == 'S1-LIMPIA']
        if not A or not L:
            continue
        c1 = sum(r['w_sal'] <= u1['w'] for r in A); c2a = sum(r['w_veneno'] <= u2['w1'] for r in A)
        c2b = sum(r['w_veneno'] <= u2['w2'] for r in A)
        c6a = sum(r['w_sal'] <= u6['w'] for r in L); c6b = sum(r['w_veneno'] <= u6['wv'] for r in L)
        V[arm] = dict(C1=dict(n=c1, med=med([r['w_sal'] for r in A]),
                              pasa=bool(c1 >= u1['n_min'] and (med([r['w_sal'] for r in A]) or 0) <= u1['med_max'])),
                      C2=dict(n28=c2a, n25=c2b, med=med([r['w_veneno'] for r in A]),
                              pasa=bool(c2a >= u2['n1'] and c2b == len(A) and len(A) == u2['n2'])),
                      C6=dict(sal=c6a, veneno=c6b, pasa=bool(c6a == u6['n_min'] and c6b == u6['n_min'])),
                      exp_sal=med([r['exp_sal'] for r in A]), des_splits=med([r['des_splits'] for r in A]),
                      muertes_alias=med([r['deaths'] for r in A]), muertes_limpias=med([r['deaths'] for r in L]))
        V[arm]['pasa'] = bool(V[arm]['C1']['pasa'] and V[arm]['C2']['pasa'] and V[arm]['C6']['pasa'])
    return V


def apaga_sola(sq):
    """P4' relativo sobre el sesgo de la boca por cuarto (la letra de PREREGISTRO_dosis_dE.md §6, condicion 3)."""
    if not sq or len(sq) < 4:
        return False
    q2, q3, q4 = sq[1], sq[2], sq[3]
    return bool(q2 <= 0.10 and q4 <= 0.10 and q2 <= 0.35 * q3 and q4 <= 0.35 * q3)


def veredicto_tg(res):
    G = lambda arm: sorted([r for r in res if r['arm'] == arm], key=lambda r: r['seed'])
    off, on, const, d10 = G('OFF'), G('dE5'), G('CONST'), G('dE10')
    m_on, m_off = med([r['recup'] for r in on]), med([r['recup'] for r in off])
    m_c = med([r['recup'] for r in const]); m_10 = med([r['recup'] for r in d10])
    par = sum(1 for a, b in zip(on, off) if a['recup'] < b['recup'])
    par_c = sum(1 for a, b in zip(on, const) if a['recup'] < b['recup']) if const else None
    ap = sum(1 for r in on if apaga_sola(r['sesgo_q']))
    ven_on = med([r['mord_post'].get('veneno', 0) for r in on]); ven_off = med([r['mord_post'].get('veneno', 0) for r in off])
    razon = (None if not m_off else round(m_on / m_off, 3))
    razon_c = (None if not m_off or m_c is None else round(m_c / m_off, 3))
    u = UMB['T-G']
    return dict(umbral=u['frase'], n=len(on), C_const=C_CONST,
                recup_on=m_on, recup_off=m_off, recup_CONST=m_c, recup_dE10=m_10,
                razon=razon, razon_CONST=razon_c, veces_mas_rapido=(None if not razon else round(1 / razon, 2)),
                pareado_on_menor=par, pareado_on_menor_que_CONST=par_c, apagado=ap,
                censurados_on=sum(r['censurado'] for r in on), censurados_off=sum(r['censurado'] for r in off),
                veneno_post_on=ven_on, veneno_post_off=ven_off,
                razon_veneno=(None if not ven_off else round(ven_on / ven_off, 3)),
                muertes_on=med([r['deaths'] for r in on]), muertes_off=med([r['deaths'] for r in off]),
                pasa=bool(razon is not None and razon <= u['razon'] and par >= u['par'] and ap >= u['apaga']
                          and par_c is not None and par_c >= u['par_const']
                          and ven_on is not None and ven_off is not None and (ven_on <= u['veneno'] * ven_off if ven_off > 0 else True)))


def nada(motivo):
    return dict(pasa=False, medido=False, nota=motivo)


if __name__ == '__main__':
    stamp = time.strftime('%Y%m%d_%H%M%S')
    nom = f"dE5_v2_humo_{stamp}" if HUMO else f"dE5_v2_{stamp}"
    _log['nom'] = nom
    SAL = DATOS_HUMO if HUMO else DATOS   # convencion 21-sep: los humos de runners nuevos van a datos/humo/
    os.makedirs(SAL, exist_ok=True)
    _log['f'] = open(os.path.join(SAL, nom + '.log'), 'w', encoding='utf-8', newline='\n')
    pre = os.path.join(AQUI, 'PREREGISTRO_dE5_v2.md')
    log(f"ARRANQUE dE5 bajo el CRITERIO DE TRONCO v2 ({'HUMO, un proceso, sin Pool' if HUMO else 'serie'}). JUACO_POOL={N_PARALELO}")
    log(f"sha preregistro {h16(pre) if os.path.exists(pre) else '(falta)'}  script {h16(os.path.abspath(__file__))}"
        f"  construye {h16(os.path.join(AQUI,'construye_v15_dE5.py'))}  identidad {h16(os.path.join(AQUI,'identidad_v15_dE5.py'))}"
        f"  organismo_v15_dE5 {h16(os.path.join(AQUI,'organismo_v15_dE5.py'))}  _on {h16(os.path.join(AQUI,'organismo_v15_dE5_on.py'))}"
        f"  g {h16(os.path.join(AQUI,'organismo_v15_dE5g.py'))}  g_on {h16(os.path.join(AQUI,'organismo_v15_dE5g_on.py'))}"
        f"  bateria_v15_dE5 {h16(os.path.join(AQUI,'bateria_v15_dE5.py'))}  bateria_generaliza_v15_dE5 {h16(os.path.join(AQUI,'bateria_generaliza_v15_dE5.py'))}"
        f"  ORIGEN organismo_vivo_rep2 {h16(os.path.join(VIVO,'organismo_vivo_rep2.py'))}  organismo_v142 {h16(os.path.join(ORG,'organismo_v142.py'))}"
        f"  organismo_v142g {h16(os.path.join(ORG,'organismo_v142g.py'))}  bateria_v142 {h16(os.path.join(ORG,'bateria_v142.py'))}"
        f"  bateria_generaliza_v142 {h16(os.path.join(ORG,'bateria_generaliza_v142.py'))}")
    log(f"dosis dE5 = {DOSIS};  control de CANTIDAD C = {C_CONST} (se fija en el humo, §7 del preregistro)")
    V = {}

    # ================================================================ HUMO: un proceso, sin Pool, <= 6 corridas
    if HUMO:
        log("HUMO 1/4 — identidad (subproceso, T=20000): 61 identidades + 7 controles que DEBEN fallar.")
        r1 = sub([sys.executable, os.path.join(AQUI, 'identidad_v15_dE5.py'), '20000'], 'identidad')
        V['identidad'] = next((l for l in r1['cola'] if 'ARNES TOTAL' in l), None)
        V['identidad_ok'] = bool(r1['returncode'] == 0 and any(ARNES_ESPERADO in l for l in r1['cola']))
        log(f"   {V['identidad']}   (esperado {ARNES_ESPERADO})")

        log(f"HUMO 2/4 — T-G: RECUPERACION, semilla {SEEDS_TG[0]}, T={T_TG}, invertir_en={T_INV}: OFF / dE5 (2 corridas).")
        rg = [tarea_tg((SEEDS_TG[0], arm)) for arm in ('OFF', 'dE5')]
        for o in rg:
            log(f"   {o['arm']:5s} s{o['seed']}  recup {o['recup']:6d} (t_ext_B {o['t_ext_B']}, censurado {o['censurado']})  "
                f"veneno tras el cambio {o['mord_post'].get('veneno')}  muertes {o['deaths']}/{o['deaths_post']}  "
                f"sesgo_q {o['sesgo_q']}  se apaga sola {apaga_sola(o['sesgo_q'])}  W {o['W']}")
        rec = {o['arm']: o['recup'] for o in rg}
        if rec['OFF']:
            log(f"   razon dE5/OFF en esta semilla = {rec['dE5']/rec['OFF']:.3f}  ({rec['OFF']/max(rec['dE5'],1):.1f}x mas rapido). NO ES LA PUERTA.")
        # --- el unico numero que el humo FIJA: C del control de CANTIDAD = sesgo medio de dE5 tras la inversion
        sq = [o for o in rg if o['arm'] == 'dE5'][0]['sesgo_q']
        C = round(float(np.mean(sq[2:])), 3)
        log(f"   *** C (control de CANTIDAD, brazo CONST) = media del sesgo de dE5 en Q3-Q4 = {C}. "
            f"Se escribe en el preregistro §10 y se pasa a la serie con JUACO_CONST={C}.")
        V['C_propuesto'] = C

        log(f"HUMO 3/4 — T-A: mundo vivo rep2, brazo VIVO, semilla {SEEDS_TA[0]}: OFF / dE5 (2 corridas).")
        rv = [tarea_vivo(('VIVO', SEEDS_TA[0], arm)) for arm in ARMS]
        for o in rv:
            log(f"   {o['arm']:5s} s{o['seed']}  r {o['r']}  descendientes {o['descendientes']}  muertes {o['deaths']} {o.get('muertes_nec')}  "
                f"celdas {o['celdas']} splits {o['splits']} des_splits {o['des_splits']}  sesgo_q {o['sesgo_q']}")

        log("HUMO 4/4 — T-D: bloque de la sal (sal muda), semilla ALIAS 326: OFF / dE5 (2 corridas).")
        rs = [tarea_sal(('S1-ALIAS', 326, arm)) for arm in ARMS]
        for o in rs:
            log(f"   {o['arm']:5s} s326  |W[sal]| {o['w_sal']} {o['w_sal_por_nec']}  W[veneno] {o['w_veneno']} {o['w_veneno_por_nec']}  "
                f"exp sal {o['exp_sal']} veneno {o['exp_veneno']}  des_splits {o['des_splits']}  splits {o['splits']} celdas {o['celdas']} muertes {o['deaths']}")

        dj = os.path.join(SAL, nom + '.json')
        json.dump(dict(meta=dict(fecha=time.strftime('%Y-%m-%dT%H:%M:%S'), humo=True, corridas=6,
                                 semillas=[SEEDS_TG[0], SEEDS_TA[0], 326], python=platform.python_version(), numpy=np.__version__,
                                 dosis=DOSIS, C_propuesto=V.get('C_propuesto'),
                                 sha_preregistro=h16(pre) if os.path.exists(pre) else None,
                                 sha_script=h16(os.path.abspath(__file__)),
                                 sha_organismo=h16(os.path.join(AQUI, 'organismo_v15_dE5.py')), identidad=V['identidad']),
                       identidad=r1, recuperacion=rg, vivo=rv, sal=rs),
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
    if C_CONST <= 0:
        log("*** C_CONST = 0: el brazo CONST seria identico a OFF y T-G no tendria control de cantidad. "
            "Pasa JUACO_CONST=<el C del humo> (preregistro §10). Se para.")
        _log['f'].close(); sys.exit(2)
    import corre_sal as CS
    for k in ('T-B', 'T-C_i', 'T-E', 'T-F_examen', 'T-D', 'T-C_ii', 'T-A', 'T-G'):
        V[k] = nada('etapa no corrida (--solo)')
    r2 = r3 = r4 = None
    res_sal = res_rev = res_vivo = res_tg = []
    VS = {}; VRev = {}

    # ---------------------------------------------------------------- ETAPA 1: identidad (SIEMPRE)
    log("ETAPA 1/9 — identidad (subproceso, un proceso): 61 identidades + 7 controles que DEBEN fallar.")
    r1 = sub([sys.executable, os.path.join(AQUI, 'identidad_v15_dE5.py'), '20000'], 'identidad')
    if r1['returncode'] != 0 or not any(ARNES_ESPERADO in l for l in r1['cola']):
        log(f"*** el arnes no es {ARNES_ESPERADO}; se para sin veredicto."); _log['f'].close(); sys.exit(1)
    V['identidad'] = ARNES_ESPERADO + ' (61 identidades + 7 controles que deben fallar)'

    # ---------------------------------------------------------------- ETAPA 2: T-B
    if hacer('TB'):
        log(f"ETAPA 2/9 — T-B generalizacion del candidato ({SEEDS_EX[0]}-{SEEDS_EX[-1]}; subproceso con su Pool).")
        r2 = sub([sys.executable, os.path.join(AQUI, 'bateria_generaliza_v15_dE5.py'), 'organismo_v15_dE5_on',
                  str(len(SEEDS_EX)), '--desde', str(SEEDS_EX[0]), '--log'], 'T-B')
        fB, jB = lee_json('regresion_generaliza_dE5_organismo_v15_dE5_on', r2)
        if jB is None:
            V['T-B'] = dict(pasa=False, medido=False, nota='sin JSON (ERR-43/ERR-87)')
        else:
            C_ = jB['corridas']; S = jB['meta']['semillas']
            px = {r['seed']: r for r in C_ if r['regla'] == 'px0'}; az = {r['seed']: r for r in C_ if r['regla'] == 'azar'}
            g1 = med([px[s]['acc'] for s in S]); g1az = med([az[s]['acc'] for s in S])
            g2 = med([px[s]['ba'] for s in S]); g2az = med([az[s]['ba'] for s in S])
            kc = sum(px[s]['cobertura'] >= 6 for s in S)
            u = UMB['T-B']
            V['T-B'] = dict(medido=True, json=os.path.basename(fB), G1=g1, G1_azar=g1az, G2=g2, G2_azar=g2az, K=kc,
                            bateria=jB['meta']['veredictos'],
                            pasa=bool(g1 is not None and g1 >= u['g1'] and g2 is not None and g2 >= u['g2']
                                      and g1az is not None and u['azar'][0] <= g1az <= u['azar'][1]
                                      and g2az is not None and u['azar2'][0] <= g2az <= u['azar2'][1] and kc == len(S)))
        log(f"   PUERTA T-B [{UMB['T-B']['frase']}] -> G1 {f3(V['T-B'].get('G1'))} G2 {f3(V['T-B'].get('G2'))} "
            f"azar {f3(V['T-B'].get('G1_azar'))}/{f3(V['T-B'].get('G2_azar'))} K {V['T-B'].get('K')}/{len(SEEDS_EX)} "
            f"-> {'PASA' if V['T-B']['pasa'] else 'NO'}")

    # ---------------------------------------------------------------- ETAPAS 3 y 4: examenes -> T-C (i), T-E, T-F
    if hacer('EX'):
        log(f"ETAPA 3/9 — examen v3' del CANDIDATO en {SEEDS_EX[0]}-{SEEDS_EX[-1]} (subproceso con su Pool).")
        r3 = sub([sys.executable, os.path.join(AQUI, 'bateria_v15_dE5.py'), str(len(SEEDS_EX)), '--desde', str(SEEDS_EX[0]), '--log'], 'examen candidato')
        fC, jC = lee_json('examen_dE5', r3)
        log(f"ETAPA 4/9 — examen v3' del TRONCO v14.2 en {SEEDS_EX[0]}-{SEEDS_EX[-1]}: JSON existente o subproceso.")
        fT, jT = json_tronco_examen()
        if jT is None:
            r4 = sub([sys.executable, os.path.join(ORG, 'bateria_v142.py'), str(len(SEEDS_EX)), '--desde', str(SEEDS_EX[0]), '--log'], 'examen tronco', cwd=ORG)
            fT, jT = lee_json('examen_v142', r4)
        else:
            log(f"   tronco: se lee {os.path.basename(fT)} (v14.2 en {SEEDS_EX[0]}-{SEEDS_EX[-1]}, ya corrido)")
        if jC is None or jT is None:
            for k in ('T-C_i', 'T-E', 'T-F_examen'):
                V[k] = dict(pasa=False, medido=False, nota='sin JSON del examen')
        else:
            con = conducta(jC, jT); cost = coste_examen(jC, jT)
            V['examen_json'] = dict(candidato=os.path.basename(fC), tronco=os.path.basename(fT),
                                    veredicto_v1_candidato=jC['meta']['veredictos'], veredicto_v1_tronco=jT['meta']['veredictos'])
            V['T-C_i'] = dict(medido=True, comeB_Q4=con['E2']['detalle']['come B Q4 >= 50 (T-C i)'],
                              pasa=bool(con['E2']['detalle']['come B Q4 >= 50 (T-C i)'] >= PUERTA_E))
            V['T-E'] = dict(medido=True, escenarios=con, pasa=bool(all(con[e]['pasa'] for e in SEIS)))
            V['T-F_examen'] = dict(medido=True, coste=cost, pasa=bool(all(cost[q]['pasa'] for q in cost)))
            for e in SEIS:
                log(f"      T-E {e:4s} {con[e]['todas']}/{con[e]['n']} {'PASA' if con[e]['pasa'] else 'NO'}  {con[e]['detalle']}  "
                    f"pesos {con[e]['pesos_reportados']}  veneno total med cand/tronco {con[e]['veneno_total_med']}")
            log(f"   PUERTA T-C (i) [come B Q4 >= 50 en >= {PUERTA_E}/20] -> {V['T-C_i']['comeB_Q4']}/20 -> {'PASA' if V['T-C_i']['pasa'] else 'NO'}")
            log(f"   PUERTA T-E [{UMB['T-E']['frase']}] -> " + ' '.join(f"{e} {con[e]['todas']}/{con[e]['n']}" for e in SEIS)
                + f" -> {'PASA' if V['T-E']['pasa'] else 'NO'}")
            log(f"   PUERTA T-F (examen) [{UMB['T-F']['frase']}] -> " + ' '.join(f"{q} {cost[q]['razon']}x" for q in cost)
                + f" -> {'PASA' if V['T-F_examen']['pasa'] else 'NO'}")

    # ---------------------------------------------------------------- ETAPA 5: T-D bloque de la sal
    if hacer('TD'):
        log("ETAPA 5/9 — T-D bloque de la sal (sal muda): 9 ALIAS + 9 LIMPIAS x {OFF, dE5} (Pool aqui).")
        tareas = [(b, s, arm) for b, seeds in (('S1-ALIAS', CS.ALIAS), ('S1-LIMPIA', CS.LIMPIAS)) for s in seeds for arm in ARMS]
        res_sal = crudo('TD', pool_map(tarea_sal, tareas, 'T-D'), extra=dict(alias=CS.ALIAS, limpias=CS.LIMPIAS))
        VS = veredicto_sal(res_sal); V['T-D'] = dict(VS, medido=True, pasa=bool(VS.get('dE5', {}).get('pasa')))
        log(f"      T-D letra (importada de creacion_B/corre_codigo.UMBRALES): {VS['letra']}")
        for arm in ARMS:
            if arm not in VS: continue
            log(f"      T-D {arm:5s} C1 {VS[arm]['C1']}  C2 {VS[arm]['C2']}  C6 {VS[arm]['C6']}  exp sal {VS[arm]['exp_sal']}  "
                f"des_splits {VS[arm]['des_splits']}  muertes alias/limpias {VS[arm]['muertes_alias']}/{VS[arm]['muertes_limpias']}")
        log(f"   PUERTA T-D [{UMB['T-D']['frase']}] -> OFF {'PASA' if VS.get('OFF', {}).get('pasa') else 'NO'} | "
            f"dE5 {'PASA' if V['T-D']['pasa'] else 'NO'} -> {'PASA' if V['T-D']['pasa'] else 'NO'}")

    # ---------------------------------------------------------------- ETAPA 6: T-C (ii) reversion en el mundo vivo
    if hacer('TC'):
        log(f"ETAPA 6/9 — T-C (ii) reversion en el mundo vivo (invertir_vivo_en={T//2}), {SEEDS_REV[0]}-{SEEDS_REV[-1]} x {{OFF, dE5}} (Pool aqui).")
        res_rev = crudo('TCii', pool_map(tarea_rev, [(s, arm) for s in SEEDS_REV for arm in ARMS], 'T-C ii'),
                        extra=dict(semillas=SEEDS_REV, invertir_vivo_en=T // 2))
        G = lambda arm: sorted([r for r in res_rev if r['arm'] == arm], key=lambda r: r['seed'])
        a = a12([r['rev'] for r in G('dE5')], [r['rev'] for r in G('OFF')])
        VRev = dict(A12_rev=a, rev_med=med([r['rev'] for r in G('dE5')]), rev_med_off=med([r['rev'] for r in G('OFF')]),
                    comeB_Q4_med=med([r['mordB'][3] for r in G('dE5')]), muerdeA_Q4_med=med([r['mordA'][3] for r in G('dE5')]),
                    muertes_med=med([r['deaths'] for r in G('dE5')]), muertes_off=med([r['deaths'] for r in G('OFF')]),
                    pasa=bool(a is not None and a >= UMB['T-C']['a12']))
        V['T-C_ii'] = dict(VRev, medido=True, pasa=VRev['pasa'])
        log(f"   PUERTA T-C (ii) [A12(rev ON > OFF) >= {UMB['T-C']['a12']}] -> A12 {VRev['A12_rev']}  rev med {VRev['rev_med']} (OFF {VRev['rev_med_off']})  "
            f"come B Q4 {VRev['comeB_Q4_med']}  muerde A Q4 {VRev['muerdeA_Q4_med']}  muertes {VRev['muertes_med']}/{VRev['muertes_off']} "
            f"-> {'PASA' if VRev['pasa'] else 'NO'}")

    # ---------------------------------------------------------------- ETAPA 7: T-A supervivencia
    if hacer('TA'):
        log(f"ETAPA 7/9 — T-A supervivencia en el mundo vivo (rep2, T={T}, costo=0.001), brazos {list(BRAZOS_TA)} x {{OFF, dE5}}, "
            f"semillas {SEEDS_TA[0]}-{SEEDS_TA[-1]} (Pool aqui).")
        res_vivo = crudo('TA', pool_map(tarea_vivo, [(b, s, arm) for b in BRAZOS_TA for s in SEEDS_TA for arm in ARMS], 'T-A'),
                         extra=dict(brazos=list(BRAZOS_TA), arms=list(ARMS), semillas=SEEDS_TA, T=T))
        VA = veredicto_vivo(res_vivo); V['T-A'] = dict(VA, medido=True)
        for b in BRAZOS_TA:
            if b not in VA: continue
            d = VA[b]
            log(f"      T-A {b:10s} muertes {d['muertes_on']} vs tronco {d['muertes_off']} (razon {d['razon_muertes']} <= {UMB['T-A']['muertes']})  "
                f"r {d['r_on']} vs {d['r_off']} (delta {d['r_delta']} >= -{UMB['T-A']['r_delta']})  A12(r) {d['A12_r']} >= {UMB['T-A']['a12']}  "
                f"desc {d['descendientes_on']}/{d['descendientes_off']}  celdas {d['celdas_on']}/{d['celdas_off']}  "
                f"splits {d['splits_on']}/{d['splits_off']}  -> {'PASA' if d['pasa'] else 'NO'}")
        log(f"   PUERTA T-A [{UMB['T-A']['frase']}] -> {'PASA' if VA['pasa'] else 'NO'}")

    # ---------------------------------------------------------------- ETAPA 8: T-G capacidad nueva (recuperacion)
    if hacer('TG'):
        log(f"ETAPA 8/9 — T-G capacidad nueva: RECUPERACION tras el cambio no avisado (mundo AB del tronco, T={T_TG}, "
            f"invertir_en={T_INV}), semillas {SEEDS_TG[0]}-{SEEDS_TG[-1]}, brazos {list(ARMS_TG)} (Pool aqui).")
        log(f"      control de CANTIDAD: CONST con sesgo_fijo = {C_CONST} (mismo empujon medio, SIN informacion); dE10 es referencia, sin umbral.")
        res_tg = crudo('TG', pool_map(tarea_tg, [(s, arm) for s in SEEDS_TG for arm in ARMS_TG], 'T-G'),
                       extra=dict(semillas=SEEDS_TG, T=T_TG, invertir_en=T_INV, brazos={k: v for k, v in ARMS_TG.items()}))
        VG = veredicto_tg(res_tg); V['T-G'] = dict(VG, medido=True)
        log(f"      T-G recup dE5 {VG['recup_on']} vs OFF {VG['recup_off']} (CONST {VG['recup_CONST']}, dE10 {VG['recup_dE10']}); "
            f"censurados {VG['censurados_on']}/{VG['censurados_off']}; veneno tras el cambio {VG['veneno_post_on']}/{VG['veneno_post_off']} "
            f"(razon {VG['razon_veneno']}); muertes {VG['muertes_on']}/{VG['muertes_off']}")
        log(f"   PUERTA T-G [{UMB['T-G']['frase']}] -> razon {VG['razon']} ({VG['veces_mas_rapido']}x)  pareado {VG['pareado_on_menor']}/{VG['n']}  "
            f"se apaga sola {VG['apagado']}/{VG['n']}  dE5<CONST {VG['pareado_on_menor_que_CONST']}/{VG['n']} (razon CONST {VG['razon_CONST']}) "
            f"-> {'PASA' if VG['pasa'] else 'NO'}")

    # ---------------------------------------------------------------- ETAPA 9: veredicto de las SIETE puertas
    log("ETAPA 9/9 — veredicto de las SIETE puertas del CRITERIO DE TRONCO v2.")
    puertas = {'T-A': V['T-A']['pasa'], 'T-B': V['T-B']['pasa'], 'T-C': bool(V['T-C_i']['pasa'] and V['T-C_ii']['pasa']),
               'T-D': V['T-D']['pasa'], 'T-E': V['T-E']['pasa'], 'T-F': V['T-F_examen']['pasa'], 'T-G': V['T-G']['pasa']}
    medido = {'T-A': bool(V['T-A'].get('medido')), 'T-B': bool(V['T-B'].get('medido')),
              'T-C': bool(V['T-C_i'].get('medido') and V['T-C_ii'].get('medido')), 'T-D': bool(V['T-D'].get('medido')),
              'T-E': bool(V['T-E'].get('medido')), 'T-F': bool(V['T-F_examen'].get('medido')), 'T-G': bool(V['T-G'].get('medido'))}
    V['puertas_dE5'] = puertas; V['puertas_medidas'] = medido
    for k in ('T-A', 'T-B', 'T-C', 'T-D', 'T-E', 'T-F', 'T-G'):
        log(f"   {k}: {'PASA' if puertas[k] else 'NO'}{'' if medido[k] else '  (NO MEDIDA en esta corrida)'}")
    todas = all(medido.values())
    if not todas:
        log("VEREDICTO: INCOMPLETO — faltan puertas por medir: " + ', '.join(k for k in medido if not medido[k]))
    elif all(puertas.values()):
        log("VEREDICTO: dE5 cruza las SIETE puertas del criterio v2 en semillas nuevas -> candidato a tronco; falta la REPLICA "
            "en semillas nuevas antes de congelar (regla 2 de v2). La decision es del director.")
    else:
        log("VEREDICTO: dE5 NO ENTRA — cae " + ', '.join(k for k in puertas if not puertas[k])
            + ". Una sola puerta caida basta (regla 2 de v2), sin modos intermedios.")
    meta = dict(fecha=time.strftime('%Y-%m-%dT%H:%M:%S'),
                semillas=dict(examen=SEEDS_EX, vivo=SEEDS_TA, reversion=SEEDS_REV, recuperacion=SEEDS_TG,
                              alias=CS.ALIAS, limpias=CS.LIMPIAS),
                dosis=DOSIS, C_const=C_CONST, umbrales={k: UMB[k]['frase'] for k in UMB}, veredictos=V, solo=SOLO,
                etapas=[r1, r2, r3, r4], procesos_python=ps, pool=N_PARALELO,
                sha_preregistro=h16(pre) if os.path.exists(pre) else None, sha_script=h16(os.path.abspath(__file__)),
                sha_construye=h16(os.path.join(AQUI, 'construye_v15_dE5.py')),
                sha_identidad=h16(os.path.join(AQUI, 'identidad_v15_dE5.py')),
                sha_organismo_v15_dE5=h16(os.path.join(AQUI, 'organismo_v15_dE5.py')),
                sha_organismo_v15_dE5_on=h16(os.path.join(AQUI, 'organismo_v15_dE5_on.py')),
                sha_bateria=h16(os.path.join(AQUI, 'bateria_v15_dE5.py')),
                sha_bateria_generaliza=h16(os.path.join(AQUI, 'bateria_generaliza_v15_dE5.py')),
                python=platform.python_version(), numpy=np.__version__)
    dj = os.path.join(DATOS, nom + '.json')
    json.dump(dict(meta=meta, sal=res_sal, reversion=res_rev, vivo=res_vivo, recuperacion=res_tg),
              open(dj, 'w', encoding='utf-8'), ensure_ascii=False, default=str)
    log(f"datos -> {os.path.basename(dj)}  sha256_16 = {h16(dj)}")
    _log['f'].close()
