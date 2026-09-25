"""identidad_gramatica.py — ARNES de ORGANELOS / GRAMATICA. Un proceso, sin Pool. Opus A, 24-sep-2026.

MISION: llegar a la AGI por este camino.

  (C)  construye_gramatica.py --verifica: los dos archivos son los que salen de los origenes (sha fijado).
  (I1) motor_gramatica + FAMB_ORG_ECO, sin gramatica == motor_eco2 + FAMB_ORG_ECO (VIDA con los 20 genes mutables, y AZAR).
  (I2) motor_eco2 + FAMB_GRAM_ECO (ctx sin gramatica) == motor_eco2 + FAMB_ORG_ECO (VIDA, 20 genes mutables: los organos numericos prenden).
  (I3) LA PEDIDA: motor_gramatica + FAMB_GRAM_ECO con la gramatica FIJA en ensena (1 slot) == motor_eco2 + FAMB_ORG_ECO con ensena
       prendido (1.2) en todos; brazos VIDA, AZAR y MUT0 (genes de organo fuera de la mutacion en los dos).
  (I4) gramatica [nacer/sin0/hijo/copiar] == motor_eco2 con ensena y filtra0 prendidos.
  (I5) gramatica vacia y gramatica con un slot silencioso == motor_eco2 con ensena apagado.
  (I6) motor_eco3 + FAMB_ORG_ECO == motor_eco2 + FAMB_ORG_ECO sin mutacion (organos apagados): el 'motor_eco3' del encargo.
  (I7) errores de copia de la gramatica PRENDIDOS pero con el alfabeto de cuando = {nunca}: la fisica == (I5) y hay errores (> 0):
       el rng de la gramatica no toca ningun rng del mundo.
  (I8) checkpoint: VIDA con gramatica mutando, corrida entera == reanudada desde el checkpoint (incluida la salida de la gramatica).
  (I9) runner: trabajo() escribe su JSON; con el motor lanzando la guardia de ERR-60 (nube-9) escribe el JSON con 'abortado' y no lanza.
  (I10) errores de copia (unidad): consumo de numeros fijo; duplicacion en tandem con origen 1; borrado; cambio a OTRO valor del alfabeto;
       tope respetado.
  (I11) conducta: los tres disenados son distintos entre si; el origen y un slot duplicado identico no cambian la conducta.
  (P)  ARNES POR PIEZA (correccion 3): cada opcion de cada campo, en un monocultivo FIJO de w30 (T 8 000, corte 6 000), cambia la
       trayectoria respecto de su base en al menos un contexto; las inertes se DECLARAN (no entran al alfabeto de la serie).
Escribe identidad_gramatica_salida.txt (y la tabla por pieza en datos/pieza_gramatica.json).
"""
import contextlib, io, json, os, sys, tempfile, time
import numpy as np

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(AQUI)))
ECO = os.path.join(RAIZ, 'experimentos', 'juaco_eco')
for _d in (AQUI, ECO, os.path.join(RAIZ, 'experimentos', 'generaciones')):
    if _d not in sys.path: sys.path.insert(0, _d)
R_ = []; OUT = []


def pr(s):
    print(s, flush=True); OUT.append(s)


def chk(nombre, ok, det=''):
    R_.append(bool(ok)); pr(f"  {'OK ' if ok else 'MAL'} {nombre} {det}")


J = lambda x: json.dumps(x, sort_keys=True, default=str)
SEM = 21002; T_ = 10000; TC = 8000


def main():
    import subprocess, hashlib
    import motor_eco2 as ME2, motor_eco3 as ME3, motor_gramatica as MG, gramatica_def as GD, pista2 as P
    import corre_gramatica as CG, conducta as C
    h = lambda p: hashlib.sha256(open(p, 'rb').read()).hexdigest()[:16]
    t00 = time.time()
    pr(f"IDENTIDAD ORGANELOS/GRAMATICA · {time.strftime('%Y-%m-%d %H:%M:%S')} · python {sys.version.split()[0]} · numpy {np.__version__}")
    pr(f"  origenes: motor_eco2 {h(os.path.join(ECO, 'motor_eco2.py'))} · motor_eco3 {h(os.path.join(ECO, 'motor_eco3.py'))} · "
       f"FAMB_ORG_ECO {h(os.path.join(ECO, 'carros', 'FAMB_ORG_ECO.py'))} · shas {CG.SHAS()}")
    v = subprocess.run([sys.executable, os.path.join(AQUI, 'construye_gramatica.py'), '--verifica'], capture_output=True, text=True)
    chk("(C) construye --verifica", v.returncode == 0 and 'OK' in v.stdout, v.stdout.strip())

    co = ME2.carga_eco('FAMB_ORG_ECO'); cg = MG.carga_eco('FAMB_GRAM_ECO')
    G0 = ME2.genoma0(P.cfg_fabrica()); IE = ME2.NOMBRES.index('ensena'); IF = ME2.NOMBRES.index('filtra0')
    MUT18 = tuple(x for x in ME2.NOMBRES if x not in ('ensena', 'filtra0'))
    base = dict(refunda=1, t_corte=TC, p_mut=0.05, sigma=0.15, banco=200, n_sombra=8, cada_gen=2000)

    def gen(e=0.9, f=0.9):
        g = G0.copy(); g[IE] = e; g[IF] = f; return g

    def corre(motor, mod, eco, T=T_, seed=SEM):
        t0 = time.time()
        r = motor.run_solapadas(seed, [('FAMB_ORG_ECO', mod)] * 30, T=T, diag=0, mundo_n=30, tope_cuerpos=3000, muestra=1000, eco=eco)
        r['_seg'] = round(time.time() - t0, 1); return r

    def igual(a, b, claves=('linajes', 'pizarra_log', 'pista', 'eco')):
        return [k for k in claves if J(a[k]) != J(b[k])]

    # (I1)
    for don in ('padre', 'azar'):
        a = corre(ME2, co, dict(base, donante=don)); b = corre(MG, co, dict(base, donante=don))
        d = igual(a, b); chk(f"(I1) motor_gramatica sin gramatica == motor_eco2 ({don}, 20 genes mutables)", not d,
                             f"(distintas {d}; nacidos {a['eco']['n_nac']}, fundadores del banco {a['eco']['n_banco']}, {a['_seg']}+{b['_seg']} s)")
        if don == 'padre': A1 = a
    # (I2)
    b = corre(ME2, cg, dict(base)); d = igual(A1, b)
    on = sum(1 for v_ in A1['eco']['vivos_final'] if v_[4 + IE] >= 1.0)
    chk("(I2) motor_eco2 + FAMB_GRAM_ECO (ctx sin gramatica) == FAMB_ORG_ECO", not d, f"(distintas {d}; vivos con ensena numerico prendido {on})")
    e2b = dict(base, genoma=gen(1.2, 0.9))   # ERR-120: que la rama de los organos NUMERICOS del carro se ejercite (nacen prendidos y mutan)
    a = corre(ME2, co, e2b); b = corre(ME2, cg, e2b); d = igual(a, b)
    on = sum(1 for v_ in a['eco']['vivos_final'] if v_[4 + IE] >= 1.0); onf = sum(1 for v_ in a['eco']['vivos_final'] if v_[4 + IF] >= 1.0)
    chk("(I2b) idem con ensena numerico nacido PRENDIDO (1.2) y los 20 genes mutables", not d and on > 0,
        f"(distintas {d}; vivos con ensena {on}, con filtra0 {onf} de {len(a['eco']['vivos_final'])})")
    # (I3) la pedida
    for brazo, don, pm in (('VIDA', 'padre', 0.05), ('AZAR', 'azar', 0.05), ('MUT0', 'padre', 0.0)):
        e2 = dict(base, donante=don, p_mut=pm, mutables=MUT18, genoma=gen(1.2))
        a = corre(ME2, co, e2); b = corre(MG, cg, dict(e2, gramatica=[GD.ENSENA] * 30))
        d = igual(a, b)
        chk(f"(I3) gramatica FIJA [nacer/todo/hijo/copiar] == motor_eco2 + FAMB_ORG_ECO con ensena prendido · {brazo}", not d,
            f"(distintas {d}; nacidos {a['eco']['n_nac']}, max vivos {a['pista']['max_vivos']}, entregas motor {b['gram']['entregas']})")
        if brazo == 'VIDA': A3 = a
    # (I4)
    e2 = dict(base, mutables=MUT18, genoma=gen(1.2, 1.2))
    a = corre(ME2, co, e2); b = corre(MG, cg, dict(e2, gramatica=[GD.FILTRA0] * 30))
    # 1a corrida del arnes (12:51): MAL por comparar la TELEMETRIA del carro: n10.dado cuenta lo dado ANTES del filtro del hijo (FAMB_ORG_ECO)
    # o DESPUES del filtro del emisor (gramatica). Se compara la FISICA (ERR-96: linajes sin d['carro'], pista, eco) y se declara la telemetria.
    fis = lambda r: [{k: v for k, v in d_.items() if k != 'carro'} for d_ in r['linajes']]
    d = [k for k, ok in (('fisica', J(fis(a)) == J(fis(b))), ('pista', J(a['pista']) == J(b['pista'])), ('eco', J(a['eco']) == J(b['eco'])),
                         ('pizarra_log', J(a['pizarra_log']) == J(b['pizarra_log']))) if not ok]
    tel = sorted(set(k for x, y in zip(a['linajes'], b['linajes']) for k in x['carro'] if J(x['carro'][k]) != J(y['carro'].get(k))))
    chk("(I4) gramatica [nacer/sin0/hijo/copiar] == motor_eco2 con ensena y filtra0 prendidos (FISICA)", not d and set(tel) <= {'n10'}
        and J(fis(a)) != J(fis(A3)), f"(distintas {d}; telemetria distinta {tel} = n10.dado, declarado; distinta de ensena solo: {J(fis(a)) != J(fis(A3))})")
    # (I5)
    e2 = dict(base, mutables=MUT18, genoma=gen(0.9))
    a5 = corre(ME2, co, e2)
    b = corre(MG, cg, dict(e2, gramatica=[()] * 30)); c = corre(MG, cg, dict(e2, gramatica=[((0, 0, 0, 0, 0),)] * 30))
    d = igual(a5, b) + igual(a5, c)
    chk("(I5) gramatica vacia y un slot silencioso == motor_eco2 con ensena apagado", not d and J(a5['linajes']) != J(A3['linajes']), f"(distintas {d})")
    # (I6)
    e0 = dict(base, p_mut=0.0)
    a = corre(ME2, co, e0); b = corre(ME3, ME3.carga_eco('FAMB_ORG_ECO'), e0); d = igual(a, b, ('linajes', 'pizarra_log', 'pista'))
    chk("(I6) motor_eco3 + FAMB_ORG_ECO == motor_eco2 + FAMB_ORG_ECO (sin mutacion; organos apagados)", not d, f"(distintas {d})")
    # (I7)
    alf0 = ((0,), (0, 1, 2, 3, 4), (0, 1, 2), (0, 1, 2))
    b = corre(MG, cg, dict(e2, gramatica=[((0, 1, 2, 1, 0),)] * 30, g_pcampo=0.3, g_pdup=0.3, g_pdel=0.1, g_alfabeto=alf0))
    d = igual(a5, b); nsl = sorted(set(len(g) for g in b['gram']['banco_final_gr']))
    chk("(I7) errores de copia prendidos con cuando = {nunca}: la fisica == ensena apagado; hubo errores", not d and b['gram']['g_nmut'] > 0,
        f"(distintas {d}; errores {b['gram']['g_nmut']}; slots en el banco {nsl})")
    # (I8) checkpoint
    tmp = tempfile.mkdtemp(); cps = {}
    ev = CG.eco_de('VIDA', SEM, 10000)
    ev['g_pcampo'] = 0.2; ev['g_pdup'] = 0.1; ev['g_pdel'] = 0.05   # que haya mucho que guardar
    a = MG.run_solapadas(SEM, ['FAMB_GRAM_ECO'] * 30, T=12000, diag=0, mundo_n=30, tope_cuerpos=3000, muestra=1000,
                         eco=dict(ev, ckpt_cada=6000, ckpt_fn=lambda t, blob: cps.__setitem__(t, blob)))
    b = MG.run_solapadas(SEM, ['FAMB_GRAM_ECO'] * 30, T=12000, diag=0, mundo_n=30, tope_cuerpos=3000, muestra=1000,
                         eco=dict(ev, ckpt_cada=6000, ckpt_fn=lambda t, blob: None, estado=cps[6000]))
    d = igual(a, b, ('linajes', 'pizarra_log', 'pista', 'eco', 'gram'))
    act = float(np.mean([len(GD.activos(g)) > 0 for g in a['gram']['banco_final_gr']]))
    chk("(I8) checkpoint: VIDA con la gramatica mutando, entera == reanudada en t = 6 000", not d,
        f"(distintas {d}; errores {a['gram']['g_nmut']}; banco con organo activo {act:.2f}; entregas {a['gram']['entregas']})")
    # (I9) runner y nube-9
    x = CG.trabajo((SEM, 'VIDA', 3000, 2000, 500, tmp, False)); fj = os.path.join(tmp, f"VIDA_s{SEM}.json")
    chk("(I9a) trabajo() escribe su JSON con las medidas de la gramatica", os.path.exists(fj) and x['abortado'] is None and
        len(x['final_banco_gr']) > 0 and len(x['final_banco_gs'][0]) == 8 and 'r0_post' in x, f"({x['seg']} s)")
    orig = MG.run_solapadas

    def falla(*a_, **k_): raise SystemExit('PISTA2: mas de 100000 cuerpos en un linaje: la semilla colisionaria (ERR-60)')
    MG.run_solapadas = falla
    try:
        x = CG.trabajo((SEM + 1, 'VIDA', 3000, 2000, 500, tmp, False)); ok9 = True
    except BaseException: ok9 = False; x = {}
    finally: MG.run_solapadas = orig
    chk("(I9b) nube-9: la guardia de ERR-60 dentro de trabajo() queda en el JSON ('abortado') y no lanza", ok9 and 'ERR-60' in (x.get('abortado') or '')
        and os.path.exists(os.path.join(tmp, f"VIDA_s{SEM + 1}.json")), f"({x.get('abortado')})")
    # (I10) errores de copia
    A = GD.ALFABETO_TODO; g1 = ((1, 0, 0, 0, 0), (2, 1, 2, 1, 0))
    r1 = np.random.default_rng(5); r2 = np.random.default_rng(5)
    GD.muta_gram(g1, r1, 0.0, 0.0, 0.0, 4, A); GD.muta_gram(((3, 3, 1, 2, 0),), r2, 1.0, 1.0, 1.0, 4, A)
    cons = r1.random() == r2.random()
    gd, _ = GD.muta_gram(g1, np.random.default_rng(1), 0.0, 1.0, 0.0, 4, A)
    dup = len(gd) == 3 and any(s[4] == 1 for s in gd) and [s[:4] for s in gd].count(gd[[s[4] for s in gd].index(1)][:4]) == 2 \
        and gd[[s[4] for s in gd].index(1) - 1][:4] == gd[[s[4] for s in gd].index(1)][:4]
    gb, _ = GD.muta_gram(g1, np.random.default_rng(1), 0.0, 0.0, 1.0, 4, A)
    gc, nc = GD.muta_gram(g1, np.random.default_rng(1), 1.0, 0.0, 0.0, 4, ((0, 1, 2, 3), (0, 1, 2, 3, 4), (0, 1, 2), (0, 1, 2)))
    camb = nc == 8 and all(gc[i][f] != g1[i][f] for i in range(2) for f in range(4)) and all(s[3] != 3 for s in gc)
    gt, _ = GD.muta_gram(((1, 0, 0, 0, 0),) * 4, np.random.default_rng(1), 0.0, 1.0, 0.0, 4, A)
    chk("(I10) errores de copia: consumo fijo, duplicacion en tandem (origen 1), borrado, cambio a OTRO valor del alfabeto, tope",
        cons and dup and len(gb) == 1 and camb and len(gt) == 4, f"(dup {GD.texto(gd)}; borrado {GD.texto(gb)}; campos {GD.texto(gc)})")
    # (I11) conducta
    dd = [C.distancia(C.firma(GD.DISENADOS[a_]), C.firma(GD.DISENADOS[b_])) for a_, b_ in (('nulo', 'ensena'), ('nulo', 'filtra0'), ('ensena', 'filtra0'))]
    chk("(I11) conducta: nulo, ensena y filtra0 distintos (> TOL); origen y duplicado identico no cambian la conducta",
        min(dd) > C.TOL and C.igual(((1, 0, 0, 0, 1),), GD.ENSENA) and C.igual(((1, 0, 0, 0, 0), (1, 0, 0, 0, 1)), GD.ENSENA)
        and C.clase_disenada(((1, 0, 0, 0, 0), (0, 2, 2, 2, 1))) == 'ensena', f"(distancias {[round(x, 3) for x in dd]})")
    # (V) la letra en entradas sinteticas
    def sint(gV, gA=((0, 0, 0, 0, 0),), pers=1):
        R = []
        for b_ in CG.BRAZOS_SERIE:
            for s_ in range(20):
                g_ = gV if b_ == 'VIDA' else (gA if b_ == 'AZAR' else (((0, 0, 0, 0, 0),) if b_ == 'MUT0' else CG.gram_de(b_)))
                R.append(dict(seed=s_, brazo=b_, abortado=None, persiste=pers, bloqueados=0, r0_post=0.9, entregas={},
                              final_banco_gr=[[list(z) for z in g_]] * 10, final_banco_gs=[[[[0, 0, 0, 0, 0]]] * 8] * 10))
        return R
    TOPs = [(1, 1, 0, 0)]
    v1 = CG.veredicto(sint(((1, 1, 0, 0, 0),)), TOPs)[0]; v2 = CG.veredicto(sint(GD.ENSENA), [(1, 0, 0, 0)])[0]
    v3 = CG.veredicto(sint(((0, 0, 0, 0, 0),)), TOPs)[0]; v4 = CG.veredicto(sint(((1, 1, 0, 0, 0),), gA=((1, 1, 0, 0, 0),)), TOPs)[0]
    v5 = CG.veredicto(sint(((1, 1, 0, 0, 0), (2, 1, 2, 0, 1))), TOPs)[0]
    chk("(V) la letra: nuevo en TOP -> COMBINA; disenado en TOP -> MODESTO; silencioso -> NO; AZAR igual -> guardia; duplicado divergente -> CREA",
        v1.startswith('FUNCIONA — LA SELECCION COMBINA') and v2.startswith('HAY ALGO MODESTO') and v3 == 'NO' and 'NO EVALUABLE' in v4
        and 'CREA' in v5, f"({v1[:40]} | {v2[:20]} | {v3} | {v4[:30]} | {v5[:45]})")
    # (R) banderas
    rr = [subprocess.run([sys.executable, os.path.join(AQUI, 'corre_gramatica.py')] + x, capture_output=True, text=True).returncode
          for x in (['--humo', '--pool', '2'], ['--serie', '--ventana', 'serie', '--pool', '3'], ['--fuerza'], ['--hum'], ['--humo=1'])]
    chk("(R) banderas malas abortan con codigo 2 (ERR-115): humo con pool, serie sin --top, fuerza sin bloque, abreviada, con '='", rr == [2] * 5, f"({rr})")
    pr(f"  (I) tiempo {round(time.time() - t00)} s")

    # (P) arnes por pieza
    pr("(P) ARNES POR PIEZA: monocultivo FIJO en w30, T 8 000, corte 6 000; una opcion 'vive' si cambia la trayectoria en algun contexto")
    ctxs = {'N': (1, 0, 0, 0), 'V': (2, 0, 2, 0), 'M': (3, 0, 2, 0)}
    pruebas = [('N', f, o) for f in range(4) for o in range(len(GD.CAMPOS[f])) if o != ctxs['N'][f]]
    pruebas += [('V', 3, 1), ('V', 3, 2), ('V', 3, 3), ('V', 1, 4), ('V', 2, 0), ('V', 2, 1), ('M', 3, 3), ('M', 3, 2)]
    cache = {}; tab = []; tmpp = tempfile.mkdtemp()

    def fija(s):
        b_ = 'FIJO:' + '.'.join(str(z) for z in s)
        if b_ not in cache: cache[b_] = CG.trabajo((21003, b_, 8000, 6000, 1000, tmpp, False))
        return cache[b_]

    for cx, f, o in pruebas:
        b0 = ctxs[cx]; s = list(b0); s[f] = o; s = tuple(s)
        x0 = fija(b0); x1 = fija(s)
        cambia = J({k: x0.get(k) for k in ('n_nac', 'r0_post', 'vivos_T', 'tam_total', 'max_vivos', 'nac_post')}) != \
            J({k: x1.get(k) for k in ('n_nac', 'r0_post', 'vivos_T', 'tam_total', 'max_vivos', 'nac_post')})
        tab.append(dict(contexto=cx, campo=GD.NOMBRE_CAMPO[f], opcion=GD.CAMPOS[f][o], base=GD.texto((b0 + (0,),)), prueba=GD.texto((s + (0,),)),
                        cambia=bool(cambia), n_nac=(x0['n_nac'], x1['n_nac']), r0=(x0['r0_post'], x1['r0_post']), entregas=x1['entregas']))
        pr(f"    [{cx}] {GD.NOMBRE_CAMPO[f]:>6} = {GD.CAMPOS[f][o]:<9} {'CAMBIA' if cambia else 'IGUAL '} nacidos {x0['n_nac']}->{x1['n_nac']} "
           f"r0 {x0['r0_post']}->{x1['r0_post']} entregas {x1['entregas']}")
    vive = {}
    for t in tab: vive[(t['campo'], t['opcion'])] = vive.get((t['campo'], t['opcion']), False) or t['cambia']
    inertes = [k for k, v_ in vive.items() if not v_]
    pr(f"  opciones INERTES en w30 (se declaran y NO entran al alfabeto de la serie): {inertes}")
    serie_ok = all(vive[(GD.NOMBRE_CAMPO[f], GD.CAMPOS[f][o])] for f in range(4) for o in CG.ALFABETO[f] if (GD.NOMBRE_CAMPO[f], GD.CAMPOS[f][o]) in vive)
    chk("(P) toda opcion del ALFABETO DE LA SERIE cambia algo medible en w30; las inertes quedan fuera", serie_ok and
        all(not (k[0] == 'como' and GD.COMO.index(k[1]) in CG.ALFABETO[3]) for k in inertes),
        f"(alfabeto de la serie: como = {[GD.COMO[c] for c in CG.ALFABETO[3]]})")
    os.makedirs(os.path.join(AQUI, 'datos'), exist_ok=True)
    json.dump(dict(tabla=tab, inertes=inertes, T=8000, t_corte=6000, semilla=21003), open(os.path.join(AQUI, 'datos', 'pieza_gramatica.json'), 'w', encoding='utf-8'), indent=1)
    pr(f"RESULTADO: {sum(R_)}/{len(R_)} · {round(time.time() - t00)} s")


if __name__ == '__main__':
    try:
        main()
    finally:
        with open(os.path.join(AQUI, 'identidad_gramatica_salida.txt'), 'w', encoding='utf-8') as f: f.write('\n'.join(OUT) + '\n')
