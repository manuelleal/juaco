"""identidad_mut.py — ARNES de CONDICIONES / MUTACION (30-sep-2026, creador). Escribe su salida ENTERA en identidad_mut_salida.txt (la cita el
runner: sin 'ARNES: PASA' con los shas actuales, --explora no corre).

MISION: llegar a la AGI por este camino. Un proceso, sin Pool. Corridas cortas (T 2 000, s 634192) + DOS de T 25 000 (s 633110: el pasaje p0
de la cadena moneda i1 GUARDADO el 29-sep; a tasas de fabrica debe salir BIT A BIT, a tasas / 10 debe diferir).

  python experimentos/organelos/condiciones/mutacion/identidad_mut.py
"""
import copy, json, os, sys, tempfile, time
import numpy as np

AQUI = os.path.dirname(os.path.abspath(__file__))
if AQUI not in sys.path: sys.path.insert(0, AQUI)
import corre_mut as R   # noqa: E402
M = R.M; SM = R.SM; CBP = R.CBP; CV = SM.CV
N = lambda x: json.loads(json.dumps(x, default=str))
SALIDA = os.path.join(AQUI, 'identidad_mut_salida.txt')
IGN = {'seg', 'seg_trabajo'}
KS_RUN = ['linajes', 'pista', 'R0_pista', 'tel', 'tel_termo', 'bq']


def muta_tasas(cfg, n, seed):
    """El operador del carro (_bq_muta) llamado n veces sobre [A] con cfg: fraccion de hijos distintos del padre y delta de largo medio."""
    mod = CV._MODS['V143_BQ3']; Car = mod.Carro; viejo = mod.BQ_C; mod.BQ_C = dict(cfg)

    class F: pass
    f = F(); f._bqrng = np.random.default_rng(seed); f._bq_azar = lambda: Car._bq_azar(f)
    base = [list(R.A)]; cam = 0; dl = 0
    try:
        for _ in range(n):
            h = Car._bq_muta(f, base); cam += int(h != base); dl += len(h) - 1
    finally:
        mod.BQ_C = viejo
    return cam / n, dl / n


def main():
    LOGF = open(SALIDA, 'w', encoding='utf-8')
    def log(s=''): print(s, flush=True); LOGF.write(s + '\n'); LOGF.flush()
    t0 = time.time(); ok = True
    log(f"ARNES mutacion · {time.strftime('%Y-%m-%d %H:%M:%S')}")
    log(f"  shas: corre_mut.py {R.h16(os.path.join(AQUI, 'corre_mut.py'))} · identidad_mut.py {R.h16(os.path.abspath(__file__))}")
    SM.registra()
    log("(K) shas fijados (corre_moneda, identidad_moneda; por corre_moneda.verifica: sentidos_muro, corre_bp, V143_BQ3, pista, juez)")
    ok &= R.verifica(log)
    sd = R.SEM_ARNES; T = 2000

    log("(C) CONFIGURACION: CFG10 = CFG de fabrica con TODAS las tasas / 10; inicial y banco iguales; CERO == corre_moneda; 'fabrica' == corre_moneda.BRAZOS")
    c = R.CFG == M.CFG == SM.CFG == CV._MODS['V143_BQ3'].BQ_C
    for k in ('p_campo', 'p_dup', 'p_del', 'p_ins'): c &= abs(R.CFG10[k] - R.CFG[k] / 10) < 1e-15
    c &= R.CFG10['inicial'] == R.CFG['inicial'] and R.CFG10['banco'] == R.CFG['banco'] and set(R.CFG10) == set(R.CFG) and R.CERO == M.CERO
    c &= R.TASAS['fabrica'] == {b: tuple(v) for b, v in M.BRAZOS.items()}
    c &= all(R.TASAS['div10'][b][0] == M.BRAZOS[b][0] and R.TASAS['div10'][b][2] == M.BRAZOS[b][2] for b in M.BRAZOS)
    c &= R.TASAS['div10']['moneda'][1] == R.TASAS['div10']['neutra'][1] == R.CFG10 and R.TASAS['div10']['cero'][1] == R.CERO
    ok &= c; log(f"  CFG {R.CFG} · CFG10 {R.CFG10} · CERO {R.CERO}: {'OK' if c else 'FALLA'}")

    log("(I) siembra inyectada == la de corre_moneda en los tres brazos (y en las dos tasas)")
    for b in ('moneda', 'neutra', 'cero'):
        i = R.siembra0(b) == R.siembra0(b, 'fabrica') == M.siembra0(b) and R.intacta(R.siembra0(b), b) == 1.0; ok &= i
        log(f"  {b}: {'OK' if i else 'FALLA'}")

    log("(F) A TASAS DE FABRICA ESTE RUNNER ES corre_moneda BIT A BIT")
    for b in ('moneda', 'neutra', 'cero'):
        S = R.siembra0(b); x = N(R.tarea(sd, b, T, S, 'fabrica')); y = N(M.tarea(sd, b, T, S))
        ks = sorted((set(x) | set(y)) - IGN); e = all(x.get(k) == y.get(k) for k in ks); ok &= e
        log(f"  tarea {b}: {len(ks)} campos {'OK' if e else 'FALLA ' + str([k for k in ks if x.get(k) != y.get(k)][:5])}")
    with tempfile.TemporaryDirectory() as td:
        d1 = os.path.join(td, 'r'); d2 = os.path.join(td, 'm'); os.makedirs(d1); os.makedirs(d2)
        R.MODOS['_tf'] = dict(ind=[9], npas=2, T_pas=1000, T_pru=1000, base_pas=634100, base_pru=634190, brazos=('moneda', 'neutra'), tasas='fabrica')
        M.MODOS['_tf'] = dict(ind=[9], npas=2, T_pas=1000, T_pru=1000, base_pas=634100, base_pru=634190, brazos=('moneda', 'neutra'))
        for b in ('moneda', 'neutra'):
            o1 = R.trabajo((b, 9, d1, '_tf')); o2 = M.trabajo((b, 9, d2, '_tf'))
            fs = sorted(f for f in os.listdir(d2) if f.startswith(f'pasaje_{b}') or f.startswith(f'{b}_s'))
            iguales = fs == sorted(f for f in os.listdir(d1) if f.startswith(f'pasaje_{b}') or f.startswith(f'{b}_s'))
            for f in fs:
                a_ = json.load(open(os.path.join(d1, f), encoding='utf-8')); b_ = json.load(open(os.path.join(d2, f), encoding='utf-8'))
                iguales &= all(a_.get(k) == b_.get(k) for k in (set(a_) | set(b_)) - IGN)
            i = iguales and o1['frac_A'] == o2['frac_A'] and o1.get('cruzan') == o2.get('cruzan') and o1['aborto'] is None
            ok &= i; log(f"  trabajo {b} (cadena 2 pasajes{' + prueba' if b == 'moneda' else ''}, T 1000): {len(fs)} JSON campo a campo y frac_A "
                         f"{o1['frac_A']}: {'OK' if i else 'FALLA'}")
        del R.MODOS['_tf']; del M.MODOS['_tf']
    f, sh = R.REF_P0; s = R.h16(f); i = s == sh; ok &= i; log(f"  sha del pasaje guardado {os.path.basename(f)} {s}: {'OK' if i else 'FALLA'}")
    ref = json.load(open(f, encoding='utf-8'))
    t1 = time.time(); x = N(R.tarea(ref['seed'], 'moneda', ref['T'], M.siembra0('moneda'), 'fabrica'))
    i = all(x.get(k) == ref.get(k) for k in KS_RUN); ok &= i
    log(f"  moneda i1 p0 (s {ref['seed']}, T {ref['T']}, {time.time()-t1:.0f}s) a tasas de fabrica == GUARDADO 29-sep en {KS_RUN}: "
        f"{'OK' if i else 'FALLA ' + str([k for k in KS_RUN if x.get(k) != ref.get(k)])}")

    log("(A) LAS TASAS NUEVAS ACTUAN")
    t1 = time.time(); z = N(R.tarea(ref['seed'], 'moneda', ref['T'], M.siembra0('moneda'), 'div10'))
    d = z['bq']['cfg'] == R.CFG10 and any(z.get(k) != ref.get(k) for k in KS_RUN); ok &= d
    Sz = CBP.siembra_de(z); Sr = CBP.siembra_de(ref)
    log(f"  el mismo pasaje a tasas / 10 ({time.time()-t1:.0f}s): cfg del carro == CFG10 y difiere del guardado: {'OK' if d else 'FALLA'} · "
        f"intacta {R.intacta(Sz, 'moneda')} (fabrica {R.intacta(Sr, 'moneda')}) · fraccion A {M.frac(Sz)} (fabrica {M.frac(Sr)})")
    n = 100000
    c1, dl1 = muta_tasas(R.CFG, n, sd); c10, dl10 = muta_tasas(R.CFG10, n, sd + 1); c0, dl0 = muta_tasas(R.CERO, 2000, sd + 2)
    rat = c10 / c1; i = 0.07 <= rat <= 0.13 and c0 == 0.0; ok &= i
    log(f"  operador _bq_muta del carro, {n} hijos de [A]: cambia {c1:.4f} (fabrica) vs {c10:.4f} (/10), razon {rat:.3f} en [0.07, 0.13]; "
        f"tasas 0: {c0}: {'OK' if i else 'FALLA'} · delta largo medio {dl1:+.4f} (fabrica) {dl10:+.4f} (/10)")

    log("(E) regla 14: ENTRADA campo a campo contra corre_bp.tarea (la de corre_moneda) con cfg explicito")
    for b, cfg in (('moneda', R.CFG10), ('neutra', R.CFG10), ('cero', R.CERO)):
        S = R.siembra0(b); x = N(R.tarea(sd, b, T, S)); y = N(CBP.tarea(sd, 'V143_BQ3', T, cfg=dict(cfg), forzada=None, siembra=S))
        ks = sorted((set(x) | set(y)) - IGN - {'brazo', 'carro'}); e = all(x.get(k) == y.get(k) for k in ks) and x['bq']['cfg'] == cfg; ok &= e
        log(f"  {b} (/10) == corre_bp.tarea('V143_BQ3', {'CFG10' if cfg is R.CFG10 else 'CERO'}, siembra): {len(ks)} campos {'OK' if e else 'FALLA'}")
    x = N(R.tarea(sd, 'cero', T, R.siembra0('cero'))); y = N(M.tarea(sd, 'cero', T, M.siembra0('cero')))
    ks = sorted((set(x) | set(y)) - IGN); e = all(x.get(k) == y.get(k) for k in ks); ok &= e
    log(f"  cero == corre_moneda.tarea('cero') (tasas 0 en los dos): {'OK' if e else 'FALLA'}")
    fu = [f_ for t in x['bq']['tel'].values() for f_ in t['fund']]
    i = len(fu) > 0 and all(f_[1] == 1 for f_ in fu); ok &= i
    log(f"  la siembra ACTUA: todo fundador sale del banco sembrado ({len(fu)}/{len(fu)}): {'OK' if i else 'FALLA'}")

    log("(D) determinismo: moneda / 10, dos veces")
    a1 = N(R.tarea(sd, 'moneda', T, R.siembra0('moneda'))); a2 = N(R.tarea(sd, 'moneda', T, R.siembra0('moneda')))
    a1.pop('seg'); a2.pop('seg'); i = a1 == a2; ok &= i; log(f"  {'OK' if i else 'FALLA'}")

    log("(W) JSON antes de volver; un JSON con aborto SE REINTENTA; uno bueno NO se recorre; cadena completa por trabajo() y --reanuda")
    with tempfile.TemporaryDirectory() as td:
        fin = os.path.join(td, 'x.json'); M._guarda(fin, dict(seed=sd, brazo='cero', aborto='prueba', linajes=[]))
        S = R.siembra0('cero')
        x1 = R._corrida(fin, sd, 'cero', 500, S, dict(i=0), 'div10'); x2 = R._corrida(fin, sd, 'cero', 500, S, dict(i=0), 'div10')
        i = x1.get('aborto') is None and x1.get('reintento_de') == 'aborto' and x2 == json.load(open(fin, encoding='utf-8')) and x2['seg_trabajo'] == x1['seg_trabajo']
        ok &= i; log(f"  reintento: {'OK' if i else 'FALLA'}")
        R.MODOS['_t'] = dict(ind=[9], npas=2, T_pas=500, T_pru=500, base_pas=634100, base_pru=634190, brazos=('moneda',), tasas='div10')
        o1 = R.trabajo(('moneda', 9, td, '_t'))
        f1 = os.path.join(td, 'pasaje_moneda_i9_p1.json'); xx = json.load(open(f1, encoding='utf-8')); xx['aborto'] = 'simulado'; M._guarda(f1, xx)
        o2 = R.trabajo(('moneda', 9, td, '_t'))
        c9, _ = R.cadena(td, R.MODOS['_t'], 'moneda', 9)
        i = o1['aborto'] is None and o2['aborto'] is None and o1['frac_A'] == o2['frac_A'] == [c9['f_ini']] + c9['f'] and o1['cruzan'] == o2['cruzan']
        ok &= i; log(f"  trabajo() cadena 2 pasajes + prueba, aborto simulado en p1 y reanuda: identico ({o1['frac_A']}, cruzan {o1['cruzan']}; "
                     f"intacta {c9['intacta']}): {'OK' if i else 'FALLA'}")
        del R.MODOS['_t']

    log("(X) el runner NIEGA pool > 2 y pool en el humo")
    for argv in (['--explora', '--pool', '3'], ['--humo', '--pool', '2']):
        try: R.main(argv); i = False
        except SystemExit as e: i = 'maximo' in str(e) or 'sin Pool' in str(e)
        ok &= i; log(f"  {argv}: {'OK (niega)' if i else 'FALLA'}")

    log("(L) LA LETRA en casos sinteticos")
    ind = [1, 2, 3, 4, 5]
    def cad(f, fi=0.5, sol=True, it=0.95, mu=3): return dict(f_ini=fi, f=[0.4, f], solo_inyectadas=sol, intacta=[1.0, it], listas_mutadas_total=mu)
    def tb(mo, ne, ce=(0.5,) * 5, it=0.95, mu=3, **kw):
        return {'moneda': {i: cad(mo[i - 1], mu=mu) for i in ind}, 'neutra': {i: cad(ne[i - 1], it=it, mu=mu) for i in ind},
                'cero': {i: cad(ce[i - 1], mu=0, **kw) for i in ind}}
    casos = [('PAGA: moneda > neutra en 4/5', tb([.5, .45, .4, .3, .1], [.3, .3, .3, .2, .2]), [], 'PAGA'),
             ('PAGA exige estricto: empates no cuentan (2/5)', tb([.5, .45, .3, .3, .1], [.3, .3, .3, .3, .2]), [], 'OTRA MONEDA'),
             ('OTRA MONEDA: 3/5 mayor', tb([.5, .45, .4, .1, .1], [.3, .3, .3, .2, .2]), [], 'OTRA MONEDA'),
             ('PURGA: <= 0.5 neutra en 4/5 y neutra >= 0.10', tb([.1, .1, .05, .0, .4], [.3, .2, .3, .3, .3]), [], 'PURGA'),
             ('PURGA: == 0.5 neutra cuenta', tb([.15, .1, .15, .1, .4], [.3, .2, .3, .2, .3]), [], 'PURGA'),
             ('no PURGA si la neutra mediana < 0.10', tb([.0, .0, .0, .0, .4], [.05, .08, .09, .12, .3]), [], 'OTRA MONEDA'),
             ('NO SE LEE (aborto)', tb([.5] * 5, [.3] * 5), ['x'], 'NO SE LEE'),
             ('NO SE LEE (cero fuera de banda)', tb([.5] * 5, [.3] * 5, ce=(.1, .2, .1, .3, .2)), [], 'NO SE LEE'),
             ('cero en el borde 0.25 se lee', tb([.5] * 5, [.3] * 5, ce=(.25,) * 5), [], 'PAGA'),
             ('NO SE LEE (cero con genotipo nuevo)', tb([.5] * 5, [.3] * 5, sol=False), [], 'NO SE LEE'),
             ('NO SE LEE (carga no bajo: intacta neutra < 0.80)', tb([.5] * 5, [.3] * 5, it=0.6), [], 'NO SE LEE'),
             ('NO SE LEE (tasas no actuan: 0 listas mutadas)', tb([.5] * 5, [.3] * 5, mu=0), [], 'NO SE LEE')]
    for txt, C, ab, e in casos:
        L = R.letra(C, ind, ab, True, True, n_pru=5); i = L['veredicto'] == e; ok &= i
        log(f"  {txt}: {L['veredicto']} (espera {e}) {'OK' if i else 'FALLA'}")
    L = R.letra(tb([.5] * 5, [.3] * 5), ind, [], True, False, n_pru=5); i = L['veredicto'] == 'NO SE LEE'; ok &= i
    log(f"  NO SE LEE (arnes): {L['veredicto']} {'OK' if i else 'FALLA'}")
    L = R.letra(tb([.5] * 5, [.3] * 5), ind, [], False, True, n_pru=5); i = L['veredicto'] == 'NO SE LEE'; ok &= i
    log(f"  NO SE LEE (referencias): {L['veredicto']} {'OK' if i else 'FALLA'}")

    log("(R) referencias GUARDADAS: forzada3 y bq3_pas (sentidos_muro), prueba de moneda a tasas x1 y la lectura de moneda (sha16)")
    for b, shas in list(M.REFS.items()) + [('moneda_x1', R.REF_MX1)]:
        d = R.MEXP if b == 'moneda_x1' else M.SMEXP; nb = 'moneda' if b == 'moneda_x1' else b
        for i_, sh in zip(ind, shas):
            f = os.path.join(d, f"{nb}_s{59200 + i_}.json"); s = R.h16(f); ok &= s == sh
            log(f"  {b} s{59200 + i_} {s} {'OK' if s == sh else '!= ' + sh + ' FALLA'}")
    s = R.h16(R.REF_LECT[0]); ok &= s == R.REF_LECT[1]; log(f"  lectura_moneda.json {s} {'OK' if s == R.REF_LECT[1] else 'FALLA'}")
    log(f"ARNES: {'PASA' if ok else 'FALLA'} · {time.time()-t0:.0f}s")
    return 0 if ok else 1


if __name__ == '__main__':
    sys.exit(main())
