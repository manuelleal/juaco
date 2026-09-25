"""corre_frio.py — RUNNER y LETRA de F1 ARRANQUE EN FRIO (comite de linaje, ficha F1; 25-sep-2026).

MISION: llegar a la AGI por este camino (organismo minimo con reglas locales, sin retropropagacion, peldanos preregistrados con
controles y replicas). Meta del director: MANTENER EL LINAJE SIN ANDAMIO.

Preregistro: PREREGISTRO_frio.md (la letra esta AQUI, en veredicto(), y alli).
Envoltorio de experimentos/juaco_eco/corre_eco_v12.py (sha 1340d268e1fd93d8; se IMPORTA, no se toca): mismo mundo (w90: esc 90,
90 fundadores, quimiostato, tope 3000), misma plomeria de ECO (eco_cfg de corre_eco, banco, checkpoint cada 10 000), la misma
genetica MUT0 (sin mutacion) en todos los brazos. Lo unico que cambia por brazo es el CARRO y t_corte (fin del vivero):
  RES0_FRIO  MUT0 + FAMB_RES0_ECO, t_corte = 1      (sin vivero desde el inicio: el vivero solo podria refundar en t = 0)
  RES0_10k   MUT0 + FAMB_RES0_ECO, t_corte = 10 000 (dosis de vivero)
  RES0_60k   MUT0 + FAMB_RES0_ECO, t_corte = 60 000 (ANCLA: == MUT0_T de ECO v1.2 bit a bit; arnes bloque B)
  BAR0_FRIO  MUT0 + BAR0_ECO,      t_corte = 1      (control de contenido: la misma tabla con las R permutadas)
  FAB_FRIO   MUT0 + FABRICA_ECO,   t_corte = 1      (sin familia)
Motor: motor_frio_rapido.py (gemelo del arnes 132/132 copiado por anclas; + BAR0; ERR-146 guardia a 1e9). El motor Python solo en
el arnes.
nube-9 / ERR-60 (declarado ANTES de correr): trabajo() atrapa TODA excepcion del motor (SystemExit incluida) y devuelve un
resultado marcado en vez de matar al trabajador del Pool. Si el mensaje es la guardia ERR-60 (un linaje paso el limite de cuerpos):
el linaje estaba VIVO -> persiste = 1 con marca guardia = 1 (su R0 se calcula con la cohorte registrada hasta el aborto). Cualquier
otro aborto: persiste = None y la serie queda NO EVALUABLE.

Uso (ERR-115: banderas desconocidas o abreviadas abortan; --help no existe; SOLO el coordinador lanza --serie):
  python experimentos/organelos/frio/corre_frio.py --humo                                   # 1 proceso, 35905, 5 brazos, T 200 000
  python experimentos/organelos/frio/corre_frio.py --serie --desde 35001 --n 20 --pool 6    # serie
  python experimentos/organelos/frio/corre_frio.py --serie --desde 35021 --n 20 --pool 6    # replica
  python experimentos/organelos/frio/corre_frio.py --serie --desde 35001 --n 20 --pool 6 --reanuda
  python experimentos/organelos/frio/corre_frio.py --lee <carpeta de la serie>
"""
import argparse, glob, hashlib, importlib.util, json, os, pickle, sys, time
import numpy as np

try: sys.stdout.reconfigure(encoding='utf-8', errors='replace')
except Exception: pass
AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(AQUI)))
ECO = os.path.join(RAIZ, 'experimentos', 'juaco_eco')
for _d in (ECO, AQUI):
    if _d not in sys.path: sys.path.insert(0, _d)
import corre_eco_v12 as V12      # importarlo deja CR.ME = motor Python (como en v1.2)
CR = V12.CR
ME_PY = V12.ME_PY
MUNDO = V12.MUNDO
SERIE = V12.SERIE
FAM = 'FAMB_RES0_ECO'; FAB = 'FABRICA_ECO'; BAR = 'BAR0_ECO'
FRIO = dict(T=1_000_000, T_lect=V12.V12['T_lect'], gen_largo=V12.V12['gen_largo'], coh_desde=10000, coh_margen=20000)
BRAZOS = {'RES0_FRIO': ('MUT0', FAM, 1), 'RES0_10k': ('MUT0', FAM, 10000), 'RES0_60k': ('MUT0', FAM, 60000),
          'BAR0_FRIO': ('MUT0', BAR, 1), 'FAB_FRIO': ('MUT0', FAB, 1)}
FRIOS = ('RES0_FRIO', 'BAR0_FRIO', 'FAB_FRIO')
VENTANAS = (35001, 35021)                 # serie y replica
PRACTICA = tuple(range(35901, 35910))    # humo 35905; el arnes usa 35901-35904
HUMO = dict(semilla=35905, T=200000)
DATOS = os.path.join(AQUI, 'datos')
_BAR0 = [None]


class BanderaMala(SystemExit):
    pass


def carga_bar0():
    """carros/BAR0_ECO.py por ruta, UNA vez por proceso, registrado en sys.modules (el pickle del checkpoint Python lo necesita)."""
    if _BAR0[0] is None:
        p = os.path.join(AQUI, 'carros', 'BAR0_ECO.py')
        spec = importlib.util.spec_from_file_location('BAR0_ECO', p)
        m = importlib.util.module_from_spec(spec); sys.modules['BAR0_ECO'] = m; spec.loader.exec_module(m)
        _BAR0[0] = m
    return _BAR0[0]


def carros_de(carro):
    """La lista de carros de run_solapadas: la de corre_eco_v12 (cadenas) para FAMB_RES0_ECO y FABRICA_ECO; (etiqueta, modulo) para BAR0."""
    if carro == BAR: return [(BAR, carga_bar0())] * MUNDO['n0']
    return [carro] * MUNDO['n0']


def usa_gemelo():
    """Enchufa motor_frio_rapido en CR.ME, como corre_eco_v12.usa_gemelo hace con motor_eco_rapido_fam."""
    import types
    import motor_frio_rapido as MF
    g = types.ModuleType('motor_frio_gemelo')
    g.__dict__.update({k: v for k, v in ME_PY.__dict__.items() if not k.startswith('__')})
    g.run_solapadas = MF.run_solapadas
    g._MF = MF
    CR.ME = g
    return MF


def nombre_motor():
    if CR.ME is ME_PY: return 'PYTHON motor_eco'
    return 'GEMELO motor_frio_rapido' if hasattr(CR.ME, '_MF') else 'GEMELO otro'


def trabajo(args):
    """UNA corrida (semilla, brazo) hasta T con el t_corte dado. Las claves de corre_eco_v12.trabajo (mismas expresiones) + las de F1.
    Atrapa toda excepcion del motor (nube-9). Checkpoint reanudable. Escribe su JSON."""
    seed, brazo, T, t_corte, T_lect, carpeta, reanuda = args
    gen_brazo, carro, _tc = BRAZOS[brazo]
    fin = os.path.join(carpeta, f"{brazo}_s{seed}.json")
    if reanuda and os.path.exists(fin): return json.load(open(fin, encoding='utf-8'))
    ck = os.path.join(carpeta, 'ckpt', f"{brazo}_s{seed}.pkl"); os.makedirs(os.path.dirname(ck), exist_ok=True)
    filas = []      # las de v1.2: nacidos (y refundados) con tn >= t_corte
    coh = []        # F1: (tn, hijos) de los NACIDOS (fund == 0) con tn >= coh_desde
    c0 = FRIO['coh_desde']

    def cb(li, row, g):
        if row[3] >= t_corte: filas.append([li] + row)
        if row[3] >= c0 and not row[6]: coh.append((row[3], row[5]))

    def guarda(t, blob):
        tmp = ck + '.tmp'
        with open(tmp, 'wb') as f: pickle.dump(dict(t=t, blob=blob, filas=filas, coh=coh), f, protocol=pickle.HIGHEST_PROTOCOL)
        os.replace(tmp, ck)

    estado = None
    if reanuda and os.path.exists(ck):
        d = pickle.load(open(ck, 'rb')); estado = d['blob']; filas[:] = d['filas']; coh[:] = d['coh']
    t0 = time.time()
    base = dict(seed=seed, brazo=brazo, genetica=gen_brazo, carro=carro, T=T, t_corte=t_corte, T_lect=T_lect)
    try:
        r = CR.ME.run_solapadas(seed, carros_de(carro), T=T, diag=0, mundo_n=MUNDO['esc'], tope_cuerpos=MUNDO['tope'],
                                muestra=MUNDO['muestra'],
                                eco=CR.eco_cfg(gen_brazo, t_corte, ckpt_cada=SERIE['ckpt_cada'], ckpt_fn=guarda, estado=estado, ind_cb=cb))
    except KeyboardInterrupt:
        raise
    except BaseException as ex:   # nube-9: NUNCA dejar que un SystemExit mate al trabajador del Pool
        msg = f"{type(ex).__name__}: {ex}"
        g60 = int('ERR-60' in msg)
        hasta = T - FRIO['coh_margen']
        cc = [h for tn, h in coh if tn <= hasta]
        res = dict(base, seg=round(time.time() - t0, 1), aborto=msg, guardia=g60, persiste=(1 if g60 else None), t_ext=None,
                   r0_nac=(round(float(np.mean(cc)), 4) if cc else None), n_coh_nac=len(cc), coh_nac=[c0, hasta],
                   bloqueados=0, n_refund=None, fundadores_rep=None, motor=nombre_motor(), lim_nac=_lim_nac())
        tmp = fin + '.tmp'
        with open(tmp, 'w', encoding='utf-8') as f: json.dump(res, f)
        os.replace(tmp, fin)
        return res
    E = r['eco']; P = r['pista']
    fila_corte = next((f for f in E['gen_t'] if f[0] == t_corte), None)
    fila_lect = next((f for f in E['gen_t'] if f[0] == T_lect), None)
    te = E['t_ext']
    pers_lect = int(te is None or te > T_lect)
    cohv = [f for f in filas if f[4] <= T - 20000]
    vivos_t = [[f[0], f[1]] for f in E['gen_t'] if f[0] >= t_corte and f[0] % FRIO['gen_largo'] == 0]
    # ---- las claves de corre_eco_v12.trabajo, en su orden y con sus expresiones (arnes bloque B)
    res = dict(seed=seed, brazo=brazo, genetica=gen_brazo, carro=carro, T=T, t_corte=t_corte, T_lect=T_lect, seg=round(time.time() - t0, 1),
               t_ext=te, persiste=int(te is None and len(E['vivos_final']) > 0), persiste_lect=pers_lect,
               vivos_lect=(fila_lect[1] if fila_lect is not None else (0 if not pers_lect else None)),
               vivos_T=len(E['vivos_final']), linajes_T=len(set(v[0] for v in E['vivos_final'])),
               gen_max_T=(max(v[2] for v in E['vivos_final']) if E['vivos_final'] else None), vivos_t=vivos_t,
               bloqueados=P['bloqueados'], max_vivos=P['max_vivos'], n_nac=E['n_nac'], n_refund=E['n_refund'], n_banco=E['n_banco'],
               tasa_mut=(E['n_mut'] / max(1, (E['n_nac'] + E['n_banco'])) / len(E['genes'])),
               nac_post=len(filas), r0_post=(round(float(np.mean([f[6] for f in cohv])), 4) if cohv else None), n_coh_post=len(cohv),
               corte=E['corte'], sel_corte=CR.sel_genes(fila_corte),
               gen_t=[f for f in E['gen_t'] if f[0] <= T_lect or f[0] % FRIO['gen_largo'] == 0], tam_total=P['tam_total'],
               genes=E['genes'], G0=E['G0'], vivos_final=E['vivos_final'][:500], juez=None, juez_placebo=None,
               motor=nombre_motor())
    # ---- lo de F1
    hasta = T - FRIO['coh_margen']
    cc = [h for tn, h in coh if tn <= hasta]
    res.update(aborto=None, guardia=0, r0_nac=(round(float(np.mean(cc)), 4) if cc else None), n_coh_nac=len(cc), coh_nac=[c0, hasta],
               fundadores_rep=int(sum(d['fundadores'] for d in r['linajes'])),
               t_fund_primero=min((x for d in r['linajes'] for x in d['t_fund']), default=None),
               vivos_1k=[int(x) for x in P['tam_total'][:11]], lim_nac=_lim_nac())
    tmp = fin + '.tmp'
    with open(tmp, 'w', encoding='utf-8') as f: json.dump(res, f)
    os.replace(tmp, fin)
    if os.path.exists(ck): os.remove(ck)
    return res


def _lim_nac():
    MF = getattr(CR.ME, '_MF', None)
    return int(MF.LIM_NAC) if MF is not None else 100000


# ================================================================================ LA LETRA (PREREGISTRO_frio.md §6)
def veredicto(R, n_esperado=20, T_esperado=None):
    T_esperado = FRIO['T'] if T_esperado is None else T_esperado
    L = []; by = {b: sorted([x for x in R if x['brazo'] == b], key=lambda x: x['seed']) for b in BRAZOS}
    n = {b: len(v) for b, v in by.items()}
    pers = {b: sum(int(x['persiste'] or 0) for x in v) for b, v in by.items()}
    guard = {b: sum(int(x.get('guardia') or 0) for x in v) for b, v in by.items()}
    abortos = [(x['brazo'], x['seed'], x['aborto']) for x in R if x.get('aborto') and not x.get('guardia')]
    tc_mal = [(x['brazo'], x['seed']) for x in R if x.get('t_corte') != BRAZOS[x['brazo']][2]]
    completo = (all(n[b] == n_esperado for b in BRAZOS) and all(x['T'] == T_esperado for x in R) and not abortos and not tc_mal
                and len({(x['brazo'], x['seed']) for x in R}) == len(R))
    bloq = sum(int(x.get('bloqueados') or 0) for x in R)
    sucio = [(x['brazo'], x['seed'], x.get('n_refund'), x.get('fundadores_rep')) for b in FRIOS for x in by[b]
             if not x.get('guardia') and (x.get('n_refund') != 0 or x.get('fundadores_rep') != 0)]
    L.append(f"semillas por brazo: {n}; persiste en T = {T_esperado}: {pers}; guardia ERR-60 disparada (cuenta como persiste): {guard}")
    L.append(f"abortos que no son la guardia: {abortos[:5]}; t_corte distinto del brazo: {tc_mal[:5]}; bloqueados: {bloq}")
    r0 = {b: [(x['r0_nac'] if x.get('r0_nac') is not None else 0.0) for x in v] for b, v in by.items()}
    med = {b: (round(float(np.median(v)), 4) if v else None) for b, v in r0.items()}
    L.append(f"R0 de NACIDOS (fund = 0) en [{FRIO['coh_desde']}, T - {FRIO['coh_margen']}], mediana sobre las semillas (cohorte vacia = 0): {med}")
    L.append(f"descriptivo: cuerpos vivos en T en los que persisten (mediana) "
             f"{ {b: (float(np.median([x['vivos_T'] for x in v if x['persiste'] and x.get('vivos_T') is not None])) if any(x['persiste'] and x.get('vivos_T') is not None for x in v) else None) for b, v in by.items()} }; "
             f"t_ext (mediana de los que se extinguen) { {b: (float(np.median([x['t_ext'] for x in v if x.get('t_ext')])) if any(x.get('t_ext') for x in v) else None) for b, v in by.items()} }")
    L.append(f"descriptivo, DOSIS de vivero (RES0): t_corte 1 -> {pers['RES0_FRIO']}/{n['RES0_FRIO']} · 10 000 -> {pers['RES0_10k']}/{n['RES0_10k']} · "
             f"60 000 -> {pers['RES0_60k']}/{n['RES0_60k']}")
    V1 = pers['RES0_60k'] >= 17
    V2 = not sucio
    P1 = pers['RES0_FRIO'] >= 15
    P2 = med['RES0_FRIO'] is not None and med['RES0_FRIO'] >= 0.90
    P3 = pers['FAB_FRIO'] <= 2
    P4 = pers['BAR0_FRIO'] <= 5
    dB = pers['RES0_FRIO'] - pers['BAR0_FRIO']; dF = pers['RES0_FRIO'] - pers['FAB_FRIO']
    M = pers['RES0_FRIO'] >= 8 and dB >= 6 and dF >= 6
    L.append(f"V1 ancla RES0_60k >= 17/20: {'SE CUMPLE' if V1 else 'NO'} ({pers['RES0_60k']}) · V2 frio limpio (0 refundados, 0 fundadores "
             f"repuestos en los {len(FRIOS)} brazos FRIO): {'SE CUMPLE' if V2 else 'NO'} {sucio[:5]}")
    L.append(f"P1 RES0_FRIO >= 15/20: {'SE CUMPLE' if P1 else 'NO'} ({pers['RES0_FRIO']}) · P2 mediana R0 nacidos >= 0.90: "
             f"{'SE CUMPLE' if P2 else 'NO'} ({med['RES0_FRIO']}) · P3 FAB_FRIO <= 2/20: {'SE CUMPLE' if P3 else 'NO'} ({pers['FAB_FRIO']}) · "
             f"P4 BAR0_FRIO <= 5/20: {'SE CUMPLE' if P4 else 'NO'} ({pers['BAR0_FRIO']}) · M (MODESTO): RES0_FRIO >= 8, "
             f"RES0 - BAR0 >= 6 ({dB}), RES0 - FAB >= 6 ({dF}): {'SE CUMPLE' if M else 'NO'}")
    if not completo: v = 'NO EVALUABLE (serie incompleta, abortos, T o t_corte distintos)'
    elif bloq > 0: v = f'NO EVALUABLE (tope de cuerpos alcanzado: bloqueados = {bloq})'
    elif not V2: v = 'NO EVALUABLE (un brazo FRIO tuvo fundadores repuestos: el frio no es frio)'
    elif not V1: v = 'NO EVALUABLE (el ancla RES0_60k no reproduce MUT0_T: < 17/20)'
    elif P1 and P2 and P3 and P4: v = 'FUNCIONA: EL LINAJE ARRANCA EN FRIO CON LA TABLA DE LA FAMILIA (en esta serie)'
    elif M: v = 'HAY ALGO MODESTO: ARRANCA EN FRIO A MEDIAS (en esta serie; ver que puertas caen)'
    else: v = 'NO (en esta serie)'
    L.append(f"VEREDICTO F1 POR LA LETRA (una serie; el del bloque exige serie + replica con el mismo veredicto): {v}")
    return v, L, dict(V1=V1, V2=V2, P1=P1, P2=P2, P3=P3, P4=P4, M=M, pers=pers, guardia=guard, med_r0=med, dB=dB, dF=dF,
                      abortos=abortos, sucio=sucio, completo=completo, bloq=bloq)


def lee(carpeta, n_esperado=20):
    R = [json.load(open(p, encoding='utf-8')) for p in sorted(glob.glob(os.path.join(carpeta, '*_s*.json')))]
    v, L, d = veredicto(R, n_esperado)
    for l in L: print(l, flush=True)
    return v, L, d, R


def SHAS():
    f = lambda p: hashlib.sha256(open(p, 'rb').read()).hexdigest()[:16]
    ps = {'corre_frio.py': os.path.join(AQUI, 'corre_frio.py'), 'construye_frio.py': os.path.join(AQUI, 'construye_frio.py'),
          'motor_frio_rapido.py': os.path.join(AQUI, 'motor_frio_rapido.py'), 'carros/BAR0_ECO.py': os.path.join(AQUI, 'carros', 'BAR0_ECO.py'),
          'PREREGISTRO_frio.md': os.path.join(AQUI, 'PREREGISTRO_frio.md'),
          'juaco_eco/corre_eco_v12.py': os.path.join(ECO, 'corre_eco_v12.py'), 'juaco_eco/corre_eco.py': os.path.join(ECO, 'corre_eco.py'),
          'juaco_eco/motor_eco.py': os.path.join(ECO, 'motor_eco.py'), 'juaco_eco/motor_eco_rapido_fam.py': os.path.join(ECO, 'motor_eco_rapido_fam.py'),
          'juaco_eco/carros/FAMB_RES0_ECO.py': os.path.join(ECO, 'carros', 'FAMB_RES0_ECO.py'),
          'juaco_eco/carros/FABRICA_ECO.py': os.path.join(ECO, 'carros', 'FABRICA_ECO.py')}
    return {k: f(p) for k, p in ps.items() if os.path.exists(p)}


def parsea(argv):
    ap = argparse.ArgumentParser(allow_abbrev=False, add_help=False)
    ap.add_argument('--humo', action='store_true'); ap.add_argument('--serie', action='store_true')
    ap.add_argument('--lee', default=None)
    ap.add_argument('--desde', type=int); ap.add_argument('--n', type=int); ap.add_argument('--pool', type=int)
    ap.add_argument('--reanuda', action='store_true')
    try:
        a, resto = ap.parse_known_args(argv)
    except SystemExit:
        raise BanderaMala('F1 FRIO: banderas mal formadas')
    if resto: raise BanderaMala(f"F1 FRIO: banderas desconocidas {resto}")
    if any(x.startswith('--') and '=' in x for x in argv): raise BanderaMala('F1 FRIO: sin la forma --bandera=valor')
    if len(argv) != len(set(x for x in argv if x.startswith('--'))) + sum(1 for x in argv if not x.startswith('--')):
        raise BanderaMala('F1 FRIO: bandera repetida')
    modos = int(a.humo) + int(a.serie) + int(a.lee is not None)
    if modos != 1: raise BanderaMala('F1 FRIO: exactamente uno de --humo, --serie, --lee')
    if a.humo and (a.desde is not None or a.n is not None or a.pool is not None or a.reanuda): raise BanderaMala('F1 FRIO: --humo va solo')
    if a.lee is not None and (a.desde is not None or a.n is not None or a.pool is not None or a.reanuda):
        raise BanderaMala('F1 FRIO: --lee va solo')
    if a.serie and (a.desde not in VENTANAS or a.n != 20 or a.pool is None or not 1 <= a.pool <= 6):
        raise BanderaMala(f"F1 FRIO: --serie --desde {VENTANAS[0]} (serie) o {VENTANAS[1]} (replica) --n 20 --pool 1..6")
    return a


def humo():
    """UN proceso, sin Pool: semilla de practica 35905, los 5 brazos, T 200 000 (regla 3: <= 6 corridas, <= 200 000 pasos). Escribe su JSON."""
    usa_gemelo()
    os.makedirs(os.path.join(DATOS, 'humo'), exist_ok=True)
    ts = time.strftime('%Y%m%d_%H%M%S'); etq = f"frio_humo_s{HUMO['semilla']}_T{HUMO['T']}_{ts}"
    carpeta = os.path.join(DATOS, 'humo', etq); os.makedirs(carpeta, exist_ok=True); t0 = time.time()
    print(f"[{time.strftime('%H:%M:%S')}] HUMO F1 FRIO (gemelo motor_frio_rapido, 1 proceso) · shas {SHAS()}", flush=True)
    R = []
    for b, (gen, carro, tc) in BRAZOS.items():
        r = trabajo((HUMO['semilla'], b, HUMO['T'], tc, FRIO['T_lect'], carpeta, False))
        R.append(r)
        print(f"[{time.strftime('%H:%M:%S')}] {b} s{r['seed']} (t_corte {tc}): {r['seg']} s · persiste {r['persiste']} (vivos {r.get('vivos_T')}) · "
              f"t_ext {r.get('t_ext')} · max_vivos {r.get('max_vivos')} · n_nac {r.get('n_nac')} · refundados {r.get('n_refund')} · "
              f"fundadores_rep {r.get('fundadores_rep')} · r0_nac {r.get('r0_nac')} (n {r.get('n_coh_nac')}) · vivos cada 1000 {r.get('vivos_1k')} · "
              f"aborto {r.get('aborto')}", flush=True)
    v, L, d = veredicto(R, n_esperado=20, T_esperado=HUMO['T'])
    for l in L: print('  ' + l, flush=True)
    ruta = os.path.join(DATOS, 'humo', etq + '.json')
    json.dump(dict(humo=HUMO, FRIO=FRIO, BRAZOS=BRAZOS, R=R, veredicto_de_prueba=v, lineas=L, seg=round(time.time() - t0, 1),
                   seg_por_brazo={x['brazo']: x['seg'] for x in R}, shas=SHAS()), open(ruta, 'w', encoding='utf-8'), default=str)
    print(f"  JSON: {os.path.relpath(ruta, RAIZ)}  ({round(time.time() - t0, 1)} s)")
    print(f"VEREDICTO (humo, una semilla, T corto: no decide): {v}")
    return ruta


def main(argv=None):
    a = parsea(sys.argv[1:] if argv is None else argv)
    if a.humo: return humo()
    if a.lee is not None:
        lee(a.lee); return
    usa_gemelo()
    T, tl = FRIO['T'], FRIO['T_lect']
    etq = f"frio_serie_s{a.desde}-{a.desde + a.n - 1}"
    carpeta = os.path.join(DATOS, etq)
    if os.path.exists(carpeta) and not a.reanuda and glob.glob(os.path.join(carpeta, '*_s*.json')):
        raise SystemExit(f"F1 FRIO: {carpeta} ya tiene resultados; --reanuda (no se pisa nada)")
    os.makedirs(carpeta, exist_ok=True)
    flog = open(os.path.join(carpeta, 'progreso.log'), 'a', encoding='utf-8')

    def log(s):
        s = f"[{time.strftime('%H:%M:%S')}] {s}"; print(s, flush=True); flog.write(s + '\n'); flog.flush()
    log(f"F1 FRIO {etq} · T {T} · brazos {BRAZOS} · pool {a.pool} · motor GEMELO motor_frio_rapido · shas {SHAS()}")
    # los brazos caros (vivero y RES0) primero: el Pool termina antes
    orden = ('RES0_60k', 'RES0_10k', 'RES0_FRIO', 'BAR0_FRIO', 'FAB_FRIO')
    jobs = [(s, b, T, BRAZOS[b][2], tl, carpeta, a.reanuda) for b in orden for s in range(a.desde, a.desde + a.n)]
    t0 = time.time()
    from multiprocessing import Pool
    with Pool(a.pool, initializer=usa_gemelo) as pool:
        for k, r in enumerate(pool.imap_unordered(trabajo, jobs), 1):
            log(f"[{k}/{len(jobs)}] {r['brazo']} s{r['seed']}: persiste {r['persiste']} (vivos {r.get('vivos_T')}) · t_ext {r.get('t_ext')} · "
                f"refundados {r.get('n_refund')} · r0_nac {r.get('r0_nac')} · max_vivos {r.get('max_vivos')} · aborto {r.get('aborto')} "
                f"({r['seg']} s; {round(time.time() - t0)} s)")
    v, L, d, R = lee(carpeta, a.n)
    for l in L: flog.write(l + '\n')
    json.dump(dict(etiqueta=etq, veredicto=v, lineas=L, d=d, seg=round(time.time() - t0), MUNDO=MUNDO, SERIE=SERIE, FRIO=FRIO,
                   BRAZOS=BRAZOS, shas=SHAS()), open(os.path.join(carpeta, 'RESUMEN.json'), 'w', encoding='utf-8'), indent=1, default=str)
    log(f"VEREDICTO: {v}")
    flog.close()


if __name__ == '__main__':
    try:
        main()
    except BanderaMala as e:
        print(str(e), file=sys.stderr); sys.exit(2)
