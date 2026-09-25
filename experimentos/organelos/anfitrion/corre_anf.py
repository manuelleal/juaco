"""corre_anf.py — RUNNER del paquete CONTROL DEL ANFITRION (organelos, Opus B, 24-sep-2026).

MISION: llegar a la AGI por este camino.

Preregistro: experimentos/organelos/anfitrion/PREREGISTRO_anfitrion.md (la letra esta AQUI, en veredicto(), y alli).
Motor: motor_anf.py (motor_endo + control_anfitrion; arnes identidad_anfitrion.py N/N) + darwin/carros/FABRICA_SIMB.
ARRANCA DESDE LO MAS EVOLUCIONADO (siembras.json): 30 fundadores con genomas del banco de VIDA de ECO v1.1 ([seed, 0, 33, 0]) y, salvo en
SIN_TRAGAR, con simbiontes DOMESTICADOS de la serie y la replica de endosimbiosis ([seed, 0, 31, 0]).
Mundo: w30 (el de endosimbiosis), quimiostato r 0.03; T 100 000, corte 40 000 (vivero mas corto: los fundadores ya vienen evolucionados).
Brazos: CONTROL, SIN_CONTROL, INERTE, SIN_TRAGAR, AZAR (control_anfitrion.py). Sin checkpoints; --reanuda salta los JSON ya escritos.
nube-9: cada trabajo ATRAPA toda excepcion y SystemExit y escribe su JSON con 'error'; ERR-60 con simb se registra y no lanza.
Uso (ERR-115: banderas desconocidas o abreviadas abortan; SOLO el coordinador lanza --serie y --prueba_pool):
  python experimentos/organelos/anfitrion/corre_anf.py --humo                                 # un proceso, semilla 26990
  python experimentos/organelos/anfitrion/corre_anf.py --prueba_pool --pool 2                 # 26993-26994, T 6000
  python experimentos/organelos/anfitrion/corre_anf.py --serie --ventana serie --pool 3       # 26001-26020
  python experimentos/organelos/anfitrion/corre_anf.py --serie --ventana replica --pool 3     # 26021-26040
  python experimentos/organelos/anfitrion/corre_anf.py --serie --ventana serie --pool 3 --reanuda
  python experimentos/organelos/anfitrion/corre_anf.py --lee <carpeta>
"""
import argparse, glob, hashlib, json, os, sys, time, traceback
import numpy as np

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(AQUI)))
DARWIN = os.path.join(os.path.dirname(AQUI), 'darwin')
for _d in (os.path.join(RAIZ, 'experimentos', 'generaciones'), os.path.join(RAIZ, 'experimentos', 'juaco_eco'), DARWIN, AQUI):
    if _d in sys.path: sys.path.remove(_d)
    sys.path.insert(0, _d)
try: sys.stdout.reconfigure(encoding='utf-8', errors='replace')
except Exception: pass
import corre_eco as CR          # eco_cfg('VIDA') del bicho
import corre_endo as CE         # medidas() de endosimbiosis (sha fijado abajo)
import motor_anf as MA
import control_anfitrion as CA

SHA_CE = '078734369e9721c5'
if hashlib.sha256(open(CE.__file__, 'rb').read()).hexdigest()[:16] != SHA_CE: raise SystemExit('ANF: darwin/corre_endo.py cambio')
SHA_SIEMBRAS = '8ff067ba6ace9f37'
CARRO = 'FABRICA_SIMB'
MUNDO = dict(esc=30, n0=30, tope=3000, muestra=1000, r_rep=0.03)
V = dict(T=100000, t_corte=40000, cola=20000)
BRAZOS = ('CONTROL', 'SIN_CONTROL', 'INERTE', 'SIN_TRAGAR', 'AZAR')
VENTANAS = {'serie': 26001, 'replica': 26021}
N = 20
UMBRAL = 15
MIN_GRUPO = 5
TRINQUETE = 0.9
PRUEBA = dict(desde=26993, n=2, T=6000, t_corte=3000)
HUMO = dict(semilla=26990, T=60000, t_corte=30000)
DATOS = os.path.join(AQUI, 'datos')
_SIEMBRAS = [None]


class BanderaMala(SystemExit):
    pass


def siembras():
    if _SIEMBRAS[0] is None:
        s = open(CA.SIEMBRAS, encoding='utf-8').read()
        if hashlib.sha256(s.encode()).hexdigest()[:16] != SHA_SIEMBRAS: raise SystemExit('ANF: siembras.json cambio')
        _SIEMBRAS[0] = json.loads(s)
    return _SIEMBRAS[0]


def huespedes(seed, n):
    P = siembras()['huespedes']
    idx = np.random.default_rng([seed, 0, 33, 0]).choice(len(P), size=n, replace=False)
    return [list(P[int(i)]) for i in idx]


def corre(seed, brazo, T, tc, simb_extra=None):
    e = CR.eco_cfg('VIDA', tc); e['genoma'] = huespedes(seed, MUNDO['n0'])
    simb = dict(brazo=brazo, siembra_s=siembras()['simbiontes']); simb.update(simb_extra or {})
    return MA.run_solapadas(seed, [CARRO] * MUNDO['n0'], T=T, diag=0, mundo_n=MUNDO['esc'], tope_cuerpos=MUNDO['tope'],
                            muestra=MUNDO['muestra'], r_rep=MUNDO['r_rep'], eco=e, simb=simb)


def medidas(r, T, tc):
    m = CE.medidas(r, T, tc)
    S = r['simb']
    T_ef = m['T_ef']
    coh = [f for f in S['ind10'] if f[6] == 0 and CA.T_REC <= f[2] <= T_ef - V['cola']]   # NACIDOS (no fundadores del vivero)
    con = [f[4] for f in coh if f[5]]; sin = [f[4] for f in coh if not f[5]]
    mean = lambda v: (round(float(np.mean(v)), 4) if v else None)
    cf = S['ctl_final']; cb = S['ctl_banco']
    m.update(r0n_con=mean(con), n_con_n=len(con), r0n_sin=mean(sin), n_sin_n=len(sin), r0n_todos=mean(con + sin), n_todos_n=len(con) + len(sin),
             tx_T=(mean([c[0] for c in cf])), san_T=(mean([c[1] for c in cf])), tx_banco=mean([c[0] for c in cb]), san_banco=mean([c[1] for c in cb]),
             ctl_fijo_ok=int(all(tuple(c) == CA.CTL0 for c in cf + cb)), bank_c_alineado=S['bank_c_alineado'], serie_ctl=S['serie_ctl'])
    return m


def trabajo(args):
    """UNA corrida. nube-9: NUNCA deja escapar una excepcion ni un SystemExit (el Pool no se cuelga)."""
    seed, brazo, T, tc, carpeta, reanuda = args
    fin = os.path.join(carpeta, f"{brazo}_s{seed}.json")
    if reanuda and os.path.exists(fin):
        try:
            x = json.load(open(fin, encoding='utf-8'))
            if x.get('error') is None: return x
        except Exception: pass
    t0 = time.time()
    try:
        r = corre(seed, brazo, T, tc)
        res = dict(seed=seed, brazo=brazo, T=T, t_corte=tc, seg=round(time.time() - t0, 1), error=None, **medidas(r, T, tc))
        for k in ('don', 'dentro_final', 'libres_final', 'decisiones', 'serie', 'ctl_final', 'ctl_banco', 'ind10'): res['c_' + k] = r['simb'][k]
        res['tam_total'] = r['pista']['tam_total']; res['cfg_simb'] = r['simb']['cfg']; res['ctl_cfg'] = r['simb']['ctl_cfg']
    except BaseException as e:   # nube-9: incluye SystemExit; KeyboardInterrupt se relanza
        if isinstance(e, KeyboardInterrupt): raise
        res = dict(seed=seed, brazo=brazo, T=T, t_corte=tc, seg=round(time.time() - t0, 1),
                   error=f"{type(e).__name__}: {e}", traza=traceback.format_exc()[-3000:])
    tmp = fin + '.tmp'
    with open(tmp, 'w', encoding='utf-8') as f: json.dump(res, f, default=str)
    os.replace(tmp, fin)
    return res


# ================================================================================ LA LETRA (PREREGISTRO_anfitrion.md §6)
def veredicto(R, n_esperado=N):
    L = []
    by = {b: {x['seed']: x for x in R if x['brazo'] == b} for b in BRAZOS}
    semillas = sorted(set(x['seed'] for x in R))
    errores = [(x['brazo'], x['seed'], x['error']) for x in R if x.get('error')]
    completo = all(len(by[b]) == n_esperado for b in BRAZOS) and not errores
    ok = [x for x in R if not x.get('error')]
    g = lambda b, s, k: (None if s not in by[b] or by[b][s].get('error') else by[b][s].get(k))

    def par(b1, k1, b2, k2, nmin=None):
        w = l_ = n_ = 0
        for s in semillas:
            a_, c_ = g(b1, s, k1), g(b2, s, k2)
            if a_ is None or c_ is None: continue
            if nmin is not None and ((g(b1, s, nmin[0]) or 0) < MIN_GRUPO or (g(b2, s, nmin[1]) or 0) < MIN_GRUPO): continue
            n_ += 1; w += int(a_ > c_); l_ += int(a_ < c_)
        return w, l_, n_

    def med(b, k):
        v_ = [g(b, s, k) for s in semillas if g(b, s, k) is not None]
        return round(float(np.median(v_)), 4) if v_ else None

    PC = par('CONTROL', 'area_post', 'SIN_CONTROL', 'area_post')
    P1a = par('CONTROL', 'area_post', 'SIN_TRAGAR', 'area_post'); P1b = par('CONTROL', 'area_post', 'INERTE', 'area_post')
    P2a = par('CONTROL', 'r0n_con', 'SIN_TRAGAR', 'r0n_todos', ('n_con_n', 'n_todos_n'))
    P2b = par('CONTROL', 'r0n_con', 'INERTE', 'r0n_con', ('n_con_n', 'n_con_n'))
    okC = PC[0] >= UMBRAL; ok1 = P1a[0] >= UMBRAL and P1b[0] >= UMBRAL; ok2 = P2a[0] >= UMBRAL and P2b[0] >= UMBRAL
    bloq = sum(x['bloqueados'] for x in ok); bloq_lib = sum(1 for x in ok if x['bloq_libres'] > 0)
    lib_ext = sum(1 for x in by['CONTROL'].values() if not x.get('error') and x['libres_extintos_t'] is not None and x['libres_extintos_t'] < x['t_corte'])
    trinq = {b: sum(1 for s in semillas if (g(b, s, 'prev_post') or 0) >= TRINQUETE) for b in ('AZAR', 'INERTE')}
    fijo_mal = [s for s in semillas if g('SIN_CONTROL', s, 'ctl_fijo_ok') == 0] + [s for s in semillas if g('SIN_TRAGAR', s, 'ctl_fijo_ok') == 0]
    trunc = [(x['brazo'], x['seed']) for x in ok if x.get('err60') is not None]
    pers = {b: sum(1 for s in semillas if g(b, s, 'persiste')) for b in BRAZOS}
    tx_sel = par('CONTROL', 'tx_banco', 'AZAR', 'tx_banco'); san_sel = par('CONTROL', 'san_banco', 'AZAR', 'san_banco')
    L.append(f"PC (el control sirve: cuerpos vivos tras el corte) CONTROL > SIN_CONTROL {PC[0]}/{n_esperado} (menor {PC[1]}) · medianas area_post "
             + ' · '.join(f"{b} {med(b, 'area_post')}" for b in BRAZOS) + f" · persisten en T {pers}")
    L.append(f"P1 (portar persiste) CONTROL > SIN_TRAGAR {P1a[0]}/{n_esperado} (menor {P1a[1]}) · CONTROL > INERTE {P1b[0]}/{n_esperado} (menor {P1b[1]})")
    L.append(f"P2 (R0 de los NACIDOS portadores, t >= {CA.T_REC}) CONTROL(portadores) > SIN_TRAGAR(todos) {P2a[0]}/{n_esperado} (evaluables {P2a[2]}) · "
             f"CONTROL(portadores) > INERTE(portadores) {P2b[0]}/{n_esperado} (evaluables {P2b[2]}) · medianas r0 portadores "
             + ' · '.join(f"{b} {med(b, 'r0n_con')}" for b in BRAZOS if b != 'SIN_TRAGAR') + f" · SIN_TRAGAR todos {med('SIN_TRAGAR', 'r0n_todos')}"
             + " · sin simbionte " + ' · '.join(f"{b} {med(b, 'r0n_sin')}" for b in BRAZOS))
    L.append(f"DESCRIPTIVO control: banco CONTROL vs AZAR tx {tx_sel[0]} mayor/{tx_sel[1]} menor · san {san_sel[0]} mayor/{san_sel[1]} menor · medianas tx_banco "
             + ' · '.join(f"{b} {med(b, 'tx_banco')}" for b in ('CONTROL', 'INERTE', 'AZAR')) + " · san_banco "
             + ' · '.join(f"{b} {med(b, 'san_banco')}" for b in ('CONTROL', 'INERTE', 'AZAR'))
             + " · sanciones (mediana) " + ' · '.join(f"{b} {med(b, 'n_sanciones')}" for b in ('CONTROL', 'AZAR')))
    L.append("DESCRIPTIVO: fraccion con simbionte tras el corte " + ' · '.join(f"{b} {med(b, 'prev_post')}" for b in BRAZOS)
             + " · D " + ' · '.join(f"{b} {med(b, 'D')}" for b in BRAZOS if b != 'SIN_TRAGAR'))
    L.append(f"Guardias: errores {len(errores)} · bloqueados {bloq} · tope de libres {bloq_lib} · libres extintos antes del corte (CONTROL) {lib_ext} · "
             f"trinquete {trinq} · control que debia quedar fijo y se movio {fijo_mal} · ERR-60 truncadas {trunc[:6]}")
    nP = int(okC) + int(ok1) + int(ok2)
    if not completo: v = f'NO EVALUABLE (ventana incompleta o con errores: {errores[:3]})'
    elif bloq > 0: v = f'NO EVALUABLE (tope de cuerpos: bloqueados = {bloq})'
    elif bloq_lib >= 5: v = f'NO EVALUABLE (tope de los libres en {bloq_lib} corridas)'
    elif lib_ext >= 5: v = f'NO EVALUABLE (libres extintos antes del corte en {lib_ext} semillas de CONTROL)'
    elif max(trinq.values()) >= 10: v = f'NO EVALUABLE (TRINQUETE: {trinq})'
    elif fijo_mal: v = f'NO EVALUABLE (instrumento: el control fijo se movio en {fijo_mal[:5]})'
    elif nP == 3: v = 'FUNCIONA: CON CONTROL DEL ANFITRION, PORTAR ES BUEN NEGOCIO (en esta ventana)'
    elif nP >= 1: v = f"HAY ALGO MODESTO (en esta ventana): pasan {[n for n, o in (('PC', okC), ('P1', ok1), ('P2', ok2)) if o]}"
    else: v = 'NO (en esta ventana)'
    L.append(f"VEREDICTO CONTROL DEL ANFITRION POR LA LETRA (una ventana; el bloque exige serie + replica con el mismo veredicto): {v}")
    return v, L, dict(PC=PC, P1a=P1a, P1b=P1b, P2a=P2a, P2b=P2b, tx_sel=tx_sel, san_sel=san_sel, pers=pers, trinq=trinq, fijo_mal=fijo_mal,
                      bloq=bloq, bloq_lib=bloq_lib, lib_ext=lib_ext, errores=errores)


def lee(carpeta, n_esperado=N):
    R = [json.load(open(p, encoding='utf-8')) for p in sorted(glob.glob(os.path.join(carpeta, '*_s*.json')))]
    for x in R:
        if not x.get('error'): x['n_sanciones'] = x['eventos'].get('sanciones')
    v, L, d = veredicto(R, n_esperado)
    for l in L: print(l, flush=True)
    return v, L, d, R


def SHAS():
    f = lambda p: hashlib.sha256(open(p, 'rb').read()).hexdigest()[:16]
    d = {p: f(os.path.join(AQUI, p)) for p in ('corre_anf.py', 'motor_anf.py', 'control_anfitrion.py', 'construye_anf.py', 'construye_siembras.py',
                                               'identidad_anfitrion.py', 'siembras.json', 'PREREGISTRO_anfitrion.md') if os.path.exists(os.path.join(AQUI, p))}
    for p in ('simbiontes.py', 'motor_endo.py', 'corre_endo.py', 'carros/FABRICA_SIMB.py'): d['darwin/' + p] = f(os.path.join(DARWIN, p))
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
        raise BanderaMala('ANF: banderas mal formadas')
    if resto: raise BanderaMala(f"ANF: banderas desconocidas {resto}")
    if any(x.startswith('--') and '=' in x for x in argv): raise BanderaMala('ANF: sin la forma --bandera=valor')
    fl = [x for x in argv if x.startswith('--')]
    if len(fl) != len(set(fl)): raise BanderaMala('ANF: bandera repetida')
    if int(a.humo) + int(a.serie) + int(a.prueba_pool) + int(a.lee is not None) != 1:
        raise BanderaMala('ANF: exactamente uno de --humo, --serie, --prueba_pool, --lee')
    if (a.humo or a.lee is not None) and (a.ventana is not None or a.pool is not None or a.reanuda): raise BanderaMala('ANF: --humo y --lee van solos')
    if a.prueba_pool and (a.ventana is not None or a.pool != 2 or a.reanuda): raise BanderaMala('ANF: --prueba_pool --pool 2')
    if a.serie and (a.ventana not in VENTANAS or a.pool is None or not 1 <= a.pool <= 6):
        raise BanderaMala('ANF: --serie --ventana serie|replica --pool 1..6')
    return a


EV_HUMO = ('sembrados', 'tragados', 'digeridos', 'quedan', 'herencias', 'decisiones_canal', 'perdidas_internas', 'fallas_herencia',
           'rechazos_tx', 'sancion_candidatos', 'sanciones', 'mut_ctl', 'fundadores_con_simb', 'nac_libres')


def humo():
    ts = time.strftime('%Y%m%d_%H%M%S'); carpeta = os.path.join(DATOS, 'humo', f"anf_humo_{ts}")
    os.makedirs(carpeta, exist_ok=True); t0 = time.time()
    flog = open(os.path.join(carpeta, 'progreso.log'), 'a', encoding='utf-8')

    def log(s):
        s = f"[{time.strftime('%H:%M:%S')}] {s}"; print(s, flush=True); flog.write(s + '\n'); flog.flush()
    log(f"HUMO CONTROL DEL ANFITRION (un proceso) · semilla {HUMO['semilla']} · T {HUMO['T']} · corte {HUMO['t_corte']} · shas {SHAS()}")
    R = []
    for b in BRAZOS:
        x = trabajo((HUMO['semilla'], b, HUMO['T'], HUMO['t_corte'], carpeta, False)); R.append(x)
        if x.get('error'): log(f"{b}: ERROR {x['error']}"); continue
        x['n_sanciones'] = x['eventos'].get('sanciones')
        log(f"{b}: {x['seg']} s · area_post {x['area_post']} · persiste {x['persiste']} · r0 nacidos con/sin {x['r0n_con']}({x['n_con_n']})/{x['r0n_sin']}({x['n_sin_n']}) · "
            f"tx/san banco {x['tx_banco']}/{x['san_banco']} · prev_post {x['prev_post']} · eventos " + str({k: x['eventos'].get(k) for k in EV_HUMO}))
    ej = {b: ({k: x['eventos'].get(k) for k in EV_HUMO} if not x.get('error') else None) for b, x in zip(BRAZOS, R)}
    req = {'CONTROL': ('sembrados', 'quedan', 'herencias', 'decisiones_canal', 'mut_ctl', 'sancion_candidatos'),
           'SIN_CONTROL': ('sembrados', 'herencias', 'decisiones_canal'), 'INERTE': ('sembrados', 'herencias', 'mut_ctl'),
           'AZAR': ('sembrados', 'herencias', 'mut_ctl'), 'SIN_TRAGAR': ('nac_libres',)}
    okd = {b: bool(ej[b]) and all((ej[b].get(k) or 0) > 0 for k in ks) for b, ks in req.items()}
    okd['CONTROL_rechaza_o_sanciona'] = bool(ej['CONTROL']) and ((ej['CONTROL']['rechazos_tx'] or 0) + (ej['CONTROL']['sanciones'] or 0) > 0)
    okd['SIN_CONTROL_fijo'] = (not R[1].get('error')) and R[1]['ctl_fijo_ok'] == 1 and ej['SIN_CONTROL']['rechazos_tx'] == 0 and ej['SIN_CONTROL']['sanciones'] == 0
    okd['SIN_TRAGAR_sin_siembra'] = bool(ej['SIN_TRAGAR']) and ej['SIN_TRAGAR']['sembrados'] == 0 and ej['SIN_TRAGAR']['tragados'] == 0
    okd['INERTE_sin_canal'] = bool(ej['INERTE']) and ej['INERTE']['decisiones_canal'] == 0 and ej['INERTE']['sanciones'] == 0
    v, L, d = veredicto(R, 1)
    for l in L: log('(letra con 1 semilla; SIN VALOR) ' + l)
    keep = ('brazo', 'seg', 'error', 'area_post', 'persiste', 'vivos_T', 'max_vivos', 'r0n_con', 'n_con_n', 'r0n_sin', 'n_sin_n', 'r0n_todos', 'n_todos_n',
            'r0_con', 'n_con', 'r0_sin', 'n_sin', 'tx_T', 'san_T', 'tx_banco', 'san_banco', 'prev_post', 'D', 'err60', 'bloq_libres', 'libres_extintos_t')
    out = dict(humo=HUMO, shas=SHAS(), seg=round(time.time() - t0, 1), eventos=ej, ejercitado=okd, todos_ejercitados=all(okd.values()),
               nota='numeros SIN VALOR (una semilla de practica): el humo solo muestra que sembrar, tragar, heredar, rechazar, sancionar y mutar el control ocurren',
               corridas=[{k: x.get(k) for k in keep} for x in R], letra_1_semilla=L)
    fj = os.path.join(carpeta, 'HUMO_anfitrion.json')
    json.dump(out, open(fj, 'w', encoding='utf-8'), indent=1, default=str)
    log(f"EJERCITADO: {okd} · todos {all(okd.values())} · {round(time.time() - t0, 1)} s · {os.path.relpath(fj, RAIZ)}")
    flog.close()


def main(argv=None):
    a = parsea(sys.argv[1:] if argv is None else argv)
    if a.lee is not None: lee(a.lee); return
    if a.humo: humo(); return
    if a.prueba_pool:
        semillas = range(PRUEBA['desde'], PRUEBA['desde'] + PRUEBA['n']); T, tc = PRUEBA['T'], PRUEBA['t_corte']; etq = 'anf_prueba_pool'
    else:
        d0 = VENTANAS[a.ventana]; semillas = range(d0, d0 + N); T, tc = V['T'], V['t_corte']; etq = f"anf_{a.ventana}_s{d0}-{d0 + N - 1}"
    carpeta = os.path.join(DATOS, etq)
    if os.path.exists(carpeta) and not a.reanuda and glob.glob(os.path.join(carpeta, '*_s*.json')):
        raise SystemExit(f"ANF: {carpeta} ya tiene resultados; --reanuda (no se pisa nada)")
    os.makedirs(carpeta, exist_ok=True)
    flog = open(os.path.join(carpeta, 'progreso.log'), 'a', encoding='utf-8')

    def log(s):
        s = f"[{time.strftime('%H:%M:%S')}] {s}"; print(s, flush=True); flog.write(s + '\n'); flog.flush()
    log(f"ANF {etq} · T {T} · corte {tc} · mundo {MUNDO} · brazos {BRAZOS} · pool {a.pool} · shas {SHAS()}")
    siembras()
    jobs = [(s, b, T, tc, carpeta, a.reanuda) for s in semillas for b in BRAZOS]
    t0 = time.time()
    from multiprocessing import Pool
    with Pool(a.pool) as pool:
        for k, x in enumerate(pool.imap_unordered(trabajo, jobs), 1):
            if x.get('error'): log(f"[{k}/{len(jobs)}] {x['brazo']} s{x['seed']}: ERROR {x['error']}"); continue
            log(f"[{k}/{len(jobs)}] {x['brazo']} s{x['seed']}: area_post {x['area_post']} · persiste {x['persiste']} · r0 nacidos con/sin "
                f"{x['r0n_con']}({x['n_con_n']})/{x['r0n_sin']}({x['n_sin_n']}) · tx/san {x['tx_banco']}/{x['san_banco']} ({x['seg']} s; {round(time.time() - t0)} s)")
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
