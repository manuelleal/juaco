"""construye_o1_lib_f2.py — construye POR ANCLAS el carro O1_LIB_F2 ("un gen por parto") del bloque o1_libre_f2 (1-oct-2026).

MISION: llegar a la AGI por este camino (organismo minimo con reglas locales, sin retropropagacion, peldanos preregistrados con
controles y replicas). Ficha F2 de investigacion_20261001/ENTREGA_1_reactor.md: "la carga de mutar los 14 genes en cada parto, no la
seleccion, tapa la subida".

ORIGEN (solo se LEE; sha16 fijado; cada ancla EXACTAMENTE una vez o aborta):
  experimentos/organelos/o1_libre/carros/O1_LIB.py (SHA_LIB = ff30214f59ed36d8; bloque cerrado, no se toca). Fin de linea LF.

UNICO CAMBIO (4 anclas): una perilla de modulo PS_UNGEN (la fija el RUNNER por corrida; 0 por defecto).
  PS_UNGEN 0: _ps_muta es la de O1_LIB (los 14 genes reciben N(0, sigma_j) en cada evento, con self._psrng): el carro es O1_LIB bit a bit
              (lo unico que se ejecuta de mas es CREAR self._ugrng, una rng propia [PS_SEMILLA, indice, instancia, 7724] que nadie consume).
  PS_UNGEN 1: cada EVENTO de mutacion (cada parto, y cada fundador/refundador: _ps_muta es la unica puerta de mutacion del carro) muta UN
              gen j elegido al azar uniforme entre los 14 con self._ugrng, con la MISMA sigma_j = PS_SIGMA * PS_ESCALA[j] y el MISMO clip;
              los otros 13 pasan iguales. self._psrng ya no se consume en la mutacion (sigue eligiendo la entrada de siembra/colonia, que
              ocurre ANTES de mutar: misma eleccion que en O1_LIB para la misma semilla e instancia).
              Telemetria de SOLO ESCRITURA (solo con PS_UNGEN 1): _TEL[indice]['ungen'] = [eventos, cambia_1_gen, cambia_0 (recorte o sigma 0)]
              y _TEL[indice]['ungen_j'] = eventos por gen (14 contadores). Nadie la lee dentro de la corrida.
  Memoria nueva heredable: CERO. Estado nuevo por cuerpo: una rng.

    python experimentos/organelos/o1_libre_f2/construye_o1_lib_f2.py [--verifica]
"""
import argparse, ast, hashlib, os, sys

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(AQUI)))
ORIGEN = os.path.join(RAIZ, 'experimentos', 'organelos', 'o1_libre', 'carros', 'O1_LIB.py')
SALIDA = os.path.join(AQUI, 'carros')
NOMBRE = 'O1_LIB_F2'
SHA_LIB = 'ff30214f59ed36d8'
NL = '\n'

MUTA_F2 = (
    '        if PS_UNGEN:   # o1_libre_f2: UN gen por evento de mutacion (misma sigma_j, mismo clip); rng propia; self._psrng no se consume aqui' + NL
    + '            j = int(self._ugrng.integers(len(PS_GENES))); z = float(self._ugrng.normal(0.0, 1.0)); g = [float(x) for x in b]' + NL
    + '            g[j] = float(min(max(b[j] + PS_SIGMA * PS_ESCALA[j] * z, PS_CLIP[j][0]), PS_CLIP[j][1]))' + NL
    + "            _u = _TEL.setdefault(self._psi, {}); _c = _u.setdefault('ungen', [0, 0, 0]); _c[0] += 1; _c[1 if g[j] != float(b[j]) else 2] += 1" + NL
    + "            _u.setdefault('ungen_j', [0] * len(PS_GENES))[j] += 1" + NL
    + '            return g' + NL)

ANCLAS = [
    ('"""O1_LIB.py — o1_libre: O1 con TODAS sus constantes como genes heredables y 4 PODERES apagados (MEM, SOC, RES, PAU).' + NL,
     f'"""{NOMBRE}.py — o1_libre_f2: O1_LIB con la perilla PS_UNGEN (1 = UN gen por evento de mutacion; 0 = O1_LIB bit a bit).' + NL
     + f'GENERADO por experimentos/organelos/o1_libre_f2/construye_o1_lib_f2.py desde o1_libre/carros/O1_LIB.py (sha {SHA_LIB}). NO editar a mano.' + NL
     + 'Lo que sigue es el encabezado de O1_LIB:' + NL
     + 'O1_LIB.py — o1_libre: O1 con TODAS sus constantes como genes heredables y 4 PODERES apagados (MEM, SOC, RES, PAU).' + NL),
    ('SIEMBRA = None; PS_SEMILLA = 0; PS_SIGMA = 0.03; PS_LEE = 1; PS_ESCRIBE = 0; PS_COLONIZA = 0   # o1_libre: los fija el RUNNER por corrida' + NL,
     'SIEMBRA = None; PS_SEMILLA = 0; PS_SIGMA = 0.03; PS_LEE = 1; PS_ESCRIBE = 0; PS_COLONIZA = 0   # o1_libre: los fija el RUNNER por corrida' + NL
     + 'PS_UNGEN = 0   # o1_libre_f2: LA UNICA PERILLA NUEVA (la fija el RUNNER por corrida): 1 = cada evento de mutacion muta UN gen al azar' + NL),
    ('        self._pwrng = np.random.default_rng([int(PS_SEMILLA), i, c, 7722])' + NL,
     '        self._pwrng = np.random.default_rng([int(PS_SEMILLA), i, c, 7722])' + NL
     + '        self._ugrng = np.random.default_rng([int(PS_SEMILLA), i, c, 7724])   # o1_libre_f2: rng propia de "un gen" (solo se consume con PS_UNGEN 1)' + NL),
    ('    def _ps_muta(self, b):' + NL, '    def _ps_muta(self, b):' + NL + MUTA_F2),
]


def h16b(b): return hashlib.sha256(b).hexdigest()[:16]
def h16(p): return h16b(open(p, 'rb').read())


def construye():
    src = open(ORIGEN, 'rb').read()
    if h16b(src) != SHA_LIB: raise SystemExit(f"origen {ORIGEN} sha {h16b(src)} != {SHA_LIB}")
    txt = src.decode('utf-8')
    for a, rep in ANCLAS:
        n = txt.count(a)
        if n != 1: raise SystemExit(f"ancla {a[:70]!r} aparece {n} veces (se exige 1)")
        txt = txt.replace(a, rep)
    arbol = ast.parse(txt)
    # PS_UNGEN se LEE en un solo sitio (_ps_muta) y _ugrng se usa solo en _ps_init (crear) y _ps_muta (consumir)
    lee = [f.name for f in ast.walk(arbol) if isinstance(f, ast.FunctionDef)
           for nd in ast.walk(f) if isinstance(nd, ast.Name) and nd.id == 'PS_UNGEN' and isinstance(nd.ctx, ast.Load)]
    if lee != ['_ps_muta']: raise SystemExit(f"PS_UNGEN se lee en {lee} (se exige solo _ps_muta, una vez)")
    usa = sorted({f.name for f in ast.walk(arbol) if isinstance(f, ast.FunctionDef)
                  for nd in ast.walk(f) if isinstance(nd, ast.Attribute) and nd.attr == '_ugrng'})
    if usa != ['_ps_init', '_ps_muta']: raise SystemExit(f"_ugrng aparece en {usa}")
    # el resto del texto es el del origen: quitando las lineas agregadas queda el origen (salvo la primera linea del encabezado)
    o = src.decode('utf-8').split(NL); t = txt.split(NL)
    so = set(o); nuevas = [x for x in t if x not in so]
    if len(t) - len(o) != 11 or len(nuevas) != 12:   # 4 de encabezado (sale la linea 1 del origen) + 1 perilla + 1 rng + 6 de _ps_muta
        raise SystemExit(f"lineas agregadas {len(t) - len(o)} (se esperan 11) · nuevas {len(nuevas)} (se esperan 12)")
    if [x for x in t if x in so] != o[1:]: raise SystemExit("quitando las lineas nuevas NO queda el origen (sin su linea 1) linea a linea")
    return txt.encode('utf-8')


def main(argv=None):
    ap = argparse.ArgumentParser(allow_abbrev=False)
    ap.add_argument('--verifica', action='store_true')
    a = ap.parse_args(argv)
    b = construye(); ruta = os.path.join(SALIDA, NOMBRE + '.py')
    if a.verifica:
        igual = os.path.exists(ruta) and open(ruta, 'rb').read() == b
        print(f"  {NOMBRE}: en disco == construido: {igual} (sha {h16b(b)})"); return 0 if igual else 1
    os.makedirs(SALIDA, exist_ok=True)
    open(ruta, 'wb').write(b); print(f"  escrito {os.path.relpath(ruta, RAIZ)} sha {h16b(b)} (origen {SHA_LIB}, {len(ANCLAS)} anclas)")
    return 0


if __name__ == '__main__':
    sys.exit(main())
