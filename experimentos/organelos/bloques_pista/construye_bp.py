"""construye_bp.py — construye POR ANCLAS los carros de BLOQUES_PISTA (28-sep-2026, creador; EXPLORATORIO).

MISION: llegar a la AGI por este camino (organismo minimo con reglas locales, sin retropropagacion, peldanos preregistrados con
controles y replicas). Principio del director: que la evolucion construya el organo, no nosotros, y solo con seleccion natural.

ORIGEN (solo se LEE; sha16 fijado; cada ancla EXACTAMENTE una vez o aborta):
  experimentos/organelos/termo/carros/V143_TERMO.py (SHA_TERMO = 3db639cab75641fb). Fin de linea CRLF (el del origen).
PORT (por lectura, no por import) del genoma de reglas de experimentos/organelos/bloques/opusM/motor_bloques.py (_sentido, _cumple,
_reglas_mov, _reglas_boca, _regla_azar, _muta_reglas) a la INTERFAZ DE CARRO de la pista:
  Regla = (sentido, parametro j, comparador, umbral th, accion, peso w in [-3, 3]); hasta NRMAX = 12.
  Sentidos (lo que el carro de la pista REALMENTE ve; obs = t, pos, E, Ag, objs):
    0 hambre (1-E), 1 sed (1-Ag), 2 cercania de lo que mira (1 - min(d,10)/10; al morder d = 0),
    3 pixel j de la letra en foco (lo que mira al moverse; lo que tiene en la celda al morder),
    4 pixel j de la ultima letra mordida por ESTE cuerpo, 5 R de la ultima mordida ((R+3)/4),
    6 NUEVO (pedido del coordinador 21:05, sonda termo_organo): "que hay alrededor" = cercania del objeto MAS CERCANO del anillo
      cuyo pixel j es 1 (1 - min(d,20)/20; 0 si no hay). No usa el significado de las letras: lee la retina de lo que hay.
  Acciones: 0 boca (Vb += w), 1 patas hacia lo que mira (w > 0) / alejarse (w < 0), 2 quedarse (V[0], V[1] -= w).
  NO portado: la accion 3 (parir) de opusM (el parto lo decide la pista; declarado). NO portada la HGT entre linajes (seria un canal
  entre carros fuera del reglamento de la pista): p_hgt = 0.
  Operadores (los de opusM sin HGT): mutar un campo (p_campo por regla), DUPLICAR (p_dup), BORRAR (p_del), INSERTAR al azar (p_ins).
  HERENCIA (DONANTE 'padre', brazo bloq): al parir, el hijo lleva las reglas del padre mutadas (memoria opaca de la cola); el padre
  entra al BANCO DEL LINAJE (solo entra quien pare). El REFUNDADOR (crea(ctx), ENMIENDA 5) toma una entrada al azar del banco de SU
  linaje, mutada; si el banco esta vacio, INICIAL reglas al azar.
  SIN HERENCIA (DONANTE 'azar', brazo bloqaza): todo cuerpo nuevo (hijo o refundador) sale de una entrada al azar del banco del linaje
  mutada, y el banco guarda las listas NUEVAS (el genoma nunca influye en su propia copia): el diseno de BLOQ_AZA de opusM.
  rng: ctx['rng'] (el rng del carro que da la pista; revisa_carro prohibe rng propio). Sin sorteos si las tasas son 0 e INICIAL 0
  (y una lista vacia no entra al banco): asi el genoma vacio con tasas 0 es V143_TERMO bit a bit. Con tasas > 0 la genetica
  consume el MISMO rng del carro (cambia su azar de conducta: declarado).
  Memoria nueva: la lista de reglas (<= 12 x 6 floats) + ultima letra mordida y su R (2 numeros) por cuerpo; banco <= BQ_C['banco'].
PERILLA BLOQ (una linea): 0 = V143_TERMO bit a bit. Con BLOQ = 1, genoma vacio (INICIAL 0) y tasas 0 tambien == V143_TERMO (arnes).
Telemetria de SOLO ESCRITURA en el modulo (_BQ_TEL): el runner la lee al terminar el run; ningun carro la lee (ERR-96).

Genera en bloques_pista/carros/: V143_BQ (BLOQ 1, padre) · V143_BQAZA (BLOQ 1, azar) · V143_BQ0 (BLOQ 0, solo arnes).

    python experimentos/organelos/bloques_pista/construye_bp.py [--verifica]
"""
import argparse, hashlib, os, sys

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(AQUI)))
ORIGEN = os.path.join(RAIZ, 'experimentos', 'organelos', 'termo', 'carros', 'V143_TERMO.py')
SALIDA = os.path.join(AQUI, 'carros')
SHA_TERMO = '3db639cab75641fb'
NL = '\r\n'
VARIANTES = [('V143_BQ', 1, 'padre'), ('V143_BQAZA', 1, 'azar'), ('V143_BQ0', 0, 'padre')]
PER = "BLOQ = {b}; DONANTE = '{d}'   # bloques_pista: LA UNICA LINEA QUE CAMBIA ENTRE VARIANTES (BLOQ 0 = V143_TERMO bit a bit)"

MODULO = ("BQ_SEMILLA = 0; BQ_C = dict(inicial=2, p_campo=0.10, p_dup=0.02, p_del=0.07, p_ins=0.05, banco=50)   # bloques_pista: los fija el RUNNER" + NL
          + "BQ_FORZADA = None   # bloques_pista: SOLO ARNES (lista de reglas fija para todo cuerpo nuevo; None = genetica normal)" + NL
          + "NRMAX = 12; NSEN = 7; NACC = 3" + NL
          + "_BQ_BANCO = {}; _BQ_CNT = {}; _BQ_TEL = {}   # bloques_pista: por linaje (indice); el runner los BORRA antes de cada run" + NL)

METODOS = '''
    # ================================================================ bloques_pista: GENOMA DE REGLAS (port de bloques/opusM/motor_bloques)
    def _bq_init(self, ctx):
        i = int(ctx['indice']); c = _BQ_CNT.get(i, 0); _BQ_CNT[i] = c + 1; self._bqi = i
        self._bqrng = ctx['rng']   # el rng PROPIO del carro que da la pista (regla de revisa_carro: nada de rng propio)
        self._bqlk = None; self._bqlr = 0.0; self._bqcache = None
        B = _BQ_BANCO.setdefault(i, []); tel = _BQ_TEL.setdefault(i, dict(fund=[], muestras=[], partos=0, suelo=[]))
        if BQ_FORZADA is not None: self._bqR = [list(map(float, r)) for r in BQ_FORZADA]; de = -1
        elif B: self._bqR = self._bq_muta(B[int(self._bqrng.integers(len(B)))]); de = 1
        else: self._bqR = self._bq_muta([self._bq_azar() for _ in range(int(BQ_C['inicial']))]); de = 0
        if DONANTE == 'azar' and BQ_FORZADA is None: self._bq_banco(self._bqR)
        tel['fund'].append([c, de, len(self._bqR)])

    def _bq_azar(self):
        rr = self._bqrng
        return [float(rr.integers(0, NSEN)), float(rr.integers(0, 6)), float(rr.integers(0, 2)), float(rr.random()),
                float(rr.integers(0, NACC)), float(rr.uniform(-3.0, 3.0))]

    def _bq_muta(self, base):
        C = BQ_C; rr = self._bqrng; R = [list(map(float, x)) for x in base]
        for x in R:
            if C['p_campo'] > 0 and rr.random() < C['p_campo']:   # sin sorteo si la tasa es 0 (arnes)
                f = int(rr.integers(0, 6))
                if f == 0: x[0] = float(rr.integers(0, NSEN))
                elif f == 1: x[1] = float(rr.integers(0, 6))
                elif f == 2: x[2] = 1.0 - x[2]
                elif f == 3: x[3] = float(min(1.0, max(0.0, x[3] + rr.normal(0, 0.15))))
                elif f == 4: x[4] = float(rr.integers(0, NACC))
                else: x[5] = float(min(3.0, max(-3.0, x[5] + rr.normal(0, 0.5))))
        if R and C['p_dup'] > 0 and rr.random() < C['p_dup']:
            j = int(rr.integers(0, len(R))); R.insert(j + 1, list(R[j]))
        if R and C['p_del'] > 0 and rr.random() < C['p_del']:
            del R[int(rr.integers(0, len(R)))]
        if C['p_ins'] > 0 and rr.random() < C['p_ins']: R.append(self._bq_azar())
        return R[:NRMAX]

    def _bq_banco(self, R):
        if not BQ_C['banco'] or not R: return   # una lista vacia no lleva nada: no entra al banco
        B = _BQ_BANCO.setdefault(self._bqi, []); B.append([list(r) for r in R])
        if len(B) > BQ_C['banco']: B.pop(0)

    def _bq_sen(self, s, j, E, Ag, d, foco):
        if s == 0: return min(max(1.0 - E, 0.0), 1.0)
        if s == 1: return min(max(1.0 - Ag, 0.0), 1.0)
        if s == 2: return 1.0 - min(d, 10) / 10.0
        if s == 3: return float(self.PAT[foco][j])
        if s == 4: return 0.0 if self._bqlk is None else float(self.PAT[self._bqlk][j])
        if s == 5: return (self._bqlr + 3.0) / 4.0
        pos, objs, L, cc = self._bqcache
        if j not in cc:
            dm = None
            for x, k in objs.items():
                if self.PAT[k][j] > 0.5:
                    dd = min((pos - x) % L, (x - pos) % L)
                    if dm is None or dd < dm: dm = dd
            cc[j] = 0.0 if dm is None else 1.0 - min(dm, 20) / 20.0
        return cc[j]

    def _bq_cumple(self, r, E, Ag, d, foco):
        x = self._bq_sen(int(r[0]), int(r[1]), E, Ag, d, foco)
        return (x > r[3]) if r[2] > 0.5 else (x < r[3])

    def _bq_mov(self, V, E, Ag, d, k, left):
        for r in self._bqR:
            a = int(r[4])
            if a == 0 or not self._bq_cumple(r, E, Ag, d, k): continue
            if a == 1:
                if d > 0:
                    if left: V[0] += r[5]
                    else: V[1] += r[5]
            else:
                V[0] -= r[5]; V[1] -= r[5]

    def _bq_boca(self, E, Ag, kk):
        b = 0.0
        for r in self._bqR:
            if int(r[4]) == 0 and self._bq_cumple(r, E, Ag, 0, kk): b += r[5]
        return b

    def _bq_paso(self, obs):
        self._bqcache = (obs['pos'], obs['objs'], self.L, {})
        t = int(obs['t'])
        if t % 5000 == 0:
            tel = _BQ_TEL[self._bqi]; tel['muestras'].append([t, [list(r) for r in self._bqR]])
            if self._bqi == 0: tel['suelo'].append([t, sum(1 for k in obs['objs'].values() if k in ('A', 'C')), len(obs['objs'])])

    def _bq_parto(self):
        if BQ_FORZADA is not None: ch = [list(r) for r in self._bqR]
        elif DONANTE == 'azar':
            B = _BQ_BANCO.get(self._bqi) or []
            ch = self._bq_muta(B[int(self._bqrng.integers(len(B)))] if B else [])
            self._bq_banco(ch)
        else:
            ch = self._bq_muta(self._bqR); self._bq_banco(self._bqR)
        _BQ_TEL[self._bqi]['partos'] += 1
        return dict(bq=ch)

    def _bq_nace(self, info):
        m = info.get('memoria')
        if m is not None and 'bq' in m: self._bqR = [list(r) for r in m['bq']]
        self._bqlk = None; self._bqlr = 0.0
'''


def anclas(nombre, b, d):
    return [
        ('"""V143_TERMO.py — termo: V143 + UNA pieza de boca (termostato de dos necesidades; ver construye_termo.py). Cero memoria nueva.' + NL,
         f'"""{nombre}.py — bloques_pista: V143_TERMO + GENOMA DE REGLAS heredable (port de bloques/opusM). EXPLORATORIO.' + NL
         + f'GENERADO por experimentos/organelos/bloques_pista/construye_bp.py desde termo/carros/V143_TERMO.py (sha {SHA_TERMO}).' + NL
         + f'NO editar a mano. BLOQ = {b}; DONANTE = {d!r}. Con BLOQ = 0 es V143_TERMO bit a bit.' + NL + NL
         + 'V143_TERMO.py — termo: V143 + UNA pieza de boca (termostato de dos necesidades; ver construye_termo.py). Cero memoria nueva.' + NL),
        ('TERMO = 1   # termo: LA UNICA LINEA QUE CAMBIA ENTRE VARIANTES (0 = V143 bit a bit; 1 = TERMO; 2 = TERMOINV)' + NL,
         'TERMO = 1   # termo: LA UNICA LINEA QUE CAMBIA ENTRE VARIANTES (0 = V143 bit a bit; 1 = TERMO; 2 = TERMOINV)' + NL
         + PER.format(b=b, d=d) + NL + MODULO),
        ('        self._tm_init(ctx)   # termo: solo contadores (sin rng)' + NL,
         '        self._tm_init(ctx)   # termo: solo contadores (sin rng)' + NL
         + '        if BLOQ: self._bq_init(ctx)   # bloques_pista: genoma del fundador (banco del linaje o INICIAL al azar), rng propio' + NL),
        ('        if OPCION: self._apr_paso(E, Ag)' + NL,
         '        if OPCION: self._apr_paso(E, Ag)' + NL
         + '        if BLOQ: self._bq_paso(obs)   # bloques_pista: foto del anillo para el sentido 6 + telemetria (sin rng)' + NL),
        ('        V = self.Wl @ x; p = 1 / (1 + np.exp(-(V - .8) / noise));',
         '        V = self.Wl @ x' + NL
         + '        if BLOQ and self._bqR: self._bq_mov(V, E, Ag, d, k, left)   # bloques_pista: sesgos de patas' + NL
         + '        p = 1 / (1 + np.exp(-(V - .8) / noise));'),
        ('            Vb = self.ALPHA * _wt + self.HAMBRE_BOCA * hambre + .5' + NL,
         '            Vb = self.ALPHA * _wt + self.HAMBRE_BOCA * hambre + .5' + NL
         + '            if BLOQ and self._bqR: Vb += self._bq_boca(E, Ag, kk)   # bloques_pista: sesgo de boca (foco = la letra en la celda)' + NL),
        ('        R = _Rv[_na]; self._R = R' + NL,
         '        R = _Rv[_na]; self._R = R' + NL
         + '        if BLOQ: self._bqlk = kk; self._bqlr = float(R)   # bloques_pista: memoria que solo leen las reglas' + NL),
        ('        return None   # hereda=\'nada\': el hijo no se lleva memoria (la dote la pone la pista)' + NL,
         '        if BLOQ: return self._bq_parto()   # bloques_pista: el hijo lleva las reglas (padre mutado, o azar del banco)' + NL
         + '        return None   # hereda=\'nada\': el hijo no se lleva memoria (la dote la pone la pista)' + NL),
        ('        if OPCION: self._apr_nace(info)' + NL,
         '        if OPCION: self._apr_nace(info)' + NL
         + '        if BLOQ: self._bq_nace(info)   # bloques_pista: el nacido aplica las reglas heredadas' + NL),
        ('    def _tm_salida(self):' + NL + '        return dict(termo=TERMO, **self._tm)' + NL,
         '    def _tm_salida(self):' + NL + '        return dict(termo=TERMO, **self._tm)' + NL + METODOS.replace('\n', NL)),
    ]


def h16b(x): return hashlib.sha256(x).hexdigest()[:16]
def h16(p): return h16b(open(p, 'rb').read())


def construye(nombre, b, d):
    src = open(ORIGEN, 'rb').read()
    if h16b(src) != SHA_TERMO: raise SystemExit(f"origen sha {h16b(src)} != {SHA_TERMO}")
    txt = src.decode('utf-8')
    for a, rep in anclas(nombre, b, d):
        n = txt.count(a)
        if n != 1: raise SystemExit(f"ancla {a[:70]!r} aparece {n} veces (se exige 1)")
        txt = txt.replace(a, rep)
    return txt.encode('utf-8')


def todas():
    return {n: construye(n, b, d) for n, b, d in VARIANTES}


def main(argv=None):
    ap = argparse.ArgumentParser(allow_abbrev=False)
    ap.add_argument('--verifica', action='store_true')
    a = ap.parse_args(argv)
    outs = todas()
    base = outs['V143_BQ'].decode('utf-8').split(NL)
    for n, bts in outs.items():
        ls = bts.decode('utf-8').split(NL)
        dif = [i for i, (x, y) in enumerate(zip(base, ls)) if x != y]
        if len(ls) != len(base) or any(not ('BLOQ = ' in ls[i] or n in ls[i]) for i in dif):
            raise SystemExit(f"{n}: difiere de V143_BQ en algo mas que perilla/nombre: lineas {dif[:6]}")
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
    print(f"origen V143_TERMO.py sha {h16(ORIGEN)} (fijado {SHA_TERMO}) - construye_bp.py sha {h16(os.path.abspath(__file__))}")
    return 0 if ok else 1


if __name__ == '__main__':
    sys.exit(main())
