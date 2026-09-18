# PREREGISTRO — BLOQUE 4: **un canal con REFERENCIA por señalamiento, SIMÉTRICO**, entre dos v15f en el mismo mundo

**Misión (primero, siempre):** llegar a la AGI por este camino — un organismo mínimo con reglas locales (sin
backprop en el runtime) que aprende, desaprende, generaliza, **sobrevive, se reproduce y se COMUNICA**, con
evidencia preregistrada. Hoy: **que dos células se comuniquen sobre algo que ambas representan.**

**Autor:** diseñador del bloque 4. **Fecha de firma:** 18 sep 2026.
**Estado al firmar:** §1–§8 y §11 se escribieron **ENTERAS antes de correr un solo brazo**. Lo único corrido al
escribirlas es el **arnés de identidad** (`identidad_familias_b4.py`, **92/92**), que no mide ninguna hipótesis —
**con dos excepciones que declaro en §5.4 y que por eso NO cuentan como predicción**. §9 (humo) se escribe después y
**nada de §1–§8 se toca al escribirlo**. §10 lo escribe el coordinador con la serie 541–560.

**ERR libres desde ERR-50.** Este preregistro **no gasta ninguno**: no mueve ningún umbral de los bloques 2 y 3, no
reabre ninguna medida cerrada y no cambia el mundo de familias — le añade una perilla (`exc_fija`) que **no toca su
rng** y que el arnés comprueba (caso w1).

**Reglas cumplidas.** No edité ningún archivo existente ni congelado. `organismo/organismo_v14.py`
(`feefc88b1fd8d434`), `organismo_familias.py` (`b9dd561a0cf056b8`), `organismo_familias_b2.py`
(`30200bea6a41c3c8`), `organismo_familias_b3.py` (`62a1e53b452b078e`), `escala_codigo.py` (`d8b8566bca77a0ae`),
`organismo_v15f.py` / `organismo_v15f_on.py` y los runners de los bloques 1–3 **sólo se leen o se importan**.
Archivos nuevos **sólo** en `experimentos/nivel12_mundo_familias/` y **todos con sufijo `_b4`**. Instrumento **por
anclas, con dos cadenas**. **Nunca `multiprocessing.Pool`** en mi humo (un proceso, **6 corridas**, T ≤ 200 000).
Sin commits. `organismo/` primero en `sys.path` (ERR-28). Criterios ANTES de medir. Todo medido por **conducta de la
boca**, nunca por pesos (ERR-44). Estadística ERR-37.

**Fuentes.** `registro/REGISTRO_etapas_1_2.md`, entradas **BLOQUE 2** y **BLOQUE 3**;
`PREREGISTRO_bloque2_variante.md` y `PREREGISTRO_bloque3_v15f.md` (§10 de cada uno);
**`registro/investigacion/sala3_celulas/PROTOCOLO_canal_20260918.md`** (síntesis de 12 células, 3 rondas — de
donde vienen la dirección decisiva de §1, la medida de especificidad de §5.3 y los cinco puntos abiertos de §8);
`experimentos/etapa5_comunicacion/` (`PREREGISTRO_N1.md`, `PREREGISTRO_N2f.md`, `PREREGISTRO_N3d.md`,
`mundo_social_n3.py`) y las entradas de ERR-32/33/34; `registro/HANDOFF.md` §13 fila 5; `registro/EQUIPO.md` 1–14.

---

## 1. La pregunta, y por qué ésta y no otra

La hipótesis del director, textual: *"hay un órgano productor y un órgano receptor y un mensaje que se codifica; si
yo aprendo que hay sal y la otra célula aprende que es sal, y yo aprendo que la sal rosada es veneno y le indico por
el mensaje que es peligro, él ya entiende el principio: estamos mandando un mensaje sobre una representación de algo
que ya tenemos."*

La precisión del coordinador: **el mensaje debe llevar REFERENCIA (de qué) además del valor**; el código interno es
privado, así que la referencia compartida sólo puede ser el **estímulo del mundo** — **señalamiento**, que es este
bloque; la señal arbitraria aprendida por los dos es el bloque 5.

### 1.1 Lo que ya está medido y hace posible preguntarlo aquí

| de dónde | qué dejó |
|---|---|
| **bloque 2** (v14.1) | la variante nunca vista se lee **desde el token**: `g1(LIN)` 1.000 ×2, `g1(BAR)` 0.25–0.31. Generalizar por familia **es lo que el organismo hace**. |
| **bloque 3** (v15f) | la tabla de pares **comprime por familia** y v15f **lee la variante nunca vista sin morderla** (`g1` 1.0 / 0.875) y **se desdice en una mordida (7 de 8)**. El precio: **una sola ganadora de 4 casillas**. |
| **etapa 5** (N1, N2f, N3d) | **teorema del canal (ERR-32):** si la vista del receptor no informa, no hay código compartido que escribir; si informa, el receptor lo aprende solo y **el canal no aporta**. |
| **sala 3** (12 células, §2.7 y §5.1 del protocolo) | **la dirección barata no vale**: avisar de veneno es justo lo que el receptor **aprendería solo** en una mordida que cuesta −3 y no mata (7 de 8, bloque 3). **Donde el receptor solo está ciego para siempre es en la dirección inversa: lo que EVITA y en realidad es COMIDA — como no lo muerde, nunca lo corrige (0 de 8).** |

### 1.2 El mundo está construido en el hueco que dejan ERR-32 y la sala 3, y es **simétrico**

La variante **retenida por la deriva** (la que el receptor **no puede haber visto**) es, en **dos** tokens, una
**EXCEPCIÓN** — y en direcciones opuestas:

- **X⁺ = `T0v2`**: su familia (`T0`, `T0v0`, `T0v1`) es **comida** y **ella es VENENO**. Generalizar por familia
  dice *"cómela"* y es **falso**. Sin mensaje, el receptor **la muerde** y se lleva un −3 — **y entonces la
  aprende**. Es la dirección **barata**.
- **X⁻ = `T1v2`**: su familia (`T1`, `T1v0`, `T1v1`) es **veneno** y **ella es COMIDA**. Generalizar por familia
  dice *"evítala"* y es **falso**. Sin mensaje, el receptor **no la muerde nunca**, así que **nunca la corrige**:
  está ciego para siempre. Es la dirección **irreemplazable**, y es la que decide este bloque.

Los **otros seis** `Tkv2` (k = 2…7) son variantes **igual de nunca vistas** con la valencia de su familia: el
**control balanceado dentro de la misma semilla** (trampa 2 de la regla 5).

**Por eso el emisor de este bloque es SIMÉTRICO:** anota su **primera mordida de cada estímulo marcado por el
mundo**, con la **R cruda** que recibió, **de cualquier signo** — `−3.0` para X⁺ y `+1.0` para X⁻. No inventa
valores: el protocolo de la sala 3 pidió `−5` y **−5 no existe** en este mundo (`R_VAL = {comida: +1, veneno: −3}`).

**H (la que se juzga).** *Un mensaje local con dos campos — el patrón del referente (coordenadas de retina, que son
públicas) y la valencia cruda — entregado mientras el receptor está ANTE el referente, cambia la conducta de su boca
en la PRIMERA exposición de su vida a ese patrón, en las dos direcciones, y lo hace de forma ESPECÍFICA de ese
estímulo.*

**H¬ (la alternativa que tomo en serio, y que es la mía).** *Llega el VALOR y no llega la REFERENCIA.* La boca lee
por **UNA** celda ganadora: **2 bits**. Un mensaje no puede ser más específico que esa casilla. En el mundo de
familias esa celda parte los tokens **por valencia** con píxeles de **forma**, que la variante comparte con sus
hermanas y con toda su clase. *"La sal rosada es peligro"* se recibiría como *"la comida es peligro"*.

**Lo que este bloque NO decide:** no declara *"lenguaje"*, *"palabra"*, *"símbolo"*, *"entiende"*, *"significado"*
ni *"representa"* (reglas 6 y 8); no juzga a v15f contra `CRITERIO_TRONCO_v2.md`; no toca el tronco; y no mide nada
del bloque 5 (§11, **sin medir**).

---

## 2. EL MUNDO — el del bloque 2/3, con **una** perilla nueva que no toca su rng

Se importa `corre_familias_b2.BASE` tal cual (el objeto, no una copia): `D = 12` (9 forma + 3 variable), `F = 8`
tokens de peso 3, `V = 3` variantes (32 estímulos), catálogo de `escala_codigo` (bloque 0), `L = 160`, `nobj = 16`,
`renov = 1.0`, `costo = 0.008`, `NK = 30`, `NKMAX = 90`, `K = 3`, `vent = 10 000`, `crit_exp = 0.5`, `n_neu = 0`,
B-5 apagado, `log_cada = 250`, `reg_b2 = 1`, `T = 100 000`.

**Fijo en todos los brazos:** `fam_val='familia'`, `cambio = 10**9` (**nada cambia nunca**: no hay viraje),
`vira = 0`, **`n_exc = 2`** y **`exc_fija = 2`**.

- **`exc_fija = 2`** (perilla nueva): la excepción candidata de cada token es la variante **2**, la que la deriva
  retiene. **El sorteo de b3 se ejecuta igual**, así que el rng del mundo no cambia: sólo se sobrescribe a quién
  señala (arnés, casos w1/w2: con `n_exc = 0` la perilla no cambia ni la permutación `azar`).
- **`n_exc = 2`**: las excepciones son `T0v2` (**X⁺**, veneno en familia de comida) y `T1v2` (**X⁻**, comida en
  familia de veneno). Arnés, caso w3.

**Los dos organismos.** Se diferencian en **su rng** y en **su deriva**; el mundo es **el mismo objeto** (misma
`fam_seed`; arnés, caso u) y sus **códigos internos son distintos** (arnés, caso v: `cod0` difiere — el código es
privado). **Ninguno ve al otro:** son dos `run()` sin visión mutua, y la corrida del receptor depende **sólo** de
los cuatro campos del mensaje (arnés, caso R). Por eso **no existe** ninguna validación del tipo *"compruebo si el
emisor rechaza después"* (protocolo §5.6), y este bloque **no tiene defensa contra la falsa alarma** — lo digo
antes, no después.

| | semilla del organismo | `fam_seed` | `deriva` | qué ve |
|---|---|---|---|---|
| **E (emisor)** | `s` | `s` | 5 000 | las tres variantes circulan: **muerde X⁺ y X⁻ y aprende las dos** |
| **R (receptor)** | `s + 100 000` | `s` | `T/3 + 1` | fases `v0 \| v1 \| v2`: **X⁺ y X⁻ no existen hasta `t = 66 668`** |

**Por qué "no lo ve hasta la prueba" y no "lo ve sin morderlo" (el encargo pedía decidir y justificar).** No puedo
impedir que la boca muerda sin tocar la boca, y tocar la boca sería otro organismo. La deriva del escenario G del
bloque 2/3 **ya** produce el estado que hace falta y **sin ninguna perilla nueva**. Y resuelve un problema que el
arnés me enseñó y que cambió el diseño — el mismo que la sala 3 marcó como *"el hallazgo del día"* (§2.7 del
protocolo):

> **si el receptor ya hubiera mordido el referente ≥ 5 veces, la puerta por evidencia del código exacto estaría
> abierta y la boca leería la vía RÁPIDA — y el mensaje, que se escribe en la vía lenta, quedaría escrito y nunca
> consultado.** Un canal de un solo mensaje **no puede** mover la vía rápida (`eta = 0.03` contra una sobrescritura
> completa de la tabla).

**Esto es una propiedad del tronco v14.1, no una conveniencia del montaje, y es el primer resultado del bloque
aunque no sea una predicción: un canal así sólo alcanza a la boca para lo que el receptor no conoce de primera
mano.** Se **mide** (P-I5) en vez de suponerse, y en la dirección (−) juega **a favor** del canal (el receptor nunca
muerde X⁻, así que su código nunca le es familiar): lo digo porque me favorece.

---

## 3. EL INSTRUMENTO — `organismo_familias_b4.py`, por **dos cadenas de anclas**

`construye_familias_b4.py` (no se edita a mano ningún archivo):

- **CADENA 1 (extracción).** Del **propio `organismo_familias_b3.py`** (sha exigido) se extrae **literalmente** el
  bloque de **escritura de la tabla de pares** — el que corre cuando la boca muerde — y se reusa, dedentado, como
  cuerpo de la **entrega** del mensaje, con cuatro sustituciones declaradas. **El canal no reimplementa el
  aprendizaje**: escribe **exactamente** lo que habría escrito una mordida, y nada más (ERR-38).
- **CADENA 2 (aplicación).** Sobre `organismo_familias_b3.py`, con **diez anclas de línea**.
- Si cualquiera de las dos no encaja, **aborta y no escribe nada**; el texto se **compila** antes de escribirse.

### 3.1 Las cuatro perillas nuevas, y nada más (todas inertes por defecto)

| perilla | qué hace |
|---|---|
| `fam_seed=None` | semilla del **mundo**, separada de la del organismo. Con `None` es `seed` → b3 exacto. |
| `exc_fija=None` | la excepción de cada token es una variante **fija**. El sorteo se hace igual: **el rng del mundo no cambia**. |
| `canal=None` | `{'modo':'emite'}` → el emisor **anota**, simétrico. `{'modo':'sen'\|'inm'\|'mudo','t','P','R','ref'}` → el receptor. |
| `reg_b4=0` | registro de la **conducta de la boca** en las 3 primeras exposiciones tras la entrega. |

**La mecánica del canal, dicha entera.** El mensaje son **dos campos**: `P` (el patrón del referente: 12 píxeles,
**coordenadas de retina, que son públicas**) y `R` (la valencia cruda que recibió el emisor). Al entregarse, el
receptor ejecuta el bloque **extraído** con esos dos campos: **una exposición sin consecuencia con la valencia
recibida**. **NO** toca la energía, **NO** quita ni repone objetos, **NO** suma evidencia del código (`ncod`),
**NO** toca la vía rápida (`Wp`/`Wn`), **NO** toca la lineal (`Wps`/`Wns`), **NO** divide células, **NO** cuenta
como mordida. **Sólo la tabla de pares.** El receptor **decodifica con SU propia proyección** (sus 66 celdas, su
ganadora): el código es privado; lo único compartido es el estímulo. *La referencia no viaja en el mensaje: viaja en
el mundo. El mensaje no nombra; coincide con lo nombrado.*

**Los tres modos de entrega.**
- **`sen` (SEÑALAMIENTO, el brazo del bloque):** en el primer paso `t ≥ t_msg` en el que el receptor **está sobre el
  referente**.
- **`inm`:** en `t = t_msg`. Separa *"lo hace el mensaje"* de *"lo hace el momento"*.
- **`mudo` (el GEMELO = CORTADO):** hace **todo** lo del canal — llega en el mismo paso, mira la misma casilla,
  anota los mismos diagnósticos — **y no escribe el mensaje**. Es el `vira = -8` de los bloques 2 y 3 trasladado.

**Cuándo habla el emisor:** en su **primera mordida de cada estímulo marcado por el mundo**, con la **R cruda de
cualquier signo**. **El emisor con `canal='emite'` es b3 bit a bit** (arnés, casos r y s): mirar no cambia nada.

### 3.2 Arnés `identidad_familias_b4.py`: **92/92**

11 casos de apagado total contra `organismo_familias_b3` (×3), 2 de rng no consumido a T = 120 000, 4 de **cadena
completa** (`organismo_v14` TRONCO, `organismo_v15f_on`, `organismo_familias`, `organismo_familias_b2`), 2 de *"el
emisor sólo mira"*, 1 de `fam_seed` inerte + 2 del montaje (mismo mundo / código privado), 4 de `exc_fija`, 2 de
claves, **5 de perilla mal usada que DEBE lanzar `ValueError`**, 10 del montaje E → R (incluidas la **puerta P-I3**
del prefijo, *"el receptor nunca había visto el referente"*, **la simetría del emisor** y **"el receptor no ve al
emisor"**) y **7 controles que DEBEN fallar** (entre ellos BARAJADO, VALOR-SOLO y **R-SIN-SAL**). **Sin 92/92 no se
corre nada (P-I1).**

---

## 4. BRAZOS Y SEMILLAS

Un emisor por semilla, del que salen **los dos mensajes**. **Siete receptores por dirección**, que se diferencian
**ÚNICAMENTE en el `canal`** (mismo mundo, misma semilla de organismo, mismas perillas):

| brazo | `modo` | `P` del mensaje | mundo de R | para qué |
|---|---|---|---|---|
| **CANAL±** | `sen` | el referente (X⁺ / X⁻) | `s` | **la pregunta** |
| **CORTADO±** | `mudo` | el referente | `s` | **el gemelo**: sin mensaje = el receptor solo (bloque 3) |
| **BAR-H±** | `sen` | una **hermana** (`T0v0` / `T1v0`) | `s` | ¿la referencia distingue la variante de sus hermanas? |
| **BAR-T±** | `sen` | **otro token** de la misma clase (`T2v2` / `T3v2`) | `s` | ¿la referencia distingue el token? |
| **VALOR±** | `sen` | **12 ceros** (sin referencia) | `s` | sólo *"peligro"* / *"premio"* |
| **INM±** | `inm` | el referente | `s` | ¿lo hace el mensaje o el señalamiento? |
| **OTRO± (R-SIN-SAL)** | `sen` | el referente **del mundo del emisor** | **`s + 200 000`** | el referente **no existe** en el mundo del receptor; y **el colateral del relevo** |

`T0v0`, `T2v2`, `T1v0` y `T3v2` están fijados **aquí, antes de ver ningún dato** (`T2` y `T0` son pares ⇒ familias
de comida; `T3` y `T1` impares ⇒ familias de veneno: el barajado cae siempre en la misma clase de valencia que su
referente, para que el control no sea de paja).

**15 corridas por semilla (1 E + 14 R) × 20 = 300 corridas.** **Semillas 541–560**, nuevas; **réplica 561–580**
(regla 12). Arnés y humo: **1, 2, 3**. Ninguna de 541–580 queda expuesta antes de la serie.

---

## 5. LAS MEDIDAS — **todas de la boca**, y con el control dentro de la semilla

Se importan de `corre_familias_b2`/`_b3` el mundo, `resuelve` y el diagnóstico estructural. La conducta se lee sobre
`primera_b2` (la **primera exposición de la VIDA** a cada estímulo) y `primera_b4` (las **tres primeras tras la
entrega**). **Nunca sobre pesos (ERR-44).**

### 5.1 Las medidas que deciden

En la **primera exposición de la vida** a cada una de las 8 variantes retenidas:

| símbolo | qué es | lo correcto |
|---|---|---|
| **`evX`** ∈ {0,1} | la boca **NO muerde** el referente | **1** para X⁺ (es veneno) · **0** para X⁻ (es comida) |
| **`okX`** ∈ {0,1} | lo que hizo la boca **acierta** con la valencia real | **1** en las dos direcciones |
| **`evU`, `okU`** | lo mismo sobre las **otras 6** `Tkv2` nunca vistas | `okU` = **1** |
| **`comH` = 1 − `evH`** | fracción de las **3 hermanas** del referente que la boca **sigue mordiendo** en su primera exposición **tras la entrega** | **1** (son comida en (+); en (−) son veneno y lo correcto es 0 — se reporta con su signo) |
| **`esp` = signo·(`evX` − `evU`)** | **especificidad referencial** entre iguales (signo = +1 si el mensaje dice *"peligro"*) | **1** |
| **`nunca`** | el receptor **no muerde el referente en TODA la corrida** | en CORTADO− debe ser **1**: *"ciego para siempre"* |
| **`ret2`, `ret3`** | la 2.ª / 3.ª exposición tras la entrega sigue movida por el mensaje | — |
| **`lag_t`, `lag_m`** | pasos y **mordidas** entre la entrega y la prueba (0 por construcción en `sen`) | — |
| **`fam1`** | qué vía usó la boca en la prueba (**1 = rápida/familiar**, 0 = lenta) | **0** (P-I5) |
| **muertes** | supervivencia del receptor | — |

`esp` es la medida que el coordinador pidió (*"evita X … sigue comiendo a las hermanas"*) **hecha balanceada**: las
6 variantes de control son tan nunca vistas como el referente y tan de su familia como él, así que un rechazo
indiscriminado no puede pasar por referencia.

### 5.2 Puertas de validez (si caen, no se lee nada más)

- **P-I1 (instrumento):** arnés **92/92** y su subconjunto en el runner; shas exactos; cruce de `cod0` campo a campo.
- **P-I2 (hay mensaje):** el emisor anota el referente de la dirección en **≥ 18/20**, con la **R cruda del signo que
  le toca**, y `t_msg < 2·deriva(R)` en todas. Las semillas sin mensaje se **excluyen de esa dirección** y se
  reportan al lado (regla 10: la exclusión se escribe aquí, antes).
- **P-I3 (gemelo):** cada brazo `sen` comparte con su CORTADO el prefijo **exacto** de `log` hasta la entrega, en
  **≥ 18/20**; INM hasta `t_msg`. Si cae, **es el instrumento y se para**.
- **P-I4 (nunca visto):** en CORTADO±, la primera exposición de la vida al referente coincide con el paso de la
  entrega, en **20/20**.
- **P-I5 (por qué vía se lee):** en la prueba, la boca usa la **vía lenta** (`fam1 = 0`) en **≥ 18/20**. Las semillas
  en las que el alias de código hace familiar el referente se reportan **aparte**: ahí el mensaje queda escrito y no
  consultado, y eso **no es un fallo del canal**.

### 5.3 Diagnósticos del mecanismo — **observados, no prometidos** (protocolo §5.2)

`canal_gan_pre` / `canal_gan_post` (celda ganadora antes y después del mensaje), **`gan_var`** (si el par ganador
usa alguno de los 3 píxeles **variables**: la única forma de que la tabla pueda distinguir una variante de sus
hermanas), `canal_bin` (la casilla del referente) y **`n_mismo_bin`** (cuántos de los 32 estímulos caen en ella).
**El techo es de 2 bits: un mensaje no puede ser más específico que esa casilla.** Ninguna cifra de discriminación
se promete a priori: **la especificidad se mide.** Alias estructural por semilla, covariable declarada.

### 5.4 **Declaración de contaminación (lo digo en vez de esconderlo)**

El arnés — corrido **antes** de escribir este documento, porque es una comprobación de instrumento — ya me enseñó
dos cosas, en **las semillas 1 y 2**, con T = 60 000:

1. **Dirección (+), `evX` de CANAL+:** el mensaje sobre `T0v2` se emite en `t ≈ 10 000` y se entrega en `t ≈ 40 000`;
   en **las dos semillas** el receptor lee `−3.0` por la **vía lenta** (`fam1 = 0`) y **no muerde** X⁺ en su primera
   exposición. La casilla del referente la comparten **8 de 32** estímulos en la semilla 1 y **16 de 32** en la 2;
   la ganadora **cambió** de `(2,4)` a `(5,11)` en la semilla 1 — **`11` es un píxel variable** — y no cambió en la
   2; y en la semilla 1 el receptor **vuelve a morder X⁺ en su 3.ª exposición**, tras 8 mordidas.
2. **El emisor es simétrico y funciona:** en la semilla 1 anota también `T1v2` con `R = +1.0` — es decir, **el
   emisor sí llega a morder lo que su propia familia le dice que es veneno**, porque la boca es estocástica.

**Por eso `evX` del brazo CANAL+ NO es una predicción ciega: es un diagnóstico declarado**, y se reporta con ese
estatus. **Lo que sí es ciego, y no lo he visto en ninguna configuración:** **toda la dirección (−)** — incluida la
predicción decisiva P-3 —, `evX` de CORTADO+, `evU`/`okU`, `comH`, `esp`, `ret2`/`ret3`, `nunca`, las muertes, y
**todos** los brazos BAR-H, BAR-T, VALOR, INM y OTRO en las dos direcciones. Ésas son las predicciones de §6.

El cambio de ganadora a un par con píxel variable es el dato que más me sorprendió y el que hace que §6.1 **no** sea
trivial: el mecanismo tiene una vía por la que la referencia *podría* llegar, y no sé si llega.

---

## 6. PREDICCIONES (escritas antes de correr un solo brazo)

**Convención ERR-37a.** `evX` es binaria por semilla (umbrales en k/20). `evU` avanza en escalones de 1/6 ≈ 0.167;
`comH` en escalones de 1/3. Los umbrales están **fuera** de la mediana esperada por el otro y las zonas intermedias
se declaran **vacías a propósito**.

### 6.1 Las dos predicciones enfrentadas (lo que decide el bloque)

| | predicción | umbral | qué la refuta |
|---|---|---|---|
| **P-C** *(del coordinador)* | el canal lleva **valor Y referencia**, en las dos direcciones: CANAL+ **≥ 15/20** evita X⁺ contra CORTADO+ **≤ 5/20**; **CANAL− ≤ 5/20** (come X⁻ a la primera) contra CORTADO− **≥ 15/20**; **BARAJADO y VALOR-SOLO se comportan como CORTADO** (|BAR − CORTADO| ≤ 3/20); **hermanas intactas `comH` ≥ 0.9** | todas a la vez | que BAR-H o BAR-T queden a ≤ 3/20 de CANAL, o `comH` ≤ 0.6 |
| **P-D** *(mía, al lado y distinta)* | **llega el valor y NO llega la referencia**: coincido en P-1 y en P-3 (el canal mueve la boca en las dos direcciones) y discrepo en todo lo demás — **`evU` mediana ≥ 0.6** en la dirección (+), **`comH` ≤ 0.6**, y **BAR-H y BAR-T indistinguibles de CANAL** (\|CANAL − BAR\| ≤ 4/20): el mensaje cae en la casilla de la **valencia**, no en la del estímulo | las tres a la vez | **BAR-H y BAR-T como CORTADO** (gana el coordinador: la referencia llega), o `comH` ≥ 0.9 |

**Zona declarada vacía:** `evU` mediana en (0.2, 0.6), o BARAJADO a distancia 4–3 de los dos extremos, o `comH` en
(0.6, 0.9). Ahí **no gana ninguno** y el veredicto lo dice con esas palabras.

**Derivación de los umbrales.** `evU ≥ 0.6` son ≥ 4 de las 6 variantes de control movidas: *"mueve su clase
entera"*. `evU ≤ 0.2` es ≤ 1 de 6: *"la referencia acierta"*. `comH ≥ 0.9` es el umbral literal del encargo y con 3
hermanas equivale a **las tres intactas**. Con 20 semillas y binomial p = 0.5, 15/20 está por encima del azar y
5/20 por debajo (ERR-37).

### 6.2 Las demás, cada una con su umbral y su refutación

| # | qué pregunta | PASA | REFUTA | mi predicción |
|---|---|---|---|---|
| **P-1** *(contaminada en CANAL+, §5.4)* | (+) ¿llega el **valor**? | CANAL+ ≥ 15/20 **y** CORTADO+ ≤ 5/20 | CANAL+ ≤ 10/20 **o** CORTADO+ ≥ 10/20 | **pasa**; lo ciego es CORTADO+ y el pareado |
| **P-2** | ¿qué hace el receptor **sin mensaje**, en las dos direcciones? | CORTADO+ ≤ 5/20 (muerde el veneno) **y** CORTADO− ≥ 15/20 (evita la comida) **y** `nunca` ≥ 15/20 | CORTADO− ≤ 10/20 | **pasa**: v15f generaliza por familia y aquí la familia miente en los dos sentidos |
| **P-3 — LA DECISIVA** | (−) ¿sirve donde el receptor **está ciego para siempre**? | CANAL− **≤ 5/20** (COME a la primera) **y** CORTADO− ≥ 15/20 **y** pareado ≥ 14/20 | CANAL− ≥ 10/20 | **pasa**: el mensaje `+1` sobrescribe la casilla y la boca lee `+1` en su primera exposición |
| **P-4** | ¿la referencia distingue **hermanas**? | \|BAR-H − CORTADO\| ≤ 3/20 | \|BAR-H − CANAL\| ≤ 3/20 | **REFUTA** |
| **P-5** | ¿la referencia distingue **token**? | \|BAR-T − CORTADO\| ≤ 3/20 | \|BAR-T − CANAL\| ≤ 3/20 | **REFUTA** |
| **P-6** | ¿hace falta el **campo de referencia**? | \|VALOR − CORTADO\| ≤ 3/20 | \|VALOR − CANAL\| ≤ 3/20 | **REFUTA**. **Subconjunto preregistrado (regla 10):** en las semillas donde la casilla de los ceros **no** es la del referente, VALOR debe comportarse como CORTADO; se reporta con los umbrales originales y junto al completo |
| **P-7** | ¿lo hace el mensaje o el **señalamiento**? | \|INM − CORTADO\| ≤ 5/20 | \|INM − CANAL\| ≤ 3/20 | **pasa**: entre `t_msg` y la prueba median ~30 000 pasos y cientos de mordidas que **sobrescriben** la casilla |
| **P-8** | ¿hace falta **compartir el mundo**? ¿y el **colateral del relevo**? | \|OTRO − CORTADO\| ≤ 3/20 **y** `okU` y muertes de OTRO **no peores** que CORTADO en ≥ 15/20 | \|OTRO − CANAL\| ≤ 3/20 | **pasa en el referente** (si no existe en su mundo, el mensaje cae donde caiga) y **no sé** el colateral: una sola entrega **reelige la ganadora de las 66** y eso mueve la lectura de todo lo que sirve la vía lenta. Es el punto §5.5 del protocolo y aquí **se mide por primera vez** |
| **P-9** | ¿**cuánto dura**? | `ret3` ≤ 8/20 | `ret3` ≥ 15/20 | **pasa**: vida media de pocas mordidas — la sobrescritura que lo hace posible es la que lo borra |
| **P-10** | ¿**sirve para vivir**? | muertes(CANAL) < muertes(CORTADO) pareado ≥ 14/20 | ≥ en ≥ 14/20 | **en (+) REFUTA** (ahorra una mordida de −3 y cuesta comidas rechazadas); **en (−) no sé**: ahí el mensaje **añade** una fuente de comida |

### 6.3 Predicción global, para poder equivocarme

Predigo que el bloque 4 entrega **media hipótesis del director, y la mitad buena**: *"el canal traslada el VALOR en
una sola exposición y sin morder, en las DOS direcciones — incluida aquélla en la que el receptor solo estaría ciego
para siempre —, pero NO traslada la REFERENCIA: con una sola celda ganadora de 2 bits, la casilla que recibe el
mensaje es la de la VALENCIA, así que el barajado hace lo mismo que el mensaje honesto y las hermanas lo pagan."*

Si acierto, la letra es: ***"para señalar hace falta un receptor cuyo código separe el referente de sus vecinos; la
memoria de pares de v15f no lo hace, y es el mismo cuello que el bloque 3 dejó abierto (una sola ganadora)"***, y el
bloque 4 entrega al 5 una **condición previa**, no un permiso.

**Si me equivoco y gana P-C** — BAR-H, BAR-T y VALOR como CORTADO, con CANAL± separado de CORTADO± y `comH` ≥ 0.9 —
entonces **el campo de referencia sí llega**, y lo diré con esas palabras: *"dos organismos con códigos privados
comparten un referente por el estímulo del mundo, y el mensaje cambia la conducta del receptor sólo sobre ese
referente, en las dos direcciones"*. En ese caso el bloque 5 se puede montar encima.

---

## 7. LO ÚNICO QUE SE PERMITE CORREGIR

**ERR-50, reservado, una sola vez.** Si **P-I2 cae** (el emisor no emite) o **P-I3 cae** (el gemelo no comparte
prefijo), el bloque **no se corrige**: se para, porque es el instrumento. La única corrección permitida es ésta: si
**P-I4 cae** — el receptor **sí** había visto el referente antes de la entrega —, se corre **una** serie más con
`deriva(R) = T/2 + 1`, con **semillas nuevas** y **la misma letra en todo lo demás**, y se reportan las dos.

**Nada más se corrige.** En particular: no se cambia la mecánica del canal, ni a qué vía escribe, ni `mem_alfa`, ni
`mem_rho`, ni el modo de entrega, ni los patrones del barajado, ni ningún umbral de §6, ni la valencia del mensaje
(**es la R cruda que recibió el emisor: `−3.0` y `+1.0`; `−5` no existe en este mundo**). Escribir el mensaje
también en la vía lineal o en la rápida **sería otro candidato**, con preregistro nuevo.

---

## 8. QUÉ SE PODRÁ DECLARAR, Y QUÉ NO

**No se declara** (reglas 6 y 8): *"lenguaje"*, *"palabra"*, *"símbolo"*, *"concepto"*, *"entiende"*,
*"representa"*, *"significado"*, ni *"comunicación"* a secas.

**Se podrá declarar, literalmente:**

- si **P-2 y P-3 pasan**: *"un mensaje de dos campos, entregado mientras el receptor está ante el estímulo, hace que
  la boca del receptor COMA, en la primera exposición de su vida, un alimento que su propia generalización por
  familia le decía que era veneno y que sin el mensaje no habría mordido nunca en toda la corrida."* **Ésa es la
  frase del bloque**, y es la única que el receptor no podía conseguir solo.
- si **P-1 pasa**: *"...y en la dirección contraria evita, sin haberlo mordido, un veneno que su familia le decía
  que era comida."*
- si **P-4, P-5 y P-6 refutan**: *"...y el mensaje no lleva referencia: el mismo efecto se consigue nombrando a una
  hermana, a otro token o a nadie, porque la casilla que lo recibe es la de la valencia."*
- si **P-4, P-5 y P-6 pasan** (gana P-C): *"...y el efecto es específico del estímulo nombrado."*
- si **P-7 pasa**: *"el mensaje sólo llega si se entrega ante el referente: entregado antes, se borra."*
- si **P-8 pasa en el referente y su colateral falla**: *"y una sola entrega reelige la celda ganadora y estropea la
  lectura de todo lo demás"* (punto §5.5 del protocolo, hasta hoy sin medir).
- si **P-10 refuta en (+)**: *"y en la dirección barata no le sirve para vivir más."*

**Qué no puedo hacer, declarado antes:**
1. No puedo separar *"el canal no lleva referencia"* de *"no la lleva **con una sola celda ganadora de 2 bits**"* —
   son la misma cosa en esta implementación. Separarlas pide **varias ganadoras**, un **nodo indexado por código y
   retina** (la línea que ERR-45 mandó al organismo) o el mensaje escrito en la vía **lineal** de 12 píxeles: los
   tres son **otro candidato y otro preregistro**.
2. **No hay defensa contra la falsa alarma.** El receptor no ve al emisor (§2), así que BARAJADO mide *"el mensaje
   no nombra"*, **no** *"el receptor detecta al mentiroso"*. Sigue abierto (protocolo §5.6).
3. La puerta de familiaridad se **mide** (P-I5) pero este bloque **no decide** si es defecto o virtud.
4. No mido nada del examen ni del mundo vivo: **no** juzgo a v15f con el criterio v2.
5. Con 20 semillas no cierro nada: la réplica 561–580 es obligatoria (regla 12).

---

## 9. HUMO — resultado (§1–§8 y §11 no se tocaron)

### 9.0 Identidad del instrumento (antes de todo)

`python experimentos/nivel12_mundo_familias/identidad_familias_b4.py` → **IDENTIDAD 92/92**, un proceso, semillas 1–3.

| bloque del arnés | casos | resultado |
|---|---|---|
| APAGADO (`canal=None`, `fam_seed=None`, `reg_b4=0`) == `organismo_familias_b3` | (a)…(k), 11 × 3 | **33/33 IDÉNTICO** (AB, inversión, sin puerta, linaje v13, B-5, relevo ON, mundo del bloque 1, escenarios G y S del bloque 2/3, perillas del b2) |
| RNG no consumido por las perillas apagadas | (l), (m) a T = 120 000 | **4/4 IDÉNTICO** (relevo apagado y encendido) |
| **Cadena completa** | (n) == `organismo_v14` TRONCO · (o) == `organismo_v15f_on` (6 px, 15 celdas) · (p) == `organismo_familias` · (q) == `organismo_familias_b2` | **12/12 IDÉNTICO** |
| **El emisor SÓLO MIRA** | (r) T = 20 000 ×3 · (s) T = 60 000 ×2, con el mensaje ya existente | **5/5 IDÉNTICO** |
| `fam_seed` y el montaje | (t) inerte ×3 · (u) **E y R en el MISMO mundo** campo a campo · (v) **`cod0` DISTINTO: el código es privado** | **5/5** |
| `exc_fija` | (w1) **con `n_exc = 0` no cambia el mundo ni la permutación `azar` → el rng del mundo intacto** · (w2) sí cambia a quién señala · (w3) `n_exc = 2` da `T0v2` veneno y `T1v2` comida · (w4) los patrones del runner son los del catálogo del bloque 0 | **4/4** |
| Claves | (w) añade exactamente las 12 del bloque 4 · (x) apagadas son inertes | **2/2** |
| **Perilla mal usada: DEBE lanzar** | (y) no es dict · (z) modo desconocido · (A) receptor sin tabla de pares · (B) `ref` inexistente · (C) `P` con otro tamaño | **5/5 LANZA** |
| **El montaje E → R** | (D) emite · (E) el mensaje es `T0v2`, `R < 0`, patrón del catálogo · **(E3) el emisor es SIMÉTRICO: también anota `T1v2` con `R = +1`** · (E2) habla antes de que R pueda ver el referente · (F) recibe · (G) entrega por señalamiento · (H) CORTADO recibe la visita y ningún mensaje · **(H2) el receptor NUNCA había visto el referente** · **(I) P-I3: prefijo exacto de `log` compartido** · (J) el canal no come · **(R) mismo `(t, ref, P, R)` construido SIN el emisor → receptor idéntico: el receptor NO ve al emisor** | **11/11** |
| **Controles que DEBEN fallar** | (K) CANAL ≠ CORTADO · (L) `inm` ≠ `sen` · (M) relevo ≠ apagado · (N) `fam_seed` distinta · (O) BARAJADO por hermana · (P) VALOR-SOLO · **(Q) R-SIN-SAL** | **14/14 DIFIERE (como debe)** |
| | **total** | **92/92** |

### 9.1 Coste declarado del humo (regla 3)

**6 corridas de un proceso, a la T real del bloque** (T = 100 000, semillas 1 y 2): **2 emisores** (de cada uno
salen los DOS mensajes) + **CANAL−** ×2 + **CORTADO−** ×2, es decir exactamente lo que pide el encargo (*"2
semillas, brazos CANAL y CORTADO"*) **en la dirección decisiva**, la (−). Dos de esas cuatro corridas de receptor
**no llegaron a existir**, porque en la semilla 2 el emisor no emitió en (−) (§9.3, punto 1). La dirección (+) **no
se humeó**: lo único que tengo de ella es el diagnóstico contaminado del arnés (§5.4), y lo digo en vez de
presentarlo como humo. El humo se corrió **dos veces**: la primera destapó tres fallos del instrumento (§9.4) y sus
números de conducta son los mismos que los de la segunda salvo `evU`, que cambió al corregir el conjunto de control.

### 9.2 La tabla del humo (n = 1 corrida útil por brazo: **NO es evidencia**)

`familias_b4_humo_20260918_172442.json`, sha16 `bb93b187ea5ca8b9`. Identidad del subconjunto **14/14** (incluido el
control (K) que debe fallar). Cruce de `cod0` del **emisor** contra `escala_codigo`: **idéntico campo a campo**.
**7.5 s/corrida** → la serie (300 corridas) ≈ **2.7 min con `Pool(14)`**. Alias por par 0.006 / 0.042, con algún par
alias en las 2 semillas (covariable declarada).

**EMISOR** (`deriva = 5000`): en la semilla 1 anota **las dos** excepciones — `T0v2` con `R = −3.0` en `t = 10 260`
(a su **1.ª** exposición) y `T1v2` con `R = +1.0` en `t = 10 264` (a su **3.ª**). En la semilla 2 anota `T0v2`
(`t = 10 029`) y **no anota `T1v2` en 100 000 pasos**.

**RECEPTOR**, dirección **(−)**, semilla 1 (`T1v2` es **comida** en una familia de **veneno**; entrega por
señalamiento en `t = 66 866`, que es su **primera exposición de la vida** a ese patrón; la boca lee por la **vía
lenta** en los dos brazos):

| brazo | `evX` | `okX` | `ret2`/`ret3` | `mord_ref` (toda la corrida) | `evU` (6 de control) | `okU` | `comH` | `esp` | muertes | ganadora | casilla | mismo bin |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| **CANAL−** | **0.0** (la **MUERDE**) | **1.0** | 0.0 / 0.0 | **8** | 0.333 | 0.833 | 1.0 | 0.333 | 19 | (2,4) → **(1,2)** | 0 | 16/32 |
| **CORTADO−** | **1.0** (no la muerde) | **0.0** | 1.0 / 1.0 | **1** | 0.333 | 0.833 | 0.0 | −0.667 | 19 | (2,4) → (2,4) | 0 | 16/32 |

**Prefijo de `log` hasta la entrega: `9c394fd0695ae005` en los dos → P-I3 se cumple con el canal encendido.**

### 9.3 Qué dice el humo, sin ajustar nada

1. **El riesgo que el humo destapa, y es el del bloque: el EMISOR también está casi mudo en la dirección
   irreemplazable.** Para poder decir *"lo que evitas es comida"*, alguien tiene que haberlo mordido — y el emisor
   lo evita por la misma razón que el receptor: su familia es veneno, así que la boca lo muerde sólo cuando el azar
   y el hambre coinciden (`p ≈ 0.025` con hambre 1, `≈ 3·10⁻⁵` saciado). En el humo, **1 de 2**. La puerta **P-I2**
   exige ≥ 18/20 en la dirección. **Si cae, el preregistro manda parar esa dirección** (§5.2) y la serie sólo lee la
   (+). **No toco el umbral, ni la T, ni el mundo** (regla 4). Lo que sí digo, antes de la serie, es que si P-I2(−)
   cae eso **no es un fallo del canal sino un resultado**: *la información tiene que entrar en la población por
   algún lado, y el mismo mecanismo que hace ciego al receptor hace casi mudo al emisor.* La corrección natural (un
   emisor más hambriento, una T mayor, o varios emisores) sería **bloque 4b, con preregistro nuevo**.
2. **La dirección decisiva funciona donde hay mensaje, y en el sentido que importa.** Con el mensaje, el receptor
   **muerde a la primera** un alimento que nunca había visto y que su propia generalización por familia le decía que
   era veneno (`okX = 1.0`), y sigue mordiéndolo (8 mordidas en la corrida). Sin el mensaje **no lo muerde**, ni en
   la 2.ª ni en la 3.ª exposición, y en 100 000 pasos lo muerde **una sola vez**. Con n = 1 esto no es evidencia; es
   la señal de que el montaje mide lo que dice medir.
3. **La referencia, observada y no prometida: el techo de 2 bits aparece tal cual.** La casilla del referente la
   comparten **16 de 32** estímulos, y el precio se ve en las hermanas: `comH` pasa de **0.0** (CORTADO: no muerde a
   las tres hermanas venenosas, que es lo correcto) a **1.0** (CANAL: **se las come todas**). El mensaje `+1` sobre
   `T1v2` **abre en canal toda la casilla del veneno**. `esp` pasa de −0.667 a +0.333: se mueve en la dirección
   buena, pero muy lejos de 1. **Esto es exactamente lo que predice P-D, y no lo cambio ni lo suavizo.** Con n = 1
   no decide nada.
4. **La ganadora cambia con una sola entrega,** de `(2,4)` a `(1,2)` en CANAL− y **no** en CORTADO−: una sola
   entrega **reelige la celda que sirve a toda la vía lenta** (punto §5.5 del protocolo de la sala 3, hasta hoy sin
   medir). Ninguno de los dos pares usa un píxel variable, así que en esta semilla la tabla **no podía** distinguir
   la variante de sus hermanas.
5. **La vía por la que se lee es la lenta en los dos brazos** (`fam1 = 0`): el montaje evita la puerta de
   familiaridad, como §2 dijo que haría. P-I5 tendrá números, no suposiciones.
6. **Las muertes son 19 en los dos brazos:** en esta semilla el canal no cuesta ni paga vidas. P-10 lo decide con 20.
7. **Coste:** 7.5 s/corrida contra los 6.7 del bloque 3; la serie completa, 300 corridas, ≈ 2.7 min con `Pool(14)`.

**Lo que esto cambia para la serie: nada de §1–§8 ni de §11.** Las predicciones quedan como están, incluida la mía,
que el humo ya señala en la dirección de cumplirse (punto 3), y la del coordinador, que el humo señala como
incumplida en la parte de las hermanas. Lo único que añado es el aviso del punto 1, que es una **puerta ya
escrita**, no un umbral nuevo.

### 9.4 Los tres fallos del instrumento que el primer humo destapó (y que no son datos)

1. El **conjunto de control** incluía la otra excepción: con `n_exc = 2` hay **dos** referentes, y `evU` los contaba
   como control. Corregido: el control son las **6** variantes retenidas que **no** son excepción.
2. El **cruce de `cod0`** se hacía sobre los receptores, cuya semilla de organismo es `s + 100 000` y por tanto no
   coincide con la del diagnóstico estructural. Corregido: se cruza el **emisor** (mismo `seed` de organismo y de
   mundo) → **idéntico campo a campo**.
3. El caso de identidad (K) del runner usaba la dirección (−) a `T = 6 000`, donde **todavía no existe el mensaje**.
   Corregido: usa la (+) con su propia `T = 30 000` → **2/2 DIFIERE (como debe)**.

Ninguno de los tres toca una predicción: son el instrumento, y por eso el humo se corrió otra vez entero.

## 10. SERIE 541–560 — resultado

*(Vacío al firmar. Lo escribe el coordinador cuando lance el `Pool`.)*

---

## 11. SIGUIENTE — **BLOQUE 5: la señal ARBITRARIA (la palabra)**, esbozo *sin medir*

Hoy el mensaje **es** el patrón del mundo: no hay palabra, hay una copia del referente, y hace falta que el
referente esté delante. El bloque 5 pregunta si los dos pueden acordar **un símbolo** que sustituya al señalamiento.

- **Montaje.** El mismo mundo y los mismos dos organismos. El canal gana **un campo más**: `S`, un símbolo **fijo y
  arbitrario**, ajeno al mundo. **El emisor emite el mismo `S` cada vez que VE el referente** — no cuando lo muerde:
  cuando lo ve, para que `S` coocurra con él muchas veces.
- **Aprendizaje del receptor, local y sin backprop.** Una tabla `S × casilla` de **coocurrencias**: cuando llega `S`
  y el receptor está ante un estímulo, se refuerza la asociación entre `S` y la casilla de ese estímulo. No hay
  maestro ni error global: es la misma sobrescritura por última evidencia del bloque 3.
- **La prueba, y es la que decide:** **`S` SOLA, sin el referente delante y sin entregar su patrón**, y después la
  primera exposición al referente. Si la conducta de la boca cambia **sólo** por haber recibido `S`, el símbolo
  **sustituye** al señalamiento.
- **Brazos:** `S` honesta · **PALABRA-CRUZADA** (la palabra de otro referente, entregada aquí: no debe mover la
  boca) · `S` sin historia de coocurrencia · sin `S`.
- **Lo que haría falta antes**, y por eso no se mide hoy: (a) que el bloque 4 muestre que el receptor puede
  representar el referente con **resolución suficiente**; (b) un alfabeto y una regla de coocurrencia
  preregistrados; (c) el control de ERR-32 otra vez — que `S` no sea deducible del mundo.
- **Falla esperada y honesta, dicha antes:** con **una** celda ganadora de **2 bits** no caben 8 palabras. El
  bloque 5 pedirá, casi seguro, **más de una ganadora** — y eso ya es **órgano nuevo, no perilla**. Y si `S` se
  asocia a la **casilla** y la casilla es la de la valencia, `S` no será una palabra: será **un timbre de alarma**.
  La prueba tiene que exigir que `S` mueva la boca ante el referente **y no ante sus hermanas**, con el mismo
  control balanceado de §5.1.
