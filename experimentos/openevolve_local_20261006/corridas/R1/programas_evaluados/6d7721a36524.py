# EVOLVE-BLOCK-START
"""Cerebro de un linaje en el mundo del anillo. Interfaz fija: crea(ctx) devuelve un objeto con
actua(obs), resultado(res), fin_paso(info), muere(info), al_parir(info), nace(info), quiere_parir(info)."""
import numpy as np

MARGEN = 0.25      # muerde una letra que sirve si la reserva que sube esta bajo rep_umbral + MARGEN
PRUEBA = 0.5       # prueba una letra desconocida solo si E y Ag > PRUEBA
PEN_OTRO = 0.35    # factor al blanco si otro cuerpo esta estrictamente mas cerca
D0 = 3.0           # suavizado de la distancia en el puntaje del blanco
SEGURO_CHURN = 0.25 # reciclamos una letra mala conocida (mordida sin beneficio) salvo con reservas muy bajas
MIN_SEGURO = 0.2   # no reciclamos si la mordida deja alguna reserva por debajo de esto
SEGURO_EXPLORA = 0.12 # mientras no conozcamos una letra buena para cada reserva, probamos letras
                       # desconocidas aunque las reservas no esten comodas: no probar nunca garantiza
                       # morir de hambre o sed si la unica fuente buena todavia no se descubrio
MARGEN_RACHA = 0.45   # margen mucho mayor mientras sostenemos la racha de reproduccion (E y Ag ya
                       # por encima del umbral): cada pizca de colchon extra retrasa el momento en
                       # que una reserva cae de nuevo por debajo del umbral y rompe la racha de 500
                       # pasos seguidos que exige el mundo para parir


class Carro:
    def __init__(self, ctx):
        self.L = int(ctx['L']); self.U = float(ctx['rep_umbral']); self.rng = ctx['rng']
        self.yo = ctx['id']
        self.suma = {}; self.n = {}          # memoria del linaje: letra -> suma de dS, numero de mordidas
        self.blanco = None
        self.racha = 0                        # pasos consecutivos con E y Ag ya por encima del umbral

    def _val(self, k):
        if k not in self.n: return None
        return self.suma[k] / self.n[k]

    def _sabe(self, j):
        """ya conocemos alguna letra que sube la reserva j (E=0, Ag=1)."""
        for k in self.n:
            v = self._val(k)
            if v is not None and v[j] > 0: return True
        return False

    def _dist(self, a, b):
        d = (b - a) % self.L; return min(d, self.L - d)

    def _dir(self, a, b):
        if a == b: return 0
        d = (b - a) % self.L; return 1 if d <= self.L - d else -1

    def _gana(self, v, lev, margen):
        """ganancia, ponderada por urgencia, de morder una letra de valor medio v con reservas lev = (E, Ag).
        margen controla hasta donde seguimos valorando topar una reserva: poco (MARGEN) en general,
        mucho mas (MARGEN_RACHA, casi hasta el tope) mientras sostenemos la racha de reproduccion."""
        if v is None: return None
        if (v < 0).any() or not (v > 0).any(): return 0.0
        g = 0.0
        for j in (0, 1):
            if v[j] <= 0: continue
            x = lev[j]
            if x >= self.U + margen: continue
            u = 4.0 if x < 0.3 else (2.0 if x < self.U else 1.0)
            g += u * min(v[j], self.U + 0.5 - x)
        return g

    def _quiere(self, k, lev, completo, margen, evitar_riesgo):
        v = self._val(k)
        if v is None:
            if evitar_riesgo: return False  # en plena racha no apostamos a probar letras desconocidas
            return min(lev) > (PRUEBA if completo else SEGURO_EXPLORA)
        return bool(self._gana(v, lev, margen))

    def _malo(self, v):
        """v tiene una componente negativa: letra que conviene evitar como comida."""
        return v is not None and bool((v < 0).any())

    def _churn_ok(self, v, lev):
        """recicla (muerde sin beneficio) una letra mala conocida para liberar el cupo
        y que salga una nueva al azar. Las letras malas sin reciclar se acumulan y dejan
        al mundo sin comida buena casi siempre, asi que conviene reciclar en casi toda
        la vida del cuerpo, salvo cuando las reservas ya estan muy bajas. Proteccion
        especifica: si una reserva YA cruzo el umbral de reproduccion, el reciclaje no
        puede hacerla caer de nuevo por debajo de ese umbral, porque eso romperia la
        racha de 500 pasos seguidos que se necesita para parir. Si la OTRA reserva
        todavia no llego al umbral, el reciclaje de letras que no la afectan sigue
        permitido."""
        if not self._malo(v): return False
        if min(lev) <= SEGURO_CHURN: return False
        for j in (0, 1):
            if lev[j] >= self.U and lev[j] + v[j] < self.U: return False
        return (lev[0] + v[0]) > MIN_SEGURO and (lev[1] + v[1]) > MIN_SEGURO

    def actua(self, obs):
        pos = obs['pos']; lev = (float(obs['E']), float(obs['Ag'])); objs = obs['objs']
        otros = [c[1] for c in obs['cuerpos'] if c[0] != self.yo]
        if lev[0] >= self.U and lev[1] >= self.U: self.racha += 1
        else: self.racha = 0
        en_racha = self.racha > 0
        margen = MARGEN_RACHA if en_racha else MARGEN
        completo = self._sabe(0) and self._sabe(1)
        umbral_desc = PRUEBA if completo else SEGURO_EXPLORA
        mejor = None; desc = None; recicla = None
        for x, k in objs.items():
            d = self._dist(pos, x); v = self._val(k)
            if v is None:
                if not en_racha and min(lev) > umbral_desc and (desc is None or d < desc[0]): desc = (d, x)
                continue
            g = self._gana(v, lev, margen)
            if g:
                s = g / (d + D0)
                if otros and min(self._dist(o, x) for o in otros) < d: s *= PEN_OTRO
                if mejor is None or s > mejor[0]: mejor = (s, x)
            elif not en_racha and self._churn_ok(v, lev) and (recicla is None or d < recicla[0]):
                recicla = (d, x)
        if mejor is not None: tgt = mejor[1]
        elif desc is not None: tgt = desc[1]
        elif recicla is not None: tgt = recicla[1]
        else: tgt = self._hueco(pos, otros)
        self.blanco = tgt
        mov = self._dir(pos, tgt)
        p2 = (pos + mov) % self.L
        muerde = False
        if p2 in objs:
            letra2 = objs[p2]
            v2 = self._val(letra2)
            if (v2 is not None and not self._malo(v2) and (v2 > 0).any()
                    and all(lev[j] < self.U + MARGEN_RACHA for j in (0, 1) if v2[j] > 0)):
                muerde = True  # comida buena y conocida al alcance, con margen real bajo el tope: gratis
            else:
                muerde = bool(self._quiere(letra2, lev, completo, margen, en_racha))
                if not muerde and not en_racha and self._churn_ok(v2, lev): muerde = True
        return dict(mov=mov, muerde=muerde, escribe=None)

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

    def quiere_parir(self, info):
        return True


def crea(ctx):
    return Carro(ctx)
# EVOLVE-BLOCK-END
