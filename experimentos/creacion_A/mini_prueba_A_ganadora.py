"""CREADOR A — implanta la regla GANADORA del meta-aprendizaje como REGLA LOCAL en el organismo y la mide.

La familia de la busqueda se restringio a perillas que `organismo_v13q5` ya tiene, asi que implantar = pasar los
parametros: **no hay gradiente en tiempo de ejecucion, no hay linea nueva de codigo**. Se compara contra el tronco
(mismas semillas, mismo T) y contra lo que el banco predijo para esa misma configuracion sobre el flujo cosechado.
Uso: python mini_prueba_A_ganadora.py <regla> <s1> <s2> <s3>   (maximo 3 corridas)
"""
import sys, os, json, time
import numpy as np

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path[:0] = [AQUI, os.path.join(AQUI, '..', 'nivel7_xor_lectura')]
import organismo_v13q5 as Q

T = 100000
LECT = 'cuadratica'


def signo_acc(Wd, test, vr):
    f = [1.0 if Wd[k] > 0 else (0.5 if Wd[k] == 0 else 0.0) for k in test if vr[k] == 'comida']
    p = [1.0 if Wd[k] < 0 else (0.5 if Wd[k] == 0 else 0.0) for k in test if vr[k] == 'veneno']
    if not f or not p: return None
    return 0.5 * float(np.mean(f)) + 0.5 * float(np.mean(p))


def kw_de(c):
    kw = dict(eta_s=c['eta'], clip_s=c['clip'], lam_lenta=c['lam'])
    if c['sel']:
        kw.update(seleccion='wta', sel_theta=c['theta'], sel_rho=c['rho'], sel_cupo=c['cupo'], sel_estad=c['estad'])
    return kw


if __name__ == '__main__':
    regla = sys.argv[1]; seeds = [int(x) for x in sys.argv[2:]]
    assert len(seeds) <= 3, 'maximo 3 corridas'
    M = json.load(open(os.path.join(AQUI, f'meta_regla_{LECT}_{regla}.json')))
    best = M['ganadora']
    tronco = dict(eta=0.015, clip=3.0, lam=0.0, sel=None)
    print(f'GANADORA: {best}')
    out = []
    for nom, c in (('TRONCO', tronco), ('GANADORA', best)):
        for s in seeds:
            t0 = time.time()
            r = Q.run(s, T=T, mundo='regla', regla=regla, lectura=LECT, constante=True,
                      regla_lenta='delta_signo', puerta=3, lab=True, **kw_de(c))
            _, tren, test, vr = Q.split_regla(s, regla)
            al = signo_acc(r['W_lenta_apriori'], test, vr)
            npre = len([e for e in r['lenta_eventos'] if e[0] < r['fase2_en']])
            fila = dict(brazo=nom, regla=regla, seed=s, acc_lenta=al,
                        acc=signo_acc(r['W_apriori'], test, vr), n_pre=npre,
                        abiertos=r.get('sel_abiertos', []), config=c, seg=round(time.time() - t0, 1))
            out.append(fila)
            print(f'  {nom:>9} s{s:>3} {regla:>6}: acc_lenta={al}  acc={fila["acc"]}  eventos_pre={npre}  '
                  f'abiertos={fila["abiertos"]}  ({fila["seg"]}s)', flush=True)
    f = os.path.join(AQUI, 'mini_ganadora.json')
    viejo = json.load(open(f)) if os.path.exists(f) else []
    json.dump(viejo + out, open(f, 'w'), indent=1)
    med = lambda b: float(np.median([x['acc_lenta'] for x in out if x['brazo'] == b and x['acc_lenta'] is not None]))
    print(f'  mediana TRONCO {med("TRONCO"):.3f}   GANADORA {med("GANADORA"):.3f}')
    print('->', f)
