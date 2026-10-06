"""identidad_baldwin.py — arnes de BALDWIN EN BLOQUES (29-sep-2026). UN proceso; T corto (<= 40 000); semillas 56491-56494.
Salida: identidad_baldwin_salida.txt. Mision: llegar a la AGI por este camino.

(K) motor_baldwin == construccion por anclas desde motor_bloques3 (sha fijado); shas de la entrada.
(A) PERILLA APAGADA (plast = 0), BIT A BIT:
    A1 sin inversion: corre_baldwin.corre(FIJO_V_Pinf) == corre_bloques.corre(BLOQ_V) con motor_bloques (el de la serie BLOQUES), campo a
       campo (regla 14; salvo seg, brazo, cfg y lo agregado: cfg_worker, baldwin) y el BQ_OUT (reglas de los vivos, banco, contadores).
    A2 con inversion cada 6 000: motor_baldwin plast 0 == motor_bloques3 inv 1 (todas las claves de trabajo + BQ_OUT).
    A3 la VIA plastica con cero reglas plasticas (plast 1 y 3, p_ins_pl 0, p_bit 0) == plast 0: las reglas evolucionan con el MISMO azar.
(B) CONTROLES QUE DEBEN DIFERIR (P 6 000): PLAST_V != FIJO_V; PLAST_AZA != PLAST_V; PLAST_RW0 != PLAST_V; la pieza actua (n_aprende > 0);
    AZA: el bit de los vivos es mezcla (fraccion en [0.2, 0.8]).
(H) SIN LAMARCK: fundadores con 2 reglas de boca plasticas (w0 = 0), tasas 0: en T todo vivo conserva w0 = 0 y bit 1 en las dos reglas,
    algun vivo tiene w aprendido != 0, y todo hijo es genetica == padre. En una corrida con tasas, las reglas NO plasticas de los vivos
    tienen w == w0 exacto.
(Q) corte en 30 000 + --reanuda == la corrida entera (PLAST_V_P6k, T 40 000).   (D) determinismo (PLAST_RW0_P6k dos veces).
(L) la LETRA de lee() en entradas sinteticas (FUNCIONA, HAY ALGO MODESTO x2, NO, NO SE LEE).   (R) banderas y candados de main().
"""
import copy, json, os, shutil, subprocess, sys, time, types
AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
import corre_baldwin as C   # noqa: E402
CB = C.CB; NS = C.NS
CAR = os.path.join(C.DATOS, 'arnes')
for _br in ('PLAST_AZA_P6k', 'PLAST_RW0_P6k'):   # brazos SOLO del arnes (la serie usa AZA y RW0 con P 22 000)
    CB.BQ.setdefault(_br, C.cfg_de(_br)); NS.BRAZOS.setdefault(_br, ('MUT0', CB.FAB, C.T_CORTE))
LOG = []
TA = 30000


def p(*a):
    s = ' '.join(str(x) for x in a); print(s, flush=True); LOG.append(s)


def ok(nombre, cond, info=''):
    p(f"  [{'OK ' if cond else 'MAL'}] {nombre} {info}"); return bool(cond)


def usa_bloques3():
    import motor_bloques3 as MB
    g = types.ModuleType('motor_bloques3_gemelo')
    g.__dict__.update({k: v for k, v in NS.ME_PY.__dict__.items() if not k.startswith('__')})
    g.run_solapadas = MB.run_solapadas; g._MF = MB; NS.CR.ME = g
    return MB


def run(motor, seed, brazo, cfg, car, TT=TA, rean=False):
    """UNA corrida por NS.trabajo con el motor pedido (1 motor_bloques, 3 motor_bloques3, 'b' motor_baldwin) y la cfg COMPLETA."""
    MB = {1: C.USA_BLOQUES_ORIGINAL, 3: usa_bloques3, 'b': C.usa_baldwin}[motor]()
    MB.BQ_CFG.clear(); MB.BQ_CFG.update(cfg)
    r = NS.trabajo((seed, brazo, TT, NS.tc_de(brazo, TT), NS.FRIO['T_lect'], os.path.join(CAR, car), rean))
    return r, json.loads(json.dumps(MB.BQ_OUT, default=float))


def difs(a, b, fuera=('seg', 'brazo')):
    return [k for k in sorted(set(a) | set(b)) if k not in fuera and json.dumps(a.get(k), sort_keys=True) != json.dumps(b.get(k), sort_keys=True)]


NUEVAS = ('cfg', 'n_flip', 'serie_pl', 'vivos_T_pl', 'n_aprende', 'n_mord_aprende')


def jb(B, fuera=NUEVAS, corta_banco=False):
    B = {k: v for k, v in B.items() if k not in fuera}
    if corta_banco and 'banco_T' in B: B['banco_T'] = [[r[:6] for r in R] for R in B['banco_T']]
    return json.dumps(B, sort_keys=True)


def cfg(brazo, **kw):
    return dict(C.DEF, **dict(CB.BQ[brazo], **kw))


def main():
    t0 = time.time(); n = 0; n_ok = 0
    shutil.rmtree(CAR, ignore_errors=True)
    p('identidad_baldwin.py', time.strftime('%Y-%m-%d %H:%M:%S'), f'T {TA}')
    p('(K) construccion y shas')
    out = subprocess.run([sys.executable, os.path.join(AQUI, 'construye_baldwin.py'), '--verifica'], capture_output=True, text=True).stdout.strip()
    n += 1; n_ok += ok('construye_baldwin --verifica', out.startswith('IGUAL'), out)
    n += 1; n_ok += ok('verifica() del runner (shas + motor == anclas)', C.verifica(log=lambda s: None))

    p('(A) perilla apagada == BLOQUES bit a bit')
    # A1: regla 14, la ENTRADA entera: corre_baldwin.corre == corre_bloques.corre con motor_bloques
    CB.usa_bloques = C.USA_BLOQUES_ORIGINAL
    try:
        o1 = CB.corre(56491, 'BLOQ_V', TA, os.path.join(CAR, 'a1_bloques'))
    finally:
        CB.usa_bloques = C.usa_baldwin
    o2 = C.corre(56491, 'FIJO_V_Pinf', TA, os.path.join(CAR, 'a1_baldwin'))
    d = difs(o1, o2, fuera=('seg', 'brazo', 'bloques', 'cfg_worker', 'baldwin'))
    B1 = dict(o1['bloques']); B2 = dict(o2['bloques'])
    n += 1; n_ok += ok('A1 corre(FIJO_V_Pinf) == corre_bloques.corre(BLOQ_V) [motor_bloques], campo a campo', not d and jb(B1, NUEVAS + ('n_inv',)) == jb(B2, NUEVAS + ('n_inv',))
                       and o1['aborto'] is None, f"distintas {d} · hijos {B1.get('n_hijos')} ins {B1.get('n_ins')} · vivos T {len(B1.get('vivos_T') or [])} · K {o1['K']}")
    # A2: con inversion, motor_bloques3
    c3 = cfg('FIJO_V_P6k'); r3, Q3 = run(3, 56492, 'FIJO_V_P6k', c3, 'a2_b3'); rb, Qb = run('b', 56492, 'FIJO_V_P6k', c3, 'a2_bal')
    d = difs(r3, rb)
    n += 1; n_ok += ok('A2 inversion cada 6 000: motor_baldwin plast 0 == motor_bloques3', not d and jb(Q3) == jb(Qb) and r3['aborto'] is None,
                       f"distintas {d} · n_inv {Q3.get('n_inv')}/{Qb.get('n_inv')} · hijos {Q3.get('n_hijos')}")
    # A3: la via plastica sin reglas plasticas == plast 0
    for modo, br in ((1, 'PLAST_V_P6k'), (3, 'PLAST_RW0_P6k')):
        rp, Qp = run('b', 56492, br, cfg(br, p_ins_pl=0.0, p_bit=0.0), f'a3_{modo}')
        d = difs(rb, rp)
        n += 1; n_ok += ok(f'A3 plast {modo} con p_ins_pl 0 y p_bit 0 == plast 0', not d and jb(Qb, NUEVAS) == jb(Qp, NUEVAS, corta_banco=True)
                           and Qp.get('n_aprende') == 0 and Qp.get('n_flip') == 0, f"distintas {d} · aprende {Qp.get('n_aprende')} · filas del banco con 7 col {sum(1 for R_ in Qp.get('banco_T') or [] for r_ in R_ if len(r_) == 7)}")

    p('(B) controles que deben diferir (P 6 000, s56493)')
    R = {}
    for br in ('FIJO_V_P6k', 'PLAST_V_P6k', 'PLAST_AZA_P6k', 'PLAST_RW0_P6k'):
        R[br] = run('b', 56493, br, cfg(br), 'b')
    for a_, b_ in (('PLAST_V_P6k', 'FIJO_V_P6k'), ('PLAST_AZA_P6k', 'PLAST_V_P6k'), ('PLAST_RW0_P6k', 'PLAST_V_P6k')):
        d = difs(R[a_][0], R[b_][0])
        n += 1; n_ok += ok(f'{a_} != {b_}', len(d) > 0, f"{len(d)} claves distintas · K {R[a_][0]['tam_total'][-1]} vs {R[b_][0]['tam_total'][-1]} (vivos en T)")
    for br in ('PLAST_V_P6k', 'PLAST_RW0_P6k', 'PLAST_AZA_P6k'):
        n += 1; n_ok += ok(f'{br}: la pieza actua (n_aprende > 0)', (R[br][1].get('n_aprende') or 0) > 0,
                           f"aprende {R[br][1].get('n_aprende')} en {R[br][1].get('n_mord_aprende')} mordidas · flips {R[br][1].get('n_flip')}")
    pl = R['PLAST_AZA_P6k'][1].get('vivos_T_pl') or []
    bits = [b for x in pl for b, _ in x]
    fa = (sum(bits) / len(bits)) if bits else None
    n += 1; n_ok += ok('AZA: bit de los vivos mezclado (fraccion en [0.2, 0.8])', fa is not None and 0.2 <= fa <= 0.8, f"fraccion {fa} de {len(bits)} reglas")
    # en PLAST_V con tasas: las reglas NO plasticas de los vivos tienen w == w0 exacto; alguna plastica aprendio
    B = R['PLAST_V_P6k'][1]; np_ok = True; pl_mov = 0
    for x, bb in zip(B.get('vivos_T') or [], B.get('vivos_T_pl') or []):
        for r, (bt, w0) in zip(x[3], bb):
            if not bt and r[5] != w0: np_ok = False
            if bt and r[5] != w0: pl_mov += 1
    n += 1; n_ok += ok('H0 PLAST_V: reglas no plasticas w == w0; alguna plastica aprendio', np_ok and pl_mov > 0, f"plasticas movidas {pl_mov}")

    p('(H) sin Lamarck: 2 reglas plasticas forzadas con w0 = 0, tasas 0 (P 6 000, s56494)')
    fz = [[3, 4, 1, 0.5, 0, 0.0], [3, 4, 0, 0.5, 0, 0.0]]   # 'pixel 4 > 0.5 -> boca' (B, D) y 'pixel 4 < 0.5 -> boca' (A, C)
    ch = cfg('PLAST_V_P6k', p_campo=0, p_dup=0, p_ins=0, p_hgt=0, p_del=0, p_bit=0.0, forzada=fz, forzada_bit=[1, 1])
    rh, Qh = run('b', 56494, 'PLAST_V_P6k', ch, 'h')
    vv = Qh.get('vivos_T') or []; pp = Qh.get('vivos_T_pl') or []
    w0s = all(len(b) == 2 and all(bt == 1 and w0 == 0.0 for bt, w0 in b) for b in pp)
    apr = sum(1 for x in vv for r in x[3] if r[5] != 0.0)
    signo = [round(sum(x[3][0][5] for x in vv) / max(1, len(vv)), 3), round(sum(x[3][1][5] for x in vv) / max(1, len(vv)), 3)]
    n += 1; n_ok += ok('todo vivo en T conserva w0 = 0 y bit 1 (no se hereda lo aprendido)', bool(pp) and w0s, f"vivos {len(pp)}")
    n += 1; n_ok += ok('algun vivo tiene w aprendido != 0', apr > 0, f"reglas movidas {apr} · w medio (B/D, A/C) {signo} · n_inv {Qh.get('n_inv')}")
    n += 1; n_ok += ok('todo hijo es genetica == padre (tasas 0)', Qh.get('n_hijos', 0) > 0 and Qh.get('n_igual_padre') == Qh.get('n_hijos'),
                       f"{Qh.get('n_igual_padre')}/{Qh.get('n_hijos')}")

    p('(Q) corte en 30 000 + reanuda == entera (PLAST_V_P6k, T 40 000, s56494)')
    TQ = 40000; cq = cfg('PLAST_V_P6k')
    ent, Be = run('b', 56494, 'PLAST_V_P6k', cq, 'Qa', TT=TQ)
    MB = C.usa_baldwin(); MB.BQ_CFG.clear(); MB.BQ_CFG.update(cq)
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
        NS.trabajo((56494, 'PLAST_V_P6k', TQ, NS.tc_de('PLAST_V_P6k', TQ), NS.FRIO['T_lect'], os.path.join(CAR, 'Qb'), False)); cortado = False
    except KeyboardInterrupt:
        cortado = True
    rea, Br = run('b', 56494, 'PLAST_V_P6k', cq, 'Qb', TT=TQ, rean=True)
    n += 1; n_ok += ok('corte + reanuda == entera', cortado and not difs(ent, rea) and jb(Be, ()) == jb(Br, ()),
                       f"cortado {cortado} · distintas {difs(ent, rea)} · aprende {Be.get('n_aprende')}/{Br.get('n_aprende')} · n_inv {Be.get('n_inv')}/{Br.get('n_inv')}")

    p('(D) determinismo')
    ra, Ba = run('b', 56494, 'PLAST_RW0_P6k', cfg('PLAST_RW0_P6k'), 'Da'); rb2, Bb = run('b', 56494, 'PLAST_RW0_P6k', cfg('PLAST_RW0_P6k'), 'Db')
    n += 1; n_ok += ok('PLAST_RW0_P6k dos veces ==', not difs(ra, rb2) and jb(Ba, ()) == jb(Bb, ()))

    p('(L) la letra en entradas sinteticas')
    n_, k_ = letra_sintetica()
    n += n_; n_ok += k_

    p('(R) banderas y candados')
    for argv, nom in ((['--serie', '--pool', '3'], '--pool 3 aborta'), (['--humo', '--pool', '2'], '--humo con pool aborta'),
                      (['--humo', '--hum'], 'bandera desconocida aborta'), (['--seri'], 'bandera abreviada aborta')):
        try:
            C.main(argv); r_ = False
        except SystemExit:
            r_ = True
        n += 1; n_ok += ok(nom, r_)
    antes = set(os.listdir(C.DATOS)) if os.path.isdir(C.DATOS) else set()
    ck = os.path.join(CAR, 'candado'); os.makedirs(ck, exist_ok=True)
    l1, e1 = C.candado(ck, False); l2, e2 = C.candado(ck, False); l3, e3 = C.candado(ck, True)
    n += 1; n_ok += ok('candado exclusivo (O_EXCL): el 1o entra, el 2o se niega, --reanuda lo retoma', l1 and not e1 and l2 is None and e2 and l3 and not e3)
    rc = C.main(['--serie', '--pool', '2'])
    despues = set(os.listdir(C.DATOS)) if os.path.isdir(C.DATOS) else set()
    n += 1; n_ok += ok('--serie sin commit (git_limpio) no corre y no crea carpeta', rc == 1 and antes == despues, f"rc {rc}")
    p(f'RESULTADO {n_ok}/{n} en {time.time() - t0:.0f} s')
    open(os.path.join(AQUI, 'identidad_baldwin_salida.txt'), 'w', encoding='utf-8').write('\n'.join(LOG) + '\n')


def letra_sintetica():
    """Carpetas falsas con los campos que lee() usa: comprueba que el codigo da la letra escrita en el preregistro."""
    base = os.path.join(CAR, 'L'); n = 0; k = 0

    def escribe(car, pers, frac, aza=0.5, fijo_inf=19, aprende=100, rompe=None, n_aza_dato=20):
        shutil.rmtree(car, ignore_errors=True); os.makedirs(car)
        for b in C.ORDEN:
            for i, s in enumerate(C.SERIE):
                P = C.PER[b.rsplit('_', 1)[1]]
                ps = pers.get(b, 0) if b != 'FIJO_V_Pinf' else fijo_inf
                fr = aza if b == 'PLAST_AZA_P22k' else frac.get(b, 0.5)
                d = dict(seed=s, brazo=b, T=C.T_DEF, t_corte=C.T_CORTE, bloqueados=0, aborto=None, persiste=int(i < ps), K=10.0, t_ext=None,
                         cfg_worker=dict(C.DEF, **C.cfg_de(b), kit=1),
                         baldwin=dict(frac_pl=(fr if i < 20 else None), n_inv=(3 if P else None), n_aprende=aprende,
                                      frac_pl_ult=(fr if (b != 'PLAST_AZA_P22k' or i < n_aza_dato) else None)))
                if rompe == 'aborto' and b == 'FIJO_V_P6k' and i == 0: d['aborto'] = 'X'
                json.dump(d, open(os.path.join(car, f'M_{b}_s{s}.json'), 'w'))
    casos = [('FUNCIONA', dict(PLAST_V_P22k=18, FIJO_V_P22k=2, PLAST_AZA_P22k=8, PLAST_RW0_P22k=6), dict(PLAST_V_P22k=0.8, PLAST_V_Pinf=0.1), {}),
             ('HAY ALGO MODESTO', dict(PLAST_V_P22k=18, FIJO_V_P22k=2, PLAST_AZA_P22k=8, PLAST_RW0_P22k=6), dict(PLAST_V_P22k=0.8, PLAST_V_Pinf=0.5), {}),
             ('HAY ALGO MODESTO', dict(PLAST_V_P22k=10, FIJO_V_P22k=2, PLAST_AZA_P22k=8, PLAST_RW0_P22k=6), dict(PLAST_V_P22k=0.8, PLAST_V_Pinf=0.1), {}),
             ('NO', dict(PLAST_V_P22k=18, FIJO_V_P22k=2, PLAST_AZA_P22k=16, PLAST_RW0_P22k=6), dict(PLAST_V_P22k=0.8, PLAST_V_Pinf=0.5), {}),
             ('NO SE LEE', dict(PLAST_V_P22k=18, FIJO_V_P22k=2, PLAST_AZA_P22k=8, PLAST_RW0_P22k=6), dict(PLAST_V_P22k=0.8, PLAST_V_Pinf=0.1), dict(fijo_inf=10)),
             ('NO SE LEE', dict(PLAST_V_P22k=18, FIJO_V_P22k=2, PLAST_AZA_P22k=8, PLAST_RW0_P22k=6), dict(PLAST_V_P22k=0.8, PLAST_V_Pinf=0.1), dict(aza=0.95)),
             ('NO SE LEE', dict(PLAST_V_P22k=18, FIJO_V_P22k=2, PLAST_AZA_P22k=8, PLAST_RW0_P22k=6), dict(PLAST_V_P22k=0.8, PLAST_V_Pinf=0.1), dict(rompe='aborto')),
             # AUDITORIA H-1: V5 sobre serie_pl; con < 8 semillas de AZA con dato NO APLICA (aunque la fraccion sea 0.95) y decide PB
             ('FUNCIONA', dict(PLAST_V_P22k=18, FIJO_V_P22k=2, PLAST_AZA_P22k=8, PLAST_RW0_P22k=6), dict(PLAST_V_P22k=0.8, PLAST_V_Pinf=0.1), dict(aza=0.95, n_aza_dato=7)),
             ('NO SE LEE', dict(PLAST_V_P22k=18, FIJO_V_P22k=2, PLAST_AZA_P22k=8, PLAST_RW0_P22k=6), dict(PLAST_V_P22k=0.8, PLAST_V_Pinf=0.1), dict(aza=0.95, n_aza_dato=8))]
    for j, (esp, pers, frac, kw) in enumerate(casos):
        car = os.path.join(base, f'c{j}'); escribe(car, pers, frac, **kw)
        L = C.lee(car, C.SERIE, humo=False, log=lambda s: None)
        n += 1; k += ok(f'caso {j}: espera {esp}', L['veredicto'] == esp, f"da {L['veredicto']} · puertas {L.get('puertas')}")
    return n, k


if __name__ == '__main__':
    main()
