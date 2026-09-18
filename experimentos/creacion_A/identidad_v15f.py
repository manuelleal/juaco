"""CREADOR A — arnes de identidad del candidato v15f (R crudo + sobrescritura + relevo a la lineal). Un proceso, sin Pool.

I1  `organismo_v15f(memoria_pares=None)` == `organismo/organismo_v14.py` (TRONCO v14.1) en TODAS las claves de v14.1.
    12 escenarios x 2 semillas = 24 comprobaciones.
I2  El `rng` NO se consume con la perilla apagada (T = 120 000, 2 semillas).
I3  `organismo_v15gf(memoria_pares=None)` == `organismo/organismo_v14g.py` con los kwargs EXACTOS de la entrada
    'organismo_v14' de bateria_generaliza (regla 14 / ERR-38), 3 reglas x 2 semillas = 6.
I4  NO es identidad: la perilla ENCENDIDA corre sin excepcion con `puerta_pat=5` y muestra la propiedad que v15f reclama:
    la via lenta lee R CRUDO exacto (±1 / −3) en cada patron cuya combinacion conoce la celda ganadora.
Uso: python identidad_v15f.py [T]
"""
import sys, os, json
import numpy as np

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
sys.path[:0] = [os.path.join(RAIZ, 'organismo'), AQUI]   # organismo/ PRIMERO (ERR-28)
import organismo_v14 as V14
import organismo_v15f as V15F
import organismo_v14g as V14G
import organismo_v15gf as V15GF

NUEV = {'memoria_pares', 'mem_alfa', 'mem_ganadora', 'mem_tabla', 'mem_vistas', 'mem_cobertura', 'mem_err_tabla',
        'W_tabla', 'mem_fam', 'mem_ev'}
KW14 = dict(eta_s=0.15, clip_s=10.0, puerta=3, mask_rel=2, del_s=0.25, del_c=0.25, ema_c=0.05, puerta_pat=5, pat_shuf=0, pat_min=1)

ESC = [('AB por defecto', dict()), ('AB invertido', dict(invertir_en=15000)),
       ('AB + patron nuevo C', dict(nuevo='C', nuevo_en=15000)), ('AB solap_AB=3 (E2L)', dict(solap_AB=3)),
       ('AB sin plasticidad', dict(plast=False)), ('AB via lenta apagada', dict(eta_s=0.0)),
       ('AB sin puerta', dict(puerta=None)), ('AB sin division por signo', dict(div_signo=False)),
       ('AB sin hija dispersa', dict(mask_rel=0)), ('AB sin puerta por codigo', dict(puerta_pat=0)),
       ('AB las dos perillas v14 off', dict(mask_rel=0, puerta_pat=0)),
       ('AB constantes v13 (eta_s .015, clip 3)', dict(eta_s=0.015, clip_s=3.0))]

ESCG = [('regla/px0, kwargs del tronco', dict(mundo='regla', regla='px0', **KW14)),
        ('regla/xor01, kwargs del tronco', dict(mundo='regla', regla='xor01', **KW14)),
        ('regla/azar, kwargs del tronco', dict(mundo='regla', regla='azar', **KW14))]


def N(x):
    return json.loads(json.dumps(x, default=str))


def comp(a, b):
    return ([k for k in a if k in b and N(a[k]) != N(b[k])] + [k for k in a if k not in b]
            + [k for k in b if k not in a and k not in NUEV])


if __name__ == '__main__':
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    T = int(sys.argv[1]) if len(sys.argv) > 1 else 30000
    ok = tot = 0
    print(f'--- I1: organismo_v15f(memoria_pares=None) == organismo_v14 (TRONCO v14.1), T={T} ---', flush=True)
    for etq, kw in ESC:
        for s in (1, 2):
            tot += 1
            d = comp(V14.run(s, T=T, **kw), V15F.run(s, T=T, memoria_pares=None, **kw))
            ok += (not d)
            print(f'  {etq:>40} s{s}: {"IDENTICO" if not d else "DIFIERE " + str(d)}', flush=True)
    print('\n--- I2: el rng NO se consume con la perilla apagada (T=120000) ---', flush=True)
    for s in (1, 2):
        tot += 1
        d = comp(V14.run(s, T=120000), V15F.run(s, T=120000, memoria_pares=None))
        ok += (not d)
        print(f'  T=120000 s{s}: {"IDENTICO" if not d else "DIFIERE " + str(d)}', flush=True)
    print(f'\n--- I3: organismo_v15gf(memoria_pares=None) == organismo_v14g (kwargs exactos del tronco), T={T} ---', flush=True)
    for etq, kw in ESCG:
        for s in (1, 2):
            tot += 1
            d = comp(V14G.run(s, T=T, **kw), V15GF.run(s, T=T, memoria_pares=None, **kw))
            ok += (not d)
            print(f'  {etq:>40} s{s}: {"IDENTICO" if not d else "DIFIERE " + str(d)}', flush=True)
    print(f'\nIDENTIDAD (I1+I2+I3): {ok}/{tot}', flush=True)

    print('\n--- I4 (NO es identidad): la perilla ENCENDIDA corre con puerta_pat=5 y la via lenta lee R CRUDO exacto ---', flush=True)
    for s in (1, 2):
        r = V15F.run(s, T=min(T, 20000), memoria_pares='relevo')
        print(f'  s{s} T={min(T,20000)}: W {r["W"]}  W_lenta(lineal) {r["W_lenta"]}  W_tabla(R crudo, None=no vista) {r["W_tabla"]}  '
              f'ganadora {r["mem_ganadora"]}  familiar {r["mem_fam"]}  mordidas B {r["mord"]["B"]}  splits {r["splits"]}', flush=True)
    print('  Lo que se busca: sin excepcion; W_tabla = +1.0 en A y -3.0 en B (R crudo); la lineal sigue aprendiendo aparte.')
