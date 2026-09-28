# EXPLORATORIO, no es dato
"""identidad_bb.py — arnes del instrumento boca_buena (un proceso, N 9, fundador limpio, T corto). Se corre ANTES de mirar numeros.

MISION: llegar a la AGI por este camino.
  (K) construye_bb.py --verifica: carros en disco == construidos por anclas; shas de origen
  (1) HIBB (BB 'ref', puente boca_buena) == HIB del puenteo (boca_buena) en TODO salvo d['carro'], y d['carro'] igual salvo bb/bbt
  (2) HIBB con todos los puentes en 0 == V143 (bundle/tronco_v14_3/carros_v143/V143.py) en todo salvo d['carro']
  (3) HIBB (BB 'glotu', puente boca_buena) == V143_GLOTU (muro/carros) en todo salvo d['carro']  (la traduccion GLOTU es la misma)
  (4) cada modo BB es determinista (dos corridas iguales); informativo: si cambia la fisica respecto de 'ref'
  (5) la letra de _bb en casos sinteticos
  (6) regla 14: los argumentos de pista.run de corre_bb == los de corre_v143.tarea (campo a campo)
Uso: python identidad_bb.py [--T 2000] [--seed 39901]   (salida -> identidad_bb_salida.txt la pega el creador)
"""
import argparse, json, os, subprocess, sys, time, importlib.util
import numpy as np

AQUI = os.path.dirname(os.path.abspath(__file__))
ORG = os.path.dirname(AQUI)
RAIZ = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(ORG))), 'bundle')   # JUACO/bundle
PISTA = os.path.join(RAIZ, 'experimentos', 'carrera_escuderias')
V143D = os.path.join(RAIZ, 'experimentos', 'tronco_v14_3', 'carros_v143')
sys.path.insert(0, PISTA); sys.path.insert(0, AQUI)
import pista as P
import corre_bb as CB


def carga(ruta, nombre):
    spec = importlib.util.spec_from_file_location(nombre, ruta); m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m


N = lambda x: json.loads(json.dumps(x, default=str))


def sin(r, claves):
    out = dict(r); out['linajes'] = [{k: v for k, v in d.items() if k not in claves} for d in r['linajes']]; return out


def main():
    ap = argparse.ArgumentParser(allow_abbrev=False)
    ap.add_argument('--T', type=int, default=2000); ap.add_argument('--seed', type=int, default=39901)
    a = ap.parse_args()
    T, seed = a.T, a.seed
    ok = True; t0 = time.time()

    def chk(nombre, cond, inf=False):
        nonlocal ok
        if not inf: ok &= bool(cond)
        print(f"  {'OK   ' if cond else ('info ' if inf else 'FALLA')} {nombre}", flush=True)

    rc = subprocess.run([sys.executable, os.path.join(AQUI, 'construye_bb.py'), '--verifica'], capture_output=True, text=True)
    print(rc.stdout.rstrip())
    chk("(K) construye_bb --verifica (carros por anclas == disco; shas de origen)", rc.returncode == 0)

    run = lambda m: P.run(seed, [('C', m)] * 9, T=T, **CB.RUN_KW)
    HIB = carga(os.path.join(ORG, 'comite2', 'puenteo', 'carros', 'HIB.py'), 'HIB_orig')
    HIBB = carga(os.path.join(AQUI, 'carros', 'HIBB.py'), 'HIBB')
    V143 = carga(os.path.join(V143D, 'V143.py'), 'V143')
    GLOTU = carga(os.path.join(ORG, 'muro', 'carros', 'V143_GLOTU.py'), 'V143_GLOTU')

    def hibb(bb, **p):
        HIBB.PUENTES = dict(patas=0, boca_buena=0, boca_mala=0, memoria=0); HIBB.PUENTES.update(p); HIBB.BB = bb; return N(run(HIBB))

    HIB.PUENTES = dict(patas=0, boca_buena=1, boca_mala=0, memoria=0); rh = N(run(HIB))
    rref = hibb('ref', boca_buena=1)
    chk(f"(1) HIBB ref == HIB boca_buena del puenteo, todo salvo d['carro'] (N 9, s {seed}, T {T})", sin(rref, ('carro',)) == sin(rh, ('carro',)))
    cc = lambda r: [{k: v for k, v in d['carro'].items() if k not in ('bb', 'bbt')} for d in r['linajes']]
    chk("(1b) ... y d['carro'] igual salvo bb/bbt", cc(rref) == cc(rh))
    rv = N(run(V143)); r0 = hibb('ref')
    chk("(2) HIBB todos los puentes en 0 == V143 en todo salvo d['carro']", sin(r0, ('carro',)) == sin(rv, ('carro',)))
    rg = N(run(GLOTU)); rhg = hibb('glotu', boca_buena=1)
    chk("(3) HIBB glotu == V143_GLOTU (muro) en todo salvo d['carro']", sin(rhg, ('carro',)) == sin(rg, ('carro',)))
    fis = lambda r: [{k: d[k] for k in ('descendientes', 'deaths', 'vidas_h1', 'mord', 'fundadores')} for d in r['linajes']]
    for bb in HIBB.BB_MODOS:
        x1 = hibb(bb, boca_buena=1); x2 = hibb(bb, boca_buena=1)
        chk(f"(4) BB {bb} determinista", x1 == x2)
        if bb != 'ref': chk(f"(4i) BB {bb} cambia la fisica respecto de ref a T {T}", fis(x1) != fis(rref), inf=True)
        s = {}
        for d in x1['linajes']:
            for k, v in d['carro']['bbt'].items(): s[k] = s.get(k, 0) + v
        print(f"       bbt {bb}: {s}")

    # (5) la letra, en casos sinteticos (un Carro de HIBB sin correr la pista)
    ctx = dict(L=360, rep_umbral=1.0, rng=np.random.default_rng(0), id='x', T=1000, fabrica=P.cfg_fabrica(), dote=0.6, costo=0.001,
               costo_a=0.001, rep_X=500, indice=0, n_linajes=1, PAT=P.cfg_fabrica()['PAT'], cupo=16, ancho=8)
    casos = [  # (modo, letra conocida con v, lev, mo, mv, esperado)
        ('ref', (0.8, 0.0), (1.3, 0.5), False, True, False),
        ('veto', (0.8, 0.0), (1.3, 0.5), False, True, False), ('veto', (0.8, 0.0), (0.5, 0.5), True, False, False),
        ('fuerza', (0.8, 0.0), (0.5, 0.5), True, False, True), ('fuerza', (0.8, 0.0), (1.3, 0.5), False, True, True),
        ('m0', (0.8, 0.0), (1.1, 0.5), True, True, False), ('m0', (0.8, 0.0), (0.9, 1.4), False, False, True),
        ('vetom0', (0.8, 0.0), (1.1, 0.5), True, True, False), ('vetom0', (0.8, 0.0), (0.9, 1.4), True, False, False),
        ('vetom0', (0.8, 0.0), (0.9, 1.4), False, True, True),
        ('glotu', (0.8, 0.0), (1.1, 0.5), True, True, False), ('glotu', (0.8, 0.0), (1.3, 1.4), False, True, True),
        ('glotu', (0.8, 0.0), (0.9, 0.5), False, True, True),
        ('sinprueba', None, (0.3, 0.3), False, True, True), ('soloprueba', None, (0.3, 0.3), False, True, False),
        ('soloprueba', (0.8, 0.0), (1.3, 0.5), False, True, True),
        ('todo', (0.8, 0.0), (1.45, 1.45), False, False, True), ('todo', None, (0.3, 0.3), False, True, False),
        ('m0', (0.8, 0.0), (1.0, 0.5), True, True, False),
        ('vetoc', (0.8, 0.0), (1.3, 0.5), False, True, False), ('vetoc', None, (0.3, 0.3), False, True, True),
        ('fuerzac', (0.8, 0.0), (0.5, 0.5), True, False, True), ('fuerzac', None, (0.6, 0.6), True, False, False),
        ('m10', (0.8, 0.0), (1.05, 0.5), False, False, True), ('m10', (0.8, 0.0), (1.15, 0.5), True, True, False),
        ('m40', (0.8, 0.0), (1.35, 0.5), False, False, True), ('m40', (0.8, 0.0), (1.45, 0.5), True, True, False),
        ('ventana', (0.8, 0.0), (1.45, 1.45), False, False, True), ('tinv', (0.8, 0.0), (0.5, 1.4), True, True, False),
        ('tinv', (0.8, 0.0), (1.4, 0.5), False, False, True),
        ('tinv40', (0.8, 0.0), (0.5, 1.35), False, False, True), ('tinv40', (0.8, 0.0), (0.5, 1.45), True, True, False),
    ]
    bien = 0
    for modo, v, lev, mo, mv, esp in casos:
        HIBB.BB = modo; c = HIBB.Carro(ctx)
        if v is not None: c.o.suma['A'] = np.asarray(v, float); c.o.n['A'] = 1
        got = c._bb('A', lev, mo, mv); bien += int(got == esp)
        if got != esp: print(f"       caso {modo} v={v} lev={lev} mo={mo} mv={mv}: {got} (esperado {esp})")
    chk(f"(5) letra de _bb en {len(casos)} casos sinteticos ({bien}/{len(casos)})", bien == len(casos))
    HIBB.BB = 'ref'

    # (6) regla 14
    r14 = CB.regla14()
    chk(f"(6) regla 14: pista.run de corre_bb == corre_v143.tarea campo a campo {r14}", r14['ok'])
    print(f"ARNES {'PASA' if ok else 'FALLA'} · {time.time()-t0:.0f}s")
    return 0 if ok else 1


if __name__ == '__main__':
    sys.exit(main())
