#!/usr/bin/env python3
"""corre_H1_humo.py — Humo minimalista de H1 vs FABRICA.

Correo con semillas 4151-4152, T=10000, 2 cuerpos (H1 + FABRICA).
Objetivo: comparar R0 de H1 contra FABRICA en competencia real (N=2).
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import pista as P
import revisa_carro as RC

AQUI = os.path.dirname(os.path.abspath(__file__))

def test_h1():
    # Revisa que H1 pase la validacion
    v = RC.revisa('H1')
    if v:
        print("H1 NO PASA VALIDACION:")
        for x in v:
            print(f"  {x}")
        return False
    print("H1 PASA validacion.")

    # Corre humo: H1 + FABRICA, 2 cuerpos
    print("\nCorriendo humo H1 vs FABRICA (2 cuerpos, semilla 4151, T=10000)...")
    r = P.run(4151, ['H1', 'FABRICA'], T=10000, pizarra=0, compat=0, rep_acum=0, escala=0)

    print("\nResultados:")
    for i, d in enumerate(r['linajes']):
        print(f"  Linaje {i} ({d['id']}):")
        print(f"    R0: {d['R0']:.4f}")
        print(f"    Descendientes: {d['descendientes']}")
        print(f"    Muertes: {d['muertes']}")
        print(f"    Vida mediana: {d['vida_med']}")
        print(f"    Coherente: {d['coherente']}")

    print(f"\nR0 pista: {r['pista']['R0_pista']:.4f}")
    print(f"Composicion mundo: {r['pista']['comp_mundo']}")

    return True

if __name__ == '__main__':
    if not test_h1():
        sys.exit(1)
    print("\nHumo completado.")
