"""construye_eco_familia.py — CONSTRUYE POR ANCLAS el carro FAMB_RES0_ECO de ECO v1.2 (nube, 24-sep-2026). No se edita a mano.

MISION: llegar a la AGI por este camino.

Origen (SOLO se LEE; sha fijado): experimentos/subida_n10b/carros/FAMB_RES.py 2addb7ca5b9d031d (la familia pasa su TABLA en el parto;
es FABRICA con MODO = 'res'). Tres cambios, los tres ya medidos en otro sitio:
  (1) _see() hacia afuera, O(distancia), misma salida: el MISMO texto que construye_eco.py puso en FABRICA_ECO (arnes (F) de ECO).
  (2) la funcion _elige de construye_eco.py.
  (3) SIN0 = 1: el hijo descarta las entradas neutras (R == 0) de la tabla recibida ANTES de todo lo demas. Es EXACTAMENTE el filtro
      de subida_n10c (carros_n10c._hijo_filtra: si la memoria no esta vacia, sin_neutras), FUNCIONA x2 en la nube el 24-sep.
Con SIN0 = 0 el carro es FAMB_RES (salvo _see, de salida identica). Arnes: identidad_eco_familia.py.
Uso: python experimentos/juaco_eco/construye_eco_familia.py [--verifica]
"""
import hashlib, os, sys

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
sys.path.insert(0, AQUI)
import construye_eco as CE

ORIG = os.path.join(RAIZ, 'experimentos', 'subida_n10b', 'carros', 'FAMB_RES.py')
SHA_ORIG = '2addb7ca5b9d031d'
DESTINO = os.path.join(AQUI, 'carros', 'FAMB_RES0_ECO.py')

MODO_ORIG = "MODO = 'res'   # SUBIDA_N10B: nada | res | res1 | bar | oraculo\n"
MEM_ORIG = "        _mem = info.get('memoria')\n"


def texto(sin0=1):
    if CE.h16(ORIG) != SHA_ORIG: raise SystemExit(f"CONSTRUYE: FAMB_RES.py cambio (sha {CE.h16(ORIG)} != {SHA_ORIG})")
    txt = open(ORIG, encoding='utf-8').read()
    cab = ('"""carros/FAMB_RES0_ECO.py (CONSTRUIDO por experimentos/juaco_eco/construye_eco_familia.py desde '
           f'subida_n10b/carros/FAMB_RES.py, sha {SHA_ORIG}; NO editar a mano).\n'
           'ECO v1.2: (1) _see() hacia afuera (el de FABRICA_ECO, misma salida); (2) _elige; (3) SIN0: el hijo descarta las entradas\n'
           'neutras (R == 0) de la tabla recibida (el filtro de subida_n10c). Lo que sigue es el docstring del origen.\n\n')
    anclas = [
        ('"""carros/FAMB_RES.py', cab + 'carros/FAMB_RES.py'),
        (CE.SEE_ORIG, CE.SEE_ECO),
        ('\n\ndef crea(ctx):', CE.ELIGE),
        (MODO_ORIG, MODO_ORIG + f"SIN0 = {int(sin0)}   # ECO v1.2 (subida_n10c): el hijo descarta las entradas neutras (R == 0) de la tabla recibida\n"),
        (MEM_ORIG, MEM_ORIG + "        if SIN0 and _mem:   # ECO v1.2 = subida_n10c RES_SIN0: sin lo neutro, ANTES de todo lo demas\n"
                              "            _mem = [_e7 for _e7 in _mem if float(_e7[1]) != 0.0]\n"),
    ]
    return CE.aplica(txt, anclas, 'FAMB_RES0_ECO')


if __name__ == '__main__':
    s = texto(1)
    if '--verifica' in sys.argv[1:]:
        ok = os.path.exists(DESTINO) and open(DESTINO, encoding='utf-8').read() == s
        print('VERIFICA', 'OK' if ok else 'FALLA'); sys.exit(0 if ok else 1)
    if set(sys.argv[1:]) - {'--verifica'}: raise SystemExit(f"CONSTRUYE: banderas desconocidas {sys.argv[1:]}")
    with open(DESTINO, 'w', encoding='utf-8', newline='\n') as f: f.write(s)
    print(os.path.relpath(DESTINO, RAIZ), CE.h16s(s))
