"""nulo_margen.py — NULOS del gen MARGEN bajo la regla de mutacion de este carro (una mutacion por nacimiento; g' = g - delta + N(0, sigma),
recortado a [0, 0.6]). Python puro, segundos, 0 pista. Sirve para fijar el margen de PG (sel > neu + margen) y para DECLARAR el falso positivo de
la puerta (b) (sel >= FUNC en >= 13/20) bajo seleccion PURIFICADORA sin gradiente (auditoria 5-oct, B-1; ERR-192).
  (1) DERIVA PURA (el neutro, PS_LEE 0): linajes sueltos desde ARRANQUE a distintas profundidades; p = P(la mutacion cae en MARGEN) = 1 si solo
      MARGEN muta (serie, PS_MUTA = (0,)) o 1/6 si mutan los seis (version del 5-oct 15:00: nulo_margen_v1_p16.py.txt).
  (2) MEDIANA de una siembra neutra de 45 muestras (9 linajes x 5).
  (3) PG (a) pareado bajo el nulo: P(sel > neu + margen) con sel y neu intercambiables (deriva pura las dos).
  (4) ERR-192: DERIVA CON SELECCION PURIFICADORA (sel sin gradiente): 9 linajes en camara; si MARGEN cae bajo LETAL el linaje "muere" y es
      refundado con copia mutada del genoma de otro linaje al azar (la camara); por encima de LETAL NO hay ventaja. Da P(mediana de sel > mediana
      de neu + margen) -> falso positivo de (a) sin gradiente, y P(mediana de sel >= FUNC) -> falso positivo de (b), que es lo que decide.
    python experimentos/organelos/muro_perillas/nulo_margen.py [--arranque 0.03] [--p 1] [--n 40000] [--letal 0.015] [--margen 0.03]
"""
import argparse, math, random, statistics as st, sys

sys.stdout.reconfigure(encoding='utf-8', errors='replace')
SIGMA = 0.03; DELTA = 0.01; CLIP = (0.0, 0.6); FUNC = 0.06


def muta(g, rng):
    return min(max(g - DELTA + rng.gauss(0.0, SIGMA), CLIP[0]), CLIP[1])


def deriva(g, n, p, rng):
    for _ in range(n):
        if p >= 1.0 or rng.random() < p: g = muta(g, rng)
    return g


def siembra_neutra(arr, p, rng, lo=20, hi=120):
    sie = []
    for _ in range(9):
        g = deriva(arr, rng.randint(lo, hi), p, rng); sie += [deriva(g, rng.randint(0, 2), p, rng) for _ in range(5)]
    return st.median(sie)


def siembra_purificadora(arr, p, letal, rng, lo=20, hi=120):
    """9 linajes con camara: cada evento muta; si el gen cae bajo LETAL el linaje muere y es refundado desde OTRO linaje vivo (copia mutada).
    Sin ventaja por encima de LETAL. Devuelve la mediana de 45 muestras y el numero de refundaciones."""
    n = rng.randint(lo, hi); g = [arr] * 9; ref = 0
    for _ in range(n):
        for i in range(9):
            if p >= 1.0 or rng.random() < p: g[i] = muta(g[i], rng)
            if g[i] < letal:
                vivos = [j for j in range(9) if j != i and g[j] >= letal]
                g[i] = muta(g[rng.choice(vivos)], rng) if vivos else arr; ref += 1
    sie = [deriva(x, rng.randint(0, 2), p, rng) for x in g for _ in range(5)]
    return st.median(sie), ref


def binom13(p1): return sum(math.comb(20, k) * p1 ** k * (1 - p1) ** (20 - k) for k in range(13, 21))


def main():
    ap = argparse.ArgumentParser(allow_abbrev=False)
    ap.add_argument('--arranque', type=float, default=0.03); ap.add_argument('--p', type=float, default=1.0); ap.add_argument('--n', type=int, default=40000)
    ap.add_argument('--letal', type=float, default=0.015); ap.add_argument('--margen', type=float, default=0.03)
    a = ap.parse_args(); rng = random.Random(883)
    print(f"NULOS de MARGEN: arranque {a.arranque}, sigma {SIGMA}, delta {DELTA}, clip {CLIP}, p(mutacion en MARGEN) {a.p}, FUNC {FUNC}, letal {a.letal}, margen {a.margen}, {a.n} linajes")
    print("(1) DERIVA PURA por linaje")
    print(f"  {'eventos':>8} {'media':>7} {'mediana':>8} {'P>0.02':>7} {'P>0.03':>7} {'P>0.05':>7} {'P>0.06':>7} {'P>0.10':>7}")
    for n in (6, 12, 30, 60, 120, 300):
        xs = [deriva(a.arranque, n, a.p, rng) for _ in range(a.n)]
        pr = lambda u: sum(x > u for x in xs) / len(xs)
        print(f"  {n:8d} {st.mean(xs):7.4f} {st.median(xs):8.4f} {pr(0.02):7.3f} {pr(0.03):7.3f} {pr(0.05):7.3f} {pr(0.06):7.3f} {pr(0.10):7.3f}")
    meds = [siembra_neutra(a.arranque, a.p, rng) for _ in range(4000)]
    pr = lambda u: sum(x > u for x in meds) / len(meds)
    print(f"(2) MEDIANA de siembra neutra (45 muestras, 4000 cadenas, profundidad 20-120): media {st.mean(meds):.4f} mediana {st.median(meds):.4f} "
          f"P>0.01 {pr(0.01):.3f} P>0.02 {pr(0.02):.3f} P>0.03 {pr(0.03):.3f} P>0.05 {pr(0.05):.3f} P>=0.06 {sum(x >= FUNC for x in meds) / len(meds):.3f}")
    print("(3) PG (a) bajo el nulo de deriva pura (sel y neu intercambiables):")
    for mg in (0.02, 0.03, 0.05):
        p1 = sum(1 for i in range(0, len(meds) - 1, 2) if meds[i] > meds[i + 1] + mg) / (len(meds) // 2)
        print(f"  margen {mg}: P(sel > neu + margen) por cadena {p1:.3f} -> P(>= 13/20) {binom13(p1):.2e}")
    print(f"(4) SELECCION PURIFICADORA sin gradiente (ERR-192): sel = 9 linajes en camara, muerte si MARGEN < {a.letal}, refundacion desde otro linaje; neu = deriva pura")
    pur = [siembra_purificadora(a.arranque, a.p, a.letal, rng) for _ in range(2000)]
    ms = [m for m, r in pur]; rs = [r for m, r in pur]
    neu = [siembra_neutra(a.arranque, a.p, rng) for _ in range(2000)]
    pa = sum(1 for s_, n_ in zip(ms, neu) if s_ > n_ + a.margen) / len(ms); pb = sum(1 for s_ in ms if s_ >= FUNC) / len(ms)
    print(f"  sel purificadora: mediana {st.median(ms):.4f} media {st.mean(ms):.4f} P>0.03 {sum(x > 0.03 for x in ms) / len(ms):.3f} P>=0.06 {pb:.3f} refundaciones por cadena mediana {st.median(rs)}")
    print(f"  (a) P(sel > neu + {a.margen}) por cadena SIN gradiente {pa:.3f} -> P(>= 13/20) {binom13(pa):.3f}   <- falso positivo de (a): por eso (a) sola no basta")
    print(f"  (b) P(sel >= {FUNC}) por cadena SIN gradiente {pb:.3f} -> P(>= 13/20) {binom13(pb):.2e}   <- falso positivo de (b) (lo que decide)")
    return 0


if __name__ == '__main__':
    sys.exit(main())
