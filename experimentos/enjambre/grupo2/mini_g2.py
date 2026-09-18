"""MINI-EQUIPO 2 (enjambre) -- mini-prueba de UN PROCESO (sin Pool): organismo_g2.py con `fision='conflicto'`
en xor01, px0 y azar. Semillas 1-3, T=100000, regla_lenta='delta_signo', constante=True, eta_s=0.15, clip_s=10
(las constantes de v14.1 / A-4), lectura='cuadratica' (con fision activo la via lenta NO usa phi(): cada celda
lee su propia base fija {P_i,1} o {P_i,P_j,P_i*P_j,1}; `lectura` solo fija el tamano inerte de Ws/Wps/Wns).
fis_umbral=3.0, fis_rho=0.05 -- constantes del mecanismo, fijadas ANTES de correr (PREREGISTRO_g2.md).

acc_lenta = signo_acc(W_lenta_apriori, test, vr): acierto balanceado por signo de la via lenta SOLA, sobre los
patrones NUNCA VISTOS, leido en la sonda a priori (t == fase2_en == T//2), exactamente como corre_xor_4.py.

EXPOSICIONES (n*): replay EXTERNO de la MISMA regla local de M2 sobre `lenta_eventos` (grabados con lab=True;
cada evento es (t, patron_str, R, residuo_organismo)), igual metodo que corre_xor_4.py/banco_lab.py: se repite
la actualizacion con los primeros n eventos pre-sonda para cada n de REJ y se mide acc_lenta con esos pesos.
Se verifica (VERIFICACION DE REPLAY, print aparte) que el replay con TODOS los eventos pre-sonda reproduce la
celda ganadora y el signo de la prediccion que el organismo calculo por si mismo en `W_lenta_apriori`.

Uso: python mini_g2.py
"""
import sys, os, json, time
import numpy as np

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path[:0] = [AQUI]
import organismo_g2 as m

SEEDS = [1, 2, 3]
REGLAS = ['xor01', 'px0', 'azar']
REJ = [10, 20, 40, 60, 100, 150, 200, 300, 400, 600, 1000, 1500]
FIS_UMBRAL = 3.0
FIS_RHO = 0.05
BASE = dict(T=100000, mundo='regla', puerta=3, constante=True, regla_lenta='delta_signo', lam_lenta=0.0,
            lectura='cuadratica', eta_s=0.15, clip_s=10.0, fision='conflicto',
            fis_umbral=FIS_UMBRAL, fis_rho=FIS_RHO, lab=True)


def signo_acc(Wd, test, vr):
    """Acierto BALANCEADO por signo sobre los nunca vistos. Empate exacto = 0.5. Formula del registro (corre_xor_4.py)."""
    f = [1.0 if Wd[k] > 0 else (0.5 if Wd[k] == 0 else 0.0) for k in test if vr[k] == 'comida']
    p = [1.0 if Wd[k] < 0 else (0.5 if Wd[k] == 0 else 0.0) for k in test if vr[k] == 'veneno']
    if not f or not p:
        return None
    return 0.5 * float(np.mean(f)) + 0.5 * float(np.mean(p))


def pat_de(nombre):
    return np.array([float(c) for c in nombre])


def replay_fision(pre, n, fis_umbral=FIS_UMBRAL, fis_rho=FIS_RHO, eta_s=BASE['eta_s'], clip_s=BASE['clip_s']):
    """Repite, FUERA del organismo, EXACTAMENTE la regla local de M2 (mismas 3 pasadas que organismo_g2.py,
    ancla 4) sobre los primeros n eventos (t, patron_str, R, _ds) de la secuencia lab. Devuelve (grupo_ganador,
    prediccion en los 64 patrones, numero de celdas)."""
    FC = [([i], np.zeros(2)) for i in range(6)]
    FE = [1e9] * 64
    Fmp = np.zeros(6); Fmn = np.zeros(6); Fsp = np.zeros((6, 6)); Fsn = np.zeros((6, 6))
    Fcp = np.zeros(6); Fcn = np.zeros(6); Fhij = []; FG = 0
    for (t, kk, R, _ds) in pre[:n]:
        Pk = pat_de(kk)
        for i in range(6):
            if Pk[i] == 1.0:
                if R > 0: Fmp[i] += 1; Fsp[i] += Pk; Fcp[i] += 1
                else: Fmn[i] += 1; Fsn[i] += Pk; Fcn[i] += 1
        for c in range(len(FC)):
            g, w = FC[c]
            a = np.array([Pk[g[0]], 1.0]) if len(g) == 1 else np.array([Pk[g[0]], Pk[g[1]], Pk[g[0]] * Pk[g[1]], 1.0])
            dc = R - float(w @ a)
            FE[c] = (1 - fis_rho) * FE[c] + fis_rho * dc * dc
            FC[c] = (g, np.clip(w + eta_s * dc * a, -clip_s, clip_s))
        for i in range(6):
            if Pk[i] == 1.0 and i not in Fhij and len(Fhij) < 6 and min(Fmp[i], Fmn[i]) >= fis_umbral:
                cands = [k for k in range(6) if k != i]
                j = max(cands, key=lambda k: abs(Fsp[i][k] / Fcp[i] - Fsn[i][k] / Fcn[i]))
                FC.append(([i, j], np.zeros(4))); Fhij.append(i)
        FG = int(min(range(len(FC)), key=lambda c: FE[c]))
    g, w = FC[FG]
    pred = {}
    for nn in range(64):
        P = np.array([float((nn >> (5 - j)) & 1) for j in range(6)])
        a = np.array([P[g[0]], 1.0]) if len(g) == 1 else np.array([P[g[0]], P[g[1]], P[g[0]] * P[g[1]], 1.0])
        nm = ''.join(str(int(v)) for v in P)
        pred[nm] = float(w @ a)
    return g, pred, len(FC)


def exposiciones(ev, fase2_en, test, vr):
    pre = [e for e in ev if e[0] < fase2_en]
    out = {}
    for n in REJ:
        if n > len(pre):
            out[n] = None
            continue
        _, pred, _ = replay_fision(pre, n)
        out[n] = signo_acc(pred, test, vr)
    return out, len(pre), pre


def n_estrella(expo, crit):
    return next((n for n in REJ if expo.get(n) is not None and expo[n] >= crit), None)


if __name__ == '__main__':
    t0 = time.time()
    filas = []
    for regla in REGLAS:
        for seed in SEEDS:
            r = m.run(seed, **BASE, regla=regla)
            pats, tren, test, vr = m.split_regla(seed, regla)
            acc_lenta = signo_acc(r['W_lenta_apriori'], test, vr)
            expo, npre, pre = exposiciones(r['lenta_eventos'], r['fase2_en'], test, vr)
            n75 = n_estrella(expo, 0.75)
            n65 = n_estrella(expo, 0.65)

            # verificacion de replay: con TODOS los eventos pre-sonda, ¿coincide el grupo ganador del replay
            # con el que el organismo calculo por si mismo en la sonda (r['W_lenta_apriori'] via lenta(P))?
            g_replay, pred_full, ncel_replay = replay_fision(pre, len(pre))
            acc_replay_full = signo_acc(pred_full, test, vr)
            replay_acc_ok = (acc_replay_full == acc_lenta) if (acc_replay_full is not None and acc_lenta is not None) else None

            abre_conjuntivo = len(r['fis_ganadora']) == 2
            fila = dict(regla=regla, seed=seed, acc_lenta=acc_lenta, fis_ganadora=r['fis_ganadora'],
                        fis_n=r['fis_n'], fis_celdas=r['fis_celdas'], abre_conjuntivo=abre_conjuntivo,
                        splits=r['splits'], celdas=r['celdas'], deaths=r['deaths'], n_pre=npre,
                        expo={str(k): v for k, v in expo.items()}, n75=n75, n65=n65,
                        grupo_ganador_replay_n_total=g_replay, celdas_replay_n_total=ncel_replay,
                        acc_replay_n_total=acc_replay_full, replay_coincide_con_organismo=replay_acc_ok)
            filas.append(fila)
            print(f"{regla:5s} s{seed}: acc_lenta={acc_lenta}  fis_ganadora={r['fis_ganadora']}  fis_n={r['fis_n']}  "
                  f"abre_conjuntivo={abre_conjuntivo}  n*(>=.75)={n75}  n*(>=.65)={n65}  "
                  f"splits={r['splits']}  celdas_kenyon={r['celdas']}  deaths={r['deaths']}  n_pre={npre}  "
                  f"replay_full: grupo={g_replay} acc={acc_replay_full} coincide={replay_acc_ok}")

    seg = round(time.time() - t0, 1)
    print(f"\n--- resumen ({seg}s) ---")
    for regla in REGLAS:
        fr = [f for f in filas if f['regla'] == regla]
        accs = [f['acc_lenta'] for f in fr]
        n75s = [f['n75'] for f in fr]
        abre = sum(f['abre_conjuntivo'] for f in fr)
        print(f"{regla:5s}: acc_lenta seeds={accs}  mediana={float(np.median(accs)):.3f}  "
              f"abre_conjuntivo={abre}/{len(fr)}  n*(>=.75) seeds={n75s}")

    out = dict(base=BASE, fis_umbral=FIS_UMBRAL, fis_rho=FIS_RHO, rej=REJ, seeds=SEEDS, reglas=REGLAS,
               filas=filas, segundos=seg)
    with open(os.path.join(AQUI, 'mini_g2.json'), 'w', encoding='utf-8') as f:
        json.dump(out, f, indent=1)
    print('\nescrito mini_g2.json')
