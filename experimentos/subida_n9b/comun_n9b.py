"""comun_n9b.py — piezas compartidas de subida_n9b: rutas, shas fijados, pista/juez/chequeo de la carrera (solo se LEEN)
apuntando a los carros de esta carpeta.

MISION: llegar a la AGI por este camino.
Shas = los de la replica 8121-8140 de APR (aprende_barrer): pista.py 9f47c65e438e0ff4 · juez.py 6a68f640a7832f12.
Lo unico que cambia es DE DONDE se cargan los carros (P.CARROS y RC.CARROS -> subida_n9b/carros). No se edita nada ajeno.
"""
import hashlib, json, os, sys

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
CARRERA = os.path.join(RAIZ, 'experimentos', 'carrera_escuderias')
CARROS_N9B = os.path.join(AQUI, 'carros')
SHAS = {os.path.join(CARRERA, 'pista.py'): '9f47c65e438e0ff4',
        os.path.join(CARRERA, 'juez.py'): '6a68f640a7832f12',
        os.path.join(CARRERA, 'revisa_carro.py'): '1c8a789f7427ab96',
        os.path.join(CARRERA, 'carros', 'APR.py'): '4402aa5142065c72',
        os.path.join(CARRERA, 'carros', 'FABRICA.py'): '2ebee3e99ea5a33a',
        os.path.join(RAIZ, 'experimentos', 'nivel09_cuerpo_nuevo_b2', 'organismo_f9c.py'): '9dd1fb91ecec35ae'}
BRAZOS = {'apr': 'APR', 'fab': 'FABRICA', 'plana': 'APR_LES_PLANA', 'cruz': 'APR_LES_CRUZ', 'mundo': 'APR_LES_MUNDO'}
LESIONES = ('plana', 'cruz', 'mundo')

if CARRERA not in sys.path: sys.path.insert(0, CARRERA)
if AQUI not in sys.path: sys.path.insert(0, AQUI)
import pista as P          # noqa: E402
import revisa_carro as RC  # noqa: E402
import juez as J           # noqa: E402
P.CARROS = CARROS_N9B
RC.CARROS = CARROS_N9B


def h16(p):
    return hashlib.sha256(open(p, 'rb').read()).hexdigest()[:16]


def verifica_shas():
    return [(os.path.relpath(p, RAIZ), h16(p), s, h16(p) == s) for p, s in SHAS.items()]


def verifica_construccion():
    """Los carros en disco son EXACTAMENTE lo que construye_n9b.py produce desde APR.py / FABRICA.py (shas fijados)."""
    import construye_n9b as C
    esperado, _ = C.construye(escribe=False)
    medido = {n: (h16(os.path.join(CARROS_N9B, n + '.py')) if os.path.exists(os.path.join(CARROS_N9B, n + '.py')) else None)
              for n in esperado}
    return esperado, medido, esperado == medido


def normaliza(x, etiqueta=None, a='APR'):
    """JSON canonico de una salida de pista.run; si etiqueta, renombra ese carro a `a` (para comparar ids)."""
    s = json.dumps(x, default=str, sort_keys=True)
    if etiqueta: s = s.replace(etiqueta, a)
    return s
