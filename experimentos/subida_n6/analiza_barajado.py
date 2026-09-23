"""Diagnostico PREREGISTRADO (PREREGISTRO_n6.md §6, no es puerta): con la lectura por SIGNO (grad=1) el control
BARAJADO solo quita informacion en las semillas donde la permutacion CAMBIA el signo de valor(A)>0 / valor(B)<0.
Donde los signos se conservan, BARAJADO es el mismo mapa con otras magnitudes y deberia rodear como GF.
Se reporta limpio(rodeo) de BARAJADO partido en 'signos conservados' y 'signos rotos', y el de GF al lado.

Uso: python experimentos/subida_n6/analiza_barajado.py <ruta.json> <sello16>
"""
import hashlib, json, statistics, sys

sys.stdout.reconfigure(encoding='utf-8', errors='replace')
ruta, sello = sys.argv[1], sys.argv[2]
b = open(ruta, 'rb').read()
s = hashlib.sha256(b).hexdigest()[:16]
if s != sello:
    raise SystemExit(f"SELLO {s} != {sello}")
d = json.loads(b.decode('utf-8'))
if 'BARAJADO' not in d['por'] or 'GF' not in d['por']:
    raise SystemExit('faltan BARAJADO o GF')
g = {'conservados': [], 'rotos': []}
for sd, v in d['por']['BARAJADO'].items():
    k = 'conservados' if (v['v_A'] > 0 and v['v_B'] < 0) else 'rotos'
    g[k].append((sd, v['limpio']['rodeo'], d['por']['GF'][sd]['limpio']['rodeo']))
for k, L in g.items():
    if L:
        print(f"  BARAJADO signos {k:11s} n={len(L):2d}  limpio(rodeo) mediana {statistics.median(x[1] for x in L):.3f}"
              f"  (GF en las mismas semillas {statistics.median(x[2] for x in L):.3f})")
    else:
        print(f"  BARAJADO signos {k:11s} n= 0")
