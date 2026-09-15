"""
bateria_3k.py - criterio (C-3a) del PREREGISTRO: la tarea A/B original no se degrada.
Corre la bateria de organismo/bateria.py (criterios IDENTICOS) sobre organismo_3k en
mundo='AB' para las cuatro condiciones de Kenyon. Uso: python bateria_3k.py [semillas]
"""
import sys, os
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import numpy as np
from multiprocessing import Pool, get_context
import organismo_3k as o3

CONDS = [("1  fijo       ", dict(kenyon_mode='fijo', k_lr=0.0)),
         ("2  hebb_visita", dict(kenyon_mode='hebb_visita', k_lr=0.01)),
         ("2b hebb_mordid", dict(kenyon_mode='hebb_mordida', k_lr=0.01)),
         ("3  error      ", dict(kenyon_mode='error', k_lr=0.01))]

tasa = lambda r, k, i: 100 * r['mord'][k][i] / max(r['vis'][k][i], 1)

ETAPAS = [
    ("E1 aprendizaje A/B", dict(), {
        "venenoQ4<Q1": lambda r: r['mord']['B'][3] < r['mord']['B'][0],
        "W_A~+1": lambda r: abs(r['W']['A'] - 1) < .15,
        "W_B~-3": lambda r: abs(r['W']['B'] + 3) < .3}),
    ("E2 inversion A<->B", dict(invertir_en=50000), {
        "W_A->-3": lambda r: abs(r['W']['A'] + 3) < .3,
        "W_B->+1": lambda r: abs(r['W']['B'] - 1) < .15,
        "come B Q4>=50": lambda r: r['mord']['B'][3] >= 50}),
    ("E2I nuevo C veneno", dict(nuevo='C'), {
        "W_C<=-2.5": lambda r: r['W']['C'] <= -2.5,
        "W_A~+1": lambda r: abs(r['W']['A'] - 1) < .15,
        "W_B<=-2.8": lambda r: r['W']['B'] <= -2.8,
        "tasaA Q4>=80%Q2": lambda r: tasa(r, 'A', 3) >= .8 * tasa(r, 'A', 1)}),
    ("E2J nuevo D, D&B=1", dict(nuevo='D', nuevo_val='comida', solap_B=1), {
        "W_D>=0.85": lambda r: r['W']['D'] >= .85,
        "W_B<=-2.7": lambda r: r['W']['B'] <= -2.7}),
    ("E2K nuevo D, D&B=2", dict(nuevo='D', nuevo_val='comida', solap_B=2), {
        "W_D>=0.8": lambda r: r['W']['D'] >= .8,
        "W_B<=-2.4": lambda r: r['W']['B'] <= -2.4}),
]


def _job(a):
    s, ckw, ekw = a
    return o3.run(s, mundo='AB', **ckw, **ekw)


if __name__ == "__main__":
    S = int(sys.argv[1]) if len(sys.argv) > 1 else 6
    seeds = list(range(1, S + 1))
    jobs = [(s, ckw, ekw) for _, ckw in CONDS for _, ekw, _ in ETAPAS for s in seeds]
    with get_context('spawn').Pool() as pool:
        res = pool.map(_job, jobs)
    it = iter(res)
    tabla = {}
    for cn, _ in CONDS:
        for en, _, crit in ETAPAS:
            rs = [next(it) for _ in seeds]
            tabla[(cn, en)] = (rs, crit)

    print(f"=== Bateria A/B sobre organismo_3k, {S} semillas (criterio C-3a del PREREGISTRO) ===")
    for cn, _ in CONDS:
        print(f"\n-- Condicion {cn} --")
        for en, _, crit in ETAPAS:
            rs, crit = tabla[(cn, en)]
            ok = [all(c(r) for c in crit.values()) for r in rs]
            det = " ".join(f"{n}:{sum(c(r) for r in rs)}/{S}" for n, c in crit.items())
            print(f"  {'PASA' if all(ok) else 'FALLA':5s} {en:22s} {sum(ok)}/{S}  [{det}]  "
                  f"W_A med={np.median([r['W']['A'] for r in rs]):+.2f} "
                  f"W_B med={np.median([r['W']['B'] for r in rs]):+.2f} "
                  f"muertes med={np.median([r['deaths'] for r in rs]):.0f}")
