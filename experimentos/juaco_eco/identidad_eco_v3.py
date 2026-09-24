"""identidad_eco_v3.py — ARNES del runner de ECO v3 (corre_eco_v3.py). Un proceso, sin Pool. Nube, 24-sep-2026.

MISION: llegar a la AGI por este camino.

  (M) los dos mundos, los brazos, las ventanas y los 7 organos son los del preregistro; el genoma es el de motor_eco3 (25 genes).
  (T) trabajo (motor Python) en los dos mundos con T corto: la fraccion del banco con cada organo == la calculada a mano; vivos_on desde
      vivos_final; sel_corte de 25 genes.
  (V) la letra por organo en entradas sinteticas (ELEGIDO, DESCARTADO, sube, neutro; FUNCIONA / MODESTO / NO / NO EVALUABLE).
  (R) banderas malas abortan (ERR-115); un subproceso con bandera desconocida sale con codigo != 0 sin escribir nada.
Escribe identidad_eco_v3_salida.txt.
"""
import contextlib, glob, io, json, os, subprocess, sys, tempfile, time
import numpy as np

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
R_ = []


def chk(nombre, ok, det=''):
    R_.append(bool(ok)); print(f"  {'OK ' if ok else 'MAL'} {nombre} {det}", flush=True)


def main():
    import corre_eco_v3 as V
    t0 = time.time()
    print(f"IDENTIDAD ECO v3 (runner) · {time.strftime('%Y-%m-%d %H:%M:%S')} · python {sys.version.split()[0]} · shas {V.SHAS()}")
    chk("(M) mundos, brazos, ventanas y organos del preregistro",
        V.MUNDOS == {'w9': dict(esc=9, n0=9, tope=3000), 'w30': dict(esc=30, n0=30, tope=3000)} and V.BRAZOS == ('VIDA', 'AZAR') and
        V.V2 == dict(T=120000, t_corte=60000) and V.VENTANAS == {'serie': 20111, 'replica': 20131} and
        V.ORGANOS == ('b5', 'mapa', 'curiosidad', 'modelo', 'lenta', 'herencia', 'interruptor') and len(V.ME2.NOMBRES) == 25 and V.CARRO == 'FRANK_ECO')
    for m, T_, tc in (('w9', 4000, 2500), ('w30', 3000, 2000)):
        x = V.trabajo((20198, m, 'VIDA', T_, tc, tempfile.mkdtemp(), False))
        B = np.asarray(x['corte']['banco'], float)
        man = {g: round(float(np.mean(B[:, V.IORG[g]] >= 1.0)), 4) for g in V.ORGANOS}
        vv = [v[4:] for v in x['vivos_final']]
        manv = {g: (round(float(np.mean([float(a[V.IORG[g]]) >= 1.0 for a in vv])), 4) if vv else None) for g in V.ORGANOS}
        chk(f"(T) {m}: banco_on y vivos_on == a mano; 25 genes; sel_corte de 25", x['banco_on'] == man and x['vivos_on'] == manv and
            len(x['genes']) == 25 and (x['sel_corte'] is None or len(x['sel_corte']) == 25), f"(nacidos {x['n_nac']}, {x['seg']} s)")
    genes = list(V.ME2.NOMBRES)

    def fake(sube, baja=None, azar_falso=None, bloq=0, incompleta=False, o2=True):
        baja = baja or {}
        R = []
        for m in V.MUNDOS:
            for i in range(20):
                for b in V.BRAZOS:
                    sc = [0] * len(genes); on = {g: 0.1 for g in V.ORGANOS}
                    for g in sube.get(m, []):
                        if b == 'VIDA' and i < 16: sc[genes.index(g)] = 1
                        if b == 'VIDA' and o2: on[g] = 0.6
                    for g in baja.get(m, []):
                        if b == 'VIDA' and i < 16: sc[genes.index(g)] = -1
                        if b == 'VIDA' and o2: on[g] = 0.0
                    if b == 'AZAR' and azar_falso == m and i < 9: sc[genes.index('eta')] = 1
                    R.append(dict(seed=20111 + i, mundo=m, brazo=b, sel_corte=sc, banco_on=on, vivos_on=on, persiste=1,
                                  bloqueados=(bloq if (i == 0 and b == 'VIDA') else 0)))
        return R[:-1] if incompleta else R
    casos = [
        ("FUNCIONA: herencia ELEGIDO en los 2 mundos", fake({'w9': ['herencia'], 'w30': ['herencia']}), 'FUNCIONA'),
        ("MODESTO: herencia ELEGIDO solo en w30", fake({'w30': ['herencia']}), 'HAY ALGO MODESTO'),
        ("MODESTO: sube en los 2 mundos sin O2", fake({'w9': ['interruptor'], 'w30': ['interruptor']}, o2=False), 'HAY ALGO MODESTO'),
        ("NO: solo DESCARTADOS", fake({}, baja={'w9': ['mapa'], 'w30': ['mapa']}), 'NO (en'),
        ("NO EVALUABLE: falsos positivos en w9", fake({'w9': ['herencia'], 'w30': ['herencia']}, azar_falso='w9'), 'NO EVALUABLE (AZAR'),
        ("NO EVALUABLE: bloqueados", fake({'w9': ['herencia'], 'w30': ['herencia']}, bloq=2), 'NO EVALUABLE (tope'),
        ("NO EVALUABLE: incompleta", fake({'w9': ['herencia'], 'w30': ['herencia']}, incompleta=True), 'NO EVALUABLE (serie'),
    ]
    for nombre, R, esp in casos:
        v, L, d = V.veredicto(R, 20)
        chk(f"(V) {nombre}", v.startswith(esp), f"-> {v}")
    v, L, d = V.veredicto(fake({'w9': ['herencia']}, baja={'w9': ['mapa'], 'w30': ['mapa']}), 20)
    chk("(V) el perfil marca ELEGIDO y DESCARTADO donde toca", d['perfil']['w9']['herencia'] == 'ELEGIDO' and d['perfil']['w9']['mapa'] == 'DESCARTADO'
        and d['perfil']['w30']['mapa'] == 'DESCARTADO' and d['perfil']['w30']['herencia'] == 'neutro', f"({d['perfil']['w9']})")
    malas = [['--help'], ['-h'], [], ['--serie'], ['--serie', '--ventana', 'serie'], ['--serie', '--ventana', 'otra', '--pool', '3'],
             ['--serie', '--ventana', 'serie', '--pool', '4'], ['--serie', '--ventana=serie', '--pool', '3'], ['--humo', '--gemelo'],
             ['--humo', '--pool', '2'], ['--humo', '--humo'], ['--prueba_pool', '--pool', '3'], ['--lee', 'x', '--pool', '2']]
    n_ab = 0
    for mm in malas:
        try: V.parsea(mm)
        except V.BanderaMala: n_ab += 1
    chk(f"(R) el parser aborta ante {len(malas)} formas malas", n_ab == len(malas), f"({n_ab}/{len(malas)})")
    antes = set(glob.glob(os.path.join(AQUI, 'datos', '**', '*'), recursive=True))
    pr = subprocess.run([sys.executable, os.path.join(AQUI, 'corre_eco_v3.py'), '--serie', '--ventana', 'serie', '--pool', '3', '--nada'],
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
    open(os.path.join(AQUI, 'identidad_eco_v3_salida.txt'), 'w', encoding='utf-8').write(buf.getvalue())
    sys.exit(0 if ok else 1)
