"""construye_ohno.py — COPIA VERIFICADA del instrumento de GRAMATICA para el paquete OHNO SOBRE BASE VIVA (Opus A, 24-sep-2026).

MISION: llegar a la AGI por este camino.

OHNO no necesita codigo nuevo en el motor ni en el carro: el mundo mas pobre es un argumento que motor_gramatica ya recibe (r_rep, el
quimiostato de P7) y los fundadores con filtra0 expresado son un valor de eco['gramatica']. Por eso las copias son BYTE A BYTE (sha
fijado) y todo lo nuevo vive en corre_ohno.py. Origenes (SOLO se LEEN), en experimentos/organelos/gramatica/ (commit 48f99b8):
  motor_gramatica.py          6b65dc5e32093424
  carros/FAMB_GRAM_ECO.py     2cee0a8510c997b9
  gramatica_def.py            c58086e103d030d9
  conducta.py                 9a2f1226fe27a514
Uso: python experimentos/organelos/ohno/construye_ohno.py [--verifica]
"""
import hashlib, os, sys

AQUI = os.path.dirname(os.path.abspath(__file__))
ORIG = os.path.join(os.path.dirname(AQUI), 'gramatica')
ARCH = {'motor_gramatica.py': '6b65dc5e32093424', os.path.join('carros', 'FAMB_GRAM_ECO.py'): '2cee0a8510c997b9',
        'gramatica_def.py': 'c58086e103d030d9', 'conducta.py': '9a2f1226fe27a514'}


def h16b(b): return hashlib.sha256(b).hexdigest()[:16]


def main():
    ver = '--verifica' in sys.argv[1:]
    if set(sys.argv[1:]) - {'--verifica'}: raise SystemExit(f"CONSTRUYE: banderas desconocidas {sys.argv[1:]}")
    ok = True
    for rel, sha in ARCH.items():
        b = open(os.path.join(ORIG, rel), 'rb').read()
        if h16b(b) != sha: raise SystemExit(f"CONSTRUYE: el origen {rel} cambio ({h16b(b)} != {sha})")
        dst = os.path.join(AQUI, rel)
        if ver:
            ok = ok and os.path.exists(dst) and open(dst, 'rb').read() == b
        else:
            os.makedirs(os.path.dirname(dst), exist_ok=True)
            open(dst, 'wb').write(b); print(rel, sha)
    if ver: print('VERIFICA', 'OK' if ok else 'FALLA'); sys.exit(0 if ok else 1)


if __name__ == '__main__':
    main()
