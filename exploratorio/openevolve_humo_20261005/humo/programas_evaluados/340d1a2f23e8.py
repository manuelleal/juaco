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
HASH_MOD = 1_000_003   # modulo para codificar una letra como numero y poder compartirla por la pizarra


class Carro:
    def __init__(self, ctx):
        self.L = int(ctx['L']); self.U = float(ctx['rep_umbral']); self.rng = ctx['rng']
        self.yo = ctx['id']
        self.val = {}          # memoria propia: codigo de letra -> mejor |dS| visto por componente (con signo)
        self.ext = {}          # memoria ajena, recibida por la pizarra de los otros cuerpos del mundo
        self._bi = 0           # indice round-robin para elegir que letra contar en la pizarra
        self.blanco = None

    def _hk(self, k):
        """codigo numerico estable de una letra (no se nombra ni se supone nada de ella): sirve para
        compartirla por la pizarra sin romper la regla de no nombrar letras concretas."""
        return hash(str(k)) % HASH_MOD

    def _funde(self, d, hk, dS):
        """el efecto de una letra es fijo; una mordida con la reserva cerca del tope puede recortar
        el cambio observado, asi que por cada componente nos quedamos con el mayor valor absoluto
        visto (propio o ajeno), la mejor estimacion posible del efecto real."""
        cur = d.get(hk)
        if cur is None: d[hk] = np.array(dS, dtype=float)
        else:
            for j in (0, 1):
                if abs(dS[j]) > abs(cur[j]): cur[j] = dS[j]

    def _lee_pizarra(self, pizarra):
        for _, _, c in pizarra:
            if not c or len(c) < 3: continue
            self._funde(self.ext, int(c[0]), (c[1], c[2]))

    def _escribe(self):
        if not self.val: return None
        claves = list(self.val.keys())
        hk = claves[self._bi % len(claves)]; self._bi += 1
        v = self.val[hk]
        return (float(hk), float(v[0]), float(v[1]))

    def _val(self, k):
        hk = self._hk(k)
        v = self.val.get(hk); e = self.ext.get(hk)
        if v is None: return e
        if e is None: return v
        out = v.copy()
        for j in (0, 1):
            if abs(e[j]) > abs(out[j]): out[j] = e[j]
        return out

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
        self._lee_pizarra(obs['pizarra'])
        otros = [c[1] for c in obs['cuerpos'] if c[0] != self.yo]
        banco = lev[0] >= self.U and lev[1] >= self.U   # ya en zona de reproduccion: priorizar no romper la racha
        d0 = D0_BANCO if banco else D0
        mejor = None; desc = None; recic = None
        for x, k in objs.items():
            d = self._dist(pos, x)
            if banco and d > RADIO_BANCO: continue
            v = self._val(k)
            if v is None:
                if (not banco) and min(lev) > PRUEBA and (desc is None or d < desc[0]): desc = (d, x)
                continue
            g = self._gana(v, lev)
            if g:
                s = g / (d + d0)
                if otros and min(self._dist(o, x) for o in otros) < d: s *= PEN_OTRO
                if mejor is None or s > mejor[0]: mejor = (s, x)
            elif (not banco) and (recic is None or d < recic[0]) and self._reciclable(v, lev):
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
            k2 = objs[p2]
            if banco:
                v2 = self._val(k2)
                muerde = v2 is not None and bool(self._gana(v2, lev))
            else:
                muerde = bool(self._quiere(k2, lev))
        return dict(mov=mov, muerde=muerde, escribe=self._escribe())

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
        self._funde(self.val, self._hk(k), dS)

    def fin_paso(self, info):
        return None

    def muere(self, info):
        return None

    def al_parir(self, info):
        return {hk: v.copy() for hk, v in self.val.items()}

    def nace(self, info):
        self.blanco = None
        m = info.get('memoria')
        if m:
            for hk, v in m.items():
                self._funde(self.val, hk, v)

    def quiere_parir(self, info):
        return True


def crea(ctx):
    return Carro(ctx)
# EVOLVE-BLOCK-END
