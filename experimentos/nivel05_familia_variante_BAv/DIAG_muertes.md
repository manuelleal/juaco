# DIAG_muertes — por que `BA-v` muere 104 en 941–960 (diagnostico, no veredicto)

> Script `analiza_muertes_bav.py` (regla 10: el analisis lo ejecuta un script sobre los JSON). UN proceso,
> sin Pool, sin simular: solo lee los dos crudos de la serie BA. Fecha 2026-09-21 14:19.

- crudo **921-940** `serie_ba_s921-940_20260921_130939_crudo.json` sha256_16 `13f3bdb70928e9f5` — 665 filas, celdas ['b5k3', 'b6suf', 'A1', 'BA', 'BA-v']
- crudo **941-960** `serie_ba_s941-960_20260921_132923_crudo.json` sha256_16 `4dcdffb3d724154d` — 665 filas, celdas ['b5k3', 'b6suf', 'A1', 'BA', 'BA-v']

La columna `muertes` de la tabla registrada es la **mediana sobre semillas de `deaths` del brazo CANAL**
(`corre_familias_ba.py:214`). Todo lo de abajo usa esa misma definicion salvo donde diga otra cosa.

## 1. La distribucion de `deaths` es BIMODAL: hay dos regimenes, no una cola

| serie | celda | n | mediana | media | min | max | semillas >= 200 (regimen de hambre) |
|---|---|---|---|---|---|---|---|
| 921-940 | b5k3 | 19 | **36** | 182 | 15 | 913 | 4 [921, 925, 933, 940] |
| 921-940 | b6suf | 19 | **38** | 173 | 24 | 905 | 4 [925, 931, 933, 937] |
| 921-940 | A1 | 19 | **48** | 214 | 22 | 1329 | 6 [921, 922, 930, 931, 938, 940] |
| 921-940 | BA | 19 | **46** | 227 | 22 | 1331 | 6 [922, 925, 930, 931, 938, 940] |
| 921-940 | BA-v | 19 | **46** | 396 | 22 | 1331 | 7 [921, 922, 925, 930, 931, 938, 940] |
| 941-960 | b5k3 | 19 | **50** | 184 | 17 | 1322 | 4 [944, 945, 948, 952] |
| 941-960 | b6suf | 19 | **49** | 136 | 25 | 896 | 2 [945, 950] |
| 941-960 | A1 | 19 | **37** | 146 | 15 | 895 | 3 [946, 947, 958] |
| 941-960 | BA | 19 | **40** | 156 | 16 | 538 | 5 [946, 947, 950, 953, 958] |
| 941-960 | BA-v | 19 | **104** | 288 | 16 | 1328 | 7 [946, 947, 949, 950, 953, 955, 958] |

Hueco entre los dos regimenes (max del bajo, min del alto) en las 10 combinaciones serie x celda: [(49, 480), (76, 459), (80, 303), (104, 455), (119, 304), (147, 464), (171, 676), (176, 201), (178, 495), (180, 459)].

## 2. Por semilla (brazo CANAL): `deaths` de las cinco celdas en el MISMO mundo

**Serie 921-940** (`*` = >= 200)

| semilla | b5k3 | b6suf | A1 | BA | BA-v | BA-v − A1 | BA-v − BA | okU(BA-v) | comio ref (CANAL) |
|---|---|---|---|---|---|---|---|---|---|
| 921 | **913*** | 46 | **470*** | 31 | **1331*** | +861 | +1300 | 0.5 | si |
| 922 | 32 | 29 | **447*** | **459*** | **480*** | +33 | +21 | 0.6667 | si |
| 923 | 36 | 44 | 38 | 49 | 49 | +11 | +0 | 0.8333 | si |
| 924 | 178 | 38 | 92 | 46 | 46 | -46 | +0 | 0.6667 | si |
| 925 | **906*** | **905*** | 39 | **714*** | **714*** | +675 | +0 | 0.5 | si |
| 926 | 43 | 44 | 22 | 41 | 41 | +19 | +0 | 0.5 | si |
| 927 | 32 | 26 | 119 | 80 | 40 | -79 | -40 | 0.8333 | si |
| 928 | 25 | 24 | 25 | 25 | 23 | -2 | -2 | 0.6667 | si |
| 929 | 36 | 33 | 37 | 31 | 31 | -6 | +0 | 0.6667 | no |
| 930 | 17 | 33 | **466*** | **468*** | **1329*** | +863 | +861 | 0.5 | no |
| 931 | 38 | **898*** | **472*** | **1331*** | **1331*** | +859 | +0 | 0.5 | si |
| 932 | 15 | 32 | 48 | 39 | 39 | -9 | +0 | 0.8333 | si |
| 933 | **495*** | **459*** | 30 | 39 | 39 | +9 | +0 | 0.8333 | si |
| 935 | 33 | 39 | 51 | 47 | 47 | -4 | +0 | 0.8333 | no |
| 936 | 31 | 27 | 30 | 22 | 22 | -8 | +0 | 0.5 | si |
| 937 | 31 | **467*** | 22 | 29 | 29 | +7 | +0 | 0.8333 | si |
| 938 | 58 | 76 | **1329*** | **523*** | **1330*** | +1 | +807 | 0.3333 | si |
| 939 | 26 | 27 | 25 | 32 | 32 | +7 | +0 | 0.6667 | si |
| 940 | **505*** | 36 | **304*** | **303*** | **562*** | +258 | +259 | 0.8333 | si |

- mediana de la diferencia pareada **BA-v − A1 = +7** (sube en 12/19 semillas, baja en 7); **BA-v − BA = +0** (sube 5, baja 2, identica 12).
- semillas donde **solo BA-v** entra en regimen de hambre (A1 y BA no): ninguna

**Serie 941-960** (`*` = >= 200)

| semilla | b5k3 | b6suf | A1 | BA | BA-v | BA-v − A1 | BA-v − BA | okU(BA-v) | comio ref (CANAL) |
|---|---|---|---|---|---|---|---|---|---|
| 941 | 36 | 27 | 34 | 30 | 40 | +6 | +10 | 0.6667 | si |
| 942 | 142 | 120 | 136 | 72 | 180 | +44 | +108 | 0.6667 | si |
| 943 | 43 | 31 | 27 | 40 | 40 | +13 | +0 | 0.6667 | si |
| 944 | **503*** | 44 | 37 | 41 | 41 | +4 | +0 | 0.8333 | si |
| 945 | **201*** | **676*** | 117 | 81 | 117 | +0 | +36 | 0.6667 | si |
| 946 | 49 | 53 | **464*** | **538*** | **509*** | +45 | -29 | 0.5 | si |
| 947 | 25 | 38 | **541*** | **468*** | **908*** | +367 | +440 | 0.3333 | si |
| 948 | **1322*** | 36 | 25 | 21 | 64 | +39 | +43 | 0.8333 | no |
| 949 | 110 | 61 | 45 | 25 | **578*** | +533 | +553 | 0.8333 | si |
| 950 | 37 | **896*** | 23 | **459*** | **459*** | +436 | +0 | 0.6667 | si |
| 951 | 24 | 25 | 37 | 31 | 31 | -6 | +0 | 1.0 | si |
| 952 | **565*** | 79 | 89 | 28 | 28 | -61 | +0 | 0.5 | si |
| 953 | 176 | 171 | 48 | **458*** | **1328*** | +1280 | +870 | 0.5 | si |
| 954 | 17 | 25 | 15 | 16 | 16 | +1 | +0 | 0.8333 | si |
| 955 | 33 | 66 | 32 | 32 | **478*** | +446 | +446 | 0.3333 | si |
| 956 | 50 | 32 | 23 | 36 | 28 | +5 | -8 | 0.5 | si |
| 958 | 52 | 49 | **895*** | **455*** | **464*** | -431 | +9 | 1.0 | si |
| 959 | 24 | 46 | 34 | 38 | 61 | +27 | +23 | 0.6667 | si |
| 960 | 87 | 110 | 147 | 104 | 104 | -43 | +0 | 0.6667 | si |

- mediana de la diferencia pareada **BA-v − A1 = +13** (sube en 14/19 semillas, baja en 4); **BA-v − BA = +9** (sube 10, baja 2, identica 7).
- semillas donde **solo BA-v** entra en regimen de hambre (A1 y BA no): [949, 955]

## 3. Por brazo: mediana de `deaths` en los siete brazos

| serie | celda | CANAL | CORTADO | BAR-H | BAR-T | VALOR | PAR | PAR0 |
|---|---|---|---|---|---|---|---|---|
| 921-940 | b5k3 | 36 | 37 | 38 | 44 | 35 | 42 | 39 |
| 921-940 | b6suf | 38 | 38 | 44 | 38 | 36 | 35 | 34 |
| 921-940 | A1 | 48 | 41 | 41 | 46 | 38 | 36 | 40 |
| 921-940 | BA | 46 | 41 | 38 | 50 | 45 | 46 | 50 |
| 921-940 | BA-v | 46 | 44 | 52 | 50 | 39 | 49 | 48 |
| 941-960 | b5k3 | 50 | 50 | 50 | 50 | 50 | 80 | 77 |
| 941-960 | b6suf | 49 | 45 | 46 | 65 | 45 | 40 | 43 |
| 941-960 | A1 | 37 | 43 | 37 | 42 | 36 | 37 | 34 |
| 941-960 | BA | 40 | 41 | 40 | 57 | 43 | 40 | 51 |
| 941-960 | BA-v | 104 | 101 | 137 | 107 | 100 | 50 | 55 |

El brazo cambia el mundo del mensaje, no el mundo del receptor: si `BA-v` muriera por el mensaje, el
efecto estaria en CANAL y no en CORTADO (gemelo mudo) ni en VALOR (ceros).

## 4. Q2 y Q3: con que correlaciona `deaths` de BA-v

| serie | pareja | rho de Spearman (n = 19) |
|---|---|---|
| 921-940 | deaths(BA-v) vs `okU` | -0.399 |
| 921-940 | deaths(BA-v) vs mordidas del referente | -0.234 |
| 921-940 | deaths(BA-v) vs `mem_vistas` (exposiciones) | -0.794 |
| 921-940 | deaths(BA-v) vs `mem_cobertura` | -0.161 |
| 921-940 | deaths(BA-v) vs celdas usadas | -0.822 |
| 921-940 | **deaths(BA-v) vs deaths(b5k3) en el mismo mundo** | +0.530 |
| 921-940 | **deaths(BA-v) vs deaths(A1) en el mismo mundo** | +0.827 |
| 941-960 | deaths(BA-v) vs `okU` | -0.292 |
| 941-960 | deaths(BA-v) vs mordidas del referente | -0.188 |
| 941-960 | deaths(BA-v) vs `mem_vistas` (exposiciones) | -0.249 |
| 941-960 | deaths(BA-v) vs `mem_cobertura` | -0.349 |
| 941-960 | deaths(BA-v) vs celdas usadas | -0.696 |
| 941-960 | **deaths(BA-v) vs deaths(b5k3) en el mismo mundo** | +0.130 |
| 941-960 | **deaths(BA-v) vs deaths(A1) en el mismo mundo** | +0.532 |

**Q3 (CORTADO 0 = el receptor NUNCA muerde al referente sin mensaje).** CORTADO es una medida de UNA
mordida (la primera exposicion de la vida al referente) en el brazo mudo; no es una tasa de abstinencia.
Lo que si es tasa esta abajo: `mord_ref` (cuantas veces mordio el referente en toda la vida) y `mem_vistas`.

| serie | celda | CORTADO (com/n) | mediana `mord_ref` (CANAL) | mediana `mem_vistas` (CANAL) | mediana celdas |
|---|---|---|---|---|---|
| 921-940 | b5k3 | 2/19 | 19 | 232 | 46 |
| 921-940 | b6suf | 6/19 | 228 | 681 | 57 |
| 921-940 | A1 | 4/19 | 3 | 232 | 38 |
| 921-940 | BA | 2/19 | 1 | 229 | 34 |
| 921-940 | BA-v | 0/19 | 1 | 226 | 34 |
| 941-960 | b5k3 | 1/19 | 4 | 232 | 40 |
| 941-960 | b6suf | 4/19 | 237 | 651 | 43 |
| 941-960 | A1 | 2/19 | 1 | 233 | 39 |
| 941-960 | BA | 1/19 | 3 | 232 | 40 |
| 941-960 | BA-v | 0/19 | 2 | 229 | 37 |

## 5. Lo que NO se puede contestar con estos crudos

- **`b4b` (la base de R6) no esta en ninguna de las dos series** (`meta.celdas` = ['b5k3', 'b6suf', 'A1', 'BA', 'BA-v']): el cociente de R6
  no existe todavia. Por eso el criterio nuevo lo obliga a estar en `--celdas` (ERR-89).
- Estos crudos no traen serie temporal de energia ni de mordidas por paso: no se puede decir *cuando*
  muere, solo *cuanto*. El criterio nuevo anade el diagnostico, no lo suple.

