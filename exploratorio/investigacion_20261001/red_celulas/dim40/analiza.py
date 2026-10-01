"""analiza.py -- tablas (mediana [min-max]) de datos/*.json -> datos/tablas.txt"""
import json, glob, os, numpy as np

def f(v, d=2):
    v = [x for x in v if x is not None]
    if not v: return '-'
    return f'{np.median(v):.{d}f} [{min(v):.{d}f}-{max(v):.{d}f}]'

def exp09(v):
    ok = [x for x in v if x is not None]
    return (f'{int(np.median(ok))} [{min(ok)}-{max(ok)}]' if ok else 'nunca') + f' ({len(ok)}/{len(v)})'

lineas = []
for fn in sorted(glob.glob(os.path.join('datos', '*.json'))):
    res = json.load(open(fn)); lineas.append(f'\n== {fn} ({len(res)} corridas) ==')
    claves = sorted({(o['D'], o['brazo'], o['lam']) for o in res}, key=lambda c: (c[1], c[0], c[2]))
    lineas.append('brazo | D | lam | acierto A | exp->0.9 A | acierto B | exp->0.9 B | camino ent->sal | celulas utiles | utiles con premio | tramposas | corr premio-aporte')
    for D, br, lam in claves:
        g = [o for o in res if o['D'] == D and o['brazo'] == br and o['lam'] == lam]
        c = lambda k: [o.get(k) for o in g]
        lineas.append(f"{br} | {D} | {lam} | {f(c('acierto_A'))} | {exp09(c('exp09_A'))} | {f(c('acierto_B'))} | {exp09(c('exp09_B'))} | "
                      f"{f(c('camino_medio'),1)} | {f(c('celulas_utiles'),0)} | {f(c('utiles_con_premio'),0)} | {f(c('tramposas'),0)} | {f(c('corr_premio_aporte'))}")
txt = '\n'.join(lineas); print(txt); open(os.path.join('datos', 'tablas.txt'), 'w', encoding='utf-8').write(txt)
