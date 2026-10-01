"""identidad_mm.py — ARNES de CONDICIONES / LA MONEDA DEL MURO (30-sep-2026, creador). Escribe su salida ENTERA en identidad_mm_salida.txt
(la cita el runner: sin 'ARNES: PASA' con los shas actuales, --explora no corre).

MISION: llegar a la AGI por este camino. Un proceso, sin Pool. Corridas cortas (T 1 000 / 500, s 638193) + DOS de T 25 000 (s 634110 y
634111: los pasajes p0 y p1 de la cadena moneda i1 GUARDADOS de condiciones/mutacion; con la moneda vieja deben salir BIT A BIT).
La moneda nueva se prueba sobre JSON GUARDADOS (pruebas de mutacion a 100k) y sobre casos sinteticos: no gasta corridas.

  python experimentos/organelos/condiciones/moneda_muro/identidad_mm.py
"""
import copy, json, os, sys, tempfile, time

AQUI = os.path.dirname(os.path.abspath(__file__))
if AQUI not in sys.path: sys.path.insert(0, AQUI)
import corre_mm as R   # noqa: E402
MU = R.MU; M = R.M; SM = R.SM; CBP = R.CBP; CV = SM.CV
N = lambda x: json.loads(json.dumps(x, default=str))
SALIDA = os.path.join(AQUI, 'identidad_mm_salida.txt')
IGN = {'seg', 'seg_trabajo', 'brazo_mm', 'moneda_siembra'}
KS_RUN = ['linajes', 'pista', 'R0_pista', 'tel', 'tel_termo', 'bq']


def main():
    LOGF = open(SALIDA, 'w', encoding='utf-8')
    def log(s=''): print(s, flush=True); LOGF.write(s + '\n'); LOGF.flush()
    t0 = time.time(); ok = True
    log(f"ARNES moneda del muro · {time.strftime('%Y-%m-%d %H:%M:%S')}")
    log(f"  shas: corre_mm.py {R.h16(os.path.join(AQUI, 'corre_mm.py'))} · identidad_mm.py {R.h16(os.path.abspath(__file__))}")
    SM.registra()
    log("(K) shas fijados (corre_mut, identidad_mut; por corre_mut.verifica: corre_moneda, sentidos_muro, corre_bp, V143_BQ3, pista, juez)")
    ok &= R.verifica(log)
    sd = R.SEM_ARNES; T = 1000

    log("(C) CONFIGURACION: CFG10 == corre_mut.CFG10; brazos -> filas y cfg de corre_mut; T_EST == juez.T_CORTE; siembra inicial == la de mutacion")
    c = R.CFG10 == MU.CFG10 and R.T_EST == CV.J.T_CORTE
    for b, (bm, mon) in R.BRAZOS.items():
        c &= MU.TASAS['div10'][bm][1] == MU.CFG10 and mon in ('L', 'vieja') and MU.siembra0(bm) == M.siembra0(bm) and M.frac(MU.siembra0(bm)) == 0.5
    c &= R.BRAZOS['moneda_L'][0] == R.BRAZOS['moneda_25'][0] == 'moneda' and R.BRAZOS['neutra_L'][0] == R.BRAZOS['neutra_25'][0] == 'neutra'
    c &= MU.TASAS['div10']['moneda'][0] == M.A == list(SM.FORZADA3[0]) and MU.TASAS['div10']['neutra'][0] == M.A0
    ok &= c; log(f"  CFG10 {R.CFG10} · T_EST {R.T_EST} (juez.T_CORTE {CV.J.T_CORTE}) · A {M.A} · A0 {M.A0} · B {M.B}: {'OK' if c else 'FALLA'}")

    log("(E) regla 14: ENTRADA campo a campo. tarea de este runner == corre_mut.tarea == corre_bp.tarea('V143_BQ3', CFG10, siembra)")
    for b in ('moneda_L', 'neutra_L'):
        bm = R.BRAZOS[b][0]; S = MU.siembra0(bm)
        x = N(R.tarea(sd, b, T, S)); y = N(MU.tarea(sd, bm, T, S, 'div10')); z = N(CBP.tarea(sd, 'V143_BQ3', T, cfg=dict(MU.CFG10), forzada=None, siembra=S))
        ks = sorted((set(x) | set(y)) - IGN); e = all(x.get(k) == y.get(k) for k in ks)
        kz = sorted((set(x) | set(z)) - IGN - {'brazo', 'carro'}); e &= all(x.get(k) == z.get(k) for k in kz) and x['bq']['cfg'] == MU.CFG10
        fu = [f_ for t in x['bq']['tel'].values() for f_ in t['fund']]; e &= len(fu) > 0 and all(f_[1] == 1 for f_ in fu)
        ok &= e; log(f"  {b}: {len(ks)} campos contra corre_mut y {len(kz)} contra corre_bp; cfg del carro == CFG10; fundadores del banco sembrado {len(fu)}/{len(fu)}: {'OK' if e else 'FALLA'}")

    log("(F) CON LA MONEDA VIEJA ESTE RUNNER ES corre_mut BIT A BIT")
    with tempfile.TemporaryDirectory() as td:
        d1 = os.path.join(td, 'r'); d2 = os.path.join(td, 'm'); os.makedirs(d1); os.makedirs(d2)
        R.MODOS['_tf'] = dict(ind=[9], npas=2, T_pas=1000, T_pru=1000, base_pas=638100, base_pru=638184, brazos=('moneda_25', 'neutra_25'))
        MU.MODOS['_tf'] = dict(ind=[9], npas=2, T_pas=1000, T_pru=1000, base_pas=638100, base_pru=638184, brazos=('moneda', 'neutra'), tasas='div10')
        for b in ('moneda', 'neutra'):
            o1 = R.trabajo((b + '_25', 9, d1, '_tf')); o2 = MU.trabajo((b, 9, d2, '_tf'))
            fs = sorted(f for f in os.listdir(d2) if f.startswith(f'pasaje_{b}') or f.startswith(f'{b}_s'))
            iguales = len(fs) >= 2
            for f in fs:
                f1 = os.path.join(d1, f.replace(b, b + '_25', 1)); iguales &= os.path.exists(f1)
                if not os.path.exists(f1): continue
                a_ = json.load(open(f1, encoding='utf-8')); b_ = json.load(open(os.path.join(d2, f), encoding='utf-8'))
                iguales &= all(a_.get(k) == b_.get(k) for k in (set(a_) | set(b_)) - IGN) and a_['moneda_siembra'] == 'vieja'
            i = iguales and o1['frac_A'] == o2['frac_A'] and o1['aborto'] is None and (b != 'moneda' or o1.get('cruzan') == o2.get('cruzan'))
            ok &= i; log(f"  trabajo {b}_25 (cadena 2 pasajes, T 1000) == corre_mut.trabajo('{b}'): {len(fs)} JSON campo a campo y frac_A "
                         f"{o1['frac_A']}: {'OK' if i else 'FALLA'}")
        del R.MODOS['_tf']; del MU.MODOS['_tf']
    sb = MU.siembra0('moneda'); refs = []
    for p, (f, sh) in enumerate(R.REF_PAS):
        s = R.h16(f); i = s == sh; ok &= i; log(f"  sha del pasaje guardado {os.path.basename(f)} {s}: {'OK' if i else 'FALLA'}")
        ref = json.load(open(f, encoding='utf-8')); refs.append(ref)
        i = ref['T'] == 25000 and ref['seed'] == 634110 + p and ref['bq']['cfg'] == R.CFG10; ok &= i
        t1 = time.time(); x = N(R.tarea(ref['seed'], 'moneda_25', ref['T'], sb))
        i = all(x.get(k) == ref.get(k) for k in KS_RUN); ok &= i
        sb2 = R.siembra(x, 'vieja'); j = sb2 == CBP.siembra_de(ref) and M.frac(sb2) == M.frac(CBP.siembra_de(ref)); ok &= j
        log(f"  mutacion moneda i1 p{p} (s {ref['seed']}, T {ref['T']}, {time.time()-t1:.0f}s) con la siembra que sale de este runner == GUARDADO en {KS_RUN}: "
            f"{'OK' if i else 'FALLA ' + str([k for k in KS_RUN if x.get(k) != ref.get(k)])} · siembra vieja == corre_bp.siembra_de (fraccion A {M.frac(sb2)}): {'OK' if j else 'FALLA'}")
        sb = sb2

    log("(J) 'establecido' con datos del linaje == el fund_post10k del juez, en TODOS los JSON guardados de mutacion (moneda: 50 pasajes + 5 pruebas)")
    fs = sorted(f for f in os.listdir(R.MUEXP) if f.startswith('pasaje_moneda_') or f.startswith('moneda_s'))
    nl = 0; bien = 0; inc = 0; G = {}
    for f in fs:
        x = json.load(open(os.path.join(R.MUEXP, f), encoding='utf-8')); G[f] = x; post = R.post10k(x)
        for l in x['linajes']:
            nl += 1; bien += int(post[int(l['indice'])] == l['fund_post10k']); inc += int(bool(l.get('fund_post_incierto')))
    i = nl == 9 * len(fs) and bien == nl and len(fs) == 55; ok &= i
    log(f"  {len(fs)} JSON, {bien}/{nl} linajes iguales (inciertos por tope de t_fund: {inc}): {'OK' if i else 'FALLA'}")

    log("(A) LA MONEDA NUEVA ACTUA (sobre los GUARDADOS de mutacion; sin corridas)")
    dif = 0; sub = True; solo = True; n = 0
    for f, x in G.items():
        SL = R.siembra_L(x); SV = CBP.siembra_de(x); idx, resp = R.elige(x); post = R.post10k(x); n += 1
        dif += int(SL != SV); kv = [json.dumps(r) for r in SV]
        sub &= all(json.dumps(r) in kv for r in SL) and len(SL) <= len(SV) and len(SL) > 0
        solo &= (all(post[k] == 0 for k in idx) if not resp else all(post[k] == min(post.values()) for k in idx))
        solo &= SL == [r for k in idx for r in x['bq']['banco'][str(k)] if r]
    i = dif > 0 and sub and solo; ok &= i
    log(f"  siembra_L != siembra vieja en {dif}/{n} JSON; siempre subconjunto no vacio: {sub}; solo bancos de linajes establecidos (o respaldo): {solo}: {'OK' if i else 'FALLA'}")
    for k, sh in zip(range(1, 6), R.REF_PRU):
        f = f"moneda_s{59200 + k}.json"; x = G[f]; s = R.h16(os.path.join(R.MUEXP, f)); i = s == sh; ok &= i
        idx, resp = R.elige(x)
        log(f"  {f} {s} {'OK' if i else 'FALLA'} · establecidos {len(idx)}/9 (respaldo {resp}) · listas {len(R.siembra_L(x))} vs {len(CBP.siembra_de(x))}")
    # sinteticos
    def lin(k, fund, tf): return dict(indice=k, fundadores=fund, telem=dict(t_fund=tf))
    RA = [list(M.A)]; RB = [list(M.B)]
    xs = dict(linajes=[lin(0, 0, []), lin(1, 2, [500, 9000]), lin(2, 3, [100, 200, 20000]), lin(3, 5, [50000] * 5)],
              bq=dict(banco={'0': [RA] * 3, '1': [RB] * 2, '2': [RA] * 4, '3': [RB] * 5}))
    i = R.post10k(xs) == {0: 0, 1: 0, 2: 1, 3: 5} and R.elige(xs) == ([0, 1], False) and R.siembra_L(xs) == [RA] * 3 + [RB] * 2 and CBP.siembra_de(xs) != R.siembra_L(xs)
    xr = dict(linajes=[lin(0, 4, [20000] * 4), lin(1, 2, [500, 30000]), lin(2, 1, [40000]), lin(3, 0, [])],
              bq=dict(banco={'0': [RA], '1': [RB] * 2, '2': [RA] * 4, '3': []}))
    i &= R.elige(xr) == ([1, 2], True) and R.siembra_L(xr) == [RB] * 2 + [RA] * 4   # el establecido 3 tiene el banco vacio: respaldo = minimo (1)
    xv = dict(linajes=[lin(0, 1, [40000])], bq=dict(banco={'0': []}))
    i &= R.elige(xv) == ([], True) and R.siembra_L(xv) == []
    xt = dict(linajes=[lin(0, 250, [5] * 200)], bq=dict(banco={'0': [RA]}))   # t_fund truncado a 200: los que faltan cuentan como posteriores
    i &= R.post10k(xt) == {0: 50}
    ok &= i; log(f"  sinteticos (establecidos, respaldo por minimo, banco vacio, siembra vacia, t_fund truncado): {'OK' if i else 'FALLA'}")

    log("(D) determinismo: moneda_L, dos veces")
    a1 = N(R.tarea(sd, 'moneda_L', T, MU.siembra0('moneda'))); a2 = N(R.tarea(sd, 'moneda_L', T, MU.siembra0('moneda')))
    a1.pop('seg'); a2.pop('seg'); i = a1 == a2; ok &= i; log(f"  {'OK' if i else 'FALLA'}")

    log("(W) JSON antes de volver; un JSON con aborto SE REINTENTA; uno bueno NO se recorre; cadena por trabajo() con aborto simulado y reanuda; cadena() == trabajo()")
    with tempfile.TemporaryDirectory() as td:
        fin = os.path.join(td, 'x.json'); M._guarda(fin, dict(seed=sd, brazo='moneda', aborto='prueba', linajes=[]))
        S = MU.siembra0('moneda')
        x1 = R._corrida(fin, sd, 'moneda_L', 500, S, dict(i=0)); x2 = R._corrida(fin, sd, 'moneda_L', 500, S, dict(i=0))
        i = x1.get('aborto') is None and x1.get('reintento_de') == 'aborto' and x2 == json.load(open(fin, encoding='utf-8')) and x2['seg_trabajo'] == x1['seg_trabajo']
        i &= x1['brazo_mm'] == 'moneda_L' and x1['moneda_siembra'] == 'L'
        ok &= i; log(f"  reintento: {'OK' if i else 'FALLA'}")
        R.MODOS['_t'] = dict(ind=[9], npas=2, T_pas=500, T_pru=500, base_pas=638100, base_pru=638184, brazos=('moneda_L', 'neutra_L'))
        for b in ('moneda_L', 'neutra_L'):
            o1 = R.trabajo((b, 9, td, '_t'))
            f1 = os.path.join(td, f'pasaje_{b}_i9_p1.json'); xx = json.load(open(f1, encoding='utf-8')); xx['aborto'] = 'simulado'; M._guarda(f1, xx)
            o2 = R.trabajo((b, 9, td, '_t'))
            c9, _ = R.cadena(td, R.MODOS['_t'], b, 9)
            i = o1['aborto'] is None and o2['aborto'] is None and o1['frac_A'] == o2['frac_A'] == [c9['f_ini']] + c9['f'] and o1['cruzan'] == o2['cruzan']
            i &= os.path.exists(os.path.join(td, f'{b}_s638193.json'))
            ok &= i; log(f"  {b}: cadena 2 pasajes + prueba, aborto simulado en p1 y reanuda: identico ({o1['frac_A']}, cruzan {o1['cruzan']}; elegidos {c9['n_ele']}): {'OK' if i else 'FALLA'}")
        C, P_, refs_, ab, rok, rtx = R.carga(td, '_t'); i = not ab and all(len(P_[b]) == 1 for b in P_); ok &= i
        log(f"  carga() de la carpeta: 2 cadenas y 2 pruebas, abortos {ab}: {'OK' if i else 'FALLA'}")
        del R.MODOS['_t']

    log("(X) el runner NIEGA pool > 2 y pool en el humo")
    for argv in (['--explora', '--pool', '3'], ['--humo', '--pool', '2']):
        try: R.main(argv); i = False
        except SystemExit as e: i = 'maximo' in str(e) or 'sin Pool' in str(e)
        ok &= i; log(f"  {argv}: {'OK (niega)' if i else 'FALLA'}")

    log("(L) LA LETRA en casos sinteticos (ERR-176: CONSERVA exige 5/5)")
    ind = [1, 2, 3, 4, 5]
    def cad(f, fi=0.5, sombra=0.3, resp=(False, False)): return dict(f_ini=fi, f=[0.4, f], f_sombra_vieja=[0.45, sombra], respaldo=list(resp), n_ele=[4, 5])
    def tb(mo, ne, **kw): return {'moneda_L': {i: cad(mo[i - 1], **kw) for i in ind}, 'neutra_L': {i: cad(ne[i - 1], **kw) for i in ind}}
    casos = [('CONSERVA: moneda >= neutra en 5/5 y mediana 0.6', tb([1, 1, .6, .5, .3], [1, 0, .5, .2, .1]), [], 'CONSERVA'),
             ('ERR-176: 4/5 con mediana 0.6 YA NO es CONSERVA', tb([1, 1, .6, .5, 0], [1, 0, .5, .2, 1]), [], 'INDETERMINADO'),
             ('CONSERVA: los empates cuentan (>=), 5/5', tb([1, 1, 1, 0, 1], [1, 1, 1, 0, 1]), [], 'CONSERVA'),
             ('ERR-176: empates y 4/5 no es CONSERVA', tb([1, 1, 1, 0, 0], [1, 1, 1, 0, 1]), [], 'INDETERMINADO'),
             ('CONSERVA en el borde: mediana == 0.40 y 5/5', tb([.4, .4, .4, .1, .9], [.3, .3, .3, .1, .2]), [], 'CONSERVA'),
             ('no CONSERVA si la mediana < 0.40 aunque >= en 5/5', tb([.3, .3, .3, .3, .9], [.2, .2, .2, .2, .2]), [], 'INDETERMINADO'),
             ('no CONSERVA con 3/5', tb([1, 1, 1, 0, 0], [0, 0, 0, 1, 1]), [], 'INDETERMINADO'),
             ('PURGA: <= 0.5 neutra en 4/5', tb([.1, .1, .05, 0, 1], [.3, .2, .3, .3, .3]), [], 'PURGA'),
             ('PURGA: == 0.5 neutra cuenta', tb([.15, .1, .15, .1, .4], [.3, .2, .3, .2, .3]), [], 'PURGA'),
             ('no PURGA: 0 contra 0 no cuenta (2/5)', tb([0, 0, 0, 0, 0], [0, 0, 0, 1, 1]), [], 'INDETERMINADO'),
             ('todas perdidas en los dos brazos: INDETERMINADO', tb([0] * 5, [0] * 5), [], 'INDETERMINADO'),
             ('NO SE LEE (aborto)', tb([1] * 5, [0] * 5), ['x'], 'NO SE LEE'),
             ('NO SE LEE (la moneda no actua: siembra == sombra en todos)', {b: {i: dict(c, f_sombra_vieja=list(c['f'])) for i, c in d.items()}
                                                                             for b, d in tb([1] * 5, [0] * 5).items()}, [], 'NO SE LEE'),
             ('NO SE LEE (respaldo en > 25 % de los pasajes)', tb([1] * 5, [0] * 5, resp=(True, False)), [], 'NO SE LEE'),
             ('NO SE LEE (entrada != 0.5)', tb([1] * 5, [0] * 5, fi=0.6), [], 'NO SE LEE')]
    ok &= R.CONSERVA_N == 5 and R.PURGA_N == 4
    for txt, C, ab, e in casos:
        L = R.letra(C, ind, ab, True, True, n_pru=10); i = L['veredicto'] == e; ok &= i
        log(f"  {txt}: {L['veredicto']} (espera {e}) {'OK' if i else 'FALLA'}")
    for txt, kw in (('arnes', dict(ref_ok=True, arnes_ok=False, n_pru=10)), ('referencias', dict(ref_ok=False, arnes_ok=True, n_pru=10)),
                    ('faltan pruebas', dict(ref_ok=True, arnes_ok=True, n_pru=9))):
        L = R.letra(tb([1] * 5, [0] * 5), ind, [], **kw); i = L['veredicto'] == 'NO SE LEE'; ok &= i
        log(f"  NO SE LEE ({txt}): {L['veredicto']} {'OK' if i else 'FALLA'}")

    log("(R) referencias GUARDADAS de condiciones/mutacion (sha16): lectura, 5 pruebas de moneda / 10")
    rok, rtx, refs = R.refs_mutacion()
    i = rok and refs['sumas'].get('moneda_div10') == sum(f['cruzan'] for f in refs['prueba'].values()) and len(refs['final']['moneda_25']) == 5; ok &= i
    log(f"  lectura_mut.json {R.h16(R.REF_LECT[0])} · finales {refs['final']} · sumas {refs['sumas']} · {rtx}: {'OK' if i else 'FALLA'}")
    log(f"ARNES: {'PASA' if ok else 'FALLA'} · {time.time()-t0:.0f}s")
    return 0 if ok else 1


if __name__ == '__main__':
    sys.exit(main())
