"""corre_anclado.py -- MUNDO ANCLADO (rama mundo-anclado). Ejecuta PREREGISTRO_mundo_anclado.md.

MISION: llegar a la AGI por este camino. Un mundo donde la ignorancia (NADA) NO sostiene un linaje y el
conocimiento perfecto (ORACULO) SI; el espacio entre los dos mide inteligencia, y REL (el aprendizaje heredado
por el nodo) se MIDE, no se calibra.

Instrumento: organismo_anclado.py (por anclas desde organismo_f9c.py 9dd1fb91ecec35ae; construye_anclado.py;
arnes identidad_anclado.py). Brazos: corre_bloque2.BRAZOS (MISMO objeto importado) + SOLO las perillas del
mundo {rep_acum, olv_mal, olv_ciego} y la medida anc_mide=1 (regla 14 campo a campo en regla14()).

    python experimentos/mundo_anclado/corre_anclado.py --humo                    (UN proceso, 6 corridas, semilla 1)
    python experimentos/mundo_anclado/corre_anclado.py --calibra                 (7001-7020, rejilla secuencial del preregistro)
    python experimentos/mundo_anclado/corre_anclado.py --confirma --h H --acum A (7041-7060, el punto elegido)
    ... --pool N   (SOLO el coordinador; por defecto 1 = un proceso, sin Pool)

ERR-54: el crudo se escribe ANTES de analizar. ERR-89: una linea por puerta.
"""
import argparse, hashlib, json, os, statistics as st, sys, time

sys.stdout.reconfigure(encoding='utf-8', errors='replace')
AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
N09B2 = os.path.join(RAIZ, 'experimentos', 'nivel09_cuerpo_nuevo_b2')
sys.path[:0] = [N09B2]
import corre_bloque2 as B2                     # inserta sus rutas (organismo/ primero, ERR-28)
sys.path.insert(0, AQUI)
import organismo_anclado as ANC

T = 100000
HUMO = os.path.join(RAIZ, 'datos', 'humo')
DATOS = os.path.join(RAIZ, 'datos')
PREREG = os.path.join(AQUI, 'PREREGISTRO_mundo_anclado.md')
SHA_F9C = '9dd1fb91ecec35ae'
SHA_ANC = 'e689c2952b1991a4'

# ------------------------------------------------------------------ LA LETRA DEL PREREGISTRO
CAL_DESDE, CONF_DESDE, NSEM = 7001, 7041, 20
# UNA sola perilla (olv_mal); rep_acum queda en 0 (la de bloque 2 por defecto) -- justificacion en el preregistro sec. 2.
# Rejilla ASCENDENTE fijada con el humo anclado_humo_20260922_135253 (semilla 1): h=0.003 ya da ORACULO 2.3.
GRID = [(0, 0.0005), (0, 0.001), (0, 0.0015), (0, 0.002), (0, 0.003)]
ANCLA_NADA = (0.10, 0.30)          # R0 mediana de NADA
ANCLA_OR = 1.0                     # R0 mediana de ORACULO
MARGEN_NADA = (0.12, 0.28)         # regla de ELECCION con margen (sec. 5 del preregistro)
MARGEN_OR = 1.10
PERILLAS = ('rep_acum', 'olv_mal', 'olv_ciego', 'anc_mide')
# brazo del anclado -> (brazo del bloque 2, olv_ciego)
BRAZOS = {'NADA': ('NADA', 0), 'REL': ('REL', 0), 'ORACULO': ('ORACULO', 0), 'REL_BAR': ('REL_BAR', 0),
          'ORACULO_CIEGO': ('ORACULO', 1), 'NADA_CIEGO': ('NADA', 1), 'RENACE': ('RENACE', 0)}
CONF_ORDEN = ['NADA', 'ORACULO', 'REL', 'REL_BAR', 'ORACULO_CIEGO', 'NADA_CIEGO', 'RENACE']

LOG = [None]


def log(s=''):
    print(s, flush=True)
    if LOG[0]:
        LOG[0].write(s + '\n'); LOG[0].flush()


def h16(p):
    return hashlib.sha256(open(p, 'rb').read()).hexdigest()[:16]


def kwargs(brazo, acum, h):
    base, ciego = BRAZOS[brazo]
    kw = dict(B2.BRAZOS[base], rep_acum=acum, anc_mide=1)
    if h:
        kw['olv_mal'] = h
        if ciego:
            kw['olv_ciego'] = 1
    elif ciego:
        raise SystemExit(f'{brazo}: el placebo exige h>0')
    return kw


def regla14():
    """Cada brazo = corre_bloque2.BRAZOS[base] campo a campo + SOLO las perillas declaradas."""
    for b in BRAZOS:
        base = BRAZOS[b][0]
        kw = kwargs(b, 1, 0.006)
        ref = B2.BRAZOS[base]
        falta = [k for k in ref if k not in kw]
        dif = [k for k in ref if k in kw and kw[k] is not ref[k] and kw[k] != ref[k]]
        extra = [k for k in kw if k not in ref and k not in PERILLAS]
        ok = not (falta or dif or extra)
        log(f"  {'OK  ' if ok else 'FALLA'} regla14 {b:14s} = corre_bloque2.BRAZOS[{base!r}] ({len(ref)} campos) + "
            f"{sorted(k for k in kw if k not in ref)}  falta={falta} dif={dif} extra={extra}")
        if not ok:
            raise SystemExit('REGLA 14 FALLA: no se corre nada')


def resumen(brazo, seed, acum, h, r, seg):
    o = B2.resumen(brazo, seed, acum, r, seg)          # MISMA definicion de R0 = desc/(muertes+1), vidas, p1, c1, J
    a = r.get('anclado') or {}
    p = a.get('pres') or {}; tot = sum(p.values())
    o.update(h=h, f_mala=(round((p.get('B', 0) + p.get('D', 0)) / tot, 4) if tot else None),
             anc_eventos=a.get('eventos'), anc_rem=a.get('rem'))
    return o


def tarea(args):
    brazo, seed, acum, h, Ti = args
    t0 = time.time()
    r = ANC.run(seed, T=Ti, **kwargs(brazo, acum, h))
    return resumen(brazo, seed, acum, h, r, time.time() - t0)


def corre(tareas, pool):
    if pool and pool > 1:
        from multiprocessing import Pool
        with Pool(pool) as P:
            return list(P.imap(tarea, tareas))
    out = []
    for i, t in enumerate(tareas):
        o = tarea(t); out.append(o)
        log(f"    {o['brazo']:14s} s{o['seed']} acum={o['acum']} h={o['h']}  R0={o['R0']:.3f}  vida={o['vida_med']}  "
            f"f_mala={o['f_mala']}  J={o['J']}  ({o['seg']:.1f}s)")
    return out


def md(R, brazo, campo='R0'):
    xs = [x[campo] for x in R if x['brazo'] == brazo and x[campo] is not None]
    return round(st.median(xs), 4) if xs else None


def escribe(ruta, obj):
    with open(ruta, 'w', encoding='utf-8') as f:
        json.dump(obj, f, ensure_ascii=False, indent=1)
    log(f"  crudo -> {ruta} (sha {h16(ruta)})")


def cabecera(modo):
    log(f"MUNDO ANCLADO · {modo} · {time.strftime('%Y-%m-%d %H:%M:%S')} · T={T}")
    log(f"  organismo_f9c {h16(os.path.join(N09B2, 'organismo_f9c.py'))} (esperado {SHA_F9C}) · organismo_anclado "
        f"{h16(os.path.join(AQUI, 'organismo_anclado.py'))} (esperado {SHA_ANC})")
    if h16(os.path.join(AQUI, 'organismo_anclado.py')) != SHA_ANC or h16(os.path.join(N09B2, 'organismo_f9c.py')) != SHA_F9C:
        raise SystemExit('SHA del instrumento cambio: no se corre')
    if os.path.exists(PREREG):
        log(f"  PREREGISTRO sha {h16(PREREG)}")
    elif not modo.startswith('HUMO'):
        raise SystemExit('sin PREREGISTRO_mundo_anclado.md no se calibra ni se confirma')
    regla14()


# ------------------------------------------------------------------ modos
def humo(pool):
    s = time.strftime('%Y%m%d_%H%M%S')
    os.makedirs(HUMO, exist_ok=True)
    LOG[0] = open(os.path.join(HUMO, f'anclado_humo_{s}.log'), 'w', encoding='utf-8')
    cabecera('HUMO (semilla 1, ya vista; 6 corridas, un proceso)')
    tareas = [('ORACULO', 1, 0, 0.003, T), ('ORACULO', 1, 0, 0.006, T), ('ORACULO', 1, 0, 0.012, T),
              ('NADA', 1, 0, 0.006, T), ('NADA', 1, 0, 0.012, T), ('ORACULO_CIEGO', 1, 0, 0.006, T)]
    R = corre(tareas, 1)
    escribe(os.path.join(HUMO, f'anclado_humo_{s}.json'), dict(modo='humo', sello=s, T=T, corridas=R))


def ancla_ok(nada, orac, lo_hi, umbral):
    return nada is not None and orac is not None and lo_hi[0] <= nada <= lo_hi[1] and orac >= umbral


def calibra(pool):
    s = time.strftime('%Y%m%d_%H%M%S')
    LOG[0] = open(os.path.join(DATOS, f'anclado_cal_s{CAL_DESDE}-{CAL_DESDE + NSEM - 1}_{s}.log'), 'w', encoding='utf-8')
    cabecera(f'CALIBRACION {CAL_DESDE}-{CAL_DESDE + NSEM - 1} (rejilla SECUENCIAL, regla sec. 5)')
    semillas = list(range(CAL_DESDE, CAL_DESDE + NSEM))
    todo, filas, elegido = [], [], None
    ruta = os.path.join(DATOS, f'anclado_cal_s{CAL_DESDE}-{CAL_DESDE + NSEM - 1}_{s}.json')
    fuera = set()
    for acum, h in GRID:
        if acum in fuera:
            log(f"  punto acum={acum} h={h}: SALTADO (NADA ya salio por arriba en este rep_acum, regla 5c)")
            continue
        log(f"  punto acum={acum} h={h}")
        R = corre([(b, sd, acum, h, T) for b in ('NADA', 'ORACULO') for sd in semillas], pool)
        todo += R
        escribe(ruta, dict(modo='calibra', sello=s, T=T, grid=GRID, corridas=todo, filas=filas))   # ERR-54
        nada, orac = md(R, 'NADA'), md(R, 'ORACULO')
        anc = ancla_ok(nada, orac, ANCLA_NADA, ANCLA_OR); mar = ancla_ok(nada, orac, MARGEN_NADA, MARGEN_OR)
        filas.append(dict(acum=acum, h=h, R0_NADA=nada, R0_OR=orac, ancla=anc, margen=mar,
                          vida_NADA=md(R, 'NADA', 'vida_med'), vida_OR=md(R, 'ORACULO', 'vida_med'),
                          fmala_NADA=md(R, 'NADA', 'f_mala'), fmala_OR=md(R, 'ORACULO', 'f_mala')))
        log(f"  -> R0 NADA {nada}  R0 ORACULO {orac}  ancla={'SI' if anc else 'no'}  con margen={'SI' if mar else 'no'}")
        if mar:
            elegido = dict(acum=acum, h=h, regla='primer punto CON MARGEN'); break
        # si NADA ya se salio por arriba del ancla, subir h en este acum no puede arreglarlo: pasar al siguiente acum
        if nada is not None and nada > ANCLA_NADA[1]:
            log(f"  NADA {nada} > {ANCLA_NADA[1]}: el resto de este rep_acum queda fuera (regla sec. 5c)")
            fuera.add(acum)
    if elegido is None:
        cand = [f for f in filas if f['ancla']]
        if cand:
            elegido = dict(acum=cand[0]['acum'], h=cand[0]['h'], regla='primer punto que ANCLA sin margen (declarado)')
    escribe(ruta, dict(modo='calibra', sello=s, T=T, grid=GRID, corridas=todo, filas=filas, elegido=elegido))
    log(f"\n  PUNTO ELEGIDO: {elegido if elegido else 'NINGUNO -- el mundo anclado NO existe con estas perillas en la rejilla (se declara; NO se amplia)'}")


def confirma(h, acum, desde, pool, brazos):
    s = time.strftime('%Y%m%d_%H%M%S')
    tag = f'anclado_conf_s{desde}-{desde + NSEM - 1}_{s}'
    LOG[0] = open(os.path.join(DATOS, tag + '.log'), 'w', encoding='utf-8')
    cabecera(f'CONFIRMACION {desde}-{desde + NSEM - 1} en acum={acum} h={h} · brazos {brazos}')
    R = corre([(b, sd, acum, h, T) for b in brazos for sd in range(desde, desde + NSEM)], pool)
    escribe(os.path.join(DATOS, tag + '.json'), dict(modo='confirma', sello=s, T=T, h=h, acum=acum, corridas=R))
    juzga(R, h, acum)


def juzga(R, h, acum):
    A12 = B2.A12
    m = {b: md(R, b) for b in CONF_ORDEN}
    v = {b: md(R, b, 'vida_med') for b in CONF_ORDEN}
    fm = {b: md(R, b, 'f_mala') for b in CONF_ORDEN}
    J = {b: md(R, b, 'J') for b in CONF_ORDEN}
    col = lambda b: [x['R0'] for x in R if x['brazo'] == b]
    log(f"\n  medianas: " + '  '.join(f"{b} R0={m[b]} vida={v[b]} f_mala={fm[b]} J={J[b]}" for b in CONF_ORDEN if m[b] is not None))
    ok = lambda c: 'PASA' if c else 'CAE'
    nada, orac, rel, bar, cie = m['NADA'], m['ORACULO'], m['REL'], m['REL_BAR'], m['ORACULO_CIEGO']
    log(f"  ANC-1  NADA no sostiene: R0 mediana {nada} en [{ANCLA_NADA[0]}, {ANCLA_NADA[1]}] -> "
        f"{ok(nada is not None and ANCLA_NADA[0] <= nada <= ANCLA_NADA[1])}")
    log(f"  ANC-2  ORACULO sostiene: R0 mediana {orac} >= {ANCLA_OR} -> {ok(orac is not None and orac >= ANCLA_OR)}")
    pos = (round((rel - nada) / (orac - nada), 3) if None not in (rel, nada, orac) and orac != nada else None)
    log(f"  REL    (se MIDE, no se calibra): R0 {rel}; posicion en el espacio NADA-ORACULO = {pos}  (prediccion P3: 0.55-0.90)")
    if bar is not None:
        pb = (round((bar - nada) / (orac - nada), 3) if None not in (bar, nada, orac) and orac != nada else None)
        a = A12(col('REL'), col('REL_BAR'))
        log(f"  CTL-1  BARAJA (contenido): REL_BAR posicion {pb} <= 0.35 y A12(REL>REL_BAR) {a} >= 0.75 -> "
            f"{ok(pb is not None and pb <= 0.35 and a is not None and a >= 0.75)}")
    if cie is not None:
        a = A12(col('ORACULO'), col('ORACULO_CIEGO'))
        log(f"  CTL-2  PLACEBO (dilucion ciega, misma dosis): ORACULO_CIEGO R0 {cie} < {ANCLA_OR} y A12(ORACULO>CIEGO) {a} >= 0.70 -> "
            f"{ok(cie < ANCLA_OR and a is not None and a >= 0.70)}  (si CAE: lo que ancla es el RECAMBIO, no el TIPO)")
    if m['NADA_CIEGO'] is not None:
        log(f"  REP-1  NADA_CIEGO R0 {m['NADA_CIEGO']} (se reporta)")
    if m['RENACE'] is not None:
        log(f"  REP-2  RENACE (inmortal subsidiado) R0 {m['RENACE']} (se reporta)")
    log(f"  REP-3  mundo que se come la comida: f_mala NADA {fm['NADA']} ORACULO {fm['ORACULO']} REL {fm['REL']} (se reporta; "
        f"f_mala < 0.25 en ORACULO = el mundo ya casi no tiene nada que discriminar, se declara)")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--humo', action='store_true')
    ap.add_argument('--calibra', action='store_true')
    ap.add_argument('--confirma', action='store_true')
    ap.add_argument('--h', type=float)
    ap.add_argument('--acum', type=int, default=0)
    ap.add_argument('--desde', type=int, default=CONF_DESDE)
    ap.add_argument('--brazos', default=','.join(CONF_ORDEN))
    ap.add_argument('--pool', type=int, default=1)
    a = ap.parse_args()
    if a.humo:
        humo(1)
    elif a.calibra:
        calibra(a.pool)
    elif a.confirma:
        if a.h is None:
            raise SystemExit('--confirma exige --h (el punto elegido por la calibracion)')
        confirma(a.h, a.acum, a.desde, a.pool, a.brazos.split(','))
    else:
        ap.print_help()


if __name__ == '__main__':
    main()
