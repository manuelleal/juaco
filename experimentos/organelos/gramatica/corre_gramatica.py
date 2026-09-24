"""corre_gramatica.py — RUNNER de ORGANELOS / GRAMATICA: ¿la seleccion ARMA un organo de transmision con piezas? (Opus A, 24-sep-2026).

MISION: llegar a la AGI por este camino.

Preregistro: experimentos/organelos/gramatica/PREREGISTRO_gramatica.md (la letra esta AQUI, en veredicto(), y alli).
Instrumento: motor_gramatica.py + carros/FAMB_GRAM_ECO.py (construye_gramatica.py; arnes identidad_gramatica.py) + gramatica_def.py +
conducta.py (novedad por CONDUCTA). Mundo w30 (esc 30, 30 fundadores, quimiostato 0.9 objetos por paso), el de ECO v2.1.

Brazos (vivero con banco 200 y 8 sombras hasta el corte; despues nadie repone nada):
  VIDA   fundadores con UN slot SILENCIOSO (cuando = nunca; que/quien/como al azar) + errores de copia de la gramatica + mutacion numerica
         (18 genes); el hijo copia al PADRE (seleccion).
  AZAR   igual, pero todo cuerpo nuevo copia una entrada AL AZAR del banco (deriva pura; motor_eco3.py:438/477).
  MUT0   igual que VIDA sin ningun error de copia (ni gramatica ni numeros): el organo silencioso no puede prenderse.
  FIJO:x la gramatica x fija en todos (disenados 'ensena', 'filtra0', 'nulo', o cualquier gramatica de la fuerza bruta), sin errores de
         copia de la gramatica; mutacion numerica y seleccion como VIDA.
nube-9: trabajo() ATRAPA SystemExit/Exception del motor (la guardia de ERR-60 y cualquier otra) y escribe el JSON con 'abortado'; nunca
cuelga un Pool. Ademas T = 120 000 en w30 queda lejos de la guardia (max_nac_linaje se registra; ver PREREGISTRO §7).

Uso (banderas desconocidas o abreviadas abortan, ERR-115):
  python experimentos/organelos/gramatica/corre_gramatica.py --humo
  python experimentos/organelos/gramatica/corre_gramatica.py --fuerza --bloque K --de N        # exploratoria, UN proceso
  python experimentos/organelos/gramatica/corre_gramatica.py --fuerza_lee <carpeta>
  python experimentos/organelos/gramatica/corre_gramatica.py --fuerza_conf --pool P [--reanuda]   # SOLO el coordinador: define el TOP
  python experimentos/organelos/gramatica/corre_gramatica.py --serie --ventana serie|replica --pool P [--reanuda]   # SOLO el coordinador
  python experimentos/organelos/gramatica/corre_gramatica.py --lee <carpeta> --top <RANKING.json de la confirmatoria>
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
MUNDO = dict(nombre='w30', esc=30, n0=30, tope=3000)
SERIE = dict(T=120000, t_corte=60000, r0_margen=20000, banco=200, n_sombra=8, sigma=0.15, p_mut=0.05, cada_gen=2000, ckpt_cada=10000)
GRAM = dict(p_campo=0.05, p_dup=0.02, p_del=0.02, tope=4)
# alfabeto de la serie: 'olvidar' (como = 3) FUERA por el arnes por pieza (inerte en w30 con un slot: PREREGISTRO §2)
ALFABETO = (tuple(range(len(GD.CUANDO))), tuple(range(len(GD.QUE))), tuple(range(len(GD.QUIEN))), (0, 1, 2))
MUTABLES = tuple(g for g in MG.NOMBRES if g not in ('ensena', 'filtra0'))   # los genes numericos de organo quedan como pseudogenes fijos
FIJOS = dict(ensena=GD.ENSENA, filtra0=GD.FILTRA0, nulo=GD.NULO)
BRAZOS_SERIE = ('VIDA', 'AZAR', 'MUT0', 'FIJO:ensena', 'FIJO:filtra0', 'FIJO:nulo')
VENTANAS = {'serie': 21011, 'replica': 21031}
N = 20
HUMO = dict(semilla=21001, T=20000, t_corte=10000, r0_margen=5000)
FUERZA = dict(semillas=(21101,), T=18000, t_corte=6000, r0_margen=6000)   # exploratoria (PREREGISTRO §5); la confirmatoria usa CONF
CONF = dict(semillas=(21201, 21202, 21203))   # fuerza bruta CONFIRMATORIA (RESERVADA: Pool, coordinador); define el TOP
DATOS = os.path.join(AQUI, 'datos')


class BanderaMala(SystemExit):
    pass


def gram_de(txt):
    """'VIDA'/'AZAR'/'MUT0' -> None; 'FIJO:ensena' -> la gramatica; 'FIJO:1.0.0.0' -> un slot (cuando.que.quien.como)."""
    if not txt.startswith('FIJO:'): return None
    x = txt[5:]
    if x in FIJOS: return FIJOS[x]
    v = tuple(int(z) for z in x.split('.'))
    if len(v) != 4: raise SystemExit(f"GRAMATICA: brazo {txt}")
    return GD.valida((v + (0,),))


def eco_de(brazo, seed, t_corte, **extra):
    fija = gram_de(brazo)
    if brazo in ('VIDA', 'AZAR', 'MUT0'):
        grs = GD.fundadores_silenciosos(seed, MUNDO['n0'], ALFABETO)
        gmut = brazo != 'MUT0'; pnum = brazo != 'MUT0'; don = 'azar' if brazo == 'AZAR' else 'padre'
    elif fija is not None:
        grs = [fija] * MUNDO['n0']; gmut = False; pnum = True; don = 'padre'
    else: raise SystemExit(f"GRAMATICA: brazo desconocido {brazo}")
    return dict(refunda=1, t_corte=t_corte, p_mut=(SERIE['p_mut'] if pnum else 0.0), sigma=SERIE['sigma'], banco=SERIE['banco'],
                n_sombra=SERIE['n_sombra'], cada_gen=SERIE['cada_gen'], mutables=MUTABLES, donante=don, gramatica=grs,
                g_pcampo=(GRAM['p_campo'] if gmut else 0.0), g_pdup=(GRAM['p_dup'] if gmut else 0.0), g_pdel=(GRAM['p_del'] if gmut else 0.0),
                g_tope=GRAM['tope'], g_alfabeto=ALFABETO, **extra)


def _lista(gr): return [list(s) for s in gr] if gr is not None else None


def trabajo(args):
    """UNA corrida (semilla, brazo). Escribe su JSON. Nunca lanza: atrapa SystemExit/Exception del motor (nube-9)."""
    seed, brazo, T, t_corte, r0_margen, carpeta, reanuda = args
    nom = brazo.replace(':', '_')
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
                             eco=eco_de(brazo, seed, t_corte, ckpt_cada=(SERIE['ckpt_cada'] if T >= 2 * SERIE['ckpt_cada'] else 0),
                                        ckpt_fn=guarda, estado=estado, ind_cb=cb))
    except SystemExit as e: abortado = f"SystemExit: {e}"          # nube-9: la guardia de ERR-60 (u otra) no cuelga nada
    except Exception as e: abortado = f"{type(e).__name__}: {e}"
    res = dict(seed=seed, brazo=brazo, T=T, t_corte=t_corte, r0_margen=r0_margen, seg=round(time.time() - t0, 1), abortado=abortado,
               mundo=MUNDO, gram_cfg=dict(GRAM, alfabeto=[list(a) for a in ALFABETO]))
    if r is not None:
        E = r['eco']; P = r['pista']; G = r['gram']
        coh = [f for f in filas if f[4] <= T - r0_margen]
        res.update(t_ext=E['t_ext'], persiste=int(E['t_ext'] is None and len(E['vivos_final']) > 0), vivos_T=len(E['vivos_final']),
                   linajes_T=len(set(v[0] for v in E['vivos_final'])), bloqueados=P['bloqueados'], max_vivos=P['max_vivos'],
                   n_nac=E['n_nac'], n_refund=E['n_refund'], n_banco=E['n_banco'], nac_post=len(filas),
                   r0_post=(round(float(np.mean([f[6] for f in coh])), 4) if coh else None), n_coh_post=len(coh),
                   tam_total=P['tam_total'], max_nac_linaje=G['max_nac_linaje'], g_nmut=G['g_nmut'], entregas=G['entregas'],
                   corte_gr=(None if not G['corte'] else dict(t=G['corte']['t'], banco_gr=[_lista(x) for x in G['corte']['banco_gr']],
                                                            banco_gs=[[_lista(y) for y in x] for x in G['corte']['banco_gs']],
                                                            vivos_gr=[v[:4] + [_lista(v[4])] for v in G['corte']['vivos_gr']])),
                   final_banco_gr=[_lista(x) for x in G['banco_final_gr']], final_banco_gs=[[_lista(y) for y in x] for x in G['banco_final_gs']],
                   vivos_gr=[v[:4] + [_lista(v[4])] for v in G['vivos_gr']])
    tmp = fin + '.tmp'
    with open(tmp, 'w', encoding='utf-8') as f: json.dump(res, f)
    os.replace(tmp, fin)
    if os.path.exists(ck) and abortado is None: os.remove(ck)
    return res


# ================================================================================ ANALISIS (conducta)
def _tup(g): return tuple(tuple(s) for s in g) if g is not None else ()


def top_de_fuerza(ranking):
    """TOP = las clases de UN slot cuyo puntaje de la fuerza bruta CONFIRMATORIA queda a <= 0.10 del mejor (PREREGISTRO §5)."""
    if not ranking: return []
    best = max(x['puntaje'] for x in ranking)
    return [tuple(x['gram'][0][:4]) for x in ranking if x['puntaje'] >= best - 0.10]


def rasgo_top(gr, TOP):
    """1 si la gramatica EXPRESA algun slot cuya conducta de un slot es la de una clase TOP."""
    import conducta as C
    for s in GD.activos(_tup(gr)):
        for t in TOP:
            if C.igual(((s + (0,)),), ((tuple(t) + (0,)),)): return 1
    return 0


def modal(banco):
    """La CONDUCTA mas frecuente entre las gramaticas del banco (agrupadas por conducta, tolerancia TOL): (gramatica representante, fraccion)."""
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


def crea(g):
    """La prueba de 'CREA' (correccion 1): >= 2 slots activos, uno nacido por duplicacion (origen 1) cuya conducta de un slot no es
    ninguno de los disenados ni la de los otros slots, y la gramatica sin ese slot tiene OTRA conducta."""
    import conducta as C
    g = _tup(g); act = [s for s in g if s[0] != 0]
    if len(act) < 2: return False
    for s in act:
        if s[4] != 1: continue
        uno = ((s[:4] + (0,)),)
        if C.clase_disenada(uno) is not None: continue
        if any(C.igual(uno, ((o[:4] + (0,)),)) for o in act if o is not s): continue
        sin = tuple(o for o in g if o is not s)
        if not C.igual(g, sin): return True
    return False


def veredicto(R, TOP, n_esperado=N):
    """La letra (PREREGISTRO §6). R = JSON de una ventana; TOP = clases de la fuerza bruta confirmatoria."""
    import conducta as C
    L = []
    by = {b: {x['seed']: x for x in R if x['brazo'] == b} for b in BRAZOS_SERIE}
    completo = all(len(by[b]) == n_esperado for b in BRAZOS_SERIE)
    abortados = [(x['brazo'], x['seed'], x['abortado']) for x in R if x.get('abortado')]
    bloq = sum(x.get('bloqueados', 0) for x in R if not x.get('abortado'))

    def expr(b):
        mas = k = 0; fr = {}
        for s, x in by[b].items():
            if x.get('abortado') or not x.get('final_banco_gr'): continue
            real = float(np.mean([rasgo_top(g, TOP) for g in x['final_banco_gr']]))
            somb = [float(np.mean([rasgo_top(gs[q], TOP) for gs in x['final_banco_gs']])) for q in range(SERIE['n_sombra'])]
            k += 1; mas += int(real > float(np.mean(somb))); fr[s] = real
        return mas, k, fr
    eV = expr('VIDA'); eA = expr('AZAR')
    P1a = eV[0] >= 15
    w = sum(1 for s in eV[2] if s in eA[2] and eV[2][s] > eA[2][s]); P1b = w >= 15
    guardia = eA[0] >= 15
    mut0_mal = any(x.get('entregas') or any(GD.activos(_tup(g)) for g in (x.get('final_banco_gr') or [])) for x in by['MUT0'].values())
    top2 = nov3 = cre = 0; mod_txt = []
    for s, x in sorted(by['VIDA'].items()):
        if x.get('abortado') or not x.get('persiste'): mod_txt.append((s, 'extinta' if not x.get('abortado') else 'abortada')); continue
        g, f = modal(x['final_banco_gr'])
        en_top = rasgo_top(g, TOP) == 1; dis = C.clase_disenada(g); c_ = crea(g)
        top2 += int(en_top); nov3 += int(en_top and dis is None); cre += int(c_)
        mod_txt.append((s, GD.texto(g), round(f, 3), 'TOP' if en_top else '-', dis or 'NUEVO', 'CREA' if c_ else ''))
    P2 = top2 >= 14; P3 = nov3 >= 10; P4 = cre >= 5

    def slots(b, activos_=True):   # LARGO del organo (pedido del coordinador tras D1 de exploracion_fable): real, sombras y AZAR
        out = {}
        for s, x in by[b].items():
            if x.get('abortado') or not x.get('final_banco_gr'): continue
            n_ = (lambda g: len(GD.activos(_tup(g)))) if activos_ else (lambda g: len(_tup(g)))
            out[s] = (float(np.mean([n_(g) for g in x['final_banco_gr']])),
                      float(np.mean([np.mean([n_(gs[q]) for gs in x['final_banco_gs']]) for q in range(SERIE['n_sombra'])])))
        return out
    Sv = slots('VIDA'); Sa = slots('AZAR'); Svt = slots('VIDA', False); Sat = slots('AZAR', False)

    def amplifica(b):   # P5 (SECUNDARIO, no cambia el veredicto): la seleccion CONCENTRA el banco en UN organo armado (TOP o no)
        # estadistico SIMETRICO: c(banco) = fraccion del banco final que expresa su clase ACTIVA mas frecuente (por conducta). Se calcula
        # igual para el real y para cada una de las 8 pistas de sombras; nula (intercambiables): P(real > media de sombras) ~ 0.5.
        n5 = k5 = 0; txt = []
        for s, x in sorted(by[b].items()):
            if x.get('abortado') or not x.get('final_banco_gr'): continue
            def conc(ban):
                act = [g for g in ban if GD.activos(_tup(g))]
                if not act: return 0.0, ()
                X, f = modal(act); return f * len(act) / len(ban), X
            cr, X = conc(x['final_banco_gr']); cs = [conc([gs[q] for gs in x['final_banco_gs']])[0] for q in range(SERIE['n_sombra'])]
            k5 += 1; n5 += int(cr > float(np.mean(cs))); txt.append((s, GD.texto(X), round(cr, 3), round(float(np.mean(cs)), 3), C.clase_disenada(X) or 'NUEVO'))
        return n5, k5, txt
    A5v = amplifica('VIDA'); A5a = amplifica('AZAR')
    s_somb = sum(1 for s in Sv if Sv[s][0] > Sv[s][1]); s_az = sum(1 for s in Sv if s in Sa and Sv[s][0] > Sa[s][0])
    S_sel = s_somb >= 15 and s_az >= 15
    med = lambda D, i: (round(float(np.median([v[i] for v in D.values()])), 3) if D else None)
    pers = {b: sum(int(x.get('persiste', 0)) for x in by[b].values()) for b in BRAZOS_SERIE}
    r0 = {b: (round(float(np.median([x['r0_post'] for x in by[b].values() if x.get('r0_post') is not None])), 4)
              if any(x.get('r0_post') is not None for x in by[b].values()) else None) for b in BRAZOS_SERIE}
    L.append(f"TOP (fuerza bruta confirmatoria): {[GD.texto(((t + (0,)),)) for t in TOP]}")
    L.append(f"P1a VIDA expresa TOP sobre la media de sus 8 sombras {eV[0]}/{eV[1]} (AZAR {eA[0]}/{eA[1]}) · P1b VIDA > AZAR {w}/{len(eV[2])}")
    L.append(f"P2 modal de VIDA en TOP {top2}/20 · P3 en TOP y NO disenado {nov3}/20 · P4 CREA {cre}/20")
    L.append(f"persisten en T {pers} · R0 de nacidos tras el corte (mediana) {r0}")
    L.append(f"S (largo, secundario) slots ACTIVOS en el banco final (mediana): VIDA {med(Sv, 0)} · sus sombras {med(Sv, 1)} · AZAR {med(Sa, 0)} · "
             f"VIDA > sombras {s_somb}/{len(Sv)} · VIDA > AZAR {s_az}/{len(Sv)} -> {'la seleccion ELIGE el largo' if S_sel else 'el largo NO lo eligio la seleccion'}; "
             f"slots TOTALES (con silenciosos): VIDA {med(Svt, 0)} · sombras {med(Svt, 1)} · AZAR {med(Sat, 0)}")
    L.append(f"P5 (secundario) VIDA CONCENTRA el banco final en un organo armado mas que sus sombras {A5v[0]}/{A5v[1]} (AZAR {A5a[0]}/{A5a[1]}); "
             f"no disenados entre los de VIDA: {sum(1 for t in A5v[2] if t[4] == 'NUEVO')}")
    for m in mod_txt: L.append(f"  VIDA s{m[0]}: {m[1:]}")
    for t in A5v[2]: L.append(f"  P5 VIDA s{t[0]}: {t[1]} real {t[2]} sombras {t[3]} {t[4]}")
    if not completo: v = 'NO EVALUABLE (ventana incompleta)'
    elif abortados: v = f'NO EVALUABLE (abortadas por el motor: {abortados[:3]})'
    elif bloq > 0: v = f'NO EVALUABLE (tope de cuerpos: bloqueados = {bloq})'
    elif guardia: v = f'NO EVALUABLE (AZAR expresa TOP sobre sus sombras {eA[0]}/20)'
    elif mut0_mal: v = 'NO EVALUABLE (MUT0 transmite: el instrumento esta mal)'
    elif P1a and P1b and P2 and P3 and P4: v = 'FUNCIONA — LA SELECCION CREA UN ORGANO (un slot duplicado diverge a una funcion que ningun disenado tiene)'
    elif P1a and P1b and P2 and P3: v = 'FUNCIONA — LA SELECCION COMBINA UN ORGANO QUE NO ESCRIBIMOS'
    elif (P1a and P1b and P2) or (P1a and P1b): v = 'HAY ALGO MODESTO (la seleccion arma un organo TOP con piezas, pero es conductualmente un disenado o no llega al tope en >= 14/20)'
    elif P1a or P1b: v = 'HAY ALGO MODESTO (solo una de las dos pruebas contra la deriva)'
    else: v = 'NO'
    L.append(f"VEREDICTO ORGANELOS/GRAMATICA POR LA LETRA (una ventana; el bloque exige serie + replica con el mismo veredicto): {v}")
    return v, L, dict(P1a=P1a, P1b=P1b, P2=P2, P3=P3, P4=P4, S_sel=S_sel, P5=(A5v[0], A5v[1], A5a[0], A5a[1]), pers=pers, r0=r0, w=w, eV=eV[:2], eA=eA[:2])


# ================================================================================ FUERZA BRUTA
def lista_fuerza():
    """Nulo + las 135 gramaticas de UN slot del alfabeto de la serie (cuando != nunca), en orden fijo."""
    return ['FIJO:nulo'] + [f"FIJO:{s[0][0]}.{s[0][1]}.{s[0][2]}.{s[0][3]}" for s in GD.un_slot_todos(ALFABETO)]


def puntaje(xs):
    """Puntaje de la fuerza bruta: media sobre semillas de (persiste + min(R0 de nacidos tras el corte, 1.2)) / 2.2 (0..1)."""
    v = [(int(x.get('persiste', 0)) + min(float(x['r0_post'] or 0.0), 1.2)) / 2.2 for x in xs if not x.get('abortado') and 'persiste' in x]
    return round(float(np.mean(v)), 4) if v else None


def fuerza_lee(carpeta):
    R = [json.load(open(p, encoding='utf-8')) for p in sorted(glob.glob(os.path.join(carpeta, 'FIJO_*_s*.json')))]
    por = {}
    for x in R: por.setdefault(x['brazo'], []).append(x)
    rk = []
    for b, xs in por.items():
        g = gram_de(b); rk.append(dict(brazo=b, gram=[list(s) for s in g], texto=GD.texto(g), n=len(xs), puntaje=puntaje(xs),
                                      persiste=sum(int(x.get('persiste', 0)) for x in xs),
                                      r0=[x.get('r0_post') for x in xs], vivos_T=[x.get('vivos_T') for x in xs], seg=sum(x['seg'] for x in xs)))
    rk.sort(key=lambda z: -(z['puntaje'] if z['puntaje'] is not None else -1))
    return rk


def SHAS():
    f = lambda p: hashlib.sha256(open(os.path.join(AQUI, p), 'rb').read()).hexdigest()[:16]
    return {p: f(p) for p in ('corre_gramatica.py', 'motor_gramatica.py', 'carros/FAMB_GRAM_ECO.py', 'gramatica_def.py', 'conducta.py',
                              'construye_gramatica.py', 'PREREGISTRO_gramatica.md') if os.path.exists(os.path.join(AQUI, p))}


def parsea(argv):
    ap = argparse.ArgumentParser(allow_abbrev=False, add_help=False)
    ap.add_argument('--humo', action='store_true'); ap.add_argument('--serie', action='store_true')
    ap.add_argument('--fuerza', action='store_true'); ap.add_argument('--fuerza_lee', default=None); ap.add_argument('--lee', default=None)
    ap.add_argument('--bloque', type=int); ap.add_argument('--de', type=int)
    ap.add_argument('--ventana', default=None); ap.add_argument('--pool', type=int); ap.add_argument('--reanuda', action='store_true')
    ap.add_argument('--top', default=None); ap.add_argument('--fuerza_conf', action='store_true')
    try:
        a, resto = ap.parse_known_args(argv)
    except SystemExit:
        raise BanderaMala('GRAMATICA: banderas mal formadas')
    if resto: raise BanderaMala(f"GRAMATICA: banderas desconocidas {resto}")
    if any(x.startswith('--') and '=' in x for x in argv): raise BanderaMala('GRAMATICA: sin la forma --bandera=valor')
    flags = [x for x in argv if x.startswith('--')]
    if len(flags) != len(set(flags)): raise BanderaMala('GRAMATICA: bandera repetida')
    if int(a.humo) + int(a.serie) + int(a.fuerza) + int(a.fuerza_conf) + int(a.fuerza_lee is not None) + int(a.lee is not None) != 1:
        raise BanderaMala('GRAMATICA: exactamente uno de --humo, --fuerza, --fuerza_conf, --fuerza_lee, --serie, --lee')
    if a.fuerza_conf and (a.pool is None or not 1 <= a.pool <= 6 or a.ventana or a.top or a.bloque is not None or a.de is not None):
        raise BanderaMala('GRAMATICA: --fuerza_conf --pool 1..6 [--reanuda] (SOLO el coordinador)')
    if a.humo and (a.ventana or a.pool or a.reanuda or a.bloque is not None or a.de is not None or a.top): raise BanderaMala('GRAMATICA: --humo va solo')
    if a.fuerza and (a.bloque is None or a.de is None or not 0 <= a.bloque < a.de or a.pool or a.ventana or a.top):
        raise BanderaMala('GRAMATICA: --fuerza --bloque K --de N (0 <= K < N), un proceso')
    if a.serie and (a.ventana not in VENTANAS or a.pool is None or not 1 <= a.pool <= 6 or a.top is None):
        raise BanderaMala('GRAMATICA: --serie --ventana serie|replica --pool 1..6 --top <ranking confirmatorio JSON>')
    return a


def main(argv=None):
    a = parsea(sys.argv[1:] if argv is None else argv)
    if a.fuerza_lee is not None:
        rk = fuerza_lee(a.fuerza_lee)
        for z in rk: print(f"{z['puntaje']}  {z['texto']:<34} persiste {z['persiste']}/{z['n']} r0 {z['r0']} vivos {z['vivos_T']}")
        TOP = top_de_fuerza([z for z in rk if z['puntaje'] is not None and len(z['gram']) == 1])
        print(f"TOP (a <= 0.10 del mejor): {[GD.texto(((t + (0,)),)) for t in TOP]}")
        meta = dict(FUERZA, semillas=CONF['semillas']) if os.path.basename(os.path.normpath(a.fuerza_lee)).startswith('fuerza_conf') else FUERZA   # ERR-125 (d)
        json.dump(dict(ranking=rk, TOP=[list(t) for t in TOP], FUERZA=meta, shas=SHAS()), open(os.path.join(a.fuerza_lee, 'RANKING.json'), 'w', encoding='utf-8'), indent=1)
        return
    if a.lee is not None:
        R = [json.load(open(p, encoding='utf-8')) for p in sorted(glob.glob(os.path.join(a.lee, '*_s*.json')))]
        TOP = [tuple(t) for t in json.load(open(a.top, encoding='utf-8'))['TOP']] if a.top else []
        v, L, d = veredicto(R, TOP)
        for l in L: print(l)
        return
    if a.humo:
        ts = time.strftime('%Y%m%d_%H%M%S'); carpeta = os.path.join(DATOS, 'humo', f"gramatica_humo_{ts}"); os.makedirs(carpeta, exist_ok=True)
        t0 = time.time(); print(f"[{time.strftime('%H:%M:%S')}] HUMO GRAMATICA · shas {SHAS()}", flush=True)
        for b in ('VIDA', 'AZAR'):
            x = trabajo((HUMO['semilla'], b, HUMO['T'], HUMO['t_corte'], HUMO['r0_margen'], carpeta, False))
            ban = x.get('final_banco_gr') or []
            act = float(np.mean([len(GD.activos(_tup(g))) > 0 for g in ban])) if ban else None
            print(f"[{time.strftime('%H:%M:%S')}] {b}: {x['seg']} s · abortado {x['abortado']} · persiste {x.get('persiste')} (vivos {x.get('vivos_T')}, "
                  f"max {x.get('max_vivos')}) · r0 {x.get('r0_post')} · errores de copia {x.get('g_nmut')} · entregas {x.get('entregas')} · "
                  f"banco final con organo activo {act} · max_nac_linaje {x.get('max_nac_linaje')}", flush=True)
            if ban:
                from collections import Counter
                cc = Counter(GD.texto(GD.activos(_tup(g))) if GD.activos(_tup(g)) else '[silencioso]' for g in ban)
                print(f"    banco final (top 5): {cc.most_common(5)}", flush=True)
        print(f"HUMO: {round(time.time() - t0, 1)} s (numeros sin valor) · {os.path.relpath(carpeta, RAIZ)}")
        return
    if a.fuerza:
        L_ = lista_fuerza()[a.bloque::a.de]
        carpeta = os.path.join(DATOS, f"fuerza_explora_s{FUERZA['semillas'][0]}_T{FUERZA['T']}"); os.makedirs(carpeta, exist_ok=True)
        flog = open(os.path.join(carpeta, f"progreso_bloque{a.bloque}de{a.de}.log"), 'a', encoding='utf-8')

        def log(s):
            s = f"[{time.strftime('%H:%M:%S')}] {s}"; print(s, flush=True); flog.write(s + '\n'); flog.flush()
        log(f"FUERZA BRUTA exploratoria bloque {a.bloque}/{a.de}: {len(L_)} gramaticas x {len(FUERZA['semillas'])} semillas · {FUERZA} · shas {SHAS()}")
        t0 = time.time()
        for k, b in enumerate(L_, 1):
            for s in FUERZA['semillas']:
                x = trabajo((s, b, FUERZA['T'], FUERZA['t_corte'], FUERZA['r0_margen'], carpeta, True))
                log(f"[{k}/{len(L_)}] {GD.texto(gram_de(b)):<34} s{s}: persiste {x.get('persiste')} vivos {x.get('vivos_T')} r0 {x.get('r0_post')} "
                    f"(n {x.get('n_coh_post')}) entregas {x.get('entregas')} abort {x['abortado']} ({x['seg']} s; {round(time.time() - t0)} s)")
        flog.close()
        return
    if a.fuerza_conf:   # fuerza bruta CONFIRMATORIA (SOLO el coordinador; Pool): define el TOP de la serie
        carpeta = os.path.join(DATOS, f"fuerza_conf_s{CONF['semillas'][0]}-{CONF['semillas'][-1]}_T{FUERZA['T']}")
        if os.path.exists(carpeta) and not a.reanuda and glob.glob(os.path.join(carpeta, '*_s*.json')):
            raise SystemExit(f"GRAMATICA: {carpeta} ya tiene resultados; --reanuda")
        os.makedirs(carpeta, exist_ok=True)
        jobs = [(s, b, FUERZA['T'], FUERZA['t_corte'], FUERZA['r0_margen'], carpeta, a.reanuda) for b in lista_fuerza() for s in CONF['semillas']]
        t0 = time.time()
        from multiprocessing import Pool
        with Pool(a.pool) as pool:
            for k, x in enumerate(pool.imap_unordered(trabajo, jobs), 1):
                print(f"[{time.strftime('%H:%M:%S')}] [{k}/{len(jobs)}] {x['brazo']} s{x['seed']}: persiste {x.get('persiste')} r0 {x.get('r0_post')} abort {x['abortado']} ({round(time.time() - t0)} s)", flush=True)
        return main(['--fuerza_lee', carpeta])
    # --serie (SOLO el coordinador; Pool)
    TOP = [tuple(t) for t in json.load(open(a.top, encoding='utf-8'))['TOP']]
    d0 = VENTANAS[a.ventana]; semillas = range(d0, d0 + N); etq = f"gramatica_{a.ventana}_s{d0}-{d0 + N - 1}"
    carpeta = os.path.join(DATOS, etq)
    if os.path.exists(carpeta) and not a.reanuda and glob.glob(os.path.join(carpeta, '*_s*.json')):
        raise SystemExit(f"GRAMATICA: {carpeta} ya tiene resultados; --reanuda (no se pisa nada)")
    os.makedirs(carpeta, exist_ok=True)
    flog = open(os.path.join(carpeta, 'progreso.log'), 'a', encoding='utf-8')

    def log(s):
        s = f"[{time.strftime('%H:%M:%S')}] {s}"; print(s, flush=True); flog.write(s + '\n'); flog.flush()
    log(f"GRAMATICA {etq} · {SERIE} · {GRAM} · pool {a.pool} · TOP {TOP} · shas {SHAS()}")
    jobs = [(s, b, SERIE['T'], SERIE['t_corte'], SERIE['r0_margen'], carpeta, a.reanuda) for s in semillas for b in BRAZOS_SERIE]
    t0 = time.time()
    from multiprocessing import Pool
    with Pool(a.pool) as pool:
        for k, x in enumerate(pool.imap_unordered(trabajo, jobs), 1):
            log(f"[{k}/{len(jobs)}] {x['brazo']} s{x['seed']}: persiste {x.get('persiste')} vivos {x.get('vivos_T')} r0 {x.get('r0_post')} "
                f"abort {x['abortado']} ({x['seg']} s; {round(time.time() - t0)} s)")
    R = [json.load(open(p, encoding='utf-8')) for p in sorted(glob.glob(os.path.join(carpeta, '*_s*.json')))]
    v, L, d = veredicto(R, TOP)
    for l in L: log(l)
    json.dump(dict(etiqueta=etq, veredicto=v, lineas=L, d=d, seg=round(time.time() - t0), SERIE=SERIE, GRAM=GRAM, TOP=TOP, shas=SHAS()),
              open(os.path.join(carpeta, 'RESUMEN.json'), 'w', encoding='utf-8'), indent=1, default=str)
    flog.close()


if __name__ == '__main__':
    try:
        main()
    except BanderaMala as e:
        print(str(e), file=sys.stderr); sys.exit(2)
