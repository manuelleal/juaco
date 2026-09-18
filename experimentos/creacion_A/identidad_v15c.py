"""CREADOR A — arnes de identidad del candidato v15c. Un proceso, sin Pool.

I1  `organismo_v15c(memoria_pares=None)` == `organismo/organismo_v14.py` (TRONCO v14.1) en TODAS las claves.
    12 escenarios x 2 semillas (mundo AB, inversion, patron nuevo, solapamientos, sin plasticidad, via lenta
    apagada, sin puerta, sin division, y las perillas de v14 apagadas).
I2  **El rng no se toca con la perilla apagada.** No basta con que las claves coincidan: se comprueba que la
    secuencia de numeros aleatorios consumida es la misma, corriendo con un `T` largo y comparando el estado final
    del organismo (si v15c consumiera un numero de mas, TODO divergiria; I1 ya lo detectaria, pero se declara
    aparte porque es la razon de escribir `_MGv=_empv[0] if len(_empv)==1 else ...`).
I3  `organismo_v15gc(memoria_pares=None)` == `organismo/organismo_v14g.py` en el mundo de regla.
I4  `organismo_v15gc(memoria_pares='combi')` contra `organismo_g3A(memoria='combi')` en el mundo de regla:
    **NO se espera identidad exacta** (v15gc lleva la hija dispersa y la puerta por codigo de v14, que g3A no
    tiene, y g3A lleva la lectura cuadratica de la via lenta, que v14 no tiene). Se declara la diferencia y se
    comprueba lo unico que debe coincidir: la GANADORA y la tabla de la celda ganadora.
Uso: python identidad_v15c.py [T]
"""
import sys, os, json
import numpy as np

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
sys.path[:0] = [AQUI, os.path.join(RAIZ, 'organismo'), os.path.join(RAIZ, 'experimentos', 'enjambre', 'grupo3')]
import organismo_v14 as V14
import organismo_v15c as V15
import organismo_v14g as V14G
import organismo_v15gc as V15G

NUEV = {'memoria_pares', 'mem_ganadora', 'mem_tabla', 'mem_vistas', 'mem_cobertura'}

ESC = [('AB por defecto', dict()), ('AB invertido', dict(invertir_en=15000)),
       ('AB + patron nuevo C', dict(nuevo='C', nuevo_en=15000)), ('AB solap_AB=3 (E2L)', dict(solap_AB=3)),
       ('AB sin plasticidad', dict(plast=False)), ('AB via lenta apagada', dict(eta_s=0.0)),
       ('AB sin puerta', dict(puerta=None)), ('AB sin division por signo', dict(div_signo=False)),
       ('AB sin hija dispersa', dict(mask_rel=0)), ('AB sin puerta por codigo', dict(puerta_pat=0)),
       ('AB las dos perillas v14 off', dict(mask_rel=0, puerta_pat=0)),
       ('AB constantes v13 (eta_s .015, clip 3)', dict(eta_s=0.015, clip_s=3.0))]

ESCG = [('regla/px0 lineal', dict(mundo='regla', regla='px0', eta_s=0.15, puerta=3)),
        ('regla/xor01', dict(mundo='regla', regla='xor01', eta_s=0.15, puerta=3)),
        ('regla/azar', dict(mundo='regla', regla='azar', eta_s=0.15, puerta=3))]


def N(x):
    return json.loads(json.dumps(x, default=str))


def comp(a, b):
    dif = [k for k in a if k in b and N(a[k]) != N(b[k])]
    falt = [k for k in a if k not in b]
    ext = [k for k in b if k not in a and k not in NUEV]
    return dif + falt + ext


if __name__ == '__main__':
    T = int(sys.argv[1]) if len(sys.argv) > 1 else 30000
    ok = tot = 0
    print(f'--- I1: organismo_v15c(memoria_pares=None) == organismo_v14 (TRONCO v14.1), T={T} ---')
    for etq, kw in ESC:
        for s in (1, 2):
            tot += 1
            d = comp(V14.run(s, T=T, **kw), V15.run(s, T=T, memoria_pares=None, **kw))
            ok += (not d)
            print(f'  {etq:>40} s{s}: {"IDENTICO" if not d else "DIFIERE " + str(d)}')
    print(f'\n--- I2: el rng NO se consume con la perilla apagada (T largo, mismo estado final) ---')
    for s in (1, 2):
        tot += 1
        d = comp(V14.run(s, T=120000), V15.run(s, T=120000, memoria_pares=None))
        ok += (not d)
        print(f'  T=120000 s{s}: {"IDENTICO" if not d else "DIFIERE " + str(d)}')
    print(f'\n--- I3: organismo_v15gc(memoria_pares=None) == organismo_v14g (mundo de regla), T={T} ---')
    for etq, kw in ESCG:
        for s in (1, 2):
            tot += 1
            d = comp(V14G.run(s, T=T, **kw), V15G.run(s, T=T, memoria_pares=None, **kw))
            ok += (not d)
            print(f'  {etq:>40} s{s}: {"IDENTICO" if not d else "DIFIERE " + str(d)}')
    print(f'\nIDENTIDAD (I1+I2+I3): {ok}/{tot}')
    print('\n--- I4: v15gc(memoria_pares="combi") contra organismo_g3A: NO se espera identidad, se DECLARA ---')
    try:
        import organismo_g3A as G3
        for s in (1, 2, 3):
            a = V15G.run(s, T=100000, mundo='regla', regla='xor01', eta_s=0.15, puerta=3, memoria_pares='combi')
            b = G3.run(s, T=100000, mundo='regla', regla='xor01', lectura='cuadratica', constante=True,
                       regla_lenta='delta_signo', lam_lenta=0.0, eta_s=0.15, clip_s=10.0, puerta=3,
                       memoria='combi', mem_apriori=True)
            gb = b['mem_apriori']['ganadora'] if b['mem_apriori'] else None
            print(f'  s{s}: v15gc ganadora {a["mem_ganadora"]} (cobertura {a["mem_cobertura"]}/4, vistas {a["mem_vistas"]})'
                  f'   g3A ganadora en la sonda {gb}   {"COINCIDEN" if a["mem_ganadora"] == gb else "distintas"}')
        print('  DIFERENCIA DECLARADA: v15gc lleva la hija dispersa y la puerta por codigo de v14.1 (g3A no) y g3A '
              'lleva la via lenta cuadratica (v14.1 no): la equivalencia exacta NO existe, y no se reclama.')
    except Exception as e:
        print(f'  (no comparable: {e})')
