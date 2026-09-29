"""identidad_bloques6.py — arnes de la inversion en el nucleo (Opus M, 28-sep-2026). Un proceso; semillas 48685-48688. Mision: llegar a la AGI.
(K) anclas y shas. (A) inv 0 y inv 1: motor_bloques6 == motor_bloques5 BIT A BIT. (B) inv 2 con periodo 20 000 == inv 1 (Python) con periodo
20 000, BIT A BIT (la inversion en el nucleo cae en el mismo momento). (C) periodo 500 != sin inversion. (D) determinismo periodo 500.
"""
import json, os, subprocess, sys, time
AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
import corre_bloques6 as C6   # noqa: E402
C5 = C6.C5; CB = C6.CB; NS = C6.NS
CAR = os.path.join(AQUI, 'datos', 'arnes6')
LOG = []


def p(*a):
    s = ' '.join(str(x) for x in a); print(s, flush=True); LOG.append(s)


def ok(nombre, cond, info=''):
    p(f"  [{'OK ' if cond else 'MAL'}] {nombre} {info}"); return bool(cond)


def run(motor, seed, brazo, extra=None, car='x', TT=30000):
    MB = C5.usa_bloques5() if motor == 5 else C6.usa_bloques6()
    MB.BQ_CFG.clear(); MB.BQ_CFG.update(CB.DEF); MB.BQ_CFG.update(CB.BQ[brazo]); MB.BQ_CFG.update(extra or {})
    r = NS.trabajo((seed, brazo, TT, NS.tc_de(brazo, TT), NS.FRIO['T_lect'], os.path.join(CAR, car), False))
    return r, json.loads(json.dumps(MB.BQ_OUT, default=float))


def difs(a, b, fuera=('seg', 'brazo')):
    return [k for k in sorted(set(a) | set(b)) if k not in fuera and json.dumps(a.get(k), sort_keys=True) != json.dumps(b.get(k), sort_keys=True)]


def jb(B, fuera=('cfg',)):
    return json.dumps({k: v for k, v in B.items() if k not in fuera}, sort_keys=True)


def main():
    t0 = time.time(); n = 0; n_ok = 0
    p('identidad_bloques6.py', time.strftime('%Y-%m-%d %H:%M:%S'))
    out = subprocess.run([sys.executable, os.path.join(AQUI, 'construye_bloques6.py'), '--verifica'], capture_output=True, text=True).stdout.strip()
    n += 1; n_ok += ok('(K) construye_bloques6 --verifica', out.startswith('IGUAL'), out)
    try: C6.verifica(); n += 1; n_ok += ok('(K) shas fijados', True)
    except SystemExit as e: n += 1; n_ok += ok('(K) shas fijados', False, str(e))
    p('(A) inv 0 / inv 1 == motor_bloques5 bit a bit')
    for b, s, TT in (('SEL_OLV_V_0', 48685, 30000), ('BLOQ4_V5a', 48686, 30000), ('BLOQ2_V_I', 48685, 50000), ('ING_F1_V', 48686, 30000)):
        r5, B5 = run(5, s, b, None, 'a5', TT); r6, B6 = run(6, s, b, None, 'a6', TT)
        n += 1; n_ok += ok(f'{b} s{s} T{TT}', not difs(r5, r6) and jb(B5) == jb(B6) and r5['aborto'] is None,
                           f"distintas {difs(r5, r6)} · hijos {B5.get('n_hijos')} · n_inv {B5.get('n_inv')}")
    p('(B) inv 2 (nucleo) con periodo 20 000 == inv 1 (Python) con periodo 20 000')
    for b, s in (('BLOQ2_V_I', 48687), ('ING_SEL_C_V5a', 48687)):
        r1, B1 = run(6, s, b, dict(inv=1, inv_cada=20000), 'b1', 60000); r2, B2 = run(6, s, b, dict(inv=2, inv_cada=20000), 'b2', 60000)
        n += 1; n_ok += ok(f'{b} s{s} T60000', not difs(r1, r2) and jb(B1, ('cfg', 'n_inv')) == jb(B2, ('cfg', 'n_inv')),
                           f"distintas {difs(r1, r2)} · n_inv python {B1.get('n_inv')}")
    p('(C) periodo 500 != sin inversion')
    r0, _ = run(6, 48688, 'SEL_OLV_V_0', None, 'c0', 20000); r5_, _ = run(6, 48688, 'SEL_OLV_V_p500', None, 'c5', 20000)
    n += 1; n_ok += ok('periodo 500 cambia la corrida', bool(difs(r0, r5_)), f"n_nac {r5_['n_nac']} vs {r0['n_nac']}")
    p('(D) determinismo')
    x1, y1 = run(6, 48688, 'BLOQ4_V_p500', None, 'd1', 30000); x2, y2 = run(6, 48688, 'BLOQ4_V_p500', None, 'd2', 30000)
    n += 1; n_ok += ok('BLOQ4_V_p500 dos veces ==', not difs(x1, x2) and jb(y1) == jb(y2))
    p(f'RESULTADO {n_ok}/{n} en {time.time() - t0:.0f} s')
    open(os.path.join(AQUI, 'identidad_bloques6_salida.txt'), 'w', encoding='utf-8').write('\n'.join(LOG) + '\n')


if __name__ == '__main__':
    main()
