"""corre_v143.py — corredor del bloque tronco_v14_3: EL BICHO REAL (v14.3 = v14.2 + piezas locales) en LA PISTA DE AYER.

MISION: llegar a la AGI por este camino. Pregunta (director, 23-sep): ¿cruza H-1 el ORGANISMO (sin politica escrita a mano) en la
misma pista donde ayer solo cruzaron carros cuya politica escribio un LLM? Preregistro: PREREGISTRO_v143.md (letra, controles,
predicciones firmadas, puntos). Carros: carros_v143/ (construye_v143.py) + FABRICA y O1 de la carrera (solo se leen).

PISTA (la de ayer, v1 escalada, sin tocar): experimentos/carrera_escuderias/pista.py, monocultivo de 9 carros iguales, L = 360,
36 objetos, olvido escalado, T = 100000, fundador_limpio = 1 (ENMIENDA 5: el fundador que pone el mundo es una instancia NUEVA,
sin nada del linaje; ERR-101 cerrado por construccion). Reserva ERR-104 vigente: en esta pista morder repone al instante. ERR-118:
no se usa la pista v2 (quimiostato) ni su "persiste el carro".

ENTRADA (regla 14, campo a campo): la MISMA de juez.tarea con fundador_limpio = 1 (args (seed, carros, T, 1, 0, 1, None, 1)) y
juez.resumen_linaje por linaje (solo fisica, ERR-96). Lo unico agregado es la telemetria propia del carro (d['carro']['v143'] y
['apr']), que se guarda aparte y NO puntua. El --humo lo verifica (9 FABRICA, s 14281, T 2000).
Antes de correr: sha de los origenes, carros en disco == construye_v143 (--verifica), chequeo estatico de cada carro
(revisa_carro.revisa_fuente), identidad corta del juez (FABRICA == monolito) e identidad corta de v14.3 (perillas en 0 == FABRICA,
N 9, s 14281, T 2000, fundador limpio). Si algo falla, NO corre.

BRAZOS (9 carros iguales):
  fab        FABRICA (v14.1: el carro de fabrica de ayer)          v142       V142 (= FABRICA + B-5 = el tronco v14.2 en la pista)
  v143       V143 (EL CANDIDATO)                                   sinfiltro  V143_SINFILTRO (lesion pieza 1)
  sintd      V143_SINTD (lesion pieza 2; el control que PUEDE GANAR)
  siempre    V143_SIEMPRE (lesion pieza 3: filtro sin condicion de meta -> no hay limpieza)
  invertido  V143_INVERTIDO (control de contenido)                 o1         O1 (techo escrito a mano; ANCLA de la pista)
SEMILLAS: practica 14281-14290 (solo --humo) · serie 14301-14320 · replica 14321-14340. El corredor se niega a usar otras.

    python experimentos/tronco_v14_3/corre_v143.py --humo [--brazos fab,v142,v143,siempre,sintd,o1] [--T 20000] [--desde 14281] [--n 1]
    python experimentos/tronco_v14_3/corre_v143.py --serie fab,v142,v143,sinfiltro,sintd,siempre,invertido,o1 --desde 14301 --n 20 --pool 6   (SOLO el coordinador)
    python experimentos/tronco_v14_3/corre_v143.py --serie v143,v142,sinfiltro,sintd,siempre,invertido --desde 14321 --n 20 --pool 6 --con <crudos de la serie>  (SOLO el coordinador)
Banderas desconocidas: ABORTA (ERR-115). ERR-54: el crudo se escribe ANTES de resumir. Al final imprime el VEREDICTO por la letra.
Vocabulario: "linaje", "cuerpo", "indice del cuerpo en el linaje"; prohibido "poblacion", "generacion", "evoluciona", "coopera",
"altruismo", "planifica".
"""
import argparse, hashlib, importlib.util, json, os, platform, statistics as st, sys, time

sys.stdout.reconfigure(encoding='utf-8', errors='replace')
AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
PISTA = os.path.join(RAIZ, 'experimentos', 'carrera_escuderias')
CARROS_V = os.path.join(AQUI, 'carros_v143')
sys.path[:0] = [AQUI, PISTA]
import pista as P
import juez as J
import revisa_carro as RC
import construye_v143 as CV

DATOS = os.path.join(AQUI, 'datos')
DATOS_HUMO = os.path.join(DATOS, 'humo')
SHAS = {os.path.join(PISTA, 'pista.py'): '9f47c65e438e0ff4', os.path.join(PISTA, 'juez.py'): '6a68f640a7832f12',
        os.path.join(PISTA, 'carros', 'FABRICA.py'): '2ebee3e99ea5a33a', os.path.join(PISTA, 'carros', 'O1.py'): '99436afa2715f028',
        os.path.join(PISTA, 'carros', 'APR.py'): '4402aa5142065c72', os.path.join(RAIZ, 'organismo', 'organismo_v142.py'): '17528d767fcebaf6'}
BRAZOS = {'fab': 'FABRICA', 'v142': 'V142', 'v143': 'V143', 'sinfiltro': 'V143_SINFILTRO', 'sintd': 'V143_SINTD',
          'siempre': 'V143_SIEMPRE', 'invertido': 'V143_INVERTIDO', 'o1': 'O1'}
DE_CARRERA = ('FABRICA', 'O1')
PRACTICA = range(14281, 14291); SERIE = range(14301, 14321); REPLICA = range(14321, 14341)
T_DEF = 100000; FL = 1
SERIE_BRAZOS = ('fab', 'v142', 'v143', 'sinfiltro', 'sintd', 'siempre', 'invertido', 'o1')
REPLICA_BRAZOS = ('v143', 'v142', 'sinfiltro', 'sintd', 'siempre', 'invertido')
GANA = 15            # >= 15/20 semillas (ENMIENDAS 2, 5, 6)
DIF_MOD = 0.10       # diferencia mediana minima de R0 real (pareado) para HAY ALGO MODESTO
ANCLA_FAB = (0.08, 0.20)   # V-ANCLA 1 (ENMIENDA 1 tras el humo, CANDIDATO A ERR): FABRICA con fundador limpio da 0.113-0.129 (5 series r2fab
                           # 9101-9140, 600 linajes; por semilla 0.098-0.151) y 0.145 en el humo; el rango [0.22, 0.45] escrito antes del
                           # humo era el de fundador NO limpio (sellada 5001-5020: 0.339). Mismo patron que ERR-116.

_MODS = {}


def h16(p): return hashlib.sha256(open(p, 'rb').read()).hexdigest()[:16]


def modulo(ident):
    """FABRICA y O1: carros/ de la carrera (pista.carga_carro). Los V14x: carros_v143/ de esta carpeta, cargados por ruta."""
    if ident not in _MODS:
        if ident in DE_CARRERA: _MODS[ident] = P.carga_carro(ident)
        else:
            ruta = os.path.join(CARROS_V, ident + '.py')
            if not os.path.exists(ruta): raise SystemExit(f"no existe {ruta} (correr construye_v143.py)")
            spec = importlib.util.spec_from_file_location(f"carro_{ident}", ruta)
            m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); _MODS[ident] = m
    return _MODS[ident]


def tarea(args):
    """== juez.tarea(seed, carros, T, pizarra=1, rep_acum=0, escala=1, mundo_n=None, fundador_limpio=1) + telemetria del carro aparte."""
    seed, ident, T = args
    t0 = time.time()
    carros = [(ident, modulo(ident))] * 9
    r = P.run(seed, carros, T=T, pizarra=1, rep_acum=0, escala=1, mundo_n=None, fundador_limpio=FL)
    L = [J.resumen_linaje(d, seed) for d in r['linajes']]
    sd = sum(x['descendientes'] for x in L); sm = sum(x['muertes'] for x in L)
    for x in L:
        tf, qf, nr = J.t_fund_reconstruido(x['telem']['vidas'], x['telem']['desc_por_vida'])
        x['t_fund_rec_ok'] = bool(tf[:200] == x['telem']['t_fund'] and qf == x['cola_final'] and nr == x['nac_reales'])
    tel = [dict(v143=d['carro'].get('v143'), apr=(d['carro'].get('apr') or {}).get('politica'),
                apr_quit=(d['carro'].get('apr') or {}).get('quit_q'), apr_anad=(d['carro'].get('apr') or {}).get('anad_q'),
                apr_opp=(d['carro'].get('apr') or {}).get('opp_q'), apr_g0=[(d['carro'].get('apr') or {}).get('mord_g0'),
                                                                        (d['carro'].get('apr') or {}).get('opp_g0')]) for d in r['linajes']]
    return dict(seed=seed, seg=round(time.time() - t0, 1), linajes=L, pista=r['pista'],
                R0_pista=round(sd / (sm + len(L)), 4), pizarra_log=r['pizarra_log'], tel=tel)


def med(xs):
    xs = [x for x in xs if x is not None]
    return round(float(st.median(xs)), 4) if xs else None


def resume(R, brazo, log):
    """ENMIENDA 5 (decide), ENMIENDA 6 (persistencia, co-principal), ENMIENDA 3 (la letra del primer cruce, se reporta)."""
    ns = len(R); todos = [l for c in R for l in c['linajes']]
    sem_e5 = sum(1 for c in R if sum(l['cruza_real'] for l in c['linajes']) * 2 > len(c['linajes']))
    sem_e6 = sum(1 for c in R if sum(l['persiste'] for l in c['linajes']) * 2 > len(c['linajes']))
    cm = J.criterio_mono(todos)
    cz = {k: sum(l['causas'][k] for l in todos) for k in ('hambre', 'sed', 'veneno', 'sal')}
    dg = [l['diag'] for l in todos if l.get('diag')]
    v3 = [t['v143'] for c in R for t in c['tel'] if t.get('v143')]
    mv = [l.get('muertes_vol') for l in todos]; mu = sum(l['muertes'] for l in todos)
    out = dict(brazo=brazo, carro=BRAZOS[brazo], semillas=ns,
               R0_real_med=med([l['R0_real'] for l in todos]), R0_real_eval_med=cm['mediana_R0_real_eval'], R0_prereg_med=med([l['R0'] for l in todos]),
               linajes_cruzan_real=sum(l['cruza_real'] for l in todos), linajes=len(todos),
               sem_cruza_e5=sem_e5, gana_e5=bool(sem_e5 >= GANA * ns / 20), sem_estabiliza_e6=sem_e6, estabiliza_e6=bool(sem_e6 >= GANA * ns / 20),
               persisten=sum(l['persiste'] for l in todos), enm3=dict(cruza=cm['cruza'], mediana_R0_eval=cm['mediana_R0_eval'],
                                                                        condiciones=cm['condiciones']),
               casi_inmortales=sum(l['casi_inmortal'] for l in todos), vida_med=med([l['vida_med'] for l in todos]),
               muertes_med=med([l['muertes'] for l in todos]), fundadores_med=med([l['fundadores'] for l in todos]),
               causas=cz, frac_BD_causa=(round((cz['veneno'] + cz['sal']) / max(1, sum(cz.values())), 4)),
               frac_vol=(round(sum(mv) / mu, 4) if mu and all(v is not None for v in mv) else None),
               frac_sin_bueno_mundo_med=med([c['pista']['frac_sin_bueno_mundo'] for c in R]),
               mord_BD_med=med([l['mord']['B'] + l['mord']['D'] for l in todos]), mord_AC_med=med([l['mord']['A'] + l['mord']['C'] for l in todos]),
               limpiezas_fisicas_por_cuerpo_med=med([x['limpiezas_por_cuerpo'] for x in dg]),
               coherente=f"{sum(l['coherente'] for l in todos)}/{len(todos)}", t_fund_rec=f"{sum(l['t_fund_rec_ok'] for l in todos)}/{len(todos)}",
               seg_med=med([c['seg'] for c in R]))
    if v3:
        s = lambda k: sum(x[k] for x in v3)
        out['v143'] = dict(frac_pasos_con_meta=round(s('pasos_meta') / max(1, s('pasos')), 4) if s('pasos') else None,
                           vetos=s('vetos'), mord_sin_meta=s('mord_sin_meta'), limpia_propia=s('limpia_propia'), todo_obst=s('todo_obst'), des_splits=s('des_splits'))
    log(f"\n== {brazo} ({BRAZOS[brazo]} x9) · {ns} semillas {R[0]['seed']}-{R[-1]['seed']} · T {R[0]['pista']['T']} · fundador limpio {R[0]['pista']['fundador_limpio']}")
    log(f"  R0 REAL (nacimientos reales) mediana {out['R0_real_med']} (evaluables {out['R0_real_eval_med']}) · R0 preregistrado {out['R0_prereg_med']} · "
        f"vida mediana {out['vida_med']} · muertes {out['muertes_med']} · fundadores {out['fundadores_med']} · casi inmortales {out['casi_inmortales']}/{out['linajes']}")
    log(f"  ENMIENDA 5 (decide): linajes que cruzan con R0 real {out['linajes_cruzan_real']}/{out['linajes']} · semillas con mayoria {sem_e5}/{ns} -> "
        f"{'GANA' if out['gana_e5'] else 'no gana'} · ENMIENDA 6: persisten {out['persisten']}/{out['linajes']} · semillas {sem_e6}/{ns} -> "
        f"{'ESTABILIZA' if out['estabiliza_e6'] else 'no estabiliza'} (muertes voluntarias fisicas {out['frac_vol']}) · ENMIENDA 3 (ayer): "
        f"{'CRUZA' if cm['cruza'] else 'no cruza'} (mediana R0 evaluables {cm['mediana_R0_eval']})")
    tot = max(1, sum(cz.values()))
    log(f"  causas hambre/sed/veneno/sal {cz['hambre']}/{cz['sed']}/{cz['veneno']}/{cz['sal']} (veneno+sal {out['frac_BD_causa']:.0%}) · "
        f"pasos sin NADA bueno en el mundo {out['frac_sin_bueno_mundo_med']} · mordidas B+D {out['mord_BD_med']} / A+C {out['mord_AC_med']} por linaje · "
        f"limpiezas fisicas por cuerpo {out['limpiezas_fisicas_por_cuerpo_med']}")
    if v3: log(f"  telemetria del carro (NO puntua): {out['v143']}")
    log(f"  contabilidad coherente {out['coherente']} · t_fund reconstruible {out['t_fund_rec']} · s por corrida (mediana) {out['seg_med']}")
    return out


def pareado(Ra, Rb):
    ma = {c['seed']: st.median([l['R0_real'] for l in c['linajes']]) for c in Ra}
    mb = {c['seed']: st.median([l['R0_real'] for l in c['linajes']]) for c in Rb}
    com = sorted(set(ma) & set(mb)); d = [ma[k] - mb[k] for k in com]
    return dict(semillas=len(com), gana=sum(1 for x in d if x > 0), dif_med=(round(float(st.median(d)), 4) if d else None))


PARES = (('v143', 'v142'), ('v143', 'fab'), ('v142', 'fab'), ('v143', 'sinfiltro'), ('v143', 'sintd'), ('sintd', 'v143'),
         ('v143', 'siempre'), ('v143', 'invertido'), ('v142', 'invertido'), ('o1', 'v143'))


# ---------------------------------------------------------------- PREDICCIONES FIRMADAS (PREREGISTRO_v143.md sec. 6) -- antes del humo
def _g(res, b, k): return res[b][k] if b in res else None
def _p(par, a, b, n=GANA, dmin=0.0):
    x = par.get((a, b)); return None if x is None else bool(x['gana'] >= n * x['semillas'] / 20 and x['dif_med'] is not None and x['dif_med'] > dmin)
PRED = [
    ("V-ANCLA-1 FABRICA: mediana R0 real en [0.08, 0.20] (ENMIENDA 1, candidato a ERR; antes [0.22, 0.45])", lambda r, p: None if 'fab' not in r else ANCLA_FAB[0] <= r['fab']['R0_real_med'] <= ANCLA_FAB[1]),
    ("V-ANCLA-2 O1 GANA por la ENMIENDA 5 (ayer, r2o1mono 9101-9120: 20/20)", lambda r, p: _g(r, 'o1', 'gana_e5')),
    ("P1 V142 ~ FABRICA: |dif mediana pareada de R0 real| <= 0.05 (p 0.65)", lambda r, p: None if ('v142', 'fab') not in p else abs(p[('v142', 'fab')]['dif_med']) <= 0.05),
    ("P2 V143 > V142 en >= 18/20 semillas con dif mediana >= 0.10 (p 0.75)", lambda r, p: _p(p, 'v143', 'v142', n=18, dmin=0.10 - 1e-12)),
    ("P3 V143: mediana R0 real en [0.45, 0.85] (p 0.55)", lambda r, p: None if 'v143' not in r else 0.45 <= r['v143']['R0_real_med'] <= 0.85),
    ("P4 V143 NO gana por la ENMIENDA 5 (p 0.80 de que NO cruza)", lambda r, p: None if 'v143' not in r else not r['v143']['gana_e5']),
    ("P5 SIEMPRE (sin limpieza) < V143 en >= 15/20 y su mundo sin nada bueno >= 0.30 de los pasos (p 0.70)",
     lambda r, p: None if 'siempre' not in r else bool(_p(p, 'v143', 'siempre')) and r['siempre']['frac_sin_bueno_mundo_med'] >= 0.30),
    ("P6 SINFILTRO: mediana R0 real en [0.30, 0.47] y V143 > SINFILTRO en >= 15/20 (p 0.70)",
     lambda r, p: None if 'sinfiltro' not in r else 0.30 <= r['sinfiltro']['R0_real_med'] <= 0.47 and bool(_p(p, 'v143', 'sinfiltro'))),
    ("P7 SINTD ~ V143: |dif mediana pareada| <= 0.05 (p 0.50; el control que puede ganar)",
     lambda r, p: None if ('v143', 'sintd') not in p else abs(p[('v143', 'sintd')]['dif_med']) <= 0.05),
    ("P8 INVERTIDO < V142 en >= 15/20 (p 0.80)", lambda r, p: _p(p, 'v142', 'invertido')),
    ("P9 V143 vida mediana >= 3 x la de V142 (p 0.70)", lambda r, p: None if 'v143' not in r or 'v142' not in r else r['v143']['vida_med'] >= 3 * r['v142']['vida_med']),
    ("P10 V143: veneno+sal <= 0.50 de las causas de muerte (V142 ~1.0) (p 0.70)", lambda r, p: None if 'v143' not in r else r['v143']['frac_BD_causa'] <= 0.50),
    ("P11 V143: pasos sin nada bueno en el mundo en [0.01, 0.30] (limpia algo, no del todo) (p 0.65)",
     lambda r, p: None if 'v143' not in r else 0.01 <= r['v143']['frac_sin_bueno_mundo_med'] <= 0.30),
]


def veredicto(res_s, par_s, res_r, par_r, log):
    """PREREGISTRO_v143.md sec. 7, por la letra. Necesita serie Y replica; con una sola, es PARCIAL."""
    def anclas(res):
        a1 = ANCLA_FAB[0] <= res['fab']['R0_real_med'] <= ANCLA_FAB[1] if 'fab' in res else None
        a2 = res['o1']['gana_e5'] if 'o1' in res else None
        return a1, a2
    def lee(res, par):
        if not all(b in res for b in ('v143', 'v142', 'siempre', 'invertido')): return None
        f = (res['v143']['gana_e5'] and res['v143']['estabiliza_e6'] and not res['siempre']['gana_e5'] and not res['invertido']['gana_e5']
             and bool(_p(par, 'v143', 'v142')))
        m = bool(_p(par, 'v143', 'v142', dmin=DIF_MOD - 1e-12)) and bool(_p(par, 'v143', 'siempre'))
        return dict(funciona=bool(f), modesto=bool(m))
    a1, a2 = anclas(res_s)
    log("\n================ VEREDICTO POR LA LETRA (PREREGISTRO_v143.md sec. 7)")
    log(f"  anclas de la serie: V-ANCLA-1 FABRICA en {ANCLA_FAB}: {a1} · V-ANCLA-2 O1 gana: {a2}")
    if a1 is False or a2 is False:
        log("  VEREDICTO: NO SE LEE (un ancla de la pista no se reprodujo; nada se declara; ERR-116 es el precedente)"); return 'NO SE LEE'
    ls = lee(res_s, par_s); lr = lee(res_r, par_r) if res_r is not None else None
    log(f"  serie: {ls} · replica: {lr}")
    if ls is None: log("  VEREDICTO: INCOMPLETO (faltan brazos del criterio en la serie)"); return 'INCOMPLETO'
    if lr is None:
        v = 'FUNCIONA' if ls['funciona'] else ('HAY ALGO MODESTO' if ls['modesto'] else 'NO')
        log(f"  VEREDICTO PARCIAL (sin replica; NO se declara): la serie sola diria {v}"); return 'PARCIAL: ' + v
    if ls['funciona'] and lr['funciona']: v = 'FUNCIONA'
    elif ls['modesto'] and lr['modesto'] or (ls['funciona'] and lr['modesto']) or (ls['modesto'] and lr['funciona']): v = 'HAY ALGO MODESTO'
    else: v = 'NO'
    log(f"  VEREDICTO: {v}")
    return v


def verifica_todo(log, con_entrada):
    ok = True
    for ruta, sha in SHAS.items():
        s = h16(ruta); ok &= s == sha
        log(f"  sha {os.path.relpath(ruta, RAIZ)} {s} {'OK' if s == sha else '!= ' + sha + ' FALLA'}")
    outs = CV.todas()
    for n, b in outs.items():
        ruta = os.path.join(CARROS_V, n + '.py'); igual = os.path.exists(ruta) and open(ruta, 'rb').read() == b
        v = RC.revisa_fuente(b.decode('utf-8'), n) if igual else ['distinto de construye_v143']
        ok &= igual and not v
        log(f"  carro {n} sha {CV.h16b(b)} == construye: {igual} · chequeo estatico: {'PASA' if not v else v[:2]}")
    for c in DE_CARRERA:
        v = RC.revisa(c); ok &= not v; log(f"  carro {c} (carrera) chequeo estatico: {'PASA' if not v else v[:2]}")
    ide = J.identidad_corta(); ok &= ide['ok']
    log(f"  IDENTIDAD CORTA del juez (FABRICA == organismo_f9c REL, s 1, T 5000): {'OK' if ide['ok'] else 'FALLA ' + str(ide['dif'][:5])}")
    N = lambda x: json.loads(json.dumps(x, default=str))
    m = modulo('V143'); guarda = (m.DESAMB, m.FILTRO, m.OPCION)
    try:
        m.DESAMB = 0; m.FILTRO = 0; m.OPCION = 0
        a = P.run(14281, [('C', modulo('FABRICA'))] * 9, T=2000, fundador_limpio=1); b = P.run(14281, [('C', m)] * 9, T=2000, fundador_limpio=1)
    finally:
        m.DESAMB, m.FILTRO, m.OPCION = guarda
    i2 = N(a) == N(b); ok &= i2
    log(f"  IDENTIDAD CORTA v14.3: perillas en 0 == FABRICA (N 9, s 14281, T 2000, fundador limpio): {'OK' if i2 else 'FALLA'}")
    if con_entrada:
        x = tarea((14281, 'FABRICA', 2000)); y = J.tarea((14281, ['FABRICA'] * 9, 2000, 1, 0, 1, None, 1))
        e = N(x['linajes']) == N(y['linajes']) and N(x['pista']) == N(y['pista']) and x['R0_pista'] == y['R0_pista']
        ok &= e; log(f"  ENTRADA campo a campo (regla 14): corre_v143.tarea == juez.tarea (9 FABRICA, s 14281, T 2000, fundador limpio): {'OK' if e else 'FALLA'}")
    return ok


def valida(humo, desde, n, T, brazos):
    """ERR-115 y regla de semillas: devuelve un texto de error o None."""
    for b in brazos:
        if b not in BRAZOS: return f"brazo desconocido {b!r} (validos {list(BRAZOS)})"
    sem = list(range(desde, desde + n))
    if n < 1: return "--n >= 1"
    if humo:
        if not all(x in PRACTICA for x in sem): return "--humo: solo semillas de practica 14281-14290"
        if T > 30000: return "--humo: T <= 30000"
        if n * len(brazos) > 6: return "--humo: maximo 6 corridas por proceso"
    else:
        if not (all(x in SERIE for x in sem) or all(x in REPLICA for x in sem)): return "serie: solo 14301-14320 (serie) o 14321-14340 (replica)"
        if T != T_DEF: return "serie: T = 100000 (preregistrado)"
    return None


def main(argv=None):
    ap = argparse.ArgumentParser(allow_abbrev=False)
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument('--humo', action='store_true')
    g.add_argument('--serie', default=None)
    ap.add_argument('--brazos', default='fab,v142,v143,siempre,sintd,o1')
    ap.add_argument('--desde', type=int, default=None)
    ap.add_argument('--n', type=int, default=None)
    ap.add_argument('--T', type=int, default=None)
    ap.add_argument('--con', default=None)
    ap.add_argument('--pool', type=int, default=0)
    a = ap.parse_args(argv)   # argparse ABORTA ante cualquier bandera desconocida (ERR-115): nunca parse_known_args
    brazos = [s.strip() for s in (a.brazos if a.humo else a.serie).split(',') if s.strip()]
    if a.humo:
        desde = a.desde or 14281; n = a.n or 1; T = a.T or 20000; pool = 0
        if a.pool: raise SystemExit("--humo: sin Pool (un proceso)")
    else:
        desde = a.desde or 14301; n = a.n or 20; T = a.T or T_DEF; pool = a.pool
    e = valida(a.humo, desde, n, T, brazos)
    if e: raise SystemExit(e)
    semillas = list(range(desde, desde + n))
    dest = DATOS_HUMO if a.humo else DATOS
    os.makedirs(dest, exist_ok=True)
    sel = time.strftime('%Y%m%d_%H%M%S')
    pre = f"v143_{'humo_' if a.humo else ''}{'-'.join(brazos)}_s{semillas[0]}-{semillas[-1]}_T{T}_{sel}"
    LOGF = open(os.path.join(dest, pre + '.log'), 'w', encoding='utf-8')

    def log(s=''):
        print(s, flush=True); LOGF.write(s + '\n'); LOGF.flush()

    t0 = time.time()
    log(f"CORRE_V143 · {pre} · python {platform.python_version()} · pool {pool or 'NO (un proceso)'} · corre_v143.py {h16(os.path.abspath(__file__))}")
    log(f"  brazos {brazos} · semillas {semillas[0]}-{semillas[-1]} · T {T} · fundador limpio {FL} · pista escalada (L 360, 36 objetos)")
    if not verifica_todo(log, con_entrada=a.humo): log("  ALGO FALLA -> no se corre."); return 1
    res = {}; RR = {}
    for b in brazos:
        tareas = [(sd, BRAZOS[b], T) for sd in semillas]; R = []
        if pool and pool > 1:
            from multiprocessing import Pool
            with Pool(pool) as PL:
                for x in PL.imap_unordered(tarea, tareas):
                    R.append(x); log(f"  [{time.time()-t0:7.1f}s] {b} semilla {x['seed']} ({x['seg']}s) R0 pista {x['R0_pista']}")
        else:
            for tk in tareas:
                x = tarea(tk); R.append(x)
                log(f"  [{time.time()-t0:7.1f}s] {b} semilla {x['seed']} ({x['seg']}s) R0 pista {x['R0_pista']} · R0 real por linaje {[l['R0_real'] for l in x['linajes']]}")
        R.sort(key=lambda x: x['seed'])
        esc = sum(l['escrituras'] for c in R for l in c['linajes'])
        for x in R: x.pop('pizarra_log')
        crudo = os.path.join(dest, f"{pre}_{b}.json")
        with open(crudo, 'w', encoding='utf-8') as fh:
            json.dump(dict(meta=dict(brazo=b, carro=BRAZOS[b], semillas=semillas, T=T, fundador_limpio=FL, humo=a.humo,
                                     sha_carro=h16(os.path.join(PISTA, 'carros', BRAZOS[b] + '.py') if BRAZOS[b] in DE_CARRERA else os.path.join(CARROS_V, BRAZOS[b] + '.py')),
                                     sha_pista=h16(os.path.join(PISTA, 'pista.py')), sha_juez=h16(os.path.join(PISTA, 'juez.py'))),
                           corridas=R), fh, ensure_ascii=False)   # ERR-54: crudo ANTES de resumir
        log(f"  CRUDO {crudo} (sha {h16(crudo)}) · escrituras en la pizarra {esc} (nadie escribe: esperado 0)")
        res[b] = resume(R, b, log); RR[b] = R
    otra = None
    if a.con:
        otra = {}
        for ruta in a.con.split(','):
            with open(ruta.strip(), encoding='utf-8') as fh: d = json.load(fh)
            b = d['meta']['brazo']
            if d['meta']['T'] != T or d['meta'].get('humo') != a.humo or d['meta'].get('fundador_limpio') != FL: raise SystemExit(f"--con {ruta}: T, humo o fundador limpio distintos")
            otra[b] = d['corridas']; log(f"  (--con) brazo {b} semillas {d['meta']['semillas'][0]}-{d['meta']['semillas'][-1]} desde {ruta} (sha {h16(ruta.strip())})")
    par = {k: pareado(RR[k[0]], RR[k[1]]) for k in PARES if k[0] in RR and k[1] in RR}
    log("\nPAREADOS (por semilla: mediana del R0 real de los 9 linajes; gana = semillas en que el primero supera al segundo)")
    for k, v in par.items(): log(f"  {k[0]} vs {k[1]}: gana {v['gana']}/{v['semillas']} · diferencia mediana {v['dif_med']}")
    log("\nPREDICCIONES FIRMADAS (PREREGISTRO_v143.md sec. 6) y lo medido" + (" -- HUMO: T corto y semillas de practica, NO cuentan" if a.humo else ""))
    pred = []
    for txt, f in PRED:
        v = f(res, par); pred.append(dict(texto=txt, se_cumple=v))
        log(f"  {txt} -> {'SE CUMPLE' if v else ('sin el brazo' if v is None else 'NO se cumple')}")
    res_o = par_o = None
    if otra:
        res_o = {b: resume(R, b, log) for b, R in otra.items()}
        par_o = {k: pareado(otra[k[0]], otra[k[1]]) for k in PARES if k[0] in otra and k[1] in otra}
    es_serie = all(x in SERIE for x in semillas)
    if a.humo: v = veredicto(res, par, None, None, log); v = 'HUMO (no cuenta): ' + v
    elif es_serie: v = veredicto(res, par, res_o, par_o, log)
    else: v = veredicto(res_o or {}, par_o or {}, res, par, log) if res_o else veredicto(res, par, None, None, log)
    rj = os.path.join(dest, pre + '_resumen.json')
    with open(rj, 'w', encoding='utf-8') as fh:
        json.dump(dict(brazos=res, pareados={f"{k[0]}_vs_{k[1]}": x for k, x in par.items()}, predicciones=pred, semillas=semillas, T=T,
                       humo=a.humo, veredicto=v), fh, ensure_ascii=False, indent=1)
    log(f"\n  RESUMEN {rj} (sha {h16(rj)})\nTerminado en {time.time()-t0:.1f}s")
    log(f"VEREDICTO: {v}")
    return 0


if __name__ == '__main__':
    sys.exit(main())
