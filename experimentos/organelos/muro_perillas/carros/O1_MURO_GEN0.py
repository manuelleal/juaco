"""O1_MURO_GEN0.py — muro_perillas: O1 con 6 mecanismos (MARGEN, PRUEBA, PEN_OTRO, PISO, LIMPIA, HUECO) como GENES-DOSIS heredables.
GENERADO por experimentos/organelos/muro_perillas/construye_muro_perillas.py desde carrera_escuderias/carros/O1.py (sha 99436afa2715f028).
NO editar a mano. PERILLAS = 0. Con PERILLAS = 0 es O1 bit a bit; con los genes de FABRICA es O1; con LIMPIA 0 es CTRL_O1_SINLIMPIA.

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

PERILLAS = 0   # muro_perillas: LA UNICA LINEA QUE CAMBIA ENTRE VARIANTES (0 = O1 bit a bit)
SIEMBRA = None; PS_SEMILLA = 0; PS_SIGMA = 0.03; PS_DELTA = 0.01; PS_LEE = 1; PS_CAMARA = 1; PS_POR_LINAJE = None; PS_MUTA = (0,); PS_TOPE = None   # muro_perillas: PS_TOPE = tope de LECTURA de MARGEN (brazo pur; None = sin tope); los fija el RUNNER por corrida (SIEMBRA None = PS_BASE; PS_LEE 0 = genes NEUTROS; PS_POR_LINAJE = pista mixta; PS_MUTA = genes que mutan)
_PS_CNT = {}; _TEL = {}; _VIVO = {}   # muro_perillas: instancias por linaje, telemetria de SOLO ESCRITURA y genoma del cuerpo actual de cada linaje (el runner los borra antes de cada run)
PS_GENES = ('MARGEN', 'PRUEBA', 'PEN_OTRO', 'PISO', 'LIMPIA', 'HUECO'); PS_BASE = (0.03, 0.5, 0.35, 0.2, 1.0, 1.0); PS_CLIP = ((0.0, 0.6), (0.0, 1.5), (0.0, 1.5), (0.0, 1.0), (0.0, 1.5), (0.0, 1.5))
PS_APAGADO = (0.0, 0.5, 1.0, 1.0, 0.0, 0.0); PS_FABRICA = (0.25, 0.5, 0.35, 0.2, 1.0, 1.0)
_PS_M64 = 18446744073709551615


class Carro:
    def __init__(self, ctx):
        self.L = int(ctx['L']); self.U = float(ctx['rep_umbral']); self.rng = ctx['rng']
        self.yo = ctx['id']
        self.suma = {}; self.n = {}          # memoria del LINAJE: letra -> suma de dS, numero de mordidas
        self.blanco = None
        self.st = dict(mord={}, pruebas=0, sin_blanco=0, pasos=0, cuerpos=0, partos=0, limpias=0)
        self.MARGEN, self.PRUEBA, self.PEN_OTRO, self.PISO, self.LIMPIA, self.HUECO = MARGEN, PRUEBA, PEN_OTRO, PISO, 1, 1   # muro_perillas: mecanismos por cuerpo (fabrica)
        if PERILLAS: self._ps_init(ctx)   # muro_perillas: genes del fundador (por linaje, de la camara, de SIEMBRA o de PS_BASE), mutados

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
            if x >= self.U + self.MARGEN: continue
            u = 4.0 if x < 0.3 else (2.0 if x < self.U else 1.0)
            g += u * min(v[j], self.U + 0.5 - x)
        return g

    def _quiere(self, k, lev, limpia=False):
        v = self._val(k)
        if v is None: return min(lev) > self.PRUEBA
        g = self._gana(v, lev)
        if g: return True
        return limpia and self._costeable(v, lev)

    def _costeable(self, v, lev):
        """v2 LIMPIEZA: morder algo que dania solo si el golpe cae en una necesidad que lo aguanta (si la ventana
        de parto corre, no la rompe; si no corre, no baja de PISO) y no toca la necesidad que se busca."""
        if not (v < 0).any(): return False
        for j in (0, 1):
            if v[j] < 0:
                piso = self.U if min(lev) >= self.U else self.PISO
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
                if min(lev) > self.PRUEBA and (desc is None or d < desc[0]): desc = (d, x)
                continue
            g = self._gana(v, lev)
            if not g: continue
            s = g / (d + D0)
            if otros and min(self._dist(o, x) for o in otros) < d: s *= self.PEN_OTRO
            if mejor is None or s > mejor[0]: mejor = (s, x)
        # v2: nada util en el mundo y hay necesidad -> limpiar (morder lo malo costeable mas cercano)
        limpia = bool(self.LIMPIA) and mejor is None and min(lev) < self.U + self.MARGEN   # muro_perillas: LIMPIA 0 == CTRL_O1_SINLIMPIA (limpia = False)
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
            tgt = (self._hueco(pos, otros) if self.HUECO else pos); self.st['sin_blanco'] += 1   # muro_perillas: HUECO 0 = se queda quieto
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
        if PERILLAS and info['t'] % 1000 == 0: self._ps_tel(info['t'])   # muro_perillas: genes del vivo (solo escritura)
        return None

    def muere(self, info):
        return None

    def al_parir(self, info):
        self.st['partos'] += 1
        _m = {k: (self.suma[k].copy(), self.n[k]) for k in self.n}
        if PERILLAS: _m['_gen'] = (self._ps_muta(self._gen), self._prof + 1); _TEL.setdefault(self._psi, {})['partos'] = _TEL[self._psi].get('partos', 0) + 1
        return _m

    def nace(self, info):
        self.st['cuerpos'] += 1; self.blanco = None
        m = info.get('memoria')
        if PERILLAS and m and '_gen' in m: m = dict(m); _g = m.pop('_gen'); self._prof = int(_g[1]); self._ps_pon(_g[0])   # muro_perillas: el hijo toma sus genes
        if m:
            for k, (s, n) in m.items():
                if k not in self.n: self.suma[k] = np.asarray(s, float).copy(); self.n[k] = int(n)

    def quiere_parir(self, info):
        return True

    def salida(self):
        return dict(tabla={k: [round(float(z), 3) for z in self._val(k)] for k in self.n}, n={k: int(v) for k, v in self.n.items()},
                    **{k: v for k, v in self.st.items()})

    # ================================================================ muro_perillas: 6 mecanismos de O1 como GENES-DOSIS heredables (arrancan en 0)
    def _ps_init(self, ctx):
        i = int(ctx['indice']); c = _PS_CNT.get(i, 0); _PS_CNT[i] = c + 1; self._psi = i; self._psc = c
        self._pss = ((int(PS_SEMILLA) * 1000003 + i * 10007 + c) * 2654435761 + 7703) & _PS_M64
        for _ in range(4): self._ps_u()
        otros = [_VIVO[j] for j in sorted(_VIVO) if j != i] if (PS_CAMARA and c > 0) else []
        if PS_POR_LINAJE is not None:   # PISTA MIXTA: cada linaje con SU genoma (fijo, tambien al refundar)
            b0 = [float(v) for v in PS_POR_LINAJE[i]]; p0 = 0; self._psfund = 3
        elif otros:   # CAMARA: la refundacion copia (mutado) el genoma del cuerpo actual de OTRO linaje al azar
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
        """UNA mutacion por nacimiento, en UN gen al azar: d - PS_DELTA + N(0, PS_SIGMA), recortado. Los demas se copian igual."""
        out = [float(x) for x in b]; j = PS_MUTA[int(self._ps_u() * len(PS_MUTA)) % len(PS_MUTA)]   # solo los genes de PS_MUTA mutan (serie: solo MARGEN)
        z = math.sqrt(-2.0 * math.log(self._ps_u())) * math.cos(2.0 * math.pi * self._ps_u())
        out[j] = float(min(max(out[j] - PS_DELTA + PS_SIGMA * z, PS_CLIP[j][0]), PS_CLIP[j][1]))
        return out

    def _ps_pon(self, g):
        """El cuerpo lee las constantes CRUDAS; LIMPIA y HUECO: regla activa si el gen > 0.5."""
        self._gen = [float(x) for x in g]
        _VIVO[self._psi] = (list(self._gen), int(self._prof))
        d = self._gen if PS_LEE else list(PS_FABRICA)   # PS_LEE 0: se heredan y mutan pero NO se leen (el cuerpo decide como O1)
        self.MARGEN, self.PRUEBA, self.PEN_OTRO, self.PISO = (d[0] if PS_TOPE is None else min(d[0], float(PS_TOPE))), d[1], d[2], d[3]   # pur: el cuerpo lee min(gen, tope); el gen heredado no se toca
        self.LIMPIA = int(d[4] > 0.5); self.HUECO = int(d[5] > 0.5)

    def _ps_tel(self, t):
        _TEL.setdefault(self._psi, {}).setdefault('vivos', []).append([int(t), list(self._gen), int(self._psc), int(self._prof)])


def crea(ctx):
    return Carro(ctx)
