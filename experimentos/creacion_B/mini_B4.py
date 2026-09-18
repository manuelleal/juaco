"""CREADOR B — mini-pruebas del organo de ASOCIACION EN UNA EXPOSICION. UN proceso, tandas de <= 3 corridas.
Numero principal: exp_hasta[<nuevo>] = MORDIDAS del patron nuevo hasta que el valor que usa la boca cae a
<= tol_sem del valor real. Uso:  python experimentos/creacion_B/mini_B4.py <escenario> <sem> [semillas...]
  escenarios: Cven (C veneno, parecido debil) · Dcom2 (D comida con solap_B=2: PARECIDO ENGANOSO) · Ccom (C comida)
  sem: 0 = v14 · 1 = via lenta (memoria 0) · 2 = canal HD (Kanerva) · 3 = CONTROL prior al azar
"""
import json, os, sys, time
import numpy as np
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
sys.path[:0] = [AQUI, os.path.join(RAIZ, 'organismo')]
import organismo_v14L as B

ESC = {
    'Cven':  dict(nuevo='C', nuevo_en=50000, nuevo_val='veneno'),
    'Ccom':  dict(nuevo='C', nuevo_en=50000, nuevo_val='comida'),
    'Dcom2': dict(nuevo='D', nuevo_en=50000, nuevo_val='comida', solap_B=2),
}

if __name__ == '__main__':
    esc = sys.argv[1]; sem = int(sys.argv[2])
    seeds = [int(x) for x in sys.argv[3:]] or [1, 2, 3]
    kw = ESC[esc]; nv = kw['nuevo']
    t0 = time.time(); out = []
    for s in seeds:
        r = B.run(s, **kw, sem=sem)
        e = r['exp_hasta']; nm = r['n_mord']
        lig = [x for x in r['sem_log'] if x[1] == nv]
        print(f"[{time.time()-t0:6.1f}s] {esc} sem={sem} s{s}  exp_hasta[{nv}]={e.get(nv)}  (A={e.get('A')} B={e.get('B')})"
              f"  mordidas[{nv}]={nm.get(nv)}  W={r['W']}  ligaduras={r['n_sem']} desligaduras={r['n_des']}"
              f"  {nv}:{lig[:2]}  muertes={r['deaths']} celdas={r['celdas']}", flush=True)
        out.append(dict(seed=s, exp=e.get(nv), expA=e.get('A'), expB=e.get('B'), nmord=nm.get(nv),
                        W=r['W'], n_sem=r['n_sem'], n_des=r['n_des'], deaths=r['deaths'], celdas=r['celdas'],
                        lig=[list(x) for x in lig[:4]]))
    v = [o['exp'] for o in out if o['exp'] is not None]
    p = os.path.join(AQUI, f'mini_B4_{esc}_sem{sem}.json')
    json.dump(dict(esc=esc, sem=sem, seeds=seeds, res=out), open(p, 'w'), indent=1)
    print(f"  EXPOSICIONES HASTA ASOCIAR [{nv}]: {[o['exp'] for o in out]}  mediana "
          f"{(np.median(v) if v else float('nan')):.1f}  (no asocia en {len(out)-len(v)}/{len(out)})"
          f"   muertes med {np.median([o['deaths'] for o in out]):.0f}   ({time.time()-t0:.1f} s)")
