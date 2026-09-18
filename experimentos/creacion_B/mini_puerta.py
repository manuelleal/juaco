"""CREADOR B — frente 3: la PUERTA de familiaridad contra la CAPACIDAD.
Diagnostico primero (sin mecanismo nuevo): en el mundo grande reducido, cuantos estimulos con el valor YA APRENDIDO
manda la puerta a la via lenta. Arms: v11 (puerta=None) y v13 (puerta=3). UN proceso, <= 3 corridas por tanda.
Uso:  python experimentos/creacion_B/mini_puerta.py <brazo> <n_est> <paso_t> [semillas...]
      brazo in {v11, v13, pat<N>}   (pat<N> = puerta por evidencia del codigo exacto, >= N mordidas)
"""
import json, os, sys, time
import numpy as np

sys.stdout.reconfigure(encoding='utf-8', errors='replace')
AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
sys.path[:0] = [AQUI, os.path.join(RAIZ, 'experimentos', 'v13_reverificacion'),
                os.path.join(RAIZ, 'experimentos', 'capacidad_grande'),
                os.path.join(RAIZ, 'experimentos', 'v11_evo_division'), os.path.join(RAIZ, 'organismo')]
import mundo_grande as G

D_PIX = 10
BASE = dict(plast=True, lam=0.05, memoria_rechazo=20, mu_norm=True, div_signo=True)

if __name__ == '__main__':
    brazo = sys.argv[1]; n_est = int(sys.argv[2]); paso_t = int(sys.argv[3])
    seeds = [int(x) for x in sys.argv[4:]] or [41, 42, 43]
    import organismo_capB as o   # con puerta_pat=0 es organismo_capD13 EXACTO (identidad 4/4)
    if brazo.startswith('pat'):
        cfg = dict(eta_s=0.015, puerta=3, puerta_pat=int(brazo[3:]))
    else:
        cfg = dict() if brazo == 'v11' else dict(eta_s=0.015, puerta=3)
    nom, pats, val, R = G.mundo(D_PIX, n_est)
    T = G.T_de(paso_t, n_est)
    print(f"mundo D={D_PIX} n_est={n_est} paso_t={paso_t} T={T}  brazo={brazo} cfg={cfg}", flush=True)
    t0 = time.time(); out = []
    for s in seeds:
        r = o.run(s, T=T, plan=G.plan_de(paso_t, nom, val), pats=pats, chk=G.chks(paso_t, n_est), **BASE, **cfg)
        for h in r['hist']:
            h['dev'] = {k: round(abs(v - R[k]), 3) for k, v in h['W'].items()}
        N = G.techo(r['hist']); M = G.m_max(r['hist'])
        dev_fin = {k: abs(v - R[k]) for k, v in r['W'].items()}
        aprend = [k for k, v in dev_fin.items() if v <= 0.3]
        nf = r.get('nofam_est', {})
        mordidos = [k for k, v in r.get('ncod_est', {}).items() if v >= 5]
        # LO QUE MIDE EL FRENTE 3: estimulos MORDIDOS >=5 veces que la puerta manda igualmente a la via lenta
        mal = [k for k in mordidos if nf.get(k, 0)]
        print(f"[{time.time()-t0:6.1f}s] {brazo} seed={s}  N*={N}  M_max={M}  celdas={r['celdas']} splits={r['splits']} "
              f"t_agot={r['t_agot']} nofam={sum(nf.values())}/{n_est}  aprendidos={len(aprend)}  "
              f"mordidos>=5={len(mordidos)}  MAL_RUTEADOS={len(mal)}  muertes={r['deaths']}", flush=True)
        out.append(dict(seed=s, N=N, M=M, celdas=r['celdas'], splits=r['splits'], t_agot=r['t_agot'],
                        nofam=int(sum(nf.values())), aprendidos=len(aprend), mordidos=len(mordidos),
                        mal=len(mal), deaths=r['deaths'], dev_fin={k: round(v, 3) for k, v in dev_fin.items()},
                        ncod_est=r.get('ncod_est', {}), nofam_est=nf))
    p = os.path.join(AQUI, f'mini_puerta_{brazo}_n{n_est}_p{paso_t}.json')
    json.dump(dict(brazo=brazo, cfg=cfg, n_est=n_est, paso_t=paso_t, seeds=seeds, res=out), open(p, 'w'), indent=1)
    print(f"  MEDIANAS  N*={np.median([o_['N'] for o_ in out]):.0f}  M_max={np.median([o_['M'] for o_ in out]):.0f}  "
          f"nofam={np.median([o_['nofam'] for o_ in out]):.0f}  aprend={np.median([o_['aprendidos'] for o_ in out]):.0f}  mal={np.median([o_['mal'] for o_ in out]):.0f}  "
          f"celdas={np.median([o_['celdas'] for o_ in out]):.0f}   ({time.time()-t0:.1f} s)")
