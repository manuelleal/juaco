"""identidad_eco_sel_ing.py — ARNES de ECO_SEL_ING. Un proceso, sin Pool, sin serie. Semillas de PRACTICA 46191-46194.

MISION: llegar a la AGI por este camino (organismo minimo con reglas locales, sin retropropagacion, peldanos preregistrados con
controles y replicas); el metodo manda sobre el como.

  (K) construye_eco_sel_ing.py --verifica y origenes con su sha (verifica()).
  (A) el nucleo ING con los brazos de ECO_SEL (F1, SEL_C) == nucleo_eco_sel.trabajo en TODAS sus claves (solo se agregan las de
      _extra_ing); ING_F1 con t_corte 1 == corre_frio.trabajo(FAB_FRIO) en todas las claves de F1 (la base ingenua es la de F1).
      kbar y rango == los de eco_sel/corre_eco_sel.py en entradas.
  (I) INGENUO: ING_F1 (FABRICA_ECO) difiere de F1 (FAMB_RES0_ECO) en la misma semilla (control que puede fallar).
  (V) vivero permanente: ING_F1 con t_corte = T refunda en la 2a mitad (fund_2a > 0) y persiste; K_nac + K_fund == K EXACTO
      (ING_F1, ING_SEL_C con vivero; F1 en frio).
  (B) p_mut = 0 (perilla apagada): ING_SEL_C e ING_AZA_C == ING_F1 (vivero permanente) bit a bit salvo configuracion; con sigma = 0
      solo se mueven genes enteros (muta fuerza +-1: sigma = 0 no apaga la mutacion del cerebro). CONTROLES con sigma 0.15: la fisica
      de ING_SEL_C difiere de ING_F1; ING_AZA_C difiere de ING_SEL_C; solo se mueven los 15 del cerebro.
  (H) herencia EXACTA con p_mut = 1, FABRICA_ECO y vivero permanente: en CEREBRO todo hijo de padre NO fundador == muta(padre); en
      CEREBRO_AZAR < 5 % (caso H de ERR-149: los hijos de fundadores no cuentan).
  (C) gemelo == motor Python en trabajo() de los tres brazos ING (T 3000, vivero permanente).
  (D) determinismo: la misma corrida dos veces == bit a bit (salvo seg).
  (Q) corte de luz en t = 30 000 + --reanuda == la corrida entera (ING_SEL_C, T 40 000; k2 en el checkpoint).
  (L) la letra en entradas sinteticas.   (R) banderas.
Escribe identidad_eco_sel_ing_salida.txt.
"""
import contextlib, glob, io, json, os, subprocess, sys, tempfile, time
import numpy as np

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
R_ = []
J = lambda x: json.dumps(x, sort_keys=True, default=str)
PR = (46191, 46192, 46193, 46194)
CONFIG = {'brazo', 'genetica', 'seg', 'mutables', 'p_mut', 'sigma', 'donante', 'genes_vivos_T'}
EXTRA = {'K_nac', 'K_fund', 'fund_2a', 'n_k2'}
tmp = lambda p: tempfile.mkdtemp(prefix='eing_' + p + '_')


def chk(nombre, ok, det=''):
    R_.append(bool(ok)); print(f"  {'OK ' if ok else 'MAL'} {nombre} {det}", flush=True)


def main():
    t0 = time.time()
    import corre_eco_sel_ing as C
    N = C.N; CR = C.CR
    print(f"IDENTIDAD ECO_SEL_ING · {time.strftime('%Y-%m-%d %H:%M:%S')} · python {sys.version.split()[0]} · numpy {np.__version__} · shas {C.SHAS()}", flush=True)
    # (K)
    import construye_eco_sel_ing as CE
    chk("(K) nucleo_eco_sel_ing.py en disco == el construido por anclas desde eco_sel/nucleo_eco_sel.py (6a36e47ce61db3e1)", CE.main(['--verifica']))
    try: C.verifica(); okv = True
    except SystemExit as e: okv = False; print(e)
    chk("(K) verifica(): origenes con el sha fijado", okv)
    # (A)
    ES_DIR = os.path.join(N.RAIZ, 'experimentos', 'organelos', 'eco_sel')
    sys.path.insert(0, ES_DIR); sys.path.insert(0, N.FRIO_DIR)
    import nucleo_eco_sel as NE
    import corre_eco_sel as CES
    import corre_frio as F
    import motor_frio_rapido as MF
    chk("(A) un solo corre_eco en el proceso (N, NE y F comparten CR)", NE.CR is CR and F.CR is CR)
    chk("(A) los cinco brazos de ECO_SEL estan sin tocar en el nucleo ING; ING_* con FABRICA_ECO y t_corte None",
        all(N.BRAZOS[b] == NE.BRAZOS[b] for b in NE.BRAZOS) and all(N.BRAZOS[b][1] == 'FABRICA_ECO' and N.BRAZOS[b][2] is None for b in N.ING)
        and N.GENETICAS == NE.GENETICAS and N.tc_de('ING_F1', 12345) == 12345 and N.tc_de('F1', 12345) == 1)
    t1 = time.time(); N.usa_gemelo()
    MF.run_solapadas(PR[0], ['FABRICA_ECO'] * 9, T=200, diag=0, mundo_n=9, tope_cuerpos=3000, muestra=1000, eco=CR.eco_cfg('MUT0', 1))
    print(f"  (compilacion / cache del gemelo: {time.time() - t1:.0f} s)", flush=True)
    for b in ('F1', 'SEL_C'):
        NE.usa_gemelo(); x = NE.trabajo((PR[0], b, 60000, 1, 50000, tmp('A_ne'), False))
        N.usa_gemelo(); y = N.trabajo((PR[0], b, 60000, 1, 50000, tmp('A_n'), False))
        dist = [k for k in x if k != 'seg' and J(x[k]) != J(y.get(k))]
        nuevas = sorted(set(y) - set(x))
        chk(f"(A) nucleo ING trabajo({b}) == nucleo_eco_sel.trabajo({b}) en TODAS sus claves salvo seg; solo se agregan {sorted(EXTRA)} (T 60 000)",
            not dist and set(nuevas) == EXTRA, f"(distintas {dist}; nuevas {nuevas}; n_nac {x['n_nac']}, K_nac {y['K_nac']}, K_fund {y['K_fund']})")
        if b == 'F1': yF1 = y
    F.usa_gemelo(); x = F.trabajo((PR[0], 'FAB_FRIO', 20000, 1, 15000, tmp('A_fab'), False))
    N.usa_gemelo(); y = N.trabajo((PR[0], 'ING_F1', 20000, 1, 15000, tmp('A_ing'), False))
    dist = [k for k in x if k not in ('brazo', 'seg') and J(x[k]) != J(y.get(k))]
    chk("(A) ING_F1 con t_corte 1 == corre_frio.trabajo(FAB_FRIO) en TODAS las claves de F1 salvo brazo y seg (T 20 000): la base ingenua es FAB_FRIO",
        not dist and y['carro'] == 'FABRICA_ECO', f"(persiste {x['persiste']}, t_ext {x['t_ext']}, n_nac {x['n_nac']}; distintas {dist})")
    xa = dict(tam_total=list(range(40)) + [7] * 300); xb = dict(tam_total=[3] * 1001)
    NOM0 = list(N.ME_PY.NOMBRES); SB = [[0.1 * (q + 1)] * len(NOM0) for q in range(8)]
    fr = lambda v: dict(genes=NOM0, gen_t=[[N.T_SEL, 0, 0, 0, None, None, [v] * len(NOM0), SB]])
    chk("(A) kbar y rango == los de eco_sel/corre_eco_sel.py en entradas (regla 14)",
        all(C.kbar(z, T) == CES.kbar(z, T) for z in (xa, xb) for T in (200000, 500000, 1000000, 60000))
        and all(C.rango(fr(v), g) == CES.rango(fr(v), g) for v in (0.0, 0.05, 0.1, 0.45, 0.85) for g in ('alpha', 'tau_e'))
        and N.T_SEL == NE.T_SEL == 100000)
    # (I) ingenuo
    chk("(I) CONTROL que puede fallar: ING_F1 (sin tabla) difiere de F1 (con tabla) en la misma semilla, frio, T 20 000",
        J([x['tam_total'], x['n_nac']]) != J([yF1['tam_total'][:21], yF1['n_nac']]),
        f"(ING_F1 t_ext {y['t_ext']}, n_nac {y['n_nac']} · F1 a 60 000 persiste {yF1['persiste']}, n_nac {yF1['n_nac']})")
    # (V) vivero permanente y K_nac + K_fund == K
    N.usa_gemelo()
    TV = 20000
    V = {b: N.trabajo((PR[1], b, TV, N.tc_de(b, TV), 15000, tmp('V'), False)) for b in N.ING}
    v0 = V['ING_F1']
    chk("(V) ING_F1 con vivero permanente (t_corte = T): persiste, refunda en la 2a mitad (fund_2a > 0), t_corte == T",
        v0['persiste'] == 1 and v0['fund_2a'] > 0 and v0['fundadores_rep'] > v0['fund_2a'] and v0['t_corte'] == TV and v0['carro'] == 'FABRICA_ECO',
        f"(K {C.kbar(v0, TV):.2f}, K_nac {v0['K_nac']}, K_fund {v0['K_fund']}, fund_2a {v0['fund_2a']}, fundadores_rep {v0['fundadores_rep']}, "
        f"{v0['seg']} s)")
    for b, z, T_ in [('ING_F1', v0, TV), ('ING_SEL_C', V['ING_SEL_C'], TV), ('ING_AZA_C', V['ING_AZA_C'], TV), ('F1 (frio, T 60 000)', yF1, 60000)]:
        k = C.kbar(z, T_)
        # ERR del arnes (1a corrida, 17:10): la tolerancia era 1e-9, pero _extra_ing redondea K_nac y K_fund a 6 decimales. Un cuerpo de
        # mas o de menos en una sola muestra mueve la suma en >= 1/501 (T 1e6) o 1/11 (T 20 000): 1.5e-6 sigue separando el error.
        chk(f"(V) {b}: K_nac + K_fund == K (mismo muestreo que tam_total; tolerancia 1.5e-6 por el redondeo a 6 decimales)",
            abs(z['K_nac'] + z['K_fund'] - k) < 1.5e-6,
            f"(K {k:.6f} = {z['K_nac']} + {z['K_fund']})")
    # (B) la perilla apagada. ERR del arnes (1a corrida, 17:10; candidato, el numero lo pone el coordinador): sigma = 0 NO apaga la mutacion
    # del cerebro. motor_eco.muta fuerza +-1 en los genes ENTEROS (NK, memoria_rechazo) cuando la mutacion dispara, aunque sigma = 0
    # (v = round(h * exp(0)) == h -> h +- 1). En ECO_SEL (B) se probo sigma = 0 solo con rep_umbral (real). Aqui la perilla apagada es
    # p_mut = 0 (el rng consume lo mismo: muta saca SIEMPRE 2 * NG numeros) y sigma = 0 queda como caso que documenta la propiedad.
    N._PMUT[0] = 0.0
    try:
        B0 = {b: N.trabajo((PR[1], b, TV, TV, 15000, tmp('B0'), False)) for b in ('ING_SEL_C', 'ING_AZA_C')}
    finally:
        N._PMUT[0] = None
    for b, z in B0.items():
        dist = [k for k in v0 if k not in CONFIG and J(v0[k]) != J(z.get(k))]
        chk(f"(B) {b} con p_mut = 0 (perilla apagada; donante {z['donante']}) == ING_F1 bit a bit (vivero permanente, T {TV}) salvo configuracion",
            not dist and z['p_mut'] == 0.0 and z['n_mut'] == 0 and z['donante'] == ('padre' if b == 'ING_SEL_C' else 'azar'),
            f"(distintas {dist}; el motor informa mutables {z['mutables']} con p_mut 0)")
    N._SIGMA[0] = 0.0
    try:
        B1 = {b: N.trabajo((PR[1], b, TV, TV, 15000, tmp('B1'), False)) for b in ('ING_SEL_C', 'ING_AZA_C')}
    finally:
        N._SIGMA[0] = None
    NOMg = list(N.ME_PY.NOMBRES); ENT = {g[0] for g in N.ME_PY.GENES if g[2]}
    for b, z in B1.items():
        G0r = [round(float(v), 6) for v in z['G0']]
        movg = sorted({NOMg[j] for v in z['vivos_final'] for j, x in enumerate(v[4:]) if x != G0r[j]})
        chk(f"(B) {b} con sigma = 0: solo se mueven genes ENTEROS (la propiedad de muta que hace que sigma = 0 no sea la perilla apagada)",
            set(movg) <= ENT and z['n_mut'] > 0, f"(genes movidos en los vivos {movg}; enteros {sorted(ENT)}; n_mut {z['n_mut']})")
    fis = lambda r: J([r['tam_total'], r['n_nac'], r['vivos_final']])
    ec = list(CR.BRAZOS['CEREBRO']['mutables'])
    chk("(B) CONTROL: con sigma 0.15 la fisica de ING_SEL_C difiere de ING_F1", fis(V['ING_SEL_C']) != fis(v0),
        f"(n_nac F1 {v0['n_nac']} · SEL {V['ING_SEL_C']['n_nac']}; n_mut {V['ING_SEL_C']['n_mut']})")
    chk("(B) CONTROL: ING_AZA_C difiere de ING_SEL_C", fis(V['ING_AZA_C']) != fis(V['ING_SEL_C']))
    chk("(B) ING_SEL_C e ING_AZA_C: mutables = los 15 del cerebro, 0 genes fuera movidos, alguno movido; ING_F1 sin mutacion",
        all(V[b]['mutables'] == ec and V[b]['fuera_mutables'] == 0 and V[b]['movidos_mutables'] > 0 for b in ('ING_SEL_C', 'ING_AZA_C'))
        and v0['n_mut'] == 0 and v0['mutables'] == [] and v0['movidos_mutables'] == 0)
    # (H) herencia exacta con p_mut = 1, FABRICA_ECO, vivero permanente
    import pista2 as P
    ME = N.ME_PY
    N._PMUT[0] = 1.0
    try:
        for gen in ('CEREBRO', 'CEREBRO_AZAR'):
            filas = []
            eco = N.eco_de(gen, TV, ind_cb=lambda li, row, g: filas.append((li, list(row), np.array(g, float))))
            E_ = ME._eco_cfg(dict(eco), P.cfg_fabrica(), 90)
            MF.run_solapadas(PR[2], ['FABRICA_ECO'] * 90, T=TV, diag=0, mundo_n=90, tope_cuerpos=3000, muestra=1000, eco=eco)
            gen_de = {(li, row[0]): g for li, row, g in filas}
            fund_de = {(li, row[0]): row[6] for li, row, g in filas}
            cu = {True: [0, 0], False: [0, 0]}
            for li, row, g in filas:
                if row[6]: continue
                gp = gen_de.get((li, row[2]))
                if gp is None: continue
                esp, _ = ME.muta(gp, np.random.default_rng([PR[2], li, ME.ETQ_MUT, row[0]]), E_['pv'], float(E_['sigma']), E_['lo'], E_['hi'])
                pf = bool(fund_de[(li, row[2])]); cu[pf][0] += int(np.array_equal(esp, g)); cu[pf][1] += 1
            iguales, con_padre = cu[False]; frc = iguales / max(1, con_padre)
            nref = sum(1 for li, row, g in filas if row[6] and row[3] > 0)
            det = f"(padre no fundador: {iguales}/{con_padre} = {frc:.3f}; padre fundador: {cu[True][0]}/{cu[True][1]}; refundados {nref})"
            if gen.endswith('AZAR'):
                chk(f"(H) {gen} (ingenuo, vivero permanente): el control rompe la copia padre -> hijo (< 5 %)", con_padre >= 50 and frc < 0.05, det)
            else:
                chk(f"(H) {gen} (ingenuo, vivero permanente): TODO hijo == muta(genoma del padre) (herencia exacta)",
                    con_padre >= 50 and iguales == con_padre and cu[True][0] == cu[True][1] and nref > 0, det)
    finally:
        N._PMUT[0] = None
    # (C) gemelo == Python
    for b in N.ING:
        CR.ME = N.ME_PY
        p = N.trabajo((PR[3], b, 3000, 3000, 2500, tmp('C_py'), False))
        N.usa_gemelo()
        g = N.trabajo((PR[3], b, 3000, 3000, 2500, tmp('C_g'), False))
        dist = [k for k in p if k not in ('seg', 'motor', 'lim_nac') and J(p[k]) != J(g.get(k))]
        chk(f"(C) {b}: gemelo == motor Python en trabajo() (T 3000, vivero permanente)",
            not dist and p['motor'].startswith('PYTHON') and g['motor'].startswith('GEMELO') and g['fundadores_rep'] > 0,
            f"(n_nac {p['n_nac']}, fundadores_rep {p['fundadores_rep']}, n_mut {p['n_mut']}; distintas {dist}; {p['seg']} s contra {g['seg']} s)")
    # (D) determinismo
    N.usa_gemelo()
    d2 = N.trabajo((PR[1], 'ING_SEL_C', TV, TV, 15000, tmp('D'), False))
    dist = [k for k in d2 if k != 'seg' and J(d2[k]) != J(V['ING_SEL_C'].get(k))]
    chk("(D) determinismo: ING_SEL_C dos veces == bit a bit (salvo seg)", not dist, f"(distintas {dist})")
    # (Q) corte de luz + reanuda
    bq = 'ING_SEL_C'; sq = PR[0]; TQ = 40000
    entera = N.trabajo((sq, bq, TQ, TQ, 35000, tmp('Q_a'), False))
    tq = tmp('Q_b'); orig_q = CR.ME.run_solapadas

    def corta(*a, _o=orig_q, **k):
        fn = k['eco']['ckpt_fn']

        def fn2(t, blob):
            fn(t, blob)
            if t == 30000: raise KeyboardInterrupt('corte de luz simulado en t = 30000')
        k['eco'] = dict(k['eco'], ckpt_fn=fn2)
        return _o(*a, **k)
    CR.ME.run_solapadas = corta
    try:
        N.trabajo((sq, bq, TQ, TQ, 35000, tq, False)); cortado = False
    except KeyboardInterrupt:
        cortado = True
    finally:
        CR.ME.run_solapadas = orig_q
    hay_ck = os.path.exists(os.path.join(tq, 'ckpt', f'{bq}_s{sq}.pkl')) and not os.path.exists(os.path.join(tq, f'{bq}_s{sq}.json'))
    re_ = N.trabajo((sq, bq, TQ, TQ, 35000, tq, True))
    dist = [k for k in entera if k != 'seg' and J(entera[k]) != J(re_.get(k))]
    chk(f"(Q) {bq}: corte en t = 30 000 + --reanuda == la corrida entera (T 40 000, vivero permanente; k2 incluida)", cortado and hay_ck and not dist,
        f"(cortado {cortado}, checkpoint {hay_ck}, distintas {dist}, n_k2 {entera['n_k2']}, fund_2a {entera['fund_2a']})")
    # (L) la letra
    NOM = list(ME.NOMBRES); G0 = [0.0] * len(NOM)
    VAL = {1: 0.05, 5: 0.45, 9: 0.85}
    T = 1_000_000

    def fake(K=None, Kn=None, F2=None, rk=None, pers=None, T_=T, quita=0, bloq=0, aborto=None, fuera=None, tc=None, carro=None,
             semilla_mala=False, nomut=None, extra_brazo=False):
        K = dict({'ING_F1': 96.0, 'ING_SEL_C': 105.0, 'ING_AZA_C': 92.0}, **(K or {}))
        Kn = dict({'ING_F1': 10.0, 'ING_SEL_C': 25.0, 'ING_AZA_C': 8.0}, **(Kn or {}))
        F2 = dict({'ING_F1': 125000, 'ING_SEL_C': 90000, 'ING_AZA_C': 130000}, **(F2 or {}))
        rk = dict({'ING_SEL_C': {'alpha': 9}}, **(rk or {}))
        pers = dict({b: 20 for b in N.ING}, **(pers or {}))
        R = []
        brz = list(N.ING) + (['SEL_C'] if extra_brazo else [])
        for i in range(20):
            for b in brz:
                gen = N.BRAZOS[b][0]
                k = K.get(b, 30.0); k = k[i] if isinstance(k, list) else k
                kn = Kn.get(b, 30.0); kn = kn[i] if isinstance(kn, list) else kn
                f2 = F2.get(b, 0); f2 = f2[i] if isinstance(f2, list) else f2
                br = [VAL[5]] * len(NOM)
                for g, r in rk.get(b, {}).items(): br[NOM.index(g)] = VAL[r]
                fila = [N.T_SEL, 30, 1, 40, G0, [G0] * 8, br, SB]
                mut = (list(N.GENETICAS[gen]['mutables'] or []) if N.GENETICAS[gen]['p'] else [])
                x = dict(seed=46101 + i + (1 if (semilla_mala and b == 'ING_AZA_C' and i == 0) else 0), brazo=b, T=T_,
                         t_corte=(tc if (tc is not None and b == 'ING_SEL_C') else T_), persiste=int(i < pers.get(b, 20)),
                         tam_total=[int(round(k))] * (T_ // 1000 + 1), bloqueados=(bloq if (i == 0 and b == 'ING_F1') else 0),
                         carro=(carro if (carro and b == 'ING_SEL_C') else 'FABRICA_ECO'), aborto=None, guardia=0, genes=NOM, gen_t=[fila],
                         mutables=mut, fuera_mutables=0, tasa_mut=(0.0 if not mut else 0.01), genes_vivos_T=None, causas_2a=[1, 1, 1, 1],
                         K_nac=kn, K_fund=k - kn, fund_2a=f2, fundadores_rep=2 * f2)
                if nomut == b: x['tasa_mut'] = 0.0
                if aborto and b == aborto and i == 2: x.update(aborto='SystemExit: otra cosa', persiste=None)
                if fuera and b == fuera and i == 5: x['fuera_mutables'] = 2
                R.append(x)
        return R[:len(R) - quita]
    casos = [
        ("C y E FUNCIONA", fake(), {'C': 'FUNCIONA', 'E': 'FUNCIONA'}),
        ("C MODESTO sin firma (rango 5)", fake(rk={'ING_SEL_C': {'alpha': 5}}), {'C': 'HAY ALGO MODESTO: LA HERENCIA', 'E': 'FUNCIONA'}),
        ("C MODESTO sin superar la base (K SEL = F1)", fake(K={'ING_SEL_C': 96.0}), {'C': 'HAY ALGO MODESTO: LA SELECCION'}),
        ("P2 cae por la mediana (+1 < +1.5)", fake(K={'ING_SEL_C': 97.0}), {'C': 'HAY ALGO MODESTO: LA SELECCION'}),
        ("P2 cae en el pareado (14/20)", fake(K={'ING_SEL_C': [105.0] * 14 + [90.0] * 6, 'ING_AZA_C': 85.0}), {'C': 'HAY ALGO MODESTO: LA SELECCION'}),
        ("TRAMPA 3: K sube pero K_nac no (comprado con fundadores) -> P2 y P3 caen: NO", fake(Kn={'ING_SEL_C': 5.0}), {'C': 'NO (en'}),
        ("P3 cae (AZA sostiene lo mismo) = NO", fake(K={'ING_AZA_C': 105.0}, Kn={'ING_AZA_C': 25.0}), {'C': 'NO (en'}),
        ("P3 cae solo en K_nac (AZA = SEL en nacidos) y P1 cae -> NO", fake(Kn={'ING_AZA_C': 25.0}, rk={'ING_SEL_C': {'alpha': 5}}), {'C': 'NO (en'}),
        ("E: P4 cae contra AZA (mismos fundadores) -> E NO; C sigue", fake(F2={'ING_AZA_C': 90000}), {'C': 'FUNCIONA', 'E': 'NO (en'}),
        ("E: P4 cae contra la base (SEL necesita mas fundadores) -> E NO", fake(F2={'ING_SEL_C': 126000}), {'E': 'NO (en'}),
        ("guardia: AZA con alpha sobre todas las sombras -> NO EVALUABLE", fake(rk={'ING_AZA_C': {'alpha': 9}}), {'C': 'NO EVALUABLE (el control', 'E': 'NO EVALUABLE (el control'}),
        ("V3: genes fuera en SEL -> NO EVALUABLE", fake(fuera='ING_SEL_C'), {'C': 'NO EVALUABLE (la genetica'}),
        ("V3: AZA sin mutacion -> NO EVALUABLE", fake(nomut='ING_AZA_C'), {'C': 'NO EVALUABLE (la genetica'}),
        ("V1: base 16/20 -> NO EVALUABLE", fake(pers={'ING_F1': 16}), {'C': 'NO EVALUABLE (la base'}),
        ("V2: un brazo con la tabla (FAMB) -> NO EVALUABLE", fake(carro='FAMB_RES0_ECO'), {'C': 'NO EVALUABLE (un brazo'}),
        ("bloqueados -> NO EVALUABLE", fake(bloq=2), {'C': 'NO EVALUABLE (tope'}),
        ("T distinto -> NO EVALUABLE", fake(T_=500000), {'C': 'NO EVALUABLE (serie'}),
        ("t_corte distinto de T (vivero no permanente) -> NO EVALUABLE", fake(tc=60000), {'C': 'NO EVALUABLE (serie'}),
        ("serie incompleta -> NO EVALUABLE", fake(quita=1), {'C': 'NO EVALUABLE (serie'}),
        ("un aborto -> NO EVALUABLE", fake(aborto='ING_SEL_C'), {'C': 'NO EVALUABLE (serie'}),
        ("semillas distintas -> NO EVALUABLE", fake(semilla_mala=True), {'C': 'NO EVALUABLE (serie'}),
        ("un brazo ajeno en la carpeta -> NO EVALUABLE", fake(extra_brazo=True), {'C': 'NO EVALUABLE (serie'}),
    ]
    for nombre, R, esp in casos:
        v, L, d = C.veredicto(R, 20, T)
        ok = all(v[q].startswith(e) for q, e in esp.items())
        chk(f"(L) {nombre}", ok, f"-> C: {v['C'][:60]} | E: {v['E'][:40]}")
    v, L, d = C.veredicto(fake(T_=500000), 20, 500000)
    chk("(L) con T = 500 000 declarada y datos a 500 000: FUNCIONA (la letra no fija 1e6)", v['C'].startswith('FUNCIONA'))
    # (R) banderas
    malas = [['--help'], ['-h'], [], ['--serie'], ['--humo', '--serie'], ['--serie', '--desde', '46101', '--n', '20', '--pool', '6'],
             ['--serie', '--desde=46101', '--n', '20', '--pool', '6', '--T', '1000000'],
             ['--serie', '--des', '46101', '--n', '20', '--pool', '6', '--T', '1000000'],
             ['--serie', '--desde', '46102', '--n', '20', '--pool', '6', '--T', '1000000'],
             ['--serie', '--desde', '46101', '--n', '19', '--pool', '6', '--T', '1000000'],
             ['--serie', '--desde', '46101', '--n', '20', '--pool', '7', '--T', '1000000'],
             ['--serie', '--desde', '46101', '--n', '20', '--pool', '6', '--T', '200000'],
             ['--humo', '--pool', '2'], ['--humo', '--T', '1000000'], ['--humo', '--humo'], ['--lee', 'x', '--pool', '2'],
             ['--serie', '--desde', '45301', '--n', '20', '--pool', '6', '--T', '1000000']]
    n_ab = 0
    for m in malas:
        try: C.parsea(m)
        except C.BanderaMala: n_ab += 1
    chk(f"(R) el parser aborta ante {len(malas)} formas de bandera mala", n_ab == len(malas), f"({n_ab}/{len(malas)})")
    buenas = [['--humo'], ['--serie', '--desde', '46101', '--n', '20', '--pool', '6', '--T', '1000000'],
              ['--serie', '--desde', '46121', '--n', '20', '--pool', '6', '--T', '500000', '--reanuda'], ['--lee', 'datos/x']]
    n_ok = 0
    for m in buenas:
        try: C.parsea(m); n_ok += 1
        except C.BanderaMala: pass
    chk(f"(R) el parser acepta las {len(buenas)} formas buenas", n_ok == len(buenas), f"({n_ok}/{len(buenas)})")
    antes = set(glob.glob(os.path.join(AQUI, 'datos', '**', '*'), recursive=True))
    pr = subprocess.run([sys.executable, os.path.join(AQUI, 'corre_eco_sel_ing.py'), '--serie', '--desde', '46101', '--n', '20', '--pool', '6',
                         '--T', '1000000', '--nada'], capture_output=True, text=True, timeout=300)
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
    open(os.path.join(AQUI, 'identidad_eco_sel_ing_salida.txt'), 'w', encoding='utf-8').write(buf.getvalue())
    sys.exit(0 if ok else 1)
