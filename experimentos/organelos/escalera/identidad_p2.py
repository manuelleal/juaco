"""identidad_p2.py — ARNES MINIMO del peldano 2 (colonia pegada + cuello). Un proceso; semillas 739550-739589. NADA de aqui es dato.
(I1) mundo pega 0 cuello 0 == motor_convive.run_solapadas BIT A BIT (salida entera + estado final del rng del mundo), 9 O1.
(I2) pega 1 cuello 0: se forman grupos (grupos fundados > 0, tam_max >= 2, pasos pegado > 0) y la fisica != base (control que puede fallar).
(I3) pega 1 cuello 2000 p_suelto 0.0: el cuello sortea pero no mata: fisica == pega 1 cuello 0 (su rng es propia, no toca el motor).
(I4) pega 0 cuello 2000 p_suelto 0.5: mata (muertes por cuello > 0, todas de sueltos) y la fisica != base.
(I5) pega 1 cuello 2000: muertes por cuello de pegados < de sueltos en proporcion (la formula p/k actua): se reporta.
(I6) trabajo() escribe su JSON y --reanuda lo relee igual.
"""
import copy, json, os, sys, tempfile, time

AQUI = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, AQUI)
import corre_p2 as CO
MCO = CO.MCO
import motor_convive as MC

N = lambda x: json.loads(json.dumps(x, default=str))
OK = [True]; NCHK = [0, 0]


def chk(nombre, c):
    c = bool(c); OK[0] &= c; NCHK[0] += 1; NCHK[1] += int(c); print(f"  {'OK   ' if c else 'FALLA'} {nombre}", flush=True)


def fis(r):
    r = copy.deepcopy(r)
    for d in r['linajes']: d['_carrera'].pop('colonia', None)
    r['pista'].pop('colonia', None)
    return N(r)


def run(seed, T, **k): return N(MCO.run(seed, [('O1', CO.carro())] * 9, T=T, **CO.KW, **k))


t0 = time.time()
print("ARNES identidad_p2.py")
print('  mundo_colonia:', MCO.construye()[1])
S, T = 739551, 4000
base = N(MC.run_solapadas(S, [('O1', CO.carro())] * 9, T=T, **CO.KW))
r0 = run(S, T, pega=0, cuello=0)
chk(f"(I1) pega 0 cuello 0 == motor_convive.run_solapadas BIT A BIT (salida entera, 9 O1, s {S}, T {T}) y mismo rng final del mundo",
    r0 == base and r0['pista']['rng_mundo_estado'] == base['pista']['rng_mundo_estado'])
r1 = run(S, T, pega=1, cuello=0); c1 = r1['pista']['colonia']; cl1 = [d['_carrera']['colonia'] for d in r1['linajes']]
chk(f"(I2) pega 1 cuello 0: grupos fundados {sum(c['grupos_fundados'] for c in cl1)} > 0, tam_max {max(c['tam_max'] for c in cl1)} >= 2, pasos pegado "
    f"{sum(c['pasos_pegado'] for c in cl1)} > 0, grupos vivos {c1['grupos_vivos']} (tamanos {c1['tam_grupos_vivos'][:8]}); y la fisica != base",
    sum(c['grupos_fundados'] for c in cl1) > 0 and max(c['tam_max'] for c in cl1) >= 2 and sum(c['pasos_pegado'] for c in cl1) > 0 and fis(r1) != fis(base))
r2 = run(S, T, pega=1, cuello=2000, p_suelto=0.0)
chk("(I3) pega 1 cuello 2000 p_suelto 0.0: sortea (cuellos > 0) pero no mata; fisica == pega 1 cuello 0", r2['pista']['colonia']['cuellos'] > 0
    and r2['pista']['colonia']['muertes_cuello'] == 0 and fis(r2) == fis(r1))
r3 = run(S, T, pega=0, cuello=2000, p_suelto=0.5); c3 = r3['pista']['colonia']; cl3 = [d['_carrera']['colonia'] for d in r3['linajes']]
chk(f"(I4) pega 0 cuello 2000 p 0.5: muertes por cuello {c3['muertes_cuello']} > 0 (de {c3['candidatos']} candidatos en {c3['cuellos']} cuellos), ninguna de pegados, fisica != base",
    c3['muertes_cuello'] > 0 and sum(c['muertes_cuello_pegado'] for c in cl3) == 0 and fis(r3) != fis(base))
r4 = run(S, T, pega=1, cuello=2000, p_suelto=0.5); c4 = r4['pista']['colonia']; cl4 = [d['_carrera']['colonia'] for d in r4['linajes']]
mp = sum(c['muertes_cuello_pegado'] for c in cl4); mt = c4['muertes_cuello']
chk(f"(I5) pega 1 cuello 2000 p 0.5: muertes por cuello {mt} (pegados {mp}) de {c4['candidatos']} candidatos; tam grupos vivos {c4['tam_grupos_vivos'][:8]}; fisica != I2 y != I4",
    fis(r4) != fis(r1) and fis(r4) != fis(r3))
with tempfile.TemporaryDirectory() as td:
    x1 = CO.trabajo((0, 'peg', 739560, 2500, td, False, 2000, 0.5)); x2 = CO.trabajo((0, 'peg', 739560, 2500, td, True, 2000, 0.5))
    chk(f"(I6) trabajo peg sin aborto ({x1['aborto']}), fila con colonia y estado {x1.get('estado', {}).get('mundo')}; --reanuda relee igual",
        x1['aborto'] is None and x1.get('colonia') and x1['estado']['mundo'] == dict(pega=1, cuello=2000, p_suelto=0.5)
        and N({k: v for k, v in x1.items() if k != 'seg'}) == N({k: v for k, v in x2.items() if k != 'seg'}))
print(f"\nARNES {'PASA' if OK[0] else 'FALLA'}, {NCHK[1]}/{NCHK[0]} · {time.time() - t0:.1f}s")
sys.exit(0 if OK[0] else 1)
