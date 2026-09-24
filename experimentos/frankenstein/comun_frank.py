"""comun_frank.py — piezas compartidas del FRANKENSTEIN (EXPLORATORIO, no es dato): rutas, shas fijados y brazos.

MISION: llegar a la AGI por este camino.
La pista y el juez de la carrera, y la pista v2 de generaciones, solo se LEEN (sha fijado). No se edita nada ajeno.
"""
import hashlib, importlib.util, os, sys, types

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
CARRERA = os.path.join(RAIZ, 'experimentos', 'carrera_escuderias')
GEN = os.path.join(RAIZ, 'experimentos', 'generaciones')
N10B = os.path.join(RAIZ, 'experimentos', 'subida_n10b')
FRANK = os.path.join(AQUI, 'organismo_frankenstein.py')
SHAS = {os.path.join(CARRERA, 'pista.py'): '9f47c65e438e0ff4',
        os.path.join(CARRERA, 'juez.py'): '6a68f640a7832f12',
        os.path.join(CARRERA, 'revisa_carro.py'): '1c8a789f7427ab96',
        os.path.join(CARRERA, 'carros', 'FABRICA.py'): '2ebee3e99ea5a33a',
        os.path.join(CARRERA, 'carros', 'APR.py'): '4402aa5142065c72',
        os.path.join(CARRERA, 'carros', 'O1.py'): '99436afa2715f028',
        os.path.join(GEN, 'pista2.py'): '4d2bee16e7961261',
        os.path.join(GEN, 'motor_convive.py'): 'd10cb9021f5d0f41',
        os.path.join(GEN, 'corre_convive.py'): 'e6dadfdad9c379cd',
        os.path.join(N10B, 'carros', 'FAMB_RES.py'): '2addb7ca5b9d031d',
        os.path.join(RAIZ, 'experimentos', 'nivel09_cuerpo_nuevo_b2', 'organismo_f9c.py'): '9dd1fb91ecec35ae',
        os.path.join(RAIZ, 'organismo', 'organismo_v142.py'): '17528d767fcebaf6'}

for _d in (CARRERA, GEN, AQUI):
    if _d not in sys.path: sys.path.insert(0, _d)


def h16(p):
    return hashlib.sha256(open(p, 'rb').read()).hexdigest()[:16]


def verifica_shas():
    return [(os.path.relpath(p, RAIZ), h16(p), s, h16(p) == s) for p, s in SHAS.items()]


def carga_mod(nombre, ruta):
    spec = importlib.util.spec_from_file_location(nombre, ruta); m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m); return m


_M = [None]


def frank():
    if _M[0] is None: _M[0] = carga_mod('organismo_frankenstein', FRANK)
    return _M[0]


def perillas_de(brazo):
    """TODO = todo encendido (b5 + 6 organos) · OFF = todo apagado (== FABRICA) · V142 = solo b5 · SIN_<ORGANO> = TODO menos uno ·
    SOLO_<ORGANO> = solo ese organo (sin b5)."""
    M = frank()
    if brazo == 'TODO': return dict(M.TODO)
    if brazo == 'OFF': return {}
    if brazo == 'V142': return dict(b5=1)
    if brazo.startswith('SIN_') and brazo[4:].lower() in M.ORGANOS:
        p = dict(M.TODO); p[brazo[4:].lower()] = 0; return p
    if brazo.startswith('SOLO_') and brazo[5:].lower() in M.ORGANOS:
        return {brazo[5:].lower(): 1}
    raise SystemExit(f"brazo desconocido: {brazo}")


def brazos_validos():
    M = frank()
    return (['TODO', 'OFF', 'V142'] + ['SIN_' + o.upper() for o in M.ORGANOS] + ['SOLO_' + o.upper() for o in M.ORGANOS]
            + ['O1', 'FABRICA', 'APR'])


def carro(brazo, etiqueta=None):
    """(etiqueta, modulo con crea) para pista.run / pista2.run. O1/FABRICA/APR: los de la carrera, sin tocar."""
    if brazo in ('O1', 'FABRICA', 'APR'):
        return (etiqueta or brazo, carga_mod(f'carro_{brazo}', os.path.join(CARRERA, 'carros', brazo + '.py')))
    pk = perillas_de(brazo); M = frank()
    return (etiqueta or brazo, types.SimpleNamespace(crea=lambda ctx, pk=pk: M.crea(ctx, pk)))
