"""prearnes_unitario.py — PRE-ARNES SIN PISTA (milisegundos; no es una corrida): el carro O1_MURO_GEN contra O1 con ENTRADAS FALSAS.
No sustituye a identidad_muro_perillas.py (salida entera de la pista); sirve para no entregar un carro que reviente al primer paso cuando
la CPU esta al tope (regla de CPU del encargo). Tambien prueba fila()/lee_mapa() con un crudo EXISTENTE (brazo o1 de tronco_v14_3) y la letra
sintetica del Paso 2 con GEN_LETRA puesto EN MEMORIA (el archivo sigue con None).
    python experimentos/organelos/muro_perillas/prearnes_unitario.py
"""
import glob, importlib.util, json, os, sys, tempfile

sys.stdout.reconfigure(encoding='utf-8', errors='replace')
AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(AQUI)))
sys.path[:0] = [AQUI, os.path.join(RAIZ, 'experimentos', 'tronco_v14_3'), os.path.join(RAIZ, 'experimentos', 'carrera_escuderias')]
import corre_muro_perillas as R
import construye_muro_perillas as CB
import numpy as np
OK = []


def ok(c, t): OK.append(bool(c)); print(f"  {'OK   ' if c else 'FALLA'} {t}")


def carga(ruta, nombre):
    spec = importlib.util.spec_from_file_location(nombre, ruta); m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m


def ctx(i, rng):
    return dict(id=f"X#{i}", indice=i, n_linajes=9, T=1000, L=360, PAT={}, rng=rng, dote=0.6, rep_umbral=1.0, costo=0.001, costo_a=0.001, rep_X=1, cupo=16, ancho=8, fabrica={})


def episodio(mod, n_pasos=400, seed=5, siembra=None, lee=1, sigma=0.0, por_linaje=None):
    """Un 'mundo' de mentira: 9 carros, objetos fijos en un anillo, niveles que bajan; devuelve la traza de decisiones y la memoria heredada."""
    es_gen = hasattr(mod, 'PERILLAS')
    if es_gen: R._pon(mod, siembra, seed, sigma, (CB.DELTA if sigma else 0.0), lee, 1, por_linaje)
    rng = np.random.default_rng(seed); cars = [mod.crea(ctx(i, np.random.default_rng([seed, i]))) for i in range(9)]
    objs = {int(x): 'ABCD'[int(rng.integers(4))] for x in rng.choice(360, 36, replace=False)}
    pos = [int(x) for x in rng.integers(360, size=9)]; E = [1.0] * 9; A = [1.0] * 9; traza = []
    for t in range(n_pasos):
        foto = tuple((cars[i].yo, pos[i], objs.get(pos[i]), None) for i in range(9))
        for i, c in enumerate(cars):
            a = c.actua(dict(t=t, pos=pos[i], E=E[i], Ag=A[i], objs=objs, cuerpos=foto, pizarra=(), yo=c.yo))
            pos[i] = (pos[i] + int(a['mov'])) % 360; res = dict(t=t, pos=pos[i], letra=None, mordio=False, dS=None)
            if pos[i] in objs and a['muerde']:
                k = objs[pos[i]]; dS = {'A': (0.3, 0.0), 'B': (-0.3, 0.0), 'C': (0.0, 0.3), 'D': (0.0, -0.3)}[k]
                E[i] = min(E[i] + dS[0], 1.5); A[i] = min(A[i] + dS[1], 1.5); res.update(letra=k, mordio=True, dS=dS)
                del objs[pos[i]]; objs[int(rng.integers(360))] = 'ABCD'[int(rng.integers(4))]
            c.resultado(res); traza.append((t, i, int(a['mov']), bool(a['muerde']), res['letra']))
            E[i] -= 0.002; A[i] -= 0.002
            if E[i] < 0.3 or A[i] < 0.3: E[i] = A[i] = 1.0   # 'muere' y renace con la memoria del parto
            c.fin_paso(dict(t=t, olvido=()))
            if t % 50 == 49:
                m = c.al_parir(dict(t=t, k=t)); c.muere(dict(t=t, causa='x', causa_juez='x', edad=1, hijos=0)); c.nace(dict(t=t, k=t, fundador=False, memoria=m, rng_hijo=None))
    sal = [c.salida() for c in cars]
    if es_gen: tel = {i: dict(v) for i, v in mod._TEL.items()}; R._quita(mod)
    else: tel = None
    return traza, sal, tel


def main():
    print("PRE-ARNES UNITARIO (sin pista)")
    o1 = carga(os.path.join(RAIZ, 'experimentos', 'carrera_escuderias', 'carros', 'O1.py'), 'o1u')
    sl = carga(os.path.join(RAIZ, 'experimentos', 'carrera_escuderias', 'carros', 'CTRL_O1_SINLIMPIA.py'), 'slu')
    g = carga(R.CARROS['O1_MURO_GEN'], 'genu'); g0 = carga(R.CARROS['O1_MURO_GEN0'], 'gen0u')
    D = dict(zip(CB.GENES, CB.FABRICA)); B = dict(zip(CB.GENES, CB.BASE))
    to, so, _ = episodio(o1); ts, ss, _ = episodio(sl)
    t0, s0, _ = episodio(g0); ok((t0, s0) == (to, so), "GEN0 == O1 (traza de 9 x 400 pasos y salida(), mundo de mentira)")
    t1, s1, tel = episodio(g, siembra=[dict(D)]); ok((t1, s1) == (to, so), "GEN fabrica sigma 0 == O1 (traza y salida)")
    ok(all(q[0] == 1 for v in tel.values() for q in v['fund']) and all(v.get('partos', 0) == 8 for v in tel.values()), f"telemetria: fundadores de siembra, 8 partos por linaje ({[v.get('partos') for v in tel.values()]})")
    t2, s2, _ = episodio(g, siembra=[dict(D, LIMPIA=0.0)]); ok((t2, s2) == (ts, ss), "GEN LIMPIA 0 == CTRL_O1_SINLIMPIA (traza y salida)")
    ok((ts, ss) != (to, so), "control: SINLIMPIA != O1 en el mundo de mentira")
    t3, s3, tel3 = episodio(g, siembra=None, lee=0, sigma=CB.SIGMA); ok((t3, s3) == (to, so), "NEUTRO (PS_LEE 0, sigma 0.03, desde la base) == O1")
    gs = {tuple(q[1]) for v in tel3.values() for q in v['fund']}; ok(len(gs) >= 1 and all(q[2] == 1 for v in tel3.values() for q in v['fund']), f"neutro: {len(gs)} genomas de fundador distintos, profundidad 1 (sin refundacion en el mundo de mentira)")
    t4, s4, tel4 = episodio(g, por_linaje=[list(CB.FABRICA)] * 9); ok((t4, s4) == (to, so) and all(q[0] == 3 for v in tel4.values() for q in v['fund']), "PS_POR_LINAJE 9 x fabrica == O1; origen 3")
    t5, s5, _ = episodio(g, por_linaje=[list(CB.FABRICA)] * 8 + [[0.25, 0.5, 0.35, 0.2, 0.0, 1.0]]); ok((t5, s5) != (to, so), "PS_POR_LINAJE con un LIMPIA 0 != O1")
    for gname, val in (('MARGEN', 0.0), ('PISO', 1.0), ('PEN_OTRO', 1.0), ('PRUEBA', 0.0), ('HUECO', 0.0)):
        t6, s6, _ = episodio(g, siembra=[dict(D, **{gname: val})]); ok((t6, s6) != (to, so), f"{gname} = {val} actua (!= O1 en el mundo de mentira)")
    # el hijo hereda y muta (sigma > 0, lee 1): la traza difiere de O1 y los genes de los vivos cambian
    t7, s7, tel7 = episodio(g, siembra=[dict(D)], sigma=CB.SIGMA)
    ok(tel7 and any(v.get('partos') for v in tel7.values()), "con sigma 0.03 el parto lleva '_gen' y nace() lo toma (no revienta en el bucle de memoria de O1)")
    # fila() y lee_mapa() sobre un crudo EXISTENTE del brazo o1 (tronco_v14_3): mismo formato que CV.tarea
    cr = sorted(glob.glob(os.path.join(RAIZ, 'experimentos', 'tronco_v14_3', 'datos', 'v143_*_o1.json')))
    if cr:
        d = json.load(open(cr[-1], encoding='utf-8')); x = dict(d['corridas'][0]); x['tel_ps'] = {}; x['estado'] = {}
        f = R.fila(x, d['meta']['T']); ok(0 <= f['cruzan'] <= 9 and f['R0_med'] is not None and len(f['por_linaje']) == 9 and f['coherente'],
                                          f"fila() sobre crudo existente (o1, s {x['seed']}): cruzan {f['cruzan']}/9 R0 {f['R0_med']} fund med {f['fund_med']} estab {f['establecidos']} vida {f['vida_med']} B+D {f['mord_BD']}")
        with tempfile.TemporaryDirectory() as td:
            for e in ('fab', 'MARGEN=0.1', 'mix:8xPISO=0.2+1xPISO=0.6'):
                y = dict(tipo='fijo', etq=e, genoma=None, genomas_linaje=None, aborto=None, T=d['meta']['T'], **f)
                json.dump(y, open(os.path.join(td, f"fijo_{e.replace(':', '-').replace('=', '')}_s{x['seed']}_T{d['meta']['T']}.json"), 'w', encoding='utf-8'))
            Rm = R.lee_mapa(td, log=lambda s: None); ok(set(Rm) == {'fab', 'MARGEN=0.1', 'mix:8xPISO=0.2+1xPISO=0.6'}, "lee_mapa() lee y ordena los JSON del mapa (carpeta temporal)")
    else:
        print("  (sin crudo o1 de tronco_v14_3: fila() no probada)")
    # la letra del Paso 2 con GEN_LETRA en memoria
    R.GEN_LETRA = 'MARGEN'
    for nombre, c, esp in R.casos_sinteticos():
        v = R.lee_serie(*c)['veredicto']; ok(v == esp, f"letra sintetica (GEN_LETRA en memoria): {nombre} -> {v} (esperado {esp})")
    R.GEN_LETRA = None
    print(f"\nPRE-ARNES {'PASA' if all(OK) else 'FALLA'}, {sum(OK)}/{len(OK)}")
    return 0 if all(OK) else 1


if __name__ == '__main__':
    sys.exit(main())
