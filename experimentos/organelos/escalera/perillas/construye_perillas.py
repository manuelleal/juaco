"""construye_perillas.py — construye POR ANCLAS el carro O1_LUGAR_GEN: O1_LUGAR (P1) con las DOS perillas del modulo de memoria de
lugar como GENES heredables continuos que ARRANCAN EN CERO (1-oct-2026, creador). Bloque "¿la seleccion prende lo que el mundo paga?".

MISION: llegar a la AGI por este camino (organismo minimo con reglas locales, sin retropropagacion, peldanos preregistrados con
controles y replicas).

ORIGEN (solo se LEE; cada ancla EXACTAMENTE una vez o aborta): el TEXTO de O1_LUGAR que arma escalera/construye_p1.py (sha16 del
constructor SHA_CP1 y del texto SHA_LUGAR fijados; construye_p1 a su vez parte de carrera_escuderias/carros/O1.py 99436afa2715f028).

PIEZA NUEVA (perilla PERILLAS; con PERILLAS = 0 el carro es O1_LUGAR bit a bit, salida ENTERA):
  GENOMA POR CUERPO = 2 genes continuos en [0, 1.5] (el cuerpo lee el gen tal cual):
    GW  peso del bono de lugar en el VALOR del bocado      valor = valor(letra) + GW * bono(sitio)          (P1: LUGAR_W = 1.0)
    GV  ganancia del VIAJE: sin blanco a la vista, va al sitio recordado solo si GV * recuerdo(bin) > LG_MIN (P1: LG_VIAJA = 1)
  Con (GW, GV) = (0, 0) el modulo es MUDO: el carro es O1 bit a bit (salvo la telemetria 'lugar': la memoria se sigue ESCRIBIENDO,
  pero nada la lee). Con (1, 1) es O1_LUGAR bit a bit (salida ENTERA). El arnes identidad_perillas.py comprueba las dos cosas.
  - MUTACION (una por nacimiento, en UN SOLO gen elegido al azar; el otro se copia igual): gen' = gen - PS_DELTA + N(0, PS_SIGMA),
    recortado a [0, 1.5]. PS_DELTA > 0 es un SESGO A LA PERDIDA (la perilla tiende a apagarse sola; solo la seleccion la sostiene):
    sin el, con un reloj largo, la deriva neutra cruza el umbral del viaje en buena parte de las cadenas y el control neutro deja de
    ser control. Con el sesgo la deriva neutra tiene una distribucion estacionaria pegada a 0 (el nulo esta en el preregistro).
  - Primer fundador de cada linaje en una corrida: base = una entrada de SIEMBRA al azar (uniforme) si SIEMBRA (lista de genomas
    {GW, GV, prof}, la fija el RUNNER entre pasajes) no es None; si es None, base = PS_BASE = (0, 0) con profundidad 0. Genes = base mutada.
  - CAMARA CONTINUA (PS_CAMARA 1): cada REFUNDACION (ENMIENDA 5: el linaje se extinguio y el mundo pone un fundador limpio) toma como
    base el genoma del cuerpo ACTUAL de OTRO linaje elegido al azar (uniforme entre los otros), mutado. Solo viajan los genes: la tabla
    y la memoria de lugar del fundador nacen vacias como siempre. El linaje que persiste es donante mas tiempo (seleccion por
    persistencia, sin juez) y las generaciones se ENCADENAN dentro de la corrida (el reloj corre aunque nadie se establezca).
  - Parto (al_parir): la memoria del hijo lleva '_gen' = (genes del padre mutados, profundidad + 1). Nace (nace): toma su '_gen'; el
    resto de la memoria (tabla por letra y memoria de lugar del LINAJE) no cambia.
  - RELOJ: cada genoma lleva su PROFUNDIDAD = numero de nacimientos (partos + fundaciones) que lo separan de la base (0, 0) del
    pasaje 0. Es el reloj real de la cadena (generaciones encadenadas = eventos de mutacion en su ascendencia), no los nacimientos.
  - Azar de la pieza: generador PROPIO (splitmix64 + Box-Muller, en Python puro; no usa numpy.random ni el rng del cuerpo ni el del
    mundo: el carro pasa el chequeo estatico revisa_carro), sembrado con (PS_SEMILLA, indice, instancia). PS_SEMILLA la fija el runner;
    _PS_CNT cuenta las instancias por linaje y el runner lo borra antes de cada run.
  - PS_LEE (la fija el runner; 1 por defecto): con 0 los genes se heredan, mutan, se muestrean y se transfieren IGUAL, pero el cuerpo NO
    los lee (decide con (0, 0), o sea como O1): es la cadena NEUTRA (deriva pura). Con PS_LEE 0 el carro es O1 con cualquier sigma.
  - Telemetria de SOLO ESCRITURA en _TEL[indice]: 'vivos' = [t, genes, instancia, profundidad] del cuerpo vivo cada 1000 pasos; 'fund'
    = [origen (0 base, 1 siembra, 2 camara), genes, profundidad] por fundador; 'partos' (conteo). Ningun carro la lee; el runner si.
  - _VIVO[indice] = (genes, profundidad) del cuerpo actual de cada linaje: lo UNICO que un fundador lee de otros linajes (la camara).
  Memoria nueva: 2 floats y un entero por cuerpo. salida() NO cambia (es la de O1_LUGAR).
Genera en perillas/carros/ (difieren SOLO en la linea PERILLAS y el nombre; se verifica):
  O1_LUGAR_GEN    PERILLAS 1
  O1_LUGAR_GEN0   PERILLAS 0 (solo arnes: == O1_LUGAR bit a bit)

    python experimentos/organelos/escalera/perillas/construye_perillas.py [--verifica]
"""
import argparse, ast, hashlib, os, sys

AQUI = os.path.dirname(os.path.abspath(__file__))
ESC = os.path.dirname(AQUI)
RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(ESC)))
if ESC not in sys.path: sys.path.insert(0, ESC)
import construye_p1 as CP1   # se IMPORTA y no se toca (sha fijado)

SALIDA = os.path.join(AQUI, 'carros')
SHA_CP1 = '90dc1b6f848fac80'      # escalera/construye_p1.py
SHA_LUGAR = '49eee6bb278ea097'    # el texto de O1_LUGAR que arma construye_p1 (= escalera/carros/O1_LUGAR.py)
NL = '\n'
VARIANTES = [('O1_LUGAR_GEN', 1), ('O1_LUGAR_GEN0', 0)]
GENES = ('GW', 'GV')
BASE = (0.0, 0.0)                 # de donde arranca la seleccion: modulo MUDO (== O1)
DISENO = (1.0, 1.0)               # el valor de DISENO de P1 (== O1_LUGAR): el techo 'fab'
CLIP = ((0.0, 1.5), (0.0, 1.5))   # recorte del gen (lo que el cuerpo lee)
SIGMA = 0.03                      # el de o1_evo y pasg (fijado a priori); UNA mutacion por nacimiento, en UN gen
DELTA = 0.01                      # sesgo a la perdida por mutacion (nulo de la deriva en el preregistro)
PER = "PERILLAS = {p}   # perillas: LA UNICA LINEA QUE CAMBIA ENTRE VARIANTES (0 = O1_LUGAR bit a bit)"


def modulo(p):
    return (NL + PER.format(p=p) + NL
            + f'SIEMBRA = None; PS_SEMILLA = 0; PS_SIGMA = {SIGMA!r}; PS_DELTA = {DELTA!r}; PS_LEE = 1; PS_CAMARA = 1   # perillas: los fija el RUNNER por corrida (SIEMBRA None = PS_BASE; PS_LEE 0 = genes NEUTROS)' + NL
            + '_PS_CNT = {}; _TEL = {}; _VIVO = {}   # perillas: instancias por linaje, telemetria de SOLO ESCRITURA y genoma del cuerpo actual de cada linaje (el runner los borra antes de cada run)' + NL
            + 'PS_GENES = ' + repr(GENES) + '; PS_BASE = ' + repr(BASE) + '; PS_CLIP = ' + repr(CLIP) + NL
            + '_PS_M64 = 18446744073709551615' + NL)


METODOS = '''
    # ================================================================ perillas: GW y GV como GENES heredables por cuerpo (arrancan en 0)
    def _ps_init(self, ctx):
        i = int(ctx['indice']); c = _PS_CNT.get(i, 0); _PS_CNT[i] = c + 1; self._psi = i; self._psc = c
        self._pss = ((int(PS_SEMILLA) * 1000003 + i * 10007 + c) * 2654435761 + 7703) & _PS_M64
        for _ in range(4): self._ps_u()
        otros = [_VIVO[j] for j in sorted(_VIVO) if j != i] if (PS_CAMARA and c > 0) else []
        if otros:   # CAMARA: la refundacion copia (mutado) el genoma del cuerpo actual de OTRO linaje al azar
            g, p0 = otros[int(self._ps_u() * len(otros)) % len(otros)]; b0 = list(g); self._psfund = 2
        elif SIEMBRA:
            e = SIEMBRA[int(self._ps_u() * len(SIEMBRA)) % len(SIEMBRA)]
            b0 = [float(e[k]) for k in PS_GENES]; p0 = int(e.get('prof', 0)); self._psfund = 1
        else:
            b0 = list(PS_BASE); p0 = 0; self._psfund = 0
        self._prof = int(p0) + 1
        self._ps_pon(self._ps_muta(b0))
        _TEL.setdefault(i, {}).setdefault('fund', []).append([self._psfund, list(self._gen), self._prof])

    def _ps_u(self):
        """generador PROPIO (splitmix64) -> uniforme en (0, 1). No toca el rng del mundo ni el del cuerpo."""
        self._pss = (self._pss + 0x9E3779B97F4A7C15) & _PS_M64
        z = self._pss
        z = ((z ^ (z >> 30)) * 0xBF58476D1CE4E5B9) & _PS_M64
        z = ((z ^ (z >> 27)) * 0x94D049BB133111EB) & _PS_M64
        z ^= z >> 31
        return ((z >> 11) + 0.5) / 9007199254740992.0

    def _ps_muta(self, b):
        """UNA mutacion por nacimiento, en UN gen al azar: gen - PS_DELTA + N(0, PS_SIGMA), recortado. El otro gen se copia igual."""
        out = [float(x) for x in b]; j = int(self._ps_u() * len(PS_GENES)) % len(PS_GENES)
        z = math.sqrt(-2.0 * math.log(self._ps_u())) * math.cos(2.0 * math.pi * self._ps_u())
        out[j] = float(min(max(out[j] - PS_DELTA + PS_SIGMA * z, PS_CLIP[j][0]), PS_CLIP[j][1]))
        return out

    def _ps_pon(self, g):
        self._gen = [float(x) for x in g]
        _VIVO[self._psi] = (list(self._gen), int(self._prof))
        if PS_LEE: self.GW, self.GV = self._gen
        else: self.GW, self.GV = 0.0, 0.0   # PS_LEE 0: se heredan y mutan pero NO se leen (el cuerpo decide como O1)

    def _ps_tel(self, t):
        _TEL.setdefault(self._psi, {}).setdefault('vivos', []).append([int(t), list(self._gen), int(self._psc), int(self._prof)])
'''


def anclas(nombre, p):
    return [
        ('"""O1_LUGAR.py — escalera p1: O1 + MEMORIA DE LUGAR del linaje (bins del anillo x lo que el sitio dio de mas que su letra).' + NL,
         f'"""{nombre}.py — perillas: O1_LUGAR con las dos perillas del modulo (GW valor, GV viaje) como GENES heredables que arrancan en 0.' + NL
         + f'GENERADO por experimentos/organelos/escalera/perillas/construye_perillas.py desde el texto de O1_LUGAR (sha {SHA_LUGAR}).' + NL
         + f'NO editar a mano. PERILLAS = {p}. Con PERILLAS = 0 es O1_LUGAR bit a bit; con genes (0, 0) es O1; con (1, 1), O1_LUGAR.' + NL + NL
         + 'O1_LUGAR.py — escalera p1: O1 + MEMORIA DE LUGAR del linaje (bins del anillo x lo que el sitio dio de mas que su letra).' + NL),
        ('import numpy as np' + NL, 'import math' + NL + 'import numpy as np' + NL),
        ('LG_VIAJA = 1   # escalera p1b (humo 2): 1 = sin blanco a la vista, VIAJA al sitio recordado en vez de al hueco (0 = humo 1)' + NL,
         'LG_VIAJA = 1   # escalera p1b (humo 2): 1 = sin blanco a la vista, VIAJA al sitio recordado en vez de al hueco (0 = humo 1)' + NL + modulo(p)),
        ('        if LUGAR: self._lg_init(ctx)   # escalera p1: memoria de lugar del linaje' + NL,
         '        if LUGAR: self._lg_init(ctx)   # escalera p1: memoria de lugar del linaje' + NL
         + '        self.GW, self.GV = float(LUGAR_W), float(LG_VIAJA)   # perillas: las dos perillas del modulo, por cuerpo (diseno de P1)' + NL
         + '        if PERILLAS: self._ps_init(ctx)   # perillas: genes del fundador (de la camara, de SIEMBRA o de PS_BASE = 0, 0), mutados' + NL),
        ('        return v + LUGAR_W * bono' + NL,
         '        if self.GW <= 0.0: return v   # perillas: gen de valor en 0 = O1' + NL
         + '        return v + self.GW * bono' + NL),
        ('            tgt = self._lg_meta(pos) if (LUGAR and LG_VIAJA) else None',
         '            tgt = self._lg_meta(pos) if (LUGAR and LG_VIAJA and self.GV > 0.0) else None'),
        ('            if s[b] <= LG_MIN: continue' + NL,
         '            if self.GV * s[b] <= LG_MIN: continue   # perillas: ganancia del viaje (1.0 = P1)' + NL),
        ('    def fin_paso(self, info):' + NL + '        return None' + NL,
         '    def fin_paso(self, info):' + NL
         + "        if PERILLAS and info['t'] % 1000 == 0: self._ps_tel(info['t'])   # perillas: genes del vivo (solo escritura)" + NL
         + '        return None' + NL),
        ("        if LUGAR: _m['_lugar'] = (self.lugar.copy(), self.nl.copy())   # escalera p1: la memoria de lugar es del linaje" + NL,
         "        if LUGAR: _m['_lugar'] = (self.lugar.copy(), self.nl.copy())   # escalera p1: la memoria de lugar es del linaje" + NL
         + "        if PERILLAS: _m['_gen'] = (self._ps_muta(self._gen), self._prof + 1); _TEL.setdefault(self._psi, {})['partos'] = _TEL[self._psi].get('partos', 0) + 1" + NL),
        ("        if LUGAR and m and '_lugar' in m: m = dict(m); self._lg_hereda(m.pop('_lugar'))   # escalera p1" + NL,
         "        if PERILLAS and m and '_gen' in m: m = dict(m); _g = m.pop('_gen'); self._prof = int(_g[1]); self._ps_pon(_g[0])   # perillas: el hijo toma sus genes" + NL
         + "        if LUGAR and m and '_lugar' in m: m = dict(m); self._lg_hereda(m.pop('_lugar'))   # escalera p1" + NL),
        (NL + NL + 'def crea(ctx):' + NL, METODOS.replace('\n', NL) + NL + NL + 'def crea(ctx):' + NL),
    ]


def h16b(b): return hashlib.sha256(b).hexdigest()[:16]
def h16(p): return h16b(open(p, 'rb').read())


def origen():
    s = h16(os.path.join(ESC, 'construye_p1.py'))
    if s != SHA_CP1: raise SystemExit(f"escalera/construye_p1.py sha {s} != {SHA_CP1}")
    src = CP1.construye('O1_LUGAR', 1, 0)
    if h16b(src) != SHA_LUGAR: raise SystemExit(f"texto de O1_LUGAR sha {h16b(src)} != {SHA_LUGAR}")
    return src.decode('utf-8')


def construye(nombre, p):
    txt = origen()
    for a, rep in anclas(nombre, p):
        n = txt.count(a)
        if n != 1: raise SystemExit(f"ancla {a[:70]!r} aparece {n} veces (se exige 1)")
        txt = txt.replace(a, rep)
    # LUGAR_W ya no se LEE como global en ningun metodo salvo __init__ (la copia) y _lg_salida (telemetria); LG_VIAJA solo en __init__ y actua
    for f in ast.walk(ast.parse(txt)):
        if isinstance(f, ast.FunctionDef):
            for g, permitidos in (('LUGAR_W', ('__init__', '_lg_salida')), ('LG_VIAJA', ('__init__', 'actua'))):
                usos = [nd.lineno for nd in ast.walk(f) if isinstance(nd, ast.Name) and nd.id == g and isinstance(nd.ctx, ast.Load)]
                if usos and f.name not in permitidos: raise SystemExit(f"{f.name}: quedan usos de {g} como global en las lineas {usos}")
    return txt.encode('utf-8')


def todas():
    return {n: construye(n, p) for n, p in VARIANTES}


def main(argv=None):
    ap = argparse.ArgumentParser(allow_abbrev=False)
    ap.add_argument('--verifica', action='store_true')
    a = ap.parse_args(argv)
    T = todas()
    l1 = T['O1_LUGAR_GEN'].decode().split(NL); l0 = T['O1_LUGAR_GEN0'].decode().split(NL)
    dif = [i for i, (x, y) in enumerate(zip(l1, l0)) if x != y]
    if len(l1) != len(l0) or len(dif) != 3: raise SystemExit(f"las variantes difieren en {dif} (se esperan 3 lineas: nombre, PERILLAS del encabezado y la perilla)")
    ok = True
    for n, b in T.items():
        ruta = os.path.join(SALIDA, n + '.py')
        if a.verifica:
            igual = os.path.exists(ruta) and open(ruta, 'rb').read() == b; ok &= igual
            print(f"  {n}: en disco == construido: {igual} (sha {h16b(b)})")
        else:
            os.makedirs(SALIDA, exist_ok=True)
            open(ruta, 'wb').write(b); print(f"  escrito {os.path.relpath(ruta, RAIZ)} sha {h16b(b)}")
    return 0 if ok else 1


if __name__ == '__main__':
    sys.exit(main())
