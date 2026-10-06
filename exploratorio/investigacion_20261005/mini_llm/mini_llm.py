"""
MINI-LLM CON COLONIA VIVA (5-oct-2026, exploracion sin preregistro formal; predicciones en PREDICCIONES.md).
BASE   = modelo de lenguaje por caracteres (transformador 2 bloques, dim 48, contexto 48) entrenado con
         retropropagacion a mano en numpy puro sobre los .md del proyecto (espanol) y luego CONGELADO.
COLONIA = celulas de memoria viva (reglas JUACO: clave = estado interno de la base, valor = correccion de la
         siguiente letra; compuerta por parecido; cobra si su correccion acerto donde la base fallaba; paga por
         existir; sin cupo muere la mas pobre; suelta la correccion si pisa donde la base ya acierta).
MAESTROS = flujos de texto NUEVO que la base nunca vio: codigo Python del repo, un idioma inventado por reglas,
         hechos "la clave de X es D" que cambian y vuelven, un maestro mentiroso y ruido. Llegan uno tras otro
         y a veces dos a la vez.
RIVALES = base sola; base + gradiente en linea; base + kNN-LM (misma memoria, sin compuerta ni energia);
         colonia barajada; colonia sin compuerta; colonia + SUENO (la base absorbe con gradiente lo que saben
         las celulas y las libera).
"""
import numpy as np, os, json, time, glob, re, argparse, sys, unicodedata

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.abspath(os.path.join(AQUI, '..', '..'))          # PROYECTOS\JUACO
D, H, DF, NB, L = 48, 4, 192, 2, 48
DH = D // H
STRIDE = 16                                                      # cada ventana de 48 predice sus ultimas 16 letras
PERM = "abcdefghijklmnopqrstuvwxyzáéíóúñü0123456789 \n.,;:()[]{}<>=+-*/_|#'\"?¿!¡%&@\\^~`$"
ESPANOL_PROBE = 400
ESP = PERM.index(' ')


# ================================================================ corpus
def limpia(t):
    t = unicodedata.normalize('NFC', t).lower()
    t = t.replace('\r', '').replace('\t', ' ')
    t = re.sub(r'[ ]{2,}', ' ', t); t = re.sub(r'\n{2,}', '\n', t)
    return ''.join(c for c in t if c in PERM)


def carga_corpus():
    f = os.path.join(AQUI, 'datos', 'corpus.json')
    if os.path.exists(f):
        return json.load(open(f, encoding='utf-8'))
    pats = ['organelos/registro/*.md', 'organelos/exploratorio/**/*.md', 'organelos/*.md', 'bundle/**/*.md']
    files = sorted(set(p for pat in pats for p in glob.glob(os.path.join(RAIZ, pat), recursive=True)))
    files = [p for p in files if 'mini_llm' not in p]
    tr, va = [], []
    for i, p in enumerate(files):
        try: t = limpia(open(p, encoding='utf-8', errors='ignore').read())
        except Exception: continue
        (va if i % 10 == 3 else tr).append(t)
    cod = []
    for p in sorted(glob.glob(os.path.join(RAIZ, 'bundle', '**', '*.py'), recursive=True))[:60]:
        cod.append(limpia(open(p, encoding='utf-8', errors='ignore').read()))
    c = dict(train='\n'.join(tr), val='\n'.join(va), codigo='\n'.join(cod), n_files=len(files))
    json.dump(c, open(f, 'w', encoding='utf-8'))
    return c


class Voc:
    def __init__(self):
        self.chars = PERM; self.V = len(PERM); self.idx = {c: i for i, c in enumerate(PERM)}
    def codifica(self, t): return np.array([self.idx[c] for c in t if c in self.idx], np.int64)
    def decodifica(self, a): return ''.join(self.chars[i] for i in a)


# ================================================================ transformador por caracteres (retropropagacion a mano)
def rms(x, g, eps=1e-5):
    r = np.sqrt((x * x).mean(-1, keepdims=True) + eps); xn = x / r
    return xn * g, (xn, r, g)


def rms_back(dy, cache):
    xn, r, g = cache
    dg = (dy * xn).sum(tuple(range(dy.ndim - 1))); dxn = dy * g
    return (dxn - xn * (dxn * xn).mean(-1, keepdims=True)) / r, dg


class LM:
    def __init__(self, V, seed=0):
        r = np.random.default_rng(seed); self.V = V
        p = {'E': r.normal(0, 0.1, (V, D)), 'Pos': r.normal(0, 0.1, (L, D)), 'gf': np.ones(D),
             'Wout': r.normal(0, 1 / np.sqrt(D), (D, V)), 'bout': np.zeros(V)}
        for b in range(NB):
            p[f'g1{b}'] = np.ones(D); p[f'g2{b}'] = np.ones(D)
            for n in 'qkv': p[f'W{n}{b}'] = r.normal(0, 1 / np.sqrt(D), (D, D))
            p[f'Wo{b}'] = r.normal(0, 0.5 / np.sqrt(D), (D, D))
            p[f'W1{b}'] = r.normal(0, 1 / np.sqrt(D), (D, DF)); p[f'b1{b}'] = np.zeros(DF)
            p[f'W2{b}'] = r.normal(0, 0.5 / np.sqrt(DF), (DF, D)); p[f'b2{b}'] = np.zeros(D)
        self.p = p; self.reset_adam(); self.mask = np.triu(np.ones((L, L), bool), 1)
        self.ops_forward = NB * (L * (4 * D * D + 2 * D * DF) + 2 * H * L * L * DH) + L * D * V   # por ventana de L

    def reset_adam(self):
        self.m = {k: np.zeros_like(v) for k, v in self.p.items()}; self.v = {k: np.zeros_like(v) for k, v in self.p.items()}; self.t = 0

    def copia(self):
        o = LM.__new__(LM); o.V = self.V; o.p = {k: v.copy() for k, v in self.p.items()}; o.reset_adam()
        o.mask = self.mask; o.ops_forward = self.ops_forward; return o

    def forward(self, toks):
        """toks (B, L) -> logits (B, L, V); guarda cache. self.hf = estado final (B, L, D) que lee la cabeza de salida."""
        p = self.p; B = toks.shape[0]; T = toks.shape[1]
        X = p['E'][toks] + p['Pos'][None, :T]; self.cache = [toks]; self.capas = []
        for b in range(NB):
            Xn, c1 = rms(X, p[f'g1{b}'])
            Q = (Xn @ p[f'Wq{b}']).reshape(B, T, H, DH).transpose(0, 2, 1, 3)
            K = (Xn @ p[f'Wk{b}']).reshape(B, T, H, DH).transpose(0, 2, 1, 3)
            Vv = (Xn @ p[f'Wv{b}']).reshape(B, T, H, DH).transpose(0, 2, 1, 3)
            S = Q @ K.transpose(0, 1, 3, 2) / np.sqrt(DH)
            S = np.where(self.mask[None, None, :T, :T], -1e9, S); S = S - S.max(-1, keepdims=True)
            A = np.exp(S); A /= A.sum(-1, keepdims=True)
            Oc = (A @ Vv).transpose(0, 2, 1, 3).reshape(B, T, D)
            X1 = X + Oc @ p[f'Wo{b}']
            X1n, c2 = rms(X1, p[f'g2{b}'])
            Hm = np.maximum(X1n @ p[f'W1{b}'] + p[f'b1{b}'], 0)
            X2 = X1 + Hm @ p[f'W2{b}'] + p[f'b2{b}']
            self.capas.append((Xn, c1, Q, K, Vv, A, Oc, X1n, c2, Hm)); X = X2
        self.hf, self.cf = rms(X, p['gf'])
        return self.hf @ p['Wout'] + p['bout']

    def backward(self, logits, y, mask=None):
        """y (B, L) objetivos; mask (B, L) booleana de posiciones que cuentan (todas si None). Perdida media."""
        toks = self.cache[0]; p = self.p; B, T, V = logits.shape
        pr = np.exp(logits - logits.max(-1, keepdims=True)); pr /= pr.sum(-1, keepdims=True)
        dl = pr.copy(); dl[np.arange(B)[:, None], np.arange(T)[None], y] -= 1
        if mask is None: dl /= (B * T)
        else: dl *= mask[..., None]; dl /= max(mask.sum(), 1)
        g = {}
        g['Wout'] = np.tensordot(self.hf, dl, ((0, 1), (0, 1))); g['bout'] = dl.sum((0, 1))
        dX, g['gf'] = rms_back(dl @ p['Wout'].T, self.cf)
        for b in reversed(range(NB)):
            Xn, c1, Q, K, Vv, A, Oc, X1n, c2, Hm = self.capas[b]
            dX2 = dX
            g[f'W2{b}'] = np.tensordot(Hm, dX2, ((0, 1), (0, 1))); g[f'b2{b}'] = dX2.sum((0, 1))
            dHm = (dX2 @ p[f'W2{b}'].T) * (Hm > 0)
            g[f'W1{b}'] = np.tensordot(X1n, dHm, ((0, 1), (0, 1))); g[f'b1{b}'] = dHm.sum((0, 1))
            dX1n, g[f'g2{b}'] = rms_back(dHm @ p[f'W1{b}'].T, c2)
            dX1 = dX2 + dX1n
            g[f'Wo{b}'] = np.tensordot(Oc, dX1, ((0, 1), (0, 1)))
            dOc = (dX1 @ p[f'Wo{b}'].T).reshape(B, T, H, DH).transpose(0, 2, 1, 3)
            dA = dOc @ Vv.transpose(0, 1, 3, 2); dV = A.transpose(0, 1, 3, 2) @ dOc
            dS = A * (dA - (dA * A).sum(-1, keepdims=True)) / np.sqrt(DH)
            dQ = (dS @ K).transpose(0, 2, 1, 3).reshape(B, T, D)
            dK = (dS.transpose(0, 1, 3, 2) @ Q).transpose(0, 2, 1, 3).reshape(B, T, D)
            dV = dV.transpose(0, 2, 1, 3).reshape(B, T, D)
            g[f'Wq{b}'] = np.tensordot(Xn, dQ, ((0, 1), (0, 1))); g[f'Wk{b}'] = np.tensordot(Xn, dK, ((0, 1), (0, 1)))
            g[f'Wv{b}'] = np.tensordot(Xn, dV, ((0, 1), (0, 1)))
            dXn = dQ @ p[f'Wq{b}'].T + dK @ p[f'Wk{b}'].T + dV @ p[f'Wv{b}'].T
            dXn, g[f'g1{b}'] = rms_back(dXn, c1)
            dX = dX1 + dXn
        g['Pos'] = np.zeros_like(p['Pos']); g['Pos'][:T] = dX.sum(0)
        gE = np.zeros_like(p['E']); np.add.at(gE, toks.reshape(-1), dX.reshape(-1, D)); g['E'] = gE
        return g

    def paso_adam(self, g, lr, b1=0.9, b2=0.99, eps=1e-8, clip=1.0):
        n = np.sqrt(sum(float((v * v).sum()) for v in g.values()))
        if n > clip:
            for k in g: g[k] = g[k] * (clip / n)
        self.t += 1
        for k in self.p:
            self.m[k] = b1 * self.m[k] + (1 - b1) * g[k]; self.v[k] = b2 * self.v[k] + (1 - b2) * g[k] ** 2
            self.p[k] -= lr * (self.m[k] / (1 - b1 ** self.t)) / (np.sqrt(self.v[k] / (1 - b2 ** self.t)) + eps)

    def entrena(self, x, y, lr, mask=None):
        lg = self.forward(x); g = self.backward(lg, y, mask); self.paso_adam(g, lr)
        return perdida(lg, y, mask)


KD = 2 * D          # dimension de la clave
VENT_CLAVE = 12     # letras que resume la segunda mitad de la clave


def unit(v): return v / (np.linalg.norm(v, axis=-1, keepdims=True) + 1e-8)


def claves(hf):
    """clave de cada posicion: [estado final de esa posicion ; media del estado final en las ultimas 12 posiciones],
    cada mitad unitaria y el total unitario. La media trae lo que la ultima posicion ya no distingue (p.ej. el nombre
    del hecho 8 letras atras): medido en la semilla 0 (datos/claves_separabilidad.txt), declarado."""
    c = np.cumsum(hf, axis=1); m = c.copy(); m[:, VENT_CLAVE:] = c[:, VENT_CLAVE:] - c[:, :-VENT_CLAVE]
    m = m / np.minimum(np.arange(1, hf.shape[1] + 1), VENT_CLAVE)[None, :, None]
    return np.concatenate([unit(hf), unit(m)], -1) / np.sqrt(2)


def softmax(lg):
    e = np.exp(lg - lg.max(-1, keepdims=True)); return e / e.sum(-1, keepdims=True)


def perdida(lg, y, mask=None):
    pr = softmax(lg); B, T = y.shape
    nll = -np.log(pr[np.arange(B)[:, None], np.arange(T)[None], y] + 1e-12)
    return float(nll.mean()) if mask is None else float((nll * mask).sum() / max(mask.sum(), 1))


def comprueba_gradiente(V=20, seed=0):
    tr = LM(V, seed); r = np.random.default_rng(seed)
    x = r.integers(0, V, (2, L)); y = r.integers(0, V, (2, L)); mk = r.random((2, L)) > 0.3
    g = tr.backward(tr.forward(x), y, mk); peor = 0
    for k in ['Wq0', 'Wk1', 'Wv0', 'Wo1', 'W10', 'W21', 'E', 'Pos', 'Wout', 'g10', 'g21', 'gf', 'b11']:
        for _ in range(3):
            idx = tuple(r.integers(0, s) for s in tr.p[k].shape); old = tr.p[k][idx]; e = 1e-5
            tr.p[k][idx] = old + e; lp = perdida(tr.forward(x), y, mk); tr.p[k][idx] = old - e; lm = perdida(tr.forward(x), y, mk); tr.p[k][idx] = old
            num = (lp - lm) / (2 * e); ana = g[k][idx]; peor = max(peor, abs(num - ana) / (abs(num) + abs(ana) + 1e-8))
    return peor


# ================================================================ base: entrenamiento con gradiente, luego congelada
def lote(rng, txt, B):
    i = rng.integers(0, len(txt) - L - 1, B); idx = i[:, None] + np.arange(L)[None]
    return txt[idx], txt[idx + 1]


def entrena_base(voc, corpus, seg_max=360, pasos_max=20000, B=32, lr=2e-3, seed=0, log=print):
    f = os.path.join(AQUI, 'datos', 'base.npz'); tr = LM(voc.V, seed)
    if os.path.exists(f):
        z = np.load(f); tr.p = {k: z[k] for k in tr.p}; return tr, json.load(open(f + '.json'))
    rng = np.random.default_rng(seed); txt = voc.codifica(corpus['train']); val = voc.codifica(corpus['val'])
    xv, yv = lote(np.random.default_rng(1), val, 200)
    t0 = time.time(); hist = []
    for s in range(pasos_max):
        x, y = lote(rng, txt, B); lr_s = lr * min(1, (s + 1) / 200) * (0.1 if s > pasos_max * 0.85 else 1.0)
        tr.entrena(x, y, lr_s)
        if s % 250 == 0:
            lv = perdida(tr.forward(xv), yv); hist.append((s, round(lv, 4), int(time.time() - t0)))
            log(f'  paso {s} val {lv:.3f} [{time.time()-t0:.0f}s]'); np.savez(f.replace('.npz', '_ckpt.npz'), **tr.p)
        if time.time() - t0 > seg_max: break
    lv = perdida(tr.forward(xv), yv)
    # cordura: contar letras (unigrama) y bigrama como pisos
    cnt = np.bincount(txt, minlength=voc.V) + 1.0; pu = cnt / cnt.sum()
    uni = float(-np.log(pu[yv]).mean())
    big = np.ones((voc.V, voc.V)); np.add.at(big, (txt[:-1], txt[1:]), 1); big /= big.sum(1, keepdims=True)
    bi = float(-np.log(big[xv, yv]).mean())
    acc = float((np.argmax(tr.forward(xv), -1) == yv).mean())
    meta = dict(pasos=s + 1, seg=int(time.time() - t0), val_nll=lv, val_ppl=float(np.exp(lv)), val_acc=acc,
                unigrama_nll=uni, bigrama_nll=bi, hist=hist, n_train=int(len(txt)), n_val=int(len(val)))
    np.savez(f, **tr.p); json.dump(meta, open(f + '.json', 'w'), indent=1)
    return tr, meta


def genera(model, voc, prompt, n=120, temp=0.7, rng=None, colonia=None):
    rng = rng or np.random.default_rng(0); s = list(voc.codifica(prompt)); esp = voc.idx[' ']
    for _ in range(n):
        w = np.array(([esp] * L + s)[-L:])[None]; lg = model.forward(w)[0, -1]; p = softmax(lg / temp)
        if colonia is not None:
            p = colonia.paso(claves(model.hf)[0, -1], p, None, aprender=False)
        s.append(int(rng.choice(voc.V, p=p / p.sum())))
    return voc.decodifica(s)


# ================================================================ maestros (texto nuevo que la base nunca vio)
def maestro_codigo(corpus, voc, rng, n, prueba=False):
    c = voc.codifica(corpus['codigo']); k = len(c) // 5
    zona = c[:k] if prueba else c[k:]                       # el primer quinto queda para sondas
    i = int(rng.integers(0, len(zona) - n)); return zona[i:i + n]


class Inventado:
    """idioma inventado por reglas: palabras CVCV nuevas con gramatica fija  DET NOM VERBO DET NOM ADJ? ."""
    def __init__(self, rng):
        cons, voc_ = 'bdfgjklmnprstvz', 'aeiou'
        def pal(n): return ''.join(rng.choice(list(cons)) + rng.choice(list(voc_)) for _ in range(n))
        self.det = ['ka', 'ni']; self.nom = list({pal(2) for _ in range(12)})[:8]
        self.verb = list({pal(2) + 'r' for _ in range(10)})[:6]; self.adj = list({pal(1) + 'ix' for _ in range(6)})[:4]
    def texto(self, rng, n):
        s = ''
        while len(s) < n:
            s += f"{rng.choice(self.det)} {rng.choice(self.nom)} {rng.choice(self.verb)} {rng.choice(self.det)} {rng.choice(self.nom)}"
            if rng.random() < 0.5: s += ' ' + rng.choice(self.adj)
            s += '. '
        return s[:n]


class Hechos:
    """hechos nuevos 'la clave de NOMBRE es D.' con nombres inventados; version 1, version 2 (cambian), vuelve a 1."""
    def __init__(self, rng, n=8):
        cons, voc_ = 'bdfgjklmnprstvz', 'aeiou'
        nombres = set()
        while len(nombres) < n: nombres.add(''.join(rng.choice(list(cons)) + rng.choice(list(voc_)) for _ in range(2)) + rng.choice(list(cons)))
        self.nombres = sorted(nombres); self.v1 = rng.integers(0, 10, n)
        self.v2 = (self.v1 + rng.integers(1, 10, n)) % 10
    def texto(self, rng, n, version, mentiroso=False):
        vals = self.v1 if version == 1 else self.v2; s = ''
        while len(s) < n:
            i = int(rng.integers(len(self.nombres))); d = int(rng.integers(10)) if mentiroso else int(vals[i])
            s += f"la clave de {self.nombres[i]} es {d}. "
        return s[:n]
    def consultas(self, voc, version):
        vals = self.v1 if version == 1 else self.v2; esp = voc.idx[' ']
        W = []; Y = []
        for i, nm in enumerate(self.nombres):
            # contexto de consulta fijo e igual para todos los brazos; el prefijo es neutro (no trae ningun valor)
            q = voc.codifica(f"fin del registro anterior. la clave de {nm} es "); W.append(([esp] * L + list(q))[-L:]); Y.append(voc.idx[str(int(vals[i]))])
        return np.array(W), np.array(Y)


def maestro_ruido(voc, rng, n):
    letras = voc.codifica('abcdefghijklmnopqrstuvwxyz'); esp = voc.idx[' ']
    return np.array([esp if rng.random() < 0.18 else int(rng.choice(letras)) for _ in range(n)])


def arma_flujo(seed, corpus, voc, cadena=False):
    """lista de segmentos (nombre, maestro, tokens). Los maestros llegan uno tras otro y en 'mix' dos a la vez."""
    rng = np.random.default_rng(seed); inv = Inventado(rng); he = Hechos(rng)
    cod = lambda n, p=False: maestro_codigo(corpus, voc, rng, n, p)
    invt = lambda n: voc.codifica(inv.texto(rng, n)); het = lambda n, v, m=False: voc.codifica(he.texto(rng, n, v, m))
    if cadena:   # (ii) cadena larga de maestros: 4 ciclos; los hechos cambian en cada ciclo
        segs = []
        for c in range(4):
            segs += [(f'py{c}', 'codigo', cod(800)), (f'inv{c}', 'inventado', invt(800)), (f'hechos{c}', 'hechos', het(800, 1 + c % 2))]
        sondas = dict(codigo=('codigo', cod(ESPANOL_PROBE, True)), inventado=('inventado', invt(ESPANOL_PROBE)),
                      espanol=('espanol', voc.codifica(corpus['val'])[2000:2000 + ESPANOL_PROBE]))
        return segs, sondas, (he, Hechos(rng, 6)), inv
    he1 = Hechos(rng, 6)                                   # hechos dichos UNA sola vez (otros nombres)
    unavez = voc.codifica(''.join(f"la clave de {nm} es {int(v)}. " for nm, v in zip(he1.nombres, he1.v1)))
    contra = ''                                            # dos maestros que se CONTRADICEN sobre los mismos hechos (A: v1, B: v2)
    rc = np.random.default_rng(seed + 50)
    while len(contra) < 600:
        i = int(rc.integers(len(he.nombres))); contra += f"la clave de {he.nombres[i]} es {int(he.v1[i])}. la clave de {he.nombres[i]} es {int(he.v2[i])}. "
    segs = [('py1', 'codigo', cod(1500)), ('inv1', 'inventado', invt(1500)), ('hechos1', 'hechos', het(1200, 1)),
            ('unavez', 'unavez', unavez), ('mentiroso', 'mentiroso', het(600, 1, True)), ('ruido', 'ruido', maestro_ruido(voc, rng, 600))]
    mix = []
    for k in range(6): mix += [cod(100), invt(100)]
    segs += [('mix', 'mixto', np.concatenate(mix)), ('hechos2', 'hechos', het(1200, 2)), ('py2', 'codigo', cod(800)),
             ('hechos3', 'hechos', het(1200, 1)), ('contra', 'contra', voc.codifica(contra[:600])), ('inv2', 'inventado', invt(800))]
    sondas = dict(codigo=('codigo', cod(ESPANOL_PROBE, True)), inventado=('inventado', invt(ESPANOL_PROBE)),
                  espanol=('espanol', voc.codifica(corpus['val'])[2000:2000 + ESPANOL_PROBE]))
    return segs, sondas, (he, he1), inv


def ventanas(s, esp):
    """un flujo s -> ventanas (n, L) con stride 16; cada ventana predice sus ultimas 16 letras. Devuelve (W, Y)."""
    pad = np.concatenate([np.full(L - STRIDE, esp), s]); n = (len(pad) - L) // STRIDE
    idx = np.arange(n)[:, None] * STRIDE + np.arange(L)[None]
    return pad[idx], pad[idx + 1]


# ================================================================ brazos
class Base:
    """base congelada sola. Interfaz: procesa(W, Y, est, aprender, maestro) -> P (n, 16, V) distribuciones."""
    nombre = 'base'; propio = False
    def __init__(self, model, C, seed): self.model = model; self.C = C; self.ops = 0; self.rng = np.random.default_rng(seed + 7); self.N_hist = []
    def estados(self, W):
        lg = self.model.forward(W); self.ops += self.model.ops_forward * len(W)
        return softmax(lg[:, -STRIDE:]), claves(self.model.hf)[:, -STRIDE:]
    def procesa(self, W, Y, est=None, aprender=True, maestro=None):
        P, Hs = est if est is not None else self.estados(W); return P
    def memoria(self): return 0
    def consulta(self, W, est=None):
        """W (B, L) ventanas de consulta; devuelve P de la ultima posicion (B, V)."""
        if est is None:
            lg = self.model.forward(W); self.ops += self.model.ops_forward * len(W)
            est = (softmax(lg[:, -1]), claves(self.model.hf)[:, -1])
        return est[0]


class Gradiente(Base):
    """techo caro: seguir entrenando la base con gradiente en linea (un paso de Adam por ventana nueva, 16 letras)."""
    nombre = 'gradiente'; propio = True
    def __init__(self, model, C, seed, lr=1e-3): super().__init__(model.copia(), C, seed); self.lr = lr
    def procesa(self, W, Y, est=None, aprender=True, maestro=None):
        Ps = []
        for k in range(len(W)):
            P, _ = self.estados(W[k:k + 1]); Ps.append(P[0])
            if aprender:
                mk = np.zeros((1, L), bool); mk[:, -STRIDE:] = True
                self.model.entrena(W[k:k + 1], Y[k:k + 1], self.lr, mk); self.ops += 3 * self.model.ops_forward
        return np.array(Ps)


class KNN(Base):
    """kNN-LM (Khandelwal 2020): guarda TODO (estado -> letra siguiente) en memoria FIFO de C, sin compuerta ni energia;
    interpola p = (1-lam) p_base + lam p_knn con los k vecinos mas parecidos (softmax de cosenos / tau)."""
    nombre = 'knn'
    def __init__(self, model, C, seed, lam=0.3, k=8, tau=0.05):
        super().__init__(model, C, seed); self.K = np.zeros((C, KD)); self.Vv = np.zeros(C, int); self.n = 0; self.pos = 0
        self.lam, self.k, self.tau = lam, k, tau
    def paso(self, x, p, c, aprender=True, maestro=None):
        if self.n:
            s = self.K[:self.n] @ x; self.ops += 2 * self.n * KD
            top = np.argpartition(-s, min(self.k, self.n) - 1)[:self.k]; w = np.exp((s[top] - s[top].max()) / self.tau); w /= w.sum()
            pk = np.zeros_like(p); np.add.at(pk, self.Vv[top], w); p = (1 - self.lam) * p + self.lam * pk
        if aprender:
            self.K[self.pos] = x; self.Vv[self.pos] = c; self.pos = (self.pos + 1) % self.C; self.n = min(self.n + 1, self.C)
        return p
    def procesa(self, W, Y, est=None, aprender=True, maestro=None):
        P, Hs = est if est is not None else self.estados(W); out = np.empty_like(P)
        for k in range(len(W)):
            for t in range(STRIDE):
                out[k, t] = self.paso(Hs[k, t], P[k, t], int(Y[k, L - STRIDE + t]), aprender)
        if aprender: self.N_hist.append(self.n)
        return out
    def memoria(self): return self.n
    def consulta(self, W, est=None):
        if est is None:
            lg = self.model.forward(W); self.ops += self.model.ops_forward * len(W)
            est = (softmax(lg[:, -1]), claves(self.model.hf)[:, -1])
        return np.array([self.paso(est[1][i], est[0][i], None, aprender=False) for i in range(len(W))])


class Colonia(Base):
    """celulas vivas sobre el estado interno de la base (reglas de la hamburguesa, 1-oct).
    clave = estado interno normalizado; valor = letra correcta; compuerta: pisa solo si coseno > theta, su letra difiere
    de la que dice la base y ya cobro alguna vez (conf > 0). Pisar = mezclar: p' = (1-alpha) p_base + alpha e_valor.
    cobra si piso y acerto donde la base fallaba (pago repartido entre las que 'oyeron'); si piso donde la base acertaba
    suelta y muere; si fallan las dos corrige su valor; paga por existir; nace una donde la base falla y nadie piso."""
    nombre = 'colonia'
    def __init__(self, model, C, seed, theta=0.9, alpha=0.8, c_exist=0.002, pago=1.0, castigo=0.25, eta=0.2,
                 barajar=False, compuerta=True, E0=1.0, adaptativa=False, th0=0.9):
        super().__init__(model, C, seed); self.adaptativa, self.th0 = adaptativa, th0
        self.W = np.zeros((0, KD)); self.Vv = np.zeros(0, int); self.E = np.zeros(0); self.conf = np.zeros(0); self.th = np.zeros(0)
        self.origen = []; self.ep = []
        self.theta, self.alpha, self.c_exist, self.pago, self.castigo, self.eta = theta, alpha, c_exist, pago, castigo, eta
        self.barajar, self.compuerta, self.E0 = barajar, compuerta, E0
        self.nac = self.mue = self.pisadas = self.pisadas_ok = self.estrechadas = 0; self.nac_por = {}; self.pisa_por = {}; self.pisa_propio = 0
    @property
    def N(self): return self.W.shape[0]
    def paso(self, x, p, c, aprender=True, maestro=None, win=None):
        yf = int(np.argmax(p)); act = cand = np.zeros(0, bool); s = None
        if self.N:
            s = self.W @ x; self.ops += 2 * self.W.size; cand = s > (self.th if self.adaptativa else self.theta)
            act = (cand & (self.Vv != yf) & (self.conf > 0)) if self.compuerta else np.ones(self.N, bool)
        if act.any():
            j = int(np.argmax(np.where(act, s, -9))); v = int(self.Vv[j]); out = (1 - self.alpha) * p; out[v] += self.alpha
            if aprender:
                self.pisadas += 1; self.pisa_por[maestro] = self.pisa_por.get(maestro, 0) + 1
                if self.origen[j] == maestro: self.pisa_propio += 1
        else:
            j = -1; out = p
        if aprender: self.aprende(x, yf, cand, j, c, maestro, win)
        return out
    def _mata(self, viva):
        self.mue += int((~viva).sum()); self.W, self.Vv, self.E, self.conf, self.th = self.W[viva], self.Vv[viva], self.E[viva], self.conf[viva], self.th[viva]
        self.origen = [o for o, v in zip(self.origen, viva) if v]; self.ep = [e for e, v in zip(self.ep, viva) if v]
    def aprende(self, x, yf, cand, j, c, maestro, win):
        if self.N:
            self.E -= self.c_exist
            if j >= 0:
                k = j if not self.barajar else int(self.rng.integers(self.N)); r = int(self.Vv[j])
                if r == c and yf != c:                                   # mi correccion valio: cobro
                    self.pisadas_ok += 1; grupo = np.where(cand)[0]
                    if not len(grupo): grupo = np.array([k])                  # sin compuerta: nadie 'oyo'; cobra la que piso
                    if self.barajar: grupo = self.rng.choice(self.N, len(grupo), replace=False)
                    self.E[grupo] += self.pago / len(grupo); self.conf[grupo] += 1.0 / len(grupo)
                    self.W[k] += self.eta * (x - self.W[k]); self.W[k] /= np.linalg.norm(self.W[k])
                elif r != c and yf == c:                                 # pise donde la base ACERTABA
                    if self.adaptativa and float(self.W[k] @ x) < 0.995:  # estrecho mi radio hasta dejar fuera este estado
                        self.th[k] = max(self.th[k], float(self.W[k] @ x) + 0.002); self.E[k] -= self.castigo; self.estrechadas += 1
                    else: self.conf[k] = 0.0; self.E[k] = -1.0            # suelto y muero
                elif r != c:                                             # fallamos las dos
                    if self.adaptativa and float(self.W[k] @ x) < 0.995:  # otro contexto parecido: estrecho, no cambio de valor
                        self.th[k] = max(self.th[k], float(self.W[k] @ x) + 0.002); self.E[k] -= self.castigo; self.estrechadas += 1
                    else:                                                # el mismo contexto: el hecho cambio, corrijo mi valor
                        self.E[k] -= self.castigo; self.Vv[k] = c
                        if win is not None: self.ep[k] = (win, c)
                        self.W[k] += self.eta * (x - self.W[k]); self.W[k] /= np.linalg.norm(self.W[k])
            muertas = self.E < 0
            if muertas.any(): self._mata(~muertas)
        if j < 0 and yf != c:                                            # nadie piso y la base fallo: nace una celula
            if self.N >= self.C:
                viva = np.ones(self.N, bool); viva[int(np.argmin(self.E))] = False; self._mata(viva)
            self.W = np.vstack([self.W, x]); self.Vv = np.append(self.Vv, c); self.E = np.append(self.E, self.E0)
            self.conf = np.append(self.conf, 1.0); self.th = np.append(self.th, self.th0); self.origen.append(maestro); self.ep.append((win, c))
            self.nac += 1; self.nac_por[maestro] = self.nac_por.get(maestro, 0) + 1
    def procesa(self, W, Y, est=None, aprender=True, maestro=None):
        P, Hs = est if est is not None else self.estados(W); out = np.empty_like(P)
        for k in range(len(W)):
            for t in range(STRIDE):
                # la ventana del episodio (para el sueno): las L letras que preceden a la letra objetivo
                win = None
                if aprender:   # las letras que preceden al objetivo (>= 33), rellenadas a la izquierda con espacio
                    ctx = W[k, max(0, t - STRIDE + 1):L - STRIDE + t + 1]
                    win = np.concatenate([np.full(L - len(ctx), ESP), ctx])
                out[k, t] = self.paso(Hs[k, t], P[k, t], int(Y[k, L - STRIDE + t]), aprender, maestro, win)
        if aprender: self.N_hist.append(self.N)
        return out
    def memoria(self): return self.N
    def consulta(self, W, est=None):
        if est is None:
            lg = self.model.forward(W); self.ops += self.model.ops_forward * len(W)
            est = (softmax(lg[:, -1]), claves(self.model.hf)[:, -1])
        return np.array([self.paso(est[1][i], est[0][i], None, aprender=False) for i in range(len(W))])
    def especializacion(self):
        return self.pisa_propio / max(self.pisadas, 1)


class Cuarentena(Colonia):
    """colonia con el protocolo JUACO como regla local: lo que ensena un maestro NO corrige de inmediato.
    Nace una celula en estado HIPOTESIS (poca energia, sin derecho a pisar). Mientras es hipotesis solo predice EN SOMBRA:
    cuando su contexto reaparece se anota si su correccion habria acertado. Gana confirmaciones solo en apariciones
    INDEPENDIENTES (a mas de L letras de la ultima confirmacion, es decir, otro trozo del flujo), las pierde por fallos y
    por contradecir a una validada que acerto. Con k confirmaciones netas pasa a VALIDADA y puede pisar. Sin validarse en
    `plazo` letras, muere. Una validada que falla al pisar vuelve a hipotesis (se cuenta: registro de errores).
    El sueno solo consolida lo validado."""
    nombre = 'cuarentena'
    def __init__(self, model, C, seed, k=2, plazo=2500, E_h=0.4, gana_sombra=0.3, pierde_sombra=0.2, **kw):
        super().__init__(model, C, seed, **kw); self.k, self.plazo, self.E_h = k, plazo, E_h
        self.gana_sombra, self.pierde_sombra = gana_sombra, pierde_sombra
        self.val = np.zeros(0, bool); self.confirm = np.zeros(0); self.nacio = np.zeros(0, int); self.ult_conf = np.zeros(0, int)
        self.pos = 0; self.reversiones = 0; self.validadas_total = 0; self.murio_sin_validar = 0; self.exp_validar = []
        self.sombra_ok = self.sombra_mal = 0; self.pisa_origen = {}; self.reversion_por = {}; self.validada_por = {}
    def _mata(self, viva):
        self.murio_sin_validar += int((~viva & ~self.val).sum())
        self.val, self.confirm, self.nacio, self.ult_conf = self.val[viva], self.confirm[viva], self.nacio[viva], self.ult_conf[viva]
        super()._mata(viva)
    def paso(self, x, p, c, aprender=True, maestro=None, win=None):
        yf = int(np.argmax(p)); act = cand = np.zeros(0, bool); s = None
        if self.N:
            s = self.W @ x; self.ops += 2 * self.W.size; cand = s > (self.th if self.adaptativa else self.theta)
            act = cand & (self.Vv != yf) & self.val
        if act.any():
            j = int(np.argmax(np.where(act, s, -9))); v = int(self.Vv[j]); out = (1 - self.alpha) * p; out[v] += self.alpha
            if aprender:
                self.pisadas += 1; self.pisa_por[maestro] = self.pisa_por.get(maestro, 0) + 1
                self.pisa_origen[self.origen[j]] = self.pisa_origen.get(self.origen[j], 0) + 1
                if self.origen[j] == maestro: self.pisa_propio += 1
        else:
            j = -1; out = p
        if aprender: self.aprende(x, yf, cand, j, c, maestro, win)
        return out
    def aprende(self, x, yf, cand, j, c, maestro, win):
        self.pos += 1; propone = bool(self.N and (cand & (self.Vv == c)).any())
        if self.N:
            self.E -= self.c_exist
            # --- sombra: hipotesis que habrian pisado (parecidas y en desacuerdo con la base)
            somb = np.where(cand & ~self.val & (self.Vv != yf))[0]
            vals_ok = np.where(cand & self.val & (self.Vv == c))[0]       # validadas que acertaron aqui
            for i in somb:
                if self.Vv[i] == c:
                    self.sombra_ok += 1
                    if self.pos - self.ult_conf[i] > L:                   # aparicion INDEPENDIENTE (otro trozo del flujo)
                        self.confirm[i] += 1; self.ult_conf[i] = self.pos; self.E[i] += self.gana_sombra
                elif self.adaptativa and float(self.W[i] @ x) < 0.995:
                    self.th[i] = max(self.th[i], float(self.W[i] @ x) + 0.002); self.estrechadas += 1
                else:
                    self.sombra_mal += 1; self.confirm[i] -= 1; self.E[i] -= self.pierde_sombra
                    if len(vals_ok): self.confirm[i] -= 1                 # contradice a una validada que acerto
                if self.confirm[i] >= self.k:                             # pasa a VALIDADA
                    self.val[i] = True; self.conf[i] = 1.0; self.E[i] += self.pago; self.validadas_total += 1
                    self.exp_validar.append(int(self.pos - self.nacio[i])); self.validada_por[self.origen[i]] = self.validada_por.get(self.origen[i], 0) + 1
            # --- la que piso
            if j >= 0:
                k = j if not self.barajar else int(self.rng.integers(self.N)); r = int(self.Vv[j])
                if r == c and yf != c:
                    self.pisadas_ok += 1; grupo = np.where(cand & self.val)[0]
                    if not len(grupo): grupo = np.array([k])
                    if self.barajar: grupo = self.rng.choice(self.N, len(grupo), replace=False)
                    self.E[grupo] += self.pago / len(grupo)
                    self.W[k] += self.eta * (x - self.W[k]); self.W[k] /= np.linalg.norm(self.W[k])
                elif self.adaptativa and float(self.W[k] @ x) < 0.995:    # otro contexto parecido: estrecho el radio, sigo validada
                    self.th[k] = max(self.th[k], float(self.W[k] @ x) + 0.002); self.E[k] -= self.castigo; self.estrechadas += 1
                else:                                                     # validada que falla EN SU contexto: vuelve a hipotesis (registro de errores)
                    self.reversiones += 1; self.reversion_por[self.origen[k]] = self.reversion_por.get(self.origen[k], 0) + 1
                    self.val[k] = False; self.confirm[k] = 0; self.nacio[k] = self.pos; self.E[k] = min(self.E[k], self.E_h)
                    if r != c and yf != c: self.Vv[k] = c; self.ep[k] = (win, c)    # fallaron las dos: nueva hipotesis con el valor visto
            # --- plazo y energia
            muertas = (self.E < 0) | (~self.val & (self.pos - self.nacio > self.plazo))
            if muertas.any(): self._mata(~muertas)
        if j < 0 and yf != c and not propone:                                      # nace en HIPOTESIS si nadie ya lo propone
            if self.N >= self.C:
                viva = np.ones(self.N, bool); viva[int(np.argmin(self.E))] = False; self._mata(viva)
            self.W = np.vstack([self.W, x]); self.Vv = np.append(self.Vv, c); self.E = np.append(self.E, self.E_h)
            self.conf = np.append(self.conf, 0.0); self.val = np.append(self.val, False); self.confirm = np.append(self.confirm, 0.0); self.th = np.append(self.th, self.th0)
            self.nacio = np.append(self.nacio, self.pos); self.ult_conf = np.append(self.ult_conf, self.pos)
            self.origen.append(maestro); self.ep.append((win, c)); self.nac += 1; self.nac_por[maestro] = self.nac_por.get(maestro, 0) + 1
    def estado(self):
        return dict(validadas=int(self.val.sum()), hipotesis=int((~self.val).sum()))


class Sueno(Colonia):
    """colonia + sueno: cada `cada` letras la base (copia propia) absorbe con gradiente los episodios de las celulas
    (+ pseudo-ensayo: contextos del corpus original con las respuestas de la base congelada, para no romper lo sabido)
    y libera las celulas cuya correccion la base ya da sola."""
    nombre = 'sueno'; propio = True
    def __init__(self, model, C, seed, cada=1500, pasos=10, lr=1e-3, ensayo=True, corpus_tok=None, **kw):
        super().__init__(model.copia(), C, seed, **kw); self.congelada = model; self.cada, self.pasos, self.lr, self.ensayo = cada, pasos, lr, ensayo
        self.corpus_tok = corpus_tok; self.t = 0; self.liberadas = 0; self.suenos = 0
    def procesa(self, W, Y, est=None, aprender=True, maestro=None):
        out = super().procesa(W, Y, None, aprender, maestro)
        if aprender:
            self.t += STRIDE * len(W)
            if self.t >= self.cada and self.N: self.t = 0; self.duerme()
        return out
    def duerme(self):
        self.suenos += 1
        val = getattr(self, 'val', None)                                 # cuarentena: solo consolida lo VALIDADO
        sel = [i for i, e in enumerate(self.ep) if e[0] is not None and (val is None or val[i])]
        if not sel: return
        if len(sel) > 96: sel = sorted(self.rng.choice(sel, 96, replace=False).tolist())      # tope por sueno (costo)
        X = np.array([self.ep[i][0] for i in sel]); y = np.array([self.ep[i][1] for i in sel])
        Xe = X; Ye = np.zeros_like(Xe); Ye[:, -1] = y; Me = np.zeros(Xe.shape, bool); Me[:, -1] = True
        if self.ensayo and self.corpus_tok is not None:
            xr, _ = lote(self.rng, self.corpus_tok, min(max(len(y), 32), 64)); yr = np.argmax(self.congelada.forward(xr), -1)
            self.ops += self.congelada.ops_forward * len(xr)
            Xe = np.vstack([Xe, xr]); Ye = np.vstack([Ye, yr]); Me = np.vstack([Me, np.ones(xr.shape, bool)])
        for _ in range(self.pasos):
            self.model.entrena(Xe, Ye, self.lr, Me); self.ops += 3 * self.model.ops_forward * len(Xe)
        ok = np.argmax(self.model.forward(X)[:, -1], -1) == y; self.ops += self.model.ops_forward * len(X)
        viva = np.ones(self.N, bool)
        for i, o in zip(sel, ok):
            if o: viva[i] = False
        self.liberadas += int((~viva).sum()); self._mata(viva)


class SuenoCuarentena(Sueno, Cuarentena):
    """cuarentena + sueno: la base solo absorbe lo validado."""
    nombre = 'sueno_cuarentena'


def fabrica(nombre, model, C, seed, corpus_tok, theta, lam):
    if nombre == 'base': return Base(model, C, seed)
    if nombre == 'gradiente': return Gradiente(model, C, seed)
    if nombre == 'knn': return KNN(model, C, seed, lam=lam)
    if nombre == 'colonia': return Colonia(model, C, seed, theta=theta, adaptativa=True)
    if nombre == 'col_fija': return Colonia(model, C, seed, theta=theta)
    if nombre == 'col_barajada': return Colonia(model, C, seed, theta=theta, adaptativa=True, barajar=True)
    if nombre == 'col_sin_compuerta': return Colonia(model, C, seed, theta=theta, compuerta=False)
    if nombre == 'cuarentena': return Cuarentena(model, C, seed, theta=theta, adaptativa=True)
    if nombre == 'cuarentena_fija': return Cuarentena(model, C, seed, theta=theta)
    if nombre == 'sueno': return Sueno(model, C, seed, corpus_tok=corpus_tok, theta=theta, adaptativa=True)
    if nombre == 'sueno_cuarentena': return SuenoCuarentena(model, C, seed, corpus_tok=corpus_tok, theta=theta, adaptativa=True)
    if nombre == 'sueno_sin_ensayo': return Sueno(model, C, seed, corpus_tok=corpus_tok, theta=theta, ensayo=False)
    raise ValueError(nombre)


def acc_digitos(P, Y, voc, partes=4):
    """acierto en las posiciones cuyo objetivo es un digito (la respuesta de un hecho), por cuartos del segmento."""
    y = Y[:, -STRIDE:].reshape(-1); pred = np.argmax(P, -1).reshape(-1); dig = set(voc.idx[d] for d in '0123456789')
    m = np.array([t in dig for t in y]); idx = np.where(m)[0]
    if not len(idx): return []
    tr = np.array_split(idx, partes); return [float((pred[t] == y[t]).mean()) for t in tr if len(t)]


# ================================================================ corrida
def mide(P, Y):
    """P (n, 16, V), Y (n, L) -> nll media y acierto de la siguiente letra."""
    y = Y[:, -STRIDE:]; pr = P[np.arange(len(P))[:, None], np.arange(STRIDE)[None], y]
    return float(-np.log(pr + 1e-12).mean()), float((np.argmax(P, -1) == y).mean())


def corre(seed, model, voc, corpus, brazos, C, theta, lam, cadena=False, muestras=False, log=print):
    segs, sondas, (he, he1), inv = arma_flujo(seed, corpus, voc, cadena); esp = voc.idx[' ']
    corpus_tok = voc.codifica(corpus['train'])
    base = Base(model, C, seed)
    # estados precomputados de la base congelada (se comparten entre los brazos que no tocan los pesos)
    pre = {}
    for nombre, maestro, s in segs:
        W, Y = ventanas(s, esp); pre[nombre] = (W, Y, base.estados(W))
    son = {}
    for k, (maestro, s) in sondas.items():
        W, Y = ventanas(s, esp); son[k] = (W, Y, base.estados(W))
    Wq1, Yq1 = he.consultas(voc, 1); Wq2, Yq2 = he.consultas(voc, 2)
    def est_q(W):
        lg = model.forward(W); return softmax(lg[:, -1]), claves(model.hf)[:, -1]
    eq = {1: est_q(Wq1), 2: est_q(Wq2)}
    Wu, Yu = he1.consultas(voc, 1); eu = est_q(Wu); base_resp = {v: np.argmax(eq[v][0], -1) for v in (1, 2)}
    res = {}; muestras_txt = {}
    for bn in brazos:
        t0 = time.time(); br = fabrica(bn, model, C, seed, corpus_tok, theta, lam); r = dict(seg={}, sonda={}, hechos={}, unavez={}, N={}, ops={}, digitos={}, cuar={})
        version = 0; visto_unavez = False
        for nombre, maestro, s in segs:
            W, Y, est = pre[nombre]; mem0 = br.memoria(); nac0 = getattr(br, 'nac', 0)
            P = br.procesa(W, Y, None if br.propio else est, True, maestro)
            nll, acc = mide(P, Y); r['seg'][nombre] = dict(nll=nll, acc=acc, N=br.memoria(), nac=getattr(br, 'nac', 0) - nac0)
            if nombre.startswith('hechos') or nombre == 'contra': r['digitos'][nombre] = acc_digitos(P, Y, voc)
            if nombre.startswith('hechos'): version = 1 if nombre in ('hechos1', 'hechos3') or (cadena and int(nombre[-1]) % 2 == 0) else 2
            if nombre == 'unavez': visto_unavez = True
            # sondas sin aprender
            sd = {}
            for k, (Ws, Ys, es) in son.items():
                sd[k] = mide(br.procesa(Ws, Ys, None if br.propio else es, False, k), Ys)
            r['sonda'][nombre] = sd
            if version:
                Wq, Yq = (Wq1, Yq1) if version == 1 else (Wq2, Yq2)
                Pq = br.consulta(Wq, None if br.propio else eq[version]); resp = np.argmax(Pq, -1)
                r['hechos'][nombre] = dict(acc=float((resp == Yq).mean()), nll=float(-np.log(Pq[np.arange(len(Yq)), Yq] + 1e-12).mean()),
                                           resp=voc.decodifica(resp), version=version,
                                           acc_v1=float((resp == Yq1).mean()), acc_v2=float((resp == Yq2).mean()),
                                           igual_base=float((resp == base_resp[version]).mean()))
            if visto_unavez:
                Pu = br.consulta(Wu, None if br.propio else eu); r['unavez'][nombre] = float((np.argmax(Pu, -1) == Yu).mean())
            if isinstance(br, Cuarentena):
                r['cuar'][nombre] = dict(br.estado(), reversiones=br.reversiones, validadas_total=br.validadas_total,
                                         murio_sin_validar=br.murio_sin_validar, exp_validar=float(np.median(br.exp_validar)) if br.exp_validar else None,
                                         pisa_origen=dict(br.pisa_origen), validada_por=dict(br.validada_por), reversion_por=dict(br.reversion_por))
            r['N'][nombre] = br.memoria(); r['ops'][nombre] = br.ops
            if muestras and bn in ('base', 'colonia', 'sueno', 'knn', 'gradiente', 'cuarentena') and nombre in ('inv1', 'hechos1', 'mentiroso', 'hechos2', 'hechos3', 'contra') and not cadena:
                rg = np.random.default_rng(seed); col = br if isinstance(br, (Colonia, KNN)) else None
                mdl = br.model
                p1 = f"{inv.det[0]} {inv.nom[0]} "; p2 = f"la clave de {he.nombres[0]} es "; p3 = "la célula "
                muestras_txt[(bn, nombre)] = [genera(mdl, voc, p, 90 if p != p2 else 30, 0.6, rg, col) for p in (p1, p2, p3)]
        ntot = sum(len(s) for _, _, s in segs)
        r['ops_por_letra'] = br.ops / ntot; r['mem_fin'] = br.memoria(); r['seg_cpu'] = time.time() - t0
        r['nac'] = getattr(br, 'nac', 0); r['mue'] = getattr(br, 'mue', 0); r['pisadas'] = getattr(br, 'pisadas', 0)
        r['pisadas_ok'] = getattr(br, 'pisadas_ok', 0); r['estrechadas'] = getattr(br, 'estrechadas', 0); r['liberadas'] = getattr(br, 'liberadas', 0); r['suenos'] = getattr(br, 'suenos', 0)
        r['nac_por'] = getattr(br, 'nac_por', {}); r['pisa_por'] = getattr(br, 'pisa_por', {}); r['N_hist'] = getattr(br, 'N_hist', [])
        r['especializacion'] = br.especializacion() if isinstance(br, Colonia) else None
        if isinstance(br, Colonia): r['origen_fin'] = {o: int(sum(1 for x in br.origen if x == o)) for o in set(br.origen)}
        r['pisa_origen'] = getattr(br, 'pisa_origen', {})
        res[bn] = r
        log(f"  s={seed} C={C} {bn}: " + ' '.join(f"{n}:{r['seg'][n]['acc']:.2f}" for n, _, _ in segs) +
            f" | hechos " + ' '.join(f"{n}:{v['acc']:.2f}" for n, v in r['hechos'].items()) + f" | N={r['mem_fin']} [{r['seg_cpu']:.0f}s]")
    return dict(seed=seed, C=C, theta=theta, lam=lam, segs=[(n, m, len(s)) for n, m, s in segs], brazos=res,
                hechos=dict(nombres=he.nombres, v1=he.v1.tolist(), v2=he.v2.tolist()), inventado=dict(nom=inv.nom, verb=inv.verb)), muestras_txt


def mr(v, f='{:.3f}'):
    v = [x for x in v if x is not None and not (isinstance(x, float) and np.isnan(x))]
    if not v: return '-'
    return f.format(np.median(v)) + ' [' + f.format(min(v)) + '-' + f.format(max(v)) + ']'


def tablas(todo, brazos):
    out = []
    for C in sorted({r['C'] for r in todo}):
        rs = [r for r in todo if r['C'] == C]; segs = [s[0] for s in rs[0]['segs']]
        out.append(f"\n## C={C} (n={len(rs)} semillas) — acierto de la siguiente letra EN LINEA por segmento (mediana [min-max])")
        out.append('| brazo | ' + ' | '.join(segs) + ' | ops/letra | mem fin |'); out.append('|---' * (len(segs) + 3) + '|')
        for b in brazos:
            v = [r['brazos'][b] for r in rs if b in r['brazos']]
            if not v: continue
            out.append(f"| {b} | " + ' | '.join(mr([x['seg'][s]['acc'] for x in v], '{:.2f}') for s in segs) +
                       f" | {int(np.median([x['ops_por_letra'] for x in v]))} | {mr([x['mem_fin'] for x in v], '{:.0f}')} |")
        out.append(f"\n### C={C} — perdida (nats/letra) EN LINEA por segmento")
        out.append('| brazo | ' + ' | '.join(segs) + ' |'); out.append('|---' * (len(segs) + 1) + '|')
        for b in brazos:
            v = [r['brazos'][b] for r in rs if b in r['brazos']]
            if not v: continue
            out.append(f"| {b} | " + ' | '.join(mr([x['seg'][s]['nll'] for x in v], '{:.2f}') for s in segs) + ' |')
        out.append(f"\n### C={C} — HECHOS: acierto del digito al preguntar 'la clave de X es ' (version vigente) tras cada segmento")
        hs = [s for s in segs if s in v[0]['hechos']]
        out.append('| brazo | ' + ' | '.join(hs) + ' |'); out.append('|---' * (len(hs) + 1) + '|')
        for b in brazos:
            v = [r['brazos'][b] for r in rs if b in r['brazos']]
            if not v: continue
            out.append(f"| {b} | " + ' | '.join(mr([x['hechos'][s]['acc'] for x in v], '{:.2f}') for s in hs) + ' |')
        out.append(f"\n### C={C} — SONDAS sin aprender (acierto) tras cada segmento: espanol original (¿rompe lo sabido?) / codigo / inventado")
        out.append('| brazo | sonda | ' + ' | '.join(segs) + ' |'); out.append('|---' * (len(segs) + 2) + '|')
        for b in brazos:
            v = [r['brazos'][b] for r in rs if b in r['brazos']]
            if not v: continue
            for k in ('espanol', 'codigo', 'inventado'):
                out.append(f"| {b} | {k} | " + ' | '.join(mr([x['sonda'][s][k][1] for x in v], '{:.2f}') for s in segs) + ' |')
        out.append(f"\n### C={C} — celulas vivas tras cada segmento / nacimientos por maestro / especializacion (pisadas en el maestro donde nacio)")
        out.append('| brazo | ' + ' | '.join(segs) + ' | nac por maestro | pisadas ok/total | liberadas | espec. |'); out.append('|---' * (len(segs) + 5) + '|')
        for b in brazos:
            v = [r['brazos'][b] for r in rs if b in r['brazos']]
            if not v or b in ('base', 'gradiente'): continue
            nac = v[0]['nac_por']
            out.append(f"| {b} | " + ' | '.join(mr([x['N'][s] for x in v], '{:.0f}') for s in segs) +
                       f" | {' '.join(f'{k}:{int(np.median([x['nac_por'].get(k, 0) for x in v]))}' for k in nac)} | {int(np.median([x['pisadas_ok'] for x in v]))}/{int(np.median([x['pisadas'] for x in v]))} | {int(np.median([x['liberadas'] for x in v]))} | {mr([x['especializacion'] for x in v], '{:.2f}')} |")
        if 'mentiroso' not in segs: continue
        out.append(f"\n### C={C} — CUARENTENA y rivales: verdad dicha UNA vez (acierto en los 6 hechos 'unavez' tras cada segmento) / mentiras / contradiccion")
        us = [s for s in segs if s in v[0]['unavez']]
        out.append('| brazo | ' + ' | '.join('unavez@' + s for s in us) + ' | hechos v1 tras mentiroso | pisadas de celulas nacidas en mentiroso / ruido | contra: acc v1 / acc v2 / igual a la base | curva digitos hechos1 (cuartos) | curva hechos2 |')
        out.append('|---' * (len(us) + 6) + '|')
        for b in brazos:
            v = [r['brazos'][b] for r in rs if b in r['brazos']]
            if not v: continue
            def po(x, k): return x.get('pisa_origen', {}).get(k, 0)
            cur = lambda s: '/'.join(f"{np.median([x['digitos'][s][q] for x in v if len(x['digitos'].get(s, [])) > q]):.2f}" for q in range(4))
            out.append(f"| {b} | " + ' | '.join(mr([x['unavez'][s] for x in v], '{:.2f}') for s in us) +
                       f" | {mr([x['hechos']['mentiroso']['acc'] for x in v], '{:.2f}')} | {int(np.median([po(x, 'mentiroso') for x in v]))} / {int(np.median([po(x, 'ruido') for x in v]))}" +
                       f" | {mr([x['hechos']['contra']['acc_v1'] for x in v], '{:.2f}')} / {mr([x['hechos']['contra']['acc_v2'] for x in v], '{:.2f}')} / {mr([x['hechos']['contra']['igual_base'] for x in v], '{:.2f}')}" +
                       f" | {cur('hechos1')} | {cur('hechos2')} |")
        out.append(f"\n### C={C} — registro de la cuarentena (tras el ultimo segmento): validadas / hipotesis / reversiones (validada que volvio a hipotesis) / murieron sin validar / letras hasta validar (mediana) / validadas por maestro / reversiones por maestro")
        for b in brazos:
            v = [r['brazos'][b] for r in rs if b in r['brazos'] and r['brazos'][b]['cuar']]
            if not v: continue
            ult = segs[-1]; q = [x['cuar'][ult] for x in v]
            out.append(f"- **{b}**: validadas {mr([x['validadas'] for x in q], '{:.0f}')} / hipotesis {mr([x['hipotesis'] for x in q], '{:.0f}')} / reversiones {mr([x['reversiones'] for x in q], '{:.0f}')} / sin validar {mr([x['murio_sin_validar'] for x in q], '{:.0f}')} / hasta validar {mr([x['exp_validar'] for x in q], '{:.0f}')} letras / validadas por maestro {q[0]['validada_por']} / reversiones por maestro {q[0]['reversion_por']} (semilla {rs[0]['seed']})")
            for s in ('hechos1', 'mentiroso', 'contra'):
                qq = [x['cuar'][s] for x in v]
                out.append(f"  - tras {s}: validadas {mr([x['validadas'] for x in qq], '{:.0f}')} hipotesis {mr([x['hipotesis'] for x in qq], '{:.0f}')} reversiones {mr([x['reversiones'] for x in qq], '{:.0f}')}")
    return '\n'.join(out)


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--humo', action='store_true'); ap.add_argument('--base', action='store_true'); ap.add_argument('--seg_base', type=int, default=360)
    ap.add_argument('--semillas', default='1,2,3,4,5'); ap.add_argument('--C', default='200,40'); ap.add_argument('--theta', type=float, default=0.98)
    ap.add_argument('--lam', type=float, default=0.4); ap.add_argument('--brazos', default='base,gradiente,knn,colonia,col_barajada,col_sin_compuerta,sueno')
    ap.add_argument('--out', default='datos/principal.json'); ap.add_argument('--cadena', action='store_true'); ap.add_argument('--muestras', action='store_true')
    a = ap.parse_args(); os.chdir(AQUI)
    voc = Voc(); t00 = time.time()
    if a.humo:
        print('gradiente: error relativo peor =', comprueba_gradiente()); sys.exit()
    corpus = carga_corpus(); print(f"corpus: train {len(corpus['train'])} val {len(corpus['val'])} codigo {len(corpus['codigo'])} archivos {corpus['n_files']}")
    model, meta = entrena_base(voc, corpus, seg_max=a.seg_base)
    print(f"base: pasos {meta['pasos']} {meta['seg']}s val nll {meta['val_nll']:.3f} ppl {meta['val_ppl']:.1f} acc {meta['val_acc']:.3f} | unigrama {meta['unigrama_nll']:.3f} bigrama {meta['bigrama_nll']:.3f}")
    if a.base:
        rg = np.random.default_rng(0)
        for p in ['la célula ', 'el director ', '## resultado']:
            print('---', repr(genera(model, voc, p, 200, 0.7, rg)))
        sys.exit()
    brazos = a.brazos.split(','); todo = []; muestras = {}
    for C in [int(c) for c in a.C.split(',')]:
        for s in [int(x) for x in a.semillas.split(',')]:
            r, m = corre(s, model, voc, corpus, brazos, C, a.theta, a.lam, a.cadena, a.muestras and s == 1 and C == int(a.C.split(',')[0]))
            todo.append(r); muestras.update(m); json.dump(todo, open(a.out, 'w'), indent=0)
            print(f'  [{time.time()-t00:.0f}s]', flush=True)
    txt = tablas(todo, brazos); print(txt); open(a.out.replace('.json', '.md'), 'w', encoding='utf-8').write(txt)
    if muestras:
        lines = ['# Muestras (semilla 1): texto generado (temp 0.6) tras cada maestro; prompts: idioma inventado / hecho / espanol\n']
        for (b, n), ms in muestras.items():
            lines.append(f"\n## {b} tras {n}")
            for m in ms: lines.append('- `' + m.replace('\n', '⏎') + '`')
        open('datos/muestras.md', 'w', encoding='utf-8').write('\n'.join(lines))
    print(f'CPU total {time.time()-t00:.0f}s')
