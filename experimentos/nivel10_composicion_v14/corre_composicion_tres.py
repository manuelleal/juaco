"""corre_composicion_tres.py -- orquesta T1-T4 de PREREGISTRO_composicion_tres.md (COMPOSICION DE TRES: hija
dispersa + puerta por codigo + "la sorpresa del mundo en la boca", dosis 5).

Los UMBRALES que decide este runner son los del PREREGISTRO (T1 8/8 en 101-120, replica 8/8 en 121-140 si 101-120
pasa; T2 G1>=0.80,G2>=0.85,K 20/20; T3 recuperacion<=0.60x y pareado>=14/20 y apagado(P4')>=16/20), NO los que
traen de fabrica bateria_generaliza.py (G1>=0.65,G2>=0.55) ni ningun otro umbral de un runner que se reutiliza --
regla derivada de ERR-31. Por eso T2 NO lee el campo `veredictos` del JSON de bateria_generaliza_v14t.py: recalcula
G1/G2/K desde `corridas` (los numeros crudos por semilla) con los umbrales de aqui.

REGLA 10 (EQUIPO.md): log desde el arranque, con fsync. REGLA 11: un solo Pool a la vez -- T1/T2/T3 se lanzan como
SUBPROCESOS SECUENCIALES (bateria_v14t.py y bateria_generaliza_v14t.py abren cada uno su propio Pool(14), heredado
sin cambios de los originales congelados; corre_recuperacion_tres.py abre el suyo) -- cada subproceso termina
(y cierra su Pool) antes de que el siguiente arranque. T4 no abre Pool: no es medible (ver PREREGISTRO, seccion 4).

REGLA 3 (EQUIPO.md) -- por que --humo no llama a bateria_v14t.py ni a bateria_generaliza_v14t.py: esos dos
scripts SIEMPRE abren Pool(14) (lo heredan sin cambios de los congelados; no tienen modo de "una sola corrida"), y
un implementador no corre Pool. --humo hace, en UN SOLO PROCESO, sin Pool: (a) una identidad en miniatura
(perillas apagadas == organismo_v13, 2 semillas -- ya se corrio la version completa en identidad_v14t.py, 25/25);
(b) T3 humo, delegado a `corre_recuperacion_tres.py --humo` (que SI corre en su propio proceso, tambien sin Pool
-- se lanza como subproceso y se espera a que termine antes de seguir: sigue siendo UN proceso vivo a la vez).
NO mide T1/T2 (Pool: los corre el coordinador, sin --humo). T4 nunca se mide (no medible con los instrumentos de
este paquete; declarado en el preregistro).

Uso (desde la raiz del repo):
  python experimentos/nivel10_composicion_v14/corre_composicion_tres.py --humo
  python experimentos/nivel10_composicion_v14/corre_composicion_tres.py [--desde-bat 101] [--n-bat 20]
      [--desde-t3 161] [--n-t3 20] [--solo T1,T2,T3]
"""
import sys, os, json, time, hashlib, platform, subprocess
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
import numpy as np

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
# ERR-28: organismo/ PRIMERO en sys.path, siempre.
sys.path[:0] = [AQUI, os.path.join(RAIZ, 'organismo')]

HUMO = '--humo' in sys.argv


def _arg(flag, default):
    return int(sys.argv[sys.argv.index(flag) + 1]) if flag in sys.argv else default


DESDE_BAT = _arg('--desde-bat', 101)
NSEM_BAT = _arg('--n-bat', 20)
DESDE_T3 = _arg('--desde-t3', 161)
NSEM_T3 = _arg('--n-t3', 20)
SOLO = set(sys.argv[sys.argv.index('--solo') + 1].split(',')) if '--solo' in sys.argv else {'T1', 'T2', 'T3', 'T4'}

# ---- T2: umbrales del PREREGISTRO (no los de bateria_generaliza.py; ERR-31) ----
G1_MIN, G2_MIN = 0.80, 0.85

# ---- T1: los 8 veredictos decisivos del examen v3'' (los mismos que C1 de composicion_v14) ----
DECISIVOS = ['5_identidad', '1_cientificos', '2_celdas', '3_control', '4a_identidad',
             '4b_sin_conflicto_no_divide', '4c_misma_valencia', '4d_causa']

_log = {'f': None, 't0': time.time()}


def log(msg=""):
    linea = f"[{time.strftime('%H:%M:%S')} +{time.time()-_log['t0']:7.1f}s] {msg}"
    print(linea, flush=True)
    if _log['f']:
        _log['f'].write(linea + "\n"); _log['f'].flush(); os.fsync(_log['f'].fileno())


def h16(p):
    return hashlib.sha256(open(p, 'rb').read()).hexdigest()[:16]


def lee_json(pref):
    """Ultimo datos/<pref>*.json escrito. None si no hay ninguno (p.ej. si el criterio 5 de bateria_v14t.py aborto
    antes de escribir: sys.exit(1) antes del json.dump)."""
    d = os.path.join(RAIZ, 'datos')
    c = sorted([f for f in os.listdir(d) if f.startswith(pref) and f.endswith('.json')])
    return json.load(open(os.path.join(d, c[-1]), encoding='utf-8')) if c else None


def corre_bateria_v14t(desde, n, env):
    """Un tramo de T1 (examen v3'' con las TRES perillas ON): subproceso, Pool propio, hasta que termine."""
    cmd = [sys.executable, os.path.join(AQUI, 'bateria_v14t.py'), str(n), '--desde', str(desde), '--log']
    p = subprocess.run(cmd, capture_output=True, text=True, env=env, cwd=os.path.join(RAIZ, 'organismo'))
    for l in [x.split('] ', 1)[-1].strip() for x in p.stdout.splitlines() if ('PASA' in x or 'FALLA' in x or 'VEREDICTO' in x or '***' in x)]:
        log(f"   {l}")
    if p.returncode != 0:
        log(f"   *** codigo {p.returncode} (si es el criterio 5, aborta antes de escribir el json): {p.stderr[-500:]}")
    j = lee_json('examen_v14t_')
    veredictos = (j or {}).get('meta', {}).get('veredictos')
    decisivos_ok = sum(bool((veredictos or {}).get(k)) for k in DECISIVOS) if veredictos else 0
    ok8 = bool(veredictos) and decisivos_ok == len(DECISIVOS)
    return dict(desde=desde, n=n, returncode=p.returncode, veredictos=veredictos, decisivos_ok=decisivos_ok, ok=ok8)


if __name__ == '__main__':
    import multiprocessing as mp
    mp.set_start_method('spawn', force=True)
    stamp = time.strftime('%Y%m%d_%H%M%S')
    nom = f'composicion_tres{"_humo" if HUMO else ""}_{stamp}'
    _log['f'] = open(os.path.join(RAIZ, 'datos', nom + '.log'), 'w', encoding='utf-8', newline='\n')
    pre = os.path.join(AQUI, 'PREREGISTRO_composicion_tres.md')
    shas = {n_: h16(p) for n_, p in [
        ('preregistro', pre), ('script', os.path.abspath(__file__)),
        ('constructor', os.path.join(AQUI, 'construye_v14t.py')), ('identidad', os.path.join(AQUI, 'identidad_v14t.py')),
        ('organismo_v14t', os.path.join(AQUI, 'organismo_v14t.py')), ('organismo_v14t_on', os.path.join(AQUI, 'organismo_v14t_on.py')),
        ('organismo_v14gt', os.path.join(AQUI, 'organismo_v14gt.py')), ('bateria_v14t', os.path.join(AQUI, 'bateria_v14t.py')),
        ('bateria_generaliza_v14t', os.path.join(AQUI, 'bateria_generaliza_v14t.py')),
        ('corre_recuperacion_tres', os.path.join(AQUI, 'corre_recuperacion_tres.py')),
        ('origen organismo_v14c (composicion de dos)', os.path.join(AQUI, 'organismo_v14c.py')),
        ('origen bateria_v13 (congelada)', os.path.join(RAIZ, 'organismo', 'bateria_v13.py')),
        ('origen bateria_generaliza', os.path.join(RAIZ, 'organismo', 'bateria_generaliza.py')),
        ('origen construye_selfmodel', os.path.join(RAIZ, 'experimentos', 'creacion_C', 'construye_selfmodel.py')),
        ('origen construye_probar', os.path.join(RAIZ, 'experimentos', 'nivel9_probar_si_mismo', 'construye_probar.py'))]}
    log(f"ARRANQUE composicion de TRES (hija dispersa + puerta por codigo + dE-TEST dosis 5). "
        f"{'HUMO (un proceso, sin Pool, sin lanzar Pool en subprocesos)' if HUMO else f'SOLO={sorted(SOLO)}  subprocesos SECUENCIALES, un Pool a la vez'}")
    log("sha " + "  ".join(f"{k}={v}" for k, v in shas.items()))
    try:
        ps = subprocess.run(['powershell', '-NoProfile', '-Command',
                             "Get-CimInstance Win32_Process | Where-Object { $_.Name -like 'python*' } | ForEach-Object { \"$($_.ProcessId) $($_.CommandLine)\" }"],
                            capture_output=True, text=True, timeout=60).stdout.strip().splitlines()
    except Exception as e:
        ps = [f"(no se pudo listar: {e})"]
    log(f"REGLA 11 -- procesos python vivos ({len(ps)}), este es pid {os.getpid()}")

    V = {}
    env = dict(os.environ, PYTHONIOENCODING='utf-8')

    if HUMO:
        log(); log("ETAPA humo 1/2 -- identidad en miniatura (perillas apagadas == organismo_v13, 2 semillas)...")
        import organismo_v13 as _V13, organismo_v14t as _V14T
        ide = []
        for s in (1, 2):
            a, b = _V13.run(s, T=3000), _V14T.run(s, T=3000)
            dif = [k for k in a if a[k] != b.get(k)]
            ide.append(dict(seed=s, identico=not dif, difieren=dif))
            log(f"   s{s}: {'IDENTICO' if not dif else 'DIFIERE ' + str(dif[:6])}")
        V['identidad_humo'] = dict(ok=all(x['identico'] for x in ide), n=len(ide))
        log(f"   -> {V['identidad_humo']['ok']}  (identidad completa: python identidad_v14t.py, 25/25 ya corrido)")

        log(); log("ETAPA humo 2/2 -- T3 humo, delegado a corre_recuperacion_tres.py --humo (subproceso, sin Pool)...")
        p = subprocess.run([sys.executable, os.path.join(AQUI, 'corre_recuperacion_tres.py'), '--humo'],
                           capture_output=True, text=True, env=env, cwd=RAIZ)
        for l in p.stdout.splitlines():
            log(f"   {l.split('] ', 1)[-1] if '] ' in l else l}")
        if p.returncode != 0:
            log(f"   *** codigo {p.returncode}: {p.stderr[-500:]}")
        V['T3_humo'] = dict(returncode=p.returncode, ok=(p.returncode == 0))

    # ---------------- T1 ----------------
    if 'T1' in SOLO and not HUMO:
        log(); log(f"ETAPA T1 -- examen v3'' completo (bateria_v14t, las TRES perillas ON), semillas {DESDE_BAT}-{DESDE_BAT+NSEM_BAT-1}...")
        r1 = corre_bateria_v14t(DESDE_BAT, NSEM_BAT, env)
        log(f"   T1 (101-120 o el rango pedido) = {r1['decisivos_ok']}/8  ok={r1['ok']}")
        replica = None
        if r1['ok']:
            log(f"   T1 paso 8/8 -> corre la REPLICA en semillas nuevas {DESDE_BAT+20}-{DESDE_BAT+39} (misma letra, sin recalibrar)...")
            replica = corre_bateria_v14t(DESDE_BAT + 20, NSEM_BAT, env)
            log(f"   T1 replica = {replica['decisivos_ok']}/8  ok={replica['ok']}")
        else:
            log("   T1 NO dio 8/8 -> NO se corre la replica (nada que replicar; clausula del preregistro decide).")
        V['T1'] = dict(primera=r1, replica=replica, ok=bool(r1['ok'] and (replica is None or replica['ok'])))
        log(f"   T1 veredicto final: ok={V['T1']['ok']}")
    elif 'T1' in SOLO:
        log(); log("ETAPA T1 -- SALTADA en modo humo (exige Pool via bateria_v14t.py; la corre el coordinador sin --humo).")

    # ---------------- T2 ----------------
    if 'T2' in SOLO and not HUMO:
        log(); log(f"ETAPA T2 -- generalizacion (bateria_generaliza_v14t, organismo_v14t_on), semillas {DESDE_BAT}-{DESDE_BAT+NSEM_BAT-1}...")
        cmd = [sys.executable, os.path.join(AQUI, 'bateria_generaliza_v14t.py'), 'organismo_v14t_on', str(NSEM_BAT), '--desde', str(DESDE_BAT), '--log']
        p = subprocess.run(cmd, capture_output=True, text=True, env=env, cwd=os.path.join(RAIZ, 'organismo'))
        for l in [x.split('] ', 1)[-1].strip() for x in p.stdout.splitlines() if ('PASA' in x or 'FALLA' in x or 'OK ' in x or 'VEREDICTO' in x)]:
            log(f"   {l}")
        if p.returncode != 0:
            log(f"   *** codigo {p.returncode}: {p.stderr[-500:]}")
        j = lee_json('regresion_generaliza_organismo_v14t_on_')
        # ERR-31: NO se lee j['meta']['veredictos'] (umbrales 0.65/0.55 de bateria_generaliza.py). Se recalcula
        # G1/G2/K desde 'corridas' (numeros crudos por semilla) con los umbrales DEL PREREGISTRO.
        if j:
            res = j['corridas']; seeds = j['meta']['semillas']
            G_ = lambda rg: {r['seed']: r for r in res if r['regla'] == rg}
            px, az = G_('px0'), G_('azar')
            mpx = float(np.median([px[s]['acc'] for s in seeds])); maz = float(np.median([az[s]['acc'] for s in seeds]))
            par1 = sum(px[s]['acc'] > az[s]['acc'] for s in seeds)
            bpx = [px[s]['ba'] for s in seeds if px[s]['ba'] is not None]; baz = [az[s]['ba'] for s in seeds if az[s]['ba'] is not None]
            par2 = sum(1 for s in seeds if px[s]['ba'] is not None and az[s]['ba'] is not None and px[s]['ba'] > az[s]['ba'])
            cob20 = sum(px[s]['cobertura'] >= 6 for s in seeds)
            G1 = mpx >= G1_MIN; G2 = bool(bpx) and bool(baz) and float(np.median(bpx)) >= G2_MIN; K = cob20 == len(seeds)
            V['T2'] = dict(returncode=p.returncode, mpx=mpx, maz=maz, par1=par1, S=len(seeds),
                           ba_px=float(np.median(bpx)) if bpx else None, ba_az=float(np.median(baz)) if baz else None, par2=par2,
                           cobertura20=cob20, G1=G1, G2=G2, K=K, ok=bool(G1 and G2 and K))
            log(f"   G1 px0={mpx:.3f} (>={G1_MIN}) azar={maz:.3f} px0>azar {par1}/{len(seeds)}  -> {G1}")
            log(f"   G2 px0={V['T2']['ba_px']}  (>={G2_MIN}) azar={V['T2']['ba_az']} px0>azar {par2}/{len(seeds)}  -> {G2}")
            log(f"   K  cobertura>=6: {cob20}/{len(seeds)}  -> {K}   ==> T2 ok={V['T2']['ok']}")
        else:
            V['T2'] = dict(returncode=p.returncode, ok=False)
            log("   *** sin JSON: T2 no medible en esta corrida.")
    elif 'T2' in SOLO:
        log(); log("ETAPA T2 -- SALTADA en modo humo (exige Pool via bateria_generaliza_v14t.py).")

    # ---------------- T3 ----------------
    if 'T3' in SOLO and not HUMO:
        log(); log(f"ETAPA T3 -- recuperacion tras la inversion, LA TERCERA PIEZA EN COMPANIA (corre_recuperacion_tres.py), "
                   f"semillas {DESDE_T3}-{DESDE_T3+NSEM_T3-1}...")
        cmd = [sys.executable, os.path.join(AQUI, 'corre_recuperacion_tres.py'), '--desde', str(DESDE_T3), '--n', str(NSEM_T3)]
        p = subprocess.run(cmd, capture_output=True, text=True, env=env, cwd=RAIZ)
        for l in p.stdout.splitlines():
            log(f"   {l.split('] ', 1)[-1] if '] ' in l else l}")
        if p.returncode != 0:
            log(f"   *** codigo {p.returncode}: {p.stderr[-500:]}")
        j = lee_json('recuperacion_tres_2')   # el prefijo del stamp real (año); nunca recoge *_humo_* (empieza distinto)
        t3 = (j or {}).get('meta', {}).get('T3')
        V['T3'] = dict(returncode=p.returncode, **(t3 or {})) if t3 else dict(returncode=p.returncode, ok=False)
        log(f"   T3 ok={V['T3'].get('ok')}")
    elif 'T3' in SOLO:
        log(); log("ETAPA T3 -- SALTADA en modo humo del orquestador (se midio aparte arriba, humo 2/2, sin Pool).")

    # ---------------- T4 ----------------
    if 'T4' in SOLO:
        log(); log("ETAPA T4 -- composicion temporal 3T-k (mundo_composicion_v14 + la tercera perilla): NO MEDIBLE.")
        log("   mundo_composicion_v14.py es un instrumento YA CORRIDO en un estilo de codigo distinto (espacios")
        log("   alrededor de operadores) del que usan las anclas de pon_dE(); extenderlo exige un cuarto")
        log("   constructor con sus PROPIAS anclas verificadas una a una (fuera del alcance de este paquete).")
        log("   Ver PREREGISTRO_composicion_tres.md, seccion 4. No se inventa ningun numero.")
        V['T4'] = dict(ok=None, medible=False, razon='mundo_composicion_v14.py en estilo distinto; requiere constructor propio no incluido en este paquete')

    log()
    if HUMO:
        log("VEREDICTO: HUMO completo -- identidad en miniatura + T3 humo corren en proceso(s) sin Pool vivos a la vez "
            "(T1/T2 exigen Pool: quedan para el coordinador; T4 nunca es medible).")
        ver = "HUMO OK"
    else:
        t1 = V.get('T1', {}).get('ok'); t2 = V.get('T2', {}).get('ok'); t3 = V.get('T3', {}).get('ok'); t4 = V.get('T4', {}).get('ok')
        medidas = {k: v for k, v in [('T1', t1), ('T2', t2), ('T3', t3), ('T4', t4)] if k in SOLO}
        if any(v is False for k, v in [('T1', t1), ('T2', t2)] if k in SOLO):
            ver = "LOS TRES ORGANOS NO VAN JUNTOS: T1 o T2 cayeron (clausula del preregistro)."
        elif t3 is False:
            ver = "LA SORPRESA PIERDE SU EFECTO EN COMPANIA: T3 cayo (clausula del preregistro)."
        elif all(v in (True, None) for v in medidas.values()) and any(v is True for v in medidas.values()):
            faltan = [k for k, v in medidas.items() if v is None and k != 'T4']
            ver = "COMPOSICION DE TRES SOSTENIDA en lo medido" + (f" (faltan: {faltan}; " if faltan else " (") + "T4 no medible)"
        else:
            ver = f"INCOMPLETO: {medidas}"
        log(f"VEREDICTO composicion_tres: {ver}")
        log(f"  T1={t1}  T2={t2}  T3={t3}  T4={t4} (no medible)")

    meta = dict(fecha=time.strftime('%Y-%m-%dT%H:%M:%S'), humo=HUMO, solo=sorted(SOLO), veredictos=V, veredicto=ver,
               semillas=dict(bat=[DESDE_BAT, DESDE_BAT + NSEM_BAT - 1] if not HUMO else None,
                             t3=[DESDE_T3, DESDE_T3 + NSEM_T3 - 1] if not HUMO else None),
               shas=shas, procesos_python=ps, python=platform.python_version(), numpy=np.__version__, plataforma=platform.platform())
    dj = os.path.join(RAIZ, 'datos', nom + '.json')
    json.dump(dict(meta=meta), open(dj, 'w', encoding='utf-8'), ensure_ascii=False, default=str)
    log(f"datos -> {os.path.basename(dj)}  sha256_16 = {h16(dj)}")
    _log['f'].close()
