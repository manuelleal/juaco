"""identidad_familia.py — ARNES DE IDENTIDAD de la subida del nivel 10 (familias vivas). Un proceso, sin Pool.

MISION: llegar a la AGI por este camino.

(0) ORIGEN: FABRICA.py, pista2.py, motor_convive.py y corre_convive.py tienen el sha fijado; los cuatro carros FAMILIA_* son
    exactamente la construccion por anclas (se reconstruyen en memoria y se comparan byte a byte).
(I) PERILLA APAGADA: FAMILIA_NADA == FABRICA BIT A BIT en TODA la salida de pista2.run (fisica + d['carro'] + rng final
    implicito en la fisica), en la pista v2 (solapadas=1) con quimiostato y con reposicion inmediata, y en la pista v1
    (solapadas=0, diag=1), semillas de practica.
(P) ANTES DEL PRIMER PARTO los cuatro modos son identicos en la fisica (T < ventana de reproduccion: nadie pare; misma
    etiqueta 'FAMILIA' para los cuatro: la etiqueta es un nombre que la pista copia a la salida, no fisica).
(B) EL CANAL, por unidad (instancias del carro con el ctx de la pista):
    B1 al_parir de PARTO devuelve lo heredado + las ultimas NODO_K mordidas; NADA devuelve None.
    B2 BAR conserva patrones, necesidades y la multiset de R (marginales) y NO consume ningun rng: el hijo BAR y el hijo
       PARTO con el mismo rng_hijo tienen los mismos pesos iniciales (Wl, KW) y el rng_hijo queda en el mismo estado.
    B3 ORACULO recibe la tabla verdadera: A/n0 +1, B/n0 -3, C/n1 +1, D/n1 -3, el resto 0 (NODO_LEE copias).
    B4 la lectura del hijo cambia su via lenta (Wps/Wns) en PARTO y no en NADA.
(D) DETERMINISMO: PARTO dos veces == PARTO.
(C) EN MARCHA (v2, T corto con partos): hay partos y, con partos, la fisica de PARTO se separa de la de NADA.
"""
import hashlib, importlib.util, json, os, sys, time
import numpy as np

sys.stdout.reconfigure(encoding='utf-8', errors='replace')
AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
GEN = os.path.join(RAIZ, 'experimentos', 'generaciones')
sys.path.insert(0, GEN); sys.path.insert(0, AQUI)
import construye_familia as CF
import pista2 as P2

SHAS = {os.path.join(RAIZ, 'experimentos', 'carrera_escuderias', 'carros', 'FABRICA.py'): '2ebee3e99ea5a33a',
        os.path.join(GEN, 'pista2.py'): '4d2bee16e7961261',
        os.path.join(GEN, 'motor_convive.py'): 'd10cb9021f5d0f41',
        os.path.join(GEN, 'corre_convive.py'): 'e6dadfdad9c379cd'}
PRACTICA = (12391, 12392, 12393)
OK = []; MAL = []


def h16(p): return hashlib.sha256(open(p, 'rb').read()).hexdigest()[:16]


def carga(et):
    p = os.path.join(AQUI, 'carros', f'FAMILIA_{et}.py')
    spec = importlib.util.spec_from_file_location(f'carro_FAMILIA_{et}', p)
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m


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


def fisica(r):
    return [{k: v for k, v in d.items() if k != 'carro'} for d in r['linajes']], r['pista']


def chk(nombre, cond, detalle=''):
    (OK if cond else MAL).append(nombre)
    print(f"  {'OK ' if cond else 'MAL'} {nombre} {detalle}", flush=True)


def ctx_prueba(i=0, k=1, seed=12391):
    cf = P2.cfg_fabrica(); kw = cf['kw']
    return dict(id=f'X/{k}', indice=i, n_linajes=9, T=100000, L=cf['L'] * 9, PAT={a: v.copy() for a, v in cf['PAT'].items()},
                rng=np.random.default_rng([seed, i, 12, k]), dote=kw['dote'], rep_umbral=kw['rep_umbral'], costo=kw['costo'],
                costo_a=kw['costo_a'], rep_X=kw['rep_X'], cupo=P2.CUPO, ancho=P2.ANCHO, fabrica=P2.cfg_fabrica())


def main():
    t0 = time.time()
    print("(0) origen y construccion", flush=True)
    for p, s in SHAS.items(): chk(f"sha {os.path.basename(p)}", h16(p) == s, f"{h16(p)} (esperado {s})")
    src = open(CF.ORIGEN, encoding='utf-8').read()
    for et, modo in CF.MODOS.items():
        s = src
        for a, b in CF.ANCLAS: s = s.replace(a, b.replace('{ET}', et).replace('{SHA}', CF.SHA_ORIGEN).replace('{MODO!r}', repr(modo)))
        p = os.path.join(AQUI, 'carros', f'FAMILIA_{et}.py')
        chk(f"FAMILIA_{et}.py == construccion por anclas", open(p, encoding='utf-8').read() == s, h16(p))
    M = {et: carga(et) for et in CF.MODOS}
    FAB = P2.carga_carro('FABRICA')

    print("(I) perilla apagada: FAMILIA_NADA == FABRICA en toda la salida", flush=True)
    casos = [(PRACTICA[0], 6000, dict(solapadas=1, diag=0, reposicion='fija')),
             (PRACTICA[1], 6000, dict(solapadas=1, diag=0, reposicion='fija')),
             (PRACTICA[2], 4000, dict(solapadas=1, diag=0, reposicion='inmediata')),
             (PRACTICA[0], 4000, dict(solapadas=0, diag=1)),
             (PRACTICA[1], 3000, dict(solapadas=0, diag=1, compat=0, fundador_limpio=1))]
    for seed, T, kw in casos:
        a = P2.run(seed, [('FABRICA', FAB)] * 9, T=T, **kw)
        b = P2.run(seed, [('FABRICA', M['NADA'])] * 9, T=T, **kw)
        ha, hb = huella(a), huella(b)
        nac = sum(d.get('nacimientos', 0) for d in a['linajes'])
        chk(f"I s{seed} T{T} {kw}", ha == hb, f"{ha} {hb} nacimientos {nac}")
    # mono de 1 cuerpo, v1 compat=1: el ancla del monolito (la pista + FABRICA == organismo_f9c REL)
    a = P2.run(PRACTICA[0], [('FABRICA', FAB)], T=5000, compat=1, pizarra=0)
    b = P2.run(PRACTICA[0], [('FABRICA', M['NADA'])], T=5000, compat=1, pizarra=0)
    chk("I v1 compat=1 (1 carro)", huella(a) == huella(b), f"{huella(a)} {huella(b)}")

    print("(P) antes del primer parto los cuatro modos son identicos en la fisica", flush=True)
    hs = {}
    for et in CF.MODOS:
        r = P2.run(PRACTICA[2], [('FAMILIA', M[et])] * 9, T=450, solapadas=1, diag=0, reposicion='fija')
        hs[et] = huella(fisica(r)); nac = sum(d['nacimientos'] for d in r['linajes'])
    chk("P fisica NADA==PARTO==BAR==ORACULO (T=450, 0 partos)", len(set(hs.values())) == 1 and nac == 0, str(hs))

    print("(B) el canal, por unidad", flush=True)
    padre = M['PARTO'].crea(ctx_prueba())
    padre._nodo = [[[1.0, 0, 0, 0, 1, 0], -3.0, 0], [[0, 1.0, 0, 1, 0, 0], 1.0, 1]]
    padre._mordh = [[t, 'ABCD'[t % 4], t % 2, [1.0, -3.0][t % 2]] for t in range(30)]
    msg = padre.al_parir(dict(t=1, k=1))
    exp_n = 2 + padre.NODO_K
    chk("B1 PARTO al_parir = heredado + ultimas NODO_K", len(msg) == exp_n and msg[0][1] == -3.0 and msg[2][1] == [1.0, -3.0][10 % 2], f"len {len(msg)}")
    chk("B1 NADA al_parir = None", M['NADA'].crea(ctx_prueba()).al_parir(dict(t=1, k=1)) is None)
    hijos = {}
    for et in ('NADA', 'PARTO', 'BAR', 'ORACULO'):
        h = M[et].crea(ctx_prueba(k=2)); rh = np.random.default_rng([12391, 0, 13, 2])
        h.nace(dict(t=1, k=2, fundador=False, memoria=[list(map(lambda z: [list(z[0]), z[1], z[2]], msg))][0], rng_hijo=rh, padre='X/1'))
        hijos[et] = (h, rh.bit_generator.state['state']['state'])
    hb, hp = hijos['BAR'][0], hijos['PARTO'][0]
    chk("B2 BAR conserva patrones y necesidades", [m[0] for m in hb._nodo] == [m[0] for m in hp._nodo] and [m[2] for m in hb._nodo] == [m[2] for m in hp._nodo])
    chk("B2 BAR conserva la multiset de R", sorted(m[1] for m in hb._nodo) == sorted(m[1] for m in hp._nodo))
    chk("B2 BAR destruye la asociacion (alguna R cambia de sitio)", [m[1] for m in hb._nodo] != [m[1] for m in hp._nodo])
    chk("B2 BAR no consume rng: mismos Wl/KW y mismo estado de rng_hijo que PARTO",
        np.array_equal(hb.Wl, hp.Wl) and np.array_equal(hb.KW, hp.KW) and hijos['BAR'][1] == hijos['PARTO'][1] == hijos['NADA'][1])
    ho = hijos['ORACULO'][0]; PAT = ho.PAT
    tabla = {(k, n): r for p, r, n in ho._nodo[:8] for k in 'ABCD' if list(PAT[k]) == p}
    chk("B3 ORACULO = tabla verdadera x NODO_LEE", tabla == {('A', 0): 1.0, ('B', 0): -3.0, ('C', 0): 0.0, ('D', 0): 0.0,
                                                          ('A', 1): 0.0, ('B', 1): 0.0, ('C', 1): 1.0, ('D', 1): -3.0}
        and len(ho._nodo) == 8 * ho.NODO_LEE, f"{tabla}")
    hn = hijos['NADA'][0]
    chk("B4 la lectura cambia la via lenta en PARTO y no en NADA", (np.abs(hp.Wps).sum() + np.abs(hp.Wns).sum()) > 0 and
        (np.abs(hn.Wps).sum() + np.abs(hn.Wns).sum()) == 0 and hn._nodo == [])

    print("(D)/(C) determinismo y canal en marcha (v2, T=8000)", flush=True)
    r1 = P2.run(PRACTICA[0], [('FAMILIA_PARTO', M['PARTO'])] * 9, T=8000, solapadas=1, diag=0, reposicion='fija')
    r2 = P2.run(PRACTICA[0], [('FAMILIA_PARTO', M['PARTO'])] * 9, T=8000, solapadas=1, diag=0, reposicion='fija')
    chk("D PARTO determinista", huella(r1) == huella(r2), huella(r1))
    nac = sum(d['nacimientos'] for d in r1['linajes'])
    rec = [d['carro'].get('n10', {}).get('recibido') for d in r1['linajes']]
    chk("C hubo partos en la prueba", nac > 0, f"nacimientos {nac}")
    rN = P2.run(PRACTICA[0], [('FAMILIA_NADA', M['NADA'])] * 9, T=8000, solapadas=1, diag=0, reposicion='fija')
    chk("C con partos, PARTO se separa de NADA en la fisica", huella(fisica(r1)) != huella(fisica(rN)))
    print(f"  (telemetria: n10.recibido del ultimo cuerpo registrado por linaje: {rec})")
    print(f"RESULTADO: {len(OK)}/{len(OK) + len(MAL)}  ({time.time() - t0:.0f} s)" + (f"  FALLAN: {MAL}" if MAL else ''))
    return 0 if not MAL else 1


if __name__ == '__main__':
    sys.exit(main())
