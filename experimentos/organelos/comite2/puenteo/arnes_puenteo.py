# EXPLORATORIO, no es dato
"""arnes_puenteo.py — arnes chico del puenteo (un proceso, N 9, fundador limpio, T corto).

MISION: llegar a la AGI por este camino.
  (1) V143P == V143 salida ENTERA (fisica + _carrera + carro + rng del mundo)
  (2) O1P == O1 salida ENTERA
  (3) HIB con todo en 0 == V143 en todo salvo d['carro']
  (4) HIB con patas + boca_buena + boca_mala == O1 en todo salvo d['carro'] y exp_hasta (telemetria que usa valor_nec, que O1 no tiene)
  (5) cada puente solo NO es inerte (cambia la fisica respecto de V143) y (6) es determinista (dos corridas iguales)
Uso: python arnes_puenteo.py [--T 2000] [--seed 36901]
"""
import argparse, json, os, sys, time

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(AQUI))))), 'bundle')   # JUACO/bundle
PISTA = os.path.join(RAIZ, 'experimentos', 'carrera_escuderias')
V143D = os.path.join(RAIZ, 'experimentos', 'tronco_v14_3', 'carros_v143')
sys.path.insert(0, PISTA)
import pista as P
import importlib.util


def carga(ruta, nombre):
    spec = importlib.util.spec_from_file_location(nombre, ruta); m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m


N = lambda x: json.loads(json.dumps(x, default=str))


def sin(r, claves):
    out = dict(r); out['linajes'] = [{k: v for k, v in d.items() if k not in claves} for d in r['linajes']]; return out


def main():
    ap = argparse.ArgumentParser(allow_abbrev=False)
    ap.add_argument('--T', type=int, default=2000); ap.add_argument('--seed', type=int, default=36901)
    a = ap.parse_args()
    T, seed = a.T, a.seed
    V143 = carga(os.path.join(V143D, 'V143.py'), 'V143'); O1 = P.carga_carro('O1')
    V143P = carga(os.path.join(AQUI, 'carros', 'V143P.py'), 'V143P'); O1P = carga(os.path.join(AQUI, 'carros', 'O1P.py'), 'O1P')
    HIB = carga(os.path.join(AQUI, 'carros', 'HIB.py'), 'HIB')
    ok = True; t0 = time.time()
    run = lambda m: P.run(seed, [('C', m)] * 9, T=T, pizarra=1, rep_acum=0, escala=1, mundo_n=None, fundador_limpio=1)

    def chk(nombre, cond):
        nonlocal ok; ok &= bool(cond); print(f"  {'OK   ' if cond else 'FALLA'} {nombre}", flush=True)

    rv = N(run(V143)); ro = N(run(O1))
    chk(f"(1) V143P == V143 salida ENTERA (N 9, s {seed}, T {T}, fundador limpio)", N(run(V143P)) == rv)
    chk(f"(2) O1P == O1 salida ENTERA", N(run(O1P)) == ro)

    def hib(**p):
        HIB.PUENTES = dict(patas=0, boca_buena=0, boca_mala=0, memoria=0); HIB.PUENTES.update(p); return N(run(HIB))
    h0 = hib()
    chk("(3) HIB todo en 0 == V143 en todo salvo d['carro']", sin(h0, ('carro',)) == sin(rv, ('carro',)))
    h1 = hib(patas=1, boca_buena=1, boca_mala=1)
    chk("(4) HIB patas+boca_buena+boca_mala == O1 en todo salvo d['carro'] y exp_hasta", sin(h1, ('carro', 'exp_hasta')) == sin(ro, ('carro', 'exp_hasta')))
    fis = lambda r: [{k: d[k] for k in ('descendientes', 'deaths', 'vidas_h1', 'mord', 'fundadores')} for d in r['linajes']]
    for p in ('patas', 'boca_buena', 'boca_mala', 'memoria'):
        hp = hib(**{p: 1}); hp2 = hib(**{p: 1})
        tel = [d['carro']['hib'] for d in hp['linajes']]
        chk(f"(5) puente {p} solo NO es inerte (fisica distinta de V143)", fis(hp) != fis(rv))
        chk(f"(6) puente {p} determinista (dos corridas iguales)", hp == hp2)
        s = {k: sum(t[k] for t in tel) for k in tel[0]}
        print(f"       telemetria hib {p}: {s}")
    print(f"ARNES {'PASA' if ok else 'FALLA'} · {time.time()-t0:.0f}s")
    return 0 if ok else 1


if __name__ == '__main__':
    sys.exit(main())
