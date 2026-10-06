"""construye_c.py — construye POR ANCLAS los carros del TRAMO C (peldanos 8, 9 y 10) sobre el texto de O1_LUGAR / O1_LUGAR_BAR que
produce construye_p1 (cadena: O1 sha 99436afa2715f028 -> O1_LUGAR (construye_p1, sha fijado) -> estos). 30-sep-2026, MODO RAFAGA.

MISION: llegar a la AGI por este camino (organismo minimo con reglas locales, sin retropropagacion, peldanos preregistrados con
controles y replicas). Plan: ESCALERA.md (P8-P10). Mundo: mundo_tramo_c.py. Runner: corre_c.py. Arnes: identidad_c.py.
Controles de contenido: "lugar equivocado" = ANTIPODA FIJO (b + 15 mod 30), como en P1 (ERR-170); "paso equivocado" (P9) = el credito va
a la PENULTIMA letra en vez de a la ultima (misma cantidad de credito, destino fijo y equivocado).

PIEZAS (cada una con su promotor; promotor 0 => O1_LUGAR bit a bit, arnes):
 P8  COMPONE (promotor COMPONE): la memoria de lugar (P1) se SUMA tambien a letras MIXTAS (con un dS negativo) y en todas las necesidades
     donde el bin recuerda > LG_MIN. P1 solo sumaba el bono a letras sin dano y en necesidades que ya valian > 0 (por eso P1 NO compone
     'letra mixta + sitio bueno': se dice). Memoria nueva: CERO. Control: COMPONE sobre O1_LUGAR_BAR (lee el antipoda).
     Lo que se mide es del MUNDO (mundo_tramo_c: exposiciones FRIAS a la letra E dentro del oasis, mordida o no).
 P9  PLAN (promotor PLAN): CREDITO DE UN PASO HACIA ATRAS (traza de elegibilidad de longitud 1, regla local): al morder una letra k ya
     conocida con sorpresa s = sum(dS - valor_medio(k)), la ULTIMA letra mordida antes (en esta vida) recibe hab[ultima] += PL_LAM*(s - hab).
     Al valorar una letra sin dano se suma PLAN_W*max(hab, 0) en las dos necesidades (una letra neutra que 'habilita' pasa a valer).
     Memoria nueva: hab (una tabla letra -> float, del linaje) + la ultima y penultima letra de esta vida. Control PLAN_BARAJA: el credito
     va a la PENULTIMA letra (paso equivocado).
 P10 PREGUNTA (promotor PREGUNTA): (a) OLVIDO POR PRESENCIA: cada paso con necesidad (min(lev) < U + MARGEN) y sin nada util a la vista, el
     bin donde esta pierde PG_OLVIDO de su memoria de lugar (estar ahi con hambre y no ver nada = 'este sitio ya no da'); (b) PREGUNTA: sin
     blanco a la vista y sin sitio recordado, en vez del hueco entre los otros cuerpos va al centro del bin que hace MAS tiempo no visita
     (edad / (distancia + D0)). Memoria nueva: visto (30 enteros, del linaje). Control PG_BARAJA: (a) igual, (b) el ANTIPODA del bin elegido.
Genera en escalera/carros/: O1_LUGAR_COMP, O1_LUGAR_COMP_BAR, O1_LUGAR_COMP0 · O1_LUGAR_PLAN, O1_LUGAR_PLAN_BAR, O1_LUGAR_PLAN0 ·
O1_LUGAR_PREG, O1_LUGAR_PREG_BAR, O1_LUGAR_PREG0  (los *0 solo para el arnes: == O1_LUGAR bit a bit).
    python experimentos/organelos/escalera/construye_c.py [--verifica]
"""
import argparse, hashlib, os, sys

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(AQUI)))
sys.path.insert(0, AQUI)
import construye_p1 as C1

SALIDA = os.path.join(AQUI, 'carros')
NL = '\n'
SHA_CONSTRUYE_P1 = '90dc1b6f848fac80'; SHA_O1_LUGAR = '49eee6bb278ea097'; SHA_O1_LUGAR_BAR = '93fc245b8db8794b'
PL_LAM = 0.2; PLAN_W = 1.0; PL_MIN = 0.05
PG_OLVIDO = 0.01
# (nombre, peldano, promotor, baraja_propia, base_bar)
VARIANTES = [('O1_LUGAR_COMP', 'comp', 1, 0, 0), ('O1_LUGAR_COMP_BAR', 'comp', 1, 0, 1), ('O1_LUGAR_COMP0', 'comp', 0, 0, 0),
             ('O1_LUGAR_PLAN', 'plan', 1, 0, 0), ('O1_LUGAR_PLAN_BAR', 'plan', 1, 1, 0), ('O1_LUGAR_PLAN0', 'plan', 0, 0, 0),
             ('O1_LUGAR_PREG', 'preg', 1, 0, 0), ('O1_LUGAR_PREG_BAR', 'preg', 1, 1, 0), ('O1_LUGAR_PREG0', 'preg', 0, 0, 0)]

METODOS = {
    'comp': '',
    'plan': '''
    # ================================================================ escalera p9: PLAN, credito de un paso hacia atras (regla local)
    def _pl_init(self):
        self.hab = {}; self._pl_last = None; self._pl_prev = None
        self.st['pl_cred'] = 0; self.st['pl_val'] = 0

    def _pl_v(self, v, k):
        """valor de la letra + lo que 'habilita' (solo si no dania y hab > PL_MIN), en las dos necesidades."""
        h = self.hab.get(k, 0.0)
        if h <= PL_MIN or (v < 0).any(): return v
        self.st['pl_val'] += 1
        return v + PLAN_W * h

    def _pl_apr(self, k, dS):
        """ANTES de actualizar la tabla por letra: la sorpresa de ESTA mordida acredita a la ultima letra (control: a la penultima)."""
        v = self._val(k)
        if v is not None:
            tgt = self._pl_prev if PLAN_BARAJA else self._pl_last
            if tgt is not None:
                s = float((dS - v).sum()); h = self.hab.get(tgt, 0.0)
                self.hab[tgt] = h + PL_LAM * (s - h); self.st['pl_cred'] += 1
        self._pl_prev = self._pl_last; self._pl_last = k

    def _pl_hereda(self, m):
        if not self.hab: self.hab = {k: float(v) for k, v in m.items()}

    def _pl_salida(self):
        return dict(plan=dict(W=PLAN_W, lam=PL_LAM, baraja=int(PLAN_BARAJA), hab={k: round(float(v), 3) for k, v in self.hab.items()}))
''',
    'preg': '''
    # ================================================================ escalera p10: PREGUNTA (olvido por presencia + ir a donde menos se sabe)
    def _pg_init(self):
        self.visto = np.full(LG_NB, -1, int); self.st['pg_exc'] = 0; self.st['pg_olv'] = 0

    def _pg_olvida(self, pos, lev, mejor):
        """(a) con necesidad y sin nada util a la vista, el bin donde esta pierde PG_OLVIDO de su memoria de lugar."""
        if mejor is None and min(lev) < self.U + MARGEN:
            b = self._lg_bin(pos)
            if (self.lugar[b] > 0).any(): self.lugar[b] *= (1.0 - PG_OLVIDO); self.st['pg_olv'] += 1

    def _pg_meta(self, pos, t):
        """(b) sin blanco y sin recuerdo: el centro del bin que hace mas tiempo no visita, por distancia (control: su antipoda)."""
        best = None
        for b in range(LG_NB):
            edad = t - self.visto[b] if self.visto[b] >= 0 else t + 1
            c = ((2 * b + 1) * self.L) // (2 * LG_NB); v = edad / (self._dist(pos, c) + D0)
            if best is None or v > best[0]: best = (v, b)
        b = best[1]
        if PG_BARAJA: b = (b + LG_NB // 2) % LG_NB
        self.st['pg_exc'] += 1
        return ((2 * b + 1) * self.L) // (2 * LG_NB)

    def _pg_hereda(self, m):
        if (self.visto < 0).all(): self.visto = np.asarray(m, int).copy()

    def _pg_salida(self):
        return dict(pregunta=dict(olvido=PG_OLVIDO, baraja=int(PG_BARAJA), visto=[int(z) for z in self.visto]))
''',
}


def cabecera(nombre, peldano, p, b, base):
    desc = {'comp': 'COMPONE (el bono de lugar se suma tambien a letras mixtas)', 'plan': 'PLAN (credito de un paso hacia atras)',
            'preg': 'PREGUNTA (olvido por presencia + ir al bin menos visitado)'}[peldano]
    prom = {'comp': 'COMPONE', 'plan': 'PLAN', 'preg': 'PREGUNTA'}[peldano]
    return (f'"""{nombre}.py — escalera {peldano}: O1_LUGAR{"_BAR" if base else ""} + {desc}. {prom} = {p}, baraja propia = {b}.' + NL
            + 'GENERADO por experimentos/organelos/escalera/construye_c.py sobre el texto de construye_p1 (sha fijado). NO editar a mano.' + NL + NL)


def anclas(nombre, peldano, p, b, base):
    A = [(f'"""O1_LUGAR{"_BAR" if base else ""}.py — escalera p1: O1 + MEMORIA DE LUGAR del linaje (bins del anillo x lo que el sitio dio de mas que su letra).' + NL,
          cabecera(nombre, peldano, p, b, base)
          + f'O1_LUGAR{"_BAR" if base else ""}.py — escalera p1: O1 + MEMORIA DE LUGAR del linaje (bins del anillo x lo que el sitio dio de mas que su letra).' + NL)]
    viaja = f'LG_VIAJA = {C1.LG_VIAJA}   # escalera p1b (humo 2): 1 = sin blanco a la vista, VIAJA al sitio recordado en vez de al hueco (0 = humo 1)' + NL
    if peldano == 'comp':
        A += [(viaja, viaja + f'COMPONE = {p}   # escalera p8: promotor (0 = O1_LUGAR bit a bit): el bono de lugar se suma tambien a letras mixtas' + NL),
              ('        if (v < 0).any(): return v' + NL + '        m = self._lg_leer(x)' + NL + '        bono = np.where((m > LG_MIN) & (v > 0), m, 0.0)' + NL,
               '        if (v < 0).any() and not COMPONE: return v   # escalera p8' + NL + '        m = self._lg_leer(x)' + NL
               + '        bono = np.where((m > LG_MIN) & ((v > 0) | bool(COMPONE)), m, 0.0)   # escalera p8' + NL)]
    elif peldano == 'plan':
        A += [(viaja, viaja + f'PLAN = {p}   # escalera p9: promotor (0 = O1_LUGAR bit a bit)' + NL
               + f'PLAN_BARAJA = {b}   # escalera p9: 1 = control (el credito va a la PENULTIMA letra: paso equivocado)' + NL
               + f'PLAN_W = {PLAN_W!r}; PL_LAM = {PL_LAM!r}; PL_MIN = {PL_MIN!r}   # escalera p9: peso de lo que habilita, EMA del credito, umbral' + NL),
              ('        if LUGAR: self._lg_init(ctx)   # escalera p1: memoria de lugar del linaje' + NL,
               '        if LUGAR: self._lg_init(ctx)   # escalera p1: memoria de lugar del linaje' + NL + '        if PLAN: self._pl_init()   # escalera p9' + NL),
              ('        if LUGAR: v = self._lg_v(v, self._lgx)   # escalera p1: el bocado vale lo de su letra + lo que el sitio recuerda' + NL,
               '        if PLAN: v = self._pl_v(v, k)   # escalera p9: + lo que la letra habilita' + NL
               + '        if LUGAR: v = self._lg_v(v, self._lgx)   # escalera p1: el bocado vale lo de su letra + lo que el sitio recuerda' + NL),
              ('            g = self._gana(self._lg_v(v, x) if LUGAR else v, lev)   # escalera p1' + NL,
               '            if PLAN: v = self._pl_v(v, k)   # escalera p9' + NL + '            g = self._gana(self._lg_v(v, x) if LUGAR else v, lev)   # escalera p1' + NL),
              ("        if LUGAR: self._lg_apr(res['pos'], k, dS)   # escalera p1: ANTES de actualizar la tabla por letra" + NL,
               "        if LUGAR: self._lg_apr(res['pos'], k, dS)   # escalera p1: ANTES de actualizar la tabla por letra" + NL
               + '        if PLAN: self._pl_apr(k, dS)   # escalera p9: ANTES de actualizar la tabla por letra' + NL),
              ("        if LUGAR: _m['_lugar'] = (self.lugar.copy(), self.nl.copy())   # escalera p1: la memoria de lugar es del linaje" + NL,
               "        if LUGAR: _m['_lugar'] = (self.lugar.copy(), self.nl.copy())   # escalera p1: la memoria de lugar es del linaje" + NL
               + "        if PLAN: _m['_plan'] = dict(self.hab)   # escalera p9" + NL),
              ("        if LUGAR and m and '_lugar' in m: m = dict(m); self._lg_hereda(m.pop('_lugar'))   # escalera p1" + NL,
               "        if LUGAR and m and '_lugar' in m: m = dict(m); self._lg_hereda(m.pop('_lugar'))   # escalera p1" + NL
               + "        if PLAN and m and '_plan' in m: m = dict(m); self._pl_hereda(m.pop('_plan'))   # escalera p9" + NL),
              ("        if LUGAR: return dict(self._salida_o1(), **self._lg_salida())   # escalera p1: la salida de O1 + la memoria de lugar" + NL,
               "        if PLAN: return dict(self._salida_o1(), **self._lg_salida(), **self._pl_salida())   # escalera p9" + NL
               + "        if LUGAR: return dict(self._salida_o1(), **self._lg_salida())   # escalera p1: la salida de O1 + la memoria de lugar" + NL)]
    elif peldano == 'preg':
        A += [(viaja, viaja + f'PREGUNTA = {p}   # escalera p10: promotor (0 = O1_LUGAR bit a bit)' + NL
               + f'PG_BARAJA = {b}   # escalera p10: 1 = control (va al ANTIPODA del bin menos visitado)' + NL
               + f'PG_OLVIDO = {PG_OLVIDO!r}   # escalera p10: olvido por presencia (por paso con necesidad y sin nada util a la vista)' + NL),
              ('        if LUGAR: self._lg_init(ctx)   # escalera p1: memoria de lugar del linaje' + NL,
               '        if LUGAR: self._lg_init(ctx)   # escalera p1: memoria de lugar del linaje' + NL + '        if PREGUNTA: self._pg_init()   # escalera p10' + NL),
              ("        self.st['pasos'] += 1" + NL,
               "        self.st['pasos'] += 1" + NL + "        if PREGUNTA: self.visto[self._lg_bin(pos)] = int(obs['t'])   # escalera p10" + NL),
              ('        limpia = mejor is None and min(lev) < self.U + MARGEN' + NL,
               '        limpia = mejor is None and min(lev) < self.U + MARGEN' + NL + '        if PREGUNTA: self._pg_olvida(pos, lev, mejor)   # escalera p10 (a)' + NL),
              ("            if tgt is None: tgt = self._hueco(pos, otros); self.st['sin_blanco'] += 1" + NL,
               "            if tgt is None and PREGUNTA: tgt = self._pg_meta(pos, int(obs['t']))   # escalera p10 (b)" + NL
               + "            if tgt is None: tgt = self._hueco(pos, otros); self.st['sin_blanco'] += 1" + NL),
              ("        if LUGAR: _m['_lugar'] = (self.lugar.copy(), self.nl.copy())   # escalera p1: la memoria de lugar es del linaje" + NL,
               "        if LUGAR: _m['_lugar'] = (self.lugar.copy(), self.nl.copy())   # escalera p1: la memoria de lugar es del linaje" + NL
               + "        if PREGUNTA: _m['_preg'] = self.visto.copy()   # escalera p10" + NL),
              ("        if LUGAR and m and '_lugar' in m: m = dict(m); self._lg_hereda(m.pop('_lugar'))   # escalera p1" + NL,
               "        if LUGAR and m and '_lugar' in m: m = dict(m); self._lg_hereda(m.pop('_lugar'))   # escalera p1" + NL
               + "        if PREGUNTA and m and '_preg' in m: m = dict(m); self._pg_hereda(m.pop('_preg'))   # escalera p10" + NL),
              ("        if LUGAR: return dict(self._salida_o1(), **self._lg_salida())   # escalera p1: la salida de O1 + la memoria de lugar" + NL,
               "        if PREGUNTA: return dict(self._salida_o1(), **self._lg_salida(), **self._pg_salida())   # escalera p10" + NL
               + "        if LUGAR: return dict(self._salida_o1(), **self._lg_salida())   # escalera p1: la salida de O1 + la memoria de lugar" + NL)]
    if METODOS[peldano]:
        A.append((NL + NL + 'def crea(ctx):' + NL, METODOS[peldano].replace('\n', NL) + NL + NL + 'def crea(ctx):' + NL))
    return A


def h16b(b): return hashlib.sha256(b).hexdigest()[:16]
def h16(p): return h16b(open(p, 'rb').read())


def verifica_origen():
    s = h16(os.path.join(AQUI, 'construye_p1.py'))
    if s != SHA_CONSTRUYE_P1: raise SystemExit(f"construye_c: construye_p1.py sha {s} != fijado {SHA_CONSTRUYE_P1} (P1 cambio: re-fijar y re-correr identidad_c)")
    for nm, sh in (('O1_LUGAR', SHA_O1_LUGAR), ('O1_LUGAR_BAR', SHA_O1_LUGAR_BAR)):
        t = h16b(C1.construye(nm, 1, int(nm.endswith('BAR'))))
        if t != sh: raise SystemExit(f"construye_c: el texto de {nm} sha {t} != fijado {sh}")


def construye(nombre, peldano, p, b, base):
    verifica_origen()
    txt = C1.construye('O1_LUGAR_BAR' if base else 'O1_LUGAR', 1, base).decode('utf-8')
    for a, rep in anclas(nombre, peldano, p, b, base):
        n = txt.count(a)
        if n != 1: raise SystemExit(f"construye_c {nombre}: ancla {a[:70]!r} aparece {n} veces (se exige 1)")
        txt = txt.replace(a, rep)
    return txt.encode('utf-8')


def todas(peldano=None):
    return {n: construye(n, pe, p, b, base) for n, pe, p, b, base in VARIANTES if peldano is None or pe == peldano}


def main(argv=None):
    ap = argparse.ArgumentParser(allow_abbrev=False)
    ap.add_argument('--verifica', action='store_true')
    a = ap.parse_args(argv)
    T = todas(); ok = True
    for n, b in T.items():
        ruta = os.path.join(SALIDA, n + '.py')
        if a.verifica:
            igual = os.path.exists(ruta) and open(ruta, 'rb').read() == b; ok &= igual
            print(f"  {n}: en disco == construido: {igual} (sha {h16b(b)})")
        else:
            os.makedirs(SALIDA, exist_ok=True); open(ruta, 'wb').write(b); print(f"  escrito {os.path.relpath(ruta, RAIZ)} sha {h16b(b)}")
    return 0 if ok else 1


if __name__ == '__main__':
    sys.exit(main())
