"""corre_n9c.py — SUBIDA DEL NIVEL 9, TANDA 3: ¿persiste un linaje del ORGANISMO PROPIO en un mundo con capacidad de carga?
(PREREGISTRO_n9c.md; letra, predicciones y criterio alli).

MISION: llegar a la AGI por este camino.

Mundo: pista v2 de generaciones que conviven (experimentos/generaciones/pista2.py + motor_convive.py, solapadas=1, quimiostato
'fija', r_rep 0.03, tope 300), SIN CAMBIOS; la entrada a pista2.run es campo a campo la de corre_convive.tarea (regla 14,
arnes identidad_n9c.py). Organismo: FABRICA (mitad cerebro del brazo REL de organismo_f9c) en cuatro variantes construidas por
anclas (construye_n9c.py v2): NADA (== FABRICA) · PRED (la boca predice su propio estado tras morder con el efecto SENTIDO
por letra, sin herencia) · CAND (PRED + el padre vivo pasa en el parto su memoria de efectos) · CRUZ (CAND con dE y dAg
intercambiados en lo heredado: control de contenido).
Brazos: monocultivos de 9 fundadores (L = 360, 36 objetos), T = 100000.
Medidas SOLO desde la fisica (ERR-96): resumen_linaje del juez v2 (corre_convive.py, importado con sha fijado) + las de esta
pregunta. La telemetria del carro (d['carro']['n9c']) va aparte y no puntua.

ERR-115: el parser es una LISTA BLANCA y ABORTA ante cualquier bandera desconocida, abreviada, con '=', repetida o -h/--help.
Formas validas (exactas):
  python experimentos/subida_n9c/corre_n9c.py --humo [--desde 14192] [--n 1] [--T 20000] [--brazos NADA,CAND,...]   (UN proceso)
  python experimentos/subida_n9c/corre_n9c.py --serie --desde 14101 --n 20 --pool 6     (SOLO el coordinador)
  python experimentos/subida_n9c/corre_n9c.py --serie --desde 14121 --n 20 --pool 6     (replica; SOLO el coordinador)
  python experimentos/subida_n9c/corre_n9c.py --veredicto <serie.json>,<replica.json>   (no corre nada; veredicto conjunto)
Semillas: practica 14191-14199 (solo --humo) · serie 14101-14120 · replica 14121-14140. El corredor se niega a usar otras.
ERR-54: el crudo se escribe ANTES de resumir. Vocabulario: "linaje", "cuerpo"; prohibido "poblacion" sin la medida, "evoluciona".
"""
import gzip, hashlib, importlib.util, json, math, os, platform, statistics as st, sys, time

sys.stdout.reconfigure(encoding='utf-8', errors='replace')
AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
GEN = os.path.join(RAIZ, 'experimentos', 'generaciones')
if GEN not in sys.path: sys.path.insert(0, GEN)
if AQUI not in sys.path: sys.path.insert(0, AQUI)
import pista2 as P2            # noqa: E402
import motor_convive as MC     # noqa: E402
import corre_convive as JV     # noqa: E402  juez v2: resumen_linaje (se importa; sha fijado)

SHAS = {os.path.join(GEN, 'pista2.py'): '4d2bee16e7961261', os.path.join(GEN, 'motor_convive.py'): 'd10cb9021f5d0f41',
        os.path.join(GEN, 'corre_convive.py'): 'e6dadfdad9c379cd',
        os.path.join(RAIZ, 'experimentos', 'carrera_escuderias', 'carros', 'FABRICA.py'): '2ebee3e99ea5a33a',
        os.path.join(AQUI, 'carros', 'N9C_NADA.py'): 'd4853da9c6ed9a82',
        os.path.join(AQUI, 'carros', 'N9C_PRED.py'): '4a1ea0844b31c837',
        os.path.join(AQUI, 'carros', 'N9C_CAND.py'): 'd5b2b9390e782a70',
        os.path.join(AQUI, 'carros', 'N9C_CRUZ.py'): '822cea5ec7d95b94'}
BRAZOS = ('NADA', 'PRED', 'CAND', 'CRUZ')
PRACTICA = range(14191, 14200); SERIE = range(14101, 14121); REPLICA = range(14121, 14141)
# 14191 = humo de la practica v1 (descartada, practica_v1/); el humo v2 usa 14192
T_DEF = 100000
DATOS = os.path.join(AQUI, 'datos'); HUMO = os.path.join(DATOS, 'humo')
# PREREGISTRO_n9c.md sec. 6 (fijado antes de la serie)
ANCLA = (0.090, 0.155)      # calibra_ancla.py (bootstrap de dos etapas sobre n10 NADA 12301-12320; ERR-116)
ANCLA_PERSISTE_MAX = 2      # NADA persiste (letra estricta) en <= 2/20 (FABRICA: 0/20 en dos series de v2)
NEED = 15                   # umbral pareado y de persistencia: >= 15/20 (fraccion 0.75 si n != 20)
PARES = (('CAND', 'NADA'), ('CAND', 'PRED'), ('CAND', 'CRUZ'), ('PRED', 'NADA'), ('CRUZ', 'PRED'))
CLAVES_PAR = ('R0_nacidos', 'vida_nacidos', 'tam_carro', 'lin_max')


def h16(p): return hashlib.sha256(open(p, 'rb').read()).hexdigest()[:16]


def verifica_shas():
    mal = {os.path.basename(p): (h16(p), s) for p, s in SHAS.items() if h16(p) != s}
    if mal: raise SystemExit(f"corre_n9c: sha cambiado {mal} (reconstruir y volver a correr identidad_n9c.py) -> ABORTA")


# ------------------------------------------------------------------------------------------------ parser (ERR-115)
class BanderaMala(SystemExit):
    pass


def parsea(argv):
    """Lista blanca estricta. Devuelve dict; ante cualquier cosa fuera de la lista lanza BanderaMala (SystemExit)."""
    CON_VALOR = {'--desde': int, '--n': int, '--T': int, '--pool': int, '--brazos': str, '--veredicto': str}
    SIN_VALOR = {'--humo', '--serie'}
    a = dict(humo=False, serie=False, desde=None, n=None, T=None, pool=None, brazos=None, veredicto=None); vistos = set(); i = 0
    while i < len(argv):
        tk = argv[i]
        if tk in vistos: raise BanderaMala(f"corre_n9c: bandera repetida {tk!r} -> ABORTA (ERR-115)")
        if tk in SIN_VALOR:
            a[tk[2:]] = True; vistos.add(tk); i += 1; continue
        if tk in CON_VALOR:
            if i + 1 >= len(argv) or argv[i + 1].startswith('-'): raise BanderaMala(f"corre_n9c: {tk} sin valor -> ABORTA (ERR-115)")
            try: a[tk[2:]] = CON_VALOR[tk](argv[i + 1])
            except ValueError: raise BanderaMala(f"corre_n9c: valor invalido para {tk}: {argv[i + 1]!r} -> ABORTA (ERR-115)")
            vistos.add(tk); i += 2; continue
        raise BanderaMala(f"corre_n9c: bandera desconocida {tk!r} (validas: {sorted(SIN_VALOR | set(CON_VALOR))}; "
                          f"sin abreviaturas, sin '=', sin --help) -> ABORTA sin correr nada (ERR-115)")
    modos = [m for m in ('humo', 'serie', 'veredicto') if a[m]]
    if len(modos) != 1: raise BanderaMala(f"corre_n9c: hace falta exactamente uno de --humo / --serie / --veredicto (hay {modos}) -> ABORTA")
    if a['brazos'] is not None:
        bz = [b.strip() for b in a['brazos'].split(',') if b.strip()]
        if not bz or any(b not in BRAZOS for b in bz) or len(set(bz)) != len(bz):
            raise BanderaMala(f"corre_n9c: --brazos {a['brazos']!r} invalido (validos {list(BRAZOS)}) -> ABORTA")
        a['brazos'] = bz
    if a['veredicto'] is not None:
        if any(a[k] is not None for k in ('desde', 'n', 'T', 'pool', 'brazos')):
            raise BanderaMala("corre_n9c: --veredicto no admite otras banderas -> ABORTA")
        fs = a['veredicto'].split(',')
        if len(fs) != 2: raise BanderaMala("corre_n9c: --veredicto <serie.json>,<replica.json> -> ABORTA")
        return a
    if a['humo']:
        if a['pool'] not in (None, 0): raise BanderaMala("corre_n9c: --humo es de UN proceso (sin --pool) -> ABORTA")
        a['desde'] = a['desde'] or 14192; a['n'] = a['n'] or 1; a['T'] = a['T'] or 20000; a['brazos'] = a['brazos'] or list(BRAZOS)
        if not all(s in PRACTICA for s in range(a['desde'], a['desde'] + a['n'])):
            raise BanderaMala("corre_n9c: --humo solo con semillas de practica 14191-14199 -> ABORTA")
        if a['n'] * len(a['brazos']) > 6 or a['n'] * len(a['brazos']) * a['T'] > 200000:
            raise BanderaMala("corre_n9c: el humo pasa de 6 corridas o de 200 000 pasos -> ABORTA")
        return a
    # --serie
    if a['desde'] is None or a['n'] is None or a['pool'] is None:
        raise BanderaMala("corre_n9c: --serie exige --desde, --n y --pool -> ABORTA")
    if a['T'] is not None and a['T'] != T_DEF: raise BanderaMala(f"corre_n9c: la serie es con T = {T_DEF} -> ABORTA")
    a['T'] = T_DEF; a['brazos'] = a['brazos'] or list(BRAZOS)
    sem = list(range(a['desde'], a['desde'] + a['n']))
    if not (sem == list(SERIE) or sem == list(REPLICA)):
        raise BanderaMala(f"corre_n9c: --serie solo con 14101-14120 (serie) o 14121-14140 (replica), n = 20 -> ABORTA")
    if not 1 <= a['pool'] <= 7: raise BanderaMala("corre_n9c: --pool entre 1 y 7 -> ABORTA")
    return a


# ------------------------------------------------------------------------------------------------ una corrida
def carga(et):
    p = os.path.join(AQUI, 'carros', f'N9C_{et}.py')
    spec = importlib.util.spec_from_file_location(f'carro_N9C_{et}', p)
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m


def kw_pista(T):
    """ENTRADA a pista2.run (regla 14): la MISMA de corre_convive.tarea con rep='fija', tope=MC.TOPE_DEF, rrep=MC.R_REP."""
    return dict(T=T, diag=0, solapadas=1, reposicion='fija', tope_cuerpos=MC.TOPE_DEF, r_rep=MC.R_REP)


def med(xs):
    xs = [x for x in xs if x is not None]
    return round(float(st.median(xs)), 4) if xs else None


def media(xs):
    xs = [x for x in xs if x is not None]
    return round(sum(xs) / len(xs), 4) if xs else None


def tarea(args):
    seed, brazo, T = args
    t0 = time.time()
    m = carga(brazo)
    r = P2.run(seed, [(f'N9C_{brazo}', m)] * 9, **kw_pista(T))
    ps = r['pista']; mu = ps['muestra']; i2 = (T // 2) // mu; tc = T // 2; i0 = JV.T_CORTE // mu
    L = [JV.resumen_linaje(d, T, mu) for d in r['linajes']]
    serie = [sum(d['tam'][k] for d in r['linajes']) for k in range(len(r['linajes'][0]['tam']))]
    ind = [x for d in r['linajes'] for x in d['individuos']]   # [k, gen, padre, t_nace, t_muere, hijos, fundador, causa, vol]
    nac = [x for x in ind if not x[6]]; fun = [x for x in ind if x[6]]
    coh = [x for x in nac if x[3] <= tc]
    mn = [x for x in nac if x[4] >= 0]; mf = [x for x in fun if x[4] >= 0]
    cau = {c: sum(1 for x in mn if x[7] == ic) for ic, c in enumerate(MC.CAUSAS)}
    # nicho (solo fisica): mordidas de lo malo (B, D) y de lo bueno (A, C) por 1000 pasos; mundo
    mB = sum(sum(d['mord']['B']) + sum(d['mord']['D']) for d in r['linajes'])
    mG = sum(sum(d['mord']['A']) + sum(d['mord']['C']) for d in r['linajes'])
    tam_post = [d['tam'][i0:-1] if len(d['tam']) > i0 + 1 else d['tam'] for d in r['linajes']]
    e = dict(
        persiste_carro=any(l['sin_extincion'] for l in L),                 # letra de generaciones sec. 9 (informativa aqui)
        persiste_estricto=any(l['persiste'] for l in L),                   # DECIDE: >= 1 linaje sin fundadores tras 10000 Y >= 5 nac.
        linajes_persisten=sum(l['persiste'] for l in L),
        lin_max=max(media(tp) or 0 for tp in tam_post),                   # tamano medio (t >= 10000) del linaje mas grande
        tam_carro=media(serie[i2:-1] if len(serie) > i2 + 1 else serie), tam_final=serie[-1],
        nac=len(nac), fundadores=len(fun), gen_max=max(l['gen_max'] for l in L),
        R0_nacidos=media([x[5] for x in coh]), n_coh_nacidos=len(coh),
        cens_nacidos=(round(sum(1 for x in coh if x[4] < 0) / len(coh), 4) if coh else None),
        R0_fund=media([x[5] for x in fun if x[3] <= tc]),
        vida_nacidos=med([x[4] - x[3] for x in mn]), vida_fund=med([x[4] - x[3] for x in mf]),
        frac_mala_nacidos=(round((cau['veneno'] + cau['sal']) / len(mn), 4) if mn else None), causas_nacidos=cau,
        mord_malo_k=round(1000 * mB / T, 3), mord_bueno_k=round(1000 * mG / T, 3),
        perdidas=ps['llegadas_perdidas'], llegadas=ps['llegadas'], nobj_medio=ps['nobj_medio'],
        buenos_mundo=round(ps['comp_mundo']['A'] + ps['comp_mundo']['C'], 3), malos_mundo=round(ps['comp_mundo']['B'] + ps['comp_mundo']['D'], 3),
        bloqueados=ps['bloqueados'], max_vivos=ps['max_vivos'])
    tele = [d.get('carro', {}).get('n9c') for d in r['linajes']]
    crudo = [dict(individuos=d['individuos'], tam=d['tam'], t_fund=d['t_fund'], mord=d['mord']) for d in r['linajes']]
    return dict(seed=seed, brazo=brazo, T=T, seg=round(time.time() - t0, 1), estr=e, linajes=L, crudo=crudo, tele=tele,
                pista={k: v for k, v in ps.items() if k not in ('pizarra_final',)})


# ------------------------------------------------------------------------------------------------ agregado y letra
def signo(g, p):
    n = g + p
    if n == 0: return 1.0
    k = min(g, p)
    return round(min(1.0, 2 * sum(math.comb(n, i) for i in range(k + 1)) / 2 ** n), 5)


def pareado(R, a, b, clave):
    xs = []
    for s in sorted({c['seed'] for c in R}):
        ca = [c for c in R if c['seed'] == s and c['brazo'] == a]; cb = [c for c in R if c['seed'] == s and c['brazo'] == b]
        if not ca or not cb: continue
        va, vb = ca[0]['estr'][clave], cb[0]['estr'][clave]
        if va is None or vb is None: continue
        xs.append(va - vb)
    g = sum(1 for d in xs if d > 0); p = sum(1 for d in xs if d < 0); e = len(xs) - g - p
    return dict(par=f"{a}-{b}", clave=clave, n=len(xs), gana=g, pierde=p, empata=e, dif_med=med(xs), p_signo=signo(g, p))


def agrega(R):
    A = {}
    for b in BRAZOS:
        cs = [c['estr'] for c in R if c['brazo'] == b]
        if not cs: continue
        A[b] = {k: med([c[k] for c in cs]) for k in ('tam_carro', 'lin_max', 'nac', 'fundadores', 'linajes_persisten', 'R0_nacidos',
                                                    'R0_fund', 'vida_nacidos', 'vida_fund', 'frac_mala_nacidos', 'gen_max',
                                                    'mord_malo_k', 'mord_bueno_k', 'perdidas', 'nobj_medio', 'buenos_mundo', 'malos_mundo')}
        A[b]['semillas'] = len(cs)
        A[b]['persiste_estricto'] = sum(bool(c['persiste_estricto']) for c in cs)
        A[b]['persiste_carro'] = sum(bool(c['persiste_carro']) for c in cs)
        A[b]['bloqueados'] = sum(c['bloqueados'] for c in cs)
    P = [pareado(R, a, b, k) for a, b in PARES for k in CLAVES_PAR]
    return A, P


def veredicto(A, P, n_sem):
    """PREREGISTRO_n9c.md sec. 6 (por la letra), UNA serie."""
    need = NEED if n_sem == 20 else math.ceil(0.75 * n_sem)
    g = lambda par, k: next((x for x in P if x['par'] == par and x['clave'] == k), None)
    K = 'R0_nacidos'; out = {}
    nada = A.get('NADA') or {}; cand = A.get('CAND') or {}; pred = A.get('PRED') or {}; cruz = A.get('CRUZ') or {}
    kA = f'V-ANCLA (mediana R0_nacidos NADA en [{ANCLA[0]:.3f}, {ANCLA[1]:.3f}] y NADA persiste en <= {ANCLA_PERSISTE_MAX}/20)'
    kB = 'V-TOPE (0 partos bloqueados por el tope de seguridad en CAND)'
    k1 = f'G1 PERSISTE (CAND: >= 1 linaje sin fundadores tras t=10000 y >= 5 nacimientos, en >= {need}/{n_sem} semillas)'
    k2 = f'G2 HERENCIA (CAND > PRED en R0_nacidos, >= {need}/{n_sem})'
    k3 = f'G3 CONTENIDO (CAND > CRUZ en R0_nacidos, >= {need}/{n_sem})'
    out[kA] = bool(nada.get(K) is not None and ANCLA[0] <= nada[K] <= ANCLA[1] and nada.get('persiste_estricto', 99) <= ANCLA_PERSISTE_MAX)
    out[kB] = bool(cand and cand.get('bloqueados', 1) == 0)
    out[k1] = bool(cand and cand.get('persiste_estricto', 0) >= need)
    x = g('CAND-PRED', K); out[k2] = bool(x and x['gana'] >= need)
    x = g('CAND-CRUZ', K); out[k3] = bool(x and x['gana'] >= need)
    out['C-PRED (control que puede ganar: la boca que predice SIN herencia persiste en >= 15/20)'] = bool(pred and pred.get('persiste_estricto', 0) >= need)
    out['C-CRUZ (control que puede ganar: CRUZ persiste en >= 15/20)'] = bool(cruz and cruz.get('persiste_estricto', 0) >= need)
    if not out[kA]: v = 'NO SE LEE (ancla fuera: el instrumento no reproduce el piso calibrado de FABRICA en v2)'
    elif not out[kB]: v = 'NO SE LEE (el tope de seguridad bloqueo partos de CAND: la densidad no la regulo el mundo)'
    elif out[k1] and out[k2] and out[k3]:
        v = 'FUNCIONA (un linaje del organismo propio persiste con flujo fijo de comida; hace falta que el hijo reciba lo que el linaje sintio, y por su contenido)'
    elif out[k1]:
        v = 'HAY ALGO MODESTO: PERSISTE SIN ATRIBUCION (el linaje del organismo propio persiste, pero algun control no pierde por la letra)'
    elif out[k2] and out[k3]:
        v = 'HAY ALGO MODESTO: SUBE SIN PERSISTIR (lo que el linaje sintio, heredado, sube el R0 de los nacidos por su contenido, sin sostener el linaje)'
    else: v = 'NO (el organismo propio no sostiene un linaje con flujo fijo de comida)'
    out['VEREDICTO'] = v
    return out


def veredicto_conjunto(fs):
    rs = [json.load(open(f, encoding='utf-8')) for f in fs]
    sems = [tuple(r['meta']['semillas']) for r in rs]
    if sorted(sems) != sorted([tuple(SERIE), tuple(REPLICA)]):
        raise SystemExit(f"corre_n9c: --veredicto exige una serie 14101-14120 y una replica 14121-14140 (hay {[(s[0], s[-1]) for s in sems]}) -> ABORTA")
    vs = [r['veredicto']['VEREDICTO'] for r in rs]
    cab = [v.split(' (')[0].split(':')[0] for v in vs]
    if cab[0] == cab[1] and cab[0] in ('FUNCIONA', 'HAY ALGO MODESTO', 'NO'):
        c = vs[0] if vs[0] == vs[1] else f"{cab[0]} (serie: {vs[0]} · replica: {vs[1]})"
    elif 'NO SE LEE' in cab: c = 'NO SE LEE (alguna de las dos no se lee)'
    else:
        orden = {'NO': 0, 'HAY ALGO MODESTO': 1, 'FUNCIONA': 2}
        c = f"{min(cab, key=lambda z: orden.get(z, -1))} (serie y replica no coinciden: {vs[0]} · {vs[1]}; vale la menor)"
    return vs, c


def main(argv):
    a = parsea(argv)
    if a['veredicto'] is not None:
        vs, c = veredicto_conjunto(a['veredicto'].split(','))
        for v in vs: print(f"  serie: {v}")
        print(f"VEREDICTO CONJUNTO (serie + replica, PREREGISTRO_n9c.md sec. 6): {c}")
        return 0
    verifica_shas()
    brazos = a['brazos']; semillas = list(range(a['desde'], a['desde'] + a['n'])); T = a['T']
    if a['humo']: sal = HUMO; et = f"n9c_humo_{'_'.join(brazos)}_s{semillas[0]}_T{T}"
    else: sal = DATOS; et = f"n9c_serie_s{semillas[0]}-{semillas[-1]}_T{T}"
    os.makedirs(sal, exist_ok=True)
    sello = time.strftime('%Y%m%d_%H%M%S'); base = os.path.join(sal, f"{et}_{sello}")
    flog = open(base + '.log', 'w', encoding='utf-8')

    def log(s=''):
        print(s, flush=True); flog.write(s + '\n'); flog.flush()
    log(f"corre_n9c · {et} · {sello} · python {platform.python_version()} · corre_n9c.py {h16(os.path.abspath(__file__))}")
    log("shas: " + ' '.join(f"{os.path.basename(p)}={s}" for p, s in SHAS.items()))
    tareas = [(s, b, T) for b in brazos for s in semillas]
    t0 = time.time(); R = []

    def linea(r):
        v = r['estr']
        return (f"  {r['brazo']:5s} s{r['seed']} {r['seg']:7.1f} s · persiste {int(v['persiste_estricto'])} (lin {v['linajes_persisten']}, "
                f"max {v['lin_max']}) · tam {v['tam_carro']} · nac {v['nac']} · R0nac {v['R0_nacidos']} · vida nac/fund "
                f"{v['vida_nacidos']}/{v['vida_fund']} · mala {v['frac_mala_nacidos']} · malo/bueno k {v['mord_malo_k']}/{v['mord_bueno_k']} · "
                f"perd {v['perdidas']} · mundo buenos/malos {v['buenos_mundo']}/{v['malos_mundo']} · gen {v['gen_max']}")
    if a['serie'] and a['pool'] > 1:
        from multiprocessing import Pool
        with Pool(a['pool']) as pool:
            for r in pool.imap_unordered(tarea, tareas): R.append(r); log(linea(r))
    else:
        for tk in tareas: r = tarea(tk); R.append(r); log(linea(r))
    with gzip.open(base + '_crudo.json.gz', 'wt', encoding='utf-8') as f: json.dump(R, f)   # ERR-54: crudo ANTES de resumir
    A, P = agrega(R)
    log(f"\nAGREGADO (medianas por semilla) · {len(semillas)} semilla(s) · {time.time() - t0:.0f} s de pared")
    for b, v in A.items(): log(f"  {b:5s} {v}")
    log("PAREADOS (por semilla):")
    for x in P: log(f"  {x}")
    if a['serie']: V = veredicto(A, P, len(semillas))
    else: V = {'VEREDICTO': 'HUMO: sin veredicto (semilla de practica, T corto; persistencia con T <= 10000 no se lee)'}
    meta = dict(etiqueta=et, sello=sello, semillas=semillas, T=T, brazos=brazos, shas={os.path.basename(p): s for p, s in SHAS.items()},
                corre_n9c=h16(os.path.abspath(__file__)), seg_pared=round(time.time() - t0, 1), seg_cpu=round(sum(r['seg'] for r in R), 1),
                ancla=ANCLA, need=NEED)
    res = dict(meta=meta, agregado=A, pareados=P, veredicto=V,
               por_semilla=[{k: r[k] for k in ('seed', 'brazo', 'T', 'seg', 'estr', 'tele')} for r in R])
    json.dump(res, open(base + '.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    log(f"\nescrito: {base}.json ({h16(base + '.json')}) · crudo {base}_crudo.json.gz")
    log("VEREDICTO por la letra (PREREGISTRO_n9c.md sec. 6):")
    for k, v in V.items(): log(f"  {k}: {v}")
    flog.close()
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
