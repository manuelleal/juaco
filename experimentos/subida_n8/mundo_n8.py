"""Mundo en FLUJO para el nivel 8 (subida_n8). Solo arma el plan; la dinamica vive en organismo_flujo.py (perilla ventana).

- Retina de D_PIX = 12 pixeles; familia completa de peso 3: C(12,3) = 220 patrones. Se usan N_EST = 200, en orden
  AL AZAR por semilla, con un generador APARTE (np.random.default_rng([semilla, 808])): no toca el rng del organismo.
- Valencias al azar por semilla y BALANCEADAS: en cada bloque de 10 introducciones consecutivas, 5 comida y 5 veneno
  (trampa "acierto sin balancear"). Al ser al azar, la via lenta (lineal en la retina) no puede predecir lo nuevo
  (trampa "lo nuevo lo generaliza gratis").
- Entrada: los dos primeros en t = 0; el i-esimo (i >= 2) en t = (i-1)*PASO_T. T = N_EST*PASO_T.
- RECICLADO (control de novedad falsa, nivel8 s3 punto 14): las primeras N0 entradas son las mismas que en FLUJO; desde
  la N0-esima, cada entrada es una REPETICION de uno de los N0 primeros (en ciclo), con su misma valencia.
"""
import itertools
import numpy as np

D_PIX = 12
N_EST = 200
PASO_T = 1000
N0_RECICLADO = 20
BLOQUE = 10


def mundo(semilla, n_est=N_EST, d_pix=D_PIX, reciclado=False, n0=N0_RECICLADO):
    """Devuelve (orden, pats, plan) con orden = lista de nombres por entrada (con repeticiones en RECICLADO)."""
    g = np.random.default_rng([int(semilla), 808])
    combos = list(itertools.combinations(range(d_pix), 3))
    perm = g.permutation(len(combos))
    if n_est > len(combos):
        raise SystemExit(f"C({d_pix},3)={len(combos)} < n_est={n_est}")
    vals = []
    for b in range(0, n_est, BLOQUE):
        m = min(BLOQUE, n_est - b)
        blk = ['comida'] * (m // 2) + ['veneno'] * (m - m // 2)
        vals += [blk[i] for i in g.permutation(m)]
    distintos = n0 if reciclado else n_est
    nombres = ['S%03d' % i for i in range(distintos)]
    pats = {nombres[i]: np.array([1. if p in combos[perm[i]] else 0. for p in range(d_pix)]) for i in range(distintos)}
    val = {nombres[i]: vals[i] for i in range(distintos)}
    orden = [nombres[i if i < distintos else (i % distintos)] for i in range(n_est)]
    return orden, pats, val


def plan_de(orden, val, paso_t=PASO_T):
    p = [(0, orden[0], val[orden[0]]), (0, orden[1], val[orden[1]])]
    for i in range(2, len(orden)):
        p.append(((i - 1) * paso_t, orden[i], val[orden[i]]))
    return p


def t_entrada(i, paso_t=PASO_T):
    return 0 if i < 2 else (i - 1) * paso_t


def T_de(n_est=N_EST, paso_t=PASO_T):
    return n_est * paso_t
