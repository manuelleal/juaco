"""corre_eco.py — RUNNER y JUEZ de JUACO-ECO v1 (nivel 10): vivero + corte en un mundo gigante con el organismo real.

MISION: llegar a la AGI por este camino.

Preregistro: experimentos/juaco_eco/PREREGISTRO_eco.md (la letra del veredicto esta AQUI, en veredicto(), y alli).
Mundo (fijo): pista v2 (quimiostato r = 0.03*esc) con esc = 90 -> L = 3600, 360 objetos (10x la pista de 9 linajes), 90 fundadores
FABRICA_ECO (FABRICA con _see rapido, identico), tope de seguridad 3000 cuerpos, muestra 1000.
Brazos: VIDA (18 genes mutan), CEREBRO (solo los 15 del cerebro/estructura), AZAR (18 genes; el genoma de todo cuerpo nuevo sale del banco al azar = sin seleccion),
MUT0 (sin mutacion). Todos: vivero (t < t_corte: fundador desde el banco de donantes) y luego corte (nadie repone nada).
Juez automatico: el BANCO en el corte (9 entradas al azar por semilla), en la bateria fija (mundo esc = 9, 9 fundadores, sin
mutacion, sin reposicion, T_b = 20000, semillas selladas 19201-19220), contra G0 en las mismas semillas.

Uso (SOLO el coordinador lanza --serie; un creador corre solo --humo):
  python experimentos/juaco_eco/corre_eco.py --humo
  python experimentos/juaco_eco/corre_eco.py --serie --desde 19101 --n 20 --pool 6            # serie
  python experimentos/juaco_eco/corre_eco.py --serie --desde 19121 --n 20 --pool 6            # replica
  python experimentos/juaco_eco/corre_eco.py --serie --desde 19101 --n 20 --pool 6 --reanuda  # tras un corte de luz
  python experimentos/juaco_eco/corre_eco.py --lee <carpeta de la serie>                     # solo agrega y dicta
  python experimentos/juaco_eco/corre_eco.py --largo --desde 19301 --n 3 --pool 6 [--reanuda]  # ECO largo (1e6 pasos), SOLO tras la serie
Banderas desconocidas o abreviadas: ABORTA (ERR-115).
"""
import argparse, glob, gzip, json, os, pickle, sys, time
import numpy as np

sys.stdout.reconfigure(encoding='utf-8', errors='replace')
AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
sys.path[:0] = [AQUI, os.path.join(RAIZ, 'experimentos', 'generaciones')]
import motor_eco as ME

MUNDO = dict(esc=90, n0=90, carro='FABRICA_ECO', tope=3000, muestra=1000)
SERIE = dict(T=120000, t_corte=60000, banco=200, n_sombra=8, sigma=0.15, p_mut=0.05, cada_gen=2000, ckpt_cada=10000)
HUMO = dict(semilla=19001, brazo='VIDA', T=12000, t_corte=8000, juez_semillas=3, juez_T=6000)
JUEZ = dict(esc=9, n=9, T_b=20000, semillas=tuple(range(19201, 19221)))
LARGO = dict(desde=19301, n=3, T=1000000, t_corte=100000, brazos=('VIDA', 'AZAR'))   # ECO largo sin atencion (SOLO tras la serie)
VENTANAS = (19101, 19121)          # serie y replica (n = 20); practica/humo 19001-19040; bateria del juez 19201-19220
VIDA_GENES = ('dote', 'rep_umbral', 'rep_X')
BRAZOS = {
    'VIDA': dict(mutables=None, donante='padre', p=True),
    'CEREBRO': dict(mutables=tuple(g for g in ME.NOMBRES if g not in VIDA_GENES), donante='padre', p=True),
    'AZAR': dict(mutables=None, donante='azar', p=True),
    'MUT0': dict(mutables=None, donante='padre', p=False),
}
JUZGADOS = ('VIDA', 'CEREBRO', 'AZAR')
DATOS = os.path.join(AQUI, 'datos')


def eco_cfg(brazo, t_corte, **extra):
    b = BRAZOS[brazo]
    return dict(refunda=1, t_corte=t_corte, p_mut=(SERIE['p_mut'] if b['p'] else 0.0), sigma=SERIE['sigma'], banco=SERIE['banco'],
                n_sombra=SERIE['n_sombra'], cada_gen=SERIE['cada_gen'], mutables=b['mutables'], donante=b['donante'], **extra)


def fundadores_juez(fuente, s):
    """Genomas de los 9 fundadores de la bateria en la semilla s. fuente = UN genoma (G0: 9 copias) o una LISTA de genomas
    (el banco en el corte: 9 entradas distintas al azar con el rng [s, 7], las mismas para cualquier lector).
    Candidato a ERR (humo 19001): la v1 del juez usaba la MEDIANA por gen del banco, y con mutaciones raras la mediana
    de cada gen ES G0 -> el juez comparaba G0 con G0 (el humo dio supervivencias identicas)."""
    a = np.asarray(fuente, float)
    if a.ndim == 1: return np.tile(a, (JUEZ['n'], 1))
    idx = np.random.default_rng([s, 7]).choice(len(a), size=JUEZ['n'], replace=len(a) < JUEZ['n'])
    return a[idx]


def juez(fuente, semillas, T_b, cache=None):
    """Bateria fija: 9 fundadores (fundadores_juez), sin mutacion ni reposicion. Mide cuanto vive la colonia (t_ext o T_b)."""
    out = []
    for s in semillas:
        gs = fundadores_juez(fuente, s)
        clave = (gs.round(9).tobytes(), s, T_b)
        if cache is not None and clave in cache: out.append(cache[clave]); continue
        r = ME.run_solapadas(s, [MUNDO['carro']] * JUEZ['n'], T=T_b, diag=0, mundo_n=JUEZ['esc'], tope_cuerpos=MUNDO['tope'],
                             muestra=MUNDO['muestra'], eco=dict(refunda=0, p_mut=0.0, genoma=gs.tolist()))
        te = r['eco']['t_ext']
        d = dict(s=s, t_ext=te, vive=(T_b if te is None else te), vivos_T=len(r['eco']['vivos_final']), nac=r['eco']['n_nac'])
        if cache is not None: cache[clave] = d
        out.append(d)
    return out


def sel_genes(fila_gen):
    """fila de gen_t, columnas del BANCO ([6] real, [7] sombras; el pool del que salen los genomas): por gen, +1 si el real
    supera a TODAS las sombras, -1 si queda por debajo de todas, 0 si no. Bajo neutralidad P(+1) = P(-1) = 1/9 por gen."""
    if fila_gen is None or len(fila_gen) < 8 or fila_gen[6] is None or not fila_gen[7]: return None
    real = np.array(fila_gen[6]); S = np.array(fila_gen[7])
    return [int(1 if real[j] > S[:, j].max() else (-1 if real[j] < S[:, j].min() else 0)) for j in range(len(real))]


def trabajo(args):
    """UNA corrida (semilla, brazo): vivero + corte, checkpoint reanudable, juez del genoma del corte. Escribe su JSON."""
    seed, brazo, T, t_corte, carpeta, n_juez, T_juez, reanuda = args
    fin = os.path.join(carpeta, f"{brazo}_s{seed}.json")
    if reanuda and os.path.exists(fin): return json.load(open(fin, encoding='utf-8'))
    ck = os.path.join(carpeta, 'ckpt', f"{brazo}_s{seed}.pkl"); os.makedirs(os.path.dirname(ck), exist_ok=True)
    filas = []   # individuos nacidos desde el corte (para R0 de cohorte tras el corte)

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
    r = ME.run_solapadas(seed, [MUNDO['carro']] * MUNDO['n0'], T=T, diag=0, mundo_n=MUNDO['esc'], tope_cuerpos=MUNDO['tope'],
                         muestra=MUNDO['muestra'],
                         eco=eco_cfg(brazo, t_corte, ckpt_cada=SERIE['ckpt_cada'], ckpt_fn=guarda, estado=estado, ind_cb=cb))
    E = r['eco']; P = r['pista']
    fila_corte = next((f for f in E['gen_t'] if f[0] == t_corte), None)
    coh = [f for f in filas if f[4] <= T - 20000]   # nacidos en [t_corte, T - 20000]: hijos (los vivos cuentan lo que llevan)
    res = dict(seed=seed, brazo=brazo, T=T, t_corte=t_corte, seg=round(time.time() - t0, 1), t_ext=E['t_ext'],
               persiste=int(E['t_ext'] is None and len(E['vivos_final']) > 0), vivos_T=len(E['vivos_final']),
               linajes_T=len(set(v[0] for v in E['vivos_final'])), gen_max_T=(max(v[2] for v in E['vivos_final']) if E['vivos_final'] else None),
               bloqueados=P['bloqueados'], max_vivos=P['max_vivos'], n_nac=E['n_nac'], n_refund=E['n_refund'], n_banco=E['n_banco'],
               tasa_mut=(E['n_mut'] / max(1, (E['n_nac'] + E['n_banco'])) / len(E['genes'])),
               nac_post=len(filas), r0_post=(round(float(np.mean([f[6] for f in coh])), 4) if coh else None), n_coh_post=len(coh),
               corte=E['corte'], sel_corte=sel_genes(fila_corte), gen_t=E['gen_t'], tam_total=P['tam_total'], genes=E['genes'], G0=E['G0'],
               vivos_final=E['vivos_final'][:500], juez=None)
    if brazo in JUZGADOS and E['corte'] and E['corte']['banco']:
        res['juez'] = dict(fuente='banco en el corte (9 entradas al azar por semilla)', med_banco=E['corte']['med_banco'],
                           bateria=juez(E['corte']['banco'], JUEZ['semillas'][:n_juez], T_juez))
    tmp = fin + '.tmp'
    with open(tmp, 'w', encoding='utf-8') as f: json.dump(res, f)
    os.replace(tmp, fin)
    if os.path.exists(ck): os.remove(ck)
    return res


# ================================================================================ LA LETRA (PREREGISTRO_eco.md §6)
def veredicto(R, G0bat, n_esperado=20):
    """R: lista de resultados de UNA serie (todas las semillas x brazos). G0bat: bateria del juez con G0 (semillas 19201-19220)."""
    L = []; by = {b: sorted([x for x in R if x['brazo'] == b], key=lambda x: x['seed']) for b in BRAZOS}
    n = {b: len(v) for b, v in by.items()}
    pers = {b: sum(x['persiste'] for x in v) for b, v in by.items()}
    L.append(f"semillas por brazo: {n}; persiste tras el corte (vivos en T): {pers}")
    completo = all(n[b] == n_esperado for b in BRAZOS)
    bloq = sum(x['bloqueados'] for x in R)
    g0_med = float(np.median([d['vive'] for d in G0bat])) if G0bat else None
    # P1 persistencia de VIDA; P1c control MUT0 (el que puede ganar)
    P1 = pers['VIDA'] >= 15
    P1c = pers['MUT0'] <= 2
    # P2 seleccion: un gen del BANCO fuera de sus 8 sombras con el mismo signo en >= 15/20 (VIDA); guardia: AZAR <= 8/20 en todo gen
    genes = R[0]['genes'] if R else []
    def cuenta(b):
        c = {}
        for j, g in enumerate(genes):
            s = [x['sel_corte'][j] for x in by[b] if x['sel_corte'] is not None]
            c[g] = (sum(1 for v in s if v > 0), sum(1 for v in s if v < 0))
        return c
    cV, cA = cuenta('VIDA'), cuenta('AZAR')
    sel = [g for g in genes if max(cV[g]) >= 15]
    falsos = [g for g in genes if max(cA[g]) > 8]   # bajo neutralidad P(>= 9/20 | p = 1/9) ~ 3e-4 por gen
    P2 = len(sel) >= 1
    P4 = pers['VIDA'] - pers['AZAR'] >= 8
    L.append(f"P2 genes seleccionados en VIDA (>=15/20 mismo signo fuera de las 8 sombras): {[(g, cV[g]) for g in sel]}; "
             f"AZAR con > 8/20 (falsos positivos del instrumento): {[(g, cA[g]) for g in falsos]}")
    # P3 juez: mediana de supervivencia en la bateria del genoma del corte > la de G0, en >= 15/20 semillas (VIDA); AZAR <= 10/20
    def gana(b):
        w = 0; m = []
        for x in by[b]:
            if x['juez']:
                v = float(np.median([d['vive'] for d in x['juez']['bateria']])); m.append(v); w += int(g0_med is not None and v > g0_med)
        return w, (float(np.median(m)) if m else None)
    wV, mV = gana('VIDA'); wA, mA = gana('AZAR'); wC, mC = gana('CEREBRO')
    P3 = wV >= 15
    P3c = wA <= 10
    L.append(f"P3 juez (supervivencia mediana en la bateria vs G0 = {g0_med}): VIDA gana {wV}/{n['VIDA']} (mediana {mV}); "
             f"AZAR {wA}/{n['AZAR']} ({mA}); CEREBRO {wC}/{n['CEREBRO']} ({mC})")
    Hc = pers['CEREBRO'] >= 15
    L.append(f"P1 VIDA persiste >= 15/20: {'SE CUMPLE' if P1 else 'NO'} ({pers['VIDA']}) · P1c MUT0 <= 2/20: {'SE CUMPLE' if P1c else 'NO'} ({pers['MUT0']}) · "
             f"P2 seleccion en genes: {'SE CUMPLE' if P2 else 'NO'} · P3 juez: {'SE CUMPLE' if P3 else 'NO'} · P3c AZAR <= 10/20: {'SE CUMPLE' if P3c else 'NO'} · "
             f"P4 VIDA - AZAR >= 8: {'SE CUMPLE' if P4 else 'NO'} ({pers['VIDA'] - pers['AZAR']}) · H-c CEREBRO persiste >= 15/20: {'SE CUMPLE' if Hc else 'NO'} ({pers['CEREBRO']})")
    if not completo: v = 'NO EVALUABLE (serie incompleta)'
    elif bloq > 0: v = f'NO EVALUABLE (tope de cuerpos alcanzado: bloqueados = {bloq}; la densidad no la regulo el mundo)'
    elif pers['MUT0'] >= 10: v = 'NO EVALUABLE (el control MUT0 persiste en >= 10/20: el vivero solo basta; el mundo es demasiado facil)'
    elif falsos: v = 'NO EVALUABLE (AZAR da falsos positivos de seleccion: el control de sombras no vale)'
    elif not P3c: v = 'NO EVALUABLE (AZAR gana el juez en > 10/20: el juez no distingue seleccion de azar; ERR-121, enmienda antes de la serie)'
    elif P1 and P1c and P2 and P3 and P4: v = 'FUNCIONA (en esta serie)'
    elif P2 and P3: v = 'HAY ALGO MODESTO (en esta serie)'
    else: v = 'NO (en esta serie)'
    L.append(f"VEREDICTO POR LA LETRA (una serie; el del bloque exige serie + replica con el mismo veredicto): {v}")
    return v, L, dict(P1=P1, P1c=P1c, P2=P2, P3=P3, P3c=P3c, P4=P4, Hc=Hc, pers=pers, sel=sel, falsos=falsos, wV=wV, wA=wA, wC=wC, g0_med=g0_med)


def g0_bateria(n_juez, T_juez, carpeta):
    ruta = os.path.join(carpeta, f"juez_G0_n{n_juez}_T{T_juez}.json")
    if os.path.exists(ruta): return json.load(open(ruta, encoding='utf-8'))
    CF = ME.genoma0(__import__('pista2').cfg_fabrica())
    b = juez(list(CF), JUEZ['semillas'][:n_juez], T_juez)
    json.dump(b, open(ruta, 'w', encoding='utf-8')); return b


def lee(carpeta, n_esperado=20):
    R = [json.load(open(p, encoding='utf-8')) for p in sorted(glob.glob(os.path.join(carpeta, '*_s*.json')))]
    G0b = next((json.load(open(p, encoding='utf-8')) for p in glob.glob(os.path.join(carpeta, 'juez_G0_*.json'))), [])
    v, L, d = veredicto(R, G0b, n_esperado)
    for l in L: print(l)
    return v, L, d, R


def main():
    ap = argparse.ArgumentParser(allow_abbrev=False)
    ap.add_argument('--humo', action='store_true'); ap.add_argument('--serie', action='store_true'); ap.add_argument('--lee', default=None)
    ap.add_argument('--desde', type=int); ap.add_argument('--n', type=int); ap.add_argument('--pool', type=int)
    ap.add_argument('--reanuda', action='store_true'); ap.add_argument('--prueba_pool', action='store_true')
    ap.add_argument('--largo', action='store_true')
    a = ap.parse_args()   # bandera desconocida -> error y salida 2 (ERR-115)
    modos = int(a.humo) + int(a.serie) + int(a.lee is not None) + int(a.largo)
    if modos != 1: raise SystemExit("ECO: exactamente uno de --humo, --serie, --lee, --largo")
    if a.humo:
        if any(v is not None for v in (a.desde, a.n, a.pool)) or a.reanuda or a.prueba_pool: raise SystemExit("ECO: --humo no admite otras banderas")
        return humo()
    if a.lee is not None:
        lee(a.lee); return
    if a.largo:   # ECO largo: VIDA y AZAR, 3 semillas, T = 1e6, corte en 1e5, checkpoint cada 10000, reanudable; sin veredicto
        if a.desde != LARGO['desde'] or a.n != LARGO['n'] or a.pool is None or not 1 <= a.pool <= 7 or a.prueba_pool:
            raise SystemExit(f"ECO: --largo --desde {LARGO['desde']} --n {LARGO['n']} --pool 6 [--reanuda]")
        carpeta = os.path.join(DATOS, f"eco_largo_s{a.desde}-{a.desde + a.n - 1}")
        if os.path.exists(carpeta) and not a.reanuda and glob.glob(os.path.join(carpeta, '*_s*.json')): raise SystemExit('ECO: ya hay resultados; --reanuda')
        os.makedirs(carpeta, exist_ok=True)
        jobs = [(s, b, LARGO['T'], LARGO['t_corte'], carpeta, len(JUEZ['semillas']), JUEZ['T_b'], a.reanuda)
                for s in range(a.desde, a.desde + a.n) for b in LARGO['brazos']]
        from multiprocessing import Pool
        with Pool(a.pool) as pool:
            for r in pool.imap_unordered(trabajo, jobs): print(f"{r['brazo']} s{r['seed']}: persiste {r['persiste']} t_ext {r['t_ext']} vivos_T {r['vivos_T']} ({r['seg']} s)", flush=True)
        print('VEREDICTO: ninguno (el largo es exploratorio: lo que aparezca se preregistra y se replica en semillas nuevas)'); return
    # --serie
    if a.pool is None or not 1 <= a.pool <= 7: raise SystemExit("ECO: --serie exige --pool entre 1 y 7 (regla de 2 Pools / 14 procesos)")
    if a.prueba_pool:   # prueba de la ruta del Pool (numeros sin valor): 2 semillas de practica, T corto
        if a.desde is None or not 19031 <= a.desde <= 19039 or a.n != 2: raise SystemExit("ECO: --prueba_pool usa --desde 19031..19039 --n 2")
        T, tc, nj, Tj = 3000, 2000, 2, 2000; etq = f"prueba_pool_s{a.desde}"
    else:
        if a.desde not in VENTANAS or a.n != 20: raise SystemExit(f"ECO: la serie es --desde {VENTANAS[0]} (serie) o {VENTANAS[1]} (replica) con --n 20")
        T, tc, nj, Tj = SERIE['T'], SERIE['t_corte'], len(JUEZ['semillas']), JUEZ['T_b']; etq = f"serie_s{a.desde}-{a.desde + a.n - 1}"
    carpeta = os.path.join(DATOS, f"eco_{etq}")
    if os.path.exists(carpeta) and not a.reanuda and glob.glob(os.path.join(carpeta, '*_s*.json')):
        raise SystemExit(f"ECO: {carpeta} ya tiene resultados; usa --reanuda o borra a mano (no se pisa nada)")
    os.makedirs(carpeta, exist_ok=True)
    jobs = [(s, b, T, tc, carpeta, nj, Tj, a.reanuda) for s in range(a.desde, a.desde + a.n) for b in ('VIDA', 'CEREBRO', 'AZAR', 'MUT0')]
    t0 = time.time()
    from multiprocessing import Pool
    with Pool(a.pool) as pool:
        G0r = pool.apply_async(g0_bateria, (nj, Tj, carpeta))
        for k, r in enumerate(pool.imap_unordered(trabajo, jobs), 1):
            print(f"[{k}/{len(jobs)}] {r['brazo']} s{r['seed']}: persiste {r['persiste']} t_ext {r['t_ext']} vivos_T {r['vivos_T']} "
                  f"({r['seg']} s; {round(time.time() - t0)} s)", flush=True)
        G0r.get()
    v, L, d, R = lee(carpeta, a.n)
    json.dump(dict(etiqueta=etq, veredicto=v, lineas=L, d={k: (list(x) if isinstance(x, tuple) else x) for k, x in d.items()},
                   seg=round(time.time() - t0), MUNDO=MUNDO, SERIE=SERIE, JUEZ=dict(JUEZ, semillas=list(JUEZ['semillas'])),
                   motor_sha=ME_SHA()), open(os.path.join(carpeta, 'RESUMEN.json'), 'w', encoding='utf-8'), indent=1)
    print(f"VEREDICTO: {v}")


def ME_SHA():
    import hashlib
    return {p: hashlib.sha256(open(os.path.join(AQUI, p), 'rb').read()).hexdigest()[:16]
            for p in ('motor_eco.py', 'carros/FABRICA_ECO.py', 'corre_eco.py')}


def humo():
    """UN proceso, UNA semilla de practica, brazo VIDA, T corto. Numeros de humo: no deciden nada. Escribe su JSON."""
    os.makedirs(os.path.join(DATOS, 'humo'), exist_ok=True)
    ts = time.strftime('%Y%m%d_%H%M%S'); carpeta = os.path.join(DATOS, 'humo', f"eco_humo_s{HUMO['semilla']}_{ts}")
    os.makedirs(carpeta, exist_ok=True); t0 = time.time()
    r = trabajo((HUMO['semilla'], HUMO['brazo'], HUMO['T'], HUMO['t_corte'], carpeta, HUMO['juez_semillas'], HUMO['juez_T'], False))
    G0b = juez(list(ME.genoma0(__import__('pista2').cfg_fabrica())), JUEZ['semillas'][:HUMO['juez_semillas']], HUMO['juez_T'])
    json.dump(G0b, open(os.path.join(carpeta, 'juez_G0.json'), 'w', encoding='utf-8'))
    pasos_s = HUMO['T'] / max(r['seg'], 1e-9)
    cuerpos_medios = float(np.mean(r['tam_total']))
    us = r['seg'] / max(1.0, sum(r['tam_total']) * MUNDO['muestra']) * 1e6
    print(f"HUMO VIDA s{HUMO['semilla']} T={HUMO['T']} corte={HUMO['t_corte']}: {r['seg']} s, {pasos_s:.1f} pasos/s, "
          f"{cuerpos_medios:.1f} cuerpos de media, ~{us:.0f} us por cuerpo y paso")
    print(f"  persiste {r['persiste']} · t_ext {r['t_ext']} · vivos_T {r['vivos_T']} · linajes_T {r['linajes_T']} · nac {r['n_nac']} · "
          f"refund {r['n_refund']} (desde banco {r['n_banco']}) · tasa de mutacion por gen {r['tasa_mut']:.4f} (p = {SERIE['p_mut']})")
    print(f"  corte: {r['corte'] and {k: r['corte'][k] for k in ('t', 'vivos', 'n_banco')}} · sel_corte {r['sel_corte']}")
    if r['juez']:
        print(f"  juez (genoma del corte, {HUMO['juez_semillas']} semillas, T_b {HUMO['juez_T']}): {[d['vive'] for d in r['juez']['bateria']]} · G0: {[d['vive'] for d in G0b]}")
    est = {N: us * N * 1e-6 for N in (100, 300, 1000)}
    print("  costo estimado por proceso: " + '; '.join(f"N={N}: 1e6 pasos {v * 1e6 / 3600:.1f} h, 1e7 pasos {v * 1e7 / 3600:.0f} h" for N, v in est.items()))
    v, L, d = veredicto([r], G0b, n_esperado=20)
    for l in L: print('  ' + l)
    out = dict(humo=HUMO, MUNDO=MUNDO, SERIE=SERIE, resultado=r, juez_G0=G0b, veredicto_de_prueba=v, lineas=L, seg_total=round(time.time() - t0, 1),
               pasos_s=pasos_s, us_cuerpo_paso=us, shas=ME_SHA())
    ruta = os.path.join(DATOS, 'humo', f"eco_humo_s{HUMO['semilla']}_{ts}.json")
    json.dump(out, open(ruta, 'w', encoding='utf-8'))
    print(f"  JSON: {os.path.relpath(ruta, RAIZ)}")
    print(f"VEREDICTO (humo, una semilla, no decide): {v}")


if __name__ == '__main__':
    main()
