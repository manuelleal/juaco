"""deriva.py — La celula de JUACO como metodo de aprendizaje EN LINEA con deriva de concepto, contra rivales estandar.
(5-oct-2026, exploracion sin preregistro formal; predicciones en PREDICCIONES.md). MISION: llegar a la AGI por este camino.

GENERADORES (implementados segun su definicion publicada, de memoria [M]):
 - SEA [M] Street & Kim 2001: 3 atributos U[0,10]; y = 1 si x1+x2 <= theta; conceptos theta = 8, 9, 7 (y 9.5).
 - Hiperplano [M] Hulten, Spencer & Domingos 2001: d=10 atributos U[0,1]; y = 1 si sum w_i (x_i - 0.5) > 0; cambia w.
 - STAGGER [M] Schlimmer & Granger 1986: tamano{s,m,l}, color{r,g,b}, forma{c,t,r}; c1: tamano=s & color=r;
   c2: color=g | forma=c; c3: tamano=m | tamano=l. One-hot de 9 dims.
 - RBF con centros que se mueven [M] (generador RandomRBF de MOA, Bifet et al. 2010): k centros gaussianos con clase;
   la deriva mueve los centros.
 (LED y Agrawal no caben en el presupuesto de CPU: se dice en el informe.)
CALENDARIO: T pasos en 4 tramos iguales: concepto A, B, A (RECURRENTE), C. Abrupto (salto) o gradual (Gama 2004: durante
 una transicion de G pasos la probabilidad del concepto nuevo sube linealmente). Ruido de etiquetas 10 %.
EVALUACION prequential (probar y luego entrenar): acierto global, acierto en ventana de 200 tras cada cambio, pasos hasta
 que el acierto en ventana deslizante de 50 vuelve a >= 0.80 (con ruido 10 % el techo es 0.90).
METODOS: base congelado (MLP 16 ocultas entrenado en 600 ejemplos del concepto A); SGD en linea; SGD + DDM (Gama 2004);
 kNN con ventana; Naive Bayes gaussiano con olvido; DWM simplificado (Kolter & Maloof 2007) con expertos MLP; reentrenar en
 ventana cada N pasos (techo); CELULA A (bloque pegado al base congelado); CELULA B (sola: el 'base' es la clase mayoritaria
 con olvido); controles: celula A con pago barajado y celula A sin compuerta. Memoria C in {20, 50, 200} para los que guardan.
"""
import numpy as np, json, time, argparse, os, sys
from collections import deque

RUIDO = 0.1


# ----------------------------------------------------------------------------------------------- generadores
class Gen:
    K = 2
    def __init__(self, seed): self.rng = np.random.default_rng(seed); self.setup()
    def setup(self): pass
    def x(self): raise NotImplementedError
    def y(self, x, concepto): raise NotImplementedError
    def conceptos(self): return [0, 1, 0, 2]


class SEA(Gen):
    D = 3; thetas = (8.0, 9.0, 7.0)
    def x(self): return self.rng.uniform(0, 10, 3)
    def y(self, x, c): return int(x[0] + x[1] <= self.thetas[c])
    def norm(self, x): return x / 10.0


class Hiperplano(Gen):
    D = 10
    def setup(self): self.W = [self.rng.uniform(-1, 1, 10) for _ in range(3)]
    def x(self): return self.rng.uniform(0, 1, 10)
    def y(self, x, c): return int(np.dot(self.W[c], x - 0.5) > 0)
    def norm(self, x): return x


class STAGGER(Gen):
    D = 9
    def x(self):
        v = self.rng.integers(0, 3, 3); x = np.zeros(9); x[v[0]] = 1; x[3 + v[1]] = 1; x[6 + v[2]] = 1; return x
    def y(self, x, c):
        tam, col, forma = int(np.argmax(x[:3])), int(np.argmax(x[3:6])), int(np.argmax(x[6:]))
        if c == 0: return int(tam == 0 and col == 0)         # small & red
        if c == 1: return int(col == 1 or forma == 0)        # green | circle
        return int(tam == 1 or tam == 2)                     # medium | large
    def norm(self, x): return x


class RBF(Gen):
    D = 5; NC = 6; S = 0.12
    def setup(self):
        self.C0 = self.rng.uniform(0.15, 0.85, (self.NC, 5)); self.lab = np.array([0, 1] * (self.NC // 2))
        self.C = [self.C0, self.C0 + self.rng.uniform(-0.35, 0.35, (self.NC, 5)), self.C0 + self.rng.uniform(-0.35, 0.35, (self.NC, 5))]
        self._c = 0
    def x(self):
        self._j = self.rng.integers(self.NC); return np.clip(self.C[self._c][self._j] + self.rng.normal(0, self.S, 5), 0, 1)
    def y(self, x, c):
        # etiqueta = clase del centro mas cercano en el concepto c (los centros se MUEVEN: la frontera cambia)
        d = np.sum((self.C[c] - x) ** 2, axis=1); return int(self.lab[int(np.argmin(d))])
    def norm(self, x): return x


GENS = {'SEA': SEA, 'hiperplano': Hiperplano, 'STAGGER': STAGGER, 'RBF': RBF}


class Flujo:
    """flujo prequential: 4 tramos (A, B, A, C), deriva abrupta o gradual, ruido de etiquetas."""
    def __init__(self, gen, seed, T=4000, gradual=False, G=300):
        self.g = gen; self.rng = np.random.default_rng(seed + 11); self.T = T; self.L = T // 4; self.gradual = gradual; self.G = G
        self.cs = gen.conceptos(); self.cambios = [self.L, 2 * self.L, 3 * self.L]

    def concepto_en(self, t):
        k = min(t // self.L, 3); c = self.cs[k]
        if self.gradual and k > 0 and t - k * self.L < self.G:
            p = (t - k * self.L) / self.G
            if self.rng.random() > p: c = self.cs[k - 1]
        return c

    def paso(self, t):
        c = self.concepto_en(t)
        if isinstance(self.g, RBF): self.g._c = c
        x = self.g.x(); y = self.g.y(x, c)
        if self.rng.random() < RUIDO: y = 1 - y
        return self.g.norm(x), y, c

    def muestra_concepto(self, c, n, seed):
        """ejemplos limpios+ruido de un concepto (para entrenar el base congelado y para validacion)."""
        rng = np.random.default_rng(seed); g2 = type(self.g)(seed)
        g2.__dict__.update({k: v for k, v in self.g.__dict__.items() if k != 'rng'}); g2.rng = rng
        X, Y = [], []
        for _ in range(n):
            if isinstance(g2, RBF): g2._c = c
            x = g2.x(); y = g2.y(x, c)
            if rng.random() < RUIDO: y = 1 - y
            X.append(g2.norm(x)); Y.append(y)
        return np.array(X), np.array(Y)


# ----------------------------------------------------------------------------------------------- MLP chico (numpy)
class MLP:
    def __init__(self, D, K=2, H=16, lr=0.01, seed=0):
        r = np.random.default_rng(seed); self.D, self.K, self.H, self.lr = D, K, H, lr
        self.W1 = r.normal(0, 1 / np.sqrt(D), (D, H)); self.b1 = np.zeros(H); self.W2 = r.normal(0, 1 / np.sqrt(H), (H, K)); self.b2 = np.zeros(K)
        self.m = [np.zeros_like(p) for p in self.params()]; self.v = [np.zeros_like(p) for p in self.params()]; self.t = 0
    def params(self): return [self.W1, self.b1, self.W2, self.b2]
    def copia(self):
        import copy; return copy.deepcopy(self)
    def fwd(self, X):
        h = np.maximum(0, X @ self.W1 + self.b1); z = h @ self.W2 + self.b2; return h, z
    def predice(self, x): return int(np.argmax(self.fwd(x[None])[1][0]))
    def grad(self, X, Y):
        h, z = self.fwd(X); z = z - z.max(1, keepdims=True); p = np.exp(z); p /= p.sum(1, keepdims=True)
        p[np.arange(len(Y)), Y] -= 1; p /= len(Y)
        gW2 = h.T @ p; gb2 = p.sum(0); gh = p @ self.W2.T; gh[h <= 0] = 0; gW1 = X.T @ gh; gb1 = gh.sum(0)
        return [gW1, gb1, gW2, gb2]
    def paso_sgd(self, x, y):
        for p, g in zip(self.params(), self.grad(x[None], np.array([y]))): p -= self.lr * g
    def paso_adam(self, X, Y, lr=0.01):
        self.t += 1; b1, b2 = 0.9, 0.999
        for i, (p, g) in enumerate(zip(self.params(), self.grad(X, Y))):
            self.m[i] = b1 * self.m[i] + (1 - b1) * g; self.v[i] = b2 * self.v[i] + (1 - b2) * g * g
            p -= lr * (self.m[i] / (1 - b1 ** self.t)) / (np.sqrt(self.v[i] / (1 - b2 ** self.t)) + 1e-8)
    def ops_fwd(self): return 2 * (self.D * self.H + self.H * self.K)


def entrena(X, Y, D, seed, pasos=400, H=16):
    m = MLP(D, 2, H, seed=seed)
    for _ in range(pasos): m.paso_adam(X, Y, lr=0.02)
    return m


# ----------------------------------------------------------------------------------------------- metodos
class Metodo:
    nombre = '?'
    def __init__(self): self.ops = 0
    def predice(self, x): raise NotImplementedError
    def aprende(self, x, y, r): pass
    def memoria(self): return 0


class Congelado(Metodo):
    nombre = 'base congelado'
    def __init__(self, base): super().__init__(); self.base = base
    def predice(self, x): self.ops += self.base.ops_fwd(); return self.base.predice(x)


class SGD(Metodo):
    nombre = 'SGD en linea'
    def __init__(self, base, lr): super().__init__(); self.m = base.copia(); self.m.lr = lr
    def predice(self, x): self.ops += self.m.ops_fwd(); return self.m.predice(x)
    def aprende(self, x, y, r): self.m.paso_sgd(x, y); self.ops += 3 * self.m.ops_fwd()


class DDM:
    """Gama et al. 2004 [M]: p = tasa de error, s = sqrt(p(1-p)/n); aviso si p+s >= pmin+2 smin; deriva si >= pmin+3 smin."""
    def __init__(self, nmin=30): self.nmin = nmin; self.reset()
    def reset(self): self.n = 0; self.e = 0; self.pmin = 1e9; self.smin = 1e9
    def actualiza(self, error):
        self.n += 1; self.e += error
        if self.n < self.nmin: return False
        p = self.e / self.n; s = np.sqrt(p * (1 - p) / self.n)
        if p + s < self.pmin + self.smin: self.pmin, self.smin = p, s
        return p + s >= self.pmin + 3 * self.smin


class SGD_DDM(SGD):
    nombre = 'SGD + DDM (reinicio)'
    def __init__(self, base, lr, D, seed):
        super().__init__(base, lr); self.ddm = DDM(); self.D = D; self.seed = seed; self.reinicios = 0
        self.buf = deque(maxlen=30)
    def aprende(self, x, y, r):
        self.buf.append((x, y))
        if self.ddm.actualiza(int(r != y)):
            self.m = MLP(self.D, 2, 16, lr=self.m.lr, seed=self.seed + self.reinicios); self.reinicios += 1; self.ddm.reset()
            for xx, yy in self.buf: self.m.paso_sgd(xx, yy)
        self.m.paso_sgd(x, y); self.ops += 3 * self.m.ops_fwd()


class KNN(Metodo):
    nombre = 'kNN ventana'
    def __init__(self, C, k, D): super().__init__(); self.C = C; self.k = k; self.X = np.zeros((C, D)); self.y = np.zeros(C, int); self.n = 0; self.i = 0
    def predice(self, x):
        if self.n == 0: return 0
        d = np.sum((self.X[:self.n] - x) ** 2, axis=1); self.ops += 3 * self.n * self.X.shape[1]
        k = min(self.k, self.n); j = np.argpartition(d, k - 1)[:k]; m = self.y[j].mean()
        if m == 0.5: return int(self.y[j[np.argmin(d[j])]])        # empate: el mas cercano
        return int(m > 0.5)
    def aprende(self, x, y, r):
        self.X[self.i] = x; self.y[self.i] = y; self.i = (self.i + 1) % self.C; self.n = min(self.n + 1, self.C)
    def memoria(self): return self.n


class NB(Metodo):
    nombre = 'Naive Bayes con olvido'
    def __init__(self, D, lam): super().__init__(); self.lam = lam; self.n = np.full(2, 1e-3); self.s = np.zeros((2, D)) + 0.5e-3; self.s2 = np.zeros((2, D)) + 0.5e-3 * 0.3
    def predice(self, x):
        mu = self.s / self.n[:, None]; var = np.maximum(self.s2 / self.n[:, None] - mu ** 2, 1e-3)
        ll = np.log(self.n / self.n.sum()) - 0.5 * np.sum((x - mu) ** 2 / var + np.log(var), axis=1); self.ops += 6 * self.s.size
        return int(np.argmax(ll))
    def aprende(self, x, y, r):
        self.n *= self.lam; self.s *= self.lam; self.s2 *= self.lam; self.n[y] += 1; self.s[y] += x; self.s2[y] += x * x


class DWM(Metodo):
    """Kolter & Maloof 2007 [M] (DWM-NB), simplificado: expertos Naive Bayes (sin olvido) con peso; peso *= beta al fallar
    (cada p pasos); si el ensamble falla nace un experto nuevo; expertos con peso < theta mueren; maximo M expertos."""
    nombre = 'DWM (ensamble)'
    def __init__(self, D, beta=0.5, theta=0.01, M=10, p=1):
        super().__init__(); self.beta, self.theta, self.M, self.D, self.p = beta, theta, M, D, p
        self.ex = [NB(D, 1.0)]; self.w = [1.0]; self.nac = 1; self.t = 0
    def predice(self, x):
        self._p = [e.predice(x) for e in self.ex]; self.ops += sum(e.ops for e in self.ex)
        for e in self.ex: e.ops = 0
        v = np.zeros(2)
        for p, w in zip(self._p, self.w): v[p] += w
        return int(np.argmax(v))
    def aprende(self, x, y, r):
        self.t += 1
        if self.t % self.p == 0:
            for i, p in enumerate(self._p):
                if p != y: self.w[i] *= self.beta
            mx = max(self.w); self.w = [w / mx for w in self.w]
            viva = [i for i, w in enumerate(self.w) if w >= self.theta]
            self.ex = [self.ex[i] for i in viva]; self.w = [self.w[i] for i in viva]
            if r != y and len(self.ex) < self.M: self.ex.append(NB(self.D, 1.0)); self.w.append(1.0); self.nac += 1
        for e in self.ex: e.aprende(x, y, r)
        self.ops += 2 * len(self.ex) * self.D
    def memoria(self): return len(self.ex)


class Reentrena(Metodo):
    nombre = 'reentrenar ventana (techo)'
    def __init__(self, base, C, D, seed, cada=50, pasos=60):
        super().__init__(); self.m = base; self.C = C; self.D = D; self.seed = seed; self.cada = cada; self.pasos = pasos
        self.X = deque(maxlen=C); self.Y = deque(maxlen=C); self.t = 0
    def predice(self, x): self.ops += self.m.ops_fwd(); return self.m.predice(x)
    def aprende(self, x, y, r):
        self.X.append(x); self.Y.append(y); self.t += 1
        if self.t % self.cada == 0 and len(self.Y) >= 10:
            X, Y = np.array(self.X), np.array(self.Y); self.m = MLP(self.D, 2, 16, seed=self.seed + self.t)
            for _ in range(self.pasos): self.m.paso_adam(X, Y, lr=0.02)
            self.ops += self.pasos * 3 * len(Y) * self.m.ops_fwd()
    def memoria(self): return len(self.Y)


class Prior:
    """'base' de la celula B: clase mayoritaria con olvido (la celula sola no tiene a quien corregir salvo a esto)."""
    def __init__(self): self.c = np.ones(2)
    def predice(self, x): return int(np.argmax(self.c))
    def aprende(self, y): self.c *= 0.99; self.c[y] += 1
    def ops_fwd(self): return 2


class Celula(Metodo):
    """bloque de celulas de JUACO (informe 3 / hamburguesa) pegado a un base: prototipo + valor + energia + confianza.
    compuerta: pisa si se parece (s > theta), su valor difiere del base y ya cobro; cobra si piso y acerto donde el base fallaba
    (pago por camino chico: las que oyeron comparten); paga por existir; E<0 muere; sin cupo muere la mas pobre; si piso donde
    el base acertaba SUELTA la correccion (pierde castigo_pisa de energia y la confianza; con castigo_pisa=inf muere en el acto,
    como en el informe 3); si fallan los dos corrige su valor. Fallo del base sin celula que pise -> nace una celula ahi."""
    nombre = 'celula A (base congelado + bloque)'
    def __init__(self, base, C, D, seed, sigma=0.2, theta=0.6, c_exist=0.002, pago=1.0, castigo=0.5, castigo_pisa=np.inf, eta=0.3,
                 barajar=False, sin_compuerta=False, camino=True, E0=1.0, prior=False, conf0=1.0):
        super().__init__(); self.base = base; self.C = C; self.D = D; self.rng = np.random.default_rng(seed + 777)
        self.W = np.zeros((0, D)); self.V = np.zeros((0, 2)); self.E = np.zeros(0); self.conf = np.zeros(0)
        self.sigma = sigma * np.sqrt(D)          # anchura relativa a la dimension (declarado: sin esto en d=10 nunca pisa)
        self.theta, self.c_exist, self.pago, self.castigo, self.castigo_pisa, self.eta = theta, c_exist, pago, castigo, castigo_pisa, eta
        self.barajar, self.sin_compuerta, self.camino, self.E0, self.prior, self.conf0 = barajar, sin_compuerta, camino, E0, prior, conf0
        self.nac = 0; self.mue = 0; self.pisadas = 0
    @property
    def N(self): return self.W.shape[0]
    def predice(self, x):
        yf = self.base.predice(x); self.ops += self.base.ops_fwd()
        act = np.zeros(0, bool); cand = act; s = None; vals = None
        if self.N:
            s = np.exp(-np.sum((self.W - x) ** 2, axis=1) / (2 * self.sigma ** 2)); self.ops += 4 * self.W.size
            vals = np.argmax(self.V, axis=1)
            if self.sin_compuerta:
                act = np.zeros(self.N, bool); act[int(np.argmax(s))] = True; cand = s > self.theta
            else:
                act = (s > self.theta) & (vals != yf) & (self.conf > 0); cand = s > self.theta
        if act.any():
            j = int(np.argmax(np.where(act, s, -1))); r = int(vals[j]); self.pisadas += 1
        else:
            j = -1; r = yf
        self._ult = (x, yf, cand, j, r, vals); return r
    def aprende(self, x, y, r):
        x, yf, cand, j, r, vals = self._ult; c = y
        if self.prior: self.base.aprende(y)
        if self.N:
            self.E -= self.c_exist
            if self.conf0 < 1 and cand.any():                           # compuerta por EVIDENCIA local (modo conf0=0): las que oyeron sin pisar
                oyo = cand.copy()                                        # suman si pisar habria servido (base fallo, yo acertaba) y restan si
                if j >= 0: oyo[j] = False                                # habria danado (base acerto, yo no); pisan solo con evidencia > 0
                if yf != c: self.conf[oyo & (vals == c)] += 1.0
                else: self.conf[oyo & (vals != c)] -= 1.0
                self.conf = np.maximum(self.conf, -2.0)
            if j >= 0:
                k = j if not self.barajar else int(self.rng.integers(self.N))
                if r == c and yf != c:                                   # mi correccion valio
                    if self.camino and cand.any():
                        grupo = np.where(cand)[0]
                        if self.barajar: grupo = self.rng.choice(self.N, len(grupo), replace=False)
                        self.E[grupo] += self.pago / len(grupo); self.conf[grupo] += 1.0 / len(grupo)
                    else:
                        self.E[k] += self.pago; self.conf[k] += 1
                    self.W[k] += 0.2 * (x - self.W[k])
                elif r != c and yf == c:                                 # pise donde el base acertaba: suelto la correccion
                    if np.isinf(self.castigo_pisa): self.conf[k] = 0.0; self.E[k] = -1.0
                    else: self.E[k] -= self.castigo_pisa; self.conf[k] = max(0.0, self.conf[k] - 1.0)
                elif r != c:                                             # fallamos los dos: corrijo mi valor
                    self.E[k] -= self.castigo * 0.5
                    self.V[k] += self.eta * (np.eye(2)[c] - self.V[k]); self.W[k] += self.eta * (x - self.W[k])
            muertas = self.E < 0
            if muertas.any():
                self.mue += int(muertas.sum()); viva = ~muertas
                self.W, self.V, self.E, self.conf = self.W[viva], self.V[viva], self.E[viva], self.conf[viva]
        if r != c and j < 0 and yf != c:                                 # nadie piso y el base fallo: nace una celula
            if self.N >= self.C:
                peor = int(np.argmin(self.E)); viva = np.ones(self.N, bool); viva[peor] = False; self.mue += 1
                self.W, self.V, self.E, self.conf = self.W[viva], self.V[viva], self.E[viva], self.conf[viva]
            self.W = np.vstack([self.W, x]); self.V = np.vstack([self.V, np.eye(2)[c]])
            self.E = np.append(self.E, self.E0); self.conf = np.append(self.conf, self.conf0); self.nac += 1
    def memoria(self): return self.N


# ----------------------------------------------------------------------------------------------- corrida prequential
def medidas(ok, flujo, VENT=200, W=50, umbral=0.8):
    ok = np.asarray(ok, float); T = len(ok); L = flujo.L
    r = dict(preq=float(ok.mean()), tramos=[float(ok[k * L:(k + 1) * L].mean()) for k in range(4)], post=[], rec=[])
    cs = np.cumsum(np.concatenate([[0], ok])); desl = (cs[W:] - cs[:-W]) / W       # desl[t] = acierto en [t, t+W)
    for t0 in flujo.cambios:
        r['post'].append(float(ok[t0:t0 + VENT].mean()))
        fin = min(t0 + L, T) - W; rec = None
        for t in range(t0, fin):
            if desl[t] >= umbral: rec = t - t0; break
        r['rec'].append(rec)
    return r


def arma_metodos(gen, flujo, base, seed, C, P, solo_C=False, solo=None):
    D = gen.D; ms = {}; cel = dict(sigma=P['sigma'], castigo_pisa=P['cp'], conf0=P['conf0'])
    if not solo_C:
        ms['base congelado'] = Congelado(base)
        ms['SGD en linea'] = SGD(base, P['lr'])
        ms['SGD + DDM'] = SGD_DDM(base, P['lr'], D, seed)
        ms['Naive Bayes olvido'] = NB(D, P['lam'])
        ms['DWM'] = DWM(D)
    ms['kNN ventana'] = KNN(C, P['k'], D)
    ms['reentrenar ventana'] = Reentrena(base, C, D, seed)
    ms['celula A'] = Celula(base, C, D, seed, **cel)
    ms['celula B (sola)'] = Celula(Prior(), C, D, seed, prior=True, **cel)
    ms['celula A barajada'] = Celula(base, C, D, seed, barajar=True, **cel)
    ms['celula A sin compuerta'] = Celula(base, C, D, seed, sin_compuerta=True, **cel)
    if solo: ms = {solo: ms[solo]}
    return ms


def corre(nombre_gen, seed, C, P, T=4000, gradual=False, solo_C=False, solo=None):
    gen = GENS[nombre_gen](seed); flujo = Flujo(gen, seed, T, gradual)
    X0, Y0 = flujo.muestra_concepto(flujo.cs[0], 600, seed + 500); base = entrena(X0, Y0, gen.D, seed)
    acc0 = float(np.mean([base.predice(x) == y for x, y in zip(*flujo.muestra_concepto(flujo.cs[0], 300, seed + 501))]))
    ms = arma_metodos(gen, flujo, base, seed, C, P, solo_C, solo); oks = {m: [] for m in ms}
    for t in range(T):
        x, y, c = flujo.paso(t)
        for m, met in ms.items():
            r = met.predice(x); oks[m].append(r == y); met.aprende(x, y, r)
    res = {}
    for m, met in ms.items():
        res[m] = medidas(oks[m], flujo); res[m]['mem'] = met.memoria(); res[m]['ops'] = met.ops / T
        if isinstance(met, Celula): res[m]['nac'] = met.nac; res[m]['mue'] = met.mue; res[m]['pisadas'] = met.pisadas
    res['_acc0'] = acc0
    return res


# ----------------------------------------------------------------------------------------------- validacion (flujo aparte)
def valida(T=3000, seeds=(101, 102, 103)):
    """ajusta cada perilla en un flujo de validacion APARTE (semillas 101-103, abrupto y gradual, C=50), por acierto prequential
    medio en los 4 generadores, una perilla a la vez (coordenada a coordenada), solo el metodo que la usa."""
    P = dict(lr=0.03, k=3, lam=0.995, sigma=0.2, cp=np.inf, conf0=1.0)
    grid = dict(lr=[0.01, 0.03, 0.1], k=[1, 3, 5], lam=[0.98, 0.995, 0.999], sigma=[0.05, 0.1, 0.2, 0.4], cp=[np.inf, 1.0, 0.5], conf0=[1.0, 0.0])
    met_de = {'lr': 'SGD + DDM', 'k': 'kNN ventana', 'lam': 'Naive Bayes olvido', 'sigma': 'celula A', 'cp': 'celula A', 'conf0': 'celula A'}
    log = []
    for key, vals in grid.items():
        mejor, mv = None, -1
        for v in vals:
            Q = dict(P); Q[key] = v; accs = []
            for g in GENS:
                for s in seeds:
                    for gr in (False, True):
                        accs.append(corre(g, s, 50, Q, T=T, gradual=gr, solo=met_de[key])[met_de[key]]['preq'])
            a = float(np.mean(accs)); log.append((key, float(v), a)); print(f"  {key}={v}: {a:.3f}", flush=True)
            if a > mv: mv, mejor = a, v
        P[key] = mejor
    return P, log


if __name__ == '__main__':
    ap = argparse.ArgumentParser(); ap.add_argument('--semillas', type=int, default=10); ap.add_argument('--T', type=int, default=4000)
    ap.add_argument('--valida', action='store_true'); ap.add_argument('--humo', action='store_true'); ap.add_argument('--out', default='datos/deriva.json')
    ap.add_argument('--gens', default='SEA,hiperplano,STAGGER,RBF'); ap.add_argument('--Cs', default='20,50,200')
    args = ap.parse_args(); t0 = time.time(); os.makedirs('datos', exist_ok=True)
    if args.humo:
        P = dict(lr=0.03, k=3, lam=0.995, sigma=0.2, cp=np.inf, conf0=0.0)
        for g in args.gens.split(','):
            r = corre(g, 1, 50, P, T=args.T); print(f"\n{g}  base paso 0: {r['_acc0']:.2f}")
            for m, v in r.items():
                if m.startswith('_'): continue
                print(f"  {m:28s} preq {v['preq']:.3f} tramos {['%.2f' % a for a in v['tramos']]} post {['%.2f' % a for a in v['post']]} rec {v['rec']} mem {v['mem']} ops {v['ops']:.0f}")
        print(f"({time.time()-t0:.0f} s)"); sys.exit()
    if args.valida:
        P, log = valida(); P2 = {k: (None if np.isinf(v) else v) for k, v in P.items()}
        json.dump(dict(P=P2, log=log), open('datos/validacion.json', 'w'), indent=1); print(P, f"({time.time()-t0:.0f} s)"); sys.exit()
    P = json.load(open('datos/validacion.json'))['P']; P['cp'] = np.inf if P['cp'] is None else P['cp']; print('perillas', P)
    todo = {}
    for g in args.gens.split(','):
        for gradual in (False, True):
            for C in [int(c) for c in args.Cs.split(',')]:
                clave = f"{g}|{'gradual' if gradual else 'abrupto'}|C{C}"; todo[clave] = []
                for s in range(1, args.semillas + 1):
                    todo[clave].append(corre(g, s, C, P, T=args.T, gradual=gradual, solo_C=(C != 50)))
                print(f"{clave} listo ({time.time()-t0:.0f} s)", flush=True)
                json.dump(todo, open(args.out, 'w'))
    print(f"({time.time()-t0:.0f} s)")
