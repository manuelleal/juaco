"""v10 = v9 + mu normalizada. Confirmatorio: Q0 (identidad), Q3 (via estructural, semillas 21-40), Q4 (retencion con guarda).
Q1/Q2 los da bateria_v10.py 20 --log (examen). Ejecuta PREREGISTRO_v10.md (0e035dc12f3fffd3).

REGLA 10: log desde el arranque (datos/v10_confirmatorio_<fecha>.log). REGLA 11: procesos vivos. Igualdades NUMERICAS.
Precisiones escritas ANTES de correr:
- Bloque M = fases {50000: C veneno + D comida (A,B fuera), 100000: vuelven A,B}, T=150000, como en la Etapa 4.
- "Hija en el codigo de B en 100k" = algun indice >= 30 en codigos[100000]['B'] (las 30 primeras celdas son las de
  nacimiento; toda celda >= 30 nace por division).
- Q3b: dW_B = sondas[100000]['B'] - sondas[50000]['B']; v10 < v9 estricto por semilla; y nunca dW_B(v10) > dW_B(v9)+0.5.
- Q4 guarda: W_C y W_D leidos en sondas[100000] (justo antes de que vuelvan A y B).
Uso:  python experimentos/v10_direccion_division/corre_v10.py
"""
import sys, os, json, time, hashlib, platform, subprocess
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
import numpy as np

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
sys.path[:0] = [AQUI, os.path.join(RAIZ, 'organismo')]
SEEDS = list(range(21, 41))
FASES = {50000: (['C', 'D'], {'C': 'veneno', 'D': 'comida'}), 100000: (['A', 'B'], {'A': 'comida', 'B': 'veneno'})}
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


def tarea(args):
    tipo = args[0]
    if tipo == 'Q0a':
        _, esc, seed = args
        import organismo_v9 as v9, organismo_v10 as v10
        a, b = v9.run(seed, **ESC_ID[esc]), v10.run(seed, mu_norm=False, **ESC_ID[esc])
        return dict(tipo=tipo, esc=esc, seed=seed, identico=all(N(a[k]) == N(b[k]) for k in a), difieren=[k for k in a if N(a[k]) != N(b[k])])
    if tipo == 'Q0b':
        _, esc, seed = args
        import organismo_v10 as v10, organismo_v10m as m
        a, b = v10.run(seed, **ESC_ID[esc]), m.run(seed, **ESC_ID[esc])
        return dict(tipo=tipo, esc=esc, seed=seed, identico=all(N(a[k]) == N(b[k]) for k in a), difieren=[k for k in a if N(a[k]) != N(b[k])])
    _, ver, seed = args
    import organismo_v10m as m
    r = m.run(seed, T=150000, fases=FASES, mu_norm=(ver == 'v10'))
    return dict(tipo='M', ver=ver, seed=seed, sondas=r['sondas'], codigos=r['codigos'], primer=r['primer'], splits=r['splits'],
                deaths=r['deaths'], celdas=r['celdas'])


if __name__ == '__main__':
    import multiprocessing as mp
    mp.set_start_method('spawn', force=True)
    stamp = time.strftime('%Y%m%d_%H%M%S')
    _log['f'] = open(os.path.join(RAIZ, 'datos', f'v10_confirmatorio_{stamp}.log'), 'w', encoding='utf-8', newline='\n')
    pre = os.path.join(AQUI, 'PREREGISTRO_v10.md')
    log(f"ARRANQUE v10 confirmatorio (Q0, Q3, Q4). semillas {SEEDS[0]}..{SEEDS[-1]}. Pool({N_PARALELO}).")
    log(f"sha preregistro {h16(pre)}  script {h16(os.path.abspath(__file__))}  v10 {h16(os.path.join(RAIZ, 'organismo', 'organismo_v10.py'))}"
        f"  v10m {h16(os.path.join(AQUI, 'organismo_v10m.py'))}  v9 {h16(os.path.join(RAIZ, 'organismo', 'organismo_v9.py'))}")
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
        ctrl = [('Q0a', e, s) for e in ESC_ID for s in range(1, 7)] + [('Q0b', e, s) for e in ('E1', 'E2') for s in range(1, 4)]
        log(f"ETAPA 1/3 — Q0 identidades ({len(ctrl)})...")
        rc = pool.map(tarea, ctrl, chunksize=1)
        for t in ('Q0a', 'Q0b'):
            g = [x for x in rc if x['tipo'] == t]
            log(f"  {t} {'v10(mu_norm=False)==v9' if t == 'Q0a' else 'v10m==v10':24s}: {sum(x['identico'] for x in g)}/{len(g)}")
            for x in g:
                if not x['identico']:
                    log(f"      DIFIERE {x}")
        V['Q0'] = all(x['identico'] for x in rc)
        if not V['Q0']:
            log("*** Q0 FALLIDO: se para."); sys.exit(1)
        trabajos = [('M', v, s) for v in ('v9', 'v10') for s in SEEDS]
        log(f"ETAPA 2/3 — bloque M, {len(trabajos)} corridas (v9 y v10 con la misma instrumentacion)...")
        res = []
        for i, r in enumerate(pool.imap_unordered(tarea, trabajos, chunksize=1), 1):
            res.append(r)
            if i % 10 == 0 or i == len(trabajos):
                log(f"          {i}/{len(trabajos)}")
    log("ETAPA 3/3 — analisis.")
    G = lambda v: {r['seed']: r for r in res if r['ver'] == v}
    g9, g10 = G('v9'), G('v10')
    hija = lambda r: any(i >= 30 for i in r['codigos'][100000]['B'])
    h9, h10 = sum(hija(g9[s]) for s in SEEDS), sum(hija(g10[s]) for s in SEEDS)
    dW = lambda r: r['sondas'][100000]['B'] - r['sondas'][50000]['B']
    menor = sum(dW(g10[s]) < dW(g9[s]) for s in SEEDS); peor = sum(dW(g10[s]) > dW(g9[s]) + 0.5 for s in SEEDS)
    V['Q3'] = h9 >= 10 and h10 <= 5 and menor >= 12 and peor == 0
    log(f"  Q3 hijas en codigo(B) en 100k: v9 {h9}/20 (>=10), v10 {h10}/20 (<=5); dW_B v10<v9 en {menor}/20 (>=12), v10 peor por >0.5 en {peor} (==0)"
        f" -> {'SOSTENIDA' if V['Q3'] else 'REFUTADA'}")
    log(f"      dW_B mediana: v9 {np.median([dW(g9[s]) for s in SEEDS]):+.3f}  v10 {np.median([dW(g10[s]) for s in SEEDS]):+.3f};"
        f"  splits en la corrida: v9 {np.median([g9[s]['splits'] for s in SEEDS]):.0f}  v10 {np.median([g10[s]['splits'] for s in SEEDS]):.0f}")
    rB9, rB10 = sum(g9[s]['sondas'][100000]['B'] <= -2 for s in SEEDS), sum(g10[s]['sondas'][100000]['B'] <= -2 for s in SEEDS)
    rA9, rA10 = sum(g9[s]['sondas'][100000]['A'] >= 0.5 for s in SEEDS), sum(g10[s]['sondas'][100000]['A'] >= 0.5 for s in SEEDS)
    gC = sum(g10[s]['sondas'][100000]['C'] <= -2.5 for s in SEEDS); gD = sum(g10[s]['sondas'][100000]['D'] >= 0.85 for s in SEEDS)
    V['Q4_guarda'] = gC >= 17 and gD >= 17
    V['Q4'] = rB10 >= rB9 and rB10 >= 8 and V['Q4_guarda']
    log(f"  Q4 retencion W_B<=-2: v9 {rB9}/20, v10 {rB10}/20 (v10>=v9 y >=8); W_A>=0.5: v9 {rA9}, v10 {rA10};"
        f" guarda W_C<=-2.5 {gC}/20, W_D>=0.85 {gD}/20 (>=17) -> {'SOSTENIDA' if V['Q4'] else 'REFUTADA'}")
    log(f"      W_B(100k) mediana: v9 {np.median([g9[s]['sondas'][100000]['B'] for s in SEEDS]):+.2f}  v10 {np.median([g10[s]['sondas'][100000]['B'] for s in SEEDS]):+.2f};"
        f"  muerde B al reencuentro: v9 {sum(bool(g9[s]['primer'].get('100000|B', {}).get('mordio')) for s in SEEDS)}, v10 {sum(bool(g10[s]['primer'].get('100000|B', {}).get('mordio')) for s in SEEDS)};"
        f"  muertes v9 {np.median([g9[s]['deaths'] for s in SEEDS]):.0f} v10 {np.median([g10[s]['deaths'] for s in SEEDS]):.0f}")
    log(); log("VEREDICTO v10_confirmatorio: " + " ".join(f"{k}={v}" for k, v in V.items()) + "   (Q1, Q2 en bateria_v10.py 20 --log)")
    meta = dict(fecha=time.strftime('%Y-%m-%dT%H:%M:%S'), semillas=SEEDS, veredictos=V, Q0=rc, procesos_python=ps,
                sha_preregistro=h16(pre), sha_script=h16(os.path.abspath(__file__)), sha_constructor=h16(os.path.join(AQUI, 'construye_v10.py')),
                sha_v10=h16(os.path.join(RAIZ, 'organismo', 'organismo_v10.py')), sha_v10m=h16(os.path.join(AQUI, 'organismo_v10m.py')),
                sha_v9=h16(os.path.join(RAIZ, 'organismo', 'organismo_v9.py')), python=platform.python_version(), numpy=np.__version__)
    dj = os.path.join(RAIZ, 'datos', f'v10_confirmatorio_{stamp}.json')
    json.dump(dict(meta=meta, corridas=res), open(dj, 'w', encoding='utf-8'), ensure_ascii=False, default=str)
    log(f"datos -> {os.path.basename(dj)}  sha256_16 = {h16(dj)}")
    _log['f'].close()
