"""
organismo_3k.py - RAMA EXPLORATORIA 3K (Kenyon aprendido). NO es tronco. NO toca organismo/.

Base literal: organismo/organismo_v6.py (hash 5f38f83cf49248a3).
Tres cambios declarados, ninguno de ellos activo con los kwargs por defecto:

 A) mundo='regla'  (por defecto 'AB' = v6 exacto)
    Retina de 6 px. Universo = los 20 patrones con EXACTAMENTE 3 px activos
    (control de luminancia: todos los patrones tienen la misma energia de entrada,
    de modo que la clase no se puede leer del brillo total).
    La valencia la decide UN pixel: px[0]==1 -> comida, px[0]==0 -> veneno.
    10 patrones de entrenamiento (5 comida + 5 veneno) durante la fase 1.
    Los otros 10 (5+5), NUNCA vistos, entran en el mundo en t=fase2_en.
    NO hay muestreo por rechazo de KW: con 20 patrones x 3 celdas sobre 30 celdas
    es imposible exigir solapamiento 0, y ademas el solapamiento accidental es
    justo el objeto de estudio.

 B) kenyon_mode: 'fijo' | 'hebb_visita' | 'hebb_mordida' | 'error'
    Regla LOCAL, sin gradiente y sin backprop. Cuando una celda gana (esta en el
    top-K del patron actual) su vector de entrada se acerca al patron:
        KW[i] <- KW[i] + lr*(P - KW[i])
        KW[i] <- KW[i] * n0[i]/||KW[i]||       (renormalizacion a la norma de nacimiento)
    Preservar la norma de nacimiento hace que en t=0 los codigos sean IDENTICOS a
    los de v6 en las cuatro condiciones: solo cambia la direccion aprendida, no la
    ganancia sorteada de cada celda.
      'fijo'         : lr=0. KW nunca cambia. = v6.
      'hebb_visita'  : actualiza en cada VISITA (la boca codifica el patron), lr=k_lr.
      'hebb_mordida' : actualiza solo al MORDER, lr=k_lr.
      'error'        : actualiza solo al MORDER, lr = k_lr*min(|delta|/k_scale, 1)
                       con delta = R - (Wp-Wn)@kc, el mismo error de prediccion que
                       usa la regla 2L para decidir cuando dividir.

 C) Instrumentacion inerte: W a priori de los 64/20 patrones en t=fase2_en (antes de
    que el organismo haya visto jamas los patrones de test), KW inicial y final,
    codigos, y conteos vis/mord en 8 bins (4 por fase).

Con mundo='AB' y kenyon_mode='fijo' este codigo es BIT-IDENTICO a organismo_v6.run():
no anade ni reordena una sola llamada al RNG. Verificado en equivalencia_3k.py.
"""
import itertools
import numpy as np

L = 40; NK = 30; K = 3
PAT_AB = {'A': np.array([1, 1, 0, 1, 0, 0.]), 'B': np.array([1, 0, 1, 0, 1, 0.]),
          'C': np.array([0, 1, 1, 0, 0, 1.]), 'D': np.array([0, 0, 1, 0, 1, 1.])}
R_VAL = {'comida': 1.0, 'veneno': -3.0}
E_VAL = {'comida': +0.8, 'veneno': -0.4}

PX_REL = 0          # pixel que decide la valencia
N_ACT = 3           # pixeles activos por patron (control de luminancia)


def patrones_regla(n_act=N_ACT):
    """Los C(6,3)=20 patrones binarios de 6 px con exactamente n_act px activos."""
    pats = {}
    for combo in itertools.combinations(range(6), n_act):
        v = np.zeros(6)
        v[list(combo)] = 1.
        pats[''.join('1' if v[j] else '0' for j in range(6))] = v
    return pats


def valencia_regla(nombre, px=PX_REL):
    return 'comida' if nombre[px] == '1' else 'veneno'


def split_regla(seed, px=PX_REL):
    """Particion entrenamiento/test, 5+5 por clase, sorteada con un RNG PROPIO
    (10_000+seed) para que sea IDENTICA en las cuatro condiciones de la misma semilla
    y para que el resultado no dependa de una unica particion arbitraria."""
    pats = patrones_regla()
    food = sorted([k for k in pats if valencia_regla(k, px) == 'comida'])
    pois = sorted([k for k in pats if valencia_regla(k, px) == 'veneno'])
    r = np.random.default_rng(10_000 + seed)
    fi = r.permutation(len(food)); pi = r.permutation(len(pois))
    food = [food[i] for i in fi]; pois = [pois[i] for i in pi]
    n = len(food) // 2
    tren = sorted(food[:n] + pois[:n])
    test = sorted(food[n:] + pois[n:])
    return pats, tren, test


def run(seed, T=100000, learn=True,
        mundo='AB', kenyon_mode='fijo', k_lr=0.0, k_scale=3.0,
        fase2_en=None, congelar_fase2=False,
        invertir_en=None, nuevo=None, nuevo_en=50000, nuevo_val='veneno', solap_B=None,
        eta=.03, tau_e=.85, alpha=1.2, hambre_boca=2.0, aversion=1.0, costo=.002,
        nobj=4, log_cada=None):

    # ---------------- mundo ----------------
    if mundo == 'AB':
        PAT = PAT_AB
        tipos = ['A', 'B']
        val = {'A': 'comida', 'B': 'veneno'}
        tren = ['A', 'B']; test = []
    elif mundo == 'regla':
        PAT, tren, test = split_regla(seed)
        tipos = list(tren)
        val = {k: valencia_regla(k) for k in PAT}
        if fase2_en is None:
            fase2_en = T // 2
    else:
        raise ValueError(mundo)

    rng = np.random.default_rng(seed)
    Wl = rng.uniform(.1, .4, (2, 9)); KW = rng.uniform(0, 1, (NK, 6))

    def codeidx(P): return np.argsort(KW @ P)[-K:]
    def code(P): return set(codeidx(P))

    if mundo == 'AB':
        cond = lambda: len(code(PAT['A']) & code(PAT['B'])) == 0 and (
            nuevo is None or solap_B is None or
            (len(code(PAT[nuevo]) & code(PAT['B'])) == solap_B and
             len(code(PAT[nuevo]) & code(PAT['A'])) == 0))
        while not cond():
            KW = rng.uniform(0, 1, (NK, 6))

    KW0 = KW.copy()
    n0 = np.linalg.norm(KW, axis=1)          # norma de nacimiento de cada fila

    def kenyon(P):
        k = np.zeros(NK); k[list(code(P))] = 1; return k

    def kw_update(P, idx, lr):
        """Regla local de aprendizaje competitivo. In-place sobre KW. Cero RNG."""
        if lr <= 0:
            return
        KW[idx] += lr * (P - KW[idx])
        nn = np.linalg.norm(KW[idx], axis=1)
        KW[idx] *= (n0[idx] / np.maximum(nn, 1e-12))[:, None]

    Wp = np.zeros(NK); Wn = np.zeros(NK); el = np.zeros_like(Wl); tr = np.zeros(9)
    pos = 0; E = 1.0; objs = {}

    def spawn():
        while len(objs) < nobj:
            x = int(rng.integers(L))
            if x not in objs:
                objs[x] = tipos[int(rng.integers(len(tipos)))]
    spawn()

    if mundo == 'AB':
        nb = 4
        qbin = lambda t: min(t // (T // 4), 3)
    else:
        nb = 8
        f2 = fase2_en; d1 = max(f2 // 4, 1); d2 = max((T - f2) // 4, 1)
        qbin = lambda t: (min(t // d1, 3) if t < f2 else 4 + min((t - f2) // d2, 3))

    mord = {k: [0] * nb for k in PAT}; vis = {k: [0] * nb for k in PAT}
    deaths = 0; log = []
    W_apriori = None; codes_f2 = None; KW_f2 = None
    splits_dummy = 0  # no hay plasticidad estructural en esta rama

    def see():
        best = None
        for x, k in objs.items():
            dl = (pos - x) % L; dr = (x - pos) % L; d = min(dl, dr)
            if best is None or d < best[0]:
                best = (d, k, dl < dr)
        return best

    for t in range(T):
        if invertir_en is not None and t == invertir_en:
            val = {'A': 'veneno', 'B': 'comida'}
        if nuevo is not None and t == nuevo_en:
            tipos.append(nuevo); val[nuevo] = nuevo_val
        if mundo == 'regla' and t == fase2_en:
            # SONDA: valor a priori de TODOS los patrones ANTES de que los de test existan
            Wb0 = Wp - Wn
            W_apriori = {k: float(Wb0 @ kenyon(PAT[k])) for k in PAT}
            codes_f2 = {k: sorted(int(i) for i in code(PAT[k])) for k in PAT}
            KW_f2 = KW.copy()
            for k in test:
                tipos.append(k)

        aprende = learn and not (mundo == 'regla' and congelar_fase2 and t >= fase2_en)

        hambre = np.clip(1 - E, 0, 1); d, k, left = see(); pat = PAT[k]
        x = np.concatenate([pat * 1.2, [1.5 if left else 0, 0 if left else 1.5, 1.0 if d == 0 else 0.]])
        noise = .15 + .5 * hambre
        V = Wl @ x; p = 1 / (1 + np.exp(-(V - .8) / noise)); u = p + rng.normal(0, .3, 2)
        m = np.zeros(2)
        if u.max() > .5:
            m[np.argmax(u)] = 1
        tr = tr * .7 + x
        if aprende:
            el = el * tau_e + np.outer(m - p, tr)
        pos = (pos + int(m[1] - m[0])) % L
        d2_, _, _ = see(); Rp = .2 if d2_ < d else 0.
        R = 0.
        if pos in objs:
            kk = objs[pos]; idx = codeidx(PAT[kk])
            kc = np.zeros(NK); kc[idx] = 1
            Wb = Wp - Wn
            Vb = alpha * (Wb @ kc) + hambre_boca * hambre + .5
            pb = 1 / (1 + np.exp(-Vb / .3)); mordio = rng.random() < pb
            vis[kk][qbin(t)] += 1
            if aprende and kenyon_mode == 'hebb_visita':
                kw_update(PAT[kk], idx, k_lr)
            if mordio:
                R = R_VAL[val[kk]]; E = min(E + E_VAL[val[kk]], 1.5); mord[kk][qbin(t)] += 1
                del objs[pos]; spawn()
                if aprende:
                    dlt = R - Wb @ kc
                    if kenyon_mode == 'hebb_mordida':
                        kw_update(PAT[kk], idx, k_lr)
                    elif kenyon_mode == 'error':
                        kw_update(PAT[kk], idx, k_lr * min(abs(float(dlt)) / k_scale, 1.0))
                    if dlt > 0:
                        Wp = np.clip(Wp + eta * dlt * kc, 0, 3.)
                    else:
                        Wn = np.clip(Wn + eta * aversion * (-dlt) * kc, 0, 3.)
        E -= costo
        if rng.random() < .003 and objs:
            del objs[list(objs)[int(rng.integers(len(objs)))]]; spawn()
        if aprende:
            Wl = np.clip(Wl + eta * (1 + 2 * hambre) * (max(R, 0) + Rp) * el, 0, 1.5)
        if E <= 0:
            deaths += 1; E = .6; pos = int(rng.integers(L))
        if log_cada and mundo == 'AB' and t % log_cada == 0:
            log.append((t,) + tuple(round(float((Wp - Wn) @ kenyon(PAT[k])), 2) for k in 'ABCD'))

    W = {k: round(float((Wp - Wn) @ kenyon(PAT[k])), 2) for k in PAT}
    comp = {k: (round(float(Wp @ kenyon(PAT[k])), 2), round(float(Wn @ kenyon(PAT[k])), 2)) for k in PAT}
    out = dict(mord=mord, vis=vis, W=W, comp=comp, deaths=deaths, log=log,
               solap={'AB': len(code(PAT['A']) & code(PAT['B'])) if mundo == 'AB' else None,
                      'nB': len(code(PAT[nuevo]) & code(PAT['B'])) if (mundo == 'AB' and nuevo) else None})
    if mundo == 'regla':
        out.update(tren=tren, test=test, fase2_en=fase2_en,
                   W_apriori=W_apriori, W_final={k: float((Wp - Wn) @ kenyon(PAT[k])) for k in PAT},
                   codes_f2=codes_f2, codes_fin={k: sorted(int(i) for i in code(PAT[k])) for k in PAT},
                   codes_0={k: sorted(int(i) for i in np.argsort(KW0 @ PAT[k])[-K:]) for k in PAT},
                   KW0=KW0, KW=KW.copy(), KW_f2=KW_f2, Wp=Wp, Wn=Wn)
    return out
