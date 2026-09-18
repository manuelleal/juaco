"""Sala 2 / crece_codigo: dato ESTRUCTURAL para la clausula de muestreo del preregistro (no simula un paso del organismo).
Para cada semilla lee el reparto tren/test de xor01 con la MISMA funcion del mundo de regla (organismo_v14g.split_regla,
solo lectura) y cuenta cuantos patrones del tren tienen P0=P1=1 ('11'): son los unicos en los que el par (0,1) esta
CO-ACTIVO, es decir los unicos que pueden reclutar el nodo (0,1) por Hebb-en-la-sorpresa. Tambien cuenta los '00' y
cuantos pares distintos estan co-activos en el tren (cota superior de la ocupacion por reclutamiento).
Uso: python coactividad_tren_xor01.py [desde] [n]
"""
import sys, os, json, itertools
AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(AQUI)))
sys.path[:0] = [os.path.join(RAIZ, 'organismo')]   # organismo/ PRIMERO (ERR-28)
import organismo_v14g as G

desde = int(sys.argv[1]) if len(sys.argv) > 1 else 1101
n = int(sys.argv[2]) if len(sys.argv) > 2 else 40
filas = []
for s in range(desde, desde + n):
    pats, tren, test, vr = G.split_regla(s, 'xor01')
    n11 = sum(1 for k in tren if k[0] == '1' and k[1] == '1')
    n00 = sum(1 for k in tren if k[0] == '0' and k[1] == '0')
    pares = set()
    for k in tren:
        act = [i for i in range(6) if k[i] == '1']
        pares |= set(itertools.combinations(act, 2))
    filas.append(dict(seed=s, n11=n11, n00=n00, n_comida=sum(1 for k in tren if vr[k] == 'comida'),
                      pares_coactivos_tren=len(pares), par01_coactivo=(0, 1) in pares))
sin11 = [f['seed'] for f in filas if f['n11'] == 0]
print(json.dumps(dict(desde=desde, n=n, semillas_sin_11_en_tren=sin11,
                      n11_mediana=sorted(f['n11'] for f in filas)[n // 2],
                      pares_coactivos_mediana=sorted(f['pares_coactivos_tren'] for f in filas)[n // 2],
                      filas=filas), indent=1))
