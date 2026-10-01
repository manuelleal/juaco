"""analiza_mover.py -- tabla del experimento 'mover' (datos/mover.json) -> datos/tabla_mover.txt"""
import json, os, numpy as np

def f(v, d=2):
    v = [x for x in v if x is not None]
    return f'{np.median(v):.{d}f} [{min(v):.{d}f}-{max(v):.{d}f}]' if v else '-'

def exp09(v):
    ok = [x for x in v if x is not None]
    return (f'{int(np.median(ok))} [{min(ok)}-{max(ok)}]' if ok else 'nunca') + f' ({len(ok)}/{len(v)})'

res = json.load(open(os.path.join('datos', 'mover.json')))
L = ['tarea | D | modo | acierto final | exp->0.9 | semillas con 0.9 en <300 | saltos ent->sal al final | dist media a la salida al final']
for tarea in ('mayoria', 'paridad'):
    for D in (3, 10, 40):
        for modo in ('rico', 'azar', 'quieto'):
            g = [o for o in res if o.get('tarea') == tarea and o['D'] == D and o['modo_mover'] == modo]
            if not g: continue
            fase = 'B' if tarea == 'mayoria' else 'A'
            ex = [o['exp09_' + fase] for o in g]
            L.append(f"{tarea} | {D} | {modo} | {f([o['acierto_' + fase] for o in g])} | {exp09(ex)} | "
                     f"{sum(1 for x in ex if x is not None and x < 300)}/{len(g)} | {f([o['camino_final'] for o in g], 1)} | "
                     f"{f([o['dist_a_salida_final'] for o in g])}")
txt = '\n'.join(L); print(txt); open(os.path.join('datos', 'tabla_mover.txt'), 'w', encoding='utf-8').write(txt)
