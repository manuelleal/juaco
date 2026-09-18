"""MUNDO VIVO (nivel 11) — ejecuta PREREGISTRO_mundo_vivo.md (EN FIRME, commit 69bfc36, con la nota del
coordinador del 18-sep 07:50 y sin ningun cambio de criterio; su sha va en el meta del JSON): dos necesidades
(hambre, sed) y cuatro estimulos (comida A, veneno B, agua C, sal D), estado interno vectorial con DOS muertes,
boca que decide con la necesidad ACTIVA y valor aprendido POR ESTIMULO Y POR NECESIDAD.
REGLA 10: log desde el arranque, con fsync, una linea por etapa con marca de tiempo.

    python experimentos/nivel11_mundo_vivo/corre_vivo.py [--desde 181] [--T 100000] [--brazos VIVO,ESCALAR,...]
    python experimentos/nivel11_mundo_vivo/corre_vivo.py --humo    (UN proceso, sin Pool: lo corre el disenador)

T = 100000 (no 200000). Razon, escrita antes de correr: el preregistro NO fija T, y todos sus umbrales son
RAZONES entre brazos (muertes, exposiciones) o cruces TEMPRANOS de criterio (`exp_hasta`, mediana 2-9 exposiciones
en la mini-prueba); ninguno depende de la longitud de la corrida. Dejarlo en 100000 mantiene la mini-prueba
(seccion 9 del preregistro) DIRECTAMENTE comparable con el bloque, que es lo unico que T decide aqui, y es el
valor por defecto del proyecto (regla 6 de CLAUDE.md). `--T` lo cambia y queda registrado en el meta del JSON.

ERR-31 (la leccion: el runner leyo los umbrales de la bateria y no los del preregistro; el registro sigue la
LETRA): todos los umbrales de P1-P9 estan en el dict UMBRALES de abajo, cada uno con la FRASE LITERAL del
preregistro al lado. Ninguno se lee de una bateria ni se recalcula aqui.

Etapas con Pool (las corre el COORDINADOR, reglas 3 y 11):
  1/2 IDENTIDAD interna, 5 casos del arnes identidad_vivo.py x 3 semillas (15 comprobaciones):
      (A) vivo=0 == organismo_v14 · (G) linaje v13 (mask_rel=0, puerta_pat=0) · (I) TODO ENCENDIDO con UNA
      necesidad y DOS estimulos == organismo_v14 · (J) lo mismo con inversion · (M) el control que DEBE FALLAR
      (4 estimulos y 2 necesidades != v14; sin el, la etapa pasaria por vacuidad). Si no es 15/15, ABORTA.
  2/2 principal: 7 brazos x 20 semillas (semillas 181-200; replica 201-220 con --desde 201).

Brazos: los de mini_vivo.py, importados SIN copiar (VIVO, UNA_NEC, ESCALAR, BARAJA_POL, BARAJA_CON, NO_INFORMA)
+ V14 (el ancla: una necesidad, dos estimulos, `costo` del tronco), que es ademas la REFERENCIA de P5.
BARAJA_POL es DIAGNOSTICO: mide que compra la politica, y su unico criterio es P3b (muertes).

20 semillas no cierran un nivel del brief: cierran o refutan ESTE mecanismo, y piden replica en 201-220.
Vocabulario (regla 6): "necesidad activa", "valor por necesidad", "exposiciones hasta criterio", "XOR necesidad x
estimulo" y "dos muertes" son las cantidades del preregistro. Nada mas: no se declara "propósito" ni "entiende".
"""
import sys, os, json, time, hashlib, platform, subprocess
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
import numpy as np

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
sys.path[:0] = [AQUI, os.path.join(RAIZ, 'organismo')]   # organismo/ PRIMERO (ERR-28)

import mini_vivo as MV        # brazos, celdas informativas, celdas del XOR y lee(): definidos ANTES de ver numeros

T = 100000
T_ID = 20000                  # el T del arnes identidad_vivo.py
N_PARALELO = 14
N_SEM = 20
DESDE = 181
SEMILLAS_ID = [1, 2, 3]       # semillas del arnes: NINGUNA de las 181-200 queda expuesta
SHA_V14_ESPERADO = 'feefc88b1fd8d434'   # organismo/organismo_v14.py = v14.1, el origen por anclas del instrumento

# V14 = el ancla y la REFERENCIA de P5: una necesidad, dos estimulos, el `costo` del TRONCO (0.002), sin drenaje
# de agua. Todo lo demas viene de mini_vivo.py sin tocar.
BRAZOS = dict(MV.BRAZOS)
BRAZOS['V14'] = dict(vivo=1, n_nec=1, estims=('A', 'B'), costo_a=0.0, A_ini=1.0)
ORDEN = ['V14', 'VIVO', 'UNA_NEC', 'ESCALAR', 'BARAJA_CON', 'NO_INFORMA', 'BARAJA_POL']
BRAZOS_ACTIVOS = list(ORDEN)
APAG = dict(vivo=0, n_nec=1)
VIVO1 = dict(vivo=1, n_nec=1, estims=('A', 'B'), costo_a=0.0, A_ini=1.0)
NUEVAS = {'n_nec', 'estims', 'agua', 'muertes_nec', 'exp_hasta', 'exposiciones', 'W_nec', 'xor_mord', 'xor_enc',
          'sorp_nec'}
CASOS_ID = {   # (etiqueta, kw de v14, kw extra de organismo_vivo, debe_diferir)
    'A': ("(A) vivo=0 == v14", dict(), APAG, False),
    'G': ("(G) linaje v13 (mask_rel=0, puerta_pat=0)", dict(mask_rel=0, puerta_pat=0), APAG, False),
    'I': ("(I) TODO encendido, 1 necesidad y 2 estimulos == v14", dict(), VIVO1, False),
    'J': ("(J) lo mismo con inversion", dict(invertir_en=T_ID // 2), VIVO1, False),
    'M': ("(M) 4 estimulos y 2 necesidades != v14 (DEBE fallar)", dict(),
          dict(vivo=1, n_nec=2, estims=('A', 'B', 'C', 'D'), costo=0.001, costo_a=0.001), True),
}

# ---------------------------------------------------------------- UMBRALES: la LETRA del preregistro (ERR-31)
UMBRALES = {
    'P1': dict(frase="xor01 de VIVO >= 0.75 en >= 15/20 semillas (mediana >= 0.875)",
               xor_min=0.75, n_min=15, mediana_min=0.875),
    'P2': dict(frase="xor01 de ESCALAR <= 0.60 y ESCALAR < VIVO en >= 16/20 (pareado)",
               xor_max=0.60, n_min=16),
    'P3a': dict(frase="nec_shuf=2 (contenido) -> xor01 <= 0.60 y por debajo de VIVO en >= 18/20",
                xor_max=0.60, n_min=18),
    'P3b': dict(frase="nec_shuf=1 (politica) -> muertes >= 2 x VIVO en >= 16/20; xor01 NO se predice que caiga",
                razon_min=2.0, n_min=16),
    'P4p': dict(frase="muertes de VIVO <= 0.75 x UNA_NEC y <= 0.70 x ESCALAR, pareado >= 16/20; y muertes por "
                      "agua de VIVO <= 0.5 x UNA_NEC",
                r_una=0.75, r_esc=0.70, r_agua=0.50, n_min=16),
    'P5': dict(frase="las 4 celdas informativas cruzan criterio en >= 18/20 (y terminan con el signo correcto, "
                     "Enmienda 1.3), con exp_tabla <= 3 x las exposiciones que v14 necesita para su celda mas "
                     "lenta (B)",
               n_min=18, factor=3.0, celda_v14='B'),
    'P6': dict(frase="NO_INFORMA: la sal nunca cruza criterio (censurada 20/20) y |W| <= 0.3 en las dos necesidades",
               w_max=0.3, n_min=20),
    'P7': dict(frase="muertes por agua de UNA_NEC >= 2 x las de VIVO, pareado >= 16/20 (Enmienda 1.4)",
               razon_min=2.0, n_min=16),
    'P9': dict(frase="VIVO <= 2 x UNA_NEC en exp_hasta[hambre][A], mediana de 20", factor=2.0),
    'P8': dict(frase="regresion del tronco (bateria_v14 6 + bateria_generaliza 20 --desde 101) intacta: NO la corre "
                     "este runner. El tronco no se toca: organismo_vivo es copia por anclas y su sha de origen se "
                     "verifica al arrancar."),
}

_log = {'f': None, 't0': time.time()}


def log(msg=""):
    linea = f"[{time.strftime('%H:%M:%S')} +{time.time()-_log['t0']:7.1f}s] {msg}"
    print(linea, flush=True)
    if _log['f']:
        _log['f'].write(linea + "\n"); _log['f'].flush(); os.fsync(_log['f'].fileno())


def N(x):
    return json.loads(json.dumps(x, default=str))


def h16(p):
    return hashlib.sha256(open(p, 'rb').read()).hexdigest()[:16]


def mediana(xs):
    xs = [x for x in xs if x is not None]
    return float(np.median(xs)) if xs else None


def razon(x, y):
    if x is None or y is None or y == 0:
        return None
    return round(x / y, 3)


def cuenta(a, b, semillas, f):
    """En cuantas semillas se cumple f(x_a, x_b). Un None NUNCA cuenta como victoria."""
    n = 0
    for s in semillas:
        x, y = a.get(s), b.get(s)
        if x is None or y is None:
            continue
        n += bool(f(x, y))
    return n


# ---------------------------------------------------------------- medidas propias del bloque
def objetivo(kw, nn, s):
    """El valor que la fisica del mundo obliga para la casilla (necesidad nn, estimulo s): +1 / -3 / 0.
    Se lee de la MISMA tabla que usa el organismo (EFECTO, o la del brazo si lo cambia): no se copia a mano."""
    import organismo_vivo as VV
    d = (kw.get('tabla') or VV.EFECTO)[VV.VAL_VIVO[s]][nn]
    return 1.0 if d > 0 else (-3.0 if d < 0 else 0.0)


def tabla_error(r, kw):
    """TABLA 2x4 APRENDIDA: error por casilla = |valor que leeria la boca - objetivo|. Con val_esc=1 la boca lee
    SIEMPRE la fila 0 (la necesidad es solo contexto), asi que la casilla se evalua con esa fila."""
    n = r['n_nec']
    fila = 0 if kw.get('val_esc') else None
    out, peor = {}, 0.0
    for nn in range(2):
        for s in MV.EST:
            if nn >= n:
                out[f'{nn}x{s}'] = None
                continue
            w = r['W_nec'][fila if fila is not None else nn][s]
            e = round(abs(w - objetivo(kw, nn, s)), 3)
            out[f'{nn}x{s}'] = e
            peor = max(peor, e)
    return out, round(peor, 3)


def celdas_estrictas(r, kw, o):
    """P5 con la Enmienda 1.3: una celda informativa cuenta SOLO si cruzo criterio Y ademas TERMINA con el signo
    correcto (en BARAJA_CON las cuatro cruzan y terminan en pure: la primera cruzada puede ser transitoria)."""
    n = r['n_nec']
    ok = 0
    det = {}
    for nn, s, sg in MV.INFORM:
        cr = o['exp_celda'][f'{nn}x{s}']
        fin = None if nn >= n else r['W_nec'][0 if kw.get('val_esc') else nn][s]
        bien = bool(cr is not None and fin is not None and fin * sg > 0 and abs(fin) >= 0.5)
        det[f'{nn}x{s}'] = dict(exposiciones=cr, valor_final=fin, cuenta=bien)
        ok += bien
    return ok, det


def resumen(brazo, seed, r, kw):
    o = MV.lee(r, kw)
    err, peor = tabla_error(r, kw)
    ok, det = celdas_estrictas(r, kw, o)
    return dict(tipo='R', brazo=brazo, seed=seed,
                xor01=o['xor01'], xor_celdas=o['xor_celdas'], tasa=o['tasa'], contraste=o['contraste'],
                exp_celda=o['exp_celda'], exp_tabla=o['exp_tabla'], celdas_ok=o['celdas_ok'],
                celdas_ok_estricto=ok, celdas_detalle=det,
                err_tabla=err, err_peor=peor,
                exposiciones=o['exposiciones'], W_nec=o['W_nec'],
                deaths=o['deaths'], muertes_nec=o['muertes_nec'],
                celdas=o['celdas'], splits=o['splits'], sorp_nec=r['sorp_nec'])


# ---------------------------------------------------------------- tareas (una por (brazo, semilla) o (caso, semilla))
def tarea(args):
    tipo = args[0]
    if tipo == 'ID':
        _, cual, seed, Ti = args
        import organismo_v14 as V14, organismo_vivo as VV
        etiq, kw14, kwvv, debe = CASOS_ID[cual]
        kw14 = {k: (Ti // 2 if k == 'invertir_en' else v) for k, v in kw14.items()}
        a = V14.run(seed, T=Ti, **kw14)
        b = VV.run(seed, T=Ti, **kw14, **kwvv)
        dif = [k for k in a if N(a[k]) != N({k2: v2 for k2, v2 in b.items() if k2 not in NUEVAS}.get(k))]
        falta = [k for k in a if k not in b]
        igual = not dif and not falta
        return dict(tipo='ID', cual=cual, etiqueta=etiq, seed=seed, identico=igual, debe_diferir=debe,
                    ok=bool(igual != debe), difieren=dif[:6], faltan=falta,
                    claves_nuevas=(sorted(set(b) - set(a)) if cual == 'I' else None))
    _, brazo, seed, Ti = args
    import organismo_vivo as VV
    kw = BRAZOS[brazo]
    return resumen(brazo, seed, VV.run(seed, T=Ti, **kw), kw)


SHAS = lambda: dict(
    preregistro=h16(os.path.join(AQUI, 'PREREGISTRO_mundo_vivo.md')),
    script=h16(os.path.abspath(__file__)),
    constructor=h16(os.path.join(AQUI, 'construye_vivo.py')),
    instrumento=h16(os.path.join(AQUI, 'organismo_vivo.py')),
    arnes=h16(os.path.join(AQUI, 'identidad_vivo.py')),
    mini=h16(os.path.join(AQUI, 'mini_vivo.py')),
    origen_organismo_v14=h16(os.path.join(RAIZ, 'organismo', 'organismo_v14.py')))


def guarda_origen():
    s = SHAS()['origen_organismo_v14']
    if s != SHA_V14_ESPERADO:
        log(f"*** ORIGEN CAMBIADO: organismo/organismo_v14.py es {s}, el instrumento se construyo desde "
            f"{SHA_V14_ESPERADO}. Reconstruir por anclas (construye_vivo.py) y repetir el arnes ANTES de correr.")
        return False
    return True


# ---------------------------------------------------------------- veredicto (umbrales EXACTOS del preregistro)
def veredicto(res, SEEDS, log=log):
    G = {b: {r['seed']: r for r in res if r['brazo'] == b} for b in BRAZOS_ACTIVOS}
    x = lambda b, c: {s: G[b][s][c] for s in G.get(b, {})}
    V = {'umbrales': UMBRALES}
    med = {}
    for b in BRAZOS_ACTIVOS:
        g = list(G[b].values())
        if not g:
            continue
        med[b] = dict(n=len(g), xor01=mediana([r['xor01'] for r in g]),
                      exp_tabla=mediana([r['exp_tabla'] for r in g]),
                      celdas_ok_estricto=mediana([r['celdas_ok_estricto'] for r in g]),
                      err_peor=mediana([r['err_peor'] for r in g]),
                      muertes=mediana([r['deaths'] for r in g]),
                      muertes_energia=mediana([r['muertes_nec'][0] for r in g]),
                      muertes_agua=mediana([r['muertes_nec'][1] for r in g]),
                      contraste=mediana([r['contraste'] for r in g]),
                      exposiciones={k: mediana([r['exposiciones'][k] for r in g]) for k in MV.EST},
                      exp_celda={k: mediana([r['exp_celda'][k] for r in g]) for k in g[0]['exp_celda']},
                      err_tabla={k: mediana([r['err_tabla'][k] for r in g]) for k in g[0]['err_tabla']})
        log(f"   {b:11s} n={med[b]['n']:<3d} xor01 {med[b]['xor01']}  celdas(estrictas) {med[b]['celdas_ok_estricto']}/4"
            f"  exp_tabla {med[b]['exp_tabla']}  peor error de casilla {med[b]['err_peor']}"
            f"  muertes {med[b]['muertes']} [E {med[b]['muertes_energia']}, agua {med[b]['muertes_agua']}]")
        log(f"        exposiciones hasta criterio por casilla {med[b]['exp_celda']}   exposiciones {med[b]['exposiciones']}")
        log(f"        error por casilla de la tabla 2x4 {med[b]['err_tabla']}")
    V['medianas'] = med
    hay = lambda *bs: all(b in med for b in bs)

    u = UMBRALES['P1']
    if hay('VIVO'):
        n = sum(r['xor01'] >= u['xor_min'] for r in G['VIVO'].values())
        V['P1'] = dict(n=n, mediana=med['VIVO']['xor01'],
                       pasa=bool(n >= u['n_min'] and med['VIVO']['xor01'] >= u['mediana_min']))
        log(f"   P1 {u['frase']}  ->  {n}/{len(SEEDS)}, mediana {med['VIVO']['xor01']}  {'PASA' if V['P1']['pasa'] else 'NO'}")

    u = UMBRALES['P2']
    if hay('VIVO', 'ESCALAR'):
        n = cuenta(x('ESCALAR', 'xor01'), x('VIVO', 'xor01'), SEEDS, lambda a, b: a < b)
        V['P2'] = dict(n=n, mediana=med['ESCALAR']['xor01'],
                       pasa=bool(med['ESCALAR']['xor01'] <= u['xor_max'] and n >= u['n_min']))
        log(f"   P2 {u['frase']}  ->  mediana {med['ESCALAR']['xor01']}, pareado {n}/{len(SEEDS)}  {'PASA' if V['P2']['pasa'] else 'NO'}")

    u = UMBRALES['P3a']
    if hay('VIVO', 'BARAJA_CON'):
        n = cuenta(x('BARAJA_CON', 'xor01'), x('VIVO', 'xor01'), SEEDS, lambda a, b: a < b)
        V['P3a'] = dict(n=n, mediana=med['BARAJA_CON']['xor01'],
                        pasa=bool(med['BARAJA_CON']['xor01'] <= u['xor_max'] and n >= u['n_min']))
        log(f"   P3a {u['frase']}  ->  mediana {med['BARAJA_CON']['xor01']}, pareado {n}/{len(SEEDS)}  {'PASA' if V['P3a']['pasa'] else 'NO'}")

    u = UMBRALES['P3b']
    if hay('VIVO', 'BARAJA_POL'):
        n = cuenta(x('BARAJA_POL', 'deaths'), x('VIVO', 'deaths'), SEEDS, lambda a, b: a >= u['razon_min'] * b)
        V['P3b'] = dict(n=n, razon=razon(med['BARAJA_POL']['muertes'], med['VIVO']['muertes']),
                        xor01=med['BARAJA_POL']['xor01'], pasa=bool(n >= u['n_min']))
        log(f"   P3b {u['frase']}  ->  razon {V['P3b']['razon']}, pareado {n}/{len(SEEDS)}, xor01 {V['P3b']['xor01']} "
            f"(sin criterio)  {'PASA' if V['P3b']['pasa'] else 'NO'}")

    u = UMBRALES['P4p']
    if hay('VIVO', 'UNA_NEC', 'ESCALAR'):
        n1 = cuenta(x('VIVO', 'deaths'), x('UNA_NEC', 'deaths'), SEEDS, lambda a, b: a <= u['r_una'] * b)
        n2 = cuenta(x('VIVO', 'deaths'), x('ESCALAR', 'deaths'), SEEDS, lambda a, b: a <= u['r_esc'] * b)
        ra = razon(med['VIVO']['muertes_agua'], med['UNA_NEC']['muertes_agua'])
        V['P4p'] = dict(n_una=n1, n_esc=n2, razon_una=razon(med['VIVO']['muertes'], med['UNA_NEC']['muertes']),
                        razon_esc=razon(med['VIVO']['muertes'], med['ESCALAR']['muertes']), razon_agua=ra,
                        pasa=bool(n1 >= u['n_min'] and n2 >= u['n_min'] and ra is not None and ra <= u['r_agua']))
        log(f"   P4' {u['frase']}  ->  razones {V['P4p']['razon_una']} / {V['P4p']['razon_esc']} / agua {ra}, "
            f"pareados {n1}/{n2} de {len(SEEDS)}  {'PASA' if V['P4p']['pasa'] else 'NO'}")

    u = UMBRALES['P5']
    if hay('VIVO', 'V14'):
        n = sum(r['celdas_ok_estricto'] == len(MV.INFORM) for r in G['VIVO'].values())
        ref_letra = med['V14']['exp_celda'].get(f"0x{u['celda_v14']}")
        cel14 = {k: v for k, v in med['V14']['exp_celda'].items() if v is not None}
        lenta = max(cel14, key=cel14.get) if cel14 else None
        ref_lenta = cel14.get(lenta)
        et = med['VIVO']['exp_tabla']
        V['P5'] = dict(n=n, exp_tabla=et, ref_letra=ref_letra, celda_letra=f"0x{u['celda_v14']}",
                       ref_mas_lenta=ref_lenta, celda_mas_lenta=lenta,
                       pasa_letra=bool(n >= u['n_min'] and et is not None and ref_letra is not None
                                       and et <= u['factor'] * ref_letra),
                       pasa_mas_lenta=bool(n >= u['n_min'] and et is not None and ref_lenta is not None
                                           and et <= u['factor'] * ref_lenta))
        V['P5']['nota'] = (
            "El preregistro dice 'su celda mas lenta (B)'. Si la celda mas lenta de V14 NO es B, la frase se "
            "contradice: se reportan LAS DOS lecturas sin elegir (ERR-31, la letra manda pero aqui la letra es "
            "ambigua) y la adjudicacion es del coordinador. NO se toca ningun umbral.")
        V['P5']['contradiccion'] = bool(lenta is not None and lenta != f"0x{u['celda_v14']}")
        log(f"   P5 {u['frase']}  ->  {n}/{len(SEEDS)} con 4/4 celdas estrictas, exp_tabla {et}")
        log(f"        letra   (celda 0x{u['celda_v14']} de V14 = {ref_letra}): umbral {None if ref_letra is None else u['factor']*ref_letra}"
            f"  {'PASA' if V['P5']['pasa_letra'] else 'NO'}")
        log(f"        'mas lenta' (celda {lenta} de V14 = {ref_lenta}): umbral {None if ref_lenta is None else u['factor']*ref_lenta}"
            f"  {'PASA' if V['P5']['pasa_mas_lenta'] else 'NO'}"
            + ("   *** CONTRADICCION EN LA LETRA: decide el coordinador" if V['P5']['contradiccion'] else ""))

    u = UMBRALES['P6']
    if hay('NO_INFORMA'):
        g = list(G['NO_INFORMA'].values())
        cens = sum(r['exp_celda']['1xD'] is None for r in g)
        wmax = max(max(abs(r['W_nec'][nn]['D']) for nn in range(len(r['W_nec']))) for r in g)
        V['P6'] = dict(censuradas=cens, w_max=round(float(wmax), 3),
                       pasa=bool(cens >= u['n_min'] and wmax <= u['w_max']))
        log(f"   P6 {u['frase']}  ->  censuradas {cens}/{len(SEEDS)}, |W| maximo {V['P6']['w_max']}  {'PASA' if V['P6']['pasa'] else 'NO'}")

    u = UMBRALES['P7']
    if hay('VIVO', 'UNA_NEC'):
        a = {s: G['UNA_NEC'][s]['muertes_nec'][1] for s in G['UNA_NEC']}
        b = {s: G['VIVO'][s]['muertes_nec'][1] for s in G['VIVO']}
        n = cuenta(a, b, SEEDS, lambda p, q: p >= u['razon_min'] * q)
        V['P7'] = dict(n=n, razon=razon(med['UNA_NEC']['muertes_agua'], med['VIVO']['muertes_agua']),
                       pasa=bool(n >= u['n_min']))
        log(f"   P7 {u['frase']}  ->  razon {V['P7']['razon']}, pareado {n}/{len(SEEDS)}  {'PASA' if V['P7']['pasa'] else 'NO'}")

    u = UMBRALES['P9']
    if hay('VIVO', 'UNA_NEC'):
        a, b = med['VIVO']['exp_celda']['0xA'], med['UNA_NEC']['exp_celda']['0xA']
        V['P9'] = dict(vivo=a, una_nec=b, razon=razon(a, b),
                       pasa=bool(a is not None and b is not None and a <= u['factor'] * b))
        log(f"   P9 {u['frase']}  ->  {a} contra {b} (razon {V['P9']['razon']})  {'PASA' if V['P9']['pasa'] else 'NO'}")

    V['P8'] = dict(frase=UMBRALES['P8']['frase'], corrida=False)
    log(f"   P8 {UMBRALES['P8']['frase']}")
    return V


def frase_final(V):
    """El veredicto en el vocabulario del preregistro. Nada de 'entiende', 'propósito' ni 'planifica'."""
    p = {k: (V.get(k) or {}).get('pasa') for k in ('P1', 'P2', 'P3a', 'P4p', 'P6', 'P7', 'P9')}
    p5 = (V.get('P5') or {})
    nucleo = bool(p['P1'] and p['P2'] and p['P3a'])
    if not nucleo:
        return ("MUNDO VIVO REFUTADO como esta escrito: " +
                ("el valor por necesidad no da el XOR necesidad x estimulo (P1). " if not p['P1'] else "") +
                ("el valor ESCALAR no queda por debajo: el valor NO tiene por que ser por necesidad (P2). " if not p['P2'] else "") +
                ("barajar el CONTENIDO no lo destruye: lo que produce la tabla no es la necesidad (P3a). " if not p['P3a'] else "") +
                "Se registra el fallo y no se declara nada.")
    s = ("MUNDO VIVO SOSTENIDO en su nucleo: el organismo aprende un VALOR POR NECESIDAD que resuelve el XOR "
         "necesidad x estimulo (P1), un valor escalar no lo hace (P2) y barajar el contenido lo destruye (P3a). ")
    s += ("Paga en supervivencia con dos muertes posibles (P4', P7). " if (p['P4p'] and p['P7']) else
          "La ventaja en supervivencia NO se sostiene con la letra (P4'/P7): el valor se aprende y el cuerpo no lo cobra. ")
    s += ("El estimulo que no informa no se aprende (P6). " if p['P6'] else "AVISO: el estimulo que no informa recibe valor (P6 cae): buscar la fuga antes de seguir. ")
    s += ("El coste en exposiciones de la segunda necesidad se mantiene (P9). " if p['P9'] else "El coste en exposiciones de la segunda necesidad crece por encima de lo previsto (P9 cae). ")
    if p5.get('contradiccion'):
        s += ("P5 queda ADJUDICADO AL COORDINADOR: la frase del preregistro nombra la celda B como la mas lenta de "
              f"v14 y no lo es ({p5.get('celda_mas_lenta')}); letra {'PASA' if p5.get('pasa_letra') else 'NO'}, "
              f"'mas lenta' {'PASA' if p5.get('pasa_mas_lenta') else 'NO'}. ")
    else:
        s += ("La tabla 2x4 se completa dentro del presupuesto de exposiciones (P5). " if p5.get('pasa_letra') else
              "La tabla 2x4 cuesta mas exposiciones de las previstas (P5 cae). ")
    return s + "20 semillas no cierran un nivel: piden replica en el rango siguiente (regla 12)."


# ---------------------------------------------------------------- humo (UN proceso, sin Pool, regla 3)
def humo():
    stamp = time.strftime('%Y%m%d_%H%M%S')
    _log['f'] = open(os.path.join(RAIZ, 'datos', f'vivo_humo_{stamp}.log'), 'w', encoding='utf-8', newline='\n')
    log("HUMO del disenador, UN proceso, sin Pool (regla 3). PREREGISTRO_mundo_vivo.md.")
    log("Semillas 1-2 (las de la mini-prueba): NINGUNA de las 181-200 del bloque queda expuesta.")
    for k, v in SHAS().items():
        log(f"    sha {k:22s} {v}")
    log(f"    origen organismo_v14 esperado {SHA_V14_ESPERADO} -> {'OK' if guarda_origen() else 'FALLA'}")
    Ti, Tb, sem = 5000, 20000, [1, 2]
    log(f"1/2 IDENTIDAD, {len(CASOS_ID)} casos x {len(sem)} semillas, T={Ti}.")
    ident = []
    for cual in CASOS_ID:
        for s in sem:
            r = tarea(('ID', cual, s, Ti)); ident.append(r)
        g = [r for r in ident if r['cual'] == cual]
        log(f"    {CASOS_ID[cual][0]:52s} {sum(r['ok'] for r in g)}/{len(g)}"
            + ("" if all(r['ok'] for r in g) else f"   difieren {g[0]['difieren']}"))
    log(f"  IDENTIDAD {sum(r['ok'] for r in ident)}/{len(ident)}")
    log(f"2/2 UNA corrida por brazo, T={Tb}, semilla 1 ({len(BRAZOS_ACTIVOS)} corridas).")
    res, t_b = [], {}
    for b in BRAZOS_ACTIVOS:
        t1 = time.time(); r = tarea(('R', b, 1, Tb)); t_b[b] = round(time.time() - t1, 2); res.append(r)
        log(f"    {b:11s} {t_b[b]:5.2f} s  xor01 {r['xor01']}  celdas(estrictas) {r['celdas_ok_estricto']}/4"
            f"  exp_tabla {r['exp_tabla']}  peor error {r['err_peor']}  muertes {r['deaths']} {r['muertes_nec']}")
        log(f"                exp por casilla {r['exp_celda']}   error por casilla {r['err_tabla']}")
    seg = sum(t_b.values()) / max(len(t_b), 1) * (T / Tb)
    log(f"ESTIMACION del bloque: {len(BRAZOS_ACTIVOS)}x{N_SEM} = {len(BRAZOS_ACTIVOS)*N_SEM} corridas de {T} pasos, "
        f"~{seg:.1f} s/corrida en serie -> ~{len(BRAZOS_ACTIVOS)*N_SEM*seg/N_PARALELO/60:.1f} min de pared con Pool({N_PARALELO}) "
        f"(+ identidad: {len(CASOS_ID)*len(SEMILLAS_ID)} comprobaciones de 2 x {T_ID} pasos).")
    log("HUMO: numeros observados, sin ajustar nada. n=1, T corto y semilla vista: NO son evidencia.")
    dj = os.path.join(RAIZ, 'datos', f'vivo_humo_{stamp}.json')
    json.dump(dict(meta=dict(fecha=time.strftime('%Y-%m-%dT%H:%M:%S'), tipo='humo', T_identidad=Ti, T_brazo=Tb,
                             semillas=sem, T_bloque=T, umbrales=UMBRALES, shas=SHAS(),
                             segundos_por_brazo=t_b, python=platform.python_version(), numpy=np.__version__),
                   identidades=ident, brazos=res), open(dj, 'w', encoding='utf-8'), ensure_ascii=False, default=str)
    log(f"datos -> {os.path.basename(dj)}  sha256_16 = {h16(dj)}")
    _log['f'].close()


# ---------------------------------------------------------------- principal
if __name__ == '__main__':
    if '--humo' in sys.argv:
        humo(); sys.exit(0)

    import multiprocessing as mp
    mp.set_start_method('spawn', force=True)
    desde = int(sys.argv[sys.argv.index('--desde') + 1]) if '--desde' in sys.argv else DESDE
    if '--T' in sys.argv:
        T = int(sys.argv[sys.argv.index('--T') + 1])
    if '--brazos' in sys.argv:
        BRAZOS_ACTIVOS = [b.strip() for b in sys.argv[sys.argv.index('--brazos') + 1].split(',') if b.strip()]
        malos = [b for b in BRAZOS_ACTIVOS if b not in BRAZOS]
        if malos:
            raise SystemExit(f"--brazos: brazo(s) desconocido(s) {malos}. Validos: {ORDEN}")
        for req in ('VIVO', 'V14'):
            if req not in BRAZOS_ACTIVOS:
                raise SystemExit(f"--brazos: {req} es referencia obligatoria (P1/P5 la necesitan).")
    SEEDS = list(range(desde, desde + N_SEM))
    stamp = time.strftime('%Y%m%d_%H%M%S')
    _log['f'] = open(os.path.join(RAIZ, 'datos', f'vivo_s{SEEDS[0]}-{SEEDS[-1]}_{stamp}.log'),
                     'w', encoding='utf-8', newline='\n')
    log(f"ARRANQUE MUNDO VIVO (nivel 11): brazos {BRAZOS_ACTIVOS}, semillas {SEEDS[0]}-{SEEDS[-1]}, T={T}. Pool({N_PARALELO}).")
    log("20 semillas no cierran un nivel del brief: cierran o refutan ESTE mecanismo, y piden replica en 201-220.")
    for k, v in SHAS().items():
        log(f"    sha {k:22s} {v}")
    if not guarda_origen():
        sys.exit(1)
    try:
        ps = subprocess.run(['powershell', '-NoProfile', '-Command',
                             "Get-CimInstance Win32_Process | Where-Object { $_.Name -like 'python*' } | ForEach-Object { \"$($_.ProcessId) $($_.CommandLine)\" }"],
                            capture_output=True, text=True, timeout=60).stdout.strip().splitlines()
    except Exception as e:
        ps = [f"(no se pudo listar: {e})"]
    log(f"REGLA 11 — procesos python vivos ({len(ps)}), este es pid {os.getpid()}")

    V, res = {}, []
    with mp.Pool(N_PARALELO) as pool:
        ctrl = [('ID', c, s, T_ID) for c in CASOS_ID for s in SEMILLAS_ID]
        log(f"ETAPA 1/2 — IDENTIDAD interna ({len(CASOS_ID)} casos x {len(SEMILLAS_ID)} semillas = {len(ctrl)} "
            f"comprobaciones de 2 x {T_ID} pasos). El caso (M) DEBE fallar: sin el, la etapa pasa por vacuidad.")
        rc = pool.map(tarea, ctrl, chunksize=1)
        for cual in CASOS_ID:
            g = [r for r in rc if r['cual'] == cual]
            log(f"    {CASOS_ID[cual][0]:52s} {sum(r['ok'] for r in g)}/{len(g)}"
                + ("" if all(r['ok'] for r in g) else f"   difieren {g[0]['difieren']} faltan {g[0]['faltan']}"))
            V[f'ID_{cual}'] = all(r['ok'] for r in g)
        V['G_IDENTIDAD'] = bool(all(V[f'ID_{c}'] for c in CASOS_ID))
        cn = next((r['claves_nuevas'] for r in rc if r['cual'] == 'I' and r['claves_nuevas']), None)
        log(f"    claves nuevas de solo lectura con vivo=1: {cn}")
        log(f"  IDENTIDAD {sum(r['ok'] for r in rc)}/{len(rc)}")
        if not V['G_IDENTIDAD']:
            log("*** GUARDA DE IDENTIDAD FALLIDA: el mundo vivo no es organismo_v14 con una necesidad y dos "
                "estimulos (o el control que debe fallar no falla). Se para.")
            sys.exit(1)

        tr = [('R', b, s, T) for b in BRAZOS_ACTIVOS for s in SEEDS]
        log(f"ETAPA 2/2 — principal: {len(tr)} corridas de {T} pasos ({len(BRAZOS_ACTIVOS)} brazos x {len(SEEDS)} semillas)...")
        for i, r in enumerate(pool.imap_unordered(tarea, tr, chunksize=1), 1):
            res.append(r)
            if i % 20 == 0 or i == len(tr):
                log(f"          {i}/{len(tr)}")

    log()
    log("ANALISIS — medianas por brazo y despues los umbrales EXACTOS del preregistro (ERR-31).")
    V.update(veredicto(res, SEEDS))
    ver = frase_final(V)
    log(); log(f"VEREDICTO: {ver}")

    meta = dict(fecha=time.strftime('%Y-%m-%dT%H:%M:%S'), semillas=SEEDS, T=T,
                brazos={b: {k: (list(v) if isinstance(v, tuple) else v) for k, v in BRAZOS[b].items()}
                        for b in BRAZOS_ACTIVOS},
                veredicto=ver, veredictos=V, identidades=rc, procesos_python=ps, shas=SHAS(),
                origen_organismo_v14_esperado=SHA_V14_ESPERADO,
                python=platform.python_version(), numpy=np.__version__)
    dj = os.path.join(RAIZ, 'datos', f'vivo_s{SEEDS[0]}-{SEEDS[-1]}_{stamp}.json')
    json.dump(dict(meta=meta, principal=res), open(dj, 'w', encoding='utf-8'), ensure_ascii=False, default=str)
    log(f"datos -> {os.path.basename(dj)}  sha256_16 = {h16(dj)}")
    _log['f'].close()
