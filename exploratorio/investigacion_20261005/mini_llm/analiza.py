"""pareadas por semilla y resumen corto. uso: python analiza.py datos/principal_C200.json [datos/principal_C40.json ...]"""
import json, sys, numpy as np

def med(v): return float(np.median(v))

def pares(todo, a, b, f):
    d = [f(r['brazos'][a]) - f(r['brazos'][b]) for r in todo if a in r['brazos'] and b in r['brazos']]
    if not d: return '-'
    return f"{sum(x > 0 for x in d)}/{sum(x < 0 for x in d)} de {len(d)} (mediana {np.median(d):+.3f})"

for f in sys.argv[1:]:
    todo = json.load(open(f)); C = todo[0]['C']; brazos = list(todo[0]['brazos']); segs = [s[0] for s in todo[0]['segs']]
    print(f"\n# {f}  C={C}  n={len(todo)}")
    maestros = {'codigo': ['py1', 'py2'], 'inventado': ['inv1', 'inv2'], 'hechos': ['hechos1', 'hechos2', 'hechos3']}
    print("\n## acierto en linea por maestro (media de sus segmentos), mediana [min-max]; y hechos (sonda) tras hechos1/2/3; espanol al final")
    print("| brazo | codigo | inventado | hechos (en linea) | sonda hechos1 | hechos2 | hechos3 | espanol fin (base " + f"{med([r['brazos']['base']['sonda'][segs[-1]]['espanol'][1] for r in todo]):.3f}) | ops/letra | N fin |")
    print("|---|---|---|---|---|---|---|---|---|---|")
    for b in brazos:
        v = [r['brazos'][b] for r in todo]
        def mm(fn): x = [fn(y) for y in v]; return f"{np.median(x):.2f} [{min(x):.2f}-{max(x):.2f}]"
        print(f"| {b} | " + ' | '.join(mm(lambda y, m=m: np.mean([y['seg'][s]['acc'] for s in maestros[m] if s in y['seg']])) for m in maestros) +
              ' | ' + ' | '.join(mm(lambda y, s=s: y['hechos'][s]['acc']) for s in ('hechos1', 'hechos2', 'hechos3') if s in v[0]['hechos']) +
              f" | {mm(lambda y: y['sonda'][segs[-1]]['espanol'][1])} | {int(med([y['ops_por_letra'] for y in v]))} | {int(med([y['mem_fin'] for y in v]))} |")
    print("\n## pareadas por semilla (gana/pierde)")
    tests = [('acierto en linea total', lambda y: np.mean([y['seg'][s]['acc'] for s in y['seg']])),
             ('perdida en linea total (menor mejor: signo invertido)', lambda y: -np.mean([y['seg'][s]['nll'] for s in y['seg']])),
             ('sonda hechos1', lambda y: y['hechos']['hechos1']['acc']), ('sonda hechos3 (vuelta)', lambda y: y['hechos']['hechos3']['acc']),
             ('inventado en linea', lambda y: np.mean([y['seg'][s]['acc'] for s in ('inv1', 'inv2') if s in y['seg']])),
             ('espanol al final', lambda y: y['sonda'][segs[-1]]['espanol'][1])]
    for a, b in [('colonia', 'base'), ('colonia', 'knn'), ('colonia', 'gradiente'), ('colonia', 'col_barajada'), ('colonia', 'col_sin_compuerta'),
                 ('colonia', 'col_fija'), ('cuarentena', 'colonia'), ('sueno', 'colonia'), ('sueno_cuarentena', 'cuarentena'), ('knn', 'base'), ('gradiente', 'base')]:
        if a in brazos and b in brazos:
            print(f"- **{a} vs {b}**: " + '; '.join(f"{n}: {pares(todo, a, b, fn)}" for n, fn in tests))
    if 'mentiroso' in segs:
        print("\n## cuarentena: mentiras y verdades (mediana de semillas)")
        print("| brazo | hechos v1 tras hechos1 | tras mentiroso | tras ruido | unavez (verdad dicha 1 vez) tras unavez / al final | pisadas de celulas nacidas en mentiroso | en ruido | contra: dice v1 / v2 / lo de la base | digitos hechos1 por cuartos | reversiones | validadas fin | hipotesis fin | letras hasta validar |")
        print("|---|---|---|---|---|---|---|---|---|---|---|---|---|")
        for b in brazos:
            v = [r['brazos'][b] for r in todo]
            g = lambda fn, fmt='{:.2f}': fmt.format(med([fn(y) for y in v]))
            cu = [y['cuar'].get(segs[-1]) for y in v]
            print(f"| {b} | {g(lambda y: y['hechos']['hechos1']['acc'])} | {g(lambda y: y['hechos']['mentiroso']['acc'])} | {g(lambda y: y['hechos']['ruido']['acc'])} | "
                  f"{g(lambda y: y['unavez']['unavez'])} / {g(lambda y: y['unavez'][segs[-1]])} | {g(lambda y: y.get('pisa_origen', {}).get('mentiroso', 0), '{:.0f}')} | {g(lambda y: y.get('pisa_origen', {}).get('ruido', 0), '{:.0f}')} | "
                  f"{g(lambda y: y['hechos']['contra']['acc_v1'])} / {g(lambda y: y['hechos']['contra']['acc_v2'])} / {g(lambda y: y['hechos']['contra']['igual_base'])} | "
                  + '/'.join(f"{med([y['digitos']['hechos1'][q] for y in v]):.2f}" for q in range(4)) +
                  (f" | {med([c['reversiones'] for c in cu]):.0f} | {med([c['validadas'] for c in cu]):.0f} | {med([c['hipotesis'] for c in cu]):.0f} | {med([c['exp_validar'] or 0 for c in cu]):.0f} |" if cu[0] else " | - | - | - | - |"))
        for b in brazos:
            v = [r['brazos'][b] for r in todo]
            if v[0]['cuar']:
                print(f"- {b}: validadas por maestro (semilla 1) {v[0]['cuar'][segs[-1]]['validada_por']}; reversiones por maestro {v[0]['cuar'][segs[-1]]['reversion_por']}; "
                      f"reversiones tras hechos1/mentiroso/hechos2/hechos3/contra: " + '/'.join(f"{med([y['cuar'][s]['reversiones'] for y in v]):.0f}" for s in ('hechos1', 'mentiroso', 'hechos2', 'hechos3', 'contra')))
    print("\n## especializacion en 'mix' (pisadas hechas por una celula nacida en el mismo maestro) y nacimientos por maestro (semilla 1)")
    for b in brazos:
        v = [r['brazos'][b] for r in todo]
        if v[0].get('especializacion') is not None:
            print(f"- {b}: especializacion {med([y['especializacion'] for y in v]):.2f}; nacimientos {v[0]['nac_por']}; vivas por origen al final {v[0].get('origen_fin')}; estrechadas {med([y.get('estrechadas', 0) for y in v]):.0f}")
