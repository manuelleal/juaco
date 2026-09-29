"""construye_organo.py — SONDA EXPLORATORIA (28-sep-2026, noche): el ORGANO DE RECHAZO que la seleccion fijo en ECO (BLOQUES, BLOQ_V)
trasplantado, por anclas, sobre V143_TERMO en la pista de la carrera. NO es preregistro ni intento contra el muro.

MISION: llegar a la AGI por este camino (organismo minimo con reglas locales, sin retropropagacion, peldanos preregistrados con
controles y replicas).

ORGANO (tal cual quedo fijado; referencia FORZ2_V de bloques/opusM/corre_bloques.py: genoma EVOLUCIONADO del linaje 66 de BLOQ_V s48402):
  dos copias de la regla (sentido 3 = pixel j del objeto en la celda al morder, comparador '<', theta 0.06, accion boca, w -2.97)
  con j = 1  ->  "no muerdas si falta el pixel 1"; peso total -5.94 sumado a Vb ANTES del sigmoide de la boca de fabrica (igual que
  motor_bloques: Vb += _reglas_boca(...)), es decir antes de FILTRO, APR y TERMO. PAT de la pista == PAT de ECO (F9C.PAT):
  pixel 1 = 0 exactamente en B (veneno) y D (sal).
  ORGANO = 2 (control desfasado): la MISMA regla leyendo el pixel 0 (falta en C agua y D sal: una buena y una mala; no separa lo malo).
  ORGANO = 0: V143_TERMO bit a bit (arnes identidad_organo.py).
Cero memoria nueva (contadores de telemetria aparte); sin rng.

ORIGEN (solo se LEE; sha16 fijado): experimentos/organelos/termo/carros/V143_TERMO.py (3db639cab75641fb).
    python experimentos/organelos/termo_organo/construye_organo.py [--verifica]
"""
import argparse, hashlib, os, sys

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(AQUI)))
ORIGEN = os.path.join(RAIZ, 'experimentos', 'organelos', 'termo', 'carros', 'V143_TERMO.py')
SALIDA = os.path.join(AQUI, 'carros')
SHA_ORIGEN = '3db639cab75641fb'
NL = '\r\n'
VARIANTES = [('V143_TERMO_ORG0', 0), ('V143_TERMO_ORG', 1), ('V143_TERMO_ORGDES', 2)]
PERILLA = "ORGANO = {o}   # organo: LA UNICA LINEA QUE CAMBIA ENTRE VARIANTES (0 = V143_TERMO bit a bit; 1 = pixel 1; 2 = DESFASADO pixel 0)"
REGLA = "ORG_REGLA = (0.06, -2.97, 2)   # (theta, w, copias) del organo fijado en BLOQ_V (FORZ2_V); comparador '<'; pixel = 1 u 0 segun ORGANO"

METODOS = '''
    # ================================================================ organo: RECHAZO POR LA RETINA (trasplantado de ECO/BLOQUES)
    def _org_init(self):
        self._org = dict(opp={k: 0 for k in 'ABCD'}, disp={k: 0 for k in 'ABCD'})

    def _org_boca(self, kk):
        j = 1 if ORGANO == 1 else 0
        th, w, n = ORG_REGLA
        self._org['opp'][kk] += 1
        if float(self.PAT[kk][j]) < th:
            self._org['disp'][kk] += 1
            return n * w
        return 0.0
'''

ANCLAS = [
    ('"""V143_TERMO.py — termo: V143 + UNA pieza de boca (termostato de dos necesidades; ver construye_termo.py). Cero memoria nueva.' + NL,
     '"""{nombre}.py — organo: V143_TERMO + el ORGANO DE RECHAZO fijado en ECO (ver construye_organo.py). SONDA EXPLORATORIA.' + NL
     + 'GENERADO por experimentos/organelos/termo_organo/construye_organo.py desde termo/carros/V143_TERMO.py (sha {sha}). NO editar a mano.' + NL
     + 'Perillas: {perillas_txt}. Con ORGANO = 0 es V143_TERMO bit a bit. Sigue el docstring de V143_TERMO.' + NL + NL
     + 'V143_TERMO.py — termo: V143 + UNA pieza de boca (termostato de dos necesidades; ver construye_termo.py). Cero memoria nueva.' + NL),
    ('TERMO = 1   # termo: LA UNICA LINEA QUE CAMBIA ENTRE VARIANTES (0 = V143 bit a bit; 1 = TERMO; 2 = TERMOINV)' + NL,
     'TERMO = 1   # termo: LA UNICA LINEA QUE CAMBIA ENTRE VARIANTES (0 = V143 bit a bit; 1 = TERMO; 2 = TERMOINV)' + NL
     + '{perilla}' + NL + REGLA + NL),
    ('        self._tm_init(ctx)   # termo: solo contadores (sin rng)' + NL,
     '        self._tm_init(ctx)   # termo: solo contadores (sin rng)' + NL + '        self._org_init()   # organo: solo contadores' + NL),
    ('            Vb = self.ALPHA * _wt + self.HAMBRE_BOCA * hambre + .5' + NL,
     '            Vb = self.ALPHA * _wt + self.HAMBRE_BOCA * hambre + .5' + NL
     + '            if ORGANO: Vb += self._org_boca(kk)   # organo: como motor_bloques (Vb += reglas de boca), antes de FILTRO/APR/TERMO' + NL),
    ('        return dict(termo=TERMO, **self._tm)' + NL,
     "        return dict(termo=TERMO, **self._tm, **({'organo': ORGANO, 'org': self._org} if ORGANO else {}))" + NL + '{metodos}'),
]


def h16b(b): return hashlib.sha256(b).hexdigest()[:16]
def h16(p): return h16b(open(p, 'rb').read())


def construye(nombre, o):
    src = open(ORIGEN, 'rb').read()
    if h16b(src) != SHA_ORIGEN: raise SystemExit(f"origen {ORIGEN} sha {h16b(src)} != {SHA_ORIGEN}")
    txt = src.decode('utf-8'); per = PERILLA.format(o=o)
    for a, rep in ANCLAS:
        n = txt.count(a)
        if n != 1: raise SystemExit(f"ancla {a[:70]!r} aparece {n} veces (se exige 1)")
        rep = (rep.replace('{nombre}', nombre).replace('{sha}', SHA_ORIGEN).replace('{perillas_txt}', per.split('   #')[0])
               .replace('{perilla}', per).replace('{metodos}', METODOS.replace('\n', NL)))
        txt = txt.replace(a, rep)
    return txt.encode('utf-8')


def main(argv=None):
    ap = argparse.ArgumentParser(allow_abbrev=False); ap.add_argument('--verifica', action='store_true'); a = ap.parse_args(argv)
    outs = {n: construye(n, o) for n, o in VARIANTES}
    base = outs['V143_TERMO_ORG0'].decode('utf-8').split(NL)
    for n, bts in outs.items():
        ls = bts.decode('utf-8').split(NL)
        dif = [i for i, (x, y) in enumerate(zip(base, ls)) if x != y]
        if len(ls) != len(base) or any(not ('ORGANO = ' in ls[i] or n in ls[i]) for i in dif):
            raise SystemExit(f"{n}: difiere de ORG0 en algo mas que perilla/nombre: lineas {dif[:6]}")
    ok = True; os.makedirs(SALIDA, exist_ok=True)
    for n, bts in outs.items():
        ruta = os.path.join(SALIDA, n + '.py')
        if a.verifica:
            igual = os.path.exists(ruta) and open(ruta, 'rb').read() == bts; ok &= igual; print(f"  {n} sha {h16b(bts)} == disco: {igual}")
        else:
            with open(ruta + '.tmp', 'wb') as fh: fh.write(bts)
            os.replace(ruta + '.tmp', ruta); print(f"  escrito {ruta} (sha {h16b(bts)})")
    print(f"origen V143_TERMO.py sha {h16(ORIGEN)} (fijado {SHA_ORIGEN}) · construye_organo.py sha {h16(os.path.abspath(__file__))}")
    return 0 if ok else 1


if __name__ == '__main__':
    sys.exit(main())
