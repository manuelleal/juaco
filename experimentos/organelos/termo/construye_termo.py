"""construye_termo.py — construye POR ANCLAS los carros del bloque TERMO (ultimo intento del muro de la carrera, 28-sep-2026).

MISION: llegar a la AGI por este camino (organismo minimo con reglas locales, sin retropropagacion, peldanos preregistrados con
controles y replicas). Preregistro: PREREGISTRO_termo.md.

PIEZA TERMO (una sola, en la BOCA; sale del diagnostico experimentos/organelos/boca_buena/, EXPLORATORIO 39001-39010):
  "termostato de dos necesidades". Sobre una letra k cuyo dS SENTIDO por el linaje (s = _adS de APR, ya en v14.3: media del dS que
  la pista devuelve al morder) NO tiene componentes negativas y tiene alguna positiva, la decision de morder la toma la pieza (manda
  sobre la boca de fabrica, el FILTRO y la opcion APR de v14.3 para ESAS letras):
      muerde  <=>  existe j con s_j > 0 y nivel_j < rep_umbral + s_j / 2
  ("come si alguna necesidad que la letra sube esta por debajo del umbral de parto mas media mordida"). Lo desconocido y lo malo
  sentido: v14.3 tal cual. Cero memoria nueva (_adS y rep_umbral ya estan; nivel = E, Ag presentes). Sin rng: usa la decision ya
  sorteada solo como valor por defecto. La constante 1/2 es PROPIA y sale del exploratorio (declarada en el preregistro).
  CONTROL TERMOINV (TERMO = 2): la misma regla leyendo el nivel de la necesidad que la letra NO sube (lev[1 - j]).
PERILLA TERMO (una linea nueva de modulo): 0 = V143 bit a bit (salida ENTERA) · 1 = TERMO (candidato) · 2 = TERMOINV (control).
Telemetria de SOLO LECTURA en d['carro']['termo'] (solo si TERMO != 0; el juez no la lee, ERR-96).

ORIGEN (solo se LEE; sha16 fijado; cada ancla EXACTAMENTE una vez o aborta):
  experimentos/tronco_v14_3/carros_v143/V143.py (SHA_V143 = 2a03048a7f1525e5)
Genera en termo/carros/: V143_TERMO (TERMO 1) · V143_TERMOINV (TERMO 2). Difieren SOLO en la linea de perillas y el nombre (se verifica).

    python experimentos/organelos/termo/construye_termo.py [--verifica]
"""
import argparse, hashlib, os, sys

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(AQUI)))
ORIGEN = os.path.join(RAIZ, 'experimentos', 'tronco_v14_3', 'carros_v143', 'V143.py')
SALIDA = os.path.join(AQUI, 'carros')
SHA_V143 = '2a03048a7f1525e5'
NL = '\r\n'   # el origen tiene fin de linea CRLF; se conserva

VARIANTES = [('V143_TERMO', 1), ('V143_TERMOINV', 2)]
PERILLAS = "TERMO = {t}   # termo: LA UNICA LINEA QUE CAMBIA ENTRE VARIANTES (0 = V143 bit a bit; 1 = TERMO; 2 = TERMOINV)"

METODOS = '''
    # ================================================================ termo: TERMOSTATO de dos necesidades (una pieza de boca)
    # Lee lo SENTIDO por el linaje (_adS) y el estado presente (E, Ag). Solo letras sentidas sin dano y con algo bueno. Sin rng.
    def _tm_init(self, ctx):
        self._tmU = float(ctx['rep_umbral'])
        self._tm = dict(dec=0, a_no=0, a_si=0, mord=0)

    def _tm_boca(self, kk, E, Ag, mf):
        m = self._adS.get(kk)
        if m is None or m[2] <= 0: return mf                                   # desconocida: v14.3
        s = (m[0] / m[2], m[1] / m[2])
        if s[0] < 0 or s[1] < 0 or not (s[0] > 0 or s[1] > 0): return mf     # sentida mala (o nula): v14.3
        lev = (float(E), float(Ag))
        if TERMO == 1: b = any(s[j] > 0 and lev[j] < self._tmU + s[j] / 2 for j in (0, 1))
        else:          b = any(s[j] > 0 and lev[1 - j] < self._tmU + s[j] / 2 for j in (0, 1))   # CONTROL: la necesidad que NO sube
        g = self._tm; g['dec'] += 1; g['a_no'] += int(mf and not b); g['a_si'] += int(b and not mf); g['mord'] += int(b)
        return b

    def _tm_salida(self):
        return dict(termo=TERMO, **self._tm)
'''

ANCLAS = [
    ('"""V143.py — tronco_v14_3 (candidato a tronco v14.3): FABRICA + B-5 + FILTRO con META + boca TD de APR.' + NL,
     '"""{nombre}.py — termo: V143 + UNA pieza de boca (termostato de dos necesidades; ver construye_termo.py). Cero memoria nueva.' + NL
     + 'GENERADO por experimentos/organelos/termo/construye_termo.py desde tronco_v14_3/carros_v143/V143.py (sha {sha}).' + NL
     + 'NO editar a mano. Perillas: {perillas_txt}. Con TERMO = 0 es V143 bit a bit. Sigue el docstring de V143.' + NL + NL
     + 'V143.py — tronco_v14_3 (candidato a tronco v14.3): FABRICA + B-5 + FILTRO con META + boca TD de APR.' + NL),
    ('DESAMB = 1; FILTRO = 1; META = 1; INVIERTE = 0   # tronco_v14_3: LA UNICA LINEA QUE CAMBIA ENTRE VARIANTES (con OPCION)' + NL,
     'DESAMB = 1; FILTRO = 1; META = 1; INVIERTE = 0   # tronco_v14_3: LA UNICA LINEA QUE CAMBIA ENTRE VARIANTES (con OPCION)' + NL
     + '{perillas}' + NL),
    ('        self._v3_init(ctx)' + NL,
     '        self._v3_init(ctx)' + NL + '        self._tm_init(ctx)   # termo: solo contadores (sin rng)' + NL),
    ('            if FILTRO and mordio and not self._v3m:' + NL,
     '            if TERMO: mordio = self._tm_boca(kk, E, Ag, mordio)   # termo: manda sobre lo sentido bueno (despues de FILTRO y APR)' + NL
     + '            if FILTRO and mordio and not self._v3m:' + NL),
    ("            **({'v143': self._v3_salida()} if (DESAMB or FILTRO) else {}))" + NL,
     "            **({'v143': self._v3_salida()} if (DESAMB or FILTRO) else {})," + NL
     + "            **({'termo': self._tm_salida()} if TERMO else {}))   # termo: telemetria (ERR-96: no puntua)" + NL
     + '{metodos}'),
]


def h16b(b): return hashlib.sha256(b).hexdigest()[:16]
def h16(p): return h16b(open(p, 'rb').read())


def construye(nombre, t):
    src = open(ORIGEN, 'rb').read()
    if h16b(src) != SHA_V143: raise SystemExit(f"origen {ORIGEN} sha {h16b(src)} != {SHA_V143}")
    txt = src.decode('utf-8')
    per = PERILLAS.format(t=t)
    metodos = METODOS.replace('\n', NL)
    for a, rep in ANCLAS:
        n = txt.count(a)
        if n != 1: raise SystemExit(f"ancla {a[:70]!r} aparece {n} veces (se exige 1)")
        rep = (rep.replace('{nombre}', nombre).replace('{sha}', SHA_V143).replace('{perillas_txt}', per.split('   #')[0])
               .replace('{perillas}', per).replace('{metodos}', metodos))
        txt = txt.replace(a, rep)
    return txt.encode('utf-8')


def todas():
    return {n: construye(n, t) for n, t in VARIANTES}


def main(argv=None):
    ap = argparse.ArgumentParser(allow_abbrev=False)
    ap.add_argument('--verifica', action='store_true')
    a = ap.parse_args(argv)
    outs = todas()
    base = outs['V143_TERMO'].decode('utf-8').split(NL)
    for n, bts in outs.items():
        ls = bts.decode('utf-8').split(NL)
        dif = [i for i, (x, y) in enumerate(zip(base, ls)) if x != y]
        if len(ls) != len(base) or any(not ('TERMO = ' in ls[i] or n in ls[i]) for i in dif):
            raise SystemExit(f"{n}: difiere de V143_TERMO en algo mas que perillas/nombre: lineas {dif[:6]}")
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
    print(f"origen V143.py sha {h16(ORIGEN)} (fijado {SHA_V143}) · construye_termo.py sha {h16(os.path.abspath(__file__))}")
    return 0 if ok else 1


if __name__ == '__main__':
    sys.exit(main())
