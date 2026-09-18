"""Trio XOR bloque 3c, Agente B (drenaje y canales) -- PUENTE_xor.md.
Mini-prueba de UN proceso (sin Pool), <=3 corridas de T=100000 por invocacion.
Usa experimentos/nivel7_xor_lectura/trio_B/organismo_v13q_B.py (copia de trabajo, NO el original).
Mide, para regla in {xor01, px0}, lectura='cuadratica', eta_s=0.015, puerta=3, T=100000:
  - acc_lenta = signo_acc(W_lenta_apriori, test, vr)  (formula identica a corre_xor_3b.py)
  - Wps-Wns en indices 0 (P0), 1 (P1), 6 (P0*P1)
para variantes (a) lam_lenta=0, (b) clip_s=10, (c) ambas, y baseline (lam_lenta=None, clip_s=3.0 = organismo_v13q.py).

Uso: python mini_prueba_B.py <etiqueta> <regla> <lam_lenta|None> <clip_s> <seed1> [seed2] [seed3]
Ejemplo: python mini_prueba_B.py a_lam0 xor01 0 3.0 201 202 203
"""
import sys, os, json
import numpy as np

AQUI_B = os.path.dirname(os.path.abspath(__file__))
sys.path[:0] = [AQUI_B]
import organismo_v13q_B as m


def signo_acc(Wd, test, vr):   # identica a corre_xor_3b.py (no se toca ese archivo, se reusa la formula)
    f = [1.0 if Wd[k] > 0 else (0.5 if Wd[k] == 0 else 0.0) for k in test if vr[k] == 'comida']
    p = [1.0 if Wd[k] < 0 else (0.5 if Wd[k] == 0 else 0.0) for k in test if vr[k] == 'veneno']
    return 0.5 * float(np.mean(f)) + 0.5 * float(np.mean(p))


def med(xs):
    xs = [x for x in xs if x is not None]
    return float(np.median(xs)), float(min(xs)), float(max(xs))


if __name__ == '__main__':
    etiqueta, regla, lam_lenta_s, clip_s_s = sys.argv[1:5]
    seeds = [int(s) for s in sys.argv[5:]]
    assert len(seeds) <= 3, "REGLA trio: <=3 corridas de 100000 pasos por invocacion"
    lam_lenta = None if lam_lenta_s == 'None' else float(lam_lenta_s)
    clip_s = float(clip_s_s)
    filas = []
    for seed in seeds:
        kw = dict(T=100000, mundo='regla', regla=regla, eta_s=0.015, puerta=3, lectura='cuadratica',
                   lam_lenta=lam_lenta, clip_s=clip_s)
        r = m.run(seed, **kw)
        vr = m.split_regla(seed, regla)[3]; test = r['test']
        acc_lenta = signo_acc(r['W_lenta_apriori'], test, vr)
        Wd = np.array(r['Wps']) - np.array(r['Wns'])
        fila = dict(etiqueta=etiqueta, regla=regla, seed=seed, lam_lenta=lam_lenta, clip_s=clip_s,
                    acc_lenta=acc_lenta, W_P0=round(float(Wd[0]), 3), W_P1=round(float(Wd[1]), 3),
                    W_P0P1=round(float(Wd[6]), 3), splits=r['splits'], celdas=r['celdas'], deaths=r['deaths'])
        filas.append(fila)
        print(json.dumps(fila, ensure_ascii=False))
    accs = [f['acc_lenta'] for f in filas]
    print(f"RESUMEN {etiqueta} regla={regla} lam_lenta={lam_lenta} clip_s={clip_s} seeds={seeds}: "
          f"acc_lenta mediana={med(accs)[0]:.3f} [{med(accs)[1]:.2f},{med(accs)[2]:.2f}] | "
          f"W_P0 mediana={med([f['W_P0'] for f in filas])[0]:+.3f} | "
          f"W_P1 mediana={med([f['W_P1'] for f in filas])[0]:+.3f} | "
          f"W_P0P1 mediana={med([f['W_P0P1'] for f in filas])[0]:+.3f}")
