"""construye_n9c.py (v2) — SUBIDA DEL NIVEL 9, TANDA 3 (persistir con capacidad de carga): construye los cuatro carros N9C_*
POR ANCLAS desde experimentos/carrera_escuderias/carros/FABRICA.py (sha fijado abajo; el origen solo se LEE).

MISION: llegar a la AGI por este camino.

Diagnostico (PREREGISTRO_n9c.md sec. 0): en la pista v2 con quimiostato el organismo propio (FABRICA = mitad cerebro del
brazo REL de organismo_f9c) muere a los ~100 pasos y el 99-100 % de sus nacidos muere por VENENO o SAL, aun con la tabla
verdadera (subida_n10, ORACULO). La boca decide con un VALOR aprendido (Rescorla-Wagner) contra un sesgo de hambre; tras una
mordida mala ese valor es chico (-1.35) y el hambre lo tapa: un cuerpo recien nacido (E = Ag = 0.6) muerde lo malo que ya
probo. Practica v1 (practica_v1/, humo 14191): leer las dos filas pesadas por el deficit + copiar los pesos del padre NO
alcanzo (todas las muertes de nacidos siguen siendo por B/D; el control cruzado empata con el candidato).

v2 (este archivo). Dos perillas; ninguna constante nueva; ningun rng nuevo:
  BOCA = 'activa'   FABRICA tal cual.
         'predice'  MODELO DIRECTO DEL CUERPO: para una letra que el cuerpo (o su linaje) ya mordio, la boca PREDICE su propio
                    estado tras morderla con el efecto SENTIDO (media de dS por letra, lo que resultado() le devuelve) y usa
                    como valor el CODIGO DE RECOMPENSA DEL TRONCO (+1 / -3 / 0, el mismo _Rv de FABRICA) aplicado al cambio
                    PREDICHO de su deficit total D = sum_n clip(1 - nivel_n, 0, 1) (setpoint 1.0 = el de FABRICA):
                    +1 si D baja, -3 si D sube, 0 si no cambia. El resto de la boca (sesgo de hambre, temperatura, el MISMO
                    uniforme) no cambia. Letra nunca mordida: decide el valor aprendido de FABRICA (explorar sigue igual).
                    Consecuencia (no escrita como regla): lo malo se muerde solo si la necesidad que golpea queda >= 1.0
                    (limpiar sin pagar deficit); lo bueno, si baja el deficit o es neutro.
  HER  = 'nada'     el hijo nace sin memoria de efectos (FABRICA: hereda = 'nada').
         'memoria'  el padre VIVO pasa en el parto su memoria de efectos sentidos (por letra: suma dE, suma dAg, mordidas).
         'cruz'     CONTROL DE CONTENIDO: la misma memoria, por el mismo canal, con dE y dAg INTERCAMBIADOS (lo que el linaje
                    sintio en la comida pasa como si fuera del agua y viceversa). Mismo tamano, mismas magnitudes y conteos.
  Memoria NUEVA declarada: 4 letras x 3 numeros por cuerpo (la misma forma que la memoria de letras de APR, aprende_barrer).
  Los fundadores que pone el mundo siguen LIMPIOS (ENMIENDA 5; la pista no llama a nace()).

Carros (diff de DOS lineas entre ellos: BOCA y HER):
  N9C_NADA   activa  / nada     == FABRICA bit a bit (arnes identidad_n9c.py)   ancla
  N9C_PRED   predice / nada     la boca que predice, sin herencia (cada cuerpo sabe solo lo que el mordio)
  N9C_CAND   predice / memoria  CANDIDATO
  N9C_CRUZ   predice / cruz     control de contenido (puede ganar si lo que ayuda es tener memoria y no lo sentido)
"""
import hashlib, os, sys

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
ORIGEN = os.path.join(RAIZ, 'experimentos', 'carrera_escuderias', 'carros', 'FABRICA.py')
SHA_ORIGEN = '2ebee3e99ea5a33a'
DESTINO = os.path.join(AQUI, 'carros')
CARROS = dict(NADA=('activa', 'nada'), PRED=('predice', 'nada'), CAND=('predice', 'memoria'), CRUZ=('predice', 'cruz'))


def h16(p):
    return hashlib.sha256(open(p, 'rb').read()).hexdigest()[:16]


ANCLAS = [
    # (0) cabecera
    ('"""carros/FABRICA.py — EL CARRO DE FABRICA de la carrera de escuderias.\n',
     '"""carros/N9C_{ET}.py (CONSTRUIDO por experimentos/subida_n9c/construye_n9c.py v2 desde carros/FABRICA.py, sha {SHA};\n'
     'NO editar a mano). SUBIDA_N9C: BOCA = {BOCA!r}, HER = {HER!r}. Con BOCA = \'activa\' y HER = \'nada\' es FABRICA.\n\n'
     'carros/FABRICA.py — EL CARRO DE FABRICA de la carrera de escuderias.\n'),
    # (1) las dos perillas
    ('import numpy as np\n\n# perillas que eligen RAMA',
     'import numpy as np\n\nBOCA = {BOCA!r}   # SUBIDA_N9C: activa | predice\nHER = {HER!r}   # SUBIDA_N9C: nada | memoria | cruz\n\n'
     '# perillas que eligen RAMA'),
    # (2) memoria de efectos sentidos + telemetria (no toca la fisica ni el rng)
    ("        self._R = 0.; self._Rp = 0.; self._hambre = 0.; self._enc = None\n",
     "        self._R = 0.; self._Rp = 0.; self._hambre = 0.; self._enc = None\n"
     "        self._fm = {}   # SUBIDA_N9C: memoria de efectos SENTIDOS por letra: [suma dE, suma dAg, mordidas] (solo con BOCA 'predice')\n"
     "        self._n9c = dict(recibido=0, letras_recibidas=0, partos=0, pred=0, pred_malo=0, pred_malo_muerde=0, expl=0)   # telemetria\n"),
    # (3) la boca: modelo directo del cuerpo
    ("            if _cue2: _wt = min(_wt, self._vnec(1 - _na, PAT[kk], kc))\n",
     "            if _cue2: _wt = min(_wt, self._vnec(1 - _na, PAT[kk], kc))\n"
     "            _fm9 = self._fm.get(kk) if BOCA == 'predice' else None\n"
     "            if _fm9 is not None and _fm9[2] > 0:   # SUBIDA_N9C: predice su estado tras morder con el efecto SENTIDO\n"
     "                _D0 = float(np.clip(1 - E, 0, 1) + np.clip(1 - Ag, 0, 1))\n"
     "                _D1 = float(np.clip(1 - min(E + _fm9[0] / _fm9[2], 1.5), 0, 1) + np.clip(1 - min(Ag + _fm9[1] / _fm9[2], 1.5), 0, 1))\n"
     "                _wt = (1.0 if _D1 < _D0 else (-3.0 if _D1 > _D0 else 0.0))   # el codigo de recompensa del tronco (_Rv)\n"
     "                self._n9c['pred'] += 1; _ml9 = int(_fm9[0] < 0 or _fm9[1] < 0); self._n9c['pred_malo'] += _ml9\n"
     "            elif BOCA == 'predice': self._n9c['expl'] += 1; _ml9 = 0\n"),
    # (4) telemetria de la decision (despues del MISMO uniforme de FABRICA)
    ("            pb = 1 / (1 + np.exp(-Vb / .3)); mordio = bool(rng.random() < pb)\n",
     "            pb = 1 / (1 + np.exp(-Vb / .3)); mordio = bool(rng.random() < pb)\n"
     "            if BOCA == 'predice': self._n9c['pred_malo_muerde'] += int(mordio and _ml9)\n"),
    # (5) lo sentido entra a la memoria de efectos (sin rng)
    ("        _dS = res['dS']; _Rv = [(1.0 if _x > 0 else (-3.0 if _x < 0 else 0.0)) for _x in _dS]\n",
     "        _dS = res['dS']; _Rv = [(1.0 if _x > 0 else (-3.0 if _x < 0 else 0.0)) for _x in _dS]\n"
     "        if BOCA == 'predice':   # SUBIDA_N9C: memoria de efectos SENTIDOS\n"
     "            _m9 = self._fm.setdefault(kk, [0.0, 0.0, 0]); _m9[0] += float(_dS[0]); _m9[1] += float(_dS[1]); _m9[2] += 1\n"),
    # (6) al_parir: la memoria de efectos del padre VIVO viaja con el hijo
    ("    def al_parir(self, info):\n        return None   # hereda='nada': el hijo no se lleva memoria (la dote la pone la pista)\n",
     "    def al_parir(self, info):\n"
     "        if HER == 'nada': return None   # hereda='nada': el hijo no se lleva memoria (la dote la pone la pista)\n"
     "        self._n9c['partos'] += 1   # SUBIDA_N9C: copia de la memoria de efectos sentidos (sin rng)\n"
     "        return {_k9: [float(_v9[0]), float(_v9[1]), int(_v9[2])] for _k9, _v9 in self._fm.items()}\n"),
    # (7) nace: el hijo instala la memoria (despues de consumir su rng_hijo igual que FABRICA)
    ("        # EL NODO: exposiciones sin consecuencia por la VIA LENTA, relevancia viva (nodo_rel=1)\n",
     "        _mem9 = info.get('memoria')\n"
     "        if HER != 'nada' and isinstance(_mem9, dict):   # SUBIDA_N9C: el hijo recibe lo que el linaje sintio\n"
     "            for _k9, _v9 in _mem9.items():\n"
     "                self._fm[_k9] = ([float(_v9[1]), float(_v9[0]), int(_v9[2])] if HER == 'cruz' else [float(_v9[0]), float(_v9[1]), int(_v9[2])])\n"
     "            self._n9c['recibido'] = 1; self._n9c['letras_recibidas'] = len(_mem9)\n"
     "        # EL NODO: exposiciones sin consecuencia por la VIA LENTA, relevancia viva (nodo_rel=1)\n"),
    # (8) salida: clave nueva SOLO fuera de NADA
    ("            _rep_cuello=int(kw['rep_cuello']))\n",
     "            _rep_cuello=int(kw['rep_cuello']), **({} if (BOCA == 'activa' and HER == 'nada') else dict(n9c=dict(boca=BOCA, her=HER,\n"
     "            memoria={_k9: [round(_v9[0] / max(_v9[2], 1), 3), round(_v9[1] / max(_v9[2], 1), 3), int(_v9[2])] for _k9, _v9 in sorted(self._fm.items())}, **self._n9c))))\n"),
]


def fuente(et):
    boca, her = CARROS[et]
    src = open(ORIGEN, encoding='utf-8').read()
    for a, _ in ANCLAS:
        if src.count(a) != 1: raise SystemExit(f"construye_n9c: ancla no unica ({src.count(a)}): {a[:70]!r}")
    for a, b in ANCLAS:
        src = src.replace(a, b.replace('{ET}', et).replace('{SHA}', SHA_ORIGEN).replace('{BOCA!r}', repr(boca)).replace('{HER!r}', repr(her)))
    return src


def construye():
    if h16(ORIGEN) != SHA_ORIGEN:
        raise SystemExit(f"construye_n9c: FABRICA.py cambio ({h16(ORIGEN)} != {SHA_ORIGEN})")
    os.makedirs(DESTINO, exist_ok=True)
    out = {}
    for et in CARROS:
        p = os.path.join(DESTINO, f'N9C_{et}.py')
        open(p, 'w', encoding='utf-8', newline='\n').write(fuente(et))
        out[et] = h16(p)
    return out


if __name__ == '__main__':
    if len(sys.argv) > 1: raise SystemExit(f"construye_n9c: no acepta argumentos ({sys.argv[1:]})")
    for et, h in construye().items(): print(f"N9C_{et}.py {h}")
