"""identidad_o1_libre_f2.py — ARNES de F2 "un gen por parto". Un proceso; semillas de practica 744950-744989. Su salida se guarda con tee en
identidad_o1_libre_f2_salida.txt (el arnes no escribe nada fuera de un directorio temporal).
(K) shas, carro == constructor, identidad corta del runner (la de o1_libre con el carro F2 + la de F2).
(I) IDENTIDAD BIT A BIT con la perilla apagada: O1_LIB_F2 con PS_UNGEN 0 == O1_LIB de o1_libre, salida ENTERA de la pista y telemetria
    (mundo del bloque, sigma 0.03, colonia, publicando; neutro con siembra; pista vieja). Control que puede fallar: con PS_UNGEN 1 cambia.
    Con PS_UNGEN 1 el neutro (PS_LEE 0) sigue siendo O1 bit a bit; eventos de mutacion == partos + fundadores.
(U) UN GEN: sin pista, instancia por instancia: cada parto y cada fundador cambian EXACTAMENTE un gen (0 solo si el recorte lo clava);
    eleccion uniforme entre los 14; paso con la sigma_j de O1_LIB; herencia exacta; misma eleccion de siembra que O1_LIB; con PS_UNGEN 0 mutan los 14.
(R) RELOJ: reloj() sobre los datos de o1_libre reproduce la auditoria de F0 (10 genes: 11.87 serie, 11.65 replica) y casos sinteticos.
(G) regla 14: lo importado sigue siendo lo de o1_libre (tarea('o1') == corre_v143.tarea; fila() solo agrega 'ungen').
(L) LA LETRA de F2 en casos sinteticos (reusa sintetico() del arnes de o1_libre).
(J) guardas: banderas, semillas 744xxx disjuntas de las de o1_libre, el humo cabe.
(P) ruta --serie --pool 2 con Pool FALSO de un proceso, candado y regla de parada.
"""
import copy, glob, json, os, shutil, sys, tempfile, time
import numpy as np

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
import corre_o1_libre_f2 as F
CO = F.CO; CV = CO.CV; P = CO.P; PL = CO.PL; CB = CO.CB; J = CO.J
import identidad_o1_libre as IO   # arnes de o1_libre: se reusa sintetico() (mismo modulo corre_o1_libre ya redirigido)
assert IO.CO is CO

N = lambda x: json.loads(json.dumps(x, default=str, sort_keys=True))
OK = [True]; NCHK = [0, 0]


def chk(nombre, c):
    c = bool(c); OK[0] &= c; NCHK[0] += 1; NCHK[1] += int(c); print(f"  {'OK   ' if c else 'FALLA'} {nombre}", flush=True)


def corre(mod, seed, T, ungen, siembra=None, sigma=0.03, lee=1, escribe=1, coloniza=1, mundo=PL.MUNDO_LIBRE, orig=False):
    """Una corrida de 9 x mod. orig=True: el O1_LIB de o1_libre con SU _pon_lib (sin PS_UNGEN). Devuelve (salida entera, telemetria)."""
    F.UNGEN = ungen
    try:
        (F._ORIG['pon'] if orig else CO._pon_lib)(mod, seed, siembra, lee, escribe, sigma, coloniza)
        k = dict(T=T, pizarra=1, rep_acum=0, escala=1, mundo_n=None, fundador_limpio=1)
        r = N((PL.run if mundo is not None else P.run)(seed, [('X', mod)] * 9, **k, **(mundo or {})))
        return r, N({str(i): v for i, v in mod._TEL.items()})
    finally:
        (F._ORIG['apaga'] if orig else CO._apaga_lib)(mod); F.UNGEN = 1


def sint(r0_neu=0.95, cruz_lib=7, cruz_o1=7, n_neu=0.9, n_lib=0.9, eventos=10, est_ungen=1, sha=None, **kw):
    """sintetico() de o1_libre + los campos de F2: telemetria 'ungen', estado (ungen, sha), R0 del neutro, cruces y siembra_final con reloj n."""
    C, R = IO.sintetico(**kw); sha = sha or F.SHA_F2
    lst = lambda v: list(v) if isinstance(v, (list, tuple)) else [v] * 10
    ug = lambda: dict(eventos=eventos, cambia_1=max(eventos - 1, 0), cambia_0=min(eventos, 1), por_gen=[0] * 14)
    for b in ('lib', 'neu', 'mix', 'mixn'):
        for i in R[b]:
            if R[b][i].get('extinto'): continue
            R[b][i]['ungen'] = ug(); R[b][i]['estado'] = dict(R[b][i]['estado'], ungen=est_ungen, sha=sha)
    for i in range(10):
        if not R['neu'][i].get('extinto'): R['neu'][i]['R0_med'] = r0_neu
        R['lib'][i]['cruzan'] = lst(cruz_lib)[i]; R['o1'][i]['cruzan'] = lst(cruz_o1)[i]
    for b, nn in (('lib', n_lib), ('neu', n_neu)):
        for i in C[b]:
            for q in C[b][i]['pasajes']:
                q['ungen'] = ug(); q['estado'] = dict(q['estado'], ungen=est_ungen, sha=sha)
                q['siembra_info'] = dict(Ne_linajes=8.2, padres_distintos=24); q['fund_colonia'] = 100; q['fund_de_siembra'] = 9
            if C[b][i].get('extinto'): continue
            C[b][i]['siembra_final'] = [{k: CO.FABRICA[k] + s * (nn ** 0.5) * F.SIG_J[k] for k in CB.GENES} for s in (1, -1)]
    return C, R


M_CARGA = 'SOLO CARGA, NO SUBIDA'
M_NOPF2 = 'la carga se quito (el neutro no se degrada) y lib sigue bajo O1: la carga no era lo que tapaba'
M_NOPF1 = 'un gen por parto no quita la degradacion del neutro'
NADA = dict(gana_c=2, gana_n=2, pod_lib=0.3, pod_neu=0.3)   # ni PC ni PN ni PP
CASOS = [   # (nombre, kwargs, veredicto, matiz, en_umbral o None)
    ('FUNCIONA: PF1, PF2 (77 vs 70), PC y PN', dict(cruz_lib=[8] * 7 + [7] * 3), 'FUNCIONA', None, False),
    ('FUNCIONA sin PP (los poderes NO se exigen en F2)', dict(pod_lib=0.3, pod_neu=0.3, cruz_lib=[8] * 7 + [7] * 3), 'FUNCIONA', None, False),
    ('FUNCIONA con empate en cruces (70 vs 70): PF2 pasa, fuera del umbral (a 5 de -5)', dict(), 'FUNCIONA', None, False),
    ('MODESTO SOLO CARGA: PF1 y PF2 (70 vs 70) sin PC ni PP', dict(NADA), 'HAY ALGO MODESTO', M_CARGA, False),
    ('MODESTO: PF1, PF2 y PP sin PC (no es solo carga)', dict(gana_c=2, gana_n=2), 'HAY ALGO MODESTO', 'un poder se prende sin conquista; el deficit de lib frente a O1 no aparece', None),
    ('MODESTO: carga quitada, lib 75 vs o1 70, sin conquista, fuera del umbral', dict(NADA, cruz_lib=[8] * 5 + [7] * 5), 'HAY ALGO MODESTO', M_CARGA, False),
    ('MODESTO: PF + PC sin PN', dict(gana_n=3, pod_lib=0.3, pod_neu=0.3), 'HAY ALGO MODESTO', 'conquista, pero la deriva sola hace lo mismo', None),
    ('MODESTO: PC sin PF1 (neutro 0.80)', dict(r0_neu=0.80, pod_lib=0.3, pod_neu=0.3), 'HAY ALGO MODESTO',
     'conquista sin que el neutro deje de degradarse o con lib bajo O1 en monocultivo', None),
    ('MODESTO: solo PP', dict(gana_c=2, gana_n=2, r0_neu=0.80), 'HAY ALGO MODESTO', 'un poder se prende; la carga no explica el deficit', None),
    ('NO: PF1 pasa, lib 60 vs o1 70', dict(NADA, cruz_lib=6), 'NO', M_NOPF2, False),
    ('NO: PF1 falla (neutro 0.80), lib 60 vs 70', dict(NADA, r0_neu=0.80, cruz_lib=6), 'NO', M_NOPF1, False),
    ('NO EN EL UMBRAL: neutro 0.88 (a 0.02 de 0.90)', dict(NADA, r0_neu=0.88, cruz_lib=6), 'NO', M_NOPF1, True),
    ('NO fuera del umbral: neutro 0.86', dict(NADA, r0_neu=0.86, cruz_lib=6), 'NO', M_NOPF1, False),
    ('H-1 frontera PF2: lib 65 vs o1 70 (dif -5) PASA, en el umbral', dict(NADA, cruz_lib=[7] * 5 + [6] * 5), 'HAY ALGO MODESTO', M_CARGA, True),
    ('H-1 frontera PF2: lib 64 vs o1 70 (dif -6) NO pasa, en el umbral', dict(NADA, cruz_lib=[7] * 4 + [6] * 6), 'NO', M_NOPF2, True),
    ('H-1 umbral PF2: dif -9 dentro (a 4 de -5)', dict(NADA, cruz_lib=[7] * 1 + [6] * 9), 'NO', M_NOPF2, True),
    ('H-1 umbral PF2: dif -1 dentro (a 4 de -5)', dict(NADA, cruz_lib=[7] * 9 + [6] * 1), 'HAY ALGO MODESTO', M_CARGA, True),
    ('PF1 justo en 0.90 pasa', dict(NADA, r0_neu=0.90), 'HAY ALGO MODESTO', M_CARGA, True),
    ('PF1 en 0.8999 no pasa', dict(NADA, r0_neu=0.8999), 'NO', M_NOPF1, True),
    ('ERR-160 v: neutro extinto en 2 indices -> se lee (R0 del neutro extinto = 0; mediana 0.95)', dict(neu_ext=(0, 1), cruz_lib=[8] * 7 + [7] * 3), 'FUNCIONA', None, None),
    ('NO SE LEE: V7 sin telemetria de un gen (eventos 0: PS_UNGEN no estuvo prendido)', dict(eventos=0), 'NO SE LEE', None, None),
    ('NO SE LEE: V7 estado ungen 0', dict(est_ungen=0), 'NO SE LEE', None, None),
    ('NO SE LEE: V7 sha de otro carro', dict(sha='ff30214f59ed36d8'), 'NO SE LEE', None, None),
    ('NO SE LEE: V8 reloj del neutro 11.9 (el de 14 genes por parto)', dict(n_neu=11.9), 'NO SE LEE', None, None),
    ('NO SE LEE: V8 reloj 3.1', dict(n_neu=3.1), 'NO SE LEE', None, None),
    ('V8 reloj 3.0 pasa', dict(n_neu=3.0, cruz_lib=[8] * 7 + [7] * 3), 'FUNCIONA', None, None),
    ('NO SE LEE: V6 de o1_libre sigue mandando (el neutro activo un poder)', dict(neu_usa=1), 'NO SE LEE', None, None),
    ('NO SE LEE: V2 de o1_libre (O1 no vive)', dict(o1_R0=0.49), 'NO SE LEE', None, None),
]


def main():
    t0 = time.time()
    print(f"ARNES identidad_o1_libre_f2.py · practica 744950-744989 · runner {CO.h16(F.__file__)} · carro F2 {CO.h16(F.F2_PY)} · constructor {CO.h16(F.CF.__file__)}")
    # ---------------- (K)
    print("(K) shas, carro == constructor, identidad corta")
    chk("K1 verifica(): shas de o1_libre + O1_LIB_F2 == construye_o1_lib_f2 y el runner importado apunta al carro F2", F.verifica(lambda s: print('   ', s)))
    chk("K2 identidad_corta() del runner (o1_libre con el carro F2 + F2)", F.identidad_corta(lambda s: print('   ', s)))
    chk("K3 el origen de las anclas es el O1_LIB de o1_libre (sha ff30214f59ed36d8) y corre_o1_libre.py es 98d3a103a1fdde3b",
        CO.h16(F.ORIG_LIB_PY) == F.CF.SHA_LIB == 'ff30214f59ed36d8' and CO.h16(CO.__file__) == F.SHA_CO)
    o = open(F.ORIG_LIB_PY, encoding='utf-8').read().split('\n'); t = open(F.F2_PY, encoding='utf-8').read().split('\n')
    chk(f"K4 O1_LIB_F2 = O1_LIB + {len(t) - len(o)} lineas (4 anclas); quitando las nuevas queda el origen sin su linea 1",
        len(t) - len(o) == 11 and [x for x in t if x in set(o)] == o[1:])
    m = CO.carga_lib(); mo = IO.ld(F.ORIG_LIB_PY, 'carro_O1_LIB_orig_arnes'); o1 = CV.modulo('O1')
    chk("K5 el carro cargado por el runner es O1_LIB_F2 y nace con PS_UNGEN 0", os.path.abspath(m.__file__) == os.path.abspath(F.F2_PY) and m.PS_UNGEN == 0 and not hasattr(mo, 'PS_UNGEN'))
    # ---------------- (I)
    print("(I) identidad bit a bit con PS_UNGEN 0 (salida ENTERA + telemetria) y control con PS_UNGEN 1")
    Z = dict(CO.FABRICA); Z.update(MARGEN=0.31, PRUEBA=0.62, PEN_OTRO=0.27, D0=2.25, PISO=0.26, U4=4.75, U2=1.625, U1=0.875, XURG=0.36, TOPE=0.58, MEM=0.8, SOC=0.8, RES=0.8, PAU=0.8)
    a = corre(mo, 744951, 6000, 0, orig=True); b = corre(m, 744951, 6000, 0)
    npar = sum(len(v.get('partos', [])) for v in a[1].values()); ncol = sum(f[0] == 2 for v in a[1].values() for f in v.get('fund', []))
    chk(f"I1 mundo del bloque, sigma 0.03, PS_LEE 1, publica, colonia, sin siembra, T 6000 ({npar} partos, {ncol} refundaciones por colonia): salida ENTERA ==", a[0] == b[0] and npar > 0 and ncol > 0)
    chk("I1b ... y la telemetria (_TEL: vivos, fund, partos, activaciones) ==, sin clave 'ungen'", a[1] == b[1] and not any('ungen' in v for v in b[1].values()))
    c = corre(m, 744951, 6000, 1)
    chk("I2 control que puede fallar: con PS_UNGEN 1 la salida CAMBIA", c[0] != a[0])
    ev = sum(v['ungen'][0] for v in c[1].values()); npc = sum(len(v.get('partos', [])) for v in c[1].values()); nfc = sum(len(v.get('fund', [])) for v in c[1].values())
    chk(f"I3 con PS_UNGEN 1: eventos de mutacion ({ev}) == partos ({npc}) + fundadores ({nfc}); cambia_1 + cambia_0 == eventos",
        ev == npc + nfc and all(v['ungen'][1] + v['ungen'][2] == v['ungen'][0] and sum(v['ungen_j']) == v['ungen'][0] for v in c[1].values()))
    a = corre(mo, 744952, 3000, 0, siembra=[Z] * 3, lee=0, orig=True); b = corre(m, 744952, 3000, 0, siembra=[Z] * 3, lee=0)
    chk("I4 neutro (PS_LEE 0) con siembra Z, T 3000: PS_UNGEN 0 == O1_LIB (salida ENTERA y telemetria)", a == b)
    a = corre(mo, 744953, 2000, 0, escribe=0, coloniza=0, mundo=None, orig=True); b = corre(m, 744953, 2000, 0, escribe=0, coloniza=0, mundo=None)
    chk("I5 pista vieja, sin colonia ni publicar, T 2000: PS_UNGEN 0 == O1_LIB (salida ENTERA y telemetria)", a == b)
    d = corre(m, 744954, 3000, 1, siembra=[Z] * 3, lee=0, escribe=0); k = dict(T=3000, pizarra=1, rep_acum=0, escala=1, mundo_n=None, fundador_limpio=1)
    chk("I6 con PS_UNGEN 1 el NEUTRO (PS_LEE 0) sigue siendo O1 bit a bit en el mundo del bloque (los genes no se leen)",
        d[0] == N(PL.run(744954, [('X', o1)] * 9, **k, **PL.MUNDO_LIBRE)) and sum(v['ungen'][0] for v in d[1].values()) > 0
        and all(v['activaciones'][q] == 0 for v in d[1].values() for q in ('mem', 'pau', 'soc', 'res')))
    # ---------------- (U)
    print("(U) un gen por evento (sin pista)")
    Zl = [float(Z[g]) for g in CB.GENES]; sig = [0.03 * e for e in CB.ESCALA]
    ctx = lambda j: dict(L=360, rep_umbral=1.0, rng=np.random.default_rng(j), id=f'X{j}', indice=j)
    ndif = lambda x, y: sum(p != q for p, q in zip(x, y))
    F.UNGEN = 1; CO._pon_lib(m, 744960, [Z], 1, 0, 0.03, 0)
    fd = [ndif(m.crea(ctx(0))._gen, Zl) for _ in range(300)]
    chk(f"U1 fundador (300 instancias desde la siembra Z, genes interiores): cambia EXACTAMENTE 1 gen (histograma {sorted(set(fd))})", set(fd) == {1})
    cu = m.crea(ctx(1)); padre = list(cu._gen); hs = [cu.al_parir(dict(t=q, k=1))['_gen'] for q in range(4200)]
    dj = [[j for j in range(14) if h[j] != padre[j]] for h in hs]
    chk("U2 4200 partos de un padre (genes interiores): cada hijo cambia EXACTAMENTE 1 gen; el padre no cambia; el parto anota al PADRE",
        all(len(x) == 1 for x in dj) and list(cu._gen) == padre and m._TEL[1]['partos'][-1] == [4199, padre])
    cnt = [sum(1 for x in dj if x == [j]) for j in range(14)]
    chk(f"U3 eleccion uniforme entre los 14 genes (esperado 300 por gen, sd 16.7; conteos {cnt})", all(216 <= x <= 384 for x in cnt) and sum(m._TEL[1]['ungen_j']) == 4201 and all(a_ - b_ in (0, 1) for a_, b_ in zip(m._TEL[1]['ungen_j'], cnt)))
    zz = [(h[x[0]] - padre[x[0]]) / sig[x[0]] for h, x in zip(hs, dj)]
    chk(f"U4 el paso del gen mutado es N(0, sigma_j) de O1_LIB: media {np.mean(zz):.3f}, sd {np.std(zz):.3f} (z = delta / sigma_j; clip lejos)",
        abs(np.mean(zz)) < 0.06 and 0.95 < np.std(zz) < 1.05)
    mem = cu.al_parir(dict(t=5000, k=1)); hijo = list(mem['_gen']); cu.nace(dict(t=5001, k=1, fundador=False, memoria=mem, rng_hijo=np.random.default_rng(1)))
    chk("U5 nace: el cuerpo nuevo lleva EXACTAMENTE los genes del hijo y los LEE", cu._gen == hijo and cu.MARGEN == hijo[0] and cu.MEM == hijo[10] and '_gen' not in cu.n)
    CO._pon_lib(m, 744961, None, 1, 0, 0.03, 0)   # fabrica: los 4 poderes en 0 (borde del recorte)
    cf = m.crea(ctx(2)); cf._gen = list(CB.FABRICA); uj0 = list(m._TEL[2]['ungen_j']); u0 = list(m._TEL[2]['ungen']); hf = [cf.al_parir(dict(t=q, k=1))['_gen'] for q in range(4200)]
    n0 = sum(ndif(h, CB.FABRICA) == 0 for h in hf); n1 = sum(ndif(h, CB.FABRICA) == 1 for h in hf); u = m._TEL[2]['ungen']; uj = m._TEL[2]['ungen_j']
    pod0 = sum(uj[10:]) - sum(uj0[10:]) - sum(1 for h in hf if any(h[j] != 0.0 for j in range(10, 14)))
    chk(f"U6 desde FABRICA (poderes en 0): {n1} hijos cambian 1 gen y {n0} cambian 0; los 0 son SOLO poderes clavados por el recorte en 0 "
        f"(telemetria cambia_0 {u[2] - u0[2]}; esperado ~ 4200 x 4/14 x 1/2 = 600)", n0 + n1 == 4200 and 500 <= n0 <= 700 and pod0 == n0 == u[2] - u0[2]
        and all(0.0 <= h[j] <= 1.0 for h in hf for j in range(10, 14)))
    S5 = [dict(Z, MARGEN=0.05 * q, PRUEBA=0.3 + 0.1 * q) for q in range(5)]; L5 = [[float(e[g]) for g in CB.GENES] for e in S5]
    cual = lambda gen: [q for q in range(5) if ndif(gen, L5[q]) <= 1]   # las entradas difieren en 2 genes: la base es la unica a <= 1 gen
    F.UNGEN = 1; CO._pon_lib(m, 744962, S5, 1, 0, 0.03, 0); e1 = [cual(m.crea(ctx(3))._gen) for _ in range(40)]
    F.UNGEN = 0; F._ORIG['pon'](mo, 744962, S5, 1, 0, 0.0, 0); e0 = [cual(mo.crea(ctx(3))._gen) for _ in range(40)]
    chk(f"U7 la ELECCION de la entrada de siembra (self._psrng) es la misma con PS_UNGEN 1 que en O1_LIB (40 fundadores, 5 entradas; O1_LIB con sigma 0 da la entrada exacta)", e1 == e0 and all(len(x) == 1 for x in e0) and len({x[0] for x in e0}) > 1)
    F.UNGEN = 0; CO._pon_lib(m, 744960, [Z], 1, 0, 0.03, 0); c0 = m.crea(ctx(1)); h0 = [c0.al_parir(dict(t=q, k=1))['_gen'] for q in range(200)]
    F._ORIG['pon'](mo, 744960, [Z], 1, 0, 0.03, 0); co = mo.crea(ctx(1)); ho = [co.al_parir(dict(t=q, k=1))['_gen'] for q in range(200)]
    chk("U8 con PS_UNGEN 0: los 14 genes mutan en cada parto, sin telemetria 'ungen', y los 200 hijos son IDENTICOS a los de O1_LIB de o1_libre",
        all(ndif(h, c0._gen) == 14 for h in h0) and 'ungen' not in m._TEL[1] and h0 == ho and c0._gen == co._gen)
    CO._apaga_lib(m); F._ORIG['apaga'](mo); F.UNGEN = 1
    # ---------------- (R)
    print("(R) reloj mutacional")
    DO = os.path.join(F.OL, 'datos')
    for pat, esp in (('serie_i734201-*', 11.87), ('replica_i734501-*', 11.65)):
        ns = [F.reloj(json.load(open(f, encoding='utf-8'))['siembra_final']) for f in sorted(glob.glob(os.path.join(DO, pat, 'cadena_i*_neu.json')))]
        chk(f"R1 reloj() sobre el neutro de o1_libre {pat}: media {np.mean(ns):.2f} (auditoria F0, 10 genes: {esp}); mediana {np.median(ns):.2f}; {len(ns)} cadenas",
            len(ns) == 10 and abs(np.mean(ns) - esp) <= 0.05)
    sie = [{g: CO.FABRICA[g] + s * 2.0 * F.SIG_J[g] for g in CB.GENES} for s in (1, -1)]
    chk("R2 sintetico: todos los genes a 2 sigma_j de fabrica -> n = 4; siembra de fabrica -> 0; None -> None",
        F.reloj(sie) == 4.0 and F.reloj([dict(CO.FABRICA)]) == 0.0 and F.reloj(None) is None)
    rng = np.random.default_rng(744963); G = []
    for _ in range(4000):   # 12 eventos de UN gen al azar por genoma
        g = dict(CO.FABRICA)
        for j in rng.integers(14, size=12): g[CB.GENES[j]] += F.SIG_J[CB.GENES[j]] * rng.normal()
        G.append(g)
    chk(f"R3 simulacion: 12 eventos de UN gen por evento -> n por gen = {F.reloj(G):.3f} (esperado 12/14 = 0.857)", abs(F.reloj(G) - 12 / 14) < 0.05)
    # ---------------- (G)
    print("(G) regla 14: lo importado sigue siendo lo de o1_libre")
    ref = N(CV.tarea((744964, 'O1', 1500))); to = N(CO.tarea(744964, 'o1', 1500, mundo=PL.MUNDO_VIEJO))
    dif = [q for q in sorted(set(ref) | set(to)) if q not in ('seg', 'tel', 'libre', 'estado') and ref.get(q) != to.get(q)]
    chk(f"G1 tarea('o1', mundo viejo) (redirigida) == corre_v143.tarea campo a campo en {len(set(ref) | set(to)) - 4} campos (salvo seg/tel/libre/estado); difieren {dif}; estado sin 'ungen'",
        not dif and 'ungen' not in to['estado'])
    x = CO.tarea(744965, 'mix:1', 1500, siembra=[dict(CO.FABRICA)], lee=1)
    f2 = CO.fila(x, 1500, 'mix:1', 1); f1 = F._ORIG['fila'](x, 1500, 'mix:1', 1)
    chk(f"G2 fila() redirigida == fila() de o1_libre + la clave 'ungen' ({f2['ungen']['eventos']} eventos); estado: carro O1_LIB, ungen 1, sha del carro F2",
        {q: v for q, v in f2.items() if q != 'ungen'} == f1 and f2['ungen']['eventos'] > 0 and x['estado']['ungen'] == 1 and x['estado']['sha'] == F.SHA_F2)
    chk("G3 mixA NO se corre: DESCRIPTIVAS vacio, TODAS == PRUEBAS == las 5 de la letra; N_IND 10, NPAS 3, T 100k, N_SIEMBRA 90, sigma 0.03, mundo del bloque (iguales a o1_libre)",
        CO.DESCRIPTIVAS == () and CO.TODAS == CO.PRUEBAS == ('lib', 'neu', 'o1', 'mix', 'mixn') and (F.N_IND, F.NPAS, F.T_PAS, F.T_PRU, CO.N_SIEMBRA, F.SIGMA) == (10, 3, 100000, 100000, 90, 0.03)
        and CO.MUNDO == PL.MUNDO_LIBRE)
    # ---------------- (L)
    print("(L) LA LETRA de F2 en casos sinteticos (n = 10)")
    for nombre, kw, esperado, matiz, umb in CASOS:
        C, R = sint(**kw); L = F.lee_serie(C, R, 10, 0)
        chk(f"L {nombre}: {L['veredicto']} ({L['matiz']}; umbral {L['en_umbral']})",
            L['veredicto'] == esperado and (esperado == 'NO SE LEE' or L['matiz'] == matiz) and (umb is None or L['en_umbral'] == umb))
    C, R = sint(**dict(NADA, n_lib=0.3, n_neu=0.9)); L = F.lee_serie(C, R, 10, 0); d = L['descriptivo']
    chk(f"L firma de PURGA (descriptiva): reloj lib 0.3 <= mitad del neutro 0.9 y sin conquista -> {d['F2']['firma_purga']}; relojes {d['relojes']['neu']['n_por_gen']['mediana']}/{d['relojes']['lib']['n_por_gen']['mediana']}",
        d['F2']['firma_purga'] is True and d['relojes']['neu']['n_por_gen']['mediana'] == 0.9 and d['relojes']['neu']['eventos_equivalentes_14n'] == 12.6
        and d['relojes']['neu']['Ne_linajes_por_pasaje'] == [8.2] * 3 and d['relojes']['lib']['fund_colonia_por_pasaje'] == [100] * 3)
    C, R = sint(**dict(NADA, cruz_lib=[8] * 7 + [7] * 3)); a7 = F.lee_serie(C, R, 10, 0)['descriptivo']['F2']['lib_supera_o1_con_margen']
    C, R = sint(**dict(NADA, cruz_lib=[8] * 6 + [7] * 4)); a6 = F.lee_serie(C, R, 10, 0)['descriptivo']['F2']['lib_supera_o1_con_margen']
    chk(f"L 'lib supera a o1 con margen' (descriptivo): +7 -> {a7}; +6 -> {a6}", a7 is True and a6 is False)
    sc = lambda **kw: F.lee_serie(*sint(**kw), 10, 0)['solo_carga']
    chk("L H-2 clave solo_carga: True solo con PF1 y PF2 sin PC ni PP; False en FUNCIONA, en NO y con PP; MARGEN_PF2 == 5",
        sc(**NADA) is True and sc() is False and sc(**dict(NADA, cruz_lib=6)) is False and sc(gana_c=2, gana_n=2) is False and F.MARGEN_PF2 == 5)
    C, R = sint(); del R['mixn'][9]; L = F.lee_serie(C, R, 10, 0)
    chk(f"L serie INCOMPLETA (falta una prueba): {L['veredicto']}", L['veredicto'] == 'NO SE LEE')
    C, R = sint(); L = F.lee_serie(C, R, 10, 1)
    chk(f"L un aborto: {L['veredicto']}", L['veredicto'] == 'NO SE LEE')
    chk("L bloque: MODESTO + NO -> NO; FUNCIONA + MODESTO -> MODESTO; NO SE LEE manda", CO.bloque('HAY ALGO MODESTO', 'NO') == 'NO'
        and CO.bloque('FUNCIONA', 'HAY ALGO MODESTO') == 'HAY ALGO MODESTO' and CO.bloque('FUNCIONA', 'NO SE LEE') == 'NO SE LEE')
    # ---------------- (J)
    print("(J) guardas")
    for args in (['--humo', '--pool', '2'], ['--serie', '--pool', '3'], ['--seri'], ['--humo', '--x']):
        try: F.main(args); r = 'corre'
        except SystemExit: r = 'aborta'
        chk(f"J1 {args} aborta", r == 'aborta')
    S = [CO.sem_pas(F.BASES[b], i, p) for b in F.BASES for i in range(F.N_IND) for p in range(F.NPAS)] + [CO.sem_pru(F.BASES[b], i) for b in F.BASES for i in range(F.N_IND)]
    H = [CO.sem_pas(F.HUMO['base'], 0, p) for p in range(F.HUMO['npas'])] + [F.HUMO['base'][1]]
    chk(f"J2 semillas serie/replica/humo disjuntas, en 744xxx, fuera de 734xxx (o1_libre) y de la practica del arnes ({len(S)} + {len(H)})",
        len(set(S)) == len(S) == 80 and not set(S) & set(H) and all(744000 <= x < 745000 for x in S + H) and not set(S + H) & set(range(744950, 744990)))
    p1 = 2 * F.HUMO['npas'] * F.HUMO['T_pas'] + 2 * F.HUMO['T_pru']; p2 = 3 * F.HUMO['T_pru']
    chk(f"J3 el humo cabe: proceso 1 {2 * F.HUMO['npas'] + 2} corridas {p1} pasos; proceso 2 3 corridas {p2} pasos (<= 6 y <= 200 000)",
        2 * F.HUMO['npas'] + 2 <= 6 and p1 <= 200000 and p2 <= 200000)
    # ---------------- (P)
    print("(P) ruta --serie --pool 2 con Pool FALSO de un proceso (T 3000/1500, 1 indice, 1 pasaje, practica), candado y parada")
    import multiprocessing
    class _R:
        def __init__(self, v): self.v = v
        def ready(self): return True
        def get(self): return self.v
    class _Falso:
        def __init__(self, n): self.n = n
        def __enter__(self): return self
        def __exit__(self, *a): return False
        def apply_async(self, f, args): return _R(f(*args))
    guard = dict(Pool=multiprocessing.Pool, git=CO.git_limpio, N=F.N_IND, NP=F.NPAS, TP=F.T_PAS, TR=F.T_PRU, B=dict(F.BASES), D=F.DATOS, CD=CO.DATOS)
    tmp = tempfile.mkdtemp(prefix='o1libre_f2_pool_')
    try:
        multiprocessing.Pool = _Falso; CO.git_limpio = lambda r, log: True
        F.N_IND = 1; F.NPAS = 1; F.T_PAS = 3000; F.T_PRU = 1500; F.BASES.update(serie=(744970, 744975), replica=(744980, 744985)); F.DATOS = tmp; CO.DATOS = tmp
        rc = F.main(['--serie', '--pool', '2'])
        car = IO.glob_uno(os.path.join(tmp, 'serie_*'))
        js = sorted(os.path.basename(x) for x in os.listdir(car) if x.endswith('.json'))
        esperado = ['cadena_i00_lib.json', 'cadena_i00_neu.json', 'pasaje_i00_lib_p00.json', 'pasaje_i00_neu_p00.json'] + [f'prueba_i00_{b}.json' for b in F.PRUEBAS] + ['resumen.json']
        rs = json.load(open(os.path.join(car, 'resumen.json'), encoding='utf-8'))
        chk(f"P1 --serie --pool 2 (Pool falso): rc 0, 2 cadenas y 5 pruebas (sin mixA), 0 abortos, resumen ({rs['veredicto']}); V1 {rs['letra']['validez']['V1_completa']} V7 {rs['letra']['validez']['V7_un_gen']}",
            rc == 0 and js == sorted(esperado) and rs['abortos'] == [] and rs['letra']['validez']['V1_completa'] and rs['letra']['validez']['V7_un_gen'] and rs['ungen'] == 1)
        pj = json.load(open(os.path.join(car, 'pasaje_i00_neu_p00.json'), encoding='utf-8'))['fila']
        chk(f"P2 el JSON del pasaje guarda los dos relojes: ungen {pj['ungen']['eventos']} eventos, estado ungen {pj['estado']['ungen']}, fund_colonia {pj['fund_colonia']}, siembra_info {bool(pj['siembra_info'])}",
            pj['ungen']['eventos'] > 0 and pj['estado']['ungen'] == 1 and pj['estado']['sha'] == F.SHA_F2 and 'fund_colonia' in pj)
        chk("P3 candado: una segunda --serie sobre una carpeta existente (sin --reanuda) se niega (rc 1)", F.main(['--serie', '--pool', '2']) == 1)
        n_antes = len(os.listdir(car)); rr = F.main(['--serie', '--pool', '2', '--reanuda'])
        chk(f"P4 --reanuda sobre una serie con veredicto se niega (o, si era NO SE LEE, no re-corre nada): rc {rr}, archivos {n_antes} -> {len(os.listdir(car))}", len(os.listdir(car)) == n_antes)
        vs = rs['letra']['veredicto']; um = rs['letra']['en_umbral']
        rr = F.main(['--replica', '--pool', '2']); permite = vs in ('FUNCIONA', 'HAY ALGO MODESTO') or (vs == 'NO' and um)
        chk(f"P5 regla de parada: serie {vs} (umbral {um}) -> replica {'corre' if permite else 'se niega'} (rc {rr})", (rr == 0) == permite)
        class _Muere(_Falso):   # H-7: un Pool cuyos trabajos no vuelven y cuyos pids cambian (un hijo murio y fue reemplazado)
            k = [0]
            @property
            def _pool(self): self.k[0] += 1; return [type('W', (), dict(pid=self.k[0]))()]
            def apply_async(self, f, args): return type('Nunca', (), dict(ready=lambda s: False))()
            def terminate(self): pass
        for z in glob.glob(os.path.join(car, 'prueba_i00_mix*.json')): os.remove(z)
        rsj = os.path.join(car, 'resumen.json'); sha_r = CO.h16(rsj); multiprocessing.Pool = _Muere; t7 = time.time()
        r7 = F.main(['--serie', '--pool', '2', '--reanuda']); multiprocessing.Pool = _Falso
        chk(f"P7 H-7: un hijo del Pool muere -> el bucle NO queda colgado: sale con rc {r7} y mensaje de --reanuda en {time.time() - t7:.0f}s, sin tocar el resumen",
            r7 == 2 and CO.h16(rsj) == sha_r)
        sha_ok = F.SHA_F2; F.SHA_F2 = '0' * 16
        try:
            try: F.trabajo(('prueba', 0, 'o1', F.BASES['serie'], 1, 3000, 1500, tmp, True)); r8 = 'corre'
            except RuntimeError as e8: r8 = 'aborta: ' + str(e8)[:24]
        finally: F.SHA_F2 = sha_ok
        F.UNGEN = 0
        try:
            try: F.trabajo(('prueba', 0, 'o1', F.BASES['serie'], 1, 3000, 1500, tmp, True)); r9 = 'corre'
            except RuntimeError: r9 = 'aborta'
        finally: F.UNGEN = 1
        F.comprueba_f2()
        chk(f"P8 H-5: trabajo() aborta de inmediato (RuntimeError) si el sha del carro no es el de F2 ({r8}) o si PS_UNGEN no queda en 1 ({r9}); con todo bien, pasa",
            r8.startswith('aborta') and r9 == 'aborta')
        falsa = os.path.join(tmp, f"serie_i{F.BASES['serie'][1]}-{F.BASES['serie'][1]}_zz_falsa"); os.makedirs(falsa)
        json.dump(dict(modo='serie', humo=False, sha_runner='0000000000000000', letra=dict(veredicto='HAY ALGO MODESTO', en_umbral=False)), open(os.path.join(falsa, 'resumen.json'), 'w', encoding='utf-8'))
        nrep = lambda: len([x for x in os.listdir(tmp) if x.startswith('replica_')]); n0 = nrep(); r1 = F.main(['--replica', '--pool', '2'])
        chk(f"P6 serie con sha_runner ajeno -> la replica se niega sin crear carpeta (rc {r1})", r1 == 1 and nrep() == n0)
    finally:
        multiprocessing.Pool = guard['Pool']; CO.git_limpio = guard['git']; F.N_IND = guard['N']; F.NPAS = guard['NP']; F.T_PAS = guard['TP']
        F.T_PRU = guard['TR']; F.BASES.clear(); F.BASES.update(guard['B']); F.DATOS = guard['D']; CO.DATOS = guard['CD']
        shutil.rmtree(tmp, ignore_errors=True)
    print(f"\nARNES {'PASA' if OK[0] else 'NO PASA'}: {NCHK[1]}/{NCHK[0]} · {time.time() - t0:.1f}s")
    return 0 if OK[0] else 1


if __name__ == '__main__':
    sys.exit(main())
