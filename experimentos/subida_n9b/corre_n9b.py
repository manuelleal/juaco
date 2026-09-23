"""corre_n9b.py — corredor de subida_n9b: ¿la ventaja que APR aprende pasa por PREDECIR SU PROPIO ESTADO?

MISION: llegar a la AGI por este camino. Preregistro: PREREGISTRO_n9b.md (letra, "pierde", predicciones, criterio).

ENTRADA (regla 14, campo a campo): la MISMA de juez.tarea / corre_aprende.tarea: pista.run(seed, carros, T, pizarra=1,
rep_acum=0, escala=1, mundo_n=None) y juez.resumen_linaje (solo fisica, ERR-96). La telemetria del carro (d['carro']['apr'])
va aparte y no puntua. Antes de correr: shas, construccion por anclas, chequeo estatico, identidad corta del juez,
mini identidad APR_LES_OFF == APR (s 13599) y entrada campo a campo. Si algo falla, NO corre.

BRAZOS (9 carros iguales, pista escalada L 360 / 36 objetos, T = 100000):
  apr APR · fab FABRICA · plana APR_LES_PLANA · cruz APR_LES_CRUZ · mundo APR_LES_MUNDO
Semillas: practica 13581-13598 (solo --humo) · serie 13501-13520 · replica 13521-13540. El corredor se niega a usar otras.

ERR-115: el parser es una LISTA BLANCA y ABORTA ante cualquier bandera desconocida, abreviada, con '=' o repetida,
incluidas -h/--help. Formas validas (exactas):
  python experimentos/subida_n9b/corre_n9b.py --humo [--desde 13591] [--n 1] [--T 20000] [--brazos apr,fab,...]   (UN proceso)
  python experimentos/subida_n9b/corre_n9b.py --serie --desde 13501 --n 20 --pool 6       (SOLO el coordinador)
  python experimentos/subida_n9b/corre_n9b.py --serie --desde 13521 --n 20 --pool 6       (replica; SOLO el coordinador)
  python experimentos/subida_n9b/corre_n9b.py --veredicto <resumen_serie.json>,<resumen_replica.json>   (no corre nada)
ERR-54: el crudo se escribe ANTES de resumir. Vocabulario: "linaje", "cuerpo"; prohibido "poblacion", "evoluciona", "sabe".
"""
import json, os, platform, statistics as st, sys, time

sys.stdout.reconfigure(encoding='utf-8', errors='replace')
AQUI = os.path.dirname(os.path.abspath(__file__))
if AQUI not in sys.path: sys.path.insert(0, AQUI)
import comun_n9b as K   # noqa: E402  (fija P.CARROS / RC.CARROS en esta carpeta; tambien en los hijos del Pool)
P, J, RC = K.P, K.J, K.RC

DATOS = os.path.join(AQUI, 'datos'); HUMO = os.path.join(DATOS, 'humo')
PRACTICA = range(13581, 13599); SERIE = range(13501, 13521); REPLICA = range(13521, 13541)
T_DEF = 100000; MINI = 13599
PIERDE_N = 15; PIERDE_DIF = 0.025; ANCLA_N = 15; ANCLA_DIF = 0.03; VM_TOPE = 0.10   # PREREGISTRO_n9b.md sec. 4, 6


# ------------------------------------------------------------------------------------------------ parser (ERR-115)
class BanderaMala(SystemExit):
    pass


def parsea(argv):
    """Lista blanca estricta. Devuelve dict; ante cualquier cosa fuera de la lista lanza BanderaMala (SystemExit)."""
    CON_VALOR = {'--desde': int, '--n': int, '--T': int, '--pool': int, '--brazos': str, '--veredicto': str}
    SIN_VALOR = {'--humo', '--serie'}
    a = dict(humo=False, serie=False, desde=None, n=None, T=None, pool=None, brazos=None, veredicto=None); vistos = set(); i = 0
    while i < len(argv):
        tk = argv[i]
        if tk in vistos: raise BanderaMala(f"corre_n9b: bandera repetida {tk!r} -> ABORTA (ERR-115)")
        if tk in SIN_VALOR:
            a[tk[2:]] = True; vistos.add(tk); i += 1; continue
        if tk in CON_VALOR:
            if i + 1 >= len(argv) or argv[i + 1].startswith('-'): raise BanderaMala(f"corre_n9b: {tk} sin valor -> ABORTA (ERR-115)")
            try: a[tk[2:]] = CON_VALOR[tk](argv[i + 1])
            except ValueError: raise BanderaMala(f"corre_n9b: valor invalido para {tk}: {argv[i + 1]!r} -> ABORTA (ERR-115)")
            vistos.add(tk); i += 2; continue
        raise BanderaMala(f"corre_n9b: bandera desconocida {tk!r} (validas: {sorted(SIN_VALOR | set(CON_VALOR))}; "
                          f"sin abreviaturas, sin '=', sin --help) -> ABORTA sin correr nada (ERR-115)")
    modos = [m for m in ('humo', 'serie', 'veredicto') if a[m]]
    if len(modos) != 1: raise BanderaMala(f"corre_n9b: hace falta exactamente uno de --humo / --serie / --veredicto (hay {modos}) -> ABORTA")
    if a['brazos'] is not None:
        bz = [b.strip() for b in a['brazos'].split(',') if b.strip()]
        if not bz or any(b not in K.BRAZOS for b in bz) or len(set(bz)) != len(bz):
            raise BanderaMala(f"corre_n9b: --brazos {a['brazos']!r} invalido (validos {list(K.BRAZOS)}) -> ABORTA")
        a['brazos'] = bz
    if a['humo']:
        if a['pool'] not in (None, 0): raise BanderaMala("corre_n9b: --humo es de UN proceso (sin --pool) -> ABORTA")
        a['desde'] = a['desde'] or 13591; a['n'] = a['n'] or 1; a['T'] = a['T'] or 20000; a['brazos'] = a['brazos'] or list(K.BRAZOS)
        sem = range(a['desde'], a['desde'] + a['n'])
        if not all(s in PRACTICA for s in sem): raise BanderaMala("corre_n9b: --humo solo con semillas de practica 13581-13598 -> ABORTA")
        corr = a['n'] * len(a['brazos'])
        if corr > 6 or corr * a['T'] > 200000: raise BanderaMala(f"corre_n9b: humo de {corr} corridas x T {a['T']} excede 6 corridas / 200000 pasos -> ABORTA")
    elif a['serie']:
        if a['desde'] not in (13501, 13521) or a['n'] != 20: raise BanderaMala("corre_n9b: --serie solo --desde 13501 --n 20 (serie) o --desde 13521 --n 20 (replica) -> ABORTA")
        if a['T'] not in (None, T_DEF): raise BanderaMala("corre_n9b: --serie con T = 100000 (preregistrado) -> ABORTA")
        if a['brazos'] not in (None, list(K.BRAZOS)): raise BanderaMala("corre_n9b: --serie corre los 5 brazos preregistrados -> ABORTA")
        if not a['pool'] or a['pool'] < 1: raise BanderaMala("corre_n9b: --serie exige --pool N explicito (N >= 1) -> ABORTA")
        a['T'] = T_DEF; a['brazos'] = list(K.BRAZOS)
    else:
        if any(a[k] is not None for k in ('desde', 'n', 'T', 'pool', 'brazos')): raise BanderaMala("corre_n9b: --veredicto no lleva otras banderas -> ABORTA")
        rutas = [r.strip() for r in a['veredicto'].split(',')]
        if len(rutas) != 2: raise BanderaMala("corre_n9b: --veredicto <resumen_serie.json>,<resumen_replica.json> -> ABORTA")
        a['veredicto'] = rutas
    return a


# ------------------------------------------------------------------------------------------------ tarea (== juez.tarea)
def tarea(args):
    """== juez.tarea (misma llamada a la pista, mismo resumen fisico) + la telemetria del carro aparte."""
    seed, carros, T = args
    t0 = time.time()
    r = P.run(seed, carros, T=T, pizarra=1, rep_acum=0, escala=1, mundo_n=None)
    L = [J.resumen_linaje(d, seed) for d in r['linajes']]
    sd = sum(x['descendientes'] for x in L); sm = sum(x['muertes'] for x in L)
    for x in L:
        tf, qf, nr = J.t_fund_reconstruido(x['telem']['vidas'], x['telem']['desc_por_vida'])
        x['t_fund_rec_ok'] = bool(tf[:200] == x['telem']['t_fund'] and qf == x['cola_final'] and nr == x['nac_reales'])
    apr = [d['carro'].get('apr') for d in r['linajes']]
    return dict(seed=seed, seg=round(time.time() - t0, 1), linajes=L, pista=r['pista'],
                R0_pista=round(sd / (sm + len(L)), 4), pizarra_log=r['pizarra_log'], apr=apr)


def tarea_brazo(args):
    seed, brazo, T = args
    x = tarea((seed, [K.BRAZOS[brazo]] * 9, T)); x['brazo'] = brazo
    return x


def entrada_campo_a_campo(log, seed=MINI, T=2000):
    """Regla 14: esta tarea == juez.tarea (linajes y pista), 9 FABRICA."""
    a = tarea((seed, ['FABRICA'] * 9, T)); b = J.tarea((seed, ['FABRICA'] * 9, T, 1, 0, 1, None))
    Nn = lambda x: json.loads(json.dumps(x, default=str))
    ok = Nn(a['linajes']) == Nn(b['linajes']) and Nn(a['pista']) == Nn(b['pista']) and a['R0_pista'] == b['R0_pista']
    log(f"  ENTRADA campo a campo (regla 14): corre_n9b.tarea == juez.tarea (9 FABRICA, s {seed}, T {T}): {'OK' if ok else 'FALLA'}")
    return ok


def mini_identidad(log, seed=MINI, T=2000):
    a = P.run(seed, ['APR'] * 9, T=T, pizarra=1, rep_acum=0, escala=1, mundo_n=None)
    b = P.run(seed, ['APR_LES_OFF'] * 9, T=T, pizarra=1, rep_acum=0, escala=1, mundo_n=None)
    ok = K.normaliza(a) == K.normaliza(b, 'APR_LES_OFF')
    log(f"  MINI IDENTIDAD APR_LES_OFF == APR (N 9, s {seed}, T {T}, toda la salida de pista.run): {'OK' if ok else 'FALLA'}")
    return ok


# ------------------------------------------------------------------------------------------------ resumen
def med(xs):
    xs = [x for x in xs if x is not None]
    return round(float(st.median(xs)), 4) if xs else None


def por_semilla(R):
    return {c['seed']: st.median([l['R0'] for l in c['linajes']]) for c in R}


def pareado(Ra, Rb):
    ma, mb = por_semilla(Ra), por_semilla(Rb)
    com = sorted(set(ma) & set(mb)); d = [ma[k] - mb[k] for k in com]
    return dict(semillas=len(com), gana=sum(1 for x in d if x > 0), dif_med=(round(float(st.median(d)), 4) if d else None),
                por_semilla={str(k): round(ma[k] - mb[k], 4) for k in com})


def fraccion_perdida(Rapr, Rx, Rfab):
    a, x, f = por_semilla(Rapr), por_semilla(Rx), por_semilla(Rfab)
    fr = [(a[k] - x[k]) / (a[k] - f[k]) for k in sorted(set(a) & set(x) & set(f)) if a[k] - f[k] > 0.005]
    return dict(mediana=(round(float(st.median(fr)), 4) if fr else None), semillas_validas=len(fr))


def resume(R, brazo, log):
    todos = [l for c in R for l in c['linajes']]
    cm = J.criterio_mono(todos)
    cz = {k: sum(l['causas'][k] for l in todos) for k in ('hambre', 'sed', 'veneno', 'sal')}
    out = dict(brazo=brazo, carro=K.BRAZOS[brazo], criterio_enm3=cm, R0_med_todos=med([l['R0'] for l in todos]),
               R0_pista_med=med([c['R0_pista'] for c in R]), vida_med=med([l['vida_med'] for l in todos]), causas=cz,
               muertes_med=med([l['muertes'] for l in todos]), frac_sin_bueno_mundo_med=med([c['pista']['frac_sin_bueno_mundo'] for c in R]),
               coherente=[sum(l['coherente'] for l in todos), len(todos)], t_fund_rec=[sum(l['t_fund_rec_ok'] for l in todos), len(todos)],
               escrituras=sum(l['escrituras'] for l in todos))
    ap = [a for c in R for a in c['apr'] if a]
    if ap:
        opp = [sum(a['opp_q'][i] for a in ap) for i in range(4)]; mq = [sum(a['mord_q'][i] for a in ap) for i in range(4)]
        qq = [sum(a['quit_q'][i] for a in ap) for i in range(4)]
        out['opcion'] = dict(oportunidades=sum(opp), tasa_global=round(sum(mq) / max(1, sum(opp)), 4),
                             quitadas_ultimo_cuarto=(round(qq[3] / opp[3], 4) if opp[3] else None),
                             fabrica_habria_mordido=round(sum(a['fab_mord'] for a in ap) / max(1, sum(opp)), 4),
                             w_mediana=[[med([a['w'][i][j] for a in ap]) for j in range(len(ap[0]['w'][0]))] for i in range(2)])
        ls = [a['lesion'] for a in ap if 'lesion' in a]
        if ls:
            n = sum(s['n'] for s in ls)
            les = dict(decisiones=n, post_real_media=round(sum(s['post_real'] for s in ls) / max(1, n), 4),
                       post_usado_media=round(sum(s['post_usado'] for s in ls) / max(1, n), 4),
                       frac_cambia_post=round(sum(s['cambia_post'] for s in ls) / max(1, n), 4),
                       frac_caida_real=round(sum(s['caida_real'] for s in ls) / max(1, n), 4),
                       frac_caida_usada=round(sum(s['caida_usada'] for s in ls) / max(1, n), 4),
                       frac_cambia_mundo=round(sum(s['cambia_mundo'] for s in ls) / max(1, n), 4))
            les['VM_cumple'] = abs(les['post_usado_media'] - les['post_real_media']) <= VM_TOPE
            out['lesion'] = les
    tot = max(1, sum(cz.values())); cmx = cm
    log(f"\n== {brazo} ({K.BRAZOS[brazo]} x9) · {len(R)} semillas · T {R[0]['pista']['T']}")
    log(f"  R0 por linaje-semilla: mediana {out['R0_med_todos']} · R0 pista (mediana por semilla) {out['R0_pista_med']} · vida mediana {out['vida_med']} · muertes mediana {out['muertes_med']}")
    log(f"  ENMIENDA 3: mediana R0 eval {cmx['mediana_R0_eval']} · R0 real eval {cmx['mediana_R0_real_eval']} · sin fund tras 10000 {cmx['frac_eval_sin_fund']} · "
        f"evaluables {cmx['evaluables']}/{cmx['n']} -> {'CRUZA' if cmx['cruza'] else 'NO CRUZA'}")
    log(f"  causas h/s/v/sal {cz['hambre']}/{cz['sed']}/{cz['veneno']}/{cz['sal']} ({cz['veneno']/tot:.0%} veneno, {cz['sal']/tot:.0%} sal) · "
        f"sin bueno en el mundo {out['frac_sin_bueno_mundo_med']} · coherente {out['coherente']} · t_fund {out['t_fund_rec']} · escrituras {out['escrituras']}")
    if 'opcion' in out:
        o = out['opcion']
        log(f"  opcion (no puntua): oportunidades {o['oportunidades']} · tasa {o['tasa_global']} (FABRICA habria {o['fabrica_habria_mordido']}) · "
            f"quitadas ult. cuarto {o['quitadas_ultimo_cuarto']} · Q mediana no/morder {o['w_mediana']}")
    if 'lesion' in out:
        s = out['lesion']
        log(f"  lesion (no puntua): decisiones {s['decisiones']} · post real {s['post_real_media']} / usado {s['post_usado_media']} · "
            f"cambia post {s['frac_cambia_post']} · caida predicha real {s['frac_caida_real']} / usada {s['frac_caida_usada']} · "
            f"cambia mundo {s['frac_cambia_mundo']} · V-M (|usado-real| <= {VM_TOPE}) {'SE CUMPLE' if s['VM_cumple'] else 'NO se cumple'}")
    return out


def pierde(par):
    return par is not None and par['gana'] >= PIERDE_N and par['dif_med'] is not None and par['dif_med'] >= PIERDE_DIF


def veredicto_serie(res, par):
    anc = par.get('apr_vs_fab')
    ancla = anc is not None and anc['gana'] >= ANCLA_N and anc['dif_med'] is not None and anc['dif_med'] >= ANCLA_DIF
    pl, cr, mu = (pierde(par.get(f'apr_vs_{x}')) if f'apr_vs_{x}' in par else None for x in ('plana', 'cruz', 'mundo'))
    instr = all(r['coherente'][0] == r['coherente'][1] and r['t_fund_rec'][0] == r['t_fund_rec'][1] and r['escrituras'] == 0 for r in res.values())
    return dict(ancla=ancla, pierde_plana=pl, pierde_cruz=cr, pierde_mundo=mu, instrumento_ok=instr)


def veredicto_final(v1, v2):
    if not (v1['instrumento_ok'] and v2['instrumento_ok']): return 'INSTRUMENTO FALLA (no se lee)'
    if not (v1['ancla'] and v2['ancla']): return 'NO EVALUABLE (APR no gana a FABRICA en las dos series)'
    if None in (v1['pierde_plana'], v1['pierde_cruz'], v1['pierde_mundo'], v2['pierde_plana'], v2['pierde_cruz'], v2['pierde_mundo']):
        return 'INCOMPLETO (faltan brazos)'
    pl = v1['pierde_plana'] and v2['pierde_plana']; cr = v1['pierde_cruz'] and v2['pierde_cruz']
    mu = v1['pierde_mundo'] and v2['pierde_mundo']; mu_no = (not v1['pierde_mundo']) and (not v2['pierde_mundo'])
    if pl and mu_no: return 'FUNCIONA (sin prediccion de si pierde la ventaja; el control del mundo no)'
    if pl and mu: return 'HAY ALGO MODESTO (a): PLANA y MUNDO pierden; depende de sus entradas, no especificamente de predecirse'
    if pl: return 'HAY ALGO MODESTO: PLANA pierde en las dos; MUNDO pierde en una sola (especificidad sin repetir)'
    if cr: return 'HAY ALGO MODESTO (b): solo CRUZ pierde; una prediccion de si equivocada cuesta, su ausencia no'
    return 'NO (la ventaja aprendida de APR es contencion general; no depende de predecir su propio estado)'


PRED = [
    ("P1 (ancla) APR > FABRICA en >= 15/20 con dif. mediana >= 0.03; APR mediana R0 en [0.36, 0.42], FABRICA en [0.30, 0.37] (p 0.85)",
     lambda r, p, v: None if not ('apr' in r and 'fab' in r) else bool(v['ancla'] and 0.36 <= r['apr']['R0_med_todos'] <= 0.42 and 0.30 <= r['fab']['R0_med_todos'] <= 0.37)),
    ("P2 APR_LES_PLANA pierde (p 0.35; el creador la da por REFUTADA con p 0.65)", lambda r, p, v: v['pierde_plana']),
    ("P3 APR_LES_CRUZ pierde (p 0.30)", lambda r, p, v: v['pierde_cruz']),
    ("P4 (control) APR_LES_MUNDO NO pierde (p 0.80)", lambda r, p, v: None if v['pierde_mundo'] is None else not v['pierde_mundo']),
    ("P5 APR_LES_PLANA > FABRICA en >= 15/20 (p 0.70)", lambda r, p, v: None if 'plana_vs_fab' not in p else p['plana_vs_fab']['gana'] >= 15),
    ("P6 ningun brazo cruza la ENMIENDA 3 (p 0.97)", lambda r, p, v: None if not r else not any(x['criterio_enm3']['cruza'] for x in r.values())),
    ("P7 fraccion mediana de la ganancia que pierde PLANA en [0.0, 0.5] (p 0.65)",
     lambda r, p, v: None if p.get('frac_perdida_plana', {}).get('mediana') is None else 0.0 <= p['frac_perdida_plana']['mediana'] <= 0.5),
]


def modo_veredicto(rutas):
    vs = []
    for ru in rutas:
        d = json.load(open(ru, encoding='utf-8'))
        if d.get('humo'): raise SystemExit(f"--veredicto: {ru} es un HUMO; solo serie y replica")
        vs.append((d['semillas'][0], d['veredicto_serie']))
    vs.sort()
    if [v[0] for v in vs] != [13501, 13521]: raise SystemExit(f"--veredicto: hacen falta la serie 13501 y la replica 13521 (hay {[v[0] for v in vs]})")
    print(f"serie 13501: {vs[0][1]}\nreplica 13521: {vs[1][1]}\nVEREDICTO (PREREGISTRO_n9b.md sec. 6): {veredicto_final(vs[0][1], vs[1][1])}")
    return 0


def main(argv):
    a = parsea(argv)
    if a['veredicto']: return modo_veredicto(a['veredicto'])
    semillas = list(range(a['desde'], a['desde'] + a['n'])); T = a['T']; brazos = a['brazos']; pool = a['pool'] or 0
    dest = HUMO if a['humo'] else DATOS; os.makedirs(dest, exist_ok=True)
    sel = time.strftime('%Y%m%d_%H%M%S')
    pre = f"n9b_{'humo' if a['humo'] else 'serie'}_{'-'.join(brazos)}_s{semillas[0]}-{semillas[-1]}_T{T}_{sel}"
    LOGF = open(os.path.join(dest, pre + '.log'), 'w', encoding='utf-8')

    def log(s=''):
        print(s, flush=True); LOGF.write(s + '\n'); LOGF.flush()

    t0 = time.time()
    log(f"CORRE_N9B · {pre} · python {platform.python_version()} · pool {pool or 'NO (un proceso)'} · corre_n9b.py {K.h16(os.path.abspath(__file__))}")
    ok = True
    for ru, med_, fij, bien in K.verifica_shas():
        log(f"  sha {ru} {med_} (fijado {fij}) {'OK' if bien else 'FALLA'}"); ok = ok and bien
    esp, medido, bien = K.verifica_construccion()
    log(f"  construccion por anclas == carros en disco: {'OK' if bien else 'FALLA'} {medido}"); ok = ok and bien
    for c in sorted(set(K.BRAZOS.values()) | {'APR_LES_OFF'}):
        v = RC.revisa(c); log(f"  CHEQUEO ESTATICO {c}: {'PASA' if not v else 'RECHAZADO ' + str(v[:3])}"); ok = ok and not v
    ide = J.identidad_corta()
    log(f"  IDENTIDAD CORTA del juez (FABRICA == organismo_f9c REL, s 1, T 5000): {'OK' if ide['ok'] else 'FALLA ' + str(ide['dif'][:5])}")
    ok = ok and ide['ok'] and mini_identidad(log) and entrada_campo_a_campo(log)
    if not ok: log("  ALGO FALLA -> no se corre."); return 1
    tareas = [(sd, b, T) for b in brazos for sd in semillas]
    R = {b: [] for b in brazos}
    if pool > 1:
        from multiprocessing import Pool
        with Pool(pool) as PL:
            for x in PL.imap_unordered(tarea_brazo, tareas):
                R[x['brazo']].append(x); log(f"  [{time.time()-t0:7.1f}s] {x['brazo']} semilla {x['seed']} ({x['seg']}s) R0 pista {x['R0_pista']}")
    else:
        for tk in tareas:
            x = tarea_brazo(tk); R[x['brazo']].append(x)
            log(f"  [{time.time()-t0:7.1f}s] {x['brazo']} semilla {x['seed']} ({x['seg']}s) R0 pista {x['R0_pista']} · R0 por linaje {[l['R0'] for l in x['linajes']]}")
    for b in brazos:
        R[b].sort(key=lambda x: x['seed'])
        for x in R[b]: x.pop('pizarra_log')
    crudo = os.path.join(dest, pre + '_crudo.json')
    shas = {c: K.h16(os.path.join(K.CARROS_N9B, c + '.py')) for c in K.BRAZOS.values()}
    json.dump(dict(meta=dict(brazos=brazos, carros={b: K.BRAZOS[b] for b in brazos}, semillas=semillas, T=T, sha_carros=shas, humo=a['humo'],
                             sha_pista=K.h16(os.path.join(K.CARRERA, 'pista.py')), sha_juez=K.h16(os.path.join(K.CARRERA, 'juez.py')),
                             sha_runner=K.h16(os.path.abspath(__file__))), corridas=R), open(crudo, 'w', encoding='utf-8'), ensure_ascii=False)
    log(f"  CRUDO {crudo} (sha {K.h16(crudo)})   <- ERR-54: escrito ANTES de resumir")
    res = {b: resume(R[b], b, log) for b in brazos}
    par = {}
    log("\nPAREADOS (por semilla: mediana del R0 de los 9 linajes; gana = semillas en que la primera supera a la segunda)")
    for x, y in [('apr', 'fab')] + [('apr', l) for l in K.LESIONES] + [(l, 'fab') for l in K.LESIONES]:
        if x in R and y in R:
            par[f'{x}_vs_{y}'] = pareado(R[x], R[y]); q = par[f'{x}_vs_{y}']
            marca = ' -> PIERDE (sec. 4)' if (x == 'apr' and y in K.LESIONES and pierde(q)) else ''
            log(f"  {x} vs {y}: gana {q['gana']}/{q['semillas']} · dif. mediana {q['dif_med']}{marca} · {q['por_semilla']}")
    for l in K.LESIONES:
        if all(b in R for b in ('apr', 'fab', l)):
            par[f'frac_perdida_{l}'] = fraccion_perdida(R['apr'], R[l], R['fab'])
            log(f"  fraccion de la ganancia APR-FABRICA que pierde {l}: mediana {par[f'frac_perdida_{l}']['mediana']} ({par[f'frac_perdida_{l}']['semillas_validas']} semillas con APR-FAB > 0.005)")
    v = veredicto_serie(res, par)
    log(f"\nVEREDICTO DE ESTA SERIE (el final exige serie Y replica, --veredicto): {v}" + ("  -- HUMO: sin valor" if a['humo'] else ''))
    pred = []
    log("PREDICCIONES FIRMADAS (PREREGISTRO_n9b.md sec. 5)" + (" -- HUMO: T y semillas de practica, NO cuentan" if a['humo'] else ""))
    for txt, f in PRED:
        try: val = f(res, par, v)
        except (KeyError, TypeError): val = None
        pred.append(dict(texto=txt, se_cumple=val)); log(f"  {txt} -> {'SE CUMPLE' if val else ('no evaluable aqui' if val is None else 'NO se cumple')}")
    rj = os.path.join(dest, pre + '_resumen.json')
    json.dump(dict(brazos=res, pareados=par, veredicto_serie=v, predicciones=pred, semillas=semillas, T=T, humo=a['humo'],
                   crudo=os.path.basename(crudo), seg_total=round(time.time() - t0, 1)), open(rj, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    log(f"\n  RESUMEN {rj}\nTerminado en {time.time()-t0:.1f}s")
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
