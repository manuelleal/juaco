"""camara_linajes.py — CAMARA DE PASAJE CON SELECCION ENTRE LINAJES (entre_linajes, 30-sep-2026, creador; EXPLORATORIO con puerta).
Preregistro: PREREGISTRO_entre_linajes.md. Arnes: identidad_entre_linajes.py.

MISION: llegar a la AGI por este camino (organismo minimo con reglas locales, sin retropropagacion, peldanos preregistrados con
controles y replicas).

QUE ES: el pasaje de o1_evo (UNA pista vieja, 9 linajes de O1_PAS, fundador limpio = ENMIENDA 5) con DOS cambios:
  (b) COLONIZACION (Moran entre linajes): cuando el linaje i se queda sin cola y la pista pone un fundador limpio (crea(ctx) otra vez,
      que sortea genes de la SIEMBRA del pasaje anterior), si en el DEPOSITO hay hijos recientes de OTRO linaje de la MISMA pista, el
      fundador toma los GENES de uno de ellos (nace(memoria={'_gen': genes})). SOLO los genes: la tabla de letras NO viaja (el fundador
      sigue ingenuo, como el fundador de la prueba oficial). El colonizador cuenta como fundador (la pista ya lo conto).
      DEPOSITO: FIFO de los ultimos TOPE partos de la pista (indice del linaje, t, genes del hijo = '_gen' de al_parir, ya mutado);
      los partos del paso t se publican al TERMINAR t. Sorteo uniforme entre las entradas con indice != i, rng [seed, i, 16, k]
      (la pista usa 11-15; pista_pob usa 16 para lo mismo en otra camara). Sin candidatos: fundador de siembra como siempre.
  (a) SIEMBRA PROPORCIONAL A HIJOS: la siembra del pasaje siguiente tiene el MISMO total (len de la siembra igualada, ~45) pero el
      numero de entradas del linaje i es proporcional a sus PARTOS en el pasaje (contador local del carro, _TEL[i]['partos']: sin juez),
      por restos mayores (empates: indice menor). Las entradas del linaje i son sus muestras de vivos (las mismas que la siembra
      igualada: cada 1 000 pasos en los ultimos 5 000) en orden cronologico, ciclando. Con partos iguales ES la siembra igualada (arnes).
      Sin partos en todo el pasaje: siembra igualada (declarado).

CONSTRUCCION: el bucle de la pista NO se reescribe: se usa pista_pob.construye_run_gen() (pista.run transformado por 5 anclas, cada una
exactamente una vez, con shas de pista.py y juez.py fijados; se IMPORTA, no se toca; su sha se fija aqui). Con _gancho None el
generador ES pista.run (arnes I1). La camara se engancha como pista.run (corre_camara) y la medida del juez del pasaje se hace con
corre_o1_evo.tarea SIN CAMBIOS (se reemplaza P.run solo durante el pasaje y se restaura).
"""
import copy, hashlib, os, sys
from collections import deque
import numpy as np

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(AQUI))))
O1EVO = os.path.join(RAIZ, 'experimentos', 'organelos', 'o1_evo')
PISTA_D = os.path.join(RAIZ, 'experimentos', 'carrera_escuderias')
for _d in (O1EVO, PISTA_D):
    if _d not in sys.path: sys.path.insert(0, _d)
import corre_o1_evo as E          # runner de o1_evo: tarea, siembra, fila (se IMPORTAN, no se tocan)
import pista_pob as PP            # construye_run_gen (anclas sobre pista.py)
P = E.P                           # el modulo pista (el mismo objeto que usa corre_v143.tarea)

SHAS_FIJOS = {os.path.join(PISTA_D, 'pista_pob.py'): 'd4ed07b28e4ba94b', os.path.join(PISTA_D, 'pista.py'): '9f47c65e438e0ff4',
              os.path.join(PISTA_D, 'juez.py'): '6a68f640a7832f12', os.path.join(O1EVO, 'corre_o1_evo.py'): '95622a2f93bb38b0',
              os.path.join(O1EVO, 'carros', 'O1_PAS.py'): 'c5377ada6b28bee0', os.path.join(O1EVO, 'construye_o1_pas.py'): '8013e4a99a004bda',
              os.path.join(RAIZ, 'experimentos', 'tronco_v14_3', 'corre_v143.py'): '24100621c450da22'}
ETQ_COL = 16      # rng de la colonizacion [seed, i, 16, k]
TOPE = 50         # deposito FIFO: ultimos 50 partos de la pista (~ los hijos de los ultimos ~1-2 mil pasos)
GENES = E.GENES


def h16(p): return hashlib.sha256(open(p, 'rb').read()).hexdigest()[:16]


def verifica_shas():
    """-> lista de (ruta, sha, fijado, ok)."""
    return [(r, h16(r), s, h16(r) == s) for r, s in SHAS_FIJOS.items()]


class Colonizador:
    """Gancho de la camara (interfaz de pista_pob: inicio, parto, fundador) + fin_paso. modo 'nada': registra y NO coloniza."""

    def __init__(self, seed, modo, tope=TOPE):
        if modo not in ('nada', 'col'): raise SystemExit(f"CAMARA: modo {modo!r}")
        self.seed = int(seed); self.modo = modo
        self.dep = deque(maxlen=tope); self.pend = []
        self.hijo = None; self.n = None
        self.partos = None; self.funds = None; self.colonos = None; self.limpios = None; self.origen = None; self.t_col = []

    def inicio(self, cars, lin, hijo):
        self.hijo = hijo; self.n = len(cars)
        self.partos = [0] * self.n; self.funds = [0] * self.n; self.colonos = [0] * self.n; self.limpios = [0] * self.n
        self.origen = [[0] * self.n for _ in range(self.n)]

    def parto(self, i, t, mem):
        self.partos[i] += 1
        g = (mem or {}).get('_gen') if isinstance(mem, dict) else None
        if g is not None: self.pend.append((int(i), int(t), [float(x) for x in g]))

    def fin_paso(self, t):
        for e in self.pend: self.dep.append(e)
        self.pend = []

    def fundador(self, i, t, k, car):
        self.funds[i] += 1
        if self.modo == 'nada':
            self.limpios[i] += 1; return
        cands = [e for e in self.dep if e[0] != i]
        if not cands:
            self.limpios[i] += 1; return
        rr = np.random.default_rng([self.seed, int(i), ETQ_COL, int(k)])
        e = cands[int(rr.integers(len(cands)))]
        car.nace(dict(t=t, k=k, fundador=True, memoria={'_gen': list(e[2])}, rng_hijo=self.hijo(i, k)))
        self.colonos[i] += 1; self.origen[i][e[0]] += 1
        if len(self.t_col) < 3000: self.t_col.append([int(t), int(i), int(e[0])])

    def resumen(self):
        return dict(modo=self.modo, tope=self.dep.maxlen, partos=self.partos, fundadores=self.funds, colonos=self.colonos,
                    limpios=self.limpios, origen=self.origen, colonos_total=sum(self.colonos or []), fundadores_total=sum(self.funds or []),
                    t_col=self.t_col, deposito_final=len(self.dep))


def corre_camara(col):
    """-> funcion con la firma de pista.run que corre run_gen con el gancho col (None: pista.run por anclas, sin gancho)."""
    run_gen, _ = PP.construye_run_gen()

    def run(seed, carros, T=100000, pizarra=1, compat=0, rep_acum=0, escala=1, telem=True, diag=1, mundo_n=None, fundador_limpio=0):
        g = run_gen(seed, carros, T=T, pizarra=pizarra, compat=compat, rep_acum=rep_acum, escala=escala, telem=telem, diag=diag,
                    mundo_n=mundo_n, fundador_limpio=fundador_limpio, _gancho=col)
        for t in range(T):
            tt = next(g)
            if tt != t: raise SystemExit(f"CAMARA: paso {tt} != {t}")
            if col is not None: col.fin_paso(t)
        try:
            next(g)
        except StopIteration as e:
            return e.value
        raise SystemExit("CAMARA: el generador no termino")
    return run


def tarea_pasaje(seed, brazo_e, T, siembra, lee, modo, sigma=None):
    """UN pasaje: corre_o1_evo.tarea TAL CUAL (juez, telemetria, estado) con P.run reemplazado por la camara durante la corrida.
    brazo_e: brazo de corre_o1_evo ('o1pas' u 'o1neu': mismo carro O1_PAS y sigma 0.03; sigma None = la del brazo; solo el arnes la cambia). Devuelve (x, resumen de la camara)."""
    col = Colonizador(seed, modo)
    orig = P.run
    P.run = corre_camara(col)
    try:
        x = E.tarea(seed, brazo_e, T, siembra=siembra, sigma=sigma, lee=lee)
    finally:
        P.run = orig
    return x, col.resumen()


def cuotas(pesos, N):
    """Restos mayores: enteros n_i >= 0 con suma N, proporcionales a pesos (empates por indice menor)."""
    S = float(sum(pesos))
    q = [N * w / S for w in pesos]; n = [int(np.floor(x)) for x in q]
    r = N - sum(n)
    orden = sorted(range(len(pesos)), key=lambda j: (-(q[j] - n[j]), j))
    for j in orden[:r]: n[j] += 1
    return n


def siembra_prop(tel, T, vent=E.VENT):
    """SIEMBRA PROPORCIONAL A HIJOS. tel = telemetria de O1_PAS {indice: {'vivos': [[t, genes]], 'partos': n}}.
    -> (lista de genomas, info). Total = len(siembra igualada). Pesos = partos del linaje en el pasaje (contador local del carro).
    No lee R0, cruza ni nada del juez."""
    igual = E.siembra(tel, T, vent)
    idx = sorted(tel or {}, key=lambda z: int(z))
    mues = {i: [g for t, g in (tel[i] or {}).get('vivos', []) if t >= T - vent] for i in idx}
    idx = [i for i in idx if mues[i]]
    partos = [int((tel[i] or {}).get('partos', 0)) for i in idx]
    if not igual or sum(partos) == 0:
        return igual, dict(prop=0, motivo='sin partos' if igual else 'sin vivos', n_por_linaje=None, partos=partos, ne=None)
    N = len(igual); n = cuotas(partos, N)
    out = []
    for i, k in zip(idx, n):
        M = mues[i]
        for j in range(k): out.append({g: float(v) for g, v in zip(GENES, M[j % len(M)])})
    w = [k / N for k in n]
    return out, dict(prop=1, n_por_linaje={str(i): k for i, k in zip(idx, n)}, partos={str(i): p for i, p in zip(idx, partos)},
                     ne=round(1.0 / sum(x * x for x in w), 3), linajes_con_entradas=sum(1 for k in n if k > 0), N=N)
