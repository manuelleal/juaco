"""construye_v143.py — construye POR ANCLAS los carros del bloque tronco_v14_3 (candidato a tronco v14.3, nivel 9).

MISION: llegar a la AGI por este camino. Pregunta del director (23-sep): ¿el BICHO REAL (el organismo, con piezas locales ya
medidas, sin politica escrita a mano) cruza H-1 en la MISMA pista de la carrera de ayer, donde solo lo cruzaron carros cuya
politica escribio un LLM (O1 limpia a mano)?

ORIGENES (solo se LEEN; sha16 fijados; cada ancla debe aparecer EXACTAMENTE una vez o el constructor aborta):
  experimentos/carrera_escuderias/carros/APR.py  (SHA_APR)   = FABRICA (v14.1 en el mundo vivo, brazo REL de organismo_f9c)
                                                              + la boca corregida por TD y heredada (aprende_barrer, 20/20 x2).
                                                              Con OPCION = 0 es FABRICA bit a bit (identidad_apr.py 21/21).
  organismo/organismo_v142.py (SHA_V142, CONGELADO)           = de aqui sale LITERAL la regla B-5 (lo unico que v14.2 agrega a
                                                              v14.1): la division por conflicto tambien con R == 0.
  experimentos/creacion_B/organismo_vivo_codigo.py (SHA_VIVO_B5) = el port de B-5 al mundo de DOS necesidades (la hija nace sin
                                                              valor en la necesidad activa y hereda las otras): se verifica que el
                                                              port de aqui es el mismo.
  experimentos/subida_n6/mundo_subida.py (SHA_N6)             = de aqui sale la pieza FILTRO (el veneno recordado no es objetivo,
                                                              SOLO si hay meta recordada); se verifica su texto.

PERILLAS (constantes de modulo; con TODAS en 0 el carro es FABRICA bit a bit -> identidad_v143.py):
  DESAMB  B-5 de v14.2 (FABRICA es v14.1: la carrera de ayer corrio SIN B-5).        -> DESAMB = 1 es "v14.2 en la pista"
  FILTRO  pieza 1, port de subida_n6 al anillo con vista completa: la letra que el organismo recuerda como mala en ALGUNA de sus
          dos filas (y no es meta) no es objetivo de las patas NI se muerde, SOLO si hay meta (algun objeto a la vista con valor
          > 0 en la fila de la necesidad activa). Sin meta, el filtro no actua (n6: "evita el bloqueo").
  META    1 = el filtro solo actua con meta (el candidato). 0 = actua siempre (LESION de la pieza 3: sin meta no hay limpieza).
  INVIERTE 1 = el filtro lee el valor de la letra pareja (A<->B, C<->D): CONTROL de contenido (debe caer).
  OPCION  pieza 2, la boca TD de APR (misma letra y mismas constantes que APR). Con FILTRO, la opcion decide SOLO donde el
          filtro no veta (en la practica: cuando no hay meta = cuando limpiar o no).
Pieza 3 (LIMPIAR) NO se escribe: si aparece, sale de la condicion de meta de la pieza 1 (sin meta, las patas van a lo mas cercano
y la boca de la fila activa muerde lo que golpea a la OTRA necesidad) y la corrige la pieza 2. Su lesion es META = 0.
Memoria nueva: CERO en FILTRO/META/INVIERTE/DESAMB (leen las dos filas de valor que el organismo ya tiene); la de OPCION es la de
APR (Q 2x6 + dS sentido por letra), ya medida y declarada. Constantes nuevas: CERO (umbral de meta y de obstaculo = 0, el signo).

Genera en experimentos/tronco_v14_3/carros_v143/ (archivos NUEVOS de esta carpeta; no toca nada fuera):
  V142            DESAMB 1                                  (el tronco v14.2 en la pista)
  V143            DESAMB 1, FILTRO 1, META 1, OPCION 1      (EL CANDIDATO)
  V143_SINFILTRO  DESAMB 1, OPCION 1                        (lesion pieza 1)
  V143_SINTD      DESAMB 1, FILTRO 1, META 1                (lesion pieza 2 -- el control que PUEDE GANAR)
  V143_SIEMPRE    DESAMB 1, FILTRO 1, META 0, OPCION 1      (lesion pieza 3: el filtro actua sin meta -> no hay limpieza)
  V143_INVERTIDO  DESAMB 1, FILTRO 1, META 1, INVIERTE 1, OPCION 1   (control de contenido)
Las variantes difieren SOLO en la linea de perillas y en el nombre (se verifica).

    python experimentos/tronco_v14_3/construye_v143.py [--verifica]
"""
import argparse, hashlib, os, sys

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
ORIGEN = os.path.join(RAIZ, 'experimentos', 'carrera_escuderias', 'carros', 'APR.py')
V142 = os.path.join(RAIZ, 'organismo', 'organismo_v142.py')
VIVO_B5 = os.path.join(RAIZ, 'experimentos', 'creacion_B', 'organismo_vivo_codigo.py')
N6 = os.path.join(RAIZ, 'experimentos', 'subida_n6', 'mundo_subida.py')
SALIDA = os.path.join(AQUI, 'carros_v143')
SHA_APR = '4402aa5142065c72'
SHA_V142 = '17528d767fcebaf6'
SHA_VIVO_B5 = '839fa71f9c84cb26'
SHA_N6 = '484e34db8f2150da'

# lo que se exige LITERAL en los origenes de las piezas (si cambian, el port ya no es el mismo)
LITERAL_V142 = ["if (Wb[c]*R<0 or (desambiguar and R==0)) and abs(float(Wb[c]))>0.2 and float(kj@P)>float(KW[c]@P) and (~activa).any():",
                "elif R<0: Wn[j]=Wn[c]; Wp[j]=0.; Wn[c]=0.",
                "else: Wp[j]=0.; Wn[j]=0.; _ndes+=1"]
LITERAL_VIVO_B5 = ["if (Wb[c]*R<0 or (desambiguar and R==0)) and abs(float(Wb[c]))>0.2 and float(kj@P)>float(KW[c]@P) and (~activa).any():",
                   "elif R<0: Wn[_nm,j]=Wn[_nm,c]; Wp[_nm,j]=0.; Wn[_nm,c]=0.",
                   "else: Wp[_nm,j]=0.; Wn[_nm,j]=0.; _ndes+=1",
                   "if n_nec>1 and hereda_nec:"]
LITERAL_N6 = ["if filtro and _obst(x): continue   # subida_n6: el veneno recordado no es objetivo",
              "if filtro and _obst(x): continue   # subida_n6: tampoco en el fallback v9",
              "return bool(_Nb[1] and _Nb[0][_x])   # solo con META recordada"]

VARIANTES = [  # nombre, DESAMB, FILTRO, META, INVIERTE, OPCION
    ('V142', 1, 0, 1, 0, 0),
    ('V143', 1, 1, 1, 0, 1),
    ('V143_SINFILTRO', 1, 0, 1, 0, 1),
    ('V143_SINTD', 1, 1, 1, 0, 0),
    ('V143_SIEMPRE', 1, 1, 0, 0, 1),
    ('V143_INVERTIDO', 1, 1, 1, 1, 1),
]


def h16b(b): return hashlib.sha256(b).hexdigest()[:16]


PERILLAS = ("DESAMB = {d}; FILTRO = {f}; META = {m}; INVIERTE = {i}   "
            "# tronco_v14_3: LA UNICA LINEA QUE CAMBIA ENTRE VARIANTES (con OPCION)")

CONSTANTES = '''
# ================================================================ tronco_v14_3 (candidato v14.3) -- perillas
# Con DESAMB = FILTRO = OPCION = 0 este archivo es FABRICA bit a bit (arnes experimentos/tronco_v14_3/identidad_v143.py).
# DESAMB: B-5 de v14.2 (literal de organismo/organismo_v142.py, port de dos necesidades de creacion_B/organismo_vivo_codigo.py).
# FILTRO: pieza 1 (subida_n6): lo recordado como malo en alguna fila no es objetivo ni se muerde, SOLO con META (algo a la vista
#         con valor > 0 en la fila activa). META = 0: actua siempre (lesion). INVIERTE = 1: lee la letra pareja (control).
{perillas}
PAREJA = {{'A': 'B', 'B': 'A', 'C': 'D', 'D': 'C'}}   # solo para INVIERTE (control de contenido)
CACHE = 1   # tras el humo: las dos filas por letra solo cambian al morder o al nacer -> se guardan hasta entonces (arnes: CACHE 0 == 1 bit a bit)
'''

METODOS = '''
    # ================================================================ tronco_v14_3: PIEZA 1 (FILTRO con META) y telemetria
    # Lee SOLO las dos filas de valor del propio organismo (_vnec: via rapida si el codigo es familiar, via lenta si no; la
    # misma lectura que usa la boca). Nada del mundo que el cuerpo no vea: la pista ya le entrega los objetos a la vista.
    def _v3_init(self, ctx):
        self._v3o = frozenset()          # letras que HOY son obstaculo (se recalcula cada paso; no persiste)
        self._v3m = False                # hay meta a la vista en este paso
        self._v3c = None                 # CACHE de las dos filas por letra (se invalida al morder y al nacer)
        self._v3 = dict(pasos=0, pasos_meta=0, vetos=0, limpia_propia=0, mord_sin_meta=0, todo_obst=0, des_splits=0, des_t=[])

    def _v3_prep(self, objs, na):
        PAT = self.PAT
        if CACHE and self._v3c is not None: v = self._v3c
        else:
            v = {}
            for k in PAT:
                kr = PAREJA[k] if INVIERTE else k
                kc = self._kenyon(PAT[kr])
                v[k] = (self._vnec(0, PAT[kr], kc), self._vnec(1, PAT[kr], kc))
            if CACHE: self._v3c = v
        letras = set(objs.values())
        meta = any(v[k][na] > 0 for k in letras)
        self._v3m = meta
        self._v3v = v
        if meta or not META: self._v3o = frozenset(k for k in PAT if v[k][na] <= 0 and min(v[k]) < 0)
        else: self._v3o = frozenset()
        self._v3['pasos'] += 1; self._v3['pasos_meta'] += int(meta)

    def _v3_salida(self):
        st = dict(self._v3); st['des_t'] = list(self._v3['des_t'][:200])
        return dict(desamb=DESAMB, filtro=FILTRO, meta=META, invierte=INVIERTE, opcion=OPCION, **st)

'''

ANCLAS = [
    # (ancla, reemplazo); NL = fin de linea del origen
    ('"""carros/APR.py — APR (camino A, experimentos/aprende_barrer): FABRICA + la OPCION APRENDIDA de morder lo malo conocido.',
     '"""{nombre}.py — tronco_v14_3 (candidato a tronco v14.3): FABRICA + B-5 + FILTRO con META + boca TD de APR.'
     'NLGENERADO por experimentos/tronco_v14_3/construye_v143.py desde carros/APR.py (sha {sha}). NO editar a mano.'
     'NLPerillas: {perillas_txt}. Con DESAMB = FILTRO = OPCION = 0 es FABRICA bit a bit. Sigue el docstring de APR.NL'
     'NLcarros/APR.py — APR (camino A, experimentos/aprende_barrer): FABRICA + la OPCION APRENDIDA de morder lo malo conocido.'),
    ("OPCION = 1NL", "OPCION = {opcion}NL"),
    ("BIN_POST = (0.0, 0.3, 0.6, 1.0)                     # min(E,Ag) PREDICHO tras morderNL",
     "BIN_POST = (0.0, 0.3, 0.6, 1.0)                     # min(E,Ag) PREDICHO tras morderNL{constantes}"),
    ("        self._apr_init(ctx)NL",
     "        self._apr_init(ctx)NL        self._v3_init(ctx)NL"),
    ("            if self.MEMORIA_RECHAZO and self._rech.get(x, -1) > t: continueNL",
     "            if self.MEMORIA_RECHAZO and self._rech.get(x, -1) > t: continueNL"
     "            if FILTRO and k in self._v3o: continue   # tronco_v14_3 FILTRO (subida_n6): lo recordado malo no es objetivoNL"),
    ("            if contar: self.sin_objetivo[self._q(t)] += 1NL            for x, k in objs.items():NL",
     "            if contar: self.sin_objetivo[self._q(t)] += 1NL            for x, k in objs.items():NL"
     "                if FILTRO and k in self._v3o: continue   # tronco_v14_3: tampoco en el fallback (n6)NL"),
    ("        return bestNL",
     "        if best is None and FILTRO:   # tronco_v14_3: TODO es obstaculo (solo posible con META = 0): las patas vuelven a lo mas cercanoNL"
     "            self._v3['todo_obst'] += 1   # (la boca sigue vetando; lo hallo el arnes (7e) antes del humo)NL"
     "            for x, k in objs.items():NL"
     "                dl = (pos - x) % L; dr = (x - pos) % L; d = min(dl, dr)NL"
     "                if best is None or d < best[0]: best = (d, k, dl < dr)NL"
     "        return bestNL"),
    ("        d, k, left = self._see(pos, objs, t, contar=True); pat = PAT[k]NL",
     "        if FILTRO: self._v3_prep(objs, _na)NL"
     "        d, k, left = self._see(pos, objs, t, contar=True); pat = PAT[k]NL"),
    ("            if OPCION: mordio = self._opcion(obs, kk, mordio, _u9, pb)NL",
     "            if FILTRO and kk in self._v3o:   # tronco_v14_3 FILTRO: con meta, lo recordado malo no se muerde (mismo sorteo consumido)NL"
     "                self._v3['vetos'] += int(mordio); mordio = FalseNL"
     "            elif OPCION: mordio = self._opcion(obs, kk, mordio, _u9, pb)NL"
     "            if FILTRO and mordio and not self._v3m:NL"
     "                self._v3['mord_sin_meta'] += 1; self._v3['limpia_propia'] += int(min(self._v3v[kk]) < 0)NL"),
    ("            if Wb[c] * R < 0 and abs(float(Wb[c])) > 0.2 and float(kj @ P) > float(KW[c] @ P) and (~activa).any():NL",
     "            if (Wb[c] * R < 0 or (DESAMB and R == 0)) and abs(float(Wb[c])) > 0.2 and float(kj @ P) > float(KW[c] @ P) and (~activa).any():   # B-5 (v14.2)NL"),
    ("                else:     Wn[_nm, j] = Wn[_nm, c]; Wp[_nm, j] = 0.; Wn[_nm, c] = 0.NL",
     "                elif R < 0: Wn[_nm, j] = Wn[_nm, c]; Wp[_nm, j] = 0.; Wn[_nm, c] = 0.NL"
     "                else:   # B-5: con R == 0 la hija nace SIN valor en la necesidad activa (hereda las otras abajo); la madre conservaNL"
     "                    Wp[_nm, j] = 0.; Wn[_nm, j] = 0.; self._v3['des_splits'] += 1NL"
     "                    if len(self._v3['des_t']) < 200: self._v3['des_t'].append((int(t), kk, int(_nm)))NL"),
    ("        if OPCION and res['mordio']: self._apr_dS(res['letra'], res['dS'])NL",
     "        if res['mordio']: self._v3c = None   # tronco_v14_3 CACHE: morder cambia las filasNL"
     "        if OPCION and res['mordio']: self._apr_dS(res['letra'], res['dS'])NL"),
    ("        if OPCION: self._apr_nace(info)NL",
     "        if OPCION: self._apr_nace(info)NL        self._v3c = None   # tronco_v14_3 CACHE: nacer reinicia las filasNL"),
    ("    def salida(self):NL", "{metodos}    def salida(self):NL"),
    ("            _rep_cuello=int(kw['rep_cuello']), **({'apr': self._apr_salida()} if OPCION else {}))NL",
     "            _rep_cuello=int(kw['rep_cuello']), **({'apr': self._apr_salida()} if OPCION else {}),NL"
     "            **({'v143': self._v3_salida()} if (DESAMB or FILTRO) else {}))NL"),
]


def lee(ruta, sha, literales=()):
    b = open(ruta, 'rb').read()
    if h16b(b) != sha: raise SystemExit(f"CONSTRUYE: {ruta} sha {h16b(b)} != {sha} (el origen cambio)")
    txt = b.decode('utf-8')
    for s in literales:
        if txt.count(s) < 1: raise SystemExit(f"CONSTRUYE: literal no encontrado en {os.path.basename(ruta)}: {s[:70]!r}")
    return txt


def construye(nombre, d, f, m, i, o):
    lee(V142, SHA_V142, LITERAL_V142); lee(VIVO_B5, SHA_VIVO_B5, LITERAL_VIVO_B5); lee(N6, SHA_N6, LITERAL_N6)
    txt = lee(ORIGEN, SHA_APR)
    NL = '\r\n' if '\r\n' in txt else '\n'
    if NL == '\r\n' and txt.replace('\r\n', '').count('\n'): raise SystemExit("CONSTRUYE: fines de linea mezclados en APR.py")
    per = PERILLAS.format(d=d, f=f, m=m, i=i)
    fmt = dict(nombre=nombre, sha=SHA_APR, opcion=o, perillas_txt=f"DESAMB {d} FILTRO {f} META {m} INVIERTE {i} OPCION {o}",
               constantes=CONSTANTES.format(perillas=per).lstrip('\n').replace('\n', NL),
               metodos=METODOS.lstrip('\n').replace('\n', NL))
    for a, r in ANCLAS:
        a = a.replace('NL', NL)
        n = txt.count(a)
        if n != 1: raise SystemExit(f"CONSTRUYE: el ancla aparece {n} veces (debe ser 1): {a[:80]!r}")
        r = r.replace('NL', NL)
        if '{' in r and any(('{' + k + '}') in r for k in fmt): r = r.format(**fmt) if "{'apr'" not in r else r
        txt = txt.replace(a, r)
    return txt.encode('utf-8')


def normaliza(b, nombre):
    """quita lo que DEBE diferir entre variantes (nombre, linea de perillas, OPCION) para comparar el resto."""
    out = []
    for ln in b.decode('utf-8').splitlines():
        if ln.startswith('DESAMB = ') or ln.startswith('OPCION = ') or ln.startswith('Perillas: '): continue
        out.append(ln.replace(nombre + '.py', 'X.py'))
    return '\n'.join(out)


def todas():
    return {v[0]: construye(*v) for v in VARIANTES}


def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--verifica', action='store_true')
    a = ap.parse_args()
    outs = todas()
    base = normaliza(outs['V143'], 'V143')
    for n in outs:
        if normaliza(outs[n], n) != base: raise SystemExit(f"CONSTRUYE: {n} difiere de V143 en algo mas que perillas / OPCION")
    os.makedirs(SALIDA, exist_ok=True)
    ok = True
    for n, b in outs.items():
        ruta = os.path.join(SALIDA, n + '.py')
        if a.verifica:
            igual = os.path.exists(ruta) and open(ruta, 'rb').read() == b
            ok &= igual; print(f"  {'IGUAL ' if igual else 'DISTINTO'} {n}.py sha {h16b(b)}")
        else:
            with open(ruta, 'wb') as fh: fh.write(b)
            print(f"  escrito {ruta} (sha {h16b(b)}; {len(b)} bytes)")
    print(f"  origenes: APR.py {SHA_APR} · organismo_v142.py {SHA_V142} · organismo_vivo_codigo.py {SHA_VIVO_B5} · mundo_subida.py {SHA_N6}")
    return 0 if ok else 1


if __name__ == '__main__':
    sys.exit(main())
