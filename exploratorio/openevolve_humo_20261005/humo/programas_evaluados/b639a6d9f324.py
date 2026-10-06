# EVOLVE-BLOCK-START
"""Cerebro de un linaje en el mundo del anillo. Interfaz fija: crea(ctx) devuelve un objeto con
actua(obs), resultado(res), fin_paso(info), muere(info), al_parir(info), nace(info), quiere_parir(info)."""
import numpy as np

MARGEN = 0.25      # muerde una letra que sirve si la reserva que sube esta bajo rep_umbral + MARGEN
PRUEBA = 0.5       # prueba una letra desconocida solo si E y Ag > PRUEBA
PEN_OTRO = 0.35    # factor al blanco si otro cuerpo esta estrictamente mas cerca
D0 = 3.0           # suavizado de la distancia en el puntaje del blanco


class Carro:
    def __init__(self, ctx):
        self.L = int(ctx['L']); self.U = float(ctx['rep_umbral']); self.rng = ctx['rng']
        self.yo = ctx['id']
        self.suma = {}; self.n = {}          # memoria del linaje: letra -> suma de dS, numero de mordidas
        self.blanco = None

    def _val(self, k):
        if k not in self.n: return None
        return self.suma[k] / self.n[k]

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
            if x >= self.U + MARGEN: continue
            u = 4.0 if x < 0.3 else (2.0 if x < self.U else 1.0)
            g += u * min(v[j], self.U + 0.5 - x)
        return g

    def _reciclable(self, v, lev):
        """letra conocida sin ganancia directa: reciclarla (si es segura) renueva el stock del
        mundo y puede hacer aparecer una letra util en otra parte. nunca se recicla una letra que
        sube alguna reserva. solo se recicla cuando las dos reservas ya llegaron al umbral de
        reproduccion (con margen) y el mordisco no las hace caer por debajo: asi el reciclaje
        nunca retrasa llegar a la reproduccion ni rompe una racha ya en curso."""
        if (v > 0).any(): return False
        if min(lev) < self.U + 0.03: return False
        for j in (0, 1):
            if v[j] < 0 and lev[j] + v[j] < self.U + 0.03: return False
        return True

    def actua(self, obs):
        pos = obs['pos']; lev = (float(obs['E']), float(obs['Ag'])); objs = obs['objs']
        otros = [c[1] for c in obs['cuerpos'] if c[0] != self.yo]
        mejor = None; desc = None; recic = None
        for x, k in objs.items():
            d = self._dist(pos, x); v = self._val(k)
            if v is None:
                if min(lev) > PRUEBA and (desc is None or d < desc[0]): desc = (d, x)
                continue
            g = self._gana(v, lev)
            if g:
                s = g / (d + D0)
                if otros and min(self._dist(o, x) for o in otros) < d: s *= PEN_OTRO
                if mejor is None or s > mejor[0]: mejor = (s, x)
            elif (recic is None or d < recic[0]) and self._reciclable(v, lev):
                recic = (d, x)
        if mejor is not None: tgt = mejor[1]
        elif desc is not None: tgt = desc[1]
        elif recic is not None: tgt = recic[1]
        else: tgt = self._hueco(pos, otros)
        self.blanco = tgt
        mov = self._dir(pos, tgt)
        p2 = (pos + mov) % self.L
        muerde = False
        if p2 in objs:
            k2 = objs[p2]; v2 = self._val(k2)
            if v2 is None:
                muerde = min(lev) > PRUEBA
            elif self._gana(v2, lev):
                muerde = True
            elif p2 == tgt and self._reciclable(v2, lev):
                muerde = True
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
