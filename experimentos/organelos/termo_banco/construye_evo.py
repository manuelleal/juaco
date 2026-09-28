"""construye_evo.py — construye POR ANCLAS los carros del bloque TERMO_EVO (nube, 28-sep-2026).

MISION: llegar a la AGI por este camino (organismo minimo con reglas locales, sin retropropagacion, peldanos preregistrados con
controles y replicas). Preregistro: PREREGISTRO_termo_evo.md. Encargo: ENCARGO_NUBE.md.

PREGUNTA: si el margen del termostato de boca (boca_buena/INFORME.md, termo/) deja de ser una constante de diseno y pasa a ser un GEN
heredable con mutacion, la seleccion lo lleva sola a la banda que funciona?

PIEZA (una sola, en la BOCA; la del brazo m40 de boca_buena con el margen como gen):
  Sobre una letra k cuyo dS SENTIDO por el linaje (s = _adS de APR, ya en v14.3) NO tiene componentes negativas y tiene alguna positiva,
  la decision de morder la toma la pieza (manda sobre la boca de fabrica, el FILTRO y la opcion APR de v14.3 para ESAS letras):
      muerde  <=>  existe j con s_j > 0 y nivel_j < rep_umbral + g
  g es un valor POR CUERPO (el gen). Lo desconocido y lo malo sentido: v14.3 tal cual.
GEN g (unica memoria nueva: un float por cuerpo):
  fundador (crea(ctx): primer cuerpo del linaje y cada refundacion de ENMIENDA 5): g ~ U[G_INI].
  EVO = 1 (hereda): al_parir devuelve {'g': clip(g_padre + N(0, SIGMA), G_CLIP)}; la pista lo guarda OPACO en la cola (con la dote) y se
      lo entrega al hijo en nace(info['memoria']). V143 no usa esa memoria (su al_parir devolvia None), asi que la unica herencia nueva es g.
  EVO = 2 (SINHER, CONTROL): misma fisica, pero el hijo NO hereda: en nace sortea g de nuevo de U[G_INI]. No hay seleccion acumulable.
  rng del gen: ctx['rng'].spawn(1)[0] (el rng del CUERPO que la pista le da al carro; spawn NO avanza su estado: se verifica en el arnes).
  Todos los sorteos de g salen de ahi; ni el rng del mundo ni el del cuerpo ni rng_hijo se tocan.
PERILLAS (una linea): EVO 0 = V143 bit a bit (salida ENTERA) · 1 = hereda · 2 = SINHER; G_INI = (lo, hi); SIGMA; G_CLIP = (-0.2, 1.0).
Telemetria de SOLO LECTURA: d['carro']['evo'] (ultima instancia; ERR-96: el juez no la lee) y el dict de modulo _TEL[indice] que el
runner BORRA antes de cada pista.run y LEE despues (las instancias de una refundacion no se ven entre si; ningun carro lee _TEL).

ORIGEN (solo se LEE; sha16 fijado; cada ancla EXACTAMENTE una vez o aborta):
  experimentos/tronco_v14_3/carros_v143/V143.py (SHA_V143 = 2a03048a7f1525e5)
Genera en termo_evo/carros/ (difieren SOLO en la linea de perillas y el nombre; se verifica):
  V143_EVO_BAJO    EVO 1, G_INI (-0.10, 0.10), SIGMA 0.03   brazo PRINCIPAL (arranca en la zona letal)
  V143_EVO_ANCHO   EVO 1, G_INI (-0.10, 0.60), SIGMA 0.03   brazo secundario
  V143_EVO_SINHER  EVO 2, G_INI (-0.10, 0.10), SIGMA 0.03   CONTROL sin herencia (la distribucion del principal)
  V143_EVO_M40     EVO 1, G_INI ( 0.40, 0.40), SIGMA 0.0    techo DISENADO (== HIBB m40 en la fisica; arnes)

    python experimentos/organelos/termo_evo/construye_evo.py [--verifica]
"""
import argparse, hashlib, os, sys

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(AQUI)))
ORIGEN = os.path.join(RAIZ, 'experimentos', 'tronco_v14_3', 'carros_v143', 'V143.py')
SALIDA = os.path.join(AQUI, 'carros')
SHA_V143 = '2a03048a7f1525e5'
NL = '\r\n'   # el origen tiene fin de linea CRLF; se conserva

VARIANTES = [('V143_EVO_BAJO', 1, (-0.10, 0.10), 0.03), ('V143_EVO_ANCHO', 1, (-0.10, 0.60), 0.03),
             ('V143_EVO_SINHER', 2, (-0.10, 0.10), 0.03), ('V143_EVO_M40', 1, (0.40, 0.40), 0.0)]
PERILLAS = ("EVO = {e}; G_INI = ({lo}, {hi}); SIGMA = {s}; G_CLIP = (-0.2, 1.0)   "
            "# termo_evo: LA UNICA LINEA QUE CAMBIA ENTRE VARIANTES (EVO 0 = V143 bit a bit; 1 = hereda; 2 = SINHER)")

METODOS = '''
    # ================================================================ termo_evo: TERMOSTATO de boca con el margen como GEN g por cuerpo
    # Lee lo SENTIDO por el linaje (_adS), el estado presente (E, Ag) y el gen g del cuerpo. El gen usa SU rng (spawn del rng del
    # cuerpo, que no avanza). Telemetria: _TEL[indice] (solo escritura; la lee el runner) y d['carro']['evo'].
    def _ev_init(self, ctx):
        if not EVO: return
        self._tmU = float(ctx['rep_umbral'])
        self._tm = dict(dec=0, a_no=0, a_si=0, mord=0)
        self._ind = int(ctx['indice'])
        self._grng = ctx['rng'].spawn(1)[0]
        self._g = self._ev_sortea(); self._gorig = 0; self._gt0 = None
        tel = _TEL.setdefault(self._ind, dict(inst=0, cuerpos=0, partos=[], nacidos=[], vivos=[], muertes=[], muertes_fuera=0, gbin={}))
        tel['inst'] += 1

    def _ev_sortea(self):
        return float(self._grng.uniform(G_INI[0], G_INI[1]))

    def _ev_tel(self):
        return _TEL.setdefault(self._ind, dict(inst=0, cuerpos=0, partos=[], nacidos=[], vivos=[], muertes=[], muertes_fuera=0, gbin={}))

    def _ev_paso(self, t):
        if self._gt0 is None: self._gt0 = int(t); self._ev_tel()['cuerpos'] += 1   # fundador: su primer paso
        if t % 1000 == 0: self._ev_tel()['vivos'].append([int(t), round(self._g, 5)])

    def _ev_parir(self, info):
        self._ev_tel()['partos'].append([int(info['t']), round(self._g, 5)])
        gh = self._g + float(self._grng.normal(0.0, SIGMA))
        return dict(g=float(min(max(gh, G_CLIP[0]), G_CLIP[1])))

    def _ev_nace(self, info):
        m = info.get('memoria')
        if EVO == 1 and m is not None: self._g = float(m['g'])
        else: self._g = self._ev_sortea()
        self._gorig = 1; self._gt0 = int(info['t']); tel = self._ev_tel(); tel['cuerpos'] += 1
        if len(tel['nacidos']) < 3000: tel['nacidos'].append([int(info['t']), round(self._g, 5)])

    def _ev_muere(self, info):
        tel = self._ev_tel(); h = int(info['hijos']); e = int(info['edad'])
        if len(tel['muertes']) < 3000: tel['muertes'].append([int(info['t']), round(self._g, 5), e, h, self._gorig])
        else: tel['muertes_fuera'] += 1
        b = str(int((self._g + 0.2) // 0.05)); x = tel['gbin'].setdefault(b, [0, 0, 0]); x[0] += 1; x[1] += h; x[2] += e

    def _tm_boca(self, kk, E, Ag, mf):
        m = self._adS.get(kk)
        if m is None or m[2] <= 0: return mf                                   # desconocida: v14.3
        s = (m[0] / m[2], m[1] / m[2])
        if s[0] < 0 or s[1] < 0 or not (s[0] > 0 or s[1] > 0): return mf     # sentida mala (o nula): v14.3
        lev = (float(E), float(Ag)); S = self._tmU + self._g
        b = any(s[j] > 0 and lev[j] < S for j in (0, 1))
        g = self._tm; g['dec'] += 1; g['a_no'] += int(mf and not b); g['a_si'] += int(b and not mf); g['mord'] += int(b)
        return b

    def _ev_salida(self):
        return dict(evo=EVO, g_ini=list(G_INI), sigma=SIGMA, g_final=round(self._g, 5), **self._tm)
'''

ANCLAS = [
    ('"""V143.py — tronco_v14_3 (candidato a tronco v14.3): FABRICA + B-5 + FILTRO con META + boca TD de APR.' + NL,
     '"""{nombre}.py — termo_evo: V143 + termostato de boca con el margen como GEN heredable (ver construye_evo.py).' + NL
     + 'GENERADO por experimentos/organelos/termo_evo/construye_evo.py desde tronco_v14_3/carros_v143/V143.py (sha {sha}).' + NL
     + 'NO editar a mano. Perillas: {perillas_txt}. Con EVO = 0 es V143 bit a bit. Sigue el docstring de V143.' + NL + NL
     + 'V143.py — tronco_v14_3 (candidato a tronco v14.3): FABRICA + B-5 + FILTRO con META + boca TD de APR.' + NL),
    ('DESAMB = 1; FILTRO = 1; META = 1; INVIERTE = 0   # tronco_v14_3: LA UNICA LINEA QUE CAMBIA ENTRE VARIANTES (con OPCION)' + NL,
     'DESAMB = 1; FILTRO = 1; META = 1; INVIERTE = 0   # tronco_v14_3: LA UNICA LINEA QUE CAMBIA ENTRE VARIANTES (con OPCION)' + NL
     + '{perillas}' + NL
     + '_TEL = {}   # termo_evo: telemetria de SOLO ESCRITURA por linaje (indice); el runner la borra antes de cada run y la lee despues' + NL),
    ('        self._v3_init(ctx)' + NL,
     '        self._v3_init(ctx)' + NL + '        self._ev_init(ctx)   # termo_evo: gen g del fundador (rng propio: spawn del rng del cuerpo)' + NL),
    ('            if FILTRO and mordio and not self._v3m:' + NL,
     '            if EVO: mordio = self._tm_boca(kk, E, Ag, mordio)   # termo_evo: manda sobre lo sentido bueno (despues de FILTRO y APR)' + NL
     + '            if FILTRO and mordio and not self._v3m:' + NL),
    ("        for _dx in info['olvido']: self._rech.pop(_dx, None)" + NL,
     "        if EVO: self._ev_paso(info['t'])   # termo_evo: telemetria (solo escritura)" + NL
     + "        for _dx in info['olvido']: self._rech.pop(_dx, None)" + NL),
    ('        self._nmu += 1' + NL,
     '        self._nmu += 1' + NL + '        if EVO: self._ev_muere(info)   # termo_evo: telemetria (g, edad, hijos del cuerpo que muere)' + NL),
    ("        return None   # hereda='nada': el hijo no se lleva memoria (la dote la pone la pista)" + NL,
     "        if EVO: return self._ev_parir(info)   # termo_evo: el hijo se lleva SOLO el gen g (mutado)" + NL
     + "        return None   # hereda='nada': el hijo no se lleva memoria (la dote la pone la pista)" + NL),
    ("        _rh = info['rng_hijo']" + NL,
     "        _rh = info['rng_hijo']" + NL + "        if EVO: self._ev_nace(info)   # termo_evo: g heredado (EVO 1) o sorteado de nuevo (EVO 2)" + NL),
    ("            **({'v143': self._v3_salida()} if (DESAMB or FILTRO) else {}))" + NL,
     "            **({'v143': self._v3_salida()} if (DESAMB or FILTRO) else {})," + NL
     + "            **({'evo': self._ev_salida()} if EVO else {}))   # termo_evo: telemetria (ERR-96: no puntua)" + NL
     + '{metodos}'),
]


def h16b(b): return hashlib.sha256(b).hexdigest()[:16]
def h16(p): return h16b(open(p, 'rb').read())


def construye(nombre, e, gi, s):
    src = open(ORIGEN, 'rb').read()
    if h16b(src) != SHA_V143: raise SystemExit(f"origen {ORIGEN} sha {h16b(src)} != {SHA_V143}")
    txt = src.decode('utf-8')
    per = PERILLAS.format(e=e, lo=gi[0], hi=gi[1], s=s)
    metodos = METODOS.replace('\n', NL)
    for a, rep in ANCLAS:
        n = txt.count(a)
        if n != 1: raise SystemExit(f"ancla {a[:70]!r} aparece {n} veces (se exige 1)")
        rep = (rep.replace('{nombre}', nombre).replace('{sha}', SHA_V143).replace('{perillas_txt}', per.split('   #')[0])
               .replace('{perillas}', per).replace('{metodos}', metodos))
        txt = txt.replace(a, rep)
    return txt.encode('utf-8')


def todas():
    return {n: construye(n, e, gi, s) for n, e, gi, s in VARIANTES}


def main(argv=None):
    ap = argparse.ArgumentParser(allow_abbrev=False)
    ap.add_argument('--verifica', action='store_true')
    a = ap.parse_args(argv)
    outs = todas()
    base = outs['V143_EVO_BAJO'].decode('utf-8').split(NL)
    for n, bts in outs.items():
        ls = bts.decode('utf-8').split(NL)
        dif = [i for i, (x, y) in enumerate(zip(base, ls)) if x != y]
        if len(ls) != len(base) or any(not ('EVO = ' in ls[i] or n in ls[i]) for i in dif):
            raise SystemExit(f"{n}: difiere de V143_EVO_BAJO en algo mas que perillas/nombre: lineas {dif[:6]}")
    ok = True
    os.makedirs(SALIDA, exist_ok=True)
    for n, bts in outs.items():
        ruta = os.path.join(SALIDA, n + '.py')
        if a.verifica:
            igual = os.path.exists(ruta) and open(ruta, 'rb').read() == bts; ok &= igual
            print(f"  {n} sha {h16b(bts)} == disco: {igual}")
        else:
            tmp = ruta + '.tmp'
            with open(tmp, 'wb') as fh: fh.write(bts)
            os.replace(tmp, ruta)
            print(f"  escrito {ruta} (sha {h16b(bts)})")
    print(f"origen V143.py sha {h16(ORIGEN)} (fijado {SHA_V143}) · construye_evo.py sha {h16(os.path.abspath(__file__))}")
    return 0 if ok else 1


if __name__ == '__main__':
    sys.exit(main())
