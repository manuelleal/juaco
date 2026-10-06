# EVOLVE-BLOCK-START
"""Cerebro de un linaje en el mundo del anillo. Interfaz fija: crea(ctx) devuelve un objeto con
actua(obs), resultado(res), fin_paso(info), muere(info), al_parir(info), nace(info), quiere_parir(info)."""
import numpy as np

MARGEN = 0.5       # muerde una letra que sirve si la reserva que sube esta bajo rep_umbral + MARGEN (casi al tope)
PRUEBA = 0.5       # prueba una letra desconocida solo si E y Ag > PRUEBA
PEN_OTRO = 0.35    # factor al blanco si otro cuerpo esta estrictamente mas cerca
D0 = 3.0           # suavizado de la distancia en el puntaje del blanco
SEGURO_MIN = 0.05  # no se muerde si la componente que baja deja la reserva por debajo de esto


class Carro:
    def __init__(self, ctx):
        self.L = int(ctx['L']); self.U = float(ctx['rep_umbral']); self.rng = ctx['rng']
        self.yo = ctx['id']; self.dote = float(ctx.get('dote', 0.6))
        self.suma = {}; self.n = {}          # memoria propia del linaje: letra -> suma de dS, numero de mordidas
        self.ext_suma = {}; self.ext_n = {}  # mejor dato ajeno visto en la pizarra, por letra (sin duplicar)
        self._bcast_i = 0
        self.blanco = None

    def _val(self, k):
        s = None; n = 0
        if k in self.n: s = self.suma[k]; n = self.n[k]
        if k in self.ext_n and self.ext_n[k] > 0:
            s = self.ext_suma[k] if s is None else s + self.ext_suma[k]
            n += self.ext_n[k]
        if n <= 0: return None
        return s / n

    def _dist(self, a, b):
        d = (b - a) % self.L; return min(d, self.L - d)

    def _dir(self, a, b):
        if a == b: return 0
        d = (b - a) % self.L; return 1 if d <= self.L - d else -1

    def _gana(self, v, lev):
        """ganancia neta, ponderada por urgencia, de morder una letra de valor medio v con reservas lev = (E, Ag).
        admite letras de efecto mixto: una componente puede bajar si la otra sube lo bastante, siempre que la
        reserva que baja no quede en riesgo de muerte."""
        if v is None: return None
        g = 0.0
        for j in (0, 1):
            x = lev[j]
            if v[j] >= 0:
                if x >= self.U + MARGEN: continue
                u = 4.0 if x < 0.3 else (2.0 if x < self.U else 1.0)
                g += u * min(v[j], self.U + 0.5 - x)
            else:
                if x + v[j] < SEGURO_MIN: return 0.0
                u = 6.0 if x < 0.3 else (3.0 if x < self.U else 1.0)
                g += u * v[j]
        return g

    def _quiere(self, k, lev):
        v = self._val(k)
        if v is None: return min(lev) > PRUEBA
        g = self._gana(v, lev)
        return g is not None and g > 0

    def actua(self, obs):
        pos = obs['pos']; lev = (float(obs['E']), float(obs['Ag'])); objs = obs['objs']
        self._leer_pizarra(obs)
        otros = [c[1] for c in obs['cuerpos'] if c[0] != self.yo]
        mejor = None; desc = None
        for x, k in objs.items():
            d = self._dist(pos, x); v = self._val(k)
            if v is None:
                if min(lev) > PRUEBA and (desc is None or d < desc[0]): desc = (d, x)
                continue
            g = self._gana(v, lev)
            if g is None or g <= 0: continue
            s = g / (d + D0)
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
            muerde = bool(self._quiere(objs[p2], lev))
        return dict(mov=mov, muerde=muerde, escribe=self._broadcast())

    def _hueco(self, pos, otros):
        """centro del tramo mas largo del anillo sin otros cuerpos."""
        if not otros: return pos
        ps = sorted(set(otros)); best = None
        for i, a in enumerate(ps):
            b = ps[(i + 1) % len(ps)]; g = (b - a) % self.L or self.L
            if best is None or g > best[0]: best = (g, (a + g // 2) % self.L)
        return best[1]

    def _encode(self, k):
        """codifica una letra (se asume caracter) en un numero, para poder compartirla en la pizarra."""
        try:
            return float(ord(k))
        except Exception:
            return None

    def _decode(self, code):
        try:
            return chr(int(round(code)))
        except Exception:
            return None

    def _leer_pizarra(self, obs):
        """adopta de la pizarra el mejor dato ajeno (letra -> suma dS, n) de cada letra, sin duplicar:
        como el efecto de una letra es fijo, un solo dato ajeno ya es informacion exacta."""
        for entrada in obs.get('pizarra', ()):
            if not entrada or len(entrada) < 3: continue
            t, oid, cont = entrada
            if oid == self.yo or cont is None or len(cont) < 4: continue
            k = self._decode(cont[0])
            if k is None: continue
            cnt = cont[3]
            if not cnt or cnt <= 0: continue
            if cnt > self.ext_n.get(k, 0):
                self.ext_suma[k] = np.array([cont[1], cont[2]], dtype=float)
                self.ext_n[k] = float(cnt)

    def _broadcast(self):
        """turna entre las letras propias conocidas, compartiendo su valor medio aprendido."""
        if not self.n: return None
        keys = sorted(self.n.keys())
        k = keys[self._bcast_i % len(keys)]
        self._bcast_i += 1
        code = self._encode(k)
        if code is None: return None
        s = self.suma[k]
        return (code, float(s[0]), float(s[1]), float(self.n[k]))

    def resultado(self, res):
        if not res['mordio']: return
        k = res['letra']; dS = np.asarray(res['dS'], float)
        self.suma[k] = self.suma.get(k, np.zeros(2)) + dS; self.n[k] = self.n.get(k, 0) + 1

    def fin_paso(self, info):
        return None

    def muere(self, info):
        return None

    def al_parir(self, info):
        """combina lo propio con lo mejor ajeno visto en la pizarra, para que el hijo herede todo."""
        mem = {}
        for k in set(self.n) | set(self.ext_n):
            s = np.zeros(2); n = 0
            if k in self.n: s = s + self.suma[k]; n += self.n[k]
            if k in self.ext_n: s = s + self.ext_suma[k]; n += self.ext_n[k]
            if n > 0: mem[k] = (s.copy(), int(n))
        return mem

    def nace(self, info):
        self.blanco = None
        m = info.get('memoria')
        if m:
            for k, (s, n) in m.items():
                if k not in self.n: self.suma[k] = np.asarray(s, float).copy(); self.n[k] = int(n)

    def quiere_parir(self, info):
        """pospone el parto si, tras pagar la dote, alguna reserva quedaria demasiado ajustada."""
        E = info.get('E'); Ag = info.get('Ag')
        if E is None or Ag is None: return True
        margen = 0.15
        return (E - self.dote) >= margen and (Ag - self.dote) >= margen


def crea(ctx):
    return Carro(ctx)
# EVOLVE-BLOCK-END
