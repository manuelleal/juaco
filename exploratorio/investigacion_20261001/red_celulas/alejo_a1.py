"""alejo_a1.py — Perspectiva A (Alejo): bloque de celulas pegado a un modelo CONGELADO para corregir hechos que cambian.
Version minima sin LLM (1-oct-2026, exploracion, sin preregistro). MISION: llegar a la AGI por este camino.

MUNDO: 100 hechos clave -> valor (7 valores). La clave es un vector en R^16 (el "estado" que regala el modelo congelado).
Cada consulta llega como PARAFRASIS: clave + ruido N(0, sq). Tras cada consulta llega el valor correcto (el conjunto solo se
entera por su propio acierto/fallo). Calendarios: 'tandas' (t=0 cambian 30 hechos; t=1500 cambian otros 30; t=3000 los 30
primeros VUELVEN al valor original) y 'deriva' (cada 300 consultas cambian 5 hechos al azar, acumulativo).

MODELO CONGELADO: MLP (16-64-7) entrenado con Adam + entropia cruzada sobre los 100 hechos originales con parafrasis hasta
acierto >= 0.98 en parafrasis nuevas (paso 0 de cordura); despues NO se toca.

BRAZOS (todos reciben la misma consulta, responden, y luego ven el valor correcto):
 1 congelado solo.
 2 congelado + DICCIONARIO a mano: sabe el id exacto del hecho (oraculo de identidad); cuando falla guarda id -> valor; capacidad C (LRU).
 3 congelado + kNN a mano sobre el vector: guarda (consulta, valor) cuando el conjunto falla; responde con el vecino mas cercano
   si esta a distancia < r; capacidad C (saca el mas viejo).
 4 congelado + BLOQUE DE CELULAS: cada celula = prototipo (R^16), valor (7), energia. Compuerta por estado propio (PISA): una
   celula PISA la respuesta del congelado solo si la consulta se le parece (s > theta) Y su valor difiere del congelado Y ha
   cobrado antes (confianza > 0). Cobra (energia) SOLO cuando piso y acerto donde el congelado fallaba (su correccion valio).
   Paga por existir. E < 0 -> muere (olvido por escasez). Fallo sin celula que pise -> nace una celula en la consulta (si no hay
   cupo, muere la de menor energia). Celula que piso y fallo -> mueve su valor al correcto y su prototipo hacia la consulta
   (reglas locales). Pago por CAMINO chico: las celulas que se activaron juntas comparten el pago.
 5 bloque con aviso BARAJADO: el pago/castigo cae en una celula al azar (control).
 6 TECHO: reentrenar el modelo con gradiente en linea (Adam) con cada consulta; se cuenta su costo.
MEDIDAS: acierto en hechos cambiados y no cambiados (parafrasis nuevas) cada 50 consultas; consultas hasta recuperar 0.9 en
cambiados tras cada tanda; memoria usada (entradas/celulas); operaciones por consulta.
"""
import numpy as np, json, time, argparse, os
from red2 import MLP2

D, K, NH = 16, 7, 100


class Mundo:
    def __init__(self, seed, sq=0.1, calendario='tandas'):   # sq 0.35 tapaba la clave (paso 0: 0.25); con 0.1 norma del ruido 0.4
        self.rng = np.random.default_rng(seed); self.sq = sq
        self.claves = self.rng.normal(0, 1, (NH, D)); self.claves /= np.linalg.norm(self.claves, axis=1, keepdims=True)
        self.v0 = self.rng.integers(0, K, NH); self.v = self.v0.copy(); self.cambiados = np.zeros(NH, bool)
        self.calendario = calendario; self.tanda1 = None; self.tanda2 = None; self.eventos = []
        # frecuencia de consulta: uniforme, o Zipf (unos hechos se preguntan mucho mas que otros) si el calendario lo pide
        p = 1.0 / (1 + np.arange(NH)) if calendario.endswith('zipf') else np.ones(NH)
        self.p = self.rng.permutation(p / p.sum())

    def siguiente(self, rng_q): return int(rng_q.choice(NH, p=self.p))

    def consulta(self, i): return self.claves[i] + self.rng.normal(0, self.sq, D)

    def cambia(self, idx):
        for i in idx:
            nuevo = (self.v[i] + self.rng.integers(1, K)) % K; self.v[i] = nuevo
        self.cambiados[idx] = self.v[idx] != self.v0[idx]

    def evento(self, t):
        """devuelve True si en t hay un cambio (para medir recuperacion)."""
        if self.calendario == 'tandas':
            if t == 0:
                self.tanda1 = self.rng.choice(NH, 30, replace=False); self.cambia(self.tanda1); return 'tanda1'
            if t == 1500:
                resto = np.setdiff1d(np.arange(NH), self.tanda1); self.tanda2 = self.rng.choice(resto, 30, replace=False)
                self.cambia(self.tanda2); return 'tanda2'
            if t == 3000:
                self.v[self.tanda1] = self.v0[self.tanda1]; self.cambiados[self.tanda1] = False; return 'vuelta'
        else:
            if t % 300 == 0: self.cambia(self.rng.choice(NH, 5, replace=False)); return f'deriva{t}'
        return None


# ----------------------------------------------------------------------------------------------- brazos
class Congelado:
    def __init__(self, mlp): self.mlp = mlp; self.ops = 0; self.mem = 0
    def logits(self, x):
        self.ops += 2 * (D * 64 + 64 * K); return self.mlp._fwd(x)[-1]
    def responde(self, x, i): return int(np.argmax(self.logits(x)))
    def aprende(self, x, i, c, r): pass
    def memoria(self): return 0


class Diccionario(Congelado):
    def __init__(self, mlp, C): super().__init__(mlp); self.C = C; self.d = {}; self.orden = []
    def responde(self, x, i):
        if i in self.d: self.ops += 1; return self.d[i]
        return int(np.argmax(self.logits(x)))
    def aprende(self, x, i, c, r):
        if r != c:
            if i not in self.d and len(self.d) >= self.C: viejo = self.orden.pop(0); del self.d[viejo]
            if i in self.d: self.orden.remove(i)
            self.d[i] = c; self.orden.append(i)
    def memoria(self): return len(self.d)


class KNN(Congelado):
    def __init__(self, mlp, C, radio=1.0): super().__init__(mlp); self.C = C; self.X = np.zeros((0, D)); self.y = np.zeros(0, int); self.radio = radio
    def responde(self, x, i):
        if len(self.y):
            d = np.linalg.norm(self.X - x, axis=1); j = int(np.argmin(d)); self.ops += 3 * self.X.size
            if d[j] < self.radio: return int(self.y[j])
        return int(np.argmax(self.logits(x)))
    def aprende(self, x, i, c, r):
        if r != c:
            self.X = np.vstack([self.X, x]); self.y = np.append(self.y, c)
            if len(self.y) > self.C: self.X = self.X[1:]; self.y = self.y[1:]
    def memoria(self): return len(self.y)


class Bloque(Congelado):
    """bloque de celulas con compuerta por estado propio, olvido por escasez y pago por camino chico."""
    def __init__(self, mlp, C, seed, theta=0.6, sigma=0.7, c_exist=0.002, pago=1.0, castigo=0.5, eta=0.3, barajar=False, camino=True, E0=1.0):
        super().__init__(mlp); self.C = C; self.rng = np.random.default_rng(seed + 777)
        self.W = np.zeros((0, D)); self.V = np.zeros((0, K)); self.E = np.zeros(0); self.conf = np.zeros(0)
        self.theta, self.sigma, self.c_exist, self.pago, self.castigo, self.eta = theta, sigma, c_exist, pago, castigo, eta
        self.barajar, self.camino, self.E0 = barajar, camino, E0; self.nac = 0; self.mue = 0; self.pisadas = 0
        self._ult = None

    @property
    def N(self): return self.W.shape[0]

    def responde(self, x, i):
        yf = int(np.argmax(self.logits(x)))
        act = np.zeros(0, bool); vals = None
        if self.N:
            s = np.exp(-np.sum((self.W - x) ** 2, axis=1) / (2 * self.sigma ** 2)); self.ops += 4 * self.W.size
            vals = np.argmax(self.V, axis=1)
            # COMPUERTA (regla local de cada celula): me parece, difiero del congelado y ya cobre antes
            act = (s > self.theta) & (vals != yf) & (self.conf > 0)
            cand = (s > self.theta)       # celulas que "oyeron" la consulta (camino), cobren o no
        else:
            cand = act
        if act.any():
            j = int(np.argmax(np.where(act, s, -1))); r = int(vals[j]); self.pisadas += 1
        else:
            j = -1; r = yf
        self._ult = (x, yf, act, cand, j, r)
        return r

    def aprende(self, x, i, c, r):
        x, yf, act, cand, j, r = self._ult
        if self.N:
            self.E -= self.c_exist                                   # existir cuesta
            # pago/castigo a la celula que piso (o a una al azar: control barajado)
            if j >= 0:
                k = j if not self.barajar else int(self.rng.integers(self.N))
                if r == c and yf != c:                               # mi correccion valio: cobro
                    if self.camino and cand.any():
                        grupo = np.where(cand)[0]
                        if self.barajar: grupo = self.rng.choice(self.N, len(grupo), replace=False)
                        self.E[grupo] += self.pago / len(grupo); self.conf[grupo] += 1.0 / len(grupo)
                    else:
                        self.E[k] += self.pago; self.conf[k] += 1
                    self.W[k] += 0.2 * (x - self.W[k])               # afino el prototipo con lo que acerte (Hebb local)
                elif r != c and yf == c:                             # pise donde el congelado ACERTABA: lo que yo decia ya no vale
                    self.conf[k] = 0.0; self.E[k] = -1.0             # SUELTO la correccion (PISA) y muero ya: libero el cupo
                elif r != c:                                         # pise y fallamos los dos: el hecho volvio a cambiar -> corrijo mi valor
                    self.E[k] -= self.castigo * 0.5
                    self.V[k] += self.eta * (np.eye(K)[c] - self.V[k]); self.W[k] += self.eta * (x - self.W[k])
            # las que oyeron pero no cobraron y cuyo valor coincide con el congelado: no sirven (su correccion ya no vale)
            # -> no cobran nunca, mueren solas por existir. (Asi SUELTAN la correccion cuando el hecho vuelve.)
            muertas = self.E < 0
            if muertas.any():
                self.mue += int(muertas.sum()); viva = ~muertas
                self.W, self.V, self.E, self.conf = self.W[viva], self.V[viva], self.E[viva], self.conf[viva]
        if r != c and j < 0 and yf != c:                             # nadie piso y el congelado fallo: nace una celula aqui
            if self.N >= self.C:
                peor = int(np.argmin(self.E)); viva = np.ones(self.N, bool); viva[peor] = False; self.mue += 1
                self.W, self.V, self.E, self.conf = self.W[viva], self.V[viva], self.E[viva], self.conf[viva]
            self.W = np.vstack([self.W, x]); self.V = np.vstack([self.V, np.eye(K)[c]])
            self.E = np.append(self.E, self.E0); self.conf = np.append(self.conf, 1.0); self.nac += 1
        elif r != c and j < 0 and yf == c:
            pass
    def memoria(self): return self.N


class Techo(Congelado):
    """reentrena el modelo en linea con gradiente (Adam): lo que el bloque pretende evitar."""
    def __init__(self, mlp, lr=0.003):
        import copy; super().__init__(copy.deepcopy(mlp)); self.mlp.lr = lr
    def aprende(self, x, i, c, r): self.mlp.expone(x, c); self.ops += self.mlp.ops; self.mlp.ops = 0
    def memoria(self): return 0


# ----------------------------------------------------------------------------------------------- flujo
def entrena_congelado(mundo, seed):
    mlp = MLP2(seed, D, K, capas=(64,), lr=0.003); rng = np.random.default_rng(seed + 99)
    for k in range(40000):                                   # 6 000 pasos daban 0.45; 20 000 a 0.003 dan 0.957
        if k == 30000: mlp.lr = 0.001
        i = rng.integers(NH); mlp.expone(mundo.consulta(i), mundo.v0[i])
    acc = np.mean([mlp.predice(mundo.consulta(i)) == mundo.v0[i] for i in range(NH) for _ in range(3)])
    mlp.ops = 0
    return mlp, float(acc)


def evalua(brazo, mundo, rng_ev):
    """acierto ponderado por la frecuencia de consulta (con uniforme es la media simple)."""
    ok = np.zeros(NH, bool)
    for i in range(NH):
        x = mundo.claves[i] + rng_ev.normal(0, mundo.sq, D)
        ok[i] = brazo.responde(x, i) == mundo.v[i]
    brazo._ult = None
    camb = mundo.cambiados; p = mundo.p
    ac = float((ok[camb] * p[camb]).sum() / p[camb].sum()) if camb.any() else float('nan')
    return ac, float((ok[~camb] * p[~camb]).sum() / p[~camb].sum())


def corre(seed, calendario, C, T=4500, cada=50):
    mundo = Mundo(seed, calendario=calendario); mlp, acc0 = entrena_congelado(mundo, seed)
    brazos = {'1 congelado': Congelado(mlp), '2 diccionario': Diccionario(mlp, C), '3 kNN': KNN(mlp, C),
              '4 bloque celulas': Bloque(mlp, C, seed), '5 bloque barajado': Bloque(mlp, C, seed, barajar=True),
              '6 techo reentrena': Techo(mlp)}
    rng_q = np.random.default_rng(seed + 5); res = {b: dict(t=[], camb=[], nocamb=[], mem=[], ev={}) for b in brazos}
    ult_evento = {b: None for b in brazos}; pend = {}
    for t in range(T):
        e = mundo.evento(t)
        if e:
            for b in brazos: pend[(b, e)] = t
        i = mundo.siguiente(rng_q); x = mundo.consulta(i); c = int(mundo.v[i])
        for b, br in brazos.items():
            r = br.responde(x, i); br.aprende(x, i, c, r)
        if (t + 1) % cada == 0:
            for b, br in brazos.items():
                ac, an = evalua(br, mundo, np.random.default_rng(seed * 1000 + t))
                res[b]['t'].append(t + 1); res[b]['camb'].append(ac); res[b]['nocamb'].append(an); res[b]['mem'].append(br.memoria())
                for (bb, ee), t0 in list(pend.items()):
                    if bb == b and ac >= 0.9: res[b]['ev'][ee] = t + 1 - t0; del pend[(bb, ee)]
    for b, br in brazos.items():
        res[b]['ops'] = br.ops / T; res[b]['acc0'] = acc0
        res[b]['final_camb'] = res[b]['camb'][-1]; res[b]['final_nocamb'] = res[b]['nocamb'][-1]
        res[b]['media_camb'] = float(np.nanmean(res[b]['camb'])); res[b]['media_nocamb'] = float(np.mean(res[b]['nocamb']))
        res[b]['mem_fin'] = res[b]['mem'][-1]
        if isinstance(br, Bloque): res[b]['nac'] = br.nac; res[b]['mue'] = br.mue; res[b]['pisadas'] = br.pisadas
    return res


def mr(v):
    v = [x for x in v if x is not None and not (isinstance(x, float) and np.isnan(x))]
    if not v: return 'nunca'
    return f"{np.median(v):.2f} [{min(v):.2f}-{max(v):.2f}]" if isinstance(v[0], float) else f"{int(np.median(v))} [{min(v)}-{max(v)}]"


if __name__ == '__main__':
    ap = argparse.ArgumentParser(); ap.add_argument('--semillas', type=int, default=10); ap.add_argument('--out', default='datos/a1.json')
    args = ap.parse_args(); todo = {}; t0 = time.time()
    for calendario in ('tandas', 'deriva', 'deriva_zipf'):
        for C in (100, 15):
            rs = [corre(s, calendario, C) for s in range(1, args.semillas + 1)]
            todo[f'{calendario}_C{C}'] = rs
            print(f"\n## calendario {calendario}, capacidad C={C} ({args.semillas} semillas; congelado paso 0: acierto {mr([r['1 congelado']['acc0'] for r in rs])})")
            print("| brazo | cambiados (media en el tiempo) | cambiados (final) | NO cambiados (media) | NO cambiados (final) | hasta 0.9 tras tanda1 | tras tanda2 | tras vuelta | memoria fin | ops/consulta |")
            print("|---|---|---|---|---|---|---|---|---|---|")
            for b in rs[0]:
                evs = [k for k in ('tanda1', 'tanda2', 'vuelta')] if calendario == 'tandas' else []
                col_ev = " | ".join(f"{mr([r[b]['ev'].get(e) for r in rs])} ({sum(e in r[b]['ev'] for r in rs)}/{len(rs)})" for e in evs) if evs else " — | — | — "
                print(f"| {b} | {mr([r[b]['media_camb'] for r in rs])} | {mr([r[b]['final_camb'] for r in rs])} | {mr([r[b]['media_nocamb'] for r in rs])} | {mr([r[b]['final_nocamb'] for r in rs])} | {col_ev} | {mr([r[b]['mem_fin'] for r in rs])} | {int(np.median([r[b]['ops'] for r in rs]))} |")
            os.makedirs('datos', exist_ok=True); json.dump(todo, open(args.out, 'w'))
    print(f"({time.time()-t0:.0f} s)")
