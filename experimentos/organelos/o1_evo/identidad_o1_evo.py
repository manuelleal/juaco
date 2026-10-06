"""identidad_o1_evo.py — ARNES del confirmatorio o1_evo (O1 con perillas heredables). Un proceso; semillas de practica 617950-617989.
(K) shas fijados + carros == construye_o1_pas + identidad corta del runner.
(a) regla 14: tarea(o1 / termo / v143) == corre_v143.tarea campo a campo (salvo 'seg', 'tel_ps', 'estado').
(b) SALIDA ENTERA de pista.run (N 9, fundador limpio): O1_PAS0 == O1; O1_PAS con sigma 0 y SIEMBRA None == O1; con SIEMBRA de genes de
    fabrica == O1. Y por el juez: o1ctl con sigma 0 == o1 (linajes y pista, ids normalizados).
(c) CABLEADO: O1_PAS con sigma 0 y SIEMBRA = genes X == O1_MANO (el texto de O1.py con las 4 constantes cambiadas a X, por anclas, aqui) en la
    salida ENTERA; y != O1 (los genes actuan: control que puede fallar).
(d) HERENCIA: con sigma 0 todos los vivos llevan exactamente X; con sigma 0.03 los genes se mueven, quedan en el clip, hay partos; la salida != O1.
(n) NEUTRO (o1neu): con PS_LEE 0 (genes heredados, mutados y transferidos pero NO leidos) y sigma 0.03 y siembra X, la salida ENTERA == O1, y los
    genes igual se mueven en la telemetria; la cadena o1neu funda de su siembra, escribe lee 0 por pasaje, y su prueba lee (lee 1).
(e) cadena de 2 pasajes: el pasaje 1 funda TODO de la siembra; trabajo() escribe su JSON y --reanuda lo relee igual (tambien desde los JSON
    por pasaje); la prueba o1pas lee la siembra de SU cadena; la o1ctl no usa siembra; o1pas sin cadena -> aborto.
(f) LA LETRA en casos sinteticos.
(g) guardas: semillas disjuntas y en 617xxx; banderas desconocidas/abreviadas abortan; --humo con --pool aborta; --pool 5 aborta; el humo cabe.
(h) la ruta de Pool (apply_async; la prueba o1pas se encola al terminar su cadena) con un Pool FALSO de un proceso; candado; regla de parada; --lee.
"""
import copy, importlib.util, inspect, json, os, shutil, sys, tempfile, time, types

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
import corre_o1_evo as CO
CV = CO.CV; P = CO.P

N = lambda x: json.loads(json.dumps(x, default=str))
OK = [True]; NCHK = [0, 0]


def chk(nombre, c):
    c = bool(c); OK[0] &= c; NCHK[0] += 1; NCHK[1] += int(c); print(f"  {'OK   ' if c else 'FALLA'} {nombre}", flush=True)


def sin(x): return N({k: v for k, v in x.items() if k not in ('seg', 'tel_ps', 'estado')})
def run(mod, seed, T): return N(P.run(seed, [('X', mod)] * 9, T=T, pizarra=1, rep_acum=0, escala=1, mundo_n=None, fundador_limpio=1))


def con(m, siembra, sigma, seed, lee=1):
    m.SIEMBRA = copy.deepcopy(siembra); m.PS_SIGMA = sigma; m.PS_SEMILLA = seed; m.PS_LEE = lee; m._TEL.clear(); m._PS_CNT.clear()


def o1_mano(X):
    """O1.py con las 4 constantes cambiadas a X (anclas exactas, una vez cada una), como modulo en memoria."""
    src = open(os.path.join(CO.PISTA, 'carros', 'O1.py'), encoding='utf-8').read()
    lit = {'MARGEN': 'MARGEN = 0.25      #', 'PRUEBA': 'PRUEBA = 0.5       #', 'PEN_OTRO': 'PEN_OTRO = 0.35    #', 'PISO': 'PISO = 0.2         #'}
    for k, a in lit.items():
        assert src.count(a) == 1, k
        src = src.replace(a, f"{k} = {X[k]!r}  #")
    m = types.ModuleType('O1_MANO'); exec(compile(src, 'O1_MANO', 'exec'), m.__dict__); return m


t0 = time.time()
print("ARNES identidad_o1_evo.py")
chk("(K) verifica(): shas fijados y carros == construye_o1_pas", CO.verifica(lambda s: print('   ', s)))
chk("(K) identidad corta del runner (O1_PAS0 y O1_PAS sigma 0 == O1)", CO.identidad_corta(lambda s: print('   ', s)))
o1 = CV.modulo('O1')
chk("(K) los genes de fabrica del constructor son las constantes de O1.py", all(getattr(o1, k) == v for k, v in CO.FABRICA.items()))
# (a)
for b in ('o1', 'termo', 'v143'):
    x = CO.tarea(617951, b, 2000); y = CV.tarea((617951, CO.BRAZOS[b][0], 2000))
    chk(f"(a) regla 14: tarea({b}) == corre_v143.tarea campo a campo (s 617951, T 2000)", sin(x) == sin(y) and set(sin(x)) == set(sin(y)))
# (b)
CO.fija('o1pas'); m = CV._MODS['O1_PAS']
spec = importlib.util.spec_from_file_location('carro_O1_PAS0', CO.O1PAS0_PY); m0 = importlib.util.module_from_spec(spec); spec.loader.exec_module(m0)
S, T = 617952, 3000
base = run(o1, S, T)
chk(f"(b) O1_PAS0 == O1 (salida ENTERA, s {S}, T {T})", run(m0, S, T) == base)
con(m, None, 0.0, S); r1 = run(m, S, T)
chk("(b) O1_PAS sigma 0 SIEMBRA None == O1 (salida ENTERA)", r1 == base)
tel = copy.deepcopy(m._TEL)
chk("(b)   ...y la telemetria dice: fundadores de FABRICA (de_siembra 0) con genes de fabrica exactos",
    all(f[0] == 0 and f[1] == list(CO.CB.FABRICA) for v in tel.values() for f in v.get('fund', [])) and sum(len(v.get('fund', [])) for v in tel.values()) >= 9)
con(m, [dict(CO.FABRICA)] * 4, 0.0, S); chk("(b) O1_PAS sigma 0 SIEMBRA de fabrica == O1 (salida ENTERA)", run(m, S, T) == base)
con(m, None, 0.03, 0)
x = CO.tarea(617953, 'o1ctl', 2000, sigma=0.0); y = CO.tarea(617953, 'o1', 2000)
norm = lambda z: json.loads(json.dumps(N({k: z[k] for k in ('linajes', 'pista', 'R0_pista')})).replace('O1_PAS#', 'O1#'))
chk("(b) por el juez: o1ctl con sigma 0 == o1 (linajes, pista, R0_pista; ids normalizados; s 617953, T 2000)", norm(x) == norm(y))
chk("(b)   ...y el estado escrito dice carro O1_PAS, PASAJE 1, sigma 0", x['estado']['carro'] == 'O1_PAS' and x['estado']['PASAJE'] == 1 and x['estado']['sigma'] == 0.0)
# (c) cableado
X = dict(MARGEN=0.40, PRUEBA=0.35, PEN_OTRO=0.60, PISO=0.30)
S2 = 617954
mano = run(o1_mano(X), S2, T); con(m, [dict(X)] * 5, 0.0, S2); rX = run(m, S2, T); telX = copy.deepcopy(m._TEL)
chk(f"(c) O1_PAS sigma 0 SIEMBRA X == O1_MANO(X) (salida ENTERA, s {S2}, T {T}); X = {X}", rX == mano)
chk("(c) control que puede fallar: con X la salida != O1 (los genes actuan)", rX != run(o1, S2, T))
# (d) herencia
vv = [g for v in telX.values() for _, g in v.get('vivos', [])]
chk(f"(d) sigma 0: los {len(vv)} vivos muestreados llevan exactamente X; todos los fundadores de siembra",
    len(vv) >= 9 and all(g == [X[k] for k in CO.GENES] for g in vv) and all(f[0] == 1 for v in telX.values() for f in v.get('fund', [])))
con(m, None, 0.03, S2); r3 = run(m, S2, T); tel3 = copy.deepcopy(m._TEL); con(m, None, 0.03, 0)
g3 = [g for v in tel3.values() for _, g in v.get('vivos', [])]
chk(f"(d) sigma 0.03: los genes se mueven ({len(g3)} vivos; ninguno exactamente de fabrica) y quedan en el clip",
    len(g3) >= 9 and all(g != list(CO.CB.FABRICA) for g in g3)
    and all(CO.CB.CLIP[j][0] <= g[j] <= CO.CB.CLIP[j][1] for g in g3 for j in range(4)))
chk(f"(d) sigma 0.03: hay partos con genes ({sum(v.get('partos', 0) for v in tel3.values())}) y la salida != O1", sum(v.get('partos', 0) for v in tel3.values()) > 0 and r3 != base)
# (n) neutro
con(m, [dict(X)] * 5, 0.03, S2, lee=0); rN = run(m, S2, T); telN = copy.deepcopy(m._TEL); con(m, None, 0.03, 0, lee=1)
gN = [g for v in telN.values() for _, g in v.get('vivos', [])]
chk(f"(n) PS_LEE 0, sigma 0.03, SIEMBRA X: salida ENTERA == O1 (s {S2}, T {T}): los genes NO se leen", rN == run(o1, S2, T))
chk(f"(n)   ...pero se heredan y mutan igual ({len(gN)} vivos, ninguno == X exacto; partos {sum(v.get('partos', 0) for v in telN.values())})",
    len(gN) >= 9 and all(g != [X[k] for k in CO.GENES] for g in gN) and sum(v.get('partos', 0) for v in telN.values()) > 0)
chk("(n) el runner deja PS_LEE en 1 tras cada tarea", (CO.tarea(617955, 'o1neu', 500, siembra=[dict(X)], lee=0) is not None) and m.PS_LEE == 1)
# (e) cadena
base_h = (617960, 617980)
with tempfile.TemporaryDirectory() as td:
    x1 = CO.trabajo(('cadena', 0, 'o1pas', base_h, 2, 3000, 3000, td, False))
    ps = x1.get('pasajes') or [{}, {}]
    chk(f"(e) cadena de 2 pasajes sin aborto ({x1['aborto']}); pasaje 0 de fabrica ({ps[0].get('fund_de_siembra')}/{ps[0].get('fund_n')}), "
        f"pasaje 1 TODO de la siembra ({ps[1].get('fund_de_siembra')}/{ps[1].get('fund_n')})",
        x1['aborto'] is None and ps[0]['fund_de_siembra'] == 0 and ps[1]['fund_n'] > 0 and ps[1]['fund_de_siembra'] == ps[1]['fund_n'])
    chk(f"(e) la siembra final es la del ultimo pasaje (n {len(x1['siembra_final'] or [])} = n_siembra {ps[1].get('n_siembra')})",
        len(x1['siembra_final'] or []) == ps[1]['n_siembra'] > 0)
    x2 = CO.trabajo(('cadena', 0, 'o1pas', base_h, 2, 3000, 3000, td, True))
    chk("(e) --reanuda relee la cadena igual", N({k: v for k, v in x1.items() if k != 'seg'}) == N({k: v for k, v in x2.items() if k != 'seg'}))
    os.remove(os.path.join(td, 'cadena_i00_o1pas.json'))
    x3 = CO.trabajo(('cadena', 0, 'o1pas', base_h, 2, 3000, 3000, td, True))
    chk("(e) --reanuda rehace la cadena desde los JSON por pasaje, igual", N({k: v for k, v in x1.items() if k != 'seg'}) == N({k: v for k, v in x3.items() if k != 'seg'}))
    y1 = CO.trabajo(('prueba', 0, 'o1pas', base_h, 2, 3000, 3000, td, False))
    chk(f"(e) la prueba o1pas usa la siembra de SU cadena (genes {y1.get('genes_siembra_usada')}; de siembra {y1.get('fund_de_siembra')}/{y1.get('fund_n')})",
        y1['aborto'] is None and y1['genes_siembra_usada'] == CO.genes_de(x1['siembra_final']) and y1['fund_de_siembra'] == y1['fund_n'] > 0)
    y2 = CO.trabajo(('prueba', 0, 'o1ctl', base_h, 2, 3000, 3000, td, False))
    chk(f"(e) la prueba o1ctl no usa siembra ({y2.get('fund_de_siembra')}/{y2.get('fund_n')}) y su fisica difiere de o1pas",
        y2['aborto'] is None and y2['fund_de_siembra'] == 0 and y2['fund_n'] > 0 and (y2['cruza'], y2['fund'], y2['R0_real']) != (y1['cruza'], y1['fund'], y1['R0_real']))
    xn = CO.trabajo(('cadena', 0, 'o1neu', base_h, 2, 3000, 3000, td, False))
    pn_ = xn.get('pasajes') or [{}, {}]
    chk(f"(e) cadena o1neu: mismas semillas de pasaje que o1pas {[q.get('seed') for q in pn_]}, lee 0 en cada pasaje, pasaje 1 TODO de su siembra "
        f"({pn_[1].get('fund_de_siembra')}/{pn_[1].get('fund_n')})",
        xn['aborto'] is None and [q['seed'] for q in pn_] == [q['seed'] for q in ps] and all(q['estado']['lee'] == 0 for q in pn_)
        and all(q['estado']['lee'] == 1 for q in ps) and pn_[1]['fund_de_siembra'] == pn_[1]['fund_n'] > 0)
    chk("(e) el pasaje 0 de o1neu es O1 de fabrica en el juez (== prueba o1 con la misma semilla y T)",
        (lambda o: pn_[0]['cruza'] == o['cruza'] and pn_[0]['fund'] == o['fund'] and pn_[0]['R0_real'] == o['R0_real'])(CO.fila(CO.tarea(pn_[0]['seed'], 'o1', 3000), 3000)))
    yn = CO.trabajo(('prueba', 0, 'o1neu', base_h, 2, 3000, 3000, td, False))
    chk(f"(e) la prueba o1neu usa la siembra de SU cadena y LEE los genes (lee {(yn.get('estado') or {}).get('lee')}; de siembra {yn.get('fund_de_siembra')}/{yn.get('fund_n')})",
        yn['aborto'] is None and yn['genes_siembra_usada'] == CO.genes_de(xn['siembra_final']) and yn['estado']['lee'] == 1
        and yn['fund_de_siembra'] == yn['fund_n'] > 0)
    chk("(e) genes por linaje en la fila de la prueba (9 linajes, media y ultimo)", len(y1.get('genes_linaje') or []) == 9
        and all(g is None or set(g) == {'media', 'ultimo'} for g in y1['genes_linaje']))
    z1 = CO.trabajo(('prueba', 1, 'o1pas', base_h, 2, 3000, 3000, td, False))
    chk("(e) prueba o1pas sin cadena -> aborto (nube-9), no se inventa siembra", z1['aborto'] is not None)
chk("(e) siembra() solo recibe la telemetria de genes (ni R0, ni hijos, ni cruza)", list(inspect.signature(CO.siembra).parameters) == ['tel', 'T', 'vent'])


# (f) LA LETRA en casos sinteticos
def sint(cz, may_o1=None, v143=0.6, aborto=0, sie_ok=True, n=20, neu_sie=True, neu_lee=0):
    """cz: {brazo: lista de 20 'cruzan'}; el resto por defecto."""
    R = {}
    for b in CO.ORDEN:
        R[b] = {}
        for i in range(n):
            c = cz.get(b, [7] * n)[i]
            may = int(c * 2 > 9) if may_o1 is None or b != 'o1' else int(i < may_o1)
            fs = 9 if ((b == 'o1pas' and sie_ok) or (b == 'o1neu' and neu_sie)) else 0
            R[b][i] = dict(cruzan=c, mayoria=may, R0_med=(v143 if b == 'v143' else 0.9), coherente=True, fund=[1] * 9, fund_post10k=[0] * 8 + [3],
                           fund_n=9, fund_de_siembra=fs, mundo_AC=2.0, genes_linaje=[dict(media=dict(CO.FABRICA), ultimo=dict(CO.FABRICA))] * 9,
                           estado=dict(carro=CO.BRAZOS[b][0], sigma=CO.BRAZOS[b][3], lee=(1 if CO.BRAZOS[b][0] == 'O1_PAS' else None)),
                           genes_vivos_fin=dict(CO.FABRICA))
    C = {b: {i: dict(pasajes=[dict(genes_siembra=dict(CO.FABRICA), cruzan=7, fund=[1] * 9, seed=0,
                                   estado=dict(lee=(1 if b == 'o1pas' else neu_lee), sigma=0.03))] * 10) for i in range(n)} for b in CO.CADENAS}
    return CO.lee_serie(C, R, n, aborto)


V = lambda L: L['veredicto']
chk("(f) FUNCIONA: o1pas 8 contra 7 (o1, ctl y neu) en 20/20", V(sint({'o1pas': [8] * 20})) == 'FUNCIONA')
L = sint({'o1pas': [9] * 12 + [7] * 8})   # gana 12, dif 24
chk(f"(f) MODESTO solo la suma (gana 12/20, +24): {V(L)} · y queda EN EL UMBRAL (12 = 13 - 1): {L['en_umbral']}", V(L) == 'HAY ALGO MODESTO' and L['en_umbral'])
L = sint({'o1pas': [9] * 10 + [7] * 10})   # gana 10, dif 20
chk(f"(f) MODESTO solo la suma lejos del umbral (gana 10, +20): {V(L)}, umbral {L['en_umbral']}", V(L) == 'HAY ALGO MODESTO' and not L['en_umbral'])
L = sint({'o1pas': [8] * 15 + [5] * 5})    # gana 15, dif 15 - 10 = 5
chk(f"(f) MODESTO solo lo pareado (gana 15, +5): {V(L)}", V(L) == 'HAY ALGO MODESTO' and not L['en_umbral'])
chk("(f) NO: o1pas == o1 == ctl (empates EN CONTRA)", V(sint({})) == 'NO')
chk("(f) NO: gana a o1 pero NO a ctl (la mutacion sola basta)", V(sint({'o1pas': [8] * 20, 'o1ctl': [8] * 20})) == 'NO')
chk("(f) NO: gana a ctl pero NO a o1", V(sint({'o1pas': [8] * 20, 'o1': [8] * 20, 'o1ctl': [6] * 20})) == 'NO')
chk("(f) umbral exacto: gana 13 con +13 -> FUNCIONA y EN EL UMBRAL", (lambda L: V(L) == 'FUNCIONA' and L['en_umbral'])(sint({'o1pas': [8] * 13 + [7] * 7})))
chk("(f) umbral de la suma: +9 con gana 9 -> NO y EN EL UMBRAL", (lambda L: V(L) == 'NO' and L['en_umbral'])(sint({'o1pas': [8] * 9 + [7] * 11})))
chk("(f) NO SE LEE: un aborto", V(sint({'o1pas': [8] * 20}, aborto=1)) == 'NO SE LEE')
chk("(f) NO SE LEE: O1 con mayoria en 15/20 (V2)", V(sint({'o1pas': [8] * 20}, may_o1=15)) == 'NO SE LEE')
chk("(f) V2 pasa con 16/20", V(sint({'o1pas': [8] * 20}, may_o1=16)) == 'FUNCIONA')
chk("(f) NO SE LEE: v143 fuera de banda (0.35, V3)", V(sint({'o1pas': [8] * 20}, v143=0.35)) == 'NO SE LEE')
chk("(f) NO SE LEE: la siembra no actua en o1pas (V4)", V(sint({'o1pas': [8] * 20}, sie_ok=False)) == 'NO SE LEE')
# (L) casos nuevos por auditoria: el brazo neutro o1neu y las puertas PN
L = sint({'o1pas': [8] * 20, 'o1neu': [8] * 20})
chk(f"(L) PA, PB, PC pasan pero PN no (o1neu == o1pas): {V(L)} ({L['matiz']})", V(L) == 'HAY ALGO MODESTO' and L['matiz'] == 'transferencia, no seleccion')
L = sint({'o1pas': [8] * 20, 'o1neu': [8] * 10 + [7] * 10})   # PN par 10/20 (no), PN suma +10 (si)
chk(f"(L) PN a medias (par 10/20, suma +10): {V(L)} ({L['matiz']}) y EN EL UMBRAL (suma = 10)", V(L) == 'HAY ALGO MODESTO' and L['matiz'] == 'transferencia, no seleccion' and L['en_umbral'])
L = sint({'o1pas': [8] * 20, 'o1neu': [6] * 20})
chk(f"(L) PN pasa y todo pasa: {V(L)} (o1neu por debajo de o1: la deriva sola cuesta)", V(L) == 'FUNCIONA' and L['matiz'] is None)
L = sint({'o1pas': [9] * 10 + [7] * 10, 'o1neu': [6] * 20})
chk(f"(L) PA/PC a medias y PN completo: {V(L)} ({L['matiz']})", V(L) == 'HAY ALGO MODESTO' and L['matiz'] == 'seleccion parcial')
chk("(L) NO: gana o1neu, no o1pas (o1pas == o1)", V(sint({'o1neu': [8] * 20})) == 'NO')
L = sint({'o1pas': [8] * 20, 'o1neu': [8] * 6 + [7] * 14})   # PN par 14 (+-1 de 13)
chk(f"(L) EN EL UMBRAL tambien por PN (par 14/20): {L['en_umbral']}, {V(L)}", L['en_umbral'] and V(L) == 'FUNCIONA')
chk("(L) NO SE LEE: la siembra no actua en o1neu (V4)", V(sint({'o1pas': [8] * 20}, neu_sie=False)) == 'NO SE LEE')
chk("(L) NO SE LEE: la cadena o1neu con lee 1 (V5: el neutro no fue neutro)", V(sint({'o1pas': [8] * 20}, neu_lee=1)) == 'NO SE LEE')
L = sint({'o1pas': [8] * 20})
chk(f"(L) descriptivo: genes por linaje cruzados con fund_post10k ({L['descriptivo']['genes_linaje_vs_establecimiento']['o1pas']['n_establecidos']} establecidos, "
    f"{L['descriptivo']['genes_linaje_vs_establecimiento']['o1pas']['n_no']} no)",
    L['descriptivo']['genes_linaje_vs_establecimiento']['o1pas']['n_establecidos'] == 160 and L['descriptivo']['genes_linaje_vs_establecimiento']['o1pas']['n_no'] == 20)
chk("(f) bloque: FUNCIONA + MODESTO -> MODESTO; NO SE LEE manda", CO.bloque('FUNCIONA', 'HAY ALGO MODESTO') == 'HAY ALGO MODESTO'
    and CO.bloque('FUNCIONA', 'NO SE LEE') == 'NO SE LEE')
# (g) guardas
ser = {CO.sem_pas(CO.BASES['serie'], i, p) for i in range(20) for p in range(10)} | {CO.sem_pru(CO.BASES['serie'], i) for i in range(20)}
rep = {CO.sem_pas(CO.BASES['replica'], i, p) for i in range(20) for p in range(10)} | {CO.sem_pru(CO.BASES['replica'], i) for i in range(20)}
pra = set(range(617900, 618000))
chk(f"(g) semillas: serie {len(ser)}, replica {len(rep)}, practica disjuntas y en 617xxx", len(ser) == len(rep) == 220 and not (ser & rep) and not (ser & pra)
    and not (rep & pra) and all(617000 <= s < 618000 for s in ser | rep) and CO.HUMO['base'][0] in pra and CO.HUMO['base'][1] in pra)


def aborta(argv):
    try: CO.main(argv); return False
    except SystemExit: return True


chk("(g) banderas desconocidas o abreviadas abortan (--ser, --humo --x)", aborta(['--ser']) and aborta(['--humo', '--x']))
chk("(g) --humo con --pool aborta; --pool 5 aborta", aborta(['--humo', '--pool', '2']) and aborta(['--serie', '--pool', '5']))
H = CO.HUMO
n1 = 2 * H['npas'] + 2; p1 = 2 * H['npas'] * H['T_pas'] + 2 * H['T_pru']; p2 = 4 * H['T_pru']
chk(f"(g) el humo cabe: proceso 1 = 2 cadenas x {H['npas']} pasajes + 2 pruebas = {n1} corridas, {p1} pasos; proceso 2 = 4 corridas, {p2} pasos",
    n1 <= 6 and p1 <= 200000 and p2 <= 200000)


# (h) la ruta de Pool del runner (apply_async + la prueba o1pas encolada al terminar su cadena), con un Pool FALSO de UN proceso
class _R:
    def __init__(self, v): self.v = v
    def ready(self): return True
    def get(self): return self.v


class FalsoPool:
    def __init__(self, n): self.n = n
    def __enter__(self): return self
    def __exit__(self, *a): return False
    def apply_async(self, f, args): return _R(f(*args))


import multiprocessing
guarda_mp = multiprocessing.Pool; guarda = (CO.DATOS, CO.N_IND, CO.NPAS, CO.T_PAS, CO.T_PRU, CO.git_limpio)
with tempfile.TemporaryDirectory() as td:
    try:
        multiprocessing.Pool = FalsoPool
        CO.DATOS = td; CO.N_IND = 1; CO.NPAS = 2; CO.T_PAS = 2000; CO.T_PRU = 2000; CO.git_limpio = lambda rutas, log: True
        r1 = CO.main(['--serie', '--pool', '4'])
        cs = [d for d in os.listdir(td) if d.startswith('serie_')]
        fs = sorted(os.listdir(os.path.join(td, cs[0]))) if cs else []
        rs = json.load(open(os.path.join(td, cs[0], 'resumen.json'), encoding='utf-8')) if cs else {}
        chk(f"(h) --serie --pool 4 (Pool FALSO, 1 indice, 2 pasajes, T 2000): termina; archivos {fs}",
            r1 == 0 and len(cs) == 1 and all(f"{t}.json" in fs for t in ('cadena_i00_o1pas', 'cadena_i00_o1neu', 'prueba_i00_o1pas', 'prueba_i00_o1neu',
                                                                          'prueba_i00_o1ctl', 'prueba_i00_o1', 'prueba_i00_termo', 'prueba_i00_v143',
                                                                          'pasaje_i00_o1pas_p00', 'pasaje_i00_o1pas_p01', 'pasaje_i00_o1neu_p00',
                                                                          'pasaje_i00_o1neu_p01', 'resumen'))
            and rs.get('modo') == 'serie' and not rs.get('abortos'))
        chk("(h) candado: --serie otra vez sin --reanuda se niega (hay carpeta)", CO.main(['--serie', '--pool', '4']) == 1)
        vs = (rs.get('letra') or {}).get('veredicto'); um = (rs.get('letra') or {}).get('en_umbral')
        chk(f"(h) regla de parada: --replica se niega (serie = {vs}, umbral {um})", (vs == 'NO SE LEE' or (vs == 'NO' and not um)) and CO.main(['--replica', '--pool', '4']) == 1)
        chk("(h) --lee relee la carpeta", CO.main(['--lee', os.path.join(td, cs[0])]) == 0)
    finally:
        multiprocessing.Pool = guarda_mp; CO.DATOS, CO.N_IND, CO.NPAS, CO.T_PAS, CO.T_PRU, CO.git_limpio = guarda
print(f"\nARNES {'PASA' if OK[0] else 'FALLA'}, {NCHK[1]}/{NCHK[0]} · {time.time() - t0:.1f}s")
sys.exit(0 if OK[0] else 1)
