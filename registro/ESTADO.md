# ESTADO — una página, se reescribe en cada cierre (skill `/juaco-cierre`)

> Última reescritura: **23-sep-2026, ~19:00** (coordinador; CIERRE PARCIAL: la cola de la noche sigue corriendo en el PC del director y cada
> resultado se registra al salir). Si esta fecha tiene más de un día de atraso, el estado real está en la cola de `REGISTRO_etapas_1_2.md` y en
> la última sección de `HANDOFF.md`; corregir esta página antes de tocar nada.
> Historia: `REGISTRO_etapas_1_2.md` (sólo añadir). Narrativa: `HANDOFF.md` (§15.30 = 22-sep, §15.31–15.32 = 23-sep). Orden vigente: **este archivo**.
> Reglas: `CLAUDE.md` y `EQUIPO.md`. Trabajo sin el PC: `NUBE.md`. Laboratorio de agentes investigadores: `LABORATORIO.md`.

## PLAN VIGENTE (aprobado por el director el 23-sep, ~19:00: *"sí, de acuerdo contigo… no permitas que haya muchos frentes"*)
**Palabras del director (~19:00):** *"¿qué sentido tendría llenar benchmarks si el bicho no hace nada? Esa es la misión real: llegar a la AGI."*
**Norte:** un solo organismo, el bicho real, que aprenda por sí mismo a sostener su vida con recursos limitados y combine sus piezas en un mismo
mundo. No se persiguen puntajes por caja: una capacidad cuenta cuando la muestra el mismo organismo en un mundo común.

**Máximo 2 frentes activos. Nada nuevo se abre hasta cerrar uno.**
1. **v14.3** (`experimentos/tronco_v14_3/`). Es el tronco v14.2 más lo replicado:
   - la reparación N del nivel 7 (FUNCIONA ×2);
   - el mapa del nivel 6 (gradiente + filtro), cuando `subida_n6b` complete la memoria y lo porte a v14.2;
   - la boca aprendida y heredada (APR, aprende_barrer).

   Se corre en la pista de la carrera del 22-sep contra O1 y pasa el examen del criterio v4. Se construye por anclas y se congela con
   manifiesto propio; v14.2 no se toca.
2. **Gemelo rápido + JUACO-ECO por escalones** (`experimentos/juaco_eco/`). Primero el gemelo numba del v14.3 (con identidad). Después ECO
   con el v14.3 a 1×, 10× y 100× del tamaño de la pista, con checkpoints. Dos preguntas:
   - ¿persiste un linaje del bicho real sin comida regalada (ERR-104) y sin fundadores repuestos (ERR-118)?
   - ¿aparece algo que el control de mutación sin selección no produce?

Lo demás se cierra: se corre lo ya preregistrado para tener su veredicto, porque un preregistro sin dato es un frente abierto, o se archiva.
Laboratorio de investigadores: una ronda al día como máximo y sólo al servicio de estos dos frentes.

## Corriendo esta noche (PC del director; cola cerrada, sin frentes nuevos)
- **Pool A:** réplica del nivel 9 13321–13340 (desde 18:15, llegada estimada ~19:40) → `subida_n9b` (serie 13501 + réplica 13521) →
  `subida_n6b` (14601 + 14621) → `subida_n8c_memoria_lenta` (15801 + 15821).
- **Pool B:** `subida_n5` V-5 (serie 25701 desde 18:38, réplica 25721) → **`tronco_v14_3`** (identidad 36/36, serie 14301 + réplica 14321;
  frente 1, adelantado a las 19:15). `subida_n8b` pasa al Pool A tras n8c. `subida_n10b` corre mañana en la nube.
- **Archivado sin correr:** `subida_n9c` (decisión 18:55, abajo).
- **Equipos terminando:** v14.3, JUACO-ECO (diseño), Frankenstein (EXPLORATORIO, no es dato) y la ronda de investigación 1 (tres
  investigadores y un crítico). Sus carpetas entran al repo cuando entreguen y se auditen.
- Cada serie corre su arnés de identidad antes y se detiene si no da N/N. Cada resultado se registra al salir (REGISTRO, commit y push).

## NOCHE 23→24-sep: trabaja sola; el coordinador audita el 24-sep (director, ~21:05: "lo cerramos así, dejamos que el agente trabaje solo y lo auditas mañana")
- **PC, hasta ~00:00:** v14.3 (serie 14301 y réplica 14321) · 9b réplica 13521 (la serie 13501 dio las tres lesiones sin pérdida, P2
  refutada: la ventaja de APR viene de contenerse, no de predecirse) · 6b → 8c → 8b.
- **Agentes locales:** examen v4 del v14.3 (`experimentos/tronco_v14_3_examen/`, creador + auditor) · prueba de humo del bicho en
  aprendizaje continuo de ML (`PROYECTOS/JUACO/ml_continuo/`, FUERA del repo, exploratoria).
- **Nube, sesión de noche** (rama `nube/noche-20260924`, bitácora `registro/NUBE_BITACORA_20260924.md`): 10b serie y réplica → ECO
  (prueba de Pool, serie, réplica) → exploratorios "arriesgar según la reserva" y "aprender prediciendo".
- **Auditoría del 24-sep, en orden:**
  1. `/juaco-estado`;
  2. leer los logs de la cola de la noche y registrar cada veredicto;
  3. leer la bitácora de la nube e integrar su rama;
  4. auditar el paquete del examen v4 y correrlo (en la nube o el PC);
  5. si pasa serie y réplica, congelar v14.3 (permiso escrito del director, 19:30);
  6. decidir con el director el nivel 9 (propuesta 55 %) y la pieza siguiente ("arriesgar según la reserva").

## Resultados del 23-sep (detalle y tablas en el REGISTRO)
| bloque | veredicto | en una línea |
|---|---|---|
| aprende_barrer, réplica | HAY ALGO MODESTO ×2 | APR 0.385 vs FABRICA 0.336, gana 20/20; aprende a contenerse, no descubre la limpieza |
| subida_n7 | **FUNCIONA** ×2 | el tronco v14.2 no compone (K_max 1): regresión. La reparación N compone hasta 8. Entra al v14.3 |
| subida_n6 | HAY ALGO MODESTO ×2 (letra) | rodea el veneno recordado por el hueco (1.0 / 0.925, controles 0). Cae V1: en 3 semillas la memoria incompleta deja escapar el campo |
| subida_n8 | HAY ALGO MODESTO ×2 | sigue aprendiendo con 90 celdas; pierde al agotarlas (réplica). El cuello es de muestreo; la fusión no sirve |
| subida_n10 | NO SE LEE | ancla 0.110 > 0.10 (ERR-116); el mensaje del padre casi no trae información |
| generaciones que conviven (monocultivos) | NO | con flujo fijo de comida ningún carro persiste ≥15/20; el cruce de H-1 del 22-sep depende de la reposición inmediata |
| subida_n9 | **HAY ALGO MODESTO ×2** | O3 cruza porque decide con su estado presente: con el mismo estado desfasado cae de 0.968 a 0.072 (0/180), 20/20 en las dos series. La reserva no hace falta |
| subida_n5 (V-5) | NO por la letra | K1 cae en la réplica (+2); aun así, en la réplica BA-v5 logra la misión (19/19, BAR-T 4) sin morir de más |

## Niveles del brief (los porcentajes los fija el director; la columna "propuesta" es del coordinador)
| nivel | fijado | propuesta tras el 23-sep | evidencia |
|---|---|---|---|
| 1–4 | cerrados | — | 18-sep (nivel 4 reparado por B-5) |
| 5 comunicación | 75 % | 75 % | V-5 NO por la letra (K1 cae); la línea se cierra con "familia O variante" |
| 6 mapa y rodeo | **60 %** (19:30) | 60 % (70–75 % si n6b completa la memoria) | n6 MODESTO ×2; `subida_n6b` en cola (memoria completa, dos metas, port a v14.2) |
| 7 composición | **78 %** (19:30) | 80 % si v14.3 pasa el criterio v4 | n7 FUNCIONA ×2 |
| 8 aprendizaje abierto | **50 %** (19:30) | según n8b y n8c esta noche | aprende_barrer ×2 (+5), n8 ×2 (+5); n8b y n8c en cola |
| 9 autonomía / modelo de sí | 50 % | **55 %** (n9 MODESTO ×2; meta del director 90 %) | la lectura de sí presente causa el cruce de O3 (política escrita por un LLM); convivencia NO; n9b en cola |
| 10–13 | ~10 % | ~10 % | n10 NO SE LEE; n10b en cola |

## Decisiones del director de las 19:30 (AskUserQuestion; sus palabras: las tres opciones recomendadas)
- **Porcentajes FIJADOS:** nivel 7 → **78 %**, nivel 8 → **50 %**, nivel 6 → **60 %**. El 9 sigue en 50 % hasta su réplica.
- **v14.3 = v14.2 + reparación N del 7:** el examen del criterio v4 se prepara esta noche y corre el 24-sep. **Permiso escrito del director:
  si pasa serie y réplica, el coordinador lo congela** (manifiesto propio, v14.2 intacto) y le avisa.
- **`subida_n10b` corre mañana en la nube:** es su primera serie real, con un paquete ya auditado. No alcanzaba antes de las 00:00 en el PC.
- **Nube calibrada (19:35): FUNCIONA, bits idénticos al PC**; Pool 3 en la nube; scipy 1.17.1 fijada en `requirements.txt`.

## Decisiones pendientes del director (máx. 2)
1. **Nube, opcional (1 min):** pegar el *Setup script* de `NUBE.md` §1 en el menú del entorno. Crédito: 250 USD, vence el 5-nov-2026 y
   NO vale para Rutinas.
2. **24-sep:** leer los veredictos de la noche (9 réplica, v14.3, 9b, 6b, 8c, 8b) y el resultado del examen v4 del v14.3.

## Decisiones del coordinador en ausencia del director (23-sep; hora, opción, alternativa descartada, porqué)
- **19:15 — el paquete `tronco_v14_3` (frente 1) se adelanta en el Pool B, antes de n10b y n8b.** Alternativa: dejarlo al final (~23:30).
  Por qué: es el frente 1 del plan vigente, y n10b y n8b son cierres de frentes viejos. Ojo: este paquete es v14.2 + filtro con meta (n6) +
  boca TD heredada (APR). **No** lleva la reparación N del 7, porque el equipo arrancó antes de la orden del director de las 18:35. El
  v14.3 que se congele será v14.2 + N (FUNCIONA ×2) + lo que de este paquete pase serie y réplica, previo examen del criterio v4.
- **18:55 — `subida_n9c` se archiva sin correr.** Alternativa: correrla al final de la cola (52 min). Por qué: su creador espera NO (p 0.97),
  el auditor la puso en prioridad baja, y lo valioso ya salió sin correr (ERR-118). El director pidió pocos frentes; la CPU va al v14.3.
- **18:55 — los paquetes ya preregistrados de la cola se corren, pero no se abren tandas nuevas.** Por qué: cada preregistro sin dato es un
  frente abierto y correrlo lo cierra. Abrir tandas nuevas los multiplica.
- **17:50 — `subida_n6` se declara por la letra (HAY ALGO MODESTO), no por el subconjunto de la regla 10.** Leer el subconjunto como FUNCIONA
  sería elegir la lectura tras ver el dato. Además, en 3 semillas de la réplica la memoria incompleta sí rompió el rodeo.
- **17:05 — la mixta H y la réplica de generaciones que conviven quedan fuera de la cola.** El monocultivo dio un NO claro y la mixta no mueve
  ningún nivel. El mundo de convivencia se retoma dentro de ECO, sin fundadores repuestos.
- **16:50 — `subida_n10` NO SE LEE y no se corre su réplica.** Mover el ancla tras ver el dato lo prohíbe la regla 11; aunque se leyera, sólo
  daría +1. Queda ERR-116, y `subida_n10b` calibra el ancla sobre esa serie antes de usar semillas nuevas.

## Pedidos del director del 23-sep (palabras) y a dónde fueron
- *"en grupos de agentes de 3… subir desde el 5 hasta el 10 a 100 o acercarnos"*: paquetes `subida_n5..n10`; meta 100 %, mínimo 80 %.
- *"esperamos al 9 antes de fijar el 65; tiene que subir a 90"*, *"dale dos tandas"*: `subida_n9`, `subida_n9b` (la n9c se archivó).
- *"arranca el v14.3; que logremos lo que ayer hicimos, superándolo"*, *"mete la reparación del 7… congelando siempre"*: frente 1.
- *"soltar el bicho real en un ambiente gigante"*: JUACO-ECO, frente 2.
- *"lanza este además"* (memoria lenta con repaso): `subida_n8c_memoria_lenta`.
- *"haz un Frankenstein con todo… y lo sueltas en el mundo"*: `experimentos/frankenstein/`, EXPLORATORIO.
- *"agentes inteligentes investigadores… exploración, experimentación y creación de la AGI"*: `LABORATORIO.md` y el agente `juaco-investigador`.
- *"si hay una decisión difícil tómala, y me dejas comentado por qué"*: la sección de decisiones de arriba.

## Tronco y criterio
**v14.2** (tag `v14.2-tronco`, 18-sep) = v14.1 + B-5. Tiene 20 archivos congelados que se verifican con `python manifiesto.py --check`. Sin
`--check`, el script **reescribe** `MANIFEST.txt`: no se usa así. Criterio para candidatos: **`CRITERIO_TRONCO_v4.md`** (vigente; v3 retirado,
v2 historia). Candidato en construcción: **v14.3** (frente 1).

## Errores
Último: **ERR-121**. Del 23-sep:
- 114: enmienda V-M de `subida_n9` hecha tras el humo;
- 115: los runners aceptan banderas desconocidas;
- 116: ancla de `subida_n10` sin calibrar;
- 117: el toro del 21-sep no obligaba a rodear;
- 118: "persiste el carro" confunde fundadores repuestos;
- 119: ancla del paquete v14.3 movida tras el humo;
- 120: el humo de ECO no ejercitaba el juez actual;
- 121: P3c de ECO pasa a decidir (NO EVALUABLE).

Del 22-sep: 94–113 (HANDOFF §15.30). Siguiente libre: **ERR-122**. Regla derivada de ERR-87: "el último JSON de un prefijo" se cita siempre con prefijo y sello exacto.

## Datos, equipo y herramientas
- **Datos:** los runners nuevos escriben en `experimentos/<carpeta>/datos/` y los humos en `datos/humo/`. `datos/humo_no_registrado/` no
  entra a git. Índice de carpetas: `experimentos/INDICE.md` (al 23-sep).
- **Agentes** (en `.claude/agents/` del repo y en `~/.claude/agents` del PC):
  - `juaco-investigador` (Opus, nuevo): propone fichas;
  - `juaco-creador` (Opus) y `juaco-compilador` (Opus);
  - `juaco-auditor` (Sonnet, sólo lectura) y `juaco-cronista` (Sonnet);
  - `probador-haiku` y `explorador-haiku`.
- **Skills** (en `.claude/skills/`): `/juaco-estado`, `/juaco-bloque`, `/juaco-cierre`, `/juaco-err`, `/veredicto`, `/encargo`.
- **Reglas para los agentes:** ningún agente corre Pool, commitea, mata procesos ni ejecuta runners con `--serie` en ninguna forma (ERR-115).
  Sólo el coordinador lo hace. Tope de CPU: 2 Pools y 14 procesos en el PC (16 lógicos). Antes de lanzar se miran los procesos python vivos.
