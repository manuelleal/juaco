# datos/sensibilidad_ctx025.json — semillas [11, 12, 13, 14, 15], 20 tareas por familia y regimen, C=200
elementos por pantalla: 8–24

## Parte 1 — tareas completas (media de semillas; entre corchetes min–max)
| regimen | macro_pos | macro_etq | 1nn | 1nn_reciente | logistica | colonia | colonia_barajada | colonia_v2 |
|---|---|---|---|---|---|---|---|---|
| sin_cambio | 1.000 [1.00–1.00] | 1.000 [1.00–1.00] | 1.000 [1.00–1.00] | 1.000 [1.00–1.00] | 1.000 [1.00–1.00] | 1.000 [1.00–1.00] | 1.000 [1.00–1.00] | 1.000 [1.00–1.00] |
| reordenar | 0.003 [0.00–0.01] | 1.000 [1.00–1.00] | 0.987 [0.98–0.99] | 0.987 [0.98–0.99] | 1.000 [1.00–1.00] | 0.972 [0.94–1.00] | 1.000 [1.00–1.00] | 0.987 [0.98–0.99] |
| renombrar | 1.000 [1.00–1.00] | 0.000 [0.00–0.00] | 0.748 [0.66–0.82] | 0.748 [0.66–0.82] | 0.113 [0.09–0.13] | 0.058 [0.01–0.14] | 0.087 [0.05–0.13] | 0.713 [0.65–0.75] |
| distractores | 0.013 [0.01–0.03] | 0.710 [0.69–0.74] | 1.000 [1.00–1.00] | 1.000 [1.00–1.00] | 0.872 [0.82–0.91] | 0.783 [0.72–0.85] | 0.845 [0.79–0.88] | 1.000 [1.00–1.00] |
| cambia_y_vuelve | 1.000 [1.00–1.00] | 1.000 [1.00–1.00] | 0.433 [0.17–0.67] | 1.000 [1.00–1.00] | 1.000 [1.00–1.00] | 1.000 [1.00–1.00] | 0.900 [0.83–1.00] | 1.000 [1.00–1.00] |
| cambia_y_vuelve@0 | 0.000 [0.00–0.00] | 0.000 [0.00–0.00] | 0.433 [0.17–0.67] | 0.000 [0.00–0.00] | 1.000 [1.00–1.00] | 0.000 [0.00–0.00] | 0.067 [0.00–0.17] | 0.000 [0.00–0.00] |
| cambia_y_vuelve@2 | 1.000 [1.00–1.00] | 1.000 [1.00–1.00] | 0.433 [0.17–0.67] | 1.000 [1.00–1.00] | 1.000 [1.00–1.00] | 1.000 [1.00–1.00] | 0.800 [0.67–0.83] | 1.000 [1.00–1.00] |
| ment_inc | 0.133 [0.00–0.17] | 0.133 [0.00–0.17] | 0.000 [0.00–0.00] | 0.133 [0.00–0.17] | 0.878 [0.82–1.00] | 0.133 [0.00–0.17] | 0.033 [0.00–0.17] | 0.133 [0.00–0.17] |
| ment_con | 0.000 [0.00–0.00] | 0.000 [0.00–0.00] | 0.000 [0.00–0.00] | 0.000 [0.00–0.00] | 0.000 [0.00–0.00] | 0.000 [0.00–0.00] | 0.033 [0.00–0.17] | 0.000 [0.00–0.00] |

## Pareado por semilla: colonia frente a cada rival (gana/empata/pierde de 5; diferencia media)
| regimen | macro_pos | macro_etq | 1nn | 1nn_reciente | logistica | colonia_barajada | colonia_v2 |
|---|---|---|---|---|---|---|---|
| sin_cambio | 0/5/0 (+0.000) | 0/5/0 (+0.000) | 0/5/0 (+0.000) | 0/5/0 (+0.000) | 0/5/0 (+0.000) | 0/5/0 (+0.000) | 0/5/0 (+0.000) |
| reordenar | 5/0/0 (+0.968) | 0/1/4 (-0.028) | 2/0/3 (-0.015) | 2/0/3 (-0.015) | 0/1/4 (-0.028) | 0/1/4 (-0.028) | 2/0/3 (-0.015) |
| renombrar | 0/0/5 (-0.942) | 5/0/0 (+0.058) | 0/0/5 (-0.690) | 0/0/5 (-0.690) | 1/0/4 (-0.055) | 1/0/4 (-0.028) | 0/0/5 (-0.655) |
| distractores | 5/0/0 (+0.770) | 5/0/0 (+0.073) | 0/0/5 (-0.217) | 0/0/5 (-0.217) | 0/0/5 (-0.088) | 0/0/5 (-0.062) | 0/0/5 (-0.217) |
| cambia_y_vuelve | 0/5/0 (+0.000) | 0/5/0 (+0.000) | 5/0/0 (+0.567) | 0/5/0 (+0.000) | 0/5/0 (+0.000) | 3/2/0 (+0.100) | 0/5/0 (+0.000) |

Exploratorio (fuera del veredicto): colonia_v2 − 1nn por regimen: sin_cambio +0.000 (0/5/0); reordenar +0.000 (0/5/0); renombrar -0.035 (0/1/4); distractores +0.000 (0/5/0); cambia_y_vuelve +0.567 (5/0/0)

## Parte 2 — irreversibles (suma de las 5 semillas)
irr errados % = clics irreversibles equivocados ejecutados / propuestas de irreversible. abst % = abstenciones / propuestas de irreversible. pide % = (abstenciones + reversiones) / pasos. completas = sin ayuda.

**Conjunto primario (5 regimenes honestos + mentiroso inconsistente)**

| brazo | irr errados % | errados / propuestas | por 100 tareas | semillas con 0 errados | abst % | pide % | completas | completas o con ayuda |
|---|---|---|---|---|---|---|---|---|
| colonia | 12.93 | 239 / 1848 | 6.64 | 0/5 | 0.0 | 0.0 | 0.658 | 0.658 |
| colonia_v2 | 7.10 | 147 / 2069 | 4.08 | 1/5 | 0.0 | 0.0 | 0.806 | 0.806 |
| cuarentena | 0.00 | 0 / 2176 | 0.00 | 5/5 | 26.7 | 4.0 | 0.714 | 0.843 |
| cuar_sin_efecto | 0.09 | 2 / 2176 | 0.06 | 4/5 | 20.8 | 3.2 | 0.749 | 0.843 |
| cuar_sin_k | 6.74 | 140 / 2076 | 3.89 | 1/5 | 6.7 | 1.1 | 0.769 | 0.810 |
| 1nn | 9.84 | 181 / 1840 | 5.03 | 0/5 | 0.0 | 0.0 | 0.695 | 0.695 |
| 1nn_abst_irr | 9.78 | 180 / 1840 | 5.00 | 1/5 | 25.2 | 3.4 | 0.566 | 0.695 |
| 1nn_abst_todo | 9.42 | 181 / 1921 | 5.03 | 0/5 | 29.2 | 4.0 | 0.635 | 0.719 |

**Solo regimenes honestos (para el costo)**

| brazo | irr errados % | errados / propuestas | por 100 tareas | semillas con 0 errados | abst % | pide % | completas | completas o con ayuda |
|---|---|---|---|---|---|---|---|---|
| colonia | 5.79 | 94 / 1623 | 3.13 | 0/5 | 0.0 | 0.0 | 0.763 | 0.763 |
| colonia_v2 | 0.11 | 2 / 1844 | 0.07 | 4/5 | 0.0 | 0.0 | 0.940 | 0.940 |
| cuarentena | 0.00 | 0 / 1846 | 0.00 | 5/5 | 15.7 | 2.3 | 0.843 | 0.945 |
| cuar_sin_efecto | 0.11 | 2 / 1846 | 0.07 | 4/5 | 8.8 | 1.4 | 0.885 | 0.945 |
| cuar_sin_k | 0.00 | 0 / 1846 | 0.00 | 5/5 | 7.0 | 1.1 | 0.897 | 0.945 |
| 1nn | 3.55 | 61 / 1720 | 2.03 | 1/5 | 0.0 | 0.0 | 0.834 | 0.834 |
| 1nn_abst_irr | 3.49 | 60 / 1720 | 2.00 | 2/5 | 26.9 | 3.6 | 0.680 | 0.834 |
| 1nn_abst_todo | 3.39 | 61 / 1801 | 2.03 | 1/5 | 31.1 | 4.3 | 0.762 | 0.863 |

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

**reordenar**

| brazo | irr errados % | errados / propuestas | por 100 tareas | semillas con 0 errados | abst % | pide % | completas | completas o con ayuda |
|---|---|---|---|---|---|---|---|---|
| colonia | 0.00 | 0 / 385 | 0.00 | 5/5 | 0.0 | 0.0 | 0.972 | 0.972 |
| colonia_v2 | 0.00 | 0 / 392 | 0.00 | 5/5 | 0.0 | 0.0 | 0.987 | 0.987 |
| cuarentena | 0.00 | 0 / 392 | 0.00 | 5/5 | 0.0 | 0.0 | 0.987 | 0.987 |
| cuar_sin_efecto | 0.00 | 0 / 392 | 0.00 | 5/5 | 0.0 | 0.0 | 0.987 | 0.987 |
| cuar_sin_k | 0.00 | 0 / 392 | 0.00 | 5/5 | 0.0 | 0.0 | 0.987 | 0.987 |
| 1nn | 0.00 | 0 / 392 | 0.00 | 5/5 | 0.0 | 0.0 | 0.987 | 0.987 |
| 1nn_abst_irr | 0.00 | 0 / 392 | 0.00 | 5/5 | 47.4 | 6.9 | 0.677 | 0.987 |
| 1nn_abst_todo | 0.00 | 0 / 392 | 0.00 | 5/5 | 0.0 | 0.0 | 0.987 | 0.987 |

**renombrar**

| brazo | irr errados % | errados / propuestas | por 100 tareas | semillas con 0 errados | abst % | pide % | completas | completas o con ayuda |
|---|---|---|---|---|---|---|---|---|
| colonia | 77.05 | 94 / 122 | 15.67 | 0/5 | 0.0 | 0.0 | 0.058 | 0.058 |
| colonia_v2 | 0.79 | 2 / 252 | 0.33 | 4/5 | 0.0 | 0.0 | 0.713 | 0.713 |
| cuarentena | 0.00 | 0 / 254 | 0.00 | 5/5 | 51.2 | 6.2 | 0.497 | 0.740 |
| cuar_sin_efecto | 0.79 | 2 / 254 | 0.33 | 4/5 | 1.2 | 0.8 | 0.705 | 0.737 |
| cuar_sin_k | 0.00 | 0 / 254 | 0.00 | 5/5 | 51.2 | 6.2 | 0.497 | 0.740 |
| 1nn | 0.37 | 1 / 268 | 0.17 | 4/5 | 0.0 | 0.0 | 0.748 | 0.748 |
| 1nn_abst_irr | 0.00 | 0 / 268 | 0.00 | 5/5 | 72.0 | 7.9 | 0.428 | 0.750 |
| 1nn_abst_todo | 0.29 | 1 / 349 | 0.17 | 4/5 | 160.5 | 21.4 | 0.390 | 0.893 |

**distractores**

| brazo | irr errados % | errados / propuestas | por 100 tareas | semillas con 0 errados | abst % | pide % | completas | completas o con ayuda |
|---|---|---|---|---|---|---|---|---|
| colonia | 0.00 | 0 / 316 | 0.00 | 5/5 | 0.0 | 0.0 | 0.783 | 0.783 |
| colonia_v2 | 0.00 | 0 / 400 | 0.00 | 5/5 | 0.0 | 0.0 | 1.000 | 1.000 |
| cuarentena | 0.00 | 0 / 400 | 0.00 | 5/5 | 0.0 | 0.0 | 1.000 | 1.000 |
| cuar_sin_efecto | 0.00 | 0 / 400 | 0.00 | 5/5 | 0.0 | 0.0 | 1.000 | 1.000 |
| cuar_sin_k | 0.00 | 0 / 400 | 0.00 | 5/5 | 0.0 | 0.0 | 1.000 | 1.000 |
| 1nn | 0.00 | 0 / 400 | 0.00 | 5/5 | 0.0 | 0.0 | 1.000 | 1.000 |
| 1nn_abst_irr | 0.00 | 0 / 400 | 0.00 | 5/5 | 21.0 | 3.1 | 0.860 | 1.000 |
| 1nn_abst_todo | 0.00 | 0 / 400 | 0.00 | 5/5 | 0.0 | 0.0 | 1.000 | 1.000 |

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

**ment_inc**

| brazo | irr errados % | errados / propuestas | por 100 tareas | semillas con 0 errados | abst % | pide % | completas | completas o con ayuda |
|---|---|---|---|---|---|---|---|---|
| colonia | 64.44 | 145 / 225 | 24.17 | 1/5 | 0.0 | 0.0 | 0.133 | 0.133 |
| colonia_v2 | 64.44 | 145 / 225 | 24.17 | 1/5 | 0.0 | 0.0 | 0.133 | 0.133 |
| cuarentena | 0.00 | 0 / 330 | 0.00 | 5/5 | 87.9 | 17.2 | 0.067 | 0.333 |
| cuar_sin_efecto | 0.00 | 0 / 330 | 0.00 | 5/5 | 87.9 | 17.2 | 0.067 | 0.333 |
| cuar_sin_k | 60.87 | 140 / 230 | 23.33 | 1/5 | 4.3 | 0.7 | 0.133 | 0.133 |
| 1nn | 100.00 | 120 / 120 | 20.00 | 1/5 | 0.0 | 0.0 | 0.000 | 0.000 |
| 1nn_abst_irr | 100.00 | 120 / 120 | 20.00 | 1/5 | 0.0 | 0.0 | 0.000 | 0.000 |
| 1nn_abst_todo | 100.00 | 120 / 120 | 20.00 | 1/5 | 0.0 | 0.0 | 0.000 | 0.000 |

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

**POST HOC (D1): solo desplazamiento (reordenar + renombrar + distractores), umbral del 1-NN calibrado ahi mismo**

| brazo | irr errados % | errados / propuestas | por 100 tareas | semillas con 0 errados | abst % | pide % | completas | completas o con ayuda |
|---|---|---|---|---|---|---|---|---|
| colonia | 11.42 | 94 / 823 | 5.22 | 0/5 | 0.0 | 0.0 | 0.604 | 0.604 |
| colonia_v2 | 0.19 | 2 / 1044 | 0.11 | 4/5 | 0.0 | 0.0 | 0.900 | 0.900 |
| cuarentena | 0.00 | 0 / 1046 | 0.00 | 5/5 | 12.4 | 1.9 | 0.828 | 0.909 |
| cuar_sin_efecto | 0.19 | 2 / 1046 | 0.11 | 4/5 | 0.3 | 0.2 | 0.897 | 0.908 |
| cuar_sin_k | 0.00 | 0 / 1046 | 0.00 | 5/5 | 12.4 | 1.9 | 0.828 | 0.909 |
| 1nn | 0.09 | 1 / 1060 | 0.06 | 4/5 | 0.0 | 0.0 | 0.912 | 0.912 |
| 1nn_abst_irr | 0.00 | 0 / 1060 | 0.00 | 5/5 | 12.2 | 1.6 | 0.841 | 0.912 |
| 1nn_abst_todo | 0.09 | 1 / 1095 | 0.06 | 4/5 | 12.5 | 1.7 | 0.879 | 0.931 |

**POST HOC (D1): primario SIN mentiroso inconsistente, umbral calibrado ahi mismo**

| brazo | irr errados % | errados / propuestas | por 100 tareas | semillas con 0 errados | abst % | pide % | completas | completas o con ayuda |
|---|---|---|---|---|---|---|---|---|
| colonia | 5.79 | 94 / 1623 | 3.13 | 0/5 | 0.0 | 0.0 | 0.763 | 0.763 |
| colonia_v2 | 0.11 | 2 / 1844 | 0.07 | 4/5 | 0.0 | 0.0 | 0.940 | 0.940 |
| cuarentena | 0.00 | 0 / 1846 | 0.00 | 5/5 | 15.7 | 2.3 | 0.843 | 0.945 |
| cuar_sin_efecto | 0.11 | 2 / 1846 | 0.07 | 4/5 | 8.8 | 1.4 | 0.885 | 0.945 |
| cuar_sin_k | 0.00 | 0 / 1846 | 0.00 | 5/5 | 7.0 | 1.1 | 0.897 | 0.945 |
| 1nn | 3.55 | 61 / 1720 | 2.03 | 1/5 | 0.0 | 0.0 | 0.834 | 0.834 |
| 1nn_abst_irr | 3.49 | 60 / 1720 | 2.00 | 2/5 | 16.5 | 2.2 | 0.739 | 0.834 |
| 1nn_abst_todo | 3.44 | 61 / 1771 | 2.03 | 1/5 | 17.0 | 2.3 | 0.792 | 0.851 |

## Microsegundos por clic (decision; media de semillas) y memoria al final de la fase A
| brazo | us/clic | memoria |
|---|---|---|
| macro_pos | 1 | 27 |
| macro_etq | 1 | 27 |
| 1nn | 85 | 135 |
| 1nn_reciente | 95 | 135 |
| logistica | 315 | 135 |
| colonia | 57 | 5 |
| colonia_barajada | 59 | 6 |
| colonia_v2 | 60 | 25 |
| cuarentena | 74 | 48 |
- honesto_A colonia: nac 5.4, mue 0.0, estrechadas 0.0, N 5.4
- honesto_A colonia_barajada: nac 5.8, mue 0.0, estrechadas 0.0, N 5.8
- honesto_A cuarentena: nac 31.2, mue 4.4, estrechadas 0.0, N 26.8, validadas 26.8, hipotesis 0.0, reversiones 0.0, cel_efecto 21.0
- honesto_fin colonia: nac 32.2, mue 7.6, estrechadas 0.6, N 24.6
- honesto_fin colonia_barajada: nac 39.6, mue 3.6, estrechadas 16.4, N 36.0
- honesto_fin cuarentena: nac 45.0, mue 18.2, estrechadas 1.2, N 26.8, validadas 21.4, hipotesis 5.4, reversiones 12.0, cel_efecto 22.6
- ment_inc colonia: nac 93.0, mue 64.4, estrechadas 5.6, N 28.6
- ment_inc colonia_barajada: nac 95.2, mue 54.4, estrechadas 24.6, N 40.8
- ment_inc cuarentena: nac 95.8, mue 66.8, estrechadas 11.2, N 29.0, validadas 5.8, hipotesis 23.2, reversiones 4.0, cel_efecto 30.4
- ment_con colonia: nac 23.8, mue 0.0, estrechadas 0.4, N 23.8
- ment_con colonia_barajada: nac 26.2, mue 0.6, estrechadas 3.6, N 25.6
- ment_con cuarentena: nac 32.6, mue 5.6, estrechadas 1.2, N 27.0, validadas 26.0, hipotesis 1.0, reversiones 0.0, cel_efecto 19.0

## Predicciones
- P1 reordenar: colonia 0.972 (≥0.80), macro_pos 0.003 (≤0.30): CUMPLIDA
- P2 distractores: colonia 0.783 (≥0.80), macro_pos 0.013 (≤0.30): REFUTADA
- P3 renombrar: colonia 0.058 (≥0.60), macro_etq 0.000 (≤0.20): REFUTADA
- P4 macro_etq en reordenar 1.000 (≥0.95): CUMPLIDA
- P5 cambia_y_vuelve: colonia − 1nn por semilla [0.667, 0.333, 0.5, 0.833, 0.5]; ≥0.15 en 5/5: CUMPLIDA
- P6 irreversibles errados: cuarentena 0.00 % (≤1), colonia sin cuarentena 12.93 % (≥8): CUMPLIDA (cuarentena ≤1: CUMPLIDA; colonia ≥8: CUMPLIDA)
- P7 costo: -8.1 puntos (≤15): CUMPLIDA
  - exploratorio: costo frente a colonia_v2 (misma riqueza de celulas): 9.7 puntos
- P8 mentiroso consistente atraviesa: cuarentena 83.3 % errados (≥50): CUMPLIDA
- Control barajada: colonia − barajada por semilla [0.025, -0.012, 0.013, -0.028, -0.017]; por delante en 2/5: REFUTADA

## Criterio de cierre
- renombrar: colonia − 1nn -0.690, por delante en 0/5 → el 1-NN empata o gana
- cambia_y_vuelve: P5 → GANA la colonia
  - candado: colonia − 1nn_reciente +0.000, por delante en 0/5 → 1nn_reciente EMPATA o gana
- irreversibles: cuarentena 0.00 % frente al mejor 1nn_abst 9.42 % → GANA la cuarentena

**VEREDICTO MECANICO: HAY ALGO MODESTO** (victorias de la colonia: 2/3)