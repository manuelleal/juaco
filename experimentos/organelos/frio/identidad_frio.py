"""identidad_frio.py — ARNES de F1 ARRANQUE EN FRIO. Un proceso, sin Pool, sin serie. Semillas de PRACTICA 35901-35904.

MISION: llegar a la AGI por este camino.

  (K) construye_frio.py --verifica: BAR0_ECO.py y motor_frio_rapido.py en disco son los construidos (origenes con sha fijado).
  (A) motor_frio_rapido == motor_eco_rapido_fam (el gemelo del arnes 132/132) en TODA la salida de run_solapadas (fisica, eco,
      carro, individuos, estado final del rng del mundo): FAMB_RES0_ECO y FABRICA_ECO, con vivero y en frio (t_corte 1), MUT0 y VIDA.
  (B) ENVOLTORIO: corre_frio.trabajo(RES0_60k) == corre_eco_v12.trabajo(MUT0_T), cada uno con su gemelo, en TODAS las claves de v1.2
      salvo brazo, seg y motor (T 80 000, corte 60 000). Y ninguna clave de v1.2 falta.
  (C) motor_frio_rapido == motor Python (motor_eco) en trabajo() de los 5 brazos (T corto; t_corte de los vivero escalado a 1500),
      en todas las claves salvo seg y motor. Con BAR0 esto prueba que el gemelo permuta EXACTAMENTE como el carro.
  (D) FRIO: 0 refundados y 0 fundadores repuestos en RES0_FRIO, BAR0_FRIO y FAB_FRIO; CONTROL que puede fallar: el mismo carro con
      vivero (t_corte 1500) SI refunda (la medida detecta refundaciones); y t_corte = 1 no refunda aunque haya extinciones de linaje.
  (E) BAR permuta de verdad: carro BAR0 contra RES0 en 200 partos aislados con la MISMA tabla: mismas claves, mismo multiset de R,
      asignacion distinta en >= 1/3; RES0 instala la tabla tal cual (sin neutras). Y la fisica de BAR0_FRIO difiere de RES0_FRIO.
  (Q) ERR-147 (anadido tras el humo): corte de luz simulado a mitad (checkpoint) + --reanuda == la corrida entera (RES0 y BAR0 FRIO).
  (F) nube-9 / ERR-60: trabajo() atrapa un SystemExit del motor: la guardia ERR-60 -> persiste 1, guardia 1, JSON escrito; otro
      aborto -> persiste None; ninguno se propaga. LIM_NAC del motor copiado = 1e9 (ERR-146).
  (V) la letra en entradas sinteticas (cada rama).
  (R) banderas malas abortan (ERR-115); un subproceso con bandera desconocida sale con codigo != 0 y no escribe nada.
Escribe identidad_frio_salida.txt.
"""
import contextlib, copy, glob, io, json, os, subprocess, sys, tempfile, time
import numpy as np

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
R_ = []
J = lambda x: json.dumps(x, sort_keys=True, default=str)
PR = (35901, 35902, 35903, 35904)


def chk(nombre, ok, det=''):
    R_.append(bool(ok)); print(f"  {'OK ' if ok else 'MAL'} {nombre} {det}", flush=True)


def main():
    t0 = time.time()
    import construye_frio as CF
    import corre_frio as F
    V12 = F.V12; CR = F.CR
    print(f"IDENTIDAD F1 FRIO · {time.strftime('%Y-%m-%d %H:%M:%S')} · python {sys.version.split()[0]} · numpy {np.__version__} · shas {F.SHAS()}", flush=True)
    # (K)
    chk("(K) BAR0_ECO.py y motor_frio_rapido.py en disco == los construidos por anclas", CF.main(['--verifica']))
    fijos = {'juaco_eco/corre_eco_v12.py': '1340d268e1fd93d8', 'juaco_eco/corre_eco.py': '47d9cee4d6462116',
             'juaco_eco/motor_eco.py': 'bca3033878b59622', 'juaco_eco/motor_eco_rapido_fam.py': 'd1f16769a53bb51c',
             'juaco_eco/carros/FAMB_RES0_ECO.py': '94ea78589bc2ce24', 'juaco_eco/carros/FABRICA_ECO.py': 'f1163009cb5193a2'}
    sh = F.SHAS()
    chk("(K) los origenes de juaco_eco tienen el sha de la serie de v1.2 (progreso.log de eco_v12_serie_s19701-19720)",
        all(sh.get(k) == v for k, v in fijos.items()), f"{ {k: sh.get(k) for k in fijos} }")
    # (A) motor copiado == gemelo original, salida entera
    import motor_eco_rapido_fam as MO
    import motor_frio_rapido as MF
    t1 = time.time()
    MF.run_solapadas(PR[0], ['FAMB_RES0_ECO'] * 9, T=200, diag=0, mundo_n=9, tope_cuerpos=3000, muestra=1000,
                     eco=CR.eco_cfg('MUT0', 1))   # compila (o lee la cache)
    print(f"  (compilacion / cache de motor_frio_rapido: {time.time() - t1:.0f} s)", flush=True)
    casos = [('FAMB_RES0_ECO', 'MUT0', 3000), ('FAMB_RES0_ECO', 'MUT0', 1), ('FABRICA_ECO', 'MUT0', 1), ('FABRICA_ECO', 'MUT0', 3000),
             ('FAMB_RES0_ECO', 'VIDA', 3000)]
    for carro, gen, tc in casos:
        kw = dict(T=8000, diag=0, mundo_n=90, tope_cuerpos=3000, muestra=1000)
        a = MO.run_solapadas(PR[0], [carro] * 90, eco=CR.eco_cfg(gen, tc), **kw)
        b = MF.run_solapadas(PR[0], [carro] * 90, eco=CR.eco_cfg(gen, tc), **kw)
        chk(f"(A) {carro} {gen} t_corte {tc}: motor_frio_rapido == motor_eco_rapido_fam en TODA la salida (T 8000, w90)", J(a) == J(b),
            f"(nacidos {a['eco']['n_nac']}, refundados {a['eco']['n_refund']}, t_ext {a['eco']['t_ext']}, max_vivos {a['pista']['max_vivos']})")
    # (B) envoltorio == corre_eco_v12 en el brazo equivalente
    V12.usa_gemelo()
    x = V12.trabajo((PR[1], 'MUT0_T', 80000, 60000, 70000, tempfile.mkdtemp(prefix='frio_B_v12_'), 0, 0, False))
    F.usa_gemelo()
    y = F.trabajo((PR[1], 'RES0_60k', 80000, 60000, 70000, tempfile.mkdtemp(prefix='frio_B_f1_'), False))
    fuera = {'seg', 'motor', 'brazo'}
    dist = [k for k in x if k not in fuera and J(x[k]) != J(y.get(k))]
    falta = [k for k in x if k not in y]
    chk("(B) corre_frio.trabajo(RES0_60k) == corre_eco_v12.trabajo(MUT0_T) en todas las claves de v1.2 salvo brazo, seg y motor "
        "(T 80 000, corte 60 000, cada uno con su gemelo)", not dist and not falta,
        f"(persiste {x['persiste']}, vivos_T {x['vivos_T']}, n_nac {x['n_nac']}, refundados {x['n_refund']}, r0_post {x['r0_post']}; "
        f"distintas {dist}, faltan {falta}; {x['seg']} s contra {y['seg']} s)")
    chk("(B) el brazo equivalente: RES0_60k = (MUT0, FAMB_RES0_ECO, 60000) y MUT0_T = (MUT0, FAMB_RES0_ECO) con el corte de v1.2",
        F.BRAZOS['RES0_60k'] == ('MUT0', 'FAMB_RES0_ECO', 60000) and V12.BRAZOS['MUT0_T'] == ('MUT0', 'FAMB_RES0_ECO')
        and V12.V12['t_corte'] == 60000 and F.FRIO['T'] == V12.V12['T'])
    # (C) gemelo copiado == Python en los 5 brazos; (D) frio limpio
    TC = {'RES0_FRIO': 1, 'RES0_10k': 700, 'RES0_60k': 1500, 'BAR0_FRIO': 1, 'FAB_FRIO': 1}
    RC = {}
    for b in F.BRAZOS:
        CR.ME = F.ME_PY
        p = F.trabajo((PR[2], b, 3000, TC[b], 2500, tempfile.mkdtemp(prefix='frio_C_py_'), False))
        F.usa_gemelo()
        g = F.trabajo((PR[2], b, 3000, TC[b], 2500, tempfile.mkdtemp(prefix='frio_C_g_'), False))
        dist = [k for k in p if k not in ('seg', 'motor', 'lim_nac') and J(p[k]) != J(g.get(k))]
        chk(f"(C) {b} (t_corte {TC[b]}): motor_frio_rapido == motor Python en trabajo() (T 3000, w90)", not dist and p['motor'].startswith('PYTHON'),
            f"(n_nac {p['n_nac']}, refundados {p['n_refund']}, fundadores_rep {p['fundadores_rep']}, vivos_T {p['vivos_T']}; distintas {dist}; "
            f"{p['seg']} s contra {g['seg']} s)")
        RC[b] = g
    for b in F.FRIOS:
        g = RC[b]
        chk(f"(D) {b}: 0 refundados y 0 fundadores repuestos (t_fund vacio)", g['n_refund'] == 0 and g['fundadores_rep'] == 0 and g['t_fund_primero'] is None,
            f"(refundados {g['n_refund']}, fundadores_rep {g['fundadores_rep']}, vivos cada 1000 {g['vivos_1k']})")
    chk("(D) CONTROL que puede fallar: con vivero (RES0_60k, t_corte 1500; RES0_10k, 700) SI hay refundados y fundadores repuestos",
        RC['RES0_60k']['n_refund'] > 0 and RC['RES0_60k']['fundadores_rep'] > 0 and RC['RES0_10k']['n_refund'] > 0,
        f"(60k: {RC['RES0_60k']['n_refund']} / {RC['RES0_60k']['fundadores_rep']}; 10k: {RC['RES0_10k']['n_refund']})")
    # frio con extinciones de linaje: T mas largo, gemelo
    F.usa_gemelo()
    gl = F.trabajo((PR[3], 'RES0_FRIO', 20000, 1, 15000, tempfile.mkdtemp(prefix='frio_D_'), False))
    lin_vivos = gl['gen_t'][-1][2] if gl['gen_t'] else None
    chk("(D) t_corte = 1 en 20 000 pasos: linajes se extinguen (quedan < 90) y aun asi 0 refundados",
        gl['n_refund'] == 0 and gl['fundadores_rep'] == 0 and (gl['t_ext'] is not None or (lin_vivos is not None and lin_vivos < 90)),
        f"(linajes vivos al final {lin_vivos}, t_ext {gl['t_ext']}, vivos_T {gl['vivos_T']}, n_nac {gl['n_nac']}, r0_nac {gl['r0_nac']} n {gl['n_coh_nac']})")
    chk("(D) en t_corte = 1 la foto del corte es de t = 1 (90 fundadores, nadie mas) y la seleccion no se mide (sel_corte None)",
        gl['corte'] is not None and gl['corte']['t'] == 1 and gl['corte']['vivos'] == 90 and gl['sel_corte'] is None,
        f"(corte t {gl['corte'] and gl['corte']['t']}, vivos {gl['corte'] and gl['corte']['vivos']})")
    # (E) BAR permuta de verdad
    import pista2 as P
    MEp = F.ME_PY
    CFb = P.cfg_fabrica(); kwb = CFb['kw']
    G0 = MEp.genoma0(P.cfg_fabrica())
    import importlib.util

    def carga(p, nom):
        spec = importlib.util.spec_from_file_location(nom, p); m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m
    mR = carga(os.path.join(F.ECO, 'carros', 'FAMB_RES0_ECO.py'), 'res0_E'); mB = carga(os.path.join(AQUI, 'carros', 'BAR0_ECO.py'), 'bar0_E')

    def ctx(r):
        d = dict(id='x', indice=0, n_linajes=90, T=1000, L=3600, PAT={k: v.copy() for k, v in CFb['PAT'].items()}, rng=r, dote=kwb['dote'],
                 rep_umbral=kwb['rep_umbral'], costo=kwb['costo'], costo_a=kwb['costo_a'], rep_X=kwb['rep_X'], cupo=P.CUPO, ancho=P.ANCHO,
                 fabrica=P.cfg_fabrica())
        return MEp.ctx_genoma(d, G0)
    PAT = CFb['PAT']
    tabla = [[list(map(float, PAT['A'])), 1.0, 0], [list(map(float, PAT['B'])), -3.0, 0], [list(map(float, PAT['C'])), 0.0, 0],
             [list(map(float, PAT['D'])), 1.0, 0], [list(map(float, PAT['B'])), 1.0, 1], [list(map(float, PAT['D'])), -3.0, 1],
             [list(map(float, PAT['A'])), 0.0, 1]]
    sin0 = [e for e in tabla if e[1] != 0.0]
    dif = 0; claves_ok = multiset_ok = res_ok = True; N = 200
    for k in range(1, N + 1):
        cs = []
        for m in (mR, mB):
            c = m.crea(ctx(np.random.default_rng([PR[0], 0, 12, k])))
            c.nace(dict(t=5, k=k, fundador=False, memoria=copy.deepcopy(tabla), rng_hijo=np.random.default_rng([PR[0], 0, 13, k]), padre='p'))
            cs.append(c._nodo[:len(sin0)])
        a, b = cs
        claves_ok &= [(e[0], e[2]) for e in a] == [(e[0], e[2]) for e in b]
        multiset_ok &= sorted(e[1] for e in a) == sorted(e[1] for e in b)
        res_ok &= [[e[0], e[1], e[2]] for e in a] == sin0
        dif += int([e[1] for e in a] != [e[1] for e in b])
    chk("(E) BAR0 contra RES0 en 200 partos aislados: mismas claves y mismo multiset de R, sin neutras; RES0 instala la tabla tal cual",
        claves_ok and multiset_ok and res_ok, f"(claves {claves_ok}, multiset {multiset_ok}, RES0 = tabla sin neutras {res_ok})")
    chk("(E) BAR0 permuta de verdad: la asignacion de R difiere de RES0 en >= 1/3 de los partos", dif >= N // 3, f"({dif}/{N})")
    chk("(E) la fisica de BAR0_FRIO difiere de la de RES0_FRIO (misma semilla, T 3000)",
        J(RC['BAR0_FRIO']['gen_t']) != J(RC['RES0_FRIO']['gen_t']) or RC['BAR0_FRIO']['n_nac'] != RC['RES0_FRIO']['n_nac'] or
        J(RC['BAR0_FRIO']['tam_total']) != J(RC['RES0_FRIO']['tam_total']),
        f"(n_nac RES0 {RC['RES0_FRIO']['n_nac']} · BAR0 {RC['BAR0_FRIO']['n_nac']} · FAB {RC['FAB_FRIO']['n_nac']})")
    # (Q) ERR-147 (anadido tras el humo; no toca runner ni letra): corte de luz simulado + --reanuda == la corrida entera
    F.usa_gemelo()
    for bq in ('RES0_FRIO', 'BAR0_FRIO'):
        # la corrida debe LLEGAR al corte: primera semilla de practica en la que el brazo sigue vivo en t = 30 000 (ERR-147: en la
        # primera version BAR0_FRIO s35904 se extinguia antes del corte y el caso no probaba nada)
        for sq in PR:
            entera = F.trabajo((sq, bq, 40000, 1, 35000, tempfile.mkdtemp(prefix='frio_Q_a_'), False))
            if entera['t_ext'] is None or entera['t_ext'] > 30000: break
        tq = tempfile.mkdtemp(prefix='frio_Q_b_')
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
            F.trabajo((sq, bq, 40000, 1, 35000, tq, False)); cortado = False
        except KeyboardInterrupt:
            cortado = True
        finally:
            CR.ME.run_solapadas = orig_q
        hay_ck = os.path.exists(os.path.join(tq, 'ckpt', f'{bq}_s{sq}.pkl')) and not os.path.exists(os.path.join(tq, f'{bq}_s{sq}.json'))
        re = F.trabajo((sq, bq, 40000, 1, 35000, tq, True))
        dist = [k for k in entera if k not in ('seg',) and J(entera[k]) != J(re.get(k))]
        chk(f"(Q) {bq}: corte en t = 30 000 + --reanuda == la corrida entera (T 40 000; cohorte F1 [1e4, 2e4] incluida)", cortado and hay_ck and not dist,
            f"(semilla {sq}, cortado {cortado}, checkpoint {hay_ck}, distintas {dist}, r0_nac {entera['r0_nac']} n {entera['n_coh_nac']}, vivos_T {entera['vivos_T']})")
    # (F) nube-9
    F.usa_gemelo()
    chk("(F) ERR-146: el limite de cuerpos por linaje del motor copiado es 1e9 (el del gemelo original, 100 000)",
        MF.LIM_NAC == 1_000_000_000 and F._lim_nac() == 1_000_000_000)
    orig = CR.ME.run_solapadas
    try:
        tmp = tempfile.mkdtemp(prefix='frio_F_')

        def guardia(*a, **k): raise SystemExit('PISTA2: mas de 100000 cuerpos en un linaje: la semilla colisionaria (ERR-60)')

        def otro(*a, **k): raise SystemExit('motor_eco_rapido_fam: mas de 256 entradas vigentes de rechazo en un cuerpo (sube RC)')
        CR.ME.run_solapadas = guardia
        try: r1 = F.trabajo((PR[0], 'RES0_FRIO', 3000, 1, 2500, tmp, False)); ok1 = True
        except BaseException: r1 = {}; ok1 = False
        CR.ME.run_solapadas = otro
        try: r2 = F.trabajo((PR[0], 'BAR0_FRIO', 3000, 1, 2500, tmp, False)); ok2 = True
        except BaseException: r2 = {}; ok2 = False
    finally:
        CR.ME.run_solapadas = orig
    chk("(F) la guardia ERR-60 no se propaga: persiste 1, guardia 1, JSON escrito",
        ok1 and r1.get('persiste') == 1 and r1.get('guardia') == 1 and os.path.exists(os.path.join(tmp, 'RES0_FRIO_s35901.json')),
        f"(aborto {r1.get('aborto')!r})")
    chk("(F) otro aborto no se propaga: persiste None, guardia 0, marcado", ok2 and r2.get('persiste') is None and r2.get('guardia') == 0 and r2.get('aborto'))
    # (V) la letra
    def fake(p, r0=0.99, T=F.FRIO['T'], sucio=0, bloq=0, guard=None, aborto=None, quita=0, tc=None):
        R = []
        for i in range(20):
            for b, (gen, carro, tcb) in F.BRAZOS.items():
                pr = int(i < p[b])
                x = dict(seed=35001 + i, brazo=b, T=T, t_corte=(tcb if tc is None or b != 'RES0_FRIO' else tc), persiste=pr,
                         r0_nac=(r0 if pr else 0.4), vivos_T=30 * pr, t_ext=(None if pr else 5000), bloqueados=(bloq if (i == 0 and b == 'FAB_FRIO') else 0),
                         n_refund=(0 if b in F.FRIOS else 900), fundadores_rep=(0 if b in F.FRIOS else 900), guardia=0, aborto=None)
                if sucio and b == 'RES0_FRIO' and i == 3: x['n_refund'] = 1
                if guard and b == guard[0] and i == guard[1]: x.update(persiste=1, guardia=1, aborto='SystemExit: ... (ERR-60)', vivos_T=None, t_ext=None)
                if aborto and b == aborto[0] and i == aborto[1]: x.update(persiste=None, guardia=0, aborto='SystemExit: otra cosa')
                R.append(x)
        return R[:len(R) - quita]
    base = {'RES0_FRIO': 16, 'RES0_10k': 18, 'RES0_60k': 19, 'BAR0_FRIO': 3, 'FAB_FRIO': 1}
    casos = [
        ("FUNCIONA", fake(base), 'FUNCIONA'),
        ("FUNCIONA con la guardia ERR-60 contando como persiste (14 + 1 guardia = 15)", fake(dict(base, RES0_FRIO=14), guard=('RES0_FRIO', 17)), 'FUNCIONA'),
        ("MODESTO (P1 cae: 12/20; RES0 - BAR0 = 9, RES0 - FAB = 11)", fake(dict(base, RES0_FRIO=12)), 'HAY ALGO MODESTO'),
        ("MODESTO (P4 cae: BAR0 7/20; 16 - 7 = 9)", fake(dict(base, BAR0_FRIO=7)), 'HAY ALGO MODESTO'),
        ("MODESTO (P2 cae: R0 0.85)", fake(base, r0=0.85), 'HAY ALGO MODESTO'),
        ("NO (P4 cae y RES0 - BAR0 = 5)", fake(dict(base, BAR0_FRIO=11)), 'NO (en'),
        ("NO (RES0_FRIO 7/20)", fake(dict(base, RES0_FRIO=7)), 'NO (en'),
        ("NO (P3 cae: FAB 11/20, RES0 - FAB = 5)", fake(dict(base, FAB_FRIO=11)), 'NO (en'),
        ("NO EVALUABLE (ancla 16/20)", fake(dict(base, RES0_60k=16)), 'NO EVALUABLE (el ancla'),
        ("NO EVALUABLE (un frio con 1 refundado)", fake(base, sucio=1), 'NO EVALUABLE (un brazo FRIO'),
        ("NO EVALUABLE (bloqueados)", fake(base, bloq=2), 'NO EVALUABLE (tope'),
        ("NO EVALUABLE (T distinto)", fake(base, T=200000), 'NO EVALUABLE (serie'),
        ("NO EVALUABLE (incompleta)", fake(base, quita=1), 'NO EVALUABLE (serie'),
        ("NO EVALUABLE (aborto que no es la guardia)", fake(base, aborto=('BAR0_FRIO', 2)), 'NO EVALUABLE (serie'),
        ("NO EVALUABLE (t_corte de RES0_FRIO distinto de 1)", fake(base, tc=60000), 'NO EVALUABLE (serie'),
    ]
    for nombre, R, esp in casos:
        v, L, d = F.veredicto(R, 20)
        chk(f"(V) {nombre}", v.startswith(esp), f"-> {v}")
    # (R) banderas
    malas = [['--help'], ['-h'], [], ['--serie'], ['--humo', '--serie'], ['--serie', '--desde', '35001', '--n', '20'],
             ['--serie', '--desde=35001', '--n', '20', '--pool', '6'], ['--serie', '--des', '35001', '--n', '20', '--pool', '6'],
             ['--serie', '--desde', '35002', '--n', '20', '--pool', '6'], ['--serie', '--desde', '35001', '--n', '19', '--pool', '6'],
             ['--serie', '--desde', '35001', '--n', '20', '--pool', '7'], ['--humo', '--pool', '2'], ['--humo', '--humo'],
             ['--lee', 'x', '--pool', '2'], ['--gemelo', '--humo']]
    n_ab = 0
    for m in malas:
        try: F.parsea(m)
        except F.BanderaMala: n_ab += 1
    chk(f"(R) el parser aborta ante {len(malas)} formas de bandera mala", n_ab == len(malas), f"({n_ab}/{len(malas)})")
    buenas = [['--humo'], ['--serie', '--desde', '35001', '--n', '20', '--pool', '6'], ['--serie', '--desde', '35021', '--n', '20', '--pool', '6', '--reanuda'],
              ['--lee', 'datos/x']]
    n_ok = 0
    for m in buenas:
        try: F.parsea(m); n_ok += 1
        except F.BanderaMala: pass
    chk(f"(R) el parser acepta las {len(buenas)} formas buenas", n_ok == len(buenas), f"({n_ok}/{len(buenas)})")
    antes = set(glob.glob(os.path.join(AQUI, 'datos', '**', '*'), recursive=True))
    pr = subprocess.run([sys.executable, os.path.join(AQUI, 'corre_frio.py'), '--serie', '--desde', '35001', '--n', '20', '--pool', '6', '--nada'],
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
    open(os.path.join(AQUI, 'identidad_frio_salida.txt'), 'w', encoding='utf-8').write(buf.getvalue())
    sys.exit(0 if ok else 1)
