"""mundo_temporal_v8 = mundo_temporal.py (1f447657faf00ef8) + drenaje de la parte comun (lam=0.05, linea
aritmeticamente identica a organismo/organismo_v8.py) + mordida del techo. Generado por
construye_mundo_v8.py. NO editar a mano. Con lam=0 es mundo_temporal.py (control K1).
Preregistro: experimentos/3T_confirmatorio/PREREGISTRO_3T_confirmatorio.md
"""
"""
3T — Mundo que exige ORDEN. Rama exploratoria. NO toca organismo/.

Copia de organismo_v7.py (v6 + regla de division 2L) con UN solo cambio de mundo:
el valor de morder depende de QUE SE MORDIO ANTES.

    morder A con last=='B'  -> comida  R=+1.0  dE=+0.8   (A|B)
    morder A con last=='A'  -> veneno  R=-3.0  dE=-0.4   (A|A)
    morder B (cualquiera)   -> neutro  R= 0.0  dE=+0.1

Cuerpo, patas, politica, hambre, muerte, renovacion, eta/tau_e/alpha/costo: identicos a v6/v7.
Regla 2L (theta=0.6, ema=0.02, paso=0.5, NKMAX=90): identica, sin recalibrar.

Brazos (ver PREREGISTRO.md):
  C1  : NIN=6,  sin plasticidad              (control v6)
  C1p : NIN=6,  con plasticidad              (control: dividir sin canal temporal)
  C2  : NIN=12 visible, sin plasticidad, rechazo hasta code(A|A) n code(A|B)==0   (techo)
  C2b : NIN=12 con columnas temporales a 0, sin plasticidad   (control de instrumento: == C1)
  C3  : NIN=12 con columnas temporales a 0, con plasticidad   (LA PREGUNTA)
  C3C : como C3 pero el canal temporal que VE el organismo es aleatorio (el mundo sigue
        usando el last real para el valor)                    (control de artefacto del clip)

Alineacion del RNG: C1/C1p/C2b/C3/C3C sortean KW como (NK,6) -> mismo flujo -> identicos
hasta la primera division. C3C usa un rng aparte (seed+100000) para el canal falso.
"""
import sys, numpy as np
try: sys.stdout.reconfigure(encoding='utf-8', errors='replace')
except Exception: pass

L = 40; NK = 30; NKMAX = 90; K = 3
PAT = {'A': np.array([1, 1, 0, 1, 0, 0.]), 'B': np.array([1, 0, 1, 0, 1, 0.])}
R_VAL = {'comida': 1.0, 'veneno': -3.0, 'neutro': 0.0}
E_VAL = {'comida': +0.8, 'veneno': -0.4, 'neutro': +0.1}
SIT = [('A', 'A'), ('A', 'B'), ('B', 'A'), ('B', 'B')]   # (actual, anterior)

ARMS = {
    #        nin  temporal_visible  plast  init        canal_falso
    'C1':  dict(nin=6,  plast=False, init='v6',    falso=False),
    'C1p': dict(nin=6,  plast=True,  init='v6',    falso=False),
    'C2':  dict(nin=12, plast=False, init='full',  falso=False),
    'C2b': dict(nin=12, plast=False, init='ciego', falso=False),
    'C3':  dict(nin=12, plast=True,  init='ciego', falso=False),
    'C3C': dict(nin=12, plast=True,  init='ciego', falso=True),
}


def valor(cur, last):
    if cur == 'B': return 'neutro'
    return 'comida' if last == 'B' else 'veneno'


def run(seed, arm='C1', T=100000, learn=True, eta=.03, tau_e=.85, alpha=1.2,
        hambre_boca=2.0, aversion=1.0, costo=.002, nobj=4,
        theta=0.6, ema=0.02, paso=0.5, early=5000, nkmax=NKMAX, wclip=3.0, lam=0.05):
    # nkmax y wclip son parametros SOLO para el diagnostico POST-HOC de los dos
    # confusores preregistrados (agotamiento del pool y saturacion de canales).
    # Con los valores por defecto (90, 3.0) el codigo es identico al congelado en v7:
    # equivalencia verificada campo a campo en las 120 corridas (ver equivalencia.py).
    cfg = ARMS[arm]; NIN = cfg['nin']; plast = cfg['plast']; falso = cfg['falso']
    rng = np.random.default_rng(seed)
    rng2 = np.random.default_rng(seed + 100000)        # canal falso, flujo separado

    Wl = rng.uniform(.1, .4, (2, 9))
    KW = np.zeros((nkmax, NIN)); activa = np.zeros(nkmax, bool); activa[:NK] = True

    def inp(cur, prev):
        return PAT[cur] if NIN == 6 else np.concatenate([PAT[cur], PAT[prev]])

    def code(P):
        v = KW @ P; v = np.where(activa, v, -1e9); return set(np.argsort(v)[-K:])

    # --- inicializacion (muestreo por rechazo) ---
    if cfg['init'] == 'full':                     # C2: 12 columnas aleatorias
        KW[:NK] = rng.uniform(0, 1, (NK, 12))
        while len(code(inp('A', 'A')) & code(inp('A', 'B'))) != 0:
            KW[:NK] = rng.uniform(0, 1, (NK, 12))
    else:                                         # C1/C1p/C2b/C3/C3C: mismo flujo que v6
        KW[:NK, :6] = rng.uniform(0, 1, (NK, 6))
        while len(code(inp('A', 'A')) & code(inp('B', 'B'))) != 0:
            KW[:NK, :6] = rng.uniform(0, 1, (NK, 6))

    def kenyon(P):
        k = np.zeros(nkmax); k[list(code(P))] = 1; return k

    Wp = np.zeros(nkmax); Wn = np.zeros(nkmax)
    err = np.zeros(nkmax); mu = np.zeros((nkmax, NIN))
    el = np.zeros_like(Wl); tr = np.zeros(9)
    pos = 0; E = 1.0; objs = {}; tipos = ['A', 'B']; last = 'B'
    splits = 0; split_t = []; deaths = 0; Rtot = 0.0; t_pool = None
    t_techo = None; n_techo = 0   # mordida del techo (solo lectura)

    def spawn():
        while len(objs) < nobj:
            x = int(rng.integers(L))
            if x not in objs: objs[x] = tipos[int(rng.integers(len(tipos)))]
    spawn()

    q = lambda t: min(t // (T // 4), 3)
    # contadores por cuarto: mordidas por situacion, visitas, mordidas cuyo anterior fue B
    n_AB = [0]*4; n_AA = [0]*4; n_B = [0]*4; prevB = [0]*4; nbit = [0]*4
    vis = {'A': [0]*4, 'B': [0]*4}
    e_AB = e_AA = e_B = e_prevB = e_nbit = 0        # ventana temprana t<early
    snaps = []

    def snapshot(t):
        cods = {f'{c}|{p}': code(inp(c, p)) for c, p in SIT}
        union = set().union(*cods.values())
        wi = float(KW[activa, :6].sum()); wt = float(KW[activa, 6:].sum()) if NIN == 12 else 0.0
        idx = sorted(union)
        wi_c = float(KW[idx, :6].sum()); wt_c = float(KW[idx, 6:].sum()) if NIN == 12 else 0.0
        return dict(t=t, solap_A=len(cods['A|A'] & cods['A|B']),
                    solap_B=len(cods['B|A'] & cods['B|B']),
                    w_inst=round(wi, 3), w_temp=round(wt, 3),
                    rho=round(wt / (wt + wi), 4) if (wt + wi) > 0 else 0.0,
                    w_inst_cod=round(wi_c, 3), w_temp_cod=round(wt_c, 3),
                    rho_cod=round(wt_c / (wt_c + wi_c), 4) if (wt_c + wi_c) > 0 else 0.0,
                    celdas=int(activa.sum()), splits=splits,
                    W={f'{c}|{p}': round(float((Wp - Wn) @ kenyon(inp(c, p))), 3) for c, p in SIT})

    def see():
        best = None
        for x, k in objs.items():
            dl = (pos - x) % L; dr = (x - pos) % L; d = min(dl, dr)
            if best is None or d < best[0]: best = (d, k, dl < dr)
        return best

    hitos = {0, T // 4, T // 2, 3 * T // 4}
    for t in range(T):
        if t in hitos: snaps.append(snapshot(t))
        hambre = np.clip(1 - E, 0, 1); d, k, left = see(); pat = PAT[k]
        x = np.concatenate([pat * 1.2, [1.5 if left else 0, 0 if left else 1.5, 1.0 if d == 0 else 0.]])
        noise = .15 + .5 * hambre
        V = Wl @ x; p = 1 / (1 + np.exp(-(V - .8) / noise)); u = p + rng.normal(0, .3, 2); m = np.zeros(2)
        if u.max() > .5: m[np.argmax(u)] = 1
        tr = tr * .7 + x
        if learn: el = el * tau_e + np.outer(m - p, tr)
        pos = (pos + int(m[1] - m[0])) % L; d2, _, _ = see(); Rp = .2 if d2 < d else 0.
        R = 0.
        if pos in objs:
            kk = objs[pos]
            prev_sent = (('A', 'B')[int(rng2.integers(2))] if falso else last)
            P = inp(kk, prev_sent); kc = kenyon(P); Wb = Wp - Wn
            Vb = alpha * (Wb @ kc) + hambre_boca * hambre + .5
            pb = 1 / (1 + np.exp(-Vb / .3)); mordio = rng.random() < pb
            vis[kk][q(t)] += 1
            if mordio:
                est = valor(kk, last)                        # el MUNDO usa el last real
                R = R_VAL[est]; E = min(E + E_VAL[est], 1.5); Rtot += R
                qq = q(t); nbit[qq] += 1
                if last == 'B': prevB[qq] += 1
                if kk == 'A':
                    (n_AB if last == 'B' else n_AA)[qq] += 1
                else:
                    n_B[qq] += 1
                if t < early:
                    e_nbit += 1
                    if last == 'B': e_prevB += 1
                    if kk == 'A':
                        if last == 'B': e_AB += 1
                        else: e_AA += 1
                    else: e_B += 1
                last = kk
                del objs[pos]; spawn()
                if learn:
                    dlt = R - Wb @ kc
                    if lam: ix=kc>0; mcom=np.minimum(Wp[ix],Wn[ix]); Wp[ix]-=lam*mcom; Wn[ix]-=lam*mcom   # drenaje de la parte comun, identico a organismo_v8
                    _ix = kc > 0
                    if dlt > 0: _trunca = bool(((Wp[_ix] + eta * dlt) > wclip).any())
                    else:       _trunca = bool(((Wn[_ix] + eta * aversion * (-dlt)) > wclip).any())
                    if _trunca:
                        n_techo += 1
                        if t_techo is None: t_techo = t
                    if dlt > 0: Wp = np.clip(Wp + eta * dlt * kc, 0, wclip)
                    else:       Wn = np.clip(Wn + eta * aversion * (-dlt) * kc, 0, wclip)
                    if plast:
                        idx = np.where(kc > 0)[0]
                        err[idx] = (1 - ema) * err[idx] + ema * abs(dlt)
                        mu[idx] = (1 - ema) * mu[idx] + ema * P
                        for c in idx:
                            if err[c] > theta and (~activa).any():
                                j = int(np.where(~activa)[0][0]); activa[j] = True
                                dist = P - mu[c]
                                a1 = float(np.abs(dist).sum())
                                ft = float(np.abs(dist[6:]).sum()) / a1 if (a1 > 0 and NIN == 12) else 0.0
                                KW[j] = np.clip(KW[c] + paso * dist, 0, 5)
                                KW[c] = np.clip(KW[c] - paso * dist, 0, 5)
                                Wp[j] = Wp[c]; Wn[j] = Wn[c]; mu[j] = mu[c].copy()
                                err[c] = err[j] = 0; splits += 1
                                split_t.append((t, kk, prev_sent, round(ft, 3)))
                                if not (~activa).any() and t_pool is None: t_pool = t
        E -= costo
        if rng.random() < .003 and objs:
            del objs[list(objs)[int(rng.integers(len(objs)))]]; spawn()
        if learn: Wl = np.clip(Wl + eta * (1 + 2 * hambre) * (max(R, 0) + Rp) * el, 0, 1.5)
        if E <= 0: deaths += 1; E = .6; pos = int(rng.integers(L))

    snaps.append(snapshot(T))
    fin = snaps[-1]
    acc = [ (n_AB[i] / (n_AB[i] + n_AA[i])) if (n_AB[i] + n_AA[i]) > 0 else None for i in range(4) ]
    base = [ (prevB[i] / nbit[i]) if nbit[i] > 0 else None for i in range(4) ]
    lift = [ (round(acc[i] - base[i], 4) if acc[i] is not None and base[i] is not None else None) for i in range(4) ]
    e_acc = (e_AB / (e_AB + e_AA)) if (e_AB + e_AA) > 0 else None
    e_base = (e_prevB / e_nbit) if e_nbit > 0 else None
    return dict(
        seed=seed, arm=arm,
        W=fin['W'], sep=round(fin['W']['A|B'] - fin['W']['A|A'], 3),
        comp={f'{c}|{p}': (round(float(Wp @ kenyon(inp(c, p))), 3),
                           round(float(Wn @ kenyon(inp(c, p))), 3)) for c, p in SIT},
        solap_A=fin['solap_A'], solap_B=fin['solap_B'],
        solap_A_q=[s['solap_A'] for s in snaps],
        rho_q=[s['rho'] for s in snaps], rho_cod_q=[s['rho_cod'] for s in snaps],
        w_temp_q=[s['w_temp'] for s in snaps], w_inst_q=[s['w_inst'] for s in snaps],
        n_AB=n_AB, n_AA=n_AA, n_B=n_B, vis=vis, nbit=nbit, prevB=prevB,
        acc=[round(a, 4) if a is not None else None for a in acc],
        base=[round(b, 4) if b is not None else None for b in base], lift=lift,
        early=dict(n_AB=e_AB, n_AA=e_AA, n_B=e_B, nbit=e_nbit,
                   acc=round(e_acc, 4) if e_acc is not None else None,
                   base=round(e_base, 4) if e_base is not None else None,
                   lift=round(e_acc - e_base, 4) if (e_acc is not None and e_base is not None) else None),
        splits=splits, celdas=fin['celdas'], t_pool=t_pool, split_t=split_t,
        deaths=deaths, Rtot=round(Rtot, 2), E_fin=round(float(E), 3), snaps=snaps,
        t_techo=t_techo, n_techo=n_techo, lam=lam)


if __name__ == '__main__':
    import json
    print(json.dumps({k: run(1, k, T=20000)['W'] for k in ARMS}, indent=1))
