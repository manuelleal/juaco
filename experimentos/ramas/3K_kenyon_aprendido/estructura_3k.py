"""
estructura_3k.py - diagnostico DESCRIPTIVO (no es criterio del PREREGISTRO).
Re-corre condicion 1 (fijo) y condicion 3 (error, k_lr=0.01) en el mundo-regla y mira
la estructura del codigo con detalle, incluida la metrica de ALCANCE del PREREGISTRO
de Etapa 3: fraccion de patrones de test con solapamiento 0 con todo el entrenamiento,
para los que el valor a priori es exactamente 0 y no hay generalizacion posible.
"""
import sys, os, json, datetime, hashlib, platform
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..', '..'))
sys.path.insert(0, HERE)
import numpy as np
from multiprocessing import get_context
import organismo_3k as o3

T = 200000; F2 = 100000
CONDS = [('fijo', 0.0), ('hebb_visita', 0.01), ('hebb_mordida', 0.01), ('error', 0.01)]


def _job(a):
    s, m, lr = a
    r = o3.run(s, T=T, mundo='regla', kenyon_mode=m, k_lr=lr, fase2_en=F2, congelar_fase2=True)
    tren, test = r['tren'], r['test']
    cf = r['codes_f2']; Wa = r['W_apriori']
    mudo = 0; sinsolap = 0; nA = []; nB = []
    for k in test:
        c = set(cf[k])
        mismo = sum(len(c & set(cf[y])) for y in tren if o3.valencia_regla(y) == o3.valencia_regla(k))
        otro = sum(len(c & set(cf[y])) for y in tren if o3.valencia_regla(y) != o3.valencia_regla(k))
        nA.append(mismo); nB.append(otro)
        if mismo + otro == 0: sinsolap += 1
        if abs(Wa[k]) < 0.02: mudo += 1
    KW = r['KW']
    col_med = KW.mean(axis=0).tolist(); col_sd = KW.std(axis=0).tolist()
    # correlacion celda a celda entre KW[:,0] y la preferencia de clase de la celda
    food = [k for k in tren + test if o3.valencia_regla(k) == 'comida']
    pois = [k for k in tren + test if o3.valencia_regla(k) == 'veneno']
    f = np.zeros(o3.NK); p = np.zeros(o3.NK)
    for k in food: f[r['codes_fin'][k]] += 1
    for k in pois: p[r['codes_fin'][k]] += 1
    usadas = (f + p) > 0
    pref = (f - p)[usadas] / (f + p)[usadas]
    r_px0_pref = float(np.corrcoef(KW[usadas, 0], pref)[0, 1]) if usadas.sum() > 2 and KW[usadas, 0].std() > 1e-9 and pref.std() > 1e-9 else float('nan')
    return dict(seed=s, modo=m, k_lr=lr, sin_solap=sinsolap, mudos=mudo,
                solap_mismo=float(np.mean(nA)), solap_otro=float(np.mean(nB)),
                col_med=col_med, col_sd=col_sd, r_px0_pref=r_px0_pref,
                celdas_usadas=int(usadas.sum()), uso_max=int((f + p).max()))


if __name__ == "__main__":
    S = int(sys.argv[1]) if len(sys.argv) > 1 else 20
    jobs = [(s, m, lr) for (m, lr) in CONDS for s in range(1, S + 1)]
    with get_context('spawn').Pool() as pool:
        rows = pool.map(_job, jobs, chunksize=1)
    print(f"=== estructura 3K (descriptivo), {S} semillas, fase2 congelada ===")
    print(f"{'cond':18s} {'test sin solapar':>17s} {'W=0':>6s} {'solap mismo cls':>16s} {'solap otra cls':>15s} "
          f"{'r(KW px0, pref)':>16s} {'celdas':>7s} {'usomax':>7s}")
    for (m, lr) in CONDS:
        rs = [r for r in rows if r['modo'] == m and abs(r['k_lr'] - lr) < 1e-12]
        print(f"{m+' lr='+str(lr):18s} {np.median([r['sin_solap'] for r in rs]):17.1f} "
              f"{np.median([r['mudos'] for r in rs]):6.1f} "
              f"{np.median([r['solap_mismo'] for r in rs]):16.2f} "
              f"{np.median([r['solap_otro'] for r in rs]):15.2f} "
              f"{np.median([r['r_px0_pref'] for r in rs]):16.2f} "
              f"{np.median([r['celdas_usadas'] for r in rs]):7.1f} "
              f"{np.median([r['uso_max'] for r in rs]):7.1f}")
    print("\n-- columnas de KW final (media y desv. tipica por pixel; px0 es el relevante) --")
    for (m, lr) in CONDS:
        rs = [r for r in rows if r['modo'] == m and abs(r['k_lr'] - lr) < 1e-12]
        md = np.median([r['col_med'] for r in rs], axis=0)
        sd = np.median([r['col_sd'] for r in rs], axis=0)
        print(f"{m+' lr='+str(lr):18s} media " + " ".join(f"{x:.3f}" for x in md) +
              "  |  sd " + " ".join(f"{x:.3f}" for x in sd))
    ts = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
    out = os.path.join(ROOT, 'datos', f'3K_estructura_{ts}.json')
    sha = lambda p: hashlib.sha256(open(p, 'rb').read()).hexdigest()[:16]
    json.dump(dict(procedencia=dict(fecha=datetime.datetime.now().isoformat(timespec='seconds'),
                                    rama='3K_kenyon_aprendido', tipo='descriptivo', T=T, fase2_en=F2,
                                    semillas=S, python=platform.python_version(), numpy=np.__version__,
                                    sha256_16=dict(organismo_3k=sha(os.path.join(HERE, 'organismo_3k.py')),
                                                   estructura_3k=sha(os.path.join(HERE, 'estructura_3k.py')))),
                   filas=rows), open(out, 'w', encoding='utf-8'), indent=1)
    print("escrito:", out)
