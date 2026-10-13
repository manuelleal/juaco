"""v12: SUPERFICIE del canje (seis beta, todos se reportan) + RAMA hija-madura (dos umbrales). Ejecuta
PREREGISTRO_v12.md con sus ENMIENDAS 1 y 2. REGLA 10: log desde el arranque. REGLA 11: procesos vivos.

Medidas, todas ya preregistradas antes en sus experimentos:
- retencion  = bloque M (fases 50k C/D, 100k vuelven A/B; T=150k): W_B(100k)<=-2 Y W_A(100k)>=0.5
- guarda     = W_C(100k)<=-2.5 y W_D(100k)>=0.85 (no retener por no aprender)
- acierto    = valor a priori sobre patrones NUNCA VISTOS, regla px0 (media balanceada); control azar
- BA_pb      = conducta al primer encuentro
- fuga       = hijas ajenas (indice>=30) en el codigo de un patron de test, de 3
Superficie: semillas 41-60. Rama: semillas 71-80, y si la prediccion se sostiene, retenidas 81-90.
Uso:  python experimentos/v12_ceguera_graduada/corre_v12.py
"""
import sys, os, json, time, hashlib, platform, subprocess
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
import numpy as np

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
sys.path[:0] = [AQUI, os.path.join(RAIZ, 'organismo'), os.path.join(RAIZ, 'experimentos', 'v11_evo_division'),
                os.path.join(RAIZ, 'experimentos', 'v11_generaliza')]
SEEDS = list(range(41, 61))
RAMA = list(range(71, 81)); RAMA_RET = list(range(81, 91))
BETAS = [0.0, 0.15, 0.30, 0.50, 0.75, 1.0]
U_MADURA = [1.0, 0.3]
FASES = {50000: (['C', 'D'], {'C': 'veneno', 'D': 'comida'}), 100000: (['A', 'B'], {'A': 'comida', 'B': 'veneno'})}
ESC_ID = {'BUG': dict(plast=False, solap_AB=3), 'E1': dict(), 'E2': dict(invertir_en=50000), 'E2I': dict(nuevo='C'),
          'E2J': dict(nuevo='D', nuevo_val='comida', solap_B=1), 'E2K': dict(nuevo='D', nuevo_val='comida', solap_B=2),
          'E2L': dict(solap_AB=3)}
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


def kwargs(cond):
    b, mad, u = cond
    return dict(beta=b, madura=mad, u_madura=u)


def tarea(args):
    tipo = args[0]
    if tipo == 'I':
        _, cual, esc, seed = args
        import organismo_v12 as v12
        if cual == 'I1':
            import organismo_v11 as ref
            a, b = ref.run(seed, **ESC_ID[esc]), v12.run(seed, **ESC_ID[esc])
        else:
            import organismo_v10 as ref
            a, b = ref.run(seed, **ESC_ID[esc]), v12.run(seed, div_signo=False, **ESC_ID[esc])
        dif = [k for k in a if N(a[k]) != N(b[k])]
        return dict(tipo=tipo, cual=cual, esc=esc, seed=seed, identico=not dif, difieren=dif)
    if tipo == 'Iinst':
        _, cual, esc, seed = args
        import organismo_v12m as m12, organismo_v12g as g12, organismo_v11m as m11, organismo_v11g as g11
        if cual == 'm':
            kw = dict(T=150000, fases=FASES) if esc == 'M' else ESC_ID[esc]
            a, b = m11.run(seed, **kw), m12.run(seed, **kw)
        else:
            kw = dict(T=200000, mundo='regla', regla=esc)
            a, b = g11.run(seed, **kw), g12.run(seed, **kw)
        dif = [k for k in a if N(a[k]) != N(b[k])]
        return dict(tipo=tipo, cual=cual, esc=esc, seed=seed, identico=not dif, difieren=dif)
    if tipo == 'M':
        _, cond, seed = args
        import organismo_v12m as m
        r = m.run(seed, T=150000, fases=FASES, **kwargs(cond))
        s100 = r['sondas'][100000]
        return dict(tipo='M', cond=cond, seed=seed, W=dict(s100), splits=r['splits'], celdas=r['celdas'],
                    deaths=r['deaths'], congeladas=r.get('congeladas'), t_cong=r.get('t_cong'))
    _, cond, regla, seed = args
    import organismo_v12g as g
    r = g.run(seed, T=200000, mundo='regla', regla=regla, **kwargs(cond))
    vr = g.split_regla(seed, regla)[3]
    test, cod = r['test'], r['codigos_f2']
    f = [1.0 if r['W_apriori'][k] > 0 else (0.5 if r['W_apriori'][k] == 0 else 0.0) for k in test if vr[k] == 'comida']
    p = [1.0 if r['W_apriori'][k] < 0 else (0.5 if r['W_apriori'][k] == 0 else 0.0) for k in test if vr[k] == 'veneno']
    pf = [r['primer'][k]['pb'] for k in test if r['primer'][k] is not None and vr[k] == 'comida']
    pp = [1 - r['primer'][k]['pb'] for k in test if r['primer'][k] is not None and vr[k] == 'veneno']
    return dict(tipo='G', cond=cond, regla=regla, seed=seed,
                acc=0.5 * float(np.mean(f)) + 0.5 * float(np.mean(p)),
                ba=(0.5 * float(np.mean(pf)) + 0.5 * float(np.mean(pp))) if (pf and pp) else None,
                fuga=float(np.mean([sum(i >= 30 for i in cod[k]) / 3 for k in test])),
                splits=r['splits'], celdas=r['celdas'], deaths=r['deaths'], congeladas=r.get('congeladas'))


def rangos(x):
    x = np.asarray(x, float); o = np.argsort(x, kind='mergesort'); r = np.empty(len(x), float); r[o] = np.arange(1, len(x) + 1)
    for v in np.unique(x):
        m = x == v
        if m.sum() > 1:
            r[m] = r[m].mean()
    return r


def spearman(x, y):
    rx, ry = rangos(x), rangos(y)
    return float('nan') if rx.std() == 0 or ry.std() == 0 else float(np.corrcoef(rx, ry)[0, 1])


def fila(res, cond, seeds, etiqueta):
    M = {r['seed']: r for r in res if r['tipo'] == 'M' and r['cond'] == cond and r['seed'] in seeds}
    Gp = {r['seed']: r for r in res if r['tipo'] == 'G' and r['cond'] == cond and r['regla'] == 'px0' and r['seed'] in seeds}
    Ga = {r['seed']: r for r in res if r['tipo'] == 'G' and r['cond'] == cond and r['regla'] == 'azar' and r['seed'] in seeds}
    n = len(seeds)
    ret = sum(M[s]['W']['B'] <= -2 and M[s]['W']['A'] >= 0.5 for s in seeds)
    guar = sum(M[s]['W']['C'] <= -2.5 and M[s]['W']['D'] >= 0.85 for s in seeds)
    acc = float(np.median([Gp[s]['acc'] for s in seeds])); az = float(np.median([Ga[s]['acc'] for s in seeds]))
    ba = [Gp[s]['ba'] for s in seeds if Gp[s]['ba'] is not None]
    fug = float(np.median([Gp[s]['fuga'] for s in seeds]))
    return dict(etiqueta=etiqueta, cond=list(cond), n=n, retencion=ret, guarda=guar, acc=acc, acc_min=float(min(Gp[s]['acc'] for s in seeds)),
                acc_max=float(max(Gp[s]['acc'] for s in seeds)), azar=az, ba=float(np.median(ba)) if ba else None, fuga=fug,
                splits=float(np.median([M[s]['splits'] for s in seeds])), celdas=float(np.median([M[s]['celdas'] for s in seeds])),
                deaths=float(np.median([M[s]['deaths'] for s in seeds])),
                congeladas=float(np.median([M[s]['congeladas'] or 0 for s in seeds])), seeds=f"{seeds[0]}-{seeds[-1]}")


if __name__ == '__main__':
    import multiprocessing as mp
    mp.set_start_method('spawn', force=True)
    stamp = time.strftime('%Y%m%d_%H%M%S')
    _log['f'] = open(os.path.join(RAIZ, 'datos', f'v12_superficie_{stamp}.log'), 'w', encoding='utf-8', newline='\n')
    pre = os.path.join(AQUI, 'PREREGISTRO_v12.md')
    shas = {n_: h16(p) for n_, p in [('preregistro', pre), ('script', os.path.abspath(__file__)),
            ('v12', os.path.join(AQUI, 'organismo_v12.py')), ('v12m', os.path.join(AQUI, 'organismo_v12m.py')),
            ('v12g', os.path.join(AQUI, 'organismo_v12g.py')), ('v11', os.path.join(RAIZ, 'organismo', 'organismo_v11.py'))]}
    log(f"ARRANQUE v12: superficie del canje ({len(BETAS)} betas, semillas {SEEDS[0]}-{SEEDS[-1]}) + rama hija-madura "
        f"(u en {U_MADURA}, semillas {RAMA[0]}-{RAMA[-1]}). Pool({N_PARALELO}).")
    log("sha " + "  ".join(f"{k} {v}" for k, v in shas.items()))
    try:
        ps = subprocess.run(['powershell', '-NoProfile', '-Command',
                             "Get-CimInstance Win32_Process | Where-Object { $_.Name -like 'python*' } | ForEach-Object { \"$($_.ProcessId) $($_.CommandLine)\" }"],
                            capture_output=True, text=True, timeout=60).stdout.strip().splitlines()
    except Exception as e:
        ps = [f"(no se pudo listar: {e})"]
    log(f"REGLA 11 — procesos python vivos ({len(ps)}), este es pid {os.getpid()}")
    V = {}
    with mp.Pool(N_PARALELO) as pool:
        ctrl = ([('I', 'I1', e, s) for e in ESC_ID for s in (1, 2, 3)] + [('I', 'I2', e, s) for e in ESC_ID for s in (1, 2, 3)]
                + [('Iinst', 'm', e, s) for e in ('E1', 'E2', 'M') for s in (1, 2, 3)]
                + [('Iinst', 'g', e, s) for e in ('px0', 'azar') for s in (1, 2, 3)])
        log(f"ETAPA 1/4 — controles de inercia ({len(ctrl)})...")
        rc = pool.map(tarea, ctrl, chunksize=1)
        for cual, nombre in (('I1', 'I1  v12(beta=0) == v11'), ('I2', 'I2  v12(div_signo=False) == v10'),
                             ('m', '    v12m == v11m'), ('g', '    v12g == v11g')):
            g = [x for x in rc if x.get('cual') == cual]
            log(f"  {nombre:32s}: {sum(x['identico'] for x in g)}/{len(g)}")
            for x in g:
                if not x['identico']:
                    log(f"      DIFIERE {x['esc']} s{x['seed']}: {x['difieren']}")
        V['INERCIA'] = all(x['identico'] for x in rc)
        if not V['INERCIA']:
            log("*** CONTROL DE INERCIA FALLIDO: se para y se arregla el instrumento (lo pidio direccion)."); sys.exit(1)
        log("  Controles de inercia OK. Recien ahora se miran los puntos intermedios.")
        CONDS_S = [(b, False, 1.0) for b in BETAS]
        CONDS_R = [(1.0, True, u) for u in U_MADURA]
        trabajos = ([('M', c, s) for c in CONDS_S for s in SEEDS] + [('G', c, rg, s) for c in CONDS_S for rg in ('px0', 'azar') for s in SEEDS]
                    + [('M', c, s) for c in CONDS_R for s in RAMA] + [('G', c, rg, s) for c in CONDS_R for rg in ('px0', 'azar') for s in RAMA])
        log(f"ETAPA 2/4 — {len(trabajos)} corridas (superficie + rama)...")
        res = []
        for i, r in enumerate(pool.imap_unordered(tarea, trabajos, chunksize=1), 1):
            res.append(r)
            if i % 30 == 0 or i == len(trabajos):
                log(f"          {i}/{len(trabajos)}")
        filas = [fila(res, c, SEEDS, f"beta={c[0]:.2f}") for c in CONDS_S] + [fila(res, c, RAMA, f"rama u={c[2]}") for c in CONDS_R]
        # rama: si la prediccion se sostiene, re-medir en semillas retenidas
        rama_ok = [c for c in CONDS_R if (lambda f: f['retencion'] >= 8 and f['acc'] >= 0.75)(fila(res, c, RAMA, ''))]
        if rama_ok:
            log(f"ETAPA 3/4 — la rama se sostiene en {len(rama_ok)} punto(s): re-medida en semillas RETENIDAS {RAMA_RET[0]}-{RAMA_RET[-1]}...")
            tr2 = ([('M', c, s) for c in rama_ok for s in RAMA_RET] + [('G', c, rg, s) for c in rama_ok for rg in ('px0', 'azar') for s in RAMA_RET])
            for i, r in enumerate(pool.imap_unordered(tarea, tr2, chunksize=1), 1):
                res.append(r)
            filas += [fila(res, c, RAMA_RET, f"rama u={c[2]} RETENIDAS") for c in rama_ok]
        else:
            log("ETAPA 3/4 — la rama no alcanza su prediccion en 71-80: no se tocan las semillas retenidas.")
    log()
    log("  TABLA UNICA (retencion = W_B<=-2 y W_A>=0.5; acierto = valor en patrones nunca vistos; fuga = hijas ajenas de 3)")
    log(f"  {'condicion':22s} {'semillas':10s} {'retencion':10s} {'guarda':7s} {'acierto':16s} {'azar':6s} {'conducta':9s} {'fuga':6s} {'div':5s} {'celdas':7s} {'muertes':8s} {'congel':6s}")
    for f in filas:
        log(f"  {f['etiqueta']:22s} {f['seeds']:10s} {f['retencion']:>3d}/{f['n']:<6d} {f['guarda']:>3d}/{f['n']:<3d} "
            f"{f['acc']:.3f} [{f['acc_min']:.2f},{f['acc_max']:.2f}] {f['azar']:.3f}  {(f['ba'] if f['ba'] is not None else float('nan')):.3f}     "
            f"{f['fuga']:.2f}   {f['splits']:>4.0f}  {f['celdas']:>5.0f}   {f['deaths']:>6.0f}   {f['congeladas']:>4.0f}")
    sup = filas[:len(BETAS)]
    V['H_canje'] = not any(f['retencion'] >= 20 and f['acc'] >= 0.78 for f in sup)
    rho = spearman(BETAS, [f['fuga'] for f in sup])
    V['GUARDA_perilla'] = rho >= 0.9
    log()
    log(f"  GUARDA: Spearman(beta, fuga) = {rho:+.3f} (>=+0.9): {'OK' if V['GUARDA_perilla'] else 'FALLA — la perilla no manipula lo que dice'}")
    log(f"  H [el canje existe]: ningun beta con retencion 20/20 Y acierto >=0.78 -> {'SOSTENIDA' if V['H_canje'] else 'REFUTADA'}")
    if not V['H_canje']:
        for f in sup:
            if f['retencion'] >= 20 and f['acc'] >= 0.78:
                log(f"      *** PUNTO QUE ROMPE EL CANJE: {f['etiqueta']} (retencion {f['retencion']}/20, acierto {f['acc']:.3f})")
    for f in filas[len(BETAS):]:
        ok = f['retencion'] >= 0.8 * f['n'] and f['acc'] >= 0.75
        ref = f['retencion'] < 0.6 * f['n'] or f['acc'] < 0.70
        log(f"  RAMA {f['etiqueta']:24s}: retencion {f['retencion']}/{f['n']}, acierto {f['acc']:.3f} -> "
            f"{'SOSTENIDA' if ok else ('REFUTADA' if ref else 'ni sostenida ni refutada (zona muerta declarada)')}")
    log(); log("VEREDICTO v12: " + " ".join(f"{k}={v}" for k, v in V.items()))
    log("ETAPA 4/4 — escritura.")
    meta = dict(fecha=time.strftime('%Y-%m-%dT%H:%M:%S'), betas=BETAS, u_madura=U_MADURA, semillas=SEEDS, rama=RAMA,
                rama_retenidas=RAMA_RET, veredictos=V, spearman_beta_fuga=rho, filas=filas, shas=shas, procesos_python=ps,
                python=platform.python_version(), numpy=np.__version__)
    dj = os.path.join(RAIZ, 'datos', f'v12_superficie_{stamp}.json')
    json.dump(dict(meta=meta, identidades=rc, corridas=res), open(dj, 'w', encoding='utf-8'), ensure_ascii=False, default=str)
    log(f"datos -> {os.path.basename(dj)}  sha256_16 = {h16(dj)}")
    _log['f'].close()
