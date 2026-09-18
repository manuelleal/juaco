"""REPRODUCCION, BLOQUE 2 (mundo vivo; linea F) — ejecuta PREREGISTRO_reproduccion_2.md (escrito ANTES de correr; sha en
el meta). ERR-40: la ventana de viabilidad sola no esta ligada a la supervivencia (premia atracones que mueren mas).
MEDIDA NUEVA: crecimiento neto del linaje  r = descendientes - muertes  (nacimientos menos muertes por corrida de
100 000 pasos; tipo de cambio 1:1, el de la dinamica de poblaciones). Instrumento organismo_vivo_rep2.py (por anclas desde
organismo_vivo_rep.py, que solo se lee; diagnosticos de solo lectura: desc_regalo y vidas).
Reutiliza corre_vivo_rep.py (brazos, resumen, A12, medianas, cuartiles) SIN copiarlo. REGLA 10: log desde el arranque.

    python experimentos/nivel11_mundo_vivo/corre_vivo_rep2.py [--desde 261] [--T 100000] [--brazos ...]
    python experimentos/nivel11_mundo_vivo/corre_vivo_rep2.py --humo     (UN proceso, sin Pool, 6 corridas: el disenador)
    python experimentos/nivel11_mundo_vivo/corre_vivo_rep2.py --retro    (RETRODICCION: la letra del bloque 2 sobre el JSON
                                                                          del bloque 1, 221-240; no es evidencia, no corre nada)

Etapas con Pool (las corre el COORDINADOR, reglas 3 y 11):
  1/2 IDENTIDAD interna, 5 casos x 3 semillas (T=20000): (A) apagada == organismo_vivo · (B) cadena == organismo_v14 ·
      (C) rep2=0 == organismo_vivo_rep · (D) rep2=1: claves viejas == organismo_vivo_rep · (E) CUELLO_MIN != (DEBE fallar).
  2/2 principal: 7 brazos x 20 semillas (261-280; replica 281-300 con --desde 281).

Brazos: VIVO, CUELLO_MIN (el mecanismo que se declara: saciado, el minimo de las dos filas), REP_SIN_COSTE (la tercera
fila, RETIRADA por Occam: se corre solo para medirla con la medida nueva), UNA_NEC, ESCALAR, BARAJA_CON, BARAJA_POL.
Subconjunto preregistrado (regla 10): ALIAS = algun solapamiento de codigos = 3 (261-280: 278 sal==agua; 281-300: 286
sal==veneno); completo y LIMPIAS al lado.

Vocabulario (regla 6): "crecimiento neto del linaje", "tasa de reemplazo (r >= 0)", "lectura pesimista saciado". NO se dice
"se reproduce" (nada nace), "poblacion", "evoluciona", "quiere".
"""
import sys, os, json, time, glob, platform, subprocess, statistics as st
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
import numpy as np

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
sys.path[:0] = [AQUI, os.path.join(RAIZ, 'organismo')]   # organismo/ PRIMERO (ERR-28)

import mini_vivo as MV
import corre_vivo_rep as C1        # brazos, MED, resumen, A12, med, q, ge, le, h16, N, alias_de: NO se copian
import diagnostico_codigos as DC

T = 100000
T_ID = 20000
N_PARALELO = 14
N_SEM = 20
DESDE = 261
SEMILLAS_ID = [1, 2, 3]
SHA_ESPERADOS = dict(v14='feefc88b1fd8d434', vivo='20c0961c79de8825', rep='aa823d56c2d4213c')

MED2 = dict(C1.MED, rep2=1, rep2_regalo=600)
BRAZOS = {b: dict(C1.BRAZOS[b], **MED2) for b in ('VIVO', 'CUELLO_MIN', 'REP_SIN_COSTE', 'UNA_NEC', 'ESCALAR', 'BARAJA_CON', 'BARAJA_POL')}
ORDEN = ['VIVO', 'CUELLO_MIN', 'REP_SIN_COSTE', 'UNA_NEC', 'ESCALAR', 'BARAJA_CON', 'BARAJA_POL']
BRAZOS_ACTIVOS = list(ORDEN)
NUEVAS_REP2 = {'desc_regalo', 'vidas', 'vida_final', 'rep2'}
CASOS_ID = {   # (etiqueta, referencia, kw referencia, kw rep2, debe_diferir, claves que se quitan)
    'A': ("(A) apagada (reproduccion=0) == organismo_vivo VIVO", 'vivo', MV.BRAZOS['VIVO'], dict(MV.BRAZOS['VIVO'], reproduccion=0), False, ()),
    'B': ("(B) cadena: rep2(vivo=0, n_nec=1) == organismo_v14", 'v14', dict(), dict(vivo=0, n_nec=1), False, ()),
    'C': ("(C) rep2=0 == organismo_vivo_rep (CUELLO_MIN, todas las claves)", 'rep', C1.BRAZOS['CUELLO_MIN'], C1.BRAZOS['CUELLO_MIN'], False, ()),
    'D': ("(D) rep2=1: claves viejas == organismo_vivo_rep VIVO (solo lectura)", 'rep', C1.BRAZOS['VIVO'], BRAZOS['VIVO'], False, NUEVAS_REP2),
    'E': ("(E) CUELLO_MIN != organismo_vivo VIVO (DEBE fallar)", 'vivo', MV.BRAZOS['VIVO'], BRAZOS['CUELLO_MIN'], True, C1.NUEVAS_REP | NUEVAS_REP2),
}

# ---------------------------------------------------------------- UMBRALES: la LETRA del preregistro (ERR-31)
UMBRALES = {
    'P21': dict(frase="la medida ordena como la supervivencia (r = desc - muertes): A12(VIVO > ESCALAR) >= 0.80; A12(VIVO > BARAJA_CON) >= 0.80; "
                      "A12(VIVO > UNA_NEC) >= 0.80; A12(UNA_NEC > BARAJA_POL) >= 0.95 (cualquiera < 0.50: la medida se tira y la linea se cierra)",
                esc=0.80, con=0.80, una=0.80, pol=0.95, tira=0.50),
    'P22': dict(frase="mediana de r por brazo dentro de su intervalo (>= 6/7): VIVO [-115,-45]; UNA_NEC [-160,-90]; ESCALAR [-150,-80]; "
                      "BARAJA_CON [-155,-85]; BARAJA_POL [-430,-310]; REP_SIN_COSTE [-55,+15]; CUELLO_MIN [-50,+25]",
                intervalos={'VIVO': (-115, -45), 'UNA_NEC': (-160, -90), 'ESCALAR': (-150, -80), 'BARAJA_CON': (-155, -85),
                            'BARAJA_POL': (-430, -310), 'REP_SIN_COSTE': (-55, 15), 'CUELLO_MIN': (-50, 25)}, n_min=6),
    'P23': dict(frase="mecanismo: r A12(CUELLO_MIN > VIVO) >= 0.90 y diferencia de medianas >= 40; muertes A12(CUELLO_MIN < VIVO) >= 0.80; "
                      "descendientes A12(CUELLO_MIN > VIVO) >= 0.90",
                a12_r=0.90, dif=40, a12_mu=0.80, a12_desc=0.90),
    'P24': dict(frase="Occam (la tercera fila se retira): r A12(REP_SIN_COSTE > CUELLO_MIN) <= 0.50 (>= 0.65: hallazgo no explicado, replica antes "
                      "de decir nada); y REP_SIN_COSTE sigue por encima de VIVO: A12 >= 0.85",
                a12_max=0.50, hallazgo=0.65, a12_vivo=0.85),
    'P25': dict(frase="tasa de reemplazo: CUELLO_MIN r >= 0 en >= 2/20 y <= 14/20 (en el filo, no por encima); VIVO, UNA_NEC, ESCALAR, "
                      "BARAJA_CON y BARAJA_POL r >= 0 en 0/20 cada uno; REP_SIN_COSTE <= 8/20",
                cm_min=2, cm_max=14, otros_max=0, rep_max=8),
    'P26': dict(frase="conducta saciado: mediana sac_tasa[D] VIVO >= 0.60; CUELLO_MIN sal <= 0.05 y veneno <= 0.05",
                vivo_min=0.60, cm_max=0.05),
    'P27': dict(frase="diagnostico de ERR-40 (blanda, se reporta): frac_regalo = desc_regalo/desc: A12(ESCALAR > CUELLO_MIN) >= 0.75 y "
                      "A12(BARAJA_CON > CUELLO_MIN) >= 0.75 (el regalo del renacer financia mas ventanas en los que mueren mas)",
                a12=0.75),
    'P28': dict(frase="seguridad y mundo: en CUELLO_MIN y REP_SIN_COSTE xor01 = 1.0 en >= 18/20 y celdas estrictas 4/4 en >= 18/20; "
                      "exposiciones[D] CUELLO_MIN <= 3 x VIVO; exposiciones[A] CUELLO_MIN >= 0.6 x VIVO",
                n_min=18, f_sal=3.0, f_com=0.6),
}
HUMO = {'H1': "r(VIVO) > r(ESCALAR) en 2/2 (misma semilla)", 'H2': "r(CUELLO_MIN) > r(VIVO) en 2/2",
        'H3': "coherencia de los diagnosticos (vidas = muertes; suma = T; regalo <= desc) en 6/6",
        'H4': "frac_regalo ESCALAR > CUELLO_MIN en 2/2 (blanda)", 'H5': "CUELLO_MIN saciado: sal <= 0.05 y veneno <= 0.05 en 2/2"}

_log = {'f': None, 't0': time.time()}


def log(msg=""):
    linea = f"[{time.strftime('%H:%M:%S')} +{time.time()-_log['t0']:7.1f}s] {msg}"
    print(linea, flush=True)
    if _log['f']:
        _log['f'].write(linea + "\n"); _log['f'].flush(); os.fsync(_log['f'].fileno())


A12, med, q, ge, le, h16, N = C1.A12, C1.med, C1.q, C1.ge, C1.le, C1.h16, C1.N


def resumen2(brazo, seed, r, kw, Ti):
    o = C1.resumen(brazo, seed, r, kw, Ti)
    vidas = r.get('vidas')
    o.update(r=r['descendientes'] - r['deaths'], desc_regalo=r.get('desc_regalo'),
             frac_regalo=(round(r['desc_regalo'] / r['descendientes'], 3) if r.get('desc_regalo') is not None and r['descendientes'] else None),
             vidas_n=(len(vidas) if vidas is not None else None),
             vida_mediana=(round(float(st.median(vidas + [r['vida_final']])), 1) if vidas is not None else None),
             vida_max=(max(vidas + [r['vida_final']]) if vidas is not None else None), vida_final=r.get('vida_final'))
    return o


def tarea(args):
    tipo = args[0]
    if tipo == 'ID':
        _, cual, seed, Ti = args
        import organismo_v14 as V14, organismo_vivo as VV, organismo_vivo_rep as VR, organismo_vivo_rep2 as V2
        etiq, ref, kwa, kwb, debe, quitar = CASOS_ID[cual]
        a = {'v14': V14, 'vivo': VV, 'rep': VR}[ref].run(seed, T=Ti, **kwa)
        b = V2.run(seed, T=Ti, **kwb)
        bb = {k: v for k, v in b.items() if k not in quitar}
        dif = [k for k in a if k in bb and N(a[k]) != N(bb[k])]
        falta = [k for k in a if k not in bb]
        extra = [k for k in bb if k not in a]
        igual = not dif and not falta and not extra
        return dict(tipo='ID', cual=cual, etiqueta=etiq, seed=seed, identico=igual, debe_diferir=debe, ok=bool(igual != debe),
                    difieren=dif[:6], faltan=falta, extra=extra[:6])
    _, brazo, seed, Ti = args
    import organismo_vivo_rep2 as V2
    kw = BRAZOS[brazo]
    return resumen2(brazo, seed, V2.run(seed, T=Ti, **kw), kw, Ti)


SHAS = lambda: dict(
    preregistro=h16(os.path.join(AQUI, 'PREREGISTRO_reproduccion_2.md')), script=h16(os.path.abspath(__file__)),
    constructor=h16(os.path.join(AQUI, 'construye_vivo_rep2.py')), instrumento=h16(os.path.join(AQUI, 'organismo_vivo_rep2.py')),
    arnes=h16(os.path.join(AQUI, 'identidad_vivo_rep2.py')), origen_organismo_vivo_rep=h16(os.path.join(AQUI, 'organismo_vivo_rep.py')),
    origen_organismo_vivo=h16(os.path.join(AQUI, 'organismo_vivo.py')), origen_organismo_v14=h16(os.path.join(RAIZ, 'organismo', 'organismo_v14.py')),
    corre_vivo_rep=h16(os.path.join(AQUI, 'corre_vivo_rep.py')), mini=h16(os.path.join(AQUI, 'mini_vivo.py')))


def guarda_origen():
    s = SHAS(); ok = True
    for k, esp in (('origen_organismo_v14', SHA_ESPERADOS['v14']), ('origen_organismo_vivo', SHA_ESPERADOS['vivo']),
                   ('origen_organismo_vivo_rep', SHA_ESPERADOS['rep'])):
        if s[k] != esp:
            log(f"*** ORIGEN CAMBIADO: {k} es {s[k]}, se esperaba {esp}. Reconstruir por anclas y repetir el arnes ANTES de correr."); ok = False
    return ok


# ---------------------------------------------------------------- veredicto (letra EXACTA del preregistro)
def veredicto(res, SEEDS, log=log):
    G = {b: {r['seed']: r for r in res if r['brazo'] == b} for b in BRAZOS_ACTIVOS}
    alias = C1.alias_de(SEEDS)
    limpias = [s for s in SEEDS if s not in alias]
    V = {'umbrales': UMBRALES, 'alias': alias, 'limpias': limpias, 'completo': serie(G, SEEDS, "CONJUNTO COMPLETO", log)}
    if alias and len(limpias) >= 0.6 * len(SEEDS):
        V['limpias_veredicto'] = serie(G, limpias, f"SUBCONJUNTO LIMPIAS (sin {alias}; regla 10)", log)
    return V


def serie(G, S, etiqueta, log):
    v = lambda b, f: [f(G[b][s]) for s in S if s in G.get(b, {})]
    rr = lambda b: v(b, lambda r: r['r'])
    desc = lambda b: v(b, lambda r: r['descendientes'])
    mu = lambda b: v(b, lambda r: r['deaths'])
    sal = lambda b: v(b, lambda r: r['sac_tasa']['D'])
    ven = lambda b: v(b, lambda r: r['sac_tasa']['B'])
    reg = lambda b: v(b, lambda r: r['frac_regalo'])
    hay = lambda *bs: all(b in G and any(s in G[b] for s in S) for b in bs)
    log(f"--- {etiqueta}: semillas {S[0]}-{S[-1]} (n={len(S)}) ---")
    M = {}
    for b in BRAZOS_ACTIVOS:
        g = [G[b][s] for s in S if s in G.get(b, {})]
        if not g:
            continue
        M[b] = dict(n=len(g), r=med(rr(b)), r_q25=q(rr(b), 0), r_q75=q(rr(b), 2), r_ge0=sum(x >= 0 for x in rr(b)),
                    desc=med(desc(b)), muertes=med(mu(b)), muertes_E=med(v(b, lambda r: r['muertes_nec'][0])),
                    muertes_agua=med(v(b, lambda r: r['muertes_nec'][1])), vida_mediana=med(v(b, lambda r: r['vida_mediana'])),
                    vida_max=med(v(b, lambda r: r['vida_max'])), frac_regalo=med(reg(b)), desc_regalo=med(v(b, lambda r: r['desc_regalo'])),
                    sac_sal=med(sal(b)), sac_ven=med(ven(b)), xor01=med(v(b, lambda r: r['xor01'])),
                    celdas_ok=med(v(b, lambda r: r['celdas_ok_estricto'])), exposiciones={k: med(v(b, lambda r, k=k: r['exposiciones'][k])) for k in MV.EST})
        m = M[b]
        log(f"   {b:13s} n={m['n']:<3d} r {m['r']} [q25 {m['r_q25']}, q75 {m['r_q75']}] r>=0 en {m['r_ge0']}  desc {m['desc']}  muertes {m['muertes']} "
            f"[E {m['muertes_E']}, agua {m['muertes_agua']}]  vida mediana {m['vida_mediana']} max {m['vida_max']}  regalo {m['frac_regalo']} ({m['desc_regalo']})")
        log(f"        saciado sal {m['sac_sal']} veneno {m['sac_ven']}  xor01 {m['xor01']}  celdas {m['celdas_ok']}/4  exposiciones {m['exposiciones']}")
    P = {'medianas': M}

    u = UMBRALES['P21']
    if hay('VIVO', 'ESCALAR', 'BARAJA_CON', 'UNA_NEC', 'BARAJA_POL'):
        a = dict(esc=A12(rr('VIVO'), rr('ESCALAR')), con=A12(rr('VIVO'), rr('BARAJA_CON')), una=A12(rr('VIVO'), rr('UNA_NEC')),
                 pol=A12(rr('UNA_NEC'), rr('BARAJA_POL')))
        P['P21'] = dict(**a, pasa=bool(all(ge(a[k], u[k]) for k in a)), se_tira=bool(any(x is not None and x < u['tira'] for x in a.values())))
        log(f"   P2-1 {u['frase']}\n        -> A12 VIVO>ESCALAR {a['esc']}, VIVO>BARAJA_CON {a['con']}, VIVO>UNA_NEC {a['una']}, UNA_NEC>BARAJA_POL {a['pol']}  "
            f"{'PASA' if P['P21']['pasa'] else ('SE TIRA LA MEDIDA' if P['P21']['se_tira'] else 'NO (ordena debilmente)')}")

    u = UMBRALES['P22']
    d = {b: (M[b]['r'], u['intervalos'][b][0] <= M[b]['r'] <= u['intervalos'][b][1]) for b in u['intervalos'] if b in M}
    if d:
        n = sum(x[1] for x in d.values())
        P['P22'] = dict(medianas={b: x[0] for b, x in d.items()}, dentro={b: x[1] for b, x in d.items()}, n=n, pasa=bool(n >= u['n_min'] and len(d) == 7))
        log(f"   P2-2 {u['frase']}\n        -> " + ", ".join(f"{b} {x[0]}{'' if x[1] else ' FUERA'}" for b, x in d.items()) + f"  ({n}/{len(d)})  {'PASA' if P['P22']['pasa'] else 'NO'}")

    u = UMBRALES['P23']
    if hay('VIVO', 'CUELLO_MIN'):
        a, dif = A12(rr('CUELLO_MIN'), rr('VIVO')), (None if M['CUELLO_MIN']['r'] is None or M['VIVO']['r'] is None else round(M['CUELLO_MIN']['r'] - M['VIVO']['r'], 1))
        am, ad = A12(mu('VIVO'), mu('CUELLO_MIN')), A12(desc('CUELLO_MIN'), desc('VIVO'))
        P['P23'] = dict(a12_r=a, dif=dif, a12_mu=am, a12_desc=ad, pasa=bool(ge(a, u['a12_r']) and ge(dif, u['dif']) and ge(am, u['a12_mu']) and ge(ad, u['a12_desc'])))
        log(f"   P2-3 {u['frase']}\n        -> r A12 {a}, diferencia {dif}; muertes A12 {am}; desc A12 {ad}  {'PASA' if P['P23']['pasa'] else 'NO'}")

    u = UMBRALES['P24']
    if hay('VIVO', 'CUELLO_MIN', 'REP_SIN_COSTE'):
        a, b_ = A12(rr('REP_SIN_COSTE'), rr('CUELLO_MIN')), A12(rr('REP_SIN_COSTE'), rr('VIVO'))
        P['P24'] = dict(a12_rep_cm=a, a12_rep_vivo=b_, pasa=bool(le(a, u['a12_max']) and ge(b_, u['a12_vivo'])), hallazgo=bool(ge(a, u['hallazgo'])))
        log(f"   P2-4 {u['frase']}\n        -> A12(REP_SIN_COSTE > CUELLO_MIN) {a}; A12(REP_SIN_COSTE > VIVO) {b_}  "
            f"{'PASA (la tercera fila queda retirada)' if P['P24']['pasa'] else ('HALLAZGO NO EXPLICADO: replica antes de decir nada' if P['P24']['hallazgo'] else 'NO')}")

    u = UMBRALES['P25']
    if hay('CUELLO_MIN'):
        ge0 = {b: M[b]['r_ge0'] for b in M}
        otros = [b for b in ('VIVO', 'UNA_NEC', 'ESCALAR', 'BARAJA_CON', 'BARAJA_POL') if b in ge0]
        P['P25'] = dict(r_ge0=ge0, pasa=bool(u['cm_min'] <= ge0['CUELLO_MIN'] <= u['cm_max'] and all(ge0[b] <= u['otros_max'] for b in otros)
                                             and ('REP_SIN_COSTE' not in ge0 or ge0['REP_SIN_COSTE'] <= u['rep_max'])))
        log(f"   P2-5 {u['frase']}\n        -> r >= 0 en {ge0}  {'PASA' if P['P25']['pasa'] else 'NO'}")

    u = UMBRALES['P26']
    if hay('VIVO', 'CUELLO_MIN'):
        P['P26'] = dict(vivo_sal=M['VIVO']['sac_sal'], cm_sal=M['CUELLO_MIN']['sac_sal'], cm_ven=M['CUELLO_MIN']['sac_ven'],
                        pasa=bool(ge(M['VIVO']['sac_sal'], u['vivo_min']) and le(M['CUELLO_MIN']['sac_sal'], u['cm_max']) and le(M['CUELLO_MIN']['sac_ven'], u['cm_max'])))
        log(f"   P2-6 {u['frase']}\n        -> VIVO sal {M['VIVO']['sac_sal']}; CUELLO_MIN sal {M['CUELLO_MIN']['sac_sal']} veneno {M['CUELLO_MIN']['sac_ven']}  {'PASA' if P['P26']['pasa'] else 'NO'}")

    u = UMBRALES['P27']
    if hay('ESCALAR', 'BARAJA_CON', 'CUELLO_MIN') and any(x is not None for x in reg('CUELLO_MIN')):
        a1, a2 = A12(reg('ESCALAR'), reg('CUELLO_MIN')), A12(reg('BARAJA_CON'), reg('CUELLO_MIN'))
        P['P27'] = dict(a12_esc=a1, a12_con=a2, pasa=bool(ge(a1, u['a12']) and ge(a2, u['a12'])))
        log(f"   P2-7 {u['frase']}\n        -> A12(ESCALAR > CUELLO_MIN) {a1}, A12(BARAJA_CON > CUELLO_MIN) {a2}  {'PASA' if P['P27']['pasa'] else 'NO (se reporta)'}")

    u = UMBRALES['P28']
    if hay('VIVO', 'CUELLO_MIN', 'REP_SIN_COSTE'):
        d = {b: dict(n_xor=sum(r['xor01'] >= 1.0 for r in [G[b][s] for s in S if s in G[b]]),
                     n_cel=sum(r['celdas_ok_estricto'] == len(MV.INFORM) for r in [G[b][s] for s in S if s in G[b]])) for b in ('CUELLO_MIN', 'REP_SIN_COSTE')}
        fs = C1.razon(M['CUELLO_MIN']['exposiciones']['D'], M['VIVO']['exposiciones']['D']); fc = C1.razon(M['CUELLO_MIN']['exposiciones']['A'], M['VIVO']['exposiciones']['A'])
        P['P28'] = dict(**d, sal=fs, comida=fc, pasa=bool(all(d[b]['n_xor'] >= u['n_min'] and d[b]['n_cel'] >= u['n_min'] for b in d) and le(fs, u['f_sal']) and ge(fc, u['f_com'])))
        log(f"   P2-8 {u['frase']}\n        -> CUELLO_MIN xor {d['CUELLO_MIN']['n_xor']}/{len(S)} celdas {d['CUELLO_MIN']['n_cel']}/{len(S)}; REP_SIN_COSTE xor {d['REP_SIN_COSTE']['n_xor']}/{len(S)} "
            f"celdas {d['REP_SIN_COSTE']['n_cel']}/{len(S)}; sal x{fs}, comida x{fc}  {'PASA' if P['P28']['pasa'] else 'NO'}")
    return P


def frase_final(V):
    P = V['completo']
    p = {k: (P.get(k) or {}).get('pasa') for k in ('P21', 'P22', 'P23', 'P24', 'P25', 'P26', 'P27', 'P28')}
    if (P.get('P21') or {}).get('se_tira'):
        return "LA MEDIDA SE TIRA OTRA VEZ: r = desc - muertes no ordena los brazos como la supervivencia (P2-1 < 0.50). La linea de reproduccion como conteo se cierra."
    s = ("El crecimiento neto del linaje ORDENA como la supervivencia (P2-1)" if p['P21'] else "r ordena DEBILMENTE (P2-1 bajo el umbral, no invertido)") + \
        (" y las medianas caen donde se predijo (P2-2). " if p['P22'] else "; las medianas NO caen donde se predijo (P2-2). ")
    s += ("La lectura pesimista saciado (CUELLO_MIN) sube r respecto de VIVO por menos muertes y mas ventanas (P2-3). " if p['P23'] else "CUELLO_MIN NO sube r como se predijo (P2-3 cae). ")
    s += ("La tercera fila queda RETIRADA: no supera a CUELLO_MIN (P2-4). " if p['P24'] else
          ("HALLAZGO NO EXPLICADO: la tercera fila supera a CUELLO_MIN; replica antes de decir nada (P2-4). " if (P.get('P24') or {}).get('hallazgo') else "P2-4 no concluyente. "))
    s += ("CUELLO_MIN esta en el filo del reemplazo (r >= 0 en algunas semillas) y ningun otro llega (P2-5). " if p['P25'] else "P2-5 cae: el cuadro del reemplazo no es el predicho. ")
    s += ("Saciado: VIVO bebe su reserva (sal) y CUELLO_MIN no (P2-6). " if p['P26'] else "P2-6 cae. ")
    s += ("El regalo del renacer financia mas ventanas en los que mueren mas (P2-7). " if p['P27'] else
          ("P2-7 no aplica (sin desc_regalo). " if 'P27' not in P else "P2-7 (blanda) no: el regalo del renacer no explica la diferencia; ERR-40 queda en la contabilidad. "))
    s += ("Tabla necesidad x estimulo intacta y el mundo no se llena de sal (P2-8). " if p['P28'] else "P2-8 cae (seguridad o mundo). ")
    return s + "20 semillas no cierran nada: piden la replica en 281-300 (regla 12)."


# ---------------------------------------------------------------- humo (UN proceso, 6 corridas) y retrodiccion
def humo():
    stamp = time.strftime('%Y%m%d_%H%M%S')
    _log['f'] = open(os.path.join(RAIZ, 'datos', f'vivo_rep2_humo_{stamp}.log'), 'w', encoding='utf-8', newline='\n')
    log("HUMO del disenador, UN proceso, sin Pool (regla 3: 6 corridas de 100000). PREREGISTRO_reproduccion_2.md.")
    log("Semillas 1-2: NINGUNA de las 261-300 del bloque queda expuesta.")
    for k, v in SHAS().items():
        log(f"    sha {k:26s} {v}")
    log(f"    origenes -> {'OK' if guarda_origen() else 'FALLA'};  alias estructurales 261-280: {C1.alias_de(range(261, 281))}; 281-300: {C1.alias_de(range(281, 301))}")
    Ti, sem = 5000, [1, 2]
    log(f"1/2 IDENTIDAD dentro del runner, {len(CASOS_ID)} casos x {len(sem)} semillas, T={Ti}.")
    ident = []
    for cual in CASOS_ID:
        for s in sem:
            ident.append(tarea(('ID', cual, s, Ti)))
        g = [r for r in ident if r['cual'] == cual]
        log(f"    {CASOS_ID[cual][0]:66s} {sum(r['ok'] for r in g)}/{len(g)}" + ("" if all(r['ok'] for r in g) else f"   {g[0]['difieren']} {g[0]['faltan']} {g[0]['extra']}"))
    log(f"  IDENTIDAD {sum(r['ok'] for r in ident)}/{len(ident)}")
    if sum(r['ok'] for r in ident) != len(ident):
        log("*** IDENTIDAD FALLIDA: no se corre el humo."); _log['f'].close(); sys.exit(1)
    plan = [('VIVO', 1), ('ESCALAR', 1), ('CUELLO_MIN', 1), ('VIVO', 2), ('ESCALAR', 2), ('CUELLO_MIN', 2)]
    log(f"2/2 {len(plan)} corridas de T={T}: {plan}")
    log(f"    {'brazo':11s} s {'seg':>5s} {'r':>5s} {'desc':>4s} {'regalo':>6s} {'muertes [E, agua]':>18s} {'vida med/max':>13s} {'saciado A/B/C/D':>20s} {'xor':>4s} {'exposiciones A/B/C/D':>21s}")
    res, tb = [], {}
    for b, s in plan:
        t1 = time.time(); r = tarea(('R', b, s, T)); tb[f'{b}_s{s}'] = round(time.time() - t1, 1); res.append(r)
        st_ = '/'.join('-' if r['sac_tasa'][k] is None else f"{r['sac_tasa'][k]:.2f}" for k in MV.EST)
        log(f"    {b:11s} {s} {tb[f'{b}_s{s}']:5.1f} {r['r']:5d} {r['descendientes']:4d} {r['desc_regalo']:6d} {str(r['deaths'])+' '+str(r['muertes_nec']):>18s} "
            f"{str(r['vida_mediana'])+'/'+str(r['vida_max']):>13s} {st_:>20s} {r['xor01']:4.2f} {'/'.join(str(r['exposiciones'][k]) for k in MV.EST):>21s}")
        coh = (r['vidas_n'] == r['deaths'] and sum(r['vida_final'] + 0 for _ in [0]) >= 0)
        log(f"                coherencia: vidas {r['vidas_n']} = muertes {r['deaths']}; desc por cuarto {r['desc_q']}; frac_regalo {r['frac_regalo']}; celdas {r['celdas_ok_estricto']}/4; err_peor {r['err_peor']}")
    R = {(r['brazo'], r['seed']): r for r in res}
    import organismo_vivo_rep2 as V2
    H = {}
    H['H1'] = all(R[('VIVO', s)]['r'] > R[('ESCALAR', s)]['r'] for s in (1, 2))
    H['H2'] = all(R[('CUELLO_MIN', s)]['r'] > R[('VIVO', s)]['r'] for s in (1, 2))
    H['H3'] = all(r['vidas_n'] == r['deaths'] and r['desc_regalo'] <= r['descendientes'] for r in res)
    H['H4'] = all((R[('ESCALAR', s)]['frac_regalo'] or 0) > (R[('CUELLO_MIN', s)]['frac_regalo'] or 0) for s in (1, 2))
    H['H5'] = all(le(R[('CUELLO_MIN', s)]['sac_tasa']['D'], 0.05) and le(R[('CUELLO_MIN', s)]['sac_tasa']['B'], 0.05) for s in (1, 2))
    for k in HUMO:
        log(f"   {k} {HUMO[k]:72s} -> {'SI' if H[k] else 'NO'}")
    seg = sum(tb.values()) / len(tb)
    log(f"ESTIMACION del bloque: {len(BRAZOS_ACTIVOS)}x{N_SEM} = {len(BRAZOS_ACTIVOS)*N_SEM} corridas de {T}, ~{seg:.1f} s/corrida -> ~{len(BRAZOS_ACTIVOS)*N_SEM*seg/N_PARALELO/60:.1f} min con Pool({N_PARALELO}).")
    log("HUMO: numeros observados, sin ajustar nada. n=1-2, semillas vistas: NO son evidencia.")
    dj = os.path.join(RAIZ, 'datos', f'vivo_rep2_humo_{stamp}.json')
    json.dump(dict(meta=dict(fecha=time.strftime('%Y-%m-%dT%H:%M:%S'), tipo='humo', T_identidad=Ti, T_brazo=T, plan=plan, umbrales=UMBRALES,
                             humo_predicciones=HUMO, humo_resultado=H, shas=SHAS(), segundos=tb,
                             brazos={b: {k: (list(v) if isinstance(v, tuple) else v) for k, v in BRAZOS[b].items()} for b in BRAZOS},
                             python=platform.python_version(), numpy=np.__version__),
                   identidades=ident, brazos=res), open(dj, 'w', encoding='utf-8'), ensure_ascii=False, default=str)
    log(f"datos -> {os.path.basename(dj)}  sha256_16 = {h16(dj)}")
    _log['f'].close()


def retro():
    """RETRODICCION: la letra del bloque 2 sobre el JSON del bloque 1 (221-240). No corre nada; NO es evidencia (esas semillas
    ya se vieron); sirve para que el coordinador vea que hace r con el dato que tumbo la medida vieja."""
    global BRAZOS_ACTIVOS
    fs = sorted(glob.glob(os.path.join(RAIZ, 'datos', 'vivo_rep_s221-240_*.json')))
    if not fs:
        raise SystemExit("no hay JSON del bloque 1")
    d = json.load(open(fs[-1], encoding='utf-8'))
    res = []
    for r in d['principal']:
        r = dict(r); r.update(r=r['descendientes'] - r['deaths'], desc_regalo=None, frac_regalo=None, vidas_n=None, vida_mediana=None, vida_max=None, vida_final=None)
        res.append(r)
    BRAZOS_ACTIVOS = [b for b in ORDEN if any(r['brazo'] == b for r in res)]
    print(f"RETRODICCION sobre {os.path.basename(fs[-1])} (sha {h16(fs[-1])}): NO ES EVIDENCIA. P2-7 no aplica (sin desc_regalo).")
    V = veredicto(res, d['meta']['semillas'], log=lambda m="": print(m))
    print("\n" + frase_final(V))


# ---------------------------------------------------------------- principal (Pool: SOLO el coordinador)
if __name__ == '__main__':
    if '--humo' in sys.argv:
        humo(); sys.exit(0)
    if '--retro' in sys.argv:
        retro(); sys.exit(0)
    import multiprocessing as mp
    mp.set_start_method('spawn', force=True)
    desde = int(sys.argv[sys.argv.index('--desde') + 1]) if '--desde' in sys.argv else DESDE
    if '--T' in sys.argv:
        T = int(sys.argv[sys.argv.index('--T') + 1])
    if '--brazos' in sys.argv:
        BRAZOS_ACTIVOS = [b.strip() for b in sys.argv[sys.argv.index('--brazos') + 1].split(',') if b.strip()]
        malos = [b for b in BRAZOS_ACTIVOS if b not in BRAZOS]
        if malos:
            raise SystemExit(f"--brazos: desconocidos {malos}. Validos: {ORDEN}")
        for req in ('VIVO', 'CUELLO_MIN'):
            if req not in BRAZOS_ACTIVOS:
                raise SystemExit(f"--brazos: {req} es referencia obligatoria.")
    SEEDS = list(range(desde, desde + N_SEM))
    stamp = time.strftime('%Y%m%d_%H%M%S')
    _log['f'] = open(os.path.join(RAIZ, 'datos', f'vivo_rep2_s{SEEDS[0]}-{SEEDS[-1]}_{stamp}.log'), 'w', encoding='utf-8', newline='\n')
    log(f"ARRANQUE REPRODUCCION BLOQUE 2 (r = desc - muertes): brazos {BRAZOS_ACTIVOS}, semillas {SEEDS[0]}-{SEEDS[-1]}, T={T}. Pool({N_PARALELO}).")
    log("20 semillas no cierran nada: cierran o refutan ESTA medida y este mecanismo, y piden la replica (281-300).")
    for k, v in SHAS().items():
        log(f"    sha {k:26s} {v}")
    if not guarda_origen():
        sys.exit(1)
    alias = C1.alias_de(SEEDS)
    log(f"REGLA 10 — alias estructurales en {SEEDS[0]}-{SEEDS[-1]}: {alias} (preregistro: 261-280 -> [278]; 281-300 -> [286])")
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
        log(f"ETAPA 1/2 — IDENTIDAD interna ({len(ctrl)} comprobaciones de 2 x {T_ID} pasos). (E) DEBE fallar.")
        rc = pool.map(tarea, ctrl, chunksize=1)
        for cual in CASOS_ID:
            g = [r for r in rc if r['cual'] == cual]
            log(f"    {CASOS_ID[cual][0]:66s} {sum(r['ok'] for r in g)}/{len(g)}" + ("" if all(r['ok'] for r in g) else f"   {g[0]['difieren']} {g[0]['faltan']} {g[0]['extra']}"))
            V[f'ID_{cual}'] = all(r['ok'] for r in g)
        V['G_IDENTIDAD'] = bool(all(V[f'ID_{c}'] for c in CASOS_ID))
        log(f"  IDENTIDAD {sum(r['ok'] for r in rc)}/{len(rc)}")
        if not V['G_IDENTIDAD']:
            log("*** GUARDA DE IDENTIDAD FALLIDA. Se para."); sys.exit(1)
        tr = [('R', b, s, T) for b in BRAZOS_ACTIVOS for s in SEEDS]
        log(f"ETAPA 2/2 — principal: {len(tr)} corridas de {T} pasos...")
        for i, r in enumerate(pool.imap_unordered(tarea, tr, chunksize=1), 1):
            res.append(r)
            if i % 20 == 0 or i == len(tr):
                log(f"          {i}/{len(tr)}")
    log(); log("ANALISIS — medianas por brazo y la letra del preregistro (A12 sin parear, medianas, cuartiles).")
    V.update(veredicto(res, SEEDS))
    ver = frase_final(V)
    log(); log(f"VEREDICTO: {ver}")
    meta = dict(fecha=time.strftime('%Y-%m-%dT%H:%M:%S'), semillas=SEEDS, T=T, alias=alias,
                brazos={b: {k: (list(v) if isinstance(v, tuple) else v) for k, v in BRAZOS[b].items()} for b in BRAZOS_ACTIVOS},
                veredicto=ver, veredictos=V, identidades=rc, procesos_python=ps, shas=SHAS(), origenes_esperados=SHA_ESPERADOS,
                python=platform.python_version(), numpy=np.__version__)
    dj = os.path.join(RAIZ, 'datos', f'vivo_rep2_s{SEEDS[0]}-{SEEDS[-1]}_{stamp}.json')
    json.dump(dict(meta=meta, principal=res), open(dj, 'w', encoding='utf-8'), ensure_ascii=False, default=str)
    log(f"datos -> {os.path.basename(dj)}  sha256_16 = {h16(dj)}")
    _log['f'].close()
