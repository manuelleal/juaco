"""carros_n10c.py — SUBIDA_N10C: "la familia pasa SOLO LO QUE IMPORTA" (PREREGISTRO_n10c.md).

MISION: llegar a la AGI por este camino.

Variantes de los carros de subida_n10b (carros/FAMB_*.py, sha fijado en corre_n10c.SHAS; aqui solo se CARGAN y se SUBCLASEAN,
no se copian ni se editan). La unica pieza nueva es un FILTRO en el parto del hijo: de la tabla recibida se quitan las entradas
con R == 0 (lo NEUTRO: la letra no toca esa necesidad). Memoria nueva: CERO. Constantes nuevas: CERO.
  RES_SIN0  = FAMB_RES con el filtro en nace()                 (candidato)
  BAR_SIN0  = FAMB_BAR con el filtro en nace() ANTES de su permutacion (mismas claves y multiset de R que RES_SIN0, R barajadas)
  ORA_SIN0  = FAMB_ORACULO con su tabla verdadera sin las 4 entradas neutras (referencia; no es techo)
Con filtro=False cada variante es su carro base BIT A BIT (arnes identidad_n10c.py, bloque I).
"""
import os, sys, types

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
sys.path.insert(0, os.path.join(RAIZ, 'experimentos', 'subida_n10b'))
import corre_n10b as CN

ULTIMO = {}   # nombre -> modulo BASE cargado en la ultima llamada (su _TELE es la telemetria de esa corrida)


CARROS_N10B = os.path.join(RAIZ, 'experimentos', 'subida_n10b', 'carros')


def base(et):
    """Modulo FAMB_<et> de subida_n10b, cargado FRESCO en cada llamada y POR RUTA, con el mismo codigo que corre_n10b.carga
    (NO se llama a corre_n10b.carga: corre_n10c la reasigna a modulo() y eso seria una recursion). La telemetria _TELE es una
    lista de modulo y no debe acumularse entre corridas."""
    import importlib.util
    p = os.path.join(CARROS_N10B, f'FAMB_{et}.py')
    spec = importlib.util.spec_from_file_location(f'carro_FAMB_{et}', p)
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m


def sin_neutras(tabla):
    """La tabla sin las entradas con R == 0 (las R son categoricas: +1, 0, -3)."""
    return [e for e in tabla if float(e[1]) != 0.0]


def _hijo_filtra(Base, filtro):
    class Carro(Base.Carro):
        def nace(self, info):
            if filtro:
                m = info.get('memoria')
                if m:
                    info = dict(info, memoria=sin_neutras(m))
            return super().nace(info)
    return Carro


def _oraculo_sin0(B, filtro):
    class Carro(B.Carro):
        def __init__(self, ctx):
            super().__init__(ctx)
            if filtro:
                self._ORA = sin_neutras(self._ORA)
    return Carro


def modulo(nombre, filtro=True):
    """Modulo-carro (expone crea(ctx)) para pista2.run. nombre en NADA, RES, BAR, ORACULO, RES_SIN0, BAR_SIN0, ORA_SIN0."""
    if nombre in ('NADA', 'RES', 'BAR', 'ORACULO', 'RES1'):
        m = base(nombre); ULTIMO[nombre] = m
        return m
    if nombre == 'RES_SIN0': B = base('RES'); K = _hijo_filtra(B, filtro)
    elif nombre == 'BAR_SIN0': B = base('BAR'); K = _hijo_filtra(B, filtro)
    elif nombre == 'ORA_SIN0': B = base('ORACULO'); K = _oraculo_sin0(B, filtro)
    else: raise SystemExit(f'carros_n10c: carro desconocido {nombre!r}')
    ULTIMO[nombre] = B
    m = types.ModuleType(f'carro_FAMB_{nombre}')
    m.Carro = K
    m.crea = lambda ctx, _K=K: _K(ctx)
    return m
