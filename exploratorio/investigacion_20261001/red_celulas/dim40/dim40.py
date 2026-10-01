"""
dim40.py -- Celulas en un espacio de D dimensiones con premio REGADO (1-oct-2026, exploracion, sin preregistro).

Idea del director: sin capas. N celulas con una posicion en R^D; cada una oye a sus k vecinas mas cercanas.
Entradas y salidas son celulas situadas en ese espacio. La senal da T pasos por el grafo (recurrente).
Premio: cada celula de SALIDA suelta un numero (que tan bien le fue a ella, menos su promedio) que se riega por el
grafo y decae con la distancia en saltos (lambda^saltos). Cada celula combina ese premio local con su traza
de elegibilidad (ruido propio x lo que oyo) y ajusta sus pesos de entrada: regla de tres factores, todo local.
Nada de gradiente global dentro de la red. El TECHO (MLP + Adam + entropia cruzada) esta aparte.

Tarea: paridad de 3 bits (necesita celulas intermedias). A mitad cambia la regla: mayoria de 3 bits.
"""
import numpy as np, json, time, argparse, os
from collections import deque

PATRONES = np.array([[(b >> i) & 1 for i in range(3)] for b in range(8)], float)
X_IN = PATRONES * 2 - 1                                  # +-1
T_PAR = PATRONES.sum(1) % 2                              # regla A: paridad
T_MAY = (PATRONES.sum(1) >= 2).astype(int)               # regla B: mayoria


def objetivo(regla, p):
    t = (T_PAR if regla == 'A' else T_MAY)[p]
    return np.array([1.0 if t == 0 else -1.0, 1.0 if t == 1 else -1.0]), int(t)   # dos salidas independientes (+1/-1)


def saltos_hacia(adj_in, fuentes, N):
    """adj_in[i] = lista de j que alimentan a i. Saltos de cada celula HACIA cada fuente siguiendo las flechas."""
    H = np.full((len(fuentes), N), np.inf)
    for a, o in enumerate(fuentes):
        H[a, o] = 0; q = deque([o])
        while q:
            i = q.popleft()
            for j in adj_in[i]:
                if H[a, j] == np.inf:
                    H[a, j] = H[a, i] + 1; q.append(j)
    return H


class Red:
    def __init__(self, seed, D=2, N=200, k=8, T=10, sigma=0.3, eta=0.02, lam=0.5, reparto='regado',
                 aleatorio=False, n_in=3, n_out=2, mover=0.0, gan=1.3, gan_in=3.0, salida_delta=True, eta_out=0.02, k_out=40):
        r = np.random.default_rng(seed); self.r = r
        self.salida_delta, self.eta_out, self.k_out = salida_delta, eta_out, k_out
        self.N, self.k, self.T, self.sigma, self.eta, self.lam = N, k, T, sigma, eta, lam
        self.reparto, self.D, self.mover = reparto, D, mover
        self.ent = np.arange(n_in); self.sal = np.arange(n_in, n_in + n_out)
        self.pos = r.random((N, D))
        self.aleatorio = aleatorio
        self.construye_grafo()
        self.W = r.normal(0, gan / np.sqrt(k), (N, N)) * self.M
        self.W[:, self.ent] *= gan_in                      # las entradas hablan fuerte: si no, la senal muere en 3 saltos
        self.b = np.zeros(N)
        self.norm0 = np.linalg.norm(self.W, axis=1, keepdims=True)
        self.base = np.zeros(n_out)                      # promedio movil del premio de cada salida
        self.E = np.zeros(N)                             # energia cobrada (premio positivo recibido)
        self.absr = np.zeros(N)                          # |premio| medio recibido
        self.perm = r.permutation(N)
        self.n_exp = 0

    def construye_grafo(self):
        N, k, r = self.N, self.k, self.r
        M = np.zeros((N, N))
        if self.aleatorio:
            for i in range(N):
                M[i, r.choice([j for j in range(N) if j != i], self.k_out if i in self.sal else k, replace=False)] = 1
        else:
            d = np.linalg.norm(self.pos[:, None, :] - self.pos[None, :, :], axis=2)
            np.fill_diagonal(d, np.inf)
            vec = np.argsort(d, axis=1)
            for i in range(N): M[i, vec[i, :(self.k_out if i in self.sal else k)]] = 1
        M[self.ent, :] = 0                                # las entradas no oyen a nadie: estan fijadas
        self.M = M
        adj_in = [np.nonzero(M[i])[0] for i in range(N)]
        self.H = saltos_hacia(adj_in, self.sal, N)        # saltos de cada celula hacia cada salida
        Hc = np.where(np.isinf(self.H), 0.0, self.lam ** self.H)
        if self.reparto == 'global':
            K = np.ones_like(Hc) / len(self.sal)
        else:
            K = Hc
        K[:, self.ent] = 0
        m = K.sum(0)[self.N - 0:].mean() if False else K.sum(0)[len(self.ent):].mean()
        self.K = K / max(m, 1e-9)                         # mismo premio medio por celula en todos los repartos
        if self.reparto == 'camino':                      # grupo chico: yo + mis 3 alimentadoras mas cercanas comparten
            G = np.eye(N)
            for i in range(N):
                for j in adj_in[i][:3]: G[i, j] = 1
            G = G / G.sum(1, keepdims=True)
            self.K = self.K @ G.T
        He = self.H[:, self.ent]
        self.camino_medio = float(np.mean(He[np.isfinite(He)])) if np.isfinite(He).any() else np.inf
        self.frac_alcanzadas = float(np.isfinite(self.H).all(0)[len(self.ent):].mean())

    def propaga(self, x_in, ruido=True, silencia=None):
        x = np.zeros(self.N); x[self.ent] = x_in
        xs, xis = [], []
        for t in range(self.T):
            u = self.W @ x + self.b
            xi = self.r.normal(0, self.sigma, self.N) if ruido else np.zeros(self.N)
            xi[self.ent] = 0
            if self.salida_delta: xi[self.sal] = 0
            xs.append(x.copy()); xis.append(xi)
            x = np.tanh(u + xi); x[self.ent] = x_in
            if silencia is not None: x[silencia] = 0
        return x, xs, xis

    def premio_local(self, R):
        rr = R - self.base
        r_cel = rr @ self.K                                # premio regado por celula
        if self.reparto == 'barajado': r_cel = r_cel[self.perm]
        return r_cel

    def expone(self, p, regla):
        x_in = X_IN[p]; tgt, _ = objetivo(regla, p)
        x, xs, xis = self.propaga(x_in)
        y = x[self.sal]
        R = -(y - tgt) ** 2                                # premio de cada salida (independiente)
        r_cel = self.premio_local(R)
        self.base = 0.95 * self.base + 0.05 * R
        XI, XS = np.array(xis), np.array(xs)
        elig = XI.T @ XS; eb = XI.sum(0)                   # traza: ruido propio x lo que oi, sumado en los T pasos
        self.W += self.eta * (r_cel[:, None] * elig) * self.M / self.sigma ** 2
        self.b += self.eta * r_cel * eb / self.sigma ** 2
        if self.salida_delta:
            # variante 3: la celula de salida conoce su propio error (local a ella) y usa regla delta sobre lo que oyo
            # en el ultimo paso; el resto de la red solo recibe el premio regado. Sin esto (variante 1) nadie aprende.
            d = (tgt - y) * (1 - y ** 2)
            self.W[self.sal] += self.eta_out * d[:, None] * xs[-1][None, :] * self.M[self.sal]
            self.b[self.sal] += self.eta_out * d
        # escala sinaptica (local): cada celula mantiene el tamano total de sus pesos de entrada (homeostasis);
        # sin esto el paseo al azar del ruido engorda los pesos y la red se satura (visto en el humo)
        nrm = np.linalg.norm(self.W, axis=1, keepdims=True)
        esc = np.where(nrm > 0, self.norm0 / np.maximum(nrm, 1e-9), 1.0)
        if self.salida_delta: esc[self.sal] = 1.0                    # las salidas (lectoras) no se escalan
        self.W *= esc
        np.clip(self.b, -1, 1, out=self.b)
        self.E += np.maximum(r_cel, 0); self.absr += np.abs(r_cel); self.n_exp += 1
        if self.mover > 0 and self.reparto == 'regado':    # geometria que se aprende: me acerco a quien me paga
            pass
        return int(np.argmax(y)) == objetivo(regla, p)[1]

    def evalua(self, regla, silencia=None):
        ac, perd = 0, 0.0
        for p in range(8):
            tgt, t = objetivo(regla, p)
            x, _, _ = self.propaga(X_IN[p], ruido=False, silencia=silencia)
            y = x[self.sal]; ac += int(np.argmax(y) == t); perd += float(((y - tgt) ** 2).sum())
        return ac / 8, perd / 8

    def contrafactual(self, regla):
        _, base = self.evalua(regla)
        c = np.zeros(self.N)
        for i in range(len(self.ent), self.N):
            _, pi = self.evalua(regla, silencia=i); c[i] = pi - base
        return c

    def mueve(self, modo='rico'):
        """Las celulas se MUEVEN (geometria aprendida); se reconstruye el grafo conservando los pesos de las aristas que
        sobreviven. modo 'rico': me acerco a una celula al azar si cobra mas que yo (regla local: comparo mi energia con
        la suya). modo 'azar': el MISMO tamano de paso en direccion al azar (control). modo 'quieto': nada."""
        if self.mover <= 0 or modo == 'quieto': return
        rico = self.E / (self.E.max() + 1e-9)
        for i in range(len(self.ent) + len(self.sal), self.N):
            j = self.r.choice(self.N)
            if rico[j] > rico[i]:
                paso = self.mover * (self.pos[j] - self.pos[i])
                if modo == 'azar':
                    v = self.r.normal(size=self.D); paso = v / np.linalg.norm(v) * np.linalg.norm(paso)
                self.pos[i] = np.clip(self.pos[i] + paso, 0, 1)
        Wold, Mold = self.W.copy(), self.M.copy()
        self.construye_grafo()
        self.W = np.where(self.M * Mold > 0, Wold, self.r.normal(0, 1.0 / np.sqrt(self.k), self.W.shape) * self.M)


class Techo:
    """MLP 3-h-2 con retropropagacion + Adam + entropia cruzada. Parametros comparables a N*k de la red."""
    def __init__(self, seed, h=266, lr=0.01):
        r = np.random.default_rng(seed)
        self.W1 = r.normal(0, 1 / np.sqrt(3), (3, h)); self.b1 = np.zeros(h)
        self.W2 = r.normal(0, 1 / np.sqrt(h), (h, 2)); self.b2 = np.zeros(2)
        self.p = [self.W1, self.b1, self.W2, self.b2]
        self.m = [np.zeros_like(a) for a in self.p]; self.v = [np.zeros_like(a) for a in self.p]
        self.t = 0; self.lr = lr

    def fwd(self, x):
        h = np.tanh(x @ self.W1 + self.b1); z = h @ self.W2 + self.b2
        z = z - z.max(); pr = np.exp(z); pr /= pr.sum(); return h, pr

    def expone(self, p, regla):
        x = X_IN[p]; _, t = objetivo(regla, p)
        h, pr = self.fwd(x); d2 = pr.copy(); d2[t] -= 1
        gW2 = np.outer(h, d2); gb2 = d2; dh = (self.W2 @ d2) * (1 - h ** 2)
        gW1 = np.outer(x, dh); gb1 = dh
        self.t += 1
        for a, g, m, v in zip(self.p, [gW1, gb1, gW2, gb2], self.m, self.v):
            m *= 0.9; m += 0.1 * g; v *= 0.999; v += 0.001 * g * g
            a -= self.lr * (m / (1 - 0.9 ** self.t)) / (np.sqrt(v / (1 - 0.999 ** self.t)) + 1e-8)
        return int(np.argmax(pr)) == t

    def evalua(self, regla):
        return sum(int(np.argmax(self.fwd(X_IN[p])[1]) == objetivo(regla, p)[1]) for p in range(8)) / 8, 0.0


def corre(seed, brazo, D, N=200, k=8, TA=2000, TB=2000, lam=0.5, eta=0.0003, sigma=0.03, cada=100, mover=0.0, mover_cada=200,
          modo_mover='rico', fases=('A', 'B'), contrafactual=True):
    r = np.random.default_rng(10000 + seed)
    if brazo == 'techo':
        red = Techo(seed)
    else:
        rep = {'regado': 'regado', 'barajado': 'barajado', 'global': 'global', 'camino': 'camino', 'aleatorio': 'regado',
               'congelado': 'regado'}[brazo]
        if brazo == 'congelado': eta = 0.0                 # control: el interior NO aprende; solo leen las salidas
        red = Red(seed, D=D, N=N, k=k, lam=lam, eta=eta, sigma=sigma, reparto=rep, aleatorio=(brazo == 'aleatorio'), mover=mover)
    out = {'seed': seed, 'brazo': brazo, 'D': D, 'lam': lam, 'curva': [], 'modo_mover': modo_mover}
    exp09 = {'A': None, 'B': None}
    for fase, n in (('A', TA), ('B', TB)):
        if fase not in fases: continue
        for e in range(n):
            p = int(r.integers(8))
            red.expone(p, fase)
            if mover > 0 and brazo != 'techo' and (e + 1) % mover_cada == 0: red.mueve(modo_mover)
            if (e + 1) % cada == 0:
                ac, _ = red.evalua(fase); out['curva'].append((fase, e + 1, ac))
                if ac >= 0.9 and exp09[fase] is None: exp09[fase] = e + 1
        out['acierto_' + fase] = red.evalua(fase)[0]
    out['exp09_A'], out['exp09_B'] = exp09['A'], exp09['B']
    if brazo != 'techo' and mover > 0:
        out['camino_final'] = red.camino_medio
        d_sal = np.linalg.norm(red.pos[:, None, :] - red.pos[None, red.sal, :], axis=2).min(1)
        out['dist_a_salida_final'] = float(d_sal[len(red.ent) + len(red.sal):].mean())
    if brazo != 'techo' and contrafactual:
        c = red.contrafactual('B'); E = red.E; nc = len(red.ent)
        util = c > 0.01
        premiadas = red.absr / max(red.absr[nc:].max(), 1e-9) > 0.1
        out['celulas_utiles'] = int(util[nc:].sum())
        out['utiles_con_premio'] = int((util & premiadas)[nc:].sum())
        rico = E >= np.quantile(E[nc:], 0.75)
        out['tramposas'] = int((rico & (c < 0.005))[nc:].sum())
        out['camino_medio'] = red.camino_medio
        out['frac_alcanzadas'] = red.frac_alcanzadas
        # correlacion entre premio recibido y aporte: ¿el premio discrimina quien aporto?
        a, b = red.absr[nc:], c[nc:]
        out['corr_premio_aporte'] = float(np.corrcoef(a, b)[0, 1]) if a.std() > 0 and b.std() > 0 else 0.0
    return out


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--exp', default='humo'); ap.add_argument('--semillas', type=int, default=8)
    ap.add_argument('--out', default='datos'); a = ap.parse_args()
    os.makedirs(a.out, exist_ok=True)
    t0 = time.time(); res = []
    if a.exp == 'humo':
        for br in ('regado', 'global', 'techo'):
            o = corre(1, br, 2); print(br, o['acierto_A'], o['exp09_A'], o['acierto_B'], o['exp09_B'],
                                       o.get('tramposas'), o.get('camino_medio'), round(time.time() - t0, 1)); res.append(o)
    elif a.exp == 'barrido':
        for D in (40, 1, 2, 3, 10):
            for br in ('congelado', 'regado', 'global'):
                for s in range(1, a.semillas + 1):
                    res.append(corre(s, br, D))
                    json.dump(res, open(os.path.join(a.out, 'barrido.json'), 'w'))
                print(D, br, round(time.time() - t0), flush=True)
        for D, br in ((40, 'barajado'), (40, 'camino'), (0, 'aleatorio'), (0, 'techo'), (2, 'barajado'), (2, 'camino')):
            for s in range(1, a.semillas + 1):
                res.append(corre(s, br, D)); json.dump(res, open(os.path.join(a.out, 'barrido.json'), 'w'))
            print(D, br, round(time.time() - t0), flush=True)
    elif a.exp == 'radio':
        for D in (40, 2):
            for lam in (0.1, 0.9):
                for s in range(1, a.semillas + 1):
                    res.append(corre(s, 'regado', D, lam=lam)); json.dump(res, open(os.path.join(a.out, 'radio.json'), 'w'))
                print(D, lam, round(time.time() - t0), flush=True)
    elif a.exp == 'mover':
        # interior CONGELADO (solo leen las salidas) + las celulas se mueven cada 200 exposiciones (paso 0.3).
        # Prediccion firmada: mayoria a 0.9 en < 300 exposiciones en >= 6/8 semillas con modo 'rico'; si no, se cierra.
        fn = os.path.join(a.out, 'mover.json')
        for tarea, fases, TA, TB in (('mayoria', ('B',), 0, 1500), ('paridad', ('A',), 2000, 0)):
            for D in (3, 10, 40):
                for modo in ('rico', 'azar', 'quieto'):
                    for s in range(1, a.semillas + 1):
                        o = corre(s, 'congelado', D, TA=TA, TB=TB, fases=fases, mover=0.3, modo_mover=modo, contrafactual=False)
                        o['tarea'] = tarea; res.append(o); json.dump(res, open(fn, 'w'))
                    print(tarea, D, modo, round(time.time() - t0), flush=True)
                if time.time() - t0 > 420: print('tope de CPU: corto aqui', flush=True); break
    elif a.exp == 'grande':
        for D in (3, 100):
            for s in range(1, a.semillas + 1):
                res.append(corre(s, 'regado', D, N=400)); json.dump(res, open(os.path.join(a.out, 'grande.json'), 'w'))
            print(D, round(time.time() - t0), flush=True)
    print('CPU s', round(time.time() - t0, 1))
