# EXPLORATORIO, no es dato
"""cadena.py — cadena trófica de 4 especies con cintas genéticas que evolucionan y cerebros que aprenden en vida (explorador Fable, 25-sep-2026).

MISION: llegar a la AGI por este camino (organismo mínimo con reglas locales, sin retropropagación); el método manda sobre el cómo.

Idea del director: cuatro roles en cadena. GUSANO (nivel 0) no come a nadie; GALLINA (1) come gusanos; OSO (2) come gallinas; HUMANO (3)
come osos. Nadie come otro nivel. No hay comida en el mundo: el gusano recibe una entrada fija de energía por paso ("sol", logístico con
su propia densidad) porque sin ninguna entrada la termodinámica mata a todos (cada paso cuesta energía y nada la produce).

Qué tomé de nuestro bicho (motor_codigo / codigo_def):
  - la CINTA: tuplas (OP, args) en un lenguaje cerrado (SUM j d | REP n | FIN | TASA r); el LECTOR la interpreta al nacer sumando en
    espacio log sobre rasgos; el COPIADOR la copia con errores (cambio 0.55 / borrado 0.20 / inserción 0.15 / duplicación en tándem 0.10)
    con tasa por zona (TASA). Sin eval/exec. rng propio por parto.
  - el CEREBRO: valencia aprendida por SEÑAL de la presa (4 bins de la señal de veneno, ruidosa) con regla delta V += eta*(dE - V),
    aversión (peso mayor si dE < 0) y hambre_boca (cuanta hambre hace falta para morder lo que sabe malo). Sin retropropagación.
  - sin vivero, sin juez: el que muere, muere; el que llega a REP pare y paga la dote.

RASGOS (x en espacio log/aditivo, arrancan en 0; PASO 0.15 por unidad de d):
  0 veneno  = max(0, x0)            (lo que dejas en quien te come)
  1 escudo  = max(0, x1)            (resistencia al veneno de tu presa)
  2 velocidad = V0_s * exp(x2)
  3 vista   = VISTA0_s * exp(x3)
  4 tamaño  = exp(x4)               (más energía por bocado, más costo)
  5 eta     = 0.3 * exp(x5)         (cuánto aprende)
  6 hambre  = exp(x6)               (hambre_boca)
  7 huida   = exp(x7)               (peso de huir del depredador visible)
"""
import argparse, json, os, sys, time
import numpy as np

NOMBRES = ('gusano', 'gallina', 'oso', 'humano')
N_RASGOS = 8
PASO = 0.15
OPS = ('SUM', 'REP', 'FIN', 'TASA')
TASAS = (0.0, 0.003, 0.01, 0.03, 0.1)
TASA_DEF = 2
TOPE_CINTA = 60
P_TIPO = (0.55, 0.75, 0.90)

# ------------------------------------------------ parámetros del mundo (calibrados a mano en el humo; ver HALLAZGOS)
L = 80.0
R_EAT = 0.9
P_CAPTURA = 0.5                          # probabilidad de que un bocado a distancia de mordida se consume
N0 = (600, 80, 10, 3)
NMAX = (1500, 400, 120, 40)
V0 = (0.25, 0.6, 0.65, 0.7)
VISTA0 = (1.5, 4.0, 8.0, 12.0)
BASE = (0.05, 0.04, 0.05, 0.06)        # costo metabólico base por paso
BOC = (0.0, 2.5, 5.0, 10.0)             # energía por bocado (× tamaño)
REP = (3.0, 8.0, 20.0, 40.0)            # umbral para parir
DOTE = (1.5, 4.0, 8.0, 16.0)            # lo que se le da al hijo
MAXAGE = (500, 800, 1200, 1600)
SOL = 0.5
K_SOL = 400.0
DANO = 1.5                               # daño por unidad de (veneno − escudo)
COSTO = dict(veneno=0.03, escudo=0.03, vel=0.04, vista=0.006, tam=0.03)
SIG_SENAL = 0.25
BINS = np.array([0.2, 0.5, 1.0])
AVERSION = 2.0
DIGESTION = (0, 10, 20, 40)             # pasos sin poder comer después de un bocado (tiempo de manejo: amortigua el boom)
SACIEDAD = 0.85                          # nadie caza con E > SACIEDAD*REP (un bocado basta para cruzar REP)


def cinta0():
    return tuple(('SUM', j, 0) for j in range(N_RASGOS)) + (('TASA', TASA_DEF),)


def _instr_azar(rng):
    op = OPS[rng.integers(len(OPS))]
    if op == 'SUM': return ('SUM', int(rng.integers(N_RASGOS)), int(rng.integers(-2, 3)))
    if op == 'REP': return ('REP', int(rng.integers(1, 4)))
    if op == 'FIN': return ('FIN',)
    return ('TASA', int(rng.integers(len(TASAS))))


def copia(cinta, rng, evo):
    """Copia con errores; la tasa por instrucción la dicta la última TASA leída linealmente. evo=0: copia perfecta."""
    if not evo: return cinta
    zona = TASA_DEF; out = []; i = 0; n = len(cinta)
    while i < n:
        ins = cinta[i]
        if ins[0] == 'TASA': zona = ins[1]
        p = TASAS[zona]
        u = rng.random()
        if u >= p:
            out.append(ins); i += 1; continue
        t = rng.random()
        if t < P_TIPO[0]:                       # cambio
            if rng.random() < 0.3: out.append(_instr_azar(rng))
            else:
                if ins[0] == 'SUM':
                    if rng.random() < 0.5: out.append(('SUM', ins[1], int(np.clip(ins[2] + rng.choice((-1, 1)), -3, 3))))
                    else: out.append(('SUM', int(rng.integers(N_RASGOS)), ins[2]))
                elif ins[0] == 'REP': out.append(('REP', int(rng.integers(1, 4))))
                elif ins[0] == 'TASA': out.append(('TASA', int(rng.integers(len(TASAS)))))
                else: out.append(ins)
            i += 1
        elif t < P_TIPO[1]:                     # borrado
            i += 1
        elif t < P_TIPO[2]:                     # inserción
            out.append(ins); out.append(_instr_azar(rng)); i += 1
        else:                                   # duplicación en tándem
            k = int(rng.integers(1, 5)); tramo = cinta[i:i + k]
            out.extend(tramo); out.extend(tramo); i += k
    return tuple(out[:TOPE_CINTA])


def desarrolla(cinta):
    """Lector: SUM j d suma d*PASO en x[j]; REP n ... FIN repite. Tope de pasos por seguridad."""
    x = np.zeros(N_RASGOS)
    pila = []; i = 0; pasos = 0; n = len(cinta)
    # ejecución lineal con pila de (indice_inicio, repeticiones_restantes)
    while i < n and pasos < 600:
        pasos += 1
        ins = cinta[i]
        if ins[0] == 'SUM':
            x[ins[1]] += ins[2] * PASO
        elif ins[0] == 'REP':
            pila.append([i, ins[1] - 1])
        elif ins[0] == 'FIN':
            if pila:
                if pila[-1][1] > 0: pila[-1][1] -= 1; i = pila[-1][0]
                else: pila.pop()
        i += 1
    return x


def fenotipo(X, s, veneno_ok):
    """X (N,8) → dict de arrays de rasgos."""
    f = {}
    f['veneno'] = np.maximum(0.0, X[:, 0]) if veneno_ok else np.zeros(len(X))
    f['escudo'] = np.maximum(0.0, X[:, 1])
    f['vel'] = np.clip(V0[s] * np.exp(X[:, 2]), 0.05, 3.0)
    f['vista'] = np.clip(VISTA0[s] * np.exp(X[:, 3]), 0.3, 20.0)
    f['tam'] = np.clip(np.exp(X[:, 4]), 0.25, 4.0)
    f['eta'] = np.clip(0.3 * np.exp(X[:, 5]), 0.01, 1.0)
    f['hambre'] = np.clip(np.exp(X[:, 6]), 0.05, 10.0)
    f['huida'] = np.clip(np.exp(X[:, 7]), 0.0, 10.0)
    return f


def costo(f, s):
    return (BASE[s] + COSTO['veneno'] * f['veneno'] + COSTO['escudo'] * f['escudo'] + COSTO['vel'] * f['vel'] ** 2
            + COSTO['vista'] * f['vista'] + COSTO['tam'] * f['tam'])


class Especie:
    def __init__(self, s, n, rng, evo, veneno_ok):
        self.s = s; self.evo = evo; self.veneno_ok = veneno_ok and (s < 3)   # el humano no necesita veneno: nadie lo come
        self.pos = rng.random((n, 2)) * L
        self.E = np.full(n, 0.7 * float(REP[s]))
        self.age = rng.integers(0, MAXAGE[s] // 2, n)
        self.cintas = [cinta0() for _ in range(n)]
        self.X = np.zeros((n, N_RASGOS))
        self.gen = np.zeros(n, dtype=np.int64)
        self.V = np.zeros((n, len(BINS) + 1))      # valencias aprendidas por bin de señal de la presa
        self.dig = np.zeros(n, dtype=np.int64)
        self.f = fenotipo(self.X, s, self.veneno_ok)
        self.nac = 0; self.muertes_hambre = 0; self.muertes_comido = 0; self.muertes_vejez = 0; self.muertes_veneno = 0
        self.comidos_por_bin = np.zeros(len(BINS) + 1); self.vistos_por_bin = np.zeros(len(BINS) + 1)

    @property
    def n(self): return len(self.E)

    def filtra(self, keep):
        self.pos = self.pos[keep]; self.E = self.E[keep]; self.age = self.age[keep]; self.X = self.X[keep]
        self.gen = self.gen[keep]; self.V = self.V[keep]; self.dig = self.dig[keep]
        idx = np.nonzero(keep)[0]; self.cintas = [self.cintas[i] for i in idx]
        self.f = {k: v[keep] for k, v in self.f.items()}

    def agrega(self, pos, E, cintas, X, gen):
        m = len(E)
        if m == 0: return
        self.pos = np.vstack([self.pos, pos]); self.E = np.concatenate([self.E, E]); self.age = np.concatenate([self.age, np.zeros(m, dtype=np.int64)])
        self.X = np.vstack([self.X, X]); self.gen = np.concatenate([self.gen, gen]); self.V = np.vstack([self.V, np.zeros((m, len(BINS) + 1))])
        self.cintas.extend(cintas); self.dig = np.concatenate([self.dig, np.zeros(m, dtype=np.int64)])
        fn = fenotipo(X, self.s, self.veneno_ok)
        self.f = {k: np.concatenate([self.f[k], fn[k]]) for k in self.f}


def dist_toro(a, b):
    """dv (Na,Nb,2) = a - b en el toro; D (Na,Nb). Por eje y en float32: es el cuello de botella."""
    a32 = a.astype(np.float32); b32 = b.astype(np.float32); half = np.float32(L / 2); Lf = np.float32(L)
    dx = np.subtract.outer(a32[:, 0], b32[:, 0]); dx += half; np.mod(dx, Lf, out=dx); dx -= half
    dy = np.subtract.outer(a32[:, 1], b32[:, 1]); dy += half; np.mod(dy, Lf, out=dy); dy -= half
    D = np.hypot(dx, dy)
    return np.stack([dx, dy], -1), D


def paso(esp, rng, t):
    n_sp = len(esp)
    # ---------------- 1. movimiento
    nuevas_pos = []
    D_cache = {}   # par (s, s-1): (dv, D) del depredador s a la presa s-1; la presa lo reusa transpuesto
    for s in range(1, n_sp):
        if esp[s].n and esp[s - 1].n: D_cache[s] = dist_toro(esp[s].pos, esp[s - 1].pos)
    for s in range(n_sp):
        e = esp[s]
        if e.n == 0: nuevas_pos.append(e.pos); continue
        dirn = rng.normal(0, 0.4, (e.n, 2))
        # hacia la presa deseable más cercana
        if s > 0 and esp[s - 1].n > 0:
            p = esp[s - 1]
            dv, D = D_cache[s]
            senal = p.f['veneno'] + rng.normal(0, SIG_SENAL, p.n)
            binp = np.digitize(senal, BINS)                       # (Np,)
            val = e.V[:, binp]                                    # (Ne, Np)
            drive = (e.f['hambre'] * (1.0 - e.E / REP[s]))[:, None]
            desea = (D < e.f['vista'][:, None]) & (val + drive > 0) & ((e.E < SACIEDAD * REP[s]) & (e.dig <= 0))[:, None]
            Dm = np.where(desea, D, np.inf)
            j = Dm.argmin(1); hay = np.isfinite(Dm[np.arange(e.n), j])
            to = -dv[np.arange(e.n), j] / (D[np.arange(e.n), j][:, None] + 1e-9)   # dv = yo - presa: hacia la presa es -dv
            dirn += np.where(hay[:, None], to, 0.0) * 1.0
        # lejos del depredador visible más cercano
        if s < n_sp - 1 and esp[s + 1].n > 0:
            q = esp[s + 1]
            dvq, Dq = D_cache[s + 1]                 # (Nq, Ne): depredador - yo
            dv2 = -np.swapaxes(dvq, 0, 1); D2 = Dq.T # (Ne, Nq): yo - depredador
            D2m = np.where(D2 < e.f['vista'][:, None], D2, np.inf)
            j2 = D2m.argmin(1); hay2 = np.isfinite(D2m[np.arange(e.n), j2])
            away = dv2[np.arange(e.n), j2] / (D2[np.arange(e.n), j2][:, None] + 1e-9)   # dv2 = yo - depredador: lejos es +dv2
            dirn += np.where(hay2[:, None], away, 0.0) * e.f['huida'][:, None]
        nrm = np.sqrt((dirn ** 2).sum(1))[:, None] + 1e-9
        nuevas_pos.append((e.pos + e.f['vel'][:, None] * dirn / nrm) % L)
    for s in range(n_sp): esp[s].pos = nuevas_pos[s]

    # ---------------- 2. comer (de arriba hacia abajo: el humano come antes de que el oso se mueva a comer... orden fijo)
    comidos = [np.zeros(esp[s].n, dtype=bool) for s in range(n_sp)]
    for s in range(n_sp - 1, 0, -1):
        e = esp[s]; p = esp[s - 1]
        if e.n == 0 or p.n == 0: continue
        dv, D = dist_toro(e.pos, p.pos)
        D = np.where(comidos[s - 1][None, :], np.inf, D)
        j = D.argmin(1); alc = (D[np.arange(e.n), j] < R_EAT) & (rng.random(e.n) < P_CAPTURA) & (e.dig <= 0)
        # cada presa la come sólo el primer depredador que la alcanza
        idx_pred = np.nonzero(alc)[0]
        if len(idx_pred) == 0: continue
        presas = j[idx_pred]
        _, first = np.unique(presas, return_index=True)
        idx_pred = idx_pred[first]; presas = presas[first]
        gan = BOC[s] * (0.5 * e.f['tam'][idx_pred] + 0.5 * p.f['tam'][presas])
        dano = DANO * np.maximum(0.0, p.f['veneno'][presas] - e.f['escudo'][idx_pred])
        dE = gan - dano
        e.E[idx_pred] += dE; e.dig[idx_pred] = DIGESTION[s]
        # aprendizaje en vida (regla delta con aversión) sobre el bin de la señal de ESA presa
        senal = p.f['veneno'][presas] + rng.normal(0, SIG_SENAL, len(presas))
        b = np.digitize(senal, BINS)
        eta = e.f['eta'][idx_pred] * np.where(dE < 0, AVERSION, 1.0)
        e.V[idx_pred, b] += eta * (dE / BOC[s] - e.V[idx_pred, b])
        e.comidos_por_bin += np.bincount(b, minlength=len(BINS) + 1)
        comidos[s - 1][presas] = True
        p.muertes_comido += len(presas)
        e.muertes_veneno += int(((e.E[idx_pred] <= 0) & (dano > 0)).sum())

    # ---------------- 3. metabolismo, sol, edad, muertes
    for s in range(n_sp):
        e = esp[s]
        if e.n == 0: continue
        e.E -= costo(e.f, s)
        if s == 0: e.E += SOL / (1.0 + e.n / K_SOL)
        e.age += 1; e.dig -= 1
        hambre = e.E <= 0; vejez = e.age >= MAXAGE[s]
        e.muertes_hambre += int((hambre & ~comidos[s]).sum()); e.muertes_vejez += int((vejez & ~hambre & ~comidos[s]).sum())
        keep = ~(hambre | vejez | comidos[s])
        if not keep.all(): e.filtra(keep)

    # ---------------- 4. nacimientos
    for s in range(n_sp):
        e = esp[s]
        if e.n == 0: continue
        puede = e.E >= REP[s]
        cupo = NMAX[s] - e.n
        idx = np.nonzero(puede)[0]
        if len(idx) == 0 or cupo <= 0: continue
        if len(idx) > cupo: idx = rng.choice(idx, cupo, replace=False)
        e.E[idx] -= DOTE[s]
        cintas = [copia(e.cintas[i], rng, e.evo) for i in idx]
        X = np.array([desarrolla(c) for c in cintas]) if cintas else np.zeros((0, N_RASGOS))
        pos = (e.pos[idx] + rng.normal(0, 1.0, (len(idx), 2))) % L
        e.agrega(pos, np.full(len(idx), float(DOTE[s])), cintas, X, e.gen[idx] + 1)
        e.nac += len(idx)


def foto(esp):
    return [dict(n=NOMBRES[s], pos=np.round(esp[s].pos, 1).tolist(), veneno=np.round(esp[s].f['veneno'], 2).tolist()) for s in range(len(esp))]


def corre(seed, T, evo, veneno_ok, salida, cada=100, quiet=False):
    rng = np.random.default_rng([seed, 7, int(evo), int(veneno_ok)])
    esp = [Especie(s, N0[s], rng, evo, veneno_ok) for s in range(4)]
    serie = dict(t=[], pop=[[] for _ in range(4)], gen=[[] for _ in range(4)], rasgos={r: [[] for _ in range(4)] for r in ('veneno', 'escudo', 'vel', 'vista', 'tam', 'eta', 'hambre', 'huida')},
                 largo_cinta=[[] for _ in range(4)], V_media=[[] for _ in range(4)])
    fotos = {}; extincion = [None] * 4; t0 = time.time()
    t_fotos = {0, T // 8, T // 4, T // 2, T - 1}
    for t in range(T):
        if t in t_fotos: fotos[str(t)] = foto(esp)
        paso(esp, rng, t)
        for s in range(4):
            if extincion[s] is None and esp[s].n == 0: extincion[s] = t
        if t % cada == 0 or t == T - 1:
            serie['t'].append(t)
            for s in range(4):
                e = esp[s]; serie['pop'][s].append(e.n)
                serie['gen'][s].append(float(e.gen.mean()) if e.n else None)
                serie['largo_cinta'][s].append(float(np.mean([len(c) for c in e.cintas])) if e.n else None)
                serie['V_media'][s].append(np.round(e.V.mean(0), 3).tolist() if e.n else None)
                for r in serie['rasgos']: serie['rasgos'][r][s].append(float(e.f[r].mean()) if e.n else None)
            if not quiet and t % (cada * 20) == 0:
                print(f"t={t:6d} pops={[e.n for e in esp]} gen_gusano={serie['gen'][0][-1]} ven_g={serie['rasgos']['veneno'][0][-1]:.2f} esc_ga={serie['rasgos']['escudo'][1][-1] if esp[1].n else None} {time.time()-t0:.0f}s", flush=True)
        if all(e.n == 0 for e in esp): break
    res = dict(EXPLORATORIO='no es dato', seed=seed, T=T, evo=evo, veneno_ok=veneno_ok, extincion=extincion, serie=serie, fotos=fotos,
               finales={NOMBRES[s]: dict(n=esp[s].n, nac=esp[s].nac, gen_max=int(esp[s].gen.max()) if esp[s].n else None,
                                        muertes=dict(hambre=esp[s].muertes_hambre, comido=esp[s].muertes_comido, vejez=esp[s].muertes_vejez, por_veneno_al_comer=esp[s].muertes_veneno),
                                        comidos_por_bin=esp[s].comidos_por_bin.tolist(),
                                        cintas_ejemplo=[list(map(list, c)) for c in esp[s].cintas[:3]]) for s in range(4)},
               segundos=time.time() - t0, params=dict(L=L, N0=N0, NMAX=NMAX, V0=V0, VISTA0=VISTA0, BASE=BASE, BOC=BOC, REP=REP, DOTE=DOTE, MAXAGE=MAXAGE, SOL=SOL, K_SOL=K_SOL, DANO=DANO, COSTO=COSTO, TASAS=TASAS))
    os.makedirs(os.path.dirname(salida) or '.', exist_ok=True)
    with open(salida, 'w', encoding='utf-8') as fh: json.dump(res, fh)
    print(f"FIN seed={seed} evo={evo} veneno={veneno_ok} extincion={extincion} pops={[e.n for e in esp]} {time.time()-t0:.0f}s -> {salida}")
    return res


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--seed', type=int, default=32001)
    ap.add_argument('--T', type=int, default=12000)
    ap.add_argument('--evo', type=int, default=1)
    ap.add_argument('--veneno', type=int, default=1)
    ap.add_argument('--out', default=None)
    ap.add_argument('--cada', type=int, default=100)
    ap.add_argument('--set', action='append', default=[], help='PARAM=valor (literal python, sin eval: json) para calibrar; p. ej. --set SOL=0.3 --set "REP=[3,8,14,26]"')
    a = ap.parse_args()
    for kv in a.set:
        k, v = kv.split('=', 1); v = json.loads(v)
        if isinstance(globals()[k], tuple): v = tuple(float(x) for x in v)
        globals()[k] = v; print('SET', k, v)
    brazo = 'EVO' if a.evo and a.veneno else ('FIJO' if not a.evo else 'SINVENENO')
    out = a.out or os.path.join(os.path.dirname(os.path.abspath(__file__)), 'datos', f'{brazo}_{a.seed}.json')
    corre(a.seed, a.T, bool(a.evo), bool(a.veneno), out, cada=a.cada)
