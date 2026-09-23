"""pista2.py (CONSTRUIDO por experimentos/generaciones/construye_pista2.py desde carrera_escuderias/pista.py, sha 9f47c65e438e0ff4; NO editar a mano)
VERSION 2: opcion solapadas=1 -> motor_convive.run_solapadas (generaciones solapadas: el hijo nace como cuerpo vivo).
Con solapadas=0 es la pista original bit a bit (identidad_convive.py).

pista.py — LA PISTA DE LA CARRERA DE ESCUDERIAS (REGLAMENTO.md sec. 3 + ENMIENDA 1; paso 1 de sec. 9).

MISION: llegar a la AGI por este camino. La pista es el MUNDO VIVO de organismo_f9c (A comida, B veneno, C agua,
D sal, costos, ventana de reproduccion, dote, cola FIFO, muerte real, fundador del mundo si el linaje se queda
sin cola) con HASTA 9 LINAJES VIVOS A LA VEZ: un cuerpo vivo por linaje, cada linaje con su cola de hijos y su
carro (que lleva su nodo). Lo que uno come desaparece para todos. Origen (solo se LEYO):
experimentos/nivel09_cuerpo_nuevo_b2/organismo_f9c.py (SHA_F9C). Las constantes del mundo se DERIVAN en tiempo de
ejecucion de organismo_f9c.run (firma) + corre_bloque2.BRAZOS['REL'] (cfg_fabrica(); H-4 de la auditoria).

ENMIENDA 1 (ERR-95): con N carros y escala=1, L = 40*N y nobj = 4*N. Con N = 1 es la pista original.

NO se construyo por anclas: es una PARTICION del monolito en MUNDO (aqui) + CEREBRO (carros/FABRICA.py). La
garantia es identidad_pista.py: con UN carro FABRICA, pizarra apagada y compat=1, la vista plana (plano()) de la
salida reproduce organismo_f9c.run(**REL) BIT A BIT y deja el rng del mundo en el MISMO estado final.

ERR-96 (CRITICO, cerrado aqui): la salida de un linaje tiene DOS espacios de nombres. Las claves de primer nivel
son SOLO la verdad fisica de la pista; lo que devuelve carro.salida() va en d['carro'] y NUNCA pisa una clave
fisica. El juez lee solo las claves fisicas (juez.resumen_linaje). Test: test_tramposo.py.

ANCLA compat=1 (SOLO para el arnes): un unico rng default_rng(seed) hace de mundo Y de cuerpo del linaje 0,
hijos con 700000+1000000*seed+k, posicion inicial 0.
CARRERA compat=0 (siempre en el juez, tambien el control SOLO): rng sembrados con listas [seed, linaje, ETQ, k]
(ERR-60: sin colisiones): mundo 11 · cuerpo 12 (ctx['rng']) · hijo 13 (info['rng_hijo']) · muerte 14 (reaparicion,
fisica) · pista 15 (posiciones iniciales y ORDEN DE TURNO, permutacion nueva cada paso).

PASO t: 1. fase A en el orden de turno (actua, mover, morder, spawn, resultado) · 2. costos · 3. olvido del
mundo una vez por paso · 4. fase B en el mismo orden (fin_paso, muerte/nacimiento, ventana/parto) · 5. la
pizarra publica lo escrito en t (se lee en t+1).

CANAL: obs['cuerpos'] = foto al inicio del paso (id, pos, letra bajo el cuerpo, letra mordida en el paso
anterior) de todos los cuerpos; obs['pizarra'] = hasta CUPO=16 entradas (t, id, contenido de <= ANCHO=8
numeros), FIFO. La pizarra se guarda COMPLETA aparte (salida['pizarra_log']; el juez la escribe en su archivo).
PERCEPCION: la pista entrega TODOS los objetos (obs['objs'], vista de solo lectura). Con escala=1 y N>1 eso
son 4N objetos en un anillo de 40N: el carro de FABRICA fue escrito para L=40 y 4 objetos (ver INFORME_PISTA.md,
condicion tecnica de la ENMIENDA 1) y ABORTA si ctx['L'] != 40.

INTERFAZ DE CARRO: ver el docstring de carros/FABRICA.py.
  ctx = dict(id, indice, n_linajes, T, L, PAT, rng, dote, rep_umbral, costo, costo_a, rep_X, cupo, ancho,
             fabrica = cfg publica del carro de fabrica (kwargs REL resueltos + L/NK/NKMAX/K/PAT del monolito))
  obs = dict(t, pos, E, Ag, objs, cuerpos, pizarra, yo)
"""
import copy, hashlib, inspect, math, os, sys, importlib.util, types
from collections import deque
import numpy as np

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
ORIGEN = os.path.join(RAIZ, 'experimentos', 'nivel09_cuerpo_nuevo_b2', 'organismo_f9c.py')
SHA_F9C = '9dd1fb91ecec35ae'   # organismo_f9c.py del 21-sep (el que cita organismo_f9c_rapido.py)
CARROS = os.path.join(RAIZ, 'experimentos', 'carrera_escuderias', 'carros')   # pista2: los carros de la carrera, sin copiar
IDX = {'A': 0, 'B': 1, 'C': 2, 'D': 3}
TIPOS = ('A', 'B', 'C', 'D')
OLVIDO = 0.003   # literal del monolito (rng.random()<.003), no es kwarg
N_MAX = 9
CUPO = 16; ANCHO = 8
W_DIAG = 50      # diagnostico: ventana (pasos) tras perder el objetivo bueno
VISTA_ORIG = 20  # la mayor distancia posible en el anillo del monolito (L = 40)
W_CAUSA = 400    # causa de muerte: 'veneno'/'sal' si mordio B/D en los ultimos 400 pasos (= |0.4| / costo)
ETQ = dict(mundo=11, cuerpo=12, hijo=13, muerte=14, pista=15)
MAX_ESCRITURAS_TELEM = 3000   # tope por linaje en la telemetria; la pizarra COMPLETA va en pizarra_log
_CFG = [None]


def h16(p):
    return hashlib.sha256(open(p, 'rb').read()).hexdigest()[:16]


def cfg_fabrica():
    """H-4: la configuracion del carro de fabrica y del mundo, DERIVADA en tiempo de ejecucion de la firma de
    organismo_f9c.run + corre_bloque2.BRAZOS['REL'] (nada escrito a mano). El alma (un invocable) NO viaja:
    se resuelve aqui a su motivo (curita constante 'f')."""
    if _CFG[0] is None:
        dirs = [os.path.join(RAIZ, 'experimentos', d) for d in
                ('nivel09_cuerpo_nuevo_b2', 'nivel09_cuerpo_nuevo', 'nivel13_alma', 'nivel11_mundo_vivo')] + [os.path.join(RAIZ, 'organismo')]
        for d in reversed(dirs):
            if d not in sys.path: sys.path.insert(0, d)
        import corre_bloque2 as CB, organismo_f9c as F9C
        kw = {k: v.default for k, v in inspect.signature(F9C.run).parameters.items() if v.default is not inspect.Parameter.empty}
        kw.update(CB.BRAZOS['REL'])
        alma = kw.pop('alma'); r = alma(None) or {}
        kw['alma_curita'] = r.get('curita', 'f'); kw['alma_motivo'] = str(r.get('motivo', ''))
        _CFG[0] = dict(kw=kw, L=F9C.L, NK=F9C.NK, NKMAX=F9C.NKMAX, K=F9C.K,
                       PAT={k: v.copy() for k, v in F9C.PAT.items()}, VAL_VIVO=dict(F9C.VAL_VIVO), EFECTO=dict(F9C.EFECTO))
    return copy.deepcopy(_CFG[0])


def carga_carro(ident):
    """carros/<ID>.py -> modulo con crea(ctx). Se carga por ruta (no por sys.path) para que nadie tape a nadie."""
    ruta = os.path.join(CARROS, f"{ident}.py")
    if not os.path.exists(ruta):
        raise SystemExit(f"PISTA: no existe el carro {ruta}")
    spec = importlib.util.spec_from_file_location(f"carro_{ident}", ruta)
    mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
    if not hasattr(mod, 'crea'):
        raise SystemExit(f"PISTA: el carro {ident} no define crea(ctx)")
    return mod


class Linaje:
    """El CUERPO en el mundo (fisica + medidas que usan la tabla verdadera). El cerebro es el carro."""

    def __init__(self, i, ident, T, M, rep_acum):
        self.i = i; self.id = ident; self.T = T; self.M = M; self.rep_acum = rep_acum
        self.pos = 0; self.E = 1.0; self.Ag = M['A_ini']; self.prev_on = -1
        self.sobre = {'veneno': [0] * 4, 'comida': [0] * 4, 'agua': [0] * 4, 'sal': [0] * 4}
        self.llegadas = {'veneno': [0] * 4, 'comida': [0] * 4, 'agua': [0] * 4, 'sal': [0] * 4}
        self.mord = {k: [0] * 4 for k in TIPOS}; self.vis = {k: [0] * 4 for k in TIPOS}
        self.deaths = 0; self.mnec = [0, 0]
        self.enc = {k: 0 for k in TIPOS}; self.exp = [{k: None for k in TIPOS} for _ in range(2)]
        self.bxor = [[0] * 4 for _ in range(2)]; self.exor = [[0] * 4 for _ in range(2)]
        self.gv = 0; self.desc = 0; self.pv = 0; self.tdesc = []; self.dq = [0] * 4
        self.bsac = {k: 0 for k in TIPOS}; self.dsac = {k: 0 for k in TIPOS}
        self.tmu = 0; self.vidas = []; self.dreg = 0; self.gv0 = 0
        self.cola = []; self.nac = 0; self.fund = 0; self.dfund = 0; self.dpv = []; self.dv = 0; self.cdes = 0
        self.tfund = []; self.svid = 0; self.esfund = True; self.vh = []; self.org = []
        self.exph = []; self.mordh = []; self.p1 = []; self.c1 = []; self.tok = []
        self.causas = {'hambre': 0, 'sed': 0, 'veneno': 0, 'sal': 0}; self.causa_cuerpo = []
        self.tB = -10 ** 9; self.tD = -10 ** 9
        self.ult_mordida = None; self.escrituras = 0; self.escr = []; self.vetos = 0
        # ENMIENDA 6 (SOLO LECTURA): muerte 'por mordida sabiendo que mata' = muere en el paso en que mordio una letra que su
        # linaje YA habia mordido y cuyo efecto NEGATIVO cae en la necesidad por la que muere (B -> energia, D -> agua)
        self.vol_kk = None; self.muertes_vol = 0
        # DIAGNOSTICO (SOLO LECTURA, sin rng): objetivo bueno de la necesidad activa al inicio del paso, perdidas y mordidas
        self.g = None; self.robos = []; self.perd_olv = []; self.t_bd = []; self.t_ac = []
        self.dg_sum = 0; self.dg_n = 0; self.sin_bueno = 0; self.sin20 = 0
        # MECANISMO (ENMIENDA 4, SOLO LECTURA): mordidas malas A SABIENDAS (letra ya mordida antes por el linaje) cuyo golpe
        # cae en la necesidad MAS LLENA (= la 'limpieza' de O1, medida desde la fisica) y lo bueno que reaparece por ellas
        self.limp = 0; self.limp_buenos = 0; self.malas = 0; self.malas_buenos = 0; self.E0 = 1.0; self.A0 = 1.0
        # HAMBRE -> BOCA (SOLO LECTURA): por (letra, necesidad activa): [decisiones, mordidas, suma deficit en decisiones,
        # suma deficit en mordidas]; histograma del deficit de la necesidad activa en mordidas malas (B/D) y buenas (A/C)
        self.boca = {}; self.hist_bd = [0] * 10; self.hist_ac = [0] * 10; self.lev_bd = []

    def q(self, t): return min(t // (self.T // 4), 3)


def _valida_escritura(x):
    if not isinstance(x, (tuple, list)) or len(x) > ANCHO:
        raise SystemExit(f"PISTA: escritura invalida (tupla de <= {ANCHO} numeros): {x!r}")
    out = []
    for v in x:
        if isinstance(v, (bool, np.bool_)) or not isinstance(v, (int, float, np.integer, np.floating)) or not math.isfinite(float(v)):
            raise SystemExit(f"PISTA: escritura invalida (solo numeros finitos): {x!r}")
        out.append(float(v))
    return tuple(out)


def run(seed, carros, T=100000, pizarra=1, compat=0, rep_acum=0, escala=1, telem=True, diag=1, mundo_n=None, fundador_limpio=0,
        solapadas=0, **kw_conv):
    """carros: lista de IDs (str) de carros/<ID>.py, o de pares (etiqueta, modulo_con_crea).
    escala=1 (ENMIENDA 1): L = 40*N, nobj = 4*N; escala=0: el mundo sin escalar (L=40, nobj=4) para cualquier N.
    mundo_n=M (ENMIENDA 4, MUNDO FORZADO): N carros en el mundo dimensionado para M: L = 40*M, nobj = 4*M y M sorteos de
    olvido por paso (ERR-98). Con M = N (y escala=1) es IDENTICO a mundo_n=None (arnes (N)).
    fundador_limpio=1 (ENMIENDA 5): cuando el linaje se extingue, el fundador es una INSTANCIA NUEVA del carro: crea(ctx) otra vez,
    con el MISMO rng de cuerpo del linaje en el estado en que este (avanzado: lo que la instancia nueva sortee al nacer sale de ahi,
    como el primer fundador de la corrida) y SIN llamar a nace() (el primer fundador tampoco la recibe). Nada del objeto viejo pasa.
    Los hijos de la cola nacen como siempre (nace() con la memoria del padre). Con 0 (por defecto): identico a antes (arnes (O)).
    Devuelve dict(linajes=[dict por linaje], pista=dict, pizarra_log=[...])."""
    if solapadas:   # pista2: generaciones solapadas (motor_convive.py)
        if AQUI not in sys.path: sys.path.insert(0, AQUI)
        import motor_convive as _MC
        return _MC.run_solapadas(seed, carros, T=T, pizarra=pizarra, compat=compat, rep_acum=rep_acum, escala=escala, telem=telem,
                                 diag=diag, mundo_n=mundo_n, fundador_limpio=fundador_limpio, **kw_conv)
    if kw_conv: raise SystemExit(f"PISTA2: opciones de solapadas {sorted(kw_conv)} con solapadas=0")
    n = len(carros)
    if not 1 <= n <= N_MAX: raise SystemExit(f"PISTA: entre 1 y {N_MAX} carros (hay {n})")
    if compat and n != 1: raise SystemExit("PISTA: compat=1 es SOLO el ancla de identidad (un carro)")
    if compat and pizarra: raise SystemExit("PISTA: compat=1 exige pizarra=0 (el ancla es con la pizarra apagada)")
    if rep_acum not in (0, 1): raise SystemExit("PISTA: rep_acum es 0 o 1")
    if compat and fundador_limpio: raise SystemExit("PISTA: compat=1 (el ancla) no admite fundador_limpio (el rng del cuerpo ES el del mundo)")
    CF = cfg_fabrica(); kw = CF['kw']
    VAL_VIVO, EFECTO = CF['VAL_VIVO'], CF['EFECTO']
    if mundo_n is not None and (int(mundo_n) != mundo_n or not 1 <= mundo_n <= N_MAX):
        raise SystemExit(f"PISTA: mundo_n entre 1 y {N_MAX} (hay {mundo_n})")
    esc = int(mundo_n) if mundo_n is not None else (n if escala else 1)
    L = CF['L'] * esc
    M = dict(nobj=kw['nobj'] * esc, costo=kw['costo'], costo_a=kw['costo_a'], A_ini=kw['A_ini'], rep_X=kw['rep_X'],
             rep_umbral=kw['rep_umbral'], dote=kw['dote'], cola_max=kw['cola_max'], rep2_regalo=kw['rep2_regalo'],
             crit_exp=kw['crit_exp'], olvido=OLVIDO)
    mods = []
    for c in carros:
        if isinstance(c, str): mods.append((c, carga_carro(c)))
        else: mods.append(c)
    etiquetas = [e for e, _ in mods]
    ids = [(e if etiquetas.count(e) == 1 else f"{e}#{i}") for i, e in enumerate(etiquetas)]

    SS = lambda i, etq, k: np.random.default_rng([seed, i, ETQ[etq], k])
    if compat:
        rng = np.random.default_rng(seed); rngs_cuerpo = [rng]; rngs_muerte = [rng]; rng_pista = None
        hijo = lambda i, k: np.random.default_rng(700000 + 1000000 * seed + k)
    else:
        rng = SS(0, 'mundo', 0)
        rngs_cuerpo = [SS(i, 'cuerpo', 0) for i in range(n)]
        rngs_muerte = [SS(i, 'muerte', 0) for i in range(n)]
        rng_pista = SS(0, 'pista', 0)
        hijo = lambda i, k: SS(i, 'hijo', k)

    objs = {}; vista = types.MappingProxyType(objs)
    lin = [Linaje(i, ids[i], T, M, rep_acum) for i in range(n)]
    cars = []
    def ctx_de(i):
        return dict(id=ids[i], indice=i, n_linajes=n, T=T, L=L, PAT={k: v.copy() for k, v in CF['PAT'].items()},
                    rng=rngs_cuerpo[i], dote=M['dote'], rep_umbral=M['rep_umbral'], costo=M['costo'],
                    costo_a=M['costo_a'], rep_X=M['rep_X'], cupo=CUPO, ancho=ANCHO, fabrica=cfg_fabrica())
    for i, (e, mod) in enumerate(mods):   # los cerebros nacen ANTES del primer spawn (como en el monolito)
        cars.append(mod.crea(ctx_de(i)))
    instancias = [1] * n
    if rng_pista is not None:
        for l in lin: l.pos = int(rng_pista.integers(L))

    def spawn():
        while len(objs) < M['nobj']:
            x = int(rng.integers(L))
            if x not in objs: objs[x] = TIPOS[int(rng.integers(len(TIPOS)))]
    spawn()

    piz = deque(maxlen=CUPO); piz_t = (); n_escr_desc = 0; piz_log = []
    obs = [dict(yo=ids[i], objs=vista) for i in range(n)]
    tiene_veto = [hasattr(c, 'quiere_parir') for c in cars]
    tiene_vn = [hasattr(c, 'valor_nec') for c in cars]
    orden = list(range(n))
    olv_n = 0
    sin_bueno_mundo = 0                    # SOLO LECTURA (ENMIENDA 4): pasos sin NINGUN objeto bueno (A ni C) en el mundo
    comp = {k: 0 for k in TIPOS}           # SOLO LECTURA: composicion del mundo al inicio de cada paso
    comp_q = [{k: 0 for k in TIPOS} for _ in range(4)]   # idem por cuarto de T (composicion EN EL TIEMPO)
    for t in range(T):
        cq = comp_q[min(t // (T // 4), 3)]
        for v in objs.values(): comp[v] += 1; cq[v] += 1
        if rng_pista is not None and n > 1: orden = [int(z) for z in rng_pista.permutation(n)]
        foto = tuple((l.id, l.pos, objs.get(l.pos), l.ult_mordida) for l in lin)
        if diag:   # SOLO LECTURA: objetivo bueno (A con hambre, C con sed) mas cercano de cada cuerpo, al INICIO del paso
            pA = [x for x, v in objs.items() if v == 'A']; pC = [x for x, v in objs.items() if v == 'C']; pT = list(objs)
            if not pA and not pC: sin_bueno_mundo += 1
            for l in lin:
                hb = min(max(1 - l.E, 0), 1); sd = min(max(1 - l.Ag, 0), 1)
                PP = pC if sd > hb else pA
                if PP:
                    dmin, l.g = min((min((l.pos - x) % L, (x - l.pos) % L), x) for x in PP)
                    l.dg_sum += dmin; l.dg_n += 1
                else:
                    l.g = None; l.sin_bueno += 1
                if min(min((l.pos - x) % L, (x - l.pos) % L) for x in pT) > VISTA_ORIG: l.sin20 += 1
        pend = []
        # ---------------- fase A
        for i in orden:
            l = lin[i]; c = cars[i]; o = obs[i]
            l.E0 = l.E; l.A0 = l.Ag; l.vol_kk = None
            o['t'] = t; o['pos'] = l.pos; o['E'] = l.E; o['Ag'] = l.Ag; o['cuerpos'] = foto; o['pizarra'] = piz_t
            hambre = np.clip(1 - l.E, 0, 1); _dfa = np.clip(1 - l.Ag, 0, 1); _na = 1 if _dfa > hambre else 0
            _sac = l.E >= M['rep_umbral'] and l.Ag >= M['rep_umbral']
            a = c.actua(o)
            mov = int(a.get('mov', 0))
            if mov not in (-1, 0, 1): raise SystemExit(f"PISTA: {l.id} mov={mov} (solo -1, 0, +1)")
            es = a.get('escribe')
            if es is not None:
                if pizarra: pend.append((t, l.id, _valida_escritura(es)))
                else: n_escr_desc += 1
            l.pos = (l.pos + mov) % L; pos = l.pos
            res = dict(t=t, pos=pos, letra=None, mordio=False, dS=None)
            l.ult_mordida = None
            if pos in objs:
                kk = objs[pos]; mordio = bool(a.get('muerde', False)); q = l.q(t)
                if diag:
                    lev = float(_dfa if _na else hambre); bk = l.boca.setdefault(kk + 'HS'[_na], [0, 0, 0.0, 0.0])
                    bk[0] += 1; bk[2] += lev
                    if mordio:
                        bk[1] += 1; bk[3] += lev
                        (l.hist_bd if kk in ('B', 'D') else l.hist_ac)[min(int(lev * 10), 9)] += 1
                        if kk in ('B', 'D'): l.lev_bd.append((t, lev))
                l.vis[kk][q] += 1
                if _sac: l.dsac[kk] += 1
                l.sobre[VAL_VIVO[kk]][q] += 1; l.llegadas[VAL_VIVO[kk]][q] += int(l.prev_on != pos)
                res['letra'] = kk
                if l.prev_on != pos:
                    l.enc[kk] += 1; l.exor[_na][IDX[kk]] += 1
                    l.exph.append([int(t), kk, int(_na), int(mordio)])
                    for _n in range(2):
                        _s0 = EFECTO[VAL_VIVO[kk]][_n]
                        if _s0 and l.exp[_n][kk] is None and tiene_vn[i]:
                            _v0 = float(c.valor_nec(_n, kk))
                            if _v0 * _s0 > 0 and abs(_v0) >= M['crit_exp']: l.exp[_n][kk] = l.enc[kk]
                if mordio:
                    _dS = EFECTO[VAL_VIVO[kk]]; _Rv = [(1.0 if _x > 0 else (-3.0 if _x < 0 else 0.0)) for _x in _dS]
                    l.E = min(l.E + _dS[0], 1.5); l.Ag = min(l.Ag + _dS[1], 1.5); l.bxor[_na][IDX[kk]] += 1
                    l.mord[kk][q] += 1
                    l.mordh.append([int(t), kk, int(_na), float(_Rv[_na])])
                    if _sac: l.bsac[kk] += 1
                    if kk == 'B': l.tB = t
                    elif kk == 'D': l.tD = t
                    l.ult_mordida = kk
                    if kk in ('B', 'D') and sum(l.mord[kk]) > 1: l.vol_kk = kk   # ENMIENDA 6: letra mala YA mordida por el linaje
                    if diag and kk in ('B', 'D'):
                        antes = set(objs); antes.discard(pos)
                        limp = (sum(l.mord[kk]) > 1) and ((l.E0 >= l.A0) if kk == 'B' else (l.A0 >= l.E0))
                    if diag:
                        (l.t_bd if kk in ('B', 'D') else l.t_ac).append(t)
                        for o2 in lin:
                            if o2.g == pos:
                                if o2 is not l: o2.robos.append(t)
                                o2.g = None
                    del objs[pos]; spawn()
                    if diag and kk in ('B', 'D'):
                        nb = sum(1 for x in objs if x not in antes and objs[x] in ('A', 'C'))
                        l.malas += 1; l.malas_buenos += nb
                        if limp: l.limp += 1; l.limp_buenos += nb
                    res['mordio'] = True; res['dS'] = tuple(_dS)
            c.resultado(res)
            l.prev_on = pos if pos in objs else -1
        # ---------------- costos
        for l in lin:
            l.E -= M['costo']; l.Ag -= M['costo_a']
        # ---------------- olvido del mundo: ERR-98 -> esc sorteos por paso (con escala=1, N; si no, 1), cada uno con p=0.003:
        #                  la tasa POR OBJETO es la de L=40 (0.003/4). Con N = 1 es UN sorteo: el monolito exacto.
        olv = []
        for _o in range(esc):
            if rng.random() < M['olvido'] and objs:
                _dx = list(objs)[int(rng.integers(len(objs)))]; del objs[_dx]; spawn(); olv.append(_dx); olv_n += 1
                if diag:
                    for o2 in lin:
                        if o2.g == _dx: o2.perd_olv.append(t); o2.g = None
        olv = tuple(olv)
        # ---------------- fase B
        for i in orden:
            l = lin[i]; c = cars[i]
            c.fin_paso(dict(t=t, olvido=olv))
            if l.E <= 0 or l.Ag <= 0:
                por_E = l.E <= 0
                _causa = ('energia' if por_E else 'agua')
                cz = (('veneno' if t - l.tB < W_CAUSA else 'hambre') if por_E else ('sal' if t - l.tD < W_CAUSA else 'sed'))
                l.causas[cz] += 1
                if l.vol_kk == ('B' if por_E else 'D'): l.muertes_vol += 1   # ENMIENDA 6: la mordida de ESTE paso lo mato
                if len(l.causa_cuerpo) < 2000: l.causa_cuerpo.append(cz)
                l.deaths += 1; l.mnec[0 if por_E else 1] += 1; l.E = .6; l.Ag = .6
                l.pos = int(rngs_muerte[i].integers(L))
                if rep_acum: l.gv = 0
                l.svid += t - l.tmu; l.vh.append(t - l.tmu); l.org.append(int(not l.esfund)); l.dpv.append(l.dv); l.dv = 0
                c.muere(dict(t=t, causa=_causa, causa_juez=cz, edad=l.vh[-1], hijos=l.dpv[-1]))
                # F9: p1/c1/t_ok del cuerpo que muere (usan la tabla verdadera: son del JUEZ, no del carro)
                _mal9 = [x for x in l.exph if x[1] == ('B' if x[2] == 0 else 'D')]
                _bue9 = [x for x in l.exph if x[1] == ('A' if x[2] == 0 else 'C')]
                l.p1.append(1 - int(_mal9[0][3]) if _mal9 else -1)
                l.c1.append(int(_bue9[0][3]) if _bue9 else -1)
                _ok9 = [x for x in l.mordh if x[3] > 0]
                l.tok.append(int(_ok9[0][0] - l.tmu) if _ok9 else -1)
                l.exph.clear(); l.mordh.clear()
                l.nac += 1
                if l.nac >= 100000: raise SystemExit('H1: mas de 100000 partos: la semilla del hijo colisionaria (ERR-60)')
                _m = (l.cola.pop(0) if l.cola else None)
                l.esfund = _m is None
                if l.esfund:
                    l.fund += 1
                    if len(l.tfund) < 200: l.tfund.append(t)
                l.E = (_m['dote'] if _m is not None else M['dote']); l.Ag = l.E; l.prev_on = -1
                l.tB = l.tD = -10 ** 9
                if l.esfund and fundador_limpio:   # ENMIENDA 5: instancia NUEVA, sin nada del objeto viejo; sin nace()
                    cars[i] = mods[i][1].crea(ctx_de(i)); c = cars[i]; instancias[i] += 1
                else:
                    c.nace(dict(t=t, k=l.nac, fundador=l.esfund, memoria=(_m['mem'] if _m is not None else None),
                                rng_hijo=hijo(i, l.nac)))
                if len(l.vidas) < 400: l.vidas.append(t - l.tmu)
                l.tmu = t
            # ventana de viabilidad (reproduccion)
            if l.E >= M['rep_umbral'] and l.Ag >= M['rep_umbral']:
                if l.gv == 0: l.gv0 = t
                l.gv += 1; l.pv += 1
            else: l.gv = (l.gv if rep_acum else 0)
            if l.gv >= M['rep_X']:
                if tiene_veto[i] and not c.quiere_parir(dict(t=t, E=l.E, Ag=l.Ag, cola=len(l.cola))):
                    l.gv = 0; l.vetos += 1
                else:
                    l.desc += 1; l.dq[l.q(t)] += 1; l.gv = 0
                    if l.gv0 - l.tmu < M['rep2_regalo']: l.dreg += 1
                    if len(l.tdesc) < 200: l.tdesc.append(t)
                    l.dv += 1
                    l.E -= M['dote']; l.Ag -= M['dote']
                    if l.esfund and l.gv0 - l.tmu < M['rep2_regalo']: l.dfund += 1
                    if len(l.cola) >= M['cola_max']: l.cola.pop(0); l.cdes += 1
                    l.cola.append(dict(dote=M['dote'], mem=c.al_parir(dict(t=t, k=l.desc))))
        # ---------------- pizarra
        if pend:
            for e in pend:
                piz.append(e); piz_log.append([e[0], e[1], list(e[2])])
                le = lin[ids.index(e[1])]; le.escrituras += 1
                if telem and len(le.escr) < MAX_ESCRITURAS_TELEM: le.escr.append([e[0], list(e[2])])
            piz_t = tuple(piz)

    # ---------------------------------------------------------------- salida (ERR-96: fisica ARRIBA, carro en d['carro'])
    out = []
    for i, l in enumerate(lin):
        c = cars[i]
        d = dict(sobre=l.sobre, llegadas=l.llegadas, mord=l.mord, vis=l.vis, deaths=l.deaths,
                 estims=list(TIPOS), agua=round(float(l.Ag), 3), muertes_nec=list(l.mnec),
                 exp_hasta=[dict(l.exp[_n]) for _n in range(2)], exposiciones=dict(l.enc),
                 xor_mord=[list(l.bxor[_n]) for _n in range(2)], xor_enc=[list(l.exor[_n]) for _n in range(2)],
                 descendientes=l.desc, pasos_viables=l.pv, desc_q=list(l.dq), t_desc=list(l.tdesc),
                 sac_mord=dict(l.bsac), sac_dec=dict(l.dsac),
                 rep=dict(mide=1, X=M['rep_X'], umbral=M['rep_umbral'], coste=0.0, nec=0, cuello=None),
                 desc_regalo=l.dreg, vidas=list(l.vidas), vida_final=T - l.tmu, rep2=dict(regalo=M['rep2_regalo']),
                 muerte_real=1, dote=M['dote'], nacimientos=l.nac, fundadores=l.fund, desc_fund=l.dfund,
                 desc_por_vida=list(l.dpv) + [l.dv], vidas_h1=list(l.vh) + [T - l.tmu],
                 origen_cuerpo=list(l.org) + [int(not l.esfund)], suma_vidas=l.svid, cola_final=len(l.cola),
                 cola_desborde=l.cdes, t_fund=list(l.tfund),
                 h1=dict(cola_max=M['cola_max'], sem_hijo=('700000+1000000*seed+k' if compat else '[seed,i,13,k]'),
                         sem_baraja='800000+1000000*seed'),
                 T_efectivo=T, vidas_cuerpo=[int(x) for x in l.vh], desc_cuerpo=[int(x) for x in l.dpv])
        if rep_acum: d['rep_acum'] = 1
        d['_carrera'] = dict(id=l.id, indice=i, causas=dict(l.causas), causa_cuerpo=list(l.causa_cuerpo),
                             escrituras=l.escrituras, escr=l.escr, vetos=l.vetos, instancias=instancias[i], muertes_vol=l.muertes_vol,
                             p1=[int(x) for x in l.p1], c1=[int(x) for x in l.c1], t_ok=[int(x) for x in l.tok])
        if diag: d['_carrera']['diag'] = _diag(l, T)
        d['carro'] = dict(c.salida()) if hasattr(c, 'salida') else {}   # ERR-96: SOLO aqui; nadie lo lee como verdad
        out.append(d)
    return dict(linajes=out, pizarra_log=piz_log,
                pista=dict(seed=seed, T=T, n=n, ids=ids, compat=int(compat), pizarra=int(pizarra),
                           rep_acum=int(rep_acum), escala=int(escala), L=L, nobj=M['nobj'], olvidos=olv_n, mundo_n=mundo_n,
                           fundador_limpio=int(fundador_limpio),
                           frac_sin_bueno_mundo=(round(sin_bueno_mundo / T, 4) if diag else None),
                           comp_mundo={k: round(comp[k] / T, 4) for k in TIPOS},
                           comp_mundo_q=[{k: round(cq[k] / max(1, (T // 4 if j < 3 else T - 3 * (T // 4))), 4) for k in TIPOS}
                                         for j, cq in enumerate(comp_q)],
                           escrituras_descartadas=n_escr_desc, pizarra_n=len(piz_log),
                           pizarra_final=[[e[0], e[1], list(e[2])] for e in piz],
                           rng_mundo_estado=_estado(rng)))


# claves de primer nivel de un linaje que son del JUEZ/pista y NO del monolito
NO_MONOLITO = ('_carrera', 'carro')


def plano(d):
    """Vista PLANA de un linaje con las claves del monolito (SOLO para el arnes de identidad): fisica + lo del
    carro, sin que el carro pise NADA (si una clave del carro choca con una fisica, aborta). f9 = lo del carro
    (nodo, lecturas, pa/pn) + p1/c1/t_ok de la pista; rep['cuello'] = el eco del carro."""
    fis = {k: v for k, v in d.items() if k not in NO_MONOLITO}
    car = dict(d['carro']); rc = car.pop('_rep_cuello', None); f9 = car.pop('f9', None)
    choque = [k for k in car if k in fis]
    if choque: raise SystemExit(f"PLANO: el carro devolvio claves FISICAS {choque} (ERR-96)")
    p = dict(fis); p.update(car)
    p['rep'] = dict(fis['rep'], cuello=rc)
    if f9 is not None:
        f9 = dict(f9); f9.update(p1=d['_carrera']['p1'], c1=d['_carrera']['c1'], t_ok=d['_carrera']['t_ok']); p['f9'] = f9
    return p


def _diag(l, T):
    """Diagnostico de 'por que un cuerpo rodeado muerde mas B/D' (SOLO LECTURA). Para cada perdida del objetivo
    bueno (ROBO: otro cuerpo se lo comio en el mismo paso; OLVIDO: el mundo lo retiro), cuantas mordidas de B/D y
    de A/C hace el cuerpo en los W_DIAG pasos siguientes, contra su tasa de base (mordidas / T * W_DIAG)."""
    import bisect
    def ventana(ts, ev):
        if not ev: return None
        return round(sum(bisect.bisect_right(ts, e + W_DIAG) - bisect.bisect_right(ts, e) for e in ev) / len(ev), 4)
    return dict(W=W_DIAG, robos=len(l.robos), perdidas_olvido=len(l.perd_olv),
                bd_tras_robo=ventana(l.t_bd, l.robos), ac_tras_robo=ventana(l.t_ac, l.robos),
                bd_tras_olvido=ventana(l.t_bd, l.perd_olv), ac_tras_olvido=ventana(l.t_ac, l.perd_olv),
                bd_base=round(len(l.t_bd) / T * W_DIAG, 4), ac_base=round(len(l.t_ac) / T * W_DIAG, 4),
                dist_bueno_media=(round(l.dg_sum / l.dg_n, 3) if l.dg_n else None),
                frac_sin_bueno=round(l.sin_bueno / T, 4), frac_sin_obj20=round(l.sin20 / T, 4),
                limpiezas=l.limp, limpiezas_por_cuerpo=round(l.limp / (len(l.vh) + 1), 4), buenos_por_limpieza=l.limp_buenos,
                mordidas_malas=l.malas, buenos_por_mala=l.malas_buenos, **_boca(l, T))


def _boca(l, T):
    """HAMBRE -> BOCA (SOLO LECTURA). Tasa de mordida por decision de boca, por (letra, necesidad activa: H hambre, S sed),
    y el deficit medio de la necesidad activa cuando decide y cuando muerde. Y si los ROBOS anteceden a las mordidas malas:
    fraccion de mordidas B/D con un robo en los W_DIAG pasos previos, contra la fraccion de TODOS los pasos cubiertos asi."""
    import bisect
    tab = {k: dict(dec=v[0], mord=v[1], tasa=round(v[1] / v[0], 4) if v[0] else None,
                   def_dec=round(v[2] / v[0], 4) if v[0] else None, def_mord=round(v[3] / v[1], 4) if v[1] else None)
           for k, v in sorted(l.boca.items())}
    rb = l.robos
    def con_robo(t): i = bisect.bisect_left(rb, t); return i > 0 and t - rb[i - 1] <= W_DIAG
    cub = 0; fin = -1
    for r in rb:
        a, b = max(r + 1, fin + 1), min(r + W_DIAG, T - 1)
        if b >= a: cub += b - a + 1; fin = b
    bd_r = [lev for t, lev in l.lev_bd if con_robo(t)]; bd_n = [lev for t, lev in l.lev_bd if not con_robo(t)]
    return dict(boca=tab, hist_def_bd=list(l.hist_bd), hist_def_ac=list(l.hist_ac),
                bd_con_robo_prev=(round(len(bd_r) / len(l.lev_bd), 4) if l.lev_bd else None),
                pasos_con_robo_prev=round(cub / T, 4),
                def_bd_con_robo=(round(sum(bd_r) / len(bd_r), 4) if bd_r else None),
                def_bd_sin_robo=(round(sum(bd_n) / len(bd_n), 4) if bd_n else None))


def _estado(r):
    s = r.bit_generator.state
    return hashlib.sha256(repr(s).encode()).hexdigest()[:16]
