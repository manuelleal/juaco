"""CREADOR A — arnes de identidad de `organismo_v14_e015c10.py` contra el TRONCO CONGELADO `organismo/organismo_v14.py`.

`organismo_v14_e015c10` sólo cambia DOS VALORES POR DEFECTO (`eta_s` 0.015 -> 0.15, `clip_s` 3.0 -> 10.0). Ninguna
línea de lógica cambia, así que llamándolo con las constantes ORIGINALES explícitas debe dar EXACTAMENTE lo mismo
que el tronco, en todas las claves. Ocho escenarios x 2 semillas (mundo AB del tronco, inversión, patrón nuevo,
solapamientos, vía lenta apagada, sin puerta), un proceso, sin Pool.
Uso: python identidad_v14_e015c10.py [T]
"""
import sys, os, json
import numpy as np

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
sys.path[:0] = [AQUI, os.path.join(RAIZ, 'organismo')]
import organismo_v14 as TRONCO
import organismo_v14_e015c10 as NUEVO

ORIG = dict(eta_s=0.015, clip_s=3.0)   # las constantes del tronco, pasadas explicitas

ESCENARIOS = [
    ('AB (tronco, por defecto)', dict()),
    ('AB invertido en T/2', dict(invertir_en=15000)),
    ('AB + patron nuevo C', dict(nuevo='C', nuevo_en=15000)),
    ('AB solap_AB=3 (E2L)', dict(solap_AB=3)),
    ('AB sin plasticidad', dict(plast=False)),
    ('AB via lenta APAGADA', dict(eta_s=0.0)),
    ('AB sin puerta', dict(puerta=None)),
    ('AB sin division por signo', dict(div_signo=False)),
]


def N(x):
    return json.loads(json.dumps(x, default=str))


if __name__ == '__main__':
    T = int(sys.argv[1]) if len(sys.argv) > 1 else 30000
    ok = 0; total = 0; malos = []
    for etq, kw in ESCENARIOS:
        for seed in (1, 2):
            total += 1
            kwt = dict(ORIG); kwt.update(kw)          # el tronco: sus propios valores (explicitos o los de kw)
            a = TRONCO.run(seed, T=T, **kwt)
            b = NUEVO.run(seed, T=T, **kwt)           # el nuevo: MISMAS constantes explicitas -> debe ser identico
            dif = [k for k in a if N(a[k]) != N(b[k])]
            ok += (not dif)
            print(f'  {etq:>28} s{seed} T={T}: {"IDENTICO" if not dif else "DIFIEREN " + str(dif)} ({len(a)} claves)')
            if dif: malos.append((etq, seed, dif))
    # y una comprobacion de que las constantes NUEVAS sí cambian algo (si no, el parche no hizo nada)
    c = NUEVO.run(1, T=30000)                          # por defecto: eta_s=0.15, clip_s=10
    d = TRONCO.run(1, T=30000)
    distinto = [k for k in d if N(d[k]) != N(c[k])]
    print(f'\nIDENTIDAD con las constantes ORIGINALES: {ok}/{total}' + ('' if ok == total else f'  FALLAN: {malos}'))
    print(f'Con las constantes NUEVAS por defecto, difiere del tronco en {len(distinto)} claves '
          f'{"(OK: el parche actua)" if distinto else "*** el parche NO hace nada"}')
