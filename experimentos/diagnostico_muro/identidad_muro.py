"""identidad_muro.py — arnes de identidad bit a bit (perillas de instrumentacion "apagadas" no aplica aqui:
la instrumentacion del MURO es observacion PURA, siempre activa, y por construccion no debe cambiar NINGUN
valor existente). Compara organismo_f9c.run (ORIGEN, sin tocar) contra organismo_f9c_muro.run (aqui) en los
BRAZOS EXACTOS de fase 9 bloque 2 (importados de corre_bloque2.BRAZOS, regla 14 por identidad de objeto).

Corre ANTES de mirar ningun numero del diagnostico (regla del equipo: arnes con las perillas apagadas ANTES
de mirar numeros). Imprime PASA/FALLA por brazo x semilla y una linea final.
"""
import os
import sys
import time

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
N09B2 = os.path.join(RAIZ, 'experimentos', 'nivel09_cuerpo_nuevo_b2')
sys.path[:0] = [N09B2]          # para que "import corre_bloque2" resuelva sus propios imports (organismo_f9c ORIGINAL incluido)
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

import corre_bloque2 as B2       # esto inserta N09B2, N09, N13, N11, organismo/ al FRENTE de sys.path (ver corre_bloque2.py)
import organismo_f9c as F9C_ORIG  # el ORIGEN, sin tocar (queda resuelto por el sys.path de arriba)

sys.path.insert(0, AQUI)          # AHORA mi carpeta, para el archivo instrumentado (nombre distinto: no hay choque)
import organismo_f9c_muro as F9M

N = B2.N


def compara(a, b):
    """Todas las claves de `a` (ORIGEN) deben existir en `b` con el mismo valor normalizado N(); `b` puede
    tener EXACTAMENTE una clave de mas: 'muro'."""
    falta = [k for k in a if k not in b]
    dif = [k for k in a if k in b and N(a[k]) != N(b[k])]
    extra = set(b) - set(a)
    ok = not falta and not dif and extra == {'muro'}
    return ok, falta, dif, sorted(extra)


def main():
    T = 20000
    casos = [('NADA', 1), ('NADA', 2), ('REL', 1), ('REL', 2), ('ORACULO', 1), ('RENACE', 1)]
    print(f"IDENTIDAD MURO · organismo_f9c (sha {B2.h16(os.path.join(N09B2,'organismo_f9c.py'))}) vs "
          f"organismo_f9c_muro (sha {B2.h16(os.path.join(AQUI,'organismo_f9c_muro.py'))}) · T={T}")
    t0 = time.time()
    todo_ok = True
    filas = []
    for brazo, seed in casos:
        kw = dict(B2.BRAZOS[brazo], rep_acum=0)
        a = F9C_ORIG.run(seed, T=T, **kw)
        b = F9M.run(seed, T=T, **kw)
        ok, falta, dif, extra = compara(a, b)
        todo_ok &= ok
        muro = b.get('muro', {})
        print(f"  {'OK  ' if ok else 'FALLA'} {brazo:8s} s{seed}  extra={extra}  falta={falta[:5]}  "
              f"dif={dif[:5]}  ·  muro.pres={muro.get('pres')} pasos={muro.get('pasos')} "
              f"muertes_registradas={len(muro.get('pre_death_bad', []))}")
        filas.append((brazo, seed, ok))
    print(f"\nT=100000 (una corrida larga, brazo REL, semilla 1) para exponer casos raros de mas pasos")
    kw = dict(B2.BRAZOS['REL'], rep_acum=0)
    a = F9C_ORIG.run(1, T=100000, **kw)
    b = F9M.run(1, T=100000, **kw)
    ok, falta, dif, extra = compara(a, b)
    todo_ok &= ok
    print(f"  {'OK  ' if ok else 'FALLA'} REL s1 T=100000  extra={extra} falta={falta[:5]} dif={dif[:5]} "
          f"muro.pasos={b['muro']['pasos']} (debe ser 100000) muertes={len(b['muro']['pre_death_bad'])} "
          f"(debe ser igual a b['deaths']={b['deaths']})")
    todo_ok &= (b['muro']['pasos'] == 100000) and (len(b['muro']['pre_death_bad']) == b['deaths'])
    print(f"\n{'TODO PASA' if todo_ok else 'ALGO FALLA'} en {time.time()-t0:.1f}s")
    return 0 if todo_ok else 1


if __name__ == '__main__':
    sys.exit(main())
