"""
LA HAMBURGUESA (1-oct-2026, exploracion sin preregistro).
PAN  = transformador diminuto entrenado con gradiente (retropropagacion a mano, numpy puro) y luego CONGELADO.
CARNE = celulas de memoria viva con reglas locales (compuerta por estado propio, energia/olvido por escasez,
        pago por camino chico) que leen el ESTADO INTERNO del pan y pisan su salida. PERSISTEN entre secuencias.

Mundo de simbolos: G grupos (hechos), P parafrasis por hecho, V valores.
Secuencia: [ g i = v ; ]*0..3  ? g i  -> predecir v.
Regla del pan (preentrenada): si en el contexto hay un hecho del mismo grupo g, responde su valor; si no, base[g].
"""
import numpy as np, json, time, sys, argparse

G, P, V = 20, 3, 8
T_Q, T_EQ, T_SEP, T_PAD = G + P + V, G + P + V + 1, G + P + V + 2, G + P + V + 3
VOC = G + P + V + 4
NC_MAX = 3
L = NC_MAX * 5 + 3           # 18 tokens; se rellena a la IZQUIERDA con PAD
D, H, DF, NB = 24, 2, 96, 2    # 2 bloques: copiar del contexto (cabeza de induccion) necesita 2 capas
DH = D // H
THETA = 0.9                    # compuerta (coseno) por defecto; 0.98 en la segunda serie (ver informe)


def tok_val(v): return G + P + v
def tok_par(i): return G + i


def arma_secuencia(ctx, g, i):
    """ctx: lista de (g, i, v). Devuelve array de L tokens con PAD a la izquierda."""
    s = []
    for (cg, ci, cv) in ctx:
        s += [cg, tok_par(ci), T_EQ, tok_val(cv), T_SEP]
    s += [T_Q, g, tok_par(i)]
    return np.array([T_PAD] * (L - len(s)) + s, dtype=np.int64)


# ---------------------------------------------------------------- transformador con retropropagacion a mano
class Transformador:
    def __init__(self, seed):
        r = np.random.default_rng(seed)
        sc = 0.3
        self.p = {'E': r.normal(0, sc, (VOC, D)), 'Pos': r.normal(0, sc, (L, D)),
                  'Wout': r.normal(0, 1 / np.sqrt(D), (D, VOC)), 'bout': np.zeros(VOC)}
        for b in range(NB):
            self.p.update({
                f'Wq{b}': r.normal(0, sc / np.sqrt(D), (D, D)), f'Wk{b}': r.normal(0, sc / np.sqrt(D), (D, D)),
                f'Wv{b}': r.normal(0, sc / np.sqrt(D), (D, D)), f'Wo{b}': r.normal(0, sc / np.sqrt(D), (D, D)),
                f'W1{b}': r.normal(0, 1 / np.sqrt(D), (D, DF)), f'b1{b}': np.zeros(DF),
                f'W2{b}': r.normal(0, 1 / np.sqrt(DF), (DF, D)), f'b2{b}': np.zeros(D)})
        self.m = {k: np.zeros_like(v) for k, v in self.p.items()}
        self.v = {k: np.zeros_like(v) for k, v in self.p.items()}
        self.t = 0
        self.mask = np.triu(np.ones((L, L), bool), 1)
        self.ops_forward = NB * (L * (4 * D * D + 2 * D * DF) + 2 * H * L * L * DH) + D * VOC  # multiplicaciones-sumas aprox.

    def forward(self, toks):
        """toks (B, L). Devuelve logits (B, VOC) de la ULTIMA posicion y guarda el cache."""
        p = self.p; B = toks.shape[0]
        X = p['E'][toks] + p['Pos'][None]                      # (B,L,D)
        self.cache = [toks]; self.capas = []
        for b in range(NB):
            X0 = X
            Q = (X0 @ p[f'Wq{b}']).reshape(B, L, H, DH).transpose(0, 2, 1, 3)   # (B,H,L,DH)
            K = (X0 @ p[f'Wk{b}']).reshape(B, L, H, DH).transpose(0, 2, 1, 3)
            Vv = (X0 @ p[f'Wv{b}']).reshape(B, L, H, DH).transpose(0, 2, 1, 3)
            S = Q @ K.transpose(0, 1, 3, 2) / np.sqrt(DH)
            S = np.where(self.mask[None, None], -1e9, S)
            S = S - S.max(-1, keepdims=True)
            A = np.exp(S); A /= A.sum(-1, keepdims=True)
            Oc = (A @ Vv).transpose(0, 2, 1, 3).reshape(B, L, D)
            X1 = X0 + Oc @ p[f'Wo{b}']
            Hm = np.maximum(X1 @ p[f'W1{b}'] + p[f'b1{b}'], 0)
            X2 = X1 + Hm @ p[f'W2{b}'] + p[f'b2{b}']
            self.capas.append((X0, Q, K, Vv, A, Oc, X1, Hm, X2)); X = X2
        logits = X[:, -1] @ p['Wout'] + p['bout']
        return logits

    def estados(self):
        """estados internos de la ultima posicion: (tras el bloque 1, tras el ultimo bloque)."""
        return self.capas[0][-1][:, -1], self.capas[-1][-1][:, -1]

    def backward(self, logits, y):
        toks = self.cache[0]; p = self.p; B = toks.shape[0]
        pr = np.exp(logits - logits.max(1, keepdims=True)); pr /= pr.sum(1, keepdims=True)
        dl = pr.copy(); dl[np.arange(B), y] -= 1; dl /= B
        g = {}
        Xtop = self.capas[-1][-1]
        g['Wout'] = Xtop[:, -1].T @ dl; g['bout'] = dl.sum(0)
        dX = np.zeros_like(Xtop); dX[:, -1] = dl @ p['Wout'].T
        for b in reversed(range(NB)):
            X0, Q, K, Vv, A, Oc, X1, Hm, X2 = self.capas[b]
            dX2 = dX
            g[f'W2{b}'] = np.tensordot(Hm, dX2, ((0, 1), (0, 1))); g[f'b2{b}'] = dX2.sum((0, 1))
            dHm = (dX2 @ p[f'W2{b}'].T) * (Hm > 0)
            g[f'W1{b}'] = np.tensordot(X1, dHm, ((0, 1), (0, 1))); g[f'b1{b}'] = dHm.sum((0, 1))
            dX1 = dX2 + dHm @ p[f'W1{b}'].T
            g[f'Wo{b}'] = np.tensordot(Oc, dX1, ((0, 1), (0, 1)))
            dOc = (dX1 @ p[f'Wo{b}'].T).reshape(B, L, H, DH).transpose(0, 2, 1, 3)   # (B,H,L,DH)
            dA = dOc @ Vv.transpose(0, 1, 3, 2)
            dV = A.transpose(0, 1, 3, 2) @ dOc
            dS = A * (dA - (dA * A).sum(-1, keepdims=True)) / np.sqrt(DH)
            dQ = (dS @ K).transpose(0, 2, 1, 3).reshape(B, L, D)
            dK = (dS.transpose(0, 1, 3, 2) @ Q).transpose(0, 2, 1, 3).reshape(B, L, D)
            dV = dV.transpose(0, 2, 1, 3).reshape(B, L, D)
            g[f'Wq{b}'] = np.tensordot(X0, dQ, ((0, 1), (0, 1))); g[f'Wk{b}'] = np.tensordot(X0, dK, ((0, 1), (0, 1)))
            g[f'Wv{b}'] = np.tensordot(X0, dV, ((0, 1), (0, 1)))
            dX = dX1 + dQ @ p[f'Wq{b}'].T + dK @ p[f'Wk{b}'].T + dV @ p[f'Wv{b}'].T
        g['Pos'] = dX.sum(0)
        gE = np.zeros_like(p['E']); np.add.at(gE, toks.reshape(-1), dX.reshape(-1, D)); g['E'] = gE
        return g

    def paso_adam(self, g, lr, b1=0.9, b2=0.999, eps=1e-8):
        self.t += 1
        for k in self.p:
            self.m[k] = b1 * self.m[k] + (1 - b1) * g[k]
            self.v[k] = b2 * self.v[k] + (1 - b2) * g[k] ** 2
            mh = self.m[k] / (1 - b1 ** self.t); vh = self.v[k] / (1 - b2 ** self.t)
            self.p[k] -= lr * mh / (np.sqrt(vh) + eps)

    def entrena_lote(self, toks, y, lr):
        lg = self.forward(toks); g = self.backward(lg, y); self.paso_adam(g, lr)
        return float(np.mean(np.argmax(lg, 1) == y))

    def copia(self):
        t = Transformador.__new__(Transformador)
        t.p = {k: v.copy() for k, v in self.p.items()}
        t.m = {k: np.zeros_like(v) for k, v in self.p.items()}
        t.v = {k: np.zeros_like(v) for k, v in self.p.items()}
        t.t = 0; t.mask = self.mask; t.ops_forward = self.ops_forward
        return t


def comprueba_gradiente(seed=0):
    """diferencias finitas sobre unos pesos (una vez; cordura del instrumento)."""
    tr = Transformador(seed); r = np.random.default_rng(seed)
    toks = r.integers(0, VOC, (3, L)); y = r.integers(0, VOC, 3)
    lg = tr.forward(toks); g = tr.backward(lg, y)
    def perdida():
        lg = tr.forward(toks); pr = np.exp(lg - lg.max(1, keepdims=True)); pr /= pr.sum(1, keepdims=True)
        return -np.mean(np.log(pr[np.arange(3), y]))
    peor = 0
    for k in ['Wq0', 'Wk0', 'Wv0', 'Wo0', 'W11', 'W21', 'E', 'Pos', 'Wout', 'b10', 'Wq1', 'Wv1']:
        for _ in range(3):
            idx = tuple(r.integers(0, s) for s in tr.p[k].shape)
            old = tr.p[k][idx]; e = 1e-5
            tr.p[k][idx] = old + e; lp = perdida(); tr.p[k][idx] = old - e; lm = perdida(); tr.p[k][idx] = old
            num = (lp - lm) / (2 * e); ana = g[k][idx]
            err = abs(num - ana) / (abs(num) + abs(ana) + 1e-8); peor = max(peor, err)
    return peor


# ---------------------------------------------------------------- mundo y preentrenamiento
def lote_pre(rng, base, B):
    toks = np.zeros((B, L), np.int64); y = np.zeros(B, np.int64)
    for b in range(B):
        nc = int(rng.integers(0, NC_MAX + 1))
        gs = rng.choice(G, nc, replace=False)
        ctx = [(int(g), int(rng.integers(P)), int(rng.integers(V))) for g in gs]
        gq = int(rng.integers(G)); iq = int(rng.integers(P))
        if nc and rng.random() < 0.5:
            j = int(rng.integers(nc)); gq = ctx[j][0]; v = ctx[j][2]
        else:
            v = int(base[gq]) if gq not in gs else [c[2] for c in ctx if c[0] == gq][0]
        toks[b] = arma_secuencia(ctx, gq, iq); y[b] = tok_val(v)
    return toks, y


def preentrena(seed, pasos=4000, B=64, lr=3e-3):
    import os
    rng = np.random.default_rng(seed); base = rng.integers(0, V, G)
    tr = Transformador(seed)
    f = f'datos/pan_s{seed}.npz'
    if os.path.exists(f):
        z = np.load(f); tr.p = {k: z[k] for k in tr.p}
    else:
        for s in range(pasos):
            toks, y = lote_pre(rng, base, B)
            tr.entrena_lote(toks, y, lr * (0.1 if s > pasos * 0.8 else 1.0))
        np.savez(f, **tr.p)
    # cordura: acierto sin contexto (hechos base) y con contexto (copia)
    rr = np.random.default_rng(seed + 5)
    t0 = np.array([arma_secuencia([], g, i) for g in range(G) for i in range(P)]); y0 = np.array([tok_val(base[g]) for g in range(G) for i in range(P)])
    a_base = float(np.mean(np.argmax(tr.forward(t0), 1) == y0))
    tc, yc = lote_pre(rr, base, 300); a_ctx = float(np.mean(np.argmax(tr.forward(tc), 1) == yc))
    return tr, base, a_base, a_ctx


# ---------------------------------------------------------------- brazos
class Brazo:
    """todos responden a una consulta (g, i) y luego reciben la verdad c (valor 0..V-1)."""
    nombre = 'congelado'
    def __init__(self, tr, C, seed): self.tr = tr; self.C = C; self.ops = 0; self.rng = np.random.default_rng(seed + 99)
    def _pan(self, ctx, g, i):
        lg = self.tr.forward(arma_secuencia(ctx, g, i)[None]); self.ops += self.tr.ops_forward
        return int(np.argmax(lg[0])) - (G + P)
    def responde(self, g, i): self._yf = self._pan([], g, i); return self._yf
    def aprende(self, g, i, c, r): pass
    def memoria(self): return 0


class Ventana(Brazo):
    """lo que hace la industria: meter los ultimos hechos vistos en el contexto (ventana finita)."""
    nombre = 'ventana'
    def __init__(self, tr, C, seed): super().__init__(tr, C, seed); self.rec = []
    def responde(self, g, i): return self._pan(self.rec[-NC_MAX:], g, i)
    def aprende(self, g, i, c, r): self.rec.append((g, i, c)); self.rec = self.rec[-NC_MAX:]
    def memoria(self): return len(self.rec)


class RAG(Brazo):
    """almacen de C hechos (LRU) + recuperacion por el token del grupo -> al contexto. Rival fuerte y realista."""
    nombre = 'rag'
    def __init__(self, tr, C, seed): super().__init__(tr, C, seed); self.d = {}; self.orden = []
    def responde(self, g, i):
        ctx = [(g, self.d[g][0], self.d[g][1])] if g in self.d else []
        return self._pan(ctx, g, i)
    def aprende(self, g, i, c, r):
        if r != c:
            self.d[g] = (i, c)
            if g in self.orden: self.orden.remove(g)
            self.orden.append(g)
            while len(self.d) > self.C: self.d.pop(self.orden.pop(0))
    def memoria(self): return len(self.d)


class Hamburguesa(Brazo):
    """celulas de memoria viva sobre el estado interno del pan.
    clave = estado interno (normalizado) en la posicion de la consulta; valor = correccion (el valor correcto).
    compuerta propia, energia, pago por camino chico, suelta la correccion si pisa donde el pan acertaba."""
    nombre = 'hamburguesa'
    def __init__(self, tr, C, seed, theta=None, c_exist=0.002, pago=1.0, castigo=0.25, eta=0.3,
                 barajar=False, camino=True, compuerta=True, capa='x2', E0=1.0):
        super().__init__(tr, C, seed)
        if theta is None: theta = THETA
        self.dim = 2 * D if capa == 'ambas' else D
        self.W = np.zeros((0, self.dim)); self.Vv = np.zeros(0, int); self.E = np.zeros(0); self.conf = np.zeros(0)
        self.ep = []       # episodio (tokens, y) por celula, para el sueno
        self.theta, self.c_exist, self.pago, self.castigo, self.eta = theta, c_exist, pago, castigo, eta
        self.barajar, self.camino, self.compuerta, self.capa, self.E0 = barajar, camino, compuerta, capa, E0
        self.nac = self.mue = self.pisadas = 0

    @property
    def N(self): return self.W.shape[0]

    def clave(self):
        x1, x2 = self.tr.estados()
        if self.capa == 'x1': k = x1[0]
        elif self.capa == 'ambas': k = np.concatenate([x1[0] / (np.linalg.norm(x1[0]) + 1e-8), x2[0] / (np.linalg.norm(x2[0]) + 1e-8)]) / np.sqrt(2)
        else: k = x2[0]
        return k / (np.linalg.norm(k) + 1e-8) if self.capa != 'ambas' else k

    def responde(self, g, i):
        yf = self._pan([], g, i); x = self.clave(); self._toks = arma_secuencia([], g, i)
        act = np.zeros(0, bool); cand = act; s = None
        if self.N:
            s = self.W @ x; self.ops += 2 * self.W.size        # coseno (claves unitarias)
            cand = s > self.theta
            if self.compuerta:
                act = cand & (self.Vv != yf) & (self.conf > 0)
            else:
                act = np.ones(self.N, bool)                    # SIN compuerta: la celula mas parecida pisa SIEMPRE
        if act.any():
            j = int(np.argmax(np.where(act, s, -1))); r = int(self.Vv[j]); self.pisadas += 1
        else:
            j = -1; r = yf
        self._ult = (x, yf, act, cand, j, r)
        return r

    def _mata(self, viva):
        self.mue += int((~viva).sum())
        self.W, self.Vv, self.E, self.conf = self.W[viva], self.Vv[viva], self.E[viva], self.conf[viva]
        self.ep = [e for e, v in zip(self.ep, viva) if v]

    def aprende(self, g, i, c, r):
        x, yf, act, cand, j, r = self._ult
        if self.N:
            self.E -= self.c_exist
            if j >= 0:
                k = j if not self.barajar else int(self.rng.integers(self.N))
                if r == c and yf != c:                                  # mi correccion valio: cobro
                    if self.camino and cand.any():
                        grupo = np.where(cand)[0]
                        if self.barajar: grupo = self.rng.choice(self.N, len(grupo), replace=False)
                        self.E[grupo] += self.pago / len(grupo); self.conf[grupo] += 1.0 / len(grupo)
                    else:
                        self.E[k] += self.pago; self.conf[k] += 1
                    self.W[k] += 0.2 * (x - self.W[k]); self.W[k] /= np.linalg.norm(self.W[k])
                elif r != c and yf == c:                                # pise donde el pan ACERTABA: suelto y muero
                    self.conf[k] = 0.0; self.E[k] = -1.0
                elif r != c:                                            # fallamos los dos: el hecho cambio otra vez
                    self.E[k] -= self.castigo; self.Vv[k] = c; self.ep[k] = (self._toks, tok_val(c))
                    self.W[k] += self.eta * (x - self.W[k]); self.W[k] /= np.linalg.norm(self.W[k])
            elif not self.compuerta and r != c and yf == c:
                pass
            muertas = self.E < 0
            if muertas.any(): self._mata(~muertas)
        if r != c and j < 0 and yf != c:                                # nadie piso y el pan fallo: nace una celula
            if self.N >= self.C:
                viva = np.ones(self.N, bool); viva[int(np.argmin(self.E))] = False; self._mata(viva)
            self.W = np.vstack([self.W, x]); self.Vv = np.append(self.Vv, c)
            self.E = np.append(self.E, self.E0); self.conf = np.append(self.conf, 1.0); self.nac += 1
            self.ep.append((self._toks, tok_val(c)))

    def memoria(self): return self.N


class Techo(Brazo):
    """seguir entrenando el pan con gradiente en linea (un paso de Adam por consulta fallida)."""
    nombre = 'techo'
    def __init__(self, tr, C, seed, lr=1e-3): super().__init__(tr.copia(), C, seed); self.lr = lr
    def aprende(self, g, i, c, r):
        if r != c:
            self.tr.entrena_lote(arma_secuencia([], g, i)[None], np.array([tok_val(c)]), self.lr)
            self.ops += 3 * self.tr.ops_forward


class Sueno(Hamburguesa):
    """hamburguesa + sueno: cada `cada` consultas el pan absorbe con gradiente los episodios de las celulas
    (mas pseudo-ensayo: consultas al azar con las respuestas del propio pan, para no romper lo sabido),
    y las celulas cuya correccion el pan ya da solo, mueren (se liberan)."""
    nombre = 'sueno'
    def __init__(self, tr, C, seed, cada=300, pasos=30, lr=1e-3, ensayo=True, **kw):
        super().__init__(tr.copia(), C, seed, **kw); self.cada, self.pasos, self.lr, self.ensayo = cada, pasos, lr, ensayo
        self.t = 0; self.liberadas = 0; self.suenos = 0
    def aprende(self, g, i, c, r):
        super().aprende(g, i, c, r); self.t += 1
        if self.t % self.cada == 0 and self.N: self.duerme()
    def duerme(self):
        self.suenos += 1
        tk = np.array([e[0] for e in self.ep]); y = np.array([e[1] for e in self.ep])
        if self.ensayo:                                                 # pseudo-ensayo: el pan se sueña a si mismo
            gs = self.rng.integers(0, G, 2 * len(y)); is_ = self.rng.integers(0, P, 2 * len(y))
            tk2 = np.array([arma_secuencia([], int(a), int(b)) for a, b in zip(gs, is_)])
            y2 = np.argmax(self.tr.forward(tk2), 1); self.ops += 2 * len(y) * self.tr.ops_forward
            tk = np.vstack([tk, tk2]); y = np.concatenate([y, y2])
        for _ in range(self.pasos):
            self.tr.entrena_lote(tk, y, self.lr); self.ops += 3 * len(y) * self.tr.ops_forward
        # liberar: si el pan ya responde solo lo que la celula corrige, la celula se va
        tk = np.array([e[0] for e in self.ep]); y = np.array([e[1] for e in self.ep])
        ok = np.argmax(self.tr.forward(tk), 1) == y; self.ops += len(y) * self.tr.ops_forward
        if ok.any(): self.liberadas += int(ok.sum()); self._mata(~ok)


# ---------------------------------------------------------------- calendarios y corrida
def calendario(nombre, base, rng, T):
    """devuelve (valor_actual inicial, eventos {t: {g: v_nuevo}}, T)."""
    w = base.copy(); ev = {}
    def cambia(gs):
        d = {}
        for g in gs:
            nv = int(rng.integers(V - 1)); nv = nv + (nv >= w[g]); d[int(g)] = nv
        return d
    if nombre == 'tandas':                 # (a)+(b): 8 cambian; luego otros 8; luego los primeros VUELVEN
        A = rng.choice(G, 8, replace=False); Bs = rng.choice([g for g in range(G) if g not in A], 8, replace=False)
        ev[0] = cambia(A); ev[T // 3] = cambia(Bs); ev[2 * T // 3] = {int(g): int(base[g]) for g in A}
    elif nombre == 'regla':                # (c): regla nueva: TODOS los hechos corren +1
        ev[0] = {g: int((base[g] + 1) % V) for g in range(G)}
    elif nombre == 'deriva_zipf':          # cambios continuos, consultas con frecuencia desigual
        for t in range(0, T, T // 6): ev[t] = cambia(rng.choice(G, 4, replace=False))
    return w, ev


def corre(seed, cal, C, brazos, T=1500, ventana_rec=100, una_vez=True):
    rng = np.random.default_rng(seed)
    tr, base, a_base, a_ctx = preentrena(seed)
    w, ev = calendario(cal, base, rng, T)
    pz = 1.0 / np.arange(1, G + 1); pz /= pz.sum()
    pq = pz if cal == 'deriva_zipf' else np.ones(G) / G
    pq = pq[rng.permutation(G)]
    res = {}
    for nombre, fab in brazos.items():
        rq = np.random.default_rng(seed + 11); br = fab(tr, C, seed)
        cambiado = np.zeros(G, bool); visto = np.zeros((G, P), int) - 1   # ultima vez que (g,i) se vio con el valor actual
        ult_cambio = np.zeros(G, int) - 10 ** 9
        reg = []                                                          # (t, cambiado?, vecina?, acierto, peso)
        rec = {}; primera = []; pendiente = {}                            # (a): primera consulta tras la exposicion UNICA
        w = base.copy()
        for t in range(T):
            if t in ev:
                for g, v in ev[t].items():
                    w[g] = v; cambiado[g] = (v != base[g]); visto[g] = -1; ult_cambio[g] = t
                    if una_vez:                                          # (a): exposicion UNICA inmediata
                        i0 = int(rq.integers(P)); r = br.responde(g, i0); br.aprende(g, i0, int(v), r); visto[g, i0] = t
                        pendiente[g] = t
            g = int(rq.choice(G, p=pq)); i = int(rq.integers(P)); c = int(w[g])
            r = br.responde(g, i); ok = int(r == c)
            if g in pendiente: primera.append((t - pendiente.pop(g), ok))   # cuantas secuencias despues y si acerto
            vecina = cambiado[g] and visto[g, i] < 0 and (visto[g] >= 0).any()  # parafrasis nueva de un hecho ya expuesto con otra
            reg.append((t, int(cambiado[g]), int(vecina), ok, float(pq[g])))
            br.aprende(g, i, c, r); visto[g, i] = t
            # rompe lo sabido? (cada 100 consultas, sin aprender): hechos NO cambiados, sin contexto
            if t % ventana_rec == ventana_rec - 1:
                pass
        reg = np.array(reg)
        camb = reg[reg[:, 1] == 1]; noc = reg[reg[:, 1] == 0]; vec = reg[reg[:, 2] == 1]
        def pond(a): return float(np.average(a[:, 3], weights=a[:, 4])) if len(a) else float('nan')
        # exposiciones hasta recuperar 0.9 en cambiados (ventana movil de 40 consultas a cambiados) tras cada evento
        recup = {}
        for te in sorted(ev):
            te_fin = min([x for x in sorted(ev) if x > te] + [T])
            seg = camb[(camb[:, 0] >= te) & (camb[:, 0] < te_fin)]
            recup[str(te)] = None
            for k in range(40, len(seg) + 1):
                if seg[k - 40:k, 3].mean() >= 0.9: recup[str(te)] = int(seg[k - 1, 0] - te); break
        # lo sabido al final: hechos no cambiados, todas las parafrasis, sin aprender
        gs_nc = [g for g in range(G) if w[g] == base[g]]
        sab = np.mean([br.responde(g, i) == base[g] for g in gs_nc for i in range(P)]) if gs_nc else float('nan')
        pr = np.array(primera) if primera else np.zeros((0, 2))
        res[nombre] = dict(camb=pond(camb), nocamb=pond(noc), vecina=pond(vec), n_vec=int(len(vec)), recup=recup,
                           primera=float(pr[:, 1].mean()) if len(pr) else float('nan'),
                           primera_lejos=float(pr[pr[:, 0] > 20, 1].mean()) if (len(pr) and (pr[:, 0] > 20).any()) else float('nan'),
                           dist_primera=float(np.median(pr[:, 0])) if len(pr) else float('nan'),
                           mem=int(br.memoria()), ops=br.ops / T, sabido_fin=float(sab),
                           pisadas=getattr(br, 'pisadas', 0), nac=getattr(br, 'nac', 0), mue=getattr(br, 'mue', 0),
                           liberadas=getattr(br, 'liberadas', 0))
    return dict(seed=seed, cal=cal, C=C, pan_base=a_base, pan_ctx=a_ctx, brazos=res)


BRAZOS = {
    'congelado': lambda tr, C, s: Brazo(tr, C, s),
    'ventana': lambda tr, C, s: Ventana(tr, C, s),
    'rag': lambda tr, C, s: RAG(tr, C, s),
    'hamburguesa': lambda tr, C, s: Hamburguesa(tr, C, s),
    'h_barajada': lambda tr, C, s: Hamburguesa(tr, C, s, barajar=True),
    'h_sin_compuerta': lambda tr, C, s: Hamburguesa(tr, C, s, compuerta=False),
    'h_dos_capas': lambda tr, C, s: Hamburguesa(tr, C, s, capa='ambas'),
    'h_capa1': lambda tr, C, s: Hamburguesa(tr, C, s, capa='x1'),
    'h_dos_capas_barajada': lambda tr, C, s: Hamburguesa(tr, C, s, capa='ambas', barajar=True),
    'h_dos_capas_sin_compuerta': lambda tr, C, s: Hamburguesa(tr, C, s, capa='ambas', compuerta=False),
    'techo_online': lambda tr, C, s: Techo(tr, C, s),
    'techo_online_fuerte': lambda tr, C, s: Techo(tr, C, s, lr=5e-3),
    'sueno': lambda tr, C, s: Sueno(tr, C, s),
    'sueno_sin_ensayo': lambda tr, C, s: Sueno(tr, C, s, ensayo=False),
}


def mr(v):
    v = [x for x in v if x is not None and not (isinstance(x, float) and np.isnan(x))]
    if not v: return 'nunca'
    return f"{np.median(v):.2f} [{min(v):.2f}-{max(v):.2f}]" if isinstance(v[0], float) else f"{int(np.median(v))} [{min(v)}-{max(v)}]"


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--semillas', type=int, default=8); ap.add_argument('--out', default='datos/h.json')
    ap.add_argument('--cal', default='tandas,regla,deriva_zipf'); ap.add_argument('--C', default='32,6')
    ap.add_argument('--brazos', default=','.join(BRAZOS)); ap.add_argument('--T', type=int, default=1500)
    ap.add_argument('--humo', action='store_true'); ap.add_argument('--theta', type=float, default=0.9)
    a = ap.parse_args(); THETA = a.theta
    if a.humo:
        print('gradiente: error relativo peor =', comprueba_gradiente()); t0 = time.time()
        tr, base, ab, ac = preentrena(1); print(f'pan: base {ab:.2f} ctx {ac:.2f} en {time.time()-t0:.0f}s'); sys.exit()
    brazos = {k: BRAZOS[k] for k in a.brazos.split(',')}
    todo = []; t0 = time.time()
    for cal in a.cal.split(','):
        for C in [int(c) for c in a.C.split(',')]:
            for s in range(1, a.semillas + 1):
                r = corre(s, cal, C, brazos, T=a.T); todo.append(r)
                print(f"{cal} C={C} s={s} pan {r['pan_base']:.2f}/{r['pan_ctx']:.2f} " +
                      ' '.join(f"{k}:{v['camb']:.2f}/{v['nocamb']:.2f}" for k, v in r['brazos'].items()) + f" [{time.time()-t0:.0f}s]", flush=True)
                json.dump(todo, open(a.out, 'w'))
    # tablas
    lineas = []
    for cal in a.cal.split(','):
        for C in [int(c) for c in a.C.split(',')]:
            rs = [r for r in todo if r['cal'] == cal and r['C'] == C]
            lineas.append(f"\n## {cal} C={C} (n={len(rs)}; pan base {mr([r['pan_base'] for r in rs])}, ctx {mr([r['pan_ctx'] for r in rs])})")
            lineas.append('| brazo | cambiados | no cambiados | 1a consulta tras exposicion unica (>20 seq. despues) | vecinas (parafrasis nueva) | sabido al final | recuperar 0.9 por evento | mem | ops/consulta | pisadas/nac/mue/lib |')
            lineas.append('|---|---|---|---|---|---|---|---|---|---|')
            for b in brazos:
                v = [r['brazos'][b] for r in rs]
                evs = sorted(v[0]['recup'].keys(), key=int)
                rec = ' / '.join(mr([x['recup'][e] for x in v]) for e in evs)
                lineas.append(f"| {b} | {mr([x['camb'] for x in v])} | {mr([x['nocamb'] for x in v])} | {mr([x['primera_lejos'] for x in v])} | {mr([x['vecina'] for x in v])} | {mr([x['sabido_fin'] for x in v])} | {rec} | {mr([x['mem'] for x in v])} | {int(np.median([x['ops'] for x in v]))} | {int(np.median([x['pisadas'] for x in v]))}/{int(np.median([x['nac'] for x in v]))}/{int(np.median([x['mue'] for x in v]))}/{int(np.median([x['liberadas'] for x in v]))} |")
    txt = '\n'.join(lineas); print(txt); open(a.out.replace('.json', '.txt'), 'w', encoding='utf-8').write(txt)
    print(f'CPU total {time.time()-t0:.0f}s')
