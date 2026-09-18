"""BLOQUE 3 -- v15f (memoria de pares con RELEVO) EN EL MUNDO DE FAMILIAS, con la MISMA letra del bloque 2.
Ejecuta PREREGISTRO_bloque3_v15f.md (su sha va en el meta del JSON).

MISION (primero, siempre): llegar a la AGI por este camino -- un organismo minimo con reglas locales (sin backprop
en el runtime) que aprende, desaprende, generaliza, sobrevive y se reproduce, con evidencia preregistrada.

    python experimentos/nivel12_mundo_familias/corre_familias_b3.py --humo     (UN proceso, sin Pool: el disenador)
    python experimentos/nivel12_mundo_familias/corre_familias_b3.py [--desde 501] [--T 100000] [--brazos S-REL,...]

REGLA 3 y 11: el `Pool` lo lanza SOLO el coordinador. `--humo` es UN proceso.
REGLA 10: log desde el arranque, con fsync, una linea por etapa con marca de tiempo.
ERR-31: los umbrales de P-G1/P-G4/P-S1..S6 son los MISMOS OBJETOS del bloque 2 (`corre_familias_b2.UMBRALES`),
importados, no recopiados: la letra no puede cambiar al pasar de organismo. Los dos umbrales nuevos (la prediccion
del coordinador y la mia) viven en UMBRALES_B3, cada uno con su frase.
ERR-38/41/42/E.6: este runner IMPORTA `corre_familias_b2.py` (y con el `corre_familias.py` y `escala_codigo.py`):
reutiliza el mundo, las medidas (`lee_G`, `lee_S`, `traza`), el diagnostico estructural y el cruce de `cod0`.
ERR-44 / T-E: todo se mide sobre lo que LEE LA BOCA (`log`, `primera_b2`, `sep_exp`), nunca sobre pesos internos.
La tabla de pares (`mem_*`) se reporta como DIAGNOSTICO DEL MECANISMO y no decide ninguna prediccion de conducta.

Etapas:
  1/3 IDENTIDAD (subconjunto; el arnes completo va en identidad_familias_b3.py). Si falla, ABORTA.
  2/3 DIAGNOSTICO ESTRUCTURAL antes de simular: alias exacto por par y por semilla, U3, ventanas SEPARABLE/ALIAS.
  3/3 PRINCIPAL: 12 brazos x 20 semillas (501-520; replica 521-540 con --desde 521) + las dos anclas.
"""
import sys, os, json, time, hashlib, platform, subprocess

sys.stdout.reconfigure(encoding='utf-8', errors='replace')
AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
CREA = os.path.join(RAIZ, 'experimentos', 'creacion_A')
CREB = os.path.join(RAIZ, 'experimentos', 'creacion_B')
sys.path[:0] = [AQUI, CREA, CREB, os.path.join(RAIZ, 'organismo')]   # organismo/ PRIMERO (ERR-28)
import numpy as np
import corre_familias_b2 as B2R       # bloque 2: el mundo, las medidas, la letra, el diagnostico
CF = B2R.CF                            # bloque 1: log, medianas, A12, cuenta, diagnostico, cruce de cod0

T = 100000
T_ID = 20000
N_PARALELO = 14
N_SEM = 20
DESDE = 501
SEMILLAS_ID = [1, 2, 3]
SHA_V14_ESPERADO = 'feefc88b1fd8d434'
SHA_B2_ESPERADO = '30200bea6a41c3c8'
SHA_V15F_ESPERADO = '96fc5c5262107850'
SHA_V15FON_ESPERADO = '54d6efe0b564113c'

log, h16, N, med, cuartiles, razon, A12, cuenta = CF.log, CF.h16, CF.N, CF.med, CF.cuartiles, CF.razon, CF.A12, CF.cuenta
DELTAS, CRIT, BASE = B2R.DELTAS, B2R.CRIT, B2R.BASE

# ---------------------------------------------------------------- brazos: el mundo del bloque 2, sin tocar
GEN, SAL = dict(B2R.GEN), dict(B2R.SAL)
OFF, REL = dict(memoria_pares=None), dict(memoria_pares='relevo')
BRAZOS = {
    # ESCENARIO G: la variante NUNCA VISTA (deriva = T/3+1; la tercera variante no existe hasta 2T/3)
    'G-LIN':   dict(GEN, n_exc=0, fam_val='familia', **OFF),    # v14.1, referencia (bloque 2: g1 = 1.000 x2)
    'G-REL':   dict(GEN, n_exc=0, fam_val='familia', **REL),    # v15f
    'G-EXC':   dict(GEN, n_exc=8, fam_val='familia', **OFF),    # v14.1 con 8 excepciones VISTAS
    'G-REXC':  dict(GEN, n_exc=8, fam_val='familia', **REL),    # v15f con 8 excepciones VISTAS
    # ESCENARIO S: la variante que DEJA DE COMPORTARSE IGUAL (8 sal rosas en T/2). Cada brazo con su GEMELO.
    'S-EXC':   dict(SAL, vira=8,  fam_val='familia', **OFF),
    'S-LIN':   dict(SAL, vira=-8, fam_val='familia', **OFF),
    'S-REL':   dict(SAL, vira=8,  fam_val='familia', **REL),
    'S-REL0':  dict(SAL, vira=-8, fam_val='familia', **REL),
    'S-RAZA':  dict(SAL, vira=8,  fam_val='azar', **REL),
    'S-RAZA0': dict(SAL, vira=-8, fam_val='azar', **REL),
    'S-RBAR':  dict(SAL, vira=8,  fam_val='barajado', **REL),
    'S-RBAR0': dict(SAL, vira=-8, fam_val='barajado', **REL),
    # anclas: NO compiten en ninguna prediccion
    'V14':     dict(mundo='AB', memoria_pares=None),
    'V15F':    dict(mundo='AB', memoria_pares='relevo'),
}
ORDEN = ['G-LIN', 'G-REL', 'G-EXC', 'G-REXC', 'S-EXC', 'S-LIN', 'S-REL', 'S-REL0',
         'S-RAZA', 'S-RAZA0', 'S-RBAR', 'S-RBAR0', 'V14', 'V15F']
BRAZOS_ACTIVOS = list(ORDEN)
PAREJAS_S = [('S-EXC', 'S-LIN'), ('S-REL', 'S-REL0'), ('S-RAZA', 'S-RAZA0'), ('S-RBAR', 'S-RBAR0')]

CASOS_ID = {   # subconjunto critico del arnes de identidad_familias_b3.py
    'a': ("(a) memoria_pares=None == organismo_familias_b2 (AB)", 'B2', dict(), T_ID),
    'n': ("(n) memoria_pares=None == organismo_familias_b2 (familias)", 'B2F', dict(), T_ID),
    'o': ("(o) relevo ON en mundo=AB == organismo_v15f_on", 'V15FON', dict(), T_ID),
    'l': ("(l) apagada + mundo=AB == organismo_v14 (TRONCO)", 'V14', dict(), T_ID),
    'u': ("(u) relevo ON: vira=8 == vira=-8 ANTES del cambio", 'GEM', dict(), 0),
    'A': ("(A) relevo ON: vira=8 != vira=-8 DESPUES (DEBE diferir)", 'GEMD', dict(), 0),
    'y': ("(y) relevo != apagada en familias (DEBE diferir)", 'REL', dict(), T_ID),
}

# ---------------------------------------------------------------- UMBRALES
# La letra de P-G1, P-G4, P-S1, P-S2, P-S3, P-S4 y P-S6 es LA MISMA del bloque 2: se importa el objeto, no se copia.
UMBRALES = {k: B2R.UMBRALES[k] for k in ('PG1', 'PG4', 'PS1', 'PS2', 'PS3', 'PS4', 'PS6', 'PI')}
UMBRALES_B3 = {
    'PC': dict(frase="PREDICCION DEL COORDINADOR (registrada antes): v15f separa >= 6 de 8 INCLUIDAS las que eran "
                     "veneno, sep_exp/exp_asoc <= 1.0, y la retencion de la virada (ok_vir en el ultimo punto de "
                     "log) >= 0.8",
               nsep=6, factor=1.0, retencion=0.8),
    'PD': dict(frase="PREDICCION DEL DISENADOR (al lado, y distinta): v15f separa rapido (coincido: n_sep >= 6 y "
                     "sep/apr <= 1.0) pero NO retiene (ok_vir final <= 0.5) porque con D = 12 la celda ganadora es "
                     "UNA tabla de 4 casillas para 32 estimulos: cada mordida de una hermana sobrescribe la casilla "
                     "de la virada. Me refuta ok_vir final >= 0.8 (la del coordinador)",
               nsep=6, factor=1.0, retencion_max=0.5, retencion_refuta=0.8),
    'PM': dict(frase="MECANISMO -- DIAGNOSTICO DECLARADO Y CONTAMINADO, NO ES UNA PREDICCION: cuantos de los 32 "
                     "estimulos leen la TABLA de la celda ganadora en vez de relevar a la lineal, con que cobertura "
                     "(casillas vistas de 4) y con que error propio. Lo vi en el arnes (semilla 1, T = 30000: 66 "
                     "celdas, ganadora (2,4), cobertura 3/4, 32/32 leen la tabla) ANTES de escribir el preregistro, "
                     "asi que NO cuenta como prediccion: se reporta en las 20 semillas y sirve para leer las demas, "
                     "que si son ciegas. Marcador informativo: >= 28 de 32 leen la tabla ('el relevo casi no "
                     "dispara' seria < 8 de 32)",
               tabla_pasa=28, tabla_refuta=8),
}

# ---------------------------------------------------------------- lectura de una corrida
def resumen(brazo, seed, r, kw):
    d = B2R.resumen(brazo, seed, r, kw)
    if d.get('mundo') not in (None, 'AB'):
        wt = r.get('W_tabla') or {}
        d['mem'] = dict(pares=kw.get('memoria_pares'), ganadora=r.get('mem_ganadora'), vistas=r.get('mem_vistas'),
                        cobertura=r.get('mem_cobertura'), err=r.get('mem_err_tabla'),
                        n_tabla=sum(1 for v in wt.values() if v is not None), n_est=(len(wt) or len(r['val_mundo'])))
    else:
        d['mem'] = dict(pares=kw.get('memoria_pares'), ganadora=r.get('mem_ganadora'),
                        cobertura=r.get('mem_cobertura'))
    return d


# ---------------------------------------------------------------- tareas
def tarea(args):
    tipo = args[0]
    if tipo == 'ID':
        _, cual, seed, Ti = args
        import organismo_v14 as V14, organismo_v15f_on as V15FON
        import organismo_familias_b2 as B2, organismo_familias_b3 as B3
        etiq, ref, kw, Tc = CASOS_ID[cual]
        Tc = Tc or Ti
        salta, debe = (), False
        if ref == 'B2':
            a, b = B2.run(seed, T=Tc), B3.run(seed, T=Tc, memoria_pares=None)
        elif ref == 'B2F':
            k = B2R.resuelve(BRAZOS['S-EXC'], Tc)
            k.pop('memoria_pares')
            a, b = B2.run(seed, T=Tc, **k), B3.run(seed, T=Tc, memoria_pares=None, **k)
        elif ref == 'V15FON':
            a, b = V15FON.run(seed, T=Tc), B3.run(seed, T=Tc, memoria_pares='relevo')
        elif ref == 'V14':
            a, b = V14.run(seed, T=Tc), B3.run(seed, T=Tc, memoria_pares=None)
        elif ref == 'REL':
            k = B2R.resuelve(BRAZOS['S-EXC'], Tc)
            k.pop('memoria_pares')
            a = B3.run(seed, T=Tc, memoria_pares=None, **k); b = B3.run(seed, T=Tc, memoria_pares='relevo', **k)
            debe = True
            salta = ('memoria_pares', 'mem_alfa', 'mem_ganadora', 'mem_tabla', 'mem_vistas', 'mem_cobertura',
                     'mem_err_tabla', 'W_tabla', 'mem_fam', 'mem_ev')
        else:                                   # GEM / GEMD: el gemelo con el relevo ENCENDIDO
            k = B2R.resuelve(BRAZOS['S-REL'], Ti)
            k.pop('vira')
            Tg = (k['cambio'] - 1) if ref == 'GEM' else (k['cambio'] + 3 * k['deriva'])
            a = B3.run(seed, T=Tg, vira=8, **k); b = B3.run(seed, T=Tg, vira=-8, **k)
            debe = (ref == 'GEMD')
            salta = ('vira', 'val_post', 'sep_exp')
        dif = [k2 for k2 in a if k2 not in salta and N(a[k2]) != N(b.get(k2))]
        falta = [k2 for k2 in a if k2 not in b and k2 not in salta]
        igual = not dif and not falta
        return dict(tipo='ID', cual=cual, etiqueta=etiq, seed=seed, identico=igual, debe_diferir=debe,
                    ok=bool(igual != debe), difieren=dif[:6], faltan=falta)
    if tipo == 'D':
        _, seed, nk, ktop = args
        d = CF.diagnostico(seed, nk, ktop, BASE)
        d.pop('cod')
        return dict(tipo='D', **d)
    _, brazo, seed, Ti, nk, ktop, nkmax = args
    import organismo_familias_b3 as B3
    kw = B2R.resuelve(BRAZOS[brazo], Ti)
    if kw.get('mundo') != 'AB':
        kw.update(nk=nk, ktop=ktop, nkmax=nkmax)
    return resumen(brazo, seed, B3.run(seed, T=Ti, **kw), kw)


SHAS = lambda: dict(
    preregistro=h16(os.path.join(AQUI, 'PREREGISTRO_bloque3_v15f.md')),
    script=h16(os.path.abspath(__file__)),
    constructor=h16(os.path.join(AQUI, 'construye_familias_b3.py')),
    instrumento=h16(os.path.join(AQUI, 'organismo_familias_b3.py')),
    arnes=h16(os.path.join(AQUI, 'identidad_familias_b3.py')),
    origen_b2=h16(os.path.join(AQUI, 'organismo_familias_b2.py')),
    origen_v15f=h16(os.path.join(CREA, 'organismo_v15f.py')),
    origen_v15f_on=h16(os.path.join(CREA, 'organismo_v15f_on.py')),
    runner_bloque2=h16(os.path.join(AQUI, 'corre_familias_b2.py')),
    escala_codigo_bloque0=h16(os.path.join(AQUI, 'escala_codigo.py')),
    origen_organismo_v14=h16(os.path.join(RAIZ, 'organismo', 'organismo_v14.py')))


def guarda_origen():
    s, ok = SHAS(), True
    for k, esp in [('origen_organismo_v14', SHA_V14_ESPERADO), ('origen_b2', SHA_B2_ESPERADO),
                   ('origen_v15f', SHA_V15F_ESPERADO), ('origen_v15f_on', SHA_V15FON_ESPERADO)]:
        if s[k] != esp:
            log(f"*** ORIGEN CAMBIADO: {k} es {s[k]}, se esperaba {esp}. Reconstruir por anclas y repetir el arnes.")
            ok = False
    return ok


# ---------------------------------------------------------------- veredicto (la letra del bloque 2, importada)
def veredicto(res, SEEDS, diags):
    G = {b: {r['seed']: r for r in res if r['brazo'] == b} for b in BRAZOS_ACTIVOS}
    gg = lambda b, c: {s: (G.get(b, {}).get(s, {}).get('G') or {}).get(c) for s in SEEDS if s in G.get(b, {})}
    ss = lambda b, c: {s: (G.get(b, {}).get(s, {}).get('S') or {}).get(c) for s in SEEDS if s in G.get(b, {})}
    tz = lambda b, c: {s: (G.get(b, {}).get(s, {}).get('traza') or {}).get(c) for s in SEEDS if s in G.get(b, {})}
    mm = lambda b, c: {s: (G.get(b, {}).get(s, {}).get('mem') or {}).get(c) for s in SEEDS if s in G.get(b, {})}
    V = {'umbrales': UMBRALES, 'umbrales_b3': UMBRALES_B3}
    V['alias'] = dict(pares_mediana=med([d['alias_pares'] for d in diags]),
                      semillas_con_alias=sum(d['alias_semilla'] for d in diags), n=len(diags),
                      U3_mediana=med([d['U3'] for d in diags]))

    # --- PM: el mecanismo (decide COMO se leen las demas)
    u = UMBRALES_B3['PM']
    cob = [v for v in mm('S-REL', 'cobertura').values() if v is not None]
    ntab = [v for v in mm('S-REL', 'n_tabla').values() if v is not None]
    V['PM'] = dict(cobertura_med=med(cob), n_cob4=sum(1 for v in cob if v >= 4),
                   n_tabla_med=med(ntab), n_est=med([v for v in mm('S-REL', 'n_est').values() if v]),
                   err_med=med([v for v in mm('S-REL', 'err').values() if v is not None]),
                   ganadoras=sorted({tuple(v) for v in mm('S-REL', 'ganadora').values() if v})[:8], n=len(cob))
    V['PM']['pasa'] = bool(V['PM']['n_tabla_med'] is not None and V['PM']['n_tabla_med'] >= u['tabla_pasa'])
    V['PM']['es_prediccion'] = False   # declarado y contaminado: lo vi en el arnes antes de escribir el preregistro
    V['PM']['refuta'] = bool(V['PM']['n_tabla_med'] is not None and V['PM']['n_tabla_med'] < u['tabla_refuta'])

    # --- PG1 (misma letra) en G-REL, con G-LIN al lado
    u = UMBRALES['PG1']
    for b in ('G-REL', 'G-LIN', 'G-EXC', 'G-REXC'):
        v = [x for x in gg(b, 'g1').values() if x is not None]
        n1 = sum(1 for x in v if x >= u['med_pasa'])
        V[f'PG1_{b}'] = dict(med=med(v), q=cuartiles(v), n_ge=n1, n=len(v),
                             g1_fuerte=med(list(gg(b, 'g1_fuerte').values())),
                             g1_lenta=med(list(gg(b, 'g1_lenta').values())),
                             cond1=med(list(gg(b, 'cond1').values())),
                             ruta1=med(list(gg(b, 'ruta1').values())),
                             n_vista=med(list(gg(b, 'n_vista').values())),
                             pasa=bool(med(v) is not None and med(v) >= u['med_pasa'] and n1 >= u['n_pasa']),
                             refuta=bool(med(v) is not None and (med(v) <= u['med_refuta'] or n1 <= u['n_refuta'])))
    dl, dr = gg('G-LIN', 'g1'), gg('G-REL', 'g1')
    V['PG1_REL_vs_LIN'] = dict(n_menor=cuenta(dr, dl, SEEDS, lambda x, y: x < y),
                               A12=A12(list(dr.values()), list(dl.values())), n=len(SEEDS))

    # --- PG4 (misma letra) por organismo: EXC contra LIN
    u = UMBRALES['PG4']
    for par, et in ((('G-EXC', 'G-LIN'), 'v14'), (('G-REXC', 'G-REL'), 'v15f')):
        de, dn = gg(par[0], 'g1'), gg(par[1], 'g1')
        ne = cuenta(de, dn, SEEDS, lambda x, y: x < y)
        rz = razon(med(list(de.values())), med(list(dn.values())))
        me, mn = med(list(de.values())), med(list(dn.values()))
        dif = (abs(me - mn) if (me is not None and mn is not None) else None)
        V[f'PG4_{et}'] = dict(med_EXC=me, med_LIN=mn, razon=rz, n_menor=ne, n=len(SEEDS),
                              A12=A12(list(de.values()), list(dn.values())), dif=dif,
                              pasa=bool(ne >= u['n_pasa'] and rz is not None and rz <= u['razon_pasa']),
                              refuta=bool(dif is not None and dif <= u['dif_refuta'] and u['n_lo'] <= ne <= u['n_hi']))

    # --- PS1 (puerta): el gemelo, en las cuatro parejas
    u = UMBRALES['PS1']; pre = {}
    for a, b in PAREJAS_S:
        pa, pb = tz(a, 'prefijo'), tz(b, 'prefijo')
        pre[f'{a}/{b}'] = sum(1 for s in SEEDS if pa.get(s) is not None and pa.get(s) == pb.get(s))
    V['PS1'] = dict(parejas=pre, n=len(SEEDS),
                    pasa=bool(pre and all(v >= min(u['n_min'], len(SEEDS)) for v in pre.values())))

    # --- PS2 (misma letra) en S-REL y S-EXC, + PC y PD
    u = UMBRALES['PS2']
    for b in ('S-REL', 'S-EXC', 'S-RAZA', 'S-RBAR', 'S-REL0', 'S-LIN'):
        ns = [v for v in ss(b, 'n_sep').values() if v is not None]
        sa = {s: v for s, v in ss(b, 'sep_apr').items() if v is not None}
        V[f'PS2_{b}'] = dict(n_sep_med=med(ns), q_n_sep=cuartiles(ns),
                             sep_med=med(list(ss(b, 'sep_med').values())),
                             apr_med=med(list(ss(b, 'apr_med').values())),
                             sep_apr_med=med(list(sa.values())),
                             n_factor2=sum(1 for v in sa.values() if v >= u['factor_pasa']),
                             n_factor1=sum(1 for v in sa.values() if v <= u['factor_refuta']), n=len(ns))
        d = V[f'PS2_{b}']
        d['pasa'] = bool(d['n_sep_med'] is not None and d['n_sep_med'] <= u['nsep_pasa'] and d['n_factor2'] >= u['n_pasa'])
        d['refuta'] = bool(d['n_sep_med'] is not None and d['n_sep_med'] >= u['nsep_refuta'] and d['n_factor1'] >= u['n_pasa'])

    # --- PS3 (misma letra) en S-REL, con S-EXC al lado
    u = UMBRALES['PS3']
    for b in ('S-REL', 'S-EXC'):
        fc = {s: ss(b, 'n_sep_comida')[s] / max(ss(b, 'n_comida')[s], 1) for s in SEEDS
              if ss(b, 'n_sep_comida').get(s) is not None}
        fv = {s: ss(b, 'n_sep_veneno')[s] / max(ss(b, 'n_veneno')[s], 1) for s in SEEDS
              if ss(b, 'n_sep_veneno').get(s) is not None}
        na = cuenta(fc, fv, SEEDS, lambda x, y: x > y)
        V[f'PS3_{b}'] = dict(frac_comida=med(list(fc.values())), frac_veneno=med(list(fv.values())),
                             n_mayor=na, n=len(SEEDS), pasa=bool(na >= u['n_pasa']), refuta=bool(na <= u['n_refuta']))

    # --- PS4 (misma letra) por pareja
    u = UMBRALES['PS4']; dd = {}
    for a, b in PAREJAS_S:
        for D in DELTAS + ['fin']:
            ka, kb = tz(a, f'ok_herm_{D}'), tz(b, f'ok_herm_{D}')
            dd[f'{a}_{D}'] = {s: (kb[s] - ka[s]) for s in SEEDS if ka.get(s) is not None and kb.get(s) is not None}
    for a, b in PAREJAS_S:
        v = list(dd.get(f'{a}_{u["delta"]}', {}).values())
        npos = sum(1 for x in v if x > 0)
        V[f'PS4_{a}'] = dict(med=med(v), q=cuartiles(v), n_pos=npos, n=len(v), delta=u['delta'],
                             por_delta={str(D): med(list(dd.get(f'{a}_{D}', {}).values())) for D in DELTAS + ['fin']},
                             ok_herm={str(D): med(list(tz(a, f'ok_herm_{D}').values())) for D in DELTAS + ['fin']},
                             ok_herm_gemelo={str(D): med(list(tz(b, f'ok_herm_{D}').values())) for D in DELTAS + ['fin']},
                             pasa=bool(med(v) is not None and med(v) >= u['med_pasa'] and npos >= u['n_pasa']),
                             refuta=bool(med(v) is not None and (med(v) <= u['med_refuta'] or npos <= u['n_refuta'])))

    # --- PS6 (misma letra; aqui SI decide, por la prediccion del coordinador) y PC / PD
    V['PS6'] = {b: {str(D): med(list(tz(b, f'ok_vir_{D}').values())) for D in DELTAS + ['fin']}
                for b in ('S-REL', 'S-EXC', 'S-REL0', 'S-RAZA', 'S-RBAR')}
    ret = [v for v in tz('S-REL', 'ok_vir_fin').values() if v is not None]
    nsr = [v for v in ss('S-REL', 'n_sep').values() if v is not None]
    sar = [v for v in ss('S-REL', 'sep_apr').values() if v is not None]
    uc, ud = UMBRALES_B3['PC'], UMBRALES_B3['PD']
    V['PC'] = dict(n_sep_med=med(nsr), sep_apr_med=med(sar), retencion_med=med(ret),
                   n_sep_ge=sum(1 for v in nsr if v >= uc['nsep']),
                   n_factor_le=sum(1 for v in sar if v <= uc['factor']),
                   n_ret_ge=sum(1 for v in ret if v >= uc['retencion']), n=len(SEEDS))
    V['PC']['pasa'] = bool(V['PC']['n_sep_med'] is not None and V['PC']['n_sep_med'] >= uc['nsep']
                           and V['PC']['sep_apr_med'] is not None and V['PC']['sep_apr_med'] <= uc['factor']
                           and V['PC']['retencion_med'] is not None and V['PC']['retencion_med'] >= uc['retencion'])
    V['PD'] = dict(retencion_med=med(ret), n_ret_le=sum(1 for v in ret if v <= ud['retencion_max']), n=len(ret))
    V['PD']['pasa'] = bool(V['PC']['n_sep_med'] is not None and V['PC']['n_sep_med'] >= ud['nsep']
                           and V['PC']['sep_apr_med'] is not None and V['PC']['sep_apr_med'] <= ud['factor']
                           and V['PD']['retencion_med'] is not None and V['PD']['retencion_med'] <= ud['retencion_max'])
    V['PD']['refuta'] = bool(V['PD']['retencion_med'] is not None
                             and V['PD']['retencion_med'] >= ud['retencion_refuta'])

    V['linea_base'] = {b: dict(muertes=med([r['deaths'] for r in G[b].values()]),
                               q_muertes=cuartiles([r['deaths'] for r in G[b].values()]),
                               celdas=med([r['celdas'] for r in G[b].values()]),
                               splits=med([r['splits'] for r in G[b].values()]),
                               exp_total=med([r.get('exp_total') for r in G[b].values()]),
                               mem=med([(r.get('mem') or {}).get('n_tabla') for r in G[b].values()]))
                       for b in BRAZOS_ACTIVOS if b in G}
    return V


def frase_final(V):
    p = lambda k: ('pasa' if V.get(k, {}).get('pasa') else ('REFUTA' if V.get(k, {}).get('refuta') else 'indeciso'))
    if not V['PS1'].get('pasa'):
        return "PS1 CAE: algun gemelo no comparte prefijo exacto con su brazo -- es el INSTRUMENTO. Nada se declara."
    s = (f"MECANISMO (diagnostico declarado, no prediccion): cobertura de la ganadora {V['PM']['cobertura_med']}/4 "
         f"({V['PM']['n_cob4']}/{V['PM']['n']} a 4), {V['PM']['n_tabla_med']} de {V['PM']['n_est']} estimulos leen "
         f"la TABLA. ")
    s += (f"CAPACIDAD 1: g1 v15f {V['PG1_G-REL']['med']} contra v14.1 {V['PG1_G-LIN']['med']} "
          f"(REL<LIN en {V['PG1_REL_vs_LIN']['n_menor']}/20) -> PG1(v15f) {p('PG1_G-REL')}; "
          f"PG4 v14 {p('PG4_v14')}, v15f {p('PG4_v15f')}. ")
    s += (f"CAPACIDAD 2: v15f separa {V['PS2_S-REL']['n_sep_med']}/8 (sep/apr {V['PS2_S-REL']['sep_apr_med']}) contra "
          f"v14.1 {V['PS2_S-EXC']['n_sep_med']}/8 -> PS2(v15f) {p('PS2_S-REL')}; asimetria comida "
          f"{V['PS3_S-REL']['frac_comida']} contra veneno {V['PS3_S-REL']['frac_veneno']} -> PS3 {p('PS3_S-REL')}; "
          f"dano a las hermanas v15f {V['PS4_S-REL']['med']} contra v14.1 {V['PS4_S-EXC']['med']} -> "
          f"PS4(v15f) {p('PS4_S-REL')}. ")
    s += (f"RETENCION de la virada {V['PC']['retencion_med']} -> prediccion del coordinador "
          f"{'SE CUMPLE' if V['PC']['pasa'] else 'NO se cumple'}; del disenador "
          f"{'SE CUMPLE' if V['PD']['pasa'] else ('REFUTADA' if V['PD']['refuta'] else 'no se cumple')}. ")
    s += (f"Alias por par {V['alias']['pares_mediana']} ({V['alias']['semillas_con_alias']}/{V['alias']['n']} "
          f"semillas), covariable declarada. 20 semillas no cierran nada: replica en el rango siguiente (regla 12).")
    return s


# ---------------------------------------------------------------- humo (UN proceso, sin Pool, regla 3)
def humo(nk, ktop, nkmax, Tb):
    stamp = time.strftime('%Y%m%d_%H%M%S')
    CF._log['f'] = open(os.path.join(RAIZ, 'datos', f'familias_b3_humo_{stamp}.log'), 'w',
                        encoding='utf-8', newline='\n')
    CF._log['t0'] = time.time()
    log("HUMO del disenador del bloque 3, UN proceso, sin Pool (regla 3). PREREGISTRO_bloque3_v15f.md.")
    log("Semillas 1-2: NINGUNA de las 501-540 del bloque queda expuesta.")
    for k, v in SHAS().items():
        log(f"    sha {k:26s} {v}")
    log(f"    origenes verificados -> {'OK' if guarda_origen() else 'FALLA'}")
    sem = [1, 2]

    log("1/3 IDENTIDAD (subconjunto; el arnes completo va en identidad_familias_b3.py).")
    ident = []
    for cual in CASOS_ID:
        for s in sem:
            ident.append(tarea(('ID', cual, s, 6000)))
        g = [r for r in ident if r['cual'] == cual]
        log(f"    {CASOS_ID[cual][0]:58s} {sum(r['ok'] for r in g)}/{len(g)}"
            + ("" if all(r['ok'] for r in g) else f"   difieren {g[0]['difieren']}"))
    log(f"  IDENTIDAD {sum(r['ok'] for r in ident)}/{len(ident)}")

    log("2/3 DIAGNOSTICO ESTRUCTURAL (antes de simular): alias exacto, U3 y ventanas SEPARABLE/ALIAS.")
    diags = []
    for s in sem:
        d = CF.diagnostico(s, nk, ktop, BASE)
        diags.append(d)
        log(f"    semilla {s}: alias_pares {d['alias_pares']:.5f}  alias_semilla {d['alias_semilla']}  U3 {d['U3']}")

    # EQUIPO regla 3: <= 6 corridas de un proceso. El encargo pide "2 semillas, S-REL y S-EXC": son 4. Se anaden
    # S-REL0 y G-REL en la semilla 1 (2 mas) porque sin el gemelo no hay `dano_herm` y sin G-REL no hay PM en G.
    plan = [('S-REL', 1), ('S-REL', 2), ('S-EXC', 1), ('S-EXC', 2), ('S-REL0', 1), ('G-REL', 1)]
    log(f"3/3 HUMO: {len(plan)} corridas de {Tb} pasos (regla 3: <= 6).")
    res, t_b = [], {}
    for b, s in plan:
        t1 = time.time(); r = tarea(('R', b, s, Tb, nk, ktop, nkmax)); dt = time.time() - t1
        res.append(r); t_b[b] = round(t_b.get(b, 0.0) + dt, 2)
        m = r['mem']
        if r['esc'] == 'G':
            g = r['G']
            log(f"    {b:7s} s{s} {dt:5.1f}s  g1 {g['g1']}  g1_fuerte {g['g1_fuerte']}  g1_lenta {g['g1_lenta']}  "
                f"cond1 {g['cond1']}  ruta1 {g['ruta1']}  vistas {g['n_vista']}/8  muertes {r['deaths']}")
        else:
            S, z = r['S'], r['traza']
            log(f"    {b:7s} s{s} {dt:5.1f}s  n_sep {S['n_sep']}/{S['n_vir']}  sep_med {S['sep_med']}  "
                f"apr_med {S['apr_med']}  comida {S['n_sep_comida']}/{S['n_comida']}  "
                f"veneno {S['n_sep_veneno']}/{S['n_veneno']}  muertes {r['deaths']}  celdas {r['celdas']}")
            log(f"            ok_herm " + " ".join(f"{D}:{z[f'ok_herm_{D}']}" for D in DELTAS)
                + f" fin:{z['ok_herm_fin']}   ok_vir " + " ".join(f"{D}:{z[f'ok_vir_{D}']}" for D in DELTAS)
                + f" fin:{z['ok_vir_fin']}   prefijo {z['prefijo']}")
        log(f"            MECANISMO ganadora {m['ganadora']}  cobertura {m['cobertura']}/4  "
            f"casillas vistas {m['vistas']}  leen la TABLA {m['n_tabla']}/{m['n_est']}  err {m['err']}")
    pe = {b: r['traza']['prefijo'] for b, r in [(x['brazo'], x) for x in res]
          if b in ('S-REL', 'S-REL0') and r.get('seed') == 1}
    log(f"  GEMELO (P-S1) semilla 1, S-REL/S-REL0: {list(pe.values())} -> "
        f"{'IDENTICOS' if len(set(pe.values())) == 1 else '*** DIFIEREN'}")
    mal = CF.cruza_cod0(res, [dict(d, cod=CF.diagnostico(d['seed'], nk, ktop, BASE)['cod']) for d in diags])
    log(f"  CRUCE cod0 contra escala_codigo (bloque 0): "
        f"{'IDENTICO campo a campo' if not mal else '*** DIFIERE en ' + str(mal[:5])}")
    seg = sum(t_b.values()) / len(plan) * (T / Tb)
    n_corr = len(ORDEN) * N_SEM
    log(f"ESTIMACION del bloque: {n_corr} corridas de {T} pasos, ~{seg:.1f} s/corrida en serie -> "
        f"~{n_corr*seg/N_PARALELO/60:.1f} min de pared con Pool({N_PARALELO}).")
    log("HUMO: numeros observados, sin ajustar nada. n<=2 y semillas vistas: NO son evidencia.")

    dj = os.path.join(RAIZ, 'datos', f'familias_b3_humo_{stamp}.json')
    with open(dj, 'w', encoding='utf-8') as f:
        json.dump(dict(meta=dict(fecha=time.strftime('%Y-%m-%dT%H:%M:%S'), tipo='humo', T_brazo=Tb, semillas=sem,
                                 T_bloque=T, nk=nk, ktop=ktop, nkmax=nkmax, brazos=N(BRAZOS), umbrales=UMBRALES,
                                 umbrales_b3=UMBRALES_B3, shas=SHAS(), segundos_por_brazo=t_b, plan=plan,
                                 cruce_cod0_ok=(not mal), python=platform.python_version(), numpy=np.__version__),
                       identidades=ident, diagnostico=diags, brazos=res), f, ensure_ascii=False, default=str)
    log(f"datos -> {os.path.basename(dj)}  sha256_16 = {h16(dj)}")
    CF._log['f'].close()


# ---------------------------------------------------------------- principal
if __name__ == '__main__':
    arg = lambda n, d: (type(d)(sys.argv[sys.argv.index(n) + 1]) if n in sys.argv else d)
    nk, ktop, nkmax = arg('--nk', 30), arg('--k', 3), arg('--nkmax', 90)
    if '--brazos' in sys.argv:
        BRAZOS_ACTIVOS = [b.strip() for b in sys.argv[sys.argv.index('--brazos') + 1].split(',') if b.strip()]
        malos = [b for b in BRAZOS_ACTIVOS if b not in BRAZOS]
        if malos:
            raise SystemExit(f"--brazos: desconocido(s) {malos}. Validos: {ORDEN}")
        for req in ('S-REL', 'S-REL0', 'S-EXC', 'S-LIN', 'G-LIN', 'G-REL'):
            if req not in BRAZOS_ACTIVOS:
                raise SystemExit(f"--brazos: {req} es obligatorio (PS1/PS4/PG1 lo necesitan).")
    if '--humo' in sys.argv:
        humo(nk, ktop, nkmax, arg('--T', T)); sys.exit(0)

    import multiprocessing as mp
    mp.set_start_method('spawn', force=True)
    T = arg('--T', T)
    desde = arg('--desde', DESDE)
    SEEDS = list(range(desde, desde + N_SEM))
    stamp = time.strftime('%Y%m%d_%H%M%S')
    CF._log['f'] = open(os.path.join(RAIZ, 'datos', f'familias_b3_s{SEEDS[0]}-{SEEDS[-1]}_{stamp}.log'),
                        'w', encoding='utf-8', newline='\n')
    CF._log['t0'] = time.time()
    log(f"ARRANQUE BLOQUE 3 (v15f en el mundo de familias): brazos {BRAZOS_ACTIVOS}, "
        f"semillas {SEEDS[0]}-{SEEDS[-1]}, T={T}. Pool({N_PARALELO}).")
    log("El mundo es el del bloque 2 SIN TOCAR. Lo unico que cambia entre brazos es `memoria_pares` (None|'relevo').")
    for k, v in SHAS().items():
        log(f"    sha {k:26s} {v}")
    if not guarda_origen():
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
        ctrl = [('ID', c, s, T_ID) for c in CASOS_ID for s in SEMILLAS_ID]
        log(f"ETAPA 1/3 — IDENTIDAD ({len(CASOS_ID)} casos x {len(SEMILLAS_ID)} = {len(ctrl)}). "
            f"(A) e (y) DEBEN fallar: sin ellos la etapa pasa por vacuidad.")
        rc = pool.map(tarea, ctrl, chunksize=1)
        for cual in CASOS_ID:
            g = [r for r in rc if r['cual'] == cual]
            log(f"    {CASOS_ID[cual][0]:58s} {sum(r['ok'] for r in g)}/{len(g)}"
                + ("" if all(r['ok'] for r in g) else f"   difieren {g[0]['difieren']} faltan {g[0]['faltan']}"))
            V[f'ID_{cual}'] = all(r['ok'] for r in g)
        V['G_IDENTIDAD'] = bool(all(V[f'ID_{c}'] for c in CASOS_ID))
        log(f"  IDENTIDAD {sum(r['ok'] for r in rc)}/{len(rc)}")
        if not V['G_IDENTIDAD']:
            log("*** GUARDA DE IDENTIDAD FALLIDA. Se para (PI).")
            sys.exit(1)

        log(f"ETAPA 2/3 — DIAGNOSTICO ESTRUCTURAL, ANTES de simular ({len(SEEDS)} semillas, T = 0).")
        diags = pool.map(tarea, [('D', s, nk, ktop) for s in SEEDS], chunksize=1)
        log(f"    alias por par mediana {med([d['alias_pares'] for d in diags])}  "
            f"semillas con algun par identico {sum(d['alias_semilla'] for d in diags)}/{len(diags)}  "
            f"U3 mediana {med([d['U3'] for d in diags])}")

        tr = [('R', b, s, T, nk, ktop, nkmax) for b in BRAZOS_ACTIVOS for s in SEEDS]
        log(f"ETAPA 3/3 — principal: {len(tr)} corridas de {T} pasos "
            f"({len(BRAZOS_ACTIVOS)} brazos x {len(SEEDS)} semillas)...")
        for i, r in enumerate(pool.imap_unordered(tarea, tr, chunksize=1), 1):
            res.append(r)
            if i % 20 == 0 or i == len(tr):
                log(f"          {i}/{len(tr)}")

    log()
    mal = CF.cruza_cod0(res, [dict(d, cod=CF.diagnostico(d['seed'], nk, ktop, BASE)['cod']) for d in diags])
    log(f"CRUCE cod0 contra escala_codigo (bloque 0): "
        f"{'IDENTICO campo a campo' if not mal else '*** DIFIERE en ' + str(mal[:5])}")
    V['cruce_cod0_ok'] = (not mal)
    log("ANALISIS — medianas y cuartiles por brazo, y los umbrales EXACTOS (la letra del bloque 2, importada).")
    V.update(veredicto(res, SEEDS, diags))
    for b, d in V['linea_base'].items():
        log(f"    {b:7s} muertes {d['muertes']} q{d['q_muertes']}  celdas {d['celdas']}  splits {d['splits']}  "
            f"exp_total {d['exp_total']}  leen_tabla {d['mem']}")
    ver = frase_final(V)
    log(); log(f"VEREDICTO: {ver}")

    meta = dict(fecha=time.strftime('%Y-%m-%dT%H:%M:%S'), semillas=SEEDS, T=T, nk=nk, ktop=ktop, nkmax=nkmax,
                brazos={b: N(BRAZOS[b]) for b in BRAZOS_ACTIVOS}, veredicto=ver, veredictos=N(V),
                identidades=rc, diagnostico=diags, procesos_python=ps, shas=SHAS(),
                python=platform.python_version(), numpy=np.__version__)
    dj = os.path.join(RAIZ, 'datos', f'familias_b3_s{SEEDS[0]}-{SEEDS[-1]}_{stamp}.json')
    with open(dj, 'w', encoding='utf-8') as f:
        json.dump(dict(meta=meta, principal=res), f, ensure_ascii=False, default=str)
    log(f"datos -> {os.path.basename(dj)}  sha256_16 = {h16(dj)}")
    CF._log['f'].close()
