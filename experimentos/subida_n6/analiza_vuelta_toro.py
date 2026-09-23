"""Candidato a ERR sobre el bloque 'rodeo obligado' (21-sep): UNA fila de veneno en un toro NO lo parte.

Toro 11 x 9 menos una fila = cilindro. El caso 'rodeo' arranca en (fx, -dd) y la comida esta en (fx, fy): cruzar la
muralla cuesta dd+fy pasos verticales; dar la VUELTA DEL TORO (alejarse de la muralla) cuesta 9-dd-fy y es LIMPIO.
Este script (regla 10b: el analisis lo hace un script del repo sobre el JSON sellado, nunca en linea) cuenta, en los
episodios 'rodeo' de la serie 1702-1721, cuantos tenian la vuelta del toro mas corta que cruzar, y de donde salieron
los 'limpio' de cada brazo.

Uso: python experimentos/subida_n6/analiza_vuelta_toro.py
"""
import hashlib, json, os, sys

sys.stdout.reconfigure(encoding='utf-8', errors='replace')
RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
RUTA = os.path.join(RAIZ, 'datos', 'muralla_s1702-1721_20260921_170652.json')
SELLO = '99dc2e86b833fc29'
ALTO, D_INI = 9, 5

b = open(RUTA, 'rb').read()
s = hashlib.sha256(b).hexdigest()[:16]
if s != SELLO:
    raise SystemExit(f"SELLO {s} != {SELLO}")
d = json.loads(b.decode('utf-8'))
assert d['mundo']['alto'] == ALTO and d['mundo']['d_ini'] == D_INI
print(f"{os.path.relpath(RUTA, RAIZ)}  sello {s}")
for br in d['por']:
    cnt = {True: [0, 0], False: [0, 0]}; cero = 0
    for sd, v in d['por'][br].items():
        fy = v['geo']['fy']
        rc = [c for c in v['casos'] if c['caso'] == 'rodeo']
        for i, c in enumerate(rc):
            dd = 1 + i % D_INI                      # corre_muralla: _dd = 1 + (_i//2) % d_ini, y rodeo son los _i pares
            vuelta = (ALTO - dd - fy) < (dd + fy)   # la vuelta del toro (limpia) es MAS CORTA que cruzar la muralla
            cnt[vuelta][0] += c['limpio']; cnt[vuelta][1] += 1
            cero += int(c['d0'] == 0)
    tv, tn = cnt[True], cnt[False]
    print(f"  {br:10s} episodios rodeo con vuelta del toro mas corta: {tv[1]:3d} (limpio {tv[0]:3d} = {tv[0]/max(tv[1],1):.3f})"
          f" | rodeo de verdad (solo por el hueco): {tn[1]:3d} (limpio {tn[0]:3d} = {tn[0]/max(tn[1],1):.3f})"
          f" | arranca SOBRE la comida (d0=0): {cero}")
