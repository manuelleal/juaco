"""construye_pas.py — construye POR ANCLAS los carros de PASAJES SERIADOS en la pista de la carrera (reunion 28-sep-2026, Opus B).
EXPLORATORIO. Nada de esto es serie.

MISION: llegar a la AGI por este camino (organismo minimo con reglas locales, sin retropropagacion, peldanos preregistrados con
controles y replicas). Principio del director: que la evolucion construya el organo, no nosotros, y solo con seleccion natural.

ORIGEN (solo se LEE; sha16 fijado; cada ancla EXACTAMENTE una vez o aborta):
  experimentos/organelos/termo_banco/carros/V143_EVO_BAJO.py (SHA_BAJO = 3187b373654e119f; = construye_evo('V143_EVO_BAJO') de la nube,
  desde tronco_v14_3/carros_v143/V143.py). Es V143 + termostato de boca con el margen g como GEN por cuerpo (con g = 0.40 es TERMO/m40
  en la fisica, arnes de termo_banco). Fin de linea CRLF (el del origen).

PIEZA NUEVA (perilla PASAJE; con PASAJE = 0 el carro es V143_EVO_BAJO bit a bit, salida ENTERA):
  GENOMA POR CUERPO = (g, b): g el margen del termostato (ya en EVO_BAJO) y b = los 15 genes del cerebro de JUACO-ECO (los mismos
  nombres de eco_a_carrera: eta tau_e alpha hambre_boca aversion ema paso lam memoria_rechazo eta_s clip_s del_s del_c ema_c NK).
  - Fundador (crea(ctx): el primero y cada refundacion de la ENMIENDA 5): si SIEMBRA (lista de genomas, la fija el RUNNER entre pasajes)
    es None -> g ~ U[G_INI] como EVO_BAJO (mismo rng, mismos sorteos) y b = G0 (fabrica) mutado; si no -> una entrada de SIEMBRA al azar
    (uniforme) con g + N(0, SIGMA) recortado a G_CLIP y b mutado.
  - Parto: el hijo lleva g (como EVO_BAJO) y b mutado (memoria opaca de la cola; V143 no usa memoria). Nace: aplica su b.
  - Mutacion de b: la de motor_eco.muta (log-normal por gen con probabilidad PS_MUT[0], sigma PS_MUT[1]; enteros redondeados y
    empujados +-1; rango [max(piso, G0/4), min(techo, 4 G0)]; NK ademas <= NKMAX). La fija el runner (defecto ECO: p 0.05, sigma 0.15).
  - rng de la pieza: np.random.default_rng([PS_SEMILLA, indice, instancia, 7701]) (PS_SEMILLA la fija el runner; _PS_CNT cuenta las
    instancias por linaje y el runner lo borra antes de cada run). No toca el rng del mundo, ni el del cuerpo, ni rng_hijo, ni el del gen.
  - Telemetria de SOLO ESCRITURA en _TEL[indice] (el dict de EVO_BAJO): 'vivos_b' = [t, g, b] del cuerpo vivo cada 1000 pasos;
    'fund_ps' = [de_siembra, g] por fundador. Ningun carro la lee; el runner la lee al terminar el run (ERR-96: no puntua).
Genera en opusB/carros/ (difieren SOLO en la linea PASAJE y el nombre; se verifica):
  V143_PAS    PASAJE 1
  V143_PAS0   PASAJE 0 (solo arnes: == V143_EVO_BAJO bit a bit)

    python experimentos/organelos/reunion/opusB/construye_pas.py [--verifica]
"""
import argparse, hashlib, os, sys

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(AQUI))))
ORIGEN = os.path.join(RAIZ, 'experimentos', 'organelos', 'termo_banco', 'carros', 'V143_EVO_BAJO.py')
SALIDA = os.path.join(AQUI, 'carros')
SHA_BAJO = '3187b373654e119f'
NL = '\r\n'

VARIANTES = [('V143_PAS', 1), ('V143_PAS0', 0)]
GENES = ('eta', 'tau_e', 'alpha', 'hambre_boca', 'aversion', 'ema', 'paso', 'lam', 'memoria_rechazo', 'eta_s', 'clip_s', 'del_s',
         'del_c', 'ema_c', 'NK')
# pisos y techos duros de motor_eco.GENES (mismo orden); enteros: memoria_rechazo y NK
PISO = (1e-4, 0.05, 0.01, 0.01, 0.01, 1e-3, 1e-3, 1e-3, 1, 1e-3, 0.5, 0.01, 0.01, 1e-3, 6)
TECHO = (1.0, 0.99, 20.0, 20.0, 20.0, 0.5, 2.0, 0.5, 200, 2.0, 50.0, 1.0, 1.0, 0.5, 90)
ENTERO = (0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1)
PER = "PASAJE = {p}   # opusB pasajes: LA UNICA LINEA QUE CAMBIA ENTRE VARIANTES (0 = V143_EVO_BAJO bit a bit)"

MODULO = ('SIEMBRA = None; PS_SEMILLA = 0; PS_MUT = (0.05, 0.15)   # opusB: los fija el RUNNER por corrida (SIEMBRA None = la inicial)' + NL
          + '_PS_CNT = {}   # opusB: instancias por linaje (el runner lo borra antes de cada run)' + NL
          + 'PS_GENES = ' + repr(GENES) + NL + 'PS_PISO = ' + repr(PISO) + NL + 'PS_TECHO = ' + repr(TECHO) + NL
          + 'PS_ENTERO = ' + repr(ENTERO) + NL)

METODOS = '''
    # ================================================================ opusB PASAJES: genoma (g, cerebro) por cuerpo; fundador de SIEMBRA
    def _ps_init(self, ctx):
        i = int(ctx['indice']); c = _PS_CNT.get(i, 0); _PS_CNT[i] = c + 1
        self._psrng = np.random.default_rng([int(PS_SEMILLA), i, c, 7701])
        cf = ctx['fabrica']; g0 = [float(cf['NK'] if k == 'NK' else cf['kw'][k]) for k in PS_GENES]
        self._pslo = [max(PS_PISO[j], g0[j] / 4) for j in range(len(PS_GENES))]
        self._pshi = [min(PS_TECHO[j], g0[j] * 4) for j in range(len(PS_GENES))]
        self._pshi[PS_GENES.index('NK')] = min(self._pshi[PS_GENES.index('NK')], float(cf['NKMAX']))
        base = SIEMBRA[int(self._psrng.integers(len(SIEMBRA)))] if SIEMBRA else None
        b0 = [float(base['b'][k]) for k in PS_GENES] if base is not None else g0
        self._psb = self._ps_muta(b0)
        self._ps_g0 = (float(min(max(float(base['g']) + float(self._psrng.normal(0.0, SIGMA)), G_CLIP[0]), G_CLIP[1]))
                       if base is not None else None)
        self._psfund = int(base is not None)
        self._ps_aplica(self._psb)

    def _ps_muta(self, b):
        p, s = PS_MUT; NG = len(PS_GENES); u = self._psrng.random(NG); z = self._psrng.normal(0.0, s, NG); h = list(b)
        for j in range(NG):
            if u[j] < p:
                v = h[j] * math.exp(z[j])
                if PS_ENTERO[j]:
                    v = float(round(v))
                    if v == h[j]: v = h[j] + (1.0 if z[j] > 0 else -1.0)
                h[j] = min(max(v, self._pslo[j]), self._pshi[j])
        return h

    def _ps_aplica(self, b):
        d = dict(zip(PS_GENES, b))
        self.ETA = float(d['eta']); self.TAU_E = float(d['tau_e']); self.ALPHA = float(d['alpha']); self.HAMBRE_BOCA = float(d['hambre_boca'])
        self.AVERSION = float(d['aversion']); self.EMA = float(d['ema']); self.PASO = float(d['paso']); self.LAM = float(d['lam'])
        self.MEMORIA_RECHAZO = int(round(d['memoria_rechazo'])); self.ETA_S = float(d['eta_s']); self.CLIP_S = float(d['clip_s'])
        self.DEL_S = float(d['del_s']); self.DEL_C = float(d['del_c']); self.EMA_C = float(d['ema_c'])
        self.NK = int(round(d['NK']))

    def _ps_nace(self, info):
        m = info.get('memoria')
        if m is not None and 'b' in m: self._psb = list(m['b']); self._ps_aplica(self._psb)

    def _ps_tel(self, t):
        self._ev_tel().setdefault('vivos_b', []).append([int(t), float(self._g), [float(x) for x in self._psb]])

    def _ps_fund(self):
        self._ev_tel().setdefault('fund_ps', []).append([self._psfund, round(float(self._g), 5)])
'''


def anclas(nombre, p):
    per_evo = "EVO = 1; G_INI = (-0.1, 0.1); SIGMA = 0.03; G_CLIP = (-0.2, 1.0)"
    return [
        ('"""V143_EVO_BAJO.py — termo_evo: V143 + termostato de boca con el margen como GEN heredable (ver construye_evo.py).' + NL,
         f'"""{nombre}.py — opusB PASAJES: V143_EVO_BAJO + genoma (g, 15 genes del cerebro) por cuerpo y fundador de SIEMBRA.' + NL
         + f'GENERADO por experimentos/organelos/reunion/opusB/construye_pas.py desde termo_banco/carros/V143_EVO_BAJO.py (sha {SHA_BAJO}).' + NL
         + f'NO editar a mano. {per_evo}; PASAJE = {p}. Con PASAJE = 0 es V143_EVO_BAJO bit a bit.' + NL + NL
         + 'V143_EVO_BAJO.py — termo_evo: V143 + termostato de boca con el margen como GEN heredable (ver construye_evo.py).' + NL),
        ('_TEL = {}   # termo_evo', PER.format(p=p) + NL + MODULO + '_TEL = {}   # termo_evo'),
        ('        NK, NKMAX, N_NEC = self.NK, self.NKMAX, self.N_NEC' + NL,
         '        if PASAJE: self._ps_init(ctx)   # opusB: genoma del fundador (de SIEMBRA o de la inicial), mutado' + NL
         + '        NK, NKMAX, N_NEC = self.NK, self.NKMAX, self.N_NEC' + NL),
        ('        self._g = self._ev_sortea(); self._gorig = 0; self._gt0 = None' + NL,
         '        self._g = (self._ps_g0 if (PASAJE and self._ps_g0 is not None) else self._ev_sortea()); self._gorig = 0; self._gt0 = None' + NL
         + '        if PASAJE: self._ps_fund()   # opusB: telemetria del fundador' + NL),
        ('        return dict(g=float(min(max(gh, G_CLIP[0]), G_CLIP[1])))' + NL,
         '        _mh = dict(g=float(min(max(gh, G_CLIP[0]), G_CLIP[1])))' + NL
         + "        if PASAJE: _mh['b'] = self._ps_muta(self._psb)   # opusB: el hijo lleva el cerebro del padre, mutado" + NL
         + '        return _mh' + NL),
        ('        NK = self.NK; ETA_S = self.ETA_S; AVERSION = self.AVERSION; LAM = self.LAM; CLIP_S = self.CLIP_S' + NL,
         '        if PASAJE: self._ps_nace(info)   # opusB: el nacido aplica su cerebro heredado ANTES de construirse' + NL
         + '        NK = self.NK; ETA_S = self.ETA_S; AVERSION = self.AVERSION; LAM = self.LAM; CLIP_S = self.CLIP_S' + NL),
        ("        if t % 1000 == 0: self._ev_tel()['vivos'].append([int(t), round(self._g, 5)])" + NL,
         "        if t % 1000 == 0: self._ev_tel()['vivos'].append([int(t), round(self._g, 5)])" + NL
         + "        if PASAJE and t % 1000 == 0: self._ps_tel(t)   # opusB: genoma del vivo (solo escritura)" + NL),
        ('        return dict(evo=EVO, g_ini=list(G_INI), sigma=SIGMA, g_final=round(self._g, 5), **self._tm)' + NL,
         '        return dict(evo=EVO, g_ini=list(G_INI), sigma=SIGMA, g_final=round(self._g, 5), **self._tm)' + NL
         + METODOS.replace('\n', NL)),
    ]


def h16b(b): return hashlib.sha256(b).hexdigest()[:16]
def h16(p): return h16b(open(p, 'rb').read())


def construye(nombre, p):
    src = open(ORIGEN, 'rb').read()
    if h16b(src) != SHA_BAJO: raise SystemExit(f"origen {ORIGEN} sha {h16b(src)} != {SHA_BAJO}")
    txt = src.decode('utf-8')
    if 'import math' not in txt and '\nimport math' not in txt:
        a = 'import numpy as np' + NL
        if txt.count(a) != 1: raise SystemExit("ancla import numpy")
        txt = txt.replace(a, 'import math   # opusB' + NL + a)
    for a, rep in anclas(nombre, p):
        n = txt.count(a)
        if n != 1: raise SystemExit(f"ancla {a[:70]!r} aparece {n} veces (se exige 1)")
        txt = txt.replace(a, rep)
    return txt.encode('utf-8')


def todas():
    return {n: construye(n, p) for n, p in VARIANTES}


def main(argv=None):
    ap = argparse.ArgumentParser(allow_abbrev=False)
    ap.add_argument('--verifica', action='store_true')
    a = ap.parse_args(argv)
    outs = todas()
    base = outs['V143_PAS'].decode('utf-8').split(NL)
    for n, bts in outs.items():
        ls = bts.decode('utf-8').split(NL)
        dif = [i for i, (x, y) in enumerate(zip(base, ls)) if x != y]
        if len(ls) != len(base) or any(not ('PASAJE = ' in ls[i] or n in ls[i]) for i in dif):
            raise SystemExit(f"{n}: difiere de V143_PAS en algo mas que perilla/nombre: lineas {dif[:6]}")
    ok = True
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
    print(f"origen V143_EVO_BAJO.py sha {h16(ORIGEN)} (fijado {SHA_BAJO}) - construye_pas.py sha {h16(os.path.abspath(__file__))}")
    return 0 if ok else 1


if __name__ == '__main__':
    sys.exit(main())
