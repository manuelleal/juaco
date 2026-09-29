"""construye_veto_muro.py — construye POR ANCLAS el carro CONFIRMATORIO TVPISO del bloque VETO_MURO (TERMO + PATAS + VETO POR RESERVAS).

MISION: llegar a la AGI por este camino (organismo minimo con reglas locales, sin retropropagacion, peldanos preregistrados con
controles y replicas).

DIAGNOSTICO (verificado por el creador sobre los JSON de TERMO 39101-39140, ver PREREGISTRO_veto_muro.md sec. 1): el hijo de TERMO muere
joven (13.1 % en <= 200 pasos contra 0.58 % de O1; vida mediana 1318 contra 3581; 47.5 % muere de veneno o sal) con solo ~62 mordidas B+D
por linaje (O1: 354). La boca de fabrica muerde lo malo CON HAMBRE (logit 1.2 w + 2 hambre + 0.5); O1 muerde lo malo solo si puede PAGAR
el golpe (O1._costeable: PISO 0.2 fuera de la ventana de parto, rep_umbral dentro). VETO 1 de dinamita (piso = rep_umbral SIEMPRE) tapo
el mundo (vu 4/90, mundo A+C 2.19); nunca se probo el piso intermedio de O1.

PIEZA VETO_PISO (una sola, en la BOCA; cero memoria nueva; sin rng; solo QUITA mordidas, nunca fuerza): sobre una letra k cuyo dS SENTIDO
por el linaje (s = _adS de TERMO, la misma lectura) tiene alguna componente NEGATIVA:
    piso = rep_umbral si min(E, Ag) >= rep_umbral (la ventana de parto corre)   ·   PISO_V = 0.2 si no
    VETOP 1 (PISO):    no muerde si existe j con s_j < 0 y nivel_j + s_j < piso        ("no me muerdo lo que no puedo pagar")
    VETOP 2 (PISOINV): CONTROL desfasado: la misma regla leyendo la necesidad que el golpe NO toca (nivel_{1-j} + s_j < piso)
Constante NUEVA declarada: PISO_V = 0.2 = dote / 3 (dote 0.6 de la pista) = el PISO de O1. Todo lo demas es de TERMO (rep_umbral, _adS).
Parecido con O1 (DECLARADO): es la clausula de piso de O1._costeable, sola. NO lleva 'el golpe cae en la necesidad MAS llena', ni 'nada util a
la vista', ni fuerza limpiezas (O1 si). Se aplica DESPUES de FILTRO, APR (opcion) y TERMO; la opcion APR aprende sobre SU decision (b), no
sobre la ejecutada (igual que VETO de dinamita; declarado).
PERILLA VETOP (una linea nueva): 0 = TPATAS bit a bit (salida ENTERA), con cualquier PATAS; y con PATAS = 0 y VETOP = 0 = V143_TERMO.
Telemetria de SOLO LECTURA en d['carro']['vpiso'] si VETOP != 0.

ORIGEN (solo se LEE; sha16 fijado; cada ancla EXACTAMENTE una vez o aborta):
  experimentos/organelos/dinamita/carros/TPATAS.py (SHA_TPATAS = 1b6272ef4616af8b; TPATAS = V143_TERMO + PATAS, por anclas)
Genera en veto_muro/carros/: TVPISO (una fuente; PATAS = 0 y VETOP = 0 en disco; el runner fija las perillas en memoria por worker).

    python experimentos/organelos/veto_muro/construye_veto_muro.py [--verifica]
"""
import argparse, hashlib, os, sys

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(AQUI)))
ORIGEN = os.path.join(RAIZ, 'experimentos', 'organelos', 'dinamita', 'carros', 'TPATAS.py')
SALIDA = os.path.join(AQUI, 'carros')
SHA_TPATAS = '1b6272ef4616af8b'
NL = '\r\n'   # el origen tiene fin de linea CRLF; se conserva

VARIANTES = [('TVPISO', 0)]
PERILLAS = ("VETOP = {v}   # veto_muro: LA UNICA LINEA QUE CAMBIA ENTRE VARIANTES (0 = TPATAS bit a bit; 1 PISO; 2 PISOINV control)" + NL
            + "PISO_V = 0.2   # veto_muro: CONSTANTE NUEVA DECLARADA = dote / 3 (dote 0.6) = PISO de O1; solo se usa si VETOP != 0")

METODOS = '''
    # ================================================================ veto_muro: VETO POR RESERVAS (una pieza de boca; piso de O1)
    # Lee lo SENTIDO por el linaje (_adS, el mismo de TERMO) y el estado presente (E, Ag). Solo QUITA mordidas de lo sentido malo. Sin rng.
    def _vp_init(self, ctx):
        self._vpU = float(ctx['rep_umbral'])
        self._vp = dict(dec=0, a_no=0, a_no_vent=0)

    def _vp_boca(self, kk, E, Ag, mf):
        m = self._adS.get(kk)
        if m is None or m[2] <= 0: return mf                                   # desconocida: TERMO / v14.3
        s = (m[0] / m[2], m[1] / m[2])
        if not (s[0] < 0 or s[1] < 0): return mf                               # no es sentida mala: TERMO / v14.3
        lev = (float(E), float(Ag)); U = self._vpU
        vent = min(lev) >= U                                                   # la ventana de parto corre
        piso = U if vent else PISO_V
        if VETOP == 1: no = any(s[j] < 0 and lev[j] + s[j] < piso for j in (0, 1))
        elif VETOP == 2: no = any(s[j] < 0 and lev[1 - j] + s[j] < piso for j in (0, 1))   # CONTROL: la necesidad que el golpe NO toca
        else: raise SystemExit(f"VETOP invalido {VETOP!r}")
        q = int(bool(mf) and no)
        g = self._vp; g['dec'] += 1; g['a_no'] += q; g['a_no_vent'] += q * int(vent)
        return bool(mf and not no)

    def _vp_salida(self):
        return dict(vetop=VETOP, piso_v=PISO_V, **self._vp)
'''

ANCLAS = [
    ('"""TPATAS.py — dinamita (EXPLORATORIO): V143_TERMO + UNA pieza de PATAS (ver construye_patas.py).' + NL,
     '"""{nombre}.py — veto_muro (CONFIRMATORIO): TPATAS + UNA pieza de boca (VETO POR RESERVAS, piso de O1; ver construye_veto_muro.py).' + NL
     + 'GENERADO por experimentos/organelos/veto_muro/construye_veto_muro.py desde dinamita/carros/TPATAS.py (sha {sha}).' + NL
     + 'NO editar a mano. Perillas: {perillas_txt}. Con VETOP = 0 es TPATAS bit a bit. Sigue el docstring de TPATAS.' + NL + NL
     + 'TPATAS.py — dinamita (EXPLORATORIO): V143_TERMO + UNA pieza de PATAS (ver construye_patas.py).' + NL),
    ('PATAS = 0   # dinamita-patas: LA UNICA LINEA QUE CAMBIA ENTRE VARIANTES (0 = V143_TERMO bit a bit; 1 DIRECTO; 2 UTIL; 3 UTIL+CEDE; 4 INUTIL control)' + NL,
     'PATAS = 0   # dinamita-patas: LA UNICA LINEA QUE CAMBIA ENTRE VARIANTES (0 = V143_TERMO bit a bit; 1 DIRECTO; 2 UTIL; 3 UTIL+CEDE; 4 INUTIL control)' + NL
     + '{perillas}' + NL),
    ('        self._pt_init(ctx)   # dinamita-patas: solo contadores (sin rng)' + NL,
     '        self._pt_init(ctx)   # dinamita-patas: solo contadores (sin rng)' + NL
     + '        self._vp_init(ctx)   # veto_muro: solo contadores (sin rng)' + NL),
    ('            if TERMO: mordio = self._tm_boca(kk, E, Ag, mordio)   # termo: manda sobre lo sentido bueno (despues de FILTRO y APR)' + NL,
     '            if TERMO: mordio = self._tm_boca(kk, E, Ag, mordio)   # termo: manda sobre lo sentido bueno (despues de FILTRO y APR)' + NL
     + '            if VETOP: mordio = self._vp_boca(kk, E, Ag, mordio)   # veto_muro: solo QUITA mordidas de lo sentido malo (piso de O1)' + NL),
    ("            **({'patas': self._pt_salida()} if PATAS else {}))   # dinamita-patas: telemetria (ERR-96: no puntua)" + NL,
     "            **({'patas': self._pt_salida()} if PATAS else {})," + NL
     + "            **({'vpiso': self._vp_salida()} if VETOP else {}))   # veto_muro: telemetria (ERR-96: no puntua)" + NL),
    ('    def _pt_salida(self):' + NL + '        return dict(patas=PATAS, **self._pt)' + NL,
     '    def _pt_salida(self):' + NL + '        return dict(patas=PATAS, **self._pt)' + NL + '{metodos}'),
]


def h16b(b): return hashlib.sha256(b).hexdigest()[:16]
def h16(p): return h16b(open(p, 'rb').read())


def construye(nombre, v):
    src = open(ORIGEN, 'rb').read()
    if h16b(src) != SHA_TPATAS: raise SystemExit(f"origen {ORIGEN} sha {h16b(src)} != {SHA_TPATAS}")
    txt = src.decode('utf-8')
    per = PERILLAS.format(v=v)
    metodos = METODOS.replace('\n', NL)
    for a, rep in ANCLAS:
        n = txt.count(a)
        if n != 1: raise SystemExit(f"ancla {a[:70]!r} aparece {n} veces (se exige 1)")
        rep = (rep.replace('{nombre}', nombre).replace('{sha}', SHA_TPATAS).replace('{perillas_txt}', f"VETOP = {v}, PATAS = 0")
               .replace('{perillas}', per).replace('{metodos}', metodos))
        txt = txt.replace(a, rep)
    return txt.encode('utf-8')


def todas():
    return {n: construye(n, v) for n, v in VARIANTES}


def main(argv=None):
    ap = argparse.ArgumentParser(allow_abbrev=False)
    ap.add_argument('--verifica', action='store_true')
    a = ap.parse_args(argv)
    outs = todas(); ok = True
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
    print(f"origen TPATAS.py sha {h16(ORIGEN)} (fijado {SHA_TPATAS}) · construye_veto_muro.py sha {h16(os.path.abspath(__file__))}")
    return 0 if ok else 1


if __name__ == '__main__':
    sys.exit(main())
