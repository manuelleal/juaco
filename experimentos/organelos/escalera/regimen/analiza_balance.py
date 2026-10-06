"""analiza_balance.py — regimen (1-oct-2026). SIN correr nada. Dos cuentas sobre las 80 pruebas de la serie de perillas:
(1) el mundo A+C como TERMOMETRO del desbalance de mordidas: el mundo tiene 36 objetos; cada mordida y cada olvido (p 0.003 x 9 sorteos
    por paso ~ 2 700 en 100k) quita un objeto y repone uno de tipo uniforme (1/4 A, 1/4 C). En estado estacionario, el stock x de A+C cumple
    repuesto_AC = quitado_AC:  (mAC + mBD + O) / 2 = mAC + O * x / 36   ->   x = 18 (mBD - mAC + O) / O.
    Si la formula calza, 'pelar el mundo' = morder A/C MAS que B/D (mas selectivo), no menos.
(2) economia por cuerpo: ingesta = 1.6 por A/C dentro del oasis + 0.4 fuera; mordidas por vida; nacimientos por ingesta.
    python experimentos/organelos/escalera/regimen/analiza_balance.py
"""
import glob, json, math, os, statistics as st, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from analiza_serie import SERIE, spearman, pearson, med

O = 0.003 * 9 * 100000   # olvidos esperados en 100k pasos (pista: esc = N = 9 sorteos por paso con p 0.003)


def main():
    R = {}
    for f in sorted(glob.glob(os.path.join(SERIE, 'prueba_i*_*.json'))):
        d = json.load(open(f, encoding='utf-8')); R.setdefault(d['brazo'], {})[d['i']] = d
    print(f"(1) TERMOMETRO: x_pred = 18 (mBD - mAC + O) / O con O = {O:.0f}; por brazo mediana de (medido, predicho), y correlacion sobre las 80 pruebas")
    xs = []; ys = []
    for b in ('sel', 'neu', 'fab', 'o1'):
        m = [R[b][i]['mundo_AC'] for i in R[b]]; p = [18 * (R[b][i]['mord_BD'] - R[b][i]['mord_AC'] + O) / O for i in R[b]]
        xs += m; ys += p
        print(f"  {b:4s} medido {med(m):6.2f}  predicho {med(p):6.2f}  · mAC - mBD mediana {med([R[b][i]['mord_AC'] - R[b][i]['mord_BD'] for i in R[b]])}")
    print(f"  Pearson(medido, predicho) n {len(xs)}: {pearson(xs, ys):+.3f} · Spearman {spearman(xs, ys):+.3f} · error mediano {med([abs(a - b) for a, b in zip(xs, ys)])}")
    print("\n(2) ECONOMIA POR CUERPO (mediana por brazo): ingesta total (1.6 x AC dentro + 0.4 x AC fuera), ingesta por mordida AC, mordidas por nacimiento, vida")
    for b in ('sel', 'neu', 'fab', 'o1'):
        rows = []
        for i in R[b]:
            q = R[b][i]; oz = q['oasis']; ing = 1.6 * oz['mord_AC_dentro'] + 0.4 * oz['mord_AC_fuera']; nac = sum(q['nac_reales']); mu = sum(q['muertes'])
            rows.append(dict(ing=ing, por_mord=ing / q['mord_AC'], frac_in=oz['mord_AC_dentro'] / q['mord_AC'], mord_por_nac=q['mord_AC'] / nac, ing_por_nac=ing / nac,
                             nac=nac, muertes=mu, vida=q['vida_med'], mBD_por_mAC=q['mord_BD'] / q['mord_AC'], cuerpos=nac + sum(q['fund'])))
        print(f"  {b:4s} " + ' · '.join(f"{k} {med([r[k] for r in rows])}" for k in rows[0]))
    print("\n(3) dentro de sel: rho(GV, ingesta), rho(GV, frac dentro), rho(GV, mBD/mAC)")
    I = sorted(R['sel']); gv = [R['sel'][i]['genoma']['GV'] for i in I]
    ing = [1.6 * R['sel'][i]['oasis']['mord_AC_dentro'] + 0.4 * R['sel'][i]['oasis']['mord_AC_fuera'] for i in I]
    fi = [R['sel'][i]['oasis']['mord_AC_dentro'] / R['sel'][i]['mord_AC'] for i in I]; bd = [R['sel'][i]['mord_BD'] / R['sel'][i]['mord_AC'] for i in I]
    print(f"  ingesta {spearman(gv, ing):+.2f} · frac dentro {spearman(gv, fi):+.2f} · mBD/mAC {spearman(gv, bd):+.2f}")
    return 0


if __name__ == '__main__':
    sys.exit(main())
