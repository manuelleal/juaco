"""corre_n10b.py — SUBIDA DEL NIVEL 10, TANDA 2: "la familia pasa su TABLA en vida" (PREREGISTRO_n10b.md).

MISION: llegar a la AGI por este camino.

Mundo: pista v2 de generaciones que conviven (experimentos/generaciones/pista2.py, solapadas=1, quimiostato 'fija', r_rep 0.03,
tope 300), SIN CAMBIOS (el mismo de la tanda 1: la serie 12301-12320 calibra las anclas). Organismo: FABRICA en cinco variantes
construidas por anclas (construye_familia_b.py; arnes identidad_familia_b.py):
  NADA (== FABRICA) · RES (candidato: tabla de la familia) · RES1 (tabla solo de lo vivido por el padre) · BAR (tabla de RES con
  las R permutadas) · ORACULO (== FAMILIA_ORACULO de la tanda 1, techo).
Brazos: monocultivos de 9 fundadores de cada variante + MIX (3 NADA + 3 RES + 3 BAR en el MISMO mundo).
Medidas SOLO desde la fisica (ERR-96): resumen_linaje del juez v2 (corre_convive.py, sha fijado; se IMPORTA) + R0 de los NACIDOS
(no fundadores, cohorte t <= T/2), vida de nacidos, causas. Telemetria del carro (_TELE: claves de la tabla instalada) solo informa.

ERR-115: el parser es una LISTA BLANCA; aborta ante cualquier bandera desconocida, abreviada, con '=', repetida o '--help'.
Uso:
  humo (un proceso, sin Pool):  python experimentos/subida_n10b/corre_n10b.py --humo              (semilla 12791, T=20000, 6 brazos)
  identidad:                    python experimentos/subida_n10b/identidad_familia_b.py
  serie (SOLO el coordinador):  python experimentos/subida_n10b/corre_n10b.py --serie --desde 12701 --n 20 --pool 6
  replica (SOLO coordinador):   python experimentos/subida_n10b/corre_n10b.py --serie --desde 12721 --n 20 --pool 6
"""
import gzip, hashlib, importlib.util, json, math, os, platform, statistics as st, sys, time

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
GEN = os.path.join(RAIZ, 'experimentos', 'generaciones')
SIN_VALOR = {'--humo', '--serie'}
CON_VALOR = {'--brazo': str, '--desde': int, '--n': int, '--T': int, '--pool': int}


class BanderaMala(SystemExit):
    pass


def parsea(argv):
    """Lista blanca (ERR-115). Devuelve dict; aborta con BanderaMala ante cualquier cosa fuera de la lista."""
    a = dict(humo=False, serie=False, brazo=None, desde=None, n=20, T=None, pool=0); vistos = set(); i = 0
    while i < len(argv):
        tk = argv[i]
        if tk in vistos: raise BanderaMala(f"corre_n10b: bandera repetida {tk!r} -> ABORTA (ERR-115)")
        if tk in SIN_VALOR:
            vistos.add(tk); a[tk[2:]] = True; i += 1; continue
        if tk in CON_VALOR:
            vistos.add(tk)
            if i + 1 >= len(argv) or argv[i + 1].startswith('--'): raise BanderaMala(f"corre_n10b: {tk} sin valor -> ABORTA (ERR-115)")
            try: a[tk[2:]] = CON_VALOR[tk](argv[i + 1])
            except ValueError: raise BanderaMala(f"corre_n10b: valor invalido para {tk}: {argv[i + 1]!r} -> ABORTA (ERR-115)")
            i += 2; continue
        raise BanderaMala(f"corre_n10b: bandera desconocida {tk!r} (validas: {sorted(SIN_VALOR | set(CON_VALOR))}) -> ABORTA (ERR-115)")
    if a['humo'] == a['serie']: raise BanderaMala("corre_n10b: --humo o --serie (exactamente uno) -> ABORTA")
    if a['humo'] and a['pool']: raise BanderaMala("corre_n10b: el humo es de UN proceso (sin --pool) -> ABORTA")
    if a['serie'] and a['desde'] is None: raise BanderaMala("corre_n10b: --serie exige --desde -> ABORTA")
    if a['serie'] and (a['T'] is not None or a['brazo'] is not None):
        raise BanderaMala("corre_n10b: la serie corre T = 100000 y los 6 brazos preregistrados (sin --T ni --brazo) -> ABORTA")
    if a['pool'] and not 1 <= a['pool'] <= 6: raise BanderaMala("corre_n10b: --pool entre 1 y 6 -> ABORTA")
    return a


MONO = ('NADA', 'RES', 'RES1', 'BAR', 'ORACULO')
BRAZOS = MONO + ('MIX',)
MIX = ['NADA'] * 3 + ['RES'] * 3 + ['BAR'] * 3
SEMILLAS = dict(practica=(12791, 12799), serie=(12701, 12720), replica=(12721, 12740))
T_DEF = 100000
DATOS = os.path.join(AQUI, 'datos')
PARES = (('RES', 'NADA'), ('RES', 'BAR'), ('RES', 'RES1'), ('BAR', 'NADA'), ('RES1', 'NADA'), ('ORACULO', 'RES'), ('ORACULO', 'NADA'))
PARES_MIX = (('RES', 'NADA'), ('RES', 'BAR'), ('BAR', 'NADA'))
# ANCLAS CALIBRADAS sobre la serie 12301-12320 de la tanda 1 (ERR-116; FAMB_NADA == FAMILIA_NADA == FABRICA y FAMB_ORACULO ==
# FAMILIA_ORACULO bit a bit por el arnes): intervalo de prediccion al 99 % de la MEDIANA de 20 semillas nuevas (bootstrap de dos
# muestras sobre los 20 valores por semilla, redondeado hacia afuera). Ver PREREGISTRO_n10b.md sec. 3.
ANCLA_NADA = (0.085, 0.135)
ANCLA_ORACULO = (0.49, 0.62)


def valida_semillas(desde, n):
    ok = any(lo <= desde and desde + n - 1 <= hi for k, (lo, hi) in SEMILLAS.items() if k != 'practica')
    if not ok: raise BanderaMala(f"corre_n10b: semillas {desde}..{desde + n - 1} fuera de las preregistradas {SEMILLAS} -> ABORTA")
    return True


def h16(p): return hashlib.sha256(open(p, 'rb').read()).hexdigest()[:16]


SHAS = {os.path.join(GEN, 'pista2.py'): '4d2bee16e7961261', os.path.join(GEN, 'motor_convive.py'): 'd10cb9021f5d0f41',
        os.path.join(GEN, 'corre_convive.py'): 'e6dadfdad9c379cd',
        os.path.join(RAIZ, 'experimentos', 'carrera_escuderias', 'carros', 'FABRICA.py'): '2ebee3e99ea5a33a',
        os.path.join(AQUI, 'carros', 'FAMB_NADA.py'): '6635a04063fe7317',
        os.path.join(AQUI, 'carros', 'FAMB_RES.py'): '2addb7ca5b9d031d',
        os.path.join(AQUI, 'carros', 'FAMB_RES1.py'): '766807733fb620e2',
        os.path.join(AQUI, 'carros', 'FAMB_BAR.py'): 'dfcb2efbf5ec8d2b',
        os.path.join(AQUI, 'carros', 'FAMB_ORACULO.py'): 'c1ee88844650a78e'}


def verifica_shas():
    mal = {os.path.basename(p): (h16(p), s) for p, s in SHAS.items() if h16(p) != s}
    if mal: raise SystemExit(f"corre_n10b: sha cambiado {mal} (reconstruir y volver a correr identidad_familia_b.py)")


def _importa_mundo():
    if GEN not in sys.path: sys.path.insert(0, GEN)
    import pista2 as P2, motor_convive as MC, corre_convive as JV
    return P2, MC, JV


def carga(et):
    p = os.path.join(AQUI, 'carros', f'FAMB_{et}.py')
    spec = importlib.util.spec_from_file_location(f'carro_FAMB_{et}', p)
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m


def med(xs):
    xs = [x for x in xs if x is not None]
    return round(float(st.median(xs)), 4) if xs else None


def media(xs):
    xs = [x for x in xs if x is not None]
    return round(sum(xs) / len(xs), 4) if xs else None


def tele(m):
    """Telemetria del carro (NO decide): tablas instaladas en los hijos."""
    T_ = getattr(m, '_TELE', [])
    if not T_: return None
    return dict(n=len(T_), claves_med=med([x[1] for x in T_]),
                frac_B_mala=round(sum(1 for x in T_ if x[2] is not None and x[2] < 0) / len(T_), 4),
                frac_D_mala=round(sum(1 for x in T_ if x[3] is not None and x[3] < 0) / len(T_), 4),
                frac_A_mala=round(sum(1 for x in T_ if x[4] is not None and x[4] < 0) / len(T_), 4),
                frac_C_mala=round(sum(1 for x in T_ if x[5] is not None and x[5] < 0) / len(T_), 4),
                frac_completa=round(sum(1 for x in T_ if x[1] == 8) / len(T_), 4))


def tarea(args):
    seed, brazo, T = args
    P2, MC, JV = _importa_mundo()
    t0 = time.time()
    mods = {et: carga(et) for et in MONO}
    al = [(f'FAMB_{e}', mods[e]) for e in MIX] if brazo == 'MIX' else [(f'FAMB_{brazo}', mods[brazo])] * 9
    r = P2.run(seed, al, T=T, diag=0, solapadas=1, reposicion='fija', tope_cuerpos=MC.TOPE_DEF, r_rep=MC.R_REP)
    ps = r['pista']; mu = ps['muestra']; i2 = (T // 2) // mu; tc = T // 2
    L = [JV.resumen_linaje(d, T, mu) for d in r['linajes']]
    estr = {}
    for e in sorted(set(l['etiqueta'] for l in L)):
        ix = [j for j, l in enumerate(L) if l['etiqueta'] == e]
        serie = [sum(r['linajes'][j]['tam'][m] for j in ix) for m in range(len(r['linajes'][0]['tam']))]
        ind = [x for j in ix for x in r['linajes'][j]['individuos']]   # [k, gen, padre, t_nace, t_muere, hijos, fundador, causa, vol]
        nac = [x for x in ind if not x[6]]; fun = [x for x in ind if x[6]]
        coh = [x for x in nac if x[3] <= tc]
        mn = [x for x in nac if x[4] >= 0]; mf = [x for x in fun if x[4] >= 0]
        cau = {c: sum(1 for x in mn if x[7] == ic) for ic, c in enumerate(MC.CAUSAS)}   # la pista guarda la causa como INDICE
        et = e.replace('FAMB_', '')
        estr[et] = dict(
            tam_carro=media(serie[i2:-1] if len(serie) > i2 + 1 else serie), tam_final=serie[-1],
            exceso=(round(media(serie[i2:-1] if len(serie) > i2 + 1 else serie) - len(ix), 4)),
            nac=sum(L[j]['nac'] for j in ix), fundadores=sum(L[j]['fundadores'] for j in ix),
            linajes_sin_ext=sum(L[j]['sin_extincion'] for j in ix), persisten=sum(L[j]['persiste'] for j in ix), n_lin=len(ix),
            persiste_carro=any(L[j]['sin_extincion'] for j in ix),
            R0_nacidos=media([x[5] for x in coh]), n_coh_nacidos=len(coh),
            cens_nacidos=(round(sum(1 for x in coh if x[4] < 0) / len(coh), 4) if coh else None),
            R0_fund=media([x[5] for x in fun if x[3] <= tc]),
            vida_nacidos=med([x[4] - x[3] for x in mn]), vida_fund=med([x[4] - x[3] for x in mf]),
            frac_mala_nacidos=(round((cau['veneno'] + cau['sal']) / len(mn), 4) if mn else None), causas_nacidos=cau,
            gen_max=max((L[j]['gen_max'] for j in ix), default=0), bloqueados=sum(L[j]['bloqueados'] for j in ix),
            tele=(tele(mods[et]) if et in ('RES', 'RES1', 'BAR') else None))
    crudo = [dict(individuos=d['individuos'], tam=d['tam'], t_fund=d['t_fund'], carro_n10=d.get('carro', {}).get('n10')) for d in r['linajes']]
    return dict(seed=seed, brazo=brazo, T=T, seg=round(time.time() - t0, 1), estr=estr, linajes=L, crudo=crudo,
                pista={k: v for k, v in ps.items() if k not in ('pizarra_final',)})


def signo(g, p):
    n = g + p
    if n == 0: return 1.0
    k = min(g, p)
    return round(min(1.0, 2 * sum(math.comb(n, i) for i in range(k + 1)) / 2 ** n), 5)


def pareado(R, a, b, clave, mix=False):
    xs = []
    for s in sorted({c['seed'] for c in R}):
        if mix:
            c = [c for c in R if c['seed'] == s and c['brazo'] == 'MIX']
            if not c: continue
            va, vb = c[0]['estr'][a][clave], c[0]['estr'][b][clave]
        else:
            ca = [c for c in R if c['seed'] == s and c['brazo'] == a]; cb = [c for c in R if c['seed'] == s and c['brazo'] == b]
            if not ca or not cb: continue
            va, vb = ca[0]['estr'][a][clave], cb[0]['estr'][b][clave]
        if va is None or vb is None: continue
        xs.append(va - vb)
    g = sum(1 for d in xs if d > 0); p = sum(1 for d in xs if d < 0); e = len(xs) - g - p
    return dict(par=f"{a}-{b}", clave=clave, n=len(xs), gana=g, pierde=p, empata=e, dif_med=med(xs), p_signo=signo(g, p))


def agrega(R):
    A = {}
    for b in MONO:
        cs = [c['estr'][b] for c in R if c['brazo'] == b]
        if not cs: continue
        A[b] = {k: med([c[k] for c in cs]) for k in ('tam_carro', 'exceso', 'nac', 'fundadores', 'linajes_sin_ext', 'persisten', 'R0_nacidos',
                                                    'R0_fund', 'vida_nacidos', 'vida_fund', 'frac_mala_nacidos', 'gen_max')}
        A[b]['semillas'] = len(cs); A[b]['persiste_carro'] = sum(c['persiste_carro'] for c in cs)
        A[b]['bloqueados'] = sum(c['bloqueados'] for c in cs)
        A[b]['sem_R0nac_ge_090'] = sum(1 for c in cs if c['R0_nacidos'] is not None and c['R0_nacidos'] >= 0.90)
        tl = [c['tele'] for c in cs if c.get('tele')]
        if tl: A[b]['tele'] = {k: med([x[k] for x in tl]) for k in tl[0]}
    # fraccion de la brecha NADA -> ORACULO que cierra RES, por semilla (informativa, P5)
    fr = []
    for s in sorted({c['seed'] for c in R}):
        v = {c['brazo']: c['estr'][c['brazo']]['R0_nacidos'] for c in R if c['seed'] == s and c['brazo'] in ('NADA', 'RES', 'ORACULO')}
        if len(v) == 3 and None not in v.values() and v['ORACULO'] - v['NADA'] > 1e-9: fr.append((v['RES'] - v['NADA']) / (v['ORACULO'] - v['NADA']))
    A['_brecha_RES'] = dict(mediana=med(fr), n=len(fr))
    P = [pareado(R, a, b, k) for a, b in PARES for k in ('R0_nacidos', 'vida_nacidos', 'exceso', 'nac', 'gen_max')]
    PM = [pareado(R, a, b, k, mix=True) for a, b in PARES_MIX for k in ('R0_nacidos', 'exceso', 'nac')]
    return A, P, PM


def veredicto(A, P, PM, n_sem):
    """PREREGISTRO_n10b.md sec. 6 (por la letra). Umbral pareado >= 15/20 (fraccion 0.75 si n != 20)."""
    need = math.ceil(0.75 * n_sem)
    g = lambda lst, par, k: next((x for x in lst if x['par'] == par and x['clave'] == k), None)
    K = 'R0_nacidos'; out = {}
    rn, rb, r1, on = g(P, 'RES-NADA', K), g(P, 'RES-BAR', K), g(P, 'RES-RES1', K), g(P, 'ORACULO-NADA', K)
    mrn, mrb = g(PM, 'RES-NADA', K), g(PM, 'RES-BAR', K)
    nada = A.get('NADA') or {}; ora = A.get('ORACULO') or {}
    k_anc = f'V-ANCLA-b (mediana R0_nacidos NADA en [{ANCLA_NADA[0]}, {ANCLA_NADA[1]}] y NADA persiste_carro <= 5/20)'
    k_tec = f'V-TECHO-b (mediana R0_nacidos ORACULO en [{ANCLA_ORACULO[0]}, {ANCLA_ORACULO[1]}] y ORACULO > NADA >= 15/20)'
    k1, k2 = 'F-1 (RES > NADA en R0_nacidos >= 15/20)', 'F-2 (RES > BAR en R0_nacidos >= 15/20)'
    k3, k4 = 'F-3 (MIX: RES > NADA, mismo mundo, >= 15/20)', 'F-4 (MIX: RES > BAR, mismo mundo, >= 15/20)'
    k5 = 'F-5 ACUMULA (RES > RES1 en R0_nacidos >= 15/20)'
    out[k_anc] = bool(nada.get(K) is not None and ANCLA_NADA[0] <= nada[K] <= ANCLA_NADA[1] and nada.get('persiste_carro', 99) <= n_sem - need)
    out[k_tec] = bool(ora.get(K) is not None and ANCLA_ORACULO[0] <= ora[K] <= ANCLA_ORACULO[1] and on and on['gana'] >= need)
    out[k1] = bool(rn and rn['gana'] >= need); out[k2] = bool(rb and rb['gana'] >= need)
    out[k3] = bool(mrn and mrn['gana'] >= need); out[k4] = bool(mrb and mrb['gana'] >= need)
    out[k5] = bool(r1 and r1['gana'] >= need)
    out['C-BAR (informativo: el control GANA o empata: BAR >= RES en >= 10/20)'] = bool(rb and (rb['pierde'] + rb['empata']) >= math.ceil(0.5 * n_sem))
    out['L-PERSISTE (informativo: semillas donde persiste el carro RES)'] = (A.get('RES') or {}).get('persiste_carro')
    out['BRECHA (informativo: mediana de (RES-NADA)/(ORACULO-NADA))'] = (A.get('_brecha_RES') or {}).get('mediana')
    if not out[k_anc]: v = 'NO SE LEE (ancla calibrada fuera: el instrumento no reproduce el piso de la tanda 1)'
    elif not out[k_tec]: v = 'NO SE LEE COMO CAPACIDAD (el techo no reproduce la tanda 1 o no le gana al piso)'
    elif out[k1] and out[k2] and out[k3] and out[k4]:
        v = 'FUNCIONA' + (' + ACUMULA' if out[k5] else '') + (' (la tabla que la familia pasa en vida sube el R0 de los nacidos por su CONTENIDO, en monocultivo y compitiendo en el mismo mundo'
                                                              + ('; la tabla de la familia gana a la del padre solo)' if out[k5] else ')'))
    elif out[k1] and out[k2]:
        v = 'HAY ALGO MODESTO' + (' + ACUMULA' if out[k5] else '') + ' (por contenido en monocultivo; no gana la competencia directa en el mismo mundo)'
    elif out[k1]: v = 'HAY ALGO MODESTO SIN CONTENIDO (pasar la tabla ayuda, pero la tabla barajada no pierde por la letra)'
    else: v = 'NO (pasar la tabla en el parto no sube el R0 de los nacidos)'
    out['VEREDICTO'] = v
    return out


def main(argv):
    a = parsea(argv)   # ANTES de importar nada pesado o tocar disco (ERR-115)
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    verifica_shas()
    if a['brazo'] is not None and a['brazo'] not in BRAZOS: raise BanderaMala(f"corre_n10b: --brazo {a['brazo']!r} no existe {BRAZOS} -> ABORTA")
    brazos = [a['brazo']] if a['brazo'] else list(BRAZOS)
    if a['humo']:
        desde = a['desde'] or SEMILLAS['practica'][0]; n = 1 if a['desde'] is None else a['n']; T = a['T'] or 20000
        if not (SEMILLAS['practica'][0] <= desde and desde + n - 1 <= SEMILLAS['practica'][1]):
            raise BanderaMala(f"corre_n10b: el humo solo corre semillas de practica {SEMILLAS['practica']} -> ABORTA")
        if n * len(brazos) > 6 or T * n > 200000: raise BanderaMala("corre_n10b: humo de a lo sumo 6 corridas y 200000 pasos por brazo -> ABORTA")
        sal = os.path.join(DATOS, 'humo'); et = f"n10b_humo_{'_'.join(brazos) if len(brazos) < len(BRAZOS) else 'todos'}_s{desde}_T{T}"
    else:
        desde = a['desde']; n = a['n']; T = T_DEF
        valida_semillas(desde, n)
        sal = DATOS; et = f"n10b_serie_s{desde}-{desde + n - 1}_T{T}"
    os.makedirs(sal, exist_ok=True)
    sello = time.strftime('%Y%m%d_%H%M%S'); base = os.path.join(sal, f"{et}_{sello}")
    flog = open(base + '.log', 'w', encoding='utf-8')

    def log(s=''):
        print(s, flush=True); flog.write(s + '\n'); flog.flush()
    pre = os.path.join(AQUI, 'PREREGISTRO_n10b.md')
    log(f"corre_n10b · {et} · {sello} · python {platform.python_version()} · corre_n10b.py {h16(os.path.abspath(__file__))} · "
        f"PREREGISTRO_n10b.md {h16(pre) if os.path.exists(pre) else 'NO EXISTE'}")
    log("shas: " + ' '.join(f"{os.path.basename(p)}={s}" for p, s in SHAS.items()))
    semillas = list(range(desde, desde + n)); tareas = [(s, b, T) for b in brazos for s in semillas]
    t0 = time.time(); R = []

    def linea(r):
        return f"  {r['brazo']:8s} s{r['seed']} {r['seg']:7.1f} s · " + ' · '.join(
            f"{e}: R0nac {v['R0_nacidos']} vida nac {v['vida_nacidos']} nac {v['nac']} tam {v['tam_carro']} gen {v['gen_max']}"
            + (f" tele {v['tele']}" if v.get('tele') else '') for e, v in r['estr'].items())
    if a['pool'] and a['pool'] > 1:
        from multiprocessing import Pool
        with Pool(a['pool']) as pool:
            for r in pool.imap_unordered(tarea, tareas): R.append(r); log(linea(r))
    else:
        for tk in tareas: r = tarea(tk); R.append(r); log(linea(r))
    A, P, PM = agrega(R)
    log(f"\nAGREGADO (medianas por semilla) · {len(semillas)} semillas · {time.time() - t0:.0f} s de pared")
    for b, v in A.items(): log(f"  {b:8s} {v}")
    log("PAREADOS (monocultivo, por semilla):")
    for x in P: log(f"  {x}")
    log("PAREADOS (MIX, dentro del mismo mundo):")
    for x in PM: log(f"  {x}")
    V = veredicto(A, P, PM, len(semillas)) if a['serie'] else {'VEREDICTO': 'HUMO: no hay veredicto (una semilla de practica)'}
    log("VEREDICTO por la letra (PREREGISTRO_n10b.md sec. 6):")
    for k, v in V.items(): log(f"  {k}: {v}")
    meta = dict(etiqueta=et, sello=sello, semillas=semillas, T=T, brazos=brazos, shas={os.path.basename(p): s for p, s in SHAS.items()},
                corre_n10b=h16(os.path.abspath(__file__)), preregistro=(h16(pre) if os.path.exists(pre) else None),
                seg_pared=round(time.time() - t0, 1), seg_cpu=round(sum(r['seg'] for r in R), 1))
    res = dict(meta=meta, agregado=A, pareados=P, pareados_mix=PM, veredicto=V,
               por_semilla=[{k: r[k] for k in ('seed', 'brazo', 'T', 'seg', 'estr')} for r in R])
    json.dump(res, open(base + '.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    with gzip.open(base + '_crudo.json.gz', 'wt', encoding='utf-8') as f: json.dump(R, f)
    log(f"\nescrito: {base}.json ({h16(base + '.json')}) · crudo {base}_crudo.json.gz")
    flog.close()


if __name__ == '__main__':
    main(sys.argv[1:])
