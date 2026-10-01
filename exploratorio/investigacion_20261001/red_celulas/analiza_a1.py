"""analiza_a1.py — comparaciones pareadas por semilla (bloque vs diccionario / kNN / barajado) y memoria tras la vuelta."""
import json, numpy as np
d = json.load(open('datos/a1.json'))
for reg in d:
    rs = d[reg]
    for a, b in (('4 bloque celulas', '2 diccionario'), ('4 bloque celulas', '3 kNN'), ('4 bloque celulas', '5 bloque barajado')):
        va = np.array([r[a]['media_camb'] for r in rs]); vb = np.array([r[b]['media_camb'] for r in rs]); dif = va - vb
        print(f"{reg:16s} {a} vs {b:18s} gana {int((dif > 0).sum())}/{len(rs)}  dif mediana {np.median(dif):+.3f}  "
              f"memoria {int(np.median([r[a]['mem_fin'] for r in rs]))} vs {int(np.median([r[b]['mem_fin'] for r in rs]))}")
rs = d['tandas_C100']
for b in ('4 bloque celulas', '3 kNN', '2 diccionario'):
    print(b, 'memoria mediana en t=3000/3500/4500:', [int(np.median([r[b]['mem'][r[b]['t'].index(t)] for r in rs])) for t in (3000, 3500, 4500)])
print('bloque tandas C100 (pisadas, nacimientos, muertes) 3 semillas:', [(r['4 bloque celulas']['pisadas'], r['4 bloque celulas']['nac'], r['4 bloque celulas']['mue']) for r in rs[:3]])
