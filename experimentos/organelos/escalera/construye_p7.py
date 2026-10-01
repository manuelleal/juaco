"""construye_p7.py — construye POR ANCLAS el carro O1_LUGAR_SENAL (peldano 7: COMUNICACION con significado dado por la pizarra) sobre el texto
de O1_LUGAR que construye construye_p1 (cadena: O1 sha 99436afa2715f028 -> O1_LUGAR -> O1_LUGAR_SENAL). 30-sep-2026, MODO RAFAGA.

MISION: llegar a la AGI por este camino (organismo minimo con reglas locales, sin retropropagacion, peldanos preregistrados con controles y
replicas). Plan: ESCALERA.md (P7). Mundo: el de P1b (mundo_escalera: oasis denso, vista parcial). Runner: corre_p7.py.

PIEZA NUEVA (promotor SENAL; con SENAL = 0 el carro es O1_LUGAR bit a bit):
  EMITE: cada SN_CADA pasos, si su memoria de lugar tiene un bin VIVIDO (nl > 0) con bono total > SN_UMBRAL, escribe en la pizarra publica
         (canal que ya existe en la pista: hasta 8 numeros, CUPO 16, FIFO) la tripla (bin, bono_E, bono_Ag) de su mejor bin. Significado DADO
         por diseno (N2 ya mostro que no emerge por refuerzo; INNATO si sirve): "en el bin b me fue asi de bien".
  LEE:   al inicio de actua, las entradas nuevas de la pizarra que no son suyas; si el linaje NO ha estado en ese bin (nl == 0), SIEMBRA su
         memoria de lugar con lo leido (maximo, peso SN_W). Lo vivido manda sobre lo oido: en cuanto muerde alli, la EMA lo corrige.
  A quien paga: en monocultivo los 9 linajes son el MISMO carro (parientes): el que lee es un fundador limpio recien nacido (nace sin memoria) o
  un linaje que aun no encontro el oasis. Se declara: pago al linaje / a los parientes, no a un rival. Emitir no cuesta energia en este humo
  (declarado; el costo de emitir es una perilla de mundo pendiente, ESCALERA P7).
  CONTROL DE CONTENIDO (SN_BARAJA = 1): lee el bin del lado OPUESTO del anillo (b + 15 mod 30): oye lo mismo, siembra SIEMPRE un lugar
  equivocado (humo 1 usaba una permutacion fija: 4 de 30 bins caian en el oasis por azar y el control filtraba contenido; cambiado ANTES del
  humo 2). Control MUDO = O1_LUGAR (nadie escribe: es el mismo carro con SENAL 0).
  Memoria nueva: el ultimo t leido (1 entero) y 3 contadores. salida(): agrega sn_escribe, sn_lee, sn_siembra (st).
Genera en escalera/carros/:  O1_LUGAR_SENAL (SENAL 1, SN_BARAJA 0) · O1_LUGAR_SENAL_BAR (1, 1) · O1_LUGAR_SENAL0 (0, 0; solo arnes).
    python experimentos/organelos/escalera/construye_p7.py [--verifica]
"""
import argparse, hashlib, os, sys

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(AQUI)))
sys.path.insert(0, AQUI)
import construye_p1 as C1

SALIDA = os.path.join(AQUI, 'carros')
NL = '\n'
VARIANTES = [('O1_LUGAR_SENAL', 1, 0), ('O1_LUGAR_SENAL_BAR', 1, 1), ('O1_LUGAR_SENAL0', 0, 0)]
SN_CADA = 100; SN_UMBRAL = 0.3; SN_W = 1.0
# ORIGEN por sha (regla: importar por sha lo congelado de P1): construye_p1.py commiteado en 76dc3d11 (control antipoda, ERR-170) y el
# texto de O1_LUGAR que produce. Si P1 cambia, esto ABORTA hasta re-fijar (una linea) y re-correr identidad_p7.
SHA_CONSTRUYE_P1 = '90dc1b6f848fac80'; SHA_O1_LUGAR = '49eee6bb278ea097'


def h16b(b): return hashlib.sha256(b).hexdigest()[:16]
def h16(p): return h16b(open(p, 'rb').read())


def verifica_origen():
    s = h16(os.path.join(AQUI, 'construye_p1.py'))
    if s != SHA_CONSTRUYE_P1: raise SystemExit(f"construye_p7: construye_p1.py sha {s} != fijado {SHA_CONSTRUYE_P1} (P1 cambio: re-fijar y re-correr el arnes)")
    t = h16b(C1.construye('O1_LUGAR', 1, 0))
    if t != SHA_O1_LUGAR: raise SystemExit(f"construye_p7: el texto de O1_LUGAR sha {t} != fijado {SHA_O1_LUGAR}")

METODOS = '''
    # ================================================================ escalera p7: SENAL con significado dado por la pizarra
    def _sn_init(self):
        self._sn_ult = -1; self.st['sn_escribe'] = 0; self.st['sn_lee'] = 0; self.st['sn_siembra'] = 0

    def _sn_lee(self, obs):
        piz = obs.get('pizarra') or ()
        for e in piz:
            t, quien, c = e[0], e[1], e[2]
            if t <= self._sn_ult or quien == self.yo or len(c) < 3: continue
            b = int(c[0])
            if not 0 <= b < LG_NB: continue
            if SN_BARAJA: b = (b + LG_NB // 2) % LG_NB   # control: el lado OPUESTO del anillo (nunca toca el oasis: 4 bins contiguos)
            self.st['sn_lee'] += 1
            if self.nl[b] == 0:
                nuevo = np.array([float(c[1]), float(c[2])]) * SN_W
                if (nuevo > self.lugar[b]).any(): self.lugar[b] = np.maximum(self.lugar[b], nuevo); self.st['sn_siembra'] += 1
        if piz: self._sn_ult = max(self._sn_ult, max(e[0] for e in piz))

    def _sn_emite(self, t):
        if t % SN_CADA: return None
        s = self.lugar.sum(1); b = int(np.argmax(s))
        if s[b] <= SN_UMBRAL or self.nl[b] == 0: return None
        self.st['sn_escribe'] += 1
        return (float(b), float(self.lugar[b][0]), float(self.lugar[b][1]))
'''


def anclas(nombre, p, b):
    return [
        ('"""O1_LUGAR.py — escalera p1: O1 + MEMORIA DE LUGAR del linaje (bins del anillo x lo que el sitio dio de mas que su letra).' + NL,
         f'"""{nombre}.py — escalera p7: O1_LUGAR + SENAL por la pizarra (significado dado: bin y bono). SENAL = {p}, SN_BARAJA = {b}.' + NL
         + 'GENERADO por experimentos/organelos/escalera/construye_p7.py sobre el texto de O1_LUGAR (construye_p1). NO editar a mano.' + NL + NL
         + 'O1_LUGAR.py — escalera p1: O1 + MEMORIA DE LUGAR del linaje (bins del anillo x lo que el sitio dio de mas que su letra).' + NL),
        (f'LG_VIAJA = {C1.LG_VIAJA}   # escalera p1b (humo 2): 1 = sin blanco a la vista, VIAJA al sitio recordado en vez de al hueco (0 = humo 1)' + NL,
         f'LG_VIAJA = {C1.LG_VIAJA}   # escalera p1b (humo 2): 1 = sin blanco a la vista, VIAJA al sitio recordado en vez de al hueco (0 = humo 1)' + NL
         + f'SENAL = {p}   # escalera p7: promotor (0 = O1_LUGAR bit a bit)' + NL
         + f'SN_BARAJA = {b}   # escalera p7: 1 = control de contenido (lee el bin permutado)' + NL
         + f'SN_CADA = {SN_CADA}; SN_UMBRAL = {SN_UMBRAL!r}; SN_W = {SN_W!r}   # escalera p7: cada cuantos pasos emite, bono minimo para emitir, peso de lo oido' + NL),
        ('        if LUGAR: self._lg_init(ctx)   # escalera p1: memoria de lugar del linaje' + NL,
         '        if LUGAR: self._lg_init(ctx)   # escalera p1: memoria de lugar del linaje' + NL
         + '        if SENAL: self._sn_init()   # escalera p7' + NL),
        ("        otros = [c[1] for c in obs['cuerpos'] if c[0] != self.yo]" + NL,
         '        if SENAL: self._sn_lee(obs)   # escalera p7: lo oido siembra la memoria de lugar donde no se ha estado' + NL
         + "        otros = [c[1] for c in obs['cuerpos'] if c[0] != self.yo]" + NL),
        ('        return dict(mov=mov, muerde=muerde, escribe=None)' + NL,
         "        return dict(mov=mov, muerde=muerde, escribe=(self._sn_emite(obs['t']) if SENAL else None))   # escalera p7" + NL),
        (NL + NL + 'def crea(ctx):' + NL, METODOS.replace('\n', NL) + NL + NL + 'def crea(ctx):' + NL),
    ]


def construye(nombre, p, b):
    verifica_origen()
    txt = C1.construye('O1_LUGAR', 1, 0).decode('utf-8')   # el texto de O1_LUGAR (LUGAR 1, BARAJA 0) tal como lo construye construye_p1
    for a, rep in anclas(nombre, p, b):
        n = txt.count(a)
        if n != 1: raise SystemExit(f"ancla {a[:70]!r} aparece {n} veces (se exige 1)")
        txt = txt.replace(a, rep)
    return txt.encode('utf-8')


def todas():
    return {n: construye(n, p, b) for n, p, b in VARIANTES}


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
