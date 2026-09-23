"""identidad_n9c.py — ARNES DE IDENTIDAD de subida_n9c (nivel 9, tanda 3). Un proceso, sin Pool. Se corre ANTES de mirar
cualquier numero; la ultima linea es "RESULTADO: N/N".

MISION: llegar a la AGI por este camino.

(0) ORIGEN Y CONSTRUCCION: shas fijados de FABRICA.py, pista2.py, motor_convive.py, corre_convive.py y de la fuente de la
    calibracion; los cuatro carros N9C_* (v2) son exactamente la construccion por anclas; chequeo estatico (revisa_carro).
(I) PERILLAS APAGADAS: N9C_NADA == FABRICA BIT A BIT en TODA la salida de pista2.run (v2 quimiostato x2, v2 inmediata,
    v1 9 carros diag=1, v1 fundador_limpio, v1 compat=1 con 1 carro).
(P) ANTES DEL PRIMER PARTO (T=450): la herencia es inerte: fisica PRED == CAND == CRUZ.
(B) EL CANAL (unidad): al_parir de NADA/PRED = None; CAND/CRUZ entregan COPIA de la memoria de efectos; el hijo CAND queda
    con la memoria del padre; el hijo CRUZ con dE y dAg intercambiados (mismos conteos); el hijo PRED/NADA nace sin memoria;
    ningun modo consume rng extra (mismo estado de rng_hijo); la copia no comparte memoria con el padre.
(M) LA BOCA (unidad, mismo uniforme): letra nunca mordida -> 'predice' decide igual que FABRICA; con E = 0.6 y la memoria
    'B quita 0.4 de comida', FABRICA (en blanco) muerde B y 'predice' no; con la comida en 1.5 (B no sube el deficit) las
    dos muerden igual (limpiar sin pagar); resultado() suma lo sentido a la memoria; el rng queda en el mismo estado.
(D) DETERMINISMO: CAND dos veces == CAND.
(C) EN MARCHA (v2, T=8000): hay partos en CAND; CAND se separa de PRED (la herencia no es inerte) y CRUZ de CAND (el
    contenido no es inerte); PRED se separa de NADA.
(E) REGLA 14: la entrada a pista2.run de corre_n9c.tarea es campo a campo la de corre_convive.tarea (semilla, 9 carros, kwargs).
(G) ERR-115: el parser aborta ante bandera desconocida, abreviada, con '=', repetida, -h/--help, semillas fuera del
    preregistro, --pool en el humo, humo de mas de 6 corridas o 200 000 pasos, serie con T distinto (sin correr nada);
    y el runner real con --help sale con error sin escribir archivos.
(V) LA LETRA: veredicto() da FUNCIONA / MODESTO / NO / NO SE LEE en casos fabricados.
"""
import hashlib, importlib.util, json, os, subprocess, sys, time
import numpy as np

sys.stdout.reconfigure(encoding='utf-8', errors='replace')
AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
GEN = os.path.join(RAIZ, 'experimentos', 'generaciones')
sys.path.insert(0, GEN); sys.path.insert(0, AQUI)
import construye_n9c as CN   # noqa: E402
import calibra_ancla as CA   # noqa: E402
import pista2 as P2          # noqa: E402
import corre_convive as JV   # noqa: E402
import corre_n9c as RN       # noqa: E402

SHAS = {CN.ORIGEN: CN.SHA_ORIGEN, os.path.join(GEN, 'pista2.py'): '4d2bee16e7961261',
        os.path.join(GEN, 'motor_convive.py'): 'd10cb9021f5d0f41', os.path.join(GEN, 'corre_convive.py'): 'e6dadfdad9c379cd',
        CA.FUENTE: CA.SHA_FUENTE}
PRACTICA = (14191, 14193, 14194)   # el humo v2 usa 14192 (no se comparte con el arnes)
OK = []; MAL = []


def h16(p): return hashlib.sha256(open(p, 'rb').read()).hexdigest()[:16]


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


def ctx_prueba(i=0, k=1, seed=14191):
    cf = P2.cfg_fabrica(); kw = cf['kw']
    return dict(id=f'X/{k}', indice=i, n_linajes=9, T=100000, L=cf['L'] * 9, PAT={a: v.copy() for a, v in cf['PAT'].items()},
                rng=np.random.default_rng([seed, i, 12, k]), dote=kw['dote'], rep_umbral=kw['rep_umbral'], costo=kw['costo'],
                costo_a=kw['costo_a'], rep_X=kw['rep_X'], cupo=P2.CUPO, ancho=P2.ANCHO, fabrica=P2.cfg_fabrica())


def main():
    t0 = time.time()
    print("(0) origen, construccion y chequeo estatico", flush=True)
    for p, s in SHAS.items(): chk(f"sha {os.path.basename(p)}", h16(p) == s, f"{h16(p)} (esperado {s})")
    rc_spec = importlib.util.spec_from_file_location('revisa_carro', os.path.join(RAIZ, 'experimentos', 'carrera_escuderias', 'revisa_carro.py'))
    RC = importlib.util.module_from_spec(rc_spec); rc_spec.loader.exec_module(RC)
    for et in CN.CARROS:
        p = os.path.join(AQUI, 'carros', f'N9C_{et}.py'); src = open(p, encoding='utf-8').read()
        chk(f"N9C_{et}.py == construccion por anclas y sha del runner", src == CN.fuente(et) and RN.SHAS[p] == h16(p), h16(p))
        v = RC.revisa_fuente(src, f'N9C_{et}'); chk(f"N9C_{et}.py pasa revisa_carro", not v, str(v[:2]))
    M = {et: RN.carga(et) for et in CN.CARROS}
    FAB = P2.carga_carro('FABRICA')

    print("(I) perillas apagadas: N9C_NADA == FABRICA en toda la salida", flush=True)
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

    print("(P) antes del primer parto la herencia es inerte", flush=True)
    hs = {}; nacs = 0
    for et in CN.CARROS:
        r = P2.run(PRACTICA[2], [('N9C', M[et])] * 9, T=450, solapadas=1, diag=0, reposicion='fija')
        hs[et] = huella(fisica(r)); nacs += sum(d['nacimientos'] for d in r['linajes'])
    chk("P fisica PRED == CAND == CRUZ (T=450, 0 partos)", hs['PRED'] == hs['CAND'] == hs['CRUZ'] and nacs == 0, f"{hs}")

    print("(B) el canal, por unidad", flush=True)
    MEM = {'A': [1.6, 0.0, 2], 'B': [-0.8, 0.0, 2], 'D': [0.0, -0.4, 1]}
    for et in ('NADA', 'PRED'):
        chk(f"B1 {et} al_parir = None", M[et].crea(ctx_prueba()).al_parir(dict(t=1, k=1)) is None)
    hijos = {}
    for et in CN.CARROS:
        p2 = M[et].crea(ctx_prueba())
        for k_, v_ in MEM.items(): p2._fm[k_] = list(v_)
        msg = p2.al_parir(dict(t=1, k=1))
        h = M[et].crea(ctx_prueba(k=2)); rh = np.random.default_rng([14191, 0, 13, 2])
        h.nace(dict(t=1, k=2, fundador=False, memoria=msg, rng_hijo=rh, padre='X/1'))
        hijos[et] = (h, rh.bit_generator.state['state']['state'], msg, p2)
    chk("B2 el hijo CAND queda con la memoria del padre", hijos['CAND'][0]._fm == MEM, str(hijos['CAND'][0]._fm))
    chk("B3 CRUZ: dE y dAg intercambiados, mismos conteos",
        hijos['CRUZ'][0]._fm == {k_: [v_[1], v_[0], v_[2]] for k_, v_ in MEM.items()}, str(hijos['CRUZ'][0]._fm))
    chk("B4 los hijos NADA y PRED nacen sin memoria", hijos['NADA'][0]._fm == {} and hijos['PRED'][0]._fm == {})
    chk("B4 ningun modo consume rng extra (mismo estado de rng_hijo)", len({v[1] for v in hijos.values()}) == 1)
    chk("B4 el hijo nace con los pesos de FABRICA (en blanco) en los cuatro modos",
        all(float(np.abs(v[0].Wp).sum() + np.abs(v[0].Wps).sum()) == 0.0 for v in hijos.values()))
    hc = hijos['CAND'][0]; hc._fm['A'][0] += 5.0
    chk("B5 la copia no comparte memoria con el padre", hijos['CAND'][3]._fm['A'][0] == 1.6)

    print("(M) la boca, por unidad (mismo uniforme)", flush=True)

    def boca(et, E, Ag, mem):
        c = M[et].crea(ctx_prueba(k=5))
        for k_, v_ in mem.items(): c._fm[k_] = list(v_)
        objs = {x: 'B' for x in (99, 100, 101)}      # se mueva a donde se mueva, cae sobre B
        a = c.actua(dict(t=5, pos=100, E=E, Ag=Ag, objs=objs, cuerpos=(), pizarra=(), yo='X/5'))
        return a['muerde'], c.rng.bit_generator.state['state']['state']
    MB = {'B': [-0.4, 0.0, 1]}
    fn, rn = boca('NADA', 0.6, 0.4, {}); fd, rd = boca('PRED', 0.6, 0.4, {})
    chk("M1 letra nunca mordida: 'predice' == FABRICA (misma decision, mismo rng)", fn == fd and rn == rd, f"{fn} {fd}")
    fn, rn = boca('NADA', 0.6, 0.4, MB); fd, rd = boca('PRED', 0.6, 0.4, MB)
    chk("M2 E = 0.6 y memoria 'B quita comida': FABRICA muerde B, 'predice' no (mismo rng)", fn is True and fd is False and rn == rd, f"{fn} {fd}")
    fn, rn = boca('NADA', 1.5, 0.5, MB); fd, rd = boca('PRED', 1.5, 0.5, MB)
    chk("M3 E = 1.5 (B no sube el deficit): las dos muerden igual (limpiar sin pagar)", fn == fd and fd is True and rn == rd, f"{fn} {fd}")
    c = M['PRED'].crea(ctx_prueba(k=6)); objs = {x: 'B' for x in (99, 100, 101)}
    c.actua(dict(t=5, pos=100, E=1.5, Ag=0.5, objs=objs, cuerpos=(), pizarra=(), yo='X/6'))
    c.resultado(dict(t=5, pos=c._enc[0], letra='B', mordio=True, dS=(-0.4, 0.0)))
    chk("M4 resultado() suma lo sentido a la memoria (PRED) y NADA no la usa", c._fm == {'B': [-0.4, 0.0, 1]} and M['NADA'].crea(ctx_prueba())._fm == {}, str(c._fm))

    print("(D)/(C) determinismo y en marcha (v2, T=8000)", flush=True)
    kw8 = dict(solapadas=1, diag=0, reposicion='fija')
    r1 = P2.run(PRACTICA[0], [('N9C_CAND', M['CAND'])] * 9, T=8000, **kw8)
    r2 = P2.run(PRACTICA[0], [('N9C_CAND', M['CAND'])] * 9, T=8000, **kw8)
    chk("D CAND determinista", huella(r1) == huella(r2), huella(r1))
    nac = sum(d['nacimientos'] for d in r1['linajes'])
    chk("C hubo partos en CAND", nac > 0, f"nacimientos {nac}")
    rB = P2.run(PRACTICA[0], [('N9C_CAND', M['PRED'])] * 9, T=8000, **kw8)
    rX = P2.run(PRACTICA[0], [('N9C_CAND', M['CRUZ'])] * 9, T=8000, **kw8)
    rN = P2.run(PRACTICA[0], [('N9C_CAND', M['NADA'])] * 9, T=8000, **kw8)
    chk("C con partos, CAND se separa de PRED (herencia no inerte)", huella(fisica(r1)) != huella(fisica(rB)))
    chk("C con partos, CRUZ se separa de CAND (contenido no inerte)", huella(fisica(r1)) != huella(fisica(rX)))
    chk("C PRED se separa de NADA (boca no inerte)", huella(fisica(rB)) != huella(fisica(rN)))

    print("(E) regla 14: entrada campo a campo contra corre_convive.tarea", flush=True)
    cap = []

    class Corta(Exception):
        pass

    def espia(seed, carros, **kw):
        cap.append((seed, len(carros), dict(kw))); raise Corta()
    orig = P2.run; P2.run = espia
    try:
        for f, arg in ((JV.tarea, (14191, 'FABRICA', 100000, 'fija', JV.MC.TOPE_DEF, JV.MC.R_REP)), (RN.tarea, (14191, 'NADA', 100000))):
            try: f(arg)
            except Corta: pass
    finally:
        P2.run = orig
    ok14 = len(cap) == 2 and cap[0][0] == cap[1][0] and cap[0][1] == cap[1][1] == 9 and cap[0][2] == cap[1][2]
    chk("E entrada de corre_n9c == corre_convive (semilla, 9 carros, cada kwarg)", ok14, f"{cap}")

    print("(G) ERR-115: el parser aborta sin correr nada", flush=True)
    malas = [['--help'], ['-h'], ['--humo', '--help'], ['--ser', '--desde', '14101', '--n', '20', '--pool', '6'],
             ['--serie', '--desde=14101', '--n', '20', '--pool', '6'], ['--humo', '--humo'], ['--humo', '--x'],
             ['--serie', '--desde', '14141', '--n', '20', '--pool', '6'], ['--serie', '--desde', '14101', '--n', '19', '--pool', '6'],
             ['--serie', '--desde', '14101', '--n', '20', '--pool', '6', '--T', '50000'], ['--serie', '--desde', '14101', '--n', '20'],
             ['--humo', '--pool', '2'], ['--humo', '--desde', '14101'], ['--humo', '--n', '2'], ['--humo', '--T', '60000'],
             ['--humo', '--serie'], [], ['--veredicto', 'a.json'], ['--veredicto', 'a.json,b.json', '--n', '20'],
             ['--humo', '--brazos', 'CAND,OTRO']]
    todas = True
    for av in malas:
        try: RN.parsea(av); todas = False; print(f"    no aborto: {av}")
        except RN.BanderaMala: pass
    chk(f"G {len(malas)} formas malas abortan en parsea()", todas)
    buenas = [['--humo'], ['--humo', '--brazos', 'NADA,CAND', '--T', '20000'], ['--serie', '--desde', '14101', '--n', '20', '--pool', '6'],
              ['--serie', '--desde', '14121', '--n', '20', '--pool', '6'], ['--veredicto', 'a.json,b.json']]
    ok = True
    for av in buenas:
        try: RN.parsea(av)
        except RN.BanderaMala as e: ok = False; print(f"    aborto una buena: {av} {e}")
    chk(f"G {len(buenas)} formas validas se aceptan (solo se parsean; nada corre)", ok)
    antes = sorted(os.listdir(RN.DATOS)) + sorted(os.listdir(RN.HUMO)) if os.path.isdir(RN.HUMO) else []
    pr = subprocess.run([sys.executable, os.path.join(AQUI, 'corre_n9c.py'), '--help'], capture_output=True, text=True, timeout=120)
    despues = sorted(os.listdir(RN.DATOS)) + sorted(os.listdir(RN.HUMO)) if os.path.isdir(RN.HUMO) else []
    chk("G el runner real con --help sale con error y no escribe nada", pr.returncode != 0 and antes == despues and 'ABORTA' in (pr.stderr + pr.stdout),
        f"rc {pr.returncode}")

    print("(V) la letra de veredicto()", flush=True)
    def A_(nada=0.11, pn=0, pc=18, bq=0): return dict(NADA=dict(R0_nacidos=nada, persiste_estricto=pn), CAND=dict(persiste_estricto=pc, bloqueados=bq),
                                                   PRED=dict(persiste_estricto=0), CRUZ=dict(persiste_estricto=0))
    def P_(g2=18, g3=18): return [dict(par='CAND-PRED', clave='R0_nacidos', gana=g2), dict(par='CAND-CRUZ', clave='R0_nacidos', gana=g3)]
    casosV = [(A_(), P_(), 'FUNCIONA'), (A_(), P_(g3=10), 'HAY ALGO MODESTO: PERSISTE'), (A_(pc=5), P_(), 'HAY ALGO MODESTO: SUBE'),
              (A_(pc=5), P_(g2=10), 'NO ('), (A_(nada=0.2), P_(), 'NO SE LEE'), (A_(pn=3), P_(), 'NO SE LEE'), (A_(bq=4), P_(), 'NO SE LEE')]
    okv = all(RN.veredicto(a, p, 20)['VEREDICTO'].startswith(e) for a, p, e in casosV)
    chk(f"V {len(casosV)} casos fabricados dan la letra esperada", okv, str([RN.veredicto(a, p, 20)['VEREDICTO'][:22] for a, p, _ in casosV]))
    chk("V el ancla del runner es la de calibra_ancla.py", tuple(RN.ANCLA) == tuple(CA.calibra()['ancla']), f"{RN.ANCLA} {CA.calibra()['ancla']}")

    print(f"({time.time() - t0:.0f} s)")
    print(f"RESULTADO: {len(OK)}/{len(OK) + len(MAL)}" + (f"  FALLAN: {MAL}" if MAL else ''))
    return 0 if not MAL else 1


if __name__ == '__main__':
    if len(sys.argv) > 1: raise SystemExit(f"identidad_n9c: no acepta argumentos ({sys.argv[1:]})")
    sys.exit(main())
