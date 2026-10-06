"""corre_o1_libre_f2.py — RUNNER y LETRA de F2 "UN GEN POR PARTO" (o1_libre_f2, 1-oct-2026; EXPLORATORIO con letra fija).
Preregistro: PREREGISTRO_o1_libre_f2.md (la letra esta AQUI, en lee_serie(), y alli en la sec. 5).

MISION: llegar a la AGI por este camino (organismo minimo con reglas locales, sin retropropagacion, peldanos preregistrados con
controles y replicas). Pregunta (ficha F2 de investigacion_20261001/ENTREGA_1_reactor.md): ¿la carga de mutar los 14 genes en cada
parto, y no la seleccion, es lo que tapa la subida en o1_libre?

UNICO CAMBIO respecto de o1_libre: el carro es O1_LIB_F2 con PS_UNGEN 1 (cada evento de mutacion muta UN gen al azar, misma sigma_j).
Todo lo demas ES o1_libre, IMPORTADO sin tocarlo (corre_o1_libre.py sha 98d3a103a1fdde3b): mundo pista_libre, siembra por partos, colonia,
cadenas lib/neu, pruebas lib/neu/o1/mix/mixn, tarea(), tarea_lista(), siembra(), fila(), cadena(), trabajo(), y la letra PC/PN/PP con
ERR-160 (lee_serie de o1_libre se LLAMA; aqui se le agregan V7, V8, PF1, PF2 y el veredicto de F2).
COMO SE REUSA: al importar ESTE modulo, _instala() cambia en el modulo corre_o1_libre SOLO en memoria (ningun archivo de o1_libre cambia):
  LIB_PY -> carros/O1_LIB_F2.py (con su sha) · _pon_lib/_apaga_lib fijan y apagan ademas PS_UNGEN · tarea() anota 'ungen' en 'estado' ·
  fila() agrega la telemetria 'ungen' · DESCRIPTIVAS = () (mixA NO se corre: declarado antes de datos, sec. 9 del preregistro) · DATOS.
  Con Pool (spawn), cada proceso hijo re-importa ESTE modulo (trabajo() esta definido aqui) y por tanto re-instala lo mismo.
SEMILLAS NUEVAS (grep 1-oct: 744xxx no aparece en .py/.md/.txt/.log de PROYECTOS/JUACO; o1_libre uso 734xxx):
  serie:   pasaje p de la cadena i -> 744000 + 10 i + p; prueba de i -> 744201 + i
  replica: pasaje p de la cadena i -> 744300 + 10 i + p; prueba de i -> 744501 + i
  practica: 744900-744999 (arnes 744950-744989; humo 744990-744998).

Uso (ERR-115: banderas desconocidas o abreviadas ABORTAN; --serie/--replica SOLO el coordinador, con todo commiteado):
  python experimentos/organelos/o1_libre_f2/corre_o1_libre_f2.py --humo              # 1 proceso: 2 cadenas x 2 pasajes de 12k + o1 y mix de 20k (6 corridas, 88 000 pasos)
  python experimentos/organelos/o1_libre_f2/corre_o1_libre_f2.py --humo --reanuda    # 2o proceso: lib, neu, mixn de 20k (3 corridas, 60 000 pasos) y lee
  python experimentos/organelos/o1_libre_f2/corre_o1_libre_f2.py --serie --pool 2
  python experimentos/organelos/o1_libre_f2/corre_o1_libre_f2.py --serie --pool 2 --reanuda     # tras un corte (apagon): salta lo hecho
  python experimentos/organelos/o1_libre_f2/corre_o1_libre_f2.py --replica --pool 2  # solo por la regla de parada (sec. 6)
  python experimentos/organelos/o1_libre_f2/corre_o1_libre_f2.py --lee <carpeta>
  python experimentos/organelos/o1_libre_f2/corre_o1_libre_f2.py --bloque <resumen serie>.json,<resumen replica>.json
"""
import argparse, glob, json, os, platform, statistics as st, sys, time

try: sys.stdout.reconfigure(encoding='utf-8', errors='replace')
except Exception: pass
AQUI = os.path.dirname(os.path.abspath(__file__))
OL = os.path.join(os.path.dirname(AQUI), 'o1_libre')
for _d in (OL, AQUI):
    if _d not in sys.path: sys.path.insert(0, _d)
import corre_o1_libre as CO          # se IMPORTA, no se toca
import construye_o1_lib_f2 as CF
RAIZ = CO.RAIZ; h16 = CO.h16; med = CO.med

PRERREGISTRO = 'PREREGISTRO_o1_libre_f2.md'
DATOS = os.path.join(AQUI, 'datos')
F2_PY = os.path.join(AQUI, 'carros', 'O1_LIB_F2.py')
ORIG_LIB_PY = os.path.join(OL, 'carros', 'O1_LIB.py')
SHA_F2 = 'ed631c4a4623ea11'
SHA_CO = '98d3a103a1fdde3b'          # corre_o1_libre.py (el runner con el que se corrio y cerro o1_libre)
SHA_CF = None                        # construye_o1_lib_f2.py: lo fija el log (git_limpio lo ata al commit)
UNGEN = 1                            # LA perilla del bloque (el arnes la pone en 0 para la identidad)
BASES = {'serie': (744000, 744201), 'replica': (744300, 744501)}
HUMO = dict(base=(744990, 744998), n=1, npas=2, T_pas=12000, T_pru=20000)
N_IND = CO.N_IND; NPAS = CO.NPAS; T_PAS = CO.T_PAS; T_PRU = CO.T_PRU; POOL_MAX = 2
PRUEBAS = CO.PRUEBAS; CADENAS = CO.CADENAS; GENES_O1 = CO.GENES_O1; GENES = CO.GENES; SIGMA = CO.SIGMA
SIG_J = {k: SIGMA * CO.CB.ESCALA[CO.CB.GENES.index(k)] for k in GENES}
# ------------------------------------------------------------------ constantes de la LETRA de F2 (PREREGISTRO sec. 5), para n = 10 indices
R0_NEU = 0.90          # PF1: mediana (por indice) del R0 real mediano de la prueba 'neu' >= 0.90 (o1_libre: 0.795 y 0.620)
MARGEN_R0 = 0.03       # en el umbral: |R0 neu - 0.90| <= 0.03
MARGEN_PF2 = 5         # PF2 (auditoria H-1): suma cruzan lib - suma cruzan o1 >= -5 (no inferioridad con margen; nulos SUPUESTOS con sd ~4)
MARGEN_CRUZ = 4        # en el umbral: |(lib - o1) - (-5)| <= 4 (~1 sd supuesta de la diferencia de dos sumas equivalentes)
SUPERA = 7             # DESCRIPTIVO: lib - o1 >= +7 en la suma de cruces (nulo "lib equivale a O1": ~0.05)
N_MAX = 3.0            # V8: reloj mutacional por gen en el neutro (mediana de cadenas) <= 3.0 (se espera ~12/14 = 0.86; en o1_libre fue ~12)

_ORIG = {}; _ULT = {}


def _instala():
    """Redirige corre_o1_libre (en memoria) al carro de F2. Idempotente. NO cambia ningun archivo de o1_libre."""
    if _ORIG: return
    if h16(os.path.join(OL, 'corre_o1_libre.py')) != SHA_CO: raise SystemExit(f"corre_o1_libre.py sha {h16(os.path.join(OL, 'corre_o1_libre.py'))} != {SHA_CO}")
    _ORIG.update(pon=CO._pon_lib, apaga=CO._apaga_lib, tarea=CO.tarea, fila=CO.fila, lee=CO.lee_serie, verifica=CO.verifica, idc=CO.identidad_corta)
    CO.SHAS[F2_PY] = SHA_F2; CO.LIB_PY = F2_PY
    CO.DESCRIPTIVAS = (); CO.TODAS = CO.PRUEBAS; CO.DATOS = DATOS; CO.PRERREGISTRO = PRERREGISTRO

    def _pon_lib(m, *a, **k):
        _ORIG['pon'](m, *a, **k); m.PS_UNGEN = int(UNGEN); _ULT['ungen'] = int(m.PS_UNGEN)

    def _apaga_lib(m):
        _ORIG['apaga'](m); m.PS_UNGEN = 0

    def tarea(seed, brazo, T, siembra=None, lee=1, mundo=None, sigma=SIGMA):
        _ULT.clear()
        x = _ORIG['tarea'](seed, brazo, T, siembra=siembra, lee=lee, mundo=mundo, sigma=sigma)
        if x['estado'].get('carro') == 'O1_LIB': x['estado']['ungen'] = _ULT.get('ungen')   # lo que _pon_lib dejo puesto en el modulo del carro
        return x

    def fila(x, T, brazo, i=None):
        f = _ORIG['fila'](x, T, brazo, i); tel = x.get('tel') or {}
        u = [sum(((v or {}).get('ungen') or [0, 0, 0])[q] for v in tel.values()) for q in range(3)]
        uj = [sum(((v or {}).get('ungen_j') or [0] * len(GENES))[q] for v in tel.values()) for q in range(len(GENES))]
        f['ungen'] = dict(eventos=u[0], cambia_1=u[1], cambia_0=u[2], por_gen=uj)   # MEDIDO en el carro (solo existe con PS_UNGEN 1)
        return f
    CO._pon_lib = _pon_lib; CO._apaga_lib = _apaga_lib; CO.tarea = tarea; CO.fila = fila


_instala()


def trabajo(args):
    """El trabajo de o1_libre, definido AQUI para que el Pool (spawn) importe este modulo en cada hijo (y con el, _instala())."""
    comprueba_f2()
    return CO.trabajo(args)


def comprueba_f2():
    """Auditoria H-5: ANTES de cada trabajo (en el proceso que lo corre): el carro que cargaria el runner importado es O1_LIB_F2 (sha) y
    _pon_lib deja PS_UNGEN 1 en el. Si no, RuntimeError (se propaga al padre por el Pool; NO es un 'aborto' de trabajo: corta la serie)."""
    m = CO.carga_lib(); s = h16(m.__file__)
    CO._pon_lib(m, 0, None, 1, 0, SIGMA, 0); u = getattr(m, 'PS_UNGEN', None); CO._apaga_lib(m)
    if s != SHA_F2 or os.path.abspath(m.__file__) != os.path.abspath(F2_PY) or u != 1 or UNGEN != 1:
        raise RuntimeError(f"F2 NO ESTA ACTIVA en este proceso (pid {os.getpid()}): carro {m.__file__} sha {s} (se exige {SHA_F2}), PS_UNGEN tras _pon_lib {u}, "
                           f"UNGEN del runner {UNGEN}. NO se corre nada: revisar el import del hijo del Pool.")


# ------------------------------------------------------------------ LOS DOS RELOJES (PREREGISTRO sec. 4)
def reloj(sie, genes=GENES_O1):
    """Reloj MUTACIONAL por gen de una siembra (lista de genomas {gen: valor}): n = media sobre los genes de E[((g - fabrica) / sigma_j)^2].
    Con 14 genes por evento, n = eventos de mutacion a lo largo de la ascendencia; con UN gen por evento, n = eventos / 14."""
    if not sie: return None
    return round(st.mean(st.mean(((s[k] - CO.FABRICA[k]) / SIG_J[k]) ** 2 for s in sie) for k in genes), 4)


def relojes(C, n, npas):
    I = [i for i in range(n)]; out = {}
    for b in CADENAS:
        ns = [reloj(C[b][i].get('siembra_final')) for i in I if i in C.get(b, {})]; vivos = [x for x in ns if x is not None]
        pj = lambda k, src: [med([(C[b][i]['pasajes'][q].get(src) or {}).get(k) if src else C[b][i]['pasajes'][q].get(k)
                                  for i in I if i in C.get(b, {}) and len(C[b][i]['pasajes']) > q]) for q in range(npas)]
        out[b] = dict(n_por_gen=dict(mediana=med(vivos), min=(min(vivos) if vivos else None), max=(max(vivos) if vivos else None), por_cadena=ns),
                      eventos_equivalentes_14n=(round(14 * med(vivos), 2) if vivos else None),
                      fund_colonia_por_pasaje=pj('fund_colonia', None), fund_de_siembra_por_pasaje=pj('fund_de_siembra', None),
                      Ne_linajes_por_pasaje=pj('Ne_linajes', 'siembra_info'), padres_distintos_por_pasaje=pj('padres_distintos', 'siembra_info'),
                      partos_por_pasaje=pj('partos_tel', None), eventos_mutacion_por_pasaje=pj('eventos', 'ungen'))
    return out


# ------------------------------------------------------------------ LA LETRA (PREREGISTRO_o1_libre_f2.md sec. 5)
def lee_serie(C, R, n, abortos, npas=NPAS):
    """Llama a la letra de o1_libre (V1-V6, PC, PN, PP con ERR-160; SIN tocarla) y le agrega la de F2:
    V7 un gen (telemetria del carro), V8 reloj, PF1 (R0 del neutro >= 0.90), PF2 (lib - o1 >= -5 en la suma de cruces) y el veredicto de F2."""
    L = _ORIG['lee'](C, R, n, abortos, npas)
    v = L['validez']; p = L['puertas']; desc = L['descriptivo']; I = list(range(n)); viva = lambda x: not x.get('extinto')
    corridas = [R[b][i] for b in ('lib', 'neu', 'mix', 'mixn') for i in R.get(b, {}) if viva(R[b][i])] \
        + [q for b in CADENAS for i in C.get(b, {}) for q in C[b][i]['pasajes']]
    ug = lambda q: q.get('ungen') or {}
    v['V7_un_gen'] = bool(corridas) and all(ug(q).get('eventos', 0) > 0 and ug(q).get('cambia_1', 0) + ug(q).get('cambia_0', 0) == ug(q)['eventos']
                                            and ug(q).get('cambia_1', 0) > 0 and (q.get('estado') or {}).get('ungen') == 1
                                            and (q.get('estado') or {}).get('sha') == SHA_F2 for q in corridas)
    rl = relojes(C, n, npas); nn = rl['neu']['n_por_gen']['mediana']
    v['V8_reloj_un_gen'] = nn is not None and nn <= N_MAX
    desc['relojes'] = rl
    L['letra_o1_libre'] = dict(veredicto=L['veredicto'], matiz=L['matiz'], en_umbral=L['en_umbral'])   # DESCRIPTIVO: lo que diria la letra vieja
    valido = all(v.values()); umbral = False; matiz = None; carga = False; solo = False
    if not p: valido = False   # serie incompleta (V1 ya es False): no hay puertas que leer
    if p:   # serie completa
        r0n = med([R['neu'][i]['R0_med'] for i in I]); sl = sum(R['lib'][i]['cruzan'] for i in I); so = sum(R['o1'][i]['cruzan'] for i in I)
        p['PF1_neutro_no_se_degrada'] = bool(r0n is not None and r0n >= R0_NEU)
        p['PF2_lib_no_bajo_o1'] = bool(sl - so >= -MARGEN_PF2)
        nl = rl['lib']['n_por_gen']['mediana']
        desc['F2'] = dict(R0_neu_med=r0n, R0_o1_med=med([R['o1'][i]['R0_med'] for i in I]), R0_lib_med=med([R['lib'][i]['R0_med'] for i in I]),
                          cruzan_lib=sl, cruzan_o1=so, cruzan_neu=sum(R['neu'][i]['cruzan'] for i in I), dif_lib_o1=sl - so,
                          lib_supera_o1_con_margen=bool(sl - so >= SUPERA),
                          historico_o1_libre=dict(R0_neu=[0.795, 0.620], cruzan_lib=[55, 39], cruzan_o1=[66, 69], cruzan_neu=[30, 32], n_neu=[11.87, 11.65]),
                          # prediccion RIVAL (PURGA, sec. 3): con menos carga la seleccion borra antes de sumar: el reloj de lib queda a <= la mitad del neutro
                          firma_purga=bool(nl is not None and nn is not None and nn > 0 and nl <= 0.5 * nn and not p['PC_conquista']),
                          reloj_lib_sobre_neu=(round(nl / nn, 3) if nl is not None and nn else None))
        umbral = bool(L['en_umbral'] or (r0n is not None and round(abs(r0n - R0_NEU), 4) <= MARGEN_R0) or abs(sl - so + MARGEN_PF2) <= MARGEN_CRUZ)
        carga = p['PF1_neutro_no_se_degrada'] and p['PF2_lib_no_bajo_o1']
    if not valido: ver = 'NO SE LEE'
    elif carga and p['PC_conquista'] and p['PN_no_es_solo_deriva']: ver = 'FUNCIONA'
    elif carga or p['PC_conquista'] or p['PP_un_poder_se_prende']:
        ver = 'HAY ALGO MODESTO'
        solo = bool(carga and not p['PC_conquista'] and not p['PP_un_poder_se_prende'])   # auditoria H-2
        if solo: matiz = 'SOLO CARGA, NO SUBIDA'
        elif carga and not p['PC_conquista']: matiz = 'un poder se prende sin conquista; el deficit de lib frente a O1 no aparece'
        elif carga: matiz = 'conquista, pero la deriva sola hace lo mismo'
        elif p['PC_conquista']: matiz = 'conquista sin que el neutro deje de degradarse o con lib bajo O1 en monocultivo'
        else: matiz = 'un poder se prende; la carga no explica el deficit'
        if p['PP_un_poder_se_prende'] and not matiz.startswith('un poder'): matiz += ' · ademas un poder se prende'
    else:
        ver = 'NO'
        matiz = ('la carga se quito (el neutro no se degrada) y lib sigue bajo O1: la carga no era lo que tapaba' if p['PF1_neutro_no_se_degrada']
                 else 'un gen por parto no quita la degradacion del neutro')
    L.update(veredicto=ver, matiz=matiz, en_umbral=umbral, solo_carga=solo)
    L['umbrales'].update(R0_neu=R0_NEU, margen_R0=MARGEN_R0, margen_PF2=MARGEN_PF2, margen_cruz=MARGEN_CRUZ, supera=SUPERA, n_max=N_MAX)
    return L


def verifica(log):
    ok = _ORIG['verifica'](log)   # shas de o1_libre (incluye O1_LIB, el ORIGEN de las anclas) + el de O1_LIB_F2; carros de o1_libre == su constructor
    igual = open(F2_PY, 'rb').read() == CF.construye(); ok &= igual
    log(f"  carro O1_LIB_F2 == construye_o1_lib_f2: {igual} · LIB_PY del runner importado -> {os.path.relpath(CO.LIB_PY, RAIZ)}")
    return bool(ok and os.path.abspath(CO.LIB_PY) == os.path.abspath(F2_PY))


def identidad_corta(log, seed=744950, T=3000):
    """En CADA corrida real: (1) la de o1_libre con el carro de F2 (O1_LIB0 == O1; O1_LIB_F2 sigma 0 == O1; pista_libre apagada == pista);
    (2) O1_LIB_F2 con PS_UNGEN 0 == O1_LIB de o1_libre, salida ENTERA y telemetria, en el mundo del bloque con sigma 0.03 y colonia;
    (3) con PS_UNGEN 1 la salida CAMBIA (control que puede fallar)."""
    global UNGEN
    ok = _ORIG['idc'](log, seed=seed, T=1500)
    import importlib.util
    spec = importlib.util.spec_from_file_location('carro_O1_LIB_orig', ORIG_LIB_PY); mo = importlib.util.module_from_spec(spec); spec.loader.exec_module(mo)
    m = CO.carga_lib(); kw = dict(T=T, pizarra=1, rep_acum=0, escala=1, mundo_n=None, fundador_limpio=1)
    j = lambda r: json.dumps(r, default=str, sort_keys=True)
    g = UNGEN; S = []
    try:
        for u, mod in ((0, mo), (0, m), (1, m)):
            UNGEN = u
            (_ORIG['pon'] if mod is mo else CO._pon_lib)(mod, seed, None, 1, 1, SIGMA, coloniza=1)
            try: S.append((j(CO.PL.run(seed, [('X', mod)] * 9, **kw, **CO.MUNDO)), j({str(k): w for k, w in mod._TEL.items()})))
            finally: (_ORIG['apaga'] if mod is mo else CO._apaga_lib)(mod)
    finally:
        UNGEN = g
    i1 = S[0] == S[1]; i2 = S[2][0] != S[0][0]
    log(f"  IDENTIDAD CORTA F2 (salida ENTERA + telemetria, N 9, s {seed}, T {T}, mundo del bloque, sigma {SIGMA}, colonia): "
        f"O1_LIB_F2 con PS_UNGEN 0 == O1_LIB {i1} · con PS_UNGEN 1 != {i2}")
    return bool(ok and i1 and i2)


def imprime(L, log):
    log(f"  validez: {L['validez']}")
    log(f"  puertas: {L['puertas']} · umbrales {L['umbrales']} · EN EL UMBRAL: {L['en_umbral']} · matiz {L['matiz']}")
    log(f"  [letra de o1_libre, descriptivo] {L['letra_o1_libre']}")
    for k, v in L['descriptivo'].items(): log(f"  [desc] {k}: {v}")


def main(argv=None):
    ap = argparse.ArgumentParser(allow_abbrev=False)
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument('--humo', action='store_true'); g.add_argument('--serie', action='store_true'); g.add_argument('--replica', action='store_true')
    g.add_argument('--bloque', default=None); g.add_argument('--lee', default=None)
    ap.add_argument('--pool', type=int, default=0); ap.add_argument('--reanuda', action='store_true')
    a = ap.parse_args(argv)   # ERR-115: nunca parse_known_args
    if a.pool < 0 or a.pool > POOL_MAX: raise SystemExit(f"--pool entre 0 y {POOL_MAX} (PC compartido: contrato del encargo)")
    yo = h16(os.path.abspath(__file__))
    if a.bloque:
        rs = [json.load(open(x.strip(), encoding='utf-8')) for x in a.bloque.split(',')]
        if len(rs) != 2 or rs[0].get('modo') != 'serie' or rs[1].get('modo') != 'replica':
            raise SystemExit("--bloque: <resumen serie>,<resumen replica> (en ese orden, no humo)")
        if any(r.get('sha_runner') != yo for r in rs):
            raise SystemExit(f"--bloque: sha_runner de los resumenes {[r.get('sha_runner') for r in rs]} != runner actual {yo}")
        va, vb = rs[0]['letra']['veredicto'], rs[1]['letra']['veredicto']
        print(f"serie {va} · replica {vb} -> BLOQUE: {CO.bloque(va, vb)}  ({PRERREGISTRO} sec. 5-6)")
        return 0
    if a.lee:
        c = os.path.abspath(a.lee); C, R, ab = CO.carga(c)
        n = max([len(v) for v in C.values()] + [len(v) for v in R.values()])
        npas = max((len(C[b][i]['pasajes']) for b in C for i in C[b]), default=NPAS)
        L = lee_serie(C, R, n, CO.ab_letra(ab), npas); imprime(L, print)
        print(f"VEREDICTO ({'HUMO/parcial, no cuenta' if n != N_IND else 'letra'}): {L['veredicto']} (matiz {L.get('matiz')}) · en el umbral {L['en_umbral']} · abortos {ab}")
        return 0
    if a.humo:
        if a.pool: raise SystemExit("--humo: sin Pool (un proceso)")
        modo = 'humo'; base = HUMO['base']; n = HUMO['n']; npas = HUMO['npas']; Tp = HUMO['T_pas']; Tr = HUMO['T_pru']
        f1 = [('cadena', 0, 'lib'), ('cadena', 0, 'neu'), ('prueba', 0, 'o1'), ('prueba', 0, 'mix')]   # 2x2 pasajes + 2 = 6 corridas
        f2 = [('prueba', 0, 'lib'), ('prueba', 0, 'neu'), ('prueba', 0, 'mixn')] if a.reanuda else []   # 3 corridas
        pre = 'humo'; dest = os.path.join(DATOS, 'humo')
    else:
        modo = 'serie' if a.serie else 'replica'; base = BASES[modo]; n = N_IND; npas = NPAS; Tp = T_PAS; Tr = T_PRU
        f1 = [('cadena', i, b) for i in range(n) for b in CADENAS] + [('prueba', i, 'o1') for i in range(n)]
        f2 = []
        pre = f"{modo}_i{CO.sem_pru(base, 0)}-{CO.sem_pru(base, n - 1)}"; dest = DATOS
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
    log(f"CORRE_O1_LIBRE_F2 · {modo} · {sel} · python {platform.python_version()} · pool {a.pool or 'NO (un proceso)'} · corre_o1_libre_f2.py {yo} · "
        f"corre_o1_libre.py (importado) {h16(os.path.join(OL, 'corre_o1_libre.py'))} · construye_o1_lib_f2.py {h16(os.path.join(AQUI, 'construye_o1_lib_f2.py'))} · "
        f"preregistro {PRERREGISTRO} {shp} · PS_UNGEN {UNGEN} · carpeta {carpeta}")
    log(f"  pasajes {CO.sem_pas(base, 0, 0)}-{CO.sem_pas(base, n - 1, npas - 1)} (T {Tp} x {npas}) · pruebas {CO.sem_pru(base, 0)}-{CO.sem_pru(base, n - 1)} (T {Tr}) · "
        f"pruebas {list(PRUEBAS)} (mixA NO se corre) · mundo {CO.MUNDO} · reanuda {a.reanuda}")
    if not a.humo:
        e = CO.guarda(pre, a.reanuda)
        if e: log(f"  NO SE CORRE (candado): {e}"); return 1
    if a.replica:
        rsm = sorted(glob.glob(os.path.join(DATOS, f"serie_i{BASES['serie'][1]}-*", 'resumen.json')))
        rs0 = json.load(open(rsm[-1], encoding='utf-8')) if rsm else {}
        vs = (rs0.get('letra') or {}).get('veredicto'); um = (rs0.get('letra') or {}).get('en_umbral')
        if not (vs in ('FUNCIONA', 'HAY ALGO MODESTO') or (vs == 'NO' and um)):
            log(f"  REGLA DE PARADA (sec. 6): la replica solo si la serie da FUNCIONA, MODESTO o NO EN EL UMBRAL; serie = {vs} (umbral {um}). No se corre.")
            return 1
        if rs0.get('sha_runner') != yo:
            log(f"  NO SE CORRE (candado): sha_runner de la serie {rs0.get('sha_runner')} != runner actual"); return 1
    ok = verifica(log) and identidad_corta(log)
    comprueba_f2()   # H-5: tambien en el padre, antes de crear la carpeta
    if not a.humo:
        ok &= CO.git_limpio([os.path.join(AQUI, PRERREGISTRO), os.path.abspath(__file__), os.path.join(AQUI, 'construye_o1_lib_f2.py'), F2_PY,
                             os.path.join(OL, 'corre_o1_libre.py'), os.path.join(OL, 'construye_o1_lib.py'), ORIG_LIB_PY, CO.LIB0_PY,
                             os.path.join(OL, 'pista_libre.py')], log)
    if not ok: log("  ALGO FALLA -> no se corre (no se crea carpeta)."); return 1
    os.makedirs(carpeta, exist_ok=True)
    LOGF[0] = open(os.path.join(carpeta, 'log.txt'), 'a', encoding='utf-8'); LOGF[0].write('\n'.join(BUF) + '\n'); LOGF[0].flush()
    mk = lambda t: (t[0], t[1], t[2], base, npas, Tp, Tr, carpeta, a.reanuda)
    X = []

    def fmt(x):
        if x['tipo'] == 'cadena':
            return (f"  [{time.time()-t0:7.1f}s] cadena i{x['i']} {x['brazo']} ({x['seg']}s) aborto {x['aborto']} cruzan por pasaje "
                    f"{[q['cruzan'] for q in x.get('pasajes', [])]} reloj n por gen {reloj(x.get('siembra_final'))} "
                    f"eventos/cambia_0 por pasaje {[((q.get('ungen') or {}).get('eventos'), (q.get('ungen') or {}).get('cambia_0')) for q in x.get('pasajes', [])]}")
        if x.get('extinto'): return f"  [{time.time()-t0:7.1f}s] prueba i{x['i']} {x['brazo']:5s} EXTINTA (cadena {x['cadena_extinta']} sin partos en el pasaje {x['p_extincion']})"
        gr = x.get('grupo') or {}
        return (f"  [{time.time()-t0:7.1f}s] prueba i{x['i']} {x['brazo']:5s} ({x['seg']}s) aborto {x['aborto']} cruzan {x.get('cruzan')}/9 R0 {x.get('R0_med')} "
                f"nac {x.get('nac_reales')} conquista {gr.get('conquista')}")
    dep = {b: [q for q in PRUEBAS if CO.SIEMBRA_DE[q] == b] for b in CADENAS}   # las pruebas entran a la cola cuando su cadena termina
    if a.pool and a.pool > 1:
        from multiprocessing import Pool
        with Pool(a.pool) as PLL:
            pend = {PLL.apply_async(trabajo, (mk(t),)): t for t in f1}
            pids = lambda: sorted(w.pid for w in getattr(PLL, '_pool', []))   # auditoria H-7: si un hijo muere, el Pool lo reemplaza y su trabajo no vuelve nunca
            pids0 = pids()
            while pend:
                listos = [r for r in pend if r.ready()]
                if not listos:
                    if pids() != pids0:
                        log(f"  UN PROCESO DEL POOL MURIO (pids {pids0} -> {pids()}): se corta la serie SIN resumen ni veredicto. Lo hecho queda en "
                            f"JSON; relanzar con --{modo} --pool {a.pool} --reanuda. Pendientes: {sorted(pend.values())[:6]}...")
                        PLL.terminate(); return 2
                    time.sleep(2); continue
                for r in listos:
                    t = pend.pop(r); x = r.get(); X.append(x); log(fmt(x))
                    if t[0] == 'cadena':
                        for q in dep[t[2]]: pend[PLL.apply_async(trabajo, (mk(('prueba', t[1], q)),))] = ('prueba', t[1], q)
    else:
        cola = list(f1)
        if not a.humo:
            cola = [t for t in f1 if t[0] == 'cadena'] + [('prueba', i, q) for i in range(n) for q in PRUEBAS]
        for t in cola + f2:
            x = trabajo(mk(t)); X.append(x); log(fmt(x))
    C, R, ab = CO.carga(carpeta)
    if a.humo and not a.reanuda:
        log(f"\n  HUMO parte 1: {len(X)} trabajos (2 cadenas de {npas} pasajes + o1 y mix = {2 * npas + 2} corridas) · faltan lib, neu, mixn (--humo --reanuda) · {time.time()-t0:.1f}s")
    L = lee_serie(C, R, n, CO.ab_letra(ab), npas)
    log(f"\n================ LA LETRA ({PRERREGISTRO} sec. 5)" + (" -- HUMO: T corto, practica, 1 indice: NO cuenta" if a.humo else ""))
    imprime(L, log)
    if ab: log(f"  ABORTOS: {ab}")
    ver = ('HUMO (no cuenta): ' if a.humo else '') + L['veredicto'] + (f" ({L['matiz']})" if L.get('matiz') else '')
    rj = os.path.join(carpeta, 'resumen.json')
    with open(rj, 'w', encoding='utf-8') as fh:
        json.dump(dict(modo=modo, humo=a.humo, letra=L, abortos=ab, n=n, npas=npas, T_pas=Tp, T_pru=Tr, veredicto=ver, preregistro=PRERREGISTRO,
                       sha_preregistro=(shp if shp != 'NO EXISTE' else None), sha_runner=yo, sha_runner_o1_libre=SHA_CO, ungen=UNGEN, solo_carga=bool(L.get('solo_carga')),
                       shas={os.path.relpath(k, RAIZ): v for k, v in CO.SHAS.items()}, seg=round(time.time() - t0, 1)), fh, ensure_ascii=False, indent=1)
    log(f"\n  RESUMEN {rj} (sha {h16(rj)}) · abortos {len(ab)} · {time.time()-t0:.1f}s")
    log(f"VEREDICTO DE LA {modo.upper()}: {ver}   (en el umbral: {L['en_umbral']}; regla de parada: {PRERREGISTRO} sec. 6)")
    return 0


if __name__ == '__main__':
    sys.exit(main())
