"""SALA 2 (grafo_tokens) — DIAGNOSTICO ESTRUCTURAL del mundo de VARIANTES. NO corre series; construye KW con el rng de
la semilla como organismo_v14.run (las mismas lineas, verificadas contra el sha del tronco) y lee los codigos de A, B y de
sus variantes a un movimiento (peso 3, Hamming 2 respecto de la base, sin empates entre familias).

Responde, ANTES de disenar umbrales por resultados:
  (1) cobertura de la arista: en que fraccion de variantes |code(var) & code(base propia)| >= 2 (y > la otra base);
  (2) coste: en que fraccion la variante cuelga de la base EQUIVOCADA (>= 2 con la otra y no con la propia);
  (3) lectura a priori de la via LENTA del tronco para las variantes (UNA corrida de un proceso, T = 50 000, semilla
      fija): signo correcto / |v| >= 0.5.
Uso: python registro/investigacion/sala2/diagnostico_variantes.py [--desde 1201] [--n 200] [--corrida 1201]
"""
import argparse, hashlib, itertools, os, sys, time
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
import numpy as np
AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(AQUI)))
sys.path[:0] = [os.path.join(RAIZ, 'organismo')]   # organismo/ PRIMERO (ERR-28)
import organismo_v14 as V14
SHA_V14 = 'feefc88b1fd8d434'
h16 = lambda p: hashlib.sha256(open(p, 'rb').read()).hexdigest()[:16]

def codigos(seed, pats):
    L, NK, NKMAX, K, PAT = V14.L, V14.NK, V14.NKMAX, V14.K, V14.PAT
    rng = np.random.default_rng(seed); rng.uniform(.1, .4, (2, 9))
    KW = np.zeros((NKMAX, 6)); activa = np.zeros(NKMAX, bool); KW[:NK] = rng.uniform(0, 1, (NK, 6)); activa[:NK] = True
    def code(P):
        v = KW @ P; v = np.where(activa, v, -1e9); return frozenset(np.argsort(v)[-K:].tolist())
    while len(code(PAT['A']) & code(PAT['B'])) != 0: KW[0:NK] = rng.uniform(0, 1, (NK, 6))
    return {k: code(P) for k, P in pats.items()}

def variantes():
    A, B = V14.PAT['A'], V14.PAT['B']; out = {}
    for combo in itertools.combinations(range(6), 3):
        P = np.zeros(6); P[list(combo)] = 1.; nm = ''.join(str(int(x)) for x in P)
        dA, dB = int(np.abs(P - A).sum()), int(np.abs(P - B).sum())
        if dA == 0 or dB == 0: continue
        fam = 'A' if dA < dB else ('B' if dB < dA else 'empate')
        out[nm] = dict(P=P, dA=dA, dB=dB, fam=fam)
    return out

if __name__ == '__main__':
    ap = argparse.ArgumentParser(); ap.add_argument('--desde', type=int, default=1201); ap.add_argument('--n', type=int, default=200)
    ap.add_argument('--corrida', type=int, default=1201); a = ap.parse_args()
    s14 = h16(os.path.join(RAIZ, 'organismo', 'organismo_v14.py'))
    print(f"sha organismo_v14 {s14}" + ("" if s14 == SHA_V14 else f"  *** CAMBIO respecto de {SHA_V14}"))
    V = variantes()
    puras = {k: v for k, v in V.items() if v['fam'] in 'AB' and min(v['dA'], v['dB']) == 2}
    lejos = {k: v for k, v in V.items() if v['fam'] in 'AB' and min(v['dA'], v['dB']) == 4}
    emp = [k for k, v in V.items() if v['fam'] == 'empate']
    print(f"patrones de peso 3: {len(V)+2}; variantes a un movimiento (puras): {len(puras)} "
          f"({sum(v['fam']=='A' for v in puras.values())} de A, {sum(v['fam']=='B' for v in puras.values())} de B); "
          f"empates a distancia 2 de ambas: {len(emp)} {emp}; lejanas (dist 4 de ambas o mas cerca de una a 4): {len(lejos)} {sorted(lejos)}")
    for k, v in sorted(puras.items()): print(f"   {k}  fam {v['fam']}  dA {v['dA']} dB {v['dB']}")
    pats = {'A': V14.PAT['A'], 'B': V14.PAT['B']}; pats.update({k: v['P'] for k, v in puras.items()})
    seeds = range(a.desde, a.desde + a.n); t0 = time.time()
    cnt = dict(total=0, propia2=0, propia3=0, equivocada2=0, equivocada3=0, ambas2=0, ninguna=0, propia1=0)
    hist = {}
    por_var = {k: dict(propia=0, equiv=0, amb=0, nada=0) for k in puras}
    ali_AB_var = 0; ali_var_var = 0
    for s in seeds:
        c = codigos(s, pats)
        cods = [c[k] for k in puras]
        ali_var_var += sum(1 for i in range(len(cods)) for j in range(i+1, len(cods)) if cods[i] == cods[j])
        for k, v in puras.items():
            op = len(c[k] & c[v['fam']]); oe = len(c[k] & c['B' if v['fam'] == 'A' else 'A'])
            hist[(op, oe)] = hist.get((op, oe), 0) + 1; cnt['total'] += 1
            if op >= 2 and oe >= 2: cnt['ambas2'] += 1; por_var[k]['amb'] += 1
            elif op >= 2: cnt['propia2'] += 1; por_var[k]['propia'] += 1; cnt['propia3'] += (op == 3)
            elif oe >= 2: cnt['equivocada2'] += 1; por_var[k]['equiv'] += 1; cnt['equivocada3'] += (oe == 3)
            else: cnt['ninguna'] += 1; por_var[k]['nada'] += 1; cnt['propia1'] += (op == 1)
    n = cnt['total']
    print(f"\nsemillas {a.desde}-{a.desde+a.n-1} ({time.time()-t0:.1f} s), {n} pares (variante, semilla):")
    print(f"  arista a la base PROPIA (>=2 propia, <2 la otra): {cnt['propia2']/n:.3f}  (de las cuales codigo IDENTICO a la base: {cnt['propia3']/n:.3f})")
    print(f"  arista a la base EQUIVOCADA (>=2 la otra, <2 propia): {cnt['equivocada2']/n:.3f}  (identico a la otra: {cnt['equivocada3']/n:.3f})")
    print(f"  ambas >=2 (empate: abstenerse): {cnt['ambas2']/n:.3f}   ninguna >=2 (sin arista -> via lenta): {cnt['ninguna']/n:.3f} (con 1 celda propia: {cnt['propia1']/n:.3f})")
    print(f"  variantes con el MISMO codigo entre si por semilla: {ali_var_var/a.n:.2f}")
    print("  histograma (solap propia, solap otra): " + ", ".join(f"{k}:{v/n:.3f}" for k, v in sorted(hist.items(), reverse=True)))
    print("  por variante (fraccion de semillas con arista propia / equivocada / ambas / ninguna):")
    for k in sorted(puras): d = por_var[k]; print(f"   {k} fam {puras[k]['fam']}: {d['propia']/a.n:.2f} / {d['equiv']/a.n:.2f} / {d['amb']/a.n:.2f} / {d['nada']/a.n:.2f}")
    # (3) UNA corrida de un proceso, T=50000: lectura de la via lenta del tronco para cada variante
    print(f"\nUNA corrida organismo_v14.run({a.corrida}, T=50000) — lectura de la via LENTA (Wps-Wns)@P para las variantes:")
    t0 = time.time(); r = V14.run(a.corrida, T=50000); Wl = np.array(r['Wps']) - np.array(r['Wns'])
    print(f"  {time.time()-t0:.1f} s; W={r['W']} W_lenta={r['W_lenta']} celdas={r['celdas']} splits={r['splits']} muertes={r['deaths']}; Wps-Wns={np.round(Wl,3).tolist()}")
    ok = 0; fuerte = 0
    for k, v in sorted(puras.items()):
        val = float(Wl @ v['P']); sgn = (val > 0) == (v['fam'] == 'A'); ok += sgn; fuerte += sgn and abs(val) >= 0.5
        print(f"   {k} fam {v['fam']} ({'comida' if v['fam']=='A' else 'veneno'}): lenta {val:+.2f}  {'OK' if sgn else 'MAL'}{' fuerte' if abs(val)>=0.5 else ''}")
    print(f"  signo correcto {ok}/{len(puras)}; correcto y |v|>=0.5: {fuerte}/{len(puras)}")
