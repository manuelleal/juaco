"""identidad_bloques5.py — arnes de OLVIDAR EL CEREBRO (Opus M, 28-sep-2026). Un proceso; semillas 48681-48684. Mision: llegar a la AGI.
(K) anclas y shas. (A) sin la pieza (kit 3, kit 2 con inversion, kit 1) motor_bloques5 == motor_bloques4 BIT A BIT (claves + reglas/banco/contadores).
(B) kit 4 vacio con tasas 0 == ING_F1_V. (C) la pieza ACTUA: el gen de olvido con lambda alto cambia la corrida y lambda despreciable (w = -3,
1e-7/paso) casi no; kit 5 hereda solo w (sentido/umbral/accion fijos). (D) determinismo kit 4 y kit 5 con inversion.
"""
import json, os, subprocess, sys, time
AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
import corre_bloques5 as C5   # noqa: E402
C4 = C5.C4; CB = C5.CB; NS = C5.NS
CAR = os.path.join(AQUI, 'datos', 'arnes5')
LOG = []
CERO = dict(p_campo=0, p_dup=0, p_ins=0, p_hgt=0, p_del=0)


def p(*a):
    s = ' '.join(str(x) for x in a); print(s, flush=True); LOG.append(s)


def ok(nombre, cond, info=''):
    p(f"  [{'OK ' if cond else 'MAL'}] {nombre} {info}"); return bool(cond)


def run(motor, seed, brazo, extra=None, car='x', TT=30000):
    MB = C4.usa_bloques4() if motor == 4 else C5.usa_bloques5()
    MB.BQ_CFG.clear(); MB.BQ_CFG.update(CB.DEF); MB.BQ_CFG.update(CB.BQ[brazo]); MB.BQ_CFG.update(extra or {})
    r = NS.trabajo((seed, brazo, TT, NS.tc_de(brazo, TT), NS.FRIO['T_lect'], os.path.join(CAR, car), False))
    return r, json.loads(json.dumps(MB.BQ_OUT, default=float))


def difs(a, b, fuera=('seg', 'brazo')):
    return [k for k in sorted(set(a) | set(b)) if k not in fuera and json.dumps(a.get(k), sort_keys=True) != json.dumps(b.get(k), sort_keys=True)]


def jb(B):
    return json.dumps({k: v for k, v in B.items() if k != 'cfg'}, sort_keys=True)


def main():
    t0 = time.time(); n = 0; n_ok = 0
    p('identidad_bloques5.py', time.strftime('%Y-%m-%d %H:%M:%S'))
    out = subprocess.run([sys.executable, os.path.join(AQUI, 'construye_bloques5.py'), '--verifica'], capture_output=True, text=True).stdout.strip()
    n += 1; n_ok += ok('(K) construye_bloques5 --verifica', out.startswith('IGUAL'), out)
    try: C5.verifica(); n += 1; n_ok += ok('(K) shas fijados', True)
    except SystemExit as e: n += 1; n_ok += ok('(K) shas fijados', False, str(e))
    p('(A) sin la pieza == motor_bloques4 bit a bit')
    for b, s, TT in (('BLOQ3_Va', 48681, 50000), ('BLOQ2_V_I', 48682, 50000), ('BLOQ_V', 48681, 30000)):
        r4, B4 = run(4, s, b, None, 'a4', TT); r5, B5 = run(5, s, b, None, 'a5', TT)
        n += 1; n_ok += ok(f'{b} s{s} T{TT}', not difs(r4, r5) and jb(B4) == jb(B5) and r4['aborto'] is None,
                           f"distintas {difs(r4, r5)} · hijos {B4.get('n_hijos')} ins {B4.get('n_ins')}")
    p('(B) kit 4 vacio, tasas 0 == ING_F1_V')
    F, _ = run(4, 48681, 'ING_F1_V', None, 'f')
    r, B = run(5, 48681, 'BLOQ4_V_0', CERO, 'b')
    n += 1; n_ok += ok('BLOQ4_V vacio == ING_F1_V', not difs(F, r), f"distintas {difs(F, r)}")
    p('(C) la pieza actua')
    ra, _ = run(5, 48683, 'BLOQ4_V_0', dict(CERO, forzada=[[0, 0, 0, 1.0, 8, 3.0]]), 'c1')     # lambda 0.1/paso
    rb, _ = run(5, 48683, 'BLOQ4_V_0', dict(CERO, forzada=[[0, 0, 0, 1.0, 8, -3.0]]), 'c2')    # lambda 1e-7/paso
    rc, _ = run(5, 48683, 'BLOQ4_V_0', dict(CERO, forzada=[[0, 0, 0, 1.0, 2, 0.0001]]), 'c3')  # regla inerte de otra accion (misma ranura)
    n += 1; n_ok += ok('olvido del cerebro fuerte (0.1/paso) != sin olvido', bool(difs(rc, ra)), f"n_nac {ra['n_nac']} vs {rc['n_nac']} · K_nac {ra['K_nac']} vs {rc['K_nac']}")
    n += 1; n_ok += ok('olvido despreciable (1e-7/paso) corre y no aborta', rb['aborto'] is None, f"n_nac {rb['n_nac']} vs {rc['n_nac']}")
    r5_, B5_ = run(5, 48684, 'SEL_OLV_V5a', dict(p_campo=1.0), 'c4', 50000)
    ok_forma = all(len(x[3]) <= 1 and all(int(rr[0]) == 0 and int(rr[4]) == 8 and rr[3] == 1.0 for rr in x[3]) for x in B5_['vivos_T'])
    ok_forma = ok_forma and all(len(R) <= 1 and all(int(rr[4]) == 8 for rr in R) for R in B5_['banco_T'])
    ws = sorted(set(round(rr[5], 3) for R in B5_['banco_T'] for rr in R))
    n += 1; n_ok += ok('kit 5: el gen conserva su forma (siempre -> olvidar el cerebro) y solo muta w', ok_forma and len(ws) > 3,
                       f"{len(ws)} valores de w distintos en el banco")
    p('(D) determinismo')
    for b in ('BLOQ4_V5a', 'SEL_OLV_V5a'):
        x1, y1 = run(5, 48684, b, None, 'D1', 50000); x2, y2 = run(5, 48684, b, None, 'D2', 50000)
        n += 1; n_ok += ok(f'{b} dos veces ==', not difs(x1, x2) and jb(y1) == jb(y2))
    p(f'RESULTADO {n_ok}/{n} en {time.time() - t0:.0f} s')
    open(os.path.join(AQUI, 'identidad_bloques5_salida.txt'), 'w', encoding='utf-8').write('\n'.join(LOG) + '\n')


if __name__ == '__main__':
    main()
