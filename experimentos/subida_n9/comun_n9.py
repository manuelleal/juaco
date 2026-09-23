"""comun_n9.py — piezas compartidas del bloque "el modelo de si es causal" (subida del nivel 9): rutas, shas fijados,
carga de la pista y del juez de la carrera (solo se LEEN; nada se edita) apuntando a los carros de esta carpeta.

MISION: llegar a la AGI por este camino.

La pista y el juez son los de la RONDA 2 (ENMIENDA 5 y 6), con los shas con los que O3 gano y se replico:
  pista.py 9f47c65e438e0ff4 · juez.py 6a68f640a7832f12 · organismo_f9c.py 9dd1fb91ecec35ae (identidad corta del juez).
Lo unico que cambia es DE DONDE se cargan los carros: P.CARROS y RC.CARROS pasan a experimentos/subida_n9/carros
(carga por ruta, igual que la pista). No se toca ningun archivo de carrera_escuderias.
"""
import hashlib, json, os, sys

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
CARRERA = os.path.join(RAIZ, 'experimentos', 'carrera_escuderias')
CARROS_N9 = os.path.join(AQUI, 'carros')
SHAS = {os.path.join(CARRERA, 'pista.py'): '9f47c65e438e0ff4',
        os.path.join(CARRERA, 'juez.py'): '6a68f640a7832f12',
        os.path.join(CARRERA, 'revisa_carro.py'): '1c8a789f7427ab96',
        os.path.join(CARRERA, 'carros', 'O3.py'): '0442c2884fcb0e11',
        os.path.join(RAIZ, 'experimentos', 'nivel09_cuerpo_nuevo_b2', 'organismo_f9c.py'): '9dd1fb91ecec35ae'}
BRAZOS = ('O3', 'O3_LES_SI', 'O3_TERM_CIEGO', 'CTRL_O3_SINTERM')   # los cuatro brazos de la serie (PREREGISTRO_n9.md)
ARNES = ('O3_LES_OFF', 'O3_LES_COLA')   # solo arnes: OFF (identidad) y L-COLA (DESCARTADA por el chequeo (M); no corre)

if CARRERA not in sys.path: sys.path.insert(0, CARRERA)
if AQUI not in sys.path: sys.path.insert(0, AQUI)
import pista as P          # noqa: E402
import revisa_carro as RC  # noqa: E402
import juez as J           # noqa: E402
P.CARROS = CARROS_N9
RC.CARROS = CARROS_N9


def h16(p):
    return hashlib.sha256(open(p, 'rb').read()).hexdigest()[:16]


def verifica_shas():
    """(ruta, sha medido, sha fijado, ok) de los originales leidos."""
    return [(os.path.relpath(p, RAIZ), h16(p), s, h16(p) == s) for p, s in SHAS.items()]


def verifica_construccion():
    """Los carros en disco son EXACTAMENTE lo que construye_n9.py produce desde O3.py (sha fijado)."""
    import construye_n9 as C
    esperado, _ = C.construye(escribe=False)
    medido = {n: h16(os.path.join(CARROS_N9, n + '.py')) for n in esperado}
    return esperado, medido, esperado == medido


def normaliza(x, etiqueta=None):
    """JSON canonico de una salida de pista.run; si etiqueta, renombra ese carro a 'O3' (para comparar ids)."""
    s = json.dumps(x, default=str, sort_keys=True)
    if etiqueta: s = s.replace(etiqueta, 'O3')
    return s
