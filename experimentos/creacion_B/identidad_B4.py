"""Arnes de identidad de organismo_v14L.py (sem=0) contra organismo/organismo_v14.py (9bab8ac0685b1f21, CONGELADO).
Las claves NUEVAS (medida y organo) se excluyen: son anadido, no cambio.
Uso:  python experimentos/creacion_B/identidad_B4.py
"""
import json, os, sys, time, hashlib
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
sys.path[:0] = [AQUI, os.path.join(RAIZ, 'organismo')]
import organismo_v14 as ORI
import organismo_v14L as B

NUEVAS = {'sem', 'exp_hasta', 'n_mord', 'n_sem', 'n_des', 'sem_log', 'rel_arista', 'n_nodos'}
CASOS = [
    ('base T=100k', dict(), [1, 2, 3]),
    ('inversion en 50k', dict(invertir_en=50000), [1, 2]),
    ('nuevo C veneno', dict(nuevo='C', nuevo_en=50000, nuevo_val='veneno'), [1, 2]),
    ('nuevo D comida solap_B=2', dict(nuevo='D', nuevo_en=50000, nuevo_val='comida', solap_B=2), [1]),
]

def norm(d):
    return json.loads(json.dumps({k: v for k, v in d.items() if k not in NUEVAS}, default=str))

if __name__ == '__main__':
    t0 = time.time()
    print(f"origen organismo_v14.py  {hashlib.sha256(open(ORI.__file__,'rb').read()).hexdigest()[:16]}")
    print(f"gemelo organismo_v14L.py {hashlib.sha256(open(B.__file__,'rb').read()).hexdigest()[:16]}")
    ok = tot = 0
    for etiq, kw, seeds in CASOS:
        for s in seeds:
            a, b = norm(ORI.run(s, **kw)), norm(B.run(s, **kw, sem=0))
            tot += 1; dif = [k for k in a if a[k] != b.get(k)]; ok += not dif
            print(f"  [{time.time()-t0:6.1f}s] {etiq:30s} s{s}  {'IDENTICO' if not dif else 'DIFIERE ' + str(dif[:6])}", flush=True)
    print(f"\nIDENTIDAD {ok}/{tot}  ({time.time()-t0:.1f} s)")
    sys.exit(0 if ok == tot else 1)
