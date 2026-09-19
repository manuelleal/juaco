# Corrida 3 - HIPOTESIS APARTE: dos parches y una accion por ronda

MISION: llegar a la AGI por este camino, con evidencia preregistrada y honestidad:
intentar romper la hipotesis, no demostrarla.

## Prediccion PREREGISTRADA (escrita antes de correr)
E-P sube R0 y baja la extincion respecto de A0-P en >= 60 % de las semillas pareadas; BARAJA-P ~ A0-P (control con la contingencia accion<->recompensa rota).

## La unica modificacion
La comida deja de ser una moneda al aire unica y pasa a estar en DOS PARCHES
(0.42 y 0.22; media 0.32, exactamente la del mundo congelado), y el organismo toma
UNA accion por ronda: elegir parche. Todo lo demas queda igual que en el mundo
congelado. Principio de una sola modificacion por experimento: respetado.

## Brazos
- **A0-P**: elige parche al azar (uniforme). Probabilidad marginal de comida 0.32.
- **E-P**: memoria episodica <= 20 episodios {state, action, reward, outcome};
  elige el parche de mejor recompensa media reciente; exploracion epsilon = 0.10
  DECLARADA.
- **BARAJA-P** (control): identico a E-P salvo que las ETIQUETAS DE ACCION de la
  memoria se permutan al azar antes de decidir. Nota honesta: barajar solo el
  ORDEN de los episodios seria un no-op, porque la media es invariante al orden;
  el control con contenido es permutar la etiqueta de accion, que es lo que rompe
  la contingencia accion<->recompensa conservando las marginales.

## Paso 0: recalibracion de A0-P (obligatoria, antes de comparar)
- R0(A0-P) = 0.9555 (SEM 0.0227)
- R0 del mundo congelado de un parche, mismas semillas = 0.9415
- Desviacion respecto de 1: -0.0445 (-1.96 errores estandar)
- Extincion A0-P 0.087 contra 0.078 del mundo congelado
- Fraccion de elecciones del parche rico en A0-P: 0.498 (debe ser ~0.5)

Lectura: A0-P se comporta como el mundo congelado, como debe ser (la probabilidad
marginal es la misma 0.32). R0 queda por debajo de 1 en la misma medida que el
mundo congelado, a menos de 2 SEM. **Se reporta la desviacion y NO se mueve
ningun parametro**, tal como ordena el encargo.

## Resultados, semillas 0..999

| brazo | R0 | +-SEM | extincion | poblacion final | lineage_survival | fraccion parche rico |
|---|---|---|---|---|---|---|
| A0-P | 0.9555 | 0.0227 | 0.087 | 3.012 | 0.708 | 0.498 |
| E-P | 1.8625 | 0.0310 | 0.008 | 7.623 | 0.908 | 0.743 |
| BARAJA-P | 0.9240 | 0.0223 | 0.092 | 2.923 | 0.707 | 0.497 |

### Comparacion pareada por semilla (R0)

| comparacion | R0 mejor | igual | peor | fraccion mejor | fraccion entre discordantes | p (signos) |
|---|---|---|---|---|---|---|
| E-P_vs_A0-P | 708 | 157 | 135 | 0.708 | 0.840 | 1.79e-94 |
| BARAJA-P_vs_A0-P | 333 | 296 | 371 | 0.333 | 0.473 | 0.163 |
| E-P_vs_BARAJA-P | 743 | 138 | 119 | 0.743 | 0.862 | 5.71e-111 |

- Extincion, semillas donde solo un brazo se extingue: solo A0-P 86 contra solo
  E-P 7 (E-P evita la extincion en la gran mayoria de los casos discordantes).
- Poblacion final: E-P mayor en 865 semillas, menor en 75.

## Replica, semillas 1000..1999

| brazo | R0 | +-SEM | extincion | poblacion final | lineage_survival | fraccion parche rico |
|---|---|---|---|---|---|---|
| A0-P | 0.9215 | 0.0224 | 0.070 | 2.932 | 0.701 | 0.499 |
| E-P | 1.9255 | 0.0321 | 0.007 | 7.699 | 0.920 | 0.750 |
| BARAJA-P | 0.9165 | 0.0222 | 0.101 | 2.884 | 0.692 | 0.497 |

| comparacion | R0 mejor | igual | peor | fraccion mejor | fraccion entre discordantes | p (signos) |
|---|---|---|---|---|---|---|
| E-P_vs_A0-P | 748 | 129 | 123 | 0.748 | 0.859 | 6.16e-110 |
| BARAJA-P_vs_A0-P | 350 | 300 | 350 | 0.350 | 0.500 | 1 |
| E-P_vs_BARAJA-P | 733 | 144 | 123 | 0.733 | 0.856 | 2.02e-106 |

## Veredicto
- Criterio preregistrado (>= 0.60 de las semillas con R0 mayor): principal
  **0.708** (CUMPLE), replica **0.748** (CUMPLE).
- delta R0 principal: **+0.9070**; delta extincion principal: **-0.079**.
- delta R0 replica: **+1.0040**; delta extincion replica: **-0.063**.
- Control BARAJA-P contra A0-P: delta R0 -0.0315, delta extincion +0.005, fraccion
  de semillas mejor 0.333, p del test de signos 0.163. **Indistinguible de A0-P**,
  como estaba predicho.

## Donde esto puede estar enganando
1. El pareado es **por semilla, no por trayectoria**: desde la primera ronda los
   brazos consumen el PRNG del mundo de forma distinta, asi que la semilla fija el
   punto de partida, no el ruido comun. El test de signos sobre 1000 semillas
   sigue siendo valido como comparacion de distribuciones, pero no es un pareado
   en el sentido fuerte.
2. El efecto es **grande y esperado a priori**: con epsilon 0.1 y un parche al
   0.42, la energia neta por ronda pasa de -0.03 a cerca de +0.06. No hace falta
   nada parecido a una mente para conseguirlo; basta un contador de dos casillas.
   Esto NO es evidencia de cognicion: es evidencia de que un bandido de dos brazos
   se resuelve con dos medias.
3. La fraccion de parche rico se queda en 0.743, lejos del 0.95 que permitiria
   epsilon. Con 20 episodios de recompensa 0/1 y medias 0.42 contra 0.22, la
   estimacion es ruidosa y los recien nacidos empiezan con la memoria vacia. El
   agente es peor de lo que podria ser.
4. El mundo tope de 12 organismos **satura**: con E-P la poblacion final media es
   7.623, asi que el hueco de reproduccion se disputa y R0 queda censurado por
   arriba. El efecto medido es una cota inferior del efecto real.
