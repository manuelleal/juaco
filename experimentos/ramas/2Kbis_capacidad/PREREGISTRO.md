# PREREGISTRO — Rama 2K-bis (capacidad en número de estímulos)

Escrito ANTES de correr la Parte 2. Regla 2 del proyecto: hipótesis, predicción numérica, criterio de
refutación, métricas y controles, fijados por adelantado. Regla 3: nada se recalibra a posteriori.

Fecha: 15 sep 2026. Entorno: Windows 11, Python 3.14.2, NumPy 2.4.3, 16 núcleos.
Carpeta: `experimentos/ramas/2Kbis_capacidad/`.

La Parte 1 (barrido de solapamiento) NO se preregistra aquí: ya está preregistrada en
`registro/REGISTRO_etapas_1_2.md`, "Criterio de congelación de v7, VERSIÓN 2", punto 5.

---

## 0. Por qué se redefine 2K-bis

`CLAUDE.md`: *"2K-bis (capacidad) parcialmente respondida por 2L: con plasticidad el techo se resuelve
dividiendo. Redefinir antes de correr."* La pregunta vieja (¿cuánto valor cabe por celda?) quedó sin
sentido cuando las celdas dejaron de ser fijas. La redefinición acordada con el director es:

> **¿Cuántos estímulos distintos caben antes de que los valores se mezclen, y cuántas celdas cuesta
> cada estímulo nuevo?**

## 1. Hipótesis

**H1 (v6, 30 celdas fijas).** Con `NK=30` y `K=3` ganadoras, el número de estímulos que el organismo puede
mantener con valor correcto está limitado por el solapamiento de códigos Kenyon, que crece con el número de
estímulos. A partir de cierto número N* los valores dejan de converger a ±R.

**H2 (v7, hasta 90 celdas, plasticidad 2L).** La división estructural sube el techo, porque convierte
solapamiento en celdas nuevas. El coste es celdas: cada estímulo nuevo que entra en conflicto consume
celdas del presupuesto de 90.

**H3 (agotamiento).** Cuando `activa.sum()==90` la regla 2L deja de poder dividir (la condición
`(~activa).any()` se vuelve falsa) **sin ningún aviso ni mecanismo de recuperación**. La predicción es
degradación suave, no colapso: los estímulos ya separados conservan su valor y sólo los nuevos se mezclan.

## 2. Diseño

### 2.1 Conjunto de patrones y por qué ése

Se usan **los 20 patrones binarios de 6 píxeles con exactamente 3 píxeles encendidos** (peso 3), es decir
la familia completa C(6,3)=20. Razones:

1. **Control de energía de entrada.** El código es `argsort(KW·P)[-3:]`. Patrones de distinto peso producen
   `KW·P` de distinta escala y algunos estímulos ganarían la competición por las celdas sistemáticamente.
   Con peso constante ningún estímulo está favorecido *a priori*. Es la única familia grande con esa propiedad.
2. **Solapamientos de píxel variados y perfectamente balanceados.** Para cualquier patrón de peso 3, los otros
   19 se reparten: **1 con solapamiento 0** (su complementario), **9 con solapamiento 1**, **9 con
   solapamiento 2**. Es decir, el conjunto cubre los tres regímenes de solapamiento y lo hace igual para todos
   los estímulos: no hay ninguno "fácil" ni ninguno "difícil" por construcción.
3. **Continuidad.** A=110100, B=101010, C=011001, D=001011 del `PAT` congelado son de peso 3, así que los
   cuatro estímulos históricos del proyecto están dentro de la familia y son los cuatro primeros.
4. **Techo duro conocido:** 20 estímulos. Si v7 no se rompe con 20, el resultado que se reporta es
   "techo ≥ 20, no alcanzado con la familia de peso 3", NO se mezclan pesos: mezclarlos rompería el control (1).

El solapamiento de **código** Kenyon no se puede elegir (emerge del sorteo de `KW`); se **mide** por semilla y
se reporta junto con el resultado. Único solapamiento forzado: A∩B=0, igual que en v6/v7.

### 2.2 Orden y valencias

Orden fijo: A, B, C, D y después los 16 restantes en orden lexicográfico de su tupla de bits (documentado en
el script). Valencias **alternando** desde el primero: A comida, B veneno, C comida, D veneno, …
(Nota: eso hace que C y D lleven aquí valencia distinta a la de las etapas E2I/E2J. Parte 2 NO es una
réplica de esas etapas; la alternancia la fija el diseño acordado.)

### 2.3 Calendario

A y B desde t=0. El estímulo n-ésimo (n≥3) entra en `t=(n-2)*paso_t` con `paso_t=20000`.
`T = (N-2)*paso_t + 2*paso_t`, de modo que el último estímulo recibe 2 intervalos.
**Checkpoint n**: en `t=(n-1)*paso_t`, justo ANTES de introducir el estímulo n+1. Cada checkpoint mide a
todos los estímulos vivos exactamente `paso_t` pasos después de que entrara el último: series comparables.
Checkpoint final adicional en `t=T`.

### 2.4 Condiciones

| id | versión | plast | celdas | paso_t | semillas |
|---|---|---|---|---|---|
| v6_20k | organismo_cap (=v6) | False | 30 fijas | 20000 | 1..20 |
| v7_20k | organismo_cap (=v7) | True | hasta 90 | 20000 | 1..20 |
| v6_60k | control de muestreo | False | 30 fijas | 60000 | 1..20 |
| v7_60k | control de muestreo | True | hasta 90 | 60000 | 1..20 |

## 3. Métricas

- **W_X** = (Wp−Wn)·kenyon(X) para cada estímulo vivo, en cada checkpoint. R_X = +1 (comida) / −3 (veneno).
- **e_n = mediana sobre los n estímulos vivos de |W_X − R_X|** en el checkpoint n. (Mediana, no media — regla 6.)
- **Techo N\*** = el mayor n tal que e_m ≤ 0.3 para todo m ≤ n. Equivalente: (menor n con e_n > 0.3) − 1.
  Se reporta la mediana y el rango de N* sobre las 20 semillas.
- **celdas(n)**: `activa.sum()` en el checkpoint n. **Celdas por estímulo** = pendiente de celdas(n) sobre
  n∈[3,N] por mínimos cuadrados, y además el incremento mediano Δceldas por estímulo. Es la cifra central.
- **splits(n)**, paso de agotamiento (primer t con celdas=90), solapamiento de código medio entre pares vivos.
- **visitas y mordidas por estímulo y por intervalo** (para separar capacidad de muestreo).
- Tras el agotamiento: e_n de los estímulos ANTIGUOS (los ya separados) vs los NUEVOS, por separado.

## 4. Predicciones numéricas

- **P1.** Techo de v6 (mediana de N*): **entre 3 y 6 estímulos**. Razón: con 30 celdas y K=3, con n estímulos
  el solapamiento medio esperado por par es ~3·3/30 = 0.3 celdas, pero lo que rompe el valor es el
  solapamiento con valencia opuesta acumulado sobre cada celda; con n≥5 casi toda celda de cada código es
  compartida con algún estímulo de valencia contraria. Se predice N*(v6) ≤ 6 en ≥15/20 semillas.
- **P2.** Techo de v7 > techo de v6 en **≥15/20 semillas**, y mediana de N*(v7) ≥ N*(v6)+2.
- **P3.** Celdas por estímulo en v7: **entre 1 y 4** (una división añade 1 celda; se predice más de una
  división por estímulo conflictivo y menos de una por estímulo ortogonal). Con 60 celdas de presupuesto
  (90−30) eso implica agotamiento entre el estímulo 17 y el estímulo 20 si el coste es ~3.
- **P4 (agotamiento).** Al llegar a 90 celdas, los estímulos aprendidos ANTES del agotamiento mantienen
  |W−R| ≤ 0.3 en la mediana; sólo los posteriores se degradan. Degradación suave.

## 5. Criterios de refutación

- **H2 refutada** si la mediana de N*(v7) ≤ la mediana de N*(v6), o si v7 no supera a v6 en ≥15/20 semillas.
  Eso significaría que la plasticidad no compra capacidad y que 2L no resuelve 2K-bis.
- **P3 refutada** si el coste mediano por estímulo cae fuera de [1,4].
- **P4 refutada** si tras el agotamiento la mediana de |W−R| de los estímulos ANTIGUOS supera 0.3, es decir
  si el agotamiento destruye lo ya aprendido. Eso sería colapso, no degradación suave, y sería un defecto
  serio de la arquitectura que habría que registrar como tal.
- **Todo el resultado se anula** si el control de muestreo (§6.2) muestra que el techo medido con paso_t=20000
  sube en ≥2 estímulos al pasar a paso_t=60000: en ese caso lo medido no es capacidad sino falta de tiempo,
  y el número reportado no es un techo.

## 6. Controles

**6.1 Equivalencia del instrumento.** `organismo_cap.py` con el `PAT` canónico de 4 patrones y el plan por
defecto debe reproducir **exactamente** `organismo/organismo_v6.py` (con `plast=False`) y
`organismo/organismo_v7.py` (con `plast=True`) en todos los campos comunes, 6 semillas × 3 escenarios.
Si un solo campo difiere, el módulo no sirve y se para.

**6.2 Control de muestreo (el que puede anular el resultado).** Con más estímulos, cada tipo se ve menos veces
por unidad de tiempo (`nobj=4` objetos en el mundo repartidos entre n tipos). Un valor que no converge puede
deberse a interferencia de representación (capacidad, lo que se quiere medir) o simplemente a pocas mordidas
(muestreo, artefacto). Se corre todo con `paso_t=60000` (3× tiempo por estímulo) y se compara el techo.
Si el techo no se mueve, el límite es representacional. Si sube, es muestreo.

**6.3 Control de disponibilidad.** Se registran visitas y mordidas por estímulo y por intervalo. Un estímulo
con <30 mordidas acumuladas en su checkpoint se marca y se reporta aparte: no se puede afirmar nada sobre un
estímulo que casi no se ha probado. (Error de instrumento tipo 2I, "disponibilidad", ya cometido una vez.)

**6.4 Control de la métrica.** e_n se reporta también excluyendo el estímulo recién introducido, para
comprobar que el techo no es un artefacto de medir un estímulo que lleva sólo paso_t pasos en el mundo.

## 7. Qué NO prueba

Nada sobre conducta: |W−R| es capa de valor, no de política (regla 4). Nada sobre generalización.
Y el techo medido es el de ESTA arquitectura con NK=30/NKMAX=90/K=3, no un límite general.
