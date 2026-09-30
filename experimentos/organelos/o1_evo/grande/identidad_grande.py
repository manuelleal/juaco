"""identidad_grande.py — ARNES del mundo grande (pista_grande.py + corre_grande.tarea). UN proceso, 6 corridas, 18 000 pasos.
Salida ENTERA en identidad_grande_salida.txt (python identidad_grande.py > identidad_grande_salida.txt).

MISION: llegar a la AGI por este camino.

I1  REGLA 14 + FABRICA: corre_grande.tarea(mundo de fabrica: G 1, sin cosas) == corre_v143.tarea, salida resumida ENTERA y crudo de la pista
    ENTERO (incluye el estado final del rng del mundo), 9 TPATAS_3 (el carro con mas caminos: valor_nec, veto, rng), fundador limpio.
I2  TAMANO: pista_grande.run(G = 2) con 4 carros == pista.run(mundo_n = 8) con los mismos 4 carros (O1): esc * G es exactamente el mundo
    forzado de la ENMIENDA 4 (L, nobj, sorteos de olvido). Salida ENTERA salvo pista['grande'] (== {'G': 2}) y mundo_n.
I3  PLACEBO (control que debe dar IGUAL): oasis y pantano DEFINIDOS pero rica_extra = 0 y lento_tasa = 0 -> el crudo es el de I1 salvo las
    claves nuevas; y los ganchos SI se ejercitaron (hubo mordidas en las zonas).
C1  LAS COSAS ACTUAN (control que debe DIFERIR): rica = lento = 1 -> el crudo DIFIERE del de I1; con un espia en resultado(): toda mordida
    de A o C en el oasis se reporto (0.8, 0.8); toda otra mordida, el nominal; hubo cargas y drenado > 0.
U   UNIDAD de Geografia (sin corridas): efectos por letra y zona, drenado EXACTO (tasa por carga activa durante dur pasos, total 1.0),
    la carga muere con el cuerpo, zonas disjuntas de W = L/10, zonas sorteadas por semilla (no sitios fijos) y deterministas.
Semillas: 718080-718089 (arnes). T 3000.
"""
import copy, json, os, sys, time, types
import numpy as np

AQUI = os.path.dirname(os.path.abspath(__file__))
if AQUI not in sys.path: sys.path.insert(0, AQUI)
import corre_grande as CG
PG = CG.PG; P = CG.P; CV = CG.CV

N = lambda x: json.dumps(x, default=str, sort_keys=True)
SEED = 718080; T = 3000
RES = []


def chk(nombre, ok, extra=''):
    RES.append((nombre, bool(ok))); print(f"  [{'OK' if ok else 'FALLA'}] {nombre} {extra}", flush=True)


def sin_nuevas(r):
    r = copy.deepcopy(r); r['pista'].pop('grande', None)
    for d in r['linajes']: d['_carrera'].pop('grande', None)
    return r


def unidad():
    print("U  unidad de Geografia")
    L = 720
    class Lf:  # linaje falso
        def __init__(s, i): s.i = i; s.E = 1.0
    g = PG.Geografia(SEED, L, 2, 1000, 1, 1, 0.8, 0.0025, 400)
    oa = sorted(g.oasis); pa = sorted(g.pantano)
    chk("U1 zonas de W = L/10 = 72, disjuntas, pantano opuesto", len(g.oasis) == 72 and len(g.pantano) == 72 and not (g.oasis & g.pantano)
        and ((g.z0 + L // 2) % L) in g.pantano, f"z0 {g.z0}")
    xo = next(iter(g.oasis)); xp = next(iter(g.pantano)); xr = next(x for x in range(L) if x not in g.oasis and x not in g.pantano)
    l0 = Lf(0)
    e = {k: g.muerde(l0, k, xo, 0, CG.P.cfg_fabrica()['EFECTO'][CG.P.cfg_fabrica()['VAL_VIVO'][k]]) for k in 'ABCD'}
    chk("U2 oasis: A y C -> (0.8, 0.8); B y D nominales", e['A'] == (0.8, 0.8) and e['C'] == (0.8, 0.8) and e['B'] == (-0.4, 0.0) and e['D'] == (0.0, -0.4), str(e))
    e2 = {k: g.muerde(l0, k, xr, 0, CG.P.cfg_fabrica()['EFECTO'][CG.P.cfg_fabrica()['VAL_VIVO'][k]]) for k in 'ABCD'}
    chk("U3 fuera de las zonas: todo nominal y sin carga", e2 == {'A': (0.8, 0.0), 'B': (-0.4, 0.0), 'C': (0.0, 0.8), 'D': (0.0, -0.4)} and not g.cargas[0], str(e2))
    l1 = Lf(1)
    ea = g.muerde(l1, 'A', xp, 10, (0.8, 0.0)); eb = g.muerde(l1, 'B', xp, 10, (-0.4, 0.0))
    chk("U4 pantano: A nominal inmediato + 1 carga; B nominal sin carga", ea == (0.8, 0.0) and eb == (-0.4, 0.0) and g.cargas[1] == [410])
    E0 = l1.E; pasos = 0
    for t in range(10, 1000):
        e_antes = l1.E; g.costo(l1, t)
        if l1.E != e_antes: pasos += 1
    chk("U5 drenado exacto: 400 pasos (t 10..409) x 0.0025 = 1.0", pasos == 400 and abs((E0 - l1.E) - 1.0) < 1e-9 and abs(g.drenado[1] - 1.0) < 1e-9,
        f"pasos {pasos} drenado {E0 - l1.E:.12f}")
    g.muerde(l1, 'C', xp, 2000, (0.0, 0.8)); g.muerde(l1, 'A', xp, 2000, (0.8, 0.0)); E1 = l1.E; g.costo(l1, 2000)
    chk("U6 cargas acumulables: 2 cargas -> 0.005 por paso", abs((E1 - l1.E) - 0.005) < 1e-12 and g.max_cargas[1] == 2)
    g.muere(l1, 2001, True); E2 = l1.E; g.costo(l1, 2002)
    chk("U7 la carga muere con el cuerpo (y se cuenta la muerte con carga)", g.cargas[1] == [] and l1.E == E2 and g.muertes_carga[1] == 1 and g.muertes[1] == 1)
    zs = [PG.Geografia(s, L, 1, 10, 1, 1, 0.8, 0.0025, 400).z0 for s in range(718080, 718090)]
    zs2 = [PG.Geografia(s, L, 1, 10, 1, 1, 0.8, 0.0025, 400).z0 for s in range(718080, 718090)]
    chk("U8 zonas por semilla: deterministas y NO fijas (10 semillas, >= 8 inicios distintos)", zs == zs2 and len(set(zs)) >= 8, str(zs))
    g0 = PG.Geografia(SEED, L, 1, 10, 1, 0, 0.8, 0.0025, 400); g1 = PG.Geografia(SEED, L, 1, 10, 0, 1, 0.8, 0.0025, 400)
    chk("U9 solo rica: sin pantano; solo lento: sin oasis; el pantano no depende de rica", not g0.pantano and not g1.oasis and g1.pantano == g.pantano)


def main():
    t0 = time.time()
    print(f"IDENTIDAD_GRANDE · python {sys.version.split()[0]} · numpy {np.__version__} · corre_grande.py {CG.h16(CG.__file__)} · "
          f"pista_grande.py {CG.h16(PG.__file__)} · seed {SEED} · T {T}")
    ok = CG.verifica(print, False); chk("V0 shas de origen y anclas", ok)
    unidad()
    # ---------------- I1
    print("I1 regla 14 + fabrica (TPATAS_3 x9)")
    CG.fija('pc'); cap = []; orig = P.run
    def spy(*a, **k):
        r = orig(*a, **k); cap.append(r); return r
    P.run = spy
    try:
        a = CV.tarea((SEED, 'TPATAS_3', T))
    finally:
        P.run = orig
    base = cap[0]
    b = CG.tarea(SEED, 'pc', T, mundo='fabrica'); rb = b.pop('_crudo')
    a.pop('seg'); b.pop('seg'); ex = {k: b.pop(k) for k in ('grande', 'tel_ps', 'estado')}
    chk("I1a tarea(fabrica) == corre_v143.tarea (resumen ENTERO)", N(a) == N(b))
    chk("I1b crudo pista_grande == pista.run (ENTERO, rng del mundo incluido)", N(base) == N(rb), f"rng {base['pista']['rng_mundo_estado']} / {rb['pista']['rng_mundo_estado']}")
    chk("I1c sin claves nuevas con el mundo de fabrica", 'grande' not in rb['pista'] and all('grande' not in d['_carrera'] for d in rb['linajes'])
        and ex['grande']['pista'] is None)
    # ---------------- I2
    print("I2 tamano: G = 2 con 4 carros == pista.run(mundo_n = 8)")
    o1 = CV.modulo('O1'); cs = [('O1', o1)] * 4
    ra = P.run(SEED + 1, cs, T=T, pizarra=1, fundador_limpio=1, mundo_n=8)
    rg = PG.run(SEED + 1, cs, T=T, pizarra=1, fundador_limpio=1, G=2)
    gp = rg['pista'].pop('grande'); ra['pista'].pop('mundo_n'); rg['pista'].pop('mundo_n')
    chk("I2 salida ENTERA igual (salvo mundo_n) y pista['grande'] == {'G': 2}", N(ra) == N(rg) and gp == {'G': 2}, f"L {rg['pista']['L']} nobj {rg['pista']['nobj']}")
    # ---------------- I3
    print("I3 placebo: zonas definidas, efectos 0 (TPATAS_3 x9)")
    CG.fija('pc'); mod = CV._MODS['TPATAS_3']
    rp = PG.run(SEED, [('TPATAS_3', mod)] * 9, T=T, pizarra=1, rep_acum=0, escala=1, mundo_n=None, fundador_limpio=1, G=1, rica=1, lento=1,
                rica_extra=0.0, lento_tasa=0.0)
    zo = sum(d['_carrera']['grande']['mord_oasis']['A'] + d['_carrera']['grande']['mord_oasis']['C'] for d in rp['linajes'])
    zp = sum(sum(d['_carrera']['grande']['mord_pantano'].values()) for d in rp['linajes'])
    chk("I3a placebo == fabrica (crudo ENTERO sin las claves nuevas)", N(sin_nuevas(rp)) == N(base))
    chk("I3b los ganchos se ejercitaron (mordidas en oasis y pantano > 0; cargas 0)", zo > 0 and zp > 0
        and all(d['_carrera']['grande']['cargas'] == 0 for d in rp['linajes']), f"A+C oasis {zo} · pantano {zp}")
    # ---------------- C1
    print("C1 las cosas actuan (TPATAS_3 x9, rica = lento = 1, G = 1 para comparar con I1), espia en resultado()")
    vistas = []

    def crea_espia(ctx):
        c = mod.crea(ctx); f = c.resultado
        def res(r):
            if r['mordio']: vistas.append((r['pos'], r['letra'], tuple(r['dS'])))
            return f(r)
        c.resultado = res; return c
    esp = types.SimpleNamespace(crea=crea_espia)
    rc = PG.run(SEED, [('TPATAS_3', esp)] * 9, T=T, pizarra=1, rep_acum=0, escala=1, mundo_n=None, fundador_limpio=1, G=1, rica=1, lento=1)
    gi = rc['pista']['grande']; L = rc['pista']['L']
    oasis = {(gi['z0'] + j) % L for j in range(gi['W'])}
    ef = P.cfg_fabrica(); nom = {k: tuple(ef['EFECTO'][ef['VAL_VIVO'][k]]) for k in 'ABCD'}
    mal = [v for v in vistas if (v[2] != (0.8, 0.8) if (v[0] in oasis and v[1] in 'AC') else v[2] != nom[v[1]])]
    n_oa = sum(1 for v in vistas if v[0] in oasis and v[1] in 'AC')
    cg = sum(d['_carrera']['grande']['cargas'] for d in rc['linajes']); dr = sum(d['_carrera']['grande']['drenado'] for d in rc['linajes'])
    chk("C1a el crudo DIFIERE de fabrica (sin las claves nuevas)", N(sin_nuevas(rc)) != N(base))
    chk("C1b dS reportado: (0.8, 0.8) en A/C del oasis, nominal en el resto", not mal and n_oa > 0, f"mordidas {len(vistas)} · A/C en oasis {n_oa} · mal {mal[:3]}")
    chk("C1c veneno lento: cargas > 0 y drenado > 0 (<= 1.0 por carga)", cg > 0 and 0 < dr <= cg * 1.0 + 1e-9, f"cargas {cg} drenado {dr:.4f}")
    print(f"  mundo C1: {gi}")
    nf = sum(1 for _, o in RES if not o)
    print(f"ARNES: {len(RES) - nf}/{len(RES)} OK · {'TODO OK' if nf == 0 else 'HAY FALLAS'} · {time.time() - t0:.1f}s")
    return 0 if nf == 0 else 1


if __name__ == '__main__':
    sys.exit(main())
