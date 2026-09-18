"""CREADOR A — (1) CONTROL POSITIVO con gradiente exacto y retropropagacion sobre EL MISMO flujo de encuentros,
(2) META-APRENDIZAJE de la regla local fuera del organismo, (3) EXPOSICIONES HASTA CRITERIO.

Entrada: `lab_eventos_<lectura>_<regla>.json`, cosechado por `cosecha_lab.py` con `organismo_v13q5(lab=True)`
(registro puro, identidad 16/16). Cada semilla trae la secuencia ORDENADA `(t, patron, R, residuo)` de todas las
actualizaciones de la via lenta. La actualizacion esta completamente determinada por esa secuencia, asi que aqui se
repite el MISMO flujo (mismo muestreo real, mismos rasgos, mismos encuentros) con lectores distintos:

  DELTA        la regla del tronco, replicada  (auto-comprobacion: debe reproducir el `acc_lenta` del organismo)
  DELTA_STOPE  la misma sin tope (`clip_s` = inf)              -> aisla el techo del tope
  LSQ          minimos cuadrados exactos (pinv) sobre los mismos (phi, R)   -> COTA SUPERIOR de cualquier lector
                                                                               lineal sobre esos rasgos
  RIDGE        idem con ridge 1e-3
  MLP          retropropagacion de laboratorio: 6 pixeles -> oculta(H, tanh) -> 1, lote completo, sobre los MISMOS
               encuentros. NO esta limitada a mis rasgos: es la cota superior "con backprop" del encargo.

PREDICCION ESCRITA ANTES DE MIRAR (18-sep): con el muestreo real, **ni LSQ ni MLP cruzan 0.75 de mediana**, porque
el techo es del mundo (una clase XOR sin morder). Si alguno lo cruza, el cuello es la regla y mi banco tiene que
explicar por que la delta no llega.

Uso: python banco_lab.py [lectura] [regla]
Sin organismo, sin Pool, segundos.
"""
import sys, os, json, itertools
import numpy as np

AQUI = os.path.dirname(os.path.abspath(__file__))
IJ = [(i, j) for i in range(6) for j in range(i + 1, 6)]
NOM = [f'px{i}' for i in range(6)] + [f'{i}x{j}' for i, j in IJ] + ['1']


def pat_de(nombre):
    return np.array([float(c) for c in nombre])


def phi_de(P, lectura, constante=True):
    if lectura == 'lineal': b = P
    elif lectura == 'cuadratica': b = np.concatenate([P, [P[i] * P[j] for i, j in IJ]])
    elif lectura == 'oraculo01': b = np.array([P[0], P[1], P[0] * P[1]])
    elif lectura == 'oraculo01_ruido': b = np.array([P[0], P[1], P[2] * P[3]])
    else: raise ValueError(lectura)
    return np.concatenate([b, [1.0]]) if constante else b


def signo_acc(pred, test, vr):
    f = [1.0 if pred[k] > 0 else (0.5 if pred[k] == 0 else 0.0) for k in test if vr[k] == 'comida']
    p = [1.0 if pred[k] < 0 else (0.5 if pred[k] == 0 else 0.0) for k in test if vr[k] == 'veneno']
    if not f or not p: return None
    return 0.5 * float(np.mean(f)) + 0.5 * float(np.mean(p))


# --------------------------------------------------------------------- lectores
def delta(X, y, eta=0.015, clip=3.0, lam=0.0, sel=None, theta=0.6, rho=0.05, cupo=1, estad='cond', npx=6, ncj=15):
    n = X.shape[1]; w = np.zeros(n); e = np.zeros(n)
    ab = np.ones(n, bool); cand = np.zeros(n, bool)
    if sel:
        cand[npx:npx + ncj] = True; ab = ~cand
    for i in range(len(y)):
        ph = X[i]; d = y[i] - float(w @ ph)
        if sel:
            act = ph > 0
            if estad == 'cond': e[act] = (1 - rho) * e[act] + rho * d
            else: e = (1 - rho) * e + rho * (d * ph)
            if int((ab & cand).sum()) < cupo:
                c = cand & ~ab
                if c.any():
                    j = int(np.argmax(np.where(c, np.abs(e), -1.0)))
                    if abs(e[j]) > theta: ab[j] = True
            ph = ph * ab
        w = np.clip(w * (1 - lam) + eta * d * ph, -clip, clip)
    return w


def lsq(X, y, ridge=0.0):
    if ridge:
        n = X.shape[1]
        return np.linalg.solve(X.T @ X + ridge * np.eye(n), X.T @ y)
    return np.linalg.pinv(X) @ y


def mlp(P, y, H=8, pasos=4000, eta=0.05, seed=0):
    """Retropropagacion de laboratorio: 6 px -> H (tanh) -> 1, lote completo, momento 0.9."""
    rng = np.random.default_rng(seed)
    W1 = rng.normal(0, 0.5, (6, H)); b1 = np.zeros(H); W2 = rng.normal(0, 0.5, H); b2 = 0.0
    v = [np.zeros_like(x) for x in (W1, b1, W2, np.array(0.0))]
    N = len(y)
    for t in range(pasos):
        Z = P @ W1 + b1; A = np.tanh(Z); o = A @ W2 + b2
        d = (o - y) / N
        gW2 = A.T @ d; gb2 = d.sum()
        dA = np.outer(d, W2) * (1 - A ** 2)
        gW1 = P.T @ dA; gb1 = dA.sum(0)
        for k, (p, g) in enumerate(((W1, gW1), (b1, gb1), (W2, gW2), (b2, gb2))):
            v[k] = 0.9 * v[k] - eta * g
        W1 = W1 + v[0]; b1 = b1 + v[1]; W2 = W2 + v[2]; b2 = b2 + float(v[3])
    return lambda Pq: float(np.tanh(Pq @ W1 + b1) @ W2 + b2)


# --------------------------------------------------------------------- evaluacion
def evalua(d, lectura, hasta=None, lector='DELTA', **kw):
    ev = [e for e in d['eventos'] if e[0] < d['fase2_en']]
    if hasta is not None: ev = ev[:hasta]
    if not ev: return None, 0
    P = np.array([pat_de(e[1]) for e in ev]); y = np.array([e[2] for e in ev])
    X = np.array([phi_de(p, lectura) for p in P])
    pats = {k: pat_de(k) for k in d['vr']}
    if lector == 'MLP':
        f = mlp(P, y, **kw); pred = {k: f(v) for k, v in pats.items()}
    else:
        if lector == 'LSQ': w = lsq(X, y)
        elif lector == 'RIDGE': w = lsq(X, y, ridge=1e-3)
        elif lector == 'DELTA_STOPE': w = delta(X, y, clip=1e9, **kw)
        else: w = delta(X, y, **kw)
        pred = {k: float(phi_de(v, lectura) @ w) for k, v in pats.items()}
    return signo_acc(pred, d['test'], d['vr']), len(ev)


def med(xs):
    xs = [x for x in xs if x is not None]
    return (round(float(np.median(xs)), 3), round(float(min(xs)), 3), round(float(max(xs)), 3)) if xs else None


if __name__ == '__main__':
    lectura = sys.argv[1] if len(sys.argv) > 1 else 'cuadratica'
    regla = sys.argv[2] if len(sys.argv) > 2 else 'xor01'
    D = json.load(open(os.path.join(AQUI, f'lab_eventos_{lectura}_{regla}.json')))
    S = sorted(D, key=int)
    print(f'=== flujo cosechado: {len(S)} semillas, lectura {lectura}, regla {regla} ===')
    npre = [D[s]['n_pre'] for s in S]; vac = [D[s]['clases_vacias'] for s in S]
    print(f'    eventos pre-sonda: mediana {int(np.median(npre))} [{min(npre)}, {max(npre)}]   '
          f'semillas con una clase XOR SIN MORDER: {sum(v > 0 for v in vac)}/{len(S)}')
    print(f'    acc_lenta del ORGANISMO: {med([D[s]["acc_lenta_organismo"] for s in S])}')

    print('\n=== (1) CONTROL POSITIVO — mismo flujo, mismos rasgos, distinto lector ===')
    print(f'{"lector":>13} {"TODAS las semillas":>22} {"solo las 4 clases mordidas":>28}')
    res = {}
    for lector in ('DELTA', 'DELTA_STOPE', 'LSQ', 'RIDGE', 'MLP'):
        a = {s: evalua(D[s], lectura, lector=lector)[0] for s in S}
        res[lector] = a
        llenas = [a[s] for s in S if D[s]['clases_vacias'] == 0]
        print(f'{lector:>13} {str(med([a[s] for s in S])):>22} {str(med(llenas)):>28}')
    dif = sum(1 for s in S if res['DELTA'][s] is not None and D[s]['acc_lenta_organismo'] is not None
              and abs(res['DELTA'][s] - D[s]['acc_lenta_organismo']) > 1e-9)
    print(f'    auto-comprobacion del replay: DELTA != organismo en {dif}/{len(S)} semillas')

    print('\n=== (3) EXPOSICIONES HASTA CRITERIO (primer n de encuentros con acierto >= criterio) ===')
    REJ = [10, 20, 40, 60, 100, 150, 200, 300, 400, 600]
    print(f'{"lector":>13} ' + ' '.join(f'{n:>6}' for n in REJ) + '   n* (>=0.65) / (>=0.75)')
    for lector in ('DELTA', 'LSQ', 'MLP'):
        fila = []
        for n in REJ:
            fila.append(med([evalua(D[s], lectura, hasta=n, lector=lector)[0] for s in S]))
        v = [f[0] if f else None for f in fila]
        n65 = next((n for n, x in zip(REJ, v) if x is not None and x >= 0.65), None)
        n75 = next((n for n, x in zip(REJ, v) if x is not None and x >= 0.75), None)
        print(f'{lector:>13} ' + ' '.join(f'{x:>6}' for x in v) + f'   {n65 or ">600"} / {n75 or ">600"}')
