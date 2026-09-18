"""Arnes de identidad de organismo_g4 (grupo4/M4) contra experimentos/creacion_A/organismo_v13q5.py (fae9c32b146fdbb4).

Con tabla_g=None (por defecto), organismo_g4.run debe reproducir BIT A BIT todas las claves ORIGINALES de
organismo_v13q5.run (se compara por subconjunto de claves porque g4 agrega claves de reporte nuevas -- el mismo
patron que construye_v13q5.py uso al agregar `lab`/`lenta_eventos` sobre v13q4; ver identidad_v13q5_rapido.py).

>= 9 casos: xor01/px0/azar x 3 semillas, T=30000, todas las claves originales. Se corre el arnes y se reporta n/n
ANTES de mirar ningun numero de mini_g4.py (regla EQUIPO.md #2). Sin Pool. Un proceso.
Uso: python identidad_g4.py
"""
import inspect, json, os, sys, time

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(AQUI)))
sys.path[:0] = [os.path.join(RAIZ, 'organismo'), os.path.join(RAIZ, 'experimentos', 'creacion_A'), AQUI]  # ERR-28: organismo/ PRIMERO

import organismo_v13q5 as LENTO   # el original, fae9c32b146fdbb4, solo lectura
import organismo_g4 as G4         # el instrumento nuevo (grupo4)

T = 30000
N = lambda x: json.loads(json.dumps(x, default=str))


def cmp(a, b, etiqueta, fallos, solo):
    falta = [k for k in solo if k not in b]
    if falta:
        fallos.append((etiqueta, ['FALTAN: ' + str(falta)])); print(f'  DIFIERE {etiqueta}: faltan claves {falta}', flush=True); return False
    dif = [k for k in solo if N(a[k]) != N(b[k])]
    if dif:
        fallos.append((etiqueta, dif)); print(f'  DIFIERE {etiqueta}: {dif}', flush=True); return False
    return True


CASOS = {}
for regla in ('xor01', 'px0', 'azar'):
    for s in (1, 2, 3):
        CASOS[f'{regla}_s{s}'] = dict(mundo='regla', regla=regla, lectura='cuadratica', eta_s=0.015, puerta=3, seed=s)
# casos extra (mas alla del minimo de 9): mundo AB (tronco) y seleccion='wta' con tabla_g=None
CASOS['AB_tronco_s1'] = dict(eta_s=0.015, puerta=3, seed=1)
CASOS['AB_tronco_s2'] = dict(eta_s=0.015, puerta=3, seed=2)
CASOS['xor01_wta_s1'] = dict(mundo='regla', regla='xor01', lectura='cuadratica', eta_s=0.015, puerta=3, seed=1,
                              seleccion='wta', sel_estad='cond')
CASOS['xor01_delta_c1_s1'] = dict(mundo='regla', regla='xor01', lectura='cuadratica', eta_s=0.15, clip_s=10, puerta=3,
                                   seed=1, regla_lenta='delta_signo', constante=True)

if __name__ == '__main__':
    print(f"organismo_v13q5.py sha {__import__('hashlib').sha256(open(LENTO.__file__,'rb').read()).hexdigest()[:16]}")
    print(f"organismo_g4.py    sha {__import__('hashlib').sha256(open(G4.__file__,'rb').read()).hexdigest()[:16]}")

    # (0) la firma: los parametros de v13q5 son un PREFIJO/subconjunto identico de los de g4, mismo orden hasta donde llegan
    sa = list(inspect.signature(LENTO.run).parameters.values())
    sb = {p.name: p for p in inspect.signature(G4.run).parameters.values()}
    faltan_firma = [p.name for p in sa if p.name not in sb or p.default != sb[p.name].default]
    print(f"(0) firma: {'OK, todos los parametros de v13q5 presentes en g4 con igual default' if not faltan_firma else 'DIFIERE ' + str(faltan_firma)}")
    assert 'tabla_g' in sb and sb['tabla_g'].default is None, 'tabla_g debe existir y ser None por defecto'

    t00 = time.time(); fallos = []; n = 0
    claves_v13q5 = None
    for nombre, kw in CASOS.items():
        s = kw.pop('seed')
        a = LENTO.run(s, T=T, **kw)
        if claves_v13q5 is None: claves_v13q5 = list(a)
        b = G4.run(s, T=T, **kw)   # tabla_g=None por defecto: no se pasa
        n += 1
        cmp(a, b, nombre, fallos, solo=claves_v13q5)
        print(f'  {nombre:20s} T={T} seed={s}  {"OK" if not fallos or fallos[-1][0]!=nombre else "FALLA"}', flush=True)

    print(f"\nIDENTIDAD {n - len(fallos)}/{n} casos identicos (subconjunto: las {len(claves_v13q5)} claves originales de organismo_v13q5)   ({time.time()-t00:.1f}s)")
    if fallos:
        print('FALLOS:'); [print('  ', f) for f in fallos]
    sys.exit(1 if fallos else 0)
