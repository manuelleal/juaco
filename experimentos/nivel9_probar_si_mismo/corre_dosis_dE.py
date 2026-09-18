"""corre_dosis_dE.py -- ejecuta PREREGISTRO_dosis_dE.md: DOS DOSIS menores de "la sorpresa del mundo en la boca"
(dE-TEST, k_testE en {3, 5}) contra la referencia YA MEDIDA (k_testE=10, v13E: recupera 7x mas rapido tras una
inversion no avisada pero la generalizacion de VALOR cae por debajo de la letra, G1 px0 0.750 < 0.80 exigido,
referencia apagada 0.800; PREREGISTRO_v13E.md). Hipotesis a probar: es una DOSIS -- con k_testE menor, la
recuperacion sigue siendo <=0.60x Y G1 vuelve a >=0.80 A LA VEZ.

Orquesta, como SUBPROCESOS SECUENCIALES -- cada uno con su propio Pool, UNO A LA VEZ (regla 11 de EQUIPO.md; nunca
mas de un Pool vivo):
  1/5 RECUPERACION    corre_probar_si_mismo.py --desde 121 --brazos V13,dE3,dE5 --baterias V13,dE3,dE5   (s121-140)
  2/5 GENERALIZACION  bateria_generaliza_E.py organismo_v13E_k3 20 --desde 101 --log                     (s101-120)
  3/5 GENERALIZACION  bateria_generaliza_E.py organismo_v13E_k5 20 --desde 101 --log                     (s101-120)
  4/5 EXAMEN          bateria_v13E_k3.py 20 --desde 101 --log                                            (s101-120)
  5/5 EXAMEN          bateria_v13E_k5.py 20 --desde 101 --log                                            (s101-120)

Cada veredicto por dosis se calcula EXACTAMENTE con los UMBRALES de PREREGISTRO_dosis_dE.md, seccion 6 -- ESTE
archivo, no los de una bateria reusada (ERR-31: corre_baterias_v13E.py decidio E2 con los umbrales de
bateria_generaliza.py [0.65/0.55] en vez de los preregistrados [0.80/0.85]; el registro siguio la letra del
preregistro, no la impresion del runner. Aqui los umbrales viven UNA sola vez, en UMBRAL, abajo).

REGLA 10: log desde el arranque, con fsync. REGLA 11: procesos python vivos al log antes de cada etapa.

Uso:  python experimentos/nivel9_probar_si_mismo/corre_dosis_dE.py [--desde 121]
      python experimentos/nivel9_probar_si_mismo/corre_dosis_dE.py --humo
          -- SECUENCIAL, de una sola tanda: 1/5 usa el --humo YA EXISTENTE de corre_probar_si_mismo.py (un solo
          proceso, semilla 1, SIN Pool -- no prueba --brazos en si, que no se puede achicar por debajo de sus 20
          semillas fijas sin tocar umbrales absolutos ya preregistrados en ESE script; --brazos/--baterias se
          probaron aparte, por validacion de argumentos + una prueba aislada del bloque de analisis con datos
          fabricados, ver la nota de implementacion en PREREGISTRO_dosis_dE.md, seccion 2); 2/5-5/5 SI corren de
          verdad, con 2 semillas cada una (mismo patron que el --humo de corre_baterias_v13E.py).
"""
import sys, os, json, time, glob, hashlib, platform, subprocess, statistics

sys.stdout.reconfigure(encoding='utf-8', errors='replace')
AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
# OJO (ERR-28): experimentos/v13_dos_vias/ tiene SU PROPIO organismo_v13.py, distinto del tronco congelado.
# organismo/ va PRIMERO en sys.path, siempre. No hace falta importar organismos aqui (solo se leen JSON), pero se
# deja por si algun dia este runner necesita h16 de un modulo fuera de AQUI/organismo.
sys.path[:0] = [AQUI, os.path.join(RAIZ, 'organismo')]

HUMO = '--humo' in sys.argv
DESDE_REC = int(sys.argv[sys.argv.index('--desde') + 1]) if '--desde' in sys.argv else 121
DESDE_GEN = 101   # semillas del examen de congelacion de v13 (ERR-21), igual que PREREGISTRO_v13E.md
NSEM = 2 if HUMO else 20
DOSIS = ('dE3', 'dE5')          # nombre del brazo en corre_probar_si_mismo.py / BRAZOS
MODULOS = {'dE3': 'organismo_v13E_k3', 'dE5': 'organismo_v13E_k5'}   # modulo para bateria_generaliza_E / bateria_v13E_kK
K_DE = {'dE3': 3, 'dE5': 5}

# ---- UMBRALES (PREREGISTRO_dosis_dE.md, seccion 6) -- EXACTOS, calculados AQUI, nunca pedidos prestados a una
# bateria reusada (ERR-31). Una dosis es CANDIDATA solo si TODOS a la vez.
UMBRAL = dict(recup_razon=0.60, recup_pareado=14, apagado_p4=16,
              G1_mediana=0.80, G1_pareado=15, G2_mediana=0.85, K_completa=20)

_log = {'f': None, 't0': time.time()}


def log(msg=""):
    linea = f"[{time.strftime('%H:%M:%S')} +{time.time()-_log['t0']:7.1f}s] {msg}"
    print(linea, flush=True)
    if _log['f']:
        _log['f'].write(linea + "\n"); _log['f'].flush(); os.fsync(_log['f'].fileno())


def h16(p):
    return hashlib.sha256(open(p, 'rb').read()).hexdigest()[:16]


def mediana(xs):
    xs = [x for x in xs if x is not None]
    return float(statistics.median(xs)) if xs else None


def procesos_python():
    try:
        return subprocess.run(['powershell', '-NoProfile', '-Command',
                               "Get-CimInstance Win32_Process | Where-Object { $_.Name -like 'python*' } | ForEach-Object { \"$($_.ProcessId) $($_.CommandLine)\" }"],
                              capture_output=True, text=True, timeout=60).stdout.strip().splitlines()
    except Exception as e:
        return [f"(no se pudo listar: {e})"]


def lee_json(pref, tras):
    """Ultimo datos/<pref>*.json escrito EN O DESPUES de <tras> (epoch, segundos) -- nunca uno viejo de otra corrida."""
    d = os.path.join(RAIZ, 'datos')
    c = sorted(f for f in os.listdir(d) if f.startswith(pref) and f.endswith('.json')
               and os.path.getmtime(os.path.join(d, f)) >= tras - 1)
    if not c:
        return None, None
    nom = c[-1]
    return nom, json.load(open(os.path.join(d, nom), encoding='utf-8'))


def corre(cmd, etiqueta):
    """Un subproceso (con SU PROPIO Pool adentro, si lo tiene) -- uno a la vez, nunca en paralelo con otro."""
    log(f"    procesos python vivos antes: {len(procesos_python())}")
    log(f"    $ {' '.join(os.path.relpath(c, RAIZ) if os.path.sep in c else c for c in cmd)}")
    t0 = time.time()
    p = subprocess.run(cmd, capture_output=True, text=True,
                        env=dict(os.environ, PYTHONIOENCODING='utf-8'), cwd=AQUI)
    dt = time.time() - t0
    claves = ('PASA', 'FALLA', 'OK ', 'ROTO', 'VEREDICTO', 'IDENTIDAD', '***', 'identicas', 'identidad:')
    for l in [x.split('] ', 1)[-1].strip() for x in p.stdout.splitlines() if any(k in x for k in claves)]:
        log(f"      {l}")
    if p.returncode != 0:
        log(f"    *** {etiqueta}: codigo de salida {p.returncode}")
        log(f"        stderr (ultimos 800): {p.stderr[-800:]}")
    else:
        log(f"    {etiqueta}: terminado OK en {dt:.1f}s")
    return p


# ---------------------------------------------------------------- analisis (umbrales propios, ERR-31)
def analiza_recuperacion(principal, dosis):
    """P1'/P4' (PREREGISTRO_probar_si_mismo.md enmienda 1; misma formula que analiza_dE.py) de <dosis> contra V13,
    sobre los datos CRUDOS de 'principal' -- nunca sobre un veredicto que corre_probar_si_mismo.py haya podido
    imprimir el mismo (con --brazos reducido esa corrida ni siquiera calcula P1/P4 genericos: ver su rama DOSIS)."""
    por = {}
    for r in principal:
        if r.get('tipo') == 'T':
            por.setdefault(r['seed'], {})[r['brazo']] = r
    seeds = sorted(s for s in por if 'V13' in por[s] and dosis in por[s])
    v13_rec = mediana([por[s]['V13']['recup'] for s in seeds])
    rec = mediana([por[s][dosis]['recup'] for s in seeds])
    par = sum(por[s][dosis]['recup'] < por[s]['V13']['recup'] for s in seeds)
    sb = lambda s: por[s][dosis]['sesgo_boca']
    apaga = sum(1 for s in seeds if all(sb(s)[q] is not None for q in (1, 2, 3)) and sb(s)[2]
                and sb(s)[1] <= 0.10 and sb(s)[3] <= 0.10 and sb(s)[1] <= 0.35 * sb(s)[2] and sb(s)[3] <= 0.35 * sb(s)[2])
    razon = (rec / v13_rec) if (rec is not None and v13_rec) else None
    return dict(n=len(seeds), v13_recup_mediana=v13_rec, recup_mediana=rec, razon=razon, pareado=par, apagado_p4=apaga,
                ok_recuperacion=bool(razon is not None and razon <= UMBRAL['recup_razon'] and par >= UMBRAL['recup_pareado']),
                ok_apagado=bool(apaga >= UMBRAL['apagado_p4']))


def analiza_generalizacion(corridas):
    """G1/G2/K -- formula COPIADA de organismo/bateria_generaliza.py sobre 'corridas' crudas, con los UMBRALES del
    preregistro de la dosis (0.80/0.85/20 de 20), no los que bateria_generaliza_E.py imprime en su propio veredicto
    (0.65/0.55/>=90%, heredados sin tocar de la Etapa 3: ERR-31 fue exactamente este error, para v13E)."""
    px = {r['seed']: r for r in corridas if r['regla'] == 'px0'}
    az = {r['seed']: r for r in corridas if r['regla'] == 'azar'}
    seeds = sorted(set(px) & set(az))
    mpx, maz = mediana([px[s]['acc'] for s in seeds]), mediana([az[s]['acc'] for s in seeds])
    par1 = sum(px[s]['acc'] > az[s]['acc'] for s in seeds)
    bpx = [px[s]['ba'] for s in seeds if px[s]['ba'] is not None]
    baz = [az[s]['ba'] for s in seeds if az[s]['ba'] is not None]
    par2 = sum(1 for s in seeds if px[s]['ba'] is not None and az[s]['ba'] is not None and px[s]['ba'] > az[s]['ba'])
    cob = sum(px[s]['cobertura'] >= 6 for s in seeds)
    g2 = mediana(bpx)
    return dict(n=len(seeds), G1_mediana=mpx, G1_azar=maz, G1_pareado=par1, G2_mediana=g2, G2_azar=mediana(baz),
                G2_pareado=par2, K_cobertura=cob,
                ok_G1=bool(mpx is not None and mpx >= UMBRAL['G1_mediana'] and par1 >= UMBRAL['G1_pareado']),
                ok_G2=bool(g2 is not None and g2 >= UMBRAL['G2_mediana']), ok_K=bool(cob >= UMBRAL['K_completa']))


DECISIVOS_EXAMEN = ['5_identidad', '1_cientificos', '2_celdas', '3_control', '4a_identidad',
                     '4b_sin_conflicto_no_divide', '4c_misma_valencia', '4d_causa']


def analiza_examen(veredictos):
    """Los OCHO veredictos decisivos del criterio v3' -- bateria_v13E_kK.py NO los pide prestados a nadie (son los
    umbrales originales, intactos, de organismo/bateria_v13.py): sin riesgo ERR-31, se leen tal cual del JSON."""
    ok = {k: bool((veredictos or {}).get(k)) for k in DECISIVOS_EXAMEN}
    return dict(veredictos=ok, ok_examen=bool(veredictos) and all(ok.values()), n_ok=sum(ok.values()), n=len(DECISIVOS_EXAMEN))


def shas():
    d = dict(
        preregistro=h16(os.path.join(AQUI, 'PREREGISTRO_dosis_dE.md')),
        preregistro_v13E=h16(os.path.join(AQUI, 'PREREGISTRO_v13E.md')),
        script=h16(os.path.abspath(__file__)),
        constructor_v13E=h16(os.path.join(AQUI, 'construye_v13E.py')),
        identidad_dosis=h16(os.path.join(AQUI, 'identidad_dosis.py')),
        corre_probar_si_mismo=h16(os.path.join(AQUI, 'corre_probar_si_mismo.py')),
        bateria_generaliza_E=h16(os.path.join(AQUI, 'bateria_generaliza_E.py')),
        organismo_v13p=h16(os.path.join(AQUI, 'organismo_v13p.py')),
        organismo_v13pg=h16(os.path.join(AQUI, 'organismo_v13pg.py')),
        origen_organismo_v13=h16(os.path.join(RAIZ, 'organismo', 'organismo_v13.py')),
        origen_organismo_v11=h16(os.path.join(RAIZ, 'organismo', 'organismo_v11.py')),
        origen_bateria_v13=h16(os.path.join(RAIZ, 'organismo', 'bateria_v13.py')),
        origen_bateria_generaliza=h16(os.path.join(RAIZ, 'organismo', 'bateria_generaliza.py')))
    for dosis, K in K_DE.items():
        d[f'organismo_v13E_k{K}'] = h16(os.path.join(AQUI, f'organismo_v13E_k{K}.py'))
        d[f'organismo_v13gE_k{K}'] = h16(os.path.join(AQUI, f'organismo_v13gE_k{K}.py'))
        d[f'bateria_v13E_k{K}'] = h16(os.path.join(AQUI, f'bateria_v13E_k{K}.py'))
    return d


if __name__ == '__main__':
    stamp = time.strftime('%Y%m%d_%H%M%S')
    nom = f'dosis_dE{"_humo" if HUMO else ""}_{stamp}'
    _log['f'] = open(os.path.join(RAIZ, 'datos', nom + '.log'), 'w', encoding='utf-8', newline='\n')
    log(f"ARRANQUE corre_dosis_dE.py {'HUMO (secuencial, min. Pool)' if HUMO else '(real)'}: dosis {list(K_DE.values())}"
        f" (k_testE) contra V13 y contra la referencia ya medida k_testE=10 (v13E, NO se repite).")
    log(f"recuperacion: semillas {DESDE_REC}-{DESDE_REC+NSEM-1 if HUMO else DESDE_REC+19}   generalizacion/examen: semillas {DESDE_GEN}-{DESDE_GEN+NSEM-1}")
    for k, v in shas().items():
        log(f"    sha {k:26s} {v}")
    log(f"UMBRALES (PREREGISTRO_dosis_dE.md §6): {UMBRAL}")
    log(f"REGLA 11 -- procesos python vivos ({len(procesos_python())}), este es pid {os.getpid()}")

    R = {}   # resultados crudos por medida
    t_rec = time.time()
    if HUMO:
        log(); log("1/5 RECUPERACION -- HUMO: se usa el --humo YA EXISTENTE de corre_probar_si_mismo.py (semilla 1,"
                    " SIN Pool). No ejercita --brazos (no se puede achicar de 20 semillas sin tocar umbrales"
                    " absolutos de ESE script ya preregistrados); --brazos/--baterias se validaron aparte -- ver"
                    " PREREGISTRO_dosis_dE.md, seccion 2 (nota de implementacion).")
        corre([sys.executable, os.path.join(AQUI, 'corre_probar_si_mismo.py'), '--humo'], '1/5 recuperacion (humo)')
        R['recuperacion'] = None
    else:
        log(); log(f"1/5 RECUPERACION -- corre_probar_si_mismo.py --desde {DESDE_REC} --brazos V13,dE3,dE5 --baterias V13,dE3,dE5 (semillas {DESDE_REC}-{DESDE_REC+19})")
        corre([sys.executable, os.path.join(AQUI, 'corre_probar_si_mismo.py'), '--desde', str(DESDE_REC),
               '--brazos', 'V13,dE3,dE5', '--baterias', 'V13,dE3,dE5'], '1/5 recuperacion')
        nomj, dj = lee_json(f'probar_si_mismo_s{DESDE_REC}-{DESDE_REC+19}_', t_rec)
        if dj is None:
            log("    *** 1/5: no aparecio el JSON esperado. Sin datos de recuperacion.")
            R['recuperacion'] = dict(archivo=None)
        else:
            principal = dj.get('principal', [])
            R['recuperacion'] = dict(archivo=nomj, sha=h16(os.path.join(RAIZ, 'datos', nomj)),
                                      **{d: analiza_recuperacion(principal, d) for d in DOSIS})
            for d in DOSIS:
                a = R['recuperacion'][d]
                log(f"    {d}: recup mediana {a['recup_mediana']} (V13 {a['v13_recup_mediana']})  razon {None if a['razon'] is None else round(a['razon'],3)}"
                    f" (<={UMBRAL['recup_razon']})  pareado {a['pareado']}/{a['n']} (>={UMBRAL['recup_pareado']})  apagado(P4') {a['apagado_p4']}/{a['n']} (>={UMBRAL['apagado_p4']})"
                    f"  -> recuperacion {'OK' if a['ok_recuperacion'] else 'NO'}  apagado {'OK' if a['ok_apagado'] else 'NO'}")

    for i, d in enumerate(DOSIS):
        K = K_DE[d]; modulo = MODULOS[d]
        t0 = time.time()
        log(); log(f"{2+i}/5 GENERALIZACION -- bateria_generaliza_E.py {modulo} {NSEM} --desde {DESDE_GEN} --log (semillas {DESDE_GEN}-{DESDE_GEN+NSEM-1})")
        corre([sys.executable, os.path.join(AQUI, 'bateria_generaliza_E.py'), modulo, str(NSEM), '--desde', str(DESDE_GEN), '--log'],
              f'{2+i}/5 generalizacion {d}')
        nomj, dj = lee_json(f'regresion_generaliza_{modulo}_', t0)
        if dj is None:
            log(f"    *** {2+i}/5: no aparecio el JSON esperado para {modulo}.")
            R.setdefault('generalizacion', {})[d] = dict(archivo=None)
        else:
            corridas = dj.get('corridas', [])
            a = analiza_generalizacion(corridas) if not HUMO else dict(nota='HUMO: 2 semillas, ningun umbral vale')
            R.setdefault('generalizacion', {})[d] = dict(archivo=nomj, sha=h16(os.path.join(RAIZ, 'datos', nomj)), **a)
            if not HUMO:
                log(f"    {d}: G1 px0 {a['G1_mediana']} (azar {a['G1_azar']}, >={UMBRAL['G1_mediana']}) pareado {a['G1_pareado']}/{a['n']} (>={UMBRAL['G1_pareado']})"
                    f"  G2 {a['G2_mediana']} (azar {a['G2_azar']}, >={UMBRAL['G2_mediana']})  K {a['K_cobertura']}/{a['n']} (=={UMBRAL['K_completa']})"
                    f"  -> G1 {'OK' if a['ok_G1'] else 'NO'}  G2 {'OK' if a['ok_G2'] else 'NO'}  K {'OK' if a['ok_K'] else 'NO'}")

    for i, d in enumerate(DOSIS):
        K = K_DE[d]
        t0 = time.time()
        log(); log(f"{4+i}/5 EXAMEN -- bateria_v13E_k{K}.py {NSEM} --desde {DESDE_GEN} --log (semillas {DESDE_GEN}-{DESDE_GEN+NSEM-1})")
        corre([sys.executable, os.path.join(AQUI, f'bateria_v13E_k{K}.py'), str(NSEM), '--desde', str(DESDE_GEN), '--log'],
              f'{4+i}/5 examen {d}')
        nomj, dj = lee_json(f'examen_v13E_k{K}_', t0)
        if dj is None:
            log(f"    *** {4+i}/5: no aparecio el JSON esperado para bateria_v13E_k{K}.")
            R.setdefault('examen', {})[d] = dict(archivo=None)
        else:
            ver = (dj.get('meta') or {}).get('veredictos') or {}
            a = analiza_examen(ver) if not HUMO else dict(nota='HUMO: 2 semillas, ningun umbral vale', veredictos=ver)
            R.setdefault('examen', {})[d] = dict(archivo=nomj, sha=h16(os.path.join(RAIZ, 'datos', nomj)), **a)
            if not HUMO:
                log(f"    {d}: examen {a['n_ok']}/{a['n']}  -> {'OK (8/8)' if a['ok_examen'] else 'NO'}   {a['veredictos']}")

    # ---------------------------------------------------------------- veredicto por dosis (PREREGISTRO_dosis_dE.md §6/§7)
    log(); log("VEREDICTO por dosis (los SEIS a la vez; PREREGISTRO_dosis_dE.md, seccion 6/7):")
    candidatas = []
    veredicto_dosis = {}
    if not HUMO:
        for d in DOSIS:
            rec = R.get('recuperacion', {}).get(d, {})
            gen = R.get('generalizacion', {}).get(d, {})
            exa = R.get('examen', {}).get(d, {})
            seis = dict(recuperacion=rec.get('ok_recuperacion', False), apagado=rec.get('ok_apagado', False),
                        G1=gen.get('ok_G1', False), G2=gen.get('ok_G2', False), K=gen.get('ok_K', False),
                        examen=exa.get('ok_examen', False))
            candidata = all(seis.values())
            veredicto_dosis[d] = dict(seis=seis, candidata=candidata)
            if candidata:
                candidatas.append(d)
            log(f"   {d} (k_testE={K_DE[d]}): " + "  ".join(f"{k}={'OK' if v else 'NO'}" for k, v in seis.items())
                + f"  -> {'CANDIDATA' if candidata else 'no candidata'}")
        if candidatas:
            veredicto = (f"CANDIDATA(S): {candidatas} cumplen las seis condiciones a la vez (recuperacion rapida Y"
                         " generalizacion de valor intacta). Camino declarado: preregistro de congelacion (gemelo +"
                         " manifiesto.py), como marca PREREGISTRO_v13E.md seccion 7.")
        else:
            veredicto = ("NINGUNA DOSIS cumple las seis condiciones a la vez: el canje recuperacion-generalizacion"
                         " de valor de 'la sorpresa del mundo en la boca' es REAL (no un artefacto de k_testE=10) y"
                         " se registra como tal. Por la clausula del preregistro (seccion 7): no se prueban mas"
                         " dosis: 'la sorpresa del mundo en la boca' se queda fuera de la propuesta de v14 con su"
                         " coste anotado, junto a la version k_testE=10 (PREREGISTRO_v13E.md).")
    else:
        veredicto = "HUMO: sin veredicto (faltan datos reales de 1/5 recuperacion y umbrales de 2/5-5/5 con solo 2 semillas)."
    log(); log(f"VEREDICTO: {veredicto}")

    meta = dict(fecha=time.strftime('%Y-%m-%dT%H:%M:%S'), humo=HUMO, desde_recuperacion=DESDE_REC, desde_gen_examen=DESDE_GEN,
                n_semillas=NSEM, dosis=K_DE, umbrales=UMBRAL, veredicto_dosis=veredicto_dosis, veredicto=veredicto,
                shas=shas(), procesos_python=procesos_python(), python=platform.python_version())
    dj = os.path.join(RAIZ, 'datos', nom + '.json')
    json.dump(dict(meta=meta, resultados=R), open(dj, 'w', encoding='utf-8'), ensure_ascii=False, indent=1, default=str)
    log(f"datos -> {os.path.basename(dj)}  sha256_16 = {h16(dj)}")
    log(f"TIEMPO TOTAL: {time.time()-_log['t0']:.1f}s")
    _log['f'].close()
