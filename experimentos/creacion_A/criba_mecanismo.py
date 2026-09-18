"""CREADOR A — CRIBA BARATA de mecanismos de creacion/seleccion del rasgo conjuntivo (bloque 3/3).

Regla: **antes de gastar un preregistro, el mecanismo tiene que proponer `P0*P1` en >= 15/20 semillas.**
Cuesta ~2 s con el gemelo compilado. Ya cribo aqui todo lo que he probado, y deja un punto de entrada
(`registra`) para meter los mecanismos de la sala (ENJAMBRE_xor_20260918.md) sin tocar nada mas.

Un mecanismo es una funcion  f(ctx) -> vector de 15 marcadores (uno por par de pixeles, orden `_IJ`),
mayor = mas propuesto. `ctx` trae TODO lo que el organismo tiene disponible localmente antes de la sonda:
    ctx['tren']    nombres de los patrones de tren            ctx['X']   phi cuadratica+cte de los de tren
    ctx['y']       recompensa R de cada patron de tren        ctx['res'] residuo del ajuste elemental EXACTO
    ctx['eventos'] secuencia (t, patron, R, residuo) grabada por `lab=True`  (muestreo real, con repeticiones)
    ctx['splits']  eventos de fision (t, patron) antes de la sonda
    ctx['pats']    los 20 patrones del mundo   ctx['vr'] sus valencias   ctx['test'] los nunca vistos
**Desempate AL AZAR obligatorio** (con `nan` para "no elegible"): el empate resuelto por el orden del indice ya me
colo un 17/20 falso una vez (ver mi seccion A13 del PUENTE).

Uso:  python criba_mecanismo.py            (criba los mecanismos ya registrados)
      python criba_mecanismo.py --ntr 8,6  (la misma criba con 14 patrones de tren, como control)
Sin Pool.
"""
import sys, os, json
import numpy as np

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path[:0] = [AQUI, os.path.join(AQUI, '..', 'nivel7_xor_lectura')]
import organismo_v13q as O
from identificabilidad_xor import phi, signo_acc, R_VAL

IJ = [(i, j) for i in range(6) for j in range(i + 1, 6)]
NOM = [f'{i}x{j}' for i, j in IJ]
IDX_OK = 0                      # `0x1` = P0*P1, el unico que generaliza
MECANISMOS = {}


def registra(nombre):
    def deco(f):
        MECANISMOS[nombre] = f; return f
    return deco


# ------------------------------------------------------------------ mecanismos ya cribados (todos mios)
@registra('residuo (cascade-correlation, estadistico IDEAL)')
def m_residuo(c):
    return np.array([abs(float(c['res'][c['X'][:, 6 + j] > 0].mean())) if (c['X'][:, 6 + j] > 0).any() else np.nan
                     for j in range(15)])


@registra('fision de v11 (mi ruta 2)')
def m_fision(c):
    v = np.zeros(15)
    for _t, k in c['splits']:
        act = [i for i in range(6) if k[i] == '1']
        for a in range(len(act)):
            for b in range(a + 1, len(act)):
                v[IJ.index((act[a], act[b]))] += 1
    return np.where(v > 0, v, np.nan)


@registra('pureza del refuerzo bajo el par (unique cue), nmin=2')
def m_pureza(c):
    out = np.full(15, np.nan)
    for j in range(15):
        m = c['X'][:, 6 + j] > 0
        if int(m.sum()) >= 2: out[j] = -float(np.var(c['y'][m]))
    return out


@registra('media del refuerzo bajo el par, nmin=2')
def m_media(c):
    out = np.full(15, np.nan)
    for j in range(15):
        m = c['X'][:, 6 + j] > 0
        if int(m.sum()) >= 2: out[j] = abs(float(c['y'][m].mean()))
    return out


@registra('[control] azar')
def m_azar(c):
    return c['rng'].random(15)


# ------------------------------------------------------------------ el arnes de la criba
def contexto(seed, ntr=None, rng=None, con_splits=True):
    pats = O.patrones_regla(); nombres = sorted(pats)
    vr = {k: ('comida' if k[0] != k[1] else 'veneno') for k in nombres}
    if ntr is None:
        _, tren, test, vr = O.split_regla(seed, 'xor01')
    else:
        r = np.random.default_rng(10000 + seed)
        f = [k for k in nombres if vr[k] == 'comida']; p = [k for k in nombres if vr[k] == 'veneno']
        f = [f[i] for i in r.permutation(len(f))][:ntr[0]]; p = [p[i] for i in r.permutation(len(p))][:ntr[1]]
        tren = sorted(f + p); test = [k for k in nombres if k not in tren]
    F = {k: phi(pats[k], 'cuadratica', True) for k in nombres}
    X = np.array([F[k] for k in tren]); y = np.array([R_VAL[vr[k]] for k in tren])
    Xe = X[:, list(range(6)) + [21]]; res = y - Xe @ (np.linalg.pinv(Xe) @ y)
    ev, sp = [], []
    if con_splits and ntr is None:
        import organismo_v13q5_rapido as R
        r = R.run(seed, T=100000, mundo='regla', regla='xor01', lectura='cuadratica', constante=True,
                  regla_lenta='delta_signo', lam_lenta=0.0, eta_s=0.15, clip_s=10.0, puerta=3, lab=True)
        f2 = r['fase2_en']
        ev = [e for e in r['lenta_eventos'] if e[0] < f2]; sp = [(t, k) for t, k in r['split_t'] if t < f2]
    return dict(seed=seed, tren=tren, test=test, vr=vr, pats=pats, F=F, X=X, y=y, res=res,
                eventos=ev, splits=sp, rng=rng or np.random.default_rng(seed))


def criba(f, seeds, ntx):
    gana = 0; accs = []; emp = []
    for s in seeds:
        c = ntx[s]
        sc = np.asarray(f(c), float)
        if np.all(np.isnan(sc)):
            accs.append(None); emp.append(15); continue
        mx = np.nanmax(sc); cand = [j for j in range(15) if not np.isnan(sc[j]) and sc[j] >= mx - 1e-12]
        j = int(c['rng'].choice(cand)); emp.append(len(cand))
        gana += int(j == IDX_OK)
        idx = list(range(6)) + [21, 6 + j]
        w = np.linalg.pinv(c['X'][:, idx]) @ c['y']
        accs.append(signo_acc({k: float(c['F'][k][idx] @ w) for k in c['pats']}, c['test'], c['vr']))
    a = [x for x in accs if x is not None]
    return gana, (round(float(np.median(a)), 3) if a else None), float(np.median(emp))


if __name__ == '__main__':
    ntr = None
    if '--ntr' in sys.argv:
        ntr = tuple(int(x) for x in sys.argv[sys.argv.index('--ntr') + 1].split(','))
    seeds = list(range(1, 21))
    rng = np.random.default_rng(12345)
    ntx = {s: contexto(s, ntr, rng) for s in seeds}
    n_tren = len(ntx[seeds[0]]['tren'])
    print(f"=== CRIBA del bloque 3/3 — {n_tren} patrones de tren, {len(seeds)} semillas, desempate al azar ===")
    print(f"    umbral para pasar: `P0*P1` propuesto en >= 15/20")
    print(f'{"mecanismo":>48} {"gana P0*P1":>11} {"acc si se abre":>15} {"empatados":>10} {"pasa":>5}')
    res = {}
    for nom, f in MECANISMOS.items():
        g, a, e = criba(f, seeds, ntx)
        res[nom] = dict(gana=g, acc=a, empatados=e, pasa=bool(g >= 15))
        print(f'{nom:>48} {g:>8}/20 {str(a):>15} {e:>10} {"SI" if g >= 15 else "no":>5}')
    json.dump(dict(n_tren=n_tren, ntr=ntr, semillas=seeds, resultados=res),
              open(os.path.join(AQUI, f'criba_{n_tren}.json'), 'w'), indent=1)
    print(f'\n-> criba_{n_tren}.json   (para meter un mecanismo de la sala: @registra("nombre") sobre una funcion '
          f'f(ctx) -> 15 marcadores)')
