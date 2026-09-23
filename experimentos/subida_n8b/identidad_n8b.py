"""Arnes de identidad de subida_n8b (se corre ANTES de mirar cualquier numero). Escribe identidad_n8b_salida.txt.
Un proceso, sin Pool. Todas las corridas <= 80 000 pasos. Ultima linea: "RESULTADO: N/N"."""
import argparse, contextlib, hashlib, inspect, io, os, subprocess, sys, time

sys.stdout.reconfigure(encoding='utf-8', errors='replace')
AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
sys.path.insert(0, AQUI)
sys.path.insert(0, os.path.join(RAIZ, 'organismo'))
sys.path.insert(0, os.path.join(RAIZ, 'experimentos', 'subida_n8'))
import numpy as np
import construye_n8b as CN
import organismo_n8b as ON
import organismo_flujo as OF
import organismo_v142 as TR
import mundo_n8b as MB
import mundo_n8 as M8
import corre_n8b as CR

NUEVAS = {'n_rec', 'rec_log', 'recicla', 'prueba', 'n_prueba', 'enc_nofam', 'enc_tot'}
R = []


def chk(nombre, ok, det=''):
    R.append(bool(ok))
    print(f"  [{'OK ' if ok else 'MAL'}] {nombre} {det}", flush=True)


def sin_nuevas(d):
    return {k: v for k, v in d.items() if k not in NUEVAS}


def h16(p):
    return hashlib.sha256(open(p, 'rb').read()).hexdigest()[:16]


def plan_de(semilla, n_est, d_pix=13, peso=4, reciclado=False):
    orden, pats, val = MB.mundo(semilla, n_est=n_est, d_pix=d_pix, peso=peso, reciclado=reciclado)
    return orden, pats, val, MB.plan_de(orden, val)


def main():
    t0 = time.time()
    print(f"identidad_n8b  {time.strftime('%Y-%m-%d %H:%M:%S')}")
    V = CR.V142
    # (0) procedencia
    chk('(0a) origen organismo_flujo sha', h16(CN.ORIGEN_ORG) == CN.SHA_ORIGEN_ORG, h16(CN.ORIGEN_ORG))
    chk('(0b) origen mundo_n8 sha', h16(CN.ORIGEN_MUN) == CN.SHA_ORIGEN_MUN, h16(CN.ORIGEN_MUN))
    chk('(0c) tronco organismo_v142 sha', h16(os.path.join(RAIZ, 'organismo', 'organismo_v142.py')) == CR.SHA_TRONCO)
    chk('(0d) organismo_n8b en disco == construye_n8b y == sha del runner',
        open(CN.DEST_ORG, encoding='utf-8').read() == CN.construir_org() and h16(CN.DEST_ORG) == CR.SHA_ORG, h16(CN.DEST_ORG))
    chk('(0e) mundo_n8b en disco == construye_n8b y == sha del runner',
        open(CN.DEST_MUN, encoding='utf-8').read() == CN.construir_mun() and h16(CN.DEST_MUN) == CR.SHA_MUN, h16(CN.DEST_MUN))
    # (A) recicla=0 == organismo_flujo EXACTO, todas las claves
    for s in (1, 2):
        a = ON.run(s, T=20000, **V); b = OF.run(s, T=20000, **V)
        chk(f'(A) s{s} retina 6, T 20000, recicla=0 == organismo_flujo, {len(b)} claves', sin_nuevas(a) == b, f"muertes {a['deaths']}")
    _, pats, _, plan = plan_de(1, 80, d_pix=12, peso=3)
    ch = [MB.t_entrada(i) for i in range(1, 80)]
    for f in (0, 1):
        a = ON.run(1, T=80000, plan=plan, pats=pats, chk=ch, ventana=8, fusion=f, **V)
        b = OF.run(1, T=80000, plan=plan, pats=pats, chk=ch, ventana=8, fusion=f, **V)
        chk(f'(A1) mundo n8 (12 px, peso 3), 80 estimulos, ventana 8, fusion={f}, pool agotado: recicla=0 == organismo_flujo',
            sin_nuevas(a) == b and a['t_agot'] is not None, f"t_agot {a['t_agot']} fus {a['n_fus']}")
    _, pats13, _, plan13 = plan_de(2, 60)
    ch13 = [MB.t_entrada(i) for i in range(1, 60)]
    a = ON.run(2, T=60000, plan=plan13, pats=pats13, chk=ch13, ventana=8, **V)
    b = OF.run(2, T=60000, plan=plan13, pats=pats13, chk=ch13, ventana=8, **V)
    chk('(A2) mundo n8b (13 px, peso 4), 60 estimulos, ventana 8: recicla=0 == organismo_flujo', sin_nuevas(a) == b,
        f"splits {a['splits']} celdas {a['celdas']}")
    # (A3) ancla al TRONCO congelado
    for s in (1, 2, 3):
        a = ON.run(s, T=20000, **V); b = TR.run(s, T=20000)
        ok = all(a[k] == b[k] for k in ('W', 'deaths', 'splits', 'celdas', 'mord', 'vis'))
        chk(f'(A3) s{s} == organismo_v142 en W, muertes, divisiones, celdas, mordidas, visitas', ok, f"W {b['W']}")
    # (B) el organo es INERTE mientras quede celda libre
    _, pats, _, plan = plan_de(1, 12)
    ch = [MB.t_entrada(i) for i in range(1, 12)]
    a0 = ON.run(1, T=12000, plan=plan, pats=pats, chk=ch, ventana=8, recicla=0, **V)
    for f in (1, 2, 3):
        af = ON.run(1, T=12000, plan=plan, pats=pats, chk=ch, ventana=8, recicla=f, **V)
        chk(f'(B) recicla={f} sin agotar el pool == recicla 0 (t_agot {a0["t_agot"]}, celdas {a0["celdas"]})',
            a0['t_agot'] is None and sin_nuevas(af) == sin_nuevas(a0) and af['n_rec'] == 0)
    # (C) con el pool agotado el organo actua, solo despues de agotarlo, y el pool no pasa de 90
    _, pats, _, plan = plan_de(1, 80, d_pix=12, peso=3)   # el mundo n8 agota el pool antes (t 53997); el n8b de 80, tarde (76170)
    ch = [MB.t_entrada(i) for i in range(1, 80)]
    rs = {f: ON.run(1, T=80000, plan=plan, pats=pats, chk=ch, ventana=8, recicla=f, **V) for f in (0, 1, 2, 3)}
    chk('(C1) recicla 1, 2 y 3 reciclan (n_rec > 0) con el pool agotado', all(rs[f]['n_rec'] > 0 for f in (1, 2, 3)),
        f"rel {rs[1]['n_rec']} azar {rs[2]['n_rec']} uso {rs[3]['n_rec']} base t_agot {rs[0]['t_agot']}")
    chk('(C2) todo reciclaje ocurre con el pool ya agotado (t >= t_agot)',
        all(rs[f]['t_agot'] is not None and all(t >= rs[f]['t_agot'] for t, _, _ in rs[f]['rec_log']) for f in (1, 2, 3)))
    chk('(C3) celdas <= 90 al final', all(rs[f]['celdas'] <= 90 for f in (0, 1, 2, 3)), str([rs[f]['celdas'] for f in (0, 1, 2, 3)]))
    chk('(C4) relevancia, uso y azar liberan celdas distintas', len({tuple(x[1] for x in rs[f]['rec_log'][:20]) for f in (1, 2, 3)}) == 3)
    t1 = min(rs[f]['rec_log'][0][0] for f in (1, 2, 3))
    chk('(C5) hasta el primer reciclaje, rel == uso == azar == base (mismo t_agot, mismas divisiones)',
        rs[1]['t_agot'] == rs[0]['t_agot'] == rs[2]['t_agot'] == rs[3]['t_agot'] and
        all([x for x in rs[f]['split_t'] if x[0] < t1] == [x for x in rs[0]['split_t'] if x[0] < t1] for f in (1, 2, 3)))
    import statistics as st
    mr = st.median([x[2] for x in rs[1]['rec_log']]); ma = st.median([x[2] for x in rs[2]['rec_log']])
    chk('(C6) la relevancia liberada por rel es menor que la liberada al azar (mediana |Wp-Wn|)', mr <= ma, f'rel {mr} azar {ma}')
    # (D) determinismo
    for f in (1, 3):
        b1 = ON.run(1, T=80000, plan=plan, pats=pats, chk=ch, ventana=8, recicla=f, **V)
        chk(f'(D) determinismo recicla {f}', b1 == rs[f])
    # (P) organo de PRUEBA: actua desde el principio (no depende del pool), solo en la decision de morder
    _, pats, _, plan = plan_de(4, 30)
    ch = [MB.t_entrada(i) for i in range(1, 30)]
    rp = {f: ON.run(4, T=30000, plan=plan, pats=pats, chk=ch, ventana=8, prueba=f, **V) for f in (0, 1, 2)}
    chk('(P1) prueba=0: contadores en cero', rp[0]['n_prueba'] == 0 and rp[0]['enc_tot'] == 0)
    chk('(P2) prueba=1: lectura neutra EXACTAMENTE en los encuentros no reconocidos, y cambia la trayectoria',
        rp[1]['n_prueba'] == rp[1]['enc_nofam'] > 0 and rp[1]['mord'] != rp[0]['mord'], f"{rp[1]['n_prueba']}/{rp[1]['enc_tot']}")
    f1 = rp[1]['enc_nofam'] / rp[1]['enc_tot']; f2 = rp[2]['n_prueba'] / rp[2]['enc_tot']; f2n = rp[2]['enc_nofam'] / rp[2]['enc_tot']
    chk('(P3) prueba=2: tasa de lecturas neutras al azar == su propia tasa de no reconocidos (+-0.05)', abs(f2 - f2n) <= 0.05,
        f'neutras {f2:.3f} no reconocidos {f2n:.3f} (prueba=1: {f1:.3f})')
    b2 = ON.run(4, T=30000, plan=plan, pats=pats, chk=ch, ventana=8, prueba=2, **V)
    chk('(P4) determinismo prueba 2', b2 == rp[2])
    src_ = open(CN.DEST_ORG, encoding='utf-8').read().splitlines()
    lp = [l for l in src_ if '_npru' in l or '_enc' in l or '_rngp' in l]
    chk('(P5) la prueba no lee valencias, R_VAL, el plan ni E; no toca dlt, Wp/Wn ni valor_tot',
        not any(w in l for l in lp for w in ('val[', 'R_VAL', 'plan', 'E_VAL', 'dlt', 'Wp', 'Wn', 'valor_tot')), f'{len(lp)} lineas')
    # (E) mundo
    ok0 = True
    for s in range(1, 41):
        a = MB.mundo(s, n_est=200, d_pix=12, peso=3); b = M8.mundo(s)
        ok0 &= a[0] == b[0] and a[2] == b[2] and all(np.array_equal(a[1][k], b[1][k]) for k in b[1]) and set(a[1]) == set(b[1])
        ar = MB.mundo(s, n_est=200, d_pix=12, peso=3, reciclado=True); br = M8.mundo(s, reciclado=True)
        ok0 &= ar[0] == br[0] and ar[2] == br[2]
    chk('(E0) mundo_n8b(12 px, peso 3, 200) == mundo_n8 (flujo y reciclado, semillas 1-40)', ok0)
    okb = True
    for s in range(1, 41):
        o, p, v = MB.mundo(s)
        for i in range(0, MB.N_EST, MB.BLOQUE):
            okb &= [v[o[j]] for j in range(i, i + MB.BLOQUE)].count('comida') == MB.BLOQUE // 2
    chk('(E1) mundo largo: valencias 5/5 en cada bloque de 10 (500 estimulos, semillas 1-40)', okb)
    o, p, v = MB.mundo(7)
    chk('(E2) 500 patrones distintos de peso 4 sobre 13 pixeles; T = 500 000',
        len(o) == 500 and len({tuple(x) for x in p.values()}) == 500 and all(x.sum() == 4 and len(x) == 13 for x in p.values())
        and MB.T_de() == 500000)
    o2, p2, v2 = MB.mundo(7, n_est=200)
    chk('(E3) el mundo del humo (200) es el PREFIJO del de la serie (500): mismo orden, patrones y valencias',
        o2 == o[:200] and all(np.array_equal(p2[k], p[k]) and v2[k] == v[k] for k in p2))
    orr, prr, vrr = MB.mundo(7, reciclado=True)
    chk('(E4) RECICLADO: 20 primeros == FLUJO; despues solo repeticiones con la misma valencia',
        orr[:20] == o[:20] and all(orr[i] in orr[:20] for i in range(20, 500)) and all(vrr[n] == v[n] for n in prr) and len(prr) == 20)
    # (F) estatico
    src = open(CN.DEST_ORG, encoding='utf-8').read(); ori = open(CN.ORIGEN_ORG, encoding='utf-8').read()
    chk('(F1) llamadas al rng principal: las mismas que el origen; _rngr y _rngp solo en 2 lineas cada uno',
        src.count('rng.') == ori.count('rng.') and sum(1 for l in src.splitlines() if '_rngr' in l) == 2
        and sum(1 for l in src.splitlines() if '_rngp' in l) == 2)
    lin = src.splitlines(); i0 = next(i for i, l in enumerate(lin) if l.startswith('    def _reciclar'))
    i1 = next(i for i in range(i0, len(lin)) if lin[i].strip() == 'return True')
    cuerpo = lin[i0:i1 + 1]
    chk('(F2) el organo no lee valencias, R_VAL, el plan ni los patrones (sin canal hacia la respuesta)',
        not any(w in l for l in cuerpo for w in ('val[', 'R_VAL', 'plan', 'pats[', 'E_VAL')), f'{len(cuerpo)} lineas')
    # (G) regla 14
    malos, filas = CR.entrada_campo_a_campo()
    chk(f'(G) entrada campo a campo contra organismo_v142: {len(filas)} campos, 0 distintos', not malos, str(malos))
    # (H) el runner ABORTA ante banderas desconocidas o mal combinadas (ERR-115). Nunca se ejecuta con --serie:
    #     la rama --serie se valida llamando a plan_de_corrida() en proceso, sin correr nada.
    runner = os.path.join(AQUI, 'corre_n8b.py')
    antes = set(os.listdir(os.path.join(AQUI, 'datos'))) if os.path.isdir(os.path.join(AQUI, 'datos')) else set()
    for args in (['--bogus'], ['--hum'], ['--humo', '--semila_humo', '14890'], []):
        pr = subprocess.run([sys.executable, runner] + args, capture_output=True, text=True, timeout=60)
        chk(f'(H1) corre_n8b.py {" ".join(args) or "(sin modo)"} aborta con error de argparse', pr.returncode == 2, f'rc {pr.returncode}')
    pr = subprocess.run([sys.executable, runner, '--humo', '--pool', '6'], capture_output=True, text=True, timeout=120)
    chk('(H2) --humo --pool 6 aborta antes de correr', pr.returncode != 0 and 'Abortado' in (pr.stderr + pr.stdout), f'rc {pr.returncode}')
    despues = set(os.listdir(os.path.join(AQUI, 'datos'))) if os.path.isdir(os.path.join(AQUI, 'datos')) else set()
    chk('(H3) ninguna de esas llamadas escribio datos', antes == despues)
    NS = lambda **k: argparse.Namespace(**{**dict(humo=False, serie=None, veredicto=None, desde=None, n=None, pool=None,
                                                    semilla_humo=14893), **k})
    malas = [NS(serie='base,prueba,azr,recic', desde=14801, n=20, pool=6), NS(serie='base', desde=12601, n=20, pool=6),
             NS(serie='base', desde=14801, n=5, pool=6), NS(serie='base', desde=14801, n=20, pool=None),
             NS(humo=True, semilla_humo=14801), NS(humo=True, n=20)]
    aborta = 0
    for ns in malas:
        try:
            CR.plan_de_corrida(ns)
        except SystemExit:
            aborta += 1
    chk(f'(H4) plan_de_corrida aborta en {len(malas)} combinaciones malas (brazo mal escrito, semilla ajena, n != 20, sin pool, humo con semilla de serie, humo con --n)',
        aborta == len(malas), f'{aborta}/{len(malas)}')
    b_, s_, n_, _, p_ = CR.plan_de_corrida(NS(serie='base,prueba,prazar,uso,pruso,pruazar,recic', desde=14821, n=20, pool=6))
    chk('(H5) la combinacion buena de la replica da 7 brazos x 20 semillas 14821-14840, 500 estimulos',
        b_ == ['base', 'prueba', 'prazar', 'uso', 'pruso', 'pruazar', 'recic'] and s_ == list(range(14821, 14841)) and n_ == 500 and p_.startswith('n8b_replica_'))
    # (I) la LETRA del veredicto (corre_n8b.predicciones / veredicto) sobre resultados SINTETICOS (no son datos)
    def sint(brazo, s, **k):
        d = dict(semilla=s, brazo=brazo, ADQ_tarde=0.7, ADQ_medio=0.7, ADQ_temprano=0.8, PRIOR_tarde=0.5, NULO_tarde=0.5,
                 ADQ_tarde_com=0.4, ADQ_tarde_ven=1.0, ADQ_medio_com=0.4, ADQ_temprano_com=0.8, PRIOR_tarde_com=0.1, PRIOR_tarde_ven=0.9,
                 RET40=0.6, RET40_com=0.2, RET_todo=0.6, cond_ult_cuarto=0.05, muertes=400, splits=60, n_rec=0, rec_rel_mediana=None,
                 n_prueba=0, frac_nofam=None, mc_tot=500, mv_tot=300, est_agot=70, dur_s=1.0,
                 curva_ADQ_bloques10=[0.7], curva_com_bloques10=[0.4])
        d.update(k); return d
    def lote(bueno=True, recic_ok=True):
        res = []
        for s in range(20):
            res.append(sint('base', s))
            res.append(sint('prueba', s, ADQ_tarde_com=0.6 if bueno else 0.4, ADQ_medio_com=0.6, muertes=300 if bueno else 400,
                            ADQ_temprano_com=0.9))
            res.append(sint('prazar', s, ADQ_tarde_com=0.5 if bueno else 0.4, muertes=400 if bueno else 300))
            res.append(sint('uso', s))
            res.append(sint('pruso', s, ADQ_tarde_com=0.7 if bueno else 0.4, ADQ_medio_com=0.7, muertes=300))
            res.append(sint('pruazar', s, ADQ_tarde_com=0.6 if bueno else 0.4, muertes=300))
            res.append(sint('recic', s, ADQ_tarde=0.95 if recic_ok else 0.7))
        return res
    e_b, _ = CR.predicciones(lote(True)); e_m, _ = CR.predicciones(lote(False)); e_r, _ = CR.predicciones(lote(True, False))
    v_b = CR.veredicto(e_b, e_b); v_m = CR.veredicto(e_m, e_m); v_r = CR.veredicto(e_r, e_b); v_x = CR.veredicto(e_b, e_m)
    chk('(I1) sintetico favorable en las dos -> FUNCIONA (piezas 1 +5, 4 +5, 3 entera +15 = +25)', v_b[0] == 'FUNCIONA' and v_b[2] == 25, str(v_b))
    chk('(I2) sintetico sin efecto -> no FUNCIONA', v_m[0] in ('NO', 'HAY ALGO MODESTO') and v_m[0] != 'FUNCIONA', str(v_m))
    chk('(I3) RECIC no ve la novedad en una serie -> NO SE LEE', v_r[0] == 'NO SE LEE', str(v_r))
    chk('(I4) favorable en una serie y no en la otra -> no FUNCIONA', v_x[0] != 'FUNCIONA', str(v_x))
    import json, tempfile
    with tempfile.TemporaryDirectory() as td:
        rutas = []
        for nom in ('serie', 'replica'):
            rr = os.path.join(td, nom + '.json')
            json.dump(dict(humo=False, n_est=500, shas=dict(organismo_n8b=CR.SHA_ORG, mundo_n8b=CR.SHA_MUN), semillas=list(range(20)), resultados=lote(True)), open(rr, 'w', encoding='utf-8'))
            rutas.append(rr)
        pr = subprocess.run([sys.executable, runner, '--veredicto'] + rutas, capture_output=True, text=True, timeout=60, encoding='utf-8')
        ult = pr.stdout.strip().splitlines()[-1] if pr.stdout.strip() else ''
    chk('(I5) --veredicto lee dos JSON, no corre nada, y su ULTIMA linea es la letra', pr.returncode == 0 and ult.startswith('VEREDICTO') and 'FUNCIONA' in ult, ult[:90])
    n_ok = sum(R)
    print(f"TOTAL {n_ok}/{len(R)} en {time.time() - t0:.1f}s")
    print(f"RESULTADO: {n_ok}/{len(R)}")
    return n_ok == len(R)


if __name__ == '__main__':
    buf = io.StringIO()

    class Tee:
        def write(self, x):
            sys.__stdout__.write(x); buf.write(x)

        def flush(self):
            sys.__stdout__.flush()
    with contextlib.redirect_stdout(Tee()):
        ok = main()
    open(os.path.join(AQUI, 'identidad_n8b_salida.txt'), 'w', encoding='utf-8').write(buf.getvalue())
    sys.exit(0 if ok else 1)
