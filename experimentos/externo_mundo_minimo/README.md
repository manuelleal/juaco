# Linea externa: MUNDO MINIMO (protocolo ChatGPT, 18-sep-2026)

MISION: llegar a la AGI por este camino, con evidencia preregistrada y honestidad:
intentar romper la hipotesis, no demostrarla.

**Advertencia vigente del coordinador**: este mundo NO es el organismo JUACO (sin
retina, sin valor, sin codigo). Es una ecologia de juguete. Sus numeros NO entran
en la escalera del proyecto (tronco v14.1). Sirven solo para calibrar la idea de
R0 y para probar si una memoria episodica cambia algo.

## Como correr (un solo proceso, sin multiprocessing)

    python docs_calibracion.py          # corrida 1 -> calibracion/
    python docs_a0_vs_e.py              # corrida 2 -> a0_vs_e/
    cd variante_parches && python docs_parches.py   # corrida 3

Cada script corre el experimento y escribe los entregables completos
(README.md, PARAMETERS.json, RESULTS.json, PER_SEED_RESULTS.json, GENEALOGY.json,
SUMMARY.md, SHA256.txt y el ZIP). Todo es determinista: repetir la ejecucion
reproduce los mismos SHA-256 byte a byte (verificado).

## Archivos

| archivo | que es |
|---|---|
| `PROTOCOLO_externo_chatgpt.md` | protocolo recibido + nota del coordinador |
| `mundo_minimo.py` | motor del mundo congelado, dinamica literal del protocolo |
| `entregables.py` | escritura de JSON, SHA256 y ZIP reproducible |
| `run_calibracion.py` / `docs_calibracion.py` | corrida 1 |
| `run_a0_vs_e.py` / `docs_a0_vs_e.py` | corrida 2 |
| `variante_parches/` | corrida 3 (hipotesis aparte) |

## Las tres corridas, en una linea cada una

1. **Calibracion** (`calibracion/`): barrido de `food_probability` en
   {0.29..0.34}, semillas 0..999. En 0.32 se obtiene R0 = 0.9415 (SEM 0.0227),
   extincion 0.078, poblacion final 2.978, frente a la referencia externa 0.9665 /
   0.082 / 3.028: dentro del ruido Monte Carlo. Mundo **CONGELADO** en 0.32.
2. **A0 contra E** (`a0_vs_e/`): en el mundo congelado, E = A0 + memoria episodica
   minima. Resultado: **identidad exacta semilla a semilla**, incluida la
   genealogia completa (0 discrepancias en 1000 semillas). Era la prediccion
   escrita antes. No es un exito de la memoria: es la prueba de que este mundo
   **no puede** testear memoria, porque no hay accion que informar.
3. **Variante de parches** (`variante_parches/`): una sola modificacion, dos
   parches (0.42 y 0.22, media 0.32) y una accion por ronda. A0-P (azar), E-P
   (memoria <= 20, epsilon 0.1), BARAJA-P (control con las etiquetas de accion
   permutadas). E-P sube R0 de 0.9555 a 1.8625 y baja la extincion de 0.087 a
   0.008, mejor en el 70.8 % de las semillas (replica 74.8 %); BARAJA-P se queda
   pegado a A0-P. Prediccion cumplida y replicada con semillas 1000..1999.

## Lo que esto NO demuestra

Que un bandido de dos brazos se resuelva llevando dos medias no es cognicion, y
la ganancia de la corrida 3 era predecible con aritmetica antes de correr nada
(epsilon 0.1 sobre un parche al 0.42 lleva la energia neta por ronda de -0.03 a
cerca de +0.06). El unico resultado con contenido es el par de corridas 2 y 3
leidas juntas: **la memoria episodica es exactamente inerte cuando no hay accion,
y paga cuando existe una accion cuya contingencia se puede registrar**. El control
BARAJA-P es lo que sostiene esa frase; sin el, el efecto podria atribuirse a tener
memoria y no a usarla.
