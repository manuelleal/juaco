"""CREADOR A — BANCO ANALITICO DE SESGO INDUCTIVO para la via lenta y la via rapida (sin correr el organismo).

Idea: `acc_lenta` (acierto por signo en los nunca vistos, sonda a priori) es una propiedad de la GEOMETRIA de la
regla, no de la dinamica del mundo. Con 8 patrones de tren la regla delta aditiva arrancando en 0 converge al
interpolante de minima norma L2 del sistema X w = y; luego su `acc_lenta` se puede CALCULAR. Este banco calcula
`acc_lenta` de varias geometrias en segundos y sirve de filtro: lo que aqui no pasa de 0.56 no merece 200000 pasos.

Se valida contra lo YA medido en 3b/3d (mediana de 20 semillas):
    lineal 0.344-0.406 · cuadratica dos canales 0.500-0.562 · random15 0.469-0.500 · cuadratica+delta 0.500
Geometrias probadas aqui:
  L2        interpolante de minima norma L2 (= regla delta aditiva desde 0)             [3d medido: 0.500]
  L1        interpolante de minima norma L1 (= EG+-/Winnow/mirror descent entropico)
  DOSCAN    SIMULACION de la regla real de v13q (dos canales no negativos Wps/Wns + drenaje lam + tope clip_s)
            sobre los 8 patrones de tren, sin mundo: comprueba que el banco reproduce la regla del organismo
  PERCEP    maximo margen L2 (= regla del perceptron / actualizar solo al equivocarse de signo)
  CONSIST   seleccion de rasgos por CONSISTENCIA LOCAL: se quedan los m rasgos con mayor |media de y cuando
            el rasgo esta activo| (estadistico local, un escalar por rasgo) y luego L2 sobre ellos
  KENYON    la via RAPIDA sola: codigo top-K de la proyeccion aleatoria KW (K=1..7), L2 sobre el codigo
  KEN+PX    codigo Kenyon concatenado con los 6 pixeles (rapida + lenta lineal, un solo error)
Tambien: ALIN = alineacion nucleo-objetivo  y^T K y / (||K||_F ||y||^2)  con K = Phi Phi^T sobre los 20 patrones,
un numero por lectura que predice si esa lectura puede separar XOR.
Sin organismo, sin Pool, segundos.
"""
import sys, os, json
import numpy as np
from scipy.optimize import linprog

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'nivel7_xor_lectura'))
import organismo_v13q as O
from identificabilidad_xor import phi, signo_acc, R_VAL, IJ, min_l1_interpolante, min_l2_interpolante

NKMAX = 90


# ---------------------------------------------------------------- geometrias
def dos_canales_fp(X, y, eta_s=0.015, lam=0.05, clip_s=3.0, aversion=1.0, pasos=40000, rng=None):
    """Simula la regla EXACTA de la via lenta de v13q sobre los 8 patrones de tren (sin mundo): dos canales no
    negativos, drenaje de la parte comun sobre los rasgos activos, tope. Orden de presentacion aleatorio."""
    rng = rng or np.random.default_rng(0)
    n = X.shape[1]; Wps = np.zeros(n); Wns = np.zeros(n)
    for t in range(pasos):
        i = int(rng.integers(len(y))); ph = X[i]
        ds = y[i] - float((Wps - Wns) @ ph)
        if lam:
            mcs = np.minimum(Wps, Wns) * (ph > 0); Wps = Wps - lam * mcs; Wns = Wns - lam * mcs
        if ds > 0: Wps = np.clip(Wps + eta_s * ds * ph, 0, clip_s)
        else:      Wns = np.clip(Wns + eta_s * aversion * (-ds) * ph, 0, clip_s)
    return Wps - Wns


def max_margen(X, y):
    """Maximo margen L2 (hard-margin SVM sin sesgo) sobre las etiquetas de signo: el sesgo implicito de la regla
    del perceptron / de cualquier regla que solo actualiza cuando se equivoca de signo."""
    s = np.sign(y); Z = X * s[:, None]
    # min ||w||^2 s.a. Z w >= 1  -> dual simple por proyeccion; se resuelve con scipy.optimize.nnls sobre el dual
    from scipy.optimize import minimize
    n = X.shape[1]
    res = minimize(lambda w: float(w @ w), np.zeros(n), jac=lambda w: 2 * w, method='SLSQP',
                   constraints=[{'type': 'ineq', 'fun': lambda w: Z @ w - 1.0, 'jac': lambda w: Z}],
                   options={'maxiter': 500, 'ftol': 1e-10})
    return res.x if res.success else None


def consistencia(X, y, m):
    """Selecciona los m rasgos con mayor |media de y cuando el rasgo esta activo| (estadistico 100% local:
    cada rasgo lleva su propia media de recompensa) y devuelve L2 sobre ese subconjunto."""
    act = X > 0
    c = np.zeros(X.shape[1])
    for i in range(X.shape[1]):
        c[i] = abs(float(y[act[:, i]].mean())) if act[:, i].any() else 0.0
    idx = np.argsort(-c)[:m]
    return idx


# ---------------------------------------------------------------- lecturas
def kenyon_map(seed, K, NK=30, con_px=False):
    """Codigo de la via rapida ANTES de cualquier division (KW inicial de organismo_v13q): top-K de KW@P."""
    rng = np.random.default_rng(seed)
    _ = rng.uniform(.1, .4, (2, 9))                    # Wl, se consume igual que en el organismo
    KW = np.zeros((NKMAX, 6)); activa = np.zeros(NKMAX, bool)
    KW[:NK] = rng.uniform(0, 1, (NK, 6)); activa[:NK] = True

    def f(P):
        v = KW @ P; v = np.where(activa, v, -1e9)
        k = np.zeros(NKMAX); k[list(np.argsort(v)[-K:])] = 1
        return np.concatenate([k, P]) if con_px else k
    return f


def alineacion(F, nombres, vr):
    Phi = np.array([F[k] for k in nombres]); y = np.array([R_VAL[vr[k]] for k in nombres])
    Kk = Phi @ Phi.T
    return float(y @ Kk @ y / (np.linalg.norm(Kk, 'fro') * float(y @ y)))


def evalua(seed, regla, Fmap, geom, **kw):
    pats, tren, test, vr = O.split_regla(seed, regla)
    F = {k: Fmap(pats[k]) for k in pats}
    X = np.array([F[k] for k in tren]); y = np.array([R_VAL[vr[k]] for k in tren])
    if geom == 'L2':       w = min_l2_interpolante(X, y)
    elif geom == 'L1':     w = min_l1_interpolante(X, y)
    elif geom == 'PERCEP': w = max_margen(X, y)
    elif geom == 'DOSCAN': w = dos_canales_fp(X, y, rng=np.random.default_rng(seed), **kw)
    elif geom == 'CONSIST':
        idx = consistencia(X, y, kw.get('m', 4)); w = np.zeros(X.shape[1])
        w[idx] = min_l2_interpolante(X[:, idx], y)
    else: raise ValueError(geom)
    if w is None: return None, None
    pred = {k: float(F[k] @ w) for k in pats}
    return signo_acc(pred, test, vr), alineacion(F, sorted(pats), vr)


def med(xs):
    xs = [x for x in xs if x is not None]
    return (round(float(np.median(xs)), 3), round(float(min(xs)), 3), round(float(max(xs)), 3)) if xs else None


if __name__ == '__main__':
    S = list(range(1, 21))
    print('=== A. la via LENTA: geometrias sobre la lectura cuadratica (+1) — xor01, 20 semillas ===')
    print(f'{"geometria":>12} {"xor01":>22} {"px0":>22} {"azar":>22}')
    for geom, kw in (('L2', {}), ('L1', {}), ('DOSCAN', {}), ('PERCEP', {}),
                     ('CONSIST', dict(m=3)), ('CONSIST', dict(m=4)), ('CONSIST', dict(m=6)), ('CONSIST', dict(m=10))):
        fila = {}
        for regla in ('xor01', 'px0', 'azar'):
            fila[regla] = med([evalua(s, regla, lambda P: phi(P, 'cuadratica', True), geom, **kw)[0] for s in S])
        etq = geom + (f"(m={kw['m']})" if 'm' in kw else '')
        print(f'{etq:>12} {str(fila["xor01"]):>22} {str(fila["px0"]):>22} {str(fila["azar"]):>22}')

    print('\n=== B. la via RAPIDA sola (codigo Kenyon inicial, L2) — prediccion para el experimento K=5 ===')
    print(f'{"K":>3} {"con px":>7} {"xor01":>22} {"px0":>22} {"alineacion xor01":>17}')
    for K in (1, 2, 3, 4, 5, 6, 7):
        for con_px in (False, True):
            r = [evalua(s, 'xor01', kenyon_map(s, K, con_px=con_px), 'L2') for s in S]
            rp = [evalua(s, 'px0', kenyon_map(s, K, con_px=con_px), 'L2') for s in S]
            print(f'{K:>3} {str(con_px):>7} {str(med([x[0] for x in r])):>22} {str(med([x[0] for x in rp])):>22} '
                  f'{np.median([x[1] for x in r]):>17.4f}')

    print('\n=== C. alineacion nucleo-objetivo por lectura (numero unico; xor01 sobre los 20 patrones) ===')
    pats = O.patrones_regla(); nombres = sorted(pats)
    for lec, cte in (('lineal', False), ('lineal', True), ('cuadratica', False), ('cuadratica', True),
                     ('oraculo', True), ('random15', False)):
        al = []
        for s in S:
            _, _, _, vr = O.split_regla(s, 'xor01')
            R15 = None
            if lec == 'random15':
                rr = np.random.default_rng(s + 900000); R15 = {}
                for n in range(64):
                    Pb = tuple(float((n >> (5 - j)) & 1) for j in range(6)); R15[Pb] = rr.integers(0, 2, 15).astype(float)
            F = {k: phi(pats[k], lec, cte, R15) for k in pats}
            al.append(alineacion(F, nombres, vr))
        print(f'  {lec:>11} cte={str(cte):>5}  alineacion = {np.median(al):.4f}')
    print('\nOK')
