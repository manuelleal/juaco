"""CREADOR A — arnes de identidad del candidato v15d. Un proceso, sin Pool.

I1  `organismo_v15d(memoria_pares=None)` == `organismo/organismo_v14.py` (TRONCO v14.1) en TODAS las claves.
    12 escenarios x 2 semillas.
I2  El `rng` NO se consume con la perilla apagada (T largo: si se consumiera un numero de mas, todo divergiria).
I3  `organismo_v15gd(memoria_pares=None)` == `organismo/organismo_v14g.py` (mundo de regla), 3 escenarios x 2.
I4  NO es identidad: los dos modos honestos ('suma', 'ruta') contra el SUSTITUTIVO de v15c ('combi') en `px0`,
    que es la regla lineal que v15c rompio (G1 0.500). Lo que se busca es que `suma` y `ruta` NO bajen px0
    respecto de la perilla apagada.
Uso: python identidad_v15d.py [T]
"""
import sys, os, json
import numpy as np

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
sys.path[:0] = [AQUI, os.path.join(RAIZ, 'organismo')]
import organismo_v14 as V14
import organismo_v15d as V15D
import organismo_v14g as V14G
import organismo_v15gd as V15GD

NUEV = {'memoria_pares', 'mem_ganadora', 'mem_tabla', 'mem_vistas', 'mem_cobertura',
        'mem_err_lineal', 'mem_err_tabla'}

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
    return ([k for k in a if k in b and N(a[k]) != N(b[k])] + [k for k in a if k not in b]
            + [k for k in b if k not in a and k not in NUEV])


def acc(r, mod, regla):
    vr = mod.split_regla(r['__seed'], regla)[3] if False else r['__vr']
    test = r['test']; W = r['W_apriori']
    f = [1.0 if W[k] > 0 else (0.5 if W[k] == 0 else 0.0) for k in test if vr[k] == 'comida']
    p = [1.0 if W[k] < 0 else (0.5 if W[k] == 0 else 0.0) for k in test if vr[k] == 'veneno']
    return 0.5 * float(np.mean(f)) + 0.5 * float(np.mean(p))


if __name__ == '__main__':
    T = int(sys.argv[1]) if len(sys.argv) > 1 else 30000
    ok = tot = 0
    print(f'--- I1: organismo_v15d(memoria_pares=None) == organismo_v14 (TRONCO v14.1), T={T} ---')
    for etq, kw in ESC:
        for s in (1, 2):
            tot += 1
            d = comp(V14.run(s, T=T, **kw), V15D.run(s, T=T, memoria_pares=None, **kw))
            ok += (not d)
            print(f'  {etq:>40} s{s}: {"IDENTICO" if not d else "DIFIERE " + str(d)}')
    print('\n--- I2: el rng NO se consume con la perilla apagada (T=120000) ---')
    for s in (1, 2):
        tot += 1
        d = comp(V14.run(s, T=120000), V15D.run(s, T=120000, memoria_pares=None))
        ok += (not d)
        print(f'  T=120000 s{s}: {"IDENTICO" if not d else "DIFIERE " + str(d)}')
    print(f'\n--- I3: organismo_v15gd(memoria_pares=None) == organismo_v14g, T={T} ---')
    for etq, kw in ESCG:
        for s in (1, 2):
            tot += 1
            d = comp(V14G.run(s, T=T, **kw), V15GD.run(s, T=T, memoria_pares=None, **kw))
            ok += (not d)
            print(f'  {etq:>40} s{s}: {"IDENTICO" if not d else "DIFIERE " + str(d)}')
    print(f'\nIDENTIDAD (I1+I2+I3): {ok}/{tot}')

    print('\n--- I4 (NO es identidad): los dos modos honestos contra el SUSTITUTIVO de v15c, en px0 ---')
    try:
        import organismo_v15gc as C
        for s in (1, 2, 3):
            fila = []
            for etq, mod, kw in (('v15c sustituye', C, dict(memoria_pares='combi')),
                                 ('v15d suma', V15GD, dict(memoria_pares='suma')),
                                 ('v15d ruta', V15GD, dict(memoria_pares='ruta')),
                                 ('v14.1 (off)', V15GD, dict(memoria_pares=None))):
                r = mod.run(s, T=100000, mundo='regla', regla='px0', eta_s=0.15, puerta=3, **kw)
                r['__vr'] = mod.split_regla(s, 'px0')[3]
                fila.append(f'{etq} {acc(r, mod, "px0"):.3f}')
            print(f'  s{s} px0: ' + ' | '.join(fila))
        print('  Lo que se busca: que `suma` y `ruta` NO bajen px0 respecto de la perilla apagada.')
    except Exception as e:
        print(f'  (no comparable: {e})')
