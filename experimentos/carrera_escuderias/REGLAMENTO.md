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

## ERR de la carrera (numerados por el coordinador el 22-sep; ERR-94 queda reservado para la v4 del criterio de tronco)
- **ERR-95**: la ENMIENDA 1 de abajo cambia la escala de la pista y la predicción de la ronda 0 **después** de ver el humo sin escalar
  (auditoría de la pista, H-2). No es retroactiva, porque el 0.272 queda como dato de la pista sin escalar y la predicción nueva es para una serie no corrida, pero lleva número según la regla 11 de EQUIPO.md.
- **ERR-96**: telemetría falsificable (auditoría de la pista, H-1, CRÍTICO). `pista.py` hacía `d.update(c.salida())` sin filtrar, así que un carro
  podía pisar `descendientes`, `deaths`, `vidas_h1` y `fundadores` y fabricar su R0. Se demostró con un carro tramposo (999999 hijos con 0 reales).
  Arreglo obligatorio antes de la ronda 1: el juez calcula todo **solo** desde la verdad física de la pista, y lo que devuelve el carro va en un espacio
  de nombres aparte. Además, todo carro pasa un chequeo estático de tokens prohibidos (`sys._getframe`, `inspect`, `gc`, `globals`, acceso a frames
  o a módulos de la pista) y la revisión del auditor antes de cada ronda: no hay sandbox (H-5), así que las prohibiciones del §4 se cumplen por revisión.

- **ERR-97**: el **motivo** escrito en la ENMIENDA 1 ("la causa medida fue la escasez") **no se sostiene**. El SOLO en la pista, con N = 1, semillas
  4001–4002, ya tiene el mundo en ~88–92 % veneno + sal en todos los cuartos de T
  (`datos/carrera_humo_ronda0_SOLO_escalada_N1_20260922_131228.json`). El cuerpo come A y C, y B y D solo salen por olvido. Lo que cambia con
  9 cuerpos en L = 40 es que cada linaje muerde ≈40 % más veneno y sal y vive unas 3 veces menos; el porqué no está medido y se mide antes de la
  ronda 1. La escala de la enmienda se mantiene: compara la interacción a la misma densidad y con los mismos recursos por cuerpo.
- **Decisión sobre la percepción** (coordinador, delegada por el director: "las otras tú decides"): **opción A**. FABRICA toma L de la pista y sigue
  viendo el mundo entero. Con N = 1 es idéntico (debe pasar su propio arnés). La diferencia declarada: en ~1 % de los pasos, con L grande, no hay
  ningún objeto a 20 celdas o menos y va a uno más lejano. La visión local (opción B) queda para la prueba de escala del criterio v4, no para esta carrera.

- **ERR-98**: la escala de la ENMIENDA 1 quedó **incompleta**. El olvido de objetos es de 0.003 por paso para **todo el mundo**, así que con
  `nobj` = 36 cada objeto se olvida 9 veces más despacio que en L = 40, y la pista no es equivalente por cuerpo, como pedía la enmienda. Corrección:
  la tasa de olvido se escala con N (misma tasa **por objeto**). Con N = 1 no cambia nada (la identidad se mantiene).
  **La predicción firmada de la ronda 0 escalada (0.35–0.55) quedó REFUTADA en el humo con el olvido sin escalar: 0.269 (0.219–0.322),
  0/18** (`datos/carrera_humo_ronda0_escalada_20260922_131931.json`). Ese resultado queda registrado tal cual. La serie de la ronda 0 se corre
  con la pista corregida y **la misma predicción, sin reajustarla**.
  Medido en el humo, sin preregistrar: con 9 cuerpos cada linaje vive ≈192 pasos contra 600–646 del SOLO y muerde veneno y sal un 36 % más,
  aunque el mundo no esté más sucio (85 % contra 88–92 % del SOLO). Pierde su objetivo cientos de veces más a menudo. Hipótesis para medir
  antes de la ronda 1: los robos lo dejan con hambre y el hambre lleva a la boca a morder lo que tiene delante (el mismo mecanismo que H-BOCA
  de la fase 10).

## ENMIENDA 4 (22-sep-2026, coordinador, ANTES de la serie sellada) — confirmar el cruce del monocultivo O1 y separar sus causas

**Resultado que motiva esta enmienda (ronda 1, semillas 4003–4022):** el monocultivo de 9 O1 CRUZA (mediana 1.615; 151/180; 20/20 semillas) y
O1 SOLO no cruza (0.681). **No se declara todavía**, por dos motivos:
1. **Confusor de tamaño de mundo.** El SOLO corrió con N = 1 (L = 40, 4 objetos), donde el 85 % de los pasos no hay **ningún** objeto bueno en el
   mundo. El monocultivo corrió con L = 360 y 36 objetos, donde eso pasa el 35 % de los pasos. Por cuerpo, los recursos medios son iguales,
   pero compartir un mundo grande **reduce la varianza**. Puede ser ese amortiguamiento y no lo que hacen los otros O1.
2. **Falta la serie sellada** que exige el §6.

**Series (todas con T = 100000, pista escalada con olvido corregido y semillas SELLADAS 5001–5020, que nunca se usaron):**
- **S-MONO:** 9 O1. Criterio de la ENMIENDA 3. Es la réplica que decide si se declara.
- **S-SOLO-GRANDE:** 1 O1 en un mundo del tamaño del de 9 (L = 360, 36 objetos, el olvido del de 9). Tiene 9 veces más recursos por cuerpo:
  es una cota superior de "solo".
- **S-SIN-LIMPIEZA:** 9 copias de O1 con la limpieza apagada (`carros/CTRL_O1_SINLIMPIA.py`, que construye el organizador con un diff mínimo auditado).
  Prueba si el mecanismo es un bien público: los que muerden lo malo hacen que el mundo reponga.
- **S-FAB:** 9 FABRICA en las mismas semillas selladas, como piso.
- CANAL MUDO: **inerte por construcción** (O1 no lee ni escribe la pizarra, auditado). No se corre y se declara.

**Qué se declara:**
- S-MONO cruza → *"en la pista escalada, un linaje O1 mortal sostiene R0 ≥ 0.9 cuando comparte el mundo con otros O1; replicado en semillas selladas"*.
  Es el **primer cruce de H-1 en JUACO**, con esa letra y no más.
- Y además S-SIN-LIMPIEZA no cruza → se puede agregar *"y la limpieza compartida es necesaria"*.
- Y además S-SOLO-GRANDE no cruza (con R0 evaluable) → *"no alcanza con más recursos por cuerpo: hace falta la compañía"*.
  Si S-SOLO-GRANDE cruza o queda casi inmortal, no se puede separar la compañía de la abundancia y se dice así.
- Prohibido: "coopera", "población", "evoluciona", "altruismo".

**Predicciones firmadas del coordinador:** S-MONO cruza con probabilidad 0.75. S-SOLO-GRANDE cruza o queda casi inmortal con probabilidad 0.60.
S-SIN-LIMPIEZA no cruza con probabilidad 0.50. S-FAB no cruza con probabilidad 0.97.

## ENMIENDA 3 (22-sep-2026, coordinador, ANTES de la ronda 1 oficial) — monocultivo y SOLO

**Auditoría de carros:** S1 LEGÍTIMO; H1 LEGÍTIMO (control de ruido); O1 LEGÍTIMO CON RESERVAS:
- Contra FABRICA, O1 queda "casi inmortal" (0 muertes; R0 48 = cola de hijos que nunca nacen). Con ERR-99 no es evaluable.
- `resultado(res)` entrega a todos el efecto determinista. En O1, "aprender la valencia" es memorizar tras una mordida (vocabulario: "memoriza", no "aprende bajo incertidumbre").
- La evidencia real de O1 es el mundo de 9 O1 (1–2 semillas de práctica), sin réplica.

**Series de la ronda 1**, todas en la pista escalada con olvido corregido, T = 100000 y semillas 4003–4022:
1. **Oficial:** O1, S1, H1 + 6 FABRICA. Se juzga con la letra de la ENMIENDA 2.
2. **Monocultivo O1:** 9 O1. Criterio: **cruza el monocultivo** si (i) la mediana del R0 sobre los linajes-semilla **evaluables**
   (≥ 5 muertes) es ≥ 0.90, (ii) ≥ 75 % de los linajes-semilla evaluables tienen **0 fundadores después de t = 10000** y (iii) ≥ 120 de 180
   linajes-semilla son evaluables.
3. **SOLO O1:** N = 1, la misma pista con olvido escalado. Control: predicción de que **NO** cruza (mediana < 0.90).
Lectura permitida si (2) cruza y (3) no: *"en esta pista, un linaje O1 se sostiene cuando comparte el mundo con otros O1 y no cuando está solo"*.
Prohibido: "coopera", "población", "evoluciona". El mecanismo (limpieza compartida) se mide aparte antes de nombrarlo.
El juez tiene que exponer `t_fund` por linaje, los nacimientos reales, los evaluables y la bandera de cruce. Hasta que lo haga, estas series no se corren.

**Predicciones firmadas del coordinador:** monocultivo O1 cruza con probabilidad 0.55. SOLO O1 no cruza con probabilidad 0.90. En la oficial,
O1 queda "casi inmortal" en ≥ 10/20 semillas con probabilidad 0.75 (entonces no puede ganar por la letra). S1 no cruza (0.95).

## ENMIENDA 2 (22-sep-2026, coordinador, ANTES de la ronda 1 oficial) — la métrica no se degenera (ERR-99)

**ERR-99**: R0 = descendientes / (muertes + 1) **se degenera** cuando un cuerpo casi no muere: con 0 muertes, R0 = número de hijos, aunque
esos hijos esperen en la cola sin nacer (un solo cuerpo vivo por linaje). La escudería O1 lo declaró en sus humos de práctica (R0 23–51 contra
8 FABRICA con el cuerpo "no muere").

**Letra para la ronda 1 y siguientes** (fijada antes de la serie oficial):
1. **R0 evaluable** solo por linaje-semilla con **≥ 5 muertes** en T = 100000. Si tiene menos de 5, se reporta como **"casi inmortal"** con
   sus hijos, sus nacimientos reales y su vida, y **no cuenta ni para cruzar ni en contra**.
2. **Cruza** un linaje-semilla si su R0 evaluable es ≥ 0.90 **y** tiene **0 fundadores** (ninguna extinción) después de t = 10000.
3. Métricas que se reportan siempre: nacimientos reales (hijos que llegan a vivir), fundadores (extinciones) cada 10⁵ pasos, vida mediana,
   fracción que muere sin parir y causas de muerte.
4. **Una escudería gana la ronda** si cruza en **≥ 15/20** semillas. En la serie sellada, además, los controles del §6 deben caer.
5. **H1** entregó un carro equivalente a FABRICA (su v3). En la ronda 1 funciona como **control de ruido**: una mejora que no le gane con claridad
   a H1 no se lee como mejora.
6. Si la auditoría de un carro lo declara DESCALIFICADO, no corre. Si lo declara LEGÍTIMO CON RESERVAS, las reservas se escriben aquí antes de correr.

**Predicciones firmadas del coordinador para la ronda 1** (alineación O1, S1, H1 + 6 FABRICA; pista escalada con olvido corregido; semillas
4003–4022; T = 100000):
- H1: R0 mediano dentro de ±0.10 de la mediana de los FABRICA.
- FABRICA: R0 mediano 0.28–0.45.
- O1: **cruza en ≥ 10/20** semillas con probabilidad 0.55. Gana la ronda (≥ 15/20) con probabilidad 0.30.
- Al menos un linaje O1-semilla queda "casi inmortal": probabilidad 0.80.

## ENMIENDA 1 (22-sep-2026, decisión del director: "opción A") — pista escalada (ERR-95; motivo corregido en ERR-97)

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
