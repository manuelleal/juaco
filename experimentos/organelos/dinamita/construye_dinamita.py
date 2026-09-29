"""construye_dinamita.py — construye POR ANCLAS los carros EXPLORATORIOS del bloque DINAMITA (piezas locales genericas SOBRE TERMO
contra el muro de la carrera; 28-sep-2026). EXPLORATORIO: nada de aqui es dato confirmatorio.

MISION: llegar a la AGI por este camino (organismo minimo con reglas locales, sin retropropagacion, peldanos preregistrados con
controles y replicas).

DIAGNOSTICO (diagnostico.py, sobre los JSON ya corridos de TERMO 39101-39140): lo que separa a TERMO de O1 en la puerta P1 no es el
fundador sino el HIJO: 10-22 % de los hijos de TERMO mueren antes de 200 pasos (nacen a 0.6, muerden una letra que el LINAJE ya sabe
mala y quedan a 0.2), contra 0.4-0.6 % en O1; paren el 53 % contra el 70 %, y la cola se vacia (91/360 linajes caen contra 24/360).
TERMO decide solo sobre lo SENTIDO BUENO; lo sentido malo lo sigue decidiendo la boca de v14.3 (hambre -> muerde).

PIEZA VETO (una sola, en la BOCA; cero memoria nueva; sin rng): sobre una letra k cuyo dS SENTIDO por el linaje (s = _adS, el mismo
que usa TERMO) tiene alguna componente NEGATIVA, la pieza solo puede QUITAR una mordida que v14.3 ya decidio (nunca fuerza):
    VETO 1 (U):     no muerde si  existe j con s_j < 0 y nivel_j + s_j < rep_umbral       ("el golpe no me saca de la ventana")
    VETO 2 (H):     no muerde si  existe j con s_j < 0 y nivel_j < rep_umbral + |s_j| / 2 ("termostato de dos lados": la MISMA
                    consigna U + |s|/2 de TERMO, leida al reves: lo malo solo si estoy por ENCIMA de la consigna)
    VETO 3 (U+NAV): VETO 1 y ademas lo vetado en este paso es OBSTACULO para las patas (se suma a los obstaculos del FILTRO de v14.3)
    VETO 4 (UINV):  CONTROL desfasado de VETO 1: la misma regla leyendo el nivel de la necesidad que el golpe NO toca (nivel_{1-j})
    VETO 5 (W):     dosis baja: no muerde si existe j con s_j < 0 y nivel_j < rep_umbral ("solo dentro de la ventana")
Constantes: NINGUNA nueva (rep_umbral de ctx; el 1/2 es el de TERMO). Parecido con O1 (DECLARADO): O1._costeable tambien prohibe un
golpe que baje la necesidad golpeada de rep_umbral cuando la ventana corre (y de PISO 0.2 si no corre) y exige que caiga en la
necesidad MAS llena y que no haya nada util; VETO 1 comparte SOLO la clausula "no bajar de rep_umbral" y no tiene PISO, ni 'mas llena',
ni disparador, ni fuerza limpiezas.
PERILLA VETO (una linea nueva): 0 = V143_TERMO bit a bit (salida ENTERA). Telemetria de SOLO LECTURA en d['carro']['veto'] si VETO != 0.

ORIGEN (solo se LEE; sha16 fijado; cada ancla EXACTAMENTE una vez o aborta):
  experimentos/organelos/termo/carros/V143_TERMO.py (SHA_TERMO = 3db639cab75641fb; el candidato TERMO, TERMO = 1)
Genera en dinamita/carros/: TVETO (una sola fuente; el modo lo fija la perilla VETO al cargar -- el runner exploratorio la pone por
corrida) y, para el intento #4 si lo hay, variantes con la perilla fija.

    python experimentos/organelos/dinamita/construye_dinamita.py [--verifica]
"""
import argparse, hashlib, os, sys

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(AQUI)))
ORIGEN = os.path.join(RAIZ, 'experimentos', 'organelos', 'termo', 'carros', 'V143_TERMO.py')
SALIDA = os.path.join(AQUI, 'carros')
SHA_TERMO = '3db639cab75641fb'
NL = '\r\n'   # el origen tiene fin de linea CRLF; se conserva

VARIANTES = [('TVETO', 0)]   # exploratorio: una fuente, VETO = 0 en disco (== V143_TERMO); el modo se pone en memoria por corrida
PERILLAS = "VETO = {v}   # dinamita: LA UNICA LINEA QUE CAMBIA ENTRE VARIANTES (0 = V143_TERMO bit a bit; 1 U; 2 H; 3 U+NAV; 4 UINV control; 5 W; 6 LIMPIA_U; 7 LIMPIA_UINV control; 8 LIMPIA_H)"

METODOS = '''
    # ================================================================ dinamita: VETO de lo sentido malo (una pieza de boca)
    # Lee lo SENTIDO por el linaje (_adS, el mismo de TERMO) y el estado presente (E, Ag). Solo QUITA mordidas. Sin rng.
    def _vm_init(self, ctx):
        self._vmU = float(ctx['rep_umbral'])
        self._vm = dict(dec=0, a_no=0, obst=0)

    def _vm_malo(self, kk):
        m = self._adS.get(kk)
        if m is None or m[2] <= 0: return None
        s = (m[0] / m[2], m[1] / m[2])
        return s if (s[0] < 0 or s[1] < 0) else None

    def _vm_prohibe(self, s, E, Ag):
        lev = (float(E), float(Ag)); U = self._vmU
        if VETO in (1, 3): return any(s[j] < 0 and lev[j] + s[j] < U for j in (0, 1))
        if VETO == 2: return any(s[j] < 0 and lev[j] < U - s[j] / 2 for j in (0, 1))
        if VETO == 4: return any(s[j] < 0 and lev[1 - j] + s[j] < U for j in (0, 1))   # CONTROL: la necesidad que el golpe NO toca
        if VETO == 5: return any(s[j] < 0 and lev[j] < U for j in (0, 1))
        raise SystemExit(f"VETO invalido {VETO!r}")

    def _vm_boca(self, kk, E, Ag, mf):
        s = self._vm_malo(kk)
        if s is None: return mf                                                 # no es malo sentido: TERMO / v14.3
        if VETO >= 6: return self._vm_decide(s, E, Ag, mf)
        no = self._vm_prohibe(s, E, Ag)
        g = self._vm; g['dec'] += 1; g['a_no'] += int(mf and no)
        return bool(mf and not no)

    # ola 2 (tras ver la ola 1: el veto solo tapa el mundo): la pieza DECIDE en los dos sentidos sobre lo sentido malo
    #   6 LIMPIA_U:    muerde <=> para todo j con s_j < 0: nivel_j + s_j >= rep_umbral   (el que puede pagar el golpe sin salir de la
    #                  ventana, LIMPIA; el que no, no muerde)
    #   7 LIMPIA_UINV: CONTROL desfasado de 6: lee el nivel de la necesidad que el golpe NO toca
    #   8 LIMPIA_H:    muerde <=> para todo j con s_j < 0: nivel_j >= rep_umbral + |s_j| / 2 (termostato de dos lados, constante de TERMO)
    def _vm_decide(self, s, E, Ag, mf):
        lev = (float(E), float(Ag)); U = self._vmU
        if VETO == 6: b = all(lev[j] + s[j] >= U for j in (0, 1) if s[j] < 0)
        elif VETO == 7: b = all(lev[1 - j] + s[j] >= U for j in (0, 1) if s[j] < 0)
        elif VETO == 8: b = all(lev[j] >= U - s[j] / 2 for j in (0, 1) if s[j] < 0)
        else: raise SystemExit(f"VETO invalido {VETO!r}")
        g = self._vm; g['dec'] += 1; g['a_no'] += int(mf and not b); g['a_si'] = g.get('a_si', 0) + int(b and not mf)
        return bool(b)

    def _vm_obst(self, E, Ag):
        o = []
        for k in self.PAT:
            s = self._vm_malo(k)
            if s is not None and self._vm_prohibe(s, E, Ag): o.append(k)
        o = frozenset(o)
        self._vm['obst'] += int(bool(o - self._v3o))
        return o

    def _vm_salida(self):
        return dict(veto=VETO, **self._vm)
'''

ANCLAS = [
    ('"""V143_TERMO.py — termo: V143 + UNA pieza de boca (termostato de dos necesidades; ver construye_termo.py). Cero memoria nueva.' + NL,
     '"""{nombre}.py — dinamita (EXPLORATORIO): V143_TERMO + UNA pieza de boca (VETO de lo sentido malo; ver construye_dinamita.py).' + NL
     + 'GENERADO por experimentos/organelos/dinamita/construye_dinamita.py desde termo/carros/V143_TERMO.py (sha {sha}).' + NL
     + 'NO editar a mano. Perillas: {perillas_txt}. Con VETO = 0 es V143_TERMO bit a bit. Sigue el docstring de V143_TERMO.' + NL + NL
     + 'V143_TERMO.py — termo: V143 + UNA pieza de boca (termostato de dos necesidades; ver construye_termo.py). Cero memoria nueva.' + NL),
    ('TERMO = 1   # termo: LA UNICA LINEA QUE CAMBIA ENTRE VARIANTES (0 = V143 bit a bit; 1 = TERMO; 2 = TERMOINV)' + NL,
     'TERMO = 1   # termo: LA UNICA LINEA QUE CAMBIA ENTRE VARIANTES (0 = V143 bit a bit; 1 = TERMO; 2 = TERMOINV)' + NL
     + '{perillas}' + NL),
    ('        self._tm_init(ctx)   # termo: solo contadores (sin rng)' + NL,
     '        self._tm_init(ctx)   # termo: solo contadores (sin rng)' + NL
     + '        self._vm_init(ctx)   # dinamita: solo contadores (sin rng)' + NL),
    ('        if FILTRO: self._v3_prep(objs, _na)' + NL,
     '        if FILTRO: self._v3_prep(objs, _na)' + NL
     + '        if VETO == 3: self._v3o = self._v3o | self._vm_obst(E, Ag)   # dinamita U+NAV: lo vetado tampoco es blanco' + NL),
    ('            if TERMO: mordio = self._tm_boca(kk, E, Ag, mordio)   # termo: manda sobre lo sentido bueno (despues de FILTRO y APR)' + NL,
     '            if TERMO: mordio = self._tm_boca(kk, E, Ag, mordio)   # termo: manda sobre lo sentido bueno (despues de FILTRO y APR)' + NL
     + '            if VETO: mordio = self._vm_boca(kk, E, Ag, mordio)   # dinamita: solo QUITA mordidas de lo sentido malo' + NL),
    ("            **({'termo': self._tm_salida()} if TERMO else {}))   # termo: telemetria (ERR-96: no puntua)" + NL,
     "            **({'termo': self._tm_salida()} if TERMO else {})," + NL
     + "            **({'veto': self._vm_salida()} if VETO else {}))   # dinamita: telemetria (ERR-96: no puntua)" + NL),
    ('    def _tm_salida(self):' + NL + '        return dict(termo=TERMO, **self._tm)' + NL,
     '    def _tm_salida(self):' + NL + '        return dict(termo=TERMO, **self._tm)' + NL + '{metodos}'),
]


def h16b(b): return hashlib.sha256(b).hexdigest()[:16]
def h16(p): return h16b(open(p, 'rb').read())


def construye(nombre, v):
    src = open(ORIGEN, 'rb').read()
    if h16b(src) != SHA_TERMO: raise SystemExit(f"origen {ORIGEN} sha {h16b(src)} != {SHA_TERMO}")
    txt = src.decode('utf-8')
    per = PERILLAS.format(v=v)
    metodos = METODOS.replace('\n', NL)
    for a, rep in ANCLAS:
        n = txt.count(a)
        if n != 1: raise SystemExit(f"ancla {a[:70]!r} aparece {n} veces (se exige 1)")
        rep = (rep.replace('{nombre}', nombre).replace('{sha}', SHA_TERMO).replace('{perillas_txt}', per.split('   #')[0])
               .replace('{perillas}', per).replace('{metodos}', metodos))
        txt = txt.replace(a, rep)
    return txt.encode('utf-8')


def todas():
    return {n: construye(n, v) for n, v in VARIANTES}


def main(argv=None):
    ap = argparse.ArgumentParser(allow_abbrev=False)
    ap.add_argument('--verifica', action='store_true')
    a = ap.parse_args(argv)
    outs = todas(); ok = True
    os.makedirs(SALIDA, exist_ok=True)
    for n, bts in outs.items():
        ruta = os.path.join(SALIDA, n + '.py')
        if a.verifica:
            igual = os.path.exists(ruta) and open(ruta, 'rb').read() == bts; ok &= igual
            print(f"  {n} sha {h16b(bts)} == disco: {igual}")
        else:
            tmp = ruta + '.tmp'
            with open(tmp, 'wb') as fh: fh.write(bts)
            os.replace(tmp, ruta)
            print(f"  escrito {ruta} (sha {h16b(bts)})")
    print(f"origen V143_TERMO.py sha {h16(ORIGEN)} (fijado {SHA_TERMO}) · construye_dinamita.py sha {h16(os.path.abspath(__file__))}")
    return 0 if ok else 1


if __name__ == '__main__':
    sys.exit(main())
