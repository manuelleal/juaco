"""red2.py — red de celulas de VARIAS CAPAS (celulas que alimentan celulas), encargo 2 (1-oct-2026, exploracion).

MISION: llegar a la AGI por este camino (organismo minimo, reglas locales, sin retropropagacion dentro del sistema).

Lo mismo que red_celulas.py (celula duena de w_in, sesgo, w_out = su axon, energia; boca con su propio error de prediccion;
pago contrafactual de la boca a sus alimentadoras; Hebb de tres factores en la entrada) pero con capas: letras -> capa 1 ->
capa 2 -> ... -> boca. Tres formas de pasar el aviso hacia atras, todas SIN calculo global:
  'cadena' : la celula recibe de cada celula que alimento SU senal de aprendizaje (aviso x desviacion propia), pesada por su
             propio axon. Es el aviso del informe 1, encadenado. (Matiz: en expectativa es la direccion de la retropropagacion
             con la derivada cambiada por la desviacion propia. Se dice.)
  'rpe'    : NINGUN error baja desde arriba. La celula solo recibe PAGO (energia) de las celulas que alimento; predice el pago
             que va a recibir y aprende de su propio error de prediccion del pago: letra x desviacion propia x (pago - esperado).
  'fa'     : como 'cadena' pero la celula pesa lo que oye con una "oreja" fija al azar (no con su axon): alineamiento por
             retroalimentacion (Lillicrap 2016). Sin transporte de pesos.
El pago baja por el camino: cada celula reparte parte de lo que cobra entre las que la alimentaron (en proporcion a cuanto le
mandaron). Opciones contra el tramposo: impuesto a la emision constante (c_const) y pago por CAMINO (grupos chicos que
comparten lo cobrado). Consolidacion: la plasticidad de una celula baja con la energia que acumulo en su vida (kappa).
PROHIBIDO y ausente en la red: gradiente global, retropropagacion entre capas, optimizador externo. El TECHO (MLP2, Adam +
entropia cruzada) esta aparte y SI usa gradiente: es el banco.
"""
import numpy as np

P = 7


# ------------------------------------------------------------------------------------------- codigos de entrada (declarados)
def cod_num(a, codigo):
    """un numero 0..6 como patron. 'onehot' 7 letras; 'binario' 3 bits; 'termometro' 6 bits (a unos);
    'angulos4' (cos, sin de 2*pi*a/7) = PRIOR de que los numeros viven en un circulo, sin productos (la red tiene que
    multiplicar sola)."""
    if codigo == 'onehot': v = np.zeros(P); v[a] = 1; return v
    if codigo == 'binario': return np.array([(a >> k) & 1 for k in range(3)], float)
    if codigo == 'termometro': return np.array([1.0 if k < a else 0.0 for k in range(6)])
    if codigo == 'angulos4': t = 2 * np.pi * a / P; return np.array([np.cos(t), np.sin(t)])
    raise ValueError(codigo)


def codifica(a, b, codigo): return np.concatenate([cod_num(a, codigo), cod_num(b, codigo)])
def dim_cod(codigo): return 2 * len(cod_num(0, codigo))


def arma_tarea(nombre, codigo, rng):
    """devuelve (vistos, retenidos, cod, fn(regla,a,b), K)."""
    if nombre == 'paridad3':
        pats = [(i, j, k) for i in (0, 1) for j in (0, 1) for k in (0, 1)]
        cod = lambda *bits: np.array([v for b in bits for v in (1 - b, b)], float)
        fn = lambda regla, *bits: (sum(bits) % 2) if regla == 'A' else 1 - (sum(bits) % 2)
        return pats, [], cod, fn, 2
    if nombre == 'paridad4':
        pats = [(i, j, k, l) for i in (0, 1) for j in (0, 1) for k in (0, 1) for l in (0, 1)]
        cod = lambda *bits: np.array([v for b in bits for v in (1 - b, b)], float)
        fn = lambda regla, *bits: (sum(bits) % 2) if regla == 'A' else 1 - (sum(bits) % 2)
        return pats, [], cod, fn, 2
    pares = [(a, b) for a in range(P) for b in range(P)]
    idx = rng.permutation(49); vistos = [pares[i] for i in idx[:30]]; ret = [pares[i] for i in idx[30:]]
    cod = lambda a, b: codifica(a, b, codigo)
    fn = lambda regla, a, b: (a + b) % P if regla == 'A' else (a - b) % P
    return vistos, ret, cod, fn, P


# ------------------------------------------------------------------------------------------- la red de capas
class Red2:
    def __init__(self, seed, D, K, capas=(40,), credito='cadena', plasticidad=True, vida=False, directo=False,
                 eta_in=0.1, eta_out=0.05, c_exist=0.002, c_emit=0.002, F=0.018, E_div=5.0, sigma_mut=0.3,
                 c_const=0.0, camino=0, kappa=0.0, baja=0.5, conect=0.7, tope=1.0, wmax=5.0, eta_med=None):
        self.rng = np.random.default_rng(seed); r = self.rng
        self.tope, self.wmax, self.eta_med = tope, wmax, eta_med   # eta_med: paso del axon INTERMEDIO (celula -> celula)
        self.D, self.K, self.credito, self.plast, self.vida, self.directo = D, K, credito, plasticidad, vida, directo
        self.eta_in, self.eta_out = eta_in, eta_out
        self.c_exist, self.c_emit, self.F, self.E_div, self.sigma_mut = c_exist, c_emit, F, E_div, sigma_mut
        self.c_const, self.camino, self.kappa, self.baja = c_const, camino, kappa, baja
        self.capas = []   # cada capa: dict(Win, bin, Wout, B (oreja fija), E, Eacum, hbar, hvar, phat, grupo)
        dprev = D
        tam = list(capas) + [K]
        for l, n in enumerate(capas):
            nsig = tam[l + 1]
            esc = min(1.0, 40.0 / n)
            self.capas.append(dict(
                Win=r.normal(0, 1.0, (n, dprev)) * (r.random((n, dprev)) < conect), bin=r.normal(0, 0.5, n),
                Wout=r.normal(0, 0.3 * np.sqrt(esc), (n, nsig)), B=r.normal(0, 0.3, (n, nsig)),
                E=np.ones(n), Eacum=np.zeros(n), hbar=np.zeros(n), hvar=np.full(n, 0.1), phat=np.zeros(n),
                grupo=r.integers(0, max(1, n // camino), n) if camino else np.zeros(n, int), esc=esc, n0=n))
            dprev = n
        self.n_max = [4 * n for n in capas]
        self.bout = np.zeros(K); self.Wdir = np.zeros((D, K))
        self.ops = 0; self.nacimientos = 0; self.muertes = 0
        self.F_tot = F * (capas[0] if capas else 40) / 40.0

    @property
    def N(self): return int(sum(c['Win'].shape[0] for c in self.capas))

    def adelante(self, x):
        hs = [x]
        for c in self.capas:
            h = np.tanh(c['Win'] @ hs[-1] + c['bin']); hs.append(h)
            self.ops += 2 * c['Win'].size
        y = (hs[-1] @ self.capas[-1]['Wout'] if self.capas else 0) + self.bout
        if self.directo: y = y + x @ self.Wdir; self.ops += 2 * self.Wdir.size
        return hs, y

    def predice(self, x):
        _, y = self.adelante(x); return int(np.argmax(y))

    def expone(self, x, c):
        hs, y = self.adelante(x)
        t = np.zeros(self.K); t[c] = 1.0; err = t - y
        if self.plast:
            self.bout += self.eta_out * err
            if self.directo: self.Wdir += self.eta_out * np.outer(x, err)
        # --- de arriba hacia abajo, pero cada paso solo usa lo que la celula tiene o le mandan las que alimento
        senal_arriba = err            # lo que mandan las celulas de arriba (la boca: su error)
        pago_arriba = None            # pagos que bajan por el camino
        for l in range(len(self.capas) - 1, -1, -1):
            cp = self.capas[l]; h = hs[l + 1]; pre = hs[l]; n = h.shape[0]
            W = cp['Wout']
            if l == len(self.capas) - 1:
                # boca: pago contrafactual (cuanto peor le iria sin i) y aviso = su error pesado por mi axon
                contrib = (err[None, :] + W * h[:, None]) ** 2 - err[None, :] ** 2
                pagoM = np.maximum(contrib, 0.0)
                presup = self.F_tot * (0.3 + 0.7 * np.maximum(0.0, 1.0 - err ** 2))   # por boca, como en red_celulas.py (informe 1)
                pago = (pagoM / (pagoM.sum(axis=0) + 1e-9)[None, :] * presup[None, :]).sum(axis=1)
                aviso = W @ err if self.credito != 'fa' else cp['B'] @ err
                self.ops += 6 * W.size
            else:
                # celula de capa intermedia: lo que le mandan las celulas que alimento
                flujo = np.abs(W * h[:, None])                     # cuanto le mande a cada una
                parte = flujo / (flujo.sum(axis=0) + 1e-9)[None, :]
                pago = (parte * (self.baja * pago_arriba)[None, :]).sum(axis=1)   # cada celula de arriba baja 'baja' de lo cobrado
                if self.credito == 'cadena': aviso = W @ senal_arriba
                elif self.credito == 'fa': aviso = cp['B'] @ senal_arriba
                else: aviso = np.zeros(n)
                self.ops += 6 * W.size
            if self.camino:                                        # pago por CAMINO: el grupo comparte lo cobrado
                g = cp['grupo']; tot = np.bincount(g, pago, minlength=g.max() + 1); cnt = np.bincount(g, minlength=g.max() + 1)
                pago = tot[g] / np.maximum(cnt[g], 1)
            desv = h - cp['hbar']
            if self.credito == 'rpe':
                tercer = pago - cp['phat']                          # error de prediccion del PAGO (propio)
                cp['phat'] = 0.9 * cp['phat'] + 0.1 * pago
                cp['pesc'] = 0.9 * cp.get('pesc', np.abs(tercer) + 1e-6) + 0.1 * np.abs(tercer)   # escala propia del error
                senal = np.clip(tercer / (cp['pesc'] + 1e-9), -self.tope, self.tope) * desv
            else:
                # TOPE al aviso (como el techo por canal de JUACO): sin el, con 2 capas el axon intermedio y el aviso se
                # realimentan y los pesos se desbordan (medido: 1e30 a las 500 exposiciones)
                senal = np.clip(aviso, -self.tope, self.tope) * desv
            if self.plast:
                fac = 1.0 / (1.0 + cp['Eacum'] / self.kappa) if self.kappa else 1.0   # consolidacion por energia vivida
                # axon: pre = lo que emiti, post = la senal que me manda la celula alimentada (boca: su error)
                post = err if l == len(self.capas) - 1 else senal_arriba
                eo = self.eta_out if l == len(self.capas) - 1 else (self.eta_med if self.eta_med is not None else self.eta_out)
                cp['Wout'] += eo * cp['esc'] * (fac[:, None] if self.kappa else 1.0) * np.outer(h, post)
                # entrada: Hebb de tres factores (letra x desviacion propia x UN numero). NO gradiente entre capas.
                cp['Win'] += self.eta_in * (fac * senal)[:, None] * pre[None, :] * (cp['Win'] != 0)
                cp['bin'] += self.eta_in * fac * senal
                np.clip(cp['Wout'], -self.wmax, self.wmax, out=cp['Wout']); np.clip(cp['Win'], -self.wmax, self.wmax, out=cp['Win'])
                self.ops += 2 * W.size + 2 * cp['Win'].size
            cp['hbar'] = 0.98 * cp['hbar'] + 0.02 * h
            cp['hvar'] = 0.98 * cp['hvar'] + 0.02 * desv ** 2
            if self.vida:
                costo = self.c_exist + self.c_emit * np.abs(h) + self.c_const * np.maximum(0.0, 1.0 - cp['hvar'] / 0.02)
                cp['E'] += pago - costo; cp['Eacum'] += pago
            else:
                cp['Eacum'] += pago
            senal_arriba = senal; pago_arriba = pago
        if self.vida: self._nacer_morir()
        return float(err @ err), int(np.argmax(y)) == c

    def _nacer_morir(self):
        for l, cp in enumerate(self.capas):
            sig = self.capas[l + 1] if l + 1 < len(self.capas) else None
            vivas = cp['E'] >= 0
            if vivas.sum() < 2: vivas[np.argsort(cp['E'])[-2:]] = True
            if (~vivas).any():
                self.muertes += int((~vivas).sum())
                for k in ('Win', 'bin', 'Wout', 'B', 'E', 'Eacum', 'hbar', 'hvar', 'phat', 'grupo'): cp[k] = cp[k][vivas]
                if sig is not None: sig['Win'] = sig['Win'][:, vivas]
            for i in np.where(cp['E'] > self.E_div)[0]:
                if cp['Win'].shape[0] >= self.n_max[l]: break
                cp['E'][i] /= 2
                win, b, wout = cp['Win'][i].copy(), cp['bin'][i], cp['Wout'][i].copy()
                k = self.rng.integers(win.size + 1 + wout.size); d = self.rng.normal(0, self.sigma_mut)
                if k < win.size: win[k] += d
                elif k == win.size: b += d
                else: wout[k - win.size - 1] += d
                cp['Win'] = np.vstack([cp['Win'], win]); cp['bin'] = np.append(cp['bin'], b)
                cp['Wout'] = np.vstack([cp['Wout'], wout]); cp['B'] = np.vstack([cp['B'], cp['B'][i]])
                for k2 in ('E', 'Eacum', 'hbar', 'hvar', 'phat', 'grupo'): cp[k2] = np.append(cp[k2], cp[k2][i])
                if sig is not None: sig['Win'] = np.hstack([sig['Win'], sig['Win'][:, i:i + 1]])
                self.nacimientos += 1

    def tramposas(self):
        return int(sum(((c['E'] > np.median(c['E'])) & (c['hvar'] < 0.01)).sum() for c in self.capas))


# ------------------------------------------------------------------------------------------- TECHO JUSTO (fuera de la red)
class MLP2:
    """Perceptron de varias capas con RETROPROPAGACION + Adam + entropia cruzada. Banco; nunca dentro de la red."""
    def __init__(self, seed, D, K, capas=(40,), lr=0.003, b1=0.9, b2=0.999):
        r = np.random.default_rng(seed); tam = [D] + list(capas) + [K]
        self.W = [r.normal(0, 1 / np.sqrt(tam[i]), (tam[i], tam[i + 1])) for i in range(len(tam) - 1)]
        self.b = [np.zeros(tam[i + 1]) for i in range(len(tam) - 1)]
        self.m = [np.zeros_like(w) for w in self.W + self.b]; self.v = [np.zeros_like(w) for w in self.W + self.b]
        self.lr, self.b1, self.b2, self.t = lr, b1, b2, 0; self.ops = 0; self.K = K
        self.N = sum(capas); self.nacimientos = self.muertes = 0

    def _fwd(self, x):
        hs = [x]
        for i, (W, b) in enumerate(zip(self.W, self.b)):
            z = hs[-1] @ W + b; hs.append(np.tanh(z) if i < len(self.W) - 1 else z); self.ops += 2 * W.size
        return hs

    def predice(self, x): return int(np.argmax(self._fwd(x)[-1]))

    def expone(self, x, c):
        hs = self._fwd(x); z = hs[-1]; p = np.exp(z - z.max()); p /= p.sum()
        t = np.zeros(self.K); t[c] = 1; d = p - t; grads = []
        for i in range(len(self.W) - 1, -1, -1):
            grads.append((np.outer(hs[i], d), d.copy())); self.ops += 3 * 2 * self.W[i].size
            if i > 0: d = (self.W[i] @ d) * (1 - hs[i] ** 2)
        grads = grads[::-1]; self.t += 1
        params = self.W + self.b; gl = [g for g, _ in grads] + [g for _, g in grads]
        for j, (prm, g) in enumerate(zip(params, gl)):
            self.m[j] = self.b1 * self.m[j] + (1 - self.b1) * g; self.v[j] = self.b2 * self.v[j] + (1 - self.b2) * g * g
            mh = self.m[j] / (1 - self.b1 ** self.t); vh = self.v[j] / (1 - self.b2 ** self.t)
            prm -= self.lr * mh / (np.sqrt(vh) + 1e-8); self.ops += 8 * prm.size
        return float(-np.log(p[c] + 1e-12)), int(np.argmax(z)) == c

    def tramposas(self): return 0
