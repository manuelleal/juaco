"""construye_pisa.py — construye POR ANCLAS la variante O1_SEN_PISA: O1_TODO_SEN (memoria + senal) donde LO OIDO PUEDE PISAR lo vivido
cuando lo vivido ya no vale. 1-oct-2026, MODO RAFAGA (no cuenta). Origen: el texto que produce juntos/construye_juntos.construye(nombre, 1, sb, 0)
(= O1_TODO_SEN salvo el nombre de la cabecera; construye_juntos sha d469c8f3bf194d64). Los originales NO se tocan.

MISION: llegar a la AGI por este camino (organismo minimo con reglas locales, sin retropropagacion, peldanos preregistrados con controles y replicas).

REGLA (local, UNA linea de conducta en _sn_lee, perilla SN_PISA; con SN_PISA = 0 el carro es O1_TODO_SEN bit a bit):
  al leer una entrada de la pizarra sobre el bin b: si el linaje YA estuvo alli (nl[b] > 0) y su memoria propia de b ya no vale
  (lugar[b].sum() <= LG_MIN: desmentida o nunca fue buena), pone nl[b] = 0 -> el bin vuelve a ser "no vivido" y la regla ORIGINAL de P7
  lo siembra con lo oido. Como nl[b] queda en 0, el linaje NO re-emite ese bin (la emision exige nl > 0) hasta que lo viva de nuevo:
  lo oido no se propaga como rumor. Lo vivido que TODAVIA vale (lugar[b].sum() > LG_MIN) sigue mandando sobre lo oido.
MEMORIA NUEVA: CERO floats (reutiliza nl). Telemetria: 1 contador (sn_pisa), solo con SN_PISA = 1.
Genera en mixto/carros/: O1_SEN_PISA (SN_BARAJA 0, SN_PISA 1) · O1_SEN_PISA_BAR (1, 1: lee al antipoda) · O1_SEN_PISA0 (0, 0: solo arnes).
    python experimentos/organelos/escalera/mixto/construye_pisa.py [--verifica]
"""
import argparse, hashlib, os, sys

AQUI = os.path.dirname(os.path.abspath(__file__)); ESC = os.path.dirname(AQUI)
sys.path.insert(0, ESC); sys.path.insert(0, os.path.join(ESC, 'juntos'))
import construye_juntos as CJ

SALIDA = os.path.join(AQUI, 'carros'); NL = '\n'
SHA_CJ = 'd469c8f3bf194d64'; SHA_O1_TODO_SEN = 'dff5e762bd23612e'
# (nombre, SN_BARAJA, SN_PISA)
VARIANTES = [('O1_SEN_PISA', 0, 1), ('O1_SEN_PISA_BAR', 1, 1), ('O1_SEN_PISA0', 0, 0)]


def h16b(b): return hashlib.sha256(b).hexdigest()[:16]
def h16(p): return h16b(open(p, 'rb').read())


def anclas(sb, p):
    a1 = f'SN_BARAJA = {sb}   # escalera p7: 1 = control de contenido (lee el bin permutado)' + NL
    a2 = "        self._sn_ult = -1; self.st['sn_escribe'] = 0; self.st['sn_lee'] = 0; self.st['sn_siembra'] = 0" + NL
    a3 = '            if self.nl[b] == 0:' + NL
    return [(a1, a1 + f'SN_PISA = {p}   # mixto: 1 = lo oido pisa lo vivido que ya no vale (0 = O1_TODO_SEN bit a bit)' + NL),
            (a2, a2 + "        if SN_PISA: self.st['sn_pisa'] = 0   # mixto (telemetria)" + NL),
            (a3, "            if SN_PISA and self.nl[b] > 0 and self.lugar[b].sum() <= LG_MIN: self.nl[b] = 0; self.st['sn_pisa'] += 1   # mixto: vuelve a 'no vivido'" + NL + a3)]


def construye(nombre, sb, p):
    s = h16(os.path.join(ESC, 'juntos', 'construye_juntos.py'))
    if s != SHA_CJ: raise SystemExit(f"construye_pisa: construye_juntos.py sha {s} != {SHA_CJ}")
    if h16b(CJ.construye('O1_TODO_SEN', 1, 0, 0)) != SHA_O1_TODO_SEN: raise SystemExit("construye_pisa: el texto de O1_TODO_SEN cambio")
    txt = CJ.construye(nombre, 1, sb, 0).decode('utf-8')
    for a, rep in anclas(sb, p):
        n = txt.count(a)
        if n != 1: raise SystemExit(f"construye_pisa {nombre}: ancla {a[:60]!r} aparece {n} veces (se exige 1)")
        txt = txt.replace(a, rep)
    return txt.encode('utf-8')


def todas(): return {n: construye(n, sb, p) for n, sb, p in VARIANTES}


def main(argv=None):
    ap = argparse.ArgumentParser(allow_abbrev=False); ap.add_argument('--verifica', action='store_true'); a = ap.parse_args(argv)
    ok = True
    for n, b in todas().items():
        ruta = os.path.join(SALIDA, n + '.py')
        if a.verifica:
            i = os.path.exists(ruta) and open(ruta, 'rb').read() == b; ok &= i; print(f"  {n}: en disco == construido: {i} (sha {h16b(b)})")
        else:
            os.makedirs(SALIDA, exist_ok=True); open(ruta, 'wb').write(b); print(f"  escrito {n}.py sha {h16b(b)}")
    return 0 if ok else 1


if __name__ == '__main__':
    sys.exit(main())
