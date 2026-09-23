"""construye_ctrl_o3.py — construye carros_ctrl/CTRL_O3_SINTERM.py POR ANCLA desde carrera_escuderias/carros/O3.py (sha fijado).

MISION: llegar a la AGI por este camino.

Control del mecanismo (PREREGISTRO_convive.md, H-b): O3 con la muerte programada APAGADA. Un unico cambio de codigo:
la linea 'TERMINAL = True' pasa a 'TERMINAL = False' (el propio O3 declara: "se apaga con TERMINAL = False"). Mas la
cabecera del docstring. Fines de linea preservados (LF, como O3.py; se trabaja en bytes). El control de O4 es O1 (O4 con M2 = False es
O1 decision a decision, segun su docstring y su bitacora), que ya esta en la serie.
Uso: python experimentos/generaciones/construye_ctrl_o3.py
"""
import hashlib, os, sys

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
ORIGEN = os.path.join(RAIZ, 'experimentos', 'carrera_escuderias', 'carros', 'O3.py')
SHA_ORIGEN = '0442c2884fcb0e11'
DESTINO = os.path.join(AQUI, 'carros_ctrl', 'CTRL_O3_SINTERM.py')
ANCLAS = [(b'"""carros/O3.py \xe2\x80\x94 escuderia O3',
           b'"""CTRL_O3_SINTERM (construido por experimentos/generaciones/construye_ctrl_o3.py desde carros/O3.py sha '
           + SHA_ORIGEN.encode() + b'; UNICO cambio: TERMINAL = False). carros/O3.py \xe2\x80\x94 escuderia O3'),
          (b'\nTERMINAL = True\n', b'\nTERMINAL = False\n')]


def main():
    src = open(ORIGEN, 'rb').read(); sha = hashlib.sha256(src).hexdigest()[:16]
    if sha != SHA_ORIGEN: raise SystemExit(f"CONSTRUYE: O3.py cambio ({sha} != {SHA_ORIGEN})")
    out = src
    for i, (a, b) in enumerate(ANCLAS, 1):
        if out.count(a) != 1: raise SystemExit(f"CONSTRUYE: ancla {i} aparece {out.count(a)} veces")
        out = out.replace(a, b)
    os.makedirs(os.path.dirname(DESTINO), exist_ok=True)
    open(DESTINO, 'wb').write(out)
    print(f"O3.py sha {sha} OK · CTRL_O3_SINTERM.py sha {hashlib.sha256(out).hexdigest()[:16]}")


if __name__ == '__main__':
    sys.exit(main())
