"""v11 confirmatorio: Q0 (identidades), R (retencion, bloque M, semillas 41-60), V10 (replica ERR-17), K (capacidad 2K-bis).
X1 (examen) y Q5 (regresion) se corren aparte: bateria_v11.py 20 --desde 41 --log  y  bateria_v9.py 6.
Ejecuta PREREGISTRO_v11.md. REGLA 10: log desde el arranque. REGLA 11: procesos vivos. Igualdades NUMERICAS.
Precisiones escritas ANTES de correr:
- Bloque M = fases {50000: C veneno + D comida (A,B fuera), 100000: vuelven A,B}, T=150000.
- Hija en el codigo de B = indice >= 30 en codigos[100000]['B'].
- Empate en V10(a) = |dW_B(v10) - dW_B(v9)| < 1e-9.
- K: dev = |W - R| por checkpoint (como en corre_reverificacion.py); M_max y N* con las mismas funciones.
Uso:  python experimentos/v11_evo_division/corre_v11.py
"""
import sys, os, json, time, hashlib, platform, subprocess, importlib.util
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
import numpy as np

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
sys.path[:0] = [AQUI, os.path.join(RAIZ, 'organismo'), os.path.join(RAIZ, 'experimentos', 'v10_direccion_division'),
                os.path.join(RAIZ, 'experimentos', 'v9_reverificacion'), os.path.join(RAIZ, 'experimentos', 'ramas', '2Kbis_capacidad')]
GENOMA = os.path.join(RAIZ, 'experimentos', 'evo', 'gen1', 'llm_2', 'organismo.py')
SEEDS = list(range(41, 61))
FASES = {50000: (['C', 'D'], {'C': 'veneno', 'D': 'comida'}), 100000: (['A', 'B'], {'A': 'comida', 'B': 'veneno'})}
ESC_Q0 = {'E1': dict(), 'E2': dict(invertir_en=50000), 'E2L': dict(solap_AB=3), 'M': dict(T=150000, fases=FASES)}
PLAN0 = [(0, 'A', 'comida'), (0, 'B', 'veneno')]
ESC_CAP = {'E1': dict(plan=PLAN0), 'C_veneno_50k': dict(plan=PLAN0 + [(50000, 'C', 'veneno')]),
           'D_comida_50k': dict(plan=PLAN0 + [(50000, 'D', 'comida')])}
BRAZOS_M = {'v9': dict(mu_norm=False, div_signo=False), 'v10': dict(div_signo=False), 'v11': dict()}
BRAZOS_K = {'v10': dict(mu_norm=True, div_signo=False), 'v11': dict(mu_norm=True, div_signo=True)}
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


def genoma():
    spec = importlib.util.spec_from_file_location('genoma_llm2', GENOMA)
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m


def iguales(a, b, claves=None):
    ks = claves or list(a)
    d = [k for k in ks if N(a[k]) != N(b[k])]
    return not d, d


def tarea(args):
    tipo = args[0]
    if tipo == 'Q0gen':
        _, esc, s = args
        import organismo_v11m as m
        ok, d = iguales(genoma().run(s, **ESC_Q0[esc]), m.run(s, **ESC_Q0[esc]))
        return dict(tipo=tipo, esc=esc, seed=s, identico=ok, difieren=d)
    if tipo == 'Q0v10m':
        _, esc, s = args
        import organismo_v11m as m, organismo_v10m as m10
        ok, d = iguales(m10.run(s, **ESC_Q0[esc]), m.run(s, div_signo=False, **ESC_Q0[esc]))
        return dict(tipo=tipo, esc=esc, seed=s, identico=ok, difieren=d)
    if tipo == 'KK1':
        _, esc, s = args
        import organismo_caph9 as c9, organismo_caph11 as c11, parte2_capacidad as P
        kw = (dict(T=P.T_de(20000, 6), plan=P.plan_de(20000, 6), pats=P.PATS, chk=P.chks(20000, 6)) if esc == 'corto6' else ESC_CAP[esc])
        ok, d = iguales(c9.run(s, lam=0.05, **kw), c11.run(s, lam=0.05, **kw))
        return dict(tipo=tipo, esc=esc, seed=s, identico=ok, difieren=d)
    if tipo == 'KK1b':
        _, s = args
        import organismo_caph11 as c11, organismo_v11 as v11
        ok, d = iguales(v11.run(s), c11.run(s, lam=0.05, mu_norm=True, div_signo=True),
                        ['W', 'mord', 'vis', 'deaths', 'splits', 'celdas', 'split_t'])
        return dict(tipo=tipo, esc='E1', seed=s, identico=ok, difieren=d)
    if tipo == 'M':
        _, brazo, s = args
        import organismo_v11m as m
        r = m.run(s, T=150000, fases=FASES, **BRAZOS_M[brazo])
        return dict(tipo='M', brazo=brazo, seed=s, sondas=r['sondas'], codigos=r['codigos'], primer=r['primer'],
                    splits=r['splits'], deaths=r['deaths'], celdas=r['celdas'])
    _, brazo, pt, s = args
    import organismo_caph11 as c11, parte2_capacidad as P
    r = c11.run(s, T=P.T_de(pt), plan=P.plan_de(pt), pats=P.PATS, chk=P.chks(pt), plast=True, lam=0.05, memoria_rechazo=20, **BRAZOS_K[brazo])
    for h in r['hist']:
        h['dev'] = {k: round(abs(v - P.R[k]), 3) for k, v in h['W'].items()}
    return dict(tipo='K', brazo=brazo, pt=pt, seed=s, hist=r['hist'], deaths=r['deaths'], t_agot=r['t_agot'],
                splits=r['splits'], celdas=r['celdas'])


def m_max(hist):
    return max(sum(1 for v in h['dev'].values() if v <= 0.3) for h in hist)


def med(xs):
    return float(np.median(xs)), float(min(xs)), float(max(xs))


if __name__ == '__main__':
    import multiprocessing as mp
    mp.set_start_method('spawn', force=True)
    import parte2_capacidad as P
    stamp = time.strftime('%Y%m%d_%H%M%S')
    _log['f'] = open(os.path.join(RAIZ, 'datos', f'v11_confirmatorio_{stamp}.log'), 'w', encoding='utf-8', newline='\n')
    pre = os.path.join(AQUI, 'PREREGISTRO_v11.md')
    shas = {n: h16(p) for n, p in [('preregistro', pre), ('script', os.path.abspath(__file__)), ('genoma', GENOMA),
            ('v11', os.path.join(RAIZ, 'organismo', 'organismo_v11.py')), ('v11m', os.path.join(AQUI, 'organismo_v11m.py')),
            ('caph11', os.path.join(AQUI, 'organismo_caph11.py')), ('v10', os.path.join(RAIZ, 'organismo', 'organismo_v10.py')),
            ('v9', os.path.join(RAIZ, 'organismo', 'organismo_v9.py'))]}
    log(f"ARRANQUE v11 confirmatorio. semillas {SEEDS[0]}..{SEEDS[-1]}. Pool({N_PARALELO}).")
    log("sha " + "  ".join(f"{k} {v}" for k, v in shas.items()))
    try:
        ps = subprocess.run(['powershell', '-NoProfile', '-Command',
                             "Get-CimInstance Win32_Process | Where-Object { $_.Name -like 'python*' } | ForEach-Object { \"$($_.ProcessId) $($_.CommandLine)\" }"],
                            capture_output=True, text=True, timeout=60).stdout.strip().splitlines()
    except Exception as e:
        ps = [f"(no se pudo listar: {e})"]
    log(f"REGLA 11 — procesos python vivos ({len(ps)}), este es pid {os.getpid()}:")
    for l in ps:
        log(f"    {l[:160]}")
    V = {}
    with mp.Pool(N_PARALELO) as pool:
        ctrl = ([('Q0gen', e, s) for e in ESC_Q0 for s in (1, 2, 3)] + [('Q0v10m', e, s) for e in ('E1', 'E2', 'M') for s in (1, 2, 3)]
                + [('KK1', e, s) for e in list(ESC_CAP) + ['corto6'] for s in (1, 2, 3)] + [('KK1b', s) for s in (1, 2, 3)])
        log(f"ETAPA 1/4 — Q0 identidades ({len(ctrl)})...")
        rc = pool.map(tarea, ctrl, chunksize=1)
        for t, nombre in (('Q0gen', 'v11m == genoma gen1/llm_2'), ('Q0v10m', 'v11m(div_signo=False) == v10m'),
                          ('KK1', 'caph11(F,F) == caph9'), ('KK1b', 'caph11(T,T) == v11 (E1)')):
            g = [x for x in rc if x['tipo'] == t]
            log(f"  {nombre:32s}: {sum(x['identico'] for x in g)}/{len(g)}")
            for x in g:
                if not x['identico']:
                    log(f"      DIFIERE {x}")
        V['Q0'] = all(x['identico'] for x in rc)
        if not V['Q0']:
            log("*** Q0 FALLIDO: se para."); sys.exit(1)
        trabajos = ([('K', b, pt, s) for pt in (60000, 20000) for b in BRAZOS_K for s in SEEDS]
                    + [('M', b, s) for b in BRAZOS_M for s in SEEDS])
        log(f"ETAPA 2/4 — {len(trabajos)} corridas (K: 80 largas primero; M: 60)...")
        res = []
        for i, r in enumerate(pool.imap_unordered(tarea, trabajos, chunksize=1), 1):
            res.append(r)
            if i % 10 == 0 or i == len(trabajos):
                log(f"          {i}/{len(trabajos)}")
    log("ETAPA 3/4 — analisis.")
    GM = lambda b: {r['seed']: r for r in res if r['tipo'] == 'M' and r['brazo'] == b}
    g9, g10, g11 = GM('v9'), GM('v10'), GM('v11')
    S100 = lambda r, k: r['sondas'][100000][k]
    conj = lambda g: sum(S100(g[s], 'B') <= -2 and S100(g[s], 'A') >= 0.5 for s in SEEDS)
    c9, c10, c11 = conj(g9), conj(g10), conj(g11)
    V['R1'] = c11 >= 16; V['R2'] = c11 - c10 >= 6
    gC = sum(S100(g11[s], 'C') <= -2.5 and S100(g11[s], 'D') >= 0.85 for s in SEEDS); V['R3'] = gC >= 18
    cod = sum(g11[s]['codigos'][100000]['A'] == g11[s]['codigos'][50000]['A'] and g11[s]['codigos'][100000]['B'] == g11[s]['codigos'][50000]['B'] for s in SEEDS)
    V['R4_mecanismo'] = cod >= 14
    log(); log(f"  BLOQUE R (retencion, bloque M, semillas {SEEDS[0]}-{SEEDS[-1]})")
    for b, g in (('v9', g9), ('v10', g10), ('v11', g11)):
        log(f"   {b:4s} conjunta {conj(g):2d}/20  W_B>=... W_B<=-2 {sum(S100(g[s],'B') <= -2 for s in SEEDS):2d}  W_A>=0.5 {sum(S100(g[s],'A') >= 0.5 for s in SEEDS):2d}"
            f"  W_B mediana {np.median([S100(g[s],'B') for s in SEEDS]):+.2f}  W_A {np.median([S100(g[s],'A') for s in SEEDS]):+.2f}"
            f"  W_C {np.median([S100(g[s],'C') for s in SEEDS]):+.2f}  W_D {np.median([S100(g[s],'D') for s in SEEDS]):+.2f}"
            f"  muerde B al volver {sum(bool(g[s]['primer'].get('100000|B', {}).get('mordio')) for s in SEEDS):2d}"
            f"  divisiones {np.median([g[s]['splits'] for s in SEEDS]):.0f}  celdas {np.median([g[s]['celdas'] for s in SEEDS]):.0f}  muertes {np.median([g[s]['deaths'] for s in SEEDS]):.0f}")
    log(f"  R1 v11 conjunta {c11}/20 (>=16): {'SOSTENIDA' if V['R1'] else 'REFUTADA'}")
    log(f"  R2 v11 - v10 = {c11 - c10:+d} (>=+6): {'SOSTENIDA' if V['R2'] else 'REFUTADA'}")
    log(f"  R3 guarda W_C<=-2.5 y W_D>=0.85 {gC}/20 (>=18): {'SOSTENIDA' if V['R3'] else 'REFUTADA'}")
    log(f"  R4 [mecanismo, vocabulario] codigos de A y B intactos 50k->100k {cod}/20 (>=14): {'SOSTENIDA' if V['R4_mecanismo'] else 'REFUTADA'}")
    dW = lambda r: r['sondas'][100000]['B'] - r['sondas'][50000]['B']
    no_emp = [s for s in SEEDS if abs(dW(g10[s]) - dW(g9[s])) >= 1e-9]
    a_ = sum(dW(g10[s]) < dW(g9[s]) for s in no_emp)
    hija = lambda r: any(i >= 30 for i in r['codigos'][100000]['B'])
    h9, h10 = sum(hija(g9[s]) for s in SEEDS), sum(hija(g10[s]) for s in SEEDS)
    peor = sum(dW(g10[s]) > dW(g9[s]) + 0.5 for s in SEEDS)
    V['V10a'] = len(no_emp) > 0 and a_ >= 0.7 * len(no_emp); V['V10b'] = h10 <= h9 / 2 and h10 <= 9; V['V10c'] = peor <= 2
    log(); log(f"  V10 (replica ERR-17): (a) v10<v9 en {a_}/{len(no_emp)} no empatados (>=70%): {V['V10a']}; (b) hijas en B v9 {h9}, v10 {h10}"
             f" (<=mitad y <=9): {V['V10b']}; (c) v10 peor por >0.5 en {peor} (<=2): {V['V10c']}")
    log(); log(f"  BLOQUE K (capacidad 2K-bis, semillas {SEEDS[0]}-{SEEDS[-1]})")
    GK = lambda b, pt: {r['seed']: r for r in res if r['tipo'] == 'K' and r['brazo'] == b and r['pt'] == pt}
    tab = {}
    for pt in (20000, 60000):
        for b in BRAZOS_K:
            g = GK(b, pt)
            Ns = [P.techo(g[s]['hist']) for s in SEEDS]; Ms = [m_max(g[s]['hist']) for s in SEEDS]
            fin = [v for s in SEEDS for v in g[s]['hist'][-1]['W'].values()]
            ceros = sum(abs(v) < 0.0005 for v in fin)
            tab[(b, pt)] = dict(N=med(Ns)[0], M=med(Ms)[0], ceros=ceros)
            log(f"   {pt//1000}k {b:4s}: N* {med(Ns)[0]:.1f} [{med(Ns)[1]:.0f},{med(Ns)[2]:.0f}]  M_max {med(Ms)[0]:.1f} [{med(Ms)[1]:.0f},{med(Ms)[2]:.0f}]"
                f"  W=0 {ceros}/{len(fin)}  agotan {sum(g[s]['t_agot'] is not None for s in SEEDS)}/20  celdas {med([g[s]['celdas'] for s in SEEDS])[0]:.0f}"
                f"  divisiones {med([g[s]['splits'] for s in SEEDS])[0]:.0f}  muertes {med([g[s]['deaths'] for s in SEEDS])[0]:.0f}")
    V['K1'] = tab[('v11', 20000)]['ceros'] <= 20
    V['K2'] = all(tab[('v11', pt)]['M'] >= tab[('v10', pt)]['M'] - 1 for pt in (20000, 60000))
    V['K3'] = all(tab[('v11', pt)]['N'] >= tab[('v10', pt)]['N'] - 1 for pt in (20000, 60000))
    for k in ('K1', 'K2', 'K3'):
        log(f"  {k}: {'SOSTENIDA' if V[k] else 'REFUTADA'}")
    log(); log("VEREDICTO v11_confirmatorio: " + " ".join(f"{k}={v}" for k, v in V.items()) + "   (X1 y Q5 aparte)")
    log("ETAPA 4/4 — escritura.")
    meta = dict(fecha=time.strftime('%Y-%m-%dT%H:%M:%S'), semillas=SEEDS, veredictos=V, Q0=rc, procesos_python=ps, shas=shas,
                python=platform.python_version(), numpy=np.__version__)
    dj = os.path.join(RAIZ, 'datos', f'v11_confirmatorio_{stamp}.json')
    json.dump(dict(meta=meta, corridas=res), open(dj, 'w', encoding='utf-8'), ensure_ascii=False, default=str)
    log(f"datos -> {os.path.basename(dj)}  sha256_16 = {h16(dj)}")
    _log['f'].close()
