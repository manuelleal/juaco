"""construye_juntos.py — construye POR ANCLAS el carro O1_TODO ("LOS TRES JUNTOS": memoria de lugar P1 + senal por pizarra P7 + modulo
PREGUNTA P10 en UN organismo, cada pieza con su perilla) sobre el texto de O1_LUGAR que produce construye_p1 (cadena: O1 sha
99436afa2715f028 -> O1_LUGAR (construye_p1) -> + anclas de construye_p7 (SENAL) -> + anclas de construye_c 'preg' (PREGUNTA)). 1-oct-2026.

MISION: llegar a la AGI por este camino (organismo minimo con reglas locales, sin retropropagacion, peldanos preregistrados con controles
y replicas).

COMO: NO se copia codigo de las piezas. Se IMPORTAN por sha construye_p7 y construye_c (congelados, commiteados) y se aplican SUS anclas y SUS
metodos, en orden P7 -> P10, sobre el texto de O1_LUGAR (cada ancla se exige 1 vez). Lo unico propio es la cabecera (las dos cabeceras de
origen anclan en la misma linea). Memoria nueva respecto de las piezas: CERO. Codigo nuevo de conducta: CERO (ninguna linea de union).
PERILLAS del carro (modulo): LUGAR (P1, siempre 1 aqui), SENAL + SN_BARAJA (P7), PREGUNTA + PG_BARAJA (P10).
  SENAL 0, PREGUNTA 0  => O1_LUGAR bit a bit            (arnes)
  SENAL 1, PREGUNTA 0  => O1_LUGAR_SENAL bit a bit      (arnes)
  SENAL 0, PREGUNTA 1  => O1_LUGAR_PREG bit a bit       (arnes)
Genera en juntos/carros/:
  O1_TODO       SENAL 1 SN_BARAJA 0 PREGUNTA 1   las tres                                  EL CANDIDATO
  O1_TODO_SBAR  SENAL 1 SN_BARAJA 1 PREGUNTA 1   las tres con la senal leida al ANTIPODA   CONTROL DE CONTENIDO
  O1_TODO_SEN   SENAL 1 SN_BARAJA 0 PREGUNTA 0   memoria + senal   (pareja; == O1_LUGAR_SENAL)
  O1_TODO_PREG  SENAL 0 SN_BARAJA 0 PREGUNTA 1   memoria + pregunta (pareja; == O1_LUGAR_PREG)
  O1_TODO0      SENAL 0 SN_BARAJA 0 PREGUNTA 0   solo memoria (solo arnes; == O1_LUGAR)
    python experimentos/organelos/escalera/juntos/construye_juntos.py [--verifica]
"""
import argparse, hashlib, os, sys

AQUI = os.path.dirname(os.path.abspath(__file__))
ESC = os.path.dirname(AQUI)
RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(ESC)))
sys.path.insert(0, ESC)
import construye_p1 as C1
import construye_p7 as C7
import construye_c as CC

SALIDA = os.path.join(AQUI, 'carros')
NL = '\n'
# ORIGEN por sha: los tres constructores congelados (commit 4154993f) y el texto de O1_LUGAR
SHA_ORIGEN = {'construye_p1.py': '90dc1b6f848fac80', 'construye_p7.py': '50179cf58798120c', 'construye_c.py': '024a89476109b997'}
SHA_O1_LUGAR = '49eee6bb278ea097'
# (nombre, SENAL, SN_BARAJA, PREGUNTA)   PG_BARAJA siempre 0 (el control de este bloque es el de la senal)
VARIANTES = [('O1_TODO', 1, 0, 1), ('O1_TODO_SBAR', 1, 1, 1), ('O1_TODO_SEN', 1, 0, 0), ('O1_TODO_PREG', 0, 0, 1), ('O1_TODO0', 0, 0, 0)]


def h16b(b): return hashlib.sha256(b).hexdigest()[:16]
def h16(p): return h16b(open(p, 'rb').read())


def verifica_origen():
    for nm, sh in SHA_ORIGEN.items():
        s = h16(os.path.join(ESC, nm))
        if s != sh: raise SystemExit(f"construye_juntos: {nm} sha {s} != fijado {sh} (el origen cambio: re-fijar y re-correr identidad_juntos)")
    t = h16b(C1.construye('O1_LUGAR', 1, 0))
    if t != SHA_O1_LUGAR: raise SystemExit(f"construye_juntos: el texto de O1_LUGAR sha {t} != fijado {SHA_O1_LUGAR}")


def anclas(nombre, s, sb, p):
    cab = '"""O1_LUGAR.py — escalera p1: O1 + MEMORIA DE LUGAR del linaje (bins del anillo x lo que el sitio dio de mas que su letra).' + NL
    A = [(cab, f'"""{nombre}.py — escalera JUNTOS: O1_LUGAR + SENAL (p7) + PREGUNTA (p10) en un organismo. SENAL = {s}, SN_BARAJA = {sb}, PREGUNTA = {p}, PG_BARAJA = 0.' + NL
          + 'GENERADO por experimentos/organelos/escalera/juntos/construye_juntos.py con las anclas de construye_p7 y construye_c (sha fijados). NO editar a mano.' + NL + NL
          + cab[3:])]
    A += C7.anclas(nombre, s, sb)[1:]                 # P7 sin su cabecera
    A += CC.anclas(nombre, 'preg', p, 0, 0)[1:]        # P10 sin su cabecera
    return A


def construye(nombre, s, sb, p):
    verifica_origen()
    txt = C1.construye('O1_LUGAR', 1, 0).decode('utf-8')
    for a, rep in anclas(nombre, s, sb, p):
        n = txt.count(a)
        if n != 1: raise SystemExit(f"construye_juntos {nombre}: ancla {a[:70]!r} aparece {n} veces (se exige 1)")
        txt = txt.replace(a, rep)
    return txt.encode('utf-8')


def todas():
    return {n: construye(n, s, sb, p) for n, s, sb, p in VARIANTES}


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
