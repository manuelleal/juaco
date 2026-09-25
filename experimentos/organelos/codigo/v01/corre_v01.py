"""corre_v01.py — RUNNER del CODIGO GENETICO v0.1: ¿la CINTA evoluciona mejor que las PERILLAS cuando se IGUALA la carga mutacional?

MISION: llegar a la AGI por este camino.

Preregistro: PREREGISTRO_v01.md (la letra esta AQUI, en veredicto(), y alli). Instrumento: motor_v01.py (construye_v01.py desde
exploracion_fable/motor_fable.py, sin tocarlo) + fable_mundos.py (IMPORTADO de exploracion_fable/) + codigo_def.py y carros/ de codigo/.
Arnes: identidad_v01.py.

Mundos (fable_mundos.catalogo(t_cambio)): 'quieto' (no cambia: la BASE) y 'onda8k' (estacional coseno, periodo 8000, A<->B y vuelve).
Brazos (w30, banco 200, sin sombras, vivero hasta t_corte y despues SOLOS):
  CODIGO_SIN_SOS    CINTA0 (v0) + copia con errores por tramo; la SOS no se lee.   <- el brazo principal (el mejor del Fable)
  CODIGO            igual, con la SOS de la cinta.
  PERILLAS          el genoma de hoy desde filtra0 + G0: numerica p 0.05 sigma 0.15 (18 genes) + gramatica (campo 0.05, dup 0.02, del 0.02).
  PERILLAS_ROBUSTA  PERILLAS con TODAS sus tasas x LAMBDA_ROB, calibrado ANTES (--calibra) para que la fraccion de hijos con fenotipo
                    IDENTICO al del donante sea la del CODIGO_SIN_SOS (la carga mutacional igualada en fenotipos, no en errores).
  MUT0              la cinta sin errores de copia.
  AZAR              CODIGO_SIN_SOS con donante al azar del banco (deriva; ERR v0.1: en v0 AZAR llevaba SOS; aqui sigue al brazo principal).

Uso (un proceso salvo --serie; la serie la lanza SOLO el coordinador):
  python experimentos/organelos/codigo/v01/corre_v01.py --calibra                 # fase 1: fraccion identica del CODIGO_SIN_SOS (29901-29903)
  python experimentos/organelos/codigo/v01/corre_v01.py --calibra_rob --lam X     # fase 2: verifica PERILLAS_ROBUSTA con lambda X (29904-29906)
  python experimentos/organelos/codigo/v01/corre_v01.py --humo
  python experimentos/organelos/codigo/v01/corre_v01.py --serie --ventana serie|replica --pool 6 [--reanuda] [--con_golpe]
  python experimentos/organelos/codigo/v01/corre_v01.py --lee <carpeta>
"""
import argparse, glob, hashlib, json, math, os, pickle, sys, time
import numpy as np

AQUI = os.path.dirname(os.path.abspath(__file__))
COD = os.path.dirname(AQUI)
FAB = os.path.join(COD, 'exploracion_fable')
RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(COD)))
for _d in (AQUI, COD, FAB, os.path.join(RAIZ, 'experimentos', 'generaciones')):
    if _d not in sys.path: sys.path.insert(0, _d)
import motor_v01 as MV
import fable_mundos as FB
import gramatica_def as GD
import codigo_def as CD

CARRO = 'FAMB_GRAM_ECO'
MUNDO = dict(nombre='w30', esc=30, n0=30, tope=3000)
BASE = dict(banco=200, sigma=0.15, p_mut=0.05, cada_gen=2000, muestra=500, ckpt_cada=10000)
GRAM = dict(p_campo=0.05, p_dup=0.02, p_del=0.02, tope=4)
ALFABETO = GD.ALFABETO_TODO
MUTABLES = tuple(g for g in MV.NOMBRES if g not in ('ensena', 'filtra0'))
CINTA0 = CD.compila()
BRAZOS = ('CODIGO_SIN_SOS', 'PERILLAS', 'PERILLAS_ROBUSTA', 'MUT0', 'AZAR', 'CODIGO')
BRAZOS_SERIE = BRAZOS[:5]                           # CODIGO (con SOS) es OPCIONAL (--con_sos): no cabe en 45 min (PREREGISTRO_v01 §5)
BRAZOS_MIN = BRAZOS[:4]                             # la letra minima; en la serie van PRIMERO, AZAR despues (si el tiempo se acaba, cae AZAR)
MUNDOS = ('quieto', 'onda8k')
MUNDO_REF = 'golpe'                                 # referencia OPCIONAL (--con_golpe), fuera de la letra
TL = dict(T=24000, t_cambio=0, t_corte=16000, r0_margen=2000)   # SERIE (<= 45 min con Pool 6): la onda corre desde t = 0, 2 periodos
TL_CAL = dict(T=36000, t_cambio=8000, t_corte=24000, r0_margen=4000)   # = TL 'corto' del Fable: la CALIBRACION (ya hecha) se corrio con este
TL_HUMO = TL   # el humo corre a la TL de la serie (1 semilla): mide el COSTO real y la fraccion identica
LAMBDA_ROB = 0.292   # CALIBRADO (PREREGISTRO_v01 §3): objetivo 0.715 (CODIGO_SIN_SOS, 29901-29903); ROBUSTA midio 0.721 (29904-29906)
VENTANAS = {'serie': 29011, 'replica': 29031}
N = 20
SEM_CAL1 = (29901, 29902, 29903); SEM_CAL2 = (29904, 29905, 29906); SEM_HUMO = 29001
W_NAC = 2000
DATOS = os.path.join(AQUI, 'datos')


class BanderaMala(SystemExit):
    pass


def eco_de(brazo, mundo, tl, lam=None, **extra):
    spec = dict(FB.catalogo(tl['t_cambio'])[mundo])   # copia por corrida
    base = dict(refunda=1, t_corte=tl['t_corte'], sigma=BASE['sigma'], banco=BASE['banco'], n_sombra=0, cada_gen=BASE['cada_gen'],
                mutables=MUTABLES, g_tope=GRAM['tope'], g_alfabeto=ALFABETO, cambio=spec)
    n0 = MUNDO['n0']
    if brazo in ('PERILLAS', 'PERILLAS_ROBUSTA'):
        f = 1.0 if brazo == 'PERILLAS' else float(LAMBDA_ROB if lam is None else lam)
        base.update(gramatica=[GD.FILTRA0] * n0, p_mut=BASE['p_mut'] * f, donante='padre',
                    g_pcampo=GRAM['p_campo'] * f, g_pdup=GRAM['p_dup'] * f, g_pdel=GRAM['p_del'] * f)
    elif brazo in ('CODIGO', 'CODIGO_SIN_SOS', 'AZAR', 'MUT0'):
        base.update(codigo=[CINTA0] * n0, p_mut=0.0, donante=('azar' if brazo == 'AZAR' else 'padre'),
                    c_on=(brazo != 'MUT0'), c_sos=(brazo == 'CODIGO'))
    else: raise SystemExit(f"V01: brazo desconocido {brazo}")
    base.update(extra)
    return base


def f_ident_perillas(lam):
    """Fraccion ANALITICA de hijos de PERILLAS con fenotipo identico (sin recortes por rango): nadie de los 18 genes muta y la gramatica
    de UN slot no cambia (ni duplicacion, ni borrado, ni ninguno de sus 4 campos)."""
    p = BASE['p_mut'] * lam
    return (1 - p) ** 18 * (1 - GRAM['p_dup'] * lam) * (1 - GRAM['p_del'] * lam) * (1 - GRAM['p_campo'] * lam) ** 4


def lam_para(f_obj):
    lo, hi = 0.0, 1.0
    for _ in range(60):
        m = (lo + hi) / 2
        if f_ident_perillas(m) > f_obj: lo = m
        else: hi = m
    return (lo + hi) / 2


def trabajo(args):
    """UNA corrida (semilla, brazo, mundo). Escribe su JSON. Nunca lanza (nube-9)."""
    seed, brazo, mundo, tl, carpeta, reanuda, lam = args
    T, t_corte, t_cambio, marg = tl['T'], tl['t_corte'], tl['t_cambio'], tl['r0_margen']
    fin = os.path.join(carpeta, f"{mundo}__{brazo}_s{seed}.json")
    if reanuda and os.path.exists(fin): return json.load(open(fin, encoding='utf-8'))
    filas = []
    def cb(li, row, g): filas.append([li] + row)
    t0 = time.time(); abortado = None; r = None
    try:
        r = MV.run_solapadas(seed, [CARRO] * MUNDO['n0'], T=T, diag=0, mundo_n=MUNDO['esc'], tope_cuerpos=MUNDO['tope'], muestra=BASE['muestra'],
                             eco=eco_de(brazo, mundo, tl, lam=lam, ind_cb=cb))
    except SystemExit as e: abortado = f"SystemExit: {e}"
    except Exception as e: abortado = f"{type(e).__name__}: {e}"
    res = dict(seed=seed, brazo=brazo, mundo=mundo, spec=FB.catalogo(t_cambio)[mundo], tl=tl, seg=round(time.time() - t0, 1), abortado=abortado,
               lam=(None if brazo != 'PERILLAS_ROBUSTA' else float(LAMBDA_ROB if lam is None else lam)))
    if r is not None:
        E = r['eco']; P = r['pista']; C = r.get('codigo', {}); G = r['gram']
        nf = [f for f in filas if not f[7]]   # [li, k, gen, padre, tn, tm, hijos, fund, causa, vd]
        tn = np.array([f[4] for f in nf], float)
        cuenta = lambda a, b: int(((tn >= a) & (tn < b)).sum())
        vent = [[a, cuenta(a, a + W_NAC)] for a in range(0, T, W_NAC)]
        pre = [cuenta(a, a + W_NAC) for a in range(max(0, t_cambio - 3 * W_NAC), max(t_cambio, 3 * W_NAC), W_NAC)]   # t_cambio 0: las 3 primeras ventanas
        post = [cuenta(a, a + W_NAC) for a in range(t_cambio, t_corte, W_NAC)]
        solo = [f for f in nf if t_corte <= f[4] < T - marg]
        Bp = float(np.mean(pre)) if pre else 0.0
        # fenotipo identico al del donante (PARTOS, antes del corte: donde esta la carga que se calibra)
        cn = [x for x in C.get('cod_nac', []) if x[3] >= 0]; pn = C.get('per_nac', [])
        if cn: ch = [x[6] for x in cn if x[0] < t_corte]; ident = (1 - float(np.mean(ch))) if ch else None; n_id = len(ch)
        elif pn: ch = [x[4] for x in pn if x[0] < t_corte]; ident = (1 - float(np.mean(ch))) if ch else None; n_id = len(ch)
        else: ident = None; n_id = 0
        def sosf(a, b):
            xs = [x[5] for x in cn if a <= x[0] < b]; return round(float(np.mean(xs)), 4) if xs else None
        res.update(persiste=int(E['t_ext'] is None and len(E['vivos_final']) > 0), vivos_T=len(E['vivos_final']), t_ext=E['t_ext'],
                   bloqueados=P['bloqueados'], max_vivos=P['max_vivos'], n_nac=E['n_nac'], n_refund=E['n_refund'],
                   nac_solo=len(solo), r0_final=(round(float(np.mean([f[6] for f in solo])), 4) if solo else 0.0),
                   B_pre=round(Bp, 2), nac_post_rel=(round(float(np.mean(post)) / Bp, 4) if Bp > 0 and post else None), ventanas=vent,
                   ident=(None if ident is None else round(ident, 4)), n_ident=n_id,
                   errores_copia=(round(float(np.mean([x[4] for x in cn if x[0] < t_corte])), 4) if cn else None),
                   sos_pre=sosf(0, t_cambio), sos_post=sosf(t_cambio, t_corte),
                   largo_corte=(round(float(np.mean([len(c) for c in C['banco_corte']])), 2) if C.get('banco_corte') else None),
                   banco_corte_cintas=C.get('banco_corte'),
                   banco_corte_gr=([[list(s) for s in g] for g in (G.get('corte') or {}).get('banco_gr', [])] if brazo.startswith('PERILLAS') else None),
                   banco_corte_g=(((E.get('corte') or {}).get('banco')) if brazo.startswith('PERILLAS') else None),
                   vivos_gr=[v[:4] + [[list(s) for s in v[4]]] for v in G['vivos_gr']][:60], cintas_vivos=C.get('cintas_vivos'))
    tmp = fin + '.tmp'
    with open(tmp, 'w', encoding='utf-8') as f: json.dump(res, f)
    os.replace(tmp, fin)
    return res


# ================================================================================ LA LETRA (PREREGISTRO_v01.md §6)
def veredicto(R, n_esperado=N, mundos=MUNDOS):
    L = []
    ok = lambda x: x is not None and not x.get('abortado')
    by = {(m, b): {x['seed']: x for x in R if x['brazo'] == b and x['mundo'] == m} for m in mundos for b in BRAZOS}
    completo = all(len(by[(m, b)]) == n_esperado for m in mundos for b in BRAZOS_MIN)
    hay_azar = len(by[('quieto', 'AZAR')]) == n_esperado
    hay_sos = all(len(by[(m, 'CODIGO')]) > 0 for m in mundos)
    abortados = [(x['mundo'], x['brazo'], x['seed'], x['abortado']) for x in R if x.get('abortado')]
    bloq = sum(x.get('bloqueados', 0) for x in R if ok(x))
    def gana(m, a, b, f=lambda x: x['nac_solo']):
        w = n_ = 0
        for s in by[(m, a)]:
            if s in by[(m, b)] and ok(by[(m, a)][s]) and ok(by[(m, b)][s]):
                n_ += 1; w += int(f(by[(m, a)][s]) > f(by[(m, b)][s]))
        return w, n_
    def suma(m, b): return sum(x['nac_solo'] for x in by[(m, b)].values() if ok(x))
    def razon(m, a, b): return (suma(m, a) + 1) / (suma(m, b) + 1)
    P0 = gana('quieto', 'CODIGO_SIN_SOS', 'PERILLAS'); P0ok = P0[0] >= 15
    P1 = {m: gana(m, 'CODIGO_SIN_SOS', 'PERILLAS_ROBUSTA') for m in mundos}; P1ok = {m: P1[m][0] >= 15 for m in mundos}
    Rq = razon('quieto', 'CODIGO_SIN_SOS', 'PERILLAS_ROBUSTA'); Ro = razon('onda8k', 'CODIGO_SIN_SOS', 'PERILLAS_ROBUSTA'); P2ok = Ro >= 1.5 * Rq
    Rq0 = razon('quieto', 'CODIGO_SIN_SOS', 'PERILLAS'); Ro0 = razon('onda8k', 'CODIGO_SIN_SOS', 'PERILLAS')
    P3 = {m: (gana(m, 'CODIGO', 'CODIGO_SIN_SOS'), gana(m, 'CODIGO_SIN_SOS', 'CODIGO')) for m in mundos}
    if not hay_sos: L.append('P3 (SOS) NO MEDIDA: la serie corrio sin CODIGO con SOS (--con_sos)')
    gM = gana('quieto', 'CODIGO_SIN_SOS', 'MUT0'); gA = gana('quieto', 'CODIGO_SIN_SOS', 'AZAR'); GM = gM[0] >= 14; GA = (gA[0] >= 14) if hay_azar else None
    pers = {m: {b: sum(int(x.get('persiste', 0)) for x in by[(m, b)].values() if ok(x)) for b in BRAZOS} for m in mundos}
    medn = lambda m, b, k: (round(float(np.median([x[k] for x in by[(m, b)].values() if ok(x) and x.get(k) is not None])), 4)
                            if any(ok(x) and x.get(k) is not None for x in by[(m, b)].values()) else None)
    for m in mundos:
        L.append(f"[{m}] nac solo (suma) " + str({b: suma(m, b) for b in BRAZOS}) + " · persisten " + str(pers[m]))
        L.append(f"[{m}] R0 final mediana " + str({b: medn(m, b, 'r0_final') for b in BRAZOS}) + " · fenotipo identico (mediana) "
                 + str({b: medn(m, b, 'ident') for b in BRAZOS}))
    L.append(f"P0 base: CODIGO_SIN_SOS > PERILLAS en quieto {P0[0]}/{P0[1]} -> {P0ok}")
    for m in mundos: L.append(f"P1 [{m}] CODIGO_SIN_SOS > PERILLAS_ROBUSTA {P1[m][0]}/{P1[m][1]} -> {P1ok[m]}")
    L.append(f"P2 amplificacion: razon SIN_SOS/ROBUSTA onda8k {Ro:.3f} vs quieto {Rq:.3f} (x{Ro / Rq:.2f}; pide >= 1.5) -> {P2ok} "
             f"· (contra PERILLAS: onda {Ro0:.3f} quieto {Rq0:.3f})")
    for m in (mundos if hay_sos else ()): L.append(f"P3 [{m}] CODIGO > SIN_SOS {P3[m][0][0]}/{P3[m][0][1]} · SIN_SOS > CODIGO {P3[m][1][0]}/{P3[m][1][1]}"
                              f" -> {'la SOS ayuda' if P3[m][0][0] >= 13 else ('la SOS ESTORBA' if P3[m][1][0] >= 13 else 'sin diferencia')}")
    L.append(f"guardia variacion (quieto) SIN_SOS > MUT0 {gM[0]}/{gM[1]} -> {GM} · guardia seleccion (quieto) SIN_SOS > AZAR {gA[0]}/{gA[1]} -> {GA}")
    n1 = sum(int(v) for v in P1ok.values())
    if not completo: v = 'NO EVALUABLE (ventana incompleta)'
    elif abortados: v = f'NO EVALUABLE (abortadas: {abortados[:3]})'
    elif bloq > 0: v = f'NO EVALUABLE (tope de cuerpos: bloqueados = {bloq})'
    elif n1 == len(mundos) and GM and GA is None: v = 'HAY ALGO MODESTO (P1 pasa en los dos mundos y la guardia de variacion; la de SELECCION no se midio: AZAR incompleto)'
    elif n1 == len(mundos) and GM and GA: v = 'FUNCIONA — LA ESTRUCTURA DE LA CINTA AYUDA: con la carga mutacional igualada el codigo sigue viviendo solo mejor, en los dos mundos'
    elif n1 == len(mundos): v = f"HAY ALGO MODESTO (P1 pasa en los dos mundos pero cae la guardia de {'variacion' if not GM else 'seleccion'}: no se atribuye a la variacion seleccionada)"
    elif n1 >= 1: v = f"HAY ALGO MODESTO (P1 pasa solo en {[m for m in mundos if P1ok[m]]})"
    else: v = 'NO — con la carga igualada la cinta no vive mejor: la ventaja de v0 era mutacion mas suave'
    L.append(f"VEREDICTO CODIGO v0.1 POR LA LETRA (una ventana; el bloque exige serie + replica con el mismo veredicto): {v}")
    return v, L


RASGOS_DESC = (('eta', 0), ('alpha', 2), ('aversion', 4), ('dote', 15), ('rep_umbral', 16), ('rep_X', 17), ('tau_e', 1))


def banco_desc(R, mundos=MUNDOS):
    """DESCRIPTIVO: el banco en el CORTE, en log(g/G0), mediana sobre semillas de la media del banco. Cintas: se DESARROLLAN (CD.desarrolla);
    PERILLAS: los genomas numericos del banco. Tambien: fraccion de cintas con algun EJE 2 de d < 0 ('vida rapida' en una mutacion)."""
    import pista2 as P2
    G0 = MV.genoma0(P2.cfg_fabrica()); lo, hi = MV.rangos(G0); L = []
    for m in mundos:
        for b in BRAZOS:
            vs = []; e2 = []
            for x in R:
                if x['mundo'] != m or x['brazo'] != b or x.get('abortado'): continue
                if x.get('banco_corte_cintas'):
                    cs = [CD.valida([tuple(i) for i in c]) for c in x['banco_corte_cintas']]
                    gs = np.array([CD.desarrolla(c, G0, lo, hi, MV.ENTEROS)[0] for c in cs])
                    e2.append(float(np.mean([any(i[0] == 'EJE' and i[1] == 2 and i[2] < 0 for i in c) for c in cs])))
                elif x.get('banco_corte_g'): gs = np.array(x['banco_corte_g'])
                else: continue
                vs.append(np.log(gs[:, :len(G0)] / G0).mean(0))
            if not vs: continue
            md = np.median(np.array(vs), 0)
            L.append(f"  banco en el corte [{m}] {b:<16} (n {len(vs)}) log(g/G0): " + ' '.join(f"{nm} {md[j]:+.3f}" for nm, j in RASGOS_DESC)
                     + (f" · cintas con EJE 2 d<0: {np.median(e2):.3f}" if e2 else ''))
    return L


def SHAS():
    f = lambda p: hashlib.sha256(open(p, 'rb').read()).hexdigest()[:16]
    ps = {'v01/corre_v01.py': os.path.join(AQUI, 'corre_v01.py'), 'v01/motor_v01.py': os.path.join(AQUI, 'motor_v01.py'),
          'v01/construye_v01.py': os.path.join(AQUI, 'construye_v01.py'), 'v01/PREREGISTRO_v01.md': os.path.join(AQUI, 'PREREGISTRO_v01.md'),
          'exploracion_fable/motor_fable.py': os.path.join(FAB, 'motor_fable.py'), 'exploracion_fable/fable_mundos.py': os.path.join(FAB, 'fable_mundos.py'),
          'codigo_def.py': os.path.join(COD, 'codigo_def.py'), 'carros/FAMB_GRAM_ECO.py': os.path.join(COD, 'carros', 'FAMB_GRAM_ECO.py')}
    return {k: f(p) for k, p in ps.items() if os.path.exists(p)}


def linea(x):
    return (f"{x['mundo']:<7} {x['brazo']:<16} s{x['seed']}: {x['seg']} s · abort {x['abortado']} · persiste {x.get('persiste')} (vivos {x.get('vivos_T')}) · "
            f"nac solo {x.get('nac_solo')} · R0 final {x.get('r0_final')} · B_pre {x.get('B_pre')} post/pre {x.get('nac_post_rel')} · "
            f"fenotipo identico {x.get('ident')} (n {x.get('n_ident')}) · errores/copia {x.get('errores_copia')} · SOS {x.get('sos_pre')}->{x.get('sos_post')} · "
            f"largo corte {x.get('largo_corte')} · lam {x.get('lam')}")


def parsea(argv):
    ap = argparse.ArgumentParser(allow_abbrev=False, add_help=False)
    for f_ in ('--calibra', '--calibra_rob', '--humo', '--serie', '--reanuda', '--con_golpe', '--con_sos'): ap.add_argument(f_, action='store_true')
    ap.add_argument('--lee', default=None); ap.add_argument('--lam', type=float); ap.add_argument('--ventana', default=None); ap.add_argument('--pool', type=int)
    try:
        a, resto = ap.parse_known_args(argv)
    except SystemExit:
        raise BanderaMala('V01: banderas mal formadas')
    if resto: raise BanderaMala(f"V01: banderas desconocidas {resto}")
    if any(x.startswith('--') and '=' in x for x in argv): raise BanderaMala('V01: sin la forma --bandera=valor')
    fl = [x for x in argv if x.startswith('--')]
    if len(fl) != len(set(fl)): raise BanderaMala('V01: bandera repetida')
    if int(a.calibra) + int(a.calibra_rob) + int(a.humo) + int(a.serie) + int(a.lee is not None) != 1:
        raise BanderaMala('V01: exactamente uno de --calibra, --calibra_rob, --humo, --serie, --lee')
    if a.calibra_rob and (a.lam is None or not 0 < a.lam <= 1): raise BanderaMala('V01: --calibra_rob --lam X (0 < X <= 1)')
    if a.serie and (a.ventana not in VENTANAS or a.pool is None or not 1 <= a.pool <= 6): raise BanderaMala('V01: --serie --ventana serie|replica --pool 1..6')
    if a.serie and LAMBDA_ROB is None: raise BanderaMala('V01: LAMBDA_ROB sin calibrar')
    if (a.calibra or a.humo or a.lee) and (a.pool or a.ventana or a.lam is not None): raise BanderaMala('V01: banderas de mas')
    return a


def main(argv=None):
    a = parsea(sys.argv[1:] if argv is None else argv)
    ts = time.strftime('%Y%m%d_%H%M%S')
    if a.lee is not None:
        R = [json.load(open(p, encoding='utf-8')) for p in sorted(glob.glob(os.path.join(a.lee, '*__*_s*.json')))]
        ms = tuple(m for m in MUNDOS if any(x['mundo'] == m for x in R))
        v, L = veredicto(R, n_esperado=len(set(x['seed'] for x in R)), mundos=ms)
        for l in L + ['DESCRIPTIVO (no entra a la letra):'] + banco_desc(R, ms): print(l)
        return
    if a.calibra or a.calibra_rob:
        carpeta = os.path.join(DATOS, 'calibra1' if a.calibra else f"calibra2_lam{a.lam}"); os.makedirs(carpeta, exist_ok=True)
        jobs = ([(s, 'CODIGO_SIN_SOS', m) for m in MUNDOS for s in SEM_CAL1] if a.calibra else [(s, 'PERILLAS_ROBUSTA', 'quieto') for s in SEM_CAL2])
        TLc = TL_CAL
        print(f"[{time.strftime('%H:%M:%S')}] CALIBRACION {'1 (el objetivo: CODIGO_SIN_SOS)' if a.calibra else f'2 (PERILLAS_ROBUSTA lam {a.lam})'} · TL {TLc} · shas {SHAS()}", flush=True)
        R = []
        for s, b, m in jobs:
            x = trabajo((s, b, m, TLc, carpeta, True, a.lam)); R.append(x); print(f"[{time.strftime('%H:%M:%S')}] " + linea(x), flush=True)
        # fraccion POOLED (partos antes del corte, sumados sobre corridas)
        num = sum((x.get('ident') or 0) * x.get('n_ident', 0) for x in R if x.get('ident') is not None); den = sum(x.get('n_ident', 0) for x in R if x.get('ident') is not None)
        f = num / den if den else None
        out = dict(fase=1 if a.calibra else 2, lam=a.lam, ident_pooled=f, n=den, por_corrida=[(x['mundo'], x['seed'], x.get('ident'), x.get('n_ident'), x['seg']) for x in R], shas=SHAS())
        if a.calibra and f is not None:
            out['lam_analitico'] = lam_para(f); out['f_ident_perillas_lam1'] = f_ident_perillas(1.0)
            print(f"OBJETIVO fenotipo identico (CODIGO_SIN_SOS, pooled) = {f:.4f} (n {den}) -> lambda analitico {out['lam_analitico']:.4f} "
                  f"(PERILLAS de hoy: analitico {f_ident_perillas(1.0):.4f})")
        else: print(f"PERILLAS_ROBUSTA lam {a.lam}: fenotipo identico pooled = {f} (n {den}); analitico {f_ident_perillas(a.lam):.4f}")
        json.dump(out, open(os.path.join(carpeta, 'CALIBRACION.json'), 'w', encoding='utf-8'), indent=1)
        return
    if a.humo:
        carpeta = os.path.join(DATOS, 'humo', f"v01_humo_{ts}"); os.makedirs(carpeta, exist_ok=True); t0 = time.time()
        print(f"[{time.strftime('%H:%M:%S')}] HUMO v0.1 {TL_HUMO} · LAMBDA_ROB {LAMBDA_ROB} · shas {SHAS()}", flush=True)
        for m in MUNDOS:
            for b in BRAZOS_SERIE:
                x = trabajo((SEM_HUMO, b, m, TL_HUMO, carpeta, False, None)); print(f"[{time.strftime('%H:%M:%S')}] " + linea(x)[:330], flush=True)
        R = [json.load(open(p, encoding='utf-8')) for p in sorted(glob.glob(os.path.join(carpeta, '*__*_s*.json')))]
        v, L = veredicto(R, n_esperado=1)
        for l in L: print('   ' + l)
        json.dump(dict(humo=True, tl=TL_HUMO, lam=LAMBDA_ROB, seg=round(time.time() - t0, 1), shas=SHAS(), veredicto_sin_valor=v, lineas=L,
                       corridas=[linea(x) for x in R]), open(os.path.join(carpeta, 'HUMO.json'), 'w', encoding='utf-8'), indent=1)
        print(f"HUMO: {round(time.time() - t0, 1)} s (numeros sin valor) · {os.path.relpath(carpeta, RAIZ)}")
        return
    # --serie (SOLO el coordinador; Pool)
    d0 = VENTANAS[a.ventana]; semillas = range(d0, d0 + N); etq = f"v01_{a.ventana}_s{d0}-{d0 + N - 1}"
    carpeta = os.path.join(DATOS, etq)
    if os.path.exists(carpeta) and not a.reanuda and glob.glob(os.path.join(carpeta, '*_s*.json')): raise SystemExit(f"V01: {carpeta} ya tiene resultados; --reanuda")
    os.makedirs(carpeta, exist_ok=True)
    flog = open(os.path.join(carpeta, 'progreso.log'), 'a', encoding='utf-8')
    def log(s):
        s = f"[{time.strftime('%H:%M:%S')}] {s}"; print(s, flush=True); flog.write(s + '\n'); flog.flush()
    ms = MUNDOS + ((MUNDO_REF,) if a.con_golpe else ())
    log(f"V01 {etq} · mundos {ms} · {TL} · LAMBDA_ROB {LAMBDA_ROB} · pool {a.pool} · shas {SHAS()}")
    bs = BRAZOS_SERIE + (('CODIGO',) if a.con_sos else ())
    jobs = [(s, b, m, TL, carpeta, a.reanuda, None) for b in bs for m in ms for s in semillas if b in BRAZOS_MIN]   # la letra minima PRIMERO
    jobs += [(s, b, m, TL, carpeta, a.reanuda, None) for b in bs for m in ms for s in semillas if b not in BRAZOS_MIN]   # AZAR (y CODIGO) al final
    t0 = time.time()
    from multiprocessing import Pool
    with Pool(a.pool) as pool:
        for k, x in enumerate(pool.imap_unordered(trabajo, jobs), 1): log(f"[{k}/{len(jobs)}] " + linea(x)[:300])
    R = [json.load(open(p, encoding='utf-8')) for p in sorted(glob.glob(os.path.join(carpeta, '*__*_s*.json')))]
    v, L = veredicto(R)
    for l in L: log(l)
    json.dump(dict(etiqueta=etq, veredicto=v, lineas=L, seg=round(time.time() - t0), TL=TL, lam=LAMBDA_ROB, shas=SHAS()),
              open(os.path.join(carpeta, 'RESUMEN.json'), 'w', encoding='utf-8'), indent=1, default=str)
    flog.close()


if __name__ == '__main__':
    try:
        main()
    except BanderaMala as e:
        print(str(e), file=sys.stderr); sys.exit(2)
