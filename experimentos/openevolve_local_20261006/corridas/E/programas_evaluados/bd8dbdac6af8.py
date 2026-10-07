# EVOLVE-BLOCK-START
"""Cerebro de un linaje en el mundo del anillo. Interfaz fija: crea(ctx) devuelve un objeto con
actua(obs), resultado(res), fin_paso(info), muere(info), al_parir(info), nace(info), quiere_parir(info)."""
import numpy as np

PRUEBA = 0.5       # prueba una letra desconocida solo si E y Ag > PRUEBA
PEN_OTRO = 0.35    # factor al blanco si otro cuerpo esta estrictamente mas cerca
D0 = 3.0           # suavizado de la distancia en el puntaje del blanco
D0_BANCO = 0.6     # suavizado de distancia cuando ya se llego al umbral: castiga fuerte lo lejano
RADIO_BANCO = 45   # en el umbral no se persigue nada mas lejos que esto: evita viajes largos y riesgosos
CAP = 1.5          # tope real de una reserva: conviene acercarse a el para tener colchon contra la espera de 500 pasos
RECICLA_SEGURO = 0.35  # al reciclar una letra mala conocida, la reserva que baja debe quedar por encima de esto
RECIC_UTIL = 0.6   # utilidad base de reciclar: compite por distancia con las letras buenas, para no viajar lejos de mas
NORM_CUENTA = 9.0  # censo esperado por letra si las 4 estuvieran repartidas parejo (36/4): normaliza cuanto reciclar urge segun cuanto una letra excede ese reparto
RADIO_GANA = 70    # sin urgencia (reservas por encima de PRUEBA) tampoco conviene cruzar medio anillo por una ganancia lejana: mas alla de esto se deja ese objeto para quien este mas cerca y se prioriza reciclar cerca, dejando mas objetos buenos "respirando" en el mundo


class Carro:
    def __init__(self, ctx):
        self.L = int(ctx['L']); self.U = float(ctx['rep_umbral']); self.rng = ctx['rng']
        self.yo = ctx['id']
        self.suma = {}; self.n = {}          # memoria del linaje: letra -> suma de dS, numero de mordidas
        self.cod_val = {}                    # conocimiento compartido: codigo generico de letra -> valor medio
        self.cod_order = []                  # orden de turno para difundir lo conocido por la pizarra
        self._bcast_i = 0
        self.blanco = None

    def _cod(self, k):
        """codigo numerico generico de una letra (no identifica ninguna letra concreta): permite
        compartir lo aprendido por la pizarra publica entre cuerpos y linajes distintos."""
        if isinstance(k, (int, np.integer)): return float(k)
        if isinstance(k, (float, np.floating)): return float(k)
        if isinstance(k, str) and k: return float(ord(k[0]))
        return float(hash(k) % 1000003)

    def _aprende(self, k, v):
        cod = self._cod(k)
        if cod not in self.cod_val: self.cod_order.append(cod)
        self.cod_val[cod] = np.asarray(v, float)

    def _val(self, k):
        if k in self.n: return self.suma[k] / self.n[k]
        return self.cod_val.get(self._cod(k))

    def _dist(self, a, b):
        d = (b - a) % self.L; return min(d, self.L - d)

    def _dir(self, a, b):
        if a == b: return 0
        d = (b - a) % self.L; return 1 if d <= self.L - d else -1

    def _gana(self, v, lev):
        """ganancia, ponderada por urgencia, de morder una letra de valor medio v con reservas lev = (E, Ag)."""
        if v is None: return None
        if (v < 0).any() or not (v > 0).any(): return 0.0
        g = 0.0
        for j in (0, 1):
            if v[j] <= 0: continue
            x = lev[j]
            room = CAP - x
            if room <= 0.0: continue
            u = 4.0 if x < 0.3 else (2.0 if x < self.U else 1.3)
            g += u * min(v[j], room)
        return g

    def _reciclable(self, v, lev):
        """letra conocida sin ganancia directa: reciclarla (si es segura) renueva el stock del
        mundo y puede hacer aparecer una letra util en otra parte. nunca se recicla una letra que
        sube alguna reserva, aunque ahora no haga falta: puede servirle a otro cuerpo, o a este
        mismo mas tarde."""
        if (v > 0).any(): return False
        for j in (0, 1):
            if v[j] < 0 and lev[j] + v[j] < RECICLA_SEGURO: return False
        return True

    def _quiere(self, k, lev):
        v = self._val(k)
        if v is None: return min(lev) > PRUEBA
        if self._gana(v, lev): return True
        return self._reciclable(v, lev)

    def actua(self, obs):
        pos = obs['pos']; lev = (float(obs['E']), float(obs['Ag'])); objs = obs['objs']
        self._escucha(obs['pizarra'])
        otros = [c[1] for c in obs['cuerpos'] if c[0] != self.yo]
        banco = lev[0] >= self.U and lev[1] >= self.U   # ya en zona de reproduccion: priorizar no romper la racha
        d0 = D0_BANCO if banco else D0
        cuenta = {}
        for k0 in objs.values(): cuenta[k0] = cuenta.get(k0, 0) + 1   # censo actual de cada letra: cuanto mas sobrerrepresentada, mas urge reciclarla
        mejor = None; desc = None
        for x, k in objs.items():
            d = self._dist(pos, x)
            if banco and d > RADIO_BANCO: continue
            v = self._val(k)
            if v is None:
                if (not banco) and min(lev) > PRUEBA and (desc is None or d < desc[0]): desc = (d, x)
                continue
            g = self._gana(v, lev)
            if g and (banco or d <= RADIO_GANA or min(lev) < PRUEBA):
                s = g / (d + d0)
            elif (not banco) and self._reciclable(v, lev):
                s = RECIC_UTIL * (cuenta[k] / NORM_CUENTA) / (d + d0)   # prioriza reciclar la letra mas sobrerrepresentada: ataca justo lo que atasca el mundo, pero nunca estando en banco: alli solo importa no romper la racha de reproduccion
            else:
                continue
            if otros and min(self._dist(o, x) for o in otros) < d: s *= PEN_OTRO
            if mejor is None or s > mejor[0]: mejor = (s, x)
        if mejor is not None: tgt = mejor[1]
        elif desc is not None: tgt = desc[1]
        else: tgt = self._hueco(pos, otros)
        self.blanco = tgt
        mov = self._dir(pos, tgt)
        p2 = (pos + mov) % self.L
        muerde = False
        if p2 in objs:
            k2 = objs[p2]
            if banco:
                v2 = self._val(k2)
                muerde = v2 is not None and bool(self._gana(v2, lev))
            else:
                muerde = bool(self._quiere(k2, lev))
        return dict(mov=mov, muerde=muerde, escribe=self._difunde())

    def _escucha(self, pizarra):
        """incorpora lo que cualquier cuerpo (de cualquier linaje) ya difundio sobre una letra,
        identificada solo por su codigo generico: asi un fundador sin memoria propia puede evitar
        explorar a ciegas si alguien mas ya conoce esa letra."""
        for entry in pizarra:
            cont = entry[2]
            if cont is None: continue
            for i in range(0, len(cont) - 2, 3):
                cod = float(cont[i])
                if cod in self.cod_val: continue
                self.cod_val[cod] = np.array([float(cont[i + 1]), float(cont[i + 2])])
                self.cod_order.append(cod)

    def _difunde(self):
        """difunde por turno, hasta dos letras ya conocidas (propias o aprendidas de otros)."""
        n = len(self.cod_order)
        if n == 0: return None
        tomar = min(2, n)
        salida = []
        for i in range(tomar):
            cod = self.cod_order[(self._bcast_i + i) % n]
            v = self.cod_val[cod]
            salida += [cod, float(v[0]), float(v[1])]
        self._bcast_i = (self._bcast_i + tomar) % n
        return tuple(salida)

    def _hueco(self, pos, otros):
        """centro del tramo mas largo del anillo sin otros cuerpos."""
        if not otros: return pos
        ps = sorted(set(otros)); best = None
        for i, a in enumerate(ps):
            b = ps[(i + 1) % len(ps)]; g = (b - a) % self.L or self.L
            if best is None or g > best[0]: best = (g, (a + g // 2) % self.L)
        return best[1]

    def resultado(self, res):
        if not res['mordio']: return
        k = res['letra']; dS = np.asarray(res['dS'], float)
        self.suma[k] = self.suma.get(k, np.zeros(2)) + dS; self.n[k] = self.n.get(k, 0) + 1
        self._aprende(k, self.suma[k] / self.n[k])

    def fin_paso(self, info):
        return None

    def muere(self, info):
        return None

    def al_parir(self, info):
        return {k: (self.suma[k].copy(), self.n[k]) for k in self.n}

    def nace(self, info):
        self.blanco = None
        m = info.get('memoria')
        if m:
            for k, (s, n) in m.items():
                if k not in self.n: self.suma[k] = np.asarray(s, float).copy(); self.n[k] = int(n)
        for k in self.n:
            self._aprende(k, self.suma[k] / self.n[k])

    def quiere_parir(self, info):
        return True


def crea(ctx):
    return Carro(ctx)
# EVOLVE-BLOCK-END
