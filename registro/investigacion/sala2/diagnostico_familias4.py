"""SALA 2 (grafo_tokens) — DIAGNOSTICO ESTRUCTURAL del mundo de FAMILIAS con CUATRO bases (A, B, C, D = los cuatro patrones
del tronco). NO corre el organismo. Para cada asignacion de valencias a las bases:
  (1) familias de los 16 patrones de peso 3 restantes por base mas cercana (Hamming; empates excluidos);
  (2) si el mapa familia -> valencia es LINEALMENTE separable (perceptron con margen, 20000 epocas; no separable = no converge);
  (3) proxy de la via LENTA del tronco: solucion de minima norma sobre las 4 bases con objetivos R (+1 / -3), signo en las
      variantes. (El proxy reproduce EXACTAMENTE Wps-Wns de la corrida real con dos bases: diagnostico_variantes.py.)
  (4) cobertura de la arista por codigo (semillas 1201-1400): variante con padre unico por solapamiento maximo >= g_sol y
      que sea de su familia / de otra familia / empate / ninguno, para g_sol = 2 y g_sol = 1.
Uso: python registro/investigacion/sala2/diagnostico_familias4.py [--desde 1201] [--n 200]
"""
import argparse, hashlib, itertools, os, sys, time
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
import numpy as np
AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(AQUI)))
sys.path[:0] = [os.path.join(RAIZ, 'organismo')]   # organismo/ PRIMERO (ERR-28)
import organismo_v14 as V14
PAT = V14.PAT; BASES = 'ABCD'

def codigos(seed, pats):
    NK, NKMAX, K = V14.NK, V14.NKMAX, V14.K
    rng = np.random.default_rng(seed); rng.uniform(.1, .4, (2, 9))
    KW = np.zeros((NKMAX, 6)); activa = np.zeros(NKMAX, bool); KW[:NK] = rng.uniform(0, 1, (NK, 6)); activa[:NK] = True
    def code(P):
        v = KW @ P; v = np.where(activa, v, -1e9); return frozenset(np.argsort(v)[-K:].tolist())
    while len(code(PAT['A']) & code(PAT['B'])) != 0: KW[0:NK] = rng.uniform(0, 1, (NK, 6))
    return {k: code(P) for k, P in pats.items()}

def familias():
    out = {}
    for combo in itertools.combinations(range(6), 3):
        P = np.zeros(6); P[list(combo)] = 1.; nm = ''.join(str(int(x)) for x in P)
        if any((P == PAT[b]).all() for b in BASES): continue
        d = {b: int(np.abs(P - PAT[b]).sum()) for b in BASES}; m = min(d.values()); cerca = [b for b in BASES if d[b] == m]
        out[nm] = dict(P=P, d=d, fam=cerca[0] if len(cerca) == 1 else 'empate', dist=m)
    return out

def separable(X, y, epocas=20000):
    w = np.zeros(X.shape[1] + 1); Xb = np.hstack([X, np.ones((len(X), 1))])
    for _ in range(epocas):
        err = 0
        for xi, yi in zip(Xb, y):
            if yi * (w @ xi) <= 0: w += yi * xi; err += 1
        if err == 0: return True, w
    return False, w

if __name__ == '__main__':
    ap = argparse.ArgumentParser(); ap.add_argument('--desde', type=int, default=1201); ap.add_argument('--n', type=int, default=200); a = ap.parse_args()
    F = familias(); puras = {k: v for k, v in F.items() if v['fam'] != 'empate'}
    print(f"patrones no base: {len(F)}; con familia unica: {len(puras)}; empates: {sorted(k for k,v in F.items() if v['fam']=='empate')}")
    for b in BASES: print(f"  familia {b} ({''.join(str(int(x)) for x in PAT[b])}): {sorted(k for k,v in puras.items() if v['fam']==b)}")
    Xb = np.array([PAT[b] for b in BASES])
    for nombre, val in (('A+ B- C+ D-  (el mundo vivo con una necesidad)', dict(A=1, B=-1, C=1, D=-1)),
                        ('A+ B- C- D+', dict(A=1, B=-1, C=-1, D=1)), ('A+ B+ C- D-', dict(A=1, B=1, C=-1, D=-1))):
        y = np.array([val[F[k]['fam']] for k in sorted(puras)]); X = np.array([puras[k]['P'] for k in sorted(puras)])
        sep, w = separable(np.vstack([X, Xb]), np.concatenate([y, [val[b] for b in BASES]]))
        R = np.array([1.0 if val[b] > 0 else -3.0 for b in BASES]); wl = np.linalg.pinv(Xb) @ R   # minima norma (proxy via lenta)
        ok = sum((float(wl @ puras[k]['P']) > 0) == (val[puras[k]['fam']] > 0) for k in sorted(puras))
        fuerte = sum(((float(wl @ puras[k]['P']) > 0) == (val[puras[k]['fam']] > 0)) and abs(float(wl @ puras[k]['P'])) >= 0.5 for k in sorted(puras))
        print(f"\n== {nombre}: familias+bases linealmente separables: {sep}")
        print(f"   proxy via lenta (min. norma sobre las 4 bases): Wps-Wns={np.round(wl,3).tolist()}; signo correcto en variantes {ok}/{len(puras)}; correcto y |v|>=0.5: {fuerte}/{len(puras)}")
        for k in sorted(puras): v = float(wl @ puras[k]['P']); print(f"     {k} fam {puras[k]['fam']} ({'+' if val[puras[k]['fam']]>0 else '-'}) dist {puras[k]['dist']}: lenta {v:+.2f} {'OK' if (v>0)==(val[puras[k]['fam']]>0) else 'MAL'}")
    pats = {b: PAT[b] for b in BASES}; pats.update({k: v['P'] for k, v in puras.items()})
    for g_sol in (2, 1):
        cnt = dict(propia=0, otra=0, empate=0, ninguno=0, total=0); ident = 0
        for s in range(a.desde, a.desde + a.n):
            c = codigos(s, pats)
            for k, v in puras.items():
                ov = {b: len(c[k] & c[b]) for b in BASES}; m = max(ov.values()); cnt['total'] += 1
                if m < g_sol: cnt['ninguno'] += 1; continue
                top = [b for b in BASES if ov[b] == m]
                if len(top) > 1: cnt['empate'] += 1
                elif top[0] == v['fam']: cnt['propia'] += 1; ident += (m == 3)
                else: cnt['otra'] += 1
        n = cnt['total']
        print(f"\ncobertura de la arista con g_sol={g_sol} (semillas {a.desde}-{a.desde+a.n-1}, {n} pares): padre PROPIO {cnt['propia']/n:.3f}"
              f" (codigo identico {ident/n:.3f}) | padre de OTRA familia {cnt['otra']/n:.3f} | empate (abstiene) {cnt['empate']/n:.3f} | ninguno {cnt['ninguno']/n:.3f}"
              f" | precision cuando hay arista {cnt['propia']/max(cnt['propia']+cnt['otra'],1):.3f}")
    # alias entre bases (K=3): pares de bases con el mismo codigo
    al = {p: 0 for p in itertools.combinations(BASES, 2)}
    for s in range(a.desde, a.desde + a.n):
        c = codigos(s, {b: PAT[b] for b in BASES})
        for p in al: al[p] += (c[p[0]] == c[p[1]])
    print("\nalias de codigo entre bases (fraccion de semillas con codigo identico): " + ", ".join(f"{p[0]}{p[1]}:{v/a.n:.3f}" for p, v in al.items()))
