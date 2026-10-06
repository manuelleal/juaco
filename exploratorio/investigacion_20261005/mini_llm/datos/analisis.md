
# datos/principal_C200.json  C=200  n=5

## acierto en linea por maestro (media de sus segmentos), mediana [min-max]; y hechos (sonda) tras hechos1/2/3; espanol al final
| brazo | codigo | inventado | hechos (en linea) | sonda hechos1 | hechos2 | hechos3 | espanol fin (base 0.555) | ops/letra | N fin |
|---|---|---|---|---|---|---|---|---|---|
| base | 0.33 [0.25-0.38] | 0.15 [0.13-0.18] | 0.43 [0.40-0.44] | 0.00 [0.00-0.00] | 0.00 [0.00-0.00] | 0.00 [0.00-0.00] | 0.55 [0.55-0.55] | 0 | 0 |
| gradiente | 0.33 [0.29-0.36] | 0.63 [0.60-0.63] | 0.85 [0.84-0.86] | 0.12 [0.12-0.38] | 0.25 [0.12-0.38] | 0.38 [0.25-0.50] | 0.19 [0.16-0.21] | 1090744 | 0 |
| knn | 0.46 [0.38-0.47] | 0.54 [0.52-0.55] | 0.82 [0.80-0.83] | 0.38 [0.25-0.50] | 0.25 [0.12-0.38] | 0.25 [0.12-0.50] | 0.48 [0.47-0.50] | 84495 | 200 |
| colonia | 0.46 [0.36-0.49] | 0.65 [0.63-0.66] | 0.90 [0.90-0.90] | 0.62 [0.62-0.75] | 0.88 [0.75-0.88] | 0.88 [0.75-1.00] | 0.53 [0.53-0.54] | 63855 | 175 |
| col_fija | 0.42 [0.30-0.47] | 0.21 [0.18-0.22] | 0.90 [0.89-0.91] | 1.00 [0.75-1.00] | 0.88 [0.75-1.00] | 0.88 [0.75-1.00] | 0.55 [0.55-0.55] | 65422 | 200 |
| col_barajada | 0.42 [0.34-0.45] | 0.58 [0.57-0.61] | 0.72 [0.69-0.72] | 0.12 [0.00-0.25] | 0.12 [0.00-0.25] | 0.25 [0.00-0.38] | 0.54 [0.54-0.55] | 73383 | 193 |
| col_sin_compuerta | 0.14 [0.10-0.19] | 0.03 [0.02-0.05] | 0.22 [0.20-0.23] | 0.00 [0.00-0.00] | 0.00 [0.00-0.00] | 0.00 [0.00-0.00] | 0.55 [0.00-0.55] | 213 | 0 |
| cuarentena | 0.37 [0.29-0.43] | 0.45 [0.43-0.49] | 0.81 [0.80-0.82] | 0.62 [0.38-0.75] | 0.50 [0.38-0.62] | 0.62 [0.50-0.88] | 0.54 [0.53-0.55] | 54556 | 162 |
| cuarentena_fija | 0.34 [0.26-0.41] | 0.15 [0.13-0.18] | 0.71 [0.70-0.74] | 0.50 [0.50-0.75] | 0.38 [0.25-0.50] | 0.50 [0.25-0.62] | 0.55 [0.55-0.55] | 54181 | 200 |
| sueno | 0.44 [0.33-0.48] | 0.59 [0.58-0.61] | 0.90 [0.89-0.91] | 0.75 [0.75-1.00] | 0.88 [0.75-1.00] | 0.88 [0.50-1.00] | 0.51 [0.50-0.52] | 7579749 | 200 |
| sueno_cuarentena | 0.37 [0.29-0.42] | 0.39 [0.36-0.39] | 0.74 [0.72-0.76] | 0.75 [0.50-0.75] | 0.38 [0.38-0.50] | 0.38 [0.12-0.75] | 0.50 [0.49-0.51] | 5337560 | 154 |

## pareadas por semilla (gana/pierde)
- **colonia vs base**: acierto en linea total: 5/0 de 5 (mediana +0.343); perdida en linea total (menor mejor: signo invertido): 5/0 de 5 (mediana +0.995); sonda hechos1: 5/0 de 5 (mediana +0.625); sonda hechos3 (vuelta): 5/0 de 5 (mediana +0.875); inventado en linea: 5/0 de 5 (mediana +0.504); espanol al final: 0/5 de 5 (mediana -0.021)
- **colonia vs knn**: acierto en linea total: 5/0 de 5 (mediana +0.056); perdida en linea total (menor mejor: signo invertido): 0/5 de 5 (mediana -0.065); sonda hechos1: 5/0 de 5 (mediana +0.375); sonda hechos3 (vuelta): 5/0 de 5 (mediana +0.500); inventado en linea: 5/0 de 5 (mediana +0.114); espanol al final: 5/0 de 5 (mediana +0.049)
- **colonia vs gradiente**: acierto en linea total: 5/0 de 5 (mediana +0.040); perdida en linea total (menor mejor: signo invertido): 0/5 de 5 (mediana -0.381); sonda hechos1: 5/0 de 5 (mediana +0.500); sonda hechos3 (vuelta): 5/0 de 5 (mediana +0.500); inventado en linea: 5/0 de 5 (mediana +0.030); espanol al final: 5/0 de 5 (mediana +0.339)
- **colonia vs col_barajada**: acierto en linea total: 5/0 de 5 (mediana +0.107); perdida en linea total (menor mejor: signo invertido): 5/0 de 5 (mediana +0.426); sonda hechos1: 5/0 de 5 (mediana +0.625); sonda hechos3 (vuelta): 5/0 de 5 (mediana +0.625); inventado en linea: 5/0 de 5 (mediana +0.061); espanol al final: 0/5 de 5 (mediana -0.010)
- **colonia vs col_sin_compuerta**: acierto en linea total: 5/0 de 5 (mediana +0.512); perdida en linea total (menor mejor: signo invertido): 5/0 de 5 (mediana +1.945); sonda hechos1: 5/0 de 5 (mediana +0.625); sonda hechos3 (vuelta): 5/0 de 5 (mediana +0.875); inventado en linea: 5/0 de 5 (mediana +0.618); espanol al final: 2/3 de 5 (mediana -0.018)
- **colonia vs col_fija**: acierto en linea total: 5/0 de 5 (mediana +0.112); perdida en linea total (menor mejor: signo invertido): 5/0 de 5 (mediana +0.316); sonda hechos1: 0/5 de 5 (mediana -0.375); sonda hechos3 (vuelta): 0/1 de 5 (mediana +0.000); inventado en linea: 5/0 de 5 (mediana +0.450); espanol al final: 0/5 de 5 (mediana -0.021)
- **cuarentena vs colonia**: acierto en linea total: 0/5 de 5 (mediana -0.087); perdida en linea total (menor mejor: signo invertido): 0/5 de 5 (mediana -0.236); sonda hechos1: 1/3 de 5 (mediana -0.125); sonda hechos3 (vuelta): 0/4 de 5 (mediana -0.250); inventado en linea: 0/5 de 5 (mediana -0.176); espanol al final: 4/0 de 5 (mediana +0.008)
- **sueno vs colonia**: acierto en linea total: 0/5 de 5 (mediana -0.014); perdida en linea total (menor mejor: signo invertido): 0/5 de 5 (mediana -0.238); sonda hechos1: 5/0 de 5 (mediana +0.125); sonda hechos3 (vuelta): 2/2 de 5 (mediana +0.000); inventado en linea: 0/5 de 5 (mediana -0.054); espanol al final: 0/5 de 5 (mediana -0.021)
- **sueno_cuarentena vs cuarentena**: acierto en linea total: 0/5 de 5 (mediana -0.045); perdida en linea total (menor mejor: signo invertido): 0/5 de 5 (mediana -0.458); sonda hechos1: 3/0 de 5 (mediana +0.125); sonda hechos3 (vuelta): 1/4 de 5 (mediana -0.250); inventado en linea: 0/5 de 5 (mediana -0.089); espanol al final: 0/5 de 5 (mediana -0.036)
- **knn vs base**: acierto en linea total: 5/0 de 5 (mediana +0.285); perdida en linea total (menor mejor: signo invertido): 5/0 de 5 (mediana +1.074); sonda hechos1: 5/0 de 5 (mediana +0.375); sonda hechos3 (vuelta): 5/0 de 5 (mediana +0.250); inventado en linea: 5/0 de 5 (mediana +0.380); espanol al final: 0/5 de 5 (mediana -0.070)
- **gradiente vs base**: acierto en linea total: 5/0 de 5 (mediana +0.304); perdida en linea total (menor mejor: signo invertido): 5/0 de 5 (mediana +1.392); sonda hechos1: 5/0 de 5 (mediana +0.125); sonda hechos3 (vuelta): 5/0 de 5 (mediana +0.375); inventado en linea: 5/0 de 5 (mediana +0.465); espanol al final: 0/5 de 5 (mediana -0.362)

## cuarentena: mentiras y verdades (mediana de semillas)
| brazo | hechos v1 tras hechos1 | tras mentiroso | tras ruido | unavez (verdad dicha 1 vez) tras unavez / al final | pisadas de celulas nacidas en mentiroso | en ruido | contra: dice v1 / v2 / lo de la base | digitos hechos1 por cuartos | reversiones | validadas fin | hipotesis fin | letras hasta validar |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| base | 0.00 | 0.00 | 0.00 | 0.00 / 0.00 | 0 | 0 | 0.00 / 0.00 / 1.00 | 0.00/0.00/0.00/0.00 | - | - | - | - |
| gradiente | 0.12 | 0.25 | 0.00 | 0.00 / 0.00 | 0 | 0 | 0.38 / 0.12 / 0.00 | 0.00/0.08/0.25/0.25 | - | - | - | - |
| knn | 0.38 | 0.00 | 0.00 | 0.50 / 0.00 | 0 | 0 | 0.00 / 0.25 / 0.38 | 0.23/0.25/0.50/0.42 | - | - | - | - |
| colonia | 0.62 | 0.00 | 0.00 | 0.33 / 0.00 | 0 | 0 | 0.25 / 0.75 / 0.00 | 0.15/0.42/0.58/0.75 | - | - | - | - |
| col_fija | 1.00 | 0.00 | 0.00 | 0.83 / 0.00 | 0 | 0 | 0.12 / 0.75 / 0.00 | 0.46/0.83/0.83/0.92 | - | - | - | - |
| col_barajada | 0.12 | 0.00 | 0.00 | 0.00 / 0.00 | 0 | 0 | 0.12 / 0.00 / 0.00 | 0.00/0.08/0.00/0.00 | - | - | - | - |
| col_sin_compuerta | 0.00 | 0.00 | 0.00 | 0.00 / 0.00 | 0 | 0 | 0.00 / 0.00 / 1.00 | 0.00/0.00/0.00/0.00 | - | - | - | - |
| cuarentena | 0.62 | 0.00 | 0.00 | 0.00 / 0.00 | 7 | 0 | 0.12 / 0.00 / 0.88 | 0.00/0.25/0.50/0.67 | 16 | 107 | 53 | 209 |
| cuarentena_fija | 0.50 | 0.00 | 0.00 | 0.00 / 0.00 | 6 | 0 | 0.00 / 0.00 / 1.00 | 0.00/0.08/0.42/0.50 | 18 | 59 | 141 | 240 |
| sueno | 0.75 | 0.00 | 0.00 | 0.33 / 0.00 | 0 | 0 | 0.12 / 0.12 / 0.12 | 0.38/0.50/0.67/0.83 | - | - | - | - |
| sueno_cuarentena | 0.75 | 0.00 | 0.00 | 0.00 / 0.00 | 4 | 0 | 0.00 / 0.12 / 0.12 | 0.00/0.25/0.50/0.67 | 13 | 52 | 113 | 216 |
- cuarentena: validadas por maestro (semilla 1) {'codigo': 72, 'inventado': 132, 'hechos': 79, 'unavez': 2, 'mentiroso': 2, 'mixto': 15, 'contra': 1}; reversiones por maestro {'codigo': 2, 'hechos': 15, 'mentiroso': 1, 'contra': 1}; reversiones tras hechos1/mentiroso/hechos2/hechos3/contra: 2/7/7/11/16
- cuarentena_fija: validadas por maestro (semilla 1) {'codigo': 46, 'inventado': 10, 'hechos': 115, 'contra': 1}; reversiones por maestro {'codigo': 3, 'inventado': 3, 'hechos': 18, 'contra': 1}; reversiones tras hechos1/mentiroso/hechos2/hechos3/contra: 2/9/10/16/18
- sueno_cuarentena: validadas por maestro (semilla 1) {'codigo': 69, 'inventado': 115, 'hechos': 127, 'mentiroso': 2, 'mixto': 10, 'contra': 3}; reversiones por maestro {'codigo': 2, 'hechos': 11, 'mentiroso': 1, 'contra': 1}; reversiones tras hechos1/mentiroso/hechos2/hechos3/contra: 2/7/7/8/13

## especializacion en 'mix' (pisadas hechas por una celula nacida en el mismo maestro) y nacimientos por maestro (semilla 1)
- colonia: especializacion 0.83; nacimientos {'codigo': 684, 'inventado': 321, 'hechos': 107, 'unavez': 17, 'mentiroso': 6, 'ruido': 412, 'mixto': 402, 'contra': 5}; vivas por origen al final {'unavez': 1, 'contra': 1, 'codigo': 4, 'hechos': 50, 'mixto': 1, 'inventado': 118}; estrechadas 1396
- col_fija: especializacion 0.80; nacimientos {'codigo': 1125, 'inventado': 1705, 'hechos': 198, 'unavez': 46, 'mentiroso': 19, 'ruido': 525, 'mixto': 827, 'contra': 7}; vivas por origen al final {'contra': 1, 'inventado': 121, 'hechos': 78}; estrechadas 0
- col_barajada: especializacion 0.81; nacimientos {'codigo': 601, 'inventado': 302, 'hechos': 183, 'unavez': 18, 'mentiroso': 20, 'ruido': 377, 'mixto': 411, 'contra': 13}; vivas por origen al final {'contra': 10, 'codigo': 32, 'hechos': 41, 'mixto': 20, 'inventado': 97}; estrechadas 2898
- col_sin_compuerta: especializacion 1.00; nacimientos {'codigo': 554, 'inventado': 524, 'hechos': 914, 'unavez': 32, 'mentiroso': 147, 'ruido': 106, 'mixto': 274, 'contra': 152}; vivas por origen al final {'inventado': 1}; estrechadas 0
- cuarentena: especializacion 0.75; nacimientos {'codigo': 966, 'inventado': 638, 'hechos': 297, 'unavez': 27, 'mentiroso': 45, 'ruido': 520, 'mixto': 555, 'contra': 17}; vivas por origen al final {'unavez': 1, 'codigo': 1, 'hechos': 45, 'mixto': 1, 'inventado': 126}; estrechadas 3180
- cuarentena_fija: especializacion 0.72; nacimientos {'codigo': 1207, 'inventado': 1774, 'hechos': 473, 'unavez': 53, 'mentiroso': 72, 'ruido': 533, 'mixto': 842, 'contra': 32}; vivas por origen al final {'inventado': 147, 'hechos': 53}; estrechadas 0
- sueno: especializacion 0.87; nacimientos {'codigo': 802, 'inventado': 450, 'hechos': 165, 'unavez': 22, 'mentiroso': 7, 'ruido': 499, 'mixto': 570, 'contra': 11}; vivas por origen al final {'contra': 1, 'inventado': 180, 'hechos': 19}; estrechadas 983
- sueno_cuarentena: especializacion 0.77; nacimientos {'codigo': 1025, 'inventado': 816, 'hechos': 415, 'unavez': 32, 'mentiroso': 44, 'ruido': 523, 'mixto': 700, 'contra': 25}; vivas por origen al final {'inventado': 143, 'hechos': 11}; estrechadas 1901

# datos/principal_C40.json  C=40  n=5

## acierto en linea por maestro (media de sus segmentos), mediana [min-max]; y hechos (sonda) tras hechos1/2/3; espanol al final
| brazo | codigo | inventado | hechos (en linea) | sonda hechos1 | hechos2 | hechos3 | espanol fin (base 0.555) | ops/letra | N fin |
|---|---|---|---|---|---|---|---|---|---|
| base | 0.33 [0.25-0.38] | 0.15 [0.14-0.18] | 0.43 [0.40-0.44] | 0.00 [0.00-0.00] | 0.00 [0.00-0.00] | 0.00 [0.00-0.00] | 0.55 [0.55-0.55] | 0 | 0 |
| knn | 0.36 [0.33-0.38] | 0.36 [0.31-0.38] | 0.68 [0.67-0.69] | 0.25 [0.00-0.38] | 0.12 [0.00-0.25] | 0.12 [0.00-0.25] | 0.49 [0.49-0.51] | 16953 | 40 |
| colonia | 0.33 [0.30-0.41] | 0.30 [0.29-0.39] | 0.65 [0.62-0.72] | 0.25 [0.00-0.38] | 0.62 [0.62-0.88] | 0.75 [0.50-0.88] | 0.55 [0.55-0.55] | 16940 | 40 |
| cuarentena | 0.34 [0.28-0.38] | 0.20 [0.18-0.28] | 0.72 [0.72-0.76] | 0.12 [0.12-0.38] | 0.12 [0.12-0.38] | 0.12 [0.00-0.38] | 0.55 [0.55-0.55] | 16943 | 40 |
| sueno | 0.34 [0.30-0.40] | 0.31 [0.30-0.37] | 0.78 [0.77-0.82] | 0.38 [0.25-0.62] | 0.50 [0.38-0.62] | 0.50 [0.25-0.62] | 0.51 [0.49-0.52] | 4087893 | 40 |
| sueno_cuarentena | 0.33 [0.27-0.36] | 0.19 [0.17-0.24] | 0.68 [0.63-0.73] | 0.25 [0.12-0.50] | 0.12 [0.12-0.25] | 0.12 [0.12-0.38] | 0.49 [0.47-0.51] | 2744691 | 40 |

## pareadas por semilla (gana/pierde)
- **colonia vs base**: acierto en linea total: 5/0 de 5 (mediana +0.171); perdida en linea total (menor mejor: signo invertido): 5/0 de 5 (mediana +0.363); sonda hechos1: 3/0 de 5 (mediana +0.250); sonda hechos3 (vuelta): 5/0 de 5 (mediana +0.750); inventado en linea: 5/0 de 5 (mediana +0.166); espanol al final: 0/5 de 5 (mediana -0.005)
- **colonia vs knn**: acierto en linea total: 2/3 de 5 (mediana -0.016); perdida en linea total (menor mejor: signo invertido): 0/5 de 5 (mediana -0.201); sonda hechos1: 2/2 de 5 (mediana +0.000); sonda hechos3 (vuelta): 5/0 de 5 (mediana +0.625); inventado en linea: 2/3 de 5 (mediana -0.050); espanol al final: 5/0 de 5 (mediana +0.057)
- **cuarentena vs colonia**: acierto en linea total: 2/3 de 5 (mediana -0.014); perdida en linea total (menor mejor: signo invertido): 4/1 de 5 (mediana +0.047); sonda hechos1: 2/2 de 5 (mediana +0.000); sonda hechos3 (vuelta): 0/5 de 5 (mediana -0.500); inventado en linea: 0/5 de 5 (mediana -0.107); espanol al final: 2/0 de 5 (mediana +0.000)
- **sueno vs colonia**: acierto en linea total: 5/0 de 5 (mediana +0.039); perdida en linea total (menor mejor: signo invertido): 0/5 de 5 (mediana -0.142); sonda hechos1: 4/1 de 5 (mediana +0.375); sonda hechos3 (vuelta): 1/3 de 5 (mediana -0.125); inventado en linea: 2/3 de 5 (mediana -0.008); espanol al final: 0/5 de 5 (mediana -0.044)
- **sueno_cuarentena vs cuarentena**: acierto en linea total: 0/5 de 5 (mediana -0.019); perdida en linea total (menor mejor: signo invertido): 0/5 de 5 (mediana -0.585); sonda hechos1: 2/0 de 5 (mediana +0.000); sonda hechos3 (vuelta): 2/0 de 5 (mediana +0.000); inventado en linea: 0/5 de 5 (mediana -0.008); espanol al final: 0/5 de 5 (mediana -0.060)
- **knn vs base**: acierto en linea total: 5/0 de 5 (mediana +0.187); perdida en linea total (menor mejor: signo invertido): 5/0 de 5 (mediana +0.614); sonda hechos1: 3/0 de 5 (mediana +0.250); sonda hechos3 (vuelta): 4/0 de 5 (mediana +0.125); inventado en linea: 5/0 de 5 (mediana +0.213); espanol al final: 0/5 de 5 (mediana -0.060)

## cuarentena: mentiras y verdades (mediana de semillas)
| brazo | hechos v1 tras hechos1 | tras mentiroso | tras ruido | unavez (verdad dicha 1 vez) tras unavez / al final | pisadas de celulas nacidas en mentiroso | en ruido | contra: dice v1 / v2 / lo de la base | digitos hechos1 por cuartos | reversiones | validadas fin | hipotesis fin | letras hasta validar |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| base | 0.00 | 0.00 | 0.00 | 0.00 / 0.00 | 0 | 0 | 0.00 / 0.00 / 1.00 | 0.00/0.00/0.00/0.00 | - | - | - | - |
| knn | 0.25 | 0.00 | 0.00 | 0.17 / 0.00 | 0 | 0 | 0.00 / 0.00 / 0.75 | 0.08/0.00/0.00/0.00 | - | - | - | - |
| colonia | 0.25 | 0.00 | 0.00 | 0.17 / 0.00 | 0 | 0 | 0.25 / 0.62 / 0.12 | 0.00/0.00/0.00/0.00 | - | - | - | - |
| cuarentena | 0.12 | 0.00 | 0.00 | 0.00 / 0.00 | 7 | 0 | 0.00 / 0.00 / 1.00 | 0.00/0.00/0.17/0.08 | 4 | 29 | 11 | 150 |
| sueno | 0.38 | 0.00 | 0.00 | 0.33 / 0.00 | 0 | 0 | 0.00 / 0.12 / 0.00 | 0.15/0.17/0.17/0.33 | - | - | - | - |
| sueno_cuarentena | 0.25 | 0.00 | 0.00 | 0.00 / 0.00 | 0 | 0 | 0.00 / 0.00 / 0.50 | 0.00/0.00/0.08/0.33 | 3 | 8 | 32 | 168 |
- cuarentena: validadas por maestro (semilla 1) {'codigo': 3, 'inventado': 17, 'hechos': 41, 'mentiroso': 1}; reversiones por maestro {'hechos': 4}; reversiones tras hechos1/mentiroso/hechos2/hechos3/contra: 0/1/1/2/4
- sueno_cuarentena: validadas por maestro (semilla 1) {'codigo': 3, 'inventado': 17, 'hechos': 70, 'contra': 6}; reversiones por maestro {'hechos': 6, 'contra': 1}; reversiones tras hechos1/mentiroso/hechos2/hechos3/contra: 0/2/2/2/3

## especializacion en 'mix' (pisadas hechas por una celula nacida en el mismo maestro) y nacimientos por maestro (semilla 1)
- colonia: especializacion 0.78; nacimientos {'codigo': 1007, 'inventado': 1308, 'hechos': 861, 'unavez': 23, 'mentiroso': 108, 'ruido': 451, 'mixto': 612, 'contra': 83}; vivas por origen al final {'hechos': 27, 'inventado': 9, 'contra': 4}; estrechadas 1083
- cuarentena: especializacion 0.71; nacimientos {'codigo': 1313, 'inventado': 1401, 'hechos': 670, 'unavez': 32, 'mentiroso': 118, 'ruido': 526, 'mixto': 743, 'contra': 101}; vivas por origen al final {'hechos': 26, 'inventado': 13, 'mentiroso': 1}; estrechadas 2489
- sueno: especializacion 0.85; nacimientos {'codigo': 1096, 'inventado': 1311, 'hechos': 600, 'unavez': 34, 'mentiroso': 90, 'ruido': 495, 'mixto': 729, 'contra': 119}; vivas por origen al final {'hechos': 10, 'inventado': 29, 'contra': 1}; estrechadas 675
- sueno_cuarentena: especializacion 0.72; nacimientos {'codigo': 1363, 'inventado': 1387, 'hechos': 730, 'unavez': 40, 'mentiroso': 110, 'ruido': 534, 'mixto': 807, 'contra': 63}; vivas por origen al final {'hechos': 8, 'inventado': 31, 'contra': 1}; estrechadas 1399
