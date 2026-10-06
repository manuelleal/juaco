"""construye_o1_lib.py — construye POR ANCLAS el carro O1_LIB ("O1 libre con poderes") del bloque o1_libre (30-sep-2026).

MISION: llegar a la AGI por este camino (organismo minimo con reglas locales, sin retropropagacion, peldanos preregistrados con
controles y replicas). Encargo del director: "corramos nuestro monstruo que pasa el muro, demosle poderes, soltemoslo a ver que hace".

ORIGEN (solo se LEE; sha16 fijado; cada ancla EXACTAMENTE una vez o aborta):
  experimentos/carrera_escuderias/carros/O1.py (SHA_O1 = 99436afa2715f028). Fin de linea LF (el del origen).

GENOMA POR CUERPO = 14 genes continuos (toda la memoria nueva heredable: 14 floats; mas el estado de los poderes, abajo):
  10 de O1 = TODAS sus constantes de decision (las 5 del modulo y los 5 literales de _gana):
    MARGEN 0.25 · PRUEBA 0.5 · PEN_OTRO 0.35 · D0 3.0 · PISO 0.2 · U4 4.0 · U2 2.0 · U1 1.0 · XURG 0.3 · TOPE 0.5
    (u = U4 si la necesidad < XURG, U2 si < rep_umbral, U1 si no; ganancia = u * min(dS, rep_umbral + TOPE - x))
  4 PODERES que nacen APAGADOS (gen = 0; clip [0, 1]; la seleccion solo puede subirlos):
    MEM  memoria de LUGAR: sin nada que hacer (el O1 iria al hueco), va a la celda de su ultima mordida BUENA si fue hace
         <= MEM * H_MEM pasos (H_MEM 5000). La memoria es del LINAJE (como la tabla; el refundador nace sin ella).
    SOC  copia SOCIAL: la primera vez que una letra que el linaje NO conoce aparece publicada en la pizarra por un vecino que PARIO,
         la copia (media dE, dAg; cuenta como una mordida) con prob SOC; si no, la probara como O1. Publicar (al parir, la tabla de
         8 numeros; 9.0 = letra no probada) es una perilla de ESPECIE (PS_ESCRIBE, la fija el runner), no un gen: publicar no le da
         nada al que publica (seria altruismo que la seleccion no ve).
    RES  sentido de RESERVA: margen efectivo = MARGEN + RES * esc, esc = media movil (EMA_ESC 500 pasos) de la fraccion de objetos
         del mundo que NO son buenos segun la tabla del linaje (se llena mas cuando lo bueno escasea).
    PAU  PAUSA: sin nada que hacer, en vez de moverse se queda quieto con prob PAU por paso (en pista_libre quieto cuesta menos).
  - sigma del gen j = PS_SIGMA * max(1, |fabrica_j|) (0.03 para los genes chicos; 0.09 D0; 0.12 U4; 0.06 U2).
  - Fundador (crea(ctx): el primero y cada refundacion de la ENMIENDA 5): con PS_COLONIZA 1 (lo fija el runner en todas las corridas
    del bloque; junta o1_evo 30-sep, antes de datos) y si la corrida ya tiene partos de OTRO linaje, base = los genes del padre de uno
    de los ultimos PS_COL_N = 50 partos de otros linajes, al azar (COLONIZACION: el hueco lo llena la descendencia de los linajes que
    paren); si no, entrada de SIEMBRA al azar (la fija el RUNNER entre pasajes); si no, FABRICA (poderes 0). genes = base + N(0, sigma).
    La colonia vive en el MODULO (_COL): es un canal entre linajes de la misma corrida, declarado como regla de mundo; solo lleva genes
    al refundar (ninguna decision la lee).
  - Parto (al_parir): la memoria del hijo lleva '_gen' = genes del padre + N(0, sigma); la telemetria anota [t, genes del PADRE]
    (la MONEDA de la siembra: cada parto es una entrada; quien pare mas, pesa mas). Nace: toma '_gen'; lo demas como O1.
  - rng propias: mutacion y siembra [PS_SEMILLA, indice, instancia, 7721]; decisiones de poderes (copia, pausa)
    [PS_SEMILLA, indice, instancia, 7722]. No tocan el rng del mundo, del cuerpo ni del hijo.
  - PS_LEE 0: los genes se heredan, mutan, se anotan y se transfieren IGUAL, pero el cuerpo NO los lee (decide con FABRICA y
    poderes 0): cadena del brazo NEUTRO. Con PS_LEE 0 (y PS_ESCRIBE 0) el carro es O1 bit a bit con cualquier sigma.
  - Telemetria de SOLO ESCRITURA en _TEL[indice] ('vivos' cada 1000 pasos, 'fund', 'partos', 'activaciones' de cada poder). Nadie la lee
    dentro de la corrida; el runner la lee al terminar (ERR-96: no puntua). salida() NO cambia.
Genera en o1_libre/carros/ (difieren SOLO en la linea PASAJE y el nombre; se verifica):
  O1_LIB    PASAJE 1
  O1_LIB0   PASAJE 0 (solo arnes: == O1 bit a bit)

    python experimentos/organelos/o1_libre/construye_o1_lib.py [--verifica]
"""
import argparse, ast, hashlib, os, sys

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(AQUI)))
ORIGEN = os.path.join(RAIZ, 'experimentos', 'carrera_escuderias', 'carros', 'O1.py')
SALIDA = os.path.join(AQUI, 'carros')
SHA_O1 = '99436afa2715f028'
NL = '\n'
VARIANTES = [('O1_LIB', 1), ('O1_LIB0', 0)]
GENES_O1 = ('MARGEN', 'PRUEBA', 'PEN_OTRO', 'D0', 'PISO', 'U4', 'U2', 'U1', 'XURG', 'TOPE')
PODERES = ('MEM', 'SOC', 'RES', 'PAU')
GENES = GENES_O1 + PODERES
FABRICA = (0.25, 0.5, 0.35, 3.0, 0.2, 4.0, 2.0, 1.0, 0.3, 0.5, 0.0, 0.0, 0.0, 0.0)   # el arnes comprueba los 5 del modulo O1
CLIP = ((-0.5, 0.5), (0.0, 1.5), (0.0, 1.5), (0.5, 10.0), (0.0, 1.0), (0.0, 10.0), (0.0, 10.0), (0.0, 10.0), (0.0, 1.0), (0.0, 1.5),
        (0.0, 1.0), (0.0, 1.0), (0.0, 1.0), (0.0, 1.0))
ESCALA = tuple(max(1.0, abs(f)) for f in FABRICA)
GLOBALES_O1 = ('MARGEN', 'PRUEBA', 'PEN_OTRO', 'D0', 'PISO')   # las constantes de modulo de O1.py
PER = "PASAJE = {p}   # o1_libre: LA UNICA LINEA QUE CAMBIA ENTRE VARIANTES (0 = O1 bit a bit)"


def modulo(p): return (NL + PER.format(p=p) + NL
          + 'SIEMBRA = None; PS_SEMILLA = 0; PS_SIGMA = 0.03; PS_LEE = 1; PS_ESCRIBE = 0; PS_COLONIZA = 0   # o1_libre: los fija el RUNNER por corrida' + NL
          + '_PS_CNT = {}; _TEL = {}   # o1_libre: instancias por linaje y telemetria de SOLO ESCRITURA (el runner los borra antes de cada run)' + NL
          + 'from collections import deque as _deque; PS_COL_N = 50; _COL = _deque(maxlen=PS_COL_N)   # o1_libre: COLONIA (regla de MUNDO declarada: solo herencia al refundar; el runner la borra antes de cada run)' + NL
          + 'PS_GENES = ' + repr(GENES) + NL + 'PS_FABRICA = ' + repr(FABRICA) + NL + 'PS_CLIP = ' + repr(CLIP) + NL
          + 'PS_ESCALA = ' + repr(ESCALA) + NL
          + 'H_MEM = 5000; EMA_ESC = 500; SIN_DATO = 9.0   # o1_libre: horizonte de la memoria de lugar; ventana de la escasez; letra no probada' + NL)


METODOS = '''
    # ================================================================ o1_libre: 14 genes heredables por cuerpo (10 de O1 + 4 poderes)
    def _ps_init(self, ctx):
        i = int(ctx['indice']); c = _PS_CNT.get(i, 0); _PS_CNT[i] = c + 1; self._psi = i
        self._psrng = np.random.default_rng([int(PS_SEMILLA), i, c, 7721])
        self._pwrng = np.random.default_rng([int(PS_SEMILLA), i, c, 7722])
        base = None; self._psfund = 0   # origen del fundador: 0 FABRICA, 1 SIEMBRA, 2 COLONIA
        if PS_COLONIZA and _COL:   # junta o1_evo (30-sep): el refundador COLONIZA desde un parto reciente de OTRO linaje de la corrida
            otros = [g for (j, g) in _COL if j != i]
            if otros: base = dict(zip(PS_GENES, otros[int(self._psrng.integers(len(otros)))])); self._psfund = 2
        if base is None and SIEMBRA: base = SIEMBRA[int(self._psrng.integers(len(SIEMBRA)))]; self._psfund = 1
        b0 = [float(base[k]) for k in PS_GENES] if base is not None else list(PS_FABRICA)
        self._esc = 0.0; self._lugar = None; self._t_lugar = -10 ** 9; self._escribe = False; self._soc_visto = set()
        self._act = _TEL.setdefault(i, {}).setdefault('activaciones', dict(mem=0, pau=0, soc=0, res=0, escr=0))
        self._ps_pon(self._ps_muta(b0))
        _TEL[i].setdefault('fund', []).append([self._psfund, list(self._gen)])

    def _ps_muta(self, b):
        z = self._psrng.normal(0.0, 1.0, len(PS_GENES))
        return [float(min(max(b[j] + PS_SIGMA * PS_ESCALA[j] * float(z[j]), PS_CLIP[j][0]), PS_CLIP[j][1])) for j in range(len(PS_GENES))]

    def _ps_pon(self, g):
        self._gen = [float(x) for x in g]
        if PS_LEE:   # PS_LEE 0: se heredan y mutan pero NO se leen (fabrica, poderes 0)
            (self.MARGEN, self.PRUEBA, self.PEN_OTRO, self.D0, self.PISO, self.U4, self.U2, self.U1, self.XURG, self.TOPE,
             self.MEM, self.SOC, self.RES, self.PAU) = self._gen
            self._mg = self.MARGEN

    def _ps_bueno(self, k):
        v = self._val(k)
        return v is not None and not (v < 0).any() and (v > 0).any()

    def _ps_ini_paso(self, obs):
        objs = obs['objs']
        if objs:   # escasez (del linaje): fraccion de objetos que NO son buenos segun su tabla; media movil
            bu = {k for k in 'ABCD' if self._ps_bueno(k)}
            x = 1.0 - sum(1 for k in objs.values() if k in bu) / len(objs)
            self._esc += (x - self._esc) / EMA_ESC
        if self.RES:
            self._mg = self.MARGEN + self.RES * self._esc
            if self.RES * self._esc > 0.01: self._act['res'] += 1
        else:
            self._mg = self.MARGEN
        if self.SOC and len(self.n) < 4 and obs['pizarra']: self._ps_copia(obs['pizarra'])

    def _ps_copia(self, piz):
        for j, k in enumerate('ABCD'):
            if k in self.n or k in self._soc_visto: continue
            src = None
            for e in reversed(piz):
                c = e[2]
                if len(c) == 8 and c[2 * j] != SIN_DATO: src = (c[2 * j], c[2 * j + 1]); break
            if src is None: continue
            self._soc_visto.add(k)
            if self._pwrng.random() < self.SOC:
                self.suma[k] = np.array(src, float); self.n[k] = 1; self._act['soc'] += 1

    def _ps_ocio(self, t, tgt):
        if self.MEM and self._lugar is not None and t - self._t_lugar <= self.MEM * H_MEM:
            self._act['mem'] += 1; return self._lugar
        return tgt

    def _ps_pausa(self, mov, ocioso):
        if ocioso and self.PAU and mov != 0 and self._pwrng.random() < self.PAU:
            self._act['pau'] += 1; return 0
        return mov

    def _ps_comio(self, res, dS):
        if not (dS < 0).any() and (dS > 0).any(): self._lugar = int(res['pos']); self._t_lugar = int(res['t'])

    def _ps_escribe(self):
        if not self._escribe: return None
        self._escribe = False; self._act['escr'] += 1; out = []
        for k in 'ABCD':
            v = self._val(k)
            out += [SIN_DATO, SIN_DATO] if v is None else [round(float(v[0]), 4), round(float(v[1]), 4)]
        return tuple(out)

    def _ps_parto(self, info):
        _TEL.setdefault(self._psi, {}).setdefault('partos', []).append([int(info['t']), list(self._gen)])
        _COL.append((self._psi, list(self._gen)))   # colonia: los ultimos PS_COL_N partos de la corrida (genes del padre)
        if PS_ESCRIBE: self._escribe = True
        return self._ps_muta(self._gen)

    def _ps_tel(self, t):
        _TEL.setdefault(self._psi, {}).setdefault('vivos', []).append([int(t), list(self._gen)])
'''


def anclas(nombre, p):
    return [
        ('"""carros/O1.py — escuderia O1 (Opus). Carrera de escuderias, ronda 1.' + NL,
         f'"""{nombre}.py — o1_libre: O1 con TODAS sus constantes como genes heredables y 4 PODERES apagados (MEM, SOC, RES, PAU).' + NL
         + f'GENERADO por experimentos/organelos/o1_libre/construye_o1_lib.py desde carrera_escuderias/carros/O1.py (sha {SHA_O1}).' + NL
         + f'NO editar a mano. PASAJE = {p}. Con PASAJE = 0 es O1 bit a bit; con PASAJE = 1, PS_SIGMA = 0, genes de fabrica y PS_ESCRIBE 0, tambien.' + NL + NL
         + 'carros/O1.py — escuderia O1 (Opus). Carrera de escuderias, ronda 1.' + NL),
        ('PISO = 0.2         # v2: la limpieza no baja la necesidad golpeada de aqui (si la ventana de parto no corre)' + NL,
         'PISO = 0.2         # v2: la limpieza no baja la necesidad golpeada de aqui (si la ventana de parto no corre)' + NL + modulo(p)),
        ('        self.st = dict(mord={}, pruebas=0, sin_blanco=0, pasos=0, cuerpos=0, partos=0, limpias=0)' + NL,
         '        self.st = dict(mord={}, pruebas=0, sin_blanco=0, pasos=0, cuerpos=0, partos=0, limpias=0)' + NL
         + '        self.MARGEN, self.PRUEBA, self.PEN_OTRO, self.D0, self.PISO = MARGEN, PRUEBA, PEN_OTRO, D0, PISO; self._mg = MARGEN   # o1_libre' + NL
         + '        self.U4, self.U2, self.U1, self.XURG, self.TOPE = 4.0, 2.0, 1.0, 0.3, 0.5   # o1_libre: los literales de _gana' + NL
         + '        self.MEM = self.SOC = self.RES = self.PAU = 0.0   # o1_libre: poderes APAGADOS' + NL
         + '        if PASAJE: self._ps_init(ctx)   # o1_libre: genes del fundador (de SIEMBRA o de FABRICA), mutados' + NL),
        ('            if x >= self.U + MARGEN: continue' + NL, '            if x >= self.U + self._mg: continue' + NL),
        ('            u = 4.0 if x < 0.3 else (2.0 if x < self.U else 1.0)' + NL,
         '            u = self.U4 if x < self.XURG else (self.U2 if x < self.U else self.U1)' + NL),
        ('            g += u * min(v[j], self.U + 0.5 - x)' + NL, '            g += u * min(v[j], self.U + self.TOPE - x)' + NL),
        ('        if v is None: return min(lev) > PRUEBA' + NL, '        if v is None: return min(lev) > self.PRUEBA' + NL),
        ('                piso = self.U if min(lev) >= self.U else PISO' + NL, '                piso = self.U if min(lev) >= self.U else self.PISO' + NL),
        ("        pos = obs['pos']; lev = (float(obs['E']), float(obs['Ag'])); objs = obs['objs']" + NL,
         "        pos = obs['pos']; lev = (float(obs['E']), float(obs['Ag'])); objs = obs['objs']" + NL
         + '        if PASAJE: self._ps_ini_paso(obs)   # o1_libre: escasez, margen efectivo (RES) y copia (SOC)' + NL),
        ('                if min(lev) > PRUEBA and (desc is None or d < desc[0]): desc = (d, x)' + NL,
         '                if min(lev) > self.PRUEBA and (desc is None or d < desc[0]): desc = (d, x)' + NL),
        ('            s = g / (d + D0)' + NL, '            s = g / (d + self.D0)' + NL),
        ('            if otros and min(self._dist(o, x) for o in otros) < d: s *= PEN_OTRO' + NL,
         '            if otros and min(self._dist(o, x) for o in otros) < d: s *= self.PEN_OTRO' + NL),
        ('        limpia = mejor is None and min(lev) < self.U + MARGEN' + NL,
         '        limpia = mejor is None and min(lev) < self.U + self._mg' + NL),
        ("            tgt = self._hueco(pos, otros); self.st['sin_blanco'] += 1" + NL,
         "            tgt = self._hueco(pos, otros); self.st['sin_blanco'] += 1" + NL
         + "            if PASAJE: tgt = self._ps_ocio(obs['t'], tgt)   # o1_libre: MEM" + NL),
        ('        mov = self._dir(pos, tgt)' + NL,
         '        mov = self._dir(pos, tgt)' + NL
         + '        if PASAJE: mov = self._ps_pausa(mov, mejor is None and desc is None and sucio is None)   # o1_libre: PAU' + NL),
        ('        return dict(mov=mov, muerde=muerde, escribe=None)' + NL,
         '        return dict(mov=mov, muerde=muerde, escribe=(self._ps_escribe() if PASAJE else None))   # o1_libre: publica tras parir' + NL),
        ("        self.st['mord'][k] = self.st['mord'].get(k, 0) + 1" + NL,
         "        self.st['mord'][k] = self.st['mord'].get(k, 0) + 1" + NL
         + '        if PASAJE: self._ps_comio(res, dS)   # o1_libre: lugar de la ultima mordida buena' + NL),
        ('    def fin_paso(self, info):' + NL + '        return None' + NL,
         '    def fin_paso(self, info):' + NL
         + "        if PASAJE and info['t'] % 1000 == 0: self._ps_tel(info['t'])   # o1_libre: genes del vivo (solo escritura)" + NL
         + '        return None' + NL),
        ('        return {k: (self.suma[k].copy(), self.n[k]) for k in self.n}' + NL,
         '        _m = {k: (self.suma[k].copy(), self.n[k]) for k in self.n}' + NL
         + "        if PASAJE: _m['_gen'] = self._ps_parto(info)   # o1_libre: genes del hijo; el parto se anota (moneda de la siembra)" + NL
         + '        return _m' + NL),
        ("        m = info.get('memoria')" + NL + '        if m:' + NL,
         "        m = info.get('memoria')" + NL
         + "        if PASAJE and m and '_gen' in m: m = dict(m); self._ps_pon(m.pop('_gen'))   # o1_libre: el hijo toma sus genes" + NL
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
    arbol = ast.parse(txt)
    for f in ast.walk(arbol):
        if isinstance(f, ast.FunctionDef):
            # las 5 constantes de modulo ya no se leen como GLOBALES en ningun metodo, salvo la linea de __init__ que las copia
            usos = [nd.lineno for nd in ast.walk(f) if isinstance(nd, ast.Name) and nd.id in GLOBALES_O1 and isinstance(nd.ctx, ast.Load)]
            if usos and not (f.name == '__init__' and len(usos) == 6 and len(set(usos)) == 1):
                raise SystemExit(f"{f.name}: quedan usos de {GLOBALES_O1} como globales en las lineas {usos}")
            # los 5 literales de _gana ya no estan en _gana (solo 0, 0.0 y 1 de la estructura)
            if f.name == '_gana':
                lit = sorted({nd.value for nd in ast.walk(f) if isinstance(nd, ast.Constant) and isinstance(nd.value, (int, float))})
                if any(x not in (0, 1) for x in lit): raise SystemExit(f"_gana: quedan literales {lit}")
    return txt.encode('utf-8')


def todas():
    return {n: construye(n, p) for n, p in VARIANTES}


def main(argv=None):
    ap = argparse.ArgumentParser(allow_abbrev=False)
    ap.add_argument('--verifica', action='store_true')
    a = ap.parse_args(argv)
    T = todas()
    l1 = T['O1_LIB'].decode().split(NL); l0 = T['O1_LIB0'].decode().split(NL)
    dif = [i for i, (x, y) in enumerate(zip(l1, l0)) if x != y]
    if len(l1) != len(l0) or len(dif) != 3: raise SystemExit(f"las variantes difieren en {dif} (se esperan 3 lineas: nombre, PASAJE del encabezado y la perilla)")
    ok = True
    for n, b in T.items():
        ruta = os.path.join(SALIDA, n + '.py')
        if a.verifica:
            igual = os.path.exists(ruta) and open(ruta, 'rb').read() == b; ok &= igual
            print(f"  {n}: en disco == construido: {igual} (sha {h16b(b)})")
        else:
            os.makedirs(SALIDA, exist_ok=True)
            open(ruta, 'wb').write(b); print(f"  escrito {os.path.relpath(ruta, RAIZ)} sha {h16b(b)}")
    print(f"  diferencias entre variantes (lineas): {dif}")
    return 0 if ok else 1


if __name__ == '__main__':
    sys.exit(main())
