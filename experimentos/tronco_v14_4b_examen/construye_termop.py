"""construye_termop.py -- CONSTRUCTOR POR ANCLAS de TERMO' (TERMO prima): la MISMA letra de TERMO con una memoria de lo sentido
que OLVIDA. MISION: llegar a la AGI por este camino (organismo minimo, reglas locales, sin retropropagacion, peldanos
preregistrados con controles y replicas).

POR QUE: TERMO guarda lo sentido como SUMA SIN OLVIDO (media de todas las mordidas del linaje). Tras una reversion, lo que fue bueno
sigue "sentido bueno" hasta que las mordidas nuevas pesan el doble que las viejas: TERMO no se desdice (examen v4 de v14.4,
PREREGISTRO_examen_v144.md sec. 5).
TERMO': la memoria de cada estimulo es una MEDIA MOVIL del dS sentido, a la tasa ema_c que el organismo YA tiene (0.05: la tasa de
sus medias condicionadas, hija dispersa D; en el carro, FABRICA kw['ema_c'] = 0.05). La primera mordida la inicializa con su dS:
  e <- dS                          (primera mordida)
  e <- e + ema_c * (dS - e)        (las siguientes)
y la letra lee s = e (se guarda [e_0, (e_1,) 1]: la MISMA funcion termo_letra / _tm_boca, con "mordidas" = 1 una vez conocido).
Constantes nuevas: CERO (ema_c es del tronco; U y 1/2 son los de TERMO). Memoria: la misma forma que la de TERMO (2 o 3 numeros por
estimulo). En un mundo QUIETO (el dS de cada estimulo no cambia: la pista, el mundo vivo sin inversion) e == dS EXACTO desde la
primera mordida (dS - e = 0.0), y TERMO' decide como TERMO salvo empates de coma flotante en el umbral (TERMO usa suma/n).
Tras invertir, e cruza 0 en ~22 mordidas (de +0.8 a -0.4: (0.95)^k < 1/3).

Construye (los origenes solo se LEEN; sha fijado; cada ancla exacta una vez):
  carros/V143_TERMOP.py   <- experimentos/organelos/termo/carros/V143_TERMO.py (3db639cab75641fb): memoria PROPIA _tmM (la _adS
                             de APR no se toca: APR la sigue usando), lineaje como _adS (no se borra al nacer)
  organismo_v144b.py      <- experimentos/tronco_v14_4_examen/organismo_v144.py    (e3768f6eab05b964)
  organismo_v144bg.py     <- experimentos/tronco_v14_4_examen/organismo_v144g.py   (1ea7fb43f41a69c5)
  organismo_v144bcal.py   <- experimentos/tronco_v14_4_examen/organismo_v144cal.py (a5a891e1d819e1bb)
En los organismos cambia UNA linea (la acumulacion de lo sentido) + el docstring. Con termo = 0 siguen siendo v14.3 bit a bit.

    python experimentos/tronco_v14_4b_examen/construye_termop.py [--verifica]
"""
import hashlib, os, sys

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
V144 = os.path.join(RAIZ, 'experimentos', 'tronco_v14_4_examen')
TERMO = os.path.join(RAIZ, 'experimentos', 'organelos', 'termo', 'carros')
ORIGENES = {os.path.join(TERMO, 'V143_TERMO.py'): '3db639cab75641fb',
            os.path.join(V144, 'organismo_v144.py'): 'e3768f6eab05b964',
            os.path.join(V144, 'organismo_v144g.py'): '1ea7fb43f41a69c5',
            os.path.join(V144, 'organismo_v144cal.py'): 'a5a891e1d819e1bb',
            os.path.join(TERMO, 'V143_TERMOINV.py'): 'da106a995b18bafd',
            os.path.join(V144, 'bateria_v144.py'): 'e928b202d9d66702',
            os.path.join(V144, 'bateria_generaliza_v144.py'): '3263ab8d8f45e7cd',
            os.path.join(V144, 'corre_examen_v144.py'): '8bb63d3f421040dd',
            os.path.join(V144, 'identidad_v144ex.py'): '6a714b193b6222dc'}


def h16b(b): return hashlib.sha256(b).hexdigest()[:16]
def h16(p): return h16b(open(p, 'rb').read())


def origen(p):
    b = open(p, 'rb').read()
    if h16b(b) != ORIGENES[p]: raise SystemExit(f'*** ORIGEN {p}: sha {h16b(b)} != {ORIGENES[p]}. No se escribe nada.')
    return b.decode('utf-8')


def sust(t, a, b, etq):
    n = t.count(a)
    if n != 1: raise SystemExit(f'*** ancla {etq!r} aparece {n} veces (se exige 1). No se escribe nada.')
    return t.replace(a, b)


NL = '\r\n'
CAB_CARRO = ('"""V143_TERMOP.py — TERMO\' (prima): V143_TERMO con la memoria de lo sentido que OLVIDA (media movil a la tasa ema_c de '
             'FABRICA). GENERADO por experimentos/tronco_v14_4b_examen/construye_termop.py desde termo/carros/V143_TERMO.py '
             '(sha 3db639cab75641fb). NO editar a mano. EXPLORATORIO hasta su preregistro."""' + NL)
UPD1 = ("                if termo: _m9=_adS.setdefault(kk,[0.0,0]); _m9[0]+=float(E_VAL[val[kk]]); _m9[1]+=1   "
        "# v14.4 TERMO: lo SENTIDO (dS nominal)\n")
NEW1 = ("                if termo: _m9=_adS.get(kk); _x9=float(E_VAL[val[kk]]); _adS[kk]=([_x9,1] if _m9 is None else [_m9[0]+ema_c*(_x9-_m9[0]),1])"
        "   # TERMO': lo SENTIDO con OLVIDO (media movil, tasa ema_c del tronco)\n")
UPD2 = ("                if termo: _m9=_adS.setdefault(kk,[0.0,0.0,0]); _m9[0]+=float(_dS[0]); _m9[1]+=float(_dS[1]); _m9[2]+=1   "
        "# v14.4 TERMO: lo SENTIDO (dS nominal)\n")
NEW2 = ("                if termo: _m9=_adS.get(kk); _x9=(float(_dS[0]),float(_dS[1])); _adS[kk]=([_x9[0],_x9[1],1] if _m9 is None else "
        "[_m9[0]+ema_c*(_x9[0]-_m9[0]),_m9[1]+ema_c*(_x9[1]-_m9[1]),1])   # TERMO': lo SENTIDO con OLVIDO (media movil, tasa ema_c del tronco)\n")
CAB_ORG = ('"""{n} = {o} con TERMO\' (prima): la MISMA letra de TERMO; la memoria de lo sentido es una MEDIA MOVIL a la tasa ema_c del '
           'tronco (0.05), inicializada por la primera mordida, y la letra la lee con mordidas = 1. Constantes nuevas: cero. Con termo=0 '
           'es v14.3 bit a bit. GENERADO por experimentos/tronco_v14_4b_examen/construye_termop.py (origen sha {s}). NO editar a mano."""\n')


def carro(nombre, fuente):
    c = origen(os.path.join(TERMO, fuente))
    c = sust(c, '"""' + fuente, CAB_CARRO.replace('V143_TERMOP', nombre[:-3]).replace('V143_TERMO.py (sha 3db639cab75641fb)', fuente + ' (sha ' + ORIGENES[os.path.join(TERMO, fuente)] + ')') + '"""' + fuente, 'carro: cabecera')
    per = 'TERMO = 1   # termo:' if fuente == 'V143_TERMO.py' else 'TERMO = 2   # termo:'
    c = sust(c, per, per.replace('# termo:', "# termo' (memoria con olvido):"), 'carro: perilla')
    c = sust(c, '        self._tm = dict(dec=0, a_no=0, a_si=0, mord=0)' + NL,
             '        self._tm = dict(dec=0, a_no=0, a_si=0, mord=0)' + NL
             + "        self._tmM = {}; self._tmL = float(self.EMA_C)   # TERMO': memoria PROPIA de lo sentido con olvido (tasa ema_c de FABRICA)" + NL,
             'carro: init')
    c = sust(c, '        m = self._adS.get(kk)' + NL + '        if m is None or m[2] <= 0: return mf',
             '        m = self._tmM.get(kk)   # TERMO\': lee SU memoria con olvido (no la _adS de APR)' + NL + '        if m is None or m[2] <= 0: return mf',
             'carro: lectura')
    c = sust(c, "        if OPCION and res['mordio']: self._apr_dS(res['letra'], res['dS'])" + NL,
             "        if OPCION and res['mordio']: self._apr_dS(res['letra'], res['dS'])" + NL
             + "        if TERMO and res['mordio']: self._tm_dS(res['letra'], res['dS'])   # TERMO': lo sentido, con olvido" + NL,
             'carro: acumula')
    c = sust(c, '    def _tm_salida(self):' + NL,
             '    def _tm_dS(self, k, dS):   # TERMO\': e <- dS (primera); e <- e + ema_c (dS - e); "mordidas" = 1' + NL
             + '        m = self._tmM.get(k); x = (float(dS[0]), float(dS[1]))' + NL
             + '        self._tmM[k] = [x[0], x[1], 1] if m is None else [m[0] + self._tmL * (x[0] - m[0]), m[1] + self._tmL * (x[1] - m[1]), 1]' + NL + NL
             + '    def _tm_salida(self):' + NL, 'carro: metodo')
    return c


CAB_BAT = ('"""bateria_v144b = experimentos/tronco_v14_4_examen/bateria_v144.py (e928b202d9d66702) apuntando a organismo_v144b (TERMOP = '
           'TERMO con memoria que olvida). Etapas, CRIT, umbrales y la identidad interna con termo=0: intactos. GENERADO por '
           'experimentos/tronco_v14_4b_examen/construye_termop.py. NO editar a mano."""' + chr(10))
CAB_GEN = ('"""bateria_generaliza_v144b = experimentos/tronco_v14_4_examen/bateria_generaliza_v144.py (3263ab8d8f45e7cd) + UNA entrada: '
           'organismo_v144b -> organismo_v144bg, kwargs CAMPO A CAMPO iguales a los de organismo_v143/v144 (regla 14). GENERADO por '
           'experimentos/tronco_v14_4b_examen/construye_termop.py. NO editar a mano."""' + chr(10))
LF = chr(10)


def construye():
    out = {os.path.join('carros', 'V143_TERMOP.py'): carro('V143_TERMOP.py', 'V143_TERMO.py'),
           os.path.join('carros', 'V143_TERMOPINV.py'): carro('V143_TERMOPINV.py', 'V143_TERMOINV.py')}
    for n, o, upd, new in (('organismo_v144b.py', 'organismo_v144.py', UPD1, NEW1), ('organismo_v144bg.py', 'organismo_v144g.py', UPD1, NEW1),
                           ('organismo_v144bcal.py', 'organismo_v144cal.py', UPD2, NEW2)):
        p = os.path.join(V144, o)
        t = sust(origen(p), upd, new, f'{n}: acumulacion')
        out[n] = CAB_ORG.format(n=n[:-3], o=o[:-3], s=ORIGENES[p]) + t
    b = origen(os.path.join(V144, 'bateria_v144.py'))
    for a_, b_, n_ in (("import organismo_v144 as v13   # v14.4 = v14.3 + TERMO (termo=1 por defecto)",
                        "import organismo_v144b as v13   # v14.4b = v14.3 + TERMOP (termo=1 por defecto)", 2),
                       ("'organismo_v144.py'", "'organismo_v144b.py'", 2), ("f'examen_v144_{stamp}", "f'examen_v144b_{stamp}", 2)):
        if b.count(a_) != n_: raise SystemExit(f'*** bateria_v144: ancla {a_!r} aparece {b.count(a_)} veces (se exigen {n_})')
        b = b.replace(a_, b_)
    out['bateria_v144b.py'] = CAB_BAT + b
    g = origen(os.path.join(V144, 'bateria_generaliza_v144.py'))
    lin = [l for l in g.split(LF) if l.startswith("    'organismo_v144': ('organismo_v144g', dict(")]
    if len(lin) != 1: raise SystemExit('*** bateria_generaliza_v144: entrada organismo_v144 no unica')
    nueva = (lin[0].replace("'organismo_v144': ('organismo_v144g',", "'organismo_v144b': ('organismo_v144bg',").split('   #')[0]
             + "   # v14.4b = v14.3 + TERMOP (termo=1 por defecto en organismo_v144bg): kwargs CAMPO A CAMPO iguales (regla 14)")
    g = sust(g, lin[0] + LF, lin[0] + LF + nueva + LF, 'gen: INSTRUMENTOS')
    g = sust(g, "'organismo_v144g': AQUI,", "'organismo_v144g': AQUI, 'organismo_v144bg': AQUI,", 'gen: _dir')
    out['bateria_generaliza_v144b.py'] = CAB_GEN + g
    return out


if __name__ == '__main__':
    ver = '--verifica' in sys.argv
    if [a for a in sys.argv[1:] if a != '--verifica']: raise SystemExit('*** uso: construye_termop.py [--verifica]')
    malo = 0
    os.makedirs(os.path.join(AQUI, 'carros'), exist_ok=True)
    for n, t in construye().items():
        p = os.path.join(AQUI, n); b = t.encode('utf-8')
        if ver:
            ok = os.path.exists(p) and open(p, 'rb').read() == b; malo += not ok
            print(f"{'OK  ' if ok else 'DIFIERE'} {n:28s} {h16b(b)}")
        else:
            open(p, 'wb').write(b); print(f'escrito {n:28s} {h16(p)}')
    sys.exit(1 if malo else 0)
