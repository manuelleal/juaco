"""pista_grande.py — MUNDO MAS GRANDE Y CON MAS COSAS (30-sep-2026, creador; EXPLORATORIO). Preregistro: PREREGISTRO_grande.md.
Arnes: identidad_grande.py (salida entera en identidad_grande_salida.txt).

MISION: llegar a la AGI por este camino (organismo minimo con reglas locales, sin retropropagacion, peldanos preregistrados con
controles y replicas).

QUE ES: la PISTA VIEJA (experimentos/carrera_escuderias/pista.py, sha fijado SHA_PISTA, NO se toca) con tres perillas nuevas:
  G      (entero >= 1): el anillo es G veces mas largo con la MISMA densidad: L = 40 * esc * G, nobj = 4 * esc * G y esc * G sorteos
         de olvido por paso (la tasa de olvido POR OBJETO no cambia). Con G = 1 es la pista vieja.
  rica   (0/1): OASIS. Un arco de FRAC_ZONA * L celdas contiguas. La comida (A) y el agua (C) que se muerden DENTRO del oasis dan,
         ademas de su efecto nominal, +RICA_EXTRA en la OTRA necesidad: A -> (+0.8, +0.8), C -> (+0.8, +0.8). La comida rica SOLO
         existe alli (fuera del oasis A y C son las de siempre). La composicion y la densidad del oasis son las del resto del anillo
         (el spawn NO cambia: ni un sorteo de rng de mas); lo unico distinto es lo que da morder alli.
  lento  (0/1): PANTANO (VENENO LENTO). Un arco de FRAC_ZONA * L celdas, en el lado OPUESTO del oasis (inicio + L // 2). A y C
         mordidas dentro del pantano dan su efecto nominal inmediato (lo mismo que el cuerpo siente de una A o C cualquiera) y
         dejan una CARGA: durante LENTO_DUR pasos el cuerpo pierde LENTO_TASA de energia por paso POR CARGA (acumulable; total
         -1.0 E por mordida: una A del pantano vale neto -0.2 E, una C del pantano +0.8 Ag y -1.0 E). La carga es del CUERPO:
         muere con el (el cuerpo siguiente nace limpio).
CANAL (el mismo de siempre, sin informacion nueva): el carro ve las LETRAS (A B C D, sin letras nuevas: ningun carro necesita un
patron de retina inventado) y recibe en resultado() el dS que su cuerpo REALMENTE recibio en ESE paso (en el oasis, el doble
efecto; en el pantano, el nominal: la carga NO se anuncia, se siente despues en E, como cualquier costo). Nadie recibe la
posicion de las zonas. Premia moverse y RECORDAR DONDE (oasis) y no morder a ciegas (pantano); ningun carro existente tiene
memoria de lugar: mide cuanto margen queda.
ZONAS: inicio sorteado POR SEMILLA con una rng NUEVA [seed, 0, ETQ_ZONA=18, 0] (la pista usa 11-15; pista_pob 16-17; ERR-60):
no perturba ninguna corriente de la pista y no son sitios fijos entre semillas (trampa 4). Dentro de una corrida SI son fijas
(eso es lo que hay que recordar).

CONSTRUCCION POR ANCLAS (patron de pista_pob.py): construye() lee pista.py (sha SHA_PISTA; juez.py SHA_JUEZ), extrae run() y
aplica ANCLAS (cada una EXACTAMENTE una vez): firma nueva, esc *= G, la geografia (_gz) en el alta, en la mordida, en los costos,
en la muerte, al inicio del paso (conteo de solo lectura) y en la salida. Con G = 1, rica = 0, lento = 0: _gz = None, ningun gancho
actua y run() ES pista.run BIT A BIT (arnes I1). Todo lo demas (Linaje, _diag, _estado, cfg_fabrica, carga_carro...) es el de
pista.py: el codigo transformado se ejecuta con los globales de pista.
SALIDA NUEVA (solo si hay algo nuevo): pista['grande'] (G, zonas, parametros, composicion de las zonas) y por linaje
d['_carrera']['grande'] (fisica de solo lectura: pasos en oasis/pantano, mordidas por letra en cada zona, cargas, drenado, muertes
con carga activa). Las causas de muerte del juez NO cambian (una muerte por carga cuenta como 'hambre'; la carga se reporta aparte).
"""
import hashlib, os, sys
import numpy as np

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(AQUI))))
PISTA_D = os.path.join(RAIZ, 'experimentos', 'carrera_escuderias')
if PISTA_D not in sys.path: sys.path.insert(0, PISTA_D)
import pista as P

SHA_PISTA = '9f47c65e438e0ff4'   # pista.py (el de corre_v143.SHAS, pista_pob, patas_muro, o1_evo)
SHA_JUEZ = '6a68f640a7832f12'    # juez.py
ETQ_ZONA = 18
FRAC_ZONA = 0.10                 # cada zona: 10 % del anillo
RICA_EXTRA = 0.8                 # oasis: + esto en la OTRA necesidad (A y C)
LENTO_TASA = 0.0025              # pantano: energia por paso por carga (2.5 x el costo metabolico 0.001)
LENTO_DUR = 400                  # pasos por carga (total 1.0 E)
FABRICA_MUNDO = dict(G=1, rica=0, lento=0)

FIRMA_VIEJA = ("def run(seed, carros, T=100000, pizarra=1, compat=0, rep_acum=0, escala=1, telem=True, diag=1, mundo_n=None, "
               "fundador_limpio=0):")
FIRMA_NUEVA = ("def run(seed, carros, T=100000, pizarra=1, compat=0, rep_acum=0, escala=1, telem=True, diag=1, mundo_n=None, "
               "fundador_limpio=0, G=1, rica=0, lento=0, rica_extra=RICA_EXTRA, lento_tasa=LENTO_TASA, lento_dur=LENTO_DUR):")
ANCLAS = [
    (FIRMA_VIEJA, FIRMA_NUEVA),
    ("    esc = int(mundo_n) if mundo_n is not None else (n if escala else 1)\n",
     "    esc = int(mundo_n) if mundo_n is not None else (n if escala else 1)\n"
     "    if int(G) != G or G < 1: raise SystemExit(f'PISTA_GRANDE: G entero >= 1 (hay {G})')\n"
     "    esc = esc * int(G)\n"),
    ("    instancias = [1] * n\n",
     "    instancias = [1] * n\n"
     "    _gz = (Geografia(seed, L, n, T, rica, lento, rica_extra, lento_tasa, lento_dur) if (rica or lento) else None)\n"),
    ("        foto = tuple((l.id, l.pos, objs.get(l.pos), l.ult_mordida) for l in lin)\n",
     "        foto = tuple((l.id, l.pos, objs.get(l.pos), l.ult_mordida) for l in lin)\n"
     "        if _gz is not None: _gz.paso(lin, objs, t)\n"),
    ("_dS = EFECTO[VAL_VIVO[kk]]; ",
     "_dS = (EFECTO[VAL_VIVO[kk]] if _gz is None else _gz.muerde(l, kk, pos, t, EFECTO[VAL_VIVO[kk]])); "),
    ("            l.E -= M['costo']; l.Ag -= M['costo_a']\n",
     "            l.E -= M['costo']; l.Ag -= M['costo_a']\n"
     "            if _gz is not None: _gz.costo(l, t)\n"),
    ("                l.deaths += 1; l.mnec[0 if por_E else 1] += 1; l.E = .6; l.Ag = .6\n",
     "                if _gz is not None: _gz.muere(l, t, por_E)\n"
     "                l.deaths += 1; l.mnec[0 if por_E else 1] += 1; l.E = .6; l.Ag = .6\n"),
    ("        if diag: d['_carrera']['diag'] = _diag(l, T)\n",
     "        if diag: d['_carrera']['diag'] = _diag(l, T)\n"
     "        if _gz is not None: d['_carrera']['grande'] = _gz.salida(i)\n"),
    ("    return dict(linajes=out, pizarra_log=piz_log,\n",
     "    _ret = dict(linajes=out, pizarra_log=piz_log,\n"),
    ("                           rng_mundo_estado=_estado(rng)))\n",
     "                           rng_mundo_estado=_estado(rng)))\n"
     "    if _gz is not None or int(G) != 1: _ret['pista']['grande'] = dict(G=int(G), **({} if _gz is None else _gz.info()))\n"
     "    return _ret\n"),
]
_RUN = [None]


def h16(p): return hashlib.sha256(open(p, 'rb').read()).hexdigest()[:16]
def h16s(s): return hashlib.sha256(s.encode('utf-8')).hexdigest()[:16]


class Geografia:
    """Oasis y pantano (reglas LOCALES: dependen solo de la celda donde se muerde y del cuerpo que muerde). Sin rng despues del alta."""

    def __init__(self, seed, L, n, T, rica, lento, rica_extra, lento_tasa, lento_dur):
        zr = np.random.default_rng([int(seed), 0, ETQ_ZONA, 0])
        self.z0 = int(zr.integers(L)); self.W = max(1, int(round(L * FRAC_ZONA))); self.L = L; self.T = T
        self.rica = int(bool(rica)); self.lento = int(bool(lento))
        self.rica_extra = float(rica_extra); self.lento_tasa = float(lento_tasa); self.lento_dur = int(lento_dur)
        self.oasis = frozenset((self.z0 + j) % L for j in range(self.W)) if rica else frozenset()
        self.pantano = frozenset((self.z0 + L // 2 + j) % L for j in range(self.W)) if lento else frozenset()
        if self.oasis & self.pantano: raise SystemExit("PISTA_GRANDE: oasis y pantano se tocan")
        z = lambda: [0] * n
        self.p_oasis = z(); self.p_pantano = z()
        self.m_oasis = [{k: 0 for k in 'ABCD'} for _ in range(n)]; self.m_pantano = [{k: 0 for k in 'ABCD'} for _ in range(n)]
        self.m_total = [{k: 0 for k in 'ABCD'} for _ in range(n)]
        self.cargas = [[] for _ in range(n)]; self.n_cargas = z(); self.drenado = [0.0] * n
        self.muertes = z(); self.muertes_carga = z(); self.muertes_carga_E = z(); self.max_cargas = z()
        self.comp_oasis = {k: 0 for k in 'ABCD'}; self.comp_pantano = {k: 0 for k in 'ABCD'}; self.comp_resto = {k: 0 for k in 'ABCD'}

    def paso(self, lin, objs, t):   # SOLO LECTURA, al inicio del paso
        for l in lin:
            if l.pos in self.oasis: self.p_oasis[l.i] += 1
            elif l.pos in self.pantano: self.p_pantano[l.i] += 1
        for x, k in objs.items():
            (self.comp_oasis if x in self.oasis else (self.comp_pantano if x in self.pantano else self.comp_resto))[k] += 1

    def muerde(self, l, kk, pos, t, dS):
        """dS nominal -> dS que el cuerpo recibe AHORA (el que la pista aplica y devuelve en resultado())."""
        self.m_total[l.i][kk] += 1
        if pos in self.oasis:
            self.m_oasis[l.i][kk] += 1
            if kk == 'A': return (dS[0], dS[1] + self.rica_extra)
            if kk == 'C': return (dS[0] + self.rica_extra, dS[1])
        elif pos in self.pantano:
            self.m_pantano[l.i][kk] += 1
            if kk in ('A', 'C') and self.lento_tasa > 0 and self.lento_dur > 0:
                self.cargas[l.i].append(t + self.lento_dur); self.n_cargas[l.i] += 1
                self.max_cargas[l.i] = max(self.max_cargas[l.i], len(self.cargas[l.i]))
        return dS

    def costo(self, l, t):
        c = self.cargas[l.i]
        if not c: return
        c[:] = [x for x in c if x > t]        # activa en los costos de t0 .. t0 + dur - 1
        if c:
            d = self.lento_tasa * len(c); l.E -= d; self.drenado[l.i] += d

    def muere(self, l, t, por_E):
        self.muertes[l.i] += 1
        if self.cargas[l.i]:
            self.muertes_carga[l.i] += 1; self.muertes_carga_E[l.i] += int(por_E)
        self.cargas[l.i] = []                 # la carga es del CUERPO

    def salida(self, i):
        return dict(pasos_oasis=self.p_oasis[i], pasos_pantano=self.p_pantano[i], mord_oasis=dict(self.m_oasis[i]),
                    mord_pantano=dict(self.m_pantano[i]), mord_total=dict(self.m_total[i]), cargas=self.n_cargas[i],
                    max_cargas=self.max_cargas[i], drenado=round(self.drenado[i], 6), muertes=self.muertes[i],
                    muertes_con_carga=self.muertes_carga[i], muertes_con_carga_E=self.muertes_carga_E[i])

    def info(self):
        T = max(1, self.T)
        return dict(z0=self.z0, W=self.W, frac_zona=FRAC_ZONA, rica=self.rica, lento=self.lento, rica_extra=self.rica_extra,
                    lento_tasa=self.lento_tasa, lento_dur=self.lento_dur,
                    oasis=([self.z0, (self.z0 + self.W - 1) % self.L] if self.rica else None),
                    pantano=([(self.z0 + self.L // 2) % self.L, (self.z0 + self.L // 2 + self.W - 1) % self.L] if self.lento else None),
                    comp_oasis={k: round(v / T, 4) for k, v in self.comp_oasis.items()},
                    comp_pantano={k: round(v / T, 4) for k, v in self.comp_pantano.items()},
                    comp_resto={k: round(v / T, 4) for k, v in self.comp_resto.items()})


def construye():
    """-> (run, info). Aborta si un sha o un ancla no calzan."""
    if _RUN[0] is not None: return _RUN[0]
    rp = os.path.join(PISTA_D, 'pista.py'); rj = os.path.join(PISTA_D, 'juez.py')
    sp, sj = h16(rp), h16(rj)
    if sp != SHA_PISTA: raise SystemExit(f"PISTA_GRANDE: pista.py sha {sp} != fijado {SHA_PISTA}")
    if sj != SHA_JUEZ: raise SystemExit(f"PISTA_GRANDE: juez.py sha {sj} != fijado {SHA_JUEZ}")
    if os.path.abspath(P.__file__) != os.path.abspath(rp): raise SystemExit(f"PISTA_GRANDE: 'pista' importado de {P.__file__}")
    txt = open(rp, encoding='utf-8').read()
    a = txt.index("def run(seed, carros,"); b = txt.index("\n\n\n# claves de primer nivel")
    src = txt[a:b] + "\n"
    for viejo, nuevo in ANCLAS:
        k = src.count(viejo)
        if k != 1: raise SystemExit(f"PISTA_GRANDE: el ancla aparece {k} veces (debe ser 1): {viejo[:70]!r}")
        src = src.replace(viejo, nuevo)
    ns = dict(vars(P)); ns.update(Geografia=Geografia, RICA_EXTRA=RICA_EXTRA, LENTO_TASA=LENTO_TASA, LENTO_DUR=LENTO_DUR)
    exec(compile(src, '<pista_grande.run desde pista.py>', 'exec'), ns)
    _RUN[0] = (ns['run'], dict(sha_pista=sp, sha_juez=sj, sha_fuente_transformada=h16s(src), anclas=len(ANCLAS)))
    return _RUN[0]


def run(*a, **k):
    return construye()[0](*a, **k)
