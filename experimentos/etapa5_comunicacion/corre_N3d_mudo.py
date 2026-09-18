"""N3d MUDO: el receptor ciego por construccion, sin el emisor desde 150000 (mudo_desde). Ejecuta PREREGISTRO_N3d_mudo.md.
Mismo mundo que N3d (4 parejas misma vista 3-5 / valencia opuesta, regen=50, acierto balanceado, solo el receptor escucha).
REGLA 10: log desde el arranque. Identidad: mudo_desde=None == mundo_social (gamma_soc=0, sin mascaras), todas las claves.
Uso:  python experimentos/etapa5_comunicacion/corre_N3d_mudo.py [--desde N]   (por defecto semillas 61-80, las de N3d)
"""
import sys, os, json, time, hashlib, platform, subprocess
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
import numpy as np

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
sys.path[:0] = [AQUI, os.path.join(RAIZ, 'organismo')]
_desde = int(sys.argv[sys.argv.index('--desde') + 1]) if '--desde' in sys.argv else 61
SEEDS = list(range(_desde, _desde + 20))
MR = [0, 0, 0, 1, 1, 1.]; ME = [1, 1, 1, 0, 0, 0.]
BASE = dict(T=200000, mundo='regla', regla='px0', d_senal=5, f_vicaria=1 / 3, regen=50)
COND = {
    'SOLO_R':    dict(n=1, mascaras=[MR]),
    'CONV':      dict(n=2, mascaras=[MR, ME], senal='conducta', kw_por_org=[dict(gamma_soc=1.5), dict(escucha=False)]),
    'CONV_MUDO': dict(n=2, mascaras=[MR, ME], senal='conducta', kw_por_org=[dict(gamma_soc=1.5), dict(escucha=False)], mudo_desde=150000),
}
IDENT = [dict(n=1, T=60000, mundo='regla', regla='px0'), dict(n=2, T=60000, mundo='regla', regla='px0', senal='conducta')]
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


def parejas(seed, val):
    """N3d: 4 vistas de px3-5 (una o dos activas) elegidas al azar; por vista un patron comida (px0=1) y uno veneno (px0=0) de peso 3."""
    r = np.random.default_rng(50000 + seed)
    vistas = ['100', '010', '001', '110', '101', '011']
    vistas = [vistas[i] for i in r.permutation(6)[:4]]
    tipos = []
    for v in vistas:
        cand_c = [k for k in val if k[3:] == v and val[k] == 'comida']; cand_v = [k for k in val if k[3:] == v and val[k] == 'veneno']
        tipos.append(cand_c[int(r.integers(len(cand_c)))]); tipos.append(cand_v[int(r.integers(len(cand_v)))])
    return tipos


def acierto_q4(r, val):   # BALANCEADO (rechazarlo todo o morderlo todo = 0.50)
    vc = sum(r['vis'][k][3] for k in r['vis'] if val[k] == 'comida'); mc = sum(r['mord'][k][3] for k in r['vis'] if val[k] == 'comida')
    vv = sum(r['vis'][k][3] for k in r['vis'] if val[k] == 'veneno'); mv = sum(r['mord'][k][3] for k in r['vis'] if val[k] == 'veneno')
    partes = ([mc / vc] if vc else []) + ([(vv - mv) / vv] if vv else [])
    return (sum(partes) / len(partes)) if partes else None


def tarea(args):
    tipo = args[0]
    if tipo == 'I':
        _, i, seed = args
        import mundo_social as a_, mundo_social_n3 as b_
        a, b = a_.run(seed, **IDENT[i]), b_.run(seed, **IDENT[i])
        dif = [(j, kk) for j in range(len(a)) for kk in a[j] if N(a[j][kk]) != N(b[j][kk])]
        return dict(tipo=tipo, esc=f'ident{i}', seed=seed, identico=not dif, difieren=dif)
    _, cond, seed = args
    import mundo_social_n3 as m
    sys.path.insert(0, os.path.join(RAIZ, 'experimentos', 'v13_dos_vias'))
    from organismo_v13g import split_regla
    _, _, _, val = split_regla(seed, 'px0')
    kw = dict(BASE); kw.update(COND[cond]); kw['tipos_fijos'] = parejas(seed, val)
    out = m.run(seed, **kw)
    r = out[0]
    ven = sum(r['mord'][k][3] for k in r['mord'] if val[k] == 'veneno')
    return dict(tipo='T', cond=cond, seed=seed, acierto=acierto_q4(r, val), veneno_q4=ven, deaths=r['deaths'], n_sesgo=r.get('n_sesgo_soc', 0),
                recibidas=r.get('senales_recibidas', 0), emisor_acierto=(acierto_q4(out[1], val) if len(out) > 1 else None))


def med(xs):
    xs = [x for x in xs if x is not None]
    return float(np.median(xs)), float(min(xs)), float(max(xs))


if __name__ == '__main__':
    import multiprocessing as mp
    mp.set_start_method('spawn', force=True)
    stamp = time.strftime('%Y%m%d_%H%M%S')
    _log['f'] = open(os.path.join(RAIZ, 'datos', f'N3dmudo_s{SEEDS[0]}-{SEEDS[-1]}_{stamp}.log'), 'w', encoding='utf-8', newline='\n')
    pre = os.path.join(AQUI, 'PREREGISTRO_N3d_mudo.md')
    log(f"ARRANQUE N3d MUDO (mudo_desde=150000; receptor ciego por construccion; acierto balanceado en Q4). condiciones {list(COND)}, semillas {SEEDS[0]}-{SEEDS[-1]}. Pool({N_PARALELO}).")
    log(f"sha preregistro {h16(pre)}  script {h16(os.path.abspath(__file__))}  mundo_social_n3 {h16(os.path.join(AQUI, 'mundo_social_n3.py'))}  mundo_social {h16(os.path.join(AQUI, 'mundo_social.py'))}")
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
        log(f"ETAPA 1/3 — identidad mudo_desde=None, gamma_soc=0, sin mascaras == mundo_social ({len(ctrl)})...")
        rc = pool.map(tarea, ctrl, chunksize=1)
        log(f"  identicos: {sum(x['identico'] for x in rc)}/{len(rc)}")
        for x in rc:
            if not x['identico']: log(f"      DIFIERE {x['esc']} s{x['seed']}: {x['difieren'][:6]}")
        V['IDENTIDAD'] = all(x['identico'] for x in rc)
        if not V['IDENTIDAD']:
            log("*** IDENTIDAD FALLIDA: se para."); sys.exit(1)
        tr = [('T', c, s) for c in COND for s in SEEDS]
        log(f"ETAPA 2/3 — {len(tr)} corridas...")
        res = []
        for i, r in enumerate(pool.imap_unordered(tarea, tr, chunksize=1), 1):
            res.append(r)
            if i % 20 == 0 or i == len(tr):
                log(f"          {i}/{len(tr)}")
    log("ETAPA 3/3 — analisis (receptor = organismo 0, ultimo cuarto = 150000-200000).")
    G = lambda c: {r['seed']: r for r in res if r['cond'] == c}
    A = lambda c, s: (G(c)[s]['acierto'] if G(c)[s]['acierto'] is not None else 0.0)
    for c in COND:
        g = list(G(c).values())
        log(f"   {c:9s} acierto {med([r['acierto'] for r in g])[0]:.3f} [{med([r['acierto'] for r in g])[1]:.2f},{med([r['acierto'] for r in g])[2]:.2f}]"
            f"  veneno_q4 {med([r['veneno_q4'] for r in g])[0]:.0f}  muertes {med([r['deaths'] for r in g])[0]:.0f}  sesgos {med([r['n_sesgo'] for r in g])[0]:.0f}"
            f"  recibidas {med([r['recibidas'] for r in g])[0]:.0f}  emisor {med([r['emisor_acierto'] for r in g])[0] if g[0]['emisor_acierto'] is not None else float('nan'):.3f}")
    par = lambda c1, c2: sum(A(c1, s) > A(c2, s) for s in SEEDS)
    mm = med([A('CONV_MUDO', s) for s in SEEDS])[0]; ms = med([A('SOLO_R', s) for s in SEEDS])[0]
    M1 = mm <= 0.60 and par('CONV', 'CONV_MUDO') >= 15
    M2 = abs(mm - ms) < 0.10
    V.update(M1=M1, M2=M2, conv_gt_mudo=par('CONV', 'CONV_MUDO'), mudo_mediana=mm, solo_mediana=ms, OBEDECE=bool(M1 and M2))
    log(f"   M1 MUDO<=.60 y CONV>MUDO en {par('CONV', 'CONV_MUDO')}/20 {'OK' if M1 else 'NO'} | M2 |MUDO-SOLO_R|<.10 ({mm:.3f} vs {ms:.3f}) {'OK' if M2 else 'NO'}")
    log(f"VEREDICTO N3d mudo: {'OBEDECE, no aprende (prediccion cumplida)' if V['OBEDECE'] else 'ANOMALIA: queda algo sin el emisor (buscar la fuga)'}")
    meta = dict(fecha=time.strftime('%Y-%m-%dT%H:%M:%S'), semillas=SEEDS, base=BASE, condiciones=N(COND), veredictos=V, identidades=rc, procesos_python=ps,
                sha_preregistro=h16(pre), sha_script=h16(os.path.abspath(__file__)), sha_mundo=h16(os.path.join(AQUI, 'mundo_social_n3.py')),
                python=platform.python_version(), numpy=np.__version__)
    dj = os.path.join(RAIZ, 'datos', f'N3dmudo_s{SEEDS[0]}-{SEEDS[-1]}_{stamp}.json')
    json.dump(dict(meta=meta, corridas=res), open(dj, 'w', encoding='utf-8'), ensure_ascii=False, default=str)
    log(f"datos -> {os.path.basename(dj)}  sha256_16 = {h16(dj)}")
    _log['f'].close()
