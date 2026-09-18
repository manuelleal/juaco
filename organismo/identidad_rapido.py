"""Arnes de identidad del gemelo compilado: organismo_v13_rapido.run(...) debe ser BIT A BIT igual (todas las claves, tras
ida y vuelta por JSON) a organismo_v13.run(...) en una rejilla de configuraciones que cubre lo que usan las baterias
(v13, v11 = eta_s=0/puerta=None, v10 = +div_signo=False, v9 = +mu_norm=False, sin plasticidad, sin memoria de rechazo,
invertir, nuevo con y sin solap_B, nobj distinto) y semillas 1-6. Imprime tambien la aceleracion.
Uso: python organismo/identidad_rapido.py [--T 30000] [--full]
"""
import sys, os, json, time
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import organismo_v13 as lento, organismo_v13_rapido as rapido

T = int(sys.argv[sys.argv.index('--T') + 1]) if '--T' in sys.argv else 30000
N = lambda x: json.loads(json.dumps(x, default=str))
CONFIGS = {
    'v13': dict(),
    'invertir': dict(invertir_en=T // 2),
    'nuevo_C': dict(nuevo='C', nuevo_en=T // 3),
    'nuevo_D_solapB': dict(nuevo='D', nuevo_en=T // 3, solap_B=1, nuevo_val='comida'),
    'v11': dict(eta_s=0.0, puerta=None),
    'v10': dict(eta_s=0.0, puerta=None, div_signo=False),
    'v9': dict(eta_s=0.0, puerta=None, div_signo=False, mu_norm=False),
    'sin_plast': dict(plast=False),
    'sin_rechazo': dict(memoria_rechazo=0),
    'nobj6_lam0': dict(nobj=6, lam=0.0),
    'sin_puerta_con_lenta': dict(puerta=None),
    'solapAB1': dict(solap_AB=1),
}
SEEDS = [1, 2, 3, 4, 5, 6]

if __name__ == '__main__':
    t0 = time.time(); rapido.run(1, T=2000); print(f"compilacion/carga de cache: {time.time()-t0:.1f}s")
    fallos = []; n = 0
    for nombre, kw in CONFIGS.items():
        for s in SEEDS:
            a = lento.run(s, T=T, **kw); b = rapido.run(s, T=T, **kw)
            dif = [k for k in a if N(a[k]) != N(b[k])]; n += 1
            if dif:
                fallos.append((nombre, s, dif))
                print(f"  DIFIERE {nombre} s{s}: {dif}")
    print(f"identidad: {n - len(fallos)}/{n} corridas identicas (T={T}, {len(CONFIGS)} configuraciones x {len(SEEDS)} semillas)")
    if '--full' in sys.argv or not fallos:
        t0 = time.time(); lento.run(7, T=100000); tl = time.time() - t0
        t0 = time.time(); rapido.run(7, T=100000); tr = time.time() - t0
        a = lento.run(7, T=100000); b = rapido.run(7, T=100000)
        print(f"100k pasos: tronco {tl:.2f}s, gemelo {tr:.2f}s -> x{tl/tr:.1f}; identidad a 100k: {'OK' if all(N(a[k]) == N(b[k]) for k in a) else 'FALLA'}")
    sys.exit(1 if fallos else 0)
