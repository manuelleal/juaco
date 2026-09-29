"""identidad_bloques.py — arnes de identidad de BLOQUES (Opus M, 28-sep-2026). Un proceso; T corto; semillas 48491-48494.
Salida: identidad_bloques_salida.txt. Mision: llegar a la AGI por este camino.

(K) motor_bloques.py == construccion por anclas desde frio/motor_frio_rapido.py (sha fijado).
(A) BQ APAGADO: motor_bloques == motor_frio_rapido en TODAS las claves de nucleo_eco_sel_ing.trabajo (ING_F1, ING_SEL_C, ING_AZA_C).
(B) BQ PRENDIDO con genoma vacio y tasas 0 ("genoma vacio = el bicho de fabrica"): BLOQ y BLOQ_AZA == ING_F1, BLOQ_C == ING_SEL_C
    de motor_frio_rapido, en todas las claves salvo 'brazo' y 'seg' (las llamadas objmode nuevas no tocan el azar del mundo).
(C) CONTROLES QUE DEBEN FALLAR: con las tasas de la serie BLOQ != ING_F1; con una regla forzada ("pixel 4 del foco > 0.5 -> boca -3":
    no morder B ni D) != ING_F1, y la regla ACTUA: menos muertes por veneno+sal que ING_F1.
(H) HERENCIA: fundadores con 1 regla al azar y tasas 0: en BLOQ todo hijo == padre (igual_padre == hijos); en BLOQ_AZA no (< 50 %).
(D) DETERMINISMO: BLOQ con las tasas de la serie dos veces == (claves y reglas de los vivos en T).
(Q) E5: corte de luz en t = 30 000 + --reanuda == la corrida entera (BLOQ con reglas vivas, T 40 000): claves, reglas de los vivos,
    banco de reglas y contadores de operadores.
(L) la LETRA de la serie (corre_bloques.veredicto) en entradas sinteticas.   (R) banderas de --serie.
"""
import json, os, subprocess, sys, time
AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
import corre_bloques as CB   # noqa: E402
NS = CB.NS
T = 20000
CAR = os.path.join(AQUI, 'datos', 'arnes')
LOG = []


def p(*a):
    s = ' '.join(str(x) for x in a); print(s, flush=True); LOG.append(s)


def ok(nombre, cond, info=''):
    p(f"  [{'OK ' if cond else 'MAL'}] {nombre} {info}")
    return bool(cond)


def run_frio(seed, brazo):
    NS.usa_gemelo()
    return NS.trabajo((seed, brazo, T, NS.tc_de(brazo, T), NS.FRIO['T_lect'], os.path.join(CAR, 'frio'), False))


def run_bq(seed, brazo, extra=None):
    MB = CB.usa_bloques()
    MB.BQ_CFG.clear(); MB.BQ_CFG.update(CB.DEF); MB.BQ_CFG.update(CB.BQ[brazo]); MB.BQ_CFG.update(extra or {})
    r = NS.trabajo((seed, brazo, T, NS.tc_de(brazo, T), NS.FRIO['T_lect'], os.path.join(CAR, 'bq'), False))
    return r, json.loads(json.dumps(MB.BQ_OUT, default=float))


def difs(a, b, fuera=('seg', 'brazo')):
    ks = sorted(set(a) | set(b))
    return [k for k in ks if k not in fuera and json.dumps(a.get(k), sort_keys=True) != json.dumps(b.get(k), sort_keys=True)]


def main():
    t0 = time.time(); n_ok = 0; n = 0
    p('identidad_bloques.py', time.strftime('%Y-%m-%d %H:%M:%S'), f'T {T}')
    p('(K) construccion por anclas')
    out = subprocess.run([sys.executable, os.path.join(AQUI, 'construye_bloques.py'), '--verifica'], capture_output=True, text=True).stdout.strip()
    n += 1; n_ok += ok('construye --verifica', out.startswith('IGUAL'), out)
    try:
        CB.verifica(); n += 1; n_ok += ok('shas fijados (nucleo, motor_frio_rapido, motor_bloques)', True)
    except SystemExit as e:
        n += 1; n_ok += ok('shas fijados', False, str(e))
    F = {}
    p('(A) BQ apagado == motor_frio_rapido')
    for b in ('ING_F1', 'ING_SEL_C', 'ING_AZA_C'):
        F[b] = run_frio(48491, b)
        r, _ = run_bq(48491, b)
        d = difs(F[b], r, fuera=('seg',))
        n += 1; n_ok += ok(f'{b} s48491', not d and F[b]['aborto'] is None, f'claves distintas {d} · K_nac {r.get("K_nac")} fund_2a {r.get("fund_2a")} n_nac {r.get("n_nac")}')
    p('(B) BQ prendido, genoma vacio, tasas 0 == fabrica')
    cero = dict(p_campo=0, p_dup=0, p_ins=0, p_hgt=0, p_del=0)
    for b, ref in (('BLOQ', 'ING_F1'), ('BLOQ_AZA', 'ING_F1'), ('BLOQ_C', 'ING_SEL_C')):
        r, B = run_bq(48491, b, cero)
        d = difs(F[ref], r)
        n += 1; n_ok += ok(f'{b} == {ref}', not d, f'distintas {d} · hijos {B["n_hijos"]} fund {B["n_fund"]} (las llamadas nuevas SI ocurrieron: {B["n_hijos"] + B["n_fund"] > 0})')
        n += 1; n_ok += ok(f'{b}: hubo llamadas objmode de reglas', B['n_hijos'] + B['n_fund'] > 0)
    p('(C) controles que deben fallar')
    r, B = run_bq(48491, 'BLOQ')
    d = difs(F['ING_F1'], r)
    n += 1; n_ok += ok('BLOQ con tasas de la serie != ING_F1', bool(d), f'ins {B["n_ins"]} · {len(d)} claves distintas')
    forz = [[3, 4, 1, 0.5, 0, -3.0]]
    r2, B2 = run_bq(48491, 'BLOQ', dict(cero, forzada=forz))
    d = difs(F['ING_F1'], r2)
    n += 1; n_ok += ok('regla forzada != ING_F1', bool(d))
    vs = lambda x: (x['causas_2a'][2] + x['causas_2a'][3]) / max(1, sum(x['causas_2a']))
    n += 1; n_ok += ok('la regla forzada ACTUA (fraccion veneno+sal de muertes 2a mitad baja)', vs(r2) < vs(F['ING_F1']),
                       f"forzada {vs(r2):.3f} vs ING_F1 {vs(F['ING_F1']):.3f} · causas {r2['causas_2a']} vs {F['ING_F1']['causas_2a']} · K_nac {r2['K_nac']} vs {F['ING_F1']['K_nac']}")
    p('(H) herencia')
    r, B = run_bq(48492, 'BLOQ', dict(cero, inicial=1))
    n += 1; n_ok += ok('BLOQ: todo hijo == padre', B['n_hijos'] > 0 and B['n_igual_padre'] == B['n_hijos'] and B['n_hijos_pl'] > 0,
                       f"{B['n_igual_padre']}/{B['n_hijos']} (padre con reglas: {B['n_igual_pl']}/{B['n_hijos_pl']})")
    r, B = run_bq(48492, 'BLOQ_AZA', dict(cero, inicial=1))
    n += 1; n_ok += ok('BLOQ_AZA: el hijo de padre CON reglas NO copia al padre (< 50 %)', B['n_hijos_pl'] > 0 and B['n_igual_pl'] < 0.5 * B['n_hijos_pl'],
                       f"{B['n_igual_pl']}/{B['n_hijos_pl']} (todos: {B['n_igual_padre']}/{B['n_hijos']})")
    p('(D) determinismo')
    ra, Ba = run_bq(48493, 'BLOQ'); rb, Bb = run_bq(48493, 'BLOQ')
    n += 1; n_ok += ok('BLOQ dos veces ==', not difs(ra, rb) and json.dumps(Ba.get('vivos_T')) == json.dumps(Bb.get('vivos_T')),
                       f"largo medio vivos T {sum(len(x[3]) for x in Ba['vivos_T']) / max(1, len(Ba['vivos_T'])):.2f}")
    p('(Q) corte de luz + reanuda (E5)')
    TQ = 40000; sq = 48494
    MB = CB.usa_bloques(); MB.BQ_CFG.clear(); MB.BQ_CFG.update(CB.DEF); MB.BQ_CFG.update(CB.BQ['BLOQ'])
    ent = NS.trabajo((sq, 'BLOQ', TQ, TQ, NS.FRIO['T_lect'], os.path.join(CAR, 'Q_a'), False))
    Bent = json.loads(json.dumps(MB.BQ_OUT, default=float))
    MB = CB.usa_bloques(); MB.BQ_CFG.clear(); MB.BQ_CFG.update(CB.DEF); MB.BQ_CFG.update(CB.BQ['BLOQ'])
    orig = NS.CR.ME.run_solapadas
    def corta(*a, _o=orig, **k):
        fn = k['eco']['ckpt_fn']
        def fn2(tt, blob):
            fn(tt, blob)
            if tt == 30000: raise KeyboardInterrupt('corte de luz simulado en t = 30000')
        k['eco'] = dict(k['eco'], ckpt_fn=fn2)
        return _o(*a, **k)
    NS.CR.ME.run_solapadas = corta
    cq = os.path.join(CAR, 'Q_b')
    import shutil; shutil.rmtree(cq, ignore_errors=True)
    try:
        NS.trabajo((sq, 'BLOQ', TQ, TQ, NS.FRIO['T_lect'], cq, False)); cortado = False
    except KeyboardInterrupt:
        cortado = True
    MB = CB.usa_bloques(); MB.BQ_CFG.clear(); MB.BQ_CFG.update(CB.DEF); MB.BQ_CFG.update(CB.BQ['BLOQ'])
    rea = NS.trabajo((sq, 'BLOQ', TQ, TQ, NS.FRIO['T_lect'], cq, True))
    Brea = json.loads(json.dumps(MB.BQ_OUT, default=float))
    dq = difs(ent, rea)
    n += 1; n_ok += ok('corte en 30 000 y reanuda == entera (claves)', cortado and not dq, f'cortado {cortado} · distintas {dq}')
    n += 1; n_ok += ok('reglas de los vivos, banco de reglas, contadores y serie ==', json.dumps(Bent, sort_keys=True) == json.dumps(Brea, sort_keys=True),
                       f"hijos {Bent['n_hijos']}/{Brea['n_hijos']} · banco {len(Bent.get('banco_T', []))}/{len(Brea.get('banco_T', []))} · "
                       f"largo medio vivos T {sum(len(x[3]) for x in Bent['vivos_T']) / max(1, len(Bent['vivos_T'])):.2f}")
    p('(L) la letra en entradas sinteticas')
    def rec(b, s, K, pers, fr=None, **kw):
        on, don = CB.CFG_ESPERADA[b]
        d = dict(seed=s, brazo=b, T=CB.T_SERIE, t_corte=CB.T_CORTE, aborto=None, bloqueados=0, carro=CB.FAB, persiste=pers, K=K,
                 frac_rechazo=fr, bloques=(dict(cfg=dict(on=1, donante=don)) if on else None))
        d.update(kw); return d
    def mundo(kb=37, ks=10, ka=2, pa=0, pf=0, fr=1.0, nsem=20, kmod=None):
        D = {b: {} for b in CB.SERIE_BR}
        for i in range(nsem):
            s = 48411 + i
            D['BLOQ_V'][s] = rec('BLOQ_V', s, kb + 0.01 * i, 1, fr)
            D['ING_SEL_C_V'][s] = rec('ING_SEL_C_V', s, ks, 1)
            D['BLOQ_AZA_V'][s] = rec('BLOQ_AZA_V', s, ka, int(i < pa))
            D['ING_F1_V'][s] = rec('ING_F1_V', s, 1.3, int(i < pf))
        if kmod: kmod(D)
        return D
    casos = [('todo pasa', mundo(), 'FUNCIONA'),
             ('P2 mediana +5 (P1+P3)', mundo(ks=32), 'MODESTO'),
             ('sin firma P4 (P1+P2+P3)', mundo(fr=0.2), 'MODESTO'),
             ('control AZA iguala (P3 cae)', mundo(ka=37.5), 'NO'),
             ('AZA persiste 6/20 (P3 cae)', mundo(pa=6), 'NO'),
             ('base F1 persiste 4/20 (V1)', mundo(pf=4), 'NO EVALUABLE'),
             ('19 semillas (V0)', mundo(nsem=19), 'NO EVALUABLE'),
             ('un aborto (V0)', mundo(kmod=lambda D: D['BLOQ_V'][48415].update(aborto='x')), 'NO EVALUABLE'),
             ('donante mal declarado (V2)', mundo(kmod=lambda D: D['BLOQ_AZA_V'][48415]['bloques']['cfg'].update(donante='padre')), 'NO EVALUABLE'),
             ('t_corte distinto (V0)', mundo(kmod=lambda D: D['ING_F1_V'][48411].update(t_corte=60000)), 'NO EVALUABLE'),
             ('BLOQ_V persiste 16/20 (P2+P3+P4 sin P1)', mundo(kmod=lambda D: [D['BLOQ_V'][48411 + i].update(persiste=0) for i in range(4)]), 'MODESTO'),
             ('P1 y P2 caen, P3 pasa', mundo(ks=32, kmod=lambda D: [D['BLOQ_V'][48411 + i].update(persiste=0) for i in range(4)]), 'NO'),
             ('P1 cae y P4 cae con P2+P3', mundo(fr=0.1, kmod=lambda D: [D['BLOQ_V'][48411 + i].update(persiste=0) for i in range(4)]), 'MODESTO')]
    for nom, D, esp in casos:
        v, _ = CB.veredicto(D, CB.T_SERIE)
        n += 1; n_ok += ok(f'letra: {nom}', v == esp, f'-> {v} (esperado {esp})')
    p('(R) banderas')
    for args, esp in ((['--serie', '--desde', '48411', '--n', '20', '--T', '400000', '--pool', '6'], '--serie exige'),
                      (['--serie', '--desde', '48401', '--n', '20', '--T', str(CB.T_SERIE), '--pool', '6'], '--serie exige'),
                      (['--serie', '--desde', '48411', '--n', '10', '--T', str(CB.T_SERIE), '--pool', '6'], '--serie exige'),
                      (['--seri'], 'banderas desconocidas'), (['--explora', '--semillas', '48411', '--brazos', 'BLOQ_V', '--T', '100'], 'fuera de las declaradas')):
        r = subprocess.run([sys.executable, os.path.join(AQUI, 'corre_bloques.py')] + args, capture_output=True, text=True)
        n += 1; n_ok += ok(f'banderas {" ".join(args)}', r.returncode != 0 and esp in (r.stdout + r.stderr), (r.stdout + r.stderr).strip().splitlines()[-1][:90])
    p(f'RESULTADO {n_ok}/{n} en {time.time() - t0:.0f} s')
    open(os.path.join(AQUI, 'identidad_bloques_salida.txt'), 'w', encoding='utf-8').write('\n'.join(LOG) + '\n')


if __name__ == '__main__':
    main()
