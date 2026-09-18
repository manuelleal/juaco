"""Arnes de identidad del gemelo compilado: mundo_temporal_k_rapido.run(...) debe ser BIT A BIT igual (todas las claves,
tras ida y vuelta por JSON) a mundo_temporal_k.run(...). Rejilla A: los 6 brazos x kprof 1-5 x semillas 1-3 con las
perillas de v13 que usa corre_3T_k.py (mu_norm=True, div_signo=True, eta_s=0.015, puerta=3). Rejilla B (cobertura de
perillas apagadas, por si el mundo se corre en otro regimen): v11 (eta_s=0, puerta=None), v10 (+div_signo=False),
v9 (+mu_norm=False), sin plasticidad forzada por lam=0, sin memoria de rechazo, wclip/nkmax distintos, sobre C3 y C1p.
Cuando algo difiere se imprime la PRIMERA clave que difiere con los dos valores. Imprime tambien la aceleracion.
Uso: python experimentos/nivel7_3T_k/identidad_temporal_rapido.py [--T 30000] [--full]
"""
import sys, os, json, time
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import mundo_temporal_k as lento, mundo_temporal_k_rapido as rapido

T = int(sys.argv[sys.argv.index('--T') + 1]) if '--T' in sys.argv else 30000
N = lambda x: json.loads(json.dumps(x, default=str))
V13 = dict(mu_norm=True, div_signo=True, eta_s=0.015, puerta=3)   # las de corre_3T_k.py
ARMS = ['C1', 'C1p', 'C2', 'C2b', 'C3', 'C3C']
KS = [1, 2, 3, 4, 5]
SEEDS = [1, 2, 3]
PERILLAS = {
    'v11': dict(eta_s=0.0, puerta=None),
    'v10': dict(eta_s=0.0, puerta=None, div_signo=False),
    'v9': dict(eta_s=0.0, puerta=None, div_signo=False, mu_norm=False),
    'lam0': dict(lam=0.0),
    'sin_rechazo': dict(memoria_rechazo=0),
    'sin_aprender': dict(learn=False),
    'pool60_wclip5': dict(nkmax=60, wclip=5.0, early=1000, nobj=6),
}


def compara(nombre, arm, k, kw, s):
    a = lento.run(s, arm=arm, T=T, kprof=k, **kw)
    b = rapido.run(s, arm=arm, T=T, kprof=k, **kw)
    falta = [x for x in a if x not in b] + [x for x in b if x not in a]
    dif = [x for x in a if x in b and N(a[x]) != N(b[x])]
    if falta or dif:
        x = (falta + dif)[0]
        print(f"  DIFIERE {nombre} {arm} k={k} s{s}: claves={falta + dif}")
        print(f"      primera clave que difiere: {x}")
        print(f"        lento  {str(N(a.get(x)))[:400]}")
        print(f"        rapido {str(N(b.get(x)))[:400]}")
        return False
    return True


if __name__ == '__main__':
    t0 = time.time(); rapido.run(1, 'C3', T=2000, kprof=2, **V13); print(f"compilacion/carga de cache: {time.time()-t0:.1f}s")
    fallos = []; n = 0
    print(f"REJILLA A — perillas v13 {V13}, T={T}")
    for k in KS:
        for arm in ARMS:
            ok = True
            for s in SEEDS:
                n += 1
                if not compara('v13', arm, k, V13, s):
                    ok = False; fallos.append(('v13', arm, k, s))
            print(f"  k={k} {arm:4s} semillas {SEEDS}: {'IDENTICO' if ok else 'FALLA'}")
    print(f"REJILLA B — perillas apagadas / variantes, T={T}")
    for nombre, kw in PERILLAS.items():
        ok = True
        for arm in ['C3', 'C1p']:
            for k in [1, 3]:
                for s in SEEDS[:2]:
                    n += 1
                    if not compara(nombre, arm, k, dict(V13, **kw), s):
                        ok = False; fallos.append((nombre, arm, k, s))
        print(f"  {nombre:14s} C3/C1p x k=1,3 x s1-2: {'IDENTICO' if ok else 'FALLA'}")
    print(f"identidad: {n - len(fallos)}/{n} corridas identicas "
          f"(T={T}; A: {len(ARMS)} brazos x {len(KS)} profundidades x {len(SEEDS)} semillas; B: {len(PERILLAS)} variantes)")
    if '--full' in sys.argv or not fallos:
        t0 = time.time(); a = lento.run(7, arm='C3', T=100000, kprof=3, **V13); tl = time.time() - t0
        t0 = time.time(); b = rapido.run(7, arm='C3', T=100000, kprof=3, **V13); tr = time.time() - t0
        ident = all(N(a[x]) == N(b[x]) for x in a) and set(a) == set(b)
        print(f"100k pasos (C3, k=3, semilla 7): original {tl:.2f}s, gemelo {tr:.2f}s -> x{tl/tr:.1f}; "
              f"identidad a 100k: {'OK' if ident else 'FALLA'}")
    sys.exit(1 if fallos else 0)
