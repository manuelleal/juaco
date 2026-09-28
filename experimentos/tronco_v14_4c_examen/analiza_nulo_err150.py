"""analiza_nulo_err150.py -- ERR-150: T-C (ii) POR VISITA. Nulo, margen y condicion anti-TERMO sobre crudos YA EXISTENTES.
MISION: llegar a la AGI por este camino. No corre ningun organismo: solo relee crudos con sha fijado. Ningun dato de TERMO'.

PROBLEMA (PREREGISTRO_examen_v144b sec. 5-6): la letra v4 de T-C (ii) mide rev = mordB[Q4] - mordA[Q4] en mordidas ABSOLUTAS.
Un organismo que come MENOS (un termostato: no muerde lo bueno cuando esta lleno) pierde rev aunque se desdiga.

LAS MEDIDAS (por corrida; cuartos Q1..Q4 de T; la reversion es en T/2, entre Q2 y Q3):
    p_X[q] = (mord_X[q] + 1) / (vis_X[q] + 2)            tasa de mordida POR VISITA (vis = pasos sobre el objeto = decisiones
                                                           de la boca), con el +1/+2 de Laplace (sin guardas: vis = 0 -> 0.5)
    S4 = p_B[Q4] / (p_A[Q4] + p_B[Q4])                    preferencia por visita, DESPUES, por lo que AHORA es bueno (B)
    S2 = p_A[Q2] / (p_A[Q2] + p_B[Q2])                    la MISMA preferencia ANTES, por lo que ENTONCES era bueno (A)
    C  = S4 - S2                                          CUANTO SE DESDICE: 0 = despues distingue lo bueno de lo malo tan bien
                                                           como antes; negativo = se quedo a medio camino; ~ -0.8 = no se desdijo
    J4 = p_B[Q4] - p_A[Q4]                                la forma propuesta en el encargo (la J balanceada de la regla 15); informe
    rev = mord_B[Q4] - mord_A[Q4]                         la letra v4 vigente; informe
  Por que C y no S4 ni J4 (el principio, antes de cualquier dato de TERMO'): el termostato (termo_letra) SOLO gobierna lo que su
  memoria dice que es bueno; lo malo cae a la boca de v14.3. Rechaza lo bueno cuando esta lleno ANTES y DESPUES de la reversion.
  C compara al organismo contra SI MISMO antes de la reversion: esa rebaja, igual antes y despues, se cancela. S4 solo la cancela si
  es igual para A y B (no lo es); J4 no la cancela nunca. Bloques 4 y 5 lo muestran con numeros.
  El suelo S4 > 0.5 (mediana) cierra el canal simetrico: un organismo que no distingue nada (S2 = S4 = 0.5) tiene C = 0.

LETRA PROPUESTA (T-C ii, ERR-150): (a) no inferioridad de una cola al 95 % (z 1.645) sobre d = C_cand - C_tronco, pareado nominal
por semilla, margen m (LI > -m), n = 80; Y (b) mediana de S4 del candidato > 0.5.
EL MARGEN (principio, no ajuste): la misma equivalencia RELATIVA que ya aprobo ERR-94 (12.5 ~ 30 % de la reversion del tronco,
medida desde "no distingue", rev = 0). Aqui "no distingue despues" es S4 = 0.5, o sea C = 0.5 - S2:
    m = 0.30 x (mediana de S4 del nulo - 0.5), redondeado a 0.005.
Luego se VERIFICA (no se elige) que cumple la regla 15 en cada serie y en el conjunto, y V4-5 (dientes).

Bloques de la salida:
  1  descriptivo por serie y brazo (rev, p, S2, S4, C, J4, visitas; trampa 3)
  2  margen por principio + reparto del nulo (OFF + TRONCO_B, ley identica por construccion; el metodo de V4-CAL: particion
     aleatoria 80/80, NI pareada nominal, B = 4000, semilla 20260922) por serie y juntas; desplazamientos -m y -1.6 m; resolucion
  3  realizaciones: TRONCO_B, PLACEBO (y PEOR) contra OFF en cada serie existente con la letra nueva (V4-2/V4-3)
  4  ANTES de la reversion no hay nada que desdecir: cada medida aplicada a Q2 (C: S2 - S1). TERMO contra OFF. Una medida que tumba
     a TERMO en Q2 mide otra cosa (cuanto come)
  5  "come menos" sintetico: mordidas de lo BUENO (A en Q1-Q2, B en Q3-Q4) adelgazadas a f (binomial; el termostato), y todas
     las mordidas adelgazadas (uniforme). C debe pasar; se reporta S4, J4 y rev
  6  ANTI-TERMO: TERMO (examen v14.4, CAND) contra OFF con la letra nueva (DEBE caer) + bootstrap P(TERMO pasa)
  7  controles que DEBEN caer: A y B intercambiados en Q4 (no se desdice); organismo indiferente (S2 = S4 = 0.5: el suelo)

    python experimentos/tronco_v14_4c_examen/analiza_nulo_err150.py
"""
import hashlib, json, os, sys, time

try:
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
except Exception:
    pass
import numpy as np

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
Z = 1.645
N_VIVO = 80
B_REP = 4000
SEM_REP = 20260922          # la del reparto de corre_criterio_v4 (V4-CAL)
PASO_M = 0.005
FRAC_ERR94 = 0.30           # 12.5 / ~42 (ERR-94): la equivalencia relativa ya aprobada
SUELO_S4 = 0.5

FUENTES = {   # nombre: (ruta relativa, sha256_16)
    'v143_serie': ('experimentos/tronco_v14_3_examen/datos/examen_v143_serie_20260924_124413_crudo_TCii.json', 'b215368ca4a1ced1'),
    'v143_replica': ('experimentos/tronco_v14_3_examen/datos/examen_v143_replica_20260924_131427_crudo_TCii.json', '7f702fe608e71706'),
    'v144_serie': ('experimentos/tronco_v14_4_examen/datos/examen_v144_serie_20260928_123734_crudo_TCii.json', 'd7b018cfd63d8eb6'),
    'v4cal_serie': ('datos/critv4_20260922_132544_crudo_TCii.json', '925dfa864941c30e'),
    'v4cal_replica': ('datos/critv4_rep_20260922_135746_crudo_TCii.json', 'bd9dcb449706a532'),
    'acal_serie': ('datos/critv3_20260921_165615_crudo_TCii.json', '5cd335dcaf6e3dd1'),
    'acal_replica': ('datos/critv3_rep_20260921_170812_crudo_TCii.json', 'd3e23a8fee406698'),
}
EXAMENES = ('v143_serie', 'v143_replica', 'v144_serie')      # lo que pidio el director (condicion 1)
CON_TB = EXAMENES + ('v4cal_serie', 'v4cal_replica')          # series con TRONCO_B (reparto posible, 160 corridas)


def h16(p):
    return hashlib.sha256(open(p, 'rb').read()).hexdigest()[:16]


def carga():
    D = {}
    for k, (rel, sha) in FUENTES.items():
        p = os.path.join(RAIZ, rel)
        s = h16(p)
        if s != sha:
            raise SystemExit(f'*** ANCLA {rel}: sha {s} != {sha}')
        j = json.load(open(p, encoding='utf-8'))
        D[k] = j['corridas'] if isinstance(j, dict) else j
    return D


# ------------------------------------------------------------------ LAS MEDIDAS (== las del runner v14.4c: el arnes lo comprueba)
def tasa(m, v):
    return (m + 1.0) / (v + 2.0)


def pref(r, q, bueno, malo):
    pb, pm = tasa(r['mord' + bueno][q], r['vis' + bueno][q]), tasa(r['mord' + malo][q], r['vis' + malo][q])
    return pb / (pb + pm)


def S4(r):
    return pref(r, 3, 'B', 'A')


def S2(r):
    return pref(r, 1, 'A', 'B')


def S1(r):
    return pref(r, 0, 'A', 'B')


def C(r):
    return S4(r) - S2(r)


def C_Q2(r):   # "antes no hay nada que desdecir": la misma cuenta entre dos cuartos SIN reversion
    return S2(r) - S1(r)


def J(r, q, bueno, malo):
    pb = r['mord' + bueno][q] / r['vis' + bueno][q] if r['vis' + bueno][q] else 0.0
    pm = r['mord' + malo][q] / r['vis' + malo][q] if r['vis' + malo][q] else 0.0
    return pb - pm


MEDIDAS = {'C': C, 'S4': S4, 'J4': lambda r: J(r, 3, 'B', 'A'), 'rev': lambda r: r['mordB'][3] - r['mordA'][3]}
MEDIDAS_Q2 = {'C': C_Q2, 'S4': S2, 'J4': lambda r: J(r, 1, 'A', 'B'), 'rev': lambda r: r['mordA'][1] - r['mordB'][1]}


def ni(xs, ys, margen, z=Z):
    """== corre_criterio_v3.no_inferior: pareada NOMINAL por posicion, una cola; pasa si LI > -margen."""
    d = np.asarray(xs, float) - np.asarray(ys, float)
    m = float(d.mean()); sd = float(d.std(ddof=1)); ee = sd / np.sqrt(len(d))
    li = m - z * ee
    return dict(n=len(d), media=round(m, 4), sd=round(sd, 4), LI=round(li, 4), margen=margen, pasa=bool(li > -margen))


def letra(off, cand, m):
    """LA LETRA de ERR-150: (a) NI sobre C con margen m; (b) mediana de S4 del candidato > 0.5."""
    a = ni([C(r) for r in cand], [C(r) for r in off], m)
    s4 = float(np.median([S4(r) for r in cand]))
    return bool(a['pasa'] and s4 > SUELO_S4), dict(NI_C=a, S4_mediana=round(s4, 4), suelo=bool(s4 > SUELO_S4))


def G(res, arm):
    return sorted([r for r in res if r['arm'] == arm], key=lambda r: r['seed'])


def reparto(v, f, n, margen, delta=0.0, B=B_REP, semilla=SEM_REP):
    """== corre_criterio_v4.reparto_TC con la medida f: particion aleatoria del nulo en dos grupos de n; P(pasa la NI)."""
    x = np.array([f(r) for r in v], float)
    rng = np.random.default_rng(semilla); ok = 0
    for _ in range(B):
        p = rng.permutation(len(x)); a = x[p[:n]]; b = x[p[n:2 * n]] + delta
        d = b - a; li = d.mean() - Z * d.std(ddof=1) / np.sqrt(n)
        ok += li > -margen
    return round(ok / B, 4)


def q(x):
    x = np.asarray(x, float)
    return dict(med=round(float(np.median(x)), 4), media=round(float(x.mean()), 4), sd=round(float(x.std(ddof=1)), 4),
                p05=round(float(np.quantile(x, 0.05)), 4), p95=round(float(np.quantile(x, 0.95)), 4))


def adelgaza(r, f, g, solo_bueno):
    """Cada mordida se conserva con probabilidad f (binomial); visitas intactas. solo_bueno: A en Q1-Q2 y B en Q3-Q4 (lo que el
    termostato gobierna); si no, todas."""
    mA, mB = list(r['mordA']), list(r['mordB'])
    for qq in range(4):
        if (not solo_bueno) or qq < 2:
            mA[qq] = int(g.binomial(mA[qq], f))
        if (not solo_bueno) or qq >= 2:
            mB[qq] = int(g.binomial(mB[qq], f))
    return dict(r, mordA=mA, mordB=mB)


if __name__ == '__main__':
    if sys.argv[1:]:
        raise SystemExit(f'*** este script no toma argumentos: {sys.argv[1:]}')
    t0 = time.time()
    D = carga()
    OUT = dict(fecha=time.strftime('%Y-%m-%dT%H:%M:%S'), fuentes={k: dict(ruta=v[0], sha=v[1]) for k, v in FUENTES.items()},
               medida="C = S4 - S2; S4 = pB4/(pA4+pB4), S2 = pA2/(pA2+pB2), pX = (mordX+1)/(visX+2); suelo mediana S4 > 0.5",
               z=Z, n=N_VIVO, B=B_REP, semilla_reparto=SEM_REP)
    print(f'ERR-150 -- T-C (ii) por visita: nulo y anti-TERMO sobre crudos existentes ({len(D)} fuentes, sha comprobado)')
    for k in ('v143_serie', 'v143_replica'):
        c, o = G(D[k], 'CAND'), G(D[k], 'OFF')
        igual = len(c) == len(o) == 80 and all(all(a[x] == b[x] for x in ('mordA', 'mordB', 'visA', 'visB')) for a, b in zip(c, o))
        print(f'   {k}: CAND (v14.3) == OFF en mordidas y visitas en las 80 semillas: {igual} -> CAND no entra al nulo (duplicado)')
        OUT.setdefault('v143_CAND_igual_OFF', {})[k] = igual

    print('\n--- 1 descriptivo por serie y brazo (medianas; visitas Q4 al lado: trampa 3)')
    DESC = {}
    for k, res in D.items():
        for arm in sorted({r['arm'] for r in res}):
            rr = G(res, arm)
            d = {m: q([f(r) for r in rr]) for m, f in MEDIDAS.items()}
            d.update(n=len(rr), S2=q([S2(r) for r in rr]),
                     pA2=round(float(np.median([tasa(r['mordA'][1], r['visA'][1]) for r in rr])), 4),
                     pB2=round(float(np.median([tasa(r['mordB'][1], r['visB'][1]) for r in rr])), 4),
                     pB4=round(float(np.median([tasa(r['mordB'][3], r['visB'][3]) for r in rr])), 4),
                     pA4=round(float(np.median([tasa(r['mordA'][3], r['visA'][3]) for r in rr])), 4),
                     visB_Q4=float(np.median([r['visB'][3] for r in rr])), visA_Q4=float(np.median([r['visA'][3] for r in rr])),
                     vis0=sum(1 for r in rr for qq in (1, 3) if r['visA'][qq] == 0 or r['visB'][qq] == 0))
            DESC[f'{k}/{arm}'] = d
            print(f"   {k:13s} {arm:8s} n {len(rr):3d} rev {d['rev']['med']:6.1f} | antes pA2 {d['pA2']:.3f} pB2 {d['pB2']:.3f} S2 {d['S2']['med']:.3f}"
                  f" | despues pB4 {d['pB4']:.3f} pA4 {d['pA4']:.3f} S4 {d['S4']['med']:.3f} | C {d['C']['med']:+.4f} (sd {d['C']['sd']:.4f}) "
                  f"J4 {d['J4']['med']:+.3f} | vis Q4 B/A {d['visB_Q4']:.0f}/{d['visA_Q4']:.0f} | vis=0: {d['vis0']}")
    OUT['descriptivo'] = DESC

    print('\n--- 2 el margen por principio y el reparto del nulo (OFF + TRONCO_B)')
    NUL = {k: [r for r in D[k] if r['arm'] in ('OFF', 'TRONCO_B')] for k in CON_TB}
    NUL_EX = [r for k in EXAMENES for r in NUL[k]]
    NUL_TODO = [r for k in CON_TB for r in NUL[k]]
    medS4 = float(np.median([S4(r) for r in NUL_EX]))
    medrev = float(np.median([MEDIDAS['rev'](r) for r in NUL_EX]))
    medJ = float(np.median([MEDIDAS['J4'](r) for r in NUL_EX]))
    m = round(round(FRAC_ERR94 * (medS4 - 0.5) / PASO_M) * PASO_M, 3)
    mJ = round(round(FRAC_ERR94 * medJ / PASO_M) * PASO_M, 3)
    print(f'   nulo de los tres examenes ({len(NUL_EX)} corridas): mediana S4 {medS4:.4f}, C {np.median([C(r) for r in NUL_EX]):+.4f}, '
          f'J4 {medJ:.4f}, rev {medrev:.1f}; suelo S4: min de las medianas por brazo y serie {min(DESC[f"{k}/{a}"]["S4"]["med"] for k in D for a in ("OFF", "TRONCO_B", "PLACEBO") if f"{k}/{a}" in DESC):.3f} > 0.5')
    print(f'   m = {FRAC_ERR94} x ({medS4:.4f} - 0.5) = {FRAC_ERR94 * (medS4 - 0.5):.4f} -> {m}   (rev: 12.5 = {12.5 / medrev:.3f} x {medrev:.1f}); '
          f'para S4 se usa el mismo m; para J4 (informe) m_J = {FRAC_ERR94} x {medJ:.4f} -> {mJ}')
    MARG = {'C': m, 'S4': m, 'J4': mJ, 'rev': 12.5}
    OUT['margen'] = dict(C=m, S4_informe=m, J4_informe=mJ, rev_v4=12.5, mediana_S4_nulo=round(medS4, 4), mediana_rev_nulo=medrev,
                         regla=f'm = {FRAC_ERR94} x (mediana de S4 del nulo de los tres examenes - 0.5), a {PASO_M}')
    REP = {}
    for etq, v in list(NUL.items()) + [('tres_examenes_juntos', NUL_EX), ('las_cinco_juntas', NUL_TODO)]:
        x = {}
        for mm in ('C', 'S4', 'J4', 'rev'):
            f = MEDIDAS[mm]; mg = MARG[mm]
            x[mm] = dict(P_nulo=reparto(v, f, N_VIVO, mg), P_menos_m=reparto(v, f, N_VIVO, mg, delta=-mg),
                         P_menos_1_6m=reparto(v, f, N_VIVO, mg, delta=-1.6 * mg),
                         sd_d=round(float(np.std([f(r) for r in v], ddof=1) * np.sqrt(2)), 4))
        REP[etq] = x
        print(f"   reparto {etq:22s} ({len(v):3d} corr.)  C: P(pasa|nulo) {x['C']['P_nulo']:.4f}  P(d=-m) {x['C']['P_menos_m']:.4f}  "
              f"P(d=-1.6m) {x['C']['P_menos_1_6m']:.4f}  sd(d)~{x['C']['sd_d']:.4f} | S4 {x['S4']['P_nulo']:.4f} | J4 {x['J4']['P_nulo']:.4f} | rev (v4) {x['rev']['P_nulo']:.4f}")
    OUT['reparto'] = REP
    techo = m / (Z + 1.645) * np.sqrt(N_VIVO)
    sd_max = max(REP[k]['C']['sd_d'] for k in NUL)
    print(f'   techo de sd(d) de C para P(pasa|nulo) >= 0.95 con n 80 y m {m}: {techo:.4f}; sd(d) maxima observada {sd_max:.4f} (holgura x{techo / sd_max:.1f})')
    fina = None
    for mm in np.arange(PASO_M, 0.2, PASO_M):
        if all(reparto(v, C, N_VIVO, float(mm), B=1000) >= 0.95 for v in NUL.values()):
            fina = round(float(mm), 3); break
    print(f'   (informe) el margen MAS FINO a paso {PASO_M} que pasaria >= 0.95 en las cinco series (B = 1000): {fina} -- NO se elige (ERR_150.md)')
    curva = {d_: reparto(NUL_EX, C, N_VIVO, m, delta=-d_) for d_ in (0.025, 0.05, 0.075, 0.1, 0.11, 0.125, 0.14, 0.15, 0.2)}
    print('   resolucion (tres examenes juntos): P(pasa) de un candidato peor por delta en C: ' + '  '.join(f'{d_}: {p_:.3f}' for d_, p_ in curva.items()))
    OUT['techo_sd'] = dict(techo=round(float(techo), 4), sd_max=sd_max, margen_mas_fino_informe=fina)
    OUT['curva_delta_C'] = curva

    print('\n--- 3 realizaciones con la letra nueva (V4-2 / V4-3): cada brazo contra OFF de SU serie')
    REAL = {}
    for k in D:
        off = G(D[k], 'OFF')
        for arm in ('TRONCO_B', 'PLACEBO', 'PEOR'):
            c = G(D[k], arm)
            if not c:
                continue
            p_, det = letra(off, c, m)
            x = {mm: ni([MEDIDAS[mm](r) for r in c], [MEDIDAS[mm](r) for r in off], MARG[mm]) for mm in MEDIDAS}
            REAL[f'{k}/{arm}'] = dict(letra=p_, det=det, informe=x)
            print(f"   {k:13s} {arm:8s} (n {len(c)}) LETRA {'PASA' if p_ else 'NO'}: C media d {det['NI_C']['media']:+.4f} LI {det['NI_C']['LI']:+.4f} "
                  f"> -{m}, S4 {det['S4_mediana']:.3f} > 0.5 | informe: S4 {'PASA' if x['S4']['pasa'] else 'NO'} J4 {'PASA' if x['J4']['pasa'] else 'NO'} "
                  f"rev {'PASA' if x['rev']['pasa'] else 'NO'} (LI {x['rev']['LI']:+.2f})")
    OUT['realizaciones'] = REAL

    print('\n--- 4 ANTES de la reversion no hay nada que desdecir: cada medida en Q2 (C: S2 - S1), TERMO y PLACEBO contra OFF (v14.4)')
    off = G(D['v144_serie'], 'OFF')
    Q2 = {}
    for arm in ('CAND', 'PLACEBO', 'TRONCO_B'):
        c = G(D['v144_serie'], arm)
        x = {mm: ni([MEDIDAS_Q2[mm](r) for r in c], [MEDIDAS_Q2[mm](r) for r in off], MARG[mm]) for mm in MEDIDAS_Q2}
        Q2[arm] = x
        print(f"   {'TERMO' if arm == 'CAND' else arm:8s} en Q2: " + ' | '.join(
            f"{mm} LI {x[mm]['LI']:+.4f} (> -{MARG[mm]}) -> {'PASA' if x[mm]['pasa'] else 'NO: *** tumba a TERMO SIN reversion'}" for mm in x))
    OUT['antes_Q2'] = Q2

    print('\n--- 5 "come menos" sintetico: CAND = TRONCO_B adelgazado, contra OFF, en cada serie de examen (visitas intactas)')
    g = np.random.default_rng(150)
    ADEL = {}
    for solo_bueno in (True, False):
        for f_ in (0.75, 0.5, 0.25, 0.1):
            for k in EXAMENES:
                off = G(D[k], 'OFF')
                c = [adelgaza(r, f_, g, solo_bueno) for r in G(D[k], 'TRONCO_B')]
                p_, det = letra(off, c, m)
                x = {mm: ni([MEDIDAS[mm](r) for r in c], [MEDIDAS[mm](r) for r in off], MARG[mm]) for mm in MEDIDAS}
                ADEL[f"{'bueno' if solo_bueno else 'todo'}/f{f_}/{k}"] = dict(letra=p_, det=det, informe=x)
                print(f"   {'solo lo BUENO' if solo_bueno else 'TODO        '} f {f_:4.2f} {k:13s} LETRA (C) {'PASA' if p_ else 'NO'} (LI {det['NI_C']['LI']:+.4f}, "
                      f"S4 {det['S4_mediana']:.3f}) | S4 LI {x['S4']['LI']:+.4f} {'PASA' if x['S4']['pasa'] else 'NO'} | J4 LI {x['J4']['LI']:+.3f} "
                      f"{'PASA' if x['J4']['pasa'] else 'NO'} | rev LI {x['rev']['LI']:+.2f} {'PASA' if x['rev']['pasa'] else 'NO'}")
    OUT['come_menos'] = ADEL

    print('\n--- 6 ANTI-TERMO: TERMO (examen v14.4, CAND = organismo_v144cal, memoria que NO olvida) contra OFF, con la letra nueva')
    termo, off = G(D['v144_serie'], 'CAND'), G(D['v144_serie'], 'OFF')
    pT, detT = letra(off, termo, m)
    x = {mm: ni([MEDIDAS[mm](r) for r in termo], [MEDIDAS[mm](r) for r in off], MARG[mm]) for mm in MEDIDAS}
    cT = [C(r) for r in termo]
    print(f"   TERMO: S2 {np.median([S2(r) for r in termo]):.4f} (antes distingue) -> S4 {detT['S4_mediana']:.4f} (despues prefiere A, el veneno); "
          f"C mediana {np.median(cT):+.4f} (p95 {np.quantile(cT, .95):+.4f}); OFF C {np.median([C(r) for r in off]):+.4f}")
    print(f"   LETRA: (a) C media d {detT['NI_C']['media']:+.4f} LI {detT['NI_C']['LI']:+.4f} > -{m} -> {detT['NI_C']['pasa']}; (b) S4 {detT['S4_mediana']} > 0.5 "
          f"-> {detT['suelo']}  => {'PASA (*** NO SIRVE)' if pT else 'NO: TUMBA A TERMO (las dos clausulas)'}")
    print(f"   informe: S4 LI {x['S4']['LI']:+.4f} | J4 LI {x['J4']['LI']:+.4f} | rev LI {x['rev']['LI']:+.2f} (lo registrado: NO)")
    g2 = np.random.default_rng(1500); okb = 0
    xs = np.array(cT); ys = np.array([C(r) for r in NUL_EX])
    for _ in range(B_REP):
        a_ = g2.choice(xs, N_VIVO); b_ = g2.choice(ys, N_VIVO); d_ = a_ - b_
        okb += (d_.mean() - Z * d_.std(ddof=1) / np.sqrt(N_VIVO)) > -m
    falta = -detT['NI_C']['LI']
    print(f"   corridas de TERMO con C > -m: {int(np.sum(np.array(cT) > -m))}/80; bootstrap (80 de TERMO contra 80 del nulo) P(pasa la NI) "
          f"{okb / B_REP:.4f}; para pasar haria falta un margen > {falta:.3f} ({falta / m:.1f} x m)")
    OUT['anti_TERMO'] = dict(letra=pT, det=detT, informe=x, C_mediana=round(float(np.median(cT)), 4),
                             P_pasa_bootstrap=round(okb / B_REP, 4), margen_que_haria_falta=round(falta, 4), tumba=bool(not pT))

    print('\n--- 7 controles que DEBEN caer')
    CAE = {}
    for k in EXAMENES:
        off = G(D[k], 'OFF')
        sw = [dict(r, mordA=r['mordA'][:3] + [r['mordB'][3]], mordB=r['mordB'][:3] + [r['mordA'][3]],
                   visA=r['visA'][:3] + [r['visB'][3]], visB=r['visB'][:3] + [r['visA'][3]]) for r in G(D[k], 'TRONCO_B')]
        ind = [dict(r, mordA=[v // 2 for v in r['visA']], mordB=[v // 2 for v in r['visB']]) for r in G(D[k], 'TRONCO_B')]
        p1, d1 = letra(off, sw, m); p2, d2 = letra(off, ind, m)
        CAE[k] = dict(intercambio=dict(letra=p1, det=d1), indiferente=dict(letra=p2, det=d2))
        print(f"   {k:13s} A y B intercambiados en Q4 (no se desdice): C LI {d1['NI_C']['LI']:+.4f}, S4 {d1['S4_mediana']:.3f} -> "
              f"{'PASA (*** sin dientes)' if p1 else 'NO (cae)'} | indiferente (muerde la mitad de todo): C LI {d2['NI_C']['LI']:+.4f} "
              f"(la NI sola {'PASA' if d2['NI_C']['pasa'] else 'NO'}), S4 {d2['S4_mediana']:.3f} -> {'PASA (*** canal simetrico abierto)' if p2 else 'NO (cae por el suelo)'}")
    OUT['controles_caen'] = CAE

    ok1 = all(REP[k]['C']['P_nulo'] >= 0.95 for k in REP)
    ok5 = all(REP[k]['C']['P_menos_1_6m'] <= 0.05 and REP[k]['C']['P_menos_m'] <= 0.15 for k in REP)
    ok3 = all(REAL[k]['letra'] for k in REAL if not k.endswith('/PEOR'))
    okQ2 = bool(Q2['CAND']['C']['pasa'] and Q2['PLACEBO']['C']['pasa'])
    ok4 = all(v['letra'] for v in ADEL.values())
    ok6 = not any(v['intercambio']['letra'] or v['indiferente']['letra'] for v in CAE.values())
    OUT['condiciones'] = dict(regla15_nulo=ok1, dientes_V4_5=ok5, realizaciones_TB_PLACEBO=ok3, antes_de_revertir_no_tumba=okQ2,
                              come_menos_no_tumba=ok4, tumba_TERMO=OUT['anti_TERMO']['tumba'], controles_caen=ok6)
    print('\n--- CONDICIONES')
    for k, v in OUT['condiciones'].items():
        print(f'   {k:28s} {"SI" if v else "*** NO"}')
    todo = all(OUT['condiciones'].values())
    OUT['veredicto'] = ('LA REGLA POR VISITA SE SOSTIENE: pasa el nulo (regla 15), tiene dientes, tumba a TERMO, no castiga comer menos '
                        'y cierra el canal simetrico' if todo else 'LA REGLA NO SE SOSTIENE: ver condiciones')
    print(f"\nVEREDICTO ERR-150: {OUT['veredicto']}   ({time.time() - t0:.0f} s)")
    os.makedirs(os.path.join(AQUI, 'datos'), exist_ok=True)
    fj = os.path.join(AQUI, 'datos', f"nulo_err150_{time.strftime('%Y%m%d_%H%M%S')}.json")
    json.dump(OUT, open(fj, 'w', encoding='utf-8'), ensure_ascii=False, indent=1, default=str)
    print(f'datos -> {os.path.relpath(fj, RAIZ)}  sha256_16 = {h16(fj)}')
    sys.exit(0 if todo else 1)
