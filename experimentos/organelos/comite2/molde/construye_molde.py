"""construye_molde.py — EXPLORATORIO, no es dato. Construye carros/MOLDE.py POR ANCLAS de texto desde
bundle/experimentos/tronco_v14_3/carros_v143/V143.py (solo se LEE). Agrega perillas de modulo (todas 0 = V143 bit a bit):
  PIZ      CULTURA PUBLICA: cada cuerpo publica en la pizarra su tabla SENTIDA (8 numeros: dE, dAg medios por letra; 0 = no probada) cada
           W_PIZ pasos o cuando cambia el signo de algo; todo cuerpo lee las entradas nuevas de OTROS cada paso y las mete por la VIA LENTA
           con la MISMA regla con que nace() lee el nodo (R = +1 / -3 por signo). El fundador limpio nace sin memoria pero con cultura.
  PIZ_BAR  control de contenido: lee con las letras cruzadas por parejas (A<->B, C<->D).
  PIZ_FUND dosis: lee SOLO mientras el carro no ha sentido nada propio (_adS vacio).
  IMITA    IMITACION sin canal: de obs['cuerpos'] (letra bajo el cuerpo, letra mordida el paso anterior) de los otros: mordio X -> +1 para X
           en las dos filas; parado sobre X sin morder -> -1. Tasa ETA_IMIT.
  ESPERA   historia de vida: veta el parto si la cola real >= ESPERA_COLA (info['cola']).
Nada de la tabla verdadera ni del rng del mundo. MISION: llegar a la AGI por este camino."""
import hashlib, os

AQUI = os.path.dirname(os.path.abspath(__file__))
ORIGEN = r'C:\Users\User\Documents\PROYECTOS\JUACO\bundle\experimentos\tronco_v14_3\carros_v143\V143.py'
SALIDA = os.path.join(AQUI, 'carros', 'MOLDE.py')


def h16b(b): return hashlib.sha256(b).hexdigest()[:16]


METODOS = '''    # ================================================================ MOLDE (comite2/molde): el LINAJE/la ESCUDERIA como unidad
    def _mol_init(self, ctx):
        self._mol_yo = ctx['id']; self._mol_tl = -1; self._mol_tw = -10 ** 9; self._mol_firma = None
        self._v3v = {}
        self._mol = dict(piz=PIZ, piz_bar=PIZ_BAR, piz_fund=PIZ_FUND, imita=IMITA, espera=ESPERA, piz_ads=PIZ_ADS, barre=BARRE, escritos=0, leidos=0, msgs=0,
                         imit_msgs=0, vetos=0, cuerpos=1, t_primera_lectura=None, ads_cult=0, tapado=0, barre_obj=0, barridas=0, barre_veto_ventana=0)
        self._mol_tap = False; self._mol_tb = -10 ** 9

    def _mol_msg(self, P, R, n, eta):
        """La MISMA regla con que nace() lee el nodo (via lenta), con tasa eta. Sin rng."""
        Wps, Wns = self.Wps, self.Wns; LAM = self.LAM
        Pv = np.asarray(P, float)
        if LAM: mc = np.minimum(Wps[n], Wns[n]) * (Pv > 0); Wps[n] = Wps[n] - LAM * mc; Wns[n] = Wns[n] - LAM * mc
        ds = R - float((Wps[n] - Wns[n]) @ Pv)
        if ds > 0: Wps[n] = np.clip(Wps[n] + eta * ds * Pv, 0, self.CLIP_S)
        else:      Wns[n] = np.clip(Wns[n] + eta * self.AVERSION * (-ds) * Pv, 0, self.CLIP_S)
        self._v3c = None; self._mol['msgs'] += 1

    def _mol_tabla(self):
        out = []
        for k in TIPOS_MOL:
            m = self._adS.get(k)
            out += ([m[0] / m[2], m[1] / m[2]] if m else [0.0, 0.0])
        return tuple(out)

    def _mol_escribe(self, obs):
        if not PIZ or not self._adS: return None
        t = obs['t']; tab = self._mol_tabla(); firma = tuple((v > 0) - (v < 0) for v in tab)
        if firma != self._mol_firma or t - self._mol_tw >= W_PIZ:
            self._mol_firma = firma; self._mol_tw = t; self._mol['escritos'] += 1
            return tab
        return None

    def _mol_lee(self, obs):
        t = obs['t']
        if PIZ:
            lee = not (PIZ_FUND and self._adS)
            tl = self._mol_tl
            for te, ide, cont in obs['pizarra']:
                if te <= self._mol_tl: continue
                tl = max(tl, te)
                if ide == self._mol_yo or not lee: continue
                self._mol['leidos'] += 1
                if self._mol['t_primera_lectura'] is None: self._mol['t_primera_lectura'] = int(t)
                for j, k in enumerate(TIPOS_MOL):
                    kr = PAREJA_MOL[k] if PIZ_BAR else k
                    for n in (0, 1):
                        v = cont[2 * j + n]
                        if v > 0: self._mol_msg(self.PAT[kr], 1.0, n, self.ETA_S)
                        elif v < 0: self._mol_msg(self.PAT[kr], -3.0, n, self.ETA_S)
                    if PIZ_ADS and kr not in self._adS and (cont[2 * j] != 0 or cont[2 * j + 1] != 0):   # la cultura tambien es tabla SENTIDA (para la opcion aprendida de APR)
                        self._adS[kr] = [float(cont[2 * j]), float(cont[2 * j + 1]), 1]; self._mol['ads_cult'] += 1
            self._mol_tl = tl
        if IMITA:
            for ide, pos, bajo, ult in obs['cuerpos']:
                if ide == self._mol_yo: continue
                if ult is not None:
                    for n in (0, 1): self._mol_msg(self.PAT[ult], 1.0, n, ETA_IMIT)
                    self._mol['imit_msgs'] += 1
                elif bajo is not None:
                    for n in (0, 1): self._mol_msg(self.PAT[bajo], -1.0, n, ETA_IMIT)
                    self._mol['imit_msgs'] += 1

    def _mol_puede(self, kk, E, Ag):
        """BARRE: la mordida mala se puede pagar si la necesidad que golpea (segun las filas del propio organismo) queda con reserva."""
        v = self._v3v.get(kk)
        if v is None or not (v[0] < 0 or v[1] < 0): return False
        if v[0] < 0 and E < BARRE_RES: return False
        if v[1] < 0 and Ag < BARRE_RES: return False
        return True

    def _mol_barre_boca(self, kk, E, Ag, t):
        """La mordida de destape. Dosis 1 (BARRE_V2 = 0): basta la reserva. Dosis 2: ademas el mundo tapado en este paso, fuera de la
        ventana de parto y con refractario BARRE_CADA."""
        if not self._mol_puede(kk, E, Ag): return False
        if BARRE_V2:
            if not self._mol_tap or t - self._mol_tb < BARRE_CADA: return False
            if E >= self.rep_umbral and Ag >= self.rep_umbral: self._mol['barre_veto_ventana'] += 1; return False
        self._mol_tb = t; self._mol['barridas'] += 1
        return True

    def _mol_barre(self, pos, objs, E, Ag, d, k, left):
        """BARRE (nicho): si el mundo esta TAPADO (>= BARRE_FRAC de los objetos son malos conocidos) y hay reserva, el objetivo es el malo
        pagable mas cercano (las patas de FABRICA lo persiguen con su ruido). Si no, el objetivo de siempre."""
        obst = self._v3o; self._mol_tap = False
        if not obst or not objs: return d, k, left
        nb = sum(1 for v in objs.values() if v in obst)
        if nb < BARRE_FRAC * len(objs): return d, k, left
        self._mol['tapado'] += 1; self._mol_tap = True
        if BARRE_V2 and (E >= self.rep_umbral and Ag >= self.rep_umbral): return d, k, left   # dosis 2: la ventana de parto manda
        best = None; L = self.L
        for x, kk in objs.items():
            if kk in obst and self._mol_puede(kk, E, Ag):
                dl = (pos - x) % L; dr = (x - pos) % L; dd = min(dl, dr)
                if best is None or dd < best[0]: best = (dd, kk, dl < dr)
        if best is None: return d, k, left
        self._mol['barre_obj'] += 1
        return best

    def quiere_parir(self, info):
        if ESPERA and info['cola'] >= ESPERA_COLA:
            self._mol['vetos'] += 1; return False
        return True

    def _mol_salida(self):
        return dict(self._mol)

'''

ANCLAS = [
    ('"""V143.py — tronco_v14_3',
     '"""MOLDE.py — comite2/molde (EXPLORATORIO, no es dato): V143.py + perillas PIZ/PIZ_BAR/PIZ_FUND/IMITA/ESPERA (todas 0 = V143 bit a bit).\n'
     'CONSTRUIDO por comite2/molde/construye_molde.py. NO editar a mano. Sigue el docstring del origen.\n\nV143.py — tronco_v14_3'),
    ('CACHE = 1   # tras el humo:',
     '# ---- MOLDE (comite2/molde): perillas de la ESCUDERIA como unidad; todas 0 = V143 bit a bit\n'
     'PIZ = 0; PIZ_BAR = 0; PIZ_FUND = 0; IMITA = 0; ESPERA = 0; PIZ_ADS = 0; BARRE = 0\n'
     'BARRE_FRAC = 0.8; BARRE_RES = 0.8   # BARRE: fraccion de objetos malos conocidos que declara el mundo tapado; nivel minimo de la necesidad golpeada\n'
     'BARRE_V2 = 0; BARRE_CADA = 200   # dosis 2: muerde solo si el mundo esta tapado EN ESTE PASO, fuera de la ventana de parto y a lo sumo una vez cada BARRE_CADA pasos\n'
     'W_PIZ = 50; ETA_IMIT = 0.05; ESPERA_COLA = 3\n'
     "TIPOS_MOL = ('A', 'B', 'C', 'D'); PAREJA_MOL = {'A': 'B', 'B': 'A', 'C': 'D', 'D': 'C'}\n"
     'MOLDE = 1   # el gancho corre siempre; con las perillas en 0 no hace nada\n'
     'CACHE = 1   # tras el humo:'),
    ('        self._v3_init(ctx)\n',
     '        self._v3_init(ctx)\n        self._mol_init(ctx)   # MOLDE\n'),
    ('        if OPCION: self._apr_paso(E, Ag)\n',
     '        if OPCION: self._apr_paso(E, Ag)\n        if MOLDE and (PIZ or IMITA): self._mol_lee(obs)   # MOLDE: cultura antes de decidir\n'),
    ('        return dict(mov=mov, muerde=mordio, escribe=None)\n',
     '        return dict(mov=mov, muerde=mordio, escribe=(self._mol_escribe(obs) if (MOLDE and PIZ) else None))\n'),
    ('        d, k, left = self._see(pos, objs, t, contar=True); pat = PAT[k]\n',
     '        d, k, left = self._see(pos, objs, t, contar=True); pat = PAT[k]\n'
     '        if MOLDE and BARRE: d, k, left = self._mol_barre(pos, objs, E, Ag, d, k, left); pat = PAT[k]   # MOLDE BARRE: objetivo\n'),
    ("                self._v3['vetos'] += int(mordio); mordio = False\n",
     "                self._v3['vetos'] += int(mordio); mordio = False\n"
     "                if MOLDE and BARRE and self._mol_barre_boca(kk, E, Ag, t): mordio = True   # MOLDE BARRE: destapa el mundo\n"),
    ('        if OPCION: self._apr_nace(info)\n',
     "        if OPCION: self._apr_nace(info)\n        self._mol['cuerpos'] += 1   # MOLDE\n"),
    ('    # ================================================================ tronco_v14_3: PIEZA 1 (FILTRO con META) y telemetria\n',
     METODOS + '    # ================================================================ tronco_v14_3: PIEZA 1 (FILTRO con META) y telemetria\n'),
    ("            **({'v143': self._v3_salida()} if (DESAMB or FILTRO) else {}))",
     "            **({'v143': self._v3_salida()} if (DESAMB or FILTRO) else {}), molde=self._mol_salida())"),
]


def construye():
    src = open(ORIGEN, encoding='utf-8').read()
    out = src
    for a, b in ANCLAS:
        if out.count(a) != 1: raise SystemExit(f"ancla no unica ({out.count(a)}): {a[:70]!r}")
        out = out.replace(a, b)
    return out.encode('utf-8')


if __name__ == '__main__':
    b = construye()
    os.makedirs(os.path.dirname(SALIDA), exist_ok=True)
    tmp = SALIDA + '.tmp'; open(tmp, 'wb').write(b); os.replace(tmp, SALIDA)   # atomico: la ola en curso puede estar importando
    print(f"origen V143.py {h16b(open(ORIGEN, 'rb').read())} -> {SALIDA} {h16b(b)}")
