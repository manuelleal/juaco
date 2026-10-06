# datos/principal.json — semillas [11, 12, 13, 14, 15], 20 tareas por familia y regimen, C=200
elementos por pantalla: 8–24

## Parte 1 — tareas completas (media de semillas; entre corchetes min–max)
| regimen | macro_pos | macro_etq | 1nn | 1nn_reciente | logistica | colonia | colonia_barajada | colonia_v2 |
|---|---|---|---|---|---|---|---|---|
| sin_cambio | 1.000 [1.00–1.00] | 1.000 [1.00–1.00] | 1.000 [1.00–1.00] | 1.000 [1.00–1.00] | 1.000 [1.00–1.00] | 1.000 [1.00–1.00] | 0.967 [0.83–1.00] | 1.000 [1.00–1.00] |
| reordenar | 0.003 [0.00–0.01] | 1.000 [1.00–1.00] | 0.375 [0.28–0.47] | 0.375 [0.28–0.47] | 1.000 [1.00–1.00] | 0.632 [0.51–0.76] | 0.860 [0.68–0.96] | 0.423 [0.28–0.51] |
| renombrar | 1.000 [1.00–1.00] | 0.000 [0.00–0.00] | 0.902 [0.82–0.96] | 0.902 [0.82–0.96] | 0.113 [0.09–0.13] | 0.255 [0.15–0.45] | 0.102 [0.02–0.18] | 0.887 [0.82–0.93] |
| distractores | 0.013 [0.01–0.03] | 0.710 [0.69–0.74] | 0.872 [0.79–0.91] | 0.873 [0.80–0.91] | 0.872 [0.82–0.91] | 0.758 [0.69–0.87] | 0.838 [0.74–0.93] | 0.880 [0.80–0.93] |
| cambia_y_vuelve | 1.000 [1.00–1.00] | 1.000 [1.00–1.00] | 0.433 [0.17–0.67] | 1.000 [1.00–1.00] | 1.000 [1.00–1.00] | 1.000 [1.00–1.00] | 0.800 [0.67–1.00] | 1.000 [1.00–1.00] |
| cambia_y_vuelve@0 | 0.000 [0.00–0.00] | 0.000 [0.00–0.00] | 0.433 [0.17–0.67] | 0.000 [0.00–0.00] | 1.000 [1.00–1.00] | 0.000 [0.00–0.00] | 0.000 [0.00–0.00] | 0.000 [0.00–0.00] |
| cambia_y_vuelve@2 | 1.000 [1.00–1.00] | 1.000 [1.00–1.00] | 0.433 [0.17–0.67] | 1.000 [1.00–1.00] | 1.000 [1.00–1.00] | 1.000 [1.00–1.00] | 0.900 [0.83–1.00] | 1.000 [1.00–1.00] |
| ment_inc | 0.133 [0.00–0.17] | 0.133 [0.00–0.17] | 0.000 [0.00–0.00] | 0.133 [0.00–0.17] | 0.878 [0.82–1.00] | 0.133 [0.00–0.17] | 0.000 [0.00–0.00] | 0.133 [0.00–0.17] |
| ment_con | 0.000 [0.00–0.00] | 0.000 [0.00–0.00] | 0.000 [0.00–0.00] | 0.000 [0.00–0.00] | 0.000 [0.00–0.00] | 0.000 [0.00–0.00] | 0.000 [0.00–0.00] | 0.000 [0.00–0.00] |

## Pareado por semilla: colonia frente a cada rival (gana/empata/pierde de 5; diferencia media)
| regimen | macro_pos | macro_etq | 1nn | 1nn_reciente | logistica | colonia_barajada | colonia_v2 |
|---|---|---|---|---|---|---|---|
| sin_cambio | 0/5/0 (+0.000) | 0/5/0 (+0.000) | 0/5/0 (+0.000) | 0/5/0 (+0.000) | 0/5/0 (+0.000) | 1/4/0 (+0.033) | 0/5/0 (+0.000) |
| reordenar | 5/0/0 (+0.628) | 0/0/5 (-0.368) | 5/0/0 (+0.257) | 5/0/0 (+0.257) | 0/0/5 (-0.368) | 0/0/5 (-0.228) | 5/0/0 (+0.208) |
| renombrar | 0/0/5 (-0.745) | 5/0/0 (+0.255) | 0/0/5 (-0.647) | 0/0/5 (-0.647) | 5/0/0 (+0.142) | 5/0/0 (+0.153) | 0/0/5 (-0.632) |
| distractores | 5/0/0 (+0.745) | 4/0/1 (+0.048) | 0/0/5 (-0.113) | 0/0/5 (-0.115) | 0/0/5 (-0.113) | 1/0/4 (-0.080) | 0/0/5 (-0.122) |
| cambia_y_vuelve | 0/5/0 (+0.000) | 0/5/0 (+0.000) | 5/0/0 (+0.567) | 0/5/0 (+0.000) | 0/5/0 (+0.000) | 3/2/0 (+0.200) | 0/5/0 (+0.000) |

Exploratorio (fuera del veredicto): colonia_v2 − 1nn por regimen: sin_cambio +0.000 (0/5/0); reordenar +0.048 (4/1/0); renombrar -0.015 (0/3/2); distractores +0.008 (3/2/0); cambia_y_vuelve +0.567 (5/0/0)

## Parte 2 — irreversibles (suma de las 5 semillas)
irr errados % = clics irreversibles equivocados ejecutados / propuestas de irreversible. abst % = abstenciones / propuestas de irreversible. pide % = (abstenciones + reversiones) / pasos. completas = sin ayuda.

**Conjunto primario (5 regimenes honestos + mentiroso inconsistente)**

| brazo | irr errados % | errados / propuestas | por 100 tareas | semillas con 0 errados | abst % | pide % | completas | completas o con ayuda |
|---|---|---|---|---|---|---|---|---|
| colonia | 14.88 | 270 / 1814 | 7.50 | 0/5 | 0.0 | 0.0 | 0.630 | 0.630 |
| colonia_v2 | 9.64 | 189 / 1960 | 5.25 | 0/5 | 0.0 | 0.0 | 0.721 | 0.721 |
| cuarentena | 0.00 | 0 / 2071 | 0.00 | 5/5 | 35.0 | 5.7 | 0.602 | 0.792 |
| cuar_sin_efecto | 1.93 | 40 / 2071 | 1.11 | 0/5 | 25.8 | 4.4 | 0.644 | 0.781 |
| cuar_sin_k | 7.10 | 140 / 1971 | 3.89 | 1/5 | 13.4 | 2.5 | 0.663 | 0.759 |
| 1nn | 13.53 | 230 / 1700 | 6.39 | 0/5 | 0.0 | 0.0 | 0.597 | 0.597 |
| 1nn_abst_irr | 10.82 | 184 / 1700 | 5.11 | 0/5 | 33.6 | 4.3 | 0.451 | 0.610 |
| 1nn_abst_todo | 13.31 | 229 / 1721 | 6.36 | 0/5 | 42.2 | 5.5 | 0.479 | 0.606 |
| 1nn_reciente | 9.79 | 190 / 1941 | 5.28 | 0/5 | 0.0 | 0.0 | 0.714 | 0.714 |
| 1nn_rec_abst_irr | 7.26 | 141 / 1941 | 3.92 | 0/5 | 31.6 | 4.4 | 0.557 | 0.728 |

**Solo regimenes honestos (para el costo)**

| brazo | irr errados % | errados / propuestas | por 100 tareas | semillas con 0 errados | abst % | pide % | completas | completas o con ayuda |
|---|---|---|---|---|---|---|---|---|
| colonia | 7.87 | 125 / 1589 | 4.17 | 0/5 | 0.0 | 0.0 | 0.729 | 0.729 |
| colonia_v2 | 2.54 | 44 / 1735 | 1.47 | 0/5 | 0.0 | 0.0 | 0.838 | 0.838 |
| cuarentena | 0.00 | 0 / 1741 | 0.00 | 5/5 | 23.8 | 4.0 | 0.716 | 0.884 |
| cuar_sin_efecto | 2.30 | 40 / 1741 | 1.33 | 0/5 | 12.9 | 2.5 | 0.766 | 0.871 |
| cuar_sin_k | 0.00 | 0 / 1741 | 0.00 | 5/5 | 14.6 | 2.7 | 0.769 | 0.884 |
| 1nn | 6.96 | 110 / 1580 | 3.67 | 0/5 | 0.0 | 0.0 | 0.716 | 0.716 |
| 1nn_abst_irr | 4.05 | 64 / 1580 | 2.13 | 1/5 | 36.1 | 4.6 | 0.541 | 0.732 |
| 1nn_abst_todo | 6.81 | 109 / 1601 | 3.63 | 0/5 | 45.3 | 5.9 | 0.575 | 0.727 |
| 1nn_reciente | 2.91 | 50 / 1721 | 1.67 | 0/5 | 0.0 | 0.0 | 0.830 | 0.830 |
| 1nn_rec_abst_irr | 0.06 | 1 / 1721 | 0.03 | 4/5 | 35.6 | 4.8 | 0.642 | 0.846 |

**sin_cambio**

| brazo | irr errados % | errados / propuestas | por 100 tareas | semillas con 0 errados | abst % | pide % | completas | completas o con ayuda |
|---|---|---|---|---|---|---|---|---|
| colonia | 0.00 | 0 / 400 | 0.00 | 5/5 | 0.0 | 0.0 | 1.000 | 1.000 |
| colonia_v2 | 0.00 | 0 / 400 | 0.00 | 5/5 | 0.0 | 0.0 | 1.000 | 1.000 |
| cuarentena | 0.00 | 0 / 400 | 0.00 | 5/5 | 0.0 | 0.0 | 1.000 | 1.000 |
| cuar_sin_efecto | 0.00 | 0 / 400 | 0.00 | 5/5 | 0.0 | 0.0 | 1.000 | 1.000 |
| cuar_sin_k | 0.00 | 0 / 400 | 0.00 | 5/5 | 0.0 | 0.0 | 1.000 | 1.000 |
| 1nn | 0.00 | 0 / 400 | 0.00 | 5/5 | 0.0 | 0.0 | 1.000 | 1.000 |
| 1nn_abst_irr | 0.00 | 0 / 400 | 0.00 | 5/5 | 0.0 | 0.0 | 1.000 | 1.000 |
| 1nn_abst_todo | 0.00 | 0 / 400 | 0.00 | 5/5 | 0.0 | 0.0 | 1.000 | 1.000 |
| 1nn_reciente | 0.00 | 0 / 400 | 0.00 | 5/5 | 0.0 | 0.0 | 1.000 | 1.000 |
| 1nn_rec_abst_irr | 0.00 | 0 / 400 | 0.00 | 5/5 | 0.0 | 0.0 | 1.000 | 1.000 |

**reordenar**

| brazo | irr errados % | errados / propuestas | por 100 tareas | semillas con 0 errados | abst % | pide % | completas | completas o con ayuda |
|---|---|---|---|---|---|---|---|---|
| colonia | 13.88 | 39 / 281 | 6.50 | 0/5 | 0.0 | 0.0 | 0.632 | 0.632 |
| colonia_v2 | 17.54 | 40 / 228 | 6.67 | 0/5 | 0.0 | 0.0 | 0.423 | 0.423 |
| cuarentena | 0.00 | 0 / 214 | 0.00 | 5/5 | 24.3 | 5.4 | 0.378 | 0.568 |
| cuar_sin_efecto | 17.29 | 37 / 214 | 6.17 | 0/5 | 7.0 | 3.7 | 0.378 | 0.507 |
| cuar_sin_k | 0.00 | 0 / 214 | 0.00 | 5/5 | 24.3 | 5.4 | 0.378 | 0.568 |
| 1nn | 21.95 | 45 / 205 | 7.50 | 0/5 | 0.0 | 0.0 | 0.375 | 0.375 |
| 1nn_abst_irr | 1.95 | 4 / 205 | 0.67 | 4/5 | 69.8 | 6.8 | 0.205 | 0.443 |
| 1nn_abst_todo | 21.95 | 45 / 205 | 7.50 | 0/5 | 68.8 | 6.7 | 0.255 | 0.380 |
| 1nn_reciente | 21.95 | 45 / 205 | 7.50 | 0/5 | 0.0 | 0.0 | 0.375 | 0.375 |
| 1nn_rec_abst_irr | 0.49 | 1 / 205 | 0.17 | 4/5 | 73.2 | 7.1 | 0.198 | 0.448 |

**renombrar**

| brazo | irr errados % | errados / propuestas | por 100 tareas | semillas con 0 errados | abst % | pide % | completas | completas o con ayuda |
|---|---|---|---|---|---|---|---|---|
| colonia | 37.63 | 70 / 186 | 11.67 | 1/5 | 0.0 | 0.0 | 0.255 | 0.255 |
| colonia_v2 | 0.00 | 0 / 349 | 0.00 | 5/5 | 0.0 | 0.0 | 0.887 | 0.887 |
| cuarentena | 0.00 | 0 / 368 | 0.00 | 5/5 | 49.7 | 7.3 | 0.613 | 0.932 |
| cuar_sin_efecto | 0.00 | 0 / 368 | 0.00 | 5/5 | 9.0 | 1.6 | 0.863 | 0.932 |
| cuar_sin_k | 0.00 | 0 / 368 | 0.00 | 5/5 | 49.7 | 7.3 | 0.613 | 0.932 |
| 1nn | 0.28 | 1 / 359 | 0.17 | 4/5 | 0.0 | 0.0 | 0.902 | 0.902 |
| 1nn_abst_irr | 0.00 | 0 / 359 | 0.00 | 5/5 | 75.8 | 10.4 | 0.450 | 0.903 |
| 1nn_abst_todo | 0.00 | 0 / 376 | 0.00 | 5/5 | 126.3 | 17.9 | 0.453 | 0.940 |
| 1nn_reciente | 0.28 | 1 / 359 | 0.17 | 4/5 | 0.0 | 0.0 | 0.902 | 0.902 |
| 1nn_rec_abst_irr | 0.00 | 0 / 359 | 0.00 | 5/5 | 85.0 | 11.6 | 0.395 | 0.903 |

**distractores**

| brazo | irr errados % | errados / propuestas | por 100 tareas | semillas con 0 errados | abst % | pide % | completas | completas o con ayuda |
|---|---|---|---|---|---|---|---|---|
| colonia | 4.97 | 16 / 322 | 2.67 | 2/5 | 0.0 | 0.0 | 0.758 | 0.758 |
| colonia_v2 | 1.12 | 4 / 358 | 0.67 | 2/5 | 0.0 | 0.0 | 0.880 | 0.880 |
| cuarentena | 0.00 | 0 / 359 | 0.00 | 5/5 | 5.3 | 1.6 | 0.853 | 0.922 |
| cuar_sin_efecto | 0.84 | 3 / 359 | 0.50 | 3/5 | 4.5 | 1.5 | 0.853 | 0.917 |
| cuar_sin_k | 0.00 | 0 / 359 | 0.00 | 5/5 | 5.3 | 1.6 | 0.853 | 0.922 |
| 1nn | 1.12 | 4 / 356 | 0.67 | 2/5 | 0.0 | 0.0 | 0.872 | 0.872 |
| 1nn_abst_irr | 0.00 | 0 / 356 | 0.00 | 5/5 | 43.8 | 6.1 | 0.618 | 0.878 |
| 1nn_abst_todo | 1.11 | 4 / 360 | 0.67 | 2/5 | 30.6 | 4.3 | 0.732 | 0.883 |
| 1nn_reciente | 1.12 | 4 / 357 | 0.67 | 2/5 | 0.0 | 0.0 | 0.873 | 0.873 |
| 1nn_rec_abst_irr | 0.00 | 0 / 357 | 0.00 | 5/5 | 44.3 | 6.1 | 0.617 | 0.880 |

**cambia_y_vuelve**

| brazo | irr errados % | errados / propuestas | por 100 tareas | semillas con 0 errados | abst % | pide % | completas | completas o con ayuda |
|---|---|---|---|---|---|---|---|---|
| colonia | 0.00 | 0 / 400 | 0.00 | 5/5 | 0.0 | 0.0 | 1.000 | 1.000 |
| colonia_v2 | 0.00 | 0 / 400 | 0.00 | 5/5 | 0.0 | 0.0 | 1.000 | 1.000 |
| cuarentena | 0.00 | 0 / 400 | 0.00 | 5/5 | 40.0 | 5.9 | 0.733 | 1.000 |
| cuar_sin_efecto | 0.00 | 0 / 400 | 0.00 | 5/5 | 40.0 | 5.9 | 0.733 | 1.000 |
| cuar_sin_k | 0.00 | 0 / 400 | 0.00 | 5/5 | 0.0 | 0.0 | 1.000 | 1.000 |
| 1nn | 23.08 | 60 / 260 | 10.00 | 2/5 | 0.0 | 0.0 | 0.433 | 0.433 |
| 1nn_abst_irr | 23.08 | 60 / 260 | 10.00 | 2/5 | 0.0 | 0.0 | 0.433 | 0.433 |
| 1nn_abst_todo | 23.08 | 60 / 260 | 10.00 | 2/5 | 0.0 | 0.0 | 0.433 | 0.433 |
| 1nn_reciente | 0.00 | 0 / 400 | 0.00 | 5/5 | 0.0 | 0.0 | 1.000 | 1.000 |
| 1nn_rec_abst_irr | 0.00 | 0 / 400 | 0.00 | 5/5 | 0.0 | 0.0 | 1.000 | 1.000 |

**ment_inc**

| brazo | irr errados % | errados / propuestas | por 100 tareas | semillas con 0 errados | abst % | pide % | completas | completas o con ayuda |
|---|---|---|---|---|---|---|---|---|
| colonia | 64.44 | 145 / 225 | 24.17 | 1/5 | 0.0 | 0.0 | 0.133 | 0.133 |
| colonia_v2 | 64.44 | 145 / 225 | 24.17 | 1/5 | 0.0 | 0.0 | 0.133 | 0.133 |
| cuarentena | 0.00 | 0 / 330 | 0.00 | 5/5 | 93.9 | 18.3 | 0.033 | 0.333 |
| cuar_sin_efecto | 0.00 | 0 / 330 | 0.00 | 5/5 | 93.9 | 18.3 | 0.033 | 0.333 |
| cuar_sin_k | 60.87 | 140 / 230 | 23.33 | 1/5 | 4.3 | 0.7 | 0.133 | 0.133 |
| 1nn | 100.00 | 120 / 120 | 20.00 | 1/5 | 0.0 | 0.0 | 0.000 | 0.000 |
| 1nn_abst_irr | 100.00 | 120 / 120 | 20.00 | 1/5 | 0.0 | 0.0 | 0.000 | 0.000 |
| 1nn_abst_todo | 100.00 | 120 / 120 | 20.00 | 1/5 | 0.0 | 0.0 | 0.000 | 0.000 |
| 1nn_reciente | 63.64 | 140 / 220 | 23.33 | 1/5 | 0.0 | 0.0 | 0.133 | 0.133 |
| 1nn_rec_abst_irr | 63.64 | 140 / 220 | 23.33 | 1/5 | 0.0 | 0.0 | 0.133 | 0.133 |

**ment_con**

| brazo | irr errados % | errados / propuestas | por 100 tareas | semillas con 0 errados | abst % | pide % | completas | completas o con ayuda |
|---|---|---|---|---|---|---|---|---|
| colonia | 100.00 | 600 / 600 | 100.00 | 0/5 | 0.0 | 0.0 | 0.000 | 0.000 |
| colonia_v2 | 100.00 | 600 / 600 | 100.00 | 0/5 | 0.0 | 0.0 | 0.000 | 0.000 |
| cuarentena | 83.33 | 500 / 600 | 83.33 | 0/5 | 16.7 | 3.7 | 0.000 | 0.167 |
| cuar_sin_efecto | 83.33 | 500 / 600 | 83.33 | 0/5 | 16.7 | 3.7 | 0.000 | 0.167 |
| cuar_sin_k | 100.00 | 600 / 600 | 100.00 | 0/5 | 0.0 | 0.0 | 0.000 | 0.000 |
| 1nn | 100.00 | 600 / 600 | 100.00 | 0/5 | 0.0 | 0.0 | 0.000 | 0.000 |
| 1nn_abst_irr | 100.00 | 600 / 600 | 100.00 | 0/5 | 0.0 | 0.0 | 0.000 | 0.000 |
| 1nn_abst_todo | 100.00 | 600 / 600 | 100.00 | 0/5 | 0.0 | 0.0 | 0.000 | 0.000 |
| 1nn_reciente | 100.00 | 600 / 600 | 100.00 | 0/5 | 0.0 | 0.0 | 0.000 | 0.000 |
| 1nn_rec_abst_irr | 100.00 | 600 / 600 | 100.00 | 0/5 | 0.0 | 0.0 | 0.000 | 0.000 |

**POST HOC (D1): solo desplazamiento (reordenar + renombrar + distractores), umbral del 1-NN calibrado ahi mismo**

| brazo | irr errados % | errados / propuestas | por 100 tareas | semillas con 0 errados | abst % | pide % | completas | completas o con ayuda |
|---|---|---|---|---|---|---|---|---|
| colonia | 15.84 | 125 / 789 | 6.94 | 0/5 | 0.0 | 0.0 | 0.548 | 0.548 |
| colonia_v2 | 4.71 | 44 / 935 | 2.44 | 0/5 | 0.0 | 0.0 | 0.730 | 0.730 |
| cuarentena | 0.00 | 0 / 941 | 0.00 | 5/5 | 27.0 | 4.8 | 0.615 | 0.807 |
| cuar_sin_efecto | 4.25 | 40 / 941 | 2.22 | 0/5 | 6.8 | 2.1 | 0.698 | 0.785 |
| cuar_sin_k | 0.00 | 0 / 941 | 0.00 | 5/5 | 27.0 | 4.8 | 0.615 | 0.807 |
| 1nn | 5.43 | 50 / 920 | 2.78 | 0/5 | 0.0 | 0.0 | 0.716 | 0.716 |
| 1nn_abst_irr | 3.70 | 34 / 920 | 1.89 | 0/5 | 27.1 | 3.4 | 0.587 | 0.725 |
| 1nn_abst_todo | 5.23 | 49 / 937 | 2.72 | 0/5 | 36.2 | 4.6 | 0.597 | 0.728 |
| 1nn_reciente | 5.43 | 50 / 921 | 2.78 | 0/5 | 0.0 | 0.0 | 0.717 | 0.717 |
| 1nn_rec_abst_irr | 3.69 | 34 / 921 | 1.89 | 0/5 | 27.0 | 3.4 | 0.587 | 0.726 |

**POST HOC (D1): primario SIN mentiroso inconsistente, umbral calibrado ahi mismo**

| brazo | irr errados % | errados / propuestas | por 100 tareas | semillas con 0 errados | abst % | pide % | completas | completas o con ayuda |
|---|---|---|---|---|---|---|---|---|
| colonia | 7.87 | 125 / 1589 | 4.17 | 0/5 | 0.0 | 0.0 | 0.729 | 0.729 |
| colonia_v2 | 2.54 | 44 / 1735 | 1.47 | 0/5 | 0.0 | 0.0 | 0.838 | 0.838 |
| cuarentena | 0.00 | 0 / 1741 | 0.00 | 5/5 | 23.8 | 4.0 | 0.716 | 0.884 |
| cuar_sin_efecto | 2.30 | 40 / 1741 | 1.33 | 0/5 | 12.9 | 2.5 | 0.766 | 0.871 |
| cuar_sin_k | 0.00 | 0 / 1741 | 0.00 | 5/5 | 14.6 | 2.7 | 0.769 | 0.884 |
| 1nn | 6.96 | 110 / 1580 | 3.67 | 0/5 | 0.0 | 0.0 | 0.716 | 0.716 |
| 1nn_abst_irr | 5.19 | 82 / 1580 | 2.73 | 1/5 | 24.2 | 3.1 | 0.598 | 0.726 |
| 1nn_abst_todo | 6.83 | 109 / 1597 | 3.63 | 0/5 | 24.8 | 3.2 | 0.633 | 0.724 |
| 1nn_reciente | 2.91 | 50 / 1721 | 1.67 | 0/5 | 0.0 | 0.0 | 0.830 | 0.830 |
| 1nn_rec_abst_irr | 0.35 | 6 / 1721 | 0.20 | 2/5 | 24.0 | 3.3 | 0.707 | 0.845 |

## Microsegundos por clic (decision; media de semillas) y memoria al final de la fase A
| brazo | us/clic | memoria |
|---|---|---|
| macro_pos | 0 | 27 |
| macro_etq | 1 | 27 |
| 1nn | 76 | 135 |
| 1nn_reciente | 83 | 135 |
| logistica | 256 | 135 |
| colonia | 49 | 13 |
| colonia_barajada | 51 | 12 |
| colonia_v2 | 49 | 26 |
| cuarentena | 62 | 48 |
- honesto_A colonia: nac 13.0, mue 0.0, estrechadas 0.0, N 13.0
- honesto_A colonia_barajada: nac 12.4, mue 0.0, estrechadas 0.0, N 12.4
- honesto_A cuarentena: nac 31.4, mue 4.6, estrechadas 0.6, N 26.8, validadas 26.8, hipotesis 0.0, reversiones 0.0, cel_efecto 21.0
- honesto_fin colonia: nac 33.6, mue 9.0, estrechadas 0.6, N 24.6
- honesto_fin colonia_barajada: nac 46.8, mue 7.0, estrechadas 20.8, N 39.8
- honesto_fin cuarentena: nac 45.2, mue 18.4, estrechadas 1.8, N 26.8, validadas 21.4, hipotesis 5.4, reversiones 12.0, cel_efecto 22.6
- ment_inc colonia: nac 93.0, mue 64.0, estrechadas 5.0, N 29.0
- ment_inc colonia_barajada: nac 94.8, mue 54.2, estrechadas 19.6, N 40.6
- ment_inc cuarentena: nac 96.2, mue 67.2, estrechadas 10.4, N 29.0, validadas 5.6, hipotesis 23.4, reversiones 3.6, cel_efecto 30.4
- ment_con colonia: nac 24.0, mue 0.0, estrechadas 0.6, N 24.0
- ment_con colonia_barajada: nac 29.0, mue 1.2, estrechadas 4.2, N 27.8
- ment_con cuarentena: nac 32.8, mue 5.8, estrechadas 1.6, N 27.0, validadas 26.0, hipotesis 1.0, reversiones 0.0, cel_efecto 19.0

## Predicciones
- P1 reordenar: colonia 0.632 (≥0.80), macro_pos 0.003 (≤0.30): REFUTADA
- P2 distractores: colonia 0.758 (≥0.80), macro_pos 0.013 (≤0.30): REFUTADA
- P3 renombrar: colonia 0.255 (≥0.60), macro_etq 0.000 (≤0.20): REFUTADA
- P4 macro_etq en reordenar 1.000 (≥0.95): CUMPLIDA
- P5 cambia_y_vuelve: colonia − 1nn por semilla [0.667, 0.333, 0.5, 0.833, 0.5]; ≥0.15 en 5/5: CUMPLIDA
- P6 irreversibles errados: cuarentena 0.00 % (≤1), colonia sin cuarentena 14.88 % (≥8): CUMPLIDA (cuarentena ≤1: CUMPLIDA; colonia ≥8: CUMPLIDA)
- P7 costo: 1.3 puntos (≤15): CUMPLIDA
  - exploratorio: costo frente a colonia_v2 (misma riqueza de celulas): 12.2 puntos
- P8 mentiroso consistente atraviesa: cuarentena 83.3 % errados (≥50): CUMPLIDA
- Control barajada: colonia − barajada por semilla [-0.043, 0.132, 0.037, 0.005, -0.052]; por delante en 3/5: REFUTADA

## Criterio de cierre
- renombrar: colonia − 1nn -0.647, por delante en 0/5 → el 1-NN empata o gana
- cambia_y_vuelve: P5 → GANA la colonia
  - candado: colonia − 1nn_reciente +0.000, por delante en 0/5 → 1nn_reciente EMPATA o gana
- irreversibles: cuarentena 0.00 % frente al mejor 1nn_abst 10.82 % → GANA la cuarentena
  - candado D1 (primario): cuarentena 0.00 % (0/2071, completas 0.602) frente a 1nn_rec_abst_irr 7.26 % (141/1941, completas 0.557)
  - candado D1 (primario sin mentiroso): cuarentena 0.00 % (0/1741, completas 0.716) frente a 1nn_rec_abst_irr 0.35 % (6/1721, completas 0.707)
  - candado D1 (solo desplazamiento): cuarentena 0.00 % (0/941, completas 0.615) frente a 1nn_rec_abst_irr 3.69 % (34/921, completas 0.587)

**VEREDICTO MECANICO: HAY ALGO MODESTO** (victorias de la colonia: 2/3)