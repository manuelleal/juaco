"""Nivel 6, experimento 2 del plan: tabla M + teletransporte en un mundo con vision limitada. Ejecuta PREREGISTRO_mapa.md.
REGLA 10: log desde el arranque. Identidad: mundo_mapa con perillas apagadas == organismo_v13 (todas las claves).
Uso:  python experimentos/nivel6_mapa/corre_mapa.py [--desde N]
"""
import sys, os, json, time, hashlib, platform, subprocess
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
import numpy as np

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
sys.path[:0] = [AQUI, os.path.join(RAIZ, 'organismo')]
_desde = int(sys.argv[sys.argv.index('--desde') + 1]) if '--desde' in sys.argv else 1
SEEDS = list(range(_desde, _desde + 20))
MUNDO = dict(r_vis=3, sitios=('A', 'B'))
PRUEBA = dict(n_tel=40, E_test=0.3, max_pasos=30)
BRAZOS = {
    'MAPA':      dict(usa_M=True, prueba=dict(PRUEBA)),
    'SINMAPA':   dict(usa_M=False, prueba=dict(PRUEBA)),
    'CONGELADA': dict(usa_M=True, escribe_M=False, prueba=dict(PRUEBA)),
    'BARAJADO':  dict(usa_M=True, prueba=dict(PRUEBA, barajar=True)),
    'SINCOMIDA': dict(usa_M=True, prueba=dict(PRUEBA), sitios=('B', 'B')),
    'INVERTIDO': dict(usa_M=True, prueba=dict(PRUEBA, invertir=True)),   # enmienda 1: valor con el signo cambiado en la prueba
}
IDENT = [dict(), dict(invertir_en=50000), dict(nuevo='C')]
N_PARALELO = 14
RAPIDO = '--rapido' in sys.argv   # gemelo compilado (mundo_mapa_rapido, identidad 90/90 + 81/81): solo si su etapa de identidad da 3/3
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
    tipo = args[0]
    if tipo == 'I':
        _, i, seed = args
        import organismo_v13 as a_, mundo_mapa as b_
        a, b = a_.run(seed, **IDENT[i]), b_.run(seed, **IDENT[i])
        dif = [kk for kk in a if N(a[kk]) != N(b[kk])]
        return dict(tipo=tipo, esc=f'ident{i}', seed=seed, identico=not dif, difieren=dif)
    if tipo == 'R':   # identidad del gemelo compilado contra el original (brazo MAPA)
        _, seed = args
        import mundo_mapa as a_, mundo_mapa_rapido as b_
        kw = dict(MUNDO); kw.update(BRAZOS['MAPA']); kw['T'] = 30000
        a, b = a_.run(seed, **kw), b_.run(seed, **kw)
        dif = [kk for kk in a if N(a[kk]) != N(b[kk])]
        return dict(tipo=tipo, esc='rapido', seed=seed, identico=not dif, difieren=dif)
    _, brazo, seed = args
    if RAPIDO:
        import mundo_mapa_rapido as m
    else:
        import mundo_mapa as m
    kw = dict(MUNDO); kw.update(BRAZOS[brazo])
    r = m.run(seed, **kw)
    return dict(tipo='T', brazo=brazo, seed=seed, tel=r['tel'], M_llenas=r['M_llenas'], W=r['W'], deaths=r['deaths'],
                mord=r['mord'], splits=r['splits'], celdas=r['celdas'])


def med(xs):
    return float(np.median(xs)), float(min(xs)), float(max(xs))


if __name__ == '__main__':
    import multiprocessing as mp
    mp.set_start_method('spawn', force=True)
    stamp = time.strftime('%Y%m%d_%H%M%S')
    _log['f'] = open(os.path.join(RAIZ, 'datos', f'mapa_s{SEEDS[0]}-{SEEDS[-1]}_{stamp}.log'), 'w', encoding='utf-8', newline='\n')
    pre = os.path.join(AQUI, 'PREREGISTRO_mapa.md')
    log(f"ARRANQUE nivel 6 (mapa) sobre v13. brazos {list(BRAZOS)}, semillas {SEEDS[0]}-{SEEDS[-1]}. Pool({N_PARALELO}).")
    log(f"sha preregistro {h16(pre)}  script {h16(os.path.abspath(__file__))}  mundo_mapa {h16(os.path.join(AQUI, 'mundo_mapa.py'))}  v13 {h16(os.path.join(RAIZ, 'organismo', 'organismo_v13.py'))}")
    try:
        ps = subprocess.run(['powershell', '-NoProfile', '-Command',
                             "Get-CimInstance Win32_Process | Where-Object { $_.Name -like 'python*' } | ForEach-Object { \"$($_.ProcessId) $($_.CommandLine)\" }"],
                            capture_output=True, text=True, timeout=60).stdout.strip().splitlines()
    except Exception as e:
        ps = [f"(no se pudo listar: {e})"]
    log(f"REGLA 11 — procesos python vivos ({len(ps)}), este es pid {os.getpid()}")
    V = {}
    with mp.Pool(N_PARALELO) as pool:
        ctrl = [('I', i, s) for i in range(len(IDENT)) for s in (1, 2, 3)]
        log(f"ETAPA 1/3 — identidad perillas apagadas == organismo_v13 ({len(ctrl)})...")
        rc = pool.map(tarea, ctrl, chunksize=1)
        log(f"  identicos: {sum(x['identico'] for x in rc)}/{len(rc)}")
        for x in rc:
            if not x['identico']: log(f"      DIFIERE {x['esc']} s{x['seed']}: {x['difieren']}")
        V['IDENTIDAD'] = all(x['identico'] for x in rc)
        if not V['IDENTIDAD']:
            log("*** IDENTIDAD FALLIDA: se para."); sys.exit(1)
        if RAPIDO:
            rr = pool.map(tarea, [('R', s) for s in (1, 2, 3)], chunksize=1)
            log(f"  identidad gemelo compilado == original (MAPA, T=30000): {sum(x['identico'] for x in rr)}/3")
            if not all(x['identico'] for x in rr):
                log('*** GEMELO NO IDENTICO: se para (corre sin --rapido).'); sys.exit(1)
            V['IDENTIDAD_RAPIDO'] = True
        tr = [('T', b, s) for b in BRAZOS for s in SEEDS]
        log(f"ETAPA 2/3 — {len(tr)} corridas...")
        res = []
        for i, r in enumerate(pool.imap_unordered(tarea, tr, chunksize=1), 1):
            res.append(r)
            if i % 20 == 0 or i == len(tr):
                log(f"          {i}/{len(tr)}")
    log("ETAPA 3/3 — analisis.")
    G = lambda b: {r['seed']: r for r in res if r['brazo'] == b}
    ac = lambda r: (r['tel']['acierto'] if r['tel']['acierto'] is not None else 0.5)
    for b in BRAZOS:
        g = list(G(b).values())
        a = [ac(r) for r in g]
        log(f"   {b:9s} acierto {med(a)[0]:.3f} [{med(a)[1]:.2f},{med(a)[2]:.2f}]  >0.60 en {sum(x > 0.6 for x in a)}/20  sin_mover {med([r['tel']['sin_mover'] for r in g])[0]:.0f}/40"
            f"  ciego {med([r['tel']['ciego_al_llegar'] for r in g])[0]:.0f}/40  M_llenas {med([r['M_llenas'] for r in g])[0]:.0f}"
            f"  comida_q4 {med([r['mord']['A'][3] for r in g])[0]:.0f}  muertes {med([r['deaths'] for r in g])[0]:.0f}  W {G(b)[SEEDS[0]]['W']}")
    mapa, sinm, cong, bar, sinc, inv = (G(b) for b in BRAZOS)
    am = [ac(mapa[s]) for s in SEEDS]
    P1 = med(am)[0] >= 0.75 and sum(x > 0.6 for x in am) >= 15
    C1 = 0.40 <= med([ac(cong[s]) for s in SEEDS])[0] <= 0.60 and all(cong[s]['M_llenas'] == 0 for s in SEEDS)
    C2 = med([ac(bar[s]) for s in SEEDS])[0] <= 0.60
    C3 = 0.40 <= med([ac(sinc[s]) for s in SEEDS])[0] <= 0.60
    C4 = 0.40 <= med([ac(sinm[s]) for s in SEEDS])[0] <= 0.60
    C5 = med([ac(inv[s]) for s in SEEDS])[0] <= 0.40   # enmienda 1: con el valor invertido debe HUIR de la comida recordada
    f1n = sum(mapa[s]['mord']['A'][3] > sinm[s]['mord']['A'][3] for s in SEEDS); F1 = f1n >= 15
    V.update(P1=P1, C1=C1, C2=C2, C3=C3, C4=C4, C5=C5, F1=F1, F1_n=f1n, ELIGE=bool(P1 and C1 and C3 and C4 and C5), C2_informativo=C2)
    log(f"   P1 MAPA>=.75 {'OK' if P1 else 'NO'} | C1 CONGELADA {'OK' if C1 else 'NO'} | C2 BARAJADO<=.60 {'OK' if C2 else 'NO (no decisivo, enmienda 1)'} | C3 SINCOMIDA {'OK' if C3 else 'NO'}"
        f" | C4 SINMAPA {'OK' if C4 else 'NO'} | C5 INVERTIDO<=.40 {'OK' if C5 else 'NO'} | F1 comida_q4 MAPA>SINMAPA en {f1n}/20 {'OK' if F1 else 'NO'}")
    log(f"VEREDICTO mapa: {'ELIGE la direccion hacia comida recordada' if V['ELIGE'] else 'NO (refutado o control caido)'}; funcional F1 {'OK' if F1 else 'NO'}")
    meta = dict(fecha=time.strftime('%Y-%m-%dT%H:%M:%S'), semillas=SEEDS, mundo=MUNDO, brazos=BRAZOS, veredictos=V, identidades=rc, procesos_python=ps,
                sha_preregistro=h16(pre), sha_script=h16(os.path.abspath(__file__)), sha_mundo=h16(os.path.join(AQUI, 'mundo_mapa.py')),
                python=platform.python_version(), numpy=np.__version__)
    dj = os.path.join(RAIZ, 'datos', f'mapa_s{SEEDS[0]}-{SEEDS[-1]}_{stamp}.json')
    json.dump(dict(meta=meta, corridas=res), open(dj, 'w', encoding='utf-8'), ensure_ascii=False, default=str)
    log(f"datos -> {os.path.basename(dj)}  sha256_16 = {h16(dj)}")
    _log['f'].close()
