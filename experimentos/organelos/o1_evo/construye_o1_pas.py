"""construye_o1_pas.py — construye POR ANCLAS el carro O1_PAS (O1 con perillas HEREDABLES) del bloque o1_evo (30-sep-2026).

MISION: llegar a la AGI por este camino (organismo minimo con reglas locales, sin retropropagacion, peldanos preregistrados con
controles y replicas). Pregunta: ¿la seleccion por pasajes hace a O1 MEJOR que su disenador?

ORIGEN (solo se LEE; sha16 fijado; cada ancla EXACTAMENTE una vez o aborta):
  experimentos/carrera_escuderias/carros/O1.py (SHA_O1 = 99436afa2715f028). Fin de linea LF (el del origen).

PIEZA NUEVA (perilla PASAJE; con PASAJE = 0 el carro es O1 bit a bit, salida ENTERA; con PASAJE = 1, PS_SIGMA = 0 y SIEMBRA None o
de genes de fabrica, tambien es O1 bit a bit: arnes identidad_o1_evo.py):
  GENOMA POR CUERPO = 4 genes continuos, las cuatro constantes de O1 que deciden CUANDO COMER Y CUANDO LIMPIAR (el muro):
    MARGEN   0.25  muerde lo bueno si la necesidad que sube esta bajo rep_umbral + MARGEN (y dispara la limpieza)   clip [-0.50, 0.50]
    PRUEBA   0.50  prueba una letra desconocida solo si E y Ag > PRUEBA                                           clip [ 0.00, 1.50]
    PEN_OTRO 0.35  factor al blanco si otro cuerpo esta mas cerca                                                 clip [ 0.00, 1.50]
    PISO     0.20  la limpieza no baja la necesidad golpeada de aqui (fuera de la ventana de parto)               clip [ 0.00, 1.00]
  (D0 queda FIJO: es el suavizado de la distancia en el puntaje, no una decision comer/limpiar.)
  - Fundador (crea(ctx): el primero y cada refundacion de la ENMIENDA 5): base = una entrada de SIEMBRA al azar (uniforme) si SIEMBRA
    (lista de genomas {gen: valor}, la fija el RUNNER entre pasajes) no es None; si es None, base = FABRICA. Genes = base + N(0, PS_SIGMA)
    por gen, recortado al clip.
  - Parto (al_parir): la memoria del hijo lleva '_gen' = genes del padre + N(0, PS_SIGMA), recortado. Nace (nace): toma su '_gen' y el
    resto de la memoria como O1 (la tabla por letra del LINAJE no cambia).
  - rng de la pieza: np.random.default_rng([PS_SEMILLA, indice, instancia, 7702]) (PS_SEMILLA la fija el runner; _PS_CNT cuenta las
    instancias por linaje y el runner lo borra antes de cada run). No toca el rng del mundo, ni el del cuerpo, ni rng_hijo.
  - Telemetria de SOLO ESCRITURA en _TEL[indice]: 'vivos' = [t, genes] del cuerpo vivo cada 1000 pasos; 'fund' = [de_siembra, genes]
    por fundador; 'partos' = numero de partos (conteo). Ningun carro la lee; el runner la lee al terminar el run (ERR-96: no puntua).
  - PS_LEE (la fija el runner; 1 por defecto): con 0 los genes se heredan, mutan, se muestrean y se transfieren IGUAL, pero el cuerpo NO los
    lee (decide con las constantes de fabrica): es el brazo NEUTRO o1neu en su cadena (deriva acumulada sin seleccion sobre los genes).
    Con PS_LEE 0 el carro es O1 bit a bit con cualquier sigma (arnes).
  Memoria nueva: 4 floats por cuerpo. salida() NO cambia (la salida ENTERA es la de O1).
Genera en o1_evo/carros/ (difieren SOLO en la linea PASAJE y el nombre; se verifica):
  O1_PAS    PASAJE 1
  O1_PAS0   PASAJE 0 (solo arnes: == O1 bit a bit)

    python experimentos/organelos/o1_evo/construye_o1_pas.py [--verifica]
"""
import argparse, ast, hashlib, os, sys

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(AQUI)))
ORIGEN = os.path.join(RAIZ, 'experimentos', 'carrera_escuderias', 'carros', 'O1.py')
SALIDA = os.path.join(AQUI, 'carros')
SHA_O1 = '99436afa2715f028'
NL = '\n'
VARIANTES = [('O1_PAS', 1), ('O1_PAS0', 0)]
GENES = ('MARGEN', 'PRUEBA', 'PEN_OTRO', 'PISO')
FABRICA = (0.25, 0.5, 0.35, 0.2)          # los literales de O1.py (el arnes comprueba que coinciden con el modulo O1)
CLIP = ((-0.5, 0.5), (0.0, 1.5), (0.0, 1.5), (0.0, 1.0))
PER = "PASAJE = {p}   # o1_evo: LA UNICA LINEA QUE CAMBIA ENTRE VARIANTES (0 = O1 bit a bit)"

def modulo(p): return (NL + PER.format(p=p) + NL
          + 'SIEMBRA = None; PS_SEMILLA = 0; PS_SIGMA = 0.03; PS_LEE = 1   # o1_evo: los fija el RUNNER por corrida (SIEMBRA None = FABRICA; PS_LEE 0 = genes NEUTROS)' + NL
          + '_PS_CNT = {}; _TEL = {}   # o1_evo: instancias por linaje y telemetria de SOLO ESCRITURA (el runner los borra antes de cada run)' + NL
          + 'PS_GENES = ' + repr(GENES) + NL + 'PS_FABRICA = ' + repr(FABRICA) + NL + 'PS_CLIP = ' + repr(CLIP) + NL)

METODOS = '''
    # ================================================================ o1_evo: 4 perillas de O1 como GENES heredables por cuerpo
    def _ps_init(self, ctx):
        i = int(ctx['indice']); c = _PS_CNT.get(i, 0); _PS_CNT[i] = c + 1; self._psi = i
        self._psrng = np.random.default_rng([int(PS_SEMILLA), i, c, 7702])
        base = SIEMBRA[int(self._psrng.integers(len(SIEMBRA)))] if SIEMBRA else None
        b0 = [float(base[k]) for k in PS_GENES] if base is not None else list(PS_FABRICA)
        self._psfund = int(base is not None)
        self._ps_pon(self._ps_muta(b0))
        _TEL.setdefault(i, {}).setdefault('fund', []).append([self._psfund, list(self._gen)])

    def _ps_muta(self, b):
        z = self._psrng.normal(0.0, 1.0, len(PS_GENES))
        return [float(min(max(b[j] + PS_SIGMA * float(z[j]), PS_CLIP[j][0]), PS_CLIP[j][1])) for j in range(len(PS_GENES))]

    def _ps_pon(self, g):
        self._gen = [float(x) for x in g]
        if PS_LEE: self.MARGEN, self.PRUEBA, self.PEN_OTRO, self.PISO = self._gen   # PS_LEE 0: se heredan y mutan pero NO se leen (fabrica)

    def _ps_tel(self, t):
        _TEL.setdefault(self._psi, {}).setdefault('vivos', []).append([int(t), list(self._gen)])
'''


def anclas(nombre, p):
    return [
        ('"""carros/O1.py — escuderia O1 (Opus). Carrera de escuderias, ronda 1.' + NL,
         f'"""{nombre}.py — o1_evo: O1 con 4 perillas HEREDABLES (MARGEN, PRUEBA, PEN_OTRO, PISO) y fundador de SIEMBRA.' + NL
         + f'GENERADO por experimentos/organelos/o1_evo/construye_o1_pas.py desde carrera_escuderias/carros/O1.py (sha {SHA_O1}).' + NL
         + f'NO editar a mano. PASAJE = {p}. Con PASAJE = 0 es O1 bit a bit; con PASAJE = 1, PS_SIGMA = 0 y genes de fabrica, tambien.' + NL + NL
         + 'carros/O1.py — escuderia O1 (Opus). Carrera de escuderias, ronda 1.' + NL),
        ('PISO = 0.2         # v2: la limpieza no baja la necesidad golpeada de aqui (si la ventana de parto no corre)' + NL,
         'PISO = 0.2         # v2: la limpieza no baja la necesidad golpeada de aqui (si la ventana de parto no corre)' + NL + modulo(p)),
        ('        self.st = dict(mord={}, pruebas=0, sin_blanco=0, pasos=0, cuerpos=0, partos=0, limpias=0)' + NL,
         '        self.st = dict(mord={}, pruebas=0, sin_blanco=0, pasos=0, cuerpos=0, partos=0, limpias=0)' + NL
         + '        self.MARGEN, self.PRUEBA, self.PEN_OTRO, self.PISO = MARGEN, PRUEBA, PEN_OTRO, PISO   # o1_evo: perillas por cuerpo' + NL
         + '        if PASAJE: self._ps_init(ctx)   # o1_evo: genes del fundador (de SIEMBRA o de FABRICA), mutados' + NL),
        ('            if x >= self.U + MARGEN: continue' + NL, '            if x >= self.U + self.MARGEN: continue' + NL),
        ('        if v is None: return min(lev) > PRUEBA' + NL, '        if v is None: return min(lev) > self.PRUEBA' + NL),
        ('                piso = self.U if min(lev) >= self.U else PISO' + NL, '                piso = self.U if min(lev) >= self.U else self.PISO' + NL),
        ('                if min(lev) > PRUEBA and (desc is None or d < desc[0]): desc = (d, x)' + NL,
         '                if min(lev) > self.PRUEBA and (desc is None or d < desc[0]): desc = (d, x)' + NL),
        ('            if otros and min(self._dist(o, x) for o in otros) < d: s *= PEN_OTRO' + NL,
         '            if otros and min(self._dist(o, x) for o in otros) < d: s *= self.PEN_OTRO' + NL),
        ('        limpia = mejor is None and min(lev) < self.U + MARGEN' + NL,
         '        limpia = mejor is None and min(lev) < self.U + self.MARGEN' + NL),
        ('    def fin_paso(self, info):' + NL + '        return None' + NL,
         '    def fin_paso(self, info):' + NL
         + "        if PASAJE and info['t'] % 1000 == 0: self._ps_tel(info['t'])   # o1_evo: genes del vivo (solo escritura)" + NL
         + '        return None' + NL),
        ('        return {k: (self.suma[k].copy(), self.n[k]) for k in self.n}' + NL,
         '        _m = {k: (self.suma[k].copy(), self.n[k]) for k in self.n}' + NL
         + "        if PASAJE: _m['_gen'] = self._ps_muta(self._gen); _TEL.setdefault(self._psi, {})['partos'] = _TEL[self._psi].get('partos', 0) + 1" + NL
         + '        return _m' + NL),
        ("        m = info.get('memoria')" + NL + '        if m:' + NL,
         "        m = info.get('memoria')" + NL
         + "        if PASAJE and m and '_gen' in m: m = dict(m); self._ps_pon(m.pop('_gen'))   # o1_evo: el hijo toma sus genes" + NL
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
    arbol = ast.parse(txt)
    for f in ast.walk(arbol):
        if isinstance(f, ast.FunctionDef):
            usos = [nd.lineno for nd in ast.walk(f) if isinstance(nd, ast.Name) and nd.id in GENES and isinstance(nd.ctx, ast.Load)]
            if usos and not (f.name == '__init__' and len(usos) == 4 and len(set(usos)) == 1):
                raise SystemExit(f"{f.name}: quedan usos de {GENES} como globales en las lineas {usos}")
    return txt.encode('utf-8')


def todas():
    return {n: construye(n, p) for n, p in VARIANTES}


def main(argv=None):
    ap = argparse.ArgumentParser(allow_abbrev=False)
    ap.add_argument('--verifica', action='store_true')
    a = ap.parse_args(argv)
    T = todas()
    # difieren SOLO en la linea PASAJE y el nombre
    l1 = T['O1_PAS'].decode().split(NL); l0 = T['O1_PAS0'].decode().split(NL)
    dif = [i for i, (x, y) in enumerate(zip(l1, l0)) if x != y]
    if len(l1) != len(l0) or dif != [0, 2, 34]: raise SystemExit(f"las variantes difieren en {dif} (se esperan 3 lineas: nombre, PASAJE del encabezado y la perilla)")
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
