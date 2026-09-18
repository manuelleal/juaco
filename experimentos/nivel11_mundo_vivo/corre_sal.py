"""LA SUPERSTICION DE LA SAL (nivel 4) — ejecuta PREREGISTRO_supersticion_sal.md.
No es un bloque del mundo vivo: mide una grieta del TRONCO v14.1 que el mundo vivo destapo. Con dos estimulos,
`cond()` PROHIBE el alias de codigo por construccion (`code(A) & code(B) = 0`); con cuatro no lo prohibe nadie, y
en 2.5 % de las semillas la sal y el veneno acaban con el MISMO codigo.
REGLA 10: log desde el arranque, con fsync, una linea por etapa con marca de tiempo.

    python experimentos/nivel11_mundo_vivo/corre_sal.py [--T 100000]
    python experimentos/nivel11_mundo_vivo/corre_sal.py --humo    (UN proceso, sin Pool: lo corre el disenador)

SEMILLAS SELECCIONADAS ANTES DE CORRER por una propiedad del CODIGO, no de un resultado (`diagnostico_codigos.py`
construye KW y lee los codigos, sin simular un paso). El runner las RECALCULA al arrancar y aborta si no coinciden
con la lista del preregistro: asi la seleccion no puede volverse circular.
    ALIAS   (|code(D) & code(B)| = 3): 326, 334, 343, 377, 446, 533, 549, 563, 670
    LIMPIAS (|code(D) & code(B)| = 0): 307, 313, 316, 323, 325, 327, 333, 338, 342
Rango 301-700, virgen: 181-200 y 201-220 ya se gastaron en el mundo vivo.

Etapas con Pool (las corre el COORDINADOR, reglas 3 y 11):
  1/2 IDENTIDAD interna: los 5 casos de identidad_vivo.py (importados de corre_vivo.py, sin copiar) x 3 semillas,
      incluido el caso (M) que DEBE fallar. Si no es 15/15, ABORTA.
  2/2 principal: 4 brazos x 9 semillas (36 corridas). Todos con la sal MUDA (tabla con sal -> (0,0)).

Brazos (un cambio por brazo, sobre el NO_INFORMA del mundo vivo):
  S1-ALIAS    semillas ALIAS, sin tocar nada        -> ¿aparece el valor espurio?
  S1-LIMPIA   semillas LIMPIAS, sin tocar nada      -> control: no debe aparecer
  S2-SIN-SED  ALIAS + n_nec=1 (no existe la sed)    -> la hipotesis del COORDINADOR; si la supersticion desaparece,
                                                       la explicacion por codigo cae y gana la de co-ocurrencia
  S3-PUERTA   ALIAS + puerta_pat=0 (puerta de v13)  -> aisla "la puerta presta la evidencia por codigo"

Vocabulario (regla 6): "alias de codigo", "valor espurio", "evitacion". NO se dice "cree", "superstición" como
propiedad del organismo ni "sabe": el titulo es una etiqueta del fenomeno, no una declaracion.
"""
import sys, os, json, time, hashlib, platform, subprocess, statistics as st
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
import numpy as np

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
sys.path[:0] = [AQUI, os.path.join(RAIZ, 'organismo')]   # organismo/ PRIMERO (ERR-28)

import mini_vivo as MV
import corre_vivo as CV          # identidad (CASOS_ID, NUEVAS, T_ID) y la guarda de origen: NO se copian
import diagnostico_codigos as DC

T = 100000
T_ID = CV.T_ID
N_PARALELO = 14
SEMILLAS_ID = CV.SEMILLAS_ID
ALIAS = [326, 334, 343, 377, 446, 533, 549, 563, 670]
LIMPIAS = [307, 313, 316, 323, 325, 327, 333, 338, 342]
SAL_MUDA = MV.SAL_MUDA
BASE = dict(MV.BRAZOS['NO_INFORMA'])          # vivo=1, n_nec=2, 4 estimulos, costo=costo_a=0.001, sal muda
BRAZOS = {
    'S1-ALIAS':   (dict(BASE), ALIAS),
    'S1-LIMPIA':  (dict(BASE), LIMPIAS),
    'S2-SIN-SED': (dict(BASE, n_nec=1), ALIAS),
    'S3-PUERTA':  (dict(BASE, puerta_pat=0), ALIAS),
}
ORDEN = list(BRAZOS)

# ---------------------------------------------------------------- UMBRALES: la LETRA del preregistro (ERR-31)
UMBRALES = {
    'S1': dict(frase="S1-ALIAS: |W[sal]| > 0.3 en >= 8/9 (mediana >= 1.0). S1-LIMPIA: |W[sal]| <= 0.3 en 9/9 (mediana 0.0)",
               w=0.3, n_alias=8, med_alias=1.0, n_limpia=9),
    'S2': dict(frase="el veneno paga: W[veneno] >= -2.3 en >= 8/9 ALIAS y <= -2.8 en 9/9 LIMPIAS",
               w_alias=-2.3, n_alias=8, w_limpia=-2.8, n_limpia=9),
    'S3': dict(frase="evitacion: exposiciones a la sal >= 3 x la mediana de las LIMPIAS, en >= 8/9 ALIAS",
               factor=3.0, n_min=8),
    'S4': dict(frase="divisiones = 0 en >= 8/9 ALIAS con la sal muda", n_min=8),
    'S5': dict(frase="S2-SIN-SED ~ S1-ALIAS: |W[sal]| dentro de +-0.3 de S1-ALIAS, en >= 7/9",
               tol=0.3, n_min=7),
    'S6': dict(frase="S3-PUERTA: |W[sal]| baja al menos 50 % respecto de S1-ALIAS en >= 7/9 (no se predice 0)",
               baja=0.5, n_min=7),
}

_log = {'f': None, 't0': time.time()}


def log(msg=""):
    linea = f"[{time.strftime('%H:%M:%S')} +{time.time()-_log['t0']:7.1f}s] {msg}"
    print(linea, flush=True)
    if _log['f']:
        _log['f'].write(linea + "\n"); _log['f'].flush(); os.fsync(_log['f'].fileno())


def h16(p):
    return hashlib.sha256(open(p, 'rb').read()).hexdigest()[:16]


def med(xs):
    xs = [x for x in xs if x is not None]
    return round(float(np.median(xs)), 3) if xs else None


def resumen(brazo, seed, r):
    """Las cuatro cantidades del preregistro. |W[sal]| es el maximo sobre las necesidades QUE EXISTEN en el brazo
    (S2-SIN-SED solo tiene una fila): es la lectura que la boca podria usar."""
    W = r['W_nec']
    return dict(tipo='R', brazo=brazo, seed=seed,
                w_sal=round(max(abs(W[n]['D']) for n in range(len(W))), 3),
                w_sal_por_nec=[round(W[n]['D'], 3) for n in range(len(W))],
                w_veneno=round(W[0]['B'], 3),
                w_veneno_por_nec=[round(W[n]['B'], 3) for n in range(len(W))],
                exp_sal=r['exposiciones']['D'], exp_veneno=r['exposiciones']['B'],
                exposiciones=r['exposiciones'], splits=r['splits'], celdas=r['celdas'],
                deaths=r['deaths'], muertes_nec=r['muertes_nec'], W_nec=W,
                exp_hasta=r['exp_hasta'],   # crudo del instrumento: la sal muda debe salir censurada (None) en todas
                sal_censurada=all(f['D'] is None for f in r['exp_hasta']))


def tarea(args):
    if args[0] == 'ID':
        return CV.tarea(args)
    _, brazo, seed, Ti = args
    import organismo_vivo as VV
    return resumen(brazo, seed, VV.run(seed, T=Ti, **BRAZOS[brazo][0]))


SHAS = lambda: dict(
    preregistro=h16(os.path.join(AQUI, 'PREREGISTRO_supersticion_sal.md')),
    script=h16(os.path.abspath(__file__)),
    runner_mundo_vivo=h16(os.path.join(AQUI, 'corre_vivo.py')),
    diagnostico=h16(os.path.join(AQUI, 'diagnostico_codigos.py')),
    constructor=h16(os.path.join(AQUI, 'construye_vivo.py')),
    instrumento=h16(os.path.join(AQUI, 'organismo_vivo.py')),
    origen_organismo_v14=h16(os.path.join(RAIZ, 'organismo', 'organismo_v14.py')))


def guarda_semillas():
    """La seleccion se RECALCULA aqui: si el tronco o el diagnostico cambiaran, las listas del preregistro dejarian
    de ser las correctas y el bloque no puede correr con ellas."""
    a = [s for s in range(301, 701) if DC.solapamientos(s)['D&B'] >= 3]
    ok_a = (a == ALIAS)
    ok_l = all(DC.solapamientos(s)['D&B'] == 0 for s in LIMPIAS)
    log(f"    ALIAS recalculadas en 301-700: {a}  -> {'coinciden con el preregistro' if ok_a else '*** NO COINCIDEN'}")
    log(f"    LIMPIAS del preregistro con |D&B| = 0: {'9/9' if ok_l else '*** alguna no es limpia'}")
    return ok_a and ok_l


# ---------------------------------------------------------------- veredicto (umbrales EXACTOS del preregistro)
def veredicto(res, log=log):
    G = {b: {r['seed']: r for r in res if r['brazo'] == b} for b in ORDEN}
    V = {'umbrales': UMBRALES}
    for b in ORDEN:
        g = [G[b][s] for s in sorted(G[b])]
        if not g:
            continue
        log(f"   {b:11s} n={len(g)}  |W[sal]| med {med([r['w_sal'] for r in g])}  W[veneno] med {med([r['w_veneno'] for r in g])}"
            f"  exposiciones sal med {med([r['exp_sal'] for r in g])}  divisiones med {med([r['splits'] for r in g])}"
            f"  muertes med {med([r['deaths'] for r in g])}")
        log(f"        |W[sal]| por semilla {[r['w_sal'] for r in g]}")
        log(f"        W[veneno] por semilla {[r['w_veneno'] for r in g]}")
    A = G.get('S1-ALIAS', {}); L = G.get('S1-LIMPIA', {}); Z = G.get('S2-SIN-SED', {}); P = G.get('S3-PUERTA', {})
    hay = lambda *ds: all(d for d in ds)

    u = UMBRALES['S1']
    if hay(A, L):
        na = sum(r['w_sal'] > u['w'] for r in A.values()); nl = sum(r['w_sal'] <= u['w'] for r in L.values())
        ma, ml = med([r['w_sal'] for r in A.values()]), med([r['w_sal'] for r in L.values()])
        V['S1'] = dict(n_alias=na, med_alias=ma, n_limpia=nl, med_limpia=ml,
                       pasa=bool(na >= u['n_alias'] and ma is not None and ma >= u['med_alias'] and nl >= u['n_limpia']))
        log(f"   S-1 {u['frase']}")
        log(f"       ALIAS {na}/{len(A)} (mediana {ma})   LIMPIA {nl}/{len(L)} (mediana {ml})   -> {'PASA' if V['S1']['pasa'] else 'NO'}")

    u = UMBRALES['S2']
    if hay(A, L):
        na = sum(r['w_veneno'] >= u['w_alias'] for r in A.values())
        nl = sum(r['w_veneno'] <= u['w_limpia'] for r in L.values())
        V['S2'] = dict(n_alias=na, med_alias=med([r['w_veneno'] for r in A.values()]),
                       n_limpia=nl, med_limpia=med([r['w_veneno'] for r in L.values()]),
                       pasa=bool(na >= u['n_alias'] and nl >= u['n_limpia']))
        log(f"   S-2 {u['frase']}")
        log(f"       ALIAS {na}/{len(A)} (mediana {V['S2']['med_alias']})   LIMPIA {nl}/{len(L)} "
            f"(mediana {V['S2']['med_limpia']})   -> {'PASA' if V['S2']['pasa'] else 'NO'}")

    u = UMBRALES['S3']
    if hay(A, L):
        ref = med([r['exp_sal'] for r in L.values()])
        n = sum(r['exp_sal'] >= u['factor'] * ref for r in A.values()) if ref else 0
        V['S3'] = dict(n=n, ref_limpias=ref, med_alias=med([r['exp_sal'] for r in A.values()]),
                       pasa=bool(ref and n >= u['n_min']))
        log(f"   S-3 {u['frase']}")
        log(f"       mediana LIMPIAS {ref} -> umbral {None if not ref else round(u['factor']*ref,1)};"
            f" ALIAS mediana {V['S3']['med_alias']}, {n}/{len(A)}   -> {'PASA' if V['S3']['pasa'] else 'NO'}")

    u = UMBRALES['S4']
    if A:
        n = sum(r['splits'] == 0 for r in A.values())
        V['S4'] = dict(n=n, splits=[r['splits'] for r in sorted(A.values(), key=lambda r: r['seed'])],
                       pasa=bool(n >= u['n_min']))
        log(f"   S-4 {u['frase']}  ->  {n}/{len(A)}   -> {'PASA' if V['S4']['pasa'] else 'NO'}")

    u = UMBRALES['S5']
    if hay(A, Z):
        # pareado por semilla: aqui SI es legitimo (ERR-37b) porque la medida es lo que se APRENDIO sobre una
        # imagen, no una integral de la trayectoria, y la semilla fija los codigos.
        d = {s: abs(Z[s]['w_sal'] - A[s]['w_sal']) for s in A if s in Z}
        n = sum(v <= u['tol'] for v in d.values())
        V['S5'] = dict(n=n, difs={str(k): round(v, 3) for k, v in d.items()},
                       med_sin_sed=med([r['w_sal'] for r in Z.values()]), pasa=bool(n >= u['n_min']))
        log(f"   S-5 {u['frase']}")
        log(f"       |W[sal]| sin sed mediana {V['S5']['med_sin_sed']} contra ALIAS {med([r['w_sal'] for r in A.values()])};"
            f" dentro de +-{u['tol']} en {n}/{len(d)}   -> {'PASA' if V['S5']['pasa'] else 'NO'}")
        log(f"       si esto NO pasa, gana la explicacion por co-ocurrencia con la necesidad y la del codigo cae")

    u = UMBRALES['S6']
    if hay(A, P):
        n = sum(P[s]['w_sal'] <= u['baja'] * A[s]['w_sal'] for s in A if s in P)
        V['S6'] = dict(n=n, med_puerta=med([r['w_sal'] for r in P.values()]), pasa=bool(n >= u['n_min']))
        log(f"   S-6 {u['frase']}")
        log(f"       |W[sal]| con puerta de v13 mediana {V['S6']['med_puerta']} contra ALIAS "
            f"{med([r['w_sal'] for r in A.values()])}; baja >= 50 % en {n}/{len(A)}   -> {'PASA' if V['S6']['pasa'] else 'NO'}")
    return V


def frase_final(V):
    """El vocabulario del preregistro: alias de codigo, valor espurio, evitacion. Nada mas."""
    s1 = (V.get('S1') or {}).get('pasa'); s5 = (V.get('S5') or {}).get('pasa')
    if not s1:
        return ("EXPLICACION POR ALIAS DE CODIGO REFUTADA: el valor espurio de la sal no sigue a "
                "|code(D) & code(B)|. La causa es otra y el bloque no dice cual. Se registra el fallo.")
    s = ("ALIAS DE CODIGO CONFIRMADO: el valor espurio de un estimulo que no informa aparece cuando su codigo "
         "coincide con el de un estimulo con valor consolidado, y no aparece cuando no coincide. ")
    s += ("El veneno paga el precio (S-2). " if (V.get('S2') or {}).get('pasa') else "El veneno NO se degrada (S-2 cae): el valor espurio no sale de su celda. ")
    s += ("La evitacion acumula el estimulo en el mundo (S-3). " if (V.get('S3') or {}).get('pasa') else "No hay acumulacion por evitacion (S-3 cae). ")
    s += ("La division por conflicto de signo no se dispara con R = 0 (S-4). " if (V.get('S4') or {}).get('pasa') else "La division SI se dispara con R = 0 (S-4 cae): revisar la lectura del codigo. ")
    s += ("Quitar la sed no lo cambia: NO es co-ocurrencia con la necesidad (S-5). " if s5 else
          "*** Quitar la sed LO CAMBIA: gana la explicacion por co-ocurrencia con la necesidad activa y la del codigo queda incompleta (S-5). ")
    s += ("La puerta por evidencia de codigo es parte del bucle (S-6). " if (V.get('S6') or {}).get('pasa') else "La puerta no es parte del bucle: basta el alias (S-6). ")
    return s + "9 semillas por brazo no cierran nada: piden replica con las ALIAS del rango siguiente."


# ---------------------------------------------------------------- humo (UN proceso, sin Pool, regla 3)
def humo():
    stamp = time.strftime('%Y%m%d_%H%M%S')
    _log['f'] = open(os.path.join(RAIZ, 'datos', f'sal_humo_{stamp}.log'), 'w', encoding='utf-8', newline='\n')
    log("HUMO del disenador, UN proceso, sin Pool (regla 3). PREREGISTRO_supersticion_sal.md.")
    log("Semillas 182 (ALIAS) y 181 (LIMPIA): las dos YA se gastaron en el mundo vivo. NINGUNA de 301-700 queda expuesta.")
    for k, v in SHAS().items():
        log(f"    sha {k:22s} {v}")
    log(f"    origen organismo_v14 -> {'OK' if CV.guarda_origen() else 'FALLA'}")
    log("1/3 seleccion de semillas (diagnostico estructural, sin correr el organismo)")
    ok = guarda_semillas()
    Ti, Tb = 5000, 20000
    log(f"2/3 IDENTIDAD, {len(CV.CASOS_ID)} casos x 1 semilla, T={Ti}.")
    ident = []
    for cual in CV.CASOS_ID:
        r = tarea(('ID', cual, 1, Ti)); ident.append(r)
        log(f"    {CV.CASOS_ID[cual][0]:52s} {'OK' if r['ok'] else 'FALLA ' + str(r['difieren'])}")
    log(f"  IDENTIDAD {sum(r['ok'] for r in ident)}/{len(ident)}")
    log(f"3/3 UNA corrida por brazo con las semillas del humo, T={Tb} (4 corridas).")
    res, t_b = [], {}
    for b, s in (('S1-ALIAS', 182), ('S1-LIMPIA', 181), ('S2-SIN-SED', 182), ('S3-PUERTA', 182)):
        t1 = time.time(); r = tarea(('R', b, s, Tb)); t_b[b] = round(time.time() - t1, 2); res.append(r)
        log(f"    {b:11s} s{s}  {t_b[b]:5.2f} s  |W[sal]| {r['w_sal']} {r['w_sal_por_nec']}  W[veneno] {r['w_veneno']}"
            f"  exposiciones sal {r['exp_sal']} (veneno {r['exp_veneno']})  divisiones {r['splits']}  muertes {r['deaths']}")
    seg = sum(t_b.values()) / max(len(t_b), 1) * (T / Tb)
    n = sum(len(v[1]) for v in BRAZOS.values())
    log(f"ESTIMACION del bloque: {n} corridas de {T} pasos, ~{seg:.1f} s/corrida en serie -> "
        f"~{n*seg/N_PARALELO/60:.1f} min de pared con Pool({N_PARALELO}) (+ identidad: {len(CV.CASOS_ID)*len(SEMILLAS_ID)} comprobaciones).")
    log("HUMO: T corto y n=1 por brazo; las dos semillas ya estaban vistas. NO son evidencia: prueban que mide.")
    dj = os.path.join(RAIZ, 'datos', f'sal_humo_{stamp}.json')
    json.dump(dict(meta=dict(fecha=time.strftime('%Y-%m-%dT%H:%M:%S'), tipo='humo', T_identidad=Ti, T_brazo=Tb,
                             T_bloque=T, alias=ALIAS, limpias=LIMPIAS, semillas_ok=ok, umbrales=UMBRALES,
                             shas=SHAS(), segundos_por_brazo=t_b, python=platform.python_version(),
                             numpy=np.__version__),
                   identidades=ident, brazos=res), open(dj, 'w', encoding='utf-8'), ensure_ascii=False, default=str)
    log(f"datos -> {os.path.basename(dj)}  sha256_16 = {h16(dj)}")
    _log['f'].close()


# ---------------------------------------------------------------- principal
if __name__ == '__main__':
    if '--humo' in sys.argv:
        humo(); sys.exit(0)

    import multiprocessing as mp
    mp.set_start_method('spawn', force=True)
    if '--T' in sys.argv:
        T = int(sys.argv[sys.argv.index('--T') + 1])
    stamp = time.strftime('%Y%m%d_%H%M%S')
    _log['f'] = open(os.path.join(RAIZ, 'datos', f'sal_alias{len(ALIAS)}_{stamp}.log'), 'w', encoding='utf-8', newline='\n')
    log(f"ARRANQUE SUPERSTICION DE LA SAL (nivel 4): brazos {ORDEN}, ALIAS {ALIAS}, LIMPIAS {LIMPIAS}, T={T}. Pool({N_PARALELO}).")
    log("9 semillas por brazo no cierran nada: confirman o refutan ESTA explicacion, y piden replica.")
    for k, v in SHAS().items():
        log(f"    sha {k:22s} {v}")
    if not CV.guarda_origen():
        sys.exit(1)
    log("SELECCION DE SEMILLAS (se recalcula: si no coincide con el preregistro, se para)")
    if not guarda_semillas():
        log("*** La seleccion de semillas del preregistro no se reproduce. Se para.")
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
        ctrl = [('ID', c, s, T_ID) for c in CV.CASOS_ID for s in SEMILLAS_ID]
        log(f"ETAPA 1/2 — IDENTIDAD interna ({len(ctrl)} comprobaciones de 2 x {T_ID} pasos; el caso (M) DEBE fallar).")
        rc = pool.map(tarea, ctrl, chunksize=1)
        for cual in CV.CASOS_ID:
            g = [r for r in rc if r['cual'] == cual]
            log(f"    {CV.CASOS_ID[cual][0]:52s} {sum(r['ok'] for r in g)}/{len(g)}"
                + ("" if all(r['ok'] for r in g) else f"   difieren {g[0]['difieren']}"))
            V[f'ID_{cual}'] = all(r['ok'] for r in g)
        V['G_IDENTIDAD'] = bool(all(V[f'ID_{c}'] for c in CV.CASOS_ID))
        log(f"  IDENTIDAD {sum(r['ok'] for r in rc)}/{len(rc)}")
        if not V['G_IDENTIDAD']:
            log("*** GUARDA DE IDENTIDAD FALLIDA. Se para.")
            sys.exit(1)

        tr = [('R', b, s, T) for b, (_, ss) in BRAZOS.items() for s in ss]
        log(f"ETAPA 2/2 — principal: {len(tr)} corridas de {T} pasos ({len(BRAZOS)} brazos).")
        for i, r in enumerate(pool.imap_unordered(tarea, tr, chunksize=1), 1):
            res.append(r)
            if i % 9 == 0 or i == len(tr):
                log(f"          {i}/{len(tr)}")

    log()
    log("ANALISIS — umbrales EXACTOS de PREREGISTRO_supersticion_sal.md (ERR-31).")
    V.update(veredicto(res))
    ver = frase_final(V)
    log(); log(f"VEREDICTO: {ver}")

    meta = dict(fecha=time.strftime('%Y-%m-%dT%H:%M:%S'), T=T, alias=ALIAS, limpias=LIMPIAS,
                brazos={b: {k: (list(v) if isinstance(v, tuple) else v) for k, v in kw.items()}
                        for b, (kw, _) in BRAZOS.items()},
                veredicto=ver, veredictos=V, identidades=rc, procesos_python=ps, shas=SHAS(),
                python=platform.python_version(), numpy=np.__version__)
    dj = os.path.join(RAIZ, 'datos', f'sal_alias{len(ALIAS)}_{stamp}.json')
    json.dump(dict(meta=meta, principal=res), open(dj, 'w', encoding='utf-8'), ensure_ascii=False, default=str)
    log(f"datos -> {os.path.basename(dj)}  sha256_16 = {h16(dj)}")
    _log['f'].close()
