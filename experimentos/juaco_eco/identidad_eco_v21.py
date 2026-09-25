"""identidad_eco_v21.py — ARNES del runner de ECO v2.1 (corre_eco_v21.py). Un proceso, sin Pool. Nube, 24-sep-2026.

MISION: llegar a la AGI por este camino.

  (M) los tres mundos y los brazos son los del preregistro; el genoma de las corridas es el de motor_eco2 (20 genes).
  (T) trabajo con el motor Python en los tres mundos (T corto) escribe las medidas: fraccion del banco con cada organo = la que se
      calcula a mano desde el banco; vivos_on desde vivos_final; sel_corte de 20 genes.
  (G) si existe el gemelo motor_eco_rapido_org: trabajo con el gemelo == con Python (salvo motor y tiempo) en los tres mundos y los dos
      brazos (T corto); si no existe, PENDIENTE y el arnes no da N/N.
  (V) la letra en entradas sinteticas.
  (R) banderas malas abortan (ERR-115); un subproceso con bandera desconocida sale con codigo != 0 sin escribir nada.
Escribe identidad_eco_v2_salida.txt.
"""
import contextlib, glob, io, json, os, subprocess, sys, tempfile, time
import numpy as np

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
R_ = []


def chk(nombre, ok, det=''):
    R_.append(bool(ok)); print(f"  {'OK ' if ok else 'MAL'} {nombre} {det}", flush=True)


J = lambda x: json.dumps(x, sort_keys=True, default=str)


def main():
    import corre_eco_v21 as V
    t0 = time.time()
    print(f"IDENTIDAD ECO v2.1 (runner) · {time.strftime('%Y-%m-%d %H:%M:%S')} · python {sys.version.split()[0]} · shas {V.SHAS()}")
    chk("(M) mundos y brazos del preregistro", V.MUNDOS == {'w30': dict(esc=30, n0=30, tope=3000), 'w90': dict(esc=90, n0=90, tope=3000),
                                                          'w270': dict(esc=270, n0=270, tope=9000)} and V.BRAZOS == ('VIDA', 'AZAR')
        and V.V2 == dict(T=120000, t_corte=60000) and V.VENTANAS == {'serie': 20211, 'replica': 20231})
    V.MOTOR[0] = V.ME2
    res = {}
    for m, T_, tc in (('w30', 3000, 2000), ('w90', 2500, 1500), ('w270', 1200, 800)):
        x = V.trabajo((20093, m, 'VIDA', T_, tc, tempfile.mkdtemp(), False)); res[m] = x
        B = np.asarray(x['corte']['banco'], float)
        man = {g: round(float(np.mean(B[:, V.IORG[g]] >= 1.0)), 4) for g in V.ORGANOS}
        vv = [v[4:] for v in x['vivos_final']]
        manv = {g: (round(float(np.mean([float(a[V.IORG[g]]) >= 1.0 for a in vv])), 4) if vv else None) for g in V.ORGANOS}
        chk(f"(T) {m}: banco_on y vivos_on == a mano; 20 genes; sel_corte de 20", x['banco_on'] == man and x['vivos_on'] == manv and
            len(x['genes']) == 20 and (x['sel_corte'] is None or len(x['sel_corte']) == 20), f"(banco_on {x['banco_on']}, nacidos {x['n_nac']}, {x['seg']} s)")
    # (S) v2.1: la expresion contra sombras sale del checkpoint del corte (cortes en multiplos de 10 000) y el real == banco_on del motor
    x = V.trabajo((20294, 'w30', 'VIDA', 12000, 10000, tempfile.mkdtemp(), False)); so = x.get('banco_on_sombras') or {}
    chk("(S) expresion en el corte: real (checkpoint) == banco_on (motor) en ensena y filtra0, con 8 sombras cada uno",
        bool(so) and all(so[g]['real'] == x['banco_on'][g] and len(so[g]['sombras']) == 8 for g in V.ORGANOS),
        f"({ {g: (so[g]['real'], round(float(np.mean(so[g]['sombras'])), 3)) for g in V.ORGANOS} if so else None})")
    if os.path.exists(os.path.join(AQUI, 'motor_eco_rapido_org.py')):
        for m, T_, tc in (('w30', 12000, 10000), ('w90', 11000, 10000), ('w270', 10500, 10000)):
            for b in V.BRAZOS:
                V.MOTOR[0] = V.ME2
                p = V.trabajo((20094, m, b, T_, tc, tempfile.mkdtemp(), False))
                V.usa_gemelo()
                g = V.trabajo((20094, m, b, T_, tc, tempfile.mkdtemp(), False))
                V.MOTOR[0] = V.ME2
                dist = [k for k in p if k not in ('seg', 'motor') and J(p[k]) != J(g.get(k))]
                chk(f"(G) {m} {b}: gemelo == Python en trabajo, con la expresion del corte (T {T_}, corte {tc})", not dist and p.get('banco_on_sombras'),
                    f"(distintas {dist}; {p['seg']} s contra {g['seg']} s)")
    else:
        chk("(G) el gemelo motor_eco_rapido_org.py existe (PENDIENTE: lo construye el compilador)", False)
    # (V)
    genes = list(V.ME2.NOMBRES); ie, jf = genes.index('ensena'), genes.index('filtra0')

    def fake(o1, o2, falso=None, bloq=0, incompleta=False, f0=0):
        R = []
        for m in V.MUNDOS:
            for i in range(20):
                for b in V.BRAZOS:
                    sc = [0] * len(genes)
                    if b == 'VIDA' and i < o1.get(m, 0): sc[ie] = 1
                    if b == 'VIDA' and i < f0: sc[jf] = 1
                    if b == 'AZAR' and falso == m and i < 9: sc[genes.index('eta')] = 1
                    on = (0.5 if (b == 'VIDA' and i < o2.get(m, 0)) else 0.1)
                    so = {'ensena': dict(real=(0.9 if (b == 'VIDA' and i < o1.get(m, 0)) else 0.2), sombras=[0.2] * 8),
                          'filtra0': dict(real=(0.9 if (b == 'VIDA' and i < f0) else 0.2), sombras=[0.2] * 8)}
                    if b == 'AZAR' and falso == m and i < 15: so['ensena'] = dict(real=0.9, sombras=[0.2] * 8)
                    R.append(dict(seed=20211 + i, mundo=m, brazo=b, sel_corte=sc, banco_on={'ensena': on, 'filtra0': 0.1}, banco_on_sombras=so,
                                  vivos_on={'ensena': on, 'filtra0': None}, persiste=1, bloqueados=(bloq if (i == 0 and b == 'VIDA' and m == 'w90') else 0),
                                  corte=dict(banco=[]), genes=genes))
        return R[:-1] if incompleta else R
    todos = {'w30': 16, 'w90': 16, 'w270': 16}
    casos = [("FUNCIONA (3 de 3)", fake(todos, todos), 'FUNCIONA'),
             ("FUNCIONA (2 de 3)", fake({'w90': 16, 'w270': 16}, {'w90': 16, 'w270': 16}), 'FUNCIONA'),
             ("MODESTO (O1 y O2 en 1 mundo)", fake({'w90': 16}, {'w90': 16}), 'HAY ALGO MODESTO'),
             ("MODESTO (O1 en 2 mundos, O2 en ninguno)", fake({'w90': 16, 'w270': 16}, {}), 'HAY ALGO MODESTO'),
             ("NO (O1 14 en todos)", fake({'w30': 14, 'w90': 14, 'w270': 14}, {'w90': 16}), 'NO (en'),
             ("NO EVALUABLE (falsos positivos en w30: media 9/20 y expresion 15/20 en AZAR)", fake(todos, todos, falso='w30'), 'NO EVALUABLE (AZAR'),
             ("NO EVALUABLE (bloqueados)", fake(todos, todos, bloq=3), 'NO EVALUABLE (tope'),
             ("NO EVALUABLE (incompleta)", fake(todos, todos, incompleta=True), 'NO EVALUABLE (serie')]
    for nombre, R, esp in casos:
        v, L, d = V.veredicto(R, 20)
        chk(f"(V) {nombre}", v.startswith(esp), f"-> {v}")
    # (R)
    malas = [['--help'], ['-h'], [], ['--serie'], ['--serie', '--ventana', 'serie'], ['--serie', '--ventana', 'otra', '--pool', '3'],
             ['--serie', '--ventana', 'serie', '--pool', '4'], ['--serie', '--ventana=serie', '--pool', '3'], ['--serie', '--ventana', 'serie', '--pool', '3', '--gemelo'],
             ['--humo', '--pool', '2'], ['--humo', '--humo'], ['--prueba_pool', '--pool', '3'], ['--lee', 'x', '--gemelo'], ['--serie', '--vent', 'serie', '--pool', '3']]
    n_ab = 0
    for mm in malas:
        try: V.parsea(mm)
        except V.BanderaMala: n_ab += 1
    chk(f"(R) el parser aborta ante {len(malas)} formas malas", n_ab == len(malas), f"({n_ab}/{len(malas)})")
    buenas = [['--humo'], ['--humo', '--gemelo'], ['--prueba_pool', '--pool', '2'], ['--serie', '--ventana', 'serie', '--pool', '3'],
              ['--serie', '--ventana', 'replica', '--pool', '3', '--reanuda'], ['--lee', 'datos/x']]
    n_ok = 0
    for mm in buenas:
        try: V.parsea(mm); n_ok += 1
        except V.BanderaMala: pass
    chk(f"(R) el parser acepta las {len(buenas)} formas buenas", n_ok == len(buenas), f"({n_ok}/{len(buenas)})")
    antes = set(glob.glob(os.path.join(AQUI, 'datos', '**', '*'), recursive=True))
    pr = subprocess.run([sys.executable, os.path.join(AQUI, 'corre_eco_v21.py'), '--serie', '--ventana', 'serie', '--pool', '3', '--nada'],
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
    open(os.path.join(AQUI, 'identidad_eco_v21_salida.txt'), 'w', encoding='utf-8').write(buf.getvalue())
    sys.exit(0 if ok else 1)
