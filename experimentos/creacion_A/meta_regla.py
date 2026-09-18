"""CREADOR A — (2) META-APRENDIZAJE DE LA REGLA LOCAL, fuera del organismo, sobre el flujo real de encuentros.

La familia de reglas se restringe A PROPOSITO a lo que `organismo_v13q4/q5` YA tiene como perillas, para que la
ganadora se pueda **implantar como regla local sin escribir una linea nueva y sin gradiente en tiempo de ejecucion**:
    eta_s · clip_s · lam_lenta · seleccion{off|wta} · sel_theta · sel_rho · sel_cupo · sel_estad{cond|cov}
Busqueda: rejilla completa sobre el flujo YA cosechado (repetir el flujo cuesta milisegundos). **Se busca en las
semillas 1-10 y se reporta en las 11-20 (retenidas)**: si la ganadora no sobrevive al cambio de semillas, es
sobreajuste de la busqueda y se dice.

Uso: python meta_regla.py [lectura] [regla]
Sin organismo, sin Pool.
"""
import sys, os, json, itertools
import numpy as np

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
from banco_lab import evalua, med

REJILLA = dict(
    eta=[0.005, 0.015, 0.05, 0.15],
    clip=[3.0, 10.0, 30.0],
    lam=[0.0, 0.002],
    sel=[None, 'wta'],
    theta=[0.3, 0.6, 1.0],
    rho=[0.02, 0.05, 0.15],
    cupo=[1, 2],
    estad=['cond', 'cov'],
)


def configs():
    vistos = set()
    for eta, clip, lam, sel in itertools.product(REJILLA['eta'], REJILLA['clip'], REJILLA['lam'], REJILLA['sel']):
        if sel is None:
            c = dict(eta=eta, clip=clip, lam=lam, sel=None)
            k = json.dumps(c, sort_keys=True)
            if k not in vistos: vistos.add(k); yield c
        else:
            for th, rh, cu, es in itertools.product(REJILLA['theta'], REJILLA['rho'], REJILLA['cupo'], REJILLA['estad']):
                yield dict(eta=eta, clip=clip, lam=lam, sel=sel, theta=th, rho=rh, cupo=cu, estad=es)


def punt(D, seeds, lectura, c, hasta=None):
    kw = dict(eta=c['eta'], clip=c['clip'], lam=c['lam'], sel=c['sel'])
    if c['sel']: kw.update(theta=c['theta'], rho=c['rho'], cupo=c['cupo'], estad=c['estad'])
    return [evalua(D[s], lectura, hasta=hasta, lector='DELTA', **kw)[0] for s in seeds]


if __name__ == '__main__':
    lectura = sys.argv[1] if len(sys.argv) > 1 else 'cuadratica'
    regla = sys.argv[2] if len(sys.argv) > 2 else 'xor01'
    D = json.load(open(os.path.join(AQUI, f'lab_eventos_{lectura}_{regla}.json')))
    S = sorted(D, key=int)
    TR = [s for s in S if int(s) <= 10]; TE = [s for s in S if int(s) > 10]
    print(f'=== meta-aprendizaje sobre {lectura}/{regla}: busco en {len(TR)} semillas, reporto en {len(TE)} retenidas ===')
    base = dict(eta=0.015, clip=3.0, lam=0.0, sel=None)
    print(f'    tronco (eta=0.015, clip=3, sin seleccion): busqueda {med(punt(D,TR,lectura,base))}   '
          f'retenidas {med(punt(D,TE,lectura,base))}')
    CS = list(configs())
    filas = []
    for i, c in enumerate(CS, 1):
        v = punt(D, TR, lectura, c)
        m = med(v)
        filas.append((m[0] if m else -1, c))
        if i % 200 == 0: print(f'    ... {i}/{len(CS)}', flush=True)
    filas.sort(key=lambda x: -x[0])
    print(f'\n--- top 8 en la BUSQUEDA (semillas {TR[0]}-{TR[-1]}), con su valor en las RETENIDAS ---')
    print(f'{"busq":>6} {"reten":>6}  config')
    mejores = []
    for m, c in filas[:8]:
        r = med(punt(D, TE, lectura, c))
        mejores.append((m, r[0] if r else None, c))
        cs = (f"eta={c['eta']} clip={c['clip']} lam={c['lam']} sel={c['sel']}"
              + (f" theta={c['theta']} rho={c['rho']} cupo={c['cupo']} estad={c['estad']}" if c['sel'] else ""))
        print(f'{m:>6} {str(r[0] if r else None):>6}  {cs}')
    best = filas[0][1]
    print(f'\n--- GANADORA: {best}')
    rb = med(punt(D, TE, lectura, best))
    print(f'    busqueda {filas[0][0]}   RETENIDAS {rb}')
    print('\n--- exposiciones hasta criterio de la ganadora contra el tronco (semillas retenidas) ---')
    REJ = [10, 20, 40, 60, 100, 150, 200, 300, 400, 600]
    for nom, c in (('tronco', base), ('ganadora', best)):
        v = [med(punt(D, TE, lectura, c, hasta=n)) for n in REJ]
        v = [x[0] if x else None for x in v]
        n65 = next((n for n, x in zip(REJ, v) if x is not None and x >= 0.65), None)
        n75 = next((n for n, x in zip(REJ, v) if x is not None and x >= 0.75), None)
        print(f'{nom:>9} ' + ' '.join(f'{x:>6}' for x in v) + f'   n*(>=.65)={n65 or ">600"}  n*(>=.75)={n75 or ">600"}')
    json.dump(dict(lectura=lectura, regla=regla, busqueda=TR, retenidas=TE,
                   top=[dict(busq=m, reten=r, config=c) for m, r, c in mejores], ganadora=best),
              open(os.path.join(AQUI, f'meta_regla_{lectura}_{regla}.json'), 'w'), indent=1)
    print(f'\nOK -> meta_regla_{lectura}_{regla}.json')
