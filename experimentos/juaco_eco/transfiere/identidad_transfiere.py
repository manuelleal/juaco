"""identidad_transfiere.py — ARNES de ECO-T (corre_transfiere.py). Un proceso, sin Pool. Nube, 24-sep-2026.

MISION: llegar a la AGI por este camino.

  (I) la colonia con 9 copias de G0 == FABRICA de la carrera en TODA la fisica (T 3000, semillas de practica 29490 y 29491).
  (A) el genoma llega a su linea: con alpha x2 y aversion x1.5 en la linea 3, el carro de esa linea tiene ALPHA 2.4 y AVERSION 1.5 y los
      otros 8 los de fabrica; en las 9 la historia de vida (dote, rep_umbral, rep_X) del ctx queda como la pone la pista.
  (B) el muestreo: 9 entradas del banco con el rng [c, 7] (y [c, 8] el placebo: otros indices), historia de vida en G0, determinista.
  (V) la letra en entradas sinteticas.
  (R) banderas malas abortan (ERR-115); un subproceso con bandera desconocida sale con codigo != 0 sin escribir nada.
Escribe identidad_transfiere_salida.txt.
"""
import contextlib, glob, io, json, os, subprocess, sys, time, types
import numpy as np

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
R_ = []


def chk(nombre, ok, det=''):
    R_.append(bool(ok)); print(f"  {'OK ' if ok else 'MAL'} {nombre} {det}", flush=True)


def fisica(r):
    return (json.dumps([{k: v for k, v in d.items() if k != 'carro'} for d in r['linajes']], sort_keys=True, default=str),
            json.dumps(r['pista'], sort_keys=True, default=str))


def main():
    import corre_transfiere as X
    P, ME = X.P, X.ME
    t0 = time.time()
    print(f"IDENTIDAD ECO-T · {time.strftime('%Y-%m-%d %H:%M:%S')} · python {sys.version.split()[0]} · shas {X.SHAS()}")
    # (I)
    for c in (29490, 29491):
        a = P.run(c, [('F', X.fab())] * 9, T=3000, pizarra=1, rep_acum=0, escala=1, mundo_n=None, fundador_limpio=1)
        b = P.run(c, [('F', X.modulo_colonia(np.tile(X.G0, (9, 1))))] * 9, T=3000, pizarra=1, rep_acum=0, escala=1, mundo_n=None, fundador_limpio=1)
        chk(f"(I) c{c}: colonia de 9 x G0 == FABRICA en toda la fisica", fisica(a) == fisica(b))
    # (A)
    G = np.tile(X.G0, (9, 1)); ia = X.ME.NOMBRES.index('alpha'); iv = X.ME.NOMBRES.index('aversion')
    G[3, ia] *= 2.0; G[3, iv] *= 1.5
    cap = {}; base = X.modulo_colonia(G, 'A')
    m = types.ModuleType('carro_cap')

    def crea(ctx):
        car = base.crea(ctx); cap[ctx['indice']] = (car, dict(dote=ctx['dote'], rep_umbral=ctx['rep_umbral'], rep_X=ctx['rep_X'])); return car
    m.crea = crea
    P.run(29492, [('A', m)] * 9, T=5, pizarra=1, rep_acum=0, escala=1, mundo_n=None, fundador_limpio=1)
    ok = (abs(cap[3][0].ALPHA - 2.4) < 1e-12 and abs(cap[3][0].AVERSION - 1.5) < 1e-12 and
          all(abs(cap[i][0].ALPHA - 1.2) < 1e-12 and abs(cap[i][0].AVERSION - 1.0) < 1e-12 for i in range(9) if i != 3) and
          all(cap[i][1] == dict(dote=0.6, rep_umbral=1.0, rep_X=500) for i in range(9)))
    chk("(A) el genoma llega a su linea (linea 3: ALPHA 2.4, AVERSION 1.5; las demas de fabrica; historia de vida intacta)", ok,
        f"(ALPHA {[round(cap[i][0].ALPHA, 3) for i in range(9)]})")
    # (B)
    vdir = X.VENTANAS['serie'][1]
    bk = X.banco(vdir, 'VIDA', 19401)
    g7 = X.genomas(bk, 29401, 7); g8 = X.genomas(bk, 29401, 8); g7b = X.genomas(bk, 29401, 7)
    i7 = np.random.default_rng([29401, 7]).choice(len(bk), 9, replace=False); i8 = np.random.default_rng([29401, 8]).choice(len(bk), 9, replace=False)
    chk("(B) muestreo: 9 del banco con [c, 7], placebo [c, 8] con otros indices, historia en G0, determinista",
        g7.shape == (9, 18) and np.array_equal(g7, g7b) and not np.array_equal(i7, i8) and np.allclose(g7[:, X.HISTORIA], X.G0[X.HISTORIA]) and
        np.array_equal(np.delete(g7, X.HISTORIA, 1), np.delete(bk[i7], X.HISTORIA, 1)),
        f"(banco {bk.shape}; log(alpha/G0) mediano en la muestra {np.median(np.log(g7[:, ia] / X.G0[ia])):.3f})")
    # (V)
    def fake(wva, wvg, plac_w=10, plac_e=0, incompleta=False):
        R = []
        for i in range(20):
            s = 19401 + i
            R.append(dict(eco_semilla=s, brazo='VIDA', R0_real_med=0.5, persisten=3))
            R.append(dict(eco_semilla=s, brazo='AZAR', R0_real_med=(0.4 if i < wva else 0.6), persisten=2))
            R.append(dict(eco_semilla=s, brazo='G0', R0_real_med=(0.4 if i < wvg else 0.6), persisten=1))
            R.append(dict(eco_semilla=s, brazo='VIDA_P', R0_real_med=(0.4 if i < plac_w else (0.5 if i < plac_w + plac_e else 0.6)), persisten=3))
        return R[:-1] if incompleta else R
    casos = [("TRANSFIERE", fake(15, 15), 'TRANSFIERE'), ("MODESTO (T1 cae: 14)", fake(14, 16), 'HAY ALGO MODESTO (en esta serie): mejor que G0'),
             ("MODESTO (T2 cae)", fake(16, 12), 'HAY ALGO MODESTO (en esta serie): mejor que la deriva'), ("NO", fake(10, 10), 'NO (en'),
             ("placebo 16 -> NO EVALUABLE", fake(15, 15, plac_w=16), 'NO EVALUABLE (el placebo'),
             ("placebo 10 + 10 empates = 15 -> valido", fake(15, 15, plac_w=10, plac_e=10), 'TRANSFIERE'),
             ("placebo 4 -> NO EVALUABLE", fake(15, 15, plac_w=4), 'NO EVALUABLE (el placebo'),
             ("incompleta", fake(15, 15, incompleta=True), 'NO EVALUABLE (serie')]
    for nombre, R, esp in casos:
        v, L, d = X.veredicto(R, 20)
        chk(f"(V) {nombre}", v.startswith(esp), f"-> {v}")
    # (R)
    malas = [['--help'], ['-h'], [], ['--serie'], ['--serie', '--ventana', 'serie'], ['--serie', '--ventana', 'otra', '--pool', '3'],
             ['--serie', '--ventana', 'serie', '--pool', '4'], ['--serie', '--ventana=serie', '--pool', '3'], ['--humo', '--pool', '2'],
             ['--humo', '--humo'], ['--lee', 'x', '--pool', '3'], ['--serie', '--vent', 'serie', '--pool', '3']]
    n_ab = 0
    for mm in malas:
        try: X.parsea(mm)
        except X.BanderaMala: n_ab += 1
    chk(f"(R) el parser aborta ante {len(malas)} formas malas", n_ab == len(malas), f"({n_ab}/{len(malas)})")
    antes = set(glob.glob(os.path.join(AQUI, 'datos', '**', '*'), recursive=True))
    pr = subprocess.run([sys.executable, os.path.join(AQUI, 'corre_transfiere.py'), '--serie', '--ventana', 'serie', '--pool', '3', '--nada'],
                        capture_output=True, text=True, timeout=120)
    despues = set(glob.glob(os.path.join(AQUI, 'datos', '**', '*'), recursive=True))
    chk("(R) subproceso con bandera desconocida: codigo != 0 y no escribe nada", pr.returncode != 0 and antes == despues, f"(codigo {pr.returncode})")
    n = sum(R_)
    print(f"RESULTADO: {n}/{len(R_)}  ({time.time() - t0:.0f} s)")
    return n == len(R_)


if __name__ == '__main__':
    buf = io.StringIO()

    class Tee:
        def write(self, x): sys.__stdout__.write(x); buf.write(x)
        def flush(self): sys.__stdout__.flush()
        def reconfigure(self, **kw): pass
    with contextlib.redirect_stdout(Tee()):
        ok = main()
    open(os.path.join(AQUI, 'identidad_transfiere_salida.txt'), 'w', encoding='utf-8').write(buf.getvalue())
    sys.exit(0 if ok else 1)
