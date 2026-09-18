"""grupo4/M4 -- replay OFFLINE de "tabla por grupos + competencia" sobre el flujo (t, patron, R, residuo) ya
harvestado (organismo_g4 con lab=True). El residuo (_ds) es EXACTAMENTE la senal que el organismo usa in-loop
(mismo dato que consume banco_lab.delta para el tronco), asi que este replay es el CONTROL POSITIVO del mecanismo:
si no reproduce el acc_lenta del organismo cuando se harvesta con la perilla YA encendida, el mecanismo entero se
para (regla EQUIPO / control 3 del jefe). Reusa (solo lectura, sin tocar el archivo) pat_de/signo_acc/med de
experimentos/creacion_A/banco_lab.py -- exactamente los mismos helpers que ya usa meta_regla.py.
Sin organismo, sin Pool, milisegundos por configuracion.
"""
import itertools
import os
import sys

import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'creacion_A'))
from banco_lab import pat_de, signo_acc, med  # noqa: E402  (solo lectura)


def tabla_g_evalua(d, g=2, estad='mse', modo='dura', tau=1.0, eta=0.15, rho=0.05, alpha=1.0, clip=10.0, hasta=None):
    """Replay puro de la regla de grupo4. Devuelve (acc_signo, n_eventos_usados, grupo_ganador_como_tupla)."""
    ev = [e for e in d['eventos'] if e[0] < d['fase2_en']]
    if hasta is not None:
        ev = ev[:hasta]
    if not ev:
        return None, 0, None
    grupos = list(itertools.combinations(range(6), g))
    ng = len(grupos)
    tabla = np.zeros((ng, 2 ** g))
    vistos = np.zeros((ng, 2 ** g), bool)
    ecomp = np.zeros(ng)

    def idx(P, gi):
        c = 0
        for p in grupos[gi]:
            c = c * 2 + (1 if P[p] > 0.5 else 0)
        return c

    for (_t, patron, _R, ds) in ev:
        P = pat_de(patron)
        for gi in range(ng):
            c = idx(P, gi)
            pred_antes = tabla[gi, c] if vistos[gi, c] else 0.0
            if estad == 'mse':
                ecomp[gi] = (1 - rho) * ecomp[gi] - rho * ((ds - pred_antes) ** 2)
            else:
                ecomp[gi] = (1 - rho) * ecomp[gi] + rho * (1.0 if (pred_antes > 0) == (ds > 0) else (0.0 if pred_antes == 0 else -1.0))
            tabla[gi, c] = np.clip((tabla[gi, c] + eta * (ds - tabla[gi, c])) if vistos[gi, c] else ds, -clip, clip)
            vistos[gi, c] = True

    gan = int(np.argmax(ecomp))

    def lee(P):
        codes = [idx(P, gi) for gi in range(ng)]
        preds = np.array([tabla[gi, codes[gi]] for gi in range(ng)])
        if modo == 'dura':
            return alpha * float(preds[gan])
        w = ecomp / max(tau, 1e-9)
        w = np.exp(w - w.max())
        w = w / w.sum()
        return alpha * float((w * preds).sum())

    pats = {k: pat_de(k) for k in d['vr']}
    pred = {k: lee(v) for k, v in pats.items()}
    return signo_acc(pred, d['test'], d['vr']), len(ev), grupos[gan]
