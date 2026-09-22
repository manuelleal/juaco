"""carros/CTRL_O1_SINLIMPIA.py — CARRO DE CONTROL (ENMIENDA 4, serie S-SIN-LIMPIEZA). NO es una escuderia.

Copia de carros/O1.py (sha 99436afa2715f028) con UNA sola linea cambiada: la bandera `limpia` es siempre False. Efecto:
nunca elige como blanco lo malo costeable (`sucio`) ni lo muerde (`_quiere(..., limpia=False)` solo muerde lo bueno que
sirve o una letra desconocida a probar). Cuando no queda nada util hace lo que O1 haria sin limpieza: va a una letra
por probar si la hay; si no, se coloca en el centro del hueco mas grande entre los otros cuerpos (su regla de espera).
Todo lo demas (memoria del linaje, blanco, penalizacion por otro mas cerca, parto, herencia) es O1 byte a byte.
"""
"""carros/O1.py — escuderia O1 (Opus). Carrera de escuderias, ronda 1.

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
import numpy as np

MARGEN = 0.25      # muerde lo bueno si la necesidad que sube esta bajo rep_umbral + MARGEN
PRUEBA = 0.5       # prueba una letra desconocida solo si E y Ag > PRUEBA
PEN_OTRO = 0.35    # factor al blanco si otro cuerpo esta estrictamente mas cerca
D0 = 3.0           # suavizado de la distancia en el puntaje
PISO = 0.2         # v2: la limpieza no baja la necesidad golpeada de aqui (si la ventana de parto no corre)


class Carro:
    def __init__(self, ctx):
        self.L = int(ctx['L']); self.U = float(ctx['rep_umbral']); self.rng = ctx['rng']
        self.yo = ctx['id']
        self.suma = {}; self.n = {}          # memoria del LINAJE: letra -> suma de dS, numero de mordidas
        self.blanco = None
        self.st = dict(mord={}, pruebas=0, sin_blanco=0, pasos=0, cuerpos=0, partos=0, limpias=0)

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
            g = self._gana(v, lev)
            if not g: continue
            s = g / (d + D0)
            if otros and min(self._dist(o, x) for o in otros) < d: s *= PEN_OTRO
            if mejor is None or s > mejor[0]: mejor = (s, x)
        # v2: nada util en el mundo y hay necesidad -> limpiar (morder lo malo costeable mas cercano)
        limpia = False   # CTRL_O1_SINLIMPIA: LIMPIEZA APAGADA (O1: limpia = mejor is None and min(lev) < self.U + MARGEN)
        sucio = None
        if limpia:
            for x, k in objs.items():
                v = self._val(k)
                if v is not None and self._costeable(v, lev):
                    d = self._dist(pos, x)
                    if sucio is None or d < sucio[0]: sucio = (d, x)
        if mejor is not None: tgt = mejor[1]
        elif desc is not None: tgt = desc[1]
        elif sucio is not None: tgt = sucio[1]
        else:
            tgt = self._hueco(pos, otros); self.st['sin_blanco'] += 1
        self.blanco = tgt
        mov = self._dir(pos, tgt)
        p2 = (pos + mov) % self.L
        muerde = False
        if p2 in objs:
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
        self.suma[k] = self.suma.get(k, np.zeros(2)) + dS; self.n[k] = self.n.get(k, 0) + 1
        self.st['mord'][k] = self.st['mord'].get(k, 0) + 1

    def fin_paso(self, info):
        return None

    def muere(self, info):
        return None

    def al_parir(self, info):
        self.st['partos'] += 1
        return {k: (self.suma[k].copy(), self.n[k]) for k in self.n}

    def nace(self, info):
        self.st['cuerpos'] += 1; self.blanco = None
        m = info.get('memoria')
        if m:
            for k, (s, n) in m.items():
                if k not in self.n: self.suma[k] = np.asarray(s, float).copy(); self.n[k] = int(n)

    def quiere_parir(self, info):
        return True

    def salida(self):
        return dict(tabla={k: [round(float(z), 3) for z in self._val(k)] for k in self.n}, n={k: int(v) for k, v in self.n.items()},
                    **{k: v for k, v in self.st.items()})


def crea(ctx):
    return Carro(ctx)
