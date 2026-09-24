"""identidad_eco_v11.py — ARNES de ECO v1.1 (corre_eco_v11.py). Se corre ANTES del humo y de cualquier serie. Un proceso, sin Pool.

MISION: llegar a la AGI por este camino.

  (G) el gemelo esta vigente: identidad_eco_rapido_salida.txt dice RESULTADO: 120/120 (se re-corre aparte antes de la serie).
  (A) juez v2 con flujo 7 == corre_eco.juez (el de v1) en el mismo banco y las mismas semillas de bateria.
  (B) el placebo (flujo 8) saca OTRA muestra del MISMO banco (distinta en las semillas de bateria), determinista; con G0 es la misma.
  (C) trabajo v1.1 con T = T_lect == corre_eco.trabajo (v1) en todo lo que v1 escribe (salvo motor/tiempo), con el juez en las semillas
      nuevas; y persiste_lect == persiste.
  (H) la dinamica no depende de T: la corrida larga (T = 2 T_lect) y la corta (T = T_lect) dan lo mismo en persiste_lect, vivos en T_lect,
      gen_t hasta T_lect, corte, banco, sel_corte, juez y placebo (VIDA y AZAR, dos semillas de practica).
  (V) la letra (veredicto y veredicto_L) en entradas sinteticas: cada rama sale donde dice el preregistro.
  (R) el parser aborta ante banderas malas (ERR-115) y un subproceso con bandera desconocida sale con codigo != 0 sin escribir nada.
Escribe identidad_eco_v11_salida.txt.
"""
import contextlib, copy, glob, io, json, os, subprocess, sys, tempfile, time
import numpy as np

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
sys.path.insert(0, AQUI)
R_ = []


def chk(nombre, ok, det=''):
    R_.append(bool(ok)); print(f"  {'OK ' if ok else 'MAL'} {nombre} {det}", flush=True)


def sin(d, fuera):
    return {k: v for k, v in d.items() if k not in fuera}


def J(x):
    return json.dumps(x, sort_keys=True, default=str)


def main():
    import corre_eco_v11 as V
    CR = V.CR
    t0 = time.time()
    print(f"IDENTIDAD ECO v1.1 · {time.strftime('%Y-%m-%d %H:%M:%S')} · python {sys.version.split()[0]} · shas {V.SHAS()}")
    # (G)
    txt = open(os.path.join(AQUI, 'identidad_eco_rapido_salida.txt'), encoding='utf-8').read()
    chk("(G) el gemelo esta vigente (identidad_eco_rapido: 120/120)", 'RESULTADO: 120/120' in txt)
    chk("(G) corre_eco usa el gemelo (CR.ME.run_solapadas es el de motor_eco_rapido)", CR.ME.run_solapadas is CRR_run())
    tmp = tempfile.mkdtemp(prefix='eco_v11_arnes_')
    # un banco real (practica 19603, VIDA, corte en 2000)
    r0 = V.trabajo((19603, 'VIDA', 3000, 2000, 3000, tmp, 2, 2000, False))
    banco = r0['corte']['banco']
    sem = V.JUEZ2['semillas'][:3]
    # (A)
    a = CR.juez(banco, sem, 2000); b = V.juez(banco, sem, 2000, 7)
    chk("(A) juez v2 flujo 7 == corre_eco.juez (v1) en el mismo banco y semillas", J(a) == J(b), f"(vive {[d['vive'] for d in b]})")
    # (B)
    ix = lambda s, f: np.random.default_rng([s, f]).choice(len(banco), size=9, replace=len(banco) < 9)
    dif = [not np.array_equal(ix(s, 7), ix(s, 8)) for s in V.JUEZ2['semillas']]
    igual_cont = sum(np.array_equal(V.fundadores(banco, s, 7), V.fundadores(banco, s, 8)) for s in V.JUEZ2['semillas'])
    chk("(B) el placebo saca otros indices del mismo banco en las 20 semillas de bateria (el contenido puede coincidir si el banco repite genomas)",
        all(dif) and all(np.array_equal(V.fundadores(banco, s, 8), np.asarray(banco, float)[ix(s, 8)]) for s in V.JUEZ2['semillas']),
        f"({sum(dif)}/20 indices distintos; contenido identico en {igual_cont}/20: banco de {len(banco)} con "
        f"{len({tuple(np.round(g, 9)) for g in banco})} genomas distintos)")
    chk("(B) el placebo es determinista", all(np.array_equal(V.fundadores(banco, s, 8), V.fundadores(banco, s, 8)) for s in sem))
    G0 = CR.ME.genoma0(__import__('pista2').cfg_fabrica())
    chk("(B) con G0 las dos muestras son las 9 copias", np.array_equal(V.fundadores(list(G0), 19501, 7), V.fundadores(list(G0), 19501, 8)))
    # (C) v1.1 con T = T_lect == v1 (con el juez en las semillas nuevas)
    orig = CR.JUEZ
    for s, br in ((19604, 'VIDA'), (19604, 'AZAR'), (19605, 'CEREBRO'), (19605, 'MUT0')):
        c1 = tempfile.mkdtemp(prefix='v1_'); c2 = tempfile.mkdtemp(prefix='v11_')
        try:
            CR.JUEZ = dict(orig, semillas=V.JUEZ2['semillas'])
            x = CR.trabajo((s, br, 6000, 4000, c1, 2, 2000, False))
        finally:
            CR.JUEZ = orig
        y = V.trabajo((s, br, 6000, 4000, 6000, c2, 2, 2000, False))
        fuera = {'seg'}
        claves = [k for k in x if k not in fuera]
        cmp = lambda d, k: (sin(d[k], {'fuente'}) if (k == 'juez' and d[k]) else d[k])   # 'fuente' es solo el texto descriptivo
        dist = [k for k in claves if J(cmp(x, k)) != J(cmp(y, k))]
        chk(f"(C) s{s} {br}: v1.1 (T = T_lect) == v1 en las {len(claves)} claves de v1 (juez: bateria y med_banco); persiste_lect == persiste",
            not dist and y['persiste_lect'] == x['persiste'], f"(persiste {x['persiste']}, t_ext {x['t_ext']}, "
            f"juez {[d['vive'] for d in x['juez']['bateria']] if x['juez'] else None}, distintas {dist})")
    # (H) horizonte
    for s in (19603, 19604):
        for br in ('VIDA', 'AZAR'):
            c1 = tempfile.mkdtemp(prefix='h1_'); c2 = tempfile.mkdtemp(prefix='h2_')
            x = V.trabajo((s, br, 6000, 4000, 6000, c1, 2, 2000, False))
            y = V.trabajo((s, br, 12000, 4000, 6000, c2, 2, 2000, False))
            gx = [f for f in x['gen_t'] if f[0] <= 6000]; gy = [f for f in y['gen_t'] if f[0] <= 6000]
            ok = (x['persiste_lect'] == y['persiste_lect'] and J(gx) == J(gy) and J(x['corte']) == J(y['corte']) and
                  J(x['sel_corte']) == J(y['sel_corte']) and J(x['juez']) == J(y['juez']) and J(x['juez_placebo']) == J(y['juez_placebo']) and
                  (x['vivos_lect'] == y['vivos_lect']) and (not x['persiste_lect'] or x['vivos_lect'] == x['vivos_T']))
            chk(f"(H) s{s} {br}: T = 12000 y T = 6000 dan lo mismo hasta T_lect = 6000", ok,
                f"(persiste_lect {x['persiste_lect']}/{y['persiste_lect']}, vivos {x['vivos_lect']}/{y['vivos_lect']}/{x['vivos_T']}, "
                f"persiste en 12000 {y['persiste']}, t_ext {y['t_ext']})")
    # (V) la letra en entradas sinteticas
    genes = list(r0['genes'])

    def fake(pers, jz, plc, sel_alpha=20, azar_falso=0, mut0=0, bloq=0, T=V.V11['T'], persT=None):
        R = []
        for i in range(20):
            s = 19401 + i
            for b in V.BRAZOS:
                p = int(i < {'VIDA': pers[0], 'CEREBRO': pers[1], 'AZAR': pers[2], 'MUT0': mut0}[b])
                pT = p if persT is None else int(i < {'VIDA': persT[0], 'CEREBRO': persT[1], 'AZAR': persT[2], 'MUT0': 0}[b])
                sc = [0] * len(genes)
                if b == 'VIDA' and i < sel_alpha: sc[genes.index('alpha')] = 1
                if b == 'AZAR' and i < azar_falso: sc[genes.index('eta')] = 1
                x = dict(seed=s, brazo=b, persiste_lect=p, persiste=pT, bloqueados=(bloq if i == 0 and b == 'VIDA' else 0), sel_corte=sc,
                         genes=genes, T=T, r0_post=0.95, juez=None, juez_placebo=None)
                if b in V.JUZGADOS:
                    v = jz[b](i)
                    x['juez'] = dict(bateria=[dict(vive=v)] * 3)
                if b in V.PLACEBO:
                    x['juez_placebo'] = dict(bateria=[dict(vive=plc[b](i))] * 3)
                R.append(x)
        return R
    G0b = [dict(vive=2000)] * 3
    base_j = {'VIDA': lambda i: 9000 if i < 16 else 1000, 'CEREBRO': lambda i: 9000, 'AZAR': lambda i: 3000}
    base_p = {'VIDA': lambda i: 9000 - (1 if i % 2 else -1), 'AZAR': lambda i: 3000 - (1 if i % 2 else -1)}   # 10/20 gana el placebo
    casos = [
        ("FUNCIONA", fake((18, 17, 9), base_j, base_p), 'FUNCIONA'),
        ("MODESTO (P1 cae)", fake((12, 17, 9), base_j, base_p), 'HAY ALGO MODESTO'),
        ("NO (P3 cae: VIDA > AZAR 14/20)", fake((18, 17, 9), dict(base_j, VIDA=lambda i: 9000 if i < 14 else 1000), base_p), 'NO (en'),
        ("NO (P3: 6 empates no cuentan como victoria)", fake((18, 17, 9), dict(base_j, VIDA=lambda i: 9000 if i < 14 else 3000), base_p), 'NO (en'),
        ("NO EVALUABLE (placebo 16/20)", fake((18, 17, 9), base_j, dict(base_p, AZAR=lambda i: 3000 - (1 if i < 16 else -1))), 'NO EVALUABLE (el placebo'),
        ("placebo con empates: 10 gana + 10 empata = 15 (borde) -> valido", fake((18, 17, 9), dict(base_j, VIDA=lambda i: 9000),
                                                                                 dict(base_p, VIDA=lambda i: 9000 - (1 if i < 10 else 0))), 'FUNCIONA'),
        ("placebo 4/20 (borde) -> NO EVALUABLE", fake((18, 17, 9), dict(base_j, VIDA=lambda i: 9000),
                                                      dict(base_p, VIDA=lambda i: 9000 + (1 if i < 16 else -1))), 'NO EVALUABLE (el placebo'),
        ("placebo 5/20 (borde) -> valido", fake((18, 17, 9), dict(base_j, VIDA=lambda i: 9000),
                                                dict(base_p, VIDA=lambda i: 9000 + (1 if i < 15 else -1))), 'FUNCIONA'),
        ("NO EVALUABLE (MUT0 10/20)", fake((18, 17, 9), base_j, base_p, mut0=10), 'NO EVALUABLE (MUT0'),
        ("NO EVALUABLE (falsos positivos 9/20)", fake((18, 17, 9), base_j, base_p, azar_falso=9), 'NO EVALUABLE (AZAR'),
        ("NO EVALUABLE (bloqueados)", fake((18, 17, 9), base_j, base_p, bloq=1), 'NO EVALUABLE (tope'),
        ("NO EVALUABLE (incompleta)", fake((18, 17, 9), base_j, base_p)[:-1], 'NO EVALUABLE (serie incompleta'),
        ("NO (P2 cae)", fake((18, 17, 9), base_j, base_p, sel_alpha=14), 'NO (en'),
    ]
    for nombre, R, esperado in casos:
        v, L, d = V.veredicto(R, G0b, 20)
        chk(f"(V) {nombre}", v.startswith(esperado), f"-> {v}")
    casosL = [
        ("L: VIDA 10, AZAR 4 -> PERSISTE LARGO Y LA SELECCION SUMA", fake((18, 17, 9), base_j, base_p, persT=(10, 9, 4)), 'PERSISTE LARGO Y'),
        ("L: VIDA 10, AZAR 5 -> PERSISTE LARGO (sin seleccion)", fake((18, 17, 9), base_j, base_p, persT=(10, 9, 5)), 'PERSISTE LARGO (en'),
        ("L: VIDA 9 -> NO PERSISTE LARGO", fake((18, 17, 9), base_j, base_p, persT=(9, 9, 0)), 'NO PERSISTE'),
        ("L: T distinto de 1e6 -> NO EVALUABLE", fake((18, 17, 9), base_j, base_p, T=120000), 'NO EVALUABLE'),
    ]
    for nombre, R, esperado in casosL:
        v, L, d = V.veredicto_L(R, 20)
        chk(f"(V) {nombre}", v.startswith(esperado), f"-> {v}")
    # (R) parser
    malas = [['--help'], ['-h'], [], ['--serie'], ['--humo', '--serie'], ['--serie', '--desde', '19401', '--n', '20'],
             ['--serie', '--desde=19401', '--n', '20', '--pool', '3'], ['--serie', '--des', '19401', '--n', '20', '--pool', '3'],
             ['--serie', '--desde', '19101', '--n', '20', '--pool', '3'], ['--serie', '--desde', '19401', '--n', '19', '--pool', '3'],
             ['--serie', '--desde', '19401', '--n', '20', '--pool', '4'], ['--humo', '--pool', '2'], ['--humo', '--humo'],
             ['--serie', '--desde', 'x', '--n', '20', '--pool', '3'], ['--prueba_pool', '--desde', '19601', '--n', '2', '--pool', '2'],
             ['--prueba_pool', '--desde', '19602', '--n', '2', '--pool', '3'], ['--lee', 'x', '--pool', '3'], ['--largo']]
    n_ab = 0
    for m in malas:
        try: V.parsea(m)
        except V.BanderaMala: n_ab += 1
    chk(f"(R) el parser aborta ante {len(malas)} formas de bandera mala", n_ab == len(malas), f"({n_ab}/{len(malas)})")
    buenas = [['--humo'], ['--serie', '--desde', '19401', '--n', '20', '--pool', '3'], ['--serie', '--desde', '19421', '--n', '20', '--pool', '3', '--reanuda'],
              ['--prueba_pool', '--desde', '19602', '--n', '2', '--pool', '2'], ['--lee', 'datos/x']]
    n_ok = 0
    for m in buenas:
        try: V.parsea(m); n_ok += 1
        except V.BanderaMala: pass
    chk(f"(R) el parser acepta las {len(buenas)} formas buenas", n_ok == len(buenas), f"({n_ok}/{len(buenas)})")
    antes = set(glob.glob(os.path.join(AQUI, 'datos', '**', '*'), recursive=True))
    pr = subprocess.run([sys.executable, os.path.join(AQUI, 'corre_eco_v11.py'), '--serie', '--desde', '19401', '--n', '20', '--pool', '3', '--nada'],
                        capture_output=True, text=True, timeout=300)
    despues = set(glob.glob(os.path.join(AQUI, 'datos', '**', '*'), recursive=True))
    chk("(R) subproceso con bandera desconocida: codigo != 0 y no escribe nada", pr.returncode != 0 and antes == despues, f"(codigo {pr.returncode})")
    n = sum(R_)
    print(f"RESULTADO: {n}/{len(R_)}  ({time.time() - t0:.0f} s)")
    return n == len(R_)


def CRR_run():
    import motor_eco_rapido as MR
    return MR.run_solapadas


if __name__ == '__main__':
    buf = io.StringIO()

    class Tee:
        def write(self, x): sys.__stdout__.write(x); buf.write(x)
        def flush(self): sys.__stdout__.flush()
        def reconfigure(self, **kw): pass   # corre_eco llama a sys.stdout.reconfigure al importarse
    with contextlib.redirect_stdout(Tee()):
        ok = main()
    open(os.path.join(AQUI, 'identidad_eco_v11_salida.txt'), 'w', encoding='utf-8').write(buf.getvalue())
    sys.exit(0 if ok else 1)
