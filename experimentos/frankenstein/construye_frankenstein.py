"""construye_frankenstein.py — construye organismo_frankenstein.py POR ANCLAS (EXPLORATORIO, no es dato).

MISION: llegar a la AGI por este camino.

Origenes (solo se LEEN; shas fijados):
  carrera_escuderias/carros/FABRICA.py 2ebee3e99ea5a33a  -> el tronco en el mundo vivo (brazo REL de f9c, linaje v14.1)
  carrera_escuderias/carros/APR.py     4402aa5142065c72  -> organo 3 (constantes y metodos de la opcion, VERBATIM)
  frankenstein/organos_frank.py (este equipo)            -> los seis organos + B-5
Con todas las perillas en 0 el carro es FABRICA bit a bit (identidad_frankenstein.py).
Uso: python experimentos/frankenstein/construye_frankenstein.py   (sin argumentos)
"""
import hashlib, os, sys

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
CARROS = os.path.join(RAIZ, 'experimentos', 'carrera_escuderias', 'carros')
FAB = os.path.join(CARROS, 'FABRICA.py'); SHA_FAB = '2ebee3e99ea5a33a'
APR = os.path.join(CARROS, 'APR.py'); SHA_APR = '4402aa5142065c72'
ORG = os.path.join(AQUI, 'organos_frank.py')
DESTINO = os.path.join(AQUI, 'organismo_frankenstein.py')


def h16(p):
    return hashlib.sha256(open(p, 'rb').read()).hexdigest()[:16]


ANCLAS = [
    # (0) cabecera
    ('"""carros/FABRICA.py — EL CARRO DE FABRICA de la carrera de escuderias.\n',
     '"""organismo_frankenstein.py — EL FRANKENSTEIN de JUACO (EXPLORATORIO, no es dato). CONSTRUIDO por\n'
     'experimentos/frankenstein/construye_frankenstein.py desde carros/FABRICA.py (sha {SHA_FAB}) + carros/APR.py (sha {SHA_APR})\n'
     '+ organos_frank.py (sha {SHA_ORG}). NO editar a mano. Perillas: b5 + mapa, curiosidad, modelo, lenta, herencia, interruptor\n'
     '(crea(ctx) = TODO encendido; crea(ctx, {}) = FABRICA bit a bit). Lo que sigue es el docstring de FABRICA.\n\n'
     'carros/FABRICA.py — EL CARRO DE FABRICA de la carrera de escuderias.\n'),
    # (1) los organos, antes de la clase
    ('\n\nclass Carro:\n    def __init__(self, ctx):\n',
     '\n\n{ORGANOS}\n\nclass Carro(_Organos):\n    def __init__(self, ctx, perillas=None):\n        self.PK = _perillas(perillas)\n'),
    # (2) fin de __init__
    ("        self._R = 0.; self._Rp = 0.; self._hambre = 0.; self._enc = None\n",
     "        self._R = 0.; self._Rp = 0.; self._hambre = 0.; self._enc = None\n        self._fk_init(ctx)\n"),
    # (3) actua: modo del interruptor + MAPA
    ("        self._nm = _na\n        d, k, left = self._see(pos, objs, t, contar=True); pat = PAT[k]\n",
     "        self._nm = _na\n        if self._FK: self._fk_paso(E, Ag, _cue2)\n"
     "        d, k, left = self._see(pos, objs, t, contar=True)\n"
     "        if self.PK['mapa']: d, k, left = self._fk_mapa(pos, objs, t, (d, k, left))\n        pat = PAT[k]\n"),
    # (4) actua: moldeo de las patas hacia el blanco del mapa
    ("d2, _, _ = self._see(pos, objs, t); Rp = .2 if d2 < d else 0.\n",
     "d2 = (self._fk_d2(pos, objs, t) if self.PK['mapa'] else self._see(pos, objs, t)[0]); Rp = .2 if d2 < d else 0.\n"),
    # (5) actua: lectura (curiosidad, memoria lenta)
    ("            if _cue2: _wt = min(_wt, self._vnec(1 - _na, PAT[kk], kc))\n",
     "            if self._FK: _wt = self._fk_lee(kk, kc, _fa9, _wt, _na, E, Ag)\n"
     "            if _cue2: _wt = min(_wt, self._vnec(1 - _na, PAT[kk], kc))\n"),
    # (6) actua: boca (modelo de si, interruptor) con el MISMO uniforme
    ("            pb = 1 / (1 + np.exp(-Vb / .3)); mordio = bool(rng.random() < pb)\n",
     "            pb = 1 / (1 + np.exp(-Vb / .3)); _u9 = rng.random(); mordio = bool(_u9 < pb)\n"
     "            if self._FK: mordio = self._fk_boca(obs, kk, mordio, _u9, pb)\n"),
    # (7) resultado: lo SENTIDO
    ("        if not res['mordio']: return\n        PAT = self.PAT; ETA = self.ETA",
     "        if not res['mordio']: return\n        if self._FK: self._fk_dS(res['letra'], res['dS'])\n        PAT = self.PAT; ETA = self.ETA"),
    # (8) B-5 (v14.2): tambien divide con R == 0; la hija nace sin valor
    ("            if Wb[c] * R < 0 and abs(float(Wb[c])) > 0.2",
     "            if (Wb[c] * R < 0 or (self._B5 and R == 0)) and abs(float(Wb[c])) > 0.2"),
    ("                else:     Wn[_nm, j] = Wn[_nm, c]; Wp[_nm, j] = 0.; Wn[_nm, c] = 0.\n",
     "                elif R < 0: Wn[_nm, j] = Wn[_nm, c]; Wp[_nm, j] = 0.; Wn[_nm, c] = 0.\n"
     "                else:     Wp[_nm, j] = 0.; Wn[_nm, j] = 0.; self._fk_des += 1   # B-5: sin valor; la madre conserva el suyo\n"),
    # (9) fin_paso: repaso
    ("        self.Wl = np.clip(self.Wl + self.ETA * (1 + 2 * self._hambre) * (max(self._R, 0) + self._Rp) * self.el, 0, 1.5)\n",
     "        self.Wl = np.clip(self.Wl + self.ETA * (1 + 2 * self._hambre) * (max(self._R, 0) + self._Rp) * self.el, 0, 1.5)\n"
     "        if self._FK: self._fk_fin(info)\n"),
    # (10) muere
    ("        self._nmu += 1\n", "        self._nmu += 1\n        if self._FK: self._fk_muere(info)\n"),
    # (11) al_parir
    ("    def al_parir(self, info):\n        return None",
     "    def al_parir(self, info):\n        if self._FK: return self._fk_parir(info)\n        return None"),
    # (12) nace
    ("        _rh = info['rng_hijo']\n", "        _rh = info['rng_hijo']\n        if self._FK: self._fk_nace(info)\n"),
    ("        # EL NODO: exposiciones sin consecuencia por la VIA LENTA, relevancia viva (nodo_rel=1)\n",
     "        if self._FK: self._fk_nodo(info)\n        # EL NODO: exposiciones sin consecuencia por la VIA LENTA, relevancia viva (nodo_rel=1)\n"),
    # (13) salida
    ("            _rep_cuello=int(kw['rep_cuello']))\n",
     "            _rep_cuello=int(kw['rep_cuello']), **({'frank': self._fk_salida()} if (self._FK or self._fk_des) else {}))\n"),
    # (14) crea
    ("def crea(ctx):\n    return Carro(ctx)", "def crea(ctx, perillas=None):\n    return Carro(ctx, perillas)"),
]


def bloque(src, ini, fin):
    a = src.index(ini); b = src.index(fin, a)
    return src[a:b].rstrip('\n') + '\n'


def construye(escribe=True):
    if h16(FAB) != SHA_FAB: raise SystemExit(f"construye: FABRICA.py cambio ({h16(FAB)})")
    if h16(APR) != SHA_APR: raise SystemExit(f"construye: APR.py cambio ({h16(APR)})")
    fab = open(FAB, encoding='utf-8').read(); apr = open(APR, encoding='utf-8').read(); org = open(ORG, encoding='utf-8').read()
    ctes = bloque(apr, '# ================================================================ APR (camino A, aprende_barrer) -- constantes',
                  '\n\n\nclass Carro')
    mets = bloque(apr, '    # ================================================================ APR (camino A): LA OPCION APRENDIDA',
                  '    def salida(self):')
    org = org.replace('# <<APR_CONSTANTES>>\n', ctes).replace('# <<APR_METODOS>>\n', mets)
    s = fab
    for a, b in ANCLAS:
        if s.count(a) != 1: raise SystemExit(f"construye: ancla no unica ({s.count(a)}): {a[:70]!r}")
        s = s.replace(a, b.replace('{SHA_FAB}', SHA_FAB).replace('{SHA_APR}', SHA_APR).replace('{SHA_ORG}', h16(ORG))
                      .replace('{ORGANOS}', org.rstrip('\n')))
    if escribe: open(DESTINO, 'w', encoding='utf-8', newline='\n').write(s)
    return s


if __name__ == '__main__':
    if len(sys.argv) > 1: raise SystemExit(f"construye_frankenstein: no admite argumentos ({sys.argv[1:]})")
    construye(); print('organismo_frankenstein.py', h16(DESTINO))
