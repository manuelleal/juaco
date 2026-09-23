"""construye_pista2.py — construye pista2.py POR ANCLAS desde carrera_escuderias/pista.py (sha fijado).

MISION: llegar a la AGI por este camino.

Origen (solo se LEE): experimentos/carrera_escuderias/pista.py, sha16 9f47c65e438e0ff4 (HEAD a170746 de la rama
carrera-escuderias). Cada ancla debe aparecer EXACTAMENTE una vez; si no, aborta sin escribir nada.
Cambios (los unicos):
  A1 cabecera del docstring: dice de donde sale.
  A2 CARROS apunta a experimentos/carrera_escuderias/carros (los carros NO se copian: corren sin cambios).
  A3 run(...) gana solapadas=0 y **kw_conv. Con solapadas=0 el cuerpo de run es el ORIGINAL byte a byte (arnes);
     con solapadas=1 delega en motor_convive.run_solapadas (el mundo con generaciones solapadas).
Uso: python experimentos/generaciones/construye_pista2.py
"""
import hashlib, os, sys

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
ORIGEN = os.path.join(RAIZ, 'experimentos', 'carrera_escuderias', 'pista.py')
SHA_ORIGEN = '9f47c65e438e0ff4'
DESTINO = os.path.join(AQUI, 'pista2.py')
NL = b'\r\n'

ANCLAS = [
    (b'"""pista.py \xe2\x80\x94 LA PISTA DE LA CARRERA DE ESCUDERIAS',
     b'"""pista2.py (CONSTRUIDO por experimentos/generaciones/construye_pista2.py desde carrera_escuderias/pista.py, sha '
     + SHA_ORIGEN.encode() + b'; NO editar a mano)' + NL
     + b'VERSION 2: opcion solapadas=1 -> motor_convive.run_solapadas (generaciones solapadas: el hijo nace como cuerpo vivo).' + NL
     + b'Con solapadas=0 es la pista original bit a bit (identidad_convive.py).' + NL + NL
     + b'pista.py \xe2\x80\x94 LA PISTA DE LA CARRERA DE ESCUDERIAS'),
    (b"CARROS = os.path.join(AQUI, 'carros')",
     b"CARROS = os.path.join(RAIZ, 'experimentos', 'carrera_escuderias', 'carros')   # pista2: los carros de la carrera, sin copiar"),
    (b"def run(seed, carros, T=100000, pizarra=1, compat=0, rep_acum=0, escala=1, telem=True, diag=1, mundo_n=None, fundador_limpio=0):",
     b"def run(seed, carros, T=100000, pizarra=1, compat=0, rep_acum=0, escala=1, telem=True, diag=1, mundo_n=None, fundador_limpio=0,"
     + NL + b"        solapadas=0, **kw_conv):"),
    (b"    n = len(carros)" + NL + b"    if not 1 <= n <= N_MAX:",
     b"    if solapadas:   # pista2: generaciones solapadas (motor_convive.py)" + NL
     + b"        if AQUI not in sys.path: sys.path.insert(0, AQUI)" + NL
     + b"        import motor_convive as _MC" + NL
     + b"        return _MC.run_solapadas(seed, carros, T=T, pizarra=pizarra, compat=compat, rep_acum=rep_acum, escala=escala, telem=telem," + NL
     + b"                                 diag=diag, mundo_n=mundo_n, fundador_limpio=fundador_limpio, **kw_conv)" + NL
     + b"    if kw_conv: raise SystemExit(f\"PISTA2: opciones de solapadas {sorted(kw_conv)} con solapadas=0\")" + NL
     + b"    n = len(carros)" + NL + b"    if not 1 <= n <= N_MAX:"),
]


def main():
    src = open(ORIGEN, 'rb').read()
    sha = hashlib.sha256(src).hexdigest()[:16]
    if sha != SHA_ORIGEN:
        raise SystemExit(f"CONSTRUYE: el origen cambio (sha {sha} != {SHA_ORIGEN}); no se construye")
    out = src
    for i, (a, b) in enumerate(ANCLAS, 1):
        k = out.count(a)
        if k != 1: raise SystemExit(f"CONSTRUYE: ancla A{i} aparece {k} veces (debe ser 1); no se construye")
        out = out.replace(a, b)
    open(DESTINO, 'wb').write(out)
    print(f"origen {ORIGEN} sha {sha} OK · {len(ANCLAS)} anclas aplicadas · pista2.py sha {hashlib.sha256(out).hexdigest()[:16]}")


if __name__ == '__main__':
    sys.exit(main())
