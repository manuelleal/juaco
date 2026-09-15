"""
analiza_3k.py - evalua los criterios preregistrados de la rama 3K sobre el JSON de run_3k.py.
Uso: python analiza_3k.py [ruta_json]   (por defecto, el 3K_kenyon_*.json mas reciente de datos/)
"""
import sys, os, json, glob
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..', '..'))

NOM = {('fijo', 0.0): '1  fijo (=v6)'}
for lr in (0.003, 0.01, 0.03):
    NOM[('hebb_visita', lr)] = f'2  hebb_visita lr={lr}'
    NOM[('hebb_mordida', lr)] = f'2b hebb_mordida lr={lr}'
    NOM[('error', lr)] = f'3  error       lr={lr}'


def med(v): return float(np.median(v))
def rng_(v): return f"[{min(v):.2f},{max(v):.2f}]"


def sel(filas, modo, lr, var):
    d = {r['seed']: r for r in filas if r['modo'] == modo and abs(r['k_lr'] - lr) < 1e-12 and r['variante'] == var}
    return [d[s] for s in sorted(d)]


def col(rs, c): return [r[c] for r in rs]


if __name__ == "__main__":
    if len(sys.argv) > 1:
        path = sys.argv[1]
    else:
        path = sorted(glob.glob(os.path.join(ROOT, 'datos', '3K_kenyon_*.json')))[-1]
    D = json.load(open(path, encoding='utf-8'))
    filas, proc = D['filas'], D['procedencia']
    celdas = [(c[0], float(c[1])) for c in proc['malla']['celdas']]
    S = proc['semillas']
    print(f"=== 3K Kenyon aprendido — {os.path.basename(path)} ===")
    print(f"{S} semillas, T={proc['T']}, fase2={proc['fase2_en']}, "
          f"sha organismo_3k={proc['sha256_16']['organismo_3k']}, PREREGISTRO={proc['sha256_16']['PREREGISTRO']}")

    for var in ('congelado', 'aprende'):
        print(f"\n\n########## VARIANTE FASE 2: {var} "
              f"({'toda la plasticidad apagada — generalizacion de tiro cero' if var=='congelado' else 'sigue aprendiendo'}) ##########")
        print(f"\n{'condicion':26s} {'precTest':>9s} {'rango':>14s} {'tComida':>8s} {'tVeneno':>8s} "
              f"{'accSigno':>9s} {'Wa_com':>7s} {'Wa_ven':>7s} {'muert':>6s} {'precTren':>9s}")
        print("-" * 118)
        for (m, lr) in celdas:
            rs = sel(filas, m, lr, var)
            if not rs: continue
            p = col(rs, 'prec_test')
            print(f"{NOM[(m,lr)]:26s} {med(p):9.3f} {rng_(p):>14s} "
                  f"{med(col(rs,'tasa_test_comida')):8.3f} {med(col(rs,'tasa_test_veneno')):8.3f} "
                  f"{med(col(rs,'acc_signo')):9.3f} {med(col(rs,'Wa_test_comida')):+7.2f} "
                  f"{med(col(rs,'Wa_test_veneno')):+7.2f} {med(col(rs,'deaths')):6.0f} "
                  f"{med(col(rs,'prec_tren')):9.3f}")

        print(f"\n{'condicion':26s} {'r_clase':>8s} {'r_solap':>8s} {'|rs|>|rc|':>10s} {'ratio_disp':>11s} "
              f"{'ratio_med':>10s} {'sel_clase':>10s} {'ratio_solap':>12s} {'celdas':>7s} {'derivaKW':>9s}")
        print("-" * 118)
        for (m, lr) in celdas:
            rs = sel(filas, m, lr, var)
            if not rs: continue
            rc = [abs(x) for x in col(rs, 'r_clase') if x == x]
            rsol = [abs(x) for x in col(rs, 'r_solap') if x == x]
            gana = sum(1 for r in rs if abs(r['r_solap']) > abs(r['r_clase']))
            print(f"{NOM[(m,lr)]:26s} {med(rc):8.2f} {med(rsol):8.2f} {gana:>7d}/{len(rs):<2d} "
                  f"{med(col(rs,'ratio_disp')):11.3f} {med(col(rs,'ratio_media')):10.3f} "
                  f"{med(col(rs,'sel_clase')):10.3f} {med(col(rs,'ratio_solap')):12.3f} "
                  f"{med(col(rs,'celdas_usadas')):7.0f} {med(col(rs,'deriva_kw')):9.4f}")

    # ---------- CRITERIOS PREREGISTRADOS ----------
    print("\n\n########## CRITERIOS PREREGISTRADOS ##########")
    base = sel(filas, 'fijo', 0.0, 'congelado')
    b = {r['seed']: r for r in base}
    print(f"\nCondicion 1 (fijo): precision mediana = {med(col(base,'prec_test')):.3f} "
          f"{rng_(col(base,'prec_test'))}")
    print("  Prediccion preregistrada C1: precision mediana en (0.50, 0.70) -> "
          f"{'SE CUMPLE' if 0.50 < med(col(base,'prec_test')) < 0.70 else 'NO SE CUMPLE'}")
    grc = med([abs(x) for x in col(base, 'r_clase')]); grs = med([abs(x) for x in col(base, 'r_solap')])
    gana = sum(1 for r in base if abs(r['r_solap']) > abs(r['r_clase']))
    print(f"  Prediccion C1 |r_solap|>|r_clase|: {grs:.2f} vs {grc:.2f}, {gana}/{len(base)} semillas -> "
          f"{'SE CUMPLE' if grs > grc else 'NO SE CUMPLE'}")

    print("\n-- C-1 (margen >= +0.10) y C-2 (pareado > 0 en >=15/20), variante congelado --")
    print(f"{'condicion':26s} {'prec':>7s} {'delta_med':>10s} {'C-1':>6s} {'pareado':>9s} {'C-2':>6s} "
          f"{'muertes':>8s} {'C-3b':>6s}")
    print("-" * 90)
    mdb = med(col(base, 'deaths'))
    for (m, lr) in celdas:
        if m == 'fijo': continue
        rs = sel(filas, m, lr, 'congelado')
        dd = [r['prec_test'] - b[r['seed']]['prec_test'] for r in rs]
        delta = med(col(rs, 'prec_test')) - med(col(base, 'prec_test'))
        pos = sum(1 for x in dd if x > 0)
        c1 = delta >= 0.10; c2 = pos >= 15; c3b = med(col(rs, 'deaths')) <= 1.5 * mdb
        print(f"{NOM[(m,lr)]:26s} {med(col(rs,'prec_test')):7.3f} {delta:+10.3f} "
              f"{'SI' if c1 else 'no':>6s} {pos:>6d}/{len(rs):<2d} {'SI' if c2 else 'no':>6s} "
              f"{med(col(rs,'deaths')):8.0f} {'SI' if c3b else 'no':>6s}")

    print("\n-- Co-primaria mecanistica: acc_signo del valor a priori (delta >= +0.10) --")
    for (m, lr) in celdas:
        if m == 'fijo': continue
        rs = sel(filas, m, lr, 'congelado')
        delta = med(col(rs, 'acc_signo')) - med(col(base, 'acc_signo'))
        print(f"{NOM[(m,lr)]:26s} acc_signo={med(col(rs,'acc_signo')):.3f} delta={delta:+.3f} "
              f"{'SI' if delta >= 0.10 else 'no'}")

    print("\n-- PRIMARIA: condicion 3 (error, k_lr=0.01, congelado) vs condicion 1 --")
    rs = sel(filas, 'error', 0.01, 'congelado')
    dd = [r['prec_test'] - b[r['seed']]['prec_test'] for r in rs]
    delta = med(col(rs, 'prec_test')) - med(col(base, 'prec_test'))
    pos = sum(1 for x in dd if x > 0)
    print(f"  precision 1 = {med(col(base,'prec_test')):.3f} {rng_(col(base,'prec_test'))}")
    print(f"  precision 3 = {med(col(rs,'prec_test')):.3f} {rng_(col(rs,'prec_test'))}")
    print(f"  C-1 margen  = {delta:+.3f}  (>= +0.10)  -> {'PASA' if delta>=0.10 else 'FALLA'}")
    print(f"  C-2 pareado = {pos}/{len(rs)}  (>= 15)     -> {'PASA' if pos>=15 else 'FALLA'}")
    print(f"  C-3b muertes= {med(col(rs,'deaths')):.0f} vs {mdb:.0f}x1.5={1.5*mdb:.0f} -> "
          f"{'PASA' if med(col(rs,'deaths'))<=1.5*mdb else 'FALLA'}")
    print(f"  deltas por semilla: {' '.join(f'{x:+.2f}' for x in dd)}")
    print(f"\n  VEREDICTO PREREGISTRADO: "
          f"{'HIPOTESIS SOSTENIDA' if (delta>=0.10 and pos>=15) else 'HIPOTESIS REFUTADA'}")

    print("\n-- Trayectoria por cuarto de fase 2 (variante aprende) --")
    print(f"{'condicion':26s} {'q1':>6s} {'q2':>6s} {'q3':>6s} {'q4':>6s}   (variante congelado: q1..q4)")
    for (m, lr) in celdas:
        if m != 'fijo' and abs(lr - 0.01) > 1e-12: continue
        ra = sel(filas, m, lr, 'aprende'); rc_ = sel(filas, m, lr, 'congelado')
        a = [med(col(ra, f'prec_test_q{i}')) for i in range(1, 5)]
        c = [med(col(rc_, f'prec_test_q{i}')) for i in range(1, 5)]
        print(f"{NOM[(m,lr)]:26s} " + " ".join(f"{x:6.3f}" for x in a) +
              "   " + " ".join(f"{x:6.3f}" for x in c))
