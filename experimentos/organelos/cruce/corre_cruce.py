"""corre_cruce.py — corredor del bloque organelos/cruce: ¿cruza el BICHO REAL (v14.3 en la pista) R0 real >= 0.90 POR SELECCION
NATURAL de genes de cableado (estado interno presente -> decisiones que ya tiene)? Preregistro: PREREGISTRO_cruce.md.

MISION: llegar a la AGI por este camino.
PISTA: la de la carrera, v1 escalada (9 linajes, L 360, 36 objetos, olvido escalado), fundador_limpio = 1 (ENMIENDA 5), por
motor_cruce.py (== pista.py bit a bit con cruce=None). CUERPO: carros/CRUCE.py (== V143 bit a bit con el genoma en 0).
ENTRADA (regla 14, campo a campo): la MISMA de juez.tarea con fundador_limpio = 1 (seed, carros x9, T, pizarra 1, rep_acum 0,
escala 1, mundo_n None, fl 1) + cruce; juez.resumen_linaje por linaje (solo fisica, ERR-96). El arnes lo compara con
corre_v143.tarea campo a campo.

DOS FASES POR SEMILLA s:
 1. CRIA (declarada: vivero con banco; seleccion SOLO natural: el que vive y pare llena la cola de su linaje y el banco de padres),
    semilla s, T = t_corte: genes nacen en 0; error de copia en cada parto (p_mut por gen, +-1); si un linaje se extingue, el
    fundador lleva un genoma del banco, mutado. En t_corte se CONGELA el banco (y se mide contra sus sombras).
 2. LECTURA (despues del corte nadie repone nada del banco): una carrera NUEVA con la letra de la carrera (ENMIENDA 5, T = 100 000,
    semilla s + 500000), 9 linajes, cada uno con UN genoma sacado al azar del banco del corte ([s, 23, k]); los hijos lo copian sin
    error (el genotipo se lee congelado); el fundador que pone la pista es una instancia NUEVA con el genotipo de su linaje (como
    el fundador de O1 es una instancia nueva del codigo O1). Los nacidos de la lectura son los "nacidos despues del corte".
BRAZOS DE LECTURA:
  vida    9 genomas del banco de VIDA (cria con seleccion)        vida_p  otros 9 del MISMO banco (PLACEBO: calibra el juez)
  azar    9 del banco de AZAR (cria donde el genoma de cada cuerpo nuevo sale al azar del banco de genomas NUEVOS: mutacion sin seleccion)
  mut0    9 del banco de MUT0 (cria sin mutacion: todo 0; == v143 bit a bit, control de instrumento)
  v143    v14.3 fijo (genes apagados)                              o1      O1 (techo escrito por un LLM; SOLO referencia, no compite)
  desf    los MISMOS 9 genomas de vida, con el cableado leyendo senales internas de un paso pasado al azar (ultimos 2000 del linaje):
          el control que PUEDE FALLAR (si vida cruza por leer su estado presente, desf debe caer)
SEMILLAS: practica 24401-24420 (humo y arnes) · serie 24601-24620 · replica 24701-24720 (lectura: +500000). Se niega a usar otras.

    python experimentos/organelos/cruce/corre_cruce.py --humo [--semilla 24401] [--tc 30000] [--tl 20000]
    python experimentos/organelos/cruce/corre_cruce.py --serie --desde 24601 --n 20 --pool 6                       (SOLO el coordinador)
    python experimentos/organelos/cruce/corre_cruce.py --serie --desde 24701 --n 20 --pool 6 --con <resumen serie>  (SOLO el coordinador)
nube-9: cada tarea atrapa SystemExit (y cualquier excepcion) y devuelve un registro de error: una guardia del motor no cuelga el Pool.
Banderas desconocidas o abreviadas: ABORTA (ERR-115). ERR-54: el crudo se escribe ANTES de resumir. Termina con "VEREDICTO:".
Vocabulario: "linaje", "cuerpo", "genoma", "la seleccion prende/apaga"; prohibido "poblacion", "generacion", "evoluciona", "coopera".
"""
import argparse, hashlib, importlib.util, json, os, platform, statistics as st, sys, time, traceback
import numpy as np

sys.dont_write_bytecode = True   # no deja __pycache__ en carpetas ajenas (pista, juez, tronco_v14_3 se importan solo para leer)
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(AQUI)))
PISTA = os.path.join(RAIZ, 'experimentos', 'carrera_escuderias')
sys.path[:0] = [AQUI, PISTA]
import motor_cruce as MC
import juez as J
import revisa_carro as RC
import construye_cruce as CC

DATOS = os.path.join(AQUI, 'datos'); DATOS_HUMO = os.path.join(DATOS, 'humo')
SHAS = {os.path.join(PISTA, 'pista.py'): '9f47c65e438e0ff4', os.path.join(PISTA, 'juez.py'): '6a68f640a7832f12',
        os.path.join(PISTA, 'carros', 'O1.py'): '99436afa2715f028', os.path.join(PISTA, 'revisa_carro.py'): '1c8a789f7427ab96',
        os.path.join(RAIZ, 'experimentos', 'tronco_v14_3', 'carros_v143', 'V143.py'): '2a03048a7f1525e5',
        os.path.join(RAIZ, 'experimentos', 'tronco_v14_3', 'corre_v143.py'): '24100621c450da22'}
PRACTICA = range(24401, 24421); SERIE = range(24601, 24621); REPLICA = range(24701, 24721)
OFF_LECT = 500000                       # semilla de la lectura = s + 500000 (grep: 524401-524420, 524601-524620, 524701-524720 sin uso)
TC_DEF = 200000; TL_DEF = 100000        # cria y lectura (preregistrados)
P_MUT = 0.03; BANCO = 200; N_SOMBRA = 8; G_MAX = 4; CADA = 10000; ETQ_MUESTRA = 23
CRIAS = ('vida', 'azar', 'mut0')
LECTURAS = ('vida', 'vida_p', 'desf', 'azar', 'mut0', 'v143', 'o1')
MUESTRA_DE = {'vida': ('vida', 0), 'vida_p': ('vida', 1), 'desf': ('vida', 0), 'azar': ('azar', 0), 'mut0': ('mut0', 0)}
GANA = 15; DIF_MOD = 0.05; R0_CRUCE = 0.90; PLACEBO = (5, 15)
ANCLA_V143 = (0.40, 0.75)   # v14.3 fijo, R0 real (juez, T 1e5): serie 14301 0.536, replica 14321 0.63
ANCLA_O1 = 0.85             # O1: R0 real mediano >= 0.85 (serie 14301: 0.9375)

_MODS = {}


def h16(p): return hashlib.sha256(open(p, 'rb').read()).hexdigest()[:16]


def modulo(ident):
    if ident not in _MODS:
        if ident == 'O1': _MODS[ident] = MC.carga_carro('O1')
        else:
            spec = importlib.util.spec_from_file_location('carro_CRUCE', os.path.join(AQUI, 'carros', 'CRUCE.py'))
            m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); _MODS[ident] = m
    return _MODS[ident]


def cfg_cria(brazo, tc):
    c = dict(NG=modulo('CRUCE').NG, p_mut=P_MUT, t_corte=tc, banco_max=BANCO, donante='padre', n_sombra=N_SOMBRA, g_max=G_MAX, cada=CADA)
    if brazo == 'azar': c['donante'] = 'azar'
    elif brazo == 'mut0': c['p_mut'] = 0.0
    elif brazo != 'vida': raise SystemExit(f"cria desconocida {brazo!r}")
    return c


def cfg_lectura(brazo, genomas):
    if brazo in ('v143', 'o1'): return None
    return dict(NG=modulo('CRUCE').NG, p_mut=0.0, t_corte=0, banco_max=0, donante='padre', n_sombra=0, g_max=G_MAX, cada=CADA,
                genomas_ini=[[int(x) for x in g] for g in genomas], lesion_desde=(0 if brazo == 'desf' else None))


def muestra(banco, seed, k):
    """9 genomas del banco del corte, sin reemplazo, con rng propio [seed, 23, k] (k = 0 la muestra, 1 el placebo)."""
    r = np.random.default_rng([seed, ETQ_MUESTRA, k])
    ix = r.choice(len(banco), size=9, replace=len(banco) < 9)
    return [list(banco[int(i)]) for i in ix]


def _carrera(seed, carros, T, cruce):
    """== juez.tarea(seed, carros, T, pizarra=1, rep_acum=0, escala=1, mundo_n=None, fundador_limpio=1) + cruce."""
    r = MC.run(seed, carros, T=T, pizarra=1, rep_acum=0, escala=1, mundo_n=None, fundador_limpio=1, cruce=cruce)
    L = [J.resumen_linaje(d, seed) for d in r['linajes']]
    for x in L:
        tf, qf, nr = J.t_fund_reconstruido(x['telem']['vidas'], x['telem']['desc_por_vida'])
        x['t_fund_rec_ok'] = bool(tf[:200] == x['telem']['t_fund'] and qf == x['cola_final'] and nr == x['nac_reales'])
    sd = sum(x['descendientes'] for x in L); sm = sum(x['muertes'] for x in L)
    tel = [dict(v143=d['carro'].get('v143'), cruce=d['carro'].get('cruce')) for d in r['linajes']]
    return dict(linajes=L, pista=r['pista'], R0_pista=round(sd / (sm + len(L)), 4), pizarra_n=len(r['pizarra_log']), tel=tel, cruce=r.get('cruce'))


def tarea(args):
    """('cria', seed, brazo, tc) | ('lee', seed, brazo, tl, genomas). nube-9: NUNCA deja escapar SystemExit (la guardia de ERR-60
    colgaba el Pool en silencio): devuelve un registro con 'error'."""
    t0 = time.time(); fase, seed, brazo = args[0], args[1], args[2]
    base = dict(fase=fase, seed=seed, brazo=brazo)
    try:
        if fase == 'cria':
            tc = args[3]
            r = _carrera(seed, [('V143', modulo('CRUCE'))] * 9, tc, cfg_cria(brazo, tc))
            k = r['cruce']['corte']
            return dict(base, T=tc, seg=round(time.time() - t0, 1), error=None, banco=k.get('banco'), corte={x: k[x] for x in k if x != 'banco'},
                        linajes=r['linajes'], pista=r['pista'], cruce={x: r['cruce'][x] for x in r['cruce'] if x not in ('corte', 'final')})
        if fase == 'lee':
            tl, genomas = args[3], args[4]
            ident = 'O1' if brazo == 'o1' else 'CRUCE'
            r = _carrera(seed + OFF_LECT, [('O1' if brazo == 'o1' else 'V143', modulo(ident))] * 9, tl, cfg_lectura(brazo, genomas))
            return dict(base, T=tl, seg=round(time.time() - t0, 1), error=None, genomas=genomas, **r)
        raise SystemExit(f"fase desconocida {fase!r}")
    except KeyboardInterrupt:
        raise
    except BaseException as e:   # SystemExit incluido (nube-9)
        return dict(base, seg=round(time.time() - t0, 1), error=f"{type(e).__name__}: {e}", tb=traceback.format_exc()[-3000:])


def med(xs):
    xs = [x for x in xs if x is not None]
    return round(float(st.median(xs)), 4) if xs else None


def sem_R0(c): return med([l['R0_real'] for l in c['linajes']])


def fisica(c): return json.dumps(c['linajes'], sort_keys=True, default=str)


# ------------------------------------------------------------------------------------------------ genes contra sombras
def genes_vs_sombras(crias, NOMBRES):
    """Por gen: en cuantas semillas la media del BANCO del corte queda por encima (o debajo) de las medias de sus 8 sombras, y en
    cuantas la fraccion que EXPRESA el gen (!= 0) supera a la de todas sus sombras. Bajo neutralidad cada una es 1/9 por semilla."""
    NG = len(NOMBRES); pos = [0] * NG; neg = [0] * NG; expr = [0] * NG; n = 0; medias = [[] for _ in range(NG)]
    for c in crias:
        k = c.get('corte') or {}
        if 'sombra_media' not in k: continue
        n += 1
        for j in range(NG):
            sm = [q[j] for q in k['sombra_media']]; sz = [q[j] for q in k['sombra_nz']]
            pos[j] += int(k['banco_media'][j] > max(sm)); neg[j] += int(k['banco_media'][j] < min(sm)); expr[j] += int(k['banco_nz'][j] > max(sz))
            medias[j].append(k['banco_media'][j])
    return dict(n=n, gen={NOMBRES[j]: dict(sube=pos[j], baja=neg[j], expresa=expr[j], media_banco=med(medias[j])) for j in range(NG)})


# Lo que HARIAN O1/O3 escrito en esta base (DESCRIPTIVO, fijado antes de la serie; NO esta en el carro): signo esperado.
PARECIDO_O = {'boca_bueno_reserva': -1,   # O1 MARGEN: muerde lo bueno solo si le sirve (con reserva alta, no)
              'boca_malo_otra': +1,       # O1 limpieza costeable: el golpe cae en la necesidad MAS llena
              'boca_neutro_sesgo': -1,    # O1 PRUEBA: lo desconocido solo con reserva ...
              'boca_neutro_reserva': +1,  # ... (E y Ag > 0.5)
              'pata_act_sesgo': +1,       # O1: va a lo que le sirve a la necesidad activa (ganancia/distancia), no a lo mas cercano
              'boca_bueno_cola': -1,      # O3 TERMINAL: con cola larga deja de comer lo bueno ...
              'boca_malo_cola': +1}       # ... y limpia hasta morir


def parecido(gs):
    out = {}
    for g, s in PARECIDO_O.items():
        x = gs['gen'][g]
        out[g] = dict(signo_O=s, semillas_mismo_signo=(x['sube'] if s > 0 else x['baja']), semillas_contrario=(x['baja'] if s > 0 else x['sube']))
    return out


# ------------------------------------------------------------------------------------------------ resumen y veredicto
def resume_lectura(R, brazo, log):
    ok = [c for c in R if not c.get('error')]; todos = [l for c in ok for l in c['linajes']]
    if not todos:
        log(f"\n== lectura {brazo}: SIN corridas validas ({len(R)} con error)"); return dict(brazo=brazo, n_ok=0, errores=len(R))
    ns = len(ok); cm = J.criterio_mono(todos)
    e5 = sum(1 for c in ok if sum(l['cruza_real'] for l in c['linajes']) * 2 > len(c['linajes']))
    e6 = sum(1 for c in ok if sum(l['persiste'] for l in c['linajes']) * 2 > len(c['linajes']))
    cz = {k: sum(l['causas'][k] for l in todos) for k in ('hambre', 'sed', 'veneno', 'sal')}
    out = dict(brazo=brazo, n_ok=ns, errores=len(R) - ns, R0_real_med=med([sem_R0(c) for c in ok]), R0_real_linajes_med=med([l['R0_real'] for l in todos]),
               linajes_cruzan=sum(l['cruza_real'] for l in todos), linajes=len(todos), sem_cruza_e5=e5, gana_e5=bool(e5 >= GANA * ns / 20),
               sem_estabiliza_e6=e6, persisten=sum(l['persiste'] for l in todos), casi_inmortales=sum(l['casi_inmortal'] for l in todos),
               R0_eval_med=cm['mediana_R0_real_eval'], vida_med=med([l['vida_med'] for l in todos]), muertes_med=med([l['muertes'] for l in todos]),
               fundadores_med=med([l['fundadores'] for l in todos]), causas=cz, frac_BD_causa=round((cz['veneno'] + cz['sal']) / max(1, sum(cz.values())), 4),
               coherente=f"{sum(l['coherente'] for l in todos)}/{len(todos)}", t_fund_rec=f"{sum(l['t_fund_rec_ok'] for l in todos)}/{len(todos)}",
               seg_med=med([c['seg'] for c in ok]), pizarra=sum(c['pizarra_n'] for c in ok),
               frac_sin_bueno_mundo_med=med([c['pista']['frac_sin_bueno_mundo'] for c in ok]))
    tel = [t['cruce'] for c in ok for t in c['tel'] if t.get('cruce')]
    if tel:
        s = lambda k: sum(t.get(k, 0) for t in tel)
        out['cableado'] = {k: s(k) for k in ('boca_dif', 'boca_dec', 'pata_dif', 'pata_dec', 'vetos_parto', 'partos_dec', 'lesion_lecturas', 'cuerpos_on')}
    log(f"\n== lectura {brazo} · {ns} semillas ({len(R) - ns} con error) · T {ok[0]['T']} · fundador limpio con el genotipo del linaje")
    log(f"  R0 REAL (juez, nacidos tras el corte) mediana por semilla {out['R0_real_med']} · ENMIENDA 5: linajes {out['linajes_cruzan']}/{out['linajes']}, "
        f"semillas con mayoria {e5}/{ns} -> {'GANA' if out['gana_e5'] else 'no gana'} · ENMIENDA 6 semillas {e6}/{ns} · casi inmortales {out['casi_inmortales']}")
    log(f"  vida {out['vida_med']} · muertes {out['muertes_med']} · fundadores {out['fundadores_med']} · veneno+sal {out['frac_BD_causa']} · "
        f"coherente {out['coherente']} · t_fund {out['t_fund_rec']} · s por corrida {out['seg_med']} · pizarra {out['pizarra']}"
        + (f" · cableado {out['cableado']}" if tel else ''))
    return out


def resume_cria(R, brazo, log):
    ok = [c for c in R if not c.get('error')]
    if not ok: return dict(brazo=brazo, n_ok=0, errores=len(R))
    cr = [c['cruce'] for c in ok]; todos = [l for c in ok for l in c['linajes']]
    out = dict(brazo=brazo, n_ok=ns if (ns := len(ok)) else 0, errores=len(R) - len(ok), R0_real_cria_med=med([sem_R0(c) for c in ok]),
               muertes_med=med([l['muertes'] for l in todos]), fundadores_med=med([l['fundadores'] for l in todos]),
               n_mut=sum(c['n_mut'] for c in cr), n_partos=sum(c['n_partos'] for c in cr), n_refund=sum(c['n_refund'] for c in cr),
               ham=[sum(c['ham'][j] for c in cr) for j in range(12)],
               banco_con_genes=med([sum(1 for g in c['banco'] if any(g)) / max(1, len(c['banco'])) for c in ok]), seg_med=med([c['seg'] for c in ok]))
    log(f"  cria {brazo}: {ns} semillas · R0 real en la cria {out['R0_real_cria_med']} · muertes {out['muertes_med']} · fundadores {out['fundadores_med']} · "
        f"mutaciones {out['n_mut']} · partos {out['n_partos']} · refundados del banco {out['n_refund']} · banco con algun gen != 0 {out['banco_con_genes']} · "
        f"distancia hijo-padre {out['ham']} · s {out['seg_med']}")
    return out


def pareado(Ra, Rb):
    A = {c['seed']: sem_R0(c) for c in Ra if not c.get('error')}; B = {c['seed']: sem_R0(c) for c in Rb if not c.get('error')}
    ss = sorted(set(A) & set(B)); g = sum(1 for s in ss if A[s] > B[s])
    return dict(n=len(ss), gana=g, dif_med=med([A[s] - B[s] for s in ss]))


def veredicto(res, pares, mut0_ok, n_err, ns):
    """La letra del PREREGISTRO_cruce.md sec. 6, por UNA serie (FUNCIONA exige serie Y replica: lo combina --con)."""
    g = lambda b, k: (res.get(b) or {}).get(k)
    pl = pares['vida-vida_p']['gana']
    lee = dict(ancla_v143=bool(g('v143', 'R0_real_med') is not None and ANCLA_V143[0] <= g('v143', 'R0_real_med') <= ANCLA_V143[1]),
               ancla_o1=bool(g('o1', 'R0_real_med') is not None and g('o1', 'R0_real_med') >= ANCLA_O1),
               placebo=bool(PLACEBO[0] * ns / 20 <= pl <= PLACEBO[1] * ns / 20), mut0_igual=bool(mut0_ok), sin_perdidas=bool(n_err <= 2))
    v = g('vida', 'R0_real_med')
    F1 = bool(v is not None and v >= R0_CRUCE and g('vida', 'gana_e5'))
    F2 = pares['vida-azar']['gana'] >= GANA * ns / 20; F3 = pares['vida-v143']['gana'] >= GANA * ns / 20
    F4 = pares['vida-desf']['gana'] >= GANA * ns / 20
    MOD = F2 and F3 and (pares['vida-v143']['dif_med'] or 0) >= DIF_MOD
    if not all(lee.values()): ver = 'NO SE LEE'
    elif F1 and F2 and F3 and F4: ver = 'FUNCIONA'
    elif F1 and F2 and F3: ver = 'HAY ALGO MODESTO (cruza, pero el control desfasado NO cae: no se puede decir que cruce por leer su estado)'
    elif MOD: ver = 'HAY ALGO MODESTO'
    else: ver = 'NO'
    return dict(lee=lee, F1_vida_cruza=F1, F2_vida_gana_azar=F2, F3_vida_gana_v143=F3, F4_desf_cae=F4, modesto=MOD, veredicto=ver)


def informe(R, log, ns):
    cr = lambda b: [c for c in R if c['fase'] == 'cria' and c['brazo'] == b]
    le = lambda b: [c for c in R if c['fase'] == 'lee' and c['brazo'] == b]
    log("\nCRIA (antes del corte; no decide)")
    rc = {b: resume_cria(cr(b), b, log) for b in CRIAS if cr(b)}
    rl = {b: resume_lectura(le(b), b, log) for b in LECTURAS if le(b)}
    pares = {f"{a}-{b}": pareado(le(a), le(b)) for a, b in (('vida', 'azar'), ('vida', 'v143'), ('vida', 'desf'), ('vida', 'vida_p'),
                                                          ('azar', 'v143'), ('o1', 'vida')) if le(a) and le(b)}
    log("\nPAREADOS (por semilla: mediana del R0 real de los 9 linajes de la lectura; gana = semillas en que el primero supera al segundo)")
    for k, p in pares.items(): log(f"  {k}: gana {p['gana']}/{p['n']} · diferencia mediana {p['dif_med']}")
    m0 = {c['seed']: fisica(c) for c in le('mut0') if not c.get('error')}; v3 = {c['seed']: fisica(c) for c in le('v143') if not c.get('error')}
    comunes = set(m0) & set(v3); ns_lee = len({c['seed'] for c in R if c['fase'] == 'lee'})   # ERR-124 (H-2 del auditor): 20/20, no la interseccion
    mut0_ok = bool(comunes) and len(comunes) == ns_lee and all(m0[s] == v3[s] for s in comunes)
    log(f"  instrumento: lectura mut0 == v143 (fisica de los 9 linajes) en {sum(m0[s] == v3[s] for s in comunes)}/{len(comunes)} semillas")
    NOM = list(modulo('CRUCE').NOMBRES_GEN); gs = {}
    for b in ('vida', 'azar'):
        if cr(b):
            gs[b] = genes_vs_sombras([c for c in cr(b) if not c.get('error')], NOM)
            top = sorted(gs[b]['gen'].items(), key=lambda kv: -max(kv[1]['sube'], kv[1]['baja']))[:8]
            log(f"  GENES contra sus 8 sombras en el corte ({b}, {gs[b]['n']} semillas; bajo neutralidad ~{gs[b]['n'] / 9:.1f} por columna): " +
                "; ".join(f"{g} sube {x['sube']} baja {x['baja']} expresa {x['expresa']} (media {x['media_banco']})" for g, x in top))
    par = parecido(gs['vida']) if 'vida' in gs else None
    if par: log(f"  PARECIDO a O1/O3 (descriptivo, signos fijados antes): {par}")
    n_err = sum(1 for c in R if c.get('error'))
    for c in R:
        if c.get('error'): log(f"  ERROR {c['fase']} {c['brazo']} s{c['seed']}: {c['error']}")
    need = ('vida-azar', 'vida-v143', 'vida-desf', 'vida-vida_p')
    ver = veredicto(rl, pares, mut0_ok, n_err, ns) if all(k in pares for k in need) and 'o1' in rl else None
    return dict(cria=rc, lectura=rl, pareados=pares, mut0_igual_v143=mut0_ok, genes=gs, parecido_O=par, errores=n_err, veredicto=ver)


# ------------------------------------------------------------------------------------------------ comprobaciones previas
def previas(log):
    malos = [os.path.relpath(r, RAIZ) for r, s in SHAS.items() if h16(r) != s]
    if malos: raise SystemExit(f"ABORTA: shas de origen cambiados {malos}")
    outs = CC.todas()
    dif = [r for r, b in outs.items() if open(r, 'rb').read() != b]
    if dif: raise SystemExit(f"ABORTA: motor o carro en disco != construye_cruce {dif}")
    v = RC.revisa_fuente(open(os.path.join(AQUI, 'carros', 'CRUCE.py'), encoding='utf-8').read(), 'CRUCE')
    if v: raise SystemExit(f"ABORTA: revisa_carro rechaza CRUCE: {v[:3]}")
    log(f"  previas OK: shas de origen, motor {h16(os.path.join(AQUI, 'motor_cruce.py'))} y carro {h16(os.path.join(AQUI, 'carros', 'CRUCE.py'))} "
        f"== construye, revisa_carro PASA, corre_cruce {h16(os.path.abspath(__file__))}")


def escribe(ruta, obj):
    os.makedirs(os.path.dirname(ruta), exist_ok=True)
    b = json.dumps(obj, default=str).encode('utf-8'); open(ruta, 'wb').write(b)
    return hashlib.sha256(b).hexdigest()[:16]


def argumentos(argv=None):
    ap = argparse.ArgumentParser(allow_abbrev=False)
    ap.add_argument('--humo', action='store_true'); ap.add_argument('--serie', action='store_true')
    ap.add_argument('--tc', type=int, default=None); ap.add_argument('--tl', type=int, default=None)
    ap.add_argument('--semilla', type=int, default=24401); ap.add_argument('--desde', type=int, default=None); ap.add_argument('--n', type=int, default=20)
    ap.add_argument('--pool', type=int, default=None); ap.add_argument('--con', default=None); ap.add_argument('--etiqueta', default='')
    ap.add_argument('--crias', default=None); ap.add_argument('--lecturas', default=None)   # SOLO --humo
    return ap.parse_args(argv)


HUMO_LECT = ('vida', 'desf', 'azar', 'v143')   # humo: 2 crias + 4 lecturas = 6 corridas


def main(argv=None):
    a = argumentos(argv)
    if a.humo == a.serie: raise SystemExit("elige --humo o --serie (uno)")
    stamp = time.strftime('%Y%m%d_%H%M%S')
    if a.humo:
        tc = a.tc or 30000; tl = a.tl or 20000
        crias = tuple(x for x in (a.crias or 'vida,azar').split(',') if x); lects = tuple(x for x in (a.lecturas or ','.join(HUMO_LECT)).split(',') if x)
        if any(x not in CRIAS for x in crias) or any(x not in LECTURAS for x in lects): raise SystemExit(f"humo: crias {CRIAS} y lecturas {LECTURAS}")
        if any(MUESTRA_DE[x][0] not in crias for x in lects if x in MUESTRA_DE): raise SystemExit("humo: una lectura pide el banco de una cria que no corre")
        if a.semilla not in PRACTICA: raise SystemExit(f"--humo solo con semillas de practica {PRACTICA.start}-{PRACTICA.stop - 1}")
        if len(crias) + len(lects) > 6 or len(crias) * tc + len(lects) * tl > 200000: raise SystemExit("humo: maximo 6 corridas y 200 000 pasos en total")
        if a.pool: raise SystemExit("humo: sin Pool (un proceso)")
        semillas = [a.semilla]; carpeta = DATOS_HUMO
        pref = os.path.join(carpeta, f"cruce_humo_s{a.semilla}_tc{tc}_tl{tl}{('_' + a.etiqueta) if a.etiqueta else ''}_{stamp}")
    else:
        tc = a.tc or TC_DEF; tl = a.tl or TL_DEF
        if (tc, tl) != (TC_DEF, TL_DEF): raise SystemExit(f"--serie solo con cria {TC_DEF} y lectura {TL_DEF} (preregistrados)")
        semillas = list(range(a.desde, a.desde + a.n)) if a.desde else []
        if not semillas or not (all(s in SERIE for s in semillas) or all(s in REPLICA for s in semillas)):
            raise SystemExit(f"--serie: --desde/--n dentro de la serie {SERIE.start}-{SERIE.stop - 1} o la replica {REPLICA.start}-{REPLICA.stop - 1}")
        if not a.pool or not 1 <= a.pool <= 6: raise SystemExit("--serie exige --pool 1..6")
        if a.crias or a.lecturas: raise SystemExit("--serie corre TODAS las crias y lecturas preregistradas (--crias/--lecturas solo en --humo)")
        crias = CRIAS; lects = LECTURAS; carpeta = DATOS
        pref = os.path.join(carpeta, f"cruce_{'serie' if semillas[0] in SERIE else 'replica'}_s{semillas[0]}-{semillas[-1]}_{stamp}")
    os.makedirs(carpeta, exist_ok=True)
    flog = open(pref + '.log', 'w', encoding='utf-8')
    def log(s=''):
        print(s, flush=True); flog.write(s + '\n'); flog.flush()
    log(f"CRUCE · {time.strftime('%Y-%m-%d %H:%M:%S')} · {platform.node()} · python {platform.python_version()} · semillas {semillas[0]}-{semillas[-1]} · "
        f"cria {tc} · lectura {tl} · crias {crias} · lecturas {lects}")
    previas(log)
    t0 = time.time(); R = []
    parcial = open(pref + '_parcial.jsonl', 'w', encoding='utf-8')
    def guarda(c):
        R.append(c); parcial.write(json.dumps({k: v for k, v in c.items() if k != 'tb'} | ({'tb': c['tb']} if 'tb' in c else {}), default=str) + '\n'); parcial.flush()
        extra = f"ERROR {c['error']}" if c.get('error') else f"R0 real {sem_R0(c)}"
        log(f"  [{time.time() - t0:7.1f}s] {c['fase']} {c['brazo']} s{c['seed']} ({c['seg']}s) {extra}")
    t1 = [('cria', s, b, tc) for b in crias for s in semillas]
    def lecturas_de(bancos):
        out = []
        for b in lects:
            for s in semillas:
                if b in MUESTRA_DE:
                    cb, k = MUESTRA_DE[b]; bk = bancos.get((cb, s))
                    if bk is None: continue   # su cria fallo: se registra como error de la cria, no se lee
                    out.append(('lee', s, b, tl, muestra(bk, s, k)))
                else: out.append(('lee', s, b, tl, None))
        return out
    if a.humo:
        for tk in t1: guarda(tarea(tk))
        bancos = {(c['brazo'], c['seed']): c['banco'] for c in R if c['fase'] == 'cria' and not c.get('error')}
        for tk in lecturas_de(bancos): guarda(tarea(tk))
    else:
        from multiprocessing import Pool   # SOLO el coordinador corre --serie
        with Pool(a.pool) as pool:
            for c in pool.imap_unordered(tarea, t1): guarda(c)
            bancos = {(c['brazo'], c['seed']): c['banco'] for c in R if c['fase'] == 'cria' and not c.get('error')}
            for c in pool.imap_unordered(tarea, lecturas_de(bancos)): guarda(c)
    parcial.close()
    R.sort(key=lambda c: (c['fase'], c['brazo'], c['seed']))
    sha = escribe(pref + '_crudo.json', R)
    log(f"  CRUDO {pref}_crudo.json (sha {sha})")
    inf = informe(R, log, len(semillas))
    resumen = dict(tc=tc, tl=tl, semillas=semillas, humo=bool(a.humo), p_mut=P_MUT, banco=BANCO, n_sombra=N_SOMBRA, g_max=G_MAX,
                   seg_total=round(time.time() - t0, 1),
                   seg_por_tarea={f"{f}_{b}": med([c['seg'] for c in R if c['fase'] == f and c['brazo'] == b]) for f, b in {(c['fase'], c['brazo']) for c in R}},
                   **inf)
    if a.con:
        prev = json.load(open(a.con, encoding='utf-8')); v1 = (prev.get('veredicto') or {}).get('veredicto'); v2 = (inf.get('veredicto') or {}).get('veredicto')
        orden = ['NO SE LEE', 'NO', 'HAY ALGO MODESTO', 'FUNCIONA']
        k = lambda v: next((i for i, o in enumerate(orden) if v and v.startswith(o)), 0)
        resumen['bloque'] = dict(serie=v1, replica=v2, veredicto=(v1 if k(v1) <= k(v2) else v2))
    sha = escribe(pref + '_resumen.json', resumen)
    log(f"  RESUMEN {pref}_resumen.json (sha {sha}) · {resumen['seg_total']} s")
    ver = inf.get('veredicto')
    if a.humo: log("VEREDICTO: HUMO (una semilla de practica: sin valor, no se lee)")
    elif 'bloque' in resumen: log(f"VEREDICTO: {resumen['bloque']['veredicto']} (serie {resumen['bloque']['serie']} · replica {resumen['bloque']['replica']})")
    else: log(f"VEREDICTO: PARCIAL (sin replica; no se declara): {ver['veredicto'] if ver else 'incompleto'} · {ver}")
    flog.close()
    return resumen


if __name__ == '__main__':
    main()
