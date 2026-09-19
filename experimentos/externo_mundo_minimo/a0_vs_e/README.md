# Corrida 2 - A0 contra E (memoria episodica minima), mundo CONGELADO

MISION: llegar a la AGI por este camino, con evidencia preregistrada y honestidad:
intentar romper la hipotesis, no demostrarla.

## Prediccion PREREGISTRADA (escrita antes de correr)
A0 == E en todas las metricas, semilla a semilla, porque en este mundo no hay accion que la memoria pueda informar. Si difieren es un error de implementacion (PRNG), no un efecto.

## Que cambio
Una sola modificacion: E = A0 + memoria episodica minima
{state, action, reward, outcome}, local, <= 20 episodios por organismo, sin acceso
global, sin futuro, sin otros organismos, sin backprop, sin supervisor.
La memoria SOLO registra: no consume PRNG y no toca ninguna rama de la dinamica.
Mundo congelado: food_probability = 0.32, semillas 0..999, comparacion pareada.

## Resultado

| metrica | A0 | E | delta |
|---|---|---|---|
| R0 | 0.9415 | 0.9415 | 0.0000 |
| extinction_rate | 0.078 | 0.078 | 0.000 |
| mean_final_population | 2.978 | 2.978 | 0.000 |
| lineage_survival | 0.714 | 0.714 | 0.000 |
| descendants_per_founder | 1.243 | 1.243 | 0.000 |
| mean_survival_time | 125.96 | 125.96 | 0.00 |
| number_of_generations | 1.226 | 1.226 | 0.000 |

- Semillas comparadas: 1000
- Semillas con alguna discrepancia en cualquier metrica: **0**
- Semillas con genealogia byte a byte identica: **1000 / 1000**
- Identidad exacta semilla a semilla: **SI**
- memory_usage: E registra en media 537.4 episodios por semilla (cap 20 por
  organismo); A0 no tiene memoria.

## Lectura honesta
Esto NO es un exito de la memoria episodica. Es la confirmacion de que este mundo
no puede testear memoria: no hay accion, luego no hay nada que una memoria pueda
informar. La identidad exacta es una prueba de correccion de la implementacion
(el PRNG se consume igual en ambas ramas), no un resultado biologico ni cognitivo.
Cualquier diferencia habria sido un bug, no un efecto.

Por eso la pregunta interesante se traslada a `variante_parches/`, donde se
introduce UNA accion (elegir parche) manteniendo la media de comida en 0.32.
