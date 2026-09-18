"""BLOQUE 1 — ENMIENDA 1 (ERR-46): la medida que separa "aprende la excepcion a costa de los hermanos" de
"no aprende nada". Ejecuta PREREGISTRO_bloque1_familias_enm1.md (su sha va en el meta del JSON).

POR QUE (401-420): `colateral` contaba MORDIDAS DE VENENO EN LOS HERMANOS, y un organismo que no aprende nada muerde
veneno todo el rato -> `azar` 19.5 y `barajado` 17.0 contra `excepciones` 6.0. La medida media IGNORANCIA. Es la
trampa ERR-44 por otra puerta. `w_var` igual: 0.000 donde el organismo aprende y 2.79 en `barajado`.

QUE HACE ESTA ENMIENDA (todo en el runner; el instrumento NO se toca y su identidad 43/43 sigue valiendo):
  - MEDIDA NUEVA `colateral_n`: caida de la fraccion de HERMANOS bien leidos por la boca en los `vent` pasos que
    siguen a la primera mordida de la ventana, CONDICIONADA a (a) que la excepcion se haya APRENDIDO dentro de la
    ventana y (b) que al menos 2 de 3 hermanos ya se leyeran bien ANTES. Se calcula de la serie `log` (perilla
    `log_cada` de v14.1, que registra `valor(P)` = LO QUE LEE LA BOCA, nunca un peso interno: T-E / ERR-44).
  - `n_valida` OBLIGATORIA al lado: donde no hay familia real la pregunta NO ESTA DEFINIDA (guarda contra ERR-39).
  - `dano_bruto` sin condicionar: el control que ensena POR QUE fallaba la medida vieja.
  - n_exc = 8 (una excepcion por token) y perilla de DUREZA: costo x4 = 0.008, elegido por la REGLA FIJA de la
    escalera {2,4,6} sobre el brazo de control (ERR-47); la derivacion x12 de la seccion 4 se refuto en el humo.
  - ERR-48: `dano` en DIFERENCIA EN DIFERENCIAS (los hermanos contra el resto del mundo, misma ventana y corrida),
    porque la version cruda medía la tendencia global de aprendizaje y salia negativa en los cuatro mundos.
  - `w_var` RETIRADA como puerta (ERR-46); se sigue reportando.

REUTILIZA `corre_familias.py` POR IMPORT (E.6 / ERR-38): el mundo, los brazos base, el diagnostico estructural, el
cruce `cod0`, los estadisticos y los casos de identidad vienen de alli. Aqui no se copia nada de eso.

    python experimentos/nivel12_mundo_familias/corre_familias_enm1.py --humo   (UN proceso, sin Pool)
    python experimentos/nivel12_mundo_familias/corre_familias_enm1.py [--desde 441] [--T 100000] [--dureza 12]

REGLA 3 y 11: el `Pool` lo lanza SOLO el coordinador. REGLA 10: log desde el arranque, con fsync.
ERR-31: los umbrales viven en UMBRALES, cada uno con la FRASE LITERAL del preregistro al lado.
"""
import sys, os, json, time, platform, subprocess

sys.stdout.reconfigure(encoding='utf-8', errors='replace')
AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
CREB = os.path.join(RAIZ, 'experimentos', 'creacion_B')
sys.path[:0] = [AQUI, CREB, os.path.join(RAIZ, 'organismo')]   # organismo/ PRIMERO (ERR-28)
import numpy as np
import corre_familias as CF                      # el bloque 1 sin tocar: mundo, brazos, diagnostico, estadisticos

log, h16, N, med, cuartiles, razon, A12, cuenta = CF.log, CF.h16, CF.N, CF.med, CF.cuartiles, CF.razon, CF.A12, CF.cuenta
_log = CF._log

T = 100000
N_PARALELO = CF.N_PARALELO
N_SEM = 20
DESDE = 441                                      # semillas NUEVAS (replica 461-480, regla 12)
SHA_INSTRUMENTO = 'b9dd561a0cf056b8'             # organismo_familias.py, el que paso 43/43. Tripwire.

# ---------------------------------------------------------------- constantes de la enmienda (PREREGISTRO enm1)
N_EXC = 8                                        # 3: una excepcion por token
DUREZA = 4     # ERR-47 (ADENDA A): la escalera {2,4,6} sobre LIN dio 3.5 / 31.0 / 82.5 muertes; la REGLA FIJA
               # (el MENOR dentro de [20,250]) elige 4 -> costo 0.008. Datos: familias_enm1_escalera_20260918_150316
               # (031a782dde669d80). La derivacion x12 de la seccion 4 quedo refutada por el humo y se registra.
COSTO_TRONCO = 0.002
LOG_CADA = 250                                   # muestreo de `valor(P)` para las medidas nuevas (no toca el rng)
H_MIN = 0.67                                     # 2: >= 2 de 3 hermanos ya bien leidos ANTES de la excepcion
CRIT = 0.5                                       # el crit_exp del mundo, sin cambio

MUNDO = dict(CF.MUNDO, n_exc=N_EXC, costo=round(COSTO_TRONCO * DUREZA, 6), log_cada=LOG_CADA)
BRAZOS = {
    'EXC': dict(MUNDO),
    'LIN': dict(MUNDO, n_exc=0),
    'AZA': dict(MUNDO, fam_val='azar'),
    'BAR': dict(MUNDO, fam_val='barajado'),
    'V14': dict(mundo='AB'),                     # ancla: v14.1 literal con el costo del TRONCO. No compite.
}
ORDEN = ['EXC', 'LIN', 'AZA', 'BAR', 'V14']
BRAZOS_ACTIVOS = list(ORDEN)

UMBRALES = {
    'E1': dict(frase="las muertes por 100000 de EXC y LIN caen en [20, 250] (medianas); con dureza=12 no cayeron "
                     "y la clausula gasto su UNICA correccion (ERR-47): dureza=4 por regla fija sobre la escalera; "
                     "fuera de banda -> UNA correccion de dureza con ERR-47 y semillas nuevas",
               lo=20, hi=250),
    'E2a': dict(frase="pareado por semilla colateral_n(EXC) > colateral_n(LIN) en >= 15/20; refuta en <= 11/20",
                n_pasa=15, n_refuta=11),
    'E2b': dict(frase="mediana colateral_n(EXC) >= 0.20; refuta en <= 0.05; entre medias INDECISO",
                pasa=0.20, refuta=0.05),
    'E3': dict(frase="mediana n_valida: EXC >= 4 y LIN >= 4 (de 8); BAR <= 2 y AZA <= 2; y colateral_n(AZA) y "
                     "colateral_n(BAR) <= colateral_n(LIN) en medianas",
               fam_min=4, nofam_max=2),
    'E4': dict(frase="dano_bruto NO ordena: dano_bruto(AZA) >= dano_bruto(EXC) o dano_bruto(BAR) >= dano_bruto(EXC), "
                     "mientras colateral_n si ordena"),
    'E5': dict(frase="w_var RETIRADA como puerta (ERR-46): se reporta, no decide"),
    'E7': dict(frase="subconjunto critico del arnes 24/24; sha organismo_familias.py == b9dd561a0cf056b8"),
}


# ---------------------------------------------------------------- las medidas nuevas, desde `log` (fuera del organismo)
def medidas_nuevas(r):
    """PREREGISTRO enm1 seccion 2. Todo sale de `log` (valor(P) = LO QUE LEE LA BOCA) y de `t_exc`; ninguna medida
    mira un peso interno (T-E, ERR-44). Devuelve colateral_n, n_valida, dano_bruto, apr_tasa, h_antes_med y el
    detalle por ventana."""
    nombres = sorted(r['val_mundo'])
    idx = {k: i + 1 for i, k in enumerate(nombres)}          # log = (t, v_k1, v_k2, ...) con k en sorted(PAT)
    lg = r['log']
    if not lg:
        return dict(colateral_n=None, n_valida=0, dano_bruto=None, dano_mundo=None, apr_tasa=None,
                    h_antes_med=None, n_ventanas=0, ventanas={})
    ts = [fila[0] for fila in lg]
    obj = {k: (1.0 if r['val_mundo'][k] == 'comida' else (-1.0 if r['val_mundo'][k] == 'veneno' else 0.0))
           for k in nombres}
    vent = r['fam']['vent']

    def fila_antes(t):                                        # ultimo punto de log ESTRICTAMENTE anterior a t
        i = np.searchsorted(ts, t, side='left') - 1
        return lg[i] if i >= 0 else None

    def fila_cerca(t):                                        # punto de log mas cercano a t (sin pasarse de la corrida)
        i = int(np.searchsorted(ts, t, side='left'))
        return lg[min(i, len(lg) - 1)]

    def ok(fila, k):
        if fila is None or obj[k] == 0:
            return None
        v = float(fila[idx[k]])
        return int(v * obj[k] > 0 and abs(v) >= CRIT)

    det = {}
    for e, t0 in r['t_exc'].items():
        herm = [h for h in r['herm'][e] if obj[h] != 0]
        if not herm:
            continue
        # ERR-48: el RESTO DEL MUNDO = los estimulos AJENOS a la familia de `e` (ni `e` ni sus hermanos).
        ajen = [k for k in nombres if obj[k] != 0 and k != e and k not in r['herm'][e]]
        f0, f1 = fila_antes(int(t0)), fila_cerca(int(t0) + vent)
        a = [ok(f0, h) for h in herm]; d = [ok(f1, h) for h in herm]
        ga = [ok(f0, k) for k in ajen]; gd = [ok(f1, k) for k in ajen]
        if any(v is None for v in a + d) or not ajen or any(v is None for v in ga + gd):
            continue
        h_antes = sum(a) / len(a); h_desp = sum(d) / len(d)
        g_antes = sum(ga) / len(ga); g_desp = sum(gd) / len(gd)
        # ERR-48 (DIFERENCIA EN DIFERENCIAS): cuanto MENOS mejoraron los hermanos que el resto del mundo, en la
        # MISMA ventana y la MISMA corrida. Positivo = dano. Un organismo que solo aprende deprisa da ~0 aqui.
        dano = (g_desp - g_antes) - (h_desp - h_antes)
        apr = ok(f1, e)
        det[e] = dict(t0=int(t0), h_antes=round(h_antes, 3), h_desp=round(h_desp, 3),
                      g_antes=round(g_antes, 3), g_desp=round(g_desp, 3),
                      dano=round(dano, 4), dano_bruto=round(h_antes - h_desp, 3),
                      dano_mundo=round(g_desp - g_antes, 3), apr=apr, n_herm=len(herm), n_ajenos=len(ajen),
                      valida=int(bool(apr) and h_antes >= H_MIN))
    val = [v['dano'] for v in det.values() if v['valida']]
    return dict(colateral_n=(round(float(np.mean(val)), 4) if len(val) >= 2 else None),   # ERR-49: con < 2 ventanas validas no esta definida
                n_valida=len(val),
                dano_bruto=(round(float(np.mean([v['dano_bruto'] for v in det.values()])), 4) if det else None),
                dano_mundo=(round(float(np.mean([v['dano_mundo'] for v in det.values()])), 4) if det else None),
                apr_tasa=(round(float(np.mean([bool(v['apr']) for v in det.values()])), 3) if det else None),
                h_antes_med=(round(float(np.mean([v['h_antes'] for v in det.values()])), 3) if det else None),
                n_ventanas=len(det), ventanas=det)


def resumen(brazo, seed, r):
    base = CF.resumen(brazo, seed, r, BRAZOS[brazo])
    if r.get('mundo') in (None, 'AB'):
        return base
    base.update(medidas_nuevas(r))
    base['costo'] = BRAZOS[brazo].get('costo')
    base.pop('cod0', None)                                    # ya cruzado en 401-420; el JSON no lo necesita dos veces
    return base


def tarea(args):
    if args[0] == 'ID':
        return CF.tarea(args)                                 # el arnes del bloque 1, sin copiar
    if args[0] == 'D':
        return CF.tarea(args)
    _, brazo, seed, Ti, nk, ktop, nkmax = args
    import organismo_familias as MF
    kw = dict(BRAZOS[brazo])
    if kw.get('mundo') != 'AB':
        kw.update(nk=nk, ktop=ktop, nkmax=nkmax)
    return resumen(brazo, seed, MF.run(seed, T=Ti, **kw))


def SHAS():
    d = CF.SHAS()
    d.update(preregistro_enm1=h16(os.path.join(AQUI, 'PREREGISTRO_bloque1_familias_enm1.md')),
             script_enm1=h16(os.path.abspath(__file__)))
    return d


def guarda():
    ok = CF.guarda_origen()
    s = h16(os.path.join(AQUI, 'organismo_familias.py'))
    if s != SHA_INSTRUMENTO:
        log(f"*** INSTRUMENTO CAMBIADO: organismo_familias.py es {s}, la identidad 43/43 se midio sobre "
            f"{SHA_INSTRUMENTO}. Repetir identidad_familias.py ANTES de correr (E7).")
        ok = False
    return ok


# ---------------------------------------------------------------- veredicto (umbrales EXACTOS del preregistro enm1)
def veredicto(res, SEEDS, diags):
    G = {b: {r['seed']: r for r in res if r['brazo'] == b} for b in BRAZOS_ACTIVOS}
    x = lambda b, c: {s: G.get(b, {}).get(s, {}).get(c) for s in SEEDS if s in G.get(b, {})}
    L = lambda b, c: list(x(b, c).values())
    V = {'umbrales': UMBRALES, 'dureza': DUREZA, 'costo': MUNDO['costo'], 'n_exc': N_EXC, 'h_min': H_MIN}

    V['alias'] = dict(pares_mediana=med([d['alias_pares'] for d in diags]),
                      semillas_con_alias=sum(d['alias_semilla'] for d in diags), n=len(diags),
                      U3_mediana=med([d['U3'] for d in diags]))

    u = UMBRALES['E1']
    m_exc, m_lin = med(L('EXC', 'deaths')), med(L('LIN', 'deaths'))
    V['E1'] = dict(muertes_EXC=m_exc, q_EXC=cuartiles(L('EXC', 'deaths')), muertes_LIN=m_lin,
                   q_LIN=cuartiles(L('LIN', 'deaths')), banda=[u['lo'], u['hi']],
                   frac_regalo_EXC=med(L('EXC', 'frac_regalo')), frac_regalo_LIN=med(L('LIN', 'frac_regalo')),
                   muertes_V14_ancla=med(L('V14', 'deaths')),
                   pasa=bool(m_exc is not None and m_lin is not None
                             and u['lo'] <= m_exc <= u['hi'] and u['lo'] <= m_lin <= u['hi']))

    u = UMBRALES['E2a']
    ce, cl = x('EXC', 'colateral_n'), x('LIN', 'colateral_n')
    n2 = cuenta(ce, cl, SEEDS, lambda a, b: a > b)            # un None NUNCA cuenta como victoria
    ub = UMBRALES['E2b']
    me = med(list(ce.values()))
    V['E2'] = dict(med_EXC=me, q_EXC=cuartiles(list(ce.values())), med_LIN=med(list(cl.values())),
                   q_LIN=cuartiles(list(cl.values())), n_pareado=n2,
                   censura_EXC=sum(1 for v in ce.values() if v is None),
                   censura_LIN=sum(1 for v in cl.values() if v is None),
                   A12=A12(list(ce.values()), list(cl.values())),
                   a_pasa=bool(n2 >= u['n_pasa']), a_refuta=bool(n2 <= u['n_refuta']),
                   b_pasa=bool(me is not None and me >= ub['pasa']),
                   b_refuta=bool(me is not None and me <= ub['refuta']))
    V['E2']['pasa'] = bool(V['E2']['a_pasa'] and V['E2']['b_pasa'])
    V['E2']['refuta'] = bool(V['E2']['a_refuta'] or V['E2']['b_refuta'])
    V['E2']['indeciso'] = bool(not V['E2']['pasa'] and not V['E2']['refuta'])

    u = UMBRALES['E3']
    nv = {b: med(L(b, 'n_valida')) for b in ('EXC', 'LIN', 'BAR', 'AZA') if b in G}
    cn = {b: med(L(b, 'colateral_n')) for b in ('EXC', 'LIN', 'BAR', 'AZA') if b in G}
    orden = []
    for b in ('AZA', 'BAR'):
        if b in cn:
            orden.append((f'colateral_n({b}) <= colateral_n(LIN)',
                          bool(cn[b] is not None and cn.get('LIN') is not None and cn[b] <= cn['LIN'])
                          or cn[b] is None))
    V['E3'] = dict(n_valida=nv, colateral_n=cn, orden=orden,
                   censurados={b: sum(1 for v in L(b, 'colateral_n') if v is None) for b in cn},
                   apr_tasa={b: med(L(b, 'apr_tasa')) for b in cn},
                   h_antes={b: med(L(b, 'h_antes_med')) for b in cn},
                   pasa=bool(nv.get('EXC') is not None and nv.get('LIN') is not None
                             and nv['EXC'] >= u['fam_min'] and nv['LIN'] >= u['fam_min']
                             and (nv.get('BAR') or 0) <= u['nofam_max'] and (nv.get('AZA') or 0) <= u['nofam_max']
                             and all(v for _, v in orden)))

    db = {b: med(L(b, 'dano_bruto')) for b in ('EXC', 'LIN', 'BAR', 'AZA') if b in G}
    V['E4'] = dict(dano_bruto=db,
                   no_ordena=bool(db.get('EXC') is not None
                                  and ((db.get('AZA') is not None and db['AZA'] >= db['EXC'])
                                       or (db.get('BAR') is not None and db['BAR'] >= db['EXC']))))

    V['E5'] = dict(w_var={b: med(L(b, 'w_var_med')) for b in cn}, nota=UMBRALES['E5']['frase'])
    V['linea_base'] = {b: dict(muertes=med(L(b, 'deaths')), q_muertes=cuartiles(L(b, 'deaths')),
                               frac_regalo=med(L(b, 'frac_regalo')), celdas=med(L(b, 'celdas')),
                               splits=med(L(b, 'splits')), colateral=med(L(b, 'colateral')),
                               omision=med(L(b, 'omision')), colateral_n=med(L(b, 'colateral_n')),
                               n_valida=med(L(b, 'n_valida')), dano_bruto=med(L(b, 'dano_bruto')),
                               dano_mundo=med(L(b, 'dano_mundo')),
                               apr_tasa=med(L(b, 'apr_tasa')), h_antes=med(L(b, 'h_antes_med')),
                               w_var=med(L(b, 'w_var_med')), exp_total=med(L(b, 'exp_total')),
                               retencion=med(L(b, 'retencion')),
                               exp_clase={c: med([(d or {}).get(c) for d in L(b, 'exp_clase')])
                                          for c in ('token', 'variante', 'excepcion', 'ventana')})
                       for b in BRAZOS_ACTIVOS if b in G}
    return V


def frase_final(V):
    if not V['E1']['pasa']:
        return (f"E1 CAE: con dureza={DUREZA} las muertes quedan fuera de [20, 250] "
                f"(EXC {V['E1']['muertes_EXC']}, LIN {V['E1']['muertes_LIN']}). E2-E4 NO se leen. UNA correccion de "
                f"dureza con ERR-47 y semillas nuevas.")
    if not V['E3']['pasa']:
        return ("E3 CAE: la condicion no distingue familia real de familia falsa "
                f"(n_valida {V['E3']['n_valida']}). La medida sigue sin servir: primero el instrumento, nada se declara.")
    e2 = V['E2']
    if e2['pasa']:
        s = (f"EL MUNDO OBLIGA con una excepcion por token: aprender la variante que contradice a su familia estropea "
             f"la lectura de los hermanos (colateral_n {e2['med_EXC']} contra {e2['med_LIN']}, pareado {e2['n_pareado']}/20), "
             f"y donde no hay familia la pregunta ni siquiera esta definida (n_valida {V['E3']['n_valida']}). ")
    elif e2['refuta']:
        s = (f"EL MUNDO NO OBLIGA ni con una excepcion por token (colateral_n {e2['med_EXC']}, pareado "
             f"{e2['n_pareado']}/20): la linea pasa al MUNDO (retina mayor, mas variantes por token), NO al organismo. ")
    else:
        s = (f"INDECISO: el dano tiene direccion pero poca masa (colateral_n {e2['med_EXC']}, pareado "
             f"{e2['n_pareado']}/20). Se reporta y NO se declara nada. ")
    s += ("El control E4 confirma por que fallaba la medida vieja: sin condicionar por 'aprendio', dano_bruto "
          f"{V['E4']['dano_bruto']} premia la ignorancia. " if V['E4']['no_ordena'] else
          "OJO: E4 dice que la condicion `apr` SOBRA -- dano_bruto ya ordena solo, y eso es una simplificacion. ")
    return s + "20 semillas no cierran nada: piden replica en 461-480 (regla 12)."


# ---------------------------------------------------------------- humo (UN proceso, sin Pool)
def humo(nk, ktop, nkmax, Tb, sem):
    stamp = time.strftime('%Y%m%d_%H%M%S')
    _log['f'] = open(os.path.join(RAIZ, 'datos', f'familias_enm1_humo_{stamp}.log'), 'w', encoding='utf-8', newline='\n')
    _log['t0'] = time.time()
    log(f"HUMO de la ENMIENDA 1 (ERR-46), UN proceso, sin Pool. PREREGISTRO_bloque1_familias_enm1.md.")
    log(f"Semillas {sem}: NINGUNA de las 441-480 de la serie queda expuesta (E.14).")
    for k, v in SHAS().items():
        log(f"    sha {k:24s} {v}")
    log(f"    origenes e instrumento verificados -> {'OK' if guarda() else 'FALLA'}")
    log(f"    n_exc={N_EXC}  dureza={DUREZA} (costo={MUNDO['costo']}, tronco {COSTO_TRONCO})  log_cada={LOG_CADA}  "
        f"h_min={H_MIN}  crit={CRIT}")
    log(f"    brazos {[b for b in BRAZOS_ACTIVOS if b != 'V14']} (+ ancla V14)")

    log("1/3 IDENTIDAD: el instrumento no cambia, asi que basta su tripwire de sha (E7) + 3 casos del arnes.")
    ident = []
    for cual in ('A', 'P', 'L'):
        etiq, ref, kwref, kwmf, debe, Tc = CF.CASOS_ID[cual]
        CF.CASOS_ID[cual] = (etiq, ref, kwref, kwmf, debe, 5000)
        for s in sem:
            ident.append(CF.tarea(('ID', cual, s, nk, ktop, nkmax)))
        g = [r for r in ident if r['cual'] == cual]
        log(f"    {etiq:52s} {sum(r['ok'] for r in g)}/{len(g)}")
        CF.CASOS_ID[cual] = (etiq, ref, kwref, kwmf, debe, Tc)
    log(f"  IDENTIDAD {sum(r['ok'] for r in ident)}/{len(ident)} (el arnes completo, 43/43, en identidad_familias.py)")

    log("2/3 DIAGNOSTICO ESTRUCTURAL (T = 0, antes de simular).")
    diags = []
    for s in sem:
        d = CF.diagnostico(s, nk, ktop, MUNDO); diags.append(d)
        log(f"    semilla {s}: alias_pares {d['alias_pares']:.5f}  U3 {d['U3']}")

    log(f"3/3 UNA corrida por brazo y semilla, T={Tb}, brazos EXC/LIN/AZA/BAR ({4*len(sem)} corridas de un proceso).")
    res, t_b = [], {}
    for b in [x for x in BRAZOS_ACTIVOS if x != 'V14']:
        t_b[b] = 0.0
        for s in sem:
            t1 = time.time(); r = tarea(('R', b, s, Tb, nk, ktop, nkmax)); t_b[b] += time.time() - t1
            res.append(r)
        t_b[b] = round(t_b[b] / len(sem), 2)
        g = [r for r in res if r['brazo'] == b]
        log(f"    {b:4s} {t_b[b]:5.2f} s  colateral_n {[r['colateral_n'] for r in g]}  n_valida {[r['n_valida'] for r in g]}  "
            f"dano_bruto {[r['dano_bruto'] for r in g]}  apr {[r['apr_tasa'] for r in g]}  "
            f"h_antes {[r['h_antes_med'] for r in g]}")
        log(f"          muertes {[r['deaths'] for r in g]}  regalo {[r['frac_regalo'] for r in g]}  "
            f"celdas {[r['celdas'] for r in g]}  colateral(viejo) {[r['colateral'] for r in g]}  "
            f"w_var {[r['w_var_med'] for r in g]}  exp_clase {[r['exp_clase'] for r in g][0]}")

    seg = sum(t_b.values()) / max(len(t_b), 1) * (T / Tb)
    n_corr = (len(ORDEN) - 1) * N_SEM
    log(f"ESTIMACION de la serie: {n_corr} corridas de {T} pasos, ~{seg:.1f} s/corrida en serie -> "
        f"~{n_corr*seg/N_PARALELO/60:.1f} min de pared con Pool({N_PARALELO}).")
    log("HUMO: numeros observados, sin ajustar nada. n=2 y semillas vistas: NO son evidencia (E.14).")

    dj = os.path.join(RAIZ, 'datos', f'familias_enm1_humo_{stamp}.json')
    with open(dj, 'w', encoding='utf-8') as f:
        json.dump(dict(meta=dict(fecha=time.strftime('%Y-%m-%dT%H:%M:%S'), tipo='humo_enm1', err='ERR-46',
                                 T_brazo=Tb, semillas=sem, T_serie=T, nk=nk, ktop=ktop, nkmax=nkmax,
                                 n_exc=N_EXC, dureza=DUREZA, costo=MUNDO['costo'], log_cada=LOG_CADA, h_min=H_MIN,
                                 brazos=N(BRAZOS), umbrales=UMBRALES, shas=SHAS(), segundos_por_brazo=t_b,
                                 python=platform.python_version(), numpy=np.__version__),
                       identidades=ident, diagnostico=diags, brazos=res), f, ensure_ascii=False, default=str)
    log(f"datos -> {os.path.basename(dj)}  sha256_16 = {h16(dj)}")
    _log['f'].close()


# ---------------------------------------------------------------- escalera de dureza (ERR-47, regla FIJA)
ESCALERA = (2, 4, 6)


def escalera(nk, ktop, nkmax, Tb, sem):
    """ERR-47, ADENDA A del preregistro enm1. Regla escrita ANTES de correr: se prueba `dureza` en {2, 4, 6} sobre el
    brazo de CONTROL (LIN) y las semillas del humo (1-2, nunca las de la serie), y se toma el MENOR cuya mediana de
    muertes caiga en [20, 250]. Si ninguno cae, `costo` NO tiene regimen intermedio en este mundo: la dureza se busca
    por ESCASEZ (nobj) en un preregistro nuevo con ERR nuevo, y la serie 441-460 no se corre. No se interpola."""
    import organismo_familias as MF
    stamp = time.strftime('%Y%m%d_%H%M%S')
    _log['f'] = open(os.path.join(RAIZ, 'datos', 'familias_enm1_escalera_%s.log' % stamp), 'w',
                     encoding='utf-8', newline='\n')
    _log['t0'] = time.time()
    lo, hi = UMBRALES['E1']['lo'], UMBRALES['E1']['hi']
    log("ESCALERA DE DUREZA (ERR-47), UN proceso, sin Pool. Regla FIJA escrita antes de correr: dureza en %s, "
        "brazo LIN (control), semillas %s; se toma el MENOR con mediana de muertes en [%d, %d]." % (ESCALERA, sem, lo, hi))
    log("    disparo: dureza=12 dio muertes LIN [699, 754] y EXC [939, 1268] (humo previo, fuera de banda).")
    filas = []
    for dz in ESCALERA:
        kw = dict(BRAZOS['LIN'], costo=round(COSTO_TRONCO * dz, 6), nk=nk, ktop=ktop, nkmax=nkmax)
        ms = [MF.run(s, T=Tb, **kw)['deaths'] for s in sem]
        dentro = bool(lo <= float(np.median(ms)) <= hi)
        filas.append(dict(dureza=dz, costo=kw['costo'], muertes=ms, mediana=float(np.median(ms)), dentro=dentro))
        log("    dureza %2d (costo %s): muertes %s  mediana %s  %s"
            % (dz, kw['costo'], ms, filas[-1]['mediana'], 'DENTRO de banda' if dentro else 'fuera'))
    eleg = next((f for f in filas if f['dentro']), None)
    if eleg:
        log("REGLA -> dureza = %d (costo %s), el MENOR de %s dentro de banda." % (eleg['dureza'], eleg['costo'], ESCALERA))
    else:
        log("REGLA -> NINGUNO de %s cae en banda: `costo` no tiene regimen intermedio en este mundo. La dureza se "
            "busca por ESCASEZ (nobj) en un preregistro nuevo con ERR nuevo; la serie NO se corre." % (ESCALERA,))
    dj = os.path.join(RAIZ, 'datos', 'familias_enm1_escalera_%s.json' % stamp)
    with open(dj, 'w', encoding='utf-8') as f:
        json.dump(dict(meta=dict(fecha=time.strftime('%Y-%m-%dT%H:%M:%S'), tipo='escalera_dureza', err='ERR-47',
                                 regla='menor dureza de %s con mediana de muertes de LIN en [%d,%d]' % (ESCALERA, lo, hi),
                                 escalera=list(ESCALERA), banda=[lo, hi], T=Tb, semillas=sem, brazo='LIN',
                                 shas=SHAS(), python=platform.python_version(), numpy=np.__version__),
                       filas=filas, elegido=eleg), f, ensure_ascii=False, default=str)
    log("datos -> %s  sha256_16 = %s" % (os.path.basename(dj), h16(dj)))
    _log['f'].close()
    return eleg


# ---------------------------------------------------------------- principal
if __name__ == '__main__':
    arg = lambda n, d: (type(d)(sys.argv[sys.argv.index(n) + 1]) if n in sys.argv else d)
    nk, ktop, nkmax = arg('--nk', 30), arg('--k', 3), arg('--nkmax', 90)
    if '--dureza' in sys.argv:
        DUREZA = arg('--dureza', DUREZA)
        MUNDO['costo'] = round(COSTO_TRONCO * DUREZA, 6)
        for b in BRAZOS:
            if BRAZOS[b].get('mundo') != 'AB':
                BRAZOS[b]['costo'] = MUNDO['costo']
    if '--escalera' in sys.argv:
        escalera(nk, ktop, nkmax, arg('--T', T), [1, 2]); sys.exit(0)
    if '--humo' in sys.argv:
        humo(nk, ktop, nkmax, arg('--T', T), [1, 2]); sys.exit(0)

    import multiprocessing as mp
    mp.set_start_method('spawn', force=True)
    T = arg('--T', T)
    desde = arg('--desde', DESDE)
    SEEDS = list(range(desde, desde + N_SEM))
    stamp = time.strftime('%Y%m%d_%H%M%S')
    _log['f'] = open(os.path.join(RAIZ, 'datos', f'familias_enm1_s{SEEDS[0]}-{SEEDS[-1]}_{stamp}.log'),
                     'w', encoding='utf-8', newline='\n')
    _log['t0'] = time.time()
    log(f"ARRANQUE BLOQUE 1 ENMIENDA 1 (ERR-46): brazos {BRAZOS_ACTIVOS}, semillas {SEEDS[0]}-{SEEDS[-1]}, T={T}. "
        f"Pool({N_PARALELO}).")
    log(f"n_exc={N_EXC}  dureza={DUREZA} (costo={MUNDO['costo']})  log_cada={LOG_CADA}  h_min={H_MIN}")
    log("El instrumento NO cambia (organismo_familias.py b9dd561a0cf056b8, identidad 43/43). Las medidas nuevas se "
        "calculan en el runner desde `log` (lo que lee la boca) y `t_exc`.")
    for k, v in SHAS().items():
        log(f"    sha {k:24s} {v}")
    if not guarda():
        sys.exit(1)
    try:
        ps = subprocess.run(['powershell', '-NoProfile', '-Command',
                             "Get-CimInstance Win32_Process | Where-Object { $_.Name -like 'python*' } | "
                             "ForEach-Object { \"$($_.ProcessId) $($_.CommandLine)\" }"],
                            capture_output=True, text=True, timeout=60).stdout.strip().splitlines()
    except Exception as e:
        ps = [f"(no se pudo listar: {e})"]
    log(f"REGLA 11 — procesos python vivos ({len(ps)}), este es pid {os.getpid()}")

    V, res = {}, []
    with mp.Pool(N_PARALELO) as pool:
        ctrl = [('ID', c, s, nk, ktop, nkmax) for c in CF.CASOS_ID for s in CF.SEMILLAS_ID]
        log(f"ETAPA 1/3 — IDENTIDAD, subconjunto critico del arnes ({len(ctrl)} comprobaciones). (L) y (M) DEBEN fallar.")
        rc = pool.map(CF.tarea, ctrl, chunksize=1)
        for cual in CF.CASOS_ID:
            g = [r for r in rc if r['cual'] == cual]
            log(f"    {CF.CASOS_ID[cual][0]:52s} {sum(r['ok'] for r in g)}/{len(g)}"
                + ("" if all(r['ok'] for r in g) else f"   difieren {g[0]['difieren']}"))
            V[f'ID_{cual}'] = all(r['ok'] for r in g)
        V['G_IDENTIDAD'] = bool(all(V[f'ID_{c}'] for c in CF.CASOS_ID))
        log(f"  IDENTIDAD {sum(r['ok'] for r in rc)}/{len(rc)}")
        if not V['G_IDENTIDAD']:
            log("*** GUARDA DE IDENTIDAD FALLIDA (E7). Se para.")
            sys.exit(1)

        log(f"ETAPA 2/3 — DIAGNOSTICO ESTRUCTURAL, ANTES de simular ({len(SEEDS)} semillas, T = 0).")
        diags = pool.map(CF.tarea, [('D', s, nk, ktop) for s in SEEDS], chunksize=1)
        log(f"    alias por par mediana {med([d['alias_pares'] for d in diags])}  "
            f"semillas con algun par identico {sum(d['alias_semilla'] for d in diags)}/{len(diags)}  "
            f"U3 mediana {med([d['U3'] for d in diags])}")

        tr = [('R', b, s, T, nk, ktop, nkmax) for b in BRAZOS_ACTIVOS for s in SEEDS]
        log(f"ETAPA 3/3 — principal: {len(tr)} corridas de {T} pasos.")
        for i, r in enumerate(pool.imap_unordered(tarea, tr, chunksize=1), 1):
            res.append(r)
            if i % 20 == 0 or i == len(tr):
                log(f"          {i}/{len(tr)}")

    log()
    log("ANALISIS — medianas y cuartiles por brazo, y despues los umbrales EXACTOS del preregistro enm1 (ERR-31).")
    V.update(veredicto(res, SEEDS, diags))
    for b, d in V['linea_base'].items():
        log(f"    {b:4s} muertes {d['muertes']} q{d['q_muertes']}  regalo {d['frac_regalo']}  "
            f"colateral_n {d['colateral_n']}  n_valida {d['n_valida']}  dano_bruto {d['dano_bruto']}  "
            f"apr {d['apr_tasa']}  h_antes {d['h_antes']}  colateral(viejo) {d['colateral']}  w_var {d['w_var']}  "
            f"celdas {d['celdas']}  exp_clase {d['exp_clase']}")
    ver = frase_final(V)
    log(); log(f"VEREDICTO: {ver}")

    meta = dict(fecha=time.strftime('%Y-%m-%dT%H:%M:%S'), err='ERR-46', semillas=SEEDS, T=T, nk=nk, ktop=ktop,
                nkmax=nkmax, n_exc=N_EXC, dureza=DUREZA, costo=MUNDO['costo'], log_cada=LOG_CADA, h_min=H_MIN,
                brazos={b: N(BRAZOS[b]) for b in BRAZOS_ACTIVOS}, veredicto=ver, veredictos=N(V),
                identidades=rc, diagnostico=diags, procesos_python=ps, shas=SHAS(),
                python=platform.python_version(), numpy=np.__version__)
    dj = os.path.join(RAIZ, 'datos', f'familias_enm1_s{SEEDS[0]}-{SEEDS[-1]}_{stamp}.json')
    with open(dj, 'w', encoding='utf-8') as f:
        json.dump(dict(meta=meta, principal=res), f, ensure_ascii=False, default=str)
    log(f"datos -> {os.path.basename(dj)}  sha256_16 = {h16(dj)}")
    _log['f'].close()
