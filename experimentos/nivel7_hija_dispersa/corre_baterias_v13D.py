"""v13D — HIJA DISPERSA sobre el TRONCO: prueba de NO REGRESION (retencion + generalizacion).
Ejecuta PREREGISTRO_v13D.md. Corre, con la perilla ENCENDIDA, exactamente la bateria del tronco (bateria_v13D =
copia por anclas de organismo/bateria_v13.py, las seis etapas y los CRIT importados INTACTOS) y la bateria de
generalizacion (bateria_generaliza_D = copia por anclas, G1/G2/K INTACTOS), en las semillas del examen v3' (101-120).
REGLA 10: log desde el arranque con fsync. REGLA 11: procesos vivos al log; un solo Pool a la vez (las baterias se
lanzan como subprocesos secuenciales, cada una con su propio Pool(14)).

Uso:  python experimentos/nivel7_hija_dispersa/corre_baterias_v13D.py [--desde 101] [--n 20] [--humo]
      --humo = un proceso, sin Pool propio, 2 semillas; solo prueba que el montaje corre.
"""
import sys, os, json, time, hashlib, platform, subprocess
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
import numpy as np

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
# OJO: experimentos/v13_dos_vias/ tiene SU PROPIO organismo_v13.py (88c3574cf9cf38bf), distinto del tronco
# congelado (cc8b16b492d4d324). `organismo/` va PRIMERO en sys.path, siempre.
sys.path[:0] = [AQUI, os.path.join(RAIZ, 'organismo'), os.path.join(RAIZ, 'experimentos', 'v13_dos_vias')]

HUMO = '--humo' in sys.argv
DESDE = int(sys.argv[sys.argv.index('--desde') + 1]) if '--desde' in sys.argv else 101
NSEM = 2 if HUMO else (int(sys.argv[sys.argv.index('--n') + 1]) if '--n' in sys.argv else 20)
N_PARALELO = 14
NUEVAS = {'mask_rel', 'del_s', 'del_c', 'ema_c'}
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
    if tipo == 'I':      # identidad: perilla apagada == organismo_v13 (congelado)
        import organismo_v13 as a_, organismo_v13D as b_
        a, b = a_.run(seed), b_.run(seed, mask_rel=0)
        dif = [k for k in a if k not in NUEVAS and N(a[k]) != N(b[k])]
        return dict(tipo=tipo, seed=seed, identico=not dif, difieren=dif, fuente=a_.__file__)
    import organismo_v13D as m   # D3: inercia esperada (divisiones y celdas con y sin perilla)
    off = m.run(seed, mask_rel=0); on = m.run(seed, mask_rel=2)
    return dict(tipo='D3', seed=seed, splits_off=off['splits'], splits_on=on['splits'],
                celdas_off=off['celdas'], celdas_on=on['celdas'],
                W_off=off['W'], W_on=on['W'], iguales=bool(N(off['W']) == N(on['W'])))


def lee_json(pref):
    """Ultimo datos/<pref>*.json escrito (las baterias lo dejan con --log)."""
    d = os.path.join(RAIZ, 'datos')
    c = sorted([f for f in os.listdir(d) if f.startswith(pref) and f.endswith('.json')])
    return json.load(open(os.path.join(d, c[-1]), encoding='utf-8')) if c else None


if __name__ == '__main__':
    import multiprocessing as mp
    mp.set_start_method('spawn', force=True)
    stamp = time.strftime('%Y%m%d_%H%M%S')
    nom = f'baterias_v13D{"_humo" if HUMO else ""}_{stamp}'
    _log['f'] = open(os.path.join(RAIZ, 'datos', nom + '.log'), 'w', encoding='utf-8', newline='\n')
    pre = os.path.join(AQUI, 'PREREGISTRO_v13D.md')
    shas = {n_: h16(p) for n_, p in [
        ('preregistro', pre), ('script', os.path.abspath(__file__)),
        ('constructor', os.path.join(AQUI, 'construye_v13D.py')),
        ('organismo_v13D', os.path.join(AQUI, 'organismo_v13D.py')),
        ('organismo_v13Don', os.path.join(AQUI, 'organismo_v13Don.py')),
        ('organismo_v13gD', os.path.join(AQUI, 'organismo_v13gD.py')),
        ('bateria_v13D', os.path.join(AQUI, 'bateria_v13D.py')),
        ('bateria_generaliza_D', os.path.join(AQUI, 'bateria_generaliza_D.py')),
        ('origen organismo_v13 (congelado)', os.path.join(RAIZ, 'organismo', 'organismo_v13.py')),
        ('origen bateria_v13 (congelada)', os.path.join(RAIZ, 'organismo', 'bateria_v13.py'))]}
    seeds = list(range(DESDE, DESDE + NSEM))
    log(f"ARRANQUE v13D (hija dispersa sobre el tronco): NO REGRESION. semillas {seeds[0]}-{seeds[-1]}. "
        f"{'HUMO (un proceso)' if HUMO else f'Pool({N_PARALELO}) en la etapa 1; las baterias abren el suyo'}")
    log("sha " + "  ".join(f"{k} {v}" for k, v in shas.items()))
    try:
        ps = subprocess.run(['powershell', '-NoProfile', '-Command',
                             "Get-CimInstance Win32_Process | Where-Object { $_.Name -like 'python*' } | ForEach-Object { \"$($_.ProcessId) $($_.CommandLine)\" }"],
                            capture_output=True, text=True, timeout=60).stdout.strip().splitlines()
    except Exception as e:
        ps = [f"(no se pudo listar: {e})"]
    log(f"REGLA 11 — procesos python vivos ({len(ps)}), este es pid {os.getpid()}")

    V = {}
    lote = [('I', s) for s in (1, 2, 3)] + [('D3', s) for s in seeds]
    log(f"ETAPA 1/3 — IDENTIDAD (perilla apagada == organismo_v13) + D3 inercia ({len(lote)})...")
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
    ide = [r for r in res if r['tipo'] == 'I']; d3 = [r for r in res if r['tipo'] == 'D3']
    log(f"  identidad: {sum(x['identico'] for x in ide)}/{len(ide)}   (organismo_v13 desde {ide[0]['fuente']})")
    for x in ide:
        if not x['identico']: log(f"      DIFIERE s{x['seed']}: {x['difieren'][:6]}")
    V['IDENTIDAD'] = all(x['identico'] for x in ide)
    if not V['IDENTIDAD']:
        log("*** IDENTIDAD FALLIDA: se para (un instrumento que no es bit a bit con la perilla apagada no confirma nada).")
        _log['f'].close(); sys.exit(1)
    so = float(np.median([r['splits_off'] for r in d3])); sn = float(np.median([r['splits_on'] for r in d3]))
    co = float(np.median([r['celdas_off'] for r in d3])); cn = float(np.median([r['celdas_on'] for r in d3]))
    n_ig = sum(r['iguales'] for r in d3)
    V['D3'] = dict(splits_off=so, splits_on=sn, celdas_off=co, celdas_on=cn, W_iguales=n_ig, n=len(d3),
                   ok=bool(abs(sn - so) <= 0.10 * max(so, 1) and abs(cn - co) <= 0.10 * max(co, 1)))
    log(f"  D3 inercia: divisiones {so:.0f} -> {sn:.0f}   celdas {co:.0f} -> {cn:.0f}   W identico en {n_ig}/{len(d3)}"
        f"   -> {'OK (+-10%)' if V['D3']['ok'] else 'LA MASCARA SI ACTUA AQUI'}")

    env = dict(os.environ, PYTHONIOENCODING='utf-8')
    # ERR-29 (hallazgo del implementador del paquete v13E, 18 sep 02:05): la clave se derivaba de
    # etiq.split()[1], y las etapas 2/3 y 3b/3 colisionaban en 'GENERALIZACION' -- la de referencia (OFF, corre
    # despues) pisaba el veredicto de la ON antes de leerlo. El veredicto YA REGISTRADO (D2_generalizacion=True en
    # datos/baterias_v13D_20260918_012145.json) no cambia: los dos lados pasan (K 20/20, G1 0.800/19-20, G2
    # 0.834/19-20 segun el log). Clave EXPLICITA por etapa; no se vuelve a correr.
    etapas = [
        ('2/3 RETENCION  (criterio v3\', perilla ENCENDIDA)', [sys.executable, os.path.join(AQUI, 'bateria_v13D.py'), str(NSEM), '--desde', str(DESDE), '--log'], 'examen_v13D_', 'RETENCION'),
        ('3/3 GENERALIZACION (G1/G2/K, perilla ENCENDIDA)', [sys.executable, os.path.join(AQUI, 'bateria_generaliza_D.py'), 'organismo_v13D_on', str(NSEM), '--desde', str(DESDE), '--log'], 'regresion_generaliza_organismo_v13D_on_', 'D2'),
        ('3b/3 GENERALIZACION de referencia (perilla APAGADA)', [sys.executable, os.path.join(AQUI, 'bateria_generaliza_D.py'), 'organismo_v13D', str(NSEM), '--desde', str(DESDE), '--log'], 'regresion_generaliza_organismo_v13D_', 'D2_ref'),
    ]
    for etiq, cmd, pref, clave in etapas:
        log(); log(f"ETAPA {etiq} ...")
        p = subprocess.run(cmd, capture_output=True, text=True, env=env, cwd=os.path.join(RAIZ, 'organismo'))
        for l in [x.split('] ', 1)[-1].strip() for x in p.stdout.splitlines()
                  if ('PASA' in x or 'FALLA' in x or 'OK ' in x or 'VEREDICTO' in x or '***' in x)]:
            log(f"   {l}")
        if p.returncode != 0:
            log(f"   *** codigo {p.returncode}: {p.stderr[-500:]}")
        j = lee_json(pref)
        V[clave] = dict(returncode=p.returncode, veredictos=(j or {}).get('meta', {}).get('veredictos'))

    ret = V.get('RETENCION', {}).get('veredictos') or {}
    gen = V.get('D2', {}).get('veredictos') or {}
    D1 = bool(ret) and all(bool(v) for v in ret.values())
    D2 = bool(gen) and all(bool(v) for v in gen.values())
    V['D1_retencion'] = D1; V['D2_generalizacion'] = D2
    if not V['IDENTIDAD']:  ver = "INERCIA FALLIDA"
    elif D1 and D2:         ver = ("NO REGRESIONA: la hija dispersa no dana la retencion ni la generalizacion del tronco"
                                   + ("; y aqui casi no actua (D3 OK)" if V['D3']['ok'] else "; pero aqui SI actua (D3 NO): revisar"))
    else:                   ver = ("SE QUEDA COMO ORGANO DE EXPERIMENTO (clausula §6): "
                                   + ("cae la retencion" if not D1 else "") + (" y " if (not D1 and not D2) else "")
                                   + ("cae la generalizacion" if not D2 else "") + "; NO entra al tronco")
    log(); log(f"VEREDICTO v13D: {ver}")
    log(f"  D1 retencion (criterio v3') = {D1}   D2 generalizacion (G1/G2/K) = {D2}   D3 inercia = {V['D3']['ok']}")
    if HUMO:
        log("(HUMO: 2 semillas — ningun criterio vale; solo prueba que el montaje corre.)")
    meta = dict(fecha=time.strftime('%Y-%m-%dT%H:%M:%S'), humo=HUMO, semillas=seeds, veredictos=V, veredicto=ver,
                identidades=ide, d3=d3, shas=shas, procesos_python=ps,
                python=platform.python_version(), numpy=np.__version__)
    dj = os.path.join(RAIZ, 'datos', nom + '.json')
    json.dump(dict(meta=meta), open(dj, 'w', encoding='utf-8'), ensure_ascii=False, default=str)
    log(f"datos -> {os.path.basename(dj)}  sha256_16 = {h16(dj)}")
    _log['f'].close()
