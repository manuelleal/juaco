"""identidad_bexp.py — arnes de BALDWIN CON EXPLORACION (29-sep-2026). UN proceso; T corto (30 000; Q 40 000); semillas 56691-56694.
Salida: identidad_bexp_salida.txt. Mision: llegar a la AGI por este camino.

(K) motor_bexp == construccion por anclas desde motor_baldwin (sha fijado); shas de la entrada.
(A) PERILLA APAGADA (exp = 0) == motor_baldwin BIT A BIT (regla 14: la entrada entera, campo a campo, + el BQ_OUT salvo cfg y 'exp'):
    A1 FIJO_V_Pinf (plast 0) · A2 PLAST_V_P22k (plast 1, con la inversion en 22 000) · A3 PLAST_AZA_P22k (plast 2)
    A4 la PUERTA de la reserva: exp = 1 con th_exp = 2.0 (inalcanzable: la reserva satura en 1.5) == exp = 0 (no se consume azar).
(B) CONTROLES QUE DEBEN DIFERIR (P 22 000, s56693, T 60 000, eps del arnes 0.1): PLAST_EXP != PLAST_V; FIJO_EXP != FIJO_V; PLAST_EXP_AZA != PLAST_EXP;
    la exploracion actua (n_mord_exp > 0) en los tres brazos EXP y es 0 en PLAST_V y FIJO_V; en PLAST_EXP la exploracion hace aprender a
    una regla plastica (n_mord_exp_aprende > 0); FIJO_EXP no aprende reglas (n_aprende None); |w - w0| se mide en los MUERTOS (reglas > 0).
(G) contadores coherentes: n_mord_exp <= n_veto_res <= n_veto, y n_mord_exp / n_veto_res ~ eps (binomial, |z| < 5).
(Q) corte en 30 000 + reanuda == la corrida entera (PLAST_EXP_P22k, T 40 000).   (D) determinismo (PLAST_EXP_P22k dos veces).
(L) la LETRA de lee() en entradas sinteticas.   (R) banderas y candados de main().
"""
import json, math, os, shutil, sys, time
AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI); sys.path.insert(0, os.path.join(os.path.dirname(AQUI), 'baldwin'))
import corre_baldwin as CW   # noqa: E402  (motor_baldwin; al importarse deja CB.usa_bloques = usa_baldwin)
import corre_bexp as C   # noqa: E402  (deja CB.usa_bloques = usa_bexp)
CB = C.CB; NS = C.NS
CAR = os.path.join(C.DATOS, 'arnes')
EPS_A = 0.1   # eps SOLO del arnes (no es el de la serie)
TB = 60000   # (B) y (G): mas largo, para que haya vetos con reserva en los tres brazos EXP
LOG = []
TA = 30000
XTRA = {'PLAST_AZA': (2, 0)}   # brazo SOLO del arnes (FIJO_V_P22k sale de MODO)


def p(*a):
    s = ' '.join(str(x) for x in a); print(s, flush=True); LOG.append(s)


def ok(nombre, cond, info=''):
    p(f"  [{'OK ' if cond else 'MAL'}] {nombre} {info}"); return bool(cond)


def cfg_x(brazo, **kw):
    arm, cond = brazo.rsplit('_', 1)
    if arm in XTRA:
        pl, ex = XTRA[arm]; c = dict(C.cfg_de('PLAST_V_' + cond, EPS_A), plast=pl, exp=ex, eps_exp=0.0)
    else: c = C.cfg_de(brazo, EPS_A)
    c.update(kw); return c


def corre_x(seed, brazo, car, TT=TA, **kw):
    """corre_bexp.corre con la cfg del arnes."""
    NS.BRAZOS[brazo] = ('MUT0', CB.FAB, C.T_CORTE); CB.BQ[brazo] = cfg_x(brazo, **kw)
    CB.usa_bloques = C.usa_bexp
    return C.corre(seed, brazo, TT, os.path.join(CAR, car))


def corre_w(seed, brazo, car, TT=TA):
    """corre_baldwin.corre (motor_baldwin) con SU cfg (la de la serie BALDWIN)."""
    arm, cond = brazo.rsplit('_', 1)
    NS.BRAZOS[brazo] = ('MUT0', CB.FAB, C.T_CORTE); CB.BQ[brazo] = CW.cfg_de(brazo)
    CB.usa_bloques = CW.usa_baldwin
    try:
        return CW.corre(seed, brazo, TT, os.path.join(CAR, car))
    finally:
        CB.usa_bloques = C.usa_bexp


def difs(a, b, fuera=('seg', 'brazo', 'cfg_worker', 'baldwin', 'bexp', 'bloques', '_seg_job')):
    return [k for k in sorted(set(a) | set(b)) if k not in fuera and json.dumps(a.get(k), sort_keys=True) != json.dumps(b.get(k), sort_keys=True)]


def jb(o, fuera=('cfg', 'exp')):
    B = {k: v for k, v in (o.get('bloques') or {}).items() if k not in fuera}
    return json.dumps(B, sort_keys=True)


def main():
    t0 = time.time(); n = 0; n_ok = 0
    shutil.rmtree(CAR, ignore_errors=True)
    p('identidad_bexp.py', time.strftime('%Y-%m-%d %H:%M:%S'), f'T {TA}', f'eps del arnes {EPS_A}', f'th_exp {C.TH_EXP}')
    p('(K) construccion y shas')
    import subprocess
    out = subprocess.run([sys.executable, os.path.join(AQUI, 'construye_bexp.py'), '--verifica'], capture_output=True, text=True).stdout.strip()
    n += 1; n_ok += ok('construye_bexp --verifica', out.startswith('IGUAL'), out)
    shas_ok = all(C.h16(r) == s for r, s in C.SHAS.items())
    n += 1; n_ok += ok('shas de la entrada (corre_bloques, motor_baldwin, construye_baldwin, motor_bexp)', shas_ok,
                       ' '.join(f"{os.path.basename(r)} {C.h16(r)}" for r in C.SHAS))
    p(f"  (verifica() completa, con EPS_EXP calibrado: {C.verifica(log=lambda s: None)} · EPS_EXP {C.EPS_EXP})")

    p('(A) perilla apagada (exp = 0) == motor_baldwin bit a bit')
    for nom, br, sd in (('A1', 'FIJO_V_Pinf', 56691), ('A2', 'PLAST_V_P22k', 56692), ('A3', 'PLAST_AZA_P22k', 56692)):
        ow = corre_w(sd, br, f'{nom}_w'); ox = corre_x(sd, br, f'{nom}_x')
        d = difs(ow, ox); igB = jb(ow) == jb(ox)
        n += 1; n_ok += ok(f'{nom} {br}: motor_bexp == motor_baldwin (campo a campo + BQ_OUT)', not d and igB and ow.get('aborto') is None,
                           f"distintas {d} · BQ_OUT igual {igB} · K {ox.get('K')} · hijos {(ox.get('bloques') or {}).get('n_hijos')} · "
                           f"aprende {(ox.get('bloques') or {}).get('n_aprende')} · n_inv {(ox.get('bloques') or {}).get('n_inv')} · "
                           f"vetos {((ox.get('bloques') or {}).get('exp') or {}).get('n_veto')}")
        if nom == 'A2': oA2 = ox
    o4 = corre_x(56692, 'PLAST_EXP_P22k', 'A4', th_exp=2.0)
    d = difs(oA2, o4)
    n += 1; n_ok += ok('A4 exp = 1 con th_exp 2.0 (puerta cerrada) == PLAST_V_P22k (exp = 0)', not d and jb(oA2) == jb(o4) and o4['bexp']['n_mord_exp'] == 0,
                       f"distintas {d} · mord_exp {o4['bexp']['n_mord_exp']} · vetos {o4['bexp']['n_veto']} · con reserva {o4['bexp']['n_veto_res']}")

    p(f'(B) controles que deben diferir (P 22 000, s56693, T {TB}, eps {EPS_A})')
    R = {br: corre_x(56693, br, 'b', TT=TB) for br in ('PLAST_EXP_P22k', 'PLAST_V_P22k', 'FIJO_EXP_P22k', 'FIJO_V_P22k', 'PLAST_EXP_AZA_P22k')}
    for a_, b_ in (('PLAST_EXP_P22k', 'PLAST_V_P22k'), ('FIJO_EXP_P22k', 'FIJO_V_P22k'), ('PLAST_EXP_AZA_P22k', 'PLAST_EXP_P22k')):
        d = difs(R[a_], R[b_]) + (['bloques'] if jb(R[a_]) != jb(R[b_]) else [])
        n += 1; n_ok += ok(f'{a_} != {b_}', len(d) > 0, f"{len(d)} claves distintas · K {R[a_].get('K')} vs {R[b_].get('K')}")
    for br in ('PLAST_EXP_P22k', 'FIJO_EXP_P22k', 'PLAST_EXP_AZA_P22k'):
        x = R[br]['bexp']
        n += 1; n_ok += ok(f'{br}: la exploracion actua (n_mord_exp > 0)', (x['n_mord_exp'] or 0) > 0,
                           f"mord_exp {x['n_mord_exp']} (R+ {x['n_exp_R_pos']}, R- {x['n_exp_R_neg']}) · exp/vida {x['exp_por_vida']} · vetos con reserva/vida {x['veto_res_por_vida']}")
    for br in ('PLAST_V_P22k',):
        n += 1; n_ok += ok(f'{br}: sin exploracion (n_mord_exp == 0)', R[br]['bexp']['n_mord_exp'] == 0, f"mord_exp {R[br]['bexp']['n_mord_exp']}")
    n += 1; n_ok += ok('FIJO_V_P22k: sin bloque exp (plast 0, exp 0: el motor no escribe nada nuevo)', 'exp' not in (R['FIJO_V_P22k'].get('bloques') or {}))
    x = R['PLAST_EXP_P22k']['bexp']
    n += 1; n_ok += ok('PLAST_EXP: la exploracion hace aprender a una regla plastica (n_mord_exp_aprende > 0)', (x['n_mord_exp_aprende'] or 0) > 0,
                       f"{x['n_mord_exp_aprende']} de {x['n_mord_exp']}")
    n += 1; n_ok += ok('PLAST_EXP: |w - w0| medido en los MUERTOS (reglas plasticas de boca de muertos > 0)',
                       (((R['PLAST_EXP_P22k']['bloques'].get('exp') or {}).get('muertos') or {}).get('n_reglas_pl') or 0) > 0,
                       f"muertos {R['PLAST_EXP_P22k']['bloques']['exp']['muertos']} · vivos {R['PLAST_EXP_P22k']['bloques']['exp']['vivos_T']} · "
                       f"pl_movidas {x['pl_movidas']}/{x['pl_reglas']}")
    n += 1; n_ok += ok('FIJO_EXP: no aprende reglas (n_aprende None)', R['FIJO_EXP_P22k']['bloques'].get('n_aprende') is None)

    p('(G) contadores coherentes')
    for br in ('PLAST_EXP_P22k', 'FIJO_EXP_P22k', 'PLAST_EXP_AZA_P22k'):
        x = R[br]['bexp']; m, nr = x['n_mord_exp'], x['n_veto_res']
        z = (m - EPS_A * nr) / math.sqrt(max(1e-9, nr * EPS_A * (1 - EPS_A)))
        n += 1; n_ok += ok(f'{br}: mord_exp <= vetos con reserva <= vetos; mord_exp/vetos_res ~ eps', m <= nr <= x['n_veto'] and abs(z) < 5,
                           f"{m} <= {nr} <= {x['n_veto']} · tasa {m / max(1, nr):.4f} · z {z:.2f}")

    p('(Q) corte en 30 000 + reanuda == entera (PLAST_EXP_P22k, T 40 000, s56694)')
    TQ = 40000
    ent = corre_x(56694, 'PLAST_EXP_P22k', 'Qa', TT=TQ)
    NS.BRAZOS['PLAST_EXP_P22k'] = ('MUT0', CB.FAB, C.T_CORTE); CB.BQ['PLAST_EXP_P22k'] = cfg_x('PLAST_EXP_P22k')
    MX = C.usa_bexp()
    orig = NS.CR.ME.run_solapadas

    def corta(*a, _o=orig, **k):
        fn = k['eco']['ckpt_fn']

        def fn2(tt, blob):
            fn(tt, blob)
            if tt == 30000: raise KeyboardInterrupt('corte simulado')
        k['eco'] = dict(k['eco'], ckpt_fn=fn2)
        return _o(*a, **k)
    cortado = False
    CB.usa_bloques = lambda: (setattr(NS.CR.ME, 'run_solapadas', corta) or MX)
    try:
        C.corre(56694, 'PLAST_EXP_P22k', TQ, os.path.join(CAR, 'Qb'))
    except KeyboardInterrupt:
        cortado = True
    finally:
        CB.usa_bloques = C.usa_bexp
    rea = C.corre(56694, 'PLAST_EXP_P22k', TQ, os.path.join(CAR, 'Qb'), reanuda=True)
    d = difs(ent, rea)
    n += 1; n_ok += ok('corte + reanuda == entera', cortado and not d and jb(ent, ()) == jb(rea, ()) and ent['bexp'] == rea['bexp'],
                       f"cortado {cortado} · distintas {d} · mord_exp {ent['bexp']['n_mord_exp']}/{rea['bexp']['n_mord_exp']} · n_inv {ent['baldwin']['n_inv']}/{rea['baldwin']['n_inv']}")

    p('(D) determinismo')
    da = corre_x(56694, 'PLAST_EXP_P22k', 'Da'); db = corre_x(56694, 'PLAST_EXP_P22k', 'Db')
    n += 1; n_ok += ok('PLAST_EXP_P22k dos veces ==', not difs(da, db) and jb(da, ()) == jb(db, ()) and da['bexp'] == db['bexp'])

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
    open(os.path.join(AQUI, 'identidad_bexp_salida.txt'), 'w', encoding='utf-8').write('\n'.join(LOG) + '\n')


def letra_sintetica():
    """Carpetas falsas con los campos que lee() usa: el codigo da la letra escrita en el preregistro."""
    base = os.path.join(CAR, 'L'); n = 0; k = 0
    eps = 0.01

    def escribe(car, pers, frac, aza=0.5, fijo_inf=19, mexp=50, mov=10, rompe=None, n_aza_dato=20, frac_T_vivo=True, expapr=5):
        shutil.rmtree(car, ignore_errors=True); os.makedirs(car)
        for b in C.ORDEN:
            for i, s in enumerate(C.SERIE):
                P = C.PER[b.rsplit('_', 1)[1]]
                ps = pers.get(b, 0) if b != 'FIJO_V_Pinf' else fijo_inf
                fr = aza if b == 'PLAST_EXP_AZA_P22k' else frac.get(b, 0.5)
                viv = i < ps
                ex = C.MODO[b.rsplit('_', 1)[0]][1]
                d = dict(seed=s, brazo=b, T=C.T_DEF, t_corte=C.T_CORTE, bloqueados=0, aborto=None, persiste=int(viv), K=10.0, t_ext=None,
                         cfg_worker=dict(C.DEF, **C.cfg_de(b, eps), kit=1),
                         baldwin=dict(frac_pl=(fr if (viv and frac_T_vivo) else None), n_inv=(5 if P else None),
                                      frac_pl_ult=(fr if (b != 'PLAST_EXP_AZA_P22k' or i < n_aza_dato) else None),
                                      frac_pl_fin=(fr if (b != 'PLAST_EXP_AZA_P22k' or i < n_aza_dato) else None)),
                         bexp=dict(n_mord_exp=(mexp if ex else 0), pl_movidas=(mov if 'PLAST' in b else 0), n_mord_exp_aprende=(expapr if (ex and 'PLAST' in b) else 0)))
                if rompe == 'aborto' and b == 'FIJO_EXP_P22k' and i == 0: d['aborto'] = 'X'
                if rompe == 'exp_en_V' and b == 'PLAST_V_P22k' and i == 0: d['bexp']['n_mord_exp'] = 3
                json.dump(d, open(os.path.join(car, f'M_{b}_s{s}.json'), 'w'))
    B = dict(PLAST_EXP_P22k=17, FIJO_EXP_P22k=3, PLAST_EXP_AZA_P22k=9)
    casos = [('FUNCIONA', B, dict(PLAST_EXP_P22k=0.8), {}),
             ('HAY ALGO MODESTO', B, dict(PLAST_EXP_P22k=0.3), {}),   # sin frac_pl
             ('HAY ALGO MODESTO', dict(PLAST_EXP_P22k=12, FIJO_EXP_P22k=3, PLAST_EXP_AZA_P22k=6), dict(PLAST_EXP_P22k=0.8), {}),   # < 15
             ('NO', dict(PLAST_EXP_P22k=17, FIJO_EXP_P22k=13, PLAST_EXP_AZA_P22k=9), dict(PLAST_EXP_P22k=0.8), {}),   # explorar basta
             ('NO', dict(PLAST_EXP_P22k=17, FIJO_EXP_P22k=3, PLAST_EXP_AZA_P22k=14), dict(PLAST_EXP_P22k=0.8), {}),   # AZA igual
             ('NO SE LEE', B, dict(PLAST_EXP_P22k=0.8), dict(fijo_inf=10)),
             ('NO SE LEE', B, dict(PLAST_EXP_P22k=0.8), dict(rompe='aborto')),
             ('NO SE LEE', B, dict(PLAST_EXP_P22k=0.8), dict(mexp=0)),   # la exploracion no actua
             ('NO SE LEE', B, dict(PLAST_EXP_P22k=0.8), dict(mov=0)),   # la regla plastica no aprende
             ('NO SE LEE', B, dict(PLAST_EXP_P22k=0.8), dict(rompe='exp_en_V')),
             ('NO SE LEE', B, dict(PLAST_EXP_P22k=0.8), dict(aza=0.95)),   # V6 aplica y falla
             ('FUNCIONA', B, dict(PLAST_EXP_P22k=0.8), dict(aza=0.95, n_aza_dato=7)),   # V6 no aplica
             # ERR-156 (auditoria antes de datos)
             ('NO SE LEE', B, dict(PLAST_EXP_P22k=0.8), dict(expapr=0)),   # H-1: la regla se mueve, pero no por la exploracion
             ('FUNCIONA', B, dict(PLAST_EXP_P22k=0.8), dict(fijo_inf=13)),   # H-2: ancla 13/20 basta
             ('NO SE LEE', B, dict(PLAST_EXP_P22k=0.8), dict(fijo_inf=12)),   # H-2: 12/20 no
             ('NO', dict(PLAST_EXP_P22k=17, FIJO_EXP_P22k=13, PLAST_EXP_AZA_P22k=9), dict(PLAST_EXP_P22k=0.8), {}),   # H-3: PM a 1 -> replica
             ('NO', dict(PLAST_EXP_P22k=2, FIJO_EXP_P22k=12, PLAST_EXP_AZA_P22k=10), dict(PLAST_EXP_P22k=0.8), {}),   # H-3: lejos -> sin replica
             ('NO SE LEE', dict(PLAST_EXP_P22k=17, FIJO_EXP_P22k=13, PLAST_EXP_AZA_P22k=9), dict(PLAST_EXP_P22k=0.8), dict(fijo_inf=12))]   # H-3: NO SE LEE nunca replica
    REPL = {15: True, 16: False, 17: False, 0: True, 1: True}   # ERR-156 H-3: caso -> replica permitida
    for j, (esp, pers, frac, kw) in enumerate(casos):
        car = os.path.join(base, f'c{j}'); escribe(car, pers, frac, **kw)
        L = C.lee(car, C.SERIE, humo=False, log=lambda s: None, eps=eps)
        n += 1; k += ok(f'caso {j}: espera {esp}', L['veredicto'] == esp, f"da {L['veredicto']} · puertas {L.get('puertas')} · validez falla {[a for a, b in (L.get('validez') or {}).items() if not b]}")
        if j in REPL:
            rp = C.replica_permitida(dict(letra=L))
            n += 1; k += ok(f'caso {j}: replica permitida == {REPL[j]} (ERR-156 H-3)', rp == REPL[j], f"cerca {L.get('cerca_umbral')}")
        if j == 0:
            dd = (L.get('secundarias') or {}).get('desc_PLAST_EXP_vs_PLAST_V_P22k')
            n += 1; k += ok('caso 0: descriptivo PLAST_EXP vs PLAST_V_P22k presente (ERR-156 H-4)', dd is not None and dd['dif'] == 17, f"{dd}")
    return n, k


if __name__ == '__main__':
    main()
