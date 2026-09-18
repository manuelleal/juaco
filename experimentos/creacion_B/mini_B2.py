"""CREADOR B — mini-pruebas del bloque 2 (hija ciega por relevancia). UN proceso, tandas de <= 3 corridas.
Uso:  python experimentos/creacion_B/mini_B2.py <tanda> [semillas...]
  perfil<k>  mask_rel=0: perfil de |mus| por slot en el momento de dividir (fija el umbral ANTES de encender nada)
  rel<k>     mask_rel=1: la hija nace ciega fuera de lo relevante
  base<k>    mask_rel=0 (control, = v13 tal cual)
"""
import json, os, sys, time
import numpy as np

sys.stdout.reconfigure(encoding='utf-8', errors='replace')
AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
sys.path[:0] = [AQUI, os.path.join(RAIZ, 'experimentos', 'nivel7_3T_k')]
import mundo_k_B2 as B

V13 = dict(mu_norm=True, div_signo=True, eta_s=0.015, puerta=3)


def resumen(r, k):
    dd = r['div_diag']
    if not dd:
        return "sin divisiones"
    pf = np.array([d[3] for d in dd])           # (n_div, k+1) max|mus| por slot
    keep = np.array([d[1] for d in dd]); tot = np.array([d[2] for d in dd])
    sl = " ".join(f"s{i}:{pf[:, i].mean():.2f}" for i in range(pf.shape[1]))
    return f"px {keep.mean():.1f}/{tot.mean():.1f}  |mus|max por slot [{sl}]"


if __name__ == '__main__':
    tanda = sys.argv[1]
    k = int(tanda[-1]); modo = tanda[:-1]
    cfg = dict(kprof=k, mask_rel=(1 if modo == 'rel' else 0))
    if len(sys.argv) > 2 and sys.argv[2].startswith('d'):     # dNN = del_s = del_c = NN/100
        v = int(sys.argv[2][1:]) / 100.0; cfg.update(del_s=v, del_c=v); sys.argv.pop(2)
    seeds = [int(x) for x in sys.argv[2:]] or [1, 2, 3]
    t0 = time.time(); out = []
    for s in seeds:
        r = B.run(s, arm='C3', T=100000, **V13, **cfg)
        print(f"[{time.time()-t0:6.1f}s] {tanda} d={cfg.get('del_s',0.25)} seed={s}  sep={r['sep']:.3f} "
              f"lift={r['lift']} celdas={r['celdas']} splits={r['splits']} t_pool={r['t_pool']} "
              f"solapA={r['solap_A']} muertes={r['deaths']} Rtot={r['Rtot']}\n            {resumen(r, k)}", flush=True)
        out.append(dict(seed=s, sep=r['sep'], lift=r['lift'], celdas=r['celdas'], splits=r['splits'],
                        t_pool=r['t_pool'], solap_A=r['solap_A'], deaths=r['deaths'], Rtot=r['Rtot'],
                        W=r['W'], diag=r['diag'], div_diag=r['div_diag'][:60]))
    p = os.path.join(AQUI, f'mini_B2_{tanda}_{cfg.get("del_s",0.25)}.json')
    json.dump(dict(tanda=tanda, cfg=cfg, seeds=seeds, res=out), open(p, 'w'), indent=1)
    lifts = [o['lift'][3] for o in out]
    print(f"  mediana lift_q4 = {float(np.median(lifts)):.4f}   mediana sep = {float(np.median([o['sep'] for o in out])):.3f}"
          f"   mediana celdas = {float(np.median([o['celdas'] for o in out])):.0f}   -> {p}  ({time.time()-t0:.1f} s)")
