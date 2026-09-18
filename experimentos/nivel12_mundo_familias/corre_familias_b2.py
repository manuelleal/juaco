"""BLOQUE 2 -- CAPACIDAD DIRECTA: generalizar a la variante NUNCA VISTA y separar la variante que DEJA DE
COMPORTARSE IGUAL, con v14.1 SIN CAMBIOS. Ejecuta PREREGISTRO_bloque2_variante.md (su sha va en el meta del JSON).

MISION (primero, siempre): llegar a la AGI por este camino -- un organismo minimo con reglas locales (sin backprop
en el runtime) que aprende, desaprende, generaliza, sobrevive y se reproduce, con evidencia preregistrada.

    python experimentos/nivel12_mundo_familias/corre_familias_b2.py --humo      (UN proceso, sin Pool: el disenador)
    python experimentos/nivel12_mundo_familias/corre_familias_b2.py [--desde 461] [--T 100000] [--brazos G-EXC,...]

REGLA 3 y 11: el `Pool` lo lanza SOLO el coordinador, y nunca con otro `Pool` vivo. `--humo` es UN proceso.
REGLA 10: log desde el arranque, con fsync, una linea por etapa con marca de tiempo.
ERR-31: TODOS los umbrales viven en el dict UMBRALES, cada uno con la FRASE LITERAL del preregistro al lado.
ERR-38/41/42/E.6: este runner IMPORTA `corre_familias.py` (bloque 1) y `escala_codigo.py` (bloque 0) y no copia ni
el diagnostico estructural, ni el cruce de `cod0`, ni la estadistica. El humo ESCRIBE su JSON.
ERR-44 / T-E: TODO se mide sobre lo que LEE LA BOCA (`log`, `primera_b2`, `sep_exp`), nunca sobre pesos internos.

Etapas:
  1/3 IDENTIDAD (subconjunto critico del arnes de 63; el completo va en identidad_familias_b2.py). Si falla, ABORTA.
  2/3 DIAGNOSTICO ESTRUCTURAL, ANTES de simular: alias exacto por par y por semilla, U3, y la etiqueta
      SEPARABLE/ALIAS de las 8 variantes RETENIDAS (escenario G) y de las 8 VIRADAS (escenario S).
  3/3 PRINCIPAL: 10 brazos x 20 semillas (461-480; replica 481-500 con --desde 481) + el ancla V14.
"""
import sys, os, json, time, hashlib, platform, subprocess

sys.stdout.reconfigure(encoding='utf-8', errors='replace')
AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
CREB = os.path.join(RAIZ, 'experimentos', 'creacion_B')
sys.path[:0] = [AQUI, CREB, os.path.join(RAIZ, 'organismo')]   # organismo/ PRIMERO (ERR-28)
import numpy as np
import corre_familias as CF          # bloque 1: log, medianas, A12, diagnostico estructural, cruce de cod0

T = 100000
T_ID = 20000
N_PARALELO = 14
N_SEM = 20
DESDE = 461
SEMILLAS_ID = [1, 2, 3]              # ninguna de 461-500 queda expuesta (E.14)
SHA_V14_ESPERADO = 'feefc88b1fd8d434'
SHA_MF_ESPERADO = 'b9dd561a0cf056b8'
SHA_ESCALA_ESPERADO = 'd8b8566bca77a0ae'
CRIT = 0.5                           # crit_exp: |v| minimo para que una lectura cuente como lectura

log, h16, N, med, cuartiles, razon, A12, cuenta = CF.log, CF.h16, CF.N, CF.med, CF.cuartiles, CF.razon, CF.A12, CF.cuenta

# ---------------------------------------------------------------- el mundo (los valores PREREGISTRADOS)
# Se hereda TODO del bloque 1 y su enmienda 1: renovacion simetrica (renov=1.0), L=160 y nobj=16 DERIVADOS
# (densidad 0.10 y distancia media 5, las del tronco), dureza 4 -> costo 0.008 (ERR-47, escalera ya ejecutada),
# NK/NKMAX/K los del TRONCO con D=12 (el alias se DECLARA, no se elimina: ERR-45).
BASE = dict(mundo='familias', renov=1.0, largo=160, nobj=16, fam_D=12, fam_nvar=3, fam_F=8, fam_V=3,
            n_neu=0, vent=10000, crit_exp=CRIT, costo=0.008, log_cada=250, reg_b2=1, desambiguar=0)
# ESCENARIO G: la deriva RETIENE la tercera variante (deriva = T/3 + 1 -> fases v0 | v1 | v2). vira=-1: nada cambia.
GEN = dict(BASE, _deriva_tercio=True, cambio=10**9, vira=0, exc_evita=2)   # cambio fuera del horizonte: NADA cambia nunca
# ESCENARIO S: las tres variantes circulan (deriva 5000) y en T/2 la VIRADA de cada token cambia de consecuencia.
SAL = dict(BASE, deriva=5000, _cambio_mitad=True, exc_evita=-1, n_exc=0)
BRAZOS = {
    'G-EXC':  dict(GEN, n_exc=8, fam_val='familia'),    # v14.1 en el mundo con 8 excepciones VISTAS
    'G-LIN':  dict(GEN, n_exc=0, fam_val='familia'),    # referencia: familias sin contradiccion
    'G-AZA':  dict(GEN, n_exc=0, fam_val='azar'),       # consecuencias al azar por estimulo: no hay familia
    'G-BAR':  dict(GEN, n_exc=0, fam_val='barajado'),   # la variante toma la valencia del token SIGUIENTE
    'S-EXC':  dict(SAL, vira=8, fam_val='familia'),     # la sal rosa: 8 variantes cambian en T/2
    'S-LIN':  dict(SAL, vira=-8, fam_val='familia'),    # gemelo EXACTO de S-EXC hasta T/2: declara las MISMAS 8, no cambia ninguna
    'S-AZA':  dict(SAL, vira=8, fam_val='azar'),
    'S-AZA0': dict(SAL, vira=-8, fam_val='azar'),
    'S-BAR':  dict(SAL, vira=8, fam_val='barajado'),
    'S-BAR0': dict(SAL, vira=-8, fam_val='barajado'),
    'V14':    dict(mundo='AB'),                          # ancla: v14.1 literal, costo del tronco. NO compite.
}
ORDEN = ['G-EXC', 'G-LIN', 'G-AZA', 'G-BAR', 'S-EXC', 'S-LIN', 'S-AZA', 'S-AZA0', 'S-BAR', 'S-BAR0', 'V14']
BRAZOS_ACTIVOS = list(ORDEN)
PAREJAS_S = [('S-EXC', 'S-LIN'), ('S-AZA', 'S-AZA0'), ('S-BAR', 'S-BAR0')]
DELTAS = [0, 2500, 10000, 25000]     # puntos de medida de las hermanas, relativos a `cambio`

CASOS_ID = {   # subconjunto critico del arnes de 63 (identidad_familias_b2.py lo corre entero)
    'a': ("(a) vira=0,exc_evita=-1,reg_b2=0 == organismo_familias (AB)", 'MF', dict(), dict(), False, T_ID),
    'k': ("(k) mundo=AB == organismo_v14 (TRONCO)", 'V14', dict(), dict(), False, T_ID),
    'f': ("(f) mundo=familias del bloque 1 == organismo_familias", 'MF', dict(mundo='familias', renov=1.0,
          largo=160, nobj=16, n_exc=4), dict(mundo='familias', renov=1.0, largo=160, nobj=16, n_exc=4), False, T_ID),
    'q': ("(q) GEMELO: vira=8 == vira=-8 ANTES del cambio (P-S1)", 'B2', dict(), dict(), False, 0),
    'v': ("(v) vira=8 != vira=-8 DESPUES del cambio (DEBE diferir)", 'B2', dict(), dict(), True, 0),
    'x': ("(x) mundo=familias != mundo=AB (DEBE diferir)", 'V14', dict(), dict(mundo='familias', renov=1.0,
          largo=160, nobj=16, n_exc=4), True, T_ID),
}

# ---------------------------------------------------------------- UMBRALES: la LETRA del preregistro (ERR-31)
UMBRALES = {
    'PG1': dict(frase="GENERALIZA: en G-LIN, g1 (acierto de signo 1/0.5/0 en la PRIMERA exposicion a la variante "
                      "nunca vista) mediana >= 0.75 Y g1 >= 0.75 en >= 15/20 semillas; refuta si mediana <= 0.60 "
                      "o si <= 11/20; entre medias, INDECISO",
                med_pasa=0.75, n_pasa=15, med_refuta=0.60, n_refuta=11),
    'PG2': dict(frase="AZAR EN BANDA (puerta de validez): en G-AZA, g1 mediana en [0.35, 0.65]. Fuera de banda: "
                      "el mundo `azar` no es azar para esta medida -> PG1, PG3 y PG4 no se leen",
                lo=0.35, hi=0.65),
    'PG3': dict(frase="DE DONDE HEREDA: en G-BAR (la variante lleva la valencia del token SIGUIENTE, opuesta a la "
                      "de su propio token) g1 mediana <= 0.35 Y g1(BAR) < g1(LIN) pareado en >= 17/20; refuta si "
                      "mediana >= 0.50 -> la lectura de la variante nunca vista NO viene del token",
                med_pasa=0.35, n_pasa=17, med_refuta=0.50),
    'PG4': dict(frase="CONTRA LIN: g1(G-EXC) < g1(G-LIN) pareado en >= 14/20 Y razon de medianas <= 0.90; refuta "
                      "la IGUALDAD si |mediana(EXC)-mediana(LIN)| <= 0.05 y EXC<LIN en 8-12/20 -> 'ocho "
                      "excepciones vistas no danan la generalizacion a la variante nunca vista'",
                n_pasa=14, razon_pasa=0.90, dif_refuta=0.05, n_lo=8, n_hi=12),
    'PG5': dict(frase="CONDUCTA (acompana): cond1 (mordio comida / rechazo veneno en la primera exposicion) "
                      "G-LIN > G-BAR pareado en >= 14/20. Se reporta siempre con ruta1 y el hambre de esa visita",
                n_pasa=14),
    'PS1': dict(frase="GEMELO (puerta): S-EXC y S-LIN comparten prefijo EXACTO de `log` hasta `cambio` en 20/20 "
                      "semillas (y lo mismo cada pareja de AZA y BAR). Si falla, es el instrumento y se para",
                n_min=20),
    'PS2': dict(frase="SEPARA TARDE Y A MEDIAS: en S-EXC, n_sep mediana <= 5 de 8 Y sep_exp >= 2.0 x exp_asoc de "
                      "los mismos estimulos, pareado en >= 14/20; refuta si n_sep mediana >= 7 Y sep_exp <= 1.0 x "
                      "exp_asoc en >= 14/20 -> 'v14.1 ya separa la variante sin organo nuevo'",
                nsep_pasa=5, factor_pasa=2.0, n_pasa=14, nsep_refuta=7, factor_refuta=1.0),
    'PS3': dict(frase="ASIMETRIA DE LA PUERTA: entre las 8 viradas, separan mas las que ERAN COMIDA que las que "
                      "ERAN VENENO (la puerta por evidencia del codigo exacto solo se abre con MORDIDAS, y el "
                      "veneno se rechaza), pareado en >= 14/20; refuta con <= 11/20",
                n_pasa=14, n_refuta=11),
    'PS4': dict(frase="DANO A LAS HERMANAS, CONTRA LIN: dano_herm(10000) = ok_herm(S-LIN) - ok_herm(S-EXC) en "
                      "cambio+10000, pareado: mediana >= 0.10 Y > 0 en >= 15/20; refuta si mediana <= 0.02 o si "
                      "> 0 en <= 11/20 -> 'separar la variante no le cuesta a las hermanas'",
                delta=10000, med_pasa=0.10, n_pasa=15, med_refuta=0.02, n_refuta=11),
    'PS5': dict(frase="EL DANO ES DE FAMILIA: dano_herm(10000) de la pareja `familia` > el de la pareja `azar` Y "
                      "> el de la pareja `barajado`, en medianas y pareado en >= 14/20 cada uno; si alguno lo "
                      "iguala o lo supera, el dano no es especifico de la familia y PS4 no se declara como tal",
                n_pasa=14),
    'PS6': dict(frase="RETENCION (se reporta, no decide): ok_vir en el ULTIMO punto de log -- fraccion de las 8 "
                      "viradas leidas con su valencia NUEVA al final de la corrida"),
    'PI': dict(frase="INSTRUMENTO (puerta): arnes 63/63 (aqui su subconjunto critico); sha organismo_familias.py "
                     "== b9dd561a0cf056b8; sha organismo_v14.py == feefc88b1fd8d434; cruce cod0 campo a campo"),
}


def resuelve(kw, Ti):
    """`deriva` y `cambio` se DERIVAN de T (no son perillas libres): deriva = T/3+1 retiene la tercera variante;
    cambio = T/2 es la mitad de la corrida."""
    kw = dict(kw)
    if kw.pop('_deriva_tercio', False):
        kw['deriva'] = Ti // 3 + 1
    if kw.pop('_cambio_mitad', False):
        kw['cambio'] = Ti // 2
    return kw


# ---------------------------------------------------------------- lectura de una corrida (SOLO conducta de la boca)
def obj_de(v):
    return 1.0 if v == 'comida' else (-1.0 if v == 'veneno' else 0.0)


def lee_G(r):
    """ESCENARIO G. La PRIMERA exposicion a la variante RETENIDA (indice V-1: la que la deriva no presenta hasta
    2T/3). Puntuacion G1 de DISENO_grafo_tokens: 1 acierto / 0.5 abstencion / 0 error."""
    F, V = r['fam']['F'], r['fam']['V']
    pb, val = r['primera_b2'], r['val_mundo']
    nombres = ['T%dv%d' % (k, V - 1) for k in range(F)]
    g1 = []; g1f = []; cd = []; rt = []; hm = []; lenta = []; t1 = []
    for n in nombres:
        e = pb.get(n)
        if e is None:
            continue
        t, wt, o, ruta, mordio, hambre, ws, wf = e
        if not o:
            continue
        t1.append(t)
        g1.append(1.0 if wt * o > 0 else (0.0 if wt * o < 0 else 0.5))
        g1f.append(1.0 if (wt * o > 0 and abs(wt) >= CRIT) else (0.0 if (wt * o < 0 and abs(wt) >= CRIT) else 0.5))
        cd.append(1.0 if ((mordio and o > 0) or (not mordio and o < 0)) else 0.0)
        rt.append(float(ruta)); hm.append(hambre)
        lenta.append(1.0 if ws * o > 0 else (0.0 if ws * o < 0 else 0.5))
    f = lambda xs: (round(float(np.mean(xs)), 4) if xs else None)
    return dict(n_vista=len(g1), n_total=len(nombres), g1=f(g1), g1_fuerte=f(g1f), cond1=f(cd), ruta1=f(rt),
                hambre1=f(hm), g1_lenta=f(lenta), t_primera=(min(t1) if t1 else None),
                retenida_ok=bool(t1 and min(t1) >= 2 * r['fam']['deriva']))


def traza(r):
    """Trayectoria de la boca leida del `log` (perilla log_cada de v14.1: valor(P) ruteado, lo que usa la boca).
    Devuelve, en `cambio` y en cambio+DELTAS, la fraccion de HERMANAS y de VIRADAS leidas bien (signo correcto con
    la valencia VIGENTE en ese instante y |v| >= crit_exp)."""
    nom = sorted(r['val_mundo'])
    idx = {n: i + 1 for i, n in enumerate(nom)}
    val0, vpost, camb = r['val_mundo'], r['val_post'], r['cambio_b2']
    vir = list(r['viradas'])
    herm = sorted({h for e in vir for h in r['herm'][e]} - set(vir))
    def frac(fila, grupo):
        t = fila[0]; ok = []
        for n in grupo:
            o = obj_de(vpost[n] if (t >= camb and n in vpost) else val0[n])
            if not o:
                continue
            v = fila[idx[n]]
            ok.append(1.0 if (v * o > 0 and abs(v) >= CRIT) else 0.0)
        return (round(float(np.mean(ok)), 4) if ok else None)
    filas = r['log']
    def cerca(t):
        return min(filas, key=lambda f: abs(f[0] - t)) if filas else None
    out = {'n_herm': len(herm), 'n_vir': len(vir)}
    for d in DELTAS:
        f = cerca(camb + d)
        out[f'ok_herm_{d}'] = frac(f, herm) if f else None
        out[f'ok_vir_{d}'] = frac(f, vir) if f else None
    ult = filas[-1] if filas else None
    out['ok_herm_fin'] = frac(ult, herm) if ult else None
    out['ok_vir_fin'] = frac(ult, vir) if ult else None
    out['t_fin'] = (ult[0] if ult else None)
    out['prefijo'] = hashlib.sha256(json.dumps([f for f in filas if f[0] < camb]).encode()).hexdigest()[:16]
    return out


def lee_S(r):
    """ESCENARIO S. Exposiciones hasta SEPARAR la virada de sus hermanas, contra lo que le costo APRENDERLA, y la
    asimetria comida/veneno declarada antes (PS3)."""
    vir = list(r['viradas'])
    sep, ea, val0 = r['sep_exp'], r['exp_asoc'], r['val_mundo']
    s = [sep.get(e) for e in vir]
    a = [ea.get(e) for e in vir]
    par = [(sep[e], ea[e]) for e in vir if sep.get(e) is not None and ea.get(e) is not None]
    era_c = [e for e in vir if val0[e] == 'comida']
    era_v = [e for e in vir if val0[e] == 'veneno']
    f = lambda xs: med([x for x in xs if x is not None])
    return dict(n_vir=len(vir), n_sep=sum(1 for x in s if x is not None), sep_med=f(s), apr_med=f(a),
                sep_apr=(round(float(np.median([x / y for x, y in par if y])), 3)
                         if [1 for x, y in par if y] else None),
                n_sep_comida=sum(1 for e in era_c if sep.get(e) is not None), n_comida=len(era_c),
                n_sep_veneno=sum(1 for e in era_v if sep.get(e) is not None), n_veneno=len(era_v),
                sep_exp={e: sep.get(e) for e in vir}, viradas=vir)


def resumen(brazo, seed, r, kw):
    if r.get('mundo') in (None, 'AB'):
        return dict(tipo='R', brazo=brazo, seed=seed, mundo='AB', deaths=r['deaths'], celdas=r['celdas'],
                    splits=r['splits'], W=r['W'])
    esc = brazo.split('-')[0]
    d = dict(tipo='R', brazo=brazo, esc=esc, seed=seed, mundo=r['mundo'],
             deaths=r['deaths'], celdas=r['celdas'], splits=r['splits'],
             frac_regalo=r['frac_regalo'], frac_veneno=r['frac_veneno'], renovados=r['renovados'],
             ruta=r['ruta'], exc=r['exc'], exc_win=r['exc_win'], cod0=r['cod0'],
             exp_total=sum(v for v in r['exp_asoc'].values() if v is not None),
             exposiciones=r['exposiciones'],
             razon_exp=razon(sum(v for k, v in r['exposiciones'].items() if r['val_mundo'][k] == 'veneno'),
                             sum(v for k, v in r['exposiciones'].items() if r['val_mundo'][k] == 'comida')))
    if esc == 'G':
        d.update(G=lee_G(r), retenidas=['T%dv%d' % (k, r['fam']['V'] - 1) for k in range(r['fam']['F'])])
    else:
        d.update(S=lee_S(r), traza=traza(r))
    return d


# ---------------------------------------------------------------- tareas
def tarea(args):
    tipo = args[0]
    if tipo == 'ID':
        _, cual, seed, Ti = args
        import organismo_v14 as V14, organismo_familias as MF, organismo_familias_b2 as B2
        etiq, ref, kwa, kwb, debe, Tc = CASOS_ID[cual]
        Tc = Tc or Ti
        if ref == 'B2':                                  # el gemelo del bloque 2, a los dos lados de `cambio`
            kw = resuelve(BRAZOS['S-EXC'], Ti)
            kw.pop('vira')
            Tg = (kw['cambio'] - 1) if cual == 'q' else (kw['cambio'] + 3 * kw['deriva'])
            a = B2.run(seed, T=Tg, vira=8, **kw); b = B2.run(seed, T=Tg, vira=-8, **kw)
            salta = ('vira', 'val_post', 'sep_exp')
        elif ref == 'MF':
            a = MF.run(seed, T=Tc, **kwa); b = B2.run(seed, T=Tc, **kwb); salta = ()
        else:
            a = V14.run(seed, T=Tc, **kwa); b = B2.run(seed, T=Tc, **kwb); salta = ()
        dif = [k for k in a if k not in salta and N(a[k]) != N(b.get(k))]
        falta = [k for k in a if k not in b and k not in salta]
        igual = not dif and not falta
        return dict(tipo='ID', cual=cual, etiqueta=etiq, seed=seed, identico=igual, debe_diferir=debe,
                    ok=bool(igual != debe), difieren=dif[:6], faltan=falta)
    if tipo == 'D':
        _, seed, nk, ktop = args
        d = CF.diagnostico(seed, nk, ktop, BASE)
        d.pop('cod')
        return dict(tipo='D', **d)
    _, brazo, seed, Ti, nk, ktop, nkmax = args
    import organismo_familias_b2 as B2
    kw = resuelve(BRAZOS[brazo], Ti)
    if kw.get('mundo') != 'AB':
        kw.update(nk=nk, ktop=ktop, nkmax=nkmax)
    return resumen(brazo, seed, B2.run(seed, T=Ti, **kw), kw)


SHAS = lambda: dict(
    preregistro=h16(os.path.join(AQUI, 'PREREGISTRO_bloque2_variante.md')),
    script=h16(os.path.abspath(__file__)),
    constructor=h16(os.path.join(AQUI, 'construye_familias_b2.py')),
    instrumento=h16(os.path.join(AQUI, 'organismo_familias_b2.py')),
    arnes=h16(os.path.join(AQUI, 'identidad_familias_b2.py')),
    origen_organismo_familias=h16(os.path.join(AQUI, 'organismo_familias.py')),
    runner_bloque1=h16(os.path.join(AQUI, 'corre_familias.py')),
    escala_codigo_bloque0=h16(os.path.join(AQUI, 'escala_codigo.py')),
    origen_organismo_v14=h16(os.path.join(RAIZ, 'organismo', 'organismo_v14.py')))


def guarda_origen():
    s = SHAS()
    ok = True
    for k, esp in [('origen_organismo_v14', SHA_V14_ESPERADO), ('origen_organismo_familias', SHA_MF_ESPERADO),
                   ('escala_codigo_bloque0', SHA_ESCALA_ESPERADO)]:
        if s[k] != esp:
            log(f"*** ORIGEN CAMBIADO: {k} es {s[k]}, se esperaba {esp}. Reconstruir por anclas y repetir el arnes.")
            ok = False
    return ok


def ventanas(diag, nombres):
    """Subconjunto preregistrado (regla 10): SEPARABLE si el codigo inicial no coincide con el de ningun otro."""
    return {e: ('ALIAS' if diag['ident'].get(e) else 'SEPARABLE') for e in nombres}


# ---------------------------------------------------------------- veredicto (umbrales EXACTOS del preregistro)
def veredicto(res, SEEDS, diags):
    G = {b: {r['seed']: r for r in res if r['brazo'] == b} for b in BRAZOS_ACTIVOS}
    gg = lambda b, c: {s: (G.get(b, {}).get(s, {}).get('G') or {}).get(c) for s in SEEDS if s in G.get(b, {})}
    ss = lambda b, c: {s: (G.get(b, {}).get(s, {}).get('S') or {}).get(c) for s in SEEDS if s in G.get(b, {})}
    tz = lambda b, c: {s: (G.get(b, {}).get(s, {}).get('traza') or {}).get(c) for s in SEEDS if s in G.get(b, {})}
    V = {'umbrales': UMBRALES}

    V['alias'] = dict(pares_mediana=med([d['alias_pares'] for d in diags]),
                      semillas_con_alias=sum(d['alias_semilla'] for d in diags), n=len(diags),
                      U3_mediana=med([d['U3'] for d in diags]))

    # --- PG1: generaliza a la variante nunca vista (en G-LIN)
    u = UMBRALES['PG1']; d1 = gg('G-LIN', 'g1'); v1 = [v for v in d1.values() if v is not None]
    n1 = sum(1 for v in v1 if v >= u['med_pasa'])
    V['PG1'] = dict(med=med(v1), q=cuartiles(v1), n_ge=n1, n=len(v1),
                    g1_fuerte=med(list(gg('G-LIN', 'g1_fuerte').values())),
                    g1_lenta=med(list(gg('G-LIN', 'g1_lenta').values())),
                    ruta1=med(list(gg('G-LIN', 'ruta1').values())),
                    n_vista=med(list(gg('G-LIN', 'n_vista').values())),
                    retenida_ok=sum(1 for v in gg('G-LIN', 'retenida_ok').values() if v))
    V['PG1']['pasa'] = bool(V['PG1']['med'] is not None and V['PG1']['med'] >= u['med_pasa'] and n1 >= u['n_pasa'])
    V['PG1']['refuta'] = bool(V['PG1']['med'] is not None and (V['PG1']['med'] <= u['med_refuta'] or n1 <= u['n_refuta']))

    # --- PG2: azar en banda (puerta de validez)
    u = UMBRALES['PG2']; va = [v for v in gg('G-AZA', 'g1').values() if v is not None]
    V['PG2'] = dict(med=med(va), q=cuartiles(va))
    V['PG2']['pasa'] = bool(V['PG2']['med'] is not None and u['lo'] <= V['PG2']['med'] <= u['hi'])

    # --- PG3: de donde hereda la variante nunca vista
    u = UMBRALES['PG3']; db = gg('G-BAR', 'g1'); vb = [v for v in db.values() if v is not None]
    nb = cuenta(db, d1, SEEDS, lambda x, y: x < y)
    V['PG3'] = dict(med_BAR=med(vb), q_BAR=cuartiles(vb), med_LIN=med(v1), n_menor=nb, n=len(SEEDS),
                    A12=A12(vb, v1), g1_lenta_BAR=med(list(gg('G-BAR', 'g1_lenta').values())))
    V['PG3']['pasa'] = bool(V['PG3']['med_BAR'] is not None and V['PG3']['med_BAR'] <= u['med_pasa'] and nb >= u['n_pasa'])
    V['PG3']['refuta'] = bool(V['PG3']['med_BAR'] is not None and V['PG3']['med_BAR'] >= u['med_refuta'])

    # --- PG4: contra LIN (las excepciones VISTAS envenenan la generalizacion?)
    u = UMBRALES['PG4']; de = gg('G-EXC', 'g1'); ve = [v for v in de.values() if v is not None]
    ne = cuenta(de, d1, SEEDS, lambda x, y: x < y)
    rz = razon(med(ve), med(v1))
    dif = (abs(med(ve) - med(v1)) if (med(ve) is not None and med(v1) is not None) else None)
    V['PG4'] = dict(med_EXC=med(ve), q_EXC=cuartiles(ve), med_LIN=med(v1), razon=rz, n_menor=ne, n=len(SEEDS),
                    A12=A12(ve, v1), dif=dif)
    V['PG4']['pasa'] = bool(ne >= u['n_pasa'] and rz is not None and rz <= u['razon_pasa'])
    V['PG4']['refuta'] = bool(dif is not None and dif <= u['dif_refuta'] and u['n_lo'] <= ne <= u['n_hi'])

    # --- PG5: conducta en la primera exposicion
    u = UMBRALES['PG5']; cl, cb = gg('G-LIN', 'cond1'), gg('G-BAR', 'cond1')
    nc = cuenta(cl, cb, SEEDS, lambda x, y: x > y)
    V['PG5'] = dict(med_LIN=med(list(cl.values())), med_BAR=med(list(cb.values())),
                    med_EXC=med(list(gg('G-EXC', 'cond1').values())),
                    med_AZA=med(list(gg('G-AZA', 'cond1').values())),
                    hambre1=med(list(gg('G-LIN', 'hambre1').values())), n_mayor=nc, n=len(SEEDS))
    V['PG5']['pasa'] = bool(nc >= u['n_pasa'])

    # --- PS1: el gemelo (puerta)
    u = UMBRALES['PS1']; pre = {}
    for a, b in PAREJAS_S:
        pa, pb = tz(a, 'prefijo'), tz(b, 'prefijo')
        pre[f'{a}/{b}'] = sum(1 for s in SEEDS if pa.get(s) is not None and pa.get(s) == pb.get(s))
    V['PS1'] = dict(parejas=pre, n=len(SEEDS))
    V['PS1']['pasa'] = bool(pre and all(v >= min(u['n_min'], len(SEEDS)) for v in pre.values()))

    # --- PS2: separa tarde y a medias
    u = UMBRALES['PS2']; ns = ss('S-EXC', 'n_sep'); sa = ss('S-EXC', 'sep_apr')
    nfac = sum(1 for v in sa.values() if v is not None and v >= u['factor_pasa'])
    nfac_r = sum(1 for v in sa.values() if v is not None and v <= u['factor_refuta'])
    V['PS2'] = dict(n_sep_med=med(list(ns.values())), q_n_sep=cuartiles(list(ns.values())),
                    sep_med=med(list(ss('S-EXC', 'sep_med').values())),
                    apr_med=med(list(ss('S-EXC', 'apr_med').values())),
                    sep_apr_med=med([v for v in sa.values() if v is not None]),
                    n_factor2=nfac, n_factor1=nfac_r, n=len(SEEDS))
    V['PS2']['pasa'] = bool(V['PS2']['n_sep_med'] is not None and V['PS2']['n_sep_med'] <= u['nsep_pasa']
                            and nfac >= u['n_pasa'])
    V['PS2']['refuta'] = bool(V['PS2']['n_sep_med'] is not None and V['PS2']['n_sep_med'] >= u['nsep_refuta']
                              and nfac_r >= u['n_pasa'])

    # --- PS3: asimetria comida/veneno (la puerta solo se abre con mordidas)
    u = UMBRALES['PS3']
    fc = {s: (ss('S-EXC', 'n_sep_comida')[s] / max(ss('S-EXC', 'n_comida')[s], 1))
          for s in SEEDS if ss('S-EXC', 'n_sep_comida').get(s) is not None}
    fv = {s: (ss('S-EXC', 'n_sep_veneno')[s] / max(ss('S-EXC', 'n_veneno')[s], 1))
          for s in SEEDS if ss('S-EXC', 'n_sep_veneno').get(s) is not None}
    na = cuenta(fc, fv, SEEDS, lambda x, y: x > y)
    V['PS3'] = dict(frac_comida=med(list(fc.values())), frac_veneno=med(list(fv.values())), n_mayor=na, n=len(SEEDS))
    V['PS3']['pasa'] = bool(na >= u['n_pasa'])
    V['PS3']['refuta'] = bool(na <= u['n_refuta'])

    # --- PS4 y PS5: dano a las hermanas, contra el gemelo
    u = UMBRALES['PS4']; dd = {}
    for a, b in PAREJAS_S:
        for D in DELTAS + ['fin']:
            ka, kb = tz(a, f'ok_herm_{D}'), tz(b, f'ok_herm_{D}')
            dd[f'{a}_{D}'] = {s: (kb[s] - ka[s]) for s in SEEDS
                              if ka.get(s) is not None and kb.get(s) is not None}
    dfam = dd.get(f'S-EXC_{u["delta"]}', {}); vf = list(dfam.values())
    npos = sum(1 for v in vf if v > 0)
    V['PS4'] = dict(med=med(vf), q=cuartiles(vf), n_pos=npos, n=len(vf), delta=u['delta'],
                    por_delta={f'S-EXC_{D}': med(list(dd.get(f'S-EXC_{D}', {}).values())) for D in DELTAS + ['fin']},
                    ok_herm_EXC={str(D): med(list(tz('S-EXC', f'ok_herm_{D}').values())) for D in DELTAS + ['fin']},
                    ok_herm_LIN={str(D): med(list(tz('S-LIN', f'ok_herm_{D}').values())) for D in DELTAS + ['fin']})
    V['PS4']['pasa'] = bool(V['PS4']['med'] is not None and V['PS4']['med'] >= u['med_pasa'] and npos >= u['n_pasa'])
    V['PS4']['refuta'] = bool(V['PS4']['med'] is not None and (V['PS4']['med'] <= u['med_refuta'] or npos <= u['n_refuta']))

    u = UMBRALES['PS5']
    daz, dba = dd.get(f'S-AZA_{UMBRALES["PS4"]["delta"]}', {}), dd.get(f'S-BAR_{UMBRALES["PS4"]["delta"]}', {})
    V['PS5'] = dict(med_familia=med(vf), med_azar=med(list(daz.values())), med_barajado=med(list(dba.values())),
                    n_mayor_azar=cuenta(dfam, daz, SEEDS, lambda x, y: x > y),
                    n_mayor_barajado=cuenta(dfam, dba, SEEDS, lambda x, y: x > y), n=len(SEEDS))
    V['PS5']['pasa'] = bool(V['PS5']['n_mayor_azar'] >= u['n_pasa'] and V['PS5']['n_mayor_barajado'] >= u['n_pasa'])

    # --- PS6: retencion (se reporta)
    V['PS6'] = dict(ok_vir_EXC={str(D): med(list(tz('S-EXC', f'ok_vir_{D}').values())) for D in DELTAS + ['fin']},
                    ok_vir_LIN={str(D): med(list(tz('S-LIN', f'ok_vir_{D}').values())) for D in DELTAS + ['fin']})

    # --- linea base por brazo
    V['linea_base'] = {b: dict(muertes=med([r['deaths'] for r in G[b].values()]),
                               q_muertes=cuartiles([r['deaths'] for r in G[b].values()]),
                               celdas=med([r['celdas'] for r in G[b].values()]),
                               splits=med([r['splits'] for r in G[b].values()]),
                               regalo=med([r.get('frac_regalo') for r in G[b].values()]),
                               exp_total=med([r.get('exp_total') for r in G[b].values()]),
                               razon_exp=med([r.get('razon_exp') for r in G[b].values()]))
                       for b in BRAZOS_ACTIVOS if b in G}
    return V


def frase_final(V):
    p = lambda k: ('pasa' if V.get(k, {}).get('pasa') else ('REFUTA' if V.get(k, {}).get('refuta') else 'indeciso'))
    if not V['PS1'].get('pasa'):
        return ("PS1 CAE: el gemelo de control no comparte prefijo exacto con su brazo -- es el INSTRUMENTO. "
                "Nada se lee, nada se declara.")
    if not V['PG2'].get('pasa'):
        return (f"PG2 CAE (azar {V['PG2']['med']} fuera de [0.35, 0.65]): la medida no tiene linea de azar en este "
                "mundo. PG1, PG3 y PG4 no se leen; primero el instrumento.")
    s = (f"CAPACIDAD 1 (variante nunca vista): g1 LIN {V['PG1']['med']} ({V['PG1']['n_ge']}/{V['PG1']['n']} "
         f">= 0.75) -> PG1 {p('PG1')}; azar {V['PG2']['med']}; BAR {V['PG3']['med_BAR']} -> PG3 {p('PG3')}; "
         f"EXC {V['PG4']['med_EXC']} contra LIN (razon {V['PG4']['razon']}, {V['PG4']['n_menor']}/20) -> "
         f"PG4 {p('PG4')}. ")
    s += (f"CAPACIDAD 2 (la variante que deja de comportarse igual): separa {V['PS2']['n_sep_med']} de 8, "
          f"sep/apr {V['PS2']['sep_apr_med']} -> PS2 {p('PS2')}; asimetria comida {V['PS3']['frac_comida']} contra "
          f"veneno {V['PS3']['frac_veneno']} -> PS3 {p('PS3')}; dano a las hermanas {V['PS4']['med']} "
          f"({V['PS4']['n_pos']}/{V['PS4']['n']} > 0) -> PS4 {p('PS4')}; especifico de familia -> "
          f"PS5 {'si' if V['PS5']['pasa'] else 'NO'}. ")
    s += (f"Retencion de la virada al final: {V['PS6']['ok_vir_EXC'].get('fin')}. "
          f"Alias por par {V['alias']['pares_mediana']}, semillas con alias "
          f"{V['alias']['semillas_con_alias']}/{V['alias']['n']} (covariable declarada, no puerta). ")
    return s + "20 semillas no cierran nada: piden replica en el rango siguiente (regla 12)."


# ---------------------------------------------------------------- humo (UN proceso, sin Pool, regla 3)
def humo(nk, ktop, nkmax, Tb):
    stamp = time.strftime('%Y%m%d_%H%M%S')
    CF._log['f'] = open(os.path.join(RAIZ, 'datos', f'familias_b2_humo_{stamp}.log'), 'w',
                        encoding='utf-8', newline='\n')
    CF._log['t0'] = time.time()
    log("HUMO del disenador del bloque 2, UN proceso, sin Pool (regla 3). PREREGISTRO_bloque2_variante.md.")
    log("Semillas 1-2: NINGUNA de las 461-500 del bloque queda expuesta (E.14).")
    for k, v in SHAS().items():
        log(f"    sha {k:26s} {v}")
    log(f"    origenes verificados -> {'OK' if guarda_origen() else 'FALLA'}")
    sem = [1, 2]

    log("1/3 IDENTIDAD (subconjunto; el arnes completo dio 63/63 en identidad_familias_b2.py).")
    ident = []
    for cual in CASOS_ID:
        for s in sem:
            ident.append(tarea(('ID', cual, s, 6000)))
        g = [r for r in ident if r['cual'] == cual]
        log(f"    {CASOS_ID[cual][0]:56s} {sum(r['ok'] for r in g)}/{len(g)}"
            + ("" if all(r['ok'] for r in g) else f"   difieren {g[0]['difieren']}"))
    log(f"  IDENTIDAD {sum(r['ok'] for r in ident)}/{len(ident)}")

    log("2/3 DIAGNOSTICO ESTRUCTURAL (antes de simular): alias exacto, U3 y las ventanas SEPARABLE/ALIAS.")
    diags = []
    for s in sem:
        d = CF.diagnostico(s, nk, ktop, BASE)
        diags.append(d)
        log(f"    semilla {s}: alias_pares {d['alias_pares']:.5f}  alias_semilla {d['alias_semilla']}  "
            f"U3 {d['U3']}  retenidas {ventanas(d, ['T%dv2' % k for k in range(8)])}")

    # EQUIPO regla 3: <= 6 corridas de un proceso. El encargo pide "2 semillas, brazos v14.1 y LIN"; se gastan
    # 4 en el escenario G (2 brazos x 2 semillas) y 2 en el escenario S (2 brazos x 1 semilla) = 6 EXACTAS.
    # Lo digo en vez de esconderlo: la pareja S de la semilla 2 NO se corre aqui.
    plan = [('G-EXC', 1), ('G-EXC', 2), ('G-LIN', 1), ('G-LIN', 2), ('S-EXC', 1), ('S-LIN', 1)]
    log(f"3/3 HUMO: {len(plan)} corridas de {Tb} pasos (regla 3: <= 6). Brazos v14.1 y LIN, semillas 1-2.")
    res, t_b = [], {}
    for b, s in plan:
        t1 = time.time(); r = tarea(('R', b, s, Tb, nk, ktop, nkmax)); dt = time.time() - t1
        res.append(r); t_b[b] = round(t_b.get(b, 0.0) + dt, 2)
        if r['esc'] == 'G':
            g = r['G']
            log(f"    {b:6s} s{s}  {dt:5.1f}s  g1 {g['g1']}  g1_fuerte {g['g1_fuerte']}  g1_lenta {g['g1_lenta']}  "
                f"cond1 {g['cond1']}  ruta1 {g['ruta1']}  hambre1 {g['hambre1']}  vistas {g['n_vista']}/8  "
                f"t_primera {g['t_primera']} (retenida_ok {g['retenida_ok']})  muertes {r['deaths']}  "
                f"celdas {r['celdas']}")
        else:
            S, z = r['S'], r['traza']
            log(f"    {b:6s} s{s}  {dt:5.1f}s  n_sep {S['n_sep']}/{S['n_vir']}  sep_med {S['sep_med']}  "
                f"apr_med {S['apr_med']}  comida {S['n_sep_comida']}/{S['n_comida']}  "
                f"veneno {S['n_sep_veneno']}/{S['n_veneno']}  muertes {r['deaths']}  celdas {r['celdas']}")
            log(f"            ok_herm " + " ".join(f"{D}:{z[f'ok_herm_{D}']}" for D in DELTAS)
                + f" fin:{z['ok_herm_fin']}   ok_vir "
                + " ".join(f"{D}:{z[f'ok_vir_{D}']}" for D in DELTAS) + f" fin:{z['ok_vir_fin']}"
                + f"   prefijo {z['prefijo']}")
    pe = [r['traza']['prefijo'] for r in res if r.get('esc') == 'S']
    log(f"  GEMELO (P-S1) en la semilla 1: prefijos {pe} -> "
        f"{'IDENTICOS (S-EXC y S-LIN son la misma corrida hasta el cambio)' if len(set(pe)) == 1 else '*** DIFIEREN'}")

    mal = CF.cruza_cod0(res, [dict(d, cod=CF.diagnostico(d['seed'], nk, ktop, BASE)['cod']) for d in diags])
    log(f"  CRUCE cod0 (instrumento) contra escala_codigo (bloque 0): "
        f"{'IDENTICO campo a campo' if not mal else '*** DIFIERE en ' + str(mal[:5])}")

    seg = sum(t_b.values()) / len(plan) * (T / Tb)
    n_corr = len(ORDEN) * N_SEM
    log(f"ESTIMACION del bloque: {n_corr} corridas de {T} pasos, ~{seg:.1f} s/corrida en serie -> "
        f"~{n_corr*seg/N_PARALELO/60:.1f} min de pared con Pool({N_PARALELO}).")
    log("HUMO: numeros observados, sin ajustar nada. n=2 y semillas vistas: NO son evidencia (E.14).")

    dj = os.path.join(RAIZ, 'datos', f'familias_b2_humo_{stamp}.json')
    with open(dj, 'w', encoding='utf-8') as f:
        json.dump(dict(meta=dict(fecha=time.strftime('%Y-%m-%dT%H:%M:%S'), tipo='humo', T_brazo=Tb, semillas=sem,
                                 T_bloque=T, nk=nk, ktop=ktop, nkmax=nkmax, brazos=N(BRAZOS), umbrales=UMBRALES,
                                 shas=SHAS(), segundos_por_brazo=t_b, cruce_cod0_ok=(not mal), plan=plan,
                                 python=platform.python_version(), numpy=np.__version__),
                       identidades=ident, diagnostico=diags, brazos=res),
                  f, ensure_ascii=False, default=str)
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
        for req in ('G-LIN', 'S-LIN'):
            if req not in BRAZOS_ACTIVOS:
                raise SystemExit(f"--brazos: {req} es referencia obligatoria (PG1/PG3/PG4 y PS1/PS4 la necesitan).")
    if '--humo' in sys.argv:
        humo(nk, ktop, nkmax, arg('--T', T)); sys.exit(0)

    import multiprocessing as mp
    mp.set_start_method('spawn', force=True)
    T = arg('--T', T)
    desde = arg('--desde', DESDE)
    SEEDS = list(range(desde, desde + N_SEM))
    stamp = time.strftime('%Y%m%d_%H%M%S')
    CF._log['f'] = open(os.path.join(RAIZ, 'datos', f'familias_b2_s{SEEDS[0]}-{SEEDS[-1]}_{stamp}.log'),
                        'w', encoding='utf-8', newline='\n')
    CF._log['t0'] = time.time()
    log(f"ARRANQUE BLOQUE 2 (capacidad directa): brazos {BRAZOS_ACTIVOS}, semillas {SEEDS[0]}-{SEEDS[-1]}, "
        f"T={T}. Pool({N_PARALELO}).")
    log("NO hay organo nuevo: v14.1 tal cual. Lo nuevo son perillas del MUNDO (vira, exc_evita) y de REGISTRO (reg_b2).")
    log(f"NK={nk} NKMAX={nkmax} K={ktop}, D=12 (el alias se DECLARA por semilla, no se elimina: ERR-45).")
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
        log(f"ETAPA 1/3 — IDENTIDAD, subconjunto critico ({len(CASOS_ID)} casos x {len(SEMILLAS_ID)} = {len(ctrl)}). "
            f"(v) y (x) DEBEN fallar: sin ellos la etapa pasa por vacuidad.")
        rc = pool.map(tarea, ctrl, chunksize=1)
        for cual in CASOS_ID:
            g = [r for r in rc if r['cual'] == cual]
            log(f"    {CASOS_ID[cual][0]:56s} {sum(r['ok'] for r in g)}/{len(g)}"
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
    log(f"CRUCE cod0 (instrumento) contra escala_codigo (bloque 0): "
        f"{'IDENTICO campo a campo' if not mal else '*** DIFIERE en ' + str(mal[:5])}")
    V['cruce_cod0_ok'] = (not mal)
    log("ANALISIS — medianas y cuartiles por brazo, y despues los umbrales EXACTOS del preregistro (ERR-31).")
    V.update(veredicto(res, SEEDS, diags))
    for b, d in V['linea_base'].items():
        log(f"    {b:6s} muertes {d['muertes']} q{d['q_muertes']}  regalo {d['regalo']}  celdas {d['celdas']}  "
            f"splits {d['splits']}  exp_total {d['exp_total']}  razon_exp {d['razon_exp']}")
    ver = frase_final(V)
    log(); log(f"VEREDICTO: {ver}")

    meta = dict(fecha=time.strftime('%Y-%m-%dT%H:%M:%S'), semillas=SEEDS, T=T, nk=nk, ktop=ktop, nkmax=nkmax,
                brazos={b: N(BRAZOS[b]) for b in BRAZOS_ACTIVOS}, veredicto=ver, veredictos=N(V),
                identidades=rc, diagnostico=diags, procesos_python=ps, shas=SHAS(),
                origen_organismo_v14_esperado=SHA_V14_ESPERADO,
                python=platform.python_version(), numpy=np.__version__)
    dj = os.path.join(RAIZ, 'datos', f'familias_b2_s{SEEDS[0]}-{SEEDS[-1]}_{stamp}.json')
    with open(dj, 'w', encoding='utf-8') as f:
        json.dump(dict(meta=meta, principal=res), f, ensure_ascii=False, default=str)
    log(f"datos -> {os.path.basename(dj)}  sha256_16 = {h16(dj)}")
    CF._log['f'].close()
