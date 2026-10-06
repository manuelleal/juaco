"""identidad_moneda.py — ARNES de LA MONEDA (29-sep-2026, creador). Escribe su salida ENTERA en identidad_moneda_salida.txt (la cita el
runner: sin 'ARNES: PASA' con los shas actuales, --explora no corre).

MISION: llegar a la AGI por este camino. Un proceso, sin Pool. Corridas cortas (T 2 000, s 633192) + UNA de T 100 000 (s 59201: la
reproduccion bit a bit de forzada3 guardada en sentidos_muro).

  python experimentos/organelos/moneda/identidad_moneda.py
"""
import copy, json, os, sys, tempfile, time

AQUI = os.path.dirname(os.path.abspath(__file__))
if AQUI not in sys.path: sys.path.insert(0, AQUI)
import corre_moneda as R   # noqa: E402
SM = R.SM; CBP = R.CBP; CV = SM.CV; P = SM.P
N = lambda x: json.loads(json.dumps(x, default=str))
SALIDA = os.path.join(AQUI, 'identidad_moneda_salida.txt')
IGN = {'seg', 'brazo', 'carro', 'aborto'}


def main():
    LOGF = open(SALIDA, 'w', encoding='utf-8')
    def log(s=''): print(s, flush=True); LOGF.write(s + '\n'); LOGF.flush()
    t0 = time.time(); ok = True
    log(f"ARNES moneda · {time.strftime('%Y-%m-%d %H:%M:%S')}")
    log(f"  shas: corre_moneda.py {R.h16(os.path.join(AQUI, 'corre_moneda.py'))} · identidad_moneda.py {R.h16(os.path.abspath(__file__))}")
    SM.registra()
    log("(K) shas fijados (sentidos_muro, corre_bp, carro V143_BQ3 == construye_sm, pista, juez)")
    ok &= R.verifica(log)
    c = R.CFG == SM.CFG == CBP.CFG0 == CV._MODS['V143_BQ3'].BQ_C and R.CERO == SM.CERO; ok &= c
    log(f"  CFG {R.CFG} == sentidos_muro == corre_bp.CFG0 == carro; CERO == sentidos_muro: {'OK' if c else 'FALLA'}")
    sd = R.SEM_ARNES; T = 2000

    log("(I) SIEMBRA INYECTADA == DECLARADA")
    i = R.A == SM.FORZADA3[0]; ok &= i; log(f"  fila A == la de forzada3 {SM.FORZADA3[0]}: {'OK' if i else 'FALLA'}")
    for b, marca in (('moneda', R.A), ('neutra', R.A0), ('cero', R.A0)):
        S = R.siembra0(b); na = sum(1 for L in S if L == [marca]); nb = sum(1 for L in S if L == [R.B])
        i = len(S) == R.NSIE and na == nb == R.NSIE // 2 and R.frac(S) == 0.5 and R.frac(S, R.es_A_neg) == (0.5 if b == 'moneda' else 0.0)
        ok &= i; log(f"  {b}: {len(S)} listas · marcada {marca} x{na} · B {R.B} x{nb} · fraccion A {R.frac(S)} · A con w<0 {R.frac(S, R.es_A_neg)}: "
                     f"{'OK' if i else 'FALLA'}")
    S = R.siembra0('moneda'); m = CBP.prepara('V143_BQ3', sd, dict(R.CFG), None, S)
    bk = [L for v in m._BQ_BANCO.values() for L in v]
    i = len(m._BQ_BANCO) == 9 and all(len(v) == 50 for v in m._BQ_BANCO.values()) and all(L in S for L in bk)
    ok &= i; log(f"  corre_bp.prepara: 9 bancos de 50, toda lista en la siembra declarada (fraccion A en los bancos {R.frac(bk)}): {'OK' if i else 'FALLA'}")

    log("(N) la etiqueta es MUDA y la neutra es NULA: con tasas 0 y regla forzada, [B] == [A0] == genoma vacio == V143_TERMO (salida ENTERA de pista.run)")
    def run(forz, cfg=R.CERO, siembra=None, seed=sd):
        CBP.prepara('V143_BQ3', seed, dict(cfg), copy.deepcopy(forz), siembra)
        return N(P.run(seed, [('C', CV._MODS['V143_BQ3'])] * 9, T=T, fundador_limpio=1))
    rb = run([list(R.B)]); ra0 = run([list(R.A0)]); rv = run(None)
    te = N(P.run(sd, [('C', CV._MODS['V143_TERMO'])] * 9, T=T, fundador_limpio=1))
    for txt, x in (('[B]', rb), ('[A0]', ra0), ('vacio', rv)):
        i = x == te; ok &= i; log(f"  {txt} == V143_TERMO: {'OK' if i else 'FALLA'}")
    ra = run([list(R.A)]); d = ra != te; ok &= d
    log(f"  control que DEBE diferir: [A] (forzada3) != V143_TERMO: {'OK (difiere)' if d else 'FALLA (igual)'}")

    log("(Z) VALIDEZ tasas 0: la fraccion solo se mueve por deriva (etiqueta invisible; no nace ningun genotipo)")
    xz = N(R.tarea(sd, 'cero', T, R.siembra0('cero')))
    Sb = [[list(R.B)] for _ in range(R.NSIE)]
    xb = N(CBP.tarea(sd, 'V143_BQ3', T, cfg=dict(R.CERO), forzada=None, siembra=Sb))
    ks = ['linajes', 'pista', 'R0_pista', 'tel_termo']
    i = all(xz.get(k) == xb.get(k) for k in ks); ok &= i
    log(f"  cero (50 % A0 / 50 % B) == todo B, en {ks}: {'OK' if i else 'FALLA ' + str([k for k in ks if xz.get(k) != xb.get(k)])}")
    sz = CBP.siembra_de(xz); g0 = {json.dumps(L) for L in R.siembra0('cero')}
    i = all(json.dumps(L) in g0 for L in sz); ok &= i
    log(f"  siembra de salida ({len(sz)} listas) solo con genotipos inyectados: {'OK' if i else 'FALLA'} · fraccion A {R.frac(sz)} (deriva, T {T})")
    xm = N(CBP.tarea(sd, 'V143_BQ3', T, cfg=dict(R.CERO), siembra=R.siembra0('moneda')))
    sm = CBP.siembra_de(xm); gm = {json.dumps(L) for L in R.siembra0('moneda')}
    i = all(json.dumps(L) in gm for L in sm); ok &= i
    log(f"  moneda con tasas 0: siembra de salida solo con A y B: {'OK' if i else 'FALLA'} · fraccion A {R.frac(sm)} (descriptivo)")

    log("(V) por que NO listas vacias: una lista vacia no entra al banco (corre_bp.siembra_de y _bq_banco la descartan)")
    Sv = [[] if k % 2 else [list(R.B)] for k in range(R.NSIE)]
    xv = N(CBP.tarea(sd, 'V143_BQ3', T, cfg=dict(R.CFG), siembra=Sv)); sv = CBP.siembra_de(xv)
    i = all(len(L) > 0 for L in sv); ok &= i
    log(f"  siembra 50 % [] / 50 % [B] -> salida {len(sv)} listas, vacias {sum(1 for L in sv if not L)} (la mitad vacia se pierde por construccion): "
        f"{'OK' if i else 'FALLA'}")

    log("(E) regla 14: ENTRADA campo a campo contra el tronco de la medida")
    S = R.siembra0('moneda')
    x = N(R.tarea(sd, 'moneda', T, S)); y = N(SM.tarea(sd, 'bq3', T, S)); z = N(CBP.tarea(sd, 'V143_BQ3', T, cfg=dict(SM.CFG), siembra=S))
    ks = sorted((set(x) | set(y)) - IGN); e = all(x.get(k) == y.get(k) == z.get(k) for k in ks); ok &= e
    log(f"  moneda == sentidos_muro.tarea('bq3', siembra) == corre_bp.tarea('V143_BQ3', CFG, siembra): {len(ks)} campos "
        f"{'OK' if e else 'FALLA ' + str([k for k in ks if not x.get(k) == y.get(k) == z.get(k)][:5])}")
    S = R.siembra0('neutra')
    x = N(R.tarea(sd, 'neutra', T, S)); y = N(SM.tarea(sd, 'bq3', T, S))
    ks = sorted((set(x) | set(y)) - IGN); e = all(x.get(k) == y.get(k) for k in ks); ok &= e
    log(f"  neutra == sentidos_muro.tarea('bq3', siembra): {len(ks)} campos {'OK' if e else 'FALLA'}")
    x = N(R.tarea(sd, 'cero', T, S)); y = N(CBP.tarea(sd, 'V143_BQ3', T, cfg=dict(SM.CERO), siembra=S))
    ks = sorted((set(x) | set(y)) - IGN); e = all(x.get(k) == y.get(k) for k in ks); ok &= e
    log(f"  cero == corre_bp.tarea('V143_BQ3', CERO, siembra): {len(ks)} campos {'OK' if e else 'FALLA'}")
    fu = [f for t in x['bq']['tel'].values() for f in t['fund']]
    i = len(fu) > 0 and all(f[1] == 1 for f in fu); ok &= i
    log(f"  la siembra ACTUA: todo fundador sale del banco sembrado ({len(fu)}/{len(fu)}): {'OK' if i else 'FALLA'}")

    log("(D) determinismo: moneda, dos veces")
    a1 = N(R.tarea(sd, 'moneda', T, R.siembra0('moneda'))); a2 = N(R.tarea(sd, 'moneda', T, R.siembra0('moneda')))
    a1.pop('seg'); a2.pop('seg'); i = a1 == a2; ok &= i; log(f"  {'OK' if i else 'FALLA'}")

    log("(W) JSON antes de volver; un JSON con aborto SE REINTENTA; uno bueno NO se recorre; cadena completa por trabajo() y --reanuda")
    with tempfile.TemporaryDirectory() as td:
        fin = os.path.join(td, 'x.json'); R._guarda(fin, dict(seed=sd, brazo='cero', aborto='prueba', linajes=[]))
        S = R.siembra0('cero')
        x1 = R._corrida(fin, sd, 'cero', 500, S, dict(i=0)); x2 = R._corrida(fin, sd, 'cero', 500, S, dict(i=0))
        i = x1.get('aborto') is None and x1.get('reintento_de') == 'aborto' and x2 == json.load(open(fin, encoding='utf-8')) and x2['seg_trabajo'] == x1['seg_trabajo']
        ok &= i; log(f"  reintento: {'OK' if i else 'FALLA'}")
        R.MODOS['_t'] = dict(ind=[9], npas=2, T_pas=500, T_pru=500, base_pas=633100, base_pru=633190, brazos=('moneda',))
        o1 = R.trabajo(('moneda', 9, td, '_t'))
        f1 = os.path.join(td, 'pasaje_moneda_i9_p1.json'); xx = json.load(open(f1, encoding='utf-8')); xx['aborto'] = 'simulado'; R._guarda(f1, xx)
        o2 = R.trabajo(('moneda', 9, td, '_t'))
        c9, _ = R.cadena(td, R.MODOS['_t'], 'moneda', 9)
        i = o1['aborto'] is None and o2['aborto'] is None and o1['frac_A'] == o2['frac_A'] == [c9['f_ini']] + c9['f'] and o1['cruzan'] == o2['cruzan']
        ok &= i; log(f"  trabajo() cadena 2 pasajes + prueba, aborto simulado en p1 y reanuda: identico ({o1['frac_A']}, cruzan {o1['cruzan']}): "
                     f"{'OK' if i else 'FALLA'}")
        del R.MODOS['_t']

    log("(X) el runner NIEGA pool > 2 y pool en el humo")
    for argv in (['--explora', '--pool', '3'], ['--humo', '--pool', '2']):
        try: R.main(argv); i = False
        except SystemExit as e: i = 'maximo' in str(e) or 'sin Pool' in str(e)
        ok &= i; log(f"  {argv}: {'OK (niega)' if i else 'FALLA'}")

    log("(L) LA LETRA en casos sinteticos (con H-1 de la auditoria)")
    ind = [1, 2, 3, 4, 5]
    def cad(f, fi=0.5, sol=True): return dict(f_ini=fi, f=[0.4, f], solo_inyectadas=sol)
    def tb(mo, ne, ce=(0.5,) * 5, **kw): return {'moneda': {i: cad(mo[i - 1]) for i in ind}, 'neutra': {i: cad(ne[i - 1]) for i in ind},
                                                 'cero': {i: cad(ce[i - 1], **kw) for i in ind}}
    casos = [('PURGA', tb([.02, .05, .0, .08, .3], [.2, .1, .1, .2, .2]), [], 'PURGA'),
             ('no PURGA si la neutra cae igual (3/5 mas rapida)', tb([.02, .05, .0, .08, .09], [.2, .01, .1, .01, .2]), [], 'INDETERMINADO'),
             ('empate no es mas rapido', tb([.05] * 5, [.05, .05, .2, .2, .2]), [], 'INDETERMINADO'),
             ('H-1a: neutra < 0.10 (mediana) -> INDETERMINADO aunque moneda caiga', tb([.01, .0, .02, .01, .0], [.05, .08, .09, .12, .3]), [], 'INDETERMINADO'),
             ('H-1a: neutra mediana == 0.10 basta', tb([.01, .0, .02, .01, .0], [.05, .1, .1, .12, .3]), [], 'PURGA'),
             ('H-1b: menor pero > 0.5 neutra en 2/5 -> INDETERMINADO', tb([.05, .06, .02, .09, .08], [.2, .2, .2, .12, .12]), [], 'INDETERMINADO'),
             ('H-1b: == 0.5 neutra cuenta (<=)', tb([.05, .05, .05, .05, .3], [.1, .1, .1, .1, .2]), [], 'PURGA'),
             ('CONSERVA', tb([.45, .5, .4, .1, .05], [.2] * 5), [], 'CONSERVA'),
             ('INDETERMINADO', tb([.2] * 5, [.3] * 5), [], 'INDETERMINADO'),
             ('NO SE LEE (aborto)', tb([.02] * 5, [.2] * 5), ['x'], 'NO SE LEE'),
             ('NO SE LEE (cero fuera de banda)', tb([.02] * 5, [.2] * 5, ce=(.1, .2, .1, .3, .2)), [], 'NO SE LEE'),
             ('NO SE LEE (cero con genotipo nuevo)', tb([.02] * 5, [.2] * 5, sol=False), [], 'NO SE LEE')]
    for txt, C, ab, e in casos:
        L = R.letra(C, ind, ab, True, True, n_pru=5); i = L['veredicto'] == e; ok &= i
        log(f"  {txt}: {L['veredicto']} (espera {e}) {'OK' if i else 'FALLA'}")
    L = R.letra(tb([.02] * 5, [.2] * 5), ind, [], True, False, n_pru=5); i = L['veredicto'] == 'NO SE LEE'; ok &= i
    log(f"  NO SE LEE (arnes): {L['veredicto']} {'OK' if i else 'FALLA'}")

    log("(R) referencias GUARDADAS (sentidos_muro explora): sha16 de 10 JSON y reproduccion BIT A BIT de forzada3 s59201 T 100 000")
    for b, shas in R.REFS.items():
        for i_, sh in zip(ind, shas):
            f = os.path.join(R.SMEXP, f"{b}_s{59200 + i_}.json"); s = R.h16(f); ok &= s == sh
            log(f"  {b} s{59200 + i_} {s} {'OK' if s == sh else '!= ' + sh + ' FALLA'}")
    t1 = time.time(); x = N(SM.tarea(59201, 'forzada3', 100000))
    ref = json.load(open(os.path.join(R.SMEXP, 'forzada3_s59201.json'), encoding='utf-8'))
    ks = [k for k in ('linajes', 'pista', 'R0_pista', 'tel', 'tel_termo', 'bq') if k in ref]
    i = all(x.get(k) == ref.get(k) for k in ks); ok &= i
    log(f"  forzada3 s59201 T 100k ({time.time()-t1:.0f}s) == guardado en {ks}: {'OK' if i else 'FALLA ' + str([k for k in ks if x.get(k) != ref.get(k)])}")
    log(f"ARNES: {'PASA' if ok else 'FALLA'} · {time.time()-t0:.0f}s")
    return 0 if ok else 1


if __name__ == '__main__':
    sys.exit(main())
