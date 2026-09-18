"""CREADOR A — MECANISMO PROPUESTO: "el rasgo se gana su plasticidad" (puerta de rasgo por elegibilidad).

Por que hace falta otra cosa (resultado del banco, misma carpeta): con los 21-22 rasgos cuadraticos NINGUNA
geometria de norma llega a 0.75 — L2 0.562, L1 0.625, dos canales (la regla real) 0.562, maximo margen 0.500,
seleccion por consistencia marginal 0.50-0.59, via rapida sola (Kenyon K=1..7) 0.41-0.50. El oraculo de 4 rasgos
{P0,P1,P0P1,1} da 1.000. La razon es de conteo: con 8 patrones y 4 rasgos el sistema es SOBREdeterminado y
consistente (solucion unica -> generaliza); con 8 patrones y 22 rasgos es subdeterminado (13 dimensiones libres)
y el regularizador solo elige entre soluciones que ya son todas compatibles con lo visto. Ninguna NORMA arregla
eso; hay que mantener el numero de rasgos ACTIVOS por debajo del numero de ejemplos.

MECANISMO (local, tres factores, un escalar extra por rasgo):
  cada rasgo i lleva una ELEGIBILIDAD  e_i <- (1-rho)*e_i + rho*(delta * phi_i)        [media movil local]
  y su ganancia es una PUERTA:         d_i = 1 si |e_i| > theta_r  (abierta), 0 si no   [con histeresis opcional]
  la actualizacion es la regla delta precondicionada:  w_i <- w_i + eta * d_i * delta * phi_i
Un rasgo irrelevante ve su correlacion con el error RESIDUAL caer a cero en cuanto los rasgos ya abiertos
explican lo que el explicaba: su puerta no abre. Un rasgo que sostiene estructura no explicada mantiene |e_i|
alto y se abre. El conjunto activo crece de a uno y se auto-limita -> el sistema se queda sobredeterminado.
Idealizacion sin ruido = matching pursuit (seleccion hacia adelante por correlacion con el residuo); aqui se
mide LAS DOS: la idealizacion (OMP) y la regla online tal como iria en el organismo.

Controles preregistrados: px0 (regla lineal) debe quedar >= 0.90 y azar en [0.35,0.65]; si la puerta sube xor01
rompiendo px0, el mecanismo no sirve. Sin organismo, sin Pool, segundos.
"""
import sys, os, json
import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'nivel7_xor_lectura'))
import organismo_v13q as O
from identificabilidad_xor import phi, signo_acc, R_VAL


def omp(X, y, m, semilla_px=0):
    """Matching pursuit ortogonal: arranca con los primeros `semilla_px` rasgos siempre abiertos y anade de a uno
    el rasgo mas correlacionado con el residuo, hasta `m` rasgos abiertos en total."""
    n = X.shape[1]; S = list(range(semilla_px))
    w = np.zeros(n)
    if S:
        w[S] = np.linalg.pinv(X[:, S]) @ y
    r = y - X @ w
    while len(S) < m:
        c = np.abs(X.T @ r); c[S] = -1
        j = int(np.argmax(c))
        if c[j] <= 1e-12: break
        S.append(j)
        w = np.zeros(n); w[S] = np.linalg.pinv(X[:, S]) @ y
        r = y - X @ w
    return w, S


def online_puerta(X, y, eta=0.015, rho=0.02, theta=0.35, pasos=40000, rng=None, hist=0.5):
    """La regla tal como iria en el organismo: elegibilidad local por rasgo + puerta sobre la ganancia.
    Devuelve w y el numero medio de puertas abiertas."""
    rng = rng or np.random.default_rng(0)
    n = X.shape[1]; w = np.zeros(n); e = np.zeros(n); abierta = np.zeros(n, bool)
    for t in range(pasos):
        i = int(rng.integers(len(y))); ph = X[i]
        d = y[i] - float(w @ ph)
        e = (1 - rho) * e + rho * (d * ph)
        abierta = np.where(np.abs(e) > theta, True, np.where(np.abs(e) < hist * theta, False, abierta))
        w = w + eta * abierta * d * ph
    return w, int(abierta.sum())


def evalua(seed, regla, geom, **kw):
    pats, tren, test, vr = O.split_regla(seed, regla)
    F = {k: phi(pats[k], 'cuadratica', True) for k in pats}
    X = np.array([F[k] for k in tren]); y = np.array([R_VAL[vr[k]] for k in tren])
    extra = None
    if geom == 'OMP':
        w, S = omp(X, y, kw['m'], kw.get('semilla_px', 0)); extra = sorted(S)
    elif geom == 'PUERTA':
        w, extra = online_puerta(X, y, rng=np.random.default_rng(seed), **kw)
    else:
        raise ValueError(geom)
    pred = {k: float(F[k] @ w) for k in pats}
    return signo_acc(pred, test, vr), extra


def med(xs):
    xs = [x for x in xs if x is not None]
    return (round(float(np.median(xs)), 3), round(float(min(xs)), 3), round(float(max(xs)), 3)) if xs else None


if __name__ == '__main__':
    S = list(range(1, 21))
    NOM = [f'px{i}' for i in range(6)] + [f'{i}x{j}' for i in range(6) for j in range(i + 1, 6)] + ['1']

    print('=== A. idealizacion (matching pursuit): cuantos rasgos abiertos hacen falta, y cuales ===')
    print(f'{"arranque":>10} {"m":>3} {"xor01":>22} {"px0":>22} {"azar":>22}')
    for semilla_px, etq in ((0, 'vacio'), (6, '6 px'), (7, '6px+cte')):
        for m in range(max(semilla_px, 1), min(semilla_px + 5, 12) + 1):
            if m > 11: break
            fila = {}
            for regla in ('xor01', 'px0', 'azar'):
                fila[regla] = med([evalua(s, regla, 'OMP', m=m, semilla_px=semilla_px)[0] for s in S])
            print(f'{etq:>10} {m:>3} {str(fila["xor01"]):>22} {str(fila["px0"]):>22} {str(fila["azar"]):>22}')

    print('\n--- que rasgos elige el matching pursuit en xor01 (arranque vacio, m=4), por semilla ---')
    cuenta = {}
    for s in S:
        a, Sx = evalua(s, 'xor01', 'OMP', m=4, semilla_px=0)
        nom = [NOM[i] for i in Sx]
        for x in nom: cuenta[x] = cuenta.get(x, 0) + 1
        print(f'  s{s:>2} acc={a:<7} rasgos={nom}')
    print('  frecuencia:', dict(sorted(cuenta.items(), key=lambda kv: -kv[1])))

    print('\n=== B. la regla ONLINE con puerta de rasgo (la que iria en el organismo) ===')
    print(f'{"theta":>7} {"rho":>6} {"xor01":>22} {"px0":>22} {"azar":>22} {"puertas abiertas (xor01)":>26}')
    for theta in (0.15, 0.25, 0.35, 0.5, 0.75, 1.0):
        for rho in (0.02,):
            fila = {}; ab = None
            for regla in ('xor01', 'px0', 'azar'):
                res = [evalua(s, regla, 'PUERTA', theta=theta, rho=rho) for s in S]
                fila[regla] = med([r[0] for r in res])
                if regla == 'xor01': ab = med([r[1] for r in res])
            print(f'{theta:>7} {rho:>6} {str(fila["xor01"]):>22} {str(fila["px0"]):>22} '
                  f'{str(fila["azar"]):>22} {str(ab):>26}')
    print('\nOK')
