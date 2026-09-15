"""
Etapa 3 - Generalizacion. EJECUCION del preregistro (REGISTRO_etapas_1_2.md, "Etapa 3 - Generalizacion. PREREGISTRO").

Corre E1 (run(s), T=100000, sin escenario) con N semillas en paralelo y SONDEA los 64 patrones binarios
de 6 pixeles con los KW, Wp, Wn finales. No toca el organismo: usa organismo_v6_sonda.py (instrumentacion inerte).

Criterios PREREGISTRADOS (no se tocan):
  C1  Sostenida si |W_obs - W_pred| < 0.15 en >=90% de los pares (patron x semilla).
  C2  Sostenida si |correlacion parcial de W_obs con la similitud visual a A, controlando nA y nB| < 0.2.
  C3  Refutada si la similitud visual predice W_X mejor que el solapamiento, o si el residuo tiene
      estructura sistematica.
  Alcance: fraccion de los 64 patrones con nA = nB = 0.

Uso:  python generalizacion.py [nsemillas]
"""
import sys, os, json, csv, hashlib, datetime, platform, itertools
import numpy as np

sys.stdout.reconfigure(encoding='utf-8', errors='replace')

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
DATOS = os.path.join(RAIZ, 'datos')
SONDA_PATH = os.path.join(AQUI, 'organismo_v6_sonda.py')
ESTE_PATH = os.path.abspath(__file__)
if AQUI not in sys.path:
    sys.path.insert(0, AQUI)

K = 3
NK = 30
A = np.array([1, 1, 0, 1, 0, 0.])
B = np.array([1, 0, 1, 0, 1, 0.])


def sha16(ruta):
    return hashlib.sha256(open(ruta, 'rb').read()).hexdigest()[:16]


# ---------------------------------------------------------------- corrida E1
def corre(seed):
    import organismo_v6_sonda as o
    r = o.run(seed)
    return dict(seed=seed, Wp=r['Wp'], Wn=r['Wn'], KW=r['KW'],
                W=r['W'], comp=r['comp'], deaths=r['deaths'], solap=r['solap'],
                mord=r['mord'], vis=r['vis'])


# ---------------------------------------------------------------- sondeo
def code(KW, P):
    """MISMA regla que v6: set(np.argsort(KW@P)[-K:])."""
    return set(int(i) for i in np.argsort(KW @ P)[-K:])


def kenyon(KW, P):
    k = np.zeros(NK)
    k[list(code(KW, P))] = 1.0
    return k


def sondea(res):
    """Devuelve las 64 filas de una semilla."""
    KW, Wp, Wn = res['KW'], res['Wp'], res['Wn']
    Wb = Wp - Wn
    cA, cB = code(KW, A), code(KW, B)
    W_A = float(Wb @ kenyon(KW, A))
    W_B = float(Wb @ kenyon(KW, B))
    filas = []
    for bits in itertools.product([0, 1], repeat=6):
        X = np.array(bits, dtype=float)
        cX = code(KW, X)
        nA = len(cX & cA)
        nB = len(cX & cB)
        W_obs = float(Wb @ kenyon(KW, X))
        W_pred = (nA / 3.0) * W_A + (nB / 3.0) * W_B           # con W_A,W_B REALES de la semilla
        W_pred_nom = (1.0 / 3.0) * nA + (-3.0 / 3.0) * nB      # nominal 0.333*nA - 1.0*nB
        comp_A = int(np.sum(X * A))       # pixeles ON compartidos con A
        comp_B = int(np.sum(X * B))
        ham_A = int(np.sum(X != A))       # distancia de Hamming a A
        ham_B = int(np.sum(X != B))
        filas.append(dict(
            seed=res['seed'],
            patron=''.join(str(b) for b in bits),
            n_activos=int(sum(bits)),
            nA=nA, nB=nB,
            W_obs=W_obs, W_pred=W_pred, residuo=W_obs - W_pred,
            W_pred_nominal=W_pred_nom, residuo_nominal=W_obs - W_pred_nom,
            hamming_A=ham_A, hamming_B=ham_B,
            compartidos_A=comp_A, compartidos_B=comp_B,
            W_A_real=W_A, W_B_real=W_B,
            es_patron_nulo=int(sum(bits) == 0),
            code_X=' '.join(str(i) for i in sorted(cX)),
        ))
    return filas


# ---------------------------------------------------------------- estadistica
def resid_lineal(y, Z):
    """Residuo de y tras regresarla sobre Z (columnas) + intercepto."""
    Zc = np.column_stack([np.ones(len(y))] + [np.asarray(z, float) for z in Z])
    beta, *_ = np.linalg.lstsq(Zc, np.asarray(y, float), rcond=None)
    return np.asarray(y, float) - Zc @ beta


def corr(a, b):
    a = np.asarray(a, float); b = np.asarray(b, float)
    sa, sb = a.std(), b.std()
    if sa < 1e-12 or sb < 1e-12:
        return float('nan')
    return float(np.corrcoef(a, b)[0, 1])


def pcorr(y, x, Z):
    """Correlacion parcial de y con x controlando Z. Devuelve (r, std_res_y, std_res_x)."""
    ry = resid_lineal(y, Z)
    rx = resid_lineal(x, Z)
    return corr(ry, rx), float(ry.std()), float(rx.std())


def r2(y, Z):
    ry = resid_lineal(y, Z)
    y = np.asarray(y, float)
    vt = y.var()
    if vt < 1e-24:
        return float('nan')
    return float(1 - ry.var() / vt)


def med_rango(v):
    v = np.asarray(v, float)
    return float(np.median(v)), float(v.min()), float(v.max())


def col(filas, nombre):
    return np.array([f[nombre] for f in filas], float)


# ---------------------------------------------------------------- main
def main():
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 20
    seeds = list(range(1, n + 1))
    import multiprocessing as mp
    print(f"=== Etapa 3 - Generalizacion. E1, {n} semillas, T=100000 ===")
    print(f"sonda  sha256[:16] = {sha16(SONDA_PATH)}")
    print(f"script sha256[:16] = {sha16(ESTE_PATH)}")
    t0 = datetime.datetime.now()
    with mp.Pool(min(len(seeds), mp.cpu_count())) as pool:
        resultados = pool.map(corre, seeds)
    print(f"corridas: {(datetime.datetime.now()-t0).total_seconds():.1f} s\n")

    # sanidad: E1 debe haber convergido (mismo criterio que bateria.py)
    print("Convergencia E1 (criterio de bateria.py: |W_A-1|<.15 y |W_B+3|<.3):")
    okA = okB = 0
    for r in resultados:
        a, b = r['W']['A'], r['W']['B']
        okA += abs(a - 1) < .15
        okB += abs(b + 3) < .3
    WAs = [r['W']['A'] for r in resultados]
    WBs = [r['W']['B'] for r in resultados]
    print(f"  W_A: mediana {np.median(WAs):+.3f} rango [{min(WAs):+.3f},{max(WAs):+.3f}]  {okA}/{n} pasan")
    print(f"  W_B: mediana {np.median(WBs):+.3f} rango [{min(WBs):+.3f},{max(WBs):+.3f}]  {okB}/{n} pasan")
    print(f"  solapamiento A&B: {sorted(set(r['solap']['AB'] for r in resultados))}\n")

    filas = []
    for r in resultados:
        filas.extend(sondea(r))

    # ---------------- guardado (nunca sobrescribe)
    ts = t0.strftime('%Y%m%d_%H%M%S')
    csv_path = os.path.join(DATOS, f'etapa3_generalizacion_{ts}.csv')
    json_path = os.path.join(DATOS, f'etapa3_generalizacion_{ts}.json')
    for p in (csv_path, json_path):
        if os.path.exists(p):
            raise SystemExit(f"ABORTA: {p} ya existe, no se sobrescribe.")
    campos = ['seed', 'patron', 'n_activos', 'nA', 'nB', 'W_obs', 'W_pred', 'residuo',
              'W_pred_nominal', 'residuo_nominal', 'hamming_A', 'hamming_B',
              'compartidos_A', 'compartidos_B', 'W_A_real', 'W_B_real',
              'es_patron_nulo', 'code_X']
    with open(csv_path, 'w', newline='', encoding='utf-8') as fh:
        w = csv.DictWriter(fh, fieldnames=campos)
        w.writeheader()
        for f in filas:
            w.writerow({c: (f'{f[c]:.12g}' if isinstance(f[c], float) else f[c]) for c in campos})

    # ---------------- analisis
    an = analiza(filas, n)

    cab = dict(
        experimento='etapa3_generalizacion',
        fecha=t0.isoformat(timespec='seconds'),
        escenario='E1 (run(seed), T=100000, sin escenario)',
        n_semillas=n, semillas=seeds, n_patrones=64, filas=len(filas),
        organismo_sonda=os.path.relpath(SONDA_PATH, RAIZ).replace('\\', '/'),
        sha256_sonda=sha16(SONDA_PATH),
        sha256_organismo_v6=sha16(os.path.join(RAIZ, 'organismo', 'organismo_v6.py')),
        script=os.path.relpath(ESTE_PATH, RAIZ).replace('\\', '/'),
        sha256_script=sha16(ESTE_PATH),
        python=platform.python_version(), numpy=np.__version__,
        plataforma=platform.platform(),
        csv=os.path.basename(csv_path),
        convergencia_E1=dict(W_A=dict(mediana=float(np.median(WAs)), min=min(WAs), max=max(WAs), pasan=int(okA)),
                             W_B=dict(mediana=float(np.median(WBs)), min=min(WBs), max=max(WBs), pasan=int(okB))),
        resultados=an,
    )
    with open(json_path, 'w', encoding='utf-8') as fh:
        json.dump(cab, fh, indent=2, ensure_ascii=False)
    print(f"\nCSV : {csv_path}")
    print(f"JSON: {json_path}")
    print(f"sha256[:16] csv={sha16(csv_path)}  json={sha16(json_path)}")


def analiza(filas, n):
    out = {}
    W_obs = col(filas, 'W_obs'); W_pred = col(filas, 'W_pred')
    res = col(filas, 'residuo'); res_nom = col(filas, 'residuo_nominal')
    nA = col(filas, 'nA'); nB = col(filas, 'nB'); nact = col(filas, 'n_activos')
    compA = col(filas, 'compartidos_A'); hamA = col(filas, 'hamming_A')
    matchA = 6 - hamA
    nulo = col(filas, 'es_patron_nulo').astype(bool)
    seeds = np.array([f['seed'] for f in filas])

    print("=" * 78)
    print("PATRON NULO 000000 (KW@X todo ceros, argsort arbitrario)")
    fn = [f for f in filas if f['es_patron_nulo']]
    codes = sorted(set(f['code_X'] for f in fn))
    print(f"  code(000000) distintos entre las {n} semillas: {codes}")
    print(f"  nA: {sorted(set(f['nA'] for f in fn))}   nB: {sorted(set(f['nB'] for f in fn))}"
          f"   W_obs rango [{min(f['W_obs'] for f in fn):+.4f},{max(f['W_obs'] for f in fn):+.4f}]")
    out['patron_nulo'] = dict(codes=codes, nA=sorted(set(f['nA'] for f in fn)),
                              nB=sorted(set(f['nB'] for f in fn)),
                              W_obs_min=min(f['W_obs'] for f in fn), W_obs_max=max(f['W_obs'] for f in fn))

    # ---------------- CRITERIO 1
    print("=" * 78)
    print("CRITERIO 1  |W_obs - W_pred| < 0.15 en >=90% de los pares (patron x semilla)")
    for etiq, rr, clave in (('W_pred con W_A,W_B REALES de la semilla', res, 'real'),
                            ('W_pred NOMINAL 0.333*nA - 1.0*nB        ', res_nom, 'nominal')):
        ok = np.abs(rr) < 0.15
        pct = 100 * ok.mean()
        por_semilla = [100 * ok[seeds == s].mean() for s in range(1, n + 1)]
        m, lo, hi = med_rango(por_semilla)
        sin_nulo = 100 * ok[~nulo].mean()
        print(f"  {etiq}")
        print(f"    global {pct:.2f}% ({ok.sum()}/{len(ok)})   sin patron nulo: {sin_nulo:.2f}%")
        print(f"    por semilla: mediana {m:.2f}%  rango [{lo:.2f}%,{hi:.2f}%]")
        print(f"    |residuo|: mediana {np.median(np.abs(rr)):.6g}  max {np.abs(rr).max():.6g}")
        print(f"    VEREDICTO: {'SOSTENIDA' if pct >= 90 else 'REFUTADA'}")
        out[f'criterio1_{clave}'] = dict(pct_global=pct, pct_sin_nulo=float(sin_nulo),
                                         pct_por_semilla_mediana=m, pct_por_semilla_min=lo, pct_por_semilla_max=hi,
                                         abs_residuo_mediana=float(np.median(np.abs(rr))),
                                         abs_residuo_max=float(np.abs(rr).max()),
                                         veredicto='SOSTENIDA' if pct >= 90 else 'REFUTADA')

    # ---------------- CRITERIO 2
    print("=" * 78)
    print("CRITERIO 2  |corr parcial de W_obs con similitud visual a A, controlando nA,nB| < 0.2")
    print("  Correlaciones SIMPLES (pooled, 64 x semillas):")
    simples = dict(nA=corr(W_obs, nA), nB=corr(W_obs, nB),
                   compartidos_A=corr(W_obs, compA), match_A_6_menos_hamming=corr(W_obs, matchA),
                   hamming_A=corr(W_obs, hamA))
    for k2, v in simples.items():
        print(f"    r(W_obs, {k2:26s}) = {v:+.4f}")
    out['correlaciones_simples'] = simples

    out['criterio2'] = {}
    for etiq, x in (('compartidos_A', compA), ('match_A (6-hamming_A)', matchA)):
        r, sy, sx = pcorr(W_obs, x, [nA, nB])
        print(f"  parcial pooled con {etiq:22s}: r = {r:+.6f}   "
              f"std(res W_obs)={sy:.3g}  std(res sim)={sx:.3g}")
        ps = []
        for s in range(1, n + 1):
            m = seeds == s
            rs, sys_, sxs = pcorr(W_obs[m], x[m], [nA[m], nB[m]])
            ps.append((rs, sys_))
        stds = np.array([p[1] for p in ps])
        rs_v = np.array([p[0] for p in ps])
        finitos = rs_v[np.isfinite(rs_v)]
        print(f"    por semilla: std(res W_obs) mediana {np.median(stds):.3g} max {stds.max():.3g} "
              f"-> residuo intra-semilla {'DEGENERADO (0 numerico)' if stds.max() < 1e-9 else 'no degenerado'}")
        if len(finitos):
            print(f"    r por semilla: mediana {np.median(finitos):+.4f} rango "
                  f"[{finitos.min():+.4f},{finitos.max():+.4f}] ({len(finitos)}/{n} definidas)")
        ver = 'SOSTENIDA' if abs(r) < 0.2 else 'REFUTADA'
        print(f"    VEREDICTO ({etiq}): {ver}")
        out['criterio2'][etiq] = dict(r_parcial_pooled=r, std_res_Wobs=sy, std_res_sim=sx,
                                      veredicto=ver,
                                      std_res_Wobs_por_semilla_max=float(stds.max()),
                                      r_por_semilla_definidas=int(len(finitos)))

    # comparacion de poder predictivo (parte de C3 preregistrado)
    R2_solap = r2(W_obs, [nA, nB])
    R2_vis = r2(W_obs, [compA, col(filas, 'compartidos_B')])
    R2_vis_ham = r2(W_obs, [hamA, col(filas, 'hamming_B')])
    print(f"  R2 de W_obs ~ solapamiento [nA,nB]        = {R2_solap:.6f}")
    print(f"  R2 de W_obs ~ visual [compartidos_A,B]    = {R2_vis:.6f}")
    print(f"  R2 de W_obs ~ visual [hamming_A,B]        = {R2_vis_ham:.6f}")
    print(f"  -> la similitud visual {'SI' if max(R2_vis, R2_vis_ham) > R2_solap else 'NO'} predice mejor que el solapamiento")
    out['R2'] = dict(solapamiento=R2_solap, visual_compartidos=R2_vis, visual_hamming=R2_vis_ham,
                     visual_gana=bool(max(R2_vis, R2_vis_ham) > R2_solap))

    # ---------------- CRITERIO 3
    print("=" * 78)
    print("CRITERIO 3  estructura sistematica del residuo")
    out['criterio3'] = {}
    for etiq, rr, clave in (('residuo (W_pred real)', res, 'real'),
                            ('residuo (W_pred nominal)', res_nom, 'nominal')):
        print(f"  -- {etiq}: mediana {np.median(rr):+.6g}  rango [{rr.min():+.6g},{rr.max():+.6g}]")
        d = {}
        for var, vn in ((nA, 'nA'), (nB, 'nB'), (nact, 'n_activos_en_X')):
            rc = corr(rr, var)
            por = {}
            for v in sorted(set(var.tolist())):
                m = var == v
                por[int(v)] = dict(n=int(m.sum()), mediana=float(np.median(rr[m])),
                                   min=float(rr[m].min()), max=float(rr[m].max()))
            print(f"     r(residuo,{vn:14s}) = {rc:+.4f}")
            for v, dd in por.items():
                print(f"        {vn}={v}: n={dd['n']:4d} mediana {dd['mediana']:+.4f} "
                      f"rango [{dd['min']:+.4f},{dd['max']:+.4f}]")
            d[vn] = dict(r=rc, por_valor=por)
        out['criterio3'][clave] = d

    # descomposicion exacta del residuo nominal: debe ser (nA/3)(W_A-1) + (nB/3)(W_B+3)
    WAr = col(filas, 'W_A_real'); WBr = col(filas, 'W_B_real')
    esperado = (nA / 3.0) * (WAr - 1.0) + (nB / 3.0) * (WBr + 3.0)
    dmax = float(np.abs(res_nom - esperado).max())
    print(f"  descomposicion del residuo nominal = (nA/3)(W_A-1)+(nB/3)(W_B+3): "
          f"desviacion maxima {dmax:.6g}")
    out['criterio3']['descomposicion_nominal_max_desv'] = dmax

    # ---------------- ALCANCE
    print("=" * 78)
    print("METRICA DE ALCANCE: fraccion de los 64 patrones con nA=0 y nB=0")
    frs, frs_sin = [], []
    for s in range(1, n + 1):
        m = seeds == s
        cero = (nA[m] == 0) & (nB[m] == 0)
        frs.append(cero.sum() / 64.0)
        m2 = m & ~nulo
        cero2 = (nA[m2] == 0) & (nB[m2] == 0)
        frs_sin.append(cero2.sum() / 63.0)
    md, lo, hi = med_rango(frs)
    print(f"  incluyendo 000000 (64 patrones): mediana {md:.4f} ({md*64:.1f}/64)  "
          f"rango [{lo:.4f},{hi:.4f}] = [{lo*64:.0f},{hi*64:.0f}]/64")
    md2, lo2, hi2 = med_rango(frs_sin)
    print(f"  excluyendo 000000 (63 patrones): mediana {md2:.4f} ({md2*63:.1f}/63)  "
          f"rango [{lo2:.4f},{hi2:.4f}] = [{lo2*63:.0f},{hi2*63:.0f}]/63")
    print(f"  conteo por semilla (de 64): {[int(round(f*64)) for f in frs]}")
    # distribucion de nA y nB
    print("  distribucion de (nA,nB) sobre todos los pares:")
    for a_ in range(4):
        for b_ in range(4):
            c = int(((nA == a_) & (nB == b_)).sum())
            if c:
                print(f"     nA={a_} nB={b_}: {c:5d} pares ({100*c/len(nA):5.2f}%)")
    out['alcance'] = dict(frac_mediana=md, frac_min=lo, frac_max=hi,
                          conteo_por_semilla=[int(round(f * 64)) for f in frs],
                          frac_sin_nulo_mediana=md2, frac_sin_nulo_min=lo2, frac_sin_nulo_max=hi2,
                          dist_nA_nB={f"{a_},{b_}": int(((nA == a_) & (nB == b_)).sum())
                                      for a_ in range(4) for b_ in range(4)
                                      if int(((nA == a_) & (nB == b_)).sum())})

    # nA/nB alcanzables
    print(f"  max nA observado: {int(nA.max())}   max nB observado: {int(nB.max())}")
    print(f"  patrones con nA=3 (code identico a A): {int((nA==3).sum())} pares; "
          f"nB=3: {int((nB==3).sum())} pares")
    return out


if __name__ == '__main__':
    import multiprocessing as mp
    mp.set_start_method('spawn', force=True)
    main()
