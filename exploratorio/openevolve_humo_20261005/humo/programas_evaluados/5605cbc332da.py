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


class Carro:
    def __init__(self, ctx):
        self.L = int(ctx['L']); self.U = float(ctx['rep_umbral']); self.rng = ctx['rng']
        self.yo = ctx['id']
        self.suma = {}; self.n = {}          # memoria propia: letra -> suma de dS, numero de mordidas
        self.ext = {}                        # memoria social: letra -> {id_emisor: (suma, n)} oida en la pizarra
        self._bc_i = 0                       # puntero round-robin: que letra propia contar hoy en la pizarra
        self.blanco = None

    def _combined(self, k):
        """suma y n de una letra combinando lo mordido por este cuerpo y lo oido en la pizarra.
        cada emisor aporta una sola vez (se sobreescribe, no se acumula), asi que repetir el mismo
        mensaje no infla el conteo."""
        s = self.suma.get(k); n = self.n.get(k, 0)
        s = s.copy() if s is not None else np.zeros(2)
        d = self.ext.get(k)
        if d:
            for ss, nn in d.values():
                s = s + ss; n += nn
        return s, n

    def _val(self, k):
        s, n = self._combined(k)
        if n == 0: return None
        return s / n

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

    def _quiere(self, k, lev, v=None):
        if v is None: v = self._val(k)
        if v is None: return min(lev) > PRUEBA
        if self._gana(v, lev): return True
        return self._reciclable(v, lev)

    def actua(self, obs):
        self._leer_pizarra(obs.get('pizarra') or ())
        pos = obs['pos']; lev = (float(obs['E']), float(obs['Ag'])); objs = obs['objs']
        otros = [c[1] for c in obs['cuerpos'] if c[0] != self.yo]
        banco = lev[0] >= self.U and lev[1] >= self.U   # ya en zona de reproduccion: priorizar no romper la racha
        d0 = D0_BANCO if banco else D0
        vals = {k: self._val(k) for k in set(objs.values())}   # una sola cuenta por letra, no por casilla
        mejor = None; desc = None; recic = None
        for x, k in objs.items():
            d = self._dist(pos, x)
            if banco and d > RADIO_BANCO: continue
            v = vals[k]
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
                v2 = vals.get(k2)
                muerde = v2 is not None and bool(self._gana(v2, lev))
            else:
                muerde = bool(self._quiere(k2, lev, vals.get(k2)))
        return dict(mov=mov, muerde=muerde, escribe=self._mensaje())

    def _hueco(self, pos, otros):
        """centro del tramo mas largo del anillo sin otros cuerpos."""
        if not otros: return pos
        ps = sorted(set(otros)); best = None
        for i, a in enumerate(ps):
            b = ps[(i + 1) % len(ps)]; g = (b - a) % self.L or self.L
            if best is None or g > best[0]: best = (g, (a + g // 2) % self.L)
        return best[1]

    def _leer_pizarra(self, pizarra):
        """incorpora a la memoria social lo que otros cuerpos contaron que mordieron en persona."""
        for ent in pizarra:
            if len(ent) != 3: continue
            t, idf, cont = ent
            if idf == self.yo or not cont or len(cont) < 4: continue
            try:
                k = chr(int(round(cont[0])))
                s0 = float(cont[1]); s1 = float(cont[2]); n = float(cont[3])
            except Exception:
                continue
            if n <= 0: continue
            self.ext.setdefault(k, {})[idf] = (np.array((s0, s1)), n)

    def _mensaje(self):
        """cuenta en la pizarra, una letra por paso (rotando), lo que este cuerpo mordio en
        persona, para que otros cuerpos aprendan su valor sin tener que probarla ellos mismos.
        degrada a None sin romper nada si la letra no es el tipo esperado."""
        if not self.n: return None
        try:
            ks = list(self.n.keys())
            k0 = ks[self._bc_i % len(ks)]; self._bc_i += 1
            s = self.suma[k0]
            return (float(ord(k0)), float(s[0]), float(s[1]), float(self.n[k0]))
        except Exception:
            return None

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
