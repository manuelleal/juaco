# ESTADO — una página, se reescribe en cada cierre (skill `/juaco-cierre`)

> Última reescritura: **23-sep-2026** (coordinador; revisión de todos los .md por el auditor de documentos + réplica de aprende_barrer + paquetes subida_n5..n10). Si esta fecha tiene más de un día de atraso, el estado real está en la cola de
> `REGISTRO_etapas_1_2.md` y en la última sección de `HANDOFF.md`; corregir esta página antes de tocar nada.
> Historia completa: `REGISTRO_etapas_1_2.md` (sólo añadir). Narrativa: `HANDOFF.md`. Orden vigente: **este archivo** (bloque más reciente) y `HANDOFF.md` §15.x; `PLAN.md` es bitácora hasta el 18-sep. Reglas: `EQUIPO.md` y `CLAUDE.md`.

## AL 23-SEP-2026 (manda sobre lo de abajo cuando se contradiga; detalle en HANDOFF 15.31 y en la cola del REGISTRO)
- **Aprende a barrer, réplica 8121–8140: HAY ALGO MODESTO replicado.** APR 0.385 vs FABRICA 0.336 (mediana R0), APR gana 20/20 (dif. 0.049),
  no cruza; P5 (no descubre la limpieza) y P6 (aprende a contenerse) se cumplen. P8 (gana a APR_SIN_HERENCIA 20/20) se midió en la serie original; la réplica sólo corrió APR y FABRICA. Nivel 8: propuesta 45 %.
- **Subida n8 (serie + réplica): HAY ALGO MODESTO** — sigue aprendiendo con 90 celdas fijas (P2, P6 ×2) pero cae tras agotarlas en la réplica (P3 −0.187); la fusión no ayuda. Propuesta +5.
- **Subida n6 (serie + réplica): HAY ALGO MODESTO por la letra** — rodea limpio por el hueco sin pisar el veneno recordado (1.0 / 0.925, controles 0), cae V1 (memoria incompleta en 1 y 5 semillas); subconjunto regla 10: 11/11 ×2. Propuesta 50 → 60 % (70–75 si el director acepta la regla 10).
- **Subida n10: NO SE LEE** (ancla 0.110 > 0.10, ERR-116); tanda 2 en diseño.
- **Generaciones que conviven, monocultivos 10101–10120: NO** — ningún carro persiste en ≥15/20 con flujo fijo de comida (O1 14/20, O4 3/20, O2/O3 0/20); el cruce de H-1 de ayer
  depende de la reposición inmediata (ERR-104). Mixta H y réplica en cola tras los paquetes de nivel.
- **Subida de niveles 5–10 (pedido del director: "en grupos de agentes de 3 … subir desde el 5 hasta el 10 a 100 o acercarnos"):** seis equipos
  (explorador Haiku → creador Opus → auditor Sonnet) dejaron paquetes preregistrados en `experimentos/subida_nN/` con arnés de identidad y humo; ninguno
  tiene serie todavía, ningún nivel cambia. Auditoría: n5, n6, n7, n9 LISTO CON CORRECCIONES; n10 LISTO PARA SERIE; n8 en construcción (el explorador falló).
  Cola de series (un paquete por Pool, máx. 2 Pools/14 procesos): n10 (corriendo) → n8 → **n9** → n6 → n7 → n5; comandos en `INFORME_nN.md`.
- **Decisión del director (23-sep):** *"esperamos al 9 antes de fijar el 65; tiene que subir a 90"*; *"adelanta el 9 después del 8 y dale dos tandas"*.
  Nivel 9 sigue en 50 % hasta el resultado de `subida_n9`; meta del director: 90 %. Segunda tanda del equipo 9 en diseño (`experimentos/subida_n9b/`).
- **Meta del director (23-sep, antes de salir):** *"si puedes llegar a 100 en todos, fabuloso, ese es el objetivo"*; mínimo leído por el coordinador: **80 %** en
  cada nivel 5–10 (a confirmar con el director). Delegación: *"si hay una decisión difícil tómala, y me dejas comentado por qué la tomaste"*.

## Pedidos del director (23-sep, tarde) y lo lanzado
- *"arranca el v14.3; la idea es que logremos lo que ayer hicimos, superándolo"* → equipo de 3 en `experimentos/tronco_v14_3/`: tronco v14.2 + mapa (n6) + boca aprendida
  (aprende_barrer) + limpieza aprendida, en la pista de la carrera de ayer, contra O1; luego examen con el criterio v4.
- *"soltar el bicho real en un ambiente gigante"* → JUACO-ECO (idea del 21-sep): equipo de 3 en `experimentos/juaco_eco/` (diseño e instrumento; la corrida larga no se lanza aún).
- *"lanza este además"* (memoria lenta con repaso) → tanda en `experimentos/subida_n8c_memoria_lenta/`.
- *"haz un Frankenstein con todo… como prototipo y lo sueltas en el mundo"* → `experimentos/frankenstein/`, **EXPLORATORIO, no es dato**
  (mapa + curiosidad con presupuesto + modelo de sí + memoria lenta + herencia + interruptor explorar/explotar).
- Principio de crecimiento del tronco (respondido al director): una pieza a la vez con memoria declarada, reglas locales, por límite medido,
  lesión que duela, entra por el criterio v4 con réplica. Hallazgo del día: el límite del nivel 8 no es cantidad de memoria sino muestreo.

## Decisiones del coordinador en ausencia del director (23-sep; cada una con su porqué)
- **17:50 — subida_n6 se declara por la letra (HAY ALGO MODESTO), no por el subconjunto de la regla 10.** Por qué: el §10 pide 11/11 principales y V1 es principal; leer el subconjunto como FUNCIONA sería elegir la lectura tras ver el dato. Se deja la propuesta 60 % y la alternativa 70–75 % para el director.
- **17:50 — subida_n9c (tanda 3 del nivel 9) va al FINAL de la cola.** Por qué: su propio creador espera NO (p 0.97) y el auditor coincide en prioridad baja; lo valioso ya salió sin correr: ERR-118 (el 14/20 de O1 no era buena señal). La tanda 4 del nivel 9 necesita otro diseño.
- **17:05 — la mixta H y la réplica de generaciones que conviven van DESPUÉS de los paquetes de nivel (6, 7, 5, 10b).** Por qué: la meta del
  director es subir niveles; la mixta no mueve ningún nivel por sí sola y el monocultivo ya dio NO claro.
- **17:05 — la tanda 3 del nivel 9 se centra en persistir con capacidad de carga.** Por qué: el monocultivo de convivencia muestra que
  el cruce de H-1 no sobrevive a un flujo fijo de comida; sin eso el nivel 9 no pasa de ~68 %.
- **16:50 — subida_n10 NO SE LEE y NO se corre su réplica.** Alternativa descartada: correr la réplica o leer la serie con el ancla movida
  a 0.12. Por qué: mover el ancla después de ver el dato es justo lo que prohíbe la regla 11 (ERR-114 fue lo mismo en pequeño); y aunque se
  leyera, F-2/F-4 caen (PARTO no le gana a BAR), así que lo máximo sería "modesto sin contenido" (+1 punto). Las 2 h de CPU de la réplica
  valen más en los niveles 8 y 9. Se registra ERR-116 y el nivel 10 va a una segunda tanda con el ancla calibrada sobre esta serie.
- **Documentos:** CRITERIO_TRONCO_v4 marcado VIGENTE (decía borrador); PLAN.md marcado bitácora; INDICE.md con filas del 22–23-sep. Último ERR: **118**.

## AL 22-SEP-2026, 21:15 (cierre; manda sobre lo de abajo cuando se contradiga; detalle en HANDOFF 15.30 y en la cola del REGISTRO)
- **Primer cruce de H-1 en JUACO** (carrera de escuderías, monocultivo de O1, que limpia): R0 de nacimientos reales 0.941, replicado en semillas
  selladas y sin la memoria del fundador. Reserva ERR-104: en ese mundo, morder repone al instante una letra al azar.
- **Ronda 2** (combos Opus): O3 y O4 estabilizan en monocultivo y con FABRICA, **replicado en sellada**, con muerte programada declarada. O2
  estabiliza en monocultivo sin muerte programada. La pista de un cuerpo por linaje obliga a morir para parir (ERR-102). Siguiente mundo:
  generaciones que conviven (quimiostato, rama integrada, sin series).
- **Criterio de tronco v4 UTILIZABLE** (v3 retirado). Mundo anclado v2: HAY ALGO MODESTO. Fanin: CAE. Aprende a barrer: HAY ALGO MODESTO sin réplica.
- **Propuestas de nivel pendientes del director:** 8 de 40 a 45 %, 9 de 50 a 65 %, 10–13 de ~10 a 15 %. Último ERR: **113**.
- **Mañana (23-sep):** series de generaciones que conviven (`experimentos/generaciones/INFORME_CONVIVE.md`) → Escuela de abejas con protocolo
  y visualización animada → JUACO-ECO.

## Tronco
**v14.2** (tag `v14.2-tronco`, 18-sep 21:25) = v14.1 + B-5 (división por conflicto disparada por R = 0 bajo retina distinta; repara el alias de
código). 20 archivos congelados (`python manifiesto.py` desde la raíz los verifica). Regla 1 en `CLAUDE.md`. Criterio para candidatos nuevos:
`CRITERIO_TRONCO_v2.md` (sobrevivir + generalizar + desdecirse + sin alias + no regresión conductual + coste + capacidad nueva declarada).

## Niveles del brief (porcentaje = lo declarado con réplica)
| nivel | estado | última evidencia |
|---|---|---|
| 1–4 (asociación, desaprender, generalizar, capacidad) | cerrados; nivel 4 con el negativo del alias reparado por B-5 (v14.2) | 18-sep |
| 5 (comunicación / transmisión) | **75 %**: N1 cerrado; referencia de FAMILIA exacta (k = 3) o de VARIANTE (sufijo), no ambas con la misma tabla; **cerrados el 21-sep: BA, BA-v (tres series ERR-90), BA-vm y BA-vM** (BA-vm cruza dist 16/20 pero muere 9.6× la base); la dirección del mensaje es exacta, el valor falla por colisión estructural; queda V-5 (C) preregistrado sin correr | 21-sep |
| 6 (mapa, dos metas y rodeo) | 50 % (consenso de la junta): elige entre dos comidas recordadas y rodea el veneno recordado (replicado); no planifica; **bloque "rodeo obligado" (21-sep, mundo muralla con geometría sorteada): CAE 5/10, el campo difundido come 2.46× y muere 0.38× pero rodea limpio sólo 0.35 y huye 0.425**; instrumento disponible, sin candidato | 21-sep |
| 7 (composición, XOR) | 70 % (consenso de la junta): 3T-k compone hasta 3; XOR CERRADA: prior estructural de pares (8 ejemplos, 1.000 ×2); hija dispersa en el tronco; **LÍNEA CERRADA (21-sep): memoria de pares en la vía lenta v15c–v15g, ninguno entra** | 21-sep |
| 8 (aprendizaje abierto) | 40 %: curiosidad por progreso refutada; mundo vivo con dos necesidades es el primer mundo con más de una dimensión de valor | 18-sep |
| 9 (autonomía / modelo de sí mismo) | **propuesta 50 % (decide el director; hoy 30 %)**: **bloque 1 DECLARADO COMPLETO** con cuatro series (dos del bloque 1, dos del bloque 2): el cuerpo nuevo rechaza lo malo al primer encuentro sin dejar de comer, vive ~6×, y F9-4bis ×2 muestra que es el contenido del nodo, no cautela; **ni el nodo ORÁCULO cruza R₀ 0.9 en ninguna serie: el muro es el mundo** (H-1 en pie); C-F9B′ cerrado; bloque 3 = cambiar el mundo, con gemelo numba ×46 | 21-sep |
| 10–13 (alma, familias, vivo) | exploratorio: serie ALMA (el alma razonada no gana al azar; el nodo transmite contenido); mundo de familias construido | 18-sep |

## Pendiente con paquete verificado (al 23-sep; historia de los ítems cerrados en el REGISTRO)
1. Generaciones que conviven: mixta H 10101 y réplica 10121 (monocultivos y mixta).
2. Paquetes `experimentos/subida_n5..n10/`: aplicar las correcciones del auditor y correr serie + réplica de cada uno (comandos en su INFORME).
3. Aprende a barrer: replicar los brazos APR_SIN_HERENCIA y APR_AZAR (P8–P10) si se quiere pasar de MODESTO.
4. Mundo anclado v2: fila tox 2.0 (7021–7040). Fase 10 externa: semillas 2441–2840.
5. Fase 9, bloque 3 ("cambiar el mundo"): lo cubren la carrera de escuderías, generaciones que conviven y `subida_n9` (modelo de sí).

## Errores
Último: **ERR-118** (23-sep: 117 el toro del 21-sep no obligaba a rodear, 118 "persiste el carro" confunde fundadores repuestos; 114 enmienda V-M de subida_n9, 115 runners aceptan banderas desconocidas, 116 ancla de subida_n10 sin calibrar en v2) · rango del 22-sep: 94 v4 resuelto · 95–103 carrera de escuderías · 104 quimiostato · 105–110 fase 10 externa · 111–113 mundo anclado v2; detalle en HANDOFF 15.30). Siguiente libre: **ERR-119**. Historia de ERR-87..93 (v3 retirado) en el REGISTRO.
Reglas de equipo 1–14 en `EQUIPO.md`; regla derivada de ERR-87: "último JSON de un prefijo" siempre con prefijo + sello exacto.

## Datos
`datos/` plano (562 archivos, 84 MB). `datos/humo_no_registrado/` guarda humos y corridas sin dueño en el registro (no entran a git).
Desde el 21-sep los runners nuevos escriben sus humos en `datos/humo/`. Índice de carpetas de experimentos: `experimentos/INDICE.md`.

## Equipo y herramientas (21-sep-2026)
Agentes fijos (en `~/.claude/agents`, valen desde cualquier carpeta): `juaco-creador` (Opus), `juaco-compilador` (Opus), `juaco-auditor` (Sonnet,
solo lectura), `juaco-cronista` (Sonnet), `probador-haiku`, `explorador-haiku`. Skills: `/juaco-estado`, `/juaco-bloque`, `/juaco-cierre`,
`/juaco-err`, `/veredicto`, `/encargo`. Ninguno corre Pool, commitea ni mata procesos: sólo el coordinador. Coordinación de CPU: mirar los
procesos python vivos con su cmdline antes de lanzar (ERR-85, ERR-86).

## Decisiones tomadas el 22-sep-2026 (el director: "opción A y las otras tú decides, basado en el objetivo")
- **Nivel 9: 50 %.** La pregunta central ("aprende en menos de una vida") está declarada con cuatro series; lo que falta es del mundo.
- **Criterio de tronco:** v3 retirado; **v4 en construcción** (rama `criterio-v4`, worktree `PROYECTOS\JUACO\criterio`). Hasta que v4 esté calibrado, v2 y v3 lado a lado.
- **Dos Pools en paralelo: SÍ**, con un máximo de 2 Pools y 14 procesos entre los dos (8 núcleos, 16 lógicos). Antes de lanzar se miran los procesos python vivos (ERR-85/86). Nunca tres.
- **Fase 5 / V-5: no por ahora.** Queda en 75 %; no está en el camino del muro de R0.
- **Carrera de escuderías** (rama `carrera-escuderias`, worktree `PROYECTOS\JUACO\carrera`): reglamento aprobado + ENMIENDA 1 (pista escalada L = 40·N, `nobj` = 4·N).
- **Rama de entradas por celda** (6 / 3 / 2; rama `rama-fanin`, worktree `PROYECTOS\JUACO\fanin`): preregistro con predicción de costo del director.

## Decisiones del director (las tres de las 16:30 tomadas y ejecutadas; pendientes al cierre de las 22:50 — resueltas arriba el 22-sep)
1. **Nivel 9: fijar el porcentaje.** Propuesta del coordinador: **50 %** (la pregunta central del nivel, "aprende en menos de una vida", declarada con cuatro series; lo que falta es que un linaje mortal se sostenga, y eso es del mundo).
2. **Criterio de tronco:** retirar v3 (la réplica no repite) y escribir v4 con ERR-94 (T-C ii n = 80 o margen 15; CAL-4 n = 80 o placebo sin tocar el rng). Hasta entonces, candidatos con v2 y v3 lado a lado.
3. **Dos Pools en paralelo como regla** (hoy 7 + 6 sin ERR-86; ninguna puerta mide tiempo de pared).
4. **Fase 5:** correr V-5 (C, 25 %) o dejarla en 75 %.
Hoy: 18 series, 2 declaraciones (fase 9 bloque 1 en parte y luego completa), 5 líneas cerradas, ERR-87..93, junta, necesidades, gemelos numba.
**Mañana:** (0) integrar el resultado externo de la fase 10 con tres correcciones (HANDOFF, nota de última hora) y relanzar la carrera de bacterias → v4 del criterio → fase 9 bloque 3 (candidato 'la boca lee las dos filas') → alefast Fase 3.
