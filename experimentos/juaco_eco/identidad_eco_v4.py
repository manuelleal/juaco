"""identidad_eco_v4.py — ARNES del runner de ECO v4 (corre_eco_v4.py). Un proceso, sin Pool. Nube, 24-sep-2026.

MISION: llegar a la AGI por este camino.

Es identidad_eco_v3.py (375bf7644a557118) adaptado al paquete:
  (M) el mundo, los brazos, las ventanas, los 7 organos, el PAQUETE (herencia, interruptor), los 5 FIJOS y los 20 genes que mutan.
  (T) trabajo (motor Python) en w30 y w9 con T corto, VIDA y AZAR: banco_on y vivos_on == a mano; 25 genes; sel_corte de 25; el motor
      informa como mutables EXACTAMENTE los 20 del runner; los 5 FIJOS no se expresan en nadie.
  (K) en AZAR, w30 (T 12 000, corte 10 000) la mutacion SI alcanza a los organos del paquete (real o sombras) y NO a los fijos (real y las
      8 sombras de cada entrada del banco en 0.0 exacto).
  (S) la expresion del corte sale del checkpoint y el real coincide con el banco del motor en los 7 organos, con 8 sombras cada uno.
  (V) la letra del paquete en entradas sinteticas (FUNCIONA / MODESTO / NO / NO EVALUABLE, incluido un organo fijo expresado).
  (R) banderas malas abortan (ERR-115); un subproceso con bandera desconocida sale con codigo != 0 sin escribir nada.
Escribe identidad_eco_v4_salida.txt.
"""
import contextlib, glob, io, json, os, subprocess, sys, tempfile, time
import numpy as np

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
R_ = []


def chk(nombre, ok, det=''):
    R_.append(bool(ok)); print(f"  {'OK ' if ok else 'MAL'} {nombre} {det}", flush=True)


def main():
    import corre_eco_v4 as V
    t0 = time.time()
    print(f"IDENTIDAD ECO v4 (runner) · {time.strftime('%Y-%m-%d %H:%M:%S')} · python {sys.version.split()[0]} · shas {V.SHAS()}")
    chk("(M) mundo, brazos, ventanas, organos, paquete, fijos y mutables del preregistro",
        V.MUNDOS == {'w30': dict(esc=30, n0=30, tope=3000), 'w9': dict(esc=9, n0=9, tope=3000)} and V.BRAZOS == ('VIDA', 'AZAR') and
        V.V2 == dict(T=120000, t_corte=60000) and V.VENTANAS == {'serie': 20311, 'replica': 20331} and
        V.ORGANOS == ('b5', 'mapa', 'curiosidad', 'modelo', 'lenta', 'herencia', 'interruptor') and V.PAQUETE == ('herencia', 'interruptor')
        and V.FIJOS == ('b5', 'mapa', 'curiosidad', 'modelo', 'lenta') and len(V.MUTABLES) == 20 and not set(V.FIJOS) & set(V.MUTABLES)
        and len(V.ME2.NOMBRES) == 25 and V.CARRO == 'FRANK_ECO')
    for m, b, T_, tc in (('w30', 'VIDA', 3000, 2000), ('w30', 'AZAR', 3000, 2000), ('w9', 'VIDA', 4000, 2500), ('w9', 'AZAR', 4000, 2500)):
        x = V.trabajo((20398, m, b, T_, tc, tempfile.mkdtemp(), False))
        B = np.asarray(x['corte']['banco'], float)
        man = {g: round(float(np.mean(B[:, V.IORG[g]] >= 1.0)), 4) for g in V.ORGANOS}
        vv = [v[4:] for v in x['vivos_final']]
        manv = {g: (round(float(np.mean([float(a[V.IORG[g]]) >= 1.0 for a in vv])), 4) if vv else None) for g in V.ORGANOS}
        fijos0 = all((x['banco_on'][g] or 0) == 0 and (x['vivos_on'][g] or 0) == 0 for g in V.FIJOS)
        chk(f"(T) {m} {b}: banco_on y vivos_on == a mano; 25 genes; sel_corte de 25; mutables == los 20; fijos apagados",
            x['banco_on'] == man and x['vivos_on'] == manv and len(x['genes']) == 25 and (x['sel_corte'] is None or len(x['sel_corte']) == 25)
            and list(x['mutables'] or []) == list(V.MUTABLES) and fijos0, f"(nacidos {x['n_nac']}, {x['seg']} s)")
    # (K) + (S): AZAR en w30, T 12 000, corte 10 000
    x = V.trabajo((20399, 'w30', 'AZAR', 12000, 10000, tempfile.mkdtemp(), False))
    so = x.get('banco_on_sombras') or {}
    alcanza = {g: round(so[g]['real'] + float(np.sum(so[g]['sombras'])), 4) for g in V.PAQUETE} if so else {}
    chk("(K) la mutacion alcanza a los 2 organos del paquete (real o sombras > 0) y a ninguno de los 5 fijos (real y 8 sombras en 0.0)",
        bool(so) and all(alcanza[g] > 0 for g in V.PAQUETE) and all(so[g]['real'] == 0.0 and all(v == 0.0 for v in so[g]['sombras']) for g in V.FIJOS),
        f"(paquete real + suma de sombras: {alcanza}; nacidos {x['n_nac']}, {x['seg']} s)")
    chk("(S) expresion en el corte: el real (del checkpoint) == banco_on (del motor) en los 7 organos, con 8 sombras cada uno",
        bool(so) and all(so[g]['real'] == x['banco_on'][g] and len(so[g]['sombras']) == 8 for g in V.ORGANOS),
        f"({ {g: (so[g]['real'], round(float(np.mean(so[g]['sombras'])), 3)) for g in V.ORGANOS} if so else None})")
    genes = list(V.ME2.NOMBRES)

    def fake(eleg=(), sube_sin_o2=(), azar_falso=False, bloq=0, incompleta=False, fijo=False):
        R = []
        for m in V.MUNDOS:
            for i in range(20):
                for b in V.BRAZOS:
                    sc = [0] * len(genes); on = {g: 0.0 for g in V.ORGANOS}; so_ = {g: dict(real=0.1, sombras=[0.1] * 8) for g in V.ORGANOS}
                    for g in V.PAQUETE: on[g] = 0.1
                    for g in eleg:
                        if b == 'VIDA' and i < 16: so_[g] = dict(real=0.9, sombras=[0.3] * 8)
                        if b == 'VIDA': on[g] = 0.6
                    for g in sube_sin_o2:
                        if b == 'VIDA' and i < 16: so_[g] = dict(real=0.9, sombras=[0.3] * 8)
                    if b == 'AZAR' and azar_falso and i < 9: sc[genes.index('eta')] = 1
                    von = dict(on)
                    if fijo and b == 'AZAR' and i == 3: von['mapa'] = 0.5
                    R.append(dict(seed=20311 + i, mundo=m, brazo=b, sel_corte=sc, banco_on=on, vivos_on=von, persiste=1, banco_on_sombras=so_,
                                  bloqueados=(bloq if (i == 0 and b == 'VIDA') else 0)))
        return R[:-1] if incompleta else R
    casos = [
        ("FUNCIONA: herencia e interruptor ELEGIDOS", fake(eleg=('herencia', 'interruptor')), 'FUNCIONA'),
        ("MODESTO: solo herencia ELEGIDO", fake(eleg=('herencia',)), 'HAY ALGO MODESTO'),
        ("MODESTO: herencia ELEGIDO e interruptor sube", fake(eleg=('herencia',), sube_sin_o2=('interruptor',)), 'HAY ALGO MODESTO'),
        ("MODESTO: los dos suben sin O2", fake(sube_sin_o2=('herencia', 'interruptor')), 'HAY ALGO MODESTO'),
        ("NO: solo interruptor sube", fake(sube_sin_o2=('interruptor',)), 'NO (en'),
        ("NO: nada sube", fake(), 'NO (en'),
        ("NO EVALUABLE: falsos positivos de AZAR", fake(eleg=('herencia', 'interruptor'), azar_falso=True), 'NO EVALUABLE (AZAR'),
        ("NO EVALUABLE: bloqueados", fake(eleg=('herencia', 'interruptor'), bloq=2), 'NO EVALUABLE (tope'),
        ("NO EVALUABLE: incompleta", fake(eleg=('herencia', 'interruptor'), incompleta=True), 'NO EVALUABLE (serie'),
        ("NO EVALUABLE: un organo fijo expresado", fake(eleg=('herencia', 'interruptor'), fijo=True), 'NO EVALUABLE (instrumento'),
    ]
    for nombre, R, esp in casos:
        v, L, d = V.veredicto(R, 20)
        chk(f"(V) {nombre}", v.startswith(esp), f"-> {v[:110]}")
    v, L, d = V.veredicto(fake(eleg=('herencia',), sube_sin_o2=('interruptor',)), 20)
    chk("(V) el perfil marca ELEGIDO y sube donde toca", all(d['perfil'][m] == {'herencia': 'ELEGIDO', 'interruptor': 'sube'} for m in V.MUNDOS), f"({d['perfil']})")
    malas = [['--help'], ['-h'], [], ['--serie'], ['--serie', '--ventana', 'serie'], ['--serie', '--ventana', 'otra', '--pool', '3'],
             ['--serie', '--ventana', 'serie', '--pool', '4'], ['--serie', '--ventana=serie', '--pool', '3'], ['--humo', '--gemelo'],
             ['--humo', '--pool', '2'], ['--humo', '--humo'], ['--prueba_pool', '--pool', '3'], ['--lee', 'x', '--pool', '2']]
    n_ab = 0
    for mm in malas:
        try: V.parsea(mm)
        except V.BanderaMala: n_ab += 1
    chk(f"(R) el parser aborta ante {len(malas)} formas malas", n_ab == len(malas), f"({n_ab}/{len(malas)})")
    antes = set(glob.glob(os.path.join(AQUI, 'datos', '**', '*'), recursive=True))
    pr = subprocess.run([sys.executable, os.path.join(AQUI, 'corre_eco_v4.py'), '--serie', '--ventana', 'serie', '--pool', '3', '--nada'],
                        capture_output=True, text=True, timeout=300)
    despues = set(glob.glob(os.path.join(AQUI, 'datos', '**', '*'), recursive=True))
    nuevos = {p for p in despues - antes if not p.startswith(os.path.join(AQUI, 'datos', 'eco_v'))}   # las series de la cola escriben en paralelo
    chk("(R) subproceso con bandera desconocida: codigo != 0 y no escribe nada", pr.returncode != 0 and not any('eco_v4' in p for p in despues - antes),
        f"(codigo {pr.returncode}; archivos nuevos fuera de las series en curso: {len(nuevos)})")
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
    open(os.path.join(AQUI, 'identidad_eco_v4_salida.txt'), 'w', encoding='utf-8').write(buf.getvalue())
    sys.exit(0 if ok else 1)
