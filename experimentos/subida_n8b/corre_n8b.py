"""corre_n8b.py -- nivel 8, tanda 2: con 90 celdas fijas y 500 estimulos nuevos (5.5 veces las celdas), ¿un organo que
RECICLA la celda de menor relevancia |Wp-Wn| libera capacidad sin pagarla con memoria? PREREGISTRO_n8b.md manda.

Brazos (todos con las perillas de v14.2, verificadas campo a campo contra organismo/organismo_v142.py, regla 14):
  base   tronco v14.2, mundo en flujo, sin organo
  (rel, recicla=1, la celda de menor |Wp-Wn|, existe en el instrumento y se practico, pero NO es brazo: ver PREREGISTRO §4)
  prueba + lectura NEUTRA (0) en la boca para lo que la puerta no reconoce, en vez del a priori de la via lenta
  prazar + la misma lectura neutra en encuentros AL AZAR, a la tasa propia de no reconocidos (control que puede ganar)
  pruso  prueba + uso (interaccion: ¿liberar celdas importa cuando el organismo si muestrea lo nuevo?)
  uso    + reciclaje de la celda que entra en MENOS codigos familiares (ncod >= puerta_pat); empate -> menor |Wp-Wn|
  pruazar prueba + reciclaje de una celda AL AZAR fuera del codigo actual (control que puede ganar de PRUSO)
  recic  tronco v14.2 en el mundo RECICLADO (novedad falsa: la medida tiene que ver la novedad)

Modos (exactamente uno; banderas desconocidas o abreviadas ABORTAN, ERR-115):
  --humo                      UN proceso, sin Pool, 200 estimulos (T = 200 000), semilla de practica; JSON en datos/humo/
  --serie base,prueba,prazar,uso,pruso,pruazar,recic --desde 14801 --n 20 --pool 6     (SOLO el coordinador; 500 estimulos, T = 500 000)
  --veredicto SERIE.json REPLICA.json                           (no corre nada: lee dos JSON y aplica la letra)
"""
import argparse, hashlib, inspect, json, os, statistics as st, sys, time

sys.stdout.reconfigure(encoding='utf-8', errors='replace')
AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
sys.path.insert(0, AQUI)
sys.path.insert(0, os.path.join(RAIZ, 'organismo'))
import numpy as np
import organismo_n8b as ON
import mundo_n8b as MN

SHA_ORG = 'f9f3b56b498f6fc7'
SHA_MUN = '74e6127ee3e36814'
SHA_TRONCO = '17528d767fcebaf6'
VENTANA, P_VIEJO = 8, 0.25
N_RET = 40
N_SERIE, N_HUMO = 500, 200
SEMILLAS_SERIE = {14801: 'serie', 14821: 'replica'}
SEMILLAS_HUMO = set(range(14890, 14900))   # 14890-14892: practica antes del preregistro; 14893: humo final
TRAMO_TEMPRANO = (10, 40)     # 30 entradas (15/15), con celdas libres
TRAMO_MEDIO = (140, 190)      # 50 entradas, las mismas que el tramo tarde de subida_n8

V142 = dict(plast=True, lam=0.05, memoria_rechazo=20, mu_norm=True, div_signo=True, eta_s=0.15, clip_s=10.0, puerta=3,
            puerta_pat=5, pat_shuf=0, pat_min=1, mask_rel=2, del_s=0.25, del_c=0.25, ema_c=0.05)
BRAZOS = {
    'base':   dict(mundo='flujo', recicla=0, prueba=0),
    'prueba': dict(mundo='flujo', recicla=0, prueba=1),
    'prazar': dict(mundo='flujo', recicla=0, prueba=2),
    'uso':    dict(mundo='flujo', recicla=3, prueba=0),
    'pruazar': dict(mundo='flujo', recicla=2, prueba=1),
    'pruso':  dict(mundo='flujo', recicla=3, prueba=1),
    'recic':  dict(mundo='recic', recicla=0, prueba=0),
}
SOLO_MUNDO = {'T', 'learn', 'invertir_en', 'nuevo', 'nuevo_en', 'nuevo_val', 'solap_B', 'solap_AB', 'log_cada', 'desambiguar'}


def h16(p):
    return hashlib.sha256(open(p, 'rb').read()).hexdigest()[:16]


def tramo_tarde(n_est):
    return (n_est - 60, n_est - 10)   # 50 entradas = 5 bloques (25/25); la ultima sale de la ventana antes de T


def kwargs_brazo(brazo):
    return dict(V142, ventana=VENTANA, p_viejo=P_VIEJO, fusion=0, recicla=BRAZOS[brazo]['recicla'], prueba=BRAZOS[brazo]['prueba'])


def entrada_campo_a_campo():
    """Regla 14: cada parametro del organismo del tronco que tambien existe en el instrumento vale lo mismo."""
    import organismo_v142 as TR
    ptr = {k: v.default for k, v in inspect.signature(TR.run).parameters.items() if v.default is not inspect._empty}
    pin = {k: v.default for k, v in inspect.signature(ON.run).parameters.items() if v.default is not inspect._empty}
    malos, filas = [], []
    for brazo in BRAZOS:
        kw = kwargs_brazo(brazo)
        for k, vt in ptr.items():
            if k in SOLO_MUNDO:
                continue
            if k not in pin:
                filas.append((brazo, k, vt, 'NO EXISTE en el instrumento')); malos.append((brazo, k, vt, None)); continue
            vi = kw.get(k, pin[k])
            filas.append((brazo, k, vt, vi))
            if vi != vt:
                malos.append((brazo, k, vt, vi))
    return malos, filas


def corre_uno(args):
    semilla, brazo, n_est = args
    b = BRAZOS[brazo]
    orden, pats, val = MN.mundo(semilla, n_est=n_est, reciclado=(b['mundo'] == 'recic'))
    plan = MN.plan_de(orden, val)
    T = MN.T_de(n_est)
    N = n_est
    t_prior = {j: MN.t_entrada(j) + 1 for j in range(2, N)}
    t_sale = {j: MN.t_entrada(j + VENTANA + 1) for j in range(0, N - VENTANA - 1)}
    chk = sorted(set(t_prior.values()) | set(t_sale.values()) | {T - 1})
    t0 = time.time()
    r = ON.run(semilla, T=T, plan=plan, pats=pats, chk=chk, **kwargs_brazo(brazo))
    dur = time.time() - t0
    fotos = {h['t']: h for h in r['hist']}
    Wprior = {j: fotos[t_prior[j]]['W'][orden[j]] for j in t_prior}
    Wsale = {j: fotos[t_sale[j]]['W'][orden[j]] for j in t_sale}
    Wfin = fotos[T - 1]['W']
    g = np.random.default_rng([int(semilla), 909])
    vnulo = {}
    for a0 in range(0, N, MN.BLOQUE):
        idx = list(range(a0, min(a0 + MN.BLOQUE, N))); pm = g.permutation(len(idx))
        for k, j in enumerate(idx):
            vnulo[j] = val[orden[idx[pm[k]]]]
    vv = lambda j: val[orden[j]]

    def acierto(w, clase):
        return 0.5 if w == 0 else (1.0 if (w > 0) == (clase == 'comida') else 0.0)

    def bal_j(js, Wj, vj):
        sc = {'comida': [], 'veneno': []}
        for j in js:
            sc[vj(j)].append(acierto(Wj[j], vj(j)))
        partes = [st.mean(v) for v in sc.values() if v]
        return round(st.mean(partes), 4) if partes else None

    def por_clase(js, Wj, clase):
        xs = [acierto(Wj[j], clase) for j in js if vv(j) == clase]
        return round(st.mean(xs), 4) if xs else None
    tt = tramo_tarde(N)
    tarde = [j for j in range(*tt) if j in Wsale]
    medio = [j for j in range(*TRAMO_MEDIO) if j in Wsale]
    temprano = [j for j in range(*TRAMO_TEMPRANO) if j in Wsale]
    Wfin_j = {j: Wfin[orden[j]] for j in range(N)}
    distintos40 = [j for j in range(N_RET)]   # en FLUJO los 40 primeros son distintos; en RECIC se repiten (es control)
    curva = [bal_j([j for j in range(a0, a0 + 10) if j in Wsale], Wsale, vv) for a0 in range(0, tt[1], 10)]
    curva_com = [por_clase([j for j in range(a0, a0 + 10) if j in Wsale], Wsale, 'comida') for a0 in range(0, tt[1], 10)]
    curva_fin = [bal_j(list(range(a0, a0 + 10)), Wfin_j, vv) for a0 in range(0, N, 10)]
    q4 = 3
    vc = sum(r['vis'][n][q4] for n in pats if val[n] == 'comida'); mc = sum(r['mord'][n][q4] for n in pats if val[n] == 'comida')
    vn = sum(r['vis'][n][q4] for n in pats if val[n] == 'veneno'); mv = sum(r['mord'][n][q4] for n in pats if val[n] == 'veneno')
    cond = (mc / vc if vc else 0.0) - (mv / vn if vn else 0.0)
    rl = r['rec_log']
    return dict(semilla=semilla, brazo=brazo, n_est=N, T=T, dur_s=round(dur, 1),
                ADQ_tarde=bal_j(tarde, Wsale, vv), ADQ_medio=bal_j(medio, Wsale, vv), ADQ_temprano=bal_j(temprano, Wsale, vv),
                PRIOR_tarde=bal_j(tarde, Wprior, vv), NULO_tarde=bal_j(tarde, Wsale, lambda j: vnulo[j]),
                ADQ_tarde_com=por_clase(tarde, Wsale, 'comida'), ADQ_tarde_ven=por_clase(tarde, Wsale, 'veneno'),
                ADQ_medio_com=por_clase(medio, Wsale, 'comida'), ADQ_temprano_com=por_clase(temprano, Wsale, 'comida'),
                PRIOR_tarde_com=por_clase(tarde, Wprior, 'comida'), PRIOR_tarde_ven=por_clase(tarde, Wprior, 'veneno'),
                RET40=bal_j(distintos40, Wfin_j, vv), RET40_com=por_clase(distintos40, Wfin_j, 'comida'),
                RET_todo=bal_j(list(range(N)), Wfin_j, vv),
                curva_ADQ_bloques10=curva, curva_com_bloques10=curva_com, curva_final_bloques10=curva_fin,
                cond_ult_cuarto=round(cond, 4), muertes=r['deaths'], splits=r['splits'], celdas=r['celdas'], t_agot=r['t_agot'],
                est_agot=(None if r['t_agot'] is None else 1 + r['t_agot'] // MN.PASO_T),
                n_rec=r['n_rec'], rec_rel_mediana=(round(st.median([x[2] for x in rl]), 4) if rl else None),
                n_prueba=r['n_prueba'], frac_nofam=(round(r['enc_nofam'] / r['enc_tot'], 4) if r['enc_tot'] else None),
                n_cod=r['n_cod'], mv_tot=r['mv_tot'], mc_tot=r['mc_tot'])


def pareado(a, b, campo):
    """A > B: A mayor en >= 15/20 semillas Y diferencia mediana >= 0.03 (misma letra que subida_n8 y aprende_barrer)."""
    sa = {x['semilla']: x[campo] for x in a}; sb = {x['semilla']: x[campo] for x in b}
    com = sorted(set(sa) & set(sb))
    d = [sa[s] - sb[s] for s in com]
    return dict(n=len(com), gana=sum(1 for x in d if x > 0), empata=sum(1 for x in d if x == 0), pierde=sum(1 for x in d if x < 0),
                dif_mediana=round(st.median(d), 4) if d else None)


def gana(p):
    return p['n'] > 0 and p['gana'] >= round(0.75 * p['n']) and p['dif_mediana'] >= 0.03


CAMPOS = ('ADQ_tarde', 'ADQ_medio', 'ADQ_temprano', 'PRIOR_tarde', 'NULO_tarde', 'ADQ_tarde_com', 'ADQ_tarde_ven', 'ADQ_medio_com',
          'ADQ_temprano_com', 'PRIOR_tarde_com', 'PRIOR_tarde_ven', 'RET40', 'RET40_com', 'RET_todo', 'cond_ult_cuarto',
          'muertes', 'splits', 'n_rec', 'rec_rel_mediana', 'n_prueba', 'frac_nofam', 'mc_tot', 'mv_tot', 'est_agot', 'dur_s')


def resumen(res):
    out = {}
    for brazo in BRAZOS:
        xs = [x for x in res if x['brazo'] == brazo]
        if not xs:
            continue
        m = lambda c: round(st.median([x[c] for x in xs if x[c] is not None]), 4) if any(x[c] is not None for x in xs) else None
        o = {c: m(c) for c in CAMPOS}
        o['n'] = len(xs)
        o['com_sobre_prior_com'] = sum(1 for x in xs if x['ADQ_tarde_com'] > x['PRIOR_tarde_com'])
        o['dif_com_prior_mediana'] = round(st.median([x['ADQ_tarde_com'] - x['PRIOR_tarde_com'] for x in xs]), 4)
        o['dif_tarde_temprano_com_mediana'] = round(st.median([x['ADQ_tarde_com'] - x['ADQ_temprano_com'] for x in xs]), 4)
        o['dif_tarde_medio_com_mediana'] = round(st.median([x['ADQ_tarde_com'] - x['ADQ_medio_com'] for x in xs]), 4)
        o['tarde_sobre_nulo'] = sum(1 for x in xs if x['ADQ_tarde'] > x['NULO_tarde'])
        o['agota'] = sum(1 for x in xs if x['est_agot'] is not None)
        o['curva_mediana'] = [round(st.median(c), 4) for c in zip(*[x['curva_ADQ_bloques10'] for x in xs])]
        o['curva_com_mediana'] = [round(st.median(c), 4) for c in zip(*[x['curva_com_bloques10'] for x in xs])]
        out[brazo] = o
    por = lambda b: [x for x in res if x['brazo'] == b]
    pares = {}
    for a, b in (('prueba', 'base'), ('prueba', 'prazar'), ('prazar', 'prueba'), ('prazar', 'base'), ('base', 'prueba'),
                 ('uso', 'base'), ('base', 'uso'), ('pruso', 'prueba'), ('prueba', 'pruso'), ('pruso', 'pruazar'),
                 ('pruazar', 'pruso'), ('pruazar', 'prueba'), ('recic', 'base')):
        if por(a) and por(b):
            for c in ('ADQ_tarde', 'ADQ_tarde_com', 'RET40', 'RET40_com', 'RET_todo', 'muertes', 'cond_ult_cuarto'):
                pares[f'{a}-{b}:{c}'] = pareado(por(a), por(b), c)
    out['pareados'] = pares
    return out


def menos_muertes(a, b):
    """A muere menos que B: A < B en >= 15/20 semillas Y mediana del cociente A/B <= 0.85."""
    sa = {x['semilla']: x['muertes'] for x in a}; sb = {x['semilla']: x['muertes'] for x in b}
    com = sorted(set(sa) & set(sb))
    if not com:
        return False, {}
    menos = sum(1 for s in com if sa[s] < sb[s]); coc = st.median([sa[s] / max(sb[s], 1) for s in com])
    return menos >= round(0.75 * len(com)) and coc <= 0.85, dict(n=len(com), menos=menos, cociente_mediano=round(coc, 3))


def predicciones(res):
    """Aplica V1-V2 y P1-P15 del PREREGISTRO_n8b.md §5 a UNA serie. Devuelve ({clave: (bool, texto)}, resumen)."""
    R = resumen(res); p = R['pareados']
    por = lambda b: [x for x in res if x['brazo'] == b]
    B, PR, PZ, U, PU, PA, C = (R.get(k) for k in ('base', 'prueba', 'prazar', 'uso', 'pruso', 'pruazar', 'recic'))
    ev = {}
    n = B['n'] if B else 0
    if C and B:
        ev['V1'] = (gana(p['recic-base:ADQ_tarde']) and C['ADQ_tarde'] >= 0.90,
                    f"RECIC > BASE y RECIC >= 0.90 (la medida ve la novedad): {p['recic-base:ADQ_tarde']}, RECIC {C['ADQ_tarde']}")
    if B:
        ev['V2'] = (B['tarde_sobre_nulo'] >= round(0.75 * n), f"BASE > NULO en ADQ_tarde {B['tarde_sobre_nulo']}/{n} (>= 15/20)")
        ev['P1'] = (B['agota'] >= round(0.9 * n) and B['est_agot'] is not None and 50 <= B['est_agot'] <= 95,
                    f"BASE agota las 90 celdas {B['agota']}/{n}, estimulo mediano {B['est_agot']} (>= 18/20, en 50-95)")
        ev['P2'] = (0.0 <= B['dif_com_prior_mediana'] <= 0.20,
                    f"BASE comida tarde - a priori, mediana {B['dif_com_prior_mediana']} (en 0.00-0.20)")
    if PR:
        ev['P3'] = (PR['com_sobre_prior_com'] >= round(0.8 * n) and PR['dif_com_prior_mediana'] >= 0.15,
                    f"PRUEBA comida tarde > a priori {PR['com_sobre_prior_com']}/{n}, dif {PR['dif_com_prior_mediana']} (>= 16/20 y >= 0.15)")
        ev['P5'] = (PR['dif_tarde_medio_com_mediana'] >= -0.10,
                    f"PRUEBA no sigue cayendo tras agotar: comida tarde - medio {PR['dif_tarde_medio_com_mediana']} (>= -0.10)")
        ev['P6'] = (PR['dif_tarde_temprano_com_mediana'] < -0.20,
                    f"PRUEBA cae contra lo temprano (muro de celdas): comida tarde - temprano {PR['dif_tarde_temprano_com_mediana']} (< -0.20)")
    if PR and B:
        ev['P4'] = (gana(p['prueba-base:ADQ_tarde_com']), f"PRUEBA > BASE en comida tarde: {p['prueba-base:ADQ_tarde_com']}")
        ok, d = menos_muertes(por('prueba'), por('base'))
        ev['P7'] = (ok, f"PRUEBA muere menos que BASE: {d} (>= 15/20 y cociente <= 0.85)")
    if PR and PZ:
        ev['P8'] = (not gana(p['prueba-prazar:ADQ_tarde_com']),
                    f"PRUEBA NO gana a PRAZAR en comida tarde: {p['prueba-prazar:ADQ_tarde_com']}")
        ok, d = menos_muertes(por('prueba'), por('prazar'))
        ev['P9'] = (ok, f"PRUEBA muere menos que PRAZAR: {d} (>= 15/20 y cociente <= 0.85)")
    if PZ and B:
        ev['P10'] = (gana(p['prazar-base:ADQ_tarde_com']), f"PRAZAR > BASE en comida tarde: {p['prazar-base:ADQ_tarde_com']}")
    if U and B:
        ev['P11'] = (not gana(p['uso-base:ADQ_tarde_com']), f"USO NO gana a BASE en comida tarde: {p['uso-base:ADQ_tarde_com']}")
        ev['P12'] = (U['RET40'] - B['RET40'] <= 0.02, f"USO no retiene mas que BASE: RET40 {U['RET40']} vs {B['RET40']} (dif <= +0.02)")
    if PU and PR:
        ev['P13'] = (not gana(p['pruso-prueba:ADQ_tarde_com']), f"PRUSO NO gana a PRUEBA en comida tarde: {p['pruso-prueba:ADQ_tarde_com']}")
    if PU and PA:
        ev['P14'] = (not gana(p['pruso-pruazar:ADQ_tarde_com']), f"PRUSO NO gana a PRUAZAR en comida tarde: {p['pruso-pruazar:ADQ_tarde_com']}")
    flujo = [R[k] for k in ('base', 'prueba', 'prazar', 'uso', 'pruso', 'pruazar') if R.get(k)]
    if flujo:
        ev['P15'] = (all(x['RET40'] <= 0.70 and x['RET40_com'] <= 0.40 for x in flujo),
                     f"ningun brazo retiene lo ausente: RET40 (com) {[(x['RET40'], x['RET40_com']) for x in flujo]} (todos <= 0.70 y <= 0.40)")
    # --- puertas de las piezas (§6), no son predicciones: se evaluan igual
    if PR and B:
        base_sigue = B['com_sobre_prior_com'] >= round(0.8 * n) and B['dif_com_prior_mediana'] >= 0.15 and B['dif_tarde_medio_com_mediana'] >= -0.10
        ev['G1'] = ((ev['P3'][0] and ev['P5'][0]) or base_sigue,
                    f"pieza 1: sigue aprendiendo a 5.5x las celdas (PRUEBA: P3 y P5; o BASE con la misma letra: {base_sigue})")
        ev['G4'] = (ev['P4'][0] and ev.get('P9', (False,))[0], "pieza 4 (parcial): PRUEBA > BASE en comida tarde Y muere menos que PRAZAR")
        ev['G4b'] = (ev['G4'][0] and gana(p['prueba-prazar:ADQ_tarde_com']), "pieza 4 (mas): ademas PRUEBA > PRAZAR en comida tarde")
    if PU and PR and PA:
        nopaga = PU['RET40'] >= PR['RET40'] - 0.05 and not gana(p['prueba-pruso:RET40'])
        ev['G3'] = (gana(p['pruso-prueba:ADQ_tarde_com']) and nopaga, f"pieza 3 (parcial): PRUSO > PRUEBA en comida tarde sin pagar memoria ({nopaga})")
        ev['G3b'] = (ev['G3'][0] and gana(p['pruso-pruazar:ADQ_tarde_com']), "pieza 3 (entera): ademas PRUSO > PRUAZAR")
    if flujo:
        ev['G2'] = (any(x['RET40'] >= 0.75 and x['RET40_com'] >= 0.50 for x in flujo), "pieza 2: algun brazo del flujo con RET40 >= 0.75 y RET40_com >= 0.50")
    return ev, R


def veredicto(ev1, ev2):
    """Letra del §6 del PREREGISTRO_n8b.md sobre serie (ev1) y replica (ev2). Devuelve (letra, porque, puntos)."""
    ambos = lambda k: bool(ev1.get(k, (False,))[0]) and bool(ev2.get(k, (False,))[0])
    if not (ambos('V1') and ambos('V2')):
        return 'NO SE LEE', 'V1 (RECIC ve la novedad) o V2 (BASE > NULO) cae en alguna de las dos series', 0
    pts, piezas = 0, []
    if ambos('G1'):
        pts += 5; piezas.append('pieza 1 completa (+5)')
    if ambos('G4b'):
        pts += 5; piezas.append('pieza 4 completa en su lectura "elige que muestrear" (+5)')
    elif ambos('G4'):
        pts += 3; piezas.append('pieza 4 parcial (+3)')
    if ambos('G3b'):
        pts += 15; piezas.append('pieza 3 entera (+15)')
    elif ambos('G3'):
        pts += 5; piezas.append('pieza 3 parcial (+5)')
    if ambos('G2'):
        pts += 10; piezas.append('pieza 2 (+10)')
    organo = ambos('G4') or ambos('G3')
    if ambos('G1') and organo:
        letra = 'FUNCIONA'
    elif piezas:
        letra = 'HAY ALGO MODESTO'
    else:
        letra = 'NO'
    return letra, ('; '.join(piezas) if piezas else 'ninguna pieza pasa en las dos series'), pts


def imprime_ev(tit, ev):
    print(f'--- {tit}')
    for k in sorted(ev, key=lambda s: ('VPG'.index(s[0]), int(''.join(c for c in s[1:] if c.isdigit())), s)):
        ok, txt = ev[k]
        print(f"  {k}: {'SE CUMPLE' if ok else 'CAE'}  {txt}")


def plan_de_corrida(a):
    """Valida el modo y las banderas ANTES de correr nada (ERR-115). Devuelve (brazos, semillas, n_est, destino, prefijo)."""
    if a.humo:
        if a.pool is not None or a.desde is not None or a.n is not None:
            raise SystemExit('--humo es UN proceso: no acepta --pool, --desde ni --n. Abortado.')
        if a.semilla_humo not in SEMILLAS_HUMO:
            raise SystemExit(f'semilla de humo fuera de las de practica {min(SEMILLAS_HUMO)}-{max(SEMILLAS_HUMO)}. Abortado.')
        brazos = list(BRAZOS); semillas = [a.semilla_humo]; n_est = N_HUMO
        dest = os.path.join(AQUI, 'datos', 'humo')
        pref = f'n8b_humo_{"-".join(brazos)}_s{a.semilla_humo}_N{n_est}'
    else:
        brazos = [x for x in a.serie.split(',') if x]
        if not brazos or any(x not in BRAZOS for x in brazos):
            raise SystemExit(f'brazos desconocidos en {a.serie!r}; validos: {list(BRAZOS)}. Abortado.')
        if a.desde not in SEMILLAS_SERIE or a.n != 20 or not a.pool or a.pool < 1:
            raise SystemExit(f'--serie exige --desde en {sorted(SEMILLAS_SERIE)}, --n 20 y --pool >= 1. Abortado.')
        semillas = list(range(a.desde, a.desde + a.n)); n_est = N_SERIE
        dest = os.path.join(AQUI, 'datos')
        pref = f'n8b_{SEMILLAS_SERIE[a.desde]}_{"-".join(brazos)}_s{semillas[0]}-{semillas[-1]}_N{n_est}'
    return brazos, semillas, n_est, dest, pref


def main():
    ap = argparse.ArgumentParser(allow_abbrev=False, description='nivel 8 tanda 2 (reciclaje por relevancia)')
    modo = ap.add_mutually_exclusive_group(required=True)
    modo.add_argument('--humo', action='store_true')
    modo.add_argument('--serie', type=str)
    modo.add_argument('--veredicto', nargs=2, metavar=('SERIE_JSON', 'REPLICA_JSON'))
    ap.add_argument('--desde', type=int)
    ap.add_argument('--n', type=int)
    ap.add_argument('--pool', type=int)
    ap.add_argument('--semilla_humo', type=int, default=14893)
    a = ap.parse_args()   # bandera desconocida o abreviada -> argparse sale con error 2 ANTES de correr nada
    if a.veredicto:
        evs = []
        for ruta in a.veredicto:
            d = json.load(open(ruta, encoding='utf-8'))
            if d.get('humo') or d.get('n_est') != N_SERIE:
                raise SystemExit(f'{ruta}: no es una serie de {N_SERIE} estimulos. Abortado.')
            if d.get('shas', {}).get('organismo_n8b') != SHA_ORG or d.get('shas', {}).get('mundo_n8b') != SHA_MUN:
                raise SystemExit(f'{ruta}: corrida con otro instrumento (sha). Abortado.')
            ev, _ = predicciones(d['resultados']); evs.append(ev)
            imprime_ev(f"{os.path.basename(ruta)} (semillas {d['semillas'][0]}-{d['semillas'][-1]})", ev)
        v, porque, pts = veredicto(*evs)
        print(f'VEREDICTO (serie + replica, PREREGISTRO_n8b §6): {v} -- {porque}; puntos propuestos del nivel 8: +{pts}')
        return
    if h16(os.path.join(AQUI, 'organismo_n8b.py')) != SHA_ORG or h16(os.path.join(AQUI, 'mundo_n8b.py')) != SHA_MUN:
        raise SystemExit('organismo_n8b.py o mundo_n8b.py no son los construidos (sha). Correr construye_n8b.py e identidad_n8b.py.')
    if h16(os.path.join(RAIZ, 'organismo', 'organismo_v142.py')) != SHA_TRONCO:
        raise SystemExit('tronco v14.2 con sha distinto. Abortado.')
    malos, filas = entrada_campo_a_campo()
    if malos:
        raise SystemExit(f'REGLA 14: entrada distinta del tronco: {malos}')
    brazos, semillas, n_est, dest, pref = plan_de_corrida(a)
    pref += '_' + time.strftime('%Y%m%d_%H%M%S')
    os.makedirs(dest, exist_ok=True)
    tareas = [(s, b, n_est) for b in brazos for s in semillas]
    print(f'{pref}: {len(tareas)} corridas, N={n_est}, T={MN.T_de(n_est)}, entrada campo a campo OK ({len(filas)} campos)', flush=True)
    t0 = time.time()
    if a.humo:
        res = []
        for tk in tareas:
            r = corre_uno(tk); res.append(r)
            print(f"  s{r['semilla']} {r['brazo']:6s} ADQ tarde {r['ADQ_tarde']} (com {r['ADQ_tarde_com']} / ven {r['ADQ_tarde_ven']}; "
                  f"prior com {r['PRIOR_tarde_com']}) temprano com {r['ADQ_temprano_com']} nulo {r['NULO_tarde']} RET40 {r['RET40']} "
                  f"(com {r['RET40_com']}) cond {r['cond_ult_cuarto']} muertes {r['muertes']} splits {r['splits']} rec {r['n_rec']} "
                  f"prueba {r['n_prueba']} (no reconocidos {r['frac_nofam']}) mord com/ven {r['mc_tot']}/{r['mv_tot']} agota@{r['est_agot']} {r['dur_s']}s", flush=True)
            print(f"     curva comida al salir de la ventana (bloques de 10): {r['curva_com_bloques10']}", flush=True)
    else:
        from multiprocessing import Pool   # solo el coordinador
        with Pool(a.pool) as p:
            res = p.map(corre_uno, tareas)
    ev, R = predicciones(res)
    out = dict(pref=pref, humo=a.humo, semillas=semillas, brazos=brazos, n_est=n_est, T=MN.T_de(n_est), ventana=VENTANA,
               p_viejo=P_VIEJO, N_RET=N_RET, tramo_tarde=tramo_tarde(n_est), tramo_medio=TRAMO_MEDIO, tramo_temprano=TRAMO_TEMPRANO,
               perillas_v142=V142, d_pix=MN.D_PIX, peso=MN.PESO,
               shas={'organismo_n8b': SHA_ORG, 'mundo_n8b': SHA_MUN, 'organismo_v142': SHA_TRONCO,
                     'corre_n8b': h16(os.path.abspath(__file__))},
               entrada_campo_a_campo=[list(map(str, f)) for f in filas], pared_s=round(time.time() - t0, 1),
               resultados=res, resumen=R, predicciones={k: [v[0], v[1]] for k, v in ev.items()})
    ruta = os.path.join(dest, pref + '.json')
    json.dump(out, open(ruta, 'w', encoding='utf-8'), indent=1, ensure_ascii=False)
    print(json.dumps({k: v for k, v in R.items() if k != 'pareados'}, ensure_ascii=False))
    imprime_ev('predicciones sobre ESTA corrida', ev)
    print(f'JSON: {os.path.relpath(ruta, RAIZ)}  sha {h16(ruta)}  pared {out["pared_s"]} s')
    if a.humo:
        print('VEREDICTO: no aplica (humo de practica, 1 semilla y 200 estimulos; la letra del §6 exige serie y replica de 500)')
    else:
        print(f'VEREDICTO: pendiente de la otra serie; con las dos: python experimentos/subida_n8b/corre_n8b.py --veredicto <serie.json> <replica.json> (esta: {os.path.relpath(ruta, RAIZ)})')


if __name__ == '__main__':
    main()
