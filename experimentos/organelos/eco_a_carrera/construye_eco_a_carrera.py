"""construye_eco_a_carrera.py — construye POR ANCLAS los carros del bloque eco_a_carrera: el GENOMA que la seleccion natural produjo
en ECO_SEL (brazo SEL_C, FUNCIONA x2) puesto en el bicho de la carrera.

MISION: llegar a la AGI por este camino. Principio del director: que la evolucion construya el organo, no nosotros.

ORIGEN (solo se LEE; sha16 fijado; cada ancla debe aparecer EXACTAMENTE una vez o el constructor aborta):
  experimentos/organelos/frio_carrera/carros/V143_RES0.py (SHA = fab1d8068fe901a5): la traduccion de F1 a la carrera (el nacido lee el
  nodo del linaje sin neutras), construida por anclas desde tronco_v14_3/carros_v143/V143.py. Es la BASE de frio_carrera.

QUE ES EL GENOMA AQUI: los 15 genes del cerebro de JUACO-ECO (motor_eco.GENES menos la historia de vida) son EXACTAMENTE las perillas
que el carro lee de ctx['fabrica'] (eta, tau_e, alpha, hambre_boca, aversion, ema, paso, lam, memoria_rechazo, eta_s, clip_s, del_s,
del_c, ema_c) mas NK (celdas de Kenyon activas al nacer). G0 de ECO == pista.cfg_fabrica() de la carrera (verificado en el arnes).
El carro de ECO (FAMB_RES0_ECO) y V143 descienden los dos de FABRICA y leen esas perillas con los mismos nombres: el trasplante es de
VALORES, no de codigo. Declarado: V143 tiene piezas (B-5, FILTRO con META, boca TD) que no estaban en el linaje donde se selecciono.

PERILLAS (dos lineas de modulo):
  RES0 / BAR / TELEM   las de frio_carrera (BAR siempre 0 aqui; TELEM 1).
  GENOMA   None -> el carro es el de origen bit a bit. dict de los 15 genes -> __init__ los aplica (mismo camino para G0, SEL y AZA:
           canal simetrico). El RUNNER lo fija por corrida (genoma de la semilla ECO emparejada); el carro no lee archivos.
  FUENTE   etiqueta de que genoma espera el brazo ('G0', 'SEL_C', 'AZA_C'); el runner la verifica.
Genera en eco_a_carrera/carros/:
  EAC_G0     RES0 1, FUENTE 'G0'     (F1/G0: la base de frio_carrera con el genoma de fabrica, aplicado por el mismo camino)
  EAC_SEL    RES0 1, FUENTE 'SEL_C'  (HIPOTESIS: el genoma que la seleccion natural produjo, sobre el linaje F1)
  EAC_AZA    RES0 1, FUENTE 'AZA_C'  (CONTROL: el genoma del brazo sin herencia: varia igual, no se selecciona)
  EAC_SELV   RES0 0, FUENTE 'SEL_C'  (EXPLORATORIO: el genoma SEL_C sobre V143 sin RES0; con GENOMA None su fisica es V143)
Las variantes difieren SOLO en la linea de perillas y en el nombre (se verifica).

    python experimentos/organelos/eco_a_carrera/construye_eco_a_carrera.py [--verifica]
"""
import argparse, hashlib, os, sys

AQUI = os.path.dirname(os.path.abspath(__file__))
ORIGEN = os.path.join(os.path.dirname(AQUI), 'frio_carrera', 'carros', 'V143_RES0.py')
SALIDA = os.path.join(AQUI, 'carros')
SHA_ORIGEN = 'fab1d8068fe901a5'
NL = '\r\n'   # el origen tiene fin de linea CRLF (539/539); se conserva

VARIANTES = [('EAC_G0', 1, 'G0'), ('EAC_SEL', 1, 'SEL_C'), ('EAC_AZA', 1, 'AZA_C'), ('EAC_SELV', 0, 'SEL_C')]   # nombre, RES0, FUENTE
GENES = ('eta', 'tau_e', 'alpha', 'hambre_boca', 'aversion', 'ema', 'paso', 'lam', 'memoria_rechazo', 'eta_s', 'clip_s', 'del_s',
         'del_c', 'ema_c', 'NK')

PERILLAS = ("RES0 = {r}; BAR = 0; TELEM = 1   # eco_a_carrera: LA UNICA LINEA QUE CAMBIA ENTRE VARIANTES (con FUENTE)" + NL
            + "GENOMA = None; FUENTE = '{f}'   # eco_a_carrera: GENOMA lo fija el runner por corrida; None = el carro de origen bit a bit")

METODOS = '''
    # ================================================================ eco_a_carrera: el genoma de ECO_SEL en el carro
    # Los 15 genes del cerebro reemplazan a las perillas de fabrica ANTES de crear nada (NK decide cuantas celdas nacen activas).
    # Enteros como en motor_eco.ctx_genoma (int(round)). Nada lee el mundo ni consume rng.
    def _eg_aplica(self, g):
        if sorted(g) != sorted(EG_GENES): raise SystemExit(f"eco_a_carrera: GENOMA con genes {sorted(g)}")
        self.ETA = float(g['eta']); self.TAU_E = float(g['tau_e']); self.ALPHA = float(g['alpha']); self.HAMBRE_BOCA = float(g['hambre_boca'])
        self.AVERSION = float(g['aversion']); self.EMA = float(g['ema']); self.PASO = float(g['paso']); self.LAM = float(g['lam'])
        self.MEMORIA_RECHAZO = int(round(g['memoria_rechazo'])); self.ETA_S = float(g['eta_s']); self.CLIP_S = float(g['clip_s'])
        self.DEL_S = float(g['del_s']); self.DEL_C = float(g['del_c']); self.EMA_C = float(g['ema_c'])
        self.NK = int(round(g['NK']))
        if not 1 <= self.NK <= self.NKMAX: raise SystemExit(f"eco_a_carrera: NK {self.NK} fuera de [1, {self.NKMAX}]")

    def _eg_salida(self):
        return dict(fuente=FUENTE, genoma={k: float(GENOMA[k]) for k in EG_GENES},
                    aplicado=dict(eta=self.ETA, tau_e=self.TAU_E, alpha=self.ALPHA, hambre_boca=self.HAMBRE_BOCA, aversion=self.AVERSION,
                                  ema=self.EMA, paso=self.PASO, lam=self.LAM, memoria_rechazo=self.MEMORIA_RECHAZO, eta_s=self.ETA_S,
                                  clip_s=self.CLIP_S, del_s=self.DEL_S, del_c=self.DEL_C, ema_c=self.EMA_C, NK=self.NK))
'''

ANCLAS = [
    ('"""V143_RES0.py — frio_carrera (F1 en la pista de la carrera): V143 + el nacido lee el nodo del linaje sin neutras.' + NL,
     '"""{nombre}.py — eco_a_carrera: el genoma de ECO_SEL (15 genes del cerebro) sobre la base de frio_carrera.' + NL
     + 'GENERADO por experimentos/organelos/eco_a_carrera/construye_eco_a_carrera.py desde frio_carrera/carros/V143_RES0.py (sha {sha}).' + NL
     + 'NO editar a mano. Perillas: {perillas_txt}. Con GENOMA None es el origen (RES0 como aqui) bit a bit. Sigue el docstring del origen.' + NL + NL
     + 'V143_RES0.py — frio_carrera (F1 en la pista de la carrera): V143 + el nacido lee el nodo del linaje sin neutras.' + NL),
    ('RES0 = 1; BAR = 0; TELEM = 1   # frio_carrera: LA UNICA LINEA QUE CAMBIA ENTRE VARIANTES (0/0/0 = V143 bit a bit)' + NL,
     '{perillas}' + NL
     + "EG_GENES = " + repr(GENES) + NL),
    ('        NK, NKMAX, N_NEC = self.NK, self.NKMAX, self.N_NEC' + NL,
     '        if GENOMA is not None: self._eg_aplica(GENOMA)   # eco_a_carrera: el genoma reemplaza las perillas del cerebro' + NL
     + '        NK, NKMAX, N_NEC = self.NK, self.NKMAX, self.N_NEC' + NL),
    ("            **({'frio_carrera': self._fc_salida()} if TELEM else {}))   # frio_carrera: telemetria (ERR-96: no puntua)" + NL,
     "            **({'frio_carrera': self._fc_salida()} if TELEM else {})," + NL
     + "            **({'eco_a_carrera': self._eg_salida()} if GENOMA is not None else {}))   # eco_a_carrera: telemetria (no puntua)" + NL
     + '{metodos}'),
]


def h16b(b): return hashlib.sha256(b).hexdigest()[:16]
def h16(p): return h16b(open(p, 'rb').read())


def construye(nombre, r, f):
    src = open(ORIGEN, 'rb').read()
    if h16b(src) != SHA_ORIGEN: raise SystemExit(f"origen {ORIGEN} sha {h16b(src)} != {SHA_ORIGEN}")
    txt = src.decode('utf-8')
    per = PERILLAS.format(r=r, f=f)
    metodos = METODOS.replace('\n', NL)
    for a, rep in ANCLAS:
        n = txt.count(a)
        if n != 1: raise SystemExit(f"ancla {a[:70]!r} aparece {n} veces (se exige 1)")
        rep = (rep.replace('{nombre}', nombre).replace('{sha}', SHA_ORIGEN).replace('{perillas_txt}', per.split('   #')[0])
               .replace('{perillas}', per).replace('{metodos}', metodos))
        txt = txt.replace(a, rep)
    return txt.encode('utf-8')


def todas():
    return {n: construye(n, r, f) for n, r, f in VARIANTES}


def main(argv=None):
    ap = argparse.ArgumentParser(allow_abbrev=False)
    ap.add_argument('--verifica', action='store_true')
    a = ap.parse_args(argv)
    outs = todas()
    base = outs['EAC_G0'].decode('utf-8').split(NL)
    for n, bts in outs.items():
        ls = bts.decode('utf-8').split(NL)
        dif = [i for i, (x, y) in enumerate(zip(base, ls)) if x != y]
        if len(ls) != len(base) or any(not ('RES0 = ' in ls[i] or 'FUENTE = ' in ls[i] or n in ls[i]) for i in dif):
            raise SystemExit(f"{n}: difiere de EAC_G0 en algo mas que perillas/nombre: lineas {dif[:6]}")
    ok = True
    os.makedirs(SALIDA, exist_ok=True)
    for n, bts in outs.items():
        ruta = os.path.join(SALIDA, n + '.py')
        if a.verifica:
            igual = os.path.exists(ruta) and open(ruta, 'rb').read() == bts; ok &= igual
            print(f"  {n} sha {h16b(bts)} == disco: {igual}")
        else:
            with open(ruta, 'wb') as fh: fh.write(bts)
            print(f"  escrito {ruta} (sha {h16b(bts)})")
    print(f"origen V143_RES0.py sha {h16(ORIGEN)} (fijado {SHA_ORIGEN}) · construye_eco_a_carrera.py sha {h16(os.path.abspath(__file__))}")
    return 0 if ok else 1


if __name__ == '__main__':
    sys.exit(main())
