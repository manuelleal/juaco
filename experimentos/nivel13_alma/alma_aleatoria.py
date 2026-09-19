"""CONTROL AUTOMATICO 1 del BLOQUE ALMA — CURITA AL AZAR del menu cerrado.

MISION: llegar a la AGI por este camino. Este control existe para que "el alma sirve" no pueda ganar por el mero
hecho de que ALGUIEN toque perillas: si tocar al azar da lo mismo, el alma no aporta nada y la hipotesis cae.

Corre SOLO, un proceso, sin Pool:
    python experimentos/nivel13_alma/alma_aleatoria.py [--sem 801] [--muertes 10] [--T 100000]

Es exactamente corre_alma.py --alma aleatoria: el rng de la eleccion es PROPIO (850000 + 1000000*sem) y no toca
el rng del mundo, igual que SEM_HIJO y SEM_BARAJA de H-1 (ERR-60).
"""
import os, sys

sys.stdout.reconfigure(encoding='utf-8', errors='replace')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import corre_alma

if __name__ == '__main__':
    if '--alma' in sys.argv:
        raise SystemExit('alma_aleatoria.py fija --alma aleatoria: no se pasa')
    sys.argv += ['--alma', 'aleatoria']
    sys.exit(corre_alma.main())
