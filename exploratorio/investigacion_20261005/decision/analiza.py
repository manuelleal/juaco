"""analiza.py — comparaciones PAREADAS por semilla (misma semilla, mismo mundo) sobre los JSON de decision.py.
Uso: python analiza.py datos/principal.json [mas archivos]"""
import json, sys, numpy as np


def med(v): v = [x for x in v if x is not None]; return (int(np.median(v)) if v else None)


def rec_mediana(r, k):
    v = [x for x in r[k] if x is not None]; return float(np.median(v)) if v else float('inf')


def pareadas(rs, a, b, k='comida_por_paso', mayor=True):
    da = [r['brazos'][a][k] for r in rs]; db = [r['brazos'][b][k] for r in rs]
    d = np.array(da) - np.array(db)
    g = int(np.sum(d > 0)) if mayor else int(np.sum(d < 0))
    return g, len(rs), float(np.median(d))


def informe(path):
    rs = json.load(open(path)); br = list(rs[0]['brazos']); n = len(rs)
    print(f"\n### {path} (n={n})")
    prop = '6 plan_pan_cel'
    if prop not in br: return
    print("| comparación (comida/paso, pareada) | gana la propuesta | mediana de la diferencia |")
    print("|---|---|---|")
    for o in br:
        if o == prop: continue
        g, nn, m = pareadas(rs, prop, o); print(f"| (6) vs {o} | {g}/{nn} | {m:+.3f} |")
    # recuperacion tras regla: mediana por semilla de la 3a comida (inf si nunca)
    print("\n| comparación (pasos hasta la 3ª comida tras REGLA, mediana por semilla; menor es mejor) | gana la propuesta |")
    print("|---|---|")
    for o in br:
        if o == prop: continue
        ga = sum(rec_mediana(r['brazos'][prop], 'rec3_regla') < rec_mediana(r['brazos'][o], 'rec3_regla') for r in rs)
        em = sum(rec_mediana(r['brazos'][prop], 'rec3_regla') == rec_mediana(r['brazos'][o], 'rec3_regla') for r in rs)
        print(f"| (6) vs {o} | {ga}/{n} (empates {em}) |")
    # tasa en ventanas tras regla
    print("\n| comparación (tasa de comida en las ventanas tras REGLA) | gana la propuesta | mediana dif |")
    print("|---|---|---|")
    for o in br:
        if o == prop: continue
        g, nn, m = pareadas(rs, prop, o, 'tasa_regla'); print(f"| (6) vs {o} | {g}/{nn} | {m:+.3f} |")
    # fraccion del oraculo
    if '0 oraculo' in br:
        print("\n| brazo | comida/paso como fracción del oráculo (mediana) |\n|---|---|")
        for o in br:
            f = [r['brazos'][o]['comida_por_paso'] / r['brazos']['0 oraculo']['comida_por_paso'] for r in rs]
            print(f"| {o} | {np.median(f):.2f} [{min(f):.2f}–{max(f):.2f}] |")


if __name__ == '__main__':
    for p in sys.argv[1:]: informe(p)
