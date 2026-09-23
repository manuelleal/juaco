"""construye_n9.py — construye POR ANCLAS los carros del bloque "el modelo de si es causal" (subida del nivel 9).

MISION: llegar a la AGI por este camino.

Origen (solo se LEE): experimentos/carrera_escuderias/carros/O3.py, sha fijado SHA_O3 (el carro que gano la ronda 2 por la
ENMIENDA 5 y estabilizo por la ENMIENDA 6, replicado en la sellada 9121-9140). Se trabaja en BYTES (fines de linea LF de O3.py).

Salidas en experimentos/subida_n9/carros/:
  O3.py               copia VERBATIM (mismo sha): el brazo de referencia corre desde esta carpeta.
  O3_LES_OFF.py       O3 + el INSTRUMENTO de lesion con las dos perillas en False: tiene que ser O3 BIT A BIT (identidad_n9.py).
  O3_LES_SI.py        LESION_SI = True: toda decision lee (E, Ag) de un paso PASADO al azar de los ultimos 2000 pasos del
                      LINAJE (misma marginal de estados propios, otro momento). La fisica sigue con el (E, Ag) verdadero.
  O3_LES_COLA.py      LESION_COLA = True: toda decision lee la reserva estimada del linaje (cola_est) de un paso PASADO al
                      azar de los ultimos 2000 pasos del linaje. DESCARTADA como brazo: fallo el chequeo (M) del arnes (tasa de TERMINAL 0.33).
  O3_TERM_CIEGO.py    O3 con COLA_TERM = 0: TERMINAL en cuanto el cuerpo lleva 2 partos, sin leer la reserva del linaje
                      (una constante; sin rng). Es el brazo de la lesion de la reserva (L-COLA quedo DESCARTADA por el arnes).
  FABRICA.py          copia VERBATIM (sha 2ebee3e99ea5a33a) para la identidad corta del juez; no corre en la serie.
  CTRL_O3_SINTERM.py  O3 con TERMINAL = False, con las MISMAS dos anclas de experimentos/generaciones/construye_ctrl_o3.py
                      (su sha tiene que ser 7bb2fff33017e559, el del control de generaciones).
La aleatoriedad de la lesion sale de ctx['rng'] (el rng de cuerpo del linaje que la pista le da al carro y que O3 NUNCA sortea);
el mundo, los hijos, las muertes y el turno tienen sus propios rng en la pista, asi que la lesion no mueve el mundo por si misma.
Uso: python experimentos/subida_n9/construye_n9.py
"""
import hashlib, os, sys

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
ORIGEN = os.path.join(RAIZ, 'experimentos', 'carrera_escuderias', 'carros', 'O3.py')
SHA_O3 = '0442c2884fcb0e11'
SHA_CTRL_GEN = '7bb2fff33017e559'   # experimentos/generaciones/carros_ctrl/CTRL_O3_SINTERM.py
ORIGEN_FAB = os.path.join(RAIZ, 'experimentos', 'carrera_escuderias', 'carros', 'FABRICA.py')
SHA_FAB = '2ebee3e99ea5a33a'   # copia VERBATIM: la identidad corta del juez (FABRICA solo == organismo_f9c REL) la carga de aqui
DEST = os.path.join(AQUI, 'carros')

CAB = (b'"""carros/O3.py \xe2\x80\x94 escuderia O3',
       b'"""@@NOMBRE@@ (construido por experimentos/subida_n9/construye_n9.py desde carrera_escuderias/carros/O3.py sha '
       + SHA_O3.encode() + b'; instrumento de LESION del modelo de si, perillas LESION_SI / LESION_COLA; las dos False = O3 bit a bit). '
       b'carros/O3.py \xe2\x80\x94 escuderia O3')

LESION = [
    # 1. perillas
    (b"PRUEBA_ULT = 0.45  # R2: nivel desde el que se prueba una letra desconocida abundante en desesperacion\n",
     b"PRUEBA_ULT = 0.45  # R2: nivel desde el que se prueba una letra desconocida abundante en desesperacion\n"
     b"# ---- LESIONES (subida_n9; instrumento, no mecanismo; las dos False = O3 bit a bit, arnes identidad_n9.py)\n"
     b"LESION_SI = False    # L-SI: las decisiones leen (E, Ag) de un paso PASADO al azar del linaje (ventana VENTANA_LES)\n"
     b"LESION_COLA = False  # L-COLA: las decisiones leen cola_est de un paso PASADO al azar del linaje (ventana VENTANA_LES)\n"
     b"VENTANA_LES = 2000   # el paso pasado sale de los ultimos VENTANA_LES pasos del LINAJE (misma marginal, otro momento)\n"),
    # 2. estado del instrumento (no decide nada con las perillas en False)
    (b"self.cola_est = 0; self.partos_cuerpo = 0; self._modo = 'o1'; self._prueba = None",
     b"self.cola_est = 0; self.partos_cuerpo = 0; self._modo = 'o1'; self._prueba = None\n"
     b"        self._hlev = []; self._hcola = []; self._ilev = 0; self._icola = 0; self._cola_dec = 0; self._term_ult = False\n"
     b"        self._les = dict(n=0, dlev=0.0, dcola=0.0, lev_real=[0.0, 0.0], lev_usado=[0.0, 0.0], cola_real=0.0, cola_usada=0.0,"
     b" cambia_term=0, term_real=0, term_usado=0)"),
    # 3. lectura del estado propio al empezar actua
    (b"pos = obs['pos']; lev = (float(obs['E']), float(obs['Ag'])); objs = obs['objs']\n",
     b"pos = obs['pos']; lev = (float(obs['E']), float(obs['Ag'])); objs = obs['objs']\n"
     b"        self._cola_dec = self.cola_est\n"
     b"        if LESION_SI or LESION_COLA: lev = self._lesiona(lev)\n"),
    # 4. TERMINAL lee la reserva que decide
    (b"        term = TERMINAL and self.partos_cuerpo >= PARTOS_TERM and self.cola_est >= COLA_TERM\n",
     b"        term = TERMINAL and self.partos_cuerpo >= PARTOS_TERM and self._cola_dec >= COLA_TERM\n"
     b"        if LESION_COLA: self._cuenta_term(term)\n"
     b"        self._term_ult = term\n"),
    # 5. limpieza por existencias
    (b"elif M3 and self.cola_est >= COLA_EXIST", b"elif M3 and self._cola_dec >= COLA_EXIST"),
    # 6. modo reserva (R1)
    (b"(RESERVA_COLA and self.cola_est <= COLA_RES)", b"(RESERVA_COLA and self._cola_dec <= COLA_RES)"),
    # 7. muerte declarada: con la lesion de la cola vale el TERMINAL que decidio el ultimo paso
    (b"if TERMINAL and self.partos_cuerpo >= PARTOS_TERM and self.cola_est >= COLA_TERM: self.st['cuerpos_term'] += 1",
     b"if (self._term_ult if LESION_COLA else (TERMINAL and self.partos_cuerpo >= PARTOS_TERM and self.cola_est >= COLA_TERM)): "
     b"self.st['cuerpos_term'] += 1"),
    # 8. la lesion
    (b"    def _hueco(self, pos, otros):",
     b"    def _lesiona(self, lev):\n"
     b"        \"\"\"LESION (subida_n9). L-SI: devuelve el (E, Ag) de un paso al azar entre los ultimos VENTANA_LES pasos del LINAJE\n"
     b"        (incluido el actual, a traves de sus cuerpos). L-COLA: fija self._cola_dec a la cola_est de un paso al azar de la misma\n"
     b"        ventana. Ventana del linaje y no historia del cuerpo: el arnes midio que sortear desde el nacimiento sesga la marginal\n"
     b"        hacia la juventud (E 0.91 contra 1.01; cola 1.44 contra 2.72; TERMINAL 5516 contra 27006 pasos). Un sorteo por lesion\n"
     b"        activa y por paso, del rng de cuerpo que la pista entrega al carro. Telemetria en self._les (no puntua).\"\"\"\n"
     b"        lu = lev\n"
     b"        if LESION_SI:\n"
     b"            self._ilev = self._anillo(self._hlev, self._ilev, lev); lu = self._hlev[int(self.rng.integers(len(self._hlev)))]\n"
     b"        if LESION_COLA:\n"
     b"            self._icola = self._anillo(self._hcola, self._icola, self.cola_est)\n"
     b"            self._cola_dec = self._hcola[int(self.rng.integers(len(self._hcola)))]\n"
     b"        s = self._les; s['n'] += 1\n"
     b"        s['dlev'] += abs(lu[0] - lev[0]) + abs(lu[1] - lev[1]); s['dcola'] += abs(self._cola_dec - self.cola_est)\n"
     b"        for j in (0, 1):\n"
     b"            s['lev_real'][j] += lev[j]; s['lev_usado'][j] += lu[j]\n"
     b"        s['cola_real'] += self.cola_est; s['cola_usada'] += self._cola_dec\n"
     b"        return lu\n"
     b"\n"
     b"    @staticmethod\n"
     b"    def _anillo(h, i, x):\n"
     b"        \"\"\"guarda x en el anillo h (ultimos VENTANA_LES pasos del linaje); devuelve el indice de escritura siguiente\"\"\"\n"
     b"        if len(h) < VENTANA_LES:\n"
     b"            h.append(x); return i\n"
     b"        h[i] = x; return (i + 1) % VENTANA_LES\n"
     b"\n"
     b"    def _cuenta_term(self, term):\n"
     b"        s = self._les; real = TERMINAL and self.partos_cuerpo >= PARTOS_TERM and self.cola_est >= COLA_TERM\n"
     b"        s['term_real'] += int(real); s['term_usado'] += int(term); s['cambia_term'] += int(real != term)\n"
     b"\n"
     b"    def _hueco(self, pos, otros):"),
    # 10. telemetria de la lesion (solo con alguna perilla encendida)
    (b"**{k: v for k, v in self.st.items()})",
     b"**{k: v for k, v in self.st.items()}, **({'lesion': dict(self._les)} if (LESION_SI or LESION_COLA) else {}))"),
]
PERILLAS = {'O3_LES_OFF': (), 'O3_LES_SI': ((b"\nLESION_SI = False ", b"\nLESION_SI = True  "),),
            'O3_LES_COLA': ((b"\nLESION_COLA = False ", b"\nLESION_COLA = True  "),)}
# CTRL_O3_SINTERM: las MISMAS dos anclas de experimentos/generaciones/construye_ctrl_o3.py (por eso el sha coincide)
CTRL = [(b'"""carros/O3.py \xe2\x80\x94 escuderia O3',
         b'"""CTRL_O3_SINTERM (construido por experimentos/generaciones/construye_ctrl_o3.py desde carros/O3.py sha '
         + SHA_O3.encode() + b'; UNICO cambio: TERMINAL = False). carros/O3.py \xe2\x80\x94 escuderia O3'),
        (b'\nTERMINAL = True\n', b'\nTERMINAL = False\n')]

# O3_TERM_CIEGO: la muerte programada NO lee la reserva del linaje (COLA_TERM 4 -> 0): TERMINAL en cuanto el cuerpo tiene 2 partos.
# Lesion determinista de UNA constante (sin rng). Reemplaza a L-COLA como brazo (L-COLA fallo el chequeo (M) del arnes: con la cola
# sorteada paso a paso la muerte programada parpadea y cae a 0.33 de la tasa real; se conserva en el instrumento, NO corre).
CIEGO = [(b'"""carros/O3.py \xe2\x80\x94 escuderia O3',
          b'"""O3_TERM_CIEGO (construido por experimentos/subida_n9/construye_n9.py desde carros/O3.py sha '
          + SHA_O3.encode() + b'; UNICO cambio: COLA_TERM = 0, la muerte programada no lee la reserva del linaje). '
          b'carros/O3.py \xe2\x80\x94 escuderia O3'),
         (b'\nCOLA_TERM = 4      # M3(c)\n', b'\nCOLA_TERM = 0      # M3(c)\n')]


def h16(b):
    return hashlib.sha256(b).hexdigest()[:16]


def aplica(src, anclas, nombre):
    out = src
    for i, (a, b) in enumerate(anclas, 1):
        n = out.count(a)
        if n != 1: raise SystemExit(f"CONSTRUYE {nombre}: el ancla {i} aparece {n} veces (tiene que ser 1): {a[:70]!r}")
        out = out.replace(a, b)
    return out


def construye(escribe=True):
    src = open(ORIGEN, 'rb').read(); sha = h16(src)
    if sha != SHA_O3: raise SystemExit(f"CONSTRUYE: O3.py cambio ({sha} != {SHA_O3})")
    res = {'O3': src}
    base = aplica(src, LESION, 'lesion')
    for nom, per in PERILLAS.items():
        cab = (CAB[0], CAB[1].replace(b'@@NOMBRE@@', nom.encode()))
        res[nom] = aplica(aplica(base, [cab], nom), list(per), nom)
    res['CTRL_O3_SINTERM'] = aplica(src, CTRL, 'CTRL_O3_SINTERM')
    res['O3_TERM_CIEGO'] = aplica(src, CIEGO, 'O3_TERM_CIEGO')
    fab = open(ORIGEN_FAB, 'rb').read()
    if h16(fab) != SHA_FAB: raise SystemExit(f"CONSTRUYE: FABRICA.py cambio ({h16(fab)} != {SHA_FAB})")
    res['FABRICA'] = fab
    if h16(res['CTRL_O3_SINTERM']) != SHA_CTRL_GEN:
        raise SystemExit(f"CONSTRUYE: CTRL_O3_SINTERM {h16(res['CTRL_O3_SINTERM'])} != {SHA_CTRL_GEN} (el de generaciones)")
    if escribe:
        os.makedirs(DEST, exist_ok=True)
        for nom, b in res.items():
            open(os.path.join(DEST, nom + '.py'), 'wb').write(b)
    return {nom: h16(b) for nom, b in res.items()}, sha


def main():
    shas, sha = construye()
    print(f"O3.py (origen) sha {sha} OK")
    for nom, s in shas.items(): print(f"  carros/{nom}.py sha {s}")
    return 0


if __name__ == '__main__':
    sys.exit(main())
