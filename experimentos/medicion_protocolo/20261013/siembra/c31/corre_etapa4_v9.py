"""ETAPA 4 sobre v9: memoria persistente. Bloque M (ausencia con interferencia) y bloque H (herencia).
Ejecuta PREREGISTRO_etapa4_v9.md. No decide nada que no este alli.

REGLA 10: log con marca de tiempo desde el arranque (datos/etapa4_v9_<fecha>.log). REGLA 11: procesos vivos.
Precisiones escritas ANTES de correr:
- Veneno en Q1 de la cria: mundo igual -> mordidas de B en Q1; mundo invertido -> mordidas de A en Q1 (descriptivo).
- Comparaciones pareadas estrictas por semilla. Igualdades NUMERICAS.
- M1 compara sondas[100000] con sondas[50000] en A y B con ==.

Uso:  python experimentos/etapa4_v9/corre_etapa4_v9.py
"""
import sys, os, json, time, hashlib, platform, csv, subprocess
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
import numpy as np

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
sys.path[:0] = [AQUI, os.path.join(RAIZ, 'organismo')]
SEEDS = list(range(1, 21))
ESC_ID = {'BUG': dict(plast=False, solap_AB=3), 'E1': dict(), 'E2': dict(invertir_en=50000),
          'E2I': dict(nuevo='C'), 'E2J': dict(nuevo='D', nuevo_val='comida', solap_B=1),
          'E2K': dict(nuevo='D', nuevo_val='comida', solap_B=2), 'E2L': dict(solap_AB=3)}
FASES = {50000: (['C', 'D'], {'C': 'veneno', 'D': 'comida'}), 100000: (['A', 'B'], {'A': 'comida', 'B': 'veneno'})}
MODOS = ['cero', 'parcial', 'completa']
MUNDOS = ['igual', 'invertido']
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
    import organismo_v9m as m
    if tipo == 'K':
        _, esc, seed = args
        import organismo_v9 as v9
        a, b = v9.run(seed, **ESC_ID[esc]), m.run(seed, **ESC_ID[esc])
        return dict(tipo=tipo, esc=esc, seed=seed, identico=all(N(a[k]) == N(b[k]) for k in a),
                    difieren=[k for k in a if N(a[k]) != N(b[k])])
    if tipo == 'Kh':
        _, seed = args
        p = m.run(seed, T=2000, devolver_estado=True)
        c = m.run(seed + 1000, T=2000, estado_inicial=p['estado'])
        return dict(tipo=tipo, seed=seed, ok=c['deaths'] >= 0 and c['W'] is not None)
    if tipo == 'M':
        _, cond, seed = args
        r = m.run(seed, T=150000, fases=FASES, congelar=(50000, 100000) if cond == 'control' else None)
        return dict(tipo=tipo, cond=cond, seed=seed, sondas=r['sondas'], primer=r['primer'], W=r['W'], deaths=r['deaths'],
                    splits=r['splits'], dq=r['dq'])
    if tipo == 'P':
        _, seed = args
        r = m.run(seed, devolver_estado=True)
        return dict(tipo=tipo, seed=seed, estado=r['estado'], W=r['W'])
    _, modo, mundo, seed, estado = args
    kw = dict(invertir_en=0) if mundo == 'invertido' else {}
    if modo == 'cero':
        r = m.run(1000 + seed, **kw)
    else:
        r = m.run(1000 + seed, estado_inicial=estado, heredar_patas=(modo == 'completa'), **kw)
    return dict(tipo='H', modo=modo, mundo=mundo, seed=seed, W=r['W'], mord=r['mord'], dq=r['dq'], deaths=r['deaths'],
                splits=r['splits'])


if __name__ == '__main__':
    import multiprocessing as mp
    mp.set_start_method('spawn', force=True)
    stamp = time.strftime('%Y%m%d_%H%M%S')
    _log['f'] = open(os.path.join(RAIZ, 'datos', f'etapa4_v9_{stamp}.log'), 'w', encoding='utf-8', newline='\n')
    pre = os.path.join(AQUI, 'PREREGISTRO_etapa4_v9.md')
    log(f"ARRANQUE Etapa 4 sobre v9 (memoria persistente). Pool({N_PARALELO}).")
    log(f"sha preregistro {h16(pre)}  script {h16(os.path.abspath(__file__))}  v9m {h16(os.path.join(AQUI, 'organismo_v9m.py'))}"
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
        ctrl = [('K', e, s) for e in ESC_ID for s in range(1, 4)] + [('Kh', s) for s in range(1, 4)]
        log(f"ETAPA 1/4 — instrumento ({len(ctrl)})...")
        rc = pool.map(tarea, ctrl, chunksize=1)
        ki = [x for x in rc if x['tipo'] == 'K']; kh = [x for x in rc if x['tipo'] == 'Kh']
        V['K_identidad'] = all(x['identico'] for x in ki); V['K_herencia_corre'] = all(x['ok'] for x in kh)
        log(f"  v9m(defecto) == v9: {sum(x['identico'] for x in ki)}/{len(ki)};  herencia corre: {sum(x['ok'] for x in kh)}/{len(kh)}")
        for x in ki:
            if not x['identico']:
                log(f"      DIFIERE {x}")
        if not (V['K_identidad'] and V['K_herencia_corre']):
            log("*** instrumento FALLIDO: se para."); sys.exit(1)

        log("ETAPA 2/4 — bloque M (40) y progenitores de H (20)...")
        t1 = [('M', c, s) for c in ('con', 'control') for s in SEEDS] + [('P', s) for s in SEEDS]
        r1 = []
        for i, r in enumerate(pool.imap_unordered(tarea, t1, chunksize=1), 1):
            r1.append(r)
            if i % 20 == 0 or i == len(t1):
                log(f"          {i}/{len(t1)}")
        estados = {r['seed']: r['estado'] for r in r1 if r['tipo'] == 'P'}
        t2 = [('H', mo, mu, s, estados[s]) for mo in MODOS for mu in MUNDOS for s in SEEDS]
        log(f"ETAPA 3/4 — crias de H ({len(t2)})...")
        r2 = []
        for i, r in enumerate(pool.imap_unordered(tarea, t2, chunksize=1), 1):
            r2.append(r)
            if i % 30 == 0 or i == len(t2):
                log(f"          {i}/{len(t2)}")

    log("ETAPA 4/4 — analisis.")
    GM = lambda c: {r['seed']: r for r in r1 if r['tipo'] == 'M' and r['cond'] == c}
    con, ctl = GM('con'), GM('control')
    m1 = sum(ctl[s]['sondas'][100000]['A'] == ctl[s]['sondas'][50000]['A'] and ctl[s]['sondas'][100000]['B'] == ctl[s]['sondas'][50000]['B'] for s in SEEDS)
    V['M1'] = m1 == 20
    wb = [con[s]['sondas'][100000]['B'] for s in SEEDS]; wa = [con[s]['sondas'][100000]['A'] for s in SEEDS]
    V['M2'] = sum(x <= -2.0 for x in wb) >= 15 and sum(x >= 0.5 for x in wa) >= 15
    dif = [abs(con[s]['sondas'][100000]['A'] - con[s]['sondas'][50000]['A']) + abs(con[s]['sondas'][100000]['B'] - con[s]['sondas'][50000]['B']) for s in SEEDS]
    V['M3'] = sum(d > 0.01 for d in dif) >= 10
    log(); log("  BLOQUE M — ausencia con interferencia (A,B fuera en [50k,100k); se aprende C veneno y D comida)")
    log(f"   M1 control sin aprendizaje: W_A y W_B en 100k == 50k en {m1}/20 -> {'SOSTENIDA' if V['M1'] else 'REFUTADA'}")
    log(f"   con aprendizaje: W_A 50k {np.median([con[s]['sondas'][50000]['A'] for s in SEEDS]):+.3f} -> 100k {np.median(wa):+.3f} [{min(wa):+.2f},{max(wa):+.2f}];"
        f"  W_B 50k {np.median([con[s]['sondas'][50000]['B'] for s in SEEDS]):+.3f} -> 100k {np.median(wb):+.3f} [{min(wb):+.2f},{max(wb):+.2f}]")
    log(f"   M2 recuerda (W_B<=-2 en {sum(x <= -2.0 for x in wb)}/20, W_A>=0.5 en {sum(x >= 0.5 for x in wa)}/20; >=15 cada): {'SOSTENIDA' if V['M2'] else 'REFUTADA'}")
    log(f"   M3 interferencia medible (|dA|+|dB|>0.01 en {sum(d > 0.01 for d in dif)}/20, >=10): {'SOSTENIDA' if V['M3'] else 'REFUTADA'}"
        f"  mediana {np.median(dif):.3f} [{min(dif):.3f},{max(dif):.3f}]")
    pbB = [con[s]['primer'].get('100000|B', {}).get('pb') for s in SEEDS]; mbB = [con[s]['primer'].get('100000|B', {}).get('mordio') for s in SEEDS]
    log(f"   (sin voto) primer reencuentro con B: pb mediana {np.median([x for x in pbB if x is not None]):.4f}; mordio {sum(bool(x) for x in mbB)}/20;"
        f"  splits en ausencia (con) {np.median([con[s]['splits'] for s in SEEDS]):.0f}")

    GH = lambda mo, mu: {r['seed']: r for r in r2 if r['modo'] == mo and r['mundo'] == mu}
    log(); log("  BLOQUE H — herencia (cria con semilla 1000+s; progenitor v9 E1 semilla s)")
    for mu in MUNDOS:
        for mo in MODOS:
            g = GH(mo, mu)
            ven = [g[s]['mord']['B' if mu == 'igual' else 'A'][0] for s in SEEDS]
            log(f"   {mu:9s} {mo:8s} veneno Q1 {np.median(ven):6.1f}  muertes Q1 {np.median([g[s]['dq'][0] for s in SEEDS]):5.1f}"
                f"  Q1+Q2 {np.median([g[s]['dq'][0]+g[s]['dq'][1] for s in SEEDS]):5.1f}  total {np.median([g[s]['deaths'] for s in SEEDS]):5.1f}"
                f"  W_A {np.median([g[s]['W']['A'] for s in SEEDS]):+.2f} W_B {np.median([g[s]['W']['B'] for s in SEEDS]):+.2f}")
    ci, pi_, co = GH('cero', 'igual'), GH('parcial', 'igual'), GH('completa', 'igual')
    ven_c = [ci[s]['mord']['B'][0] for s in SEEDS]; ven_k = [co[s]['mord']['B'][0] for s in SEEDS]; ven_p = [pi_[s]['mord']['B'][0] for s in SEEDS]
    V['H1'] = np.median(ven_k) <= 0.5 * np.median(ven_c) and sum(co[s]['mord']['B'][0] < ci[s]['mord']['B'][0] for s in SEEDS) >= 15
    V['H3'] = sum(co[s]['dq'][0] < ci[s]['dq'][0] for s in SEEDS) >= 15
    cv, kv = GH('cero', 'invertido'), GH('completa', 'invertido')
    V['H4'] = sum(kv[s]['dq'][0] + kv[s]['dq'][1] > cv[s]['dq'][0] + cv[s]['dq'][1] for s in SEEDS) >= 15
    V['H5'] = sum(abs(kv[s]['W']['A'] + 3) < .3 and abs(kv[s]['W']['B'] - 1) < .15 for s in SEEDS) >= 15
    V['H2_sin_voto'] = bool(np.median(ven_p) <= 0.6 * np.median(ven_c))
    log(f"   H1 igual: veneno Q1 completa {np.median(ven_k):.1f} <= 0.5x cero {np.median(ven_c):.1f}; completa<cero "
        f"{sum(co[s]['mord']['B'][0] < ci[s]['mord']['B'][0] for s in SEEDS)}/20: {'SOSTENIDA' if V['H1'] else 'REFUTADA'}")
    log(f"   H3 igual: muertes Q1 completa<cero {sum(co[s]['dq'][0] < ci[s]['dq'][0] for s in SEEDS)}/20: {'SOSTENIDA' if V['H3'] else 'REFUTADA'}")
    log(f"   H4 invertido: muertes Q1+Q2 completa>cero {sum(kv[s]['dq'][0]+kv[s]['dq'][1] > cv[s]['dq'][0]+cv[s]['dq'][1] for s in SEEDS)}/20: "
        f"{'SOSTENIDA' if V['H4'] else 'REFUTADA'}")
    log(f"   H5 invertido: completa revierte al final {sum(abs(kv[s]['W']['A'] + 3) < .3 and abs(kv[s]['W']['B'] - 1) < .15 for s in SEEDS)}/20: "
        f"{'SOSTENIDA' if V['H5'] else 'REFUTADA'}")
    log(f"   H2 (sin voto) parcial veneno Q1 {np.median(ven_p):.1f} <= 0.6x cero: {V['H2_sin_voto']}")
    V['ETAPA4_CERRADA'] = all(V[k] for k in ('K_identidad', 'K_herencia_corre', 'M1', 'M2', 'M3', 'H1', 'H3', 'H4', 'H5'))
    log(); log("VEREDICTO etapa4_v9: " + " ".join(f"{k}={v}" for k, v in V.items()))

    meta = dict(fecha=time.strftime('%Y-%m-%dT%H:%M:%S'), semillas=SEEDS, veredictos=V, controles=rc, procesos_python=ps,
                sha_preregistro=h16(pre), sha_script=h16(os.path.abspath(__file__)),
                sha_constructor=h16(os.path.join(AQUI, 'construye_v9m.py')), sha_v9m=h16(os.path.join(AQUI, 'organismo_v9m.py')),
                sha_v9=h16(os.path.join(RAIZ, 'organismo', 'organismo_v9.py')),
                python=platform.python_version(), numpy=np.__version__, plataforma=platform.platform())
    sin_estado = [{k: v for k, v in r.items() if k != 'estado'} for r in r1] + r2
    dj = os.path.join(RAIZ, 'datos', f'etapa4_v9_{stamp}.json')
    json.dump(dict(meta=meta, corridas=sin_estado), open(dj, 'w', encoding='utf-8'), ensure_ascii=False, default=str)
    log(f"datos -> {os.path.basename(dj)}  sha256_16 = {h16(dj)}")
    _log['f'].close()
