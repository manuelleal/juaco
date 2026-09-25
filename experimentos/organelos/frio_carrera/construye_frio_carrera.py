"""construye_frio_carrera.py — construye POR ANCLAS los carros del bloque frio_carrera (F1 llevado a la pista de la carrera).

MISION: llegar a la AGI por este camino. F1 (experimentos/organelos/frio, FUNCIONA x2): la familia que pasa al hijo SOLO las entradas
de su tabla con R != 0 sostiene el linaje en ECO sin vivero. Aqui el mismo principio en la pista de la carrera, sobre el bicho real
v14.3. En la carrera el carro ES el cerebro del linaje: lo que heredan los nacidos (hijos de la cola) es el NODO del linaje (las ultimas
nodo_k = 20 mordidas de cada cuerpo muerto: [patron, R de la necesidad activa, necesidad]), que el que nace lee por la via lenta
(nodo_lee = 50 entradas, ordenadas por sorpresa). La traduccion mas fiel de RES_SIN0 / FAMB_RES0 es: el nacido lee el nodo SIN las
entradas neutras (R == 0). El nodo guardado NO se toca (se filtra una copia en cada lectura).

ORIGEN (solo se LEE; sha16 fijado; cada ancla debe aparecer EXACTAMENTE una vez o el constructor aborta):
  experimentos/tronco_v14_3/carros_v143/V143.py (SHA_V143 = 2a03048a7f1525e5, el candidato v14.3 de la serie 14301/14321)

PERILLAS (una linea nueva de modulo; con RES0 = BAR = TELEM = 0 el carro es V143 bit a bit -> identidad_frio_carrera.py):
  RES0   el nacido lee el nodo del linaje sin las entradas con R == 0 (H-NEUTRAS; F1). Cero memoria nueva.
  BAR    control de CONTENIDO que puede ganar: las R de las entradas que pasan se PERMUTAN entre entradas (patron y necesidad quedan)
         en cada lectura. Permutacion con splitmix64 propio en enteros de Python sembrado con (indice del linaje, t, k del parto):
         no consume NINGUN rng de la pista ni del cuerpo (revisa_carro prohibe np.random y default_rng en los carros).
  TELEM  telemetria de SOLO LECTURA en d['carro']['frio_carrera'] (el juez no la lee, ERR-96): entradas del nodo, neutras, cuantas
         de las leidas eran neutras, cuantas R cambio la permutacion. No toca la conducta (arnes (3): fisica identica a V143).
Genera en frio_carrera/carros/:
  V143_RES0   RES0 1, BAR 0, TELEM 1   (el candidato)
  V143_BAR0   RES0 1, BAR 1, TELEM 1   (control de contenido)
  V143_TEL    RES0 0, BAR 0, TELEM 1   (SOLO para el arnes y el humo: V143 con la telemetria; mide las neutras del nodo de V143)
Las variantes difieren SOLO en la linea de perillas y en el nombre (se verifica).

    python experimentos/organelos/frio_carrera/construye_frio_carrera.py [--verifica]
"""
import argparse, hashlib, os, sys

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(AQUI)))
ORIGEN = os.path.join(RAIZ, 'experimentos', 'tronco_v14_3', 'carros_v143', 'V143.py')
SALIDA = os.path.join(AQUI, 'carros')
SHA_V143 = '2a03048a7f1525e5'
NL = '\r\n'   # el origen tiene fin de linea CRLF (492/492); se conserva

VARIANTES = [('V143_RES0', 1, 0, 1), ('V143_BAR0', 1, 1, 1), ('V143_TEL', 0, 0, 1)]   # nombre, RES0, BAR, TELEM

PERILLAS = "RES0 = {r}; BAR = {b}; TELEM = {t}   # frio_carrera: LA UNICA LINEA QUE CAMBIA ENTRE VARIANTES (0/0/0 = V143 bit a bit)"

METODOS = '''
    # ================================================================ frio_carrera: F1 en la carrera (RES0 / BAR / TELEM)
    # Lo que hereda el nacido es el NODO del linaje. RES0: lee una COPIA sin las entradas neutras (R == 0). BAR: ademas, las R de esa
    # copia se permutan entre entradas (control de contenido). El nodo guardado no cambia. Nada lee el mundo ni consume rng.
    def _fc_init(self, ctx):
        self._fc_ind = int(ctx['indice'])
        self._fc = dict(lect=0, entradas=0, neutras=0, pasan=0, sel=0, sel_neutras=0, bar_lect=0, bar_distintas=0, bar_cambian=0,
                        bar_entradas=0)

    def _fc_perm(self, n, info):
        M = 0xFFFFFFFFFFFFFFFF
        x = (0x9E3779B97F4A7C15 * (36977 + 1000003 * self._fc_ind + 7919 * int(info['t']) + 104729 * int(info['k']))) & M
        idx = list(range(n))
        for i in range(n - 1, 0, -1):
            x = (x + 0x9E3779B97F4A7C15) & M
            z = ((x ^ (x >> 30)) * 0xBF58476D1CE4E5B9) & M
            z = ((z ^ (z >> 27)) * 0x94D049BB133111EB) & M
            z = z ^ (z >> 31)
            j = z % (i + 1); idx[i], idx[j] = idx[j], idx[i]
        return idx

    def _fc_msg(self, info):
        msg = list(self._nodo); fc = self._fc
        fc['lect'] += 1; fc['entradas'] += len(msg); fc['neutras'] += sum(1 for e in msg if e[1] == 0.0)
        if RES0: msg = [e for e in msg if e[1] != 0.0]
        if BAR and len(msg) > 1:
            pr = self._fc_perm(len(msg), info)
            m2 = [[e[0], float(msg[pr[i]][1]), e[2]] for i, e in enumerate(msg)]
            ch = sum(1 for a, b in zip(msg, m2) if a[1] != b[1])
            fc['bar_lect'] += 1; fc['bar_distintas'] += int(ch > 0); fc['bar_cambian'] += ch; fc['bar_entradas'] += len(msg)
            msg = m2
        fc['pasan'] += len(msg)
        return msg

    def _fc_sel(self, msg, sel):
        self._fc['sel'] += len(sel); self._fc['sel_neutras'] += sum(1 for i in sel if msg[i][1] == 0.0)

    def _fc_salida(self):
        return dict(res0=RES0, bar=BAR, telem=TELEM, **self._fc)
'''

ANCLAS = [
    ('"""V143.py — tronco_v14_3 (candidato a tronco v14.3): FABRICA + B-5 + FILTRO con META + boca TD de APR.' + NL,
     '"""{nombre}.py — frio_carrera (F1 en la pista de la carrera): V143 + el nacido lee el nodo del linaje sin neutras.' + NL
     + 'GENERADO por experimentos/organelos/frio_carrera/construye_frio_carrera.py desde tronco_v14_3/carros_v143/V143.py (sha {sha}).' + NL
     + 'NO editar a mano. Perillas: {perillas_txt}. Con RES0 = BAR = TELEM = 0 es V143 bit a bit. Sigue el docstring de V143.' + NL + NL
     + 'V143.py — tronco_v14_3 (candidato a tronco v14.3): FABRICA + B-5 + FILTRO con META + boca TD de APR.' + NL),
    ('DESAMB = 1; FILTRO = 1; META = 1; INVIERTE = 0   # tronco_v14_3: LA UNICA LINEA QUE CAMBIA ENTRE VARIANTES (con OPCION)' + NL,
     'DESAMB = 1; FILTRO = 1; META = 1; INVIERTE = 0   # tronco_v14_3: LA UNICA LINEA QUE CAMBIA ENTRE VARIANTES (con OPCION)' + NL
     + '{perillas}' + NL),
    ('        self._v3_init(ctx)' + NL,
     '        self._v3_init(ctx)' + NL + '        self._fc_init(ctx)   # frio_carrera: solo contadores (sin rng)' + NL),
    ('            _msg = list(self._nodo)' + NL,
     '            _msg = self._fc_msg(info) if (RES0 or BAR or TELEM) else list(self._nodo)   # frio_carrera' + NL),
    ('            self._ldiv += int(len(self._nodo) > self.NODO_LEE or (_sel9 != sorted(_sel9)))' + NL,
     '            self._ldiv += int(len(self._nodo) > self.NODO_LEE or (_sel9 != sorted(_sel9)))' + NL
     + '            if TELEM: self._fc_sel(_msg, _sel9)   # frio_carrera (solo lectura)' + NL),
    ("            **({'v143': self._v3_salida()} if (DESAMB or FILTRO) else {}))" + NL,
     "            **({'v143': self._v3_salida()} if (DESAMB or FILTRO) else {})," + NL
     + "            **({'frio_carrera': self._fc_salida()} if TELEM else {}))   # frio_carrera: telemetria (ERR-96: no puntua)" + NL
     + '{metodos}'),
]


def h16b(b): return hashlib.sha256(b).hexdigest()[:16]
def h16(p): return h16b(open(p, 'rb').read())


def construye(nombre, r, b, t):
    src = open(ORIGEN, 'rb').read()
    if h16b(src) != SHA_V143: raise SystemExit(f"origen {ORIGEN} sha {h16b(src)} != {SHA_V143}")
    txt = src.decode('utf-8')
    per = PERILLAS.format(r=r, b=b, t=t)
    metodos = METODOS.replace('\n', NL)
    for a, rep in ANCLAS:
        n = txt.count(a)
        if n != 1: raise SystemExit(f"ancla {a[:70]!r} aparece {n} veces (se exige 1)")
        rep = (rep.replace('{nombre}', nombre).replace('{sha}', SHA_V143).replace('{perillas_txt}', per.split('   #')[0])
               .replace('{perillas}', per).replace('{metodos}', metodos))
        txt = txt.replace(a, rep)
    return txt.encode('utf-8')


def todas():
    return {n: construye(n, r, b, t) for n, r, b, t in VARIANTES}


def main(argv=None):
    ap = argparse.ArgumentParser(allow_abbrev=False)
    ap.add_argument('--verifica', action='store_true')
    a = ap.parse_args(argv)
    outs = todas()
    # las variantes difieren SOLO en la linea de perillas y en el nombre
    base = outs['V143_RES0'].decode('utf-8').split(NL)
    for n, bts in outs.items():
        ls = bts.decode('utf-8').split(NL)
        dif = [i for i, (x, y) in enumerate(zip(base, ls)) if x != y]
        if len(ls) != len(base) or any(not ('RES0 = ' in ls[i] or n in ls[i]) for i in dif):
            raise SystemExit(f"{n}: difiere de V143_RES0 en algo mas que perillas/nombre: lineas {dif[:6]}")
    ok = True
    os.makedirs(SALIDA, exist_ok=True)
    for n, bts in outs.items():
        ruta = os.path.join(SALIDA, n + '.py')
        if a.verifica:
            igual = os.path.exists(ruta) and open(ruta, 'rb').read() == bts; ok &= igual
            print(f"  {n} sha {h16b(bts)} == disco: {igual}")
        else:
            with open(ruta, 'wb') as fh: fh.write(bts)
            print(f"  escrito {ruta} (sha {h16b(bts)})")
    print(f"origen V143.py sha {h16(ORIGEN)} (fijado {SHA_V143}) · construye_frio_carrera.py sha {h16(os.path.abspath(__file__))}")
    return 0 if ok else 1


if __name__ == '__main__':
    sys.exit(main())
