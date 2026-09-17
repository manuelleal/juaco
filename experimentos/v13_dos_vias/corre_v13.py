"""v13 (dos vias): superficie de eta_s (todos los puntos) + confirmatorio automatico del punto que cumpla, en semillas
61-80 que solo decide el. Ejecuta PREREGISTRO_v13.md. REGLA 10: log desde el arranque. REGLA 11: procesos vivos.

Medidas: retencion del bloque M con guarda; acierto px0 / azar / xor01 (valor TOTAL a priori); conducta BA_pb;
E1, E2, E2L con los criterios exactos del criterio v3 (copiados de bateria_v10.CRIT).
Uso:  python experimentos/v13_dos_vias/corre_v13.py
"""
import sys, os, json, time, hashlib, platform, subprocess
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
import numpy as np

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
sys.path[:0] = [AQUI, os.path.join(RAIZ, 'organismo'), os.path.join(RAIZ, 'experimentos', 'v11_evo_division'),
                os.path.join(RAIZ, 'experimentos', 'v11_generaliza')]
SEEDS = list(range(41, 61)); CONF = list(range(61, 81))
ETAS = [0.0, 0.003, 0.006, 0.015, 0.03]
BRAZOS = {'suma': None, 'puerta2': 2, 'puerta3': 3}   # suma = un error compartido; puertaK = cada via su error, la boca consulta la rapida solo si >=K de las 3 celdas del codigo estan consolidadas
FASES = {50000: (['C', 'D'], {'C': 'veneno', 'D': 'comida'}), 100000: (['A', 'B'], {'A': 'comida', 'B': 'veneno'})}
ESC_ID = {'BUG': dict(plast=False, solap_AB=3), 'E1': dict(), 'E2': dict(invertir_en=50000), 'E2I': dict(nuevo='C'),
          'E2J': dict(nuevo='D', nuevo_val='comida', solap_B=1), 'E2K': dict(nuevo='D', nuevo_val='comida', solap_B=2),
          'E2L': dict(solap_AB=3)}
ETAPAS = {'E1': dict(), 'E2': dict(invertir_en=50000), 'E2L': dict(solap_AB=3)}
CRIT = {'E1': lambda r: r['mord']['B'][3] < r['mord']['B'][0] and abs(r['W']['A'] - 1) < .15 and abs(r['W']['B'] + 3) < .3,
        'E2': lambda r: abs(r['W']['A'] + 3) < .3 and abs(r['W']['B'] - 1) < .15 and r['mord']['B'][3] >= 50,
        'E2L': lambda r: abs(r['W']['A'] - 1) < .15 and abs(r['W']['B'] + 3) < .3 and r['solap']['AB'] == 0}
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
    tipo = args[0]
    if tipo == 'I':
        _, cual, esc, seed = args
        if cual == 'v11':
            import organismo_v11 as ref, organismo_v13 as v13
            a, b = ref.run(seed, **ESC_ID[esc]), v13.run(seed, **ESC_ID[esc])
        elif cual == 'm':
            import organismo_v11m as ref, organismo_v13m as v13
            kw = dict(T=150000, fases=FASES) if esc == 'M' else ESC_ID[esc]
            a, b = ref.run(seed, **kw), v13.run(seed, **kw)
        else:
            import organismo_v11g as ref, organismo_v13g as v13
            kw = dict(T=200000, mundo='regla', regla=esc)
            a, b = ref.run(seed, **kw), v13.run(seed, **kw)
        dif = [k for k in a if N(a[k]) != N(b[k])]
        return dict(tipo=tipo, cual=cual, esc=esc, seed=seed, identico=not dif, difieren=dif)
    if tipo == 'M':
        _, brazo, eta_s, seed = args
        import organismo_v13m as m
        r = m.run(seed, T=150000, fases=FASES, eta_s=eta_s, puerta=BRAZOS[brazo])
        return dict(tipo='M', brazo=brazo, eta_s=eta_s, seed=seed, W=dict(r['sondas'][100000]), W_lenta=r['W_lenta'], splits=r['splits'],
                    celdas=r['celdas'], deaths=r['deaths'], muerde_B=bool(r['primer'].get('100000|B', {}).get('mordio')))
    if tipo == 'E':
        _, brazo, eta_s, etapa, seed = args
        import organismo_v13 as v13
        r = v13.run(seed, eta_s=eta_s, puerta=BRAZOS[brazo], **ETAPAS[etapa])
        return dict(tipo='E', brazo=brazo, eta_s=eta_s, etapa=etapa, seed=seed, pasa=bool(CRIT[etapa](r)), W=r['W'], splits=r['splits'], celdas=r['celdas'])
    _, brazo, eta_s, regla, seed = args
    import organismo_v13g as g
    r = g.run(seed, T=200000, mundo='regla', regla=regla, eta_s=eta_s, puerta=BRAZOS[brazo])
    vr = g.split_regla(seed, regla)[3]
    test, cod = r['test'], r['codigos_f2']
    f = [1.0 if r['W_apriori'][k] > 0 else (0.5 if r['W_apriori'][k] == 0 else 0.0) for k in test if vr[k] == 'comida']
    p = [1.0 if r['W_apriori'][k] < 0 else (0.5 if r['W_apriori'][k] == 0 else 0.0) for k in test if vr[k] == 'veneno']
    pf = [r['primer'][k]['pb'] for k in test if r['primer'][k] is not None and vr[k] == 'comida']
    pp = [1 - r['primer'][k]['pb'] for k in test if r['primer'][k] is not None and vr[k] == 'veneno']
    return dict(tipo='G', brazo=brazo, eta_s=eta_s, regla=regla, seed=seed,
                acc=0.5 * float(np.mean(f)) + 0.5 * float(np.mean(p)),
                ba=(0.5 * float(np.mean(pf)) + 0.5 * float(np.mean(pp))) if (pf and pp) else None,
                fuga=float(np.mean([sum(i >= 30 for i in cod[k]) / 3 for k in test])),
                lenta=float(np.median([abs(v) for v in r['W_lenta'].values()])), splits=r['splits'], celdas=r['celdas'], deaths=r['deaths'])


def fila(res, cond, seeds, etiqueta):
    brazo, eta_s = cond
    M = {r['seed']: r for r in res if r['tipo'] == 'M' and r['brazo'] == brazo and r['eta_s'] == eta_s and r['seed'] in seeds}
    G = lambda rg: {r['seed']: r for r in res if r['tipo'] == 'G' and r['brazo'] == brazo and r['eta_s'] == eta_s and r['regla'] == rg and r['seed'] in seeds}
    E = lambda et: sum(r['pasa'] for r in res if r['tipo'] == 'E' and r['brazo'] == brazo and r['eta_s'] == eta_s and r['etapa'] == et and r['seed'] in seeds)
    Gp, Ga, Gx = G('px0'), G('azar'), G('xor01')
    n = len(seeds)
    ret = sum(M[s]['W']['B'] <= -2 and M[s]['W']['A'] >= 0.5 for s in seeds)
    guar = sum(M[s]['W']['C'] <= -2.5 and M[s]['W']['D'] >= 0.85 for s in seeds)
    ba = [Gp[s]['ba'] for s in seeds if Gp[s]['ba'] is not None]
    return dict(etiqueta=etiqueta, brazo=brazo, eta_s=eta_s, n=n, seeds=f"{seeds[0]}-{seeds[-1]}", retencion=ret, guarda=guar,
                W_B=float(np.median([M[s]['W']['B'] for s in seeds])), W_A=float(np.median([M[s]['W']['A'] for s in seeds])),
                lenta_B=float(np.median([M[s]['W_lenta']['B'] for s in seeds])),
                acc=float(np.median([Gp[s]['acc'] for s in seeds])), acc_min=float(min(Gp[s]['acc'] for s in seeds)),
                acc_max=float(max(Gp[s]['acc'] for s in seeds)), azar=float(np.median([Ga[s]['acc'] for s in seeds])),
                xor=float(np.median([Gx[s]['acc'] for s in seeds])), ba=float(np.median(ba)) if ba else None,
                fuga=float(np.median([Gp[s]['fuga'] for s in seeds])), E1=E('E1'), E2=E('E2'), E2L=E('E2L'),
                splits=float(np.median([M[s]['splits'] for s in seeds])), deaths=float(np.median([M[s]['deaths'] for s in seeds])),
                muerde_B=sum(M[s]['muerde_B'] for s in seeds))


def trabajos_de(conds, seeds):
    return ([('M', b, e, s) for b, e in conds for s in seeds] + [('G', b, e, rg, s) for b, e in conds for rg in ('px0', 'azar', 'xor01') for s in seeds]
            + [('E', b, e, et, s) for b, e in conds for et in ETAPAS for s in seeds])


def imprime(filas):
    log(f"  {'condicion':24s} {'semillas':8s} {'retencion':10s} {'guarda':7s} {'W_B':6s} {'lenta_B':8s} {'acierto px0':17s} {'azar':6s} {'xor':6s} {'conducta':9s} {'fuga':5s} {'E1':6s} {'E2':6s} {'E2L':6s} {'muerdeB':8s} {'div':4s} {'muertes':7s}")
    for f in filas:
        log(f"  {f['etiqueta']:24s} {f['seeds']:8s} {f['retencion']:>3d}/{f['n']:<6d} {f['guarda']:>3d}/{f['n']:<3d} {f['W_B']:+.2f} {f['lenta_B']:+.2f}    "
            f"{f['acc']:.3f} [{f['acc_min']:.2f},{f['acc_max']:.2f}] {f['azar']:.3f}  {f['xor']:.3f}  {(f['ba'] if f['ba'] is not None else float('nan')):.3f}     "
            f"{f['fuga']:.2f}  {f['E1']:>2d}/{f['n']:<3d} {f['E2']:>2d}/{f['n']:<3d} {f['E2L']:>2d}/{f['n']:<3d} {f['muerde_B']:>4d}     {f['splits']:>3.0f}  {f['deaths']:>5.0f}")


if __name__ == '__main__':
    import multiprocessing as mp
    mp.set_start_method('spawn', force=True)
    stamp = time.strftime('%Y%m%d_%H%M%S')
    _log['f'] = open(os.path.join(RAIZ, 'datos', f'v13_dos_vias_{stamp}.log'), 'w', encoding='utf-8', newline='\n')
    pre = os.path.join(AQUI, 'PREREGISTRO_v13.md')
    shas = {n_: h16(p) for n_, p in [('preregistro', pre), ('script', os.path.abspath(__file__)),
            ('v13', os.path.join(AQUI, 'organismo_v13.py')), ('v13m', os.path.join(AQUI, 'organismo_v13m.py')),
            ('v13g', os.path.join(AQUI, 'organismo_v13g.py')), ('v11', os.path.join(RAIZ, 'organismo', 'organismo_v11.py'))]}
    log(f"ARRANQUE v13 dos vias: eta_s en {ETAS}, superficie en {SEEDS[0]}-{SEEDS[-1]}, confirmatorio en {CONF[0]}-{CONF[-1]}. Pool({N_PARALELO}).")
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
        ctrl = ([('I', 'v11', e, s) for e in ESC_ID for s in (1, 2, 3)] + [('I', 'm', e, s) for e in ('E1', 'E2', 'M') for s in (1, 2, 3)]
                + [('I', 'g', e, s) for e in ('px0', 'azar') for s in (1, 2, 3)])
        log(f"ETAPA 1/4 — P1 inercia ({len(ctrl)})...")
        rc = pool.map(tarea, ctrl, chunksize=1)
        for cual, nombre in (('v11', 'v13(eta_s=0) == v11'), ('m', 'v13m == v11m'), ('g', 'v13g == v11g')):
            g = [x for x in rc if x['cual'] == cual]
            log(f"  {nombre:26s}: {sum(x['identico'] for x in g)}/{len(g)}")
            for x in g:
                if not x['identico']:
                    log(f"      DIFIERE {x['esc']} s{x['seed']}: {x['difieren']}")
        V['P1_inercia'] = all(x['identico'] for x in rc)
        if not V['P1_inercia']:
            log("*** P1 FALLIDA: se para y se arregla el instrumento."); sys.exit(1)
        CONDS = [(b, e) for b in BRAZOS for e in ETAS]
        tr = trabajos_de(CONDS, SEEDS)
        log(f"ETAPA 2/4 — superficie: {len(tr)} corridas ({len(BRAZOS)} brazos x {len(ETAS)} tasas x [M + 3 reglas + 3 etapas] x 20)...")
        res = []
        for i, r in enumerate(pool.imap_unordered(tarea, tr, chunksize=1), 1):
            res.append(r)
            if i % 40 == 0 or i == len(tr):
                log(f"          {i}/{len(tr)}")
        filas = [fila(res, (b, e), SEEDS, f"{b} eta_s={e:g}" + (" (=v11)" if (e == 0 and b == 'suma') else "")) for b, e in CONDS]
        log(); log("  SUPERFICIE (semillas 41-60). Referencias: v9 retencion 0/20 y acierto 0.800; azar 0.50.")
        imprime(filas)
        cumplen = [f for f in filas if f['eta_s'] > 0 and f['retencion'] >= 18 and f['acc'] >= 0.78]
        V['P4_en_41_60'] = bool(cumplen)
        if cumplen:
            elegido = max(cumplen, key=lambda f: (f['retencion'] + f['E1'] + f['E2'] + f['E2L'], f['acc']))
            e_c = (elegido['brazo'], elegido['eta_s'])
            log(f"ETAPA 3/4 — {len(cumplen)} punto(s) cumplen en 41-60; se lleva UNO ({elegido['etiqueta']}) al confirmatorio en {CONF[0]}-{CONF[-1]}, que es el que decide...")
            tr2 = trabajos_de([e_c], CONF)
            for i, r in enumerate(pool.imap_unordered(tarea, tr2, chunksize=1), 1):
                res.append(r)
            fc = fila(res, e_c, CONF, f"{e_c[0]} eta_s={e_c[1]:g} CONF")
            log(); imprime([fc])
            V['P4_confirmado'] = fc['retencion'] >= 18 and fc['acc'] >= 0.78
            V['P5_nada_se_rompe'] = fc['E1'] >= 18 and fc['E2'] >= 18 and fc['E2L'] >= 18 and fc['guarda'] >= 18
            V['xor_bajo'] = fc['xor'] <= 0.60
            V['punto'] = list(e_c)
            filas.append(fc)
        else:
            log("ETAPA 3/4 — ningun punto cumple retencion>=18/20 y acierto>=0.78 en 41-60: no se toca 61-80.")
            V['P4_confirmado'] = False
    log()
    log(f"  P4 [el canje se rompe] en 41-60: {'SI' if V['P4_en_41_60'] else 'NO'};  confirmado en 61-80: {'SI' if V.get('P4_confirmado') else 'NO'}")
    if V.get('P4_confirmado'):
        log(f"  P5 [nada se rompe: E1, E2, E2L y guarda >= 18/20]: {'SOSTENIDA' if V['P5_nada_se_rompe'] else 'REFUTADA'};  XOR <= 0.60: {V['xor_bajo']}")
    log(); log("VEREDICTO v13: " + " ".join(f"{k}={v}" for k, v in V.items()))
    log("ETAPA 4/4 — escritura.")
    meta = dict(fecha=time.strftime('%Y-%m-%dT%H:%M:%S'), etas=ETAS, brazos=BRAZOS, semillas=SEEDS, confirmatorio=CONF, veredictos=V, filas=filas,
                shas=shas, procesos_python=ps, python=platform.python_version(), numpy=np.__version__)
    dj = os.path.join(RAIZ, 'datos', f'v13_dos_vias_{stamp}.json')
    json.dump(dict(meta=meta, identidades=rc, corridas=res), open(dj, 'w', encoding='utf-8'), ensure_ascii=False, default=str)
    log(f"datos -> {os.path.basename(dj)}  sha256_16 = {h16(dj)}")
    _log['f'].close()
