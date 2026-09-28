"""umbrales_examen_v144b = experimentos/tronco_v14_4_examen/umbrales_examen_v144.py (0df02bd6a4d548c4; solo se leyo) con: la
letra T-R (nueva, mas estricta), SEMILLAS NUEVAS (49001-50600, sin 50000; busca_semillas_v144b.py), el arnes esperado y las
PREDICCIONES de TERMO' (escritas ANTES del arnes y del humo). La letra T-A..T-G y T-H: la de v14.4 sin tocar. Generado POR ANCLAS por
experimentos/tronco_v14_4b_examen/construye_v144b.py. NO editar a mano. Lo que sigue es el docstring del origen (renombrado)."""
"""UMBRALES, SEMILLAS y PREDICCIONES del examen del CRITERIO DE TRONCO v4 sobre v14.4b = v14.3 + TERMO′ -- un solo modulo (ERR-31).

MISMA LETRA QUE EL EXAMEN DE v14.3 (encargo del coordinador: "misma letra y umbrales, SIN cambiarlos"): T-A..T-F y T-H se
IMPORTAN de experimentos/tronco_v14_3_examen/umbrales_examen_v143.py (LETRA, NUM y ERR122: la banda de azar G2 de T-B enmendada
por ERR-122 ANTES de la serie de v14.3, [0.31, 0.60], es la letra con la que v14.3 entro al tronco). Ese modulo a su vez restaba
la letra de criterio_v4/umbrales_v4, tronco_v15_dE5/corre_dE5_v2 y creacion_B/corre_codigo; regla14() del runner comprueba las
dos cosas. Lo UNICO propio de este examen es T-G (la capacidad que declara el candidato; la letra v4 la deja al preregistro) y
las semillas. Ningun numero de aqui se toca despues de correr; un cambio lleva ERR y fecha.
"""
import os, sys

_AQUI = os.path.dirname(os.path.abspath(__file__))
_V143EX = os.path.join(os.path.dirname(os.path.dirname(_AQUI)), 'experimentos', 'tronco_v14_3_examen')
if _V143EX not in sys.path:
    sys.path.append(_V143EX)   # AL FINAL: no tapa nada de organismo/ ni de esta carpeta
import umbrales_examen_v143 as U143   # la letra del examen de v14.3 (sha fijado en corre_examen_v144b.ANCLAS)

# ---------------------------------------------------------------- la letra (T-A..T-F y T-H: importada, sin tocar)
LETRA = {k: U143.LETRA[k] for k in ('T-A', 'T-B', 'T-C_i', 'T-C_ii', 'T-D', 'T-E', 'T-F', 'T-H')}
LETRA['T-G'] = ("capacidad declarada: TERMO sube el crecimiento neto del linaje en el mundo vivo. Brazo CUELLO_MIN, n = 80, "
                "d = r - r_OFF pareado (nominal): G-1 CAND gana: LI_95(d_CAND) > 1 (superioridad de una cola, z 1.645, margen m = 1); "
                "G-2 el CONTROL TERMOINV no gana: LI_95(d_CTRL) <= 1; G-3 la pieza actua (a_no + a_si > 0) en >= 95 % de las "
                "corridas del CANDIDATO. VIVO: se reporta, no decide")
NUM = dict(U143.NUM)
# ---------------------------------------------------------------- v14.4b: T-R, la reversion con la pieza ACTUANDO (mas estricta; no reemplaza nada)
LETRA['T-R'] = ("v14.4b: T-C (ii) pasa por la letra v4 (NI en rev, margen 12.5) Y la pieza ACTUA (a_no + a_si > 0) en >= 95 % de las "
                "80 corridas CAND de T-C (ii) (G-3 analogo): una reversion aprobada con la pieza muda no cuenta")
TR = dict(actua_frac=0.95, n=80)
ERR122 = U143.ERR122

# ---------------------------------------------------------------- T-G: la capacidad que DECLARA el candidato (PREREGISTRO sec. 4)
# Nulo, margen y n: analiza_potencia_v144.py sobre los crudos REALES del mundo vivo del examen de v14.3 (160 semillas por brazo;
# datos/humo/potencia_examen_v144_20260928_121917.json, sha 4e4df40a5c3cc67d). En CUELLO_MIN: sd(d) 18.8; con m = 0 el nulo no
# centrado pasa G-1 0.107 (> 0.05, regla 15) -> m = 1: P(G-1 | nulo) 0.044, P(G-2 | nulo) 0.994, P(T-G | nulo) 0.042; potencia
# de G-1 en delta = +6 de r: 0.883; P(T-G) en ese margen con CTRL nulo 0.877 (>= 0.80).
TG = dict(brazo='CUELLO_MIN', informe='VIVO', z=1.645, n=80, m=1.0, delta_margen=6.0, actua_frac=0.95, ctrl='CTRL',
          nulo=dict(fuente='datos/humo/potencia_examen_v144_20260928_121917.json', sha='4e4df40a5c3cc67d',
                    P_G1=0.0439, P_G2=0.9941, P_TG=0.0421, potencia_G1_delta6=0.8828, P_TG_delta6=0.8769))

# ---------------------------------------------------------------- brazos
ARMS_VIVO = ['OFF', 'CAND', 'TRONCO_B', 'PLACEBO']   # 4' de v4: TRONCO_B y PLACEBO obligatorios en el mundo vivo
ARMS_TA = ARMS_VIVO + ['CTRL']                      # T-G: el CONTROL TERMOINV (termo = 2) corre en los dos brazos de T-A
BRAZOS_TA = ['VIVO', 'CUELLO_MIN']
ARMS_SAL = ['OFF', 'CAND']
ORGS_EX = ['CAND', 'TRONCO']                          # examen v3' y T-B: v14.4 y el TRONCO v14.3 (CONGELADO) en las MISMAS semillas
SEIS = list(U143.SEIS)
REGLAS_TB = list(U143.REGLAS_TB)
T_VIVO = U143.T_VIVO
T_HUMO = U143.T_HUMO
DESPL_TRONCO_B = U143.DESPL_TRONCO_B

# ---------------------------------------------------------------- SEMILLAS NUEVAS (busca_semillas_v144b.py, 28-sep-2026: 43 957
# archivos de texto de PROYECTOS/JUACO; en 47000-48600 y 147000-148600 solo aparecen fragmentos de sha y un numero de issue;
# ninguna en contexto de semilla ni en nombres de archivo. Salida en busca_semillas_v144b_salida.txt; PREREGISTRO sec. 8)
# v14.4b: SEMILLAS NUEVAS (busca_semillas_v144b.py, 28-sep-2026, repo entero: los numeros 49001-49999, 50001-50600 y 149001-149999 no
# aparecen en ningun .py/.md, ni en contexto de semilla, ni en nombres de archivo; en los datos solo como pasos de tiempo). 50000 (T/2
# de medio repo) se excluye. T-D: la seleccion ESTRUCTURAL (diagnostico_codigos.solapamientos, sin simular) sobre sus rangos; el runner
# la recalcula y se para si no coincide. TRONCO_B = s + 100000 -> 149101-149380.
_r = lambda a, b: list(range(a, b + 1))
SEMILLAS = {
    'serie': dict(EX=_r(49001, 49020), VIVO=_r(49101, 49180),
                  TD_rango=(49401, 49999),
                  ALIAS=[49449, 49492, 49509, 49528, 49563, 49597, 49621, 49652, 49718],
                  LIMPIAS=[49407, 49418, 49431, 49444, 49450, 49451, 49457, 49464, 49466]),
    'replica': dict(EX=_r(49021, 49040), VIVO=_r(49201, 49280),
                    TD_rango=(50001, 50600),
                    ALIAS=[50004, 50054, 50181, 50208, 50212, 50235, 50250, 50294, 50296],
                    LIMPIAS=[50001, 50005, 50008, 50011, 50019, 50020, 50030, 50031, 50040]),
    # RESERVA: SOLO si TRONCO_B no pasa (serie del mundo vivo que "no se lee", letra v4 4'): T-A + T-C (ii) + T-F vivo + T-G + T-R
    'reserva': dict(VIVO=_r(49301, 49380)),
    'humo': [49041, 49042, 49043],   # + la ALIAS historica 326 (ya publica) para el camino de B-5 en el humo
    'identidad': [49045, 49046, 49047],
}

# ---------------------------------------------------------------- el arnes que debe dar N/N antes de mirar un numero
ARNES_ESPERADO = 'RESULTADO: 151/151'   # v14.4b identidad_v144bex.py: (0) 10 (A) 15 (I) 16 (T) 12 (V) 4 (P) 9 (L) 3 (D) 6 (R) 44 (J) 16 (K) 16

# ---------------------------------------------------------------- predicciones firmadas de TERMO' (PREREGISTRO_examen_v144b sec. 5)
# Escritas el 28-sep-2026 ANTES del arnes y del humo de v14.4b, desde el mecanismo y los crudos de la SERIE de TERMO (47101-47180, que ya
# existian): (2) hace a v14.4b y v14.4bg la FISICA de v14.3 -> T-B, T-E, T-C (i) y T-F examen son el tronco contra si mismo. Sin
# inversion (T-A, T-D, T-G) la tabla que olvida da las mismas decisiones que TERMO -> se esperan los numeros de TERMO. En T-C (ii) la
# tabla deja de gobernar A a la primera mordida mala, PERO la pieza pasa a gobernar B (la comida nueva) y lo come ~25 % menos (TERMO,
# antes de invertir: A 152 contra 204 del OFF por cuarto, y B-veneno 119 contra 156); rev = mordB_Q4 - mordA_Q4 es una DIFERENCIA DE
# CONTEOS: si todo baja ~25 %, rev baja de ~44 a ~33 y d ~ -11 contra el margen -12.5 (LI ~ -15). Por eso T-C (ii) y T-R son las
# puertas en riesgo aun con la tabla que olvida (trampa 3: el mundo que se come la comida).
PRED = {
    'legible': dict(p=0.97, frase="TRONCO_B pasa T-A, T-C (ii) y T-F vivo (las tareas calibradas; en TERMO y en v14.3 pasaron)"),
    'T-A': dict(p=0.95, frase="como TERMO: r VIVO CAND mediana en [-45, -20] (OFF ~ -75), CUELLO_MIN en [0, +15] (OFF ~ -6); muertes 0.6-0.95 x"),
    'T-B': dict(p=0.95, frase="CAND == TRONCO en la fisica (40/40 identicas): G1 1.000, G2 >= 0.95, azar G2 = el del tronco en [0.31, 0.60]"),
    'T-C': dict(p=0.33, frase="(i) == tronco (p 0.97); (ii) rev CAND mediana en [15, 40] (OFF ~ 44), d media en [-20, -3]: LI > -12.5 con p 0.35"),
    'T-D': dict(p=0.95, frase="como TERMO: C1, C2, C6 pasan (la sal muda tiene s nula; la pieza no gobierna B ni D)"),
    'T-E': dict(p=0.97, frase="CAND == TRONCO en la fisica (120/120 identicas): cada escenario 20/20 salvo las clausulas absolutas del tronco"),
    'T-F': dict(p=0.90, frase="examen: razon 1.0 (identico); vivo: muertes T-C (ii) 0.9-1.1 x, T-A <= 1.0 x (como TERMO)"),
    'T-G': dict(p=0.90, frase="como TERMO: G-1 d media en [+8, +22] (LI > 1 con p 0.92), G-2 TERMOINV no gana (p 0.98), G-3 80/80"),
    'T-R': dict(p=0.34, frase="la pieza actua en T-C (ii) en 80/80 (gobierna A antes de invertir y B despues): T-R ~ T-C (ii)"),
    'serie': dict(p=0.25, frase="producto (T-C ii y T-R casi la misma apuesta) ~ 0.25; P(serie y replica) ~ 0.15: VEREDICTO previsto NO PASA (p ~ 0.85), por T-C (ii) y T-R"),
}
