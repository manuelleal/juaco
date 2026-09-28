"""construye_carrera_termop.py -- construye POR ANCLAS el runner y el arnes de la CARRERA de TERMO' desde los de TERMO
(experimentos/organelos/termo/corre_termo.py e identidad_termo.py, sha fijado). MISION: llegar a la AGI por este camino.
MISMA pista, MISMA letra (lee_serie, bloque), mismos brazos en su papel: v143 (base), termop = V143_TERMOP (CANDIDATO), termopinv =
V143_TERMOPINV (CONTROL: la misma regla leyendo la necesidad que la letra NO sube), o1 (techo y ancla). Cambian: los carros (de
construye_termop.py), las semillas (nuevas: serie 49941-49960, replica 49961-49980, practica 49991-49994), el prefijo de salida y
el preregistro (PREREGISTRO_termop.md). En el arnes, el bloque (b)/(c) (TERMO == HIBB del diagnostico) se reemplaza por:
TERMO' == TERMO en la FISICA en una pista QUIETA (el dS de cada letra no cambia: la media movil == el dS exacto), TERMOPINV ==
TERMOINV, y la pieza actua.

    python experimentos/tronco_v14_4b_examen/construye_carrera_termop.py [--verifica]
"""
import hashlib, os, sys

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
TD = os.path.join(RAIZ, 'experimentos', 'organelos', 'termo')
ORIGENES = {os.path.join(TD, 'corre_termo.py'): '66f1f2539f1030ef', os.path.join(TD, 'identidad_termo.py'): '95249ad33bbde643'}


def h16b(b): return hashlib.sha256(b).hexdigest()[:16]


def origen(p):
    b = open(p, 'rb').read()
    if h16b(b) != ORIGENES[p]: raise SystemExit(f'*** ORIGEN {p}: sha {h16b(b)} != {ORIGENES[p]}')
    return b.decode('utf-8')


def sust(t, a, b, etq, n=1):
    c = t.count(a)
    if c != n: raise SystemExit(f'*** ancla {etq!r} aparece {c} veces (se esperaban {n})')
    return t.replace(a, b)


SEM = [('39101', '49941'), ('39120', '49960'), ('39121', '49961'), ('39140', '49980'), ('39141', '49981'),
       ('39911', '49991'), ('39912', '49992'), ('39913', '49993'), ('39914', '49994'), ('39915', '49995')]


def construye(shas_carros):
    out = {}
    r = origen(os.path.join(TD, 'corre_termo.py'))
    r = sust(r, "RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(AQUI)))", "RAIZ = os.path.dirname(os.path.dirname(AQUI))", 'raiz')
    r = sust(r, "import construye_termo as CB", "import construye_termop as CB", 'CB')
    r = sust(r, "PRERREGISTRO = 'PREREGISTRO_termo.md'", "PRERREGISTRO = 'PREREGISTRO_termop.md'", 'prereg')
    r = sust(r, "        os.path.join(AQUI, 'construye_termo.py'): '23f57933c51c64e8',\n"
                "        os.path.join(CARROS, 'V143_TERMO.py'): '3db639cab75641fb', os.path.join(CARROS, 'V143_TERMOINV.py'): 'da106a995b18bafd'}",
             f"        os.path.join(AQUI, 'construye_termop.py'): '{shas_carros['construye']}',\n"
             f"        os.path.join(CARROS, 'V143_TERMOP.py'): '{shas_carros['V143_TERMOP']}', os.path.join(CARROS, 'V143_TERMOPINV.py'): '{shas_carros['V143_TERMOPINV']}'}}",
             'SHAS')
    r = sust(r, "BRAZOS = {'v143': 'V143', 'termo': 'V143_TERMO', 'termoinv': 'V143_TERMOINV', 'o1': 'O1'}",
             "BRAZOS = {'v143': 'V143', 'termop': 'V143_TERMOP', 'termopinv': 'V143_TERMOPINV', 'o1': 'O1'}", 'BRAZOS')
    r = sust(r, "PROPIOS = ('V143_TERMO', 'V143_TERMOINV')", "PROPIOS = ('V143_TERMOP', 'V143_TERMOPINV')", 'PROPIOS')
    r = sust(r, "CAND = 'termo'; CTRL = 'termoinv'", "CAND = 'termop'; CTRL = 'termopinv'", 'CAND')
    r = sust(r, "SERIE_BRAZOS = ('v143', 'termo', 'termoinv', 'o1')", "SERIE_BRAZOS = ('v143', 'termop', 'termopinv', 'o1')", 'SERIE_BRAZOS')
    r = sust(r, "HUMO = [(39911, 'v143'), (39911, 'termo'), (39911, 'termoinv'), (39911, 'o1'), (39912, 'v143'), (39912, 'termo')]",
             "HUMO = [(39911, 'v143'), (39911, 'termop'), (39911, 'termopinv'), (39911, 'o1'), (39912, 'v143'), (39912, 'termop')]", 'HUMO')
    r = sust(r, "a.brazos or 'v143,termo,termoinv,o1'", "a.brazos or 'v143,termop,termopinv,o1'", 'humo brazos')
    # verifica(): los carros se comparan con construye_termop (claves 'carros/<nombre>.py')
    r = sust(r, "    for n, b in CB.todas().items():\n        ruta = os.path.join(CARROS, n + '.py'); igual = os.path.exists(ruta) and open(ruta, 'rb').read() == b",
             "    for n, b in {k[len('carros') + 1:-3]: v.encode('utf-8') for k, v in CB.construye().items() if k.startswith('carros')}.items():\n"
             "        ruta = os.path.join(CARROS, n + '.py'); igual = os.path.exists(ruta) and open(ruta, 'rb').read() == b", 'verifica carros')
    r = sust(r, "log(f\"  carro {n} sha {CB.h16b(b)} == construye: {igual}", "log(f\"  carro {n} sha {CB.h16b(b)} == construye_termop: {igual}", 'verifica log')
    r = sust(r, "['distinto de construye_termo']", "['distinto de construye_termop']", 'verifica msg')
    r = sust(r, 'pre = f"termo_{', 'pre = f"termop_{', 'prefijo')
    r = sust(r, 'log(f"CORRE_TERMO · ', 'log(f"CORRE_TERMOP · ', 'cabecera log')
    r = sust(r, 'f"corre_termo.py {h16(', 'f"corre_termop.py {h16(', 'log sha')
    for a, b in SEM:
        r = r.replace(a, b)
    CAB = ('"""corre_termop.py = experimentos/organelos/termo/corre_termo.py (66f1f2539f1030ef) para TERMO\' (memoria de lo sentido con '
           'olvido): MISMA pista y MISMA letra; carros V143_TERMOP / V143_TERMOPINV; semillas nuevas 49941-49994. Preregistro: '
           'PREREGISTRO_termop.md. GENERADO por construye_carrera_termop.py. NO editar a mano."""\n')
    out['corre_termop.py'] = CAB + r
    # ---- arnes
    i = origen(os.path.join(TD, 'identidad_termo.py')).replace(chr(13) + chr(10), chr(10))   # el origen trae CRLF: se normaliza a LF (declarado)
    i = sust(i, "import corre_termo as CT\nimport construye_termo as CB", "import corre_termop as CT\nimport construye_termop as CB", 'arnes imports')
    i = sust(i, "    chk(\"(K) construye_termo --verifica (carros == anclas desde V143.py 2a03048a7f1525e5; solo perillas/nombre)\", CB.main(['--verifica']) == 0)\n",
             "    chk(\"(K) construye_termop: carros en disco == construccion por anclas desde V143_TERMO / V143_TERMOINV (sha fijados)\",\n"
             "        all(open(os.path.join(AQUI, k), 'rb').read() == v.encode('utf-8') for k, v in CB.construye().items() if k.startswith('carros')))\n",
             'arnes K')
    i = sust(i, "TM = CV._MODS['V143_TERMO']; TI = CV._MODS['V143_TERMOINV']", "TM = CV._MODS['V143_TERMOP']; TI = CV._MODS['V143_TERMOPINV']", 'arnes mods')
    i = sust(i, "for nm, m in (('V143_TERMO', TM), ('V143_TERMOINV', TI)):", "for nm, m in (('V143_TERMOP', TM), ('V143_TERMOPINV', TI)):", 'arnes a')
    ini = i.index("    from hashlib import sha256\n"); fin = i.index("    lines = []\n")
    NUEVO = '''    import importlib.util as _iu
    def _carga(n, ruta):
        s_ = _iu.spec_from_file_location(n, ruta); m_ = _iu.module_from_spec(s_); s_.loader.exec_module(m_); return m_
    TD_ = os.path.join(CT.RAIZ, 'experimentos', 'organelos', 'termo', 'carros')
    T0, T0I = _carga('carro_TERMO_ref', os.path.join(TD_, 'V143_TERMO.py')), _carga('carro_TERMOINV_ref', os.path.join(TD_, 'V143_TERMOINV.py'))
    fis = lambda r: sin(r, ('carro', 'id'))
    R = {}
    for s, T in ((39913, 5000), (39914, 20000)):
        R[(s, T)] = run(TM, s, T)
        chk(f"(b) pista QUIETA: V143_TERMOP == V143_TERMO en la FISICA (todo salvo d['carro'] e id; s {s}, T {T}): la media movil de un dS "
            f"constante es ese dS", fis(R[(s, T)]) == fis(run(T0, s, T)))
    ri = run(TI, 39913, 5000)
    chk("(c) V143_TERMOPINV == V143_TERMOINV en la FISICA (s 39913, T 5000)", fis(ri) == fis(run(T0I, 39913, 5000)))
    chk("(c) V143_TERMOPINV != V143_TERMOP en la fisica (s 39913, T 5000)", fis(ri) != fis(R[(39913, 5000)]))
    tt = CT.tm_suma([dict(tel_termo=[d['carro'].get('termo') for d in R[(39913, 5000)]['linajes']])])
    ti = CT.tm_suma([dict(tel_termo=[d['carro'].get('termo') for d in ri['linajes']])])
    print(f"       telemetria termop {tt} · termopinv {ti}")
    chk("(c) la pieza ACTUA en TERMOP y en TERMOPINV (V4: a_no + a_si > 0)", CT.pieza(tt) and CT.pieza(ti))
    chk("(c) determinismo: V143_TERMOP dos corridas iguales (s 39913, T 5000)", run(TM, 39913, 5000) == R[(39913, 5000)])
    c = object.__new__(TM.Carro); c._tmM = {}; c._tmL = 0.05; ref = None; okm = True
    for x in [(0.8, 0.0)] * 20 + [(-0.4, 0.0)] * 30:
        c._tm_dS('A', x); ref = [x[0], x[1], 1] if ref is None else [ref[0] + 0.05 * (x[0] - ref[0]), ref[1] + 0.05 * (x[1] - ref[1]), 1]
        okm &= c._tmM['A'] == ref
    chk(f"(c) la memoria de TERMO' se DESDICE: tras 20 x (+0.8) y 30 x (-0.4) vale {c._tmM['A'][0]:.3f} < 0 (media movil, ema_c 0.05 de "
        f"FABRICA); la de TERMO seguiria en {(20 * 0.8 - 30 * 0.4) / 50:+.3f}", okm and c._tmM['A'][0] < 0)
'''
    i = i[:ini] + NUEVO + i[fin:]
    i = i.replace("valida: rechaza semillas del exploratorio 39001", "valida: rechaza semillas del exploratorio de TERMO 39001")
    i = i.replace("['v143', 'termo', 'o1']", "['v143', 'termop', 'o1']").replace("['termo']", "['termop']")
    for a, b in SEM:
        i = i.replace(a, b)
    CABI = ('"""identidad_termop.py = experimentos/organelos/termo/identidad_termo.py (95249ad33bbde643) para TERMO\' (carrera). GENERADO por '
            'construye_carrera_termop.py. NO editar a mano. Salida -> identidad_termop_salida.txt."""\n')
    out['identidad_termop.py'] = CABI + i
    return out


if __name__ == '__main__':
    ver = '--verifica' in sys.argv
    if [a for a in sys.argv[1:] if a != '--verifica']: raise SystemExit('*** uso: construye_carrera_termop.py [--verifica]')
    h = lambda p: h16b(open(p, 'rb').read())
    sc = dict(construye=h(os.path.join(AQUI, 'construye_termop.py')), V143_TERMOP=h(os.path.join(AQUI, 'carros', 'V143_TERMOP.py')),
              V143_TERMOPINV=h(os.path.join(AQUI, 'carros', 'V143_TERMOPINV.py')))
    malo = 0
    for n, t in construye(sc).items():
        p = os.path.join(AQUI, n); b = t.encode('utf-8')
        if ver:
            ok = os.path.exists(p) and open(p, 'rb').read() == b; malo += not ok
            print(f"{'OK  ' if ok else 'DIFIERE'} {n:22s} {h16b(b)}")
        else:
            open(p, 'wb').write(b); print(f'escrito {n:22s} {h16b(b)}')
    sys.exit(1 if malo else 0)
