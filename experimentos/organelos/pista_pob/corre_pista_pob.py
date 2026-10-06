"""corre_pista_pob.py — PISTA_POB (29-sep-2026, creador; EXPLORATORIO con puerta hacia serie). Preregistro: PREREGISTRO_pista_pob.md.

MISION: llegar a la AGI por este camino (organismo minimo con reglas locales, sin retropropagacion, peldanos preregistrados con
controles y replicas). Principio del director: que la seleccion construya el organo, no nosotros.

TRABAJO (por indice j = 1..5 y brazo):
  1. CAMARA (fuera de la medida): pista_pob.run(semilla 59800 + j, K = 8 copias de la pista vieja, carro V143_BQ2 SIN cambios,
     tasas BQ_C de la ronda 2 = corre_bp.CFG0, T_evo = 50 000, modo sel | neutro). Salida: siembra = por linaje 50 listas al azar de
     las fotos (deposito + vivos) cada 1000 pasos en los ultimos 5000. Se escribe evo_<brazo>_i<j>.json ANTES de seguir (ERR-54).
  2. MEDIDA OFICIAL (la pista vieja, el juez, fundador limpio, letra ENMIENDA 5, T 100 000): corre_bp.tarea(59200 + j, 'bloq2', T,
     siembra=siembra) -- la MISMA funcion (importada, no copiada) que hizo bloq_pas / bloq2 en bloques_pista, en las semillas de prueba
     59201-59205, PAREADA con sus JSON (termo, bloq2, bloq2aza, bloq_pas, o1). Se escribe <brazo>_s<59200+j>.json.
  REFERENCIA nueva: v143 (V143 via corre_bp.tarea) en 59201-59205, T 100 000 (validez: R0 real mediano en [0.40, 0.80]).
MEDIDA PRINCIPAL: linajes que cruzan (cruza_real, ENMIENDA 5) de 9 por indice; R0 real mediano al lado. Veredicto: lee() (codigo).
nube-9: trabajo() atrapa TODO y devuelve/escribe un resultado marcado 'aborto'. Cualquier aborto -> NO APLICA.

  python experimentos/organelos/pista_pob/corre_pista_pob.py --humo                              # 1 proceso: 1 indice, K 8, T_evo 3000
  python experimentos/organelos/pista_pob/corre_pista_pob.py --explora --pool 6                  # SOLO el coordinador (15 trabajos)
  python experimentos/organelos/pista_pob/corre_pista_pob.py --explora --pool 6 --reanuda   # reintenta tambien los abortos guardados
  python experimentos/organelos/pista_pob/corre_pista_pob.py --humo --reanuda --carpeta datos/humo_<sello>   # prueba de --reanuda
  python experimentos/organelos/pista_pob/corre_pista_pob.py --lee datos/explora
(ERR-115: banderas desconocidas o abreviadas abortan.)
"""
import argparse, copy, hashlib, json, os, statistics as st, sys, time, traceback

try: sys.stdout.reconfigure(encoding='utf-8', errors='replace')
except Exception: pass
AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(AQUI)))
PISTAD = os.path.join(RAIZ, 'experimentos', 'carrera_escuderias')
BPD = os.path.join(RAIZ, 'experimentos', 'organelos', 'bloques_pista')
TERMOD = os.path.join(RAIZ, 'experimentos', 'organelos', 'termo')
for _d in (PISTAD, BPD):
    if _d not in sys.path: sys.path.insert(0, _d)
import corre_bp as CB      # tarea (la medida), prepara, CFG0 (se IMPORTA, no se toca)
import pista_pob as PP
J = CB.CV.J; P = CB.P

CARRO_BQ2 = os.path.join(BPD, 'carros', 'V143_BQ2.py')
SHAS = {os.path.join(PISTAD, 'pista.py'): '9f47c65e438e0ff4', os.path.join(PISTAD, 'juez.py'): '6a68f640a7832f12',
        os.path.join(PISTAD, 'revisa_carro.py'): '1c8a789f7427ab96', os.path.join(PISTAD, 'carros', 'O1.py'): '99436afa2715f028',
        CARRO_BQ2: '183fb81cf6ad520c', os.path.join(BPD, 'corre_bp.py'): '6b9c11a6639d3948',
        os.path.join(TERMOD, 'corre_termo.py'): '66f1f2539f1030ef', os.path.join(TERMOD, 'carros', 'V143_TERMO.py'): '3db639cab75641fb',
        os.path.join(RAIZ, 'experimentos', 'tronco_v14_3', 'carros_v143', 'V143.py'): '2a03048a7f1525e5',
        os.path.join(RAIZ, 'experimentos', 'tronco_v14_3', 'corre_v143.py'): '24100621c450da22',
        os.path.join(PISTAD, 'pista_pob.py'): 'd4ed07b28e4ba94b'}
SHA_RUN_GEN = '7b05c9615ee40483'   # fuente transformada por ANCLAS (pista_pob.construye_run_gen)
DATOS = os.path.join(AQUI, 'datos')
REFS = os.path.join(BPD, 'datos', 'explora_T100000')
REF_BRAZOS = ('termo', 'bloq2', 'bloq2aza', 'bloq_pas', 'o1')
SALIDA_ARNES = os.path.join(AQUI, 'identidad_pista_pob_salida.txt')
K_DEF = 8; T_EVO = 50000; T_PRUEBA = 100000
INDICES = (1, 2, 3, 4, 5)
def sem_evo(j): return 59800 + j            # grep 29-sep: 598xx libre en py/md/txt (solo aparece 59801 como numero de un log)
def sem_prueba(j): return 59200 + j         # = las de bloques_pista (pareado)
HUMO = dict(evo=59891, prueba=59891, K=8, T_evo=3000, T=10000)
BRAZOS = ('pob_sel', 'pob_neutro')
MODO = {'pob_sel': 'sel', 'pob_neutro': 'neutro'}
ANCLA_V143 = (0.40, 0.80)
CFG = {}


def h16(p): return hashlib.sha256(open(p, 'rb').read()).hexdigest()[:16]


def verifica(log=print):
    ok = True
    for p, s in SHAS.items():
        h = h16(p); ok &= (h == s)
        log(f"  sha {os.path.relpath(p, RAIZ)} {h} {'OK' if h == s else 'DISTINTO (fijado ' + s + ')'}")
    _, info = PP.construye_run_gen()
    ok &= info['sha_fuente_transformada'] == SHA_RUN_GEN
    log(f"  run_gen por anclas: {info} {'OK' if info['sha_fuente_transformada'] == SHA_RUN_GEN else 'DISTINTO'}")
    return ok


def cfg():
    if not CFG:
        CB._cfg_carro(); CFG.update(CB.CFG0)
        m = PP.carga_modulo(CARRO_BQ2, 'carro_V143_BQ2_cfg')
        if dict(m.BQ_C) != CFG: raise SystemExit(f"BQ_C del carro {m.BQ_C} != CFG0 de corre_bp {CFG}")
    return dict(CFG)


def prepara_bq(m, c, sc):
    """= corre_bp.prepara sin siembra (la de la ronda 2), sobre el modulo PROPIO de la copia."""
    m._BQ_BANCO.clear(); m._BQ_CNT.clear(); m._BQ_TEL.clear(); m.BQ_SEMILLA = int(sc); m.BQ_FORZADA = None
    m.BQ_C = cfg()


def evoluciona(seed, modo, K, T_evo, log=None):
    r = PP.run(seed, K, CARRO_BQ2, T_evo, modo=modo, ident='V143_BQ2', prepara=prepara_bq, ref_vivo=PP.ref_reglas_bq,
               muta=PP.muta_bq, log=log)
    cop = []
    for c, o in enumerate(r['copias']):
        sc = PP.semilla_copia(seed, c); L = []
        for d in o['linajes']:
            x = J.resumen_linaje(d, sc)
            L.append({k: x[k] for k in ('id', 'fundadores', 'descendientes', 'muertes', 'nac_reales', 'R0_real', 'cruza_real',
                                        'fund_post10k', 'coherente')})
        cop.append(dict(semilla=sc, linajes=L, rng_mundo=o['pista']['rng_mundo_estado']))
    return dict(camara=r['camara'], copias=cop, siembra=r['siembra'], meta=r['meta'])


def prueba(seed, siembra, T):
    """LA MEDIDA: la pista vieja + el juez (corre_bp.tarea importada, sin tocar), con el banco sembrado."""
    return CB.tarea(seed, 'bloq2', T, siembra=siembra)


def _escribe(fin, x):
    tmp = fin + '.tmp'
    with open(tmp, 'w', encoding='utf-8') as fh: json.dump(x, fh, ensure_ascii=False)
    os.replace(tmp, fin)


def trabajo(args):
    """UNA tarea; atrapa TODO (nube-9); escribe su JSON antes de volver (ERR-54)."""
    tipo, j, brazo, carpeta, se, sp, K, T_evo, T = args
    t0 = time.time()
    fin = os.path.join(carpeta, f"{brazo}_s{sp}.json")
    previo = None
    if os.path.exists(fin):
        with open(fin, encoding='utf-8') as fh: x0 = json.load(fh)
        if not x0.get('aborto'): return x0
        previo = x0['aborto']   # AUDITORIA H-1: un aborto guardado SE REINTENTA con --reanuda (queda anotado en 'reintento_de')
    try:
        cfg()   # AUDITORIA H-1: corre_bp.CFG0 fijado en ESTE proceso (worker de Pool o --reanuda con evo_*.json ya escrito)
        if tipo == 'ref':
            x = CB.tarea(sp, 'V143', T); x['brazo'] = brazo; x['aborto'] = None
        else:
            fe = os.path.join(carpeta, f"evo_{brazo}_i{j}.json")
            ev = None
            if os.path.exists(fe):
                with open(fe, encoding='utf-8') as fh: ev = json.load(fh)
                if ev.get('aborto'): ev = None   # AUDITORIA H-1: la camara abortada se reintenta
            if ev is None:
                try:
                    ev = evoluciona(se, MODO[brazo], K, T_evo); ev['aborto'] = None
                except BaseException as e:   # noqa: nube-9
                    ev = dict(aborto=f"{type(e).__name__}: {e}"[:300], traza=traceback.format_exc()[-1500:])
                ev.update(brazo=brazo, indice=j, semilla_evo=se, K=K, T_evo=T_evo, seg=round(time.time() - t0, 1))
                _escribe(fe, ev)
                if ev.get('aborto'): raise RuntimeError(f"evo con aborto: {ev['aborto']}")
            t1 = time.time()
            x = prueba(sp, ev['siembra'], T)
            x.update(brazo=brazo, aborto=None, siembra_n=len(ev['siembra']), indice=j, semilla_evo=se, K=K, T_evo=T_evo,
                     seg_evo=ev['seg'], seg_prueba=round(time.time() - t1, 1),
                     camara=dict(migrantes=sum(map(sum, ev['camara']['migrantes'])), limpios=sum(map(sum, ev['camara']['limpios'])),
                                 depositos=sum(ev['camara']['depositos']), siembra_por_linaje=ev['camara']['siembra_por_linaje']))
    except BaseException as e:   # noqa: nube-9
        x = dict(seed=sp, brazo=brazo, indice=j, aborto=f"{type(e).__name__}: {e}"[:300], traza=traceback.format_exc()[-1500:], linajes=[])
    x.pop('pizarra_log', None)
    if previo is not None: x['reintento_de'] = previo
    x['seg_total'] = round(time.time() - t0, 1)
    _escribe(fin, x)
    return x


# ------------------------------------------------------------------ lectura y veredicto (por codigo)
def med(xs):
    xs = [x for x in xs if x is not None]
    return round(float(st.median(xs)), 4) if xs else None


def _carga(carpeta, brazo, s):
    f = os.path.join(carpeta, f"{brazo}_s{s}.json")
    if not os.path.exists(f): return None
    with open(f, encoding='utf-8') as fh: return json.load(fh)


def _fila(x):
    if x is None or x.get('aborto') or not x.get('linajes'): return None
    L = x['linajes']
    return dict(cruzan=sum(1 for l in L if l['cruza_real']), R0_real_med=round(st.median([l['R0_real'] for l in L]), 3),
                mayoria=bool(sum(1 for l in L if l['cruza_real']) * 2 > len(L)),
                fund_med=med([l['fundadores'] for l in L]))


def arnes_pasado():
    if not os.path.exists(SALIDA_ARNES): return False, 'no existe la salida del arnes'
    t = open(SALIDA_ARNES, encoding='utf-8').read()
    sp = h16(os.path.join(PISTAD, 'pista_pob.py')); sr = h16(os.path.abspath(__file__))
    ok = ('ARNES pista_pob: PASA' in t) and (f"pista_pob.py {sp}" in t) and (f"corre_pista_pob.py {sr}" in t)   # AUDITORIA: tambien el runner
    return ok, (f"salida {'PASA' if 'ARNES pista_pob: PASA' in t else 'NO PASA'} · pista_pob.py actual {sp} {'citado' if f'pista_pob.py {sp}' in t else 'NO citado'}"
                f" · corre_pista_pob.py actual {sr} {'citado' if f'corre_pista_pob.py {sr}' in t else 'NO citado'}")


def predicciones(carpeta, semp, indices, humo, tab, a, b_, ssel, sneu, v143, n, log):
    """Q1-Q7 del preregistro (sec. 5), lo medido al lado. Q5 es un PROXY: migrantes / (migrantes + limpios) de toda la camara."""
    js = [0] if humo else list(indices)
    q5 = {}
    for br in BRAZOS:
        fr = []
        for j in js:
            f = os.path.join(carpeta, f"evo_{br}_i{j}.json")
            if not os.path.exists(f): fr.append(None); continue
            with open(f, encoding='utf-8') as fh: ev = json.load(fh)
            cam = ev.get('camara') or {}
            m = sum(map(sum, cam.get('migrantes', []))); l = sum(map(sum, cam.get('limpios', [])))
            fr.append(round(m / (m + l), 3) if m + l else None)
        q5[br] = fr
    sel = tab['pob_sel']; neu = tab['pob_neutro']
    q7 = sum(1 for k in range(n) if sel[k] and neu[k] and sel[k]['fund_med'] is not None and neu[k]['fund_med'] is not None
             and sel[k]['fund_med'] < neu[k]['fund_med'])
    Q = [('Q1', 'suma cruzan pob_sel en [18, 28] (p 0.65)', ssel, 18 <= ssel <= 28),
         ('Q2', 'suma cruzan pob_neutro en [16, 26] (p 0.65)', sneu, 16 <= sneu <= 26),
         ('Q3', 'pob_sel > pob_neutro en >= 4/5 (p 0.15)', f"{a}/{n}", a >= 4 * n / 5),
         ('Q4', 'pob_sel >= bloq2 en >= 4/5 (p 0.30)', f"{b_}/{n}", b_ >= 4 * n / 5),
         ('Q5', 'PROXY: migrantes/(migrantes+limpios) >= 0.90 en los dos brazos, todos los indices (p 0.80)', q5,
          all(v is not None and v >= 0.90 for fr in q5.values() for v in fr)),
         ('Q6', 'v143 R0 real mediano en [0.40, 0.80] (p 0.80)', v143, v143 is not None and 0.40 <= v143 <= 0.80),
         ('Q7', 'fundadores (mediana de 9) pob_sel < pob_neutro en >= 3/5 (p 0.35)', f"{q7}/{n}", q7 >= 3 * n / 5)]
    log("  PREDICCIONES (PREREGISTRO sec. 5) y lo medido" + (' (HUMO: no cuentan)' if humo else '') + ":")
    for q, txt, m, ok in Q: log(f"    {q} {txt}: medido {m} -> {'SE CUMPLE' if ok else 'NO se cumple'}")
    return [dict(q=q, texto=txt, medido=m, cumple=bool(ok)) for q, txt, m, ok in Q]


def lee(carpeta, indices, humo=False, log=print):
    semp = [HUMO['prueba']] if humo else [sem_prueba(j) for j in indices]
    tab = {}
    abortos = []
    for f in sorted(os.listdir(carpeta)):
        if f.endswith('.json') and not f.startswith('lectura'):
            with open(os.path.join(carpeta, f), encoding='utf-8') as fh: x = json.load(fh)
            if isinstance(x, dict) and x.get('aborto'): abortos.append([f, x['aborto']])
    for b in BRAZOS + ('v143',):
        tab[b] = [_fila(_carga(carpeta, b, s)) for s in semp]
    for b in REF_BRAZOS:
        tab[b] = [_fila(_carga(REFS, b, s)) for s in semp]
    log(f"\nLECTURA pista_pob · {carpeta} · semillas de prueba {semp}{' (HUMO: no decide)' if humo else ''}")
    log(f"  {'brazo':12s} " + ' '.join(f"{'s' + str(s):>16s}" for s in semp) + "   suma cruzan · R0 real med (mediana por semilla)")
    for b, fs in tab.items():
        cel = [(f"{f['cruzan']}/9 R0 {f['R0_real_med']}" if f else '--') for f in fs]
        log(f"  {b:12s} " + ' '.join(f"{c:>16s}" for c in cel) +
            f"   {sum(f['cruzan'] for f in fs if f) if any(fs) else '--'} · {med([f['R0_real_med'] for f in fs if f])}")
    completos = all(tab[b][k] is not None for b in BRAZOS for k in range(len(semp)))
    sel = tab['pob_sel']; neu = tab['pob_neutro']; bp = tab['bloq2']; bpas = tab['bloq_pas']
    a = sum(1 for k in range(len(semp)) if sel[k] and neu[k] and sel[k]['cruzan'] > neu[k]['cruzan'])
    b_ = sum(1 for k in range(len(semp)) if sel[k] and bp[k] and sel[k]['cruzan'] >= bp[k]['cruzan'])   # AUDITORIA H-2: bloq2 decide
    c_ = sum(1 for k in range(len(semp)) if sel[k] and bpas[k] and sel[k]['cruzan'] >= bpas[k]['cruzan'])   # bloq_pas: SOLO se imprime
    ssel = sum(f['cruzan'] for f in sel if f); sneu = sum(f['cruzan'] for f in neu if f)
    v143 = med([f['R0_real_med'] for f in tab['v143'] if f]); o1may = sum(1 for f in tab['o1'] if f and f['mayoria'])
    ar_ok, ar_txt = arnes_pasado()
    n = len(semp)
    val = dict(abortos=len(abortos), completos=completos, v143_R0_med=v143,
               v143_ok=bool(v143 is not None and ANCLA_V143[0] <= v143 <= ANCLA_V143[1]), o1_mayoria=f"{o1may}/{n}",
               o1_ok=bool(o1may >= 4 * n / 5), arnes=ar_txt, arnes_ok=ar_ok)
    valido = val['abortos'] == 0 and completos and val['v143_ok'] and val['o1_ok'] and ar_ok
    if not valido: ver = 'NO APLICA'
    elif a >= 4 * n / 5 and b_ >= 4 * n / 5: ver = 'FUNCIONA'
    elif a >= 3 * n / 5 or ssel >= sneu + 5: ver = 'HAY ALGO MODESTO'
    else: ver = 'NO'
    log(f"  PUERTA: sel > neutro (cruzan) en {a}/{n} · sel >= bloq2 en {b_}/{n} · suma cruzan sel {ssel} vs neutro {sneu} (+5 -> {sneu + 5}) "
        f"· (solo se imprime: sel >= bloq_pas en {c_}/{n})")
    log(f"  VALIDEZ: abortos {len(abortos)} {abortos[:3] if abortos else ''} · completos {completos} · v143 R0 real mediano {v143} en "
        f"{list(ANCLA_V143)}: {val['v143_ok']} · O1 mayoria {o1may}/{n} (>= 4/5): {val['o1_ok']} · arnes: {ar_txt}")
    pq = predicciones(carpeta, semp, indices, humo, tab, a, b_, ssel, sneu, v143, n, log)
    log(f"  VEREDICTO{' (HUMO, no cuenta)' if humo else ''}: {ver}")
    res = dict(tabla=tab, predicciones=pq, puerta=dict(sel_gt_neutro=a, sel_ge_bloq2=b_, sel_ge_bloq_pas_solo_se_imprime=c_, suma_sel=ssel, suma_neutro=sneu, n=n), validez=val,
               veredicto=ver, humo=humo, abortos=abortos)
    _escribe(os.path.join(carpeta, 'lectura_pista_pob.json'), res)
    return res


# ------------------------------------------------------------------ main
def main(argv=None):
    ap = argparse.ArgumentParser(allow_abbrev=False)
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument('--humo', action='store_true'); g.add_argument('--explora', action='store_true'); g.add_argument('--lee', default=None)
    ap.add_argument('--pool', type=int, default=0); ap.add_argument('--reanuda', action='store_true')
    ap.add_argument('--indices', default='1,2,3,4,5'); ap.add_argument('--carpeta', default=None)   # solo --humo --reanuda
    a = ap.parse_args(argv)
    ind = tuple(int(x) for x in a.indices.split(','))
    if not set(ind) <= set(INDICES): raise SystemExit(f"--indices dentro de {INDICES}")
    if a.lee:
        c = a.lee if os.path.isabs(a.lee) else os.path.join(AQUI, a.lee)
        LOGF = open(os.path.join(c, 'lectura.txt'), 'w', encoding='utf-8')
        def log(s=''): print(s, flush=True); LOGF.write(s + '\n'); LOGF.flush()
        lee(c, ind, humo=('humo' in os.path.basename(c)), log=log); return 0
    if a.humo:
        if a.pool: raise SystemExit("--humo es de UN proceso (sin --pool)")
        if a.carpeta:   # AUDITORIA H-1: humo de --reanuda sobre una carpeta de humo ya escrita
            carpeta = a.carpeta if os.path.isabs(a.carpeta) else os.path.join(AQUI, a.carpeta)
            if not (a.reanuda and os.path.isdir(carpeta) and os.path.basename(carpeta).startswith('humo_')):
                raise SystemExit("--carpeta solo con --humo --reanuda y una carpeta humo_* existente")
        else:
            if a.reanuda: raise SystemExit("--humo --reanuda exige --carpeta humo_*")
            carpeta = os.path.join(DATOS, time.strftime('humo_%Y%m%d_%H%M%S')); os.makedirs(carpeta, exist_ok=True)
    else:
        if a.carpeta: raise SystemExit("--carpeta solo con --humo --reanuda")
        carpeta = os.path.join(DATOS, 'explora'); os.makedirs(carpeta, exist_ok=True)
        hay = [f for f in os.listdir(carpeta) if f.endswith('.json')]
        if hay and not a.reanuda: raise SystemExit(f"{carpeta} ya tiene {len(hay)} JSON: usar --reanuda (no se pisa nada)")
    LOGF = open(os.path.join(carpeta, 'log.txt'), 'a', encoding='utf-8')
    def log(s=''): print(s, flush=True); LOGF.write(s + '\n'); LOGF.flush()
    log(f"PISTA_POB · {'HUMO' if a.humo else 'EXPLORA'} · {time.strftime('%Y-%m-%d %H:%M:%S')} · pool {a.pool or 'NO (un proceso)'} · carpeta {carpeta}")
    ok = verifica(log)
    log(f"  CFG (tasas BQ_C de la ronda 2 = corre_bp.CFG0): {cfg()}")
    if not ok: log("  UN SHA NO CALZA -> no se corre nada."); return 1
    ar_ok, ar_txt = arnes_pasado(); log(f"  arnes: {ar_txt}")
    if not a.humo and not ar_ok: log("  ARNES NO PASADO -> el explora no se corre."); return 1
    if a.humo:
        H = HUMO
        tareas = [('pob', 0, b, carpeta, H['evo'], H['prueba'], H['K'], H['T_evo'], H['T']) for b in BRAZOS] + \
                 [('ref', 0, 'v143', carpeta, None, H['prueba'], None, None, H['T'])]
    else:
        tareas = [('pob', j, b, carpeta, sem_evo(j), sem_prueba(j), K_DEF, T_EVO, T_PRUEBA) for j in ind for b in BRAZOS] + \
                 [('ref', j, 'v143', carpeta, None, sem_prueba(j), None, None, T_PRUEBA) for j in ind]
    log(f"  {len(tareas)} tareas: {[(t[2], t[4], t[5]) for t in tareas]} · K {tareas[0][6]} · T_evo {tareas[0][7]} · T prueba {tareas[0][8]}")
    t0 = time.time()
    def informa(x):
        L = x.get('linajes', [])
        log(f"  [{time.time() - t0:7.1f}s] {x.get('brazo')} s{x.get('seed')} aborto {x.get('aborto')} · seg evo {x.get('seg_evo')} prueba "
            f"{x.get('seg_prueba', x.get('seg'))} · camara {x.get('camara')} · cruzan {sum(l['cruza_real'] for l in L)}/{len(L)} · "
            f"R0 real {[l['R0_real'] for l in L]}")
    if a.pool and a.pool > 1:
        from multiprocessing import Pool
        with Pool(a.pool) as PL:
            for x in PL.imap_unordered(trabajo, tareas): informa(x)
    else:
        for tk in tareas: informa(trabajo(tk))
    lee(carpeta, ind, humo=a.humo, log=log)
    log(f"Terminado en {time.time() - t0:.1f}s")
    return 0


if __name__ == '__main__':
    sys.exit(main())
