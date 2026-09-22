"""corre_aprende.py — corredor del camino A (aprende_barrer): 9 carros iguales en la pista escalada de la carrera.

MISION: llegar a la AGI por este camino. Pregunta: ¿puede FABRICA + una OPCION APRENDIDA de morder lo malo conocido
(carros/APR.py) descubrir la limpieza y pasarla al cuerpo siguiente del linaje, hasta cruzar H-1 sin que nadie le
escriba la regla? Preregistro: PREREGISTRO_aprende.md (letra, controles, predicciones firmadas, lectura permitida).

ENTRADA (regla 14, campo a campo): la MISMA de juez.tarea de la serie sellada: pista.run(seed, carros, T, pizarra=1,
rep_acum=0, escala=1, mundo_n=None) y juez.resumen_linaje por linaje (solo fisica, ERR-96). Lo unico agregado es la
telemetria propia de APR (d['carro']['apr']), que se guarda APARTE y no puntua. El --humo lo verifica: esta tarea ==
juez.tarea en linajes y pista (9 FABRICA, s 8001, T 2000).
Antes de correr: chequeo estatico de cada carro (revisa_carro), identidad corta del juez (FABRICA == monolito) e
identidad corta de APR (OPCION 0 == FABRICA, N 9, s 8001, T 2000). Si algo falla, NO corre.

SERIES (9 carros iguales, pista escalada L 360 / 36 objetos, T = 100000):
  apr     9 APR                 (el candidato)
  fab     9 FABRICA             (piso)
  o1      9 O1                  (techo diseñado)
  azar    9 APR_AZAR            (placebo de CUANDO: P_AZAR = tasa de APR en el ultimo cuarto de T, fijada con construye_apr.py --p_azar)
  sinher  9 APR_SIN_HERENCIA    (el valor de la opcion no pasa al cuerpo siguiente)
Semillas: practica 8001-8040 (solo --humo) · serie 8101-8120 · replica 8121-8140. El corredor se niega a usar otras.

    python experimentos/aprende_barrer/corre_aprende.py --humo [--serie apr] [--T 30000] [--desde 8001] [--n 1]   (UN proceso)
    python experimentos/aprende_barrer/corre_aprende.py --serie apr,fab,o1,sinher --desde 8101 --n 20 --pool 6         (SOLO el coordinador)
    python experimentos/aprende_barrer/corre_aprende.py --serie azar --desde 8101 --n 20 --pool 6                      (despues de fijar P_AZAR)
ERR-54: el crudo se escribe ANTES de resumir. Vocabulario: "linaje", "cuerpo"; prohibido "poblacion", "generacion"
(se dice "indice del cuerpo en el linaje"), "evoluciona", "coopera", "altruismo".
"""
import argparse, json, os, platform, statistics as st, sys, time, types

sys.stdout.reconfigure(encoding='utf-8', errors='replace')
AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
PISTA = os.path.join(RAIZ, 'experimentos', 'carrera_escuderias')
sys.path[:0] = [AQUI, PISTA]
import pista as P
import juez as J
import revisa_carro as RC

DATOS = os.path.join(AQUI, 'datos')
SERIES = {'apr': 'APR', 'fab': 'FABRICA', 'o1': 'O1', 'azar': 'APR_AZAR', 'sinher': 'APR_SIN_HERENCIA'}
PRACTICA = range(8001, 8041); SERIE = range(8101, 8121); REPLICA = range(8121, 8141)
T_DEF = 100000
# PREDICCIONES FIRMADAS (PREREGISTRO_aprende.md sec. 5; escritas DESPUES de los humos de practica 8001-8002 y ANTES de la
# serie 8101-8120). Cada una: (texto, funcion(res, par) -> True / False / None si falta la serie). res[serie] = resume(...);
# par[(a, b)] = semillas en que la mediana por semilla del R0 de los 9 linajes de a supera a la de b, y la mediana de a - b.
def _r0(res, s): return res[s]['R0_med_todos'] if s in res else None
def _cm(res, s): return res[s]['criterio_enm3']['cruza'] if s in res else None
def _ap(res, k): return res['apr']['apr'][k] if 'apr' in res and 'apr' in res['apr'] else None
def _gana(par, a, b, n=15, dmin=0.03):
    x = par.get((a, b)); return None if x is None else (x['gana'] >= n and x['dif_med'] >= dmin)
def _descubre(res):
    q = _ap(res, 'anadidas_por_cuarto'); pol = _ap(res, 'politica_mediana')
    if q is None: return None
    return (q[3] or 0) >= 0.02 and (pol['g0=1 post=0.8'] - pol['g0=0 post=0.8']) >= 0.5
PRED = [
    ("P1 APR NO cruza por la ENMIENDA 3 (p 0.97)", lambda r, p: None if _cm(r, 'apr') is None else not _cm(r, 'apr')),
    ("P2 APR: mediana del R0 de los linajes-semilla en 0.32-0.45", lambda r, p: None if _r0(r, 'apr') is None else 0.32 <= _r0(r, 'apr') <= 0.45),
    ("P3 FABRICA NO cruza y su mediana cae en 0.28-0.40 (sellada 5001-5020: 0.34)",
     lambda r, p: None if _r0(r, 'fab') is None else (not _cm(r, 'fab')) and 0.28 <= _r0(r, 'fab') <= 0.40),
    ("P4 O1 CRUZA (p 0.85; sellada 5001-5020: 1.565)", lambda r, p: _cm(r, 'o1')),
    ("P5 APR NO DESCUBRE la limpieza (p 0.93): anadidas en el ultimo cuarto < 0.02 por oportunidad O correccion(sin bueno) - "
     "correccion(con bueno) < 0.5 logit", lambda r, p: None if _descubre(r) is None else not _descubre(r)),
    ("P6 APR aprende a CONTENERSE (p 0.85): quitadas en el ultimo cuarto >= 0.03 por oportunidad",
     lambda r, p: None if _ap(r, 'quitadas_por_cuarto') is None else (_ap(r, 'quitadas_por_cuarto')[3] or 0) >= 0.03),
    ("P7 APR > FABRICA en >= 15/20 semillas con diferencia mediana >= 0.03 (p 0.55)", lambda r, p: _gana(p, 'apr', 'fab')),
    ("P8 APR > APR_SIN_HERENCIA en >= 15/20 semillas con diferencia mediana >= 0.03 (p 0.45)", lambda r, p: _gana(p, 'apr', 'sinher')),
    ("P9 APR > APR_AZAR en >= 15/20 semillas con diferencia mediana >= 0.03 (p 0.70)", lambda r, p: _gana(p, 'apr', 'azar')),
    ("P10 APR_SIN_HERENCIA y APR_AZAR NO cruzan (p 0.97)",
     lambda r, p: None if (_cm(r, 'sinher') is None and _cm(r, 'azar') is None) else not any(_cm(r, s) for s in ('sinher', 'azar') if s in r)),
    ("P11 APR: fraccion de pasos sin ningun bueno en el mundo 0.003-0.03 (el mundo no se ensucia; O1 ~0.05)",
     lambda r, p: None if 'apr' not in r else 0.003 <= r['apr']['frac_sin_bueno_mundo_med'] <= 0.03),
]


def pareado(Ra, Rb):
    ma = {c['seed']: st.median([l['R0'] for l in c['linajes']]) for c in Ra}
    mb = {c['seed']: st.median([l['R0'] for l in c['linajes']]) for c in Rb}
    com = sorted(set(ma) & set(mb))
    d = [ma[k] - mb[k] for k in com]
    return dict(semillas=len(com), gana=sum(1 for x in d if x > 0), dif_med=(round(float(st.median(d)), 4) if d else None),
                por_semilla={k: round(ma[k] - mb[k], 4) for k in com})


def tarea(args):
    """== juez.tarea (misma llamada a la pista, mismo resumen fisico) + la telemetria APR aparte."""
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


def med(xs):
    xs = [x for x in xs if x is not None]
    return round(float(st.median(xs)), 4) if xs else None


def suma(listas):
    if not listas: return []
    if isinstance(listas[0][0], list): return [suma([l[i] for l in listas]) for i in range(len(listas[0]))]
    return [sum(l[i] for l in listas) for i in range(len(listas[0]))]


def tasa(m, o):
    if m is None or o is None: return None
    if isinstance(m, list) and m and isinstance(m[0], list): return [tasa(a, b) for a, b in zip(m, o)]
    return [round(a / b, 4) if b else None for a, b in zip(m, o)]


def resume(R, serie, log):
    todos = [l for c in R for l in c['linajes']]
    cm = J.criterio_mono(todos)
    r0 = med([l['R0'] for l in todos])
    fsb = [c['pista']['frac_sin_bueno_mundo'] for c in R]
    dg = [l['diag'] for l in todos if l.get('diag')]
    cz = {k: sum(l['causas'][k] for l in todos) for k in ('hambre', 'sed', 'veneno', 'sal')}
    out = dict(serie=serie, criterio_enm3=cm, R0_med_todos=r0, R0_pista_med=med([c['R0_pista'] for c in R]),
               vida_med=med([l['vida_med'] for l in todos]), causas=cz, frac_sin_bueno_mundo_med=med(fsb),
               limpiezas_fisicas_por_cuerpo_med=med([x['limpiezas_por_cuerpo'] for x in dg]),
               limpiezas_fisicas_por_linaje_med=med([x['limpiezas'] for x in dg]),
               mord_BD_por_linaje_med=med([l['mord']['B'] + l['mord']['D'] for l in todos]),
               coherente=f"{sum(l['coherente'] for l in todos)}/{len(todos)}",
               t_fund_rec=f"{sum(l['t_fund_rec_ok'] for l in todos)}/{len(todos)}")
    log(f"\n== SERIE {serie} ({SERIES[serie]} x9) · {len(R)} semillas {R[0]['seed']}-{R[-1]['seed']} · T {R[0]['pista']['T']}")
    log(f"  R0 por linaje-semilla: mediana {r0} · R0 de la pista (mediana por semilla) {out['R0_pista_med']} · vida mediana {out['vida_med']}")
    log(f"  ENMIENDA 3: (i) mediana R0 evaluables {cm['mediana_R0_eval']} · (ii) sin fundadores tras 10000 {cm['frac_eval_sin_fund']} · "
        f"(iii) evaluables {cm['evaluables']}/{cm['n']} · casi inmortales {cm['casi_inmortales']} · linajes que cruzan {cm['cruzan_linajes']} "
        f"-> {'CRUZA' if cm['cruza'] else 'NO CRUZA'}")
    tot = max(1, sum(cz.values()))
    log(f"  causas de muerte hambre/sed/veneno/sal {cz['hambre']}/{cz['sed']}/{cz['veneno']}/{cz['sal']} "
        f"({cz['hambre']/tot:.0%}/{cz['sed']/tot:.0%}/{cz['veneno']/tot:.0%}/{cz['sal']/tot:.0%})")
    log(f"  fraccion de pasos SIN ningun objeto bueno en el mundo: mediana {out['frac_sin_bueno_mundo_med']} (por semilla {fsb})")
    log(f"  limpieza FISICA (juez: B/D a sabiendas con el golpe en la necesidad mas llena): por cuerpo {out['limpiezas_fisicas_por_cuerpo_med']} · "
        f"por linaje-semilla {out['limpiezas_fisicas_por_linaje_med']} · mordidas B+D por linaje-semilla {out['mord_BD_por_linaje_med']}")
    log(f"  contabilidad coherente {out['coherente']} · t_fund reconstruible {out['t_fund_rec']}")
    ap = [a for c in R for a in c['apr'] if a]
    if ap:
        k = lambda n: (suma([a[n] for a in ap]) if all(n in a for a in ap) else None)   # None: crudo sin ese contador
        oq, mq = k('opp_q'), k('mord_q')
        o = dict(oportunidades=sum(oq), mordidas=sum(mq), tasa_global=round(sum(mq) / max(1, sum(oq)), 4),
                 tasa_por_cuarto=tasa(mq, oq), tasa_ultimo_cuarto=(round(mq[3] / oq[3], 4) if oq[3] else None),
                 tasa_por_edad=tasa(k('mord_edad'), k('opp_edad')), bin_edad=ap[0]['bin_edad'],
                 tasa_por_indice_cuerpo=tasa(k('mord_gen'), k('opp_gen')), bin_gen=ap[0]['bin_gen'],
                 opp_por_indice_cuerpo=k('opp_gen'),
                 tasa_sin_bueno_vs_con=dict(con_bueno=tasa(k('mord_g0'), k('opp_g0'))[0], sin_bueno=tasa(k('mord_g0'), k('opp_g0'))[1],
                                            opp=k('opp_g0')),
                 tasa_por_post=dict(con_bueno=tasa(k('mord_post'), k('opp_post'))[0], sin_bueno=tasa(k('mord_post'), k('opp_post'))[1],
                                    bin_post=ap[0]['bin_post'], opp=k('opp_post')),
                 anadidas_por_cuarto=tasa(k('anad_q'), oq), quitadas_por_cuarto=tasa(k('quit_q'), oq),
                 anadidas_con_vs_sin_bueno=tasa(k('anad_g0'), k('opp_g0')), quitadas_con_vs_sin_bueno=tasa(k('quit_g0'), k('opp_g0')),
                 anadidas_por_edad=tasa(k('anad_edad'), k('opp_edad')), anadidas_por_indice_cuerpo=tasa(k('anad_gen'), k('opp_gen')),
                 quitadas_por_edad=tasa(k('quit_edad'), k('opp_edad')), quitadas_por_indice_cuerpo=tasa(k('quit_gen'), k('opp_gen')),
                 fabrica_habria_mordido=round(sum(a['fab_mord'] for a in ap) / max(1, sum(oq)), 4),
                 acuerdo_mordidas=sum(a['ambas'] for a in ap),
                 p_media=round(sum(a['suma_p'] for a in ap) / max(1, sum(oq)), 4),
                 td_abs_medio=round(sum(a['td_abs'] for a in ap) / max(1, sum(a['td_n'] for a in ap)), 4),
                 w_mediana=[[med([a['w'][i][j] for a in ap]) for j in range(len(ap[0]['w'][0]))] for i in range(2)],
                 politica_mediana={g: med([a['politica'][g] for a in ap]) for g in ap[0]['politica']})
        out['apr'] = o
        log(f"  OPCION (telemetria del carro, no puntua): oportunidades {o['oportunidades']} · mordidas {o['mordidas']} · tasa {o['tasa_global']} "
            f"· por cuarto de T {o['tasa_por_cuarto']} · ULTIMO CUARTO {o['tasa_ultimo_cuarto']} (-> P_AZAR de APR_AZAR si serie apr)")
        log(f"    tasa por EDAD del cuerpo (cortes {o['bin_edad']}): {o['tasa_por_edad']}")
        log(f"    tasa por INDICE DEL CUERPO en el linaje (cortes {o['bin_gen']}): {o['tasa_por_indice_cuerpo']} (oportunidades {o['opp_por_indice_cuerpo']})")
        log(f"    CUANDO: tasa con algun bueno en el mundo {o['tasa_sin_bueno_vs_con']['con_bueno']} vs SIN ningun bueno {o['tasa_sin_bueno_vs_con']['sin_bueno']} "
            f"(oportunidades {o['tasa_sin_bueno_vs_con']['opp']})")
        log(f"    por min(E,Ag) predicho tras morder (cortes {o['tasa_por_post']['bin_post']}): con bueno {o['tasa_por_post']['con_bueno']} · "
            f"sin bueno {o['tasa_por_post']['sin_bueno']}")
        log(f"    DESVIO respecto de la boca de FABRICA (por oportunidad): ANADIDAS (limpia donde FABRICA no) por cuarto {o['anadidas_por_cuarto']} · "
            f"QUITADAS (se contiene donde FABRICA morderia) por cuarto {o['quitadas_por_cuarto']}")
        log(f"      anadidas con bueno / SIN bueno {o['anadidas_con_vs_sin_bueno']} · quitadas con / sin {o['quitadas_con_vs_sin_bueno']} · "
            f"anadidas por edad {o['anadidas_por_edad']} · por indice del cuerpo {o['anadidas_por_indice_cuerpo']}")
        log(f"      QUITADAS por edad {o['quitadas_por_edad']} · por INDICE DEL CUERPO en el linaje {o['quitadas_por_indice_cuerpo']}")
        log(f"    FABRICA habria mordido {o['fabrica_habria_mordido']} de esas oportunidades · p media {o['p_media']} · |delta TD| medio {o['td_abs_medio']}")
        log(f"    Q final (mediana por linaje-semilla; rasgos [1, u, u_tras, sin_bueno, dist]): no morder {o['w_mediana'][0]} · morder {o['w_mediana'][1]}")
        log(f"    correccion final al logit de la boca de FABRICA, BETA*(Q1-Q0) (mediana; > 0 = limpia mas): {o['politica_mediana']}")
    return out


def entrada_campo_a_campo(log):
    """Regla 14: esta tarea == juez.tarea (linajes y pista), 9 FABRICA, s 8001, T 2000."""
    a = tarea((8001, ['FABRICA'] * 9, 2000)); b = J.tarea((8001, ['FABRICA'] * 9, 2000, 1, 0, 1, None))
    N = lambda x: json.loads(json.dumps(x, default=str))
    ok = N(a['linajes']) == N(b['linajes']) and N(a['pista']) == N(b['pista']) and a['R0_pista'] == b['R0_pista']
    log(f"  ENTRADA campo a campo (regla 14): corre_aprende.tarea == juez.tarea (9 FABRICA, s 8001, T 2000): {'OK' if ok else 'FALLA'}")
    return ok


def identidad_apr_corta(log):
    N = lambda x: json.loads(json.dumps(x, default=str))
    m = P.carga_carro('APR'); m.OPCION = 0
    a = P.run(8001, [('C', P.carga_carro('FABRICA'))] * 9, T=2000); b = P.run(8001, [('C', m)] * 9, T=2000)
    ok = N(a) == N(b)
    log(f"  IDENTIDAD CORTA APR: OPCION 0 == FABRICA (N 9, s 8001, T 2000): {'OK' if ok else 'FALLA'}")
    return ok


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--humo', action='store_true')
    ap.add_argument('--serie', default='apr')
    ap.add_argument('--desde', type=int, default=None)
    ap.add_argument('--n', type=int, default=None)
    ap.add_argument('--T', type=int, default=None)
    ap.add_argument('--con', default=None)   # crudos (json) de series ya corridas, separados por coma, para los pareados
    ap.add_argument('--pool', type=int, default=int(os.environ.get('JUACO_POOL', 0)))
    a = ap.parse_args()
    series = [s.strip() for s in a.serie.split(',') if s.strip()]
    for s in series:
        if s not in SERIES: raise SystemExit(f"serie desconocida {s} (validas {list(SERIES)})")
    if a.humo:
        desde = a.desde or 8001; n = a.n or 1; T = a.T or 30000; pool = 0
        if not all(x in PRACTICA for x in range(desde, desde + n)): raise SystemExit("--humo: solo semillas de practica 8001-8040")
    else:
        desde = a.desde or 8101; n = a.n or 20; T = a.T or T_DEF; pool = a.pool
        sem = range(desde, desde + n)
        if not (all(x in SERIE for x in sem) or all(x in REPLICA for x in sem)): raise SystemExit("serie: solo 8101-8120 (serie) u 8121-8140 (replica)")
        if T != T_DEF: raise SystemExit("serie: T = 100000 (preregistrado)")
    semillas = list(range(desde, desde + n))
    os.makedirs(DATOS, exist_ok=True)
    sel = time.strftime('%Y%m%d_%H%M%S'); pre = f"aprende_{'humo_' if a.humo else ''}{'-'.join(series)}_s{semillas[0]}-{semillas[-1]}_T{T}_{sel}"
    LOGF = open(os.path.join(DATOS, pre + '.log'), 'w', encoding='utf-8')

    def log(s=''):
        print(s, flush=True); LOGF.write(s + '\n'); LOGF.flush()

    t0 = time.time()
    carros_ids = sorted({SERIES[s] for s in series} | {'FABRICA'})
    shas = {c: P.h16(os.path.join(P.CARROS, c + '.py')) for c in carros_ids}
    log(f"CORRE_APRENDE · {pre} · python {platform.python_version()} · pool {pool or 'NO (un proceso)'}")
    log(f"  pista.py {P.h16(os.path.join(PISTA, 'pista.py'))} · juez.py {P.h16(os.path.join(PISTA, 'juez.py'))} · "
        f"corre_aprende.py {P.h16(os.path.abspath(__file__))} · carros {shas}")
    pa = P.carga_carro('APR_AZAR').P_AZAR
    log(f"  series {series} · semillas {semillas[0]}-{semillas[-1]} · T {T} · APR_AZAR.P_AZAR = {pa}")
    if 'azar' in series and pa is None: log("  APR_AZAR sin P_AZAR: fijarlo con construye_apr.py --p_azar <tasa del ultimo cuarto de la serie apr>"); return 1
    rv = {c: RC.revisa(c) for c in carros_ids}
    for c, v in rv.items(): log(f"  CHEQUEO ESTATICO {c}: {'PASA' if not v else 'RECHAZADO ' + str(v)}")
    ide = J.identidad_corta()
    log(f"  IDENTIDAD CORTA del juez (FABRICA == organismo_f9c REL, s 1, T 5000): {'OK' if ide['ok'] else 'FALLA ' + str(ide['dif'][:5])}")
    ok = not any(rv.values()) and ide['ok'] and identidad_apr_corta(log)
    if a.humo: ok = entrada_campo_a_campo(log) and ok
    if not ok: log("  ALGO FALLA -> no se corre."); return 1
    res = {}; RR = {}
    for s in series:
        carros = [SERIES[s]] * 9
        tareas = [(sd, carros, T) for sd in semillas]
        R = []
        if pool and pool > 1:
            from multiprocessing import Pool
            with Pool(pool) as PL:
                for x in PL.imap_unordered(tarea, tareas):
                    R.append(x); log(f"  [{time.time()-t0:7.1f}s] {s} semilla {x['seed']} ({x['seg']}s) R0 pista {x['R0_pista']}")
        else:
            for tk in tareas:
                x = tarea(tk); R.append(x)
                log(f"  [{time.time()-t0:7.1f}s] {s} semilla {x['seed']} ({x['seg']}s) R0 pista {x['R0_pista']} · R0 por linaje {[l['R0'] for l in x['linajes']]}")
        R.sort(key=lambda x: x['seed'])
        for x in R: x.pop('pizarra_log')   # nadie escribe (APR/FABRICA/O1 no usan la pizarra); se verifica abajo
        crudo = os.path.join(DATOS, f"{pre}_{s}.json")
        json.dump(dict(meta=dict(serie=s, carros=carros, semillas=semillas, T=T, sha_carros=shas, P_AZAR=pa, humo=a.humo,
                                 sha_pista=P.h16(os.path.join(PISTA, 'pista.py')), sha_juez=P.h16(os.path.join(PISTA, 'juez.py'))),
                       corridas=R), open(crudo, 'w', encoding='utf-8'), ensure_ascii=False)   # ERR-54: crudo ANTES de resumir
        log(f"  CRUDO {crudo} (sha {P.h16(crudo)}) · escrituras en la pizarra {sum(l['escrituras'] for c in R for l in c['linajes'])}")
        res[s] = resume(R, s, log); RR[s] = R
    if a.con:
        for ruta in a.con.split(','):
            d = json.load(open(ruta.strip(), encoding='utf-8')); s = d['meta']['serie']
            if s in RR: continue
            if d['meta']['T'] != T or d['meta'].get('humo') != a.humo: raise SystemExit(f"--con {ruta}: T o humo distintos")
            RR[s] = d['corridas']; log(f"  (--con) serie {s} desde {ruta} (sha {P.h16(ruta.strip())})")
            res[s] = resume(RR[s], s, log)
    par = {}
    log("\nPAREADOS (por semilla: mediana del R0 de los 9 linajes; gana = semillas en que la primera supera a la segunda)")
    for x, y in (('apr', 'fab'), ('apr', 'sinher'), ('apr', 'azar'), ('sinher', 'fab'), ('azar', 'fab')):
        if x in RR and y in RR:
            par[(x, y)] = pareado(RR[x], RR[y])
            log(f"  {x} vs {y}: gana {par[(x, y)]['gana']}/{par[(x, y)]['semillas']} · diferencia mediana {par[(x, y)]['dif_med']} · {par[(x, y)]['por_semilla']}")
    log("\nPREDICCIONES FIRMADAS (PREREGISTRO_aprende.md) y lo medido" + (" -- HUMO: T y semillas de practica, NO cuentan" if a.humo else ""))
    pred = []
    for txt, f in PRED:
        v = f(res, par); pred.append(dict(texto=txt, se_cumple=v))
        log(f"  {txt} -> {'SE CUMPLE' if v else ('sin la serie' if v is None else 'NO se cumple')}")
    rj = os.path.join(DATOS, pre + '_resumen.json')
    json.dump(dict(series=res, pareados={f"{k[0]}_vs_{k[1]}": v for k, v in par.items()}, predicciones=pred, semillas=semillas, T=T,
                   humo=a.humo, P_AZAR=pa), open(rj, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    log(f"\n  RESUMEN {rj}\nTerminado en {time.time()-t0:.1f}s")
    return 0


if __name__ == '__main__':
    sys.exit(main())
