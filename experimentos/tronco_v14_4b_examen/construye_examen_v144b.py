"""construye_examen_v144b.py -- construye POR ANCLAS el runner y el arnes del examen v4 de v14.4b = v14.3 + TERMO' desde los del
examen de v14.4 (experimentos/tronco_v14_4_examen/, sha fijado). MISION: llegar a la AGI por este camino.
Cambian: los nombres de modulos y salidas (v144 -> v144b), las semillas (umbrales_examen_v144b), el constructor que se verifica
(construye_termop.py) y, en el arnes, el bloque de la MEMORIA (la de TERMO' es una media movil, no una suma) y la letra comparada
TAMBIEN con los carros V143_TERMOP / V143_TERMOPINV. La letra del examen, el juez y la T-G: iguales (se importan de v14.4 / v14.3).

    python experimentos/tronco_v14_4b_examen/construye_examen_v144b.py [--verifica]
"""
import hashlib, os, sys

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
V144 = os.path.join(RAIZ, 'experimentos', 'tronco_v14_4_examen')
ORIGENES = {os.path.join(V144, 'corre_examen_v144.py'): '8bb63d3f421040dd',
            os.path.join(V144, 'identidad_v144ex.py'): '6a714b193b6222dc'}


def h16b(b): return hashlib.sha256(b).hexdigest()[:16]


def origen(p):
    b = open(p, 'rb').read()
    if h16b(b) != ORIGENES[p]: raise SystemExit(f'*** ORIGEN {p}: sha {h16b(b)} != {ORIGENES[p]}')
    return b.decode('utf-8')


def sust(t, a, b, etq, n=1):
    c = t.count(a)
    if (n is None and c < 1) or (n is not None and c != n):
        raise SystemExit(f'*** ancla {etq!r} aparece {c} veces (se esperaban {n if n is not None else ">= 1"})')
    return t.replace(a, b)


GLOBAL = [('potencia_examen_v144_', '@@POT@@'), ('tronco_v14_4_examen', 'tronco_v14_4b_examen'),
          ('bateria_generaliza_v144', 'bateria_generaliza_v144b'), ('bateria_v144', 'bateria_v144b'),
          ('organismo_v144', 'organismo_v144b'), ('identidad_v144ex', 'identidad_v144bex'),
          ('umbrales_examen_v144', 'umbrales_examen_v144b'), ('corre_examen_v144', 'corre_examen_v144b'),
          ('examen_v144_', 'examen_v144b_'), ('PREREGISTRO_examen_v144.md', 'PREREGISTRO_examen_v144b.md'),
          ("'construye_v144.py'", "'construye_termop.py'"), ('v14.4 = v14.3 + TERMO', 'v14.4b = v14.3 + TERMOP'),
          ('v14.4 (v14.3 + TERMO)', 'v14.4b (v14.3 + TERMOP)'), ('v14.4 no se congela', 'v14.4b no se congela'),
          ('@@POT@@', 'potencia_examen_v144_')]


def globales(t, etq):
    for a, b in GLOBAL:
        t = t.replace(a, b)   # reemplazo global (puede no aparecer en el arnes); lo que importa lo comprueban regla14() y el arnes
    for a in ('organismo_v144.', 'organismo_v144g', 'organismo_v144cal', "'bateria_v144'", 'examen_v144_1', '@@POT@@'):
        if a in t: raise SystemExit(f'*** {etq}: quedo {a!r} sin reemplazar')
    return t


CAB_R = ('"""corre_examen_v144b.py = corre_examen_v144.py (8bb63d3f421040dd) para v14.4b = v14.3 + TERMOP (TERMO con memoria que olvida: '
         'media movil a la tasa ema_c del tronco). MISMA letra, mismo juez, misma T-G; semillas nuevas. GENERADO por '
         'experimentos/tronco_v14_4b_examen/construye_examen_v144b.py. NO editar a mano."""\n')
CAB_I = ('"""identidad_v144bex.py = identidad_v144ex.py (6a714b193b6222dc) para v14.4b = v14.3 + TERMOP. Cambia el bloque de la MEMORIA '
         '(media movil: en un mundo quieto e == dS exacto; tras invertir, A negativa y B positiva) y la letra se compara tambien con los '
         'carros V143_TERMOP / V143_TERMOPINV. GENERADO por construye_examen_v144b.py. NO editar a mano."""\n')


def construye():
    out = {}
    r = globales(origen(os.path.join(V144, 'corre_examen_v144.py')), 'runner')
    r = sust(r, "and C4.semilla_real(47101, 'TRONCO_B') == 147101 and C4.semilla_real(47101, 'OFF') == 47101",
             "and C4.semilla_real(49201, 'TRONCO_B') == 149201 and C4.semilla_real(49201, 'OFF') == 49201", 'runner: semilla_real')
    r = sust(r, "| set(range(43000, 44601)) | set(range(39001, 39141)) | set(range(39901, 39915)))",
             "| set(range(43000, 44601)) | set(range(39001, 39141)) | set(range(39901, 39915))\n"
             "              | set(range(47000, 48601)) | set(range(49001, 49100)) | set(range(49941, 49995)))", 'runner: usadas')
    r = sust(r, "all(47000 <= s <= 48600 for s in ss)", "all(49100 <= s <= 49940 or 149500 <= s <= 149999 for s in ss)", 'runner: rango')
    r = sust(r, "dentro de 47000-48600, ninguna de V4-CAL, subida_n7, tronco_v14_3, el '\n              'examen de v14.3 ni TERMO; TRONCO_B s+100000 (147xxx) libre",
             "dentro de 49100-49940 / 149500-149999, ninguna de V4-CAL, subida_n7, tronco_v14_3, los '\n              'examenes de v14.3 y v14.4, TERMO, el exploratorio de TERMO\\' ni la carrera de TERMO\\'; TRONCO_B s+100000 libre", 'runner: frase R6')
    r = sust(r, "    os.path.join(RAIZ, 'datos', 'humo', 'potencia_examen_v144_20260928_121917.json'): '4e4df40a5c3cc67d',\n",
             "    os.path.join(RAIZ, 'datos', 'humo', 'potencia_examen_v144_20260928_121917.json'): '4e4df40a5c3cc67d',\n"
             "    os.path.join(RAIZ, 'experimentos', 'tronco_v14_4_examen', 'umbrales_examen_v144.py'): '0df02bd6a4d548c4',   # T-G y letra (v14.4)\n",
             'runner: ancla umbrales v144')
    r = sust(r, "set(G144.INSTRUMENTOS) - set(G143.INSTRUMENTOS) == {'organismo_v144b'}",
             "set(G144.INSTRUMENTOS) - set(G143.INSTRUMENTOS) == {'organismo_v144', 'organismo_v144b'}", 'runner: R3 entradas nuevas')
    out['corre_examen_v144b.py'] = CAB_R + r
    i = globales(origen(os.path.join(V144, 'identidad_v144ex.py')), 'arnes')
    i = sust(i, "S = 47045 ", "S = 49905 ", 'arnes: semilla')
    i = sust(i, "organismo_v144bcal as V144C, construye_v144 as CO", "organismo_v144bcal as V144C, construye_termop as CO", 'arnes: constructor')
    i = sust(i, "(0) CONSTRUCCION: los cinco archivos en disco == construye_v144.construye()", "(0) CONSTRUCCION: los siete archivos en disco == construye_termop.construye()", 'arnes: doc 0')
    i = sust(i, "R.tarea_vivo(('VIVO', 47046, ", "R.tarea_vivo(('VIVO', 49906, ", 'arnes: semilla K', n=3)
    i = sust(i, "    import V143_TERMO as CT, V143_TERMOINV as CTI\n",
             "    import V143_TERMO as CT, V143_TERMOINV as CTI, importlib.util\n"
             "    def _carga(n):\n"
             "        s_ = importlib.util.spec_from_file_location(n, os.path.join(AQUI, 'carros', n + '.py')); m_ = importlib.util.module_from_spec(s_); s_.loader.exec_module(m_); return m_\n"
             "    CTP, CTPI = _carga('V143_TERMOP'), _carga('V143_TERMOPINV')\n", 'arnes: carros TERMOP')
    i = sust(i, "        c._adS = {k: list(v) for k, v in adS.items()}; c._tmU = float(U); c._tm = dict(dec=0, a_no=0, a_si=0, mord=0)\n",
             "        c._adS = {k: list(v) for k, v in adS.items()}; c._tmM = {k: list(v) for k, v in adS.items()}   # TERMO lee _adS; TERMO' lee _tmM\n"
             "        c._tmU = float(U); c._tm = dict(dec=0, a_no=0, a_si=0, mord=0)\n", 'arnes: carro sintetico')
    i = sust(i, "            for modo, mod in ((1, CT), (2, CTI)):\n", "            for modo, mod in ((1, CT), (2, CTI), (1, CTP), (2, CTPI)):\n", 'arnes: modos')
    i = sust(i, "termo_letra == V143_TERMO._tm_boca (modo 1) y V143_TERMOINV._tm_boca (modo 2)",
             "termo_letra == _tm_boca de V143_TERMO y V143_TERMOP (modo 1) y de V143_TERMOINV y V143_TERMOPINV (modo 2)", 'arnes: frase L')
    # la memoria: media movil (reemplaza el bloque de la suma secuencial)
    ini = i.index("    a1, _, kw, s = PV['T-A VIVO']\n    EF = V144C.EFECTO")
    fin = i.index("    print('--- (X) cadena")
    MEM = '''    a1, _, kw, s = PV['T-A VIVO']
    EF = V144C.EFECTO; VAL = V144C.VAL_VIVO
    det_m = {k: v for k, v in a1['termo']['adS'].items()}
    okm = all(v == [float(EF[VAL[k]][0]), float(EF[VAL[k]][1]), 1] and sum(a1['mord'][k]) > 0 for k, v in det_m.items())
    anota('L', f"TERMO': en el mundo vivo QUIETO (T-A VIVO) la memoria de cada estimulo mordido es EXACTAMENTE su dS nominal, con "
               f"'mordidas' = 1 (media movil de un valor constante): {det_m}", okm and len(det_m) == 4)
    a1, _, kw, s = PV['T-C (ii) reversion en T/2']
    mA, mB = a1['termo']['adS']['A'], a1['termo']['adS']['B']
    anota('L', f"TERMO' SE DESDICE: tras la reversion (T-C ii, T = {T}) la memoria de A es NEGATIVA ({mA[0]:.3f}) y la de B POSITIVA "
               f"({mB[0]:.3f})", mA[0] < 0 < mB[0] and mA[2] == mB[2] == 1)
    import inspect
    lam = inspect.signature(V144C.run).parameters['ema_c'].default
    c = object.__new__(CTP.Carro); c._tmM = {}; c._tmL = lam
    ref = None; ok_e = True
    for x in [(0.8, 0.0)] * 30 + [(-0.4, 0.0)] * 25 + [(0.0, 0.8)] * 3:
        c._tm_dS('A', x)
        ref = [x[0], x[1], 1] if ref is None else [ref[0] + lam * (x[0] - ref[0]), ref[1] + lam * (x[1] - ref[1]), 1]
        ok_e &= (c._tmM['A'] == ref)
    anota('L', f"el carro V143_TERMOP acumula con la MISMA regla (e <- dS; e <- e + ema_c (dS - e)) y ema_c del tronco == la de FABRICA "
               f"({lam}); 58 mordidas sinteticas identicas", ok_e and lam == 0.05)
'''
    i = i[:ini] + MEM + i[fin:]
    out['identidad_v144bex.py'] = CAB_I + i
    return out


if __name__ == '__main__':
    ver = '--verifica' in sys.argv
    if [a for a in sys.argv[1:] if a != '--verifica']: raise SystemExit('*** uso: construye_examen_v144b.py [--verifica]')
    malo = 0
    for n, t in construye().items():
        p = os.path.join(AQUI, n); b = t.encode('utf-8')
        if ver:
            ok = os.path.exists(p) and open(p, 'rb').read() == b; malo += not ok
            print(f"{'OK  ' if ok else 'DIFIERE'} {n:24s} {h16b(b)}")
        else:
            open(p, 'wb').write(b); print(f'escrito {n:24s} {h16b(b)}')
    sys.exit(1 if malo else 0)
