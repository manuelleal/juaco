"""identidad_bloques2.py — arnes del KIT GRANDE (Opus M, 28-sep-2026, noche). Un proceso; T corto; semillas 48791-48794.
Salida: identidad_bloques2_salida.txt. Mision: llegar a la AGI por este camino.

(K) motor_bloques2 == construccion por anclas desde motor_bloques (sha fijado).
(A) KIT GRANDE APAGADO (kit 1): motor_bloques2 == motor_bloques BIT A BIT en todas las claves y en las reglas/banco/contadores:
    BLOQ_V (reglas evolucionando), BLOQ (vivero permanente), regla forzada, ING_F1_V (BQ apagado).
(B) kit 2 con genoma vacio y tasas 0 == fabrica (ING_F1 de motor_bloques).
(C) CONTROLES QUE DEBEN FALLAR / las piezas nuevas ACTUAN: kit 2 con las tasas != kit 1; "seguir al vecino" !=; "ventana +3" da mas
    nacimientos; "no muerdas lo que recuerdas malo" (memF) baja la fraccion de muertes por veneno+sal; sentidos 6, 7, 11, 12 != .
(H) herencia kit 2 (tasas 0, 1 regla inicial): todo hijo == padre.   (Q) corte + reanuda (kit 2) == entera.   (D) determinismo kit 2.
"""
import json, os, shutil, subprocess, sys, time
AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
import corre_bloques2 as C2   # noqa: E402
CB = C2.CB; NS = C2.NS
T = 30000
CAR = os.path.join(AQUI, 'datos', 'arnes2')
LOG = []
CERO = dict(p_campo=0, p_dup=0, p_ins=0, p_hgt=0, p_del=0)


def p(*a):
    s = ' '.join(str(x) for x in a); print(s, flush=True); LOG.append(s)


def ok(nombre, cond, info=''):
    p(f"  [{'OK ' if cond else 'MAL'}] {nombre} {info}"); return bool(cond)


def run(motor, seed, brazo, extra=None, car='x', rean=False, TT=T):
    MB = C2.usa_bloques1() if motor == 1 else C2.usa_bloques2()
    MB.BQ_CFG.clear(); MB.BQ_CFG.update(CB.DEF); MB.BQ_CFG.update(CB.BQ[brazo]); MB.BQ_CFG.update(extra or {})
    r = NS.trabajo((seed, brazo, TT, NS.tc_de(brazo, TT), NS.FRIO['T_lect'], os.path.join(CAR, car), rean))
    return r, json.loads(json.dumps(MB.BQ_OUT, default=float))


def difs(a, b, fuera=('seg', 'brazo')):
    return [k for k in sorted(set(a) | set(b)) if k not in fuera and json.dumps(a.get(k), sort_keys=True) != json.dumps(b.get(k), sort_keys=True)]


def jb(B):
    return json.dumps({k: v for k, v in B.items() if k != 'cfg'}, sort_keys=True)


def vs(x):
    return (x['causas_2a'][2] + x['causas_2a'][3]) / max(1, sum(x['causas_2a']))


def main():
    t0 = time.time(); n = 0; n_ok = 0
    p('identidad_bloques2.py', time.strftime('%Y-%m-%d %H:%M:%S'), f'T {T}')
    p('(K) construccion y shas')
    out = subprocess.run([sys.executable, os.path.join(AQUI, 'construye_bloques2.py'), '--verifica'], capture_output=True, text=True).stdout.strip()
    n += 1; n_ok += ok('construye_bloques2 --verifica', out.startswith('IGUAL'), out)
    try: C2.verifica(); n += 1; n_ok += ok('shas fijados', True)
    except SystemExit as e: n += 1; n_ok += ok('shas fijados', False, str(e))
    p('(A) kit 1 en motor_bloques2 == motor_bloques (bit a bit, con reglas)')
    forz = [[3, 1, 0, 0.5, 0, -3.0], [0, 0, 1, 0.3, 2, 1.0], [5, 0, 0, 0.5, 3, 1.5]]
    for nom, seed, brazo, extra in (('BLOQ_V', 48791, 'BLOQ_V', None), ('BLOQ', 48792, 'BLOQ', None),
                                    ('BLOQ_V forzada (boca, quieto, parir)', 48791, 'BLOQ_V', dict(forzada=forz)),
                                    ('ING_F1_V (apagado)', 48791, 'ING_F1_V', None)):
        r1, B1 = run(1, seed, brazo, extra, 'a1'); r2, B2 = run(2, seed, brazo, extra, 'a2')
        d = difs(r1, r2)
        n += 1; n_ok += ok(nom, not d and jb(B1) == jb(B2) and r1['aborto'] is None,
                           f"distintas {d} · reglas/banco/contadores {'==' if jb(B1) == jb(B2) else '!='} · hijos {B1.get('n_hijos')} ins {B1.get('n_ins')} · K_nac {r1.get('K_nac')}")
    F1, _ = run(1, 48791, 'ING_F1', None, 'f1')
    p('(B) kit 2, genoma vacio, tasas 0 == fabrica')
    r, B = run(2, 48791, 'BLOQ2_V', CERO, 'b')
    Fv, _ = run(1, 48791, 'ING_F1_V', None, 'f1v')
    d = difs(Fv, r)
    n += 1; n_ok += ok('BLOQ2_V vacio == ING_F1_V', not d, f"distintas {d} · hijos {B['n_hijos']} fund {B['n_fund']}")
    p('(C) controles y piezas nuevas')
    r2, B2 = run(2, 48791, 'BLOQ2_V', None, 'c'); r1, B1 = run(2, 48791, 'BLOQ2_V', dict(kit=1, tope=12), 'c1')
    n += 1; n_ok += ok('kit 2 con tasas != kit 1 con tasas', bool(difs(r1, r2)), f"ins kit2 {B2['n_ins']}")
    casos = [('seguir al vecino siempre', [[10, 0, 0, 1.01, 4, 3.0]], None),
             ('ventana +3 siempre (parir antes)', [[0, 0, 0, 1.01, 5, 3.0]], 'nac'),
             ('no muerdas lo que recuerdas malo (memF < 0.5 -> boca -3)', [[8, 0, 0, 0.5, 0, -3.0]], 'veneno'),
             ('resE > 0.6 -> quieto +2', [[6, 0, 1, 0.6, 2, 2.0]], None),
             ('resA < 0.5 -> hacia +2', [[7, 0, 0, 0.5, 1, 2.0]], None),
             ('vecino mordio > 0.5 -> boca +2', [[11, 0, 1, 0.5, 0, 2.0]], None),
             ('tParto < 0.3 -> ventana -3', [[12, 0, 0, 0.3, 5, -3.0]], None)]
    for nom, fz, tipo in casos:
        r, B = run(2, 48791, 'BLOQ2_V', dict(CERO, forzada=fz), 'cz')
        d = difs(F1, r)
        info = f"{len(d)} claves distintas"
        cond = bool(d) and r['aborto'] is None
        if tipo == 'nac':
            cond = cond and r['n_nac'] > F1['n_nac']; info += f" · n_nac {r['n_nac']} vs {F1['n_nac']}"
        if tipo == 'veneno':
            cond = cond and vs(r) < vs(F1); info += f" · veneno+sal {vs(r):.3f} vs {vs(F1):.3f}"
        n += 1; n_ok += ok(nom, cond, info)
    p('(H) herencia kit 2')
    r, B = run(2, 48793, 'BLOQ2_V', dict(CERO, inicial=1), 'h')
    n += 1; n_ok += ok('todo hijo == padre', B['n_hijos'] > 0 and B['n_igual_padre'] == B['n_hijos'] and B['n_hijos_pl'] > 0,
                       f"{B['n_igual_padre']}/{B['n_hijos']} (padre con reglas {B['n_igual_pl']}/{B['n_hijos_pl']})")
    p('(Q) corte + reanuda, kit 2')
    TQ = 40000
    ent, Be = run(2, 48794, 'BLOQ2_V', None, 'Qa', TT=TQ)
    cq = os.path.join(CAR, 'Qb'); shutil.rmtree(cq, ignore_errors=True)
    MB = C2.usa_bloques2(); MB.BQ_CFG.clear(); MB.BQ_CFG.update(CB.DEF); MB.BQ_CFG.update(CB.BQ['BLOQ2_V'])
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
        NS.trabajo((48794, 'BLOQ2_V', TQ, NS.tc_de('BLOQ2_V', TQ), NS.FRIO['T_lect'], cq, False)); cortado = False
    except KeyboardInterrupt:
        cortado = True
    rea, Br = run(2, 48794, 'BLOQ2_V', None, 'Qb', rean=True, TT=TQ)
    n += 1; n_ok += ok('corte en 30 000 + reanuda == entera', cortado and not difs(ent, rea) and jb(Be) == jb(Br),
                       f"cortado {cortado} · distintas {difs(ent, rea)} · reglas {'==' if jb(Be) == jb(Br) else '!='}")
    p('(D) determinismo kit 2')
    ra, Ba = run(2, 48794, 'BLOQ2_V', None, 'Da'); rb, Bb = run(2, 48794, 'BLOQ2_V', None, 'Db')
    n += 1; n_ok += ok('dos veces ==', not difs(ra, rb) and jb(Ba) == jb(Bb),
                       f"largo medio vivos T {sum(len(x[3]) for x in Ba['vivos_T']) / max(1, len(Ba['vivos_T'])):.2f}")
    p(f'RESULTADO {n_ok}/{n} en {time.time() - t0:.0f} s')
    open(os.path.join(AQUI, 'identidad_bloques2_salida.txt'), 'w', encoding='utf-8').write('\n'.join(LOG) + '\n')


if __name__ == '__main__':
    main()
