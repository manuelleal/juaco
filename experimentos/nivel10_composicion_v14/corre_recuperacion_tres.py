"""corre_recuperacion_tres.py -- T3 de PREREGISTRO_composicion_tres.md: recuperacion tras la inversion con LA
TERCERA PIEZA EN COMPAÑIA de las otras dos. Brazos V13 (organismo_v14t, las TRES perillas apagadas) y TRES
(organismo_v14t_on, las TRES ON), semillas 161-180 (nunca antes vistas por este mecanismo).

POR QUE UN RUNNER APARTE (declarado en la seccion 4 del preregistro): `corre_probar_si_mismo.py` decide sus
BRAZOS por kwargs sobre un MODULO FIJO -- su `tarea()` hace `import organismo_v13p as v13p` (tipos 'T'/'M'/'B') o
`import organismo_v13pg as pg` (tipo 'G') SIN CONDICION, y llama `v13p.run(seed, ..., **BRAZOS[brazo])`. No hay
forma de pedirle "usa organismo_v14t_on para el brazo TRES" sin editarlo, y es un instrumento YA CORRIDO
(identidades J1-J6 en PREREGISTRO_probar_si_mismo.md): no se toca (EQUIPO.md regla 1). Este runner reproduce
EXACTAMENTE su medida:
  - t_ext_B: igual criterio (M1 del bloque 6), mismo campo de salida.
  - recup = T - invertir_en  si t_ext_B is None (censurado)  si no  t_ext_B - invertir_en.  Misma formula que
    `rec_pasos()` de corre_probar_si_mismo.py.
  - T=200000, invertir_en=100000: LOS MISMOS valores que corre_probar_si_mismo.py (T_INV = T//2).
  - criterio **P1'/P4'** de `analiza_dE.py` (la forma RELATIVA preregistrada en la enmienda 1 de
    PREREGISTRO_probar_si_mismo.md para organos que actuan en la boca -- la misma vara que ya paso dE-TEST solo):
      P1' recuperacion(TRES) mediana <= 0.60 x recuperacion(V13) mediana  Y  pareado (TRES < V13) >= 14/20
      P4' se apaga solo (forma relativa): sesgo_boca[Q2]<=0.10, sesgo_boca[Q4]<=0.10,
          sesgo_boca[Q2]<=0.35*sesgo_boca[Q3], sesgo_boca[Q4]<=0.35*sesgo_boca[Q3]  en  >=16/20
    Los umbrales que decide este runner son los del PREREGISTRO (ERR-31): 0.60x/14/20/16/20, escritos ANTES de
    correr en PREREGISTRO_composicion_tres.md seccion 5 -- no se leen de ningun otro runner que se reutiliza.

REGLA 10 (EQUIPO.md): log desde el arranque, con fsync. REGLA 11: un solo Pool a la vez -- este runner abre UN
Pool (real) o ninguno (--humo, un proceso). REGLA 3: un implementador no corre Pool -- --humo corre 2 semillas,
T corto, un proceso, sin Pool; el coordinador corre la version real (sin --humo). REGLA 28 (ERR-28): organismo/
va PRIMERO en sys.path, siempre.

Uso (desde la raiz del repo):
  python experimentos/nivel10_composicion_v14/corre_recuperacion_tres.py --humo
  python experimentos/nivel10_composicion_v14/corre_recuperacion_tres.py [--desde 161] [--n 20]
"""
import sys, os, json, time, hashlib, platform
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
import numpy as np

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
# ERR-28: organismo/ PRIMERO en sys.path, siempre (aunque organismo_v14t/_on vivan en este mismo directorio).
sys.path[:0] = [AQUI, os.path.join(RAIZ, 'organismo')]

HUMO = '--humo' in sys.argv


def _arg(flag, default):
    return int(sys.argv[sys.argv.index(flag) + 1]) if flag in sys.argv else default


DESDE = _arg('--desde', 161)
NSEM = 2 if HUMO else _arg('--n', 20)
SEEDS = list(range(DESDE, DESDE + NSEM))
T = 3000 if HUMO else 200000
T_INV = T // 2   # 1500 en humo, 100000 real -- igual que T_INV de corre_probar_si_mismo.py (T//2)
N_PARALELO = 14

# V13 = organismo_v14t con SUS PROPIOS defaults (las tres perillas apagadas, == organismo_v13, identidad_v14t.py a).
# TRES = organismo_v14t_on con SUS PROPIOS defaults (las tres perillas fijas ON). Ni un kwarg extra en ninguno.
BRAZOS = {'V13': {}, 'TRES': {}}

# ---- criterio del preregistro (T3, seccion 5): P1'/P4' de analiza_dE.py, forma relativa ----
REC_MAX_RATIO = 0.60
REC_PAREADO_MIN = 14
APAGA_MIN = 16


def rec_pasos(r):
    """Recuperacion = t_ext_B - invertir_en, censurada a T-T_INV si nunca ocurre. Misma formula que rec_pasos() de
    corre_probar_si_mismo.py."""
    te = r.get('t_ext_B')
    return (T - T_INV) if te is None else (te - T_INV)


def tarea(args):
    brazo, seed = args
    import organismo_v14t as V14T, organismo_v14t_on as V14TON
    mod = V14T if brazo == 'V13' else V14TON
    r = mod.run(seed, T=T, invertir_en=T_INV, **BRAZOS[brazo])
    return dict(brazo=brazo, seed=seed, t_ext_B=r['t_ext_B'], recup=rec_pasos(r), censurado=r['t_ext_B'] is None,
                sesgo_boca=r['sesgo_boca'], veneno_post=r['mord_post']['veneno'], comida_post=r['mord_post']['comida'],
                deaths=r['deaths'], deaths_post=r['deaths_post'], sbarE=r['sbarE'], W=r['W'], celdas=r['celdas'],
                splits=r['splits'])


_log = {'f': None, 't0': time.time()}


def log(msg=""):
    linea = f"[{time.strftime('%H:%M:%S')} +{time.time()-_log['t0']:7.1f}s] {msg}"
    print(linea, flush=True)
    if _log['f']:
        _log['f'].write(linea + "\n"); _log['f'].flush(); os.fsync(_log['f'].fileno())


def h16(p):
    return hashlib.sha256(open(p, 'rb').read()).hexdigest()[:16]


def mediana(xs):
    xs = [x for x in xs if x is not None]
    return float(np.median(xs)) if xs else None


def veredicto_txt(v):
    return 'OK' if v is True else ('NO' if v is False else 'HUMO: no aplica')


if __name__ == '__main__':
    import multiprocessing as mp
    mp.set_start_method('spawn', force=True)
    stamp = time.strftime('%Y%m%d_%H%M%S')
    nom = f'recuperacion_tres{"_humo" if HUMO else ""}_{stamp}'
    _log['f'] = open(os.path.join(RAIZ, 'datos', nom + '.log'), 'w', encoding='utf-8', newline='\n')
    shas = {n_: h16(p) for n_, p in [
        ('preregistro', os.path.join(AQUI, 'PREREGISTRO_composicion_tres.md')), ('script', os.path.abspath(__file__)),
        ('organismo_v14t', os.path.join(AQUI, 'organismo_v14t.py')), ('organismo_v14t_on', os.path.join(AQUI, 'organismo_v14t_on.py')),
        ('referencia_medida corre_probar_si_mismo', os.path.join(RAIZ, 'experimentos', 'nivel9_probar_si_mismo', 'corre_probar_si_mismo.py')),
        ('referencia_criterio analiza_dE', os.path.join(RAIZ, 'experimentos', 'nivel9_probar_si_mismo', 'analiza_dE.py'))]}
    log(f"ARRANQUE T3 recuperacion tras la inversion, LA TERCERA PIEZA EN COMPANIA (V13 vs TRES). "
        f"{'HUMO (un proceso, sin Pool)' if HUMO else f'REAL Pool({N_PARALELO})'}  T={T}  invertir_en={T_INV}  semillas {SEEDS[0]}-{SEEDS[-1]}")
    log("sha " + "  ".join(f"{k}={v}" for k, v in shas.items()))

    lote = [(b, s) for b in BRAZOS for s in SEEDS]
    if HUMO:
        res = [tarea(x) for x in lote]
    else:
        with mp.Pool(N_PARALELO) as pool:
            res = list(pool.imap_unordered(tarea, lote, chunksize=1))

    Gb = {b: {r['seed']: r for r in res if r['brazo'] == b} for b in BRAZOS}
    v13m = mediana([Gb['V13'][s]['recup'] for s in SEEDS])
    tresm = mediana([Gb['TRES'][s]['recup'] for s in SEEDS])
    razon = (tresm / v13m) if (v13m not in (None, 0) and tresm is not None) else None
    pareado = sum(1 for s in SEEDS if Gb['TRES'][s]['recup'] < Gb['V13'][s]['recup'])
    apaga = sum(1 for s in SEEDS
                if all(Gb['TRES'][s]['sesgo_boca'][i] is not None for i in (1, 2, 3))
                and Gb['TRES'][s]['sesgo_boca'][1] <= 0.10 and Gb['TRES'][s]['sesgo_boca'][3] <= 0.10
                and Gb['TRES'][s]['sesgo_boca'][1] <= 0.35 * Gb['TRES'][s]['sesgo_boca'][2]
                and Gb['TRES'][s]['sesgo_boca'][3] <= 0.35 * Gb['TRES'][s]['sesgo_boca'][2])
    ven_v13 = mediana([Gb['V13'][s]['veneno_post'] for s in SEEDS]); ven_tres = mediana([Gb['TRES'][s]['veneno_post'] for s in SEEDS])
    dea_v13 = mediana([Gb['V13'][s]['deaths'] for s in SEEDS]); dea_tres = mediana([Gb['TRES'][s]['deaths'] for s in SEEDS])
    cens_v13 = sum(Gb['V13'][s]['censurado'] for s in SEEDS); cens_tres = sum(Gb['TRES'][s]['censurado'] for s in SEEDS)

    log(); log(f"V13  recuperacion mediana {v13m}  censuradas {cens_v13}/{len(SEEDS)}")
    log(f"TRES recuperacion mediana {tresm}  censuradas {cens_tres}/{len(SEEDS)}  razon TRES/V13 {razon}")

    P1 = None if HUMO else bool(razon is not None and razon <= REC_MAX_RATIO and pareado >= REC_PAREADO_MIN)
    P4 = None if HUMO else bool(apaga >= APAGA_MIN)
    P7 = None if HUMO else bool(ven_tres is not None and ven_v13 is not None and dea_tres is not None and dea_v13 is not None
                                and ven_tres <= 4 * ven_v13 and dea_tres <= 1.5 * dea_v13)
    log(f"T3-P1' recuperacion TRES/V13 = {razon} (<={REC_MAX_RATIO}) y pareado {pareado}/{len(SEEDS)} (>={REC_PAREADO_MIN})  -> {veredicto_txt(P1)}")
    log(f"T3-P4' se apaga solo (forma relativa) en {apaga}/{len(SEEDS)} (>={APAGA_MIN})  -> {veredicto_txt(P4)}")
    log(f"T3-P7' (no bloqueante) veneno_post {ven_tres} <=4x{ven_v13}, muertes {dea_tres} <=1.5x{dea_v13}  -> {veredicto_txt(P7)}")

    ok_T3 = None if HUMO else bool(P1 and P4)
    log()
    log("VEREDICTO T3: " + ("HUMO OK (montaje corre, ningun criterio numerico vale)" if HUMO else
        ("CUMPLE" if ok_T3 else "NO CUMPLE (la sorpresa pierde su efecto en compania, clausula del preregistro)")))

    meta = dict(fecha=time.strftime('%Y-%m-%dT%H:%M:%S'), humo=HUMO, T=T, invertir_en=T_INV, semillas=[SEEDS[0], SEEDS[-1]],
               shas=shas, python=platform.python_version(), numpy=np.__version__, plataforma=platform.platform(),
               T3=dict(recup_V13=v13m, recup_TRES=tresm, razon=razon, pareado=pareado, apaga=apaga,
                       veneno_post_V13=ven_v13, veneno_post_TRES=ven_tres, deaths_V13=dea_v13, deaths_TRES=dea_tres,
                       censuradas_V13=cens_v13, censuradas_TRES=cens_tres,
                       P1=P1, P4=P4, P7=P7, ok=ok_T3))
    dj = os.path.join(RAIZ, 'datos', nom + '.json')
    json.dump(dict(meta=meta, corridas=res), open(dj, 'w', encoding='utf-8'), ensure_ascii=False, default=str)
    log(f"datos -> {os.path.basename(dj)}  sha256_16 = {h16(dj)}")
    _log['f'].close()
