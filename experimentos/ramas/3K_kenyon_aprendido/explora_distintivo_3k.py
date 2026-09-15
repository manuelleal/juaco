"""
explora_distintivo_3k.py - SONDA EXPLORATORIA POSTERIOR. **NO forma parte del criterio
preregistrado y NO puede cambiar el veredicto de 3K.** Se corre despues de cerrar el
veredicto, para generar la hipotesis del SIGUIENTE preregistro.

Motivo: el registro del proyecto (2L v1, lineas 125-126) ya documenta que desplazar una
celda hacia el PATRON COMPLETO la deja dominada por los pixeles compartidos, y que la
correccion fue desplazarla hacia lo DISTINTIVO (P - media de lo que la celda suele ver).
Las tres condiciones preregistradas de 3K usan la direccion "patron completo" = 2L v1.
Esta sonda prueba la direccion 2L v2 sobre KW.

Modos nuevos:
  'dist'       : al morder, KW[i] += lr*(P - m_i); m_i = media movil de los patrones que
                 la celda i gana. Se recorta a >=0 y se renormaliza a la norma de nacimiento.
  'dist_error' : lo mismo, modulado por |error de prediccion|/3, como la condicion 3.

El archivo es independiente para que organismo_3k.py conserve intacto el hash con el que
se generaron los datos del experimento principal.
"""
import sys, os, json, datetime, hashlib, platform
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..', '..'))
sys.path.insert(0, HERE)
import numpy as np
from multiprocessing import get_context
import organismo_3k as o3
from organismo_3k import L, NK, K, R_VAL, E_VAL, split_regla, valencia_regla
import run_3k as R3


def run_dist(seed, T=200000, kenyon_mode='dist', k_lr=0.01, k_scale=3.0, tau_m=0.01,
             fase2_en=100000, congelar_fase2=True,
             eta=.03, tau_e=.85, alpha=1.2, hambre_boca=2.0, aversion=1.0, costo=.002, nobj=4):
    PAT, tren, test = split_regla(seed)
    tipos = list(tren); val = {k: valencia_regla(k) for k in PAT}
    rng = np.random.default_rng(seed)
    Wl = rng.uniform(.1, .4, (2, 9)); KW = rng.uniform(0, 1, (NK, 6))
    KW0 = KW.copy(); n0 = np.linalg.norm(KW, axis=1)
    M = np.full((NK, 6), 0.5)          # media movil de lo que cada celda suele ver
    codeidx = lambda P: np.argsort(KW @ P)[-K:]
    code = lambda P: set(codeidx(P))
    kenyon = lambda P: np.eye(NK)[list(code(P))].sum(0)

    def kw_update(P, idx, lr):
        M[idx] += tau_m * (P - M[idx])
        if lr <= 0:
            return
        KW[idx] = np.clip(KW[idx] + lr * (P - M[idx]), 0, None)
        nn = np.linalg.norm(KW[idx], axis=1)
        KW[idx] *= (n0[idx] / np.maximum(nn, 1e-12))[:, None]

    Wp = np.zeros(NK); Wn = np.zeros(NK); el = np.zeros_like(Wl); tr = np.zeros(9)
    pos = 0; E = 1.0; objs = {}

    def spawn():
        while len(objs) < nobj:
            x = int(rng.integers(L))
            if x not in objs:
                objs[x] = tipos[int(rng.integers(len(tipos)))]
    spawn()
    f2 = fase2_en; d1 = max(f2 // 4, 1); d2 = max((T - f2) // 4, 1)
    qbin = lambda t: (min(t // d1, 3) if t < f2 else 4 + min((t - f2) // d2, 3))
    mord = {k: [0] * 8 for k in PAT}; vis = {k: [0] * 8 for k in PAT}; deaths = 0
    W_apriori = None; codes_f2 = None; KW_f2 = None

    def see():
        best = None
        for x, k in objs.items():
            dl = (pos - x) % L; dr = (x - pos) % L; d = min(dl, dr)
            if best is None or d < best[0]:
                best = (d, k, dl < dr)
        return best

    for t in range(T):
        if t == f2:
            Wb0 = Wp - Wn
            W_apriori = {k: float(Wb0 @ kenyon(PAT[k])) for k in PAT}
            codes_f2 = {k: sorted(int(i) for i in code(PAT[k])) for k in PAT}
            KW_f2 = KW.copy()
            for k in test:
                tipos.append(k)
        aprende = not (congelar_fase2 and t >= f2)
        hambre = np.clip(1 - E, 0, 1); d, k, left = see(); pat = PAT[k]
        x = np.concatenate([pat * 1.2, [1.5 if left else 0, 0 if left else 1.5, 1.0 if d == 0 else 0.]])
        noise = .15 + .5 * hambre
        V = Wl @ x; p = 1 / (1 + np.exp(-(V - .8) / noise)); u = p + rng.normal(0, .3, 2)
        m = np.zeros(2)
        if u.max() > .5: m[np.argmax(u)] = 1
        tr = tr * .7 + x
        if aprende: el = el * tau_e + np.outer(m - p, tr)
        pos = (pos + int(m[1] - m[0])) % L
        d2_, _, _ = see(); Rp = .2 if d2_ < d else 0.
        R = 0.
        if pos in objs:
            kk = objs[pos]; idx = codeidx(PAT[kk])
            kc = np.zeros(NK); kc[idx] = 1; Wb = Wp - Wn
            Vb = alpha * (Wb @ kc) + hambre_boca * hambre + .5
            pb = 1 / (1 + np.exp(-Vb / .3)); mordio = rng.random() < pb
            vis[kk][qbin(t)] += 1
            if mordio:
                R = R_VAL[val[kk]]; E = min(E + E_VAL[val[kk]], 1.5); mord[kk][qbin(t)] += 1
                del objs[pos]; spawn()
                if aprende:
                    dlt = R - Wb @ kc
                    if kenyon_mode == 'dist':
                        kw_update(PAT[kk], idx, k_lr)
                    elif kenyon_mode == 'dist_error':
                        kw_update(PAT[kk], idx, k_lr * min(abs(float(dlt)) / k_scale, 1.0))
                    if dlt > 0: Wp = np.clip(Wp + eta * dlt * kc, 0, 3.)
                    else:       Wn = np.clip(Wn + eta * aversion * (-dlt) * kc, 0, 3.)
        E -= costo
        if rng.random() < .003 and objs:
            del objs[list(objs)[int(rng.integers(len(objs)))]]; spawn()
        if aprende: Wl = np.clip(Wl + eta * (1 + 2 * hambre) * (max(R, 0) + Rp) * el, 0, 1.5)
        if E <= 0: deaths += 1; E = .6; pos = int(rng.integers(L))
    return dict(mord=mord, vis=vis, deaths=deaths, tren=tren, test=test, fase2_en=f2,
                W_apriori=W_apriori, codes_f2=codes_f2, KW_f2=KW_f2, KW=KW.copy(), KW0=KW0,
                W_final={k: float((Wp - Wn) @ kenyon(PAT[k])) for k in PAT},
                codes_fin={k: sorted(int(i) for i in code(PAT[k])) for k in PAT}, Wp=Wp, Wn=Wn)


def _job(a):
    s, m, lr = a
    r = run_dist(s, kenyon_mode=m, k_lr=lr)
    d = R3.analiza(r); d.update(seed=s, modo=m, k_lr=lr, variante='congelado')
    return d


if __name__ == "__main__":
    S = int(sys.argv[1]) if len(sys.argv) > 1 else 20
    jobs = [(s, m, lr) for m in ('dist', 'dist_error') for lr in (0.01, 0.03) for s in range(1, S + 1)]
    with get_context('spawn').Pool() as pool:
        rows = pool.map(_job, jobs, chunksize=1)
    print("=== SONDA EXPLORATORIA (fuera del preregistro): direccion 'distintivo' (2L v2) sobre KW ===")
    print(f"{'modo':16s} {'precTest':>9s} {'rango':>14s} {'accSigno':>9s} {'r_clase':>8s} {'r_solap':>8s} "
          f"{'ratio_disp':>11s} {'sel_clase':>10s} {'muertes':>8s} {'derivaKW':>9s}")
    for m in ('dist', 'dist_error'):
        for lr in (0.01, 0.03):
            rs = [r for r in rows if r['modo'] == m and abs(r['k_lr'] - lr) < 1e-12]
            p = [r['prec_test'] for r in rs]
            print(f"{m+' lr='+str(lr):16s} {np.median(p):9.3f} [{min(p):.2f},{max(p):.2f}]".ljust(42) +
                  f"{np.median([r['acc_signo'] for r in rs]):9.3f} "
                  f"{np.median([abs(r['r_clase']) for r in rs]):8.2f} "
                  f"{np.median([abs(r['r_solap']) for r in rs]):8.2f} "
                  f"{np.median([r['ratio_disp'] for r in rs]):11.3f} "
                  f"{np.median([r['sel_clase'] for r in rs]):10.3f} "
                  f"{np.median([r['deaths'] for r in rs]):8.0f} "
                  f"{np.median([r['deriva_kw'] for r in rs]):9.4f}")
    ts = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
    out = os.path.join(ROOT, 'datos', f'3K_exploratorio_distintivo_{ts}.json')
    sha = lambda p: hashlib.sha256(open(p, 'rb').read()).hexdigest()[:16]
    json.dump(dict(procedencia=dict(fecha=datetime.datetime.now().isoformat(timespec='seconds'),
                                    rama='3K_kenyon_aprendido', tipo='EXPLORATORIO_fuera_del_preregistro',
                                    T=200000, fase2_en=100000, semillas=S,
                                    python=platform.python_version(), numpy=np.__version__,
                                    sha256_16=dict(organismo_3k=sha(os.path.join(HERE, 'organismo_3k.py')),
                                                   explora=sha(os.path.join(HERE, 'explora_distintivo_3k.py')))),
                   filas=rows), open(out, 'w', encoding='utf-8'), indent=1)
    print("escrito:", out)
