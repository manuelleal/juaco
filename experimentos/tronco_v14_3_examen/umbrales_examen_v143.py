"""UMBRALES, SEMILLAS y PREDICCIONES del examen del CRITERIO DE TRONCO v4 sobre v14.3 -- un solo modulo (ERR-31).

La LETRA no se escribe aqui: se IMPORTA de donde vive (y regla14() del runner comprueba que lo restado aqui coincide):
  T-A, T-C (ii), T-F vivo  <- experimentos/criterio_v4/umbrales_v4.py (V4)            (la letra calibrada en V4-CAL)
  T-B, T-C (i), T-E, T-F examen <- experimentos/tronco_v15_dE5/corre_dE5_v2.py (UMB, TOL, TOL_COME, PUERTA_E, CLAUSULAS)
                              (la letra de v2; v3 y v4 dicen "sin cambio")
  T-D                      <- experimentos/creacion_B/corre_codigo.py (UMBRALES C1, C2, C6)  (ERR-31: importados)
  T-G (la capacidad que declara el candidato) <- experimentos/subida_n7/corre_n7.py (U: T1..T5) + las tres clausulas G-1..G-3
                              de abajo (las de P2 y P6 del preregistro de subida_n7, sin tocar un numero)
Ningun numero de aqui se toca despues de correr; un cambio lleva ERR y fecha (regla 3 / regla 11 de EQUIPO.md).

ENMIENDA ERR-122 (23-sep-2026 ~21:10, ANTES de la serie; no existe ningun dato de serie): decision del director "corrige la
banda" (opcion (b) del PREREGISTRO §7). La banda de azar G2 de T-B pasa de [0.42, 0.58] a [0.31, 0.60] (nulo real del tronco,
40 semillas 101-140; ver ERR122 abajo). Es la UNICA diferencia con la letra importada: regla14() la registra como diferencia
DECLARADA. La banda vieja se sigue calculando y se REPORTA (CAND y TRONCO), sin decidir. bateria_generaliza_v142 (CONGELADA) y
su copia v143 conservan su banda interna [0.42, 0.58]: el examen no usa su veredicto interno, solo sus valores crudos.
"""

# ---------------------------------------------------------------- lo que el runner imprime al lado de cada puerta (ERR-89)
LETRA = {
    'T-A': "v4 T-A: en VIVO y en CUELLO_MIN: mediana de muertes <= 1.10 x tronco, mediana de r >= tronco - 10, y no "
           "inferioridad de una cola al 95 % (z 1.645) en r con margen 10 (LI > -10); n = 80 por brazo",
    'T-B': "G1 >= 0.80, G2 >= 0.85, azar G1 en [0.35, 0.65], azar G2 en [0.31, 0.60] (ENMIENDA ERR-122; la de la letra "
           "[0.42, 0.58] se reporta y NO decide), K 20/20 (bateria_generaliza, 20 semillas)",
    'T-C_i': "examen E2: come B en Q4 >= 50 en >= 18/20",
    'T-C_ii': "v4 T-C (ii): no inferioridad de una cola al 95 % en rev con margen 12.5 (LI > -12.5); n = 80",
    'T-D': "bloque de la sal (9 ALIAS + 9 LIMPIAS, sal muda): C1, C2, C6 de B-5 importados de creacion_B/corre_codigo.UMBRALES",
    'T-E': "examen v3': conducta por escenario frente al tronco en las mismas semillas >= 18/20, tolerancias 1.10 / 0.8",
    'T-F': "celdas, divisiones y muertes (medianas) <= 1.25 x tronco en el examen (seis etapas) y en el mundo vivo "
           "(T-A y T-C ii, divisor max(tronco, 1))",
    'T-G': "capacidad declarada: composicion en 3T-k (letra de subida_n7): G-1 K_max(N) >= 5; G-2 N > T142 en lift_q4 "
           "pareado >= 15/20 en k = 3, 4 y 5; G-3 el canal falso NC3C no separa (sep mediana < 1.0 y lift_q4 mediana < 0.15) "
           "en ningun k de 1 a 8",
    'T-H': "ESCALA: reportada, NO eliminatoria; su instrumento (criterio v4 §5) no esta construido: NO SE MIDE y se declara",
}
# ---------------------------------------------------------------- ENMIENDA ERR-122 (antes de la serie; PREREGISTRO §7)
ERR122 = dict(
    err='ERR-122',
    fecha='2026-09-23 ~21:10 (antes de la serie: ningun dato de serie existe)',
    decision="director: 'corrige la banda' = opcion (b) del PREREGISTRO_examen_v143 §7",
    banda_nueva=(0.31, 0.60),   # DECIDE azar G2 de T-B (CAND); tambien se aplica al TRONCO, que se reporta al lado
    banda_vieja=(0.42, 0.58),   # == corre_dE5_v2.UMB['T-B']['azar2'] (letra v2 = v3 = v4) y banda interna de bateria_generaliza:
                                # SOLO INFORME (CAND y TRONCO), no decide
    nulo=dict(fuente='datos/humo/potencia_examen_v143_20260923_203158.json (sha 281b2e55b4ad1aaf; analiza_potencia_v143.py)',
              semillas='101-140 (tronco v14.1 == v14.2 == v14.3 en el mundo de regla)', mediana_azar_G2=0.4344,
              cuantiles_mediana_n20={'0.005': 0.3028, '0.01': 0.3184, '0.99': 0.5974, '0.995': 0.6033},
              P_TB_bajo_el_nulo=dict(banda_vieja=0.549, banda_nueva=0.957)),
)
# los numeros que la letra fija (regla14() los compara con los modulos de donde se importan; TB_azar2 es la UNICA diferencia,
# DECLARADA por ERR-122: el origen corre_dE5_v2 dice [0.42, 0.58] == ERR122['banda_vieja'])
NUM = dict(TA_muertes=1.10, TA_r_delta=10.0, TA_margen=10.0, z=1.645, n_vivo=80, TC_margen=12.5, TF_razon=1.25,
           TB_g1=0.80, TB_g2=0.85, TB_azar=(0.35, 0.65), TB_azar2=ERR122['banda_nueva'], TB_cob=6, n_examen=20,
           TC_i_come=50, puerta_E=18, tol=1.10, tol_come=0.8)

# ---------------------------------------------------------------- T-G: la capacidad que DECLARA el candidato (3T-k, subida_n7)
TG = dict(ks=[1, 2, 3, 4, 5, 6, 7, 8], brazos=['T142', 'N', 'NC3C'], T=100000,
          G1_kmax=5,                      # P2 de subida_n7: N compone en k = 1..5 (FUNCIONA pedia K_max >= 5 en serie y replica)
          G2_ks=[3, 4, 5], G2_n=15,       # P2 de subida_n7: N > T142 en lift_q4 pareado >= 15/20 para k = 3, 4, 5
          G3_sep=1.0, G3_lift=0.15)       # P6 de subida_n7: NC3C sep mediana < 1.0 y lift_q4 < 0.15 en todo k (== U['T4_*'])

# ---------------------------------------------------------------- brazos
ARMS_VIVO = ['OFF', 'CAND', 'TRONCO_B', 'PLACEBO']   # 4' de v4: TRONCO_B y PLACEBO obligatorios en el mundo vivo
BRAZOS_TA = ['VIVO', 'CUELLO_MIN']
ARMS_SAL = ['OFF', 'CAND']
ORGS_EX = ['CAND', 'TRONCO']                          # examen v3' y T-B: el candidato y el tronco en las MISMAS semillas
SEIS = ['E1', 'E2', 'E2I', 'E2J', 'E2K', 'E2L']
REGLAS_TB = ['px0', 'azar']
T_VIVO = 100000
T_HUMO = 20000
DESPL_TRONCO_B = 100000   # == umbrales_v4.SEMILLAS['DESPLAZAMIENTO_TRONCO_B'] (lo comprueba regla14)

# ---------------------------------------------------------------- SEMILLAS NUEVAS (grep 23-sep-2026 ~21:00 sobre bundle y los 8
# worktrees de PROYECTOS/JUACO/* + anclado/sandbox/respaldo: 43000-44600 y 143000-144600 solo aparecen como sellos de hora
# HHMMSS en nombres de archivo, fragmentos de sha, URL o conteos de pasos; nunca como semilla. Detalle en el PREREGISTRO §8)
_r = lambda a, b: list(range(a, b + 1))
SEMILLAS = {
    'serie': dict(EX=_r(43001, 43020), VIVO=_r(43101, 43180), TG=_r(43401, 43420),
                  TD_rango=(43501, 44000),
                  ALIAS=[43568, 43572, 43575, 43605, 43626, 43647, 43654, 43712, 43748],
                  LIMPIAS=[43505, 43522, 43528, 43529, 43539, 43541, 43551, 43556, 43571]),
    'replica': dict(EX=_r(43021, 43040), VIVO=_r(43201, 43280), TG=_r(43421, 43440),
                    TD_rango=(44001, 44500),
                    ALIAS=[44031, 44099, 44119, 44138, 44185, 44218, 44237, 44242, 44291],
                    LIMPIAS=[44004, 44005, 44015, 44016, 44017, 44020, 44022, 44025, 44027]),
    # RESERVA: SOLO si TRONCO_B no pasa (serie del mundo vivo que "no se lee", letra v4 4'): T-A + T-C (ii) + T-F vivo
    'reserva': dict(VIVO=_r(43301, 43380)),
    'humo': [43041, 43042, 43043, 43044],   # + la ALIAS historica 326 (ya publica) para el camino de B-5 en el humo
    'identidad': [43045, 43046, 43047],
}
# ALIAS = |code(D) & code(B)| = 3 y LIMPIAS = |code(D) & code(B)| = 0: las 9 PRIMERAS de su rango, calculadas por
# experimentos/nivel11_mundo_vivo/diagnostico_codigos.solapamientos (no simula un paso) ANTES de correr nada; el runner las
# RECALCULA al arrancar y se para si no coinciden (como corre_sal.guarda_semillas).

# ---------------------------------------------------------------- el arnes que debe dar N/N antes de mirar un numero
ARNES_ESPERADO = 'RESULTADO: 114/114'   # 106 + (R) T-B partida en dos por ERR-122 + (X) 7 chequeos de ERR-122

# ---------------------------------------------------------------- predicciones firmadas (PREREGISTRO §5), ANTES de la serie
# p = probabilidad de que la puerta PASE por la letra en UNA serie. Calculo: analiza_potencia_v143.py sobre datos REALES
# (datos/humo/potencia_examen_v143_20260923_203158.json, sha 281b2e55b4ad1aaf). CAND == tronco en T-A..T-F: se calcula el tronco.
PRED = {
    'legible': dict(p=0.97, frase="TRONCO_B pasa T-A, T-C (ii) y T-F vivo: reparto del nulo real de V4-CAL 0.968-0.976 (con la reserva ~0.999)"),
    'T-A': dict(p=1.00, frase="CAND == OFF bit a bit en las 160 corridas: d = 0, LI = 0 > -10; razon de muertes 1.000"),
    'T-B': dict(p=0.957, frase="ERR-122: G1 1.000, G2 >= 0.93, K 20/20, azar G1 en banda (0.969), azar G2 0.33-0.55 en [0.31, 0.60]: "
                               "T-B entera 0.957 bajo el nulo real (antes de ERR-122, con [0.42, 0.58]: 0.55)"),
    'T-C': dict(p=0.97, frase="(i) come B Q4 >= 50 en 20/20 (el tronco: 60/60, minimo 51; cota >= 0.93); (ii) CAND == OFF: LI = 0 > -12.5"),
    'T-D': dict(p=0.95, frase="C1 9/9 (|W[sal]| 0.0), C2 9/9 (W[veneno] -3.0), C6 9/9: el tronco con B-5 lo hace en 36/36 semillas (declarada)"),
    'T-E': dict(p=0.97, frase="20/20 en las seis etapas (identico al tronco; solo pesan E2 come B >= 50 y E2I tasa, 60/60 y 60/60 en el tronco)"),
    'T-F': dict(p=1.00, frase="razones 1.000 exactas (identico al tronco) en el examen y en el mundo vivo"),
    'T-G': dict(p=0.99, frase="K_max(N) = 8 (1000/1000 remuestreos), K_max(T142) = 1, NC3C 0; N > T142 20/20 en k = 3, 4, 5"),
    'inercia': dict(p=1.00, frase="CAND == tronco bit a bit en TODAS las corridas de T-A, T-B, T-C, T-D, T-E (mismos kwargs + norm_lenta)"),
    'serie': dict(p=0.86, frase="ERR-122: P(PASA una serie) 0.82-0.91; P(serie y replica) 0.67-0.82 (antes de ERR-122: 0.47-0.52 y "
                                "0.22-0.27; sin la banda de azar G2: 0.85 y 0.73)"),
}
