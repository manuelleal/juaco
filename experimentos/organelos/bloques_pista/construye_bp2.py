"""construye_bp2.py — BLOQUES_PISTA v2: dos SENTIDOS mas para "cuando probar / cuando limpiar" (28-sep-2026, creador; EXPLORATORIO).

MISION: llegar a la AGI por este camino. Principio del director: que la evolucion construya el organo, no nosotros, y solo con seleccion natural.

Por que (lectura de la exploracion v1, 59201-59205, y de la sonda termo_organo): el fundador de TERMO muere a los ~43 pasos por veneno+sal
(99 %) porque prueba letras DESCONOCIDAS sin mirar sus reservas (dote 0.6; dos golpes de -0.4 lo matan). O1 solo prueba lo desconocido con
E y Ag > 0.5. Con los sentidos v1 (hambre, sed, pixeles, ultima mordida, alrededor) una regla NO puede distinguir "desconocida" de "conocida":
eso vive en la memoria del linaje (_adS, lo SENTIDO al morder; ya existe en v14.3). v2 lo deja LEER a las reglas:
  sentido 7 = la letra en foco ya fue mordida por el linaje (1) o no (0)        [lee _adS: memoria que ya existia; cero memoria nueva]
  sentido 8 = reserva = min(E, Ag) recortada a [0, 1]
Nada mas cambia (operadores, tasas, herencia, banco). NSEN 7 -> 9.

ORIGEN (solo se LEE; sha16 fijado; cada ancla EXACTAMENTE una vez): bloques_pista/carros/V143_BQ.py (31cfda6b3efca02f) y V143_BQAZA.py
(a9182feec29f1a83). Genera V143_BQ2 (padre) y V143_BQ2AZA (azar). Con genoma vacio y tasas 0 siguen siendo V143_TERMO bit a bit (arnes).

    python experimentos/organelos/bloques_pista/construye_bp2.py [--verifica]
"""
import argparse, hashlib, os, sys

AQUI = os.path.dirname(os.path.abspath(__file__))
CARROS = os.path.join(AQUI, 'carros')
ORIGENES = {'V143_BQ2': ('V143_BQ', '31cfda6b3efca02f'), 'V143_BQ2AZA': ('V143_BQAZA', 'a9182feec29f1a83')}
NL = '\r\n'


def anclas(nombre, orig):
    return [
        (f'"""{orig}.py — bloques_pista:', f'"""{nombre}.py — bloques_pista v2 (construye_bp2.py desde {orig}.py; sentidos 7 conocida y 8 reserva):'),
        ('NRMAX = 12; NSEN = 7; NACC = 3' + NL, 'NRMAX = 12; NSEN = 9; NACC = 3   # bloques_pista v2: sentidos 7 (conocida) y 8 (reserva)' + NL),
        ('        pos, objs, L, cc = self._bqcache' + NL,
         '        if s == 7: return 1.0 if foco in self._adS else 0.0   # v2: la letra en foco ya fue mordida por el linaje' + NL
         + '        if s == 8: return min(max(min(E, Ag), 0.0), 1.0)      # v2: reserva' + NL
         + '        pos, objs, L, cc = self._bqcache' + NL),
    ]


def h16b(b): return hashlib.sha256(b).hexdigest()[:16]


def construye(nombre):
    orig, sha = ORIGENES[nombre]
    src = open(os.path.join(CARROS, orig + '.py'), 'rb').read()
    if h16b(src) != sha: raise SystemExit(f"origen {orig} sha {h16b(src)} != {sha}")
    txt = src.decode('utf-8')
    for a, rep in anclas(nombre, orig):
        n = txt.count(a)
        if n != 1: raise SystemExit(f"ancla {a[:70]!r} aparece {n} veces (se exige 1)")
        txt = txt.replace(a, rep)
    return txt.encode('utf-8')


def todas(): return {n: construye(n) for n in ORIGENES}


def main(argv=None):
    ap = argparse.ArgumentParser(allow_abbrev=False); ap.add_argument('--verifica', action='store_true'); a = ap.parse_args(argv)
    ok = True
    for n, b in todas().items():
        ruta = os.path.join(CARROS, n + '.py')
        if a.verifica:
            i = os.path.exists(ruta) and open(ruta, 'rb').read() == b; ok &= i; print(f"  {n} sha {h16b(b)} == disco: {i}")
        else:
            open(ruta + '.tmp', 'wb').write(b); os.replace(ruta + '.tmp', ruta); print(f"  escrito {ruta} (sha {h16b(b)})")
    print(f"construye_bp2.py sha {h16b(open(os.path.abspath(__file__), 'rb').read())}")
    return 0 if ok else 1


if __name__ == '__main__':
    sys.exit(main())
