"""
mundo_social.py — N organismos v9 en el MISMO anillo, compartiendo los objetos. Etapa 5 (comunicación), nivel N1.

Cada organismo es v9 (organismo/organismo_v9.py, d3b72fb8819fbe8e) línea por línea: patas R-STDP, boca con valor +
hambre, canales Wp/Wn con drenaje (lam=0.05), plasticidad 2L, memoria de trabajo de rechazo. El mundo (objetos,
reposición, retirada aleatoria) es compartido.

SEÑAL (N1, apagada por defecto): al morder, el organismo emite placer (+) o asco (−) según el resultado. Los demás
organismos a distancia de anillo <= d_senal ven (patrón mordido, signo) y actualizan SU PROPIO valor de ese patrón con
Rescorla-Wagner vicario (tasa eta*f_vicaria, con drenaje, sin comer, sin energía, sin divisiones). El signo se mapea a
la escala innata (+ -> +1, − -> −3). Nunca se transmiten pesos ni códigos: cada receptor usa SU código Kenyon.
  senal=None       sin señal (N0 si hay 2 o más organismos)
  senal='honesta'  N1
  senal='barajada' mismo número de señales, signo al azar (RNG propio seed_mundo+300000): control de contenido

RNG: un generador por organismo (patas, boca, sorteo de Kenyon, reaparición al morir) y uno del mundo (reposición y
retirada). Con n=1 y compat=True el mundo usa EL MISMO generador que el organismo, en el mismo orden de llamadas que v9:
con n=1 y senal=None el resultado es bit a bit el de organismo_v9.run(seed) (control de identidad).
Orden dentro de cada paso: fase A de cada organismo (percibir, mover, morder, aprender, gastar energía) -> entrega de
señales -> retirada aleatoria del mundo -> fase B de cada organismo (aprendizaje de patas, muerte). Con n>=2 el orden
de los organismos alterna por paridad del paso.
"""
import numpy as np

L = 40; NK = 30; NKMAX = 90; K = 3
PAT = {'A': np.array([1, 1, 0, 1, 0, 0.]), 'B': np.array([1, 0, 1, 0, 1, 0.]),
       'C': np.array([0, 1, 1, 0, 0, 1.]), 'D': np.array([0, 0, 1, 0, 1, 1.])}
R_VAL = {'comida': 1.0, 'veneno': -3.0}; E_VAL = {'comida': +0.8, 'veneno': -0.4}


class Mundo:
    def __init__(self, rng, nobj, tipos):
        self.rng = rng; self.nobj = nobj; self.tipos = tipos; self.objs = {}

    def spawn(self):
        while len(self.objs) < self.nobj:
            x = int(self.rng.integers(L))
            if x not in self.objs: self.objs[x] = self.tipos[int(self.rng.integers(len(self.tipos)))]


class Organismo:
    def __init__(self, rng, T, eta=.03, tau_e=.85, alpha=1.2, hambre_boca=2.0, aversion=1.0, costo=.002, plast=True,
                 theta=0.6, ema=0.02, paso=0.5, lam=0.05, memoria_rechazo=20, learn=True):
        self.rng = rng; self.T = T; self.eta = eta; self.tau_e = tau_e; self.alpha = alpha; self.hambre_boca = hambre_boca
        self.aversion = aversion; self.costo = costo; self.plast = plast; self.theta = theta; self.ema = ema; self.paso = paso
        self.lam = lam; self.memoria_rechazo = memoria_rechazo; self.learn = learn
        self.Wl = rng.uniform(.1, .4, (2, 9)); self.KW = np.zeros((NKMAX, 6)); self.activa = np.zeros(NKMAX, bool)
        self.KW[:NK] = rng.uniform(0, 1, (NK, 6)); self.activa[:NK] = True
        while not (len(self.code(PAT['A']) & self.code(PAT['B'])) == 0):
            self.KW[0:NK] = rng.uniform(0, 1, (NK, 6))
        self.Wp = np.zeros(NKMAX); self.Wn = np.zeros(NKMAX); self.err = np.zeros(NKMAX); self.mu = np.zeros((NKMAX, 6))
        self.splits = 0; self.el = np.zeros_like(self.Wl); self.tr = np.zeros(9)
        self.pos = 0; self.E = 1.0; self._rech = {}; self._prev_on = -1
        self.split_t = []; self.mord = {k: [0] * 4 for k in PAT}; self.vis = {k: [0] * 4 for k in PAT}; self.deaths = 0
        self.dq = [0] * 4; self.veneno_propio = {k: 0 for k in PAT}; self.n_crit = {}; self.vicarias = {k: 0 for k in PAT}
        self.t_ext_B = None; self.R = 0.; self.Rp = 0.; self.hambre = 0.

    def q(self, t): return min(t // (self.T // 4), 3)

    def code(self, P):
        v = self.KW @ P; v = np.where(self.activa, v, -1e9); return set(np.argsort(v)[-K:])

    def kenyon(self, P):
        k = np.zeros(NKMAX); k[list(self.code(P))] = 1; return k

    def valor(self, kk): return float((self.Wp - self.Wn) @ self.kenyon(PAT[kk]))

    def see(self, objs, t):
        best = None
        for x, k in objs.items():
            if self.memoria_rechazo and self._rech.get(x, -1) > t: continue
            dl = (self.pos - x) % L; dr = (x - self.pos) % L; d = min(dl, dr)
            if best is None or d < best[0]: best = (d, k, dl < dr)
        if best is None:
            for x, k in objs.items():
                dl = (self.pos - x) % L; dr = (x - self.pos) % L; d = min(dl, dr)
                if best is None or d < best[0]: best = (d, k, dl < dr)
        return best

    def _criterios(self, val, t, invertir_en):
        for kk in ('A', 'B'):
            if (kk not in self.n_crit) and val[kk] == 'veneno' and self.valor(kk) <= -2.5:
                self.n_crit[kk] = self.veneno_propio[kk]
        if invertir_en is not None and t >= invertir_en and self.t_ext_B is None and self.valor('B') >= 0:
            self.t_ext_B = t

    def fase_A(self, mundo, val, t, invertir_en):
        """Percibir, mover, morder, aprender (boca y valor), gastar energia. Devuelve (pos, kk, signo) si mordio."""
        rng = self.rng; objs = mundo.objs; emitida = None
        hambre = np.clip(1 - self.E, 0, 1); self.hambre = hambre; d, k, left = self.see(objs, t); pat = PAT[k]
        x = np.concatenate([pat * 1.2, [1.5 if left else 0, 0 if left else 1.5, 1.0 if d == 0 else 0.]]); noise = .15 + .5 * hambre
        V = self.Wl @ x; p = 1 / (1 + np.exp(-(V - .8) / noise)); u = p + rng.normal(0, .3, 2); m = np.zeros(2)
        if u.max() > .5: m[np.argmax(u)] = 1
        self.tr = self.tr * .7 + x
        if self.learn: self.el = self.el * self.tau_e + np.outer(m - p, self.tr)
        self.pos = (self.pos + int(m[1] - m[0])) % L; d2, _, _ = self.see(objs, t); self.Rp = .2 if d2 < d else 0.
        self.R = 0.
        if self.pos in objs:
            kk = objs[self.pos]; kc = self.kenyon(PAT[kk]); Wb = self.Wp - self.Wn
            Vb = self.alpha * (Wb @ kc) + self.hambre_boca * hambre + .5; pb = 1 / (1 + np.exp(-Vb / .3)); mordio = rng.random() < pb
            self.vis[kk][self.q(t)] += 1
            if self.memoria_rechazo and not mordio: self._rech[self.pos] = t + self.memoria_rechazo
            if mordio:
                self.R = R_VAL[val[kk]]; self.E = min(self.E + E_VAL[val[kk]], 1.5); self.mord[kk][self.q(t)] += 1
                if val[kk] == 'veneno': self.veneno_propio[kk] += 1
                emitida = (self.pos, kk, 1 if self.R > 0 else -1)
                del objs[self.pos]; mundo.spawn()
                self._rech.pop(self.pos, None)
                if self.learn:
                    self._aprender(kk, kc, Wb, self.R, self.eta, t, dividir=True)
            self._criterios(val, t, invertir_en)
        self._prev_on = self.pos if self.pos in objs else -1
        self.E -= self.costo
        return emitida

    def _aprender(self, kk, kc, Wb, R, eta, t, dividir):
        dlt = R - Wb @ kc
        if self.lam: ix = kc > 0; mcom = np.minimum(self.Wp[ix], self.Wn[ix]); self.Wp[ix] -= self.lam * mcom; self.Wn[ix] -= self.lam * mcom
        if dlt > 0: self.Wp = np.clip(self.Wp + eta * dlt * kc, 0, 3.)
        else:       self.Wn = np.clip(self.Wn + eta * self.aversion * (-dlt) * kc, 0, 3.)
        if dividir and self.plast:
            P = PAT[kk]; idx = np.where(kc > 0)[0]; self.err[idx] = (1 - self.ema) * self.err[idx] + self.ema * abs(dlt)
            self.mu[idx] = (1 - self.ema) * self.mu[idx] + self.ema * P
            for c in idx:
                if self.err[c] > self.theta and (~self.activa).any():
                    j = int(np.where(~self.activa)[0][0]); self.activa[j] = True; dist = P - self.mu[c]
                    self.KW[j] = np.clip(self.KW[c] + self.paso * dist, 0, 5); self.KW[c] = np.clip(self.KW[c] - self.paso * dist, 0, 5)
                    self.Wp[j] = self.Wp[c]; self.Wn[j] = self.Wn[c]; self.mu[j] = self.mu[c].copy(); self.err[c] = self.err[j] = 0
                    self.splits += 1; self.split_t.append((t, kk))

    def recibir(self, kk, signo, f_vicaria, val, t, invertir_en):
        """Aprendizaje vicario: la señal dice +/− del patron kk; escala innata + -> +1, − -> −3. Sin divisiones."""
        if not self.learn: return
        kc = self.kenyon(PAT[kk]); Wb = self.Wp - self.Wn
        self._aprender(kk, kc, Wb, 1.0 if signo > 0 else -3.0, self.eta * f_vicaria, t, dividir=False)
        self.vicarias[kk] += 1
        self._criterios(val, t, invertir_en)

    def fase_B(self, t):
        if self.learn: self.Wl = np.clip(self.Wl + self.eta * (1 + 2 * self.hambre) * (max(self.R, 0) + self.Rp) * self.el, 0, 1.5)
        if self.E <= 0: self.deaths += 1; self.E = .6; self.pos = int(self.rng.integers(L)); self.dq[self.q(t)] += 1

    def resultado(self):
        W = {k: round(float((self.Wp - self.Wn) @ self.kenyon(PAT[k])), 2) for k in PAT}
        comp = {k: (round(float(self.Wp @ self.kenyon(PAT[k])), 2), round(float(self.Wn @ self.kenyon(PAT[k])), 2)) for k in PAT}
        return dict(W=W, comp=comp, mord=self.mord, vis=self.vis, deaths=self.deaths, splits=self.splits, split_t=self.split_t,
                    celdas=int(self.activa.sum()), dq=self.dq, n_crit=self.n_crit, veneno_propio=self.veneno_propio,
                    vicarias=self.vicarias, t_ext_B=self.t_ext_B)


def run(seed, n=1, T=100000, invertir_en=None, senal=None, d_senal=5, f_vicaria=1/3, nobj_por_org=4, compat=True, **kw_org):
    rngs = [np.random.default_rng(seed + 100000 * i) for i in range(n)]
    orgs = [Organismo(rngs[i], T, **kw_org) for i in range(n)]
    rng_mundo = rngs[0] if (n == 1 and compat) else np.random.default_rng(seed + 900000)
    rng_senal = np.random.default_rng(seed + 300000)
    val = {'A': 'comida', 'B': 'veneno'}
    mundo = Mundo(rng_mundo, nobj_por_org * n, ['A', 'B']); mundo.spawn()
    senales_emitidas = [0] * n; senales_recibidas = [0] * n
    for t in range(T):
        if invertir_en is not None and t == invertir_en: val = {'A': 'veneno', 'B': 'comida'}
        orden = range(n) if t % 2 == 0 else range(n - 1, -1, -1)
        emitidas = []
        for i in orden:
            e = orgs[i].fase_A(mundo, val, t, invertir_en)
            if e is not None:
                emitidas.append((i, e)); senales_emitidas[i] += 1
        if senal is not None and n > 1:
            for i, (px, kk, signo) in emitidas:
                s = signo if senal == 'honesta' else (1 if rng_senal.random() < .5 else -1)
                for j in range(n):
                    if j == i: continue
                    dl = (orgs[j].pos - px) % L; dist = min(dl, L - dl)
                    if dist <= d_senal:
                        orgs[j].recibir(kk, s, f_vicaria, val, t, invertir_en); senales_recibidas[j] += 1
        if mundo.rng.random() < .003 and mundo.objs:
            _dx = list(mundo.objs)[int(mundo.rng.integers(len(mundo.objs)))]; del mundo.objs[_dx]; mundo.spawn()
            for o in orgs: o._rech.pop(_dx, None)
        for i in orden:
            orgs[i].fase_B(t)
    out = [o.resultado() for o in orgs]
    for i in range(n):
        out[i]['senales_emitidas'] = senales_emitidas[i]; out[i]['senales_recibidas'] = senales_recibidas[i]
    return out
