"""corre_perillas.py — RUNNER y LETRA de "¿LA SELECCION PRENDE LO QUE EL MUNDO PAGA?" (perillas del modulo de memoria de lugar como
GENES que arrancan en 0, en el mundo CON oasis de P1). 1-oct-2026, creador. Preregistro: PREREGISTRO_perillas.md (la letra esta AQUI, en
lee_serie(), y alli en la sec. 6). Carro: construye_perillas.py (O1_LUGAR_GEN). Arnes: identidad_perillas.py. Bitacora: ../BITACORA.md.

MISION: llegar a la AGI por este camino (organismo minimo con reglas locales, sin retropropagacion, peldanos preregistrados con
controles y replicas).

QUE SE CORRE: cada corrida ES experimentos/tronco_v14_3/corre_v143.tarea (regla 14; se IMPORTA) con mundo_escalera.run en lugar de
pista.run y el mundo de P1 (corre_p1.MUNDO_OASIS: oasis 1, extra 0.8, pobre 0.5, dens 0.5, vista_r 20). La fila fisica es
corre_p1.fila (CONGELADO, sha fijado). Monocultivo de 9 carros O1_LUGAR_GEN, L 360, 36 objetos, fundador limpio.
  Por indice i (0..N-1):
  CADENA sel: NPAS pasajes de T_PAS; PS_LEE 1 (los genes se LEEN); UNA mutacion por nacimiento en UN gen (sigma 0.03, sesgo a la
              perdida delta 0.01). Pasaje 0: SIEMBRA None = los 9 primeros fundadores nacen de (GW, GV) = (0, 0) + mutacion (modulo MUDO
              == O1). DENTRO del pasaje, CAMARA CONTINUA: cada refundacion copia (mutado) el genoma del cuerpo actual de OTRO linaje al
              azar (seleccion por persistencia, sin juez). ENTRE pasajes (mundo nuevo, oasis en otro sitio):
              siembra() = genes de los cuerpos VIVOS muestreados cada 1 000 pasos en los ultimos VENT pasos, SOLO de los linajes
              ESTABLECIDOS EN EL PASAJE (ninguna refundacion en la segunda mitad: la misma instancia del carro en todas sus muestras
              con t >= T/2). Respaldo si ninguno: los de menos refundaciones. No lee R0, hijos, cruza ni nada del juez.
  RELOJES (dos, por separado; V7): (1) PROFUNDIDAD MUTACIONAL = eventos de mutacion (nacimientos: partos + fundaciones) en la ascendencia
              de un genoma desde la base (0, 0) del pasaje 0; de una cadena = mediana sobre su siembra final. (2) REFUNDACIONES POR
              CAMARA = numero de reemplazos (un linaje extinto recibe la copia mutada del genoma de otro) sumados en la cadena.
  CADENA neu: LA MISMA cadena (mismas semillas, herencia, mutacion, muestreo y moneda) con PS_LEE 0: los genes se heredan y derivan
              pero ningun cuerpo los lee (cada cuerpo decide como O1): deriva pura, mismo pedigri que O1.
  PRUEBA T_PRU (semilla propia de i), los 4 brazos con EL MISMO carro, sin mutacion (sigma 0, delta 0), sin camara y UN genoma fijo
  (monomorfica: la prueba no es otra ronda de seleccion):
     sel = genoma MEDIANO de la siembra final de SU cadena sel · neu = idem de SU cadena neu ·
     fab = (1, 1), el valor de DISENO de P1 (== O1_LUGAR bit a bit: el techo) · o1 = (0, 0) (== O1: el piso).
SEMILLAS NUEVAS 741xxx (grep 1-oct: no aparecen en .py/.md):
  serie:   pasaje p (0..4) de la cadena i -> 741000 + 10 i + p (741000-741194); prueba de i -> 741201 + i (741201-741220)
  replica: pasaje p (0..4) de la cadena i -> 741300 + 10 i + p (741300-741494); prueba de i -> 741501 + i (741501-741520)
  practica 741900-741999: explora cadenas 741900 + 10 i + p (i 0..3; 741900-741902 usadas) · explora genomas fijos 741941-741944 (741941 usada) ·
           arnes 741950-741989 · humo 741990-741998.
nube-9: trabajo() atrapa TODO y devuelve 'aborto'; JSON por trabajo y por pasaje ANTES de volver (ERR-54); --reanuda salta lo hecho.

  python experimentos/organelos/escalera/perillas/corre_perillas.py --humo                 # 1 proceso: 2 cadenas x 2 pasajes de 5k + pruebas sel y neu de 20k = 6 corridas
  python experimentos/organelos/escalera/perillas/corre_perillas.py --humo --reanuda       # 2o proceso: pruebas fab y o1 (2 corridas), lee y escribe el resumen
  python experimentos/organelos/escalera/perillas/corre_perillas.py --explora --genomas 1:0,0:1 [--n 2] [--T 100000]
  python experimentos/organelos/escalera/perillas/corre_perillas.py --explora --npas 3 [--T 100000] [--cadenas sel,neu] [--desde 0]
  python experimentos/organelos/escalera/perillas/corre_perillas.py --serie --pool 2 [--reanuda]     (SOLO el coordinador)
  python experimentos/organelos/escalera/perillas/corre_perillas.py --replica --pool 2 [--reanuda]   (solo por la regla de parada)
  python experimentos/organelos/escalera/perillas/corre_perillas.py --lee <carpeta>
"""
import argparse, copy, glob, hashlib, importlib.util, json, math, os, platform, statistics as st, subprocess, sys, time

try: sys.stdout.reconfigure(encoding='utf-8', errors='replace')
except Exception: pass
AQUI = os.path.dirname(os.path.abspath(__file__))
ESC = os.path.dirname(AQUI)
RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(ESC)))
for _d in (AQUI, ESC):
    if _d not in sys.path: sys.path.insert(0, _d)
import corre_p1 as CO            # fila, MUNDO_OASIS, sin_tel, verifica (se IMPORTA; CONGELADO, sha fijado)
import construye_perillas as CB
CV = CO.CV; P = CO.P; ME = CO.ME

PRERREGISTRO = 'PREREGISTRO_perillas.md'
DATOS = os.path.join(AQUI, 'datos'); BITACORA = os.path.join(ESC, 'BITACORA.md')
CARRO = 'O1_LUGAR_GEN'
CARROS = {n: os.path.join(AQUI, 'carros', n + '.py') for n, _ in CB.VARIANTES}
SHAS_ESC = {'corre_p1.py': '392b71186cf49b60', 'construye_p1.py': '90dc1b6f848fac80', 'mundo_escalera.py': '4f28b372207ba0a6',
            os.path.join('carros', 'O1_LUGAR.py'): '49eee6bb278ea097'}   # de escalera/ (commiteados; no se tocan)
SHAS_PROPIOS = {'construye_perillas.py': 'b5d1a10f6f913556', os.path.join('carros', 'O1_LUGAR_GEN.py'): 'ecc996d2fecccc30',
                os.path.join('carros', 'O1_LUGAR_GEN0.py'): '89db6c8a74902fe1'}   # fijados al cerrar el preregistro (1-oct 07:45); si cambian, no corre
MUNDO = dict(CO.MUNDO_OASIS)     # el mundo de P1: oasis 1, extra 0.8, pobre 0.5, dens 0.5, vista_r 20
GENES = CB.GENES; BASE = dict(zip(GENES, CB.BASE)); DISENO = dict(zip(GENES, CB.DISENO)); SIGMA = CB.SIGMA; DELTA = CB.DELTA
CADENAS = ('sel', 'neu'); LEE_CADENA = {'sel': 1, 'neu': 0}
ORDEN = ('sel', 'neu', 'fab', 'o1'); CAND = 'sel'; NEU = 'neu'; TECHO = 'fab'; PISO = 'o1'
BASES = {'serie': (741000, 741201), 'replica': (741300, 741501), 'humo': (741990, 741998), 'explora': (741900, 741941)}
N_IND = 20; NPAS = 5; T_PAS = 100000; T_PRU = 100000; VENT = 5000; POOL_MAX = 2
HUMO = dict(n=1, npas=2, T_pas=5000, T_pru=20000)
MAX_CORRIDAS_1P = 6; MAX_PASOS_1P = 200000
# ------------------------------------------------------------------ constantes de la LETRA (PREREGISTRO sec. 6), para n = 20
GEN_LETRA = 'GV'       # PG se lee en el gen del VIAJE (el que el mundo paga por diseno: P1 sec. 11 y exploracion de este bloque)
MARGEN_G = 0.05        # PG: gen mediano de la siembra final de sel > el de neu + 0.05 (pareado por cadena)
GANA_PAR = 13          # PG y PC-par: en >= 13/20 cadenas (nulo binomial p 0.5: P(X >= 13) = 0.132)
DIF_SUMA = 10          # PC-suma: suma de linajes que cruzan (de 180) de sel >= la de neu + 10
FAB_GANA = 16          # V2: el mundo paga en las semillas de prueba: fab > o1 en linajes que cruzan en >= 16/20 (historico 20/20 x2)
PROF_MIN = 30          # V7a: PROFUNDIDAD MUTACIONAL de la cadena NEUTRA (mediana de su siembra final) >= 30 eventos de mutacion (exploracion:
                       #      ~13 por pasaje en neu; en sel el gen ya habia subido con 10.5) ...
REFUND_MIN = 3000      # V7b: ...y REFUNDACIONES POR CAMARA de la cadena NEUTRA (suma de sus pasajes) >= 3000 reemplazos (exploracion: ~930 por
                       #      pasaje en neu; en sel el gen subio en un pasaje con 972) ...
RELOJ_CAD = 16         #      ...cada una en >= 16/20 cadenas. Si no: NO SE LEE (no hubo reloj: no es un NO)


def h16(p): return hashlib.sha256(open(p, 'rb').read()).hexdigest()[:16]
def sem_pas(base, i, p): return base[0] + 10 * i + p
def sem_pru(base, i): return base[1] + i
def med(x):
    x = [v for v in x if v is not None]
    return round(float(st.median(x)), 4) if x else None
def esc(k, n): return math.ceil(k * n / 20 - 1e-9)   # umbral escalado (solo humo/explora, que NO cuentan)


# ------------------------------------------------------------------ estado por proceso (cfg por worker)
def fija():
    """Carga en ESTE proceso el carro O1_LUGAR_GEN (verifica que el archivo == construye_perillas) y lo registra en corre_v143._MODS."""
    ruta = CARROS[CARRO]
    if open(ruta, 'rb').read() != CB.todas()[CARRO]: raise SystemExit(f"{ruta} != construye_perillas (correr construye_perillas.py)")
    m = CV._MODS.get(CARRO)
    if m is None or os.path.abspath(m.__file__) != os.path.abspath(ruta):
        spec = importlib.util.spec_from_file_location(f"carro_{CARRO}", ruta)
        m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); CV._MODS[CARRO] = m
    if m.PERILLAS != 1: raise SystemExit(f"{CARRO}: PERILLAS {m.PERILLAS} != 1")
    return dict(carro=CARRO, sha=h16(ruta), PERILLAS=m.PERILLAS, LUGAR=m.LUGAR, LUGAR_BARAJA=m.LUGAR_BARAJA, LG_MIN=m.LG_MIN,
                PS_BASE=list(m.PS_BASE), PS_CLIP=[list(z) for z in m.PS_CLIP])


def _pon(m, siembra, seed, sigma, delta, lee, camara):
    m.SIEMBRA = copy.deepcopy(siembra); m.PS_SEMILLA = int(seed); m.PS_SIGMA = float(sigma); m.PS_DELTA = float(delta); m.PS_LEE = int(lee); m.PS_CAMARA = int(camara)
    m._TEL.clear(); m._PS_CNT.clear(); m._VIVO.clear()


def _quita(m): _pon(m, None, 0, SIGMA, DELTA, 1, 1)


def tarea(seed, T, siembra=None, sigma=SIGMA, lee=1, mundo=None, delta=DELTA, camara=1):
    """corre_v143.tarea tal cual (regla 14) con el mundo de P1 en lugar de pista.run + la fisica del oasis por linaje y la telemetria
    'lugar' (como corre_p1._tarea_completa) + 'tel_ps' (copia de _TEL del carro, solo lectura) + 'estado' (perillas de ESTE proceso)."""
    est = fija(); m = CV._MODS[CARRO]
    mk = dict(MUNDO if mundo is None else mundo)
    _pon(m, siembra, seed, sigma, delta, lee, camara)
    est.update(sigma=float(sigma), delta=float(delta), camara=int(camara), siembra_n=len(siembra or []), lee=int(lee), mundo=dict(mk))
    cap = []; tel = []; orig = P.run

    def run2(*a, **k):
        m._TEL.clear(); m._PS_CNT.clear(); m._VIVO.clear()
        r = ME.run(*a, **dict(k, **mk)); cap.append(r)
        tel.append(copy.deepcopy({str(i): v for i, v in m._TEL.items()}))
        return r
    P.run = run2
    try:
        x = CV.tarea((seed, CARRO, T))
    finally:
        P.run = orig; _quita(m)
    r = cap[0]
    for l, d in zip(x['linajes'], r['linajes']): l['_oasis'] = d['_carrera'].get('oasis')
    x['tel'] = [dict(lugar=(dict(d['carro']['lugar'], st_lg_bono=d['carro'].get('lg_bono', 0), st_lg_apr=d['carro'].get('lg_apr', 0),
                                 st_lg_viajes=d['carro'].get('lg_viajes', 0)) if isinstance(d.get('carro'), dict) and 'lugar' in d['carro'] else None),
                     sn=None) for d in r['linajes']]
    x['tel_ps'] = tel[0]; x['estado'] = est
    return x


# ------------------------------------------------------------------ LA MONEDA (la transferencia entre pasajes)
def siembra(tel, T, vent=VENT):
    """SOLO de los VIVOS de los linajes ESTABLECIDOS EN EL PASAJE. tel = {indice: {'vivos': [[t, genes, instancia, profundidad], ...]}}.
    Establecido = todas sus muestras con t >= T/2 son de LA MISMA instancia del carro (ninguna refundacion en la segunda mitad) y tiene
    muestras en la ventana final. Da siembra: los genes de sus muestras con t >= T - vent. Respaldo (ninguno establecido): los linajes con
    MENOS instancias distintas en la segunda mitad. No recibe (ni puede leer) R0, hijos, cruza ni nada del juez.
    -> (lista de genomas {GW, GV, prof} o None, info)."""
    cand = {}
    for i in sorted(tel or {}, key=lambda z: int(z)):
        vv = (tel[i] or {}).get('vivos', [])
        fin = [(g, pr) for t, g, c, pr in vv if t >= T - vent]
        if not fin: continue
        cand[int(i)] = (len({c for t, g, c, pr in vv if t >= T // 2}), fin)
    if not cand: return None, dict(n_est=0, respaldo=True, idx=[], n=0)
    est = [i for i in cand if cand[i][0] == 1]
    resp = not est
    idx = est if est else [i for i in cand if cand[i][0] == min(v[0] for v in cand.values())]
    out = [dict({k: float(v) for k, v in zip(GENES, g)}, prof=int(pr)) for i in idx for g, pr in cand[i][1]]
    return (out or None), dict(n_est=len(est), respaldo=bool(resp), idx=idx, n=len(out))


def genoma_mediano(sie):
    """El genoma que entra a la PRUEBA: mediana por gen (CRUDO) de la siembra final."""
    if not sie: return None
    return {k: float(st.median([s[k] for s in sie])) for k in GENES}


def prof_de(sie):
    """PROFUNDIDAD MUTACIONAL de una siembra: mediana de los eventos de mutacion en la ascendencia de sus genomas (desde la base del pasaje 0)."""
    return float(st.median([s['prof'] for s in sie])) if sie else None


def fila(x, T):
    """corre_p1.fila (fisica del juez + del oasis + telemetria 'lugar') + lo de los genes (telemetria de solo escritura del carro)."""
    f = CO.fila(x, T); tel = x.get('tel_ps') or {}
    fp = [q for v in tel.values() for q in (v or {}).get('fund', [])]
    viv = [g for v in tel.values() for t, g, c, pr in (v or {}).get('vivos', []) if t >= T - VENT]
    prs = [pr for v in tel.values() for t, g, c, pr in (v or {}).get('vivos', []) if t >= T - VENT]
    f.update(fund_de_siembra=sum(int(q[0] == 1) for q in fp), fund_de_camara=sum(int(q[0] == 2) for q in fp), fund_de_base=sum(int(q[0] == 0) for q in fp),
             fund_n=len(fp), partos_tel=sum((v or {}).get('partos', 0) for v in tel.values()), prof_vivos_fin=med(prs),
             fund_genes_distintos=len({tuple(q[1]) for q in fp}),
             fund_gen0=(dict(zip(GENES, fp[0][1])) if fp else None),
             genes_vivos_fin={k: med([g[j] for g in viv]) for j, k in enumerate(GENES)} if viv else None)
    return f


def cadena(i, base, npas, T, carpeta, reanuda, brazo, log=None):
    """Cadena sel (genes que se LEEN) o neu (PS_LEE 0): npas pasajes con las MISMAS semillas; JSON por pasaje (reanudable)."""
    sie = None; F = []; lee = LEE_CADENA[brazo]
    for p in range(npas):
        fin = os.path.join(carpeta, f"pasaje_i{i:02d}_{brazo}_p{p:02d}.json")
        if reanuda and os.path.exists(fin):
            with open(fin, encoding='utf-8') as fh: d = json.load(fh)
        else:
            x = tarea(sem_pas(base, i, p), T, siembra=sie, sigma=SIGMA, lee=lee, delta=DELTA, camara=1)
            sig, info = siembra(x['tel_ps'], T)
            f = fila(x, T); gm = genoma_mediano(sig)
            f.update(p=p, sembrado=int(sie is not None), moneda=info, prof=prof_de(sig), genes_siembra=({k: round(v, 4) for k, v in gm.items()} if gm else None),
                     frac_on=(round(sum(1 for s in sig if s[GEN_LETRA] > MARGEN_G) / len(sig), 3) if sig else None))
            d = dict(fila=f, siembra_sig=sig)
            tmp = fin + '.tmp'
            with open(tmp, 'w', encoding='utf-8') as fh: json.dump(d, fh, ensure_ascii=False)
            os.replace(tmp, fin)
        F.append(d['fila']); sie = d['siembra_sig']
        if log: log(f"    cadena i{i} {brazo} p{p} s{d['fila']['seed']} cruzan {d['fila']['cruzan']}/9 moneda {d['fila']['moneda']} prof mutacional {d['fila']['prof']} refundaciones por camara {d['fila']['fund_de_camara']} genes siembra {d['fila']['genes_siembra']}")
        if not sie: raise RuntimeError(f"pasaje {p}: siembra vacia (no hay vivos muestreados)")
    return dict(pasajes=F, siembra_final=sie, genoma_final=genoma_mediano(sie), prof_final=prof_de(sie), refund_camara=sum(q['fund_de_camara'] for q in F),
                partos=sum(q['partos_tel'] for q in F))


def genoma_de(brazo, i, carpeta):
    if brazo == TECHO: return dict(DISENO)
    if brazo == PISO: return dict(BASE)
    with open(os.path.join(carpeta, f"cadena_i{i:02d}_{brazo}.json"), encoding='utf-8') as fh: c = json.load(fh)
    if c.get('aborto') or not c.get('genoma_final'): raise RuntimeError("cadena sin genoma final")
    return c['genoma_final']


def trabajo(args):
    """UN trabajo: ('cadena', i, 'sel'|'neu') · ('prueba', i, brazo) · ('fijo', i, 'gw:gv'). Atrapa TODO (nube-9); escribe su JSON antes de
    volver (ERR-54); con reanuda salta el que ya existe SIN aborto (un aborto guardado se reintenta y queda anotado)."""
    tipo, i, brazo, base, npas, T_pas, T_pru, carpeta, reanuda = args
    fin = os.path.join(carpeta, f"{tipo}_i{i:02d}_{brazo.replace(':', '_')}.json"); previo = None
    if reanuda and os.path.exists(fin):
        with open(fin, encoding='utf-8') as fh: x0 = json.load(fh)
        if not x0.get('aborto'): return x0
        previo = x0['aborto']
    t0 = time.time()
    try:
        if tipo == 'cadena':
            if brazo not in CADENAS: raise RuntimeError(f"cadena desconocida {brazo}")
            x = dict(tipo=tipo, i=i, brazo=brazo, aborto=None, **cadena(i, base, npas, T_pas, carpeta, reanuda, brazo))
        else:
            if tipo == 'fijo': g = dict(zip(GENES, [float(z) for z in brazo.split(':')]))
            elif brazo in ORDEN: g = genoma_de(brazo, i, carpeta)
            else: raise RuntimeError(f"brazo desconocido {brazo}")
            y = tarea(sem_pru(base, i), T_pru, siembra=[g], sigma=0.0, lee=1, delta=0.0, camara=0)   # PRUEBA: un genoma fijo, sin mutacion ni camara, genes leidos
            x = dict(tipo=tipo, i=i, brazo=brazo, aborto=None, genoma=g, **fila(y, T_pru))
    except BaseException as e:   # noqa: nube-9
        x = dict(tipo=tipo, i=i, brazo=brazo, aborto=f"{type(e).__name__}: {e}"[:300])
    if previo: x['reintento_de'] = previo
    x['seg'] = round(time.time() - t0, 1)
    tmp = fin + '.tmp'
    with open(tmp, 'w', encoding='utf-8') as fh: json.dump(x, fh, ensure_ascii=False)
    os.replace(tmp, fin)
    return x


# ------------------------------------------------------------------ LA LETRA (PREREGISTRO_perillas.md sec. 6)
def par(A, B, I):
    """Pareado por indice en LINAJES QUE CRUZAN (0-9). gana = indices con A > B (empates EN CONTRA)."""
    a = [A[i]['cruzan'] for i in I]; b = [B[i]['cruzan'] for i in I]
    return dict(n=len(I), gana=sum(x > y for x, y in zip(a, b)), empata=sum(x == y for x, y in zip(a, b)), pierde=sum(x < y for x, y in zip(a, b)),
                suma_a=sum(a), suma_b=sum(b), dif=sum(a) - sum(b), por_indice_a=a, por_indice_b=b)


def par_gen(C, I, k, margen=MARGEN_G):
    """Pareado por cadena en el gen k (CRUDO, mediano de la siembra final): gana = cadenas con sel > neu + margen (empates EN CONTRA)."""
    a = [C[CAND][i]['genoma_final'][k] for i in I]; b = [C[NEU][i]['genoma_final'][k] for i in I]
    return dict(gen=k, margen=margen, n=len(I), gana=sum(x > y + margen for x, y in zip(a, b)), pierde=sum(x < y - margen for x, y in zip(a, b)),
                med_sel=med(a), med_neu=med(b), sel_sobre_margen=sum(x > margen for x in a), neu_sobre_margen=sum(y > margen for y in b),
                sel_positivo=sum(x > 0 for x in a), neu_positivo=sum(y > 0 for y in b),
                por_cadena_sel=[round(x, 4) for x in a], por_cadena_neu=[round(y, 4) for y in b])


def lee_serie(C, R, n, abortos, npas=NPAS):
    """C[brazo][i] = cadena (sel, neu); R[brazo][i] = prueba. n = indices esperados (20 en serie/replica)."""
    I = list(range(n)); gp = esc(GANA_PAR, n); dsu = math.ceil(DIF_SUMA * n / 20 - 1e-9); fg = esc(FAB_GANA, n); rc = esc(RELOJ_CAD, n)
    completo = all(len(C.get(b, {})) == n and all(len(C[b][i]['pasajes']) == npas for i in C[b]) for b in CADENAS) and all(len(R.get(b, {})) == n for b in ORDEN)
    est = lambda d: d.get('estado') or {}
    pas = lambda b: [q for i in C.get(b, {}) for q in C[b][i]['pasajes']]
    v = {}
    v['V1_completa'] = bool(abortos == 0 and completo and all(R[b][i]['coherente'] for b in ORDEN for i in R.get(b, {})) and all(q['coherente'] for b in CADENAS for q in pas(b)))
    pf = par(R[TECHO], R[PISO], I) if completo else None
    v['V2_mundo_paga'] = bool(pf and pf['gana'] >= fg)
    filas = [R[b][i] for b in ORDEN for i in R.get(b, {})] + [q for b in CADENAS for q in pas(b)]
    v['V3_mundo_actua'] = bool(filas and all(q.get('oasis') and q['oasis']['mord_AC_dentro'] > 0 and est(q).get('mundo') == MUNDO for q in filas))
    gen_ok = lambda q, g: q.get('genoma') == g and q['fund_n'] > 0 and q['fund_de_siembra'] == q['fund_n'] and q['fund_genes_distintos'] == 1 and q['fund_gen0'] == g
    v['V4_estado'] = bool(completo and all(est(q).get('carro') == CARRO and est(q).get('PERILLAS') == 1 for q in filas)
                          and all(est(q).get('lee') == LEE_CADENA[b] and est(q).get('sigma') == SIGMA and est(q).get('delta') == DELTA and est(q).get('camara') == 1 for b in CADENAS for q in pas(b))
                          and all(est(R[b][i]).get('lee') == 1 and est(R[b][i]).get('sigma') == 0.0 and est(R[b][i]).get('delta') == 0.0 and est(R[b][i]).get('camara') == 0
                                  and est(R[b][i]).get('siembra_n') == 1 for b in ORDEN for i in I)
                          and all(gen_ok(R[b][i], C[b][i]['genoma_final']) for b in CADENAS for i in I)
                          and all(gen_ok(R[TECHO][i], DISENO) and gen_ok(R[PISO][i], BASE) for i in I))
    lgv = lambda q: (q.get('lugar') or {}).get('viajes')
    nl = 9   # los 9 primeros fundadores salen de la base (pasaje 0) o de la siembra (pasajes siguientes); las refundaciones, de la camara
    v['V5_desde_cero_y_neutro'] = bool(completo and all(C[b][i]['pasajes'][0]['sembrado'] == 0 and C[b][i]['pasajes'][0]['fund_de_base'] == nl and C[b][i]['pasajes'][0]['fund_de_siembra'] == 0 for b in CADENAS for i in I)
                                       and all(q['sembrado'] == 1 and q['fund_de_siembra'] == nl and q['fund_de_base'] == 0 for b in CADENAS for i in I for q in C[b][i]['pasajes'][1:])
                                       and all(q['fund_de_camara'] == q['fund_n'] - nl for b in CADENAS for q in pas(b))
                                       and all(lgv(q) == 0 for q in pas(NEU)) and all(lgv(R[PISO][i]) == 0 and (lgv(R[TECHO][i]) or 0) > 0 for i in I))
    rl = {b: dict(prof=[C[b][i].get('prof_final') for i in sorted(C.get(b, {}))], refund=[C[b][i].get('refund_camara') for i in sorted(C.get(b, {}))],
                  partos=[C[b][i].get('partos') for i in sorted(C.get(b, {}))]) for b in CADENAS}
    sobre = lambda xs, m_: sum(1 for z in xs if z is not None and z >= m_)
    v['V7a_profundidad_mutacional_neutra'] = bool(completo and sobre(rl[NEU]['prof'], PROF_MIN) >= rc)
    v['V7b_refundaciones_por_camara_neutra'] = bool(completo and sobre(rl[NEU]['refund'], REFUND_MIN) >= rc)
    valido = all(v.values()); ok = valido or completo
    p = {}; pg = pc = None
    if ok:
        pg = par_gen(C, I, GEN_LETRA); pc = par(R[CAND], R[NEU], I)
        p['PG_gen_sube'] = pg['gana'] >= gp
        p['PC_par_neu'] = pc['gana'] >= gp
        p['PC_suma_neu'] = pc['dif'] >= dsu
    umbral = bool(ok and (abs(pg['gana'] - gp) <= 1 or abs(pc['gana'] - gp) <= 1 or abs(pc['dif'] - dsu) <= 1))
    matiz = None
    if not valido: ver = 'NO SE LEE'
    else:
        G = p['PG_gen_sube']; Cz = p['PC_par_neu'] and p['PC_suma_neu']
        if G and Cz: ver = 'FUNCIONA'
        elif G or Cz:
            ver = 'HAY ALGO MODESTO'; matiz = 'el gen sube pero no cruza mas que la deriva' if G else 'cruza mas que la deriva sin que el gen suba por la letra'
        else: ver = 'NO'
    desc = {}
    if ok:
        desc['suma_cruzan'] = {b: sum(R[b][i]['cruzan'] for i in I) for b in ORDEN}
        desc['mayorias'] = {b: sum(R[b][i]['mayoria'] for i in I) for b in ORDEN}
        desc['R0_med'] = {b: med([R[b][i]['R0_med'] for i in I]) for b in ORDEN}
        desc['establecidos_0fund_post10k'] = {b: sum(sum(int(z == 0) for z in R[b][i]['fund_post10k']) for i in I) for b in ORDEN}
        desc['fund_media'] = {b: med([st.mean(R[b][i]['fund']) for i in I]) for b in ORDEN}
        desc['ratio_pasos_oasis'] = {b: med([R[b][i]['oasis']['ratio_pasos'] for i in I]) for b in ORDEN}
        desc['mundo_AC'] = {b: med([R[b][i]['mundo_AC'] for i in I]) for b in ORDEN}
        desc['genoma_prueba_mediana'] = {b: {k: med([R[b][i]['genoma'][k] for i in I]) for k in GENES} for b in ORDEN}
        desc['pareados'] = {f"{a}_vs_{b}": par(R[a], R[b], I) for a, b in (('sel', 'neu'), ('sel', 'o1'), ('sel', 'fab'), ('neu', 'o1'), ('fab', 'o1'))}
        desc['genes'] = {k: par_gen(C, I, k) for k in GENES}
    for b in CADENAS:
        Cb = C.get(b, {})
        if not Cb: continue
        np_ = max(len(Cb[i]['pasajes']) for i in Cb)
        col = lambda q, f: [f(Cb[i]['pasajes'][q]) for i in Cb if len(Cb[i]['pasajes']) > q]
        desc[f'{b}_trayectoria_gen_mediana_por_pasaje'] = {k: [med(col(q, lambda z: (z['genes_siembra'] or {}).get(k))) for q in range(np_)] for k in GENES}
        desc[f'{b}_cadenas_con_{GEN_LETRA}_sobre_margen_por_pasaje'] = [sum(1 for z in col(q, lambda z: (z['genes_siembra'] or {}).get(GEN_LETRA)) if z is not None and z > MARGEN_G) for q in range(np_)]
        desc[f'{b}_frac_on_por_pasaje'] = [med(col(q, lambda z: z.get('frac_on'))) for q in range(np_)]
        desc[f'{b}_establecidos_en_pasaje_mediana'] = [med(col(q, lambda z: z['moneda']['n_est'])) for q in range(np_)]
        desc[f'{b}_respaldo_por_pasaje'] = [sum(col(q, lambda z: int(z['moneda']['respaldo']))) for q in range(np_)]
        desc[f'{b}_profundidad_mutacional_por_pasaje_mediana'] = [med(col(q, lambda z: z.get('prof'))) for q in range(np_)]
        desc[f'{b}_refundaciones_por_camara_por_pasaje_mediana'] = [med(col(q, lambda z: z.get('fund_de_camara'))) for q in range(np_)]
        desc[f'{b}_partos_por_pasaje_mediana'] = [med(col(q, lambda z: z.get('partos_tel'))) for q in range(np_)]
        desc[f'{b}_cruzan_por_pasaje_mediana'] = [med(col(q, lambda z: z['cruzan'])) for q in range(np_)]
        desc[f'{b}_ratio_pasos_por_pasaje'] = [med(col(q, lambda z: z['oasis']['ratio_pasos'])) for q in range(np_)]
        desc[f'{b}_viajes_por_pasaje'] = [med(col(q, lambda z: (z.get('lugar') or {}).get('viajes'))) for q in range(np_)]
    desc['relojes'] = {b: dict(profundidad_mutacional=dict(mediana=med(rl[b]['prof']), minimo=min([z for z in rl[b]['prof'] if z is not None] or [None]),
                                                           cadenas_sobre_minimo=sobre(rl[b]['prof'], PROF_MIN), por_cadena=rl[b]['prof']),
                               refundaciones_por_camara=dict(mediana=med(rl[b]['refund']), minimo=min([z for z in rl[b]['refund'] if z is not None] or [None]),
                                                             cadenas_sobre_minimo=sobre(rl[b]['refund'], REFUND_MIN), por_cadena=rl[b]['refund'],
                                                             rondas_de_reemplazo_mediana=(round(med(rl[b]['refund']) / 9, 1) if med(rl[b]['refund']) is not None else None)),
                               partos=dict(mediana=med(rl[b]['partos']))) for b in CADENAS}
    if ok:   # pendiente del gen por evento de mutacion, con el reloj DEL PROPIO brazo (descriptivo; no decide)
        desc['gen_por_evento_de_mutacion'] = {b: {k: med([(C[b][i]['genoma_final'][k] / C[b][i]['prof_final']) if C[b][i].get('prof_final') else None for i in I]) for k in GENES} for b in CADENAS}
    return dict(validez=v, puertas=p, veredicto=ver, matiz=matiz, en_umbral=umbral,
                umbrales=dict(gana_par=gp, dif_suma=dsu, fab_gana=fg, margen_gen=MARGEN_G, gen=GEN_LETRA, prof_min=PROF_MIN, refund_min=REFUND_MIN, reloj_cadenas=rc),
                pareado_gen=pg, pareado_neu=pc, pareado_fab_o1=pf, descriptivo=desc)


ORD_V = {'NO SE LEE': -1, 'NO': 0, 'HAY ALGO MODESTO': 1, 'FUNCIONA': 2}
def bloque(a, b): return a if a == b else min((a, b), key=lambda z: ORD_V[z])


def carga(carpeta):
    C = {b: {} for b in CADENAS}; R = {b: {} for b in ORDEN}; F = []; ab = []
    for f in sorted(glob.glob(os.path.join(carpeta, 'cadena_i*_*.json')) + glob.glob(os.path.join(carpeta, 'prueba_i*_*.json')) + glob.glob(os.path.join(carpeta, 'fijo_i*_*.json'))):
        d = json.load(open(f, encoding='utf-8'))
        if d.get('aborto'): ab.append(f"{d['tipo']} i{d['i']} {d['brazo']}: {d['aborto']}"); continue
        if d['tipo'] == 'cadena': C[d['brazo']][d['i']] = d
        elif d['tipo'] == 'prueba': R[d['brazo']][d['i']] = d
        else: F.append(d)
    return C, R, F, ab


def imprime(L, log):
    log(f"  validez: {L['validez']}")
    log(f"  puertas: {L['puertas']} · umbrales {L['umbrales']} · EN EL UMBRAL (+-1): {L['en_umbral']} · matiz {L['matiz']}")
    q = L['pareado_gen']
    if q: log(f"  pareado_gen {q['gen']} (sel > neu + {q['margen']}): gana {q['gana']} pierde {q['pierde']} de {q['n']} · mediana sel {q['med_sel']} neu {q['med_neu']} · "
              f"sobre el margen: sel {q['sel_sobre_margen']} neu {q['neu_sobre_margen']} · por cadena sel {q['por_cadena_sel']} neu {q['por_cadena_neu']}")
    for k in ('pareado_neu', 'pareado_fab_o1'):
        q = L[k]
        if q: log(f"  {k}: gana {q['gana']} empata {q['empata']} pierde {q['pierde']} · suma {q['suma_a']} vs {q['suma_b']} (dif {q['dif']}) · por indice {q['por_indice_a']} vs {q['por_indice_b']}")
    for k, v in L['descriptivo'].items():
        if k != 'pareados': log(f"  [desc] {k}: {v}")
    for k, q in (L['descriptivo'].get('pareados') or {}).items():
        log(f"  [desc] {k}: gana {q['gana']} empata {q['empata']} pierde {q['pierde']} · suma {q['suma_a']} vs {q['suma_b']}")


# ------------------------------------------------------------------ verificaciones y candados
def verifica(log):
    ok = CO.verifica(log)
    for nm, sha in SHAS_ESC.items():
        s = h16(os.path.join(ESC, nm)); ok &= s == sha; log(f"  sha escalera/{nm} {s} {'OK' if s == sha else '!= ' + sha + ' FALLA'}")
    for nm, sha in SHAS_PROPIOS.items():
        s = h16(os.path.join(AQUI, nm)); fij = sha is not None; ok &= (s == sha) if fij else True
        log(f"  sha perillas/{nm} {s} {'OK' if (not fij or s == sha) else '!= ' + sha + ' FALLA'}{'' if fij else ' (NO FIJADO: solo humo/explora)'}")
    for nm, b in CB.todas().items():
        igual = os.path.exists(CARROS[nm]) and open(CARROS[nm], 'rb').read() == b; ok &= igual
        log(f"  carro {nm} == construye_perillas: {igual}")
    return ok


def _run(mod, seed, T, **mundo):
    return json.loads(json.dumps(ME.run(seed, [('X', mod)] * 9, T=T, pizarra=1, rep_acum=0, escala=1, mundo_n=None, fundador_limpio=1, **mundo), default=str))


def _con(m, siembra, sigma, lee, seed, T, camara=1, **mundo):
    try:
        _pon(m, siembra, seed, sigma, (DELTA if sigma else 0.0), lee, camara)
        return _run(m, seed, T, **mundo)
    finally:
        _quita(m)


def identidad_corta(log, seed=741950, T=1500):
    """En el mundo de P1 (salida ENTERA, N 9, fundador limpio): GEN0 == O1_LUGAR · GEN con genoma (1, 1) y sigma 0 == O1_LUGAR · GEN con
    (0, 0) y sigma 0 == O1 (salvo la telemetria 'lugar') · GEN con PS_LEE 0 y sigma 0.03 == O1 (idem) · control: GEN (1, 1) != O1."""
    fija(); m = CV._MODS[CARRO]; o1 = CV.modulo('O1'); CO.fija('lug'); lug = CV._MODS['O1_LUGAR']
    spec = importlib.util.spec_from_file_location('carro_O1_LUGAR_GEN0', CARROS['O1_LUGAR_GEN0']); m0 = importlib.util.module_from_spec(spec); spec.loader.exec_module(m0)
    rl = _run(lug, seed, T, **MUNDO); ro = _run(o1, seed, T, **MUNDO)
    i0 = _run(m0, seed, T, **MUNDO) == rl
    i1 = _con(m, [dict(DISENO)], 0.0, 1, seed, T, **MUNDO) == rl
    i2 = CO.sin_tel(_con(m, [dict(BASE)], 0.0, 1, seed, T, **MUNDO)) == ro
    i3 = CO.sin_tel(_con(m, None, SIGMA, 0, seed, T, **MUNDO)) == ro
    i4 = CO.sin_tel(rl) != ro
    log(f"  IDENTIDAD CORTA PERILLAS (salida ENTERA, N 9, s {seed}, T {T}, mundo de P1): GEN0 == O1_LUGAR {i0} · GEN (1,1) sigma 0 == O1_LUGAR {i1} · "
        f"GEN (0,0) sigma 0 == O1 (salvo telemetria 'lugar') {i2} · GEN PS_LEE 0, sigma {SIGMA}, delta {DELTA}, camara 1 == O1 {i3} · control O1_LUGAR != O1 {i4}")
    return i0 and i1 and i2 and i3 and i4


def guarda(modo, pre, reanuda):
    """Candados de --serie/--replica (PREREGISTRO sec. 7): shas FIJADOS; se niega si ya hay resumen con veredicto; carpetas previas solo
    con --reanuda; la replica solo si la serie dio FUNCIONA, MODESTO o NO en el umbral y con el mismo sha del runner; todo commiteado."""
    if any(x is None for x in SHAS_PROPIOS.values()): return f"SHAS_PROPIOS sin fijar: {[k for k, x in SHAS_PROPIOS.items() if x is None]}"
    previas = sorted(d for d in glob.glob(os.path.join(DATOS, pre + '_*')) if os.path.isdir(d))
    for d in previas:
        rj = os.path.join(d, 'resumen.json')
        if os.path.exists(rj):
            r = json.load(open(rj, encoding='utf-8'))
            if r.get('modo') == modo and (r.get('letra') or {}).get('veredicto') in ('FUNCIONA', 'HAY ALGO MODESTO', 'NO'):
                return f"{os.path.relpath(rj, RAIZ)} ya tiene veredicto {r['letra']['veredicto']}: no se re-corre"
    if previas and not reanuda: return f"ya existe {os.path.relpath(previas[-1], RAIZ)}: solo --reanuda (cortada o NO SE LEE)"
    if modo == 'replica':
        rsm = sorted(glob.glob(os.path.join(DATOS, f"serie_i{BASES['serie'][1]}-*", 'resumen.json')))
        rs0 = json.load(open(rsm[-1], encoding='utf-8')) if rsm else {}
        vs = (rs0.get('letra') or {}).get('veredicto'); um = (rs0.get('letra') or {}).get('en_umbral')
        if not (vs in ('FUNCIONA', 'HAY ALGO MODESTO') or (vs == 'NO' and um)):
            return f"REGLA DE PARADA: la replica solo si la serie da FUNCIONA, MODESTO o NO EN EL UMBRAL; serie = {vs} (umbral {um})"
        if rs0.get('sha_runner') != h16(os.path.abspath(__file__)): return f"sha_runner de la serie {rs0.get('sha_runner')} != runner actual"
    for r in [os.path.join(AQUI, PRERREGISTRO), os.path.abspath(__file__), os.path.join(AQUI, 'construye_perillas.py')] + list(CARROS.values()):
        rel = os.path.relpath(r, RAIZ).replace(os.sep, '/')
        t = subprocess.run(['git', '-C', RAIZ, 'ls-files', '--error-unmatch', rel], capture_output=True, text=True).returncode == 0
        c = subprocess.run(['git', '-C', RAIZ, 'diff', '--quiet', 'HEAD', '--', rel], capture_output=True, text=True).returncode == 0
        if not (t and c): return f"git: {rel} commiteado {t} · sin cambios vs HEAD {c} (la serie exige todo commiteado)"
    return None


def bitacora(linea):
    with open(BITACORA, 'a', encoding='utf-8') as fh: fh.write(linea + '\n')


def main(argv=None):
    ap = argparse.ArgumentParser(allow_abbrev=False)
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument('--humo', action='store_true'); g.add_argument('--explora', action='store_true')
    g.add_argument('--serie', action='store_true'); g.add_argument('--replica', action='store_true')
    g.add_argument('--bloque', default=None); g.add_argument('--lee', default=None)
    ap.add_argument('--pool', type=int, default=0); ap.add_argument('--reanuda', action='store_true')
    ap.add_argument('--T', type=int, default=None); ap.add_argument('--n', type=int, default=None); ap.add_argument('--npas', type=int, default=None)
    ap.add_argument('--genomas', default=None); ap.add_argument('--cadenas', default=None); ap.add_argument('--desde', type=int, default=None)
    ap.add_argument('--nota', default='')
    a = ap.parse_args(argv)   # ERR-115: nunca parse_known_args
    if a.pool < 0 or a.pool > POOL_MAX: raise SystemExit(f"--pool entre 0 y {POOL_MAX} (contrato del encargo)")
    if a.bloque:
        rs = [json.load(open(x.strip(), encoding='utf-8')) for x in a.bloque.split(',')]
        if len(rs) != 2 or rs[0].get('modo') != 'serie' or rs[1].get('modo') != 'replica': raise SystemExit("--bloque: <resumen serie>,<resumen replica> (en ese orden)")
        yo = h16(os.path.abspath(__file__))
        if any(r.get('sha_runner') != yo for r in rs): raise SystemExit(f"--bloque: sha_runner de los resumenes {[r.get('sha_runner') for r in rs]} != runner actual {yo}")
        va, vb = rs[0]['letra']['veredicto'], rs[1]['letra']['veredicto']
        print(f"serie {va} · replica {vb} -> BLOQUE: {bloque(va, vb)}  ({PRERREGISTRO} sec. 6-7)")
        return 0
    if a.lee:
        c = os.path.abspath(a.lee); C, R, F, ab = carga(c)
        n = max([len(x) for x in C.values()] + [len(x) for x in R.values()] + [0])
        for d in F: print(f"  fijo {d['brazo']} s{d['seed']}: cruzan {d['cruzan']}/9 R0 {d['R0_med']} ratio pasos {d['oasis']['ratio_pasos']}")
        if n and all(len(R[b]) == n for b in ORDEN):
            npas = max(len(C[b][i]['pasajes']) for b in CADENAS for i in C[b])
            L = lee_serie(C, R, n, len(ab), npas); imprime(L, print)
            print(f"VEREDICTO ({'HUMO/parcial, no cuenta' if n != N_IND or npas != NPAS else 'letra'}): {L['veredicto']} (matiz {L.get('matiz')}) · en el umbral {L['en_umbral']} · abortos {ab}")
        else:
            for b in CADENAS:
                for i in sorted(C[b]):
                    for q in C[b][i]['pasajes']: print(f"  cadena i{i} {b} p{q['p']}: cruzan {q['cruzan']}/9 moneda {q['moneda']} prof mutacional {q.get('prof')} refundaciones por camara {q['fund_de_camara']} genes {q['genes_siembra']} frac_on {q['frac_on']} ratio {q['oasis']['ratio_pasos']}")
            print(f"  (parcial: sin las 4 pruebas no hay letra) · abortos {ab}")
        return 0
    fijos = []
    if a.humo:
        if a.pool or a.T or a.n or a.npas or a.genomas or a.cadenas or a.desde is not None: raise SystemExit("--humo: sin Pool y sin perillas (un proceso, configuracion fija)")
        modo = 'humo'; base = BASES['humo']; n = HUMO['n']; npas = HUMO['npas']; Tp = HUMO['T_pas']; Tr = HUMO['T_pru']
        f1 = [('cadena', 0, 'sel'), ('cadena', 0, 'neu'), ('prueba', 0, 'sel'), ('prueba', 0, 'neu')]   # 2 x 2 pasajes + 2 pruebas = 6 corridas
        if a.reanuda: f1 += [('prueba', 0, 'fab'), ('prueba', 0, 'o1')]   # 2o proceso: 2 corridas; lo ya escrito se salta
        ncorr = 2 if a.reanuda else 6; pre = 'humo'; dest = os.path.join(DATOS, 'humo')
    elif a.explora:
        if a.pool: raise SystemExit("--explora: sin Pool (un proceso)")
        modo = 'explora'; base = BASES['explora']; dest = os.path.join(DATOS, 'explora'); i0 = a.desde or 0
        if a.genomas:
            if a.npas or a.cadenas: raise SystemExit("--explora --genomas: sin --npas ni --cadenas")
            n = a.n or 2; Tr = a.T or T_PRU; Tp = 0; npas = 0
            gs = [s.strip() for s in a.genomas.split(',')]
            for s in gs:
                if len(s.split(':')) != len(GENES): raise SystemExit(f"--genomas: 'gw:gv' separados por coma (hay {s!r})")
            f1 = [('fijo', i0 + j, s) for j in range(n) for s in gs]; ncorr = len(f1); pasos = Tr
            pre = f"explora_genomas_{'_'.join(s.replace(':', '-') for s in gs)}_i{i0}-{i0 + n - 1}_T{Tr}"
        else:
            n = a.n or 1; npas = a.npas or 3; Tp = a.T or T_PAS; Tr = 0; cs = tuple(a.cadenas.split(',')) if a.cadenas else CADENAS
            for c in cs:
                if c not in CADENAS: raise SystemExit(f"cadena desconocida {c}")
            f1 = [('cadena', i0 + j, c) for j in range(n) for c in cs]; ncorr = len(f1) * npas; pasos = Tp
            pre = f"explora_cadenas_{'_'.join(cs)}_i{i0}-{i0 + n - 1}_p{npas}_T{Tp}"
        if i0 < 0 or i0 + n > 4: raise SystemExit("--explora: indices 0..3 (semillas de practica 7419xx)")
        if ncorr > MAX_CORRIDAS_1P or pasos > MAX_PASOS_1P: raise SystemExit(f"un proceso: <= {MAX_CORRIDAS_1P} corridas (hay {ncorr}) y <= {MAX_PASOS_1P} pasos (T {pasos})")
    else:
        if a.T or a.n or a.npas or a.genomas or a.cadenas or a.desde is not None: raise SystemExit("--serie/--replica: T, n, pasajes y semillas los fija el preregistro")
        modo = 'serie' if a.serie else 'replica'; base = BASES[modo]; n = N_IND; npas = NPAS; Tp = T_PAS; Tr = T_PRU
        f1 = [('cadena', i, b) for i in range(n) for b in CADENAS] + [('prueba', i, b) for i in range(n) for b in (TECHO, PISO)]
        pre = f"{modo}_i{sem_pru(base, 0)}-{sem_pru(base, n - 1)}"; dest = DATOS
    sel = time.strftime('%Y%m%d_%H%M%S')
    prev = sorted(d for d in os.listdir(dest) if d.startswith(pre + '_') and os.path.isdir(os.path.join(dest, d))) if os.path.isdir(dest) else []
    if a.reanuda and not prev: raise SystemExit(f"--reanuda: no hay carpeta {pre}_* en {dest}")
    if modo in ('serie', 'replica'):
        e = guarda(modo, pre, a.reanuda)
        if e: raise SystemExit(f"NO SE CORRE (candado): {e}")
    carpeta = os.path.join(dest, prev[-1]) if (a.reanuda and prev) else os.path.join(dest, pre + '_' + sel)
    BUF = []; LOGF = [None]   # la carpeta se crea SOLO si todas las verificaciones pasan

    def log(s=''):
        s = f"[{time.strftime('%H:%M:%S')}] {s}"
        print(s, flush=True)
        if LOGF[0] is None: BUF.append(s)
        else: LOGF[0].write(s + '\n'); LOGF[0].flush()
    t0 = time.time()
    shp = h16(os.path.join(AQUI, PRERREGISTRO)) if os.path.exists(os.path.join(AQUI, PRERREGISTRO)) else 'NO EXISTE'
    log(f"CORRE_PERILLAS · {modo} · {sel} · python {platform.python_version()} · pool {a.pool or 'NO (un proceso)'} · corre_perillas.py "
        f"{h16(os.path.abspath(__file__))} · preregistro {PRERREGISTRO} {shp} · carpeta {carpeta}")
    log(f"  base de semillas {base} · pasajes T {Tp} x {npas} · pruebas T {Tr} · n {n} · mundo {MUNDO} · sigma {SIGMA} delta {DELTA} (una mutacion por nacimiento, en un gen) · camara continua · moneda: vivos de los ultimos {VENT} pasos de "
        f"linajes sin refundacion en la segunda mitad · trabajos {[(t[0], t[1], t[2]) for t in f1]} · reanuda {a.reanuda} · nota {a.nota!r}")
    ok = verifica(log) and identidad_corta(log)
    if not ok: log("  ALGO FALLA -> no se corre (no se crea carpeta)."); return 1
    os.makedirs(carpeta, exist_ok=True)
    LOGF[0] = open(os.path.join(carpeta, 'log.txt'), 'a', encoding='utf-8'); LOGF[0].write('\n'.join(BUF) + '\n'); LOGF[0].flush()
    mk = lambda t: (t[0], t[1], t[2], base, npas, Tp, Tr, carpeta, a.reanuda)
    X = []

    def fmt(x):
        if x['tipo'] == 'cadena':
            ps = x.get('pasajes') or []
            return (f"  [{time.time()-t0:7.1f}s] cadena i{x['i']} {x['brazo']} ({x['seg']}s) aborto {x['aborto']} · cruzan por pasaje {[q['cruzan'] for q in ps]} · "
                    f"establecidos {[q['moneda']['n_est'] for q in ps]} respaldo {[int(q['moneda']['respaldo']) for q in ps]} · prof mutacional {[q.get('prof') for q in ps]} · refundaciones por camara {[q['fund_de_camara'] for q in ps]} · partos {[q['partos_tel'] for q in ps]} · {GEN_LETRA} {[(q['genes_siembra'] or {}).get(GEN_LETRA) for q in ps]} · "
                    f"GW {[(q['genes_siembra'] or {}).get('GW') for q in ps]} · frac_on {[q['frac_on'] for q in ps]} · ratio pasos {[q['oasis']['ratio_pasos'] for q in ps]} · genoma final {x.get('genoma_final')}")
        oz = x.get('oasis') or {}
        return (f"  [{time.time()-t0:7.1f}s] {x['tipo']} i{x['i']} {x['brazo']:5s} ({x['seg']}s) aborto {x['aborto']} · genoma {x.get('genoma')} · cruzan {x.get('cruzan')}/9 R0 {x.get('R0_med')} "
                f"fund {x.get('fund')} · ratio pasos {oz.get('ratio_pasos')} · viajes {(x.get('lugar') or {}).get('viajes')} · mundo AC {x.get('mundo_AC')}")
    if a.pool and a.pool > 1:
        from multiprocessing import Pool
        with Pool(a.pool) as PL:
            pend = {PL.apply_async(trabajo, (mk(t),)): t for t in f1}
            while pend:
                listos = [r for r in pend if r.ready()]
                if not listos: time.sleep(2); continue
                for r in listos:
                    t = pend.pop(r); x = r.get(); X.append(x); log(fmt(x))
                    if t[0] == 'cadena':   # su prueba (sel o neu) entra a la cola en cuanto la cadena termina
                        pend[PL.apply_async(trabajo, (mk(('prueba', t[1], t[2])),))] = ('prueba', t[1], t[2])
    else:
        f2 = [('prueba', t[1], t[2]) for t in f1 if t[0] == 'cadena'] if modo in ('serie', 'replica') else []
        for t in f1 + f2:
            x = trabajo(mk(t)); X.append(x); log(fmt(x))
    C, R, F, ab = carga(carpeta)
    L = None
    if all(len(R[b]) == n for b in ORDEN) and all(len(C[b]) == n for b in CADENAS):
        L = lee_serie(C, R, n, len(ab), npas)
        log(f"\n================ LA LETRA ({PRERREGISTRO} sec. 6)" + (f" -- {modo.upper()}: practica, NO cuenta" if modo in ('humo', 'explora') else ""))
        imprime(L, log)
    else:
        log(f"\n  {modo.upper()} parcial: sin las 4 pruebas no hay letra" + (" (faltan fab y o1: --humo --reanuda)" if modo == 'humo' else ""))
    if ab: log(f"  ABORTOS: {ab}")
    ver = (f"{modo.upper()} (no cuenta): " if modo in ('humo', 'explora') else '') + (L['veredicto'] + (f" ({L['matiz']})" if L.get('matiz') else '') if L else 'parcial')
    rj = os.path.join(carpeta, 'resumen.json')
    with open(rj, 'w', encoding='utf-8') as fh:
        json.dump(dict(modo=modo, letra=L, abortos=ab, n=n, npas=npas, T_pas=Tp, T_pru=Tr, veredicto=ver, nota=a.nota, mundo=MUNDO, sigma=SIGMA, delta=DELTA, vent=VENT,
                       preregistro=PRERREGISTRO, sha_preregistro=(shp if shp != 'NO EXISTE' else None), sha_runner=h16(os.path.abspath(__file__)),
                       shas_escalera={k: h16(os.path.join(ESC, k)) for k in SHAS_ESC}, shas_propios={k: h16(os.path.join(AQUI, k)) for k in SHAS_PROPIOS},
                       mundo_escalera=ME.construye()[1], seg=round(time.time() - t0, 1)), fh, ensure_ascii=False, indent=1)
    log(f"\n  RESUMEN {rj} (sha {h16(rj)}) · abortos {len(ab)} · {time.time()-t0:.1f}s")
    log(f"VEREDICTO: {ver}" + (f"   (en el umbral: {L['en_umbral']}; regla de parada: {PRERREGISTRO} sec. 7)" if L else ''))
    if modo in ('humo', 'explora'):
        cad = {f"{b} i{i}": dict(cruzan=[q['cruzan'] for q in C[b][i]['pasajes']], est=[q['moneda']['n_est'] for q in C[b][i]['pasajes']],
                                 GV=[(q['genes_siembra'] or {}).get('GV') for q in C[b][i]['pasajes']], GW=[(q['genes_siembra'] or {}).get('GW') for q in C[b][i]['pasajes']],
                                 frac_on=[q['frac_on'] for q in C[b][i]['pasajes']], prof_mut=[q.get('prof') for q in C[b][i]['pasajes']],
                                 refund_camara=[q['fund_de_camara'] for q in C[b][i]['pasajes']], ratio=[q['oasis']['ratio_pasos'] for q in C[b][i]['pasajes']]) for b in CADENAS for i in sorted(C[b])}
        pru = {f"{b} i{i}": dict(cruzan=R[b][i]['cruzan'], ratio=R[b][i]['oasis']['ratio_pasos']) for b in ORDEN for i in sorted(R[b])}
        fj = {f"{d['brazo']} s{d['seed']}": dict(cruzan=d['cruzan'], R0=d['R0_med'], ratio=d['oasis']['ratio_pasos'], est=sum(int(z == 0) for z in d['fund_post10k'])) for d in F}
        bitacora(f"| {time.strftime('%Y-%m-%d %H:%M')} | PERILLAS (seleccion sobre GW, GV desde 0; mundo de P1) | {modo} base {base} pasajes T{Tp} x{npas} pruebas T{Tr} carro {h16(CARROS[CARRO])} {a.nota} | "
                 f"cadenas {cad} · pruebas {pru} · fijos {fj} · abortos {len(ab)} · perillas\\{os.path.relpath(carpeta, AQUI)} | {ver} |")
    return 0


if __name__ == '__main__':
    sys.exit(main())
