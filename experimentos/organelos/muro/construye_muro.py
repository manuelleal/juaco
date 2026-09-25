"""construye_muro.py — construye POR ANCLAS los carros del bloque MURO (intento de cruzar H-1 con el bicho real, 25-sep-2026).

MISION: llegar a la AGI por este camino (organismo minimo con reglas locales, sin retropropagacion, peldanos preregistrados con
controles y replicas).

EL CANDIDATO PREREGISTRADO es GLOT = 3 (GLOTU, abajo) con su control GLOT = 4 (GLOTUINV). Las demas perillas quedan como
instrumento del EXPLORATORIO (declarado en INFORME.md; todas nacen inertes: con todo en 0 el carro es V143 bit a bit).

PIEZA PAGA (v2, tras el exploratorio v1 declarado en INFORME.md): CTA, "no vuelvas a morder lo que ya te hizo dano
en lo que HOY mas te falta" (aversion por IDENTIDAD de un ensayo, Garcia y Koelling), con el estado presente. Cero memoria nueva: lee
lo que el linaje SINTIO de cada letra (_adS de APR, ya en v14.3: media del dS que la pista devuelve en resultado(), por letra; NO las
filas de valor, que generalizan por pixeles: v1 las usaba y el fundador dejaba de probar lo bueno) y el estado presente (E, Ag).
Ningun umbral escrito a mano: la unica comparacion es entre las dos necesidades del propio cuerpo.
  s(k)      media del dS sentido por el linaje al morder k (None si nunca la mordio).
  act(k)    s(k) < 0 en la necesidad ACTIVA na (la que mas falta).
  otra(k)   s(k) < 0 solo en la otra necesidad o.
  paga(k)   el golpe sentido, cobrado a la otra necesidad, la deja al menos tan llena como la activa: lev[o] + s_o(k) >= lev[na].
Actua SOLO en la BOCA y SOLO en los pasos SIN META (sin nada a la vista con valor > 0 en la fila activa), que es donde v14.3 no veta
nada y la boca de fabrica muerde por hambre. Con meta: v14.3 tal cual. Las patas: v14.3 tal cual siempre. Usa el mismo sorteo.
PERILLA PAGA (una linea nueva de modulo):
  0  V143 bit a bit (arnes identidad_muro.py).
  1  CTA (el CANDIDATO): sin meta, la boca veta act y la otra-no-pagable.
  2  CTA+LIMPIA (exploratorio): 1 + con meta, la boca NO veta la otra-pagable que v14.3 vetaria (limpieza costeable en ruta).
  3  CONTROL "sin estado": sin meta, la boca veta TODO lo sentido malo (act y otra), pague o no.
  4  CONTROL "desfasado": sin meta, la boca veta lo sentido malo para la OTRA necesidad y deja lo malo para la activa (necesidad al reves).
PERILLA GLOT (v3, tras la lectura temprana del puenteo del coordinador: "el problema es la glotoneria de lo bueno"):
  0  nada.
  1  GLOT: en TODOS los pasos, la boca no muerde una letra cuyo dS SENTIDO por el linaje (_adS) solo sube la necesidad que NO es la
     activa (s_o > 0 y s_na <= 0): "lo que solo sirve a lo que ya te sobra, dejalo en el mundo". Sin umbral: no mira cuanto, solo cual.
  2  CONTROL "por filas": lo mismo leyendo las FILAS de valor (v[k][o] > 0 y v[k][na] <= 0; generalizan por pixeles) en vez de lo sentido.
  3  GLOTU (v5, tras GLOT 0/5: vetar lo de la otra necesidad SIEMPRE mataba de hambre): la boca no muerde una letra cuyo dS SENTIDO
     solo sube la necesidad j, si j es la MAS LLENA de las dos (lev[j] > lev[otra]) Y ya esta en el umbral de reproduccion o encima
     (lev[j] >= rep_umbral, el del mundo, en ctx; el mismo que usa APR). "No comas para lo que ya tienes de sobra; come para lo que
     te falta". Mide niveles, no deficits recortados (con E y Ag >= umbral los deficits son 0 y la necesidad activa es siempre la 0).
  4  CONTROL "al reves" de GLOTU: veta lo que solo sube la MENOS llena de las dos cuando esa ya esta en el umbral o encima.
PERILLA PATAS (v4, tras GLOT 0/5 en el exploratorio y la lectura del puenteo "las patas de O1 solas cierran la brecha en s36001"):
  0  nada (las patas de v14.3: van al objeto MAS CERCANO que no sea obstaculo, sea lo que sea; la boca decide al llegar).
  1  PATAS: con META (hay a la vista algo con valor > 0 en la fila ACTIVA, la misma lectura del FILTRO), el objetivo de las patas es
     el MAS CERCANO de ESOS (lo que sirve a lo que hoy mas falta). Sin meta: v14.3 tal cual. Sin umbral, sin memoria nueva, sin rng.
     Distinto del cable 'patas' de trasplantes (sesgo lineal +2/+1 sumado a la distancia: 16 celdas por unidad de valor): aqui es
     categorico (solo cuenta QUE sirva a la necesidad activa, no cuanto).
  2  CONTROL "necesidad al reves": con meta, el objetivo es el mas cercano con valor > 0 en la fila de la OTRA necesidad (si no hay
     ninguno, v14.3). Misma lectura, misma dosis de restriccion; cambia solo que necesidad se mira.
TELEM (0/1): contadores de SOLO LECTURA en d['carro']['muro'] (el juez no los lee, ERR-96).

ORIGEN (solo se LEE; sha16 fijado; cada ancla EXACTAMENTE una vez o aborta):
  experimentos/tronco_v14_3/carros_v143/V143.py (SHA_V143 = 2a03048a7f1525e5)
Genera en muro/carros/ (PAGA, GLOT, PATAS, TELEM): V143_CTA (1,0,0,1) · V143_LIMPIA (2,0,0,1) · V143_SINEST (3,0,0,1) ·
  V143_DESF (4,0,0,1) · V143_GLOT (0,1,0,1) · V143_GLOTCTA (1,1,0,1) · V143_GLOTFILA (0,2,0,1) · V143_PATAS (0,0,1,1) ·
  V143_PATASDESF (0,0,2,1) · V143_GLOTU (0,3,0,1) · V143_GLOTUINV (0,4,0,1) · V143_GLOTUPATAS (0,3,1,1) · V143_MTEL (0,0,0,1)
Las variantes difieren SOLO en la linea de perillas y en el nombre (se verifica).

    python experimentos/organelos/muro/construye_muro.py [--verifica]
"""
import argparse, hashlib, os, sys

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(AQUI)))
ORIGEN = os.path.join(RAIZ, 'experimentos', 'tronco_v14_3', 'carros_v143', 'V143.py')
SALIDA = os.path.join(AQUI, 'carros')
SHA_V143 = '2a03048a7f1525e5'
NL = '\r\n'   # el origen tiene fin de linea CRLF; se conserva

VARIANTES = [('V143_CTA', 1, 0, 0, 1), ('V143_LIMPIA', 2, 0, 0, 1), ('V143_SINEST', 3, 0, 0, 1), ('V143_DESF', 4, 0, 0, 1),
             ('V143_GLOT', 0, 1, 0, 1), ('V143_GLOTCTA', 1, 1, 0, 1), ('V143_GLOTFILA', 0, 2, 0, 1),
             ('V143_PATAS', 0, 0, 1, 1), ('V143_PATASDESF', 0, 0, 2, 1), ('V143_GLOTU', 0, 3, 0, 1), ('V143_GLOTUINV', 0, 4, 0, 1),
             ('V143_GLOTUPATAS', 0, 3, 1, 1), ('V143_MTEL', 0, 0, 0, 1)]

PERILLAS = "PAGA = {p}; GLOT = {g}; PATAS = {q}; TELEM = {t}   # muro: LA UNICA LINEA QUE CAMBIA ENTRE VARIANTES (0/0/0/0 = V143 bit a bit)"

METODOS = '''
    # ================================================================ muro: CTA ("no vuelvas a morder lo que te hizo dano en lo que mas te falta")
    # Lee lo SENTIDO por el linaje (_adS) y el estado presente. Solo la boca, solo sin meta (PAGA 2: tambien limpieza con meta). Sin rng.
    def _pg_init(self, ctx):
        self._pg_lev = (1.0, 1.0); self._pgv = frozenset(); self._pg_act = frozenset(); self._pg_otra = frozenset(); self._pg_nop = frozenset()
        self._pg_glot = frozenset()
        self._pg = dict(pasos=0, sin_meta=0, veto_act=0, veto_otra=0, libera=0, mord_act=0, mord_otra_paga=0, mord_otra_nopaga=0,
                        mord_act_sinmeta=0, mord_otra_sinmeta=0, veto_glot=0, mord_solo_otra=0, patas_meta=0, patas_cambia=0)

    def _pg_prep(self, v, na, meta):
        lev = self._pg_lev; o = 1 - na; act = set(); otra = set(); nop = set(); glot = set()
        for k, m in self._adS.items():
            if m[2] <= 0: continue
            s0 = m[na] / m[2]; s1 = m[o] / m[2]
            if GLOT in (3, 4):   # GLOTU: por NIVELES (j = la necesidad que la letra sube, sola)
                e0 = m[0] / m[2]; e1 = m[1] / m[2]
                j = 0 if (e0 > 0 and e1 <= 0) else (1 if (e1 > 0 and e0 <= 0) else None)
                if j is not None and lev[j] >= self._aU and ((lev[j] > lev[1 - j]) if GLOT == 3 else (lev[j] < lev[1 - j])): glot.add(k)
            elif s1 > 0 and s0 <= 0: glot.add(k)   # lo SENTIDO solo sirve a la necesidad que no es la activa
            if s0 < 0: act.add(k)
            elif s1 < 0:
                otra.add(k)
                if lev[o] + s1 < lev[na]: nop.add(k)
        act = frozenset(act); otra = frozenset(otra); nop = frozenset(nop)
        self._pg_act = act; self._pg_otra = otra; self._pg_nop = nop
        if PAGA == 0: veto = self._v3o
        elif meta: veto = (self._v3o - (otra - nop)) if PAGA == 2 else self._v3o
        elif PAGA == 1 or PAGA == 2: veto = act | nop
        elif PAGA == 3: veto = act | otra
        else: veto = otra
        if GLOT == 2: glot = set(k for k in self.PAT if v[k][o] > 0 and v[k][na] <= 0)   # control: las FILAS (generalizan)
        self._pg_glot = frozenset(glot)
        if GLOT: veto = veto | self._pg_glot
        self._pgv = veto
        if TELEM: self._pg['pasos'] += 1; self._pg['sin_meta'] += int(not meta)

    def _pg_boca(self, kk, mordio_fab):
        if not TELEM: return
        g = self._pg
        if kk in self._pgv and kk not in self._v3o and mordio_fab: g['veto_act' if kk in self._pg_act else 'veto_otra'] += 1
        if kk in self._v3o and kk not in self._pgv and mordio_fab: g['libera'] += 1
        if GLOT and kk in self._pg_glot and kk not in self._v3o and mordio_fab: g['veto_glot'] += 1

    def _pg_mord(self, kk):
        if not TELEM: return
        g = self._pg; sm = not self._v3m
        if kk in self._pg_glot: g['mord_solo_otra'] += 1
        if kk in self._pg_act: g['mord_act'] += 1; g['mord_act_sinmeta'] += int(sm)
        elif kk in self._pg_otra:
            g['mord_otra_nopaga' if kk in self._pg_nop else 'mord_otra_paga'] += 1; g['mord_otra_sinmeta'] += int(sm)

    def _pg_salida(self):
        return dict(paga=PAGA, glot=GLOT, patas=PATAS, telem=TELEM, **self._pg)

    def _pg_sirve(self, k):
        """PATAS: la letra k es objetivo si, con meta, tiene valor > 0 en la fila activa (1) o en la de la otra necesidad (2, control)."""
        n = self._na if PATAS == 1 else 1 - self._na
        return self._v3v[k][n] > 0
'''

ANCLAS = [
    ('        L = self.L; best = None' + NL
     + '        for x, k in objs.items():' + NL
     + '            if self.MEMORIA_RECHAZO and self._rech.get(x, -1) > t: continue' + NL
     + '            if FILTRO and k in self._v3o: continue   # tronco_v14_3 FILTRO (subida_n6): lo recordado malo no es objetivo' + NL,
     '        L = self.L; best = None' + NL
     + '        _pq = bool(PATAS and FILTRO and self._v3m and any(self._pg_sirve(_k) for _k in set(objs.values())))   # muro PATAS' + NL
     + '        if _pq and contar and TELEM: self._pg["patas_meta"] += 1' + NL
     + '        for x, k in objs.items():' + NL
     + '            if self.MEMORIA_RECHAZO and self._rech.get(x, -1) > t: continue' + NL
     + '            if FILTRO and k in self._v3o: continue   # tronco_v14_3 FILTRO (subida_n6): lo recordado malo no es objetivo' + NL
     + '            if _pq and not self._pg_sirve(k): continue   # muro PATAS: con meta, solo lo que sirve (1: a la activa; 2: a la otra)' + NL),
    ('"""V143.py — tronco_v14_3 (candidato a tronco v14.3): FABRICA + B-5 + FILTRO con META + boca TD de APR.' + NL,
     '"""{nombre}.py — muro: V143 + UNA pieza local del bloque MURO (la de sus perillas; ver construye_muro.py). Cero memoria nueva.' + NL
     + 'GENERADO por experimentos/organelos/muro/construye_muro.py desde tronco_v14_3/carros_v143/V143.py (sha {sha}).' + NL
     + 'NO editar a mano. Perillas: {perillas_txt}. Con PAGA = GLOT = PATAS = TELEM = 0 es V143 bit a bit. Sigue el docstring de V143.' + NL + NL
     + 'V143.py — tronco_v14_3 (candidato a tronco v14.3): FABRICA + B-5 + FILTRO con META + boca TD de APR.' + NL),
    ('DESAMB = 1; FILTRO = 1; META = 1; INVIERTE = 0   # tronco_v14_3: LA UNICA LINEA QUE CAMBIA ENTRE VARIANTES (con OPCION)' + NL,
     'DESAMB = 1; FILTRO = 1; META = 1; INVIERTE = 0   # tronco_v14_3: LA UNICA LINEA QUE CAMBIA ENTRE VARIANTES (con OPCION)' + NL
     + '{perillas}' + NL),
    ('        self._v3_init(ctx)' + NL,
     '        self._v3_init(ctx)' + NL + '        self._pg_init(ctx)   # muro: solo estado propio y contadores (sin rng)' + NL),
    ('        if FILTRO: self._v3_prep(objs, _na)' + NL,
     '        if PAGA or GLOT or TELEM: self._pg_lev = (float(E), float(Ag))   # muro: estado presente (solo lectura)' + NL
     + '        if FILTRO: self._v3_prep(objs, _na)' + NL),
    ('        else: self._v3o = frozenset()' + NL,
     '        else: self._v3o = frozenset()' + NL
     + '        if PAGA or GLOT or TELEM: self._pg_prep(v, na, meta)   # muro (con PAGA = GLOT = 0 solo lee: veto = _v3o)' + NL),
    ('            if FILTRO and kk in self._v3o:   # tronco_v14_3 FILTRO: con meta, lo recordado malo no se muerde (mismo sorteo consumido)' + NL,
     '            if PAGA or GLOT or TELEM: self._pg_boca(kk, mordio)   # muro: telemetria (solo lectura)' + NL
     + '            if FILTRO and kk in (self._pgv if (PAGA or GLOT) else self._v3o):   # tronco_v14_3 FILTRO / muro: veto (mismo sorteo consumido)' + NL),
    ('            if FILTRO and mordio and not self._v3m:' + NL,
     '            if (PAGA or GLOT or TELEM) and mordio: self._pg_mord(kk)   # muro: telemetria (solo lectura)' + NL
     + '            if FILTRO and mordio and not self._v3m:' + NL),
    ("            **({'v143': self._v3_salida()} if (DESAMB or FILTRO) else {}))" + NL,
     "            **({'v143': self._v3_salida()} if (DESAMB or FILTRO) else {})," + NL
     + "            **({'muro': self._pg_salida()} if (PAGA or GLOT or TELEM) else {}))   # muro: telemetria (ERR-96: no puntua)" + NL
     + '{metodos}'),
]

def h16b(b): return hashlib.sha256(b).hexdigest()[:16]
def h16(p): return h16b(open(p, 'rb').read())


def construye(nombre, p, g, q, t):
    src = open(ORIGEN, 'rb').read()
    if h16b(src) != SHA_V143: raise SystemExit(f"origen {ORIGEN} sha {h16b(src)} != {SHA_V143}")
    txt = src.decode('utf-8')
    per = PERILLAS.format(p=p, g=g, q=q, t=t)
    metodos = METODOS.replace('\n', NL)
    for a, rep in ANCLAS:
        n = txt.count(a)
        if n != 1: raise SystemExit(f"ancla {a[:70]!r} aparece {n} veces (se exige 1)")
        rep = (rep.replace('{nombre}', nombre).replace('{sha}', SHA_V143).replace('{perillas_txt}', per.split('   #')[0])
               .replace('{perillas}', per).replace('{metodos}', metodos))
        txt = txt.replace(a, rep)
    return txt.encode('utf-8')


def todas():
    return {n: construye(n, p, g, q, t) for n, p, g, q, t in VARIANTES}


def main(argv=None):
    ap = argparse.ArgumentParser(allow_abbrev=False)
    ap.add_argument('--verifica', action='store_true')
    a = ap.parse_args(argv)
    outs = todas()
    base = outs['V143_CTA'].decode('utf-8').split(NL)
    for n, bts in outs.items():
        ls = bts.decode('utf-8').split(NL)
        dif = [i for i, (x, y) in enumerate(zip(base, ls)) if x != y]
        if len(ls) != len(base) or any(not ('PAGA = ' in ls[i] or n in ls[i]) for i in dif):
            raise SystemExit(f"{n}: difiere de V143_CTA en algo mas que perillas/nombre: lineas {dif[:6]}")
    ok = True
    os.makedirs(SALIDA, exist_ok=True)
    for n, bts in outs.items():
        ruta = os.path.join(SALIDA, n + '.py')
        if a.verifica:
            igual = os.path.exists(ruta) and open(ruta, 'rb').read() == bts; ok &= igual
            print(f"  {n} sha {h16b(bts)} == disco: {igual}")
        else:
            with open(ruta, 'wb') as fh: fh.write(bts)
            print(f"  escrito {ruta} (sha {h16b(bts)})")
    print(f"origen V143.py sha {h16(ORIGEN)} (fijado {SHA_V143}) · construye_muro.py sha {h16(os.path.abspath(__file__))}")
    return 0 if ok else 1


if __name__ == '__main__':
    sys.exit(main())
