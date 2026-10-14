# EVOLVE-BLOCK-START
"""MINIMO: O1 sin limpieza + la decision de dos modos, escrita a mano (bloque MURO MINIMO, 8-oct-2026).

Lejos de criar (alguna reserva bajo rep_umbral): prueba lo desconocido y LIMPIA (muerde lo malo conocido para que el mundo
reponga), sin bajar de PISO la reserva golpeada. Cerca de criar (las dos reservas sobre rep_umbral): solo come lo que sirve,
hasta TOPE. Nada mas: sin pizarra, sin radio, sin utilidad de limpiar. Interfaz fija: crea(ctx) devuelve un objeto con
actua(obs), resultado(res), fin_paso(info), muere(info), al_parir(info), nace(info), quiere_parir(info)."""
import numpy as np
# VARIANTE M_PIZARRA (bloque MURO MINIMO PIEZA, 13-oct-2026): MINIMO + pieza(s) [1] de §2 del PREREGISTRO de
# muro_minimo_20261008. Escrita por construye.py desde MINIMO (sha b9cfbb3bb7cb3de6); todo trozo nuevo sale de HUMO.py
# (sha 69fcfcb2473fdbf6) salvo las llaves P_*. Con las llaves en 0 es MINIMO bit a bit (identidad.py).

TOPE = 1.5         # CAP: lo que sirve se come hasta el tope real de la reserva (la raiz paraba en rep_umbral + 0.25)
PISO = 0.35        # RECICLA: limpiar no deja la reserva golpeada por debajo de esto
PRUEBA = 0.5       # prueba una letra desconocida solo si E y Ag > PRUEBA
PEN_OTRO = 0.35    # factor al blanco si otro cuerpo esta estrictamente mas cerca
D0 = 3.0           # suavizado de la distancia en el puntaje del blanco
P_PIZARRA = 1      # llave de la pieza 1 (pizarra de HUMO: escucha y difunde); 0 = MINIMO


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
            if x >= TOPE: continue
            u = 4.0 if x < 0.3 else (2.0 if x < self.U else 1.0)
            g += u * min(v[j], TOPE - x)
        return g

    def _limpia(self, v, lev):
        """RECICLA: una letra conocida que no sube nada se muerde para que el mundo reponga, si el golpe es costeable."""
        return not (v > 0).any() and all(lev[j] + v[j] >= PISO for j in (0, 1) if v[j] < 0)

    def _quiere(self, k, lev, criando):
        v = self._val(k)
        if self._gana(v, lev): return True
        if criando: return False                      # BANCO: cerca de criar no se prueba ni se limpia
        return min(lev) > PRUEBA if v is None else self._limpia(v, lev)

    def actua(self, obs):
        pos = obs['pos']; lev = (float(obs['E']), float(obs['Ag'])); objs = obs['objs']
        if P_PIZARRA: self._escucha(obs['pizarra'])
        otros = [c[1] for c in obs['cuerpos'] if c[0] != self.yo]
        criando = min(lev) >= self.U                  # BANCO: los dos modos
        mejor = None; desc = None; sucio = None
        for x, k in objs.items():
            d = self._dist(pos, x); v = self._val(k)
            g = self._gana(v, lev)
            if g:
                s = g / (d + D0)
                if otros and min(self._dist(o, x) for o in otros) < d: s *= PEN_OTRO
                if mejor is None or s > mejor[0]: mejor = (s, x)
            elif not self._quiere(k, lev, criando): continue
            elif v is None:
                if desc is None or d < desc[0]: desc = (d, x)
            elif sucio is None or d < sucio[0]: sucio = (d, x)
        if mejor is not None: tgt = mejor[1]
        elif desc is not None: tgt = desc[1]
        elif sucio is not None: tgt = sucio[1]        # RECICLA: sin nada mejor que hacer, va a lo malo mas cercano
        else: tgt = self._hueco(pos, otros)
        self.blanco = tgt
        mov = self._dir(pos, tgt)
        p2 = (pos + mov) % self.L
        muerde = False
        if p2 in objs:
            muerde = bool(self._quiere(objs[p2], lev, criando))
        return dict(mov=mov, muerde=muerde, escribe=self._difunde() if P_PIZARRA else None)

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
