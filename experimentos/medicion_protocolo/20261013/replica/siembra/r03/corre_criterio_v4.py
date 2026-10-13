"""V4-CAL — CALIBRACION DEL CRITERIO DE TRONCO v4 (ERR-94). Ejecuta PREREGISTRO_calibracion_v4.md.

MISION: llegar a la AGI por este camino. Este bloque no mide un organo: mide EL INSTRUMENTO que decide si un organo
entra al tronco. Un criterio sirve si deja pasar al tronco presentado como candidato, deja pasar a un candidato inerte y
tumba a uno conocido como malo. v2 fallo lo primero (ERR-91); v3 fallo su replica (T-C ii 0.789/0.652 y un gatillo,
CAL-4, que se dispara en falso 47 % de las veces). v4 = n 80 en el mundo vivo + margen 12.5 en T-C (ii) + TRONCO_B.

Cuatro brazos del MISMO organismo (v14.2 en organismo_v3cal, REUSADO por import con sha verificado, sin copiar):
    OFF       el tronco v14.2, semilla s                                     (placebo = 0)
    TRONCO_B  el tronco v14.2, semilla s + 100000, SIN perilla: el tronco contra si mismo. Ley identica POR
              CONSTRUCCION (mismo codigo, mismos kwargs; no toca el rng: sustituye al CAL-4 de v3)
    PLACEBO   candidato inerte: placebo = 1 (consume un sorteo por paso y lo descarta)
    PEOR      conocido malo: costo = costo_a = 0.001 x 1.5 (cae T-A en las dos series de A-CAL)

  ETAPA 1  identidad: identidad_criterio_v3.py (54/54, el instrumento reusado) + identidad_v4.py (lo nuevo de v4).
  ETAPA 2  regla 14 campo a campo (regla14_v4.py).
  ETAPA 3  T-C (ii): mini_vivo VIVO, invertir_vivo_en = T/2, 80 semillas x 4 brazos = 320 corridas.
  ETAPA 4  T-A: corre_vivo_rep2 VIVO y CUELLO_MIN, 80 semillas x 2 x 4 = 640 corridas.
  ETAPA 5  veredicto de v4 (y v3, v2 al lado) sobre TRONCO_B, PLACEBO y PEOR: una linea por puerta (ERR-89).
  ETAPA 6  calibracion por REPARTO del nulo OFF + TRONCO_B (160 corridas por puerta) -> V4-1..V4-5 y P-1..P-7.

Uso:
  python experimentos/criterio_v4/corre_criterio_v4.py --humo                 (UN proceso, sin Pool: 2 semillas, T=30000)
  python experimentos/criterio_v4/corre_criterio_v4.py --pool 6               (serie 2841-2920)
  python experimentos/criterio_v4/corre_criterio_v4.py --pool 6 --replica A-B (semillas de replica, las fija el coordinador)
  python experimentos/criterio_v4/corre_criterio_v4.py --pool 6 --solo TA,TC
  (JUACO_POOL=N tambien vale; --pool manda. ERR-86)
"""
import sys, os, json, time, hashlib, platform, subprocess, re
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
import numpy as np

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
ORG = os.path.join(RAIZ, 'organismo')
VIVO_DIR = os.path.join(RAIZ, 'experimentos', 'nivel11_mundo_vivo')
V3_DIR = os.path.join(RAIZ, 'experimentos', 'criterio_v3')
DATOS = os.path.join(RAIZ, 'datos')
DATOS_HUMO = os.path.join(DATOS, 'humo')
sys.path[:0] = [ORG, VIVO_DIR, V3_DIR, AQUI]   # organismo/ PRIMERO (ERR-28); criterio_v4 al frente de todo

import umbrales_v4 as U


def h16(p):
    return hashlib.sha256(open(p, 'rb').read()).hexdigest()[:16]


# ------------------------------------------------------------------ ANCLAS: lo que se REUSA sin copiar, con sha fijo
ANCLAS = {
    os.path.join(V3_DIR, 'organismo_v3cal.py'): '148014f68cb01785',
    os.path.join(V3_DIR, 'identidad_criterio_v3.py'): '1356458f34134c83',
    os.path.join(V3_DIR, 'corre_criterio_v3.py'): '7f93eca0e45e167b',
    os.path.join(VIVO_DIR, 'corre_vivo_rep2.py'): '10ab45355883d98d',
    os.path.join(VIVO_DIR, 'mini_vivo.py'): 'f3e86cbe6c17e6d7',
    os.path.join(VIVO_DIR, 'organismo_vivo_rep2.py'): '96feb4918dc5d694',
    os.path.join(ORG, 'organismo_v142.py'): '17528d767fcebaf6',
}


def verifica_anclas():
    malas = [(os.path.relpath(p, RAIZ), h16(p), s) for p, s in ANCLAS.items() if h16(p) != s]
    if malas:
        raise SystemExit(f'*** ANCLA CAMBIADA (el instrumento reusado no es el que se calibro): {malas}')


def arg(nombre, defecto=None):
    return sys.argv[sys.argv.index(nombre) + 1] if nombre in sys.argv else defecto


HUMO = '--humo' in sys.argv
REP_ARG = arg('--replica')
SOLO = arg('--solo').split(',') if '--solo' in sys.argv else None
N_PARALELO = int(arg('--pool', os.environ.get('JUACO_POOL', 6)))

if REP_ARG:
    a, b = (int(x) for x in REP_ARG.split('-'))
    SEEDS = list(range(a, b + 1))
    if len(SEEDS) != U.V4['T-A']['n']:
        raise SystemExit(f'--replica debe dar exactamente {U.V4["T-A"]["n"]} semillas; da {len(SEEDS)}')
else:
    SEEDS = U.SEMILLAS['SERIE']
DESPL = U.SEMILLAS['DESPLAZAMIENTO_TRONCO_B']
T = 30000 if HUMO else 100000
BRAZOS_TA = ('VIVO', 'CUELLO_MIN')
ARMS = ('OFF', 'TRONCO_B', 'PLACEBO', 'PEOR')
CANDS = ('TRONCO_B', 'PLACEBO', 'PEOR')
C0, M_PEOR = U.PEOR['costo_base'], U.PEOR['m']
B_REP = 4000
ARNES_V3 = 'ARNES TOTAL: 54/54'
_log = {'f': None, 't0': time.time(), 'nom': None}


# ------------------------------------------------------------------ utilidades puras REUSADAS de v3 (por import)
def _v3():
    import corre_criterio_v3 as R3   # su modulo solo define funciones y lee su propio umbrales_v3; no corre nada
    return R3


def med(xs):
    return _v3().med(xs)


def a12(xs, ys):
    return _v3().a12(xs, ys)


def a12_np(xs, ys):
    return _v3().a12_np(xs, ys)


def no_inferior(xs, ys, margen, z):
    return _v3().no_inferior(xs, ys, margen, z)


# ------------------------------------------------------------------ los brazos: LO UNICO que los distingue
def perillas(arm):
    if arm in ('OFF', 'TRONCO_B'):
        return dict(placebo=0)
    if arm == 'PLACEBO':
        return dict(placebo=U.K_PLACEBO)
    if arm == 'PEOR':
        return dict(placebo=0, costo=C0 * M_PEOR, costo_a=C0 * M_PEOR)
    raise SystemExit(f'brazo desconocido: {arm}')


def semilla_real(seed, arm):
    """TRONCO_B corre la semilla s + 100000: otra trayectoria del MISMO organismo sin tocar el generador."""
    return seed + DESPL if arm == 'TRONCO_B' else seed


def kw_vivo(brazo, arm):
    import corre_vivo_rep2 as CR2
    return dict(CR2.BRAZOS[brazo], desambiguar=1, **perillas(arm))


def kw_rev(arm, Ti=None):
    import mini_vivo as MV
    return dict(MV.BRAZOS['VIVO'], desambiguar=1, invertir_vivo_en=(Ti or T) // 2, **perillas(arm))


# ------------------------------------------------------------------ tareas (aptas para Pool: importan dentro)
def tarea_vivo(args):
    brazo, seed, arm, Ti = args
    import corre_vivo_rep2 as CR2, organismo_v3cal as CAL
    kw = kw_vivo(brazo, arm); sr = semilla_real(seed, arm)
    t0 = time.time()
    r = CAL.run(sr, T=Ti, **kw)
    o = CR2.resumen2(brazo, sr, r, kw, Ti)
    o.update(seed=seed, seed_real=sr, arm=arm, placebo=r['placebo'], des_splits=r['des_splits'], seg=round(time.time() - t0, 2))
    return o


def tarea_rev(args):
    seed, arm, Ti = args
    import organismo_v3cal as CAL
    sr = semilla_real(seed, arm); t0 = time.time()
    r = CAL.run(sr, T=Ti, **kw_rev(arm, Ti))
    return dict(seed=seed, seed_real=sr, arm=arm, mordA=r['mord']['A'], mordB=r['mord']['B'], visA=r['vis']['A'],
                visB=r['vis']['B'], rev=r['mord']['B'][3] - r['mord']['A'][3], deaths=r['deaths'],
                muertes_nec=r['muertes_nec'], celdas=r['celdas'], splits=r['splits'], placebo=r['placebo'],
                seg=round(time.time() - t0, 2))


# ------------------------------------------------------------------ LAS LETRAS (v4 decide; v3 y v2 se reportan al lado)
def letra_TA(off, cand, u, delta=0.0, a12_min=None):
    """off, cand: listas ordenadas por semilla-etiqueta del MISMO brazo del mundo vivo."""
    rc = [x['r'] + delta for x in cand]; ro = [x['r'] for x in off]
    mu_c, mu_o = med([x['deaths'] for x in cand]), med([x['deaths'] for x in off])
    c_mu = bool(mu_c <= u['muertes'] * mu_o) if mu_o > 0 else bool(mu_c <= u['muertes'])
    c_r = bool(med(rc) >= med(ro) - u['r_delta'])
    if a12_min is not None:      # v2
        a = a12(rc, ro); return bool(c_mu and c_r and a is not None and a >= a12_min), dict(A12=a)
    ni = no_inferior(rc, ro, u['margen'], u['z'])
    return bool(c_mu and c_r and ni['pasa']), dict(muertes_c=mu_c, muertes_o=mu_o, r_c=med(rc), r_o=med(ro),
                                                   clausula_muertes=c_mu, clausula_r=c_r, NI=ni)


def letra_TC(off, cand, u, delta=0.0, a12_min=None):
    rc = [x['rev'] + delta for x in cand]; ro = [x['rev'] for x in off]
    if a12_min is not None:
        a = a12(rc, ro); return bool(a is not None and a >= a12_min), dict(A12=a)
    ni = no_inferior(rc, ro, u['margen'], u['z'])
    return bool(ni['pasa']), dict(rev_c=med(rc), rev_o=med(ro), NI=ni)


def letra_TF(off, cand):
    """T-F del mundo vivo: medianas de muertes, celdas y splits <= 1.25 x tronco (divisor max(tronco, 1))."""
    k = U.V4['T-F_vivo']['razon']; det = {}
    for c in ('deaths', 'celdas', 'splits'):
        mc, mo = med([x[c] for x in cand]), med([x[c] for x in off])
        det[c] = dict(cand=mc, tronco=mo, razon=round(mc / max(mo, 1), 3), pasa=bool(mc <= k * max(mo, 1)))
    return bool(all(d['pasa'] for d in det.values())), det


def G(res, arm, brazo=None):
    return sorted([r for r in res if r['arm'] == arm and (brazo is None or r.get('brazo') == brazo)], key=lambda r: r['seed'])


def juzga(res_vivo, res_rev, cand):
    """Veredicto de UN candidato contra OFF: T-A (dos brazos), T-C (ii), T-F vivo; v4 decide, v3/v2 al lado."""
    V = dict(candidato=cand)
    if res_vivo:
        ta = {}
        for b in BRAZOS_TA:
            off, c = G(res_vivo, 'OFF', b), G(res_vivo, cand, b)
            p4, d4 = letra_TA(off, c, U.V4['T-A'])
            p3, _ = letra_TA(off[:40], c[:40], U.V3['T-A'])
            p2, d2 = letra_TA(off[:20], c[:20], U.V2['T-A'], a12_min=U.V2['T-A']['a12'])
            pf, df = letra_TF(off, c)
            frac = round(float(np.mean([x['r'] - y['r'] >= -U.V4['T-A']['r_delta'] for x, y in zip(c, off)])), 3)
            ta[b] = dict(v4=p4, det_v4=d4, v3_n40=p3, v2_n20=p2, A12_v2=d2['A12'], TF=pf, det_TF=df, frac_semillas_d_ge_menos10=frac)
            log(f"   T-A {b:10s} [{cand:8s}] muertes {d4['muertes_c']}/{d4['muertes_o']} (<= {U.V4['T-A']['muertes']}x) "
                f"r {d4['r_c']}/{d4['r_o']} (>= -{U.V4['T-A']['r_delta']})  NI media {d4['NI']['media']} sd {d4['NI'].get('sd')} "
                f"LI {d4['NI']['LI']} > -{U.V4['T-A']['margen']} -> v4 {'PASA' if p4 else 'NO'} | v3(n40) {'PASA' if p3 else 'NO'} | "
                f"v2(n20, A12 {d2['A12']}) {'PASA' if p2 else 'NO'}  | fraccion de semillas con d >= -10: {frac} (lectura, no puerta)")
            log(f"   T-F {b:10s} [{cand:8s}] " + '  '.join(f"{k} {d['cand']}/{d['tronco']} ({d['razon']} <= 1.25)" for k, d in df.items())
                + f" -> {'PASA' if pf else 'NO'}")
        V['T-A'] = dict(brazos=ta, v4=all(ta[b]['v4'] for b in BRAZOS_TA), v3=all(ta[b]['v3_n40'] for b in BRAZOS_TA),
                        v2=all(ta[b]['v2_n20'] for b in BRAZOS_TA))
        V['T-F_vivo_TA'] = all(ta[b]['TF'] for b in BRAZOS_TA)
    if res_rev:
        off, c = G(res_rev, 'OFF'), G(res_rev, cand)
        p4, d4 = letra_TC(off, c, U.V4['T-C_ii'])
        p3, _ = letra_TC(off[:40], c[:40], U.V3['T-C_ii'])
        p2, d2 = letra_TC(off[:20], c[:20], U.V2['T-C_ii'], a12_min=U.V2['T-C_ii']['a12'])
        pf, df = letra_TF(off, c)
        expo = dict(expB_Q4=(med([r['visB'][3] for r in c]), med([r['visB'][3] for r in off])),
                    expA_Q4=(med([r['visA'][3] for r in c]), med([r['visA'][3] for r in off])))
        V['T-C_ii'] = dict(v4=p4, det_v4=d4, v3=p3, v2=p2, A12_v2=d2['A12'], exposiciones=expo)
        V['T-F_vivo_TC'] = pf; V['det_TF_TC'] = df
        log(f"   T-C ii       [{cand:8s}] rev {d4['rev_c']}/{d4['rev_o']}  NI media {d4['NI']['media']} sd {d4['NI'].get('sd')} "
            f"LI {d4['NI']['LI']} > -{U.V4['T-C_ii']['margen']} -> v4 {'PASA' if p4 else 'NO'} | v3(n40) {'PASA' if p3 else 'NO'} | "
            f"v2(n20, A12 {d2['A12']}) {'PASA' if p2 else 'NO'}   expB_Q4 {expo['expB_Q4']} expA_Q4 {expo['expA_Q4']} (trampa 3)")
    V['v4'] = bool(V.get('T-A', {}).get('v4', True) and V.get('T-C_ii', {}).get('v4', True)
                   and V.get('T-F_vivo_TA', True) and V.get('T-F_vivo_TC', True))
    log(f"   >>> {cand}: v4 (T-A, T-C ii, T-F vivo) {'PASA' if V['v4'] else 'NO PASA'}")
    return V


# ------------------------------------------------------------------ ETAPA 6: reparto del nulo (OFF + TRONCO_B)
def reparto_TA(res_vivo, n, u, delta=0.0, a12_min=None, B=B_REP, semilla=20260922):
    """Particion CONJUNTA de las etiquetas (semilla, arm) del nulo: la misma para VIVO y CUELLO_MIN (T-A es una puerta)."""
    etq = sorted({(r['seed'], r['arm']) for r in res_vivo if r['arm'] in ('OFF', 'TRONCO_B')})
    por = {b: {(r['seed'], r['arm']): r for r in res_vivo if r.get('brazo') == b and r['arm'] in ('OFF', 'TRONCO_B')} for b in BRAZOS_TA}
    if len(etq) < 2 * n or any(len(por[b]) < len(etq) for b in BRAZOS_TA):
        return None
    rng = np.random.default_rng(semilla); ok = 0
    for _ in range(B):
        p = rng.permutation(len(etq)); A = [etq[i] for i in p[:n]]; Bm = [etq[i] for i in p[n:2 * n]]
        ok += all(letra_TA([por[b][k] for k in A], [por[b][k] for k in Bm], u, delta, a12_min)[0] for b in BRAZOS_TA)
    return round(ok / B, 4)


def reparto_TC(res_rev, n, u, delta=0.0, a12_min=None, B=B_REP, semilla=20260922):
    v = [r for r in res_rev if r['arm'] in ('OFF', 'TRONCO_B')]
    if len(v) < 2 * n:
        return None
    rng = np.random.default_rng(semilla); ok = 0
    for _ in range(B):
        p = rng.permutation(len(v)); A = [v[i] for i in p[:n]]; Bm = [v[i] for i in p[n:2 * n]]
        ok += letra_TC(A, Bm, u, delta, a12_min)[0]
    return round(ok / B, 4)


def reparto_juntas(res_vivo, res_rev, n, uA, uC, B=B_REP):
    """T-A y T-C ii son mundos y semillas independientes: P(juntas) = P(T-A) x P(T-C ii) por reparto."""
    pa, pc = reparto_TA(res_vivo, n, uA, B=B), reparto_TC(res_rev, n, uC, B=B)
    return None if pa is None or pc is None else round(pa * pc, 4), pa, pc


def calibracion(V, res_vivo, res_rev, B=B_REP):
    log(f"ETAPA 6/6 — CALIBRACION por REPARTO del nulo OFF + TRONCO_B (ley identica por construccion), B={B}.")
    n4 = U.V4['T-A']['n']
    C = {}
    C['v4'] = dict(zip(('juntas', 'TA', 'TC'), reparto_juntas(res_vivo, res_rev, n4, U.V4['T-A'], U.V4['T-C_ii'], B)))
    C['v3'] = dict(zip(('juntas', 'TA', 'TC'), reparto_juntas(res_vivo, res_rev, 40, U.V3['T-A'], U.V3['T-C_ii'], B)))
    C['v2_TA_n20'] = reparto_TA(res_vivo, 20, U.V2['T-A'], a12_min=U.V2['T-A']['a12'], B=B)
    C['v2_TC_n20'] = reparto_TC(res_rev, 20, U.V2['T-C_ii'], a12_min=U.V2['T-C_ii']['a12'], B=B)
    C['v4_delta20'] = dict(TA=reparto_TA(res_vivo, n4, U.V4['T-A'], delta=-20.0, B=B), TC=reparto_TC(res_rev, n4, U.V4['T-C_ii'], delta=-20.0, B=B))
    C['v4_delta_margen'] = dict(TA=reparto_TA(res_vivo, n4, U.V4['T-A'], delta=-U.V4['T-A']['margen'], B=B),
                                TC=reparto_TC(res_rev, n4, U.V4['T-C_ii'], delta=-U.V4['T-C_ii']['margen'], B=B))
    for k, v in C.items():
        log(f"   reparto {k:16s} {v}")

    # marginales (ex CAL-4): DIAGNOSTICO con banda de Bonferroni, NO puerta
    marg = {}
    for cand in ('TRONCO_B', 'PLACEBO'):
        m = {}
        for b in BRAZOS_TA:
            g = lambda arm, k: [r[k] for r in res_vivo if r.get('brazo') == b and r['arm'] == arm]
            m[f'r_{b}'] = a12_np(g(cand, 'r'), g('OFF', 'r'))
            m[f'muertes_{b}'] = a12_np([-x for x in g(cand, 'deaths')], [-x for x in g('OFF', 'deaths')])
        g = lambda arm, k: [r[k] for r in res_rev if r['arm'] == arm]
        m['rev'] = a12_np(g(cand, 'rev'), g('OFF', 'rev'))
        m['muertes_rev'] = a12_np([-x for x in g(cand, 'deaths')], [-x for x in g('OFF', 'deaths')])
        dentro = sum(1 for x in m.values() if x is not None and U.MARGINALES['lo'] <= x <= U.MARGINALES['hi'])
        marg[cand] = dict(valores=m, dentro=dentro)
        log(f"   marginales {cand:8s} (A12 no pareado vs OFF; banda Bonferroni [{U.MARGINALES['lo']}, {U.MARGINALES['hi']}], NO puerta): "
            f"{m}  dentro {dentro}/6")

    # ---- condiciones de uso V4-1..V4-5
    VC = {}
    j = C['v4']['juntas']
    VC['V4-1'] = dict(medido=j, pasa=bool(j is not None and j >= U.CAL['V4-1']['lo']))
    VC['V4-2'] = dict(medido=V['TRONCO_B']['v4'], pasa=bool(V['TRONCO_B']['v4']))
    VC['V4-3'] = dict(medido=V['PLACEBO']['v4'], pasa=bool(V['PLACEBO']['v4']))
    VC['V4-4'] = dict(medido=V['PEOR']['v4'], pasa=bool(not V['PEOR']['v4']))
    d20, dm = C['v4_delta20'], C['v4_delta_margen']
    VC['V4-5'] = dict(medido=dict(delta20=d20, delta_margen=dm),
                      pasa=bool(all(x is not None and x <= U.CAL['V4-5']['hi20'] for x in d20.values())
                                and all(x is not None and x <= U.CAL['V4-5']['hi_margen'] for x in dm.values())))
    for k in ('V4-1', 'V4-2', 'V4-3', 'V4-4', 'V4-5'):
        log(f"   {k} [{U.CAL[k]['frase']}] -> {VC[k]['medido']} -> {'CUMPLE' if VC[k]['pasa'] else '*** NO CUMPLE ***'}")
    VC['utilizable_en_esta_serie'] = all(VC[k]['pasa'] for k in ('V4-1', 'V4-2', 'V4-3', 'V4-4', 'V4-5'))
    log(f"   >>> v4 {'CUMPLE' if VC['utilizable_en_esta_serie'] else 'NO CUMPLE'} sus cinco condiciones en esta serie "
        f"(utilizable sólo si la replica tambien las cumple)")

    # ---- predicciones firmadas P-1..P-7
    P = {}
    dentro = lambda x, k: bool(x is not None and U.PRED[k]['lo'] <= x <= U.PRED[k]['hi'])
    P['P-1'] = dict(medido=j, acierta=dentro(j, 'P-1'))
    P['P-2'] = dict(medido=C['v4']['TC'], acierta=dentro(C['v4']['TC'], 'P-2'))
    P['P-3'] = dict(medido=C['v4']['TA'], acierta=dentro(C['v4']['TA'], 'P-3'))
    P['P-4'] = dict(medido=C['v2_TA_n20'], acierta=dentro(C['v2_TA_n20'], 'P-4'))
    P['P-5'] = dict(medido=C['v3']['juntas'], acierta=dentro(C['v3']['juntas'], 'P-5'))
    P['P-6'] = dict(medido={c: marg[c]['dentro'] for c in marg},
                    acierta=bool(marg['TRONCO_B']['dentro'] == 6 and marg['PLACEBO']['dentro'] >= 5))
    dr = [V['PEOR']['T-A']['brazos'][b]['det_v4']['r_c'] - V['PEOR']['T-A']['brazos'][b]['det_v4']['r_o'] for b in BRAZOS_TA] if 'T-A' in V['PEOR'] else []
    P['P-7'] = dict(medido=dr, acierta=bool(dr and all(x <= -60 for x in dr)))
    for k in sorted(P):
        log(f"   {k} [{U.PRED[k]['frase']}] firmado {U.PRED[k].get('lo', '')}-{U.PRED[k].get('hi', '')} -> {P[k]['medido']} -> "
            f"{'ACERTADA' if P[k]['acierta'] else 'REFUTADA'}")
    V['calibracion'] = C; V['marginales'] = marg; V['condiciones'] = VC; V['predicciones'] = P
    return V


def etapas_5_6(res_vivo, res_rev, B=B_REP):
    log("ETAPA 5/6 — veredicto de v4 (v3 y v2 al lado) sobre TRONCO_B, PLACEBO y PEOR.")
    V = {c: juzga(res_vivo, res_rev, c) for c in CANDS}
    return calibracion(V, res_vivo, res_rev, B)


# ------------------------------------------------------------------ infraestructura (log, subprocesos, crudos, Pool)
def log(msg=""):
    linea = f"[{time.strftime('%H:%M:%S')} +{time.time()-_log['t0']:7.1f}s] {msg}"
    print(linea, flush=True)
    if _log['f']:
        _log['f'].write(linea + "\n"); _log['f'].flush(); os.fsync(_log['f'].fileno())


def sub(cmd, etq):
    log(f"   -> SUBPROCESO ({etq}): {' '.join(os.path.basename(x) for x in cmd)}")
    t0 = time.time()
    p = subprocess.run([sys.executable] + cmd, capture_output=True, text=True, cwd=AQUI, encoding='utf-8', errors='replace')
    salida = p.stdout or ''
    for l in salida.strip().splitlines()[-12:]:
        log(f"      | {l}")
    if p.returncode != 0:
        log(f"      *** codigo {p.returncode}; stderr: {(p.stderr or '')[-800:]}")
    log(f"      ({time.time()-t0:.0f}s)")
    return dict(etq=etq, returncode=p.returncode, cola=salida.strip().splitlines()[-12:], stdout=salida, seg=round(time.time() - t0, 1))


def lee_json(prefijo, res, carpeta):
    """ERR-87: PREFIJO + SELLO EXACTO leido de la salida del subproceso; nunca 'el ultimo del prefijo'."""
    m = re.findall(re.escape(prefijo) + r'_(\d{8}_\d{6})\.json', res.get('stdout', ''))
    if not m:
        log(f"      *** no aparece el sello de {prefijo}_*.json: SIN MEDIR (ERR-87)"); return None
    f = os.path.join(carpeta, f"{prefijo}_{m[-1]}.json")
    if not os.path.exists(f):
        log(f"      *** el sello {m[-1]} no existe"); return None
    log(f"      JSON por prefijo+sello: {os.path.basename(f)}  sha256_16 = {h16(f)}")
    return os.path.basename(f)


def crudo(etq, res, carpeta, extra=None):
    """ERR-54: crudos a disco ANTES del analisis, y el analisis los RELEE del disco."""
    f = os.path.join(carpeta, f"{_log['nom']}_crudo_{etq}.json")
    json.dump(dict(meta=dict(etapa=etq, fecha=time.strftime('%Y-%m-%dT%H:%M:%S'), n=len(res), extra=extra), corridas=res),
              open(f, 'w', encoding='utf-8'), ensure_ascii=False, default=str)
    log(f"   CRUDO ({len(res)} corridas) -> {os.path.basename(f)}  sha256_16 = {h16(f)}")
    return json.load(open(f, encoding='utf-8'))['corridas']


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
            if i % 40 == 0 or i == len(tareas):
                log(f"          {etq} {i}/{len(tareas)}")
    return res


def identidad(carpeta):
    r1 = sub([os.path.join(V3_DIR, 'identidad_criterio_v3.py'), '20000'], 'identidad v3 (instrumento reusado)')
    ok1 = r1['returncode'] == 0 and any(ARNES_V3 in l for l in r1['cola'])
    j1 = lee_json('identidad_v3cal', r1, DATOS_HUMO)
    r2 = sub([os.path.join(AQUI, 'identidad_v4.py'), '20000'], 'identidad v4 (lo nuevo)')
    tot = next((l for l in r2['cola'] if 'ARNES V4 TOTAL' in l), '')
    ok2 = r2['returncode'] == 0 and 'OK' in tot
    j2 = lee_json('identidad_v4', r2, DATOS_HUMO)
    r3 = sub([os.path.join(AQUI, 'regla14_v4.py')], 'regla 14 v4')
    ok3 = r3['returncode'] == 0
    return dict(ok=bool(ok1 and ok2 and ok3), v3=next((l for l in r1['cola'] if 'ARNES TOTAL' in l), None), v3_json=j1,
                v4=tot, v4_json=j2, regla14=('OK' if ok3 else 'FALLA'), seg=[r1['seg'], r2['seg'], r3['seg']])


# ------------------------------------------------------------------ crudos SINTETICOS (solo para probar el cableado en el humo)
def sinteticos(rng, delta_peor=-75.0):
    """Numeros INVENTADOS con las sd medidas (r 12-14, rev 20, muertes 10). NO son evidencia; solo prueban que las
    etapas 5-6 llegan al final con n = 80 y cuatro brazos, y que las letras hacen lo que dicen."""
    V, R = [], []
    for b, (mr, sr) in (('VIVO', (-75.0, 12.0)), ('CUELLO_MIN', (-8.0, 13.5))):
        for s in SEEDS:
            for arm in ARMS:
                d = delta_peor if arm == 'PEOR' else 0.0
                V.append(dict(brazo=b, seed=s, arm=arm, r=float(rng.normal(mr, sr) + d), deaths=float(rng.normal(94, 10) - 0.8 * d),
                              celdas=37.0, splits=float(rng.integers(3, 12))))
    for s in SEEDS:
        for arm in ARMS:
            R.append(dict(seed=s, arm=arm, rev=float(rng.normal(42, 20)), deaths=float(rng.normal(97, 10) + (60 if arm == 'PEOR' else 0)),
                          celdas=37.0, splits=float(rng.integers(3, 12)), visA=[0, 0, 0, 1700], visB=[0, 0, 0, 220]))
    return V, R


if __name__ == '__main__':
    verifica_anclas()
    stamp = time.strftime('%Y%m%d_%H%M%S')
    nom = f"critv4_humo_{stamp}" if HUMO else f"critv4_{'rep_' if REP_ARG else ''}{stamp}"
    _log['nom'] = nom
    SAL = DATOS_HUMO if HUMO else DATOS
    os.makedirs(SAL, exist_ok=True)
    _log['f'] = open(os.path.join(SAL, nom + '.log'), 'w', encoding='utf-8', newline='\n')
    pre = os.path.join(AQUI, 'PREREGISTRO_calibracion_v4.md'); crit = os.path.join(RAIZ, 'registro', 'CRITERIO_TRONCO_v4.md')
    SHAS = dict(preregistro=h16(pre) if os.path.exists(pre) else None, criterio_v4=h16(crit) if os.path.exists(crit) else None,
                script=h16(os.path.abspath(__file__)), umbrales=h16(os.path.join(AQUI, 'umbrales_v4.py')),
                identidad_v4=h16(os.path.join(AQUI, 'identidad_v4.py')), regla14=h16(os.path.join(AQUI, 'regla14_v4.py')),
                anclas={os.path.relpath(p, RAIZ): s for p, s in ANCLAS.items()})
    log(f"ARRANQUE V4-CAL — calibracion del CRITERIO DE TRONCO v4 ({'HUMO, un proceso, sin Pool' if HUMO else f'serie, Pool {N_PARALELO}'})")
    log(f"shas {SHAS}")
    log(f"brazos: " + ' | '.join(f"{a} {perillas(a)}{' semilla+'+str(DESPL) if a == 'TRONCO_B' else ''}" for a in ARMS))
    log(f"letra v4: {U.V4['T-A']['frase']} || {U.V4['T-C_ii']['frase']} || {U.V4['T-F_vivo']['frase']}")
    for k, o in U.OPCIONES_ERR94.items():
        log(f"   opcion ERR-94 {k:28s} P(pasa|nulo) T-A {o['P_TA']}  T-C ii {o['P_TC']}  juntas {o['P_juntas']}")

    # ================================================================ HUMO
    if HUMO:
        sh = U.SEMILLAS['HUMO']
        log(f"HUMO 0/3 — identidad (v3 54/54 + v4) y regla 14, en subprocesos de UN proceso.")
        ID = identidad(DATOS_HUMO)
        log(f"   identidad: {ID['v3']} | {ID['v4']} | regla 14 {ID['regla14']} -> {'OK' if ID['ok'] else '*** FALLA ***'}")
        log(f"HUMO 1/3 — 6 corridas de T={T} (180 000 pasos): T-A VIVO semilla {sh[0]} x 4 brazos; T-C ii semilla {sh[1]} x OFF/TRONCO_B.")
        rv = [tarea_vivo(('VIVO', sh[0], arm, T)) for arm in ARMS]
        for o in rv:
            log(f"   T-A VIVO {o['arm']:8s} s{o['seed']} (real {o['seed_real']})  r {o['r']}  desc {o['descendientes']}  muertes {o['deaths']}  "
                f"celdas {o['celdas']} splits {o['splits']}  placebo {o['placebo']}  {o['seg']} s")
        rr = [tarea_rev((sh[1], arm, T)) for arm in ('OFF', 'TRONCO_B')]
        for o in rr:
            log(f"   T-C ii  {o['arm']:8s} s{o['seed']} (real {o['seed_real']})  rev {o['rev']}  visB {o['visB']}  muertes {o['deaths']}  {o['seg']} s")
        dif_B = rv[1]['r'] != rv[0]['r'] or rv[1]['deaths'] != rv[0]['deaths']
        dif_P = rv[2]['r'] != rv[0]['r'] or rv[2]['deaths'] != rv[0]['deaths']
        log(f"   TRONCO_B difiere de OFF en la trayectoria: {dif_B} (DEBE ser True) | PLACEBO difiere: {dif_P} (DEBE ser True)")
        seg_vivo = float(np.mean([o['seg'] for o in rv])); seg_rev = float(np.mean([o['seg'] for o in rr]))
        f = 100000 / T
        cpu = 640 * seg_vivo * f + 320 * seg_rev * f
        idseg = sum(ID['seg'])
        log(f"   DURACION: {seg_vivo:.2f} s/corrida T-A y {seg_rev:.2f} s/corrida T-C a T={T} -> x{f:.2f} a T=100000 (lineal, supuesto) "
            f"-> {cpu:.0f} s de CPU; con Pool 6 ~ {cpu/6/60:.1f} min + identidad {idseg/60:.1f} min + reparto ~1 min "
            f"= ~{(cpu/6 + idseg + 60)/60:.0f} min por serie (sin contencion de CPU)")
        log("HUMO 2/3 — CABLEADO de las etapas 5-6 con crudos SINTETICOS (n = 80, cuatro brazos; B = 400). NO son evidencia.")
        sv, sr_ = sinteticos(np.random.default_rng(20260922))
        Vs = etapas_5_6(sv, sr_, B=400)
        cab = dict(TRONCO_B=Vs['TRONCO_B']['v4'], PLACEBO=Vs['PLACEBO']['v4'], PEOR=Vs['PEOR']['v4'],
                   reparto_v4=Vs['calibracion']['v4'], delta20=Vs['calibracion']['v4_delta20'])
        cab_ok = bool(cab['PEOR'] is False and cab['reparto_v4']['juntas'] is not None and cab['delta20']['TA'] <= 0.05)
        log(f"   cableado: {cab} -> {'OK' if cab_ok else '*** revisar ***'} (PEOR sintetico DEBE caer; el reparto DEBE salir)")
        log("HUMO 3/3 — JSON.")
        dj = os.path.join(SAL, nom + '.json')
        json.dump(dict(meta=dict(fecha=time.strftime('%Y-%m-%dT%H:%M:%S'), humo=True, T=T, corridas=6, pasos=6 * T, semillas=sh,
                                 shas=SHAS, python=platform.python_version(), numpy=np.__version__,
                                 identidad=ID, trayectoria_difiere=dict(TRONCO_B=dif_B, PLACEBO=dif_P),
                                 duracion=dict(seg_vivo=seg_vivo, seg_rev=seg_rev, cpu_serie_s=round(cpu), min_pool6=round((cpu / 6 + idseg + 60) / 60, 1)),
                                 cableado=cab, cableado_ok=cab_ok),
                       vivo=rv, reversion=rr), open(dj, 'w', encoding='utf-8'), ensure_ascii=False, default=str)
        log(f"datos -> {os.path.basename(dj)}  sha256_16 = {h16(dj)}")
        _log['f'].close()
        sys.exit(0 if (ID['ok'] and dif_B and dif_P and cab_ok) else 1)

    # ================================================================ SERIE
    log(f"semillas {SEEDS[0]}-{SEEDS[-1]} (n={len(SEEDS)}; TRONCO_B {SEEDS[0]+DESPL}-{SEEDS[-1]+DESPL}); T={T}")
    try:
        ps = subprocess.run(['powershell', '-NoProfile', '-Command',
                             "Get-CimInstance Win32_Process | Where-Object { $_.Name -like 'python*' } | ForEach-Object { \"$($_.ProcessId) $($_.CommandLine)\" }"],
                            capture_output=True, text=True, timeout=60).stdout.strip().splitlines()
    except Exception as e:
        ps = [f"(no se pudo listar: {e})"]
    log(f"REGLA 11 — procesos python vivos ({len(ps)}), este es pid {os.getpid()}")
    log("ETAPA 1-2/6 — identidad (v3 54/54 + v4) y regla 14.")
    ID = identidad(DATOS_HUMO)
    if not ID['ok']:
        log(f"*** identidad o regla 14 fallan ({ID}); se para sin veredicto."); _log['f'].close(); sys.exit(1)
    res_rev = res_vivo = []
    if SOLO is None or 'TC' in SOLO:
        log(f"ETAPA 3/6 — T-C (ii), {len(SEEDS)} semillas x {list(ARMS)} = {len(SEEDS)*len(ARMS)} corridas (Pool {N_PARALELO}).")
        res_rev = crudo('TCii', pool_map(tarea_rev, [(s, a, T) for s in SEEDS for a in ARMS], 'T-C ii'), DATOS,
                        extra=dict(semillas=SEEDS, despl=DESPL, arms=list(ARMS), invertir_vivo_en=T // 2))
    if SOLO is None or 'TA' in SOLO:
        log(f"ETAPA 4/6 — T-A, {list(BRAZOS_TA)} x {len(SEEDS)} x {list(ARMS)} = {2*len(SEEDS)*len(ARMS)} corridas (Pool {N_PARALELO}).")
        res_vivo = crudo('TA', pool_map(tarea_vivo, [(b, s, a, T) for b in BRAZOS_TA for s in SEEDS for a in ARMS], 'T-A'), DATOS,
                         extra=dict(brazos=list(BRAZOS_TA), semillas=SEEDS, despl=DESPL, arms=list(ARMS)))
    V = etapas_5_6(res_vivo, res_rev) if (res_vivo and res_rev) else dict(nota='etapa 5-6 exige T-A y T-C ii (--solo parcial)')
    meta = dict(fecha=time.strftime('%Y-%m-%dT%H:%M:%S'), replica=REP_ARG, semillas=SEEDS, despl_tronco_b=DESPL,
                brazos={a: perillas(a) for a in ARMS}, B_reparto=B_REP, pool=N_PARALELO, identidad=ID, shas=SHAS,
                letra=dict(v4={k: U.V4[k]['frase'] for k in U.V4}), procesos_python=ps,
                python=platform.python_version(), numpy=np.__version__)
    dj = os.path.join(DATOS, nom + '.json')
    json.dump(dict(meta=meta, veredictos=V), open(dj, 'w', encoding='utf-8'), ensure_ascii=False, default=str)
    log(f"datos -> {os.path.basename(dj)}  sha256_16 = {h16(dj)}")
    _log['f'].close()
