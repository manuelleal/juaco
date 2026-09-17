# Nivel 8 — Aprendizaje abierto: qué existe, qué falta, cómo acortar la línea

**17 sep 2026, noche. Informe de investigación, sin correr nada. Pedido por dirección sobre el Puente 4 de
`HORIZONTE_frontera.md`. Escrito por Claude, sobre el estado del registro al cierre del día 5 (tronco v13).
Citas verificadas por búsqueda; lo no verificado queda marcado.**

## 1. Qué existe

**Open-endedness / novelty search**
- Lehman y Stanley, 2011 (*Evolutionary Computation* 19(2):189–223) — buscar novedad de comportamiento en vez
  de una función objetivo; un objetivo fijo puede ser engañoso y bloquear lo que busca.
- Stanley y Lehman, 2015, libro *Why Greatness Cannot Be Planned* [verificar edición] — el logro complejo pasa
  por piedras de paso que un objetivo no puede anticipar.
- Wang, Lehman, Clune y Stanley, 2019 (POET, arXiv 1901.01753), con *Enhanced POET* en 2020 — co-evolución
  emparejada de mundos (pistas con obstáculos) y agentes que los resuelven; una solución que mejora en un mundo
  se trasplanta a otros; no hay un solo linaje, hay una población de pares mundo–agente.
- Clune, 2019 (AI-GAs, arXiv 1905.10985) — tres piezas hacia IA general: meta-aprender arquitecturas,
  meta-aprender el algoritmo de aprendizaje, generar sin fin entornos de aprendizaje.
- Hughes, Dennis, Parker-Holder, Behbahani, Mavalankar, Shi, Schaul y Rocktäschel (DeepMind), 2024, ICML (arXiv
  2406.04268) — define open-endedness como novedad + aprendibilidad sostenidas para un observador; es postura,
  no resultado.

**Curiosidad por progreso de aprendizaje**
- Oudeyer, Kaplan y Hafner, 2007 (*IEEE Trans. Evolutionary Computation* 11(6):265–286) — Curiosidad Adaptativa
  Inteligente: recompensa interna = mejora reciente de la predicción, no la predicción en sí; evita lo ya
  predecible y lo puramente aleatorio.
- Schmidhuber, teoría formal de la creatividad (1990–2010) y PowerPlay, 2011 — lo interesante es el progreso de
  compresión (la derivada), no el error; PowerPlay busca sin fin el próximo problema más simple aún no resuelto
  que no arruine lo ya resuelto.

**Aprendizaje continuo sin olvido, y sus límites con recursos fijos**
- McClelland, McNaughton y O'Reilly, 1995 — sistemas complementarios (rápido/lento); ya usado en este registro
  para explicar v9→v11.
- Kirkpatrick et al. (DeepMind), 2017, PNAS — EWC: penalización cuadrática que frena mover los pesos importantes
  para tareas viejas (información de Fisher) al aprender una nueva.
- Shin, Lee, Kim y Kim, 2017, NeurIPS (arXiv 1705.08690) — *replay* generativo: un generador entrenado junto al
  modelo produce datos sintéticos de lo viejo para repasar mientras se aprende lo nuevo.
- Límite con recursos fijos [razonamiento propio, no una cita puntual]: la penalización de EWC se acumula tarea
  a tarea; con tareas suficientes las regiones permitidas dejan de solaparse y la red deja de poder moverse. El
  generador del *replay* es también una red de capacidad fija que debe representar una distribución creciente:
  sin crecer, también olvida. Ninguno de los dos métodos, tal como se publicaron, resuelve un número **no
  acotado** de tareas con memoria fija — es el problema del nivel 8.

**Neurogénesis y olvido adaptativo**
- Akers, Martínez-Canabal, Restivo y colegas, con Josselyn y Frankland como autores séniores, 2014, *Science*
  344:598–602 — subir la neurogénesis del hipocampo adulto después de formar un recuerdo basta para borrarlo;
  bajarla en la infancia reduce la amnesia infantil. Ya citado en `HORIZONTE_frontera.md` como paralelo de la
  Etapa 4.

**Evolución abierta en vida artificial**
- Ray, 1991–92 — Tierra: programas autorreplicantes en una CPU virtual; en la primera corrida, sin diseñarlo,
  aparecen parásitos e hiperparásitos.
- Lenski, Ofria, Pennock y Adami, 2003, *Nature* 423:139–144 — en Avida, la función lógica EQU (la más difícil)
  evoluciona desde operaciones simples por piedras de paso, sin diseño dirigido.

**Evolución guiada por LLM**
- Novikov y colegas (Google DeepMind), 2025 — AlphaEvolve: un LLM (Gemini) propone mutaciones de código, un
  evaluador automático las puntúa, ciclo evolutivo; halló un algoritmo para multiplicar matrices complejas 4×4
  con 48 multiplicaciones escalares, mejor que Strassen (1969).
- Zhang, Hu, Lu, Lange y Clune, 2025, arXiv 2505.22954 (ICLR 2026) — Darwin Gödel Machine: un agente que
  reescribe su propio código y se valida en benchmarks de programación; mantiene un archivo creciente de
  variantes (abierto, no un solo linaje), mejora con más cómputo.
- Sakana AI [verificar autoría completa], 2025, arXiv 2509.19349 (ICLR 2026) — ShinkaEvolve: misma idea con un
  conjunto de LLM como operadores de mutación, muestreo por novedad y por bandido; llega a resultados
  comparables con cientos de evaluaciones en vez de miles.

## 2. Qué falta para un organismo de 90 celdas con reglas locales

- **Mundo sin techo.** Los mundos de JUACO tienen 2, 4, 20 o 60 estímulos fijos. El nivel 8 exige un flujo que
  no termine, con presupuesto de interacción constante por paso — no existe hoy (ya señalado en el Puente 4).
- **Órgano que libere capacidad.** v9→v13 sólo saben crecer (división de Kenyon). No hay operación inversa. Con
  90 celdas fijas y novedad sin fin el pool se agota necesariamente; se sabe que se agota suave (v13: 35/60),
  no qué pasa después, porque "después" no existe todavía en ningún mundo del proyecto.
- **Señal de progreso de aprendizaje.** JUACO se mueve por hambre y por valor aprendido (Wp−Wn), nunca por qué
  tan rápido está mejorando en un estímulo. No hay curiosidad.
- **Currículo automático.** La secuencia y el ritmo de los estímulos los fija el experimentador, no el mundo ni
  el organismo.
- **Criterio preregistrado de "sigue aprendiendo indefinidamente".** Las baterías actuales miden un punto fijo
  en el tiempo con semillas 1..N; no una trayectoria larga con estímulos creciendo sin fin. Falta escribirlo
  antes de correr nada (sección 3).
- **Riesgo de confundir capacidad con aprendizaje abierto.** N\*=35/60 es un techo de representación en un mundo
  fijo, no evidencia de que el organismo siga aprendiendo cuando el mundo no para.

## 3. Mecanismo mínimo compatible con v13 (≤ 15 líneas conceptuales)

Mundo (generador de novedad, presupuesto fijo):
1. Un estímulo nuevo entra cada T pasos, sin techo total de estímulos.
2. El estímulo nuevo comparte código Kenyon parcial con estímulos previos (novedad real, no ruido puro).
3. El presupuesto de cómputo por paso no crece con el tiempo.
4. Los estímulos viejos siguen apareciendo, para medir retención y no sólo adquisición.

Órgano (fusión / olvido dirigido, rama 3F):
5. Sin celda libre para un código nuevo: fusionar las dos celdas activas de código más solapado y valor más
   redundante.
6. La fusión promedia el valor, no lo descarta; libera una celda al pool.
7. Regla local, disparada por el mismo tipo de conflicto que hoy dispara división — sin almacén externo (evitar
   la trampa ya documentada en K4: "memoria escondida").

Curiosidad (progreso de aprendizaje, mínima):
8. Cada celda guarda el error de sus últimas M mordidas.
9. La política suma un sesgo hacia el estímulo cuyo error cae más rápido, no hacia el más alto ni el más bajo.
10. Fusión y curiosidad se preregistran y prueban por separado antes de combinarlas (regla 2).

Criterio preregistrable ("sigue aprendiendo"):
11. Medida: acierto en los últimos K estímulos introducidos, no en el total acumulado.
12. Horizonte: cientos de estímulos nuevos, no unas decenas — muchas veces el pool de 90 celdas.
13. Control 1: mismo organismo sin el órgano candidato, mismo mundo.
14. Control 2: mundo con estímulos reciclados en vez de nuevos (novedad falsa).
15. Éxito: acierto en lo nuevo sostenido sobre azar más allá del punto donde v13 sin el órgano cae a azar.

## 4. Cómo acortar la línea

- **Con 6 (planificación):** el mismo sesgo por progreso de aprendizaje que dirige la curiosidad (punto 9) es
  ya una política que elige acción por beneficio futuro esperado, no sólo por gradiente inmediato — un
  experimento sirve a los dos niveles.
- **Con 7 (composición):** la fusión (punto 5) es una operación compositiva, construye una celda desde dos. Si
  la celda fundida resuelve mejor un estímulo que combina rasgos de las dos fusionadas, eso es evidencia de
  composición, no sólo de ahorro de celdas.
- **Con 9 (autonomía):** hoy el currículo lo elige el experimentador y el evaluador de JUACO-EVO lo cura el
  director. Un organismo que elige su propio currículo por curiosidad, y un evaluador que acepta mutaciones con
  menos curaduría humana, son los dos primeros pasos medibles hacia autonomía.
- **El experimento único más informativo:** un experimento, dos brazos, mismas semillas, sobre el mundo de la
  sección 3: v13 sin órgano contra v13+fusión. Da a la vez (a) la asíntota real de v13 más allá de 60 estímulos,
  hoy desconocida, y (b) si el órgano más barato posible alcanza para sostenerla — resuelve con el menor cambio
  de código si además hace falta curiosidad, o no.
- **JUACO-EVO sin trampa:** pedir a subagentes mutaciones candidatas de la regla de fusión, como ya se hizo con
  la división por conflicto de signo; puntuar con semillas retenidas nunca vistas por quien propone; mantener el
  control ciego en paralelo para medir si el LLM de verdad acelera y no sólo para elegir ganador; auditar el
  diff línea a línea antes de fundir a tronco, buscando las trampas de la sección 6; examen final en semillas
  nunca usadas durante la evolución antes de declarar el órgano congelado.

## 5. Romper la frontera

**Idea no probada:** usar JUACO-EVO para co-evolucionar organismo y mundo a la vez — no sólo mutar
`organismo_v13.py`, también mutar el generador de estímulos — siguiendo el patrón de POET.

**Por qué podría funcionar:** JUACO-EVO ya mostró que la búsqueda guiada encuentra en una generación lo que la
búsqueda ciega no encuentra en seis. El nivel 8 tiene dos incógnitas acopladas (qué currículo, qué órgano); POET
mostró que co-evolucionar ambas encuentra soluciones que evolucionar sólo una no encuentra.

**Cómo se refuta:** preregistrar que si la co-evolución no sostiene, con el mismo presupuesto de generaciones,
más acierto en estímulos nuevos que el mejor órgano de la sección 3 corrido sobre el currículo fijo de esa
sección, la idea se refuta — co-evolucionar el mundo no añadió nada sobre evolucionar sólo el organismo.

## 6. Trampas

- **Memoria escondida:** que "fusión" en realidad guarde el valor viejo en un arreglo aparte no contado como
  celda — ya ocurrió con K4 ("retiene 17–20/20 pero la memoria vive en el almacén", día 4).
- **Explotar el mundo:** que los estímulos "nuevos" sean recombinaciones que la vía lenta ya generaliza gratis,
  disfrazando generalización de aprendizaje; o que el organismo evite lo difícil en vez de aprenderlo
  (precedente: huir explotando la geometría del anillo, punto 15 del brief).
- **Medir volumen en vez de aprendizaje:** contar celdas usadas, generaciones corridas o mutaciones aceptadas
  por JUACO-EVO como si fueran progreso, en vez de acierto sobre estímulos nuevos (precedente: criterio por
  conteo vs. tasa). Un evaluador que premia "más mutaciones aceptadas" corre el riesgo ya anotado en
  `REFLEXION_agi.md` para AlphaEvolve y Darwin Gödel Machine: aprender a engañar al evaluador.
- **Curiosidad hackeada:** un sesgo por "el error sigue bajando" se puede ganar generando y resolviendo error
  propio en vez de buscar novedad real; se evita midiendo progreso sólo sobre estímulos que el mundo produce,
  nunca sobre variables que el organismo controla.

## 7. Propuesta en formato del proyecto

**Hipótesis.** v13 con un órgano mínimo de fusión dirigida (sección 3, puntos 5–7) sostiene acierto sobre azar
en estímulos nuevos, en un mundo de novedad creciente con 90 celdas fijas, más allá del punto donde v13 sin el
órgano cae a azar.

**Mundo.** Extensión del generador actual: un estímulo nuevo cada T pasos, sin techo total, presupuesto de
interacción constante, los estímulos viejos siguen apareciendo (sección 3, puntos 1–4).

**Medidas.** Acierto en los últimos K estímulos (adquisición); acierto en los primeros K (retención); celdas
activas y fusionadas; curva de acierto contra número total de estímulos vistos.

**Predicción numérica** (predicción a verificar, no dato medido). v13 sin el órgano cae a azar cerca de donde ya
cae en el mundo fijo (35/60 ≈ 58%, dato existente en el registro); v13+fusión predicho a sostener acierto sobre
azar en al menos la mitad de la distancia entre ese punto y el techo de v11 (50/60 ≈ 83%), manteniendo retención
igual o mayor al estándar vigente de v13.

**Refutación.** Se refuta si el acierto en lo nuevo cae a azar igual con o sin el órgano (la fusión no sirvió),
o si la fusión baja la retención de lo viejo por debajo del piso vigente (compró capacidad con memoria).

**Controles.** (a) v13 sin el órgano, mismo mundo — línea base; (b) fusión ciega/aleatoria (fusiona dos celdas
al azar) — separa el efecto de liberar celdas del efecto de elegir bien cuáles; (c) mundo con estímulos
reciclados en vez de nuevos — separa novedad real de aparente; (d) regresión completa del tronco (regla 1) para
no reabrir ninguna etapa cerrada.

**Coste en corridas.** Del orden de lo ya usado en el proyecto (20 semillas por brazo, T=100000): 4 brazos
(línea base, fusión, fusión ciega, reciclado) × ~20 semillas ≈ 80 corridas, del orden de segundos a minutos cada
una en CPU (punto 17 del brief) — horas de pared, no días.
