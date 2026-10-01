"""nulo_perillas.py — EL NULO de la deriva (sin corridas del mundo: solo la regla de mutacion de construye_perillas). 1-oct-2026.
Un gen que NADIE lee, arranca en 0 y muta como en el carro: en cada nacimiento, con probabilidad 1/2 (se elige UNO de los 2 genes),
gen' = recorte(gen - DELTA + N(0, SIGMA), [0, 1.5]). Pregunta: tras n generaciones (profundidad), ¿con que probabilidad la deriva sola
deja el gen por encima de x? Lo decide DELTA (sesgo a la perdida). Sale la tabla del preregistro (sec. 5) y el nulo de la puerta PG.
    python experimentos/organelos/escalera/perillas/nulo_perillas.py
"""
import numpy as np

SIGMA = 0.03; REPS = 40000; SEM = 20261001
XS = (0.05, 0.10, 0.15, 0.20); NS = (30, 60, 150, 300, 600)


def deriva(delta, n, rng, reps=REPS):
    g = np.zeros(reps)
    for _ in range(n):
        toca = rng.random(reps) < 0.5
        g = np.where(toca, np.clip(g - delta + SIGMA * rng.standard_normal(reps), 0.0, 1.5), g)
    return g


def main():
    rng = np.random.default_rng(SEM)
    print(f"NULO de la deriva: sigma {SIGMA}, un gen de 2 por nacimiento, recorte [0, 1.5], {REPS} linajes independientes, semilla {SEM}")
    print(f"{'delta':>6} {'n':>5} {'media':>7} {'mediana':>8} " + ' '.join(f"P(>{x:.2f})" for x in XS))
    for delta in (0.0, 0.005, 0.01, 0.015, 0.02):
        for n in NS:
            g = deriva(delta, n, rng)
            print(f"{delta:6.3f} {n:5d} {g.mean():7.4f} {np.median(g):8.4f} " + ' '.join(f"{(g > x).mean():8.4f}" for x in XS))
    # nulo de PG: sel y neu son la MISMA deriva (genes no leidos): P(sel > neu + 0.05) por cadena y P(>= 13 de 20)
    from math import comb
    for delta in (0.0, 0.01):
        a = deriva(delta, 300, rng); b = deriva(delta, 300, rng); p = float((a > b + 0.05).mean())
        p13 = sum(comb(20, k) * p ** k * (1 - p) ** (20 - k) for k in range(13, 21))
        print(f"PG bajo el nulo (delta {delta}, n 300): P(sel > neu + 0.05) por cadena = {p:.4f} -> P(>= 13/20) = {p13:.2e}")
    print("cota sin supuestos (intercambiabilidad sel/neu bajo el nulo, empates en contra): p <= 0.5 -> P(>= 13/20) <= 0.132")


if __name__ == '__main__':
    main()
