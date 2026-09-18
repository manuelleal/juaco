"""CREADOR A — sonda de IDENTIFICABILIDAD de la via lenta (bloque 3e, sin correr el organismo).

Pregunta: el diagnostico del registro (3d) dice que con 8 patrones de tren y 21 rasgos la particion XOR esta
INDETERMINADA. Eso es cierto para CUALQUIER regla, pero un sistema indeterminado no es indecidible: la regla local
elige UNA de las infinitas soluciones, y cual elige lo fija la GEOMETRIA de su actualizacion (su regularizador
implicito). Esta sonda mide, sin organismo, que solucion elige cada geometria y si generaliza.

Teorema usado (Widrow-Hoff / mirror descent; se cita, no se descubre aqui):
  - la regla delta aditiva `w <- w + eta*e*phi` arrancando en w=0 se queda SIEMPRE en el espacio fila de los datos,
    luego su unico punto fijo interpolante es el interpolante de MINIMA NORMA L2.
  - una regla MULTIPLICATIVA (EG+-/Winnow, Kivinen-Warmuth 1997) es descenso espejo con entropia: su sesgo
    implicito es el interpolante de minima ENTROPIA RELATIVA, que en el limite de masa chica se comporta como
    minima norma L1 (solucion dispersa).
Por tanto: si el interpolante min-L2 NO generaliza y el min-L1 SI, el limite de 3d no es "identificabilidad"
a secas sino SESGO INDUCTIVO EQUIVOCADO, y la reparacion es cambiar la geometria de la regla, no el mundo.

No toca ningun archivo original: importa `organismo_v13q` SOLO para `split_regla`/`patrones_regla`.
Sin Pool, sin organismo, segundos.
"""
import sys, os, json, itertools
import numpy as np
from scipy.optimize import linprog

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'nivel7_xor_lectura'))
import organismo_v13q as O   # solo split_regla / patrones_regla (no se corre el organismo)

R_VAL = {'comida': 1.0, 'veneno': -3.0}
IJ = [(i, j) for i in range(6) for j in range(i + 1, 6)]


def phi(P, lectura='cuadratica', constante=False, R15=None):
    if lectura == 'lineal':
        b = np.asarray(P, float)
    elif lectura == 'cuadratica':
        b = np.concatenate([P, [P[i] * P[j] for i, j in IJ]])
    elif lectura == 'oraculo':          # {P0, P1, P0*P1} (el "oraculo" de rasgos del 3e preregistrado)
        b = np.array([P[0], P[1], P[0] * P[1]], float)
    elif lectura == 'random15':
        b = np.concatenate([P, R15[tuple(float(v) for v in P)]])
    else:
        raise ValueError(lectura)
    return np.concatenate([b, [1.0]]) if constante else b


def signo_acc(pred, test, vr):
    """Misma formula que corre_xor_3d.signo_acc (balanceado, empate exacto = 0.5)."""
    f = [1.0 if pred[k] > 0 else (0.5 if pred[k] == 0 else 0.0) for k in test if vr[k] == 'comida']
    p = [1.0 if pred[k] < 0 else (0.5 if pred[k] == 0 else 0.0) for k in test if vr[k] == 'veneno']
    if not f or not p:
        return None
    return 0.5 * float(np.mean(f)) + 0.5 * float(np.mean(p))


def min_l1_interpolante(X, y, tol=1e-9):
    """min ||w||_1 s.a. X w = y  (LP estandar con w = u - v, u,v >= 0)."""
    n = X.shape[1]
    c = np.ones(2 * n)
    Aeq = np.hstack([X, -X])
    res = linprog(c, A_eq=Aeq, b_eq=y, bounds=[(0, None)] * (2 * n), method='highs')
    if not res.success:
        return None
    w = res.x[:n] - res.x[n:]
    w[np.abs(w) < tol] = 0.0
    return w


def min_l2_interpolante(X, y):
    return np.linalg.pinv(X) @ y


def analiza(seed, lectura='cuadratica', constante=False, regla='xor01'):
    pats, tren, test, vr = O.split_regla(seed, regla)
    R15 = None
    if lectura == 'random15':
        rr = np.random.default_rng(seed + 900000); R15 = {}
        for n in range(64):
            Pb = tuple(float((n >> (5 - j)) & 1) for j in range(6)); R15[Pb] = rr.integers(0, 2, 15).astype(float)
    F = {k: phi(pats[k], lectura, constante, R15) for k in pats}
    X = np.array([F[k] for k in tren]); y = np.array([R_VAL[vr[k]] for k in tren])
    out = dict(seed=seed, lectura=lectura, constante=constante, n_tren=len(tren), n_rasgos=X.shape[1],
               rango=int(np.linalg.matrix_rank(X)))
    # clases XOR representadas en el tren (cota de muestreo de C)
    cls = {}
    for k in tren:
        c = (int(pats[k][0]), int(pats[k][1])); cls[c] = cls.get(c, 0) + 1
    out['clases_tren'] = {f'{a}{b}': n for (a, b), n in sorted(cls.items())}
    out['clases_vacias'] = 4 - len(cls)
    for nombre, w in (('L2', min_l2_interpolante(X, y)), ('L1', min_l1_interpolante(X, y))):
        if w is None:
            out[f'acc_{nombre}'] = None; continue
        resid = float(np.abs(X @ w - y).max())
        pred = {k: float(F[k] @ w) for k in pats}
        out[f'acc_{nombre}'] = signo_acc(pred, test, vr)
        out[f'acc_tren_{nombre}'] = signo_acc(pred, tren, vr)
        out[f'resid_{nombre}'] = round(resid, 9)
        out[f'nnz_{nombre}'] = int((np.abs(w) > 1e-6).sum())
        out[f'l1_{nombre}'] = round(float(np.abs(w).sum()), 3)
        out[f'l2_{nombre}'] = round(float(np.linalg.norm(w)), 3)
        if lectura == 'cuadratica':
            out[f'w01_{nombre}'] = round(float(w[6]), 3)     # indice 6 = producto P0*P1
            out[f'wP0_{nombre}'] = round(float(w[0]), 3); out[f'wP1_{nombre}'] = round(float(w[1]), 3)
    return out


def med(xs):
    xs = [x for x in xs if x is not None]
    return (round(float(np.median(xs)), 3), round(float(min(xs)), 3), round(float(max(xs)), 3)) if xs else None


if __name__ == '__main__':
    semillas = list(range(1, 21))
    escenarios = [('cuadratica', False), ('cuadratica', True), ('lineal', False), ('lineal', True),
                  ('oraculo', True), ('oraculo', False), ('random15', False)]
    todo = []
    print(f'{"lectura":>12} {"cte":>4} {"rasgos":>7} {"acc_L2":>18} {"acc_L1":>18} {"nnzL1":>6} {"clases vacias":>14}')
    for lec, cte in escenarios:
        filas = [analiza(s, lec, cte) for s in semillas]
        todo += filas
        a2 = med([f['acc_L2'] for f in filas]); a1 = med([f['acc_L1'] for f in filas])
        nn = med([f.get('nnz_L1') for f in filas]); cv = sum(f['clases_vacias'] > 0 for f in filas)
        print(f'{lec:>12} {str(cte):>4} {filas[0]["n_rasgos"]:>7} '
              f'{str(a2):>18} {str(a1):>18} {str(nn[0] if nn else None):>6} {cv:>10}/{len(filas)}')
    # detalle del escenario que replica 3b/3d (cuadratica sin constante)
    print('\n--- cuadratica sin constante, por semilla (el escenario de 3b/3d: acc_lenta medida 0.500) ---')
    print(f'{"s":>3} {"rango":>5} {"acc_L2":>7} {"acc_L1":>7} {"nnzL1":>6} {"w(P0P1) L1":>11} {"wP0 L1":>7} {"wP1 L1":>7} {"clases":>18}')
    for f in [x for x in todo if x['lectura'] == 'cuadratica' and not x['constante']]:
        print(f'{f["seed"]:>3} {f["rango"]:>5} {f["acc_L2"]:>7} {f["acc_L1"]:>7} {f["nnz_L1"]:>6} '
              f'{f["w01_L1"]:>11} {f["wP0_L1"]:>7} {f["wP1_L1"]:>7} {str(f["clases_tren"]):>18}')
    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'identificabilidad_xor.json'), 'w') as fh:
        json.dump(todo, fh, indent=1)
    print('\nOK -> identificabilidad_xor.json')
