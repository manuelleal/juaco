"""CRITERIO v4 — CALCULO DE POTENCIA sobre corridas REALES del tronco (ERR-94). No corre ninguna simulacion.

MISION: llegar a la AGI por este camino. Antes de fijar una letra se mide cuanto rechaza al propio tronco.

Lee (solo lectura) los crudos de las DOS series de calibracion de v3 (A-CAL 2121-2200 y su replica 2281-2360):
    datos/critv3_20260921_165615_crudo_{TA,TCii}.json
    datos/critv3_rep_20260921_170812_crudo_{TA,TCii}.json
y calcula, para cada opcion de letra, P(pasa | nulo) y P(pasa | desplazado delta) con dos modelos:
  (N) normal: d ~ N(delta, sd_d^2/n), LI = media - z*EE  ->  P(pasa) = Phi((delta + margen)*sqrt(n)/sd_d - z)
  (B) bootstrap NO pareado (el pareado es nominal, ERR-91 regla 6): cada brazo de n se remuestrea con reemplazo de
      las corridas del nulo; la letra COMPLETA (medianas + no inferioridad, los dos brazos de T-A a la vez con la
      MISMA semilla remuestreada) se aplica. B = 4000 por celda.
Nulo usado: SOLO los brazos OFF (el tronco sin perilla, 80 corridas por medida). Se repite con OFF+PLACEBO (160)
como sensibilidad: si difieren mucho, el placebo k=1 no es el nulo (la duda de CAL-4).

Tambien calcula la tasa de falso disparo de la vieja CAL-4 (6 marginales A12 no pareados en [0.40, 0.60]) bajo el nulo.

Uso: python experimentos/criterio_v4/analiza_potencia_v4.py      (escribe datos/humo/potencia_v4_<sello>.json)
"""
import sys, os, json, time, hashlib
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
import numpy as np
from math import erf, sqrt

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
DATOS = os.path.join(RAIZ, 'datos')
SERIES = ('critv3_20260921_165615', 'critv3_rep_20260921_170812')
Z = 1.645
B = 4000
RNG = np.random.default_rng(20260922)


def h16(p):
    return hashlib.sha256(open(p, 'rb').read()).hexdigest()[:16]


def Phi(x):
    return 0.5 * (1 + erf(x / sqrt(2)))


def carga():
    TA, TC, shas = [], [], {}
    for s in SERIES:
        for etq, L in (('TA', TA), ('TCii', TC)):
            f = os.path.join(DATOS, f'{s}_crudo_{etq}.json')
            shas[os.path.basename(f)] = h16(f)
            for r in json.load(open(f, encoding='utf-8'))['corridas']:
                r = dict(r); r['serie'] = s; L.append(r)
    return TA, TC, shas


def ni_pasa(dc, do, margen):
    """no inferioridad NO pareada (las semillas no controlan la trayectoria): LI = (mc - mo) - z*sqrt(vc/n + vo/n).
    Numericamente es la misma EE que la pareada cuando rho ~ 0 (medido: rho -0.47..+0.38)."""
    n = len(dc)
    d = np.asarray(dc) - np.asarray(do)       # pareado por indice, como el runner (pareado nominal)
    ee = d.std(ddof=1) / np.sqrt(n)
    return d.mean() - Z * ee > -margen


def boot_TC(rev, n, margen, delta=0.0):
    rev = np.asarray(rev, float); ok = 0
    for _ in range(B):
        c = RNG.choice(rev, n) + delta; o = RNG.choice(rev, n)
        ok += ni_pasa(c, o, margen)
    return ok / B


def boot_TA(null_por_brazo, n, margen, delta=0.0, muertes=1.10, r_delta=10.0):
    """null_por_brazo: {brazo: (r array, deaths array)} con las corridas ALINEADAS por (serie, semilla, arm), para
    que el remuestreo tome la MISMA corrida-etiqueta en los dos brazos (conserva la correlacion entre brazos)."""
    br = list(null_por_brazo)
    m = len(null_por_brazo[br[0]][0]); ok = 0; claus = np.zeros(3)
    for _ in range(B):
        ic = RNG.integers(0, m, n); io = RNG.integers(0, m, n)
        todo = True
        for b in br:
            r, dth = null_por_brazo[b]
            rc, ro = r[ic] + delta, r[io]; mc, mo = np.median(dth[ic]), np.median(dth[io])
            c1 = mc <= muertes * mo; c2 = np.median(rc) >= np.median(ro) - r_delta; c3 = ni_pasa(rc, ro, margen)
            claus += np.array([not c1, not c2, not c3]) / len(br)
            todo = todo and c1 and c2 and c3
        ok += todo
    return ok / B, (claus / B).round(4).tolist()


def a12_np(x, y):
    x = np.asarray(x)[:, None]; y = np.asarray(y)[None, :]
    return float(((x > y) + 0.5 * (x == y)).mean())


def cal4_falso(TA, TC, n, lo, hi, arms=('OFF',)):
    """P(las 6 marginales caen en [lo, hi]) cuando los dos 'brazos' son el MISMO nulo remuestreado (ley identica)."""
    V = {b: [r for r in TA if r['brazo'] == b and r['arm'] in arms] for b in ('VIVO', 'CUELLO_MIN')}
    R = [r for r in TC if r['arm'] in arms]
    ok = 0; BB = 1000
    for _ in range(BB):
        dentro = True
        for b in V:
            i, j = RNG.integers(0, len(V[b]), n), RNG.integers(0, len(V[b]), n)
            for k, sg in (('r', 1), ('deaths', -1)):
                x = [sg * V[b][t][k] for t in i]; y = [sg * V[b][t][k] for t in j]
                a = a12_np(x, y); dentro = dentro and lo <= a <= hi
        i, j = RNG.integers(0, len(R), n), RNG.integers(0, len(R), n)
        for k, sg in (('rev', 1), ('deaths', -1)):
            a = a12_np([sg * R[t][k] for t in i], [sg * R[t][k] for t in j]); dentro = dentro and lo <= a <= hi
        ok += dentro
    return ok / BB


def reparto_rapido(vals, n, margen, B_=400, rng=None):
    """P(pasa) de la no inferioridad por REPARTO (particion al azar en dos brazos de n) de un vector del nulo."""
    rng = rng or RNG; ok = 0
    for _ in range(B_):
        p = rng.permutation(len(vals)); c, o = vals[p[:n]], vals[p[n:2 * n]]
        ok += ni_pasa(c, o, margen)
    return ok / B_


def reparto_TA_rapido(nb, n, margen, B_=400, rng=None):
    rng = rng or RNG; m = len(nb['VIVO'][0]); ok = 0
    for _ in range(B_):
        p = rng.permutation(m); ic, io = p[:n], p[n:2 * n]; todo = True
        for b in nb:
            r, dth = nb[b]
            todo = todo and (np.median(dth[ic]) <= 1.10 * np.median(dth[io])) and \
                (np.median(r[ic]) >= np.median(r[io]) - 10) and ni_pasa(r[ic], r[io], margen)
        ok += todo
    return ok / B_


def meta_calibracion(TA, TC, disenos, S=200, n_serie=80):
    """POTENCIA DE LA PROPIA CALIBRACION (la leccion de la replica de v3): si la letra esta bien, ¿con que
    probabilidad la ESTIMACION por reparto de una serie de calibracion (2 x n_serie corridas del nulo por puerta)
    sale >= 0.95 (o >= 0.90)? Se simulan S pseudo-series remuestreando el nulo real (OFF+PLACEBO de las dos series de
    v3) y en cada una se estima P(T-A y T-C ii pasan) por reparto."""
    clave = lambda r: (r['serie'], r['seed'], r['arm'])
    V = {b: {clave(r): r for r in TA if r['brazo'] == b and r['arm'] in ('OFF', 'PLACEBO')} for b in ('VIVO', 'CUELLO_MIN')}
    ks = sorted(set(V['VIVO']) & set(V['CUELLO_MIN']))
    rA = {b: (np.array([V[b][k]['r'] for k in ks], float), np.array([V[b][k]['deaths'] for k in ks], float)) for b in V}
    rev = np.array([r['rev'] for r in TC if r['arm'] in ('OFF', 'PLACEBO')], float)
    res = {}
    for (n, mg) in disenos:
        est = []
        for _ in range(S):
            i = RNG.integers(0, len(ks), 2 * n); j = RNG.integers(0, len(rev), 2 * n)
            nb = {b: (rA[b][0][i], rA[b][1][i]) for b in rA}
            pa = reparto_TA_rapido(nb, n, 10.0, B_=200); pc = reparto_rapido(rev[j], n, mg, B_=200)
            est.append(pa * pc)
        est = np.array(est)
        res[f'n{n}_m{mg}'] = dict(media=round(est.mean(), 3), p05=round(np.percentile(est, 5), 3),
                                 P_est_ge_095=round((est >= 0.95).mean(), 3), P_est_ge_090=round((est >= 0.90).mean(), 3))
        print(f'  diseno n={n} margen T-C={mg}: estimacion de P(T-A y T-C ii | nulo) por serie: media {est.mean():.3f}  '
              f'p05 {np.percentile(est, 5):.3f}   P(est >= 0.95) {(est >= 0.95).mean():.3f}   P(est >= 0.90) {(est >= 0.90).mean():.3f}')
    return res


if __name__ == '__main__' and '--meta' in sys.argv:
    TA, TC, shas = carga()
    print('=== META: potencia de la propia calibracion (S=200 pseudo-series)')
    r = meta_calibracion(TA, TC, [(40, 10.0), (40, 15.0), (80, 10.0), (80, 12.5), (80, 15.0)])
    f = os.path.join(DATOS, 'humo', f"potencia_v4_meta_{time.strftime('%Y%m%d_%H%M%S')}.json")
    json.dump(dict(meta=dict(shas=shas, sha_script=h16(os.path.abspath(__file__))), res=r), open(f, 'w', encoding='utf-8'), indent=1)
    print(f'datos -> {os.path.relpath(f, RAIZ)}  sha256_16 = {h16(f)}')
    sys.exit(0)

if __name__ == '__main__':
    TA, TC, shas = carga()
    out = dict(meta=dict(fecha=time.strftime('%Y-%m-%dT%H:%M:%S'), z=Z, B=B, series=SERIES, shas=shas,
                         sha_script=h16(os.path.abspath(__file__))))
    print('crudos:', shas)
    for nulo_etq, arms in (('OFF', ('OFF',)), ('OFF+PLACEBO', ('OFF', 'PLACEBO'))):
        rev = np.array([r['rev'] for r in TC if r['arm'] in arms], float)
        sd_arm = rev.std(ddof=1); sd_d = sd_arm * np.sqrt(2)
        print(f'\n=== NULO {nulo_etq}: T-C (ii) rev  N={len(rev)}  media {rev.mean():.1f}  mediana {np.median(rev):.1f}  '
              f'sd brazo {sd_arm:.2f}  sd(d) no pareada {sd_d:.2f}')
        tabla = {}
        for n in (40, 60, 80, 100):
            for mg in (10.0, 12.5, 15.0, 20.0):
                pn = Phi(mg * np.sqrt(n) / sd_d - Z)
                pb = boot_TC(rev, n, mg)
                rej_m = boot_TC(rev, n, mg, delta=-mg)          # desplazado EXACTAMENTE el margen: debe pasar ~0.05
                rej_20 = boot_TC(rev, n, mg, delta=-20.0)
                rej_25 = boot_TC(rev, n, mg, delta=-0.5 * np.median(rev))   # la mitad de la reversion del tronco
                tabla[f'n{n}_m{mg}'] = dict(n=n, margen=mg, normal_nulo=round(pn, 3), boot_nulo=round(pb, 3),
                                           boot_delta_margen=round(rej_m, 3), boot_delta_20=round(rej_20, 3),
                                           boot_delta_media_rev=round(rej_25, 3))
                print(f'  n={n:3d} margen={mg:4.1f}  P(pasa|nulo) normal {pn:.3f} boot {pb:.3f}   '
                      f'P(pasa|delta=-margen) {rej_m:.3f}  P(pasa|delta=-20) {rej_20:.3f}  P(pasa|delta=-rev/2={-0.5*np.median(rev):.1f}) {rej_25:.3f}')
        out[f'TCii_{nulo_etq}'] = dict(N=len(rev), sd_brazo=round(sd_arm, 3), sd_d=round(sd_d, 3),
                                        mediana=float(np.median(rev)), tabla=tabla)

        # T-A: los dos brazos alineados por (serie, semilla, arm)
        clave = lambda r: (r['serie'], r['seed'], r['arm'])
        V = {b: {clave(r): r for r in TA if r['brazo'] == b and r['arm'] in arms} for b in ('VIVO', 'CUELLO_MIN')}
        ks = sorted(set(V['VIVO']) & set(V['CUELLO_MIN']))
        nb = {b: (np.array([V[b][k]['r'] for k in ks], float), np.array([V[b][k]['deaths'] for k in ks], float)) for b in V}
        print(f'--- T-A ENTERA (VIVO y CUELLO_MIN a la vez), nulo {nulo_etq}, N={len(ks)} etiquetas; '
              f'sd(r) VIVO {nb["VIVO"][0].std(ddof=1):.2f}, CUELLO_MIN {nb["CUELLO_MIN"][0].std(ddof=1):.2f}')
        ta = {}
        for n in (40, 60, 80):
            p, cl = boot_TA(nb, n, 10.0)
            p20, _ = boot_TA(nb, n, 10.0, delta=-20.0)
            p10, _ = boot_TA(nb, n, 10.0, delta=-10.0)
            ta[f'n{n}'] = dict(boot_nulo=round(p, 3), caida_por_clausula_media_brazo=dict(muertes=cl[0], r_mediana=cl[1], NI=cl[2]),
                               boot_delta_10=round(p10, 3), boot_delta_20=round(p20, 3))
            print(f'  n={n:3d} margen=10  P(pasa|nulo) {p:.3f}  caidas por clausula (media por brazo) muertes {cl[0]:.4f} '
                  f'r_med {cl[1]:.4f} NI {cl[2]:.4f}   P(pasa|delta=-10) {p10:.3f}  P(pasa|delta=-20) {p20:.3f}')
        out[f'TA_{nulo_etq}'] = ta

    print('\n=== CAL-4 (6 marginales A12 no pareado en una banda) con LEY IDENTICA (OFF contra OFF remuestreado)')
    c4 = {}
    for n, lo, hi in ((40, .40, .60), (80, .40, .60), (40, .33, .67), (80, .379, .621)):
        p = cal4_falso(TA, TC, n, lo, hi)
        c4[f'n{n}_[{lo},{hi}]'] = round(p, 3)
        print(f'  n={n} banda [{lo}, {hi}]  P(las 6 dentro | ley identica) = {p:.3f}   (falso disparo {1-p:.3f})')
    out['CAL4_ley_identica'] = c4
    sd40 = np.sqrt((40 + 40 + 1) / (12 * 40 * 40)); sd80 = np.sqrt((80 + 80 + 1) / (12 * 80 * 80))
    print(f'  sd teorica de A12 no pareado bajo H0: n=40 {sd40:.4f}, n=80 {sd80:.4f}; Bonferroni 6 marginales dos colas al 5 %: z = 2.638')
    out['CAL4_sd_teorica'] = dict(n40=round(sd40, 4), n80=round(sd80, 4), z_bonf6=2.638)

    os.makedirs(os.path.join(DATOS, 'humo'), exist_ok=True)
    f = os.path.join(DATOS, 'humo', f"potencia_v4_{time.strftime('%Y%m%d_%H%M%S')}.json")
    json.dump(out, open(f, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print(f'\ndatos -> {os.path.relpath(f, RAIZ)}  sha256_16 = {h16(f)}')
