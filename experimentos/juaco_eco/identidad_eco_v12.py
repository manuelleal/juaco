"""identidad_eco_v12.py — ARNES de ECO v1.2 (corre_eco_v12.py). Un proceso, sin Pool. Nube, 24-sep-2026.

MISION: llegar a la AGI por este camino.

  (J) juez v1.2 con el carro FABRICA_ECO, flujo 7 y el mismo T_b == corre_eco_v11.juez (motor Python) en el mismo banco y semillas
      (de PRACTICA: la bateria sellada no se toca en el arnes).
  (C) trabajo v1.2 del brazo VIDA (FABRICA_ECO) == trabajo v1.1 de VIDA en todas las claves de v1.1 salvo juez/placebo (otra bateria),
      motor y tiempo (motor Python, T corto).
  (F) el brazo VIDA_T usa FAMB_RES0_ECO y su fisica difiere de VIDA (la familia actua) y la genetica de cada brazo es la de corre_eco.
  (G) si existe el gemelo motor_eco_rapido_fam: trabajo v1.2 de VIDA_T, AZAR_T, MUT0_T y VIDA con el gemelo == con Python (salvo motor y
      tiempo), T corto; si no existe todavia, el caso se marca PENDIENTE y el arnes NO da N/N.
  (V) la letra en entradas sinteticas.
  (R) banderas malas abortan (ERR-115); un subproceso con bandera desconocida sale con codigo != 0 sin escribir nada.
Escribe identidad_eco_v12_salida.txt.
"""
import contextlib, glob, io, json, os, subprocess, sys, tempfile, time
import numpy as np

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
sys.path.insert(0, AQUI)
R_ = []


def chk(nombre, ok, det=''):
    R_.append(bool(ok)); print(f"  {'OK ' if ok else 'MAL'} {nombre} {det}", flush=True)


J = lambda x: json.dumps(x, sort_keys=True, default=str)


def main():
    import corre_eco_v12 as V
    import corre_eco_v11 as V11
    CR = V.CR
    t0 = time.time()
    print(f"IDENTIDAD ECO v1.2 · {time.strftime('%Y-%m-%d %H:%M:%S')} · python {sys.version.split()[0]} · shas {V.SHAS()}")
    CR.ME = V.ME_PY
    tmp = tempfile.mkdtemp(prefix='eco_v12_arnes_')
    r0 = V.trabajo((19906, 'VIDA', 3000, 2000, 3000, tmp, 1, 1000, False))
    banco = r0['corte']['banco']
    # (J)
    PR = (19903, 19904)   # semillas de PRACTICA para el juez del arnes: la bateria 19801-19820 queda sellada (aviso del compilador, 24-sep)
    a = V11.juez(banco, PR, 2000, 7)
    b = V.juez(banco, PR, 2000, 7, V.FAB)
    chk("(J) juez v1.2 (FABRICA_ECO, flujo 7) == juez v1.1, motor Python", J(a) == J(b), f"(vive {[d['vive'] for d in b]})")
    # (C) VIDA v1.2 == VIDA v1.1 (motor Python) salvo juez/placebo
    x = V11.trabajo((19907, 'VIDA', 6000, 4000, 5000, tempfile.mkdtemp(), 1, 1000, False))
    y = V.trabajo((19907, 'VIDA', 6000, 4000, 5000, tempfile.mkdtemp(), 1, 1000, False))
    fuera = {'seg', 'juez', 'juez_placebo', 'motor'}
    dist = [k for k in x if k not in fuera and J(x[k]) != J(y.get(k))]
    chk("(C) trabajo v1.2 de VIDA == trabajo v1.1 de VIDA (motor Python) en todas las claves de v1.1 salvo juez, motor y tiempo",
        not dist, f"(persiste {x['persiste']}, t_ext {x['t_ext']}, distintas {dist})")
    # (F)
    z = V.trabajo((19907, 'VIDA_T', 6000, 4000, 5000, tempfile.mkdtemp(), 1, 1000, False))
    chk("(F) VIDA_T usa FAMB_RES0_ECO con la genetica VIDA y su fisica difiere de la de VIDA",
        z['carro'] == 'FAMB_RES0_ECO' and z['genetica'] == 'VIDA' and J(z['gen_t']) != J(y['gen_t']),
        f"(nacidos VIDA {y['n_nac']} · VIDA_T {z['n_nac']})")
    chk("(F) la genetica y el carro de cada brazo", V.BRAZOS == {'VIDA_T': ('VIDA', 'FAMB_RES0_ECO'), 'AZAR_T': ('AZAR', 'FAMB_RES0_ECO'),
                                                              'MUT0_T': ('MUT0', 'FAMB_RES0_ECO'), 'VIDA': ('VIDA', 'FABRICA_ECO')})
    # (G) gemelo
    if os.path.exists(os.path.join(AQUI, 'motor_eco_rapido_fam.py')):
        J3 = V.JUEZ3; V.JUEZ3 = dict(J3, semillas=(19903, 19904))   # (G) tambien con semillas de practica en el juez
        for br in ('VIDA_T', 'AZAR_T', 'MUT0_T', 'VIDA'):
            CR.ME = V.ME_PY
            p = V.trabajo((19908, br, 8000, 4000, 6000, tempfile.mkdtemp(), 2, 2000, False))
            V.usa_gemelo()
            g = V.trabajo((19908, br, 8000, 4000, 6000, tempfile.mkdtemp(), 2, 2000, False))
            CR.ME = V.ME_PY
            dist = [k for k in p if k not in ('seg', 'motor') and J(p[k]) != J(g.get(k))]
            chk(f"(G) {br}: el gemelo == Python en trabajo v1.2 (T 8000, corte 4000, juez 2 semillas de practica T_b 2000)", not dist,
                f"(persiste {p['persiste']}, nacidos {p['n_nac']}, distintas {dist}; {p['seg']} s contra {g['seg']} s)")
        V.JUEZ3 = J3
    else:
        chk("(G) el gemelo motor_eco_rapido_fam.py existe (PENDIENTE: lo construye el compilador)", False)
    # (V) la letra
    genes = list(r0['genes'])

    def fake(p1, pv, jz, plc, sel=20, falso=0, bloq=0, T=V.V12['T']):
        R = []
        for i in range(20):
            for b in V.BRAZOS:
                pr = int(i < {'VIDA_T': p1, 'AZAR_T': 5, 'MUT0_T': 3, 'VIDA': pv}[b])
                sc = [0] * len(genes)
                if b == 'VIDA_T' and i < sel: sc[genes.index('alpha')] = 1
                if b == 'AZAR_T' and i < falso: sc[genes.index('eta')] = 1
                xx = dict(seed=19701 + i, brazo=b, persiste=pr, persiste_lect=pr, bloqueados=(bloq if (i == 0 and b == 'VIDA') else 0),
                          sel_corte=sc, genes=genes, T=T, r0_post=0.99, vivos_T=10 * pr, max_vivos=100, juez=None, juez_placebo=None)
                if b in V.JUZGADOS:
                    xx['juez'] = dict(bateria=[dict(vive=jz[b](i))] * 3)
                    xx['juez_placebo'] = dict(bateria=[dict(vive=plc[b](i))] * 3)
                R.append(xx)
        return R
    G0b = [dict(vive=2000)] * 3
    jz = {'VIDA_T': lambda i: 90000 if i < 16 else 1000, 'AZAR_T': lambda i: 30000}
    pl = {'VIDA_T': lambda i: 90000 - (1 if i % 2 else -1), 'AZAR_T': lambda i: 30000 - (1 if i % 2 else -1)}
    casos = [
        ("FUNCIONA", fake(16, 6, jz, pl), 'FUNCIONA'),
        ("MODESTO persiste con familia (F3 cae)", fake(16, 6, dict(jz, VIDA_T=lambda i: 90000 if i < 14 else 1000), pl), 'HAY ALGO MODESTO: PERSISTE'),
        ("MODESTO seleccion con familia (F1 cae)", fake(14, 6, jz, pl), 'HAY ALGO MODESTO: SELECCION'),
        ("MODESTO seleccion con familia (F2 cae: 16 - 11 = 5)", fake(16, 11, jz, pl), 'HAY ALGO MODESTO: SELECCION'),
        ("NO (F1 y F3 caen)", fake(14, 6, dict(jz, VIDA_T=lambda i: 90000 if i < 14 else 1000), pl), 'NO (en'),
        ("NO (empates en el techo no ganan)", fake(14, 6, dict(jz, VIDA_T=lambda i: 100000, AZAR_T=lambda i: 100000),
                                                   dict(pl, VIDA_T=lambda i: 100000 - (1 if i % 2 else -1), AZAR_T=lambda i: 100000 - (1 if i % 2 else -1))), 'NO (en'),
        ("NO EVALUABLE (placebo 16/20)", fake(16, 6, jz, dict(pl, AZAR_T=lambda i: 30000 - (1 if i < 16 else -1))), 'NO EVALUABLE (el placebo'),
        ("NO EVALUABLE (falsos positivos)", fake(16, 6, jz, pl, falso=9), 'NO EVALUABLE (AZAR_T'),
        ("NO EVALUABLE (bloqueados)", fake(16, 6, jz, pl, bloq=2), 'NO EVALUABLE (tope'),
        ("NO EVALUABLE (T distinto)", fake(16, 6, jz, pl, T=120000), 'NO EVALUABLE (serie'),
        ("NO EVALUABLE (incompleta)", fake(16, 6, jz, pl)[:-1], 'NO EVALUABLE (serie'),
    ]
    for nombre, R, esperado in casos:
        v, L, d = V.veredicto(R, G0b, 20)
        chk(f"(V) {nombre}", v.startswith(esperado), f"-> {v}")
    # (R)
    malas = [['--help'], ['-h'], [], ['--serie'], ['--humo', '--serie'], ['--serie', '--desde', '19701', '--n', '20'],
             ['--serie', '--desde=19701', '--n', '20', '--pool', '3'], ['--serie', '--des', '19701', '--n', '20', '--pool', '3'],
             ['--serie', '--desde', '19401', '--n', '20', '--pool', '3'], ['--serie', '--desde', '19701', '--n', '19', '--pool', '3'],
             ['--serie', '--desde', '19701', '--n', '20', '--pool', '4'], ['--serie', '--desde', '19701', '--n', '20', '--pool', '3', '--gemelo'],
             ['--humo', '--pool', '2'], ['--humo', '--humo'], ['--prueba_pool', '--desde', '19901', '--n', '2', '--pool', '2'],
             ['--lee', 'x', '--gemelo'], ['--largo']]
    n_ab = 0
    for m in malas:
        try: V.parsea(m)
        except V.BanderaMala: n_ab += 1
    chk(f"(R) el parser aborta ante {len(malas)} formas de bandera mala", n_ab == len(malas), f"({n_ab}/{len(malas)})")
    buenas = [['--humo'], ['--humo', '--gemelo'], ['--serie', '--desde', '19701', '--n', '20', '--pool', '3'],
              ['--serie', '--desde', '19721', '--n', '20', '--pool', '3', '--reanuda'], ['--prueba_pool', '--desde', '19902', '--n', '2', '--pool', '2'],
              ['--lee', 'datos/x']]
    n_ok = 0
    for m in buenas:
        try: V.parsea(m); n_ok += 1
        except V.BanderaMala: pass
    chk(f"(R) el parser acepta las {len(buenas)} formas buenas", n_ok == len(buenas), f"({n_ok}/{len(buenas)})")
    antes = set(glob.glob(os.path.join(AQUI, 'datos', '**', '*'), recursive=True))
    pr = subprocess.run([sys.executable, os.path.join(AQUI, 'corre_eco_v12.py'), '--serie', '--desde', '19701', '--n', '20', '--pool', '3', '--nada'],
                        capture_output=True, text=True, timeout=300)
    despues = set(glob.glob(os.path.join(AQUI, 'datos', '**', '*'), recursive=True))
    chk("(R) subproceso con bandera desconocida: codigo != 0 y no escribe nada", pr.returncode != 0 and antes == despues, f"(codigo {pr.returncode})")
    n = sum(R_)
    print(f"RESULTADO: {n}/{len(R_)}  ({time.time() - t0:.0f} s)")
    return n == len(R_)


if __name__ == '__main__':
    buf = io.StringIO()

    class Tee:
        def write(self, x): sys.__stdout__.write(x); buf.write(x)
        def flush(self): sys.__stdout__.flush()
        def reconfigure(self, **kw): pass
    with contextlib.redirect_stdout(Tee()):
        ok = main()
    open(os.path.join(AQUI, 'identidad_eco_v12_salida.txt'), 'w', encoding='utf-8').write(buf.getvalue())
    sys.exit(0 if ok else 1)
