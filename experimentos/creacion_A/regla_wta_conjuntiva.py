"""CREADOR A — REGLA PROPUESTA: rasgos elementales siempre plasticos + rasgos conjuntivos que COMPITEN por abrirse
(inhibicion lateral / ganador-se-lo-lleva sobre el residuo). Version online de lo que el banco ya valido.

Lo que dice el banco (misma carpeta, 20 semillas, xor01, nunca vistos, formula `signo_acc` del registro):
   geometria de NORMA sobre los 22 rasgos       L2 0.562 · L1 0.625 · dos canales (regla real) 0.562 · margen 0.500
   via rapida sola (Kenyon K=1..7)              0.406-0.500 (no mejora con K)
   oraculo {P0,P1,P0P1,1}                       1.000
   SELECCION hacia adelante (matching pursuit)  arranque {6 px}          m=7  -> 0.625
                                                arranque {6 px + cte}    m=7  -> 1.000   <-- aqui
La diferencia entre 0.562 y 1.000 no es la norma: es SELECCION (abrir UN rasgo conjuntivo) contra ENCOGIMIENTO
(repartir el residuo entre los 15). Un regularizador convexo encoge; para seleccionar hace falta COMPETENCIA.

REGLA (local, un escalar extra por rasgo conjuntivo, tres factores):
  elementales (6 px + constante): ganancia 1 siempre.
  conjuntivo i: lleva  e_i <- (1-rho)*e_i + rho*d   SOLO cuando phi_i = 1   (= media movil del residuo cuando el
    rasgo esta activo; un escalar, actualizacion local, sin normalizar nada global).
  competencia: entre los conjuntivos CERRADOS, el de mayor |e_i| se ABRE si |e_i| > theta y quedan cupos.
  aprendizaje: Ws_i <- Ws_i + eta*d*phi_i  SOLO para los rasgos abiertos;  d = R - Ws@phi_abierto.
Por que deberia funcionar: mientras los elementales explican lo que pueden, d es el RESIDUO elemental; e_i es
la media del residuo bajo el rasgo i, es decir su correlacion con lo no explicado. El rasgo conjuntivo que
sostiene estructura no explicada gana la competencia; los demas ven su e_i caer a cero en cuanto el ganador
explica el residuo. El cupo mantiene #rasgos abiertos < #ejemplos: el sistema se queda SOBREdeterminado, que es
la unica razon por la que el oraculo generaliza.
Controles que pueden fallar: px0 (lineal) debe quedar >= 0.90 — si la competencia abre conjuntivos donde no hacen
falta, px0 cae; azar debe quedar en [0.35,0.65] — si sube, la regla esta memorizando.
Sin organismo, sin Pool, segundos.
"""
import sys, os, json
import numpy as np

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(AQUI, '..', 'nivel7_xor_lectura'))
import organismo_v13q as O
from identificabilidad_xor import phi, signo_acc, R_VAL

NPX = 6; NPROD = 15   # phi = [6 px | 15 productos | 1]


def wta(X, y, eta=0.015, rho=0.05, theta=0.6, cupo=1, pasos=40000, rng=None, calienta=4000):
    n = X.shape[1]
    w = np.zeros(n); e = np.zeros(n)
    abierta = np.zeros(n, bool); abierta[:NPX] = True; abierta[-1] = True     # elementales + constante
    conj = np.zeros(n, bool); conj[NPX:NPX + NPROD] = True
    hist = []
    for t in range(pasos):
        i = int(rng.integers(len(y))); ph = X[i]
        d = y[i] - float(w[abierta] @ ph[abierta])
        act = ph > 0
        e[act] = (1 - rho) * e[act] + rho * d                                # media movil del residuo bajo el rasgo
        if t >= calienta and int((abierta & conj).sum()) < cupo:             # competencia entre conjuntivos cerrados
            cand = conj & ~abierta
            if cand.any():
                j = int(np.argmax(np.where(cand, np.abs(e), -1.0)))
                if abs(e[j]) > theta:
                    abierta[j] = True; hist.append((t, j, float(e[j])))
        w[abierta] = w[abierta] + eta * d * ph[abierta]
    return w, [h[1] for h in hist]


def evalua(seed, regla, **kw):
    pats, tren, test, vr = O.split_regla(seed, regla)
    F = {k: phi(pats[k], 'cuadratica', True) for k in pats}
    X = np.array([F[k] for k in tren]); y = np.array([R_VAL[vr[k]] for k in tren])
    w, abiertos = wta(X, y, rng=np.random.default_rng(seed), **kw)
    pred = {k: float(F[k] @ w) for k in pats}
    return signo_acc(pred, test, vr), abiertos


def med(xs):
    xs = [x for x in xs if x is not None]
    return (round(float(np.median(xs)), 3), round(float(min(xs)), 3), round(float(max(xs)), 3)) if xs else None


if __name__ == '__main__':
    S = list(range(1, 21))
    NOM = [f'px{i}' for i in range(6)] + [f'{i}x{j}' for i in range(6) for j in range(i + 1, 6)] + ['1']
    filas = []
    print('=== barrido (theta, cupo, rho) — mediana [min,max] de 20 semillas ===')
    print(f'{"theta":>6} {"cupo":>5} {"rho":>5} {"xor01":>22} {"px0":>22} {"azar":>22} {"gana 0x1":>9}')
    for cupo in (1, 2):
        for theta in (0.3, 0.6, 1.0, 1.5, 2.0):
            for rho in (0.05,):
                fila = {}; gana = 0
                for regla in ('xor01', 'px0', 'azar'):
                    res = [evalua(s, regla, theta=theta, cupo=cupo, rho=rho) for s in S]
                    fila[regla] = med([r[0] for r in res])
                    if regla == 'xor01':
                        gana = sum(1 for r in res if 6 in r[1])      # indice 6 = P0*P1
                print(f'{theta:>6} {cupo:>5} {rho:>5} {str(fila["xor01"]):>22} {str(fila["px0"]):>22} '
                      f'{str(fila["azar"]):>22} {gana:>6}/20')
                filas.append(dict(theta=theta, cupo=cupo, rho=rho, **fila))

    print('\n--- detalle del mejor punto (theta=1.0, cupo=1): que conjuntivo abre cada semilla, xor01 ---')
    for s in S:
        a, ab = evalua(s, 'xor01', theta=1.0, cupo=1)
        print(f'  s{s:>2} acc={a:<8} abre={[NOM[i] for i in ab]}')
    with open(os.path.join(AQUI, 'regla_wta_conjuntiva.json'), 'w') as fh:
        json.dump(filas, fh, indent=1)
    print('\nOK -> regla_wta_conjuntiva.json')
