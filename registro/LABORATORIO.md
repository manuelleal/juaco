# LABORATORIO — agentes investigadores que exploran, experimentan y crean

> Pedido del director (23-sep-2026): *"mundos más grandes pero agentes inteligentes investigadores, para que no se limite sólo a mí,
> sino a la exploración, la experimentación y la creación de la AGI"*. Este archivo define el ciclo. Vale en el PC y en la nube (`NUBE.md`).

## Principio (director, 23-sep): la misión es la AGI, no llenar benchmarks
*"¿Qué sentido tendría llenar benchmarks si el bicho no hace nada? Esa es la misión real: llegar a la AGI."*

Cada ficha se juzga por lo que le agrega al MISMO organismo en un mundo común (v14.x en JUACO-ECO), no por los puntos que sume en una
caja hecha para ella. **Máximo 2 frentes activos** (hoy: v14.3; gemelo rápido + ECO). El laboratorio alimenta esos frentes y no abre otros.

## El ciclo (una vuelta = una ronda)
1. **Investigar** (`juaco-investigador`, Opus, varios en paralelo con miradas distintas: neurociencia, vida artificial y open-endedness,
   desarrollo cognitivo, y "el crítico del método"). Cada uno entrega fichas de hipótesis (formato en `.claude/agents/juaco-investigador.md`).
2. **Criticar y ordenar** (un `juaco-auditor` como crítico). Intenta refutar cada ficha: ¿repite una línea cerrada? ¿el control puede ganar
   de verdad? ¿la predicción es falsable? Ordena las fichas por **valor = cuánto acerca al organismo común (v14.x) a sostener su vida con recursos limitados y a
   combinar sus piezas en un mismo mundo × probabilidad / costo de CPU**, no por puntos de nivel; desempate a favor de lo que más
   información da si falla.
3. **Diseñar** (`juaco-creador`) las 1–3 primeras: preregistro, instrumento por anclas, arnés N/N, humo.
4. **Auditar** (`juaco-auditor`) cada paquete.
5. **Correr** (el coordinador; Pool): serie y réplica.
6. **Registrar** (`juaco-cronista` + coordinador): REGISTRO, ESTADO, HANDOFF, commit, push.
7. **Integrar**: lo que FUNCIONA con réplica se propone al tronco (v14.3, v14.4…) por anclas y con el criterio v4; cada versión se congela.

## Presupuesto de exploración
- **70 %** de las rondas van a fichas con protocolo, por valor.
- **20 %** a ideas grandes de riesgo alto: mundos gigantes (JUACO-ECO), órganos nuevos, cambios de mundo.
- **10 %** a exploratorios libres, como la escuela, el tesoro o el Frankenstein: sin protocolo y marcados "EXPLORATORIO — no es dato".
  Sirven para ver qué pasa; lo que prometa se rehace con protocolo.

## Mundos más grandes
JUACO-ECO (`experimentos/juaco_eco/`) es el banco de pruebas grande: el organismo real, energía finita, herencia con mutación y juez
automático. Cada órgano o tronco nuevo que pase su réplica se suelta ahí. Se escala por pasos (1×, 10×, 100× de la pista de la carrera)
con checkpoints. La medida de éxito del laboratorio es una capacidad que nadie diseñó, replicable.

## Frenos
- Sin retropropagación, reglas locales, memoria declarada, tronco congelado y regla 11 (ERR por cualquier umbral tocado tras ver datos).
- Dos NO seguidos en la misma línea la cierran.
- Nada se declara sin réplica; los porcentajes de nivel los fija el director.

## Huecos de ciencia (23-sep-2026, 20:30; pregunta del director: "¿qué nos falta, dónde está el santo grial, qué ciencia no hemos probado?")
Revisados contra el repo (grep en registro/ y preregistros): estas ideas aparecen como literatura, pero **nunca se probaron en el bicho**.
1. **Aprender prediciendo, no sólo valorando.** El tronco aprende sólo al morder (delta de valor en Wp/Wn; nivel 8: 4–8 mordidas por
   comida en toda la vida). Ver y moverse no le enseñan nada. Candidato: predecir en cada paso lo que verá o sentirá y aprender del error
   (codificación predictiva: Rao y Ballard 1999; inferencia activa: Friston). Con reglas locales aproxima la retropropagación (Whittington
   y Bogacz 2017), así que respeta la regla de JUACO.
2. **Evolucionar la regla de aprendizaje, no sólo perillas.** La naturaleza evolucionó reglas de plasticidad; cada animal aprende con
   ellas (Soltoggio, Risi y Stanley 2018; Najarro y Risi 2020, reglas de Hebb evolucionadas). Encaja en ECO v2.
3. **Jerarquía.** El bicho tiene un solo nivel de representación (expansión fija + celdas); nunca se intentó apilar niveles que aprendan
   de los de abajo (0 menciones en el registro). La codificación predictiva jerárquica lo da con reglas locales.
4. **Un mundo que pida inteligencia.** El crítico de la ronda 1: el mundo "bien mezclado" no paga las capacidades de los niveles 6–10.
   Hacen falta ubicación, tiempo, otros agentes y novedad (POET: Wang et al. 2019). Es el diseño de ECO.
5. **Cultura acumulativa.** Transmisión fiel más innovación durante muchas generaciones (Tomasello; Henrich). Se probó transmitir;
   nunca acumular.

**Apuesta del coordinador (juicio, no dato):** 1 + 2 juntos: un bicho que aprende prediciendo en cada paso, con una regla que afina la
evolución en ECO, en un mundo que paga por predecir. No es un frente nuevo: (1) es la pieza del frente 1 después de "arriesgar según
la reserva"; (2) es ECO v2 en el frente 2.
