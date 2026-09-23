"""carros/O4.py — escuderia O4 (combo Opus: disenador, biologo, critico). Carrera de escuderias, RONDA 2 (ENMIENDA 5). VERSION FINAL (v5).

MISION: llegar a la AGI por este camino.

BASE: carros/O1.py (sha 99436afa2715f028), copiado entero. Con M2 = False el carro es O1 decision por decision
(arnes de identidad bit a bit contra O1 en la pista, fundador limpio; ver bitacoras/O4.md). Con fundador limpio impuesto
por la pista, O1 == CTRL_O1_FUNDBORRA, asi que el control "M2 = False" ES el rival O1 de la ronda 2.

v5 (DISENADOR, tras la critica del CRITICO-PROBADOR sobre la v4; declarado en la bitacora):
  - Se QUITAN M1 (modos ULTIMO/OBRERA, biologo), M4 ("lo escaso es lo bueno", disenador) y el cambio v2 (a).
    Motivo (medido en los humos de la v4, no en semillas nuevas): en el mundo sucio casi todos los cuerpos tienen cola 0
    -> modo ULTIMO -> la limpieza exige que la necesidad golpeada quede >= 0.60 (O1: 0.20). Es casi CTRL_O1_SINLIMPIA:
    muertes por hambre/sed 40-52 % (O1-FUNDBORRA 15 %), fundadores en [10k,30k) en 33 % de linajes (O1 12 %).
  - Queda SOLO M2 (relevo, biologo) con dos cambios:
    (1) COLA_S = 6 (era 3): el relevo solo se dispara con >= 6 hijos esperando. Razon fijada ANTES de los humos de la v5:
        en el mundo sucio ~60 % de los hijos muere sin parir; 0.6^3 = 0.22 de agotar la cola tras un relevo, 0.6^6 = 0.05.
        En el mundo sucio la cola casi nunca llega a 6 -> el carro es O1 exacto (lo que pidio el critico, sin mirar el mundo).
    (2) Se quita la condicion ">= 1 parto en esta vida" (bug de la "obrera recien nacida", critico): un cuerpo que tiene
        >= COLA_S hijos detras a los EDAD_S pasos se retira aunque no haya parido (el linaje ya tiene su reserva).
  M2 (relevo): edad del cuerpo >= EDAD_S y cola >= COLA_S -> SENESCENTE hasta morir: no come lo bueno (lo deja) y
    muerde lo malo conocido, sin piso. Sigue aceptando partos. DECLARADO: es una MUERTE PROGRAMADA. Sin ella un O1 en un
    mundo abundante (pista con FABRICA) es casi inmortal y no evaluable (ERR-99), y sus hijos no nacen nunca. El reloj
    pone D (y con F fijo el R0 real = (D-F)/(D+1) sube con D): por eso al lado del R0 se leen los fundadores por 1e5 pasos.
    Control que decide (critico): M2 = False (= O1). Control que separa la limpieza del senescente: SENESCE_LIMPIA = False.
  El carro cuenta SU cola sin leer nada prohibido: +1 en al_parir (tope 200, como la pista), -1 en nace() de un hijo;
  una instancia nueva (t=0 o fundador limpio) arranca con cola 0. Se re-sincroniza con info['cola'] de quiere_parir
  (interfaz publica) y cuenta los desajustes en salida().
  No escribe ni lee la pizarra. No usa ctx['rng'].
"""
import numpy as np

MARGEN = 0.25      # muerde lo bueno si la necesidad que sube esta bajo rep_umbral + MARGEN
PRUEBA = 0.5       # prueba una letra desconocida solo si E y Ag > PRUEBA
PEN_OTRO = 0.35    # factor al blanco si otro cuerpo esta estrictamente mas cerca
D0 = 3.0           # suavizado de la distancia en el puntaje
PISO = 0.2         # v2: la limpieza no baja la necesidad golpeada de aqui (si la ventana de parto no corre)

# ---- M2 (biologo; v5: COLA_S 6 y sin exigir parto) -- fijado ANTES de los humos de la v5
M2 = True
EDAD_S = 3000
COLA_S = 6
SENESCE_LIMPIA = True   # control CTRL_SENESCE_SINLIMPIA = esta linea en False
COLA_MAX = 200          # cola_max publico de la pista


class Carro:
    def __init__(self, ctx):
        self.L = int(ctx['L']); self.U = float(ctx['rep_umbral']); self.rng = ctx['rng']
        self.yo = ctx['id']
        self.suma = {}; self.n = {}          # memoria del LINAJE: letra -> suma de dS, numero de mordidas
        self.blanco = None
        self.cola = 0; self.edad = 0; self.sen = False
        self.st = dict(mord={}, pruebas=0, sin_blanco=0, pasos=0, cuerpos=0, partos=0, limpias=0,
                       senescentes=0, pasos_S=0, mordidas_S=0, cola_desajuste=0, muertes=0)

    # ------------------------------------------------------------ memoria
    def _val(self, k):
        if k not in self.n: return None
        return self.suma[k] / self.n[k]

    def _malo(self, k):
        v = self._val(k)
        return v is not None and bool((v < 0).any())

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
        """v2 LIMPIEZA (O1): morder algo que dania solo si el golpe cae en una necesidad que lo aguanta (si la ventana
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
        if M2:
            self.edad += 1
            if not self.sen and self.edad >= EDAD_S and self.cola >= COLA_S:
                self.sen = True; self.st['senescentes'] += 1
            if self.sen:
                self.st['pasos_S'] += 1
                return self._senescente(obs)
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
        # v2 (O1): nada util en el mundo y hay necesidad -> limpiar (morder lo malo costeable mas cercano)
        limpia = mejor is None and min(lev) < self.U + MARGEN
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

    def _senescente(self, obs):
        """M2: no come lo bueno; va a lo malo conocido mas cercano y lo muerde sin piso (si SENESCE_LIMPIA)."""
        pos = obs['pos']; objs = obs['objs']
        otros = [c[1] for c in obs['cuerpos'] if c[0] != self.yo]
        sucio = None
        if SENESCE_LIMPIA:
            for x, k in objs.items():
                if self._malo(k):
                    d = self._dist(pos, x)
                    if sucio is None or d < sucio[0]: sucio = (d, x)
        tgt = sucio[1] if sucio is not None else self._hueco(pos, otros)
        self.blanco = tgt
        mov = self._dir(pos, tgt)
        p2 = (pos + mov) % self.L
        muerde = bool(SENESCE_LIMPIA and p2 in objs and self._malo(objs[p2]))
        if muerde: self.st['mordidas_S'] += 1
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
        self.st['muertes'] += 1
        return None

    def al_parir(self, info):
        self.st['partos'] += 1
        self.cola = min(self.cola + 1, COLA_MAX)
        return {k: (self.suma[k].copy(), self.n[k]) for k in self.n}

    def nace(self, info):
        self.st['cuerpos'] += 1; self.blanco = None
        self.edad = 0; self.sen = False
        if info.get('fundador'): self.cola = 0
        else: self.cola = max(self.cola - 1, 0)
        m = info.get('memoria')
        if m:
            for k, (s, n) in m.items():
                if k not in self.n: self.suma[k] = np.asarray(s, float).copy(); self.n[k] = int(n)

    def quiere_parir(self, info):
        c = int(info.get('cola', self.cola))
        if c != self.cola: self.st['cola_desajuste'] += 1; self.cola = c
        return True

    def salida(self):
        return dict(tabla={k: [round(float(z), 3) for z in self._val(k)] for k in self.n}, n={k: int(v) for k, v in self.n.items()},
                    cola_propia=self.cola, **{k: v for k, v in self.st.items()})


def crea(ctx):
    return Carro(ctx)
