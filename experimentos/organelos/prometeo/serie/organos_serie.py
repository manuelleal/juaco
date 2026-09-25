# EXPLORATORIO, no es dato (instrumento de la serie)
"""organos_serie.py — que ORGANOS ARMADOS lleva una cinta (lo usan corre_serie.py y motor_serie.py). Opus, 25-sep-2026.
MISION: llegar a la AGI por este camino. ERR-144: sale de corre_serie.py para que el motor mida el suministro DE NOVO con la MISMA definicion."""
import os, sys
_AQ = os.path.dirname(os.path.abspath(__file__)); _PR = os.path.dirname(_AQ)
for _d in (_PR, os.path.join(os.path.dirname(_PR), 'codigo')):
    if _d not in sys.path: sys.path.append(_d)
import codigo_prometeo as CP
import gramatica_def as GD

SEN = ('sesgo', 'reserva', 'la_otra', 'ventana', 'edad', 'hijos')
DEC = ('boca', 'patas', 'parto')
_G0 = [1.0] * 18; _LO = [1e-9] * 18; _HI = [1e9] * 18; _EN = [0] * 18   # solo para LEER los organos de una cinta (las perillas no importan)
_CACHE = {}


def claves(c):
    """-> (funcionales, inertes): conjuntos de claves de ORGANOS ARMADOS (ausentes en la cinta inicial). FUNCIONAL = puede cambiar una decision:
    cable a boca/patas con peso != 0; cable a parto con algun peso < 0 (las 6 senales son >= 0: si todos los pesos son >= 0 nunca veta);
    slot de transmision con cuando != nunca y distinto de filtra0 (1,3,0,0). INERTE = cable de parto sin peso negativo, slot con cuando = nunca.
    La instruccion HGT NO es un organo (es el mecanismo de variacion; se reporta aparte)."""
    W, h, gram = CP.organos(tuple(tuple(x) for x in c), _G0, _LO, _HI, _EN)
    fun = set(); ine = set()
    if W is not None:
        for d in range(3):
            inerte = d == 2 and all(W[2][q] >= 0 for q in range(6))
            for q in range(6):
                if W[d][q] != 0: (ine if inerte else fun).add(f"{SEN[q]}->{DEC[d]}{'+' if W[d][q] > 0 else '-'}")
    for s in gram:
        if tuple(s[:4]) == (1, 3, 0, 0): continue
        k = f"ORG {GD.CUANDO[s[0]]}/{GD.QUE[s[1]]}/{GD.QUIEN[s[2]]}/{GD.COMO[s[3]]}"
        (ine if s[0] == 0 else fun).add(k)
    return fun, ine, h is not None



def armados(c):
    """Conjunto de TODAS las claves de organos armados (funcionales + inertes) de una cinta (tupla de tuplas), con cache."""
    k = _CACHE.get(c)
    if k is None:
        f, i, h = claves(c); k = frozenset(f) | frozenset('~' + z for z in i)
        if len(_CACHE) < 200000: _CACHE[c] = k
    return k
