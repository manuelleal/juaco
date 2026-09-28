"""identidad_eco_sel_largo.py — ARNES de ECO_SEL LARGO. Un proceso, sin Pool, sin serie. Semillas de PRACTICA 45492-45496.

MISION: llegar a la AGI por este camino (organismo minimo con reglas locales, sin retropropagacion, peldanos preregistrados con
controles y replicas); el metodo manda sobre el como.

  (K) construye_eco_sel_largo --verifica (nucleo == el construido por anclas desde eco_sel/nucleo_eco_sel.py 6a36e47ce61db3e1) y
      verifica() del runner (todo lo que corre con su sha fijado).
  (A) A T = 1e6 (gemelo): nucleo_largo.trabajo(F1) == nucleo_eco_sel.trabajo(F1) y lo mismo con SEL_C, en TODAS las claves de eco_sel salvo
      seg; la unica clave nueva es 'ventanas'. K de eco_sel (kbar) == kvent(x, T/2, T). Mide el checkpoint (bytes y segundos) a lo largo
      de 1e6 para extrapolar a 1e7. eco_de('MC') = los 16 genes en el orden de NOMBRES, p 0.05 y sigma 0.15 por gen como eco_sel.
  (B) p_mut = 0: SEL_MC y AZA_MC == F1 bit a bit (salvo configuracion; genes de 'ventanas' = G0). (B') sigma = 0: SEL_MC deja los 14
      genes reales en G0 y solo mueve los 2 enteros (regla de paso entero de motor_eco.muta; ver el ERR candidato en el caso). CONTROLES
      que pueden fallar con sigma 0.15: la fisica de SEL_MC difiere de F1; AZA_MC difiere de SEL_MC.
  (M) SEL_MC muta EXACTAMENTE los 16 genes declarados (p_mut 1, T 20 000): todo gen que difiere padre -> hijo esta en los 16, los 16 se
      mueven alguna vez, dote y rep_X nunca; en T 60 000 con p 0.05: 0 valores fuera de G0 en genes no mutables.
  (H) herencia EXACTA con p_mut = 1 (T 20 000): en SEL_MC todo hijo == motor_eco.muta(genoma del padre, rng [s, lin, 16, k]); en AZA_MC
      casi ninguno de los hijos de padre NO fundador (< 5 %; caso H de ERR-149: los hijos de fundadores no cuentan).
  (C) gemelo == motor Python en trabajo() de SEL_MC y AZA_MC (T 4000; y con p_mut 1), todas las claves salvo seg/motor/lim_nac.
  (D) frio limpio en SEL_MC y AZA_MC; CONTROL: con vivero (t_corte 1500) SI refunda.
  (T) telemetria por ventana (T 60 000, T_lect = T para tener todas las filas de gen_t): vivos en el borde W == gen_t[W][1] ==
      tam_total[W/1000]; media_log == gen_t[W][4] (tolerancia 1e-5: orden de suma); sum(nac) == n_nac; sum(muertes) == n_nac + 90 - vivos_T;
      los cuantiles son los de np.quantile de los vivos (recalculados desde vivos_final en W = T).
  (P) la dinamica no depende de T: tam_total de T 120 000 empieza con el de T 60 000 (la ventana base de 1e7 es la K de eco_sel a 1e6).
  (Q) corte de luz en t = 100 000 + --reanuda == la corrida entera (SEL_MC, T 200 000; tel en el checkpoint).
  (Z) determinismo: la misma corrida dos veces == bit a bit.
  (F) nube-9: la guardia y otro aborto no se propagan.
  (V) la letra en entradas sinteticas (cada rama de L y de MC, validez, bloqueados).
  (R) banderas malas abortan (ERR-115); subproceso con bandera desconocida: codigo != 0 y no escribe nada.
Escribe identidad_eco_sel_largo_salida.txt.
"""
import contextlib, glob, io, json, os, resource, subprocess, sys, tempfile, time
import numpy as np

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
R_ = []
J = lambda x: json.dumps(x, sort_keys=True, default=str)
PR = (45492, 45493, 45494, 45495, 45496)
CONFIG = {'brazo', 'genetica', 'seg', 'mutables', 'p_mut', 'sigma', 'donante', 'genes_vivos_T', 'ventanas'}


def chk(nombre, ok, det=''):
    R_.append(bool(ok)); print(f"  {'OK ' if ok else 'MAL'} {nombre} {det}", flush=True)


def main():
    t0 = time.time()
    import corre_eco_sel_largo as C
    N = C.N; CR = C.CR
    print(f"IDENTIDAD ECO_SEL LARGO · {time.strftime('%Y-%m-%d %H:%M:%S')} · python {sys.version.split()[0]} · numpy {np.__version__} · "
          f"CPU COMPARTIDA con otra serie Pool 3 (tiempos contaminados) · shas {C.SHAS()}", flush=True)
    # (K)
    import construye_eco_sel_largo as CL
    chk("(K) nucleo_eco_sel_largo.py en disco == el construido por anclas desde eco_sel/nucleo_eco_sel.py (6a36e47ce61db3e1)", CL.main(['--verifica']))
    try: C.verifica(); okv = True
    except SystemExit as e: okv = False; print(e)
    chk("(K) verifica(): nucleo, eco_sel y origenes con el sha fijado; eco_sel/nucleo == su construido", okv)
    sys.path.insert(0, C.ECO_SEL_DIR)
    import nucleo_eco_sel as NE
    import corre_eco_sel as CE
    import motor_frio_rapido as MF
    ME = N.ME_PY
    chk("(A) un solo corre_eco en el proceso (eco_sel y largo comparten CR)", NE.CR is CR and CE.CR is CR)
    mc = [g for g in ME.NOMBRES if g not in ('dote', 'rep_X')]
    e_mc = N.eco_de('MC', 1); e_c = NE.eco_de('CEREBRO', 1)
    E_mc = ME._eco_cfg(dict(e_mc), __import__('pista2').cfg_fabrica(), 90)
    chk("(A) eco_de('MC'): mutables = rep_umbral + los 15 del cerebro (16, orden de NOMBRES); p 0.05 y sigma 0.15 por gen, == eco_sel en todo lo demas",
        list(e_mc['mutables']) == mc and len(mc) == 16 and set(mc) - set(NE.GENETICAS['CEREBRO']['mutables']) == {'rep_umbral'}
        and [float(x) for x in E_mc['pv']] == [0.05 if g in mc else 0.0 for g in ME.NOMBRES] and e_mc['sigma'] == 0.15
        and {k: v for k, v in e_mc.items() if k != 'mutables'} == {k: v for k, v in e_c.items() if k != 'mutables'}
        and N.eco_de('MC_AZAR', 1)['donante'] == 'azar' and N.eco_de('MC_AZAR', 1)['mutables'] == e_mc['mutables'],
        f"(pv > 0 en {[g for g, q in zip(ME.NOMBRES, E_mc['pv']) if q > 0]})")
    chk("(A) los brazos de eco_sel quedan como estaban en el nucleo largo", all(N.BRAZOS[b] == NE.BRAZOS[b] for b in NE.BRAZOS)
        and all(N.GENETICAS[g] == NE.GENETICAS[g] for g in NE.GENETICAS))
    t1 = time.time(); N.usa_gemelo()
    MF.run_solapadas(PR[0], ['FAMB_RES0_ECO'] * 9, T=200, diag=0, mundo_n=9, tope_cuerpos=3000, muestra=1000, eco=CR.eco_cfg('MUT0', 1))
    print(f"  (compilacion / cache de motor_frio_rapido: {time.time() - t1:.0f} s)", flush=True)
    # (A) a T = 1e6: identidad con eco_sel y medida del checkpoint
    T6 = 1_000_000
    medidas = {}
    for b in ('F1', 'SEL_C'):
        NE.usa_gemelo()
        x = NE.trabajo((PR[0], b, T6, 1, 120000, tempfile.mkdtemp(prefix='esl_A_e_'), False))
        N.usa_gemelo()
        reg = []; orig = C._mide_ckpt(reg)
        try:
            y = N.trabajo((PR[0], b, T6, 1, 120000, tempfile.mkdtemp(prefix='esl_A_l_'), False))
        finally:
            CR.ME.run_solapadas = orig
        medidas[b] = reg
        dist = [k for k in x if k != 'seg' and J(x[k]) != J(y.get(k))]
        nuevas = sorted(set(y) - set(x))
        chk(f"(A) T 1e6 {b}: nucleo largo == nucleo_eco_sel en TODAS las claves de eco_sel salvo seg; clave nueva solo 'ventanas'",
            not dist and nuevas == ['ventanas'] and y['motor'] == 'GEMELO motor_frio_rapido',
            f"(persiste {x['persiste']}, vivos_T {x['vivos_T']}, n_nac {x['n_nac']}, K eco_sel {round(CE.kbar(x, T6), 3)}; distintas {dist}; "
            f"nuevas {nuevas}; {x['seg']} s eco_sel (ckpt 10 000) contra {y['seg']} s largo (ckpt 100 000))")
        chk(f"(A) T 1e6 {b}: kvent(x, T/2, T) == kbar de corre_eco_sel exacto; K por ventana = {[round(k, 2) for k in C.kcurva(y, T6)]}",
            C.kvent(y, T6 // 2, T6, T6) == CE.kbar(x, T6) == C.kbar(y, T6))
        print(f"  (checkpoint {b} a T 1e6, (t, bytes, s): {reg})", flush=True)
    # (B) el genoma fijo
    y = N.trabajo((PR[1], 'F1', 60000, 1, 60000, tempfile.mkdtemp(prefix='esl_B_f1_'), False))
    # ERR candidato (arnes, 1a corrida 61/64, antes del humo): el caso del encargo "SEL_MC con sigma = 0 == F1" NO puede valer con genes
    # ENTEROS: motor_eco.muta redondea y, si el valor no cambia, mueve el gen +-1 segun el signo de z; con sigma = 0, z = 0 -> -1 siempre.
    # memoria_rechazo y NK (enteros, en los 16 de MC) se mueven con sigma = 0. El caso se parte en dos: (B) p_mut = 0 == F1 bit a bit
    # (el camino de 16 mutables, banco y donante corre y no mueve nada) y (B') sigma = 0 mueve SOLO los dos enteros.
    N._PMUT[0] = 0.0
    try:
        B0 = {b: N.trabajo((PR[1], b, 60000, 1, 60000, tempfile.mkdtemp(prefix='esl_B0_'), False)) for b in ('SEL_MC', 'AZA_MC')}
    finally:
        N._PMUT[0] = None
    G0 = dict(zip(ME.NOMBRES, y['G0']))
    for b, z in B0.items():
        dist = [k for k in y if k not in CONFIG and J(y[k]) != J(z.get(k))]
        vz, vy = z['ventanas'], y['ventanas']
        tel_ok = all(vz[k] == vy[k] for k in ('W', 'vivos', 'nac', 'muertes', 'vida_media', 'media_log'))
        g0_ok = all(v is None or abs(v - round(G0[g], 6)) < 1e-12 for g, d in vz['genes'].items() for c in d.values() for v in c)
        chk(f"(B) {b} con p_mut = 0 (16 mutables, banco y donante {z['donante']}: el camino corre y no mueve) == F1 bit a bit (salvo configuracion; "
            f"ventanas iguales; genes = G0)", not dist and tel_ok and g0_ok and z['p_mut'] == 0.0 and z['mutables'] == [] and z['n_mut'] == 0,   # E['mutables'] = los de p > 0
            f"(distintas {dist}; n_nac {z['n_nac']} F1 {y['n_nac']})")
    N._SIGMA[0] = 0.0
    try:
        zs = N.trabajo((PR[1], 'SEL_MC', 60000, 1, 60000, tempfile.mkdtemp(prefix='esl_Bs_'), False))
    finally:
        N._SIGMA[0] = None
    ent = [g for g in mc if ME.GENES[ME.NOMBRES.index(g)][2]]
    Vs = [dict(zip(ME.NOMBRES, v[4:])) for v in zs['vivos_final']]
    flot_g0 = all(v[g] == round(G0[g], 6) for v in Vs for g in mc if g not in ent)
    ent_mov = {g: sum(1 for v in Vs if v[g] != round(G0[g], 6)) for g in ent}
    chk("(B') SEL_MC con sigma = 0: los 14 genes reales quedan en G0 en todos los vivos; solo se mueven los enteros (memoria_rechazo, NK: paso -1 de muta con z = 0)",
        ent == ['memoria_rechazo', 'NK'] and flot_g0 and all(n > 0 for n in ent_mov.values()), f"(enteros movidos en vivos {ent_mov} de {len(Vs)})")
    S = {b: N.trabajo((PR[1], b, 60000, 1, 60000, tempfile.mkdtemp(prefix='esl_B1_'), False)) for b in ('SEL_MC', 'AZA_MC')}
    fis = lambda r: J([r['tam_total'], r['n_nac'], r['vivos_final']])
    chk("(B) CONTROL: con sigma = 0.15 la fisica de SEL_MC difiere de la de F1", fis(S['SEL_MC']) != fis(y),
        f"(n_nac F1 {y['n_nac']} · SEL_MC {S['SEL_MC']['n_nac']}; n_mut {S['SEL_MC']['n_mut']})")
    chk("(B) CONTROL: AZA_MC (los mismos genes sin herencia) difiere de SEL_MC", fis(S['AZA_MC']) != fis(S['SEL_MC']),
        f"(n_nac AZA_MC {S['AZA_MC']['n_nac']}; donante {S['AZA_MC']['donante']})")
    for b in ('SEL_MC', 'AZA_MC'):
        chk(f"(M) {b} T 60 000 p 0.05: mutables = los 16; 0 valores fuera de G0 en dote y rep_X; genes movidos en los vivos",
            S[b]['mutables'] == mc and S[b]['fuera_mutables'] == 0 and S[b]['movidos_mutables'] > 0,
            f"(movidos {S[b]['movidos_mutables']} de {S[b]['vivos_T']} vivos x 16)")
    # (T) telemetria
    for b in ('SEL_MC', 'F1'):
        x = S['SEL_MC'] if b == 'SEL_MC' else y
        vt = x['ventanas']; gt = {f[0]: f for f in x['gen_t']}
        ok_v = all(vt['vivos'][k] == gt[W][1] == x['tam_total'][W // 1000] for k, W in enumerate(vt['W']))
        ok_l = all((vt['media_log'][k] is None and gt[W][4] is None) or max(abs(a - c) for a, c in zip(vt['media_log'][k], gt[W][4])) <= 1e-5
                   for k, W in enumerate(vt['W']))
        n_muertes = sum(sum(m) for m in vt['muertes'])
        ok_n = sum(vt['nac']) == x['n_nac'] and n_muertes == x['n_nac'] + 90 - x['vivos_T']
        ok_q = True
        if x['mutables']:
            V = np.array([v[4:] for v in x['vivos_final']])
            for g in x['mutables']:
                j = ME.NOMBRES.index(g); q = np.quantile(V[:, j], [0.1, 0.5, 0.9])
                d = vt['genes'][g]
                # vivos_final guarda los genes redondeados a 1e-6: los cuantiles de la telemetria (valores crudos) difieren <= 1e-6
                # (ERR candidato de la 1a corrida del arnes: el caso exigia igualdad exacta)
                ok_q &= max(abs(d['q10'][-1] - q[0]), abs(d['q50'][-1] - q[1]), abs(d['q90'][-1] - q[2]), abs(d['media'][-1] - V[:, j].mean())) <= 2e-6
        chk(f"(T) {b}: vivos por borde == gen_t[W][1] == tam_total[W/1000]; media_log == gen_t[W][4]; nac y muertes cuadran; cuantiles en W = T",
            ok_v and ok_l and ok_n and ok_q and len(vt['W']) == 10,
            f"(vivos {vt['vivos']}; nac {sum(vt['nac'])} = n_nac {x['n_nac']}; muertes {n_muertes} = {x['n_nac']} + 90 - {x['vivos_T']})")
    # (P) independencia de T
    x2 = N.trabajo((PR[1], 'SEL_MC', 120000, 1, 60000, tempfile.mkdtemp(prefix='esl_P_'), False))
    chk("(P) SEL_MC: tam_total y vivos por borde de T 120 000 empiezan con los de T 60 000 (la dinamica no depende de T)",
        x2['tam_total'][:61] == S['SEL_MC']['tam_total'][:61] and x2['ventanas']['vivos'][4] == S['SEL_MC']['ventanas']['vivos'][9],
        f"(K [T/2, T] 60k {round(C.kbar(S['SEL_MC'], 60000), 2)}; misma ventana en 120k {round(C.kvent(x2, 30000, 60000, 120000), 2)})")
    # (Z) determinismo
    z2 = N.trabajo((PR[1], 'SEL_MC', 60000, 1, 60000, tempfile.mkdtemp(prefix='esl_Z_'), False))
    dz = [k for k in z2 if k != 'seg' and J(z2[k]) != J(S['SEL_MC'].get(k))]
    chk("(Z) determinismo: SEL_MC dos veces == bit a bit (todas las claves salvo seg)", not dz, f"(distintas {dz})")
    # (C) gemelo == Python; (D) frio limpio
    RC = {}
    for b in ('SEL_MC', 'AZA_MC'):
        CR.ME = N.ME_PY
        p = N.trabajo((PR[2], b, 4000, 1, 3000, tempfile.mkdtemp(prefix='esl_C_py_'), False))
        N.usa_gemelo()
        g = N.trabajo((PR[2], b, 4000, 1, 3000, tempfile.mkdtemp(prefix='esl_C_g_'), False))
        dist = [k for k in p if k not in ('seg', 'motor', 'lim_nac') and J(p[k]) != J(g.get(k))]
        chk(f"(C) {b}: gemelo == motor Python en trabajo() (T 4000, w90; ventanas incluidas)",
            not dist and p['motor'].startswith('PYTHON') and g['motor'].startswith('GEMELO'),
            f"(n_nac {p['n_nac']}, n_mut {p['n_mut']}; distintas {dist}; {p['seg']} s contra {g['seg']} s)")
        RC[b] = g
    N._PMUT[0] = 1.0
    try:
        for b in ('SEL_MC', 'AZA_MC'):
            CR.ME = N.ME_PY
            p = N.trabajo((PR[2], b, 4000, 1, 3000, tempfile.mkdtemp(prefix='esl_C2_py_'), False))
            N.usa_gemelo()
            g = N.trabajo((PR[2], b, 4000, 1, 3000, tempfile.mkdtemp(prefix='esl_C2_g_'), False))
            dist = [k for k in p if k not in ('seg', 'motor', 'lim_nac') and J(p[k]) != J(g.get(k))]
            chk(f"(C) {b} con p_mut = 1: gemelo == motor Python (T 4000)", not dist and p['n_mut'] > 0, f"(n_mut {p['n_mut']}; distintas {dist})")
    finally:
        N._PMUT[0] = None
    for b, g in RC.items():
        chk(f"(D) {b}: 0 refundados y 0 fundadores repuestos", g['n_refund'] == 0 and g['fundadores_rep'] == 0 and g['t_fund_primero'] is None)
    N.usa_gemelo()
    gv = N.trabajo((PR[2], 'SEL_MC', 4000, 1500, 3000, tempfile.mkdtemp(prefix='esl_D_'), False))
    chk("(D) CONTROL que puede fallar: SEL_MC con vivero (t_corte 1500) SI refunda", gv['n_refund'] > 0 and gv['fundadores_rep'] > 0,
        f"(refundados {gv['n_refund']})")
    # (H) y (M): herencia exacta y genes exactos con p_mut = 1
    import pista2 as P
    N._PMUT[0] = 1.0
    try:
        for gen in ('MC', 'MC_AZAR'):
            filas = []
            eco = N.eco_de(gen, 1, ind_cb=lambda li, row, g: filas.append((li, list(row), np.array(g, float))))
            E_ = ME._eco_cfg(dict(eco), P.cfg_fabrica(), 90)
            MF.run_solapadas(PR[3], ['FAMB_RES0_ECO'] * 90, T=20000, diag=0, mundo_n=90, tope_cuerpos=3000, muestra=1000, eco=eco)
            gen_de = {(li, row[0]): g for li, row, g in filas}
            fund_de = {(li, row[0]): row[6] for li, row, g in filas}
            hijos = [(li, row, g) for li, row, g in filas if not row[6]]
            cu = {True: [0, 0], False: [0, 0]}
            movidos = np.zeros(len(ME.NOMBRES), int)
            for li, row, g in hijos:
                gp = gen_de.get((li, row[2]))
                if gp is None: continue
                esp, _ = ME.muta(gp, np.random.default_rng([PR[3], li, ME.ETQ_MUT, row[0]]), E_['pv'], float(E_['sigma']), E_['lo'], E_['hi'])
                pf = bool(fund_de[(li, row[2])]); cu[pf][0] += int(np.array_equal(esp, g)); cu[pf][1] += 1
                movidos += (g != gp).astype(int)
            iguales, con_padre = cu[False]; fr = iguales / max(1, con_padre)
            det = f"(padre no fundador: {iguales}/{con_padre} = {fr:.3f}; padre fundador: {cu[True][0]}/{cu[True][1]})"
            if gen == 'MC_AZAR':
                chk(f"(H) {gen}: el control rompe la copia padre -> hijo (hijos de padre NO fundador == muta(padre) < 5 %; caso H de ERR-149)",
                    con_padre >= 50 and fr < 0.05, det)
            else:
                chk(f"(H) {gen}: TODO hijo == muta(genoma del padre, rng [s, lin, 16, k]) (herencia exacta)",
                    con_padre >= 50 and iguales == con_padre and cu[True][0] == cu[True][1], det)
                mv = [ME.NOMBRES[j] for j in range(len(movidos)) if movidos[j] > 0]
                chk("(M) MC con p_mut = 1: los genes que cambian padre -> hijo son EXACTAMENTE los 16 declarados (dote y rep_X nunca)",
                    sorted(mv) == sorted(mc), f"(cambian {len(mv)}: fuera de los 16 {sorted(set(mv) - set(mc))}; no cambian {sorted(set(mc) - set(mv))})")
    finally:
        N._PMUT[0] = None
    # (Q) corte de luz + reanuda (checkpoint cada 100 000)
    N.usa_gemelo()
    bq = 'SEL_MC'; sq = PR[4]
    entera = N.trabajo((sq, bq, 200000, 1, 150000, tempfile.mkdtemp(prefix='esl_Q_a_'), False))
    tq = tempfile.mkdtemp(prefix='esl_Q_b_')
    orig_q = CR.ME.run_solapadas

    def corta(*a, _o=orig_q, **k):
        fn = k['eco']['ckpt_fn']

        def fn2(t, blob):
            fn(t, blob)
            if t == 100000: raise KeyboardInterrupt('corte de luz simulado en t = 100000')
        k['eco'] = dict(k['eco'], ckpt_fn=fn2)
        return _o(*a, **k)
    CR.ME.run_solapadas = corta
    try:
        N.trabajo((sq, bq, 200000, 1, 150000, tq, False)); cortado = False
    except KeyboardInterrupt:
        cortado = True
    finally:
        CR.ME.run_solapadas = orig_q
    hay_ck = os.path.exists(os.path.join(tq, 'ckpt', f'{bq}_s{sq}.pkl')) and not os.path.exists(os.path.join(tq, f'{bq}_s{sq}.json'))
    re = N.trabajo((sq, bq, 200000, 1, 150000, tq, True))
    dist = [k for k in entera if k != 'seg' and J(entera[k]) != J(re.get(k))]
    chk(f"(Q) {bq}: corte en t = 100 000 + --reanuda == la corrida entera (T 200 000; ventanas incluidas)", cortado and hay_ck and not dist and entera['t_ext'] is None,
        f"(semilla {sq}, cortado {cortado}, checkpoint {hay_ck}, distintas {dist}, vivos por borde {entera['ventanas']['vivos']}; {entera['seg']} s)")
    # (F) nube-9
    orig = CR.ME.run_solapadas
    try:
        tmp = tempfile.mkdtemp(prefix='esl_F_')

        def guardia(*a, **k): raise SystemExit('PISTA2: mas de 100000 cuerpos en un linaje: la semilla colisionaria (ERR-60)')

        def otro(*a, **k): raise SystemExit('motor: otra cosa')
        CR.ME.run_solapadas = guardia
        try: r1 = N.trabajo((PR[0], 'SEL_MC', 3000, 1, 2500, tmp, False)); ok1 = True
        except BaseException: r1 = {}; ok1 = False
        CR.ME.run_solapadas = otro
        try: r2 = N.trabajo((PR[0], 'AZA_MC', 3000, 1, 2500, tmp, False)); ok2 = True
        except BaseException: r2 = {}; ok2 = False
    finally:
        CR.ME.run_solapadas = orig
    chk("(F) la guardia ERR-60 no se propaga: persiste 1, guardia 1, JSON escrito",
        ok1 and r1.get('persiste') == 1 and r1.get('guardia') == 1 and os.path.exists(os.path.join(tmp, f'SEL_MC_s{PR[0]}.json')))
    chk("(F) otro aborto no se propaga: persiste None, marcado", ok2 and r2.get('persiste') is None and r2.get('aborto'))
    chk("(F) LIM_NAC del gemelo = 1e9 (ERR-146)", MF.LIM_NAC == 1_000_000_000)
    # (V) la letra
    T = C.T_LARGO
    BASE = {'F1': (31.0, 31.0), 'SEL_C': (39.0, 43.0), 'SEL_MC': (40.0, 46.0), 'AZA_MC': (22.0, 20.0), 'SEL_M': (35.0, 36.0)}

    def fake(K=None, pers=None, T_=T, quita=0, sucio=None, bloq=(), aborto=None, fuera=None, nomut=None, tc=None, semilla_mala=False,
             ajeno=False, extingue=None):
        K = dict(BASE, **(K or {}))
        pers = dict({b: 20 for b in C.BRAZOS}, **(pers or {}))
        R = []
        n = T_ // 1000 + 1; i_b = (T_ // 10) // 1000; i_f = (9 * T_ // 10) // 1000
        for i in range(20):
            for b, (gen, carro, tcb) in C.BRAZOS.items():
                kb, kf = K[b]
                kb = kb[i] if isinstance(kb, list) else kb; kf = kf[i] if isinstance(kf, list) else kf
                tt = [kb] * (i_b + 1) + [(kb + kf) / 2] * (i_f - i_b - 1) + [kf] * (n - i_f)
                if extingue == b: tt = tt[:5000]
                mut = (list(N.GENETICAS[gen]['mutables'] or []) if N.GENETICAS[gen]['p'] else [])
                x = dict(seed=45401 + i + (1 if (semilla_mala and b == 'AZA_MC' and i == 0) else 0), brazo=b, T=T_,
                         t_corte=(tc if (tc is not None and b == 'SEL_MC') else tcb), persiste=int(i < pers[b]), tam_total=tt,
                         bloqueados=(3 if (i in bloq and b == 'SEL_C') else 0), n_refund=0, fundadores_rep=0, aborto=None, guardia=0,
                         genes=list(ME.NOMBRES), gen_t=[], mutables=mut, fuera_mutables=0, tasa_mut=(0.0 if not mut else 0.01))
                if nomut == b: x['tasa_mut'] = 0.0
                if sucio == b and i == 3: x['n_refund'] = 1
                if aborto == b and i == 2: x.update(aborto='SystemExit: otra cosa', persiste=None)
                if fuera == b and i == 5: x['fuera_mutables'] = 2
                R.append(x)
            if ajeno and i == 0: R.append(dict(R[-1], brazo='AZA_C'))
        return R[:len(R) - quita]
    L14 = [43.0] * 14 + [38.0] * 6
    casos = [
        ("FUNCIONA en L y en MC", fake(), {'L': 'FUNCIONA', 'MC': 'FUNCIONA'}),
        ("L MODESTO: SEL_C sube +1 en 20/20 (mediana < +2)", fake(K={'SEL_C': (39.0, 40.0), 'SEL_MC': (40.0, 43.0)}), {'L': 'HAY ALGO MODESTO', 'MC': 'FUNCIONA'}),
        ("L NO: SEL_C se estanca (dK = 0: empate no cuenta)", fake(K={'SEL_C': (39.0, 39.0)}), {'L': 'NO:'}),
        ("L NO: SEL_C baja", fake(K={'SEL_C': (39.0, 36.0), 'SEL_MC': (40.0, 38.0)}), {'L': 'NO:', 'MC': 'FUNCIONA'}),
        ("L NO: sube en 14/20 aunque la mediana sea +4", fake(K={'SEL_C': (39.0, L14)}), {'L': 'NO:'}),
        ("L-2a: AZA_MC tambien sube +3 en 20/20 -> NO", fake(K={'AZA_MC': (22.0, 25.0)}), {'L': 'NO:'}),
        ("L-2b: AZA_MC sube +6 en 14/20 (L-2a pasa) y SEL_C +4 le gana solo en 6 -> NO",
         fake(K={'AZA_MC': (22.0, [28.0] * 14 + [22.0] * 6)}), {'L': 'NO:', 'MC': 'FUNCIONA'}),
        ("L-3: F1 sube +5 (el tiempo solo) y SEL_C +4 -> NO", fake(K={'F1': (31.0, 36.0)}), {'L': 'NO:', 'MC': 'FUNCIONA'}),
        ("L NO: SEL_C se extingue a mitad de T (K final 0)", fake(extingue='SEL_C'), {'L': 'NO:'}),
        ("MC MODESTO: SEL_MC = SEL_C + 1 en la ventana final", fake(K={'SEL_MC': (40.0, 44.0)}), {'MC': 'HAY ALGO MODESTO', 'L': 'FUNCIONA'}),
        ("MC NO: SEL_MC = SEL_C (empate)", fake(K={'SEL_MC': (40.0, 43.0)}), {'MC': 'NO:'}),
        ("MC NO: SEL_MC +3 sobre SEL_C solo en 14/20", fake(K={'SEL_MC': (40.0, [46.0] * 14 + [42.0] * 6)}), {'MC': 'NO:'}),
        ("MC-2: AZA_MC >= SEL_MC -> NO", fake(K={'AZA_MC': (22.0, 46.0)}), {'MC': 'NO:'}),
        ("V1: F1 persiste 16/20 -> las dos NO EVALUABLE", fake(pers={'F1': 16}), {'L': 'NO EVALUABLE (el ancla', 'MC': 'NO EVALUABLE (el ancla'}),
        ("V2: un refundado en AZA_MC -> las dos NO EVALUABLE", fake(sucio='AZA_MC'), {'L': 'NO EVALUABLE (un brazo', 'MC': 'NO EVALUABLE (un brazo'}),
        ("bloqueados en 2 semillas: evaluable (18/20 cuentan) -> FUNCIONA", fake(bloq=(0, 1)), {'L': 'FUNCIONA', 'MC': 'FUNCIONA'}),
        ("bloqueados en 3 semillas -> las dos NO EVALUABLE", fake(bloq=(0, 1, 2)), {'L': 'NO EVALUABLE (tope', 'MC': 'NO EVALUABLE (tope'}),
        ("bloqueadas cuentan como fallo: SEL_C sube en 16/20, 2 de ellas bloqueadas -> 14 -> L NO",
         fake(K={'SEL_C': (39.0, [43.0] * 16 + [38.0] * 4)}, bloq=(0, 1)), {'L': 'NO:'}),
        ("V3: SEL_MC con genes fuera -> MC NO EVALUABLE; L sigue", fake(fuera='SEL_MC'), {'MC': 'NO EVALUABLE (la genetica', 'L': 'FUNCIONA'}),
        ("V3: SEL_C sin mutacion -> L y MC NO EVALUABLE", fake(nomut='SEL_C'), {'L': 'NO EVALUABLE (la genetica', 'MC': 'NO EVALUABLE (la genetica'}),
        ("V3: F1 con mutacion -> las dos NO EVALUABLE", [dict(x, tasa_mut=(0.01 if x['brazo'] == 'F1' else x['tasa_mut'])) for x in fake()],
         {'L': 'NO EVALUABLE (la genetica', 'MC': 'NO EVALUABLE (la genetica'}),
        ("T distinto -> NO EVALUABLE", fake(T_=1_000_000), {'L': 'NO EVALUABLE (serie', 'MC': 'NO EVALUABLE (serie'}),
        ("serie incompleta -> NO EVALUABLE", fake(quita=1), {'L': 'NO EVALUABLE (serie'}),
        ("un aborto -> NO EVALUABLE", fake(aborto='SEL_M'), {'L': 'NO EVALUABLE (serie', 'MC': 'NO EVALUABLE (serie'}),
        ("t_corte distinto de 1 -> NO EVALUABLE", fake(tc=60000), {'MC': 'NO EVALUABLE (serie'}),
        ("semillas distintas entre brazos -> NO EVALUABLE", fake(semilla_mala=True), {'L': 'NO EVALUABLE (serie'}),
        ("un brazo ajeno (AZA_C) en la carpeta -> NO EVALUABLE", fake(ajeno=True), {'L': 'NO EVALUABLE (serie'}),
    ]
    for nombre, R, esp in casos:
        v, L, d = C.veredicto(R, 20)
        ok = all(v[q].startswith(e) for q, e in esp.items())
        chk(f"(V) {nombre}", ok, f"-> L: {v['L'][:60]} | MC: {v['MC'][:60]}")
    rng = np.random.default_rng(7)
    tt = [int(v) for v in rng.integers(0, 60, 10001)]
    xx = dict(tam_total=tt)
    chk("(V) kvent: [T/2, T] == kbar de eco_sel (con y sin extincion); base = muestras 500..1000; final = 9000..10000",
        C.kvent(xx, T // 2, T, T) == CE.kbar(xx, T) and C.kbar(dict(tam_total=tt[:7000]), T) == CE.kbar(dict(tam_total=tt[:7000]), T)
        and C.kbase(xx, T) == float(np.mean(tt[500:1001])) and C.kfin(xx, T) == float(np.mean(tt[9000:10001]))
        and C.kbase(dict(tam_total=tt[:10]), T) == 0.0)
    # (R) banderas
    malas = [['--help'], ['-h'], [], ['--serie'], ['--humo', '--serie'], ['--serie', '--desde', '45401', '--n', '20'],
             ['--serie', '--desde=45401', '--n', '20', '--pool', '3'], ['--serie', '--des', '45401', '--n', '20', '--pool', '3'],
             ['--serie', '--desde', '45402', '--n', '20', '--pool', '3'], ['--serie', '--desde', '45401', '--n', '19', '--pool', '3'],
             ['--serie', '--desde', '45401', '--n', '20', '--pool', '7'], ['--humo', '--pool', '2'], ['--humo', '--humo'],
             ['--lee', 'x', '--pool', '2'], ['--gemelo', '--humo'], ['--serie', '--desde', '45301', '--n', '20', '--pool', '3']]
    n_ab = 0
    for m in malas:
        try: C.parsea(m)
        except C.BanderaMala: n_ab += 1
    chk(f"(R) el parser aborta ante {len(malas)} formas de bandera mala", n_ab == len(malas), f"({n_ab}/{len(malas)})")
    buenas = [['--humo'], ['--serie', '--desde', '45401', '--n', '20', '--pool', '3'], ['--serie', '--desde', '45421', '--n', '20', '--pool', '3', '--reanuda'],
              ['--lee', 'datos/x']]
    n_ok = 0
    for m in buenas:
        try: C.parsea(m); n_ok += 1
        except C.BanderaMala: pass
    chk(f"(R) el parser acepta las {len(buenas)} formas buenas", n_ok == len(buenas), f"({n_ok}/{len(buenas)})")
    antes = set(glob.glob(os.path.join(AQUI, 'datos', '**', '*'), recursive=True))
    pr = subprocess.run([sys.executable, os.path.join(AQUI, 'corre_eco_sel_largo.py'), '--serie', '--desde', '45401', '--n', '20', '--pool', '3', '--nada'],
                        capture_output=True, text=True, timeout=300)
    despues = set(glob.glob(os.path.join(AQUI, 'datos', '**', '*'), recursive=True))
    chk("(R) subproceso con bandera desconocida: codigo != 0 y no escribe nada", pr.returncode != 0 and antes == despues, f"(codigo {pr.returncode})")
    rss = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024
    print(f"  (checkpoint a T 1e6 con CKPT_LARGO, (t, bytes, s): {medidas}; memoria maxima del proceso {rss:.0f} MB)")
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
    open(os.path.join(AQUI, 'identidad_eco_sel_largo_salida.txt'), 'w', encoding='utf-8').write(buf.getvalue())
    sys.exit(0 if ok else 1)
