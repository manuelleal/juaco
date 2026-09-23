# LABORATORIO — agentes investigadores que exploran, experimentan y crean

> Pedido del director (23-sep-2026): *"mundos más grandes pero agentes inteligentes investigadores, para que no se limite sólo a mí,
> sino a la exploración, la experimentación y la creación de la AGI"*. Este archivo define el ciclo. Vale en el PC y en la nube (`NUBE.md`).

## El ciclo (una vuelta = una ronda)
1. **Investigar** (`juaco-investigador`, Opus, varios en paralelo con miradas distintas: neurociencia, vida artificial y open-endedness,
   desarrollo cognitivo, y "el crítico del método"). Cada uno entrega fichas de hipótesis (formato en `.claude/agents/juaco-investigador.md`).
2. **Criticar y ordenar** (un `juaco-auditor` como crítico). Intenta refutar cada ficha: ¿repite una línea cerrada? ¿el control puede ganar
   de verdad? ¿la predicción es falsable? Ordena las fichas por **valor = puntos del nivel × probabilidad / costo de CPU**, con desempate a
   favor de lo que más información da si falla.
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
