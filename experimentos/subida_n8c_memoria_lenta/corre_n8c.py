"""corre_n8c.py -- nivel 8, tanda 3 (pieza 2, "retener lo ausente mientras aprende lo nuevo"): ¿un organo de MEMORIA
LENTA CON REPASO (el organismo repasa sus propias huellas por celda y las consolida en sus pesos de valor) retiene los
40 primeros estimulos sin pagar la adquisicion de lo nuevo? PREREGISTRO_n8c.md manda.

Mundo: el de subida_n8 (mundo_n8.py b0b57d7ff02afe4e, importado de solo lectura): retina 12, 200 estimulos de peso 3,
uno cada 1000 pasos, ventana 8, p_viejo 0.25, valencias balanceadas 5/5 por bloque; T = 200 000.
Brazos (todos con las perillas de v14.2, verificadas campo a campo contra organismo/organismo_v142.py, regla 14):
  base      tronco v14.2 (organismo_repaso con repaso=0 == organismo_flujo == la BASE de subida_n8)
  rep1      + 1 repaso de la huella tras cada mordida (signo de la huella, objetivo = ultima R vivida de ese signo)
  rep10     + 10 repasos por mordida (BRAZO PRINCIPAL)
  baraj10   + 10 repasos con el SIGNO barajado (de la huella de otra celda): control que puede ganar
  sinhue10  + 10 repasos sin huella (objetivo = valor ACTUAL de la celda, K6): control "repaso sin consolidacion"

Modos (exactamente uno; banderas desconocidas o abreviadas ABORTAN con codigo 2, ERR-115):
  --humo                                   UN proceso, sin Pool, semilla de practica/humo (15890-15899); JSON en datos/humo/
  --serie base,rep1,rep10,baraj10,sinhue10 --desde 15801 --n 20 --pool 6     (SOLO el coordinador; replica: --desde 15821)
  --veredicto SERIE.json REPLICA.json      no corre nada: aplica la letra del PREREGISTRO §6 y la imprime en la ULTIMA linea
"""
import argparse, hashlib, inspect, json, os, statistics as st, sys, time

sys.stdout.reconfigure(encoding='utf-8', errors='replace')
AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
N8 = os.path.join(RAIZ, 'experimentos', 'subida_n8')
sys.path.insert(0, AQUI)
sys.path.insert(0, N8)
sys.path.insert(0, os.path.join(RAIZ, 'organismo'))
import numpy as np
import organismo_repaso as OR
import mundo_n8 as MN

SHA_ORG = '1dce42830f4230bc'
SHA_MUN = 'b0b57d7ff02afe4e'
SHA_TRONCO = '17528d767fcebaf6'
VENTANA, P_VIEJO = 8, 0.25
N_RET = 40
TRAMO_TARDE = (140, 190)
TRAMO_TEMPRANO = (10, 40)
SEMILLAS_SERIE = {15801: 'serie', 15821: 'replica'}
SEMILLAS_HUMO = set(range(15890, 15900))

V142 = dict(plast=True, lam=0.05, memoria_rechazo=20, mu_norm=True, div_signo=True, eta_s=0.15, clip_s=10.0, puerta=3,
            puerta_pat=5, pat_shuf=0, pat_min=1, mask_rel=2, del_s=0.25, del_c=0.25, ema_c=0.05)
BRAZOS = {
    'base':     dict(repaso=0, dosis=1),
    'rep1':     dict(repaso=1, dosis=1),
    'rep10':    dict(repaso=1, dosis=10),
    'baraj10':  dict(repaso=2, dosis=10),
    'sinhue10': dict(repaso=3, dosis=10),
}
SOLO_MUNDO = {'T', 'learn', 'invertir_en', 'nuevo', 'nuevo_en', 'nuevo_val', 'solap_B', 'solap_AB', 'log_cada', 'desambiguar'}


def h16(p):
    return hashlib.sha256(open(p, 'rb').read()).hexdigest()[:16]


def kwargs_brazo(brazo):
    return dict(V142, ventana=VENTANA, p_viejo=P_VIEJO, fusion=0, repaso=BRAZOS[brazo]['repaso'], dosis=BRAZOS[brazo]['dosis'])


def entrada_campo_a_campo():
    """Regla 14: cada parametro del organismo del tronco que tambien existe en el instrumento vale lo mismo."""
    import organismo_v142 as TR
    ptr = {k: v.default for k, v in inspect.signature(TR.run).parameters.items() if v.default is not inspect._empty}
    pin = {k: v.default for k, v in inspect.signature(OR.run).parameters.items() if v.default is not inspect._empty}
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


def acierto(w, clase):
    return 0.5 if w == 0 else (1.0 if (w > 0) == (clase == 'comida') else 0.0)


def corre_uno(args):
    semilla, brazo = args
    orden, pats, val = MN.mundo(semilla)
    plan = MN.plan_de(orden, val)
    T = MN.T_de(); N = MN.N_EST
    t_prior = {j: MN.t_entrada(j) + 1 for j in range(2, N)}
    t_sale = {j: MN.t_entrada(j + VENTANA + 1) for j in range(0, N - VENTANA - 1)}
    chk = sorted(set(t_prior.values()) | set(t_sale.values()) | {T - 1})
    t0 = time.time()
    r = OR.run(semilla, T=T, plan=plan, pats=pats, chk=chk, **kwargs_brazo(brazo))
    dur = time.time() - t0
    fotos = {h['t']: h for h in r['hist']}
    Wprior = {j: fotos[t_prior[j]]['W'][orden[j]] for j in t_prior}
    Wsale = {j: fotos[t_sale[j]]['W'][orden[j]] for j in t_sale}
    Wfin = fotos[T - 1]['W']
    g = np.random.default_rng([int(semilla), 909])   # NULO: el mismo que subida_n8
    vnulo = {}
    for a0 in range(0, N, MN.BLOQUE):
        idx = list(range(a0, min(a0 + MN.BLOQUE, N))); pm = g.permutation(len(idx))
        for k, j in enumerate(idx):
            vnulo[j] = val[orden[idx[pm[k]]]]
    vv = lambda j: val[orden[j]]
    def bal_j(js, Wj, vj):
        sc = {'comida': [], 'veneno': []}
        for j in js:
            sc[vj(j)].append(acierto(Wj[j], vj(j)))
        partes = [st.mean(v) for v in sc.values() if v]
        return round(st.mean(partes), 4) if partes else None
    def por_clase(js, Wj, clase):
        xs = [acierto(Wj[j], clase) for j in js if vv(j) == clase]
        return round(st.mean(xs), 4) if xs else None
    tarde = [j for j in range(*TRAMO_TARDE) if j in Wsale]
    temprano = [j for j in range(*TRAMO_TEMPRANO) if j in Wsale]
    j40 = list(range(N_RET))
    Wfin_j = {j: Wfin[orden[j]] for j in range(N)}
    # RET40_rel: de las comidas de los 40 primeros que estaban APRENDIDAS al salir de la ventana, cuantas siguen al final
    apr = [j for j in j40 if vv(j) == 'comida' and Wsale[j] > 0]
    ret_rel = round(sum(1 for j in apr if Wfin_j[j] > 0) / len(apr), 4) if apr else None
    vc = sum(r['vis'][n][3] for n in pats if val[n] == 'comida'); mc = sum(r['mord'][n][3] for n in pats if val[n] == 'comida')
    vn = sum(r['vis'][n][3] for n in pats if val[n] == 'veneno'); mv = sum(r['mord'][n][3] for n in pats if val[n] == 'veneno')
    v40c = sum(r['vis'][orden[j]][3] for j in j40 if vv(j) == 'comida'); m40c = sum(r['mord'][orden[j]][3] for j in j40 if vv(j) == 'comida')
    return dict(semilla=semilla, brazo=brazo, T=T, dur_s=round(dur, 1),
                ADQ_tarde=bal_j(tarde, Wsale, vv), ADQ_temprano=bal_j(temprano, Wsale, vv),
                PRIOR_tarde=bal_j(tarde, Wprior, vv), NULO_tarde=bal_j(tarde, Wsale, lambda j: vnulo[j]),
                ADQ_tarde_com=por_clase(tarde, Wsale, 'comida'), ADQ_tarde_ven=por_clase(tarde, Wsale, 'veneno'),
                ADQ_temprano_com=por_clase(temprano, Wsale, 'comida'),
                PRIOR_tarde_com=por_clase(tarde, Wprior, 'comida'),
                ADQ40_com=por_clase(j40, Wsale, 'comida'),
                RET40=bal_j(j40, Wfin_j, vv), RET40_com=por_clase(j40, Wfin_j, 'comida'), RET40_ven=por_clase(j40, Wfin_j, 'veneno'),
                RET40_rel=ret_rel, n_apr40=len(apr), RET40_NULO=bal_j(j40, Wfin_j, lambda j: vnulo[j]),
                RET_todo=bal_j(list(range(N)), Wfin_j, vv),
                cond_ult_cuarto=round((mc / vc if vc else 0.0) - (mv / vn if vn else 0.0), 4),
                mord40_com_ult=m40c, vis40_com_ult=v40c,
                muertes=r['deaths'], splits=r['splits'], celdas=r['celdas'], t_agot=r['t_agot'],
                est_agot=(None if r['t_agot'] is None else 1 + r['t_agot'] // MN.PASO_T),
                n_rep=r['n_rep'], n_rep_pos=r['n_rep_pos'], n_rep_neg=r['n_rep_neg'], mv_tot=r['mv_tot'], mc_tot=r['mc_tot'])


def pareado(a, b, campo):
    sa = {x['semilla']: x[campo] for x in a if x[campo] is not None}; sb = {x['semilla']: x[campo] for x in b if x[campo] is not None}
    com = sorted(set(sa) & set(sb)); d = [sa[s] - sb[s] for s in com]
    return dict(n=len(com), gana=sum(1 for x in d if x > 0), empata=sum(1 for x in d if x == 0),
                pierde=sum(1 for x in d if x < 0), dif_mediana=round(st.median(d), 4) if d else None)


def gana(p):   # letra: A > B = A mayor en >= 15/20 semillas Y diferencia mediana >= 0.03
    return p['gana'] >= 15 and p['dif_mediana'] is not None and p['dif_mediana'] >= 0.03


CAMPOS = ('ADQ_tarde', 'ADQ_tarde_com', 'PRIOR_tarde_com', 'ADQ_temprano', 'ADQ_temprano_com', 'NULO_tarde', 'ADQ40_com',
          'RET40', 'RET40_com', 'RET40_ven', 'RET40_rel', 'RET40_NULO', 'RET_todo', 'cond_ult_cuarto', 'muertes', 'splits',
          'est_agot', 'n_rep', 'n_rep_pos', 'dur_s')


def resumen(res):
    out = {}
    for brazo in BRAZOS:
        xs = [x for x in res if x['brazo'] == brazo]
        if not xs:
            continue
        out[brazo] = {c: (round(st.median([x[c] for x in xs if x[c] is not None]), 4) if any(x[c] is not None for x in xs) else None) for c in CAMPOS}
        out[brazo]['n'] = len(xs)
    por = lambda b: [x for x in res if x['brazo'] == b]
    pares = {}
    for a, b in (('rep10', 'base'), ('rep1', 'base'), ('rep10', 'baraj10'), ('rep10', 'sinhue10'), ('baraj10', 'base'), ('sinhue10', 'base')):
        if por(a) and por(b):
            for c in ('RET40', 'RET40_com', 'RET40_ven', 'ADQ_tarde', 'ADQ_tarde_com', 'muertes', 'RET_todo'):
                pares[f'{a}-{b}:{c}'] = pareado(por(a), por(b), c)
    out['pareados'] = pares
    return out


def predicciones(res):
    """PREREGISTRO_n8c.md §5, por la letra. Devuelve {Pk: (bool, texto)}. REP = rep10 (brazo principal)."""
    por = lambda b: [x for x in res if x['brazo'] == b]
    B, R1, R, BJ, SH = por('base'), por('rep1'), por('rep10'), por('baraj10'), por('sinhue10')
    if not (B and R1 and R and BJ and SH):
        return {}
    med = lambda xs, c: st.median([x[c] for x in xs if x[c] is not None])
    ev = {}
    m = med(R, 'RET40'); ev['P1'] = (m >= 0.75, f'REP10 RET40 mediana {m:.4f} >= 0.75 (prediccion central del encargo)')
    p = pareado(R, B, 'RET40'); ev['P2'] = (p['gana'] >= 15 and p['dif_mediana'] >= 0.05, f'REP10 > BASE en RET40 (>= 15/20 y dif >= 0.05): {p}')
    d = med(R, 'ADQ_tarde_com') - med(B, 'ADQ_tarde_com'); d2 = med(R, 'ADQ_tarde') - med(B, 'ADQ_tarde')
    ev['P3'] = (d >= -0.05 and d2 >= -0.05, f'adquisicion REP10 - BASE: ADQ_tarde_com {d:+.4f}, ADQ_tarde {d2:+.4f} (ambas >= -0.05)')
    p = pareado(R, BJ, 'RET40'); ev['P4'] = (gana(p), f'REP10 > BARAJ10 en RET40 (el contenido de la huella): {p}')
    p = pareado(R, SH, 'RET40'); ev['P5'] = (gana(p), f'REP10 > SINHUE10 en RET40 (la huella, no el valor actual): {p}')
    q = med(R, 'muertes') / med(B, 'muertes'); ev['P6'] = (q <= 1.15, f'muertes REP10/BASE {q:.3f} <= 1.15')
    m = med(R, 'RET40_ven'); ev['P7'] = (m >= 0.85, f'REP10 RET40_ven {m:.4f} >= 0.85 (no compra comida con veneno)')
    m = med(B, 'RET40'); ev['P8'] = (0.55 <= m <= 0.70, f'BASE RET40 {m:.4f} en 0.55-0.70 (validez: reproduce subida_n8)')
    p = pareado(R, B, 'RET40_rel'); ev['P9'] = (gana(p), f'REP10 > BASE en RET40_rel (lo aprendido que se conserva): {p}')
    d10 = st.median([x['RET40'] - y['RET40'] for x, y in zip(sorted(R, key=lambda z: z['semilla']), sorted(B, key=lambda z: z['semilla']))])
    d1 = st.median([x['RET40'] - y['RET40'] for x, y in zip(sorted(R1, key=lambda z: z['semilla']), sorted(B, key=lambda z: z['semilla']))])
    ev['P10'] = (d10 > d1, f'dosis: RET40 (REP10 - BASE) {d10:+.4f} > (REP1 - BASE) {d1:+.4f}')
    p = pareado(R1, B, 'RET40'); q = pareado(B, R1, 'RET40')
    ev['P11'] = (not gana(p) and not gana(q), f'REP1 y BASE no se separan en RET40: REP1-BASE {p}')
    return ev


PRINCIPALES = ('P2', 'P4', 'P6', 'P7')


def veredicto(ev1, ev2):
    """PREREGISTRO_n8c.md §6. Devuelve la letra."""
    if not ev1 or not ev2:
        return 'NO SE LEE (faltan brazos)'
    if not (ev1['P8'][0] and ev2['P8'][0]):
        return 'NO SE LEE (la BASE no reproduce subida_n8: P8)'
    ok = lambda k: ev1[k][0] and ev2[k][0]
    if all(ok(k) for k in PRINCIPALES) and ok('P1') and ok('P3') and ok('P5'):
        return 'FUNCIONA'
    if all(ok(k) for k in PRINCIPALES):
        return 'HAY ALGO MODESTO'
    if ok('P2') and not ok('P4'):
        return 'NO (el repaso retiene, pero el contenido de la huella no importa: BARAJ10 no pierde)'
    return 'NO'


def imprime_ev(tit, ev):
    print(f'--- {tit}')
    for k, (b, txt) in ev.items():
        print(f'  {k} {"SI" if b else "NO"}  {txt}')


def main():
    ap = argparse.ArgumentParser(allow_abbrev=False, description='nivel 8 tanda 3: memoria lenta con repaso')
    modo = ap.add_mutually_exclusive_group(required=True)
    modo.add_argument('--humo', action='store_true')
    modo.add_argument('--serie', type=str)
    modo.add_argument('--veredicto', nargs=2, metavar=('SERIE_JSON', 'REPLICA_JSON'))
    ap.add_argument('--desde', type=int)
    ap.add_argument('--n', type=int)
    ap.add_argument('--pool', type=int)
    ap.add_argument('--semilla_humo', type=int, default=15893)
    ap.add_argument('--brazos_humo', type=str, default='base,rep1,rep10,baraj10,sinhue10')
    a = ap.parse_args()   # bandera desconocida o abreviada -> argparse sale con codigo 2 ANTES de correr nada
    if a.veredicto:
        evs = []
        for ruta in a.veredicto:
            d = json.load(open(ruta, encoding='utf-8'))
            if d.get('humo') or d.get('shas', {}).get('organismo_repaso') != SHA_ORG:
                raise SystemExit(f'{ruta}: no es una serie de este instrumento (humo o sha distinto). Abortado.')
            evs.append(predicciones(d['resultados']))
        imprime_ev('serie', evs[0]); imprime_ev('replica', evs[1])
        print(f'VEREDICTO: {veredicto(*evs)}')
        return
    if h16(os.path.join(AQUI, 'organismo_repaso.py')) != SHA_ORG:
        raise SystemExit('organismo_repaso.py no es el construido (sha). Correr construye_n8c.py e identidad_n8c.py. Abortado.')
    if h16(os.path.join(N8, 'mundo_n8.py')) != SHA_MUN:
        raise SystemExit('mundo_n8.py con sha distinto. Abortado.')
    if h16(os.path.join(RAIZ, 'organismo', 'organismo_v142.py')) != SHA_TRONCO:
        raise SystemExit('tronco v14.2 con sha distinto. Abortado.')
    malos, filas = entrada_campo_a_campo()
    if malos:
        raise SystemExit(f'REGLA 14: entrada distinta del tronco: {malos}. Abortado.')
    sello = time.strftime('%Y%m%d_%H%M%S')
    if a.humo:
        if a.desde is not None or a.n is not None or a.pool is not None:
            raise SystemExit('--humo es UN proceso: no acepta --pool, --desde ni --n. Abortado.')
        if a.semilla_humo not in SEMILLAS_HUMO:
            raise SystemExit(f'semilla de humo fuera de {min(SEMILLAS_HUMO)}-{max(SEMILLAS_HUMO)}. Abortado.')
        brazos = [x for x in a.brazos_humo.split(',') if x]
        semillas = [a.semilla_humo]; dest = os.path.join(AQUI, 'datos', 'humo')
        pref = f'n8c_humo_{"-".join(brazos)}_s{a.semilla_humo}_{sello}'
    else:
        brazos = [x for x in a.serie.split(',') if x]
        if a.desde not in SEMILLAS_SERIE or a.n != 20 or a.pool is None or a.pool < 1:
            raise SystemExit(f'--serie exige --desde en {sorted(SEMILLAS_SERIE)}, --n 20 y --pool >= 1. Abortado.')
        semillas = list(range(a.desde, a.desde + a.n)); dest = os.path.join(AQUI, 'datos')
        pref = f'n8c_{SEMILLAS_SERIE[a.desde]}_{"-".join(brazos)}_s{semillas[0]}-{semillas[-1]}_{sello}'
    if not brazos or any(x not in BRAZOS for x in brazos) or len(set(brazos)) != len(brazos):
        raise SystemExit(f'brazos invalidos {brazos}; validos: {list(BRAZOS)}. Abortado.')
    os.makedirs(dest, exist_ok=True)
    tareas = [(s, b) for b in brazos for s in semillas]
    print(f'{pref}: {len(tareas)} corridas, T={MN.T_de()}, entrada campo a campo OK ({len(filas)} campos)', flush=True)
    t0 = time.time()
    if a.humo:
        res = []
        for tk in tareas:
            r = corre_uno(tk); res.append(r)
            print(f"  s{r['semilla']} {r['brazo']:7s} RET40 {r['RET40']} (com {r['RET40_com']} / ven {r['RET40_ven']}; rel {r['RET40_rel']} de {r['n_apr40']}) "
                  f"ADQ40_com {r['ADQ40_com']} | ADQ_tarde {r['ADQ_tarde']} com {r['ADQ_tarde_com']} prior_com {r['PRIOR_tarde_com']} nulo {r['NULO_tarde']} "
                  f"| muertes {r['muertes']} rep {r['n_rep']} (+{r['n_rep_pos']}) mord40c {r['mord40_com_ult']}/{r['vis40_com_ult']} {r['dur_s']}s", flush=True)
    else:
        from multiprocessing import Pool   # SOLO el coordinador
        with Pool(a.pool) as p:
            res = p.map(corre_uno, tareas)
    out = dict(pref=pref, humo=bool(a.humo), semillas=semillas, brazos=brazos, T=MN.T_de(), ventana=VENTANA, p_viejo=P_VIEJO,
               N_RET=N_RET, tramo_tarde=TRAMO_TARDE, tramo_temprano=TRAMO_TEMPRANO, perillas_v142=V142,
               shas={'organismo_repaso': SHA_ORG, 'organismo_v142': SHA_TRONCO, 'mundo_n8': SHA_MUN,
                     'corre_n8c': h16(os.path.abspath(__file__))},
               entrada_campo_a_campo=[list(map(str, f)) for f in filas], pared_s=round(time.time() - t0, 1),
               resultados=res, resumen=resumen(res))
    ruta = os.path.join(dest, pref + '.json')
    json.dump(out, open(ruta, 'w', encoding='utf-8'), indent=1, ensure_ascii=False)
    print(json.dumps({k: v for k, v in out['resumen'].items() if k != 'pareados'}, ensure_ascii=False))
    print(f'JSON: {os.path.relpath(ruta, RAIZ)}  sha {h16(ruta)}  pared {out["pared_s"]} s')
    ev = predicciones(res)
    if ev and not a.humo:
        imprime_ev('predicciones de esta serie (el veredicto exige serie Y replica: --veredicto)', ev)
    print('VEREDICTO: (humo: no es dato; la letra sale de --veredicto SERIE REPLICA)' if a.humo else
          'VEREDICTO: pendiente de la otra serie; correr --veredicto SERIE.json REPLICA.json')


if __name__ == '__main__':
    main()
