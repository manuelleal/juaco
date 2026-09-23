"""construye_familia.py — SUBIDA DEL NIVEL 10 (familias vivas): construye los cuatro carros FAMILIA_* POR ANCLAS desde
experimentos/carrera_escuderias/carros/FABRICA.py (sha fijado abajo; el origen solo se LEE, nunca se edita).

MISION: llegar a la AGI por este camino.

Pregunta: en el mundo CON CAPACIDAD DE CARGA (pista v2, generaciones que conviven, quimiostato), el organismo real del
proyecto (FABRICA = mitad cerebro del brazo REL de organismo_f9c) perdio su unico canal de herencia: el NODO se llenaba
al MORIR el padre y en v2 ningun cuerpo nace de un muerto (INFORME_CONVIVE.md: "FABRICA pierde su nodo REL").
Mecanismo minimo (MEMORIA NUEVA: CERO; el nodo ya existe): el nodo viaja EN EL PARTO desde el padre VIVO =
  lo que el padre heredo (self._nodo) + sus ultimas NODO_K mordidas (las mismas que muere() anade en v1),
y el hijo lo lee al nacer por la MISMA regla de relevancia de F9 (nodo_rel=1, NODO_LEE), sin tocar una linea de la lectura.

Cuatro carros, diff de UNA linea entre ellos (MODO):
  FAMILIA_NADA     MODO='nada'     == FABRICA bit a bit (arnes identidad_familia.py)
  FAMILIA_PARTO    MODO='parto'    candidato
  FAMILIA_BAR      MODO='bar'      control de CONTENIDO: mismo canal, mismos patrones, mismas R y necesidades (marginales),
                                   las R se PERMUTAN entre mensajes (como nodo_baraja de F9/ALMA2). rng PROPIO del barajado
                                   [860000] + entropia de rng_hijo: NO consume el rng del cuerpo, del hijo ni del mundo.
  FAMILIA_ORACULO  MODO='oraculo'  cota superior: el hijo recibe la TABLA VERDADERA (patron, necesidad) -> R, NODO_LEE copias
                                   (como nodo_or de F9C), por el mismo canal y la misma lectura.
Los fundadores (extincion del linaje) siguen LIMPIOS en los cuatro (ENMIENDA 5; la pista no llama a nace()).
"""
import hashlib, os, sys

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
ORIGEN = os.path.join(RAIZ, 'experimentos', 'carrera_escuderias', 'carros', 'FABRICA.py')
SHA_ORIGEN = '2ebee3e99ea5a33a'
DESTINO = os.path.join(AQUI, 'carros')
MODOS = dict(NADA='nada', PARTO='parto', BAR='bar', ORACULO='oraculo')


def h16(p):
    return hashlib.sha256(open(p, 'rb').read()).hexdigest()[:16]


ANCLAS = [
    # (0) cabecera
    ('"""carros/FABRICA.py — EL CARRO DE FABRICA de la carrera de escuderias.\n',
     '"""carros/FAMILIA_{ET}.py (CONSTRUIDO por experimentos/subida_n10/construye_familia.py desde carros/FABRICA.py,\n'
     'sha {SHA}; NO editar a mano). SUBIDA_N10: el nodo viaja en el PARTO (MODO = {MODO!r}). Con MODO = \'nada\' es FABRICA.\n\n'
     'carros/FABRICA.py — EL CARRO DE FABRICA de la carrera de escuderias.\n'),
    # (1) la perilla (una linea distinta entre los cuatro carros)
    ('import numpy as np\n\n# perillas que eligen RAMA',
     'import numpy as np\n\nMODO = {MODO!r}   # SUBIDA_N10: nada | parto | bar | oraculo\n\n# perillas que eligen RAMA'),
    # (2) telemetria propia (no toca la fisica ni el rng)
    ("        self._R = 0.; self._Rp = 0.; self._hambre = 0.; self._enc = None\n",
     "        self._R = 0.; self._Rp = 0.; self._hambre = 0.; self._enc = None\n"
     "        self._n10 = dict(recibido=-1, partos=0, dado=[])   # SUBIDA_N10: solo telemetria (salida con MODO != 'nada')\n"
     "        self._ORA = None\n"
     "        if MODO == 'oraculo':   # SUBIDA_N10: tabla verdadera (patron, necesidad) -> R, de VAL_VIVO/EFECTO que YA existian\n"
     "            _vv = cf['VAL_VIVO']; _ef = cf['EFECTO']\n"
     "            self._ORA = [[[float(_z9) for _z9 in self.PAT[_k9]], float(1.0 if _ef[_vv[_k9]][_n9] > 0 else (-3.0 if _ef[_vv[_k9]][_n9] < 0 else 0.0)), int(_n9)]\n"
     "                         for _n9 in range(min(self.N_NEC, 2)) for _k9 in 'ABCD']\n"),
    # (3) al_parir: el nodo del padre VIVO viaja con el hijo
    ("    def al_parir(self, info):\n        return None   # hereda='nada': el hijo no se lleva memoria (la dote la pone la pista)\n",
     "    def al_parir(self, info):\n"
     "        if MODO == 'nada': return None   # hereda='nada': el hijo no se lleva memoria (la dote la pone la pista)\n"
     "        # SUBIDA_N10: lo heredado + las ultimas NODO_K mordidas del padre VIVO (las mismas que muere() anade al nodo)\n"
     "        _msg = [[list(_p7), float(_r7), int(_n7)] for _p7, _r7, _n7 in self._nodo]\n"
     "        _msg += [[[float(_z9) for _z9 in self.PAT[_k9]], float(_R9), int(_n9)] for _t9, _k9, _n9, _R9 in self._mordh[-self.NODO_K:]]\n"
     "        self._n10['partos'] += 1; self._n10['dado'].append(len(_msg))\n"
     "        return _msg\n"),
    # (4) nace: el hijo instala el mensaje en su nodo ANTES de la lectura de F9 (que no se toca)
    ("        # EL NODO: exposiciones sin consecuencia por la VIA LENTA, relevancia viva (nodo_rel=1)\n",
     "        _mem = info.get('memoria')\n"
     "        if MODO != 'nada' and _mem is not None:   # SUBIDA_N10: el mensaje del padre pasa a ser el nodo del hijo\n"
     "            if MODO == 'oraculo':\n"
     "                _mem = [[list(_p7), _r7, _n7] for _p7, _r7, _n7 in self._ORA] * max(1, self.NODO_LEE)\n"
     "            elif MODO == 'bar':   # control de CONTENIDO: permuta las R entre mensajes (rng propio, no toca ningun rng del mundo)\n"
     "                _rb = np.random.default_rng([860000] + [int(_z) for _z in np.atleast_1d(_rh.bit_generator.seed_seq.entropy)])\n"
     "                _pn = _rb.permutation(len(_mem))\n"
     "                _mem = [[list(_mem[_i7][0]), float(_mem[int(_pn[_i7])][1]), int(_mem[_i7][2])] for _i7 in range(len(_mem))]\n"
     "            self._nodo = [[list(_p7), float(_r7), int(_n7)] for _p7, _r7, _n7 in _mem]\n"
     "            self._n10['recibido'] = len(self._nodo)\n"
     "        # EL NODO: exposiciones sin consecuencia por la VIA LENTA, relevancia viva (nodo_rel=1)\n"),
    # (5) salida: clave nueva SOLO con MODO != 'nada'
    ("            _rep_cuello=int(kw['rep_cuello']))\n",
     "            _rep_cuello=int(kw['rep_cuello']), **({} if MODO == 'nada' else dict(n10=dict(modo=MODO, recibido=self._n10['recibido'],\n"
     "            partos=self._n10['partos'], dado=self._n10['dado'][:50], nodo_n=len(self._nodo)))))\n"),
]


def construye():
    if h16(ORIGEN) != SHA_ORIGEN:
        raise SystemExit(f"construye_familia: FABRICA.py cambio ({h16(ORIGEN)} != {SHA_ORIGEN})")
    src = open(ORIGEN, encoding='utf-8').read()
    for a, _ in ANCLAS:
        if src.count(a) != 1: raise SystemExit(f"construye_familia: ancla no unica ({src.count(a)}): {a[:70]!r}")
    os.makedirs(DESTINO, exist_ok=True)
    out = {}
    for et, modo in MODOS.items():
        s = src
        for a, b in ANCLAS:
            s = s.replace(a, b.replace('{ET}', et).replace('{SHA}', SHA_ORIGEN).replace('{MODO!r}', repr(modo)))
        p = os.path.join(DESTINO, f'FAMILIA_{et}.py')
        open(p, 'w', encoding='utf-8', newline='\n').write(s)
        out[et] = h16(p)
    return out


if __name__ == '__main__':
    for et, h in construye().items(): print(f"FAMILIA_{et}.py {h}")
