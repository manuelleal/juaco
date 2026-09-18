"""Etapa 5 N3 (sentidos complementarios) = experimento 3 del plan. Ejecuta PREREGISTRO_N3.md.
REGLA 10: log desde el arranque. Identidad: mundo_social_n3 con gamma_soc=0 y sin mascaras == mundo_social (todas las claves).
Uso:  python experimentos/etapa5_comunicacion/corre_N3.py [--desde N]
"""
import sys, os, json, time, hashlib, platform, subprocess
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
import numpy as np

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
sys.path[:0] = [AQUI, os.path.join(RAIZ, 'organismo')]
_desde = int(sys.argv[sys.argv.index('--desde') + 1]) if '--desde' in sys.argv else 1
SEEDS = list(range(_desde, _desde + 20))
MR = [0, 0, 0, 1, 1, 1.]; ME = [1, 1, 1, 0, 0, 0.]
BASE = dict(T=200000, mundo='regla', regla='px0', d_senal=5, f_vicaria=1 / 3)
COND = {
    'TECHO':    dict(n=1),
    'SOLO_E':   dict(n=1, mascaras=[ME]),
    'SOLO_R':   dict(n=1, mascaras=[MR]),
    'N0':       dict(n=2, mascaras=[MR, ME]),
    'CONV':     dict(n=2, mascaras=[MR, ME], senal='conducta', gamma_soc=1.5),
    'SHUF':     dict(n=2, mascaras=[MR, ME], senal='barajada_conducta', gamma_soc=1.5),
    'SACIEDAD': dict(n=2, mascaras=[MR, ME], senal='conducta', gamma_soc=1.5, kw_por_org=[{}, dict(alpha=0.0)]),
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


def acierto_q4(r, val):
    ok = sum(r['mord'][k][3] if val[k] == 'comida' else r['vis'][k][3] - r['mord'][k][3] for k in r['vis'])
    tot = sum(r['vis'][k][3] for k in r['vis'])
    return (ok / tot) if tot else None


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
    kw = dict(BASE); kw.update(COND[cond])
    out = m.run(seed, **kw)
    r = out[0]
    ven = sum(r['mord'][k][3] for k in r['mord'] if val[k] == 'veneno')
    return dict(tipo='T', cond=cond, seed=seed, acierto=acierto_q4(r, val), veneno_q4=ven, deaths=r['deaths'], n_sesgo=r.get('n_sesgo_soc', 0),
                recibidas=r.get('senales_recibidas', 0), emisor_acierto=(acierto_q4(out[1], val) if len(out) > 1 else None),
                W_lenta=r['W_lenta'] if 'W_lenta' in r else None)


def med(xs):
    xs = [x for x in xs if x is not None]
    return float(np.median(xs)), float(min(xs)), float(max(xs))


if __name__ == '__main__':
    import multiprocessing as mp
    mp.set_start_method('spawn', force=True)
    stamp = time.strftime('%Y%m%d_%H%M%S')
    _log['f'] = open(os.path.join(RAIZ, 'datos', f'N3_s{SEEDS[0]}-{SEEDS[-1]}_{stamp}.log'), 'w', encoding='utf-8', newline='\n')
    pre = os.path.join(AQUI, 'PREREGISTRO_N3.md')
    log(f"ARRANQUE N3 (sentidos complementarios) sobre v13. condiciones {list(COND)}, semillas {SEEDS[0]}-{SEEDS[-1]}. Pool({N_PARALELO}).")
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
        log(f"ETAPA 1/3 — identidad gamma_soc=0 sin mascaras == mundo_social ({len(ctrl)})...")
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
    log("ETAPA 3/3 — analisis (receptor = organismo 0, ultimo cuarto).")
    G = lambda c: {r['seed']: r for r in res if r['cond'] == c}
    A = lambda c, s: (G(c)[s]['acierto'] if G(c)[s]['acierto'] is not None else 0.0)
    for c in COND:
        g = list(G(c).values())
        log(f"   {c:9s} acierto {med([r['acierto'] for r in g])[0]:.3f} [{med([r['acierto'] for r in g])[1]:.2f},{med([r['acierto'] for r in g])[2]:.2f}]"
            f"  veneno_q4 {med([r['veneno_q4'] for r in g])[0]:.0f}  muertes {med([r['deaths'] for r in g])[0]:.0f}  sesgos {med([r['n_sesgo'] for r in g])[0]:.0f}"
            f"  recibidas {med([r['recibidas'] for r in g])[0]:.0f}  emisor {med([r['emisor_acierto'] for r in g])[0] if g[0]['emisor_acierto'] is not None else float('nan'):.3f}")
    par = lambda c1, c2: sum(A(c1, s) > A(c2, s) for s in SEEDS)
    S1 = med([A('CONV', s) for s in SEEDS])[0] >= 0.80 and par('CONV', 'SOLO_R') >= 15
    S2 = par('CONV', 'SHUF') >= 15
    S3 = par('CONV', 'SACIEDAD') >= 15
    S4 = med([A('SOLO_R', s) for s in SEEDS])[0] <= 0.75 and med([A('TECHO', s) for s in SEEDS])[0] >= 0.80 and med([A('SOLO_E', s) for s in SEEDS])[0] >= 0.80
    S5 = par('N0', 'SOLO_R') < 15
    V.update(S1=S1, S2=S2, S3=S3, S4=S4, S5=S5, pareados=dict(conv_solo=par('CONV', 'SOLO_R'), conv_shuf=par('CONV', 'SHUF'), conv_sac=par('CONV', 'SACIEDAD'), n0_solo=par('N0', 'SOLO_R')),
             TRANSFIERE=bool(S1 and S2 and S3 and S4 and S5))
    log(f"   S1 CONV>=.80 y >SOLO_R en {V['pareados']['conv_solo']}/20 {'OK' if S1 else 'NO'} | S2 >SHUF en {V['pareados']['conv_shuf']}/20 {'OK' if S2 else 'NO'}"
        f" | S3 >SACIEDAD en {V['pareados']['conv_sac']}/20 {'OK' if S3 else 'NO'} | S4 validez {'OK' if S4 else 'NO'} | S5 N0>SOLO_R en {V['pareados']['n0_solo']}/20 {'OK' if S5 else 'NO'}")
    log(f"VEREDICTO N3: {'TRANSFIERE entre sensores por conducta' if V['TRANSFIERE'] else 'NO (refutado o montaje invalido)'}")
    meta = dict(fecha=time.strftime('%Y-%m-%dT%H:%M:%S'), semillas=SEEDS, base=BASE, condiciones=N(COND), veredictos=V, identidades=rc, procesos_python=ps,
                sha_preregistro=h16(pre), sha_script=h16(os.path.abspath(__file__)), sha_mundo=h16(os.path.join(AQUI, 'mundo_social_n3.py')),
                python=platform.python_version(), numpy=np.__version__)
    dj = os.path.join(RAIZ, 'datos', f'N3_s{SEEDS[0]}-{SEEDS[-1]}_{stamp}.json')
    json.dump(dict(meta=meta, corridas=res), open(dj, 'w', encoding='utf-8'), ensure_ascii=False, default=str)
    log(f"datos -> {os.path.basename(dj)}  sha256_16 = {h16(dj)}")
    _log['f'].close()
