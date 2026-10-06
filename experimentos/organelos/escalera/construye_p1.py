"""construye_p1.py — construye POR ANCLAS el carro O1_LUGAR (O1 + MEMORIA DE LUGAR del linaje), peldano 1 de la escalera (30-sep-2026).

MISION: llegar a la AGI por este camino (organismo minimo con reglas locales, sin retropropagacion, peldanos preregistrados con
controles y replicas). Escalera: ESCALERA.md. Mundo: mundo_escalera.py (oasis). Arnes: identidad_p1.py. Runner: corre_p1.py.

ORIGEN (solo se LEE; sha16 fijado; cada ancla EXACTAMENTE una vez o aborta):
  experimentos/carrera_escuderias/carros/O1.py (SHA_O1 = 99436afa2715f028). Fin de linea LF (el del origen).

PIEZA NUEVA (promotor LUGAR; con LUGAR = 0 el carro es O1 bit a bit, salida ENTERA; con LUGAR = 1 y LUGAR_W = 0.0 tambien; y con
LUGAR = 1 en un mundo SIN oasis tambien, porque ningun sitio da nunca mas que su letra y el bono queda en 0 exacto: arnes identidad_p1.py):
  MEMORIA DE LUGAR del linaje = LG_NB bins del anillo (30 bins de L/30 celdas) x 2 necesidades: lo que ESE sitio dio DE MAS (o de menos)
  que lo que su letra da en promedio. Regla LOCAL de aprendizaje, en resultado(), ANTES de actualizar la tabla por letra:
      lugar[bin(pos)] += LG_ETA * ((dS - valor_medio(letra)) - lugar[bin(pos)])        (EMA; la primera mordida de una letra no ensena)
  Uso (actua y _quiere): el valor esperado de un objeto en x es  valor(letra) + LUGAR_W * bono(x),  con bono = la parte de la memoria
  del bin que supera LG_MIN (0.05), solo en necesidades donde ya vale > 0 y solo si la letra no dania. El resto de O1 (urgencia, distancia,
  PEN_OTRO, limpieza, pruebas) NO cambia: el sitio solo cambia cuanto vale el bocado. Ni el hambre ni la limpieza leen la memoria de lugar.
  CONTROL DE CONTENIDO (LUGAR_BARAJA = 1): la memoria se ESCRIBE en el bin verdadero pero se LEE (valor y viaje) en el bin ANTIPODA
  FIJO (b + 15 mod 30): el mismo sesgo, SIEMPRE el lugar equivocado (el oasis son 4 bins contiguos de 30: el antipoda nunca lo toca).
  ERR-170: hasta la exploracion 739201-739202 el control leia un bin PERMUTADO al azar por instancia (rng del cuerpo); con 4 bins de oasis
  en 30, ~45 % de las instancias leian bien algun bin del oasis (por eso bar dio razon de pasos 3.5). Cambiado ANTES de datos de serie.
  Ya no se consume ningun rng: BAR es determinista como O1.
  Herencia: la memoria es del LINAJE, como la tabla por letra de O1 (viaja en al_parir/nace; el fundador limpio nace vacio).
  Memoria nueva: 30 x 2 floats + 30 conteos. salida() con LUGAR = 0 NO cambia; con LUGAR = 1 agrega d['lugar'] (telemetria; el juez no la lee).
  DISENO, no evolucion: el modulo y su promotor los pone el ingeniero; la seleccion podra afinar LUGAR_W despues (gen, como o1_evo).
Genera en escalera/carros/ (difieren SOLO en las lineas LUGAR / LUGAR_BARAJA y el nombre; se verifica):
  O1_LUGAR      LUGAR 1, LUGAR_BARAJA 0   (el candidato)
  O1_LUGAR_BAR  LUGAR 1, LUGAR_BARAJA 1   (control de contenido)
  O1_LUGAR0     LUGAR 0, LUGAR_BARAJA 0   (solo arnes: == O1 bit a bit)

    python experimentos/organelos/escalera/construye_p1.py [--verifica]
"""
import argparse, hashlib, os, sys

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(AQUI)))
ORIGEN = os.path.join(RAIZ, 'experimentos', 'carrera_escuderias', 'carros', 'O1.py')
SALIDA = os.path.join(AQUI, 'carros')
SHA_O1 = '99436afa2715f028'
NL = '\n'
VARIANTES = [('O1_LUGAR', 1, 0), ('O1_LUGAR_BAR', 1, 1), ('O1_LUGAR0', 0, 0)]
LG_NB = 30; LG_ETA = 0.5; LG_MIN = 0.05; LUGAR_W = 1.0; LG_VIAJA = 1


def modulo(p, b):
    return (NL + f'LUGAR = {p}   # escalera p1: promotor. LA LINEA QUE CAMBIA ENTRE VARIANTES (0 = O1 bit a bit)' + NL
            + f'LUGAR_BARAJA = {b}   # escalera p1: 1 = control de contenido (escribe en el bin verdadero, LEE en un bin permutado)' + NL
            + f'LUGAR_W = {LUGAR_W!r}; LG_NB = {LG_NB}; LG_ETA = {LG_ETA!r}; LG_MIN = {LG_MIN!r}   # escalera p1: peso del bono (0.0 = O1 bit a bit), bins, EMA, umbral' + NL
            + f'LG_VIAJA = {LG_VIAJA}   # escalera p1b (humo 2): 1 = sin blanco a la vista, VIAJA al sitio recordado en vez de al hueco (0 = humo 1)' + NL)


METODOS = '''
    # ================================================================ escalera p1: MEMORIA DE LUGAR del linaje (regla local)
    def _lg_init(self, ctx):
        self.lugar = np.zeros((LG_NB, 2)); self.nl = np.zeros(LG_NB, int); self._lgx = None
        self.st['lg_bono'] = 0; self.st['lg_apr'] = 0; self.st['lg_viajes'] = 0

    def _lg_bin(self, x):
        return (int(x) * LG_NB) // self.L

    def _lg_rb(self, b):
        """bin que se LEE: el verdadero, o (control, ERR-170) el ANTIPODA fijo b + LG_NB//2: nunca toca el oasis (4 bins contiguos de 30)."""
        return (b + LG_NB // 2) % LG_NB if LUGAR_BARAJA else b

    def _lg_leer(self, x):
        return self.lugar[self._lg_rb(self._lg_bin(x))]

    def _lg_v(self, v, x):
        """valor de la letra + lo que el sitio recuerda DE MAS (solo bonos > LG_MIN, solo en necesidades que ya valen > 0, solo si no dania)."""
        if (v < 0).any(): return v
        m = self._lg_leer(x)
        bono = np.where((m > LG_MIN) & (v > 0), m, 0.0)
        if not (bono > 0).any(): return v
        return v + LUGAR_W * bono

    def _lg_apr(self, x, k, dS):
        v = self._val(k)
        if v is None: return
        b = self._lg_bin(x)
        self.lugar[b] += LG_ETA * ((dS - v) - self.lugar[b]); self.nl[b] += 1; self.st['lg_apr'] += 1

    def _lg_cuenta(self, x):
        if (self._lg_leer(x) > LG_MIN).any(): self.st['lg_bono'] += 1

    def _lg_meta(self, pos):
        """P1b: sin blanco a la vista: el centro del bin recordado con mas bono por distancia (None si ningun sitio recuerda nada)."""
        s = self.lugar.sum(1) if not LUGAR_BARAJA else np.array([self.lugar[self._lg_rb(b)].sum() for b in range(LG_NB)])
        best = None
        for b in range(LG_NB):
            if s[b] <= LG_MIN: continue
            c = ((2 * b + 1) * self.L) // (2 * LG_NB); v = s[b] / (self._dist(pos, c) + D0)
            if best is None or v > best[0]: best = (v, c)
        if best is None: return None
        self.st['lg_viajes'] += 1
        return best[1]

    def _lg_hereda(self, m):
        if self.nl.sum() == 0: self.lugar = np.asarray(m[0], float).copy(); self.nl = np.asarray(m[1], int).copy()

    def _lg_salida(self):
        s = self.lugar.sum(1)
        return dict(lugar=dict(W=LUGAR_W, nb=LG_NB, baraja=int(LUGAR_BARAJA), n=[int(z) for z in self.nl],
                               mem=[[round(float(z), 3) for z in fila] for fila in self.lugar],
                               bin_max=int(np.argmax(s)), max=round(float(s.max()), 3),
                               bins_con_bono=[int(i) for i in range(LG_NB) if (self.lugar[i] > LG_MIN).any()]))
'''


def anclas(nombre, p, b):
    return [
        ('"""carros/O1.py — escuderia O1 (Opus). Carrera de escuderias, ronda 1.' + NL,
         f'"""{nombre}.py — escalera p1: O1 + MEMORIA DE LUGAR del linaje (bins del anillo x lo que el sitio dio de mas que su letra).' + NL
         + f'GENERADO por experimentos/organelos/escalera/construye_p1.py desde carrera_escuderias/carros/O1.py (sha {SHA_O1}).' + NL
         + f'NO editar a mano. LUGAR = {p}, LUGAR_BARAJA = {b}. Con LUGAR = 0 es O1 bit a bit; con LUGAR_W = 0.0 o sin oasis, tambien.' + NL + NL
         + 'carros/O1.py — escuderia O1 (Opus). Carrera de escuderias, ronda 1.' + NL),
        ('PISO = 0.2         # v2: la limpieza no baja la necesidad golpeada de aqui (si la ventana de parto no corre)' + NL,
         'PISO = 0.2         # v2: la limpieza no baja la necesidad golpeada de aqui (si la ventana de parto no corre)' + NL + modulo(p, b)),
        ('        self.st = dict(mord={}, pruebas=0, sin_blanco=0, pasos=0, cuerpos=0, partos=0, limpias=0)' + NL,
         '        self.st = dict(mord={}, pruebas=0, sin_blanco=0, pasos=0, cuerpos=0, partos=0, limpias=0)' + NL
         + '        if LUGAR: self._lg_init(ctx)   # escalera p1: memoria de lugar del linaje' + NL),
        ('        if v is None: return min(lev) > PRUEBA' + NL + '        g = self._gana(v, lev)' + NL,
         '        if v is None: return min(lev) > PRUEBA' + NL
         + '        if LUGAR: v = self._lg_v(v, self._lgx)   # escalera p1: el bocado vale lo de su letra + lo que el sitio recuerda' + NL
         + '        g = self._gana(v, lev)' + NL),
        ('            g = self._gana(v, lev)' + NL + '            if not g: continue' + NL,
         '            g = self._gana(self._lg_v(v, x) if LUGAR else v, lev)   # escalera p1' + NL + '            if not g: continue' + NL),
        ('        if mejor is not None: tgt = mejor[1]' + NL,
         '        if mejor is not None:' + NL + '            tgt = mejor[1]' + NL
         + '            if LUGAR: self._lg_cuenta(tgt)   # escalera p1: telemetria (blancos con bono de lugar)' + NL),
        ("            tgt = self._hueco(pos, otros); self.st['sin_blanco'] += 1" + NL,
         '            tgt = self._lg_meta(pos) if (LUGAR and LG_VIAJA) else None   # escalera p1b: sin blanco a la vista, al sitio recordado' + NL
         + "            if tgt is None: tgt = self._hueco(pos, otros); self.st['sin_blanco'] += 1" + NL),
        ('            muerde = bool(self._quiere(objs[p2], lev, limpia))' + NL,
         '            if LUGAR: self._lgx = p2   # escalera p1: donde esta lo que se va a morder' + NL
         + '            muerde = bool(self._quiere(objs[p2], lev, limpia))' + NL),
        ("        k = res['letra']; dS = np.asarray(res['dS'], float)" + NL,
         "        k = res['letra']; dS = np.asarray(res['dS'], float)" + NL
         + "        if LUGAR: self._lg_apr(res['pos'], k, dS)   # escalera p1: ANTES de actualizar la tabla por letra" + NL),
        ('        return {k: (self.suma[k].copy(), self.n[k]) for k in self.n}' + NL,
         '        _m = {k: (self.suma[k].copy(), self.n[k]) for k in self.n}' + NL
         + "        if LUGAR: _m['_lugar'] = (self.lugar.copy(), self.nl.copy())   # escalera p1: la memoria de lugar es del linaje" + NL
         + '        return _m' + NL),
        ("        m = info.get('memoria')" + NL + '        if m:' + NL,
         "        m = info.get('memoria')" + NL
         + "        if LUGAR and m and '_lugar' in m: m = dict(m); self._lg_hereda(m.pop('_lugar'))   # escalera p1" + NL
         + '        if m:' + NL),
        ('    def salida(self):' + NL + '        return dict(tabla=',
         '    def salida(self):' + NL
         + '        if LUGAR: return dict(self._salida_o1(), **self._lg_salida())   # escalera p1: la salida de O1 + la memoria de lugar' + NL
         + '        return self._salida_o1()' + NL + NL
         + '    def _salida_o1(self):' + NL + '        return dict(tabla='),
        (NL + NL + 'def crea(ctx):' + NL, METODOS.replace('\n', NL) + NL + NL + 'def crea(ctx):' + NL),
    ]


def h16b(b): return hashlib.sha256(b).hexdigest()[:16]
def h16(p): return h16b(open(p, 'rb').read())


def construye(nombre, p, b):
    src = open(ORIGEN, 'rb').read()
    if h16b(src) != SHA_O1: raise SystemExit(f"origen {ORIGEN} sha {h16b(src)} != {SHA_O1}")
    txt = src.decode('utf-8')
    for a, rep in anclas(nombre, p, b):
        n = txt.count(a)
        if n != 1: raise SystemExit(f"ancla {a[:70]!r} aparece {n} veces (se exige 1)")
        txt = txt.replace(a, rep)
    return txt.encode('utf-8')


def todas():
    return {n: construye(n, p, b) for n, p, b in VARIANTES}


def main(argv=None):
    ap = argparse.ArgumentParser(allow_abbrev=False)
    ap.add_argument('--verifica', action='store_true')
    a = ap.parse_args(argv)
    T = todas()
    l1 = T['O1_LUGAR'].decode().split(NL); l0 = T['O1_LUGAR0'].decode().split(NL); lb = T['O1_LUGAR_BAR'].decode().split(NL)
    d0 = [i for i, (x, y) in enumerate(zip(l1, l0)) if x != y]; db = [i for i, (x, y) in enumerate(zip(l1, lb)) if x != y]
    if not (len(l1) == len(l0) == len(lb)) or len(d0) != 3 or len(db) != 3:
        raise SystemExit(f"las variantes difieren en {d0} / {db} (se esperan 3 lineas: nombre, encabezado y la perilla)")
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
