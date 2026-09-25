"""construye_frio.py — CONSTRUCTOR POR ANCLAS del bloque F1 ARRANQUE EN FRIO (comite de linaje, 25-sep-2026).

MISION: llegar a la AGI por este camino (organismo minimo con reglas locales, sin retropropagacion, peldanos preregistrados con
controles y replicas).

Construye DOS archivos, cada uno desde su origen con sha fijado, por reemplazos de ancla que deben aparecer EXACTAMENTE una vez:
  carros/BAR0_ECO.py        <- experimentos/juaco_eco/carros/FAMB_RES0_ECO.py (94ea78589bc2ce24): MODO = 'res' -> 'bar'.
                               = BAR_SIN0 de subida_n10c/carros_n10c.py (FAMB_BAR + filtro SIN0 ANTES de la permutacion) con el _see
                               de ECO. FAMB_BAR y FAMB_RES de subida_n10b difieren SOLO en MODO (diff comprobado); la rama 'bar' ya
                               esta en el carro de ECO, verbatim: permuta las R entre las entradas con un rng propio [860000, entropia
                               del rng del hijo], sin tocar ningun rng del mundo.
  motor_frio_rapido.py      <- experimentos/juaco_eco/motor_eco_rapido_fam.py (d1f16769a53bb51c), el gemelo del arnes 132/132:
    (a) rutas: el archivo vive en frio/ pero lee motor_eco, carros y pista2 de juaco_eco/ y generaciones/ (mismos sha fijados);
    (b) acepta ademas el cerebro BAR0_ECO.py (sha fijado aqui) con MODO = 'bar' y SIN0 = 1; LFAM = 2 marca sus linajes;
    (c) en el parto de un linaje BAR0 (LFAM == 2), ANTES de _nace_fam: filtro SIN0 y permutacion de las R (en objmode, con las
        mismas lineas del carro); _nace_fam vuelve a filtrar (no-op: el multiset de R no tiene ceros);
    (d) ERR-146 (guardia ERR-60 / nube-9): el limite de cuerpos por linaje pasa de 100 000 a 1e9. La semilla de cada cuerpo en este
        motor es la LISTA [seed, linaje, ETQ, k] (SeedSequence), que no colisiona para k distintos (< 2**32); la guardia de 100 000
        venia de la formula escalar 700000 + 1000000*seed + k de H-1, que aqui no existe. Mientras ningun linaje pase de 100 000
        cuerpos, la salida es la MISMA (la guardia solo abortaba); el arnes lo comprueba contra el gemelo original.
    (e) FIRMA_GEMELO propia (un checkpoint de un motor no se reanuda con el otro).
Con los cerebros FABRICA_ECO / FAMB_RES0_ECO el motor copiado == el gemelo original BIT A BIT (identidad_frio.py, bloque A).

Uso:  python construye_frio.py            (escribe los dos archivos)
      python construye_frio.py --verifica (comprueba que los archivos en disco son los construidos; no escribe)
"""
import hashlib, os, sys

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(AQUI)))
ECO = os.path.join(RAIZ, 'experimentos', 'juaco_eco')
ORIG_CARRO = os.path.join(ECO, 'carros', 'FAMB_RES0_ECO.py'); SHA_CARRO = '94ea78589bc2ce24'
ORIG_MOTOR = os.path.join(ECO, 'motor_eco_rapido_fam.py'); SHA_MOTOR = 'd1f16769a53bb51c'
DEST_CARRO = os.path.join(AQUI, 'carros', 'BAR0_ECO.py')
DEST_MOTOR = os.path.join(AQUI, 'motor_frio_rapido.py')


def h16(p):
    return hashlib.sha256(open(p, 'rb').read()).hexdigest()[:16]


def reemplaza(s, anclas, que):
    for viejo, nuevo in anclas:
        n = s.count(viejo)
        if n != 1: raise SystemExit(f"construye_frio: ancla de {que} aparece {n} veces (debe ser 1): {viejo[:80]!r}")
        s = s.replace(viejo, nuevo)
    return s


def texto_carro():
    if h16(ORIG_CARRO) != SHA_CARRO: raise SystemExit(f"construye_frio: {ORIG_CARRO} cambio de sha")
    s = open(ORIG_CARRO, encoding='utf-8').read()
    return reemplaza(s, [
        ('"""carros/FAMB_RES0_ECO.py (CONSTRUIDO',
         '"""carros/BAR0_ECO.py (CONSTRUIDO por experimentos/organelos/frio/construye_frio.py desde juaco_eco/carros/FAMB_RES0_ECO.py, '
         'sha 94ea78589bc2ce24; NO editar a mano). F1 ARRANQUE EN FRIO: control de CONTENIDO BAR0 = MODO \'bar\' con SIN0 = 1 (el\n'
         'BAR_SIN0 de subida_n10c con el _see de ECO). Lo que sigue es el docstring del origen.\n\ncarros/FAMB_RES0_ECO.py (CONSTRUIDO'),
        ("MODO = 'res'   # SUBIDA_N10B: nada | res | res1 | bar | oraculo",
         "MODO = 'bar'   # SUBIDA_N10B: nada | res | res1 | bar | oraculo   (F1 FRIO: BAR0, construye_frio.py)"),
    ], 'BAR0_ECO')


def texto_motor(sha_bar):
    if h16(ORIG_MOTOR) != SHA_MOTOR: raise SystemExit(f"construye_frio: {ORIG_MOTOR} cambio de sha")
    s = open(ORIG_MOTOR, encoding='utf-8').read()
    return reemplaza(s, [
        ('"""motor_eco_rapido_fam.py — GEMELO COMPILADO',
         '"""motor_frio_rapido.py (CONSTRUIDO por experimentos/organelos/frio/construye_frio.py desde juaco_eco/motor_eco_rapido_fam.py,\n'
         'sha d1f16769a53bb51c; NO editar a mano). F1 ARRANQUE EN FRIO. Cambios: (a) rutas a juaco_eco; (b) + cerebro BAR0_ECO (LFAM 2);\n'
         '(c) permutacion de BAR0 en el parto (objmode, lineas del carro); (d) ERR-146: guardia ERR-60 a 1e9 cuerpos por linaje (la\n'
         'semilla [seed, linaje, ETQ, k] no colisiona); (e) firma propia. Lo que sigue es el docstring del origen.\n\n'
         'motor_eco_rapido_fam.py — GEMELO COMPILADO'),
        ("AQUI = os.path.dirname(os.path.abspath(__file__))\nRAIZ = os.path.dirname(os.path.dirname(AQUI))\n",
         "FRIO = os.path.dirname(os.path.abspath(__file__))   # F1 FRIO: este archivo vive en experimentos/organelos/frio\n"
         "RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(FRIO)))\n"
         "AQUI = os.path.join(RAIZ, 'experimentos', 'juaco_eco')   # F1 FRIO: motor_eco, carros y sha fijados, los de juaco_eco\n"),
        ("       os.path.join(AQUI, 'carros', 'FAMB_RES0_ECO.py'): '94ea78589bc2ce24',\n",
         "       os.path.join(AQUI, 'carros', 'FAMB_RES0_ECO.py'): '94ea78589bc2ce24',\n"
         f"       os.path.join(FRIO, 'carros', 'BAR0_ECO.py'): '{sha_bar}',   # F1 FRIO\n"),
        ("CEREBROS = {'FABRICA.py': '2ebee3e99ea5a33a', 'FABRICA_ECO.py': 'f1163009cb5193a2', 'FAMB_RES0_ECO.py': '94ea78589bc2ce24'}\n",
         "CEREBROS = {'FABRICA.py': '2ebee3e99ea5a33a', 'FABRICA_ECO.py': 'f1163009cb5193a2', 'FAMB_RES0_ECO.py': '94ea78589bc2ce24',\n"
         f"            'BAR0_ECO.py': '{sha_bar}'}}   # F1 FRIO: + BAR0\n"
         "BARAJA = 'BAR0_ECO.py'   # F1 FRIO: la misma tabla con las R permutadas (MODO = 'bar', SIN0 = 1); LFAM = 2\n"),
        ("FIRMA_GEMELO = 'motor_eco_rapido_fam v1'", "FIRMA_GEMELO = 'motor_frio_rapido v1'"),
        ("ERR_MSG = {ERR_NAC: 'PISTA2: mas de 100000 cuerpos en un linaje: la semilla colisionaria (ERR-60)',",
         "LIM_NAC = 1_000_000_000   # F1 FRIO, ERR-146: era 100000 (guardia ERR-60); la semilla en lista no colisiona\n"
         "ERR_MSG = {ERR_NAC: 'motor_frio_rapido: mas de 1e9 cuerpos en un linaje (guardia ERR-60, subida por ERR-146)',"),
        ("                if li[lin, L_NAC] >= 100000:\n", "                if li[lin, L_NAC] >= LIM_NAC:   # F1 FRIO, ERR-146\n"),
        ("                    if k >= 100000:\n", "                    if k >= LIM_NAC:   # F1 FRIO, ERR-146\n"),
        ("                    if LFAM[lin]:   # ch.nace(dict(..., memoria=mem, ...)): SIN0 + tabla + lectura del nodo\n",
         "                    if LFAM[lin] == 2:   # F1 FRIO: BAR0 (MODO 'bar'): SIN0 y permutacion de las R ANTES de instalar\n"
         "                        mt = _baraja(lin, k, mt, tn, tk, tR, sin0)\n"
         "                    if LFAM[lin]:   # ch.nace(dict(..., memoria=mem, ...)): SIN0 + tabla + lectura del nodo\n"),
        ("_CTX = {}\n",
         "_CTX = {}\n\n\n"
         "def _py_perm(i, k, m):\n"
         "    \"\"\"F1 FRIO, BAR0: las MISMAS lineas del carro (nace, MODO 'bar'): rng [860000] + entropia del rng del hijo [seed, i, 13, k].\"\"\"\n"
         "    _rh = np.random.default_rng([_CTX['seed'], i, P.ETQ['hijo'], k])\n"
         "    _rb = np.random.default_rng([860000] + [int(_z) for _z in np.atleast_1d(_rh.bit_generator.seed_seq.entropy)])\n"
         "    return np.ascontiguousarray(_rb.permutation(m), np.int64)\n\n\n"
         "@njit(cache=True)\n"
         "def _baraja(lin, k, m, tn, tk, tR, sin0):\n"
         "    \"\"\"F1 FRIO, BAR0: filtro SIN0 (como _nace_fam) y R[e] <- R[perm[e]] (claves y multiset intactos). Devuelve el n filtrado.\"\"\"\n"
         "    m2 = 0\n"
         "    for e in range(m):\n"
         "        if sin0 == 0 or tR[e] != 0.0:\n"
         "            tn[m2] = tn[e]; tk[m2] = tk[e]; tR[m2] = tR[e]; m2 += 1\n"
         "    with objmode(pn='int64[:]'):\n"
         "        pn = _py_perm(lin, k, m2)\n"
         "    tmp = tR[:m2].copy()\n"
         "    for e in range(m2): tR[e] = tmp[pn[e]]\n"
         "    return m2\n"),
        ("    if os.path.basename(mod.__file__) == FAMILIA:   # el nodo",
         "    if os.path.basename(mod.__file__) in (FAMILIA, BARAJA):   # F1 FRIO: + BAR0 · el nodo"),
        ("        if f_ == FAMILIA and (getattr(m_, 'MODO', None) != 'res' or getattr(m_, 'SIN0', None) != 1):\n",
         "        if f_ == BARAJA and (getattr(m_, 'MODO', None) != 'bar' or getattr(m_, 'SIN0', None) != 1):   # F1 FRIO\n"
         "            raise ValueError(f\"motor_frio_rapido: el carro {e_!r} no es MODO = 'bar' con SIN0 = 1\")\n"
         "        if f_ == FAMILIA and (getattr(m_, 'MODO', None) != 'res' or getattr(m_, 'SIN0', None) != 1):\n"),
        ("    LFAM = np.array([int(os.path.basename(m_.__file__) == FAMILIA) for e_, m_ in mods], np.int64)\n",
         "    LFAM = np.array([(1 if b_ == FAMILIA else (2 if b_ == BARAJA else 0)) for b_ in (os.path.basename(m_.__file__) for e_, m_ in mods)],\n"
         "                    np.int64)   # F1 FRIO: 2 = BAR0\n"),
    ], 'motor_frio_rapido')


def main(argv):
    c = texto_carro()
    sha_bar = hashlib.sha256(c.encode('utf-8')).hexdigest()[:16]
    m = texto_motor(sha_bar)
    if '--verifica' in argv:
        ok = (os.path.exists(DEST_CARRO) and open(DEST_CARRO, encoding='utf-8').read() == c and
              os.path.exists(DEST_MOTOR) and open(DEST_MOTOR, encoding='utf-8').read() == m)
        print(f"construye_frio --verifica: {'IGUAL' if ok else 'DISTINTO'} (BAR0_ECO {sha_bar} · motor_frio_rapido "
              f"{hashlib.sha256(m.encode('utf-8')).hexdigest()[:16]})")
        return ok
    os.makedirs(os.path.dirname(DEST_CARRO), exist_ok=True)
    with open(DEST_CARRO, 'w', encoding='utf-8', newline='\n') as f: f.write(c)
    with open(DEST_MOTOR, 'w', encoding='utf-8', newline='\n') as f: f.write(m)
    print(f"escrito carros/BAR0_ECO.py ({h16(DEST_CARRO)}) y motor_frio_rapido.py ({h16(DEST_MOTOR)})")
    return True


if __name__ == '__main__':
    sys.exit(0 if main(sys.argv[1:]) else 1)
