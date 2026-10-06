"""corre_o1_evo.py — RUNNER y LETRA del CONFIRMATORIO "O1 CON PERILLAS HEREDABLES" (o1_evo, parte A, 30-sep-2026).
Preregistro: PREREGISTRO_o1_evo.md (la letra esta AQUI, en lee_serie(), y alli en la sec. 6).

MISION: llegar a la AGI por este camino (organismo minimo con reglas locales, sin retropropagacion, peldanos preregistrados con
controles y replicas). Pregunta: ¿la seleccion por pasajes hace a O1 MEJOR que su disenador?

QUE SE CORRE (cada corrida ES experimentos/tronco_v14_3/corre_v143.tarea, que se IMPORTA y no se toca = juez.tarea(seed, 9 carros iguales,
T, pizarra 1, rep_acum 0, escala 1, mundo_n None, fundador_limpio 1) + juez.resumen_linaje; lo unico agregado es 'tel_ps', copia de SOLO
LECTURA de la telemetria del carro O1_PAS, y 'estado', las perillas fijadas en ESTE proceso):
  Por indice i (0..19) de una serie:
  CADENA o1pas: 10 pasajes de T 25 000 de O1_PAS (sigma 0.03); al final de cada pasaje la SIEMBRA del siguiente = genes de los VIVOS
                muestreados cada 1 000 pasos en los ultimos 5 000 pasos (siembra(): no ve R0, hijos ni cruza). Pasaje 0: SIEMBRA None
                (fundadores de FABRICA + mutacion). = pasg del termostato (reunion/opusB/corre_termostato.py), con los genes de O1.
  CADENA o1neu: LA MISMA cadena (mismas semillas, herencia, mutacion, muestreo y transferencia) con PS_LEE 0: los genes se heredan y
                derivan pero el cuerpo NO los lee (decide como O1 de fabrica): deriva acumulada sin seleccion sobre los genes.
  PRUEBA T 100 000 (semilla propia de i; PS_LEE 1 siempre): o1pas y o1neu (fundadores de la siembra FIJA del ultimo pasaje de SU cadena) · o1ctl (el MISMO carro y
                sigma, SIN transferencia: fundadores de FABRICA + mutacion) · o1 (O1 de fabrica) · termo (V143_TERMO) · v143 (V143).
  La cadena de o1ctl NO se corre (declarado en el preregistro, sec. 3): sin transferencia sus pasajes no tocan su prueba; el pasaje 0 de la
  cadena o1pas ES un pasaje de o1ctl (misma siembra None) y da el movimiento de genes dentro de un pasaje sin seleccion entre pasajes.
SEMILLAS (grep 30-sep: 617xxx no aparece en .py/.md; en .txt/.out/.json solo como digitos decimales o conteos, no semillas):
  serie:   pasaje p de la cadena i -> 617000 + 10 i + p (617000-617199); prueba T 100k de i -> 617201 + i (617201-617220)
  replica: pasaje p de la cadena i -> 617300 + 10 i + p (617300-617499); prueba T 100k de i -> 617501 + i (617501-617520)
  practica: 617900-617999 (arnes 617950-617989; humo 617990-617998).
nube-9: trabajo() atrapa TODO y devuelve 'aborto'; JSON por trabajo (y por pasaje) ANTES de volver (ERR-54); --reanuda salta lo hecho.
Cualquier aborto -> NO SE LEE.

Uso (ERR-115: banderas desconocidas o abreviadas ABORTAN; --serie/--replica SOLO el coordinador, con el preregistro, este runner, el
constructor y el carro COMMITEADOS y sin cambios respecto de HEAD):
  python experimentos/organelos/o1_evo/corre_o1_evo.py --humo                 # 1 proceso, 6 corridas (2 cadenas x 2 pasajes de 5k + o1ctl o1 de 20k), 60 000 pasos
  python experimentos/organelos/o1_evo/corre_o1_evo.py --humo --reanuda       # 2o proceso: 4 corridas (termo v143 o1pas o1neu, 80 000 pasos), salta lo escrito y lee
  python experimentos/organelos/o1_evo/corre_o1_evo.py --serie --pool 4       # 40 cadenas + 120 pruebas; se niega si ya hay veredicto
  python experimentos/organelos/o1_evo/corre_o1_evo.py --serie --pool 4 --reanuda
  python experimentos/organelos/o1_evo/corre_o1_evo.py --replica --pool 4     # solo si la serie da FUNCIONA, MODESTO o queda EN EL UMBRAL
  python experimentos/organelos/o1_evo/corre_o1_evo.py --lee <carpeta>
  python experimentos/organelos/o1_evo/corre_o1_evo.py --bloque <resumen serie>.json,<resumen replica>.json
"""
import argparse, copy, glob, hashlib, importlib.util, json, math, os, platform, statistics as st, subprocess, sys, time

try: sys.stdout.reconfigure(encoding='utf-8', errors='replace')
except Exception: pass
AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(AQUI)))
V143D = os.path.join(RAIZ, 'experimentos', 'tronco_v14_3')
PISTA = os.path.join(RAIZ, 'experimentos', 'carrera_escuderias')
for _d in (AQUI, V143D, PISTA):
    if _d not in sys.path: sys.path.insert(0, _d)
import corre_v143 as CV          # tarea (se IMPORTA, no se toca)
import construye_o1_pas as CB
P = CV.P; J = CV.J

PRERREGISTRO = 'PREREGISTRO_o1_evo.md'
DATOS = os.path.join(AQUI, 'datos')
O1PAS_PY = os.path.join(AQUI, 'carros', 'O1_PAS.py'); O1PAS0_PY = os.path.join(AQUI, 'carros', 'O1_PAS0.py')
TERMO_PY = os.path.join(RAIZ, 'experimentos', 'organelos', 'termo', 'carros', 'V143_TERMO.py')
SHAS = {os.path.join(V143D, 'corre_v143.py'): '24100621c450da22', os.path.join(V143D, 'carros_v143', 'V143.py'): '2a03048a7f1525e5',
        os.path.join(PISTA, 'pista.py'): '9f47c65e438e0ff4', os.path.join(PISTA, 'juez.py'): '6a68f640a7832f12',
        os.path.join(PISTA, 'carros', 'O1.py'): '99436afa2715f028', TERMO_PY: '3db639cab75641fb',
        os.path.join(AQUI, 'construye_o1_pas.py'): None, O1PAS_PY: None, O1PAS0_PY: None}   # None: se fijan abajo (SHAS_PROPIOS)
SHAS_PROPIOS = {'construye_o1_pas.py': '8013e4a99a004bda', 'O1_PAS.py': 'c5377ada6b28bee0', 'O1_PAS0.py': '940a70aeacb8581c'}
for _r in list(SHAS):
    if SHAS[_r] is None: SHAS[_r] = SHAS_PROPIOS[os.path.basename(_r)]
# brazo -> (carro, archivo propio o None, transfiere (tiene cadena), sigma, PS_LEE en su CADENA). En la PRUEBA, PS_LEE es siempre 1.
BRAZOS = {'o1pas': ('O1_PAS', O1PAS_PY, 1, 0.03, 1), 'o1neu': ('O1_PAS', O1PAS_PY, 1, 0.03, 0), 'o1ctl': ('O1_PAS', O1PAS_PY, 0, 0.03, None),
          'o1': ('O1', None, 0, None, None), 'termo': ('V143_TERMO', TERMO_PY, 0, None, None), 'v143': ('V143', None, 0, None, None)}
ORDEN = ('o1pas', 'o1neu', 'o1ctl', 'o1', 'termo', 'v143'); CAND = 'o1pas'; NEU = 'o1neu'; CTRL = 'o1ctl'; BASE = 'o1'
CADENAS = ('o1pas', 'o1neu')
GENES = CB.GENES; FABRICA = dict(zip(CB.GENES, CB.FABRICA))
BASES = {'serie': (617000, 617201), 'replica': (617300, 617501)}
N_IND = 20; NPAS = 10; T_PAS = 25000; T_PRU = 100000; VENT = 5000; POOL_MAX = 4
HUMO = dict(base=(617990, 617998), n=1, npas=2, T_pas=5000, T_pru=20000)   # proceso 1: 2 cadenas x 2 pasajes + o1ctl + o1; proceso 2: termo v143 o1pas o1neu
# ------------------------------------------------------------------ constantes de la LETRA (PREREGISTRO sec. 6), para n = 20 indices
GANA_PAR = 13          # PA / PC-par / PN-par: el candidato tiene MAS linajes que cruzan que el otro brazo en >= 13/20 indices (empates EN CONTRA)
DIF_SUMA = 10          # PB / PC-suma / PN-suma: suma de linajes que cruzan (de 180) del candidato >= la del otro + 10
O1_MAY = 16            # V2: O1 con mayoria que cruza (>= 5/9) en >= 16/20 (binomial, sec. 6)
ANCLA_V143 = (0.40, 0.80)   # V3: V143, mediana del R0 real (historico 0.536-0.634)


def h16(p): return hashlib.sha256(open(p, 'rb').read()).hexdigest()[:16]
def sem_pas(base, i, p): return base[0] + 10 * i + p
def sem_pru(base, i): return base[1] + i
def med(x):
    x = [v for v in x if v is not None]
    return round(float(st.median(x)), 4) if x else None
def esc(k, n): return math.ceil(k * n / 20 - 1e-9)   # umbral escalado (solo humo, que NO cuenta)


# ------------------------------------------------------------------ estado por proceso (cfg por worker)
def fija(brazo):
    """Carga en ESTE proceso (worker de Pool, --reanuda o arnes) la instancia del carro del brazo si falta (verifica su sha) y la registra en
    corre_v143._MODS. Devuelve el estado que se escribe en el JSON. Las perillas por corrida (SIEMBRA, PS_SEMILLA, PS_SIGMA) las fija tarea()."""
    n, ruta, tr, sg, _lee = BRAZOS[brazo]
    if ruta is None:
        CV.modulo(n); return dict(carro=n, sha=None, PASAJE=None)
    s = h16(ruta)
    if s != SHAS[ruta]: raise SystemExit(f"sha {ruta} {s} != {SHAS[ruta]}")
    m = CV._MODS.get(n)
    if m is None or os.path.abspath(m.__file__) != os.path.abspath(ruta):
        spec = importlib.util.spec_from_file_location(f"carro_{n}", ruta)
        m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); CV._MODS[n] = m
    if n == 'O1_PAS' and m.PASAJE != 1: raise SystemExit(f"{n}: PASAJE {m.PASAJE} != 1")
    return dict(carro=n, sha=s, PASAJE=getattr(m, 'PASAJE', None), transfiere=tr, sigma=sg)


def tarea(seed, brazo, T, siembra=None, sigma=None, lee=1):
    """corre_v143.tarea tal cual (regla 14) + 'tel_ps' (copia de _TEL de O1_PAS, solo lectura) + 'estado'.
    sigma None -> la del brazo. siembra y lee (PS_LEE: 0 = genes NEUTROS, se heredan pero no se leen) solo cuentan si el carro es O1_PAS."""
    est = fija(brazo)
    n = BRAZOS[brazo][0]; m = CV._MODS.get(n) if n == 'O1_PAS' else None
    sg = BRAZOS[brazo][3] if sigma is None else sigma
    cap = []; orig = P.run
    if m is not None:
        m.SIEMBRA = copy.deepcopy(siembra); m.PS_SEMILLA = int(seed); m.PS_SIGMA = float(sg); m.PS_LEE = int(lee)
        est.update(sigma=float(sg), siembra_n=len(siembra or []), lee=int(lee))

    def run2(*a, **k):
        if m is not None: m._TEL.clear(); m._PS_CNT.clear()
        r = orig(*a, **k)
        cap.append(copy.deepcopy({str(i): v for i, v in m._TEL.items()}) if m is not None else None)
        return r
    P.run = run2
    try:
        x = CV.tarea((seed, n, T))
    finally:
        P.run = orig
        if m is not None: m.SIEMBRA = None; m.PS_SEMILLA = 0; m.PS_SIGMA = 0.03; m.PS_LEE = 1
    x['tel_ps'] = cap[0] if cap else None; x['estado'] = est
    return x


def siembra(tel, T, vent=VENT):
    """SOLO de los VIVOS: tel = {indice: {'vivos': [[t, genes], ...]}} -> lista de genomas {gen: valor} de las muestras con t >= T - vent.
    No recibe (ni puede leer) R0, hijos, cruza ni nada del juez: la transferencia no usa fitness."""
    out = []
    for i in sorted(tel or {}, key=lambda z: int(z)):
        for t, g in (tel[i] or {}).get('vivos', []):
            if t >= T - vent: out.append({k: float(v) for k, v in zip(GENES, g)})
    return out or None


def genes_de(sie):
    if not sie: return None
    return {k: round(sum(s[k] for s in sie) / len(sie), 4) for k in GENES}


def genes_linaje(tel, n):
    """DESCRIPTIVO por linaje (indice 0..n-1): media de los genes de sus vivos muestreados en toda la corrida y los del ultimo vivo."""
    out = []
    for i in range(n):
        vv = [g for _, g in ((tel or {}).get(str(i)) or {}).get('vivos', [])]
        out.append(None if not vv else dict(media={k: round(sum(g[j] for g in vv) / len(vv), 4) for j, k in enumerate(GENES)},
                                             ultimo={k: round(vv[-1][j], 4) for j, k in enumerate(GENES)}))
    return out


def fila(x, T):
    L = x['linajes']; tel = x.get('tel_ps') or {}
    fp = [f for v in tel.values() for f in (v or {}).get('fund', [])]
    return dict(seed=x['seed'], T=T, R0_real=[l['R0_real'] for l in L], R0_med=med([l['R0_real'] for l in L]),
                fund=[l['fundadores'] for l in L], fund_post10k=[l['fund_post10k'] for l in L], cruza=[int(l['cruza_real']) for l in L],
                cruzan=sum(int(l['cruza_real']) for l in L), mayoria=int(sum(int(l['cruza_real']) for l in L) * 2 > len(L)),
                coherente=all(l.get('coherente', True) for l in L), nac_reales=[l.get('nac_reales') for l in L],
                fund_de_siembra=sum(f[0] for f in fp), fund_n=len(fp), partos_tel=sum((v or {}).get('partos', 0) for v in tel.values()),
                genes_vivos_fin=genes_de(siembra(tel, T, vent=1000)), genes_linaje=genes_linaje(tel, len(L)), mundo_AC=round(x['pista']['comp_mundo']['A'] + x['pista']['comp_mundo']['C'], 4),
                estado=x.get('estado'), seg=x.get('seg'))


def cadena(i, base, npas, T, carpeta, reanuda, log=None, brazo='o1pas'):
    """Cadena de o1pas (genes que se LEEN) u o1neu (genes NEUTROS: PS_LEE 0; misma herencia, mutacion, muestreo y transferencia): npas
    pasajes con las MISMAS semillas; JSON por pasaje (reanudable). Devuelve dict(pasajes=[fila + genes de la siembra], siembra_final)."""
    sie = None; F = []; lee = BRAZOS[brazo][4]
    for p in range(npas):
        fin = os.path.join(carpeta, f"pasaje_i{i:02d}_{brazo}_p{p:02d}.json")
        if reanuda and os.path.exists(fin):
            with open(fin, encoding='utf-8') as fh: d = json.load(fh)
        else:
            x = tarea(sem_pas(base, i, p), brazo, T, siembra=sie, lee=lee)
            sig = siembra(x['tel_ps'], T)
            f = fila(x, T); f['p'] = p; f['sembrado'] = int(sie is not None); f['genes_siembra'] = genes_de(sig); f['n_siembra'] = len(sig or [])
            d = dict(fila=f, siembra_sig=sig)
            tmp = fin + '.tmp'
            with open(tmp, 'w', encoding='utf-8') as fh: json.dump(d, fh, ensure_ascii=False)
            os.replace(tmp, fin)
        F.append(d['fila']); sie = d['siembra_sig']
        if log: log(f"    cadena i{i} p{p} s{d['fila']['seed']} cruzan {d['fila']['cruzan']}/9 fund {d['fila']['fund']} genes siembra {d['fila']['genes_siembra']}")
        if not sie: raise RuntimeError(f"pasaje {p}: siembra vacia (no hay vivos muestreados)")
    return dict(pasajes=F, siembra_final=sie)


def trabajo(args):
    """UN trabajo: ('cadena', i, 'o1pas'|'o1neu') o ('prueba', i, brazo). Atrapa TODO (nube-9); escribe su JSON antes de volver (ERR-54); con
    reanuda salta el que ya existe SIN aborto (un aborto guardado se reintenta y queda anotado en 'reintento_de')."""
    tipo, i, brazo, base, npas, T_pas, T_pru, carpeta, reanuda = args
    fin = os.path.join(carpeta, f"{tipo}_i{i:02d}_{brazo}.json"); previo = None
    if reanuda and os.path.exists(fin):
        with open(fin, encoding='utf-8') as fh: x0 = json.load(fh)
        if not x0.get('aborto'): return x0
        previo = x0['aborto']
    t0 = time.time()
    try:
        if tipo == 'cadena':
            x = dict(tipo=tipo, i=i, brazo=brazo, aborto=None, **cadena(i, base, npas, T_pas, carpeta, reanuda, brazo=brazo))
        else:
            sie = None
            if BRAZOS[brazo][2]:
                with open(os.path.join(carpeta, f"cadena_i{i:02d}_{brazo}.json"), encoding='utf-8') as fh: c = json.load(fh)
                if c.get('aborto') or not c.get('siembra_final'): raise RuntimeError("cadena sin siembra final")
                sie = c['siembra_final']
            y = tarea(sem_pru(base, i), brazo, T_pru, siembra=sie, lee=1)   # en la PRUEBA los genes se leen siempre
            x = dict(tipo=tipo, i=i, brazo=brazo, aborto=None, genes_siembra_usada=genes_de(sie), **fila(y, T_pru))
    except BaseException as e:   # noqa: nube-9
        x = dict(tipo=tipo, i=i, brazo=brazo, aborto=f"{type(e).__name__}: {e}"[:300])
    if previo: x['reintento_de'] = previo
    x['seg'] = round(time.time() - t0, 1)
    tmp = fin + '.tmp'
    with open(tmp, 'w', encoding='utf-8') as fh: json.dump(x, fh, ensure_ascii=False)
    os.replace(tmp, fin)
    return x


# ------------------------------------------------------------------ LA LETRA (PREREGISTRO_o1_evo.md sec. 6 y seccion de cambios por auditoria)
def par(A, B, I):
    """Pareado por indice en LINAJES QUE CRUZAN (0-9). gana = indices con A > B (empates EN CONTRA)."""
    a = [A[i]['cruzan'] for i in I]; b = [B[i]['cruzan'] for i in I]
    return dict(n=len(I), gana=sum(x > y for x, y in zip(a, b)), empata=sum(x == y for x, y in zip(a, b)), pierde=sum(x < y for x, y in zip(a, b)),
                suma_a=sum(a), suma_b=sum(b), dif=sum(a) - sum(b), por_indice_a=a, por_indice_b=b)


def lee_serie(C, R, n, abortos):
    """C[brazo][i] = cadena (o1pas, o1neu); R[brazo][i] = prueba T 100k. n = indices esperados (20 en serie/replica)."""
    I = list(range(n)); gp = esc(GANA_PAR, n); dsu = math.ceil(DIF_SUMA * n / 20 - 1e-9); o1m = esc(O1_MAY, n)
    completo = all(len(C.get(b, {})) == n for b in CADENAS) and all(len(R.get(b, {})) == n for b in ORDEN)
    v = {}
    v['V1_completa'] = bool(abortos == 0 and completo and all(R[b][i]['coherente'] for b in ORDEN for i in R.get(b, {})))
    v['V2_ancla_o1'] = sum(R['o1'][i]['mayoria'] for i in R.get('o1', {})) >= o1m
    m = med([R['v143'][i]['R0_med'] for i in R.get('v143', {})])
    v['V3_ancla_v143'] = m is not None and ANCLA_V143[0] <= m <= ANCLA_V143[1]
    v['V4_siembra_actua'] = all(bool(R.get(b)) and all(R[b][i]['fund_n'] > 0 and R[b][i]['fund_de_siembra'] == R[b][i]['fund_n'] for i in R[b])
                                for b in CADENAS) \
        and bool(R.get(CTRL)) and all(R[CTRL][i]['fund_n'] > 0 and R[CTRL][i]['fund_de_siembra'] == 0 for i in R[CTRL])
    est = lambda d: d.get('estado') or {}
    v['V5_perillas'] = all(est(R[b][i]).get('carro') == BRAZOS[b][0] for b in ORDEN for i in R.get(b, {})) \
        and all(est(R[b][i]).get('sigma') == BRAZOS[b][3] and est(R[b][i]).get('lee') == 1 for b in (CAND, NEU, CTRL) for i in R.get(b, {})) \
        and all(est(q).get('lee') == BRAZOS[b][4] and est(q).get('sigma') == BRAZOS[b][3] for b in CADENAS for i in C.get(b, {}) for q in C[b][i]['pasajes'])
    valido = all(v.values())
    ok = valido or completo
    pb = par(R[CAND], R[BASE], I) if ok else None; pc = par(R[CAND], R[CTRL], I) if ok else None; pn = par(R[CAND], R[NEU], I) if ok else None
    p = {}
    if ok:
        p['PA_par_o1'] = pb['gana'] >= gp
        p['PB_suma_o1'] = pb['dif'] >= dsu
        p['PC_par_ctl'] = pc['gana'] >= gp
        p['PC_suma_ctl'] = pc['dif'] >= dsu
        p['PN_par_neu'] = pn['gana'] >= gp
        p['PN_suma_neu'] = pn['dif'] >= dsu
    umbral = bool(ok and any(abs(q['gana'] - gp) <= 1 or abs(q['dif'] - dsu) <= 1 for q in (pb, pc, pn)))
    matiz = None
    if not valido: ver = 'NO SE LEE'
    elif all(p.values()): ver = 'FUNCIONA'
    elif (p['PA_par_o1'] or p['PB_suma_o1']) and (p['PC_par_ctl'] or p['PC_suma_ctl']):
        ver = 'HAY ALGO MODESTO'
        # PA, PB y PC completos pero PN no (o PN a medias): gana a o1 y a o1ctl pero no se separa de la deriva neutra acumulada
        matiz = 'seleccion parcial' if (p['PN_par_neu'] and p['PN_suma_neu']) else 'transferencia, no seleccion'
    else: ver = 'NO'
    # ---------------- descriptivo (NO decide)
    desc = {}
    if ok:
        desc['pareados'] = {f"{a}_vs_{b}": par(R[a], R[b], I) for a, b in (('o1pas', 'o1'), ('o1pas', 'o1ctl'), ('o1pas', 'o1neu'), ('o1neu', 'o1'),
                                                                           ('o1neu', 'o1ctl'), ('o1ctl', 'o1'), ('o1pas', 'termo'), ('termo', 'v143'), ('o1', 'v143'))}
        desc['suma_cruzan'] = {b: sum(R[b][i]['cruzan'] for i in I) for b in ORDEN}
        desc['mayorias'] = {b: sum(R[b][i]['mayoria'] for i in I) for b in ORDEN}
        desc['R0_med'] = {b: med([R[b][i]['R0_med'] for i in I]) for b in ORDEN}
        desc['fund_por_linaje_media'] = {b: med([st.mean(R[b][i]['fund']) for i in I]) for b in ORDEN}
        desc['fund_por_linaje_mediana'] = {b: med([med(R[b][i]['fund']) for i in I]) for b in ORDEN}
        desc['establecidos_0fund_post10k'] = {b: sum(sum(int(z == 0) for z in R[b][i]['fund_post10k']) for i in I) for b in ORDEN}
        fp = [(st.mean(R[CAND][i]['fund']), st.mean(R[BASE][i]['fund'])) for i in I]
        desc['fund_o1pas_menos_que_o1'] = sum(a < b for a, b in fp)
        desc['mundo_AC'] = {b: med([R[b][i]['mundo_AC'] for i in I]) for b in ORDEN}
        desc['genes_vivos_fin_prueba'] = {b: {k: med([(R[b][i]['genes_vivos_fin'] or {}).get(k) for i in I]) for k in GENES} for b in (CAND, NEU, CTRL)}
        # genes POR LINAJE cruzados con el establecimiento de la prueba (fund_post10k == 0): mediana de la media de genes del linaje
        gl = {}
        for b in (CAND, NEU, CTRL):
            pares = [(g, f) for i in I for g, f in zip(R[b][i].get('genes_linaje') or [], R[b][i]['fund_post10k']) if g]
            e_ = [g['media'] for g, f in pares if f == 0]; n_ = [g['media'] for g, f in pares if f > 0]
            gl[b] = dict(n_establecidos=len(e_), n_no=len(n_), establecidos={k: med([g[k] for g in e_]) for k in GENES},
                         no_establecidos={k: med([g[k] for g in n_]) for k in GENES})
        desc['genes_linaje_vs_establecimiento'] = gl
    for b in CADENAS:
        Cb = C.get(b, {})
        if not Cb: continue
        np_ = max(len(Cb[i]['pasajes']) for i in Cb)
        tray = {k: [med([Cb[i]['pasajes'][q]['genes_siembra'][k] for i in Cb if len(Cb[i]['pasajes']) > q and Cb[i]['pasajes'][q]['genes_siembra']])
                    for q in range(np_)] for k in GENES}
        ult = {i: Cb[i]['pasajes'][-1]['genes_siembra'] for i in Cb}
        desc[f'{b}_trayectoria_genes_siembra_mediana_por_pasaje'] = tray
        desc[f'{b}_genes_siembra_ultimo_por_cadena'] = ult
        desc[f'{b}_desplazamiento_ultimo_vs_fabrica'] = {k: dict(med=med([ult[i][k] - FABRICA[k] for i in ult if ult[i]]),
                                                                 med_abs=med([abs(ult[i][k] - FABRICA[k]) for i in ult if ult[i]]),
                                                                 sube=sum(1 for i in ult if ult[i] and ult[i][k] > FABRICA[k]),
                                                                 baja=sum(1 for i in ult if ult[i] and ult[i][k] < FABRICA[k])) for k in GENES}
        desc[f'{b}_cadena_cruzan_por_pasaje_mediana'] = [med([Cb[i]['pasajes'][q]['cruzan'] for i in Cb if len(Cb[i]['pasajes']) > q]) for q in range(np_)]
        desc[f'{b}_cadena_fund_por_linaje_por_pasaje'] = [med([st.mean(Cb[i]['pasajes'][q]['fund']) for i in Cb if len(Cb[i]['pasajes']) > q]) for q in range(np_)]
    return dict(validez=v, puertas=p, veredicto=ver, matiz=matiz, en_umbral=umbral, umbrales=dict(gana_par=gp, dif_suma=dsu, o1_may=o1m),
                pareado_o1=pb, pareado_ctl=pc, pareado_neu=pn, descriptivo=desc)


ORD_V = {'NO SE LEE': -1, 'NO': 0, 'HAY ALGO MODESTO': 1, 'FUNCIONA': 2}
def bloque(a, b): return a if a == b else min((a, b), key=lambda z: ORD_V[z])


def carga(carpeta):
    C = {b: {} for b in CADENAS}; R = {b: {} for b in ORDEN}; ab = []
    for f in sorted(glob.glob(os.path.join(carpeta, 'cadena_i*_*.json')) + glob.glob(os.path.join(carpeta, 'prueba_i*_*.json'))):
        d = json.load(open(f, encoding='utf-8'))
        if d.get('aborto'): ab.append(f"{d['tipo']} i{d['i']} {d['brazo']}: {d['aborto']}"); continue
        if d['tipo'] == 'cadena': C[d['brazo']][d['i']] = d
        else: R[d['brazo']][d['i']] = d
    return C, R, ab


def imprime(L, log):
    log(f"  validez: {L['validez']}")
    log(f"  puertas: {L['puertas']} · umbrales {L['umbrales']} · EN EL UMBRAL (+-1): {L['en_umbral']} · matiz {L['matiz']}")
    for k in ('pareado_o1', 'pareado_ctl', 'pareado_neu'):
        q = L[k]
        if q: log(f"  {k}: gana {q['gana']} empata {q['empata']} pierde {q['pierde']} · suma {q['suma_a']} vs {q['suma_b']} (dif {q['dif']})")
    for k, v in L['descriptivo'].items():
        if 'ultimo_por_cadena' not in k: log(f"  [desc] {k}: {v}")


# ------------------------------------------------------------------ verificaciones y candados
def verifica(log):
    ok = True
    for ruta, sha in SHAS.items():
        s = h16(ruta); ok &= s == sha; log(f"  sha {os.path.relpath(ruta, RAIZ)} {s} {'OK' if s == sha else '!= ' + sha + ' FALLA'}")
    for nm, b in CB.todas().items():
        igual = open(os.path.join(AQUI, 'carros', nm + '.py'), 'rb').read() == b; ok &= igual
        log(f"  carro {nm} == construye_o1_pas: {igual}")
    return ok


def identidad_corta(log, seed=617950, T=1500):
    fija('o1pas'); m = CV._MODS['O1_PAS']
    spec = importlib.util.spec_from_file_location('carro_O1_PAS0', O1PAS0_PY); m0 = importlib.util.module_from_spec(spec); spec.loader.exec_module(m0)
    o1 = CV.modulo('O1')
    run = lambda mod: json.loads(json.dumps(P.run(seed, [('X', mod)] * 9, T=T, pizarra=1, rep_acum=0, escala=1, mundo_n=None, fundador_limpio=1), default=str))
    base = run(o1); i0 = run(m0) == base
    try:
        m.SIEMBRA = None; m.PS_SEMILLA = seed; m.PS_SIGMA = 0.0; m._TEL.clear(); m._PS_CNT.clear(); i1 = run(m) == base
        m.SIEMBRA = [dict(FABRICA)] * 3; m._TEL.clear(); m._PS_CNT.clear(); i2 = run(m) == base
    finally:
        m.SIEMBRA = None; m.PS_SEMILLA = 0; m.PS_SIGMA = 0.03
    log(f"  IDENTIDAD CORTA (salida ENTERA, N 9, s {seed}, T {T}, fundador limpio): O1_PAS0 == O1 {i0} · O1_PAS sigma 0 sin siembra == O1 {i1} · "
        f"O1_PAS sigma 0 con siembra de fabrica == O1 {i2}")
    return i0 and i1 and i2


def git_limpio(rutas, log):
    """--serie/--replica: preregistro, runner, constructor y carro COMMITEADOS y sin cambios respecto de HEAD."""
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
    """Candados. Si ya hay un resumen.json (no humo) de esta serie/replica con veredicto: se niega siempre. Si hay carpetas previas
    (cortadas o NO SE LEE): solo --reanuda. Devuelve None si se puede correr, o el motivo."""
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
    if a.pool < 0 or a.pool > POOL_MAX: raise SystemExit(f"--pool entre 0 y {POOL_MAX} (contrato del encargo)")
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
        L = lee_serie(C, R, n, len(ab)); imprime(L, print)
        print(f"VEREDICTO ({'HUMO/parcial, no cuenta' if n != N_IND else 'letra'}): {L['veredicto']} (matiz {L.get('matiz')}) · en el umbral {L['en_umbral']} · abortos {ab}")
        return 0
    if a.humo:
        if a.pool: raise SystemExit("--humo: sin Pool (un proceso)")
        modo = 'humo'; base = HUMO['base']; n = HUMO['n']; npas = HUMO['npas']; Tp = HUMO['T_pas']; Tr = HUMO['T_pru']
        f1 = [('cadena', 0, 'o1pas'), ('cadena', 0, 'o1neu'), ('prueba', 0, 'o1ctl'), ('prueba', 0, 'o1')]   # 2x2 pasajes + 2 = 6 corridas
        f2 = []
        if a.reanuda:   # 2o proceso: 4 corridas (termo, v143, o1pas, o1neu); lo ya escrito se salta
            f1 += [('prueba', 0, 'termo'), ('prueba', 0, 'v143')]; f2 = [('prueba', 0, 'o1pas'), ('prueba', 0, 'o1neu')]
        pre = 'humo'; dest = os.path.join(DATOS, 'humo')
    else:
        modo = 'serie' if a.serie else 'replica'; base = BASES[modo]; n = N_IND; npas = NPAS; Tp = T_PAS; Tr = T_PRU
        f1 = [('cadena', i, b) for i in range(n) for b in CADENAS] + [('prueba', i, b) for i in range(n) for b in ORDEN if not BRAZOS[b][2]]
        f2 = [('prueba', i, b) for i in range(n) for b in CADENAS]
        pre = f"{modo}_i{sem_pru(base, 0)}-{sem_pru(base, n - 1)}"; dest = DATOS
    sel = time.strftime('%Y%m%d_%H%M%S')
    prev = sorted(d for d in os.listdir(dest) if d.startswith(pre + '_') and os.path.isdir(os.path.join(dest, d))) if os.path.isdir(dest) else []
    if a.reanuda and not prev: raise SystemExit(f"--reanuda: no hay carpeta {pre}_* en {dest}")
    carpeta = os.path.join(dest, prev[-1]) if (a.reanuda and prev) else os.path.join(dest, pre + '_' + sel)
    BUF = []; LOGF = [None]   # la carpeta se crea SOLO si todas las verificaciones pasan

    def log(s=''):
        s = f"[{time.strftime('%H:%M:%S')}] {s}"
        print(s, flush=True)
        if LOGF[0] is None: BUF.append(s)
        else: LOGF[0].write(s + '\n'); LOGF[0].flush()
    t0 = time.time()
    shp = h16(os.path.join(AQUI, PRERREGISTRO)) if os.path.exists(os.path.join(AQUI, PRERREGISTRO)) else 'NO EXISTE'
    log(f"CORRE_O1_EVO · {modo} · {sel} · python {platform.python_version()} · pool {a.pool or 'NO (un proceso)'} · corre_o1_evo.py "
        f"{h16(os.path.abspath(__file__))} · preregistro {PRERREGISTRO} {shp} · carpeta {carpeta}")
    log(f"  pasajes {sem_pas(base, 0, 0)}-{sem_pas(base, n - 1, npas - 1)} (T {Tp} x {npas}) · pruebas {sem_pru(base, 0)}-{sem_pru(base, n - 1)} (T {Tr}) · "
        f"brazos {list(ORDEN)} · reanuda {a.reanuda}")
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
        ok &= git_limpio([os.path.join(AQUI, PRERREGISTRO), os.path.abspath(__file__), os.path.join(AQUI, 'construye_o1_pas.py'), O1PAS_PY], log)
    if not ok: log("  ALGO FALLA -> no se corre (no se crea carpeta)."); return 1
    os.makedirs(carpeta, exist_ok=True)
    LOGF[0] = open(os.path.join(carpeta, 'log.txt'), 'a', encoding='utf-8'); LOGF[0].write('\n'.join(BUF) + '\n'); LOGF[0].flush()
    mk = lambda t: (t[0], t[1], t[2], base, npas, Tp, Tr, carpeta, a.reanuda)
    X = []

    def fmt(x):
        if x['tipo'] == 'cadena':
            return (f"  [{time.time()-t0:7.1f}s] cadena i{x['i']} {x['brazo']} ({x['seg']}s) aborto {x['aborto']} cruzan por pasaje "
                    f"{[q['cruzan'] for q in x.get('pasajes', [])]} genes p-ultimo {(x.get('pasajes') or [{}])[-1].get('genes_siembra')}")
        return (f"  [{time.time()-t0:7.1f}s] prueba i{x['i']} {x['brazo']:5s} ({x['seg']}s) aborto {x['aborto']} cruzan {x.get('cruzan')}/9 "
                f"fund {x.get('fund')} de siembra {x.get('fund_de_siembra')}/{x.get('fund_n')}")
    if a.pool and a.pool > 1:
        from multiprocessing import Pool
        with Pool(a.pool) as PL:
            pend = {PL.apply_async(trabajo, (mk(t),)): t for t in f1}
            while pend:
                listos = [r for r in pend if r.ready()]
                if not listos: time.sleep(2); continue
                for r in listos:
                    t = pend.pop(r); x = r.get(); X.append(x); log(fmt(x))
                    if t[0] == 'cadena':   # su prueba (o1pas u o1neu) entra a la cola en cuanto la cadena termina
                        pend[PL.apply_async(trabajo, (mk(('prueba', t[1], t[2])),))] = ('prueba', t[1], t[2])
    else:
        for t in f1 + f2:
            x = trabajo(mk(t)); X.append(x); log(fmt(x))
    C, R, ab = carga(carpeta)
    if a.humo and not a.reanuda:
        log(f"\n  HUMO parte 1: {len(X)} trabajos (2 cadenas de {npas} pasajes + 2 pruebas = {2 * npas + 2} corridas) · faltan termo, v143, o1pas, o1neu (--humo --reanuda) · {time.time()-t0:.1f}s")
    L = lee_serie(C, R, n, len(ab))
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
