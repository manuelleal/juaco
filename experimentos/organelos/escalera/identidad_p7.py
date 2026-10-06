"""identidad_p7.py — ARNES del peldano 7 (SENAL por la pizarra sobre O1_LUGAR, con costo de emitir). Un proceso; semillas de practica
739750-739759. NADA de aqui es dato.
(K) shas fijados (pista, juez, O1, corre_v143; corre_p1 CONGELADO; construye_p1 y el texto de O1_LUGAR por sha; mundo_escalera por sha) +
    carros en disco == construye_p7 + chequeo estatico revisa_carro + identidad corta del runner.
(M) MUNDO: mundo_tramo_c con c_e 0 == mundo_escalera BIT A BIT (salida entera, rng); c_e 0.01 con un carro que no escribe == c_e 0 (linajes,
    salvo el contador 'cobros' = 0); c_e 0.01 con SENAL: cobros == escrituras aceptadas por linaje y la fisica != c_e 0 (el costo actua).
(C) CARRO: SENAL0 == O1_LUGAR (salida entera, mundo P1b); SENAL con la pizarra apagada == O1_LUGAR (mudo == base); SENAL != O1_LUGAR con
    pizarra (el canal actua: escrituras y siembras > 0); SENAL_BAR != SENAL y != O1_LUGAR, y en SENAL_BAR ningun linaje que solo oyo (sin
    morder) tiene bono en el oasis (lee el antipoda: siembra siempre el lugar equivocado).
(m) MECANISMO: en SENAL, los linajes que solo oyeron tienen sus bins con bono DENTRO del oasis; latencia por vida registrada.
(a) regla 14: corre_p7.tarea('lug', c_e 0) == corre_p1.tarea('lug') campo a campo (salvo lo agregado); corre_p1.tarea('o1f') == corre_v143.tarea.
(e) trabajo() escribe su JSON; --reanuda relee igual; brazo desconocido aborta dentro (nube-9).
(f) la letra en casos sinteticos (8 casos). (g) guardas: semillas disjuntas y en 7396xx-7397xx; banderas desconocidas abortan; --humo con
    --pool aborta; --pool 3 aborta; --serie con --T aborta; el humo y la exploracion caben en un proceso.
Uso: python experimentos/organelos/escalera/identidad_p7.py [--corto]
"""
import copy, importlib.util, json, os, sys, tempfile, time

AQUI = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, AQUI)
import corre_p7 as C7R
import construye_p7 as C7
CO = C7R.CO; ME = C7R.ME; MC = C7R.MC; CV = C7R.CV
sys.path.insert(0, CO.PISTA); import revisa_carro as RC

N = lambda x: json.loads(json.dumps(x, default=str))
OK = [True]; NCHK = [0, 0]
CORTO = '--corto' in sys.argv
T = 800 if CORTO else 4000


def chk(nombre, c):
    c = bool(c); OK[0] &= c; NCHK[0] += 1; NCHK[1] += int(c); print(f"  {'OK   ' if c else 'FALLA'} {nombre}", flush=True)


def carga(n):
    spec = importlib.util.spec_from_file_location('c_' + n, C7R.CARROS[n]); m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m


def lin(r, quita=('sn_escribe', 'sn_lee', 'sn_siembra'), quita_oasis=('latencia_vida', 'cobros')):
    r = copy.deepcopy(r['linajes'])
    for d in r:
        for k in quita: d['carro'].pop(k, None)
        for k in quita_oasis: (d['_carrera'].get('oasis') or {}).pop(k, None)
    return N(r)


KW = dict(pizarra=1, rep_acum=0, escala=1, mundo_n=None, fundador_limpio=1, **CO.MUNDO_OASIS)
def run(m, seed, **k): return N(MC.run(seed, [('X', m)] * 9, T=T, **dict(KW, **k)))


t0 = time.time()
print(f"ARNES identidad_p7.py (T {T}{' CORTO' if CORTO else ''})")
chk("(K) verifica(): shas fijados (pista, juez, O1, corre_v143, corre_p1), carros P1 == construye_p1, carros P7 == construye_p7, mundos construidos", C7R.verifica(lambda s: print('   ', s)))
C7.verifica_origen(); chk(f"(K) construye_p1.py sha == {C7.SHA_CONSTRUYE_P1} y texto de O1_LUGAR == {C7.SHA_O1_LUGAR}", True)
chk(f"(K) mundo_escalera.py sha == {MC.SHAS_FIJOS['mundo_escalera']}", MC.construye()[1]['sha_mundo_escalera'] == MC.SHAS_FIJOS['mundo_escalera'])
for n, b in C7.todas().items():
    v = RC.revisa_fuente(b.decode('utf-8'), n); chk(f"(K) chequeo estatico {n}: {'PASA' if not v else v[:2]}", not v)
chk("(K) identidad corta de corre_p1 (mundo oasis 0 == pista; O1_LUGAR0 == O1; O1_LUGAR sin oasis == O1)", CO.identidad_corta(lambda s: print('   ', s), T=min(T, 1500)))
chk("(K) identidad corta de corre_p7 (c_e 0 == mundo_escalera; SENAL0 == O1_LUGAR; SENAL con pizarra 0 == O1_LUGAR)", C7R.identidad_corta(lambda s: print('   ', s), T=min(T, 1500)))
lug = carga('O1_LUGAR'); s0 = carga('O1_LUGAR_SENAL0'); sen = carga('O1_LUGAR_SENAL'); sb = carga('O1_LUGAR_SENAL_BAR')
S = 739751
# (M)
base = N(ME.run(S, [('X', lug)] * 9, T=T, **KW)); r0 = run(lug, S)
chk(f"(M) mundo_tramo_c c_e 0 == mundo_escalera BIT A BIT (salida entera, s {S}, T {T}) y mismo rng final", r0 == base and r0['pista']['rng_mundo_estado'] == base['pista']['rng_mundo_estado'])
r1 = run(lug, S, c_e=C7R.C_E)
chk(f"(M) c_e {C7R.C_E} con O1_LUGAR (no escribe) == c_e 0 en los linajes (salvo 'cobros' = 0) y rng",
    lin(r1) == lin(r0) and all(d['_carrera']['oasis']['cobros'] == 0 for d in r1['linajes']) and r1['pista']['rng_mundo_estado'] == r0['pista']['rng_mundo_estado'])
c0 = run(sen, S); c1 = run(sen, S, c_e=C7R.C_E)
cob = [d['_carrera']['oasis']['cobros'] for d in c1['linajes']]; esc_ = [d['_carrera']['escrituras'] for d in c1['linajes']]
chk(f"(M) c_e {C7R.C_E} con SENAL: cobros por linaje {cob} == escrituras aceptadas {esc_}; fisica != c_e 0 (el costo actua)", cob == esc_ and sum(cob) > 0 and lin(c1) != lin(c0))
# (C)
chk(f"(C) SENAL0 == O1_LUGAR BIT A BIT (salida entera, mundo P1b, s {S}, T {T})", run(s0, S) == r0)
e = run(sen, S, pizarra=0, c_e=C7R.C_E); f = run(lug, S, pizarra=0)
chk(f"(C) SENAL con la pizarra apagada (y c_e) == O1_LUGAR en los linajes (mudo == base; escrituras descartadas {e['pista']['escrituras_descartadas']})", lin(e) == lin(f))
sie = [d['carro']['sn_siembra'] for d in c1['linajes']]
chk(f"(C) SENAL != O1_LUGAR con pizarra (el canal actua): escrituras {esc_} (> 0), siembras {sie} (> 0)", lin(c1) != lin(r1) and sum(esc_) > 0 and sum(sie) > 0)
d1 = run(sb, S, c_e=C7R.C_E)
ob = set(c1['pista']['oasis']['bins30']); bb = [x['carro']['lugar']['bins_con_bono'] for x in d1['linajes']]
fuera = [i for i, x in enumerate(d1['linajes']) if x['carro']['sn_siembra'] > 0 and x['carro']['lg_apr'] == 0 and any(z in ob for z in bb[i])]
chk(f"(C) SENAL_BAR != SENAL y != O1_LUGAR; siembras BAR {[x['carro']['sn_siembra'] for x in d1['linajes']]}; bins con bono {bb} vs oasis {sorted(ob)}: "
    f"ningun linaje que solo oyo (sin morder) tiene bono en el oasis ({len(fuera)} lo tienen)", lin(d1) != lin(c1) and lin(d1) != lin(r1) and not fuera)
# (m)
bs = [x['carro']['lugar']['bins_con_bono'] for x in c1['linajes']]; solo_oyen = [i for i, x in enumerate(c1['linajes']) if x['carro']['sn_siembra'] > 0 and x['carro']['lg_apr'] == 0]
den = sum(1 for i in solo_oyen if bs[i] and all(z in ob for z in bs[i]))
chk(f"(m) SENAL: los linajes que SOLO oyeron (sin morder) {solo_oyen} tienen todos sus bins con bono DENTRO del oasis ({den}/{len(solo_oyen)}; bins {[bs[i] for i in solo_oyen]} vs oasis {sorted(ob)})",
    den == len(solo_oyen))
lat = [d['_carrera']['oasis']['latencia_vida'] for d in c1['linajes']]
chk(f"(m) latencia por vida registrada en SENAL (vidas con bocado dentro: {[len(z) for z in lat]}; todas en [0, T])", sum(len(z) for z in lat) > 0 and all(0 <= v <= T for z in lat for v in z))
# (a) regla 14
sin = lambda x: N({k: v for k, v in x.items() if k not in ('seg', 'estado', 'tel')})
x7 = C7R.tarea(739752, 'lug', 2000, mundo=dict(CO.MUNDO_OASIS, c_e=0.0)); x1 = CO._tarea_completa(739752, 'lug', 2000)   # la que captura _oasis (corre_p1.trabajo la usa)
def q7(x):
    x = copy.deepcopy(x)
    for l in x['linajes']:
        if l.get('_oasis'): l['_oasis'].pop('latencia_vida', None); l['_oasis'].pop('cobros', None)
    return sin(x)
chk("(a) regla 14: corre_p7.tarea('lug', c_e 0) == corre_p1.tarea('lug') campo a campo (s 739752, T 2000; salvo seg/estado/tel)", q7(x7) == q7(x1))
y = CO.tarea(739752, 'o1f', 2000); z = CV.tarea((739752, 'O1', 2000))
chk("(a) regla 14 (cadena): corre_p1.tarea('o1f') == corre_v143.tarea campo a campo", sin(y) == sin(z))
chk("(a) el runner deja pista.run como estaba", CO.P.run is CV.P.run and 'run2' not in repr(CO.P.run))
# (e)
with tempfile.TemporaryDirectory() as td:
    x1 = C7R.trabajo((0, 'sen', 739753, 2000, td, False))
    chk(f"(e) trabajo sen sin aborto ({x1['aborto']}); fila con oasis, pizarra (escr {x1.get('pizarra', {}).get('escrituras_total')}, cobros {x1.get('pizarra', {}).get('cobros_total')}), senal, latencia y estado (c_e {x1.get('estado', {}).get('mundo', {}).get('c_e')})",
        x1['aborto'] is None and x1.get('oasis') and x1['pizarra']['cobros_total'] == x1['pizarra']['escrituras_total'] and x1['estado']['carro'] == 'O1_LUGAR_SENAL'
        and x1['estado']['mundo'] == C7R.MUNDO_P7 and x1['estado']['SENAL'] == 1 and x1['estado']['SN_BARAJA'] == 0 and 'latencia' in x1)
    x2 = C7R.trabajo((0, 'sen', 739753, 2000, td, True))
    chk("(e) --reanuda relee igual", N({k: v for k, v in x1.items() if k != 'seg'}) == N({k: v for k, v in x2.items() if k != 'seg'}))
    x3 = C7R.trabajo((0, 'lug', 739753, 2000, td, False))
    chk("(e) trabajo lug: sin escrituras ni cobros; estado SENAL 0", x3['aborto'] is None and x3['pizarra']['escrituras_total'] == 0 and x3['pizarra']['cobros_total'] == 0 and x3['estado']['SENAL'] == 0)
    x4 = C7R.trabajo((0, 'zzz', 739753, 2000, td, False))
    chk("(e) brazo desconocido -> aborto escrito (nube-9)", x4['aborto'] is not None and os.path.exists(os.path.join(td, 'prueba_i00_zzz.json')))


# (f) letra sintetica
def sint(cz, n=20, fund=None, lat=None, aborto=0, escr=None):
    """lat = fraccion de vidas con bocado dentro (PM, H-9: mayor gana); la latencia queda fija (descriptivo)."""
    R = {}
    for b in C7R.ORDEN:
        R[b] = {}
        for i in range(n):
            c = cz.get(b, [7] * n)[i]
            fm = (fund or {}).get(b, [10] * n)[i]; lt = (lat or {}).get(b, [0.5] * n)[i]
            es = (escr or {}).get(b, 5 if b != 'lug' else 0)
            est = dict(carro=C7R.BRAZOS[b][0], mundo=C7R.BRAZOS[b][1], LUGAR=1, LUGAR_BARAJA=0, SENAL=int(b != 'lug'), SN_BARAJA=int(b == 'senbar'))
            R[b][i] = dict(cruzan=c, mayoria=int(c * 2 > 9), R0_med=0.9, coherente=True, fund=[fm] * 9, fund_media=float(fm), fund_post10k=[0] * 9,
                           oasis=dict(mord_AC_dentro=5, extra=ME.EXTRA, pobre=ME.POBRE, ratio_pasos=3.0, ratio_mord=1.0), estado=est, vida_med=1000,
                           mundo_AC=2.0, mord_AC=100, mord_BD=10, lugar=None, T=100000,
                           pizarra=dict(escrituras=[es] * 9, escrituras_total=es * 9, cobros=[es] * 9, cobros_total=es * 9, c_e=C7R.C_E),
                           senal=(dict(sn_escribe=es * 9, sn_lee=5, sn_siembra=2) if b != 'lug' else None), lat_med=500.0, frac_vidas=float(lt),
                           latencia=dict(med=500.0, n=10, vidas=20, frac_vidas=float(lt)))
    return C7R.lee_serie(R, n, aborto)


V = lambda L: L['veredicto']
G = {'sen': [8] * 20}; F = {'sen': [5] * 20}; LT = {'sen': [0.8] * 20}
chk("(f) FUNCIONA: sen 8 contra 7 (lug y senbar) 20/20, menos fundadores, llegan mas vidas al oasis (0.8 vs 0.5)", V(sint(G, fund=F, lat=LT)) == 'FUNCIONA')
chk("(f) NO: sen == lug == senbar en todo", V(sint({})) == 'NO')
chk("(f) NO: gana a lug pero no a senbar (el canal con contenido equivocado iguala: lo que paga es hablar, no el contenido)", V(sint({'sen': [8] * 20, 'senbar': [8] * 20}, fund=F, lat=LT)) == 'NO')
L = sint(G, fund=F, lat=None)
chk(f"(f) gana cruce y fundadores pero NO llegan mas vidas (PM): {V(L)} ({L['matiz']})", V(L) == 'NO' and 'instrumento' in (L['matiz'] or ''))
L = sint({'sen': [9] * 12 + [7] * 8}, fund=F, lat=LT)
chk(f"(f) MODESTO: cruce solo por suma (gana 12, +24), fundadores y PM si: {V(L)} umbral {L['en_umbral']}", V(L) == 'HAY ALGO MODESTO' and L['en_umbral'])
L = sint({}, fund=F, lat=LT)
chk(f"(f) NO: fundadores y PM mejores pero cruce igual a lug Y a senbar (PB cae): {V(L)}", V(L) == 'NO')
chk("(f) NO SE LEE: un aborto", V(sint(G, fund=F, lat=LT, aborto=1)) == 'NO SE LEE')
chk("(f) NO SE LEE: el canal no actua (0 escrituras en sen)", V(sint(G, fund=F, lat=LT, escr={'sen': 0})) == 'NO SE LEE')
# (g)
ser = set(range(C7R.SEM['serie'], C7R.SEM['serie'] + 20)); rep = set(range(C7R.SEM['replica'], C7R.SEM['replica'] + 20))
exp = set(range(C7R.SEM['explora'], C7R.SEM['explora'] + 6)); hum = set(range(C7R.SEM['humo'], C7R.SEM['humo'] + 6)); pra = set(range(739750, 739760))
p1 = set(range(739001, 739021)) | set(range(739101, 739121)) | set(range(739201, 739207)) | set(range(739990, 739996)) | set(range(739950, 739990))
todo = [ser, rep, exp, hum, pra]
chk("(g) semillas: serie, replica, explora, humo y arnes disjuntas entre si y de las de P1, y en 7396xx-7397xx",
    all(not (a & b) for i, a in enumerate(todo) for b in todo[i + 1:]) and not (set.union(*todo) & p1) and all(739600 <= s < 739800 for s in set.union(*todo)))


def aborta(argv):
    try: C7R.main(argv); return False
    except SystemExit: return True


chk("(g) banderas desconocidas o abreviadas abortan (--hum, --humo --x)", aborta(['--hum']) and aborta(['--humo', '--x']))
chk("(g) --humo con --pool aborta; --pool 3 aborta; --serie --T aborta; --humo --n 3 (9 corridas) aborta; --explora --T 250000 aborta",
    aborta(['--humo', '--pool', '2']) and aborta(['--serie', '--pool', '3']) and aborta(['--serie', '--T', '1000']) and aborta(['--humo', '--n', '3']) and aborta(['--explora', '--T', '250000']))
chk(f"(g) el humo cabe: {len(C7R.RAFAGA) * C7R.HUMO['n']} corridas de {C7R.HUMO['T']} · la exploracion: {len(C7R.RAFAGA) * C7R.EXPLORA['n']} de {C7R.EXPLORA['T']}",
    len(C7R.RAFAGA) * C7R.HUMO['n'] <= 6 and C7R.HUMO['T'] <= 200000 and len(C7R.RAFAGA) * C7R.EXPLORA['n'] <= 6 and C7R.EXPLORA['T'] <= 200000)
print(f"\nARNES {'PASA' if OK[0] else 'FALLA'}, {NCHK[1]}/{NCHK[0]} · {time.time() - t0:.1f}s")
sys.exit(0 if OK[0] else 1)
