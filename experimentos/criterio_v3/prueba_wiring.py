"""PRUEBA DE CABLEADO del runner A-CAL — NO corre ninguna simulacion, no abre ningun Pool, no escribe en datos/.
Le pasa a etapa_TC, etapa_TA y etapas_5_6 unos crudos SINTETICOS con la forma exacta que producen tarea_rev y
tarea_vivo, y verifica que el runner llega al final y que las letras hacen lo que dicen. Sirve para que la serie
de 360 corridas no se caiga en la etapa 6 despues de quince minutos de Pool.

Los numeros de aqui son INVENTADOS (ruido gaussiano con la sd medida en las series reales, sd(r) ~ 11-13):
NO son evidencia de nada y no se citan como resultado. Lo unico que se prueba es el cableado y el sentido de cada
letra sobre casos construidos:
  A) NULO (candidato = tronco, delta 0)      -> v3 debe PASAR casi siempre; v2 n=20 debe caer a menudo.
  B) PEOR (delta = -20 en r y en rev)        -> las dos letras deben RECHAZAR.
  C) MEJOR (delta = +25 en rev)              -> v2 T-C ii puede pasar; v3 tambien (no inferioridad).

    python experimentos/criterio_v3/prueba_wiring.py
"""
import sys, os

sys.stdout.reconfigure(encoding='utf-8', errors='replace')
AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
sys.path[:0] = [os.path.join(RAIZ, 'organismo'), os.path.join(RAIZ, 'experimentos', 'nivel11_mundo_vivo'), AQUI]

import numpy as np
import corre_criterio_v3 as R

rng = np.random.default_rng(20260921)
SEM = list(range(2161, 2201))
SEM_R = list(range(2121, 2161))


def crudo_vivo(delta_peor):
    out = []
    for b, (mr, sr) in (('VIVO', (-72.0, 11.0)), ('CUELLO_MIN', (-8.0, 9.0))):
        for s in SEM:
            base = rng.normal(0, 0.8)
            for arm in R.ARMS:
                d = delta_peor if arm == 'PEOR' else 0.0
                out.append(dict(brazo=b, seed=s, arm=arm, r=float(rng.normal(mr, sr) + base + d),
                                deaths=float(rng.normal(95, 9) - d * 0.8), descendientes=float(rng.normal(20, 4)),
                                celdas=float(rng.normal(34, 3)), splits=float(rng.normal(4, 1)),
                                des_splits=1, placebo=(1 if arm == 'PLACEBO' else 0)))
    return out


def crudo_rev(delta_peor, delta_mejor=0.0):
    out = []
    for s in SEM_R:
        for arm in R.ARMS:
            d = delta_peor if arm == 'PEOR' else (delta_mejor if arm == 'PLACEBO' else 0.0)
            out.append(dict(seed=s, arm=arm, rev=float(rng.normal(40, 14) + d),
                            deaths=float(rng.normal(110, 10)), celdas=40.0, splits=10.0,
                            mordA=[0, 0, 0, 160], mordB=[0, 0, 0, 200],
                            visA=[0, 0, 0, 1700], visB=[0, 0, 0, 240], placebo=(1 if arm == 'PLACEBO' else 0)))
    return out


if __name__ == '__main__':
    R._log['nom'] = 'prueba_wiring'
    R.B_REP = 800   # la prueba de cableado no necesita 4000 repartos
    fallos = 0

    print('=== CASO A: el PLACEBO es el nulo (delta 0) y el PEOR esta a delta = -20 ===')
    V = {}
    R.etapa_TC(crudo_rev(-20.0), V)
    R.etapa_TA(crudo_vivo(-20.0), V)
    res_v = crudo_vivo(-20.0); res_r = crudo_rev(-20.0)
    V = {}; R.etapa_TC(res_r, V); R.etapa_TA(res_v, V); R.etapas_5_6(V, res_v, res_r)
    esperado = [
        ('PLACEBO pasa T-A v3', V['T-A']['pasa_v3_PLACEBO'], True),
        ('PEOR NO pasa T-A v3', V['T-A']['pasa_v3_PEOR'], False),
        ('PEOR NO pasa T-A v2', V['T-A']['pasa_v2_PEOR'], False),
        ('PLACEBO pasa T-C ii v3', V['T-C_ii']['PLACEBO']['pasa_v3'], True),
        ('PEOR NO pasa T-C ii v3', V['T-C_ii']['PEOR']['pasa_v3'], False),
        ('CAL-3 (delta -20 rechazado) <= 0.05', V['CAL']['CAL-3']['medido'] <= 0.05, True),
        ('CAL-1 (placebo pasa v3 n=40) >= 0.85', V['CAL']['CAL-1']['medido'] >= 0.85, True),
        ('CAL-2 (placebo pasa v2 n=20) <= 0.50', V['CAL']['CAL-2']['medido'] <= 0.50, True),
        ('CAL-5 (placebo pasa T-C ii v2) <= 0.10', V['CAL']['CAL-5']['medido'] <= 0.10, True),
    ]
    print('\n--- cableado ---')
    for nom, got, exp in esperado:
        ok = (got == exp)
        fallos += (not ok)
        print(f"  {'OK ' if ok else '***'} {nom:42s} -> {got}")

    print('\n=== CASO C: un candidato que REVIERTE MEJOR (delta = +25 en rev) ===')
    res_r2 = crudo_rev(-20.0, delta_mejor=+25.0)
    V2 = {}; R.etapa_TC(res_r2, V2)
    for nom, got, exp in (('MEJOR pasa T-C ii v2 (A12>=0.75)', V2['T-C_ii']['PLACEBO']['pasa_v2'], True),
                          ('MEJOR pasa T-C ii v3 (no inferioridad)', V2['T-C_ii']['PLACEBO']['pasa_v3'], True)):
        ok = (got == exp); fallos += (not ok)
        print(f"  {'OK ' if ok else '***'} {nom:42s} -> {got}")

    print(f"\nCABLEADO: {'OK' if fallos == 0 else f'*** {fallos} FALLOS ***'}  (numeros sinteticos: no son evidencia)")
    sys.exit(0 if fallos == 0 else 1)
