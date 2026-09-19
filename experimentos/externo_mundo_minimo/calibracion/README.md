# Corrida 1 - CALIBRACION del mundo minimo (linea externa)

MISION: llegar a la AGI por este camino, con evidencia preregistrada y honestidad:
intentar romper la hipotesis, no demostrarla.

Advertencia del coordinador (vigente): este mundo NO es el organismo JUACO (sin
retina, sin valor, sin codigo). Es una ecologia de juguete. Sus numeros NO entran
en la escalera del proyecto; sirven solo para calibrar la idea de R0.

## Que se corrio
Barrido de `food_probability` en {0.29, 0.30, 0.31, 0.32, 0.33, 0.34}, semillas
0..999 exactas, 180 rondas, 2 fundadores, poblacion maxima 12. Un solo proceso.
PRNG: `random.Random(seed)`, uno por semilla, consumido en el orden exacto de la
dinamica (mezcla -> coste -> comida -> muerte -> reproduccion).

## R0 operacional
R0 = media sobre las 1000 semillas de (hijos directos del fundador 0 + hijos
directos del fundador 1) / 2. NO se usa births/deaths.
Extincion = poblacion 0 al final de las 180 rondas.

## Tabla

| food_probability | R0 | +-SEM | extinction_rate | mean_final_population |
|---|---|---|---|---|
| 0.29 | 0.5335 | 0.0157 | 0.406 | 1.031 |
| 0.30 | 0.6255 | 0.0173 | 0.261 | 1.571 |
| 0.31 | 0.7575 | 0.0202 | 0.153 | 2.119 |
| 0.32 **(CONGELADO)** | 0.9415 | 0.0227 | 0.078 | 2.978 |
| 0.33 | 1.1200 | 0.0242 | 0.037 | 3.835 |
| 0.34 | 1.3130 | 0.0265 | 0.020 | 4.896 |

## Contraste con la referencia externa (ChatGPT)
Referencia: food_probability 0.32 -> R0 0.9665, extincion 0.082, poblacion 3.028.
Obtenido:   R0 0.9415 (SEM 0.0227), extincion 0.078, poblacion 2.978.
Diferencias en unidades de nuestro error estandar: R0 z=-1.10, extincion z=-0.47,
poblacion z=-0.75.

No es reproduccion bit a bit y no puede serlo: la referencia salio de otra
implementacion con otro consumo de PRNG. Lo que se comprueba es que el mismo
mundo, con el mismo R0 operacional, cae dentro del ruido Monte Carlo de la
referencia en las tres cifras. Si se quisiera igualdad exacta habria que recibir
el codigo original, no solo los numeros.

## Congelacion
Se CONGELA food_probability = 0.32. `PARAMETERS.json` lleva el sha256 del motor.
A partir de aqui, una sola modificacion por experimento.

## Archivos
README.md, PARAMETERS.json, RESULTS.json, PER_SEED_RESULTS.json (1000 filas por
arm), GENEALOGY.json (genealogia reconstruible: id, linaje, padre, generacion,
ronda de nacimiento, ronda de muerte, hijos), SUMMARY.md, SHA256.txt y el ZIP.
