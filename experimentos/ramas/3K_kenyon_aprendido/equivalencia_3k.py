"""
equivalencia_3k.py - prueba de que organismo_3k.run(mundo='AB', kenyon_mode='fijo')
es BIT-IDENTICO a organismo/organismo_v6.run() en todos los escenarios de la bateria.
Regla 5: primero el instrumento. Si esto no da 100%, nada de lo que sigue vale.
"""
import sys, os, json
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..', '..'))
sys.path.insert(0, os.path.join(ROOT, 'organismo'))
sys.path.insert(0, HERE)

import organismo_v6 as v6
import organismo_3k as o3

ESC = [
    ("E1", dict()),
    ("E1_sinaprender", dict(learn=False)),
    ("E2_inversion", dict(invertir_en=50000)),
    ("E2I_C", dict(nuevo='C')),
    ("E2J_D_solap1", dict(nuevo='D', nuevo_val='comida', solap_B=1)),
    ("E2K_D_solap2", dict(nuevo='D', nuevo_val='comida', solap_B=2)),
]

def norm(r):
    return json.dumps({k: r[k] for k in ('mord', 'vis', 'W', 'comp', 'deaths', 'solap')},
                      sort_keys=True, default=str)

if __name__ == "__main__":
    S = int(sys.argv[1]) if len(sys.argv) > 1 else 4
    tot = ok = 0
    for nombre, kw in ESC:
        for s in range(1, S + 1):
            a = v6.run(s, **kw)
            b = o3.run(s, mundo='AB', kenyon_mode='fijo', **kw)
            tot += 1
            same = norm(a) == norm(b)
            ok += same
            if not same:
                print(f"  DIFERENCIA en {nombre} semilla {s}")
                for f in ('mord', 'vis', 'W', 'comp', 'deaths', 'solap'):
                    if json.dumps(a[f], sort_keys=True, default=str) != json.dumps(b[f], sort_keys=True, default=str):
                        print(f"    campo {f}:\n      v6={a[f]}\n      3k={b[f]}")
    print(f"EQUIVALENCIA v6 vs 3k(mundo=AB, kenyon=fijo): {ok}/{tot} escenarios x semillas identicos")
    sys.exit(0 if ok == tot else 1)
