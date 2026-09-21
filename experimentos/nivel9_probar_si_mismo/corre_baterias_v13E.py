"""v13E -- "LA SORPRESA DEL MUNDO EN LA BOCA" (dE-TEST, PROPUESTA_v14.md segundo candidato) sobre el TRONCO:
prueba de NO REGRESION (retencion + generalizacion). Ejecuta PREREGISTRO_v13E.md. Corre, con la perilla
ENCENDIDA (organismo_v13E = organismo_v13p con eta_pred=0.03, ema_pred=0.05, k_testE=10.0 fijos por defecto),
exactamente la bateria del tronco (bateria_v13E = copia por anclas de organismo/bateria_v13.py, las seis etapas
y los CRIT importados INTACTOS) y la bateria de generalizacion (bateria_generaliza_E = copia por anclas, G1/G2/K
INTACTOS), en las semillas del examen v3' (101-120). REGLA 10: log desde el arranque con fsync. REGLA 11:
procesos vivos al log; un solo Pool a la vez (las baterias se lanzan como subprocesos secuenciales, cada una con
su propio Pool(14)).

Copiado de nivel7_hija_dispersa/corre_baterias_v13D.py con una correccion: alli las dos etapas de generalizacion
(perilla ON y la de referencia OFF) escriben en V[etiq.split()[1]], y las DOS etiquetas parten en la palabra
"GENERALIZACION" -- la etapa de referencia (que corre DESPUES) SOBREESCRIBE el veredicto de la etapa ON antes de
leerlo. Para la hija dispersa (perilla predicha casi inerte) probablemente no cambio el resultado; para dE-TEST,
que NO se predice inerte (ver PREREGISTRO_v13E.md §1), si importaria. Aqui cada etapa usa una CLAVE explicita.

Uso:  python experimentos/nivel9_probar_si_mismo/corre_baterias_v13E.py [--desde 101] [--n 20] [--humo]
      --humo = un proceso, sin Pool propio, 2 semillas; solo prueba que el montaje corre.
"""
import sys, os, re, json, time, hashlib, platform, subprocess
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
import numpy as np

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
# OJO: experimentos/v13_dos_vias/ tiene SU PROPIO organismo_v13.py (88c3574cf9cf38bf), distinto del tronco
# congelado (cc8b16b492d4d324). `organismo/` va PRIMERO en sys.path, siempre (ERR-28).
sys.path[:0] = [AQUI, os.path.join(RAIZ, 'organismo')]

HUMO = '--humo' in sys.argv
DESDE = int(sys.argv[sys.argv.index('--desde') + 1]) if '--desde' in sys.argv else 101
NSEM = 2 if HUMO else (int(sys.argv[sys.argv.index('--n') + 1]) if '--n' in sys.argv else 20)
N_PARALELO = 14
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


def tarea(args):
    tipo, seed = args
    if tipo == 'I':      # identidad: organismo_v13p (perillas en su default = apagadas) == organismo_v13 (congelado)
        import organismo_v13 as a_, organismo_v13p as b_
        a, b = a_.run(seed), b_.run(seed)
        dif = [k for k in a if N(a[k]) != N(b.get(k))]
        return dict(tipo=tipo, seed=seed, identico=not dif, difieren=dif, fuente=a_.__file__)
    import organismo_v13p as p_, organismo_v13E as e_   # E3: inercia (divisiones, celdas y sesgo de boca, con y sin la perilla; SIN inversion)
    off = p_.run(seed); on = e_.run(seed)
    return dict(tipo='E3', seed=seed, splits_off=off['splits'], splits_on=on['splits'],
                celdas_off=off['celdas'], celdas_on=on['celdas'],
                W_off=off['W'], W_on=on['W'], iguales=bool(N(off['W']) == N(on['W'])),
                sesgo_boca_on=on['sesgo_boca'], sbarE_on=on['sbarE'])


def lee_json(pref):
    """Ultimo datos/<pref><AAAAMMDD_HHMMSS>.json escrito (las baterias lo dejan con --log).
    ERR-87 (21 sep 2026): con startswith() el prefijo 'regresion_generaliza_organismo_v13E_' casaba tambien
    '..._v13E_k3_*' y '..._v13E_k5_*' (existen desde el 18 sep 03:09/03:24) y por orden de nombre ('k' > digito)
    devolvia el de k5. La corrida registrada (baterias_v13E_20260918_023210, 02:37) es ANTERIOR a esos archivos:
    no la afecta (verificado). Ahora exige prefijo + sello de tiempo exacto, igual que corre_baterias_v13D.py."""
    d = os.path.join(RAIZ, 'datos')
    pat = re.compile(r'^' + re.escape(pref) + r'\d{8}_\d{6}\.json$')
    c = sorted(f for f in os.listdir(d) if pat.match(f))
    return json.load(open(os.path.join(d, c[-1]), encoding='utf-8')) if c else None


if __name__ == '__main__':
    import multiprocessing as mp
    mp.set_start_method('spawn', force=True)
    stamp = time.strftime('%Y%m%d_%H%M%S')
    nom = f'baterias_v13E{"_humo" if HUMO else ""}_{stamp}'
    _log['f'] = open(os.path.join(RAIZ, 'datos', nom + '.log'), 'w', encoding='utf-8', newline='\n')
    pre = os.path.join(AQUI, 'PREREGISTRO_v13E.md')
    shas = {n_: h16(p) for n_, p in [
        ('preregistro', pre), ('script', os.path.abspath(__file__)),
        ('constructor_v13E', os.path.join(AQUI, 'construye_v13E.py')),
        ('constructor_probar', os.path.join(AQUI, 'construye_probar.py')),
        ('organismo_v13p', os.path.join(AQUI, 'organismo_v13p.py')),
        ('organismo_v13pg', os.path.join(AQUI, 'organismo_v13pg.py')),
        ('organismo_v13E', os.path.join(AQUI, 'organismo_v13E.py')),
        ('organismo_v13gE', os.path.join(AQUI, 'organismo_v13gE.py')),
        ('bateria_v13E', os.path.join(AQUI, 'bateria_v13E.py')),
        ('bateria_generaliza_E', os.path.join(AQUI, 'bateria_generaliza_E.py')),
        ('origen organismo_v13 (congelado)', os.path.join(RAIZ, 'organismo', 'organismo_v13.py')),
        ('origen bateria_v13 (congelada)', os.path.join(RAIZ, 'organismo', 'bateria_v13.py')),
        ('origen bateria_generaliza (congelada)', os.path.join(RAIZ, 'organismo', 'bateria_generaliza.py'))]}
    seeds = list(range(DESDE, DESDE + NSEM))
    log(f'ARRANQUE v13E ("la sorpresa del mundo en la boca", dE-TEST, sobre el tronco): NO REGRESION. semillas '
        f"{seeds[0]}-{seeds[-1]}. {'HUMO (un proceso)' if HUMO else f'Pool({N_PARALELO}) en la etapa 1; las baterias abren el suyo'}")
    log("sha " + "  ".join(f"{k} {v}" for k, v in shas.items()))
    try:
        ps = subprocess.run(['powershell', '-NoProfile', '-Command',
                             "Get-CimInstance Win32_Process | Where-Object { $_.Name -like 'python*' } | ForEach-Object { \"$($_.ProcessId) $($_.CommandLine)\" }"],
                            capture_output=True, text=True, timeout=60).stdout.strip().splitlines()
    except Exception as e:
        ps = [f"(no se pudo listar: {e})"]
    log(f"REGLA 11 -- procesos python vivos ({len(ps)}), este es pid {os.getpid()}")

    V = {}
    lote = [('I', s) for s in (1, 2, 3)] + [('E3', s) for s in seeds]
    log(f"ETAPA 1/3 -- IDENTIDAD (organismo_v13p == organismo_v13) + E3 inercia ({len(lote)})...")
    if HUMO:
        res = []
        for i, x in enumerate(lote, 1):
            res.append(tarea(x)); log(f"          {i}/{len(lote)}")
    else:
        with mp.Pool(N_PARALELO) as pool:
            res = []
            for i, r in enumerate(pool.imap_unordered(tarea, lote, chunksize=1), 1):
                res.append(r)
                if i % 5 == 0 or i == len(lote): log(f"          {i}/{len(lote)}")
    ide = [r for r in res if r['tipo'] == 'I']; e3 = [r for r in res if r['tipo'] == 'E3']
    log(f"  identidad: {sum(x['identico'] for x in ide)}/{len(ide)}   (organismo_v13 desde {ide[0]['fuente']})")
    for x in ide:
        if not x['identico']: log(f"      DIFIERE s{x['seed']}: {x['difieren'][:6]}")
    V['IDENTIDAD'] = all(x['identico'] for x in ide)
    if not V['IDENTIDAD']:
        log("*** IDENTIDAD FALLIDA: se para (un instrumento que no es bit a bit con la perilla apagada no confirma nada).")
        _log['f'].close(); sys.exit(1)
    so = float(np.median([r['splits_off'] for r in e3])); sn = float(np.median([r['splits_on'] for r in e3]))
    co = float(np.median([r['celdas_off'] for r in e3])); cn = float(np.median([r['celdas_on'] for r in e3]))
    n_ig = sum(r['iguales'] for r in e3)
    sesgo_med = [ (float(np.median(vals)) if (vals := [r['sesgo_boca_on'][q] for r in e3 if r['sesgo_boca_on'][q] is not None]) else None)
                  for q in range(4)]
    sbarE_med = float(np.median([r['sbarE_on'] for r in e3]))
    V['E3'] = dict(splits_off=so, splits_on=sn, celdas_off=co, celdas_on=cn, W_iguales=n_ig, n=len(e3),
                   sesgo_boca_mediana=sesgo_med, sbarE_mediana=sbarE_med,
                   ok_inercia=bool(abs(sn - so) <= 0.10 * max(so, 1) and abs(cn - co) <= 0.10 * max(co, 1)),
                   ok_sesgo_pequeno=bool(sbarE_med < 0.05 and all(x is not None and x < 0.05 for x in sesgo_med)))
    log(f"  E3 inercia: divisiones {so:.0f} -> {sn:.0f}   celdas {co:.0f} -> {cn:.0f}   W identico en {n_ig}/{len(e3)}"
        f"   -> {'OK (+-10%)' if V['E3']['ok_inercia'] else 'LA PERILLA SI MUEVE DIVISIONES/CELDAS AQUI'}")
    log(f"  E3 sesgo de boca (perilla ON, sin inversion): sesgo_boca mediana por cuarto {sesgo_med}   sbarE mediana final {sbarE_med:.5f}"
        f"   -> {'PEQUENO (<0.05)' if V['E3']['ok_sesgo_pequeno'] else 'NO ES PEQUENO (>=0.05 en algun punto)'}   [diagnostico, NO es gate -- ver PREREGISTRO_v13E.md §6]")

    env = dict(os.environ, PYTHONIOENCODING='utf-8')
    # clave EXPLICITA por etapa (NO se deriva del texto de la etiqueta: ver la nota de cabecera sobre el bug de
    # corre_baterias_v13D.py, donde 'GENERALIZACION' (ON) y 'GENERALIZACION de referencia' (OFF) colisionaban).
    etapas = [
        ('E1 RETENCION  (criterio v3\' completo, perilla ENCENDIDA)',
         [sys.executable, os.path.join(AQUI, 'bateria_v13E.py'), str(NSEM), '--desde', str(DESDE), '--log'],
         'examen_v13E_', 'E1'),
        ('E2 GENERALIZACION (G1/G2/K, perilla ENCENDIDA)',
         [sys.executable, os.path.join(AQUI, 'bateria_generaliza_E.py'), 'organismo_v13E', str(NSEM), '--desde', str(DESDE), '--log'],
         'regresion_generaliza_organismo_v13E_', 'E2'),
        ('GENERALIZACION de referencia (perilla APAGADA)',
         [sys.executable, os.path.join(AQUI, 'bateria_generaliza_E.py'), 'organismo_v13p', str(NSEM), '--desde', str(DESDE), '--log'],
         'regresion_generaliza_organismo_v13p_', 'E2_ref'),
    ]
    for etiq, cmd, pref, clave in etapas:
        log(); log(f"ETAPA {clave} -- {etiq} ...")
        p = subprocess.run(cmd, capture_output=True, text=True, env=env, cwd=os.path.join(RAIZ, 'organismo'))
        for l in [x.split('] ', 1)[-1].strip() for x in p.stdout.splitlines()
                  if ('PASA' in x or 'FALLA' in x or 'OK ' in x or 'VEREDICTO' in x or '***' in x)]:
            log(f"   {l}")
        if p.returncode != 0:
            log(f"   *** codigo {p.returncode}: {p.stderr[-500:]}")
        j = lee_json(pref)
        V[clave] = dict(returncode=p.returncode, veredictos=(j or {}).get('meta', {}).get('veredictos'))

    ret = V.get('E1', {}).get('veredictos') or {}
    gen = V.get('E2', {}).get('veredictos') or {}
    E1_ok = bool(ret) and all(bool(v) for v in ret.values())
    E2_ok = bool(gen) and all(bool(v) for v in gen.values())
    V['E1_retencion'] = E1_ok; V['E2_generalizacion'] = E2_ok
    if not V['IDENTIDAD']:
        ver = "INERCIA FALLIDA"
    elif E1_ok and E2_ok:
        ver = ('NO REGRESIONA: "la sorpresa del mundo en la boca" no dana la retencion ni la generalizacion del tronco'
               + ("; y el sesgo sin inversion es pequeno (E3 OK)" if V['E3']['ok_sesgo_pequeno'] else "; pero el sesgo sin inversion NO es pequeno (E3): revisar, no gate"))
    else:
        ver = ("SE QUEDA COMO ORGANO DE EXPERIMENTO (clausula §6 de PREREGISTRO_v13E.md): "
               + ("cae la retencion" if not E1_ok else "") + (" y " if (not E1_ok and not E2_ok) else "")
               + ("cae la generalizacion" if not E2_ok else "") + "; NO entra al tronco. Nada se recalibra.")
    log(); log(f"VEREDICTO v13E: {ver}")
    log(f"  E1 retencion (criterio v3' completo, 8 veredictos) = {E1_ok}   E2 generalizacion (G1/G2/K) = {E2_ok}"
        f"   E3 inercia/sesgo (diagnostico) = {V['E3']['ok_inercia']}/{V['E3']['ok_sesgo_pequeno']}")
    if HUMO:
        log("(HUMO: 2 semillas -- ningun criterio vale; solo prueba que el montaje corre.)")
    meta = dict(fecha=time.strftime('%Y-%m-%dT%H:%M:%S'), humo=HUMO, semillas=seeds, veredictos=V, veredicto=ver,
                identidades=ide, e3=e3, shas=shas, procesos_python=ps,
                python=platform.python_version(), numpy=np.__version__)
    dj = os.path.join(RAIZ, 'datos', nom + '.json')
    json.dump(dict(meta=meta), open(dj, 'w', encoding='utf-8'), ensure_ascii=False, default=str)
    log(f"datos -> {os.path.basename(dj)}  sha256_16 = {h16(dj)}")
    _log['f'].close()
