"""MINI-EQUIPO 4 -- ORACULO DE LABORATORIO (M4): busca, sobre el flujo YA cosechado (harvestado bajo la regla del
TRONCO, no la mia -- experimentos/creacion_A/lab_eventos_cuadratica_xor01.json, 20 semillas, solo lectura), la mejor
configuracion de "tabla por grupos de pixeles + competencia" (banco_g4.tabla_g_evalua). Repetir el flujo cuesta
milisegundos (mismo patron que meta_regla.py). Busca en semillas 1-10, reporta en las 11-20 RETENIDAS: si la
ganadora no sobrevive al cambio de semillas es sobreajuste de la busqueda, y se dice.

ALCANCE (honesto, por tiempo -- no es la rejilla completa del mecanismo M4 tal como la escribio el jefe):
  g in {1,2} (no 3) x estad in {mse,signo} (no cobertura ni primer-encuentro) x modo in {dura, mezcla(tau=0.5,2.0)}
  x eta in {0.05,0.15} x rho in {0.02,0.05,0.15} x clip in {3,10,30} x alpha in {0.3,1.0}  =  432 configuraciones
  x estimador SOLO 'tabla' (no tabla_binaria ni MCR por celda).

OJO -- limitacion declarada (control 3 del jefe, "el que puede matar el mecanismo entero"): este archivo busca
sobre un flujo harvestado con la regla del TRONCO activa (no con tabla_g encendido), asi que el muestreo real
(que patrones se muerden) es el del tronco, NO el que produciria el organismo con esta regla encendida. Es
BUSQUEDA/DESCUBRIMIENTO rapido, no la validacion final. La validacion en-organismo (con tabla_g REALMENTE
encendido durante el harvesting, control positivo replay==organismo 9/9) ya se corrio en mini_g4.py.

Uso: python meta_regla2_g4.py
Sin organismo, sin Pool, segundos.
"""
import itertools
import json
import os
import sys
import time

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
sys.path.insert(0, os.path.join(AQUI, '..', '..', 'creacion_A'))
from banco_g4 import tabla_g_evalua, med  # noqa: E402

FUENTE = os.path.join(AQUI, '..', '..', 'creacion_A', 'lab_eventos_cuadratica_xor01.json')
REJ = [10, 20, 40, 60, 100, 150, 200, 300, 400, 600]


def configs():
    for g, estad, eta, rho, clip, alpha in itertools.product((1, 2), ('mse', 'signo'), (0.05, 0.15), (0.02, 0.05, 0.15), (3.0, 10.0, 30.0), (0.3, 1.0)):
        yield dict(g=g, estad=estad, modo='dura', tau=1.0, eta=eta, rho=rho, clip=clip, alpha=alpha)
        for tau in (0.5, 2.0):
            yield dict(g=g, estad=estad, modo='mezcla', tau=tau, eta=eta, rho=rho, clip=clip, alpha=alpha)


def punt(D, seeds, c, hasta=None):
    return [tabla_g_evalua(D[s], hasta=hasta, **c)[0] for s in seeds]


def cs(c):
    return (f"g={c['g']} estad={c['estad']} modo={c['modo']}" + (f" tau={c['tau']}" if c['modo'] == 'mezcla' else '')
            + f" eta={c['eta']} rho={c['rho']} clip={c['clip']} alpha={c['alpha']}")


if __name__ == '__main__':
    t00 = time.time()
    D = json.load(open(FUENTE))
    S = sorted(D, key=int)
    TR = [s for s in S if int(s) <= 10]
    TE = [s for s in S if int(s) > 10]
    print(f'=== M4 (grupo4) sobre {os.path.basename(FUENTE)}: busco en {len(TR)} semillas, reporto en {len(TE)} retenidas ===')

    CS = list(configs())
    print(f'espacio: {len(CS)} configuraciones (alcance reducido, ver docstring)')
    filas = []
    for i, c in enumerate(CS, 1):
        v = punt(D, TR, c)
        m = med(v)
        filas.append((m[0] if m else -1, c))
        if i % 100 == 0:
            print(f'  ... {i}/{len(CS)}  ({time.time()-t00:.1f}s)', flush=True)
    filas.sort(key=lambda x: -x[0])

    print(f'\n--- top 10 en la BUSQUEDA (semillas {TR[0]}-{TR[-1]}), con su valor en las RETENIDAS ---')
    print(f'{"busq":>6} {"reten":>6}  config')
    mejores = []
    for m, c in filas[:10]:
        r = med(punt(D, TE, c))
        mejores.append((m, r[0] if r else None, c))
        print(f'{m:>6} {str(r[0] if r else None):>6}  {cs(c)}')

    best = filas[0][1]
    print(f'\n--- GANADORA: {cs(best)}')
    rb = med(punt(D, TE, best))
    print(f'    busqueda {filas[0][0]}   RETENIDAS {rb}')

    # donde queda mi hipotesis (g=2, mse, dura, eta=0.15, rho=0.05, clip=10, alpha=1.0) en el ranking
    hip = dict(g=2, estad='mse', modo='dura', tau=1.0, eta=0.15, rho=0.05, clip=10.0, alpha=1.0)
    rank_hip = next((i for i, (_, c) in enumerate(filas, 1) if c == hip), None)
    print(f'\n--- mi hipotesis (g=2,mse,dura,eta=.15,rho=.05,clip=10,alpha=1) en el ranking de la busqueda: puesto {rank_hip}/{len(filas)}')
    print(f'    busqueda {[m for m,c in filas if c==hip]}   retenidas {med(punt(D, TE, hip))}')

    print('\n--- exposiciones hasta criterio: TRONCO (delta clasico via banco_lab) vs mi GANADORA (semillas retenidas) ---')
    sys.path.insert(0, os.path.join(AQUI, '..', '..', 'creacion_A'))
    from banco_lab import evalua as evalua_delta
    for nom, fn in (('tronco(delta)', lambda s, n: evalua_delta(D[s], 'cuadratica', hasta=n, lector='DELTA')[0]),
                    ('M4_ganadora', lambda s, n: tabla_g_evalua(D[s], hasta=n, **best)[0])):
        vfila = []
        for n in REJ:
            vv = [fn(s, n) for s in TE]
            vfila.append(med(vv))
        v = [x[0] if x else None for x in vfila]
        n65 = next((n for n, x in zip(REJ, v) if x is not None and x >= 0.65), None)
        n75 = next((n for n, x in zip(REJ, v) if x is not None and x >= 0.75), None)
        print(f'{nom:>14} ' + ' '.join(f'{x:>6}' for x in v) + f'   n*(>=.65)={n65 or ">600"}  n*(>=.75)={n75 or ">600"}')

    json.dump(dict(fuente=os.path.basename(FUENTE), busqueda=TR, retenidas=TE, n_configs=len(CS),
                    top=[dict(busq=m, reten=r, config=c) for m, r, c in mejores],
                    ganadora=best, hipotesis_rank=rank_hip),
              open(os.path.join(AQUI, 'meta_regla2_g4.json'), 'w'), indent=1)
    print(f'\nOK -> meta_regla2_g4.json   ({time.time()-t00:.1f}s total)')
