"""decision.py — Experimento B "decidir" (5-oct-2026, exploracion sin preregistro formal; predicciones en PREDICCIONES.md).
MISION: llegar a la AGI por este camino (JUACO: organismo minimo, reglas locales, con controles).

PAN   = predictor de consecuencias (estado, accion -> estado siguiente), MLP entrenado con gradiente UNA vez sobre el mundo
        original y CONGELADO. Paso 0 de cordura: debe predecir >= 0.98 antes de cualquier cambio.
CARNE = bloque de celulas JUACO (compuerta por estado propio, pago por acierto, olvido por escasez, suelta la correccion
        cuando el pan vuelve a acertar) que corrige al pan donde el mundo cambio. Dos formas:
        (ii) 'pred'  : la celula dice DONDE se cae de verdad (desplazamiento observado) -> el planificador usa pan + correccion.
        (i)  'costo' : la celula solo dice "ese paso no vale" (la arista imaginada cuesta como quedarse quieto) -> el
                       planificador evita la arista. Es el "critico" que corrige el costo de lo imaginado.
PLANIFICADOR = iteracion de valor sobre la tabla imaginada (64 estados x 4 acciones), meta = ultimo sitio donde comio.
        Si llega a la meta y no hay comida, olvida la meta y explora (ir a lo menos visitado).

MUNDO: rejilla NxN (8x8), sin muros; 4 acciones; chocar con el borde = quedarse. Una comida fija en un sitio, VISIBLE
        (el agente observa su posicion y la de la comida, como la "imagen de la meta" de V-JEPA 2-AC); al comer (+1) el
        agente se teletransporta a una casilla al azar y la comida sigue en su sitio. Eventos:
        'sitio' : la comida se muda a otra casilla (todos lo ven: lo que cambia es la META).
        'regla' : dos acciones intercambian su efecto (acumulativo) en TODO el mundo (o solo en la mitad izquierda,
                  --regional). Nadie lo ve: el pan congelado queda parcialmente EQUIVOCADO.
        (Humo previo con comida escondida: todos los brazos se reducian a buscar a ciegas 1 casilla entre 64; se cambio.)

BRAZOS (mismas semillas):
  1 regla_mano     : regla a mano: ir hacia la comida con el mapa ORIGINAL de acciones (conocimiento del disenador);
                     si el ultimo paso no me movio (choque), accion menos probada en este estado (reflejo JUACO).
  2 plan_pan       : planificador con el pan congelado solo, meta = comida visible.
  3 q_tabular      : Q-learning tabular sobre la posicion RELATIVA (dx, dy) de la comida (generaliza entre sitios), eps-greedy.
  4 plan_pan_grad  : TECHO: planificador + pan reentrenado en linea con gradiente (un paso de Adam por transicion); cuenta su costo.
  5 bloque_solo    : celulas (posicion relativa, accion, energia) sin planificador: pago por camino cuando se come; manda la mas rica.
  6 plan_pan_cel   : LA PROPUESTA: pan congelado + planificador + bloque (ii) que corrige la prediccion.
  6c plan_pan_cel_costo : lo mismo con bloque (i) que corrige el costo.
  7 plan_pan_cel_baraj : (6) con el pago barajado (control).
  8 sueno          : (6) + cada 250 pasos el pan absorbe con gradiente lo que las celulas corrigieron (con pseudo-ensayo) y las libera.
MEDIDAS: comida por paso; pasos hasta la 1a y la 3a comida tras cada evento (sitio y regla por separado); ops por decision;
         memoria (celulas / entradas / parametros entrenables); rompe lo sabido = acierto del pan (o pan+celulas) sobre las
         transiciones del mundo ORIGINAL al final (solo tiene sentido en los que tocan el pan) y acierto del modelo combinado
         sobre el mundo ACTUAL al final.
"""
import numpy as np, json, time, argparse, os, sys

MOV = np.array([[0, -1], [0, 1], [-1, 0], [1, 0]])   # arriba, abajo, izquierda, derecha (dx, dy)
A = 4


# ----------------------------------------------------------------------------------------------- mundo
class Mundo:
    def __init__(self, seed, N=8, regional=False):
        self.rng = np.random.default_rng(seed); self.N = N; self.S = N * N; self.regional = regional
        self.mapa = np.arange(A)                 # accion -> efecto (indice en MOV); cambia con 'regla'
        self.mapa_reg = np.arange(A)             # efecto en la region cambiada (mitad izquierda) si regional
        self.comida = int(self.rng.integers(self.S)); self.pos = int(self.rng.integers(self.S))
        while self.pos == self.comida: self.pos = int(self.rng.integers(self.S))

    def xy(self, s): return s % self.N, s // self.N
    def sid(self, x, y): return y * self.N + x

    def efecto(self, s, a):
        x, y = self.xy(s)
        m = self.mapa_reg if (self.regional and x < self.N // 2) else self.mapa
        dx, dy = MOV[m[a]]
        return self.sid(min(max(x + dx, 0), self.N - 1), min(max(y + dy, 0), self.N - 1))

    def tabla(self):
        return np.array([[self.efecto(s, a) for a in range(A)] for s in range(self.S)])

    def paso(self, a):
        s2 = self.efecto(self.pos, a); come = (s2 == self.comida)
        self.pos = s2
        if come:
            self.pos = int(self.rng.integers(self.S))
            while self.pos == self.comida: self.pos = int(self.rng.integers(self.S))
        return s2, come

    def muda_sitio(self):
        c = int(self.rng.integers(self.S))
        while c == self.comida or c == self.pos: c = int(self.rng.integers(self.S))
        self.comida = c

    def cambia_regla(self):
        i, j = self.rng.choice(A, 2, replace=False)
        m = self.mapa_reg if self.regional else self.mapa
        m[i], m[j] = m[j], m[i]


# ----------------------------------------------------------------------------------------------- pan (MLP con Adam)
class Pan:
    """(onehot estado + onehot accion) -> onehot estado siguiente. Retropropagacion a mano, Adam."""
    def __init__(self, seed, S, Hd=64, lr=3e-3, tipo='onehot'):
        r = np.random.default_rng(seed); self.S = S; self.N = int(round(np.sqrt(S))); self.tipo = tipo; self.lr = lr
        self.D = S + A if tipo == 'onehot' else 2 + A       # 'coord': (x/N, y/N, onehot a): puede generalizar entre posiciones
        if tipo == 'coord': Hd = 128
        self.p = {'W1': r.normal(0, 1 / np.sqrt(self.D), (self.D, Hd)), 'b1': np.zeros(Hd),
                  'W2': r.normal(0, 1 / np.sqrt(Hd), (Hd, S)), 'b2': np.zeros(S)}
        self.m = {k: np.zeros_like(v) for k, v in self.p.items()}; self.v = {k: np.zeros_like(v) for k, v in self.p.items()}
        self.t = 0; self.ops_fwd = 2 * (self.D * Hd + Hd * S); self.ops = 0
        self.X_all = np.array([self.x(s, a) for s in range(S) for a in range(A)])

    def x(self, s, a):
        v = np.zeros(self.D)
        if self.tipo == 'onehot': v[s] = 1; v[self.S + a] = 1
        else: v[0] = (s % self.N) / self.N; v[1] = (s // self.N) / self.N; v[2 + a] = 1
        return v

    def fwd(self, X):
        H = np.maximum(X @ self.p['W1'] + self.p['b1'], 0); L = H @ self.p['W2'] + self.p['b2']
        self.ops += self.ops_fwd * X.shape[0]; return H, L

    def predice(self, s, a): return int(np.argmax(self.fwd(self.x(s, a)[None])[1][0]))

    def tabla(self):
        """prediccion para todos los (s,a): (S, A)."""
        return np.argmax(self.fwd(self.X_all)[1], 1).reshape(self.S, A)

    def paso(self, X, y, lr=None):
        H, L = self.fwd(X); B = X.shape[0]
        pr = np.exp(L - L.max(1, keepdims=True)); pr /= pr.sum(1, keepdims=True)
        dl = pr; dl[np.arange(B), y] -= 1; dl /= B
        g = {'W2': H.T @ dl, 'b2': dl.sum(0)}
        dH = (dl @ self.p['W2'].T) * (H > 0)
        g['W1'] = X.T @ dH; g['b1'] = dH.sum(0)
        self.t += 1; lr = self.lr if lr is None else lr
        for k in self.p:
            self.m[k] = 0.9 * self.m[k] + 0.1 * g[k]; self.v[k] = 0.999 * self.v[k] + 0.001 * g[k] ** 2
            self.p[k] -= lr * (self.m[k] / (1 - 0.9 ** self.t)) / (np.sqrt(self.v[k] / (1 - 0.999 ** self.t)) + 1e-8)
        self.ops += 2 * self.ops_fwd * B

    def copia(self):
        c = Pan.__new__(Pan); c.__dict__.update({k: v for k, v in self.__dict__.items()})
        c.p = {k: v.copy() for k, v in self.p.items()}
        c.m = {k: np.zeros_like(v) for k, v in self.p.items()}; c.v = {k: np.zeros_like(v) for k, v in self.p.items()}
        c.t = 0; c.ops = 0; return c

    def n_param(self): return sum(v.size for v in self.p.values())


def entrena_pan(mundo, seed, pasos=1500, tipo='onehot'):
    pan = Pan(seed, mundo.S, tipo=tipo); T = mundo.tabla().reshape(-1); rng = np.random.default_rng(seed + 7)
    if tipo == 'coord': pasos = 6000
    for k in range(pasos):
        idx = rng.integers(0, mundo.S * A, 64); pan.paso(pan.X_all[idx], T[idx], lr=3e-3 if k < pasos * 0.8 else 1e-3)
    acc = float(np.mean(pan.tabla().reshape(-1) == T)); pan.ops = 0
    return pan, acc


# ----------------------------------------------------------------------------------------------- planificador
def planifica(tabla, meta, S, sweeps=40, gamma=0.95):
    """iteracion de valor sobre la tabla imaginada: V(meta)=0; cada paso cuesta 1. Devuelve (politica, V, ops)."""
    V = np.zeros(S); ops = 0
    for _ in range(sweeps):
        Q = 1 + gamma * V[tabla]            # (S, A)
        Q[meta] = 0
        Vn = Q.min(1); ops += S * A * 2
        if np.allclose(Vn, V): V = Vn; break
        V = Vn
    Q = 1 + gamma * V[tabla]; Q[meta] = 0
    return Q, V, ops


# ----------------------------------------------------------------------------------------------- bloque de celulas (ii) y (i)
class Bloque:
    """celula = prototipo en rasgos (x/N, y/N, 2*onehot(a)) + correccion + energia + confianza.
    modo 'pred': la correccion es el desplazamiento observado (dx, dy): dice DONDE se cae de verdad.
    modo 'costo': la correccion es "esa arista no vale": el planificador la trata como quedarse quieto.
    Compuerta propia: pisa si se parece (s > theta), difiere del pan y ya cobro. Cobra solo si piso y acerto donde el pan
    fallaba. Suelta la correccion (muere) si piso donde el pan acertaba. Paga por existir. Nace donde el pan falla sin celula."""
    def __init__(self, N, C, seed, modo='pred', theta=0.5, sigma=0.5, c_exist=0.002, pago=1.0, castigo=0.5, eta=0.3,
                 barajar=False, E0=1.0, nacer_azar=False):
        self.nacer_azar = nacer_azar; self.N = N; self.C = C; self.modo = modo; self.rng = np.random.default_rng(seed + 777)
        self.dim = 2 + A; self.W = np.zeros((0, self.dim)); self.Dxy = np.zeros((0, 2), int); self.E = np.zeros(0)
        self.conf = np.zeros(0); self.theta, self.sigma, self.c_exist, self.pago, self.castigo, self.eta = theta, sigma, c_exist, pago, castigo, eta
        self.barajar, self.E0 = barajar, E0; self.nac = self.mue = self.pisadas = 0; self.ops = 0; self.cambio = True
        self.ep = []   # episodios (s, a, s2) para el sueno

    @property
    def n(self): return self.W.shape[0]

    def rasgos(self, s, a):
        f = np.zeros(self.dim); f[0] = (s % self.N) / self.N; f[1] = (s // self.N) / self.N; f[2 + a] = 2.0; return f

    def _sim(self, f):
        self.ops += 4 * self.W.size
        return np.exp(-np.sum((self.W - f) ** 2, 1) / (2 * self.sigma ** 2))

    def aplica(self, s, a, s_pan):
        """que diria el bloque para (s,a) dado lo que dice el pan. Devuelve (s_corregido, j_celula, cand)."""
        if not self.n: return s_pan, -1, np.zeros(0, bool)
        f = self.rasgos(s, a); sim = self._sim(f)
        x, y = s % self.N, s // self.N
        if self.modo == 'pred':
            tx = np.clip(x + self.Dxy[:, 0], 0, self.N - 1); ty = np.clip(y + self.Dxy[:, 1], 0, self.N - 1)
            pred = ty * self.N + tx
        else:
            pred = np.full(self.n, s)                                      # 'costo': la arista vale como quedarse
        cand = sim > self.theta
        act = cand & (pred != s_pan) & (self.conf > 0)
        if act.any():
            j = int(np.argmax(np.where(act, sim, -1))); return int(pred[j]), j, cand
        return s_pan, -1, cand

    def tabla_corregida(self, tabla_pan):
        """tabla imaginada por pan + correcciones de las celulas (para el planificador). Vectorizado: misma regla que aplica()."""
        T = tabla_pan.copy()
        if not self.n: return T
        S = T.shape[0]; N = self.N
        ss = np.repeat(np.arange(S), A); aa = np.tile(np.arange(A), S)
        F = np.zeros((S * A, self.dim)); F[:, 0] = (ss % N) / N; F[:, 1] = (ss // N) / N; F[np.arange(S * A), 2 + aa] = 2.0
        d2 = ((F[:, None, :] - self.W[None, :, :]) ** 2).sum(2); sim = np.exp(-d2 / (2 * self.sigma ** 2)); self.ops += 4 * F.size * self.n
        if self.modo == 'pred':
            tx = np.clip((ss % N)[:, None] + self.Dxy[None, :, 0], 0, N - 1); ty = np.clip((ss // N)[:, None] + self.Dxy[None, :, 1], 0, N - 1)
            pred = ty * N + tx
        else:
            pred = np.repeat(ss[:, None], self.n, 1)
        sp = tabla_pan.reshape(-1)
        act = (sim > self.theta) & (pred != sp[:, None]) & (self.conf[None, :] > 0)
        j = np.argmax(np.where(act, sim, -1), 1); hay = act.any(1)
        out = sp.copy(); out[hay] = pred[np.arange(S * A), j][hay]
        return out.reshape(S, A)

    def aprende(self, s, a, s_pan, s2):
        """tras observar la transicion real (s, a) -> s2, con la prediccion del pan s_pan."""
        self.cambio = False
        r, j, cand = self.aplica(s, a, s_pan); f = self.rasgos(s, a)
        if self.n:
            self.E -= self.c_exist
            if j >= 0:
                self.pisadas += 1
                k = j if not self.barajar else int(self.rng.integers(self.n))
                if r == s2 and s_pan != s2:                               # mi correccion valio: cobro
                    grupo = np.where(cand)[0]
                    if self.barajar: grupo = self.rng.choice(self.n, len(grupo), replace=False)
                    self.E[grupo] += self.pago / len(grupo); self.conf[grupo] += 1.0 / len(grupo)
                    self.W[k] += 0.2 * (f - self.W[k])
                elif r != s2 and s_pan == s2:                             # pise donde el pan acertaba: suelto y muero
                    self.conf[k] = 0.0; self.E[k] = -1.0; self.cambio = True
                elif r != s2:                                             # fallamos los dos: corrijo
                    self.E[k] -= self.castigo * 0.5
                    if self.modo == 'pred':
                        self.Dxy[k] = [(s2 % self.N) - (s % self.N), (s2 // self.N) - (s // self.N)]
                        self.ep[k] = (s, a, s2); self.cambio = True
                    self.W[k] += self.eta * (f - self.W[k])
            elif self.modo == 'costo' and cand.any() and s_pan == s2:
                pass
            muertas = self.E < 0
            if muertas.any(): self._mata(~muertas)
        if j < 0 and s_pan != s2:                                         # nadie piso y el pan fallo: nace una celula aqui
            if self.n >= self.C: viva = np.ones(self.n, bool); viva[int(np.argmin(self.E))] = False; self._mata(viva)
            self.W = np.vstack([self.W, f]); self.E = np.append(self.E, self.E0); self.conf = np.append(self.conf, 1.0)
            dxy = [(s2 % self.N) - (s % self.N), (s2 // self.N) - (s // self.N)]
            if self.nacer_azar: dxy = list(self.rng.integers(-1, 2, 2))        # control: nace con desplazamiento al azar
            self.Dxy = np.vstack([self.Dxy, [dxy]])
            self.ep.append((s, a, s2)); self.nac += 1; self.cambio = True

    def _mata(self, viva):
        self.mue += int((~viva).sum()); self.cambio = True
        self.W, self.Dxy, self.E, self.conf = self.W[viva], self.Dxy[viva], self.E[viva], self.conf[viva]
        self.ep = [e for e, v in zip(self.ep, viva) if v]


# ----------------------------------------------------------------------------------------------- brazos
class Agente:
    nombre = 'base'
    def __init__(self, mundo, pan, seed, C=32):
        self.m = mundo; self.pan = pan; self.rng = np.random.default_rng(seed + 31); self.C = C; self.ops = 0
        self.S = mundo.S; self.N = mundo.N; self.visitas = np.zeros((self.S, A)); self.meta = -1
    def _menos_visitado(self, s):
        v = self.visitas[s]; self.ops += A; c = np.where(v == v.min())[0]; return int(self.rng.choice(c))
    def rel(self, s, meta):
        """posicion relativa de la comida (dx, dy) en -(N-1)..N-1."""
        return (meta % self.N) - (s % self.N), (meta // self.N) - (s // self.N)
    def decide(self, s, meta): return self._menos_visitado(s)
    def aprende(self, s, a, s2, come, meta): self.visitas[s, a] += 1
    def memoria(self): return 0
    def modelo(self): return None          # tabla imaginada final (para "rompe lo sabido"), si aplica


class ReglaMano(Agente):
    """regla a mano: hacia la comida con el mapa ORIGINAL (arriba=0, abajo=1, izq=2, der=3); si choque, menos visitado."""
    nombre = '1 regla_mano'
    def __init__(self, mundo, pan, seed, C=32): super().__init__(mundo, pan, seed, C); self.choque = False
    def decide(self, s, meta):
        self.ops += A
        if self.choque: return self._menos_visitado(s)
        dx, dy = self.rel(s, meta); c = []
        if dx > 0: c.append(3)
        if dx < 0: c.append(2)
        if dy > 0: c.append(1)
        if dy < 0: c.append(0)
        return int(self.rng.choice(c)) if c else int(self.rng.integers(A))
    def aprende(self, s, a, s2, come, meta): self.visitas[s, a] += 1; self.choque = (s2 == s)


class PlanPan(Agente):
    """planificador con el pan congelado; meta = comida visible; replanifica si la meta o la tabla cambian."""
    nombre = '2 plan_pan'
    def __init__(self, mundo, pan, seed, C=32):
        super().__init__(mundo, pan, seed, C); self.T0 = pan.tabla(); self.ops += pan.ops; pan.ops = 0
        self.Q = None; self.replan = True
    def tabla(self): return self.T0
    def decide(self, s, meta):
        if meta != self.meta: self.meta = meta; self.replan = True
        if self.replan:
            self.Q, _, o = planifica(self.tabla(), self.meta, self.S); self.ops += o; self.replan = False
        q = self.Q[s]; self.ops += A; c = np.where(q == q.min())[0]; return int(self.rng.choice(c))
    def aprende(self, s, a, s2, come, meta): self.visitas[s, a] += 1
    def modelo(self): return self.tabla()


class Oraculo(PlanPan):
    """techo de rendimiento: planifica con la tabla VERDADERA del mundo (la mira cada paso; no es un rival, es la cota)."""
    nombre = '0 oraculo'
    def tabla(self):
        T = self.m.tabla()
        if not np.array_equal(T, self.T0): self.T0 = T; self.replan = True
        return self.T0
    def decide(self, s, meta):
        self.tabla(); return super().decide(s, meta)


class PlanPanGrad(PlanPan):
    """TECHO: el pan se reentrena en linea con un paso de Adam por transicion observada; replanifica con la tabla nueva."""
    nombre = '4 plan_pan_grad'
    def __init__(self, mundo, pan, seed, C=32, lr=3e-3, bufer=0, lote=32):
        super().__init__(mundo, pan.copia(), seed, C); self.lr = lr; self.Tc = self.T0.copy(); self.cuenta = 0
        self.bufer = bufer; self.lote = lote; self.B = []
    def tabla(self): return self.Tc
    def aprende(self, s, a, s2, come, meta):
        super().aprende(s, a, s2, come, meta)
        if self.bufer:                                   # bufer de repeticion: un paso de Adam sobre un lote de transiciones recientes
            self.B.append((s, a, s2)); self.B = self.B[-self.bufer:]
            idx = self.rng.integers(0, len(self.B), min(self.lote, len(self.B)))
            X = np.array([self.pan.x(self.B[i][0], self.B[i][1]) for i in idx]); y = np.array([self.B[i][2] for i in idx])
            self.pan.paso(X, y, lr=self.lr)
        else:
            self.pan.paso(self.pan.x(s, a)[None], np.array([s2]), lr=self.lr)
        self.cuenta += 1
        self.Tc = self.pan.tabla(); self.ops += self.pan.ops; self.pan.ops = 0; self.replan = True
    def memoria(self): return self.pan.n_param()


class QTab(Agente):
    """Q tabular sobre la posicion relativa (dx, dy) de la comida: (2N-1)^2 x A entradas."""
    nombre = '3 q_tabular'
    def __init__(self, mundo, pan, seed, C=32, alpha=0.3, gamma=0.95, eps=0.1, q0=0.0):
        super().__init__(mundo, pan, seed, C); M = 2 * self.N - 1; self.M = M
        self.Qt = np.full((M * M, A), q0); self.alpha, self.gamma, self.eps = alpha, gamma, eps
    def k(self, s, meta):
        dx, dy = self.rel(s, meta); return (dy + self.N - 1) * self.M + (dx + self.N - 1)
    def decide(self, s, meta):
        self.ops += A
        if self.rng.random() < self.eps: return int(self.rng.integers(A))
        q = self.Qt[self.k(s, meta)]; c = np.where(q == q.max())[0]; return int(self.rng.choice(c))
    def aprende(self, s, a, s2, come, meta):
        self.visitas[s, a] += 1; r = 1.0 if come else 0.0
        objetivo = r + (0 if come else self.gamma * self.Qt[self.k(s2, meta)].max())
        self.Qt[self.k(s, meta), a] += self.alpha * (objetivo - self.Qt[self.k(s, meta), a]); self.ops += 2 * A
    def memoria(self): return self.Qt.size


class BloqueSolo(Agente):
    """bloque JUACO sin planificador: celulas (posicion relativa, accion, energia). La celula mas rica con conf>0 manda
    (90 %); si no, menos visitado. Cuando come, las celulas del camino (ultimos 12 pasos) comparten el pago. Pagan por
    existir; sin energia mueren. Nace una celula en cada (rel, a) tomado sin celula (si no hay cupo, muere la mas pobre)."""
    nombre = '5 bloque_solo'
    def __init__(self, mundo, pan, seed, C=256, c_exist=0.01, pago=10.0, barajar=False):
        super().__init__(mundo, pan, seed, C); self.cel = {}   # (rel, a) -> [E, conf]
        self.camino = []; self.c_exist, self.pago, self.barajar = c_exist, pago, barajar; self.nac = self.mue = 0
    def decide(self, s, meta):
        r = self.rel(s, meta); cands = [(self.cel[(r, a)][0], a) for a in range(A) if (r, a) in self.cel and self.cel[(r, a)][1] > 0]; self.ops += A
        if cands and self.rng.random() > 0.1: return max(cands)[1]
        return self._menos_visitado(s)
    def aprende(self, s, a, s2, come, meta):
        self.visitas[s, a] += 1; k = (self.rel(s, meta), a)
        if k not in self.cel:
            if len(self.cel) >= self.C:
                peor = min(self.cel, key=lambda q: self.cel[q][0]); del self.cel[peor]; self.mue += 1
            self.cel[k] = [0.5, 0.0]; self.nac += 1
        self.camino.append(k)
        for v in self.cel.values(): v[0] -= self.c_exist
        self.ops += len(self.cel)
        if come:
            grupo = self.camino[-12:]
            if self.barajar and self.cel: ks = list(self.cel.keys()); grupo = [ks[int(self.rng.integers(len(ks)))] for _ in grupo]
            for q in grupo:
                if q in self.cel: self.cel[q][0] += self.pago / len(grupo); self.cel[q][1] += 1.0 / len(grupo)
            self.camino = []
        muertas = [q for q, v in self.cel.items() if v[0] < 0]
        for q in muertas: del self.cel[q]; self.mue += 1
    def memoria(self): return len(self.cel)


class PlanPanCel(PlanPan):
    """LA PROPUESTA: pan congelado + planificador + bloque de celulas que corrige al pan (modo 'pred' o 'costo')."""
    nombre = '6 plan_pan_cel'
    def __init__(self, mundo, pan, seed, C=32, modo='pred', barajar=False, **kw):
        super().__init__(mundo, pan, seed, C); self.b = Bloque(self.N, C, seed, modo=modo, barajar=barajar, **kw); self.Tc = self.T0.copy()
    def tabla(self):
        if self.b.cambio:
            self.Tc = self.b.tabla_corregida(self.T0); self.ops += self.b.ops; self.b.ops = 0; self.b.cambio = False; self.replan = True
        return self.Tc
    def decide(self, s, meta):
        self.tabla(); return super().decide(s, meta)
    def aprende(self, s, a, s2, come, meta):
        super().aprende(s, a, s2, come, meta)
        self.b.aprende(s, a, int(self.T0[s, a]), s2); self.ops += self.b.ops; self.b.ops = 0
    def memoria(self): return self.b.n
    def modelo(self): return self.b.tabla_corregida(self.T0)


class Sueno(PlanPanCel):
    """(6) + cada `cada` pasos el pan absorbe con gradiente los episodios de las celulas (+ pseudo-ensayo con sus propias
    predicciones) y libera las celulas cuya correccion ya da solo."""
    nombre = '8 sueno'
    def __init__(self, mundo, pan, seed, C=32, cada=250, pasos=30, lr=1e-3, **kw):
        super().__init__(mundo, pan.copia(), seed, C, **kw); self.cada, self.pasos, self.lr = cada, pasos, lr; self.t = 0; self.liberadas = 0
    def aprende(self, s, a, s2, come, meta):
        super().aprende(s, a, s2, come, meta); self.t += 1
        if self.t % self.cada == 0 and self.b.n: self.duerme()
    def duerme(self):
        ep = self.b.ep; X = np.array([self.pan.x(s, a) for s, a, _ in ep]); y = np.array([s2 for _, _, s2 in ep])
        idx = self.rng.integers(0, self.S * A, 2 * len(y)); X2 = self.pan.X_all[idx]; y2 = self.T0.reshape(-1)[idx]   # pseudo-ensayo
        Xt = np.vstack([X, X2]); yt = np.concatenate([y, y2])
        for _ in range(self.pasos): self.pan.paso(Xt, yt, lr=self.lr)
        self.T0 = self.pan.tabla(); self.ops += self.pan.ops; self.pan.ops = 0
        ok = np.array([int(self.T0[s, a]) == s2 for s, a, s2 in ep])
        if ok.any(): self.liberadas += int(ok.sum()); self.b._mata(~ok)
        self.b.cambio = True
    def memoria(self): return self.b.n


def fabrica(C):
    return {
        '0 oraculo': lambda m, p, s: Oraculo(m, p, s, C),
        '1 regla_mano': lambda m, p, s: ReglaMano(m, p, s, C),
        '2 plan_pan': lambda m, p, s: PlanPan(m, p, s, C),
        '3 q_tabular': lambda m, p, s: QTab(m, p, s, C),
        '3b q_optimista': lambda m, p, s: QTab(m, p, s, C, eps=0.05, q0=1.0),
        '3c q_rapido': lambda m, p, s: QTab(m, p, s, C, alpha=0.5, eps=0.2, q0=0.0),
        '4 plan_pan_grad': lambda m, p, s: PlanPanGrad(m, p, s, C),
        '4b plan_pan_grad_bufer': lambda m, p, s: PlanPanGrad(m, p, s, C, lr=1e-3, bufer=256, lote=32),
        '4c plan_pan_grad_bufer_lr3': lambda m, p, s: PlanPanGrad(m, p, s, C, lr=3e-3, bufer=128, lote=32),
        '5 bloque_solo': lambda m, p, s: BloqueSolo(m, p, s),
        '6 plan_pan_cel': lambda m, p, s: PlanPanCel(m, p, s, C, modo='pred'),
        '6c plan_pan_cel_costo': lambda m, p, s: PlanPanCel(m, p, s, C, modo='costo'),
        '7 plan_pan_cel_baraj': lambda m, p, s: PlanPanCel(m, p, s, C, modo='pred', barajar=True),
        '7b plan_pan_cel_nace_azar': lambda m, p, s: PlanPanCel(m, p, s, C, modo='pred', nacer_azar=True),
        '7c plan_pan_cel_baraj_y_azar': lambda m, p, s: PlanPanCel(m, p, s, C, modo='pred', nacer_azar=True, barajar=True),
        '8 sueno': lambda m, p, s: Sueno(m, p, s, C, modo='pred'),
    }


# ----------------------------------------------------------------------------------------------- corrida
def eventos_de(T, cada_sitio, reglas):
    ev = {}
    for t in range(cada_sitio, T, cada_sitio): ev[t] = 'sitio'
    for t in reglas: ev[t] = 'regla'
    return ev


def corre(seed, N=8, T=3000, cada_sitio=300, reglas=(900, 1800, 2700), C=32, regional=False, brazos=None, pan_tipo='onehot'):
    m0 = Mundo(seed, N, regional); pan, acc0 = entrena_pan(m0, seed, tipo=pan_tipo)
    ev = eventos_de(T, cada_sitio, reglas); T_orig = m0.tabla()
    fab = fabrica(C); brazos = brazos or list(fab)
    res = {'acc0': acc0, 'seed': seed, 'brazos': {}}
    for nombre in brazos:
        m = Mundo(seed, N, regional); ag = fab[nombre](m, pan, seed)
        comidas = []; t_ev = []; pos_tr = []
        for t in range(T):
            if t in ev:
                (m.muda_sitio() if ev[t] == 'sitio' else m.cambia_regla()); t_ev.append((t, ev[t]))
            s = m.pos; meta = m.comida; a = ag.decide(s, meta); s2, come = m.paso(a); ag.aprende(s, a, s2, come, meta)
            if come: comidas.append(t)
        comidas = np.array(comidas); tiempos = sorted(ev)
        rec = {'sitio': [], 'regla': []}; rec1 = {'sitio': [], 'regla': []}; tasa = {'sitio': [], 'regla': []}
        for te, tipo in t_ev:
            fin = min([x for x in tiempos if x > te] + [T])
            c = comidas[(comidas >= te) & (comidas < fin)]
            rec1[tipo].append(int(c[0] - te) if len(c) else None)
            rec[tipo].append(int(c[2] - te) if len(c) >= 3 else None)
            tasa[tipo].append(len(c) / (fin - te))
        base = len(comidas[comidas < tiempos[0]]) / tiempos[0]
        mod = ag.modelo(); T_fin = m.tabla(); intacto = (T_fin == T_orig)      # transiciones que NUNCA cambiaron
        res['brazos'][nombre] = dict(
            modelo_intacto=float(np.mean(mod[intacto] == T_orig[intacto])) if mod is not None else None,
            comida_por_paso=len(comidas) / T, base=base,
            rec1_sitio=rec1['sitio'], rec3_sitio=rec['sitio'], rec1_regla=rec1['regla'], rec3_regla=rec['regla'],
            tasa_sitio=float(np.mean(tasa['sitio'])), tasa_regla=float(np.mean(tasa['regla'])),
            ops=ag.ops / T, mem=ag.memoria(),
            modelo_orig=float(np.mean(mod == T_orig)) if mod is not None else None,
            modelo_actual=float(np.mean(mod == T_fin)) if mod is not None else None,
            pan_orig=float(np.mean(ag.pan.tabla() == T_orig)) if mod is not None else None,
            nac=getattr(getattr(ag, 'b', ag), 'nac', 0), mue=getattr(getattr(ag, 'b', ag), 'mue', 0),
            liberadas=getattr(ag, 'liberadas', 0))
    return res


def mr(v, f='{:.3f}'):
    v = [x for x in v if x is not None and not (isinstance(x, float) and np.isnan(x))]
    if not v: return 'nunca'
    med = np.median(v)
    return (f.format(med) + ' [' + f.format(min(v)) + '–' + f.format(max(v)) + ']') if isinstance(v[0], float) else f"{int(med)} [{int(min(v))}–{int(max(v))}]"


def tabla(rs, titulo):
    L = [f"\n## {titulo} (n={len(rs)}; paso 0 del pan: {mr([r['acc0'] for r in rs])})",
         "| brazo | comida/paso | tasa tras sitio | 1a comida tras sitio | 3a tras sitio | tasa tras regla | 1a tras regla | 3a tras regla | ops/decision | memoria | modelo vs mundo actual | modelo en lo que nunca cambió | pan solo vs original |",
         "|---|---|---|---|---|---|---|---|---|---|---|---|---|"]
    for b in rs[0]['brazos']:
        v = [r['brazos'][b] for r in rs]
        def ev(k):   # mediana de medianas por semilla; cuenta de eventos recuperados
            tod = [x for r in v for x in r[k]]; n_ok = sum(x is not None for x in tod)
            return f"{mr(tod)} ({n_ok}/{len(tod)})"
        L.append(f"| {b} | {mr([x['comida_por_paso'] for x in v])} | {mr([x['tasa_sitio'] for x in v])} | {ev('rec1_sitio')} | {ev('rec3_sitio')} | "
                 f"{mr([x['tasa_regla'] for x in v])} | {ev('rec1_regla')} | {ev('rec3_regla')} | {int(np.median([x['ops'] for x in v]))} | "
                 f"{mr([x['mem'] for x in v])} | {mr([x['modelo_actual'] for x in v], '{:.2f}')} | {mr([x['modelo_intacto'] for x in v], '{:.2f}')} | {mr([x['pan_orig'] for x in v], '{:.2f}')} |")
    return '\n'.join(L)


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--semillas', type=int, default=10); ap.add_argument('--N', type=int, default=8); ap.add_argument('--T', type=int, default=3000)
    ap.add_argument('--cada_sitio', type=int, default=300); ap.add_argument('--reglas', default='900,1800,2700'); ap.add_argument('--C', type=int, default=32)
    ap.add_argument('--regional', action='store_true'); ap.add_argument('--out', default='datos/principal.json'); ap.add_argument('--brazos', default='')
    ap.add_argument('--humo', action='store_true'); ap.add_argument('--pan', default='onehot')
    a = ap.parse_args(); t0 = time.time()
    if a.humo:
        m = Mundo(1, a.N); pan, acc = entrena_pan(m, 1, tipo=a.pan); print(f'paso 0: pan {a.pan} predice {acc:.3f} sobre el mundo original ({time.time()-t0:.1f}s)')
        m.cambia_regla(); print(f'tras un cambio de regla el pan acierta {np.mean(pan.tabla() == m.tabla()):.3f}'); sys.exit()
    brazos = a.brazos.split(',') if a.brazos else None
    rs = []
    os.makedirs(os.path.dirname(a.out) or '.', exist_ok=True)
    for s in range(1, a.semillas + 1):
        r = corre(s, a.N, a.T, a.cada_sitio, tuple(int(x) for x in a.reglas.split(',')) if a.reglas else (), a.C, a.regional, brazos, a.pan)
        rs.append(r); json.dump(rs, open(a.out, 'w'))
        print(f"s={s} pan0={r['acc0']:.3f} " + ' '.join(f"{k.split()[0]}:{v['comida_por_paso']:.3f}" for k, v in r['brazos'].items()) + f" [{time.time()-t0:.0f}s]", flush=True)
    titulo = f"N={a.N} T={a.T} sitio cada {a.cada_sitio} reglas {a.reglas} C={a.C} pan={a.pan}{' regional' if a.regional else ''}"
    txt = tabla(rs, titulo); print(txt); open(a.out.replace('.json', '.txt'), 'w', encoding='utf-8').write(txt)
    print(f'CPU {time.time()-t0:.0f}s')
