# PREREGISTRO — Bloque 6 (RAMA exploratoria): modelo de sí mismo mínimo = predictor de ΔE y sorpresa que modula `eta`

**17 sep 2026. Diseñador de preregistros (Opus), equipo JUACO. Escrito ANTES de correr nada.**
**Rama exploratoria, 10 semillas: nada se cierra aquí.** Lo que salga no cambia el tronco (v13 sigue siendo el tronco)
y no se declara con vocabulario nuevo: **sólo se mide, no se declara** (regla 6 de `registro/EQUIPO.md`). Si pasa, el
paso siguiente es una réplica preregistrada en semillas nuevas (11–20), no un anuncio.

Origen del encargo: `registro/PLAN.md`, bloque 6 del plan del día 6; `registro/investigacion/nivel9_autonomia.md` §3
(adaptividad medida, no declarada; control obligatorio que pueda fallar) y §7 (mundo, medidas, refutación, controles);
`registro/REFLEXION_agi.md` §1 y §3 (aprender de las propias consecuencias; la parte del sistema que no puede mentir).
Antecedente citado como **dato, no instrucción** (regla 8): Sterling (allostasis: estabilidad mediante cambio,
regulación **predictiva**), Man y Damasio 2019 (motivación desde el cuerpo), Oudeyer, Kaplan y Hafner 2007 (el error de
predicción como señal interna). Ninguno se replica aquí: se toma sólo la idea de **usar el error de la propia
predicción como señal**.

---

## 1. Pregunta única y medible

> **¿La sorpresa (el error de la predicción que el organismo hace de su propia ganancia de energía) acelera la
> recuperación tras una inversión de la regla del mundo (`invertir_en = T/2`, el mundo invertido de N1), sin dañar la
> retención (`bateria_v13`) ni la generalización (`bateria_generaliza`, px0/azar)?**

Una sola pregunta. Todo lo demás de este archivo son medidas, controles y guardas de esa pregunta.

## 2. Mecanismo (qué se añade, exactamente)

Sobre el tronco `organismo/organismo_v13.py` (sha `cc8b16b492d4d324`, **congelado, no se toca**) se añade **una tercera
lectura lineal**, que no decide nada, sólo predice:

- **Predictor de ΔE** (`Wpe` sobre los 6 píxeles de la retina, `Wke` sobre las NKMAX celdas de Kenyon; ambos con signo,
  recortados a ±`clip_e`, inicializados a 0):

  ```
  ΔE_pred(P) = Wpe @ P + Wke @ kenyon(P)
  ```

  Es "como la vía lenta, pero prediciendo ΔE en vez de R", más una copia sobre la vía rápida (las 3 celdas del código),
  para que pueda predecir tanto por regla (píxeles) como por caso (celdas).

- **Objetivo de la predicción:** `ΔE = E_VAL[valencia]` (+0.8 comida, −0.4 veneno), la energía **que rinde el bocado**.
  **Decisión declarada y su motivo:** NO se usa la ΔE *realizada* `min(E+E_VAL,1.5) − E`, porque el techo de energía
   introduce en el objetivo una componente que depende de `E` — una variable que la retina no ve —; el predictor no
  podría anularla nunca y la sorpresa quedaría permanentemente alta y **confundida con la saciedad**. Con el objetivo
  nominal, la sorpresa tiende a 0 cuando el patrón está aprendido y se dispara cuando el mundo cambia, que es lo que se
  quiere medir. Queda escrito para que la alternativa no se elija después de ver datos.

- **Aprendizaje del predictor** (sólo en el paso en que **muerde**, que es cuando ΔE existe; regla delta, tasa propia):

  ```
  e   = ΔE − ΔE_pred                (error con signo)
  sorpresa = |e|
  Wpe ← clip(Wpe + eta_pred · e · P,           −clip_e, clip_e)
  Wke ← clip(Wke + eta_pred · e · kenyon(P),   −clip_e, clip_e)
  ```

- **Modulación de la tasa de aprendizaje** (la señal interna):

  ```
  eta_ef = eta · (1 + k_sorpresa · sorpresa)
  ```

  `eta_ef` sustituye a `eta` **sólo** en la actualización de valor de la **vía rápida** (`Wp`/`Wn`) y, por coherencia,
  en el predicado de truncamiento `_trunca` que instrumenta el techo (si no, la instrumentación mentiría).
  **NO se modula** `eta_s` (vía lenta: es la que consolida la regla) ni `eta` de las patas (`Wl`, que se actualiza en
  todos los pasos y exigiría un estado de sorpresa persistente). Declarado aquí para que no se amplíe después.

- **Lo que el predictor NO hace:** no entra en la decisión de la boca (`Vb = alpha*_wt + hambre_boca*hambre + .5` queda
  intacto), no entra en `valor(P)`, no consume el RNG del organismo y no cambia ningún otro camino de código. De ahí
  sale la identidad I2 de §4, que es lo que da derecho a llamar "sólo mide" al brazo V13+PRED.

**Perillas nuevas** (todas con el valor apagado por defecto): `eta_pred=0.0`, `k_sorpresa=0.0`, `clip_e=3.0`,
`buf_sorpresa=20`, `sorpresa_barajada=False`, `vent_sorpresa=2000`.

**Valores usados, y por qué no están ajustados:** `eta_pred = 0.03` = **el mismo `eta` del tronco** (no se buscó);
`k_sorpresa = 1.0` (la escala de ΔE es de orden 1 por construcción: `E_VAL ∈ {+0.8, −0.4}`, luego `sorpresa ≤ 1.2` y
`eta_ef ≤ 2.2·eta`). Si el resultado exigiera otro valor, eso es un experimento nuevo con semillas nuevas, no un ajuste.

## 3. Instrumento

`experimentos/nivel9_allostasis/organismo_v13a.py`, **construido por anclas** (conteo exacto, aborta si un ancla no
aparece el número de veces esperado) desde `organismo/organismo_v13.py` (sha `cc8b16b492d4d324`) por
`construye_allostasis.py`. **No se edita a mano.** El mismo constructor genera
`experimentos/nivel9_allostasis/organismo_v13ag.py` desde `experimentos/v13_dos_vias/organismo_v13g.py`
(sha `2a80e125f8593bf2`) con **las mismas anclas**, para poder medir generalización en modo regla (§6, medida M5).

## 4. Identidades (se corren PRIMERO; si fallan, no hay experimento)

- **I1 — apagado ≡ tronco:** `organismo_v13a.run(eta_pred=0, k_sorpresa=0, ...)` == `organismo_v13.run(...)` en
  **todas las claves de v13**, en **semillas 1–6 × 3 escenarios** {base, `invertir_en=50000`, `nuevo='C'`}.
- **I2 — el predictor sólo mide:** `organismo_v13a.run(eta_pred=0.03, k_sorpresa=0, ...)` == `organismo_v13.run(...)`
  en **todas las claves de v13**, mismas 6 semillas × 3 escenarios. Esta identidad es la que convierte a V13+PRED en un
  **medidor** y no en una intervención; si falla, el predictor está tocando la dinámica y el brazo PRED no vale.
- **I3 — modo regla:** `organismo_v13ag.run(eta_pred=0, k_sorpresa=0, mundo='regla', regla='px0')` ==
  `organismo_v13g.run(mundo='regla', regla='px0')` en todas las claves, semillas 1–3.

Las claves nuevas (§6) quedan fuera de la comparación por construcción: sólo se comparan las claves que devuelve el
tronco.

## 5. Brazos, mundo y semillas

| brazo | perillas | qué es |
|---|---|---|
| **V13** | `eta_pred=0, k_sorpresa=0` | el tronco, línea base |
| **V13+PRED** | `eta_pred=0.03, k_sorpresa=0` | predictor encendido **sin modular**: sólo mide la sorpresa (por I2, conducta idéntica a V13) |
| **V13+SORPRESA** | `eta_pred=0.03, k_sorpresa=1.0` | la hipótesis |
| **V13+RUIDO** (control) | `eta_pred=0.03, k_sorpresa=1.0, sorpresa_barajada=True` | misma magnitud de modulación, **sorpresa barajada en el tiempo** con RNG propio (`default_rng(seed+900000)`) |

**Mundo:** el anillo del tronco, escenario E2 alargado: `T = 200000`, `invertir_en = 100000` (= T/2). Los cuartos del
tronco quedan alineados con el evento: Q1, Q2 antes de la inversión; Q3, Q4 después.

**Semillas: 1–10** (rama; 10 semillas no cierran nada). La réplica, si la hay, será en 11–20 y se preregistra aparte.

**Cómo se baraja la sorpresa (control RUIDO), exactamente:** ventana móvil de `buf_sorpresa` bocados (**10** en el
experimento; ver ENMIENDA 2, §10 ter). En cada bocado se empuja la sorpresa real a la ventana y, si la ventana está
llena, se **extrae al azar** (RNG propio) un elemento de ella y **ése** es el que modula `eta`. Durante el llenado
inicial (los primeros `buf_sorpresa` bocados, todos en Q1) se emite el valor corriente. Consecuencia buscada: **la misma
cantidad de aprendizaje extra en el mismo tramo, repartida sobre bocados equivocados**.

**Alcance declarado del control:** RUIDO controla **"qué bocado"** recibe el impulso, no **"en qué tramo del experimento"**
(una ventana de 20 bocados ≈ 200–400 pasos, muy corta frente a la ventana de recuperación). Si SORPRESA gana a V13 pero
**no** gana a RUIDO, la lectura preregistrada es: *lo que acelera es la cantidad de actualización tras el cambio, no la
sorpresa* — y se registra así, sin adornos.

## 6. Medidas

Del tronco (ya existen): `W`, `comp`, `mord`, `vis`, `deaths`, `splits`, `celdas`, `solap`, `W_lenta`.

Nuevas del instrumento:

- **M1 `t_ext_B`** — primer paso `t ≥ invertir_en` con `valor('B') ≥ 0` (B pasa a ser comida al invertir). Es el
  equivalente del `t_ext_B` de `experimentos/etapa5_comunicacion/mundo_social.py` (líneas 156–157), calculado aquí con
  el mismo criterio. **Censurado = `T`** si nunca ocurre. Se informa `t_ext_B − invertir_en` (pasos de recuperación).
- **M2 `mord_post`** — bocados **tras la inversión**, separados en `veneno` (el patrón A, ahora venenoso) y `comida`;
  y `deaths_post`. El veneno mordido tras la inversión es el coste conductual de recuperarse.
- **M3 `sorpresa_media[q]`, `error_pred[q]`, `eta_media[q]`, `bocados[q]`** — por cuarto: media de `|e|`, media de `e`
  **con signo** (para ver sesgo del predictor), media del factor `eta_ef/eta`, y número de bocados (denominador).
  Además, en ventana fina alrededor del evento (`vent_sorpresa = 2000` pasos): `sorpresa_pre`, `sorpresa_post`,
  `eta_pre`, `eta_post`, `n_pre`, `n_post` — porque promediar un cuarto entero de 50 000 pasos diluye el salto.
- **M4 retención tipo `bateria_v13`** — las SEIS etapas del examen del tronco (`E1, E2, E2I, E2J, E2K, E2L`, T=100 000,
  evento en 50 000) con **los criterios `CRIT` de `organismo/bateria_v13.py` (sha `1a027bcb37eb536e`) importados tal
  cual**, corridas con las perillas de cada brazo. No se reescribe ningún umbral.
- **M5 generalización `bateria_generaliza` (px0/azar)** — **es viable**: se hace con `organismo_v13ag.py` en
  `mundo='regla'`, `T=200000`, `eta_s=0.015`, `puerta=3`, reproduciendo **literalmente** la fórmula de G1 (acierto de
  signo a priori sobre patrones nunca vistos) y G2 (`BA_pb` al primer encuentro) de `organismo/bateria_generaliza.py`
  (sha `46772f5a582872c8`), con sus umbrales. **No se modifica `bateria_generaliza.py`** (es una batería compartida): el
  runner importa `split_regla` del instrumento y calcula G1/G2/cobertura con el mismo código, citado en el script. Si el
  coordinador prefiere, añadir `organismo_v13a` a su `INSTRUMENTOS` es un cambio de una línea, pero no hace falta.

## 7. Predicción numérica (escrita antes de correr; no se recalibra)

Con 10 semillas (1–10), `T = 200000`, `invertir_en = 100000`:

- **P1 [aceleración]** — mediana de `t_ext_B − invertir_en` de **V13+SORPRESA ≤ 0.70 ×** la de **V13**, y pareado
  (SORPRESA más rápido que V13 en la misma semilla) en **≥ 8/10**.
- **P2 [el control puede fallarlo]** — **V13+RUIDO no lo consigue**: mediana de RUIDO **≥ 0.85 ×** la de V13, y pareado
  (SORPRESA más rápido que RUIDO) en **≥ 8/10**. La lectura de P2 pasa por la tabla de la **ENMIENDA 1** (§10 bis):
  con razón de excesos en Q3 `< 0.95` el resultado es **inconcluso**, no un sí.
- **P3 [el predictor de verdad predice]** — en **V13+PRED**: `sorpresa_pre ≤ 0.25` (antes de la inversión ya casi no se
  equivoca) y `sorpresa_post ≥ max(0.20, 2 × sorpresa_pre)` en **≥ 8/10** semillas (el salto absoluto lo añade la
  **ENMIENDA 2**, §10 ter).
- **P4 [no daña la retención]** — en cada una de las SEIS etapas, **V13+SORPRESA no pierde más de 1 semilla** respecto de
  V13 (sobre 10), y en E2I `W_B ≤ −2.8` en **≥ 9/10**.
- **P5 [no daña la generalización]** — G1 con px0: mediana **≥ 0.65** y **≥ mediana(V13) − 0.10**; control `azar` en
  **[0.35, 0.65]**.
- **P6 [no gana por pasividad]** — mediana de `veneno_post` de SORPRESA **≤** la de V13, y mediana de `comida_post`
  **≥ 0.90 ×** la de V13. (Trampa "premiar pasividad", `nivel9_autonomia.md` §6.)

**Predicción del brazo PRED sobre la conducta, por I2:** idéntica a V13, semilla a semilla, en todas las claves del
tronco. Si no lo es, el instrumento está roto.

## 8. Criterio de refutación

- **Se refuta la pregunta** si **P1 falla**: la sorpresa no acelera la recuperación. Se registra así, sin reintentos con
  otro `k_sorpresa` (eso sería un experimento nuevo, con preregistro y semillas nuevas).
- **P1 sí y P2 no** → lo que acelera es **la cantidad de actualización**, no la sorpresa. Registrado con ese nombre.
- **P1 sí, P2 sí, pero P4 o P5 no** → acelera **a costa** de retención o generalización: es un canje, no una mejora, y se
  registra como canje medido (el proyecto ya tiene dos: puerta/capacidad, mapa/adquisición).
- **P6 no** → la "recuperación" es dejar de comer; la medida M1 no significa lo que dice y queda anulada.

## 9. Guardas de validez (se miran ANTES que las predicciones; si una cae, el contraste es nulo y va ERR numerado)

- **G-a [identidades]** I1, I2, I3 al 100 %. Si no, se para.
- **G-b [misma `eta` media — la trampa central]** ver **ENMIENDA 1** (regla de lectura) y **ENMIENDA 2** (dónde se mide).
  Se compara el **exceso de `eta`** (`eta_media[Q3] − 1`, cuarto inmediatamente posterior a la inversión) entre RUIDO y
  SORPRESA, y se informan `eta_media[q]` de los cuatro cuartos y `eta_pre`/`eta_post` de la ventana fina, para que la
  auditoría vea entero cuánto aprendizaje extra recibió cada brazo y cuándo.
- **G-c [hay sitio para acelerar]** mediana de `t_ext_B − invertir_en` en **V13** entre **500 y T/2 − 1** pasos y
  censura (`t_ext_B is None`) en **≤ 2/10** semillas. Si V13 se recupera en menos de 500 pasos no hay margen (suelo), y
  si no se recupera nunca la medida está censurada: en ambos casos M1 no sirve y hace falta otro mundo.
- **G-d [el predictor no está saturado]** `|error_pred[q]|` (media con signo) no pegado a la cota `clip_e` y
  `sorpresa_media[Q2] < sorpresa_media[Q1]` en ≥ 7/10 (el predictor aprende antes del evento).

## 10. Trampas revisadas (regla 5 + `nivel9_autonomia.md` §6)

| trampa | cómo se evita aquí |
|---|---|
| **"más actualizaciones" confundido con "las correctas"** | brazo RUIDO con **la misma magnitud** barajada, y la guarda **G-b** mide la `eta` media en la ventana crítica en vez de suponerla |
| canal social simétrico | no hay canal social en este bloque |
| acierto sin balancear | G1/G2 se toman de `bateria_generaliza` (ya balanceados por valencia); M1 es un tiempo, no un acierto |
| mundo que se come la comida | mundo del tronco sin tocar, `nobj=4` con reposición; los brazos difieren **sólo** en las perillas nuevas |
| sitios fijos que se memorizan | no se usan sitios; la inversión es de valencia, no de posición |
| premiar pasividad | **P6**: veneno y comida tras la inversión |
| Goodhart | ninguna medida de este preregistro entra en un criterio de aceptación de EVO ni de tronco: esto es una rama |
| declarar por conducta compleja | **vocabulario**: "predictor", "error de predicción", "sorpresa" = las tres cantidades definidas en §2. **No** se escribirá "el organismo sabe", "se conoce a sí mismo", "es consciente de su estado" ni "allostasis" como logro. Lo que se declara es lo que se midió |
| criterio que no puede fallar | P1–P6 pueden fallar; G-b y G-c pueden anular el contraste; I2 puede refutar el brazo PRED |

## 10 bis. ENMIENDA 1 — la guarda G-b no puede ser una igualdad por construcción (escrita ANTES del experimento)

**Cuándo:** tras generar el instrumento y comprobar su sintaxis y sus identidades con una corrida mínima de
comprobación (semilla 1, `T = 5 000`, un proceso). **Qué se vio, y sólo esto:** I1, I2 e I3 idénticos, y que
`eta_media` por cuarto **no coincide** entre SORPRESA y RUIDO, unas veces por arriba y otras por abajo. **No se miró
ninguna comparación de `t_ext_B` entre brazos.**

**Por qué era inevitable y por qué el criterio original estaba mal escrito:** la sorpresa es **endógena**. Barajarla
cambia lo que el organismo aprende, lo que cambia su error de predicción futuro, lo que cambia su propia sorpresa. Dos
brazos con la misma regla de modulación **no pueden** tener la misma `eta` media por construcción: un brazo que aprende
peor se sorprende más y acaba con **más** `eta`, no menos. Exigir ±10 % era un criterio que podía fallar por una razón
que no tiene nada que ver con la hipótesis (ERR-16: criterio que no puede cumplirse por diseño, en su forma inversa).

**G-b, versión vigente (regla de lectura, no anulación automática):** se compara el **exceso de `eta` en Q3** (`eta_media[Q3] − 1`) de RUIDO con el de SORPRESA (ENMIENDA 2).

| lo que se observe | lectura preregistrada de P2 |
|---|---|
| SORPRESA más rápida que RUIDO **y** `exceso de eta(RUIDO) ≥ exceso de eta(SORPRESA)` en Q3 | contraste **limpio y fuerte**: el control recibió **igual o más** aprendizaje y aun así fue más lento ⇒ lo que importa es **en qué bocado**, no cuánto |
| SORPRESA más rápida que RUIDO **y** `0.95 ≤ razón de excesos < 1` en Q3 | contraste **válido** (diferencia de cantidad ≤ 5 %) |
| SORPRESA más rápida que RUIDO **y** razón de excesos en Q3 `< 0.95` | **P2 INCONCLUSIVO**, candidato a ERR: la ventaja está confundida con "más actualizaciones". Se registra así y el paso siguiente es un control nuevo, **V13+ETA_FIJA**, con `eta_ef = eta·(1 + k_sorpresa·s̄)` y `s̄` = la `sorpresa` media **medida** en SORPRESA, en semillas nuevas. No se corre aquí |
| RUIDO igual o más rápido que SORPRESA | P2 **falla**: lo que acelera es la cantidad de actualización tras el cambio, no la sorpresa |

Esta enmienda **no toca** P1 ni ninguna otra predicción, y sólo puede hacer la lectura de P2 **más exigente**, nunca más
laxa.

## 10 ter. ENMIENDA 2 — escala del control y de la ventana, con los números del humo a la vista (ANTES del experimento)

**Cuándo:** tras el humo del diseñador (`datos/allostasis_humo_20260917_225728.*`), que corrió **una sola** corrida del
brazo SORPRESA, semilla 1, sin ningún brazo de comparación. **Qué se vio, y sólo esto** (números observados, sin ajustar
nada): identidades I1 e I2 **6/6**; `t_ext_B = 107 620`, es decir **7 620 pasos** de recuperación; `bocados` por cuarto
`[232, 171, 191, 161]` ⇒ **≈ 1 bocado cada 170 pasos**; `sorpresa_media` por cuarto `[0.0345, 0.0, 0.0836, 0.0002]`;
ventana ±2 000: `sorpresa_pre 0.0 → sorpresa_post 0.8294`, `eta_pre 1.0 → eta_post 1.8294` (n = 9/12 bocados);
`W_pred = {A −0.399, B 0.800, C 0.206, D 1.201→0.446}`. **No se vio V13 ni RUIDO, ni ninguna razón entre brazos.**

Tres consecuencias de escala, ninguna sobre P1:

1. **`buf_sorpresa` de la ventana barajada: 20 → 10 bocados** (se fija en el runner, `BRAZOS['V13+RUIDO']`; el valor por
   defecto del instrumento sigue siendo 20 y **es inerte** cuando `sorpresa_barajada=False`, comprobado: la corrida
   SORPRESA es idéntica con 20 y con 10). Motivo: a ≈ 170 pasos por bocado, 20 bocados son ≈ 3 400 pasos, casi la mitad
   de la ventana de recuperación observada; 10 bocados (≈ 1 700 pasos, ≈ 22 %) siguen rompiendo el emparejamiento
   bocado↔sorpresa y **hacen el control más fuerte**, es decir la prueba **más difícil** para la hipótesis.
2. **La guarda G-b se mide sobre `eta_media[Q3]`** (el cuarto inmediatamente posterior a la inversión: 50 000 pasos,
   ≈ 190 bocados), no sobre la ventana de ±2 000 pasos (≈ 12 bocados). Motivo: el cuarto es ancho de sobra para contener
   el retraso de ≤ 10 bocados que introduce el barajado, así que compara **cantidad** de aprendizaje extra; la ventana
   fina mide **promptitud**, que es justo lo que el control altera a propósito, y por eso pasa a ser un **diagnóstico
   informado, no una guarda**. Se compara el **exceso** sobre `eta` (`eta_media[Q3] − 1`), que es lo que se reparte.
3. **P3 se endurece:** con `sorpresa_pre = 0` exacto, "post ≥ 2 × pre" se cumple con cualquier cosa. Se añade un salto
   **absoluto**: `sorpresa_post ≥ 0.20` **y** `≥ 2 × sorpresa_pre`. El 0.20 se deriva de la estructura del mundo (al
   invertir, ΔE salta 1.2 = 0.8 − (−0.4)) y es deliberadamente holgado por abajo; **no** se toma del 0.8294 observado.

**Limitación del control, declarada:** RUIDO cambia a la vez *qué bocado* recibe el impulso y, en ≈ 1 700 pasos,
*cuándo*. Si RUIDO resulta más lento, no se podrá separar "bocado equivocado" de "impulso tardío": eso lo separa el
control **V13+ETA_FIJA** de la ENMIENDA 1, que **no se corre aquí**.

**Declaración de exposición (para la auditoría):** la **semilla 1 del brazo SORPRESA** se vio en el humo, y las semillas
1–6 se vieron en las identidades (donde por construcción no hay nada que ver). El experimento corre en **1–10** como
manda el encargo; si el auditor prefiere un conjunto no visto, `--desde 11` da semillas limpias sin tocar nada más.

## 11. Coste y quién corre qué

- **Runner:** `experimentos/nivel9_allostasis/corre_allostasis.py` (con `Pool`, **lo corre el coordinador**, regla 3 y 11).
  Etapas: identidades (I1, I2, I3) → experimento principal (4 brazos × 10 semillas × 200 000) → retención M4 (4 brazos ×
  6 etapas × 10 semillas × 100 000) → generalización M5 (4 brazos × 2 reglas × 10 semillas × 200 000). Orden de coste:
  el de `curiosidad`/`largo`, minutos con `Pool`.
- **Humo del diseñador (un proceso, sin `Pool`):** `corre_allostasis.py --humo` = identidad semilla 1 × 3 escenarios a
  **T = 40 000** (I1 e I2 comparten la corrida de referencia de v13: 9 simulaciones, 360 000 pasos) + **una** corrida
  V13+SORPRESA con inversión a T = 200 000. Total **560 000 pasos**, por debajo del techo de 3 × 200 000 de la regla 3.
  Los números que salgan se informan **tal cual, sin ajustar nada**.
- **Sin commits** (regla 7): el coordinador integra.
