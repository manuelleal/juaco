"""corre_convive.py — JUEZ v2 de la pista con GENERACIONES SOLAPADAS (PREREGISTRO_convive.md).

MISION: llegar a la AGI por este camino.

Corre monocultivos (9 fundadores del mismo carro, 9 linajes) en pista2.run(..., solapadas=1, diag=0) y mide SOLO desde la
fisica (ERR-96; d['carro'] no se usa para puntuar, salvo la muerte programada DECLARADA, que se reporta y no puntua):
  R0 VERDADERO por individuo: hijos nacidos en su vida. COHORTE = individuos nacidos en t <= T/2 (fundadores incluidos).
    R0_coh = media de hijos de la cohorte; los que siguen vivos en T cuentan con los hijos que llevan (CENSURA -> cota
    inferior; se reporta la fraccion censurada). R0_compl = solo los de la cohorte muertos antes de T (vida completa).
    R0_muertos = todos los muertos (sesgado hacia vidas cortas; solo lectura).
  PERSISTENCIA (letra de la ENMIENDA 6): un linaje-semilla persiste si tiene 0 fundadores despues de t = 10000 (no se
    extingue) y >= 5 nacimientos. Un carro ESTABILIZA en una semilla si persisten > la mitad de sus 9 linajes; ESTABILIZA
    la serie si lo hace en >= 15/20 semillas.
  TAMANO del linaje (cuerpos vivos, muestreo cada 100 pasos): media y minimo en t >= 10000, maximo, final.
  GENERACIONES: profundidad genealogica maxima (fundador = 0).
  MUERTES VOLUNTARIAS: declaradas por el carro (O3 'cuerpos_term', O4 'senescentes'); la fisica (ENMIENDA 6) al lado, sin valor (ERR-103).
Uso:
  humo (un proceso):  python experimentos/generaciones/corre_convive.py --humo [--carro O2] [--T 20000] [--desde 10001]
  serie (coordinador): python experimentos/generaciones/corre_convive.py --serie --desde 10101 --n 20 --pool 6
  replica:             python experimentos/generaciones/corre_convive.py --serie --desde 10121 --n 20 --pool 6
"""
import argparse, gzip, importlib.util, json, os, platform, statistics as st, sys, time

sys.stdout.reconfigure(encoding='utf-8', errors='replace')
AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
CARRERA = os.path.join(RAIZ, 'experimentos', 'carrera_escuderias')
sys.path.insert(0, AQUI)
import pista2 as P2
import motor_convive as MC

DATOS = os.path.join(AQUI, 'datos')
CARROS_SERIE = ('FABRICA', 'O1', 'O2', 'O3', 'O4', 'CTRL_O3_SINTERM')
CTRL = {'CTRL_O3_SINTERM': os.path.join(AQUI, 'carros_ctrl', 'CTRL_O3_SINTERM.py')}   # control de H-b (construye_ctrl_o3.py)
T_DEF = 100000
T_CORTE = 10000
MIN_NAC = 5
SEMILLAS = dict(practica=(10001, 10040), serie=(10101, 10120), replica=(10121, 10140))
MIN_EVAL = 10      # H y H-b solo se evaluan si algun carro implicado tiene >= 10 linajes-semilla persistentes (si no: piso)
TOL_PERSISTE = 15  # H: "igual o mejor" = O2 >= O3 - 15 y >= O4 - 15 de 180 (~1.6-2 DE de la diferencia bajo un modelo binomial con p 0.2-0.4 por linaje)


def _rc():
    spec = importlib.util.spec_from_file_location('revisa_carro', os.path.join(CARRERA, 'revisa_carro.py'))
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m


def ruta_carro(c):
    return CTRL.get(c) or os.path.join(P2.CARROS, c + '.py')


def espec(c):
    """el carro para pista2.run: el ID (carros de la carrera) o el par (etiqueta, modulo) de un control de esta carpeta."""
    if c not in CTRL: return c
    spec = importlib.util.spec_from_file_location(f"carro_{c}", CTRL[c]); m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m); return (c, m)


def med(xs):
    xs = [x for x in xs if x is not None]
    return round(float(st.median(xs)), 3) if xs else None


def media(xs):
    xs = [x for x in xs if x is not None]
    return round(sum(xs) / len(xs), 4) if xs else None


def resumen_linaje(d, T, muestra):
    ind = d['individuos']   # [k, gen, padre, t_nace, t_muere, hijos, fundador, causa, vol_decl]
    tc = T // 2
    coh = [x for x in ind if x[3] <= tc]
    cens = [x for x in coh if x[4] < 0]
    compl = [x for x in coh if x[4] >= 0]
    muertos = [x for x in ind if x[4] >= 0]
    tf = d['t_fund']; fund = d['fundadores']
    fpost = sum(1 for t in tf if t >= T_CORTE) + max(0, fund - len(tf))   # tope 200 de t_fund: los que faltan cuentan como tardios
    tam = d['tam']; i0 = T_CORTE // muestra
    tam_post = tam[i0:-1] if len(tam) > i0 + 1 else tam
    nac = d['nacimientos']
    vd = d['_carrera']['muertes_vol_decl']; vf = d['_carrera']['muertes_vol']; mu = d['deaths']
    return dict(id=d['_carrera']['id'], etiqueta=d['_carrera']['etiqueta'], nac=nac, muertes=mu, fundadores=fund,
                fund_post10k=fpost, persiste=bool(fpost == 0 and nac >= MIN_NAC), sin_extincion=bool(fpost == 0),
                R0_coh=media([x[5] for x in coh]), n_coh=len(coh), cens_frac=(round(len(cens) / len(coh), 4) if coh else None),
                R0_compl=media([x[5] for x in compl]), R0_muertos=media([x[5] for x in muertos]),
                tam_media=media(tam_post), tam_min=(min(tam_post) if tam_post else None), tam_max=max(tam), tam_final=d['vivos_final'],
                gen_max=max(x[1] for x in ind), vida_med=med([x[4] - x[3] for x in muertos]),
                frac_sin_hijos=(round(sum(1 for x in muertos if x[5] == 0) / len(muertos), 4) if muertos else None),
                vol_decl=vd, vol_decl_vivos_T=d['_carrera']['vol_decl_vivos_T'], vol_fis=vf,
                frac_vol_decl=(round(vd / mu, 4) if mu else None), frac_vol_fis=(round(vf / mu, 4) if mu else None),
                causas=d['_carrera']['causas'], bloqueados=d['bloqueados'], vetos=d['vetos'])


def tarea(args):
    seed, carro, T, rep, tope, rrep = args
    t0 = time.time()
    r = P2.run(seed, [espec(carro)] * 9, T=T, diag=0, solapadas=1, reposicion=rep, tope_cuerpos=tope, r_rep=rrep)
    ps = r['pista']
    L = [resumen_linaje(d, T, ps['muestra']) for d in r['linajes']]
    crudo = [dict(individuos=d['individuos'], tam=d['tam'], t_fund=d['t_fund']) for d in r['linajes']]
    return dict(seed=seed, carro=carro, seg=round(time.time() - t0, 1), linajes=L, crudo=crudo,
                pista={k: v for k, v in ps.items() if k not in ('pizarra_final',)}, pizarra_log=r['pizarra_log'])


def agrega(R, carro):
    xs = [l for c in R if c['carro'] == carro for l in c['linajes']]
    sem = [c for c in R if c['carro'] == carro]
    est = [sum(l['persiste'] for l in c['linajes']) > len(c['linajes']) / 2 for c in sem]
    tot = [media(c['pista']['tam_total'][T_CORTE // c['pista']['muestra']:-1]) for c in sem]
    return dict(carro=carro, n_semillas=len(sem), n_linajes=len(xs), persisten=sum(l['persiste'] for l in xs),
                sin_extincion=sum(l['sin_extincion'] for l in xs), semillas_estabiliza=sum(est),
                semillas_persiste_carro=sum(any(l['persiste'] for l in c['linajes']) for c in sem),
                estabiliza_serie=bool(sum(est) >= 0.75 * len(sem)) if sem else None,
                R0_coh_med=med([l['R0_coh'] for l in xs]), R0_compl_med=med([l['R0_compl'] for l in xs]),
                R0_muertos_med=med([l['R0_muertos'] for l in xs]), cens_frac_med=med([l['cens_frac'] for l in xs]),
                tam_media_med=med([l['tam_media'] for l in xs]), tam_min_med=med([l['tam_min'] for l in xs]),
                tam_final_med=med([l['tam_final'] for l in xs]), gen_max_med=med([l['gen_max'] for l in xs]),
                vida_med=med([l['vida_med'] for l in xs]), nac_med=med([l['nac'] for l in xs]), muertes_med=med([l['muertes'] for l in xs]),
                fundadores_tot=sum(l['fundadores'] for l in xs), fund_post10k_tot=sum(l['fund_post10k'] for l in xs),
                vol_decl=sum(l['vol_decl'] for l in xs), vol_fis=sum(l['vol_fis'] for l in xs), muertes=sum(l['muertes'] for l in xs),
                frac_vol_decl=(round(sum(l['vol_decl'] for l in xs) / max(1, sum(l['muertes'] for l in xs)), 4)),
                total_cuerpos_med=med(tot), max_vivos=max((c['pista']['max_vivos'] for c in sem), default=None),
                bloqueados=sum(c['pista']['bloqueados'] for c in sem), seg_med=med([c['seg'] for c in sem]))


# ---- PREDICCIONES FIRMADAS (PREREGISTRO_convive.md; se fijan ANTES de la serie y no se tocan)
PRED = [
    ("H (coordinador): O2 persiste igual o mejor que O3 y O4 (persisten O2 >= O3 - 15 y >= O4 - 15, de 180)",
     lambda A: A['O2']['persisten'] >= A['O3']['persisten'] - TOL_PERSISTE and A['O2']['persisten'] >= A['O4']['persisten'] - TOL_PERSISTE),
    ("H-b (mecanismo): la muerte programada no da ventaja: O3 <= CTRL_O3_SINTERM + 15 y O4 <= O1 + 15 (persisten, de 180)",
     lambda A: A['O3']['persisten'] <= A['CTRL_O3_SINTERM']['persisten'] + TOL_PERSISTE and A['O4']['persisten'] <= A['O1']['persisten'] + TOL_PERSISTE),
]
PRED_NEC = {0: ('O2', 'O3', 'O4'), 1: ('O1', 'O3', 'O4', 'CTRL_O3_SINTERM')}
PRED_CARRO = {}   # se llena desde el PREREGISTRO (rango de persisten y de tam_media_med por carro); ver abajo


def carga_pred():
    """Rangos FIRMADOS por carro (PREREGISTRO_convive.md sec. 5; fijados tras el humo 10012 y ANTES de la serie):
    persisten [lo, hi] de 180 linajes-semilla; tam = mediana del tamano medio del linaje en t >= 10000;
    carro = semillas (de 20) en que persiste AL MENOS un linaje del carro."""
    return {
        'FABRICA': dict(persisten=(0, 5), tam=(0.9, 1.2), carro=(0, 2)),
        'O1': dict(persisten=(0, 30), tam=(1.1, 2.2), carro=(8, 20)),
        'O2': dict(persisten=(5, 45), tam=(1.1, 2.2), carro=(12, 20)),
        'O3': dict(persisten=(10, 60), tam=(1.2, 2.5), carro=(15, 20)),
        'O4': dict(persisten=(5, 50), tam=(1.0, 2.0), carro=(12, 20)),
        'CTRL_O3_SINTERM': dict(persisten=(10, 60), tam=(1.2, 2.5), carro=(15, 20)),
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--humo', action='store_true')
    ap.add_argument('--serie', action='store_true')
    ap.add_argument('--carro', default=None)   # uno solo (si falta: los cinco de CARROS_SERIE)
    ap.add_argument('--desde', type=int, default=None)
    ap.add_argument('--n', type=int, default=20)
    ap.add_argument('--T', type=int, default=None)
    ap.add_argument('--reposicion', default='fija')
    ap.add_argument('--tope', type=int, default=MC.TOPE_DEF)
    ap.add_argument('--r_rep', type=float, default=MC.R_REP)
    ap.add_argument('--pool', type=int, default=int(os.environ.get('JUACO_POOL', 0)))
    a = ap.parse_args()
    if a.humo == a.serie: raise SystemExit("CONVIVE: --humo o --serie (uno)")
    carros = [a.carro] if a.carro else list(CARROS_SERIE)
    if a.humo:
        T = a.T or 20000; desde = a.desde or 10001; semillas = [desde]; pool = 0
        lo, hi = SEMILLAS['practica']
        if not lo <= desde <= hi: raise SystemExit(f"CONVIVE: el humo usa semillas de practica {lo}-{hi}")
        et = f"humo_{'_'.join(carros) if len(carros) < 5 else 'cinco'}_s{desde}_T{T}"
    else:
        T = a.T or T_DEF; desde = a.desde or SEMILLAS['serie'][0]; semillas = list(range(desde, desde + a.n)); pool = a.pool
        et = f"serie_s{semillas[0]}-{semillas[-1]}_T{T}"
    et += f"_{a.reposicion}" + (f"_tope{a.tope}" if a.tope != MC.TOPE_DEF else '') + (f"_r{a.r_rep}" if a.r_rep != MC.R_REP else '')
    os.makedirs(DATOS, exist_ok=True)
    pre = f"convive_{et}_{time.strftime('%Y%m%d_%H%M%S')}"
    LOGF = open(os.path.join(DATOS, pre + '.log'), 'w', encoding='utf-8')

    def log(s=''):
        print(s, flush=True); LOGF.write(s + '\n'); LOGF.flush()

    t0 = time.time()
    RC = _rc()
    shas = {c: P2.h16(ruta_carro(c)) for c in carros}
    log(f"CONVIVE · {et} · {time.strftime('%Y-%m-%d %H:%M:%S')} · python {platform.python_version()} · pool {pool or 'NO (un proceso)'}")
    log(f"  pista2 {P2.h16(os.path.join(AQUI, 'pista2.py'))} · motor {P2.h16(os.path.join(AQUI, 'motor_convive.py'))} · juez "
        f"{P2.h16(os.path.abspath(__file__))} · carros {shas}")
    log(f"  9 fundadores por carro · semillas {semillas[0]}-{semillas[-1]} · T={T} · reposicion {a.reposicion} · r_rep {a.r_rep} · tope {a.tope}")
    rv = {c: RC.revisa_fuente(open(ruta_carro(c), encoding='utf-8').read(), c) for c in carros}
    for c, v in rv.items(): log(f"  CHEQUEO ESTATICO {c}: {'PASA' if not v else 'RECHAZADO ' + str(v)}")
    if any(rv.values()): log("  un carro no pasa -> no se corre"); return 1
    # identidad corta: solapadas=0 == v1 (1 FABRICA compat, T=3000)
    spec = importlib.util.spec_from_file_location('pista', os.path.join(CARRERA, 'pista.py'))
    P1 = importlib.util.module_from_spec(spec); sys.modules['pista'] = P1; spec.loader.exec_module(P1)
    N = lambda x: json.loads(json.dumps(x, default=str))
    ide = N(P1.run(1, ['FABRICA'], T=3000, compat=1, pizarra=0)) == N(P2.run(1, ['FABRICA'], T=3000, compat=1, pizarra=0, solapadas=0))
    log(f"  IDENTIDAD CORTA solapadas=0 == pista v1 (1 FABRICA compat, T=3000): {'OK' if ide else 'FALLA'}")
    if not ide: return 1
    tareas = [(s, c, T, a.reposicion, a.tope, a.r_rep) for c in carros for s in semillas]
    R = []
    if pool and pool > 1:
        from multiprocessing import Pool
        with Pool(pool) as PL:
            for x in PL.imap_unordered(tarea, tareas):
                R.append(x); log(f"  [{time.time()-t0:8.1f}s] {x['carro']} s{x['seed']} ({x['seg']}s) persisten "
                                 f"{sum(l['persiste'] for l in x['linajes'])}/9 · cuerpos max {x['pista']['max_vivos']}")
    else:
        for tk in tareas:
            x = tarea(tk); R.append(x)
            log(f"  [{time.time()-t0:8.1f}s] {x['carro']} s{x['seed']} ({x['seg']}s) persisten {sum(l['persiste'] for l in x['linajes'])}/9 · "
                f"cuerpos max {x['pista']['max_vivos']} · bloqueados {x['pista']['bloqueados']}")
    R.sort(key=lambda x: (x['carro'], x['seed']))
    with gzip.open(os.path.join(DATOS, pre + '_pizarra.jsonl.gz'), 'wt', encoding='utf-8') as fz:
        for x in R:
            for e in x.pop('pizarra_log'): fz.write(json.dumps([x['carro'], x['seed']] + e) + chr(10))
    meta = dict(etiqueta=et, semillas=semillas, T=T, carros=carros, sha_carros=shas, reposicion=a.reposicion, r_rep=a.r_rep,
                tope=a.tope, sha_pista2=P2.h16(os.path.join(AQUI, 'pista2.py')), sha_motor=P2.h16(os.path.join(AQUI, 'motor_convive.py')),
                sha_juez=P2.h16(os.path.abspath(__file__)), identidad_corta=ide, T_CORTE=T_CORTE, MIN_NAC=MIN_NAC, cohorte='t_nace <= T/2')
    crudo = os.path.join(DATOS, pre + '.json')
    json.dump(dict(meta=meta, corridas=R), open(crudo, 'w', encoding='utf-8'), ensure_ascii=False)
    log(f"  CRUDO {crudo} (sha {P2.h16(crudo)})")
    A = {c: agrega(R, c) for c in carros}
    log("\n  carro   | persisten/lin | sin ext | sem estab (con >=1 lin) | R0_coh (cens) | R0_compl | R0_muertos | tam media/min/final | gen max | vida | vol decl/muertes | cuerpos (max) | bloq | s/semilla")
    for c in carros:
        x = A[c]
        log(f"  {c:7s} | {x['persisten']:3d}/{x['n_linajes']:3d} | {x['sin_extincion']:3d} | {x['semillas_estabiliza']:2d}/{x['n_semillas']} "
            f"({x['semillas_persiste_carro']}) | {x['R0_coh_med']} ({x['cens_frac_med']}) | {x['R0_compl_med']} | {x['R0_muertos_med']} | {x['tam_media_med']}/{x['tam_min_med']}/{x['tam_final_med']} "
            f"| {x['gen_max_med']} | {x['vida_med']} | {x['vol_decl']}/{x['muertes']} ({x['frac_vol_decl']}) | {x['total_cuerpos_med']} ({x['max_vivos']}) "
            f"| {x['bloqueados']} | {x['seg_med']}")
    ev = []
    if a.serie:
        PC = carga_pred()
        log("\n  PREDICCIONES FIRMADAS (PREREGISTRO_convive.md)")
        for j, (txt, f) in enumerate(PRED):
            if all(c in A for c in PRED_NEC[j]):
                if max(A[c]['persisten'] for c in PRED_NEC[j]) < MIN_EVAL:   # trampa del piso: todos en ~0 -> H trivial
                    ev.append([txt, None]); log(f"   - {txt}: NO EVALUABLE (ningun carro llega a {MIN_EVAL} linajes persistentes)"); continue
                ok = bool(f(A)); ev.append([txt, ok]); log(f"   - {txt}: {'SE CUMPLE' if ok else 'NO se cumple (REFUTADA)'}")
        for c in carros:
            if c in PC:
                p = PC[c]; ok1 = p['persisten'][0] <= A[c]['persisten'] <= p['persisten'][1]
                tm = A[c]['tam_media_med']; ok2 = tm is not None and p['tam'][0] <= tm <= p['tam'][1]
                ok3 = p['carro'][0] <= A[c]['semillas_persiste_carro'] <= p['carro'][1]
                ev.append([f"{c} persisten en {p['persisten']}", ok1]); ev.append([f"{c} tam medio en {p['tam']}", ok2])
                ev.append([f"{c} semillas con >= 1 linaje que persiste en {p['carro']}", ok3])
                log(f"   - {c}: persisten {A[c]['persisten']} en {p['persisten']}: {'SI' if ok1 else 'NO'} · tam medio {tm} en {p['tam']}: "
                    f"{'SI' if ok2 else 'NO'} · semillas con >= 1 linaje persistente {A[c]['semillas_persiste_carro']} en {p['carro']}: {'SI' if ok3 else 'NO'}")
                if A[c]['bloqueados']: log(f"     MARCA: {c} alcanzo el tope de seguridad ({A[c]['bloqueados']} partos bloqueados): la densidad NO la regulo el mundo")
    res = os.path.join(DATOS, pre + '_resumen.json')
    json.dump(dict(meta=meta, agregado=A, predicciones=ev,
                   por_semilla=[dict(carro=x['carro'], seed=x['seed'], seg=x['seg'], linajes=x['linajes'],
                                     pista={k: x['pista'][k] for k in ('max_vivos', 'bloqueados', 't_tope', 'nobj_medio', 'llegadas',
                                                                       'llegadas_perdidas', 'pisos', 'comp_mundo', 'olvidos')})
                                for x in R]), open(res, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    log(f"  RESUMEN {res}\nTerminado en {time.time()-t0:.1f}s")
    return 0


if __name__ == '__main__':
    sys.exit(main())
