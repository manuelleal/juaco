"""CREADOR A — que GEOMETRIA local elige la solucion que generaliza (continuacion de identificabilidad_xor.py).

Resultado previo (misma carpeta): con los 21 rasgos cuadraticos, el interpolante de minima norma L2 da 0.562 y el
de minima norma L1 da 0.562 (mediana, 20 semillas) — o sea que NI la geometria aditiva (regla delta) NI la
multiplicativa/dispersa (EG+-/Winnow/L1) identifican XOR. Con los 4 rasgos del oraculo {P0,P1,P0P1,1} el mismo
interpolante L2 da 1.000. Luego el limite es de SELECCION DE RASGOS, y la dispersion es el sesgo EQUIVOCADO:
en este espacio los rasgos de orden alto (productos) son casi funciones delta (P_i*P_j activo en 4 de 20 patrones,
un pixel en 10 de 20), asi que la solucion mas dispersa es la que MEMORIZA.

Hipotesis de esta sonda: el sesgo correcto es el CONTRARIO de la dispersion — preferir los rasgos FRECUENTES
(orden bajo) y usar los raros solo para el residuo que los frecuentes no explican ("elemental primero, configural
para el resto"; unique-cue de Deisig-Lachnit-Giurfa 2001). Como regla local eso es un PRECONDICIONADOR DIAGONAL:
    Delta w_i = eta * d_i * delta * phi_i,      d_i = gana local del rasgo i
cuyo sesgo implicito (arrancando en w=0) es el interpolante de minima norma PONDERADA  sum_i w_i^2 / d_i
(el iterado vive en el espacio fila de X*D, no de X). Se miden dos familias de d_i:
  - `grado`  d = 1 para pixeles (y constante), d = eps para productos  [idealizacion: la celda conjuntiva aprende mas lento]
  - `frec`   d_i = f_i^p, con f_i = fraccion de los 20 patrones del mundo en que el rasgo i esta activo
             (f_i es 100% LOCAL: cada rasgo lleva su propia tasa de disparo; no necesita saber su "orden")
Controles preregistrados aqui: la misma geometria sobre `px0` (regla lineal) debe quedar en 1.000 y sobre `azar`
en [0.35,0.65]; si `frec` sube xor01 pero rompe px0, el mecanismo no sirve.
Sin organismo, sin Pool, segundos.
"""
import sys, os, json
import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'nivel7_xor_lectura'))
import organismo_v13q as O

from identificabilidad_xor import phi, signo_acc, R_VAL, IJ


def min_D_norm(X, y, d):
    """Interpolante de minima norma ponderada sum w_i^2/d_i  =  D X^T (X D X^T)^+ y  (limite de la regla
    delta precondicionada `w <- w + eta*d*e*phi` arrancando en w=0)."""
    D = np.diag(d)
    XD = X @ D
    return D @ X.T @ np.linalg.pinv(XD @ X.T) @ y


def frecuencias(pats, lectura, constante):
    F = np.array([phi(pats[k], lectura, constante) for k in sorted(pats)])
    return F.mean(axis=0)   # f_i = fraccion de los 20 patrones en que el rasgo esta activo


def corrida(seed, regla, lectura, constante, d_fn):
    pats, tren, test, vr = O.split_regla(seed, regla)
    F = {k: phi(pats[k], lectura, constante) for k in pats}
    X = np.array([F[k] for k in tren]); y = np.array([R_VAL[vr[k]] for k in tren])
    d = d_fn(pats, lectura, constante)
    w = min_D_norm(X, y, d)
    pred = {k: float(F[k] @ w) for k in pats}
    resid = float(np.abs(X @ w - y).max())
    return signo_acc(pred, test, vr), resid, w


def med(xs):
    xs = [x for x in xs if x is not None]
    return (round(float(np.median(xs)), 3), round(float(min(xs)), 3), round(float(max(xs)), 3)) if xs else None


if __name__ == '__main__':
    semillas = list(range(1, 21))
    pats0 = O.patrones_regla()
    NPX = 6
    filas = []

    def d_grado(eps, cte_libre=True):
        def f(pats, lectura, constante):
            n = (6 if lectura == 'lineal' else 21) + (1 if constante else 0)
            d = np.ones(n)
            if lectura != 'lineal':
                d[NPX:NPX + 15] = eps
            if constante and not cte_libre:
                d[-1] = eps
            return d
        return f

    def d_frec(p):
        def f(pats, lectura, constante):
            fr = frecuencias(pats, lectura, constante)
            return np.maximum(fr, 1e-12) ** p
        return f

    print('=== familia `grado` (productos con gana eps; pixeles y constante con gana 1) — lectura cuadratica+1 ===')
    print(f'{"eps":>8} {"xor01":>22} {"px0":>22} {"azar":>22} {"resid max":>10}')
    for eps in [1.0, 0.3, 0.1, 0.03, 0.01, 0.003, 0.001, 1e-4, 1e-6]:
        out = {}
        rmax = 0.0
        for regla in ('xor01', 'px0', 'azar'):
            accs = []
            for s in semillas:
                a, r, _ = corrida(s, regla, 'cuadratica', True, d_grado(eps))
                accs.append(a); rmax = max(rmax, r)
            out[regla] = med(accs)
        print(f'{eps:>8} {str(out["xor01"]):>22} {str(out["px0"]):>22} {str(out["azar"]):>22} {rmax:>10.2e}')
        filas.append(dict(familia='grado', par=eps, **{k: out[k] for k in out}))

    print('\n=== familia `frec` (d_i = f_i^p, f_i = tasa de disparo local del rasgo) — lectura cuadratica+1 ===')
    print(f'{"p":>8} {"xor01":>22} {"px0":>22} {"azar":>22} {"resid max":>10}')
    for p in [-2.0, -1.0, 0.0, 1.0, 2.0, 3.0, 4.0, 6.0, 8.0]:
        out = {}; rmax = 0.0
        for regla in ('xor01', 'px0', 'azar'):
            accs = []
            for s in semillas:
                a, r, _ = corrida(s, regla, 'cuadratica', True, d_frec(p))
                accs.append(a); rmax = max(rmax, r)
            out[regla] = med(accs)
        print(f'{p:>8} {str(out["xor01"]):>22} {str(out["px0"]):>22} {str(out["azar"]):>22} {rmax:>10.2e}')
        filas.append(dict(familia='frec', par=p, **{k: out[k] for k in out}))

    print('\n=== mecanismo: pesos medios (xor01, cuadratica+1) en las tres geometrias ===')
    for nombre, dfn in (('L2 plano (p=0)', d_frec(0.0)), ('frec p=4', d_frec(4.0)), ('grado eps=0.01', d_grado(0.01))):
        WS = []
        for s in semillas:
            _, _, w = corrida(s, 'xor01', 'cuadratica', True, dfn); WS.append(w)
        W = np.array(WS)
        prods = np.abs(W[:, 6:21]); otros = np.delete(np.arange(15), 0)
        print(f'{nombre:>16}  wP0 {W[:,0].mean():+6.2f}  wP1 {W[:,1].mean():+6.2f}  '
              f'wP2..P5 {W[:,2:6].mean():+6.2f}  w(P0P1) {W[:,6].mean():+6.2f}  '
              f'|prod irrelev| {prods[:, otros].mean():5.2f}  cte {W[:,-1].mean():+6.2f}')

    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'sesgo_grado_xor.json'), 'w') as fh:
        json.dump(filas, fh, indent=1)
    print('\nOK -> sesgo_grado_xor.json')
