"""Bloque 3/3 de la linea XOR (A-7): ¿el mecanismo de la sala construye el rasgo con 8 ejemplos?
Ejecuta PREREGISTRO_xor_7.md. REGLA 10: log desde el arranque. REGLA 11: lista los python vivos antes del Pool.

Brazos: M3 (grupo 3, memoria de un golpe por combinacion) con desempate por INDICE y por AZAR (control de rigging),
M4 (grupo 4, tabla por grupos), REF (v13q6 + seleccion WTA: el mejor local anterior, 0.625) y SIN_SEL.

Instrumentos: `organismo_g3A.py` (creacion_A, por anclas desde `experimentos/enjambre/grupo3/organismo_g3.py`
`91eb167023cb37b7`; perillas `mem_apriori` y `mem_desempate`, apagadas == g3, identidad 10/10),
`experimentos/enjambre/grupo4/organismo_g4.py` (del grupo 4, sin tocar) y `organismo_v13q6.py` (creacion_A).

--rapido: el gemelo `organismo_v13q5_rapido` NO tiene `memoria` ni `tabla_g` ni `ntr`; sirve solo para REF y SIN_SEL.
M3 y M4 van SIEMPRE interpretados (~5 s/corrida) y el runner lo dice por brazo.

DOS PUNTUACIONES SIEMPRE: la del registro (valor 0 exacto = 0.5, empate) y la ESTRICTA (valor 0 = fallo), porque
M3 y M4 ABSTIENEN explicitamente en las combinaciones nunca vistas y parte del numero es ese medio punto.

Uso:  python experimentos/creacion_A/corre_xor_7.py [--desde N] [--rapido]   (por defecto semillas 121-140)
      python experimentos/creacion_A/corre_xor_7.py --humo                   (UN proceso, sin Pool)
"""
import sys, os, json, time, hashlib, platform, subprocess
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
import numpy as np

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
sys.path[:0] = [AQUI, os.path.join(RAIZ, 'experimentos', 'nivel7_xor_lectura'),
                os.path.join(RAIZ, 'experimentos', 'enjambre', 'grupo3'),
                os.path.join(RAIZ, 'experimentos', 'enjambre', 'grupo4'), os.path.join(RAIZ, 'organismo')]
_desde = int(sys.argv[sys.argv.index('--desde') + 1]) if '--desde' in sys.argv else 121
SEEDS = list(range(_desde, _desde + 20))
HUMO = '--humo' in sys.argv
RAPIDO = '--rapido' in sys.argv

BASE = dict(T=100000, mundo='regla', lectura='cuadratica', constante=True, regla_lenta='delta_signo',
            lam_lenta=0.0, eta_s=0.15, clip_s=10.0, puerta=3, lab=True)
WTA = dict(seleccion='wta', sel_theta=0.3, sel_rho=0.02, sel_cupo=1, sel_estad='cond')
G4 = dict(g=2, crit='mse', lectura_g='dura', rho=0.02, eta=0.05, clip=3.0, alpha=0.3)   # FIJADAS ANTES (informe §5)
BRAZOS = {
    'M3':       dict(mod='g3A', memoria='combi', mem_apriori=True, mem_desempate='indice'),
    'M3_AZAR':  dict(mod='g3A', memoria='combi', mem_apriori=True, mem_desempate='azar'),   # control de rigging
    'M3_NTR14': dict(mod='g3A', memoria='combi', mem_apriori=True, mem_desempate='azar', ntr=(8, 6)),  # control de prior
    'M4':       dict(mod='g4', tabla_g=G4),
    'REF':      dict(mod='q6', **WTA),
    'SIN_SEL':  dict(mod='q6'),
}
REGLAS = ['xor01', 'px0', 'azar']
IDX_PROD = 6
REJ = [5, 7, 10, 20, 40, 60, 100, 150, 200, 300, 600]
IJ = [(i, j) for i in range(6) for j in range(i + 1, 6)]
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


def f3(x, n=3):
    return '  n/a' if x is None else f"{x:.{n}f}"


def med(xs):
    xs = [x for x in xs if x is not None]
    if not xs:
        return None, None, None
    return float(np.median(xs)), float(min(xs)), float(max(xs))


def acc_dos(Wd, test, vr):
    """(registro, estricta). Registro: valor 0 exacto = 0.5. Estricta: valor 0 = FALLO (la abstencion no puntua)."""
    out = []
    for medio in (0.5, 0.0):
        f = [1.0 if Wd[k] > 0 else (medio if Wd[k] == 0 else 0.0) for k in test if vr[k] == 'comida']
        p = [1.0 if Wd[k] < 0 else (medio if Wd[k] == 0 else 0.0) for k in test if vr[k] == 'veneno']
        out.append(None if (not f or not p) else 0.5 * float(np.mean(f)) + 0.5 * float(np.mean(p)))
    return out[0], out[1]


# ------------------------------------------------------------------ replay (EXPOSICIONES, solo M3)
def replay_M3(ev, modo='combi', rho=0.02, alfa=0.3, hasta=None, rng=None):
    MM = np.zeros((15, 4)); MN = np.zeros((15, 4)); ME = np.full(15, 1e9)
    for e in (ev if hasta is None else ev[:hasta]):
        P = [int(ch) for ch in e[1]]; R = e[2]
        for ci, (i, j) in enumerate(IJ):
            d = P[i] * 2 + P[j]
            p = float(MM[ci, d]) if MN[ci, d] > 0 else 0.0
            er = R - p; prim = MN[ci].sum() == 0
            ME[ci] = (er * er) if prim else (1 - rho) * ME[ci] + rho * (er * er)
            if MN[ci, d] == 0: MM[ci, d] = R
            elif modo == 'combi': MM[ci, d] += alfa * (R - MM[ci, d])
            MN[ci, d] += 1
    mn = float(ME.min()); emp = [k for k in range(15) if ME[k] <= mn + 1e-12]
    g = int(emp[int(rng.integers(len(emp)))]) if rng is not None else int(np.argmin(ME))
    return g, MM, MN, len(emp)


def expo_M3(ev, pats, test, vr, modo, rng):
    out = {}
    for n in REJ:
        if n > len(ev): out[n] = None; continue
        g, MM, MN, _ = replay_M3(ev, modo, hasta=n, rng=rng)
        i, j = IJ[g]
        W = {}
        for k, v in pats.items():
            d = int(v[i]) * 2 + int(v[j]); W[k] = float(MM[g, d]) if MN[g, d] > 0 else 0.0
        out[n] = acc_dos(W, test, vr)[0]
    return out


# ------------------------------------------------------------------ tarea
def tarea(args):
    tipo = args[0]
    if tipo == 'I':
        _, caso, seed = args
        if caso == 'g3':
            import organismo_g3 as a_, organismo_g3A as b_
            kw = dict(BASE); kw.update(regla='xor01', memoria='combi')
            a, b = a_.run(seed, **kw), b_.run(seed, mem_apriori=False, mem_desempate='indice', **kw)
            nuev = {'mem_apriori', 'mem_desempate'}
        elif caso == 'q6':
            import organismo_v13q3 as a_, organismo_v13q6 as b_
            kw = dict(T=60000, mundo='regla', regla='px0', lectura='lineal', eta_s=0.015, puerta=3)
            a, b = a_.run(seed, **kw), b_.run(seed, ntr=None, seleccion=None, lab=False, **kw)
            nuev = {'ntr', 'lab', 'lenta_eventos', 'fase2_en', 'seleccion', 'sel_estad', 'sel_theta', 'sel_rho',
                    'sel_cupo', 'sel_abre', 'sel_abiertos', 'sel_e', 'sel_n'}
        else:
            import organismo_v13q5 as a_, organismo_g4 as b_
            kw = dict(BASE); kw.update(regla='xor01')
            a, b = a_.run(seed, **kw), b_.run(seed, tabla_g=None, **kw)
            nuev = {k for k in b_.run(seed, T=1000, tabla_g=None, mundo='regla', regla='px0')} - set(a)
        dif = [k for k in a if k in b and N(a[k]) != N(b[k])]
        falt = [k for k in a if k not in b]
        return dict(tipo='I', esc=caso, seed=seed, identico=not dif and not falt, difieren=dif + falt)
    _, brazo, regla, seed = args
    kwb = dict(BRAZOS[brazo]); mod = kwb.pop('mod'); ntr = kwb.pop('ntr', None)
    kw = dict(BASE); kw.update(kwb); kw['regla'] = regla
    usa_gemelo = RAPIDO and mod == 'q6' and ntr is None
    if mod == 'g3A':
        import organismo_g3A as m
    elif mod == 'g4':
        import organismo_g4 as m
    elif usa_gemelo:
        import organismo_v13q5_rapido as m
    else:
        import organismo_v13q6 as m
    import organismo_v13q6 as sr
    if mod == 'q6' and not usa_gemelo:
        kw['ntr'] = ntr
    r = m.run(seed, **kw)
    pats, tren, test, vr = sr.split_regla(seed, regla, ntr)
    a_reg, a_est = acc_dos(r['W_lenta_apriori'], test, vr)
    t_reg, _ = acc_dos(r['W_apriori'], test, vr)
    pre = [e for e in r['lenta_eventos'] if e[0] < r['fase2_en']]
    cls = {}
    for e in pre: cls[e[1][:2]] = cls.get(e[1][:2], 0) + 1
    ma = r.get('mem_apriori')
    ab = r.get('sel_abiertos') or []
    rng = np.random.default_rng(seed + 99000)
    ex = expo_M3(pre, pats, test, vr, kwb.get('memoria', 'combi'), rng) if mod == 'g3A' else {}
    return dict(tipo='T', brazo=brazo, regla=regla, seed=seed, gemelo=bool(usa_gemelo), n_tren=len(tren),
                n_test=len(test), acc_lenta=a_reg, acc_lenta_estricta=a_est, acc=t_reg,
                gana01=bool((ma and tuple(ma['ganadora']) == (0, 1)) or (not ma and IDX_PROD in ab)),
                n_empate=(ma['n_empate'] if ma else None),
                cobertura=(ma['cobertura_ganadora'] if ma else None),
                ganadora=(ma['ganadora'] if ma else None), abiertos=[int(x) for x in ab],
                n_pre=len(pre), clases_pre=cls, clases_sin_morder=4 - len(cls),
                expo={str(k): v for k, v in ex.items()},
                deaths=r['deaths'], celdas=r['celdas'], splits=r['splits'])


# ------------------------------------------------------------------ informe
def informe(res, seeds):
    G = lambda b, rg: [r for r in res if r['tipo'] == 'T' and r['brazo'] == b and r['regla'] == rg]
    log("ETAPA 3/4 — tabla. DOS puntuaciones: registro (empate 0.5) y ESTRICTA (abstencion = fallo).")
    for b in BRAZOS:
        for rg in REGLAS:
            g = G(b, rg)
            if not g: continue
            ar = med([r['acc_lenta'] for r in g]); ae = med([r['acc_lenta_estricta'] for r in g])
            log(f"   {b:9s} {rg:6s} tren {g[0]['n_tren']:>2}/test {g[0]['n_test']:>2} "
                f"{'gemelo' if g[0]['gemelo'] else 'interp'}  registro {f3(ar[0])} [{f3(ar[1],2)},{f3(ar[2],2)}]"
                f"  ESTRICTA {f3(ae[0])}  gana(0,1) {sum(r['gana01'] for r in g)}/{len(g)}"
                f"  empates {f3(med([r['n_empate'] for r in g])[0], 1)}"
                f"  cobertura {f3(med([r['cobertura'] for r in g])[0], 1)}/4"
                f"  clases sin morder {sum(r['clases_sin_morder'] > 0 for r in g)}/{len(g)}"
                f"  muertes {f3(med([r['deaths'] for r in g])[0], 0)}")
    log("EXPOSICIONES (solo M3; replay de su regla sobre el flujo real). n* = primer n con mediana >= 0.75.")
    expos = {}
    for b in ('M3', 'M3_AZAR', 'M3_NTR14'):
        g = G(b, 'xor01')
        if not g or not g[0]['expo']: continue
        v = [med([r['expo'].get(str(n)) for r in g])[0] for n in REJ]
        n75 = next((n for n, x in zip(REJ, v) if x is not None and x >= 0.75), None)
        expos[b] = dict(curva={str(n): x for n, x in zip(REJ, v)}, n75=n75)
        log(f"   {b:9s} " + ' '.join(f'{f3(x,3):>6}' for x in v) + f"   n* = {n75 or '>600'}")
    return expos


def criterios(res, seeds, expos):
    A = lambda b, rg, s, k: next((r[k] for r in res if r['tipo'] == 'T' and r['brazo'] == b and r['regla'] == rg
                                  and r['seed'] == s), None)
    M = lambda b, rg, k: med([A(b, rg, s, k) for s in seeds])[0]
    V = {}
    m3 = M('M3_AZAR', 'xor01', 'acc_lenta'); e3 = M('M3_AZAR', 'xor01', 'acc_lenta_estricta')
    p3 = sum(1 for s in seeds if A('M3_AZAR', 'xor01', s, 'acc_lenta') is not None
             and A('REF', 'xor01', s, 'acc_lenta') is not None
             and A('M3_AZAR', 'xor01', s, 'acc_lenta') > A('REF', 'xor01', s, 'acc_lenta'))
    V['X1'] = bool(m3 is not None and m3 >= 0.75 and p3 >= 15); V['X1_mediana'] = m3; V['X1_pareado'] = p3
    V['X2'] = bool(e3 is not None and e3 >= 0.60); V['X2_estricta'] = e3
    n01 = sum(1 for s in seeds if A('M3_AZAR', 'xor01', s, 'gana01'))
    V['X3'] = bool(n01 >= 15); V['X3_gana01'] = n01
    mi = M('M3', 'xor01', 'acc_lenta')
    V['X4_rigging'] = dict(indice=mi, azar=m3, delta=(None if (mi is None or m3 is None) else round(mi - m3, 3)))
    V['X4'] = bool(mi is not None and m3 is not None and abs(mi - m3) <= 0.05)
    m14 = M('M3_NTR14', 'xor01', 'acc_lenta')
    V['X5'] = bool(m14 is not None and m14 >= 0.90); V['X5_ntr14'] = m14
    malos = []
    for b in BRAZOS:
        px = M(b, 'px0', 'acc_lenta'); az = M(b, 'azar', 'acc_lenta')
        if px is None or px < 1.0 - 1e-9: malos.append(f'px0 {b}={f3(px)}')
        if az is None or not (0.35 <= az <= 0.65): malos.append(f'azar {b}={f3(az)}')
    V['X6'] = not malos; V['X6_fallos'] = malos
    V['EXPO'] = {k: v['n75'] for k, v in expos.items()}
    V['clases_sin_morder'] = {b: sum(1 for s in seeds if (A(b, 'xor01', s, 'clases_sin_morder') or 0) > 0) for b in BRAZOS}
    V['CONSTRUYE_EL_RASGO'] = bool(V['X1'] and V['X3'] and V['X4'] and V['X6'])
    log("ETAPA 4/4 — criterios del preregistro.")
    log(f"   X1 M3 (desempate AZAR) registro {f3(m3)} >= .75 y > REF en {p3}/20 >= 15        {'OK' if V['X1'] else 'NO'}")
    log(f"   X2 M3 ESTRICTA {f3(e3)} >= .60                                                  {'OK' if V['X2'] else 'NO'}")
    log(f"   X3 gana (0,1) EN LA SONDA en {n01}/20 >= 15                                     {'OK' if V['X3'] else 'NO'}")
    log(f"   X4 RIGGING: indice {f3(mi)} vs azar {f3(m3)} (|dif| <= .05)                     {'OK' if V['X4'] else 'NO — el indice decide'}")
    log(f"   X5 PRIOR: con 14 patrones {f3(m14)} >= .90                                      {'OK' if V['X5'] else 'NO'}")
    log(f"   X6 px0 = 1.000 y azar en [.35,.65]: {'OK' if V['X6'] else 'NO — ' + '; '.join(malos)}")
    log(f"   clausula de muestreo (semillas con una clase sin morder): {V['clases_sin_morder']}")
    log(f"VEREDICTO bloque 3/3: {'M3 CONSTRUYE EL RASGO CON 8 EJEMPLOS -> se declara PRIOR ESTRUCTURAL (candidatos = pares de pixeles), no aprendizaje de la estructura' if V['CONSTRUYE_EL_RASGO'] else 'NO: M3 no cumple (mirar X1/X3/X4/X6)'}")
    log("RECORDATORIO: cruzar con 8 ejemplos = PRIOR declarado. El control que lo separa de una fuga es `azar` "
        "en [0.35, 0.65] (X6); el que lo separa de un artefacto es el desempate AL AZAR (X4).")
    return V


def humo():
    stamp = time.strftime('%Y%m%d_%H%M%S')
    _log['f'] = open(os.path.join(RAIZ, 'datos', f'xor_7_humo_{stamp}.log'), 'w', encoding='utf-8', newline='\n')
    log(f"HUMO bloque 3/3 (un proceso, sin Pool). identidad + {len(BRAZOS)} brazos, xor01, semilla {_desde}.")
    log(f"sha organismo_g3A {h16(os.path.join(AQUI,'organismo_g3A.py'))}"
        f"  construye_g3A {h16(os.path.join(AQUI,'construye_g3A.py'))}"
        f"  organismo_g3 {h16(os.path.join(RAIZ,'experimentos','enjambre','grupo3','organismo_g3.py'))}"
        f"  organismo_g4 {h16(os.path.join(RAIZ,'experimentos','enjambre','grupo4','organismo_g4.py'))}"
        f"  organismo_v13q6 {h16(os.path.join(AQUI,'organismo_v13q6.py'))}  script {h16(os.path.abspath(__file__))}")
    ide = [tarea(('I', c, _desde)) for c in ('g3', 'q6', 'g4')]
    for x in ide:
        log(f"   identidad {x['esc']:4s} s{x['seed']}: {'IDENTICO' if x['identico'] else 'DIFIERE ' + str(x['difieren'])}")
    if not all(x['identico'] for x in ide):
        log("*** IDENTIDAD FALLIDA."); _log['f'].close(); sys.exit(1)
    res = [tarea(('T', b, 'xor01', _desde)) for b in BRAZOS]
    for r in res:
        n75 = next((n for n in REJ if r['expo'].get(str(n)) is not None and r['expo'][str(n)] >= 0.75), None)
        log(f"   {r['brazo']:9s} s{r['seed']}: tren {r['n_tren']:>2}/test {r['n_test']:>2} "
            f"registro {f3(r['acc_lenta'])}  ESTRICTA {f3(r['acc_lenta_estricta'])}  ganadora {r['ganadora'] or r['abiertos']}"
            f"  empates {r['n_empate']}  cobertura {r['cobertura']}/4  eventos {r['n_pre']}"
            f"  clases sin morder {r['clases_sin_morder']}  n* {n75 or '-'}")
    dj = os.path.join(RAIZ, 'datos', f'xor_7_humo_{stamp}.json')
    json.dump(dict(meta=dict(fecha=time.strftime('%Y-%m-%dT%H:%M:%S'), base=BASE, brazos=BRAZOS, semilla=_desde,
                             sha_g3A=h16(os.path.join(AQUI, 'organismo_g3A.py')),
                             sha_script=h16(os.path.abspath(__file__)),
                             python=platform.python_version(), numpy=np.__version__),
                   identidades=ide, corridas=res), open(dj, 'w', encoding='utf-8'), ensure_ascii=False, default=str)
    log(f"datos -> {os.path.basename(dj)}  sha256_16 = {h16(dj)}")
    _log['f'].close()


if __name__ == '__main__':
    if HUMO:
        humo(); sys.exit(0)
    import multiprocessing as mp
    mp.set_start_method('spawn', force=True)
    stamp = time.strftime('%Y%m%d_%H%M%S')
    _log['f'] = open(os.path.join(RAIZ, 'datos', f'xor_7_s{SEEDS[0]}-{SEEDS[-1]}_{stamp}.log'), 'w',
                     encoding='utf-8', newline='\n')
    pre = os.path.join(AQUI, 'PREREGISTRO_xor_7.md')
    log(f"ARRANQUE bloque 3/3 (A-7). brazos {list(BRAZOS)}, reglas {REGLAS}, semillas {SEEDS[0]}-{SEEDS[-1]}. "
        f"Pool({N_PARALELO}).  --rapido {'SI (solo REF/SIN_SEL)' if RAPIDO else 'no'}")
    log(f"BASE {BASE}")
    for b, kw in BRAZOS.items(): log(f"   brazo {b:9s} {kw}")
    log(f"sha preregistro {h16(pre) if os.path.exists(pre) else '(falta)'}  script {h16(os.path.abspath(__file__))}"
        f"  organismo_g3A {h16(os.path.join(AQUI,'organismo_g3A.py'))}"
        f"  organismo_g3 {h16(os.path.join(RAIZ,'experimentos','enjambre','grupo3','organismo_g3.py'))}"
        f"  organismo_g4 {h16(os.path.join(RAIZ,'experimentos','enjambre','grupo4','organismo_g4.py'))}"
        f"  organismo_v13q6 {h16(os.path.join(AQUI,'organismo_v13q6.py'))}")
    try:
        ps = subprocess.run(['powershell', '-NoProfile', '-Command',
                             "Get-CimInstance Win32_Process | Where-Object { $_.Name -like 'python*' } | ForEach-Object { \"$($_.ProcessId) $($_.CommandLine)\" }"],
                            capture_output=True, text=True, timeout=60).stdout.strip().splitlines()
    except Exception as e:
        ps = [f"(no se pudo listar: {e})"]
    log(f"REGLA 11 — procesos python vivos ({len(ps)}), este es pid {os.getpid()}")
    with mp.Pool(N_PARALELO) as pool:
        ctrl = [('I', c, s) for c in ('g3', 'q6', 'g4') for s in SEEDS[:3]]
        log(f"ETAPA 1/4 — identidad (perillas apagadas == el original de cada grupo), {len(ctrl)} corridas...")
        rc = pool.map(tarea, ctrl, chunksize=1)
        log(f"   identicos: {sum(x['identico'] for x in rc)}/{len(rc)}")
        for x in rc:
            if not x['identico']: log(f"      DIFIERE {x['esc']} s{x['seed']}: {x['difieren']}")
        if not all(x['identico'] for x in rc):
            log("*** IDENTIDAD FALLIDA: se para."); sys.exit(1)
        tr = [('T', b, rg, s) for b in BRAZOS for rg in REGLAS for s in SEEDS]
        log(f"ETAPA 2/4 — {len(tr)} corridas de T={BASE['T']}...")
        res = []
        for i, r in enumerate(pool.imap_unordered(tarea, tr, chunksize=1), 1):
            res.append(r)
            if i % 40 == 0 or i == len(tr): log(f"          {i}/{len(tr)}")
    expos = informe(res, SEEDS)
    V = criterios(res, SEEDS, expos)
    meta = dict(fecha=time.strftime('%Y-%m-%dT%H:%M:%S'), semillas=SEEDS, base=BASE, brazos=BRAZOS, reglas=REGLAS,
                veredictos=V, exposiciones=expos, identidades=rc, procesos_python=ps,
                sha_preregistro=h16(pre) if os.path.exists(pre) else None, sha_script=h16(os.path.abspath(__file__)),
                sha_g3A=h16(os.path.join(AQUI, 'organismo_g3A.py')),
                sha_g3=h16(os.path.join(RAIZ, 'experimentos', 'enjambre', 'grupo3', 'organismo_g3.py')),
                sha_g4=h16(os.path.join(RAIZ, 'experimentos', 'enjambre', 'grupo4', 'organismo_g4.py')),
                rapido=RAPIDO, python=platform.python_version(), numpy=np.__version__)
    dj = os.path.join(RAIZ, 'datos', f'xor_7_s{SEEDS[0]}-{SEEDS[-1]}_{stamp}.json')
    json.dump(dict(meta=meta, corridas=res), open(dj, 'w', encoding='utf-8'), ensure_ascii=False, default=str)
    log(f"datos -> {os.path.basename(dj)}  sha256_16 = {h16(dj)}")
    _log['f'].close()
