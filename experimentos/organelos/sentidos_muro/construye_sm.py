"""construye_sm.py — SENTIDOS CONTRA EL MURO (29-sep-2026, creador; EXPLORATORIO). Construye POR ANCLAS el carro V143_BQ3.

MISION: llegar a la AGI por este camino (organismo minimo con reglas locales, sin retropropagacion, peldanos preregistrados con
controles y replicas). Principio del director: que la seleccion construya el organo, no nosotros.

ORIGEN (solo se LEE; sha16 fijado; cada ancla EXACTAMENTE una vez o aborta):
  experimentos/organelos/bloques_pista/carros/V143_BQ2.py (SHA_BQ2 = 183fb81cf6ad520c). Fin de linea CRLF (el del origen).
Lo que BQ2 YA SENTIA (declarado en el preregistro): 6 = cercania del objeto mas cercano con pixel j (j = 1 -> "A o C a la vista",
por IDENTIDAD de letra: instinto); 7 = la letra en foco ya fue mordida por el linaje; 8 = reserva min(E, Ag).
SENTIDOS NUEVOS (cero memoria nueva: leen _adS, lo SENTIDO por el linaje, que ya existe desde v14.3, y el anillo que la pista ya entrega):
  9  "algo BUENO a la vista" (aprendido, no por letra): cercania (1 - min(d, 20)/20) del objeto mas cercano del anillo cuya letra el
     linaje SINTIO buena (el mismo criterio que TERMO: media dE >= 0 y dAg >= 0, alguna > 0); 0 si no hay ninguna. Misma foto del anillo
     que el sentido 6 (posicion del inicio del paso; retraso de una celda declarado, igual que 6).
  10 "riesgo de morder": 1 - reserva si la letra en foco NO es sentida buena (desconocida o sentida mala); 0 si es sentida buena.
     Una sola regla "10 > th -> boca -w" dice "con reservas bajas no pruebes ni limpies; con reservas altas, si" (la regla PRUEBA de O1,
     que en BQ2 exige DOS reglas coordinadas: 'prueba_forzada' de bloques_pista).
PERILLA SENT3 (una linea): 0 -> NSEN 9 == V143_BQ2 BIT A BIT (tambien con tasas de exploracion: el sorteo de sentidos usa NSEN).
                           1 -> NSEN 11 (sentidos 9 y 10 disponibles para la gramatica; nada mas cambia: operadores, tasas, herencia, banco).
Genera en sentidos_muro/carros/: V143_BQ3 (SENT3 1) y V143_BQ3_0 (SENT3 0, solo arnes).

    python experimentos/organelos/sentidos_muro/construye_sm.py [--verifica]
"""
import argparse, hashlib, os, sys

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(AQUI)))
ORIGEN = os.path.join(RAIZ, 'experimentos', 'organelos', 'bloques_pista', 'carros', 'V143_BQ2.py')
SALIDA = os.path.join(AQUI, 'carros')
SHA_BQ2 = '183fb81cf6ad520c'
NL = '\r\n'
VARIANTES = [('V143_BQ3', 1), ('V143_BQ3_0', 0)]

SEN3 = '''
    # ================================================================ sentidos_muro: SENTIDOS 9 y 10 (leen _adS y el anillo; cero memoria nueva)
    def _bq_buena(self, k):
        m = self._adS.get(k)
        if m is None or m[2] <= 0: return False
        s0 = m[0] / m[2]; s1 = m[1] / m[2]
        return s0 >= 0 and s1 >= 0 and (s0 > 0 or s1 > 0)   # el mismo criterio que TERMO (_tm_boca)

    def _bq_s3(self, s, E, Ag, foco):
        if s == 10: return 0.0 if self._bq_buena(foco) else min(max(1.0 - min(E, Ag), 0.0), 1.0)
        pos, objs, L, cc = self._bqcache
        if 'b9' not in cc:
            dm = None
            for x, k in objs.items():
                if self._bq_buena(k):
                    dd = min((pos - x) % L, (x - pos) % L)
                    if dm is None or dd < dm: dm = dd
            cc['b9'] = 0.0 if dm is None else 1.0 - min(dm, 20) / 20.0
        return cc['b9']
'''


def anclas(nombre, s3):
    return [
        ('"""V143_BQ2.py — bloques_pista v2 (construye_bp2.py desde V143_BQ.py; sentidos 7 conocida y 8 reserva):',
         f'"""{nombre}.py — sentidos_muro (construye_sm.py desde bloques_pista/carros/V143_BQ2.py sha {SHA_BQ2}; SENT3 = {s3}; '
         'sentidos 9 bueno-a-la-vista y 10 riesgo). NO editar a mano. Con SENT3 = 0 es V143_BQ2 bit a bit.' + NL + NL
         + 'V143_BQ2.py — bloques_pista v2 (construye_bp2.py desde V143_BQ.py; sentidos 7 conocida y 8 reserva):'),
        ('NRMAX = 12; NSEN = 9; NACC = 3   # bloques_pista v2: sentidos 7 (conocida) y 8 (reserva)' + NL,
         f'SENT3 = {s3}   # sentidos_muro: LA UNICA LINEA QUE CAMBIA ENTRE VARIANTES (0 = V143_BQ2 bit a bit)' + NL
         + 'NRMAX = 12; NSEN = 11 if SENT3 else 9; NACC = 3   # bloques_pista v2: sentidos 7 (conocida) y 8 (reserva); sentidos_muro: 9 y 10' + NL),
        ('        if s == 8: return min(max(min(E, Ag), 0.0), 1.0)      # v2: reserva' + NL,
         '        if s == 8: return min(max(min(E, Ag), 0.0), 1.0)      # v2: reserva' + NL
         + '        if s >= 9: return self._bq_s3(s, E, Ag, foco)         # sentidos_muro: 9 bueno a la vista, 10 riesgo' + NL),
        ('    def _bq_cumple(self, r, E, Ag, d, foco):' + NL,
         SEN3.replace('\n', NL).lstrip(NL) + NL + '    def _bq_cumple(self, r, E, Ag, d, foco):' + NL),
    ]


def h16b(x): return hashlib.sha256(x).hexdigest()[:16]
def h16(p): return h16b(open(p, 'rb').read())


def construye(nombre, s3):
    src = open(ORIGEN, 'rb').read()
    if h16b(src) != SHA_BQ2: raise SystemExit(f"origen sha {h16b(src)} != {SHA_BQ2}")
    txt = src.decode('utf-8')
    for a, rep in anclas(nombre, s3):
        n = txt.count(a)
        if n != 1: raise SystemExit(f"ancla {a[:70]!r} aparece {n} veces (se exige 1)")
        txt = txt.replace(a, rep)
    return txt.encode('utf-8')


def todas(): return {n: construye(n, s) for n, s in VARIANTES}


def main(argv=None):
    ap = argparse.ArgumentParser(allow_abbrev=False); ap.add_argument('--verifica', action='store_true'); a = ap.parse_args(argv)
    outs = todas()
    b0 = outs['V143_BQ3'].decode('utf-8').split(NL); b1 = outs['V143_BQ3_0'].decode('utf-8').split(NL)
    dif = [i for i, (x, y) in enumerate(zip(b0, b1)) if x != y]
    if len(b0) != len(b1) or any('SENT3 = ' not in b0[i] for i in dif):
        raise SystemExit(f"las variantes difieren en algo mas que la perilla/nombre: lineas {dif[:6]}")
    ok = True; os.makedirs(SALIDA, exist_ok=True)
    for n, bts in outs.items():
        ruta = os.path.join(SALIDA, n + '.py')
        if a.verifica:
            i = os.path.exists(ruta) and open(ruta, 'rb').read() == bts; ok &= i; print(f"  {n} sha {h16b(bts)} == disco: {i}")
        else:
            open(ruta + '.tmp', 'wb').write(bts); os.replace(ruta + '.tmp', ruta); print(f"  escrito {ruta} (sha {h16b(bts)})")
    print(f"origen V143_BQ2.py sha {h16(ORIGEN)} (fijado {SHA_BQ2}) - construye_sm.py sha {h16(os.path.abspath(__file__))}")
    return 0 if ok else 1


if __name__ == '__main__':
    sys.exit(main())
