"""Bloque 6 (A-6): construir el rasgo conjuntivo YA NO es el cuello; lo es la SOBREDETERMINACION.
Ejecuta PREREGISTRO_xor_6.md. REGLA 10: log desde el arranque. REGLA 11: lista los python vivos antes del Pool.

Instrumento: `experimentos/creacion_A/organismo_v13q6.py` (perillas `ntr`, `seleccion` y `lab`; con las tres
apagadas es `organismo_v13q3` EXACTO). AVISO: los brazos `NTR*` CAMBIAN EL MUNDO (suben el tren, bajan el test);
el brazo que decide es `SIN_CTE`, que no lo toca.

--rapido: el gemelo `organismo_v13q5_rapido.py` (del compilador; identidad contra el interpretado 6/6, x56-105)
SI tiene `regla_lenta`, `constante`, `oraculo01`, `seleccion` y `lab`, pero **NO tiene `ntr`**: los brazos con `ntr`
van SIEMPRE interpretados y el runner lo dice por brazo. ETAPA 1b: identidad gemelo == interpretado en 3 casos.

ETAPA 1a identidad (obligatoria): `organismo_v13q6(ntr=None, seleccion=None, lab=False)` == `organismo_v13q3`.
ETAPA 1b identidad del gemelo: `organismo_v13q5_rapido` == `organismo_v13q5` en 3 casos.
ETAPA 2 las 360 corridas. ETAPA 3 tabla + EXPOSICIONES. ETAPA 4 criterios del preregistro.

Las EXPOSICIONES se calculan repitiendo el flujo `(patron, R)` que cada corrida graba con `lab=True` (la
actualizacion de la via lenta queda determinada por ese flujo). El replay esta verificado contra el organismo:
0 diferencias en 20/20 semillas (`banco_lab.py`, seccion A9 de PUENTE_creacion.md).

Uso:  python experimentos/creacion_A/corre_xor_6.py [--desde N] [--rapido]   (por defecto semillas 101-120)
      python experimentos/creacion_A/corre_xor_6.py --humo                     (UN proceso, sin Pool)
"""
import sys, os, json, time, hashlib, platform, subprocess, itertools
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
import numpy as np

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
sys.path[:0] = [AQUI, os.path.join(RAIZ, 'experimentos', 'nivel7_xor_lectura'), os.path.join(RAIZ, 'organismo')]
_desde = int(sys.argv[sys.argv.index('--desde') + 1]) if '--desde' in sys.argv else 101
SEEDS = list(range(_desde, _desde + 20))
HUMO = '--humo' in sys.argv
RAPIDO = '--rapido' in sys.argv   # solo para los brazos SIN `ntr`: el gemelo no tiene esa perilla

BASE = dict(T=100000, mundo='regla', puerta=3, regla_lenta='delta_signo', lam_lenta=0.0,
            eta_s=0.15, clip_s=10.0)                                   # las constantes que A-4 valido
WTA = dict(seleccion='wta', sel_theta=0.3, sel_rho=0.02, sel_cupo=1, sel_estad='cond')   # las meta-aprendidas
BRAZOS = {
    'REF':            dict(constante=True,  ntr=None,   **WTA),   # 8 rasgos vs 8 patrones: exactamente determinado
    'SIN_CTE':        dict(constante=False, ntr=None,   **WTA),   # L1: 7 vs 8, GRATIS y sin tocar el mundo
    'NTR11':          dict(constante=True,  ntr=(6, 5), **WTA),   # L2 dosis 1 (CAMBIA EL MUNDO)
    'NTR14':          dict(constante=True,  ntr=(8, 6), **WTA),   # L2 dosis 2 (CAMBIA EL MUNDO)
    'SIN_CTE_NTR11':  dict(constante=False, ntr=(6, 5), **WTA),   # las dos palancas
    'SIN_SEL':        dict(constante=True,  ntr=None),            # CONTROL: sin competencia
}
LECTURAS = ['cuadratica']
REGLAS = ['xor01', 'px0', 'azar']
IDX_PROD = {'cuadratica': 6, 'oraculo01': 2}        # donde vive P0*P1 en phi
SIN_CTE_OK = True   # phi sin constante: el replay lo respeta (phi_de(..., constante))
REJ = [10, 20, 40, 60, 100, 150, 200, 300, 400, 600]   # cortes para las exposiciones
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


def signo_acc(Wd, test, vr):
    """Acierto BALANCEADO por signo sobre los nunca vistos. Empate exacto = 0.5. La formula del registro."""
    f = [1.0 if Wd[k] > 0 else (0.5 if Wd[k] == 0 else 0.0) for k in test if vr[k] == 'comida']
    p = [1.0 if Wd[k] < 0 else (0.5 if Wd[k] == 0 else 0.0) for k in test if vr[k] == 'veneno']
    if not f or not p:
        return None
    return 0.5 * float(np.mean(f)) + 0.5 * float(np.mean(p))


# ------------------------------------------------------------------ replay (para las EXPOSICIONES)
def phi_de(P, lectura, constante=True):
    if lectura == 'lineal': b = P
    elif lectura == 'cuadratica': b = np.concatenate([P, [P[i] * P[j] for i, j in IJ]])
    elif lectura == 'oraculo01': b = np.array([P[0], P[1], P[0] * P[1]])
    elif lectura == 'oraculo01_ruido': b = np.array([P[0], P[1], P[2] * P[3]])
    else: raise ValueError(lectura)
    return np.concatenate([b, [1.0]]) if constante else b


def replay(X, y, eta, clip, sel=None, theta=0.6, rho=0.05, cupo=1, estad='cond', npx=6, ncj=15):
    """La MISMA regla de la via lenta de organismo_v13q5 (delta con signo, lam_lenta=0), fuera del mundo."""
    n = X.shape[1]; w = np.zeros(n); e = np.zeros(n)
    ab = np.ones(n, bool); cand = np.zeros(n, bool)
    if sel:
        cand[npx:npx + ncj] = True; ab = ~cand
    for i in range(len(y)):
        ph = X[i]; d = y[i] - float(w @ ph)
        if sel:
            act = ph > 0
            if estad == 'cond': e[act] = (1 - rho) * e[act] + rho * d
            else: e = (1 - rho) * e + rho * (d * ph)
            if int((ab & cand).sum()) < cupo:
                c = cand & ~ab
                if c.any():
                    j = int(np.argmax(np.where(c, np.abs(e), -1.0)))
                    if abs(e[j]) > theta: ab[j] = True
            ph = ph * ab
        w = np.clip(w + eta * d * ph, -clip, clip)
    return w


def exposiciones(ev, fase2_en, lectura, kw, pats, test, vr, cte=True):
    """acc_lenta usando solo los primeros n eventos pre-sonda, para cada n de REJ."""
    pre = [e for e in ev if e[0] < fase2_en]
    if not pre:
        return {n: None for n in REJ}, 0
    P = np.array([np.array([float(c) for c in e[1]]) for e in pre])
    y = np.array([e[2] for e in pre])
    X = np.array([phi_de(p, lectura, cte) for p in P])
    npx = 2 if lectura.startswith('oraculo') else 6
    ncj = 1 if lectura.startswith('oraculo') else 15
    out = {}
    for n in REJ:
        if n > len(y):
            out[n] = None; continue
        w = replay(X[:n], y[:n], kw['eta_s'], kw['clip_s'],
                   sel=kw.get('seleccion'), theta=kw.get('sel_theta', 0.6), rho=kw.get('sel_rho', 0.05),
                   cupo=kw.get('sel_cupo', 1), estad=kw.get('sel_estad', 'cond'), npx=npx, ncj=ncj)
        out[n] = signo_acc({k: float(phi_de(v, lectura, cte) @ w) for k, v in pats.items()}, test, vr)
    return out, len(pre)


# ------------------------------------------------------------------ tarea
def tarea(args):
    tipo = args[0]
    if tipo == 'I':          # 1a: la perilla nueva apagada == el original
        _, regla, lectura, seed = args
        import organismo_v13q3 as a_, organismo_v13q6 as b_
        kw = dict(T=60000, mundo='regla', regla=regla, lectura=lectura, eta_s=0.015, puerta=3)
        if lectura != 'lineal':
            kw.update(constante=True, regla_lenta='delta_signo', lam_lenta=0.0)
        a, b = a_.run(seed, **kw), b_.run(seed, ntr=None, seleccion=None, lab=False, **kw)
        dif = [k for k in a if N(a[k]) != N(b[k])]
        return dict(tipo='I', esc=f'{regla}/{lectura}', seed=seed, identico=not dif, difieren=dif,
                    claves_nuevas=[k for k in b if k not in a])
    if tipo == 'G':          # 1b: el gemelo compilado == el interpretado
        _, seed, caso = args
        import organismo_v13q5 as i_, organismo_v13q5_rapido as r_
        kw = dict(BASE); kw.pop('ntr', None)
        kw.update(mundo='regla', regla='xor01', lectura='cuadratica', constante=True, lab=True, T=30000)
        if caso == 1: kw.update(WTA)
        if caso == 2: kw.update(regla='px0', lectura='lineal', eta_s=0.015, clip_s=3.0, lab=False)
        a, b = i_.run(seed, **kw), r_.run(seed, **kw)
        dif = [k for k in a if N(a[k]) != N(b[k])]
        return dict(tipo='G', esc=f'gemelo caso{caso}', seed=seed, identico=not dif, difieren=dif)
    _, brazo, lectura, regla, seed = args
    kwb = dict(BRAZOS[brazo]); ntr = kwb.pop('ntr', None); cte = kwb.get('constante', True)
    usa_gemelo = RAPIDO and ntr is None
    if usa_gemelo:
        import organismo_v13q5_rapido as m
        import organismo_v13q6 as sr
    else:
        import organismo_v13q6 as m; sr = m
    kw = dict(BASE); kw.update(kwb); kw.update(regla=regla, lectura=lectura, lab=True)
    if not usa_gemelo:
        kw['ntr'] = ntr
    r = m.run(seed, **kw)
    pats, tren, test, vr = sr.split_regla(seed, regla, ntr)
    expo, npre = exposiciones(r['lenta_eventos'], r['fase2_en'], lectura, dict(BASE, **kwb), pats, test, vr, cte)
    ab = r.get('sel_abiertos') or []
    abre = [x for x in (r.get('sel_abre') or []) if int(x[1]) == IDX_PROD[lectura]]
    abre_t = int(abre[0][0]) if abre else None
    abre_antes = bool(abre_t is not None and abre_t < r['fase2_en'])   # abrir DESPUES de la sonda no sirve para acc_lenta
    cls = {}
    for e in r['lenta_eventos']:
        if e[0] < r['fase2_en']:
            cls[e[1][:2]] = cls.get(e[1][:2], 0) + 1
    Wsa = r['Ws_apriori'] or []
    return dict(tipo='T', brazo=brazo, lectura=lectura, regla=regla, seed=seed, gemelo=bool(usa_gemelo),
                n_tren=len(tren), n_test=len(test),
                acc=signo_acc(r['W_apriori'], test, vr), acc_lenta=signo_acc(r['W_lenta_apriori'], test, vr),
                abre_prod=bool(IDX_PROD[lectura] in ab), abiertos=[int(x) for x in ab],
                abre_t=abre_t, abre_antes=abre_antes, fase2_en=int(r['fase2_en']),
                Ws_prod=(float(Wsa[IDX_PROD[lectura]]) if len(Wsa) > IDX_PROD[lectura] else None),
                max_abs_Ws=(float(max(abs(x) for x in Wsa)) if Wsa else None),
                n_pre=npre, clases_pre=cls, clases_sin_morder=4 - len(cls),
                expo={str(k): v for k, v in expo.items()},
                splits=r['splits'], celdas=r['celdas'], deaths=r['deaths'])


# ------------------------------------------------------------------ informe y criterios
def tabla(res, seeds):
    log("ETAPA 3/4 — tabla. acc = valor total a priori en nunca vistos; acc_lenta = via lenta sola.")
    G = lambda b, lec, rg: [r for r in res if r['tipo'] == 'T' and r['brazo'] == b and r['lectura'] == lec and r['regla'] == rg]
    for lec in LECTURAS:
        for b in BRAZOS:
            for rg in REGLAS:
                g = G(b, lec, rg)
                if not g: continue
                al = med([r['acc_lenta'] for r in g])
                log(f"   {b:15s} {rg:6s} tren {g[0]['n_tren']:>2}/test {g[0]['n_test']:>2} "
                    f"{'gemelo' if g[0]['gemelo'] else 'interp'} acc {f3(med([r['acc'] for r in g])[0])}"
                    f"  acc_lenta {f3(al[0])} [{f3(al[1], 2)},{f3(al[2], 2)}]"
                    f"  abre P0*P1 {sum(r['abre_prod'] for r in g)}/{len(g)}"
                    f"  Ws(P0*P1) {f3(med([r['Ws_prod'] for r in g])[0], 2)}"
                    f"  max|Ws| {f3(med([r['max_abs_Ws'] for r in g])[0], 2)}"
                    f"  eventos {f3(med([r['n_pre'] for r in g])[0], 0)}"
                    f"  clases sin morder {sum(r['clases_sin_morder'] > 0 for r in g)}/{len(g)}")
    log("EXPOSICIONES — acc_lenta con los primeros n encuentros (mediana); n* = primer n con mediana >= 0.75.")
    expos = {}
    for lec in LECTURAS:
        log(f"   {lec}:  " + ' '.join(f'{n:>6}' for n in REJ) + '   n*(>=0.75) / n*(>=0.65)')
        for b in BRAZOS:
            g = G(b, lec, 'xor01')
            if not g: continue
            v = [med([r['expo'].get(str(n)) for r in g])[0] for n in REJ]
            n75 = next((n for n, x in zip(REJ, v) if x is not None and x >= 0.75), None)
            n65 = next((n for n, x in zip(REJ, v) if x is not None and x >= 0.65), None)
            expos[f'{lec}/{b}'] = dict(curva={str(n): x for n, x in zip(REJ, v)}, n75=n75, n65=n65)
            log(f"      {b:12s} " + ' '.join(f'{f3(x, 3):>6}' for x in v) + f"   {n75 or '>600'} / {n65 or '>600'}")
    return expos


def criterios(res, seeds, expos):
    A = lambda b, rg, s, k: next((r[k] for r in res if r['tipo'] == 'T' and r['brazo'] == b
                                  and r['regla'] == rg and r['seed'] == s), None)
    M = lambda b, rg, k: med([A(b, rg, s, k) for s in seeds])[0]
    par = lambda b1, b2, rg, k: sum(1 for s in seeds if A(b1, rg, s, k) is not None and A(b2, rg, s, k) is not None
                                    and A(b1, rg, s, k) > A(b2, rg, s, k))
    V = {}
    p1 = par('SIN_CTE', 'REF', 'xor01', 'acc_lenta'); m1 = M('SIN_CTE', 'xor01', 'acc_lenta')
    V['W1'] = bool(p1 >= 14 and m1 is not None and m1 >= 0.625); V['W1_pareado'] = p1; V['W1_mediana'] = m1
    m11 = M('NTR11', 'xor01', 'acc_lenta'); m14 = M('NTR14', 'xor01', 'acc_lenta')
    V['W2'] = bool(m11 is not None and m11 >= 0.75 and m14 is not None and m14 >= 0.80)
    V['W2_ntr11'] = m11; V['W2_ntr14'] = m14
    p3 = par('NTR11', 'SIN_CTE_NTR11', 'xor01', 'acc_lenta')
    V['W3'] = bool(p3 < 14); V['W3_ntr11_gana'] = p3
    V['W4'] = {}; w4ok = True
    for b in BRAZOS:
        if 'seleccion' not in BRAZOS[b]: continue
        n = sum(1 for s in seeds if A(b, 'xor01', s, 'abre_antes'))   # solo cuentan las aperturas ANTES de la sonda
        V['W4'][b] = n
        w4ok &= (n >= 15)
    V['W4_ok'] = bool(w4ok)
    malos = []
    for b in BRAZOS:
        px = M(b, 'px0', 'acc_lenta'); az = M(b, 'azar', 'acc_lenta')
        if px is None or px < 1.0 - 1e-9: malos.append(f'px0 {b}={f3(px)}')
        if az is None or not (0.35 <= az <= 0.65): malos.append(f'azar {b}={f3(az)}')
    ss = par('SIN_SEL', 'REF', 'xor01', 'acc_lenta')
    V['W5'] = bool(not malos and ss <= 10); V['W5_fallos'] = malos; V['W5_sin_sel_gana'] = ss
    V['clases_sin_morder'] = {b: sum(1 for s in seeds if (A(b, 'xor01', s, 'clases_sin_morder') or 0) > 0) for b in BRAZOS}
    V['EXPO'] = {k: dict(n75=v['n75'], n65=v['n65']) for k, v in expos.items()}
    V['SOBREDETERMINACION'] = bool(V['W1'] and V['W4_ok'] and V['W5'])
    log("ETAPA 4/4 — criterios del preregistro.")
    log(f"   W1 (decide, y no toca el mundo) SIN_CTE > REF en {p1}/20 >= 14 y mediana {f3(m1)} >= .625   {'OK' if V['W1'] else 'NO'}")
    log(f"   W2 NTR11 {f3(m11)} >= .75 y NTR14 {f3(m14)} >= .80 (CAMBIAN EL MUNDO)                       {'OK' if V['W2'] else 'NO'}")
    log(f"   W3 las dos palancas no se estorban: NTR11 > SIN_CTE_NTR11 en {p3}/20 (< 14)                {'OK' if V['W3'] else 'NO'}")
    log(f"   W4 abre P0*P1 ANTES de la sonda >= 15/20 en cada brazo con competencia: {V['W4']}                            {'OK' if V['W4_ok'] else 'NO'}")
    log(f"   W5 px0 = 1.000, azar en [.35,.65], y SIN_SEL no gana a REF ({ss}/20): "
        f"{'OK' if V['W5'] else 'NO — ' + '; '.join(malos)}")
    log(f"   clausula de muestreo — semillas con una clase XOR SIN MORDER, por brazo: {V['clases_sin_morder']}")
    log(f"VEREDICTO bloque 6: {'EL CUELLO ERA LA SOBREDETERMINACION (8 rasgos abiertos vs 8 patrones), no el mecanismo de seleccion' if V['SOBREDETERMINACION'] else 'NO: la sobredeterminacion no explica el techo (mirar W1/W4/W5)'}")
    log("RECORDATORIO: los brazos NTR* CAMBIAN EL MUNDO (sube el tren, baja el test): no son comparables numero a "
        "numero con los bloques 3-4, y por eso W1 (que no toca el mundo) es la que decide.")
    return V


def humo():
    """UN proceso, sin Pool (EQUIPO regla 3): identidad 1a + 1b + los 6 brazos en xor01, 1 semilla."""
    stamp = time.strftime('%Y%m%d_%H%M%S')
    _log['f'] = open(os.path.join(RAIZ, 'datos', f'xor_6_humo_{stamp}.log'), 'w', encoding='utf-8', newline='\n')
    log(f"HUMO bloque 6 (un proceso, sin Pool). identidad 1a + 1b + {len(BRAZOS)} brazos, xor01, semilla {_desde}, "
        f"T={BASE['T']}.  --rapido {'SI' if RAPIDO else 'no'} (solo brazos sin `ntr`)")
    log(f"sha organismo_v13q6 {h16(os.path.join(AQUI, 'organismo_v13q6.py'))}"
        f"  construye_v13q6 {h16(os.path.join(AQUI, 'construye_v13q6.py'))}"
        f"  organismo_v13q5 {h16(os.path.join(AQUI, 'organismo_v13q5.py'))}"
        f"  gemelo {h16(os.path.join(AQUI, 'organismo_v13q5_rapido.py'))}"
        f"  organismo_v13q3 {h16(os.path.join(RAIZ,'experimentos','nivel7_xor_lectura','organismo_v13q3.py'))}"
        f"  script {h16(os.path.abspath(__file__))}")
    ide = [tarea(('I', rg, lec, _desde)) for rg, lec in (('px0', 'lineal'), ('xor01', 'cuadratica'))]
    ide += [tarea(('G', _desde, c)) for c in (0, 1, 2)]
    for x in ide:
        log(f"   identidad {x['esc']:20s} s{x['seed']}: {'IDENTICO' if x['identico'] else 'DIFIERE ' + str(x['difieren'])}")
    if not all(x['identico'] for x in ide):
        log("*** IDENTIDAD FALLIDA: el instrumento no sirve."); _log['f'].close(); sys.exit(1)
    log(f"   identidad: {sum(x['identico'] for x in ide)}/{len(ide)} (1a original + 1b gemelo)")
    res = [tarea(('T', b, 'cuadratica', 'xor01', _desde)) for b in BRAZOS]
    for r in res:
        n75 = next((n for n in REJ if r['expo'].get(str(n)) is not None and r['expo'][str(n)] >= 0.75), None)
        log(f"   {r['brazo']:15s} s{r['seed']}: tren {r['n_tren']:>2}/test {r['n_test']:>2} "
            f"{'gemelo' if r['gemelo'] else 'interp'}  acc_lenta {f3(r['acc_lenta'])}  acc {f3(r['acc'])}"
            f"  abre P0*P1 {'SI' if r['abre_prod'] else 'no'}{' (TRAS la sonda)' if r['abre_prod'] and not r['abre_antes'] else ''}"
            f"  Ws(P0*P1) {f3(r['Ws_prod'], 2)}"
            f"  eventos {r['n_pre']}  clases sin morder {r['clases_sin_morder']}  n*(>=.75) {n75 or '>600'}")
    log("   (referencia del humo de 3 semillas: REF 0.500, SIN_CTE 0.625, NTR11 0.833, NTR14 0.500;"
        " nada se ajusta con esto.)")
    dj = os.path.join(RAIZ, 'datos', f'xor_6_humo_{stamp}.json')
    json.dump(dict(meta=dict(fecha=time.strftime('%Y-%m-%dT%H:%M:%S'), base=BASE, brazos=BRAZOS, wta=WTA,
                             semilla=_desde, rapido=RAPIDO,
                             sha_instrumento=h16(os.path.join(AQUI, 'organismo_v13q6.py')),
                             sha_gemelo=h16(os.path.join(AQUI, 'organismo_v13q5_rapido.py')),
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
    _log['f'] = open(os.path.join(RAIZ, 'datos', f'xor_6_s{SEEDS[0]}-{SEEDS[-1]}_{stamp}.log'), 'w', encoding='utf-8', newline='\n')
    pre = os.path.join(AQUI, 'PREREGISTRO_xor_6.md')
    log(f"ARRANQUE bloque 6 (A-6: sobredeterminacion). brazos {list(BRAZOS)}, lecturas {LECTURAS}, "
        f"reglas {REGLAS}, semillas {SEEDS[0]}-{SEEDS[-1]}. Pool({N_PARALELO}).")
    log(f"BASE {BASE}")
    for b, kw in BRAZOS.items():
        log(f"   brazo {b:12s} {kw}")
    log(f"sha preregistro {h16(pre) if os.path.exists(pre) else '(falta)'}  script {h16(os.path.abspath(__file__))}"
        f"  organismo_v13q6 {h16(os.path.join(AQUI, 'organismo_v13q6.py'))}"
        f"  construye_v13q6 {h16(os.path.join(AQUI, 'construye_v13q6.py'))}"
        f"  gemelo {h16(os.path.join(AQUI, 'organismo_v13q5_rapido.py'))}"
        f"  organismo_v13q3 {h16(os.path.join(RAIZ,'experimentos','nivel7_xor_lectura','organismo_v13q3.py'))}")
    try:
        ps = subprocess.run(['powershell', '-NoProfile', '-Command',
                             "Get-CimInstance Win32_Process | Where-Object { $_.Name -like 'python*' } | ForEach-Object { \"$($_.ProcessId) $($_.CommandLine)\" }"],
                            capture_output=True, text=True, timeout=60).stdout.strip().splitlines()
    except Exception as e:
        ps = [f"(no se pudo listar: {e})"]
    log(f"REGLA 11 — procesos python vivos ({len(ps)}), este es pid {os.getpid()}")
    with mp.Pool(N_PARALELO) as pool:
        ctrl = [('I', rg, lec, s) for rg, lec in (('px0', 'lineal'), ('xor01', 'cuadratica')) for s in SEEDS[:3]]
        ctrl += [('G', s, c) for c in (0, 1, 2) for s in SEEDS[:1]]
        log(f"ETAPA 1/4 — identidad 1a (v13q6 perillas apagadas == v13q3) y 1b (gemelo == interpretado) "
            f"({len(ctrl)} corridas)...")
        rc = pool.map(tarea, ctrl, chunksize=1)
        log(f"   identicos: {sum(x['identico'] for x in rc)}/{len(rc)}   claves nuevas: {rc[0]['claves_nuevas']}")
        for x in rc:
            if not x['identico']:
                log(f"      DIFIERE {x['esc']} s{x['seed']}: {x['difieren']}")
        if not all(x['identico'] for x in rc):
            log("*** IDENTIDAD FALLIDA: se para."); sys.exit(1)
        tr = [('T', b, lec, rg, s) for b in BRAZOS for lec in LECTURAS for rg in REGLAS for s in SEEDS]
        log(f"ETAPA 2/4 — {len(tr)} corridas de T={BASE['T']}...")
        res = []
        for i, r in enumerate(pool.imap_unordered(tarea, tr, chunksize=1), 1):
            res.append(r)
            if i % 40 == 0 or i == len(tr):
                log(f"          {i}/{len(tr)}")
    expos = tabla(res, SEEDS)
    V = criterios(res, SEEDS, expos)
    meta = dict(fecha=time.strftime('%Y-%m-%dT%H:%M:%S'), semillas=SEEDS, base=BASE, brazos=BRAZOS,
                lecturas=LECTURAS, reglas=REGLAS, veredictos=V, exposiciones=expos, identidades=rc, procesos_python=ps,
                sha_preregistro=h16(pre) if os.path.exists(pre) else None, sha_script=h16(os.path.abspath(__file__)),
                sha_instrumento=h16(os.path.join(AQUI, 'organismo_v13q6.py')),
                sha_constructor=h16(os.path.join(AQUI, 'construye_v13q6.py')),
                sha_gemelo=h16(os.path.join(AQUI, 'organismo_v13q5_rapido.py')), rapido=RAPIDO,
                sha_origen=h16(os.path.join(RAIZ, 'experimentos', 'nivel7_xor_lectura', 'organismo_v13q3.py')),
                python=platform.python_version(), numpy=np.__version__)
    dj = os.path.join(RAIZ, 'datos', f'xor_6_s{SEEDS[0]}-{SEEDS[-1]}_{stamp}.json')
    json.dump(dict(meta=meta, corridas=res), open(dj, 'w', encoding='utf-8'), ensure_ascii=False, default=str)
    log(f"datos -> {os.path.basename(dj)}  sha256_16 = {h16(dj)}")
    _log['f'].close()
