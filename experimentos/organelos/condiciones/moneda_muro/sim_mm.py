"""sim_mm.py — simulacion del NULO POR PUERTA de la moneda del muro (30-sep-2026, creador; H-2 de la auditoria). No corre el organismo.
Modelo de deriva: cada pasaje, 5 a 7 linajes establecidos, cada uno clon de un fundador; el fundador es A con odds = OR x odds(f).
6 pasajes, 5 cadenas por brazo, neutra con OR 1. Imprime la probabilidad de cada veredicto con CONSERVA en 4/5 (letra vieja) y 5/5 (ERR-176).
  python experimentos/organelos/condiciones/moneda_muro/sim_mm.py
"""
import random, statistics as st
random.seed(1)


def chain(OR, P=6):
    f = 0.5
    for _ in range(P):
        n = random.choice([5, 6, 6, 7])
        if f <= 0: p = 0.0
        elif f >= 1: p = 1.0
        else: o = OR * f / (1 - f); p = o / (1 + o)
        f = sum(random.random() < p for _ in range(n)) / n
    return f


def ver(mo, ne, cn):
    ge = sum(m >= n for m, n in zip(mo, ne)); mit = sum(n > 0 and m <= 0.5 * n for m, n in zip(mo, ne))
    if ge >= cn and st.median(mo) >= 0.4: return 'CONSERVA'
    if mit >= 4: return 'PURGA'
    return 'INDET'


if __name__ == '__main__':
    N = 20000
    for OR in (0.4, 0.5, 0.7, 1.0, 1.5, 2.0, 3.0):
        c = {cn: {'CONSERVA': 0, 'PURGA': 0, 'INDET': 0} for cn in (4, 5)}; fx = 0
        for _ in range(N):
            mo = [chain(OR) for _ in range(5)]; ne = [chain(1.0) for _ in range(5)]
            for cn in (4, 5): c[cn][ver(mo, ne, cn)] += 1
            fx += sum(v in (0, 1) for v in mo + ne)
        print(f"OR {OR}: CONSERVA_N 4 {({k: round(v / N, 3) for k, v in c[4].items()})} · CONSERVA_N 5 {({k: round(v / N, 3) for k, v in c[5].items()})} "
              f"· fijadas o perdidas de 10: {fx / N:.2f}")
