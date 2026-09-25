"""conducta.py — NOVEDAD POR CONDUCTA, no por etiqueta (correccion 2). Equipo organelos, Opus A, 24-sep-2026.

MISION: llegar a la AGI por este camino.

BANCO FIJO de estados de memoria (emisores S0-S4 x receptores Rn/Ra) y, para cada gramatica, la TABLA DE EFECTO que produce en el receptor:
por (evento, a quien, emisor, receptor) el cambio en los 8 valores de la via lenta (Wps - Wns)[n] @ PAT[k] (k = A..D, n = hambre/sed)
respecto del mismo receptor sin recibir nada. Se calcula con el CODIGO REAL del carro (al_parir/nace para nacer-hijo; emite/recibe para
lo demas), no con una copia de la regla.
Dos gramaticas son EL MISMO ORGANO si sus tablas de efecto difieren en a lo sumo TOL = 0.05 en todas las celdas (escala: R en {+1, -3, 0}).
Solo se usan estados ALCANZABLES en w30 (S4, lo heredado invertido o a medias, aparece con 'invertir'/'promediar' en la linea).

La verdad del mundo (VAL_VIVO/EFECTO de fabrica): R(A,hambre)=+1, R(A,sed)=0, R(B,hambre)=-3, R(B,sed)=0, R(C,hambre)=0, R(C,sed)=+1,
R(D,hambre)=0, R(D,sed)=-3.
"""
import os, sys
import numpy as np

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(AQUI)))
for _d in (AQUI, os.path.join(RAIZ, 'experimentos', 'generaciones')):
    if _d not in sys.path: sys.path.insert(0, _d)
import gramatica_def as GD

TOL = 0.05
VERDAD = {('A', 0): 1.0, ('A', 1): 0.0, ('B', 0): -3.0, ('B', 1): 0.0, ('C', 0): 0.0, ('C', 1): 1.0, ('D', 0): 0.0, ('D', 1): -3.0}
_CARRO = [None]; _CF = [None]


def _carro():
    if _CARRO[0] is None:
        import importlib.util, pista2 as P
        ruta = os.path.join(AQUI, 'carros', 'FAMB_GRAM_ECO.py'); nom = 'carro_eco_FAMB_GRAM_ECO'
        if nom in sys.modules: _CARRO[0] = sys.modules[nom]
        else:
            spec = importlib.util.spec_from_file_location(nom, ruta); mod = importlib.util.module_from_spec(spec)
            sys.modules[nom] = mod; spec.loader.exec_module(mod); _CARRO[0] = mod
        _CF[0] = P
    return _CARRO[0]


def _ctx(gr, semilla):
    P = _CF[0]; CF = P.cfg_fabrica(); kw = CF['kw']
    return dict(id='banco', indice=0, n_linajes=1, T=100000, L=CF['L'] * 30, PAT={k: v.copy() for k, v in CF['PAT'].items()},
                rng=np.random.default_rng([990000, semilla]), dote=kw['dote'], rep_umbral=kw['rep_umbral'], costo=kw['costo'],
                costo_a=kw['costo_a'], rep_X=kw['rep_X'], cupo=P.CUPO, ancho=P.ANCHO, fabrica=CF, gramatica=gr)


def _nuevo(gr, semilla):
    c = _carro().crea(_ctx(gr, semilla)); c.nace(dict(t=0, k=1, fundador=False, memoria=None, rng_hijo=np.random.default_rng([991000, semilla]), padre='x'))
    return c


def _ent(k, n, R, PAT): return [[float(z) for z in PAT[k]], float(R), int(n)]


def _emisor(c, cual):
    """Estados del EMISOR (lo vivido va a _mordh como [t, letra, necesidad, R]; lo heredado a _nodo)."""
    PAT = c.PAT; V = VERDAD
    c._mordh = []; c._nodo = []
    if cual == 'S0': pass                                            # no vivio ni heredo nada
    elif cual == 'S1': c._mordh = [[i, k, n, V[(k, n)]] for i, (k, n) in enumerate(sorted(V))]            # vivio todo
    elif cual == 'S2':                                               # heredo todo (verdad); vivio solo lo bueno
        c._nodo = [_ent(k, n, V[(k, n)], PAT) for (k, n) in sorted(V)] * 3
        c._mordh = [[1, 'A', 0, 1.0], [2, 'C', 1, 1.0]]
    elif cual == 'S3':                                               # vivio el veneno y la sal HACE MUCHO; despues 20 mordidas buenas
        c._mordh = [[1, 'B', 0, -3.0], [2, 'D', 1, -3.0]] + [[3 + i, ('A' if i % 2 == 0 else 'C'), i % 2, 1.0] for i in range(20)]
    elif cual == 'S4':                                               # heredo el veneno INVERTIDO y la comida a medias; vivio lo neutro
        c._nodo = [_ent('B', 0, 3.0, PAT), _ent('D', 1, 3.0, PAT), _ent('A', 0, 0.5, PAT)] * 3
        c._mordh = [[1, 'A', 1, 0.0], [2, 'C', 0, 0.0]]
    return c


def _receptor(cual, semilla):
    c = _nuevo(GD.NULO, semilla)
    if cual == 'Ra':   # adulto: vivio el veneno y la comida (via lenta entrenada con lo vivido)
        c._mordh = [[1, 'B', 0, -3.0], [2, 'A', 0, 1.0]]
        c._lee([_ent('B', 0, -3.0, c.PAT), _ent('A', 0, 1.0, c.PAT)] * c.NODO_LEE)
    return c


def _valores(c):
    return np.array([float((c.Wps[n] - c.Wns[n]) @ c.PAT[k]) for k in 'ABCD' for n in (0, 1)])


EMISORES = ('S0', 'S1', 'S2', 'S3', 'S4')
RECEPTORES = ('Rn', 'Ra')
CELDAS = tuple((ev, q) for ev in ('nacer', 'vida', 'morir') for q in GD.QUIEN)


def tabla_efecto(gr):
    """dict (evento, quien, emisor, receptor) -> vector de 8 efectos (redondeado a 1e-6). Solo celdas con efecto != 0 se guardan."""
    gr = GD.valida(gr) if gr else ()
    out = {}
    for si, S in enumerate(EMISORES):
        em = _emisor(_nuevo(gr, 10 + si), S)
        # nacer / hijo: al_parir -> nace del hijo (receptor recien nacido)
        mem = em.al_parir(dict(t=5, k=1))
        hijo = _carro().crea(_ctx(GD.NULO, 50 + si)); hijo.nace(dict(t=5, k=2, fundador=False, memoria=mem, rng_hijo=np.random.default_rng([992000, si]), padre='x'))
        base = _carro().crea(_ctx(GD.NULO, 50 + si)); base.nace(dict(t=5, k=2, fundador=False, memoria=None, rng_hijo=np.random.default_rng([992000, si]), padre='x'))
        d = _valores(hijo) - _valores(base)
        if np.abs(d).max() > 1e-9: out[('nacer', 'hijo', S, 'Rn')] = np.round(d, 6)
        for ev in ('nacer', 'vida', 'morir'):
            paqs = em.emite(ev)
            for q in GD.QUIEN:
                pq = [p for (qq, p) in paqs if qq == q]
                if not pq: continue
                for R in RECEPTORES:
                    rc = _receptor(R, 70 + si); r0 = _valores(rc)
                    for p in pq: rc.recibe(p)
                    d = _valores(rc) - r0
                    if np.abs(d).max() > 1e-9: out[(ev, q, S, R)] = np.round(d, 6)
    return out


def distancia(a, b):
    ks = set(a) | set(b); z = np.zeros(8)
    return max([float(np.abs(a.get(k, z) - b.get(k, z)).max()) for k in ks] or [0.0])


_CACHE = {}


def firma(gr):
    """Tabla de efecto con cache por gramatica EXPRESADA (sin origen ni slots silenciosos)."""
    key = GD.activos(gr) if gr else ()
    if key not in _CACHE: _CACHE[key] = tabla_efecto(tuple(s + (0,) for s in key))
    return _CACHE[key]


def igual(a, b, tol=TOL): return distancia(firma(a), firma(b)) <= tol


def clase_disenada(gr, tol=TOL):
    """Nombre del disenado con la misma conducta ('nulo', 'ensena', 'filtra0') o None si no es ninguno."""
    f = firma(gr)
    for nom, g in GD.DISENADOS.items():
        if distancia(f, firma(g)) <= tol: return nom
    return None
