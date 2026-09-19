"""JUNTA FASE 5, CREADOR C -- HUMO de `variante_hija` (LA CASILLA QUE SE DIVIDE).

MISION (primero, siempre): llegar a la AGI por este camino -- un organismo minimo con reglas locales, sin
backpropagation, que aprende, desaprende, generaliza, sobrevive y se COMUNICA CON REFERENCIA. Hoy, exactamente:
que la MISMA tabla refiera a la FAMILIA (BAR-T <= 5/20) Y a la VARIANTE (PAR >= 15/20) a la vez, sin subir la
base sin mensaje.

EL CUELLO (registro, BLOQUE 6): con 4 casillas por par el mensaje refiere a la familia exacta (k = 3: BAR-T
5/20, pero PAR 12/20) o a la variante (sufijo uniforme de 3 px: PAR 15/20, pero BAR-T 11/20 y la base sube de
0 a 4-6). El sufijo del bloque 6 divide TODA la tabla por 8 de golpe: las celdas que SI distinguen se quedan sin
datos en la subcasilla que toca, ABSTIENEN, y una sola celda con fuga decide sin que las demas voten en contra.

EL MECANISMO DE C (angulo: sistemas vivos y mente -- crecimiento y jerarquia): la distincion de variante NO se
reparte por decreto, NACE donde la de familia FALLA. La casilla que tiene un valor de familia consolidado y
recibe una recompensa de SIGNO CONTRARIO se DIVIDE (la regla de v11 y de B-5, un nivel mas abajo), y sus hijas
NACEN CON EL VALOR DE LA MADRE: la tabla gana resolucion de variante sin perder densidad, asi que las celdas
que distinguen siguen pudiendo votar. El mensaje sobre `T1v2` cae en la hija de su firma; la hermana `T1v0`
sigue leyendo el valor de la familia.

CELDAS DEL HUMO (las tres en las MISMAS semillas, pareadas):
  k3v0 = organismo_familias_b5 con k = 3, BIT A BIT (familia exacta, variante no)   -- linea base 1
  k3v1 = organismo_familias_b6 con el sufijo uniforme, BIT A BIT (variante si, familia no) -- linea base 2
  k3h1 = EL CANDIDATO: k = 3 + `variante_hija` (la casilla que se divide)

REGLA 3 y 11: el HUMO es UN proceso, sin Pool, con semillas 901-903 (nave de la junta: nunca 821-860 ni
721-760); el `Pool` de la CONFIRMACION lo lanza SOLO el coordinador (`--serie`). ERR-31: el mundo, el canal, el
EMISOR (b4b bit a bit) y la lectura de la boca son los OBJETOS de los bloques 4b/5/6, importados, no recopiados.
ERR-44: todo se mide sobre la CONDUCTA de la boca. ERR-54: el crudo se guarda ANTES del analisis. ERR-52: OTRO
queda fuera de P-I3. ERR-64b: los controles de identidad que DEBEN diferir piden >= 2 de 3. ERR-70: P-I4 por
exclusion de semilla. ERR-71: el caso (d) de la identidad NO pasa por el emisor.

P-I5 (decision del coordinador, 19-sep-2026, DESPUES del humo y ANTES de la confirmacion): NO se toca el
criterio. Se lee como puerta de VALIDEZ: la semilla en la que la boca leyo la via RAPIDA no mide nada, sale del
numerador Y del denominador de TODOS los brazos de esa celda y se DECLARA (cuantas y cuales), con el mismo
trato para la linea base. Ver UMBRALES (V1/V2: la prediccion cuantitativa del hallazgo, escrita antes).

    python experimentos/junta_fase5/C/corre_c1.py [--T 100000] [--desde 901] [--n 3]   (humo; modo por defecto)
    python experimentos/junta_fase5/C/corre_c1.py --serie --desde 821 --T 100000              (el COORDINADOR)
    python experimentos/junta_fase5/C/corre_c1.py --serie --desde 841 --T 100000              (replica)
    python experimentos/junta_fase5/C/corre_c1.py --serie --desde 821 --plan                  (en seco, no simula)
"""
import sys, os, json, time, hashlib, platform, subprocess

sys.stdout.reconfigure(encoding='utf-8', errors='replace')
AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(AQUI)))
N12 = os.path.join(RAIZ, 'experimentos', 'nivel12_mundo_familias')
CREA = os.path.join(RAIZ, 'experimentos', 'creacion_A')
CREB = os.path.join(RAIZ, 'experimentos', 'creacion_B')
sys.path[:0] = [AQUI, N12, CREA, CREB, os.path.join(RAIZ, 'organismo')]

import numpy as np
import corre_familias_b6 as B6R              # bloque 6: brazos, canal, estructura, emisor, letra
B5R, B4BR, B2R, CF = B6R.B5R, B6R.B4BR, B6R.B2R, B6R.CF
import organismo_familias_c1 as C1
import organismo_familias_b6 as B6

T = 100000
N_SEM = 3
DESDE = 901                                  # nave de la junta: humo SOLO con 901-910
SEM_R, SEM_OTRO, VORAZ = B6R.SEM_R, B6R.SEM_OTRO, B6R.VORAZ
MUNDO, KW_E, KW_R = B6R.MUNDO, B6R.KW_E, B6R.KW_R
XNEG, BAR, PATS, prefijo = B6R.XNEG, B6R.BAR, B6R.PATS, B6R.prefijo
PAR_HERM, PARES12, NVAR = B6R.PAR_HERM, B6R.PARES12, B6R.NVAR
log, h16, N, med = CF.log, CF.h16, CF.N, CF.med
BASE = B2R.BASE

T_ID = 20000
T_CANAL_ID = 60000                           # ERR-64: a T = 30000 el mensaje no se entrega en 1/3 semillas
import os as _os
N_PARALELO = int(_os.environ.get('JUACO_POOL', 14))   # el Pool lo lanza SOLO el coordinador (regla 3);
                                             # bajado por el coordinador con JUACO_POOL cuando hay otras corridas (BrokenPipe 17:16)
SEMILLAS_ID = [1, 2, 3]

# celda -> (k_ganadoras, memoria_variante, variante_hija)
CELDAS = {'k3v0': (3, 0, 0), 'k3v1': (3, 1, 0), 'k3h1': (3, 0, 1)}
PLANTILLA = B5R.PLANTILLA                    # los NUEVE brazos del 4b (-), importados (ERR-31)
BRAZOS, ORDEN = {}, []
for _c in CELDAS:
    for _n, _m, _p, _o, _ph in PLANTILLA:
        _b = '%s-%s' % (_n, _c)
        BRAZOS[_b] = dict(dir='neg', modo=_m, pat=_p, otro=_o, par=_ph, cel=_c, base=_n,
                          k=CELDAS[_c][0], mv=CELDAS[_c][1], vh=CELDAS[_c][2])
        ORDEN.append(_b)
BRAZOS_HUMO = [b for b in ORDEN if BRAZOS[b]['base'] in ('CANAL', 'CORTADO', 'BAR-H', 'BAR-T', 'VALOR',
                                                         'PAR', 'PAR0')]   # el humo no corre INM ni OTRO
gemelo_de = lambda b: ('PAR0-%s' % BRAZOS[b]['cel']) if BRAZOS[b]['base'].startswith('PAR') \
    else ('CORTADO-%s' % BRAZOS[b]['cel'])

NUEVAS_C1 = ('variante_hija', 'vh_ev', 'vh_umbral', 'vh_hijas', 'vh_hijas_gan', 'vh_conocidos')
NUEVAS_B6 = ('memoria_variante', 'memoria_slots', 'memoria_nvar', 'canal_mismo_dir_k')
NUEVAS_B5 = ('k_ganadoras', 'mem_ganadoras', 'canal_gan_k_pre', 'canal_gan_k_post', 'canal_mismo_bin_k')
NUEVAS_B4B = ('voraz', 'par_herm', 'par_fijo')
CASOS_ID = {   # subconjunto critico del arnes `identidad_c1.py` (61/61), corrido ANTES de medir (P-I1)
    'a': ("(a) vh=0, k=3 == organismo_familias_b6 (el mundo del bloque 4, RECEPTOR)", 'B6F', T_ID),
    'b': ("(b) vh=0, k=3, sufijo b6=1 == organismo_familias_b6 (el brazo k3v1 es b6 BIT A BIT)", 'B6MV', T_ID),
    'n': ("(n) vh=0, k=1, mundo=AB == organismo_v14 (TRONCO)", 'V14', T_ID),
    'x': ("(x) memoria_pares=None: vh=1 == vh=0 (la perilla es INERTE sin tabla)", 'INERTE', T_ID),
    'e': ("(e) perilla mal escrita LANZA (2, -1, 0.5, '1', True, y vh=1 con mv=1)", 'LANZA', 200),
    'd': ("(d) la DIVISION: la HERMANA sale de la direccion del referente y el referente sigue dentro", 'DIR',
          T_CANAL_ID),
    'K': ("(K) vh=1 != vh=0 con el relevo ON (DEBE diferir)", 'VDIF', T_ID),
    'C': ("(C) CANAL-k3h1 != CORTADO-k3h1 (DEBE diferir)", 'CAN', T_CANAL_ID),
    'H': ("(H) BAR-H-k3h1 != CANAL-k3h1 (DEBE diferir: es el brazo que decide)", 'HER', T_CANAL_ID),
}

SHAS = lambda: dict(instrumento_c1=h16(os.path.join(AQUI, 'organismo_familias_c1.py')),
                    arnes_c1=h16(os.path.join(AQUI, 'identidad_c1.py')),
                    script=h16(os.path.abspath(__file__)),
                    origen_b6=h16(os.path.join(N12, 'organismo_familias_b6.py')),
                    origen_b5=h16(os.path.join(N12, 'organismo_familias_b5.py')),
                    runner_b6=h16(os.path.join(N12, 'corre_familias_b6.py')),
                    origen_organismo_v14=h16(os.path.join(RAIZ, 'organismo', 'organismo_v14.py')))
SHA_ESPERADOS = dict(origen_b6='b10cbd4ddd0c32a3', origen_b5='e0b6b90f6f92d5c1',
                     origen_organismo_v14='feefc88b1fd8d434')


def canal_de(brazo, msg, fam_seed_R, D=12):
    b = BRAZOS[brazo]
    if b['pat'] == 'CEROS':
        P = [0.0] * D
    elif b['pat'] == 'REF':
        P = msg['P']
    else:
        P = PATS(msg['fam_seed'])[BAR[b['dir']][b['pat']]]
    return dict(modo=b['modo'], t=msg['t'], ref=msg['ref'], P=P, R=msg['R'])


def n_conoce(r, nombre):
    """DIAGNOSTICO (observado, no prometido): cuantas de las k ganadoras CONOCEN el estimulo `nombre`, o sea
    cuantas pueden VOTAR cuando la boca lee. Es el numero que el sufijo uniforme del bloque 6 hunde y que la
    division por conflicto conserva. Se lee de `mem_tabla` (en este mundo R in {+1, -3}: una casilla escrita
    nunca vale exactamente 0.0, asi que 0.0 == no vista). Para `variante_hija` se mira el nivel GRUESO, que es
    el que decide si la casilla conoce: una casilla solo se divide si ya estaba vista, y sus hijas nacen con el
    valor de la madre -- luego conocer el nivel grueso equivale a conocer el vigente."""
    P = PATS(r['fam_seed'])[nombre]
    gan = r.get('mem_ganadoras') or []
    mv, vh = int(r.get('memoria_variante') or 0), int(r.get('variante_hija') or 0)
    n = 0
    for par in gan:
        b = int(P[par[0]]) * 2 + int(P[par[1]])
        if mv and not vh:
            s = 0
            for q in range(12 - NVAR, 12):
                s = s * 2 + int(P[q])
            b = b * (1 << NVAR) + s
        g = PARES12.index(tuple(par))
        n += int(float(r['mem_tabla'][g][b]) != 0.0)
    return n


def corre(brazo, seed, msg, Ti, nk, ktop, nkmax):
    b = BRAZOS[brazo]
    kw = B2R.resuelve(KW_R, Ti)
    kw.update(nk=nk, ktop=ktop, nkmax=nkmax)
    fsr = seed + SEM_OTRO if b['otro'] else seed
    r = C1.run(seed + SEM_R, T=Ti, fam_seed=fsr, canal=canal_de(brazo, msg, fsr), par_herm=b['par'],
               k_ganadoras=b['k'], memoria_variante=b['mv'], variante_hija=b['vh'], **kw)
    d = dict(tipo='R', brazo=brazo, base=b['base'], cel=b['cel'], k=b['k'], mv=b['mv'], vh=b['vh'], seed=seed,
             deaths=r['deaths'], celdas=r['celdas'], splits=r['splits'], fam_seed=r['fam_seed'],
             entregado=r['canal_entregado'], t_entrega=r['canal_t_entrega'], t_msg=r['canal_t_msg'],
             vh_hijas=r['vh_hijas'], vh_hijas_gan=r['vh_hijas_gan'], vh_conocidos=r['vh_conocidos'],
             wv=r.get('w_var_med'), cobertura=r['mem_cobertura'], vistas=r['mem_vistas'],
             conoce_ref=n_conoce(r, XNEG), conoce_herm=n_conoce(r, BAR['neg']['H']),
             conoce_tok=n_conoce(r, BAR['neg']['TK']))
    d['B4'] = B4BR.lee_b4(r, msg['ref'])
    d['mem'] = B6R.mecanismo(r)
    d['prefijo'] = prefijo(r, r['canal_t_entrega'] if r['canal_t_entrega'] is not None else r['canal_t_msg'])
    d['prefijo_msg'] = prefijo(r, r['canal_t_msg'])        # P-I3 del brazo INM: hasta t_msg
    return d


def _cmp(a, b, salta):
    return [k for k in a if k not in salta and N(a[k]) != N(b.get(k))] + \
           [k for k in a if k not in b and k not in salta]


def tarea(args):
    """Una tarea del Pool. Tipos: ID (guarda de identidad), E (emisor), R (receptor de un brazo)."""
    tipo = args[0]
    if tipo == 'E':
        _, seed, Ti, nk, ktop, nkmax = args
        return dict(tipo='E', seed=seed, msgs=B6R.emisor(seed, Ti, nk, ktop, nkmax))
    if tipo == 'R':
        _, brazo, seed, msg, Ti, nk, ktop, nkmax = args
        return corre(brazo, seed, msg, Ti, nk, ktop, nkmax)
    _, cual, seed = args
    import organismo_v14 as V14
    import organismo_familias_b6 as B6
    etiq, ref, Tc = CASOS_ID[cual]
    salta, debe = NUEVAS_C1, False
    kwf = dict(B2R.resuelve(KW_R, Tc), fam_seed=seed)
    if ref == 'B6F':
        a, b = B6.run(seed, T=Tc, k_ganadoras=3, **kwf), C1.run(seed, T=Tc, k_ganadoras=3, variante_hija=0, **kwf)
    elif ref == 'B6MV':
        a = B6.run(seed, T=Tc, k_ganadoras=3, memoria_variante=1, **kwf)
        b = C1.run(seed, T=Tc, k_ganadoras=3, memoria_variante=1, variante_hija=0, **kwf)
    elif ref == 'V14':
        a, b = V14.run(seed, T=Tc), C1.run(seed, T=Tc)
        salta = NUEVAS_C1 + NUEVAS_B6 + NUEVAS_B5 + NUEVAS_B4B
    elif ref == 'INERTE':
        k = dict(kwf, memoria_pares=None)
        a = C1.run(seed, T=Tc, k_ganadoras=3, variante_hija=0, **k)
        b = C1.run(seed, T=Tc, k_ganadoras=3, variante_hija=1, **k)
    elif ref == 'VDIF':
        a = C1.run(seed, T=Tc, k_ganadoras=3, variante_hija=0, **kwf)
        b = C1.run(seed, T=Tc, k_ganadoras=3, variante_hija=1, **kwf)
        debe = True
    elif ref == 'LANZA':
        ok = True
        for mala in (2, -1, 0.5, '1', True):
            try:
                C1.run(seed, T=Tc, variante_hija=mala); ok = False
            except (ValueError, TypeError):
                pass
            except Exception:
                ok = False
        try:
            C1.run(seed, T=Tc, variante_hija=1, memoria_variante=1, **kwf); ok = False
        except (ValueError, TypeError):
            pass
        except Exception:
            ok = False
        return dict(tipo='ID', cual=cual, etiqueta=etiq, seed=seed, identico=ok, debe_diferir=False,
                    ok=bool(ok), difieren=[] if ok else ['no lanza'], faltan=[])
    elif ref == 'DIR':
        # ERR-71: NO pasa por el EMISOR. El mensaje se construye del catalogo del bloque 0.
        Q, H = PATS(seed), BAR['neg']['H']
        m = dict(t=10000, ref=XNEG, P=[float(x) for x in Q[XNEG]], R=1.0, fam_seed=seed)
        ok = True
        for vh in (0, 1):
            r = C1.run(seed + SEM_R, T=Tc, fam_seed=seed, canal=canal_de('CANAL-k3h1', m, seed),
                       k_ganadoras=3, memoria_variante=0, variante_hija=vh, **B2R.resuelve(KW_R, Tc))
            if not r['canal_entregado'] or r['canal_mismo_dir_k'] is None:
                return dict(tipo='ID', cual=cual, etiqueta=etiq, seed=seed, identico=False, debe_diferir=False,
                            ok=False, difieren=['sin entrega vh=%d' % vh], faltan=[])
            ok &= bool(XNEG in r['canal_mismo_dir_k'])                    # el referente, en su propia direccion
            if vh:
                ok &= bool(r['vh_hijas'] > 0)                             # la casilla se dividio (no vacuidad)
                ok &= bool(H not in r['canal_mismo_dir_k'])               # y la HERMANA sale de esa direccion
                ok &= all(v is not None for v in r['W_tabla'].values())   # DENSIDAD: nadie abstiene por dividirse
        return dict(tipo='ID', cual=cual, etiqueta=etiq, seed=seed, identico=ok, debe_diferir=False,
                    ok=bool(ok), difieren=[] if ok else ['division/direccion'], faltan=[])
    else:                                    # CAN / HER: no-vacuidad del canal, con el emisor real
        m = B6R.emisor(seed, Tc)['neg']
        if m is None:
            return dict(tipo='ID', cual=cual, etiqueta=etiq, seed=seed, identico=False, debe_diferir=True,
                        ok=False, difieren=['sin mensaje (-)'], faltan=[])
        otro = 'CORTADO-k3h1' if ref == 'CAN' else 'BAR-H-k3h1'
        kw = B2R.resuelve(KW_R, Tc)
        a = C1.run(seed + SEM_R, T=Tc, fam_seed=seed, canal=canal_de(otro, m, seed),
                   k_ganadoras=3, variante_hija=1, **kw)
        b = C1.run(seed + SEM_R, T=Tc, fam_seed=seed, canal=canal_de('CANAL-k3h1', m, seed),
                   k_ganadoras=3, variante_hija=1, **kw)
        debe = True; salta = ('canal', 'canal_modo')
    dif = _cmp(a, b, salta)
    return dict(tipo='ID', cual=cual, etiqueta=etiq, seed=seed, identico=not dif, debe_diferir=debe,
                ok=bool((not dif) != debe), difieren=dif[:6], faltan=[])


# ---------------------------------------------------------------- LA LETRA (escrita antes de la confirmacion)
# DECISION DEL COORDINADOR (19-sep-2026, tras el humo; §1 de su mensaje): P-I5 NO se toca. Se lee como puerta de
# VALIDEZ y no de calidad: la semilla en la que la boca leyo la via RAPIDA no mide nada (el mensaje queda escrito
# y no consultado), sale del numerador Y del denominador de TODOS los brazos de esa celda, y se DECLARA (cuantas
# y cuales). Mismo trato para la linea base que para el candidato. Los umbrales del bloque 6 se leen como
# FRACCION de las semillas validas: >= 15/20 -> ceil(0.75 n), <= 5/20 -> floor(0.25 n), margenes +3 y +5 -> los
# mismos enteros. Se reportan las dos lecturas, declaradas ANTES de correr:
#   PRINCIPAL  : exclusion POR CELDA (cada celda con sus propias semillas validas; la P-I5 es una propiedad del
#                montaje de esa celda, porque la ruta depende de la vida entera del receptor).
#   SECUNDARIA : la INTERSECCION (las semillas validas en las tres celdas), que es la comparacion pareada.
import math
UMBRALES = {
    'R1': "CANAL >= ceil(0.75 n) y CORTADO <= floor(0.25 n) y pareado >= ceil(0.70 n)",
    'R2': "BAR-T <= CORTADO + 3", 'R3': "BAR-H <= CORTADO + 5", 'R4': "VALOR <= CORTADO + 3",
    'R5': "dist(PAR) >= ceil(0.60 n) y dist(PAR) >= dist(PAR0) + 5",
    'R6': "muertes(CANAL-celda) <= 1.5 x muertes(CANAL-k3v0) y okU >= okU(CANAL-k3v0) - 0.10",
    'O_C': "EL OBJETIVO DE LA JUNTA, en k3h1 y en LAS DOS series: BAR-T <= floor(0.25 n) Y dist(PAR) >= "
           "ceil(0.75 n) A LA VEZ, con CANAL >= ceil(0.75 n), CORTADO <= floor(0.25 n), BAR-H <= floor(0.25 n) "
           "y VALOR <= floor(0.25 n)",
    'V1': "PREDICCION DEL HALLAZGO (§3 del coordinador): vacuas(k3h1) - vacuas(k3v0) >= +3 semillas en LAS DOS "
          "series; predigo vacuas k3h1 6/20 (3-11), k3v0 1/20 (0-2), k3v1 2/20 (0-4). Me refuta <= +1.",
    'V2': "MECANISMO DE LA VACUIDAD: en k3h1, la mediana de `celdas` (Kenyon) de las semillas VACUAS es MENOR "
          "que la de las validas, en las dos series (menos divisiones -> codigo estable -> puerta cerrada)",
}
ceil75 = lambda n: int(math.ceil(0.75 * n))
piso25 = lambda n: int(math.floor(0.25 * n))


def veredicto(res, msgs, SEEDS):
    G = {b: {r['seed']: r for r in res if r['brazo'] == b} for b in ORDEN}
    hay = lambda b: len(G.get(b, {})) > 0
    con_msg = [s for s in SEEDS if (msgs.get(s) or {}).get('neg')]
    mal_pi4 = set()                                   # ERR-70: exclusion POR SEMILLA (herencia del bloque 6)
    for c in CELDAS:
        for s in con_msg:
            r = G.get('CORTADO-' + c, {}).get(s)
            if r is None:
                continue
            tx = (r.get('B4') or {}).get('t_X')
            if tx is None or tx != r.get('t_entrega'):
                mal_pi4.add(s)
    base = [s for s in con_msg if s not in mal_pi4]
    # --- P-I5 POR SEMILLA Y POR CELDA (decision del coordinador): fam1 = 1 -> via RAPIDA -> semilla VACUA
    pi5 = {c: {s: int((G.get('CORTADO-' + c, {}).get(s, {}).get('B4') or {}).get('fam1') or 0) for s in base
               if s in G.get('CORTADO-' + c, {})} for c in CELDAS}
    vacuas = {c: sorted(s for s, v in pi5[c].items() if v == 1) for c in CELDAS}
    validas = {c: [s for s in base if s in pi5[c] and pi5[c][s] == 0] for c in CELDAS}
    comun = [s for s in base if all(pi5[c].get(s) == 0 for c in CELDAS if pi5[c])]
    V = dict(umbrales=UMBRALES, n_semillas=len(SEEDS), n_con_mensaje=len(con_msg), n_base=len(base),
             sin_mensaje=[s for s in SEEDS if s not in con_msg], excluidas_pi4_ERR70=sorted(mal_pi4),
             PI5_por_semilla=pi5, vacuas_PI5=vacuas, n_vacuas={c: len(v) for c, v in vacuas.items()},
             validas_por_celda={c: len(v) for c, v in validas.items()}, n_comun=len(comun),
             celdas={}, celdas_comun={})
    V['PI3'] = {b: sum(1 for s in base if G.get(b, {}).get(s) and G.get(gemelo_de(b), {}).get(s)
                       and G[b][s]['prefijo_msg' if BRAZOS[b]['base'] == 'INM' else 'prefijo']
                       == G[gemelo_de(b)][s]['prefijo_msg' if BRAZOS[b]['base'] == 'INM' else 'prefijo'])
                for b in ORDEN if BRAZOS[b]['modo'] in ('sen', 'inm') and BRAZOS[b]['base'] != 'OTRO'
                and hay(b) and hay(gemelo_de(b))}                      # ERR-52: OTRO fuera (vive en otro mundo)
    V['PI2'] = dict(n_emite=len(con_msg), n=len(SEEDS),
                    signo_ok=sum(1 for s in con_msg if msgs[s]['neg']['R'] > 0),
                    t_msg_med=med([msgs[s]['neg']['t'] for s in con_msg]))

    def bloque(c, sem):
        """Los brazos de la celda `c` contados sobre las semillas `sem`. Sin indexar a ciegas (ERR-54)."""
        n = len(sem)
        bb = lambda b, k2: [(G[b][s].get('B4') or {}).get(k2) for s in sem if s in G.get(b, {})]
        gg = lambda b, k2: [G[b][s].get(k2) for s in sem if s in G.get(b, {})]
        com = lambda b: sum(1 for v in bb(b, 'evX') if v == 0.0)
        dst = lambda b: sum(1 for v in bb(b, 'dist') if v == 1.0)
        CA, CO, PA, P0 = 'CANAL-' + c, 'CORTADO-' + c, 'PAR-' + c, 'PAR0-' + c
        q = {x: com('%s-%s' % (x, c)) for x in ('CANAL', 'CORTADO', 'BAR-H', 'BAR-T', 'VALOR', 'INM', 'OTRO')
             if hay('%s-%s' % (x, c))}
        dk, dc = bb(CA, 'evX'), bb(CO, 'evX')
        par = sum(1 for i in range(min(len(dk), len(dc)))
                  if dk[i] is not None and dc[i] is not None and dk[i] < dc[i])
        d = dict(n=n, **q, PAR_dist=dst(PA), PAR0_dist=dst(P0), pareado=par,
                 muertes=med(gg(CA, 'deaths')), okU=med([v for v in bb(CA, 'okU') if v is not None]),
                 celdas_kenyon=med(gg(CA, 'celdas')), hijas=med(gg(CA, 'vh_hijas')),
                 cobertura=med(gg(CA, 'cobertura')), conocidos=med(gg(CA, 'vh_conocidos')),
                 conoce_ref=med(gg(CA, 'conoce_ref')), conoce_ref_barT=med(gg('BAR-T-' + c, 'conoce_ref')),
                 n_mismo_dir_k=med([r['mem'].get('n_mismo_dir_k') for r in G[CA].values()
                                    if r['seed'] in sem and r['mem'].get('n_mismo_dir_k') is not None]),
                 wv=med([v for v in gg('BAR-H-' + c, 'wv') if v is not None]),
                 lag_par=med([v for v in bb(PA, 'lag_par') if v is not None]))
        if n:
            d.update(R1=bool(q['CANAL'] >= ceil75(n) and q['CORTADO'] <= piso25(n)
                             and par >= int(math.ceil(0.70 * n))),
                     R2=bool(q['BAR-T'] <= q['CORTADO'] + 3), R3=bool(q['BAR-H'] <= q['CORTADO'] + 5),
                     R4=bool(q['VALOR'] <= q['CORTADO'] + 3),
                     R5=bool(d['PAR_dist'] >= int(math.ceil(0.60 * n)) and d['PAR_dist'] >= d['PAR0_dist'] + 5),
                     O_C=bool(q['BAR-T'] <= piso25(n) and d['PAR_dist'] >= ceil75(n)
                              and q['CANAL'] >= ceil75(n) and q['CORTADO'] <= piso25(n)
                              and q['BAR-H'] <= piso25(n) and q['VALOR'] <= piso25(n)))
        return d

    for c in CELDAS:
        if hay('CANAL-' + c):
            V['celdas'][c] = bloque(c, validas[c])                     # PRINCIPAL: exclusion por celda
            V['celdas_comun'][c] = bloque(c, comun)                    # SECUNDARIA: pareada en la interseccion
    ref = V['celdas'].get('k3v0')
    for c, d in V['celdas'].items():                                   # R6 contra el control de Occam k3v0
        d['R6'] = bool(ref and d['muertes'] is not None and ref['muertes'] is not None
                       and d['muertes'] <= 1.5 * max(ref['muertes'], 1)
                       and d['okU'] is not None and ref['okU'] is not None and d['okU'] >= ref['okU'] - 0.10)
    # --- V1/V2: la prediccion del HALLAZGO (la vacuidad), medible en esta misma corrida
    kv = lambda c, sem: med([G['CANAL-' + c][s]['celdas'] for s in sem if s in G.get('CANAL-' + c, {})])
    V['VACUIDAD'] = dict(frase=UMBRALES['V1'], n_vacuas=V['n_vacuas'], n_base=len(base),
                         contraste_h1_menos_v0=(len(vacuas['k3h1']) - len(vacuas['k3v0'])),
                         V1_pasa=bool(len(vacuas['k3h1']) - len(vacuas['k3v0']) >= 3),
                         celdas_kenyon_vacuas={c: kv(c, vacuas[c]) for c in CELDAS},
                         celdas_kenyon_validas={c: kv(c, validas[c]) for c in CELDAS})
    vk, vl = V['VACUIDAD']['celdas_kenyon_vacuas'].get('k3h1'), V['VACUIDAD']['celdas_kenyon_validas'].get('k3h1')
    V['VACUIDAD']['V2_pasa'] = bool(vk is not None and vl is not None and vk < vl)
    return V


def frase(V):
    s = (f"DIRECCION (-) SOLA (ERR-53). `com` = mordio en su PRIMERA exposicion de la vida al referente.\n"
         f"  semillas {V['n_semillas']}; con mensaje {V['n_con_mensaje']} (sin mensaje {V['sin_mensaje']}); "
         f"excluidas por ERR-70 {V['excluidas_pi4_ERR70']}; base {V['n_base']}.\n"
         f"  P-I5 (decision del coordinador: puerta de VALIDEZ). Semillas VACUAS (la boca leyo la via RAPIDA, "
         f"el mensaje quedo escrito y no consultado), por celda: "
         + "; ".join(f"{c}: {len(V['vacuas_PI5'][c])} {V['vacuas_PI5'][c]}" for c in V['vacuas_PI5'])
         + f". Interseccion valida en las tres celdas: {V['n_comun']}.\n")
    for nom, blo in (('PRINCIPAL (exclusion por celda)', V['celdas']),
                     ('SECUNDARIA (pareada, interseccion)', V['celdas_comun'])):
        s += (f"  --- {nom}\n  {'celda':6s} {'n':>3s} {'CANAL':>6s} {'CORT':>5s} {'BAR-H':>6s} {'BAR-T':>6s} "
              f"{'VALOR':>6s} {'PARd':>5s} {'PAR0d':>6s} {'muert':>7s} {'R1':>3s} {'R2':>3s} {'R3':>3s} "
              f"{'R4':>3s} {'R5':>3s} {'O-C':>4s}\n")
        for c, d in blo.items():
            f_ = lambda k2: ('si' if d.get(k2) else 'NO')
            s += (f"  {c:6s} {d['n']:3d} {d.get('CANAL',0):6d} {d.get('CORTADO',0):5d} {d.get('BAR-H',0):6d} "
                  f"{d.get('BAR-T',0):6d} {d.get('VALOR',0):6d} {d['PAR_dist']:5d} {d['PAR0_dist']:6d} "
                  f"{str(d['muertes']):>7s} {f_('R1'):>3s} {f_('R2'):>3s} {f_('R3'):>3s} {f_('R4'):>3s} "
                  f"{f_('R5'):>3s} {f_('O_C'):>4s}\n")
    W = V['VACUIDAD']
    s += (f"  --- HALLAZGO (predicho antes de correr): vacuas k3h1 {W['n_vacuas'].get('k3h1')} contra k3v0 "
          f"{W['n_vacuas'].get('k3v0')} y k3v1 {W['n_vacuas'].get('k3v1')} -> contraste "
          f"{W['contraste_h1_menos_v0']:+d} (V1 {'PASA' if W['V1_pasa'] else 'CAE'}); celdas de Kenyon en k3h1, "
          f"vacuas {W['celdas_kenyon_vacuas'].get('k3h1')} contra validas "
          f"{W['celdas_kenyon_validas'].get('k3h1')} (V2 {'PASA' if W['V2_pasa'] else 'CAE'}).\n"
          f"  20 semillas no cierran nada: replica en el rango siguiente (regla 12).")
    return s


if __name__ == '__main__':
    arg = lambda n, d: (type(d)(sys.argv[sys.argv.index(n) + 1]) if n in sys.argv else d)
    T = arg('--T', T)
    desde = arg('--desde', DESDE)
    n_sem = arg('--n', N_SEM)
    nk, ktop, nkmax = arg('--nk', 30), arg('--k', 3), arg('--nkmax', 90)
    # `--arnes`: DIAGNOSTICO en las semillas del ARNES (1, 2) -- las MISMAS que uso el humo del bloque 6 (su
    # preregistro 9.1) y las del arnes de identidad. NO son semillas de serie ni de confirmacion. Se declara en
    # el informe como desviacion de la nave (que fija el humo en 901-910) en vez de esconderse: el humo de
    # 901-903 dejo 1 sola semilla utilizable por la puerta P-I5 y con n = 1 no se ve nada.
    ARNES = '--arnes' in sys.argv
    SERIE = '--serie' in sys.argv          # CONFIRMACION: la corre el COORDINADOR (regla 3: el Pool es suyo)
    if SERIE:
        desde = arg('--desde', 821)
        n_sem = arg('--n', 20)
        if desde not in (821, 841) or n_sem != 20:
            raise SystemExit("CONFIRMACION: --desde 821 o 841, con --n 20 (los dos rangos del preregistro).")
        SEEDS = list(range(desde, desde + n_sem))
    elif ARNES:
        SEEDS = [1, 2]
    else:
        if not (901 <= desde and desde + n_sem - 1 <= 910):
            raise SystemExit("NAVE DE LA JUNTA: el humo solo usa semillas 901-910.")
        if n_sem > 3:
            raise SystemExit("NAVE DE LA JUNTA: humo con <= 3 semillas.")
        SEEDS = list(range(desde, desde + n_sem))
    if '--plan' in sys.argv:               # comprobacion en seco: NO simula nada, imprime el plan y sale
        print(f"PLAN {'SERIE' if SERIE else ('ARNES' if ARNES else 'HUMO')}: semillas {SEEDS[0]}-{SEEDS[-1]} "
              f"({len(SEEDS)}), T = {T}")
        print(f"  identidad: {len(CASOS_ID)} casos x {len(SEMILLAS_ID)} semillas = "
              f"{len(CASOS_ID)*len(SEMILLAS_ID)} tareas  ({', '.join(CASOS_ID)})")
        br = ORDEN if SERIE else BRAZOS_HUMO
        print(f"  brazos: {len(br)} = {len(CELDAS)} celdas x {len(br)//len(CELDAS)}  -> "
              f"{len(br)*len(SEEDS)} corridas + {len(SEEDS)} emisores")
        print(f"  Pool({N_PARALELO})" if SERIE else "  un proceso, sin Pool")
        for k, v in SHAS().items():
            print(f"    sha {k:24s} {v}"
                  + ('' if k not in SHA_ESPERADOS else ('  OK' if v == SHA_ESPERADOS[k] else '  *** CAMBIO')))
        sys.exit(0 if all(SHAS()[k] == v for k, v in SHA_ESPERADOS.items()) else 1)
    if SERIE:
        import multiprocessing as mp
        mp.set_start_method('spawn', force=True)
        stamp = time.strftime('%Y%m%d_%H%M%S')
        CF._log['f'] = open(os.path.join(AQUI, f'c1_serie_s{SEEDS[0]}-{SEEDS[-1]}_{stamp}.log'), 'w',
                            encoding='utf-8', newline='\n')
        CF._log['t0'] = time.time()
        log(f"CONFIRMACION -- CREADOR C, junta de la fase 5: `variante_hija` (LA CASILLA QUE SE DIVIDE).")
        log(f"Semillas {SEEDS[0]}-{SEEDS[-1]}, T = {T}, {len(ORDEN)} brazos = {len(CELDAS)} celdas x "
            f"{len(PLANTILLA)}. Pool({N_PARALELO}). Direccion (-) sola (ERR-53).")
        log("La letra y las exclusiones estan en UMBRALES (escritas ANTES de correr; P-I5 segun la decision "
            "del coordinador del 19-sep: puerta de VALIDEZ, exclusion por semilla declarada, mismo trato para "
            "la linea base).")
        for k, v in SHAS().items():
            marca = '' if k not in SHA_ESPERADOS else ('  OK' if v == SHA_ESPERADOS[k] else '  *** CAMBIO')
            log(f"    sha {k:24s} {v}{marca}")
        if any(SHAS()[k] != v for k, v in SHA_ESPERADOS.items()):
            raise SystemExit("Un origen cambio: no se mide nada.")
        try:
            ps = subprocess.run(['powershell', '-NoProfile', '-Command',
                                 "Get-CimInstance Win32_Process | Where-Object { $_.Name -like 'python*' } | "
                                 "ForEach-Object { \"$($_.ProcessId) $($_.CommandLine)\" }"],
                                capture_output=True, text=True, timeout=60).stdout.strip().splitlines()
        except Exception as e:
            ps = [f"(no se pudo listar: {e})"]
        log(f"REGLA 11 - procesos python vivos ({len(ps)}), este es pid {os.getpid()}")
        V = {}
        with mp.Pool(N_PARALELO) as pool:
            ctrl = [('ID', c, s) for c in CASOS_ID for s in SEMILLAS_ID]
            log(f"ETAPA 1/3 - IDENTIDAD, P-I1 ({len(CASOS_ID)} casos x {len(SEMILLAS_ID)} = {len(ctrl)}). "
                "(K), (C) y (H) DEBEN diferir: sin ellos la etapa pasa por vacuidad. El arnes completo "
                "(61/61) es identidad_c1.py.")
            rc = pool.map(tarea, ctrl, chunksize=1)
            for cual in CASOS_ID:
                g = [r for r in rc if r['cual'] == cual]
                ml = next((r for r in g if not r['ok']), None)          # ERR-71: la semilla que FALLA
                log(f"    {CASOS_ID[cual][0]:78s} {sum(r['ok'] for r in g)}/{len(g)}"
                    + ("" if ml is None else f"   semilla {ml['seed']}: difieren {ml['difieren']}"))
                # ERR-64b: los controles que DEBEN diferir prueban no-vacuidad con >= 2 de 3
                V[f'ID_{cual}'] = (sum(r['ok'] for r in g) >= 2) if (g and g[0].get('debe_diferir')) \
                    else all(r['ok'] for r in g)
            V['G_IDENTIDAD'] = bool(all(V[f'ID_{c}'] for c in CASOS_ID))
            log(f"  IDENTIDAD {sum(r['ok'] for r in rc)}/{len(rc)}")
            if not V['G_IDENTIDAD']:
                log("*** GUARDA DE IDENTIDAD FALLIDA. Se para (P-I1).")
                sys.exit(1)
            log(f"ETAPA 2/3 - EMISORES ({len(SEEDS)} corridas de {T}; mv = 0, k = 1 = b4b bit a bit, sin tocar).")
            em = pool.map(tarea, [('E', s, T, nk, ktop, nkmax) for s in SEEDS], chunksize=1)
            msgs = {d['seed']: d['msgs'] for d in em}
            sin = [s for s in SEEDS if not (msgs.get(s) or {}).get('neg')]
            log(f"    emiten {len(SEEDS)-len(sin)}/{len(SEEDS)}; sin mensaje (excluidas, P-I2): {sin}")
            tr = [('R', b, s, msgs[s]['neg'], T, nk, ktop, nkmax) for b in ORDEN for s in SEEDS
                  if (msgs.get(s) or {}).get('neg')]
            log(f"ETAPA 3/3 - RECEPTORES: {len(tr)} corridas de {T} pasos...")
            res = []
            for i, r in enumerate(pool.imap_unordered(tarea, tr, chunksize=1), 1):
                res.append(r)
                if i % 40 == 0 or i == len(tr):
                    log(f"          {i}/{len(tr)}")
        crudo = os.path.join(AQUI, f'c1_serie_s{SEEDS[0]}-{SEEDS[-1]}_{stamp}_crudo.json')
        with open(crudo, 'w', encoding='utf-8') as f:                  # ERR-54: el crudo, ANTES del analisis
            json.dump(dict(meta=dict(fecha=time.strftime('%Y-%m-%dT%H:%M:%S'), tipo='serie_C', T=T,
                                     semillas=SEEDS, celdas=N(CELDAS), brazos=N(BRAZOS), umbrales=UMBRALES,
                                     shas=SHAS(), nk=nk, ktop=ktop, nkmax=nkmax, kw_R=N(KW_R), kw_E=N(KW_E),
                                     python=platform.python_version(), numpy=np.__version__),
                           identidades=rc, mensajes=N(msgs), brazos=res), f, ensure_ascii=False, default=str)
        log(f"CRUDO -> {os.path.basename(crudo)}  sha256_16 = {h16(crudo)}  (ERR-54: antes del analisis)")
        try:
            V.update(veredicto(res, msgs, SEEDS))
            log(); log(frase(V)); log(f"  P-I3 (gemelo, prefijo exacto): {V['PI3']}")
        except Exception as e:
            V['analisis_error'] = f"{type(e).__name__}: {e}"
            log(f"*** EL ANALISIS FALLO ({V['analisis_error']}). El CRUDO ya esta en disco (ERR-54).")
        with open(os.path.join(AQUI, f'c1_serie_s{SEEDS[0]}-{SEEDS[-1]}_{stamp}.json'), 'w',
                  encoding='utf-8') as f:
            json.dump(dict(meta=dict(tipo='serie_C', T=T, semillas=SEEDS, shas=SHAS(), umbrales=UMBRALES,
                                     crudo=os.path.basename(crudo)), veredicto=N(V), identidades=rc,
                           mensajes=N(msgs), brazos=res), f, ensure_ascii=False, default=str)
        CF._log['f'].close()
        sys.exit(0)
    stamp = time.strftime('%Y%m%d_%H%M%S')
    CF._log['f'] = open(os.path.join(AQUI, f'c1_humo_s{SEEDS[0]}-{SEEDS[-1]}_{stamp}.log'), 'w',
                        encoding='utf-8', newline='\n')
    CF._log['t0'] = time.time()
    log("HUMO del CREADOR C de la junta de la fase 5: `variante_hija` -- LA CASILLA QUE SE DIVIDE.")
    log(f"UN proceso, sin Pool (regla 3). Semillas {SEEDS} (nave: 901-910), T = {T}, "
        f"{len(ORDEN)} brazos = {len(CELDAS)} celdas x {len(PLANTILLA)}.")
    for k, v in SHAS().items():
        marca = '' if k not in SHA_ESPERADOS else ('  OK' if v == SHA_ESPERADOS[k] else '  *** CAMBIO')
        log(f"    sha {k:24s} {v}{marca}")
    if any(SHAS()[k] != v for k, v in SHA_ESPERADOS.items()):
        raise SystemExit("Un origen cambio: no se mide nada.")

    log(f"1/3 EMISORES (el del bloque 6 SIN TOCAR: mv = 0, k = 1 = b4b bit a bit): {len(SEEDS)} corridas.")
    msgs = {}
    for s in SEEDS:
        t1 = time.time(); msgs[s] = B6R.emisor(s, T, nk, ktop, nkmax)
        q = msgs[s]['neg']
        log(f"    E s{s} {time.time()-t1:5.1f}s  mensaje "
            f"{q and (q['ref'], q['R'], 't=%d' % q['t'], 'tras %d exposiciones' % q['enc'])}")

    log("2/3 ESTRUCTURA (T = 0, sin simular): en cuantas de las 66 celdas NO se distingue el referente.")
    for s in SEEDS:
        e = B6R.estructura_v(s)
        log(f"    s{s}: BAR-H {e['BAR_H_v0']} (bin) -> {e['BAR_H_v1']} (con firma); BAR-T {e['BAR_T_v0']} -> "
            f"{e['BAR_T_v1']}; piso de forma {e['piso_forma_v0']}/32 -> {e['piso_forma_v1']}/32; "
            f"px en que difieren referente y hermana {e['BAR_H_px_dif']}")

    tr = [(b, s) for b in BRAZOS_HUMO for s in SEEDS if (msgs.get(s) or {}).get('neg')]
    log(f"3/3 RECEPTORES: {len(tr)} corridas de {T} pasos, un proceso (el humo no corre INM ni OTRO).")
    res, t_b = [], {}
    for b, s in tr:
        t1 = time.time(); r = corre(b, s, msgs[s]['neg'], T, nk, ktop, nkmax); dt = time.time() - t1
        res.append(r); t_b[b] = round(t_b.get(b, 0.0) + dt, 2)
        B, M = r['B4'], r['mem']
        log(f"    {b:14s} s{s} {dt:5.1f}s  entrega t={r['t_entrega']}  comio {1-int(B['evX'] or 0)} "
            f"(via {'RAPIDA' if B['fam1'] else 'lenta'})  dist {B['dist']}  okU {B['okU']}  muertes {r['deaths']}"
            f"  hijas {r['vh_hijas']}  k_conoce ref/herm/tok {r['conoce_ref']}/{r['conoce_herm']}/"
            f"{r['conoce_tok']}  dir_k {M['n_mismo_dir_k']}/32 (bin {M['n_mismo_bin_k']}/32)")

    crudo = os.path.join(AQUI, f'c1_humo_s{SEEDS[0]}-{SEEDS[-1]}_{stamp}_crudo.json')
    with open(crudo, 'w', encoding='utf-8') as f:                     # ERR-54: el crudo, ANTES del analisis
        json.dump(dict(meta=dict(fecha=time.strftime('%Y-%m-%dT%H:%M:%S'), tipo='humo_C', T=T, semillas=SEEDS,
                                 celdas=N(CELDAS), brazos=N(BRAZOS), shas=SHAS(), nk=nk, ktop=ktop, nkmax=nkmax,
                                 kw_R=N(KW_R), kw_E=N(KW_E), segundos=t_b,
                                 python=platform.python_version(), numpy=np.__version__),
                       mensajes=N(msgs), brazos=res), f, ensure_ascii=False, default=str)
    log(f"CRUDO -> {os.path.basename(crudo)}  sha256_16 = {h16(crudo)}  (ERR-54: antes del analisis)")
    try:
        V = veredicto(res, msgs, SEEDS)
        log(); log(frase(V))
        log(f"  P-I3 (gemelo, prefijo exacto): {V['PI3']}")
    except Exception as e:
        V = dict(error=f"{type(e).__name__}: {e}")
        log(f"*** EL ANALISIS FALLO ({V['error']}). El CRUDO ya esta en disco (ERR-54).")
    with open(os.path.join(AQUI, f'c1_humo_s{SEEDS[0]}-{SEEDS[-1]}_{stamp}.json'), 'w', encoding='utf-8') as f:
        json.dump(dict(meta=dict(tipo='humo_C', T=T, semillas=SEEDS, shas=SHAS()), veredicto=N(V),
                       mensajes=N(msgs), brazos=res), f, ensure_ascii=False, default=str)
    CF._log['f'].close()
