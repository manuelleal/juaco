"""corre_o1_libre.py — RUNNER y LETRA de "O1 LIBRE CON PODERES" (o1_libre, 30-sep-2026; EXPLORATORIO con letra fija).
Preregistro: PREREGISTRO_o1_libre.md (la letra esta AQUI, en lee_serie(), y alli en la sec. 6).

MISION: llegar a la AGI por este camino (organismo minimo con reglas locales, sin retropropagacion, peldanos preregistrados con
controles y replicas). Pregunta: con O1 entero como genoma (14 genes: sus 10 constantes + 4 poderes que nacen en 0) en un mundo donde
cada poder puede pagar, y seleccion por HIJOS a 100k, ¿que poderes se prenden (contra la deriva), en que orden, y el linaje evolucionado
le gana a O1 de fabrica EN EL MISMO MUNDO?

QUE SE CORRE (mundo = pista_libre con estacion, parche y quieto; 9 linajes, L 360, 36 objetos, pizarra 1, fundador limpio):
  Por indice i (0..N_IND-1):
  CADENA lib: NPAS pasajes de T_PAS de O1_LIB (sigma 0.03, PS_LEE 1, PS_ESCRIBE 1). SIEMBRA del pasaje siguiente = N_SIEMBRA partos al
              azar de los partos con t >= T_PAS/2 (cada parto = [t, genes del PADRE]): LA MONEDA SON LOS HIJOS (quien pare mas pesa mas;
              los linajes que paren mas aportan mas). No ve R0, cruce ni nada del juez. Pasaje 0: SIEMBRA None (fabrica + mutacion).
  CADENA neu: LA MISMA cadena (mismas semillas) con PS_LEE 0: los genes se heredan, mutan, se anotan y se transfieren igual, pero ningun
              cuerpo los lee (decide como O1 de fabrica): deriva acumulada SIN seleccion sobre los genes (control que puede fallar: V6).
  PRUEBAS T_PRU (semilla de prueba de i, LA MISMA para las 6: numeros aleatorios comunes):
     lib  : 9 x O1_LIB con la siembra final de SU cadena lib (PS_LEE 1)       · neu : idem con la de SU cadena neu (PS_LEE 1)
     o1   : 9 x O1 de fabrica (la BASE)
     mix  : CONQUISTA: O1_LIB (siembra lib) en las casillas S_i y O1 de fabrica en las otras, en el MISMO mundo
     mixn : CONTROL de la conquista: idem con la siembra neu
     mixA : SOLO DESCRIPTIVO (auditoria H-5; NO entra en la letra): idem con la siembra lib y los 4 poderes puestos en 0 (vuelven a mutar
            desde 0 durante la prueba, como en el pasaje 0): separa "conquista por los poderes" de "conquista por las perillas de O1".
     S_i = casillas pares (0,2,4,6,8) si i es par; impares (1,3,5,7) si i es impar: 45 casillas de cada lado en 10 indices.
  Cada prueba de monocultivo ES corre_v143.tarea (se IMPORTA y no se toca), con pista.run -> pista_libre.run(mundo) SOLO durante la
  llamada; las mixtas usan tarea_lista(), copia de corre_v143.tarea que acepta una lista de carros (el arnes (h) la compara campo a
  campo con corre_v143.tarea: regla 14).
SEMILLAS NUEVAS (grep 30-sep: 734xxx no aparece en .py/.md de PROYECTOS/JUACO/o1libre):
  serie:   pasaje p de la cadena i -> 734000 + 10 i + p; prueba de i -> 734201 + i
  replica: pasaje p de la cadena i -> 734300 + 10 i + p; prueba de i -> 734501 + i
  practica: 734900-734999 (arnes 734950-734989; humo 734990-734998).
nube-9: trabajo() atrapa TODO y devuelve 'aborto'; JSON por trabajo y por pasaje ANTES de volver (ERR-54); --reanuda salta lo hecho:
  un JSON VALIDO nunca se re-corre; solo se reintentan los trabajos con 'aborto' (fallas del instrumento/maquina), y queda 'reintento_de'.

Uso (ERR-115: banderas desconocidas o abreviadas ABORTAN; --serie/--replica SOLO el coordinador, con el preregistro, este runner, el
constructor, el carro y el mundo COMMITEADOS y sin cambios respecto de HEAD):
  python experimentos/organelos/o1_libre/corre_o1_libre.py --humo              # 1 proceso: 2 cadenas x 2 pasajes de 12k + o1 y mix de 20k (6 corridas, 88 000 pasos)
  python experimentos/organelos/o1_libre/corre_o1_libre.py --humo --reanuda    # 2o proceso: lib, neu, mixn, mixA de 20k (4 corridas, 80 000 pasos) y lee
  python experimentos/organelos/o1_libre/corre_o1_libre.py --serie --pool 2
  python experimentos/organelos/o1_libre/corre_o1_libre.py --serie --pool 2 --reanuda
  python experimentos/organelos/o1_libre/corre_o1_libre.py --replica --pool 2  # solo por la regla de parada (sec. 7)
  python experimentos/organelos/o1_libre/corre_o1_libre.py --lee <carpeta>
  python experimentos/organelos/o1_libre/corre_o1_libre.py --bloque <resumen serie>.json,<resumen replica>.json
"""
import argparse, copy, glob, hashlib, importlib.util, json, math, os, platform, statistics as st, subprocess, sys, time
import numpy as np

try: sys.stdout.reconfigure(encoding='utf-8', errors='replace')
except Exception: pass
AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(AQUI)))
V143D = os.path.join(RAIZ, 'experimentos', 'tronco_v14_3')
PISTA = os.path.join(RAIZ, 'experimentos', 'carrera_escuderias')
for _d in (AQUI, V143D, PISTA):
    if _d not in sys.path: sys.path.insert(0, _d)
import corre_v143 as CV          # tarea (se IMPORTA, no se toca)
import construye_o1_lib as CB
import pista_libre as PL
P = CV.P; J = CV.J
if P is not PL.P: raise SystemExit("corre_o1_libre: pista importada dos veces (corre_v143 y pista_libre ven modulos distintos)")

PRERREGISTRO = 'PREREGISTRO_o1_libre.md'
DATOS = os.path.join(AQUI, 'datos')
LIB_PY = os.path.join(AQUI, 'carros', 'O1_LIB.py'); LIB0_PY = os.path.join(AQUI, 'carros', 'O1_LIB0.py')
SHAS = {os.path.join(V143D, 'corre_v143.py'): '24100621c450da22', os.path.join(PISTA, 'pista.py'): '9f47c65e438e0ff4',
        os.path.join(PISTA, 'juez.py'): '6a68f640a7832f12', os.path.join(PISTA, 'carros', 'O1.py'): '99436afa2715f028',
        os.path.join(AQUI, 'pista_libre.py'): None, os.path.join(AQUI, 'construye_o1_lib.py'): None, LIB_PY: None, LIB0_PY: None}
SHAS_PROPIOS = {'pista_libre.py': 'bf538326a74af8e4', 'construye_o1_lib.py': 'ec63375ee0b980d0', 'O1_LIB.py': 'ff30214f59ed36d8', 'O1_LIB0.py': '7dda8b7f8448b386'}
for _r in list(SHAS):
    if SHAS[_r] is None: SHAS[_r] = SHAS_PROPIOS[os.path.basename(_r)]
GENES = CB.GENES; PODERES = CB.PODERES; GENES_O1 = CB.GENES_O1; FABRICA = dict(zip(CB.GENES, CB.FABRICA))
SIGMA = 0.03
CADENAS = {'lib': 1, 'neu': 0}                      # PS_LEE de cada cadena
PRUEBAS = ('lib', 'neu', 'o1', 'mix', 'mixn')       # las de LA LETRA
DESCRIPTIVAS = ('mixA',)                            # auditoria H-5: se corren, se reportan, NO entran en la letra (ni en V1)
TODAS = PRUEBAS + DESCRIPTIVAS
SIEMBRA_DE = {'lib': 'lib', 'neu': 'neu', 'o1': None, 'mix': 'lib', 'mixn': 'neu', 'mixA': 'lib'}
MIXTAS = ('mix', 'mixn', 'mixA')
PODERES_A_CERO = ('mixA',)
BASES = {'serie': (734000, 734201), 'replica': (734300, 734501)}
N_IND = 10; NPAS = 3; T_PAS = 100000; T_PRU = 100000; N_SIEMBRA = 90; POOL_MAX = 2
HUMO = dict(base=(734990, 734998), n=1, npas=2, T_pas=12000, T_pru=20000)   # T_pas 12k: el primer pasaje ya ve escasez (empieza en t 10k)
MUNDO = dict(PL.MUNDO_LIBRE)
# ------------------------------------------------------------------ constantes de la LETRA (PREREGISTRO sec. 6), para n = 10 indices
GANA = 8               # PC, PN, PP: >= 8/10 (empates EN CONTRA)
DIF_PODER = 0.05       # PP: mediana(lib) - mediana(neu) del gen en la siembra final >= 0.05
O1_R0 = 0.50           # V2: mediana (por indice) del R0 real mediano de o1 >= 0.50 (el mundo es vivible para O1 de fabrica)


def h16(p): return hashlib.sha256(open(p, 'rb').read()).hexdigest()[:16]
def sem_pas(base, i, p): return base[0] + 10 * i + p
def sem_pru(base, i): return base[1] + i
def med(x):
    x = [v for v in x if v is not None]
    return round(float(st.median(x)), 4) if x else None
def esc(k, n): return math.ceil(k * n / 10 - 1e-9)   # umbral escalado (solo humo, que NO cuenta)
def casillas(i): return (0, 2, 4, 6, 8) if i % 2 == 0 else (1, 3, 5, 7)


# ------------------------------------------------------------------ carga de carros por proceso
def carga_lib():
    """Carga (una vez por proceso) O1_LIB verificando su sha y lo registra en corre_v143._MODS."""
    s = h16(LIB_PY)
    if s != SHAS[LIB_PY]: raise SystemExit(f"sha {LIB_PY} {s} != {SHAS[LIB_PY]}")
    m = CV._MODS.get('O1_LIB')
    if m is None or os.path.abspath(m.__file__) != os.path.abspath(LIB_PY):
        spec = importlib.util.spec_from_file_location("carro_O1_LIB", LIB_PY)
        m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); CV._MODS['O1_LIB'] = m
    if m.PASAJE != 1: raise SystemExit(f"O1_LIB: PASAJE {m.PASAJE} != 1")
    return m


def _pon_lib(m, seed, siembra, lee, escribe, sigma=SIGMA, coloniza=0):
    m.SIEMBRA = copy.deepcopy(siembra); m.PS_SEMILLA = int(seed); m.PS_SIGMA = float(sigma); m.PS_LEE = int(lee); m.PS_ESCRIBE = int(escribe)
    m.PS_COLONIZA = int(coloniza); m._TEL.clear(); m._PS_CNT.clear(); m._COL.clear()


def _apaga_lib(m):
    m.SIEMBRA = None; m.PS_SEMILLA = 0; m.PS_SIGMA = 0.03; m.PS_LEE = 1; m.PS_ESCRIBE = 0; m.PS_COLONIZA = 0; m._COL.clear()


def tarea_lista(seed, carros, T, mundo):
    """COPIA de corre_v143.tarea que acepta una LISTA de 9 (etiqueta, modulo) y el mundo de pista_libre (regla 14: el arnes (h) la compara
    campo a campo con corre_v143.tarea con 9 x O1 y el mundo viejo). Devuelve (salida con las claves de corre_v143.tarea, crudo)."""
    t0 = time.time()
    r = PL.run(seed, carros, T=T, pizarra=1, rep_acum=0, escala=1, mundo_n=None, fundador_limpio=CV.FL, **mundo)
    L = [J.resumen_linaje(d, seed) for d in r['linajes']]
    sd = sum(x['descendientes'] for x in L); sm = sum(x['muertes'] for x in L)
    for x in L:
        tf, qf, nr = J.t_fund_reconstruido(x['telem']['vidas'], x['telem']['desc_por_vida'])
        x['t_fund_rec_ok'] = bool(tf[:200] == x['telem']['t_fund'] and qf == x['cola_final'] and nr == x['nac_reales'])
    tel = [dict(v143=d['carro'].get('v143'), apr=(d['carro'].get('apr') or {}).get('politica'),
                apr_quit=(d['carro'].get('apr') or {}).get('quit_q'), apr_anad=(d['carro'].get('apr') or {}).get('anad_q'),
                apr_opp=(d['carro'].get('apr') or {}).get('opp_q'), apr_g0=[(d['carro'].get('apr') or {}).get('mord_g0'),
                                                                        (d['carro'].get('apr') or {}).get('opp_g0')]) for d in r['linajes']]
    return dict(seed=seed, seg=round(time.time() - t0, 1), linajes=L, pista=r['pista'],
                R0_pista=round(sd / (sm + len(L)), 4), pizarra_log=r['pizarra_log'], tel=tel), r


def tarea(seed, brazo, T, siembra=None, lee=1, mundo=None, sigma=SIGMA):
    """brazo 'lib'/'neu' (9 x O1_LIB), 'o1' (9 x O1): corre_v143.tarea tal cual con pista.run -> pista_libre.run(mundo) SOLO durante la
    llamada. 'mix'/'mixn': tarea_lista con O1_LIB en casillas(i) (i = seed - base de prueba, lo pasa el runner via brazo 'mix:i').
    Agrega 'tel' (copia de SOLO LECTURA de la telemetria de O1_LIB), 'libre' (contadores del mundo), 'estado' (perillas de ESTE proceso)."""
    mw = dict(MUNDO if mundo is None else mundo)
    b, _, ix = brazo.partition(':')
    est = dict(brazo=b, mundo=dict(mw))
    o1 = CV.modulo('O1')
    m = carga_lib() if b != 'o1' else None
    if m is not None:
        _pon_lib(m, seed, siembra, lee, 1, sigma, coloniza=1)
        est.update(carro='O1_LIB', sha=h16(LIB_PY), sigma=float(sigma), lee=int(lee), escribe=1, coloniza=1, siembra_n=len(siembra or []))
    else:
        est.update(carro='O1', sha=h16(os.path.join(PISTA, 'carros', 'O1.py')))
    try:
        if b in MIXTAS:
            cas = casillas(int(ix))
            carros = [('O1_LIB', m) if j in cas else ('O1', o1) for j in range(9)]
            x, r = tarea_lista(seed, carros, T, mw); est['casillas_lib'] = list(cas)
        else:
            cap = []; orig = P.run

            def run2(*a, **k):
                if k != dict(T=T, pizarra=1, rep_acum=0, escala=1, mundo_n=None, fundador_limpio=1) or len(a) != 2:
                    raise SystemExit(f"corre_o1_libre: corre_v143.tarea llamo a pista.run con {k}")
                r = PL.run(*a, **k, **mw); cap.append(r); return r
            P.run = run2
            try:
                x = CV.tarea((seed, 'O1_LIB' if m is not None else 'O1', T))
            finally:
                P.run = orig
            r = cap[0]
        x['tel'] = copy.deepcopy({str(i): v for i, v in m._TEL.items()}) if m is not None else None
    finally:
        if m is not None: _apaga_lib(m)
    x['libre'] = r['pista'].get('libre'); x['estado'] = est
    return x


def siembra(tel, T, seed, n=N_SIEMBRA):
    """LA MONEDA: SOLO los PARTOS. tel = {indice: {'partos': [[t, genes del padre], ...]}} -> n genomas {gen: valor} al azar sin reposicion
    (rng [seed, 7723]) de los partos con t >= T/2 (si no hay ninguno: de todos los partos; si no hay partos: None). No ve R0 ni cruce."""
    P2 = [(t, g, int(i)) for i in sorted(tel or {}, key=lambda z: int(z)) for t, g in (tel[i] or {}).get('partos', [])]
    tarde = [x for x in P2 if x[0] >= T // 2]
    fuente = tarde or P2
    if not fuente: return None, dict(partos=0, tarde=0, usados=0)
    rr = np.random.default_rng([int(seed), 7723])
    ix = sorted(int(j) for j in rr.choice(len(fuente), size=min(n, len(fuente)), replace=False))
    # DESCRIPTIVO (junta o1_evo): aportes por linaje (proporcionales a sus partos, sin cuotas), Ne por linaje = 1/sum p^2 y
    # padres distintos (genomas distintos entre los elegidos)
    por = {}
    for j in ix: por[fuente[j][2]] = por.get(fuente[j][2], 0) + 1
    ne = round(1.0 / sum((c / len(ix)) ** 2 for c in por.values()), 2)
    padres = len({tuple(fuente[j][1]) for j in ix})
    return [{k: float(v) for k, v in zip(GENES, fuente[j][1])} for j in ix], dict(partos=len(P2), tarde=len(tarde), usados=len(ix),
                                                                              por_linaje={str(k): v for k, v in sorted(por.items())},
                                                                              linajes=len(por), Ne_linajes=ne, padres_distintos=padres)


def genes_de(sie):
    if not sie: return None
    return {k: round(sum(s[k] for s in sie) / len(sie), 4) for k in GENES}


def fila(x, T, brazo, i=None):
    L = x['linajes']; tel = x.get('tel') or {}
    fp = [f for v in tel.values() for f in (v or {}).get('fund', [])]
    act = {k: sum(((v or {}).get('activaciones') or {}).get(k, 0) for v in tel.values()) for k in ('mem', 'pau', 'soc', 'res', 'escr')}
    b = brazo.partition(':')[0]
    grupo = None
    if b in MIXTAS:
        cas = casillas(i)
        g = lambda f, lado: [f(l) for j, l in enumerate(L) if (j in cas) == lado]
        # auditoria H-4: 'nac' = nacimientos reales (RECAMBIO: hijos que llegaron a nacer, la medida de la conquista); 'partos' =
        # descendientes (PARTOS: hijos puestos en la cola, nazcan o no); muertes y fundadores por lado, DESCRIPTIVOS
        lado = lambda es: dict(nac=g(lambda l: l['nac_reales'], es), partos=g(lambda l: l['descendientes'], es), muertes=g(lambda l: l['muertes'], es),
                               fund=g(lambda l: l['fundadores'], es), cruza=g(lambda l: int(l['cruza_real']), es), R0=g(lambda l: l['R0_real'], es))
        grupo = dict(casillas_lib=list(cas), lib=lado(True), o1=lado(False))
        grupo['conquista'] = round(st.mean(grupo['lib']['nac']) - st.mean(grupo['o1']['nac']), 4)
        grupo['dif_partos'] = round(st.mean(grupo['lib']['partos']) - st.mean(grupo['o1']['partos']), 4)
        grupo['dif_muertes'] = round(st.mean(grupo['lib']['muertes']) - st.mean(grupo['o1']['muertes']), 4)
        grupo['dif_fund'] = round(st.mean(grupo['lib']['fund']) - st.mean(grupo['o1']['fund']), 4)
    lb = x.get('libre') or {}
    pg = [g for v in tel.values() for _, g in (v or {}).get('partos', [])]
    return dict(seed=x['seed'], T=T, brazo=b, R0_real=[l['R0_real'] for l in L], R0_med=med([l['R0_real'] for l in L]),
                fund=[l['fundadores'] for l in L], fund_post10k=[l['fund_post10k'] for l in L], cruza=[int(l['cruza_real']) for l in L],
                cruzan=sum(int(l['cruza_real']) for l in L), mayoria=int(sum(int(l['cruza_real']) for l in L) * 2 > len(L)),
                nac_reales=[l['nac_reales'] for l in L], partos=[l['descendientes'] for l in L], muertes=[l['muertes'] for l in L],
                coherente=all(l.get('coherente', True) for l in L), t_fund_ok=all(l.get('t_fund_rec_ok', True) for l in L),
                fund_de_siembra=sum(f[0] == 1 for f in fp), fund_colonia=sum(f[0] == 2 for f in fp), fund_fabrica=sum(f[0] == 0 for f in fp), fund_n=len(fp), activaciones=act, partos_tel=len(pg),
                genes_partos=({k: round(sum(g[j] for g in pg) / len(pg), 4) for j, k in enumerate(GENES)} if pg else None),
                grupo=grupo, mundo_AC=round(x['pista']['comp_mundo']['A'] + x['pista']['comp_mundo']['C'], 4),
                libre=dict((k, lb.get(k)) for k in ('a_mala', 'a_buena', 'mudadas', 'sin_libre', 'nacidos', 'frac_escasez', 'quietos', 'frac_en_parche')),
                estado=x.get('estado'), seg=x.get('seg'))


def cadena(i, base, npas, T, carpeta, reanuda, brazo, log=None):
    """Cadena lib (PS_LEE 1) o neu (PS_LEE 0; misma herencia, mutacion, anotacion y transferencia). JSON por pasaje (reanudable)."""
    sie = None; F = []; lee = CADENAS[brazo]
    for p in range(npas):
        fin = os.path.join(carpeta, f"pasaje_i{i:02d}_{brazo}_p{p:02d}.json")
        if reanuda and os.path.exists(fin):
            with open(fin, encoding='utf-8') as fh: d = json.load(fh)
        else:
            s = sem_pas(base, i, p)
            x = tarea(s, brazo, T, siembra=sie, lee=lee)
            sig, info = siembra(x['tel'], T, s)
            f = fila(x, T, brazo); f['p'] = p; f['sembrado'] = int(sie is not None); f['genes_siembra'] = genes_de(sig); f['siembra_info'] = info
            d = dict(fila=f, siembra_sig=sig)
            tmp = fin + '.tmp'
            with open(tmp, 'w', encoding='utf-8') as fh: json.dump(d, fh, ensure_ascii=False)
            os.replace(tmp, fin)
        F.append(d['fila']); sie = d['siembra_sig']
        if log: log(f"    cadena i{i} {brazo} p{p} cruzan {d['fila']['cruzan']}/9 partos {d['fila']['siembra_info']}")
        if not sie:   # ERR-160 (v): 0 partos en TODO el pasaje (siembra() ya cae de t >= T/2 a todo el pasaje): la cadena se EXTINGUE (DATO)
            return dict(pasajes=F, siembra_final=None, extinto=True, p_extincion=p)
    return dict(pasajes=F, siembra_final=sie, extinto=False, p_extincion=None)


class _Listo(Exception):
    def __init__(self, x): super().__init__('listo'); self.x = x


def extinta(tipo, i, brazo, de, p_ext):
    """ERR-160 (v): prueba de una cadena EXTINTA (0 partos en un pasaje entero): no se corre; DATO, no aborto. En la letra: la conquista
    de esa mixta es -inf (el lado O1_LIB perdio: mixn -> 'perdida del neutro'; mix -> 'perdida de lib'); el monocultivo cruza 0."""
    return dict(tipo=tipo, i=i, brazo=brazo, aborto=None, extinto=True, cadena_extinta=de, p_extincion=p_ext, cruzan=0, mayoria=0, R0_med=0.0,
                nac_reales=[], partos=[], muertes=[], cruza=[], coherente=True, t_fund_ok=True, fund_n=0, fund_de_siembra=0, fund_colonia=0,
                fund_fabrica=0, activaciones=dict(mem=0, pau=0, soc=0, res=0, escr=0), partos_tel=0, grupo=None, mundo_AC=None, libre=None,
                estado=None, genes_siembra_usada=None)


def trabajo(args):
    """UN trabajo: ('cadena', i, 'lib'|'neu') o ('prueba', i, brazo). Atrapa TODO (nube-9); escribe su JSON antes de volver (ERR-54)."""
    tipo, i, brazo, base, npas, T_pas, T_pru, carpeta, reanuda = args
    fin = os.path.join(carpeta, f"{tipo}_i{i:02d}_{brazo}.json"); previo = None
    if reanuda and os.path.exists(fin):
        with open(fin, encoding='utf-8') as fh: x0 = json.load(fh)
        if not x0.get('aborto'): return x0
        previo = x0['aborto']
    t0 = time.time()
    try:
        if tipo == 'cadena':
            x = dict(tipo=tipo, i=i, brazo=brazo, aborto=None, **cadena(i, base, npas, T_pas, carpeta, reanuda, brazo))
        else:
            sie = None; de = SIEMBRA_DE[brazo]
            if de is not None:
                with open(os.path.join(carpeta, f"cadena_i{i:02d}_{de}.json"), encoding='utf-8') as fh: c = json.load(fh)
                if c.get('aborto'): raise RuntimeError("cadena abortada")
                if c.get('extinto'):   # ERR-160 (v): la prueba NO se corre; queda un JSON de DATO "extinto" (no es aborto)
                    x = extinta(tipo, i, brazo, de, c.get('p_extincion'))
                    raise _Listo(x)
                if not c.get('siembra_final'): raise RuntimeError("cadena sin siembra final")
                sie = c['siembra_final']
                if brazo in PODERES_A_CERO: sie = [dict(e, **{k: 0.0 for k in PODERES}) for e in sie]   # mixA: siembra lib con poderes en 0
            b = f"{brazo}:{i}" if brazo in MIXTAS else brazo
            y = tarea(sem_pru(base, i), b, T_pru, siembra=sie, lee=1)   # en la PRUEBA los genes se leen siempre
            fy = fila(y, T_pru, b, i); fy.pop("brazo")   # humo 16:31: la clave brazo de fila() chocaba con la de trabajo()
            x = dict(tipo=tipo, i=i, brazo=brazo, aborto=None, genes_siembra_usada=genes_de(sie), **fy)
    except _Listo as z:
        x = z.x
    except BaseException as e:   # noqa: nube-9
        x = dict(tipo=tipo, i=i, brazo=brazo, aborto=f"{type(e).__name__}: {e}"[:300])
    if previo: x['reintento_de'] = previo
    x['seg'] = round(time.time() - t0, 1)
    tmp = fin + '.tmp'
    with open(tmp, 'w', encoding='utf-8') as fh: json.dump(x, fh, ensure_ascii=False)
    os.replace(tmp, fin)
    return x


# ------------------------------------------------------------------ LA LETRA (PREREGISTRO_o1_libre.md sec. 6)
def lee_serie(C, R, n, abortos, npas=NPAS):
    """C[brazo][i] = cadena (lib, neu); R[brazo][i] = prueba. n = indices esperados (10 en serie/replica).
    ERR-160 (v): una cadena EXTINTA (0 partos en un pasaje entero) es un DATO: sus pruebas son JSON 'extinto' (no se corren, no son abortos).
    En la letra: conquista de esa mixta = -inf (pierde el lado O1_LIB); en PP ese indice NO cuenta a favor de lib (lib > neu solo se cuenta
    con las dos cadenas vivas; medianas sobre las cadenas vivas de cada brazo). Validez: solo sobre las corridas que existen."""
    INF = float('-inf'); I = list(range(n)); g8 = esc(GANA, n)
    viva = lambda x: not x.get('extinto')
    completo = all(len(C.get(b, {})) == n for b in CADENAS) and all(len(R.get(b, {})) == n for b in PRUEBAS) \
        and all(C[b][i].get('extinto') or len(C[b][i]['pasajes']) == npas for b in CADENAS for i in C.get(b, {}))
    RV = {b: {i: R[b][i] for i in R.get(b, {}) if viva(R[b][i])} for b in TODAS}
    v = {}
    v['V1_completa'] = bool(abortos == 0 and completo and all(RV[b][i]['coherente'] and RV[b][i]['t_fund_ok'] for b in PRUEBAS for i in RV[b]))
    m = med([R['o1'][i]['R0_med'] for i in R.get('o1', {})])
    v['V2_o1_vive'] = m is not None and m >= O1_R0
    todas = [RV[b][i] for b in PRUEBAS for i in RV[b]] + [q for b in CADENAS for i in C.get(b, {}) for q in C[b][i]['pasajes']]
    v['V3_mundo_actua'] = bool(todas) and all((q['libre'] or {}).get('a_mala', 0) > 0 and (q['libre'] or {}).get('a_buena', 0) > 0
                                              and (q['libre'] or {}).get('mudadas', 0) > 0 and sum((q['libre'] or {}).get('quietos') or [0]) > 0 for q in todas)
    # V4 (con la colonizacion): ningun fundador O1_LIB de FABRICA en las pruebas y los primeros salen de la siembra (>= 1)
    v['V4_siembra_actua'] = all(all(RV[b][i]['fund_n'] > 0 and RV[b][i]['fund_fabrica'] == 0 and RV[b][i]['fund_de_siembra'] > 0 for i in RV[b])
                                for b in ('lib', 'neu', 'mix', 'mixn')) \
        and bool(R.get('o1')) and all(R['o1'][i]['fund_n'] == 0 for i in R['o1'])
    est = lambda d: d.get('estado') or {}
    v['V5_perillas'] = all(est(RV[b][i]).get('carro') == ('O1' if b == 'o1' else 'O1_LIB') for b in PRUEBAS for i in RV[b]) \
        and all(est(RV[b][i]).get('sigma') == SIGMA and est(RV[b][i]).get('lee') == 1 and est(RV[b][i]).get('escribe') == 1 and est(RV[b][i]).get('coloniza') == 1
                for b in PRUEBAS if b != 'o1' for i in RV[b]) \
        and all(est(q).get('lee') == CADENAS[b] and est(q).get('sigma') == SIGMA and est(q).get('escribe') == 1 and est(q).get('coloniza') == 1
                for b in CADENAS for i in C.get(b, {}) for q in C[b][i]['pasajes']) \
        and all(est(q).get('mundo') == MUNDO for q in todas)
    v['V6_neutro_neutro'] = bool(C.get('neu')) and all(all(q['activaciones'][k] == 0 for k in ('mem', 'pau', 'soc', 'res'))
                                                       for i in C['neu'] for q in C['neu'][i]['pasajes'])
    valido = all(v.values())
    ok = completo
    p = {}; desc = {}; umbral = False; matiz = None; aviso_carga = False
    if ok:
        cq = lambda b, i: (R[b][i]['grupo']['conquista'] if viva(R[b][i]) else INF)
        conq = [cq('mix', i) for i in I]; conqn = [cq('mixn', i) for i in I]
        pc = sum(c > 0 for c in conq); pn = sum(a > b for a, b in zip(conq, conqn))
        fin = {b: {i: (None if C[b][i].get('extinto') else C[b][i]['pasajes'][-1]['genes_siembra']) for i in I} for b in CADENAS}
        ambas = [i for i in I if fin['lib'][i] and fin['neu'][i]]
        pp = {}
        for k in PODERES:
            a = [fin['lib'][i][k] for i in I if fin['lib'][i]]; bb = [fin['neu'][i][k] for i in I if fin['neu'][i]]
            gana = sum(fin['lib'][i][k] > fin['neu'][i][k] for i in ambas)
            dm = round(med(a) - med(bb), 4) if a and bb else None
            pp[k] = dict(gana=gana, dif_med=dm, lib_med=med(a), neu_med=med(bb), indices_con_ambas=len(ambas),
                         se_prende=bool(dm is not None and gana >= g8 and dm >= DIF_PODER))
        p['PC_conquista'] = pc >= g8
        p['PN_no_es_solo_deriva'] = pn >= g8   # auditoria H-5: "no es solo deriva (purga de carga)": el neutro lleva genes de O1 sin purgar
        p['PP_un_poder_se_prende'] = any(pp[k]['se_prende'] for k in PODERES)
        # EN EL UMBRAL: PC a +-1 de 8; PN a +-1 de 8 SOLO si PC >= 7 (ERR-160 i); o un poder con 'gana' a +-1 de 8 (y dif >= 0.04), o con
        # dif a +-0.01 de 0.05 (y gana >= 7)
        umbral = bool(abs(pc - g8) <= 1 or (pc >= g8 - 1 and abs(pn - g8) <= 1)
                      or any(pp[k]['dif_med'] is not None and abs(pp[k]['gana'] - g8) <= 1 and round(pp[k]['dif_med'] - (DIF_PODER - 0.01), 4) >= 0 for k in PODERES)
                      or any(pp[k]['dif_med'] is not None and pp[k]['gana'] >= g8 - 1 and round(abs(pp[k]['dif_med'] - DIF_PODER), 4) <= 0.01 for k in PODERES))
        nz = lambda L_: [None if x == INF else x for x in L_]
        desc['conquista_por_indice'] = dict(mix=nz(conq), mixn=nz(conqn), mix_gana=pc, mix_gana_a_mixn=pn)
        desc['extinciones'] = {b: {str(i): C[b][i].get('p_extincion') for i in I if C[b][i].get('extinto')} for b in CADENAS}
        desc['poderes_siembra_final'] = pp
        gs = lambda b, i, q: (C[b][i]['pasajes'][q]['genes_siembra'] if len(C[b][i]['pasajes']) > q else None)
        tray = {b: {k: [med([gs(b, i, q)[k] for i in I if gs(b, i, q)]) for q in range(npas)] for k in GENES} for b in CADENAS}
        desc['trayectoria_siembra_mediana'] = tray
        orden = {}
        for k in PODERES:
            d_ = [(round(tray['lib'][k][q] - tray['neu'][k][q], 4) if tray['lib'][k][q] is not None and tray['neu'][k][q] is not None else None) for q in range(npas)]
            prim = next((q for q in range(npas) if all(x is not None and x >= DIF_PODER for x in d_[q:])), None)
            orden[k] = dict(dif_por_pasaje=d_, prende_en_pasaje=prim)
        desc['orden_de_encendido'] = orden
        desc['genes_O1_final'] = {k: dict(lib=med([fin['lib'][i][k] for i in I if fin['lib'][i]]), neu=med([fin['neu'][i][k] for i in I if fin['neu'][i]]),
                                          fabrica=FABRICA[k], lib_gana_neu=sum(fin['lib'][i][k] > fin['neu'][i][k] for i in ambas)) for k in GENES_O1}
        # R-5b: carga: mediana (cadenas) del R0 real mediano de lib en el ULTIMO pasaje contra el PRIMERO
        r0 = lambda q: med([C['lib'][i]['pasajes'][q]['R0_med'] for i in I if len(C['lib'][i]['pasajes']) > q])
        r_1, r_u = r0(0), r0(npas - 1)
        aviso_carga = bool(r_1 is not None and r_u is not None and round(r_1 - r_u, 4) >= 0.15)
        desc['carga_R0_lib_primer_vs_ultimo_pasaje'] = dict(primero=r_1, ultimo=r_u, aviso=aviso_carga)
        desc['suma_cruzan'] = {b: sum(R[b][i]['cruzan'] for i in I) for b in PRUEBAS}
        desc['nac_reales_total_med'] = {b: med([sum(R[b][i]['nac_reales']) for i in I]) for b in PRUEBAS}
        desc['R0_med'] = {b: med([R[b][i]['R0_med'] for i in I]) for b in PRUEBAS}
        desc['PM_monocultivo'] = dict(lib_gana_o1=sum(R['lib'][i]['cruzan'] > R['o1'][i]['cruzan'] for i in I),
                                      neu_gana_o1=sum(R['neu'][i]['cruzan'] > R['o1'][i]['cruzan'] for i in I),
                                      lib_gana_neu=sum(R['lib'][i]['cruzan'] > R['neu'][i]['cruzan'] for i in I),
                                      nac_lib_gana_o1=sum(sum(R['lib'][i]['nac_reales']) > sum(R['o1'][i]['nac_reales']) for i in I))
        desc['mix_cruzan'] = {b: dict(lib=sum(sum(RV[b][i]['grupo']['lib']['cruza']) for i in RV[b]), o1=sum(sum(RV[b][i]['grupo']['o1']['cruza']) for i in RV[b]))
                              for b in MIXTAS if len(R.get(b, {})) == n}
        desc['activaciones_prueba'] = {b: {k: med([RV[b][i]['activaciones'][k] for i in RV[b]]) for k in ('mem', 'pau', 'soc', 'res', 'escr')} for b in ('lib', 'neu', 'mix', 'mixn')}
        # auditoria H-3: partos (descendientes anotados por el carro) por pasaje, lib contra neu (mediana de cadenas)
        desc['partos_por_pasaje'] = {b: [med([C[b][i]['pasajes'][q]['partos_tel'] for i in I if len(C[b][i]['pasajes']) > q]) for q in range(npas)] for b in CADENAS}
        # auditoria H-4: por lado en las mixtas (DESCRIPTIVO; PC NO se lee como supervivencia): medianas de las diferencias lib - o1
        desc['mixtas_por_lado'] = {b: {k: med([RV[b][i]['grupo'][k] for i in RV[b]]) for k in ('conquista', 'dif_partos', 'dif_muertes', 'dif_fund')}
                                   for b in MIXTAS if len(R.get(b, {})) == n}
        # auditoria H-5: mixA (siembra lib con poderes en 0) SOLO DESCRIPTIVO: ¿la conquista de mix se va al quitar los poderes?
        if len(R.get('mixA', {})) == n:
            cA = [cq('mixA', i) for i in I]
            desc['mixA_descriptivo'] = dict(conquista=nz(cA), mixA_gana_o1=sum(c > 0 for c in cA), mix_gana_mixA=sum(a > b for a, b in zip(conq, cA)),
                                            mediana_mix_menos_mixA=med([a - b for a, b in zip(conq, cA) if a != INF and b != INF]))
        desc['activaciones_cadena_lib_ultimo'] = {k: med([C['lib'][i]['pasajes'][-1]['activaciones'][k] for i in I]) for k in ('mem', 'pau', 'soc', 'res', 'escr')}
        desc['mundo_AC'] = {b: med([RV[b][i]['mundo_AC'] for i in RV[b]]) for b in PRUEBAS}
        desc['frac_en_parche_med'] = {b: med([st.mean(RV[b][i]['libre']['frac_en_parche']) for i in RV[b]]) for b in PRUEBAS}
    if not valido: ver = 'NO SE LEE'
    elif all(p.values()): ver = 'FUNCIONA'
    elif p['PC_conquista'] or p['PP_un_poder_se_prende']:
        ver = 'HAY ALGO MODESTO'
        if p['PC_conquista'] and not p['PN_no_es_solo_deriva']: matiz = 'conquista, pero la deriva sola hace lo mismo'
        elif p['PC_conquista'] and p['PN_no_es_solo_deriva']: matiz = 'conquista por seleccion sin poderes (afina las perillas de O1)'
        else: matiz = 'un poder se prende sin conquista'
    else:
        ver = 'NO'
        if aviso_carga: matiz = 'carga domina; NO no informa sobre poderes'   # R-5b: el veredicto NO cambia
    return dict(validez=v, puertas=p, veredicto=ver, matiz=matiz, en_umbral=umbral, aviso_carga=aviso_carga,
                umbrales=dict(gana=g8, dif_poder=DIF_PODER, o1_R0=O1_R0), descriptivo=desc)


def ab_letra(ab):
    """Abortos que cuentan para V1: todos salvo los de las pruebas DESCRIPTIVAS (mixA), que se reportan aparte."""
    return sum(1 for a in ab if not any(f" {d}:" in a for d in DESCRIPTIVAS))


ORD_V = {'NO SE LEE': -1, 'NO': 0, 'HAY ALGO MODESTO': 1, 'FUNCIONA': 2}
def bloque(a, b): return a if a == b else min((a, b), key=lambda z: ORD_V[z])


def carga(carpeta):
    C = {b: {} for b in CADENAS}; R = {b: {} for b in TODAS}; ab = []
    for f in sorted(glob.glob(os.path.join(carpeta, 'cadena_i*_*.json')) + glob.glob(os.path.join(carpeta, 'prueba_i*_*.json'))):
        d = json.load(open(f, encoding='utf-8'))
        if d.get('aborto'): ab.append(f"{d['tipo']} i{d['i']} {d['brazo']}: {d['aborto']}"); continue
        if d['tipo'] == 'cadena': C[d['brazo']][d['i']] = d
        else: R[d['brazo']][d['i']] = d
    return C, R, ab


def imprime(L, log):
    log(f"  validez: {L['validez']}")
    log(f"  puertas: {L['puertas']} · umbrales {L['umbrales']} · EN EL UMBRAL (+-1): {L['en_umbral']} · matiz {L['matiz']}")
    for k, v in L['descriptivo'].items(): log(f"  [desc] {k}: {v}")


# ------------------------------------------------------------------ verificaciones y candados
def verifica(log):
    ok = True
    for ruta, sha in SHAS.items():
        s = h16(ruta); ok &= s == sha; log(f"  sha {os.path.relpath(ruta, RAIZ)} {s} {'OK' if s == sha else '!= ' + sha + ' FALLA'}")
    for nm, b in CB.todas().items():
        igual = open(os.path.join(AQUI, 'carros', nm + '.py'), 'rb').read() == b; ok &= igual
        log(f"  carro {nm} == construye_o1_lib: {igual}")
    return ok


def identidad_corta(log, seed=734950, T=1500):
    """En CADA corrida real: O1_LIB0 == O1, O1_LIB (sigma 0, fabrica) == O1 y pista_libre apagada == pista, salida ENTERA."""
    m = carga_lib()
    spec = importlib.util.spec_from_file_location('carro_O1_LIB0', LIB0_PY); m0 = importlib.util.module_from_spec(spec); spec.loader.exec_module(m0)
    o1 = CV.modulo('O1')
    kw = dict(T=T, pizarra=1, rep_acum=0, escala=1, mundo_n=None, fundador_limpio=1)
    j = lambda r: json.dumps(r, default=str, sort_keys=True)
    base = j(P.run(seed, [('X', o1)] * 9, **kw))
    i0 = j(P.run(seed, [('X', m0)] * 9, **kw)) == base
    try:
        _pon_lib(m, seed, None, 1, 0, 0.0); i1 = j(P.run(seed, [('X', m)] * 9, **kw)) == base
    finally:
        _apaga_lib(m)
    i2 = j(PL.run(seed, [('X', o1)] * 9, **kw, **PL.MUNDO_VIEJO)) == base
    log(f"  IDENTIDAD CORTA (salida ENTERA, N 9, s {seed}, T {T}): O1_LIB0 == O1 {i0} · O1_LIB sigma 0 fabrica == O1 {i1} · pista_libre apagada == pista {i2}")
    return i0 and i1 and i2


def git_limpio(rutas, log):
    ok = True
    for r in rutas:
        rel = os.path.relpath(r, RAIZ).replace('\\', '/')
        try:
            t = subprocess.run(['git', '-C', RAIZ, 'ls-files', '--error-unmatch', rel], capture_output=True, text=True).returncode == 0
            c = subprocess.run(['git', '-C', RAIZ, 'diff', '--quiet', 'HEAD', '--', rel], capture_output=True, text=True).returncode == 0
            h = subprocess.run(['git', '-C', RAIZ, 'log', '-1', '--format=%h %cI', '--', rel], capture_output=True, text=True).stdout.strip()
        except Exception as e:   # noqa
            t = c = False; h = str(e)
        ok &= t and c; log(f"  git {rel}: commiteado {t} · sin cambios vs HEAD {c} · ultimo commit {h}")
    return ok


def guarda(pre, reanuda):
    previas = sorted(d for d in glob.glob(os.path.join(DATOS, pre + '_*')) if os.path.isdir(d))
    for d in previas:
        rj = os.path.join(d, 'resumen.json')
        if os.path.exists(rj):
            r = json.load(open(rj, encoding='utf-8'))
            if not r.get('humo') and (r.get('letra') or {}).get('veredicto') in ('FUNCIONA', 'HAY ALGO MODESTO', 'NO'):
                return f"{os.path.relpath(rj, RAIZ)} ya tiene veredicto {r['letra']['veredicto']}: no se re-corre"
    if previas and not reanuda: return f"ya existe {os.path.relpath(previas[-1], RAIZ)}: solo --reanuda (cortada o NO SE LEE)"
    return None


def main(argv=None):
    ap = argparse.ArgumentParser(allow_abbrev=False)
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument('--humo', action='store_true'); g.add_argument('--serie', action='store_true'); g.add_argument('--replica', action='store_true')
    g.add_argument('--bloque', default=None); g.add_argument('--lee', default=None)
    ap.add_argument('--pool', type=int, default=0); ap.add_argument('--reanuda', action='store_true')
    a = ap.parse_args(argv)   # ERR-115: nunca parse_known_args
    if a.pool < 0 or a.pool > POOL_MAX: raise SystemExit(f"--pool entre 0 y {POOL_MAX} (PC compartido: contrato del encargo)")
    if a.bloque:
        rs = [json.load(open(x.strip(), encoding='utf-8')) for x in a.bloque.split(',')]
        if len(rs) != 2 or rs[0].get('modo') != 'serie' or rs[1].get('modo') != 'replica':
            raise SystemExit("--bloque: <resumen serie>,<resumen replica> (en ese orden, no humo)")
        yo = h16(os.path.abspath(__file__))
        if any(r.get('sha_runner') != yo for r in rs):
            raise SystemExit(f"--bloque: sha_runner de los resumenes {[r.get('sha_runner') for r in rs]} != runner actual {yo}")
        va, vb = rs[0]['letra']['veredicto'], rs[1]['letra']['veredicto']
        print(f"serie {va} · replica {vb} -> BLOQUE: {bloque(va, vb)}  ({PRERREGISTRO} sec. 6-7)")
        return 0
    if a.lee:
        c = os.path.abspath(a.lee); C, R, ab = carga(c)
        n = max([len(v) for v in C.values()] + [len(v) for v in R.values()])
        npas = max((len(C[b][i]['pasajes']) for b in C for i in C[b]), default=NPAS)
        L = lee_serie(C, R, n, ab_letra(ab), npas); imprime(L, print)
        print(f"VEREDICTO ({'HUMO/parcial, no cuenta' if n != N_IND else 'letra'}): {L['veredicto']} (matiz {L.get('matiz')}) · en el umbral {L['en_umbral']} · abortos {ab}")
        return 0
    if a.humo:
        if a.pool: raise SystemExit("--humo: sin Pool (un proceso)")
        modo = 'humo'; base = HUMO['base']; n = HUMO['n']; npas = HUMO['npas']; Tp = HUMO['T_pas']; Tr = HUMO['T_pru']
        f1 = [('cadena', 0, 'lib'), ('cadena', 0, 'neu'), ('prueba', 0, 'o1'), ('prueba', 0, 'mix')]   # 2x2 pasajes + 2 = 6 corridas
        f2 = []
        if a.reanuda: f2 = [('prueba', 0, 'lib'), ('prueba', 0, 'neu'), ('prueba', 0, 'mixn'), ('prueba', 0, 'mixA')]   # 4 corridas
        pre = 'humo'; dest = os.path.join(DATOS, 'humo')
    else:
        modo = 'serie' if a.serie else 'replica'; base = BASES[modo]; n = N_IND; npas = NPAS; Tp = T_PAS; Tr = T_PRU
        f1 = [('cadena', i, b) for i in range(n) for b in CADENAS] + [('prueba', i, 'o1') for i in range(n)]
        f2 = []
        pre = f"{modo}_i{sem_pru(base, 0)}-{sem_pru(base, n - 1)}"; dest = DATOS
    sel = time.strftime('%Y%m%d_%H%M%S')
    prev = sorted(d for d in os.listdir(dest) if d.startswith(pre + '_') and os.path.isdir(os.path.join(dest, d))) if os.path.isdir(dest) else []
    if a.reanuda and not prev: raise SystemExit(f"--reanuda: no hay carpeta {pre}_* en {dest}")
    carpeta = os.path.join(dest, prev[-1]) if (a.reanuda and prev) else os.path.join(dest, pre + '_' + sel)
    BUF = []; LOGF = [None]

    def log(s=''):
        s = f"[{time.strftime('%H:%M:%S')}] {s}"
        print(s, flush=True)
        if LOGF[0] is None: BUF.append(s)
        else: LOGF[0].write(s + '\n'); LOGF[0].flush()
    t0 = time.time()
    shp = h16(os.path.join(AQUI, PRERREGISTRO)) if os.path.exists(os.path.join(AQUI, PRERREGISTRO)) else 'NO EXISTE'
    log(f"CORRE_O1_LIBRE · {modo} · {sel} · python {platform.python_version()} · pool {a.pool or 'NO (un proceso)'} · corre_o1_libre.py "
        f"{h16(os.path.abspath(__file__))} · preregistro {PRERREGISTRO} {shp} · carpeta {carpeta}")
    log(f"  pasajes {sem_pas(base, 0, 0)}-{sem_pas(base, n - 1, npas - 1)} (T {Tp} x {npas}) · pruebas {sem_pru(base, 0)}-{sem_pru(base, n - 1)} (T {Tr}) · "
        f"pruebas {list(PRUEBAS)} + descriptivas {list(DESCRIPTIVAS)} · mundo {MUNDO} · reanuda {a.reanuda}")
    if not a.humo:
        e = guarda(pre, a.reanuda)
        if e: log(f"  NO SE CORRE (candado): {e}"); return 1
    if a.replica:
        rsm = sorted(glob.glob(os.path.join(DATOS, f"serie_i{BASES['serie'][1]}-*", 'resumen.json')))
        rs0 = json.load(open(rsm[-1], encoding='utf-8')) if rsm else {}
        vs = (rs0.get('letra') or {}).get('veredicto'); um = (rs0.get('letra') or {}).get('en_umbral')
        if not (vs in ('FUNCIONA', 'HAY ALGO MODESTO') or (vs == 'NO' and um)):
            log(f"  REGLA DE PARADA (sec. 7): la replica solo si la serie da FUNCIONA, MODESTO o NO EN EL UMBRAL; serie = {vs} (umbral {um}). No se corre.")
            return 1
        if rs0.get('sha_runner') != h16(os.path.abspath(__file__)):
            log(f"  NO SE CORRE (candado): sha_runner de la serie {rs0.get('sha_runner')} != runner actual"); return 1
    ok = verifica(log) and identidad_corta(log)
    if not a.humo:
        ok &= git_limpio([os.path.join(AQUI, PRERREGISTRO), os.path.abspath(__file__), os.path.join(AQUI, 'construye_o1_lib.py'), LIB_PY, LIB0_PY,
                          os.path.join(AQUI, 'pista_libre.py')], log)
    if not ok: log("  ALGO FALLA -> no se corre (no se crea carpeta)."); return 1
    os.makedirs(carpeta, exist_ok=True)
    LOGF[0] = open(os.path.join(carpeta, 'log.txt'), 'a', encoding='utf-8'); LOGF[0].write('\n'.join(BUF) + '\n'); LOGF[0].flush()
    mk = lambda t: (t[0], t[1], t[2], base, npas, Tp, Tr, carpeta, a.reanuda)
    X = []

    def fmt(x):
        if x['tipo'] == 'cadena':
            return (f"  [{time.time()-t0:7.1f}s] cadena i{x['i']} {x['brazo']} ({x['seg']}s) aborto {x['aborto']} cruzan por pasaje "
                    f"{[q['cruzan'] for q in x.get('pasajes', [])]} poderes p-ultimo "
                    f"{ {k: (x.get('pasajes') or [{}])[-1].get('genes_siembra', {}).get(k) for k in PODERES} if x.get('pasajes') else None}")
        if x.get('extinto'): return f"  [{time.time()-t0:7.1f}s] prueba i{x['i']} {x['brazo']:5s} EXTINTA (cadena {x['cadena_extinta']} sin partos en el pasaje {x['p_extincion']})"
        gr = x.get('grupo') or {}
        return (f"  [{time.time()-t0:7.1f}s] prueba i{x['i']} {x['brazo']:5s} ({x['seg']}s) aborto {x['aborto']} cruzan {x.get('cruzan')}/9 "
                f"nac {x.get('nac_reales')} conquista {gr.get('conquista')} activaciones {x.get('activaciones')}")
    # las pruebas que dependen de una cadena entran a la cola cuando su cadena termina
    dep = {b: [q for q in TODAS if SIEMBRA_DE[q] == b] for b in CADENAS}
    if a.pool and a.pool > 1:
        from multiprocessing import Pool
        with Pool(a.pool) as PLL:
            pend = {PLL.apply_async(trabajo, (mk(t),)): t for t in f1}
            while pend:
                listos = [r for r in pend if r.ready()]
                if not listos: time.sleep(2); continue
                for r in listos:
                    t = pend.pop(r); x = r.get(); X.append(x); log(fmt(x))
                    if t[0] == 'cadena':
                        for q in dep[t[2]]: pend[PLL.apply_async(trabajo, (mk(('prueba', t[1], q)),))] = ('prueba', t[1], q)
    else:
        cola = list(f1)
        if not a.humo:
            cola = [t for t in f1 if t[0] == 'cadena'] + [('prueba', i, q) for i in range(n) for q in TODAS]
        for t in cola + f2:
            x = trabajo(mk(t)); X.append(x); log(fmt(x))
    C, R, ab = carga(carpeta)
    if a.humo and not a.reanuda:
        log(f"\n  HUMO parte 1: {len(X)} trabajos (2 cadenas de {npas} pasajes + o1 y mix = {2 * npas + 2} corridas) · faltan lib, neu, mixn, mixA (--humo --reanuda) · {time.time()-t0:.1f}s")
    L = lee_serie(C, R, n, ab_letra(ab), npas)
    log(f"\n================ LA LETRA ({PRERREGISTRO} sec. 6)" + (" -- HUMO: T corto, practica, 1 indice: NO cuenta" if a.humo else ""))
    imprime(L, log)
    if ab: log(f"  ABORTOS: {ab}")
    ver = ('HUMO (no cuenta): ' if a.humo else '') + L['veredicto'] + (f" ({L['matiz']})" if L.get('matiz') else '')
    rj = os.path.join(carpeta, 'resumen.json')
    with open(rj, 'w', encoding='utf-8') as fh:
        json.dump(dict(modo=modo, humo=a.humo, letra=L, abortos=ab, n=n, npas=npas, T_pas=Tp, T_pru=Tr, veredicto=ver, preregistro=PRERREGISTRO,
                       sha_preregistro=(shp if shp != 'NO EXISTE' else None), sha_runner=h16(os.path.abspath(__file__)),
                       shas={os.path.relpath(k, RAIZ): v for k, v in SHAS.items()}, seg=round(time.time() - t0, 1)), fh, ensure_ascii=False, indent=1)
    log(f"\n  RESUMEN {rj} (sha {h16(rj)}) · abortos {len(ab)} · {time.time()-t0:.1f}s")
    log(f"VEREDICTO DE LA {modo.upper()}: {ver}   (en el umbral: {L['en_umbral']}; regla de parada: {PRERREGISTRO} sec. 7)")
    return 0


if __name__ == '__main__':
    sys.exit(main())
