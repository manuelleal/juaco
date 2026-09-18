"""CREADOR A — CUANTO CUESTA EL ORACULO: de "es dinamica" a un numero preregistrable.
(Encargo del coordinador tras 3e: `xor_3e_s61-80_20260917_231444` mide 0.625 con los rasgos exactos
{P0,P1,P0P1,1}; mi banco predice 1.000 para el interpolante al que converge esa misma regla. La diferencia es
DINAMICA: ~330 actualizaciones, refuerzo solo al morder, R = +1 / -3, y clases muy desiguales.)

Este script simula la regla de la via lenta SOBRE LOS RASGOS DEL ORACULO, sin mundo, con:
  - el numero n de actualizaciones (mordidas) como eje,
  - el muestreo por clase XOR: `uniforme` o `real` (las proporciones medidas por el Agente C en PUENTE_xor:
    00->46, 01->0, 10->272, 11->13 sobre 331 mordidas antes de la sonda), o `real_sin_ceros` (misma forma pero
    dando al menos 1 mordida a cada clase presente en el tren),
  - las dos reglas que usa el organismo: `dos_canales` (Wps/Wns >= 0 + drenaje lam + tope) y `delta_signo`,
  - `eta_s` variable.
Salida: n* = numero de actualizaciones con el que la mediana de `acc_lenta` (misma formula `signo_acc` del
registro) cruza 0.80, por muestreo y por eta_s. Eso convierte "es dinamica" en un criterio preregistrable:
"si el organismo da >= n* mordidas a la via lenta con clases no vacias, el oraculo debe cruzar 0.80".
Sin organismo, sin Pool, segundos.
"""
import sys, os, json
import numpy as np

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(AQUI, '..', 'nivel7_xor_lectura'))
import organismo_v13q as O
from identificabilidad_xor import signo_acc, R_VAL

# proporciones medidas por el Agente C (PUENTE_xor, hipotesis ii), semilla 1, xor01, antes de la sonda
REAL = {(0, 0): 46, (0, 1): 0, (1, 0): 272, (1, 1): 13}


def phi_or(P):
    return np.array([P[0], P[1], P[0] * P[1], 1.0])


def pesos_muestreo(tren, pats, modo):
    if modo == 'uniforme':
        return np.ones(len(tren))
    w = []
    for k in tren:
        c = (int(pats[k][0]), int(pats[k][1])); n = REAL[c]
        if modo == 'real_sin_ceros': n = max(n, 20)
        w.append(float(n))
    w = np.array(w)
    return w / w.sum() if w.sum() > 0 else np.ones(len(tren))


def simula(X, y, n, regla, eta_s=0.015, lam=0.05, clip_s=3.0, aversion=1.0, p=None, rng=None):
    rng = rng or np.random.default_rng(0)
    d = X.shape[1]; Wps = np.zeros(d); Wns = np.zeros(d); Ws = np.zeros(d)
    idx = rng.choice(len(y), size=n, p=(p / p.sum()) if p is not None else None)
    for i in idx:
        ph = X[i]
        if regla == 'delta_signo':
            ds = y[i] - float(Ws @ ph)
            Ws = np.clip(Ws + eta_s * ds * ph, -clip_s, clip_s)
        else:
            ds = y[i] - float((Wps - Wns) @ ph)
            if lam:
                mcs = np.minimum(Wps, Wns) * (ph > 0); Wps = Wps - lam * mcs; Wns = Wns - lam * mcs
            if ds > 0: Wps = np.clip(Wps + eta_s * ds * ph, 0, clip_s)
            else:      Wns = np.clip(Wns + eta_s * aversion * (-ds) * ph, 0, clip_s)
    return Ws if regla == 'delta_signo' else (Wps - Wns)


def acc(seed, n, regla, muestreo, eta_s):
    pats, tren, test, vr = O.split_regla(seed, 'xor01')
    F = {k: phi_or(pats[k]) for k in pats}
    X = np.array([F[k] for k in tren]); y = np.array([R_VAL[vr[k]] for k in tren])
    p = pesos_muestreo(tren, pats, muestreo)
    w = simula(X, y, n, regla, eta_s=eta_s, p=p, rng=np.random.default_rng(seed))
    return signo_acc({k: float(F[k] @ w) for k in pats}, test, vr)


def med(xs):
    xs = [x for x in xs if x is not None]
    return round(float(np.median(xs)), 3) if xs else None


if __name__ == '__main__':
    S = list(range(1, 21))
    NS = [50, 100, 200, 331, 500, 1000, 2000, 5000]
    filas = []
    for regla in ('dos_canales', 'delta_signo'):
        for eta_s in (0.015, 0.05):
            print(f'\n=== oraculo {{P0,P1,P0P1,1}} · regla {regla} · eta_s={eta_s} · mediana de 20 semillas ===')
            print(f'{"n actualizaciones":>18} ' + ' '.join(f'{m:>16}' for m in ('uniforme', 'real', 'real_sin_ceros')))
            for n in NS:
                v = [med([acc(s, n, regla, m, eta_s) for s in S]) for m in ('uniforme', 'real', 'real_sin_ceros')]
                print(f'{n:>18} ' + ' '.join(f'{x:>16}' for x in v), flush=True)
                filas.append(dict(regla=regla, eta_s=eta_s, n=n, uniforme=v[0], real=v[1], real_sin_ceros=v[2]))
    # n* por muestreo
    print('\n=== n* = primeras n con mediana >= 0.80 ===')
    for regla in ('dos_canales', 'delta_signo'):
        for eta_s in (0.015, 0.05):
            sub = [f for f in filas if f['regla'] == regla and f['eta_s'] == eta_s]
            fila = {}
            for m in ('uniforme', 'real', 'real_sin_ceros'):
                ok = [f['n'] for f in sub if f[m] is not None and f[m] >= 0.80]
                fila[m] = min(ok) if ok else '>30000'
            print(f'  {regla:>12} eta_s={eta_s:<6} uniforme={fila["uniforme"]:>7}  real={fila["real"]:>7}  '
                  f'real_sin_ceros={fila["real_sin_ceros"]:>7}')
    json.dump(filas, open(os.path.join(AQUI, 'dinamica_oraculo.json'), 'w'), indent=1)
    print('\nOK -> dinamica_oraculo.json')
