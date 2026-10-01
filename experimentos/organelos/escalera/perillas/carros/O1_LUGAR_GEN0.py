"""O1_LUGAR_GEN0.py — perillas: O1_LUGAR con las dos perillas del modulo (GW valor, GV viaje) como GENES heredables que arrancan en 0.
GENERADO por experimentos/organelos/escalera/perillas/construye_perillas.py desde el texto de O1_LUGAR (sha 49eee6bb278ea097).
NO editar a mano. PERILLAS = 0. Con PERILLAS = 0 es O1_LUGAR bit a bit; con genes (0, 0) es O1; con (1, 1), O1_LUGAR.

O1_LUGAR.py — escalera p1: O1 + MEMORIA DE LUGAR del linaje (bins del anillo x lo que el sitio dio de mas que su letra).
GENERADO por experimentos/organelos/escalera/construye_p1.py desde carrera_escuderias/carros/O1.py (sha 99436afa2715f028).
NO editar a mano. LUGAR = 1, LUGAR_BARAJA = 0. Con LUGAR = 0 es O1 bit a bit; con LUGAR_W = 0.0 o sin oasis, tambien.

carros/O1.py — escuderia O1 (Opus). Carrera de escuderias, ronda 1.

MISION: llegar a la AGI por este camino.

IDEA (bacteria con quimiotaxis dirigida + historia de vida):
  1. Lo que la boca sabe lo aprende el linaje MORDIENDO: por cada letra, la media del dS (dE, dAg) que la pista
     devuelve en resultado(). Nada de la tabla verdadera: una letra sin probar es 'desconocida' y se prueba una
     vez, solo si el cuerpo aguanta el golpe (E y Ag por encima de PRUEBA).
  2. La boca NO la manda el hambre (lo medido: con sed muerde el veneno el 67-90 %). Una buena se muerde solo si
     le sirve (la necesidad que sube esta bajo rep_umbral + MARGEN). Una letra con algun dS negativo solo se
     muerde para LIMPIAR (v2): cuando en el mundo no queda nada util y el golpe es costeable (cae en la necesidad
     mas llena, no rompe la ventana de parto si corre, no baja de PISO si no corre). Lo bueno solo reaparece
     cuando alguien muerde algo o por olvido: sin limpieza, un cuerpo solo se muere de hambre (SOLO v1).
  3. Rechazar sin alejarse no sirve: el cuerpo NO se queda junto a lo malo, VA a lo bueno. Blanco = el objeto
     bueno con mejor ganancia/(distancia), penalizado si otro cuerpo esta mas cerca (no perseguir lo que otro
     se va a comer). Sin blanco: se coloca en el centro del hueco mas grande entre los otros cuerpos (ahi lo
     que aparece le queda mas cerca a el que a nadie).
  4. Historia de vida: nunca veta el parto; la memoria (tabla por letra) es del LINAJE: el hijo la recibe en
     al_parir/nace, y como el carro es el cerebro del linaje (igual que el nodo de FABRICA, que tambien pasa a
     los fundadores), el fundador que pone el mundo tambien la conserva. DECLARADO.
  No escribe en la pizarra (es publica y los rivales no son su linaje). No lee la pizarra.
"""
import math
import numpy as np

MARGEN = 0.25      # muerde lo bueno si la necesidad que sube esta bajo rep_umbral + MARGEN
PRUEBA = 0.5       # prueba una letra desconocida solo si E y Ag > PRUEBA
PEN_OTRO = 0.35    # factor al blanco si otro cuerpo esta estrictamente mas cerca
D0 = 3.0           # suavizado de la distancia en el puntaje
PISO = 0.2         # v2: la limpieza no baja la necesidad golpeada de aqui (si la ventana de parto no corre)

LUGAR = 1   # escalera p1: promotor. LA LINEA QUE CAMBIA ENTRE VARIANTES (0 = O1 bit a bit)
LUGAR_BARAJA = 0   # escalera p1: 1 = control de contenido (escribe en el bin verdadero, LEE en un bin permutado)
LUGAR_W = 1.0; LG_NB = 30; LG_ETA = 0.5; LG_MIN = 0.05   # escalera p1: peso del bono (0.0 = O1 bit a bit), bins, EMA, umbral
LG_VIAJA = 1   # escalera p1b (humo 2): 1 = sin blanco a la vista, VIAJA al sitio recordado en vez de al hueco (0 = humo 1)

PERILLAS = 0   # perillas: LA UNICA LINEA QUE CAMBIA ENTRE VARIANTES (0 = O1_LUGAR bit a bit)
SIEMBRA = None; PS_SEMILLA = 0; PS_SIGMA = 0.03; PS_DELTA = 0.01; PS_LEE = 1; PS_CAMARA = 1   # perillas: los fija el RUNNER por corrida (SIEMBRA None = PS_BASE; PS_LEE 0 = genes NEUTROS)
_PS_CNT = {}; _TEL = {}; _VIVO = {}   # perillas: instancias por linaje, telemetria de SOLO ESCRITURA y genoma del cuerpo actual de cada linaje (el runner los borra antes de cada run)
PS_GENES = ('GW', 'GV'); PS_BASE = (0.0, 0.0); PS_CLIP = ((0.0, 1.5), (0.0, 1.5))
_PS_M64 = 18446744073709551615


class Carro:
    def __init__(self, ctx):
        self.L = int(ctx['L']); self.U = float(ctx['rep_umbral']); self.rng = ctx['rng']
        self.yo = ctx['id']
        self.suma = {}; self.n = {}          # memoria del LINAJE: letra -> suma de dS, numero de mordidas
        self.blanco = None
        self.st = dict(mord={}, pruebas=0, sin_blanco=0, pasos=0, cuerpos=0, partos=0, limpias=0)
        if LUGAR: self._lg_init(ctx)   # escalera p1: memoria de lugar del linaje
        self.GW, self.GV = float(LUGAR_W), float(LG_VIAJA)   # perillas: las dos perillas del modulo, por cuerpo (diseno de P1)
        if PERILLAS: self._ps_init(ctx)   # perillas: genes del fundador (de la camara, de SIEMBRA o de PS_BASE = 0, 0), mutados

    # ------------------------------------------------------------ memoria
    def _val(self, k):
        if k not in self.n: return None
        return self.suma[k] / self.n[k]

    def _dist(self, a, b):
        d = (b - a) % self.L; return min(d, self.L - d)

    def _dir(self, a, b):
        if a == b: return 0
        d = (b - a) % self.L; return 1 if d <= self.L - d else -1

    def _gana(self, v, lev):
        """ganancia ponderada por urgencia de morder una letra de valor v con niveles lev=(E, Ag); None si dania."""
        if v is None: return None
        if (v < 0).any() or not (v > 0).any(): return 0.0
        g = 0.0
        for j in (0, 1):
            if v[j] <= 0: continue
            x = lev[j]
            if x >= self.U + MARGEN: continue
            u = 4.0 if x < 0.3 else (2.0 if x < self.U else 1.0)
            g += u * min(v[j], self.U + 0.5 - x)
        return g

    def _quiere(self, k, lev, limpia=False):
        v = self._val(k)
        if v is None: return min(lev) > PRUEBA
        if LUGAR: v = self._lg_v(v, self._lgx)   # escalera p1: el bocado vale lo de su letra + lo que el sitio recuerda
        g = self._gana(v, lev)
        if g: return True
        return limpia and self._costeable(v, lev)

    def _costeable(self, v, lev):
        """v2 LIMPIEZA: morder algo que dania solo si el golpe cae en una necesidad que lo aguanta (si la ventana
        de parto corre, no la rompe; si no corre, no baja de PISO) y no toca la necesidad que se busca."""
        if not (v < 0).any(): return False
        for j in (0, 1):
            if v[j] < 0:
                piso = self.U if min(lev) >= self.U else PISO
                if lev[j] + v[j] < piso: return False
            if v[j] < 0 and lev[j] < lev[1 - j]: return False   # el golpe va a la necesidad MAS llena
        return True

    # ------------------------------------------------------------ INTERFAZ
    def actua(self, obs):
        pos = obs['pos']; lev = (float(obs['E']), float(obs['Ag'])); objs = obs['objs']
        self.st['pasos'] += 1
        otros = [c[1] for c in obs['cuerpos'] if c[0] != self.yo]
        mejor = None; desc = None
        for x, k in objs.items():
            d = self._dist(pos, x); v = self._val(k)
            if v is None:
                if min(lev) > PRUEBA and (desc is None or d < desc[0]): desc = (d, x)
                continue
            g = self._gana(self._lg_v(v, x) if LUGAR else v, lev)   # escalera p1
            if not g: continue
            s = g / (d + D0)
            if otros and min(self._dist(o, x) for o in otros) < d: s *= PEN_OTRO
            if mejor is None or s > mejor[0]: mejor = (s, x)
        # v2: nada util en el mundo y hay necesidad -> limpiar (morder lo malo costeable mas cercano)
        limpia = mejor is None and min(lev) < self.U + MARGEN
        sucio = None
        if limpia:
            for x, k in objs.items():
                v = self._val(k)
                if v is not None and self._costeable(v, lev):
                    d = self._dist(pos, x)
                    if sucio is None or d < sucio[0]: sucio = (d, x)
        if mejor is not None:
            tgt = mejor[1]
            if LUGAR: self._lg_cuenta(tgt)   # escalera p1: telemetria (blancos con bono de lugar)
        elif desc is not None: tgt = desc[1]
        elif sucio is not None: tgt = sucio[1]
        else:
            tgt = self._lg_meta(pos) if (LUGAR and LG_VIAJA and self.GV > 0.0) else None   # escalera p1b: sin blanco a la vista, al sitio recordado
            if tgt is None: tgt = self._hueco(pos, otros); self.st['sin_blanco'] += 1
        self.blanco = tgt
        mov = self._dir(pos, tgt)
        p2 = (pos + mov) % self.L
        muerde = False
        if p2 in objs:
            if LUGAR: self._lgx = p2   # escalera p1: donde esta lo que se va a morder
            muerde = bool(self._quiere(objs[p2], lev, limpia))
            if muerde and objs[p2] not in self.n: self.st['pruebas'] += 1
            if muerde and limpia and self._val(objs[p2]) is not None and (self._val(objs[p2]) < 0).any(): self.st['limpias'] += 1
        return dict(mov=mov, muerde=muerde, escribe=None)

    def _hueco(self, pos, otros):
        if not otros: return pos
        ps = sorted(set(otros)); best = None
        for i, a in enumerate(ps):
            b = ps[(i + 1) % len(ps)]; g = (b - a) % self.L or self.L
            if best is None or g > best[0]: best = (g, (a + g // 2) % self.L)
        return best[1]

    def resultado(self, res):
        if not res['mordio']: return
        k = res['letra']; dS = np.asarray(res['dS'], float)
        if LUGAR: self._lg_apr(res['pos'], k, dS)   # escalera p1: ANTES de actualizar la tabla por letra
        self.suma[k] = self.suma.get(k, np.zeros(2)) + dS; self.n[k] = self.n.get(k, 0) + 1
        self.st['mord'][k] = self.st['mord'].get(k, 0) + 1

    def fin_paso(self, info):
        if PERILLAS and info['t'] % 1000 == 0: self._ps_tel(info['t'])   # perillas: genes del vivo (solo escritura)
        return None

    def muere(self, info):
        return None

    def al_parir(self, info):
        self.st['partos'] += 1
        _m = {k: (self.suma[k].copy(), self.n[k]) for k in self.n}
        if LUGAR: _m['_lugar'] = (self.lugar.copy(), self.nl.copy())   # escalera p1: la memoria de lugar es del linaje
        if PERILLAS: _m['_gen'] = (self._ps_muta(self._gen), self._prof + 1); _TEL.setdefault(self._psi, {})['partos'] = _TEL[self._psi].get('partos', 0) + 1
        return _m

    def nace(self, info):
        self.st['cuerpos'] += 1; self.blanco = None
        m = info.get('memoria')
        if PERILLAS and m and '_gen' in m: m = dict(m); _g = m.pop('_gen'); self._prof = int(_g[1]); self._ps_pon(_g[0])   # perillas: el hijo toma sus genes
        if LUGAR and m and '_lugar' in m: m = dict(m); self._lg_hereda(m.pop('_lugar'))   # escalera p1
        if m:
            for k, (s, n) in m.items():
                if k not in self.n: self.suma[k] = np.asarray(s, float).copy(); self.n[k] = int(n)

    def quiere_parir(self, info):
        return True

    def salida(self):
        if LUGAR: return dict(self._salida_o1(), **self._lg_salida())   # escalera p1: la salida de O1 + la memoria de lugar
        return self._salida_o1()

    def _salida_o1(self):
        return dict(tabla={k: [round(float(z), 3) for z in self._val(k)] for k in self.n}, n={k: int(v) for k, v in self.n.items()},
                    **{k: v for k, v in self.st.items()})

    # ================================================================ escalera p1: MEMORIA DE LUGAR del linaje (regla local)
    def _lg_init(self, ctx):
        self.lugar = np.zeros((LG_NB, 2)); self.nl = np.zeros(LG_NB, int); self._lgx = None
        self.st['lg_bono'] = 0; self.st['lg_apr'] = 0; self.st['lg_viajes'] = 0

    def _lg_bin(self, x):
        return (int(x) * LG_NB) // self.L

    def _lg_rb(self, b):
        """bin que se LEE: el verdadero, o (control, ERR-170) el ANTIPODA fijo b + LG_NB//2: nunca toca el oasis (4 bins contiguos de 30)."""
        return (b + LG_NB // 2) % LG_NB if LUGAR_BARAJA else b

    def _lg_leer(self, x):
        return self.lugar[self._lg_rb(self._lg_bin(x))]

    def _lg_v(self, v, x):
        """valor de la letra + lo que el sitio recuerda DE MAS (solo bonos > LG_MIN, solo en necesidades que ya valen > 0, solo si no dania)."""
        if (v < 0).any(): return v
        m = self._lg_leer(x)
        bono = np.where((m > LG_MIN) & (v > 0), m, 0.0)
        if not (bono > 0).any(): return v
        if self.GW <= 0.0: return v   # perillas: gen de valor en 0 = O1
        return v + self.GW * bono

    def _lg_apr(self, x, k, dS):
        v = self._val(k)
        if v is None: return
        b = self._lg_bin(x)
        self.lugar[b] += LG_ETA * ((dS - v) - self.lugar[b]); self.nl[b] += 1; self.st['lg_apr'] += 1

    def _lg_cuenta(self, x):
        if (self._lg_leer(x) > LG_MIN).any(): self.st['lg_bono'] += 1

    def _lg_meta(self, pos):
        """P1b: sin blanco a la vista: el centro del bin recordado con mas bono por distancia (None si ningun sitio recuerda nada)."""
        s = self.lugar.sum(1) if not LUGAR_BARAJA else np.array([self.lugar[self._lg_rb(b)].sum() for b in range(LG_NB)])
        best = None
        for b in range(LG_NB):
            if self.GV * s[b] <= LG_MIN: continue   # perillas: ganancia del viaje (1.0 = P1)
            c = ((2 * b + 1) * self.L) // (2 * LG_NB); v = s[b] / (self._dist(pos, c) + D0)
            if best is None or v > best[0]: best = (v, c)
        if best is None: return None
        self.st['lg_viajes'] += 1
        return best[1]

    def _lg_hereda(self, m):
        if self.nl.sum() == 0: self.lugar = np.asarray(m[0], float).copy(); self.nl = np.asarray(m[1], int).copy()

    def _lg_salida(self):
        s = self.lugar.sum(1)
        return dict(lugar=dict(W=LUGAR_W, nb=LG_NB, baraja=int(LUGAR_BARAJA), n=[int(z) for z in self.nl],
                               mem=[[round(float(z), 3) for z in fila] for fila in self.lugar],
                               bin_max=int(np.argmax(s)), max=round(float(s.max()), 3),
                               bins_con_bono=[int(i) for i in range(LG_NB) if (self.lugar[i] > LG_MIN).any()]))

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


def crea(ctx):
    return Carro(ctx)
