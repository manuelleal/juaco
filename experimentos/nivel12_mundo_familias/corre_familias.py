"""BLOQUE 1 — EL MUNDO QUE OBLIGA A REPRESENTAR, con v14.1 SIN CAMBIOS.
Ejecuta PREREGISTRO_bloque1_familias.md (su sha va en el meta del JSON). NO hay organo nuevo: el organismo es v14.1
tal cual; la unica perilla de organismo que se enciende en algun brazo es B-5 (`desambiguar`), una reparacion YA
medida (18/18 ALIAS, tronco identico), por encargo del coordinador.

    python experimentos/nivel12_mundo_familias/corre_familias.py --humo    (UN proceso, sin Pool: lo corre el disenador)
    python experimentos/nivel12_mundo_familias/corre_familias.py [--desde 401] [--T 100000] [--brazos EXC,LIN,...]
                                                                 [--nk 30] [--k 3] [--nkmax 90]

REGLA 3 y 11: el `Pool` lo lanza SOLO el coordinador, y nunca con otro `Pool` vivo. `--humo` es un proceso.
REGLA 10: log desde el arranque, con fsync, una linea por etapa con marca de tiempo.
ERR-31 (el runner leyo los umbrales de la bateria y no los del preregistro): TODOS los umbrales viven en el dict
UMBRALES de abajo, cada uno con la FRASE LITERAL del preregistro al lado. Ninguno se lee de otra parte.
ERR-38/42: el humo ESCRIBE su JSON; el catalogo y el alias se calculan con escala_codigo (bloque 0) IMPORTADO, y se
comparan CAMPO A CAMPO con el `cod0` que devuelve el propio instrumento (dos caminos al mismo numero).

Etapas:
  1/3 IDENTIDAD (subconjunto critico del arnes: A, G, I, J, N, P, L, M). Si no es 24/24, ABORTA.
  2/3 DIAGNOSTICO ESTRUCTURAL, ANTES de simular: alias exacto por par y por semilla, U3 (sim intra - inter) y la
      etiqueta SEPARABLE/ALIAS de cada una de las 8 ventanas de medida (subconjunto preregistrado, regla 10).
  3/3 PRINCIPAL: 8 brazos x 20 semillas (401-420; replica 421-440 con --desde 421) + el ancla V14.
"""
import sys, os, json, time, hashlib, platform, subprocess

sys.stdout.reconfigure(encoding='utf-8', errors='replace')
AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
CREB = os.path.join(RAIZ, 'experimentos', 'creacion_B')
sys.path[:0] = [AQUI, CREB, os.path.join(RAIZ, 'organismo')]   # organismo/ PRIMERO (ERR-28)
import numpy as np

T = 100000
T_ID = 20000
T_ID_LARGO = 120000
N_PARALELO = 14
N_SEM = 20
DESDE = 401
SEMILLAS_ID = [1, 2, 3]          # ninguna de 401-440 queda expuesta
SHA_V14_ESPERADO = 'feefc88b1fd8d434'
SHA_B5ON_ESPERADO = '2f7794d92e68cc89'
SHA_ESCALA_ESPERADO = 'd8b8566bca77a0ae'

# ---------------------------------------------------------------- el mundo, con los valores PREREGISTRADOS
# L = 160 y nobj = 16 estan DERIVADOS (PREREGISTRO 2.7): densidad 0.10 y distancia media 5 pasos, las del tronco.
# NK/NKMAX/K: los del TRONCO (PREREGISTRO 2.6, enmienda del coordinador tras el bloque 0). --nk/--k/--nkmax los cambian.
MUNDO = dict(mundo='familias', renov=1.0, largo=160, nobj=16,
             fam_D=12, fam_nvar=3, fam_F=8, fam_V=3, deriva=5000, cambio=None,
             vent=10000, crit_exp=0.5, n_exc=4, n_neu=0, fam_val='familia', desambiguar=0)
BRAZOS = {
    'EXC':    dict(MUNDO),
    'LIN':    dict(MUNDO, n_exc=0),
    'AZA':    dict(MUNDO, fam_val='azar'),
    'BAR':    dict(MUNDO, fam_val='barajado'),
    'EXC-B5': dict(MUNDO, desambiguar=1),
    'LIN-B5': dict(MUNDO, n_exc=0, desambiguar=1),
    'NEU':    dict(MUNDO, n_neu=2),
    'NEU-B5': dict(MUNDO, n_neu=2, desambiguar=1),
    'V14':    dict(mundo='AB'),          # ancla: v14.1 literal. NO compite en ninguna prediccion.
}
ORDEN = ['EXC', 'LIN', 'AZA', 'BAR', 'EXC-B5', 'LIN-B5', 'NEU', 'NEU-B5', 'V14']
BRAZOS_ACTIVOS = list(ORDEN)

CASOS_ID = {   # (etiqueta, modulo de referencia, kw de referencia, kw extra del instrumento, debe_diferir, T)
    'A': ("(A) mundo=AB == v14", 'V14', dict(), dict(), False, T_ID),
    'G': ("(G) linaje v13 (mask_rel=0, puerta_pat=0)", 'V14', dict(mask_rel=0, puerta_pat=0), dict(), False, T_ID),
    'I': ("(I) rng no consumido: mundo=AB a T=120000", 'V14', dict(), dict(), False, T_ID_LARGO),
    'J': ("(J) perillas del mundo puestas, mundo=AB", 'V14', dict(),
          dict(fam_D=12, fam_nvar=3, fam_F=8, fam_V=3, n_exc=4, n_neu=2, fam_val='barajado', deriva=1000,
               cambio=5000, vent=3000), False, T_ID),
    'N': ("(N) mundo=AB, desambiguar=1 == organismo_v14_codigo_on", 'B5', dict(desambiguar=1),
          dict(desambiguar=1), False, T_ID),
    'P': ("(P) familias n_neu=0: B-5 INERTE (P7a)", 'MF', dict(MUNDO, desambiguar=1), dict(MUNDO), False, T_ID),
    'L': ("(L) mundo=familias != v14 (DEBE diferir)", 'V14', dict(), dict(MUNDO), True, T_ID),
    'M': ("(M) mundo=AB con renov=1.0 != v14 (DEBE diferir)", 'V14', dict(), dict(renov=1.0), True, T_ID),
}

# ---------------------------------------------------------------- UMBRALES: la LETRA del preregistro (ERR-31)
UMBRALES = {
    'P1a': dict(frase="frac_veneno del anillo: mediana en [0.35, 0.65] en los 4 cuartos, en los 4 mundos",
                lo=0.35, hi=0.65),
    'P1b': dict(frase="razon exposiciones(veneno)/exposiciones(comida) mediana en [0.7, 1.4] (hoy: 6.3x y 23x)",
                lo=0.7, hi=1.4),
    'P1c': dict(frase="en `lineal`, v14.1 cruza criterio en >= 4 de los 8 tokens en >= 16/20 semillas",
                tokens_min=4, n_min=16),
    'P2': dict(frase="colateral(EXC) >= 2.0 x colateral(LIN) en razon de medianas Y A12(EXC > LIN) >= 0.75; "
                     "refuta si razon <= 1.3 o A12 <= 0.60; entre medias, INDECISO -> endurecer n_exc 4->8 con ERR-46",
               razon_pasa=2.0, a12_pasa=0.75, razon_refuta=1.3, a12_refuta=0.60),
    'P3': dict(frase="w_var(EXC) mediana >= 1.0 Y w_var(LIN) mediana <= 0.5 (acompana, no decide: razon >= 2.0 con "
                     "A12 >= 0.75)", exc_min=1.0, lin_max=0.5, razon_acomp=2.0, a12_acomp=0.75),
    'P4': dict(frase="exp_asoc mediana de las excepciones activas >= 3 x la de los tokens de la misma corrida, "
                     "pareado en >= 15/20; y exp_total(EXC) >= 1.3 x exp_total(LIN)",
               factor=3.0, n_min=15, razon_total=1.3),
    'P5': dict(frase="lineal < excepciones <= barajado <= azar en colateral Y en w_var (medianas): >= 3 de las 4 "
                     "desigualdades", n_min=3),
    'P6': dict(frase="arnes 43/43 (aqui su subconjunto critico 24/24); sha de organismo_v14.py == feefc88b1fd8d434"),
    'P7a': dict(frase="B-5 INERTE con n_neu=0: EXC-B5 == EXC y LIN-B5 == LIN BIT A BIT en 20/20, des_splits=0 en 20/20",
                n_min=20),
    'P7b': dict(frase="con n_neu=2: (i) des_splits >= 1 en >= 16/20; (ii) |W| de los neutros NEU-B5 <= 0.5 x NEU "
                      "pareado en >= 15/20; (iii) muertes NEU-B5 <= 1.10 x NEU y colateral NEU-B5 dentro de +-25% de NEU",
                i_min=16, ii_factor=0.5, ii_min=15, iii_muertes=1.10, iii_col=0.25),
}

_log = {'f': None, 't0': time.time()}


def log(msg=""):
    linea = f"[{time.strftime('%H:%M:%S')} +{time.time()-_log['t0']:7.1f}s] {msg}"
    print(linea, flush=True)
    if _log['f']:
        _log['f'].write(linea + "\n"); _log['f'].flush(); os.fsync(_log['f'].fileno())


def h16(p):
    return hashlib.sha256(open(p, 'rb').read()).hexdigest()[:16]


def N(x):
    return json.loads(json.dumps(x, default=str))


def med(xs):
    xs = [x for x in xs if x is not None]
    return round(float(np.median(xs)), 4) if xs else None


def cuartiles(xs):
    xs = [x for x in xs if x is not None]
    if not xs:
        return None
    return [round(float(np.percentile(xs, p)), 4) for p in (25, 50, 75)]


def razon(x, y):
    if x is None or y is None or y == 0:
        return None
    return round(x / y, 3)


def A12(xa, xb):
    """A12 SIN parear (ERR-37b: integrales de trayectoria nunca se parean). P(Xa > Xb) + 0.5 P(Xa == Xb)."""
    a = [v for v in xa if v is not None]; b = [v for v in xb if v is not None]
    if not a or not b:
        return None
    g = sum(1 for u in a for v in b if u > v) + 0.5 * sum(1 for u in a for v in b if u == v)
    return round(g / (len(a) * len(b)), 3)


def cuenta(da, db, semillas, f):
    """En cuantas semillas se cumple f(x_a, x_b). Un None NUNCA cuenta como victoria."""
    n = 0
    for s in semillas:
        x, y = da.get(s), db.get(s)
        if x is None or y is None:
            continue
        n += bool(f(x, y))
    return n


# ---------------------------------------------------------------- DIAGNOSTICO ESTRUCTURAL (antes de simular)
def diagnostico(seed, nk, ktop, kw):
    """El alias del mundo, calculado con las funciones del BLOQUE 0 (escala_codigo), no reimplementadas.
    Devuelve alias por par, alias por semilla, U3 (sim intra - inter) y la etiqueta SEPARABLE/ALIAS de cada una
    de las 8 ventanas de medida. PREREGISTRO 2.6 (enmienda del coordinador)."""
    import escala_codigo as EC
    D, F, V = kw['fam_D'], kw['fam_F'], kw['fam_V']
    P, fam, es_var, raiz, _ = EC.catalogo(D, F, V, seed)
    KW = EC.kw_del_tronco(seed, nk, D)
    M = EC.codigos(KW, P, ktop)
    n = P.shape[0]
    nom = []
    for i in range(n):
        k = int(fam[i])
        nom.append(('T%d' % k) if not bool(es_var[i]) else ('T%dv%d' % (k, i - int(raiz[i]) - 1)))
    cod = {nom[i]: sorted(np.flatnonzero(M[i]).tolist()) for i in range(n)}
    ident = np.zeros(n, bool)
    intra = []; inter = []; npar = 0; nid = 0
    for i in range(n):
        for j in range(i + 1, n):
            inter_c = int((M[i] * M[j]).sum())
            npar += 1
            if inter_c == ktop:
                nid += 1; ident[i] = ident[j] = True
            (intra if fam[i] == fam[j] else inter).append(inter_c / ktop)
    return dict(seed=seed, alias_pares=round(nid / npar, 5), alias_semilla=int(nid > 0),
                sim_intra=round(float(np.mean(intra)), 4), sim_inter=round(float(np.mean(inter)), 4),
                U3=round(float(np.mean(intra) - np.mean(inter)), 4),
                cod={k: v for k, v in cod.items()},
                ident={nom[i]: bool(ident[i]) for i in range(n)})


def etiqueta_ventanas(diag, exc_win):
    """Subconjunto preregistrado (regla 10): cada ventana es SEPARABLE o ALIAS."""
    return {e: ('ALIAS' if diag['ident'].get(e) else 'SEPARABLE') for e in exc_win}


# ---------------------------------------------------------------- lectura de una corrida
def clases(r):
    """exp_asoc por CLASE: token / variante (no excepcional) / excepcion activa / ventana de medida."""
    fam = r['fam']; exc = set(r['exc']); win = set(r['exc_win']); ea = r['exp_asoc']
    out = {'token': [], 'variante': [], 'excepcion': [], 'ventana': []}
    ncens = {'token': 0, 'variante': 0, 'excepcion': 0, 'ventana': 0}
    for k in sorted(r['val_mundo']):
        es_var = 'v' in k[1:]
        cl = 'excepcion' if k in exc else ('variante' if es_var else 'token')
        v = ea.get(k)
        (out[cl].append(v) if v is not None else ncens.__setitem__(cl, ncens[cl] + 1))
        if k in win:
            (out['ventana'].append(v) if v is not None else ncens.__setitem__('ventana', ncens['ventana'] + 1))
    return {c: med(out[c]) for c in out}, {c: len(out[c]) for c in out}, ncens, fam


def resumen(brazo, seed, r, kw):
    if r.get('mundo') is None or r.get('mundo') == 'AB':          # ancla V14: sin mundo de familias
        return dict(tipo='R', brazo=brazo, seed=seed, mundo='AB', deaths=r['deaths'], celdas=r['celdas'],
                    splits=r['splits'], W=r['W'], des_splits=r.get('des_splits'))
    m, ncl, ncens, _ = clases(r)
    val = r['val_mundo']; enc = r['exposiciones']
    ev = sum(v for k, v in enc.items() if val[k] == 'veneno')
    ec = sum(v for k, v in enc.items() if val[k] == 'comida')
    tok_cruza = sum(1 for k in val if 'v' not in k[1:] and r['exp_asoc'].get(k) is not None)
    # retencion: signo correcto en la ULTIMA visita de cada excepcion activa
    ret = [1 if (r['ultima'].get(e) and r['ultima'][e][2] and r['ultima'][e][1] * r['ultima'][e][2] > 0) else 0
           for e in r['exc']]
    neu = [abs(r['W'][k]) for k in val if val[k] == 'nada']
    exp_total = sum(v for v in r['exp_asoc'].values() if v is not None)
    return dict(tipo='R', brazo=brazo, seed=seed, mundo=r['mundo'],
                colateral=r['colateral'], omision=r['omision'], colateral_tot=r['colateral_tot'],
                w_var=r['w_var'], w_var_med=r['w_var_med'],
                exp_clase=m, n_clase=ncl, n_censura=ncens, exp_total=exp_total,
                exp_asoc=r['exp_asoc'], exposiciones=enc,
                exp_veneno=ev, exp_comida=ec, razon_exp=razon(ev, ec),
                tokens_cruzan=tok_cruza, retencion=(round(sum(ret) / len(ret), 3) if ret else None),
                neutros_W=(round(float(np.median(neu)), 3) if neu else None),
                frac_veneno=r['frac_veneno'], frac_regalo=r['frac_regalo'], renovados=r['renovados'],
                ruta=r['ruta'], deaths=r['deaths'], celdas=r['celdas'], splits=r['splits'],
                des_splits=r.get('des_splits'), exc=r['exc'], exc_win=r['exc_win'], cod0=r['cod0'],
                cod_cambia=sum(1 for k in r['cod0'] if r['cod0'][k] != r['cod_fin'][k]))


# ---------------------------------------------------------------- tareas
def tarea(args):
    tipo = args[0]
    if tipo == 'ID':
        _, cual, seed, nk, ktop, nkmax = args
        import organismo_v14 as V14, organismo_v14_codigo_on as B5ON, organismo_familias as MF
        etiq, ref, kwref, kwmf, debe, Ti = CASOS_ID[cual]
        mod = {'V14': V14, 'B5': B5ON, 'MF': MF}[ref]
        a = mod.run(seed, T=Ti, **kwref)
        # El instrumento recibe LOS MISMOS kwargs que la referencia, mas los del caso -- salvo cuando la referencia ES
        # el instrumento con otras perillas (caso P: kwref y kwmf son dos configuraciones completas del mundo).
        b = MF.run(seed, T=Ti, **kwmf) if ref == 'MF' else MF.run(seed, T=Ti, **{**kwref, **kwmf})
        salta = ('desambiguar', 'des_splits', 'des_t') if ref == 'MF' else ()
        base = {k: v for k, v in b.items() if k in a}
        dif = [k for k in a if k not in salta and N(a[k]) != N(base.get(k))]
        falta = [k for k in a if k not in b and k not in salta]
        igual = not dif and not falta
        return dict(tipo='ID', cual=cual, etiqueta=etiq, seed=seed, identico=igual, debe_diferir=debe,
                    ok=bool(igual != debe), difieren=dif[:6], faltan=falta)
    if tipo == 'D':
        _, seed, nk, ktop = args
        d = diagnostico(seed, nk, ktop, MUNDO)
        d.pop('cod')
        return dict(tipo='D', **d)
    _, brazo, seed, Ti, nk, ktop, nkmax = args
    import organismo_familias as MF
    kw = dict(BRAZOS[brazo])
    if kw.get('mundo') != 'AB':
        kw.update(nk=nk, ktop=ktop, nkmax=nkmax)
    return resumen(brazo, seed, MF.run(seed, T=Ti, **kw), kw)


SHAS = lambda: dict(
    preregistro=h16(os.path.join(AQUI, 'PREREGISTRO_bloque1_familias.md')),
    script=h16(os.path.abspath(__file__)),
    constructor=h16(os.path.join(AQUI, 'construye_familias.py')),
    instrumento=h16(os.path.join(AQUI, 'organismo_familias.py')),
    arnes=h16(os.path.join(AQUI, 'identidad_familias.py')),
    escala_codigo_bloque0=h16(os.path.join(AQUI, 'escala_codigo.py')),
    origen_organismo_v14=h16(os.path.join(RAIZ, 'organismo', 'organismo_v14.py')),
    origen_v14_codigo_on=h16(os.path.join(CREB, 'organismo_v14_codigo_on.py')))


def guarda_origen():
    s = SHAS()
    ok = True
    for k, esp in [('origen_organismo_v14', SHA_V14_ESPERADO), ('origen_v14_codigo_on', SHA_B5ON_ESPERADO),
                   ('escala_codigo_bloque0', SHA_ESCALA_ESPERADO)]:
        if s[k] != esp:
            log(f"*** ORIGEN CAMBIADO: {k} es {s[k]}, se esperaba {esp}. Reconstruir por anclas y repetir el arnes.")
            ok = False
    return ok


def cruza_cod0(res, diags):
    """ERR-38 aplicado al mundo: el codigo inicial calculado por escala_codigo (bloque 0) debe coincidir CAMPO A
    CAMPO con el `cod0` que devuelve el propio instrumento. Dos caminos al mismo numero."""
    D = {d['seed']: d for d in diags}
    mal = []
    for r in res:
        if r.get('mundo') in (None, 'AB') or 'cod0' not in r:
            continue
        d = D.get(r['seed'])
        if d is None or 'cod' not in d:
            continue
        for k, v in r['cod0'].items():
            if list(d['cod'].get(k, [])) != list(v):
                mal.append((r['seed'], k))
    return mal


# ---------------------------------------------------------------- veredicto (umbrales EXACTOS del preregistro)
def veredicto(res, SEEDS, diags):
    G = {b: {r['seed']: r for r in res if r['brazo'] == b} for b in BRAZOS_ACTIVOS}
    x = lambda b, c: {s: G.get(b, {}).get(s, {}).get(c) for s in SEEDS if s in G.get(b, {})}
    L = lambda b, c: [v for v in x(b, c).values()]
    V = {'umbrales': UMBRALES}

    # --- alias declarado (NO es puerta: covariable del mundo, PREREGISTRO 2.6)
    V['alias'] = dict(pares_mediana=med([d['alias_pares'] for d in diags]),
                      semillas_con_alias=sum(d['alias_semilla'] for d in diags), n=len(diags),
                      U3_mediana=med([d['U3'] for d in diags]))

    # --- P1 validez del mundo
    fv = [v for b in ('EXC', 'LIN', 'AZA', 'BAR') if b in G for r in G[b].values() for v in (r['frac_veneno'] or [])]
    u = UMBRALES['P1a']
    V['P1a'] = dict(mediana=med(fv), banda=[u['lo'], u['hi']],
                    pasa=bool(med(fv) is not None and u['lo'] <= med(fv) <= u['hi']))
    u = UMBRALES['P1b']
    rz = [v for b in ('EXC', 'LIN', 'AZA', 'BAR') if b in G for v in L(b, 'razon_exp')]
    V['P1b'] = dict(mediana=med(rz), banda=[u['lo'], u['hi']],
                    pasa=bool(med(rz) is not None and u['lo'] <= med(rz) <= u['hi']))
    u = UMBRALES['P1c']
    tk = L('LIN', 'tokens_cruzan')
    V['P1c'] = dict(mediana=med(tk), n=sum(1 for v in tk if v is not None and v >= u['tokens_min']),
                    pasa=bool(sum(1 for v in tk if v is not None and v >= u['tokens_min']) >= u['n_min']))
    V['P1'] = bool(V['P1a']['pasa'] and V['P1b']['pasa'] and V['P1c']['pasa'])

    # --- P2 colateral (LA QUE DECIDE)
    u = UMBRALES['P2']
    ce, cl = L('EXC', 'colateral'), L('LIN', 'colateral')
    r2, a2 = razon(med(ce), med(cl)), A12(ce, cl)
    V['P2'] = dict(med_EXC=med(ce), q_EXC=cuartiles(ce), med_LIN=med(cl), q_LIN=cuartiles(cl), razon=r2, A12=a2,
                   pasa=bool(r2 is not None and a2 is not None and r2 >= u['razon_pasa'] and a2 >= u['a12_pasa']),
                   refuta=bool(r2 is not None and a2 is not None and (r2 <= u['razon_refuta'] or a2 <= u['a12_refuta'])))
    V['P2']['indeciso'] = bool(not V['P2']['pasa'] and not V['P2']['refuta'])
    # La razon puede quedar INDEFINIDA por denominador cero (mediana del control = 0), no por datos que falten: se
    # marca explicitamente para que la lectura no sea ambigua (con mediana 0 en LIN, P2 se lee por A12 y cuartiles).
    V['P2']['razon_indefinida_denominador_cero'] = bool(med(cl) == 0)

    # --- P3 w_var (LA QUE DECIDE)
    u = UMBRALES['P3']
    we, wl = L('EXC', 'w_var_med'), L('LIN', 'w_var_med')
    r3, a3 = razon(med(we), med(wl)), A12(we, wl)
    V['P3'] = dict(med_EXC=med(we), q_EXC=cuartiles(we), med_LIN=med(wl), q_LIN=cuartiles(wl), razon=r3, A12=a3,
                   pasa=bool(med(we) is not None and med(wl) is not None and med(we) >= u['exc_min'] and med(wl) <= u['lin_max']),
                   acompana=bool(r3 is not None and a3 is not None and r3 >= u['razon_acomp'] and a3 >= u['a12_acomp']))
    V['P3']['razon_indefinida_denominador_cero'] = bool(med(wl) == 0)

    # --- P4 exposiciones
    u = UMBRALES['P4']
    ee = {s: (G['EXC'][s]['exp_clase']['excepcion'] if s in G.get('EXC', {}) else None) for s in SEEDS}
    et = {s: (G['EXC'][s]['exp_clase']['token'] if s in G.get('EXC', {}) else None) for s in SEEDS}
    n4 = cuenta(ee, et, SEEDS, lambda a, b: b and a >= u['factor'] * b)
    te, tl = L('EXC', 'exp_total'), L('LIN', 'exp_total')
    V['P4'] = dict(med_exc=med(list(ee.values())), med_token=med(list(et.values())), n_pareado=n4,
                   exp_total_EXC=med(te), exp_total_LIN=med(tl), razon_total=razon(med(te), med(tl)),
                   censura={b: [r['n_censura'] for r in G[b].values()][:1] for b in ('EXC', 'LIN') if b in G},
                   pasa=bool(n4 >= u['n_min'] and (razon(med(te), med(tl)) or 0) >= u['razon_total']))

    # --- P5 orden de los cuatro mundos
    u = UMBRALES['P5']
    mc = {b: med(L(b, 'colateral')) for b in ('LIN', 'EXC', 'BAR', 'AZA') if b in G}
    mw = {b: med(L(b, 'w_var_med')) for b in ('LIN', 'EXC', 'BAR', 'AZA') if b in G}
    des = []
    for m, nom in ((mc, 'colateral'), (mw, 'w_var')):
        if all(k in m and m[k] is not None for k in ('LIN', 'EXC', 'BAR', 'AZA')):
            des.append((f'{nom}: LIN < EXC', m['LIN'] < m['EXC']))
            des.append((f'{nom}: EXC <= BAR <= AZA', m['EXC'] <= m['BAR'] <= m['AZA']))
    V['P5'] = dict(colateral=mc, w_var=mw, desigualdades=des,
                   n=sum(1 for _, v in des if v), pasa=bool(sum(1 for _, v in des if v) >= u['n_min']))

    # --- P7a B-5 inerte con n_neu=0
    u = UMBRALES['P7a']
    ig = 0; n7 = 0
    for pa, pb in (('EXC', 'EXC-B5'), ('LIN', 'LIN-B5')):
        if pa in G and pb in G:
            for s in SEEDS:
                if s in G[pa] and s in G[pb]:
                    n7 += 1
                    ig += int(all(G[pa][s].get(c) == G[pb][s].get(c)
                                  for c in ('colateral', 'omision', 'w_var_med', 'deaths', 'celdas', 'splits',
                                            'exp_total', 'exp_asoc')))
    ds = [v for b in ('EXC-B5', 'LIN-B5') if b in G for v in L(b, 'des_splits')]
    V['P7a'] = dict(identicos=ig, n=n7, des_splits_no_cero=sum(1 for v in ds if v), pasa=bool(n7 and ig == n7 and not any(ds)))

    # --- P7b B-5 con estimulos que NO informan
    u = UMBRALES['P7b']
    dsn = L('NEU-B5', 'des_splits')
    wn_on = x('NEU-B5', 'neutros_W'); wn_off = x('NEU', 'neutros_W')
    n_ii = cuenta(wn_on, wn_off, SEEDS, lambda a, b: b and a <= u['ii_factor'] * b)
    mo, mn = med(L('NEU-B5', 'deaths')), med(L('NEU', 'deaths'))
    co, cn = med(L('NEU-B5', 'colateral')), med(L('NEU', 'colateral'))
    i1 = sum(1 for v in dsn if v)
    iii = bool(mo is not None and mn is not None and (mn == 0 or mo <= u['iii_muertes'] * mn)
               and co is not None and cn not in (None, 0) and abs(co / cn - 1) <= u['iii_col'])
    V['P7b'] = dict(des_splits_mediana=med(dsn), n_actua=i1, neutros_W_NEU=med(list(wn_off.values())),
                    neutros_W_NEU_B5=med(list(wn_on.values())), n_repara=n_ii,
                    muertes=[mn, mo], colateral=[cn, co],
                    i=bool(i1 >= u['i_min']), ii=bool(n_ii >= u['ii_min']), iii=iii)
    V['P7b']['pasa'] = bool(V['P7b']['i'] and V['P7b']['ii'] and V['P7b']['iii'])

    # --- lectura por brazo (linea base de T-A, T-F y T-G: lo que ESTE bloque entrega)
    V['linea_base'] = {b: dict(muertes=med(L(b, 'deaths')), q_muertes=cuartiles(L(b, 'deaths')),
                               frac_regalo=med(L(b, 'frac_regalo')), celdas=med(L(b, 'celdas')),
                               splits=med(L(b, 'splits')), colateral=med(L(b, 'colateral')),
                               omision=med(L(b, 'omision')), w_var=med(L(b, 'w_var_med')),
                               exp_total=med(L(b, 'exp_total')), retencion=med(L(b, 'retencion')),
                               ruta_exacto=med([(r or [0, 0])[0] for r in L(b, 'ruta')]),
                               ruta_lenta=med([(r or [0, 0])[1] for r in L(b, 'ruta')]),
                               exp_clase={c: med([ (d or {}).get(c) for d in L(b, 'exp_clase')])
                                          for c in ('token', 'variante', 'excepcion', 'ventana')})
                       for b in BRAZOS_ACTIVOS if b in G}
    return V


def frase_final(V):
    if not V.get('P1'):
        return ("P1 CAE: el mundo no es valido tal como esta construido (renovacion simetrica o habitabilidad). "
                "P2-P5 NO se leen. Clausula (iii): UNA correccion de `renov` con ERR-46 y semillas nuevas.")
    p2, p3 = V['P2'], V['P3']
    if p2['pasa'] and p3['pasa']:
        s = ("EL MUNDO OBLIGA: v14.1 paga cada excepcion contaminando a sus hermanos (colateral %s x) y ensuciando "
             "los pixeles de variable (w_var %s contra %s). " % (p2['razon'], p3['med_EXC'], p3['med_LIN']))
    elif p2['refuta'] and not p3['pasa']:
        s = ("EL MUNDO NO OBLIGA: con 4 excepciones sobre 32 estimulos la fuga por pixel de v14.1 basta "
             "(colateral %s x, w_var %s / %s). Se endurece n_exc 4->8 con ERR-46, semillas 441-460, misma letra; "
             "NO se toca el organismo. " % (p2['razon'], p3['med_EXC'], p3['med_LIN']))
    elif p2['indeciso']:
        s = ("INDECISO en P2 (razon %s, A12 %s, en la zona declarada): se endurece n_exc 4->8 con ERR-46 y se repite "
             "en 441-460. " % (p2['razon'], p2['A12']))
    else:
        s = ("MIXTO: P2 %s, P3 %s. " % ('pasa' if p2['pasa'] else ('refuta' if p2['refuta'] else 'indeciso'),
                                        'pasa' if p3['pasa'] else 'no'))
    if not V['P5']['pasa']:
        s += "OJO: P5 cae -- las medidas no ordenan los cuatro mundos; primero el instrumento, nada se declara. "
    s += ("B-5: %s con n_neu=0 (P7a %s); con estimulos que no informan %s (P7b). "
          % ('inerte' if V['P7a']['pasa'] else 'NO inerte', 'pasa' if V['P7a']['pasa'] else 'CAE',
             'repara' if V['P7b']['pasa'] else 'no repara segun la letra'))
    return s + "20 semillas no cierran nada: piden replica en el rango siguiente (regla 12)."


# ---------------------------------------------------------------- humo (UN proceso, sin Pool, regla 3)
def humo(nk, ktop, nkmax, Tb):
    stamp = time.strftime('%Y%m%d_%H%M%S')
    _log['f'] = open(os.path.join(RAIZ, 'datos', f'familias_humo_{stamp}.log'), 'w', encoding='utf-8', newline='\n')
    log("HUMO del disenador del bloque 1, UN proceso, sin Pool (regla 3). PREREGISTRO_bloque1_familias.md.")
    log("Semillas 1-2: NINGUNA de las 401-440 del bloque queda expuesta (E.14).")
    for k, v in SHAS().items():
        log(f"    sha {k:24s} {v}")
    log(f"    origenes verificados -> {'OK' if guarda_origen() else 'FALLA'}")
    log(f"    tamano de codigo (PREREGISTRO 2.6, enmienda del coordinador): NK={nk} NKMAX={nkmax} K={ktop}, D=12")
    sem = [1, 2]
    Ti = 5000

    log(f"1/3 IDENTIDAD, {len(CASOS_ID)} casos x {len(sem)} semillas (T corto = {Ti} salvo (I)).")
    ident = []
    for cual in CASOS_ID:
        etiq, ref, kwref, kwmf, debe, Tcaso = CASOS_ID[cual]
        CASOS_ID[cual] = (etiq, ref, kwref, kwmf, debe, Ti if cual != 'I' else 30000)
        for s in sem:
            ident.append(tarea(('ID', cual, s, nk, ktop, nkmax)))
        g = [r for r in ident if r['cual'] == cual]
        log(f"    {etiq:52s} {sum(r['ok'] for r in g)}/{len(g)}"
            + ("" if all(r['ok'] for r in g) else f"   difieren {g[0]['difieren']}"))
        CASOS_ID[cual] = (etiq, ref, kwref, kwmf, debe, Tcaso)
    log(f"  IDENTIDAD {sum(r['ok'] for r in ident)}/{len(ident)} (el arnes completo, 43/43, va en identidad_familias.py)")

    log("2/3 DIAGNOSTICO ESTRUCTURAL (antes de simular): alias exacto y ventanas SEPARABLE/ALIAS.")
    diags = []
    for s in sem:
        d = diagnostico(s, nk, ktop, MUNDO)
        diags.append(d)
        log(f"    semilla {s}: alias_pares {d['alias_pares']:.5f}  alias_semilla {d['alias_semilla']}  "
            f"sim_intra {d['sim_intra']}  sim_inter {d['sim_inter']}  U3 {d['U3']}")

    log(f"3/3 UNA corrida por brazo, T={Tb}, semillas {sem}.")
    res, t_b = [], {}
    for b in BRAZOS_ACTIVOS:
        t_b[b] = 0.0
        for s in sem:
            t1 = time.time(); r = tarea(('R', b, s, Tb, nk, ktop, nkmax)); t_b[b] += time.time() - t1
            res.append(r)
        t_b[b] = round(t_b[b] / len(sem), 2)
        g = [r for r in res if r['brazo'] == b]
        if b == 'V14':
            log(f"    {b:7s} {t_b[b]:5.2f} s  (ancla v14.1, 6 px)  muertes {[r['deaths'] for r in g]}  "
                f"celdas {[r['celdas'] for r in g]}")
            continue
        log(f"    {b:7s} {t_b[b]:5.2f} s  colateral {[r['colateral'] for r in g]}  omision {[r['omision'] for r in g]}  "
            f"w_var {[r['w_var_med'] for r in g]}  muertes {[r['deaths'] for r in g]}  "
            f"des_splits {[r['des_splits'] for r in g]}")
        log(f"            exp_clase {[r['exp_clase'] for r in g][0]}  tokens_cruzan {[r['tokens_cruzan'] for r in g]}  "
            f"razon_exp {[r['razon_exp'] for r in g]}  frac_veneno {[r['frac_veneno'] for r in g][0]}  "
            f"ruta {[r['ruta'] for r in g][0]}  retencion {[r['retencion'] for r in g]}")

    mal = cruza_cod0(res, [dict(d) for d in diags])
    log(f"  CRUCE cod0 (instrumento) contra escala_codigo (bloque 0): "
        f"{'IDENTICO campo a campo' if not mal else '*** DIFIERE en ' + str(mal[:5])}")
    for s in sem:
        g = [r for r in res if r['seed'] == s and r['brazo'] == 'EXC']
        if g:
            d = next(d for d in diags if d['seed'] == s)
            log(f"    semilla {s}: ventanas {etiqueta_ventanas(d, g[0]['exc_win'])}")
            log(f"    semilla {s}: excepciones activas {g[0]['exc']}")

    seg = sum(t_b.values()) / max(len(t_b), 1) * (T / Tb)
    n_corr = len(ORDEN) * N_SEM   # la estimacion es la del BLOQUE (9 brazos), no la del humo
    log(f"ESTIMACION del bloque: {n_corr} corridas de {T} pasos, ~{seg:.1f} s/corrida en serie -> "
        f"~{n_corr*seg/N_PARALELO/60:.1f} min de pared con Pool({N_PARALELO}).")
    log("HUMO: numeros observados, sin ajustar nada. n=2, T corto y semillas vistas: NO son evidencia (E.14).")

    dj = os.path.join(RAIZ, 'datos', f'familias_humo_{stamp}.json')
    with open(dj, 'w', encoding='utf-8') as f:
        json.dump(dict(meta=dict(fecha=time.strftime('%Y-%m-%dT%H:%M:%S'), tipo='humo', T_brazo=Tb, semillas=sem,
                                 T_bloque=T, nk=nk, ktop=ktop, nkmax=nkmax, brazos=N(BRAZOS), umbrales=UMBRALES,
                                 shas=SHAS(), segundos_por_brazo=t_b, cruce_cod0_ok=(not mal),
                                 python=platform.python_version(), numpy=np.__version__),
                       identidades=ident, diagnostico=diags, brazos=res),
                  f, ensure_ascii=False, default=str)
    log(f"datos -> {os.path.basename(dj)}  sha256_16 = {h16(dj)}")
    _log['f'].close()


# ---------------------------------------------------------------- principal
if __name__ == '__main__':
    arg = lambda n, d: (type(d)(sys.argv[sys.argv.index(n) + 1]) if n in sys.argv else d)
    nk, ktop, nkmax = arg('--nk', 30), arg('--k', 3), arg('--nkmax', 90)
    if '--brazos' in sys.argv:
        BRAZOS_ACTIVOS = [b.strip() for b in sys.argv[sys.argv.index('--brazos') + 1].split(',') if b.strip()]
        malos = [b for b in BRAZOS_ACTIVOS if b not in BRAZOS]
        if malos:
            raise SystemExit(f"--brazos: desconocido(s) {malos}. Validos: {ORDEN}")
        for req in ('EXC', 'LIN'):
            if req not in BRAZOS_ACTIVOS:
                raise SystemExit(f"--brazos: {req} es referencia obligatoria (P2/P3/P4 la necesitan).")
    if '--humo' in sys.argv:
        # EQUIPO regla 3: un agente corre <= 6 corridas de <= 200000 pasos. El humo son EXC y LIN x 2 semillas = 4
        # corridas a la T REAL del bloque (100000): asi `colateral` y `w_var` son los del regimen que se va a medir.
        # La inercia de B-5 (P7a) NO gasta corridas aqui: la comprueba el arnes (caso P) y el diagnostico (caso Q).
        if '--brazos' not in sys.argv:
            BRAZOS_ACTIVOS = ['EXC', 'LIN']
        humo(nk, ktop, nkmax, arg('--T', T)); sys.exit(0)

    import multiprocessing as mp
    mp.set_start_method('spawn', force=True)
    T = arg('--T', T)
    desde = arg('--desde', DESDE)
    SEEDS = list(range(desde, desde + N_SEM))
    stamp = time.strftime('%Y%m%d_%H%M%S')
    _log['f'] = open(os.path.join(RAIZ, 'datos', f'familias_s{SEEDS[0]}-{SEEDS[-1]}_{stamp}.log'),
                     'w', encoding='utf-8', newline='\n')
    log(f"ARRANQUE BLOQUE 1 (mundo de familias): brazos {BRAZOS_ACTIVOS}, semillas {SEEDS[0]}-{SEEDS[-1]}, T={T}. Pool({N_PARALELO}).")
    log(f"NK={nk} NKMAX={nkmax} K={ktop}, D=12 (PREREGISTRO 2.6: los del TRONCO; el alias se DECLARA, no se elimina).")
    log("NO hay organo nuevo. La unica perilla de organismo encendida en algun brazo es B-5, reparacion ya medida.")
    for k, v in SHAS().items():
        log(f"    sha {k:24s} {v}")
    if not guarda_origen():
        sys.exit(1)
    try:
        ps = subprocess.run(['powershell', '-NoProfile', '-Command',
                             "Get-CimInstance Win32_Process | Where-Object { $_.Name -like 'python*' } | "
                             "ForEach-Object { \"$($_.ProcessId) $($_.CommandLine)\" }"],
                            capture_output=True, text=True, timeout=60).stdout.strip().splitlines()
    except Exception as e:
        ps = [f"(no se pudo listar: {e})"]
    log(f"REGLA 11 — procesos python vivos ({len(ps)}), este es pid {os.getpid()}")

    V, res = {}, []
    with mp.Pool(N_PARALELO) as pool:
        ctrl = [('ID', c, s, nk, ktop, nkmax) for c in CASOS_ID for s in SEMILLAS_ID]
        log(f"ETAPA 1/3 — IDENTIDAD, subconjunto critico del arnes ({len(CASOS_ID)} casos x {len(SEMILLAS_ID)} "
            f"semillas = {len(ctrl)}). (L) y (M) DEBEN fallar: sin ellos la etapa pasa por vacuidad.")
        rc = pool.map(tarea, ctrl, chunksize=1)
        for cual in CASOS_ID:
            g = [r for r in rc if r['cual'] == cual]
            log(f"    {CASOS_ID[cual][0]:52s} {sum(r['ok'] for r in g)}/{len(g)}"
                + ("" if all(r['ok'] for r in g) else f"   difieren {g[0]['difieren']} faltan {g[0]['faltan']}"))
            V[f'ID_{cual}'] = all(r['ok'] for r in g)
        V['G_IDENTIDAD'] = bool(all(V[f'ID_{c}'] for c in CASOS_ID))
        log(f"  IDENTIDAD {sum(r['ok'] for r in rc)}/{len(rc)}")
        if not V['G_IDENTIDAD']:
            log("*** GUARDA DE IDENTIDAD FALLIDA: mundo='AB' no es v14.1 bit a bit (o el control que debe fallar "
                "no falla). Se para (P6).")
            sys.exit(1)

        log(f"ETAPA 2/3 — DIAGNOSTICO ESTRUCTURAL, ANTES de simular ({len(SEEDS)} semillas, T = 0).")
        diags = pool.map(tarea, [('D', s, nk, ktop) for s in SEEDS], chunksize=1)
        log(f"    alias por par mediana {med([d['alias_pares'] for d in diags])}  "
            f"semillas con algun par identico {sum(d['alias_semilla'] for d in diags)}/{len(diags)}  "
            f"U3 mediana {med([d['U3'] for d in diags])}")

        tr = [('R', b, s, T, nk, ktop, nkmax) for b in BRAZOS_ACTIVOS for s in SEEDS]
        log(f"ETAPA 3/3 — principal: {len(tr)} corridas de {T} pasos ({len(BRAZOS_ACTIVOS)} brazos x {len(SEEDS)} semillas)...")
        for i, r in enumerate(pool.imap_unordered(tarea, tr, chunksize=1), 1):
            res.append(r)
            if i % 20 == 0 or i == len(tr):
                log(f"          {i}/{len(tr)}")

    log()
    mal = cruza_cod0(res, [dict(d, cod=diagnostico(d['seed'], nk, ktop, MUNDO)['cod']) for d in diags])
    log(f"CRUCE cod0 (instrumento) contra escala_codigo (bloque 0): "
        f"{'IDENTICO campo a campo' if not mal else '*** DIFIERE en ' + str(mal[:5])}")
    V['cruce_cod0_ok'] = (not mal)
    log("ANALISIS — medianas y cuartiles por brazo, y despues los umbrales EXACTOS del preregistro (ERR-31).")
    V.update(veredicto(res, SEEDS, diags))
    for b, d in V['linea_base'].items():
        log(f"    {b:7s} muertes {d['muertes']} q{d['q_muertes']}  regalo {d['frac_regalo']}  celdas {d['celdas']}  "
            f"splits {d['splits']}  colateral {d['colateral']}  omision {d['omision']}  w_var {d['w_var']}  "
            f"exp_total {d['exp_total']}  exp_clase {d['exp_clase']}  retencion {d['retencion']}")
    ver = frase_final(V)
    log(); log(f"VEREDICTO: {ver}")

    meta = dict(fecha=time.strftime('%Y-%m-%dT%H:%M:%S'), semillas=SEEDS, T=T, nk=nk, ktop=ktop, nkmax=nkmax,
                brazos={b: N(BRAZOS[b]) for b in BRAZOS_ACTIVOS}, veredicto=ver, veredictos=N(V),
                identidades=rc, diagnostico=diags, procesos_python=ps, shas=SHAS(),
                origen_organismo_v14_esperado=SHA_V14_ESPERADO,
                python=platform.python_version(), numpy=np.__version__)
    dj = os.path.join(RAIZ, 'datos', f'familias_s{SEEDS[0]}-{SEEDS[-1]}_{stamp}.json')
    with open(dj, 'w', encoding='utf-8') as f:
        json.dump(dict(meta=meta, principal=res), f, ensure_ascii=False, default=str)
    log(f"datos -> {os.path.basename(dj)}  sha256_16 = {h16(dj)}")
    _log['f'].close()
