"""sim_mmr.py — NULO POR PUERTA de la REPLICA de la moneda del muro (1-oct-2026, creador). No corre el organismo.
El modelo de deriva ES el de moneda_muro/sim_mm.py (se IMPORTA su chain(); sha fijado): cada pasaje 5 a 7 linajes establecidos, clones
de un fundador; el fundador es A con odds = OR x odds(f); 6 pasajes. Aqui n = 10 cadenas por brazo y se comparan las lecturas:
  (a10) letra original escalada: moneda_L >= neutra_L en 10/10 y mediana >= 0.40
  (a5)  letra original sobre las 5 primeras cadenas: >= en 5/5 y mediana (de las 5) >= 0.40
  (bK)  estricta: moneda_L > neutra_L (los empates en contra) en >= K/10 y mediana (de las 10) >= 0.40, K = 7..10
  PURGA: moneda_L <= 0.5 x neutra_L (neutra > 0) en >= K/10, K = 7, 8
CO-PRINCIPAL (cruce en la prueba final, pareado, 10 parejas de 0..9): nulo = las dos cadenas de la pareja cruzan Binomial(9, q) con la
MISMA q de la pareja, q ~ U(0.25, 0.65) (en el explora: 2..6 de 9); alternativa = q_moneda = q + d. Gana = estricto; empates en contra.
  python experimentos/organelos/condiciones/moneda_muro_rep/sim_mmr.py
"""
import hashlib, os, random, statistics as st, sys

AQUI = os.path.dirname(os.path.abspath(__file__))
MMD = os.path.join(os.path.dirname(AQUI), 'moneda_muro')
SHA_SIM = 'ae805f42e2e6f26c'
assert hashlib.sha256(open(os.path.join(MMD, 'sim_mm.py'), 'rb').read()).hexdigest()[:16] == SHA_SIM, 'sim_mm.py cambio'
sys.path.insert(0, MMD)
import sim_mm as S0   # chain(OR, P=6): el modelo del explora, sin tocar
try: sys.stdout.reconfigure(encoding='utf-8', errors='replace')
except Exception: pass


def lecturas(mo, ne):
    ge = sum(m >= n for m, n in zip(mo, ne)); gt = sum(m > n for m, n in zip(mo, ne)); med = st.median(mo) >= 0.4
    ge5 = sum(m >= n for m, n in zip(mo[:5], ne[:5])); med5 = st.median(mo[:5]) >= 0.4
    mit = sum(n > 0 and m <= 0.5 * n for m, n in zip(mo, ne))
    d = dict(a10=ge >= 10 and med, a5=ge5 >= 5 and med5, pu7=mit >= 7, pu8=mit >= 8)
    for k in (7, 8, 9, 10): d[f'b{k}'] = gt >= k and med
    return d


def binom(q): return sum(random.random() < q for _ in range(9))


if __name__ == '__main__':
    random.seed(2); N = 20000
    print("== FRACCION A FINAL, n = 10 cadenas por brazo (probabilidad de cada lectura; OR = razon de ventaja de A por pasaje; neutra OR 1)")
    for OR in (0.5, 0.7, 1.0, 1.5, 2.0, 3.0):
        c = {}; emp = 0
        for _ in range(N):
            mo = [S0.chain(OR) for _ in range(10)]; ne = [S0.chain(1.0) for _ in range(10)]
            for k, v in lecturas(mo, ne).items(): c[k] = c.get(k, 0) + int(v)
            emp += sum(m == n for m, n in zip(mo, ne))
        print(f"OR {OR}: " + ' · '.join(f"{k} {c[k] / N:.3f}" for k in ('a10', 'a5', 'b7', 'b8', 'b9', 'b10', 'pu7', 'pu8')) + f" · empates de 10: {emp / N:.2f}")
    print("== H-1 (auditoria): la NEUTRA con sesgo propio y la moneda SIN ventaja (moneda OR 1). Probabilidad de CONSERVA por cada lectura")
    for ORn in (1.0, 0.7, 0.5):
        c = {}
        for _ in range(N):
            mo = [S0.chain(1.0) for _ in range(10)]; ne = [S0.chain(ORn) for _ in range(10)]
            for k, v in lecturas(mo, ne).items(): c[k] = c.get(k, 0) + int(v)
        print(f"neutra OR {ORn}, moneda OR 1.0: " + ' · '.join(f"{k} {c[k] / N:.3f}" for k in ('a10', 'a5', 'b7', 'b8')))
    print("== CRUCE EN LA PRUEBA FINAL, 10 parejas (probabilidad de: gana >= K/10 y suma de diferencias >= D)")
    for d in (-0.13, 0.0, 0.10, 0.15, 0.20, 0.30):
        c = {}; sd = []
        for _ in range(N):
            q = [random.uniform(0.25, 0.65) for _ in range(10)]
            mo = [binom(min(1, max(0, x + d))) for x in q]; ne = [binom(x) for x in q]
            g = sum(m > n for m, n in zip(mo, ne)); p = sum(m < n for m, n in zip(mo, ne)); D = sum(mo) - sum(ne); sd.append(D)
            for K, DD in ((6, 9), (7, 0), (7, 9), (8, 0)):
                c[('+', K, DD)] = c.get(('+', K, DD), 0) + int(g >= K and D >= DD and D > 0)
                c[('-', K, DD)] = c.get(('-', K, DD), 0) + int(p >= K and -D >= DD and D < 0)
        print(f"d {d:+.2f}: " + ' · '.join(f"{s}K{K}D{DD} {v / N:.3f}" for (s, K, DD), v in sorted(c.items())) + f" · D media {st.mean(sd):+.1f} sd {st.pstdev(sd):.1f}")
