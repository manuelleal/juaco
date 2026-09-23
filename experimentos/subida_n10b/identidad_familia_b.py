"""identidad_familia_b.py — ARNES DE IDENTIDAD de la subida del nivel 10, tanda 2 (n10b). Un proceso, sin Pool.

MISION: llegar a la AGI por este camino.

(0) ORIGEN: FABRICA.py, pista2.py, motor_convive.py, corre_convive.py y los carros de la tanda 1 que sirven de ancla
    (FAMILIA_NADA, FAMILIA_ORACULO) con sha fijado; los cinco FAMB_* son exactamente la construccion por anclas.
(I) PERILLA APAGADA: FAMB_NADA == FABRICA BIT A BIT en TODA la salida de pista2.run, en v2 (quimiostato y reposicion
    inmediata) y en v1 (diag=1, fundador_limpio, compat=1 con un carro). FAMB_NADA == FAMILIA_NADA (tanda 1) en v2.
(O) TECHO = TANDA 1: FAMB_ORACULO == FAMILIA_ORACULO (tanda 1) en TODA la salida (fisica + d['carro']), v2 con partos, misma
    etiqueta. Con (I) y (O), la serie 12301-12320 es la calibracion de los brazos NADA y ORACULO de este instrumento (ERR-116).
(P) ANTES DEL PRIMER PARTO los cinco modos son identicos en la fisica (misma etiqueta).
(B) EL CANAL, por unidad:
    B1 RES: al_parir = una entrada por (letra, necesidad), la R mas reciente VIVIDA, y la HEREDADA para lo no vivido; orden del ORACULO.
    B1 RES1: lo mismo SIN lo heredado.  NADA: None.
    B2 BAR: mismas claves, misma multiset de R, alguna R cambia de sitio, NO consume rng (Wl/KW/estado de rng_hijo == RES).
    B3 RES con la tabla verdadera COMPLETA == ORACULO: mismo nodo instalado y MISMA via lenta tras la lectura (misma dosis).
    B4 la lectura cambia la via lenta en RES y no en NADA.
(D) DETERMINISMO: RES dos veces == RES.
(C) EN MARCHA (v2, T=8000): hay partos; RES se separa de NADA; la telemetria registra tablas instaladas.
(R) RUNNER (ERR-115): corre_n10b.parsea aborta ante bandera desconocida, abreviada, con '=', repetida, '--help', humo con --pool,
    serie con --T; valida_semillas acepta 12701-12720 y 12721-12740 y rechaza la tanda 1 y la practica. Un subproceso con una
    bandera desconocida sale con codigo != 0 sin escribir nada. NUNCA se ejecuta --serie.
"""
import hashlib, importlib.util, json, os, subprocess, sys, time
import numpy as np

sys.stdout.reconfigure(encoding='utf-8', errors='replace')
AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
GEN = os.path.join(RAIZ, 'experimentos', 'generaciones')
N10 = os.path.join(RAIZ, 'experimentos', 'subida_n10')
sys.path.insert(0, GEN); sys.path.insert(0, AQUI)
import construye_familia_b as CB
import corre_n10b as CR
import pista2 as P2

SHAS = {os.path.join(RAIZ, 'experimentos', 'carrera_escuderias', 'carros', 'FABRICA.py'): '2ebee3e99ea5a33a',
        os.path.join(GEN, 'pista2.py'): '4d2bee16e7961261',
        os.path.join(GEN, 'motor_convive.py'): 'd10cb9021f5d0f41',
        os.path.join(GEN, 'corre_convive.py'): 'e6dadfdad9c379cd',
        os.path.join(N10, 'carros', 'FAMILIA_NADA.py'): 'f7ae98715f170153',
        os.path.join(N10, 'carros', 'FAMILIA_ORACULO.py'): '55df592f57671b54'}
PRACTICA = (12791, 12792, 12793)
OK = []; MAL = []


def h16(p): return hashlib.sha256(open(p, 'rb').read()).hexdigest()[:16]


def carga_de(p, nombre):
    spec = importlib.util.spec_from_file_location(nombre, p)
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m


def carga(et): return carga_de(os.path.join(AQUI, 'carros', f'FAMB_{et}.py'), f'carro_FAMB_{et}')


def canon(x):
    if isinstance(x, dict): return {str(k): canon(v) for k, v in sorted(x.items(), key=lambda kv: str(kv[0]))}
    if isinstance(x, (list, tuple)): return [canon(v) for v in x]
    if isinstance(x, np.ndarray): return [canon(v) for v in x.tolist()]
    if isinstance(x, (np.integer,)): return int(x)
    if isinstance(x, (np.floating, float)): return repr(float(x))
    if isinstance(x, (np.bool_,)): return bool(x)
    if isinstance(x, (set, frozenset)): return sorted(canon(v) for v in x)
    return x


def huella(r): return hashlib.sha256(json.dumps(canon(r), sort_keys=True).encode()).hexdigest()[:16]


def fisica(r): return [{k: v for k, v in d.items() if k != 'carro'} for d in r['linajes']], r['pista']


def chk(nombre, cond, detalle=''):
    (OK if cond else MAL).append(nombre)
    print(f"  {'OK ' if cond else 'MAL'} {nombre} {detalle}", flush=True)


def ctx_prueba(i=0, k=1, seed=12791):
    cf = P2.cfg_fabrica(); kw = cf['kw']
    return dict(id=f'X/{k}', indice=i, n_linajes=9, T=100000, L=cf['L'] * 9, PAT={a: v.copy() for a, v in cf['PAT'].items()},
                rng=np.random.default_rng([seed, i, 12, k]), dote=kw['dote'], rep_umbral=kw['rep_umbral'], costo=kw['costo'],
                costo_a=kw['costo_a'], rep_X=kw['rep_X'], cupo=P2.CUPO, ancho=P2.ANCHO, fabrica=P2.cfg_fabrica())


def aborta(argv):
    try: CR.parsea(argv); return False
    except CR.BanderaMala: return True


def main():
    t0 = time.time()
    print(f"identidad_familia_b.py {h16(os.path.abspath(__file__))}")
    print("(0) origen y construccion", flush=True)
    for p, s in SHAS.items(): chk(f"sha {os.path.basename(p)}", h16(p) == s, f"{h16(p)} (esperado {s})")
    src = open(CB.ORIGEN, encoding='utf-8').read()
    for et, modo in CB.MODOS.items():
        p = os.path.join(AQUI, 'carros', f'FAMB_{et}.py')
        chk(f"FAMB_{et}.py == construccion por anclas", open(p, encoding='utf-8').read() == CB.construye_texto(src, et, modo), h16(p))
    M = {et: carga(et) for et in CB.MODOS}
    FAB = P2.carga_carro('FABRICA')
    F1N = carga_de(os.path.join(N10, 'carros', 'FAMILIA_NADA.py'), 'n10_FAMILIA_NADA')
    F1O = carga_de(os.path.join(N10, 'carros', 'FAMILIA_ORACULO.py'), 'n10_FAMILIA_ORACULO')

    print("(I) perilla apagada: FAMB_NADA == FABRICA en toda la salida", flush=True)
    casos = [(PRACTICA[0], 6000, dict(solapadas=1, diag=0, reposicion='fija')),
             (PRACTICA[1], 6000, dict(solapadas=1, diag=0, reposicion='fija')),
             (PRACTICA[2], 4000, dict(solapadas=1, diag=0, reposicion='inmediata')),
             (PRACTICA[0], 4000, dict(solapadas=0, diag=1)),
             (PRACTICA[1], 3000, dict(solapadas=0, diag=1, compat=0, fundador_limpio=1))]
    for seed, T, kw in casos:
        a = P2.run(seed, [('FABRICA', FAB)] * 9, T=T, **kw)
        b = P2.run(seed, [('FABRICA', M['NADA'])] * 9, T=T, **kw)
        nac = sum(d.get('nacimientos', 0) for d in a['linajes'])
        chk(f"I s{seed} T{T} {kw}", huella(a) == huella(b), f"{huella(a)} {huella(b)} nacimientos {nac}")
    a = P2.run(PRACTICA[0], [('FABRICA', FAB)], T=5000, compat=1, pizarra=0)
    b = P2.run(PRACTICA[0], [('FABRICA', M['NADA'])], T=5000, compat=1, pizarra=0)
    chk("I v1 compat=1 (1 carro)", huella(a) == huella(b), f"{huella(a)} {huella(b)}")
    a = P2.run(PRACTICA[1], [('FAM', F1N)] * 9, T=6000, solapadas=1, diag=0, reposicion='fija')
    b = P2.run(PRACTICA[1], [('FAM', M['NADA'])] * 9, T=6000, solapadas=1, diag=0, reposicion='fija')
    chk("I FAMB_NADA == FAMILIA_NADA (tanda 1), v2", huella(a) == huella(b), f"{huella(a)} {huella(b)}")

    print("(O) techo = tanda 1: FAMB_ORACULO == FAMILIA_ORACULO en toda la salida (con partos)", flush=True)
    for seed, T in ((PRACTICA[0], 8000), (PRACTICA[2], 8000)):
        a = P2.run(seed, [('FAM_ORA', F1O)] * 9, T=T, solapadas=1, diag=0, reposicion='fija')
        b = P2.run(seed, [('FAM_ORA', M['ORACULO'])] * 9, T=T, solapadas=1, diag=0, reposicion='fija')
        nac = sum(d.get('nacimientos', 0) for d in a['linajes'])
        chk(f"O s{seed} T{T} v2 fija", huella(a) == huella(b) and nac > 0, f"{huella(a)} {huella(b)} nacimientos {nac}")

    print("(P) antes del primer parto los cinco modos son identicos en la fisica", flush=True)
    hs = {}; nac = 0
    for et in CB.MODOS:
        r = P2.run(PRACTICA[2], [('FAMB', M[et])] * 9, T=450, solapadas=1, diag=0, reposicion='fija')
        hs[et] = huella(fisica(r)); nac += sum(d['nacimientos'] for d in r['linajes'])
    chk("P fisica NADA==RES==RES1==BAR==ORACULO (T=450, 0 partos)", len(set(hs.values())) == 1 and nac == 0, str(hs))

    print("(B) el canal, por unidad", flush=True)
    PAT = P2.cfg_fabrica()['PAT']; pv = lambda k: [float(z) for z in PAT[k]]
    her = [[pv('B'), -3.0, 0], [pv('D'), 0.0, 0]] * 50          # lo heredado (en NODO_LEE copias, como lo instala nace)
    mordh = [[1, 'A', 0, 1.0], [2, 'C', 1, 1.0], [3, 'D', 0, 0.0], [4, 'A', 0, 1.0], [5, 'C', 0, 0.0]]
    esper_res = {('A', 0): 1.0, ('B', 0): -3.0, ('C', 0): 0.0, ('D', 0): 0.0, ('C', 1): 1.0}
    esper_r1 = {('A', 0): 1.0, ('C', 0): 0.0, ('D', 0): 0.0, ('C', 1): 1.0}
    def tabla(msg): return {(k, n): r for p, r, n in msg for k in 'ABCD' if pv(k) == list(p)}
    msgs = {}
    for et in ('RES', 'RES1', 'BAR'):
        pa = M[et].crea(ctx_prueba()); pa._nodo = [[list(p), r, n] for p, r, n in her]; pa._mordh = [list(x) for x in mordh]
        msgs[et] = pa.al_parir(dict(t=9, k=1))
    chk("B1 RES = vivido mas reciente + heredado no vivido", tabla(msgs['RES']) == esper_res and len(msgs['RES']) == 5, str(tabla(msgs['RES'])))
    chk("B1 RES orden del ORACULO (necesidad, letra)", [(n, next(k for k in 'ABCD' if pv(k) == p)) for p, r, n in msgs['RES']]
        == [(0, 'A'), (0, 'B'), (0, 'C'), (0, 'D'), (1, 'C')])
    chk("B1 RES1 = solo lo vivido", tabla(msgs['RES1']) == esper_r1 and len(msgs['RES1']) == 4, str(tabla(msgs['RES1'])))
    chk("B1 BAR entrega lo mismo que RES (el barajado es al nacer)", msgs['BAR'] == msgs['RES'])
    chk("B1 NADA al_parir = None", M['NADA'].crea(ctx_prueba()).al_parir(dict(t=1, k=1)) is None)
    pa = M['RES'].crea(ctx_prueba()); pa._mordh = [[1, 'D', 0, 0.0], [2, 'D', 0, 0.0]]; pa._nodo = [[pv('D'), -3.0, 0]] * 3
    chk("B1 RES: lo vivido pisa lo heredado", tabla(pa.al_parir(dict(t=3, k=1))) == {('D', 0): 0.0})
    hijos = {}
    full = [[pv(k), (1.0 if (k, n) in (('A', 0), ('C', 1)) else (-3.0 if (k, n) in (('B', 0), ('D', 1)) else 0.0)), n]
            for n in (0, 1) for k in 'ABCD']
    for et, mem in (('NADA', msgs['RES']), ('RES', msgs['RES']), ('BAR', msgs['RES']), ('RESF', full), ('ORACULO', msgs['RES'])):
        h = M['RES' if et == 'RESF' else et].crea(ctx_prueba(k=2)); rh = np.random.default_rng([12791, 0, 13, 2])
        h.nace(dict(t=1, k=2, fundador=False, memoria=[[list(p), r, n] for p, r, n in mem], rng_hijo=rh, padre='X/1'))
        hijos[et] = (h, rh.bit_generator.state['state']['state'])
    hb, hr = hijos['BAR'][0], hijos['RES'][0]
    ub = [tuple(x[0]) + (x[2],) for x in hb._nodo[:5]]; ur = [tuple(x[0]) + (x[2],) for x in hr._nodo[:5]]
    chk("B2 BAR mismas claves y dosis que RES", ub == ur and len(hb._nodo) == len(hr._nodo) == 5 * hr.NODO_LEE)
    chk("B2 BAR misma multiset de R", sorted(x[1] for x in hb._nodo) == sorted(x[1] for x in hr._nodo))
    chk("B2 BAR destruye la asociacion (alguna R cambia de sitio)", [x[1] for x in hb._nodo[:5]] != [x[1] for x in hr._nodo[:5]],
        f"{[x[1] for x in hr._nodo[:5]]} -> {[x[1] for x in hb._nodo[:5]]}")
    chk("B2 BAR no consume rng: mismos Wl/KW y mismo estado de rng_hijo que RES y NADA",
        np.array_equal(hb.Wl, hr.Wl) and np.array_equal(hb.KW, hr.KW) and hijos['BAR'][1] == hijos['RES'][1] == hijos['NADA'][1])
    hf, ho = hijos['RESF'][0], hijos['ORACULO'][0]
    chk("B3 RES con la tabla COMPLETA == ORACULO: mismo nodo y misma via lenta",
        canon(hf._nodo) == canon(ho._nodo) and np.array_equal(hf.Wps, ho.Wps) and np.array_equal(hf.Wns, ho.Wns)
        and (np.abs(ho.Wps).sum() + np.abs(ho.Wns).sum()) > 0, f"len {len(hf._nodo)} {len(ho._nodo)}")
    hn = hijos['NADA'][0]
    chk("B4 la lectura cambia la via lenta en RES y no en NADA", (np.abs(hr.Wps).sum() + np.abs(hr.Wns).sum()) > 0 and
        (np.abs(hn.Wps).sum() + np.abs(hn.Wns).sum()) == 0 and hn._nodo == [])

    print("(D)/(C) determinismo y canal en marcha (v2, T=8000)", flush=True)
    M2 = {et: carga(et) for et in ('RES',)}   # modulo fresco: telemetria vacia
    r1 = P2.run(PRACTICA[0], [('FAMB_RES', M2['RES'])] * 9, T=8000, solapadas=1, diag=0, reposicion='fija')
    n_tele = len(M2['RES']._TELE); cl = sorted(x[1] for x in M2['RES']._TELE)
    r2 = P2.run(PRACTICA[0], [('FAMB_RES', carga('RES'))] * 9, T=8000, solapadas=1, diag=0, reposicion='fija')
    chk("D RES determinista", huella(r1) == huella(r2), huella(r1))
    nac = sum(d['nacimientos'] for d in r1['linajes'])
    chk("C hubo partos en la prueba", nac > 0, f"nacimientos {nac}")
    rN = P2.run(PRACTICA[0], [('FAMB_RES', M['NADA'])] * 9, T=8000, solapadas=1, diag=0, reposicion='fija')
    chk("C con partos, RES se separa de NADA en la fisica", huella(fisica(r1)) != huella(fisica(rN)))
    chk("C telemetria: una tabla instalada por hijo nacido", n_tele == nac, f"tablas {n_tele} nacidos {nac} claves {cl}")

    print("(R) runner: lista blanca (ERR-115) y semillas; nunca se ejecuta --serie", flush=True)
    malas = [['--humo', '--xyz'], ['--hum'], ['--humo', '--T=100'], ['--humo', '--humo'], ['--help'], ['--humo', '--pool', '2'],
             ['--serie', '--desde', '12701', '--T', '5000'], ['--serie'], ['--humo', '--desde'], ['--humo', '--n', 'x'], [], ['-h'],
             ['--serie', '--humo', '--desde', '12701']]
    chk("R parsea aborta en los 13 casos malos", all(aborta(x) for x in malas), str([x for x in malas if not aborta(x)]))
    chk("R parsea acepta humo y serie bien formados", not aborta(['--humo']) and not aborta(['--serie', '--desde', '12701', '--n', '20', '--pool', '6']))
    def vs(d, n):
        try: return CR.valida_semillas(d, n)
        except CR.BanderaMala: return False
    chk("R semillas: acepta 12701-12720 y 12721-12740; rechaza 12301 (tanda 1), 12791 (practica), 12711+20",
        vs(12701, 20) and vs(12721, 20) and not vs(12301, 20) and not vs(12791, 5) and not vs(12711, 20))
    antes = set(os.listdir(os.path.join(AQUI, 'datos', 'humo')))
    p = subprocess.run([sys.executable, os.path.join(AQUI, 'corre_n10b.py'), '--humo', '--bandera_que_no_existe'], capture_output=True, text=True, timeout=120)
    chk("R subproceso con bandera desconocida: codigo != 0 y no escribe nada", p.returncode != 0 and set(os.listdir(os.path.join(AQUI, 'datos', 'humo'))) == antes,
        f"codigo {p.returncode} · {p.stderr.strip()[-90:]}")
    chk("R shas de corre_n10b.SHAS == carros construidos", all(h16(q) == s for q, s in CR.SHAS.items()))

    print(f"RESULTADO: {len(OK)}/{len(OK) + len(MAL)}  ({time.time() - t0:.0f} s)" + (f"  FALLAN: {MAL}" if MAL else ''))
    return 0 if not MAL else 1


if __name__ == '__main__':
    if len(sys.argv) > 1: raise SystemExit(f"identidad_familia_b: no admite argumentos ({sys.argv[1:]})")
    sys.exit(main())
