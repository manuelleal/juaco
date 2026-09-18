"""SALA 2 (grafo_tokens) — tres preguntas estructurales mas, sin correr el organismo (ver diagnostico_variantes.py):
 (a) identidad de codigo de las variantes TINTE (+0.5 en un pixel apagado), ATENUADA (un pixel de la base a 0.5) y UN
     MOVIMIENTO (Hamming 2) respecto de su base, semillas 1201-1400: si caen en el mismo token, el tronco ya las trata como
     la misma palabra (4c) y el grafo no tiene nada que hacer ahi;
 (b) TRES bases (A, B, C): variantes puras a un movimiento, separabilidad, proxy lineal (minima norma) para las tres
     asignaciones de valencia posibles, cobertura de la arista por codigo (g_sol 2 y 1) y por imagen (L1 <= 2);
 (c) contaminacion lineal: minima norma sobre {A:+1, B:-3, Vf:-3} (una variante de A que se vuelve veneno) leida en los
     hermanos de A; y {A:-3, B:+1} (inversion de la familia) leida en las variantes de A.
"""
import argparse, hashlib, itertools, os, sys
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
import numpy as np
AQUI = os.path.dirname(os.path.abspath(__file__)); RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(AQUI)))
sys.path[:0] = [os.path.join(RAIZ, 'organismo')]
import organismo_v14 as V14
PAT = V14.PAT

def codigos(seed, pats):
    NK, NKMAX, K = V14.NK, V14.NKMAX, V14.K
    rng = np.random.default_rng(seed); rng.uniform(.1, .4, (2, 9))
    KW = np.zeros((NKMAX, 6)); activa = np.zeros(NKMAX, bool); KW[:NK] = rng.uniform(0, 1, (NK, 6)); activa[:NK] = True
    def code(P):
        v = KW @ P; v = np.where(activa, v, -1e9); return frozenset(np.argsort(v)[-K:].tolist())
    while len(code(PAT['A']) & code(PAT['B'])) != 0: KW[0:NK] = rng.uniform(0, 1, (NK, 6))
    return {k: code(P) for k, P in pats.items()}

def peso3():
    out = {}
    for combo in itertools.combinations(range(6), 3):
        P = np.zeros(6); P[list(combo)] = 1.; out[''.join(str(int(x)) for x in P)] = P
    return out

def puras(bases):
    out = {}
    for nm, P in peso3().items():
        if any((P == PAT[b]).all() for b in bases): continue
        d = {b: int(np.abs(P - PAT[b]).sum()) for b in bases}; m = min(d.values()); c = [b for b in bases if d[b] == m]
        if len(c) == 1 and m == 2: out[nm] = dict(P=P, fam=c[0], d=d)
    return out

if __name__ == '__main__':
    ap = argparse.ArgumentParser(); ap.add_argument('--desde', type=int, default=1201); ap.add_argument('--n', type=int, default=200); a = ap.parse_args()
    seeds = range(a.desde, a.desde + a.n)
    # (a) tipos de variante, dos bases
    tipos = {}
    for b in 'AB':
        P = PAT[b]
        for j in range(6):
            if P[j] == 0: Q = P.copy(); Q[j] = 0.5; tipos[f'tinte_{b}{j}'] = (b, Q)
            else: Q = P.copy(); Q[j] = 0.5; tipos[f'aten_{b}{j}'] = (b, Q)
    for nm, v in puras('AB').items(): tipos[f'mov_{v["fam"]}_{nm}'] = (v['fam'], v['P'])
    pats = {'A': PAT['A'], 'B': PAT['B']}; pats.update({k: v[1] for k, v in tipos.items()})
    agg = {}
    for s in seeds:
        c = codigos(s, pats)
        for k, (b, Q) in tipos.items():
            o = len(c[k] & c[b]); oo = len(c[k] & c['B' if b == 'A' else 'A'])
            d = agg.setdefault(k.split('_')[0], dict(n=0, id=0, ov2=0, ov1=0, ov0=0, otro2=0))
            d['n'] += 1; d['id'] += (o == 3); d['ov2'] += (o == 2); d['ov1'] += (o == 1); d['ov0'] += (o == 0); d['otro2'] += (oo >= 2 and o < 2)
    print("(a) codigo de la variante respecto de su base (dos bases, semillas %d-%d):" % (a.desde, a.desde + a.n - 1))
    for k, d in agg.items():
        n = d['n']; print(f"   {k:6s}: identico {d['id']/n:.3f}  comparte 2 {d['ov2']/n:.3f}  comparte 1 {d['ov1']/n:.3f}  comparte 0 {d['ov0']/n:.3f}  | >=2 con la OTRA base y <2 con la propia {d['otro2']/n:.3f}")
    # (b) tres bases
    print("\n(b) TRES bases A, B, C:")
    pu = puras('ABC'); print(f"   variantes puras a un movimiento: {len(pu)}: " + ", ".join(f"{k}->{v['fam']}" for k, v in sorted(pu.items())))
    Xb = np.array([PAT[b] for b in 'ABC'])
    for val in (dict(A=1, B=-1, C=1), dict(A=1, B=-1, C=-1), dict(A=1, B=1, C=-1)):
        R = np.array([1.0 if val[b] > 0 else -3.0 for b in 'ABC']); wl = np.linalg.pinv(Xb) @ R
        res = [(k, float(wl @ v['P']), val[v['fam']]) for k, v in sorted(pu.items())]
        ok = sum((x > 0) == (y > 0) for _, x, y in res); fu = sum(((x > 0) == (y > 0)) and abs(x) >= 0.5 for _, x, y in res)
        print(f"   valencias {val}: proxy lineal Wps-Wns={np.round(wl,2).tolist()}; signo OK {ok}/{len(res)}; OK y |v|>=0.5 {fu}/{len(res)} :: " + ", ".join(f"{k}{x:+.2f}{'' if (x>0)==(y>0) else '(MAL)'}" for k, x, y in res))
    pats3 = {b: PAT[b] for b in 'ABC'}; pats3.update({k: v['P'] for k, v in pu.items()})
    for g in (2, 1):
        c_ = dict(prop=0, otra=0, emp=0, nada=0); ident = 0
        for s in seeds:
            c = codigos(s, pats3)
            for k, v in pu.items():
                ov = {b: len(c[k] & c[b]) for b in 'ABC'}; m = max(ov.values())
                if m < g: c_['nada'] += 1; continue
                top = [b for b in 'ABC' if ov[b] == m]
                if len(top) > 1: c_['emp'] += 1
                elif top[0] == v['fam']: c_['prop'] += 1; ident += (m == 3)
                else: c_['otra'] += 1
        n = sum(c_.values())
        print(f"   arista por CODIGO g_sol={g}: propia {c_['prop']/n:.3f} (identica {ident/n:.3f}) | otra {c_['otra']/n:.3f} | empate {c_['emp']/n:.3f} | ninguna {c_['nada']/n:.3f}")
    # arista por imagen: L1 a la base propia = 2 por construccion; a las otras:
    dd = [sorted(v['d'].values()) for v in pu.values()]
    print(f"   arista por IMAGEN (L1<=2): propia 1.000 por construccion; L1 a la segunda base mas cercana: min {min(d[1] for d in dd)}, asi que con radio 2 no hay empates ni aristas equivocadas")
    al = 0
    for s in seeds:
        c = codigos(s, {b: PAT[b] for b in 'ABC'}); al += (c['A'] == c['C'] or c['B'] == c['C'])
    print(f"   alias de codigo C==A o C==B: {al/a.n:.3f} de las semillas")
    # (c) contaminacion lineal
    print("\n(c) contaminacion lineal (minima norma, dos bases):")
    pu2 = puras('AB'); A, B = PAT['A'], PAT['B']
    for vf in [k for k, v in sorted(pu2.items()) if v['fam'] == 'A']:
        X = np.array([A, B, pu2[vf]['P']]); w = np.linalg.pinv(X) @ np.array([1.0, -3.0, -3.0])
        herm = [(k, float(w @ v['P'])) for k, v in sorted(pu2.items()) if v['fam'] == 'A' and k != vf]
        print(f"   Vf={vf} vuelto veneno: A lee {float(w@A):+.2f}; hermanos de A: " + ", ".join(f"{k}{x:+.2f}{'(MAL)' if x<=0 else ''}" for k, x in herm))
    X = np.array([A, B]); w = np.linalg.pinv(X) @ np.array([-3.0, 1.0])
    print("   familia invertida (A:-3, B:+1): variantes de A leen " + ", ".join(f"{k}{float(w@v['P']):+.2f}" for k, v in sorted(pu2.items()) if v['fam'] == 'A'))
