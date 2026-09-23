"""corre_n8.py -- nivel 8: ¿sigue aprendiendo el tronco v14.2 con 90 celdas en un mundo de 200 estimulos nuevos, y la
fusion de celdas (nivel8_aprendizaje_abierto.md s3 y s7) lo sostiene? PREREGISTRO_n8.md manda.

Brazos (todos con las perillas de v14.2, verificadas campo a campo contra organismo/organismo_v142.py, regla 14):
  base     tronco v14.2, mundo en flujo, sin fusion
  fus      + fusion dirigida (KW mas parecido, valor compatible)
  fusazar  + fusion de dos celdas al azar (control que puede ganar)
  recic    tronco v14.2 en el mundo RECICLADO (novedad falsa)

Uso:
  python experimentos/subida_n8/corre_n8.py --humo                     (UN proceso, semilla 12690, los 4 brazos; JSON en datos/humo/)
  python experimentos/subida_n8/corre_n8.py --serie base,fus,fusazar,recic --desde 12601 --n 20 --pool 6   (solo el coordinador)
"""
import argparse, hashlib, inspect, json, os, statistics as st, sys, time

sys.stdout.reconfigure(encoding='utf-8', errors='replace')
AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
sys.path.insert(0, AQUI)
sys.path.insert(0, os.path.join(RAIZ, 'organismo'))
import numpy as np
import organismo_flujo as OF
import mundo_n8 as MN

SHA_FLUJO = '14afed5aa16e09bf'
SHA_TRONCO = '17528d767fcebaf6'
VENTANA, P_VIEJO = 8, 0.25
N_RET = 40          # RET40: los 40 primeros introducidos, leidos al final (t = T-1)
# ADQ: signo del valor de cada estimulo en el momento en que SALE de la ventana (t_entrada(j+VENTANA+1)), balanceado
TRAMO_TARDE = (140, 190)    # 50 entradas = 5 bloques de 10 (25/25), mas alla del agotamiento del pool
TRAMO_TEMPRANO = (10, 40)   # 30 entradas = 3 bloques (15/15), con celdas libres

# Perillas de v14.2 (defectos de organismo_v142.run) que el instrumento de capacidad NO trae por defecto.
V142 = dict(plast=True, lam=0.05, memoria_rechazo=20, mu_norm=True, div_signo=True, eta_s=0.15, clip_s=10.0, puerta=3,
            puerta_pat=5, pat_shuf=0, pat_min=1, mask_rel=2, del_s=0.25, del_c=0.25, ema_c=0.05)
BRAZOS = {
    'base':    dict(mundo='flujo', fusion=0),
    'fus':     dict(mundo='flujo', fusion=1),
    'fusazar': dict(mundo='flujo', fusion=2),
    'recic':   dict(mundo='recic', fusion=0),
}
# Parametros de mundo que el tronco fija a su mundo de dos estimulos y aqui se declaran distintos (no son del organismo).
SOLO_MUNDO = {'T', 'learn', 'invertir_en', 'nuevo', 'nuevo_en', 'nuevo_val', 'solap_B', 'solap_AB', 'log_cada', 'desambiguar'}


def h16(p):
    return hashlib.sha256(open(p, 'rb').read()).hexdigest()[:16]


def kwargs_brazo(brazo):
    b = BRAZOS[brazo]
    return dict(V142, ventana=VENTANA, p_viejo=P_VIEJO, fusion=b['fusion'])


def entrada_campo_a_campo():
    """Regla 14: cada parametro del organismo del tronco que tambien existe en el instrumento vale lo mismo."""
    import organismo_v142 as TR
    ptr = {k: v.default for k, v in inspect.signature(TR.run).parameters.items() if v.default is not inspect._empty}
    pin = {k: v.default for k, v in inspect.signature(OF.run).parameters.items() if v.default is not inspect._empty}
    malos, filas = [], []
    for brazo in BRAZOS:
        kw = kwargs_brazo(brazo)
        for k, vt in ptr.items():
            if k in SOLO_MUNDO:
                continue
            if k not in pin:
                filas.append((brazo, k, vt, 'NO EXISTE en el instrumento'))
                malos.append((brazo, k, vt, None))
                continue
            vi = kw.get(k, pin[k])
            ok = (vi == vt)
            filas.append((brazo, k, vt, vi))
            if not ok:
                malos.append((brazo, k, vt, vi))
    # desambiguar (B-5) no existe en el instrumento: es INERTE aqui por construccion (R en {+1,-3} en toda mordida).
    return malos, filas


def bal(nombres, W, val):
    """Acierto de signo BALANCEADO (media de comida y veneno); W == 0 cuenta 0.5."""
    sc = {'comida': [], 'veneno': []}
    for n in nombres:
        w = W[n]
        s = 0.5 if w == 0 else (1.0 if (w > 0) == (val[n] == 'comida') else 0.0)
        sc[val[n]].append(s)
    partes = [st.mean(v) for v in sc.values() if v]
    return st.mean(partes) if partes else None


def corre_uno(args):
    semilla, brazo = args
    b = BRAZOS[brazo]
    orden, pats, val = MN.mundo(semilla, reciclado=(b['mundo'] == 'recic'))
    plan = MN.plan_de(orden, val)
    T = MN.T_de()
    N = MN.N_EST
    # fotos (solo lectura): justo despues de cada entrada (t+1: el estimulo ya esta, sin ninguna mordida = su valor A PRIORI)
    # y justo antes de cada entrada (t: los j <= n-1-VENTANA acaban de salir de la ventana); ultima en T-1
    t_prior = {j: MN.t_entrada(j) + 1 for j in range(2, N)}
    t_sale = {j: MN.t_entrada(j + VENTANA + 1) for j in range(0, N - VENTANA - 1)}
    chk = sorted(set(t_prior.values()) | set(t_sale.values()) | {T - 1})
    t0 = time.time()
    r = OF.run(semilla, T=T, plan=plan, pats=pats, chk=chk, **kwargs_brazo(brazo))
    dur = time.time() - t0
    fotos = {h['t']: h for h in r['hist']}
    Wprior = {j: fotos[t_prior[j]]['W'][orden[j]] for j in t_prior}
    Wsale = {j: fotos[t_sale[j]]['W'][orden[j]] for j in t_sale}
    Wfin = fotos[T - 1]['W']
    # nulo: las mismas W contra valencias PERMUTADAS dentro de cada bloque de 10 (generador aparte; esperado 0.5)
    g = np.random.default_rng([int(semilla), 909])
    vnulo = {}
    for a0 in range(0, N, MN.BLOQUE):
        idx = list(range(a0, min(a0 + MN.BLOQUE, N))); pm = g.permutation(len(idx))
        for k, j in enumerate(idx):
            vnulo[j] = val[orden[idx[pm[k]]]]
    def bal_j(js, Wj, vj):
        sc = {'comida': [], 'veneno': []}
        for j in js:
            w = Wj[j]
            sc[vj(j)].append(0.5 if w == 0 else (1.0 if (w > 0) == (vj(j) == 'comida') else 0.0))
        partes = [st.mean(v) for v in sc.values() if v]
        return round(st.mean(partes), 4) if partes else None
    vv = lambda j: val[orden[j]]
    def por_clase(js, Wj, clase):   # acierto de signo SOLO en una clase (transparencia: el a priori negativo regala el veneno)
        xs = [0.5 if Wj[j] == 0 else (1.0 if (Wj[j] > 0) == (clase == 'comida') else 0.0) for j in js if vv(j) == clase]
        return round(st.mean(xs), 4) if xs else None
    tarde = [j for j in range(*TRAMO_TARDE) if j in Wsale]
    temprano = [j for j in range(*TRAMO_TEMPRANO) if j in Wsale]
    curva = [bal_j([j for j in range(a0, a0 + 10) if j in Wsale], Wsale, vv) for a0 in range(0, TRAMO_TARDE[1], 10)]   # 19 bloques completos (0-189)
    curva_fin = [bal_j(list(range(a0, a0 + 10)), {j: Wfin[orden[j]] for j in range(N)}, vv) for a0 in range(0, N, 10)]
    ret = bal(list(dict.fromkeys(orden[:N_RET])), Wfin, val)
    ret_todo = bal(list(dict.fromkeys(orden)), Wfin, val)
    # conducta en el ultimo cuarto (t >= 150000): tasa de mordida de comida menos la de veneno
    vc = sum(r['vis'][n][3] for n in pats if val[n] == 'comida'); mc = sum(r['mord'][n][3] for n in pats if val[n] == 'comida')
    vn = sum(r['vis'][n][3] for n in pats if val[n] == 'veneno'); mv = sum(r['mord'][n][3] for n in pats if val[n] == 'veneno')
    cond = (mc / vc if vc else 0.0) - (mv / vn if vn else 0.0)
    return dict(semilla=semilla, brazo=brazo, T=T, dur_s=round(dur, 1),
                ADQ_tarde=bal_j(tarde, Wsale, vv), ADQ_temprano=bal_j(temprano, Wsale, vv),
                PRIOR_tarde=bal_j(tarde, Wprior, vv), NULO_tarde=bal_j(tarde, Wsale, lambda j: vnulo[j]),
                ADQ_tarde_com=por_clase(tarde, Wsale, 'comida'), ADQ_tarde_ven=por_clase(tarde, Wsale, 'veneno'),
                ADQ_temprano_com=por_clase(temprano, Wsale, 'comida'),
                PRIOR_tarde_com=por_clase(tarde, Wprior, 'comida'), PRIOR_tarde_ven=por_clase(tarde, Wprior, 'veneno'),
                RET40=round(ret, 4), RET_todo=round(ret_todo, 4),
                curva_ADQ_bloques10=curva, curva_final_bloques10=curva_fin, cond_ult_cuarto=round(cond, 4),
                mord_com_ult=mc, vis_com_ult=vc, mord_ven_ult=mv, vis_ven_ult=vn,
                muertes=r['deaths'], splits=r['splits'], celdas=r['celdas'], t_agot=r['t_agot'],
                est_agot=(None if r['t_agot'] is None else 1 + r['t_agot'] // MN.PASO_T),
                n_fus=r['n_fus'], n_cod=r['n_cod'], mv_tot=r['mv_tot'], mc_tot=r['mc_tot'])


def pareado(a, b, campo):
    """A > B: A mayor en >= 15/20 semillas Y diferencia mediana >= 0.03 (misma letra que aprende_barrer)."""
    sa = {x['semilla']: x[campo] for x in a}; sb = {x['semilla']: x[campo] for x in b}
    com = sorted(set(sa) & set(sb))
    d = [sa[s] - sb[s] for s in com]
    return dict(n=len(com), gana=sum(1 for x in d if x > 0), empata=sum(1 for x in d if x == 0),
                dif_mediana=round(st.median(d), 4) if d else None)


def resumen(res):
    out = {}
    for brazo in BRAZOS:
        xs = [x for x in res if x['brazo'] == brazo]
        if not xs:
            continue
        m = lambda c: round(st.median([x[c] for x in xs if x[c] is not None]), 4) if any(x[c] is not None for x in xs) else None
        out[brazo] = {c: m(c) for c in ('ADQ_tarde', 'ADQ_temprano', 'PRIOR_tarde', 'NULO_tarde', 'ADQ_tarde_com', 'ADQ_tarde_ven',
                                         'ADQ_temprano_com', 'PRIOR_tarde_com', 'PRIOR_tarde_ven', 'RET40', 'RET_todo',
                                         'cond_ult_cuarto', 'muertes', 'splits', 'n_fus', 'est_agot', 'dur_s')}
        out[brazo]['n'] = len(xs)
        out[brazo]['ADQ_tarde_min'] = min(x['ADQ_tarde'] for x in xs)
        out[brazo]['ADQ_tarde_sobre_nulo'] = sum(1 for x in xs if x['ADQ_tarde'] > x['NULO_tarde'])
        out[brazo]['ADQ_tarde_sobre_prior'] = sum(1 for x in xs if x['ADQ_tarde'] > x['PRIOR_tarde'])
        out[brazo]['caida'] = sum(1 for x in xs if x['ADQ_tarde'] < x['ADQ_temprano'] - 0.10)
        out[brazo]['com_sobre_prior_com'] = sum(1 for x in xs if x['ADQ_tarde_com'] > x['PRIOR_tarde_com'])
        out[brazo]['dif_com_prior_mediana'] = round(st.median([x['ADQ_tarde_com'] - x['PRIOR_tarde_com'] for x in xs]), 4)
        out[brazo]['dif_tarde_temprano_com_mediana'] = round(st.median([x['ADQ_tarde_com'] - x['ADQ_temprano_com'] for x in xs]), 4)
        out[brazo]['curva_mediana'] = [round(st.median(c), 4) for c in zip(*[x['curva_ADQ_bloques10'] for x in xs])]
        out[brazo]['curva_final_mediana'] = [round(st.median(c), 4) for c in zip(*[x['curva_final_bloques10'] for x in xs])]
    por = lambda b: [x for x in res if x['brazo'] == b]
    pares = {}
    for a, b in (('fus', 'base'), ('fus', 'fusazar'), ('fusazar', 'base'), ('recic', 'base')):
        if por(a) and por(b):
            for c in ('ADQ_tarde', 'ADQ_tarde_com', 'RET40', 'RET_todo', 'cond_ult_cuarto'):
                pares[f'{a}-{b}:{c}'] = pareado(por(a), por(b), c)
    out['pareados'] = pares
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--humo', action='store_true')
    ap.add_argument('--serie', default='base,fus,fusazar,recic')
    ap.add_argument('--desde', type=int, default=12601)
    ap.add_argument('--n', type=int, default=20)
    ap.add_argument('--pool', type=int, default=0)
    ap.add_argument('--semilla_humo', type=int, default=12690)
    a = ap.parse_args()
    if h16(os.path.join(AQUI, 'organismo_flujo.py')) != SHA_FLUJO:
        raise SystemExit('organismo_flujo.py no es el construido (sha). Correr construye_n8.py e identidad_n8.py.')
    if h16(os.path.join(RAIZ, 'organismo', 'organismo_v142.py')) != SHA_TRONCO:
        raise SystemExit('tronco v14.2 con sha distinto. Abortado.')
    malos, filas = entrada_campo_a_campo()
    if malos:
        raise SystemExit(f'REGLA 14: entrada distinta del tronco: {malos}')
    brazos = [x for x in a.serie.split(',') if x]
    for x in brazos:
        if x not in BRAZOS:
            raise SystemExit(f'brazo desconocido {x}')
    sello = time.strftime('%Y%m%d_%H%M%S')
    if a.humo:
        semillas = [a.semilla_humo]
        dest = os.path.join(AQUI, 'datos', 'humo')
        pref = f'n8_humo_{"-".join(brazos)}_s{a.semilla_humo}_{sello}'
    else:
        semillas = list(range(a.desde, a.desde + a.n))
        dest = os.path.join(AQUI, 'datos')
        pref = f'n8_serie_{"-".join(brazos)}_s{semillas[0]}-{semillas[-1]}_{sello}'
    os.makedirs(dest, exist_ok=True)
    tareas = [(s, b) for b in brazos for s in semillas]
    print(f'{pref}: {len(tareas)} corridas, T={MN.T_de()}, entrada campo a campo OK ({len(filas)} campos)', flush=True)
    t0 = time.time()
    if a.humo or a.pool <= 1:
        res = []
        for tk in tareas:
            r = corre_uno(tk); res.append(r)
            print(f"  s{r['semilla']} {r['brazo']:8s} ADQ_tarde {r['ADQ_tarde']} temprano {r['ADQ_temprano']} prior {r['PRIOR_tarde']} "
                  f"nulo {r['NULO_tarde']} (com {r['ADQ_tarde_com']} / ven {r['ADQ_tarde_ven']}; prior com {r['PRIOR_tarde_com']} / ven {r['PRIOR_tarde_ven']}) RET40 {r['RET40']} cond {r['cond_ult_cuarto']} muertes {r['muertes']} splits {r['splits']} "
                  f"fus {r['n_fus']} agota@{r['est_agot']} {r['dur_s']}s", flush=True)
            print(f"     curva al salir de la ventana (bloques de 10): {r['curva_ADQ_bloques10']}", flush=True)
            print(f"     curva al final (bloques de 10):              {r['curva_final_bloques10']}", flush=True)
    else:
        from multiprocessing import Pool   # solo el coordinador
        with Pool(a.pool) as p:
            res = p.map(corre_uno, tareas)
    out = dict(pref=pref, humo=a.humo, semillas=semillas, brazos=brazos, T=MN.T_de(), ventana=VENTANA, p_viejo=P_VIEJO,
               N_RET=N_RET, tramo_tarde=TRAMO_TARDE, tramo_temprano=TRAMO_TEMPRANO, perillas_v142=V142,
               shas={'organismo_flujo': SHA_FLUJO, 'organismo_v142': SHA_TRONCO,
                     'mundo_n8': h16(os.path.join(AQUI, 'mundo_n8.py')), 'corre_n8': h16(os.path.abspath(__file__))},
               entrada_campo_a_campo=[list(map(str, f)) for f in filas], cpu_s=round(time.time() - t0, 1),
               resultados=res, resumen=resumen(res))
    ruta = os.path.join(dest, pref + '.json')
    json.dump(out, open(ruta, 'w', encoding='utf-8'), indent=1, ensure_ascii=False)
    print(json.dumps(out['resumen'], ensure_ascii=False, indent=1))
    print(f'JSON: {os.path.relpath(ruta, RAIZ)}  sha {h16(ruta)}  pared {out["cpu_s"]} s')


if __name__ == '__main__':
    main()
