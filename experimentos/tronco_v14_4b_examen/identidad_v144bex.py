"""identidad_v144bex.py -- ARNES DE IDENTIDAD del examen v4 de v14.4b = v14.3 + TERMO' (UN proceso, sin Pool; se corre ANTES de
mirar numeros). Ultima linea: 'RESULTADO: N/N'. Escribe su JSON en datos/humo/ (ERR-42). Salida en identidad_v144bex_salida.txt.
MISION: llegar a la AGI por este camino.

(0) CONSTRUCCION: los nueve archivos en disco == construye_v144b.construye() (por anclas; origenes con sha) y todas las anclas
    reusadas del runner con su sha.
(A) PIEZA APAGADA == v14.3 BIT A BIT, TODAS las claves: organismo_v144b(termo=0) == organismo/organismo_v143 (CONGELADO) en 6
    escenarios; organismo_v144bg(termo=0) == organismo_v143g (px0, xor01, azar); organismo_v144bcal(termo=0) == organismo_v143cal en
    los cinco montajes del examen y con vivo=0.
(I) (2) INERTE SIN CONSIGNA: organismo_v144b con sus DEFECTOS (termo=1, rep_umbral=None) == organismo_v143 en la FISICA (todas las
    claves salvo la telemetria 'termo') en 12 escenarios, con dec = a_no = a_si = 0; organismo_v144bg con sus defectos == organismo_v143g
    en px0, xor01 y azar.
(T) (1) LA TABLA QUE OLVIDA, SIN INVERSION, DECIDE COMO TERMO: organismo_v144bcal(termo=1) == organismo_v144cal(termo=1) (TERMO) en la
    FISICA y en los contadores de la pieza (todo salvo termo.adS) en T-A VIVO, T-A CUELLO_MIN, T-D ALIAS 326 / LIMPIA 307, en DOS
    semillas (49045, 49046); TERMOINV igual; vivo=0 (una necesidad, U 1.0) igual; organismo_v144b/v144bg con rep_umbral=1.0 == TERMO
    (organismo_v144/v144g) en AB por defecto y px0. Si algo NO es identico se reporta la primera clave distinta (no se ajusta nada).
(V) LA REVERSION: con inversion la tabla que olvida CAMBIA algo (v144bcal T-C ii != v144cal T-C ii; v144b AB invertido con
    rep_umbral=1.0 != TERMO) y tras invertir la memoria de A es EXACTAMENTE el ultimo dS (veneno) y la de B la comida nueva.
(P) LA PIEZA ACTUA donde debe: v144bcal termo=1 != v143cal en T-A VIVO, CUELLO_MIN, T-C (ii) y T-D ALIAS con a_no + a_si > 0 (T-C ii:
    la condicion de T-R); TERMOINV != TERMO'; v144b con rep_umbral=1.0 != v14.3; determinismo; guardas.
(L) LA LETRA: termo_letra es el MISMO texto en los seis organismos (v144*, v144b*) y == Carro._tm_boca de V143_TERMO / V143_TERMOINV
    con memorias de la forma nueva [dE, dAg, 1] (casos sinteticos); la memoria del organismo en T-A VIVO == [ultimo dS nominal, 1].
(D) EL RUNNER: sus tareas corren lo declarado; tarea_ex E2 (T = 100 000) CAND == TRONCO (bateria_v144b con sus defectos == bateria_v143
    CONGELADA, todas las claves) y tarea_tb px0 (T = 200 000) CAND == TRONCO (bateria_generaliza_v144b == bateria_generaliza_v143).
(R) REGLA 14 del runner (sin simular).
(J) EL JUEZ reproduce, sin simular, los veredictos registrados del examen de v14.3 (serie y replica) y de la SERIE DE TERMO (47101-...:
    cae T-C y T-E), y sobre esta ultima T-R da NO (T-C ii NO con la pieza actuando 80/80).
(K) CONTROLES QUE DEBEN FALLAR: TRONCO_B != OFF; PLACEBO != OFF; el juez dice SI al sintetico bueno (ocho puertas) y NO al malo; T-R
    cae si la pieza no actua en 5/80 de T-C (ii) o si falta una corrida; T-G cae en sus mutaciones; una letra mutada difiere del carro;
    el PARSER rechaza banderas malas (solo se parsea; nunca se llama a main()).

    python experimentos/tronco_v14_4b_examen/identidad_v144bex.py
"""
import contextlib, io, json, os, sys, time

try:
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
except Exception:
    pass
AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
import corre_examen_v144b as R   # pone sys.path (organismo/, mundo vivo, criterio_v3/v4, creacion_B, dE5; al final v14.3, carros, v14.4)
import numpy as np

RAIZ = R.RAIZ
T = 20000
S = 49045            # semilla de IDENTIDAD (umbrales_examen_v144b.SEMILLAS['identidad']); S2 la segunda de (T)
S2 = 49046
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


def primera(a, b, d):
    """La primera clave distinta con sus dos valores (recortados): lo que se reporta si una identidad cae."""
    if not d:
        return ''
    k = d[0]
    return f"difieren {d[:6]}; {k}: {N(a.get(k))[:160]} != {N(b.get(k))[:160]}"


def igual(bloque, nombre, a, b, claves=None, fuera=()):
    d = dif(a, b, claves, fuera)
    anota(bloque, nombre, not d, primera(a, b, d))


def distinto(bloque, nombre, a, b, claves):
    d = dif(a, b, claves)
    anota(bloque, nombre + ' (DEBE diferir)', bool(d), 'SALIO IDENTICO')


def sin_adS(r):
    """La salida con la telemetria de la pieza SIN la tabla (la tabla es lo unico que debe diferir entre TERMO y TERMO')."""
    x = dict(r)
    if x.get('termo') is not None:
        x['termo'] = {k: v for k, v in x['termo'].items() if k != 'adS'}
    return x


def empate_ulp(modB, modA, fB, fA):
    """Corre fB (TERMO') y fA (TERMO) registrando CADA llamada a termo_letra de su modulo. Devuelve (identicas, texto, ok): si las
    salidas difieren, la PRIMERA decision distinta debe ser un EMPATE A NIVEL DE ULP: la memoria de TERMO' es el dS nominal exacto, la
    media de TERMO difiere de el en <= 4 ulp y el nivel cae entre los dos umbrales U + s/2 (nada mas explica la diferencia)."""
    L = {'b': [], 'a': []}
    viejo = (modB.termo_letra, modA.termo_letra)

    def envuelve(mod, k):
        f = mod.termo_letra
        def g(m, lev, U, mf, modo):
            r = f(m, lev, U, mf, modo); L[k].append((None if m is None else list(m), tuple(float(x) for x in lev), U, bool(mf), r)); return r
        mod.termo_letra = g
    try:
        envuelve(modB, 'b'); envuelve(modA, 'a')
        rb, ra = fB(), fA()
    finally:
        modB.termo_letra, modA.termo_letra = viejo
    if not dif(sin_adS(rb), sin_adS(ra)):
        return True, f'identicas ({len(L["b"])} consultas a la letra)', True
    for i, (x, y) in enumerate(zip(L['b'], L['a'])):
        if x[4] != y[4]:
            break
    else:
        return False, 'las salidas difieren sin decision distinta de la pieza (NO explicado)', False
    mb, lev, U = x[0], x[1], x[2]; ma = y[0]
    ok = bool(mb is not None and ma is not None and x[1] == y[1] and x[3] == y[3] and mb[-1] == 1)
    txt = f'consulta {i}: nivel {lev}, TERMO\' {mb} -> {x[4][0]}, TERMO {ma} -> {y[4][0]}'
    if ok:
        for j in range(len(mb) - 1):
            sb, sa = mb[j] / mb[-1], ma[j] / ma[-1]
            if sb > 0:
                ulps = abs(sa - sb) / np.spacing(sb)
                tb, ta = U + sb / 2, U + sa / 2
                ok &= bool(ulps <= 4 and min(tb, ta) <= lev[j] <= max(tb, ta))
                txt += f'; s {sb!r} contra {sa!r} ({ulps:.0f} ulp), umbrales {tb!r} / {ta!r}'
    return False, txt, ok


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
    import organismo_v3cal as CAL, organismo_v143cal as V143C, organismo_v144bcal as V144C, construye_v144b as CO
    import organismo_v144 as T144, organismo_v144g as T144G, organismo_v144cal as T144C   # TERMO (v14.4): solo se leen
    import V143_TERMO as CT, V143_TERMOINV as CTI
    print(f'ARNES identidad_v144bex — T={T}, semillas {S}/{S2}; python {sys.version.split()[0]}, numpy {np.__version__}')
    for nom, p in [('organismo_v143 (CONGELADO)', V143.__file__), ('organismo_v144b', V144.__file__), ('organismo_v143g (CONGELADO)', V143G.__file__),
                   ('organismo_v144bg', V144G.__file__), ('organismo_v3cal', CAL.__file__), ('organismo_v143cal', V143C.__file__),
                   ('organismo_v144bcal', V144C.__file__), ('organismo_v144 (TERMO)', T144.__file__), ('organismo_v144g (TERMO)', T144G.__file__),
                   ('organismo_v144cal (TERMO)', T144C.__file__), ('carro V143_TERMO', CT.__file__), ('carro V143_TERMOINV', CTI.__file__),
                   ('corre_examen_v144b', R.__file__), ('este arnes', os.path.abspath(__file__))]:
        print(f'  sha {nom:28s} {R.h16(p)}  {os.path.relpath(p, RAIZ)}')

    print('--- (0) construccion por anclas y anclas reusadas')
    C = CO.construye()
    for n_, txt in C.items():
        p = os.path.join(AQUI, n_)
        anota('0', f'{n_} en disco == construccion por anclas', os.path.exists(p) and open(p, 'rb').read().decode('utf-8') == txt)
    malas = [(os.path.relpath(p, RAIZ), R.h16(p), s) for p, s in R.ANCLAS.items() if R.h16(p) != s]
    anota('0', f'las {len(R.ANCLAS)} anclas reusadas tienen su sha (carros, examen de v14.3, TERMO y su serie)', not malas, str(malas))

    ESC = [('AB por defecto', dict()), ('AB invertido', dict(invertir_en=15000)),
           ('AB + patron nuevo C', dict(nuevo='C', nuevo_en=15000)), ('AB solap_AB=3 (E2L)', dict(solap_AB=3)),
           ('AB sin plasticidad', dict(plast=False)), ('AB via lenta apagada', dict(eta_s=0.0)),
           ('AB sin puerta', dict(puerta=None)), ('AB sin division por signo', dict(div_signo=False)),
           ('AB sin hija dispersa', dict(mask_rel=0)), ('AB sin puerta por codigo', dict(puerta_pat=0)),
           ('AB N apagada (norm_lenta=0)', dict(norm_lenta=0)),
           ('AB D comida solap_B=2 (E2K)', dict(nuevo='D', nuevo_val='comida', solap_B=2, nuevo_en=15000))]
    REF = {}
    print(f'--- (A) organismo_v144b(termo=0) == organismo_v143 (CONGELADO), T={T}')
    for etq, kw in ESC:
        REF[etq] = V143.run(S, T=T, **kw)
    for etq, kw in ESC[:6]:
        igual('A', f'{etq}: TERMO\' apagado == v14.3 (todas las claves)', V144.run(S, T=T, termo=0, **kw), REF[etq])
    KWG = R.G143.INSTRUMENTOS['organismo_v143'][1]
    REFG = {rg: V143G.run(S, T=T, mundo='regla', regla=rg, **KWG) for rg in ('px0', 'xor01', 'azar')}
    for rg in REFG:
        igual('A', f'regla/{rg}: TERMO\' apagado == v143g', V144G.run(S, T=T, mundo='regla', regla=rg, termo=0, **KWG), REFG[rg])
    MONT = [('T-A VIVO', R.C4.kw_vivo('VIVO', 'OFF')), ('T-A CUELLO_MIN', R.C4.kw_vivo('CUELLO_MIN', 'OFF')),
            ('T-C (ii) reversion en T/2', R.C4.kw_rev('OFF', T)),
            ('T-D ALIAS 326 (sal muda)', R.kw_sal('OFF')), ('T-D LIMPIA 307 (sal muda)', R.kw_sal('OFF'))]
    SEM = {'T-D ALIAS 326 (sal muda)': 326, 'T-D LIMPIA 307 (sal muda)': 307}
    R143 = {}
    for etq, kw in MONT:
        s = SEM.get(etq, S)
        R143[etq] = V143C.run(s, T=T, **dict(kw, norm_lenta=1))
        igual('A', f'{etq}: TERMO\' apagado == v143cal (todas las claves)', V144C.run(s, T=T, **dict(kw, norm_lenta=1, termo=0)), R143[etq])
    igual('A', 'vivo=0, n_nec=1: organismo_v144bcal(termo=0) == organismo_v143cal', V144C.run(S, T=T, vivo=0, n_nec=1, placebo=0, termo=0),
          V143C.run(S, T=T, vivo=0, n_nec=1, placebo=0))

    print(f'--- (I) (2) SIN CONSIGNA: organismo_v144b / v144bg con sus DEFECTOS (termo=1, rep_umbral=None) == v14.3 en la FISICA, T={T}')
    tele0 = True
    for etq, kw in ESC:
        a = V144.run(S, T=T, **kw)
        tele0 &= bool(a['termo']['termo'] == 1 and a['termo']['U'] is None and a['termo']['dec'] == a['termo']['a_no'] == a['termo']['a_si'] == 0)
        igual('I', f'{etq}: v144b (defectos) == v14.3 en la fisica (todo salvo la telemetria)', a, REF[etq], fuera=('termo',))
    anota('I', 'en los 12: la pieza encendida (termo 1) con U None NO decide: dec = a_no = a_si = 0', tele0)
    for rg in REFG:
        a = V144G.run(S, T=T, mundo='regla', regla=rg, **KWG)
        igual('I', f'regla/{rg}: v144bg (defectos) == v143g en la fisica (dec {a["termo"]["dec"]})', a, REFG[rg], fuera=('termo',))

    print(f'--- (T) (1) sin inversion, la tabla que olvida decide COMO TERMO: v144bcal == v144cal (todo salvo termo.adS), T={T}')
    PB = {}
    for s in (S, S2):
        for etq, kw in MONT:
            if etq.startswith('T-C'):
                continue
            ss = SEM.get(etq, s) if s == S else s   # la segunda semilla: 49046 tambien en los mundos de la sal (no importa si es ALIAS)
            b = V144C.run(ss, T=T, **dict(kw, norm_lenta=1, termo=1)); a = T144C.run(ss, T=T, **dict(kw, norm_lenta=1, termo=1))
            if s == S:
                PB[etq] = b
            igual('T', f'{etq} s{ss}: TERMO\' == TERMO en la fisica y los contadores (dec {b["termo"]["dec"]}, a_no {b["termo"]["a_no"]}, '
                       f'a_si {b["termo"]["a_si"]})', sin_adS(b), sin_adS(a))
    kwv = R.C4.kw_vivo('VIVO', 'OFF')
    igual('T', 'T-A VIVO: TERMOINV (termo=2) con la tabla que olvida == TERMOINV de TERMO', sin_adS(V144C.run(S, T=T, **dict(kwv, norm_lenta=1, termo=2))),
          sin_adS(T144C.run(S, T=T, **dict(kwv, norm_lenta=1, termo=2))))
    # UNA necesidad con consigna explicita (U 1.0; NINGUNO de estos montajes esta en el examen): la primera corrida del arnes (28-sep) dio
    # DISTINTO en vivo=0 y en AB; la primera decision distinta es un empate a nivel de ulp (E == 1.4 exacto contra U + s/2 = 1.4 en
    # TERMO' y 1.4000000000000001 con la media de TERMO, 0.8000000000000004). Se declara y se comprueba que es SOLO eso.
    for etq, fb, fa, mb_, ma_ in (('vivo=0, n_nec=1 (U 1.0): v144bcal vs v144cal', lambda: V144C.run(S, T=T, vivo=0, n_nec=1, placebo=0, termo=1),
                                   lambda: T144C.run(S, T=T, vivo=0, n_nec=1, placebo=0, termo=1), V144C, T144C),
                                  ('AB por defecto con rep_umbral=1.0 explicito: v144b vs TERMO (v144)', lambda: V144.run(S, T=T, rep_umbral=1.0),
                                   lambda: T144.run(S, T=T, rep_umbral=1.0), V144, T144),
                                  ('regla/px0 con rep_umbral=1.0 explicito: v144bg vs TERMO (v144g)',
                                   lambda: V144G.run(S, T=T, mundo='regla', regla='px0', rep_umbral=1.0, **KWG),
                                   lambda: T144G.run(S, T=T, mundo='regla', regla='px0', rep_umbral=1.0, **KWG), V144G, T144G)):
        ig, txt, ok = empate_ulp(mb_, ma_, fb, fa)
        anota('T', f"{etq}: {'IDENTICAS' if ig else 'DISTINTAS; la primera decision distinta es un EMPATE DE ULP'} -- {txt}", ok, txt)
    b1 = V144.run(S, T=T, rep_umbral=1.0)

    print(f'--- (V) la REVERSION: la tabla que olvida cambia algo tras invertir, y lo que guarda es el ULTIMO dS')
    kwr = R.C4.kw_rev('OFF', T)
    rb = V144C.run(S, T=T, **dict(kwr, norm_lenta=1, termo=1)); ra = T144C.run(S, T=T, **dict(kwr, norm_lenta=1, termo=1))
    distinto('V', f"T-C (ii) (invierte en {T // 2}): TERMO' != TERMO (rev TERMO' {rb['mord']['B'][3] - rb['mord']['A'][3]}, TERMO "
                  f"{ra['mord']['B'][3] - ra['mord']['A'][3]}; mordA Q4 {rb['mord']['A'][3]} / {ra['mord']['A'][3]})", rb, ra, ['mord', 'vis', 'deaths', 'W_nec'])
    EF, VAL = V144C.EFECTO, V144C.VAL_VIVO
    mA, mB = rb['termo']['adS'].get('A'), rb['termo']['adS'].get('B')
    anota('V', f"T-C (ii): tras invertir la memoria de A es EXACTAMENTE el veneno [-0.4, 0.0, 1] ({mA}) y la de B la comida [0.8, 0.0, 1] ({mB})",
          mA == [float(EF['veneno'][0]), float(EF['veneno'][1]), 1] and mB == [float(EF['comida'][0]), float(EF['comida'][1]), 1]
          and sum(rb['mord']['A'][2:]) > 0 and sum(rb['mord']['B'][2:]) > 0)
    bi = V144.run(S, T=T, invertir_en=15000, rep_umbral=1.0); ai = T144.run(S, T=T, invertir_en=15000, rep_umbral=1.0)
    distinto('V', f"examen AB invertido con rep_umbral=1.0: TERMO' != TERMO (muerde A por cuarto {bi['mord']['A']} / {ai['mord']['A']})", bi, ai,
             ['mord', 'deaths', 'W'])
    anota('V', f"examen AB invertido: la memoria de A tras invertir es [-0.4, 1] ({bi['termo']['adS'].get('A')}); la de TERMO era una suma "
               f"({ai['termo']['adS'].get('A')})", bi['termo']['adS'].get('A') == [float(V144.E_VAL['veneno']), 1])

    print('--- (P) la pieza ACTUA donde debe; guardas; determinismo')
    for etq in ('T-A VIVO', 'T-A CUELLO_MIN', 'T-D ALIAS 326 (sal muda)'):
        a1_ = PB[etq]
        distinto('P', f'{etq}: TERMO\' != v14.3 y a_no + a_si > 0 ({a1_["termo"]["a_no"]} / {a1_["termo"]["a_si"]})', a1_, R143[etq],
                 ['mord', 'vis', 'deaths', 'W_nec'] if actua(a1_) else [])
    distinto('P', f'T-C (ii): TERMO\' != v14.3 y a_no + a_si > 0 ({rb["termo"]["a_no"]} / {rb["termo"]["a_si"]}) -- la condicion de T-R',
             rb, R143['T-C (ii) reversion en T/2'], ['mord', 'vis', 'deaths', 'W_nec'] if actua(rb) else [])
    a2 = V144C.run(S, T=T, **dict(kwv, norm_lenta=1, termo=2))
    distinto('P', f'T-A VIVO: TERMOINV (termo=2) != TERMO\' y actua ({a2["termo"]["a_no"]} / {a2["termo"]["a_si"]})', a2, PB['T-A VIVO'],
             ['mord', 'deaths', 'W_nec'] if actua(a2) else [])
    distinto('P', f'examen AB con rep_umbral=1.0: la pieza decide ({b1["termo"]["a_no"]} / {b1["termo"]["a_si"]}) y difiere de v14.3', b1, REF['AB por defecto'],
             ['mord', 'vis', 'deaths', 'W'] if actua(b1) else [])
    igual('P', 'determinismo: T-A VIVO con TERMO\', dos veces, identico', V144C.run(S, T=T, **dict(kwv, norm_lenta=1, termo=1)), PB['T-A VIVO'])
    igual('P', 'determinismo: examen AB invertido con rep_umbral=1.0, dos veces, identico', V144.run(S, T=T, invertir_en=15000, rep_umbral=1.0), bi)
    anota('P', 'guardas: termo=2 con UNA necesidad aborta (v144b, v144bg, v144bcal con vivo=0); termo=3 aborta',
          aborta(V144.run, S, T=10, termo=2) and aborta(V144G.run, S, T=10, termo=2) and aborta(V144C.run, S, T=10, termo=2)
          and aborta(V144.run, S, T=10, termo=3) and aborta(V144C.run, S, T=10, termo=3, **R.C4.kw_vivo('VIVO', 'OFF')))

    print('--- (L) la LETRA (sin simular)')
    import inspect
    fuentes = {inspect.getsource(m.termo_letra) for m in (V144, V144G, V144C, T144, T144G, T144C)}
    anota('L', 'termo_letra es el MISMO texto en los seis organismos (v144b, v144bg, v144bcal y TERMO v144, v144g, v144cal)', len(fuentes) == 1)

    def carro(mod, mem, U):
        c = object.__new__(mod.Carro)
        c._adS = {k: list(v) for k, v in mem.items()}; c._tmU = float(U); c._tm = dict(dec=0, a_no=0, a_si=0, mord=0)
        return c
    MEM = {'desconocida': None, 'comida': [0.8, 0.0, 1], 'agua': [0.0, 0.8, 1], 'las dos': [0.8, 0.8, 1], 'veneno': [-0.4, 0.0, 1],
           'sal': [0.0, -0.4, 1], 'mixta': [0.8, -0.4, 1], 'nula': [0.0, 0.0, 1], 'chica': [0.1, 0.0, 1]}
    n_cas = n_mal = 0
    for U in (1.0, 0.5):
        niv = sorted({0.0, 0.99, 1.0, 1.2, 1.3999999, 1.4, 1.4000001, 1.5, U + 0.4, U + 0.05})
        for kk, m in MEM.items():
            for modo, mod in ((1, CT), (2, CTI)):
                for E in niv:
                    for Ag in niv:
                        for mf in (True, False):
                            c = carro(mod, {} if m is None else {'X': m}, U)
                            bc = c._tm_boca('X', E, Ag, mf)
                            bo, go = V144C.termo_letra(None if m is None else list(m), (float(E), float(Ag)), U, mf, modo)
                            n_cas += 1; n_mal += int(bool(bc) != bool(bo) or c._tm['dec'] != int(go) or c._tm['mord'] != int(bo and go))
    anota('L', f'termo_letra == V143_TERMO / V143_TERMOINV ._tm_boca con memorias de la forma nueva [dE, dAg, 1]: {n_cas} casos, {n_mal} distintos',
          n_mal == 0 and n_cas > 0)
    a1_ = PB['T-A VIVO']
    okm = all(v == [float(EF[VAL[k]][0]), float(EF[VAL[k]][1]), 1] for k, v in a1_['termo']['adS'].items())
    anota('L', f"T-A VIVO: la memoria del organismo == [ultimo dS nominal, 1] por estimulo ({a1_['termo']['adS']})", okm and len(a1_['termo']['adS']) == 4)

    print('--- (D) las tareas del runner corren lo declarado (con el candidato INERTE donde (2) lo dice)')
    kwc = R.kw_vivo_cand('VIVO'); r = V144C.run(S, T=T, **kwc)
    o = R.tarea_vivo(('VIVO', S, 'CAND', T))
    igual('D', 'tarea_vivo CAND == resumen de organismo_v144bcal con kw_vivo_cand (norm_lenta=1, termo=1)', o,
          dict(R.CR2.resumen2('VIVO', S, r, kwc, T), termo=R.telemetria(r)), fuera=('seed_real', 'arm', 'placebo', 'des_splits', 'seg', 'org'))
    ok_ = R.tarea_vivo(('VIVO', S, 'CTRL', T)); oo = R.tarea_vivo(('VIVO', S, 'OFF', T))
    anota('D', f"tarea_vivo CTRL corre termo=2 ({ok_['termo']['termo']}) y difiere de CAND; CAND difiere de OFF",
          ok_['termo']['termo'] == 2 and not R.iguales(ok_, o) and not R.iguales(o, oo))
    r = V144C.run(S, T=T, **R.kw_rev_cand(T)); o = R.tarea_rev((S, 'CAND', T))
    anota('D', 'tarea_rev CAND == organismo_v144bcal con kw_rev_cand (rev, mordidas, muertes, telemetria)',
          o['rev'] == r['mord']['B'][3] - r['mord']['A'][3] and o['deaths'] == r['deaths'] and o['mordA'] == r['mord']['A']
          and N(o['termo']) == N(R.telemetria(r)))
    r = V144C.run(326, T=T, **R.kw_sal('CAND')); o = R.tarea_sal(('S1-ALIAS', 326, 'CAND', T))
    anota('D', 'tarea_sal CAND == organismo_v144bcal con kw_sal(CAND)', o['w_sal'] == R.CS.resumen('S1-ALIAS', 326, r)['w_sal']
          and o['deaths'] == r['deaths'] and N(o['termo']) == N(R.telemetria(r)))
    e1 = R.tarea_ex(('CAND', 'E2', S)); et = R.tarea_ex(('TRONCO', 'E2', S))
    anota('D', f"tarea_ex E2 (T = 100 000): bateria_v144b CON SUS DEFECTOS == bateria_v143 (CONGELADA), todas las claves (muerde A por cuarto "
               f"{e1['mord']['A']} / {et['mord']['A']})", R.iguales(e1, et), primera(e1, et, dif(e1, et, fuera=('org', 'seg', 'termo'))))
    g1 = R.tarea_tb(('CAND', 'px0', S)); gt = R.tarea_tb(('TRONCO', 'px0', S))
    anota('D', 'tarea_tb px0 (T = 200 000): bateria_generaliza_v144b CON SUS DEFECTOS == bateria_generaliza_v143 (CONGELADA)',
          R.iguales(g1, gt), primera(g1, gt, dif(g1, gt, fuera=('org', 'seg', 'modulo', 'termo'))))

    print('--- (R) regla 14 (sin simular)')
    for nombre, ok in R.regla14():
        anota('R', nombre, ok)

    print('--- (J) el juez reproduce los examenes registrados (sin simular)')

    def juez(carpeta, sello):
        J = json.load(open(os.path.join(carpeta, sello + '.json'), encoding='utf-8'))
        lee = lambda etq: json.load(open(os.path.join(carpeta, f'{sello}_crudo_{etq}.json'), encoding='utf-8'))['corridas']
        V = dict(TB=callado(R.veredicto_TB, lee('TB')), EX=callado(R.veredicto_EX, lee('EX')), TD=callado(R.veredicto_TD, lee('TD')),
                 vivo=callado(R.veredicto_vivo, lee('TA'), lee('TCii')))
        if 'examen_v144_' in sello:   # T-G de ESTE examen (la de TERMO); el examen de v14.3 tenia otra T-G (no se compara)
            V['TG'] = callado(R.veredicto_TG, lee('TA'))
        return J, V
    D143 = os.path.join(RAIZ, 'experimentos', 'tronco_v14_3_examen', 'datos')
    D144 = os.path.join(RAIZ, 'experimentos', 'tronco_v14_4_examen', 'datos')
    for etq_, carpeta, sello in (('v14.3 serie', D143, 'examen_v143_serie_20260924_124413'), ('v14.3 replica', D143, 'examen_v143_replica_20260924_131427'),
                                 ('TERMO serie', D144, 'examen_v144_serie_20260928_123734')):
        J, V = juez(carpeta, sello)
        Vr = J['veredictos']
        anota('J', f'{etq_}: T-B (G1, G2, azares, K, pasa de CAND y TRONCO) == lo registrado',
              all(N({k: V['TB'][o_][k] for k in ('G1', 'G1_azar', 'G2', 'G2_azar', 'K', 'pasa')}) ==
                  N({k: Vr['TB'][o_][k] for k in ('G1', 'G1_azar', 'G2', 'G2_azar', 'K', 'pasa')}) for o_ in ('CAND', 'TRONCO')))
        ve = V['EX']
        anota('J', f'{etq_}: T-E por escenario, T-C (i) y T-F examen == lo registrado',
              {e: ve['conducta'][e]['todas'] for e in R.U.SEIS} == {e: Vr['EX']['conducta'][e]['todas'] for e in R.U.SEIS}
              and ve['T_C_i'] == Vr['EX']['T_C_i'] and ve['T_F']['pasa'] == Vr['EX']['T_F']['pasa'] and ve['T_E'] == Vr['EX']['T_E'])
        anota('J', f'{etq_}: T-D (C1, C2, C6 de OFF y CAND) == lo registrado',
              all(N({c: V['TD'][a][c] for c in ('C1', 'C2', 'C6')}) == N({c: Vr['TD'][a][c] for c in ('C1', 'C2', 'C6')}) for a in ('OFF', 'CAND')))
        vv = V['vivo']
        anota('J', f'{etq_}: T-A, T-C (ii), T-F vivo de CAND, TRONCO_B y PLACEBO == lo registrado',
              all(vv[a]['v4'] == Vr['vivo'][a]['v4'] for a in ('CAND', 'TRONCO_B', 'PLACEBO'))
              and all(N(vv[a]['T-A']['brazos'][b]['det_v4']['NI']) == N(Vr['vivo'][a]['T-A']['brazos'][b]['det_v4']['NI'])
                      for a in ('CAND', 'TRONCO_B', 'PLACEBO') for b in R.U.BRAZOS_TA)
              and all(N(vv[a]['T-C_ii']['det_v4']['NI']) == N(Vr['vivo'][a]['T-C_ii']['det_v4']['NI']) for a in ('CAND', 'TRONCO_B', 'PLACEBO'))
              and vv['legible'] == Vr['vivo']['legible'])
        sub = R.subpuertas(V)
        ks = [k for k in R.SUB if k != 'T-R' and (k != 'T-G' or 'TG' in V)]
        anota('J', f'{etq_}: las sub-puertas {ks[0]}..{ks[-1]} == las registradas', all(sub[k] == J['sub'][k] for k in ks), str({k: (sub[k], J['sub'].get(k)) for k in ks}))
        if etq_ == 'TERMO serie':
            tr = vv['T_R']
            anota('J', f"TERMO serie: T-R da NO (T-C ii {tr['T_C_ii']} con la pieza actuando {tr['actua']}/{tr['n']}) y el veredicto por la letra "
                       f"de v14.4b es NO PASA por T-C, T-E y T-R", tr['pasa'] is False and tr['T_C_ii'] is False and tr['actua'] == tr['n'] == 80
                  and [k for k, v in R.puertas_de(sub).items() if v is False] == ['T-C', 'T-E', 'T-R'])

    print('--- (K) controles que DEBEN fallar o diferir')
    oA = R.tarea_vivo(('VIVO', 49047, 'OFF', T))
    distinto('K', 'TRONCO_B (s + 100000) != OFF en la misma semilla-etiqueta', R.tarea_vivo(('VIVO', 49047, 'TRONCO_B', T)), oA,
             ['r', 'deaths', 'descendientes', 'splits'])
    distinto('K', 'PLACEBO (placebo = 1) != OFF', R.tarea_vivo(('VIVO', 49047, 'PLACEBO', T)), oA, ['r', 'deaths', 'descendientes', 'splits'])
    Ss = R.U.SEMILLAS['serie']
    for malo in (False, True):
        RV, RR, TB, EXr, TD = R.sinteticos(80, 20, Ss['ALIAS'], Ss['LIMPIAS'], malo=malo)
        Vs = callado(lambda: dict(TB=R.veredicto_TB(TB), EX=R.veredicto_EX(EXr), TD=R.veredicto_TD(TD), vivo=R.veredicto_vivo(RV, RR),
                                  TG=R.veredicto_TG(RV)))
        P = R.puertas_de(R.subpuertas(Vs))
        if malo:
            anota('K', 'el juez dice NO a un candidato sintetico MALO en T-A, T-B, T-C, T-D, T-G y T-R', not any(P[k] for k in ('T-A', 'T-B', 'T-C', 'T-D', 'T-G', 'T-R')), str(P))
        else:
            anota('K', 'el juez dice SI al sintetico bueno en las OCHO puertas (siete de v4 + T-R) y la serie se lee',
                  all(P.values()) and len(P) == 8 and Vs['vivo']['legible'], str(P))
            RV0, RR0 = RV, RR
    for etq, rr in (('la pieza no actua en 5/80 corridas CAND de T-C (ii) (0.9375 < 0.95)',
                     [dict(r, termo=dict(r['termo'], a_no=0, a_si=0)) if (r['arm'] == 'CAND' and r['seed'] <= 5) else r for r in RR0]),
                    ('falta la telemetria de una corrida CAND de T-C (ii) (n 79)',
                     [dict(r, termo=None) if (r['arm'] == 'CAND' and r['seed'] == 80) else r for r in RR0])):
        vv = callado(R.veredicto_vivo, RV0, rr)
        anota('K', f"T-R cae si {etq}, aunque T-C (ii) pase ({vv['T_R']})", vv['T_R']['pasa'] is False and vv['T_R']['T_C_ii'] is True)
    b_ = R.U.TG['brazo']
    off_r = {(x['brazo'], x['seed']): x['r'] for x in RV0 if x['arm'] == 'OFF'}
    muta = {
        'CAND == OFF (d = 0: G-1 cae)': [dict(r, r=off_r[(r['brazo'], r['seed'])]) if r['arm'] == 'CAND' else r for r in RV0],
        'el CONTROL gana (G-2 cae)': [dict(r, r=r['r'] + 30.0) if r['arm'] == 'CTRL' else r for r in RV0],
        'la pieza no actua en 5/80 de T-A (G-3 cae)': [dict(r, termo=dict(r['termo'], a_no=0, a_si=0))
                                                       if (r['arm'] == 'CAND' and r['brazo'] == b_ and r['seed'] <= 5) else r for r in RV0],
    }
    for etq, rv in muta.items():
        anota('K', f'T-G: {etq}', callado(R.veredicto_TG, rv)['pasa'] is False)
    src = inspect.getsource(V144C.termo_letra).replace('U + s[_j] / 2', 'U + s[_j] / 3')
    ns = {}
    exec(src, ns)
    dm = sum(int(bool(carro(CT, {'X': [0.8, 0.0, 1]}, 1.0)._tm_boca('X', E, 2.0, True)) != bool(ns['termo_letra']([0.8, 0.0, 1], (E, 2.0), 1.0, True, 1)[0]))
             for E in (1.2, 1.3, 1.35, 1.38))
    anota('K', f'una letra MUTADA (U + s/3) difiere del carro en {dm} de 4 casos (la comparacion de (L) tiene dientes)', dm > 0)
    for args, etq in ((['--humoo'], 'bandera desconocida --humoo'), (['--hum'], 'abreviatura --hum (allow_abbrev=False)'),
                      (['--serie'], 'modo de serie sin --pool'), (['--serie', '--pool', '9'], '--pool 9 (> 6)'),
                      (['--reserva', '--pool', '6'], '--reserva sin --sustituye'), (['--serie', '--pool', '6', '--solo', 'TR'], '--solo TR (T-R sale de TC)')):
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
        anota('K', f'el parser del runner RECHAZA {etq} (codigo 2; solo se parsea)', codigo == 2 and 'error:' in err.getvalue(), f'codigo {codigo}')

    tot = f'RESULTADO: {OK[0]}/{OK[0] + NO[0]}'
    bloques = {}
    for d in DET:
        o_, t_ = bloques.get(d['bloque'], (0, 0)); bloques[d['bloque']] = (o_ + d['ok'], t_ + 1)
    print('\n' + '  '.join(f'({b}) {o_}/{t_}' for b, (o_, t_) in bloques.items()) + f'   ({time.time() - t0:.0f} s)')
    os.makedirs(R.DATOS_HUMO, exist_ok=True)
    f = os.path.join(R.DATOS_HUMO, f"identidad_v144bex_{time.strftime('%Y%m%d_%H%M%S')}.json")
    json.dump(dict(T=T, semillas=[S, S2], total=tot, bloques=bloques, detalle=DET, seg=round(time.time() - t0, 1),
                   python=sys.version.split()[0], numpy=np.__version__), open(f, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print(f'datos -> {os.path.relpath(f, RAIZ)}  sha256_16 = {R.h16(f)}')
    print(tot)
    sys.exit(0 if NO[0] == 0 else 1)
