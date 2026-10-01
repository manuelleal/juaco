"""identidad_c.py — ARNES del TRAMO C (mundo_tramo_c + carros COMP / PLAN / PREG). Un proceso; semillas de practica 739955-739959. NADA es dato.
(K) shas fijados (pista, juez, mundo_escalera, construye_p1, corre_p1) y carros en disco == construye_c; chequeo estatico revisa_carro.
(M) MUNDO: perillas apagadas == mundo_escalera BIT A BIT (salida entera + rng); cada perilla encendida != apagada y ACTUA:
    c_e: cobros > 0 solo con un carro que escribe (SENAL) y la E del linaje baja; letra E / K: nace (comp_mundo), se muerde, entra en mord;
    cerrojo: mordidas dentro con llave 0 para O1_LUGAR (nunca muerde K mas de una vez por fundador) -> todas 'sin'; mueve: mudanzas y el
    oasis final != inicial, latencias registradas.
(C) CARROS: COMP0 == PLAN0 == PREG0 == O1_LUGAR (salida entera; mundo_escalera y mundo_tramo_c con su perilla); cada modulo con promotor 1
    != O1_LUGAR en SU mundo; cada control != candidato.
(m) MECANISMO minimo: PLAN acredita (pl_cred > 0) y hab tiene claves; PREG explora (pg_exc > 0) y olvida (pg_olv > 0); COMP muerde E dentro
    del oasis mas que O1_LUGAR (mord_E_dentro).
Uso: python experimentos/organelos/escalera/identidad_c.py [--corto]   (--corto: T 600, para no cargar el PC mientras corre una serie)
"""
import copy, json, os, sys, time

AQUI = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, AQUI)
import corre_c as CC_R
CO = CC_R.CO; MC = CC_R.MC; ME = CC_R.ME; CC = CC_R.CC
sys.path.insert(0, CO.PISTA); import revisa_carro as RC

N = lambda x: json.loads(json.dumps(x, default=str))
OK = [True]; NCHK = [0, 0]
CORTO = '--corto' in sys.argv
T = 600 if CORTO else 3000


def chk(nombre, c):
    c = bool(c); OK[0] &= c; NCHK[0] += 1; NCHK[1] += int(c); print(f"  {'OK   ' if c else 'FALLA'} {nombre}", flush=True)


def fis(r):
    r = copy.deepcopy(r)
    for d in r['linajes']: d.pop('carro', None)
    return N(r)


KW = dict(pizarra=1, rep_acum=0, escala=1, mundo_n=None, fundador_limpio=1, **CO.MUNDO_OASIS)
def run(m, seed, **k): return N(MC.run(seed, [('X', m)] * 9, T=T, **dict(KW, **k)))


t0 = time.time()
print(f"ARNES identidad_c.py (T {T}{' CORTO' if CORTO else ''})")
chk("(K) corre_p1.verifica (shas pista/juez/O1/corre_v143, carros P1 == construye_p1, mundo_escalera)", CO.verifica(lambda s: print('   ', s)))
chk(f"(K) corre_p1.py sha == {CC_R.SHA_CORRE_P1}", CO.h16(os.path.join(AQUI, 'corre_p1.py')) == CC_R.SHA_CORRE_P1)
chk(f"(K) mundo_tramo_c: {MC.construye()[1]}", MC.construye()[1]['sha_mundo_escalera'] == MC.SHAS_FIJOS['mundo_escalera'])
for nm, b in CC.todas().items():
    chk(f"(K) carro {nm} en disco == construye_c", open(CC_R.CARROS[nm], 'rb').read() == b)
    v = RC.revisa_fuente(b.decode('utf-8'), nm); chk(f"(K) chequeo estatico {nm}: {'PASA' if not v else v[:2]}", not v)
chk("(K) identidad corta de corre_c (perillas apagadas == mundo_escalera; promotores 0 == O1_LUGAR)", CC_R.identidad_corta_c(lambda s: print('   ', s), T=min(T, 1200)))
lug, _ = CC_R.modulo('O1_LUGAR'); S = 739956
base = N(ME.run(S, [('X', lug)] * 9, T=T, **KW)); r0 = run(lug, S)
chk(f"(M) mundo_tramo_c apagado == mundo_escalera BIT A BIT (salida entera, s {S}, T {T}) y mismo rng final", r0 == base and r0['pista']['rng_mundo_estado'] == base['pista']['rng_mundo_estado'])
# c_e
CO.fija('lug'); sys.path.insert(0, AQUI); import construye_p7 as C7, importlib.util
def carga(n, ruta):
    spec = importlib.util.spec_from_file_location('c_' + n, ruta); m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m
sen = carga('O1_LUGAR_SENAL', os.path.join(AQUI, 'carros', 'O1_LUGAR_SENAL.py'))
chk("(K) O1_LUGAR_SENAL en disco == construye_p7", open(os.path.join(AQUI, 'carros', 'O1_LUGAR_SENAL.py'), 'rb').read() == C7.todas()['O1_LUGAR_SENAL'])
rs0 = run(sen, S); rs1 = run(sen, S, c_e=0.01)
cob = [d['_carrera']['oasis'].get('cobros', 0) for d in rs1['linajes']]
chk(f"(M) c_e 0.01 con SENAL: cobros por linaje {cob} (> 0 donde hay escrituras {[d['_carrera']['escrituras'] for d in rs1['linajes']]}) y la fisica != c_e 0",
    sum(cob) > 0 and all((c > 0) == (d['_carrera']['escrituras'] > 0) or c <= d['_carrera']['escrituras'] for c, d in zip(cob, rs1['linajes'])) and fis(rs1) != fis(rs0))
rl1 = run(lug, S, c_e=0.01)
def sin_cobros(r):
    r = copy.deepcopy(r)
    for d in r['linajes']: d['_carrera']['oasis'].pop('cobros', None); d['_carrera']['oasis'].pop('latencia_vida', None)
    return r['linajes']
chk("(M) c_e 0.01 con O1_LUGAR (no escribe) == c_e 0 (linajes enteros salvo la telemetria 'cobros' = 0 y 'latencia_vida', y rng: cobrar a quien no habla no cambia nada)",
    sin_cobros(rl1) == sin_cobros(r0) and all(d['_carrera']['oasis'].get('cobros') == 0 for d in rl1['linajes']) and rl1['pista']['rng_mundo_estado'] == r0['pista']['rng_mundo_estado'])
# letra E
rE = run(lug, S, letra_x='E', efecto_x=(0.3, -0.1), p_x=0.1)
mE = sum(sum(d['mord']['E']) for d in rE['linajes']); cE = rE['pista']['comp_mundo'].get('E')
chk(f"(M) letra E nace (comp_mundo A/B/C/D {[rE['pista']['comp_mundo'][k] for k in 'ABCD']}; E vive en el mundo: {sum(sum(d['vis']['E']) for d in rE['linajes'])} visitas), se muerde ({mE}) y la fisica != sin E",
    sum(sum(d['vis']['E']) for d in rE['linajes']) > 0 and fis(rE) != fis(r0) and all('E' in d['mord'] for d in rE['linajes']))
chk("(M) letra E: la contabilidad del juez sigue cerrando (coherente) y A/B/C/D siguen en mord", all(CO.J.resumen_linaje(d, S)['coherente'] for d in rE['linajes']) and all(set('ABCD') <= set(d['mord']) for d in rE['linajes']))
# letra K + cerrojo
rK = run(lug, S, letra_x='K', efecto_x=(0.0, 0.0), p_x=0.1, cerrojo=1)
ll = [d['_carrera']['oasis']['llave'] for d in rK['linajes']]
chk(f"(M) cerrojo con O1_LUGAR: llaves {[z['llaves'] for z in ll]} (<= 1 por fundador: {[d['fundadores'] + 1 for d in rK['linajes']]}), dentro con llave {sum(z['con'] for z in ll)} sin {sum(z['sin'] for z in ll)}",
    all(z['llaves'] <= d['fundadores'] + 1 for z, d in zip(ll, rK['linajes'])) and sum(z['sin'] for z in ll) > 0)
rK0 = run(lug, S, letra_x='K', efecto_x=(0.0, 0.0), p_x=0.1, cerrojo=0)
chk("(M) cerrojo 1 != cerrojo 0 (el cerrojo actua) con la misma letra K", fis(rK) != fis(rK0))
# mueve
rM = run(lug, S, mueve=max(200, T // 3))
mud = rM['pista']['oasis']['mudanzas']; lat = [d['_carrera']['oasis']['latencias'] for d in rM['linajes']]
chk(f"(M) mueve: mudanzas {mud} (>= 2 epocas; oasis final {rM['pista']['oasis']['bins30_final']} != inicial {rM['pista']['oasis']['bins30']}), latencias por linaje {lat[:3]}..., fisica != sin mudanza",
    len(mud) >= 3 and rM['pista']['oasis']['bins30_final'] != rM['pista']['oasis']['bins30'] and all(len(z) == len(mud) for z in lat) and fis(rM) != fis(r0))
# (C) carros
MW = dict(comp=dict(letra_x='E', efecto_x=(0.3, -0.1), p_x=0.1), plan=dict(letra_x='K', efecto_x=(0.0, 0.0), p_x=0.1, cerrojo=1), preg=dict(mueve=max(200, T // 3)))
for pe, (c, b, z) in {'comp': ('O1_LUGAR_COMP', 'O1_LUGAR_COMP_BAR', 'O1_LUGAR_COMP0'), 'plan': ('O1_LUGAR_PLAN', 'O1_LUGAR_PLAN_BAR', 'O1_LUGAR_PLAN0'), 'preg': ('O1_LUGAR_PREG', 'O1_LUGAR_PREG_BAR', 'O1_LUGAR_PREG0')}.items():
    mc, _ = CC_R.modulo(c); mb, _ = CC_R.modulo(b); mz, _ = CC_R.modulo(z)
    rb0 = run(lug, S, **MW[pe]); rz = run(mz, S, **MW[pe]); rc = run(mc, S, **MW[pe]); rbb = run(mb, S, **MW[pe])
    chk(f"(C) {z} == O1_LUGAR en el mundo de {pe} (salida entera)", rz == rb0)
    chk(f"(C) {c} != O1_LUGAR y {b} != {c} y != O1_LUGAR en el mundo de {pe} (los modulos y sus controles actuan)", fis(rc) != fis(rb0) and fis(rbb) != fis(rc) and fis(rbb) != fis(rb0))
    if pe == 'plan':
        cr = [d['carro'].get('pl_cred', 0) for d in rc['linajes']]; hb = [d['carro']['plan']['hab'] for d in rc['linajes']]
        chk(f"(m) PLAN acredita: pl_cred {cr} (> 0), hab {hb[:3]}...", sum(cr) > 0 and any(hb))
    if pe == 'preg':
        ex = [d['carro'].get('pg_exc', 0) for d in rc['linajes']]; ol = [d['carro'].get('pg_olv', 0) for d in rc['linajes']]
        exb = [d['carro'].get('pg_exc', 0) for d in rbb['linajes']]
        chk(f"(m) PREG explora (pg_exc {ex}) y olvida (pg_olv {ol}); el control tambien explora (pg_exc {exb})", sum(ex) > 0 and sum(ol) > 0 and sum(exb) > 0)
    if pe == 'comp':
        me = sum(d['_carrera']['oasis']['x']['mord_dentro'] for d in rc['linajes']); ml = sum(d['_carrera']['oasis']['x']['mord_dentro'] for d in rb0['linajes'])
        ef = [d['_carrera']['oasis']['x']['exp_frio'] for d in rc['linajes']]
        chk(f"(m) COMP muerde E dentro del oasis ({me}) vs O1_LUGAR ({ml}); exposiciones frias registradas {ef}", me >= ml)
print(f"\nARNES {'PASA' if OK[0] else 'FALLA'}, {NCHK[1]}/{NCHK[0]} · {time.time() - t0:.1f}s")
sys.exit(0 if OK[0] else 1)
