"""EXO-2: la capa JUACO decide que entra a entrenar (digitos 8x8). Ver PREREGISTRO_exo2_ml.md.
Uso: python exo2_ml.py --desde 1 --n 10
"""
import argparse, json, os
from datetime import datetime
import numpy as np
from sklearn.datasets import load_digits

AQUI = os.path.dirname(os.path.abspath(__file__))
X0, Y0 = load_digits(return_X_y=True); X0 = X0 / 16.0
LOTE, FASE1, BUF, REPASO, LR = 50, 600, 200, 50, 0.1


def swap(y): y = y.copy(); a, b = y == 3, y == 8; y[a], y[b] = 8, 3; return y


class Softmax:
    def __init__(s): s.W = np.zeros((64, 10)); s.b = np.zeros(10)
    def p(s, X):
        z = X @ s.W + s.b; z -= z.max(1, keepdims=True); e = np.exp(z); return e / e.sum(1, keepdims=True)
    def fit(s, X, y, epocas=3):
        for _ in range(epocas):
            P = s.p(X); P[np.arange(len(y)), y] -= 1
            s.W -= LR * X.T @ P / len(y) * 5; s.b -= LR * P.mean(0) * 5
    def acc(s, X, y, m=None):
        ok = s.p(X).argmax(1) == y; return float(ok[m].mean() if m is not None else ok.mean())


def corre(brazo, seed, cuotas=None):
    rng = np.random.default_rng(seed); idx = rng.permutation(len(Y0))
    Xs, ys, Xt, yt = X0[idx[:1200]], Y0[idx[:1200]].copy(), X0[idx[1200:]], Y0[idx[1200:]]
    ys[FASE1:] = swap(ys[FASE1:]); yt2 = swap(yt); m38 = np.isin(yt2, [3, 8])
    M = Softmax(); bX, by = np.zeros((0, 64)), np.zeros(0, int); usados = 0; escritos = []; out = {}
    for k, i in enumerate(range(0, 1200, LOTE)):
        X, y = Xs[i:i + LOTE], ys[i:i + LOTE]
        if brazo == "TODO":
            sel = np.arange(len(y))
        elif brazo == "J":
            pt = M.p(X)[np.arange(len(y)), y]; sel = np.where(pt < 0.5)[0]
        else:
            sel = rng.choice(len(y), cuotas[k], replace=False)
        escritos.append(len(sel)); usados += len(sel)
        if brazo == "J" and len(sel) and len(by):          # sobrescritura: vecinos con etiqueta distinta salen
            nX = X[sel] / (np.linalg.norm(X[sel], axis=1, keepdims=True) + 1e-9)
            nB = bX / (np.linalg.norm(bX, axis=1, keepdims=True) + 1e-9)
            sim = nX @ nB.T; malo = ((sim > 0.9) & (y[sel][:, None] != by[None, :])).any(0)
            bX, by = bX[~malo], by[~malo]
        if brazo != "TODO":
            rep = rng.choice(len(by), min(REPASO, len(by)), replace=False) if len(by) else np.array([], int)
            TX = np.vstack([X[sel], bX[rep]]); Ty = np.concatenate([y[sel], by[rep]])
        else:
            TX, Ty = X, y
        if len(Ty): M.fit(TX, Ty)
        if brazo != "TODO" and len(sel):
            bX, by = np.vstack([bX, X[sel]]), np.concatenate([by, y[sel]])
            if brazo == "J":                                   # olvido de lo redundante
                keep = M.p(bX)[np.arange(len(by)), by] <= 0.95; bX, by = bX[keep], by[keep]
            bX, by = bX[-BUF:], by[-BUF:]
        visto = i + LOTE
        if visto == FASE1: out["fase1"] = M.acc(Xt, yt)
        if visto == FASE1 + 100: out["38_tras100"] = M.acc(Xt, yt2, m38)
        if visto == FASE1 + 200: out["38_tras200"] = M.acc(Xt, yt2, m38)
    out["fase2"] = M.acc(Xt, yt2); out["frac_usada"] = usados / 1200
    return out, escritos


if __name__ == "__main__":
    ap = argparse.ArgumentParser(); ap.add_argument("--desde", type=int, default=1); ap.add_argument("--n", type=int, default=10)
    a = ap.parse_args(); seeds = range(a.desde, a.desde + a.n); R = {"TODO": [], "J": [], "R": []}
    for s in seeds:
        R["TODO"].append(corre("TODO", s)[0]); oj, cuotas = corre("J", s); R["J"].append(oj)
        R["R"].append(corre("R", s, cuotas)[0])
    res = {b: {k: round(float(np.mean([r[k] for r in v])), 3) for k in v[0]} for b, v in R.items()}
    nom = f"exo2_s{a.desde}-{a.desde + a.n - 1}_{datetime.now():%Y%m%d_%H%M%S}"
    os.makedirs(os.path.join(AQUI, "datos"), exist_ok=True)
    json.dump(dict(res=res, crudo=R), open(os.path.join(AQUI, "datos", nom + ".json"), "w"), indent=1)
    print(nom)
    for b, m in res.items(): print(b.ljust(5), m)
