"""ETAPA 3 sobre v9: version dura (VD) y generalizacion en conducta al primer encuentro (G).
Ejecuta PREREGISTRO_etapa3_v9.md (sha 5a2af284ee73ae76). No decide nada que no este alli.

REGLA 10: log con marca de tiempo desde el arranque (datos/etapa3_v9_<fecha>.log). REGLA 11: procesos vivos.

Precisiones de implementacion escritas ANTES de correr:
- VD residuo por patron X con sum_S |code(X)∩code(S)| >= 1: |W_X - sum_S (n_S/3)*R_S|. En AB: codigos FINALES de A,B
  (+D en E2J/E2K), W de la sonda final; se excluye '000000' (ERR-07). En regla px0: S = 10 de entrenamiento con los
  codigos en fase2_en, W a priori, sobre los 20 patrones. Estadistico por corrida = mediana; en E1 ademas el maximo.
- G1 exactitud de signo sobre patrones de TEST: W>0 cuenta 1 si comida y 0 si veneno; W<0 al reves; W==0 cuenta 0.5.
- G2 BA_pb sobre patrones de test CON primer encuentro registrado; si una clase no tiene ninguno, la corrida no es
  evaluable y cuenta como no cumplida en el pareado.
- Comparaciones pareadas estrictas (>), por semilla.

Uso:  python experimentos/etapa3_v9/corre_etapa3_v9.py
"""
import sys, os, json, time, hashlib, platform, csv, subprocess
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
import numpy as np

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
sys.path[:0] = [AQUI, os.path.join(RAIZ, 'organismo')]
SEEDS = list(range(1, 21))
R = {'comida': 1.0, 'veneno': -3.0}
ESC_ID = {'BUG': dict(plast=False, solap_AB=3), 'E1': dict(), 'E2': dict(invertir_en=50000),
          'E2I': dict(nuevo='C'), 'E2J': dict(nuevo='D', nuevo_val='comida', solap_B=1),
          'E2K': dict(nuevo='D', nuevo_val='comida', solap_B=2), 'E2L': dict(solap_AB=3)}
VD_ESC = {'E1': dict(), 'E2J': dict(nuevo='D', nuevo_val='comida', solap_B=1), 'E2K': dict(nuevo='D', nuevo_val='comida', solap_B=2)}
VAL_AB = {'A': 'comida', 'B': 'veneno', 'D': 'comida'}
REGLAS = ['px0', 'azar', 'xor01']
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


def tarea_k(args):
    cual, esc, seed = args
    import organismo_v9 as v9, organismo_v9g as g
    if cual == 'AB':
        a, b = v9.run(seed, **ESC_ID[esc]), g.run(seed, **ESC_ID[esc])
    else:
        a, b = v9.run(seed, **ESC_ID[esc]), g.run(seed, sonda_final=True, **ESC_ID[esc])
    dif = [k for k in a if N(a[k]) != N(b[k])]
    return dict(cual=cual, esc=esc, seed=seed, identico=not dif, difieren=dif)


def tarea(args):
    bloque, cond, seed = args
    import organismo_v9g as g
    if bloque == 'VD':
        r = g.run(seed, sonda_final=True, **VD_ESC[cond])
        return dict(bloque=bloque, cond=cond, seed=seed, W=r['W'], sonda=r['sonda'], codigos_fin=r['codigos_fin'],
                    n_techo=r['n_techo'], splits=r['splits'], deaths=r['deaths'])
    r = g.run(seed, T=200000, mundo='regla', regla=cond)
    return dict(bloque=bloque, cond=cond, seed=seed, tren=r['tren'], test=r['test'], W_apriori=r['W_apriori'],
                codigos_f2=r['codigos_f2'], primer=r['primer'], n_techo=r['n_techo'], splits=r['splits'],
                deaths=r['deaths'], celdas=r['celdas'], W_final=r['W_final'])


def valencia(regla, seed):
    import organismo_v9g as g
    return g.split_regla(seed, regla)[3]


def residuos_AB(r):
    estim = ['A', 'B'] + (['D'] if r['cond'] != 'E1' else [])
    out = []
    for nm, d in r['sonda'].items():
        if nm == '000000':
            continue
        cod = set(d['codigo'])
        ns = {s: len(cod & set(r['codigos_fin'][s])) for s in estim}
        if sum(ns.values()) >= 1:
            pred = sum(ns[s] / 3 * R[VAL_AB[s]] for s in estim)
            out.append(abs(d['W'] - pred))
    return out


def residuos_regla(r, vr):
    out = []
    for nm, w in r['W_apriori'].items():
        cod = set(r['codigos_f2'][nm])
        ns = {s: len(cod & set(r['codigos_f2'][s])) for s in r['tren']}
        if sum(ns.values()) >= 1:
            pred = sum(ns[s] / 3 * R[vr[s]] for s in r['tren'])
            out.append(abs(w - pred))
    return out


def acc_signo(r, vr):
    f = []; p = []
    for k in r['test']:
        w = r['W_apriori'][k]
        s = 0.5 if w == 0 else (1.0 if w > 0 else 0.0)
        (f if vr[k] == 'comida' else p).append(s if vr[k] == 'comida' else 1 - s)
    return 0.5 * np.mean(f) + 0.5 * np.mean(p)


def ba_pb(r, vr):
    f = [r['primer'][k]['pb'] for k in r['test'] if r['primer'][k] is not None and vr[k] == 'comida']
    p = [1 - r['primer'][k]['pb'] for k in r['test'] if r['primer'][k] is not None and vr[k] == 'veneno']
    if not f or not p:
        return None
    return 0.5 * np.mean(f) + 0.5 * np.mean(p)


if __name__ == '__main__':
    import multiprocessing as mp
    mp.set_start_method('spawn', force=True)
    stamp = time.strftime('%Y%m%d_%H%M%S')
    _log['f'] = open(os.path.join(RAIZ, 'datos', f'etapa3_v9_{stamp}.log'), 'w', encoding='utf-8', newline='\n')
    pre = os.path.join(AQUI, 'PREREGISTRO_etapa3_v9.md')
    log(f"ARRANQUE Etapa 3 sobre v9. semillas 1..20, Pool({N_PARALELO}).")
    log(f"sha preregistro {h16(pre)}  script {h16(os.path.abspath(__file__))}  v9g {h16(os.path.join(AQUI, 'organismo_v9g.py'))}"
        f"  v9 {h16(os.path.join(RAIZ, 'organismo', 'organismo_v9.py'))}")
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
        trabajos = [('AB', e, s) for e in ESC_ID for s in range(1, 4)] + [('sonda', 'E1', s) for s in range(1, 4)]
        log(f"ETAPA 1/4 — K identidades ({len(trabajos)})...")
        k = pool.map(tarea_k, trabajos, chunksize=1)
        for c in ('AB', 'sonda'):
            g_ = [x for x in k if x['cual'] == c]
            log(f"  K {c}: {sum(x['identico'] for x in g_)}/{len(g_)}")
            for x in g_:
                if not x['identico']:
                    log(f"      DIFIERE {x['esc']} s{x['seed']}: {x['difieren']}")
        V['K_identidad'] = all(x['identico'] for x in k)
        if not V['K_identidad']:
            log("*** K FALLIDO: se para."); sys.exit(1)

        trabajos = [('G', rg, s) for rg in REGLAS for s in SEEDS] + [('VD', e, s) for e in VD_ESC for s in SEEDS]
        log(f"ETAPA 2/4 — {len(trabajos)} corridas (G: 3 reglas x 20, T=200k; VD: 3 escenarios x 20)...")
        res = []
        for i, r in enumerate(pool.imap_unordered(tarea, trabajos, chunksize=1), 1):
            res.append(r)
            if i % 30 == 0 or i == len(trabajos):
                log(f"          {i}/{len(trabajos)}")

    log("ETAPA 3/4 — analisis.")
    G = lambda b, c: {r['seed']: r for r in res if r['bloque'] == b and r['cond'] == c}
    VR = {rg: {s: valencia(rg, s) for s in SEEDS} for rg in REGLAS}

    # K cobertura
    cob = {}
    for rg in REGLAS:
        minimo = 10 if rg == 'xor01' else 8
        cob[rg] = sum(sum(v is not None for v in G('G', rg)[s]['primer'].values()) >= minimo for s in SEEDS)
    V['K_cobertura'] = all(v == 20 for v in cob.values())
    log(f"  K cobertura de primer encuentro (20/20 con >=8 de 10, xor >=10 de 12): {cob} -> {'OK' if V['K_cobertura'] else 'NO EVALUABLE'}")

    # VD
    log()
    med_res = {}
    for e in VD_ESC:
        med_res[e] = {s: float(np.median(residuos_AB(G('VD', e)[s]))) for s in SEEDS}
    max_E1 = {s: float(np.max(residuos_AB(G('VD', 'E1')[s]))) for s in SEEDS}
    med_res['px0'] = {s: float(np.median(residuos_regla(G('G', 'px0')[s], VR['px0'][s]))) for s in SEEDS}
    for e in ('E1', 'E2J', 'E2K', 'px0'):
        v = list(med_res[e].values())
        log(f"  VD residuo mediano {e:4s}: {np.median(v):.4f} [{min(v):.4f}, {max(v):.4f}]"
            + (f"   max E1 {np.median(list(max_E1.values())):.4f} [{min(max_E1.values()):.4f}, {max(max_E1.values()):.4f}]" if e == 'E1' else ""))
    V['VD1'] = all(m < 0.01 for m in max_E1.values())
    a12 = sum(med_res['E1'][s] < med_res['E2J'][s] for s in SEEDS); a23 = sum(med_res['E2J'][s] < med_res['E2K'][s] for s in SEEDS)
    V['VD2'] = a12 >= 15 and a23 >= 15
    a34 = sum(med_res['px0'][s] > med_res['E2K'][s] for s in SEEDS)
    V['VD3'] = a34 >= 15
    log(f"  VD1 E1 residuo max < 0.01 en 20/20: {'SOSTENIDA' if V['VD1'] else 'REFUTADA'}  ({sum(m < 0.01 for m in max_E1.values())}/20)")
    log(f"  VD2 E1<E2J en {a12}/20, E2J<E2K en {a23}/20 (>=15 cada una): {'SOSTENIDA' if V['VD2'] else 'REFUTADA'}")
    log(f"  VD3 px0 > E2K en {a34}/20 (>=15): {'SOSTENIDA' if V['VD3'] else 'REFUTADA'}")
    log(f"  truncaciones (n_techo mediana): " + ", ".join(f"{e} {np.median([G('VD', e)[s]['n_techo'] for s in SEEDS]):.0f}" for e in VD_ESC)
        + ", " + ", ".join(f"{rg} {np.median([G('G', rg)[s]['n_techo'] for s in SEEDS]):.0f}" for rg in REGLAS))

    # G
    log()
    acc = {rg: {s: acc_signo(G('G', rg)[s], VR[rg][s]) for s in SEEDS} for rg in REGLAS}
    ba = {rg: {s: ba_pb(G('G', rg)[s], VR[rg][s]) for s in SEEDS} for rg in REGLAS}
    for rg in REGLAS:
        a = list(acc[rg].values()); b = [x for x in ba[rg].values() if x is not None]
        prim = [G('G', rg)[s]['primer'] for s in SEEDS]
        mf = [v['mordio'] for s, pr in zip(SEEDS, prim) for kk, v in pr.items() if v is not None and VR[rg][s][kk] == 'comida']
        mv = [v['mordio'] for s, pr in zip(SEEDS, prim) for kk, v in pr.items() if v is not None and VR[rg][s][kk] == 'veneno']
        cero = np.median([sum(G('G', rg)[s]['W_apriori'][kk] == 0 for kk in G('G', rg)[s]['test']) / len(G('G', rg)[s]['test']) for s in SEEDS])
        log(f"  {rg:5s} valor (signo) {np.median(a):.3f} [{min(a):.3f}, {max(a):.3f}]   conducta BA_pb {np.median(b):.3f} [{min(b):.3f}, {max(b):.3f}]"
            f"   mordidas 1er encuentro: comida {np.mean(mf):.2f} (n={len(mf)}), veneno {np.mean(mv):.2f} (n={len(mv)})   alcance W=0: {cero:.2f}"
            f"   splits {np.median([G('G', rg)[s]['splits'] for s in SEEDS]):.0f}  muertes {np.median([G('G', rg)[s]['deaths'] for s in SEEDS]):.0f}")
    mpx = float(np.median(list(acc['px0'].values()))); maz = float(np.median(list(acc['azar'].values())))
    par1 = sum(acc['px0'][s] > acc['azar'][s] for s in SEEDS)
    V['G1'] = mpx >= 0.65 and 0.35 <= maz <= 0.65 and par1 >= 14
    bpx = [x for x in ba['px0'].values() if x is not None]; baz = [x for x in ba['azar'].values() if x is not None]
    par2 = sum(ba['px0'][s] is not None and ba['azar'][s] is not None and ba['px0'][s] > ba['azar'][s] for s in SEEDS)
    V['G2'] = bool(bpx) and bool(baz) and float(np.median(bpx)) >= 0.55 and 0.42 <= float(np.median(baz)) <= 0.58 and par2 >= 14
    mxo = float(np.median(list(acc['xor01'].values())))
    par3 = sum(acc['xor01'][s] < acc['px0'][s] for s in SEEDS)
    V['G3_sin_voto'] = mxo <= 0.60 and par3 >= 14
    log()
    log(f"  G1 valor: px0 {mpx:.3f} (>=0.65), azar {maz:.3f} (en [0.35,0.65]), px0>azar {par1}/20 (>=14): {'SOSTENIDA' if V['G1'] else 'REFUTADA'}")
    log(f"  G2 conducta 1er encuentro: px0 {np.median(bpx):.3f} (>=0.55), azar {np.median(baz):.3f} (en [0.42,0.58]), px0>azar {par2}/20 (>=14): "
        f"{'SOSTENIDA' if V['G2'] else 'REFUTADA'}")
    log(f"  G3 frontera XOR (sin voto): xor {mxo:.3f} (<=0.60), xor<px0 {par3}/20 (>=14): {'SOSTENIDA' if V['G3_sin_voto'] else 'REFUTADA'}")
    CIERRE = bool(V['K_identidad'] and V['K_cobertura'] and V['G1'] and V['G2'])
    V['ETAPA3_CERRADA'] = CIERRE
    log(); log("VEREDICTO etapa3_v9: " + " ".join(f"{k}={v}" for k, v in V.items()))

    log("ETAPA 4/4 — escritura.")
    meta = dict(fecha=time.strftime('%Y-%m-%dT%H:%M:%S'), semillas=SEEDS, veredictos=V, cobertura=cob,
                residuo_mediano=med_res, residuo_max_E1=max_E1, acc_signo=acc, ba_pb=ba, K=k, procesos_python=ps,
                sha_preregistro=h16(pre), sha_script=h16(os.path.abspath(__file__)),
                sha_constructor=h16(os.path.join(AQUI, 'construye_v9g.py')), sha_v9g=h16(os.path.join(AQUI, 'organismo_v9g.py')),
                sha_v9=h16(os.path.join(RAIZ, 'organismo', 'organismo_v9.py')),
                python=platform.python_version(), numpy=np.__version__, plataforma=platform.platform())
    dj = os.path.join(RAIZ, 'datos', f'etapa3_v9_{stamp}.json')
    json.dump(dict(meta=meta, corridas=res), open(dj, 'w', encoding='utf-8'), ensure_ascii=False, default=str)
    dc = os.path.join(RAIZ, 'datos', f'etapa3_v9_{stamp}.csv')
    with open(dc, 'w', encoding='utf-8', newline='') as f:
        w = csv.writer(f); w.writerow(['bloque', 'cond', 'seed', 'residuo_mediano', 'acc_signo', 'ba_pb', 'n_techo', 'splits', 'deaths'])
        for r in sorted(res, key=lambda r: (r['bloque'], r['cond'], r['seed'])):
            s = r['seed']; c = r['cond']
            w.writerow([r['bloque'], c, s, round(med_res[c][s], 5) if c in med_res else '',
                        round(acc[c][s], 4) if r['bloque'] == 'G' else '',
                        (round(ba[c][s], 4) if ba[c][s] is not None else '') if r['bloque'] == 'G' else '',
                        r['n_techo'], r['splits'], r['deaths']])
    log(f"datos -> {os.path.basename(dj)}  sha256_16 = {h16(dj)}")
    log(f"         {os.path.basename(dc)}  sha256_16 = {h16(dc)}")
    _log['f'].close()
