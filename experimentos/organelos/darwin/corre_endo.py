"""corre_endo.py — RUNNER de ENDOSIMBIOSIS, escalon 1 (equipo organelos, Opus B, 24-sep-2026).

MISION: llegar a la AGI por este camino.

Preregistro: experimentos/organelos/darwin/PREREGISTRO_endosimbiosis.md (la letra esta AQUI, en veredicto(), y alli).
Motor: motor_endo.py (motor_eco3 + ganchos a simbiontes.py; arnes identidad_endosimbiosis.py N/N) + carros/FABRICA_SIMB.
Mundo: w30 (esc 30, 30 fundadores FABRICA_SIMB, L 1200, quimiostato de ECO), tope de cuerpos 3000. T 120 000, corte 60 000
(vivero antes, nadie repone nada despues). El bicho evoluciona como VIDA de ECO en los 5 brazos (corre_eco.eco_cfg('VIDA', ...):
banco 200, 8 sombras, p_mut 0.05, sigma 0.15) y SIN checkpoints (el estado de los simbiontes no va en el pickle): una corrida
cortada se repite entera (--reanuda salta las que ya escribieron su JSON).
Brazos del simbionte: VIDA_S, INERTE, BARAJADO, SIN_TRAGAR, AZAR_S (ver simbiontes.py).
nube-9: cada trabajo ATRAPA cualquier excepcion y SystemExit (el Pool no se cuelga) y escribe su JSON con 'error'; la guardia de ERR-60
del motor, con simb, no lanza: se registra (err60, t_trunc) y la corrida termina en ese paso.
Uso (ERR-115: banderas desconocidas o abreviadas abortan; SOLO el coordinador lanza --serie y --prueba_pool):
  python experimentos/organelos/darwin/corre_endo.py --humo                                # un proceso, semilla 22993, T 80 000
  python experimentos/organelos/darwin/corre_endo.py --prueba_pool --pool 2                # 22991-22992, T 6000 (coordinador)
  python experimentos/organelos/darwin/corre_endo.py --serie --ventana serie --pool 3      # 22001-22020 (coordinador)
  python experimentos/organelos/darwin/corre_endo.py --serie --ventana replica --pool 3    # 22021-22040 (coordinador)
  python experimentos/organelos/darwin/corre_endo.py --serie --ventana serie --pool 3 --reanuda
  python experimentos/organelos/darwin/corre_endo.py --lee <carpeta>
"""
import argparse, glob, hashlib, json, os, sys, time, traceback
import numpy as np

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(AQUI)))
for _d in (os.path.join(RAIZ, 'experimentos', 'generaciones'), os.path.join(RAIZ, 'experimentos', 'juaco_eco'), AQUI):
    if _d not in sys.path: sys.path.insert(0, _d)
try: sys.stdout.reconfigure(encoding='utf-8', errors='replace')
except Exception: pass
import corre_eco as CR          # eco_cfg (brazo VIDA del bicho); NO se usa su motor
import motor_endo as MD
import simbiontes as SIM

CARRO = 'FABRICA_SIMB'
MUNDO = dict(esc=30, n0=30, tope=3000, muestra=1000)
V = dict(T=120000, t_corte=60000, cola=20000)
BRAZOS = SIM.BRAZOS             # ('VIDA_S', 'INERTE', 'BARAJADO', 'SIN_TRAGAR', 'AZAR_S')
VENTANAS = {'serie': 22001, 'replica': 22021}
N = 20
UMBRAL = 15                     # >= 15/20: P = 0.021 bajo la nula p = 0.5
MIN_GRUPO = 5                   # P2: minimo de cuerpos por grupo (con / sin simbionte al nacer)
T_TRANS = 10000                 # P3: los partos antes de t = 10 000 no cuentan (los libres nacen con g al azar y se adaptan en ~2000-5000 pasos)
PRUEBA = dict(desde=22991, n=2, T=6000, t_corte=3000)
HUMO = dict(semilla=22993, T=80000, t_corte=50000)   # humo 1 (22990, T 40000) se corrio con la ecologia v1; declarado
DATOS = os.path.join(AQUI, 'datos')


class BanderaMala(SystemExit):
    pass


def medidas(r, T, tc, cola=V['cola']):
    """Lo que la letra lee de UNA corrida (todo desde d['simb'] y d['eco']; sin mirar el carro)."""
    E = r['eco']; P = r['pista']; S = r['simb']
    T_ef = S['t_trunc'] if S['t_trunc'] is not None else (E['t_ext'] if E['t_ext'] is not None else T)
    post = [x for x in S['serie'] if x[0] >= tc]
    prev = [x[2] / x[1] for x in post if x[1] > 0]
    Il = [x[4] for x in post if x[4] is not None]
    mu_ = MUNDO['muestra']
    Imap = {x[0]: x[4] for x in S['serie'] if x[4] is not None}   # I medio de los libres en cada muestra
    # P3: cada transmision EN UN PARTO (vivero incluido; los fundadores del vivero NO cuentan) contra los libres de la MISMA muestra
    parD = [(d[0], d[1] - Imap[(d[0] // mu_) * mu_]) for d in S['don']
            if d[2] == 1 and d[1] is not None and d[0] >= T_TRANS and (d[0] // mu_) * mu_ in Imap]   # sin el transitorio inicial de los libres
    don = [d[1] for d in S['don'] if d[1] is not None and d[2] == 1 and d[0] >= tc]
    coh = [f for f in S['ind'] if tc <= f[2] <= T_ef - cola]
    con = [f[4] for f in coh if f[5]]; sin = [f[4] for f in coh if not f[5]]
    D = (round(float(np.mean([x for _, x in parD])), 6) if parD else None)
    Dp = [x for t_, x in parD if t_ >= tc]
    D_post = (round(float(np.mean(Dp)), 6) if Dp else None)
    dec = S['decisiones']
    tasa = lambda q, k: (round(dec[q][k][1] / dec[q][k][0], 4) if dec[q][k][0] else None)
    gin = np.array([d[3:] for d in S['dentro_final']], float) if S['dentro_final'] else None
    gli = np.array(S['libres_final'], float) if S['libres_final'] else None
    mu = MUNDO['muestra']; tt = P['tam_total']
    area = int(sum(v for i, v in enumerate(tt[:-1]) if i * mu >= tc))   # cuerpos vivos sumados en las muestras t >= t_corte (cuerpos-paso / muestra)
    return dict(
        area_post=area, delta_r0=None,
        persiste=int(E['t_ext'] is None and len(E['vivos_final']) > 0), vivos_T=len(E['vivos_final']), t_ext=E['t_ext'],
        bloqueados=P['bloqueados'], max_vivos=P['max_vivos'], n_nac=E['n_nac'], n_refund=E['n_refund'], T_ef=T_ef,
        err60=S['err60'], t_trunc=S['t_trunc'], bloq_libres=S['eventos']['bloq_libres'], libres_extintos_t=S['eventos']['libres_extintos_t'],
        prev_post=(round(float(np.mean(prev)), 6) if prev else None), n_muestras_post=len(prev),
        prev_T=(round(len(S['dentro_final']) / len(E['vivos_final']), 4) if E['vivos_final'] else None),
        r0_con=(round(float(np.mean(con)), 4) if con else None), n_con=len(con),
        r0_sin=(round(float(np.mean(sin)), 4) if sin else None), n_sin=len(sin),
        I_don=(round(float(np.mean(don)), 6) if don else None), n_don=len(don), I_libres_post=(round(float(np.mean(Il)), 6) if Il else None), D=D,
        n_D=len(parD), D_post=D_post, n_D_post=len(Dp),
        I_dentro_T=(round(float(np.mean(S['I_dentro_final'])), 6) if S['I_dentro_final'] else None),
        I_libres_T=(round(float(np.mean(S['I_libres_final'])), 6) if S['I_libres_final'] else None),
        g_dentro_T=(None if gin is None else [round(float(x), 4) for x in gin.mean(0)]),
        g_libres_T=(None if gli is None else [round(float(x), 4) for x in gli.mean(0)]),
        dist_T=(None if gin is None or gli is None else round(float(np.linalg.norm(gin.mean(0) - gli.mean(0))), 4)),
        muerde={q: {k: tasa(q, k) for k in SIM.LETRAS} for q in ('con', 'sin')},
        eventos=S['eventos'])


def trabajo(args):
    """UNA corrida (semilla, brazo). Escribe su JSON. nube-9: NUNCA deja escapar una excepcion ni un SystemExit (el Pool no se cuelga)."""
    seed, brazo, T, tc, carpeta, reanuda = args
    fin = os.path.join(carpeta, f"{brazo}_s{seed}.json")
    if reanuda and os.path.exists(fin):
        x = json.load(open(fin, encoding='utf-8'))
        if x.get('error') is None: return x
    t0 = time.time()
    try:
        r = MD.run_solapadas(seed, [CARRO] * MUNDO['n0'], T=T, diag=0, mundo_n=MUNDO['esc'], tope_cuerpos=MUNDO['tope'],
                             muestra=MUNDO['muestra'], eco=CR.eco_cfg('VIDA', tc), simb=dict(brazo=brazo))
        res = dict(seed=seed, brazo=brazo, T=T, t_corte=tc, seg=round(time.time() - t0, 1), error=None, **medidas(r, T, tc))
        if res['n_con'] >= MIN_GRUPO and res['n_sin'] >= MIN_GRUPO: res['delta_r0'] = round(res['r0_con'] - res['r0_sin'], 4)
        res['serie_simb'] = r['simb']['serie']; res['cfg_simb'] = r['simb']['cfg']
        res['tam_total'] = r['pista']['tam_total']; res['gen_t'] = r['eco']['gen_t']
        # crudos para recalcular la letra sin volver a correr (auditoria): transmisiones, cohortes tras el corte, genomas finales
        res['don'] = r['simb']['don']; res['ind'] = r['simb']['ind']; res['ind_trunc'] = r['simb']['ind_trunc']
        res['dentro_final'] = r['simb']['dentro_final']; res['libres_final'] = r['simb']['libres_final']; res['decisiones'] = r['simb']['decisiones']
    except BaseException as e:   # nube-9: incluye SystemExit; KeyboardInterrupt se relanza
        if isinstance(e, KeyboardInterrupt): raise
        res = dict(seed=seed, brazo=brazo, T=T, t_corte=tc, seg=round(time.time() - t0, 1),
                   error=f"{type(e).__name__}: {e}", traza=traceback.format_exc()[-3000:])
    tmp = fin + '.tmp'
    with open(tmp, 'w', encoding='utf-8') as f: json.dump(res, f, default=str)
    os.replace(tmp, fin)
    return res


# ================================================================================ LA LETRA (PREREGISTRO_endosimbiosis.md §6)
# Correccion del coordinador (antes de cualquier serie; trinquete de Fable, D3): la FRACCION con simbionte NO decide (es descriptiva);
# deciden la PERSISTENCIA y el R0 de los portadores, PAREADOS contra los controles, y la domesticacion pareada contra AZAR_S.
TRINQUETE = 0.9                 # fraccion con simbionte tras el corte >= 0.9 en >= 10/20 semillas de AZAR_S o de INERTE -> trinquete


def veredicto(R, n_esperado=N):
    L = []
    by = {b: {x['seed']: x for x in R if x['brazo'] == b} for b in BRAZOS}
    semillas = sorted(set(x['seed'] for x in R))
    completo = all(len(by[b]) == n_esperado for b in BRAZOS) and not any(x.get('error') for x in R)
    errores = [(x['brazo'], x['seed'], x['error']) for x in R if x.get('error')]
    ok = [x for x in R if not x.get('error')]
    bloq = sum(x['bloqueados'] for x in ok)
    bloq_lib = sum(1 for x in ok if x['bloq_libres'] > 0)
    trunc = [(x['brazo'], x['seed'], x['err60']) for x in ok if x['err60'] is not None]
    lib_ext = sum(1 for x in by['VIDA_S'].values() if not x.get('error') and x['libres_extintos_t'] is not None
                  and x['libres_extintos_t'] < x['t_corte'])
    g = lambda b, s, k: (None if s not in by[b] or by[b][s].get('error') else by[b][s].get(k))

    def par(b1, b2, k):
        """pareado, estricto: (gana b1, gana b2, evaluables). Sin dato en cualquiera de los dos: no gana nadie."""
        w = l_ = n_ = 0
        for s in semillas:
            a_, c_ = g(b1, s, k), g(b2, s, k)
            if a_ is None or c_ is None: continue
            n_ += 1; w += int(a_ > c_); l_ += int(a_ < c_)
        return w, l_, n_

    def pos(b, k):
        return (sum(1 for s in semillas if g(b, s, k) is not None and g(b, s, k) > 0),
                sum(1 for s in semillas if g(b, s, k) is not None and g(b, s, k) < 0))

    def med(b, k):
        v_ = [g(b, s, k) for s in semillas if g(b, s, k) is not None]
        return round(float(np.median(v_)), 4) if v_ else None

    P1a = par('VIDA_S', 'INERTE', 'area_post'); P1b = par('VIDA_S', 'SIN_TRAGAR', 'area_post')
    P2a = par('VIDA_S', 'INERTE', 'delta_r0'); P2b = par('VIDA_S', 'BARAJADO', 'delta_r0')
    P3 = par('VIDA_S', 'AZAR_S', 'D'); P3b = par('VIDA_S', 'INERTE', 'D')
    ok1 = P1a[0] >= UMBRAL and P1b[0] >= UMBRAL
    ok2 = P2a[0] >= UMBRAL and P2b[0] >= UMBRAL
    ok3 = P3[0] >= UMBRAL and P3b[0] >= UMBRAL
    G_in_D = pos('INERTE', 'D'); G_az_D = pos('AZAR_S', 'D'); G_in_R0 = pos('INERTE', 'delta_r0')
    PLAC = pos('BARAJADO', 'D')   # placebo del instrumento de D: BARAJADO transmite un libre al azar -> el signo de D es una moneda
    trinq = {b: sum(1 for s in semillas if g(b, s, 'prev_post') is not None and g(b, s, 'prev_post') >= TRINQUETE) for b in ('AZAR_S', 'INERTE')}
    pers = {b: sum(1 for s in semillas if g(b, s, 'persiste')) for b in BRAZOS}
    L.append(f"P1 (persistencia pareada: cuerpos vivos tras el corte) VIDA_S > INERTE {P1a[0]}/{n_esperado} (menor {P1a[1]}) · VIDA_S > SIN_TRAGAR "
             f"{P1b[0]}/{n_esperado} (menor {P1b[1]}) · VIDA_S > BARAJADO {par('VIDA_S', 'BARAJADO', 'area_post')[0]} · VIDA_S > AZAR_S "
             f"{par('VIDA_S', 'AZAR_S', 'area_post')[0]} · medianas " + ' · '.join(f"{b} {med(b, 'area_post')}" for b in BRAZOS) + f" · persisten en T {pers}")
    L.append(f"P2 (R0 de los portadores: delta = r0 con simbionte al nacer - r0 sin, >= {MIN_GRUPO} por grupo) VIDA_S > INERTE {P2a[0]}/{n_esperado} "
             f"(evaluables {P2a[2]}) · VIDA_S > BARAJADO {P2b[0]}/{n_esperado} (evaluables {P2b[2]}) · VIDA_S > AZAR_S {par('VIDA_S', 'AZAR_S', 'delta_r0')[0]} · "
             f"delta > 0 en VIDA_S {pos('VIDA_S', 'delta_r0')[0]} · medianas delta " + ' · '.join(f"{b} {med(b, 'delta_r0')}" for b in BRAZOS if b != 'SIN_TRAGAR'))
    L.append(f"P3 (domesticacion pareada: D = media sobre los PARTOS de I(lo transmitido) - I(libres en la misma muestra)) VIDA_S > AZAR_S {P3[0]}/{n_esperado} (evaluables {P3[2]}) · VIDA_S > INERTE {P3b[0]}/{n_esperado} (evaluables {P3b[2]}) · placebo BARAJADO D > 0 {PLAC[0]}, < 0 {PLAC[1]} · D > 0: "
             f"VIDA_S {pos('VIDA_S', 'D')[0]} · INERTE {G_in_D[0]} · AZAR_S {G_az_D[0]} · BARAJADO {pos('BARAJADO', 'D')[0]} · medianas D "
             + ' · '.join(f"{b} {med(b, 'D')}" for b in BRAZOS if b != 'SIN_TRAGAR')
             + " · descriptivo D solo tras el corte " + ' · '.join(f"{b} {med(b, 'D_post')}" for b in BRAZOS if b != 'SIN_TRAGAR'))
    L.append("DESCRIPTIVO (no decide; trinquete de Fable): fraccion con simbionte tras el corte, medianas "
             + ' · '.join(f"{b} {med(b, 'prev_post')}" for b in BRAZOS) + f" · semillas con fraccion >= {TRINQUETE}: {trinq} · distancia dentro-libres en T "
             + ' · '.join(f"{b} {med(b, 'dist_T')}" for b in BRAZOS if b != 'SIN_TRAGAR'))

    def mB(b, q, k):
        v_ = [x['muerde'][q][k] for x in by[b].values() if not x.get('error') and x['muerde'][q][k] is not None]
        return round(float(np.median(v_)), 4) if v_ else None
    L.append("DESCRIPTIVO: fraccion de mordidas por letra en VIDA_S con canal " + str({k: mB('VIDA_S', 'con', k) for k in SIM.LETRAS})
             + " · sin canal " + str({k: mB('VIDA_S', 'sin', k) for k in SIM.LETRAS}))
    L.append(f"Guardias: errores {len(errores)} · bloqueados {bloq} · corridas con tope de libres {bloq_lib} · ERR-60 truncadas {trunc[:6]} · "
             f"VIDA_S con libres extintos antes del corte {lib_ext} · trinquete {trinq} · placebo de D (BARAJADO) {PLAC} · delta > 0 en INERTE {G_in_R0[0]} · "
             f"descriptivo, sesgo de adquisicion (D > 0 sin canal / sin seleccion): INERTE {G_in_D[0]} AZAR_S {G_az_D[0]}")
    nP = int(ok1) + int(ok2) + int(ok3)
    if not completo: v = f'NO EVALUABLE (serie incompleta o con errores: {errores[:3]})'
    elif bloq > 0: v = f'NO EVALUABLE (tope de cuerpos alcanzado: bloqueados = {bloq})'
    elif bloq_lib >= 5: v = f'NO EVALUABLE (el tope de SEGURIDAD de los libres actuo en {bloq_lib} corridas: la densidad no la regulo el mundo)'
    elif lib_ext >= 5: v = f'NO EVALUABLE (los libres se extinguieron antes del corte en {lib_ext} semillas de VIDA_S)'
    elif max(trinq.values()) >= 10: v = f'NO EVALUABLE (TRINQUETE: fraccion con simbionte >= {TRINQUETE} sin seleccion o sin canal en {trinq})'
    elif max(PLAC) >= UMBRAL: v = f'NO EVALUABLE (placebo de D: BARAJADO da D de un solo signo en {PLAC} de 20; el instrumento de D esta sesgado)'
    elif G_in_R0[0] >= UMBRAL: v = f'NO EVALUABLE (instrumento: en INERTE los que nacen con simbionte tienen mas hijos en {G_in_R0[0]}/20)'
    elif nP == 3: v = 'FUNCIONA: LA FUSION SE QUEDA POR SELECCION Y EL SIMBIONTE SE DOMESTICA (en esta ventana)'
    elif nP >= 1: v = f"HAY ALGO MODESTO (en esta ventana): pasan {[n for n, o in (('P1', ok1), ('P2', ok2), ('P3', ok3)) if o]}"
    else: v = 'NO (en esta ventana)'
    L.append(f"VEREDICTO ENDOSIMBIOSIS POR LA LETRA (una ventana; el bloque exige serie + replica con el mismo veredicto): {v}")
    return v, L, dict(P1a=P1a, P1b=P1b, P2a=P2a, P2b=P2b, P3=P3, P3b=P3b, PLAC=PLAC, G_in_D=G_in_D, G_az_D=G_az_D, G_in_R0=G_in_R0, trinq=trinq, pers=pers,
                      bloq=bloq, bloq_lib=bloq_lib, trunc=trunc, lib_ext=lib_ext, errores=errores)


def lee(carpeta, n_esperado=N):
    R = [json.load(open(p, encoding='utf-8')) for p in sorted(glob.glob(os.path.join(carpeta, '*_s*.json')))]
    v, L, d = veredicto(R, n_esperado)
    for l in L: print(l, flush=True)
    return v, L, d, R


def SHAS():
    f = lambda p: hashlib.sha256(open(p, 'rb').read()).hexdigest()[:16]
    d = {os.path.basename(p): f(os.path.join(AQUI, p)) for p in ('corre_endo.py', 'motor_endo.py', 'simbiontes.py', 'carros/FABRICA_SIMB.py',
                                                                 'construye_endo.py', 'identidad_endosimbiosis.py', 'PREREGISTRO_endosimbiosis.md')
         if os.path.exists(os.path.join(AQUI, p))}
    d['motor_eco3.py'] = f(os.path.join(RAIZ, 'experimentos', 'juaco_eco', 'motor_eco3.py'))
    d['corre_eco.py'] = f(os.path.join(RAIZ, 'experimentos', 'juaco_eco', 'corre_eco.py'))
    return d


def parsea(argv):
    ap = argparse.ArgumentParser(allow_abbrev=False, add_help=False)
    ap.add_argument('--humo', action='store_true'); ap.add_argument('--serie', action='store_true')
    ap.add_argument('--prueba_pool', action='store_true'); ap.add_argument('--lee', default=None)
    ap.add_argument('--ventana', default=None); ap.add_argument('--pool', type=int)
    ap.add_argument('--reanuda', action='store_true')
    try:
        a, resto = ap.parse_known_args(argv)
    except SystemExit:
        raise BanderaMala('ENDO: banderas mal formadas')
    if resto: raise BanderaMala(f"ENDO: banderas desconocidas {resto}")
    if any(x.startswith('--') and '=' in x for x in argv): raise BanderaMala('ENDO: sin la forma --bandera=valor')
    fl = [x for x in argv if x.startswith('--')]
    if len(fl) != len(set(fl)): raise BanderaMala('ENDO: bandera repetida')
    if int(a.humo) + int(a.serie) + int(a.prueba_pool) + int(a.lee is not None) != 1:
        raise BanderaMala('ENDO: exactamente uno de --humo, --serie, --prueba_pool, --lee')
    if a.humo and (a.ventana is not None or a.pool is not None or a.reanuda): raise BanderaMala('ENDO: --humo va solo')
    if a.lee is not None and (a.ventana is not None or a.pool is not None or a.reanuda): raise BanderaMala('ENDO: --lee va solo')
    if a.prueba_pool and (a.ventana is not None or a.pool != 2 or a.reanuda): raise BanderaMala('ENDO: --prueba_pool --pool 2')
    if a.serie and (a.ventana not in VENTANAS or a.pool is None or not 1 <= a.pool <= 6):
        raise BanderaMala('ENDO: --serie --ventana serie|replica --pool 1..6')
    return a


EVENTOS_HUMO = ('tragados', 'digeridos', 'quedan', 'herencias', 'herencias_mutadas', 'decisiones_canal', 'perdidas_internas',
                'fallas_herencia', 'fundadores_con_simb', 'nac_libres', 'muertes_libres')


def humo():
    ts = time.strftime('%Y%m%d_%H%M%S'); carpeta = os.path.join(DATOS, 'humo', f"endo_humo_{ts}")
    os.makedirs(carpeta, exist_ok=True); t0 = time.time()
    flog = open(os.path.join(carpeta, 'progreso.log'), 'a', encoding='utf-8')

    def log(s):
        s = f"[{time.strftime('%H:%M:%S')}] {s}"; print(s, flush=True); flog.write(s + '\n'); flog.flush()
    log(f"HUMO ENDOSIMBIOSIS (un proceso) · semilla {HUMO['semilla']} · T {HUMO['T']} · corte {HUMO['t_corte']} · shas {SHAS()}")
    R = []
    for b in BRAZOS:
        x = trabajo((HUMO['semilla'], b, HUMO['T'], HUMO['t_corte'], carpeta, False)); R.append(x)
        if x.get('error'): log(f"{b}: ERROR {x['error']}"); continue
        ev = x['eventos']
        log(f"{b}: {x['seg']} s · persiste {x['persiste']} (vivos {x['vivos_T']}, max {x['max_vivos']}) · area_post {x['area_post']} · delta_r0 {x['delta_r0']} · prev_post {x['prev_post']} · "
            f"r0 con/sin {x['r0_con']}({x['n_con']})/{x['r0_sin']}({x['n_sin']}) · D {x['D']} · eventos " + str({k: ev[k] for k in EVENTOS_HUMO}))
    ej = {b: {k: (x['eventos'][k] if not x.get('error') else None) for k in EVENTOS_HUMO} for b, x in zip(BRAZOS, R)}
    requeridos = {'VIDA_S': ('tragados', 'digeridos', 'quedan', 'herencias', 'decisiones_canal'),
                  'INERTE': ('tragados', 'quedan', 'herencias'), 'BARAJADO': ('quedan', 'herencias'),
                  'AZAR_S': ('quedan', 'herencias'), 'SIN_TRAGAR': ('nac_libres',)}
    ok = {b: all((ej[b][k] or 0) > 0 for k in ks) for b, ks in requeridos.items()}
    ok['SIN_TRAGAR_no_traga'] = (ej['SIN_TRAGAR']['tragados'] == 0)
    ok['INERTE_sin_canal'] = (ej['INERTE']['decisiones_canal'] == 0)
    v, L, d = veredicto(R, 1)
    for l in L: log('(letra con 1 semilla; SIN VALOR) ' + l)
    out = dict(humo=HUMO, shas=SHAS(), seg=round(time.time() - t0, 1), eventos=ej, ejercitado=ok, todos_ejercitados=all(ok.values()),
               nota='numeros SIN VALOR (una semilla de practica); el humo solo muestra que tragar, digerir, quedarse, heredar y actuar ocurren',
               corridas=[{k: x.get(k) for k in ('brazo', 'seg', 'error', 'persiste', 'vivos_T', 'max_vivos', 'area_post', 'delta_r0', 'prev_post', 'prev_T', 'r0_con', 'n_con',
                                                  'r0_sin', 'n_sin', 'D', 'n_D', 'D_post', 'n_D_post', 'I_don', 'n_don', 'I_libres_post', 'I_dentro_T', 'I_libres_T',
                                                  'g_dentro_T', 'g_libres_T', 'dist_T', 'muerde', 'err60', 'bloq_libres', 'libres_extintos_t')} for x in R],
               letra_1_semilla=L)
    fj = os.path.join(carpeta, 'HUMO_endosimbiosis.json')
    json.dump(out, open(fj, 'w', encoding='utf-8'), indent=1, default=str)
    log(f"EJERCITADO: {ok} · todos {all(ok.values())} · {round(time.time() - t0, 1)} s · {os.path.relpath(fj, RAIZ)}")
    flog.close()


def main(argv=None):
    a = parsea(sys.argv[1:] if argv is None else argv)
    if a.lee is not None: lee(a.lee); return
    if a.humo: humo(); return
    if a.prueba_pool:
        semillas = range(PRUEBA['desde'], PRUEBA['desde'] + PRUEBA['n']); T, tc = PRUEBA['T'], PRUEBA['t_corte']; etq = 'endo_prueba_pool'
    else:
        d0 = VENTANAS[a.ventana]; semillas = range(d0, d0 + N); T, tc = V['T'], V['t_corte']; etq = f"endo_{a.ventana}_s{d0}-{d0 + N - 1}"
    carpeta = os.path.join(DATOS, etq)
    if os.path.exists(carpeta) and not a.reanuda and glob.glob(os.path.join(carpeta, '*_s*.json')):
        raise SystemExit(f"ENDO: {carpeta} ya tiene resultados; --reanuda (no se pisa nada)")
    os.makedirs(carpeta, exist_ok=True)
    flog = open(os.path.join(carpeta, 'progreso.log'), 'a', encoding='utf-8')

    def log(s):
        s = f"[{time.strftime('%H:%M:%S')}] {s}"; print(s, flush=True); flog.write(s + '\n'); flog.flush()
    log(f"ENDO {etq} · T {T} · corte {tc} · mundo {MUNDO} · brazos {BRAZOS} · pool {a.pool} · shas {SHAS()}")
    jobs = [(s, b, T, tc, carpeta, a.reanuda) for s in semillas for b in BRAZOS]
    t0 = time.time()
    from multiprocessing import Pool
    with Pool(a.pool) as pool:
        for k, x in enumerate(pool.imap_unordered(trabajo, jobs), 1):
            if x.get('error'): log(f"[{k}/{len(jobs)}] {x['brazo']} s{x['seed']}: ERROR {x['error']}"); continue
            log(f"[{k}/{len(jobs)}] {x['brazo']} s{x['seed']}: persiste {x['persiste']} (vivos {x['vivos_T']}) · prev_post {x['prev_post']} · D {x['D']} · "
                f"err60 {x['err60']} ({x['seg']} s; {round(time.time() - t0)} s)")
    v, L, d, R = lee(carpeta, len(semillas))
    for l in L: flog.write(l + '\n')
    json.dump(dict(etiqueta=etq, veredicto=v, lineas=L, d=d, seg=round(time.time() - t0), V=V, MUNDO=MUNDO, shas=SHAS()),
              open(os.path.join(carpeta, 'RESUMEN.json'), 'w', encoding='utf-8'), indent=1, default=str)
    log(f"VEREDICTO: {v}")
    flog.close()


if __name__ == '__main__':
    try:
        main()
    except BanderaMala as e:
        print(str(e), file=sys.stderr); sys.exit(2)
