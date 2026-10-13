"""Mundo de capacidad GRANDE: retina de D pixeles, estimulos de peso 3, familia completa C(D,3).
Mismas convenciones que experimentos/ramas/2Kbis_capacidad/parte2_capacidad.py (que se importa para techo() y TOL):
  - orden: los canonicos A,B,C,D primero (cuando D_pix=6), y el resto en orden lexicografico;
  - valencias ALTERNANDO desde el primero: comida, veneno, comida, veneno, ...;
  - el estimulo n>=3 entra en t=(n-1)*paso_t; checkpoint n en t=(n-1)*paso_t; T=(n_est-1)*paso_t+paso_t.
Con D_pix=6 y n_est=20, PATS, VAL, R, plan_de, chks y T_de son IDENTICOS a parte2_capacidad (control G0).
"""
import itertools
import numpy as np

CANON = [('A', (0, 1, 3)), ('B', (0, 2, 4)), ('C', (1, 2, 5)), ('D', (2, 4, 5))]


def mundo(D_pix=10, n_est=60):
    """Devuelve (NOMBRES, PATS, VAL, R) con n_est estimulos de peso 3 sobre D_pix pixeles."""
    todos = list(itertools.combinations(range(D_pix), 3))
    if D_pix == 6:
        usados = {c for _, c in CANON}
        nombres = [n for n, _ in CANON] + ['E%02d' % (i + 5) for i in range(len(todos) - len(usados))]
        combos = [c for _, c in CANON] + [c for c in todos if c not in usados]
    else:
        nombres = ['P%03d' % (i + 1) for i in range(len(todos))]
        combos = todos
    nombres, combos = nombres[:n_est], combos[:n_est]
    if len(nombres) < n_est:
        raise SystemExit(f"C({D_pix},3)={len(todos)} < n_est={n_est}")
    pats = {n: np.array([1. if i in c else 0. for i in range(D_pix)]) for n, c in zip(nombres, combos)}
    val = {n: ('comida' if i % 2 == 0 else 'veneno') for i, n in enumerate(nombres)}
    R = {n: (1.0 if val[n] == 'comida' else -3.0) for n in nombres}
    return nombres, pats, val, R


def plan_de(paso_t, nombres, val):
    p = [(0, nombres[0], val[nombres[0]]), (0, nombres[1], val[nombres[1]])]
    for i in range(2, len(nombres)):
        p.append(((i - 1) * paso_t, nombres[i], val[nombres[i]]))
    return p


def chks(paso_t, n_est):
    return [(n - 1) * paso_t for n in range(2, n_est + 1)]


def T_de(paso_t, n_est):
    return (n_est - 1) * paso_t + paso_t


def techo(hist, TOL=0.3):
    """Copia literal de parte2_capacidad.techo() con excl_nuevo=False: mayor n con mediana |W-R| <= TOL
    en TODOS los checkpoints hasta n."""
    import statistics as st
    N = 1
    for h in sorted(hist, key=lambda h: h['t']):
        d = dict(h['dev'])
        if not d:
            continue
        if st.median(d.values()) <= TOL:
            N = h['n']
        else:
            break
    return N


def m_max(hist, TOL=0.3):
    return max(sum(1 for v in h['dev'].values() if v <= TOL) for h in hist)
