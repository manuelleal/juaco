# PREREGISTRO (EXPLORATORIO) — BLOQUES3: un mundo que cambia (Opus M, 28-sep-2026, última ronda)

Misión: llegar a la AGI por este camino (organismo mínimo con reglas locales, sin retropropagación, peldaños preregistrados con controles
y réplicas). Escrito ANTES de ver números de exploración (con el arnés y el humo corriendo).

## 1. Pregunta
Cuando lo bueno se vuelve malo, ¿los órganos de memoria o los sociales (kit grande) le ganan al instinto fijo (kit actual) en persistencia
y en K? ¿Cuáles se fijan?

## 2. Mecanismo (`construye_bloques3.py` → `motor_bloques3.py`, 5 anclas desde `motor_bloques2.py` e365506be24bb490)
- Cada **20 000 pasos** se intercambia el SIGNIFICADO de A↔B y C↔D (filas de EFF y RV: efecto y R). La apariencia (los píxeles) no cambia.
  A 500 000 son 24 inversiones; 4 antes de t_corte 100 000.
- La inversión corre en Python entre tramos, en su lugar, y viaja en el checkpoint. Con inv = 0 es motor_bloques2 bit a bit (arnés).
- No usé pat_shuf/nec_shuf de pista2: el gemelo compila su propia física, y la inversión de EFF/RV es el cambio mínimo.
- Declarado: las causas "veneno"/"sal" del núcleo quedan mal rotuladas tras una inversión (miran las letras B/D); no se usan.

## 3. Brazos (ECO w90, FABRICA_ECO, vivero finito t_corte 100 000, T 500 000)
- BLOQ_V_I (kit actual)
- BLOQ2_V_I (kit grande: memoria por letra y vecino)
- BLOQ2_AZA_V_I (kit grande sin herencia)
- ING_F1_V_I (base sin reglas)
- ING_SEL_C_V_I (15 genes; el cerebro aprende en vida)

Semillas NUEVAS 48901–48906 (grep del 28-sep: 489xx libre salvo 48965); arnés 48991–48994; humo 48995. Costo estimado: 30 corridas × ~40 s
≈ 20 min de CPU, 6 procesos.

## 4. Predicciones (antes de números)
| # | predicción | p |
|---|---|---|
| R1 | BLOQ_V_I persiste ≤ 3/6 (el instinto fijo muere con la inversión) | 0.60 |
| R2 | BLOQ2_V_I persiste más que BLOQ_V_I | 0.45 |
| R3 | K(BLOQ2_V_I) > K(BLOQ_V_I) pareado ≥ 4/6 | 0.40 |
| R4 | el órgano de memoria (memF/memL → boca) fijado en ≥ 2/6 de BLOQ2_V_I | 0.40 |
| R5 | un órgano social (vecino) fijado en ≥ 1/6 de BLOQ2_V_I | 0.30 |
| R6 | BLOQ2_AZA_V_I persiste ≤ 1/6 | 0.80 |
| R7 | ING_F1_V_I persiste 0/6 | 0.90 |
| R8 | ING_SEL_C_V_I persiste ≥ BLOQ_V_I (aprender en vida tolera el cambio mejor que el instinto) | 0.50 |

## 5. Qué lo refuta
"La memoria y lo social le ganan al instinto cuando el mundo cambia" cae si BLOQ2_V_I no supera a BLOQ_V_I en persistencia ni en K. El control
sin herencia (AZA) dice si lo fijado es selección o deriva.

## 6. Números

### 6a. Inversión cada 20 000 (48901–48906; `datos/inv`): TODO SE EXTINGUE
0/30 persisten. Los 5 brazos mueren en t ≈ 104 000–121 000, justo al acabarse el vivero; sólo un BLOQ2_V_I llega a 182 819.
Efecto piso: NO SE LEE.
- Aciertan R1, R6 y R7.
- R2, R3, R4, R5 y R8 no se pueden evaluar.

### 6b. Enmienda de las 21:59 (DESPUÉS de 6a, ANTES de correrla)
Periodos largos, mismas semillas, T y t_corte: inversión cada 50 000 (`_I50`) y cada 100 000 (`_I100`; la primera inversión cae justo al
acabarse el vivero).
| # | predicción | p |
|---|---|---|
| S1 | con 100 000, algún brazo persiste en ≥ 2/6 | 0.50 |
| S2 | con 50 000 y con 100 000, BLOQ2_V_I persiste ≥ BLOQ_V_I | 0.50 |
| S3 | con 100 000, ING_SEL_C_V_I persiste más que BLOQ_V_I (el instinto de la fase vieja mata en el cambio) | 0.45 |
Mecanismo que sospecho (antes de datos): tras la inversión, el adulto que APRENDIÓ "A es bueno" muerde veneno, y el que aprendió "B es malo" rechaza la
comida nueva y nunca la vuelve a probar (memoria de rechazo y aversión). Olvidar no está entre las piezas.

### 6c. Periodos largos (6b): TAMBIÉN SE EXTINGUE TODO (0/60)
Los linajes mueren justo después de cada inversión (t_ext agrupados en 100 000, 200 000, 300 000 y 400 000, apenas pasado cada cambio).
Tiempo de extinción, mediana:
| brazo | inversión cada 100 000 | inversión cada 50 000 |
|---|---|---|
| ING_SEL_C (15 genes, aprende en vida) | 203 k | 194 k |
| BLOQ2_V | 200 k | 129 k |
| BLOQ_V | 165 k | 108 k |
| AZA y F1 | ~105–113 k | ~105–113 k |
- Pareado con inversión cada 100 000: SEL_C > BLOQ_V en 4/6; BLOQ2 > BLOQ en 3/6.
- S1, S2 y S3 no se pueden evaluar (piso).

### 6d. Enmienda de las 22:04 (ANTES de correrla)
t_corte 250 000 con inversión cada 50 000 (`_IL`; 5 cambios con subsidio y 5 sin él). Brazos BLOQ_V_IL, BLOQ2_V_IL, BLOQ2_AZA_V_IL e
ING_SEL_C_V_IL; mismas semillas.
Predicción: persiste ≥ 2/6 en algún brazo, p 0.35. Si persiste alguno, BLOQ2_V_IL ≥ BLOQ_V_IL, p 0.5.

### 6e. Vivero hasta 250 000 con inversión cada 50 000 (`_IL`)
| brazo | persiste | K (6 semillas) | t_ext |
|---|---|---|---|
| ING_SEL_C_V_IL (15 genes) | **2/6** | 6.33, 1.57, 1.48, 0.97, 6.03, 1.17 | vivo, 301k, 301k, 277k, vivo, 301k |
| BLOQ2_V_IL | 0/6 | máx. 10.65 | 251k–451k |
| BLOQ_V_IL | 0/6 | máx. 4.29 | 251k–401k |
| BLOQ2_AZA_V_IL | 0/6 | ~0.5 | 252k–259k |
- Acierta la predicción de 6d (algún brazo persiste ≥ 2/6), pero el que persiste es el de los 15 genes, no uno de reglas.
- BLOQ2 ≥ BLOQ: 0 = 0, no se lee.

### 6f. Órganos fijados (banco de padres al extinguirse; formas activas en ≥ 50 % de las 200 entradas)
- **BLOQ_V (kit actual):**
  - el instinto de la retina en casi todas las semillas; el linaje muere en la inversión siguiente;
  - en 2 semillas la selección ya había fijado el instinto INVERTIDO de la fase nueva ("no muerdas píxel 1 presente", "no muerdas sin píxel 4"): lo siguió, pero tarde.
- **BLOQ2_V (kit grande):**
  - con inversión cada 100 000, **el órgano de memoria "no muerdas lo que recuerdas malo" se fija en 4/6** y el instinto de la retina en 1/6. En el mundo estable (k2L) era memoria 3/8 y retina 5/8;
  - con `_IL`: memoria en 2/6, retina en 3/6;
  - no apareció ningún órgano social.
- **BLOQ2_AZA_V:** nada fijado.
- **Mecanismo (visto en las reglas, no medido aparte):** la memoria es "la última R de esa letra" y sólo se actualiza si el cuerpo vuelve a morderla. Tras la inversión, la
  comida nueva quedó recordada como mala y nunca se vuelve a probar. Olvidar no está entre las piezas.

### 6g. Lectura
- **NO:** ni la memoria ni lo social rescatan al linaje cuando el mundo cambia. 0/108 corridas de los brazos de reglas persisten.
- Lo único que persiste (2/6, con vivero largo) es el cerebro de fábrica con sus 15 genes seleccionados, que aprende en vida.
- **Hallazgo descriptivo:** el cambio desplaza la selección del instinto a la memoria (4/6 con inversión cada 100 000), y alarga algo la vida del linaje:
  t_ext mediano 200 k contra 165 k del kit actual; pareado sólo 3/6.
- **Predicciones refutadas:** R3, R5, S1 y S3. R2 y S2 no se leen (0 = 0). Aciertan R1, R4 (4/6 con 100 000), R6, R7, R8 y 6d.
- Instrumento (sha a 16): construye_bloques3 5532f1c1fddbb624 · motor_bloques3 21b5ee28d086b3be · corre_bloques3 3f65f87615b76b24 · identidad_bloques3 5c2dd863daebf702 → salida 9b9c860e4b248623 (10/10).
