"""construye_orac.py — SONDA 1 (1-oct-2026, EXPLORATORIA): construye POR ANCLAS, sobre el texto de O1_LUGAR que produce construye_p1 (sha
fijado, el mismo que fija construye_c), el ORACULO ESCRITO A MANO del mundo con llave no letal y su control al azar. NO SON CANDIDATOS: el
oraculo es una COTA (sabe por diseno que K es la llave y cuanto dura); nada de esto aprende nada nuevo.

MISION: llegar a la AGI por este camino (organismo minimo con reglas locales, sin retropropagacion, peldanos preregistrados con controles y replicas).

  ORACULO = 0 : O1_LUGAR bit a bit (arnes).
  ORACULO = 1 : TECHO. Si NO lleva llave vigente (t - ultima K mordida por ESTE cuerpo > OR_D - OR_MARGEN), el cuerpo aguanta (min nivel >
                OR_SEG) y hay una K a la vista: el blanco es la K mas cercana y la muerde. En todo lo demas es O1_LUGAR (que vuelve al oasis
                recordado). Es decir: K -> oasis, en ese orden, condicionado a su estado.
  ORACULO = 2 : AZAR. La misma maquinaria, pero la decision de ir por K NO mira la llave: una moneda (p 0.5) por bloque de OR_BLOQUE pasos
                (hash determinista del bloque y del indice del linaje; no consume rng). Apetito por K sin estado ni orden.
Genera en sondas/carros/: O1_LUGAR_ORAC, O1_LUGAR_AZAR, O1_LUGAR_ORAC0.
    python experimentos/organelos/escalera/sondas/construye_orac.py [--verifica]
"""
import argparse, hashlib, os, sys

AQUI = os.path.dirname(os.path.abspath(__file__))
ESC = os.path.dirname(AQUI)
RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(ESC)))
sys.path.insert(0, ESC)
import construye_p1 as C1
import construye_c as CC   # solo para sus shas fijados y verifica_origen

SALIDA = os.path.join(AQUI, 'carros')
NL = '\n'
OR_D = 600; OR_MARGEN = 50; OR_SEG = 0.4; OR_BLOQUE = 100; OR_K = 'K'
VARIANTES = [('O1_LUGAR_ORAC', 1), ('O1_LUGAR_AZAR', 2), ('O1_LUGAR_ORAC0', 0)]

METODOS = '''
    # ================================================================ sonda 1: ORACULO escrito a mano (cota, no candidato)
    def _or_init(self, ctx):
        self._or_tk = -10 ** 9; self._or_sal = 7919 * (int(ctx.get('indice', 0)) + 1)
        self.st['or_idas'] = 0; self.st['or_mord'] = 0

    def _or_falta(self, t):
        if ORACULO == 2: return ((((int(t) // OR_BLOQUE) + self._or_sal) * 2654435761) % 4294967296) >> 31 == 1   # AZAR: moneda por bloque
        return int(t) - self._or_tk > OR_D - OR_MARGEN                                                                # TECHO: no lleva llave

    def _or_blanco(self, obs, pos, lev, tgt):
        if min(lev) <= OR_SEG or not self._or_falta(obs['t']): return tgt
        best = None
        for x, k in obs['objs'].items():
            if k == OR_K:
                d = self._dist(pos, x)
                if best is None or d < best[0]: best = (d, x)
        if best is None: return tgt
        self.st['or_idas'] += 1
        return best[1]

    def _or_quiere(self, obs, lev):
        return min(lev) > OR_SEG and self._or_falta(obs['t'])
'''


def anclas(nombre, p):
    viaja = f'LG_VIAJA = {C1.LG_VIAJA}   # escalera p1b (humo 2): 1 = sin blanco a la vista, VIAJA al sitio recordado en vez de al hueco (0 = humo 1)' + NL
    return [
        ('"""O1_LUGAR.py — escalera p1: O1 + MEMORIA DE LUGAR del linaje (bins del anillo x lo que el sitio dio de mas que su letra).' + NL,
         f'"""{nombre}.py — sonda 1: O1_LUGAR + ORACULO escrito a mano (COTA, no candidato). ORACULO = {p} (0 = O1_LUGAR bit a bit, 1 = techo, 2 = azar).' + NL
         + 'GENERADO por experimentos/organelos/escalera/sondas/construye_orac.py sobre el texto de construye_p1 (sha fijado). NO editar a mano.' + NL + NL
         + 'O1_LUGAR.py — escalera p1: O1 + MEMORIA DE LUGAR del linaje (bins del anillo x lo que el sitio dio de mas que su letra).' + NL),
        (viaja, viaja + f'ORACULO = {p}   # sonda 1: 0 = O1_LUGAR bit a bit; 1 = techo (K si no lleva llave, luego oasis); 2 = azar (K por moneda, sin estado)' + NL
         + f'OR_D = {OR_D}; OR_MARGEN = {OR_MARGEN}; OR_SEG = {OR_SEG!r}; OR_BLOQUE = {OR_BLOQUE}; OR_K = {OR_K!r}   # sonda 1' + NL),
        ('        if LUGAR: self._lg_init(ctx)   # escalera p1: memoria de lugar del linaje' + NL,
         '        if LUGAR: self._lg_init(ctx)   # escalera p1: memoria de lugar del linaje' + NL + '        if ORACULO: self._or_init(ctx)   # sonda 1' + NL),
        ('        self.blanco = tgt' + NL,
         '        if ORACULO: tgt = self._or_blanco(obs, pos, lev, tgt)   # sonda 1' + NL + '        self.blanco = tgt' + NL),
        ("            if muerde and objs[p2] not in self.n: self.st['pruebas'] += 1" + NL,
         "            if ORACULO and objs[p2] == OR_K: muerde = muerde or self._or_quiere(obs, lev)   # sonda 1" + NL
         + "            if muerde and objs[p2] not in self.n: self.st['pruebas'] += 1" + NL),
        ("        k = res['letra']; dS = np.asarray(res['dS'], float)" + NL,
         "        k = res['letra']; dS = np.asarray(res['dS'], float)" + NL
         + "        if ORACULO and k == OR_K: self._or_tk = int(res['t']); self.st['or_mord'] += 1   # sonda 1" + NL),
        ("        self.st['cuerpos'] += 1; self.blanco = None" + NL,
         "        self.st['cuerpos'] += 1; self.blanco = None" + NL + "        if ORACULO: self._or_tk = -10 ** 9   # sonda 1: la llave es del cuerpo" + NL),
        (NL + NL + 'def crea(ctx):' + NL, METODOS.replace('\n', NL) + NL + NL + 'def crea(ctx):' + NL),
    ]


def h16b(b): return hashlib.sha256(b).hexdigest()[:16]


def construye(nombre, p):
    CC.verifica_origen()   # construye_p1.py y el texto de O1_LUGAR en sus shas fijados
    txt = C1.construye('O1_LUGAR', 1, 0).decode('utf-8')
    for a, rep in anclas(nombre, p):
        n = txt.count(a)
        if n != 1: raise SystemExit(f"construye_orac {nombre}: ancla {a[:70]!r} aparece {n} veces (se exige 1)")
        txt = txt.replace(a, rep)
    return txt.encode('utf-8')


def todas():
    return {n: construye(n, p) for n, p in VARIANTES}


def main(argv=None):
    ap = argparse.ArgumentParser(allow_abbrev=False); ap.add_argument('--verifica', action='store_true')
    a = ap.parse_args(argv); ok = True
    for n, b in todas().items():
        ruta = os.path.join(SALIDA, n + '.py')
        if a.verifica:
            igual = os.path.exists(ruta) and open(ruta, 'rb').read() == b; ok &= igual
            print(f"  {n}: en disco == construido: {igual} (sha {h16b(b)})")
        else:
            os.makedirs(SALIDA, exist_ok=True); open(ruta, 'wb').write(b); print(f"  escrito {os.path.relpath(ruta, RAIZ)} sha {h16b(b)}")
    return 0 if ok else 1


if __name__ == '__main__':
    sys.exit(main())
