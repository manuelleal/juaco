# datos/humo.json — semillas [99], 5 tareas por familia y regimen, C=200
elementos por pantalla: 9–22

## Parte 1 — tareas completas (media de semillas; entre corchetes min–max)
| regimen | macro_pos | macro_etq | 1nn | 1nn_reciente | logistica | colonia | colonia_barajada | colonia_v2 |
|---|---|---|---|---|---|---|---|---|
| sin_cambio | 1.000 [1.00–1.00] | 1.000 [1.00–1.00] | 1.000 [1.00–1.00] | 1.000 [1.00–1.00] | 1.000 [1.00–1.00] | 1.000 [1.00–1.00] | 1.000 [1.00–1.00] | 1.000 [1.00–1.00] |
| reordenar | 0.000 [0.00–0.00] | 1.000 [1.00–1.00] | 0.533 [0.53–0.53] | 0.533 [0.53–0.53] | 1.000 [1.00–1.00] | 0.633 [0.63–0.63] | 0.800 [0.80–0.80] | 0.600 [0.60–0.60] |
| renombrar | 1.000 [1.00–1.00] | 0.000 [0.00–0.00] | 0.967 [0.97–0.97] | 0.967 [0.97–0.97] | 0.133 [0.13–0.13] | 0.233 [0.23–0.23] | 0.100 [0.10–0.10] | 0.967 [0.97–0.97] |
| distractores | 0.000 [0.00–0.00] | 0.733 [0.73–0.73] | 0.933 [0.93–0.93] | 0.933 [0.93–0.93] | 0.900 [0.90–0.90] | 0.733 [0.73–0.73] | 0.867 [0.87–0.87] | 0.933 [0.93–0.93] |
| cambia_y_vuelve | 1.000 [1.00–1.00] | 1.000 [1.00–1.00] | 0.167 [0.17–0.17] | 1.000 [1.00–1.00] | 1.000 [1.00–1.00] | 1.000 [1.00–1.00] | 1.000 [1.00–1.00] | 1.000 [1.00–1.00] |
| cambia_y_vuelve@0 | 0.000 [0.00–0.00] | 0.000 [0.00–0.00] | 0.167 [0.17–0.17] | 0.000 [0.00–0.00] | 1.000 [1.00–1.00] | 0.000 [0.00–0.00] | 0.000 [0.00–0.00] | 0.000 [0.00–0.00] |
| cambia_y_vuelve@2 | 1.000 [1.00–1.00] | 1.000 [1.00–1.00] | 0.167 [0.17–0.17] | 1.000 [1.00–1.00] | 1.000 [1.00–1.00] | 1.000 [1.00–1.00] | 1.000 [1.00–1.00] | 1.000 [1.00–1.00] |
| ment_inc | 0.333 [0.33–0.33] | 0.333 [0.33–0.33] | 0.167 [0.17–0.17] | 0.500 [0.50–0.50] | 1.000 [1.00–1.00] | 0.333 [0.33–0.33] | 0.167 [0.17–0.17] | 0.333 [0.33–0.33] |
| ment_con | 0.000 [0.00–0.00] | 0.000 [0.00–0.00] | 0.000 [0.00–0.00] | 0.000 [0.00–0.00] | 0.000 [0.00–0.00] | 0.000 [0.00–0.00] | 0.000 [0.00–0.00] | 0.000 [0.00–0.00] |

## Pareado por semilla: colonia frente a cada rival (gana/empata/pierde de 1; diferencia media)
| regimen | macro_pos | macro_etq | 1nn | 1nn_reciente | logistica | colonia_barajada | colonia_v2 |
|---|---|---|---|---|---|---|---|
| sin_cambio | 0/1/0 (+0.000) | 0/1/0 (+0.000) | 0/1/0 (+0.000) | 0/1/0 (+0.000) | 0/1/0 (+0.000) | 0/1/0 (+0.000) | 0/1/0 (+0.000) |
| reordenar | 1/0/0 (+0.633) | 0/0/1 (-0.367) | 1/0/0 (+0.100) | 1/0/0 (+0.100) | 0/0/1 (-0.367) | 0/0/1 (-0.167) | 1/0/0 (+0.033) |
| renombrar | 0/0/1 (-0.767) | 1/0/0 (+0.233) | 0/0/1 (-0.733) | 0/0/1 (-0.733) | 1/0/0 (+0.100) | 1/0/0 (+0.133) | 0/0/1 (-0.733) |
| distractores | 1/0/0 (+0.733) | 0/1/0 (+0.000) | 0/0/1 (-0.200) | 0/0/1 (-0.200) | 0/0/1 (-0.167) | 0/0/1 (-0.133) | 0/0/1 (-0.200) |
| cambia_y_vuelve | 0/1/0 (+0.000) | 0/1/0 (+0.000) | 1/0/0 (+0.833) | 0/1/0 (+0.000) | 0/1/0 (+0.000) | 0/1/0 (+0.000) | 0/1/0 (+0.000) |

Exploratorio (fuera del veredicto): colonia_v2 − 1nn por regimen: sin_cambio +0.000 (0/1/0); reordenar +0.067 (1/0/0); renombrar +0.000 (0/1/0); distractores +0.000 (0/1/0); cambia_y_vuelve +0.833 (1/0/0)

## Parte 2 — irreversibles (suma de las 1 semillas)
irr errados % = clics irreversibles equivocados ejecutados / propuestas de irreversible. abst % = abstenciones / propuestas de irreversible. pide % = (abstenciones + reversiones) / pasos. completas = sin ayuda.

**Conjunto primario (5 regimenes honestos + mentiroso inconsistente)**

| brazo | irr errados % | errados / propuestas | por 100 tareas | semillas con 0 errados | abst % | pide % | completas | completas o con ayuda |
|---|---|---|---|---|---|---|---|---|
| colonia | 5.49 | 5 / 91 | 2.78 | 0/1 | 0.0 | 0.0 | 0.656 | 0.656 |
| cuarentena | 0.00 | 0 / 102 | 0.00 | 1/1 | 24.5 | 4.0 | 0.667 | 0.828 |
| cuar_sin_efecto | 1.96 | 2 / 102 | 1.11 | 0/1 | 13.7 | 2.5 | 0.717 | 0.817 |
| cuar_sin_k | 0.00 | 0 / 102 | 0.00 | 1/1 | 14.7 | 2.6 | 0.722 | 0.828 |
| 1nn | 15.22 | 14 / 92 | 7.78 | 0/1 | 0.0 | 0.0 | 0.628 | 0.628 |
| 1nn_abst_irr | 11.96 | 11 / 92 | 6.11 | 0/1 | 25.0 | 3.4 | 0.517 | 0.644 |
| 1nn_abst_todo | 15.05 | 14 / 93 | 7.78 | 0/1 | 23.7 | 3.2 | 0.556 | 0.633 |

**Solo regimenes honestos (para el costo)**

| brazo | irr errados % | errados / propuestas | por 100 tareas | semillas con 0 errados | abst % | pide % | completas | completas o con ayuda |
|---|---|---|---|---|---|---|---|---|
| colonia | 6.17 | 5 / 81 | 3.33 | 0/1 | 0.0 | 0.0 | 0.720 | 0.720 |
| cuarentena | 0.00 | 0 / 92 | 0.00 | 1/1 | 27.2 | 4.2 | 0.733 | 0.913 |
| cuar_sin_efecto | 2.17 | 2 / 92 | 1.33 | 0/1 | 15.2 | 2.5 | 0.793 | 0.900 |
| cuar_sin_k | 0.00 | 0 / 92 | 0.00 | 1/1 | 16.3 | 2.6 | 0.800 | 0.913 |
| 1nn | 16.09 | 14 / 87 | 9.33 | 0/1 | 0.0 | 0.0 | 0.720 | 0.720 |
| 1nn_abst_irr | 12.64 | 11 / 87 | 7.33 | 0/1 | 26.4 | 3.7 | 0.587 | 0.740 |
| 1nn_abst_todo | 15.91 | 14 / 88 | 9.33 | 0/1 | 25.0 | 3.5 | 0.633 | 0.727 |

**sin_cambio**

| brazo | irr errados % | errados / propuestas | por 100 tareas | semillas con 0 errados | abst % | pide % | completas | completas o con ayuda |
|---|---|---|---|---|---|---|---|---|
| colonia | 0.00 | 0 / 20 | 0.00 | 1/1 | 0.0 | 0.0 | 1.000 | 1.000 |
| cuarentena | 0.00 | 0 / 20 | 0.00 | 1/1 | 0.0 | 0.0 | 1.000 | 1.000 |
| cuar_sin_efecto | 0.00 | 0 / 20 | 0.00 | 1/1 | 0.0 | 0.0 | 1.000 | 1.000 |
| cuar_sin_k | 0.00 | 0 / 20 | 0.00 | 1/1 | 0.0 | 0.0 | 1.000 | 1.000 |
| 1nn | 0.00 | 0 / 20 | 0.00 | 1/1 | 0.0 | 0.0 | 1.000 | 1.000 |
| 1nn_abst_irr | 0.00 | 0 / 20 | 0.00 | 1/1 | 0.0 | 0.0 | 1.000 | 1.000 |
| 1nn_abst_todo | 0.00 | 0 / 20 | 0.00 | 1/1 | 0.0 | 0.0 | 1.000 | 1.000 |

**reordenar**

| brazo | irr errados % | errados / propuestas | por 100 tareas | semillas con 0 errados | abst % | pide % | completas | completas o con ayuda |
|---|---|---|---|---|---|---|---|---|
| colonia | 0.00 | 0 / 13 | 0.00 | 1/1 | 0.0 | 0.0 | 0.633 | 0.633 |
| cuarentena | 0.00 | 0 / 14 | 0.00 | 1/1 | 35.7 | 6.1 | 0.467 | 0.700 |
| cuar_sin_efecto | 14.29 | 2 / 14 | 6.67 | 0/1 | 21.4 | 4.4 | 0.467 | 0.633 |
| cuar_sin_k | 0.00 | 0 / 14 | 0.00 | 1/1 | 35.7 | 6.1 | 0.467 | 0.700 |
| 1nn | 28.57 | 4 / 14 | 13.33 | 0/1 | 0.0 | 0.0 | 0.533 | 0.533 |
| 1nn_abst_irr | 7.14 | 1 / 14 | 3.33 | 0/1 | 71.4 | 8.3 | 0.300 | 0.633 |
| 1nn_abst_todo | 28.57 | 4 / 14 | 13.33 | 0/1 | 0.0 | 0.0 | 0.533 | 0.533 |

**renombrar**

| brazo | irr errados % | errados / propuestas | por 100 tareas | semillas con 0 errados | abst % | pide % | completas | completas o con ayuda |
|---|---|---|---|---|---|---|---|---|
| colonia | 41.67 | 5 / 12 | 16.67 | 0/1 | 0.0 | 0.0 | 0.233 | 0.233 |
| cuarentena | 0.00 | 0 / 19 | 0.00 | 1/1 | 47.4 | 6.9 | 0.633 | 0.933 |
| cuar_sin_efecto | 0.00 | 0 / 19 | 0.00 | 1/1 | 0.0 | 0.0 | 0.933 | 0.933 |
| cuar_sin_k | 0.00 | 0 / 19 | 0.00 | 1/1 | 47.4 | 6.9 | 0.633 | 0.933 |
| 1nn | 0.00 | 0 / 19 | 0.00 | 1/1 | 0.0 | 0.0 | 0.967 | 0.967 |
| 1nn_abst_irr | 0.00 | 0 / 19 | 0.00 | 1/1 | 36.8 | 5.3 | 0.733 | 0.967 |
| 1nn_abst_todo | 0.00 | 0 / 20 | 0.00 | 1/1 | 110.0 | 16.3 | 0.533 | 1.000 |

**distractores**

| brazo | irr errados % | errados / propuestas | por 100 tareas | semillas con 0 errados | abst % | pide % | completas | completas o con ayuda |
|---|---|---|---|---|---|---|---|---|
| colonia | 0.00 | 0 / 16 | 0.00 | 1/1 | 0.0 | 0.0 | 0.733 | 0.733 |
| cuarentena | 0.00 | 0 / 19 | 0.00 | 1/1 | 5.3 | 0.8 | 0.900 | 0.933 |
| cuar_sin_efecto | 0.00 | 0 / 19 | 0.00 | 1/1 | 5.3 | 0.8 | 0.900 | 0.933 |
| cuar_sin_k | 0.00 | 0 / 19 | 0.00 | 1/1 | 5.3 | 0.8 | 0.900 | 0.933 |
| 1nn | 0.00 | 0 / 19 | 0.00 | 1/1 | 0.0 | 0.0 | 0.933 | 0.933 |
| 1nn_abst_irr | 0.00 | 0 / 19 | 0.00 | 1/1 | 31.6 | 4.6 | 0.733 | 0.933 |
| 1nn_abst_todo | 0.00 | 0 / 19 | 0.00 | 1/1 | 0.0 | 0.0 | 0.933 | 0.933 |

**cambia_y_vuelve**

| brazo | irr errados % | errados / propuestas | por 100 tareas | semillas con 0 errados | abst % | pide % | completas | completas o con ayuda |
|---|---|---|---|---|---|---|---|---|
| colonia | 0.00 | 0 / 20 | 0.00 | 1/1 | 0.0 | 0.0 | 1.000 | 1.000 |
| cuarentena | 0.00 | 0 / 20 | 0.00 | 1/1 | 50.0 | 7.4 | 0.667 | 1.000 |
| cuar_sin_efecto | 0.00 | 0 / 20 | 0.00 | 1/1 | 50.0 | 7.4 | 0.667 | 1.000 |
| cuar_sin_k | 0.00 | 0 / 20 | 0.00 | 1/1 | 0.0 | 0.0 | 1.000 | 1.000 |
| 1nn | 66.67 | 10 / 15 | 33.33 | 0/1 | 0.0 | 0.0 | 0.167 | 0.167 |
| 1nn_abst_irr | 66.67 | 10 / 15 | 33.33 | 0/1 | 0.0 | 0.0 | 0.167 | 0.167 |
| 1nn_abst_todo | 66.67 | 10 / 15 | 33.33 | 0/1 | 0.0 | 0.0 | 0.167 | 0.167 |

**ment_inc**

| brazo | irr errados % | errados / propuestas | por 100 tareas | semillas con 0 errados | abst % | pide % | completas | completas o con ayuda |
|---|---|---|---|---|---|---|---|---|
| colonia | 0.00 | 0 / 10 | 0.00 | 1/1 | 0.0 | 0.0 | 0.333 | 0.333 |
| cuarentena | 0.00 | 0 / 10 | 0.00 | 1/1 | 0.0 | 2.2 | 0.333 | 0.400 |
| cuar_sin_efecto | 0.00 | 0 / 10 | 0.00 | 1/1 | 0.0 | 2.2 | 0.333 | 0.400 |
| cuar_sin_k | 0.00 | 0 / 10 | 0.00 | 1/1 | 0.0 | 2.2 | 0.333 | 0.400 |
| 1nn | 0.00 | 0 / 5 | 0.00 | 1/1 | 0.0 | 0.0 | 0.167 | 0.167 |
| 1nn_abst_irr | 0.00 | 0 / 5 | 0.00 | 1/1 | 0.0 | 0.0 | 0.167 | 0.167 |
| 1nn_abst_todo | 0.00 | 0 / 5 | 0.00 | 1/1 | 0.0 | 0.0 | 0.167 | 0.167 |

**ment_con**

| brazo | irr errados % | errados / propuestas | por 100 tareas | semillas con 0 errados | abst % | pide % | completas | completas o con ayuda |
|---|---|---|---|---|---|---|---|---|
| colonia | 100.00 | 30 / 30 | 100.00 | 0/1 | 0.0 | 0.0 | 0.000 | 0.000 |
| cuarentena | 100.00 | 30 / 30 | 100.00 | 0/1 | 0.0 | 0.0 | 0.000 | 0.000 |
| cuar_sin_efecto | 100.00 | 30 / 30 | 100.00 | 0/1 | 0.0 | 0.0 | 0.000 | 0.000 |
| cuar_sin_k | 100.00 | 30 / 30 | 100.00 | 0/1 | 0.0 | 0.0 | 0.000 | 0.000 |
| 1nn | 100.00 | 30 / 30 | 100.00 | 0/1 | 0.0 | 0.0 | 0.000 | 0.000 |
| 1nn_abst_irr | 100.00 | 30 / 30 | 100.00 | 0/1 | 0.0 | 0.0 | 0.000 | 0.000 |
| 1nn_abst_todo | 100.00 | 30 / 30 | 100.00 | 0/1 | 0.0 | 0.0 | 0.000 | 0.000 |

## Microsegundos por clic (decision; media de semillas) y memoria al final de la fase A
| brazo | us/clic | memoria |
|---|---|---|
| macro_pos | 0 | 27 |
| macro_etq | 1 | 27 |
| 1nn | 77 | 135 |
| 1nn_reciente | 81 | 135 |
| logistica | 939 | 135 |
| colonia | 46 | 15 |
| colonia_barajada | 48 | 14 |
| colonia_v2 | 50 | 26 |
| cuarentena | 61 | 48 |
- honesto_A colonia: nac 15.0, mue 0.0, estrechadas 1.0, N 15.0
- honesto_A colonia_barajada: nac 14.0, mue 0.0, estrechadas 0.0, N 14.0
- honesto_A cuarentena: nac 37.0, mue 10.0, estrechadas 1.0, N 27.0, validadas 27.0, hipotesis 0.0, reversiones 0.0, cel_efecto 21.0
- honesto_fin colonia: nac 32.0, mue 5.0, estrechadas 2.0, N 27.0
- honesto_fin colonia_barajada: nac 38.0, mue 0.0, estrechadas 10.0, N 38.0
- honesto_fin cuarentena: nac 55.0, mue 28.0, estrechadas 3.0, N 27.0, validadas 23.0, hipotesis 4.0, reversiones 10.0, cel_efecto 22.0
- ment_inc colonia: nac 88.0, mue 61.0, estrechadas 4.0, N 27.0
- ment_inc colonia_barajada: nac 90.0, mue 52.0, estrechadas 16.0, N 38.0
- ment_inc cuarentena: nac 90.0, mue 62.0, estrechadas 11.0, N 28.0, validadas 11.0, hipotesis 17.0, reversiones 2.0, cel_efecto 31.0
- ment_con colonia: nac 25.0, mue 0.0, estrechadas 1.0, N 25.0
- ment_con colonia_barajada: nac 30.0, mue 2.0, estrechadas 5.0, N 28.0
- ment_con cuarentena: nac 32.0, mue 5.0, estrechadas 3.0, N 27.0, validadas 27.0, hipotesis 0.0, reversiones 0.0, cel_efecto 19.0

## Predicciones
- P1 reordenar: colonia 0.633 (≥0.80), macro_pos 0.000 (≤0.30): REFUTADA
- P2 distractores: colonia 0.733 (≥0.80), macro_pos 0.000 (≤0.30): REFUTADA
- P3 renombrar: colonia 0.233 (≥0.60), macro_etq 0.000 (≤0.20): REFUTADA
- P4 macro_etq en reordenar 1.000 (≥0.95): CUMPLIDA
- P5 cambia_y_vuelve: colonia − 1nn por semilla [0.833]; ≥0.15 en 1/1: REFUTADA
- P6 irreversibles errados: cuarentena 0.00 % (≤1), colonia sin cuarentena 5.49 % (≥8): REFUTADA (cuarentena ≤1: CUMPLIDA; colonia ≥8: REFUTADA)
- P7 costo: -1.3 puntos (≤15): CUMPLIDA
- P8 mentiroso consistente atraviesa: cuarentena 100.0 % errados (≥50): CUMPLIDA
- Control barajada: colonia − barajada por semilla [np.float64(-0.033)]; por delante en 0/1: REFUTADA

## Criterio de cierre
- renombrar: colonia − 1nn -0.733, por delante en 0/1 → el 1-NN empata o gana
- cambia_y_vuelve: P5 → el 1-NN empata o gana
  - candado: colonia − 1nn_reciente +0.000, por delante en 0/1 → 1nn_reciente EMPATA o gana
- irreversibles: cuarentena 0.00 % frente al mejor 1nn_abst 11.96 % → GANA la cuarentena

**VEREDICTO MECANICO: HAY ALGO MODESTO** (victorias de la colonia: 1/3)