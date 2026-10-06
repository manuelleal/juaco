"""identidad_o1_libre.py — ARNES de o1_libre (O1 libre con poderes). Un proceso; semillas de practica 734950-734989. Escribe su salida en
identidad_o1_libre_salida.txt (la escribe el que lo corre con tee; el arnes no escribe nada fuera de un directorio temporal).
(K) shas fijados + carros == construye_o1_lib + identidad corta del runner; las 5 constantes del modulo O1 == FABRICA del constructor.
(a) MUNDO: pista_libre con las 3 perillas en 0 == pista.run SALIDA ENTERA (O1 x9 con fundador limpio; mezcla O1/V143; FABRICA compat=1).
(b) CARRO: O1_LIB0 == O1; O1_LIB sigma 0 sin siembra == O1; con siembra de fabrica == O1 (salida ENTERA, pista vieja y pista_libre).
(c) CABLEADO de los 10 genes de O1: O1_LIB sigma 0 con genes X == O1_MANO (texto de O1.py con las 10 constantes cambiadas a X, aqui) y
    != O1 (control que puede fallar); y O1_LIB con los 4 genes de o1_evo == O1_PAS (carro de o1_evo, sha fijado) con los mismos 4.
(d) NEUTRO: PS_LEE 0, sigma 0.03, siembra con poderes 0.8 y genes de O1 movidos == O1 (salida ENTERA, pista vieja y pista_libre);
    d1c-d1d (R-3): el neutro REAL del bloque (coloniza 1) en pista_libre T 3000 con refundaciones por colonia == O1 (y fisica == O1 publicando);
    los genes igual se mueven; las activaciones de los poderes quedan en 0.
(e) PODERES: cada uno solo (0.6, sigma 0) en pista_libre cambia la salida, sus activaciones > 0 y las de los otros tres == 0.
    PUBLICAR (PS_ESCRIBE 1) sin poderes: la FISICA del juez == O1 (solo cambian las escrituras) y la pizarra tiene entradas.
(f) PERILLAS DEL MUNDO: cada una sola cambia la salida y su contador > 0; la estacion convierte en los dos sentidos a T 16k.
(g) REGLA 14: tarea_lista(9 x O1, mundo viejo) == corre_v143.tarea campo a campo (salvo 'seg'); tarea('o1', mundo viejo) tambien
    (salvo 'seg', 'tel', 'libre', 'estado'); tarea('mix') pone O1_LIB en las casillas de su indice.
(h) SIEMBRA: solo lee 'partos'; excluye t < T/2 (si no hay tardios, todo el pasaje); pesa por partos; None si no hay partos;
    h5-h6 (ERR-160 v): una cadena sin partos en un pasaje entero se EXTINGUE como dato (sin aborto) y sus pruebas quedan 'extinto'.
(i) LA LETRA en casos sinteticos (incluye los 2 de ERR-160).
(j) guardas: banderas; --pool 3 aborta; --humo con --pool aborta; semillas disjuntas y en 734xxx; el humo cabe (<= 6 corridas y <= 200k pasos por proceso).
(k) la ruta --serie --pool 2 con un Pool FALSO de un proceso (T corto, practica): encola cada prueba tras su cadena; mixA con poderes en 0;
    candado; regla de parada; k4: la rama que PERMITE la replica y el candado de sha_runner.
(d6-d7) herencia directa del gen al hijo con sigma > 0 (auditoria H-8).
"""
import copy, importlib.util, json, os, re, shutil, sys, tempfile, time

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
import corre_o1_libre as CO
CV = CO.CV; P = CO.P; PL = CO.PL; CB = CO.CB; J = CO.J
RAIZ = CO.RAIZ

N = lambda x: json.loads(json.dumps(x, default=str, sort_keys=True))
OK = [True]; NCHK = [0, 0]
T_ID = 2000


def chk(nombre, c):
    c = bool(c); OK[0] &= c; NCHK[0] += 1; NCHK[1] += int(c); print(f"  {'OK   ' if c else 'FALLA'} {nombre}", flush=True)


def ld(ruta, et):
    s = importlib.util.spec_from_file_location(et, ruta); m = importlib.util.module_from_spec(s); s.loader.exec_module(m); return m


def run(mods, seed, T=T_ID, mundo=None, **kw):
    carros = [('X', mods)] * 9 if not isinstance(mods, list) else mods
    f = PL.run if mundo is not None else P.run
    k = dict(T=T, pizarra=1, rep_acum=0, escala=1, mundo_n=None, fundador_limpio=1); k.update(kw)
    return N(f(seed, carros, **k, **(mundo or {})))


def fija(m, siembra=None, sigma=0.0, seed=0, lee=1, escribe=0, coloniza=0):
    CO._pon_lib(m, seed, siembra, lee, escribe, sigma, coloniza)


def o1_mano(X):
    """El texto de O1.py con las 10 constantes cambiadas a X (reemplazo textual exacto; cada una EXACTAMENTE una vez)."""
    src = open(os.path.join(CO.PISTA, 'carros', 'O1.py'), encoding='utf-8').read()
    reps = [('MARGEN = 0.25 ', f"MARGEN = {X['MARGEN']!r} "), ('PRUEBA = 0.5 ', f"PRUEBA = {X['PRUEBA']!r} "),
            ('PEN_OTRO = 0.35 ', f"PEN_OTRO = {X['PEN_OTRO']!r} "), ('D0 = 3.0 ', f"D0 = {X['D0']!r} "), ('PISO = 0.2 ', f"PISO = {X['PISO']!r} "),
            ('u = 4.0 if x < 0.3 else (2.0 if x < self.U else 1.0)', f"u = {X['U4']!r} if x < {X['XURG']!r} else ({X['U2']!r} if x < self.U else {X['U1']!r})"),
            ('self.U + 0.5 - x', f"self.U + {X['TOPE']!r} - x")]
    for a, b in reps:
        if src.count(a) != 1: raise SystemExit(f"o1_mano: {a!r} aparece {src.count(a)} veces")
        src = src.replace(a, b)
    d = tempfile.mkdtemp(prefix='o1mano_'); ruta = os.path.join(d, 'O1_MANO.py')
    open(ruta, 'w', encoding='utf-8').write(src)
    m = ld(ruta, 'carro_O1_MANO_' + str(abs(hash(tuple(X.values())))))
    shutil.rmtree(d, ignore_errors=True)
    return m


def main():
    t0 = time.time()
    print("ARNES identidad_o1_libre.py · practica 734950-734989 · T", T_ID)
    # ---------------- (K)
    print("(K) shas, carros, identidad corta, fabrica")
    chk("K1 verifica(): shas fijados y carros == construye_o1_lib", CO.verifica(lambda s: print('   ', s)))
    chk("K2 identidad_corta() del runner", CO.identidad_corta(lambda s: print('   ', s)))
    o1 = CV.modulo('O1')
    chk("K3 las 5 constantes de modulo de O1 == FABRICA del constructor", tuple(getattr(o1, k) for k in CB.GLOBALES_O1) == CB.FABRICA[:5])
    chk("K4 poderes de fabrica == 0 y clip [0, 1]", all(CO.FABRICA[k] == 0.0 for k in CB.PODERES) and all(CB.CLIP[CB.GENES.index(k)] == (0.0, 1.0) for k in CB.PODERES))
    m = CO.carga_lib(); m0 = ld(CO.LIB0_PY, 'carro_O1_LIB0_arnes')
    # ---------------- (a) mundo
    print("(a) pista_libre apagada == pista (salida ENTERA)")
    for s in (734951, 734952):
        chk(f"a1 O1 x9 s{s}: pista_libre(0,0,0) == pista.run", run(o1, s, mundo=PL.MUNDO_VIEJO) == run(o1, s))
    v143 = CV.modulo('V143')
    mez = [('O1', o1), ('V143', v143)] * 4 + [('O1', o1)]
    chk("a2 mezcla O1/V143 s734953: pista_libre(0,0,0) == pista.run", run(mez, 734953, mundo=PL.MUNDO_VIEJO) == run(mez, 734953))
    fab = P.carga_carro('FABRICA')
    a = N(P.run(734954, [('F', fab)], T=3000, pizarra=0, compat=1)); b = N(PL.run(734954, [('F', fab)], T=3000, pizarra=0, compat=1, **PL.MUNDO_VIEJO))
    chk("a3 FABRICA compat=1 (el ancla del monolito): pista_libre(0,0,0) == pista.run, rng del mundo incluido", a == b)
    # ---------------- (b) carro
    print("(b) O1_LIB == O1 con todo en fabrica")
    base = run(o1, 734955)
    chk("b1 O1_LIB0 (PASAJE 0) == O1", run(m0, 734955) == base)
    fija(m, None, 0.0, 734955); chk("b2 O1_LIB sigma 0, SIEMBRA None, PS_ESCRIBE 0 == O1", run(m, 734955) == base)
    fija(m, [dict(CO.FABRICA)] * 3, 0.0, 734955); chk("b3 O1_LIB sigma 0, SIEMBRA de fabrica == O1", run(m, 734955) == base)
    baseL = run(o1, 734956, mundo=PL.MUNDO_LIBRE)
    fija(m, [dict(CO.FABRICA)] * 3, 0.0, 734956); chk("b4 en pista_libre (mundo prendido): O1_LIB sigma 0 fabrica == O1", run(m, 734956, mundo=PL.MUNDO_LIBRE) == baseL)
    chk("b5 O1_LIB0 == O1 en pista_libre", run(m0, 734956, mundo=PL.MUNDO_LIBRE) == baseL)
    fija(m, [dict(CO.FABRICA)] * 3, 0.0, 734956, escribe=0, coloniza=1)
    chk("b6 con COLONIZACION (PS_COLONIZA 1), sigma 0 y fabrica == O1 en pista_libre (colonizar no cambia decisiones)",
        run(m, 734956, mundo=PL.MUNDO_LIBRE) == baseL)
    # ---------------- (c) cableado
    print("(c) cableado de los 10 genes de O1")
    X = dict(CO.FABRICA); X.update(MARGEN=0.31, PRUEBA=0.62, PEN_OTRO=0.27, D0=2.25, PISO=0.26, U4=4.75, U2=1.625, U1=0.875, XURG=0.36, TOPE=0.58)
    mano = o1_mano(X)
    fija(m, [X], 0.0, 734957); cab = run(m, 734957)
    chk("c1 O1_LIB sigma 0 con genes X == O1_MANO(X) (salida ENTERA)", cab == run(mano, 734957))
    chk("c2 ... y != O1 (los genes actuan; control que puede fallar)", cab != run(o1, 734957))
    fija(m, [X], 0.0, 734958); chk("c3 idem en pista_libre", run(m, 734958, mundo=PL.MUNDO_LIBRE) == run(mano, 734958, mundo=PL.MUNDO_LIBRE))
    for k in CB.GENES_O1:   # cada gen por separado actua (su cableado no es un no-op)
        Y = dict(CO.FABRICA); Y[k] = X[k]
        fija(m, [Y], 0.0, 734959); chk(f"c4 gen {k} solo ({CO.FABRICA[k]} -> {X[k]}) == O1_MANO", run(m, 734959, T=1500) == run(o1_mano(Y), 734959, T=1500))
    pas_py = os.path.join(RAIZ, 'experimentos', 'organelos', 'o1_evo', 'carros', 'O1_PAS.py')
    chk("c5 O1_PAS de o1_evo con sha fijado c5377ada6b28bee0 (solo se lee)", CO.h16(pas_py) == 'c5377ada6b28bee0')
    pas = ld(pas_py, 'carro_O1_PAS_arnes')
    X4 = dict(CO.FABRICA); X4.update(MARGEN=0.31, PRUEBA=0.62, PEN_OTRO=0.27, PISO=0.26)
    pas.SIEMBRA = [{k: X4[k] for k in pas.PS_GENES}]; pas.PS_SIGMA = 0.0; pas.PS_SEMILLA = 734960; pas.PS_LEE = 1; pas._TEL.clear(); pas._PS_CNT.clear()
    rp = run(pas, 734960)
    fija(m, [X4], 0.0, 734960); chk("c6 O1_LIB con los 4 genes de o1_evo == O1_PAS con los mismos 4 (otro equipo, otro constructor)", run(m, 734960) == rp)
    # ---------------- (d) neutro
    print("(d) neutro: PS_LEE 0")
    Z = dict(X); Z.update(MEM=0.8, SOC=0.8, RES=0.8, PAU=0.8)
    fija(m, [Z], 0.03, 734961, lee=0); rn = run(m, 734961); tel = copy.deepcopy(m._TEL)
    chk("d1 PS_LEE 0, sigma 0.03, siembra Z (poderes 0.8) == O1 (salida ENTERA)", rn == run(o1, 734961))
    g0 = tel[0]['fund'][0][1]
    chk("d2 ... y los genes igual se mueven (el fundador lleva Z + ruido, no fabrica)", abs(g0[CB.GENES.index('MEM')] - 0.8) < 0.2 and g0 != list(CB.FABRICA))
    chk("d3 ... y las activaciones de los poderes quedan en 0", all(tel[i]['activaciones'][k] == 0 for i in tel for k in ('mem', 'pau', 'soc', 'res')))
    fija(m, [Z], 0.03, 734962, lee=0, escribe=0); rnL = run(m, 734962, mundo=PL.MUNDO_LIBRE)
    chk("d4 idem en pista_libre (el mundo del bloque)", rnL == run(o1, 734962, mundo=PL.MUNDO_LIBRE))
    # R-3: el NEUTRO REAL del bloque (PS_LEE 0, sigma 0.03, COLONIZA 1) en pista_libre, T 3000, con refundaciones por colonia
    fija(m, [Z], 0.03, 734961, lee=0, escribe=0, coloniza=1); rc = run(m, 734961, T=3000, mundo=PL.MUNDO_LIBRE)
    orig = [f[0] for i in m._TEL for f in m._TEL[i].get('fund', [])]
    chk(f"d1c neutro real (PS_LEE 0, sigma 0.03, coloniza 1, pista_libre, T 3000) == O1 salida ENTERA, con refundaciones por colonia ({orig.count(2)} de {len(orig)})",
        rc == run(o1, 734961, T=3000, mundo=PL.MUNDO_LIBRE) and orig.count(2) > 0)
    fija(m, [Z], 0.03, 734961, lee=0, escribe=1, coloniza=1); rw_ = run(m, 734961, T=3000, mundo=PL.MUNDO_LIBRE)
    fisn = lambda R_: [{k: v for k, v in d.items() if k in J.FISICAS and k != '_carrera'} for d in R_['linajes']]
    chk("d1d ... y publicando (PS_ESCRIBE 1, como en el bloque): la FISICA de cada linaje == O1 (solo cambian las escrituras)",
        fisn(rw_) == fisn(run(o1, 734961, T=3000, mundo=PL.MUNDO_LIBRE)) and rw_['pista']['pizarra_n'] > 0)
    fija(m, [Z], 0.03, 734962, lee=0, escribe=0); rnL = run(m, 734962, mundo=PL.MUNDO_LIBRE)
    chk("d5 con sigma 0.03 hay partos anotados con genes dentro del clip",
        sum(len(m._TEL[i].get('partos', [])) for i in m._TEL) > 0
        and all(CB.CLIP[j][0] <= g[j] <= CB.CLIP[j][1] for i in m._TEL for _, g in m._TEL[i].get('partos', []) for j in range(len(CB.GENES))))
    # auditoria H-8: herencia DIRECTA del gen al hijo con sigma > 0 (una instancia, sin pista)
    import numpy as np
    fija(m, [Z], 0.03, 734969)
    Z = Z_lista(Z)
    c = m.crea(dict(L=360, rep_umbral=1.0, rng=np.random.default_rng(0), id='X', indice=0)); padre = list(c._gen)
    mem = c.al_parir(dict(t=5, k=1)); hijo = list(mem['_gen'])
    sig = [0.03 * e for e in CB.ESCALA]
    chk(f"d6 herencia: hijo = padre + N(0, sigma_j): distinto, cada gen a <= 5 sigma_j del padre y en el clip; el parto anota al PADRE",
        hijo != padre and all(abs(h - q) <= 5 * sj + 1e-12 and CB.CLIP[j][0] <= h <= CB.CLIP[j][1] for j, (h, q, sj) in enumerate(zip(hijo, padre, sig)))
        and m._TEL[0]['partos'][-1] == [5, padre])
    c.nace(dict(t=6, k=1, fundador=False, memoria=mem, rng_hijo=np.random.default_rng(1)))
    chk("d7 nace: el cuerpo nuevo lleva EXACTAMENTE los genes del hijo y los LEE (PS_LEE 1)",
        c._gen == hijo and c.MEM == hijo[CB.GENES.index('MEM')] and c.MARGEN == hijo[0] and '_gen' not in c.n)
    # junta o1_evo: COLONIZACION directa (una instancia por linaje, sin pista)
    fija(m, [dict(CO.FABRICA)], 0.03, 734969, coloniza=1)
    ctx = lambda j: dict(L=360, rep_umbral=1.0, rng=np.random.default_rng(j), id=f'X{j}', indice=j)
    a0 = m.crea(ctx(0)); a0._gen = list(Z); a0.al_parir(dict(t=7, k=1))          # el linaje 0 pare con genes Z
    b0 = m.crea(ctx(0)); o0 = m._TEL[0]['fund'][-1][0]                             # refundar el MISMO linaje: no se coloniza de si mismo
    b1 = m.crea(ctx(1)); o1f = m._TEL[1]['fund'][-1]                               # otro linaje: coloniza desde el parto de 0
    chk(f"d8 colonizacion: refundador de OTRO linaje toma los genes del padre que pario (+ sigma), origen 2; el mismo linaje no (origen {o0})",
        o0 == 1 and o1f[0] == 2 and all(abs(g - z) <= 5 * 0.03 * e + 1e-12 for g, z, e in zip(o1f[1], Z_lista(Z), CB.ESCALA)))
    fija(m, [dict(CO.FABRICA)], 0.03, 734969, coloniza=0); q = m.crea(ctx(0)); q._gen = list(Z); q.al_parir(dict(t=8, k=2)); cc = m.crea(ctx(1))
    chk("d9 sin PS_COLONIZA, aunque haya partos de otro linaje, el refundador sale de la siembra (origen 1)", len(m._COL) == 1 and m._TEL[1]['fund'][-1][0] == 1)
    # ---------------- (e) poderes
    print("(e) cada poder solo actua (pista_libre, sigma 0)")
    fija(m, [dict(CO.FABRICA)], 0.0, 734963, escribe=1); ref = run(m, 734963, T=3000, mundo=PL.MUNDO_LIBRE)
    for k, u in (('MEM', 'mem'), ('SOC', 'soc'), ('RES', 'res'), ('PAU', 'pau')):
        W = dict(CO.FABRICA); W[k] = 0.6
        fija(m, [W], 0.0, 734963, escribe=1); r = run(m, 734963, T=3000, mundo=PL.MUNDO_LIBRE)
        us = {z: sum(m._TEL[i]['activaciones'][z] for i in m._TEL) for z in ('mem', 'pau', 'soc', 'res')}
        chk(f"e1 {k} 0.6 solo: salida != sin poderes; activaciones {u} > 0; otros 0 ({us})", r != ref and us[u] > 0 and all(us[z] == 0 for z in us if z != u))
    fija(m, [dict(CO.FABRICA)], 0.0, 734964, escribe=1); rw = run(m, 734964)
    ro = run(o1, 734964)
    fis = lambda R: [{k: v for k, v in d.items() if k in J.FISICAS and k != '_carrera'} for d in R['linajes']]
    chk("e2 PUBLICAR sin poderes: la FISICA de cada linaje == O1; la pizarra tiene entradas (O1 no escribe)",
        fis(rw) == fis(ro) and rw['pista']['pizarra_n'] > 0 and ro['pista']['pizarra_n'] == 0)
    # ---------------- (f) perillas del mundo
    print("(f) cada perilla del mundo actua")
    rv = run(o1, 734965, T=3000)
    for kk, cont in (('estacion', 'a_buena'), ('parche', 'mudadas'), ('quieto', 'quietos')):
        mw = dict(PL.MUNDO_VIEJO); mw[kk] = 1
        r = run(o1, 734965, T=3000, mundo=mw); c = r['pista']['libre'][cont]; c = sum(c) if isinstance(c, list) else c
        chk(f"f1 {kk} sola: salida != mundo viejo y {cont} > 0 ({c})", r != rv and c > 0)
    r = run(o1, 734966, T=16000, mundo=dict(PL.MUNDO_VIEJO, estacion=1))['pista']['libre']
    chk(f"f2 estacion a T 16k convierte en los dos sentidos (a_buena {r['a_buena']}, a_mala {r['a_mala']}; escasez {r['frac_escasez']})",
        r['a_buena'] > 0 and r['a_mala'] > 0 and 0.3 < r['frac_escasez'] < 0.5)
    # ---------------- (g) regla 14
    print("(g) regla 14: la bateria copiada campo a campo contra corre_v143.tarea")
    ref = N(CV.tarea((734967, 'O1', T_ID)))
    tl, _ = CO.tarea_lista(734967, [('O1', o1)] * 9, T_ID, PL.MUNDO_VIEJO); tl = N(tl)
    campos = sorted(set(ref) | set(tl))
    dif = [k for k in campos if k != 'seg' and ref.get(k) != tl.get(k)]
    chk(f"g1 tarea_lista(9 x O1, mundo viejo) == corre_v143.tarea en {len(campos) - 1} campos (salvo seg); difieren {dif}", not dif)
    to = N(CO.tarea(734967, 'o1', T_ID, mundo=PL.MUNDO_VIEJO))
    dif = [k for k in sorted(set(ref) | set(to)) if k not in ('seg', 'tel', 'libre', 'estado') and ref.get(k) != to.get(k)]
    chk(f"g2 tarea('o1', mundo viejo) == corre_v143.tarea (salvo seg/tel/libre/estado); difieren {dif}", not dif)
    for i in (0, 1):
        x = CO.tarea(734968, f'mix:{i}', 1500, siembra=[dict(CO.FABRICA)], lee=1)
        ids = [l['id'] for l in x['linajes']]; cas = CO.casillas(i)
        chk(f"g3 mix indice {i}: O1_LIB en {list(cas)} y O1 en las demas ({ids})",
            all(ids[j].startswith('O1_LIB') == (j in cas) for j in range(9)))
    f = CO.fila(x, 1500, 'mix:1', 1)
    chk(f"g4 fila(mix): fundadores O1_LIB de siembra {f['fund_de_siembra']} + colonia {f['fund_colonia']} = {f['fund_n']}, ninguno de fabrica; conquista = media nac lib - media nac o1",
        f['fund_n'] > 0 and f['fund_fabrica'] == 0 and f['fund_de_siembra'] > 0 and f['fund_de_siembra'] + f['fund_colonia'] == f['fund_n']
        and abs(f['grupo']['conquista'] - (sum(f['grupo']['lib']['nac']) / 4 - sum(f['grupo']['o1']['nac']) / 5)) < 1e-9)
    # ---------------- (h) siembra
    print("(h) siembra por partos")
    G = lambda v: [v] * len(CB.GENES)
    tel = {'0': {'partos': [[100, G(0.1)], [6000, G(0.2)]], 'vivos': [[9000, G(0.9)]]}, '1': {'partos': [[5000 + j, G(0.3)] for j in range(30)]},
           '2': {'partos': [[7000 + j, G(0.4)] for j in range(10)]}}
    s, info = CO.siembra(tel, 10000, 1, n=41)
    vals = sorted(round(e['MARGEN'], 2) for e in s)
    chk(f"h1 excluye t < T/2 y a los vivos; toma los 41 partos tardios ({info})",
        (info['partos'], info['tarde'], info['usados']) == (42, 41, 41) and 0.1 not in vals and 0.9 not in vals
        and info['por_linaje'] == {'0': 1, '1': 30, '2': 10} and info['linajes'] == 3)
    s, _ = CO.siembra(tel, 10000, 1, n=20); v = [round(e['MARGEN'], 2) for e in s]
    chk(f"h2 pesa por partos: el linaje con 30 partos aporta mas que el de 10 ({v.count(0.3)} vs {v.count(0.4)})", v.count(0.3) > v.count(0.4))
    chk("h3 sin partos -> None", CO.siembra({'0': {'vivos': [[9000, G(0.9)]]}}, 10000, 1)[0] is None)
    s4, i4 = CO.siembra({'0': {'partos': [[100, G(0.1)], [200, G(0.2)]]}}, 10000, 1)
    chk(f"h4 sin partos tardios la siembra cae a TODOS los partos del pasaje ({i4['tarde']} tardios, {i4['usados']} usados)", i4['tarde'] == 0 and i4['usados'] == 2)
    tmpx = tempfile.mkdtemp(prefix='o1libre_ext_')
    try:
        bx = (734986, 734987)
        xc = CO.trabajo(('cadena', 0, 'neu', bx, 2, 300, 300, tmpx, False))
        chk(f"h5 cadena sin partos en un pasaje entero (T 300): NO aborta; extinto {xc.get('extinto')} en el pasaje {xc.get('p_extincion')}; 1 pasaje corrido",
            xc['aborto'] is None and xc['extinto'] is True and xc['p_extincion'] == 0 and len(xc['pasajes']) == 1)
        xn = CO.trabajo(('prueba', 0, 'mixn', bx, 2, 300, 300, tmpx, False)); xu = CO.trabajo(('prueba', 0, 'neu', bx, 2, 300, 300, tmpx, False))
        chk("h6 sus pruebas (mixn, neu) no se corren: JSON de DATO 'extinto', sin aborto; la mixn cuenta como perdida del neutro",
            xn['aborto'] is None and xn['extinto'] and xu['extinto'] and xn['cadena_extinta'] == 'neu' and os.path.exists(os.path.join(tmpx, 'prueba_i00_mixn.json')))
    finally:
        shutil.rmtree(tmpx, ignore_errors=True)
    # ---------------- (i) letra
    print("(i) LA LETRA en casos sinteticos (n = 10)")
    for nombre, kw, esperado, matiz, umb in CASOS:
        C, R = sintetico(**kw); L = CO.lee_serie(C, R, 10, 0)
        chk(f"i {nombre}: {L['veredicto']} ({L['matiz']}; umbral {L['en_umbral']}) == {esperado} ({matiz}; umbral {umb})",
            L['veredicto'] == esperado and L['matiz'] == matiz and (umb is None or L['en_umbral'] == umb))
    # ---------------- (j) guardas
    print("(j) guardas")
    for args in (['--humo', '--pool', '2'], ['--serie', '--pool', '3'], ['--seri'], ['--humo', '--x']):
        try: CO.main(args); r = 'corre'
        except SystemExit: r = 'aborta'
        chk(f"j1 {args} aborta", r == 'aborta')
    S = [CO.sem_pas(CO.BASES[b], i, p) for b in CO.BASES for i in range(CO.N_IND) for p in range(CO.NPAS)] + [CO.sem_pru(CO.BASES[b], i) for b in CO.BASES for i in range(CO.N_IND)]
    H = [CO.sem_pas(CO.HUMO['base'], 0, p) for p in range(CO.HUMO['npas'])] + [CO.HUMO['base'][1]]
    chk(f"j2 semillas serie/replica/humo disjuntas y en 734xxx ({len(S)} + {len(H)})",
        len(set(S)) == len(S) and not set(S) & set(H) and all(734000 <= x < 735000 for x in S + H) and not set(S) & set(range(734950, 734990)))
    p1 = 2 * CO.HUMO['npas'] * CO.HUMO['T_pas'] + 2 * CO.HUMO['T_pru']; p2 = 4 * CO.HUMO['T_pru']
    chk(f"j3 el humo cabe: proceso 1 {2 * CO.HUMO['npas'] + 2} corridas {p1} pasos; proceso 2 4 corridas {p2} pasos (<= 6 y <= 200 000)",
        2 * CO.HUMO['npas'] + 2 <= 6 and p1 <= 200000 and p2 <= 200000)
    # ---------------- (k) ruta Pool con un Pool FALSO (un proceso), candado y regla de parada
    print("(k) ruta --serie --pool 2 con Pool FALSO de un proceso (T 3000/1500, 1 indice, 1 pasaje, semillas de practica), candado y parada")
    import multiprocessing
    class _R:
        def __init__(self, v): self.v = v
        def ready(self): return True
        def get(self): return self.v
    class _Falso:
        def __init__(self, n): self.n = n; self.llamadas = 0
        def __enter__(self): return self
        def __exit__(self, *a): return False
        def apply_async(self, f, args): self.llamadas += 1; return _R(f(*args))
    guard = dict(Pool=multiprocessing.Pool, git=CO.git_limpio, N=CO.N_IND, NP=CO.NPAS, TP=CO.T_PAS, TR=CO.T_PRU, B=dict(CO.BASES), D=CO.DATOS)
    tmp = tempfile.mkdtemp(prefix='o1libre_pool_')
    try:
        multiprocessing.Pool = _Falso; CO.git_limpio = lambda r, log: True
        CO.N_IND = 1; CO.NPAS = 1; CO.T_PAS = 3000; CO.T_PRU = 1500; CO.BASES.update(serie=(734970, 734975), replica=(734980, 734985)); CO.DATOS = tmp
        rc = CO.main(['--serie', '--pool', '2'])
        car = glob_uno(os.path.join(tmp, 'serie_*'))
        js = sorted(os.path.basename(x) for x in os.listdir(car) if x.endswith('.json'))
        esperado = ['cadena_i00_lib.json', 'cadena_i00_neu.json', 'pasaje_i00_lib_p00.json', 'pasaje_i00_neu_p00.json'] + \
                   [f'prueba_i00_{b}.json' for b in sorted(CO.TODAS)] + ['resumen.json']
        rs = json.load(open(os.path.join(car, 'resumen.json'), encoding='utf-8'))
        chk(f"k1 --serie --pool 2 (Pool falso): rc 0, 2 cadenas y 6 pruebas encoladas tras su cadena, 0 abortos, resumen ({rs['veredicto']})",
            rc == 0 and js == sorted(esperado) and rs['abortos'] == [] and rs['letra']['validez']['V1_completa'])
        xa = json.load(open(os.path.join(car, 'prueba_i00_mixA.json'), encoding='utf-8'))
        xm = json.load(open(os.path.join(car, 'prueba_i00_mix.json'), encoding='utf-8'))
        chk("k1b mixA (descriptivo): la siembra usada es la de lib con los 4 poderes en 0 y el resto igual",
            all(xa['genes_siembra_usada'][k] == 0.0 for k in CB.PODERES)
            and all(xa['genes_siembra_usada'][k] == xm['genes_siembra_usada'][k] for k in CB.GENES_O1))
        chk("k2 candado: una segunda --serie sobre una carpeta existente (sin --reanuda) se niega (rc 1)", CO.main(['--serie', '--pool', '2']) == 1)
        vs = rs['letra']['veredicto']; um = rs['letra']['en_umbral']
        rr = CO.main(['--replica', '--pool', '2'])
        permite = vs in ('FUNCIONA', 'HAY ALGO MODESTO') or (vs == 'NO' and um)
        chk(f"k3 regla de parada: serie {vs} (umbral {um}) -> replica {'corre' if permite else 'se niega'} (rc {rr})", (rr == 0) == permite)
        # auditoria H-6: k4 ejerce la rama que PERMITE la replica y el candado de sha_runner (resumen de serie FALSO, mas nuevo)
        falsa = os.path.join(tmp, f"serie_i{CO.BASES['serie'][1]}-{CO.BASES['serie'][1]}_zz_falsa"); os.makedirs(falsa)
        def pon(sha): json.dump(dict(modo='serie', humo=False, sha_runner=sha, letra=dict(veredicto='HAY ALGO MODESTO', en_umbral=False)),
                                open(os.path.join(falsa, 'resumen.json'), 'w', encoding='utf-8'))
        rep = lambda: sorted(x for x in os.listdir(tmp) if x.startswith('replica_'))
        pon('0000000000000000'); r1 = CO.main(['--replica', '--pool', '2']); n1 = rep()
        pon(CO.h16(os.path.abspath(CO.__file__))); r2 = CO.main(['--replica', '--pool', '2']); n2 = rep()
        ok2 = bool(n2) and os.path.exists(os.path.join(tmp, n2[-1], 'resumen.json'))
        chk(f"k4 serie MODESTO con sha_runner ajeno -> la replica se niega sin crear carpeta (rc {r1}, {n1}); con el sha del runner -> corre (rc {r2}, resumen {ok2})",
            r1 == 1 and not n1 and r2 == 0 and ok2)
    finally:
        multiprocessing.Pool = guard['Pool']; CO.git_limpio = guard['git']; CO.N_IND = guard['N']; CO.NPAS = guard['NP']; CO.T_PAS = guard['TP']
        CO.T_PRU = guard['TR']; CO.BASES.clear(); CO.BASES.update(guard['B']); CO.DATOS = guard['D']
        shutil.rmtree(tmp, ignore_errors=True)
    print(f"\nARNES {'PASA' if OK[0] else 'NO PASA'}: {NCHK[1]}/{NCHK[0]} · {time.time() - t0:.1f}s")
    return 0 if OK[0] else 1


def Z_lista(Z):
    return [float(Z[k]) for k in CB.GENES] if isinstance(Z, dict) else list(Z)


def glob_uno(patron):
    import glob
    g = sorted(glob.glob(patron))
    if len(g) != 1: raise SystemExit(f"glob {patron}: {g}")
    return g[0]


# ------------------------------------------------------------------ casos sinteticos de la letra
def sintetico(conq=1.0, conqn=-1.0, pod_lib=0.5, pod_neu=0.3, gana_pod=10, gana_c=10, gana_n=10, o1_R0=0.8, neu_usa=0, fund_ok=True,
              lista_c=None, lista_n=None, neu_ext=(), r0_lib=(0.9, 0.9, 0.9)):
    """10 indices. conquista de mix > 0 en gana_c indices; mix > mixn en gana_n; poder MEM lib > neu en gana_pod cadenas."""
    I = range(10); MW = dict(CO.MUNDO)
    lib_ = dict(a_mala=5, a_buena=5, mudadas=5, sin_libre=0, nacidos=9, frac_escasez=0.4, quietos=[1] * 9, frac_en_parche=[0.1] * 9)
    def est(carro, lee, esc_=1): return dict(carro=carro, sigma=CO.SIGMA, lee=lee, escribe=esc_, coloniza=1, mundo=MW)
    def prueba(b, i):
        g = None
        if b in CO.MIXTAS:
            c = (conq if i < gana_c else -abs(conq)) if b == 'mix' else (conqn if i < gana_n else conq + 1.0)
            if b == 'mix' and lista_c: c = lista_c[i]
            if b == 'mixn' and lista_n: c = lista_n[i]
            g = dict(conquista=c, dif_partos=0.0, dif_muertes=0.0, dif_fund=0.0, lib=dict(cruza=[1] * 4), o1=dict(cruza=[1] * 5))
        return dict(coherente=True, t_fund_ok=True, R0_med=(o1_R0 if b == 'o1' else 0.9), libre=lib_,
                    fund_n=(0 if b == 'o1' else 3), fund_de_siembra=(0 if b == 'o1' else 2), fund_colonia=(0 if b == 'o1' else (1 if fund_ok else 0)),
                    fund_fabrica=(0 if (b == 'o1' or fund_ok) else 1),
                    estado=(est('O1', None) if b == 'o1' else est('O1_LIB', 1)), grupo=g, cruzan=7, nac_reales=[10] * 9,
                    activaciones=dict(mem=1, pau=1, soc=1, res=1, escr=1), mundo_AC=1.0)
    R = {b: {i: prueba(b, i) for i in I} for b in CO.PRUEBAS}
    for i in neu_ext:
        for b in ('neu', 'mixn'): R[b][i] = CO.extinta('prueba', i, b, 'neu', 1)
    def gs(b, i, q):
        d = dict(CO.FABRICA)
        if b == 'lib': d['MEM'] = pod_lib if i < gana_pod else pod_neu - 0.1
        else: d['MEM'] = pod_neu
        return d
    C = {b: {i: dict(pasajes=[dict(genes_siembra=gs(b, i, q), libre=lib_, estado=est('O1_LIB', CO.CADENAS[b]), cruzan=5, partos_tel=40,
                                   R0_med=(r0_lib[q] if b == 'lib' else 0.9),
                                   activaciones=(dict(mem=neu_usa, pau=0, soc=0, res=0, escr=1) if b == 'neu' else dict(mem=3, pau=3, soc=3, res=3, escr=3)))
                              for q in range(CO.NPAS)]) for i in I} for b in CO.CADENAS}
    for i in neu_ext:
        C['neu'][i] = dict(pasajes=C['neu'][i]['pasajes'][:2], siembra_final=None, extinto=True, p_extincion=1)
        C['neu'][i]['pasajes'][-1] = dict(C['neu'][i]['pasajes'][-1], genes_siembra=None)
    return C, R


CASOS = [
    ('FUNCIONA', dict(), 'FUNCIONA', None, False),
    ('MODESTO conquista = deriva (PN no)', dict(gana_n=3), 'HAY ALGO MODESTO', 'conquista, pero la deriva sola hace lo mismo', False),
    ('MODESTO conquista sin poderes', dict(pod_lib=0.3, pod_neu=0.3), 'HAY ALGO MODESTO', 'conquista por seleccion sin poderes (afina las perillas de O1)', None),
    ('MODESTO poder sin conquista', dict(gana_c=2, gana_n=2), 'HAY ALGO MODESTO', 'un poder se prende sin conquista', False),
    ('NO (nada)', dict(gana_c=2, gana_n=2, pod_lib=0.3, pod_neu=0.3), 'NO', None, None),
    ('NO: poder gana 10/10 pero dif 0.04 < 0.05', dict(gana_c=2, gana_n=2, pod_lib=0.34, pod_neu=0.30), 'NO', None, True),
    ('NO EN EL UMBRAL: conquista 7/10', dict(gana_c=7, gana_n=2, pod_lib=0.3, pod_neu=0.3), 'NO', None, True),
    ('FUNCIONA EN EL UMBRAL: PC 8/10', dict(gana_c=8), 'FUNCIONA', None, True),
    # ERR-160 (auditoria H-2): PN cuenta para EN EL UMBRAL solo si PC >= 7
    ('ERR-160: PN 8/10 con PC 2/10 -> NO fuera del umbral', dict(pod_lib=0.3, pod_neu=0.3, lista_c=[1, 1] + [-1] * 8, lista_n=[-2] * 8 + [5, 5]), 'NO', None, False),
    ('ERR-160: PN 8/10 con PC 7/10 -> NO en el umbral', dict(pod_lib=0.3, pod_neu=0.3, lista_c=[1] * 7 + [-1] * 3, lista_n=[-2] * 8 + [5, 5]), 'NO', None, True),
    # ERR-160 (v): el neutro extinto en 2 indices es DATO: se lee; mixn = perdida del neutro; PP solo con las dos cadenas vivas
    ('ERR-160 v: neutro extinto en 2 indices -> se lee (FUNCIONA)', dict(neu_ext=(0, 1)), 'FUNCIONA', None, None),
    ('ERR-160 v: neutro extinto en 3 indices -> PP 7/7 no llega a 8 -> MODESTO', dict(neu_ext=(0, 1, 2)), 'HAY ALGO MODESTO', 'conquista por seleccion sin poderes (afina las perillas de O1)', None),
    # R-5b: R0 de lib cae >= 0.15 del primer al ultimo pasaje y la serie da NO: matiz de carga, el veredicto no cambia
    ('R-5b: NO con carga (R0 lib 0.90 -> 0.75)', dict(gana_c=2, gana_n=2, pod_lib=0.3, pod_neu=0.3, r0_lib=(0.9, 0.8, 0.75)), 'NO', 'carga domina; NO no informa sobre poderes', None),
    ('R-5b: NO sin carga (0.90 -> 0.76)', dict(gana_c=2, gana_n=2, pod_lib=0.3, pod_neu=0.3, r0_lib=(0.9, 0.8, 0.76)), 'NO', None, None),
    ('NO SE LEE: el neutro activo un poder (V6)', dict(neu_usa=1), 'NO SE LEE', None, None),
    ('NO SE LEE: O1 no vive (V2, R0 0.49)', dict(o1_R0=0.49), 'NO SE LEE', None, None),
    ('NO SE LEE: un fundador salio de FABRICA (V4)', dict(fund_ok=False), 'NO SE LEE', None, None),
]


if __name__ == '__main__':
    sys.exit(main())
