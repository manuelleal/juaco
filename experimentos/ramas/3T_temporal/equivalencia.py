"""Prueba de que anadir los parametros nkmax/wclip a mundo_temporal.run es INERTE:
con los valores por defecto (90, 3.0) las 120 corridas deben coincidir campo a campo
con el CSV confirmatorio corrido ANTES del cambio. Mismo patron que v7 vs v7c en el registro."""
import sys, os, csv, glob
try: sys.stdout.reconfigure(encoding='utf-8', errors='replace')
except Exception: pass
AQUI = os.path.dirname(os.path.abspath(__file__))


def leer(p):
    with open(p, encoding='utf-8') as fh:
        lin = [l for l in fh if not l.startswith('#')]
    return {(r['arm'], r['seed']): r for r in csv.DictReader(lin)}


def main(a, b):
    A, B = leer(a), leer(b)
    print(f"antes : {os.path.basename(a)}  n={len(A)}")
    print(f"despues: {os.path.basename(b)}  n={len(B)}")
    assert set(A) == set(B), "conjuntos de (arm,seed) distintos"
    dif = [(k, c, A[k][c], B[k][c]) for k in A for c in A[k] if A[k][c] != B[k][c]]
    print(f"campos comparados: {len(A)*len(next(iter(A.values())))}   discrepancias: {len(dif)}")
    print("-> EQUIVALENCIA EXACTA. El cambio es inerte." if not dif else f"-> FALLA: {dif[:10]}")
    return not dif


if __name__ == '__main__':
    cs = sorted(glob.glob(os.path.join(AQUI, '3T_*.csv')))
    main(sys.argv[1] if len(sys.argv) > 2 else cs[0], sys.argv[2] if len(sys.argv) > 2 else cs[-1])
