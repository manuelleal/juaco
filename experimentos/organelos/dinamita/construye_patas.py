"""construye_patas.py — construye POR ANCLAS el carro EXPLORATORIO TPATAS del bloque DINAMITA (ola 3: piezas de PATAS sobre TERMO).
EXPLORATORIO: nada de aqui es dato confirmatorio.

MISION: llegar a la AGI por este camino (organismo minimo con reglas locales, sin retropropagacion, peldanos preregistrados con
controles y replicas).

POR QUE PATAS (tras las olas 1 y 2): tocar lo sentido MALO en la boca (vetar al hambriento, o forzar al lleno a limpiar) hunde a TERMO
(0.23-0.30 y ~0.1): el mundo se tapa o el que limpia sale de la ventana. El diagnostico dice que el hijo de TERMO muere joven (<= 200) o
de hambre a los 600 sin comer. En el puenteo del comite 2 las PATAS de O1 solas llevaron a V143 a 0.949: la otra mitad de la brecha es
A DONDE VA el cuerpo. El motor de v14.3 es una politica aprendida con ruido que CRECE con el hambre (noise = .15 + .5 * hambre): el hijo
hambriento camina mas al azar.

PIEZA PATAS (una sola, en las PATAS; cero memoria nueva; sin rng nuevo -- el motor de v14.3 corre y consume su rng igual, y su
aprendizaje sigue; la pieza solo reemplaza el paso que sale):
    PATAS 1 DIRECTO:   un paso derecho hacia el objetivo que YA elige el ojo de v14.3 (_see); 0 si esta encima.
    PATAS 2 UTIL:      objetivo = el objeto mas cercano cuya letra la BOCA DE TERMO morderia ahora (sentida buena y alguna necesidad que
                       sube esta bajo rep_umbral + s/2: la misma lectura de TERMO); si no hay, el de _see; paso derecho.
    PATAS 3 UTIL+CEDE: como 2, pero descarta los utiles que otro cuerpo tiene ESTRICTAMENTE mas cerca (si todos lo estan, como 2).
    PATAS 4 INUTIL:    CONTROL desfasado de 2: objetivo = el mas cercano de lo sentido bueno que la boca NO morderia ahora; si no hay, _see.
Constantes: NINGUNA nueva (rep_umbral y el 1/2 de TERMO). Parecido con O1 (DECLARADO): O1 tambien va derecho (un paso) a un blanco
bueno "que le sirve" (ganancia > 0 <=> alguna necesidad que sube bajo rep_umbral + MARGEN, la misma forma que TERMO) y penaliza x0.35 el
blanco que otro tiene mas cerca (PEN_OTRO). PATAS 2/3 comparten la IDEA; no usan MARGEN, PEN_OTRO, D0, la ganancia ponderada por
urgencia (4/2/1), la neofobia, el hueco ni la limpieza. PATAS 3 es la mas cercana a O1 (exclusion en vez de penalizacion).
PERILLA PATAS (una linea nueva): 0 = V143_TERMO bit a bit (salida ENTERA). Telemetria de SOLO LECTURA en d['carro']['patas'] si PATAS != 0.

ORIGEN (solo se LEE; sha16 fijado; cada ancla EXACTAMENTE una vez o aborta):
  experimentos/organelos/termo/carros/V143_TERMO.py (SHA_TERMO = 3db639cab75641fb)
Genera en dinamita/carros/: TPATAS (una fuente; PATAS = 0 en disco; el modo lo pone el runner exploratorio en memoria por corrida).

    python experimentos/organelos/dinamita/construye_patas.py [--verifica]
"""
import argparse, hashlib, os, sys

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(AQUI)))
ORIGEN = os.path.join(RAIZ, 'experimentos', 'organelos', 'termo', 'carros', 'V143_TERMO.py')
SALIDA = os.path.join(AQUI, 'carros')
SHA_TERMO = '3db639cab75641fb'
NL = '\r\n'

VARIANTES = [('TPATAS', 0)]
PERILLAS = "PATAS = {v}   # dinamita-patas: LA UNICA LINEA QUE CAMBIA ENTRE VARIANTES (0 = V143_TERMO bit a bit; 1 DIRECTO; 2 UTIL; 3 UTIL+CEDE; 4 INUTIL control)"

METODOS = '''
    # ================================================================ dinamita-patas: A DONDE VA el cuerpo (una pieza de patas)
    # Lee lo SENTIDO por el linaje (_adS, el de TERMO), el estado presente (E, Ag), los objetos y la foto de los cuerpos (lo que la pista
    # ya entrega en obs). Solo reemplaza el paso que sale del motor de v14.3. Sin rng.
    def _pt_init(self, ctx):
        self._pt = dict(pasos=0, cambia=0, util=0, cede=0)

    def _pt_dir(self, pos, x):
        dl = (pos - x) % self.L; dr = (x - pos) % self.L
        if dl == 0: return 0
        return -1 if dl < dr else 1

    def _pt_mov(self, obs, pos, d, left, mf):
        g = self._pt; g['pasos'] += 1; L = self.L; tgt = None
        if PATAS in (2, 3, 4):
            lev = (float(obs['E']), float(obs['Ag'])); U = self._tmU; cands = []
            for x, k in obs['objs'].items():
                m = self._adS.get(k)
                if m is None or m[2] <= 0: continue
                s = (m[0] / m[2], m[1] / m[2])
                if s[0] < 0 or s[1] < 0 or not (s[0] > 0 or s[1] > 0): continue
                util = any(s[j] > 0 and lev[j] < U + s[j] / 2 for j in (0, 1))
                if util != (PATAS != 4): continue                              # 2/3: lo util · 4 (CONTROL): lo bueno que NO morderia
                cands.append((min((pos - x) % L, (x - pos) % L), x))
            if PATAS == 3 and cands:
                otros = [c[1] for c in obs['cuerpos'] if c[0] != obs['yo']]
                libres = [(dd, x) for dd, x in cands if not any(min((o - x) % L, (x - o) % L) < dd for o in otros)]
                if libres: g['cede'] += int(len(libres) < len(cands)); cands = libres
            if cands: tgt = min(cands)[1]; g['util'] += 1
        mv = (0 if d == 0 else (-1 if left else 1)) if tgt is None else self._pt_dir(pos, tgt)
        g['cambia'] += int(mv != mf)
        return mv

    def _pt_salida(self):
        return dict(patas=PATAS, **self._pt)
'''

ANCLAS = [
    ('"""V143_TERMO.py — termo: V143 + UNA pieza de boca (termostato de dos necesidades; ver construye_termo.py). Cero memoria nueva.' + NL,
     '"""{nombre}.py — dinamita (EXPLORATORIO): V143_TERMO + UNA pieza de PATAS (ver construye_patas.py).' + NL
     + 'GENERADO por experimentos/organelos/dinamita/construye_patas.py desde termo/carros/V143_TERMO.py (sha {sha}).' + NL
     + 'NO editar a mano. Perillas: {perillas_txt}. Con PATAS = 0 es V143_TERMO bit a bit. Sigue el docstring de V143_TERMO.' + NL + NL
     + 'V143_TERMO.py — termo: V143 + UNA pieza de boca (termostato de dos necesidades; ver construye_termo.py). Cero memoria nueva.' + NL),
    ('TERMO = 1   # termo: LA UNICA LINEA QUE CAMBIA ENTRE VARIANTES (0 = V143 bit a bit; 1 = TERMO; 2 = TERMOINV)' + NL,
     'TERMO = 1   # termo: LA UNICA LINEA QUE CAMBIA ENTRE VARIANTES (0 = V143 bit a bit; 1 = TERMO; 2 = TERMOINV)' + NL
     + '{perillas}' + NL),
    ('        self._tm_init(ctx)   # termo: solo contadores (sin rng)' + NL,
     '        self._tm_init(ctx)   # termo: solo contadores (sin rng)' + NL
     + '        self._pt_init(ctx)   # dinamita-patas: solo contadores (sin rng)' + NL),
    ('        mov = int(m[1] - m[0]); pos = (pos + mov) % self.L; d2, _, _ = self._see(pos, objs, t); Rp = .2 if d2 < d else 0.' + NL,
     '        mov = int(m[1] - m[0])' + NL
     + '        if PATAS: mov = self._pt_mov(obs, pos, d, left, mov)   # dinamita-patas: reemplaza SOLO el paso (el motor ya consumio su rng)' + NL
     + '        pos = (pos + mov) % self.L; d2, _, _ = self._see(pos, objs, t); Rp = .2 if d2 < d else 0.' + NL),
    ("            **({'termo': self._tm_salida()} if TERMO else {}))   # termo: telemetria (ERR-96: no puntua)" + NL,
     "            **({'termo': self._tm_salida()} if TERMO else {})," + NL
     + "            **({'patas': self._pt_salida()} if PATAS else {}))   # dinamita-patas: telemetria (ERR-96: no puntua)" + NL),
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
    print(f"origen V143_TERMO.py sha {h16(ORIGEN)} (fijado {SHA_TERMO}) · construye_patas.py sha {h16(os.path.abspath(__file__))}")
    return 0 if ok else 1


if __name__ == '__main__':
    sys.exit(main())
