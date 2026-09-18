"""MINI-EQUIPO 4 -- mini-prueba de UN proceso (regla EQUIPO.md #3: <=6 corridas, T<=200000; aqui 3 semillas x 3
mundos x 2 brazos = 18 corridas de T=100000, secuenciales, un solo proceso, sin Pool).

Mide, con tabla_g encendido (g=2, estad='mse', modo='dura', eta=0.15, rho=0.05, alpha=1.0, clip=10 -- la
configuracion que predijo el jefe de investigacion) contra el brazo APAGADO (tabla_g=None, que es exactamente
A-4: regla_lenta='delta_signo', constante=True, eta_s=0.15, clip_s=10):
  - acc_lenta en xor01, px0, azar (signo_acc sobre W_lenta_apriori, semillas 1-3)
  - CONTROL POSITIVO: el replay offline (banco_g4) sobre el MISMO flujo harvestado debe reproducir el acc_lenta
    in-organismo semilla a semilla (si no, el mecanismo entero se para -- control 3 del jefe)
  - exposiciones hasta 0.75 (REJ igual a banco_lab.py/corre_xor_4.py), via replay
  - cuantas semillas de xor01 abren el rasgo conjuntivo CORRECTO (par (0,1))

Uso: python mini_g4.py
"""
import json
import os
import sys
import time

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(AQUI)))
sys.path[:0] = [os.path.join(RAIZ, 'organismo'), AQUI]  # ERR-28: organismo/ PRIMERO

import organismo_g4 as G4  # noqa: E402
from banco_g4 import tabla_g_evalua, med  # noqa: E402

BASE = dict(mundo='regla', lectura='cuadratica', regla_lenta='delta_signo', constante=True,
            eta_s=0.15, clip_s=10, puerta=3, lab=True)
CFG_G4 = dict(g=2, estad='mse', modo='dura', tau=1.0, eta=0.15, rho=0.05, alpha=1.0, clip=10.0)
REJ = [10, 20, 40, 60, 100, 150, 200, 300, 400, 600]
SEEDS = [1, 2, 3]
REGLAS = ['xor01', 'px0', 'azar']
T = 100000


def signo_acc_local(Wd, test, vr):
    f = [1.0 if Wd[k] > 0 else (0.5 if Wd[k] == 0 else 0.0) for k in test if vr[k] == 'comida']
    p = [1.0 if Wd[k] < 0 else (0.5 if Wd[k] == 0 else 0.0) for k in test if vr[k] == 'veneno']
    if not f or not p:
        return None
    return 0.5 * (sum(f) / len(f)) + 0.5 * (sum(p) / len(p))


if __name__ == '__main__':
    t00 = time.time()
    resultados = {}
    for regla in REGLAS:
        for brazo, tg in (('APAGADO_A4', None), ('GRUPO4_g2mse', CFG_G4)):
            for s in SEEDS:
                t0 = time.time()
                r = G4.run(s, T=T, regla=regla, tabla_g=tg, **BASE)
                pats, tren, test, vr = G4.split_regla(s, regla)
                acc_organismo = signo_acc_local(r['W_lenta_apriori'], test, vr)
                d = dict(seed=s, lectura=BASE['lectura'], regla=regla, T=T, fase2_en=r['fase2_en'],
                          eventos=[[int(a), b, float(c), float(dd)] for a, b, c, dd in r['lenta_eventos']],
                          test=test, vr={k: vr[k] for k in vr})
                n_pre = len([e for e in d['eventos'] if e[0] < d['fase2_en']])
                if tg is not None:
                    acc_replay, n_ev, gan = tabla_g_evalua(d, **CFG_G4)
                    control_ok = (acc_replay is None and acc_organismo is None) or (acc_replay is not None and acc_organismo is not None and abs(acc_replay - acc_organismo) < 1e-9)
                    curva = {}
                    for n in REJ:
                        a_n, _, _ = tabla_g_evalua(d, hasta=n, **CFG_G4)
                        curva[n] = a_n
                    n75 = next((n for n in REJ if curva[n] is not None and curva[n] >= 0.75), None)
                    n65 = next((n for n in REJ if curva[n] is not None and curva[n] >= 0.65), None)
                    abre_correcto = bool(r['g4_abre_conjuntivo_correcto']) if regla == 'xor01' else None
                    ganador_final = r['g4_ganador']
                else:
                    acc_replay = control_ok = curva = n75 = n65 = abre_correcto = ganador_final = None
                key = f'{regla}_{brazo}_s{s}'
                resultados[key] = dict(regla=regla, brazo=brazo, seed=s, n_pre=n_pre,
                                        acc_lenta_organismo=acc_organismo, acc_lenta_replay=acc_replay,
                                        control_replay_ok=control_ok, curva_expo=curva, n75=n75, n65=n65,
                                        ganador_final=ganador_final, abre_conjuntivo_correcto=abre_correcto,
                                        segs=round(time.time() - t0, 2))
                print(f"  {key:28s} n_pre={n_pre:4d} acc_org={acc_organismo} acc_replay={acc_replay} "
                      f"control_ok={control_ok} n75={n75} ganador={ganador_final} ({time.time()-t0:.1f}s)", flush=True)

    print(f"\n=== RESUMEN (t total {time.time()-t00:.1f}s) ===")
    for brazo in ('APAGADO_A4', 'GRUPO4_g2mse'):
        for regla in REGLAS:
            vs = [resultados[f'{regla}_{brazo}_s{s}']['acc_lenta_organismo'] for s in SEEDS]
            print(f"  acc_lenta {brazo:14s} {regla:6s}: semillas {vs}  mediana {med(vs)}")
    controles = [resultados[k]['control_replay_ok'] for k in resultados if resultados[k]['control_replay_ok'] is not None]
    print(f"\n  CONTROL POSITIVO (replay == organismo): {sum(bool(c) for c in controles)}/{len(controles)}")
    n75s = {regla: [resultados[f'{regla}_GRUPO4_g2mse_s{s}']['n75'] for s in SEEDS] for regla in REGLAS}
    print(f"  n*(>=0.75) por regla (GRUPO4): {n75s}")
    aciertos_conj = [resultados[f'xor01_GRUPO4_g2mse_s{s}']['abre_conjuntivo_correcto'] for s in SEEDS]
    print(f"  xor01: abre el par (0,1) correcto en {sum(bool(x) for x in aciertos_conj)}/{len(aciertos_conj)} semillas: {aciertos_conj}")

    json.dump(resultados, open(os.path.join(AQUI, 'mini_g4.json'), 'w'), indent=1)
    print("\nOK -> mini_g4.json")
