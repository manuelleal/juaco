"""corre_ohno.py — RUNNER de OHNO SOBRE BASE VIVA: ¿la seleccion MEJORA el organo ganador (filtra0) duplicandolo y dejando divergir la
copia? (Opus A, 24-sep-2026). Principio del director: la evolucion arranca DESDE LO MAS EVOLUCIONADO que tengamos.

MISION: llegar a la AGI por este camino.

Preregistro: experimentos/organelos/ohno/PREREGISTRO_ohno.md (la letra esta AQUI, en veredicto(), y alli).
Instrumento: copias BYTE A BYTE de gramatica/ (construye_ohno.py): motor_gramatica + carros/FAMB_GRAM_ECO + gramatica_def + conducta.
Mundo: w30 con el quimiostato MAS POBRE que fija la calibracion (R_REP; PREREGISTRO §3), para que filtra0 fijo NO este en el techo.
Brazos (vivero con banco 200 y 8 sombras hasta el corte; despues nadie repone nada):
  VIDA          los 30 fundadores con filtra0 (nacer/sin0/hijo/copiar) EXPRESADO + errores de copia (campo 0.05, duplicacion 0.02,
                borrado 0.02, tope 4) + mutacion numerica (18 genes); el hijo copia al padre.
  FIJO:filtra0  igual sin errores de copia de la gramatica (= MUT0 de la gramatica; la mutacion numerica sigue, como en VIDA).
  AZAR          como VIDA, pero todo cuerpo nuevo copia una entrada AL AZAR del banco (deriva pura).
  (arnes)       VIDA_SINMUT = VIDA con las tasas de la gramatica en 0; GRAM_VIDA = el brazo VIDA de corre_gramatica (fundadores al azar).
nube-9: trabajo() atrapa SystemExit/Exception del motor, escribe el JSON con 'abortado' y nunca cuelga un Pool.

Uso (banderas desconocidas o abreviadas abortan, ERR-115):
  python experimentos/organelos/ohno/corre_ohno.py --humo
  python experimentos/organelos/ohno/corre_ohno.py --calibra --rrep X --desde S --n K         # un proceso, FIJO:filtra0 al T de la serie
  python experimentos/organelos/ohno/corre_ohno.py --prueba_pool --pool 2
  python experimentos/organelos/ohno/corre_ohno.py --serie --ventana serie|replica --pool 3 [--reanuda]   # SOLO el coordinador
  python experimentos/organelos/ohno/corre_ohno.py --lee <carpeta>
"""
import argparse, glob, hashlib, json, os, pickle, sys, time
import numpy as np

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(AQUI)))
for _d in (AQUI, os.path.join(RAIZ, 'experimentos', 'generaciones')):
    if _d not in sys.path: sys.path.insert(0, _d)
import motor_gramatica as MG
import gramatica_def as GD

CARRO = 'FAMB_GRAM_ECO'
R_REP = 0.006           # quimiostato de OHNO (w30 de ECO: 0.03). Fijado por la CALIBRACION 25901-25918 y la regla de §3b (PREREGISTRO)
MUNDO = dict(nombre='w30_pobre', esc=30, n0=30, tope=3000)
SERIE = dict(T=80000, t_corte=40000, r0_margen=15000, banco=200, n_sombra=8, sigma=0.15, p_mut=0.05, cada_gen=2000, ckpt_cada=10000)
GRAM = dict(p_campo=0.05, p_dup=0.02, p_del=0.02, tope=4)
ALFABETO = (tuple(range(len(GD.CUANDO))), tuple(range(len(GD.QUE))), tuple(range(len(GD.QUIEN))), (0, 1, 2))   # sin 'olvidar' (gramatica §2c)
MUTABLES = tuple(g for g in MG.NOMBRES if g not in ('ensena', 'filtra0'))
BRAZOS_SERIE = ('VIDA', 'FIJO:filtra0', 'AZAR')
VENTANAS = {'serie': 25011, 'replica': 25031}
N = 20
HUMO = dict(semilla=25001, T=20000, t_corte=10000, r0_margen=5000)
PRUEBA = dict(desde=25991, n=2, T=12000, t_corte=10000, r0_margen=1000)
DATOS = os.path.join(AQUI, 'datos')


class BanderaMala(SystemExit):
    pass


def eco_de(brazo, seed, t_corte, **extra):
    gm = True; don = 'padre'
    if brazo == 'VIDA': grs = [GD.FILTRA0] * MUNDO['n0']
    elif brazo == 'VIDA_SINMUT': grs = [GD.FILTRA0] * MUNDO['n0']; gm = False
    elif brazo == 'FIJO:filtra0': grs = [GD.FILTRA0] * MUNDO['n0']; gm = False
    elif brazo == 'AZAR': grs = [GD.FILTRA0] * MUNDO['n0']; don = 'azar'
    elif brazo == 'GRAM_VIDA': grs = GD.fundadores_silenciosos(seed, MUNDO['n0'], ALFABETO)
    elif brazo.startswith('FIJO:'):   # arnes por pieza: 'FIJO:1.3.0.0+1.3.2.0*' (el * marca origen 1)
        grs = [tuple(tuple(int(z) for z in s.rstrip('*').split('.')) + ((1,) if s.endswith('*') else (0,)) for s in brazo[5:].split('+'))] * MUNDO['n0']
        gm = False
    else: raise SystemExit(f"OHNO: brazo desconocido {brazo}")
    return dict(refunda=1, t_corte=t_corte, p_mut=SERIE['p_mut'], sigma=SERIE['sigma'], banco=SERIE['banco'], n_sombra=SERIE['n_sombra'],
                cada_gen=SERIE['cada_gen'], mutables=MUTABLES, donante=don, gramatica=grs,
                g_pcampo=(GRAM['p_campo'] if gm else 0.0), g_pdup=(GRAM['p_dup'] if gm else 0.0), g_pdel=(GRAM['p_del'] if gm else 0.0),
                g_tope=GRAM['tope'], g_alfabeto=ALFABETO, **extra)


def _lista(gr): return [list(s) for s in gr] if gr is not None else None
def _tup(g): return tuple(tuple(s) for s in g) if g is not None else ()


def trabajo(args):
    """UNA corrida. Escribe su JSON. Nunca lanza: atrapa SystemExit/Exception del motor (nube-9)."""
    seed, brazo, T, t_corte, r0_margen, r_rep, carpeta, reanuda = args
    nom = brazo.replace(':', '_').replace('+', '_').replace('*', 'd')
    fin = os.path.join(carpeta, f"{nom}_s{seed}.json")
    if reanuda and os.path.exists(fin): return json.load(open(fin, encoding='utf-8'))
    ck = os.path.join(carpeta, 'ckpt', f"{nom}_s{seed}.pkl"); os.makedirs(os.path.dirname(ck), exist_ok=True)
    filas = []

    def cb(li, row, g):
        if row[3] >= t_corte: filas.append([li] + row)

    def guarda(t, blob):
        tmp = ck + '.tmp'
        with open(tmp, 'wb') as f: pickle.dump(dict(t=t, blob=blob, filas=filas), f, protocol=pickle.HIGHEST_PROTOCOL)
        os.replace(tmp, ck)
    estado = None
    if reanuda and os.path.exists(ck):
        d = pickle.load(open(ck, 'rb')); estado = d['blob']; filas[:] = d['filas']
    t0 = time.time(); abortado = None; r = None
    try:
        r = MG.run_solapadas(seed, [CARRO] * MUNDO['n0'], T=T, diag=0, mundo_n=MUNDO['esc'], tope_cuerpos=MUNDO['tope'], muestra=1000,
                             r_rep=r_rep, eco=eco_de(brazo, seed, t_corte, ckpt_cada=(SERIE['ckpt_cada'] if T >= 2 * SERIE['ckpt_cada'] else 0),
                                                     ckpt_fn=guarda, estado=estado, ind_cb=cb))
    except SystemExit as e: abortado = f"SystemExit: {e}"          # nube-9
    except Exception as e: abortado = f"{type(e).__name__}: {e}"
    res = dict(seed=seed, brazo=brazo, T=T, t_corte=t_corte, r0_margen=r0_margen, r_rep=r_rep, seg=round(time.time() - t0, 1), abortado=abortado,
               mundo=MUNDO, gram_cfg=dict(GRAM, alfabeto=[list(a) for a in ALFABETO]))
    if r is not None:
        E = r['eco']; P = r['pista']; G = r['gram']
        coh = [f for f in filas if f[4] <= T - r0_margen]
        res.update(t_ext=E['t_ext'], persiste=int(E['t_ext'] is None and len(E['vivos_final']) > 0), vivos_T=len(E['vivos_final']),
                   linajes_T=len(set(v[0] for v in E['vivos_final'])), bloqueados=P['bloqueados'], max_vivos=P['max_vivos'], r_paso=P['r_paso'],
                   n_nac=E['n_nac'], n_refund=E['n_refund'], n_banco=E['n_banco'], nac_post=len(filas),
                   r0_post=(round(float(np.mean([f[6] for f in coh])), 4) if coh else None), n_coh_post=len(coh),
                   tam_total=P['tam_total'], max_nac_linaje=G['max_nac_linaje'], g_nmut=G['g_nmut'], entregas=G['entregas'],
                   corte_gr=(None if not G['corte'] else dict(t=G['corte']['t'], banco_gr=[_lista(x) for x in G['corte']['banco_gr']],
                                                            banco_gs=[[_lista(y) for y in x] for x in G['corte']['banco_gs']])),
                   final_banco_gr=[_lista(x) for x in G['banco_final_gr']], final_banco_gs=[[_lista(y) for y in x] for x in G['banco_final_gs']],
                   vivos_gr=[v[:4] + [_lista(v[4])] for v in G['vivos_gr']],
                   carro_n10=[(d.get('carro') or {}).get('n10') for d in r['linajes']][:3])
    tmp = fin + '.tmp'
    with open(tmp, 'w', encoding='utf-8') as f: json.dump(res, f)
    os.replace(tmp, fin)
    if os.path.exists(ck) and abortado is None: os.remove(ck)
    return res


# ================================================================================ ANALISIS (conducta)
def modal(banco):
    """La CONDUCTA mas frecuente del banco (agrupada por conducta, TOL de conducta.py): (gramatica representante, fraccion)."""
    import conducta as C
    grupos = []
    for g in banco:
        g = _tup(g)
        for gr_ in grupos:
            if C.igual(g, gr_[0]): gr_[1] += 1; break
        else: grupos.append([g, 1])
    if not grupos: return None, 0.0
    g, k = max(grupos, key=lambda x: x[1])
    return g, k / len(banco)


def ohno(g):
    """P-OHNO por genoma: >= 2 slots activos, uno nacido por DUPLICACION (origen 1) cuya conducta de un slot no es la de ningun disenado
    ni la de los otros slots, y la gramatica sin ese slot tiene OTRA conducta; y la gramatica entera no es conductualmente filtra0."""
    import conducta as C
    g = _tup(g); act = [s for s in g if s[0] != 0]
    if len(act) < 2 or C.igual(g, GD.FILTRA0): return False
    for s in act:
        if s[4] != 1: continue
        uno = ((s[:4] + (0,)),)
        if C.clase_disenada(uno) is not None: continue
        if any(C.igual(uno, ((o[:4] + (0,)),)) for o in act if o is not s): continue
        if not C.igual(g, tuple(o for o in g if o is not s)): return True
    return False


def veredicto(R, n_esperado=N):
    """La letra (PREREGISTRO_ohno §6)."""
    import conducta as C
    L = []
    by = {b: {x['seed']: x for x in R if x['brazo'] == b} for b in BRAZOS_SERIE}
    completo = all(len(by[b]) == n_esperado for b in BRAZOS_SERIE)
    abortados = [(x['brazo'], x['seed'], x['abortado']) for x in R if x.get('abortado')]
    bloq = sum(x.get('bloqueados', 0) for x in R if not x.get('abortado'))
    r0 = lambda x: float(x.get('r0_post') or 0.0)   # sin cohorte (extinto antes) = 0
    semillas = sorted(set(by['VIDA']) & set(by['FIJO:filtra0']))
    g1 = sum(1 for s in semillas if r0(by['VIDA'][s]) > r0(by['FIJO:filtra0'][s]))
    g1m = sum(1 for s in semillas if r0(by['VIDA'][s]) < r0(by['FIJO:filtra0'][s]))
    az = sum(1 for s in semillas if s in by['AZAR'] and r0(by['AZAR'][s]) > r0(by['FIJO:filtra0'][s]))
    pers = {b: sum(int(x.get('persiste', 0)) for x in by[b].values()) for b in BRAZOS_SERIE}
    medr0 = {b: (round(float(np.median([r0(x) for x in by[b].values()])), 4) if by[b] else None) for b in BRAZOS_SERIE}
    G1 = g1 >= 15; G2 = pers['VIDA'] >= pers['FIJO:filtra0']
    g3 = po = 0; txt = []; frac = []
    for s, x in sorted(by['VIDA'].items()):
        if x.get('abortado') or not x.get('final_banco_gr'): txt.append((s, 'sin banco')); continue
        fr_r = float(np.mean([ohno(g) for g in x['final_banco_gr']]))
        fr_s = float(np.mean([np.mean([ohno(gs[q]) for gs in x['final_banco_gs']]) for q in range(SERIE['n_sombra'])]))
        frac.append((fr_r, fr_s))
        if not x.get('persiste'): txt.append((s, 'extinta', round(fr_r, 3), round(fr_s, 3))); continue
        g, f = modal(x['final_banco_gr']); dis = C.clase_disenada(g); o = ohno(g)
        g3 += int(dis is None); po += int(o)
        txt.append((s, GD.texto(g), round(f, 3), dis or 'NUEVO', 'OHNO' if o else '', round(fr_r, 3), round(fr_s, 3)))
    G3 = g3 >= 10; PO = po >= 5
    somb = sum(1 for a, b in frac if a > b)
    fijo = by['FIJO:filtra0']; techo = pers['FIJO:filtra0'] >= 18 and (medr0['FIJO:filtra0'] or 0) >= 0.9
    inviable = pers['FIJO:filtra0'] <= 2
    L.append(f"R0 de nacidos tras el corte (mediana): {medr0} · persisten en T: {pers}")
    L.append(f"G1 VIDA > FIJO:filtra0 en R0 (pareado) {g1}/{len(semillas)} (VIDA < FIJO {g1m}) · AZAR > FIJO {az} · G2 persiste VIDA >= FIJO: {G2}")
    L.append(f"G3 modal de VIDA NO disenada {g3}/20 · P-OHNO modal con duplicado divergente {po}/20 · fraccion del banco con OHNO real > sombras {somb}/{len(frac)}")
    for t in txt: L.append(f"  VIDA s{t[0]}: {t[1:]}")
    if not completo: v = 'NO EVALUABLE (ventana incompleta)'
    elif abortados: v = f'NO EVALUABLE (abortadas por el motor: {abortados[:3]})'
    elif bloq > 0: v = f'NO EVALUABLE (tope de cuerpos: bloqueados = {bloq})'
    elif techo: v = 'NO EVALUABLE (TECHO: FIJO:filtra0 persiste >= 18/20 con R0 >= 0.9; la calibracion no se sostuvo)'
    elif inviable: v = 'NO EVALUABLE (mundo INVIABLE: FIJO:filtra0 persiste <= 2/20)'
    elif G1 and G2 and G3 and PO: v = 'FUNCIONA — LA SELECCION MEJORA EL ORGANO GANADOR CON UN DUPLICADO QUE DIVERGE (Ohno)'
    elif G1 and G2 and G3: v = 'FUNCIONA — LA SELECCION MEJORA EL ORGANO GANADOR CON UN ORGANO NO DISENADO'
    elif (G1 and G2) or (PO and g1m < 15): v = 'HAY ALGO MODESTO (VIDA le gana a filtra0 fijo sin organo nuevo, o aparece el duplicado divergente sin perder)'
    else: v = 'NO'
    L.append(f"VEREDICTO OHNO POR LA LETRA (una ventana; el bloque exige serie + replica con el mismo veredicto): {v}")
    return v, L, dict(G1=G1, G2=G2, G3=G3, PO=PO, g1=g1, g1m=g1m, g3=g3, po=po, pers=pers, r0=medr0, somb=somb)


def SHAS():
    f = lambda p: hashlib.sha256(open(os.path.join(AQUI, p), 'rb').read()).hexdigest()[:16]
    return {p: f(p) for p in ('corre_ohno.py', 'motor_gramatica.py', 'carros/FAMB_GRAM_ECO.py', 'gramatica_def.py', 'conducta.py',
                              'construye_ohno.py', 'PREREGISTRO_ohno.md') if os.path.exists(os.path.join(AQUI, p))}


def parsea(argv):
    ap = argparse.ArgumentParser(allow_abbrev=False, add_help=False)
    for b in ('--humo', '--serie', '--prueba_pool', '--calibra', '--reanuda'): ap.add_argument(b, action='store_true')
    ap.add_argument('--lee', default=None); ap.add_argument('--ventana', default=None); ap.add_argument('--pool', type=int)
    ap.add_argument('--rrep', type=float); ap.add_argument('--desde', type=int); ap.add_argument('--n', type=int)
    try:
        a, resto = ap.parse_known_args(argv)
    except SystemExit:
        raise BanderaMala('OHNO: banderas mal formadas')
    if resto: raise BanderaMala(f"OHNO: banderas desconocidas {resto}")
    if any(x.startswith('--') and '=' in x for x in argv): raise BanderaMala('OHNO: sin la forma --bandera=valor')
    fl = [x for x in argv if x.startswith('--')]
    if len(fl) != len(set(fl)): raise BanderaMala('OHNO: bandera repetida')
    if int(a.humo) + int(a.serie) + int(a.prueba_pool) + int(a.calibra) + int(a.lee is not None) != 1:
        raise BanderaMala('OHNO: exactamente uno de --humo, --calibra, --prueba_pool, --serie, --lee')
    extra = lambda *ks: any(getattr(a, k) not in (None, False) for k in ks)
    if a.humo and extra('ventana', 'pool', 'reanuda', 'rrep', 'desde', 'n'): raise BanderaMala('OHNO: --humo va solo')
    if a.lee is not None and extra('ventana', 'pool', 'reanuda', 'rrep', 'desde', 'n'): raise BanderaMala('OHNO: --lee va solo')
    if a.calibra and (a.rrep is None or a.desde is None or a.n is None or not 25900 <= a.desde <= 25989 or extra('ventana', 'pool', 'reanuda')):
        raise BanderaMala('OHNO: --calibra --rrep X --desde 25900..25989 --n K (un proceso)')
    if a.prueba_pool and (a.pool != 2 or extra('ventana', 'reanuda', 'rrep', 'desde', 'n')): raise BanderaMala('OHNO: --prueba_pool --pool 2')
    if a.serie and (a.ventana not in VENTANAS or a.pool is None or not 1 <= a.pool <= 6 or extra('rrep', 'desde', 'n')):
        raise BanderaMala('OHNO: --serie --ventana serie|replica --pool 1..6 [--reanuda]')
    return a


def _pool(jobs, pool, log):
    from multiprocessing import Pool
    t0 = time.time()
    with Pool(pool) as p:
        for k, x in enumerate(p.imap_unordered(trabajo, jobs), 1):
            log(f"[{k}/{len(jobs)}] {x['brazo']} s{x['seed']}: persiste {x.get('persiste')} vivos {x.get('vivos_T')} r0 {x.get('r0_post')} "
                f"abort {x['abortado']} ({x['seg']} s; {round(time.time() - t0)} s)")


def main(argv=None):
    a = parsea(sys.argv[1:] if argv is None else argv)
    if a.lee is not None:
        R = [json.load(open(p, encoding='utf-8')) for p in sorted(glob.glob(os.path.join(a.lee, '*_s*.json')))]
        v, L, d = veredicto(R)
        for l in L: print(l)
        json.dump(dict(veredicto=v, lineas=L, d=d, shas=SHAS()), open(os.path.join(a.lee, 'RESUMEN.json'), 'w', encoding='utf-8'), indent=1, default=str)
        return
    if a.humo:
        ts = time.strftime('%Y%m%d_%H%M%S'); carpeta = os.path.join(DATOS, 'humo', f"ohno_humo_{ts}"); os.makedirs(carpeta, exist_ok=True)
        t0 = time.time(); print(f"[{time.strftime('%H:%M:%S')}] HUMO OHNO · r_rep {R_REP} · shas {SHAS()}", flush=True)
        for b in BRAZOS_SERIE:
            x = trabajo((HUMO['semilla'], b, HUMO['T'], HUMO['t_corte'], HUMO['r0_margen'], R_REP, carpeta, False))
            from collections import Counter
            cc = Counter(GD.texto(_tup(g)) for g in (x.get('final_banco_gr') or []))
            print(f"[{time.strftime('%H:%M:%S')}] {b}: {x['seg']} s · abortado {x['abortado']} · persiste {x.get('persiste')} (vivos {x.get('vivos_T')}, "
                  f"max {x.get('max_vivos')}) · r0 {x.get('r0_post')} · errores {x.get('g_nmut')} · r_paso {x.get('r_paso')} · max_nac_linaje "
                  f"{x.get('max_nac_linaje')}\n    banco final (top 4): {cc.most_common(4)}", flush=True)
        print(f"HUMO: {round(time.time() - t0, 1)} s (numeros sin valor) · {os.path.relpath(carpeta, RAIZ)}")
        return
    if a.calibra:   # un proceso: FIJO:filtra0 al T de la serie en el mundo de prueba
        carpeta = os.path.join(DATOS, f"calibra_rrep{a.rrep}"); os.makedirs(carpeta, exist_ok=True)
        print(f"[{time.strftime('%H:%M:%S')}] CALIBRA r_rep {a.rrep} · semillas {a.desde}-{a.desde + a.n - 1} · {SERIE} · shas {SHAS()}", flush=True)
        for s in range(a.desde, a.desde + a.n):
            x = trabajo((s, 'FIJO:filtra0', SERIE['T'], SERIE['t_corte'], SERIE['r0_margen'], a.rrep, carpeta, True))
            print(f"[{time.strftime('%H:%M:%S')}] s{s}: persiste {x.get('persiste')} vivos {x.get('vivos_T')} max {x.get('max_vivos')} r0 {x.get('r0_post')} "
                  f"(n {x.get('n_coh_post')}) t_ext {x.get('t_ext')} abort {x['abortado']} ({x['seg']} s)", flush=True)
        return
    if a.prueba_pool:
        carpeta = os.path.join(DATOS, 'ohno_prueba_pool'); os.makedirs(carpeta, exist_ok=True)
        jobs = [(s, b, PRUEBA['T'], PRUEBA['t_corte'], PRUEBA['r0_margen'], R_REP, carpeta, False)
                for s in range(PRUEBA['desde'], PRUEBA['desde'] + PRUEBA['n']) for b in BRAZOS_SERIE]
        _pool(jobs, a.pool, lambda s: print(f"[{time.strftime('%H:%M:%S')}] {s}", flush=True))
        print('PRUEBA DEL POOL: corre'); return
    d0 = VENTANAS[a.ventana]; etq = f"ohno_{a.ventana}_s{d0}-{d0 + N - 1}"; carpeta = os.path.join(DATOS, etq)
    if os.path.exists(carpeta) and not a.reanuda and glob.glob(os.path.join(carpeta, '*_s*.json')):
        raise SystemExit(f"OHNO: {carpeta} ya tiene resultados; --reanuda (no se pisa nada)")
    os.makedirs(carpeta, exist_ok=True)
    flog = open(os.path.join(carpeta, 'progreso.log'), 'a', encoding='utf-8')

    def log(s):
        s = f"[{time.strftime('%H:%M:%S')}] {s}"; print(s, flush=True); flog.write(s + '\n'); flog.flush()
    log(f"OHNO {etq} · r_rep {R_REP} · {SERIE} · {GRAM} · pool {a.pool} · shas {SHAS()}")
    jobs = [(s, b, SERIE['T'], SERIE['t_corte'], SERIE['r0_margen'], R_REP, carpeta, a.reanuda) for s in range(d0, d0 + N) for b in BRAZOS_SERIE]
    _pool(jobs, a.pool, log)
    R = [json.load(open(p, encoding='utf-8')) for p in sorted(glob.glob(os.path.join(carpeta, '*_s*.json')))]
    v, L, d = veredicto(R)
    for l in L: log(l)
    json.dump(dict(etiqueta=etq, veredicto=v, lineas=L, d=d, R_REP=R_REP, SERIE=SERIE, GRAM=GRAM, shas=SHAS()),
              open(os.path.join(carpeta, 'RESUMEN.json'), 'w', encoding='utf-8'), indent=1, default=str)
    flog.close()


if __name__ == '__main__':
    try:
        main()
    except BanderaMala as e:
        print(str(e), file=sys.stderr); sys.exit(2)
