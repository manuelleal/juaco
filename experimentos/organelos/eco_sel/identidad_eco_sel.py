"""identidad_eco_sel.py — ARNES de ECO_SEL. Un proceso, sin Pool, sin serie. Semillas de PRACTICA 45391-45394.

MISION: llegar a la AGI por este camino (organismo minimo con reglas locales, sin retropropagacion, peldanos preregistrados con
controles y replicas); el metodo manda sobre el como.

  (K) construye_eco_sel.py --verifica (nucleo == el construido por anclas desde frio/corre_frio.py) y origenes con su sha (verifica()).
  (A) nucleo.trabajo(F1) == corre_frio.trabajo(RES0_FRIO), gemelo, en TODAS las claves de F1 salvo brazo y seg (T 60 000); y
      eco_de == corre_eco.eco_cfg en MUT0 y CEREBRO.
  (B) EL GEN FIJO: con sigma = 0 (el camino de mutacion corre y no mueve nada) SEL_M y AZA_M == F1 bit a bit en todas las claves salvo las
      de configuracion. CONTROLES que pueden fallar, con sigma = 0.15: la fisica de SEL_M difiere de F1; solo se mueve rep_umbral (0 genes
      fuera); en SEL_C los tres genes de historia de vida quedan en G0 y algun gen del cerebro se mueve; AZA_M difiere de SEL_M.
  (C) gemelo == motor Python en trabajo() de los 5 brazos (T 4000) y con p_mut = 1 (SEL_M, AZA_C), en todas las claves salvo seg y motor.
  (D) frio limpio en los 5 brazos; CONTROL: el mismo brazo con vivero (t_corte 1500) SI refunda.
  (H) herencia EXACTA con p_mut = 1 (T 20 000, gemelo): en SEL_M y SEL_C todo hijo == motor_eco.muta(genoma del padre, rng [s, lin, 16, k]);
      en AZA_M y AZA_C casi ninguno de los hijos de padre NO fundador (< 5 %): el control rompe la copia padre -> hijo. (Candidato a ERR,
      antes del humo: la 1a version contaba los hijos de fundadores, clones de G0 como el banco inicial; ver el comentario en el caso.)
  (Q) corte de luz simulado en t = 30 000 + --reanuda == la corrida entera (SEL_M, T 40 000; vid en el checkpoint).
  (F) nube-9: trabajo() atrapa un SystemExit del motor (guardia -> persiste 1; otro -> persiste None); ninguno se propaga.
  (V) la letra en entradas sinteticas (cada rama, cada pregunta).
  (R) banderas malas abortan (ERR-115); subproceso con bandera desconocida: codigo != 0 y no escribe nada.
Escribe identidad_eco_sel_salida.txt.
"""
import contextlib, glob, io, json, os, subprocess, sys, tempfile, time
import numpy as np

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
R_ = []
J = lambda x: json.dumps(x, sort_keys=True, default=str)
PR = (45391, 45392, 45393, 45394)
CONFIG = {'brazo', 'genetica', 'seg', 'mutables', 'p_mut', 'sigma', 'donante', 'genes_vivos_T'}


def chk(nombre, ok, det=''):
    R_.append(bool(ok)); print(f"  {'OK ' if ok else 'MAL'} {nombre} {det}", flush=True)


def main():
    t0 = time.time()
    import corre_eco_sel as C
    N = C.N; CR = C.CR
    print(f"IDENTIDAD ECO_SEL · {time.strftime('%Y-%m-%d %H:%M:%S')} · python {sys.version.split()[0]} · numpy {np.__version__} · shas {C.SHAS()}", flush=True)
    # (K)
    import construye_eco_sel as CE
    chk("(K) nucleo_eco_sel.py en disco == el construido por anclas desde frio/corre_frio.py (3ba8b0f5cf1fbbfa)", CE.main(['--verifica']))
    try: C.verifica(); okv = True
    except SystemExit as e: okv = False; print(e)
    chk("(K) verifica(): origenes con el sha fijado (corre_frio, motor_frio_rapido, corre_eco_v12, corre_eco, motor_eco, FAMB_RES0_ECO)", okv)
    # (A) envoltorio
    sys.path.insert(0, N.FRIO_DIR)
    import corre_frio as F
    import motor_frio_rapido as MF
    chk("(A) un solo corre_eco y un solo gemelo en el proceso (F y N comparten CR y MF)", F.CR is CR and N.CR is CR)
    chk("(A) eco_de == corre_eco.eco_cfg en MUT0 y en CEREBRO (misma expresion; t_corte 1)",
        N.eco_de('MUT0', 1) == CR.eco_cfg('MUT0', 1) and N.eco_de('CEREBRO', 1) == CR.eco_cfg('CEREBRO', 1))
    t1 = time.time(); N.usa_gemelo()
    MF.run_solapadas(PR[0], ['FAMB_RES0_ECO'] * 9, T=200, diag=0, mundo_n=9, tope_cuerpos=3000, muestra=1000, eco=CR.eco_cfg('MUT0', 1))
    print(f"  (compilacion / cache de motor_frio_rapido: {time.time() - t1:.0f} s)", flush=True)
    F.usa_gemelo()
    x = F.trabajo((PR[0], 'RES0_FRIO', 60000, 1, 50000, tempfile.mkdtemp(prefix='esel_A_f1_'), False))
    N.usa_gemelo()
    y = N.trabajo((PR[0], 'F1', 60000, 1, 50000, tempfile.mkdtemp(prefix='esel_A_n_'), False))
    dist = [k for k in x if k not in ('brazo', 'seg') and J(x[k]) != J(y.get(k))]
    falta = [k for k in x if k not in y]
    chk("(A) nucleo.trabajo(F1) == corre_frio.trabajo(RES0_FRIO) en TODAS las claves de F1 salvo brazo y seg (T 60 000, gemelo)",
        not dist and not falta and y['motor'] == 'GEMELO motor_frio_rapido',
        f"(persiste {x['persiste']}, vivos_T {x['vivos_T']}, n_nac {x['n_nac']}, r0_nac {x['r0_nac']}; distintas {dist}, faltan {falta}; "
        f"{x['seg']} s contra {y['seg']} s)")
    chk("(A) claves nuevas de ECO_SEL en F1: sin mutables, 0 mutaciones, 0 genes fuera de G0",
        y['mutables'] == [] and y['n_mut'] == 0 and y['fuera_mutables'] == 0 and y['movidos_mutables'] == 0 and y['p_mut'] == 0.0,
        f"(nac_2a {y['nac_2a']}, vida {y['vida_media_muertos_2a']}, causas {y['causas_2a']}, sel_100k {y['sel_100k']})")
    # (B) el gen fijo
    N._SIGMA[0] = 0.0
    try:
        B0 = {b: N.trabajo((PR[0], b, 60000, 1, 50000, tempfile.mkdtemp(prefix='esel_B0_'), False)) for b in ('SEL_M', 'AZA_M')}
    finally:
        N._SIGMA[0] = None
    for b, z in B0.items():
        dist = [k for k in y if k not in CONFIG and J(y[k]) != J(z.get(k))]
        chk(f"(B) {b} con sigma = 0 (p_mut 0.05: la mutacion corre y no mueve) == F1 bit a bit en todas las claves salvo las de configuracion",
            not dist and z['sigma'] == 0.0 and z['p_mut'] == 0.05 and z['mutables'] == ['rep_umbral'],
            f"(distintas {dist}; donante {z['donante']}; genes vivos T {z['genes_vivos_T']})")
    S = {b: N.trabajo((PR[0], b, 60000, 1, 50000, tempfile.mkdtemp(prefix='esel_B1_'), False)) for b in ('SEL_M', 'AZA_M', 'SEL_C')}
    fis = lambda r: J([r['tam_total'], r['n_nac'], r['vivos_final']])
    chk("(B) CONTROL: con sigma = 0.15 la fisica de SEL_M difiere de la de F1 (el gen actua)", fis(S['SEL_M']) != fis(y),
        f"(n_nac F1 {y['n_nac']} · SEL_M {S['SEL_M']['n_nac']}; n_mut {S['SEL_M']['n_mut']})")
    chk("(B) SEL_M: solo se mueve rep_umbral (0 valores fuera de G0 en genes no mutables; >= 1 cuerpo vivo con rep_umbral movido)",
        S['SEL_M']['fuera_mutables'] == 0 and S['SEL_M']['movidos_mutables'] > 0 and S['SEL_M']['mutables'] == ['rep_umbral'],
        f"(movidos {S['SEL_M']['movidos_mutables']} de {S['SEL_M']['vivos_T']} vivos)")
    ec = list(CR.BRAZOS['CEREBRO']['mutables'])
    chk("(B) SEL_C: mutables = los 15 del cerebro; dote, rep_umbral y rep_X en G0 en todos los vivos; algun gen del cerebro movido",
        S['SEL_C']['mutables'] == ec and len(ec) == 15 and not {'dote', 'rep_umbral', 'rep_X'} & set(ec)
        and S['SEL_C']['fuera_mutables'] == 0 and S['SEL_C']['movidos_mutables'] > 0,
        f"(movidos {S['SEL_C']['movidos_mutables']}, n_mut {S['SEL_C']['n_mut']})")
    chk("(B) CONTROL: AZA_M (el mismo gen sin herencia) difiere de SEL_M en la misma semilla", fis(S['AZA_M']) != fis(S['SEL_M']),
        f"(n_nac AZA_M {S['AZA_M']['n_nac']} · donante {S['AZA_M']['donante']})")
    # (C) gemelo == Python; (D) frio limpio
    RC = {}
    for b in N.BRAZOS:
        CR.ME = N.ME_PY
        p = N.trabajo((PR[1], b, 4000, 1, 3000, tempfile.mkdtemp(prefix='esel_C_py_'), False))
        N.usa_gemelo()
        g = N.trabajo((PR[1], b, 4000, 1, 3000, tempfile.mkdtemp(prefix='esel_C_g_'), False))
        dist = [k for k in p if k not in ('seg', 'motor', 'lim_nac') and J(p[k]) != J(g.get(k))]
        chk(f"(C) {b}: gemelo == motor Python en trabajo() (T 4000, w90)", not dist and p['motor'].startswith('PYTHON') and g['motor'].startswith('GEMELO'),
            f"(n_nac {p['n_nac']}, n_mut {p['n_mut']}, vivos_T {p['vivos_T']}; distintas {dist}; {p['seg']} s contra {g['seg']} s)")
        RC[b] = g
    N._PMUT[0] = 1.0
    try:
        for b in ('SEL_M', 'AZA_C'):
            CR.ME = N.ME_PY
            p = N.trabajo((PR[1], b, 4000, 1, 3000, tempfile.mkdtemp(prefix='esel_C2_py_'), False))
            N.usa_gemelo()
            g = N.trabajo((PR[1], b, 4000, 1, 3000, tempfile.mkdtemp(prefix='esel_C2_g_'), False))
            dist = [k for k in p if k not in ('seg', 'motor', 'lim_nac') and J(p[k]) != J(g.get(k))]
            chk(f"(C) {b} con p_mut = 1 (toda cria muta): gemelo == motor Python (T 4000)", not dist and p['n_mut'] > 0,
                f"(n_nac {p['n_nac']}, n_mut {p['n_mut']}; distintas {dist})")
    finally:
        N._PMUT[0] = None
    for b in N.BRAZOS:
        g = RC[b]
        chk(f"(D) {b}: 0 refundados y 0 fundadores repuestos", g['n_refund'] == 0 and g['fundadores_rep'] == 0 and g['t_fund_primero'] is None,
            f"(vivos cada 1000 {g['vivos_1k']})")
    N.usa_gemelo()
    gv = N.trabajo((PR[1], 'SEL_M', 4000, 1500, 3000, tempfile.mkdtemp(prefix='esel_D_'), False))
    chk("(D) CONTROL que puede fallar: SEL_M con vivero (t_corte 1500) SI refunda", gv['n_refund'] > 0 and gv['fundadores_rep'] > 0,
        f"(refundados {gv['n_refund']}, fundadores_rep {gv['fundadores_rep']})")
    # (H) herencia exacta con p_mut = 1
    import pista2 as P
    ME = N.ME_PY
    N._PMUT[0] = 1.0
    try:
        for gen in ('MARGEN', 'CEREBRO', 'MARGEN_AZAR', 'CEREBRO_AZAR'):
            filas = []
            eco = N.eco_de(gen, 1, ind_cb=lambda li, row, g: filas.append((li, list(row), np.array(g, float))))
            E_ = ME._eco_cfg(dict(eco), P.cfg_fabrica(), 90)
            MF.run_solapadas(PR[2], ['FAMB_RES0_ECO'] * 90, T=20000, diag=0, mundo_n=90, tope_cuerpos=3000, muestra=1000, eco=eco)
            gen_de = {(li, row[0]): g for li, row, g in filas}
            fund_de = {(li, row[0]): row[6] for li, row, g in filas}
            hijos = [(li, row, g) for li, row, g in filas if not row[6]]
            # ERR candidato (arnes, 28-sep, antes del humo): la 1a version contaba tambien a los hijos de FUNDADORES. Los 90 fundadores son
            # clones de G0 y el banco arranca con ellos: en AZA una entrada al azar coincide con el genoma del padre por identidad de clones,
            # no por herencia (dio 13 % y 8 %). Se mide la herencia en los hijos de padres NO fundadores (con p_mut = 1 su genoma es unico).
            cu = {True: [0, 0], False: [0, 0]}   # padre fundador? -> [iguales, total]
            for li, row, g in hijos:
                gp = gen_de.get((li, row[2]))
                if gp is None: continue
                esp, _ = ME.muta(gp, np.random.default_rng([PR[2], li, ME.ETQ_MUT, row[0]]), E_['pv'], float(E_['sigma']), E_['lo'], E_['hi'])
                pf = bool(fund_de[(li, row[2])]); cu[pf][0] += int(np.array_equal(esp, g)); cu[pf][1] += 1
            iguales, con_padre = cu[False]; fr = iguales / max(1, con_padre)
            det = f"(padre no fundador: {iguales}/{con_padre} = {fr:.3f}; padre fundador: {cu[True][0]}/{cu[True][1]})"
            if gen.endswith('AZAR'):
                chk(f"(H) {gen}: el control rompe la copia padre -> hijo (hijos de padre no fundador == muta(padre) < 5 %)", con_padre >= 50 and fr < 0.05, det)
            else:
                chk(f"(H) {gen}: TODO hijo == muta(genoma del padre, rng [s, lin, 16, k]) (herencia exacta)",
                    con_padre >= 50 and iguales == con_padre and cu[True][0] == cu[True][1], det)
    finally:
        N._PMUT[0] = None
    # (Q) corte de luz + reanuda
    N.usa_gemelo()
    bq = 'SEL_M'
    for sq in PR:
        entera = N.trabajo((sq, bq, 40000, 1, 35000, tempfile.mkdtemp(prefix='esel_Q_a_'), False))
        if entera['t_ext'] is None or entera['t_ext'] > 30000: break
    tq = tempfile.mkdtemp(prefix='esel_Q_b_')
    orig_q = CR.ME.run_solapadas

    def corta(*a, _o=orig_q, **k):
        fn = k['eco']['ckpt_fn']

        def fn2(t, blob):
            fn(t, blob)
            if t == 30000: raise KeyboardInterrupt('corte de luz simulado en t = 30000')
        k['eco'] = dict(k['eco'], ckpt_fn=fn2)
        return _o(*a, **k)
    CR.ME.run_solapadas = corta
    try:
        N.trabajo((sq, bq, 40000, 1, 35000, tq, False)); cortado = False
    except KeyboardInterrupt:
        cortado = True
    finally:
        CR.ME.run_solapadas = orig_q
    hay_ck = os.path.exists(os.path.join(tq, 'ckpt', f'{bq}_s{sq}.pkl')) and not os.path.exists(os.path.join(tq, f'{bq}_s{sq}.json'))
    re = N.trabajo((sq, bq, 40000, 1, 35000, tq, True))
    dist = [k for k in entera if k not in ('seg',) and J(entera[k]) != J(re.get(k))]
    chk(f"(Q) {bq}: corte en t = 30 000 + --reanuda == la corrida entera (T 40 000; vid de la 2a mitad incluida)", cortado and hay_ck and not dist,
        f"(semilla {sq}, cortado {cortado}, checkpoint {hay_ck}, distintas {dist}, nac_2a {entera['nac_2a']}, n_mut {entera['n_mut']})")
    # (F) nube-9
    orig = CR.ME.run_solapadas
    try:
        tmp = tempfile.mkdtemp(prefix='esel_F_')

        def guardia(*a, **k): raise SystemExit('PISTA2: mas de 100000 cuerpos en un linaje: la semilla colisionaria (ERR-60)')

        def otro(*a, **k): raise SystemExit('motor: otra cosa')
        CR.ME.run_solapadas = guardia
        try: r1 = N.trabajo((PR[0], 'SEL_M', 3000, 1, 2500, tmp, False)); ok1 = True
        except BaseException: r1 = {}; ok1 = False
        CR.ME.run_solapadas = otro
        try: r2 = N.trabajo((PR[0], 'AZA_C', 3000, 1, 2500, tmp, False)); ok2 = True
        except BaseException: r2 = {}; ok2 = False
    finally:
        CR.ME.run_solapadas = orig
    chk("(F) la guardia ERR-60 no se propaga: persiste 1, guardia 1, JSON escrito",
        ok1 and r1.get('persiste') == 1 and r1.get('guardia') == 1 and os.path.exists(os.path.join(tmp, f'SEL_M_s{PR[0]}.json')))
    chk("(F) otro aborto no se propaga: persiste None, marcado", ok2 and r2.get('persiste') is None and r2.get('aborto'))
    chk("(F) LIM_NAC del gemelo = 1e9 (ERR-146)", MF.LIM_NAC == 1_000_000_000)
    # (V) la letra
    NOM = list(ME.NOMBRES); G0 = [0.0] * len(NOM)
    SOMB = [[0.1 * (q + 1)] * len(NOM) for q in range(8)]
    VAL = {1: 0.05, 5: 0.45, 9: 0.85}
    T = N.FRIO['T']

    def fake(K=None, rk=None, pers=None, T_=T, quita=0, sucio=None, bloq=0, aborto=None, fuera=None, tc=None, semilla_mala=False, nomut=None,
             guardia_ab=None):
        K = dict({'F1': 31.0, 'SEL_M': 36.0, 'AZA_M': 30.0, 'SEL_C': 36.0, 'AZA_C': 20.0}, **(K or {}))
        rk = dict({'SEL_M': {'rep_umbral': 1}, 'SEL_C': {'alpha': 9}}, **(rk or {}))
        pers = dict({b: 20 for b in N.BRAZOS}, **(pers or {}))
        R = []
        for i in range(20):
            for b, (gen, carro, tcb) in N.BRAZOS.items():
                k = K[b][i] if isinstance(K[b], list) else K[b]
                br = [VAL[5]] * len(NOM)
                for g, r in rk.get(b, {}).items(): br[NOM.index(g)] = VAL[r]
                fila = [N.T_SEL, 30, 1, 40, G0, [G0] * 8, br, SOMB]
                mut = (list(N.GENETICAS[gen]['mutables'] or []) if N.GENETICAS[gen]['p'] else [])
                pr = int(i < pers[b])
                x = dict(seed=45301 + i + (1 if (semilla_mala and b == 'AZA_C' and i == 0) else 0), brazo=b, T=T_,
                         t_corte=(tc if (tc is not None and b == 'SEL_M') else tcb), persiste=pr,
                         tam_total=[int(round(k))] * (T_ // 1000 + 1), bloqueados=(bloq if (i == 0 and b == 'F1') else 0),
                         n_refund=0, fundadores_rep=0, aborto=None, guardia=0, genes=NOM, gen_t=[fila], mutables=mut,
                         fuera_mutables=0, tasa_mut=(0.0 if not mut else 0.01), genes_vivos_T=None, causas_2a=[1, 1, 1, 1])
                if b in ('SEL_M', 'SEL_C', 'AZA_M', 'AZA_C') and nomut == b: x['tasa_mut'] = 0.0
                if sucio and b == sucio and i == 3: x['n_refund'] = 1
                if aborto and b == aborto and i == 2: x.update(aborto='SystemExit: otra cosa', persiste=None)
                if guardia_ab and b == guardia_ab and i == 2: x.update(aborto=r1.get('aborto'), guardia=1, persiste=1)
                if fuera and b == fuera and i == 5: x['fuera_mutables'] = 2
                R.append(x)
        return R[:len(R) - quita]
    casos = [
        ("FUNCIONA en M y en C", fake(), {'M': 'FUNCIONA', 'C': 'FUNCIONA'}),
        ("M: MODESTO sin firma (P1 cae: rango 5); C FUNCIONA", fake(rk={'SEL_M': {'rep_umbral': 5}}), {'M': 'HAY ALGO MODESTO: LA HERENCIA', 'C': 'FUNCIONA'}),
        ("C: MODESTO sin superar a F1 (P2 cae: SEL_C = F1)", fake(K={'SEL_C': 31.0}), {'M': 'FUNCIONA', 'C': 'HAY ALGO MODESTO: LA SELECCION'}),
        ("C: P2 cae por la mediana (+1.0 < +1.5 aunque 20/20 > F1)", fake(K={'SEL_C': 32.0}), {'C': 'HAY ALGO MODESTO: LA SELECCION'}),
        ("M: P2 sin P3 (AZA_M sostiene lo mismo) = NO", fake(K={'AZA_M': 36.0}), {'M': 'NO (en', 'C': 'FUNCIONA'}),
        ("M: P2 cae en el pareado (14/20 > F1) aunque la mediana sea +5", fake(K={'SEL_M': [36.0] * 14 + [30.0] * 6, 'AZA_M': 25.0}), {'M': 'HAY ALGO MODESTO: LA SELECCION'}),
        ("M: empate SEL_M = AZA_M no cuenta como ganar (P3 cae) y P1 cae = NO", fake(K={'AZA_M': 36.0}, rk={'SEL_M': {'rep_umbral': 5}}), {'M': 'NO (en'}),
        ("M: solo P1 (sin P2 ni P3) = NO", fake(K={'SEL_M': 31.0, 'AZA_M': 31.0}), {'M': 'NO (en'}),
        ("guardia: AZA_M sale de sus sombras -> M NO EVALUABLE; C sigue", fake(rk={'AZA_M': {'rep_umbral': 9}}), {'M': 'NO EVALUABLE (el control', 'C': 'FUNCIONA'}),
        ("guardia C: AZA_C con tau_e bajo todas las sombras -> C NO EVALUABLE", fake(rk={'AZA_C': {'tau_e': 1}}), {'C': 'NO EVALUABLE (el control', 'M': 'FUNCIONA'}),
        ("V3: SEL_C con genes fuera de los mutables -> C NO EVALUABLE", fake(fuera='SEL_C'), {'C': 'NO EVALUABLE (la genetica', 'M': 'FUNCIONA'}),
        ("V3: AZA_M sin mutacion en 20/20 -> M NO EVALUABLE", fake(nomut='AZA_M'), {'M': 'NO EVALUABLE (la genetica', 'C': 'FUNCIONA'}),
        ("V1: F1 16/20 -> las dos NO EVALUABLE", fake(pers={'F1': 16}), {'M': 'NO EVALUABLE (el ancla', 'C': 'NO EVALUABLE (el ancla'}),
        ("V2: un refundado en AZA_C -> las dos NO EVALUABLE", fake(sucio='AZA_C'), {'M': 'NO EVALUABLE (un brazo', 'C': 'NO EVALUABLE (un brazo'}),
        ("bloqueados -> NO EVALUABLE", fake(bloq=3), {'M': 'NO EVALUABLE (tope', 'C': 'NO EVALUABLE (tope'}),
        ("T distinto -> NO EVALUABLE", fake(T_=200000), {'M': 'NO EVALUABLE (serie', 'C': 'NO EVALUABLE (serie'}),
        ("serie incompleta -> NO EVALUABLE", fake(quita=1), {'M': 'NO EVALUABLE (serie'}),
        ("un aborto -> NO EVALUABLE", fake(aborto='SEL_C'), {'M': 'NO EVALUABLE (serie', 'C': 'NO EVALUABLE (serie'}),
        ("t_corte distinto de 1 -> NO EVALUABLE", fake(tc=60000), {'M': 'NO EVALUABLE (serie'}),
        ("la guardia ERR-60 (imposible a 1e9) tambien cuenta como aborto -> NO EVALUABLE", fake(guardia_ab='SEL_M'), {'M': 'NO EVALUABLE (serie'}),
        ("semillas distintas entre brazos -> NO EVALUABLE", fake(semilla_mala=True), {'C': 'NO EVALUABLE (serie'}),
    ]
    for nombre, R, esp in casos:
        v, L, d = C.veredicto(R, 20)
        ok = all(v[q].startswith(e) for q, e in esp.items())
        chk(f"(V) {nombre}", ok, f"-> M: {v['M'][:70]} | C: {v['C'][:70]}")
    chk("(V) rango: real bajo las 8 sombras = 1, sobre = 9, en medio = 5, empate total = 5, sin fila = 5",
        C.rango(dict(genes=NOM, gen_t=[[N.T_SEL, 0, 0, 0, None, None, [0.05] * 18, SOMB]]), 'alpha') == 1.0
        and C.rango(dict(genes=NOM, gen_t=[[N.T_SEL, 0, 0, 0, None, None, [0.85] * 18, SOMB]]), 'alpha') == 9.0
        and C.rango(dict(genes=NOM, gen_t=[[N.T_SEL, 0, 0, 0, None, None, [0.45] * 18, SOMB]]), 'alpha') == 5.0
        and C.rango(dict(genes=NOM, gen_t=[[N.T_SEL, 0, 0, 0, None, None, [0.0] * 18, [[0.0] * 18] * 8]]), 'alpha') == 5.0
        and C.rango(dict(genes=NOM, gen_t=[]), 'alpha') == 5.0)
    chk("(V) K: media de [T/2, T] con la extincion en 0 (tam_total corto)",
        abs(C.kbar(dict(tam_total=[10] * 1001), 1_000_000) - 10) < 1e-12 and abs(C.kbar(dict(tam_total=[10] * 751), 1_000_000) - 10 * 251 / 501) < 1e-12)
    # (R) banderas
    malas = [['--help'], ['-h'], [], ['--serie'], ['--humo', '--serie'], ['--serie', '--desde', '45301', '--n', '20'],
             ['--serie', '--desde=45301', '--n', '20', '--pool', '6'], ['--serie', '--des', '45301', '--n', '20', '--pool', '6'],
             ['--serie', '--desde', '45302', '--n', '20', '--pool', '6'], ['--serie', '--desde', '45301', '--n', '19', '--pool', '6'],
             ['--serie', '--desde', '45301', '--n', '20', '--pool', '7'], ['--humo', '--pool', '2'], ['--humo', '--humo'],
             ['--lee', 'x', '--pool', '2'], ['--gemelo', '--humo'], ['--serie', '--desde', '35001', '--n', '20', '--pool', '6']]
    n_ab = 0
    for m in malas:
        try: C.parsea(m)
        except C.BanderaMala: n_ab += 1
    chk(f"(R) el parser aborta ante {len(malas)} formas de bandera mala", n_ab == len(malas), f"({n_ab}/{len(malas)})")
    buenas = [['--humo'], ['--serie', '--desde', '45301', '--n', '20', '--pool', '6'], ['--serie', '--desde', '45321', '--n', '20', '--pool', '6', '--reanuda'],
              ['--lee', 'datos/x']]
    n_ok = 0
    for m in buenas:
        try: C.parsea(m); n_ok += 1
        except C.BanderaMala: pass
    chk(f"(R) el parser acepta las {len(buenas)} formas buenas", n_ok == len(buenas), f"({n_ok}/{len(buenas)})")
    antes = set(glob.glob(os.path.join(AQUI, 'datos', '**', '*'), recursive=True))
    pr = subprocess.run([sys.executable, os.path.join(AQUI, 'corre_eco_sel.py'), '--serie', '--desde', '45301', '--n', '20', '--pool', '6', '--nada'],
                        capture_output=True, text=True, timeout=300)
    despues = set(glob.glob(os.path.join(AQUI, 'datos', '**', '*'), recursive=True))
    chk("(R) subproceso con bandera desconocida: codigo != 0 y no escribe nada", pr.returncode != 0 and antes == despues, f"(codigo {pr.returncode})")
    n = sum(R_)
    print(f"RESULTADO: {n}/{len(R_)}  ({time.time() - t0:.0f} s)")
    return n == len(R_)


if __name__ == '__main__':
    buf = io.StringIO()

    class Tee:
        def write(self, x): sys.__stdout__.write(x); buf.write(x)
        def flush(self): sys.__stdout__.flush()
        def reconfigure(self, **kw): pass
    with contextlib.redirect_stdout(Tee()):
        ok = main()
    open(os.path.join(AQUI, 'identidad_eco_sel_salida.txt'), 'w', encoding='utf-8').write(buf.getvalue())
    sys.exit(0 if ok else 1)
