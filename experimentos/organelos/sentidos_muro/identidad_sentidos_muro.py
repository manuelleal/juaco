"""identidad_sentidos_muro.py — ARNES de SENTIDOS CONTRA EL MURO (29-sep-2026, creador). Escribe su salida ENTERA en
identidad_sentidos_muro_salida.txt (la cita el runner: sin 'ARNES: PASA' con los shas actuales, --explora no corre).

MISION: llegar a la AGI por este camino. Un proceso, sin Pool. Corridas: muchas de T 2 000 (s 614992) + UNA de T 100 000 (s 59201: la
reproduccion bit a bit de la referencia guardada bloq2).

  python experimentos/organelos/sentidos_muro/identidad_sentidos_muro.py
"""
import copy, json, os, sys, tempfile, time

AQUI = os.path.dirname(os.path.abspath(__file__))
if AQUI not in sys.path: sys.path.insert(0, AQUI)
import corre_sentidos_muro as R   # noqa: E402
CBP = R.CBP; CV = R.CV; P = R.P
N = lambda x: json.loads(json.dumps(x, default=str))
SALIDA = os.path.join(AQUI, 'identidad_sentidos_muro_salida.txt')


def main():
    LOGF = open(SALIDA, 'w', encoding='utf-8')
    def log(s=''): print(s, flush=True); LOGF.write(s + '\n'); LOGF.flush()
    t0 = time.time(); ok = True
    log(f"ARNES sentidos_muro · {time.strftime('%Y-%m-%d %H:%M:%S')}")
    log(f"  shas: corre_sentidos_muro.py {R.h16(os.path.join(AQUI, 'corre_sentidos_muro.py'))} · construye_sm.py {R.h16(os.path.join(AQUI, 'construye_sm.py'))} · "
        f"V143_BQ3.py {R.h16(os.path.join(R.CARROS, 'V143_BQ3.py'))} · V143_BQ3_0.py {R.h16(os.path.join(R.CARROS, 'V143_BQ3_0.py'))} · "
        f"identidad_sentidos_muro.py {R.h16(os.path.abspath(__file__))}")
    R.registra()
    log("(K) shas fijados, carros == construye_sm, revisa_carro; CFG del runner == BQ_C del carro == corre_bp.CFG0")
    ok &= R.verifica(log)
    c1 = R.CFG == CV._MODS['V143_BQ3'].BQ_C == CV._MODS['V143_BQ2'].BQ_C == CBP.CFG0; ok &= c1
    log(f"  CFG {R.CFG} == carro == CFG0: {'OK' if c1 else 'FALLA'}")
    sd = R.SEM_ARNES; T = 2000

    def run(ident, cfg, forz=None, siembra=None, seed=sd, TT=T):
        CBP.prepara(ident, seed, dict(cfg), copy.deepcopy(forz), siembra)
        return N(P.run(seed, [('C', CV._MODS[ident])] * 9, T=TT, fundador_limpio=1))

    log(f"(A) SENT3 = 0 == V143_BQ2 BIT A BIT con tasas de EXPLORACION (salida ENTERA de pista.run, N 9, s {sd}, T {T}, fundador limpio)")
    b2 = run('V143_BQ2', R.CFG); a0 = run('V143_BQ3_0', R.CFG); i = a0 == b2; ok &= i
    log(f"  V143_BQ3_0 == V143_BQ2 (CFG): {'OK' if i else 'FALLA'}")
    # (arreglo antes de datos, ver PREREGISTRO sec. 11: la version 1 forzaba la regla de SENTIDO 10, que BQ2 no tiene; con SENT3 = 0 el
    #  codigo de 9 y 10 sigue en el carro pero la mutacion no lo alcanza (NSEN 9). Se compara con la regla PRUEBA_O1 de sentidos 7 y 8.)
    b2s = run('V143_BQ2', R.CERO, CBP.PRUEBA_O1); a0s = run('V143_BQ3_0', R.CERO, CBP.PRUEBA_O1); i = a0s == b2s; ok &= i
    log(f"  V143_BQ3_0 == V143_BQ2 (tasas 0, misma regla forzada PRUEBA_O1 de sentidos 7 y 8): {'OK' if i else 'FALLA'}")
    d = run('V143_BQ2', R.CERO, R.FORZADA3) != run('V143_BQ3', R.CERO, R.FORZADA3); ok &= d
    log(f"  control que DEBE diferir: regla de sentido 10 forzada en BQ2 (no lo tiene) != en BQ3: {'OK (difiere)' if d else 'FALLA (igual)'}")
    log("(B) SENT3 = 1 con genoma vacio y tasas 0 == V143_TERMO (salida ENTERA)")
    te = N(P.run(sd, [('C', CV._MODS['V143_TERMO'])] * 9, T=T, fundador_limpio=1))
    i = run('V143_BQ3', R.CERO) == te; ok &= i; log(f"  V143_BQ3 vacio == V143_TERMO: {'OK' if i else 'FALLA'}")
    i = run('V143_BQ3_0', R.CERO) == te; ok &= i; log(f"  V143_BQ3_0 vacio == V143_TERMO: {'OK' if i else 'FALLA'}")
    log("(C) controles que DEBEN diferir: SENT3 = 1 con CFG != BQ2; la regla de riesgo forzada != TERMO y ACTUA")
    a1 = run('V143_BQ3', R.CFG); d = a1 != b2; ok &= d; log(f"  V143_BQ3 (CFG) != V143_BQ2 (CFG): {'OK (difiere)' if d else 'FALLA (igual)'}")
    f3 = run('V143_BQ3', R.CERO, R.FORZADA3); d = f3 != te; ok &= d
    Lt = [CV.J.resumen_linaje(x, sd) for x in te['linajes']]; Lf = [CV.J.resumen_linaje(x, sd) for x in f3['linajes']]
    s = lambda L, ks: sum(l['mord'][k] for l in L for k in ks)
    log(f"  forzada3 != TERMO: {'OK' if d else 'FALLA'} · mordidas B+D {s(Lt, 'BD')} -> {s(Lf, 'BD')} · A+C {s(Lt, 'AC')} -> {s(Lf, 'AC')} · "
        f"fundadores {sum(l['fundadores'] for l in Lt)} -> {sum(l['fundadores'] for l in Lf)} (T {T}; solo dice que actua)")
    log("(S) sentidos 9 y 10 con un objeto de prueba (sin correr la pista)")
    M = CV._MODS['V143_BQ3']; c = object.__new__(M.Carro)
    c._adS = {'A': [0.8, 0.0, 1], 'B': [-0.4, 0.0, 1], 'C': [0.0, 0.0, 2]}; c._bqcache = (10, {12: 'B', 15: 'A', 30: 'C', 38: 'D'}, 40, {})
    casos = [('s9: A sentida buena a d 5 (C nula no cuenta)', c._bq_sen(9, 0, 0.9, 0.9, 0, 'B'), 0.75),
             ('s10: foco A sentida buena', c._bq_sen(10, 0, 0.3, 0.3, 0, 'A'), 0.0),
             ('s10: foco B sentida mala, E 0.3 Ag 0.9', c._bq_sen(10, 0, 0.3, 0.9, 0, 'B'), 0.7),
             ('s10: foco D desconocida, E 0.9 Ag 0.8', c._bq_sen(10, 0, 0.9, 0.8, 0, 'D'), 0.2),
             ('s10: foco C nula (media 0) cuenta como NO buena, E 1.2', c._bq_sen(10, 0, 1.2, 1.3, 0, 'C'), 0.0),
             ('s8 reserva sin cambios', c._bq_sen(8, 0, 0.3, 0.9, 0, 'B'), 0.3)]
    c2 = object.__new__(M.Carro); c2._adS = {}; c2._bqcache = (10, {12: 'B', 15: 'A'}, 40, {})
    casos.append(('s9: linaje sin nada sentido -> 0', c2._bq_sen(9, 0, 0.5, 0.5, 0, 'B'), 0.0))
    for txt, v, e in casos:
        i = abs(v - e) < 1e-9; ok &= i; log(f"  {txt}: {v:.6f} (espera {e}) {'OK' if i else 'FALLA'}")
    log("(E) regla 14: ENTRADA campo a campo contra el tronco de la medida (corre_bp.tarea)")
    x = N(R.tarea(sd, 'bq3', T)); y = N(CBP.tarea(sd, 'V143_BQ3', T, cfg=dict(R.CFG)))
    ks = sorted((set(x) | set(y)) - {'seg', 'brazo', 'carro', 'aborto'}); e = all(x.get(k) == y.get(k) for k in ks); ok &= e
    log(f"  bq3 == corre_bp.tarea(V143_BQ3, CFG): {len(ks)} campos {'OK' if e else 'FALLA ' + str([k for k in ks if x.get(k) != y.get(k)][:5])}")
    x = json.loads(json.dumps(N(R.tarea(sd, 'bq2_pas', T))).replace('V143_BQ2#', 'V143_BQ2#'))
    y = N(CBP.tarea(sd, 'bloq2', T))
    ks = sorted((set(x) | set(y)) - {'seg', 'brazo', 'carro', 'aborto'}); e = all(x.get(k) == y.get(k) for k in ks); ok &= e
    log(f"  bq2_pas (sin siembra) == corre_bp.tarea('bloq2') con CFG0: {len(ks)} campos {'OK' if e else 'FALLA ' + str([k for k in ks if x.get(k) != y.get(k)][:5])}")
    z = json.loads(json.dumps(N(CBP.tarea(sd, 'V143_BQ3_0', T, cfg=dict(R.CFG)))).replace('V143_BQ3_0#', 'V143_BQ2#'))
    kz = [k for k in ks if k not in ('bq',)]; e = all(z.get(k) == y.get(k) for k in kz) and z['bq']['banco'] == y['bq']['banco']; ok &= e
    log(f"  tarea V143_BQ3_0 == tarea V143_BQ2 (ids normalizados; banco final igual): {'OK' if e else 'FALLA ' + str([k for k in kz if z.get(k) != y.get(k)][:5])}")
    log("(P) pasaje: la siembra ACTUA (todo fundador de la prueba sale del banco sembrado) y siembra_de solo toma listas no vacias")
    xp = R.tarea(sd, 'bq3', T); sb = CBP.siembra_de(xp)
    xq = R.tarea(sd + 1, 'bq3', T, siembra=sb); fu = [f for t in xq['bq']['tel'].values() for f in t['fund']]
    i = bool(sb) and all(len(r) > 0 for r in sb) and len(fu) > 0 and all(f[1] == 1 for f in fu); ok &= i
    log(f"  siembra {len(sb)} listas · fundadores de la prueba {len(fu)}, del banco {sum(f[1] == 1 for f in fu)}: {'OK' if i else 'FALLA'}")
    log("(D) determinismo: bq3 con CFG, dos veces")
    a1 = N(R.tarea(sd, 'bq3', T)); a2 = N(R.tarea(sd, 'bq3', T)); a1.pop('seg'); a2.pop('seg'); i = a1 == a2; ok &= i
    log(f"  {'OK' if i else 'FALLA'}")
    log("(W) JSON antes de volver; un JSON con aborto SE REINTENTA; uno bueno NO se recorre")
    with tempfile.TemporaryDirectory() as td:
        fin = os.path.join(td, 'x.json'); R._guarda(fin, dict(seed=sd, brazo='bq3', aborto='prueba', linajes=[]))
        x1 = R._corrida(fin, sd, 'bq3', 500, None, dict(i=0)); x2 = R._corrida(fin, sd, 'bq3', 500, None, dict(i=0))
        i = x1.get('aborto') is None and x1.get('reintento_de') == 'aborto' and x2 == json.load(open(fin, encoding='utf-8')) and x2['seg_trabajo'] == x1['seg_trabajo']
        ok &= i; log(f"  {'OK' if i else 'FALLA'}")
    log("(L) LA LETRA en casos sinteticos (tab[brazo][i] = cruzan, mayoria, R0, coherente)")
    def fx(cz): return dict(cruzan=cz, mayoria=int(cz * 2 > 9), R0_med=0.6, coherente=True, seed=0)
    base = {'v143': [2] * 5, 'termo': [4] * 5, 'o1': [8] * 5, 'bloq2': [4] * 5, 'forzada3': [5] * 5}
    ind = [1, 2, 3, 4, 5]
    def tb(b3p, b2p, b3):
        t = {k: {i: fx(v[i - 1]) for i in ind} for k, v in dict(base, bq3_pas=b3p, bq2_pas=b2p, bq3=b3).items()}
        return t
    pruebas = [('FUNCIONA', tb([6, 6, 7, 5, 3], [4, 4, 4, 4, 4], [3, 3, 3, 3, 3]), 0, True, True),
               ('MODESTO (3/5 y 3/5, mayoria 3)', tb([6, 6, 5, 4, 3], [4, 4, 4, 4, 4], [3, 3, 3, 4, 4]), 0, True, True),
               ('MODESTO (suma +5)', tb([4, 4, 4, 4, 9], [4, 4, 4, 4, 4], [4, 4, 4, 4, 4]), 0, True, True),
               ('NO (empates no ganan)', tb([4, 4, 4, 4, 4], [4, 4, 4, 4, 4], [4, 4, 4, 4, 4]), 0, True, True),
               ('NO SE LEE (aborto)', tb([6, 6, 7, 5, 5], [4, 4, 4, 4, 4], [3, 3, 3, 3, 3]), 1, True, True),
               ('NO SE LEE (arnes)', tb([6, 6, 7, 5, 5], [4, 4, 4, 4, 4], [3, 3, 3, 3, 3]), 0, True, False)]
    esper = ['FUNCIONA', 'HAY ALGO MODESTO', 'HAY ALGO MODESTO', 'NO', 'NO SE LEE', 'NO SE LEE']
    for (txt, t, ab, rf, ar), e in zip(pruebas, esper):
        for k in ('v143',):
            for i in ind: t[k][i]['R0_med'] = 0.6
        L = R.letra(t, ind, ['x'] * ab, rf, ar); i = L['veredicto'] == e; ok &= i
        log(f"  {txt}: {L['veredicto']} (espera {e}) {'OK' if i else 'FALLA'}")
    log(f"(R) referencias GUARDADAS: sha16 de los 20 JSON y reproduccion BIT A BIT de bloq2 s59201 T 100 000 por este runner")
    for b, (dd, shas) in R.REFS.items():
        for i, sh in zip(ind, shas):
            f = os.path.join(dd, f"{b}_s{59200 + i}.json"); s = R.h16(f); ok &= s == sh
            log(f"  {b} s{59200 + i} {s} {'OK' if s == sh else '!= ' + sh + ' FALLA'}")
    t1 = time.time(); x = N(R.tarea(59201, 'bq2_pas', 100000)); ref = json.load(open(os.path.join(R.EXP, 'bloq2_s59201.json'), encoding='utf-8'))
    ks = [k for k in ('linajes', 'pista', 'R0_pista', 'tel', 'tel_termo', 'bq') if k in ref]
    i = all(x.get(k) == ref.get(k) for k in ks); ok &= i
    log(f"  bloq2 s59201 T 100k ({time.time()-t1:.0f}s) == guardado en {ks}: {'OK' if i else 'FALLA ' + str([k for k in ks if x.get(k) != ref.get(k)])}")
    log(f"ARNES: {'PASA' if ok else 'FALLA'} · {time.time()-t0:.0f}s")
    return 0 if ok else 1


if __name__ == '__main__':
    sys.exit(main())
