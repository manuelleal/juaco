"""mundo_escalera.py — EL MUNDO DE LA ESCALERA, peldano 1: un OASIS que hay que RECORDAR (30-sep-2026, ingeniero genetico Fable).
Preregistro: PREREGISTRO_p1.md. Arnes: identidad_p1.py. Plan completo: ESCALERA.md.

MISION: llegar a la AGI por este camino (organismo minimo con reglas locales, sin retropropagacion, peldanos preregistrados con
controles y replicas).

QUE ES: la PISTA de la carrera (experimentos/carrera_escuderias/pista.py, sha fijado SHA_PISTA, NO se toca) con UNA perilla de mundo
(oasis) y dos parametros:
  oasis  (0/1): un arco de FRAC_ZONA * L celdas contiguas, sorteado POR SEMILLA. La comida (A) y el agua (C) mordidas DENTRO dan,
         ademas de su efecto nominal, +extra en la OTRA necesidad: A -> (+0.8, +extra), C -> (+extra, +0.8). FUERA del oasis A y C
         dan su efecto nominal multiplicado por pobre: A -> (+0.8*pobre, 0), C -> (0, +0.8*pobre). B y D no cambian en ningun sitio.
         El spawn NO cambia (ni un sorteo de rng de mas): el oasis tiene la densidad y la composicion del resto del anillo; lo unico
         distinto es lo que da morder alli. Con oasis = 0: run() ES pista.run BIT A BIT (arnes M1).
  extra  (0.8 de fabrica) y pobre (0.5 de fabrica). Con extra 0.8 y pobre 1.0 el mundo ES pista_grande.run(G=1, rica=1, lento=0) de
         o1_evo/grande (misma rng de zona [seed, 0, 18, 0], mismo z0 y W): arnes M2, que ata este mundo al que ya existe.
POR QUE pobre < 1 ("el mundo tiene que PAGAR la capacidad", ESTADO 29-sep): con pobre 1.0 el oasis es un regalo que nadie necesita
(grande: nadie lo usa y O1 cruza igual). Con pobre 0.5 el mismo bocado vale la mitad fuera y (0.8 + 0.8) dentro: recordar DONDE
paga 4 veces por mordida, y evitar (no ir) no es gratis: fuera hay que morder el doble, y morder el doble repone el doble de B/D.
CANAL (el mismo de siempre): el carro ve las LETRAS (A B C D, sin letras nuevas) y recibe en resultado() el dS que su cuerpo
REALMENTE recibio en ESE paso (dentro: el doble; fuera: el pobre). NADIE recibe la posicion del oasis: lo unico que puede hacer
un carro es asociar lo que sintio con DONDE lo sintio. Eso es la memoria de lugar del peldano 1 (construye_p1.py).
ZONA: inicio sorteado con una rng NUEVA [seed, 0, ETQ_ZONA=18, 0] (la pista usa 11-15; pista_pob 16-17; pista_grande 18 con la
misma formula, a proposito): no perturba ninguna corriente de la pista y no es un sitio fijo entre semillas (trampa 4). Dentro de
una corrida SI es fijo (eso es lo que hay que recordar; que se mueva es el mundo del peldano 5).

CONSTRUCCION POR ANCLAS (patron de pista_grande.py / pista_pob.py): construye() lee pista.py (sha SHA_PISTA; juez.py SHA_JUEZ),
extrae run() y aplica ANCLAS (cada una EXACTAMENTE una vez): firma nueva, el oasis (_oz) en el alta, en el conteo de solo lectura al
inicio del paso, en la mordida y en la salida. Todo lo demas (Linaje, _diag, _estado, cfg_fabrica, carga_carro...) es el de pista.py:
el codigo transformado se ejecuta con los globales de pista.
SALIDA NUEVA (solo si oasis = 1): pista['oasis'] (z0, W, extra, pobre, composicion dentro/fuera) y por linaje
d['_carrera']['oasis'] (fisica de solo lectura: pasos dentro, mordidas por letra dentro y fuera). Las causas de muerte del juez y
todo lo fisico que lee juez.resumen_linaje NO cambian de nombre ni de forma.
"""
import hashlib, os, sys
import numpy as np

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(AQUI)))
PISTA_D = os.path.join(RAIZ, 'experimentos', 'carrera_escuderias')
if PISTA_D not in sys.path: sys.path.insert(0, PISTA_D)
import pista as P

SHA_PISTA = '9f47c65e438e0ff4'   # pista.py (el de corre_v143.SHAS, o1_evo, pista_grande)
SHA_JUEZ = '6a68f640a7832f12'    # juez.py
ETQ_ZONA = 18
FRAC_ZONA = 0.10                 # el oasis: 10 % del anillo (36 celdas en L = 360)
EXTRA = 0.8                      # dentro: + esto en la OTRA necesidad (A y C)
POBRE = 0.5                      # fuera: A y C valen esto por su efecto nominal
FABRICA_MUNDO = dict(oasis=0, extra=EXTRA, pobre=POBRE)

FIRMA_VIEJA = ("def run(seed, carros, T=100000, pizarra=1, compat=0, rep_acum=0, escala=1, telem=True, diag=1, mundo_n=None, "
               "fundador_limpio=0):")
FIRMA_NUEVA = ("def run(seed, carros, T=100000, pizarra=1, compat=0, rep_acum=0, escala=1, telem=True, diag=1, mundo_n=None, "
               "fundador_limpio=0, oasis=0, extra=EXTRA, pobre=POBRE, dens=0.0, vista_r=0):")
ANCLAS = [
    (FIRMA_VIEJA, FIRMA_NUEVA),
    ("    instancias = [1] * n\n",
     "    instancias = [1] * n\n"
     "    _oz = (Oasis(seed, L, n, T, extra, pobre, dens, vista_r) if oasis else None)\n"),
    # P1b (humo 2): dens > 0 -> una fraccion dens de lo que el mundo repone nace DENTRO del oasis (alli crece la comida); consume sorteos del
    # rng del mundo SOLO con oasis 1 y dens > 0 (con dens 0 el spawn es el de la pista, sorteo por sorteo).
    ("            x = int(rng.integers(L))\n            if x not in objs: objs[x] = TIPOS[int(rng.integers(len(TIPOS)))]\n",
     "            x = int(rng.integers(L)) if (_oz is None or not _oz.dens) else _oz.sitio(rng)\n"
     "            if x not in objs: objs[x] = TIPOS[int(rng.integers(len(TIPOS)))]\n"),
    ("        foto = tuple((l.id, l.pos, objs.get(l.pos), l.ult_mordida) for l in lin)\n",
     "        foto = tuple((l.id, l.pos, objs.get(l.pos), l.ult_mordida) for l in lin)\n"
     "        if _oz is not None: _oz.paso(lin, objs)\n"),
    # P1b (humo 2): vista_r > 0 -> VISTA PARCIAL (se llama vista_r porque 'vista' ya es un local de pista.run: el MappingProxy de objs): el carro solo recibe los objetos a distancia <= vista de su cuerpo (la pista entrega TODOS).
    ("            o['t'] = t; o['pos'] = l.pos; o['E'] = l.E; o['Ag'] = l.Ag; o['cuerpos'] = foto; o['pizarra'] = piz_t\n",
     "            o['t'] = t; o['pos'] = l.pos; o['E'] = l.E; o['Ag'] = l.Ag; o['cuerpos'] = foto; o['pizarra'] = piz_t\n"
     "            if _oz is not None and _oz.vista: o['objs'] = _oz.ve(l.pos, objs)\n"),
    ("_dS = EFECTO[VAL_VIVO[kk]]; ",
     "_dS = (EFECTO[VAL_VIVO[kk]] if _oz is None else _oz.muerde(l, kk, pos, EFECTO[VAL_VIVO[kk]])); "),
    ("        if diag: d['_carrera']['diag'] = _diag(l, T)\n",
     "        if diag: d['_carrera']['diag'] = _diag(l, T)\n"
     "        if _oz is not None: d['_carrera']['oasis'] = _oz.salida(i)\n"),
    ("    return dict(linajes=out, pizarra_log=piz_log,\n",
     "    _ret = dict(linajes=out, pizarra_log=piz_log,\n"),
    ("                           rng_mundo_estado=_estado(rng)))\n",
     "                           rng_mundo_estado=_estado(rng)))\n"
     "    if _oz is not None: _ret['pista']['oasis'] = _oz.info()\n"
     "    return _ret\n"),
]
_RUN = [None]


def h16(p): return hashlib.sha256(open(p, 'rb').read()).hexdigest()[:16]
def h16s(s): return hashlib.sha256(s.encode('utf-8')).hexdigest()[:16]


class Oasis:
    """El oasis (regla LOCAL: depende solo de la celda donde se muerde). Sin rng despues del alta."""

    def __init__(self, seed, L, n, T, extra, pobre, dens=0.0, vista=0):
        zr = np.random.default_rng([int(seed), 0, ETQ_ZONA, 0])
        self.z0 = int(zr.integers(L)); self.W = max(1, int(round(L * FRAC_ZONA))); self.L = L; self.T = T
        self.extra = float(extra); self.pobre = float(pobre); self.dens = float(dens); self.vista = int(vista)
        if not 0 <= self.dens <= 1 or self.vista < 0: raise SystemExit(f"MUNDO_ESCALERA: dens en [0, 1] (hay {dens}) y vista >= 0 (hay {vista})")
        self.celdas = frozenset((self.z0 + j) % L for j in range(self.W))
        self.p_dentro = [0] * n
        self.m_dentro = [{k: 0 for k in 'ABCD'} for _ in range(n)]; self.m_fuera = [{k: 0 for k in 'ABCD'} for _ in range(n)]
        self.comp_dentro = {k: 0 for k in 'ABCD'}; self.comp_fuera = {k: 0 for k in 'ABCD'}

    def paso(self, lin, objs):   # SOLO LECTURA, al inicio del paso
        for l in lin:
            if l.pos in self.celdas: self.p_dentro[l.i] += 1
        for x, k in objs.items():
            (self.comp_dentro if x in self.celdas else self.comp_fuera)[k] += 1

    def muerde(self, l, kk, pos, dS):
        """dS nominal -> dS que el cuerpo recibe AHORA (el que la pista aplica y devuelve en resultado())."""
        if pos in self.celdas:
            self.m_dentro[l.i][kk] += 1
            if kk == 'A': return (dS[0], dS[1] + self.extra)
            if kk == 'C': return (dS[0] + self.extra, dS[1])
            return dS
        self.m_fuera[l.i][kk] += 1
        if kk in ('A', 'C'): return (dS[0] * self.pobre, dS[1] * self.pobre)
        return dS

    def sitio(self, rng):
        """P1b: donde nace un objeto nuevo: dentro del oasis con probabilidad dens (celda uniforme del arco), si no uniforme en el anillo."""
        if rng.random() < self.dens: return (self.z0 + int(rng.integers(self.W))) % self.L
        return int(rng.integers(self.L))

    def ve(self, pos, objs):
        """P1b: vista parcial: los objetos a distancia <= vista de pos (dict nuevo; la pista sigue teniendo todos)."""
        L = self.L; R = self.vista
        return {x: k for x, k in objs.items() if min((x - pos) % L, (pos - x) % L) <= R}

    def salida(self, i):
        return dict(pasos_dentro=self.p_dentro[i], mord_dentro=dict(self.m_dentro[i]), mord_fuera=dict(self.m_fuera[i]))

    def bins(self, nb):
        """Que bins (de nb en el anillo) toca el oasis: para leer la memoria de lugar del carro contra la fisica (solo lectura)."""
        return sorted({(x * nb) // self.L for x in self.celdas})

    def info(self):
        T = max(1, self.T)
        return dict(z0=self.z0, W=self.W, frac_zona=FRAC_ZONA, extra=self.extra, pobre=self.pobre, dens=self.dens, vista=self.vista,
                    oasis=[self.z0, (self.z0 + self.W - 1) % self.L], bins30=self.bins(30),
                    comp_dentro={k: round(v / T, 4) for k, v in self.comp_dentro.items()},
                    comp_fuera={k: round(v / T, 4) for k, v in self.comp_fuera.items()})


def construye():
    """-> (run, info). Aborta si un sha o un ancla no calzan."""
    if _RUN[0] is not None: return _RUN[0]
    rp = os.path.join(PISTA_D, 'pista.py'); rj = os.path.join(PISTA_D, 'juez.py')
    sp, sj = h16(rp), h16(rj)
    if sp != SHA_PISTA: raise SystemExit(f"MUNDO_ESCALERA: pista.py sha {sp} != fijado {SHA_PISTA}")
    if sj != SHA_JUEZ: raise SystemExit(f"MUNDO_ESCALERA: juez.py sha {sj} != fijado {SHA_JUEZ}")
    if os.path.abspath(P.__file__) != os.path.abspath(rp): raise SystemExit(f"MUNDO_ESCALERA: 'pista' importado de {P.__file__}")
    txt = open(rp, encoding='utf-8').read()
    a = txt.index("def run(seed, carros,"); b = txt.index("\n\n\n# claves de primer nivel")
    src = txt[a:b] + "\n"
    for viejo, nuevo in ANCLAS:
        k = src.count(viejo)
        if k != 1: raise SystemExit(f"MUNDO_ESCALERA: el ancla aparece {k} veces (debe ser 1): {viejo[:70]!r}")
        src = src.replace(viejo, nuevo)
    ns = dict(vars(P)); ns.update(Oasis=Oasis, EXTRA=EXTRA, POBRE=POBRE)
    exec(compile(src, '<mundo_escalera.run desde pista.py>', 'exec'), ns)
    _RUN[0] = (ns['run'], dict(sha_pista=sp, sha_juez=sj, sha_fuente_transformada=h16s(src), anclas=len(ANCLAS)))
    return _RUN[0]


def run(*a, **k):
    return construye()[0](*a, **k)


if __name__ == '__main__':
    print(construye()[1])
