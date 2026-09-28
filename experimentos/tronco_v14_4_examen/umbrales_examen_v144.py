"""UMBRALES, SEMILLAS y PREDICCIONES del examen del CRITERIO DE TRONCO v4 sobre v14.4 = v14.3 + TERMO -- un solo modulo (ERR-31).

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
import umbrales_examen_v143 as U143   # la letra del examen de v14.3 (sha fijado en corre_examen_v144.ANCLAS)

# ---------------------------------------------------------------- la letra (T-A..T-F y T-H: importada, sin tocar)
LETRA = {k: U143.LETRA[k] for k in ('T-A', 'T-B', 'T-C_i', 'T-C_ii', 'T-D', 'T-E', 'T-F', 'T-H')}
LETRA['T-G'] = ("capacidad declarada: TERMO sube el crecimiento neto del linaje en el mundo vivo. Brazo CUELLO_MIN, n = 80, "
                "d = r - r_OFF pareado (nominal): G-1 CAND gana: LI_95(d_CAND) > 1 (superioridad de una cola, z 1.645, margen m = 1); "
                "G-2 el CONTROL TERMOINV no gana: LI_95(d_CTRL) <= 1; G-3 la pieza actua (a_no + a_si > 0) en >= 95 % de las "
                "corridas del CANDIDATO. VIVO: se reporta, no decide")
NUM = dict(U143.NUM)
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

# ---------------------------------------------------------------- SEMILLAS NUEVAS (busca_semillas_v144.py, 28-sep-2026: 43 957
# archivos de texto de PROYECTOS/JUACO; en 47000-48600 y 147000-148600 solo aparecen fragmentos de sha y un numero de issue;
# ninguna en contexto de semilla ni en nombres de archivo. Salida en busca_semillas_v144_salida.txt; PREREGISTRO sec. 8)
_r = lambda a, b: list(range(a, b + 1))
SEMILLAS = {
    'serie': dict(EX=_r(47001, 47020), VIVO=_r(47101, 47180),
                  TD_rango=(47501, 48000),
                  ALIAS=[47518, 47575, 47597, 47608, 47621, 47686, 47713, 47714, 47725],
                  LIMPIAS=[47501, 47508, 47516, 47521, 47530, 47554, 47556, 47559, 47568]),
    'replica': dict(EX=_r(47021, 47040), VIVO=_r(47201, 47280),
                    TD_rango=(48001, 48500),
                    ALIAS=[48011, 48031, 48070, 48071, 48074, 48094, 48101, 48116, 48117],
                    LIMPIAS=[48009, 48012, 48017, 48020, 48028, 48029, 48030, 48043, 48051]),
    # RESERVA: SOLO si TRONCO_B no pasa (serie del mundo vivo que "no se lee", letra v4 4'): T-A + T-C (ii) + T-F vivo + T-G
    'reserva': dict(VIVO=_r(47301, 47380)),
    'humo': [47041, 47042, 47043],   # + la ALIAS historica 326 (ya publica) para el camino de B-5 en el humo
    'identidad': [47045, 47046, 47047],
}

# ---------------------------------------------------------------- el arnes que debe dar N/N antes de mirar un numero
ARNES_ESPERADO = 'RESULTADO: 126/126'   # (0) 6 (A) 21 (A') 5 (P) 10 (L) 5 (X) 2 (D) 7 (R) 41 (J) 10 (K) 19; primera corrida limpia

# ---------------------------------------------------------------- predicciones firmadas (PREREGISTRO sec. 5), ANTES del humo
# p = probabilidad de que la puerta PASE por la letra en UNA serie.
# Escritas el 28-sep-2026 ANTES del humo, desde el mecanismo (sec. 5 del PREREGISTRO): la memoria de lo sentido (_adS) SUMA sin
# olvido; tras una reversion, lo que fue bueno sigue 'sentido bueno' hasta que las mordidas nuevas (-0.4) pesen mas del doble que
# las viejas (+0.8): TERMO lo sigue mordiendo (T-E E2 y T-C ii). Ademas no hay ningun dato de v14.3 + TERMO sin FILTRO ni APR.
PRED = {
    'legible': dict(p=0.97, frase="TRONCO_B pasa T-A, T-C (ii) y T-F vivo: las tareas calibradas de V4-CAL, igual que en el examen de v14.3"),
    'T-A': dict(p=0.55, frase="r VIVO CAND mediana en [-85, -55] (OFF ~ -72), CUELLO_MIN en [-20, +10] (OFF ~ -7); muertes 0.85-1.15 x"),
    'T-B': dict(p=0.90, frase="G1 >= 0.90, G2 0.93-1.00, azar G2 0.33-0.55, K 20/20: la conducta de primer encuentro (ba) no la toca la pieza"),
    'T-C': dict(p=0.20, frase="(i) come B Q4 >= 50 en >= 18/20 con p 0.85; (ii) rev CAND mediana en [-30, +25] (OFF ~ 42): LI > -12.5 con p 0.25"),
    'T-D': dict(p=0.85, frase="C1, C2, C6 como el tronco (la pieza no gobierna B ni D; la sal muda tiene s nula)"),
    'T-E': dict(p=0.05, frase="cae E2 'muerde A Q4 <= 1.10 x tronco': A sigue sentida buena tras invertir; muerde A en Q4 (mediana) 60-250 contra ~10"),
    'T-F': dict(p=0.40, frase="examen p 0.80; vivo p 0.50 (las muertes de T-C ii suben 1.1-1.6 x por las mordidas de A envenenada)"),
    'T-G': dict(p=0.25, frase="G-1 (LI > 1 en CUELLO_MIN) p 0.25: d mediana en [-10, +10]; G-2 (TERMOINV no gana) p 0.95; TERMOINV r <= OFF - 10 con p 0.7"),
    'serie': dict(p=0.005, frase="producto < 0.01; P(serie y replica) ~ 0: VEREDICTO previsto NO PASA (p ~ 0.99), por T-E y T-C (ii); probable T-G"),
}
