"""CONTROL AUTOMATICO 2 del BLOQUE ALMA — SIN CURITA Y SIN NODO (la linea base de H-1).

MISION: llegar a la AGI por este camino. Este control es H-1 tal cual (CUELLO_MIN, muerte real, hereda nada,
dote 0.6) mirado cuerpo a cuerpo: es el 0.148 de R0 contra el que todo lo demas se compara. Si el alma no lo
supera, no hay nada que contar.

Corre SOLO, un proceso, sin Pool:
    python experimentos/nivel13_alma/alma_ninguna.py [--sem 801] [--muertes 10] [--T 100000]

Es corre_alma.py --alma ninguna: la curita es siempre (f) NADA y el runner apaga el nodo (`nodo=0`), asi que ni
se llena ni se lee. La UNICA diferencia con organismo_vivo_h1 es que la corrida para en la muerte `--muertes` y
que se registran las vidas y los hijos cuerpo a cuerpo (solo lectura).
"""
import os, sys

sys.stdout.reconfigure(encoding='utf-8', errors='replace')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import corre_alma

if __name__ == '__main__':
    if '--alma' in sys.argv:
        raise SystemExit('alma_ninguna.py fija --alma ninguna: no se pasa')
    sys.argv += ['--alma', 'ninguna']
    sys.exit(corre_alma.main())
