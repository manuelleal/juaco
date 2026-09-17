"""Diagnostico del control negativo para v13 (ERR-21). NO decide la congelacion; mide 3' y 3'' en semillas 81-100.
  3'  : v13(plast=False, solap_AB=3, eta_s=0)  -> la via rapida sola debe FALLAR E2L (como v11), >= 19/20
  3'' : v13(plast=False, solap_AB=3)          -> con la via lenta activa PASA E2L (ya visto 20/20 en el examen)
Uso:  python experimentos/v13_dos_vias/control3_v13.py
"""
import sys, os, json, time, hashlib
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
import numpy as np
AQUI = os.path.dirname(os.path.abspath(__file__)); RAIZ = os.path.dirname(os.path.dirname(AQUI))
sys.path.insert(0, os.path.join(RAIZ, 'organismo'))
SEEDS = list(range(81, 101))
pasa = lambda r: abs(r['W']['A'] - 1) < .15 and abs(r['W']['B'] + 3) < .3


def tarea(a):
    cual, s = a
    import organismo_v13 as v13
    kw = dict(plast=False, solap_AB=3)
    if cual == "3'": kw['eta_s'] = 0.0
    r = v13.run(s, **kw)
    return dict(cual=cual, seed=s, pasa=pasa(r), W_A=r['W']['A'], W_B=r['W']['B'], lenta_A=r['W_lenta']['A'], lenta_B=r['W_lenta']['B'])


if __name__ == '__main__':
    import multiprocessing as mp
    mp.set_start_method('spawn', force=True)
    stamp = time.strftime('%Y%m%d_%H%M%S')
    with mp.Pool(14) as pool:
        res = pool.map(tarea, [(c, s) for c in ("3'", "3''") for s in SEEDS], chunksize=1)
    V = {}
    for c in ("3'", "3''"):
        g = [r for r in res if r['cual'] == c]
        n = sum(r['pasa'] for r in g)
        V[c] = n
        print(f"  {c:4s} plast=False, A∩B=3{', eta_s=0 (via rapida sola)' if c == chr(51)+chr(39) else ' (via lenta activa)'}: pasan E2L {n}/20"
              f"  W_A mediana {np.median([r['W_A'] for r in g]):+.2f}  W_B {np.median([r['W_B'] for r in g]):+.2f}"
              f"  lenta_A {np.median([r['lenta_A'] for r in g]):+.2f}  lenta_B {np.median([r['lenta_B'] for r in g]):+.2f}")
    print(f"  3'  (rapida sola debe FALLAR, pasan <= 1/20): {'SOSTENIDA' if V[chr(51)+chr(39)] <= 1 else 'REFUTADA'}")
    print(f"  3'' (lenta activa PASA, >= 19/20): {'SOSTENIDA' if V[chr(51)+chr(39)+chr(39)] >= 19 else 'REFUTADA'}")
    dj = os.path.join(RAIZ, 'datos', f'control3_v13_{stamp}.json')
    json.dump(dict(meta=dict(fecha=stamp, semillas=SEEDS, veredictos={k: int(v) for k, v in V.items()},
                             sha_v13=hashlib.sha256(open(os.path.join(RAIZ, 'organismo', 'organismo_v13.py'), 'rb').read()).hexdigest()[:16]),
                   corridas=res), open(dj, 'w', encoding='utf-8'), ensure_ascii=False)
    print(f"  datos -> {os.path.basename(dj)}")
