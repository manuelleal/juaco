# Carrera de escuderías — REGLAMENTO (borrador v0, 22-sep-2026)

Rama: `carrera-escuderias` (worktree `PROYECTOS\JUACO\carrera`). La línea principal (`main`) no se toca.
Idea del director (22-sep): nueve equipos de agentes, cada uno con su bacteria ("carro"), en la misma pista,
a ver si con la interacción entre bacterias y los arreglos de los equipos se cruza el umbral de R0 que nos frena.
Encaja como candidato al **bloque 3 de la fase 9** ("más de un cuerpo a la vez").
Estado: **APROBADO por el director el 22-sep-2026 ("córrelo")**, con las opciones recomendadas: canal público (pizarra) + se ven entre ellos;
5 rondas de 20 semillas de práctica; ganador confirmado con 20 semillas selladas.

## 1. Meta

- **Umbral a cruzar:** R0 ≥ 0.90 (H-1, ERR-62). Meta fuerte: R0 ≥ 1.0 en ≥ 15/20 semillas selladas (= M-1 / M10-1).
- R0 de un linaje = descendientes / (muertes + 1), igual que `nivel09_cuerpo_nuevo/corre_f9.py:193-207`.
- Referencia (bloque 2, réplica 1601-1620, un cuerpo a la vez): REL 0.395 (acum 1: 0.483);
  ORÁCULO 0.458 (acum 1: 0.557). **Ni la memoria perfecta cruza:** faltan ~0.4 que no salen de recordar el veneno.
- Pista suelta: el borrador C de anoche (`carrera_fase10/C/C_E1.log`) reporta RENACE con R0 0.40-0.95. Sin auditar; se revisa antes de la ronda 1.

## 2. El carro de fábrica (muestra más actualizada)

`experimentos/nivel09_cuerpo_nuevo_b2/organismo_f9c.py`, brazo REL (`nodo_rel=1`), cuerpo `CUELLO_MIN + MED2`,
`muerte_real=1`, `hereda='nada'`, `dote=0.6`, `nodo_k=20`, `nodo_lee=50`. Gemelo numba `organismo_f9c_rapido.py` (arnés ×51).
Todos los equipos arrancan con este mismo carro.

## 3. La pista (se construye; es lo único que falta de ingeniería)

- Mundo vivo actual sin cambios: L = 40, `nobj = 4`, A comida (+0.8), B veneno (−0.4), C agua, D sal,
  `costo = costo_a = 0.001`, reproducción `rep_X = 500`, `rep_umbral = 1.0`, `dote = 0.6`.
- **Novedad:** hasta 9 cuerpos vivos **a la vez** en el mismo mundo (hoy hay uno solo y los hijos esperan en fila,
  `organismo_f9c.py:469-547`). Lo que uno come deja de estar para los otros. Cada linaje conserva su propia fila de hijos.
- **Ancla de identidad (obligatoria antes de todo):** con un solo carro, la pista reproduce `organismo_f9c` **bit a bit**
  (mismo consumo del rng del mundo). Sin esa identidad, no hay carrera.
- **Canal de interacción (fijo, igual para todos):** cada cuerpo puede leer lo que los otros tienen a la vista y un canal
  público de la pista (pizarra con cupo fijo). Qué escribe cada uno en el canal lo decide su equipo; el canal no.
- Extinción: igual que hoy, si un linaje se queda sin hijos, el mundo pone un fundador y se cuenta.

## 4. Las escuderías

| Equipo | Modelo | Carro |
|---|---|---|
| O1, O2, O3 | Opus | `carros/O1.py` ... |
| S1, S2, S3 | Sonnet | `carros/S1.py` ... |
| H1, H2, H3 | Haiku | `carros/H1.py` ... |

**Pueden cambiar (solo su archivo):** memoria, qué y cómo heredan los hijos, conducta, cuándo reproducirse (respetando
el costo), qué escriben en el canal y cómo leen a los otros.

**Prohibido (descalifica):** tocar la pista, los costos de vida, la aparición de objetos, las semillas, el juez;
leer el rng del mundo o la tabla verdadera (eso es el ORÁCULO, que es un control y no un carro); editar el carro de otro equipo.

## 5. Formato: rondas

1. **Ronda 0 (línea base):** 9 carros de fábrica en la pista. Si la interacción sola ya cambia R0, se sabe desde el inicio.
2. **Rondas 1 a 5:** cada ronda es una carrera de 20 semillas de práctica (4001-4199), con todos los carros a la vez.
   Durante la carrera nadie toca nada. Después, cada equipo recibe su telemetría (R0, vida, causa de cada muerte,
   qué leyó y qué escribió) y puede cambiar su carro. Cada cambio queda en su bitácora con el porqué.
3. **Tope:** 5 rondas. No hay reanimaciones fuera de ronda.

## 6. Declarar ganador (solo con repetición)

El carro que cruce en práctica se **congela** y corre con **20 semillas selladas (5001-5020)** más estos controles, que deben fallar:

| Control | Qué prueba |
|---|---|
| SOLO: el campeón sin los demás carros (un cuerpo) | ¿cruza por la interacción o por el carro solo? |
| CANAL MUDO: lo que lee del canal, barajado o apagado | ¿es el contenido de la interacción lo que ayuda? |
| RIVALES DE FÁBRICA: el campeón contra 8 carros REL | ¿cruza en cualquier pista o solo con sus aliados? |
| NADA: cuerpo vacío | piso |

Se declara solo si R0 ≥ 0.90 en ≥ 15/20 selladas y los controles caen como se predijo. Vocabulario prohibido hasta medirlo:
"población", "generación", "evoluciona", "coopera".

## 7. Juez y documentación

- `juez.py` fijo, commiteado antes de la ronda 0. Los equipos no lo leen por dentro ni lo editan.
- Por equipo: `bitacoras/<equipo>.md` (cambio, porqué, resultado). Del organizador: `BITACORA_CARRERA.md` por ronda.
  Al final: `INFORME.md`. Los errores de instrumento se registran como ERR.

## 8. Riesgos conocidos

- La competencia por la comida **baja** R0 (lo advirtió el preregistro de C, `carrera_fase10/C/PREREGISTRO_C.md:15-24`).
  La interacción tiene que dar más de lo que quita.
- Los equipos Haiku pueden no alcanzar a diseñar. Eso también es un dato.
- Si se cae la API de Opus (como el 21-sep), la ronda se repite completa, sin medias rondas.

## ENMIENDA 1 (22-sep-2026, decisión del director: "opción A") — pista escalada

**Motivo.** El humo de la ronda 0 (9 FABRICA en L = 40, `nobj = 4`; `datos/carrera_humo_ronda0_20260922_124440.json`) dio R0 por linaje
0.272 contra 0.44–0.52 de un carro SOLO, y la causa medida fue la **escasez**: con 9 cuerpos, la comida y el agua se agotan y el mundo queda
~86 % veneno y sal. Así, la carrera mediría escasez y no interacción.

**Cambio.** Con N carros, la pista usa **L = 40·N y `nobj` = 4·N**: la misma densidad y los mismos recursos por cuerpo que el mundo de un
solo cuerpo. Con N = 1 es exactamente la pista original, así que la identidad con `organismo_f9c` se conserva (el arnés debe volver a pasar).
Todo lo demás del reglamento queda igual (costos, aparición de objetos, reproducción, recompensas).

**Condición técnica.** Si la percepción o el movimiento del carro de fábrica dependen de L o de `nobj` (por ejemplo, si ve el anillo entero y
recibe 9 veces más objetos), se reporta **antes** de correr y se decide aparte. No se adapta el carro sin avisar.

**Predicción firmada (coordinador, antes de correr).** Ronda 0 en la pista escalada, 9 FABRICA: R0 por linaje con mediana **0.35–0.55**, es
decir, cerca del SOLO. Si baja de 0.30, queda un efecto de competencia que no es escasez y se estudia antes de la ronda 1. Si pasa de 0.60,
la sola presencia de otros cuerpos ayuda (se verifica con el control SOLO en la misma pista).

**Además, fijado:** `rep_acum = 0` (la referencia 0.395). El control SOLO se corre **en la pista**, no con el original. La pizarra se guarda
completa aparte de la telemetría.

## 9. Plan de construcción

1. Pista para varios cuerpos + arnés de identidad con un carro (creador Opus + compilador para el gemelo).
2. Juez + ronda 0 con 9 carros de fábrica (humo de un proceso y después serie).
3. Soltar a las 9 escuderías.
