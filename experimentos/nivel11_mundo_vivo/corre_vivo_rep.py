"""PROPOSITO Y REPRODUCCION COMO MEDIDA (mundo vivo, peldano 2; linea F) — ejecuta PREREGISTRO_reproduccion.md
(escrito ANTES de correr; su sha va en el meta del JSON). Instrumento organismo_vivo_rep.py (por anclas desde
organismo_vivo.py, que solo se lee; a su vez desde el tronco congelado v14.1). REGLA 10: log desde el arranque, con
fsync, una linea por etapa con marca de tiempo.

    python experimentos/nivel11_mundo_vivo/corre_vivo_rep.py [--desde 221] [--T 100000] [--brazos VIVO,REP,...]
    python experimentos/nivel11_mundo_vivo/corre_vivo_rep.py --humo    (UN proceso, sin Pool, 6 corridas: lo corre el disenador)

ERR-31 (el runner lee la LETRA del preregistro): todos los umbrales de P-R1..P-R8 estan en UMBRALES, cada uno con su frase.
ERR-37 (lecciones): descendientes, pasos_viables, muertes y tasas SACIADO son integrales de trayectoria -> NO se parean
por semilla: A12 sobre los 400 pares, razon de medianas, cuartiles. Se parea SOLO lo aprendido (tabla de la fila 2,
xor01, celdas estrictas). Ningun `max` sobre lecturas; un None nunca cuenta como victoria.

Etapas con Pool (las corre el COORDINADOR, reglas 3 y 11):
  1/2 IDENTIDAD interna, 5 casos x 3 semillas (15 comprobaciones, T=20000):
      (A) apagada == organismo_vivo VIVO · (B) cadena: rep(vivo=0) == organismo_v14 · (C) medida de solo lectura: las
      claves viejas == organismo_vivo VIVO · (D) tercera necesidad != organismo_vivo (DEBE fallar) · (E) CUELLO != (DEBE fallar).
      Si no es 15/15, ABORTA.
  2/2 principal: 9 brazos x 20 semillas (221-240; replica 241-260 con --desde 241).

Brazos: VIVO, UNA_NEC, ESCALAR, BARAJA_CON, BARAJA_POL (los del bloque anterior + la MEDIDA de solo lectura),
REP_SIN_COSTE (tercera necesidad, sin pagar), REP (tercera necesidad, paga 0.4/0.4 por descendiente), CUELLO (control:
saciado enruta a la fila del recurso mas escaso, sin fila nueva; el humo mostro que asi el veneno le queda invisible) y
CUELLO_MIN (ERR-39, anadido tras el humo y ANTES del bloque: el control que puede ganar — saciado, la boca
lee el MINIMO de las dos filas primarias; sin fila nueva, sin aprendizaje nuevo). P-R5 se desdobla en P-R5 (CUELLO, letra
original) y P-R5b (CUELLO_MIN, mismos umbrales); P-R5b es la que decide si la tercera fila aporta.
El humo de registro (vivo_rep_humo_20260918_090014, instrumento ed31d9b989b93307) NO se repite: la construccion final es
bit a bit la v1 en los brazos que el humo corrio (arnes, caso H).
Subconjunto preregistrado (regla 10): semillas ALIAS = algun solapamiento de codigos = 3 (diagnostico_codigos.py, sin
simular); se reporta el conjunto completo y al lado las LIMPIAS.

Vocabulario (regla 6): "tercera necesidad", "cuello de botella", "saciado rechaza", "ventanas de viabilidad /
descendientes viables", "paga el coste". NO se dice "quiere", "tiene proposito", "se reproduce" (nada nace), "planifica".
"""
import sys, os, json, time, hashlib, platform, subprocess, statistics as st
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
import numpy as np

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
sys.path[:0] = [AQUI, os.path.join(RAIZ, 'organismo')]   # organismo/ PRIMERO (ERR-28)

import mini_vivo as MV            # brazos del nucleo, celdas informativas, XOR y lee(): NO se copian
import corre_vivo as CV           # tabla_error, celdas_estrictas, N, h16: NO se copian
import diagnostico_codigos as DC  # alias de codigo, estructural

T = 100000
T_ID = 20000
N_PARALELO = 14
N_SEM = 20
DESDE = 221
SEMILLAS_ID = [1, 2, 3]
SHA_V14_ESPERADO = 'feefc88b1fd8d434'    # organismo/organismo_v14.py (v14.1): origen del origen
SHA_VIVO_ESPERADO = '20c0961c79de8825'   # organismo_vivo.py: origen por anclas del instrumento

MED = dict(reproduccion=1, rep_mide=1, rep_X=500, rep_umbral=1.0, rep_coste=0.0)   # la MEDIDA, de solo lectura
BRAZOS = {
    'VIVO':          dict(MV.BRAZOS['VIVO'], **MED),
    'UNA_NEC':       dict(MV.BRAZOS['UNA_NEC'], **MED),
    'ESCALAR':       dict(MV.BRAZOS['ESCALAR'], **MED),
    'BARAJA_CON':    dict(MV.BRAZOS['BARAJA_CON'], **MED),
    'BARAJA_POL':    dict(MV.BRAZOS['BARAJA_POL'], **MED),
    'REP_SIN_COSTE': dict(MV.CUERPO, n_nec=3, rep_nec=1, **MED),
    'REP':           dict(dict(MV.CUERPO, n_nec=3, rep_nec=1, **MED), rep_coste=0.4),
    'CUELLO':        dict(MV.CUERPO, n_nec=2, rep_cuello=1, **MED),
    'CUELLO_MIN':    dict(MV.CUERPO, n_nec=2, rep_cuello=2, **MED),   # ERR-39: anadido tras el humo, antes del bloque
}
ORDEN = ['VIVO', 'REP_SIN_COSTE', 'REP', 'CUELLO', 'CUELLO_MIN', 'UNA_NEC', 'ESCALAR', 'BARAJA_CON', 'BARAJA_POL']
BRAZOS_ACTIVOS = list(ORDEN)
NUEVAS_REP = {'descendientes', 'pasos_viables', 'desc_q', 't_desc', 'sac_mord', 'sac_dec', 'rep'}
CASOS_ID = {   # (etiqueta, referencia, kw de la referencia, kw de organismo_vivo_rep, debe_diferir, claves que se quitan)
    'A': ("(A) apagada (reproduccion=0) == organismo_vivo VIVO", 'vivo', MV.BRAZOS['VIVO'],
          dict(MV.BRAZOS['VIVO'], reproduccion=0), False, ()),
    'B': ("(B) cadena: rep(vivo=0, n_nec=1) == organismo_v14", 'v14', dict(), dict(vivo=0, n_nec=1), False, ()),
    'C': ("(C) medida de solo lectura: claves viejas == organismo_vivo VIVO", 'vivo', MV.BRAZOS['VIVO'],
          BRAZOS['VIVO'], False, NUEVAS_REP),
    'D': ("(D) tercera necesidad != organismo_vivo VIVO (DEBE fallar)", 'vivo', MV.BRAZOS['VIVO'],
          BRAZOS['REP_SIN_COSTE'], True, NUEVAS_REP),
    'E': ("(E) CUELLO != organismo_vivo VIVO (DEBE fallar)", 'vivo', MV.BRAZOS['VIVO'], BRAZOS['CUELLO'], True, NUEVAS_REP),
}

# ---------------------------------------------------------------- UMBRALES: la LETRA del preregistro (ERR-31)
UMBRALES = {
    'PR1': dict(frase="la medida ordena como la supervivencia: A12(desc VIVO > UNA_NEC) >= 0.70; A12(UNA_NEC > BARAJA_POL) "
                      ">= 0.80; A12(VIVO > ESCALAR) >= 0.70; A12(VIVO > BARAJA_CON) >= 0.70 (cualquiera < 0.50: la medida se tira)",
                una=0.70, pol=0.80, esc=0.70, con=0.70, tira=0.50),
    'PR2': dict(frase="saciado, la sal: mediana sac_tasa[D] VIVO >= 0.60; REP_SIN_COSTE <= 0.25; REP <= 0.25; "
                      "A12(REP_SIN_COSTE < VIVO) >= 0.90 (refuta: REP_SIN_COSTE >= 0.40)",
                vivo_min=0.60, rep_max=0.25, a12=0.90, refuta=0.40),
    'PR3': dict(frase="sin pagar: desc REP_SIN_COSTE vs VIVO A12 >= 0.75 y razon de medianas >= 1.5; pasos_viables A12 >= 0.75, "
                      "razon >= 1.3 (refuta: A12 <= 0.60)",
                a12=0.75, razon=1.5, a12_pv=0.75, razon_pv=1.3, refuta=0.60),
    'PR4': dict(frase="pagando: desc REP >= 0.5 x REP_SIN_COSTE (razon de medianas) y A12(REP > VIVO) >= 0.60 (refuta: < 0.50)",
                frac=0.5, a12=0.60, refuta=0.50),
    'PR5': dict(frase="Occam (CUELLO): desc A12(REP_SIN_COSTE > CUELLO) >= 0.65; sac_tasa[D]: A12(REP_SIN_COSTE < CUELLO) >= 0.75 y "
                      "A12(CUELLO < VIVO) >= 0.75; mediana CUELLO <= 0.50 (refuta: A12 desc <= 0.55 -> la tercera fila sobra)",
                a12_desc=0.65, a12_sal=0.75, cuello_max=0.50, refuta=0.55),
    'PR5b': dict(frase="Occam, el control que puede ganar (CUELLO_MIN; ERR-39): DECIDE desc A12(REP_SIN_COSTE > CUELLO_MIN) "
                       ">= 0.65 (<= 0.55: la tercera fila sobra); ademas CUELLO_MIN veta la sal como REP (mediana sac_tasa[D] <= 0.25; no se "
                       "predice orden entre los dos) y la FIRMA de la tercera fila es el valor positivo aprendido de comida y agua: sac_tasa[A] y "
                       "sac_tasa[C] A12(REP_SIN_COSTE > CUELLO_MIN) >= 0.75 (0.98 contra 0.84 por la ecuacion de la boca)",
                 a12_desc=0.65, sal_max=0.25, a12_ac=0.75, refuta=0.55),
    'PR6': dict(frase="seguridad: en REP y REP_SIN_COSTE xor01 = 1.0 en >= 18/20, celdas estrictas 4/4 en >= 18/20, exp_tabla "
                      "<= 1.5 x VIVO; muertes A12(REP_SIN_COSTE < VIVO) >= 0.50; REP <= 1.5 x VIVO (razon de medianas)",
                n_min=18, f_exp=1.5, a12_mu=0.50, f_mu=1.5),
    'PR7': dict(frase="tabla de la fila 2: A >= +0.3, C >= +0.3, B <= -1.0, D <= -1.0 en >= 18/20 (REP_SIN_COSTE y REP)",
                pos=0.3, neg=-1.0, n_min=18),
    'PR8': dict(frase="coste en el mundo: exposiciones[D] REP_SIN_COSTE <= 3 x VIVO y exposiciones[A] >= 0.7 x VIVO (medianas)",
                f_sal=3.0, f_com=0.7),
}
HUMO = {   # predicciones del humo (seccion 10), escritas antes de lanzarlo
    'H1': "desc de VIVO en [1, 150] en 2/2", 'H2': "desc REP_SIN_COSTE > VIVO en 2/2 (misma semilla)",
    'H3': "sac_tasa[D]: VIVO >= 0.60 y REP_SIN_COSTE <= 0.25 en 2/2",
    'H4': "W_nec[2] de REP_SIN_COSTE con signos {A+, B-, C+, D-} y |W| >= 0.3 en 2/2",
    'H5': "desc REP >= 0.5 x REP_SIN_COSTE (semilla 1)", 'H6': "sac_tasa[D] de CUELLO entre REP_SIN_COSTE y VIVO (semilla 1)",
}

_log = {'f': None, 't0': time.time()}


def log(msg=""):
    linea = f"[{time.strftime('%H:%M:%S')} +{time.time()-_log['t0']:7.1f}s] {msg}"
    print(linea, flush=True)
    if _log['f']:
        _log['f'].write(linea + "\n"); _log['f'].flush(); os.fsync(_log['f'].fileno())


h16, N = CV.h16, CV.N


def med(xs):
    xs = [x for x in xs if x is not None]
    return round(float(st.median(xs)), 3) if xs else None


def razon(x, y):
    return None if (x is None or not y) else round(x / y, 3)


def A12(a, b):
    """P(a > b) + 0.5 P(a = b) sobre TODOS los pares (n x m). Distribucion libre, sin parear (ERR-37b)."""
    a = [x for x in a if x is not None]; b = [y for y in b if y is not None]
    if not a or not b:
        return None
    return round(sum((x > y) + 0.5 * (x == y) for x in a for y in b) / (len(a) * len(b)), 3)


def q(xs, k, metodo='exclusive'):
    xs = [x for x in xs if x is not None]
    return round(st.quantiles(xs, n=4, method=metodo)[k], 1) if len(xs) >= 4 else None


def ge(x, u):
    return bool(x is not None and x >= u)


def le(x, u):
    return bool(x is not None and x <= u)


# ---------------------------------------------------------------- medidas por corrida
def resumen(brazo, seed, r, kw, Ti):
    o = MV.lee(r, kw)
    err, peor = CV.tabla_error(r, kw)
    ok, det = CV.celdas_estrictas(r, kw, o)
    sac = {k: (round(r['sac_mord'][k] / r['sac_dec'][k], 3) if r['sac_dec'][k] >= 20 else None) for k in MV.EST}
    return dict(tipo='R', brazo=brazo, seed=seed, T=Ti,
                descendientes=r['descendientes'], pasos_viables=r['pasos_viables'],
                frac_viable=round(r['pasos_viables'] / Ti, 4), desc_q=r['desc_q'], t_desc=r['t_desc'][:60],
                sac_tasa=sac, sac_dec=r['sac_dec'], sac_mord=r['sac_mord'],
                W_rep=(r['W_nec'][2] if r['n_nec'] == 3 else None),
                xor01=o['xor01'], xor_celdas=o['xor_celdas'], contraste=o['contraste'],
                exp_celda=o['exp_celda'], exp_tabla=o['exp_tabla'], celdas_ok_estricto=ok, celdas_detalle=det,
                err_tabla=err, err_peor=peor, exposiciones=o['exposiciones'], W_nec=o['W_nec'],
                deaths=o['deaths'], muertes_nec=o['muertes_nec'], celdas=o['celdas'], splits=o['splits'])


def tarea(args):
    tipo = args[0]
    if tipo == 'ID':
        _, cual, seed, Ti = args
        import organismo_v14 as V14, organismo_vivo as VV, organismo_vivo_rep as VR
        etiq, ref, kwa, kwb, debe, quitar = CASOS_ID[cual]
        a = (V14.run(seed, T=Ti, **kwa) if ref == 'v14' else VV.run(seed, T=Ti, **kwa))
        b = VR.run(seed, T=Ti, **kwb)
        bb = {k: v for k, v in b.items() if k not in quitar}
        dif = [k for k in a if k in bb and N(a[k]) != N(bb[k])]
        falta = [k for k in a if k not in bb]
        extra = [k for k in bb if k not in a]
        igual = not dif and not falta and not extra
        return dict(tipo='ID', cual=cual, etiqueta=etiq, seed=seed, identico=igual, debe_diferir=debe,
                    ok=bool(igual != debe), difieren=dif[:6], faltan=falta, extra=extra[:6])
    _, brazo, seed, Ti = args
    import organismo_vivo_rep as VR
    kw = BRAZOS[brazo]
    return resumen(brazo, seed, VR.run(seed, T=Ti, **kw), kw, Ti)


SHAS = lambda: dict(
    preregistro=h16(os.path.join(AQUI, 'PREREGISTRO_reproduccion.md')),
    script=h16(os.path.abspath(__file__)),
    constructor=h16(os.path.join(AQUI, 'construye_vivo_rep.py')),
    instrumento=h16(os.path.join(AQUI, 'organismo_vivo_rep.py')),
    arnes=h16(os.path.join(AQUI, 'identidad_vivo_rep.py')),
    origen_organismo_vivo=h16(os.path.join(AQUI, 'organismo_vivo.py')),
    origen_organismo_v14=h16(os.path.join(RAIZ, 'organismo', 'organismo_v14.py')),
    mini=h16(os.path.join(AQUI, 'mini_vivo.py')), corre_vivo=h16(os.path.join(AQUI, 'corre_vivo.py')))


def guarda_origen():
    s = SHAS()
    ok = True
    if s['origen_organismo_v14'] != SHA_V14_ESPERADO:
        log(f"*** ORIGEN CAMBIADO: organismo_v14.py es {s['origen_organismo_v14']}, se esperaba {SHA_V14_ESPERADO}."); ok = False
    if s['origen_organismo_vivo'] != SHA_VIVO_ESPERADO:
        log(f"*** ORIGEN CAMBIADO: organismo_vivo.py es {s['origen_organismo_vivo']}, se esperaba {SHA_VIVO_ESPERADO}."); ok = False
    if not ok:
        log("    Reconstruir por anclas (construye_vivo_rep.py) y repetir el arnes ANTES de correr.")
    return ok


def alias_de(seeds):
    return [s for s in seeds if any(v >= 3 for v in DC.solapamientos(s).values())]


# ---------------------------------------------------------------- veredicto (umbrales EXACTOS del preregistro)
def veredicto(res, SEEDS, log=log):
    G = {b: {r['seed']: r for r in res if r['brazo'] == b} for b in BRAZOS_ACTIVOS}
    alias = alias_de(SEEDS)
    limpias = [s for s in SEEDS if s not in alias]
    V = {'umbrales': UMBRALES, 'alias': alias, 'limpias': limpias}
    V['completo'] = serie(G, SEEDS, "CONJUNTO COMPLETO", log)
    if alias and len(limpias) >= 0.6 * len(SEEDS):   # regla 10: el subconjunto se hace siempre y se reporta al lado
        V['limpias_veredicto'] = serie(G, limpias, f"SUBCONJUNTO LIMPIAS (sin {alias}; regla 10)", log)
    return V


def serie(G, S, etiqueta, log):
    v = lambda b, f: [f(G[b][s]) for s in S if s in G.get(b, {})]
    desc = lambda b: v(b, lambda r: r['descendientes'])
    pv = lambda b: v(b, lambda r: r['pasos_viables'])
    mu = lambda b: v(b, lambda r: r['deaths'])
    sal = lambda b: v(b, lambda r: r['sac_tasa']['D'])
    hay = lambda *bs: all(b in G and any(s in G[b] for s in S) for b in bs)
    log(f"--- {etiqueta}: semillas {S[0]}-{S[-1]} (n={len(S)}) ---")
    med_ = {}
    for b in BRAZOS_ACTIVOS:
        g = [G[b][s] for s in S if s in G.get(b, {})]
        if not g:
            continue
        wr = [r['W_rep'] for r in g if r['W_rep'] is not None]
        med_[b] = dict(n=len(g), desc=med(desc(b)), desc_q25=q(desc(b), 0), desc_q75=q(desc(b), 2),
                       pasos_viables=med(pv(b)), frac_viable=med([r['frac_viable'] for r in g]),
                       sac_tasa={k: med([r['sac_tasa'][k] for r in g]) for k in MV.EST},
                       sac_n={k: sum(r['sac_tasa'][k] is not None for r in g) for k in MV.EST},
                       W_rep=({k: med([w[k] for w in wr]) for k in MV.EST} if wr else None),
                       xor01=med([r['xor01'] for r in g]), celdas_ok=med([r['celdas_ok_estricto'] for r in g]),
                       exp_tabla=med([r['exp_tabla'] for r in g]), err_peor=med([r['err_peor'] for r in g]),
                       muertes=med(mu(b)), muertes_E=med([r['muertes_nec'][0] for r in g]),
                       muertes_agua=med([r['muertes_nec'][1] for r in g]),
                       exposiciones={k: med([r['exposiciones'][k] for r in g]) for k in MV.EST},
                       celdas=med([r['celdas'] for r in g]), splits=med([r['splits'] for r in g]))
        m = med_[b]
        log(f"   {b:13s} n={m['n']:<3d} desc {m['desc']} [q25 {m['desc_q25']}, q75 {m['desc_q75']}]  viable {m['frac_viable']}"
            f"  muertes {m['muertes']} [E {m['muertes_E']}, agua {m['muertes_agua']}]  xor01 {m['xor01']}  celdas {m['celdas_ok']}/4"
            f"  exp_tabla {m['exp_tabla']}  err_peor {m['err_peor']}")
        log(f"        saciado tasa {m['sac_tasa']} (n con >=20 decisiones {m['sac_n']})   W fila 2 {m['W_rep']}   exposiciones {m['exposiciones']}")
    P = {'medianas': med_}

    u = UMBRALES['PR1']
    if hay('VIVO', 'UNA_NEC', 'BARAJA_POL', 'ESCALAR', 'BARAJA_CON'):
        a = dict(una=A12(desc('VIVO'), desc('UNA_NEC')), pol=A12(desc('UNA_NEC'), desc('BARAJA_POL')),
                 esc=A12(desc('VIVO'), desc('ESCALAR')), con=A12(desc('VIVO'), desc('BARAJA_CON')))
        P['PR1'] = dict(**a, pasa=bool(ge(a['una'], u['una']) and ge(a['pol'], u['pol']) and ge(a['esc'], u['esc']) and ge(a['con'], u['con'])),
                        se_tira=bool(any(x is not None and x < u['tira'] for x in a.values())))
        log(f"   P-R1 {u['frase']}\n        -> A12 VIVO>UNA_NEC {a['una']}, UNA_NEC>BARAJA_POL {a['pol']}, VIVO>ESCALAR {a['esc']}, VIVO>BARAJA_CON {a['con']}"
            f"  {'PASA' if P['PR1']['pasa'] else ('SE TIRA LA MEDIDA' if P['PR1']['se_tira'] else 'NO (ordena debilmente)')}")

    u = UMBRALES['PR2']
    if hay('VIVO', 'REP_SIN_COSTE', 'REP'):
        mv, ms, mr = med(sal('VIVO')), med(sal('REP_SIN_COSTE')), med(sal('REP'))
        a = A12(sal('VIVO'), sal('REP_SIN_COSTE'))   # P(VIVO > REP_SIN_COSTE) = P(REP_SIN_COSTE < VIVO)
        P['PR2'] = dict(vivo=mv, rep_sin_coste=ms, rep=mr, a12=a,
                        pasa=bool(ge(mv, u['vivo_min']) and le(ms, u['rep_max']) and le(mr, u['rep_max']) and ge(a, u['a12'])),
                        refutada=bool(ms is not None and ms >= u['refuta']))
        log(f"   P-R2 {u['frase']}\n        -> medianas VIVO {mv}, REP_SIN_COSTE {ms}, REP {mr}; A12 {a}  "
            f"{'PASA' if P['PR2']['pasa'] else ('REFUTADA' if P['PR2']['refutada'] else 'NO')}")

    u = UMBRALES['PR3']
    if hay('VIVO', 'REP_SIN_COSTE'):
        a, r = A12(desc('REP_SIN_COSTE'), desc('VIVO')), razon(med(desc('REP_SIN_COSTE')), med(desc('VIVO')))
        ap, rp = A12(pv('REP_SIN_COSTE'), pv('VIVO')), razon(med(pv('REP_SIN_COSTE')), med(pv('VIVO')))
        P['PR3'] = dict(a12_desc=a, razon_desc=r, a12_pv=ap, razon_pv=rp,
                        q75_vivo=q(desc('VIVO'), 2), q25_rep=q(desc('REP_SIN_COSTE'), 0),
                        pasa=bool(ge(a, u['a12']) and ge(r, u['razon']) and ge(ap, u['a12_pv']) and ge(rp, u['razon_pv'])),
                        refutada=bool(a is not None and a <= u['refuta']))
        log(f"   P-R3 {u['frase']}\n        -> desc: A12 {a}, razon de medianas {r} (q75 VIVO {P['PR3']['q75_vivo']} / q25 REP_SIN_COSTE {P['PR3']['q25_rep']}); "
            f"pasos_viables: A12 {ap}, razon {rp}  {'PASA' if P['PR3']['pasa'] else ('REFUTADA' if P['PR3']['refutada'] else 'NO')}")

    u = UMBRALES['PR4']
    if hay('VIVO', 'REP_SIN_COSTE', 'REP'):
        f, a = razon(med(desc('REP')), med(desc('REP_SIN_COSTE'))), A12(desc('REP'), desc('VIVO'))
        P['PR4'] = dict(frac=f, a12=a, pasa=bool(ge(f, u['frac']) and ge(a, u['a12'])),
                        refutada=bool(a is not None and a < u['refuta']))
        log(f"   P-R4 {u['frase']}\n        -> REP / REP_SIN_COSTE {f}; A12(REP > VIVO) {a}  "
            f"{'PASA' if P['PR4']['pasa'] else ('REFUTADA (pagar deja peor)' if P['PR4']['refutada'] else 'NO concluyente')}")

    u = UMBRALES['PR5']
    if hay('VIVO', 'REP_SIN_COSTE', 'CUELLO'):
        ad = A12(desc('REP_SIN_COSTE'), desc('CUELLO'))
        as1, as2, mc = A12(sal('CUELLO'), sal('REP_SIN_COSTE')), A12(sal('VIVO'), sal('CUELLO')), med(sal('CUELLO'))
        P['PR5'] = dict(control='CUELLO', a12_desc=ad, a12_sal_rep_lt_ctl=as1, a12_sal_ctl_lt_vivo=as2, ctl_sal=mc,
                        desc_ctl=med(desc('CUELLO')), desc_rep=med(desc('REP_SIN_COSTE')),
                        pasa=bool(ge(ad, u['a12_desc']) and ge(as1, u['a12_sal']) and ge(as2, u['a12_sal']) and le(mc, u['cuello_max'])),
                        sobra=bool(ad is not None and ad <= u['refuta']))
        log(f"   P-R5 {u['frase']}\n        -> desc A12(REP_SIN_COSTE > CUELLO) {ad} (medianas {P['PR5']['desc_rep']} / {P['PR5']['desc_ctl']}); "
            f"sal: A12(REP_SIN_COSTE < CUELLO) {as1}, A12(CUELLO < VIVO) {as2}, mediana CUELLO {mc}  "
            f"{'PASA' if P['PR5']['pasa'] else ('LA TERCERA FILA SOBRA' if P['PR5']['sobra'] else 'NO')}")

    u = UMBRALES['PR5b']
    if hay('VIVO', 'REP_SIN_COSTE', 'CUELLO_MIN'):
        tasa = lambda b, k: v(b, lambda r: r['sac_tasa'][k])
        ad, mc = A12(desc('REP_SIN_COSTE'), desc('CUELLO_MIN')), med(sal('CUELLO_MIN'))
        aA, aC = A12(tasa('REP_SIN_COSTE', 'A'), tasa('CUELLO_MIN', 'A')), A12(tasa('REP_SIN_COSTE', 'C'), tasa('CUELLO_MIN', 'C'))
        P['PR5b'] = dict(control='CUELLO_MIN', a12_desc=ad, ctl_sal=mc, a12_comida=aA, a12_agua=aC,
                         desc_ctl=med(desc('CUELLO_MIN')), desc_rep=med(desc('REP_SIN_COSTE')),
                         tasa_A=(med(tasa('REP_SIN_COSTE', 'A')), med(tasa('CUELLO_MIN', 'A'))),
                         tasa_C=(med(tasa('REP_SIN_COSTE', 'C')), med(tasa('CUELLO_MIN', 'C'))),
                         pasa=bool(ge(ad, u['a12_desc']) and le(mc, u['sal_max']) and ge(aA, u['a12_ac']) and ge(aC, u['a12_ac'])),
                         sobra=bool(ad is not None and ad <= u['refuta']))
        log(f"   P-R5b {u['frase']}\n        -> desc A12(REP_SIN_COSTE > CUELLO_MIN) {ad} (medianas {P['PR5b']['desc_rep']} / {P['PR5b']['desc_ctl']}); "
            f"sal CUELLO_MIN {mc}; comida A12 {aA} (medianas {P['PR5b']['tasa_A']}); agua A12 {aC} (medianas {P['PR5b']['tasa_C']})  "
            f"{'PASA' if P['PR5b']['pasa'] else ('LA TERCERA FILA SOBRA' if P['PR5b']['sobra'] else 'NO')}")

    u = UMBRALES['PR6']
    if hay('VIVO', 'REP_SIN_COSTE', 'REP'):
        d = {}
        for b in ('REP_SIN_COSTE', 'REP'):
            g = [G[b][s] for s in S if s in G[b]]
            d[b] = dict(n_xor=sum(r['xor01'] >= 1.0 for r in g), n_cel=sum(r['celdas_ok_estricto'] == len(MV.INFORM) for r in g),
                        exp_tabla=razon(med([r['exp_tabla'] for r in g]), med([G['VIVO'][s]['exp_tabla'] for s in S if s in G['VIVO']])))
        d['a12_mu'] = A12(mu('VIVO'), mu('REP_SIN_COSTE'))   # P(REP_SIN_COSTE < VIVO)
        d['mu_rep'] = razon(med(mu('REP')), med(mu('VIVO')))
        P['PR6'] = dict(**d, pasa=bool(all(d[b]['n_xor'] >= u['n_min'] and d[b]['n_cel'] >= u['n_min'] and le(d[b]['exp_tabla'], u['f_exp'])
                                          for b in ('REP_SIN_COSTE', 'REP')) and ge(d['a12_mu'], u['a12_mu']) and le(d['mu_rep'], u['f_mu'])))
        log(f"   P-R6 {u['frase']}\n        -> REP_SIN_COSTE xor {d['REP_SIN_COSTE']['n_xor']}/{len(S)} celdas {d['REP_SIN_COSTE']['n_cel']}/{len(S)} exp_tabla x{d['REP_SIN_COSTE']['exp_tabla']}; "
            f"REP xor {d['REP']['n_xor']}/{len(S)} celdas {d['REP']['n_cel']}/{len(S)} exp_tabla x{d['REP']['exp_tabla']}; "
            f"muertes A12(REP_SIN_COSTE < VIVO) {d['a12_mu']}, REP/VIVO {d['mu_rep']}  {'PASA' if P['PR6']['pasa'] else 'NO'}")

    u = UMBRALES['PR7']
    if hay('REP_SIN_COSTE', 'REP'):
        d = {}
        for b in ('REP_SIN_COSTE', 'REP'):
            g = [G[b][s] for s in S if s in G[b]]
            d[b] = sum(bool(r['W_rep'] and r['W_rep']['A'] >= u['pos'] and r['W_rep']['C'] >= u['pos']
                            and r['W_rep']['B'] <= u['neg'] and r['W_rep']['D'] <= u['neg']) for r in g)
        P['PR7'] = dict(**d, pasa=bool(all(d[b] >= u['n_min'] for b in d)))
        log(f"   P-R7 {u['frase']}\n        -> REP_SIN_COSTE {d['REP_SIN_COSTE']}/{len(S)}, REP {d['REP']}/{len(S)}  {'PASA' if P['PR7']['pasa'] else 'NO'}")

    u = UMBRALES['PR8']
    if hay('VIVO', 'REP_SIN_COSTE'):
        ex = lambda b, k: med(v(b, lambda r: r['exposiciones'][k]))
        fs, fc = razon(ex('REP_SIN_COSTE', 'D'), ex('VIVO', 'D')), razon(ex('REP_SIN_COSTE', 'A'), ex('VIVO', 'A'))
        P['PR8'] = dict(sal=fs, comida=fc, pasa=bool(le(fs, u['f_sal']) and ge(fc, u['f_com'])))
        log(f"   P-R8 {u['frase']}\n        -> sal x{fs}, comida x{fc}  {'PASA' if P['PR8']['pasa'] else 'NO'}")
    return P


def frase_final(V):
    """El veredicto en el vocabulario del preregistro (seccion 6). Nada de 'quiere', 'proposito', 'se reproduce'."""
    P = V['completo']
    p = {k: (P.get(k) or {}).get('pasa') for k in ('PR1', 'PR2', 'PR3', 'PR4', 'PR5', 'PR5b', 'PR6', 'PR7', 'PR8')}
    if (P.get('PR1') or {}).get('se_tira'):
        return "LA MEDIDA SE TIRA: descendientes_viables no ordena los brazos como la supervivencia (P-R1 < 0.50). Nada mas se lee."
    s = ("La medida ORDENA como la supervivencia (P-R1). " if p['PR1'] else "La medida ordena DEBILMENTE (P-R1 bajo el umbral, no invertida). ")
    if p['PR2'] and p['PR3']:
        s += "Con la tercera fila (cuello de botella), el organismo SACIADO rechaza la sal (P-R2) y sostiene mas ventanas de viabilidad sin pagar (P-R3). "
    elif p['PR2']:
        s += "La tercera fila cambia la conducta saciado (P-R2) pero eso NO se vuelve viabilidad sostenida (P-R3 cae). "
    else:
        s += "La tercera fila NO cambia la conducta saciado (P-R2 cae): el mecanismo se refuta como conducta. "
    s += ("Pagando 0.4/0.4 por descendiente sigue por encima de VIVO (P-R4). " if p['PR4'] else
          ("Pagando queda PEOR que sin proposito: el precio no se paga (P-R4 refutada). " if (P.get('PR4') or {}).get('refutada')
           else "Pagando: no concluyente (P-R4). "))
    s += ("Leer la fila del recurso mas escaso NO basta (P-R5, CUELLO). " if p['PR5'] else
          ("CUELLO (fila del recurso mas escaso) rinde igual que la tercera fila (P-R5). " if (P.get('PR5') or {}).get('sobra')
           else "CUELLO queda cerca (P-R5 NO). "))
    s += ("La lectura pesimista de las dos filas (CUELLO_MIN) tampoco basta: la tercera fila aporta sobre el control que podia ganar (P-R5b). "
          if p['PR5b'] else
          ("LA TERCERA FILA SOBRA: la lectura pesimista de las dos filas existentes (CUELLO_MIN) rinde igual; se declara ese enrutamiento, "
           "no una necesidad (P-R5b). " if (P.get('PR5b') or {}).get('sobra')
           else "CUELLO_MIN queda cerca: no se declara la tercera fila por encima de la lectura pesimista (P-R5b NO). "))
    s += ("La tabla necesidad x estimulo y las muertes no se resienten (P-R6). " if p['PR6'] else "AVISO: la tercera fila cuesta conocimiento o vidas (P-R6 cae). ")
    s += ("La fila 2 aprende la tabla del cuello de botella (P-R7). " if p['PR7'] else "La fila 2 NO aprende la tabla predicha (P-R7 cae). ")
    s += ("El mundo no se llena de sal rechazada (P-R8). " if p['PR8'] else "La sal rechazada inunda el anillo o roba comida (P-R8 cae): P-R3 se lee neto. ")
    return s + "20 semillas no cierran nada: piden la replica en 241-260 (regla 12)."


# ---------------------------------------------------------------- humo (UN proceso, sin Pool, regla 3: 6 corridas)
def humo():
    stamp = time.strftime('%Y%m%d_%H%M%S')
    _log['f'] = open(os.path.join(RAIZ, 'datos', f'vivo_rep_humo_{stamp}.log'), 'w', encoding='utf-8', newline='\n')
    log("HUMO del disenador, UN proceso, sin Pool (regla 3: 6 corridas de 100000). PREREGISTRO_reproduccion.md seccion 10.")
    log("Semillas 1-2 (las de la mini-prueba): NINGUNA de las 221-260 del bloque queda expuesta.")
    for k, v in SHAS().items():
        log(f"    sha {k:22s} {v}")
    log(f"    origenes esperados v14 {SHA_V14_ESPERADO} / vivo {SHA_VIVO_ESPERADO} -> {'OK' if guarda_origen() else 'FALLA'}")
    log(f"    alias estructurales en 221-240: {alias_de(range(221, 241))}; en 241-260: {alias_de(range(241, 261))}")
    Ti, sem = 5000, [1, 2]
    log(f"1/2 IDENTIDAD dentro del runner, {len(CASOS_ID)} casos x {len(sem)} semillas, T={Ti}.")
    ident = []
    for cual in CASOS_ID:
        for s in sem:
            ident.append(tarea(('ID', cual, s, Ti)))
        g = [r for r in ident if r['cual'] == cual]
        log(f"    {CASOS_ID[cual][0]:66s} {sum(r['ok'] for r in g)}/{len(g)}"
            + ("" if all(r['ok'] for r in g) else f"   difieren {g[0]['difieren']} faltan {g[0]['faltan']} extra {g[0]['extra']}"))
    log(f"  IDENTIDAD {sum(r['ok'] for r in ident)}/{len(ident)}")
    if sum(r['ok'] for r in ident) != len(ident):
        log("*** IDENTIDAD FALLIDA: no se corre el humo."); _log['f'].close(); sys.exit(1)
    Tb = T
    plan = [('VIVO', 1), ('REP_SIN_COSTE', 1), ('REP', 1), ('CUELLO', 1), ('VIVO', 2), ('REP_SIN_COSTE', 2)]
    log(f"2/2 {len(plan)} corridas de T={Tb}: {plan}")
    log(f"    {'brazo':13s} s  {'seg':>6s} {'desc':>5s} {'viable':>7s} {'muertes [E, agua]':>19s}  {'saciado tasa A/B/C/D':>28s}  {'W fila 2':>34s}  xor01  celdas  exposiciones A/B/C/D")
    res, t_b = [], {}
    for b, s in plan:
        t1 = time.time(); r = tarea(('R', b, s, Tb)); t_b[f'{b}_s{s}'] = round(time.time() - t1, 1); res.append(r)
        st_ = '/'.join('-' if r['sac_tasa'][k] is None else f"{r['sac_tasa'][k]:.2f}" for k in MV.EST)
        wr = '-' if r['W_rep'] is None else ' '.join(f"{k}{r['W_rep'][k]:+.2f}" for k in MV.EST)
        ex = '/'.join(str(r['exposiciones'][k]) for k in MV.EST)
        log(f"    {b:13s} {s}  {t_b[f'{b}_s{s}']:6.1f} {r['descendientes']:5d} {r['frac_viable']:7.3f} {str(r['deaths']) + ' ' + str(r['muertes_nec']):>19s}  {st_:>28s}  {wr:>34s}  {r['xor01']:.2f}   {r['celdas_ok_estricto']}/4    {ex}")
        log(f"                    desc por cuarto {r['desc_q']}   decisiones saciado {r['sac_dec']}   tabla 2x4 error {r['err_peor']}   sac_mord {r['sac_mord']}")
    R = {(r['brazo'], r['seed']): r for r in res}
    H = {}
    H['H1'] = all(1 <= R[('VIVO', s)]['descendientes'] <= 150 for s in (1, 2))
    H['H2'] = all(R[('REP_SIN_COSTE', s)]['descendientes'] > R[('VIVO', s)]['descendientes'] for s in (1, 2))
    H['H3'] = all(ge(R[('VIVO', s)]['sac_tasa']['D'], 0.60) and le(R[('REP_SIN_COSTE', s)]['sac_tasa']['D'], 0.25) for s in (1, 2))
    H['H4'] = all(bool(R[('REP_SIN_COSTE', s)]['W_rep']) and R[('REP_SIN_COSTE', s)]['W_rep']['A'] >= 0.3 and R[('REP_SIN_COSTE', s)]['W_rep']['C'] >= 0.3
                  and R[('REP_SIN_COSTE', s)]['W_rep']['B'] <= -0.3 and R[('REP_SIN_COSTE', s)]['W_rep']['D'] <= -0.3 for s in (1, 2))
    H['H5'] = bool(R[('REP', 1)]['descendientes'] >= 0.5 * R[('REP_SIN_COSTE', 1)]['descendientes'])
    c, a, b_ = R[('CUELLO', 1)]['sac_tasa']['D'], R[('REP_SIN_COSTE', 1)]['sac_tasa']['D'], R[('VIVO', 1)]['sac_tasa']['D']
    H['H6'] = bool(c is not None and a is not None and b_ is not None and a < c < b_)
    for k in HUMO:
        log(f"   {k} {HUMO[k]:70s} -> {'SI' if H[k] else 'NO'}")
    seg = sum(t_b.values()) / len(t_b)
    log(f"ESTIMACION del bloque: {len(BRAZOS_ACTIVOS)}x{N_SEM} = {len(BRAZOS_ACTIVOS)*N_SEM} corridas de {T} pasos, ~{seg:.1f} s/corrida en serie "
        f"(maquina cargada con otro Pool) -> ~{len(BRAZOS_ACTIVOS)*N_SEM*seg/N_PARALELO/60:.1f} min de pared con Pool({N_PARALELO}).")
    log("HUMO: numeros observados, sin ajustar nada. n=1-2, semillas vistas: NO son evidencia.")
    dj = os.path.join(RAIZ, 'datos', f'vivo_rep_humo_{stamp}.json')
    json.dump(dict(meta=dict(fecha=time.strftime('%Y-%m-%dT%H:%M:%S'), tipo='humo', T_identidad=Ti, T_brazo=Tb, plan=plan,
                             umbrales=UMBRALES, humo_predicciones=HUMO, humo_resultado=H, shas=SHAS(), segundos=t_b,
                             brazos={b: {k: (list(v) if isinstance(v, tuple) else v) for k, v in BRAZOS[b].items()} for b in BRAZOS},
                             python=platform.python_version(), numpy=np.__version__),
                   identidades=ident, brazos=res), open(dj, 'w', encoding='utf-8'), ensure_ascii=False, default=str)
    log(f"datos -> {os.path.basename(dj)}  sha256_16 = {h16(dj)}")
    _log['f'].close()


# ---------------------------------------------------------------- principal (Pool: SOLO el coordinador)
if __name__ == '__main__':
    if '--humo' in sys.argv:
        humo(); sys.exit(0)

    import multiprocessing as mp
    mp.set_start_method('spawn', force=True)
    desde = int(sys.argv[sys.argv.index('--desde') + 1]) if '--desde' in sys.argv else DESDE
    if '--T' in sys.argv:
        T = int(sys.argv[sys.argv.index('--T') + 1])
    if '--brazos' in sys.argv:
        BRAZOS_ACTIVOS = [b.strip() for b in sys.argv[sys.argv.index('--brazos') + 1].split(',') if b.strip()]
        malos = [b for b in BRAZOS_ACTIVOS if b not in BRAZOS]
        if malos:
            raise SystemExit(f"--brazos: brazo(s) desconocido(s) {malos}. Validos: {ORDEN}")
        for req in ('VIVO', 'REP_SIN_COSTE'):
            if req not in BRAZOS_ACTIVOS:
                raise SystemExit(f"--brazos: {req} es referencia obligatoria.")
    SEEDS = list(range(desde, desde + N_SEM))
    stamp = time.strftime('%Y%m%d_%H%M%S')
    _log['f'] = open(os.path.join(RAIZ, 'datos', f'vivo_rep_s{SEEDS[0]}-{SEEDS[-1]}_{stamp}.log'), 'w', encoding='utf-8', newline='\n')
    log(f"ARRANQUE PROPOSITO Y REPRODUCCION (mundo vivo, peldano 2): brazos {BRAZOS_ACTIVOS}, semillas {SEEDS[0]}-{SEEDS[-1]}, T={T}. Pool({N_PARALELO}).")
    log("20 semillas no cierran nada: cierran o refutan ESTE mecanismo y piden la replica (241-260).")
    for k, v in SHAS().items():
        log(f"    sha {k:22s} {v}")
    if not guarda_origen():
        sys.exit(1)
    alias = alias_de(SEEDS)
    log(f"REGLA 10 — alias estructurales de codigo en {SEEDS[0]}-{SEEDS[-1]} (calculados sin simular): {alias}"
        f"  (preregistro: 221-240 -> [236]; 241-260 -> [260])")
    try:
        ps = subprocess.run(['powershell', '-NoProfile', '-Command',
                             "Get-CimInstance Win32_Process | Where-Object { $_.Name -like 'python*' } | ForEach-Object { \"$($_.ProcessId) $($_.CommandLine)\" }"],
                            capture_output=True, text=True, timeout=60).stdout.strip().splitlines()
    except Exception as e:
        ps = [f"(no se pudo listar: {e})"]
    log(f"REGLA 11 — procesos python vivos ({len(ps)}), este es pid {os.getpid()}")

    V, res = {}, []
    with mp.Pool(N_PARALELO) as pool:
        ctrl = [('ID', c, s, T_ID) for c in CASOS_ID for s in SEMILLAS_ID]
        log(f"ETAPA 1/2 — IDENTIDAD interna ({len(CASOS_ID)} casos x {len(SEMILLAS_ID)} semillas = {len(ctrl)} comprobaciones de 2 x {T_ID} pasos). "
            "(D) y (E) DEBEN fallar: sin ellos la etapa pasa por vacuidad.")
        rc = pool.map(tarea, ctrl, chunksize=1)
        for cual in CASOS_ID:
            g = [r for r in rc if r['cual'] == cual]
            log(f"    {CASOS_ID[cual][0]:66s} {sum(r['ok'] for r in g)}/{len(g)}"
                + ("" if all(r['ok'] for r in g) else f"   difieren {g[0]['difieren']} faltan {g[0]['faltan']} extra {g[0]['extra']}"))
            V[f'ID_{cual}'] = all(r['ok'] for r in g)
        V['G_IDENTIDAD'] = bool(all(V[f'ID_{c}'] for c in CASOS_ID))
        log(f"  IDENTIDAD {sum(r['ok'] for r in rc)}/{len(rc)}")
        if not V['G_IDENTIDAD']:
            log("*** GUARDA DE IDENTIDAD FALLIDA. Se para."); sys.exit(1)

        tr = [('R', b, s, T) for b in BRAZOS_ACTIVOS for s in SEEDS]
        log(f"ETAPA 2/2 — principal: {len(tr)} corridas de {T} pasos ({len(BRAZOS_ACTIVOS)} brazos x {len(SEEDS)} semillas)...")
        for i, r in enumerate(pool.imap_unordered(tarea, tr, chunksize=1), 1):
            res.append(r)
            if i % 20 == 0 or i == len(tr):
                log(f"          {i}/{len(tr)}")

    log()
    log("ANALISIS — medianas por brazo y los umbrales EXACTOS del preregistro (A12 sin parear, razon de medianas, cuartiles).")
    V.update(veredicto(res, SEEDS))
    ver = frase_final(V)
    log(); log(f"VEREDICTO: {ver}")
    meta = dict(fecha=time.strftime('%Y-%m-%dT%H:%M:%S'), semillas=SEEDS, T=T, alias=alias,
                brazos={b: {k: (list(v) if isinstance(v, tuple) else v) for k, v in BRAZOS[b].items()} for b in BRAZOS_ACTIVOS},
                veredicto=ver, veredictos=V, identidades=rc, procesos_python=ps, shas=SHAS(),
                origenes_esperados=dict(v14=SHA_V14_ESPERADO, vivo=SHA_VIVO_ESPERADO),
                python=platform.python_version(), numpy=np.__version__)
    dj = os.path.join(RAIZ, 'datos', f'vivo_rep_s{SEEDS[0]}-{SEEDS[-1]}_{stamp}.json')
    json.dump(dict(meta=meta, principal=res), open(dj, 'w', encoding='utf-8'), ensure_ascii=False, default=str)
    log(f"datos -> {os.path.basename(dj)}  sha256_16 = {h16(dj)}")
    _log['f'].close()
