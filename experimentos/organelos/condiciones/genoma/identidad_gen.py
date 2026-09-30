"""identidad_gen.py — ARNES de CONDICIONES / GENOMA (30-sep-2026, creador). Escribe su salida ENTERA en identidad_gen_salida.txt (la cita el
runner: sin 'ARNES: PASA' con los shas actuales, --explora no corre).

MISION: llegar a la AGI por este camino. Un proceso, sin Pool. Corridas cortas (T 2 000, s 635192) + UNA de T 25 000 (s 614010: el pasaje p0
de la cadena bq2_pas i1 de sentidos_muro GUARDADO el 29-sep; el brazo fab debe salir BIT A BIT).

  python experimentos/organelos/condiciones/genoma/identidad_gen.py
"""
import json, os, sys, tempfile, time
import numpy as np

AQUI = os.path.dirname(os.path.abspath(__file__))
if AQUI not in sys.path: sys.path.insert(0, AQUI)
import corre_gen as R   # noqa: E402
SM = R.SM; CBP = R.CBP; CV = R.CV; P = SM.P
N = lambda x: json.loads(json.dumps(x, default=str))
SALIDA = os.path.join(AQUI, 'identidad_gen_salida.txt')
IGN = {'seg', 'seg_trabajo', 'brazo', 'siembra_tam_por_pasaje'}
KS_RUN = ['linajes', 'pista', 'R0_pista', 'tel', 'tel_termo', 'bq']


def _fake(carro, seed):
    Car = CV._MODS[carro].Carro

    class F: pass
    f = F(); f._bqrng = np.random.default_rng(seed); f._bq_azar = lambda: Car._bq_azar(f)
    return Car, f


def muta_delta(carro, cfg, n, seed):
    """El operador del carro (_bq_muta) sobre listas de 6 reglas al azar: delta de largo medio por parto."""
    mod = CV._MODS[carro]; viejo = mod.BQ_C; mod.BQ_C = dict(cfg); Car, f = _fake(carro, seed); dl = 0
    try:
        for _ in range(n):
            base = [f._bq_azar() for _ in range(6)]; dl += len(Car._bq_muta(f, base)) - 6
    finally:
        mod.BQ_C = viejo
    return dl / n


def main():
    LOGF = open(SALIDA, 'w', encoding='utf-8')
    def log(s=''): print(s, flush=True); LOGF.write(s + '\n'); LOGF.flush()
    t0 = time.time(); ok = True
    log(f"ARNES genoma · {time.strftime('%Y-%m-%d %H:%M:%S')}")
    log(f"  shas: corre_gen.py {R.h16(os.path.join(AQUI, 'corre_gen.py'))} · identidad_gen.py {R.h16(os.path.abspath(__file__))}")
    SM.registra()
    log("(K) shas fijados (sentidos_muro, corre_bp, V143_BQ2, V143_BQ2AZA; por sentidos_muro.verifica: TERMO, pista, juez, O1, V143, carros)")
    ok &= R.verifica(log)
    sd = R.SEM_ARNES; T = 2000

    log("(C) CONFIGURACION: CAP = CFG de fabrica con inicial 6 y p_dup 0.06 (nada mas); CFG == sentidos_muro == corre_bp.CFG0 == carros")
    c = R.CFG == SM.CFG == CBP.CFG0 == CV._MODS['V143_BQ2'].BQ_C == CV._MODS['V143_BQ2AZA'].BQ_C
    c &= {k: v for k, v in R.CAP.items() if R.CFG[k] != v} == {'inicial': 6, 'p_dup': 0.06} and set(R.CAP) == set(R.CFG)
    c &= R.TASAS['cap']['fab'] == ('V143_BQ2', R.CFG) and R.TASAS['cap']['cap'] == ('V143_BQ2', R.CAP) and R.TASAS['cap']['aza_largo'] == ('V143_BQ2AZA', R.CAP)
    dcap = R.CAP['p_dup'] + R.CAP['p_ins'] - R.CAP['p_del']; dfab = R.CFG['p_dup'] + R.CFG['p_ins'] - R.CFG['p_del']
    c &= abs(dcap - 0.04) < 1e-12 and abs(dfab) < 1e-12
    ok &= c; log(f"  CFG {R.CFG} · CAP {R.CAP} · delta largo esperado: cap {dcap:+.3f}, fab {dfab:+.3f}: {'OK' if c else 'FALLA'}")

    log("(F) A TASAS DE FABRICA ESTE RUNNER ES EL INSTRUMENTO ORIGINAL BIT A BIT")
    x = N(R.tarea(sd, 'fab', T)); y = N(SM.tarea(sd, 'bq2_pas', T))
    ks = sorted((set(x) | set(y)) - IGN); e = all(x.get(k) == y.get(k) for k in ks); ok &= e
    log(f"  fab == sentidos_muro.tarea('bq2_pas') sin siembra: {len(ks)} campos {'OK' if e else 'FALLA ' + str([k for k in ks if x.get(k) != y.get(k)][:5])}")
    S = CBP.siembra_de(x)
    x2 = N(R.tarea(sd + 1, 'fab', T, S)); y2 = N(SM.tarea(sd + 1, 'bq2_pas', T, S))
    e = all(x2.get(k) == y2.get(k) for k in ks) and len(S) > 0; ok &= e
    log(f"  fab == sentidos_muro.tarea('bq2_pas') con siembra ({len(S)} listas): {'OK' if e else 'FALLA'}")
    x = N(R.tarea(sd, 'aza_largo', T, None, 'fabrica')); y = N(CBP.tarea(sd, 'bloq2aza', T))
    ks2 = sorted((set(x) | set(y)) - IGN - {'carro'}); e = all(x.get(k) == y.get(k) for k in ks2); ok &= e
    log(f"  aza_largo a tasas de fabrica == corre_bp.tarea('bloq2aza'): {len(ks2)} campos {'OK' if e else 'FALLA'}")
    x = N(R.tarea(sd, 'cap', T, None, 'fabrica')); y = N(R.tarea(sd, 'fab', T))
    e = all(x.get(k) == y.get(k) for k in ks); ok &= e
    log(f"  cap a tasas de fabrica == fab: {'OK' if e else 'FALLA'}")
    with tempfile.TemporaryDirectory() as td:
        d1 = os.path.join(td, 'r'); d2 = os.path.join(td, 's'); os.makedirs(d1); os.makedirs(d2)
        R.MODOS['_tf'] = dict(ind=[9], npas=2, T_pas=1000, T_pru=1000, base_pas=635000, base_pru=635180, tasas='fabrica')
        SM.MODOS['_tf'] = dict(ind=[9], npas=2, T_pas=1000, T_pru=1000, base_pas=635000, base_pru=635180)
        o1 = R.trabajo(('fab', 9, d1, '_tf')); o2 = SM.trabajo(('pas', 9, 'bq2_pas', d2, '_tf'))
        pares = [(f"pasaje_fab_i9_p{p}.json", f"pasaje_bq2_pas_i9_p{p}.json") for p in range(2)] + [("fab_s635189.json", "bq2_pas_s635189.json")]
        iguales = True
        for a_, b_ in pares:
            xa = json.load(open(os.path.join(d1, a_), encoding='utf-8')); xb = json.load(open(os.path.join(d2, b_), encoding='utf-8'))
            iguales &= all(xa.get(k) == xb.get(k) for k in (set(xa) | set(xb)) - IGN)
        i = iguales and o1['aborto'] is None and o2['aborto'] is None and o1['cruzan'] == o2['cruzan'] and o1['R0'] == o2['R0']
        ok &= i; log(f"  trabajo fab == sentidos_muro.trabajo('pas', 'bq2_pas') (2 pasajes + prueba, T 1000): 3 JSON campo a campo, cruzan {o1['cruzan']}: "
                     f"{'OK' if i else 'FALLA'}")
        del R.MODOS['_tf']; del SM.MODOS['_tf']
    f, sh = R.REF_P0; s = R.h16(f); i = s == sh; ok &= i; log(f"  sha del pasaje guardado {os.path.basename(f)} {s}: {'OK' if i else 'FALLA'}")
    ref = json.load(open(f, encoding='utf-8'))
    t1 = time.time(); x = N(R.tarea(ref['seed'], 'fab', ref['T']))
    i = all(x.get(k) == ref.get(k) for k in KS_RUN); ok &= i
    log(f"  bq2_pas i1 p0 (s {ref['seed']}, T {ref['T']}, {time.time()-t1:.0f}s) por el brazo fab == GUARDADO 29-sep en {KS_RUN}: "
        f"{'OK' if i else 'FALLA ' + str([k for k in KS_RUN if x.get(k) != ref.get(k)])}")

    log("(A) LAS TASAS NUEVAS ACTUAN")
    for b in ('fab', 'cap', 'aza_largo'):
        x = N(R.tarea(sd, b, T)); fu = [ff[2] for t in x['bq']['tel'].values() for ff in t['fund'] if ff[1] == 0]
        esp = R.TASAS['cap'][b][1]['inicial']; md = float(np.median(fu)) if fu else None
        i = x['bq']['cfg'] == R.TASAS['cap'][b][1] and md is not None and abs(md - esp) <= 1; ok &= i
        log(f"  {b}: cfg del carro == {'CAP' if esp == 6 else 'CFG'}; largo mediano de los fundadores sin banco {md} (inicial {esp}; n {len(fu)}): {'OK' if i else 'FALLA'}")
    n = 60000
    d_cap = muta_delta('V143_BQ2', R.CAP, n, sd); d_fab = muta_delta('V143_BQ2', R.CFG, n, sd + 1)
    i = 0.03 <= d_cap <= 0.05 and -0.01 <= d_fab <= 0.01; ok &= i
    log(f"  operador _bq_muta del carro sobre listas de 6 reglas ({n} partos): delta largo cap {d_cap:+.4f} (espera +0.04), fab {d_fab:+.4f} (espera 0): "
        f"{'OK' if i else 'FALLA'}")

    log("(M) LA MEDIDA: es_doble / es_o1 en casos y piso de azar p_azar(n) contra Monte Carlo con el _bq_azar del carro")
    casos = [([[7, 0, 0, .5, 0, -3], [8, 0, 1, .5, 0, 3]], True, True), ([[7, 0, 0, .5, 0, -3], [7, 2, 1, .5, 0, 1]], True, False),
             ([[7, 0, 0, .5, 0, -3], [8, 0, 1, .5, 1, 3]], False, False), ([[7, 0, 0, .5, 0, -3], [8, 0, 1, .5, 0, -3]], False, False),
             ([[8, 0, 1, .5, 0, 3], [3, 4, 1, .5, 0, -3]], False, False), ([[7, 0, 1, .5, 0, -3], [8, 0, 1, .5, 0, 3]], True, False), ([], False, False)]
    for Rr, ed, eo in casos:
        i = R.es_doble(Rr) == ed and R.es_o1(Rr) == eo; ok &= i
        log(f"  {Rr}: doble {R.es_doble(Rr)} (espera {ed}) · O1 {R.es_o1(Rr)} (espera {eo}): {'OK' if i else 'FALLA'}")
    i = all(R.es_o1(Rr) for Rr in [CBP.PRUEBA_O1]) and R.es_doble(CBP.PRUEBA_O1); ok &= i
    log(f"  corre_bp.PRUEBA_O1 es doble y tiene forma O1: {'OK' if i else 'FALLA'}")
    Car, f = _fake('V143_BQ2', sd + 2)
    for nn, K in ((6, 100000), (2, 100000)):
        mc = sum(R.es_doble([f._bq_azar() for _ in range(nn)]) for _ in range(K)) / K; pa = R.p_azar(nn)
        i = abs(mc - pa) <= 4 * np.sqrt(pa * (1 - pa) / K); ok &= i
        log(f"  p_azar({nn}) {pa:.4f} vs Monte Carlo {mc:.4f} (K {K}): {'OK' if i else 'FALLA'}")

    log("(E) regla 14: ENTRADA campo a campo contra corre_bp.tarea(carro, cfg explicito)")
    for b in ('cap', 'aza_largo'):
        carro, cfg = R.TASAS['cap'][b]
        x = N(R.tarea(sd, b, T)); y = N(CBP.tarea(sd, carro, T, cfg=dict(cfg), forzada=None, siembra=None))
        kk = sorted((set(x) | set(y)) - IGN - {'carro'}); e = all(x.get(k) == y.get(k) for k in kk); ok &= e
        log(f"  {b} == corre_bp.tarea('{carro}', CAP): {len(kk)} campos {'OK' if e else 'FALLA'}")
    x = N(R.tarea(sd, 'cap', T)); S = CBP.siembra_de(x); z = N(R.tarea(sd + 3, 'cap', T, S))
    fu = [ff for t in z['bq']['tel'].values() for ff in t['fund']]; i = len(S) > 0 and len(fu) > 0 and all(ff[1] == 1 for ff in fu); ok &= i
    log(f"  la siembra ACTUA en cap: todo fundador sale del banco sembrado ({len(fu)}/{len(fu)}; siembra {len(S)} listas): {'OK' if i else 'FALLA'}")

    log("(D) determinismo: cap, dos veces")
    a1 = N(R.tarea(sd, 'cap', T)); a2 = N(R.tarea(sd, 'cap', T)); a1.pop('seg'); a2.pop('seg'); i = a1 == a2; ok &= i; log(f"  {'OK' if i else 'FALLA'}")

    log("(W) JSON antes de volver; un JSON con aborto SE REINTENTA; uno bueno NO se recorre; cadena completa por trabajo() y --reanuda")
    with tempfile.TemporaryDirectory() as td:
        fin = os.path.join(td, 'x.json'); R._guarda(fin, dict(seed=sd, brazo='cap', aborto='prueba', linajes=[]))
        x1 = R._corrida(fin, sd, 'cap', 500, None, dict(i=0), 'cap'); x2 = R._corrida(fin, sd, 'cap', 500, None, dict(i=0), 'cap')
        i = x1.get('aborto') is None and x1.get('reintento_de') == 'aborto' and x2 == json.load(open(fin, encoding='utf-8')) and x2['seg_trabajo'] == x1['seg_trabajo']
        ok &= i; log(f"  reintento: {'OK' if i else 'FALLA'}")
        R.MODOS['_t'] = dict(ind=[9], npas=2, T_pas=1000, T_pru=1000, base_pas=635000, base_pru=635180, tasas='cap')
        o1 = R.trabajo(('cap', 9, td, '_t'))
        f1 = os.path.join(td, 'pasaje_cap_i9_p1.json'); xx = json.load(open(f1, encoding='utf-8')); xx['aborto'] = 'simulado'; R._guarda(f1, xx)
        o2 = R.trabajo(('cap', 9, td, '_t'))
        c9, ab = R.cadena(td, R.MODOS['_t'], 'cap', 9)
        i = o1['aborto'] is None and o2['aborto'] is None and ab is None and o1['largo_siembra'] == o2['largo_siembra'] == c9['largo_siembra'] \
            and o1['cruzan'] == o2['cruzan'] == c9['cruzan']
        ok &= i; log(f"  trabajo() 2 pasajes + prueba, aborto simulado en p1 y reanuda: identico (largo {o1['largo_siembra']}, cruzan {o1['cruzan']}, "
                     f"largo_med {c9['largo_med']}): {'OK' if i else 'FALLA'}")
        del R.MODOS['_t']

    log("(X) el runner NIEGA pool > 2 y pool en el humo")
    for argv in (['--explora', '--pool', '3'], ['--humo', '--pool', '2']):
        try: R.main(argv); i = False
        except SystemExit as e: i = 'maximo' in str(e) or 'sin Pool' in str(e)
        ok &= i; log(f"  {argv}: {'OK (niega)' if i else 'FALLA'}")

    log("(L) LA LETRA en casos sinteticos")
    ind = [1, 2, 3, 4, 5]
    def cad(cz, lm, l0, db=0.0, r0=0.5, coh=True):
        return dict(cruzan=cz, largo_med=lm, largo_siembra=[l0, lm], R0_med=r0, doble_siembra=[db, db], coherente=coh, mayoria=int(cz >= 5),
                    doble_lin=0, o1_lin=0, lin_con_banco=9)
    def tb(cap, fab, aza, lcap=(6,) * 5, l0cap=6.0, dcap=(0,) * 5, daza=(0,) * 5, coh=True):
        return {'cap': {i: cad(cap[i - 1], lcap[i - 1], l0cap, dcap[i - 1], coh=coh) for i in ind},
                'fab': {i: cad(fab[i - 1], 2.2, 2.0) for i in ind}, 'aza_largo': {i: cad(aza[i - 1], 6.5, 6.0, daza[i - 1]) for i in ind}}
    casos = [('PAGA: gana a fab y a aza en 4/5', tb([5, 5, 5, 5, 1], [2] * 5, [3] * 5), [], 'CAPACIDAD PAGA', False),
             ('PAGA exige las dos (aza 3/5)', tb([5, 5, 5, 5, 1], [2] * 5, [3, 3, 3, 6, 6]), [], 'CAPACIDAD SIN USO', False),
             ('empate no gana', tb([2] * 5, [2] * 5, [1] * 5), [], 'CAPACIDAD SIN USO', False),
             ('PURGADA: largo < 4 en 3/5', tb([2] * 5, [2] * 5, [2] * 5, lcap=(3.9, 3, 2, 6, 6)), [], 'CAPACIDAD PURGADA', False),
             ('largo 4.0 exacto cuenta como >= 4', tb([2] * 5, [2] * 5, [2] * 5, lcap=(4.0, 4.0, 4.0, 4.0, 3)), [], 'CAPACIDAD SIN USO', False),
             ('INDETERMINADO: largo >= 4 en 3/5 y < 4 en 2/5', tb([2] * 5, [2] * 5, [2] * 5, lcap=(3, 3, 5, 5, 5)), [], 'INDETERMINADO', False),
             ('PAGA manda sobre PURGADA', tb([5, 5, 5, 5, 1], [2] * 5, [3] * 5, lcap=(3,) * 5), [], 'CAPACIDAD PAGA', False),
             ('NO SE LEE (aborto)', tb([2] * 5, [2] * 5, [2] * 5), ['x'], 'NO SE LEE', False),
             ('NO SE LEE (tasas no actuan: cap p0 < fab p0 + 1)', tb([2] * 5, [2] * 5, [2] * 5, l0cap=2.5), [], 'NO SE LEE', False),
             ('NO SE LEE (incoherente)', tb([2] * 5, [2] * 5, [2] * 5, coh=False), [], 'NO SE LEE', False),
             ('COMPONE: doble >= 2 p_azar(6) en 3/5 y > aza en 4/5', tb([2] * 5, [2] * 5, [2] * 5, dcap=(.1, .1, .1, .01, .05), daza=(.0, .0, .0, .0, .1)), [],
              'CAPACIDAD SIN USO', True),
             ('no COMPONE si aza igual', tb([2] * 5, [2] * 5, [2] * 5, dcap=(.1,) * 5, daza=(.1,) * 5), [], 'CAPACIDAD SIN USO', False)]
    for txt, C, ab, e, ce in casos:
        L = R.letra(C, ind, ab, True); i = L['veredicto'] == e and L['compone'] == ce; ok &= i
        log(f"  {txt}: {L['veredicto']} · compone {L['compone']} (espera {e} · {ce}) {'OK' if i else 'FALLA'}")
    L = R.letra(tb([2] * 5, [2] * 5, [2] * 5), ind, [], False); i = L['veredicto'] == 'NO SE LEE'; ok &= i
    log(f"  NO SE LEE (arnes): {L['veredicto']} {'OK' if i else 'FALLA'}")
    C = tb([2] * 5, [2] * 5, [2] * 5); del C['aza_largo'][3]; L = R.letra(C, ind, [], True); i = L['veredicto'] == 'NO SE LEE'; ok &= i
    log(f"  NO SE LEE (incompleto): {L['veredicto']} {'OK' if i else 'FALLA'}")
    log(f"ARNES: {'PASA' if ok else 'FALLA'} · {time.time()-t0:.0f}s")
    return 0 if ok else 1


if __name__ == '__main__':
    sys.exit(main())
