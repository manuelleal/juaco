"""corre_baldwin.py — RUNNER y LETRA de BALDWIN EN BLOQUES (la seleccion construye la PLASTICIDAD). Preregistro: PREREGISTRO_baldwin.md
(la letra esta AQUI, en lee(), y alli en la sec. 6).

MISION: llegar a la AGI por este camino (organismo minimo con reglas locales, sin retropropagacion, peldanos preregistrados con
controles y replicas).

ENTRADA (regla 14): cada corrida ES corre_bloques.corre (experimentos/organelos/bloques/opusM/corre_bloques.py, sha a090b82eae9f1ee3, se
IMPORTA y no se toca; es la de la serie BLOQUES = FUNCIONA x2) con su gemelo cambiado a motor_baldwin (construido por anclas desde
motor_bloques3; plast = 0 == motor_bloques3 bit a bit, y sin inversion == motor_bloques: arnes identidad_baldwin.py). Lo unico agregado
al JSON de corre_bloques.corre: el bloque 'baldwin' (medidas de la plasticidad, calculadas del mismo JSON) y 'cfg_worker' (la BQ_CFG que el
worker uso de verdad).

MUNDO: ECO w90, carro FABRICA_ECO (hijo ingenuo), vivero finito (t_corte 100 000), genetica MUT0 + reglas heredables (kit 1 = BLOQ_V).
Inversion del SIGNIFICADO A<->B, C<->D cada P pasos (motor_bloques3). Vida medida: mediana de vida_media_muertos_2a de BLOQ_V en las dos
series de BLOQUES = 2289 y 2257 pasos -> VIDA = 2270. P/vida ~ 3, 10, 30 -> P = 6 000 (2.6), 22 000 (9.7), 68 000 (30.0) (multiplos de
cada_gen 2 000, exigencia de motor_bloques3) y P = infinito (sin inversion).

BRAZOS (plast: 0 FIJO = BLOQ_V, 1 PLAST_V, 2 PLAST_AZA bit sorteado al nacer, 3 PLAST_RW0 w deriva sin la consecuencia):
  P22k: PLAST_V, FIJO_V, PLAST_AZA, PLAST_RW0   ·   P6k, P68k, Pinf: PLAST_V, FIJO_V        (10 brazos x 20 semillas = 200 corridas)

SEMILLAS NUEVAS (grep 29-sep en PROYECTOS/JUACO, .py/.md/.txt fuera de datos: 564xx no aparece): serie 56401-56420 · replica 56421-56440 ·
arnes 56491-56494 · humo 56495.

Uso (banderas desconocidas o abreviadas ABORTAN, ERR-115; --serie/--replica SOLO el coordinador, con el preregistro y este runner
commiteados y sin cambios respecto de HEAD):
  python experimentos/organelos/baldwin/corre_baldwin.py --humo                 # 1 proceso, 6 corridas, s56495, T 200 000; escribe JSON
  python experimentos/organelos/baldwin/corre_baldwin.py --serie --pool 2       # 200 corridas; se niega si ya hay veredicto
  python experimentos/organelos/baldwin/corre_baldwin.py --serie --pool 2 --reanuda
  python experimentos/organelos/baldwin/corre_baldwin.py --replica --pool 2     # solo si la serie da FUNCIONA o HAY ALGO MODESTO
  python experimentos/organelos/baldwin/corre_baldwin.py --lee <carpeta>
  python experimentos/organelos/baldwin/corre_baldwin.py --bloque <resumen serie>.json,<resumen replica>.json
"""
import argparse, glob, hashlib, json, os, platform, subprocess, sys, time, types
import numpy as np

try: sys.stdout.reconfigure(encoding='utf-8', errors='replace')
except Exception: pass
AQUI = os.path.dirname(os.path.abspath(__file__))
ORG = os.path.dirname(AQUI)
RAIZ = os.path.dirname(os.path.dirname(ORG))
OPUSM = os.path.join(ORG, 'bloques', 'opusM')
for _d in (OPUSM, AQUI):
    if _d not in sys.path: sys.path.insert(0, _d)
import corre_bloques as CB   # noqa: E402  (importa nucleo_eco_sel_ing; se IMPORTA, no se toca)
import construye_baldwin as KB   # noqa: E402  (solo construye(): no escribe nada)
NS = CB.NS
USA_BLOQUES_ORIGINAL = CB.usa_bloques   # el arnes lo usa para la identidad contra motor_bloques

PRERREGISTRO = 'PREREGISTRO_baldwin.md'
DATOS = os.path.join(AQUI, 'datos')
MOTOR = os.path.join(AQUI, 'motor_baldwin.py')
SHAS = {os.path.join(OPUSM, 'corre_bloques.py'): 'a090b82eae9f1ee3', os.path.join(OPUSM, 'motor_bloques.py'): 'ff782697e54585a5',
        os.path.join(OPUSM, 'motor_bloques3.py'): '21b5ee28d086b3be', os.path.join(OPUSM, 'construye_bloques3.py'): '5532f1c1fddbb624',
        MOTOR: 'd0a620d2f5e2605e'}
VIDA = 2270
PER = {'P6k': 6000, 'P22k': 22000, 'P68k': 68000, 'Pinf': 0}
MODO = {'FIJO_V': 0, 'PLAST_V': 1, 'PLAST_AZA': 2, 'PLAST_RW0': 3}
ORDEN = ('PLAST_V_P22k', 'FIJO_V_P22k', 'PLAST_AZA_P22k', 'PLAST_RW0_P22k', 'PLAST_V_P6k', 'FIJO_V_P6k', 'PLAST_V_P68k', 'FIJO_V_P68k',
         'PLAST_V_Pinf', 'FIJO_V_Pinf')
T_DEF = 500000   # PREREGISTRO sec. 4 y 13: costo proyectado por el humo con pool 2 <= 2 h -> 500 000 (el de BLOQUES)
T_CORTE = 100000
T_HUMO = 200000
SERIE = tuple(range(56401, 56421)); REPLICA = tuple(range(56421, 56441)); ARNES = (56491, 56492, 56493, 56494); HUMO_S = 56495
HUMO2_S = (56496, 56497, 56498)   # AUDITORIA H-6 (29-sep, antes de datos): 2o humo DECLARADO, no cuenta: PLAST_V_Pinf y FIJO_V_Pinf
HUMO2 = ('PLAST_V_Pinf', 'FIJO_V_Pinf')
HUMO = ('FIJO_V_Pinf', 'PLAST_V_Pinf', 'PLAST_V_P22k', 'FIJO_V_P22k', 'PLAST_AZA_P22k', 'PLAST_RW0_P22k')   # 6 corridas, un proceso
POOL_MAX = 2
DEF = dict(CB.DEF, inv=0, inv_cada=20000, plast=0, p_bit=0.01, p_ins_pl=0.5, forzada_bit=None)
# umbrales de la letra (sec. 6)
PERS_PL = 15; PERS_FIJO = 5; MARGEN_CTL = 5; FRAC_ALTA = 0.5; FRAC_BAJA = 0.2; N_FRAC = 15; ANCLA_FIJO = 15; AZA_BANDA = (0.3, 0.7); N_V5 = 8; N_DISC_MIN = 10


def cfg_de(brazo):
    arm, cond = brazo.rsplit('_', 1)
    P = PER[cond]
    return dict(on=1, donante='padre', inv=(1 if P else 0), inv_cada=(P if P else 20000), plast=MODO[arm], p_bit=DEF['p_bit'],
                p_ins_pl=DEF['p_ins_pl'], forzada_bit=None)


for _b in ORDEN:
    NS.BRAZOS[_b] = ('MUT0', CB.FAB, T_CORTE)
    CB.BQ[_b] = cfg_de(_b)


def h16(p):
    return hashlib.sha256(open(p, 'rb').read()).hexdigest()[:16]


def usa_baldwin():
    """Como corre_bloques.usa_bloques, con motor_baldwin."""
    import motor_baldwin as MB
    g = types.ModuleType('motor_baldwin_gemelo')
    g.__dict__.update({k: v for k, v in NS.ME_PY.__dict__.items() if not k.startswith('__')})

    def _rs(*a, **k):
        r = MB.run_solapadas(*a, **k); P = r['pista']
        CB.MUNDO_ULT.clear(); CB.MUNDO_ULT.update(comp_mundo=P['comp_mundo'], nobj_medio=P['nobj_medio'], llegadas=P['llegadas'],
                                                  perdidas=P['llegadas_perdidas'])
        return r
    g.run_solapadas = _rs
    g._MF = MB
    NS.CR.ME = g
    return MB


CB.usa_bloques = usa_baldwin   # corre_bloques.corre busca usa_bloques en su modulo al llamarse


def verifica(log=print):
    ok = True
    for ruta, sha in SHAS.items():
        s = h16(ruta); ok &= s == sha; log(f"  sha {os.path.relpath(ruta, RAIZ)} {s} {'OK' if s == sha else '!= ' + sha + ' FALLA'}")
    try:
        CB.verifica(); log("  corre_bloques.verifica (nucleo_eco_sel_ing, motor_frio_rapido, motor_bloques): OK")
    except SystemExit as e:
        ok = False; log(f"  corre_bloques.verifica FALLA: {e}")
    igual = open(MOTOR, encoding='utf-8').read() == KB.construye()
    ok &= igual; log(f"  motor_baldwin.py == construye_baldwin.construye() por anclas desde motor_bloques3: {'OK' if igual else 'FALLA'}")
    return ok


# ------------------------------------------------------------------ medidas de la plasticidad (del JSON)
def es_boca(r): return int(r[4]) == 0


def discrimina(r):
    return int(r[0]) == 3 and es_boca(r) and 0 < sum(1 for x in 'ABCD' if ((CB.PATM[x][int(r[1])] > r[3]) if r[2] > 0.5 else (CB.PATM[x][int(r[1])] < r[3]))) < 4


def medidas(o):
    """frac_pl = fraccion de reglas PLASTICAS entre las reglas de boca que discriminan letras (pixel del foco; se cumplen en 1-3 de las 4)
    de los cuerpos vivos en T (MEDIDA PRINCIPAL); frac_pl_boca = entre todas las de boca. None si no hay vivos o no hay tales reglas."""
    B = o.get('bloques') or {}
    vv = B.get('vivos_T') or []; pl = B.get('vivos_T_pl')
    m = dict(frac_pl=None, frac_pl_boca=None, n_disc=0, n_boca=0, dw_med=None, n_aprende=B.get('n_aprende'),
             n_mord_aprende=B.get('n_mord_aprende'), n_inv=B.get('n_inv'), n_flip=B.get('n_flip'), vivos_T=len(vv))
    sp = B.get('serie_pl') or []   # AUDITORIA H-1 / punto 3: el bit EN EL TIEMPO (antes de la extincion), no solo en T
    ult = [x for x in sp if x[3] is not None and x[4] >= N_DISC_MIN]; ultb = [x for x in sp if x[2] is not None]   # ultimo dato con >= 10 reglas
    m.update(frac_pl_ult=(ult[-1][3] if ult else None), t_frac_pl_ult=(ult[-1][0] if ult else None), frac_pl_boca_ult=(ultb[-1][2] if ultb else None),
             frac_pl_t={str(x[0]): x[3] for x in sp if x[0] % 50000 == 0}, dw_t={str(x[0]): x[5] for x in sp if x[0] % 50000 == 0})
    if not vv or pl is None: return m
    nd = ndp = nb = nbp = 0; dw = []
    for x, bits in zip(vv, pl):
        for r, (bt, w0) in zip(x[3], bits):
            if not es_boca(r): continue
            nb += 1; nbp += bt
            if bt: dw.append(abs(r[5] - w0))
            if discrimina(r): nd += 1; ndp += bt
    m.update(frac_pl=(round(ndp / nd, 4) if nd else None), frac_pl_boca=(round(nbp / nb, 4) if nb else None), n_disc=nd, n_boca=nb,
             dw_med=(round(float(np.median(dw)), 4) if dw else None))
    return m


def corre(seed, brazo, T, carpeta, extra=None, reanuda=False):
    """corre_bloques.corre (la entrada de BLOQUES, intacta) + el bloque 'baldwin' y la cfg del worker."""
    o = CB.corre(seed, brazo, T, carpeta, extra=extra, reanuda=reanuda)
    if 'baldwin' in o: return o
    o['cfg_worker'] = (o.get('bloques') or {}).get('cfg')   # la BQ_CFG que el motor registro al arrancar (viaja en el checkpoint)
    o['baldwin'] = medidas(o)
    fn = os.path.join(carpeta, f'M_{brazo}_s{seed}.json')
    with open(fn + '.tmp', 'w', encoding='utf-8') as f: json.dump(o, f)
    os.replace(fn + '.tmp', fn)
    return o


def trabajo(a):
    seed, brazo, T, car, rean = a
    t0 = time.time()
    try:
        o = corre(seed, brazo, T, car, reanuda=rean)
    except KeyboardInterrupt:
        raise
    except BaseException as ex:   # nunca matar al trabajador del Pool: la serie queda NO SE LEE por V0
        o = dict(seed=seed, brazo=brazo, T=T, aborto=f'{type(ex).__name__}: {ex}', K=None, persiste=None, bloqueados=None)
    o['_seg_job'] = round(time.time() - t0, 1)
    return o


def carga(carpeta):
    R = {b: {} for b in ORDEN}; ab = []
    for f in sorted(glob.glob(os.path.join(carpeta, 'M_*_s*.json'))):
        d = json.load(open(f, encoding='utf-8'))
        if d.get('brazo') not in R: continue
        if d.get('aborto'): ab.append(f"{d['brazo']} s{d['seed']}: {d['aborto']}")
        else: R[d['brazo']][d['seed']] = d
    return R, ab


def med(v):
    v = [x for x in v if x is not None]
    return round(float(np.median(v)), 4) if v else None


# ------------------------------------------------------------------ LA LETRA (PREREGISTRO_baldwin.md sec. 6)
def lee(carpeta, semillas, humo=False, T=None, log=print):
    R, ab = carga(carpeta); sem = list(semillas); n = len(sem)
    brs = [b for b in ORDEN if (not humo) or R[b]]
    completa = all(s in R[b] for b in brs for s in sem)
    if not completa:
        log(f"  INCOMPLETA: faltan {[(b, s) for b in brs for s in sem if s not in R[b]][:12]} · abortos {ab[:5]}")
        return dict(veredicto='NO SE LEE', abortos=ab)
    X = lambda b, s: R[b][s]
    Bm = lambda b, s: X(b, s).get('baldwin') or {}
    pers = {b: sum(1 for s in sem if X(b, s).get('persiste')) for b in brs}
    fr = {b: [Bm(b, s).get('frac_pl') for s in sem] for b in brs}
    esc = (lambda k: max(1, round(k * n / 20))) if humo else (lambda k: k)
    v = {}
    Tt = T or X(brs[0], sem[0]).get('T')
    v['V0_completa_sin_abortos'] = bool(not ab and all(X(b, s).get('T') == Tt and X(b, s).get('t_corte') == T_CORTE and X(b, s).get('bloqueados') == 0
                                                       for b in brs for s in sem) and (humo or n == 20))
    v['V1_ancla_FIJO_Pinf_persiste'] = pers.get('FIJO_V_Pinf', 0) >= esc(ANCLA_FIJO)

    def cfg_ok(b, s):
        c = X(b, s).get('cfg_worker') or {}; e = cfg_de(b)
        return all(c.get(k) == e[k] for k in e) and c.get('kit', 1) == 1 and c.get('p_bit') == DEF['p_bit'] and c.get('p_ins_pl') == DEF['p_ins_pl']
    v['V2_cfg_por_brazo'] = all(cfg_ok(b, s) for b in brs for s in sem)

    def inv_ok(b, s):
        ni = Bm(b, s).get('n_inv'); P = PER[b.rsplit('_', 1)[1]]
        return (not ni) if P == 0 else (ni is not None and ni >= 1)
    v['V3_inversiones'] = all(inv_ok(b, s) for b in brs for s in sem)
    na = [Bm('PLAST_V_P22k', s).get('n_aprende') or 0 for s in sem] if 'PLAST_V_P22k' in brs else []
    v['V4_la_pieza_actua'] = (humo and not na) or sum(1 for x in na if x > 0) >= esc(18)   # en humo2 no hay PLAST_V_P22k: no aplica
    # AUDITORIA H-1: V5 sobre el ULTIMO dato de serie_pl (el bit antes de la extincion), no sobre los vivos en T. Con menos de 8 semillas con
    # dato, V5 'no aplica' (cuenta como cumplida) y el control AZA decide solo por PB.
    faza = [Bm('PLAST_AZA_P22k', s).get('frac_pl_ult') for s in sem] if 'PLAST_AZA_P22k' in brs else []
    faza = [x for x in faza if x is not None]
    v5_aplica = len(faza) >= esc(N_V5)
    v['V5_AZA_bit_al_azar'] = (not v5_aplica) or (AZA_BANDA[0] <= float(np.median(faza)) <= AZA_BANDA[1])
    v5_nota = (f"aplica: mediana {med(faza)} en {len(faza)} semillas" if v5_aplica else f"NO APLICA ({len(faza)} semillas con dato < {esc(N_V5)}): decide PB")
    valido = all(v.values())
    g = esc(N_FRAC)
    p = {}
    p['PA_rescate'] = pers.get('PLAST_V_P22k', 0) >= esc(PERS_PL) and pers.get('FIJO_V_P22k', 99) <= (esc(PERS_FIJO) if humo else PERS_FIJO)
    p['PB_controles'] = (pers.get('PLAST_V_P22k', 0) >= pers.get('PLAST_AZA_P22k', 99) + esc(MARGEN_CTL)
                         and pers.get('PLAST_V_P22k', 0) >= pers.get('PLAST_RW0_P22k', 99) + esc(MARGEN_CTL))
    p['PD_seleccion_prende'] = sum(1 for x in fr.get('PLAST_V_P22k', []) if x is not None and x >= FRAC_ALTA) >= g
    p['PE_seleccion_apaga'] = sum(1 for x in fr.get('PLAST_V_Pinf', []) if x is not None and x <= FRAC_BAJA) >= g
    if not valido: ver = 'NO SE LEE'
    elif all(p.values()): ver = 'FUNCIONA'
    elif (p['PA_rescate'] and p['PB_controles']) or (p['PD_seleccion_prende'] and p['PE_seleccion_apaga']): ver = 'HAY ALGO MODESTO'
    else: ver = 'NO'
    # --- secundarias (NO deciden; sec. 7)
    curva = {c: med(fr.get(f'PLAST_V_{c}', [])) for c in PER if f'PLAST_V_{c}' in brs}
    par = {}
    for a, b, k in (('PLAST_V_P22k', 'PLAST_V_Pinf', 'frac_pl'), ('PLAST_V_P6k', 'PLAST_V_P68k', 'frac_pl'),
                    ('PLAST_V_P22k', 'PLAST_RW0_P22k', 'frac_pl'), ('PLAST_V_P22k', 'FIJO_V_P22k', 'K'), ('PLAST_V_Pinf', 'FIJO_V_Pinf', 'K'),
                    ('PLAST_V_P6k', 'FIJO_V_P6k', 'K'), ('PLAST_V_P68k', 'FIJO_V_P68k', 'K'), ('PLAST_V_P22k', 'FIJO_V_P22k', 't_ext')):
        if a in brs and b in brs:
            if k == 'frac_pl': xa = [Bm(a, s).get(k) for s in sem]; xb = [Bm(b, s).get(k) for s in sem]
            elif k == 't_ext': xa = [X(a, s).get('t_ext') or Tt for s in sem]; xb = [X(b, s).get('t_ext') or Tt for s in sem]
            else: xa = [X(a, s).get(k) for s in sem]; xb = [X(b, s).get(k) for s in sem]
            dd = [x - y for x, y in zip(xa, xb) if x is not None and y is not None]
            par[f'{a}-{b}[{k}]'] = dict(gana=sum(1 for d in dd if d > 0), n=len(dd), dif_med=med(dd))
    sec = dict(curva_frac_pl_por_P=curva, pareados=par,
               D1_curva_baja_con_P=(curva.get('P6k') is not None and curva.get('P68k') is not None and curva['P6k'] > curva['P68k']),
               RW0_frac_alta=sum(1 for x in fr.get('PLAST_RW0_P22k', []) if x is not None and x >= FRAC_ALTA))
    # --- impresion
    log(f"\n================ LECTURA ({PRERREGISTRO} sec. 6-7) · {carpeta} · VIDA {VIDA} · P/vida " +
        ' '.join(f"{c} {(PER[c] / VIDA if PER[c] else float('inf')):.1f}" for c in PER))
    log(f"{'brazo':15s} {'persiste':>8s} {'K med':>7s} {'t_ext med':>9s} {'frac_pl med':>11s} {'frac_boca':>9s} {'n_disc':>6s} {'|w-w0|':>7s} {'aprende':>9s} {'n_inv':>5s} {'vida2a':>7s} {'seg':>6s}")
    for b in brs:
        xs = [X(b, s) for s in sem]; bs = [Bm(b, s) for s in sem]
        log(f"{b:15s} {str(pers[b]) + '/' + str(n):>8s} {med([x.get('K') for x in xs])!s:>7s} {med([x.get('t_ext') for x in xs])!s:>9s} "
            f"{med(fr[b])!s:>11s} {med([y.get('frac_pl_boca') for y in bs])!s:>9s} {med([y.get('n_disc') for y in bs])!s:>6s} "
            f"{med([y.get('dw_med') for y in bs])!s:>7s} {med([y.get('n_aprende') for y in bs])!s:>9s} {med([y.get('n_inv') for y in bs])!s:>5s} "
            f"{med([x.get('vida_media_muertos_2a') for x in xs])!s:>7s} {med([x.get('seg') for x in xs])!s:>6s}")
    for b in brs:
        if b.startswith('PLAST'): log(f"  frac_pl por semilla {b}: {fr[b]}")
    log("  DESCRIPTIVO (punto 3 del auditor): frac_pl EN EL TIEMPO (mediana entre semillas con dato, n) y el ultimo dato antes de extinguirse")
    tiempos = [str(t_) for t_ in range(50000, (Tt or 0) + 1, 50000)]
    tiempo = {}
    for b in brs:
        if not b.startswith('PLAST'): continue
        fila = {t_: (med([(Bm(b, s).get('frac_pl_t') or {}).get(t_) for s in sem]),
                     sum(1 for s in sem if (Bm(b, s).get('frac_pl_t') or {}).get(t_) is not None)) for t_ in tiempos}
        ul = [Bm(b, s).get('frac_pl_ult') for s in sem]
        tiempo[b] = dict(t=fila, ult=ul)
        log(f"  {b:15s} " + ' '.join(f"{int(t_) // 1000}k:{fila[t_][0]}({fila[t_][1]})" for t_ in tiempos) + f" · ultimo por semilla {ul}")
    sec['frac_pl_tiempo'] = tiempo
    log(f"  pareados (secundarios): {par}")
    log(f"  curva frac_pl (mediana) por P: {curva}")
    log(f"\n  VALIDEZ {v} · V5 {v5_nota}\n  PUERTAS {p}\n  SECUNDARIAS {dict((k, x) for k, x in sec.items() if k != 'pareados')}")
    log(f"  VEREDICTO {'(HUMO, no cuenta) ' if humo else ''}{ver}")
    return dict(validez=v, v5_nota=v5_nota, puertas=p, secundarias=sec, veredicto=ver, persiste=pers, frac_pl=fr, abortos=ab, n=n, humo=humo)


ORDV = {'NO SE LEE': -1, 'NO': 0, 'HAY ALGO MODESTO': 1, 'FUNCIONA': 2}


def bloque(a, b):
    return a if a == b else min((a, b), key=lambda z: ORDV[z])


# ------------------------------------------------------------------ candados
def git_limpio(rutas, log):
    ok = True
    for r in rutas:
        rel = os.path.relpath(r, RAIZ).replace('\\', '/')
        try:
            t = subprocess.run(['git', '-C', RAIZ, 'ls-files', '--error-unmatch', rel], capture_output=True, text=True).returncode == 0
            c = subprocess.run(['git', '-C', RAIZ, 'diff', '--quiet', 'HEAD', '--', rel], capture_output=True, text=True).returncode == 0
            h = subprocess.run(['git', '-C', RAIZ, 'log', '-1', '--format=%h %cI', '--', rel], capture_output=True, text=True).stdout.strip()
        except Exception as e:   # noqa
            t = c = False; h = str(e)
        ok &= t and c; log(f"  git {rel}: commiteado {t} · sin cambios vs HEAD {c} · ultimo commit {h}")
    return ok


def guarda(pre, reanuda):
    """Si ya hay un resumen.json (no humo) con veredicto: se niega siempre. Si hay carpetas previas (cortadas o NO SE LEE): solo --reanuda."""
    previas = sorted(d for d in glob.glob(os.path.join(DATOS, pre + '_*')) if os.path.isdir(d))
    for d in previas:
        rj = os.path.join(d, 'resumen.json')
        if os.path.exists(rj):
            r = json.load(open(rj, encoding='utf-8'))
            if not r.get('humo') and (r.get('letra') or {}).get('veredicto') in ('FUNCIONA', 'HAY ALGO MODESTO', 'NO'):
                return f"{os.path.relpath(rj, RAIZ)} ya tiene veredicto {r['letra']['veredicto']}: no se re-corre"
    if previas and not reanuda: return f"ya existe {os.path.relpath(previas[-1], RAIZ)}: solo --reanuda (cortada o NO SE LEE)"
    return None


def candado(carpeta, reanuda):
    """Un solo lanzamiento por carpeta: EN_CURSO.lock se crea en exclusiva. Con --reanuda se reescribe (el coordinador asegura que el
    proceso anterior ya no corre: nunca se matan procesos)."""
    lk = os.path.join(carpeta, 'EN_CURSO.lock')
    if os.path.exists(lk) and reanuda: os.remove(lk)   # candado viejo de una corrida cortada: solo con --reanuda
    try:   # AUDITORIA H-5: creacion EXCLUSIVA (atomica): dos lanzamientos simultaneos no pueden tener el candado a la vez
        fd = os.open(lk, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
    except FileExistsError:
        return None, f"{lk} existe: otro lanzamiento en curso o cortado (usa --reanuda si esta cortado)"
    with os.fdopen(fd, 'w', encoding='utf-8') as f: f.write(f"pid {os.getpid()} · {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
    return lk, None


def main(argv=None):
    ap = argparse.ArgumentParser(allow_abbrev=False)
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument('--humo', action='store_true'); g.add_argument('--humo2', action='store_true'); g.add_argument('--serie', action='store_true'); g.add_argument('--replica', action='store_true')
    g.add_argument('--bloque', default=None); g.add_argument('--lee', default=None)
    ap.add_argument('--pool', type=int, default=0); ap.add_argument('--reanuda', action='store_true')
    a = ap.parse_args(argv)   # ERR-115: nunca parse_known_args
    if a.pool < 0 or a.pool > POOL_MAX: raise SystemExit(f"--pool entre 0 y {POOL_MAX} (contrato del encargo)")
    yo = h16(os.path.abspath(__file__))
    if a.bloque:
        rs = [json.load(open(x.strip(), encoding='utf-8')) for x in a.bloque.split(',')]
        if len(rs) != 2: raise SystemExit("--bloque: <resumen serie>,<resumen replica>")
        if not (rs[0]['semillas'][0] == SERIE[0] and rs[1]['semillas'][0] == REPLICA[0]) or rs[0]['humo'] or rs[1]['humo']:
            raise SystemExit(f"--bloque: primero la serie {SERIE[0]}-{SERIE[-1]} y luego la replica {REPLICA[0]}-{REPLICA[-1]} (no humo)")
        if any(r.get('sha_runner') != yo for r in rs):
            raise SystemExit(f"--bloque: sha_runner de los resumenes {[r.get('sha_runner') for r in rs]} != runner actual {yo}")
        va, vb = rs[0]['letra']['veredicto'], rs[1]['letra']['veredicto']
        print(f"serie {va} · replica {vb} -> BLOQUE: {bloque(va, vb)}  ({PRERREGISTRO} sec. 8)")
        return 0
    if a.lee:
        c = os.path.abspath(a.lee); sems = sorted({json.load(open(f, encoding='utf-8'))['seed'] for f in glob.glob(os.path.join(c, 'M_*_s*.json'))})
        humo = not (sems == list(SERIE) or sems == list(REPLICA))
        L = lee(c, sems, humo=humo); print(f"VEREDICTO ({'HUMO, no cuenta' if humo else 'letra'}): {L['veredicto']}"); return 0
    if a.humo2:   # 2o humo (auditoria H-6): 3 semillas x 2 brazos = 6 corridas, un proceso
        if a.pool: raise SystemExit("--humo2: sin Pool (un proceso)")
        a.humo = True
        tareas = [(s, b) for s in HUMO2_S for b in HUMO2]; T = T_HUMO; semillas = list(HUMO2_S); pre = f"humo2_s{HUMO2_S[0]}-{HUMO2_S[-1]}_T{T}"
    elif a.humo:
        if a.pool: raise SystemExit("--humo: sin Pool (un proceso)")
        tareas = [(HUMO_S, b) for b in HUMO]; T = T_HUMO; semillas = [HUMO_S]; pre = f"humo_s{HUMO_S}_T{T}"
    else:
        semillas = list(SERIE if a.serie else REPLICA); T = T_DEF
        tareas = [(s, b) for b in ORDEN for s in semillas]   # los caros (persisten) se mezclan con los baratos
        pre = f"{'serie' if a.serie else 'replica'}_s{semillas[0]}-{semillas[-1]}_T{T}"
    sel = time.strftime('%Y%m%d_%H%M%S')
    prev = sorted(d for d in os.listdir(DATOS) if d.startswith(pre + '_') and os.path.isdir(os.path.join(DATOS, d))) if os.path.isdir(DATOS) else []
    if a.reanuda and not prev: raise SystemExit(f"--reanuda: no hay carpeta {pre}_* en {DATOS}")
    carpeta = os.path.join(DATOS, prev[-1]) if (a.reanuda and prev) else os.path.join(DATOS, pre + '_' + sel)
    BUF = []; LOGF = [None]

    def log(s=''):
        print(s, flush=True)
        if LOGF[0] is None: BUF.append(s)
        else: LOGF[0].write(s + '\n'); LOGF[0].flush()

    t0 = time.time()
    log(f"CORRE_BALDWIN · {pre} · {sel} · python {platform.python_version()} · pool {a.pool or 'NO (un proceso)'} · corre_baldwin.py {yo} · "
        f"preregistro {PRERREGISTRO} {h16(os.path.join(AQUI, PRERREGISTRO)) if os.path.exists(os.path.join(AQUI, PRERREGISTRO)) else 'NO EXISTE'} · carpeta {carpeta}")
    log(f"  tareas {len(tareas)} · brazos {sorted(set(b for _, b in tareas), key=ORDEN.index)} · semillas {semillas[0]}-{semillas[-1]} · T {T} · "
        f"t_corte {T_CORTE} · VIDA {VIDA} · P {PER} · reanuda {a.reanuda}")
    if not a.humo:
        e = guarda(pre, a.reanuda)
        if e: log(f"  NO SE CORRE: {e}"); return 1
    if a.replica:
        rsm = sorted(glob.glob(os.path.join(DATOS, f"serie_s{SERIE[0]}-{SERIE[-1]}_T{T_DEF}_*", 'resumen.json')))
        rs0 = json.load(open(rsm[-1], encoding='utf-8')) if rsm else {}
        vs = (rs0.get('letra') or {}).get('veredicto')
        if vs not in ('FUNCIONA', 'HAY ALGO MODESTO'):
            log(f"  REGLA DE PARADA (sec. 8): la replica solo se corre si la serie da FUNCIONA o HAY ALGO MODESTO; serie = {vs}. No se corre."); return 1
        if rs0.get('sha_runner') != yo:
            log(f"  NO SE CORRE: sha_runner de la serie {rs0.get('sha_runner')} != runner actual {yo}"); return 1
    ok = verifica(log)
    if not a.humo: ok &= git_limpio([os.path.join(AQUI, PRERREGISTRO), os.path.abspath(__file__), MOTOR, os.path.join(AQUI, 'construye_baldwin.py')], log)
    if not ok: log("  ALGO FALLA -> no se corre (no se crea carpeta)."); return 1
    os.makedirs(carpeta, exist_ok=True)
    lk, e = candado(carpeta, a.reanuda)
    if e: log(f"  NO SE CORRE: {e}"); return 1
    LOGF[0] = open(os.path.join(carpeta, 'log.txt'), 'a', encoding='utf-8'); LOGF[0].write('\n'.join(BUF) + '\n'); LOGF[0].flush()
    args = [(s, b, T, carpeta, a.reanuda) for s, b in tareas]

    def fmt(x, k):
        bm = x.get('baldwin') or {}
        return (f"  [{time.strftime('%H:%M:%S')}] [{k}/{len(args)}] [{time.time() - t0:7.1f}s] {x['brazo']:15s} s{x['seed']} ({x.get('_seg_job')}s) "
                f"persiste {x.get('persiste')} K {x.get('K')} t_ext {x.get('t_ext')} frac_pl {bm.get('frac_pl')} aprende {bm.get('n_aprende')} "
                f"n_inv {bm.get('n_inv')} vida2a {x.get('vida_media_muertos_2a')} aborto {x.get('aborto')}")
    if a.pool and a.pool > 1:
        from multiprocessing import Pool
        with Pool(a.pool) as PL:
            for k, x in enumerate(PL.imap_unordered(trabajo, args), 1): log(fmt(x, k))
    else:
        for k, ar in enumerate(args, 1): log(fmt(trabajo(ar), k))
    letra = lee(carpeta, semillas, humo=a.humo, T=T, log=log)
    ver = ('HUMO (no cuenta): ' if a.humo else '') + letra['veredicto']
    rj = os.path.join(carpeta, 'resumen.json')
    with open(rj, 'w', encoding='utf-8') as fh:
        json.dump(dict(letra=letra, semillas=semillas, T=T, humo=a.humo, veredicto=ver, preregistro=PRERREGISTRO,
                       sha_preregistro=(h16(os.path.join(AQUI, PRERREGISTRO)) if os.path.exists(os.path.join(AQUI, PRERREGISTRO)) else None),
                       sha_runner=yo, shas={os.path.relpath(k, RAIZ): v for k, v in SHAS.items()}), fh, ensure_ascii=False, indent=1, default=float)
    log(f"\n  RESUMEN {rj} (sha {h16(rj)})\nTerminado en {time.time() - t0:.1f}s")
    log(f"VEREDICTO DE LA {'CORRIDA' if a.humo else ('SERIE' if a.serie else 'REPLICA')}: {ver}   (regla de parada: {PRERREGISTRO} sec. 8)")
    LOGF[0].close()
    if lk and os.path.exists(lk): os.remove(lk)
    return 0


if __name__ == '__main__':
    sys.exit(main())
