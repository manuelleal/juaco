"""Niveles 8+9, experimento 4 del plan: mundo largo con novedad (50 patrones) y cambio de regla en t=100000; v13 contra
v13+mapa, con control de novedad reciclada. Ejecuta PREREGISTRO_mundo_largo.md. REGLA 10: log desde el arranque.
Identidad: mundo_largo con pool=None == mundo_mapa (todas las claves).
Uso:  python experimentos/nivel8_mundo_largo/corre_mundo_largo.py [--desde N]
"""
import sys, os, json, time, hashlib, platform, subprocess, itertools
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
import numpy as np

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
sys.path[:0] = [AQUI, os.path.join(RAIZ, 'experimentos', 'nivel6_mapa'), os.path.join(RAIZ, 'organismo')]
_desde = int(sys.argv[sys.argv.index('--desde') + 1]) if '--desde' in sys.argv else 1
SEEDS = list(range(_desde, _desde + 20))
T = 200000; T_NUEVO = 4000; T_INV = 100000
BRAZOS = {
    'V13':       dict(usa_M=False),
    'MAPA':      dict(usa_M=True),
    'REC_V13':   dict(usa_M=False, reciclado=True),
    'REC_MAPA':  dict(usa_M=True, reciclado=True),
}
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


def pool_de(seed):
    """50 patrones (peso 2, 3 y 4 sobre 6 px), valencias al azar 25/25 con RNG propio. Nombres = cadena de bits."""
    pats = []
    for w in (2, 3, 4):
        for combo in itertools.combinations(range(6), w):
            v = np.zeros(6); v[list(combo)] = 1.
            pats.append((''.join('1' if v[j] else '0' for j in range(6)), v))
    r0 = np.random.default_rng(30000 + seed); perm = r0.permutation(len(pats))
    com = set(pats[i][0] for i in perm[:25])
    return [(n, v, 'comida' if n in com else 'veneno') for n, v in pats]


def sitios_de(pool, seed):
    """4 patrones iniciales (2 comida, 2 veneno) de PESO 3, cada uno en dos sitios, intercalados."""
    r1 = np.random.default_rng(40000 + seed)
    f = [n for n, v, vl in pool if vl == 'comida' and n.count('1') == 3]; p = [n for n, v, vl in pool if vl == 'veneno' and n.count('1') == 3]
    f = [f[i] for i in r1.permutation(len(f))[:2]]; p = [p[i] for i in r1.permutation(len(p))[:2]]
    return (f[0], p[0], f[1], p[1], f[0], p[0], f[1], p[1])


def recuperacion(cb, db):
    pre = float(np.mean(cb[80:100])); b0 = T_INV // 1000
    rec = None
    for b in range(b0, len(cb) - 3):
        if np.mean(cb[b:b + 3]) >= 0.8 * pre: rec = (b - b0) * 1000; break
    return dict(pre=round(pre, 2), rec=rec if rec is not None else T - T_INV, muertes_20k=int(sum(db[b0:b0 + 20])), rec_hallada=rec is not None)


def tarea(args):
    tipo = args[0]
    if tipo == 'I':
        _, seed = args
        import mundo_mapa as a_, mundo_largo as b_
        kw = dict(r_vis=3, sitios=('A', 'B'), usa_M=True, prueba=dict(n_tel=40))
        a, b = a_.run(seed, **kw), b_.run(seed, **kw)
        dif = [kk for kk in a if N(a[kk]) != N(b[kk])]
        return dict(tipo=tipo, esc='ident', seed=seed, identico=not dif, difieren=dif)
    _, brazo, seed = args
    import mundo_largo as m
    pool = pool_de(seed)
    kw = dict(T=T, r_vis=3, sitios=sitios_de(pool, seed), pool=pool, T_nuevo=T_NUEVO, invertir_largo=T_INV); kw.update(BRAZOS[brazo])
    r = m.run(seed, **kw)
    cv = r['curva']
    hasta30 = [c[2] for c in cv if c[1] <= 30]; fin = cv[-1] if cv else (None, None, None, None)
    return dict(tipo='T', brazo=brazo, seed=seed, curva=cv, n_vistos=len(r['vistos']), adq_hasta30=float(np.median(hasta30)) if hasta30 else None,
                adq_final=fin[2], ret_final=fin[3], deaths=r['deaths'], celdas=r['celdas'], splits=r['splits'], **recuperacion(r['comida_bin'], r['muertes_bin']))


def med(xs):
    xs = [x for x in xs if x is not None]
    return float(np.median(xs)), float(min(xs)), float(max(xs))


if __name__ == '__main__':
    import multiprocessing as mp
    mp.set_start_method('spawn', force=True)
    stamp = time.strftime('%Y%m%d_%H%M%S')
    _log['f'] = open(os.path.join(RAIZ, 'datos', f'largo_s{SEEDS[0]}-{SEEDS[-1]}_{stamp}.log'), 'w', encoding='utf-8', newline='\n')
    pre = os.path.join(AQUI, 'PREREGISTRO_mundo_largo.md')
    log(f"ARRANQUE mundo largo (niveles 8+9) sobre v13. brazos {list(BRAZOS)}, semillas {SEEDS[0]}-{SEEDS[-1]}, T={T}, T_nuevo={T_NUEVO}, inversion en {T_INV}. Pool({N_PARALELO}).")
    log(f"sha preregistro {h16(pre)}  script {h16(os.path.abspath(__file__))}  mundo_largo {h16(os.path.join(AQUI, 'mundo_largo.py'))}  mundo_mapa {h16(os.path.join(RAIZ, 'experimentos', 'nivel6_mapa', 'mundo_mapa.py'))}  v13 {h16(os.path.join(RAIZ, 'organismo', 'organismo_v13.py'))}")
    try:
        ps = subprocess.run(['powershell', '-NoProfile', '-Command',
                             "Get-CimInstance Win32_Process | Where-Object { $_.Name -like 'python*' } | ForEach-Object { \"$($_.ProcessId) $($_.CommandLine)\" }"],
                            capture_output=True, text=True, timeout=60).stdout.strip().splitlines()
    except Exception as e:
        ps = [f"(no se pudo listar: {e})"]
    log(f"REGLA 11 — procesos python vivos ({len(ps)}), este es pid {os.getpid()}")
    V = {}
    with mp.Pool(N_PARALELO) as pool:
        ctrl = [('I', s) for s in (1, 2, 3)]
        log(f"ETAPA 1/3 — identidad pool=None == mundo_mapa ({len(ctrl)})...")
        rc = pool.map(tarea, ctrl, chunksize=1)
        log(f"  identicos: {sum(x['identico'] for x in rc)}/{len(rc)}")
        for x in rc:
            if not x['identico']: log(f"      DIFIERE {x['esc']} s{x['seed']}: {x['difieren']}")
        V['IDENTIDAD'] = all(x['identico'] for x in rc)
        if not V['IDENTIDAD']:
            log("*** IDENTIDAD FALLIDA: se para."); sys.exit(1)
        tr = [('T', b, s) for b in BRAZOS for s in SEEDS]
        log(f"ETAPA 2/3 — {len(tr)} corridas...")
        res = []
        for i, r in enumerate(pool.imap_unordered(tarea, tr, chunksize=1), 1):
            res.append(r)
            if i % 20 == 0 or i == len(tr):
                log(f"          {i}/{len(tr)}")
    log("ETAPA 3/3 — analisis.")
    G = lambda b: {r['seed']: r for r in res if r['brazo'] == b}
    for b in BRAZOS:
        g = list(G(b).values())
        log(f"   {b:9s} vistos {med([r['n_vistos'] for r in g])[0]:.0f}  adq(<=30) {med([r['adq_hasta30'] for r in g])[0]:.3f}  adq(final) {med([r['adq_final'] for r in g])[0]:.3f}"
            f"  ret(final) {med([r['ret_final'] for r in g])[0]:.3f}  recup {med([r['rec'] for r in g])[0]:.0f} [{med([r['rec'] for r in g])[1]:.0f},{med([r['rec'] for r in g])[2]:.0f}]"
            f"  hallada {sum(r['rec_hallada'] for r in g)}/20  muertes_20k {med([r['muertes_20k'] for r in g])[0]:.0f}  muertes {med([r['deaths'] for r in g])[0]:.0f}  celdas {med([r['celdas'] for r in g])[0]:.0f}")
    # curva media de adquisicion por numero de patrones vistos (V13 y MAPA)
    for b in ('V13', 'MAPA'):
        pts = {}
        for r in G(b).values():
            for t_, nv, a_, p_ in r['curva']: pts.setdefault(nv, []).append(a_)
        log(f"   curva {b}: " + " ".join(f"{nv}:{np.median(v):.2f}" for nv, v in sorted(pts.items()) if nv % 5 == 0 or nv == 50))
    v13, mapa, rv, rm = (G(b) for b in BRAZOS)
    A1 = all(med([g[s]['adq_hasta30'] for s in SEEDS])[0] >= 0.75 for g in (v13, mapa))
    A2 = all(0.55 <= med([g[s]['adq_final'] for s in SEEDS])[0] <= 0.70 for g in (v13, mapa))
    A3 = all(med([g[s]['adq_final'] for s in SEEDS])[0] >= 0.85 for g in (rv, rm))
    R1 = all(med([g[s]['ret_final'] for s in SEEDS])[0] >= 0.70 for g in (v13, mapa))
    c1n = sum(v13[s]['rec'] <= 10000 for s in SEEDS); C1 = c1n >= 15
    c2a = sum(mapa[s]['rec'] < v13[s]['rec'] for s in SEEDS); c2b = sum(mapa[s]['muertes_20k'] > v13[s]['muertes_20k'] for s in SEEDS)
    C2 = c2a >= 15 and c2b >= 15
    V.update(A1=A1, A2=A2, A3=A3, R1=R1, C1=C1, C1_n=c1n, C2=C2, C2_rec=c2a, C2_muertes=c2b, SIGUE_Y_SE_RECUPERA=bool(A1 and C1))
    log(f"   A1 adq<=30 >=.75 {'OK' if A1 else 'NO'} | A2 adq final en [.55,.70] {'OK' if A2 else 'NO'} | A3 reciclado >=.85 {'OK' if A3 else 'NO'} | R1 retencion >=.70 {'OK' if R1 else 'NO'}"
        f" | C1 V13 recupera <=10k en {c1n}/20 {'OK' if C1 else 'NO'} | C2 MAPA recupera antes {c2a}/20 y muere mas {c2b}/20 {'OK' if C2 else 'NO'}")
    log(f"VEREDICTO largo: {'SIGUE APRENDIENDO y SE RECUPERA' if V['SIGUE_Y_SE_RECUPERA'] else 'NO'}; predicciones A2 {'OK' if A2 else 'NO'} A3 {'OK' if A3 else 'NO'} R1 {'OK' if R1 else 'NO'} C2 {'OK' if C2 else 'NO'}")
    meta = dict(fecha=time.strftime('%Y-%m-%dT%H:%M:%S'), semillas=SEEDS, T=T, T_nuevo=T_NUEVO, T_inv=T_INV, brazos=BRAZOS, veredictos=V, identidades=rc, procesos_python=ps,
                sha_preregistro=h16(pre), sha_script=h16(os.path.abspath(__file__)), sha_mundo=h16(os.path.join(AQUI, 'mundo_largo.py')),
                python=platform.python_version(), numpy=np.__version__)
    dj = os.path.join(RAIZ, 'datos', f'largo_s{SEEDS[0]}-{SEEDS[-1]}_{stamp}.json')
    json.dump(dict(meta=meta, corridas=res), open(dj, 'w', encoding='utf-8'), ensure_ascii=False, default=str)
    log(f"datos -> {os.path.basename(dj)}  sha256_16 = {h16(dj)}")
    _log['f'].close()
