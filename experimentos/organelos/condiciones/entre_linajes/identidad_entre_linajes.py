"""identidad_entre_linajes.py — ARNES del exploratorio entre_linajes (30-sep-2026). Un proceso, sin Pool. Semillas de practica 624950-624989.
Corre ANTES de mirar numeros. Escribe identidad_entre_linajes_salida.txt (y la imprime).

(a) shas fijados (pista.py, juez.py, pista_pob.py, corre_o1_evo.py, O1_PAS.py, construye_o1_pas.py, corre_v143.py).
(b) I1: la camara sin gancho y con gancho 'nada' == pista.run (salida ENTERA, 9 x O1_PAS, fundador limpio).
(c) I2: cadena 'igual' (2 pasajes) == corre_o1_evo.cadena('o1pas') campo a campo y siembra bit a bit; pasaje 'nada' con PS_LEE 0 y siembra ==
    corre_o1_evo.tarea('o1neu') (salida entera menos 'seg').
(d) N1 (el neutro es neutro): PS_LEE 0, colonizacion vs 'nada', mismas semillas y siembra: la FISICA (juez: linajes y pista) es identica
    bit a bit y hubo colonos (no vacuo).
(e) N2: PS_LEE 1 con sigma 0 y genes de fabrica: colonizar no cambia la fisica (los colonos traen fabrica) y hubo colonos.
(f) C1 (DEBE DIFERIR): PS_LEE 1, sigma 0.03, colonizacion vs 'nada': la fisica cambia.
(g) siembra_prop: con partos iguales == siembra igualada; con partos desiguales difiere, conserva el total y reparte por restos mayores;
    un linaje con todos los partos se lleva toda la siembra; sin partos -> igualada.
(h) integridad de la colonizacion: nunca de si mismo (diagonal 0), colonos <= fundadores, t_col == colonos, partos de la camara ==
    contador del carro (_TEL partos) por linaje.
(i) regla 14: prueba del runner == corre_o1_evo.trabajo('prueba') (misma entrada, salida menos 'seg'), para O1_PAS con siembra y para O1.
(j) LA LETRA en casos sinteticos (FUNCIONA, MODESTO x4 incl. H-1 'no atribuible a la camara', NO, NO APLICA x3, umbral; ERR-158).
(k) el runner niega --pool 3 y banderas abreviadas.
"""
import copy, json, os, shutil, sys, tempfile, time
AQUI = os.path.dirname(os.path.abspath(__file__))
if AQUI not in sys.path: sys.path.insert(0, AQUI)
import camara_linajes as CL
import corre_entre_linajes as R
E = CL.E; P = CL.P
SAL = []; RES = []


def log(s=''):
    print(s, flush=True); SAL.append(s)


def chk(nombre, ok, extra=''):
    RES.append(bool(ok)); log(f"  [{'OK' if ok else 'FALLA'}] {nombre}{(' · ' + extra) if extra else ''}")


def sin_seg(x):
    if isinstance(x, dict): return {k: sin_seg(v) for k, v in x.items() if k != 'seg'}
    if isinstance(x, list): return [sin_seg(v) for v in x]
    return x


def js(x): return json.loads(json.dumps(x, default=str))
def fisica(x): return js(dict(linajes=x['linajes'], pista=x['pista'], R0=x.get('R0_pista')))


t0 = time.time()
log(f"ARNES entre_linajes · {time.strftime('%Y-%m-%d %H:%M:%S')} · camara {CL.h16(os.path.join(AQUI, 'camara_linajes.py'))} · runner "
    f"{CL.h16(os.path.join(AQUI, 'corre_entre_linajes.py'))}")
# (a)
log("(a) shas")
for r, s, s0, ok in CL.verifica_shas(): chk(f"sha {os.path.relpath(r, CL.RAIZ)} {s}", ok, '' if ok else f"fijado {s0}")
# (b)
log("(b) I1 camara sin gancho / 'nada' == pista.run")
E.fija('o1pas'); m = E.CV._MODS['O1_PAS']
kw = dict(T=2000, pizarra=1, rep_acum=0, escala=1, mundo_n=None, fundador_limpio=1)
def corre(f, seed):
    m._TEL.clear(); m._PS_CNT.clear(); m.PS_SEMILLA = seed; return json.dumps(f(seed, [('X', m)] * 9, **kw), default=str)
base = corre(P.run, 624951)
chk("camara(None) == pista.run (salida entera)", corre(CL.corre_camara(None), 624951) == base)
chk("camara(Colonizador 'nada') == pista.run (salida entera)", corre(CL.corre_camara(CL.Colonizador(624951, 'nada')), 624951) == base)
m.PS_SEMILLA = 0
# (c)
log("(c) I2 cadena 'igual' == corre_o1_evo.cadena ; pasaje 'nada' PS_LEE 0 == corre_o1_evo.tarea('o1neu')")
tmp = tempfile.mkdtemp(prefix='entre_linajes_arnes_')
try:
    bs = (624952, 0)
    ce = E.cadena(0, bs, 2, 2000, os.path.join(tmp), False, brazo='o1pas')
    d2 = os.path.join(tmp, 'mia'); os.makedirs(d2)
    cm = R.cadena(0, 'igual', bs, 2, 2000, d2, False)
    for p in range(2):
        fe = sin_seg(js(ce['pasajes'][p])); fm = sin_seg(js(cm['pasajes'][p]))
        chk(f"pasaje {p}: fila de o1_evo == fila de la camara en TODAS sus claves ({len(fe)})", all(fm.get(k) == v for k, v in fe.items()))
    chk("siembra final bit a bit", js(ce['siembra_final']) == js(cm['siembra_final']), f"{len(cm['siembra_final'])} entradas")
    sie = cm['siembra_final']
    xe = E.tarea(624953, 'o1neu', 2000, siembra=sie, lee=0); xm, cam = CL.tarea_pasaje(624953, 'o1neu', 2000, sie, 0, 'nada')
    chk("pasaje 'nada' PS_LEE 0 con siembra == corre_o1_evo.tarea('o1neu') (salida entera menos seg)", sin_seg(js(xe)) == sin_seg(js(xm)))
    # (d)
    log("(d) N1 neutro: PS_LEE 0, colonizacion vs 'nada' -> misma fisica")
    for s in (624954, 624955):
        xa, ca = CL.tarea_pasaje(s, 'o1neu', 3000, sie, 0, 'nada'); xb, cb = CL.tarea_pasaje(s, 'o1neu', 3000, sie, 0, 'col')
        chk(f"s {s}: fisica identica con {cb['colonos_total']} colonos (>0)", fisica(xa) == fisica(xb) and cb['colonos_total'] > 0)
        chk(f"s {s}: los genes SI viajan (siembra siguiente distinta)", E.siembra(xa['tel_ps'], 3000) != E.siembra(xb['tel_ps'], 3000))
    # (e)
    log("(e) N2: PS_LEE 1, sigma 0, fabrica: colonizar no cambia la fisica")
    xa, ca = CL.tarea_pasaje(624956, 'o1pas', 3000, None, 1, 'nada', sigma=0.0); xb, cb = CL.tarea_pasaje(624956, 'o1pas', 3000, None, 1, 'col', sigma=0.0)
    chk(f"fisica identica con {cb['colonos_total']} colonos (>0)", fisica(xa) == fisica(xb) and cb['colonos_total'] > 0)
    # (f)
    log("(f) C1 DEBE DIFERIR: PS_LEE 1, sigma 0.03, colonizacion vs 'nada'")
    dif = []
    for s in (624957, 624958):
        xa, ca = CL.tarea_pasaje(s, 'o1pas', 3000, sie, 1, 'nada'); xb, cb = CL.tarea_pasaje(s, 'o1pas', 3000, sie, 1, 'col')
        dif.append(fisica(xa) != fisica(xb)); log(f"    s {s}: colonos {cb['colonos_total']}/{cb['fundadores_total']} · fisica distinta {dif[-1]}")
        # (h) integridad sobre esta corrida
        chk(f"(h) s {s}: diagonal de origen 0", all(cb['origen'][i][i] == 0 for i in range(9)))
        chk(f"(h) s {s}: colonos <= fundadores por linaje; t_col == colonos",
            all(c <= f for c, f in zip(cb['colonos'], cb['fundadores'])) and len(cb['t_col']) == cb['colonos_total'])
        chk(f"(h) s {s}: partos de la camara == contador del carro", cb['partos'] == [int((xb['tel_ps'].get(str(i)) or {}).get('partos', 0)) for i in range(9)],
            f"{cb['partos']}")
        chk(f"(h) s {s}: el colonizador actua solo tras fundadores (limpios + colonos == fundadores)",
            all(l + c == f for l, c, f in zip(cb['limpios'], cb['colonos'], cb['fundadores'])))
    chk("C1: la fisica cambia en al menos una semilla (el control puede fallar)", any(dif))
    # (g)
    log("(g) siembra_prop")
    fab = list(E.FABRICA.values())
    tel = {str(j): dict(vivos=[[t, [fab[0] + j, fab[1], fab[2], fab[3] + t]] for t in range(5)], partos=4) for j in range(9)}
    chk("partos iguales -> == siembra igualada (bit a bit)", CL.siembra_prop(tel, 5, 5)[0] == E.siembra(tel, 5, 5))
    tel2 = copy.deepcopy(tel)
    for j, pp in enumerate([0, 1, 2, 3, 4, 5, 6, 7, 8]): tel2[str(j)]['partos'] = pp
    s2, inf2 = CL.siembra_prop(tel2, 5, 5)
    esper = CL.cuotas([0, 1, 2, 3, 4, 5, 6, 7, 8], 45)
    chk("partos desiguales -> distinta, total 45, cuotas por restos mayores", s2 != E.siembra(tel2, 5, 5) and len(s2) == 45
        and [inf2['n_por_linaje'][str(j)] for j in range(9)] == esper and esper[0] == 0 and sum(esper) == 45, f"cuotas {esper} · ne {inf2['ne']}")
    chk("las entradas del linaje j son SUS muestras (MARGEN = fabrica + j)", all(abs(g['MARGEN'] - fab[0] - round(g['MARGEN'] - fab[0])) < 1e-12 for g in s2)
        and sorted(set(round(g['MARGEN'] - fab[0]) for g in s2)) == [j for j in range(9) if esper[j] > 0])
    tel3 = copy.deepcopy(tel)
    for j in range(9): tel3[str(j)]['partos'] = 9 if j == 3 else 0
    s3, _ = CL.siembra_prop(tel3, 5, 5)
    chk("un linaje con todos los partos se lleva toda la siembra (ciclando sus 5 muestras)", len(s3) == 45 and all(round(g['MARGEN'] - fab[0]) == 3 for g in s3)
        and s3[:5] == s3[5:10])
    tel4 = copy.deepcopy(tel)
    for j in range(9): tel4[str(j)]['partos'] = 0
    s4, i4 = CL.siembra_prop(tel4, 5, 5)
    chk("sin partos -> siembra igualada (declarado)", s4 == E.siembra(tel4, 5, 5) and i4['prop'] == 0)
    # (i)
    log("(i) regla 14: prueba del runner == corre_o1_evo.trabajo('prueba')")
    dE = os.path.join(tmp, 'pe'); dM = os.path.join(tmp, 'pm'); os.makedirs(dE); os.makedirs(dM)
    cad = dict(tipo='cadena', i=0, aborto=None, siembra_final=sie)
    json.dump(dict(cad, brazo='o1pas'), open(os.path.join(dE, 'cadena_i00_o1pas.json'), 'w', encoding='utf-8'))
    json.dump(dict(cad, brazo='sel'), open(os.path.join(dM, 'cadena_i00_sel.json'), 'w', encoding='utf-8'))
    bp = (0, 624959)
    ye = E.trabajo(('prueba', 0, 'o1pas', bp, 0, 0, 2000, dE, False)); ym = R.trabajo(('prueba', 0, 'sel', bp, 0, 0, 2000, dM, False))
    q = lambda y: {k: v for k, v in sin_seg(js(y)).items() if k != 'brazo'}
    chk("O1_PAS con siembra: salida identica (menos seg y el nombre del brazo)", q(ye) == q(ym) and ye['aborto'] is None, f"claves {len(q(ye))}")
    ye = E.trabajo(('prueba', 0, 'o1', bp, 0, 0, 2000, dE, False)); ym = R.trabajo(('prueba', 0, 'o1', bp, 0, 0, 2000, dM, False))
    chk("O1 de fabrica: salida identica", q(ye) == q(ym) and ye['aborto'] is None)
finally:
    shutil.rmtree(tmp, ignore_errors=True)
# (j)
log("(j) LA LETRA en casos sinteticos (n = 5)")
def caso(sel, neu, igual=(7,) * 5, o1=(7,) * 5, dsel=0.1, dneu=0.01, col_igual=0, may_o1=1, sube_sel=5):
    Cc = {b: {} for b in R.CADENAS}; Rr = {b: {} for b in R.ORDEN}
    for b in R.CADENAS:
        for i in range(5):
            if b == 'sel': d = dsel if i < sube_sel else -dsel
            elif b == 'neu': d = dneu * (1 if i % 2 else -1)
            else: d = 0.0
            g = dict(E.FABRICA); g['MARGEN'] += d
            prop = 0 if b == 'igual' else 1
            q = dict(genes_siembra=g, cruzan=0, estado=dict(lee=R.BRAZOS[b][1], sigma=0.03, carro='O1_PAS'),
                     camara=dict(colonos_total=(col_igual if b == 'igual' else 3), fundadores_total=5, partos=[1] * 9),
                     siembra_info=(dict(prop=1, n_por_linaje={'0': 10, '1': 35}, ne=1.6) if prop else dict(prop=0)))
            Cc[b][i] = dict(pasajes=[q])
    for b, v in (('sel', sel), ('neu', neu), ('igual', igual), ('o1', o1)):
        for i in range(5):
            Rr[b][i] = dict(cruzan=v[i], mayoria=(may_o1 if b == 'o1' else int(v[i] >= 5)), coherente=True, fund_n=4, fund_de_siembra=(0 if b == 'o1' else 4),
                            estado=dict(lee=1, sigma=0.03, carro=('O1' if b == 'o1' else 'O1_PAS')), R0_med=0.9, fund=[1] * 9, fund_post10k=[0] * 9,
                            mundo_AC=1.0, genes_vivos_fin=dict(E.FABRICA))
    return R.lee_explora(Cc, Rr, 5, 0)
L = caso((8,) * 5, (6,) * 5); chk("FUNCIONA: sel > neu 5/5, MARGEN +0.1 en 5/5 (neu 0.01), sel > igual 5/5", L['veredicto'] == 'FUNCIONA' and L['matiz'] is None, str(L['puertas']))
L = caso((8,) * 5, (6,) * 5, igual=(8, 8, 7, 7, 7)); chk("H-1: sel > igual 3/5 justo (empates 2 en contra) -> FUNCIONA", L['veredicto'] == 'FUNCIONA' and L['puertas']['P4_sel_gana_igual'])
L = caso((8,) * 5, (6,) * 5, igual=(8, 8, 8, 7, 7)); chk("H-1: P1 y P2 con sel > igual 2/5 -> MODESTO (seleccion sobre genes, no atribuible a la camara)",
    L['veredicto'] == 'HAY ALGO MODESTO' and L['matiz'] == 'seleccion sobre genes, no atribuible a la camara' and not L['puertas']['P4_sel_gana_igual'])
L = caso((8,) * 5, (6,) * 5, igual=(9,) * 5); chk("H-1: P1 y P2 con sel < igual 5/5 -> MODESTO con matiz", L['veredicto'] == 'HAY ALGO MODESTO' and L['matiz'] is not None)
L = caso((8,) * 5, (6,) * 5, dneu=0.06); chk("P1 sin P2 (|sel| 0.1 < 2 x 0.06) -> MODESTO", L['veredicto'] == 'HAY ALGO MODESTO' and not L['puertas']['P2_direccional'])
L = caso((8, 8, 8, 6, 6), (6,) * 5, sube_sel=3); chk("sel > neu 3/5 -> MODESTO (y en el umbral)", L['veredicto'] == 'HAY ALGO MODESTO' and L['en_umbral'])
L = caso((6, 6, 6, 6, 11), (6,) * 5); chk("sel > neu 1/5 pero suma +5 -> MODESTO", L['veredicto'] == 'HAY ALGO MODESTO')
L = caso((7, 6, 6, 6, 6), (6,) * 5); chk("sel > neu 1/5, suma +1 -> NO", L['veredicto'] == 'NO')
L = caso((7, 7, 6, 6, 7), (6, 6, 6, 6, 7)); chk("H-4: sel > neu 2/5 y dif 2 < 4 -> NO", L['veredicto'] == 'NO')
L = caso((7, 7, 6, 6, 8), (6, 6, 7, 6, 6)); chk("H-4: sel > neu 3/5 (dif 3) -> MODESTO (frontera de NO: <= 2/5 y dif < 4)", L['veredicto'] == 'HAY ALGO MODESTO')
L = caso((8,) * 5, (6,) * 5, sube_sel=3); chk("signo 3/5 -> P2 no pasa -> MODESTO", L['veredicto'] == 'HAY ALGO MODESTO')
L = caso((8,) * 5, (6,) * 5, may_o1=0); chk("o1 sin mayoria -> NO APLICA", L['veredicto'] == 'NO APLICA')
L = caso((8,) * 5, (6,) * 5, col_igual=2); chk("colonos en 'igual' -> NO APLICA (V5)", L['veredicto'] == 'NO APLICA')
Cc_ = {b: {} for b in R.CADENAS}; Rr_ = {b: {} for b in R.ORDEN}
chk("vacio -> NO APLICA", R.lee_explora(Cc_, Rr_, 5, 0)['veredicto'] == 'NO APLICA')
# (k)
log("(k) candados del runner")
for argv, nom in ((['--explora', '--pool', '3'], '--pool 3'), (['--explo'], 'bandera abreviada')):
    try:
        R.main(argv); ok = False
    except SystemExit: ok = True
    chk(f"el runner niega {nom}", ok)
log(f"\nARNES: {'PASA' if all(RES) else 'FALLA'} ({sum(RES)}/{len(RES)}) · {time.time() - t0:.0f}s")
open(os.path.join(AQUI, 'identidad_entre_linajes_salida.txt'), 'w', encoding='utf-8').write('\n'.join(SAL) + '\n')
