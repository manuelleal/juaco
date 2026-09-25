"""corre_eco_v12.py — RUNNER y JUEZ de JUACO-ECO v1.2 (nivel 10): SELECCION + LA FAMILIA PASA SU TABLA. Nube, 24-sep-2026.

MISION: llegar a la AGI por este camino.

Preregistro: experimentos/juaco_eco/PREREGISTRO_eco_v12.md (la letra esta AQUI, en veredicto(), y alli).
ECO v1.2 = ECO v1.1 (mismo mundo esc 90, mismo vivero, corte en 60 000, T = 1e6, misma mutacion, banco y sombras, juez v2 con placebo)
con UN cambio de mecanismo en tres de sus cuatro brazos: el carro FAMB_RES0_ECO (la familia pasa su tabla en el parto, sin las entradas
neutras: el RES_SIN0 de subida_n10c, bit a bit; arnes identidad_eco_familia.py 7/7). Brazos:
  VIDA_T = VIDA + FAMB_RES0_ECO · AZAR_T = AZAR + FAMB_RES0_ECO · MUT0_T = MUT0 + FAMB_RES0_ECO · VIDA = VIDA + FABRICA_ECO (el v1.1).
Juez v2 (colonia del banco de VIDA_T contra la de AZAR_T, con el carro de la familia) en una bateria sellada NUEVA 19801-19820 con
T_b = 100 000 (con la familia las colonias pueden llegar al techo de 20 000; ver preregistro §2).
Motor: --serie SOLO con el gemelo motor_eco_rapido_fam (vale mientras su arnes de N/N); --humo con el motor Python (o --gemelo).

Uso (ERR-115: banderas desconocidas o abreviadas abortan; --help no existe):
  python experimentos/juaco_eco/corre_eco_v12.py --humo [--gemelo]
  python experimentos/juaco_eco/corre_eco_v12.py --prueba_pool --desde 19902 --n 2 --pool 2
  python experimentos/juaco_eco/corre_eco_v12.py --serie --desde 19701 --n 20 --pool 3        # serie
  python experimentos/juaco_eco/corre_eco_v12.py --serie --desde 19721 --n 20 --pool 3        # replica
  python experimentos/juaco_eco/corre_eco_v12.py --serie --desde 19701 --n 20 --pool 3 --reanuda
  python experimentos/juaco_eco/corre_eco_v12.py --lee <carpeta de la serie>
"""
import argparse, glob, hashlib, json, os, pickle, sys, time
import numpy as np

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
if AQUI not in sys.path: sys.path.insert(0, AQUI)
import corre_eco as CR           # el runner de v1 (eco_cfg, sel_genes, MUNDO, SERIE); su ME es el motor PYTHON hasta que se enchufe el gemelo
import motor_eco as ME_PY
import corre_eco_v11 as V11     # fundadores (flujo 7/8), med_bat; importarlo enchufa el gemelo VIEJO (FABRICA_ECO) en CR.ME: se deshace abajo

CR.ME = ME_PY                    # punto de partida: motor Python (el gemelo nuevo se enchufa SOLO con usa_gemelo())
MUNDO = CR.MUNDO
SERIE = CR.SERIE
V12 = dict(T=1_000_000, t_corte=60000, T_lect=120000, gen_largo=50000)
JUEZ3 = dict(esc=9, n=9, T_b=100000, semillas=tuple(range(19801, 19821)), flujo=7, flujo_placebo=8)
VENTANAS = (19701, 19721)
PRACTICA = tuple(range(19901, 19910))   # humo 19905; prueba del Pool 19902-19904 (el compilador usa 19901-19909 en su arnes: son practica)
HUMO = dict(semilla=19905, brazos=('VIDA_T', 'AZAR_T'), T=30000, t_corte=8000, T_lect=12000, juez_semillas=2, juez_T=6000)
FAM = 'FAMB_RES0_ECO'; FAB = 'FABRICA_ECO'
BRAZOS = {'VIDA_T': ('VIDA', FAM), 'AZAR_T': ('AZAR', FAM), 'MUT0_T': ('MUT0', FAM), 'VIDA': ('VIDA', FAB)}
JUZGADOS = ('VIDA_T', 'AZAR_T')      # juez v2 y placebo, los dos con el carro de la familia
DATOS = os.path.join(AQUI, 'datos')


class BanderaMala(SystemExit):
    pass


def usa_gemelo():
    """Enchufa el gemelo numba de FAMB_RES0_ECO y FABRICA_ECO (motor_eco_rapido_fam) en CR.ME, como corre_eco_rapido hace con el suyo."""
    import types
    import motor_eco_rapido_fam as MF
    g = types.ModuleType('motor_eco_gemelo_fam')
    g.__dict__.update({k: v for k, v in ME_PY.__dict__.items() if not k.startswith('__')})
    g.run_solapadas = MF.run_solapadas
    CR.ME = g
    return MF


def juez(fuente, semillas, T_b, flujo, carro):
    """Bateria: colonia de 9 genomas (V11.fundadores: 9 entradas al azar del banco con el rng [s, flujo], o 9 copias de un genoma), mundo
    esc 9, sin mutacion ni reposicion, con el carro dado. Mide cuanto vive (t_ext o T_b) y cuantos nacen."""
    out = []
    for s in semillas:
        gs = V11.fundadores(fuente, s, flujo)
        r = CR.ME.run_solapadas(s, [carro] * JUEZ3['n'], T=T_b, diag=0, mundo_n=JUEZ3['esc'], tope_cuerpos=MUNDO['tope'],
                                muestra=MUNDO['muestra'], eco=dict(refunda=0, p_mut=0.0, genoma=gs.tolist()))
        te = r['eco']['t_ext']
        out.append(dict(s=s, t_ext=te, vive=(T_b if te is None else te), vivos_T=len(r['eco']['vivos_final']), nac=r['eco']['n_nac']))
    return out


def trabajo(args):
    """UNA corrida (semilla, brazo) hasta T: vivero + corte (= v1.1) con el carro del brazo; lectura descriptiva en T_lect; juez v2 y
    placebo del banco del corte en los JUZGADOS. Checkpoint reanudable. Escribe su JSON."""
    seed, brazo, T, t_corte, T_lect, carpeta, n_juez, T_juez, reanuda = args
    gen_brazo, carro = BRAZOS[brazo]
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
    r = CR.ME.run_solapadas(seed, [carro] * MUNDO['n0'], T=T, diag=0, mundo_n=MUNDO['esc'], tope_cuerpos=MUNDO['tope'],
                            muestra=MUNDO['muestra'],
                            eco=CR.eco_cfg(gen_brazo, t_corte, ckpt_cada=SERIE['ckpt_cada'], ckpt_fn=guarda, estado=estado, ind_cb=cb))
    E = r['eco']; P = r['pista']
    fila_corte = next((f for f in E['gen_t'] if f[0] == t_corte), None)
    fila_lect = next((f for f in E['gen_t'] if f[0] == T_lect), None)
    te = E['t_ext']
    pers_lect = int(te is None or te > T_lect)
    coh = [f for f in filas if f[4] <= T - 20000]
    vivos_t = [[f[0], f[1]] for f in E['gen_t'] if f[0] >= t_corte and f[0] % V12['gen_largo'] == 0]
    res = dict(seed=seed, brazo=brazo, genetica=gen_brazo, carro=carro, T=T, t_corte=t_corte, T_lect=T_lect, seg=round(time.time() - t0, 1),
               t_ext=te, persiste=int(te is None and len(E['vivos_final']) > 0), persiste_lect=pers_lect,
               vivos_lect=(fila_lect[1] if fila_lect is not None else (0 if not pers_lect else None)),
               vivos_T=len(E['vivos_final']), linajes_T=len(set(v[0] for v in E['vivos_final'])),
               gen_max_T=(max(v[2] for v in E['vivos_final']) if E['vivos_final'] else None), vivos_t=vivos_t,
               bloqueados=P['bloqueados'], max_vivos=P['max_vivos'], n_nac=E['n_nac'], n_refund=E['n_refund'], n_banco=E['n_banco'],
               tasa_mut=(E['n_mut'] / max(1, (E['n_nac'] + E['n_banco'])) / len(E['genes'])),
               nac_post=len(filas), r0_post=(round(float(np.mean([f[6] for f in coh])), 4) if coh else None), n_coh_post=len(coh),
               corte=E['corte'], sel_corte=CR.sel_genes(fila_corte),
               gen_t=[f for f in E['gen_t'] if f[0] <= T_lect or f[0] % V12['gen_largo'] == 0], tam_total=P['tam_total'],
               genes=E['genes'], G0=E['G0'], vivos_final=E['vivos_final'][:500], juez=None, juez_placebo=None,
               motor=('GEMELO motor_eco_rapido_fam' if CR.ME is not ME_PY else 'PYTHON motor_eco'))
    if brazo in JUZGADOS and E['corte'] and E['corte']['banco']:
        sem = JUEZ3['semillas'][:n_juez]
        res['juez'] = dict(fuente='banco en el corte (9 entradas al azar por semilla, flujo 7)', carro=FAM, med_banco=E['corte']['med_banco'],
                           bateria=juez(E['corte']['banco'], sem, T_juez, JUEZ3['flujo'], FAM))
        res['juez_placebo'] = dict(fuente='el MISMO banco, otra muestra de 9 (flujo 8)', carro=FAM,
                                   bateria=juez(E['corte']['banco'], sem, T_juez, JUEZ3['flujo_placebo'], FAM))
    tmp = fin + '.tmp'
    with open(tmp, 'w', encoding='utf-8') as f: json.dump(res, f)
    os.replace(tmp, fin)
    if os.path.exists(ck): os.remove(ck)
    return res


def g0_bateria(n_juez, T_juez, carpeta):
    """G0 (9 copias) con el carro de la familia en la bateria sellada: DESCRIPTIVO, no decide."""
    ruta = os.path.join(carpeta, f"juez_G0_{FAM}_n{n_juez}_T{T_juez}.json")
    if os.path.exists(ruta): return json.load(open(ruta, encoding='utf-8'))
    G0 = ME_PY.genoma0(__import__('pista2').cfg_fabrica())
    b = juez(list(G0), JUEZ3['semillas'][:n_juez], T_juez, JUEZ3['flujo'], FAM)
    json.dump(b, open(ruta, 'w', encoding='utf-8')); return b


# ================================================================================ LA LETRA (PREREGISTRO_eco_v12.md §6)
def veredicto(R, G0bat, n_esperado=20):
    L = []; by = {b: sorted([x for x in R if x['brazo'] == b], key=lambda x: x['seed']) for b in BRAZOS}
    n = {b: len(v) for b, v in by.items()}
    pers = {b: sum(x['persiste'] for x in v) for b, v in by.items()}
    pers_l = {b: sum(x['persiste_lect'] for x in v) for b, v in by.items()}
    completo = all(n[b] == n_esperado for b in BRAZOS) and all(x['T'] == V12['T'] for x in R)
    bloq = sum(x['bloqueados'] for x in R)
    L.append(f"semillas por brazo: {n}; persiste en T = {V12['T']}: {pers}; en {V12['T_lect']} (descriptivo): {pers_l}")
    r0 = {b: [x['r0_post'] for x in v if x['persiste'] and x['r0_post'] is not None] for b, v in by.items()}
    viv = {b: [x['vivos_T'] for x in v if x['persiste']] for b, v in by.items()}
    L.append(f"descriptivo: R0 tras el corte en los que persisten (mediana) { {b: (round(float(np.median(v)), 4) if v else None) for b, v in r0.items()} }; "
             f"cuerpos vivos en T en los que persisten (mediana) { {b: (float(np.median(v)) if v else None) for b, v in viv.items()} }; "
             f"max_vivos (max) { {b: max((x['max_vivos'] for x in v), default=None) for b, v in by.items()} }")
    F1 = pers['VIDA_T'] >= 15
    F2 = pers['VIDA_T'] - pers['VIDA'] >= 6
    genes = R[0]['genes'] if R else []

    def cuenta(b):
        c = {}
        for j, g in enumerate(genes):
            s = [x['sel_corte'][j] for x in by[b] if x['sel_corte'] is not None]
            c[g] = (sum(1 for v in s if v > 0), sum(1 for v in s if v < 0))
        return c
    cV, cA = cuenta('VIDA_T'), cuenta('AZAR_T')
    sel = [g for g in genes if max(cV[g]) >= 15]
    falsos = [g for g in genes if max(cA[g]) > 8]
    F4 = len(sel) >= 1
    L.append(f"F4 genes seleccionados en VIDA_T (>=15/20 mismo signo fuera de las 8 sombras): {[(g, cV[g]) for g in sel]}; "
             f"AZAR_T con > 8/20 (falsos positivos): {[(g, cA[g]) for g in falsos]}")
    m = {b: {x['seed']: (V11.med_bat(x['juez']['bateria']) if x.get('juez') else None) for x in by[b]} for b in JUZGADOS}
    mp = {b: {x['seed']: (V11.med_bat(x['juez_placebo']['bateria']) if x.get('juez_placebo') else None) for x in by[b]} for b in JUZGADOS}
    w = e = k = 0
    for s in sorted(set(m['VIDA_T']) & set(m['AZAR_T'])):
        a, b = m['VIDA_T'][s], m['AZAR_T'][s]
        if a is None or b is None: continue
        k += 1; w += int(a > b); e += int(a == b)
    F3 = w >= 15
    plac = {}
    for b in JUZGADOS:
        pw = pe = pk = 0
        for s, v in m[b].items():
            u = mp[b].get(s)
            if v is None or u is None: continue
            pk += 1; pw += int(v > u); pe += int(v == u)
        plac[b] = (pw + 0.5 * pe, pk)
    placebo_ok = all(pk == n_esperado and 5 <= p <= 15 for p, pk in plac.values())
    g0_med = V11.med_bat(G0bat)
    L.append(f"F3 juez v2 (bateria sellada 19801-19820, T_b {JUEZ3['T_b']}, carro de la familia): VIDA_T > AZAR_T (pareado, estricto) "
             f"{w}/{k} (empates {e}); medianas VIDA_T {V11.med_bat([dict(vive=v) for v in m['VIDA_T'].values() if v is not None])} · "
             f"AZAR_T {V11.med_bat([dict(vive=v) for v in m['AZAR_T'].values() if v is not None])} · G0 (descriptivo) {g0_med}")
    L.append(f"PLACEBO (flujo 7 contra 8 del MISMO banco; valido en [5, 15] de 20): { {b: p for b, p in plac.items()} } -> "
             f"{'VALIDO' if placebo_ok else 'NO VALIDO'}")
    L.append(f"F1 VIDA_T persiste en 1e6 >= 15/20: {'SE CUMPLE' if F1 else 'NO'} ({pers['VIDA_T']}) · F2 VIDA_T - VIDA >= 6: "
             f"{'SE CUMPLE' if F2 else 'NO'} ({pers['VIDA_T'] - pers['VIDA']}) · F3 VIDA_T > AZAR_T >= 15/20: {'SE CUMPLE' if F3 else 'NO'} ({w}) · "
             f"F4: {'SE CUMPLE' if F4 else 'NO'} · C (descriptivo) MUT0_T persiste {pers['MUT0_T']}/20, AZAR_T {pers['AZAR_T']}/20")
    if not completo: v = 'NO EVALUABLE (serie incompleta o T distinto de 1e6)'
    elif bloq > 0: v = f'NO EVALUABLE (tope de cuerpos alcanzado: bloqueados = {bloq})'
    elif falsos: v = 'NO EVALUABLE (AZAR_T da falsos positivos de seleccion: el control de sombras no vale)'
    elif not placebo_ok: v = 'NO EVALUABLE (el placebo del juez sale de [5, 15]: el juez no esta calibrado)'
    elif F1 and F2 and F3 and F4: v = 'FUNCIONA (en esta serie)'
    elif F1 and F2: v = 'HAY ALGO MODESTO: PERSISTE CON FAMILIA (en esta serie; la seleccion no se distingue con el juez)'
    elif F3 and F4: v = 'HAY ALGO MODESTO: SELECCION CON FAMILIA (en esta serie; no persiste largo en >= 15/20 o la familia no suma)'
    else: v = 'NO (en esta serie)'
    L.append(f"VEREDICTO v1.2 POR LA LETRA (una serie; el del bloque exige serie + replica con el mismo veredicto): {v}")
    return v, L, dict(F1=F1, F2=F2, F3=F3, F4=F4, pers=pers, pers_lect=pers_l, sel=sel, falsos=falsos, w=w, e=e,
                      placebo={b: list(p) for b, p in plac.items()}, placebo_ok=placebo_ok, g0_med=g0_med)


def lee(carpeta, n_esperado=20):
    R = [json.load(open(p, encoding='utf-8')) for p in sorted(glob.glob(os.path.join(carpeta, '*_s*.json')))]
    G0b = next((json.load(open(p, encoding='utf-8')) for p in glob.glob(os.path.join(carpeta, 'juez_G0_*.json'))), [])
    v, L, d = veredicto(R, G0b, n_esperado)
    for l in L: print(l, flush=True)
    return v, L, d, R


def SHAS():
    f = lambda p: hashlib.sha256(open(os.path.join(AQUI, p), 'rb').read()).hexdigest()[:16]
    return {p: f(p) for p in ('corre_eco_v12.py', 'corre_eco_v11.py', 'corre_eco.py', 'motor_eco.py', 'motor_eco_rapido_fam.py',
                              'carros/FABRICA_ECO.py', 'carros/FAMB_RES0_ECO.py', 'PREREGISTRO_eco_v12.md') if os.path.exists(os.path.join(AQUI, p))}


def parsea(argv):
    ap = argparse.ArgumentParser(allow_abbrev=False, add_help=False)
    ap.add_argument('--humo', action='store_true'); ap.add_argument('--serie', action='store_true')
    ap.add_argument('--prueba_pool', action='store_true'); ap.add_argument('--lee', default=None)
    ap.add_argument('--desde', type=int); ap.add_argument('--n', type=int); ap.add_argument('--pool', type=int)
    ap.add_argument('--reanuda', action='store_true'); ap.add_argument('--gemelo', action='store_true')
    try:
        a, resto = ap.parse_known_args(argv)
    except SystemExit:
        raise BanderaMala('ECO v1.2: banderas mal formadas')
    if resto: raise BanderaMala(f"ECO v1.2: banderas desconocidas {resto}")
    if any(x.startswith('--') and '=' in x for x in argv): raise BanderaMala('ECO v1.2: sin la forma --bandera=valor')
    if len(argv) != len(set(x for x in argv if x.startswith('--'))) + sum(1 for x in argv if not x.startswith('--')):
        raise BanderaMala('ECO v1.2: bandera repetida')
    modos = int(a.humo) + int(a.serie) + int(a.prueba_pool) + int(a.lee is not None)
    if modos != 1: raise BanderaMala('ECO v1.2: exactamente uno de --humo, --serie, --prueba_pool, --lee')
    if a.humo and (a.desde is not None or a.n is not None or a.pool is not None or a.reanuda): raise BanderaMala('ECO v1.2: --humo sólo admite --gemelo')
    if a.lee is not None and (a.desde is not None or a.n is not None or a.pool is not None or a.reanuda or a.gemelo):
        raise BanderaMala('ECO v1.2: --lee va solo')
    if a.prueba_pool and (a.desde not in (19902, 19903) or a.n != 2 or a.pool != 2 or a.reanuda or a.gemelo):
        raise BanderaMala('ECO v1.2: --prueba_pool --desde 19902|19903 --n 2 --pool 2 (siempre con el gemelo)')
    if a.serie and (a.desde not in VENTANAS or a.n != 20 or a.pool is None or not 1 <= a.pool <= 3 or a.gemelo):
        raise BanderaMala(f"ECO v1.2: --serie --desde {VENTANAS[0]} (serie) o {VENTANAS[1]} (replica) --n 20 --pool 1..3 (siempre con el gemelo)")
    return a


def humo(gemelo):
    if gemelo: usa_gemelo()
    os.makedirs(os.path.join(DATOS, 'humo'), exist_ok=True)
    ts = time.strftime('%Y%m%d_%H%M%S'); etq = f"eco_v12_humo_s{HUMO['semilla']}_{'gemelo' if gemelo else 'python'}_{ts}"
    carpeta = os.path.join(DATOS, 'humo', etq); os.makedirs(carpeta, exist_ok=True); t0 = time.time()
    print(f"[{time.strftime('%H:%M:%S')}] HUMO ECO v1.2 ({'gemelo' if gemelo else 'Python'}) · shas {SHAS()}", flush=True)
    R = []
    for b in HUMO['brazos']:
        r = trabajo((HUMO['semilla'], b, HUMO['T'], HUMO['t_corte'], HUMO['T_lect'], carpeta, HUMO['juez_semillas'], HUMO['juez_T'], False))
        R.append(r)
        print(f"[{time.strftime('%H:%M:%S')}] {b} s{r['seed']}: {r['seg']} s · persiste_lect {r['persiste_lect']} (vivos {r['vivos_lect']}) · "
              f"persiste en T {r['persiste']} (vivos {r['vivos_T']}) · t_ext {r['t_ext']} · max_vivos {r['max_vivos']} · "
              f"juez {[d['vive'] for d in r['juez']['bateria']] if r['juez'] else None} · placebo "
              f"{[d['vive'] for d in r['juez_placebo']['bateria']] if r['juez_placebo'] else None}", flush=True)
    G0b = juez(list(ME_PY.genoma0(__import__('pista2').cfg_fabrica())), JUEZ3['semillas'][:HUMO['juez_semillas']], HUMO['juez_T'], 7, FAM)
    v, L, d = veredicto(R, G0b, n_esperado=20)
    for l in L: print('  ' + l, flush=True)
    ruta = os.path.join(DATOS, 'humo', etq + '.json')
    json.dump(dict(humo=HUMO, V12=V12, JUEZ3=dict(JUEZ3, semillas=list(JUEZ3['semillas'])), R=R, G0=G0b, veredicto_de_prueba=v,
                   lineas=L, seg=round(time.time() - t0, 1), shas=SHAS()), open(ruta, 'w', encoding='utf-8'))
    print(f"  JSON: {os.path.relpath(ruta, RAIZ)}  ({round(time.time() - t0, 1)} s)")
    print(f"VEREDICTO (humo, una semilla, no decide): {v}")


def main(argv=None):
    a = parsea(sys.argv[1:] if argv is None else argv)
    if a.humo: return humo(a.gemelo)
    if a.lee is not None:
        lee(a.lee); return
    usa_gemelo()
    if a.prueba_pool:
        T, tc, tl, nj, Tj = 3000, 2000, 2500, 2, 2000; etq = f"v12_prueba_pool_s{a.desde}"
    else:
        T, tc, tl, nj, Tj = V12['T'], V12['t_corte'], V12['T_lect'], len(JUEZ3['semillas']), JUEZ3['T_b']
        etq = f"v12_serie_s{a.desde}-{a.desde + a.n - 1}"
    carpeta = os.path.join(DATOS, f"eco_{etq}")
    if os.path.exists(carpeta) and not a.reanuda and glob.glob(os.path.join(carpeta, '*_s*.json')):
        raise SystemExit(f"ECO v1.2: {carpeta} ya tiene resultados; --reanuda (no se pisa nada)")
    os.makedirs(carpeta, exist_ok=True)
    flog = open(os.path.join(carpeta, 'progreso.log'), 'a', encoding='utf-8')

    def log(s):
        s = f"[{time.strftime('%H:%M:%S')}] {s}"; print(s, flush=True); flog.write(s + '\n'); flog.flush()
    log(f"ECO v1.2 {etq} · T {T} · corte {tc} · juez {nj} semillas T_b {Tj} · pool {a.pool} · motor GEMELO · shas {SHAS()}")
    jobs = [(s, b, T, tc, tl, carpeta, nj, Tj, a.reanuda) for s in range(a.desde, a.desde + a.n) for b in BRAZOS]
    t0 = time.time()
    from multiprocessing import Pool
    with Pool(a.pool, initializer=usa_gemelo) as pool:
        G0r = pool.apply_async(g0_bateria, (nj, Tj, carpeta))
        for k, r in enumerate(pool.imap_unordered(trabajo, jobs), 1):
            log(f"[{k}/{len(jobs)}] {r['brazo']} s{r['seed']}: persiste {r['persiste']} (vivos {r['vivos_T']}) · persiste_lect {r['persiste_lect']} "
                f"· t_ext {r['t_ext']} · max_vivos {r['max_vivos']} ({r['seg']} s; {round(time.time() - t0)} s)")
        G0r.get()
    v, L, d, R = lee(carpeta, a.n)
    for l in L: flog.write(l + '\n')
    json.dump(dict(etiqueta=etq, veredicto=v, lineas=L, d=d, seg=round(time.time() - t0), MUNDO=MUNDO, SERIE=SERIE, V12=V12,
                   JUEZ3=dict(JUEZ3, semillas=list(JUEZ3['semillas'])), BRAZOS=BRAZOS, shas=SHAS()),
              open(os.path.join(carpeta, 'RESUMEN.json'), 'w', encoding='utf-8'), indent=1, default=str)
    log(f"VEREDICTO: {v}")
    flog.close()


if __name__ == '__main__':
    try:
        main()
    except BanderaMala as e:
        print(str(e), file=sys.stderr); sys.exit(2)
