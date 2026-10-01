"""nulo_p8.py — EL NULO Y LA POTENCIA de la letra de P8 (regla 15 / ERR-91), por codigo, sobre los JSON de la SONDA 2 (semillas 737300-737305, que
NO entran en la serie). Unidad = semilla. Nulo = la memoria de lugar PERMUTADA entre bins (la composicion sin contenido de lugar).
SESGO DECLARADO: los umbrales se fijaron DESPUES de ver esta sonda; aqui solo se calcula que tan a menudo los pasaria el nulo y la senal vista.
    python experimentos/organelos/escalera/p8/nulo_p8.py [--perm 200] [--sim 20000]
"""
import argparse, glob, json, math, os, statistics as st, sys
import numpy as np
AQUI = os.path.dirname(os.path.abspath(__file__)); ESC = os.path.dirname(AQUI)
sys.path.insert(0, AQUI)
import corre_p8 as C8
S2 = C8.S2


def main(argv=None):
    ap = argparse.ArgumentParser(allow_abbrev=False); ap.add_argument('--perm', type=int, default=200); ap.add_argument('--sim', type=int, default=20000)
    a = ap.parse_args(argv)
    comp = C8.modulo('O1_LUGAR_COMP')[0]; rng = np.random.default_rng(20261001)
    fs = sorted(glob.glob(os.path.join(ESC, 'sondas', 'datos', 's2_humo', '*', 'prueba_i*_cria.json')))
    obs = []; nulo = []
    for f in fs:
        d = json.load(open(f, encoding='utf-8')); L = d['L']; z0 = d['oasis_info']['z0']
        ls = [l for l in d['linajes_s2'] if l['establecido'] and l['conoce_E'] and l['conoce_A'] and (l['mord_E_dentro'] or 0) == 0]   # 'valido' de corre_p8
        if len(ls) < C8.MIN_VAL: continue
        obs.append(st.median(l['resp']['comp']['L_D'] for l in ls))
        for _ in range(a.perm):
            dd = []
            for l in ls:
                m = d['memorias'][l['i']]; p = [int(z) for z in rng.permutation(30)]
                dd.append(S2.pregunta({'x': comp}, dict(m, lugar=[m['lugar'][j] for j in p], nl=[m['nl'][j] for j in p]), L, z0)['x']['L_D'])
            nulo.append(st.median(dd))
    p0 = sum(x > 0 for x in nulo) / len(nulo)
    binom = lambda n, k, p: sum(math.comb(n, j) * p ** j * (1 - p) ** (n - j) for j in range(k, n + 1))
    print(f"sonda: {len(obs)} semillas · D por semilla (comp sobre memoria de lug) {sorted(obs)} · mediana {st.median(obs)} · semillas con D > 0: {sum(x > 0 for x in obs)}/{len(obs)}")
    print(f"NULO (memoria de lugar permutada, {len(nulo)} semillas-permutacion): P(D de la semilla > 0) = {p0:.4f} · media {st.mean(nulo):.4f} · P(|D| > {C8.PERM_MAX}) = {sum(abs(x) > C8.PERM_MAX for x in nulo) / len(nulo):.4f}")
    print(f"  falso positivo de P1 (>= {C8.K_POS}/20 semillas con D > 0) bajo el nulo: {binom(20, C8.K_POS, p0):.2e} (cota con p0 x 5: {binom(20, C8.K_POS, min(1, 5 * p0)):.2e})")
    nb = np.asarray(nulo); ob = np.asarray(obs); sn = rng.choice(nb, size=(a.sim, 20)); so = rng.choice(ob, size=(a.sim, 20))
    fun = lambda s, m: float((((s > 0).sum(1) >= C8.K_POS) & (np.median(s, 1) >= m)).mean())
    print(f"  simulacion de 20 semillas (remuestreo, {a.sim}): bajo el nulo P(P1 y mediana >= {C8.MED_FUN}) = {fun(sn, C8.MED_FUN):.4f} · P(P1 y mediana >= {C8.MED_MOD}) = {fun(sn, C8.MED_MOD):.4f}")
    print(f"  POTENCIA si la serie se parece a la sonda (remuestreo de {len(obs)} semillas; cruda): P(FUNCIONA por P1+P2) = {fun(so, C8.MED_FUN):.3f} · P(al menos MODESTO) = {fun(so, C8.MED_MOD):.3f}")
    print(f"  puerta P3 (|mediana de la permutada| <= {C8.PERM_MAX}) bajo el nulo, 20 semillas con media de {C8.NPERM} permutaciones: la mediana por semilla del nulo es 0 en {float((nb == 0).mean()):.3f} de los casos")
    return 0


if __name__ == '__main__':
    sys.exit(main())
