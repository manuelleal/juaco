"""carros/FRANK_ECO.py (CONSTRUIDO por experimentos/juaco_eco/construye_eco_frank.py; NO editar a mano). ECO v3, nube, 24-sep-2026.

El Frankenstein del PC (experimentos/frankenstein/organismo_frankenstein.py, sha baff124177d44e90; se IMPORTA sin tocarlo) con sus 7 perillas
leidas del GENOMA del cuerpo: la perilla k vale 1 si ctx['fabrica']['kw'][k] >= 1.0 (el gen de organo de motor_eco3; sin genoma, 0.9:
apagada). Con todo apagado es FABRICA bit a bit (arnes del Frankenstein, A1). En la pista v2 cada cuerpo es una instancia nueva: lo que
el Frankenstein guarda "del linaje" en el carro (la opcion TD del modelo, Wc de la memoria lenta) vale aqui solo durante una vida; la
herencia (la tabla del padre en el parto) si cruza entre cuerpos.
"""
import hashlib, os, sys

_D = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'frankenstein')
if _D not in sys.path: sys.path.insert(0, _D)
import organismo_frankenstein as OF

SHA_FRANK = 'baff124177d44e90'
if hashlib.sha256(open(OF.__file__, 'rb').read()).hexdigest()[:16] != SHA_FRANK:
    raise SystemExit(f"FRANK_ECO: organismo_frankenstein.py cambio (sha distinto de {SHA_FRANK})")
UMBRAL = 1.0
ORGANOS = ('b5', 'mapa', 'curiosidad', 'modelo', 'lenta', 'herencia', 'interruptor')
if tuple(OF.PERILLAS) != ORGANOS: raise SystemExit(f"FRANK_ECO: las perillas del Frankenstein cambiaron: {OF.PERILLAS}")


def perillas_de(kw):
    return dict((k, int(float(kw.get(k, 0.9)) >= UMBRAL)) for k in ORGANOS)


def crea(ctx):
    return OF.Carro(ctx, perillas_de(ctx['fabrica']['kw']))
