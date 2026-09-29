"""identidad_bloques3.py — arnes de UN MUNDO QUE CAMBIA (Opus M, 28-sep-2026). Un proceso; semillas 48991-48994. Mision: llegar a la AGI por este camino.
(K) anclas y shas. (A) inv = 0: motor_bloques3 == motor_bloques2 BIT A BIT (BLOQ2_V con reglas, BLOQ_V, ING_F1_V; tambien reglas/banco/contadores).
(B) inv = 1: la corrida es IDENTICA antes de t = 20 000 (tam_total) y DISTINTA despues (la inversion ocurre justo alli); 2 inversiones a T 60 000.
(Q) corte en 30 000 (tras la 1a inversion) + reanuda == entera.   (D) determinismo con inversion.
"""
import json, os, shutil, subprocess, sys, time
AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
import corre_bloques3 as C3   # noqa: E402
C2 = C3.C2; CB = C3.CB; NS = C3.NS
CAR = os.path.join(AQUI, 'datos', 'arnes3')
LOG = []


def p(*a):
    s = ' '.join(str(x) for x in a); print(s, flush=True); LOG.append(s)


def ok(nombre, cond, info=''):
    p(f"  [{'OK ' if cond else 'MAL'}] {nombre} {info}"); return bool(cond)


def run(motor, seed, brazo, extra=None, car='x', rean=False, TT=30000):
    MB = C2.usa_bloques2() if motor == 2 else C3.usa_bloques3()
    MB.BQ_CFG.clear(); MB.BQ_CFG.update(CB.DEF); MB.BQ_CFG.update(CB.BQ[brazo]); MB.BQ_CFG.update(extra or {})
    r = NS.trabajo((seed, brazo, TT, NS.tc_de(brazo, TT), NS.FRIO['T_lect'], os.path.join(CAR, car), rean))
    return r, json.loads(json.dumps(MB.BQ_OUT, default=float))


def difs(a, b, fuera=('seg', 'brazo')):
    return [k for k in sorted(set(a) | set(b)) if k not in fuera and json.dumps(a.get(k), sort_keys=True) != json.dumps(b.get(k), sort_keys=True)]


def jb(B):
    return json.dumps({k: v for k, v in B.items() if k != 'cfg'}, sort_keys=True)


def main():
    t0 = time.time(); n = 0; n_ok = 0
    p('identidad_bloques3.py', time.strftime('%Y-%m-%d %H:%M:%S'))
    p('(K)')
    out = subprocess.run([sys.executable, os.path.join(AQUI, 'construye_bloques3.py'), '--verifica'], capture_output=True, text=True).stdout.strip()
    n += 1; n_ok += ok('construye_bloques3 --verifica', out.startswith('IGUAL'), out)
    try: C3.verifica(); n += 1; n_ok += ok('shas fijados', True)
    except SystemExit as e: n += 1; n_ok += ok('shas fijados', False, str(e))
    p('(A) inversion apagada == motor_bloques2 bit a bit')
    for b, s in (('BLOQ2_V', 48991), ('BLOQ_V', 48992), ('ING_F1_V', 48991)):
        r2, B2 = run(2, s, b, None, 'a2'); r3, B3 = run(3, s, b, None, 'a3')
        d = difs(r2, r3); jb2 = {k: v for k, v in B2.items() if k not in ('cfg', 'n_inv')}; jb3 = {k: v for k, v in B3.items() if k not in ('cfg', 'n_inv')}
        n += 1; n_ok += ok(f'{b} s{s}', not d and json.dumps(jb2, sort_keys=True) == json.dumps(jb3, sort_keys=True) and r2['aborto'] is None,
                           f"distintas {d} · hijos {B2.get('n_hijos')} ins {B2.get('n_ins')}")
    p('(B) la inversion ocurre justo en t = 20 000')
    TB = 60000
    r0, B0 = run(3, 48993, 'BLOQ2_V', None, 'b0', TT=TB); r1, B1 = run(3, 48993, 'BLOQ2_V_I', None, 'b1', TT=TB)
    m = NS.MUNDO['muestra']; i20 = 20000 // m
    t0a, t1a = r0['tam_total'], r1['tam_total']
    antes = t0a[:i20 + 1] == t1a[:i20 + 1]
    despues = t0a[i20 + 1:] != t1a[i20 + 1:]
    n += 1; n_ok += ok('tam_total igual hasta t = 20 000 inclusive', antes, f'(muestra {m})')
    n += 1; n_ok += ok('y distinto despues', despues)
    n += 1; n_ok += ok('2 inversiones a T 60 000 (t = 20 000 y 40 000)', B1.get('n_inv') == 2 and not B0.get('n_inv'), f"n_inv {B1.get('n_inv')} / {B0.get('n_inv')}")
    p('(Q) corte en 30 000 + reanuda == entera (con inversion)')
    TQ = 40000
    ent, Be = run(3, 48994, 'BLOQ2_V_I', None, 'Qa', TT=TQ)
    cq = os.path.join(CAR, 'Qb'); shutil.rmtree(cq, ignore_errors=True)
    MB = C3.usa_bloques3(); MB.BQ_CFG.clear(); MB.BQ_CFG.update(CB.DEF); MB.BQ_CFG.update(CB.BQ['BLOQ2_V_I'])
    orig = NS.CR.ME.run_solapadas

    def corta(*a, _o=orig, **k):
        fn = k['eco']['ckpt_fn']
        def fn2(tt, blob):
            fn(tt, blob)
            if tt == 30000: raise KeyboardInterrupt('corte simulado')
        k['eco'] = dict(k['eco'], ckpt_fn=fn2)
        return _o(*a, **k)
    NS.CR.ME.run_solapadas = corta
    try:
        NS.trabajo((48994, 'BLOQ2_V_I', TQ, NS.tc_de('BLOQ2_V_I', TQ), NS.FRIO['T_lect'], cq, False)); cortado = False
    except KeyboardInterrupt:
        cortado = True
    rea, Br = run(3, 48994, 'BLOQ2_V_I', None, 'Qb', rean=True, TT=TQ)
    n += 1; n_ok += ok('corte + reanuda == entera', cortado and not difs(ent, rea) and jb(Be) == jb(Br),
                       f"cortado {cortado} · distintas {difs(ent, rea)} · n_inv {Be.get('n_inv')}/{Br.get('n_inv')}")
    p('(D) determinismo')
    ra, Ba = run(3, 48994, 'BLOQ2_V_I', None, 'Da', TT=TQ); rb, Bb = run(3, 48994, 'BLOQ2_V_I', None, 'Db', TT=TQ)
    n += 1; n_ok += ok('dos veces ==', not difs(ra, rb) and jb(Ba) == jb(Bb))
    p(f'RESULTADO {n_ok}/{n} en {time.time() - t0:.0f} s')
    open(os.path.join(AQUI, 'identidad_bloques3_salida.txt'), 'w', encoding='utf-8').write('\n'.join(LOG) + '\n')


if __name__ == '__main__':
    main()
