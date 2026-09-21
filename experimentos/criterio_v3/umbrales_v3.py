"""UMBRALES del bloque A-CAL — un solo modulo, importado por el runner (ERR-31: el runner NUNCA lee los umbrales
de una bateria ni los inventa; los lee de aqui, y aqui estan COPIADOS de registro/CRITERIO_TRONCO_v2.md,
registro/CRITERIO_TRONCO_v3.md y PREREGISTRO_calibracion_v3.md).

No se toca despues de correr. Cualquier cambio lleva ERR y fecha (regla 3 / regla 11 de EQUIPO.md).
"""

# ---------------------------------------------------------------- la letra v2 (registro/CRITERIO_TRONCO_v2.md, 18-sep)
V2 = {
    'T-A': dict(
        frase="v2 T-A: muertes <= 1.10 x tronco (mediana) y r >= tronco - 10 (mediana) y A12(r) >= 0.50 pareado",
        muertes=1.10, r_delta=10.0, a12=0.50, n=20),
    'T-C_ii': dict(
        frase="v2 T-C (ii): A12(rev cand > tronco) >= 0.75 pareado",
        a12=0.75, n=20),
}

# ---------------------------------------------------------------- la letra v3 (registro/CRITERIO_TRONCO_v3.md, 21-sep, ERR-91)
V3 = {
    'T-A': dict(
        frase="v3 T-A: muertes <= 1.10 x tronco (mediana) y r >= tronco - 10 (mediana) y NO INFERIORIDAD pareada de "
              "una cola al 95 % (z = 1.645) con margen 10 en r (LI > -10). SIN clausula A12.",
        muertes=1.10, r_delta=10.0, margen=10.0, z=1.645, n=40),
    'T-C_ii': dict(
        frase="v3 T-C (ii): NO INFERIORIDAD pareada de una cola al 95 % (z = 1.645) con margen 10 en rev (LI > -10). "
              "La exigencia de GANAR se traslada a T-G.",
        margen=10.0, z=1.645, n=40),
}

# ---------------------------------------------------------------- predicciones CAL-1..CAL-5 (PREREGISTRO_calibracion_v3.md §5)
CAL = {
    'CAL-1': dict(frase="el PLACEBO pasa T-A v3 (n = 40, margen 10) con probabilidad 0.90-0.98", lo=0.90, hi=0.98),
    'CAL-2': dict(frase="el PLACEBO pasa T-A v2 (n = 20, con A12 >= 0.50) con probabilidad 0.25-0.40", lo=0.25, hi=0.40),
    'CAL-3': dict(frase="v3 RECHAZA un candidato desplazado delta = -20 puntos de r: pasa <= 0.05", hi=0.05),
    'CAL-4': dict(frase="marginales PLACEBO vs tronco: A12 NO pareado en [0.40, 0.60] en las 6 comparaciones", lo=0.40, hi=0.60),
    'CAL-5': dict(frase="el PLACEBO pasa T-C (ii) v2 (A12 >= 0.75, n = 20) con probabilidad 0.01-0.05", lo=0.01, hi=0.05),
}

# ---------------------------------------------------------------- semillas (verificadas libres con grep el 21-sep 19:00)
SEMILLAS = dict(
    TCii=list(range(2121, 2161)),    # 40; la segunda mitad (2141-2160) es el rango que pidio el encargo
    TA=list(range(2161, 2201)),      # 40
    TCii_replica=list(range(2321, 2361)),
    TA_replica=list(range(2281, 2321)),
    ocupadas="2001-2080 dE5-v2 y v15f-v2; 2101-2120 BA-v tercera serie (21-sep); 2201-2280 RESERVADAS por el creador C para dE5-fam",
)

# ---------------------------------------------------------------- el brazo PEOR (control negativo con perilla YA del tronco)
PEOR = dict(
    frase="PEOR = el mismo organismo con COSTE DE VIDA mayor: costo = costo_a = 0.001 x m. `costo`/`costo_a` ya son "
          "argumentos del tronco (mini_vivo.CUERPO). m se fija UNA vez en el humo con la regla escrita en "
          "PREREGISTRO_calibracion_v3.md §6 y no se vuelve a tocar.",
    m_candidatos=(1.25, 1.50),
    # FIJADO POR LA REGLA de §6 en el humo del 21-sep 16:33 (datos/humo/critv3_humo_20260921_163338.json,
    # sha 3662dcc1b522473a): semilla 2161 brazo VIVO, delta_r(1.25) = -17 (no llega a -20), delta_r(1.50) = -73.
    # El brazo PEOR resulta MAS DURO que el delta = -20 pedido: CAL-3 se juzga con CAL-3a (desplazamiento exacto).
    # No se recalibra.
    m=1.50,
    costo_base=0.001,
)
