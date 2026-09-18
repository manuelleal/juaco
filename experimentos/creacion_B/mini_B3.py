"""CREADOR B — mini-pruebas del bloque 3 (dendrita de dos ramas + division diferida). UN proceso, <= 3 corridas.
Uso:  python experimentos/creacion_B/mini_B3.py <k> <n_cf> <mask_rel> [del] [semillas...]
Ej.:  python experimentos/creacion_B/mini_B3.py 5 4 0            perfil discriminativo con division diferida
      python experimentos/creacion_B/mini_B3.py 5 4 2 0.35 1 2 3  dendrita encendida
"""
import json, os, sys, time
import numpy as np

sys.stdout.reconfigure(encoding='utf-8', errors='replace')
AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
sys.path[:0] = [AQUI, os.path.join(RAIZ, 'experimentos', 'nivel7_3T_k')]
import mundo_k_B3 as B

V13 = dict(mu_norm=True, div_signo=True, eta_s=0.015, puerta=3)

if __name__ == '__main__':
    k = int(sys.argv[1]); n_cf = int(sys.argv[2]); mr = int(sys.argv[3])
    rest = sys.argv[4:]
    dv = 0.25
    if rest and '.' in rest[0]:
        dv = float(rest.pop(0))
    seeds = [int(x) for x in rest] or [1, 2, 3]
    cfg = dict(kprof=k, n_cf=n_cf, mask_rel=mr, del_s=dv, del_c=dv)
    t0 = time.time(); out = []
    for s in seeds:
        r = B.run(s, arm='C3', T=100000, **V13, **cfg)
        dd = r['div_diag']
        if dd:
            dis = np.array([d[3] for d in dd]); ctx = np.array([d[4] for d in dd])
            keep = np.array([d[1] for d in dd]); tot = np.array([d[2] for d in dd])
            perfil = (f"px {keep.mean():.1f}/{tot.mean():.1f} | disc por slot ["
                      + " ".join(f"s{i}:{dis[:, i].mean():.2f}" for i in range(dis.shape[1])) + "] | ctx ["
                      + " ".join(f"s{i}:{ctx[:, i].mean():.2f}" for i in range(ctx.shape[1])) + "]")
        else:
            perfil = "sin divisiones"
        print(f"[{time.time()-t0:6.1f}s] k={k} n_cf={n_cf} mask={mr} d={dv} seed={s}  sep={r['sep']:.3f} "
              f"lift={r['lift']} celdas={r['celdas']} splits={r['splits']} t_pool={r['t_pool']} "
              f"solapA={r['solap_A']} muertes={r['deaths']} Rtot={r['Rtot']} W={r['W']}\n            {perfil}", flush=True)
        out.append(dict(seed=s, sep=r['sep'], lift=r['lift'], celdas=r['celdas'], splits=r['splits'],
                        t_pool=r['t_pool'], solap_A=r['solap_A'], deaths=r['deaths'], Rtot=r['Rtot'],
                        W=r['W'], diag=r['diag'], div_diag=dd[:60]))
    p = os.path.join(AQUI, f'mini_B3_k{k}_ncf{n_cf}_m{mr}_d{dv}.json')
    json.dump(dict(cfg=cfg, seeds=seeds, res=out), open(p, 'w'), indent=1)
    print(f"  MEDIANAS  lift_q4={float(np.median([o['lift'][3] for o in out])):.4f}  "
          f"sep={float(np.median([o['sep'] for o in out])):.3f}  celdas={float(np.median([o['celdas'] for o in out])):.0f}  "
          f"splits={float(np.median([o['splits'] for o in out])):.0f}  muertes={float(np.median([o['deaths'] for o in out])):.0f}"
          f"   -> {os.path.basename(p)}  ({time.time()-t0:.1f} s)")
