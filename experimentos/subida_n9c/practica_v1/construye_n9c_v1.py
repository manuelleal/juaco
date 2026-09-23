"""construye_n9c.py — SUBIDA DEL NIVEL 9, TANDA 3 (persistir con capacidad de carga): construye los cinco carros N9C_*
POR ANCLAS desde experimentos/carrera_escuderias/carros/FABRICA.py (sha fijado abajo; el origen solo se LEE).

MISION: llegar a la AGI por este camino.

Diagnostico (solo lectura, PREREGISTRO_n9c.md sec. 0): en la pista v2 con quimiostato el organismo propio (FABRICA = mitad
cerebro del brazo REL de organismo_f9c) muere a los ~100 pasos y el 99-100 % de sus nacidos muere por VENENO o SAL, aun con la
tabla verdadera (FAMILIA_ORACULO de subida_n10: 590/593 muertes por B/D en una semilla). La causa esta en la boca: decide
con la fila de la necesidad ACTIVA; con sed, el veneno vale 0 para el agua y lo muerde (H-BOCA, reproducido 4/4 en la fase 10
externa). Y en v2 el hijo nace en blanco (hereda='nada'): lo que el padre aprendio muere con el.

Dos perillas (memoria nueva en el organismo: CERO; ninguna constante nueva; ningun rng nuevo):
  BOCA = 'activa'  FABRICA tal cual (fila de la necesidad activa; minimo de las dos filas si esta saciado).
         'deriva'  el valor de la mordida es el GRADIENTE DE LA DERIVA homeostatica (Hull; Keramati y Gutkin 2014): la suma
                   de las dos filas de valor APRENDIDAS, cada una pesada por el deficit de su necesidad relativo al deficit
                   mayor (la fila activa pesa 1; la otra, d_otra/d_activa en [0, 1]). Saciado: igual que FABRICA (minimo).
                   Con la otra necesidad llena (d_otra = 0) es FABRICA exacto. No hay umbral de 'cuando limpiar': morder lo
                   malo cuesta en proporcion a cuanto le falta al cuerpo la necesidad que golpea.
  HER  = 'nada'    FABRICA tal cual (el hijo nace en blanco).
         'todo'    el padre VIVO pasa en el parto una COPIA de su estado aprendido (Wl, KW, activa, Wp, Wn, Wps, Wns, err, mu,
                   mup, mun, zp, zn, ncod, _ord); el hijo la instala al nacer (despues de consumir su rng_hijo igual que
                   FABRICA). Los fundadores que pone el mundo siguen LIMPIOS (ENMIENDA 5; la pista no llama a nace()).
         'cruz'    CONTROL DE CONTENIDO: la misma copia, por el mismo canal, con las dos filas de necesidad INTERCAMBIADAS en
                   Wp, Wn, Wps, Wns (lo aprendido para la comida pasa como si fuera del agua y viceversa). Mismo tamano, mismas
                   magnitudes, misma estructura de celdas y mismo motor; solo cambia a que necesidad se refiere el contenido.

Carros (diff de DOS lineas entre ellos: BOCA y HER):
  N9C_NADA   activa / nada   == FABRICA bit a bit (arnes identidad_n9c.py)   ancla
  N9C_BOCA   deriva / nada   la boca sola
  N9C_HER    activa / todo   la herencia sola
  N9C_CAND   deriva / todo   CANDIDATO
  N9C_CRUZ   deriva / cruz   control de contenido (puede ganar si lo que ayuda es el canal y no lo aprendido)
"""
import hashlib, os, sys

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
ORIGEN = os.path.join(RAIZ, 'experimentos', 'carrera_escuderias', 'carros', 'FABRICA.py')
SHA_ORIGEN = '2ebee3e99ea5a33a'
DESTINO = os.path.join(AQUI, 'carros')
CARROS = dict(NADA=('activa', 'nada'), BOCA=('deriva', 'nada'), HER=('activa', 'todo'), CAND=('deriva', 'todo'),
              CRUZ=('deriva', 'cruz'))
HEREDA = ('Wl', 'KW', 'activa', 'Wp', 'Wn', 'Wps', 'Wns', 'err', 'mu', 'mup', 'mun', 'zp', 'zn')   # arrays copiados en el parto
FILAS = ('Wp', 'Wn', 'Wps', 'Wns')   # arrays con una fila por necesidad (los que 'cruz' intercambia)


def h16(p):
    return hashlib.sha256(open(p, 'rb').read()).hexdigest()[:16]


ANCLAS = [
    # (0) cabecera
    ('"""carros/FABRICA.py — EL CARRO DE FABRICA de la carrera de escuderias.\n',
     '"""carros/N9C_{ET}.py (CONSTRUIDO por experimentos/subida_n9c/construye_n9c.py desde carros/FABRICA.py, sha {SHA};\n'
     'NO editar a mano). SUBIDA_N9C: BOCA = {BOCA!r}, HER = {HER!r}. Con BOCA = \'activa\' y HER = \'nada\' es FABRICA.\n\n'
     'carros/FABRICA.py — EL CARRO DE FABRICA de la carrera de escuderias.\n'),
    # (1) las dos perillas
    ('import numpy as np\n\n# perillas que eligen RAMA',
     'import numpy as np\n\nBOCA = {BOCA!r}   # SUBIDA_N9C: activa | deriva\nHER = {HER!r}   # SUBIDA_N9C: nada | todo | cruz\n'
     "_N9C_HEREDA = ('Wl', 'KW', 'activa', 'Wp', 'Wn', 'Wps', 'Wns', 'err', 'mu', 'mup', 'mun', 'zp', 'zn')\n"
     "_N9C_FILAS = ('Wp', 'Wn', 'Wps', 'Wns')\n\n# perillas que eligen RAMA"),
    # (2) telemetria propia (no toca la fisica ni el rng)
    ("        self._R = 0.; self._Rp = 0.; self._hambre = 0.; self._enc = None\n",
     "        self._R = 0.; self._Rp = 0.; self._hambre = 0.; self._enc = None\n"
     "        self._n9c = dict(recibido=0, partos=0, enc=0, enc_otra=0, cambia=0)   # SUBIDA_N9C: solo telemetria\n"),
    # (3) la boca: gradiente de la deriva (dos filas pesadas por el deficit)
    ("            if _cue2: _wt = min(_wt, self._vnec(1 - _na, PAT[kk], kc))\n",
     "            if BOCA == 'deriva' and not _cue2:   # SUBIDA_N9C: fila activa (peso 1) + otra fila * d_otra / d_activa\n"
     "                _d9 = (float(np.clip(1 - E, 0, 1)), float(np.clip(1 - Ag, 0, 1))); _dm9 = max(_d9)\n"
     "                _w9 = _wt + (_d9[1 - _na] / _dm9) * self._vnec(1 - _na, PAT[kk], kc)\n"
     "                self._n9c['enc'] += 1; self._n9c['enc_otra'] += int(_d9[1 - _na] > 0)\n"
     "                self._n9c['cambia'] += int((self.ALPHA * _w9 + self.HAMBRE_BOCA * hambre + .5 > 0) != (self.ALPHA * _wt + self.HAMBRE_BOCA * hambre + .5 > 0))\n"
     "                _wt = _w9\n"
     "            if _cue2: _wt = min(_wt, self._vnec(1 - _na, PAT[kk], kc))\n"),
    # (4) al_parir: copia del estado aprendido del padre VIVO
    ("    def al_parir(self, info):\n        return None   # hereda='nada': el hijo no se lleva memoria (la dote la pone la pista)\n",
     "    def al_parir(self, info):\n"
     "        if HER == 'nada': return None   # hereda='nada': el hijo no se lleva memoria (la dote la pone la pista)\n"
     "        # SUBIDA_N9C: copia del estado APRENDIDO del padre vivo (sin rng, sin memoria nueva)\n"
     "        self._n9c['partos'] += 1\n"
     "        _m9 = {}\n"
     "        for _a9, _v9 in (('Wl', self.Wl), ('KW', self.KW), ('activa', self.activa), ('Wp', self.Wp), ('Wn', self.Wn),\n"
     "                         ('Wps', self.Wps), ('Wns', self.Wns), ('err', self.err), ('mu', self.mu), ('mup', self.mup),\n"
     "                         ('mun', self.mun), ('zp', self.zp), ('zn', self.zn)): _m9[_a9] = _v9.copy()\n"
     "        _m9['ncod'] = dict(self.ncod); _m9['_ord'] = list(self._ord)\n"
     "        return _m9\n"),
    # (5) nace: el hijo instala la copia DESPUES de consumir su rng_hijo como FABRICA (mismo estado de rng en los tres modos)
    ("        # EL NODO: exposiciones sin consecuencia por la VIA LENTA, relevancia viva (nodo_rel=1)\n",
     "        _mem9 = info.get('memoria')\n"
     "        if HER != 'nada' and isinstance(_mem9, dict):   # SUBIDA_N9C: el hijo instala lo aprendido por el padre\n"
     "            for _a9, _v9 in (('Wl', self.Wl), ('KW', self.KW), ('activa', self.activa), ('Wp', self.Wp), ('Wn', self.Wn),\n"
     "                             ('Wps', self.Wps), ('Wns', self.Wns), ('err', self.err), ('mu', self.mu), ('mup', self.mup),\n"
     "                             ('mun', self.mun), ('zp', self.zp), ('zn', self.zn)):\n"
     "                _x9 = np.asarray(_mem9[_a9])\n"
     "                if HER == 'cruz' and _a9 in _N9C_FILAS: _x9 = _x9[::-1]   # CONTROL: contenido referido a la otra necesidad\n"
     "                _v9[...] = _x9\n"
     "            self.ncod.update(_mem9['ncod']); self._ord.extend(_mem9['_ord'])\n"
     "            self._n9c['recibido'] = 1\n"
     "        # EL NODO: exposiciones sin consecuencia por la VIA LENTA, relevancia viva (nodo_rel=1)\n"),
    # (6) salida: clave nueva SOLO fuera de NADA
    ("            _rep_cuello=int(kw['rep_cuello']))\n",
     "            _rep_cuello=int(kw['rep_cuello']), **({} if (BOCA == 'activa' and HER == 'nada') else dict(n9c=dict(boca=BOCA, her=HER, **self._n9c))))\n"),
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
