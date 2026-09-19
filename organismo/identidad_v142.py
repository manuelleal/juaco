"""ARNES DE IDENTIDAD DEL TRONCO v14.2 (= v14.1 + B-5 desambiguar). UN proceso, sin Pool (regla 3 de EQUIPO.md).

v14.2 no cambia ningun numero del tronco: lo unico que cambia respecto de v14.1 es el defecto de la perilla
`desambiguar` (0 -> 1). Este arnes lo demuestra por los dos lados, bit a bit:

I1  organismo_v142(desambiguar=0) == organismo_v14 (v14.1, CONGELADO) en TODAS las claves de v14:
    12 escenarios x 2 semillas (T = 30000 por defecto).
I2  el rng NO se consume con la perilla apagada: T = 120000, 2 semillas (un numero de mas y todo diverge).
I3  organismo_v142() (la perilla ENCENDIDA por defecto) == experimentos/creacion_B/organismo_v14_codigo_on.py
    (2f7794d92e68cc89), el modulo que ya paso el bloque B-5 y su replica: 12 escenarios x 2 semillas.
    Es lo que hace que la evidencia de B-5 (examen 8/8, generalizacion 40/40, alias 18/18) valga para v14.2
    sin volver a correrla: el archivo nuevo es ese archivo con otro nombre y el defecto movido.
I4  el instrumento de mundo de regla: organismo_v142g(desambiguar=0) == organismo_v14g y organismo_v142g()
    == organismo_v14g_codigo_on: 3 reglas x 2 semillas por lado.
I5  PREDICCION (no exigencia): en los mundos del tronco R in (+1,-3), asi que la regla de B-5 es INERTE POR
    CONSTRUCCION: organismo_v142() == organismo_v14 en los 12 escenarios y v142g() == v14g en las 3 reglas.
    Si esto falla, R == 0 ocurre donde no lo esperabamos y el coste 0 % del tronco deja de ser identidad.

VEREDICTO: identidad 3/3 = I1, I2 e I3 completos (I4 se exige tambien; I5 se reporta).
Uso: python identidad_v142.py [T]        (desde organismo/)
"""
import hashlib, json, os, sys, time

sys.stdout.reconfigure(encoding='utf-8', errors='replace')
AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(AQUI)
CREB = os.path.join(RAIZ, 'experimentos', 'creacion_B')
sys.path[:0] = [AQUI, CREB]   # organismo/ PRIMERO (ERR-28)

import organismo_v14 as V14
import organismo_v142 as V142
import organismo_v14g as V14G
import organismo_v142g as V142G
import organismo_v14_codigo_on as VON
import organismo_v14g_codigo_on as VGON

NUEV = {'desambiguar', 'des_splits', 'des_t'}   # claves nuevas de solo lectura (siempre presentes en v14.2)

ESC = [('AB por defecto', dict()), ('AB invertido', dict(invertir_en=15000)),
       ('AB + patron nuevo C', dict(nuevo='C', nuevo_en=15000)), ('AB solap_AB=3 (E2L)', dict(solap_AB=3)),
       ('AB sin plasticidad', dict(plast=False)), ('AB via lenta apagada', dict(eta_s=0.0)),
       ('AB sin puerta', dict(puerta=None)), ('AB sin division por signo', dict(div_signo=False)),
       ('AB sin hija dispersa', dict(mask_rel=0)), ('AB sin puerta por codigo', dict(puerta_pat=0)),
       ('AB las dos perillas v14 off', dict(mask_rel=0, puerta_pat=0)),
       ('AB D comida solap_B=2 (E2K)', dict(nuevo='D', nuevo_val='comida', solap_B=2, nuevo_en=15000))]
KWG = dict(eta_s=0.15, clip_s=10.0, puerta=3, mask_rel=2, puerta_pat=5, pat_min=1)   # los kwargs del tronco
ESCG = [('regla/px0', dict(mundo='regla', regla='px0', **KWG)),
        ('regla/xor01', dict(mundo='regla', regla='xor01', **KWG)),
        ('regla/azar', dict(mundo='regla', regla='azar', **KWG))]


def h16(p):
    return hashlib.sha256(open(p, 'rb').read()).hexdigest()[:16]


def N(x):
    return json.loads(json.dumps(x, default=str))


def comp(a, b):
    """claves de `a` que difieren o faltan en `b`; y claves nuevas de `b` fuera de NUEV."""
    return ([k for k in a if k in b and N(a[k]) != N(b[k])] + [k for k in a if k not in b]
            + [k for k in b if k not in a and k not in NUEV])


if __name__ == '__main__':
    T = int(sys.argv[1]) if len(sys.argv) > 1 else 30000
    t0 = time.time()
    for nom, p in [('organismo_v14 (v14.1)', os.path.join(AQUI, 'organismo_v14.py')),
                   ('organismo_v14g', os.path.join(AQUI, 'organismo_v14g.py')),
                   ('organismo_v142 (TRONCO)', os.path.join(AQUI, 'organismo_v142.py')),
                   ('organismo_v142g', os.path.join(AQUI, 'organismo_v142g.py')),
                   ('organismo_v14_codigo_on', os.path.join(CREB, 'organismo_v14_codigo_on.py')),
                   ('organismo_v14g_codigo_on', os.path.join(CREB, 'organismo_v14g_codigo_on.py')),
                   ('este arnes', os.path.abspath(__file__))]:
        print(f'  sha {nom:26s} {h16(p)}')
    print()
    ok1 = tot1 = ok2 = tot2 = ok3 = tot3 = ok4 = tot4 = 0
    ok5 = tot5 = 0

    print(f"--- I1: organismo_v142(desambiguar=0) == organismo_v14 (v14.1), T={T}"
          f" | I3: organismo_v142() == organismo_v14_codigo_on() | I5: v142() == v14 (inercia predicha) ---")
    for etq, kw in ESC:
        for s in (1, 2):
            a = V14.run(s, T=T, **kw)
            on = VON.run(s, T=T, **kw)
            v0 = V142.run(s, T=T, desambiguar=0, **kw)
            v1 = V142.run(s, T=T, **kw)                    # la perilla ENCENDIDA por defecto
            d1 = comp(a, v0); tot1 += 1; ok1 += (not d1)
            d3 = comp(on, v1); tot3 += 1; ok3 += (not d3)
            d5 = comp(a, v1); tot5 += 1; ok5 += (not d5)
            print(f'  [{time.time()-t0:5.0f}s] {etq:>30} s{s}: I1 {"IDENTICO" if not d1 else "DIFIERE " + str(d1)}'
                  f' | I3 {"IDENTICO" if not d3 else "DIFIERE " + str(d3)}'
                  f' | I5 {"inerte" if not d5 else "ACTUA " + str(d5)}')

    print('\n--- I2: el rng NO se consume con la perilla apagada (T=120000) ---')
    for s in (1, 2):
        d = comp(V14.run(s, T=120000), V142.run(s, T=120000, desambiguar=0)); tot2 += 1; ok2 += (not d)
        print(f'  [{time.time()-t0:5.0f}s] T=120000 s{s}: {"IDENTICO" if not d else "DIFIERE " + str(d)}')

    print(f'\n--- I4: organismo_v142g(0) == organismo_v14g y v142g() == organismo_v14g_codigo_on, T={T}; I5 en regla ---')
    for etq, kw in ESCG:
        for s in (1, 2):
            a = V14G.run(s, T=T, **kw)
            on = VGON.run(s, T=T, **kw)
            g0 = V142G.run(s, T=T, desambiguar=0, **kw)
            g1 = V142G.run(s, T=T, **kw)
            d0 = comp(a, g0); tot4 += 1; ok4 += (not d0)
            d1 = comp(on, g1); tot4 += 1; ok4 += (not d1)
            d5 = comp(a, g1); tot5 += 1; ok5 += (not d5)
            print(f'  [{time.time()-t0:5.0f}s] {etq:>30} s{s}: off {"IDENTICO" if not d0 else "DIFIERE " + str(d0)}'
                  f' | on==codigo_on {"IDENTICO" if not d1 else "DIFIERE " + str(d1)}'
                  f' | I5 {"inerte" if not d5 else "ACTUA " + str(d5)}')

    B = {'I1 v142(0) == v14 (v14.1)': (ok1, tot1), 'I2 rng no consumido': (ok2, tot2),
         'I3 v142() == organismo_v14_codigo_on': (ok3, tot3), 'I4 mundo de regla': (ok4, tot4)}
    print()
    for k, (o, t) in B.items():
        print(f'  {"PASA" if o == t else "FALLA":5s} {k}: {o}/{t}')
    tres = sum(1 for k in ('I1 v142(0) == v14 (v14.1)', 'I2 rng no consumido', 'I3 v142() == organismo_v14_codigo_on')
               if B[k][0] == B[k][1])
    okt = sum(o for o, _ in B.values()); tott = sum(t for _, t in B.values())
    print(f'\nIDENTIDAD exigida: {okt}/{tott}   (bloques {tres}/3 + I4)')
    print(f'INERCIA predicha en los mundos del tronco (I5, perilla ON): {ok5}/{tot5}')
    todo = okt == tott
    print(f'\nVEREDICTO identidad_v142: {"PASA" if todo else "NO PASA"}  (identidad {tres}/3; I4 {ok4}/{tot4}; I5 {ok5}/{tot5})')
    sys.exit(0 if todo else 1)
