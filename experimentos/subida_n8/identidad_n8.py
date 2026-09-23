"""Arnes de identidad de subida_n8 (se corre ANTES de mirar cualquier numero). Escribe identidad_n8_salida.txt.
Un proceso, sin Pool. Todas las corridas <= 80 000 pasos."""
import hashlib, inspect, io, os, sys, time, contextlib

sys.stdout.reconfigure(encoding='utf-8', errors='replace')
AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
sys.path.insert(0, AQUI)
sys.path.insert(0, os.path.join(RAIZ, 'organismo'))
sys.path.insert(0, os.path.join(RAIZ, 'experimentos', 'nivel10_composicion_v14'))
import numpy as np
import construye_n8 as CN
import organismo_flujo as OF
import organismo_capBD_on as CB
import organismo_v142 as TR
import mundo_n8 as MN
import corre_n8 as CR

NUEVAS = {'n_fus', 'fus_log', 'ventana', 'fusion'}
R = []


def chk(nombre, ok, det=''):
    R.append(ok)
    print(f"  [{'OK ' if ok else 'MAL'}] {nombre} {det}", flush=True)


def sin_nuevas(d):
    return {k: v for k, v in d.items() if k not in NUEVAS}


def h16(p):
    return hashlib.sha256(open(p, 'rb').read()).hexdigest()[:16]


def plan12(semilla, n_est, reciclado=False):
    orden, pats, val = MN.mundo(semilla, n_est=n_est, reciclado=reciclado)
    return orden, pats, val, MN.plan_de(orden, val)


def main():
    t0 = time.time()
    print(f"identidad_n8  {time.strftime('%Y-%m-%d %H:%M:%S')}")
    # (0) procedencia
    chk('(0a) origen capBD_on sha', h16(CN.ORIGEN) == CN.SHA_ORIGEN, h16(CN.ORIGEN))
    chk('(0b) tronco organismo_v142 sha', h16(os.path.join(RAIZ, 'organismo', 'organismo_v142.py')) == CR.SHA_TRONCO)
    chk('(0c) organismo_flujo en disco == construye_n8 y == sha del runner',
        open(os.path.join(AQUI, 'organismo_flujo.py'), encoding='utf-8').read() == CN.construir()
        and h16(os.path.join(AQUI, 'organismo_flujo.py')) == CR.SHA_FLUJO, h16(os.path.join(AQUI, 'organismo_flujo.py')))
    V = CR.V142
    # (A) perillas apagadas == capBD_on EXACTO, todas las claves (retina 6, mundo de dos estimulos)
    for s in (1, 2, 3):
        a = OF.run(s, T=20000, **V); b = CB.run(s, T=20000, **V)
        chk(f'(A) s{s} ventana=0 fusion=0 == capBD_on, retina 6, T 20000, {len(b)} claves', sin_nuevas(a) == b,
            f"muertes {a['deaths']} W {a['W']}")
    # (A1) idem en el mundo de 12 pixeles con fotos (plan del flujo, sin ventana)
    for s in (1, 2):
        _, pats, _, plan = plan12(s, 30)
        ch = [MN.t_entrada(i) for i in range(1, 30)]
        a = OF.run(s, T=30000, plan=plan, pats=pats, chk=ch, **V); b = CB.run(s, T=30000, plan=plan, pats=pats, chk=ch, **V)
        chk(f'(A1) s{s} retina 12, 30 estimulos, fotos: == capBD_on todas las claves', sin_nuevas(a) == b,
            f"splits {a['splits']} celdas {a['celdas']} fotos {len(a['hist'])}")
    # (A2) ancla al TRONCO: perillas v14.2, retina 6 == organismo_v142 (congelado)
    for s in (1, 2, 3):
        a = OF.run(s, T=20000, **V); b = TR.run(s, T=20000)
        ok = all(a[k] == b[k] for k in ('W', 'deaths', 'splits', 'celdas', 'mord', 'vis'))
        chk(f'(A2) s{s} == organismo_v142 en W, muertes, divisiones, celdas, mordidas, visitas', ok, f"W {b['W']}")
    # (B) la fusion es INERTE mientras quede celda libre
    _, pats, _, plan = plan12(1, 12)
    ch = [MN.t_entrada(i) for i in range(1, 12)]
    a0 = OF.run(1, T=12000, plan=plan, pats=pats, chk=ch, ventana=8, fusion=0, **V)
    for f in (1, 2):
        af = OF.run(1, T=12000, plan=plan, pats=pats, chk=ch, ventana=8, fusion=f, **V)
        chk(f'(B) fusion={f} sin agotar el pool == fusion 0 (t_agot {a0["t_agot"]}, celdas {a0["celdas"]})',
            a0['t_agot'] is None and sin_nuevas(af) == sin_nuevas(a0) and af['n_fus'] == 0)
    # (C) con el pool agotado la fusion actua, solo despues de agotarlo, y el pool no pasa de 90
    _, pats, _, plan = plan12(1, 80)
    ch = [MN.t_entrada(i) for i in range(1, 80)]
    rs = {f: OF.run(1, T=80000, plan=plan, pats=pats, chk=ch, ventana=8, fusion=f, **V) for f in (0, 1, 2)}
    chk('(C1) fusion 1 y 2 funden (n_fus > 0)', rs[1]['n_fus'] > 0 and rs[2]['n_fus'] > 0,
        f"fus {rs[1]['n_fus']} azar {rs[2]['n_fus']} base t_agot {rs[0]['t_agot']}")
    chk('(C2) toda fusion ocurre con el pool ya agotado (t >= t_agot)',
        all(rs[f]['t_agot'] is not None and all(t >= rs[f]['t_agot'] for t, _, _ in rs[f]['fus_log']) for f in (1, 2)))
    chk('(C3) celdas <= 90 al final', all(rs[f]['celdas'] <= 90 for f in (0, 1, 2)), str([rs[f]['celdas'] for f in (0, 1, 2)]))
    chk('(C4) la dirigida y la azar eligen pares distintos', rs[1]['fus_log'][:20] != rs[2]['fus_log'][:20])
    chk('(C5) antes de la primera fusion, fus == base (mismo t_agot y mismas divisiones hasta ahi)',
        rs[1]['t_agot'] == rs[0]['t_agot'] and [x for x in rs[1]['split_t'] if x[0] <= rs[1]['t_agot']] ==
        [x for x in rs[0]['split_t'] if x[0] <= rs[0]['t_agot']])
    # (D) determinismo
    b1 = OF.run(1, T=80000, plan=plan, pats=pats, chk=ch, ventana=8, fusion=1, **V)
    chk('(D) determinismo fusion 1', b1 == rs[1])
    # (E) mundo
    okb = True
    for s in range(1, 41):
        o, p, v = MN.mundo(s)
        for i in range(0, MN.N_EST, MN.BLOQUE):
            if [v[o[j]] for j in range(i, i + MN.BLOQUE)].count('comida') != MN.BLOQUE // 2:
                okb = False
    chk('(E1) valencias balanceadas 5/5 en cada bloque de 10 (semillas 1-40)', okb)
    o, p, v = MN.mundo(7)
    chk('(E2) 200 patrones distintos de peso 3 sobre 12 pixeles',
        len({tuple(x) for x in p.values()}) == 200 and all(x.sum() == 3 and len(x) == 12 for x in p.values()))
    orr, prr, vrr = MN.mundo(7, reciclado=True)
    chk('(E3) RECICLADO: 20 primeros == FLUJO; despues solo repeticiones con la misma valencia',
        orr[:20] == o[:20] and all(orr[i] in orr[:20] for i in range(20, 200)) and
        all(vrr[n] == v[n] and np.array_equal(prr[n], p[n]) for n in prr) and len(prr) == 20)
    # (E4 v2; la v1 contaba como 'viejos' a los que estuvieron en la ventana durante el cuarto: mal disenada, declarado)
    # ultimo cuarto = t >= 60000; entonces ya entraron los indices 0..61 y la ventana es 54..61: los j <= 53 son viejos todo el cuarto
    vs = rs[0]['vis']
    orden80 = MN.mundo(1, n_est=80)[0]
    fuera = sum(vs[orden80[j]][3] for j in range(0, 54)); tot = sum(vs[n][3] for n in vs)
    chk('(E4) ventana 8, p_viejo 0.25: fraccion de visitas del ultimo cuarto a estimulos viejos todo el cuarto en [0.10, 0.45]',
        0.10 <= fuera / tot <= 0.45, f'{fuera}/{tot} = {fuera / tot:.3f}')
    # (F) estatico: el rng del mundo/organismo solo gana las dos llamadas nuevas de spawn; _rngf solo en la fusion
    src = open(os.path.join(AQUI, 'organismo_flujo.py'), encoding='utf-8').read()
    ori = open(CN.ORIGEN, encoding='utf-8').read()
    d_rng = src.count('rng.') - ori.count('rng.')   # 'rng.' no cuenta '_rngf.'
    chk('(F1) llamadas nuevas al rng principal: exactamente 3 (spawn: random + integers en dos ramas); _rngf en 2 lineas',
        d_rng == 3 and sum(1 for l in src.splitlines() if '_rngf' in l) == 2, f'd_rng {d_rng}')
    chk('(F2) la fusion no lee val, R_VAL ni el plan (sin canal hacia la respuesta)',
        not any(w in l for l in src.splitlines() if '_fundir' in l or l.startswith('        ') and ('_cand' in l or '_C=' in l)
                for w in ('val[', 'R_VAL', 'plan', 'pats[')))
    # (G) regla 14
    malos, filas = CR.entrada_campo_a_campo()
    chk(f'(G) entrada campo a campo contra organismo_v142: {len(filas)} campos, 0 distintos', not malos, str(malos))
    n_ok = sum(R)
    print(f"TOTAL {n_ok}/{len(R)} en {time.time() - t0:.1f}s")
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
    open(os.path.join(AQUI, 'identidad_n8_salida.txt'), 'w', encoding='utf-8').write(buf.getvalue())
    sys.exit(0 if ok else 1)
