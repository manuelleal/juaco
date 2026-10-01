"""red_celulas.py — RED DE CELULAS VIVAS, version minima (1-oct-2026, exploracion, sin preregistro).

MISION: llegar a la AGI por este camino (organismo minimo, reglas locales, sin retropropagacion dentro del sistema).

QUE ES:
  - Hay LETRAS de entrada (one-hot de a y de b; o, si se pide, el prior de angulos: conocimiento puesto a mano, DECLARADO).
  - Hay N celulas ocultas. Cada celula es dueña de: sus pesos de entrada w_in (que letras oye), su sesgo, sus pesos de
    salida w_out (su "axon": cuanto le manda a cada celula de boca) y una ENERGIA E.
  - Hay 7 celulas de BOCA (una por simbolo c). Cada boca suma lo que le llega de las ocultas (y, si se permite, de las letras
    directamente) y predice. Cuando llega el siguiente simbolo del flujo, la boca calcula SU PROPIO error de prediccion.
  - La boca manda a sus alimentadoras dos cosas LOCALES: (1) su error (aviso) y (2) un PAGO en energia, proporcional a cuanto
    peor le habria ido sin esa celula (aporte contrafactual: se calcula en la sinapsis, con lo que la boca ya tiene).
  - La celula oculta ajusta su w_out con regla delta local (pre = lo que emitio, post = el aviso de la boca que alimenta).
  - La celula oculta ajusta su w_in por TANTEO: emite con un ruido propio xi; si el aviso escalar que recibio correlaciona con
    su ruido, mueve w_in en esa direccion (regla de tres factores: letra que llego x ruido propio x aviso). NUNCA recibe un
    vector: solo un numero. (En la literatura: perturbacion de nodo / REINFORCE por unidad. No es retropropagacion.)
  - VIDA: E sube con los pagos, baja por existir y por emitir. E alta -> se divide (hija = copia con UNA mutacion chica).
    E < 0 -> muere. La red cambia de tamano sola.

PROHIBIDO dentro de la red (y no esta en el codigo): gradiente global, retropropagacion a traves de capas, optimizador externo.
El TECHO (clase MLP, abajo) SI usa retropropagacion: esta aparte, es el banco de comparacion ("Alejo"), nunca parte de la red.
"""
import numpy as np

P = 7  # modulo


# ----------------------------------------------------------------------------------------------------- codificacion
def codifica(a, b, prior):
    """Letras de entrada. 'onehot': 14 letras (7 de a, 7 de b). 'angulos': 8 rasgos cos/sin y sus productos
    (PRIOR PUESTO A MANO: hace lineal la suma mod 7; se declara)."""
    if prior == 'onehot':
        x = np.zeros(2 * P); x[a] = 1.0; x[P + b] = 1.0; return x
    ta, tb = 2 * np.pi * a / P, 2 * np.pi * b / P
    ca, sa, cb, sb = np.cos(ta), np.sin(ta), np.cos(tb), np.sin(tb)
    return np.array([ca, sa, cb, sb, ca * cb, ca * sb, sa * cb, sa * sb])


def dim_entrada(prior):
    return 2 * P if prior == 'onehot' else 8


def tarea(nombre, a, b):
    if nombre == 'suma': return (a + b) % P
    if nombre == 'resta': return (a - b) % P
    raise ValueError(nombre)


def particion(rng):
    """49 pares; 30 vistos, 19 retenidos (nunca vistos en entrenamiento)."""
    pares = [(a, b) for a in range(P) for b in range(P)]
    idx = rng.permutation(len(pares))
    vistos = [pares[i] for i in idx[:30]]; ret = [pares[i] for i in idx[30:]]
    return vistos, ret


# ----------------------------------------------------------------------------------------------------- la red
class RedCelulas:
    def __init__(self, seed, n0=40, prior='onehot', plasticidad=True, vida=True, credito='individual',
                 barajar=False, directo=True, eta_out=0.05, eta_in=0.02, sigma=0.3,
                 c_exist=0.01, c_emit=0.002, F=0.09, E_div=2.0, n_max=None, sigma_mut=0.3, n_salidas=P, regla_in='tanteo'):
        self.rng = np.random.default_rng(seed)
        self.regla_in = regla_in
        self.D = dim_entrada(prior); self.K = n_salidas
        self.prior = prior; self.plast = plasticidad; self.vida = vida; self.credito = credito; self.barajar = barajar
        self.eta_out, self.eta_in, self.sigma = eta_out, eta_in, sigma
        self.c_exist, self.c_emit, self.F, self.E_div, self.sigma_mut = c_exist, c_emit, F, E_div, sigma_mut
        self.n_max = n_max or 4 * n0; self.n_min = 2
        r = self.rng
        # cada celula: w_in (D), b_in, w_out (K), E. Conectividad parcial: cada celula oye ~70 % de las letras (no ve todo).
        self.Win = r.normal(0, 1.0, (n0, self.D)) * (r.random((n0, self.D)) < 0.7)
        self.bin = r.normal(0, 0.5, n0)
        # ESCALA: la boca reparte su paso entre sus alimentadoras (sabe cuantas son: local a la boca); el axon nace mas
        # debil cuantas mas celulas hay; y la comida del mundo (F) crece con el tamano inicial. Referencia: 40 celulas.
        self.esc = min(1.0, 40.0 / n0)      # solo reparte (n0 > 40); con menos de 40 no amplifica (a 20 amplificar rompia)
        self.F = F * n0 / 40.0
        self.Wout = r.normal(0, 0.3 * np.sqrt(self.esc), (n0, self.K))
        self.E = np.ones(n0)
        self.hbar = np.zeros(n0)          # media movil de la emision propia (para medir "celula constante")
        self.hvar = np.ones(n0) * 0.1     # varianza movil de la emision propia
        # celulas de boca: sesgo propio y, si directo, lectura directa de las letras (regla delta local)
        self.bout = np.zeros(self.K)
        self.directo = directo
        self.Wdir = np.zeros((self.D, self.K))
        self.Lbar = 1.0                   # error medio movil del grupo (para el credito de grupo)
        self.nacimientos = 0; self.muertes = 0
        self.ops = 0                      # conteo aproximado de sumas/multiplicaciones

    @property
    def N(self): return self.Win.shape[0]

    def adelante(self, x, ruido):
        pre = self.Win @ x + self.bin
        h0 = np.tanh(pre)
        xi = self.rng.normal(0, self.sigma, self.N) if ruido else np.zeros(self.N)
        h = h0 + xi
        y = h @ self.Wout + self.bout
        if self.directo: y = y + x @ self.Wdir
        self.ops += 2 * self.N * self.D + 2 * self.N * self.K + (2 * self.D * self.K if self.directo else 0)
        return h, xi, y

    def predice(self, x):
        _, _, y = self.adelante(x, ruido=False)
        return int(np.argmax(y))

    def expone(self, x, c):
        """Una exposicion: ve (x) y luego llega c en el flujo. Todo lo que sigue es local a cada celula/sinapsis."""
        h, xi, y = self.adelante(x, ruido=self.plast)
        t = np.zeros(self.K); t[c] = 1.0
        err = t - y                                     # error de prediccion PROPIO de cada boca
        L = float(err @ err)
        # --- aporte contrafactual de la sinapsis (i -> boca j): cuanto peor le iria a j sin i. Local a la sinapsis.
        contrib = (err[None, :] + self.Wout * h[:, None]) ** 2 - err[None, :] ** 2    # (N, K)
        self.ops += 4 * self.N * self.K
        # --- aviso escalar que recibe cada celula oculta
        if self.credito == 'individual':
            aviso = self.Wout @ err                     # cada boca manda su error; la celula lo pesa con SU axon. Escalar.
            pago = np.maximum(contrib, 0.0)             # pago de cada boca a cada alimentadora por su aporte
            presup = self.F * (0.3 + 0.7 * np.maximum(0.0, 1.0 - err ** 2))   # cada boca paga mas si predijo bien
            tot = pago.sum(axis=0) + 1e-9
            pago_i = (pago / tot[None, :] * presup[None, :]).sum(axis=1)
        else:                                           # 'grupo': mismo numero para todas (hizo mejor el grupo que antes?)
            R = self.Lbar - L
            aviso = np.full(self.N, R)
            presup = self.F * (0.3 + 0.7 * np.maximum(0.0, 1.0 - err ** 2))
            pago_i = np.full(self.N, presup.sum() / self.N)   # reparto igual: todas las del camino cobran lo mismo
        self.Lbar = 0.95 * self.Lbar + 0.05 * L
        if self.barajar:                                # CONTROL: el aviso y el pago llegan a la celula equivocada
            perm = self.rng.permutation(self.N); aviso = aviso[perm]; pago_i = pago_i[perm]
        # --- plasticidad (reglas locales; ninguna usa el gradiente de otra capa)
        if self.plast:
            # regla delta en el axon: pre = h_i (lo que emiti), post = err_j (aviso de la boca que alimento)
            self.Wout += self.eta_out * self.esc * np.outer(h, err)
            self.bout += self.eta_out * err
            if self.directo: self.Wdir += self.eta_out * np.outer(x, err)
            # regla de tres factores en la entrada (NO gradiente: la celula solo recibe UN numero, el aviso):
            #   'tanteo': letra x ruido propio xi x aviso   (perturbacion de nodo)
            #   'hebb3' : letra x (emision - su media) x aviso   (Hebb con tercer factor, sin ruido)
            tercer = xi if self.regla_in == 'tanteo' else (h - self.hbar)
            self.Win += self.eta_in * (aviso * tercer)[:, None] * x[None, :] * (self.Win != 0)
            self.bin += self.eta_in * aviso * tercer
            self.ops += 2 * self.N * self.K + 2 * self.N * self.D + 2 * self.D * self.K
        # --- medicion de emision (para detectar celulas constantes = posibles tramposas)
        self.hbar = 0.98 * self.hbar + 0.02 * h
        self.hvar = 0.98 * self.hvar + 0.02 * (h - self.hbar) ** 2
        # --- vida
        if self.vida:
            self.E += pago_i - self.c_exist - self.c_emit * np.abs(h)
            self._nacer_morir()
        return L, int(np.argmax(y)) == c

    def _nacer_morir(self):
        # morir: E < 0 (se poda), nunca por debajo de n_min
        vivas = self.E >= 0
        if vivas.sum() < self.n_min:
            vivas[np.argsort(self.E)[-self.n_min:]] = True
        nm = int((~vivas).sum())
        if nm:
            self.muertes += nm
            for nombre in ('Win', 'bin', 'Wout', 'E', 'hbar', 'hvar'):
                setattr(self, nombre, getattr(self, nombre)[vivas])
        # dividir: E > E_div y hay sitio. La hija lleva los pesos de la madre con UNA mutacion (un numero, paso chico).
        div = np.where(self.E > self.E_div)[0]
        for i in div:
            if self.N >= self.n_max: break
            self.E[i] /= 2.0
            win, b, wout = self.Win[i].copy(), self.bin[i], self.Wout[i].copy()
            k = self.rng.integers(self.D + 1 + self.K)
            d = self.rng.normal(0, self.sigma_mut)
            if k < self.D: win[k] += d
            elif k == self.D: b += d
            else: wout[k - self.D - 1] += d
            self.Win = np.vstack([self.Win, win]); self.bin = np.append(self.bin, b)
            self.Wout = np.vstack([self.Wout, wout]); self.E = np.append(self.E, self.E[i])
            self.hbar = np.append(self.hbar, self.hbar[i]); self.hvar = np.append(self.hvar, self.hvar[i])
            self.nacimientos += 1

    def tramposas(self):
        """celulas con energia alta (> mediana) y emision casi constante (var < 0.01): cobran sin informar."""
        if self.N == 0: return 0
        return int(((self.E > np.median(self.E)) & (self.hvar < 0.01)).sum())


# ----------------------------------------------------------------------------------------------------- TECHO (fuera de la red)
class MLP:
    """TECHO 'Alejo': red de 2 capas con RETROPROPAGACION (gradiente). Esta fuera de la red de celulas; es el banco."""
    def __init__(self, seed, H=40, prior='onehot', lr=0.05, n_salidas=P):
        self.rng = np.random.default_rng(seed); self.D = dim_entrada(prior); self.K = n_salidas
        self.W1 = self.rng.normal(0, 1.0 / np.sqrt(self.D), (self.D, H)); self.b1 = np.zeros(H)
        self.W2 = self.rng.normal(0, 1.0 / np.sqrt(H), (H, self.K)); self.b2 = np.zeros(self.K)
        self.lr = lr; self.ops = 0; self.H = H
        self.esc = min(1.0, 40.0 / H)     # misma regla de escala que la red: el paso de la capa de salida se reparte entre H

    @property
    def N(self): return self.H

    def predice(self, x):
        h = np.tanh(x @ self.W1 + self.b1); return int(np.argmax(h @ self.W2 + self.b2))

    def expone(self, x, c):
        h = np.tanh(x @ self.W1 + self.b1); y = h @ self.W2 + self.b2
        t = np.zeros(self.K); t[c] = 1.0; err = y - t
        # retropropagacion (SOLO aqui, en el techo)
        dW2 = np.outer(h, err); db2 = err
        dh = self.W2 @ err * (1 - h ** 2)
        dW1 = np.outer(x, dh); db1 = dh
        self.W2 -= self.lr * self.esc * dW2; self.b2 -= self.lr * db2; self.W1 -= self.lr * dW1; self.b1 -= self.lr * db1
        self.ops += 3 * (2 * self.D * self.H + 2 * self.H * self.K)
        return float(err @ err), int(np.argmax(y)) == c

    def tramposas(self): return 0
