"""UMBRALES del CRITERIO DE TRONCO v4 y de su calibracion V4-CAL — un solo modulo, importado por el runner (ERR-31).
Copiados de registro/CRITERIO_TRONCO_v4.md y de experimentos/criterio_v4/PREREGISTRO_calibracion_v4.md. Ninguno se
toca despues de correr; cualquier cambio lleva ERR y fecha (regla 3 / regla 11 de EQUIPO.md).

Los numeros de potencia que justifican cada umbral salen de analiza_potencia_v4.py sobre las 320 corridas reales del
nulo de A-CAL (crudos de critv3_20260921_165615 y critv3_rep_20260921_170812):
    datos/humo/potencia_v4_20260922_125604.json       (sha 2d975a4885eb41ae)
    datos/humo/potencia_v4_meta_20260922_130017.json  (sha 1e9eb3843c48703e)
"""

Z = 1.645            # una cola al 95 %

# ---------------------------------------------------------------- la letra v3 (retirada; se reporta al lado)
V3 = {
    'T-A': dict(frase="v3 T-A (RETIRADA): medianas (muertes <= 1.10x, r >= tronco-10) + NI margen 10, n = 40",
                muertes=1.10, r_delta=10.0, margen=10.0, z=Z, n=40),
    'T-C_ii': dict(frase="v3 T-C (ii) (RETIRADA): NI margen 10 en rev, n = 40", margen=10.0, z=Z, n=40),
}
# ---------------------------------------------------------------- la letra v2 (historia; se reporta al lado, ERR-91)
V2 = {
    'T-A': dict(frase="v2 T-A (historia): medianas + A12(r) >= 0.50 pareado", muertes=1.10, r_delta=10.0, a12=0.50, n=20),
    'T-C_ii': dict(frase="v2 T-C (ii) (historia): A12(rev) >= 0.75 pareado", a12=0.75, n=20),
}

# ---------------------------------------------------------------- LA LETRA v4 (registro/CRITERIO_TRONCO_v4.md, ERR-94)
V4 = {
    'T-A': dict(
        frase="v4 T-A: en VIVO y en CUELLO_MIN: mediana de muertes <= 1.10 x tronco, mediana de r >= tronco - 10, y NO "
              "INFERIORIDAD de una cola al 95 % (z = 1.645) en r con margen 10 (LI > -10). n = 80 por brazo.",
        muertes=1.10, r_delta=10.0, margen=10.0, z=Z, n=80,
        # potencia (bootstrap del nulo OFF, 80 corridas por brazo): P(pasa|nulo) n40 0.928 / n80 0.999;
        # P(pasa|delta=-10) n80 0.003; P(pasa|delta=-20) 0.000
    ),
    'T-C_ii': dict(
        frase="v4 T-C (ii): NO INFERIORIDAD de una cola al 95 % (z = 1.645) en rev con margen 12.5 (LI > -12.5). n = 80.",
        margen=12.5, z=Z, n=80,
        # potencia (sd(d) no pareada 28.3-29.0): P(pasa|nulo) 0.987-0.990; techo de sd(d) para 0.95: 34.0
        # (observado 27.4 y 30.9); P(pasa|delta=-12.5) 0.05; P(pasa|delta=-10) ~0.19; P(pasa|delta=-20) 0.000
    ),
    'T-F_vivo': dict(
        frase="v4 T-F (parte del mundo vivo): medianas de muertes, celdas y splits <= 1.25 x tronco (divisor max(tronco, 1))",
        razon=1.25),
}

# ---------------------------------------------------------------- las opciones de ERR-94, con su tasa de falso rechazo
# (se imprimen en el runner al lado de la letra elegida; NO deciden nada)
OPCIONES_ERR94 = {
    'v3 (n40, m10)':                dict(n_TA=40, n_TC=40, m_TC=10.0, P_TA=0.928, P_TC=0.707, P_juntas=0.656),
    'solo n = 80 (m10)':            dict(n_TA=80, n_TC=80, m_TC=10.0, P_TA=0.999, P_TC=0.931, P_juntas=0.930),
    'solo margen 15 (n40)':         dict(n_TA=40, n_TC=40, m_TC=15.0, P_TA=0.928, P_TC=0.950, P_juntas=0.882),
    'ELEGIDA: n = 80 y m_TC 12.5':  dict(n_TA=80, n_TC=80, m_TC=12.5, P_TA=0.999, P_TC=0.987, P_juntas=0.986),
    'n = 80 y m_TC 15 (reserva)':   dict(n_TA=80, n_TC=80, m_TC=15.0, P_TA=0.999, P_TC=0.999, P_juntas=0.998),
}

# ---------------------------------------------------------------- calibracion V4-CAL: condiciones de uso (PREREGISTRO §5/§6)
CAL = {
    'V4-1': dict(frase="REPARTO del nulo (OFF + TRONCO_B, ley identica por construccion): P(T-A v4 y T-C ii v4 pasan) >= 0.95",
                 lo=0.95),
    'V4-2': dict(frase="TRONCO_B (el tronco en semillas s+100000, sin perilla) PASA T-A, T-C ii y T-F vivo bajo v4 en la realizacion"),
    'V4-3': dict(frase="PLACEBO (candidato inerte, placebo = 1) PASA T-A, T-C ii y T-F vivo bajo v4 en la realizacion"),
    'V4-4': dict(frase="PEOR (coste de vida x1.5, conocido malo x2 series) CAE v4 en la realizacion"),
    'V4-5': dict(frase="desplazamiento exacto por reparto: delta = -20 pasa <= 0.05 en T-A y en T-C ii, y delta = -margen "
                       "pasa <= 0.15 en cada puerta (por construccion ~0.05; 0.15 deja lugar al error de estimacion del reparto)",
                 hi20=0.05, hi_margen=0.15),
}
# CAL-4 de v3 deja de ser gatillo: sus 6 marginales se REPORTAN con la banda de Bonferroni que tiene 0.95 bajo ley
# identica (n = 80: 0.5 +- 2.638 x 0.0458 = [0.379, 0.621]). Medido: la banda vieja [0.40, 0.60] con n = 40 dispara en
# falso 0.468 de las veces; con n = 80, 0.113.
MARGINALES = dict(lo=0.379, hi=0.621, z_bonf=2.638, sd_n80=0.0458, es_puerta=False)

# ---------------------------------------------------------------- predicciones firmadas (PREREGISTRO §5), ANTES del humo
PRED = {
    'P-1': dict(frase="V4-1 (reparto del nulo, las dos puertas juntas)", lo=0.965, hi=1.000),
    'P-2': dict(frase="T-C (ii) sola por reparto", lo=0.970, hi=1.000),
    'P-3': dict(frase="T-A entera sola por reparto", lo=0.985, hi=1.000),
    'P-4': dict(frase="v2 sobre el mismo nulo (T-A, n = 20) sigue rechazando al tronco", lo=0.20, hi=0.45),
    'P-5': dict(frase="v3 sobre el mismo nulo (n = 40, T-A y T-C ii juntas)", lo=0.55, hi=0.80),
    'P-6': dict(frase="marginales dentro de la banda de Bonferroni: TRONCO_B 6/6; PLACEBO >= 5/6"),
    'P-7': dict(frase="PEOR: delta_r mediano <= -60 en los dos brazos de T-A (medido -74..-114)"),
}

# ---------------------------------------------------------------- semillas (verificadas libres con grep el 22-sep 13:0x)
SEMILLAS = dict(
    SERIE=list(range(2841, 2921)),      # 80: T-A (VIVO y CUELLO_MIN) y T-C (ii) usan las MISMAS 80 (mundos distintos)
    HUMO=[2921, 2922],                  # fuera de la serie: el humo no mira ninguna semilla de la serie
    IDENTIDAD=[2923],                   # la usa identidad_v4.py (T = 20000); no es de la serie
    RESERVA=list(range(2924, 2941)),    # 17 libres, sin uso asignado
    DESPLAZAMIENTO_TRONCO_B=100000,     # TRONCO_B corre la semilla s + 100000 (102841-102920 libres como semilla)
    REPLICA=None,                       # 80 semillas NUEVAS a asignar por el coordinador (no caben en 2841-2940)
    ocupadas="2441-2840, 3001-3299, 4001-4199, 5001-5020, 6001-6020 reservadas por otros frentes (22-sep)",
)

# ---------------------------------------------------------------- brazos
PEOR = dict(m=1.50, costo_base=0.001,
            frase="PEOR = el mismo organismo con costo = costo_a = 0.001 x 1.5 (fijado en A-CAL 21-sep; no se recalibra)")
K_PLACEBO = 1
