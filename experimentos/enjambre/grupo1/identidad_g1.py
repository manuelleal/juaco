"""Arnes de identidad de organismo_g1 (enjambre/grupo1, mecanismo M1 - compartimentos de dos canales).

Con `celdas=None` (por defecto), organismo_g1.run(...) debe ser BIT A BIT igual -- TODAS las claves del
original, mas las 3 claves nuevas SIEMPRE presentes pero sin efecto (cel_modo=None, cel_ganadora=None,
cel_E=[1e9]*15) -- a experimentos/creacion_A/organismo_v13q5.run(...) (fae9c32b146fdbb4, solo se lee).
Normalizacion: N = json.loads(json.dumps(x, default=str)) (misma convencion que identidad_v13q5_rapido.py).

Cobertura (>= 9 casos pedidos): 2 configuraciones (BASE de la serie de grupo1, y una config ALTERNA con las
perillas viejas en sus valores por defecto) x 3 reglas (xor01/px0/azar) x 3 semillas (1,2,3) = 18, mas el
mundo 'AB' x 3 semillas = 21 comparaciones en total. T=30000 (mas corto que el mini_g1, solo para identidad).

REGLA: si esto no da 100%, la perilla no se usa para nada. Se corre y se reporta n/n ANTES de mirar cualquier
otro numero (acc_lenta, etc.) -- protocolo del proyecto (registro/EQUIPO.md).
OJO (ERR-28): organismo/ va PRIMERO en sys.path, siempre.
Uso: python identidad_g1.py
"""
import json, os, sys

sys.stdout.reconfigure(encoding='utf-8', errors='replace')
AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.abspath(os.path.join(AQUI, '..', '..', '..'))
CREACION_A = os.path.abspath(os.path.join(AQUI, '..', '..', 'creacion_A'))
sys.path[:0] = [os.path.join(RAIZ, 'organismo'), AQUI, CREACION_A]   # ERR-28: organismo/ PRIMERO

import organismo_g1 as G1         # el instrumento de esta sesion (celdas=None debe ser el original exacto)
import organismo_v13q5 as ORIG    # el original de referencia (fae9c32b146fdbb4), interpretado

T = 30000
SEEDS = [1, 2, 3]
N = lambda x: json.loads(json.dumps(x, default=str))

CLAVES_NUEVAS = {'cel_modo', 'cel_ganadora', 'cel_E'}


def cmp(a, b, etiqueta, fallos):
    """Compara TODAS las claves de `b` (el original, con menos claves) contra `a` (organismo_g1)."""
    fa = set(a)
    faltan = [k for k in b if k not in fa]
    if faltan:
        fallos.append((etiqueta, ['FALTAN: ' + str(faltan)])); print(f"  DIFIERE {etiqueta}: faltan claves {faltan}", flush=True); return False
    extra_inesperada = fa - set(b) - CLAVES_NUEVAS
    if extra_inesperada:
        fallos.append((etiqueta, ['CLAVES EXTRA NO DECLARADAS: ' + str(sorted(extra_inesperada))]))
        print(f"  DIFIERE {etiqueta}: claves extra no declaradas {sorted(extra_inesperada)}", flush=True); return False
    dif = [k for k in b if N(a[k]) != N(b[k])]
    if dif:
        fallos.append((etiqueta, dif)); print(f"  DIFIERE {etiqueta}: {dif}", flush=True); return False
    return True


BASE = dict(mundo='regla', puerta=3, lectura='cuadratica', regla_lenta='delta_signo', constante=True,
            lam_lenta=0.0, eta_s=0.15, clip_s=10.0)
ALT = dict(mundo='regla', puerta=3)   # perillas viejas en su default: lectura='lineal', regla_lenta='dos_canales', constante=False, eta_s=0.0

CONFIGS = {}
for _nom, _kw in (('base', BASE), ('alt', ALT)):
    for _regla in ('xor01', 'px0', 'azar'):
        CONFIGS[f'{_nom}_{_regla}'] = dict(_kw, regla=_regla)

if __name__ == '__main__':
    print(f"organismo_g1.py      sha {__import__('hashlib').sha256(open(G1.__file__,'rb').read()).hexdigest()[:16]}")
    print(f"organismo_v13q5.py   sha {__import__('hashlib').sha256(open(ORIG.__file__,'rb').read()).hexdigest()[:16]}")
    fallos = []; n = 0

    # ---- (0) la firma: los parametros VIEJOS de organismo_g1.run deben calzar uno a uno con organismo_v13q5.run
    import inspect
    sg = inspect.signature(G1.run); so = inspect.signature(ORIG.run)
    viejos = [(p.name, p.default) for p in sg.parameters.values() if p.name not in ('celdas', 'cel_rho')]
    orig_params = [(p.name, p.default) for p in so.parameters.values()]
    n += 1
    if viejos != orig_params:
        fallos.append(('0/firma', ['firma distinta']))
        print(f"  DIFIERE 0/firma:\n    g1(sin celdas/cel_rho) = {viejos}\n    v13q5                  = {orig_params}", flush=True)
    else:
        print(f"(0) firma identica parametro a parametro salvo celdas/cel_rho al final ({len(orig_params)} parametros viejos)")
    nuevos = [p.name for p in sg.parameters.values()][-2:]
    print(f"    perillas nuevas al final de la firma: {nuevos} (esperado ['celdas', 'cel_rho'])")

    # ---- (1) la rejilla: celdas=None (organismo_g1) == organismo_v13q5, TODAS las claves de v13q5
    print(f"\n(1) celdas=None == organismo_v13q5, {len(CONFIGS)} configuraciones x {len(SEEDS)} semillas a T={T}")
    for nombre, kw in CONFIGS.items():
        fc = 0
        for s in SEEDS:
            a = G1.run(s, T=T, celdas=None, **kw); b = ORIG.run(s, T=T, **kw); n += 1
            if not cmp(a, b, f"1/{nombre}/s{s}", fallos): fc += 1
        print(f"  {nombre:12s} {len(SEEDS) - fc}/{len(SEEDS)} semillas identicas", flush=True)

    # ---- (2) mundo 'AB' (bonus, no contado en el >=9 pedido pero cubre la otra rama del codigo)
    print(f"\n(2) mundo 'AB' (bonus)")
    for s in SEEDS:
        a = G1.run(s, T=T, celdas=None); b = ORIG.run(s, T=T); n += 1
        cmp(a, b, f"2/AB/s{s}", fallos)
    print(f"  AB           {len(SEEDS) - sum(1 for f in fallos if f[0].startswith('2/AB'))}/{len(SEEDS)} semillas identicas", flush=True)

    # ---- (3) celdas=None: las 3 claves nuevas existen y son el valor 'apagado' declarado
    print(f"\n(3) claves nuevas en el brazo apagado (celdas=None)")
    r = G1.run(1, T=2000, celdas=None); n += 1
    ok3 = (r['cel_modo'] is None) and (r['cel_ganadora'] is None) and (r['cel_E'] == [1e9] * 15)
    if not ok3:
        fallos.append(('3/apagado', ['cel_modo/cel_ganadora/cel_E inesperados']))
        print(f"  DIFIERE 3/apagado: cel_modo={r['cel_modo']} cel_ganadora={r['cel_ganadora']} cel_E[:3]={r['cel_E'][:3]}")
    else:
        print(f"  OK: cel_modo=None, cel_ganadora=None, cel_E=[1e9]*15 (nunca tocado)")

    print(f"\nIDENTIDAD {n - len(fallos)}/{n} comparaciones identicas")
    if fallos:
        print("FALLOS:"); [print('  ', f) for f in fallos]
    sys.exit(1 if fallos else 0)
