"""identidad_frio_carrera.py — ARNES del bloque frio_carrera. Sin el, no hay serie. Un proceso, sin Pool, corridas cortas (T <= 5000).

MISION: llegar a la AGI por este camino. Con las perillas apagadas (RES0 = BAR = TELEM = 0) los carros frio_carrera son V143 bit a bit
en la pista de la carrera (N 9, fundador limpio); la telemetria es de solo lectura; la entrada del runner es corre_v143.tarea campo a
campo (regla 14); el filtro quita de verdad las neutras; BAR permuta de verdad; nube-9 atrapado; ERR-115; la letra.
Salida: identidad_frio_carrera_salida.txt (y por pantalla). Semillas de practica 36901-36904.

    python experimentos/organelos/frio_carrera/identidad_frio_carrera.py
"""
import io, json, os, sys, time, contextlib
AQUI = os.path.dirname(os.path.abspath(__file__))
if AQUI not in sys.path: sys.path.insert(0, AQUI)
import corre_frio_carrera as R
CV = R.CV; P = R.P; CF = R.CF; RC = R.RC
N = lambda x: json.loads(json.dumps(x, default=str))
OUT = []; RES = []


def log(s=''):
    print(s, flush=True); OUT.append(s)


def chk(nombre, cond, extra=''):
    RES.append(bool(cond)); log(f"  [{'OK ' if cond else 'FALLA'}] {nombre}{(' · ' + extra) if extra else ''}")


class Perillas:
    def __init__(self, m, **kw): self.m = m; self.kw = kw
    def __enter__(self):
        self.g = {k: getattr(self.m, k) for k in self.kw}
        for k, v in self.kw.items(): setattr(self.m, k, v)
    def __exit__(self, *a):
        for k, v in self.g.items(): setattr(self.m, k, v)


def sin_fc(r):
    """Copia de la salida de P.run SIN la clave de telemetria frio_carrera (lo unico que TELEM agrega)."""
    r = N(r)
    for d in r['linajes']:
        if isinstance(d.get('carro'), dict): d['carro'].pop('frio_carrera', None)
    return r


def main():
    t0 = time.time()
    log(f"IDENTIDAD frio_carrera · {time.strftime('%Y-%m-%d %H:%M:%S')} · python {sys.version.split()[0]} · numpy {R.P.np.__version__}")
    log(f"  corre_frio_carrera.py {R.h16(R.__file__)} · construye_frio_carrera.py {R.h16(CF.__file__)} · este arnes {R.h16(os.path.abspath(__file__))}")
    # (K) construccion por anclas y chequeo estatico
    log("(K) construccion y chequeo estatico")
    with contextlib.redirect_stdout(io.StringIO()) as so: rc = CF.main(['--verifica'])
    chk("(K1) carros en disco == construye_frio_carrera (origen V143.py 2a03048a7f1525e5; variantes solo difieren en perillas/nombre)", rc == 0,
        so.getvalue().strip().replace('\n', ' | ')[:300])
    shas_ok = all(R.h16(p) == s for p, s in R.SHAS.items())
    chk("(K2) sha de corre_v143, V143, pista, juez, O1 == fijados", shas_ok)
    for n in R.PROPIOS:
        v = RC.revisa_fuente(open(os.path.join(R.CARROS, n + '.py'), encoding='utf-8').read(), n)
        chk(f"(K3) revisa_carro {n}: PASA (sin np.random, sin default_rng, sin imports fuera de lista)", not v, str(v[:2]))
    R.registra()
    V = CV.modulo('V143'); M = {n: CV._MODS[n] for n in R.PROPIOS}
    # (A) perillas apagadas == V143, salida ENTERA
    log("(A) perillas apagadas == V143 bit a bit (salida ENTERA de pista.run: fisica + carro + pizarra; N 9, fundador limpio)")
    for n, s, T in (('V143_RES0', 36901, 3000), ('V143_RES0', 36902, 3000), ('V143_BAR0', 36903, 3000), ('V143_TEL', 36904, 3000)):
        a = P.run(s, [('C', V)] * 9, T=T, fundador_limpio=1)
        with Perillas(M[n], RES0=0, BAR=0, TELEM=0): b = P.run(s, [('C', M[n])] * 9, T=T, fundador_limpio=1)
        nac = sum(sum(d['origen_cuerpo']) for d in a['linajes'])
        chk(f"(A) {n} con RES0 = BAR = TELEM = 0 == V143 (s {s}, T {T})", N(a) == N(b), f"nacimientos reales en la corrida {nac}")
    # (B) TELEM es de solo lectura
    log("(B) TELEM = 1 no toca la conducta: todo igual salvo la clave d['carro']['frio_carrera']")
    a = P.run(36901, [('C', V)] * 9, T=5000, fundador_limpio=1)
    b = P.run(36901, [('C', M['V143_TEL'])] * 9, T=5000, fundador_limpio=1)
    fcb = [d['carro'].get('frio_carrera') for d in b['linajes']]
    tel = {k: sum(x[k] for x in fcb if x) for k in ('lect', 'entradas', 'neutras', 'sel', 'sel_neutras')}
    chk("(B1) V143_TEL == V143 (s 36901, T 5000) en todo salvo la telemetria", sin_fc(a) == sin_fc(b))
    chk("(B2) la telemetria existe en los 9 linajes y hubo lecturas del nodo", all(fcb) and tel['lect'] > 0, str(tel))
    log(f"      DATO (V143 = V143_TEL, s 36901, T 5000; ultima instancia de cada linaje): entradas del nodo en las lecturas {tel['entradas']}, "
        f"neutras {tel['neutras']} ({tel['neutras'] / max(1, tel['entradas']):.3f}); de las leidas por la via lenta {tel['sel']}, neutras "
        f"{tel['sel_neutras']} ({tel['sel_neutras'] / max(1, tel['sel']):.3f})")
    # (C) regla 14: la entrada del runner es corre_v143.tarea
    log("(C) regla 14: la tarea del runner == corre_v143.tarea campo a campo")
    x = R.tarea((36902, 'V143', 2000)); y = CV.tarea((36902, 'V143', 2000))
    tf = x.pop('tel_fc'); x.pop('seg'); y.pop('seg')
    chk("(C1) runner.tarea(V143) == corre_v143.tarea(V143) (s 36902, T 2000), salvo seg; tel_fc = 9 x None", N(x) == N(y) and tf == [None] * 9)
    with Perillas(M['V143_RES0'], RES0=0, BAR=0, TELEM=0): z = R.tarea((36902, 'V143_RES0', 2000))
    z.pop('tel_fc'); z.pop('seg')
    zz = json.loads(json.dumps(N(z)).replace('"V143_RES0#', '"V143#'))   # la unica diferencia legitima: la etiqueta del linaje
    chk("(C2) runner.tarea(V143_RES0 apagado) == corre_v143.tarea(V143) (s 36902, T 2000), salvo la etiqueta 'V143_RES0#i'", zz == N(y) and N(z) != N(y))
    chk("(C3) P.run quedo restaurado tras la captura", P.run is R.P.run and P.run.__name__ == 'run')
    # (D) el filtro RES0 quita las neutras y solo ellas; el nodo guardado no cambia
    log("(D) RES0: el nacido lee el nodo sin neutras (prueba directa sobre un nodo conocido y en la pista)")
    ctx = dict(id='X', indice=3, n_linajes=9, T=1000, L=360, PAT={k: v.copy() for k, v in P.cfg_fabrica()['PAT'].items()},
               rng=P.np.random.default_rng(1), dote=0.6, rep_umbral=0.8, costo=0.001, costo_a=0.001, rep_X=500, cupo=16, ancho=8,
               fabrica=P.cfg_fabrica())
    c = M['V143_RES0'].crea(ctx)
    nodo = [[[1., 1., 0., 1., 0., 0.], 1.0, 0], [[1., 1., 0., 1., 0., 0.], 0.0, 1], [[1., 0., 1., 0., 1., 0.], -3.0, 0],
            [[0., 1., 1., 0., 0., 1.], 1.0, 1], [[1., 0., 1., 0., 1., 0.], 0.0, 1], [[0., 0., 1., 0., 1., 1.], -3.0, 1]]
    c._nodo = [list(e) for e in nodo]
    m1 = c._fc_msg(dict(t=100, k=5))
    chk("(D1) quita exactamente las 2 neutras y deja las 4 con consecuencia, en orden", m1 == [e for e in nodo if e[1] != 0.0])
    chk("(D2) el nodo guardado no cambia", c._nodo == nodo)
    a = P.run(36903, [('C', V)] * 9, T=5000, fundador_limpio=1)
    b = P.run(36903, [('C', M['V143_RES0'])] * 9, T=5000, fundador_limpio=1)
    fr = [d['carro']['frio_carrera'] for d in b['linajes']]
    s = {k: sum(x[k] for x in fr) for k in ('lect', 'entradas', 'neutras', 'pasan', 'sel', 'sel_neutras')}
    chk("(D3) en la pista: 0 neutras leidas, pasan = entradas - neutras, hubo neutras que quitar",
        s['sel_neutras'] == 0 and s['pasan'] == s['entradas'] - s['neutras'] and s['neutras'] > 0, str(s))
    chk("(D4) RES0 NO es inerte: la salida cambia respecto de V143 (s 36903, T 5000)", N(a) != N(b))
    # (E) BAR permuta de verdad
    log("(E) BAR: permuta las R entre entradas (multiconjunto, patron y necesidad intactos), determinista, sin rng de nadie")
    cb = M['V143_BAR0'].crea(ctx); cb._nodo = [list(e) for e in nodo]
    st0 = ctx['rng'].bit_generator.state
    m2 = cb._fc_msg(dict(t=100, k=5)); m3 = cb._fc_msg(dict(t=100, k=5)); m4 = cb._fc_msg(dict(t=101, k=5))
    base = [e for e in nodo if e[1] != 0.0]
    chk("(E1) sin neutras; multiconjunto de R igual; patron y necesidad en su sitio",
        sorted(e[1] for e in m2) == sorted(e[1] for e in base) and [(e[0], e[2]) for e in m2] == [(e[0], e[2]) for e in base] and 0.0 not in [e[1] for e in m2])
    chk("(E2) determinista (mismo t, k -> misma permutacion) y cambia con t", m2 == m3 and (m2 != m4 or m3 != m4))
    chk("(E3) no consume el rng del cuerpo", ctx['rng'].bit_generator.state == st0)
    chk("(E4) el nodo guardado no cambia", cb._nodo == nodo)
    cambios = 0; pruebas = 200
    for t in range(pruebas):
        mm = cb._fc_msg(dict(t=1000 + t, k=t)); cambios += int([e[1] for e in mm] != [e[1] for e in base])
    chk("(E5) la permutacion cambia alguna R en >= 0.5 de 200 lecturas del nodo conocido", cambios / pruebas >= 0.5, f"{cambios}/{pruebas}")
    # el arnes (no el carro) guarda TODAS las instancias (fundador limpio = instancia nueva) para sumar su telemetria
    inst = []; crea0 = M['V143_BAR0'].crea
    M['V143_BAR0'].crea = lambda ctx: inst.append(crea0(ctx)) or inst[-1]
    try:
        b2 = P.run(36903, [('C', M['V143_BAR0'])] * 9, T=5000, fundador_limpio=1)
    finally:
        M['V143_BAR0'].crea = crea0
    sb = {k: sum(c_._fc[k] for c_ in inst) for k in ('lect', 'bar_lect', 'bar_distintas', 'bar_cambian', 'bar_entradas', 'sel_neutras')}
    sb['instancias'] = len(inst)
    chk(f"(E6) en la pista (todas las instancias): la permutacion cambia alguna R en >= {R.BAR_REAL} de las lecturas; 0 neutras leidas",
        sb['bar_lect'] > 0 and sb['bar_distintas'] / sb['bar_lect'] >= R.BAR_REAL and sb['sel_neutras'] == 0, str(sb))
    chk("(E7) BAR0 != RES0 en la pista (s 36903, T 5000)", N(b2) != N(b))
    # (G) determinismo
    b3 = P.run(36903, [('C', M['V143_RES0'])] * 9, T=5000, fundador_limpio=1)
    chk("(G) determinismo: V143_RES0 dos veces == (s 36903, T 5000)", N(b3) == N(b))
    # (F) nube-9
    log("(F) nube-9: un SystemExit dentro de la corrida no mata al trabajador; se marca aborto y se escribe el JSON")
    import types, tempfile
    fake = types.ModuleType('carro_FALLA')
    def _crea(ctx): raise SystemExit('H1: mas de 100000 partos: la semilla del hijo colisionaria (ERR-60)')
    fake.crea = _crea; CV._MODS['FALLA'] = fake; R.BRAZOS['falla'] = 'FALLA'
    try:
        with tempfile.TemporaryDirectory() as td:
            try:
                xf = R.trabajo((36904, 'falla', 1000, td, False)); vivo = True
            except BaseException:
                xf = {}; vivo = False
            escrito = os.path.exists(os.path.join(td, 'falla_s36904.json'))
            chk("(F1) SystemExit atrapado, aborto marcado, JSON escrito", vivo and str(xf.get('aborto', '')).startswith('SystemExit') and escrito,
                str(xf.get('aborto'))[:80])
            with open(os.path.join(td, 'res0_s36904.json'), 'w', encoding='utf-8') as fh: json.dump(dict(seed=36904, brazo='res0', aborto=None, marca=1, linajes=[]), fh)
            xr = R.trabajo((36904, 'res0', 1000, td, True))
            chk("(F2) --reanuda devuelve el JSON ya escrito sin volver a correr", xr.get('marca') == 1)
    finally:
        R.BRAZOS.pop('falla', None); CV._MODS.pop('FALLA', None)
    let = R.lee_serie({'v143': dict(R0_real_med=0.6, coherente='180/180', gana_e5=False),
                       'res0': dict(R0_real_med=0.6, coherente='180/180', gana_e5=False), 'bar0': dict(R0_real_med=0.5, coherente='180/180', gana_e5=False),
                       'o1': dict(R0_real_med=0.94, coherente='180/180', gana_e5=True)}, {}, {'res0': dict(sel_neutras=0), 'bar0': dict(frac_bar_distintas=0.9)},
                      True, 1)
    chk("(F3) con 1 aborto la serie es NO SE LEE", let['veredicto'] == 'NO SE LEE')
    # (H) ERR-115 y semillas
    log("(H) ERR-115: banderas desconocidas o abreviadas abortan; semillas y T ajenos se rechazan")
    def aborta(argv):
        try:
            with contextlib.redirect_stderr(io.StringIO()): R.main(argv)
            return False
        except SystemExit: return True
    for argv in (['--humo', '--xyz'], ['--hum'], ['--help'], ['--serie', '--desde', '14301', '--n', '20'], ['--serie', '--T', '20000'],
                 ['--humo', '--pool', '6'], ['--humo', '--desde', '36001', '--n', '1'], ['--serie', '--brazos', 'v143,res0'],
                 ['--humo', '--T', '40000', '--desde', '36905', '--n', '1'], ['--humo', '--desde', '36901', '--n', '4', '--brazos', 'v143,res0']):
        chk(f"(H) aborta: {' '.join(argv)}", aborta(argv))
    # (V) la letra
    log("(V) la letra (sec. 6) sobre entradas sinteticas")
    def fal(r0v=0.6, gr=True, gb=False, go=True, w_rv=18, d_rv=0.15, w_rb=18, sel=0, fb=0.9, comp=True, ab=0):
        res = {'v143': dict(R0_real_med=r0v, coherente='180/180', gana_e5=False), 'res0': dict(R0_real_med=0.95, coherente='180/180', gana_e5=gr),
               'bar0': dict(R0_real_med=0.3, coherente='180/180', gana_e5=gb), 'o1': dict(R0_real_med=0.94, coherente='180/180', gana_e5=go)}
        par = {('res0', 'v143'): dict(semillas=20, gana=w_rv, dif_med=d_rv), ('res0', 'bar0'): dict(semillas=20, gana=w_rb, dif_med=0.3)}
        return R.lee_serie(res, par, {'res0': dict(sel_neutras=sel), 'bar0': dict(frac_bar_distintas=fb)}, comp, ab)['veredicto']
    casos = [(dict(), 'FUNCIONA'), (dict(gr=False), 'HAY ALGO MODESTO'), (dict(gr=False, d_rv=0.05), 'NO'), (dict(gb=True), 'HAY ALGO MODESTO'),
             (dict(w_rv=14), 'NO'), (dict(w_rv=15, gr=False, d_rv=0.10), 'HAY ALGO MODESTO'), (dict(gr=False, w_rb=14), 'NO'),
             (dict(go=False), 'NO SE LEE'), (dict(r0v=0.39), 'NO SE LEE'), (dict(r0v=0.81), 'NO SE LEE'), (dict(sel=3), 'NO SE LEE'),
             (dict(fb=0.4), 'NO SE LEE'), (dict(comp=False), 'NO SE LEE'), (dict(gb=True, w_rb=10), 'NO')]
    for kw, esp in casos:
        v = fal(**kw); chk(f"(V) {kw or 'todo pasa'} -> {esp}", v == esp, f"da {v}")
    for a_, b_, esp in (('FUNCIONA', 'FUNCIONA', 'FUNCIONA'), ('FUNCIONA', 'HAY ALGO MODESTO', 'HAY ALGO MODESTO'), ('FUNCIONA', 'NO', 'NO'),
                        ('NO', 'NO SE LEE', 'NO SE LEE'), ('HAY ALGO MODESTO', 'HAY ALGO MODESTO', 'HAY ALGO MODESTO')):
        chk(f"(V) bloque {a_} + {b_} -> {esp}", R.bloque(a_, b_) == esp)
    ok = sum(RES); log(f"\nRESULTADO: {ok}/{len(RES)} ({time.time() - t0:.0f} s)")
    with open(os.path.join(AQUI, 'identidad_frio_carrera_salida.txt'), 'w', encoding='utf-8') as fh: fh.write('\n'.join(OUT) + '\n')
    return 0 if ok == len(RES) else 1


if __name__ == '__main__':
    sys.exit(main())
