"""corre_codigo.py — RUNNER del CODIGO GENETICO v0: ¿la cinta con lector, copia regulada y SOS se RECUPERA mejor cuando el mundo cambia?

MISION: llegar a la AGI por este camino.

Preregistro: PREREGISTRO_codigo.md (la letra esta AQUI, en veredicto(), y alli). Instrumento: motor_codigo.py (construye_codigo.py desde
motor_gramatica.py) + carros/FAMB_GRAM_ECO.py (copia byte a byte) + codigo_def.py (cinta, lector, copiador). Arnes: identidad_codigo.py.

Mundo w30 (el de ECO v2.1 y de la gramatica). Todos arrancan desde LO MAS EVOLUCIONADO: FIJO:filtra0 con las perillas de fabrica.
En t_cambio (DENTRO del vivero, ERR-140) el mundo INTERCAMBIA el valor de A y B (comida <-> veneno); el vivero (banco 200) sigue hasta
t_corte y despues nadie repone nada: la prueba final es vivir SOLO en el mundo nuevo.
Brazos:
  CODIGO          cinta compilada (CD.compila) + copia con errores regulada por la cinta (TASA) + SOS; el hijo copia al padre.
  PERILLAS        el genoma de hoy desde el mismo fenotipo: gramatica FIJA en filtra0 como punto de partida PERO con sus errores de copia
                  de hoy (campo 0.05, dup 0.02, del 0.02) + mutacion numerica de hoy (p 0.05, sigma 0.15, 18 genes).
  CODIGO_SIN_SOS  la misma cinta; la regla SOS no se lee (tasa por tramo fija).
  AZAR            CODIGO con donante 'azar' (todo cuerpo nuevo copia una entrada al azar del banco): deriva, sin seleccion.
  MUT0            la cinta sin errores de copia: nadie cambia de genoma (lo que cambie es aprendizaje dentro de la vida y transmision).
  QUIETO          (ERR-141, DESCRIPTIVO, fuera de la letra) CODIGO en el mundo que NO cambia: dice cuanto de la caida es el cambio y
                  cuanto es el corte (las medidas se toman en el mismo t_cambio nominal).

Uso (un proceso; la serie con Pool la lanza SOLO el coordinador):
  python experimentos/organelos/codigo/corre_codigo.py --humo
  python experimentos/organelos/codigo/corre_codigo.py --explora --bloque K --de N          # EXPLORATORIO, un proceso
  python experimentos/organelos/codigo/corre_codigo.py --lee <carpeta>
  python experimentos/organelos/codigo/corre_codigo.py --serie --ventana serie|replica --pool P [--reanuda]   # SOLO el coordinador
"""
import argparse, glob, hashlib, json, os, pickle, sys, time
import numpy as np

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(AQUI)))
for _d in (AQUI, os.path.join(RAIZ, 'experimentos', 'generaciones')):
    if _d not in sys.path: sys.path.insert(0, _d)
import motor_codigo as MC
import gramatica_def as GD
import codigo_def as CD

CARRO = 'FAMB_GRAM_ECO'
MUNDO = dict(nombre='w30', esc=30, n0=30, tope=3000)
BASE = dict(banco=200, sigma=0.15, p_mut=0.05, cada_gen=2000, muestra=500, ckpt_cada=10000)
GRAM = dict(p_campo=0.05, p_dup=0.02, p_del=0.02, tope=4)
ALFABETO = GD.ALFABETO_TODO   # con 'olvidar': el mundo cambia (en la gramatica se quito por inerte en un mundo QUIETO)
MUTABLES = tuple(g for g in MC.NOMBRES if g not in ('ensena', 'filtra0'))
CAMBIO = ('A', 'B')           # comida <-> veneno (VAL_VIVO): el cambio minimo que el motor permite, un intercambio de dos letras
CINTA0 = CD.compila()         # desde lo MAS EVOLUCIONADO: FIJO:filtra0 en G0
BRAZOS_LETRA = ('CODIGO', 'PERILLAS', 'CODIGO_SIN_SOS', 'AZAR', 'MUT0')
BRAZOS = BRAZOS_LETRA + ('QUIETO',)   # ERR-141: QUIETO es descriptivo
TL = dict(T=80000, t_cambio=15000, t_corte=40000, r0_margen=10000)          # la SERIE (reservada)
TL_EXP = dict(T=40000, t_cambio=10000, t_corte=25000, r0_margen=5000)        # EXPLORATORIO (T corto)
TL_HUMO = dict(T=8000, t_cambio=3000, t_corte=5000, r0_margen=1000)
VENTANAS = {'serie': 27011, 'replica': 27031}
N = 20
SEM_EXP = (27901, 27902, 27903)   # practica (EXPLORATORIO)
SEM_HUMO = 27001
UMBRAL_REC = 0.8                  # recuperado: los NACIMIENTOS por ventana de 2000 pasos vuelven a >= 0.8 x los de antes del cambio
W_NAC = 2000
DATOS = os.path.join(AQUI, 'datos')


class BanderaMala(SystemExit):
    pass


def eco_de(brazo, t_corte, t_cambio, **extra):
    base = dict(refunda=1, t_corte=t_corte, sigma=BASE['sigma'], banco=BASE['banco'], n_sombra=0, cada_gen=BASE['cada_gen'],
                mutables=MUTABLES, g_tope=GRAM['tope'], g_alfabeto=ALFABETO,
                cambio=(None if (t_cambio is None or brazo == 'QUIETO') else (t_cambio,) + CAMBIO))
    n0 = MUNDO['n0']
    if brazo == 'PERILLAS':
        base.update(gramatica=[GD.FILTRA0] * n0, p_mut=BASE['p_mut'], donante='padre',
                    g_pcampo=GRAM['p_campo'], g_pdup=GRAM['p_dup'], g_pdel=GRAM['p_del'])
    elif brazo in ('CODIGO', 'CODIGO_SIN_SOS', 'AZAR', 'MUT0', 'QUIETO'):
        base.update(codigo=[CINTA0] * n0, p_mut=0.0, donante=('azar' if brazo == 'AZAR' else 'padre'),
                    c_on=(brazo != 'MUT0'), c_sos=(brazo in ('CODIGO', 'AZAR', 'QUIETO')))
    else: raise SystemExit(f"CODIGO: brazo desconocido {brazo}")
    base.update(extra)
    return base


def recuperacion(tn_nac, t_cambio, t_fin):
    """ERR-140; ERR-141: t_fin = t_CORTE (la recuperacion se mide DENTRO del vivero; despues del corte la demografia es otra y su
    minimo se comia la medida). (B_pre, t_rec, minimo). tn_nac = tiempos de nacimiento (partos reales, no fundadores). B_pre = nacimientos medios por
    ventana de W_NAC pasos en [t_cambio - 3 W_NAC, t_cambio). Tras el cambio, ventanas [t_cambio + i W_NAC, ...) hasta t_fin; t_rec = pasos
    desde t_cambio hasta el INICIO de la primera ventana, desde la del minimo, con nacimientos >= UMBRAL_REC x B_pre (0 si nunca cayo por
    debajo; None si no vuelve antes de t_fin: censurado)."""
    tn = np.array(tn_nac, float)
    pre = [((tn >= a) & (tn < a + W_NAC)).sum() for a in range(t_cambio - 3 * W_NAC, t_cambio, W_NAC) if a >= 0]
    if not pre or np.mean(pre) <= 0: return None, None, None
    Bp = float(np.mean(pre))
    post = [(a, int(((tn >= a) & (tn < a + W_NAC)).sum())) for a in range(t_cambio, t_fin - W_NAC + 1, W_NAC)]
    if not post: return Bp, None, None
    imin = int(np.argmin([c for _, c in post])); mn = post[imin][1]
    if mn >= UMBRAL_REC * Bp: return Bp, 0, mn
    for a, c in post[imin:]:
        if c >= UMBRAL_REC * Bp: return Bp, int(a - t_cambio), mn
    return Bp, None, mn


def relee_trec(x):
    """ERR-141: JSON escritos ANTES del arreglo (la exploratoria) -> t_rec se recalcula desde ventanas_r0 (nacidos por ventana de W_NAC desde
    t = 0), igual que recuperacion(..., t_corte). Solo si t_cambio es multiplo de W_NAC (ventanas alineadas); si no, se deja."""
    tl = x.get('tl') or {}; V = x.get('ventanas_r0')
    if x.get('abortado') or not V or tl.get('t_cambio', 1) % W_NAC or x.get('trec_err141'): return x
    n = {v[0]: v[2] for v in V}; tc, tk = tl['t_cambio'], tl['t_corte']
    pre = [n.get(a, 0) for a in range(tc - 3 * W_NAC, tc, W_NAC) if a >= 0]
    post = [(a, n.get(a, 0)) for a in range(tc, tk - W_NAC + 1, W_NAC)]
    if not pre or np.mean(pre) <= 0 or not post: return x
    Bp = float(np.mean(pre)); imin = int(np.argmin([c for _, c in post])); mn = post[imin][1]
    tr = 0 if mn >= UMBRAL_REC * Bp else next((a - tc for a, c in post[imin:] if c >= UMBRAL_REC * Bp), None)
    x.update(B_pre=Bp, t_rec=tr, minimo_post=mn, trec_err141=1)
    return x


def trabajo(args):
    """UNA corrida (semilla, brazo). Escribe su JSON. Nunca lanza (nube-9)."""
    seed, brazo, tl, carpeta, reanuda = args
    T, t_corte, t_cambio, marg = tl['T'], tl['t_corte'], tl['t_cambio'], tl['r0_margen']
    fin = os.path.join(carpeta, f"{brazo}_s{seed}.json")
    if reanuda and os.path.exists(fin): return json.load(open(fin, encoding='utf-8'))
    ck = os.path.join(carpeta, 'ckpt', f"{brazo}_s{seed}.pkl"); os.makedirs(os.path.dirname(ck), exist_ok=True)
    filas = []

    def cb(li, row, g): filas.append([li] + row)

    def guarda(t, blob):
        tmp = ck + '.tmp'
        with open(tmp, 'wb') as f: pickle.dump(dict(t=t, blob=blob, filas=filas), f, protocol=pickle.HIGHEST_PROTOCOL)
        os.replace(tmp, ck)
    estado = None
    if reanuda and os.path.exists(ck):
        d = pickle.load(open(ck, 'rb')); estado = d['blob']; filas[:] = d['filas']
    t0 = time.time(); abortado = None; r = None
    try:
        r = MC.run_solapadas(seed, [CARRO] * MUNDO['n0'], T=T, diag=0, mundo_n=MUNDO['esc'], tope_cuerpos=MUNDO['tope'], muestra=BASE['muestra'],
                             eco=eco_de(brazo, t_corte, t_cambio, ckpt_cada=(BASE['ckpt_cada'] if T >= 2 * BASE['ckpt_cada'] else 0),
                                        ckpt_fn=guarda, estado=estado, ind_cb=cb))
    except SystemExit as e: abortado = f"SystemExit: {e}"
    except Exception as e: abortado = f"{type(e).__name__}: {e}"
    res = dict(seed=seed, brazo=brazo, tl=tl, seg=round(time.time() - t0, 1), abortado=abortado, mundo=MUNDO, cambio=CAMBIO,
               cinta0=[list(x) for x in CINTA0])
    if r is not None:
        E = r['eco']; P = r['pista']; C = r.get('codigo', {}); G = r['gram']
        nf = [f for f in filas if not f[7]]   # nacidos (no fundadores): [li, k, gen, padre, tn, tm, hijos, fund, causa, vd]
        def r0(a, b):
            x = [f[6] for f in nf if a <= f[4] < b]; return (round(float(np.mean(x)), 4) if x else None), len(x)
        W = W_NAC; ventanas = []
        for a in range(0, T - marg, W): ventanas.append([a] + list(r0(a, min(a + W, T - marg))))
        Np, trec, mn = recuperacion([f[4] for f in nf], t_cambio, t_corte)   # ERR-141
        cn = C.get('cod_nac', [])
        def resumen_nac(xs):
            if not xs: return None
            a = np.array([[x[4], x[5], x[6], x[7]] for x in xs], float)
            fm = [x[12] for x in xs if x[12] >= 0]
            return dict(n=len(xs), errores_media=round(float(a[:, 0].mean()), 3), sos_frac=round(float(a[:, 1].mean()), 4),
                        fen_cambia=round(float(a[:, 2].mean()), 4), largo_media=round(float(a[:, 3].mean()), 2),
                        largo_max=int(a[:, 3].max()), frac_mal_media=(round(float(np.mean(fm)), 4) if fm else None),
                        frac_mal_p90=(round(float(np.percentile(fm, 90)), 4) if fm else None))
        # robustez (descriptiva): hijos nacidos con >= 1 error de copia; fenotipo igual (NEUTRA) / cambia y deja hijos (SUAVE) / cambia y 0 hijos
        hij = {(f[0], f[1]): f[6] for f in nf}
        rob = None
        con_err = [x for x in cn if x[3] >= 0 and x[4] > 0 and x[0] < T - marg]
        if con_err:
            neu = sum(1 for x in con_err if not x[6]); ch = [x for x in con_err if x[6]]
            suave = sum(1 for x in ch if hij.get((x[1], x[2]), 0) > 0)
            base0 = [hij.get((x[1], x[2]), 0) > 0 for x in cn if x[3] >= 0 and x[4] == 0 and x[0] < T - marg]
            rob = dict(n=len(con_err), neutra=round(neu / len(con_err), 4), cambia_con_hijos=round(suave / len(con_err), 4),
                       cambia_sin_hijos=round((len(ch) - suave) / len(con_err), 4),
                       sin_error_con_hijos=(round(float(np.mean(base0)), 4) if base0 else None))
        res.update(trec_err141=1, t_ext=E['t_ext'], persiste=int(E['t_ext'] is None and len(E['vivos_final']) > 0), vivos_T=len(E['vivos_final']),
                   bloqueados=P['bloqueados'], max_vivos=P['max_vivos'], n_nac=E['n_nac'], n_refund=E['n_refund'],
                   r0_pre_cambio=r0(t_cambio - 3 * W_NAC, t_cambio)[0], r0_cambio_corte=r0(t_cambio, t_corte)[0],
                   r0_final=r0(t_corte, T - marg)[0], n_final=r0(t_corte, T - marg)[1],
                   ventanas_r0=ventanas, B_pre=Np, t_rec=trec, minimo_post=mn, tam_total=P['tam_total'],
                   max_nac_linaje=G['max_nac_linaje'], mord_signo=C.get('mord_signo'),
                   nac_pre=resumen_nac([x for x in cn if x[3] >= 0 and x[0] < t_cambio]),
                   nac_post=resumen_nac([x for x in cn if x[3] >= 0 and t_cambio <= x[0] < t_cambio + 5000]),
                   nac_tarde=resumen_nac([x for x in cn if x[3] >= 0 and x[0] >= t_cambio + 5000]),
                   robustez=rob, vivos_gr=[v[:4] + [[list(s) for s in v[4]]] for v in G['vivos_gr']][:80],
                   cintas_vivos=C.get('cintas_vivos'),
                   genoma_vivos_T=[v[4:22] for v in E['vivos_final']][:80])
    tmp = fin + '.tmp'
    with open(tmp, 'w', encoding='utf-8') as f: json.dump(res, f)
    os.replace(tmp, fin)
    if os.path.exists(ck) and abortado is None: os.remove(ck)
    return res


# ================================================================================ LA LETRA (PREREGISTRO_codigo.md §6)
def veredicto(R, n_esperado=N):
    L = []
    by = {b: {x['seed']: x for x in R if x['brazo'] == b} for b in BRAZOS}
    completo = all(len(by[b]) == n_esperado for b in BRAZOS_LETRA)   # QUIETO es descriptivo (ERR-141)
    abortados = [(x['brazo'], x['seed'], x['abortado']) for x in R if x.get('abortado')]
    bloq = sum(x.get('bloqueados', 0) for x in R if not x.get('abortado'))
    ok = lambda x: x is not None and not x.get('abortado')
    pers = {b: sum(int(x.get('persiste', 0)) for x in by[b].values() if ok(x)) for b in BRAZOS}
    def trec(x):   # ERR-141: censurado = t_corte - t_cambio + 1 si no se recupera dentro del vivero
        return x['t_rec'] if x.get('t_rec') is not None else (x['tl']['t_corte'] - x['tl']['t_cambio'] + 1)
    def r0f(x): return x['r0_final'] if x.get('r0_final') is not None else 0.0
    med = lambda b, f: (round(float(np.median([f(x) for x in by[b].values() if ok(x)])), 4) if any(ok(x) for x in by[b].values()) else None)
    def pareado(a, b, f, mayor=True):
        w = 0; n_ = 0
        for s in by[a]:
            if s in by[b] and ok(by[a][s]) and ok(by[b][s]):
                n_ += 1; va, vb = f(by[a][s]), f(by[b][s]); w += int(va > vb if mayor else va < vb)
        return w, n_
    # P1: CODIGO se recupera MAS RAPIDO que PERILLAS (t_rec menor, pareado por semilla) en >= 14/20 Y persiste en T en al menos tantas
    p1 = pareado('CODIGO', 'PERILLAS', trec, mayor=False)
    P1 = p1[0] >= 14 and pers['CODIGO'] >= pers['PERILLAS']
    # P2: CODIGO llega MAS LEJOS: R0 final mayor que PERILLAS en >= 14/20
    p2 = pareado('CODIGO', 'PERILLAS', r0f); P2 = p2[0] >= 14
    # P3 (la SOS sirve): CODIGO mejor que CODIGO_SIN_SOS en R0 final >= 13/20 Y la SOS se PRENDE tras el cambio (fraccion de partos con SOS
    # en los 5000 pasos tras el cambio >= 2 x la de antes, en >= 15/20 semillas de CODIGO)
    p3 = pareado('CODIGO', 'CODIGO_SIN_SOS', r0f)
    def prende(x):
        a = (x.get('nac_pre') or {}).get('sos_frac'); b = (x.get('nac_post') or {}).get('sos_frac')
        return a is not None and b is not None and b >= 2 * a and b > 0
    sos_on = sum(int(prende(x)) for x in by['CODIGO'].values() if ok(x))
    P3 = p3[0] >= 13 and sos_on >= 15
    # guardias (controles que pueden fallar): la seleccion importa (CODIGO > AZAR en R0 final >= 14/20); la variacion importa (CODIGO > MUT0
    # en R0 final >= 14/20). Si falla la primera, lo que se ve no es seleccion; si falla la segunda, no es la variacion genetica.
    gA = pareado('CODIGO', 'AZAR', r0f); gM = pareado('CODIGO', 'MUT0', r0f)
    GA = gA[0] >= 14; GM = gM[0] >= 14
    L.append(f"persisten en T {pers}")
    L.append(f"t_rec mediana (censurado = t_corte - t_cambio + 1) " + str({b: med(b, trec) for b in BRAZOS}))
    L.append(f"R0 final mediana (extinto = 0) " + str({b: med(b, r0f) for b in BRAZOS}))
    L.append(f"P1 CODIGO se recupera antes que PERILLAS {p1[0]}/{p1[1]} (y persiste {pers['CODIGO']} vs {pers['PERILLAS']}) -> {P1}")
    L.append(f"P2 CODIGO R0 final > PERILLAS {p2[0]}/{p2[1]} -> {P2}")
    L.append(f"P3 CODIGO R0 final > SIN_SOS {p3[0]}/{p3[1]}; la SOS se prende tras el cambio en {sos_on} semillas -> {P3}")
    L.append(f"guardia seleccion CODIGO > AZAR {gA[0]}/{gA[1]} -> {GA} · guardia variacion CODIGO > MUT0 {gM[0]}/{gM[1]} -> {GM}")
    for b in BRAZOS:
        rb = [x['robustez'] for x in by[b].values() if ok(x) and x.get('robustez')]
        if rb: L.append(f"  robustez {b}: neutra {np.median([z['neutra'] for z in rb]):.3f} · cambia con hijos {np.median([z['cambia_con_hijos'] for z in rb]):.3f} · "
                        f"cambia sin hijos {np.median([z['cambia_sin_hijos'] for z in rb]):.3f} · (sin error, con hijos {np.median([z['sin_error_con_hijos'] or 0 for z in rb]):.3f})")
    if not completo: v = 'NO EVALUABLE (ventana incompleta)'
    elif abortados: v = f'NO EVALUABLE (abortadas: {abortados[:3]})'
    elif bloq > 0: v = f'NO EVALUABLE (tope de cuerpos: bloqueados = {bloq})'
    elif (P1 or P2) and GA and GM and P3: v = 'FUNCIONA — EL CODIGO (cinta + copia regulada + SOS) ES MAS EVOLUCIONABLE que las perillas, y la SOS aporta'
    elif (P1 or P2) and GA and GM: v = 'FUNCIONA — EL CODIGO ES MAS EVOLUCIONABLE que las perillas (la SOS no se demuestra)'
    elif (P1 or P2) and not (GA and GM): v = 'HAY ALGO MODESTO (el codigo gana a las perillas pero una guardia cae: no se atribuye a seleccion/variacion)'
    elif P3 or (GA and GM): v = 'HAY ALGO MODESTO (el codigo evoluciona o la SOS sirve, pero no le gana a las perillas)'
    else: v = 'NO'
    L.append(f"VEREDICTO CODIGO v0 POR LA LETRA (una ventana; el bloque exige serie + replica con el mismo veredicto): {v}")
    return v, L


def SHAS():
    f = lambda p: hashlib.sha256(open(os.path.join(AQUI, p), 'rb').read()).hexdigest()[:16]
    return {p: f(p) for p in ('corre_codigo.py', 'motor_codigo.py', 'codigo_def.py', 'construye_codigo.py', 'carros/FAMB_GRAM_ECO.py',
                              'gramatica_def.py', 'PREREGISTRO_codigo.md') if os.path.exists(os.path.join(AQUI, p))}


def resumen_linea(x):
    return (f"{x['brazo']:<15} s{x['seed']}: {x['seg']} s · abort {x['abortado']} · persiste {x.get('persiste')} (vivos {x.get('vivos_T')}, t_ext {x.get('t_ext')}) · "
            f"nac/ventana antes {None if x.get('B_pre') is None else round(x['B_pre'], 1)} min {x.get('minimo_post')} t_rec {x.get('t_rec')} · "
            f"R0 antes {x.get('r0_pre_cambio')} cambio->corte {x.get('r0_cambio_corte')} FINAL solo {x.get('r0_final')} (n {x.get('n_final')}) · "
            f"nac pre {x.get('nac_pre')} · post {x.get('nac_post')} · mord {x.get('mord_signo')}")


def parsea(argv):
    ap = argparse.ArgumentParser(allow_abbrev=False, add_help=False)
    ap.add_argument('--humo', action='store_true'); ap.add_argument('--explora', action='store_true'); ap.add_argument('--serie', action='store_true')
    ap.add_argument('--lee', default=None); ap.add_argument('--bloque', type=int); ap.add_argument('--de', type=int)
    ap.add_argument('--ventana', default=None); ap.add_argument('--pool', type=int); ap.add_argument('--reanuda', action='store_true')
    try:
        a, resto = ap.parse_known_args(argv)
    except SystemExit:
        raise BanderaMala('CODIGO: banderas mal formadas')
    if resto: raise BanderaMala(f"CODIGO: banderas desconocidas {resto}")
    if any(x.startswith('--') and '=' in x for x in argv): raise BanderaMala('CODIGO: sin la forma --bandera=valor')
    flags = [x for x in argv if x.startswith('--')]
    if len(flags) != len(set(flags)): raise BanderaMala('CODIGO: bandera repetida')
    if int(a.humo) + int(a.explora) + int(a.serie) + int(a.lee is not None) != 1: raise BanderaMala('CODIGO: exactamente uno de --humo, --explora, --serie, --lee')
    if a.humo and (a.ventana or a.pool or a.reanuda or a.bloque is not None or a.de is not None): raise BanderaMala('CODIGO: --humo va solo')
    if a.explora and (a.bloque is None or a.de is None or not 0 <= a.bloque < a.de or a.pool or a.ventana): raise BanderaMala('CODIGO: --explora --bloque K --de N')
    if a.serie and (a.ventana not in VENTANAS or a.pool is None or not 1 <= a.pool <= 6): raise BanderaMala('CODIGO: --serie --ventana serie|replica --pool 1..6')
    return a


def main(argv=None):
    a = parsea(sys.argv[1:] if argv is None else argv)
    if a.lee is not None:
        R = [json.load(open(p, encoding='utf-8')) for p in sorted(glob.glob(os.path.join(a.lee, '*_s*.json')))]
        for x in R: relee_trec(x)
        n_ = len(set(x['seed'] for x in R))
        v, L = veredicto(R, n_esperado=n_)
        for l in L: print(l)
        return
    if a.humo:
        ts = time.strftime('%Y%m%d_%H%M%S'); carpeta = os.path.join(DATOS, 'humo', f"codigo_humo_{ts}"); os.makedirs(carpeta, exist_ok=True)
        t0 = time.time(); print(f"[{time.strftime('%H:%M:%S')}] HUMO CODIGO {TL_HUMO} · shas {SHAS()}", flush=True)
        for b in BRAZOS:
            x = trabajo((SEM_HUMO, b, TL_HUMO, carpeta, False)); print(f"[{time.strftime('%H:%M:%S')}] " + resumen_linea(x), flush=True)
        R = [json.load(open(p, encoding='utf-8')) for p in sorted(glob.glob(os.path.join(carpeta, '*_s*.json')))]
        v, L = veredicto(R, n_esperado=1)
        for l in L: print('   ' + l)
        json.dump(dict(humo=True, tl=TL_HUMO, seg=round(time.time() - t0, 1), shas=SHAS(), veredicto_sin_valor=v, lineas=L),
                  open(os.path.join(carpeta, 'HUMO.json'), 'w', encoding='utf-8'), indent=1)
        print(f"HUMO: {round(time.time() - t0, 1)} s (numeros sin valor) · {os.path.relpath(carpeta, RAIZ)}")
        return
    if a.explora:
        carpeta = os.path.join(DATOS, f"EXPLORATORIO_s{SEM_EXP[0]}-{SEM_EXP[-1]}_T{TL_EXP['T']}"); os.makedirs(carpeta, exist_ok=True)
        jobs = [(s, b) for s in SEM_EXP for b in BRAZOS][a.bloque::a.de]
        flog = open(os.path.join(carpeta, f"progreso_bloque{a.bloque}de{a.de}.log"), 'a', encoding='utf-8')
        def log(s):
            s = f"[{time.strftime('%H:%M:%S')}] {s}"; print(s, flush=True); flog.write(s + '\n'); flog.flush()
        log(f"EXPLORATORIO (numeros vistos; no es serie) bloque {a.bloque}/{a.de}: {len(jobs)} corridas · {TL_EXP} · shas {SHAS()}")
        for s, b in jobs:
            x = trabajo((s, b, TL_EXP, carpeta, True)); log(resumen_linea(x))
        flog.close()
        return
    # --serie (SOLO el coordinador; Pool)
    d0 = VENTANAS[a.ventana]; semillas = range(d0, d0 + N); etq = f"codigo_{a.ventana}_s{d0}-{d0 + N - 1}"
    carpeta = os.path.join(DATOS, etq)
    if os.path.exists(carpeta) and not a.reanuda and glob.glob(os.path.join(carpeta, '*_s*.json')):
        raise SystemExit(f"CODIGO: {carpeta} ya tiene resultados; --reanuda")
    os.makedirs(carpeta, exist_ok=True)
    flog = open(os.path.join(carpeta, 'progreso.log'), 'a', encoding='utf-8')
    def log(s):
        s = f"[{time.strftime('%H:%M:%S')}] {s}"; print(s, flush=True); flog.write(s + '\n'); flog.flush()
    log(f"CODIGO {etq} · {TL} · {BASE} · {GRAM} · pool {a.pool} · shas {SHAS()}")
    jobs = [(s, b, TL, carpeta, a.reanuda) for s in semillas for b in BRAZOS]
    t0 = time.time()
    from multiprocessing import Pool
    with Pool(a.pool) as pool:
        for k, x in enumerate(pool.imap_unordered(trabajo, jobs), 1):
            log(f"[{k}/{len(jobs)}] " + resumen_linea(x)[:400])
    R = [json.load(open(p, encoding='utf-8')) for p in sorted(glob.glob(os.path.join(carpeta, '*_s*.json')))]
    v, L = veredicto(R)
    for l in L: log(l)
    json.dump(dict(etiqueta=etq, veredicto=v, lineas=L, seg=round(time.time() - t0), TL=TL, shas=SHAS()),
              open(os.path.join(carpeta, 'RESUMEN.json'), 'w', encoding='utf-8'), indent=1, default=str)
    flog.close()


if __name__ == '__main__':
    try:
        main()
    except BanderaMala as e:
        print(str(e), file=sys.stderr); sys.exit(2)
