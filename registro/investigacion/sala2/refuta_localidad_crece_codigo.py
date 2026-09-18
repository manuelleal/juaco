"""REFUTADOR sala 2 (lente localidad/consistencia) -- replay de SOLO la via lenta del diseno DISENO_crece_codigo.md.
NO es el organismo: no hay cuerpo, ni Kenyon, ni mundo. Transcribe literalmente las reglas del pseudocodigo (Ancla B y E:
_lin, _cas, _lector, _lenta, _nace, _crece_paso; la lineal de v14.1 L117-L120 con eta_s=0.15, clip_s=10, lam=0.05) y las
alimenta con una secuencia de mordidas sobre los 8 patrones de tren de xor01 (split_regla de organismo_v14g, solo lectura).
Pregunta unica: con g_theta=1.5, g_rec=2, g_min_vis=6, g_rho=0.02, ¿un nodo reclutado puede llegar a LEER (relevo exige
_GE[n] < _EL) antes de que la poda lo mate a la 6.a mordida, dado que nace con _GE = (R-_lb)^2 (el error del padre en la sorpresa)?
Dos regimenes de mordida (ambos favorables al diseno en distinto sentido): 'siempre' (muerde todo encuentro: mas mordidas de
veneno, _EL mas alto) y 'boca' (pb de la boca de v14.1 con hambre=1: 0.025 a lectura -3, el regimen del registro).
Dos brazos: CRECE y FIJO15 (mismo lector y poda, sin reclutamiento; §4.2 lo llama 'v15f dentro de este instrumento').
Un proceso, sin Pool, ~segundos. Salida: refuta_localidad_crece_codigo.json (esta carpeta).
Uso: python refuta_localidad_crece_codigo.py [desde=1101] [n=20] [mordidas=300]
"""
import sys, os, json
import numpy as np
AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(AQUI)))
sys.path[:0] = [os.path.join(RAIZ, 'organismo')]   # organismo/ PRIMERO (ERR-28)
import organismo_v14g as G

R_VAL = {'comida': 1.0, 'veneno': -3.0}
ETA_S, CLIP_S, LAM = 0.15, 10.0, 0.05
G_THETA, G_REC, G_MAX, G_MIN_VIS, G_RHO = 1.5, 2, 15, 6, 0.02


def replay(seed, regimen, brazo, n_mord):
    pats, tren, test, vr = G.split_regla(seed, 'xor01')
    P_ = {k: pats[k] for k in pats}
    rng_m = np.random.default_rng(seed)                 # secuencia de encuentros (sustituye al mundo)
    Wps = np.zeros(6); Wns = np.zeros(6)
    _PAR = [(i, j) for i in range(6) for j in range(i + 1, 6)]
    _GP = [None] * G_MAX; _GA = np.zeros(G_MAX, bool); _GT = np.zeros((G_MAX, 4)); _GV = np.zeros((G_MAX, 4), int)
    _GE = np.full(G_MAX, np.inf); _GN = np.zeros(G_MAX, int); _GQ = np.zeros(G_MAX); _GS = np.zeros((6, 6)); _EL = np.inf
    _rg = np.random.default_rng(seed + 800000)
    st = dict(reclutas=0, podas=0, podas_a_6=0, nacidos_leyeron=0, nacidos=[], leyo=set(), lecturas_nodo=0, lecturas_lineal=0,
              nace_GE_mayor_EL=0, sorpresas=0)

    def _lin(P): return float((Wps - Wns) @ P)
    def _cas(P, i, j): return int(P[i]) * 2 + int(P[j])
    def _lector(P):
        best = None; m = np.inf; emp = 0
        for n in np.flatnonzero(_GA):
            i, j = _GP[n]; c = _cas(P, i, j)
            if _GV[n, c] == 0 or not (_GE[n] < _EL): continue
            if _GE[n] < m - 1e-12: best = int(n); m = float(_GE[n]); emp = 1
            elif abs(_GE[n] - m) <= 1e-12:
                emp += 1
                if _GQ[n] > _GQ[best]: best = int(n)
        return best, emp
    def _lenta(P):
        n, emp = _lector(P)
        if n is None: return _lin(P), None
        i, j = _GP[n]; return float(_GT[n, _cas(P, i, j)]), n
    def _nace(i, j, P, R, _lb):
        nonlocal _EL
        n = int(np.flatnonzero(~_GA)[0]); _GA[n] = True; _GP[n] = (i, j); _GT[n] = 0.; _GV[n] = 0
        _GT[n, _cas(P, i, j)] = R; _GV[n, _cas(P, i, j)] = 1
        _GE[n] = (R - _lb) ** 2; _GN[n] = 1; _GQ[n] = float(_rg.random()); _GS[i, j] = 0.
        st['nacidos'].append(dict(par=(i, j), GE0=round(float(_GE[n]), 3), EL=round(float(_EL), 3), mordida=t_m))
        if _GE[n] >= _EL: st['nace_GE_mayor_EL'] += 1
        return n
    if brazo == 'fijo15':
        for (i, j) in _PAR:
            n = int(np.flatnonzero(~_GA)[0]); _GA[n] = True; _GP[n] = (i, j); _GQ[n] = float(_rg.random())

    def _crece_paso(P, R, _ws_boca, _lb):
        nonlocal _EL
        e = R - _ws_boca
        el = (R - _lb) ** 2; _EL = el if not np.isfinite(_EL) else (1 - G_RHO) * _EL + G_RHO * el
        for n in np.flatnonzero(_GA):
            i, j = _GP[n]; c = _cas(P, i, j)
            pred = float(_GT[n, c]) if _GV[n, c] > 0 else _lb
            en = (R - pred) ** 2; _GE[n] = en if _GN[n] == 0 else (1 - G_RHO) * _GE[n] + G_RHO * en
            _GT[n, c] = R; _GV[n, c] += 1
            _GN[n] += 1
            if _GN[n] >= G_MIN_VIS and _GE[n] >= _EL:
                _GA[n] = False; _GS[i, j] = 0.; st['podas'] += 1
                if _GN[n] == G_MIN_VIS: st['podas_a_6'] += 1
        if brazo == 'fijo15': return
        if abs(e) > G_THETA:
            st['sorpresas'] += 1
            act = [k for k in range(6) if P[k] > 0]; pares = [(a, b) for a in act for b in act if a < b]
            for (i, j) in pares: _GS[i, j] += 1
            vivos = {_GP[n] for n in np.flatnonzero(_GA)}
            listos = [p for p in pares if _GS[p] >= G_REC and p not in vivos]
            if len(listos) > 1: listos = sorted(listos, key=lambda p: (-_GS[p], _rg.random()))
            for (i, j) in listos:
                if (~_GA).any(): _nace(i, j, P, R, _lb); st['reclutas'] += 1

    t_m = 0; enc = 0
    while t_m < n_mord and enc < 200000:
        enc += 1
        kk = tren[int(rng_m.integers(len(tren)))]; P = P_[kk]
        _ws, n_lee = _lenta(P)
        if regimen == 'boca':
            Vb = 1.2 * _ws + 2.0 * 1.0 + .5; pb = 1 / (1 + np.exp(-Vb / .3))
            if not (rng_m.random() < pb): continue
        t_m += 1
        if n_lee is not None: st['lecturas_nodo'] += 1; st['leyo'].add(int(n_lee))
        else: st['lecturas_lineal'] += 1
        R = R_VAL[vr[kk]]
        _lb = _lin(P); _ds = R - _lb
        if LAM: _mcs = np.minimum(Wps, Wns) * (P > 0); Wps = Wps - LAM * _mcs; Wns = Wns - LAM * _mcs
        if _ds > 0: Wps = np.clip(Wps + ETA_S * _ds * P, 0, CLIP_S)
        else:       Wns = np.clip(Wns + ETA_S * (-_ds) * P, 0, CLIP_S)
        _crece_paso(P, R, _ws, _lb)

    # sonda: lectura lenta pura sobre los patrones de test (sin tocar estado)
    ac = {'comida': [], 'veneno': []}; lect = {}
    for k in test:
        w, n = _lenta(P_[k]); v = vr[k]
        ok = (w > 0) if v == 'comida' else (w < 0)
        ac[v].append(1.0 if ok else 0.0); lect[k] = (None if n is None else _GP[n])
    acc_estricta = 0.5 * (np.mean(ac['comida']) + np.mean(ac['veneno']))
    vivos = [_GP[n] for n in np.flatnonzero(_GA)]
    lee01 = sum(1 for k in test if lect[k] == (0, 1)); leeN = sum(1 for k in test if lect[k] is not None)
    return dict(seed=seed, regimen=regimen, brazo=brazo, mordidas=t_m, encuentros=enc, acc_estricta=round(float(acc_estricta), 3),
                nodos_vivos=len(vivos), vivo_01=((0, 1) in vivos), reclutas=st['reclutas'], podas=st['podas'],
                podas_a_6=st['podas_a_6'], nacidos_con_GE_mayor_o_igual_EL=st['nace_GE_mayor_EL'],
                nodos_que_leyeron_alguna_vez=len(st['leyo']), lecturas_nodo=st['lecturas_nodo'], lecturas_lineal=st['lecturas_lineal'],
                test_leidos_por_nodo=leeN, test_leidos_por_01=lee01, sorpresas=st['sorpresas'], EL_final=round(float(_EL), 3),
                primeros_nacidos=st['nacidos'][:6])


def e1_aritmetica():
    """E1 del tronco, segun §2.5 del diseno: errores -3.00, -1.65 (dos sorpresas) -> nodos nacen en la 2.a mordida.
    _EL tras 50 000 pasos con la lineal ajustando A y B: tomo 0.05 (generoso; la EMA de errores ~0)."""
    EL = 0.05
    el1 = 3.0 ** 2; EL = (1 - G_RHO) * EL + G_RHO * el1            # 1.a mordida del estimulo nuevo (lineal 0)
    lb2 = -0.45 * 3.0; el2 = (-3.0 - lb2) ** 2; EL = (1 - G_RHO) * EL + G_RHO * el2   # 2.a mordida: lineal -1.35
    GE_nace = el2
    filas = []
    ge, ele = GE_nace, EL
    for k in range(1, 6):   # 5 mordidas mas (de A, error ~0) -> GN = 6: poda si GE >= EL
        ge = (1 - G_RHO) * ge; ele = (1 - G_RHO) * ele
        filas.append((k + 1, round(ge, 3), round(ele, 3), ge < ele))
    return dict(EL_antes=0.05, el_mordida1=el1, el_mordida2=round(el2, 4), EL_al_nacer=round(EL, 4), GE_al_nacer=round(GE_nace, 4),
                puede_leer_al_nacer=bool(GE_nace < EL), trayectoria_GN_GE_EL_lee=filas,
                lectura='el nodo nace con GE ~10x _EL; ambos decaen a 0.98 por mordida; nunca GE < _EL -> no lee nunca y muere en GN=6')


if __name__ == '__main__':
    desde = int(sys.argv[1]) if len(sys.argv) > 1 else 1101
    n = int(sys.argv[2]) if len(sys.argv) > 2 else 20
    n_mord = int(sys.argv[3]) if len(sys.argv) > 3 else 300
    filas = []
    for regimen in ('siempre', 'boca'):
        for brazo in ('crece', 'fijo15'):
            for s in range(desde, desde + n):
                filas.append(replay(s, regimen, brazo, n_mord))
    res = {}
    for regimen in ('siempre', 'boca'):
        for brazo in ('crece', 'fijo15'):
            f = [x for x in filas if x['regimen'] == regimen and x['brazo'] == brazo]
            med = lambda k: float(np.median([x[k] for x in f]))
            res[f'{regimen}/{brazo}'] = dict(
                acc_estricta_mediana=med('acc_estricta'), acc_ge_075=sum(1 for x in f if x['acc_estricta'] >= 0.75),
                nodos_vivos_mediana=med('nodos_vivos'), vivo_01=sum(1 for x in f if x['vivo_01']),
                test_leidos_por_01_mediana=med('test_leidos_por_01'), test_leidos_por_nodo_mediana=med('test_leidos_por_nodo'),
                reclutas_mediana=med('reclutas'), podas_mediana=med('podas'), podas_a_6_mediana=med('podas_a_6'),
                nacidos_con_GE_ge_EL_mediana=med('nacidos_con_GE_mayor_o_igual_EL'),
                nodos_que_leyeron_alguna_vez_mediana=med('nodos_que_leyeron_alguna_vez'),
                lecturas_nodo_mediana=med('lecturas_nodo'), lecturas_lineal_mediana=med('lecturas_lineal'),
                EL_final_mediana=med('EL_final'))
    out = dict(desde=desde, n=n, mordidas_por_corrida=n_mord, resumen=res, E1_aritmetica=e1_aritmetica(), filas=filas)
    json.dump(out, open(os.path.join(AQUI, 'refuta_localidad_crece_codigo.json'), 'w', encoding='utf-8'), indent=1, default=str)
    print(json.dumps(dict(resumen=res, E1=out['E1_aritmetica']), indent=1, default=str))
