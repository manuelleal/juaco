# PREREGISTRO — nivel 9, segunda tanda: ¿la predicción de sí APRENDIDA por el organismo es causal? (subida_n9b, 23-sep-2026, creador)

Misión: llegar a la AGI por este camino. Escrito ANTES del arnés de las lesiones, del humo y de cualquier serie.
Carpeta: `experimentos/subida_n9b/`. Sólo se escribe aquí. `carrera_escuderias/`, `aprende_barrer/`, `subida_n9/` y los
congelados sólo se leen.

## 0. Por qué este bloque (y no otro)
La primera tanda (`subida_n9`) lesiona a **O3**, cuya política escribió un LLM: mide si *leerse* es causal, no si el
organismo tiene un modelo de sí propio. El coordinador pide que la autonomía la sostenga el **organismo propio**, con un
modelo de sí **que prediga** y cuya lesión cueste. El único carro de JUACO que cumple las tres cosas hoy, con réplica, es
**APR** (`aprende_barrer`): el cerebro REL de FABRICA (el organismo del tronco) + una corrección de la boca aprendida por TD
(regla local, sin retropropagación), heredada por el linaje. APR gana a FABRICA 20/20 en la serie 8101–8120 (+0.051) y
20/20 en la réplica 8121–8140 (+0.049), sin cruzar H-1 (R0 0.385).
Uno de los seis rasgos con que APR decide es una **predicción de su propio estado**: `post = min(E + dE_k, Ag + dAg_k)`, el
nivel que tendría su necesidad más baja *si* mordiera la letra k, con dE_k y dAg_k = lo que el **linaje sintió** al morder
k (memoria aprendida del efecto de cada letra sobre su propio cuerpo). Es un modelo directo (forward model) del cuerpo,
aprendido y no escrito. Nadie midió si la ventaja de APR pasa por esa predicción o por la contención general (sesgo y
ventana de parto). En los pesos medianos de APR (8101–8120, sólo lectura) la corrección al logit tiene +2.8 por unidad de
`post` y −2.7 por unidad de `u`: la ventaja *podría* ser "contenerse cuando la letra golpea la necesidad que falta"
(predicción de sí) o sólo "contenerse" (el sesgo −1.4 y la ventana −4.2 logit pesan más). Este bloque lo separa.
Descartados: bloque 5 del explorador (O3_DECIDE_MORIR: otra política escrita a mano); predictor de ΔE dE5 portado a la pista
(mecanismo nuevo grande, candidato a tronco pendiente del director: no se mezcla); APR_AZAR (es la P9 pendiente de
`aprende_barrer`, carpeta ajena).

## 1. Hipótesis
- **H-PRED (principal):** la ventaja de APR sobre FABRICA depende de que el organismo **prediga el efecto de la letra sobre su
  propio estado**. Si el rasgo `post` se reemplaza por su estado actual (`post = u`: "morder no me cambia"), APR pierde la ventaja.
- **H-CRUZ (secundaria):** si la predicción es de la **necesidad equivocada** (el efecto sentido de la letra aplicado a la otra
  necesidad), APR también pierde, aunque el aprendizaje sigue y podría re-aprender a usar el rasgo cruzado.
- **Control de especificidad (H-MUNDO):** la misma operación ("la otra necesidad") aplicada a los rasgos **del mundo** (qué es
  bueno cerca, a qué distancia) **no** debe costar lo mismo. Si cuesta igual, lo que importa es la entrada en general, no la
  predicción de sí.

## 2. Mecanismo mínimo y memoria nueva
**Ningún mecanismo nuevo; memoria nueva en el organismo: CERO.** Son lesiones del instrumento sobre APR, dos perillas:
- `LES_PRED = None | 'plana' | 'cruz'`: `plana` → `post = u`; `cruz` → `post = min(E + dAg_k, Ag + dE_k)` (efecto sentido
  aplicado a la otra necesidad; para las letras malas de este mundo es exactamente el efecto de la otra letra mala). Sin rng.
- `LES_MUNDO = False | True`: el conjunto "bueno" que dan `g0` y `dist` se calcula para la necesidad NO activa. Sin rng.
- Todo lo demás de APR queda igual: la boca de FABRICA, el TD, la herencia de Q, el mismo uniforme. La lesión entra sólo
  por el vector de rasgos φ; con Q = 0 (`ALFA_Q = 0`) las tres lesiones son APR bit a bit (lo verifica el arnés).
- Telemetría de la lesión (no puntúa): decisiones, media de `post` real y usado, decisiones donde cambia, caídas predichas.

## 3. Instrumento y anclas
- Pista, juez y chequeo estático de la carrera (sólo se importan; `P.CARROS` apunta a `subida_n9b/carros`):
  `pista.py` 9f47c65e438e0ff4, `juez.py` 6a68f640a7832f12, `revisa_carro.py` 1c8a789f7427ab96, `organismo_f9c.py`
  9dd1fb91ecec35ae. Son los shas con los que corrió la réplica 8121–8140 de APR.
- `construye_n9b.py`: anclas en bytes (CRLF) sobre `carrera_escuderias/carros/APR.py` (4402aa5142065c72). Carros:
  `APR` (copia, mismo sha), `APR_LES_OFF` (perillas apagadas), `APR_LES_PLANA`, `APR_LES_CRUZ`, `APR_LES_MUNDO`,
  `FABRICA` (copia, 2ebee3e99ea5a33a).
- Arnés `identidad_n9b.py` (N/N en `identidad_n9b_salida.txt`): shas; construcción reproducible; chequeo estático de todos;
  identidad corta del juez; **APR_LES_OFF == APR bit a bit** en toda la salida de `pista.run` (N = 9, dos semillas); APR con
  OPCION 0 == FABRICA; con `ALFA_Q = 0` las tres lesiones == APR; lesiones no inertes con Q aprendido; entrada del runner
  campo a campo contra `juez.tarea` (regla 14); el runner aborta ante banderas desconocidas, `--help` y abreviaturas (ERR-115).
- Mundo: el de APR en `aprende_barrer`: monocultivo de 9, pista escalada (L = 360, 36 objetos), `pizarra=1, rep_acum=0,
  escala=1, mundo_n=None`, fundador por defecto, T = 100000. Reserva **ERR-104** declarada: en esta pista morder repone al
  instante una letra al azar (el mundo no tiene capacidad de carga). No afecta la comparación pareada (todos los brazos en el
  mismo mundo), sí impide leer R0 absoluto como "persistiría con recurso limitado".
- Medida (la de `corre_aprende`): por semilla, mediana del R0 de los 9 linajes (`juez.resumen_linaje`, sólo física); pareado
  por semilla. ENMIENDA 3 (`juez.criterio_mono`) para "cruza".

## 4. Qué significa "pierde" (fijado antes)
Un brazo X **pierde** contra APR en una serie si APR supera a X en **≥ 15/20 semillas** y la diferencia mediana por semilla
es **≥ 0.025** (la mitad de la ganancia replicada de APR sobre FABRICA, 0.049–0.051). Se reporta al lado, sin decidir: la
fracción de la ganancia perdida por semilla, (APR − X) / (APR − FABRICA), su mediana; R0 real (ENMIENDA 5); causas de
muerte; contención (quitadas por oportunidad) y la telemetría de la lesión.

## 5. Predicciones firmadas (creador, antes del arnés de las lesiones y del humo)
| código | predicción | prob. |
|---|---|---|
| P1 (ancla) | APR > FABRICA en ≥ 15/20 con diferencia mediana ≥ 0.03; APR mediana R0 en [0.36, 0.42], FABRICA en [0.30, 0.37] | 0.85 |
| **P2 (puede fallar; la doy por REFUTADA con p 0.65)** | **APR_LES_PLANA pierde (§4)** | 0.35 |
| P3 | APR_LES_CRUZ pierde (§4) | 0.30 |
| P4 (control) | APR_LES_MUNDO **no** pierde | 0.80 |
| P5 | APR_LES_PLANA > FABRICA en ≥ 15/20 (conserva parte de la ganancia) | 0.70 |
| P6 | ningún brazo cruza la ENMIENDA 3 | 0.97 |
| P7 | fracción mediana de la ganancia que pierde PLANA en [0.0, 0.5] | 0.65 |
Base: pesos medianos de APR en 8101–8120 y 8121–8140 (sólo lectura): sesgo −1.4 y ventana −4.2 logit pesan más que el
término de la predicción (≈ −1.1 logit sólo cuando la letra golpea la necesidad más baja). Por eso creo que la ventaja es
sobre todo contención general y que H-PRED cae.

## 6. Criterio (por la letra; serie 13501–13520 Y réplica 13521–13540 con el mismo veredicto)
- **NO EVALUABLE:** APR no gana a FABRICA (≥ 15/20, dif ≥ 0.03) en alguna de las dos series: no hay ganancia que lesionar.
- **FUNCIONA:** APR_LES_PLANA pierde **y** APR_LES_MUNDO no pierde, en las dos series.
  Vocabulario: *"la ventaja que el linaje aprende sobre FABRICA pasa por una predicción de su propio estado aprendida de lo
  que sintió: sin esa predicción la pierde; quitar la misma cantidad de información del mundo no cuesta igual"*.
- **HAY ALGO MODESTO:** (a) PLANA y MUNDO pierden las dos (depende de sus entradas, no específicamente de predecirse), o
  (b) sólo CRUZ pierde, en las dos series (una predicción de sí equivocada cuesta; su ausencia no). Se dice cuál.
- **NO:** PLANA y CRUZ no pierden en las dos series: *"la ventaja aprendida de APR es contención general; no depende de
  predecir su propio estado"*.
- V-M (condición de lectura de CRUZ, se imprime, no decide): si |media de `post` usado − real| ≤ 0.10, CRUZ se lee
  *"contenido cruzado con la misma media"*; si no, *"cruzado y sesgado"*. PLANA está sesgada por construcción (`u ≥ post`).
Prohibido: "sabe", "quiere", "se imagina", "es consciente", "coopera", "población", "evoluciona". Permitido: "predice su
propio estado", "modelo del efecto de las letras sobre su cuerpo, aprendido de lo que sintió". Los rasgos los eligió un LLM
(diseñador); lo aprendido son los pesos y el efecto de cada letra.

## 7. Qué lo refuta
H-PRED: PLANA no pierde en alguna de las dos series. Especificidad: MUNDO pierde. Instrumento: identidad OFF == APR falla,
coherencia física < 100 %, t_fund reconstruible < 100 %, escrituras en la pizarra > 0, o la mini identidad del runner falla.

## 8. Semillas (NUEVAS; grep en `bundle` y en los worktrees `anclado, aprende, carrera, convive, criterio, escuela,
exploracion, fanin, respaldo, sandbox`: 135xx no aparece como semilla en ningún .py/.md, ni `"seed": 135xx` / `_s135xx` /
`semilla 135xx` en .json/.log, ni en nombres de archivo)
Serie **13501–13520** · réplica **13521–13540** · humo **13591** (práctica 13581–13598) · arnés **13592–13594** · mini
identidad del runner **13599**.

## 9. Puntos del nivel 9 (propuesta; decide el director). Hoy 50 %, meta 90 %.
| n9b \ subida_n9 | n9 FUNCIONA (+10) | n9 MODESTO (+3..+5) | n9 NO (0) |
|---|---|---|---|
| **FUNCIONA** | +8 → ~68 % | +8 → ~62 % | +8 → 58 %: la única evidencia de modelo de sí sería la del organismo propio |
| **MODESTO** | +3 → ~63 % | +3 | +3 |
| **NO** | 0 (el modelo de sí queda en la política escrita a mano) | 0 | 0, y el nivel 9 queda en 50 % |
Honesto: **las dos tandas no llevan el nivel 9 a 90 %** con ningún resultado. Lo que falta para 90: (i) un linaje cuyo
cerebro sea el organismo propio y **cruce H-1** (APR queda en 0.385; ni el oráculo cruza en la pista v1 sin limpieza); (ii) el
modelo de sí causal en **ese** linaje; (iii) que sobreviva a un cambio de reglas del mundo (T-C). Este bloque aporta (ii) en
un linaje que no cruza.

## 10. Enmiendas
(ninguna al escribir; toda enmienda posterior al humo que toque un umbral lleva "candidato a ERR")
