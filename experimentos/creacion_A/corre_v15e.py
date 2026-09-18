"""Candidato v15e: la tabla de pares REESCRIBIBLE (sin doble cuenta) en la via lenta del tronco. Ejecuta PREREGISTRO_v15e.md.
REGLA 10: log desde el arranque. REGLA 11: lista los python vivos antes del Pool. Nunca dos Pool a la vez.

ETAPA 1  identidad interna (`identidad_v15e.py` como SUBPROCESO, un proceso): I1 v15e(None) == v14.1 (24), I2 rng no consumido (2),
         I3 v15ge(None) == v14g con los kwargs exactos del tronco (6) -> 32/32 o se para.
ETAPA 2  V1 examen del criterio v3' (`bateria_v15e.py 20 --desde 101 --log`, SUBPROCESO; trae su propio Pool).
ETAPA 3  V2a generalizacion (`bateria_generaliza_v15e.py organismo_v15e_on 20 --desde 101 --log`, SUBPROCESO).
ETAPA 4  V2b mundo de regla 141-160 con la memoria ON y OFF pareadas, con los kwargs EXACTOS de la entrada del tronco
         (regla 14): xor01 (DOS puntuaciones), px0 y azar. Pool aqui.
ETAPA 5  umbrales del preregistro (§5) y JSON.

Uso:  python experimentos/creacion_A/corre_v15e.py [--desde N]
      python experimentos/creacion_A/corre_v15e.py --humo   (UN proceso, sin Pool: identidad corta + E1/E2 a mano + 1 semilla de regla)
"""
import sys, os, re, json, time, hashlib, platform, subprocess
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
import numpy as np

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
sys.path[:0] = [os.path.join(RAIZ, 'organismo'), AQUI]   # organismo/ PRIMERO (ERR-28)
_desde = int(sys.argv[sys.argv.index('--desde') + 1]) if '--desde' in sys.argv else 141
SEEDS = list(range(_desde, _desde + 20))
HUMO = '--humo' in sys.argv
REGLAS = ['xor01', 'px0', 'azar']
MODOS = ['suma', None]   # v15e: el candidato y el apagado (== v14.1), pareados
# Regla 14 (ERR-38): en el mundo de regla, los kwargs EXACTOS de la entrada 'organismo_v14' de bateria_generaliza.py
KW14 = dict(eta_s=0.15, clip_s=10.0, puerta=3, mask_rel=2, del_s=0.25, del_c=0.25, ema_c=0.05, puerta_pat=5, pat_shuf=0, pat_min=1)
HUMO_SEEDS = (101, 102)   # E1/E2 a mano (el examen usa 101-120)
N_PARALELO = 14
_log = {'f': None, 't0': time.time()}


def log(msg=""):
    linea = f"[{time.strftime('%H:%M:%S')} +{time.time()-_log['t0']:7.1f}s] {msg}"
    print(linea, flush=True)
    if _log['f']:
        _log['f'].write(linea + "\n"); _log['f'].flush(); os.fsync(_log['f'].fileno())


def h16(p):
    return hashlib.sha256(open(p, 'rb').read()).hexdigest()[:16]


def f3(x, n=3):
    return '  n/a' if x is None else f"{x:.{n}f}"


def med(xs):
    xs = [x for x in xs if x is not None]
    if not xs:
        return None, None, None
    return float(np.median(xs)), float(min(xs)), float(max(xs))


def acc_dos(Wd, test, vr):
    """(registro, ESTRICTA). Registro: valor 0 exacto = 0.5. Estricta: valor 0 = FALLO (la abstencion no puntua)."""
    out = []
    for medio in (0.5, 0.0):
        f = [1.0 if Wd[k] > 0 else (medio if Wd[k] == 0 else 0.0) for k in test if vr[k] == 'comida']
        p = [1.0 if Wd[k] < 0 else (medio if Wd[k] == 0 else 0.0) for k in test if vr[k] == 'veneno']
        out.append(None if (not f or not p) else 0.5 * float(np.mean(f)) + 0.5 * float(np.mean(p)))
    return out[0], out[1]


def tarea(args):
    """Una corrida del mundo de regla con la memoria ENCENDIDA (o su gemela APAGADA, pareada), kwargs exactos del tronco."""
    regla, seed, mem = args
    import organismo_v15ge as m
    r = m.run(seed, T=200000, mundo='regla', regla=regla, memoria_pares=mem, **KW14)
    vr = m.split_regla(seed, regla)[3]; test = r['test']
    a_reg, a_est = acc_dos(r['W_apriori'], test, vr)
    pf = [r['primer'][k]['pb'] for k in test if r['primer'].get(k) is not None and vr[k] == 'comida']
    pp = [1 - r['primer'][k]['pb'] for k in test if r['primer'].get(k) is not None and vr[k] == 'veneno']
    return dict(regla=regla, seed=seed, memoria=mem, acc=a_reg, acc_estricta=a_est,
                ba=(0.5 * float(np.mean(pf)) + 0.5 * float(np.mean(pp))) if (pf and pp) else None,
                cobertura_test=sum(v is not None for v in r['primer'].values()),
                ganadora=r['mem_ganadora'], cobertura=r['mem_cobertura'], vistas=r['mem_vistas'],
                celdas=r['celdas'], splits=r['splits'], deaths=r['deaths'])


# ---------- humo: E1 y E2 a mano, cuatro organismos pareados ----------
ORGS = [('v14.1 (off)', 'organismo_v15e', dict(memoria_pares=None)),
        ('v15d suma a=0.3', 'organismo_v15d', dict(memoria_pares='suma')),
        ('v15d suma a=1.0', 'organismo_v15d', dict(memoria_pares='suma', mem_alfa=1.0)),
        ('v15e suma', 'organismo_v15e', dict(memoria_pares='suma'))]
ESC = {'E1': dict(), 'E2': dict(invertir_en=50000)}
CRIT = {'E1': lambda r: (abs(r['W']['B'] + 3) < .3, abs(r['W']['A'] - 1) < .15, r['mord']['B'][3] < r['mord']['B'][0]),
        'E2': lambda r: (abs(r['W']['A'] + 3) < .3, abs(r['W']['B'] - 1) < .15, r['mord']['B'][3] >= 50)}
NOM = {'E1': ('W_B≈-3', 'W_A≈+1', 'venQ4<Q1'), 'E2': ('W_A→-3', 'W_B→+1', 'comeB Q4≥50')}


def tarea_examen(org, esc, seed):
    etq, mod, kw = org
    import importlib
    m = importlib.import_module(mod)
    r = m.run(seed, T=100000, **ESC[esc], **kw)
    return dict(org=etq, esc=esc, seed=seed, W=r['W'], W_lenta=r['W_lenta'], W_tabla=r.get('W_tabla'), comp=r['comp'],
                fam=r.get('mem_fam'), ev=r.get('mem_ev'), mord=r['mord'], vis=r['vis'], deaths=r['deaths'],
                splits=r['splits'], celdas=r['celdas'], ganadora=r.get('mem_ganadora'),
                pasa=[bool(x) for x in CRIT[esc](r)])


def linea_examen(r):
    esc = r['esc']; fam = r['fam'] or {}; ev = r['ev'] or {}; tb = r['W_tabla'] or {}
    k = 'B' if esc == 'E1' else 'A'
    base = (f"   {esc} s{r['seed']} {r['org']:16s} W_A {r['W']['A']:+6.2f} W_B {r['W']['B']:+6.2f} | lineal A {r['W_lenta']['A']:+6.2f} B {r['W_lenta']['B']:+6.2f}"
            f" | residuo A {f3(tb.get('A'),2) if tb else '  --'} B {f3(tb.get('B'),2) if tb else '  --'}"
            f" | rapida A {r['comp']['A']} B {r['comp']['B']} | familiar A {fam.get('A')} B {fam.get('B')} (ev {ev.get('A')},{ev.get('B')})"
            f" | mord A {r['mord']['A']} B {r['mord']['B']} | vis B {r['vis']['B']} | splits {r['splits']} muertes {r['deaths']}")
    return base + "  => " + " ".join(f"{n}:{'si' if p else 'NO'}" for n, p in zip(NOM[esc], r['pasa']))


def sub(cmd, etq):
    log(f"   -> SUBPROCESO ({etq}): {' '.join(cmd[1:])}")
    t0 = time.time()
    p = subprocess.run([sys.executable] + cmd[1:], capture_output=True, text=True, cwd=AQUI, encoding='utf-8', errors='replace')
    cola = [l for l in (p.stdout or '').strip().splitlines()[-16:]]
    for l in cola: log(f"      | {l}")
    if p.returncode != 0:
        log(f"      *** codigo {p.returncode}; stderr: {(p.stderr or '')[-600:]}")
    log(f"      ({time.time()-t0:.0f}s)")
    return dict(etq=etq, cmd=cmd[1:], returncode=p.returncode, cola=cola, stdout=(p.stdout or '')[-6000:])


def num(patron, texto, default=None):
    m = re.search(patron, texto)
    return float(m.group(1)) if m else default


if __name__ == '__main__':
    stamp = time.strftime('%Y%m%d_%H%M%S')
    nom = f"v15e_humo_{stamp}" if HUMO else f"v15e_s{SEEDS[0]}-{SEEDS[-1]}_{stamp}"
    _log['f'] = open(os.path.join(RAIZ, 'datos', nom + '.log'), 'w', encoding='utf-8', newline='\n')
    pre = os.path.join(AQUI, 'PREREGISTRO_v15e.md')
    log(f"ARRANQUE v15e ({'HUMO, un proceso, sin Pool' if HUMO else f'semillas V2b {SEEDS[0]}-{SEEDS[-1]}; V1/V2a 101-120'}).")
    log(f"sha preregistro {h16(pre) if os.path.exists(pre) else '(falta)'}  script {h16(os.path.abspath(__file__))}"
        f"  construye_v15e {h16(os.path.join(AQUI,'construye_v15e.py'))}"
        f"  organismo_v15e {h16(os.path.join(AQUI,'organismo_v15e.py'))}"
        f"  organismo_v15e_on {h16(os.path.join(AQUI,'organismo_v15e_on.py'))}"
        f"  organismo_v15ge {h16(os.path.join(AQUI,'organismo_v15ge.py'))}"
        f"  organismo_v15ge_on {h16(os.path.join(AQUI,'organismo_v15ge_on.py'))}"
        f"  bateria_v15e {h16(os.path.join(AQUI,'bateria_v15e.py'))}"
        f"  bateria_generaliza_v15e {h16(os.path.join(AQUI,'bateria_generaliza_v15e.py'))}"
        f"  identidad_v15e {h16(os.path.join(AQUI,'identidad_v15e.py'))}"
        f"  ORIGEN organismo_v14 {h16(os.path.join(RAIZ,'organismo','organismo_v14.py'))}"
        f"  organismo_v14g {h16(os.path.join(RAIZ,'organismo','organismo_v14g.py'))}"
        f"  bateria_v14 {h16(os.path.join(RAIZ,'organismo','bateria_v14.py'))}"
        f"  bateria_generaliza {h16(os.path.join(RAIZ,'organismo','bateria_generaliza.py'))}"
        f"  (comparador) organismo_v15d {h16(os.path.join(AQUI,'organismo_v15d.py'))}")
    log(f"kwargs del mundo de regla (regla 14, = entrada 'organismo_v14' de bateria_generaliza): {KW14}")
    V = {}
    if HUMO:
        log("ETAPA 1/3 — identidad corta (T=20000, un proceso).")
        r1 = sub([sys.executable, os.path.join(AQUI, 'identidad_v15e.py'), '20000'], 'identidad')
        V['identidad'] = next((l for l in r1['cola'] if 'IDENTIDAD' in l), None)
        log(f"ETAPA 2/3 — E1 y E2 a mano (T=100000), semillas {HUMO_SEEDS}, cuatro organismos pareados.")
        rex = []
        for esc in ('E1', 'E2'):
            for seed in HUMO_SEEDS:
                for org in ORGS:
                    r = tarea_examen(org, esc, seed); rex.append(r); log(linea_examen(r))
        log(f"ETAPA 3/3 — mundo de regla, semilla {_desde}, memoria ON y OFF (pareado, kwargs del tronco), T=200000.")
        res = [tarea((rg, _desde, mem)) for rg in REGLAS for mem in MODOS]
        for r in res:
            log(f"   {r['regla']:6s} memoria={str(r['memoria']):5s} s{r['seed']}: registro {f3(r['acc'])}  "
                f"ESTRICTA {f3(r['acc_estricta'])}  ba {f3(r['ba'])}  ganadora {r['ganadora']}  "
                f"cobertura {r['cobertura']}/4  celdas {r['celdas']}  splits {r['splits']}  muertes {r['deaths']}")
        log("Las baterias NO se corren en el humo (traen su propio Pool). Comandos para el coordinador (secuenciales):")
        log("   python experimentos/creacion_A/corre_v15e.py        (identidad -> V1 -> V2a -> V2b 141-160)")
        dj = os.path.join(RAIZ, 'datos', nom + '.json')
        json.dump(dict(meta=dict(fecha=time.strftime('%Y-%m-%dT%H:%M:%S'), humo=True, semillas_examen=HUMO_SEEDS, semilla_regla=_desde,
                                 kw14=KW14, python=platform.python_version(), numpy=np.__version__,
                                 sha_preregistro=h16(pre) if os.path.exists(pre) else None, sha_script=h16(os.path.abspath(__file__)),
                                 sha_v15e=h16(os.path.join(AQUI, 'organismo_v15e.py')), sha_v15ge=h16(os.path.join(AQUI, 'organismo_v15ge.py'))),
                       identidad=r1, examen=rex, regla=res), open(dj, 'w', encoding='utf-8'), ensure_ascii=False, default=str)
        log(f"datos -> {os.path.basename(dj)}  sha256_16 = {h16(dj)}")
        _log['f'].close(); sys.exit(0)

    try:
        ps = subprocess.run(['powershell', '-NoProfile', '-Command',
                             "Get-CimInstance Win32_Process | Where-Object { $_.Name -like 'python*' } | ForEach-Object { \"$($_.ProcessId) $($_.CommandLine)\" }"],
                            capture_output=True, text=True, timeout=60).stdout.strip().splitlines()
    except Exception as e:
        ps = [f"(no se pudo listar: {e})"]
    log(f"REGLA 11 — procesos python vivos ({len(ps)}), este es pid {os.getpid()}")
    log("ETAPA 1/5 — identidad interna (subproceso, un proceso).")
    r1 = sub([sys.executable, os.path.join(AQUI, 'identidad_v15e.py'), '30000'], 'identidad')
    if r1['returncode'] != 0 or not any('IDENTIDAD (I1+I2+I3): 32/32' in l for l in r1['cola']):
        log("*** la identidad no es 32/32 (o no se pudo leer); se para. No se corre nada mas."); _log['f'].close(); sys.exit(1)
    V['identidad'] = '32/32'
    log("ETAPA 2/5 — V1: examen del criterio v3' con la perilla ENCENDIDA (subproceso, trae su Pool).")
    r2 = sub([sys.executable, os.path.join(AQUI, 'bateria_v15e.py'), '20', '--desde', '101', '--log'], 'V1 examen')
    V['V1'] = any('CUMPLE EL CRITERIO v3 con 20 semillas' in l for l in r2['cola'])
    log("ETAPA 3/5 — V2a: generalizacion con la memoria ENCENDIDA (subproceso, trae su Pool).")
    r3 = sub([sys.executable, os.path.join(AQUI, 'bateria_generaliza_v15e.py'),
              'organismo_v15e_on', '20', '--desde', '101', '--log'], 'V2a generalizacion')
    txt3 = "\n".join(r3['cola'])
    g1 = num(r"G1 valor en patrones nunca vistos: px0 ([0-9.]+)", txt3); g1az = num(r"G1 valor[^\n]*azar ([0-9.]+)", txt3)
    g2 = num(r"G2 conducta al primer encuentro: px0 ([0-9.]+)", txt3); g2az = num(r"G2 conducta[^\n]*azar ([0-9.]+)", txt3)
    kc = num(r"cobertura del primer encuentro: ([0-9]+)/", txt3)
    V['V2a_G1'] = g1; V['V2a_G2'] = g2; V['V2a_K'] = kc
    V['V2a'] = bool(g1 is not None and g1 >= 0.80 and g2 is not None and g2 >= 0.85 and kc is not None and kc >= 20
                    and g1az is not None and 0.35 <= g1az <= 0.65 and any('CONSERVA' in l and 'NO CONSERVA' not in l for l in r3['cola']))
    log(f"ETAPA 4/5 — V2b: mundo de regla {SEEDS[0]}-{SEEDS[-1]}, memoria ON y OFF pareadas, {len(REGLAS)} reglas, kwargs del tronco.")
    import multiprocessing as mp
    mp.set_start_method('spawn', force=True)
    tr = [(rg, s, mem) for rg in REGLAS for s in SEEDS for mem in MODOS]
    with mp.Pool(N_PARALELO) as pool:
        res = []
        for i, r in enumerate(pool.imap_unordered(tarea, tr, chunksize=1), 1):
            res.append(r)
            if i % 20 == 0 or i == len(tr): log(f"          {i}/{len(tr)}")
    G = lambda rg, mem: sorted([r for r in res if r['regla'] == rg and r['memoria'] == mem], key=lambda r: r['seed'])
    for rg in REGLAS:
        for mem in MODOS:
            g = G(rg, mem)
            ar = med([r['acc'] for r in g]); ae = med([r['acc_estricta'] for r in g])
            log(f"   {rg:6s} memoria={str(mem):5s}  registro {f3(ar[0])} [{f3(ar[1],2)},{f3(ar[2],2)}]  "
                f"ESTRICTA {f3(ae[0])}  ba {f3(med([r['ba'] for r in g])[0])}  "
                f"gana(0,1) {sum(1 for r in g if r['ganadora'] == [0, 1])}/{len(g)}  "
                f"cobertura {f3(med([r['cobertura'] for r in g])[0],1)}/4  "
                f"celdas {f3(med([r['celdas'] for r in g])[0],0)}  splits {f3(med([r['splits'] for r in g])[0],0)}  "
                f"muertes {f3(med([r['deaths'] for r in g])[0],0)}")
    log("ETAPA 5/5 — umbrales del preregistro (§5).")
    x = med([r['acc_estricta'] for r in G('xor01', 'suma')])[0]
    p_on = med([r['acc'] for r in G('px0', 'suma')])[0]; p_off = med([r['acc'] for r in G('px0', None)])[0]
    par_px = sum(1 for a, b in zip(G('px0', 'suma'), G('px0', None)) if a['acc'] >= b['acc'])
    az = med([r['acc'] for r in G('azar', 'suma')])[0]
    V['V2b_xor01_estricta'] = x; V['V2b_px0_on'] = p_on; V['V2b_px0_off'] = p_off; V['V2b_px0_pareado_on>=off'] = par_px; V['V2b_azar'] = az
    V['V2b'] = bool(x is not None and x >= 0.75 and p_on is not None and p_off is not None and p_on >= p_off - 1e-9
                    and az is not None and 0.35 <= az <= 0.65)
    V4 = {}
    for rg in ('xor01', 'px0'):
        for q in ('celdas', 'splits'):
            a = med([r[q] for r in G(rg, 'suma')])[0]; b = med([r[q] for r in G(rg, None)])[0]
            V4[f'{rg}_{q}'] = dict(on=a, off=b, delta=(None if not b else round((a - b) / b, 3)))
    V['V4'] = V4
    V['V4_dentro'] = all(v['delta'] is not None and abs(v['delta']) <= 0.10 for v in V4.values())
    V['V4_por_arriba'] = any(v['delta'] is not None and v['delta'] > 0.10 for v in V4.values())
    log(f"   V1  examen v3' 8/8 ON (lo que mata: E1 W_B≈-3 y E2 reversion)                 {'OK' if V['V1'] else 'NO'}")
    log(f"   V2a G1 {f3(g1)} >= .80 (azar {f3(g1az)}) · G2 {f3(g2)} >= .85 (azar {f3(g2az)}) · K {kc}/20   {'OK' if V['V2a'] else 'NO'}")
    log(f"   V2b xor01 ESTRICTA {f3(x)} >= .75 · px0 ON {f3(p_on)} >= OFF {f3(p_off)} (pareado ON>=OFF {par_px}/20) · azar {f3(az)} en [.35,.65]   {'OK' if V['V2b'] else 'NO'}")
    log(f"   V4  ±10 %: {V4}  dentro {'si' if V['V4_dentro'] else 'NO'}; por ARRIBA (+10 %, cuenta como coste) {'si' if V['V4_por_arriba'] else 'no'}"
        f"  (declarado: se esperaba incumplir por abajo en xor01)")
    entra = V['V1'] and V['V2a'] and V['V2b']
    log(f"VEREDICTO por la clausula §7: {'v15e CUMPLE V1, V2a y V2b -> candidato a tronco (decision del director; V4 se pesa aparte)' if entra else 'v15e NO ENTRA al tronco (cae V1, V2a o V2b). Sin modos intermedios.'}")
    meta = dict(fecha=time.strftime('%Y-%m-%dT%H:%M:%S'), semillas_V2b=SEEDS, semillas_V1_V2a=list(range(101, 121)), reglas=REGLAS,
                kw14=KW14, veredictos=V, etapas=[r1, r2, r3], procesos_python=ps,
                sha_preregistro=h16(pre) if os.path.exists(pre) else None, sha_script=h16(os.path.abspath(__file__)),
                sha_v15e=h16(os.path.join(AQUI, 'organismo_v15e.py')), sha_v15e_on=h16(os.path.join(AQUI, 'organismo_v15e_on.py')),
                sha_v15ge=h16(os.path.join(AQUI, 'organismo_v15ge.py')), sha_v15ge_on=h16(os.path.join(AQUI, 'organismo_v15ge_on.py')),
                sha_bateria_v15e=h16(os.path.join(AQUI, 'bateria_v15e.py')), sha_bateria_generaliza_v15e=h16(os.path.join(AQUI, 'bateria_generaliza_v15e.py')),
                sha_origen_v14=h16(os.path.join(RAIZ, 'organismo', 'organismo_v14.py')), sha_origen_v14g=h16(os.path.join(RAIZ, 'organismo', 'organismo_v14g.py')),
                python=platform.python_version(), numpy=np.__version__)
    dj = os.path.join(RAIZ, 'datos', nom + '.json')
    json.dump(dict(meta=meta, corridas=res), open(dj, 'w', encoding='utf-8'), ensure_ascii=False, default=str)
    log(f"datos -> {os.path.basename(dj)}  sha256_16 = {h16(dj)}")
    _log['f'].close()
