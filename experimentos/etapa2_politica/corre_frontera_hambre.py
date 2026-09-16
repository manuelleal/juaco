"""Etapa 2 (2P) — frontera entre explorar con hambre y sobrevivir. Ejecuta PREREGISTRO_frontera_hambre.md.

REGLA 10: log con marca de tiempo desde el arranque (datos/frontera_hambre_<fecha>.log). REGLA 11: procesos vivos.

Precisiones de implementacion escritas ANTES de correr:
- Todas las comparaciones de igualdad son NUMERICAS (leccion de ERR-13): los resultados se normalizan con un
  ida y vuelta por JSON (tuplas -> listas) y se comparan con ==, que trata 0.0 == -0.0.
- F4 "mordidas de veneno en la segunda mitad": total por semilla de MH['veneno'] (suma de los 5 tramos), mediana
  sobre semillas. Si la mediana con hb=2.0 fuese 0, F4 se declara no evaluable.
- F2 tolerancia: pasa(hb_siguiente) >= pasa(hb_anterior) - 2 para hb en 0..2.0.

Uso:  python experimentos/etapa2_politica/corre_frontera_hambre.py [semillas]
"""
import sys, os, json, time, hashlib, platform, csv, subprocess
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
import numpy as np

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
sys.path[:0] = [AQUI, os.path.join(RAIZ, 'organismo')]
HB = [0.0, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0]
ESC = {'E1': dict(), 'E2': dict(invertir_en=50000)}
ESC_ID = {'BUG': dict(plast=False, solap_AB=3), 'E1': dict(), 'E2': dict(invertir_en=50000),
          'E2I': dict(nuevo='C'), 'E2J': dict(nuevo='D', nuevo_val='comida', solap_B=1),
          'E2K': dict(nuevo='D', nuevo_val='comida', solap_B=2), 'E2L': dict(solap_AB=3)}
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


def tarea_id(args):
    esc, seed = args
    import organismo_v8 as a, organismo_v8p as b
    ra, rb = a.run(seed, **ESC_ID[esc]), b.run(seed, **ESC_ID[esc])
    dif = [k for k in ra if N(ra[k]) != N(rb[k])]
    return dict(esc=esc, seed=seed, identico=not dif, difieren=dif)


def tarea(args):
    esc, hb, seed = args
    import organismo_v8p as o
    r = o.run(seed, hambre_boca=hb, **ESC[esc])
    return dict(esc=esc, hb=hb, seed=seed, W=r['W'], mord=r['mord'], vis=r['vis'], deaths=r['deaths'], splits=r['splits'],
                dq=r['dq'], VH=r['VH'], MH=r['MH'], PH=r['PH'], t_ext=r['t_ext'])


def med(xs):
    xs = [x for x in xs if x is not None]
    return float(np.median(xs)) if xs else None


if __name__ == '__main__':
    import multiprocessing as mp
    mp.set_start_method('spawn', force=True)
    S = int(sys.argv[1]) if len(sys.argv) > 1 else 20
    seeds = list(range(1, S + 1))
    stamp = time.strftime('%Y%m%d_%H%M%S')
    _log['f'] = open(os.path.join(RAIZ, 'datos', f'frontera_hambre_{stamp}.log'), 'w', encoding='utf-8', newline='\n')
    pre = os.path.join(AQUI, 'PREREGISTRO_frontera_hambre.md')
    log(f"ARRANQUE frontera hambre-supervivencia sobre v8. {S} semillas, hb={HB}, Pool({N_PARALELO}).")
    log(f"sha preregistro {h16(pre)}  script {h16(os.path.abspath(__file__))}  v8p {h16(os.path.join(AQUI, 'organismo_v8p.py'))}"
        f"  v8 {h16(os.path.join(RAIZ, 'organismo', 'organismo_v8.py'))}")
    try:
        ps = subprocess.run(['powershell', '-NoProfile', '-Command',
                             "Get-CimInstance Win32_Process | Where-Object { $_.Name -like 'python*' } | "
                             "ForEach-Object { \"$($_.ProcessId) $($_.CommandLine)\" }"],
                            capture_output=True, text=True, timeout=60).stdout.strip().splitlines()
    except Exception as e:
        ps = [f"(no se pudo listar: {e})"]
    log(f"REGLA 11 — procesos python vivos ({len(ps)}), este es pid {os.getpid()}:")
    for l in ps:
        log(f"    {l[:160]}")
    V = {}

    with mp.Pool(N_PARALELO) as pool:
        trabajos = [(e, s) for e in ESC_ID for s in range(1, 7)]
        log(f"ETAPA 1/4 — F0a: v8p == v8 ({len(trabajos)} comparaciones)...")
        ids = pool.map(tarea_id, trabajos, chunksize=1)
        V['F0a'] = all(x['identico'] for x in ids)
        log(f"  F0a: {sum(x['identico'] for x in ids)}/{len(ids)} -> {'OK' if V['F0a'] else 'FALLA'}")
        for x in ids:
            if not x['identico']:
                log(f"      DIFIERE {x['esc']} s{x['seed']}: {x['difieren']}")
        if not V['F0a']:
            log("*** F0a FALLIDA: v8p no es v8. No se corre nada mas."); sys.exit(1)

        trabajos = [(e, hb, s) for hb in HB for e in ESC for s in seeds]
        log(f"ETAPA 2/4 — {len(trabajos)} corridas (hb x E1/E2 x semillas)...")
        res = []
        for i, r in enumerate(pool.imap_unordered(tarea, trabajos, chunksize=1), 1):
            res.append(r)
            if i % 40 == 0 or i == len(trabajos):
                log(f"          {i}/{len(trabajos)}")

    log("ETAPA 3/4 — analisis.")
    G = lambda e, hb: sorted([r for r in res if r['esc'] == e and r['hb'] == hb], key=lambda r: r['seed'])

    # F0b: reproduce el examen de v8 con hb=2.0
    ex = json.load(open(os.path.join(RAIZ, 'datos', 'examen_v8_20260916_145204.json'), encoding='utf-8'))['corridas']
    ok_b = 0; tot_b = 0
    for e in ('E1', 'E2'):
        viejo = {r['seed']: r for r in ex if r['etapa'] == e}
        for r in G(e, 2.0):
            if r['seed'] in viejo:
                tot_b += 1
                ok_b += all(N(r[k]) == N(viejo[r['seed']][k]) for k in ('W', 'mord', 'vis', 'deaths', 'splits'))
    V['F0b'] = tot_b == 2 * S and ok_b == tot_b
    log(f"  F0b reproduce el examen de v8 (hb=2.0): {ok_b}/{tot_b} -> {'OK' if V['F0b'] else 'FALLA'}")
    if not V['F0b']:
        log("*** F0b FALLIDA: se para la lectura.")

    # tabla descriptiva
    log()
    log(f"  {'hb':>4} | {'muertes E1':>10} {'muertes E2':>10} {'combinado':>9} | {'E2 pasa':>7} {'t_ext med':>9} | "
        f"{'veneno E1 2a mitad':>18} {'comida E1':>9}")
    pasa = {}; mE1 = {}; mE2 = {}; ven = {}
    crit_E2 = lambda r: abs(r['W']['A'] + 3) < .3 and abs(r['W']['B'] - 1) < .15 and r['mord']['B'][3] >= 50
    for hb in HB:
        e1, e2 = G('E1', hb), G('E2', hb)
        mE1[hb] = med([r['deaths'] for r in e1]); mE2[hb] = med([r['deaths'] for r in e2])
        pasa[hb] = sum(crit_E2(r) for r in e2)
        ven[hb] = med([sum(r['MH']['veneno']) for r in e1])
        com = med([sum(r['MH']['comida']) for r in e1])
        text = med([r['t_ext'] for r in e2])
        log(f"  {hb:4.1f} | {mE1[hb]:10.1f} {mE2[hb]:10.1f} {mE1[hb]+mE2[hb]:9.1f} | {pasa[hb]:4d}/{S} "
            f"{('-' if text is None else f'{text:9.0f}'):>9} | {ven[hb]:18.1f} {com:9.1f}")

    # F1
    malos = []; celdas = 0
    for hb in HB:
        e1 = G('E1', hb)
        for v in ('veneno', 'comida'):
            for b in range(5):
                exp = sum(r['PH'][v][b] for r in e1); obs = sum(r['MH'][v][b] for r in e1)
                if exp >= 20:
                    celdas += 1
                    if not (0.8 <= obs / exp <= 1.25):
                        malos.append((hb, v, b, obs, round(exp, 1)))
    V['F1'] = not malos
    log(); log(f"  F1 contador (obs/esperadas en [0.8,1.25], {celdas} celdas con >=20 esperadas): "
             f"{'SOSTENIDA' if V['F1'] else 'REFUTADA'} {malos[:5]}")
    # tasas de veneno por tramo de hambre, E1 (descriptivo)
    for hb in (0.0, 1.0, 2.0, 3.0):
        e1 = G('E1', hb)
        tasas = []
        for b in range(5):
            vis_b = sum(r['VH']['veneno'][b] for r in e1); m_b = sum(r['MH']['veneno'][b] for r in e1)
            tasas.append('-' if vis_b == 0 else f"{100*m_b/vis_b:.2f}%")
        log(f"      tasa de veneno por visita E1 2a mitad, hb={hb}: tramos de hambre 0-.2..-.8-1 = {tasas}")

    # F2
    mono = all(pasa[HB[i + 1]] >= pasa[HB[i]] - 2 for i in range(0, 4))
    V['F2'] = pasa[2.0] >= 18 and pasa[1.0] <= 5 and pasa[0.0] == 0 and mono
    log(f"  F2 umbral de reversibilidad (hb=2 >=18, hb=1 <=5, hb=0 ==0, monotona): {'SOSTENIDA' if V['F2'] else 'REFUTADA'}"
        f"  {[(hb, pasa[hb]) for hb in HB]}")
    # F3
    V['F3'] = mE2[1.0] >= 1.5 * mE2[2.0]
    log(f"  F3 sin exploracion se muere en E2 (hb=1 >= 1.5x hb=2): {'SOSTENIDA' if V['F3'] else 'REFUTADA'}"
        f"  {mE2[1.0]} vs {mE2[2.0]} (x{mE2[1.0]/mE2[2.0]:.2f})")
    # F4
    if ven[2.0] and ven[2.0] > 0:
        V['F4'] = abs(mE1[0.0] - mE1[2.0]) <= 0.10 * mE1[2.0] and ven[0.0] <= 0.20 * ven[2.0]
        log(f"  F4 en E1 la exploracion cuesta poco (muertes +-10%, veneno <=20%): {'SOSTENIDA' if V['F4'] else 'REFUTADA'}"
            f"  muertes {mE1[0.0]} vs {mE1[2.0]} ({100*(mE1[0.0]-mE1[2.0])/mE1[2.0]:+.1f}%), veneno {ven[0.0]} vs {ven[2.0]}")
    else:
        V['F4'] = None; log("  F4 NO EVALUABLE: mediana de veneno con hb=2.0 es 0")
    # F5
    comb = {hb: mE1[hb] + mE2[hb] for hb in HB}
    arg = min(comb, key=comb.get)
    V['F5'] = arg in (1.5, 2.0, 2.5)
    log(f"  F5 v8 en el optimo combinado (argmin en 1.5-2.5): {'SOSTENIDA' if V['F5'] else 'REFUTADA'}  argmin hb={arg}  {comb}")
    # F6
    V['F6'] = mE1[3.0] >= 1.10 * mE1[2.0]
    log(f"  F6 demasiada exploracion tambien mata (E1 hb=3 >= 1.10x hb=2): {'SOSTENIDA' if V['F6'] else 'REFUTADA'}"
        f"  {mE1[3.0]} vs {mE1[2.0]} (x{mE1[3.0]/mE1[2.0]:.2f})")

    log()
    log("VEREDICTO frontera_hambre: " + " ".join(f"{k}={v}" for k, v in V.items()))
    log("ETAPA 4/4 — escritura.")
    meta = dict(fecha=time.strftime('%Y-%m-%dT%H:%M:%S'), semillas=S, HB=HB, veredictos=V, identidad=ids, procesos_python=ps,
                muertes_E1=mE1, muertes_E2=mE2, pasa_E2=pasa, veneno_E1=ven,
                sha_preregistro=h16(pre), sha_script=h16(os.path.abspath(__file__)),
                sha_constructor=h16(os.path.join(AQUI, 'construye_v8p.py')), sha_v8p=h16(os.path.join(AQUI, 'organismo_v8p.py')),
                sha_v8=h16(os.path.join(RAIZ, 'organismo', 'organismo_v8.py')),
                python=platform.python_version(), numpy=np.__version__, plataforma=platform.platform())
    dj = os.path.join(RAIZ, 'datos', f'frontera_hambre_{stamp}.json')
    json.dump(dict(meta=meta, corridas=res), open(dj, 'w', encoding='utf-8'), ensure_ascii=False, default=str)
    dc = os.path.join(RAIZ, 'datos', f'frontera_hambre_{stamp}.csv')
    with open(dc, 'w', encoding='utf-8', newline='') as f:
        w = csv.writer(f); w.writerow(['esc', 'hb', 'seed', 'W_A', 'W_B', 'deaths', 'dq', 'mordB_q4', 't_ext', 'veneno_2a', 'comida_2a'])
        for r in sorted(res, key=lambda r: (r['esc'], r['hb'], r['seed'])):
            w.writerow([r['esc'], r['hb'], r['seed'], r['W']['A'], r['W']['B'], r['deaths'], r['dq'], r['mord']['B'][3],
                        r['t_ext'], sum(r['MH']['veneno']), sum(r['MH']['comida'])])
    log(f"datos -> {os.path.basename(dj)}  sha256_16 = {h16(dj)}")
    log(f"         {os.path.basename(dc)}  sha256_16 = {h16(dc)}")
    _log['f'].close()
