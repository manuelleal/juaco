"""REFUTADOR sala 2 (lente medibilidad) del diseno DISENO_dos_escalas.md. Calculos ESTRUCTURALES de solo lectura:
NO simula un paso del organismo, no usa Pool, no toca nada del repo. organismo/ PRIMERO en sys.path (ERR-28).
(1) Clausula de muestreo del diseno: cuantos '11' y '00' hay en el tren de xor01 en 181-200 y 201-220 (split_regla de v14g).
(2) Cuantos pares (i,j) son CONSISTENTES con el tren (casilla -> una sola valencia): mas de uno = competidor de (0,1)
    con error propio 0 tras sus primeras visitas (la 'racha de 10 victorias unicas' no garantiza que gane (0,1)).
(3) TECHO de informacion de la lectura 'sin tabla' del diseno (P4): ajuste de minimos cuadrados (el proxy del gradiente
    exacto que uso A-5) con los 7 rasgos del diseno {P0..P5, P0*P1}, sin sesgo (la lineal del tronco no lo tiene), sobre los
    8 patrones de tren con objetivos +1/-3, evaluado con la puntuacion ESTRICTA (signo; 0 = fallo) en los 12 nunca vistos.
    Tambien con los 6 pixeles solos (la lineal de v14.1) y con {P0,P1,P0*P1,1} (el oraculo de A-4) como referencia.
Uso: python refuta_dos_escalas_estructural.py   -> escribe refuta_dos_escalas_estructural.json
"""
import sys, os, json, itertools
import numpy as np
AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(AQUI)))
sys.path[:0] = [os.path.join(RAIZ, 'organismo')]
import organismo_v14g as G
R = {'comida': 1.0, 'veneno': -3.0}

def acc_estricta(pred, test, vr):
    f = [1.0 if pred[k] > 0 else 0.0 for k in test if vr[k] == 'comida']
    p = [1.0 if pred[k] < 0 else 0.0 for k in test if vr[k] == 'veneno']
    return None if (not f or not p) else 0.5 * float(np.mean(f)) + 0.5 * float(np.mean(p))

def rasgos(P, modo):
    if modo == 'lineal6': return np.array(P, float)
    if modo == 'lineal6+P0P1': return np.concatenate([P, [P[0] * P[1]]])
    if modo == 'oraculo': return np.array([P[0], P[1], P[0] * P[1], 1.0])
    raise ValueError(modo)

def lsq(pats, tren, test, vr, modo):
    X = np.array([rasgos(pats[k], modo) for k in tren]); y = np.array([R[vr[k]] for k in tren])
    w = np.linalg.lstsq(X, y, rcond=None)[0]
    pred = {k: float(rasgos(pats[k], modo) @ w) for k in pats}
    res = float(np.abs(X @ w - y).max())
    return acc_estricta(pred, test, vr), acc_estricta(pred, tren, vr), res

out = {}
for rango in [(181, 200), (201, 220), (161, 180)]:
    filas = []
    for s in range(rango[0], rango[1] + 1):
        pats, tren, test, vr = G.split_regla(s, 'xor01')
        n11 = sum(1 for k in tren if k[0] == '1' and k[1] == '1'); n00 = sum(1 for k in tren if k[0] == '0' and k[1] == '0')
        pares_ok = []
        for (i, j) in itertools.combinations(range(6), 2):
            cas = {}; ok = True
            for k in tren:
                c = (k[i], k[j])
                if c in cas and cas[c] != vr[k]: ok = False; break
                cas[c] = vr[k]
            if ok: pares_ok.append([i, j])
        fila = dict(seed=s, n11_tren=n11, n00_tren=n00, pares_consistentes_con_el_tren=pares_ok)
        for modo in ('lineal6', 'lineal6+P0P1', 'oraculo'):
            a_test, a_tren, res = lsq(pats, tren, test, vr, modo)
            fila[f'lsq_{modo}'] = dict(estricta_test=a_test, estricta_tren=a_tren, residuo_max_tren=round(res, 4))
        filas.append(fila)
    def med(xs): xs = [x for x in xs if x is not None]; return float(np.median(xs)) if xs else None
    resumen = {}
    for modo in ('lineal6', 'lineal6+P0P1', 'oraculo'):
        v = [f[f'lsq_{modo}']['estricta_test'] for f in filas]
        resumen[modo] = dict(mediana_test=med(v), n_ge_075=sum(1 for x in v if x is not None and x >= 0.75), n=len(v), valores=v)
    out[f'{rango[0]}-{rango[1]}'] = dict(
        semillas_sin_11_en_tren=[f['seed'] for f in filas if f['n11_tren'] == 0],
        semillas_sin_00_en_tren=[f['seed'] for f in filas if f['n00_tren'] == 0],
        semillas_con_mas_de_un_par_consistente=[(f['seed'], f['pares_consistentes_con_el_tren']) for f in filas if len(f['pares_consistentes_con_el_tren']) > 1],
        techo_lsq=resumen, filas=filas)
for k, v in out.items():
    print(f"== {k} ==  sin '11': {v['semillas_sin_11_en_tren']}  sin '00': {v['semillas_sin_00_en_tren']}")
    print(f"   >1 par consistente con el tren: {v['semillas_con_mas_de_un_par_consistente']}")
    for modo, r in v['techo_lsq'].items():
        print(f"   techo LSQ {modo:14s}: mediana estricta test {r['mediana_test']}  >=0.75 en {r['n_ge_075']}/{r['n']}  {[round(x,3) if x is not None else None for x in r['valores']]}")
json.dump(out, open(os.path.join(AQUI, 'refuta_dos_escalas_estructural.json'), 'w'), indent=1)
print('escrito refuta_dos_escalas_estructural.json')
