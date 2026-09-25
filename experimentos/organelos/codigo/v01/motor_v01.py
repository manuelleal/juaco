# motor_v01.py: CONSTRUIDO por v01/construye_v01.py desde exploracion_fable/motor_fable.py (sha 46750da69ef8cce1). NO EDITAR A MANO.
# motor_fable.py: CONSTRUIDO por construye_fable.py desde motor_codigo.py (sha dd0051a348f93c6e). NO EDITAR A MANO.
"""motor_codigo.py (CONSTRUIDO por experimentos/organelos/codigo/construye_codigo.py desde experimentos/organelos/gramatica/motor_gramatica.py, sha 6b65dc5e32093424; NO editar a mano).
CODIGO v0: + LA CINTA (codigo_def.py): el cuerpo DESARROLLA su cinta al nacer y el parto la COPIA con errores que la propia cinta regula (TASA, SOS); + el mundo que CAMBIA (eco['cambio']). Con codigo=None y cambio=None es motor_gramatica BIT A BIT.

motor_gramatica.py (CONSTRUIDO por experimentos/organelos/gramatica/construye_gramatica.py desde experimentos/juaco_eco/motor_eco2.py, sha 0921ee3a50ce7f7a; NO editar a mano).
ORGANELOS: + la GRAMATICA del organo de transmision (G1-G4, ver construye_gramatica.py). Con eco['gramatica'] = None es motor_eco2 BIT A BIT. Lo que sigue es el docstring del origen.

motor_eco2.py (CONSTRUIDO por experimentos/juaco_eco/construye_eco_org.py desde motor_eco.py, sha bca3033878b59622; NO editar a mano). ECO v2: + los genes de organo ensena y filtra0 al final del genoma
(rasgos con umbral: se expresan si valen >= UMBRAL_ORG). Lo que sigue es el docstring del origen.

motor_eco.py (CONSTRUIDO por experimentos/juaco_eco/construye_eco.py desde experimentos/generaciones/motor_convive.py,
sha d10cb9021f5d0f41; NO editar a mano). JUACO-ECO: con eco=None es motor_convive BIT A BIT; con eco=dict(...) agrega
E1-E8 (ver construye_eco.py). Lo que sigue es el docstring del origen.

motor_convive.py — PISTA v2 CON GENERACIONES SOLAPADAS (pista2.run(..., solapadas=1)).

MISION: llegar a la AGI por este camino.

Pedido del director (22-sep): un mundo donde las generaciones CONVIVAN. En la pista v1 hay UN cuerpo vivo por linaje y
el hijo espera en una cola hasta que muere el padre; para que haya generaciones el padre tiene que morir (ERR-102).

EL MUNDO ES EL MISMO: L = 40*esc, nobj = 4*esc, esc sorteos de olvido por paso (ERR-98), mismos objetos, mismos
efectos, mismos costos (0.001 por necesidad y paso), ventana de reproduccion (E y Ag >= 1.0 durante 500 pasos), dote 0.6.
Con esc = numero de linajes fundadores (9 en monocultivo: L = 360, 36 objetos), FIJO durante toda la corrida.

REGLAS NUEVAS (las unicas):
 P1 PARTO REAL. Cuando un cuerpo completa la ventana (y no la veta con quiere_parir), paga la dote (E -= 0.6, Ag -= 0.6)
    y el hijo NACE EN ESE PASO como cuerpo vivo, en la MISMA CELDA del padre (sin rng), con E = Ag = dote. No hay cola.
    Actua desde el paso siguiente (como el cuerpo que nacia de la cola en v1). Pueden vivir a la vez varios cuerpos del
    mismo linaje.
 P2 CEREBRO POR CUERPO. Cada cuerpo es una INSTANCIA del carro: crea(ctx) con su propio rng de cuerpo
    [seed, linaje, 12, k] (k = numero de cuerpo en el linaje, k >= 1) y en seguida nace(info) con
    info = dict(t, k, fundador=False, memoria=<lo que devolvio al_parir del padre>, rng_hijo=[seed, linaje, 13, k], padre).
    La herencia viaja SOLO por al_parir/nace (lo que el carro declara). ctx['id'] = '<linaje>/<k>' (unico por cuerpo).
 P3 EXTINCION. Si muere el ULTIMO cuerpo vivo de un linaje, el mundo pone un FUNDADOR LIMPIO (ENMIENDA 5): instancia nueva
    crea(ctx) con el rng de fundadores del linaje [seed, linaje, 12, 0] (el mismo de v1), SIN nace(), posicion del rng de
    muerte del linaje [seed, linaje, 14, 0], E = Ag = dote, id = el del linaje. Toma el LUGAR del muerto en la lista de
    turno (con eso, sin partos, v2 == v1 con fundador_limpio=1 BIT A BIT: arnes (S)). Se cuenta como fundador.
 P4 CAPACIDAD DE CARGA: NINGUN tope de cuerpos por linaje. La densidad la regulan los recursos: la comida y el agua son
    los mismos 4*esc objetos (el mundo repone al azar lo que se muerde y olvida); con mas cuerpos cada uno llega a menos
    objetos buenos, tarda mas en juntar 500 pasos saciado (menos partos) y muere mas (dependencia de la densidad).
    TOPE DE SEGURIDAD COMPUTACIONAL (declarado, no biologico): tope_cuerpos (por defecto 300) cuerpos vivos EN TODA LA
    PISTA. Al alcanzarlo, una ventana completa NO produce hijo: no se paga la dote, la ventana se reinicia y se cuenta
    en 'bloqueados' (por linaje) y 't_tope' (primer paso con el tope alcanzado). Si bloqueados > 0 la corrida queda
    MARCADA: la densidad no la regulo el mundo.
 P5 quiere_parir(info): info['cola'] = cuerpos vivos del linaje SIN contar al que pare (la 'reserva viva': en v1 la cola
    era la reserva de hijos del linaje; en v2 esa reserva esta viva en el mundo). Tambien vivos_linaje y hijos_vivos
    (hijos vivos de ESE cuerpo). Asi la muerte programada de O3 (TERMINAL, cola_est >= 4) y O4 (senescencia, cola >= 6)
    sigue disponible con la misma letra.
 P7 REPOSICION DEL MUNDO (opcion reposicion; MEDIDO en el humo de 10001, T=5000: con la regla de v1 NO hay capacidad de
    carga para quien limpia: 9 O2 pasan de 9 a 128 cuerpos y siguen creciendo; ver INFORME_CONVIVE.md):
    'inmediata' = v1: lo mordido u olvidado se repone AL INSTANTE con una letra al azar. Cada mordida de B/D fabrica
       ~0.5 objetos buenos: limpiar es una bomba de energia y el flujo de comida CRECE con el numero de cuerpos.
    'fija' (por defecto con solapadas=1) = QUIMIOSTATO: lo mordido u olvidado desaparece y el mundo repone a tasa FIJA
       r = r_rep * esc objetos por paso (r_rep = 0.03: la reposicion medida del mundo SOLO de v1 con un FABRICA,
       0.0316 por paso en 10001-10004, T=20000), a lo sumo 1 objeto pendiente (banco <= 1 + r) y hasta nobj objetos,
       en celda libre al azar con letra al azar (rng del mundo). Piso: si un paso deja el mundo SIN objetos, se pone uno
       al instante (los carros de v1 no estan escritos para un mundo vacio; se cuenta en 'pisos'). Con demanda < r
       el mundo es casi el de v1; con demanda > r el flujo de comida queda FIJO -> capacidad de carga
       K <= (r/2 * 0.8) / 0.001 por necesidad (~54 cuerpos con esc = 9, cota sin perdidas).
 P6 turno: permutacion nueva cada paso sobre los cuerpos vivos (rng de la pista [seed, 0, 15, 0], como v1).
    Lista de turno: vivos en su orden + nacidos en el paso al final; un fundador ocupa el lugar del muerto.

NO SE PORTAN (declarado): compat=1, diag=1 (el diagnostico de robos/boca de v1), exposiciones/xor/p1/c1 (telemetria F9).
El clasificador fisico de muertes voluntarias (ENMIENDA 6) se conserva, pero NO discrimina (ERR-103): la cifra que vale
es la DECLARADA por el carro (VOL_DECL: O3 'cuerpos_term', O4 'senescentes'), leida de salida() de la instancia al morir.

SALIDA: dict(linajes=[...], pista=..., pizarra_log=[...]). Por linaje, en primer nivel SOLO fisica (ERR-96):
individuos = [[k, gen, padre, t_nace, t_muere(-1 si vive en T), hijos, fundador, causa, vol_decl], ...]; tam = cuerpos vivos
del linaje cada MUESTRA pasos (al inicio del paso; mas el valor final). Lo del carro va en d['carro'].
"""
import math, os, sys, types
import numpy as np

_V01 = os.path.dirname(os.path.abspath(__file__))   # v0.1 (V0)
_FABLE = os.path.join(os.path.dirname(_V01), 'exploracion_fable')   # FABLE (F0): fable_mundos se IMPORTA de alli, sin copiar
if _FABLE not in sys.path: sys.path.insert(0, _FABLE)
AQUI = os.path.dirname(_V01)   # la carpeta codigo/
if AQUI not in sys.path: sys.path.insert(0, AQUI)

MUESTRA = 100
TOPE_DEF = 300
R_REP = 0.03     # P7: objetos por paso y por unidad de escala (mundo SOLO de v1: 0.0316 medido)

# ============================================================================ JUACO-ECO (E1-E8; solo con eco=dict)
GEN = os.path.join(os.path.dirname(os.path.dirname(AQUI)), 'generaciones')      # pista2 (mundo de la pista v2), solo se LEE
if GEN not in sys.path: sys.path.insert(1, GEN)
CARROS_ECO = os.path.join(AQUI, 'carros')
ECO_NMAX = 400        # linajes fundadores
ECO_ESC_MAX = 2000    # escala del mundo (L = 40*esc)
ETQ_MUT = 16; ETQ_SOMBRA = 17
# GENES: (nombre, destino, entero, piso_duro, techo_duro). Rango efectivo = [max(piso, G0/4), min(techo, 4*G0)].
# destino 'kw' = perilla del cerebro (ctx['fabrica']['kw']); 'NK' = celdas de Kenyon activas al nacer (estructura);
# 'dote'/'rep_umbral'/'rep_X' = historia de vida (la pista las aplica al cuerpo).
GENES = (('eta', 'kw', 0, 1e-4, 1.0), ('tau_e', 'kw', 0, 0.05, 0.99), ('alpha', 'kw', 0, 0.01, 20.0),
         ('hambre_boca', 'kw', 0, 0.01, 20.0), ('aversion', 'kw', 0, 0.01, 20.0), ('ema', 'kw', 0, 1e-3, 0.5),
         ('paso', 'kw', 0, 1e-3, 2.0), ('lam', 'kw', 0, 1e-3, 0.5), ('memoria_rechazo', 'kw', 1, 1, 200),
         ('eta_s', 'kw', 0, 1e-3, 2.0), ('clip_s', 'kw', 0, 0.5, 50.0), ('del_s', 'kw', 0, 0.01, 1.0),
         ('del_c', 'kw', 0, 0.01, 1.0), ('ema_c', 'kw', 0, 1e-3, 0.5), ('NK', 'NK', 1, 6, 90),
         ('dote', 'dote', 0, 0.15, 1.2), ('rep_umbral', 'rep_umbral', 0, 0.5, 1.45), ('rep_X', 'rep_X', 1, 100, 2000),
         ('ensena', 'kw', 0, 0.05, 10.0), ('filtra0', 'kw', 0, 0.05, 10.0))   # ECO v2: ORGANOS COMO GENES (umbral UMBRAL_ORG)
ORG_G0 = {'ensena': 0.9, 'filtra0': 0.9}   # ECO v2: los organos nacen APAGADOS (0.9 < UMBRAL_ORG)
UMBRAL_ORG = 1.0
NOMBRES = tuple(g[0] for g in GENES)
I_DOTE = NOMBRES.index('dote'); I_RU = NOMBRES.index('rep_umbral'); I_RX = NOMBRES.index('rep_X')
ECO_DEF = dict(refunda=1, p_mut=0.0, sigma=0.15, genoma=None, n_sombra=0, cada_gen=0, ckpt_cada=0, ckpt_fn=None,
               estado=None, ind_cb=None, mutables=None, banco=0, donante='padre', t_corte=None,
               gramatica=None, g_pcampo=0.0, g_pdup=0.0, g_pdel=0.0, g_tope=4, g_alfabeto=None,
               codigo=None, c_on=True, c_sos=True, cambio=None)   # CODIGO v0 (C1, C4)   # ORGANELOS (G1)
ETQ_BANCO = 18; ETQ_DONANTE = 19
ETQ_GMUT = 20; ETQ_GSOMBRA = 21   # ORGANELOS: rng de los errores de copia de la gramatica (real y sombras); 22 = fundadores (runner)
import gramatica_def as GD
import codigo_def as CD   # CODIGO v0
import fable_mundos as FB   # FABLE
ETQ_CMUT = 23   # CODIGO: rng de los errores de copia de la cinta
ENTEROS = tuple(g[2] for g in GENES)
# VIVERO (E9, solo con refunda=1 y t < t_corte): si un linaje se extingue, el mundo pone un fundador cuyo genoma sale del
# BANCO (anillo de los ultimos `banco` genomas DONANTES de un parto), mutado; banco vacio -> genoma inicial del linaje.
# Desde t_corte: refunda = 0 (nadie pone nada; si todo muere, muere). donante='padre': el hijo copia el genoma del padre
# (seleccion natural; el banco guarda el genoma del PADRE en cada parto). donante='azar' (control 'mutacion sin seleccion'):
# el genoma de TODO cuerpo nuevo (hijo o fundador) sale de una entrada AL AZAR del banco, mutada, y el banco guarda el genoma
# NUEVO al crearse: el genoma nunca influye en su propia copia (ni por fertilidad ni por viabilidad). Candidato a ERR (humo
# exploratorio del 23-sep): la primera version del control copiaba el genoma de un cuerpo VIVO al azar, y eso es seleccion
# por viabilidad (el que vive mas dona mas): alpha subio +0.39 tambien en ese 'control'. El banco arranca con los fundadores.


def genoma0(CF):
    """G0 = los valores de fabrica (ctx), en el orden de GENES."""
    kw = CF['kw']; v = []
    for nom, dest, ent, lo, hi in GENES:
        v.append(float(CF['NK'] if dest == 'NK' else (kw[nom] if nom in kw else ORG_G0[nom])))   # ECO v2: organos fuera del ctx de fabrica
    return np.array(v, float)


def rangos(G0):
    lo = np.array([max(g[3], G0[j] / 4) for j, g in enumerate(GENES)]); hi = np.array([min(g[4], G0[j] * 4) for j, g in enumerate(GENES)])
    return lo, hi


def muta(g, r, p, sigma, lo, hi):
    """Mutacion log-normal por gen con probabilidad p[j] (0 en los genes no mutables). Consume SIEMPRE 2*NG numeros."""
    NG = len(g); u = r.random(NG); z = r.normal(0.0, sigma, NG); h = g.copy(); nm = 0
    for j in range(NG):
        if u[j] < p[j]:
            v = h[j] * math.exp(z[j])
            if GENES[j][2]:
                v = float(round(v))
                if v == h[j]: v = h[j] + (1.0 if z[j] > 0 else -1.0)
            v = min(max(v, lo[j]), hi[j])
            nm += int(v != h[j]); h[j] = v
    return h, nm


def carga_eco(ident):
    """carro por ruta: primero juaco_eco/carros, luego los de la carrera. Se REGISTRA en sys.modules (pickle del checkpoint)."""
    import importlib.util
    ruta = os.path.join(CARROS_ECO, f"{ident}.py")
    if not os.path.exists(ruta):
        import pista2 as P
        ruta = os.path.join(P.CARROS, f"{ident}.py")
    if not os.path.exists(ruta): raise SystemExit(f"ECO: no existe el carro {ident}")
    nom = f"carro_eco_{ident}"
    if nom in sys.modules: return sys.modules[nom]
    spec = importlib.util.spec_from_file_location(nom, ruta); mod = importlib.util.module_from_spec(spec)
    sys.modules[nom] = mod; spec.loader.exec_module(mod)
    if not hasattr(mod, 'crea'): raise SystemExit(f"ECO: el carro {ident} no define crea(ctx)")
    return mod


def _eco_cfg(eco, CF, n):
    mal = set(eco) - set(ECO_DEF)
    if mal: raise SystemExit(f"ECO: claves desconocidas en eco: {sorted(mal)}")
    E_ = dict(ECO_DEF); E_.update(eco)
    if E_['refunda'] not in (0, 1): raise SystemExit("ECO: refunda 0 o 1")
    if not 0.0 <= float(E_['p_mut']) <= 1.0: raise SystemExit("ECO: p_mut en [0, 1]")
    G0 = genoma0(CF); E_['G0'] = G0; E_['lo'], E_['hi'] = rangos(G0)
    mut = NOMBRES if E_['mutables'] is None else tuple(E_['mutables'])
    if set(mut) - set(NOMBRES): raise SystemExit(f"ECO: genes desconocidos {sorted(set(mut) - set(NOMBRES))}")
    E_['pv'] = np.array([float(E_['p_mut']) if nm_ in mut else 0.0 for nm_ in NOMBRES])
    if E_['donante'] not in ('padre', 'azar'): raise SystemExit("ECO: donante 'padre' o 'azar'")
    if not (isinstance(E_['banco'], int) and E_['banco'] >= 0): raise SystemExit("ECO: banco entero >= 0")
    if E_['t_corte'] is not None and not E_['refunda']: raise SystemExit("ECO: t_corte exige refunda=1 (vivero)")
    g = E_['genoma']
    if g is None: gs = [G0.copy() for _ in range(n)]
    else:
        a = np.asarray(g, float)
        if a.ndim == 1: a = np.tile(a, (n, 1))
        if a.shape != (n, len(GENES)): raise SystemExit(f"ECO: genoma con forma {a.shape}; se espera ({n}, {len(GENES)})")
        gs = [a[i].copy() for i in range(n)]
        for x in gs:
            if (x < E_['lo'] - 1e-12).any() or (x > E_['hi'] + 1e-12).any(): raise SystemExit("ECO: genoma fuera de rango")
    E_['gs0'] = gs
    if E_['gramatica'] is None: E_['gr0'] = None   # ORGANELOS (G1)
    else:
        _tp = int(E_['g_tope'])
        if not 1 <= _tp <= 8: raise SystemExit('GRAMATICA: g_tope entre 1 y 8')
        _grs = list(E_['gramatica'])
        if len(_grs) != n: raise SystemExit(f'GRAMATICA: {len(_grs)} gramaticas para {n} fundadores')
        E_['gr0'] = [GD.valida(x, _tp) for x in _grs]
        E_['g_alf'] = GD.ALFABETO_TODO if E_['g_alfabeto'] is None else tuple(tuple(int(v) for v in a) for a in E_['g_alfabeto'])
        E_['g_on'] = float(E_['g_pcampo']) > 0 or float(E_['g_pdup']) > 0 or float(E_['g_pdel']) > 0
    E_['cod0'] = None   # CODIGO v0 (C1)
    if E_['codigo'] is not None:
        if E_['gramatica'] is not None: raise SystemExit('CODIGO: con codigo la gramatica la DESARROLLA la cinta (gramatica=None)')
        if float(E_['p_mut']) != 0.0 or int(E_['n_sombra']) != 0: raise SystemExit('CODIGO: con codigo, p_mut = 0 y n_sombra = 0')
        _cs = list(E_['codigo'])
        if len(_cs) != n: raise SystemExit(f'CODIGO: {len(_cs)} cintas para {n} fundadores')
        E_['cod0'] = [CD.valida(c) for c in _cs]; _tp = int(E_['g_tope'])
        E_['g_alf'] = GD.ALFABETO_TODO if E_['g_alfabeto'] is None else tuple(tuple(int(v) for v in a) for a in E_['g_alfabeto']); E_['g_on'] = False
        _dv = [CD.desarrolla(c, G0, E_['lo'], E_['hi'], ENTEROS) for c in E_['cod0']]
        E_['gs0'] = [d[0] for d in _dv]; E_['gr0'] = [GD.valida(d[1], _tp) for d in _dv]
    if isinstance(E_['cambio'], dict): FB.valida(E_['cambio'])   # FABLE (F1)
    elif E_['cambio'] is not None:   # CODIGO v0 (C4)
        _c = tuple(E_['cambio'])
        if len(_c) != 3 or _c[1] == _c[2] or _c[1] not in 'ABCD' or _c[2] not in 'ABCD' or int(_c[0]) < 0: raise SystemExit('CODIGO: cambio = (t, X, Y)')
    return E_


def ctx_genoma(d, g):
    """Aplica el genoma g al ctx d (in situ). Con g == G0 el ctx queda IGUAL al de fabrica (arnes (E))."""
    kw = d['fabrica']['kw']
    for j, (nom, dest, ent, lo, hi) in enumerate(GENES):
        v = int(round(g[j])) if ent else float(g[j])
        if dest == 'kw': kw[nom] = v
        elif dest == 'NK': d['fabrica']['NK'] = v
        else: d[dest] = v; kw[dest] = v
    return d


VOL_DECL = {'O3': 'cuerpos_term', 'O4': 'senescentes', 'CTRL_O3_SINTERM': 'cuerpos_term'}   # muerte programada DECLARADA por el carro (bitacoras)
CAUSAS = ('hambre', 'sed', 'veneno', 'sal')


class Cuerpo:
    __slots__ = ('lin', 'k', 'gen', 'padre', 'tn', 'c', 'id', 'obs', 'pos', 'E', 'Ag', 'gv', 'gv0', 'tB', 'tD',
                 'ult_mordida', 'vol_kk', 'hijos', 'fund', 'vivo', 'hvivos', 'pc', 'g', 's', 'gr', 'gs', 'cin', 'mb')   # ORGANELOS: gr, gs; CODIGO: cin, mb

    def __init__(self, lin, k, gen, padre, tn, c, ident, vista, pos, E, fund, pc=None):
        self.lin = lin; self.k = k; self.gen = gen; self.padre = padre; self.tn = tn; self.c = c; self.id = ident
        self.obs = dict(yo=ident, objs=vista); self.pos = pos; self.E = E; self.Ag = E
        self.gv = 0; self.gv0 = 0; self.tB = -10 ** 9; self.tD = -10 ** 9; self.ult_mordida = None; self.vol_kk = None
        self.hijos = 0; self.fund = fund; self.vivo = True; self.hvivos = 0; self.pc = pc; self.g = None; self.s = None   # pc = cuerpo padre (vivo o no)
        self.gr = None; self.gs = None   # ORGANELOS: gramatica real y sombras
        self.cin = None; self.mb = None   # CODIGO v0 (C2): la cinta y las ultimas 20 mordidas (1 = mala)


class LinajeV2:
    def __init__(self, i, ident, T, etiqueta):
        self.i = i; self.id = ident; self.T = T; self.etq = etiqueta
        self.mord = {k: [0] * 4 for k in 'ABCD'}; self.vis = {k: [0] * 4 for k in 'ABCD'}
        self.deaths = 0; self.mnec = [0, 0]; self.causas = {k: 0 for k in CAUSAS}; self.muertes_vol = 0
        self.fund = 0; self.tfund = []; self.desc = 0; self.nac = 0; self.vetos = 0; self.bloq = 0
        self.escrituras = 0; self.escr = []; self.vidas = []; self.ind = []; self.vivos = 0; self.tam = []
        self.vol_decl = 0; self.pv = 0

    def q(self, t): return min(t // (self.T // 4), 3)


def run_solapadas(seed, carros, T=100000, pizarra=1, compat=0, rep_acum=0, escala=1, telem=True, diag=1, mundo_n=None,
                  fundador_limpio=0, tope_cuerpos=TOPE_DEF, muestra=MUESTRA, reposicion='fija', r_rep=R_REP, eco=None):
    import pista2 as P
    n = len(carros)
    NMX = P.N_MAX if eco is None else ECO_NMAX
    if not 1 <= n <= NMX: raise SystemExit(f"PISTA2: entre 1 y {P.N_MAX} linajes fundadores (hay {n})")
    if compat: raise SystemExit("PISTA2: solapadas=1 no admite compat=1 (el ancla del monolito es de la pista v1)")
    if diag: raise SystemExit("PISTA2: solapadas=1 exige diag=0 (el diagnostico de v1 no se porto; declarado)")
    if rep_acum not in (0, 1): raise SystemExit("PISTA2: rep_acum es 0 o 1")
    if not (isinstance(tope_cuerpos, int) and tope_cuerpos >= n): raise SystemExit("PISTA2: tope_cuerpos entero >= n")
    if reposicion not in ('inmediata', 'fija'): raise SystemExit("PISTA2: reposicion 'inmediata' (v1) o 'fija' (quimiostato)")
    inst = reposicion == 'inmediata'
    # fundador_limpio: en v2 el fundador SIEMPRE es limpio (P3); el argumento se acepta y se ignora (se declara en la salida)
    CF = P.cfg_fabrica(); kw = CF['kw']; VAL_VIVO, EFECTO = CF['VAL_VIVO'], CF['EFECTO']
    EMX = P.N_MAX if eco is None else ECO_ESC_MAX
    if mundo_n is not None and (int(mundo_n) != mundo_n or not 1 <= mundo_n <= EMX):
        raise SystemExit(f"PISTA2: mundo_n entre 1 y {P.N_MAX}")
    esc = int(mundo_n) if mundo_n is not None else (n if escala else 1)
    L = CF['L'] * esc
    M = dict(nobj=kw['nobj'] * esc, costo=kw['costo'], costo_a=kw['costo_a'], rep_X=kw['rep_X'],
             rep_umbral=kw['rep_umbral'], dote=kw['dote'], olvido=P.OLVIDO)
    mods = [(c, (P.carga_carro(c) if eco is None else carga_eco(c))) if isinstance(c, str) else c for c in carros]
    E_ = None if eco is None else _eco_cfg(eco, CF, n)
    _GR = E_ is not None and E_['gr0'] is not None   # ORGANELOS
    _CO = E_ is not None and E_['cod0'] is not None   # CODIGO v0
    _FB = E_['cambio'] if (E_ is not None and isinstance(E_['cambio'], dict)) else None   # FABLE (F2)
    _CB = None if E_ is None or E_['cambio'] is None else ((int(_FB['t']), str(_FB.get('X', 'A')), str(_FB.get('Y', 'B'))) if _FB is not None else (int(E_['cambio'][0]), str(E_['cambio'][1]), str(E_['cambio'][2])))
    _EF0 = {k: tuple(EFECTO[VAL_VIVO[k]]) for k in 'ABCD'}   # FABLE: la tabla de fabrica
    ES = dict(t_ext=None, gen_t=[], n_mut=0, n_mut_s=0, n_nac=0, banco=[], n_banco=0, n_refund=0, corte=None)
    SE = lambda i, etq, k: np.random.default_rng([seed, i, etq, k])
    etiquetas = [e for e, _ in mods]
    ids = [(e if etiquetas.count(e) == 1 else f"{e}#{i}") for i, e in enumerate(etiquetas)]
    SS = lambda i, etq, k: np.random.default_rng([seed, i, P.ETQ[etq], k])
    rng = SS(0, 'mundo', 0)
    rngs_fund = [SS(i, 'cuerpo', 0) for i in range(n)]
    rngs_muerte = [SS(i, 'muerte', 0) for i in range(n)]
    rng_pista = SS(0, 'pista', 0)

    objs = {}; vista = types.MappingProxyType(objs)
    lin = [LinajeV2(i, ids[i], T, etiquetas[i]) for i in range(n)]
    id2lin = {}

    def ctx_de(i, r, ident, g=None, gr=None):
        _d = dict(id=ident, indice=i, n_linajes=n, T=T, L=L, PAT={k: v.copy() for k, v in CF['PAT'].items()},
                    rng=r, dote=M['dote'], rep_umbral=M['rep_umbral'], costo=M['costo'], costo_a=M['costo_a'],
                    rep_X=M['rep_X'], cupo=P.CUPO, ancho=P.ANCHO, fabrica=P.cfg_fabrica())
        if gr is not None: _d['gramatica'] = gr   # ORGANELOS (G2)
        return _d if g is None else ctx_genoma(_d, g)

    cuerpos = []
    for i, (e, mod) in enumerate(mods):   # los cerebros nacen ANTES del primer spawn (como en v1)
        c = mod.crea(ctx_de(i, rngs_fund[i], ids[i], (None if E_ is None else E_['gs0'][i]), gr=(E_['gr0'][i] if _GR else None)))
        cuerpos.append(Cuerpo(i, 0, 0, -1, 0, c, ids[i], vista, 0, M['dote'], 1))
        if E_ is not None:
            cuerpos[-1].g = E_['gs0'][i].copy(); cuerpos[-1].s = np.tile(E_['gs0'][i], (int(E_['n_sombra']), 1))
            if _GR: cuerpos[-1].gr = E_['gr0'][i]; cuerpos[-1].gs = (E_['gr0'][i],) * int(E_['n_sombra'])
            if _CO: cuerpos[-1].cin = E_['cod0'][i]; cuerpos[-1].mb = []   # CODIGO v0
        id2lin[ids[i]] = i; lin[i].vivos = 1; lin[i].fund = 0
    for b in cuerpos: b.E = 1.0; b.Ag = kw['A_ini']   # v1 (Linaje.__init__): el primer cuerpo arranca con E = 1.0, Ag = A_ini
    for b in cuerpos: b.pos = int(rng_pista.integers(L))

    def spawn():
        while len(objs) < M['nobj']:
            x = int(rng.integers(L))
            if x not in objs: objs[x] = P.TIPOS[int(rng.integers(len(P.TIPOS)))]
    spawn()
    r_paso = float(r_rep) * esc; banco = [0.0]; pisos = [0]; llegadas = [0]; perdidas = [0]

    def quita(x):   # P7: con 'inmediata' se repone al instante (v1); con 'fija' solo se quita (piso de 1 objeto)
        del objs[x]
        if inst: spawn()
        elif not objs:
            pisos[0] += 1; x2 = int(rng.integers(L)); objs[x2] = P.TIPOS[int(rng.integers(len(P.TIPOS)))]

    from collections import deque
    piz = deque(maxlen=P.CUPO); piz_t = (); n_escr_desc = 0; piz_log = []
    olv_n = 0; comp = {k: 0 for k in P.TIPOS}; nobj_suma = 0
    total = n; max_vivos = n; t_tope = None; tam_total = []
    orden = list(range(len(cuerpos)))

    def _muta_gr(gr, gs, i, k):   # ORGANELOS (G1): errores de copia de la gramatica real y de sus sombras (rng propios)
        if not _GR: return None, None
        if not E_['g_on']: return gr, gs
        _a = (float(E_['g_pcampo']), float(E_['g_pdup']), float(E_['g_pdel']), int(E_['g_tope']), E_['g_alf'])
        g2, nm = GD.muta_gram(gr, SE(i, ETQ_GMUT, k), *_a)
        _rg = SE(i, ETQ_GSOMBRA, k); s2 = tuple(GD.muta_gram(x, _rg, *_a)[0] for x in gs)
        ES['g_nmut'] = ES.get('g_nmut', 0) + nm
        return g2, s2

    def _destino(b, quien):   # ORGANELOS (G3): el destinatario mas cercano en el anillo; empate -> el primero de la lista; sin rng
        best = None; bd = None
        for z in cuerpos:
            if z is b or not z.vivo: continue
            if quien == 'hijo' and not (z.lin == b.lin and z.padre == b.k and not z.fund): continue
            if quien == 'hermano' and not (b.padre >= 0 and not b.fund and z.lin == b.lin and z.padre == b.padre and not z.fund): continue
            dd = abs(z.pos - b.pos); dd = min(dd, L - dd)
            if bd is None or dd < bd: best = z; bd = dd
        return best

    def _entrega(b, paqs, ev):   # ORGANELOS (G3)
        ce = ES.setdefault('g_ent', {})
        for quien, paq in paqs:
            z = _destino(b, quien); kk_ = f'{ev}/{quien}/{0 if z is None else 1}'; ce[kk_] = ce.get(kk_, 0) + 1
            if z is not None: z.c.recibe(paq)

    def _cod(cin, r, fm, prev_g, prev_gr, i, k, t, pk):   # CODIGO v0 (C3): COPIA (con la regla de la cinta) y DESARROLLO
        c2, st = CD.copia(cin, r, fm, bool(E_['c_sos']), bool(E_['c_on']))
        g2, gr2, _dd = CD.desarrolla(c2, E_['G0'], E_['lo'], E_['hi'], ENTEROS); gr2 = GD.valida(gr2, int(E_['g_tope']))
        ch = int(not (np.array_equal(g2, prev_g) and tuple(gr2) == tuple(prev_gr)))
        ES.setdefault('cod_nac', []).append([t, i, k, pk, st['n'], st['sos'], ch, len(c2)] + list(st['tipos']) + [(-1.0 if fm is None else round(float(fm), 3))])
        return c2, g2, gr2

    def _fmal(b): return (sum(b.mb) / len(b.mb)) if b.mb else 0.0   # CODIGO v0: lo VIVIDO por el padre (fisica)

    def registra(b, tm, causa, vd):
        L_ = lin[b.lin]
        _row = [b.k, b.gen, b.padre, b.tn, tm, b.hijos, b.fund, causa, vd]
        if E_ is not None and E_['ind_cb'] is not None: E_['ind_cb'](b.lin, _row, b.g)
        else: L_.ind.append(_row)

    _t0 = 0
    if E_ is not None and E_['banco']: ES['banco'] = [(b.g.copy(), b.s.copy(), b.gr, b.gs, b.cin) for b in cuerpos][-int(E_['banco']):]   # E9 (+ ORGANELOS)
    def _muestra_gen(tt):   # E4: genoma real y sombras (log(g/G0)): media sobre los VIVOS [4],[5] y sobre el BANCO [6],[7]
        G0 = E_['G0']; R5 = lambda v: [round(float(x), 5) for x in v]
        if ES['banco']:
            Br = R5(np.log(np.array([x[0] for x in ES['banco']]) / G0).mean(0))
            Bs = ([R5(f) for f in np.log(np.array([x[1] for x in ES['banco']]) / G0).mean(0)] if int(E_['n_sombra']) else [])
        else: Br = None; Bs = None
        vv = [b for b in cuerpos if b.vivo]
        if not vv: ES['gen_t'].append([tt, 0, 0, 0, None, None, Br, Bs]); return
        Gr = np.log(np.array([b.g for b in vv]) / G0).mean(0)
        Sr = (np.log(np.array([b.s for b in vv]) / G0).mean(0) if int(E_['n_sombra']) else np.zeros((0, len(G0))))
        ES['gen_t'].append([tt, len(vv), len(set(b.lin for b in vv)), int(max(b.gen for b in vv)),
                            R5(Gr), [R5(f) for f in Sr], Br, Bs])

    def _estado(tn):   # E7: TODO el estado en un solo pickle (los rng compartidos siguen compartidos)
        import pickle
        for b in cuerpos: b.obs['objs'] = None
        try:
            st = dict(t=tn, objs=dict(objs), rng=rng, rng_pista=rng_pista, rngs_fund=rngs_fund, rngs_muerte=rngs_muerte,
                      lin=lin, id2lin=id2lin, cuerpos=cuerpos, banco=banco, pisos=pisos, llegadas=llegadas, perdidas=perdidas,
                      piz=piz, piz_t=piz_t, n_escr_desc=n_escr_desc, piz_log=piz_log, olv_n=olv_n, comp=comp,
                      nobj_suma=nobj_suma, total=total, max_vivos=max_vivos, t_tope=t_tope, tam_total=tam_total, orden=orden, ES=ES,
                      firma=(seed, T, n, ids, L, M['nobj'], reposicion, float(r_rep), tope_cuerpos, muestra))
            return pickle.dumps(st, protocol=pickle.HIGHEST_PROTOCOL)
        finally:
            for b in cuerpos: b.obs['objs'] = vista

    if E_ is not None and E_['estado'] is not None:   # E7: reanudar
        import pickle
        st = pickle.loads(E_['estado'])
        if st['firma'] != (seed, T, n, ids, L, M['nobj'], reposicion, float(r_rep), tope_cuerpos, muestra):
            raise SystemExit('ECO: el checkpoint es de otra corrida (firma distinta)')
        objs.clear(); objs.update(st['objs'])
        rng = st['rng']; rng_pista = st['rng_pista']; rngs_fund[:] = st['rngs_fund']; rngs_muerte[:] = st['rngs_muerte']
        lin[:] = st['lin']; id2lin.clear(); id2lin.update(st['id2lin']); cuerpos = st['cuerpos']
        banco[:] = st['banco']; pisos[:] = st['pisos']; llegadas[:] = st['llegadas']; perdidas[:] = st['perdidas']
        piz = st['piz']; piz_t = st['piz_t']; n_escr_desc = st['n_escr_desc']; piz_log = st['piz_log']; olv_n = st['olv_n']
        comp = st['comp']; nobj_suma = st['nobj_suma']; total = st['total']; max_vivos = st['max_vivos']; t_tope = st['t_tope']
        tam_total = st['tam_total']; orden = st['orden']; ES.clear(); ES.update(st['ES'])
        for b in cuerpos: b.obs['objs'] = vista
        _t0 = st['t']; del st
    if _FB is None and _CB is not None and _t0 > _CB[0]: VAL_VIVO = dict(VAL_VIVO); VAL_VIVO[_CB[1]], VAL_VIVO[_CB[2]] = VAL_VIVO[_CB[2]], VAL_VIVO[_CB[1]]   # reanudar
    for t in range(_t0, T):
        _EFT = None if _FB is None else FB.efecto(_FB, t, _EF0, L)   # FABLE (F4)
        if _FB is None and _CB is not None and t == _CB[0]:   # CODIGO v0 (C4): EL MUNDO CAMBIA (se intercambia el valor de dos letras)
            VAL_VIVO = dict(VAL_VIVO); VAL_VIVO[_CB[1]], VAL_VIVO[_CB[2]] = VAL_VIVO[_CB[2]], VAL_VIVO[_CB[1]]
        if t % muestra == 0:
            for l in lin: l.tam.append(l.vivos)
            tam_total.append(total)
        for v in objs.values(): comp[v] += 1
        nobj_suma += len(objs)
        nb = len(cuerpos)
        if nb > 1: orden = [int(z) for z in rng_pista.permutation(nb)]
        else: orden = list(range(nb))
        foto = tuple((b.id, b.pos, objs.get(b.pos), b.ult_mordida) for b in cuerpos)
        pend = []
        # ---------------- fase A (igual que v1, sin diag)
        for j in orden:
            b = cuerpos[j]; l = lin[b.lin]; c = b.c; o = b.obs
            b.vol_kk = None
            o['t'] = t; o['pos'] = b.pos; o['E'] = b.E; o['Ag'] = b.Ag; o['cuerpos'] = foto; o['pizarra'] = piz_t
            a = c.actua(o)
            mov = int(a.get('mov', 0))
            if mov not in (-1, 0, 1): raise SystemExit(f"PISTA2: {b.id} mov={mov} (solo -1, 0, +1)")
            es = a.get('escribe')
            if es is not None:
                if pizarra: pend.append((t, b.id, P._valida_escritura(es)))
                else: n_escr_desc += 1
            b.pos = (b.pos + mov) % L; pos = b.pos
            res = dict(t=t, pos=pos, letra=None, mordio=False, dS=None)
            b.ult_mordida = None
            if pos in objs:
                kk = objs[pos]; mordio = bool(a.get('muerde', False)); q = l.q(t)
                l.vis[kk][q] += 1
                res['letra'] = kk
                if mordio:
                    _dS = EFECTO[VAL_VIVO[kk]] if _EFT is None else _EFT(kk, pos)   # FABLE (F5)
                    if _CO:   # CODIGO v0 (C2): registro fisico de lo vivido
                        b.mb.append(1 if min(_dS) < 0 else 0)
                        if len(b.mb) > 20: del b.mb[0]
                    if _CB is not None:   # CODIGO v0 (C5)
                        _ms = ES.setdefault('mord_signo', {}); _kq = f"{kk}/{'post' if t >= _CB[0] else 'pre'}"
                        _ms.setdefault(_kq, [0, 0]); _ms[_kq][1 if min(_dS) < 0 else 0] += 1
                    b.E = min(b.E + _dS[0], 1.5); b.Ag = min(b.Ag + _dS[1], 1.5)
                    l.mord[kk][q] += 1
                    if kk == 'B': b.tB = t
                    elif kk == 'D': b.tD = t
                    b.ult_mordida = kk
                    if kk in ('B', 'D') and sum(l.mord[kk]) > 1: b.vol_kk = kk   # ENMIENDA 6 (fisica; no discrimina, ERR-103)
                    quita(pos)
                    res['mordio'] = True; res['dS'] = tuple(_dS)
            c.resultado(res)
        # ---------------- costos
        for b in cuerpos:
            b.E -= M['costo']; b.Ag -= M['costo_a']
        # ---------------- olvido (ERR-98: esc sorteos por paso)
        olv = []
        for _o in range(esc):
            if rng.random() < M['olvido'] and objs:
                _dx = list(objs)[int(rng.integers(len(objs)))]; quita(_dx); olv.append(_dx); olv_n += 1
        olv = tuple(olv)
        if not inst:   # P7 quimiostato: llegadas a tasa fija, banco de a lo sumo 1 objeto pendiente
            banco[0] = min(banco[0] + r_paso, 1.0 + r_paso)
            while banco[0] >= 1.0:
                banco[0] -= 1.0
                if len(objs) < M['nobj']:
                    while True:
                        x2 = int(rng.integers(L))
                        if x2 not in objs: objs[x2] = P.TIPOS[int(rng.integers(len(P.TIPOS)))]; break
                    llegadas[0] += 1
                else: perdidas[0] += 1
        # ---------------- fase B
        nuevos = []; muertos = False
        for j in orden:
            b = cuerpos[j]; l = lin[b.lin]; c = b.c; i = b.lin
            c.fin_paso(dict(t=t, olvido=olv))
            if b.E <= 0 or b.Ag <= 0:
                por_E = b.E <= 0
                _causa = ('energia' if por_E else 'agua')
                cz = (('veneno' if t - b.tB < P.W_CAUSA else 'hambre') if por_E else ('sal' if t - b.tD < P.W_CAUSA else 'sed'))
                l.causas[cz] += 1
                if b.vol_kk == ('B' if por_E else 'D'): l.muertes_vol += 1
                l.deaths += 1; l.mnec[0 if por_E else 1] += 1
                edad = t - b.tn
                if _GR and 'morir' in c.EV: _entrega(b, c.emite('morir'), 'morir')   # ORGANELOS (G3): antes de muere()
                c.muere(dict(t=t, causa=_causa, causa_juez=cz, edad=edad, hijos=b.hijos))
                vd = 0
                campo = VOL_DECL.get(l.etq)
                if campo is not None and hasattr(c, 'salida'):
                    vd = int(bool(dict(c.salida()).get(campo, 0)))
                l.vol_decl += vd
                if len(l.vidas) < 100000: l.vidas.append(edad)
                registra(b, t, CAUSAS.index(cz), vd)
                b.vivo = False; l.vivos -= 1; total -= 1; muertos = True
                if b.pc is not None: b.pc.hvivos -= 1
                if E_ is not None: b.pc = None   # E8
                id2lin.pop(b.id, None); b.c = None; b.obs = None   # libera el cerebro del muerto
                if l.vivos > 0 or (E_ is not None and (not E_['refunda'] or (E_['t_corte'] is not None and t >= E_['t_corte']))): continue   # E5
                # P3: extincion -> fundador limpio en el LUGAR del muerto
                l.nac += 1
                if l.nac >= 100000: raise SystemExit('PISTA2: mas de 100000 cuerpos en un linaje: la semilla colisionaria (ERR-60)')
                l.fund += 1
                if len(l.tfund) < 200: l.tfund.append(t)
                _gf = _sf = _grf = _gsf = _cif = None
                if E_ is not None:   # E9 vivero: genoma del fundador = entrada del banco al azar, mutada (o el inicial)
                    if ES['banco']:
                        _gb, _sb, _grb, _gsb, _cib = ES['banco'][int(SE(i, ETQ_BANCO, l.nac).integers(len(ES['banco'])))]
                        _gf, _nm = muta(_gb, SE(i, ETQ_MUT, l.nac), E_['pv'], float(E_['sigma']), E_['lo'], E_['hi']); ES['n_mut'] += _nm
                        _rs = SE(i, ETQ_SOMBRA, l.nac); _sf = _sb.copy()
                        for _q in range(_sf.shape[0]): _sf[_q], _nm = muta(_sb[_q], _rs, E_['pv'], float(E_['sigma']), E_['lo'], E_['hi'])
                        ES['n_banco'] += 1; _grf, _gsf = _muta_gr(_grb, _gsb, i, l.nac)
                        if _CO: _cif, _gf, _grf = _cod(_cib, SE(i, ETQ_CMUT, l.nac), None, _gb, _grb, i, l.nac, t, -1)   # CODIGO v0
                    else:
                        _gf = E_['gs0'][i].copy(); _sf = np.tile(E_['gs0'][i], (int(E_['n_sombra']), 1))
                        if _GR: _grf = E_['gr0'][i]; _gsf = (_grf,) * int(E_['n_sombra'])
                        if _CO: _cif = E_['cod0'][i]
                    ES['n_refund'] += 1
                    if E_['donante'] == 'azar' and E_['banco']:   # control: el banco guarda el genoma NUEVO
                        ES['banco'].append((_gf.copy(), _sf.copy(), _grf, _gsf, _cif))
                        if len(ES['banco']) > E_['banco']: ES['banco'].pop(0)
                cnew = mods[i][1].crea(ctx_de(i, rngs_fund[i], ids[i], _gf, gr=_grf))
                F = Cuerpo(i, l.nac, 0, -1, t, cnew, ids[i], vista, int(rngs_muerte[i].integers(L)), M['dote'], 1)
                cuerpos[j] = F; b = F; c = cnew; l.vivos = 1; total += 1; id2lin[F.id] = i
                if E_ is not None: F.g = _gf; F.s = _sf; F.gr = _grf; F.gs = _gsf; F.cin = _cif; F.mb = ([] if _CO else None)
            # ventana de viabilidad (reproduccion)
            _ru = M['rep_umbral'] if b.g is None else b.g[I_RU]
            if b.E >= _ru and b.Ag >= _ru:
                if b.gv == 0: b.gv0 = t
                b.gv += 1; l.pv += 1
            else: b.gv = (b.gv if rep_acum else 0)
            if b.gv >= (M['rep_X'] if b.g is None else b.g[I_RX]):
                if hasattr(c, 'quiere_parir') and not c.quiere_parir(dict(t=t, E=b.E, Ag=b.Ag, cola=l.vivos - 1,
                                                                       vivos_linaje=l.vivos, hijos_vivos=b.hvivos)):
                    b.gv = 0; l.vetos += 1
                elif total >= tope_cuerpos:
                    b.gv = 0; l.bloq += 1
                    if t_tope is None: t_tope = t
                else:
                    l.desc += 1; b.gv = 0; b.hijos += 1; b.hvivos += 1
                    _dt = M['dote'] if b.g is None else float(b.g[I_DOTE])
                    b.E -= _dt; b.Ag -= _dt
                    mem = c.al_parir(dict(t=t, k=l.desc))
                    if _GR and 'nacer' in c.EV: _entrega(b, c.emite('nacer'), 'nacer')   # ORGANELOS (G3): hermano/vecino al parir
                    l.nac += 1; k = l.nac
                    if k >= 100000: raise SystemExit('PISTA2: mas de 100000 cuerpos en un linaje: la semilla colisionaria (ERR-60)')
                    hid = f"{ids[i]}/{k}"
                    _gh = _sh = _grh = _gsh = _cih = None
                    if E_ is not None:   # E3/E4: mutacion del hijo y de sus sombras (rng propios)
                        _dg, _ds, _dgr, _dgs, _dci = b.g, b.s, b.gr, b.gs, b.cin
                        if E_['donante'] == 'azar' and ES['banco']:   # control sin seleccion: entrada del banco al azar
                            _dg, _ds, _dgr, _dgs, _dci = ES['banco'][int(SE(i, ETQ_DONANTE, k).integers(len(ES['banco'])))]
                        _gh, _nm = muta(_dg, SE(i, ETQ_MUT, k), E_['pv'], float(E_['sigma']), E_['lo'], E_['hi'])
                        ES['n_mut'] += _nm; ES['n_nac'] += 1
                        _rs = SE(i, ETQ_SOMBRA, k); _sh = _ds.copy()
                        for _q in range(_sh.shape[0]):
                            _sh[_q], _nm = muta(_ds[_q], _rs, E_['pv'], float(E_['sigma']), E_['lo'], E_['hi']); ES['n_mut_s'] += _nm
                        _grh, _gsh = _muta_gr(_dgr, _dgs, i, k)   # ORGANELOS (G1)
                        if _CO: _cih, _gh, _grh = _cod(_dci, SE(i, ETQ_CMUT, k), _fmal(b), _dg, _dgr, i, k, t, b.k)   # CODIGO v0 (C3)
                        elif _GR: ES.setdefault('per_nac', []).append([t, i, k, b.k, int(not (np.array_equal(_gh, _dg) and tuple(_grh) == tuple(_dgr)))])   # v0.1 (V1)
                        if E_['banco']:   # 'padre': el genoma del PADRE (fertilidad); 'azar': el genoma NUEVO
                            ES['banco'].append((_dg.copy(), _ds.copy(), _dgr, _dgs, _dci) if E_['donante'] == 'padre' else (_gh.copy(), _sh.copy(), _grh, _gsh, _cih))
                            if len(ES['banco']) > E_['banco']: ES['banco'].pop(0)
                    ch = mods[i][1].crea(ctx_de(i, SS(i, 'cuerpo', k), hid, _gh, gr=_grh))
                    ch.nace(dict(t=t, k=k, fundador=False, memoria=mem, rng_hijo=SS(i, 'hijo', k), padre=b.id))
                    H = Cuerpo(i, k, b.gen + 1, b.k, t, ch, hid, vista, b.pos, _dt, 0, pc=b); H.g = _gh; H.s = _sh; H.gr = _grh; H.gs = _gsh; H.cin = _cih; H.mb = ([] if _CO else None)
                    nuevos.append(H); l.vivos += 1; total += 1; id2lin[hid] = i
                    if total > max_vivos: max_vivos = total
            if _GR and b.vivo and 'vida' in b.c.EV and t > b.tn and (t - b.tn) % GD.PER_VIDA == 0:   # ORGANELOS (G3): en vida
                _entrega(b, b.c.emite('vida'), 'vida')
        if muertos or nuevos:
            cuerpos = [b for b in cuerpos if b.vivo] + nuevos
        # ---------------- pizarra
        if pend:
            for e in pend:
                piz.append(e); piz_log.append([e[0], e[1], list(e[2])])
                le = lin[id2lin[e[1]]] if e[1] in id2lin else None
                if le is not None:
                    le.escrituras += 1
                    if telem and len(le.escr) < P.MAX_ESCRITURAS_TELEM: le.escr.append([e[0], list(e[2])])
            piz_t = tuple(piz)
        if E_ is not None:
            if E_['cada_gen'] and (t + 1) % E_['cada_gen'] == 0: _muestra_gen(t + 1)
            if E_['t_corte'] is not None and t + 1 == E_['t_corte']:   # E9: foto del genoma en el corte (lo que examina el juez)
                _vv = [z for z in cuerpos if z.vivo]
                ES['corte'] = dict(t=t + 1, vivos=len(_vv), n_banco=len(ES['banco']),
                                   med_vivos=([float(x) for x in np.median(np.array([z.g for z in _vv]), 0)] if _vv else None),
                                   med_banco=([float(x) for x in np.median(np.array([x[0] for x in ES['banco']]), 0)] if ES['banco'] else None),
                                   med_sombra_banco=([float(x) for x in np.median(np.array([x[1][0] for x in ES['banco']]), 0)]
                                                     if ES['banco'] and int(E_['n_sombra']) else None),
                                   banco=[[round(float(x), 9) for x in e[0]] for e in ES['banco']])
                if _GR: ES['gcorte'] = dict(t=t + 1, banco_gr=[e[2] for e in ES['banco']], banco_gs=[e[3] for e in ES['banco']],
                                            vivos_gr=[[z.lin, z.k, z.gen, z.tn, z.gr] for z in _vv])   # ORGANELOS (G4)
                if _CO: ES['ccorte'] = [[list(x) for x in e[4]] for e in ES['banco']]   # v0.1 (V2): el banco de CINTAS en el corte
            if total == 0:   # E5: si todo muere, muere
                ES['t_ext'] = t + 1; break
            if E_['ckpt_cada'] and (t + 1) % E_['ckpt_cada'] == 0 and t + 1 < T: E_['ckpt_fn'](t + 1, _estado(t + 1))

    for l in lin: l.tam.append(l.vivos)
    tam_total.append(total)
    # ---------------------------------------------------------------- salida (ERR-96: fisica ARRIBA, carro en d['carro'])
    vivos_de = {i: [b for b in cuerpos if b.lin == i] for i in range(n)}
    out = []
    for i, l in enumerate(lin):
        vd_vivos = 0
        campo = VOL_DECL.get(l.etq)
        for b in vivos_de[i]:
            v = 0
            if campo is not None and hasattr(b.c, 'salida'): v = int(bool(dict(b.c.salida()).get(campo, 0)))
            vd_vivos += v
            registra(b, -1, -1, v)
        car = {}
        if vivos_de[i] and hasattr(vivos_de[i][0].c, 'salida'): car = dict(vivos_de[i][0].c.salida())
        d = dict(mord=l.mord, vis=l.vis, deaths=l.deaths, muertes_nec=list(l.mnec), descendientes=l.desc,
                 nacimientos=l.desc, fundadores=l.fund, t_fund=list(l.tfund), vetos=l.vetos, bloqueados=l.bloq,
                 pasos_viables=l.pv, vidas_muertos=list(l.vidas), vivos_final=l.vivos, tam=list(l.tam),
                 individuos=l.ind, T_efectivo=T, dote=M['dote'], muerte_real=1)
        d['_carrera'] = dict(id=l.id, indice=i, etiqueta=l.etq, causas=dict(l.causas), escrituras=l.escrituras, escr=l.escr,
                             muertes_vol=l.muertes_vol, muertes_vol_decl=l.vol_decl, vol_decl_vivos_T=vd_vivos,
                             vol_decl_campo=campo)
        d['carro'] = car
        out.append(d)
    _gout = {} if not _GR else dict(gram=dict(   # ORGANELOS (G4)
        corte=ES.get('gcorte'), banco_final_gr=[e[2] for e in ES['banco']], banco_final_gs=[e[3] for e in ES['banco']],
        vivos_gr=[[b.lin, b.k, b.gen, b.tn, b.gr] for b in cuerpos if b.vivo], g_nmut=ES.get('g_nmut', 0), entregas=dict(ES.get('g_ent', {})),
        cfg=dict(p_campo=float(E_['g_pcampo']), p_dup=float(E_['g_pdup']), p_del=float(E_['g_pdel']), tope=int(E_['g_tope']),
                 alfabeto=[list(a) for a in E_['g_alf']], per_vida=GD.PER_VIDA),
        max_nac_linaje=max(l.nac for l in lin)))
    _cout = {} if not (_CO or _CB is not None) else dict(codigo=dict(per_nac=ES.get('per_nac', []), banco_corte=ES.get('ccorte'),   # v0.1 (V3)
        cod_nac=ES.get('cod_nac', []), mord_signo=ES.get('mord_signo', {}), cambio=(None if _CB is None else list(_CB)),
        c_on=(None if E_['cod0'] is None else bool(E_['c_on'])), c_sos=(None if E_['cod0'] is None else bool(E_['c_sos'])),
        cintas_vivos=[[b.lin, b.k, b.gen, [list(x) for x in b.cin]] for b in cuerpos if b.vivo and b.cin is not None][:80]))
    return dict(linajes=out, pizarra_log=piz_log, **_gout, **_cout,
                pista=dict(seed=seed, T=T, n=n, ids=ids, solapadas=1, compat=0, pizarra=int(pizarra), rep_acum=int(rep_acum),
                           escala=int(escala), L=L, nobj=M['nobj'], olvidos=olv_n, mundo_n=mundo_n,
                           fundador_limpio='siempre (P3)', reposicion=reposicion, r_paso=(None if inst else r_paso),
                           llegadas=llegadas[0], llegadas_perdidas=perdidas[0], pisos=pisos[0], tope_cuerpos=tope_cuerpos, t_tope=t_tope, max_vivos=max_vivos,
                           bloqueados=sum(l.bloq for l in lin), muestra=muestra, tam_total=tam_total,
                           comp_mundo={k: round(comp[k] / T, 4) for k in P.TIPOS}, nobj_medio=round(nobj_suma / T, 3), nobj_final=len(objs),
                           escrituras_descartadas=n_escr_desc, pizarra_n=len(piz_log),
                           pizarra_final=[[e[0], e[1], list(e[2])] for e in piz],
                           rng_mundo_estado=P._estado(rng)),
                **({} if E_ is None else dict(eco=dict(
                    genes=list(NOMBRES), G0=[float(x) for x in E_['G0']], lo=[float(x) for x in E_['lo']], hi=[float(x) for x in E_['hi']],
                    refunda=int(E_['refunda']), t_corte=E_['t_corte'], banco=int(E_['banco']), donante=E_['donante'], n_banco=ES['n_banco'],
                    n_refund=ES['n_refund'], corte=ES['corte'], mutables=[x for x, q in zip(NOMBRES, E_['pv']) if q > 0], p_mut=float(E_['p_mut']), sigma=float(E_['sigma']), n_sombra=int(E_['n_sombra']),
                    cada_gen=int(E_['cada_gen']), t_ext=ES['t_ext'], n_nac=ES['n_nac'], n_mut=ES['n_mut'], n_mut_s=ES['n_mut_s'],
                    gen_t=ES['gen_t'], vivos_final=[[b.lin, b.k, b.gen, b.tn] + [round(float(x), 6) for x in b.g] for b in cuerpos if b.vivo]))))
