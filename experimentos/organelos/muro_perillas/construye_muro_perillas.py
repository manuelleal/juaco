"""construye_muro_perillas.py — construye POR ANCLAS el carro O1_MURO_GEN: O1 con SEIS mecanismos como GENES-DOSIS heredables
que pueden ARRANCAR EN CERO (apagados). Bloque "perillas del muro" (1-oct-2026, ingeniero genetico).

MISION: llegar a la AGI por este camino (organismo minimo con reglas locales, sin retropropagacion, peldanos preregistrados con
controles y replicas).

PRIMERA LINEA (honesta): O1 NO se puede "apagar" hacia el tronco (v14.3 / FABRICA): son ARQUITECTURAS DISTINTAS (tabla por letra del
linaje contra celdas Kenyon). La base de este mapa es "O1 con cada mecanismo neutralizado". El UNICO organismo de referencia que ya
existe con un mecanismo apagado es carrera_escuderias/carros/CTRL_O1_SINLIMPIA.py (O1 con `limpia = False`): el arnes prueba que
el gen LIMPIA en 0 (y el resto de fabrica) lo reproduce BIT A BIT (salida entera). Con todo en 1 el carro es O1 bit a bit.

ORIGEN (solo se LEE; sha16 fijado; cada ancla EXACTAMENTE una vez o aborta): carrera_escuderias/carros/O1.py (SHA_O1).

PIEZA NUEVA (perilla PERILLAS; con PERILLAS = 0 el carro es O1 bit a bit, salida ENTERA):
  GENOMA POR CUERPO = 6 genes CRUDOS (el cuerpo lee la constante tal cual, como O1_PAS de o1_evo; LIMPIA y HUECO: regla activa si > 0.5):
    gen      FABRICA   clip         APAGADO (provisional; el mapa decide)   que decide
    MARGEN   0.25      [0, 0.6]     0.0  (consigna EN U: letal, tabla_bb)   muerde lo bueno solo si la necesidad esta bajo U + MARGEN; 0.5 = "todo"
    PRUEBA   0.50      [0, 1.5]     0.5  (fabrica: 0 = prueba sin cautela)  prueba una letra desconocida solo si E y Ag > PRUEBA
    PEN_OTRO 0.35      [0, 1.5]     1.0  (sin reparto)                      factor al blanco si otro cuerpo esta mas cerca
    PISO     0.20      [0, 1.0]     1.0  (casi sin limpieza)                la limpieza no baja la necesidad golpeada de aqui
    LIMPIA   1         [0, 1.5]     0    (nunca muerde lo malo a sabiendas) regla v2 (0 == CTRL_O1_SINLIMPIA bit a bit)
    HUECO    1         [0, 1.5]     0    (sin blanco se queda quieto)       sin blanco va al centro del hueco mayor entre cuerpos
  D0 (3.0) y los pesos de urgencia (4/2/1) quedan fijos (no son decisiones comer/limpiar; o1_evo tampoco los toco).
  - MUTACION (una por nacimiento, en UN gen al azar ENTRE LOS DE PS_MUTA; serie: solo MARGEN, los otros cinco fijos en fabrica): g' = g - PS_DELTA + N(0, PS_SIGMA), recortado al clip. PS_DELTA = sesgo a la perdida
    (nulo de la deriva: el de perillas, misma regla). Sigma y delta los de perillas (a priori).
  - Primer fundador de cada linaje: PS_POR_LINAJE[indice] si PS_POR_LINAJE no es None (PISTA MIXTA: cada linaje con SU genoma fijo, tambien
    en cada refundacion; origen 3); si no, base = una entrada de SIEMBRA al azar si SIEMBRA no es None; si no, base = PS_BASE (APAGADO).
  - CAMARA CONTINUA (PS_CAMARA 1): cada REFUNDACION (ENMIENDA 5) copia, mutado, el genoma del cuerpo ACTUAL de OTRO linaje al azar.
  - Parto: la memoria del hijo lleva '_gen' = (genes del padre mutados, profundidad + 1). El resto de la memoria (tabla por letra) no cambia.
  - PS_LEE 0: los genes se heredan, mutan y viajan IGUAL pero el cuerpo NO los lee (decide con la fabrica): el carro es O1.
  - PS_TOPE (brazo pur, 5-oct): el cuerpo lee MARGEN = min(gen, PS_TOPE); el gen heredado muta y viaja libre por encima del tope. Con PS_TOPE None (o
    >= al gen) es identico a sel bit a bit; con PS_TOPE 0 el cuerpo se comporta como MARGEN 0.
  - Azar PROPIO (splitmix64 + Box-Muller en Python puro): no toca el rng del mundo ni el del cuerpo; pasa revisa_carro.
  - Telemetria de SOLO ESCRITURA en _TEL[indice]: 'vivos' = [t, genes, instancia, profundidad] cada 1000 pasos; 'fund' = [origen (0
    base, 1 siembra, 2 camara, 3 por linaje), genes, profundidad] por fundador; 'partos'. _VIVO[indice] = (genes, prof) del cuerpo actual.
  Memoria nueva: 6 floats y un entero por cuerpo. salida() NO cambia (es la de O1).
Genera en muro_perillas/carros/ (difieren SOLO en la linea PERILLAS y el nombre):
  O1_MURO_GEN    PERILLAS 1
  O1_MURO_GEN0   PERILLAS 0 (solo arnes: == O1 bit a bit)

    python experimentos/organelos/muro_perillas/construye_muro_perillas.py [--verifica]
"""
import argparse, ast, hashlib, os, sys

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(AQUI)))
ORIGEN = os.path.join(RAIZ, 'experimentos', 'carrera_escuderias', 'carros', 'O1.py')
SALIDA = os.path.join(AQUI, 'carros')
SHA_O1 = '99436afa2715f028'
SHA_SINLIMPIA = 'be029b0a1b8d6634'   # carrera_escuderias/carros/CTRL_O1_SINLIMPIA.py (referencia existente: LIMPIA apagada)
NL = '\n'
VARIANTES = [('O1_MURO_GEN', 1), ('O1_MURO_GEN0', 0)]
GENES = ('MARGEN', 'PRUEBA', 'PEN_OTRO', 'PISO', 'LIMPIA', 'HUECO')
APAGADO = (0.0, 0.5, 1.0, 1.0, 0.0, 0.0)   # APAGADO provisional (genetista, ficha 2): MARGEN 0, PRUEBA fabrica, PEN_OTRO 1, PISO 1, LIMPIA 0, HUECO 0
FABRICA = (0.25, 0.5, 0.35, 0.2, 1.0, 1.0)   # los literales de O1.py + reglas prendidas (el arnes lo comprueba)
ARRANQUE_MARGEN = 0.03                       # PASO B (5-oct 17:10, decidido ANTES de la serie): desde 0.0 la cadena no muta (humo_cadena T 20k: R0 0, 15 partos, profundidad 1: nadie pare y el reloj no corre); 0.03 = primer escalon medido (R0 0.83-0.89, 8-9 establecidos)
BASE = (ARRANQUE_MARGEN, 0.5, 0.35, 0.2, 1.0, 1.0)   # de donde arranca la seleccion del PASO B: MARGEN desde ARRANQUE, el resto de O1 en fabrica
DISENO = FABRICA                             # O1
CLIP = ((0.0, 0.6), (0.0, 1.5), (0.0, 1.5), (0.0, 1.0), (0.0, 1.5), (0.0, 1.5))
SIGMA = 0.03                                 # perillas (a priori)
DELTA = 0.01                                 # sesgo a la perdida (perillas)
MUTA = (0,)                                  # auditoria 5-oct (punto 3): indices de los genes que MUTAN; (0,) = SOLO MARGEN (todo el reloj cae en el gen de la letra); (0,1,2,3,4,5) = los seis
PER = "PERILLAS = {p}   # muro_perillas: LA UNICA LINEA QUE CAMBIA ENTRE VARIANTES (0 = O1 bit a bit)"


def modulo(p):
    return (NL + PER.format(p=p) + NL
            + f'SIEMBRA = None; PS_SEMILLA = 0; PS_SIGMA = {SIGMA!r}; PS_DELTA = {DELTA!r}; PS_LEE = 1; PS_CAMARA = 1; PS_POR_LINAJE = None; PS_MUTA = ' + repr(MUTA) + '; PS_TOPE = None   # muro_perillas: PS_TOPE = tope de LECTURA de MARGEN (brazo pur; None = sin tope); los fija el RUNNER por corrida (SIEMBRA None = PS_BASE; PS_LEE 0 = genes NEUTROS; PS_POR_LINAJE = pista mixta; PS_MUTA = genes que mutan)' + NL
            + '_PS_CNT = {}; _TEL = {}; _VIVO = {}   # muro_perillas: instancias por linaje, telemetria de SOLO ESCRITURA y genoma del cuerpo actual de cada linaje (el runner los borra antes de cada run)' + NL
            + 'PS_GENES = ' + repr(GENES) + '; PS_BASE = ' + repr(BASE) + '; PS_CLIP = ' + repr(CLIP) + NL
            + 'PS_APAGADO = ' + repr(APAGADO) + '; PS_FABRICA = ' + repr(FABRICA) + NL
            + '_PS_M64 = 18446744073709551615' + NL)


METODOS = '''
    # ================================================================ muro_perillas: 6 mecanismos de O1 como GENES-DOSIS heredables (arrancan en 0)
    def _ps_init(self, ctx):
        i = int(ctx['indice']); c = _PS_CNT.get(i, 0); _PS_CNT[i] = c + 1; self._psi = i; self._psc = c
        self._pss = ((int(PS_SEMILLA) * 1000003 + i * 10007 + c) * 2654435761 + 7703) & _PS_M64
        for _ in range(4): self._ps_u()
        otros = [_VIVO[j] for j in sorted(_VIVO) if j != i] if (PS_CAMARA and c > 0) else []
        if PS_POR_LINAJE is not None:   # PISTA MIXTA: cada linaje con SU genoma (fijo, tambien al refundar)
            b0 = [float(v) for v in PS_POR_LINAJE[i]]; p0 = 0; self._psfund = 3
        elif otros:   # CAMARA: la refundacion copia (mutado) el genoma del cuerpo actual de OTRO linaje al azar
            g, p0 = otros[int(self._ps_u() * len(otros)) % len(otros)]; b0 = list(g); self._psfund = 2
        elif SIEMBRA:
            e = SIEMBRA[int(self._ps_u() * len(SIEMBRA)) % len(SIEMBRA)]
            b0 = [float(e[k]) for k in PS_GENES]; p0 = int(e.get('prof', 0)); self._psfund = 1
        else:
            b0 = list(PS_BASE); p0 = 0; self._psfund = 0
        self._prof = int(p0) + 1
        self._ps_pon(self._ps_muta(b0))
        _TEL.setdefault(i, {}).setdefault('fund', []).append([self._psfund, list(self._gen), self._prof])

    def _ps_u(self):
        """generador PROPIO (splitmix64) -> uniforme en (0, 1). No toca el rng del mundo ni el del cuerpo."""
        self._pss = (self._pss + 0x9E3779B97F4A7C15) & _PS_M64
        z = self._pss
        z = ((z ^ (z >> 30)) * 0xBF58476D1CE4E5B9) & _PS_M64
        z = ((z ^ (z >> 27)) * 0x94D049BB133111EB) & _PS_M64
        z ^= z >> 31
        return ((z >> 11) + 0.5) / 9007199254740992.0

    def _ps_muta(self, b):
        """UNA mutacion por nacimiento, en UN gen al azar: d - PS_DELTA + N(0, PS_SIGMA), recortado. Los demas se copian igual."""
        out = [float(x) for x in b]; j = PS_MUTA[int(self._ps_u() * len(PS_MUTA)) % len(PS_MUTA)]   # solo los genes de PS_MUTA mutan (serie: solo MARGEN)
        z = math.sqrt(-2.0 * math.log(self._ps_u())) * math.cos(2.0 * math.pi * self._ps_u())
        out[j] = float(min(max(out[j] - PS_DELTA + PS_SIGMA * z, PS_CLIP[j][0]), PS_CLIP[j][1]))
        return out

    def _ps_pon(self, g):
        """El cuerpo lee las constantes CRUDAS; LIMPIA y HUECO: regla activa si el gen > 0.5."""
        self._gen = [float(x) for x in g]
        _VIVO[self._psi] = (list(self._gen), int(self._prof))
        d = self._gen if PS_LEE else list(PS_FABRICA)   # PS_LEE 0: se heredan y mutan pero NO se leen (el cuerpo decide como O1)
        self.MARGEN, self.PRUEBA, self.PEN_OTRO, self.PISO = (d[0] if PS_TOPE is None else min(d[0], float(PS_TOPE))), d[1], d[2], d[3]   # pur: el cuerpo lee min(gen, tope); el gen heredado no se toca
        self.LIMPIA = int(d[4] > 0.5); self.HUECO = int(d[5] > 0.5)

    def _ps_tel(self, t):
        _TEL.setdefault(self._psi, {}).setdefault('vivos', []).append([int(t), list(self._gen), int(self._psc), int(self._prof)])
'''


def anclas(nombre, p):
    return [
        ('"""carros/O1.py — escuderia O1 (Opus). Carrera de escuderias, ronda 1.' + NL,
         f'"""{nombre}.py — muro_perillas: O1 con 6 mecanismos (MARGEN, PRUEBA, PEN_OTRO, PISO, LIMPIA, HUECO) como GENES-DOSIS heredables.' + NL
         + f'GENERADO por experimentos/organelos/muro_perillas/construye_muro_perillas.py desde carrera_escuderias/carros/O1.py (sha {SHA_O1}).' + NL
         + f'NO editar a mano. PERILLAS = {p}. Con PERILLAS = 0 es O1 bit a bit; con los genes de FABRICA es O1; con LIMPIA 0 es CTRL_O1_SINLIMPIA.' + NL + NL
         + 'carros/O1.py — escuderia O1 (Opus). Carrera de escuderias, ronda 1.' + NL),
        ('import numpy as np' + NL, 'import math' + NL + 'import numpy as np' + NL),
        ('PISO = 0.2         # v2: la limpieza no baja la necesidad golpeada de aqui (si la ventana de parto no corre)' + NL,
         'PISO = 0.2         # v2: la limpieza no baja la necesidad golpeada de aqui (si la ventana de parto no corre)' + NL + modulo(p)),
        ('        self.st = dict(mord={}, pruebas=0, sin_blanco=0, pasos=0, cuerpos=0, partos=0, limpias=0)' + NL,
         '        self.st = dict(mord={}, pruebas=0, sin_blanco=0, pasos=0, cuerpos=0, partos=0, limpias=0)' + NL
         + '        self.MARGEN, self.PRUEBA, self.PEN_OTRO, self.PISO, self.LIMPIA, self.HUECO = MARGEN, PRUEBA, PEN_OTRO, PISO, 1, 1   # muro_perillas: mecanismos por cuerpo (fabrica)' + NL
         + '        if PERILLAS: self._ps_init(ctx)   # muro_perillas: genes del fundador (por linaje, de la camara, de SIEMBRA o de PS_BASE), mutados' + NL),
        ('            if x >= self.U + MARGEN: continue' + NL, '            if x >= self.U + self.MARGEN: continue' + NL),
        ('        if v is None: return min(lev) > PRUEBA' + NL, '        if v is None: return min(lev) > self.PRUEBA' + NL),
        ('                piso = self.U if min(lev) >= self.U else PISO' + NL, '                piso = self.U if min(lev) >= self.U else self.PISO' + NL),
        ('                if min(lev) > PRUEBA and (desc is None or d < desc[0]): desc = (d, x)' + NL,
         '                if min(lev) > self.PRUEBA and (desc is None or d < desc[0]): desc = (d, x)' + NL),
        ('            if otros and min(self._dist(o, x) for o in otros) < d: s *= PEN_OTRO' + NL,
         '            if otros and min(self._dist(o, x) for o in otros) < d: s *= self.PEN_OTRO' + NL),
        ('        limpia = mejor is None and min(lev) < self.U + MARGEN' + NL,
         '        limpia = bool(self.LIMPIA) and mejor is None and min(lev) < self.U + self.MARGEN   # muro_perillas: LIMPIA 0 == CTRL_O1_SINLIMPIA (limpia = False)' + NL),
        ("            tgt = self._hueco(pos, otros); self.st['sin_blanco'] += 1" + NL,
         "            tgt = (self._hueco(pos, otros) if self.HUECO else pos); self.st['sin_blanco'] += 1   # muro_perillas: HUECO 0 = se queda quieto" + NL),
        ('    def fin_paso(self, info):' + NL + '        return None' + NL,
         '    def fin_paso(self, info):' + NL
         + "        if PERILLAS and info['t'] % 1000 == 0: self._ps_tel(info['t'])   # muro_perillas: genes del vivo (solo escritura)" + NL
         + '        return None' + NL),
        ('        return {k: (self.suma[k].copy(), self.n[k]) for k in self.n}' + NL,
         '        _m = {k: (self.suma[k].copy(), self.n[k]) for k in self.n}' + NL
         + "        if PERILLAS: _m['_gen'] = (self._ps_muta(self._gen), self._prof + 1); _TEL.setdefault(self._psi, {})['partos'] = _TEL[self._psi].get('partos', 0) + 1" + NL
         + '        return _m' + NL),
        ("        m = info.get('memoria')" + NL + '        if m:' + NL,
         "        m = info.get('memoria')" + NL
         + "        if PERILLAS and m and '_gen' in m: m = dict(m); _g = m.pop('_gen'); self._prof = int(_g[1]); self._ps_pon(_g[0])   # muro_perillas: el hijo toma sus genes" + NL
         + '        if m:' + NL),
        (NL + NL + 'def crea(ctx):' + NL, METODOS.replace('\n', NL) + NL + NL + 'def crea(ctx):' + NL),
    ]


def h16b(b): return hashlib.sha256(b).hexdigest()[:16]
def h16(p): return h16b(open(p, 'rb').read())


def construye(nombre, p):
    src = open(ORIGEN, 'rb').read()
    if h16b(src) != SHA_O1: raise SystemExit(f"origen {ORIGEN} sha {h16b(src)} != {SHA_O1}")
    txt = src.decode('utf-8')
    for a, rep in anclas(nombre, p):
        n = txt.count(a)
        if n != 1: raise SystemExit(f"ancla {a[:70]!r} aparece {n} veces (se exige 1)")
        txt = txt.replace(a, rep)
    # las 4 constantes ya no se leen como GLOBALES en ningun metodo, salvo la linea de __init__ que las copia (ast)
    for f in ast.walk(ast.parse(txt)):
        if isinstance(f, ast.FunctionDef):
            usos = [nd.lineno for nd in ast.walk(f) if isinstance(nd, ast.Name) and nd.id in GENES[:4] and isinstance(nd.ctx, ast.Load)]
            if usos and not (f.name == '__init__' and len(usos) == 4 and len(set(usos)) == 1):
                raise SystemExit(f"{f.name}: quedan usos de {GENES[:4]} como globales en las lineas {usos}")
    return txt.encode('utf-8')


def todas():
    return {n: construye(n, p) for n, p in VARIANTES}


def main(argv=None):
    ap = argparse.ArgumentParser(allow_abbrev=False)
    ap.add_argument('--verifica', action='store_true')
    a = ap.parse_args(argv)
    T = todas()
    l1 = T['O1_MURO_GEN'].decode().split(NL); l0 = T['O1_MURO_GEN0'].decode().split(NL)
    dif = [i for i, (x, y) in enumerate(zip(l1, l0)) if x != y]
    if len(l1) != len(l0) or len(dif) != 3: raise SystemExit(f"las variantes difieren en {dif} (se esperan 3 lineas: nombre, PERILLAS del encabezado y la perilla)")
    ok = True
    for n, b in T.items():
        ruta = os.path.join(SALIDA, n + '.py')
        if a.verifica:
            igual = os.path.exists(ruta) and open(ruta, 'rb').read() == b; ok &= igual
            print(f"  {n}: en disco == construido: {igual} (sha {h16b(b)})")
        else:
            os.makedirs(SALIDA, exist_ok=True)
            open(ruta, 'wb').write(b); print(f"  escrito {os.path.relpath(ruta, RAIZ)} sha {h16b(b)}")
    return 0 if ok else 1


if __name__ == '__main__':
    sys.exit(main())
