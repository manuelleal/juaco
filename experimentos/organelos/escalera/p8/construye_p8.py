"""construye_p8.py — P8 PROTOCOLO COMPLETO ("componer en celda retenida"): construye POR ANCLAS, sobre el texto de O1_LUGAR_COMP que produce
construye_c (sha fijado; cadena O1 -> construye_p1 -> construye_c -> aqui), el candidato COMP2. 1-oct-2026. DISENO, no seleccion.

MISION: llegar a la AGI por este camino (organismo minimo con reglas locales, sin retropropagacion, peldanos preregistrados con controles y replicas).

QUE CAMBIA EN COMP2 respecto de COMP (dos lineas de regla, CERO floats nuevos, cero memoria nueva):
  LG2 = 1      APRENDIZAJE: una mordida en un bin que YA recuerda bono (algun componente de lugar[bin] > LG_MIN, leido despues de _lg_apr) NO
               actualiza la tabla por letra (si la letra ya es conocida). La tabla aprende solo donde el sitio no da de mas: converge al valor de la
               letra FUERA del oasis y deja de absorber el extra; el bono (dS - valor de la letra) queda entero en la memoria de lugar.
  COMPONE = 2  COMPUERTA: el bono de lugar se suma a una letra mixta solo si la letra ALIMENTA algo (algun componente > 0). Con COMPONE = 1 (COMP)
               se suma a toda letra mixta. Motivo declarado ANTES de correr: con el bono entero (LG2) una suma sin compuerta volveria "buena" a B y D
               dentro del oasis (segunda puerta); la variante sin compuerta (COMP2SG) se pregunta sobre la misma memoria y se reporta.
Genera en p8/carros/:  O1_LUGAR_COMP2 (LG2 1, COMPONE 2: el candidato) · O1_LUGAR_COMP2SG (LG2 1, COMPONE 1: solo para preguntar) ·
                       O1_LUGAR_COMP2_0 (LG2 0, COMPONE 1: arnes, == O1_LUGAR_COMP bit a bit).
    python experimentos/organelos/escalera/p8/construye_p8.py [--verifica]
"""
import argparse, hashlib, os, sys

AQUI = os.path.dirname(os.path.abspath(__file__))
ESC = os.path.dirname(AQUI)
RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(ESC)))
sys.path.insert(0, ESC)
import construye_c as CC

SALIDA = os.path.join(AQUI, 'carros')
NL = '\n'
SHA_CONSTRUYE_C = '024a89476109b997'; SHA_O1_LUGAR_COMP = 'c75b4cdb9eec933d'
# (nombre, LG2, COMPONE)
VARIANTES = [('O1_LUGAR_COMP2', 1, 2), ('O1_LUGAR_COMP2SG', 1, 1), ('O1_LUGAR_COMP2_0', 0, 1)]


def anclas(nombre, lg2, comp):
    c1 = 'COMPONE = 1   # escalera p8: promotor (0 = O1_LUGAR bit a bit): el bono de lugar se suma tambien a letras mixtas' + NL
    tabla = '        self.suma[k] = self.suma.get(k, np.zeros(2)) + dS; self.n[k] = self.n.get(k, 0) + 1' + NL
    return [
        ('"""O1_LUGAR_COMP.py — escalera comp:',
         f'"""{nombre}.py — p8 protocolo: O1_LUGAR_COMP + COMP2 (LG2 = {lg2}: la tabla no aprende donde el sitio ya da bono; COMPONE = {comp}: 2 = compuerta "solo letras que alimentan").' + NL
         + 'GENERADO por experimentos/organelos/escalera/p8/construye_p8.py sobre el texto de construye_c (sha fijado). NO editar a mano.' + NL + NL
         + 'O1_LUGAR_COMP.py — escalera comp:'),
        (c1, f'COMPONE = {comp}   # escalera p8: promotor (0 = O1_LUGAR bit a bit): el bono de lugar se suma tambien a letras mixtas (2 = solo si la letra alimenta algo)' + NL
         + f'LG2 = {lg2}   # p8 protocolo: 1 = una mordida en un bin que ya recuerda bono NO actualiza la tabla por letra (0 = O1_LUGAR_COMP bit a bit)' + NL),
        ('        if (v < 0).any() and not COMPONE: return v   # escalera p8' + NL,
         '        if (v < 0).any() and not COMPONE: return v   # escalera p8' + NL
         + '        if COMPONE == 2 and (v < 0).any() and not (v > 0).any(): return v   # p8 protocolo: compuerta (una letra que no alimenta nada no recibe bono)' + NL),
        (tabla,
         "        if LG2 and k in self.n and (self.lugar[self._lg_bin(res['pos'])] > LG_MIN).any(): self.st['lg2_omit'] = self.st.get('lg2_omit', 0) + 1   # p8 protocolo" + NL
         + '        else: self.suma[k] = self.suma.get(k, np.zeros(2)) + dS; self.n[k] = self.n.get(k, 0) + 1' + NL),
    ]


def h16b(b): return hashlib.sha256(b).hexdigest()[:16]
def h16(p): return h16b(open(p, 'rb').read())


def construye(nombre, lg2, comp):
    s = h16(os.path.join(ESC, 'construye_c.py'))
    if s != SHA_CONSTRUYE_C: raise SystemExit(f"construye_p8: construye_c.py sha {s} != fijado {SHA_CONSTRUYE_C}")
    b = CC.construye('O1_LUGAR_COMP', 'comp', 1, 0, 0)
    if h16b(b) != SHA_O1_LUGAR_COMP: raise SystemExit(f"construye_p8: el texto de O1_LUGAR_COMP sha {h16b(b)} != fijado {SHA_O1_LUGAR_COMP}")
    txt = b.decode('utf-8')
    for a, rep in anclas(nombre, lg2, comp):
        n = txt.count(a)
        if n != 1: raise SystemExit(f"construye_p8 {nombre}: ancla {a[:70]!r} aparece {n} veces (se exige 1)")
        txt = txt.replace(a, rep)
    return txt.encode('utf-8')


def todas():
    return {n: construye(n, g, c) for n, g, c in VARIANTES}


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
