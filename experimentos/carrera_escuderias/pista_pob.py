"""pista_pob.py — PISTA CON POBLACION (29-sep-2026, creador; EXPLORATORIO con puerta hacia serie). Preregistro:
experimentos/organelos/pista_pob/PREREGISTRO_pista_pob.md. Arnes: experimentos/organelos/pista_pob/identidad_pista_pob.py.

MISION: llegar a la AGI por este camino (organismo minimo con reglas locales, sin retropropagacion, peldanos preregistrados con
controles y replicas). Principio del director: que la seleccion construya el organo, no nosotros.

QUE ES: K copias de la PISTA VIEJA (pista.run, sin tocarla) corriendo EN PASO FIJO. Cada copia es EXACTAMENTE una corrida vieja
(9 carros, misma densidad, veneno, sal, dote, cola FIFO local, fundador limpio = ENMIENDA 5, T), con sus propias corrientes rng
(las de pista.run con su semilla). Lo unico que une a las copias es un DEPOSITO por indice de linaje:
  - DEPOSITO pool[i]: en cada parto del linaje i de la copia c se guarda deepcopy de la memoria que devuelve al_parir(), marcada c.
    FIFO con tope TOPE_POR_COPIA * K. Los partos del paso t se publican al TERMINAR el paso t en las K copias (simetrico: ninguna
    copia ve antes que otra lo que paso en su mismo paso).
  - FUNDACION: cuando el linaje i de la copia c se queda sin cola (fundador limpio: la pista ya hizo crea(ctx)), si pool[i] tiene
    entradas de OTRA copia, el fundador es un MIGRANTE: nace(memoria=...) sobre la instancia nueva, con el rng_hijo normal de la
    pista (hijo(i, k), k = nacimiento) y el sorteo con una rng NUEVA [semilla_c, i, ETQ_MIG=16, k] (la pista usa 11-15; ERR-60).
    Sin entradas de otras copias: fundador limpio como en la vieja. El migrante CUENTA COMO FUNDADOR (origen_cuerpo 0: no suma
    nacimientos reales).
  - modo 'sel'   : memoria = una entrada al azar de pool[i] con marca != c (solo entra quien PARIO: seleccion).
    modo 'neutro': memoria = las reglas del cuerpo VIVO del linaje i en otra copia al azar (haya parido o no), leidas al final del
                   paso anterior, con UNA mutacion del operador del carro (la entrada del pool ya trae la mutacion de al_parir).
                   MISMA TASA: migra si y solo si pool[i] tiene entradas de otra copia (el mismo deposito se lleva igual).
    modo 'nada'  : el deposito se lleva, nadie migra (arnes I2: cada copia == pista.run de su semilla).
SEMILLAS: copia 0 = seed; copia c >= 1 = 10**8 + 1000*seed + c.
CANAL OCULTO (cerrado): un carro con estado de MODULO (V143_BQ2: _BQ_BANCO) se carga UNA VEZ POR COPIA (carga_modulo): nada pasa entre
copias salvo lo que la camara pasa. Arnes I2 lo prueba (K=2 sin migracion == dos pista.run independientes).

CONSTRUCCION POR ANCLAS: el bucle NO se reescribe a mano. construye_run_gen() lee pista.py (sha fijado SHA_PISTA), extrae run() y
aplica ANCLAS (cada una debe aparecer EXACTAMENTE una vez): run -> run_gen (generador que cede cada paso), tres ganchos (inicio,
parto, fundador). Con _gancho=None o K=1 el generador ES pista.run (arnes I1). Todo lo demas (Linaje, _diag, _estado, cfg_fabrica,
carga_carro...) es el de pista.py: el codigo transformado se ejecuta con los globales de pista.
"""
import copy, hashlib, importlib.util, os, sys, time, types
from collections import deque
import numpy as np

AQUI = os.path.dirname(os.path.abspath(__file__))
if AQUI not in sys.path: sys.path.insert(0, AQUI)
import pista as P

SHA_PISTA = '9f47c65e438e0ff4'   # pista.py (el de corre_termo.SHAS y de los datos de bloques_pista)
SHA_JUEZ = '6a68f640a7832f12'    # juez.py
ETQ_MIG = 16                     # rng de la migracion [semilla_c, i, 16, k]
ETQ_MUESTRA = 17                 # rng de la muestra final (siembra) [seed, i, 17, 0]
TOPE_POR_COPIA = 50              # pool[i] FIFO con tope 50 * K
N_SIEMBRA = 50                   # listas por linaje en la siembra
VENTANA_MUESTRA = 5000; CADA_MUESTRA = 1000

ANCLAS = [
    ("def run(seed, carros, T=100000, pizarra=1, compat=0, rep_acum=0, escala=1, telem=True, diag=1, mundo_n=None, fundador_limpio=0):",
     "def run_gen(seed, carros, T=100000, pizarra=1, compat=0, rep_acum=0, escala=1, telem=True, diag=1, mundo_n=None, fundador_limpio=0, _gancho=None):"),
    ("    instancias = [1] * n\n",
     "    instancias = [1] * n\n    if _gancho is not None: _gancho.inicio(cars, lin, hijo)\n"),
    ("                    cars[i] = mods[i][1].crea(ctx_de(i)); c = cars[i]; instancias[i] += 1\n",
     "                    cars[i] = mods[i][1].crea(ctx_de(i)); c = cars[i]; instancias[i] += 1\n"
     "                    if _gancho is not None: _gancho.fundador(i, t, l.nac, c)\n"),
    ("                    l.cola.append(dict(dote=M['dote'], mem=c.al_parir(dict(t=t, k=l.desc))))\n",
     "                    _mem = c.al_parir(dict(t=t, k=l.desc)); l.cola.append(dict(dote=M['dote'], mem=_mem))\n"
     "                    if _gancho is not None: _gancho.parto(i, t, _mem)\n"),
    ("            piz_t = tuple(piz)\n\n    # ----",
     "            piz_t = tuple(piz)\n        yield t\n\n    # ----"),
]
_RG = [None]


def h16(p): return hashlib.sha256(open(p, 'rb').read()).hexdigest()[:16]
def h16s(s): return hashlib.sha256(s.encode('utf-8')).hexdigest()[:16]


def construye_run_gen():
    """-> (run_gen, dict(sha_pista, sha_juez, sha_fuente_transformada, anclas)). Aborta si un sha o un ancla no calzan."""
    if _RG[0] is not None: return _RG[0]
    rp = os.path.join(AQUI, 'pista.py'); rj = os.path.join(AQUI, 'juez.py')
    sp, sj = h16(rp), h16(rj)
    if sp != SHA_PISTA: raise SystemExit(f"PISTA_POB: pista.py sha {sp} != fijado {SHA_PISTA}")
    if sj != SHA_JUEZ: raise SystemExit(f"PISTA_POB: juez.py sha {sj} != fijado {SHA_JUEZ}")
    txt = open(rp, encoding='utf-8').read()
    a = txt.index("def run(seed, carros,"); b = txt.index("\n\n\n# claves de primer nivel")
    src = txt[a:b] + "\n"
    for viejo, nuevo in ANCLAS:
        n = src.count(viejo)
        if n != 1: raise SystemExit(f"PISTA_POB: el ancla aparece {n} veces (debe ser 1): {viejo[:70]!r}")
        src = src.replace(viejo, nuevo)
    ns = dict(vars(P))   # los globales de pista (Linaje, _diag, _estado, cfg_fabrica, carga_carro, ETQ, TIPOS...)
    exec(compile(src, '<pista_pob.run_gen desde pista.py>', 'exec'), ns)
    _RG[0] = (ns['run_gen'], dict(sha_pista=sp, sha_juez=sj, sha_fuente_transformada=h16s(src), anclas=len(ANCLAS)))
    return _RG[0]


def semilla_copia(seed, c):
    return int(seed) if c == 0 else 10 ** 8 + 1000 * int(seed) + int(c)


def carga_modulo(ruta, etiqueta):
    """Un modulo NUEVO por llamada (estado de modulo propio: canal oculto cerrado)."""
    spec = importlib.util.spec_from_file_location(etiqueta, ruta)
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
    if not hasattr(m, 'crea'): raise SystemExit(f"PISTA_POB: {ruta} no define crea(ctx)")
    return m


# ------------------------------------------------------------------ adaptadores del genoma de reglas (V143_BQ*)
def ref_reglas_bq(car):
    """Referencia (sin copiar) a la lista de reglas del cuerpo vivo. V143_BQ2 nunca muta _bqR en su lugar (solo lo REEMPLAZA en
    _bq_init y _bq_nace): una referencia tomada al final del paso t sigue valiendo las reglas de ese paso."""
    return car._bqR


def muta_bq(mod, reglas, rr):
    """UNA pasada del operador de mutacion del carro (_bq_muta, tasas BQ_C del modulo de la copia que recibe) con la rng de la
    migracion. Mismo operador que aplica al_parir a la entrada del pool."""
    shim = types.SimpleNamespace(_bqrng=rr)
    shim._bq_azar = lambda: mod.Carro._bq_azar(shim)
    return dict(bq=mod.Carro._bq_muta(shim, [list(r) for r in reglas]))


def reglas_de_mem(mem):
    return (mem or {}).get('bq') if isinstance(mem, dict) else None


# ------------------------------------------------------------------ la camara
class _Gancho:
    def __init__(self, cam, c): self.cam = cam; self.c = c; self.cars = None; self.hijo = None

    def inicio(self, cars, lin, hijo): self.cars = cars; self.lin = lin; self.hijo = hijo

    def parto(self, i, t, mem): self.cam.pend.append((i, self.c, t, copy.deepcopy(mem)))

    def fundador(self, i, t, k, car): self.cam.funda(self.c, i, t, k, car)


class Camara:
    def __init__(self, seed, K, n, modo, mods, T, ref_vivo=None, muta=None):
        if modo not in ('sel', 'neutro', 'nada'): raise SystemExit(f"PISTA_POB: modo {modo!r}")
        if modo == 'neutro' and (ref_vivo is None or muta is None): raise SystemExit("PISTA_POB: neutro exige ref_vivo y muta")
        self.seed = seed; self.K = K; self.n = n; self.modo = modo; self.mods = mods; self.T = T
        self.ref_vivo = ref_vivo; self.muta = muta
        self.pool = [deque(maxlen=TOPE_POR_COPIA * K) for _ in range(n)]
        self.pend = []; self.G = [_Gancho(self, c) for c in range(K)]
        self.vivos_prev = [[None] * n for _ in range(K)]
        self.migrantes = [[0] * n for _ in range(K)]; self.limpios = [[0] * n for _ in range(K)]
        self.depositos = [0] * n; self.dep_por_copia = [[0] * n for _ in range(K)]
        self.malas_marcas = 0; self.origen_mig = [[[0] * K for _ in range(n)] for _ in range(K)]
        self.t_mig = [[] for _ in range(K)]
        self.muestra = [[] for _ in range(n)]; self.t_muestras = []

    def funda(self, c, i, t, k, car):
        if self.modo == 'nada':
            self.limpios[c][i] += 1; return
        cands = [e for e in self.pool[i] if e[0] != c]
        if not cands:
            self.limpios[c][i] += 1; return
        rr = np.random.default_rng([semilla_copia(self.seed, c), i, ETQ_MIG, k])
        if self.modo == 'sel':
            e = cands[int(rr.integers(len(cands)))]; mem = copy.deepcopy(e[2]); org = e[0]
        else:
            otras = [x for x in range(self.K) if x != c]; org = otras[int(rr.integers(len(otras)))]
            R = self.vivos_prev[org][i]
            if R is None: raise SystemExit("PISTA_POB: neutro sin foto del vivo (no deberia pasar: la foto se toma cada paso)")
            mem = self.muta(self.mods[c], R, rr)
        if org == c: self.malas_marcas += 1
        car.nace(dict(t=t, k=k, fundador=True, memoria=mem, rng_hijo=self.G[c].hijo(i, k)))
        self.migrantes[c][i] += 1; self.origen_mig[c][i][org] += 1
        if len(self.t_mig[c]) < 2000: self.t_mig[c].append([int(t), int(i), int(org)])

    def fin_paso(self, t):
        for (i, c, tt, mem) in self.pend:
            self.pool[i].append((c, tt, mem)); self.depositos[i] += 1; self.dep_por_copia[c][i] += 1
        self.pend = []
        if self.ref_vivo is not None:
            for c in range(self.K):
                cars = self.G[c].cars
                self.vivos_prev[c] = [self.ref_vivo(cars[i]) for i in range(self.n)]
        w = min(VENTANA_MUESTRA, self.T)
        if t >= self.T - w and (t + 1) % CADA_MUESTRA == 0 and self.ref_vivo is not None:
            self.t_muestras.append(int(t))
            for i in range(self.n):
                for e in self.pool[i]:
                    R = reglas_de_mem(e[2])
                    if R: self.muestra[i].append(R)
                for c in range(self.K):
                    R = self.vivos_prev[c][i]
                    if R: self.muestra[i].append(R)

    def siembra(self):
        """Por linaje: N_SIEMBRA listas al azar (sin reposicion; rng [seed, i, 17, 0]) de las fotos del deposito + vivos; se concatenan."""
        out = []; por = []
        for i in range(self.n):
            M = self.muestra[i]
            if not M: por.append(0); continue
            rr = np.random.default_rng([int(self.seed), i, ETQ_MUESTRA, 0])
            ix = rr.choice(len(M), size=min(N_SIEMBRA, len(M)), replace=False)
            out += [[list(map(float, r)) for r in M[int(j)]] for j in ix]; por.append(len(ix))
        return out, por


def run(seed, K, carro, T, modo='sel', ident=None, prepara=None, ref_vivo=None, muta=None, n=9, pizarra=1, compat=0,
        fundador_limpio=1, log=None, _compartir_modulo=False):
    """K copias en paso fijo. carro = ruta a un .py con crea(ctx) (se carga K veces). prepara(mod, c, semilla_c) opcional, antes de
    correr. Devuelve dict(copias=[salida de pista.run de cada copia], camara=..., siembra=..., meta=...).
    _compartir_modulo=True: SOLO ARNES (control que DEBE fallar: el canal oculto abierto, un modulo para todas las copias)."""
    run_gen, info = construye_run_gen()
    ident = ident or os.path.splitext(os.path.basename(carro))[0]
    mods = []
    for c in range(K):
        if _compartir_modulo and c > 0: mods.append(mods[0]); continue
        m = carga_modulo(carro, f"carro_{ident}_pob{c}_{id(object())}")
        if prepara is not None: prepara(m, c, semilla_copia(seed, c))
        mods.append(m)
    cam = Camara(seed, K, n, modo, mods, T, ref_vivo=ref_vivo, muta=muta)
    gens = [run_gen(semilla_copia(seed, c), [(ident, mods[c])] * n, T=T, pizarra=pizarra, compat=compat,
                    fundador_limpio=fundador_limpio, _gancho=cam.G[c]) for c in range(K)]
    t0 = time.time()
    for t in range(T):
        for g in gens:
            tt = next(g)
            if tt != t: raise SystemExit(f"PISTA_POB: paso {tt} != {t}")
        cam.fin_paso(t)
        if log is not None and (t + 1) % 10000 == 0: log(f"    camara paso {t + 1}/{T} ({time.time() - t0:.0f}s)")
    outs = []
    for g in gens:
        try:
            next(g); raise SystemExit("PISTA_POB: el generador no termino")
        except StopIteration as e:
            outs.append(e.value)
    sb, por = cam.siembra() if ref_vivo is not None else ([], [])
    camara = dict(modo=modo, K=K, semillas=[semilla_copia(seed, c) for c in range(K)], migrantes=cam.migrantes, limpios=cam.limpios,
                  depositos=cam.depositos, dep_por_copia=cam.dep_por_copia, pool_final=[len(p) for p in cam.pool],
                  tope=TOPE_POR_COPIA * K, malas_marcas=cam.malas_marcas, origen_mig=cam.origen_mig, t_mig=cam.t_mig,
                  t_muestras=cam.t_muestras, muestra_n=[len(x) for x in cam.muestra], siembra_por_linaje=por)
    return dict(copias=outs, camara=camara, siembra=sb, meta=dict(info, seed=seed, T=T, ident=ident, seg=round(time.time() - t0, 1)))
