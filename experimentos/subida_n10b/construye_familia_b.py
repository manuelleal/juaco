"""construye_familia_b.py — SUBIDA DEL NIVEL 10, TANDA 2 (n10b): "la familia pasa su TABLA en vida".
Construye los carros FAMB_* POR ANCLAS desde experimentos/carrera_escuderias/carros/FABRICA.py (sha fijado; solo se LEE).

MISION: llegar a la AGI por este camino.

Diagnostico que decide el diseno (diagnostico_mensaje.py, practica 12392, T=20000): el mensaje de la tanda 1 (nodo heredado +
ultimas 20 mordidas del padre VIVO) trae 4 % de entradas con R < 0 y el 47 % de los mensajes no trae NINGUNA R < 0 propia; el
grueso es A|hambre +1 y C|hambre 0. Barajar R que casi todas valen lo mismo no cambia nada: por eso PARTO ~ BAR (11/20). El
mundo SI tiene donde usar contenido (ORACULO 0.553 contra NADA 0.110, 20/20): lo que faltaba era contenido en el mensaje.

Mecanismo n10b (MEMORIA NUEVA: CERO; ninguna constante nueva): el padre vivo pasa en el parto SU TABLA, una entrada por
(letra, necesidad): la R MAS RECIENTE que VIVIO en toda su vida (self._mordh, que ya existe) y, para las claves que no vivio, la
que HEREDO (self._nodo). A lo sumo 8 entradas. El hijo la instala como nodo en NODO_LEE copias (la MISMA dosis y la MISMA
lectura de F9 que el ORACULO de la tanda 1) y la vuelve a pasar enriquecida: la tabla ACUMULA por generaciones.

Carros (una linea distinta entre ellos: MODO):
  FAMB_NADA     'nada'     == FABRICA bit a bit (arnes)
  FAMB_RES      'res'      CANDIDATO: tabla de la familia (vivido + heredado)
  FAMB_RES1     'res1'     tabla SOLO de lo vivido por el padre (sin lo heredado): separa "acumula la familia" de "sabe el padre"
  FAMB_BAR      'bar'      CONTROL DE CONTENIDO: la tabla de RES con las R PERMUTADAS entre sus entradas en cada parto (mismas
                           claves, misma multiset de R, misma dosis); rng propio [860000]+entropia de rng_hijo (no consume rng)
  FAMB_ORACULO  'oraculo'  techo: == FAMILIA_ORACULO de la tanda 1 en toda la salida (arnes): la serie 12301-12320 lo calibra
"""
import hashlib, os, sys

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
ORIGEN = os.path.join(RAIZ, 'experimentos', 'carrera_escuderias', 'carros', 'FABRICA.py')
SHA_ORIGEN = '2ebee3e99ea5a33a'
DESTINO = os.path.join(AQUI, 'carros')
MODOS = dict(NADA='nada', RES='res', RES1='res1', BAR='bar', ORACULO='oraculo')


def h16(p):
    return hashlib.sha256(open(p, 'rb').read()).hexdigest()[:16]


ANCLAS = [
    # (0) cabecera
    ('"""carros/FABRICA.py — EL CARRO DE FABRICA de la carrera de escuderias.\n',
     '"""carros/FAMB_{ET}.py (CONSTRUIDO por experimentos/subida_n10b/construye_familia_b.py desde carros/FABRICA.py,\n'
     'sha {SHA}; NO editar a mano). SUBIDA_N10B: la familia pasa su TABLA en el parto (MODO = {MODO!r}). Con MODO = \'nada\' es FABRICA.\n\n'
     'carros/FABRICA.py — EL CARRO DE FABRICA de la carrera de escuderias.\n'),
    # (1) la perilla (una linea distinta entre los carros) + telemetria de modulo (solo modos de tabla)
    ('import numpy as np\n\n# perillas que eligen RAMA',
     'import numpy as np\n\nMODO = {MODO!r}   # SUBIDA_N10B: nada | res | res1 | bar | oraculo\n'
     '_TABLA = (\'res\', \'res1\', \'bar\')\n'
     '_TELE = []   # SUBIDA_N10B: telemetria (claves recibidas, R de B|hambre y D|sed en lo instalado); no toca la fisica\n\n'
     '# perillas que eligen RAMA'),
    # (2) telemetria propia + tabla del oraculo (texto IDENTICO a la tanda 1)
    ("        self._R = 0.; self._Rp = 0.; self._hambre = 0.; self._enc = None\n",
     "        self._R = 0.; self._Rp = 0.; self._hambre = 0.; self._enc = None\n"
     "        self._n10 = dict(recibido=-1, partos=0, dado=[])   # SUBIDA_N10: solo telemetria (salida con MODO != 'nada')\n"
     "        self._ORA = None\n"
     "        if MODO == 'oraculo':   # SUBIDA_N10: tabla verdadera (patron, necesidad) -> R, de VAL_VIVO/EFECTO que YA existian\n"
     "            _vv = cf['VAL_VIVO']; _ef = cf['EFECTO']\n"
     "            self._ORA = [[[float(_z9) for _z9 in self.PAT[_k9]], float(1.0 if _ef[_vv[_k9]][_n9] > 0 else (-3.0 if _ef[_vv[_k9]][_n9] < 0 else 0.0)), int(_n9)]\n"
     "                         for _n9 in range(min(self.N_NEC, 2)) for _k9 in 'ABCD']\n"),
    # (3) al_parir
    ("    def al_parir(self, info):\n        return None   # hereda='nada': el hijo no se lleva memoria (la dote la pone la pista)\n",
     "    def al_parir(self, info):\n"
     "        if MODO == 'nada': return None   # hereda='nada': el hijo no se lleva memoria (la dote la pone la pista)\n"
     "        if MODO in _TABLA:   # SUBIDA_N10B: la TABLA: por (patron, necesidad) la R mas reciente VIVIDA; si no la vivio, la HEREDADA\n"
     "            _tab = {}\n"
     "            if MODO != 'res1':\n"
     "                for _p7, _r7, _n7 in self._nodo: _tab[(tuple(float(_z) for _z in _p7), int(_n7))] = float(_r7)\n"
     "            for _t9, _k9, _n9, _R9 in self._mordh: _tab[(tuple(float(_z9) for _z9 in self.PAT[_k9]), int(_n9))] = float(_R9)\n"
     "            _o7 = {tuple(float(_z) for _z in self.PAT[_q7]): _i7 for _i7, _q7 in enumerate('ABCD')}   # orden del ORACULO: necesidad, letra\n"
     "            _msg = [[list(_c7[0]), _tab[_c7], _c7[1]] for _c7 in sorted(_tab, key=lambda _c7: (_c7[1], _o7.get(_c7[0], 99), _c7[0]))]\n"
     "            self._n10['partos'] += 1; self._n10['dado'].append(len(_msg))\n"
     "            return _msg\n"
     "        # SUBIDA_N10: lo heredado + las ultimas NODO_K mordidas del padre VIVO (las mismas que muere() anade al nodo)\n"
     "        _msg = [[list(_p7), float(_r7), int(_n7)] for _p7, _r7, _n7 in self._nodo]\n"
     "        _msg += [[[float(_z9) for _z9 in self.PAT[_k9]], float(_R9), int(_n9)] for _t9, _k9, _n9, _R9 in self._mordh[-self.NODO_K:]]\n"
     "        self._n10['partos'] += 1; self._n10['dado'].append(len(_msg))\n"
     "        return _msg\n"),
    # (4) nace: el hijo instala el mensaje en su nodo ANTES de la lectura de F9 (que no se toca)
    ("        # EL NODO: exposiciones sin consecuencia por la VIA LENTA, relevancia viva (nodo_rel=1)\n",
     "        _mem = info.get('memoria')\n"
     "        if MODO in _TABLA and _mem is not None:   # SUBIDA_N10B: la tabla del padre, NODO_LEE copias (dosis del ORACULO)\n"
     "            if MODO == 'bar':   # control de CONTENIDO: permuta las R entre las entradas (rng propio, no toca ningun rng del mundo)\n"
     "                _rb = np.random.default_rng([860000] + [int(_z) for _z in np.atleast_1d(_rh.bit_generator.seed_seq.entropy)])\n"
     "                _pn = _rb.permutation(len(_mem))\n"
     "                _mem = [[list(_mem[_i7][0]), float(_mem[int(_pn[_i7])][1]), int(_mem[_i7][2])] for _i7 in range(len(_mem))]\n"
     "            _tb = [[list(_p7), float(_r7), int(_n7)] for _p7, _r7, _n7 in _mem]\n"
     "            self._nodo = [[list(_e7[0]), _e7[1], _e7[2]] for _e7 in _tb] * max(1, self.NODO_LEE)\n"
     "            self._n10['recibido'] = len(self._nodo)\n"
     "            _g7 = {(_q7, _n7): _r7 for _p7, _r7, _n7 in _tb for _q7 in 'ABCD' if [float(_z) for _z in self.PAT[_q7]] == _p7}\n"
     "            _TELE.append((int(info.get('t', -1)), len(_tb), _g7.get(('B', 0)), _g7.get(('D', 1)), _g7.get(('A', 0)), _g7.get(('C', 1))))\n"
     "        elif MODO != 'nada' and _mem is not None:   # SUBIDA_N10: el mensaje del padre pasa a ser el nodo del hijo\n"
     "            if MODO == 'oraculo':\n"
     "                _mem = [[list(_p7), _r7, _n7] for _p7, _r7, _n7 in self._ORA] * max(1, self.NODO_LEE)\n"
     "            self._nodo = [[list(_p7), float(_r7), int(_n7)] for _p7, _r7, _n7 in _mem]\n"
     "            self._n10['recibido'] = len(self._nodo)\n"
     "        # EL NODO: exposiciones sin consecuencia por la VIA LENTA, relevancia viva (nodo_rel=1)\n"),
    # (5) salida: clave nueva SOLO con MODO != 'nada' (IDENTICA a la tanda 1)
    ("            _rep_cuello=int(kw['rep_cuello']))\n",
     "            _rep_cuello=int(kw['rep_cuello']), **({} if MODO == 'nada' else dict(n10=dict(modo=MODO, recibido=self._n10['recibido'],\n"
     "            partos=self._n10['partos'], dado=self._n10['dado'][:50], nodo_n=len(self._nodo)))))\n"),
]


def construye_texto(src, et, modo):
    s = src
    for a, b in ANCLAS:
        s = s.replace(a, b.replace('{ET}', et).replace('{SHA}', SHA_ORIGEN).replace('{MODO!r}', repr(modo)))
    return s


def construye():
    if h16(ORIGEN) != SHA_ORIGEN:
        raise SystemExit(f"construye_familia_b: FABRICA.py cambio ({h16(ORIGEN)} != {SHA_ORIGEN})")
    src = open(ORIGEN, encoding='utf-8').read()
    for a, _ in ANCLAS:
        if src.count(a) != 1: raise SystemExit(f"construye_familia_b: ancla no unica ({src.count(a)}): {a[:70]!r}")
    os.makedirs(DESTINO, exist_ok=True)
    out = {}
    for et, modo in MODOS.items():
        p = os.path.join(DESTINO, f'FAMB_{et}.py')
        open(p, 'w', encoding='utf-8', newline='\n').write(construye_texto(src, et, modo))
        out[et] = h16(p)
    return out


if __name__ == '__main__':
    if len(sys.argv) > 1: raise SystemExit(f"construye_familia_b: no admite argumentos ({sys.argv[1:]})")
    for et, h in construye().items(): print(f"FAMB_{et}.py {h}")
