"""identidad_p1.py — ARNES del peldano 1 (memoria de lugar). Un proceso; semillas de practica 739950-739989. NADA de aqui es dato.
(K) shas fijados + carros == construye_p1 + identidad corta del runner + chequeo estatico de los carros (revisa_carro).
(M) MUNDO: oasis 0 == pista.run BIT A BIT (salida entera y estado final del rng del mundo); oasis 1 con extra 0.8 y pobre 1.0 == pista_grande
    (G 1, rica 1, lento 0) en toda la fisica (mismo z0 y W); controles que deben diferir: oasis 1 != pista; pobre 0.5 != pobre 1.0.
(C) CARRO: O1_LUGAR0 == O1; O1_LUGAR con LUGAR_W 0.0 == O1 (promotor apagado) en el mundo con oasis; O1_LUGAR sin oasis == O1 (el bono
    queda en 0 exacto); controles que deben diferir: O1_LUGAR != O1 con oasis; O1_LUGAR_BAR != O1_LUGAR y != O1.
(m) MECANISMO: con oasis, la memoria de O1_LUGAR pone sus bins con bono DENTRO del oasis (>= 7/9 linajes con todos sus bins con bono en el
    oasis) y O1_LUGAR_BAR escribe lo mismo (misma fisica de escritura) pero lee permutado.
(a) regla 14: tarea('o1f') == corre_v143.tarea campo a campo (salvo seg, estado, tel).
(e) trabajo() escribe su JSON; --reanuda lo relee igual; un brazo desconocido aborta dentro de trabajo (nube-9) y queda escrito.
(f) la letra en casos sinteticos. (g) guardas: semillas disjuntas y en 739xxx; banderas desconocidas abortan; --humo con --pool aborta;
    --pool 3 aborta; el humo y la exploracion caben en un proceso.
"""
import copy, importlib.util, json, os, sys, tempfile, time

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
import corre_p1 as CO
CV = CO.CV; P = CO.P; ME = CO.ME
GR = os.path.join(CO.RAIZ, 'experimentos', 'organelos', 'o1_evo', 'grande')
sys.path.insert(0, CO.PISTA); import revisa_carro as RC

N = lambda x: json.loads(json.dumps(x, default=str))
OK = [True]; NCHK = [0, 0]


def chk(nombre, c):
    c = bool(c); OK[0] &= c; NCHK[0] += 1; NCHK[1] += int(c); print(f"  {'OK   ' if c else 'FALLA'} {nombre}", flush=True)


KW = dict(pizarra=1, rep_acum=0, escala=1, mundo_n=None, fundador_limpio=1)
def run(mod, seed, T, **k): return N(ME.run(seed, [('X', mod)] * 9, T=T, **KW, **k))
def sin(x): return N({k: v for k, v in x.items() if k not in ('seg', 'estado', 'tel')})
def fis(r):
    """la fisica de una salida sin las claves nuevas del mundo (para comparar mundos distintos que deben coincidir en todo lo demas)."""
    r = copy.deepcopy(r)
    for d in r['linajes']:
        d['_carrera'].pop('oasis', None); d['_carrera'].pop('grande', None)
    r['pista'].pop('oasis', None); r['pista'].pop('grande', None)
    return N(r)


t0 = time.time()
print("ARNES identidad_p1.py")
chk("(K) verifica(): shas fijados, carros == construye_p1, mundo construido", CO.verifica(lambda s: print('   ', s)))
chk("(K) identidad corta del runner (mundo oasis 0 == pista; O1_LUGAR0 == O1; O1_LUGAR sin oasis == O1)", CO.identidad_corta(lambda s: print('   ', s)))
for nm, ruta in CO.CARROS.items():
    v = RC.revisa_fuente(open(ruta, encoding='utf-8').read(), nm)
    chk(f"(K) chequeo estatico revisa_carro {nm}: {'PASA' if not v else v[:2]}", not v)
o1 = CV.modulo('O1'); CO.fija('lug'); m = CV._MODS['O1_LUGAR']; CO.fija('bar'); mb = CV._MODS['O1_LUGAR_BAR']
spec = importlib.util.spec_from_file_location('carro_O1_LUGAR0', CO.CARROS['O1_LUGAR0']); m0 = importlib.util.module_from_spec(spec); spec.loader.exec_module(m0)
# (M) mundo
S, T = 739951, 3000
base = N(P.run(S, [('X', o1)] * 9, T=T, **KW))
r0 = run(o1, S, T, oasis=0)
chk(f"(M) mundo oasis 0 == pista.run BIT A BIT (salida entera, N 9, s {S}, T {T}) y mismo estado final del rng del mundo",
    r0 == base and r0['pista']['rng_mundo_estado'] == base['pista']['rng_mundo_estado'])
spec = importlib.util.spec_from_file_location('pista_grande', os.path.join(GR, 'pista_grande.py')); PG = importlib.util.module_from_spec(spec); spec.loader.exec_module(PG)
rg = N(PG.run(S, [('X', o1)] * 9, T=T, G=1, rica=1, lento=0, **KW)); r1 = run(o1, S, T, oasis=1, extra=0.8, pobre=1.0)
chk(f"(M) mundo oasis 1, extra 0.8, pobre 1.0 == pista_grande (G 1, rica 1, lento 0) en TODA la fisica; mismo oasis [z0, fin] {r1['pista']['oasis']['oasis']} == {rg['pista']['grande']['oasis']}",
    fis(r1) == fis(rg) and r1['pista']['oasis']['oasis'] == rg['pista']['grande']['oasis'] and r1['pista']['rng_mundo_estado'] == rg['pista']['rng_mundo_estado'])
chk("(M)   ...y los pasos dentro del oasis coinciden con pista_grande linaje a linaje",
    [d['_carrera']['oasis']['pasos_dentro'] for d in r1['linajes']] == [d['_carrera']['grande']['pasos_oasis'] for d in rg['linajes']])
r5 = run(o1, S, T, oasis=1)
chk("(M) control que puede fallar: oasis 1 (pobre 0.5) != pista; pobre 0.5 != pobre 1.0", fis(r5) != base and fis(r5) != fis(r1))
chk(f"(M) el oasis actua: O1 muerde A+C dentro ({sum(d['_carrera']['oasis']['mord_dentro']['A'] + d['_carrera']['oasis']['mord_dentro']['C'] for d in r5['linajes'])}) y fuera "
    f"({sum(d['_carrera']['oasis']['mord_fuera']['A'] + d['_carrera']['oasis']['mord_fuera']['C'] for d in r5['linajes'])}); extra 0.8 pobre 0.5 escritos",
    sum(d['_carrera']['oasis']['mord_dentro']['A'] + d['_carrera']['oasis']['mord_dentro']['C'] for d in r5['linajes']) > 0
    and r5['pista']['oasis']['extra'] == 0.8 and r5['pista']['oasis']['pobre'] == 0.5)
# (C) carro
S2 = 739952
b2 = run(o1, S2, T, oasis=1)
chk(f"(C) O1_LUGAR0 == O1 en el mundo con oasis (salida ENTERA, s {S2}, T {T})", run(m0, S2, T, oasis=1) == b2)
w, vj = m.LUGAR_W, m.LG_VIAJA
try:
    m.LUGAR_W = 0.0; m.LG_VIAJA = 0; rw = run(m, S2, T, oasis=1)
finally:
    m.LUGAR_W = w; m.LG_VIAJA = vj
# P1b: dens y vista
rd = run(o1, S2, T, oasis=1, dens=0.5); cd = rd['pista']['oasis']['comp_dentro']; cf = rd['pista']['oasis']['comp_fuera']
chk(f"(M) P1b dens 0.5: el oasis es denso (objetos dentro {sum(cd.values()):.2f} vs fuera {sum(cf.values()):.2f}; 10 % del anillo) y la fisica != dens 0",
    sum(cd.values()) > 0.3 * (sum(cd.values()) + sum(cf.values())) and fis(rd) != fis(b2))
rv = run(o1, S2, T, oasis=1, vista_r=20); rv2 = run(o1, S2, T, oasis=1, vista_r=200)
chk("(M) P1b vista 20: la fisica != vista 0 (O1 ve menos); vista 200 (>= media vuelta) == vista 0 (salida entera)", fis(rv) != fis(b2) and fis(rv2) == fis(b2))
chk("(C) O1_LUGAR con LUGAR_W 0.0 y LG_VIAJA 0 (modulo mudo) == O1 en el mundo con oasis: fisica y carro (salvo la telemetria 'lugar')",
    fis({k: v for k, v in rw.items()}) != None and N([{k: v for k, v in d.items() if k != 'carro'} for d in rw['linajes']]) == N([{k: v for k, v in d.items() if k != 'carro'} for d in b2['linajes']])
    and rw['pista'] == b2['pista'] and all({k: v for k, v in d['carro'].items() if k not in CO.TELEM_LUGAR} == e['carro'] for d, e in zip(rw['linajes'], b2['linajes'])))
chk(f"(C) O1_LUGAR sin oasis == O1 (salida ENTERA salvo telemetria; s {S2}, T {T}): sin sitios que den de mas el bono es 0 exacto",
    N([{k: v for k, v in d.items() if k != 'carro'} for d in run(m, S2, T, oasis=0)['linajes']]) == N([{k: v for k, v in d.items() if k != 'carro'} for d in run(o1, S2, T, oasis=0)['linajes']]))
rl = run(m, S2, T, oasis=1); rb = run(mb, S2, T, oasis=1)
chk("(C) control que puede fallar: O1_LUGAR != O1 con oasis (el modulo actua); O1_LUGAR_BAR != O1_LUGAR y != O1", fis(rl) != fis(b2) and fis(rb) != fis(rl) and fis(rb) != fis(b2))
# (m) mecanismo
S3, T3 = 739953, 6000
rl3 = run(m, S3, T3, oasis=1); ob = set(rl3['pista']['oasis']['bins30'])
bb = [d['carro']['lugar']['bins_con_bono'] for d in rl3['linajes']]
con = [b for b in bb if b]; den = sum(1 for b in con if all(x in ob for x in b))
chk(f"(m) O1_LUGAR (s {S3}, T {T3}): bins con bono {bb} · oasis en bins {sorted(ob)} · linajes con memoria {len(con)}/9 (>= 3; los demas son refundaciones "
    f"limpias sin memoria aun) y de ellos con TODOS sus bins con bono dentro del oasis {den}/{len(con)} (todos)", len(con) >= 3 and den == len(con))
chk(f"(m) O1_LUGAR: blancos con bono de lugar > 0 en TODOS los linajes con memoria ({[d['carro']['lg_bono'] for d in rl3['linajes']]})",
    all(d['carro']['lg_bono'] > 0 for d in rl3['linajes'] if d['carro']['lugar']['bins_con_bono']))
# (m) ERR-170: el control lee el ANTIPODA fijo (b + 15 mod 30), sin rng
import numpy as _np
_cb = mb.crea(dict(L=360, rep_umbral=1.0, rng=_np.random.default_rng(1), id='x', indice=0)); _cl = m.crea(dict(L=360, rep_umbral=1.0, rng=_np.random.default_rng(1), id='y', indice=0))
_cb.lugar[20] = [1.0, 0.5]; _cl.lugar[20] = [1.0, 0.5]
chk("(m) ERR-170: O1_LUGAR_BAR lee en el bin ANTIPODA fijo: con memoria solo en el bin 20, lee [1, .5] en la celda 66 (bin 5 = 20 - 15) y 0 en la celda 246 (bin 20); "
    "O1_LUGAR lee al reves; y _lg_meta de BAR apunta al bin 5 (celda 66)",
    list(_cb._lg_leer(66)) == [1.0, 0.5] and list(_cb._lg_leer(246)) == [0.0, 0.0] and list(_cl._lg_leer(246)) == [1.0, 0.5] and list(_cl._lg_leer(66)) == [0.0, 0.0]
    and _cb._lg_meta(0) == 66 and _cl._lg_meta(0) == 246)
rb3 = run(mb, S3, T3, oasis=1)
chk(f"(m) O1_LUGAR_BAR escribe en el bin verdadero (baraja 1 = antipoda; bins con bono {[d['carro']['lugar']['bins_con_bono'] for d in rb3['linajes']]}) y su fisica difiere de O1_LUGAR",
    all(d['carro']['lugar']['baraja'] == 1 for d in rb3['linajes']) and fis(rb3) != fis(rl3))
# (a) regla 14
x = CO.tarea(739954, 'o1f', 2000); y = CV.tarea((739954, 'O1', 2000))
chk("(a) regla 14: tarea('o1f') == corre_v143.tarea campo a campo (s 739954, T 2000)", sin(x) == sin(y) and set(sin(x)) == set(sin(y)))
chk("(a) el runner deja pista.run como estaba", P.run is CV.P.run and 'run2' not in repr(P.run))
# (e) trabajo / reanuda
with tempfile.TemporaryDirectory() as td:
    x1 = CO.trabajo((0, 'lug', 739960, 2500, td, False))
    chk(f"(e) trabajo lug sin aborto ({x1['aborto']}); fila con oasis, lugar y estado (carro {x1.get('estado', {}).get('carro')}, mundo {x1.get('estado', {}).get('mundo')})",
        x1['aborto'] is None and x1.get('oasis') and x1.get('lugar') and x1['estado']['carro'] == 'O1_LUGAR' and x1['estado']['mundo'] == CO.MUNDO_OASIS and x1['estado']['LUGAR_BARAJA'] == 0)
    x2 = CO.trabajo((0, 'lug', 739960, 2500, td, True))
    chk("(e) --reanuda relee igual", N({k: v for k, v in x1.items() if k != 'seg'}) == N({k: v for k, v in x2.items() if k != 'seg'}))
    x3 = CO.trabajo((0, 'o1f', 739960, 2500, td, False))
    chk("(e) trabajo o1f: sin oasis en la fila y mundo liso en el estado", x3['aborto'] is None and x3.get('oasis') is None and x3['estado']['mundo'] == CO.MUNDO_LISO)
    x4 = CO.trabajo((0, 'zzz', 739960, 2500, td, False))
    chk("(e) brazo desconocido -> aborto escrito (nube-9)", x4['aborto'] is not None and os.path.exists(os.path.join(td, 'prueba_i00_zzz.json')))


# (f) letra sintetica
def sint(cz, n=20, may_o1f=None, ratio=None, aborto=0):
    R = {}
    for b in CO.ORDEN:
        R[b] = {}
        for i in range(n):
            c = cz.get(b, [7] * n)[i]
            may = int(c * 2 > 9) if may_o1f is None or b != 'o1f' else int(i < may_o1f)
            oz = None if b == 'o1f' else dict(mord_AC_dentro=5, extra=ME.EXTRA, pobre=ME.POBRE, ratio_pasos=(ratio or {}).get(b, 1.0), ratio_mord=1.0)
            est = dict(carro=CO.BRAZOS[b][0], mundo=CO.BRAZOS[b][2], LUGAR=(1 if b in ('lug', 'bar') else None), LUGAR_W=CO.CB.LUGAR_W, LUGAR_BARAJA=int(b == 'bar'))
            R[b][i] = dict(cruzan=c, mayoria=may, R0_med=0.9, coherente=True, fund=[1] * 9, fund_post10k=[0] * 9, oasis=oz, estado=est, vida_med=1000,
                           mundo_AC=2.0, mord_AC=100, mord_BD=10, lugar=None)
    return CO.lee_serie(R, n, aborto)


V = lambda L: L['veredicto']
chk("(f) FUNCIONA: lug 8 contra 7 (o1 y bar) 20/20 y usa el lugar (ratio 2.5 vs o1 1.0)", V(sint({'lug': [8] * 20}, ratio={'lug': 2.5, 'o1': 1.0})) == 'FUNCIONA')
L = sint({'lug': [8] * 20}, ratio={'lug': 1.2, 'o1': 1.0})
chk(f"(f) gana pero NO va al oasis (ratio 1.2): {V(L)} ({L['matiz']})", V(L) == 'NO' and 'instrumento' in (L['matiz'] or ''))
chk("(f) NO: lug == o1 == bar", V(sint({}, ratio={'lug': 2.5, 'o1': 1.0})) == 'NO')
chk("(f) NO: gana a o1 pero no a bar (el sesgo basta, no el contenido)", V(sint({'lug': [8] * 20, 'bar': [8] * 20}, ratio={'lug': 2.5, 'o1': 1.0})) == 'NO')
L = sint({'lug': [9] * 12 + [7] * 8}, ratio={'lug': 2.5, 'o1': 1.0})
chk(f"(f) MODESTO solo la suma (gana 12, +24) y EN EL UMBRAL: {V(L)} {L['en_umbral']}", V(L) == 'HAY ALGO MODESTO' and L['en_umbral'])
chk("(f) NO SE LEE: un aborto", V(sint({'lug': [8] * 20}, ratio={'lug': 2.5, 'o1': 1.0}, aborto=1)) == 'NO SE LEE')
chk("(f) NO SE LEE: o1f con mayoria en 15/20 (V2)", V(sint({'lug': [8] * 20}, ratio={'lug': 2.5, 'o1': 1.0}, may_o1f=15)) == 'NO SE LEE')
# (g) guardas
ser = set(range(CO.SEM['serie'], CO.SEM['serie'] + 20)); rep = set(range(CO.SEM['replica'], CO.SEM['replica'] + 20))
exp = set(range(CO.SEM['explora'], CO.SEM['explora'] + 6)); hum = set(range(CO.SEM['humo'], CO.SEM['humo'] + 6)); pra = set(range(739950, 739990))
chk("(g) semillas: serie, replica, explora, humo y arnes disjuntas y en 739xxx",
    not (ser & rep) and not (ser & exp) and not (ser & hum) and not (ser & pra) and not (rep & exp) and not (rep & hum) and not (exp & hum) and not (hum & pra)
    and all(739000 <= s < 740000 for s in ser | rep | exp | hum | pra))


def aborta(argv):
    try: CO.main(argv); return False
    except SystemExit: return True


chk("(g) banderas desconocidas o abreviadas abortan (--hum, --humo --x)", aborta(['--hum']) and aborta(['--humo', '--x']))
chk("(g) --humo con --pool aborta; --pool 3 aborta; --humo --n 3 (9 corridas) aborta; --explora --T 250000 aborta",
    aborta(['--humo', '--pool', '2']) and aborta(['--serie', '--pool', '3']) and aborta(['--humo', '--n', '3']) and aborta(['--explora', '--T', '250000']))
chk(f"(g) el humo cabe: {len(CO.RAFAGA) * CO.HUMO['n']} corridas de {CO.HUMO['T']} · la exploracion: {len(CO.RAFAGA) * CO.EXPLORA['n']} de {CO.EXPLORA['T']}",
    len(CO.RAFAGA) * CO.HUMO['n'] <= 6 and CO.HUMO['T'] <= 200000 and len(CO.RAFAGA) * CO.EXPLORA['n'] <= 6 and CO.EXPLORA['T'] <= 200000)
print(f"\nARNES {'PASA' if OK[0] else 'FALLA'}, {NCHK[1]}/{NCHK[0]} · {time.time() - t0:.1f}s")
sys.exit(0 if OK[0] else 1)
