"""CREADOR B — mini-pruebas del bloque 1 (presupuesto de celdas), UN proceso, tandas de <= 3 corridas.
Uso:  python experimentos/creacion_B/mini_B1.py <tanda>
  diag5   diagnostico: k=5, recic=0, semillas 1-3 (cuantas celdas quedan invisibles a la puerta al agotarse el pool)
  diag4   idem k=4
  rci5    RCI encendido: k=5, recic=1, semillas 1-3
  rci4    RCI encendido: k=4, recic=1, semillas 1-3
"""
import json, os, sys, time

sys.stdout.reconfigure(encoding='utf-8', errors='replace')
AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
sys.path[:0] = [AQUI, os.path.join(RAIZ, 'experimentos', 'nivel7_3T_k')]
import mundo_k_B as B

V13 = dict(mu_norm=True, div_signo=True, eta_s=0.015, puerta=3)
TANDAS = {
    'diag5': dict(kprof=5, recic=0, tau_r=0),
    'diag4': dict(kprof=4, recic=0, tau_r=0),
    'diag1': dict(kprof=1, recic=0, tau_r=0),
    'rci5':  dict(kprof=5, recic=1, tau_r=2000),
    'rci4':  dict(kprof=4, recic=1, tau_r=2000),
    # control decisivo del presupuesto: el MISMO mundo con el doble de celdas (nkmax no toca el flujo de azar
    # hasta la primera division; es el confusor "agotamiento del pool" que el 3T original ya usaba post-hoc)
    'pool5': dict(kprof=5, recic=0, tau_r=0, nkmax=180),
    'pool4': dict(kprof=4, recic=0, tau_r=0, nkmax=180),
}

if __name__ == '__main__':
    tanda = sys.argv[1]
    cfg = TANDAS[tanda]
    seeds = [int(x) for x in sys.argv[2:]] or [1, 2, 3]
    t0 = time.time()
    out = []
    for s in seeds:
        r = B.run(s, arm='C3', T=100000, **V13, **cfg)
        d = r['diag']
        print(f"[{time.time()-t0:6.1f}s] k={cfg['kprof']} recic={cfg['recic']} seed={s}  "
              f"sep={r['sep']:.3f} lift_q4={r['lift'][3]} celdas={r['celdas']} splits={r['splits']} "
              f"t_pool={r['t_pool']} div_bloq={r['div_bloq']} n_recic={r['n_recic']} | "
              f"inv<=0.2:{d['inv']} frias:{d['frias']} recic_ok:{d['recic_ok']} nunca:{d['nunca']} "
              f"hist(|W|):{d['hist']} n_act_med={d['n_act_med']:.0f} muertes={r['deaths']}", flush=True)
        out.append(dict(seed=s, sep=r['sep'], lift=r['lift'], celdas=r['celdas'], splits=r['splits'],
                        t_pool=r['t_pool'], div_bloq=r['div_bloq'], n_recic=r['n_recic'], diag=d,
                        deaths=r['deaths'], Rtot=r['Rtot'], W=r['W'], solap_A=r['solap_A']))
    p = os.path.join(AQUI, f'mini_B1_{tanda}.json')
    json.dump(dict(tanda=tanda, cfg=cfg, seeds=seeds, res=out), open(p, 'w'), indent=1)
    print(f"  -> {p}  ({time.time()-t0:.1f} s)")
