"""corre_eco_v11.py — RUNNER y JUEZ v2 de JUACO-ECO v1.1 (nivel 10), con el MOTOR GEMELO. Nube, 24-sep-2026.

MISION: llegar a la AGI por este camino.

Preregistro: experimentos/juaco_eco/PREREGISTRO_eco_v11.md (la letra esta AQUI, en veredicto() y veredicto_L(), y alli).
ECO v1.1 = ECO v1 (PREREGISTRO_eco.md: mismo mundo, mismos brazos, mismo vivero, mismo corte en 60 000, misma mutacion) con DOS cambios
de INSTRUMENTO, ninguno de mecanismo:
  (1) JUEZ v2 (candidatos nube-4 y nube-6 de la bitacora de la nube): la colonia del banco de VIDA se compara con la del banco de AZAR de
      la MISMA semilla (las dos diversas; no contra 9 copias de G0), en una bateria sellada NUEVA (19501-19520), y un PLACEBO calibra el
      juez: dos muestras distintas del MISMO banco (flujos de rng 7 y 8) deben empatar en distribucion (5 <= puntaje <= 15 de 20).
  (2) LECTURA LARGA: cada corrida sigue hasta T = 1e6 con el gemelo. El veredicto de v1.1 se lee en T_lect = 120 000 (el horizonte de
      v1; la dinamica no depende de T: arnes (H)); el bloque L (persistencia a 1e6) tiene su propia letra (veredicto_L).
Motor: el gemelo numba (motor_eco_rapido, 120/120 en identidad_eco_rapido.py), via corre_eco_rapido (que cambia SOLO CR.ME).
Nada de corre_eco.py, corre_eco_rapido.py, motor_eco*.py ni de los carros se modifica: este archivo los IMPORTA.

Uso (ERR-115: banderas desconocidas o abreviadas abortan; --help no existe):
  python experimentos/juaco_eco/corre_eco_v11.py --humo
  python experimentos/juaco_eco/corre_eco_v11.py --prueba_pool --desde 19602 --n 2 --pool 2
  python experimentos/juaco_eco/corre_eco_v11.py --serie --desde 19401 --n 20 --pool 3        # serie
  python experimentos/juaco_eco/corre_eco_v11.py --serie --desde 19421 --n 20 --pool 3        # replica
  python experimentos/juaco_eco/corre_eco_v11.py --serie --desde 19401 --n 20 --pool 3 --reanuda
  python experimentos/juaco_eco/corre_eco_v11.py --lee <carpeta de la serie>
"""
import argparse, glob, hashlib, json, os, pickle, sys, time
import numpy as np

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
if AQUI not in sys.path: sys.path.insert(0, AQUI)
import corre_eco_rapido as CRR   # importa corre_eco (CR) y cambia CR.ME por el gemelo; nada mas
CR = CRR.CR

MUNDO = CR.MUNDO                  # esc 90, 90 fundadores FABRICA_ECO, tope 3000, muestra 1000 (v1, sin cambios)
SERIE = CR.SERIE                  # banco 200, 8 sombras, sigma 0.15, p_mut 0.05, cada_gen 2000, ckpt_cada 10000 (v1, sin cambios)
V11 = dict(T=1_000_000, t_corte=60000, T_lect=120000, gen_largo=50000)   # corte y lectura = los de v1; T largo = el de ECO largo
JUEZ2 = dict(esc=9, n=9, T_b=20000, semillas=tuple(range(19501, 19521)), flujo=7, flujo_placebo=8)
VENTANAS = (19401, 19421)         # serie y replica (n = 20)
PRACTICA = tuple(range(19601, 19610))   # humo 19601; prueba del Pool 19602-19609; el arnes usa 19603-19605
HUMO = dict(semilla=19601, brazos=('VIDA', 'AZAR'), T=30000, t_corte=8000, T_lect=12000, juez_semillas=3, juez_T=6000)
BRAZOS = tuple(CR.BRAZOS)         # VIDA, CEREBRO, AZAR, MUT0 (v1, sin cambios)
JUZGADOS = ('VIDA', 'CEREBRO', 'AZAR')
PLACEBO = ('VIDA', 'AZAR')
DATOS = os.path.join(AQUI, 'datos')


class BanderaMala(SystemExit):
    pass


# ================================================================================ JUEZ v2
def fundadores(fuente, s, flujo):
    """9 genomas de la colonia en la semilla de bateria s. fuente = UN genoma (9 copias) o el BANCO (lista): 9 entradas al azar con el
    rng [s, flujo]. Con flujo = 7 es EXACTAMENTE corre_eco.fundadores_juez (arnes (A)); el placebo usa flujo = 8."""
    a = np.asarray(fuente, float)
    if a.ndim == 1: return np.tile(a, (JUEZ2['n'], 1))
    idx = np.random.default_rng([s, flujo]).choice(len(a), size=JUEZ2['n'], replace=len(a) < JUEZ2['n'])
    return a[idx]


def juez(fuente, semillas, T_b, flujo=7):
    """Bateria: colonia de 9 (fundadores), mundo esc = 9, sin mutacion ni reposicion. Mide cuanto vive (t_ext o T_b). = corre_eco.juez
    con otro rng de muestreo si flujo != 7."""
    out = []
    for s in semillas:
        gs = fundadores(fuente, s, flujo)
        r = CR.ME.run_solapadas(s, [MUNDO['carro']] * JUEZ2['n'], T=T_b, diag=0, mundo_n=JUEZ2['esc'], tope_cuerpos=MUNDO['tope'],
                                muestra=MUNDO['muestra'], eco=dict(refunda=0, p_mut=0.0, genoma=gs.tolist()))
        te = r['eco']['t_ext']
        out.append(dict(s=s, t_ext=te, vive=(T_b if te is None else te), vivos_T=len(r['eco']['vivos_final']), nac=r['eco']['n_nac']))
    return out


def med_bat(bat):
    return float(np.median([d['vive'] for d in bat])) if bat else None


# ================================================================================ UNA CORRIDA
def trabajo(args):
    """UNA corrida (semilla, brazo) hasta T con el gemelo: vivero + corte (= v1), lectura en T_lect, juez v2 (y placebo) del banco del
    corte. Checkpoint reanudable. Escribe su JSON (gen_t aclarado tras T_lect: una fila cada gen_largo)."""
    seed, brazo, T, t_corte, T_lect, carpeta, n_juez, T_juez, reanuda = args
    fin = os.path.join(carpeta, f"{brazo}_s{seed}.json")
    if reanuda and os.path.exists(fin): return json.load(open(fin, encoding='utf-8'))
    ck = os.path.join(carpeta, 'ckpt', f"{brazo}_s{seed}.pkl"); os.makedirs(os.path.dirname(ck), exist_ok=True)
    filas = []

    def cb(li, row, g):
        if row[3] >= t_corte: filas.append([li] + row)

    def guarda(t, blob):
        tmp = ck + '.tmp'
        with open(tmp, 'wb') as f: pickle.dump(dict(t=t, blob=blob, filas=filas), f, protocol=pickle.HIGHEST_PROTOCOL)
        os.replace(tmp, ck)

    estado = None
    if reanuda and os.path.exists(ck):
        d = pickle.load(open(ck, 'rb')); estado = d['blob']; filas[:] = d['filas']
    t0 = time.time()
    r = CR.ME.run_solapadas(seed, [MUNDO['carro']] * MUNDO['n0'], T=T, diag=0, mundo_n=MUNDO['esc'], tope_cuerpos=MUNDO['tope'],
                            muestra=MUNDO['muestra'],
                            eco=CR.eco_cfg(brazo, t_corte, ckpt_cada=SERIE['ckpt_cada'], ckpt_fn=guarda, estado=estado, ind_cb=cb))
    E = r['eco']; P = r['pista']
    fila_corte = next((f for f in E['gen_t'] if f[0] == t_corte), None)
    fila_lect = next((f for f in E['gen_t'] if f[0] == T_lect), None)
    te = E['t_ext']
    pers_lect = int(te is None or te > T_lect)       # vivo tras el paso T_lect - 1 (t_ext = t + 1 del paso en que murio el ultimo)
    coh = [f for f in filas if f[4] <= T - 20000]
    res = dict(seed=seed, brazo=brazo, T=T, t_corte=t_corte, T_lect=T_lect, seg=round(time.time() - t0, 1), t_ext=te,
               persiste=int(te is None and len(E['vivos_final']) > 0), persiste_lect=pers_lect,
               vivos_lect=(fila_lect[1] if fila_lect is not None else (0 if not pers_lect else None)),
               vivos_T=len(E['vivos_final']), linajes_T=len(set(v[0] for v in E['vivos_final'])),
               gen_max_T=(max(v[2] for v in E['vivos_final']) if E['vivos_final'] else None),
               bloqueados=P['bloqueados'], max_vivos=P['max_vivos'], n_nac=E['n_nac'], n_refund=E['n_refund'], n_banco=E['n_banco'],
               tasa_mut=(E['n_mut'] / max(1, (E['n_nac'] + E['n_banco'])) / len(E['genes'])),
               nac_post=len(filas), r0_post=(round(float(np.mean([f[6] for f in coh])), 4) if coh else None), n_coh_post=len(coh),
               corte=E['corte'], sel_corte=CR.sel_genes(fila_corte),
               gen_t=[f for f in E['gen_t'] if f[0] <= T_lect or f[0] % V11['gen_largo'] == 0], tam_total=P['tam_total'],
               genes=E['genes'], G0=E['G0'], vivos_final=E['vivos_final'][:500], juez=None, juez_placebo=None,
               motor='GEMELO motor_eco_rapido')
    if brazo in JUZGADOS and E['corte'] and E['corte']['banco']:
        sem = JUEZ2['semillas'][:n_juez]
        res['juez'] = dict(fuente='banco en el corte (9 entradas al azar por semilla, flujo 7)', med_banco=E['corte']['med_banco'],
                           bateria=juez(E['corte']['banco'], sem, T_juez, JUEZ2['flujo']))
        if brazo in PLACEBO:
            res['juez_placebo'] = dict(fuente='el MISMO banco, otra muestra de 9 (flujo 8)',
                                       bateria=juez(E['corte']['banco'], sem, T_juez, JUEZ2['flujo_placebo']))
    tmp = fin + '.tmp'
    with open(tmp, 'w', encoding='utf-8') as f: json.dump(res, f)
    os.replace(tmp, fin)
    if os.path.exists(ck): os.remove(ck)
    return res


def g0_bateria(n_juez, T_juez, carpeta):
    """G0 (9 copias) en la bateria sellada nueva: DESCRIPTIVO (nube-6: AZAR contra G0 mide diversidad + deriva), no decide."""
    ruta = os.path.join(carpeta, f"juez_G0_n{n_juez}_T{T_juez}.json")
    if os.path.exists(ruta): return json.load(open(ruta, encoding='utf-8'))
    G0 = CR.ME.genoma0(__import__('pista2').cfg_fabrica())
    b = juez(list(G0), JUEZ2['semillas'][:n_juez], T_juez)
    json.dump(b, open(ruta, 'w', encoding='utf-8')); return b


# ================================================================================ LA LETRA (PREREGISTRO_eco_v11.md §6)
def veredicto(R, G0bat, n_esperado=20):
    """ECO v1.1 (una serie). Persistencia leida en T_lect = 120 000 (persiste_lect). Juez v2: VIDA contra AZAR, pareado por semilla."""
    L = []; by = {b: sorted([x for x in R if x['brazo'] == b], key=lambda x: x['seed']) for b in BRAZOS}
    n = {b: len(v) for b, v in by.items()}
    pers = {b: sum(x['persiste_lect'] for x in v) for b, v in by.items()}
    L.append(f"semillas por brazo: {n}; persiste en T_lect = {V11['T_lect']} (como v1): {pers}")
    completo = all(n[b] == n_esperado for b in BRAZOS)
    bloq = sum(x['bloqueados'] for x in R)
    g0_med = med_bat(G0bat)
    P1 = pers['VIDA'] >= 15
    P1c = pers['MUT0'] <= 2
    genes = R[0]['genes'] if R else []

    def cuenta(b):
        c = {}
        for j, g in enumerate(genes):
            s = [x['sel_corte'][j] for x in by[b] if x['sel_corte'] is not None]
            c[g] = (sum(1 for v in s if v > 0), sum(1 for v in s if v < 0))
        return c
    cV, cA = cuenta('VIDA'), cuenta('AZAR')
    sel = [g for g in genes if max(cV[g]) >= 15]
    falsos = [g for g in genes if max(cA[g]) > 8]
    P2 = len(sel) >= 1
    L.append(f"P2 genes seleccionados en VIDA (>=15/20 mismo signo fuera de las 8 sombras): {[(g, cV[g]) for g in sel]}; "
             f"AZAR con > 8/20 (falsos positivos del instrumento): {[(g, cA[g]) for g in falsos]}")
    # juez v2: pareado por semilla
    m = {b: {x['seed']: (med_bat(x['juez']['bateria']) if x.get('juez') else None) for x in by[b]} for b in JUZGADOS}
    mp = {b: {x['seed']: (med_bat(x['juez_placebo']['bateria']) if x.get('juez_placebo') else None) for x in by[b]} for b in PLACEBO}

    def pareado(a, b):
        w = e = k = 0
        for s in sorted(set(m[a]) & set(m[b])):
            if m[a][s] is None or m[b][s] is None: continue
            k += 1; w += int(m[a][s] > m[b][s]); e += int(m[a][s] == m[b][s])
        return w, e, k
    wVA, eVA, kVA = pareado('VIDA', 'AZAR')
    wCA, eCA, kCA = pareado('CEREBRO', 'AZAR')
    P3 = wVA >= 15
    plac = {}
    for b in PLACEBO:
        w = e = k = 0
        for s, v in m[b].items():
            u = mp[b].get(s)
            if v is None or u is None: continue
            k += 1; w += int(v > u); e += int(v == u)
        plac[b] = (w + 0.5 * e, k)
    placebo_ok = all(k == n_esperado and 5 <= p <= 15 for p, k in plac.values())
    gV = sum(1 for v in m['VIDA'].values() if v is not None and g0_med is not None and v > g0_med)
    gA = sum(1 for v in m['AZAR'].values() if v is not None and g0_med is not None and v > g0_med)
    medV = float(np.median([v for v in m['VIDA'].values() if v is not None])) if any(v is not None for v in m['VIDA'].values()) else None
    medA = float(np.median([v for v in m['AZAR'].values() if v is not None])) if any(v is not None for v in m['AZAR'].values()) else None
    L.append(f"P3 juez v2 (bateria sellada 19501-19520): VIDA > AZAR (pareado, estricto) {wVA}/{kVA} (empates {eVA}); CEREBRO > AZAR "
             f"{wCA}/{kCA} (empates {eCA}); medianas VIDA {medV} · AZAR {medA}")
    L.append(f"PLACEBO del juez (muestra flujo 7 contra flujo 8 del MISMO banco; puntaje = gana + empates/2, valido en [5, 15] de 20): "
             f"{ {b: p for b, p in plac.items()} } -> {'VALIDO' if placebo_ok else 'NO VALIDO'}")
    L.append(f"DESCRIPTIVO (nube-6, no decide): contra G0 (mediana {g0_med}) ganan VIDA {gV}/{n['VIDA']} y AZAR {gA}/{n['AZAR']}")
    P4 = pers['VIDA'] - pers['AZAR'] >= 8
    Hc = pers['CEREBRO'] >= 15
    L.append(f"P1 VIDA persiste >= 15/20: {'SE CUMPLE' if P1 else 'NO'} ({pers['VIDA']}) · P1c MUT0 <= 2/20: {'SE CUMPLE' if P1c else 'NO'} "
             f"({pers['MUT0']}) · P2: {'SE CUMPLE' if P2 else 'NO'} · P3 VIDA > AZAR >= 15/20: {'SE CUMPLE' if P3 else 'NO'} ({wVA}) · "
             f"P4 VIDA - AZAR >= 8: {'SE CUMPLE' if P4 else 'NO'} ({pers['VIDA'] - pers['AZAR']}) · H-c CEREBRO >= 15/20: "
             f"{'SE CUMPLE' if Hc else 'NO'} ({pers['CEREBRO']})")
    if not completo: v = 'NO EVALUABLE (serie incompleta)'
    elif bloq > 0: v = f'NO EVALUABLE (tope de cuerpos alcanzado: bloqueados = {bloq})'
    elif pers['MUT0'] >= 10: v = 'NO EVALUABLE (MUT0 persiste en >= 10/20: el mundo es demasiado facil)'
    elif falsos: v = 'NO EVALUABLE (AZAR da falsos positivos de seleccion: el control de sombras no vale)'
    elif not placebo_ok: v = 'NO EVALUABLE (el placebo del juez v2 sale de [5, 15]: el juez no esta calibrado)'
    elif P1 and P1c and P2 and P3 and P4: v = 'FUNCIONA (en esta serie)'
    elif P2 and P3: v = 'HAY ALGO MODESTO (en esta serie)'
    else: v = 'NO (en esta serie)'
    L.append(f"VEREDICTO v1.1 POR LA LETRA (una serie; el del bloque exige serie + replica con el mismo veredicto): {v}")
    return v, L, dict(P1=P1, P1c=P1c, P2=P2, P3=P3, P4=P4, Hc=Hc, pers=pers, sel=sel, falsos=falsos, wVA=wVA, eVA=eVA, wCA=wCA,
                      placebo={b: list(p) for b, p in plac.items()}, placebo_ok=placebo_ok, gV=gV, gA=gA, g0_med=g0_med)


def veredicto_L(R, n_esperado=20):
    """Bloque L (su propia letra): persistencia a T = 1e6 (940 000 pasos tras el corte), mismas corridas."""
    L = []; by = {b: [x for x in R if x['brazo'] == b] for b in BRAZOS}
    n = {b: len(v) for b, v in by.items()}
    pers = {b: sum(x['persiste'] for x in v) for b, v in by.items()}
    completo = all(n[b] == n_esperado for b in BRAZOS) and all(x['T'] == V11['T'] for x in R)
    bloq = sum(x['bloqueados'] for x in R)
    L1 = pers['VIDA'] >= 10
    L2 = pers['VIDA'] - pers['AZAR'] >= 6
    L1c = pers['MUT0'] <= 2
    r0 = {b: [x['r0_post'] for x in v if x['persiste'] and x['r0_post'] is not None] for b, v in by.items()}
    L.append(f"L: persiste en T = {V11['T']}: {pers}; R0 de la cohorte tras el corte en los que persisten (mediana): "
             f"{ {b: (round(float(np.median(v)), 4) if v else None) for b, v in r0.items()} }")
    L.append(f"L1 VIDA >= 10/20: {'SE CUMPLE' if L1 else 'NO'} ({pers['VIDA']}) · L1c MUT0 <= 2/20: {'SE CUMPLE' if L1c else 'NO'} "
             f"({pers['MUT0']}) · L2 VIDA - AZAR >= 6: {'SE CUMPLE' if L2 else 'NO'} ({pers['VIDA'] - pers['AZAR']})")
    if not completo: v = 'NO EVALUABLE (serie incompleta o T distinto de 1e6)'
    elif bloq > 0: v = f'NO EVALUABLE (tope de cuerpos alcanzado: bloqueados = {bloq})'
    elif L1 and L1c and L2: v = 'PERSISTE LARGO Y LA SELECCION SUMA (en esta serie)'
    elif L1 and L1c: v = 'PERSISTE LARGO (en esta serie; la seleccion no se distingue del azar por persistencia)'
    else: v = 'NO PERSISTE LARGO (en esta serie)'
    L.append(f"VEREDICTO L POR LA LETRA (una serie): {v}")
    return v, L, dict(L1=L1, L1c=L1c, L2=L2, pers=pers)


def lee(carpeta, n_esperado=20):
    R = [json.load(open(p, encoding='utf-8')) for p in sorted(glob.glob(os.path.join(carpeta, '*_s*.json')))]
    G0b = next((json.load(open(p, encoding='utf-8')) for p in glob.glob(os.path.join(carpeta, 'juez_G0_*.json'))), [])
    v, L, d = veredicto(R, G0b, n_esperado)
    vL, LL, dL = veredicto_L(R, n_esperado)
    for l in L + LL: print(l, flush=True)
    return v, L, d, vL, LL, dL, R


def SHAS():
    f = lambda p: hashlib.sha256(open(os.path.join(AQUI, p), 'rb').read()).hexdigest()[:16]
    return {p: f(p) for p in ('corre_eco_v11.py', 'corre_eco.py', 'corre_eco_rapido.py', 'motor_eco.py', 'motor_eco_rapido.py',
                              'carros/FABRICA_ECO.py', 'PREREGISTRO_eco_v11.md') if os.path.exists(os.path.join(AQUI, p))}


# ================================================================================ BANDERAS (ERR-115)
def parsea(argv):
    ap = argparse.ArgumentParser(allow_abbrev=False, add_help=False)
    ap.add_argument('--humo', action='store_true'); ap.add_argument('--serie', action='store_true')
    ap.add_argument('--prueba_pool', action='store_true'); ap.add_argument('--lee', default=None)
    ap.add_argument('--desde', type=int); ap.add_argument('--n', type=int); ap.add_argument('--pool', type=int)
    ap.add_argument('--reanuda', action='store_true')
    try:
        a, resto = ap.parse_known_args(argv)
    except SystemExit:
        raise BanderaMala('ECO v1.1: banderas mal formadas')
    if resto: raise BanderaMala(f"ECO v1.1: banderas desconocidas {resto}")
    if any(x.startswith('--') and '=' in x for x in argv): raise BanderaMala('ECO v1.1: sin la forma --bandera=valor')
    if len(argv) != len(set(x for x in argv if x.startswith('--'))) + sum(1 for x in argv if not x.startswith('--')):
        raise BanderaMala('ECO v1.1: bandera repetida')
    modos = int(a.humo) + int(a.serie) + int(a.prueba_pool) + int(a.lee is not None)
    if modos != 1: raise BanderaMala('ECO v1.1: exactamente uno de --humo, --serie, --prueba_pool, --lee')
    if a.humo and (a.desde is not None or a.n is not None or a.pool is not None or a.reanuda): raise BanderaMala('ECO v1.1: --humo va solo')
    if a.lee is not None and (a.desde is not None or a.n is not None or a.pool is not None or a.reanuda): raise BanderaMala('ECO v1.1: --lee va solo')
    if a.prueba_pool and (a.desde not in PRACTICA[1:] or a.desde + 1 not in PRACTICA or a.n != 2 or a.pool != 2 or a.reanuda):
        raise BanderaMala('ECO v1.1: --prueba_pool --desde 19602..19608 --n 2 --pool 2')
    if a.serie and (a.desde not in VENTANAS or a.n != 20 or a.pool is None or not 1 <= a.pool <= 3):
        raise BanderaMala(f"ECO v1.1: --serie --desde {VENTANAS[0]} (serie) o {VENTANAS[1]} (replica) --n 20 --pool 1..3 (nube: 4 nucleos)")
    return a


def humo():
    """UN proceso, semilla de practica 19601, VIDA y AZAR, T corto (lectura en 12 000 de 30 000). Numeros de humo: no deciden nada."""
    os.makedirs(os.path.join(DATOS, 'humo'), exist_ok=True)
    ts = time.strftime('%Y%m%d_%H%M%S'); carpeta = os.path.join(DATOS, 'humo', f"eco_v11_humo_s{HUMO['semilla']}_{ts}")
    os.makedirs(carpeta, exist_ok=True); t0 = time.time()
    print(f"[{time.strftime('%H:%M:%S')}] HUMO ECO v1.1 · shas {SHAS()}", flush=True)
    R = []
    for b in HUMO['brazos']:
        r = trabajo((HUMO['semilla'], b, HUMO['T'], HUMO['t_corte'], HUMO['T_lect'], carpeta, HUMO['juez_semillas'], HUMO['juez_T'], False))
        R.append(r)
        print(f"[{time.strftime('%H:%M:%S')}] {b} s{r['seed']}: {r['seg']} s · persiste_lect {r['persiste_lect']} (vivos {r['vivos_lect']}) · "
              f"persiste en T {r['persiste']} · t_ext {r['t_ext']} · juez {[d['vive'] for d in r['juez']['bateria']] if r['juez'] else None} · "
              f"placebo {[d['vive'] for d in r['juez_placebo']['bateria']] if r['juez_placebo'] else None}", flush=True)
    G0b = juez(list(CR.ME.genoma0(__import__('pista2').cfg_fabrica())), JUEZ2['semillas'][:HUMO['juez_semillas']], HUMO['juez_T'])
    print(f"  G0: {[d['vive'] for d in G0b]}", flush=True)
    v, L, d = veredicto(R, G0b, n_esperado=20)
    vL, LL, dL = veredicto_L(R, n_esperado=20)
    for l in L + LL: print('  ' + l, flush=True)
    ruta = os.path.join(DATOS, 'humo', f"eco_v11_humo_s{HUMO['semilla']}_{ts}.json")
    json.dump(dict(humo=HUMO, V11=V11, JUEZ2=dict(JUEZ2, semillas=list(JUEZ2['semillas'])), R=R, G0=G0b, veredicto_de_prueba=v,
                   veredicto_L_de_prueba=vL, lineas=L + LL, seg=round(time.time() - t0, 1), shas=SHAS()),
              open(ruta, 'w', encoding='utf-8'))
    print(f"  JSON: {os.path.relpath(ruta, RAIZ)}  ({round(time.time() - t0, 1)} s)")
    print(f"VEREDICTO (humo, una semilla, no decide): {v} · L: {vL}")


def main(argv=None):
    a = parsea(sys.argv[1:] if argv is None else argv)
    if a.humo: return humo()
    if a.lee is not None:
        lee(a.lee); return
    if a.prueba_pool:
        T, tc, tl, nj, Tj = 3000, 2000, 2500, 2, 2000; etq = f"v11_prueba_pool_s{a.desde}"
    else:
        T, tc, tl, nj, Tj = V11['T'], V11['t_corte'], V11['T_lect'], len(JUEZ2['semillas']), JUEZ2['T_b']
        etq = f"v11_serie_s{a.desde}-{a.desde + a.n - 1}"
    carpeta = os.path.join(DATOS, f"eco_{etq}")
    if os.path.exists(carpeta) and not a.reanuda and glob.glob(os.path.join(carpeta, '*_s*.json')):
        raise SystemExit(f"ECO v1.1: {carpeta} ya tiene resultados; --reanuda (no se pisa nada)")
    os.makedirs(carpeta, exist_ok=True)
    flog = open(os.path.join(carpeta, 'progreso.log'), 'a', encoding='utf-8')

    def log(s):
        s = f"[{time.strftime('%H:%M:%S')}] {s}"; print(s, flush=True); flog.write(s + '\n'); flog.flush()
    log(f"ECO v1.1 {etq} · T {T} · corte {tc} · lectura {tl} · juez {nj} semillas T_b {Tj} · pool {a.pool} · shas {SHAS()}")
    jobs = [(s, b, T, tc, tl, carpeta, nj, Tj, a.reanuda) for s in range(a.desde, a.desde + a.n) for b in BRAZOS]
    t0 = time.time()
    from multiprocessing import Pool
    with Pool(a.pool) as pool:
        G0r = pool.apply_async(g0_bateria, (nj, Tj, carpeta))
        for k, r in enumerate(pool.imap_unordered(trabajo, jobs), 1):
            log(f"[{k}/{len(jobs)}] {r['brazo']} s{r['seed']}: persiste_lect {r['persiste_lect']} · persiste_T {r['persiste']} · t_ext {r['t_ext']} "
                f"· vivos_T {r['vivos_T']} ({r['seg']} s; {round(time.time() - t0)} s)")
        G0r.get()
    v, L, d, vL, LL, dL, R = lee(carpeta, a.n)
    for l in L + LL: flog.write(l + '\n')
    json.dump(dict(etiqueta=etq, veredicto=v, veredicto_L=vL, lineas=L + LL, d=d, dL=dL, seg=round(time.time() - t0), MUNDO=MUNDO,
                   SERIE=SERIE, V11=V11, JUEZ2=dict(JUEZ2, semillas=list(JUEZ2['semillas'])), shas=SHAS()),
              open(os.path.join(carpeta, 'RESUMEN.json'), 'w', encoding='utf-8'), indent=1, default=str)
    log(f"VEREDICTO: {v}")
    log(f"VEREDICTO L: {vL}")
    flog.close()


if __name__ == '__main__':
    try:
        main()
    except BanderaMala as e:
        print(str(e), file=sys.stderr); sys.exit(2)
