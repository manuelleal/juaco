"""identidad_eco_a_carrera.py — ARNES del bloque eco_a_carrera. Sin el, no hay exploratorio ni serie. Un proceso, sin Pool, T <= 5000.

MISION: llegar a la AGI por este camino. Con GENOMA None los carros EAC son su origen bit a bit (EAC_G0/SEL/AZA == V143_RES0 de
frio_carrera; EAC_SELV == V143_TEL, cuya fisica es V143). CON EL GENOMA G0 aplicado por el camino nuevo, EAC_G0 es la base de
frio_carrera bit a bit en todo salvo la clave de telemetria. El genoma SEL_C no es inerte y se aplica entero; la entrada del runner es
corre_frio_carrera.tarea / corre_v143.tarea campo a campo (regla 14); la extraccion es reproducible; la contabilidad de fundadores
cierra con la del juez; nube-9; ERR-115; la letra en casos sinteticos.
Salida: identidad_eco_a_carrera_salida.txt (y por pantalla). Semillas de practica 39491-39494.

    python experimentos/organelos/eco_a_carrera/identidad_eco_a_carrera.py
"""
import contextlib, io, json, math, os, sys, time
AQUI = os.path.dirname(os.path.abspath(__file__))
if AQUI not in sys.path: sys.path.insert(0, AQUI)
import corre_eco_a_carrera as R
CV = R.CV; P = R.P; FC = R.FC; CE = R.CE; XG = R.XG; RC = R.RC
N = lambda x: json.loads(json.dumps(x, default=str))
OUT = []; RES = []


def log(s=''):
    print(s, flush=True); OUT.append(s)


def chk(nombre, cond, extra=''):
    RES.append(bool(cond)); log(f"  [{'OK ' if cond else 'FALLA'}] {nombre}{(' · ' + extra) if extra else ''}")


def sin(r, *claves):
    r = N(r)
    for d in r['linajes']:
        if isinstance(d.get('carro'), dict):
            for k in claves: d['carro'].pop(k, None)
    return r


def fis(r):
    """Solo la FISICA de pista.run (sin lo que devuelve el carro)."""
    r = N(r)
    for d in r['linajes']: d.pop('carro', None)
    return r


def corre(m, s, T, g):
    m.GENOMA = g
    try: return P.run(s, [('C', m)] * 9, T=T, fundador_limpio=1)
    finally: m.GENOMA = None


def main():
    t0 = time.time()
    log(f"IDENTIDAD eco_a_carrera · {time.strftime('%Y-%m-%d %H:%M:%S')} · python {sys.version.split()[0]} · numpy {P.np.__version__}")
    log(f"  corre_eco_a_carrera.py {R.h16(R.__file__)} · construye {R.h16(CE.__file__)} · extrae {R.h16(XG.__file__)} · "
        f"este arnes {R.h16(os.path.abspath(__file__))}")
    # (K) construccion, orígenes, extraccion
    log("(K) construccion por anclas, origenes y extraccion")
    with contextlib.redirect_stdout(io.StringIO()) as so: rc = CE.main(['--verifica'])
    chk("(K1) carros en disco == construye_eco_a_carrera (origen V143_RES0 fab1d8068fe901a5; solo difieren en perillas/nombre)", rc == 0,
        so.getvalue().strip().replace('\n', ' | ')[:260])
    chk("(K2) sha de corre_frio_carrera, V143_RES0, V143_TEL, corre_v143, V143, pista, juez, O1 == fijados",
        all(R.h16(p) == s for p, s in R.SHAS.items()))
    for n in R.PROPIOS:
        v = RC.revisa_fuente(open(os.path.join(R.CARROS, n + '.py'), encoding='utf-8').read(), n)
        chk(f"(K3) revisa_carro {n}: PASA", not v, str(v[:2]))
    with contextlib.redirect_stdout(io.StringIO()) as so: rx = XG.main(['--verifica'])
    chk("(K4) genomas_eco_sel.json == re-extraccion desde los 160 JSON de ECO_SEL (determinista) y sha == fijado en el runner",
        rx == 0 and R.h16(R.GENOMAS) == R.SHA_GENOMAS, so.getvalue().strip())
    G = R.genomas(); cf = P.cfg_fabrica()
    g0_pista = {k: (cf['NK'] if k == 'NK' else cf['kw'][k]) for k in CE.GENES}
    chk("(K5) G0 de ECO == perillas de fabrica de la carrera (pista.cfg_fabrica), gen a gen", all(G['G0'][k] == g0_pista[k] for k in CE.GENES),
        str(g0_pista))
    chk("(K6) los genes del genoma son EXACTAMENTE los del carro (construye.GENES == EG_GENES del modulo) y los 15 mutables de C",
        tuple(G['genes']) == CE.GENES and "EG_GENES = " + repr(CE.GENES) in open(os.path.join(R.CARROS, 'EAC_SEL.py'), encoding='utf-8').read())
    # (D) la extraccion: medoide real, historia de vida en G0, rangos, sustitutos
    log("(D) extraccion: cada genoma es un cuerpo vivo real en T de su JSON ECO; rangos de ECO; sustitutos declarados")
    real = 0; tot = 0; fuera = 0; sust = []
    for c, carp, s0 in XG.CORRIDAS:
        for b in XG.BRAZOS:
            for s, x in G['corridas'][c][b].items():
                tot += 1
                src = x.get('sustituye') or int(s)
                d = json.load(open(os.path.join(XG.ECO, carp, f"{b}_s{src}.json"), encoding='utf-8'))
                gv = [x['genoma'][k] for k in CE.GENES]
                real += int(any(v[4:4 + 15] == gv for v in d['vivos_final']))
                for k in CE.GENES:
                    g0 = G['G0'][k]
                    fuera += int(not (g0 / 4 - 1e-9 <= x['genoma'][k] <= 4 * g0 + 1e-9))
                if x.get('sustituye'): sust.append(f"{c}:{b}:{s}<-{x['sustituye']}")
    chk("(D1) los 80 genomas son medoides REALES (un cuerpo vivo en T tiene exactamente esos 15 genes)", real == tot == 80, f"{real}/{tot}")
    chk("(D2) todos dentro de [G0/4, 4*G0] (rango de mutacion de ECO)", fuera == 0, f"fuera {fuera}")
    chk("(D3) sustitutos = solo AZA_C extintos (serie 45312, 45315, 45319; replica 45323-45325, 45333, 45339)",
        sorted(sust) == sorted(['serie:AZA_C:45312<-45313', 'serie:AZA_C:45315<-45316', 'serie:AZA_C:45319<-45320',
                                'replica:AZA_C:45323<-45326', 'replica:AZA_C:45324<-45326', 'replica:AZA_C:45325<-45326',
                                'replica:AZA_C:45333<-45334', 'replica:AZA_C:45339<-45340']), str(sust))
    chk("(D4) emparejamiento: explora 39401 -> serie 45301; serie 39440 -> 45320; replica 39441 -> 45321; practica 39491 -> replica 45331",
        R.eco_de(39401) == ('serie', 45301) and R.eco_de(39440) == ('serie', 45320) and R.eco_de(39441) == ('replica', 45321)
        and R.eco_de(39491) == ('replica', 45331))
    R.registra(); FC.registra()
    M = {n: CV._MODS[n] for n in R.PROPIOS}; RES0 = CV._MODS['V143_RES0']; TEL = CV._MODS['V143_TEL']; V = CV.modulo('V143')
    # (A) GENOMA None == origen, salida ENTERA
    log("(A) GENOMA None == origen bit a bit (salida ENTERA de pista.run: fisica + carro + pizarra; N 9, fundador limpio)")
    for n, s, T, ori in (('EAC_G0', 39491, 3000, RES0), ('EAC_SEL', 39492, 3000, RES0), ('EAC_AZA', 39493, 3000, RES0), ('EAC_SELV', 39494, 3000, TEL)):
        a = P.run(s, [('C', ori)] * 9, T=T, fundador_limpio=1); b = corre(M[n], s, T, None)
        nac = sum(sum(d['origen_cuerpo']) for d in a['linajes'])
        chk(f"(A) {n} con GENOMA None == {'V143_RES0' if ori is RES0 else 'V143_TEL'} (s {s}, T {T})", N(a) == N(b), f"nacimientos reales {nac}")
    # (A') EL ARNES DEL ENCARGO: con el genoma G0 por el camino nuevo, idéntico a la base de frio_carrera
    log("(A') con GENOMA = G0 (aplicado por _eg_aplica, el mismo camino que SEL y AZA) == base de frio_carrera, todo salvo la telemetria")
    g0 = dict(G['G0'])
    a = P.run(39491, [('C', RES0)] * 9, T=5000, fundador_limpio=1); b = corre(M['EAC_G0'], 39491, 5000, g0)
    nac = sum(sum(d['origen_cuerpo']) for d in a['linajes'])
    chk("(A'1) EAC_G0 + G0 == V143_RES0 (s 39491, T 5000) salvo d['carro']['eco_a_carrera']", sin(a) == sin(b, 'eco_a_carrera'),
        f"nacimientos reales {nac}")
    te = [d['carro'].get('eco_a_carrera') for d in b['linajes']]
    chk("(A'2) la telemetria existe en los 9 linajes y declara fuente G0 y el genoma aplicado", all(te) and all(t['fuente'] == 'G0' for t in te))
    b2 = corre(M['EAC_SELV'], 39492, 5000, g0); a2 = P.run(39492, [('C', V)] * 9, T=5000, fundador_limpio=1)
    chk("(A'3) EAC_SELV + G0 == V143 (s 39492, T 5000) salvo la telemetria frio_carrera/eco_a_carrera", sin(a2) == sin(b2, 'eco_a_carrera', 'frio_carrera'))
    x = R.tarea((39493, 'g0', 5000)); y = FC.tarea((39493, 'V143_RES0', 5000))
    # la etiqueta del linaje ('EAC_G0#i' contra 'V143_RES0#i') es el nombre del carro, no la fisica: se iguala ANTES de comparar
    xn = json.loads(json.dumps({k: v for k, v in x.items() if k not in ('seg', 'tel_eac', 'genoma', 'genoma_de')}, default=str).replace('"EAC_G0#', '"V143_RES0#'))
    ok = xn == N({k: v for k, v in y.items() if k != 'seg'})
    chk("(A'4) runner.tarea(g0) == corre_frio_carrera.tarea(V143_RES0) campo a campo (s 39493, T 5000) salvo tel_eac/genoma y la etiqueta del linaje", ok)
    chk("(A'5) tras la corrida el modulo vuelve a GENOMA None", all(m.GENOMA is None for m in M.values()))
    # (B) el genoma SEL no es inerte y se aplica entero; controles que pueden fallar
    log("(B) el genoma SEL_C actua y se aplica entero")
    gs, de = R.genoma_de('sel', 39491)
    b3 = corre(M['EAC_SEL'], 39491, 5000, gs)
    chk("(B1) EAC_SEL + genoma SEL (practica 39491 -> replica 45331) != G0 en la FISICA (control que puede fallar)",
        fis(b3) != fis(b), de)
    xs = dict(R.tarea((39491, 'sel', 3000)), brazo='sel')
    chk("(B2) genoma_ok: lo aplicado == lo declarado en los 9 linajes (sel)", R.genoma_ok([xs], 'sel'))
    xm = json.loads(json.dumps(xs)); xm['genoma']['alpha'] = xm['genoma']['alpha'] * 1.01
    chk("(B3) genoma_ok FALLA si el declarado difiere en un gen (alpha x1.01) -- el control del instrumento puede fallar", not R.genoma_ok([xm], 'sel'))
    xa = dict(R.tarea((39491, 'aza', 3000)), brazo='aza')
    chk("(B4) aza lleva el genoma AZA de la misma semilla ECO (replica 45331), distinto del de sel", xa['genoma'] != xs['genoma']
        and xa['genoma_de'].startswith('replica:AZA_C:45331') and R.genoma_ok([xa], 'aza'), xa['genoma_de'])
    src = open(os.path.join(R.CARROS, 'EAC_SEL.py'), encoding='utf-8').read()
    usos = {k: src.count(f"kw['{k}']") for k in CE.GENES if k != 'NK'}
    chk("(B5) estatico: cada gen se lee de kw UNA sola vez (en __init__, antes de _eg_aplica); nada lo relee despues", all(v == 1 for v in usos.values())
        and src.count("cf['NK']") == 1 and src.index("self._eg_aplica(GENOMA)") > src.index("kw['ema_c']"), str(usos))
    # (C) regla 14
    log("(C) regla 14: la tarea del runner == corre_v143.tarea campo a campo")
    for brz, carro in (('v143', 'V143'), ('o1', 'O1')):
        x = R.tarea((39494, brz, 2000)); y = CV.tarea((39494, carro, 2000))
        e = (x.pop('tel_eac') == [None] * 9 and x.pop('tel_fc') == [None] * 9 and x.pop('genoma') is None and x.pop('genoma_de') is None
             and N({k: v for k, v in x.items() if k != 'seg'}) == N({k: v for k, v in y.items() if k != 'seg'}))
        chk(f"(C) runner.tarea({brz}) == corre_v143.tarea({carro}) (s 39494, T 2000)", e)
    chk("(C2) P.run restaurado tras las tareas", P.run.__name__ == 'run')
    # (F) contabilidad de fundadores == juez
    log("(F) contabilidad de fundadores (fisica) cierra con la del juez")
    x = dict(R.tarea((39492, 'v143', 5000)), brazo='v143', aborto=None)
    fz = R.fundadores([x]); cz = {k: sum(l['causas'][k] for l in x['linajes']) for k in ('hambre', 'sed', 'veneno', 'sal')}
    tot_ok = all(fz['causas_fundadores'][k] + fz['causas_nacidos'][k] == cz[k] for k in cz)
    nf_ok = sum(1 for l in x['linajes'] for i in range(l['muertes']) if not l['telem']['origen'][i]) == fz['muertes_fundadores']
    ff_ok = all(sum(1 for g in l['telem']['origen'] if not g) == l['fundadores'] + 1 for l in x['linajes'])
    chk("(F1) causas fundadores + causas nacidos == causas del juez, por causa", tot_ok, f"{fz['causas_fundadores']} + {fz['causas_nacidos']} = {cz}")
    chk("(F2) muertes de fundadores == cuerpos con origen 0 muertos; fundadores del juez + 1 == origen 0", nf_ok and ff_ok, str(fz))
    # (G) determinismo
    x2 = dict(R.tarea((39492, 'v143', 5000)), brazo='v143', aborto=None)
    chk("(G) determinismo: la misma tarea dos veces da lo mismo (salvo seg)", N({k: v for k, v in x.items() if k != 'seg'}) == N({k: v for k, v in x2.items() if k != 'seg'}))
    # (H) nube-9
    log("(H) nube-9: un aborto dentro del carro se atrapa, escribe JSON y deja el modulo limpio")
    import tempfile
    tmp = tempfile.mkdtemp(prefix='eac_arnes_')
    orig = R.genoma_de
    try:
        R.genoma_de = lambda b, s: (dict(orig(b, s)[0], NK=9999), 'MALO')
        z = R.trabajo((39493, 'sel', 1000, tmp, False))
    finally:
        R.genoma_de = orig
    chk("(H1) NK fuera de rango -> aborto atrapado (SystemExit del carro), JSON escrito, GENOMA vuelve a None",
        z['aborto'] and 'NK' in z['aborto'] and os.path.exists(os.path.join(tmp, 'sel_s39493.json')) and M['EAC_SEL'].GENOMA is None, str(z['aborto'])[:120])
    # (V) la letra en casos sinteticos
    log("(V) la letra (la del muro, sin cambios) y el criterio exploratorio en casos sinteticos")
    def res(sel_g, aza_g, o1_g=True, v143=0.6, coh=True):
        b = lambda g: dict(gana_e5=g, R0_real_med=0.5, coherente='180/180' if coh else '179/180')
        r = {k: b(False) for k in R.SERIE_BRAZOS}; r['sel'] = b(sel_g); r['aza'] = b(aza_g); r['o1'] = b(o1_g); r['v143']['R0_real_med'] = v143
        return r
    pv = lambda g, d, ga=16: {('sel', 'v143'): dict(semillas=20, gana=g, dif_med=d), ('sel', 'aza'): dict(semillas=20, gana=ga, dif_med=0.1)}
    gk = dict(sel=True, aza=True, g0=True)
    casos = [
        ("FUNCIONA", res(True, False), pv(16, 0.2), gk, True, 0, 'FUNCIONA'),
        ("MODESTO (P2 + dif 0.10 + gana a aza 11/20)", res(False, False), pv(15, 0.10, 11), gk, True, 0, 'HAY ALGO MODESTO'),
        ("NO: gana a aza solo 10/20", res(False, False), pv(15, 0.10, 10), gk, True, 0, 'NO'),
        ("NO: dif 0.09", res(False, False), pv(18, 0.09), gk, True, 0, 'NO'),
        ("NO: P2 14/20", res(True, False), pv(14, 0.3), gk, True, 0, 'NO'),
        ("NO: el control cruza (P3) y no hay MODESTO por P2", res(True, True), pv(14, 0.3), gk, True, 0, 'NO'),
        ("MODESTO: todo salvo P3", res(True, True), pv(16, 0.3), gk, True, 0, 'HAY ALGO MODESTO'),
        ("NO SE LEE: O1 no gana", res(True, False, o1_g=False), pv(16, 0.2), gk, True, 0, 'NO SE LEE'),
        ("NO SE LEE: V143 fuera [0.40, 0.80]", res(True, False, v143=0.85), pv(16, 0.2), gk, True, 0, 'NO SE LEE'),
        ("NO SE LEE: genoma no aplicado (V4)", res(True, False), pv(16, 0.2), dict(gk, aza=False), True, 0, 'NO SE LEE'),
        ("NO SE LEE: un aborto", res(True, False), pv(16, 0.2), gk, True, 1, 'NO SE LEE'),
        ("NO SE LEE: contabilidad incoherente", res(True, False, coh=False), pv(16, 0.2), gk, True, 0, 'NO SE LEE'),
    ]
    for nom, r_, p_, g_, c_, a_, esp in casos:
        v = R.lee_serie(r_, p_, g_, c_, a_)['veredicto']; chk(f"(V) {nom} -> {esp}", v == esp, v)
    fz_ = lambda s, g: dict(sel=dict(frac_BD_fundadores=s), g0=dict(frac_BD_fundadores=g))
    ce = lambda gg, dg, ga: {('sel', 'g0'): dict(semillas=10, gana=gg, dif_med=dg), ('sel', 'aza'): dict(semillas=10, gana=ga, dif_med=0.1)}
    chk("(V) explora: 8/10 +0.05, aza 8/10, BD menor -> mejora", R.criterio_explora(ce(8, 0.05, 8), fz_(0.8, 0.9))['mejora_claramente'])
    chk("(V) explora: 7/10 -> no", not R.criterio_explora(ce(7, 0.2, 9), fz_(0.8, 0.9))['mejora_claramente'])
    chk("(V) explora: dif 0.04 -> no", not R.criterio_explora(ce(9, 0.04, 9), fz_(0.8, 0.9))['mejora_claramente'])
    chk("(V) explora: BD igual -> no", not R.criterio_explora(ce(9, 0.2, 9), fz_(0.9, 0.9))['mejora_claramente'])
    # (R) banderas
    log("(R) banderas (ERR-115) y rangos")
    for args, nom in ((['--humo', '--pool', '2'], 'humo con pool'), (['--explora', '--semillas', '39411'], 'explora fuera de rango'),
                      (['--serie', '--desde', '39401', '--n', '20'], 'serie en semillas de explora'), (['--humo', '--hum'], 'bandera abreviada'),
                      (['--explora', '--semillas', '39401', '--T', '20000'], 'explora con T != 1e5'),
                      (['--explora', '--semillas', '39401', '--brazos', 'bar0'], 'brazo desconocido')):
        try:
            with contextlib.redirect_stderr(io.StringIO()): R.main(args)
            ab = False
        except SystemExit:
            ab = True
        chk(f"(R) {nom}: ABORTA", ab)
    n_ok = sum(RES)
    log(f"\nARNES eco_a_carrera: {n_ok}/{len(RES)} {'TODO OK' if n_ok == len(RES) else 'HAY FALLAS'} · {time.time() - t0:.0f} s")
    with open(os.path.join(AQUI, 'identidad_eco_a_carrera_salida.txt'), 'w', encoding='utf-8') as fh: fh.write('\n'.join(OUT) + '\n')
    return 0 if n_ok == len(RES) else 1


if __name__ == '__main__':
    sys.exit(main())
