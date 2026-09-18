"""CREADOR A — cosecha el FLUJO DE ENCUENTROS de la via lenta (para el control positivo y el meta-aprendizaje).

Corre `organismo_v13q5` con `lab=True` (registro puro; identidad 16/16 con la perilla apagada) y guarda, por semilla,
la secuencia exacta `(t, patron, R, residuo)` de cada actualizacion de la via lenta, el paso de la sonda, el
`acc_lenta` que el organismo obtuvo y el reparto tren/test. Con eso, `banco_lab.py` repite ESE MISMO flujo fuera del
organismo con cualquier lector (delta del tronco, minimos cuadrados exactos, gradiente, MLP con retropropagacion)
sin volver a correr el mundo.

Uso: python cosecha_lab.py <lectura> <regla> <s1> ... (maximo 6 corridas por invocacion, EQUIPO regla 3)
Sin Pool.
"""
import sys, os, json, time
import numpy as np

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path[:0] = [AQUI, os.path.join(AQUI, '..', 'nivel7_xor_lectura')]
import organismo_v13q5 as Q

T = 100000                                   # el BASE de 3d/3e
BASE = dict(mundo='regla', eta_s=0.015, puerta=3, constante=True,
            regla_lenta='delta_signo', lam_lenta=0.0, clip_s=3.0, puerta_=None)
BASE.pop('puerta_')


def signo_acc(Wd, test, vr):
    f = [1.0 if Wd[k] > 0 else (0.5 if Wd[k] == 0 else 0.0) for k in test if vr[k] == 'comida']
    p = [1.0 if Wd[k] < 0 else (0.5 if Wd[k] == 0 else 0.0) for k in test if vr[k] == 'veneno']
    if not f or not p: return None
    return 0.5 * float(np.mean(f)) + 0.5 * float(np.mean(p))


if __name__ == '__main__':
    lectura = sys.argv[1]; regla = sys.argv[2]; seeds = [int(x) for x in sys.argv[3:]]
    assert len(seeds) <= 6, 'maximo 6 corridas por invocacion (EQUIPO regla 3)'
    f = os.path.join(AQUI, f'lab_eventos_{lectura}_{regla}.json')
    datos = json.load(open(f)) if os.path.exists(f) else {}
    for s in seeds:
        t0 = time.time()
        r = Q.run(s, T=T, regla=regla, lectura=lectura, lab=True, **BASE)
        pats, tren, test, vr = Q.split_regla(s, regla)
        al = signo_acc(r['W_lenta_apriori'], test, vr)
        pre = [e for e in r['lenta_eventos'] if e[0] < r['fase2_en']]
        cls = {}
        for _, k, _, _ in pre:
            c = k[:2]; cls[c] = cls.get(c, 0) + 1
        datos[str(s)] = dict(seed=s, lectura=lectura, regla=regla, T=T, fase2_en=r['fase2_en'],
                             eventos=[[int(a), b, float(c), float(d)] for a, b, c, d in r['lenta_eventos']],
                             n_pre=len(pre), clases_pre=cls, clases_vacias=4 - len(cls),
                             acc_lenta_organismo=al, tren=tren, test=test,
                             vr={k: vr[k] for k in vr}, Ws_apriori=[float(x) for x in r['Ws_apriori']])
        print(f'  s{s:>3} {lectura:>12} {regla:>6}: eventos pre-sonda {len(pre):>4}  clases {cls}  '
              f'vacias {4-len(cls)}  acc_lenta_organismo {al}  ({time.time()-t0:.1f}s)', flush=True)
    json.dump(datos, open(f, 'w'), indent=None)
    print(f'-> {os.path.basename(f)}  ({len(datos)} semillas)')
