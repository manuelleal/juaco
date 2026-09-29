"""identidad_bloques4.py — arnes de OLVIDAR / REPROBAR (Opus M, 28-sep-2026). Un proceso; semillas 48691-48694. Mision: llegar a la AGI por este camino.
(K) anclas y shas. (A) sin kit 3 (olvido y reprueba apagados) motor_bloques4 == motor_bloques3 BIT A BIT: kit 2 con inversion, kit 1 con
inversion, kit 2 sin inversion (claves + reglas/banco/contadores). (B) kit 3 vacio con tasas 0 == ING_F1_V. (C) las piezas ACTUAN: olvido y
reprobar forzados cambian la corrida; kit 3 con tasas != kit 2. (D) determinismo kit 3 con inversion.
"""
import json, os, subprocess, sys, time
AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
import corre_bloques4 as C4   # noqa: E402
C3 = C4.C3; CB = C4.CB; NS = C4.NS
CAR = os.path.join(AQUI, 'datos', 'arnes4')
LOG = []
CERO = dict(p_campo=0, p_dup=0, p_ins=0, p_hgt=0, p_del=0)


def p(*a):
    s = ' '.join(str(x) for x in a); print(s, flush=True); LOG.append(s)


def ok(nombre, cond, info=''):
    p(f"  [{'OK ' if cond else 'MAL'}] {nombre} {info}"); return bool(cond)


def run(motor, seed, brazo, extra=None, car='x', TT=30000):
    MB = C3.usa_bloques3() if motor == 3 else C4.usa_bloques4()
    MB.BQ_CFG.clear(); MB.BQ_CFG.update(CB.DEF); MB.BQ_CFG.update(CB.BQ[brazo]); MB.BQ_CFG.update(extra or {})
    r = NS.trabajo((seed, brazo, TT, NS.tc_de(brazo, TT), NS.FRIO['T_lect'], os.path.join(CAR, car), False))
    return r, json.loads(json.dumps(MB.BQ_OUT, default=float))


def difs(a, b, fuera=('seg', 'brazo')):
    return [k for k in sorted(set(a) | set(b)) if k not in fuera and json.dumps(a.get(k), sort_keys=True) != json.dumps(b.get(k), sort_keys=True)]


def jb(B):
    return json.dumps({k: v for k, v in B.items() if k != 'cfg'}, sort_keys=True)


def main():
    t0 = time.time(); n = 0; n_ok = 0
    p('identidad_bloques4.py', time.strftime('%Y-%m-%d %H:%M:%S'))
    out = subprocess.run([sys.executable, os.path.join(AQUI, 'construye_bloques4.py'), '--verifica'], capture_output=True, text=True).stdout.strip()
    n += 1; n_ok += ok('(K) construye_bloques4 --verifica', out.startswith('IGUAL'), out)
    try: C4.verifica(); n += 1; n_ok += ok('(K) shas fijados', True)
    except SystemExit as e: n += 1; n_ok += ok('(K) shas fijados', False, str(e))
    p('(A) olvido y reprueba apagados == motor_bloques3 bit a bit')
    for b, s, TT in (('BLOQ2_V_I', 48691, 50000), ('BLOQ_V_I', 48692, 50000), ('BLOQ2_V', 48691, 30000)):
        r3, B3 = run(3, s, b, None, 'a3', TT); r4, B4 = run(4, s, b, None, 'a4', TT)
        n += 1; n_ok += ok(f'{b} s{s} T{TT}', not difs(r3, r4) and jb(B3) == jb(B4) and r3['aborto'] is None,
                           f"distintas {difs(r3, r4)} · hijos {B3.get('n_hijos')} ins {B3.get('n_ins')} · n_inv {B3.get('n_inv')}")
    p('(B) kit 3 vacio, tasas 0 == ING_F1_V')
    F, _ = run(3, 48691, 'ING_F1_V', None, 'f')
    r, B = run(4, 48691, 'BLOQ3_V', CERO, 'b')
    n += 1; n_ok += ok('BLOQ3_V vacio == ING_F1_V', not difs(F, r), f"distintas {difs(F, r)} · hijos {B['n_hijos']}")
    p('(C) las piezas nuevas actuan')
    mem = [8, 0, 0, 0.5, 0, -3.0]
    rm, _ = run(4, 48691, 'BLOQ3_V', dict(CERO, forzada=[mem]), 'c0')
    ro, _ = run(4, 48691, 'BLOQ3_V', dict(CERO, forzada=[mem, [0, 0, 0, 1.01, 6, 3.0]]), 'c1')
    rr, _ = run(4, 48691, 'BLOQ3_V', dict(CERO, forzada=[mem, [0, 0, 0, 1.01, 7, 3.0]]), 'c2')
    n += 1; n_ok += ok('olvido (lambda 0.1/paso) cambia la corrida de "no muerdas lo recordado malo"', bool(difs(rm, ro)), f"n_nac {ro['n_nac']} vs {rm['n_nac']}")
    n += 1; n_ok += ok('reprobar (p = 1) cambia la corrida', bool(difs(rm, rr)), f"n_nac {rr['n_nac']} vs {rm['n_nac']}")
    k3, B3 = run(4, 48693, 'BLOQ3_V', None, 'k3'); k2, _ = run(4, 48693, 'BLOQ3_V', dict(kit=2), 'k2')
    n += 1; n_ok += ok('kit 3 con tasas != kit 2 con tasas', bool(difs(k2, k3)), f"ins {B3['n_ins']}")
    p('(D) determinismo')
    ra, Ba = run(4, 48694, 'BLOQ3_Va', None, 'Da', 50000); rb, Bb = run(4, 48694, 'BLOQ3_Va', None, 'Db', 50000)
    n += 1; n_ok += ok('BLOQ3_Va dos veces ==', not difs(ra, rb) and jb(Ba) == jb(Bb))
    p(f'RESULTADO {n_ok}/{n} en {time.time() - t0:.0f} s')
    open(os.path.join(AQUI, 'identidad_bloques4_salida.txt'), 'w', encoding='utf-8').write('\n'.join(LOG) + '\n')


if __name__ == '__main__':
    main()
