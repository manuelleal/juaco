"""Mini-prueba de UN proceso (enjambre/grupo1, mecanismo M1): identidad ya OK (identidad_g1.py, 23/23).
Semillas 1-3, T=100000, mundo='regla', puerta=3, regla_lenta='delta_signo', constante=True, lam_lenta=0.0,
eta_s=0.15, clip_s=10 (constantes v14.1 / A-4), lectura='cuadratica', celdas='par2', cel_rho=0.02 (default).
Sin Pool. Reglas: xor01, px0, azar.

Mide, por (regla, semilla):
  - acc_lenta = signo_acc(W_lenta_apriori, test, vr): acierto balanceado por SIGNO en los patrones de TEST,
    nunca vistos en el tren, usando la via lenta SOLA (formula del registro, igual que corre_xor_4.py/
    mini_prueba_A_ganadora.py).
  - acc = signo_acc(W_apriori, test, vr): el valor TOTAL (rapida+lenta con puerta), de referencia.
  - cel_ganadora: el par (i,j) que gano en la sonda a priori (via `cel_ganadora` del organismo).
  - EXPOSICIONES hasta 0.75: se recosecha con lab=True (celda encendida) -- NO se reusa el replay viejo
    cosechado bajo la regla_lenta='delta_signo' estandar (ese flujo cambia con la perilla encendida, la via
    lenta alimenta la boca). Se repite offline, evento a evento, la MISMA regla_local de organismo_g1.py
    (control_que_puede_fallar #1 del mecanismo) sobre los eventos (t,patron,R) pre-sonda grabados por el
    organismo mismo en ESTA corrida, y se AUTO-COMPRUEBA contra el acc_lenta real del organismo (igual que
    banco_lab.py): el replay completo debe reproducir W_lenta_apriori exactamente.

OJO (ERR-28): organismo/ va PRIMERO en sys.path, siempre.
Uso: python mini_g1.py
"""
import json, os, sys, time
import numpy as np

sys.stdout.reconfigure(encoding='utf-8', errors='replace')
AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.abspath(os.path.join(AQUI, '..', '..', '..'))
sys.path[:0] = [os.path.join(RAIZ, 'organismo'), AQUI]   # ERR-28: organismo/ PRIMERO

import organismo_g1 as G1

T = 100000
SEEDS = [1, 2, 3]
REGLAS = ['xor01', 'px0', 'azar']
BASE = dict(T=T, mundo='regla', puerta=3, lectura='cuadratica', regla_lenta='delta_signo', constante=True,
            lam_lenta=0.0, eta_s=0.15, clip_s=10.0, celdas='par2', cel_rho=0.02, lab=True)
_PAR = [(i, j) for i in range(6) for j in range(i + 1, 6)]
REJ_BASE = [10, 20, 40, 60, 100, 150, 200, 300, 400, 600]


def signo_acc(Wd, test, vr):
    """Acierto BALANCEADO por signo sobre los nunca vistos. Empate exacto = 0.5. La formula del registro."""
    f = [1.0 if Wd[k] > 0 else (0.5 if Wd[k] == 0 else 0.0) for k in test if vr[k] == 'comida']
    p = [1.0 if Wd[k] < 0 else (0.5 if Wd[k] == 0 else 0.0) for k in test if vr[k] == 'veneno']
    if not f or not p:
        return None
    return 0.5 * float(np.mean(f)) + 0.5 * float(np.mean(p))


def replay_regla_local(pre_eventos, pats, eta_s, clip_s, cel_rho, checkpoints):
    """Repite OFFLINE, evento a evento, la regla_local exacta de organismo_g1.py (anclas 2/3/4).
    Devuelve {n: {pat: lenta(pat)}} en cada n de `checkpoints` (tras procesar los primeros n eventos)."""
    CW = np.zeros((15, 4)); CE = np.full(15, 1e9); CG = 0
    out = {}
    cps = sorted(set(c for c in checkpoints if c <= len(pre_eventos)))
    ci = 0
    for idx, (t, kk, R, ds) in enumerate(pre_eventos, start=1):
        P = pats[kk]
        A = np.array([[P[i], P[j], P[i] * P[j], 1.0] for i, j in _PAR])
        dc = R - (CW * A).sum(axis=1); dc2 = dc * dc
        CE = np.where(CE >= 1e9, dc2, (1 - cel_rho) * CE + cel_rho * dc2)
        CW = np.clip(CW + eta_s * dc[:, None] * A, -clip_s, clip_s)
        CG = int(np.argmin(CE))
        while ci < len(cps) and cps[ci] == idx:
            i, j = _PAR[CG]
            out[idx] = dict(cel_ganadora=[i, j],
                             lenta={k: float(CW[CG] @ np.array([p[i], p[j], p[i] * p[j], 1.0])) for k, p in pats.items()})
            ci += 1
    # snapshot final (todos los eventos), para la auto-comprobacion, aunque no caiga en `checkpoints`
    if pre_eventos:
        i, j = _PAR[CG]
        out['final'] = dict(cel_ganadora=[i, j],
                             lenta={k: float(CW[CG] @ np.array([p[i], p[j], p[i] * p[j], 1.0])) for k, p in pats.items()})
    else:
        out['final'] = dict(cel_ganadora=None, lenta={k: 0.0 for k in pats})
    return out


if __name__ == '__main__':
    print(f"organismo_g1.py sha {__import__('hashlib').sha256(open(G1.__file__,'rb').read()).hexdigest()[:16]}")
    print(f"BASE = {BASE}\n")
    filas = []
    t00 = time.time()
    for regla in REGLAS:
        for s in SEEDS:
            t0 = time.time()
            r = G1.run(s, **BASE, regla=regla)
            seg = time.time() - t0
            pats, tren, test, vr = G1.split_regla(s, regla)
            al = signo_acc(r['W_lenta_apriori'], test, vr)
            ac = signo_acc(r['W_apriori'], test, vr)
            pre = [e for e in r['lenta_eventos'] if e[0] < r['fase2_en']]
            npre = len(pre)
            # -- clases presentes en TREN (para el techo declarado por el jefe: control #6)
            clases_tren = set(vr[k] for k in tren)
            techo_tren = len(clases_tren) < 2

            # -- REJ dinamico: si con 600 no alcanza, extender hasta cubrir todos los eventos pre-sonda
            rej = list(REJ_BASE)
            nx = 600
            while nx < npre:
                nx = int(nx * 1.5); rej.append(min(nx, npre))
            rej = sorted(set(x for x in rej if x <= npre))

            rep = replay_regla_local(pre, pats, BASE['eta_s'], BASE['clip_s'], BASE['cel_rho'], rej)

            # -- auto-comprobacion (control #1 del mecanismo): el replay COMPLETO debe reproducir W_lenta_apriori
            auto_ok = None; auto_maxdif = None
            if npre > 0:
                lf = rep['final']['lenta']
                difs = [abs(lf[k] - r['W_lenta_apriori'][k]) for k in r['W_lenta_apriori']]
                auto_maxdif = max(difs); auto_ok = auto_maxdif < 1e-6
                cg_ok = rep['final']['cel_ganadora'] == r['cel_ganadora']
            else:
                cg_ok = (r['cel_ganadora'] is None)

            curva = []
            for n in rej:
                al_n = signo_acc(rep[n]['lenta'], test, vr)
                curva.append((n, al_n, tuple(rep[n]['cel_ganadora'])))
            n75 = next((n for n, x, _ in curva if x is not None and x >= 0.75), None)
            n65 = next((n for n, x, _ in curva if x is not None and x >= 0.65), None)

            abre_01 = (r['cel_ganadora'] == [0, 1])
            filas.append(dict(regla=regla, seed=s, acc_lenta=al, acc=ac, npre=npre,
                               cel_ganadora=r['cel_ganadora'], abre_01=abre_01,
                               techo_tren=techo_tren, clases_tren=sorted(clases_tren),
                               n75=n75, n65=n65, curva=curva,
                               auto_ok=auto_ok, auto_maxdif=auto_maxdif, cg_ok=cg_ok, seg=round(seg, 1)))
            print(f"  {regla:6s} s{s}: acc_lenta={al}  acc={ac}  cel_ganadora={r['cel_ganadora']}  "
                  f"abre(0,1)={abre_01}  techo_tren={techo_tren}({sorted(clases_tren)})  "
                  f"n_pre={npre}  n*(>=.75)={n75 or '>' + str(rej[-1] if rej else 0)}  "
                  f"n*(>=.65)={n65 or '>' + str(rej[-1] if rej else 0)}  "
                  f"auto_replay_ok={auto_ok}(maxdif={auto_maxdif})  cg_replay_ok={cg_ok}  ({seg:.1f}s)", flush=True)
            print(f"      curva: {[(n, None if x is None else round(x,3)) for n,x,_ in curva]}", flush=True)

    out = dict(BASE={k: v for k, v in BASE.items()}, filas=filas)
    fjson = os.path.join(AQUI, 'mini_g1.json')
    json.dump(out, open(fjson, 'w', encoding='utf-8'), indent=1, default=str)
    print(f"\n-> {fjson}")

    print(f"\n--- resumen por regla (mediana de {len(SEEDS)} semillas) ---")
    for regla in REGLAS:
        fr = [f for f in filas if f['regla'] == regla]
        al = [f['acc_lenta'] for f in fr if f['acc_lenta'] is not None]
        print(f"  {regla:6s} acc_lenta mediana={np.median(al) if al else None}  min={min(al) if al else None}  "
              f"max={max(al) if al else None}  abre(0,1)={sum(f['abre_01'] for f in fr)}/{len(fr)}  "
              f"techo_tren={sum(f['techo_tren'] for f in fr)}/{len(fr)}  "
              f"auto_replay_ok={sum(bool(f['auto_ok']) for f in fr)}/{len(fr)}")
    print(f"\ntotal {time.time()-t00:.1f}s")
