"""identidad_perillas.py — ARNES del bloque "perillas" (¿la seleccion prende lo que el mundo paga?). Un proceso; semillas de practica
741950-741989. NADA de aqui es dato.
(K) shas fijados + carros == construye_perillas + identidad corta del runner + chequeo estatico (revisa_carro) de los dos carros.
(C) CARRO en el mundo de P1 (salida ENTERA): GEN0 == O1_LUGAR · GEN (1,1) sin mutacion == O1_LUGAR · GEN (0,0) sin mutacion == O1 (salvo
    la telemetria 'lugar') · NEUTRO: PS_LEE 0 con mutacion, camara y siembra de genes altos == O1 aunque los genes se mueven · cableado:
    GEN (0.5, 1) == O1_LUGAR con LUGAR_W 0.5; GEN (1, 0) == O1_LUGAR con LG_VIAJA 0 · controles que deben diferir (uno por uno).
(G) el generador propio, la mutacion (UN gen por nacimiento, sesgo -delta, recorte en 0), la herencia con PROFUNDIDAD, la CAMARA (la
    refundacion copia a OTRO linaje, nunca a si mismo; el primer fundador sale de la siembra) y el umbral del viaje.
(S) la MONEDA: siembra() en casos sinteticos y contra la fisica del juez (t_fund) en una corrida real; los dos relojes.
(a) regla 14: tarea en el mundo liso con genoma (0,0) == corre_v143.tarea('O1') campo a campo.
(e) trabajo(): cadena de 2 pasajes (sel y neu, mismas semillas), prueba con el genoma mediano, fijo, reanuda, aborto escrito.
(f) la letra en casos sinteticos. (g) guardas: semillas, banderas, pool, tamanos de humo/explora, candado de la serie.
"""
import importlib.util, json, math, os, sys, tempfile, time

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
import corre_perillas as R
CO = R.CO; CV = R.CV; P = R.P; ME = R.ME; CB = R.CB
sys.path.insert(0, CO.PISTA); import revisa_carro as RC
import numpy as np

N = lambda x: json.loads(json.dumps(x, default=str))
OK = [True]; NCHK = [0, 0]


def chk(nombre, c):
    c = bool(c); OK[0] &= c; NCHK[0] += 1; NCHK[1] += int(c); print(f"  {'OK   ' if c else 'FALLA'} {nombre}", flush=True)


t0 = time.time()
print("ARNES identidad_perillas.py")
chk("(K) verifica(): shas de escalera fijados, carros == construye_perillas", R.verifica(lambda s: print('   ', s)))
chk("(K) identidad corta del runner", R.identidad_corta(lambda s: print('   ', s)))
for nm, ruta in R.CARROS.items():
    v = RC.revisa_fuente(open(ruta, encoding='utf-8').read(), nm)
    chk(f"(K) chequeo estatico revisa_carro {nm}: {'PASA' if not v else v[:2]}", not v)
chk("(K) constantes: BASE (0,0), DISENO (1,1) == (LUGAR_W, LG_VIAJA) de construye_p1, sigma 0.03, delta 0.01, recorte [0, 1.5], mundo == el de P1",
    R.BASE == dict(GW=0.0, GV=0.0) and R.DISENO == dict(GW=float(CB.CP1.LUGAR_W), GV=float(CB.CP1.LG_VIAJA)) and R.SIGMA == 0.03 and R.DELTA == 0.01
    and CB.CLIP == ((0.0, 1.5), (0.0, 1.5)) and R.MUNDO == CO.MUNDO_OASIS == dict(oasis=1, extra=0.8, pobre=0.5, dens=0.5, vista_r=20))

R.fija(); m = CV._MODS[R.CARRO]; o1 = CV.modulo('O1'); CO.fija('lug'); lug = CV._MODS['O1_LUGAR']
spec = importlib.util.spec_from_file_location('carro_O1_LUGAR_GEN0', R.CARROS['O1_LUGAR_GEN0']); m0 = importlib.util.module_from_spec(spec); spec.loader.exec_module(m0)
W = R.MUNDO; st = CO.sin_tel
ALTOS = [dict(GW=0.9, GV=0.8, prof=5), dict(GW=0.2, GV=1.2, prof=9)]
# (C) carro
S, T = 741951, 4000
rl = R._run(lug, S, T, **W); ro = R._run(o1, S, T, **W)
chk(f"(C) GEN0 == O1_LUGAR (salida ENTERA, s {S}, T {T}, mundo de P1)", R._run(m0, S, T, **W) == rl)
chk("(C) GEN con genoma (1, 1), sin mutacion == O1_LUGAR (salida ENTERA), con camara y sin camara",
    R._con(m, [dict(R.DISENO)], 0.0, 1, S, T, **W) == rl and R._con(m, [dict(R.DISENO)], 0.0, 1, S, T, camara=0, **W) == rl)
chk("(C) GEN con genoma (0, 0), sin mutacion == O1 (salida ENTERA salvo la telemetria 'lugar'), con camara y sin camara",
    st(R._con(m, [dict(R.BASE)], 0.0, 1, S, T, **W)) == ro and st(R._con(m, [dict(R.BASE)], 0.0, 1, S, T, camara=0, **W)) == ro)
chk("(C) GEN sin siembra (PS_BASE), sin mutacion == O1", st(R._con(m, None, 0.0, 1, S, T, **W)) == ro)
chk("(C) NEUTRO: PS_LEE 0 con mutacion (sigma 0.03, delta 0.01), camara y siembra de genes ALTOS == O1 (ningun cuerpo los lee)", st(R._con(m, ALTOS, R.SIGMA, 0, S, T, **W)) == ro)
x = R.tarea(S, T, siembra=ALTOS, sigma=R.SIGMA, lee=0)
fu = [q for v in x['tel_ps'].values() for q in v.get('fund', [])]
chk(f"(C)   ...y sus genes SI se mueven: {len(fu)} fundadores ({sum(q[0] == 1 for q in fu)} de siembra = los 9 primeros, {sum(q[0] == 2 for q in fu)} de camara), "
    f"{len({tuple(q[1]) for q in fu})} genomas distintos, profundidad mutacional maxima {max(q[2] for q in fu)}; el modulo no viaja (viajes 0)",
    sum(q[0] == 1 for q in fu) == 9 and sum(q[0] == 2 for q in fu) == len(fu) - 9 > 9 and len({tuple(q[1]) for q in fu}) > 0.9 * len(fu)
    and max(q[2] for q in fu) > 5 and sum(t['lugar']['st_lg_viajes'] for t in x['tel']) == 0)
chk("(C) el runner deja el modulo como estaba (SIEMBRA None, PS_LEE 1, sigma 0.03, delta 0.01, camara 1, registros vacios) y pista.run intacta",
    m.SIEMBRA is None and m.PS_LEE == 1 and m.PS_SIGMA == 0.03 and m.PS_DELTA == 0.01 and m.PS_CAMARA == 1 and not m._VIVO and not m._TEL
    and P.run is CV.P.run and 'run2' not in repr(P.run))
w0, v0 = lug.LUGAR_W, lug.LG_VIAJA
try:
    lug.LUGAR_W = 0.5; rw = R._run(lug, S, T, **W)
    lug.LUGAR_W = w0; lug.LG_VIAJA = 0; rv = R._run(lug, S, T, **W)
finally:
    lug.LUGAR_W = w0; lug.LG_VIAJA = v0
chk("(C) cableado GW: GEN (0.5, 1) sin mutacion == O1_LUGAR con LUGAR_W 0.5 escrito a mano (salvo telemetria)", st(R._con(m, [dict(GW=0.5, GV=1.0)], 0.0, 1, S, T, **W)) == st(rw))
chk("(C) cableado GV: GEN (1, 0) sin mutacion == O1_LUGAR con LG_VIAJA 0 escrito a mano (salvo telemetria)", st(R._con(m, [dict(GW=1.0, GV=0.0)], 0.0, 1, S, T, **W)) == st(rv))
chk("(C) control que debe diferir: O1_LUGAR != O1 (el modulo actua)", st(rl) != ro)
chk("(C) control que debe diferir: el gen del VIAJE actua (LG_VIAJA 0 != 1)", st(rv) != st(rl))
SV, TV = 741956, 12000; rov = R._run(o1, SV, TV, **W)
chk(f"(C) control que debe diferir: el gen del VALOR actua (GW 1.5 con GV 0 != O1 y GW 0.5 != O1; s {SV}, T {TV}; a T {T} aun son iguales: actua poco y tarde)",
    st(R._con(m, [dict(GW=1.5, GV=0.0)], 0.0, 1, SV, TV, **W)) != rov and st(R._con(m, [dict(GW=0.5, GV=0.0)], 0.0, 1, SV, TV, **W)) != rov)
chk("(C) control que debe diferir: LEER los genes actua (misma siembra alta y mutacion, PS_LEE 1 != PS_LEE 0)", st(R._con(m, ALTOS, R.SIGMA, 1, S, T, **W)) != ro)
chk("(C) el modulo de O1_LUGAR quedo como estaba", lug.LUGAR_W == 1.0 and lug.LG_VIAJA == 1)
# (G) generador, mutacion, herencia, camara
CT = lambda i: dict(L=360, rep_umbral=1.0, rng=np.random.default_rng(1), id='x', indice=i)
R._pon(m, None, 741952, 0.03, 0.01, 1, 1)
c = m.crea(CT(0))
u = [c._ps_u() for _ in range(40000)]
z = [math.sqrt(-2.0 * math.log(c._ps_u())) * math.cos(2.0 * math.pi * c._ps_u()) for _ in range(40000)]
mu, sd = float(np.mean(z)), float(np.std(z))
chk(f"(G) generador propio: uniforme en (0,1) media {np.mean(u):.4f} (0.5 +- 0.01), normal media {mu:.4f} (+- 0.02) desv {sd:.4f} (1 +- 0.02), P(z > 1.9) {np.mean(np.array(z) > 1.9):.4f} (0.029 +- 0.005)",
    0 < min(u) and max(u) < 1 and abs(np.mean(u) - 0.5) < 0.01 and abs(mu) < 0.02 and abs(sd - 1) < 0.02 and abs(np.mean(np.array(z) > 1.9) - 0.0287) < 0.005)
chk(f"(G) primer fundador sin siembra: origen 0 (base), profundidad 1, genes = (0, 0) con UNA mutacion en un gen ({c._gen})", c._psfund == 0 and c._prof == 1 and min(c._gen) == 0.0 and all(q >= 0 for q in c._gen))
g0 = [0.5, 0.5]; h = np.array([c._ps_muta(g0) for _ in range(8000)]); d = h - np.array(g0); cam = d != 0
chk(f"(G) mutacion: UN gen por nacimiento (cambian 2 genes en {int((cam.sum(1) == 2).sum())} de 8000; 0 genes en {int((cam.sum(1) == 0).sum())}), cada gen la mitad de las veces ({cam[:, 0].mean():.3f})",
    (cam.sum(1) == 1).all() and abs(cam[:, 0].mean() - 0.5) < 0.02)
dd = [d[:, j][cam[:, j]] for j in (0, 1)]
chk(f"(G) mutacion: gen' = gen - delta + N(0, sigma): media {[round(float(q.mean()), 4) for q in dd]} (-0.01 +- 0.002), desv {[round(float(q.std()), 4) for q in dd]} (0.03 +- 0.002)",
    all(abs(q.mean() + 0.01) < 0.002 and abs(q.std() - 0.03) < 0.002 for q in dd))
h0 = np.array([c._ps_muta([0.0, 0.0]) for _ in range(4000)])
chk(f"(G) recorte en 0: desde (0, 0) ningun gen negativo; queda en (0, 0) el {float((h0.sum(1) == 0).mean()):.3f} (esperado P(N(-0.01, 0.03) <= 0) = 0.63 +- 0.03); P(gen > 0.05) = {float((h0.max(1) > 0.05).mean()):.4f} (0.023 +- 0.008)",
    (h0 >= 0).all() and abs((h0.sum(1) == 0).mean() - 0.63) < 0.03 and abs((h0.max(1) > 0.05).mean() - 0.0228) < 0.008)
gA = list(c._gen); R._pon(m, None, 741952, 0.03, 0.01, 1, 1); c2 = m.crea(CT(0)); R._pon(m, None, 741953, 0.03, 0.01, 1, 1); c3 = m.crea(CT(0))
chk("(G) determinista por (semilla, indice, instancia): misma semilla -> mismos genes del fundador; otra semilla -> otra corriente", c2._gen == gA and c3._pss != c2._pss)
c3._prof = 7; mem = c3.al_parir(dict(t=0, k=0)); gh = mem['_gen']; c3.nace(dict(t=1, k=1, fundador=False, memoria=mem, rng_hijo=None))
chk("(G) herencia: al_parir pone '_gen' = (genes mutados, profundidad + 1) en la memoria del hijo; nace lo toma (y no lo confunde con una letra de la tabla)",
    c3._gen == list(gh[0]) and c3._prof == 8 == gh[1] and '_gen' not in c3.n and '_lugar' not in c3.n and m._VIVO[0] == (list(gh[0]), 8))
c3.lugar[:] = 0; c3.lugar[20] = [0.06, 0.04]
c3.GV = 1.0; a1 = c3._lg_meta(0); c3.GV = 0.6; a2 = c3._lg_meta(0); c3.GV = 0.4; a3 = c3._lg_meta(0)
chk(f"(G) umbral del viaje: con recuerdo 0.10 en el bin 20, GV 1.0 -> celda {a1}, GV 0.6 -> {a2}, GV 0.4 -> {a3} (0.04 <= LG_MIN 0.05: no viaja)", a1 == 246 and a2 == 246 and a3 is None)
R._pon(m, [dict(GW=0.3, GV=0.2, prof=17)], 741952, 0.03, 0.01, 1, 1); c4 = m.crea(CT(3))
chk(f"(G) primer fundador con siembra: origen 1, profundidad 17 + 1, genes {[round(q, 3) for q in c4._gen]} = (0.3, 0.2) con un gen mutado; el cuerpo los lee tal cual",
    c4._psfund == 1 and c4._prof == 18 and sum(a != b for a, b in zip(c4._gen, [0.3, 0.2])) == 1 and max(abs(a - b) for a, b in zip(c4._gen, [0.3, 0.2])) < 0.15 and [c4.GW, c4.GV] == c4._gen)
m._VIVO.clear(); m._VIVO[3] = ([0.3, 0.2], 18); m._VIVO[5] = ([0.7, 0.6], 40)
c5 = m.crea(CT(3))
chk(f"(G) CAMARA: la refundacion del linaje 3 copia (mutado) el genoma del OTRO linaje (5), nunca el suyo: origen 2, profundidad 40 + 1, genes {[round(q, 3) for q in c5._gen]}",
    c5._psfund == 2 and c5._psc == 1 and c5._prof == 41 and sum(a != b for a, b in zip(c5._gen, [0.7, 0.6])) == 1 and max(abs(a - b) for a, b in zip(c5._gen, [0.7, 0.6])) < 0.15)
m.PS_CAMARA = 0; m._VIVO[5] = ([0.7, 0.6], 40); c6 = m.crea(CT(3))
chk("(G) sin camara (PS_CAMARA 0, la PRUEBA): la refundacion sale de la SIEMBRA (origen 1)", c6._psfund == 1 and c6._prof == 18)
m.PS_LEE = 0; m.PS_CAMARA = 1; c7 = m.crea(CT(3))
chk("(G) PS_LEE 0: el cuerpo lee (0, 0) aunque su genoma sea alto", c7._gen != [0.0, 0.0] and (c7.GW, c7.GV) == (0.0, 0.0))
R._quita(m)
# (S) la moneda y los relojes
gA = [0.1, 0.2]; gB = [0.0, 0.3]
tel = {'0': dict(vivos=[[t, gA, 3, 50 + t // 1000] for t in range(0, 10000, 1000)]),                     # establecido (una instancia en la 2a mitad)
       '1': dict(vivos=[[t, gB, 1 + (t >= 7000), 20] for t in range(0, 10000, 1000)]),                   # refundo en la 2a mitad
       '2': dict(vivos=[[t, gB, 5, 9] for t in range(0, 4000, 1000)])}                                   # sin muestras en la ventana final
s, info = R.siembra(tel, 10000, vent=3000)
chk(f"(S) siembra sintetica: solo el linaje establecido da siembra ({info}), con su profundidad", info == dict(n_est=1, respaldo=False, idx=[0], n=3)
    and s == [dict(GW=0.1, GV=0.2, prof=57), dict(GW=0.1, GV=0.2, prof=58), dict(GW=0.1, GV=0.2, prof=59)] and R.prof_de(s) == 58.0)
s, info = R.siembra({k: tel[k] for k in ('1', '2')}, 10000, vent=3000)
chk(f"(S) respaldo: sin establecidos dan siembra los de menos instancias en la 2a mitad ({info})", info['respaldo'] and info['n_est'] == 0 and info['idx'] == [1] and len(s) == 3)
s, info = R.siembra({'2': tel['2']}, 10000, vent=3000)
chk("(S) sin vivos en la ventana: siembra None", s is None and info['n'] == 0)
chk("(S) genoma mediano por gen (sin la profundidad)", R.genoma_mediano([dict(GW=0.1, GV=0.0, prof=3), dict(GW=0.5, GV=0.2, prof=9), dict(GW=0.3, GV=0.1, prof=4)]) == dict(GW=0.3, GV=0.1))
S4, T4 = 741954, 12000
x = R.tarea(S4, T4, siembra=[dict(GW=0.5, GV=0.5, prof=0)], sigma=R.SIGMA, lee=1); s, info = R.siembra(x['tel_ps'], T4)
tf = {int(l['indice']): l['telem']['t_fund'] for l in x['linajes']}; ul = {int(i): max(q[0] for q in v['vivos']) for i, v in x['tel_ps'].items()}
fis = sorted(i for i in tf if len(tf[i]) < 200 and not any(T4 // 2 <= t < ul[i] for t in tf[i]))
chk(f"(S) contra la fisica del juez (s {S4}, T {T4}): establecidos por instancia {info['idx']} == linajes sin fundacion (t_fund) entre T/2 y su ultima muestra {fis}; "
    f"siembra de {info['n']} genomas, profundidad mutacional mediana {R.prof_de(s)}", (not info['respaldo']) and info['idx'] == fis and info['n'] == 5 * len(fis) and 0 < len(fis) < 9)
f4 = R.fila(x, T4); nf = sum(l['fundadores'] for l in x['linajes'])
chk(f"(S) reloj de reemplazos contra la fisica: refundaciones por camara {f4['fund_de_camara']} == fundadores del juez {nf} (el juez no cuenta los 9 primeros cuerpos; el carro si: {f4['fund_n']} = 9 de siembra + camara)",
    f4['fund_de_camara'] == nf and f4['fund_de_siembra'] == 9 and f4['fund_n'] == nf + 9 and f4['fund_de_base'] == 0)
# (a) regla 14
y = CV.tarea((741955, 'O1', 2000)); xx = R.tarea(741955, 2000, siembra=[dict(R.BASE)], sigma=0.0, lee=1, mundo=CO.MUNDO_LISO, delta=0.0, camara=0)
qa = N({k: v for k, v in xx.items() if k not in ('seg', 'estado', 'tel', 'tel_ps')}); qb = N({k: v for k, v in y.items() if k not in ('seg', 'tel')})
for l in qa['linajes']: l.pop('_oasis', None)
qa = json.loads(json.dumps(qa).replace('O1_LUGAR_GEN#', 'O1#'))   # lo unico que cambia es el NOMBRE del carro en los ids
dif = [k for k in qb if qa.get(k) != qb[k]]
chk(f"(a) regla 14: tarea (genoma (0,0), mundo liso) == corre_v143.tarea('O1') campo a campo salvo el nombre del carro en los ids (s 741955, T 2000){'' if not dif else ' difiere en ' + str(dif)}", qa == qb and set(qa) == set(qb))
# (e) trabajo / cadena / reanuda
with tempfile.TemporaryDirectory() as td:
    base = (741960, 741975); mk = lambda t, re=False: (t[0], t[1], t[2], base, 2, 3000, 3000, td, re)
    cs = R.trabajo(mk(('cadena', 0, 'sel'))); cn = R.trabajo(mk(('cadena', 0, 'neu')))
    chk(f"(e) cadenas sel y neu sin aborto ({cs['aborto']}, {cn['aborto']}), 2 pasajes, mismas semillas {[q['seed'] for q in cs['pasajes']]}",
        cs['aborto'] is None and cn['aborto'] is None and [q['seed'] for q in cs['pasajes']] == [q['seed'] for q in cn['pasajes']] == [741960, 741961])
    e = lambda q: q['estado']
    chk("(e) estado escrito: sel lee 1, neu lee 0; sigma 0.03, delta 0.01, camara 1, mundo de P1; pasaje 0: 9 fundadores de la base y el resto de camara; pasaje 1: 9 de siembra y el resto de camara",
        all(e(q)['lee'] == 1 and e(q)['sigma'] == 0.03 and e(q)['delta'] == 0.01 and e(q)['camara'] == 1 and e(q)['mundo'] == R.MUNDO for q in cs['pasajes']) and all(e(q)['lee'] == 0 for q in cn['pasajes'])
        and all(c_['pasajes'][0]['sembrado'] == 0 and c_['pasajes'][0]['fund_de_base'] == 9 and c_['pasajes'][0]['fund_de_siembra'] == 0 and c_['pasajes'][1]['sembrado'] == 1
                and c_['pasajes'][1]['fund_de_siembra'] == 9 and c_['pasajes'][1]['fund_de_base'] == 0 and all(q['fund_de_camara'] == q['fund_n'] - 9 > 0 for q in c_['pasajes']) for c_ in (cs, cn)))
    chk(f"(e) el neutro no viaja en ningun pasaje (viajes {[q['lugar']['viajes'] for q in cn['pasajes']]}); relojes del neutro: profundidad mutacional por pasaje {[q['prof'] for q in cn['pasajes']]} "
        f"(no baja), refundaciones por camara {cn['refund_camara']}; genoma final {cn['genoma_final']}",
        all(q['lugar']['viajes'] == 0 for q in cn['pasajes']) and set(cn['genoma_final']) == set(R.GENES) and cn['pasajes'][1]['prof'] >= cn['pasajes'][0]['prof'] >= 1
        and cn['prof_final'] == cn['pasajes'][1]['prof'] and cn['refund_camara'] == sum(q['fund_de_camara'] for q in cn['pasajes']))
    ps = R.trabajo(mk(('prueba', 0, 'sel'))); pf = R.trabajo(mk(('prueba', 0, 'fab'))); po = R.trabajo(mk(('prueba', 0, 'o1')))
    chk(f"(e) prueba sel: genoma == mediano de la siembra final de su cadena; sin mutacion ni camara; todos los fundadores con ESE genoma ({ps.get('fund_n')} fundadores, {ps.get('fund_genes_distintos')} genoma)",
        ps['aborto'] is None and ps['genoma'] == cs['genoma_final'] and e(ps)['sigma'] == 0.0 and e(ps)['delta'] == 0.0 and e(ps)['camara'] == 0 and e(ps)['lee'] == 1 and e(ps)['siembra_n'] == 1
        and ps['fund_genes_distintos'] == 1 and ps['fund_gen0'] == cs['genoma_final'] and ps['fund_de_siembra'] == ps['fund_n'])
    chk(f"(e) pruebas fab (1,1) y o1 (0,0): genomas de diseno y base; fab viaja ({pf['lugar']['viajes']}), o1 no ({po['lugar']['viajes']}); semilla de prueba {pf['seed']}",
        pf['genoma'] == R.DISENO and po['genoma'] == R.BASE and pf['lugar']['viajes'] > 0 and po['lugar']['viajes'] == 0 and pf['seed'] == po['seed'] == ps['seed'] == 741975)
    ps2 = R.trabajo(mk(('prueba', 0, 'sel'), True)); cs2 = R.trabajo(mk(('cadena', 0, 'sel'), True))
    chk("(e) --reanuda relee igual (prueba y cadena)", N({k: v for k, v in ps.items() if k != 'seg'}) == N({k: v for k, v in ps2.items() if k != 'seg'}) and N(cs) == N(cs2))
    os.remove(os.path.join(td, 'cadena_i00_sel.json')); os.remove(os.path.join(td, 'pasaje_i00_sel_p01.json')); cs3 = R.trabajo(mk(('cadena', 0, 'sel'), True))
    sinseg = lambda c_: N(dict({k: v for k, v in c_.items() if k not in ('seg', 'pasajes')}, pasajes=[{k: v for k, v in q.items() if k != 'seg'} for q in c_['pasajes']]))
    chk("(e) cadena cortada a mitad (queda el pasaje 0, falta el 1): --reanuda relee el 0, recorre el 1 y da la MISMA cadena (determinista)", sinseg(cs3) == sinseg(cs))
    fj = R.trabajo(mk(('fijo', 1, '1:0')))
    chk("(e) trabajo fijo '1:0': genoma (1, 0), sin aborto, JSON escrito", fj['aborto'] is None and fj['genoma'] == dict(GW=1.0, GV=0.0) and os.path.exists(os.path.join(td, 'fijo_i01_1_0.json')))
    xz = R.trabajo(mk(('prueba', 0, 'zzz'))); xn = R.trabajo(mk(('prueba', 5, 'neu')))
    chk("(e) brazo desconocido y prueba sin cadena -> aborto escrito (nube-9)", xz['aborto'] and xn['aborto'] and os.path.exists(os.path.join(td, 'prueba_i00_zzz.json')))
    C, Rr, F, ab = R.carga(td)
    chk("(e) carga(): 2 cadenas, 3 pruebas, 1 fijo, 2 abortos", len(C['sel']) == 1 and len(C['neu']) == 1 and sum(len(v) for v in Rr.values()) == 3 and len(F) == 1 and len(ab) == 2)


# (f) la letra en casos sinteticos
def sint(gv_sel, gv_neu, cz, n=20, npas=R.NPAS, aborto=0, lee_neu=0, viajes_neu=0, sigma_pru=0.0, gen_mal=False, prof_neu=None, refund_neu=None, camara_cad=1, pas_menos=0):
    est = lambda lee, sg, dl, cm, sn: dict(carro=R.CARRO, PERILLAS=1, lee=lee, sigma=sg, delta=dl, camara=cm, siembra_n=sn, mundo=dict(R.MUNDO))
    C = {b: {} for b in R.CADENAS}; RR = {b: {} for b in R.ORDEN}
    for i in range(n):
        for b in R.CADENAS:
            gv = (gv_sel if b == 'sel' else gv_neu)[i]; g = dict(GW=0.0, GV=gv)
            pas = [dict(p=p, sembrado=int(p > 0), fund_de_base=(0 if p else 9), fund_de_siembra=(9 if p else 0), fund_de_camara=900, fund_n=909, partos_tel=50, coherente=True, cruzan=3,
                        moneda=dict(n_est=5, respaldo=False, idx=[0], n=5), prof=13.0 * (p + 1), genes_siembra=g, frac_on=0.5, oasis=dict(mord_AC_dentro=5, ratio_pasos=1.0),
                        lugar=dict(viajes=(10 if b == 'sel' else viajes_neu)), estado=est(1 if b == 'sel' else lee_neu, 0.03, 0.01, camara_cad, 0 if p == 0 else 5)) for p in range(npas - pas_menos)]
            C[b][i] = dict(pasajes=pas, genoma_final=g, prof_final=(65.0 if b == 'sel' or prof_neu is None else prof_neu[i]),
                           refund_camara=(4500 if b == 'sel' or refund_neu is None else refund_neu[i]), partos=250)
        for b in R.ORDEN:
            g = C[b][i]['genoma_final'] if b in R.CADENAS else (R.DISENO if b == 'fab' else R.BASE)
            c_ = cz.get(b, [4] * n)[i]
            RR[b][i] = dict(cruzan=c_, mayoria=int(c_ * 2 > 9), R0_med=0.9, coherente=True, fund=[1] * 9, fund_post10k=[0] * 9, mundo_AC=7.0,
                            oasis=dict(mord_AC_dentro=5, ratio_pasos=5.0), lugar=dict(viajes=(0 if b == 'o1' else 10)), genoma=dict(g),
                            fund_n=9, fund_de_siembra=9, fund_genes_distintos=1, fund_gen0=(dict(g) if not (gen_mal and b == 'sel') else dict(GW=9.0, GV=9.0)),
                            estado=est(1, sigma_pru, 0.0, 0, 1))
    return R.lee_serie(C, RR, n, aborto, npas)


V = lambda L: L['veredicto']
ON = [0.2] * 20; OFF = [0.0] * 20; BASEZ = dict(fab=[4] * 20, o1=[0] * 20)
L = sint(ON, OFF, dict(BASEZ, sel=[4] * 20, neu=[0] * 20))
chk(f"(f) FUNCIONA: GV sel 0.2 vs neu 0 en 20/20 y sel cruza 4 vs neu 0: {V(L)}", V(L) == 'FUNCIONA' and all(L['validez'].values()) and not L['en_umbral'])
L = sint(ON, OFF, dict(BASEZ, sel=[4] * 20, neu=[4] * 20))
chk(f"(f) MODESTO: el gen sube pero la deriva cruza igual: {V(L)} ({L['matiz']})", V(L) == 'HAY ALGO MODESTO' and 'no cruza mas' in L['matiz'])
L = sint([0.04] * 20, OFF, dict(BASEZ, sel=[4] * 20, neu=[0] * 20))
chk(f"(f) MODESTO: cruza mas pero el gen no pasa el margen 0.05 (0.04): {V(L)} ({L['matiz']})", V(L) == 'HAY ALGO MODESTO' and 'sin que el gen' in L['matiz'])
chk("(f) NO: ni gen ni cruce (con reloj valido)", V(sint(OFF, OFF, dict(BASEZ, sel=[0] * 20, neu=[0] * 20))) == 'NO')
chk("(f) NO: la deriva tambien sube el gen (sel 0.2, neu 0.2) y cruza igual", V(sint(ON, ON, dict(BASEZ, sel=[4] * 20, neu=[4] * 20))) == 'NO')
L = sint([0.2] * 12 + [0.0] * 8, OFF, dict(BASEZ, sel=[4] * 12 + [0] * 8, neu=[0] * 20))
chk(f"(f) 12/20 en el gen y en el cruce (suma +48): NO y EN EL UMBRAL: {V(L)} {L['en_umbral']}", V(L) == 'NO' and L['en_umbral'])
L = sint([0.2] * 13 + [0.0] * 7, OFF, dict(BASEZ, sel=[4] * 13 + [0] * 7, neu=[0] * 20))
chk(f"(f) 13/20 en las dos: FUNCIONA y EN EL UMBRAL: {V(L)} {L['en_umbral']}", V(L) == 'FUNCIONA' and L['en_umbral'])
L = sint(ON, OFF, dict(BASEZ, sel=[1] * 9 + [0] * 11, neu=[0] * 20))
chk(f"(f) cruce: gana 9/20 y suma +9: PC cae entero -> MODESTO (solo el gen), umbral por la suma: {V(L)} {L['en_umbral']}", V(L) == 'HAY ALGO MODESTO' and L['en_umbral'])
chk("(f) empates EN CONTRA en el gen: sel == neu + margen exacto no cuenta", sint([0.05] * 20, OFF, dict(BASEZ, sel=[4] * 20, neu=[0] * 20))['pareado_gen']['gana'] == 0)
ok_ = dict(BASEZ, sel=[4] * 20, neu=[0] * 20)
chk("(f) NO SE LEE: un aborto", V(sint(ON, OFF, ok_, aborto=1)) == 'NO SE LEE')
chk("(f) NO SE LEE: el mundo no paga (fab > o1 solo en 15/20) (V2)", V(sint(ON, OFF, dict(ok_, fab=[4] * 15 + [0] * 5))) == 'NO SE LEE')
chk("(f) NO SE LEE: el neutro LEYO los genes (lee 1 en su cadena) (V4)", V(sint(ON, OFF, ok_, lee_neu=1)) == 'NO SE LEE')
chk("(f) NO SE LEE: el neutro viajo (V5)", V(sint(ON, OFF, ok_, viajes_neu=3)) == 'NO SE LEE')
chk("(f) NO SE LEE: la prueba muto (sigma 0.03 en la prueba) (V4)", V(sint(ON, OFF, ok_, sigma_pru=0.03)) == 'NO SE LEE')
chk("(f) NO SE LEE: la cadena corrio sin camara (V4)", V(sint(ON, OFF, ok_, camara_cad=0)) == 'NO SE LEE')
chk("(f) NO SE LEE: el genoma de la prueba de sel no es el de su cadena (V4)", V(sint(ON, OFF, ok_, gen_mal=True)) == 'NO SE LEE')
L = sint(OFF, OFF, dict(BASEZ, sel=[0] * 20, neu=[0] * 20), prof_neu=[R.PROF_MIN - 1.0] * 5 + [65.0] * 15)
chk(f"(f) RELOJ: profundidad mutacional neutra < {R.PROF_MIN} en 5 cadenas (15/20 < 16): un 'NO' sin reloj es NO SE LEE: {V(L)} {L['validez']['V7a_profundidad_mutacional_neutra']}",
    V(L) == 'NO SE LEE' and not L['validez']['V7a_profundidad_mutacional_neutra'] and L['validez']['V7b_refundaciones_por_camara_neutra'])
chk("(f) RELOJ: con 4 cadenas cortas (16/20) se lee", V(sint(OFF, OFF, dict(BASEZ, sel=[0] * 20, neu=[0] * 20), prof_neu=[R.PROF_MIN - 1.0] * 4 + [float(R.PROF_MIN)] * 16)) == 'NO')
L = sint(ON, OFF, ok_, refund_neu=[R.REFUND_MIN - 1] * 5 + [R.REFUND_MIN] * 15)
chk(f"(f) RELOJ: refundaciones por camara neutras < {R.REFUND_MIN} en 5 cadenas: NO SE LEE (tambien si el resultado era FUNCIONA): {V(L)}", V(L) == 'NO SE LEE' and not L['validez']['V7b_refundaciones_por_camara_neutra'])
chk("(f) NO SE LEE: cadenas con un pasaje de menos (V1)", V(sint(ON, OFF, ok_, pas_menos=1)) == 'NO SE LEE')
chk("(f) bloque: FUNCIONA + MODESTO = MODESTO; FUNCIONA + NO SE LEE = NO SE LEE", R.bloque('FUNCIONA', 'HAY ALGO MODESTO') == 'HAY ALGO MODESTO' and R.bloque('FUNCIONA', 'NO SE LEE') == 'NO SE LEE' and R.bloque('NO', 'NO') == 'NO')
# (g) guardas
ser = {R.sem_pas(R.BASES['serie'], i, p) for i in range(20) for p in range(R.NPAS)} | {R.sem_pru(R.BASES['serie'], i) for i in range(20)}
rep = {R.sem_pas(R.BASES['replica'], i, p) for i in range(20) for p in range(R.NPAS)} | {R.sem_pru(R.BASES['replica'], i) for i in range(20)}
exp = {R.sem_pas(R.BASES['explora'], i, p) for i in range(4) for p in range(6)} | {R.sem_pru(R.BASES['explora'], i) for i in range(4)}
hum = {R.sem_pas(R.BASES['humo'], 0, p) for p in range(2)} | {R.sem_pru(R.BASES['humo'], 0)}; pra = set(range(741950, 741990))
chk(f"(g) semillas: serie ({len(ser)}), replica ({len(rep)}), explora, humo y arnes disjuntas y en 741xxx",
    len(ser) == len(rep) == 20 * R.NPAS + 20 and not (ser & rep) and not (ser & exp) and not (ser & hum) and not (ser & pra) and not (rep & exp) and not (rep & hum) and not (rep & pra)
    and not (exp & hum) and not (exp & pra) and not (hum & pra) and all(741000 <= s_ < 742000 for s_ in ser | rep | exp | hum | pra))


def aborta(argv):
    try: R.main(argv); return False
    except SystemExit: return True


chk("(g) banderas desconocidas o abreviadas abortan (--hum, --humo --x); --humo con --pool aborta; --pool 3 aborta",
    aborta(['--hum']) and aborta(['--humo', '--x']) and aborta(['--humo', '--pool', '2']) and aborta(['--serie', '--pool', '3']))
chk("(g) --explora: 8 corridas aborta (--npas 4 con 2 cadenas); T 250000 aborta; indice 4 aborta; --serie con --T aborta; 8 genomas fijos aborta",
    aborta(['--explora', '--npas', '4']) and aborta(['--explora', '--npas', '1', '--T', '250000']) and aborta(['--explora', '--npas', '1', '--desde', '4']) and aborta(['--serie', '--T', '5'])
    and aborta(['--explora', '--genomas', '1:0,0:1', '--n', '4']))
sp = dict(R.SHAS_PROPIOS)
try:
    R.SHAS_PROPIOS.update({k: None for k in sp}); c1 = R.guarda('serie', 'serie_x', False)
finally:
    R.SHAS_PROPIOS.update(sp)
chk(f"(g) candado: con los shas propios sin fijar la serie no corre ({str(c1)[:40]}...)", c1 is not None and 'sin fijar' in c1)
chk(f"(g) el humo cabe en un proceso: {2 * R.HUMO['npas'] + 2} corridas de <= {max(R.HUMO['T_pas'], R.HUMO['T_pru'])} pasos; serie: {R.N_IND} indices x (2 cadenas x {R.NPAS} pasajes de {R.T_PAS} + 4 pruebas de {R.T_PRU}); pool max {R.POOL_MAX}",
    2 * R.HUMO['npas'] + 2 <= 6 and max(R.HUMO['T_pas'], R.HUMO['T_pru']) <= 200000 and R.POOL_MAX == 2)
print(f"\nARNES {'PASA' if OK[0] else 'FALLA'}, {NCHK[1]}/{NCHK[0]} · {time.time() - t0:.1f}s")
sys.exit(0 if OK[0] else 1)
