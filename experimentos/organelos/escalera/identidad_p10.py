"""identidad_p10.py — ARNES del peldano 10 (PREGUNTA sobre O1_LUGAR en el mundo que se muda). Un proceso; semillas de practica 739880-739889.
(K) shas (pista, juez, O1, corre_v143; corre_p1 congelado; construye_p1; mundo_escalera; mundo_tramo_c; construye_c y corre_c si fijados) +
    carros PREG == construye_c + chequeo estatico + identidades cortas (corre_p1, corre_c, corre_p10).
(M) mueve 0 == mundo_escalera BIT A BIT; mueve T/3: 3 epocas, el oasis final != inicial, latencias registradas por linaje y epoca, los objetos
    nuevos nacen en el oasis NUEVO (composicion dentro > 0 tras la mudanza); mueve T/3 != mueve 0 (actua).
(C) PREG0 == O1_LUGAR (salida entera, con mueve); PREG != O1_LUGAR; PREG_BAR != PREG y != O1_LUGAR; PREG con PG_OLVIDO 0 y sin excursiones
    (promotor 1, piezas mudas) == O1_LUGAR en la fisica (el modulo apagado por sus perillas tambien es la base).
(m) PREG explora (pg_exc > 0) y olvida (pg_olv > 0); PREG_BAR explora igual (pg_exc > 0): mismas excursiones, otro destino.
(a) regla 14: corre_p10.trabajo('lug', mueve 0) fila == corre_p1 fila (campo a campo salvo lo agregado: preg, oasis_info, estado).
(e) trabajo escribe JSON; --reanuda relee; brazo desconocido aborta dentro. (f) letra sintetica (8 casos). (g) guardas y semillas.
Uso: python experimentos/organelos/escalera/identidad_p10.py [--corto]
"""
import copy, json, os, sys, tempfile, time

AQUI = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, AQUI)
import corre_p10 as C10
CR = C10.CR; CO = C10.CO; ME = C10.ME; MC = C10.MC; CC = C10.CC
sys.path.insert(0, CO.PISTA); import revisa_carro as RC

N = lambda x: json.loads(json.dumps(x, default=str))
OK = [True]; NCHK = [0, 0]
CORTO = '--corto' in sys.argv
T = 900 if CORTO else 4500


def chk(nombre, c):
    c = bool(c); OK[0] &= c; NCHK[0] += 1; NCHK[1] += int(c); print(f"  {'OK   ' if c else 'FALLA'} {nombre}", flush=True)


def fis(r):
    r = copy.deepcopy(r)
    for d in r['linajes']: d.pop('carro', None)
    return N(r)


KW = dict(pizarra=1, rep_acum=0, escala=1, mundo_n=None, fundador_limpio=1, **CO.MUNDO_OASIS)
def run(m, seed, **k): return N(MC.run(seed, [('X', m)] * 9, T=T, **dict(KW, **k)))


t0 = time.time()
print(f"ARNES identidad_p10.py (T {T}{' CORTO' if CORTO else ''})")
chk("(K) verifica(): shas, carros PREG == construye_c, mundo_tramo_c", C10.verifica(lambda s: print('   ', s)))
for n, b in CC.todas('preg').items():
    v = RC.revisa_fuente(b.decode('utf-8'), n); chk(f"(K) chequeo estatico {n}: {'PASA' if not v else v[:2]}", not v)
chk("(K) identidad corta corre_p1", CO.identidad_corta(lambda s: print('   ', s), T=min(T, 1500)))
chk("(K) identidad corta corre_c (mundo apagado == mundo_escalera; promotores 0 == O1_LUGAR)", CR.identidad_corta_c(lambda s: print('   ', s), T=min(T, 1200)))
chk("(K) identidad corta corre_p10 (mueve 0 == mundo_escalera; PREG0 == O1_LUGAR; el oasis se muda)", C10.identidad_corta(lambda s: print('   ', s), T=min(T, 1500)))
lug, _ = CR.modulo('O1_LUGAR'); p0, _ = CR.modulo('O1_LUGAR_PREG0'); pg, _ = CR.modulo('O1_LUGAR_PREG'); pb, _ = CR.modulo('O1_LUGAR_PREG_BAR')
S = 739881; MV = T // 3
base = N(ME.run(S, [('X', lug)] * 9, T=T, **KW)); r0 = run(lug, S)
chk(f"(M) mueve 0 == mundo_escalera BIT A BIT (salida entera, s {S}, T {T}) y rng", r0 == base and r0['pista']['rng_mundo_estado'] == base['pista']['rng_mundo_estado'])
rm = run(lug, S, mueve=MV); oz = rm['pista']['oasis']; lat = [d['_carrera']['oasis']['latencias'] for d in rm['linajes']]
chk(f"(M) mueve {MV}: mudanzas {oz['mudanzas']} (3 epocas), bins {oz['bins30']} -> {oz['bins30_final']} (distintos), latencias por linaje con 3 entradas {[len(z) for z in lat]}, fisica != mueve 0",
    len(oz['mudanzas']) == 3 and oz['bins30_final'] != oz['bins30'] and all(len(z) == 3 for z in lat) and fis(rm) != fis(r0))
cd = oz['comp_dentro']
chk(f"(M) tras las mudanzas el oasis actual tiene comida (composicion dentro A+C {cd['A'] + cd['C']:.2f} > 0) y se muerde dentro ({sum(d['_carrera']['oasis']['mord_dentro']['A'] + d['_carrera']['oasis']['mord_dentro']['C'] for d in rm['linajes'])})",
    cd['A'] + cd['C'] > 0 and sum(d['_carrera']['oasis']['mord_dentro']['A'] + d['_carrera']['oasis']['mord_dentro']['C'] for d in rm['linajes']) > 0)
# (C)
chk(f"(C) PREG0 == O1_LUGAR con mueve (salida entera)", run(p0, S, mueve=MV) == rm)
rp = run(pg, S, mueve=MV); rb = run(pb, S, mueve=MV)
chk("(C) PREG != O1_LUGAR; PREG_BAR != PREG y != O1_LUGAR (el modulo y el control actuan)", fis(rp) != fis(rm) and fis(rb) != fis(rp) and fis(rb) != fis(rm))
ol = pg.PG_OLVIDO
try:
    pg.PG_OLVIDO = 0.0
    rq = run(pg, S, mueve=MV)
finally:
    pg.PG_OLVIDO = ol
# con PG_OLVIDO 0 el contador pg_olv sigue contando OCASIONES (estar con hambre sin ver nada) pero la memoria no decae: se verifica que la fisica
# cambie respecto de PREG (la pieza (a) actuaba) y respecto de la base (la pieza (b) sigue actuando: pg_exc > 0)
chk(f"(C) PREG con PG_OLVIDO 0 (pieza (a) muda; ocasiones contadas {[d['carro'].get('pg_olv') for d in rq['linajes']][:3]}...): la (b) sigue (pg_exc > 0) y la fisica != base y != PREG",
    sum(d['carro'].get('pg_exc', 0) for d in rq['linajes']) > 0 and fis(rq) != fis(rm) and fis(rq) != fis(rp))
# (m)
ex = [d['carro'].get('pg_exc', 0) for d in rp['linajes']]; ov = [d['carro'].get('pg_olv', 0) for d in rp['linajes']]; exb = [d['carro'].get('pg_exc', 0) for d in rb['linajes']]
chk(f"(m) PREG explora {ex} y olvida {ov} (> 0); PREG_BAR explora {exb} (> 0); O1_LUGAR no tiene esas claves", sum(ex) > 0 and sum(ov) > 0 and sum(exb) > 0 and all('pg_exc' not in d['carro'] for d in rm['linajes']))
# (a) regla 14 a nivel de FILA: corre_p10 (mueve 0) vs corre_p1 (trabajo)
with tempfile.TemporaryDirectory() as td:
    x10 = C10.trabajo((0, 'lug', 739882, 2000, td, False, dict(CO.MUNDO_OASIS, mueve=0)))
    x1 = CO.trabajo((1, 'lug', 739881, 2000, td, False))   # base 739881 + i 1 = 739882
    def q(x, quita): return N({k: v for k, v in x.items() if k not in quita})
    quita = ('seg', 'estado', 'preg', 'oasis_info', 'i', 'tipo', 'brazo', 'aborto')
    chk("(a) regla 14 (fila): corre_p10.trabajo('lug', mueve 0) == corre_p1.trabajo('lug') campo a campo (s 739882, T 2000; salvo lo agregado)", q(x10, quita) == q(x1, quita) and x10['aborto'] is None)
    x2 = C10.trabajo((0, 'preg', 739882, 2000, td, False, dict(CO.MUNDO_OASIS, mueve=600)))
    chk(f"(e) trabajo preg: JSON escrito, fila con preg (latencia {x2.get('preg', {}).get('latencia_med')}, mudanzas {x2.get('preg', {}).get('mudanzas')}), estado PREGUNTA 1 PG_BARAJA 0",
        x2['aborto'] is None and os.path.exists(os.path.join(td, 'prueba_i00_preg.json')) and x2['preg']['mudanzas'] == 3 and x2['estado']['PREGUNTA'] == 1 and x2['estado']['PG_BARAJA'] == 0)
    x3 = C10.trabajo((0, 'preg', 739882, 2000, td, True, dict(CO.MUNDO_OASIS, mueve=600)))
    chk("(e) --reanuda relee igual", N({k: v for k, v in x2.items() if k != 'seg'}) == N({k: v for k, v in x3.items() if k != 'seg'}))
    x4 = C10.trabajo((0, 'zzz', 739882, 2000, td, False, dict(CO.MUNDO_OASIS, mueve=600)))
    chk("(e) brazo desconocido -> aborto escrito (nube-9)", x4['aborto'] is not None and os.path.exists(os.path.join(td, 'prueba_i00_zzz.json')))


# (f) letra sintetica
def sint(cz, n=20, fund=None, lat=None, aborto=0, exc=None, mud=4):
    R = {}
    for b in C10.ORDEN:
        R[b] = {}
        for i in range(n):
            c = cz.get(b, [7] * n)[i]; fm = (fund or {}).get(b, [10] * n)[i]; lt = (lat or {}).get(b, [1000] * n)[i]
            ex = (exc or {}).get(b, 100 if b != 'lug' else 0)
            est = dict(carro=C10.BRAZOS[b], mundo=dict(C10.MUNDO_P10), LUGAR=1, LUGAR_BARAJA=0)
            if b != 'lug': est.update(PREGUNTA=1, PG_BARAJA=int(b == 'pregbar'))
            R[b][i] = dict(cruzan=c, mayoria=int(c * 2 > 9), R0_med=0.9, coherente=True, fund=[fm] * 9, fund_media=float(fm), fund_post10k=[0] * 9,
                           oasis=dict(mord_AC_dentro=5, extra=ME.EXTRA, pobre=ME.POBRE, ratio_pasos=3.0, ratio_mord=1.0), estado=est, vida_med=1000,
                           mundo_AC=2.0, mord_AC=100, mord_BD=10, T=100000, oasis_info=dict(mueve=C10.MUEVE),
                           preg=dict(latencia_med=float(lt), latencias_n=36, nunca=0, mudanzas=mud, pg_exc=ex, pg_olv=ex), lat_med=float(lt))
    return C10.lee_serie(R, n, aborto)


V = lambda L: L['veredicto']
G = {'preg': [8] * 20}; F = {'preg': [5] * 20}; LT = {'preg': [400] * 20}
chk("(f) FUNCIONA: preg 8 contra 7 (lug y pregbar) 20/20, menos fundadores, latencia menor que ambos", V(sint(G, fund=F, lat=LT)) == 'FUNCIONA')
chk("(f) NO: todo igual", V(sint({})) == 'NO')
chk("(f) NO: gana a lug pero no a pregbar (la excursion basta, no el destino)", V(sint({'preg': [8] * 20, 'pregbar': [8] * 20}, fund=F, lat=LT)) == 'NO')
L = sint(G, fund=F, lat=None)
chk(f"(f) gana cruce y fundadores pero NO encuentra antes (PM): {V(L)} ({L['matiz']})", V(L) == 'NO' and 'instrumento' in (L['matiz'] or ''))
L = sint({'preg': [9] * 12 + [7] * 8}, fund=F, lat=LT)
chk(f"(f) MODESTO: cruce solo por suma (gana 12, +24), fundadores y latencia si: {V(L)} umbral {L['en_umbral']}", V(L) == 'HAY ALGO MODESTO' and L['en_umbral'])
chk("(f) NO SE LEE: un aborto", V(sint(G, fund=F, lat=LT, aborto=1)) == 'NO SE LEE')
chk("(f) NO SE LEE: el modulo no actua (0 excursiones en preg)", V(sint(G, fund=F, lat=LT, exc={'preg': 0})) == 'NO SE LEE')
chk("(f) NO SE LEE: el mundo no se mudo 4 veces", V(sint(G, fund=F, lat=LT, mud=3)) == 'NO SE LEE')
# (g)
ser = set(range(C10.SEM['serie'], C10.SEM['serie'] + 20)); rep = set(range(C10.SEM['replica'], C10.SEM['replica'] + 20))
exp = set(range(C10.SEM['explora'], C10.SEM['explora'] + 6)); hum = set(range(C10.SEM['humo'], C10.SEM['humo'] + 6)); pra = set(range(739880, 739890))
otros = set(range(739000, 739300)) | set(range(739300, 739500)) | set(range(739500, 739800)) | set(range(739950, 740000))
todo = [ser, rep, exp, hum, pra]
chk("(g) semillas: serie, replica, explora, humo y arnes disjuntas entre si y de P1/P7/P2/C/D (7398xx)",
    all(not (a & b) for i, a in enumerate(todo) for b in todo[i + 1:]) and not (set.union(*todo) & otros) and all(739800 <= s < 739900 for s in set.union(*todo)))


def aborta(argv):
    try: C10.main(argv); return False
    except SystemExit: return True


chk("(g) banderas desconocidas o abreviadas abortan (--hum, --humo --x)", aborta(['--hum']) and aborta(['--humo', '--x']))
chk("(g) --humo con --pool aborta; --pool 3 aborta; --serie --T aborta; --humo --n 3 aborta; --explora --T 250000 aborta; --serie sin shas fijados aborta (candado)",
    aborta(['--humo', '--pool', '2']) and aborta(['--serie', '--pool', '3']) and aborta(['--serie', '--T', '1000']) and aborta(['--humo', '--n', '3']) and aborta(['--explora', '--T', '250000'])
    and (C10.guarda('serie', 'p10_serie_x', False) is not None))
print(f"\nARNES {'PASA' if OK[0] else 'FALLA'}, {NCHK[1]}/{NCHK[0]} · {time.time() - t0:.1f}s")
sys.exit(0 if OK[0] else 1)
