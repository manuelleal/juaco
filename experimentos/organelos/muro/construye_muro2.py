"""construye_muro2.py — el carro NUEVO del SEGUNDO intento del muro (PREREGISTRO_muro2.md): el control V143_GLOTUPATASDESF.

MISION: llegar a la AGI por este camino.
NO toca construye_muro.py (sha ad607c6ad4f9ced9: es el instrumento de la serie 1, que esta corriendo). IMPORTA su funcion construye()
(las mismas nueve anclas desde V143.py 2a03048a7f1525e5) y genera UNA variante mas, con la misma linea de perillas:
  V143_GLOTUPATASDESF   PAGA 0 · GLOT 3 (GLOTU) · PATAS 2 (patas a lo que sirve a la OTRA necesidad) · TELEM 1
El candidato del segundo intento es V143_GLOTUPATAS (0, 3, 1, 1), que YA genera construye_muro.py (sha dec2d8ceb004e541).

    python experimentos/organelos/muro/construye_muro2.py [--verifica]
"""
import argparse, os, sys

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
import construye_muro as CB

SHA_CONSTRUYE_MURO = 'ad607c6ad4f9ced9'
VARIANTES2 = [('V143_GLOTUPATASDESF', 0, 3, 2, 1)]


def todas2():
    return {n: CB.construye(n, p, g, q, t) for n, p, g, q, t in VARIANTES2}


def main(argv=None):
    ap = argparse.ArgumentParser(allow_abbrev=False)
    ap.add_argument('--verifica', action='store_true')
    a = ap.parse_args(argv)
    s = CB.h16(CB.__file__)
    if s != SHA_CONSTRUYE_MURO: raise SystemExit(f"construye_muro.py sha {s} != {SHA_CONSTRUYE_MURO}")
    # la variante nueva difiere de V143_GLOTUPATAS SOLO en la linea de perillas y en el nombre
    base = CB.construye('V143_GLOTUPATAS', 0, 3, 1, 1).decode('utf-8').split(CB.NL)
    ok = True
    for n, bts in todas2().items():
        ls = bts.decode('utf-8').split(CB.NL)
        dif = [i for i, (x, y) in enumerate(zip(base, ls)) if x != y]
        if len(ls) != len(base) or any(not ('PAGA = ' in ls[i] or n in ls[i]) for i in dif):
            raise SystemExit(f"{n}: difiere de V143_GLOTUPATAS en algo mas que perillas/nombre: lineas {dif[:6]}")
        ruta = os.path.join(CB.SALIDA, n + '.py')
        if a.verifica:
            igual = os.path.exists(ruta) and open(ruta, 'rb').read() == bts; ok &= igual
            print(f"  {n} sha {CB.h16b(bts)} == disco: {igual}")
        else:
            with open(ruta, 'wb') as fh: fh.write(bts)
            print(f"  escrito {ruta} (sha {CB.h16b(bts)})")
    print(f"construye_muro.py sha {s} · construye_muro2.py sha {CB.h16(os.path.abspath(__file__))}")
    return 0 if ok else 1


if __name__ == '__main__':
    sys.exit(main())
