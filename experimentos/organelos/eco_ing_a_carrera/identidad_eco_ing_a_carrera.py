"""identidad_eco_ing_a_carrera.py — ARNES del bloque eco_ing_a_carrera. Sin el, no hay exploratorio ni serie. Un proceso, sin Pool, T <= 5000.

MISION: llegar a la AGI por este camino. Con GENOMA None los carros EIC son su origen bit a bit (EIC_G0/ING/AZA/SELC == V143_RES0;
EIC_G0V/INGV/AZAV == V143_TEL, fisica V143). CON EL GENOMA G0 por el camino nuevo, EIC_G0 == V143_RES0 y EIC_G0V == V143 (la base
PRIMARIA) salvo telemetria. Los genomas ING son medoides reales de ECO_SEL_ING con la regla importada de eco_a_carrera; no son inertes y
se aplican enteros; regla 14 contra corre_v143.tarea / corre_frio_carrera.tarea; fundadores == juez y == eco_a_carrera.fundadores;
nube-9; ERR-115; la letra y el criterio en casos sinteticos. Semillas de practica 39561-39564.
Salida: identidad_eco_ing_a_carrera_salida.txt.

    python experimentos/organelos/eco_ing_a_carrera/identidad_eco_ing_a_carrera.py
"""
import contextlib, io, json, os, sys, time
AQUI = os.path.dirname(os.path.abspath(__file__))
if AQUI not in sys.path: sys.path.insert(0, AQUI)
import corre_eco_ing_a_carrera as R
CV = R.CV; P = R.P; FC = R.FC; CI = R.CI; XI = R.XI; RC = R.RC
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
    r = N(r)
    for d in r['linajes']: d.pop('carro', None)
    return r


def corre(m, s, T, g):
    m.GENOMA = g
    try: return P.run(s, [('C', m)] * 9, T=T, fundador_limpio=1)
    finally: m.GENOMA = None


def main():
    t0 = time.time()
    log(f"IDENTIDAD eco_ing_a_carrera · {time.strftime('%Y-%m-%d %H:%M:%S')} · python {sys.version.split()[0]} · numpy {P.np.__version__}")
    log(f"  corre_eco_ing_a_carrera.py {R.h16(R.__file__)} · construye {R.h16(CI.__file__)} · extrae {R.h16(XI.__file__)} · "
        f"este arnes {R.h16(os.path.abspath(__file__))}")
    log("(K) construccion por anclas, origenes y extraccion")
    with contextlib.redirect_stdout(io.StringIO()) as so: rc = CI.main(['--verifica'])
    chk("(K1) carros en disco == construye_eco_ing_a_carrera (sobre construye_eco_a_carrera 403c747caaae1c1e; solo cabecera/perillas/nombre)",
        rc == 0, so.getvalue().strip().replace('\n', ' | ')[:300])
    chk("(K2) shas fijados (frio_carrera, V143_RES0, V143_TEL, corre_v143, V143, pista, juez, O1, eco_a_carrera x3, genomas_eco_sel)",
        all(R.h16(p) == s for p, s in R.SHAS.items()))
    for n in R.PROPIOS:
        v = RC.revisa_fuente(open(os.path.join(R.CARROS, n + '.py'), encoding='utf-8').read(), n)
        chk(f"(K3) revisa_carro {n}: PASA", not v, str(v[:2]))
    with contextlib.redirect_stdout(io.StringIO()) as so: rx = XI.main(['--corrida', 'serie', '--verifica'])
    chk("(K4) genomas_ing_serie.json == re-extraccion desde los 40 JSON de ECO_SEL_ING serie y sha == fijado en el runner",
        rx == 0 and R.h16(R.GEN_ING['serie']) == R.SHA_GEN['serie'], so.getvalue().strip())
    XG = XI.xg()
    chk("(K5) el medoide es la funcion de eco_a_carrera (importada, no copiada)", XG.medoide.__module__ == 'extrae_genomas'
        and os.path.samefile(XG.__file__, os.path.join(R.EAC, 'extrae_genomas.py')))
    G = R.carga('serie', R.GEN_ING['serie'], R.SHA_GEN['serie']); GS = R.carga('sel', R.GEN_SEL, R.SHAS[R.GEN_SEL])
    cf = P.cfg_fabrica(); g0_pista = {k: (cf['NK'] if k == 'NK' else cf['kw'][k]) for k in R.CI.ce().GENES}
    chk("(K6) G0 de ECO_SEL_ING == G0 de ECO_SEL == perillas de fabrica de la carrera, gen a gen",
        all(G['G0'][k] == g0_pista[k] == GS['G0'][k] for k in g0_pista), str(g0_pista))
    chk("(K7) genes del genoma == EG_GENES del carro == 15 mutables", tuple(G['genes']) == R.CI.ce().GENES
        and "EG_GENES = " + repr(R.CI.ce().GENES) in open(os.path.join(R.CARROS, 'EIC_INGV.py'), encoding='utf-8').read())
    ref = open(os.path.join(R.EAC, 'carros', 'EAC_SEL.py'), encoding='utf-8').read().split('\n')
    mio = open(os.path.join(R.CARROS, 'EIC_SELC.py'), encoding='utf-8').read().split('\n')
    dif = [i for i, (x, y) in enumerate(zip(ref, mio)) if x != y]
    chk("(K8) EIC_SELC == EAC_SEL de eco_a_carrera salvo la cabecera y el nombre (la referencia es el carro que fallo)",
        len(ref) == len(mio) and all(i == 0 or 'EIC_SELC' in mio[i] for i in dif), f"lineas distintas {dif}")
    log("(D) extraccion: cada genoma es un cuerpo vivo real en T de su JSON ECO_SEL_ING; rangos; sin sustitutos")
    real = tot = fuera = 0; sust = []
    carp, s0 = XI.CORRIDAS['serie']
    for b in XI.BRAZOS:
        for s, x in G['brazos'][b].items():
            tot += 1; src = x.get('sustituye') or int(s)
            d = json.load(open(os.path.join(XI.ECO, carp, f"{b}_s{src}.json"), encoding='utf-8'))
            gv = [x['genoma'][k] for k in G['genes']]
            real += int(any(v[4:4 + 15] == gv for v in d['vivos_final']))
            fuera += sum(int(not (G['G0'][k] / 4 - 1e-9 <= x['genoma'][k] <= 4 * G['G0'][k] + 1e-9)) for k in G['genes'])
            if x.get('sustituye'): sust.append(f"{b}:{s}")
    chk("(D1) los 40 genomas son medoides REALES", real == tot == 40, f"{real}/{tot}")
    chk("(D2) todos dentro de [G0/4, 4*G0]", fuera == 0, f"fuera {fuera}")
    chk("(D3) sin sustitutos (vivero permanente: nadie se extingue)", not sust, str(sust))
    chk("(D4) emparejamiento: 39461 -> ING serie 46101 / ECO_SEL 45301; 39530 -> 46120; 39531 -> replica 46121 / 45321; 39561 -> 46111 / 45311",
        R.eco_de(39461) == ('serie', 46101, 'serie', 45301) and R.eco_de(39530) == ('serie', 46120, 'serie', 45320)
        and R.eco_de(39531) == ('replica', 46121, 'replica', 45321) and R.eco_de(39561) == ('serie', 46111, 'serie', 45311))
    gi, dei = R.genoma_de('ingv', 39461); gs, des = R.genoma_de('selc', 39461)
    chk("(D5) ingv 39461 lleva el medoide ING_SEL_C de 46101; selc el SEL_C de 45301 (el de eco_a_carrera en 39401)",
        gi == G['brazos']['ING_SEL_C']['46101']['genoma'] and gs == GS['corridas']['serie']['SEL_C']['45301']['genoma'], f"{dei} · {des}")
    try: R.genoma_de('ingv', 39531); rep = False
    except SystemExit: rep = True
    chk("(D6) la replica ABORTA mientras su sha no este fijado", rep)
    R.registra(); FC.registra()
    M = {n: CV._MODS[n] for n in R.PROPIOS}; RES0 = CV._MODS['V143_RES0']; TEL = CV._MODS['V143_TEL']; V = CV.modulo('V143')
    log("(A) GENOMA None == origen bit a bit (salida ENTERA de pista.run; N 9, fundador limpio, T 2000)")
    for i, n in enumerate(R.PROPIOS):
        ori = RES0 if n in ('EIC_G0', 'EIC_ING', 'EIC_AZA', 'EIC_SELC') else TEL; s = 39561 + i % 4
        a = P.run(s, [('C', ori)] * 9, T=2000, fundador_limpio=1); b = corre(M[n], s, 2000, None)
        chk(f"(A) {n} con GENOMA None == {'V143_RES0' if ori is RES0 else 'V143_TEL'} (s {s})", N(a) == N(b))
    log("(A') con GENOMA = G0 por el camino nuevo == la base (todo salvo la telemetria)")
    g0 = dict(G['G0'])
    a = P.run(39561, [('C', RES0)] * 9, T=5000, fundador_limpio=1); b = corre(M['EIC_G0'], 39561, 5000, g0)
    nac = sum(sum(d['origen_cuerpo']) for d in a['linajes'])
    chk("(A'1) EIC_G0 + G0 == V143_RES0 (s 39561, T 5000) salvo d['carro']['eco_a_carrera']", sin(a) == sin(b, 'eco_a_carrera'), f"nacimientos {nac}")
    a2 = P.run(39562, [('C', V)] * 9, T=5000, fundador_limpio=1); b2 = corre(M['EIC_G0V'], 39562, 5000, g0)
    nac2 = sum(sum(d['origen_cuerpo']) for d in a2['linajes'])
    chk("(A'2) EIC_G0V + G0 == V143 (s 39562, T 5000) salvo telemetria (LA BASE PRIMARIA)", sin(a2) == sin(b2, 'eco_a_carrera', 'frio_carrera'),
        f"nacimientos {nac2}")
    x = R.tarea((39563, 'g0v', 5000)); y = CV.tarea((39563, 'V143', 5000))
    chk("(A'3) runner.tarea(g0v) == corre_v143.tarea(V143) con fisica_igual (s 39563, T 5000) -- la comparacion de la identidad LARGA",
        R.fisica_igual(x, y, 'EIC_G0V', 'V143'))
    x = R.tarea((39563, 'g0', 5000)); y = FC.tarea((39563, 'V143_RES0', 5000))
    chk("(A'4) runner.tarea(g0) == corre_frio_carrera.tarea(V143_RES0) (s 39563, T 5000)", R.fisica_igual(x, y, 'EIC_G0', 'V143_RES0'))
    chk("(A'5) tras las corridas los modulos vuelven a GENOMA None", all(m.GENOMA is None for m in M.values()))
    log("(B) los genomas actuan y se aplican enteros; controles que pueden fallar")
    gp, dep = R.genoma_de('ingv', 39561)
    b3 = corre(M['EIC_INGV'], 39562, 5000, gp)
    chk("(B1) EIC_INGV + ING_SEL_C != G0 en la FISICA (s 39562)", fis(b3) != fis(b2), dep)
    xi = dict(R.tarea((39561, 'ingv', 3000)), brazo='ingv'); xa = dict(R.tarea((39561, 'azav', 3000)), brazo='azav')
    chk("(B2) genoma_ok ingv y azav (aplicado == declarado en los 9 linajes)", R.genoma_ok([xi], 'ingv') and R.genoma_ok([xa], 'azav'))
    xm = json.loads(json.dumps(xi)); xm['genoma']['alpha'] *= 1.01
    chk("(B3) genoma_ok FALLA si el declarado difiere en un gen (alpha x1.01)", not R.genoma_ok([xm], 'ingv'))
    chk("(B4) azav lleva ING_AZA_C de la misma semilla ECO (46111), distinto de ING_SEL_C", xa['genoma'] != xi['genoma']
        and xa['genoma_de'] == 'serie:ING_AZA_C:46111' and xi['genoma_de'] == 'serie:ING_SEL_C:46111', f"{xa['genoma_de']} · {xi['genoma_de']}")
    y2 = CV.tarea((39561, 'V143', 3000))
    chk("(B5) fisica_igual PUEDE FALLAR: ingv != v143 (s 39561, T 3000)", not R.fisica_igual(xi, y2, 'EIC_INGV', 'V143'))
    xs = dict(R.tarea((39561, 'selc', 3000)), brazo='selc')
    chk("(B6) selc: genoma SEL_C de ECO_SEL 45311 aplicado", R.genoma_ok([xs], 'selc') and xs['genoma_de'] == 'serie:SEL_C:45311', xs['genoma_de'])
    log("(C) regla 14: la tarea del runner == corre_v143.tarea campo a campo")
    for brz, carro in (('v143', 'V143'), ('o1', 'O1')):
        x = R.tarea((39564, brz, 2000)); y = CV.tarea((39564, carro, 2000))
        e = (x.pop('tel_eac') == [None] * 9 and x.pop('tel_fc') == [None] * 9 and x.pop('genoma') is None and x.pop('genoma_de') is None
             and N({k: v for k, v in x.items() if k != 'seg'}) == N({k: v for k, v in y.items() if k != 'seg'}))
        chk(f"(C) runner.tarea({brz}) == corre_v143.tarea({carro}) (s 39564, T 2000)", e)
    chk("(C2) P.run restaurado tras las tareas", P.run.__name__ == 'run')
    log("(F) fundadores: == juez y == eco_a_carrera.fundadores (entrada)")
    x = dict(R.tarea((39562, 'v143', 5000)), brazo='v143', aborto=None)
    fz = R.fundadores([x]); cz = {k: sum(l['causas'][k] for l in x['linajes']) for k in ('hambre', 'sed', 'veneno', 'sal')}
    chk("(F1) causas fundadores + nacidos == causas del juez", all(fz['causas_fundadores'][k] + fz['causas_nacidos'][k] == cz[k] for k in cz))
    chk("(F2) fundadores del juez + 1 == cuerpos de origen 0", all(sum(1 for g in l['telem']['origen'] if not g) == l['fundadores'] + 1 for l in x['linajes']))
    if R.EAC not in sys.path: sys.path.insert(0, R.EAC)
    with contextlib.redirect_stdout(io.StringIO()): import corre_eco_a_carrera as EA
    chk("(F3) fundadores() == eco_a_carrera.fundadores() sobre la misma corrida (copia textual)", N(EA.fundadores([x])) == N(fz))
    pf = R.pareado_fund([dict(seed=1, linajes=[dict(fundadores=2)] * 9), dict(seed=2, linajes=[dict(fundadores=5)] * 9)],
                        [dict(seed=1, linajes=[dict(fundadores=3)] * 9), dict(seed=2, linajes=[dict(fundadores=5)] * 9)])
    chk("(F4) pareado_fund: menos estricto (2<3 cuenta, 5=5 no)", pf['menos'] == 1 and pf['semillas'] == 2, str(pf))
    x2 = dict(R.tarea((39562, 'v143', 5000)), brazo='v143', aborto=None)
    chk("(G) determinismo: la misma tarea dos veces da lo mismo (salvo seg)", N({k: v for k, v in x.items() if k != 'seg'}) == N({k: v for k, v in x2.items() if k != 'seg'}))
    log("(H) nube-9")
    import tempfile
    tmp = tempfile.mkdtemp(prefix='eic_arnes_'); orig = R.genoma_de
    try:
        R.genoma_de = lambda b, s: (dict(orig(b, s)[0], NK=9999), 'MALO')
        z = R.trabajo((39563, 'ingv', 1000, tmp, False))
    finally:
        R.genoma_de = orig
    chk("(H1) NK fuera de rango -> aborto atrapado, JSON escrito, GENOMA vuelve a None",
        z['aborto'] and 'NK' in z['aborto'] and os.path.exists(os.path.join(tmp, 'ingv_s39563.json')) and M['EIC_INGV'].GENOMA is None, str(z['aborto'])[:100])
    log("(V) la letra (la del muro, sin cambios; hipotesis ingv, control azav) y el criterio exploratorio en casos sinteticos")
    def res(h, c, o1_g=True, v143=0.6, coh=True):
        b = lambda g: dict(gana_e5=g, R0_real_med=0.5, coherente='180/180' if coh else '179/180')
        r = {k: b(False) for k in R.SERIE_BRAZOS}; r['ingv'] = b(h); r['azav'] = b(c); r['o1'] = b(o1_g); r['v143']['R0_real_med'] = v143
        return r
    pv = lambda g, d, ga=16: {('ingv', 'v143'): dict(semillas=20, gana=g, dif_med=d), ('ingv', 'azav'): dict(semillas=20, gana=ga, dif_med=0.1)}
    gk = dict(ingv=True, azav=True)
    casos = [("FUNCIONA", res(True, False), pv(16, 0.2), gk, 0, 'FUNCIONA'),
             ("MODESTO (P2 + dif 0.10 + gana a azav 11/20)", res(False, False), pv(15, 0.10, 11), gk, 0, 'HAY ALGO MODESTO'),
             ("NO: gana a azav solo 10/20", res(False, False), pv(15, 0.10, 10), gk, 0, 'NO'),
             ("NO: dif 0.09", res(False, False), pv(18, 0.09), gk, 0, 'NO'),
             ("NO: P2 14/20", res(True, False), pv(14, 0.3), gk, 0, 'NO'),
             ("MODESTO: todo salvo P3", res(True, True), pv(16, 0.3), gk, 0, 'HAY ALGO MODESTO'),
             ("NO SE LEE: O1 no gana", res(True, False, o1_g=False), pv(16, 0.2), gk, 0, 'NO SE LEE'),
             ("NO SE LEE: V143 fuera [0.40, 0.80]", res(True, False, v143=0.85), pv(16, 0.2), gk, 0, 'NO SE LEE'),
             ("NO SE LEE: genoma no aplicado (V4)", res(True, False), pv(16, 0.2), dict(gk, azav=False), 0, 'NO SE LEE'),
             ("NO SE LEE: un aborto", res(True, False), pv(16, 0.2), gk, 1, 'NO SE LEE'),
             ("NO SE LEE: contabilidad incoherente", res(True, False, coh=False), pv(16, 0.2), gk, 0, 'NO SE LEE')]
    for nom, r_, p_, g_, a_, esp in casos:
        v = R.lee_serie(r_, p_, g_, True, a_)['veredicto']; chk(f"(V) {nom} -> {esp}", v == esp, v)
    ce = lambda g1, g2, fm: R.criterio_explora({('ingv', 'v143'): dict(semillas=10, gana=g1, dif_med=0.1), ('ingv', 'azav'): dict(semillas=10, gana=g2, dif_med=0.1)},
                                                {('ingv', 'v143'): dict(semillas=10, menos=fm, dif_med=-1)}, 'ingv', 'azav', 'v143')['PASA']
    chk("(V) explora 7/7/7 -> PASA", ce(7, 7, 7))
    chk("(V) explora 6/9/9 -> no; 9/6/9 -> no; 9/9/6 -> no", not ce(6, 9, 9) and not ce(9, 6, 9) and not ce(9, 9, 6))
    log("(R) banderas (ERR-115) y rangos")
    for args, nom in ((['--humo', '--pool', '2'], 'humo con pool'), (['--explora', '--semillas', '39471'], 'explora fuera de rango'),
                      (['--serie', '--desde', '39461', '--n', '10'], 'serie en semillas de explora'), (['--humo', '--hum'], 'bandera abreviada'),
                      (['--explora', '--semillas', '39461', '--T', '20000'], 'explora con T != 1e5'),
                      (['--explora', '--semillas', '39461', '--brazos', 'sel'], 'brazo desconocido')):
        try:
            with contextlib.redirect_stderr(io.StringIO()): R.main(args)
            ab = False
        except SystemExit:
            ab = True
        chk(f"(R) {nom}: ABORTA", ab)
    n_ok = sum(RES)
    log(f"\nARNES eco_ing_a_carrera: {n_ok}/{len(RES)} {'TODO OK' if n_ok == len(RES) else 'HAY FALLAS'} · {time.time() - t0:.0f} s")
    with open(os.path.join(AQUI, 'identidad_eco_ing_a_carrera_salida.txt'), 'w', encoding='utf-8') as fh: fh.write('\n'.join(OUT) + '\n')
    return 0 if n_ok == len(RES) else 1


if __name__ == '__main__':
    sys.exit(main())
