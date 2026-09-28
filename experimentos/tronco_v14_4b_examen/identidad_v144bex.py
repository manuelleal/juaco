"""identidad_v144bex.py = identidad_v144ex.py (6a714b193b6222dc) para v14.4b = v14.3 + TERMOP. Cambia el bloque de la MEMORIA (media movil: en un mundo quieto e == dS exacto; tras invertir, A negativa y B positiva) y la letra se compara tambien con los carros V143_TERMOP / V143_TERMOPINV. GENERADO por construye_examen_v144b.py. NO editar a mano."""
"""identidad_v144bex.py -- ARNES DE IDENTIDAD del examen v4 de v14.4b = v14.3 + TERMOP (UN proceso, sin Pool; se corre ANTES de
mirar numeros). Ultima linea: 'RESULTADO: N/N'. Escribe su JSON en datos/humo/ (ERR-42). Salida en identidad_v144bex_salida.txt.

(0) CONSTRUCCION: los siete archivos en disco == construye_termop.construye() (por anclas; la letra del carro V143_TERMO esta
    literal en el origen) y todas las anclas reusadas con su sha.
(A) PIEZA APAGADA == v14.3 BIT A BIT, TODAS las claves: organismo_v144b(termo=0) == organismo/organismo_v143 (CONGELADO) en 12
    escenarios (T = 20 000, semilla 47045); organismo_v144bg(termo=0) == organismo_v143g (px0, xor01, azar; kwargs del tronco);
    organismo_v144bcal(termo=0) == organismo_v143cal en los cinco montajes del examen (T-A VIVO, T-A CUELLO_MIN, T-C ii, T-D
    ALIAS 326 y LIMPIA 307) y con vivo=0.
(A') EL TRONCO DEL MUNDO VIVO: organismo_v143cal (v14.3) == organismo_v3cal (el OFF calibrado de V4-CAL) en los cinco montajes:
    el OFF del examen ES v14.3.
(P) LA PIEZA ACTUA: termo=1 != termo=0 (con a_no + a_si > 0) en el examen AB y AB invertido, en el mundo de regla (lee: dec > 0)
    y en los cinco... cuatro montajes del mundo vivo; TERMOINV (termo=2) != TERMO; las guardas (termo=2 con una necesidad, termo=3)
    abortan. Determinismo: dos corridas iguales dan lo mismo.
(L) LA LETRA == V143_TERMO / V143_TERMOINV de la carrera: termo_letra contra Carro._tm_boca de los DOS carros (construidos sin
    __init__, solo con _adS, _tmU y _tm) en una rejilla de casos sinteticos (memorias con medias positivas, negativas, mixtas,
    nulas, desconocidas; niveles en y alrededor de U + s/2; U 1.0 y 0.5; mf si/no): misma decision y mismos contadores. Con UNA
    necesidad, termo_letra([s0, n], (E,)) == el carro con [s0, 0.0, n] y cualquier Ag. La memoria del organismo (_adS en la
    telemetria) == la suma secuencial del dS nominal, como APR._apr_dS, con mordidas == mord.
(X) CADENA una necesidad / dos necesidades: organismo_v144bcal(vivo=0, n_nec=1, termo=1) == organismo_v144b(termo=1) (claves de
    v14.2 y contadores de la pieza).
(D) EL RUNNER: sus tareas corren el organismo y los kwargs declarados (CAND/CTRL/rev/sal == llamada directa); bateria_v144b con
    termo=0 == bateria_v143 (CONGELADA) en E2 (T = 100 000) y con la pieza, DIFIERE; bateria_generaliza_v144b con termo=0 ==
    bateria_generaliza_v143 (CONGELADA) en px0 (T = 200 000).
(R) REGLA 14 del runner (sin simular).
(J) EL JUEZ reproduce el examen de v14.3 (crudos y veredictos registrados de serie y replica, sin simular): T-B, T-C (i), T-E,
    T-F examen, T-D, T-A, T-C (ii), T-F vivo, TRONCO_B y PLACEBO.
(K) CONTROLES QUE DEBEN FALLAR O DIFERIR: TRONCO_B != OFF; PLACEBO != OFF; el juez dice SI al sintetico bueno y NO al malo; T-G
    cae si CAND == OFF (G-1), si el control gana (G-2), si la pieza no actua (G-3) o si falta una corrida; una letra mutada
    (U + s/3) difiere del carro; el PARSER rechaza banderas desconocidas, abreviadas, serie sin --pool, --pool > 6, --reserva
    sin --sustituye y --solo TG. Solo se llama al parser, en este proceso; nunca a main(): este arnes no lanza ninguna serie.

    python experimentos/tronco_v14_4b_examen/identidad_v144bex.py
"""
import contextlib, io, json, os, sys, time

try:
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
except Exception:
    pass
AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
import corre_examen_v144b as R   # pone sys.path (organismo/, mundo vivo, criterio_v3/v4, creacion_B, dE5; al final v14.3 y carros)
import numpy as np

RAIZ = R.RAIZ
T = 20000
S = 49905            # semilla de IDENTIDAD (umbrales_examen_v144b.SEMILLAS['identidad']): no es de ninguna serie
OK = [0]; NO = [0]; DET = []; t0 = time.time()


def N(x):
    return json.dumps(x, sort_keys=True, default=str)


def anota(bloque, nombre, bien, det=''):
    (OK if bien else NO)[0] += 1
    DET.append(dict(bloque=bloque, nombre=nombre, ok=bool(bien), det=det))
    print(f"  [{time.time() - t0:5.0f}s] ({bloque}) {'OK ' if bien else '***'} {nombre}" + ('' if bien or not det else f'  -> {det}'), flush=True)


def dif(a, b, claves=None, fuera=()):
    ks = claves if claves is not None else sorted((set(a) | set(b)) - set(fuera))
    return [k for k in ks if N(a.get(k, '<falta>')) != N(b.get(k, '<falta>'))]


def igual(bloque, nombre, a, b, claves=None, fuera=()):
    d = dif(a, b, claves, fuera)
    anota(bloque, nombre, not d, f'difieren {d[:6]}')


def distinto(bloque, nombre, a, b, claves):
    d = dif(a, b, claves)
    anota(bloque, nombre + ' (DEBE diferir)', bool(d), 'SALIO IDENTICO')


def callado(f, *a, **k):
    with contextlib.redirect_stdout(io.StringIO()):
        return f(*a, **k)


def aborta(f, *a, **k):
    try:
        f(*a, **k)
        return False
    except SystemExit:
        return True


def actua(r):
    t = r.get('termo')
    return bool(t and t['a_no'] + t['a_si'] > 0)


if __name__ == '__main__':
    extra = sys.argv[1:]
    if extra:
        raise SystemExit(f'*** banderas desconocidas {extra}: este arnes no toma argumentos (ERR-115)')
    import organismo_v143 as V143, organismo_v144b as V144, organismo_v143g as V143G, organismo_v144bg as V144G
    import organismo_v3cal as CAL, organismo_v143cal as V143C, organismo_v144bcal as V144C, construye_termop as CO
    import V143_TERMO as CT, V143_TERMOINV as CTI, importlib.util
    def _carga(n):
        s_ = importlib.util.spec_from_file_location(n, os.path.join(AQUI, 'carros', n + '.py')); m_ = importlib.util.module_from_spec(s_); s_.loader.exec_module(m_); return m_
    CTP, CTPI = _carga('V143_TERMOP'), _carga('V143_TERMOPINV')
    print(f'ARNES identidad_v144bex — T={T}, semilla {S}; python {sys.version.split()[0]}, numpy {np.__version__}')
    for nom, p in [('organismo_v143 (CONGELADO)', V143.__file__), ('organismo_v144b', V144.__file__), ('organismo_v143g (CONGELADO)', V143G.__file__),
                   ('organismo_v144bg', V144G.__file__), ('organismo_v3cal', CAL.__file__), ('organismo_v143cal', V143C.__file__),
                   ('organismo_v144bcal', V144C.__file__), ('carro V143_TERMO', CT.__file__), ('carro V143_TERMOINV', CTI.__file__),
                   ('corre_examen_v144b', R.__file__), ('este arnes', os.path.abspath(__file__))]:
        print(f'  sha {nom:28s} {R.h16(p)}  {os.path.relpath(p, RAIZ)}')

    print('--- (0) construccion por anclas y anclas reusadas')
    C = CO.construye()
    for n_, txt in C.items():
        p = os.path.join(AQUI, n_)
        anota('0', f'{n_} en disco == construccion por anclas', os.path.exists(p) and open(p, 'rb').read().decode('utf-8') == txt)
    malas = [(os.path.relpath(p, RAIZ), R.h16(p), s) for p, s in R.ANCLAS.items() if R.h16(p) != s]
    anota('0', f'las {len(R.ANCLAS)} anclas reusadas tienen su sha (incluidos los dos carros de la carrera y el examen de v14.3)', not malas, str(malas))

    ESC = [('AB por defecto', dict()), ('AB invertido', dict(invertir_en=15000)),
           ('AB + patron nuevo C', dict(nuevo='C', nuevo_en=15000)), ('AB solap_AB=3 (E2L)', dict(solap_AB=3)),
           ('AB sin plasticidad', dict(plast=False)), ('AB via lenta apagada', dict(eta_s=0.0)),
           ('AB sin puerta', dict(puerta=None)), ('AB sin division por signo', dict(div_signo=False)),
           ('AB sin hija dispersa', dict(mask_rel=0)), ('AB sin puerta por codigo', dict(puerta_pat=0)),
           ('AB N apagada (norm_lenta=0)', dict(norm_lenta=0)),
           ('AB D comida solap_B=2 (E2K)', dict(nuevo='D', nuevo_val='comida', solap_B=2, nuevo_en=15000))]
    print(f'--- (A) organismo_v144b(termo=0) == organismo_v143 (CONGELADO), T={T}')
    P1 = {}
    for etq, kw in ESC:
        ref = V143.run(S, T=T, **kw)
        igual('A', f'{etq}: TERMO apagado == v14.3 (todas las claves)', V144.run(S, T=T, termo=0, **kw), ref)
        if etq in ('AB por defecto', 'AB invertido'):
            P1[etq] = (V144.run(S, T=T, **kw), ref)

    print(f'--- (A) mundo de regla: organismo_v144bg(termo=0) == organismo_v143g (CONGELADO), T={T}')
    KWG = R.G143.INSTRUMENTOS['organismo_v143'][1]
    PG = {}
    for regla in ('px0', 'xor01', 'azar'):
        ref = V143G.run(S, T=T, mundo='regla', regla=regla, **KWG)
        igual('A', f'regla/{regla}: TERMO apagado == v143g', V144G.run(S, T=T, mundo='regla', regla=regla, termo=0, **KWG), ref)
        if regla == 'px0':
            PG[regla] = (V144G.run(S, T=T, mundo='regla', regla=regla, **KWG), ref)

    print(f"--- (A) mundo vivo: organismo_v144bcal(termo=0) == organismo_v143cal y (A') organismo_v143cal == organismo_v3cal, T={T}")
    MONT = [('T-A VIVO', S, R.C4.kw_vivo('VIVO', 'OFF')), ('T-A CUELLO_MIN', S, R.C4.kw_vivo('CUELLO_MIN', 'OFF')),
            ('T-C (ii) reversion en T/2', S, R.C4.kw_rev('OFF', T)),
            ('T-D ALIAS 326 (sal muda)', 326, R.kw_sal('OFF')), ('T-D LIMPIA 307 (sal muda)', 307, R.kw_sal('OFF'))]
    PV = {}
    for etq, s, kw in MONT:
        r143 = V143C.run(s, T=T, **dict(kw, norm_lenta=1))
        igual('A', f'{etq}: TERMO apagado == v143cal (todas las claves)', V144C.run(s, T=T, **dict(kw, norm_lenta=1, termo=0)), r143)
        igual("A'", f'{etq}: v143cal (v14.3) == v3cal (el OFF calibrado): el tronco del mundo vivo ES v14.3', r143, CAL.run(s, T=T, **kw))
        PV[etq] = (V144C.run(s, T=T, **dict(kw, norm_lenta=1, termo=1)), r143, kw, s)
    igual('A', 'vivo=0, n_nec=1: organismo_v144bcal(termo=0) == organismo_v143cal', V144C.run(S, T=T, vivo=0, n_nec=1, placebo=0, termo=0),
          V143C.run(S, T=T, vivo=0, n_nec=1, placebo=0))

    print('--- (P) la pieza ACTUA (termo=1 != termo=0) y las guardas')
    for etq, (a1, a0) in P1.items():
        distinto('P', f'examen {etq}: TERMO encendido != v14.3 y a_no + a_si > 0 ({a1["termo"]["a_no"]} / {a1["termo"]["a_si"]})', a1, a0,
                 ['mord', 'vis', 'deaths', 'W'] if actua(a1) else [])
    a1, a0 = PG['px0']
    anota('P', f'regla/px0: la pieza LEE lo sentido y gobierna decisiones (dec {a1["termo"]["dec"]} > 0; a_no {a1["termo"]["a_no"]}, '
               f'a_si {a1["termo"]["a_si"]}: se reporta)', a1['termo']['dec'] > 0)
    for etq in ('T-A VIVO', 'T-A CUELLO_MIN', 'T-C (ii) reversion en T/2', 'T-D ALIAS 326 (sal muda)'):
        a1, a0, kw, s = PV[etq]
        distinto('P', f'{etq}: TERMO encendido != v14.3 y a_no + a_si > 0 ({a1["termo"]["a_no"]} / {a1["termo"]["a_si"]})', a1, a0,
                 ['mord', 'vis', 'deaths', 'W_nec'] if actua(a1) else [])
    a1, a0, kw, s = PV['T-A VIVO']
    a2 = V144C.run(s, T=T, **dict(kw, norm_lenta=1, termo=2))
    distinto('P', f'T-A VIVO: TERMOINV (termo=2) != TERMO y actua ({a2["termo"]["a_no"]} / {a2["termo"]["a_si"]})', a2, a1,
             ['mord', 'deaths', 'W_nec'] if actua(a2) else [])
    igual('P', 'determinismo: T-A VIVO con TERMO, dos veces, identico', V144C.run(s, T=T, **dict(kw, norm_lenta=1, termo=1)), a1)
    anota('P', 'guardas: termo=2 con UNA necesidad aborta (organismo_v144b, organismo_v144bg, organismo_v144bcal con vivo=0); termo=3 aborta',
          aborta(V144.run, S, T=10, termo=2) and aborta(V144G.run, S, T=10, termo=2) and aborta(V144C.run, S, T=10, termo=2)
          and aborta(V144.run, S, T=10, termo=3) and aborta(V144C.run, S, T=10, termo=3, **R.C4.kw_vivo('VIVO', 'OFF')))

    print('--- (L) la LETRA: termo_letra == Carro._tm_boca de V143_TERMO y V143_TERMOINV (casos sinteticos, sin simular)')

    def carro(mod, adS, U):
        c = object.__new__(mod.Carro)
        c._adS = {k: list(v) for k, v in adS.items()}; c._tmM = {k: list(v) for k, v in adS.items()}   # TERMO lee _adS; TERMO' lee _tmM
        c._tmU = float(U); c._tm = dict(dec=0, a_no=0, a_si=0, mord=0)
        return c

    def suma(seq):   # la memoria como APR._apr_dS: m[0] += float(dS[0]); m[1] += float(dS[1]); m[2] += 1
        m = [0.0, 0.0, 0]
        for x, y in seq:
            m[0] += float(x); m[1] += float(y); m[2] += 1
        return m
    MEM = {'desconocida': None, 'contada cero': [0.0, 0.0, 0], 'comida x5': suma([(0.8, 0.0)] * 5), 'agua x3': suma([(0.0, 0.8)] * 3),
           'las dos': suma([(0.8, 0.8)] * 2), 'veneno x4': suma([(-0.4, 0.0)] * 4), 'sal x2': suma([(0.0, -0.4)] * 2),
           'mixta': suma([(0.8, -0.4)] * 3), 'nula (sal muda)': suma([(0.0, 0.0)] * 6),
           'comida luego veneno (media +)': suma([(0.8, 0.0)] * 10 + [(-0.4, 0.0)] * 19),
           'comida luego veneno (media -)': suma([(0.8, 0.0)] * 10 + [(-0.4, 0.0)] * 21),
           'comida chica': suma([(0.1, 0.0)] * 7), 'agua grande': suma([(0.0, 2.3)] * 1)}
    n_cas = n_mal = 0; cambia = {1: [0, 0], 2: [0, 0]}; malos = []
    for U in (1.0, 0.5):
        niv = sorted({0.0, 0.5, 0.99, 1.0, 1.2, 1.3999999, 1.4, 1.4000001, 1.45, 1.5, U, U + 0.4, U + 0.05, U + 1.15, U + 0.4 - 1e-12})
        for kk, m in MEM.items():
            for modo, mod in ((1, CT), (2, CTI), (1, CTP), (2, CTPI)):
                for E in niv:
                    for Ag in niv:
                        for mf in (True, False):
                            c = carro(mod, {} if m is None else {'X': m}, U)
                            bc = c._tm_boca('X', E, Ag, mf)
                            bo, go = V144C.termo_letra(None if m is None else list(m), (float(E), float(Ag)), U, mf, modo)
                            n_cas += 1
                            ok = (bool(bc) == bool(bo)) and (c._tm['dec'] == int(go)) and (c._tm['mord'] == int(bo and go))
                            if not ok:
                                n_mal += 1; malos.append((kk, modo, U, E, Ag, mf, bc, bo, go))
                            if go and bool(bo) != bool(mf):
                                cambia[modo][0 if mf else 1] += 1
    anota('L', f'termo_letra == _tm_boca de V143_TERMO y V143_TERMOP (modo 1) y de V143_TERMOINV y V143_TERMOPINV (modo 2): decision y contadores en {n_cas} casos '
               f'(la pieza cambia la decision de la boca: TERMO a_no {cambia[1][0]} a_si {cambia[1][1]}; TERMOINV {cambia[2][0]} / {cambia[2][1]})',
          n_mal == 0 and min(cambia[1] + cambia[2]) > 0, str(malos[:3]))
    anota('L', 'la funcion de la letra es la MISMA en los tres organismos (organismo_v144b, v144g, v144cal)',
          all(f(m_, l_, u_, mf_, 1) == V144C.termo_letra(m_, l_, u_, mf_, 1) for f in (V144.termo_letra, V144G.termo_letra)
              for m_, l_, u_, mf_ in (([1.6, 2], (1.0,), 1.0, False), ([1.6, 2], (1.5,), 1.0, True), (None, (0.2,), 1.0, True))))
    n1 = n1m = 0
    for U in (1.0, 0.5):
        for kk, m in MEM.items():
            if m is not None and m[1] != 0.0:
                continue   # UNA necesidad: el carro con la segunda componente muda
            for E in (0.0, 0.99, 1.0, 1.3999999, 1.4, 1.45, U + 0.4, 1.5):
                for Ag in (-1.0, 0.0, 1.4, 9.0):
                    for mf in (True, False):
                        c = carro(CT, {} if m is None else {'X': m}, U)
                        bc = c._tm_boca('X', E, Ag, mf)
                        bo, go = V144.termo_letra(None if m is None else [m[0], m[2]], (float(E),), U, mf, 1)
                        n1 += 1; n1m += int(bool(bc) != bool(bo) or c._tm['dec'] != int(go))
    anota('L', f'UNA necesidad: termo_letra([s0, n], (E,)) == el carro con [s0, 0.0, n] y cualquier Ag, en {n1} casos', n1m == 0)
    a1, _, kw, s = PV['T-A VIVO']
    EF = V144C.EFECTO; VAL = V144C.VAL_VIVO
    det_m = {k: v for k, v in a1['termo']['adS'].items()}
    okm = all(v == [float(EF[VAL[k]][0]), float(EF[VAL[k]][1]), 1] and sum(a1['mord'][k]) > 0 for k, v in det_m.items())
    anota('L', f"TERMO': en el mundo vivo QUIETO (T-A VIVO) la memoria de cada estimulo mordido es EXACTAMENTE su dS nominal, con "
               f"'mordidas' = 1 (media movil de un valor constante): {det_m}", okm and len(det_m) == 4)
    a1, _, kw, s = PV['T-C (ii) reversion en T/2']
    mA, mB = a1['termo']['adS']['A'], a1['termo']['adS']['B']
    anota('L', f"TERMO' SE DESDICE: tras la reversion (T-C ii, T = {T}) la memoria de A es NEGATIVA ({mA[0]:.3f}) y la de B POSITIVA "
               f"({mB[0]:.3f})", mA[0] < 0 < mB[0] and mA[2] == mB[2] == 1)
    import inspect
    lam = inspect.signature(V144C.run).parameters['ema_c'].default
    c = object.__new__(CTP.Carro); c._tmM = {}; c._tmL = lam
    ref = None; ok_e = True
    for x in [(0.8, 0.0)] * 30 + [(-0.4, 0.0)] * 25 + [(0.0, 0.8)] * 3:
        c._tm_dS('A', x)
        ref = [x[0], x[1], 1] if ref is None else [ref[0] + lam * (x[0] - ref[0]), ref[1] + lam * (x[1] - ref[1]), 1]
        ok_e &= (c._tmM['A'] == ref)
    anota('L', f"el carro V143_TERMOP acumula con la MISMA regla (e <- dS; e <- e + ema_c (dS - e)) y ema_c del tronco == la de FABRICA "
               f"({lam}); 58 mordidas sinteticas identicas", ok_e and lam == 0.05)
    print('--- (X) cadena una necesidad / dos necesidades (la pieza encendida)')
    b = V144.run(S, T=T); a = V144C.run(S, T=T, vivo=0, n_nec=1, placebo=0, termo=1)
    igual('X', 'organismo_v144bcal(vivo=0, n_nec=1, termo=1) == organismo_v144b(termo=1) en las claves de v14.2', a, b,
          claves=sorted(set(b) - {'termo'}))
    anota('X', f"contadores de la pieza iguales (dec/a_no/a_si/mord {[b['termo'][k] for k in ('dec', 'a_no', 'a_si', 'mord')]}) y la "
               f"memoria igual en la necesidad E",
          all(a['termo'][k] == b['termo'][k] for k in ('dec', 'a_no', 'a_si', 'mord'))
          and {k: (v[0], v[2]) for k, v in a['termo']['adS'].items()} == {k: (v[0], v[1]) for k, v in b['termo']['adS'].items()})

    print('--- (D) las tareas del runner corren lo declarado')
    kwc = R.kw_vivo_cand('VIVO'); r = V144C.run(S, T=T, **kwc)
    o = R.tarea_vivo(('VIVO', S, 'CAND', T))
    igual('D', 'tarea_vivo CAND == resumen de organismo_v144bcal con kw_vivo_cand (norm_lenta=1, termo=1)', o,
          dict(R.CR2.resumen2('VIVO', S, r, kwc, T), termo=R.telemetria(r)), fuera=('seed_real', 'arm', 'placebo', 'des_splits', 'seg', 'org'))
    ok_ = R.tarea_vivo(('VIVO', S, 'CTRL', T)); oo = R.tarea_vivo(('VIVO', S, 'OFF', T))
    anota('D', f"tarea_vivo CTRL corre termo=2 ({ok_['termo']['termo']}) y difiere de CAND; CAND difiere de OFF (la pieza actua)",
          ok_['termo']['termo'] == 2 and not R.iguales(ok_, o) and not R.iguales(o, oo))
    r = V144C.run(S, T=T, **R.kw_rev_cand(T)); o = R.tarea_rev((S, 'CAND', T))
    anota('D', 'tarea_rev CAND == organismo_v144bcal con kw_rev_cand (rev, mordidas, muertes, telemetria)',
          o['rev'] == r['mord']['B'][3] - r['mord']['A'][3] and o['deaths'] == r['deaths'] and o['mordA'] == r['mord']['A']
          and N(o['termo']) == N(R.telemetria(r)))
    r = V144C.run(326, T=T, **R.kw_sal('CAND')); o = R.tarea_sal(('S1-ALIAS', 326, 'CAND', T))
    anota('D', 'tarea_sal CAND == organismo_v144bcal con kw_sal(CAND)', o['w_sal'] == R.CS.resumen('S1-ALIAS', 326, r)['w_sal']
          and o['deaths'] == r['deaths'] and N(o['termo']) == N(R.telemetria(r)))
    run0 = V144.run
    try:
        V144.run = lambda seed, **k: run0(seed, **dict(k, termo=0))
        e0 = R.tarea_ex(('CAND', 'E2', S))
    finally:
        V144.run = run0
    et = R.tarea_ex(('TRONCO', 'E2', S)); e1 = R.tarea_ex(('CAND', 'E2', S))
    anota('D', 'tarea_ex E2 (T = 100 000): bateria_v144b con termo=0 == bateria_v143 (CONGELADA) -> la copia es la misma bateria',
          R.iguales(e0, et), str(dif(e0, et, fuera=('org', 'seg'))[:5]))
    distinto('D', f"tarea_ex E2: bateria_v144b con la pieza (muerde A por cuarto {e1['mord']['A']}) != v14.3 ({et['mord']['A']})", e1, et,
             ['mord', 'W', 'deaths'])
    ent = R.G144.INSTRUMENTOS['organismo_v144b']
    try:
        R.G144.INSTRUMENTOS['organismo_v144b'] = (ent[0], dict(ent[1], termo=0))
        g0 = R.tarea_tb(('CAND', 'px0', S))
    finally:
        R.G144.INSTRUMENTOS['organismo_v144b'] = ent
    gt = R.tarea_tb(('TRONCO', 'px0', S))
    anota('D', 'tarea_tb px0 (T = 200 000): bateria_generaliza_v144b con termo=0 == bateria_generaliza_v143 (CONGELADA)',
          R.iguales(g0, gt), str(dif(g0, gt, fuera=('org', 'seg', 'modulo'))[:5]))

    print('--- (R) regla 14 (sin simular)')
    for nombre, ok in R.regla14():
        anota('R', nombre, ok)

    print('--- (J) el juez reproduce el examen de v14.3 (crudos y veredictos registrados, sin simular)')
    D143 = os.path.join(RAIZ, 'experimentos', 'tronco_v14_3_examen', 'datos')
    for modo, sello in (('serie', 'examen_v143_serie_20260924_124413'), ('replica', 'examen_v143_replica_20260924_131427')):
        J = json.load(open(os.path.join(D143, sello + '.json'), encoding='utf-8'))
        Vr = J['veredictos']
        lee = lambda etq: json.load(open(os.path.join(D143, f'{sello}_crudo_{etq}.json'), encoding='utf-8'))['corridas']
        vb = callado(R.veredicto_TB, lee('TB'))
        anota('J', f'{modo}: T-B (G1, G2, azares, K, pasa de CAND y TRONCO) == lo registrado',
              all(N({k: vb[o][k] for k in ('G1', 'G1_azar', 'G2', 'G2_azar', 'K', 'pasa')}) ==
                  N({k: Vr['TB'][o][k] for k in ('G1', 'G1_azar', 'G2', 'G2_azar', 'K', 'pasa')}) for o in ('CAND', 'TRONCO')))
        ve = callado(R.veredicto_EX, lee('EX'))
        anota('J', f'{modo}: T-E por escenario, T-C (i) y T-F examen == lo registrado',
              {e: ve['conducta'][e]['todas'] for e in R.U.SEIS} == {e: Vr['EX']['conducta'][e]['todas'] for e in R.U.SEIS}
              and ve['T_C_i'] == Vr['EX']['T_C_i'] and ve['T_F']['pasa'] == Vr['EX']['T_F']['pasa'] and ve['T_E'] == Vr['EX']['T_E'])
        vd = callado(R.veredicto_TD, lee('TD'))
        anota('J', f'{modo}: T-D (C1, C2, C6 de OFF y CAND) == lo registrado',
              all(N({c: vd[a][c] for c in ('C1', 'C2', 'C6')}) == N({c: Vr['TD'][a][c] for c in ('C1', 'C2', 'C6')}) for a in ('OFF', 'CAND')))
        vv = callado(R.veredicto_vivo, lee('TA'), lee('TCii'))
        anota('J', f'{modo}: T-A, T-C (ii), T-F vivo de CAND, TRONCO_B y PLACEBO == lo registrado (LI de TRONCO_B en VIVO '
                   f"{vv['TRONCO_B']['T-A']['brazos']['VIVO']['det_v4']['NI']['LI']})",
              all(vv[a]['v4'] == Vr['vivo'][a]['v4'] for a in ('CAND', 'TRONCO_B', 'PLACEBO'))
              and all(N(vv[a]['T-A']['brazos'][b]['det_v4']['NI']) == N(Vr['vivo'][a]['T-A']['brazos'][b]['det_v4']['NI'])
                      for a in ('CAND', 'TRONCO_B', 'PLACEBO') for b in R.U.BRAZOS_TA)
              and all(N(vv[a]['T-C_ii']['det_v4']['NI']) == N(Vr['vivo'][a]['T-C_ii']['det_v4']['NI']) for a in ('CAND', 'TRONCO_B', 'PLACEBO'))
              and vv['legible'] == Vr['vivo']['legible'])
        sub = R.subpuertas(dict(TB=vb, EX=ve, TD=vd, vivo=vv))
        anota('J', f'{modo}: las sub-puertas T-A..T-F == las registradas', all(sub[k] == J['sub'][k] for k in R.SUB if k != 'T-G'))

    print('--- (K) controles que DEBEN fallar o diferir')
    oA = R.tarea_vivo(('VIVO', 49906, 'OFF', T))
    distinto('K', 'TRONCO_B (s + 100000) != OFF en la misma semilla-etiqueta', R.tarea_vivo(('VIVO', 49906, 'TRONCO_B', T)), oA,
             ['r', 'deaths', 'descendientes', 'splits'])
    distinto('K', 'PLACEBO (placebo = 1) != OFF', R.tarea_vivo(('VIVO', 49906, 'PLACEBO', T)), oA, ['r', 'deaths', 'descendientes', 'splits'])
    Ss = R.U.SEMILLAS['serie']
    for malo in (False, True):
        RV, RR, TB, EXr, TD = R.sinteticos(80, 20, Ss['ALIAS'], Ss['LIMPIAS'], malo=malo)
        Vs = callado(lambda: dict(TB=R.veredicto_TB(TB), EX=R.veredicto_EX(EXr), TD=R.veredicto_TD(TD), vivo=R.veredicto_vivo(RV, RR),
                                  TG=R.veredicto_TG(RV)))
        P = R.puertas_de(R.subpuertas(Vs))
        if malo:
            anota('K', 'el juez dice NO a un candidato sintetico MALO en T-A, T-B, T-C, T-D y T-G (r y rev -40, azar 0.30, |W[sal]| 1.45)',
                  not any(P[k] for k in ('T-A', 'T-B', 'T-C', 'T-D', 'T-G')), str(P))
        else:
            anota('K', 'el juez dice SI al candidato sintetico bueno (gana +10 en r, el control pierde, la pieza actua) y la serie se lee',
                  all(P.values()) and Vs['vivo']['legible'], str(P))
            RV0 = RV
    b_ = R.U.TG['brazo']
    muta = {
        'CAND == OFF (d = 0: G-1 cae)': [dict(r, r=[x for x in RV0 if x['brazo'] == r['brazo'] and x['seed'] == r['seed'] and x['arm'] == 'OFF'][0]['r'])
                                         if r['arm'] == 'CAND' else r for r in RV0],
        'CAND gana +0.9 en todas (LI 0.9, no > m = 1: G-1 cae)': [dict(r, r=[x for x in RV0 if x['brazo'] == r['brazo'] and x['seed'] == r['seed'] and x['arm'] == 'OFF'][0]['r'] + 0.9)
                                                          if r['arm'] == 'CAND' else r for r in RV0],
        'el CONTROL gana +10 (G-2 cae)': [dict(r, r=r['r'] + 30.0) if r['arm'] == 'CTRL' else r for r in RV0],
        'la pieza no actua en 5/80 (G-3 cae: 0.9375 < 0.95)': [dict(r, termo=dict(r['termo'], a_no=0, a_si=0))
                                                               if (r['arm'] == 'CAND' and r['brazo'] == b_ and r['seed'] <= 5) else r for r in RV0],
        'falta una corrida del CANDIDATO (n 79: cae)': [r for r in RV0 if not (r['arm'] == 'CAND' and r['brazo'] == b_ and r['seed'] == 80)],
    }
    for etq, rv in muta.items():
        vg = callado(R.veredicto_TG, rv)
        anota('K', f'T-G: {etq}', vg['pasa'] is False, str({k: vg[b_][k] for k in ('G1', 'G2', 'G3')})[:200])
    vg = callado(R.veredicto_TG, [dict(r, r=r['r'] + 30.0) if (r['arm'] == 'CTRL' and r['brazo'] == 'VIVO') else r for r in RV0])
    anota('K', 'T-G: si el control gana SOLO en VIVO (informe), T-G sigue PASANDO (decide CUELLO_MIN, declarado)', vg['pasa'] is True)
    import inspect
    src = inspect.getsource(V144C.termo_letra).replace('U + s[_j] / 2', 'U + s[_j] / 3')
    ns = {}
    exec(src, ns)
    dm = 0
    for E in (1.2, 1.3, 1.35, 1.38):
        c = carro(CT, {'X': MEM['comida x5']}, 1.0)
        dm += int(bool(c._tm_boca('X', E, 2.0, True)) != bool(ns['termo_letra'](MEM['comida x5'], (E, 2.0), 1.0, True, 1)[0]))
    anota('K', f'una letra MUTADA (U + s/3) difiere del carro en {dm} de 4 casos (la comparacion de (L) tiene dientes)', dm > 0)
    for args, etq in ((['--humoo'], 'bandera desconocida --humoo'), (['--humo', '--humoo'], 'modo valido + bandera desconocida --humoo'),
                      (['--hum'], 'abreviatura --hum (allow_abbrev=False)'),
                      (['--serie'], 'modo de serie sin --pool'), (['--serie', '--pool', '9'], '--pool 9 (> 6)'),
                      (['--reserva', '--pool', '6'], '--reserva sin --sustituye'),
                      (['--serie', '--pool', '6', '--solo', 'TG'], '--solo TG (T-G no es etapa: sale de TA)'),
                      (['--combina', 'x.json'], '--combina (se llama --bloque)')):
        viejo, err = sys.argv, io.StringIO()
        sys.argv = ['corre_examen_v144b.py'] + args
        try:
            with contextlib.redirect_stderr(err):
                R.argumentos()
            codigo = 0
        except SystemExit as e:
            codigo = e.code
        finally:
            sys.argv = viejo
        anota('K', f'el parser del runner RECHAZA {etq} (argparse, codigo 2; solo se parsea, nunca se corre)',
              codigo == 2 and 'error:' in err.getvalue(), f"codigo {codigo}; {err.getvalue()[-160:]!r}")

    tot = f'RESULTADO: {OK[0]}/{OK[0] + NO[0]}'
    bloques = {}
    for d in DET:
        o, t = bloques.get(d['bloque'], (0, 0)); bloques[d['bloque']] = (o + d['ok'], t + 1)
    print('\n' + '  '.join(f'({b}) {o}/{t}' for b, (o, t) in bloques.items()) + f'   ({time.time() - t0:.0f} s)')
    os.makedirs(R.DATOS_HUMO, exist_ok=True)
    f = os.path.join(R.DATOS_HUMO, f"identidad_v144bex_{time.strftime('%Y%m%d_%H%M%S')}.json")
    json.dump(dict(T=T, semilla=S, total=tot, bloques=bloques, detalle=DET, seg=round(time.time() - t0, 1),
                   python=sys.version.split()[0], numpy=np.__version__), open(f, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print(f'datos -> {os.path.relpath(f, RAIZ)}  sha256_16 = {R.h16(f)}')
    print(tot)
    sys.exit(0 if NO[0] == 0 else 1)
