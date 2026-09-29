"""corre_cond.py — EXTRA POST HOC de la sonda: brazo orgcond (V143_TERMO_ORGCOND) con la misma corrida de corre_organo (importado).
  python .../corre_cond.py --arnes          # ORGANO 0 de este constructor == V143_TERMO bit a bit (49856, T 20 000)
  python .../corre_cond.py --corre 49851    # una corrida T 100 000 (semillas de la sonda 49851-49855), escribe JSON
"""
import argparse, importlib.util, json, os, sys, time
AQUI = os.path.dirname(os.path.abspath(__file__))
if AQUI not in sys.path: sys.path.insert(0, AQUI)
import corre_organo as CR
CR.BRAZOS.update({'orgcond': 'V143_TERMO_ORGCOND', 'orgc0': 'V143_TERMO_ORGC0'})
# E1 (arnes cond, 20:40): limpia() reemplaza nombres en orden y 'V143_TERMO_ORG' se comia 'V143_TERMO_ORGC0' -> 'CARROC0' (falso
# False). Arreglo: los nombres largos primero.
CR.PROPIOS = tuple(sorted(CR.PROPIOS + ('V143_TERMO_ORGC0', 'V143_TERMO_ORGCOND'), key=len, reverse=True))


def main():
    ap = argparse.ArgumentParser(allow_abbrev=False); ap.add_argument('--arnes', action='store_true'); ap.add_argument('--corre', type=int)
    a = ap.parse_args()
    if a.arnes:
        x = CR.limpia(CR.corre(CR.ARNES, 'termo', CR.T_HUMO)); y = CR.limpia(CR.corre(CR.ARNES, 'orgc0', CR.T_HUMO))
        print(f"(A') ORGANO 0 (constructor cond) == V143_TERMO bit a bit (49856, T {CR.T_HUMO}): {x == y}"); return 0 if x == y else 1
    if a.corre:
        if a.corre not in CR.SONDA: raise SystemExit('fuera de la sonda')
        x = CR.corre(a.corre, 'orgcond', CR.T_SONDA)
        print(time.strftime('%H:%M:%S'), 'escrito', CR.escribe(x, os.path.join(CR.DATOS, f'sonda_T{CR.T_SONDA}')), x['seg'], 's', flush=True)


if __name__ == '__main__':
    main()
