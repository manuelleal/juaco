"""pista_libre.py — MUNDO DONDE CADA PODER PUEDE PAGAR (o1_libre, 30-sep-2026, creador; EXPLORATORIO). Preregistro:
PREREGISTRO_o1_libre.md. Arnes: identidad_o1_libre.py (salida entera en identidad_o1_libre_salida.txt).

MISION: llegar a la AGI por este camino (organismo minimo con reglas locales, sin retropropagacion, peldanos preregistrados con
controles y replicas). Encargo del director: "O1 libre con poderes: no es tiempo, son condiciones para evolucionar".

QUE ES: la PISTA VIEJA (experimentos/carrera_escuderias/pista.py, sha fijado SHA_PISTA, NO se toca; 9 linajes, L 360, 36 objetos)
con tres perillas de mundo. Con las tres en 0, run() ES pista.run BIT A BIT (arnes (f)), incluido el estado final del rng del mundo.
  estacion (0/1): TEMPORADAS SUAVES. s(t) = -sin(2 pi t / EST_P) (empieza en abundancia: los fundadores se establecen antes de la
         primera escasez). Cada objeto que nace (spawn: por mordida o por olvido) sortea su letra como siempre (rng del mundo) y
         despues, con una rng PROPIA: si s > 0 (escasez) una A/C pasa a B/D con prob EST_AMP * s; si s < 0 (abundancia) una B/D pasa
         a A/C con prob EST_AMP * |s|. Fraccion buena de lo que nace = 0.5 (1 - EST_AMP s): de 0.25 a 0.75, suave, sin golpes.
         Media en un periodo: la del mundo viejo. Las letras NO cambian de significado (lo aprendido sigue valiendo: nada de
         inversiones; ESTADO 29-sep: "el mundo que cambia de golpe mata a todos").
  parche (0/1): PARCHE RICO QUE SE MUEVE LENTO. Un arco de PAR_W celdas que avanza 1 celda cada PAR_V pasos (inicio sorteado por
         semilla). Cada A/C que nace (tras la estacion) se muda, con prob PAR_Q y rng PROPIA, a una celda LIBRE del parche. La comida
         se CONCENTRA donde esta el parche; el parche no se anuncia (nadie recibe su posicion); se ve la comida (como siempre: la pista
         entrega todos los objetos), no el parche vacio.
  quieto (0/1): ESPERAR PAGA. Un cuerpo que en fase A no se movio (mov 0) paga en los costos del paso (1 - QUIETO_AHORRO) del costo
         metabolico en E y en Ag. Todos los carros cobran igual (O1 de fabrica tambien se queda quieto en su blanco).
POR QUE CADA UNA (poder que puede pagar): parche -> MEMORIA DE LUGAR (cuando no hay nada util, esperar donde se comio: la comida
nueva cae ahi); estacion -> SENTIDO DE RESERVA (llenarse cuando escasea) y ESPERA; quieto -> PAUSA. La COPIA SOCIAL paga en el
mundo viejo (un refundador con tabla vacia no sabe que comer); la unica condicion que necesita es que los vecinos publiquen (lo hace
el carro, perilla PS_ESCRIBE: el mundo no cambia). "Evitar no es gratis" ya en la pista vieja (lo no mordido TAPA el mundo: por
eso O1 limpia) y aqui mas: en la escasez nace mas B/D.
RNG PROPIA: [seed, 0, ETQ_LIBRE=21, 0] (pista 11-15; pista_pob 16-17; pista_grande 18): no perturba NINGUNA corriente de la pista;
no son sitios fijos entre semillas (trampa 4).

CONSTRUCCION POR ANCLAS (patron de pista_grande.py): construye() lee pista.py (sha SHA_PISTA; juez.py SHA_JUEZ), extrae run() y
aplica ANCLAS (cada una EXACTAMENTE una vez). Todo lo demas es el de pista.py (el codigo transformado corre con sus globales).
SALIDA NUEVA (solo si alguna perilla esta prendida): pista['libre'] (parametros y contadores de SOLO LECTURA).
"""
import hashlib, math, os, sys
import numpy as np

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(AQUI)))
PISTA_D = os.path.join(RAIZ, 'experimentos', 'carrera_escuderias')
if PISTA_D not in sys.path: sys.path.insert(0, PISTA_D)
import pista as P

SHA_PISTA = '9f47c65e438e0ff4'   # pista.py (el de corre_v143.SHAS, pista_pob, pista_grande, o1_evo)
SHA_JUEZ = '6a68f640a7832f12'    # juez.py
ETQ_LIBRE = 21
EST_P = 20000                    # periodo de la estacion (5 por prueba de 100k)
EST_AMP = 0.5                    # fraccion buena de lo que nace: 0.25 (escasez) .. 0.75 (abundancia)
PAR_W = 36                       # ancho del parche (10 % de L 360)
PAR_V = 250                      # pasos por celda (400 celdas por 100k: ~1.1 vueltas)
PAR_Q = 0.5                      # prob. de que una A/C que nace se mude al parche
QUIETO_AHORRO = 0.3              # quieto paga 0.7 del costo metabolico
MUNDO_LIBRE = dict(estacion=1, parche=1, quieto=1)
MUNDO_VIEJO = dict(estacion=0, parche=0, quieto=0)

FIRMA_VIEJA = ("def run(seed, carros, T=100000, pizarra=1, compat=0, rep_acum=0, escala=1, telem=True, diag=1, mundo_n=None, "
               "fundador_limpio=0):")
FIRMA_NUEVA = ("def run(seed, carros, T=100000, pizarra=1, compat=0, rep_acum=0, escala=1, telem=True, diag=1, mundo_n=None, "
               "fundador_limpio=0, estacion=0, parche=0, quieto=0):")
ANCLAS = [   # cada ancla empieza con salto de linea: casa una LINEA ENTERA con su sangria (no un pedazo de una linea mas sangrada)
    (FIRMA_VIEJA, FIRMA_NUEVA),
    ("\n    instancias = [1] * n\n",
     "\n    instancias = [1] * n\n"
     "    _mw = (MundoLibre(seed, L, n, T, estacion, parche, quieto) if (estacion or parche or quieto) else None)\n"),
    ("\n            if x not in objs: objs[x] = TIPOS[int(rng.integers(len(TIPOS)))]\n",
     "\n            if x not in objs:\n"
     "                _k = TIPOS[int(rng.integers(len(TIPOS)))]\n"
     "                if _mw is not None: x, _k = _mw.nace_obj(x, _k, objs)\n"
     "                objs[x] = _k\n"),
    ("\n        foto = tuple((l.id, l.pos, objs.get(l.pos), l.ult_mordida) for l in lin)\n",
     "\n        foto = tuple((l.id, l.pos, objs.get(l.pos), l.ult_mordida) for l in lin)\n"
     "        if _mw is not None: _mw.paso(t, lin, objs)\n"),
    ("\n            l.pos = (l.pos + mov) % L; pos = l.pos\n",
     "\n            l.pos = (l.pos + mov) % L; pos = l.pos\n"
     "            if _mw is not None: _mw.mov[i] = mov\n"),
    ("\n            l.E -= M['costo']; l.Ag -= M['costo_a']\n",
     "\n            if _mw is None or not _mw.quieto_de(l.i): l.E -= M['costo']; l.Ag -= M['costo_a']\n"
     "            else: l.E -= M['costo'] * _mw.fq; l.Ag -= M['costo_a'] * _mw.fq\n"),
    ("\n    return dict(linajes=out, pizarra_log=piz_log,\n",
     "\n    _ret = dict(linajes=out, pizarra_log=piz_log,\n"),
    ("\n                           rng_mundo_estado=_estado(rng)))\n",
     "\n                           rng_mundo_estado=_estado(rng)))\n"
     "    if _mw is not None: _ret['pista']['libre'] = _mw.info()\n"
     "    return _ret\n"),
]
_RUN = [None]


def h16(p): return hashlib.sha256(open(p, 'rb').read()).hexdigest()[:16]
def h16s(s): return hashlib.sha256(s.encode('utf-8')).hexdigest()[:16]


class MundoLibre:
    """Estacion, parche y quieto. Reglas LOCALES (la letra que nace, la celda donde nace, el cuerpo que no se movio).
    Una sola rng propia [seed, 0, 21, 0]; el rng del mundo de la pista hace EXACTAMENTE los mismos sorteos que en la pista vieja."""
    MALA = {'A': 'B', 'C': 'D'}; BUENA = {'B': 'A', 'D': 'C'}

    def __init__(self, seed, L, n, T, estacion, parche, quieto):
        self.r = np.random.default_rng([int(seed), 0, ETQ_LIBRE, 0])
        self.L = L; self.n = n; self.T = T
        self.est = int(bool(estacion)); self.par = int(bool(parche)); self.qui = int(bool(quieto))
        self.z0 = int(self.r.integers(L)) if self.par else None
        self.t = 0; self.s = 0.0; self.celdas = ()
        self.mov = [1] * n                   # mov de fase A de ESTE paso (lo escribe la pista)
        self.fq = 1.0 - QUIETO_AHORRO
        self.a_mala = 0; self.a_buena = 0; self.mudadas = 0; self.sin_libre = 0; self.nacidos = 0; self.nacidos_AC = 0
        self.quietos = [0] * n; self.en_parche = [0] * n; self.pasos_escasez = 0
        self.comp_parche = {k: 0 for k in 'ABCD'}
        self._pon(0)

    def _pon(self, t):
        self.t = t
        self.s = -math.sin(2.0 * math.pi * t / EST_P) if self.est else 0.0
        if self.par:
            c0 = (self.z0 + t // PAR_V) % self.L
            self.celdas = tuple((c0 + j) % self.L for j in range(PAR_W)); self._set = frozenset(self.celdas)

    def paso(self, t, lin, objs):   # al inicio del paso t (antes de la fase A); SOLO LECTURA salvo el reloj
        self._pon(t)
        if self.s > 0: self.pasos_escasez += 1
        if self.par:
            for l in lin:
                if l.pos in self._set: self.en_parche[l.i] += 1
            for x, k in objs.items():
                if x in self._set: self.comp_parche[k] += 1

    def nace_obj(self, x, k, objs):
        """(x, letra) que sorteo la pista -> (x, letra) que nace. x ya esta libre."""
        self.nacidos += 1
        if self.est:
            if self.s > 0 and k in self.MALA and self.r.random() < EST_AMP * self.s: k = self.MALA[k]; self.a_mala += 1
            elif self.s < 0 and k in self.BUENA and self.r.random() < EST_AMP * (-self.s): k = self.BUENA[k]; self.a_buena += 1
        if k in ('A', 'C'): self.nacidos_AC += 1
        if self.par and k in ('A', 'C') and self.r.random() < PAR_Q:
            lib = [c for c in self.celdas if c not in objs]
            if lib: x = lib[int(self.r.integers(len(lib)))]; self.mudadas += 1
            else: self.sin_libre += 1
        return x, k

    def quieto_de(self, i):
        q = self.qui and self.mov[i] == 0
        if q: self.quietos[i] += 1
        self.mov[i] = 1
        return q

    def info(self):
        T = max(1, self.T)
        return dict(estacion=self.est, parche=self.par, quieto=self.qui, EST_P=EST_P, EST_AMP=EST_AMP, PAR_W=PAR_W, PAR_V=PAR_V,
                    PAR_Q=PAR_Q, QUIETO_AHORRO=QUIETO_AHORRO, z0=self.z0, nacidos=self.nacidos, nacidos_AC=self.nacidos_AC,
                    a_mala=self.a_mala, a_buena=self.a_buena, mudadas=self.mudadas, sin_libre=self.sin_libre,
                    frac_escasez=round(self.pasos_escasez / T, 4), quietos=list(self.quietos),
                    frac_en_parche=[round(x / T, 4) for x in self.en_parche],
                    comp_parche={k: round(v / T, 4) for k, v in self.comp_parche.items()})


def construye():
    """-> (run, info). Aborta si un sha o un ancla no calzan."""
    if _RUN[0] is not None: return _RUN[0]
    rp = os.path.join(PISTA_D, 'pista.py'); rj = os.path.join(PISTA_D, 'juez.py')
    sp, sj = h16(rp), h16(rj)
    if sp != SHA_PISTA: raise SystemExit(f"PISTA_LIBRE: pista.py sha {sp} != fijado {SHA_PISTA}")
    if sj != SHA_JUEZ: raise SystemExit(f"PISTA_LIBRE: juez.py sha {sj} != fijado {SHA_JUEZ}")
    if os.path.abspath(P.__file__) != os.path.abspath(rp): raise SystemExit(f"PISTA_LIBRE: 'pista' importado de {P.__file__}")
    txt = open(rp, encoding='utf-8').read()
    a = txt.index("def run(seed, carros,"); b = txt.index("\n\n\n# claves de primer nivel")
    src = txt[a:b] + "\n"
    for viejo, nuevo in ANCLAS:
        k = src.count(viejo)
        if k != 1: raise SystemExit(f"PISTA_LIBRE: el ancla aparece {k} veces (debe ser 1): {viejo[:70]!r}")
        src = src.replace(viejo, nuevo)
    ns = dict(vars(P)); ns.update(MundoLibre=MundoLibre)
    exec(compile(src, '<pista_libre.run desde pista.py>', 'exec'), ns)
    _RUN[0] = (ns['run'], dict(sha_pista=sp, sha_juez=sj, sha_fuente_transformada=h16s(src), anclas=len(ANCLAS)))
    return _RUN[0]


def run(*a, **k):
    return construye()[0](*a, **k)
