"""corre_moneda.py — LA MONEDA (29-sep-2026, creador; DIAGNOSTICO EXPLORATORIO). Preregistro: PREREGISTRO_moneda.md.

MISION: llegar a la AGI por este camino (organismo minimo con reglas locales, sin retropropagacion, peldanos preregistrados con
controles y replicas).

PREGUNTA (junta Fable, investigador 1): la seleccion por pasajes (siembra = bancos finales a 25k) no solo no ENCUENTRA la regla de riesgo
de forzada3 ("riesgo(10) > 0.5 -> boca -3"); la PURGA aunque cruce a 100k, porque paga en la moneda de la letra y no en la del pasaje.

ENTRADA (regla 14): TODA corrida ES sentidos_muro/corre_sentidos_muro.tarea(seed, 'bq3', T, siembra) (se IMPORTA, no se toca; sha fijado)
= bloques_pista/corre_bp.tarea(seed, 'V143_BQ3', T, cfg=CFG, siembra) = juez.tarea(...) con el carro V143_BQ3 de sentidos_muro. El brazo
'cero' (validez) usa la misma entrada con cfg = CERO (tasas 0). Cadena = la de bq3_pas: NPAS pasajes de T_PAS; la siembra del pasaje
siguiente = corre_bp.siembra_de (union de los bancos finales). UNICA diferencia con bq3_pas: la siembra del pasaje 0 (inyectada).

SIEMBRA INYECTADA (450 listas de UNA regla; la mitad de cada una, intercaladas):
  moneda : A = [10, 0, 1, 0.5, 0, -3.0]  (LA fila de forzada3)       + B = [10, 5, 1, 0.5, 0, 0.0] (neutra: w 0, etiqueta j 5)
  neutra : A0 = [10, 0, 1, 0.5, 0, 0.0]  (la misma fila con w 0)      + B
  cero   : A0 + B con TASAS 0 (validez: la etiqueta es invisible; solo deriva)
  Para el sentido 10 el campo j NO se lee (_bq_s3): j es una ETIQUETA muda. "Vacias" del encargo -> B (ver PREREGISTRO sec. 2: una lista
  vacia no entra nunca al banco, corre_bp.siembra_de y _bq_banco la descartan, y la comparacion quedaria regalada).
MEDIDA: fraccion de listas de la siembra con una regla de CLASE A (sentido 10, j 0, '>', boca; cualquier theta y w) a la SALIDA de cada
pasaje p0..p9 (p9 = la siembra que entra a la prueba). Igual para los tres brazos.
PRUEBA (solo moneda): pista vieja T 100 000, semillas 59201-59205 con la siembra final; pareada con forzada3 y bq3_pas GUARDADOS.

SEMILLAS NUEVAS (grep 29-sep: 6331xx no aparece en .py/.md/.txt de PROYECTOS/JUACO; en .json solo como cifras de floats):
  pasaje p del indice i (1..5): 633100 + 10 i + p (633110-633159), LAS MISMAS en los tres brazos (pareado)
  humo: pasajes 633180 + p, prueba 633191 · arnes 633192.
Pool: MAXIMO 2. Cada trabajo registra los carros y fija cfg al entrar, atrapa TODO y escribe cada JSON ANTES de volver (ERR-54).
--reanuda sigue la ultima carpeta y REINTENTA los JSON con aborto (los buenos no se recorren). ERR-115: banderas exactas.

  python experimentos/organelos/moneda/corre_moneda.py --humo                 # 1 proceso, 6 corridas, 135 000 pasos
  python experimentos/organelos/moneda/corre_moneda.py --explora --pool 2     # 15 cadenas (10 x 25k) + 5 pruebas 100k
  python experimentos/organelos/moneda/corre_moneda.py --explora --pool 2 --reanuda
  python experimentos/organelos/moneda/corre_moneda.py --lee datos/explora_<fecha>
"""
import argparse, hashlib, json, os, platform, statistics as st, sys, time

try: sys.stdout.reconfigure(encoding='utf-8', errors='replace')
except Exception: pass
AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(AQUI)))
SMD = os.path.join(RAIZ, 'experimentos', 'organelos', 'sentidos_muro')
BPD = os.path.join(RAIZ, 'experimentos', 'organelos', 'bloques_pista')
for _d in (AQUI, SMD, BPD):
    if _d not in sys.path: sys.path.insert(0, _d)
import corre_sentidos_muro as SM   # tarea, registra, verifica, CFG, CERO, FORZADA3 (se IMPORTA, no se toca; sha fijado)
CBP = SM.CBP

PRERREGISTRO = 'PREREGISTRO_moneda.md'
DATOS = os.path.join(AQUI, 'datos')
SMEXP = os.path.join(SMD, 'datos', 'explora_20260929_110024')
SHAS = {os.path.join(SMD, 'corre_sentidos_muro.py'): '4776b80e18733079', os.path.join(SMD, 'construye_sm.py'): '59e3a6693012d358',
        os.path.join(SMD, 'carros', 'V143_BQ3.py'): 'dd527e3c627e77fb', os.path.join(BPD, 'corre_bp.py'): '6b9c11a6639d3948'}
REFS = {'forzada3': ['45f584a52a12222b', '598d1e3511f75407', 'c38f58315cc06f8a', 'dab209fb1e96edcd', '6eed99ada0876760'],
        'bq3_pas': ['f81ee08a42df3008', 'e5717fc4fa44e43f', '8dfc6994f235cfe2', '349fa9efcf35d174', '360e08b3bdb4faf7']}

CFG = dict(SM.CFG); CERO = dict(SM.CERO)
A = [10.0, 0.0, 1.0, 0.5, 0.0, -3.0]     # == SM.FORZADA3[0] (arnes)
A0 = [10.0, 0.0, 1.0, 0.5, 0.0, 0.0]
B = [10.0, 5.0, 1.0, 0.5, 0.0, 0.0]
NSIE = 450
# brazo -> (fila marcada, cfg, prueba)
BRAZOS = {'moneda': (A, CFG, True), 'neutra': (A0, CFG, False), 'cero': (A0, CERO, False)}
MODOS = {'explora': dict(ind=[1, 2, 3, 4, 5], npas=10, T_pas=25000, T_pru=100000, base_pas=633100, base_pru=59200,
                         brazos=('moneda', 'neutra', 'cero')),
         'humo': dict(ind=[8], npas=2, T_pas=25000, T_pru=10000, base_pas=633100, base_pru=633183, brazos=('moneda', 'neutra', 'cero'),
                      npas_por_brazo={'cero': 1})}
SEM_ARNES = 633192
POOL_MAX = 2
# LA LETRA (PREREGISTRO sec. 6)
PURGA_UMB = 0.10; PURGA_N = 4; RAPIDO_N = 4; MITAD = 0.5; NEUTRA_MIN = 0.10   # auditoria H-1 (29-sep, antes de datos)
CONSERVA_UMB = 0.40; CONSERVA_N = 3; CERO_BANDA = (0.30, 0.70)


def h16(p): return hashlib.sha256(open(p, 'rb').read()).hexdigest()[:16]
def sem_pas(m, i, p): return m['base_pas'] + 10 * i + p
def sem_pru(m, i): return m['base_pru'] + i
def npas(m, b): return m.get('npas_por_brazo', {}).get(b, m['npas'])


def siembra0(brazo):
    """La siembra INYECTADA del pasaje 0: NSIE listas de una regla, intercaladas marcada / B."""
    a = BRAZOS[brazo][0]
    return [[list(a)] if k % 2 == 0 else [list(B)] for k in range(NSIE)]


def es_A(r): return int(r[0]) == 10 and int(r[1]) == 0 and r[2] > 0.5 and int(r[4]) == 0
def es_A_neg(r): return es_A(r) and r[5] < 0
def frac(S, pred=es_A): return round(sum(any(pred(r) for r in R) for R in S) / len(S), 4) if S else None


def tarea(seed, brazo, T, siembra):
    """UNA corrida: ES SM.tarea(seed, 'bq3', T, siembra) con cfg = CFG (moneda, neutra) o SM.CBP.tarea con CERO (cero)."""
    SM.registra()
    cfg = BRAZOS[brazo][1]
    if cfg is CFG: x = SM.tarea(seed, 'bq3', T, siembra)
    else: x = CBP.tarea(seed, 'V143_BQ3', T, cfg=dict(cfg), forzada=None, siembra=siembra)
    x['brazo'] = brazo; x['carro'] = 'V143_BQ3'
    return x


def _guarda(fin, x):
    tmp = fin + '.tmp'
    with open(tmp, 'w', encoding='utf-8') as fh: json.dump(x, fh, ensure_ascii=False)
    os.replace(tmp, fin)


def _ok_previo(fin):
    if not os.path.exists(fin): return None
    try:
        with open(fin, encoding='utf-8') as fh: x = json.load(fh)
    except Exception: return None
    return None if x.get('aborto') else x


def _corrida(fin, seed, brazo, T, siembra, extra):
    x = _ok_previo(fin)
    if x is not None: return x
    reint = os.path.exists(fin); t0 = time.time()
    try:
        x = tarea(seed, brazo, T, siembra); x['aborto'] = None
    except BaseException as e:   # noqa: nube-9
        x = dict(seed=seed, brazo=brazo, aborto=f"{type(e).__name__}: {e}"[:300], linajes=[])
    x.update(extra); x['T'] = T; x['seg_trabajo'] = round(time.time() - t0, 1); x['siembra_n'] = len(siembra)
    x['frac_A_entra'] = frac(siembra)
    if reint: x['reintento_de'] = 'aborto'
    _guarda(fin, x)
    return x


def trabajo(args):
    """UN trabajo = una cadena (brazo, indice): NPAS pasajes + (solo moneda) la prueba."""
    brazo, i, carpeta, modo = args
    m = MODOS[modo]; t0 = time.time(); fr = []; aborto = None; out = dict(brazo=brazo, i=i)
    try:
        SM.registra()   # carros y cfg fijados en CADA worker
        sb = siembra0(brazo); fr.append(frac(sb))
        for p in range(npas(m, brazo)):
            x = _corrida(os.path.join(carpeta, f"pasaje_{brazo}_i{i}_p{p}.json"), sem_pas(m, i, p), brazo, m['T_pas'], sb,
                         dict(i=i, p=p, tipo='pasaje'))
            if x.get('aborto'): aborto = f"pasaje {p}: {x['aborto']}"; break
            sb = CBP.siembra_de(x); fr.append(frac(sb))
            if not sb: aborto = f"pasaje {p}: siembra vacia"; break
        if aborto is None and BRAZOS[brazo][2]:
            x = _corrida(os.path.join(carpeta, f"{brazo}_s{sem_pru(m, i)}.json"), sem_pru(m, i), brazo, m['T_pru'], sb,
                         dict(i=i, tipo='prueba', siembra_final=sb))
            aborto = x.get('aborto'); L = x.get('linajes', [])
            out.update(cruzan=sum(int(l['cruza_real']) for l in L), R0=[l['R0_real'] for l in L])
        out.update(aborto=aborto, frac_A=fr)
    except BaseException as e:   # noqa: nube-9
        out.update(aborto=f"{type(e).__name__}: {e}"[:300], frac_A=fr)
    out['seg'] = round(time.time() - t0, 1)
    return out


# ------------------------------------------------------------------ lectura y LA LETRA
def _med(xs):
    xs = [x for x in xs if x is not None]; return round(float(st.median(xs)), 4) if xs else None


def cadena(carpeta, m, brazo, i):
    """Lee una cadena de sus JSON: fracciones por pasaje, arrastre, partos, vivos con A. None si falta o aborto."""
    sb = siembra0(brazo); f_ini = frac(sb); fr = []; fneg = []; arr = []; partos = []; vivos = []; conserva = True; ab = None
    gen0 = {json.dumps(r) for R in sb for r in [R]}
    for p in range(npas(m, brazo)):
        fin = os.path.join(carpeta, f"pasaje_{brazo}_i{i}_p{p}.json")
        if not os.path.exists(fin): return None, f"falta {os.path.basename(fin)}"
        x = json.load(open(fin, encoding='utf-8'))
        if x.get('aborto'): return None, f"{brazo} i{i} p{p}: {x['aborto']}"
        nb = min(int(x['bq']['cfg']['banco']), len(sb))
        sb = CBP.siembra_de(x); fr.append(frac(sb)); fneg.append(frac(sb, es_A_neg))
        tel = x['bq']['tel']; pp = [tel[k]['partos'] for k in sorted(tel)]; partos.append(sum(pp))
        arr.append(round(sum(max(0, nb - q) for q in pp) / max(1, len(sb)), 3))   # cota inferior de listas de la siembra que NO pasaron por un parto
        mu = [R for t in tel.values() for (_, R) in t['muestras']]
        vivos.append(frac(mu) if mu else None)
        conserva &= all(json.dumps(R) in gen0 for R in sb)
    return dict(f_ini=f_ini, f=fr, f_neg=fneg, arrastre=arr, partos=partos, vivos_A=vivos, solo_inyectadas=conserva,
                siembra_final=sb), ab


def fila_prueba(x):
    L = x['linajes']; cz = sum(int(l['cruza_real']) for l in L)
    return dict(seed=x['seed'], cruzan=cz, mayoria=int(cz * 2 > len(L)), R0_med=_med([l['R0_real'] for l in L]),
                fund_med=_med([l['fundadores'] for l in L]), desc=sum(l['descendientes'] for l in L),
                coherente=all(l.get('coherente', True) for l in L))


def carga(carpeta, modo):
    m = MODOS[modo]; C = {}; abortos = []; P_ = {'moneda': {}}; refs = {b: {} for b in REFS}; ref_ok = True; ref_txt = []
    for b in m['brazos']:
        C[b] = {}
        for i in m['ind']:
            c, ab = cadena(carpeta, m, b, i)
            if c is None: abortos.append(ab); continue
            C[b][i] = c
    for i in m['ind']:
        fin = os.path.join(carpeta, f"moneda_s{sem_pru(m, i)}.json")
        if not os.path.exists(fin): abortos.append(f"falta prueba moneda i{i}"); continue
        x = json.load(open(fin, encoding='utf-8'))
        if x.get('aborto'): abortos.append(f"prueba moneda i{i}: {x['aborto']}"); continue
        P_['moneda'][i] = fila_prueba(x)
    if modo == 'explora':
        for b, shas in REFS.items():
            for i, sh in zip(m['ind'], shas):
                fin = os.path.join(SMEXP, f"{b}_s{sem_pru(m, i)}.json"); s = h16(fin) if os.path.exists(fin) else None
                if s != sh: ref_ok = False; ref_txt.append(f"{b} s{sem_pru(m, i)} sha {s} != {sh}"); continue
                refs[b][i] = fila_prueba(json.load(open(fin, encoding='utf-8')))
    return C, P_, refs, abortos, ref_ok, ref_txt


def letra(C, ind, abortos, ref_ok, arnes_ok, n_pru=None):
    """PREREGISTRO sec. 6. C[brazo][i] = cadena. Devuelve validez, conteos y veredicto (PURGA / CONSERVA / INDETERMINADO / NO SE LEE)."""
    n = len(ind)
    fin = {b: {i: C[b][i]['f'][-1] for i in C.get(b, {})} for b in C}
    cero = [fin['cero'][i] for i in fin.get('cero', {})]
    val = dict(abortos_0=(len(abortos) == 0),
               completas=all(len(C.get(b, {})) == n for b in ('moneda', 'neutra', 'cero')) and (n_pru is None or n_pru == n),
               f_ini_05=all(c['f_ini'] == 0.5 for b in C for c in C[b].values()),
               cero_solo_inyectadas=all(c['solo_inyectadas'] for c in C.get('cero', {}).values()) and len(C.get('cero', {})) == n,
               cero_banda=(len(cero) == n and CERO_BANDA[0] <= st.mean(cero) <= CERO_BANDA[1]),
               refs_sha=bool(ref_ok), arnes=bool(arnes_ok))
    valido = all(val.values())
    I = [i for i in ind if i in fin.get('moneda', {}) and i in fin.get('neutra', {})]
    bajo = sum(1 for i in fin.get('moneda', {}) if fin['moneda'][i] < PURGA_UMB)
    rapido = sum(1 for i in I if fin['moneda'][i] < fin['neutra'][i])   # descriptivo (M3 firmada)
    mitad = sum(1 for i in I if fin['moneda'][i] <= MITAD * fin['neutra'][i])   # H-1b: moneda <= 0.5 neutra, pareado
    neu_med = _med(list(fin.get('neutra', {}).values()))   # H-1a: la neutra debe conservar algo (mediana p9 >= 0.10)
    alto = sum(1 for i in fin.get('moneda', {}) if fin['moneda'][i] >= CONSERVA_UMB)
    if not valido: ver = 'NO SE LEE'
    elif bajo >= PURGA_N and mitad >= RAPIDO_N and neu_med is not None and neu_med >= NEUTRA_MIN: ver = 'PURGA'
    elif alto >= CONSERVA_N: ver = 'CONSERVA'
    else: ver = 'INDETERMINADO'
    return dict(validez=val, veredicto=ver, moneda_bajo_010=bajo, moneda_mas_rapida_que_neutra=f"{rapido}/{len(I)}", moneda_le_mitad_neutra=f"{mitad}/{len(I)}", neutra_mediana_p9=neu_med,
                moneda_alto_040=alto, final={b: {str(i): v for i, v in d.items()} for b, d in fin.items()},
                cero_media=(round(st.mean(cero), 4) if cero else None))


def predicciones(C, P_, refs, L):
    fin = L['final']; mo = [v for v in fin.get('moneda', {}).values()]; ne = [v for v in fin.get('neutra', {}).values()]
    arr = [a for b in C for c in C[b].values() for a in c['arrastre']]
    cz = sum(f['cruzan'] for f in P_['moneda'].values()) if P_['moneda'] else None
    r = int(L['moneda_mas_rapida_que_neutra'].split('/')[0])
    return [('M1', 'neutra: mediana de la fraccion A en p9 en [0.05, 0.30]', _med(ne), _med(ne) is not None and 0.05 <= _med(ne) <= 0.30, 0.60),
            ('M2', 'moneda: mediana de la fraccion A en p9 en [0.00, 0.15]', _med(mo), _med(mo) is not None and _med(mo) <= 0.15, 0.60),
            ('M3', 'moneda cae mas rapido que neutra en >= 4/5 cadenas', L['moneda_mas_rapida_que_neutra'], r >= 4, 0.55),
            ('M4', 'veredicto PURGA', L['veredicto'], L['veredicto'] == 'PURGA', 0.45),
            ('M5', 'cero: media de p9 en [0.35, 0.65]', L['cero_media'], L['cero_media'] is not None and 0.35 <= L['cero_media'] <= 0.65, 0.80),
            ('M6', 'arrastre (cota inferior) mediano por pasaje en [0.55, 0.80]', _med(arr), _med(arr) is not None and 0.55 <= _med(arr) <= 0.80, 0.80),
            ('M7', 'prueba moneda: suma de cruzan (de 45) en [8, 22]', cz, cz is not None and 8 <= cz <= 22, 0.60),
            ('INV1', 'investigador 1 (junta Fable): veredicto PURGA', L['veredicto'], L['veredicto'] == 'PURGA', 0.60)]


def arnes_pasado():
    f = os.path.join(AQUI, 'identidad_moneda_salida.txt')
    if not os.path.exists(f): return False, 'sin salida del arnes'
    t = open(f, encoding='utf-8').read()
    need = [h16(os.path.abspath(__file__)), h16(os.path.join(AQUI, 'identidad_moneda.py'))]
    ok = 'ARNES: PASA' in t and all(s in t for s in need)
    return ok, ('PASA con los shas actuales' if ok else f'no PASA o no cita los shas actuales {need}')


def lee(carpeta, log=print, modo=None):
    modo = modo or ('humo' if os.path.basename(carpeta).startswith('humo') else 'explora')
    m = MODOS[modo]; C, P_, refs, abortos, ref_ok, ref_txt = carga(carpeta, modo)
    aok, atxt = arnes_pasado()
    L = letra(C, m['ind'], abortos, ref_ok, aok, n_pru=len(P_['moneda']))
    log(f"\n================ LECTURA moneda · {modo} · {carpeta}")
    log(f"  arnes: {atxt} · refs: {'sha OK' if ref_ok else ref_txt} · abortos: {abortos}")
    for b in m['brazos']:
        for i in sorted(C.get(b, {})):
            c = C[b][i]
            log(f"  {b:6s} i{i}: fraccion A  ini {c['f_ini']} -> p0..p{len(c['f'])-1} {c['f']}")
            log(f"  {'':6s}     A con w<0 {c['f_neg']} · vivos con A {c['vivos_A']}")
            log(f"  {'':6s}     arrastre>= {c['arrastre']} · partos {c['partos']} · solo inyectadas {c['solo_inyectadas']}")
    for i in sorted(P_['moneda']):
        f = P_['moneda'][i]; ex = ' · '.join(f"{b} {refs[b][i]['cruzan']}/9" for b in refs if i in refs[b])
        log(f"  prueba moneda i{i} s{f['seed']}: cruzan {f['cruzan']}/9 · mayoria {f['mayoria']} · R0 med {f['R0_med']} · fund med {f['fund_med']} "
            f"· descendientes {f['desc']} || guardados: {ex}")
    sumas = {'moneda': sum(f['cruzan'] for f in P_['moneda'].values())}
    sumas.update({b: sum(f['cruzan'] for f in refs[b].values()) for b in refs})
    log(f"  suma cruzan (de {9 * len(m['ind'])}): {sumas}")
    for k in ('validez', 'final', 'cero_media', 'moneda_bajo_010', 'moneda_mas_rapida_que_neutra', 'moneda_le_mitad_neutra', 'neutra_mediana_p9', 'moneda_alto_040'): log(f"  {k}: {L[k]}")
    pq = predicciones(C, P_, refs, L) if modo == 'explora' else []
    for q in pq: log(f"  {q[0]} {q[1]} (p {q[4]}): medido {q[2]} -> {'CUMPLE' if q[3] else 'REFUTADA'}")
    ver = ('HUMO (no cuenta; sin referencias, 2 pasajes): ' if modo == 'humo' else '') + L['veredicto']
    out = os.path.join(carpeta, 'lectura_moneda.json')
    json.dump(dict(modo=modo, letra=L, cadenas={b: {str(i): {k: v for k, v in c.items() if k != 'siembra_final'} for i, c in d.items()}
                                                 for b, d in C.items()},
                   prueba={str(i): f for i, f in P_['moneda'].items()}, refs={b: {str(i): f for i, f in d.items()} for b, d in refs.items()},
                   sumas=sumas, abortos=abortos, predicciones=[[q[0], q[1], q[2], bool(q[3]), q[4]] for q in pq], preregistro=PRERREGISTRO,
                   sha_runner=h16(os.path.abspath(__file__))), open(out, 'w', encoding='utf-8'), ensure_ascii=False, indent=1, default=str)
    log(f"  LECTURA {out}")
    log(f"VEREDICTO ({PRERREGISTRO} sec. 6): {ver}")
    return L


def verifica(log):
    ok = True
    for ruta, sha in SHAS.items():
        s = h16(ruta); ok &= s == sha; log(f"  sha {os.path.relpath(ruta, RAIZ)} {s} {'OK' if s == sha else '!= ' + sha + ' FALLA'}")
    log("  -- verifica de sentidos_muro (shas de pista, juez, corre_bp, V143_BQ2, TERMO; carros == construye_sm):")
    ok &= SM.verifica(lambda s: log('  ' + s))
    return ok


def main(argv=None):
    ap = argparse.ArgumentParser(allow_abbrev=False)
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument('--humo', action='store_true'); g.add_argument('--explora', action='store_true'); g.add_argument('--lee', default=None)
    ap.add_argument('--pool', type=int, default=0); ap.add_argument('--reanuda', action='store_true')
    a = ap.parse_args(argv)   # ERR-115
    if a.pool > POOL_MAX: raise SystemExit(f"--pool: maximo {POOL_MAX}")
    if a.humo and a.pool: raise SystemExit("--humo: sin Pool (un proceso)")
    if a.lee:
        c = a.lee if os.path.isabs(a.lee) else os.path.join(AQUI, a.lee)
        LOGF = open(os.path.join(c, 'lectura.txt'), 'w', encoding='utf-8')
        def log(s=''): print(s, flush=True); LOGF.write(s + '\n'); LOGF.flush()
        lee(c, log); return 0
    modo = 'humo' if a.humo else 'explora'
    m = MODOS[modo]; os.makedirs(DATOS, exist_ok=True)
    prev = sorted(d for d in os.listdir(DATOS) if d.startswith(modo + '_'))
    carpeta = os.path.join(DATOS, prev[-1] if (a.reanuda and prev) else time.strftime(f'{modo}_%Y%m%d_%H%M%S'))
    os.makedirs(carpeta, exist_ok=True)
    LOGF = open(os.path.join(carpeta, 'log.txt'), 'a', encoding='utf-8')
    def log(s=''): print(s, flush=True); LOGF.write(s + '\n'); LOGF.flush()
    t0 = time.time()
    log(f"CORRE_MONEDA · {modo} · {time.strftime('%Y-%m-%d %H:%M:%S')} · python {platform.python_version()} · pool {a.pool or 'NO'} · "
        f"runner {h16(os.path.abspath(__file__))} · {PRERREGISTRO} · indices {m['ind']} · npas {m['npas']} · T_pas {m['T_pas']} · T_pru {m['T_pru']} · "
        f"pasajes {sem_pas(m, m['ind'][0], 0)}.. · prueba {[sem_pru(m, i) for i in m['ind']]} · CFG {CFG} · CERO {CERO} · {carpeta}")
    if not verifica(log): log("  ALGO FALLA -> no se corre."); return 1
    if modo == 'explora':
        aok, atxt = arnes_pasado(); log(f"  arnes: {atxt}")
        if not aok: log("  el arnes no esta pasado con los shas actuales -> no se corre."); return 1
    tareas = [(b, i, carpeta, modo) for b in m['brazos'] for i in m['ind']]
    tareas.sort(key=lambda t: 0 if t[0] == 'moneda' else 1)   # las largas (con prueba) primero
    X = []

    def informa(x):
        X.append(x); log(f"  [{time.time()-t0:7.1f}s] {x['brazo']} i{x['i']} ({x['seg']}s) aborto {x['aborto']} · fraccion A {x.get('frac_A')} · "
                         f"cruzan {x.get('cruzan')}")
    if a.pool and a.pool > 1:
        from multiprocessing import Pool
        with Pool(a.pool) as PL:
            for x in PL.imap_unordered(trabajo, tareas): informa(x)
    else:
        for t in tareas: informa(trabajo(t))
    log(f"  {len(X)} trabajos · abortos {sum(1 for x in X if x['aborto'])} · {time.time()-t0:.1f}s")
    lee(carpeta, log, modo)
    return 0


if __name__ == '__main__':
    sys.exit(main())
