"""corre_bexp.py — RUNNER y LETRA de BALDWIN CON EXPLORACION. Preregistro: PREREGISTRO_baldwin_exp.md (la letra esta AQUI, en lee(), y
alli en la sec. 6).

MISION: llegar a la AGI por este camino (organismo minimo con reglas locales, sin retropropagacion, peldanos preregistrados con
controles y replicas).

HIPOTESIS NUEVA (no rescate del NO de BALDWIN, commit 43f1a6df): la regla plastica de BALDWIN solo aprende tras morder, y una regla de
rechazo (w ~ -2.5) inhibe la mordida: nunca recibe la consecuencia y no se entera de la inversion. Si el cuerpo PRUEBA de vez en cuando
lo que sus reglas rechazan (exploracion local ligada a la reserva: 'prueba solo si aguanta el golpe'), la plasticidad rescata al linaje
en el mundo que cambia y la seleccion prende el bit plastico.

ENTRADA (regla 14): cada corrida ES corre_bloques.corre (experimentos/organelos/bloques/opusM/corre_bloques.py, sha a090b82eae9f1ee3, se
IMPORTA y no se toca) con su gemelo cambiado a motor_bexp (construido por anclas desde motor_baldwin, sha d0a620d2f5e2605e; exp = 0 ==
motor_baldwin bit a bit: arnes identidad_bexp.py). Lo unico agregado al JSON: 'baldwin' (medidas de BALDWIN, mismas expresiones),
'bexp' (medidas de la exploracion) y 'cfg_worker' (la BQ_CFG que el worker uso de verdad).

MUNDO: el de BALDWIN (ECO w90, FABRICA_ECO, vivero finito t_corte 100 000, MUT0 + reglas heredables kit 1). Inversion A<->B, C<->D cada
22 000 pasos (P/vida 9.7, el caso central) o ninguna (Pinf).

BRAZOS (plast: 0 fijo, 1 bit heredable, 2 bit sorteado al nacer; exp: 0 sin exploracion, 1 con exploracion):
  P22k: PLAST_EXP (1,1) candidato · FIJO_EXP (0,1) ¿basta con explorar? · PLAST_EXP_AZA (2,1) bit sin herencia · PLAST_V (1,0) referencia
  Pinf: PLAST_EXP (1,1) la puerta 'apaga' (secundaria) · FIJO_V (0,0) ancla de validez                  (6 brazos x 20 = 120 corridas)

SEMILLAS NUEVAS (grep 29-sep en PROYECTOS/JUACO, .py/.md/.txt fuera de datos y .git: 566xx no aparece): serie 56601-56620 ·
replica 56621-56640 · calibracion 56681-56682 · arnes 56691-56694 · humo 56695.

Uso (banderas desconocidas o abreviadas ABORTAN, ERR-115; --serie/--replica SOLO el coordinador, con preregistro, runner, motor y
constructor commiteados y sin cambios respecto de HEAD):
  python experimentos/organelos/baldwin_exp/corre_bexp.py --humo                 # 1 proceso, 6 corridas, s56695, T 200 000; escribe JSON
  python experimentos/organelos/baldwin_exp/corre_bexp.py --serie --pool 2       # 120 corridas; se niega si ya hay veredicto
  python experimentos/organelos/baldwin_exp/corre_bexp.py --serie --pool 2 --reanuda
  python experimentos/organelos/baldwin_exp/corre_bexp.py --replica --pool 2     # solo si la serie da FUNCIONA o HAY ALGO MODESTO
  python experimentos/organelos/baldwin_exp/corre_bexp.py --lee <carpeta>
  python experimentos/organelos/baldwin_exp/corre_bexp.py --bloque <resumen serie>.json,<resumen replica>.json
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
import corre_bloques as CB   # noqa: E402  (se IMPORTA, no se toca)
import construye_bexp as KX   # noqa: E402  (solo construye(): no escribe nada)
NS = CB.NS
USA_BLOQUES_ORIGINAL = CB.usa_bloques

PRERREGISTRO = 'PREREGISTRO_baldwin_exp.md'
DATOS = os.path.join(AQUI, 'datos')
MOTOR = os.path.join(AQUI, 'motor_bexp.py')
SHAS = {os.path.join(OPUSM, 'corre_bloques.py'): 'a090b82eae9f1ee3', os.path.join(ORG, 'baldwin', 'motor_baldwin.py'): 'd0a620d2f5e2605e',
        os.path.join(ORG, 'baldwin', 'construye_baldwin.py'): 'c9cad63496519fb7', MOTOR: '0af10809633c945d'}
VIDA = 2270
PER = {'P22k': 22000, 'Pinf': 0}
MODO = {'FIJO_V': (0, 0), 'PLAST_V': (1, 0), 'FIJO_EXP': (0, 1), 'PLAST_EXP': (1, 1), 'PLAST_EXP_AZA': (2, 1)}   # (plast, exp)
ORDEN = ('PLAST_EXP_P22k', 'FIJO_EXP_P22k', 'PLAST_EXP_AZA_P22k', 'PLAST_V_P22k', 'PLAST_EXP_Pinf', 'FIJO_V_Pinf')
# EXPLORACION (PREREGISTRO sec. 2 y 4): th_exp = |peor efecto de una mordida| + 0.1 = 0.5 (fijado a priori); eps_exp CALIBRADO por la
# regla de la sec. 4 (calibra_bexp.py, exploracion APAGADA, antes de toda corrida con exploracion): eps = 4 / (vetos con reserva por vida).
TH_EXP = 0.5
EPS_EXP = 0.063   # calibra_bexp.py (sha 7c1e9f4b2e8e5b05), calibra_salida.txt: 4 / 63.5063 -> 0.063; fijado ANTES del humo
T_DEF = 500000
T_CORTE = 100000
T_HUMO = 200000
SERIE = tuple(range(56601, 56621)); REPLICA = tuple(range(56621, 56641)); CALIBRA = (56681, 56682); ARNES = (56691, 56692, 56693, 56694)
HUMO_S = 56695
HUMO = ORDEN   # 6 corridas, un proceso
POOL_MAX = 2
DEF = dict(CB.DEF, inv=0, inv_cada=20000, plast=0, p_bit=0.01, p_ins_pl=0.5, forzada_bit=None, exp=0, eps_exp=0.0, th_exp=TH_EXP)
# umbrales de la letra (sec. 6)
PERS_PL = 15; PERS_FIJO = 5; MARGEN = 5; FRAC_ALTA = 0.5; FRAC_BAJA = 0.2; N_FRAC = 15; ANCLA_FIJO = 13; N_ACTUA = 18   # ERR-156 H-2: V1 baja de 15 a 13 (decision del coordinador, antes de datos)
AZA_BANDA = (0.3, 0.7); N_V6 = 8; N_DISC_MIN = 10


def cfg_de(brazo, eps=None):
    arm, cond = brazo.rsplit('_', 1)
    P = PER[cond]; pl, ex = MODO[arm]
    e = EPS_EXP if eps is None else eps
    return dict(on=1, donante='padre', inv=(1 if P else 0), inv_cada=(P if P else 20000), plast=pl, p_bit=DEF['p_bit'],
                p_ins_pl=DEF['p_ins_pl'], forzada_bit=None, exp=ex, eps_exp=(float(e) if (ex and e is not None) else 0.0), th_exp=TH_EXP)


def registra(eps=None):
    for _b in ORDEN:
        NS.BRAZOS[_b] = ('MUT0', CB.FAB, T_CORTE)
        CB.BQ[_b] = cfg_de(_b, eps)


registra()


def h16(p):
    return hashlib.sha256(open(p, 'rb').read()).hexdigest()[:16]


def usa_bexp():
    """Como corre_bloques.usa_bloques, con motor_bexp."""
    import motor_bexp as MX
    g = types.ModuleType('motor_bexp_gemelo')
    g.__dict__.update({k: v for k, v in NS.ME_PY.__dict__.items() if not k.startswith('__')})

    def _rs(*a, **k):
        r = MX.run_solapadas(*a, **k); P = r['pista']
        CB.MUNDO_ULT.clear(); CB.MUNDO_ULT.update(comp_mundo=P['comp_mundo'], nobj_medio=P['nobj_medio'], llegadas=P['llegadas'],
                                                  perdidas=P['llegadas_perdidas'])
        return r
    g.run_solapadas = _rs
    g._MF = MX
    NS.CR.ME = g
    return MX


CB.usa_bloques = usa_bexp   # corre_bloques.corre busca usa_bloques en su modulo al llamarse


def verifica(log=print):
    ok = True
    for ruta, sha in SHAS.items():
        s = h16(ruta); ok &= s == sha; log(f"  sha {os.path.relpath(ruta, RAIZ)} {s} {'OK' if s == sha else '!= ' + sha + ' FALLA'}")
    try:
        CB.verifica(); log("  corre_bloques.verifica (nucleo_eco_sel_ing, motor_frio_rapido, motor_bloques): OK")
    except SystemExit as e:
        ok = False; log(f"  corre_bloques.verifica FALLA: {e}")
    igual = open(MOTOR, encoding='utf-8').read() == KX.construye()
    ok &= igual; log(f"  motor_bexp.py == construye_bexp.construye() por anclas desde motor_baldwin: {'OK' if igual else 'FALLA'}")
    ok &= EPS_EXP is not None; log(f"  EPS_EXP calibrado: {EPS_EXP}")
    return ok


# ------------------------------------------------------------------ medidas (del JSON)
def es_boca(r): return int(r[4]) == 0


def discrimina(r):
    return int(r[0]) == 3 and es_boca(r) and 0 < sum(1 for x in 'ABCD' if ((CB.PATM[x][int(r[1])] > r[3]) if r[2] > 0.5 else (CB.PATM[x][int(r[1])] < r[3]))) < 4


def medidas(o):
    """Las de BALDWIN (mismas expresiones: frac_pl en los vivos en T; frac_pl_ult = ultimo dato de serie_pl con >= 10 reglas
    discriminantes) + frac_pl_fin = frac_pl si hay vivos con reglas discriminantes, si no frac_pl_ult (el bit ANTES de extinguirse)."""
    B = o.get('bloques') or {}
    vv = B.get('vivos_T') or []; pl = B.get('vivos_T_pl')
    m = dict(frac_pl=None, frac_pl_boca=None, n_disc=0, n_boca=0, dw_med=None, n_aprende=B.get('n_aprende'),
             n_mord_aprende=B.get('n_mord_aprende'), n_inv=B.get('n_inv'), n_flip=B.get('n_flip'), vivos_T=len(vv))
    sp = B.get('serie_pl') or []
    ult = [x for x in sp if x[3] is not None and x[4] >= N_DISC_MIN]; ultb = [x for x in sp if x[2] is not None]
    m.update(frac_pl_ult=(ult[-1][3] if ult else None), t_frac_pl_ult=(ult[-1][0] if ult else None), frac_pl_boca_ult=(ultb[-1][2] if ultb else None),
             frac_pl_t={str(x[0]): x[3] for x in sp if x[0] % 50000 == 0}, dw_t={str(x[0]): x[5] for x in sp if x[0] % 50000 == 0})
    if vv and pl is not None:
        nd = ndp = nb = nbp = 0; dw = []
        for x, bits in zip(vv, pl):
            for r, (bt, w0) in zip(x[3], bits):
                if not es_boca(r): continue
                nb += 1; nbp += bt
                if bt: dw.append(abs(r[5] - w0))
                if discrimina(r): nd += 1; ndp += bt
        m.update(frac_pl=(round(ndp / nd, 4) if nd else None), frac_pl_boca=(round(nbp / nb, 4) if nb else None), n_disc=nd, n_boca=nb,
                 dw_med=(round(float(np.median(dw)), 4) if dw else None))
    m['frac_pl_fin'] = m['frac_pl'] if m['frac_pl'] is not None else m['frac_pl_ult']
    return m


def medidas_exp(o):
    X = (o.get('bloques') or {}).get('exp') or {}
    mu = X.get('muertos') or {}; vi = X.get('vivos_T') or {}
    npl = (mu.get('n_reglas_pl') or 0) + (vi.get('n_reglas_pl') or 0); nmv = (mu.get('n_movidas') or 0) + (vi.get('n_movidas') or 0)
    cp = X.get('n_cuerpo_paso') or 0
    return dict(n_mord_exp=X.get('n_mord_exp'), n_mord_exp_aprende=X.get('n_mord_exp_aprende'), n_veto=X.get('n_veto'), n_veto_res=X.get('n_veto_res'),
                n_cuerpo_paso=cp, n_exp_R_pos=X.get('n_exp_R_pos'), n_exp_R_neg=X.get('n_exp_R_neg'),
                exp_por_vida=(round(X.get('n_mord_exp', 0) / cp * VIDA, 3) if cp else None),
                veto_res_por_vida=(round(X.get('n_veto_res', 0) / cp * VIDA, 3) if cp else None),
                pl_movidas=nmv, pl_reglas=npl, frac_pl_movidas=(round(nmv / npl, 4) if npl else None),
                dw_medio_muertos=(round(mu['sum_dw'] / mu['n_reglas_pl'], 4) if mu.get('n_reglas_pl') else None),
                frac_muertos_movidos=(round(mu['n_cuerpos_movidos'] / mu['n_cuerpos_pl'], 4) if mu.get('n_cuerpos_pl') else None))


def corre(seed, brazo, T, carpeta, extra=None, reanuda=False):
    """corre_bloques.corre (la entrada de BLOQUES, intacta) + 'baldwin', 'bexp' y la cfg del worker."""
    o = CB.corre(seed, brazo, T, carpeta, extra=extra, reanuda=reanuda)
    if 'bexp' in o: return o
    o['cfg_worker'] = (o.get('bloques') or {}).get('cfg')
    o['baldwin'] = medidas(o)
    o['bexp'] = medidas_exp(o)
    fn = os.path.join(carpeta, f'M_{brazo}_s{seed}.json')
    with open(fn + '.tmp', 'w', encoding='utf-8') as f: json.dump(o, f)
    os.replace(fn + '.tmp', fn)
    return o


def trabajo(a):
    seed, brazo, T, car, rean, eps = a
    t0 = time.time()
    registra(eps)   # cfg por worker: el hijo del Pool (spawn en Windows) re-importa el modulo; la cfg viaja en el argumento
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


# ------------------------------------------------------------------ LA LETRA (PREREGISTRO_baldwin_exp.md sec. 6)
def lee(carpeta, semillas, humo=False, T=None, log=print, eps=None):
    R, ab = carga(carpeta); sem = list(semillas); n = len(sem)
    eps = EPS_EXP if eps is None else eps
    brs = [b for b in ORDEN if (not humo) or R[b]]
    completa = all(s in R[b] for b in brs for s in sem)
    if not completa:
        log(f"  INCOMPLETA: faltan {[(b, s) for b in brs for s in sem if s not in R[b]][:12]} · abortos {ab[:5]}")
        return dict(veredicto='NO SE LEE', abortos=ab)
    X = lambda b, s: R[b][s]
    Bm = lambda b, s: X(b, s).get('baldwin') or {}
    Bx = lambda b, s: X(b, s).get('bexp') or {}
    pers = {b: sum(1 for s in sem if X(b, s).get('persiste')) for b in brs}
    fr = {b: [Bm(b, s).get('frac_pl_fin') for s in sem] for b in brs}
    esc = (lambda k: max(1, round(k * n / 20))) if humo else (lambda k: k)
    v = {}
    Tt = T or X(brs[0], sem[0]).get('T')
    v['V0_completa_sin_abortos'] = bool(not ab and all(X(b, s).get('T') == Tt and X(b, s).get('t_corte') == T_CORTE and X(b, s).get('bloqueados') == 0
                                                       for b in brs for s in sem) and (humo or n == 20))
    v['V1_ancla_FIJO_V_Pinf_persiste'] = pers.get('FIJO_V_Pinf', 0) >= esc(ANCLA_FIJO)

    def cfg_ok(b, s):
        c = X(b, s).get('cfg_worker') or {}; e = cfg_de(b, eps)
        return all(c.get(k) == e[k] for k in e) and c.get('kit', 1) == 1
    v['V2_cfg_por_brazo'] = all(cfg_ok(b, s) for b in brs for s in sem)

    def inv_ok(b, s):
        ni = Bm(b, s).get('n_inv') if Bm(b, s).get('n_inv') is not None else (X(b, s).get('bloques') or {}).get('n_inv')
        P = PER[b.rsplit('_', 1)[1]]
        return (not ni) if P == 0 else (ni is not None and ni >= 1)
    v['V3_inversiones'] = all(inv_ok(b, s) for b in brs for s in sem)
    exb = [b for b in ('PLAST_EXP_P22k', 'FIJO_EXP_P22k', 'PLAST_EXP_AZA_P22k') if b in brs]
    v['V4_la_exploracion_actua'] = (all(sum(1 for s in sem if (Bx(b, s).get('n_mord_exp') or 0) > 0) >= esc(N_ACTUA) for b in exb)
                                   and all((Bx(b, s).get('n_mord_exp') or 0) == 0 for b in ('PLAST_V_P22k', 'FIJO_V_Pinf') if b in brs for s in sem))
    # ERR-156 H-1: la regla plastica aprende POR la exploracion (pl_movidas > 0 Y n_mord_exp_aprende > 0); la vieja (solo pl_movidas) era
    # vacua: PLAST_V sin exploracion tambien la pasaba
    v['V5_la_regla_plastica_aprende'] = ('PLAST_EXP_P22k' not in brs) or sum(1 for s in sem if (Bx('PLAST_EXP_P22k', s).get('pl_movidas') or 0) > 0
                                                                           and (Bx('PLAST_EXP_P22k', s).get('n_mord_exp_aprende') or 0) > 0) >= esc(N_ACTUA)
    faza = [Bm('PLAST_EXP_AZA_P22k', s).get('frac_pl_ult') for s in sem] if 'PLAST_EXP_AZA_P22k' in brs else []
    faza = [x for x in faza if x is not None]
    v6_aplica = len(faza) >= esc(N_V6)
    v['V6_AZA_bit_al_azar'] = (not v6_aplica) or (AZA_BANDA[0] <= float(np.median(faza)) <= AZA_BANDA[1])
    v6_nota = (f"aplica: mediana {med(faza)} en {len(faza)} semillas" if v6_aplica else f"NO APLICA ({len(faza)} semillas con dato < {esc(N_V6)}): decide PB")
    valido = all(v.values())
    p = {}
    pe = pers.get('PLAST_EXP_P22k', 0); pf = pers.get('FIJO_EXP_P22k', 99); pa = pers.get('PLAST_EXP_AZA_P22k', 99)
    p['PA_rescate'] = pe >= esc(PERS_PL) and pf <= (esc(PERS_FIJO) if humo else PERS_FIJO)
    p['PB_control_AZA'] = pe >= pa + esc(MARGEN)
    p['PD_seleccion_prende'] = sum(1 for x in fr.get('PLAST_EXP_P22k', []) if x is not None and x >= FRAC_ALTA) >= esc(N_FRAC)
    p['PM_supera_controles'] = pe >= pf + esc(MARGEN) and pe >= pa + esc(MARGEN)
    if not valido: ver = 'NO SE LEE'
    elif p['PA_rescate'] and p['PB_control_AZA'] and p['PD_seleccion_prende']: ver = 'FUNCIONA'
    elif p['PM_supera_controles']: ver = 'HAY ALGO MODESTO'
    else: ver = 'NO'
    cerca = cerca_umbral(pe, pf, pa, humo, esc)   # ERR-156 H-3 (regla 12): a +-1 de un umbral de PA, PB o PM -> replica aunque sea NO
    # --- secundarias (NO deciden; sec. 7)
    sec = {}
    sec['PE_apaga_Pinf(no decide)'] = (sum(1 for s in sem if 'PLAST_EXP_Pinf' in brs and Bm('PLAST_EXP_Pinf', s).get('frac_pl') is not None
                                          and Bm('PLAST_EXP_Pinf', s)['frac_pl'] <= FRAC_BAJA) >= esc(N_FRAC))
    par = {}
    for a, b, k in (('PLAST_EXP_P22k', 'PLAST_V_P22k', 't_ext'), ('PLAST_EXP_P22k', 'FIJO_EXP_P22k', 't_ext'),
                    ('PLAST_EXP_P22k', 'PLAST_EXP_AZA_P22k', 't_ext'), ('PLAST_EXP_Pinf', 'FIJO_V_Pinf', 'K'), ('PLAST_EXP_P22k', 'FIJO_EXP_P22k', 'K')):
        if a in brs and b in brs:
            if k == 't_ext': xa = [X(a, s).get('t_ext') or Tt for s in sem]; xb = [X(b, s).get('t_ext') or Tt for s in sem]
            else: xa = [X(a, s).get(k) for s in sem]; xb = [X(b, s).get(k) for s in sem]
            dd = [x - y for x, y in zip(xa, xb) if x is not None and y is not None]
            par[f'{a}-{b}[{k}]'] = dict(gana=sum(1 for d in dd if d > 0), n=len(dd), dif_med=med(dd))
    sec['pareados'] = par
    # ERR-156 H-4 (DESCRIPTIVO, no decide): PM no exige piso y no se compara con PLAST_V_P22k; aqui se informa esa comparacion
    if 'PLAST_V_P22k' in brs and 'PLAST_EXP_P22k' in brs:
        sec['desc_PLAST_EXP_vs_PLAST_V_P22k'] = dict(persiste=[pe, pers['PLAST_V_P22k']], dif=pe - pers['PLAST_V_P22k'],
                                                     t_ext=par.get('PLAST_EXP_P22k-PLAST_V_P22k[t_ext]'))
    # --- impresion
    log(f"\n================ LECTURA ({PRERREGISTRO} sec. 6-7) · {carpeta} · VIDA {VIDA} · eps_exp {eps} · th_exp {TH_EXP}")
    log(f"{'brazo':19s} {'persiste':>8s} {'K med':>7s} {'t_ext med':>9s} {'frac_fin':>8s} {'frac_T':>7s} {'exp/vida':>8s} {'veto_r/v':>8s} "
        f"{'mord_exp':>9s} {'exp_apr':>8s} {'pl_mov':>7s} {'fr_mov':>6s} {'dw_mu':>6s} {'n_inv':>5s} {'seg':>6s}")
    for b in brs:
        xs = [X(b, s) for s in sem]; bs = [Bm(b, s) for s in sem]; es = [Bx(b, s) for s in sem]
        log(f"{b:19s} {str(pers[b]) + '/' + str(n):>8s} {med([x.get('K') for x in xs])!s:>7s} {med([x.get('t_ext') for x in xs])!s:>9s} "
            f"{med(fr[b])!s:>8s} {med([y.get('frac_pl') for y in bs])!s:>7s} {med([y.get('exp_por_vida') for y in es])!s:>8s} "
            f"{med([y.get('veto_res_por_vida') for y in es])!s:>8s} {med([y.get('n_mord_exp') for y in es])!s:>9s} "
            f"{med([y.get('n_mord_exp_aprende') for y in es])!s:>8s} {med([y.get('pl_movidas') for y in es])!s:>7s} "
            f"{med([y.get('frac_pl_movidas') for y in es])!s:>6s} {med([y.get('dw_medio_muertos') for y in es])!s:>6s} "
            f"{med([y.get('n_inv') for y in bs])!s:>5s} {med([x.get('seg') for x in xs])!s:>6s}")
    for b in brs:
        if 'PLAST' in b: log(f"  frac_pl_fin por semilla {b}: {fr[b]}")
    for b in exb:
        log(f"  exploracion {b}: R+ {med([Bx(b, s).get('n_exp_R_pos') for s in sem])} · R- {med([Bx(b, s).get('n_exp_R_neg') for s in sem])} (medianas)")
    log(f"  pareados (secundarios): {par}")
    log(f"\n  VALIDEZ {v} · V6 {v6_nota}\n  PUERTAS {p}\n  SECUNDARIAS {dict((k, x) for k, x in sec.items() if k != 'pareados')}")
    log(f"  VEREDICTO {'(HUMO, no cuenta) ' if humo else ''}{ver}")
    log(f"  CERCA DEL UMBRAL (ERR-156 H-3, regla 12): {cerca}")
    return dict(validez=v, v6_nota=v6_nota, puertas=p, secundarias=sec, veredicto=ver, cerca_umbral=cerca, persiste=pers, frac_pl_fin=fr, abortos=ab, n=n, humo=humo,
                eps_exp=eps, th_exp=TH_EXP)


def cerca_umbral(pe, pf, pa, humo=False, esc=lambda k: k):
    """ERR-156 H-3: {puerta: True} si alguna comparacion de PA, PB o PM queda a +-1 de su umbral (con los conteos de la serie)."""
    m = esc(MARGEN)
    c = dict(PA=abs(pe - esc(PERS_PL)) <= 1 or abs(pf - (esc(PERS_FIJO) if humo else PERS_FIJO)) <= 1,
             PB=abs(pe - (pa + m)) <= 1,
             PM=abs(pe - (pf + m)) <= 1 or abs(pe - (pa + m)) <= 1)
    c['alguna'] = any(c.values())
    return c


def replica_permitida(rs0):
    """Regla de parada (sec. 8) con ERR-156 H-3: FUNCIONA o HAY ALGO MODESTO, o NO con alguna puerta a +-1 de su umbral. NO SE LEE: no."""
    L = rs0.get('letra') or {}; vs = L.get('veredicto')
    return vs in ('FUNCIONA', 'HAY ALGO MODESTO') or (vs == 'NO' and bool((L.get('cerca_umbral') or {}).get('alguna')))


ORDV = {'NO SE LEE': -1, 'NO': 0, 'HAY ALGO MODESTO': 1, 'FUNCIONA': 2}


def bloque(a, b):
    return a if a == b else min((a, b), key=lambda z: ORDV[z])


# ------------------------------------------------------------------ candados (copiados de corre_baldwin)
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
    lk = os.path.join(carpeta, 'EN_CURSO.lock')
    if os.path.exists(lk) and reanuda: os.remove(lk)
    try:
        fd = os.open(lk, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
    except FileExistsError:
        return None, f"{lk} existe: otro lanzamiento en curso o cortado (usa --reanuda si esta cortado)"
    with os.fdopen(fd, 'w', encoding='utf-8') as f: f.write(f"pid {os.getpid()} · {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
    return lk, None


def main(argv=None):
    ap = argparse.ArgumentParser(allow_abbrev=False)
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument('--humo', action='store_true'); g.add_argument('--serie', action='store_true'); g.add_argument('--replica', action='store_true')
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
    if a.humo:
        if a.pool: raise SystemExit("--humo: sin Pool (un proceso)")
        tareas = [(HUMO_S, b) for b in HUMO]; T = T_HUMO; semillas = [HUMO_S]; pre = f"humo_s{HUMO_S}_T{T}"
    else:
        semillas = list(SERIE if a.serie else REPLICA); T = T_DEF
        tareas = [(s, b) for b in ORDEN for s in semillas]
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
    log(f"CORRE_BEXP · {pre} · {sel} · python {platform.python_version()} · pool {a.pool or 'NO (un proceso)'} · corre_bexp.py {yo} · "
        f"preregistro {PRERREGISTRO} {h16(os.path.join(AQUI, PRERREGISTRO)) if os.path.exists(os.path.join(AQUI, PRERREGISTRO)) else 'NO EXISTE'} · carpeta {carpeta}")
    log(f"  tareas {len(tareas)} · brazos {sorted(set(b for _, b in tareas), key=ORDEN.index)} · semillas {semillas[0]}-{semillas[-1]} · T {T} · "
        f"t_corte {T_CORTE} · VIDA {VIDA} · P {PER} · eps_exp {EPS_EXP} · th_exp {TH_EXP} · reanuda {a.reanuda}")
    if not a.humo:
        e = guarda(pre, a.reanuda)
        if e: log(f"  NO SE CORRE: {e}"); return 1
    if a.replica:
        rsm = sorted(glob.glob(os.path.join(DATOS, f"serie_s{SERIE[0]}-{SERIE[-1]}_T{T_DEF}_*", 'resumen.json')))
        rs0 = json.load(open(rsm[-1], encoding='utf-8')) if rsm else {}
        vs = (rs0.get('letra') or {}).get('veredicto')
        if not replica_permitida(rs0):
            log(f"  REGLA DE PARADA (sec. 8 + ERR-156 H-3): la replica solo se corre si la serie da FUNCIONA o HAY ALGO MODESTO, o si PA, PB o PM "
                f"cayeron a +-1 de su umbral; serie = {vs}, cerca {(rs0.get('letra') or {}).get('cerca_umbral')}. No se corre."); return 1
        if rs0.get('sha_runner') != yo:
            log(f"  NO SE CORRE: sha_runner de la serie {rs0.get('sha_runner')} != runner actual {yo}"); return 1
    ok = verifica(log)
    if not a.humo: ok &= git_limpio([os.path.join(AQUI, PRERREGISTRO), os.path.abspath(__file__), MOTOR, os.path.join(AQUI, 'construye_bexp.py')], log)
    if not ok: log("  ALGO FALLA -> no se corre (no se crea carpeta)."); return 1
    os.makedirs(carpeta, exist_ok=True)
    lk, e = candado(carpeta, a.reanuda)
    if e: log(f"  NO SE CORRE: {e}"); return 1
    LOGF[0] = open(os.path.join(carpeta, 'log.txt'), 'a', encoding='utf-8'); LOGF[0].write('\n'.join(BUF) + '\n'); LOGF[0].flush()
    args = [(s, b, T, carpeta, a.reanuda, EPS_EXP) for s, b in tareas]

    def fmt(x, k):
        bm = x.get('baldwin') or {}; bx = x.get('bexp') or {}
        return (f"  [{time.strftime('%H:%M:%S')}] [{k}/{len(args)}] [{time.time() - t0:7.1f}s] {x['brazo']:19s} s{x['seed']} ({x.get('_seg_job')}s) "
                f"persiste {x.get('persiste')} K {x.get('K')} t_ext {x.get('t_ext')} frac_fin {bm.get('frac_pl_fin')} mord_exp {bx.get('n_mord_exp')} "
                f"exp/vida {bx.get('exp_por_vida')} pl_mov {bx.get('pl_movidas')}/{bx.get('pl_reglas')} aprende {bm.get('n_aprende')} "
                f"n_inv {bm.get('n_inv')} aborto {x.get('aborto')}")
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
                       sha_runner=yo, eps_exp=EPS_EXP, th_exp=TH_EXP, shas={os.path.relpath(k, RAIZ): v for k, v in SHAS.items()}),
                  fh, ensure_ascii=False, indent=1, default=float)
    log(f"\n  RESUMEN {rj} (sha {h16(rj)})\nTerminado en {time.time() - t0:.1f}s")
    log(f"VEREDICTO DE LA {'CORRIDA' if a.humo else ('SERIE' if a.serie else 'REPLICA')}: {ver}   (regla de parada: {PRERREGISTRO} sec. 8)")
    LOGF[0].close()
    if lk and os.path.exists(lk): os.remove(lk)
    return 0


if __name__ == '__main__':
    sys.exit(main())
