# PREREGISTRO — BLOQUE 3: **v15f en el mundo de familias**, con la MISMA letra del bloque 2

**Misión (primero, siempre):** llegar a la AGI por este camino — un organismo mínimo con reglas locales (sin backprop en el
runtime) que **generaliza y se desdice**, sobrevive y se reproduce, con evidencia preregistrada.

**Autor:** diseñador del bloque 3, sala 2. **Fecha de firma:** 18 sep 2026.
**Estado al firmar:** §1–§8 se escribieron **ENTERAS antes de correr un solo brazo**. Lo único corrido al escribirlas es el
**arnés de identidad** (`identidad_familias_b3.py`, 71/71), que no mide ninguna hipótesis — **con una excepción que declaro
en §5.3 y que por eso NO cuenta como predicción**. §9 (humo) se escribe después y **nada de §1–§8 se toca al escribirlo**.
§10 lo escribe el coordinador con la serie 501–520.

**ERR libres desde ERR-50.** Este preregistro **no gasta ninguno**: no mueve ningún umbral del bloque 2 (los **importa**),
no reabre ninguna medida cerrada y no toca el mundo. Reserva **ERR-50** para la única corrección que §7 permite.

**Reglas cumplidas.** No edité ningún archivo existente ni congelado. `organismo/organismo_v14.py` (`feefc88b1fd8d434`),
`experimentos/creacion_A/organismo_v15f.py` (`96fc5c5262107850`) y `organismo_v15f_on.py` (`54d6efe0b564113c`),
`organismo_familias.py` (`b9dd561a0cf056b8`), `organismo_familias_b2.py` (`30200bea6a41c3c8`), `escala_codigo.py`
(`d8b8566bca77a0ae`) y los runners de los bloques 1 y 2 **sólo se leen o se importan**. Archivos nuevos **sólo** en
`experimentos/nivel12_mundo_familias/` y **todos con sufijo `_b3`**. Instrumento **por anclas, con dos cadenas**. **Nunca
`multiprocessing.Pool`** en mi humo (un proceso, ≤ 6 corridas, T ≤ 200 000). Sin commits. `organismo/` primero en `sys.path`
(ERR-28).

**Fuentes.** `experimentos/creacion_A/PREREGISTRO_v15f.md` (`df7348599aa68333`) y la entrada *"Candidato v15f"* de
`registro/REGISTRO_etapas_1_2.md`; `PREREGISTRO_bloque2_variante.md` y su §10 (resultado 461–480 y réplica 481–500);
`registro/CRITERIO_TRONCO_v2.md`; `registro/investigacion/SALA2_frontera_20260918.md` §B.3 y §C.3 (*"en los bloques 2 y 3,
v15f es el control de Occam, no un competidor"*); `registro/EQUIPO.md` 1–14.

---

## 1. La pregunta, y por qué es exactamente ésta

El bloque 2 dejó el hueco medido y replicado, con v14.1 en este mundo:

| capacidad | v14.1 (461–480 / 481–500) |
|---|---|
| **generalizar a la variante nunca vista** | **ya la tiene**: `g1(G-LIN)` **1.000 ×2**, y la tiene **porque lee el token** (`g1(G-BAR)` 0.25 / 0.31, P-G3 pasa ×2) |
| **separar la variante que deja de comportarse igual** | **no la tiene**: separa **4 de 8**, `sep/apr` 2.0, y **sólo las que ya había mordido** (comida 1.0 contra veneno 0.0, P-S3 pasa ×2) |
| el precio | **ninguno**: P-S4 **REFUTADA ×2** (daño 0.0) — cuando consigue separarla, sus hermanas no lo pagan |

Es decir: **lo que falta no es marcar la sal rosa como sal; es dejar de marcarla**, y falta exactamente en las cuatro que el
organismo rechaza (la puerta por evidencia del código exacto sólo se abre con **mordidas**). v15f es el único candidato del
proyecto que **se desdice de un golpe** (E2 reversión 20/20, sobrescritura con R crudo). **La pregunta de este bloque es si
eso se traslada a este mundo, y a qué precio en la capacidad que v14.1 ya tenía.**

**H (la que se juzga).** *La memoria de pares con relevo separa la variante que cambia de consecuencia — también las que
eran veneno — porque su tabla sobrescribe con la última recompensa y no depende de la puerta por código.*

**H¬ (la alternativa que tomo en serio, y que es la mía).** *En una retina de 12 píxeles con 32 estímulos, la celda
ganadora de v15f es **una** tabla de **4 casillas**, así que la sobrescritura que la hace desdecirse rápido es la misma que
la hace **olvidar** rápido: separa y desepara, y de paso destruye la lectura lineal que daba `g1 = 1.000`.* (§5.3, §6.)

**Lo que este bloque NO decide:** no juzga a v15f contra `CRITERIO_TRONCO_v2.md` (eso es el bloque 0(d) de la síntesis, con
su examen y su mundo vivo), no lo declara candidato ni lo descarta como tal, y no declara *"token"*, *"lenguaje"*,
*"concepto"* ni *"representa"* (regla 6 y 8).

---

## 2. EL MUNDO — **no cambia ni un valor**

Se importa el del bloque 2 tal cual (`corre_familias_b2.GEN` y `.SAL`, los objetos, no una copia): `D = 12` (9 forma + 3
variable), `F = 8` tokens, `V = 3` variantes (32 estímulos), catálogo de `escala_codigo` (bloque 0), `L = 160`, `nobj = 16`,
`renov = 1.0`, `costo = 0.008` (`dureza = 4`), `NK = 30`, `NKMAX = 90`, `K = 3`, `vent = 10 000`, `crit_exp = 0.5`,
`n_neu = 0`, B-5 apagado, `log_cada = 250`, `T = 100 000`.

- **Escenario G**: `deriva = T/3 + 1` (fases `v0 | v1 | v2`; la tercera variante no existe hasta `t = 66 668`),
  `exc_evita = 2`, `cambio` fuera del horizonte.
- **Escenario S**: `deriva = 5 000`, `n_exc = 0`, `cambio = T/2`, `vira = 8` (las 8 candidatas de `exc_win`, una por token,
  invierten su valencia; sus hermanas no) contra `vira = −8` (el **gemelo**: declara las mismas 8 y no cambia ninguna).

**La única cosa que varía entre brazos es `memoria_pares` (`None` ↔ `'relevo'`).** Un cambio por experimento (regla 2), y el
control del bloque 2 (`S-EXC`/`S-LIN`, `G-LIN`/`G-EXC`) se **vuelve a correr en las semillas nuevas** para que la
comparación sea dentro de la misma serie y no contra números de otro rango.

---

## 3. EL INSTRUMENTO — **dos cadenas de anclas** (`construye_familias_b3.py`)

- **CADENA 1 (extracción).** De `organismo_v15f.py` (sha exigido) se **extraen literalmente** los tres bloques del mecanismo
  — la inicialización con las tres funciones de lectura (`_lin_v15f`, `_tabla_v15f`, `_lenta_v15f`), el bloque de escritura
  de la tabla, y el prefijo del diccionario de salida — más cuatro anclas de línea. **No se reescriben a mano** (ERR-38).
- **CADENA 2 (aplicación).** Sobre `organismo_familias_b2.py` (sha exigido), con siete anclas.
- **Si cualquiera de las dos no encaja, aborta y no escribe nada.** Además, el texto resultante se **compila** antes de
  escribirse.

### 3.1 La única generalización al texto de v15f, declarada

v15f fija la retina en 6 px: `_PARv` sobre `range(6)` y **15** celdas. El mundo de familias tiene `_D = 12`, así que **`6`
pasa a `_D`** (la variable que el bloque 1 ya introdujo) y **`15` pasa a `_NP = len(_PARv) = C(_D,2)`**. El constructor
comprueba que **no queda ningún 6 ni ningún 15 fijo** tras generalizar. **Con `_D = 6` esto es literalmente 15**, y por eso
la identidad con `organismo_v15f_on` es comprobable y se comprueba. **Nada más del mecanismo cambia**: R crudo,
sobrescritura, error propio por celda (EMA con `mem_rho = 0.02`), ganadora por menor error, desempate al azar con el rng del
organismo, y relevo a la lineal cuando la celda ganadora no conoce la combinación. `mem_alfa = 1.0`, los valores de v15f.

### 3.2 Arnés `identidad_familias_b3.py`: **71/71** (§9.0)

10 casos de apagado total contra `organismo_familias_b2`, 1 de rng no consumido a T = 120 000, 3 de **cadena completa hasta
el TRONCO** (`organismo_v14`, `organismo_v14_codigo_on`, `organismo_familias`), **6 de `relevo` ON en 6 px ≡
`organismo_v15f_on` bit a bit** (incluido T = 120 000, que cubre el consumo de rng del desempate), 1 del gemelo del bloque 2
con el relevo encendido, 3 de conjunto de claves, y **8 controles que deben fallar**. Sin 71/71 no se corre nada (**P-I**).

---

## 4. BRAZOS Y SEMILLAS

| brazo | escenario | `memoria_pares` | perillas | para qué |
|---|---|---|---|---|
| **G-LIN** | G | `None` | `n_exc=0` | v14.1: la referencia (bloque 2: `g1` 1.000 ×2) |
| **G-REL** | G | `'relevo'` | `n_exc=0` | **v15f** |
| **G-EXC** | G | `None` | `n_exc=8` | v14.1 con 8 excepciones vistas (P-G4) |
| **G-REXC** | G | `'relevo'` | `n_exc=8` | v15f con 8 excepciones vistas (P-G4) |
| **S-EXC / S-LIN** | S | `None` | `vira=8` / `vira=−8` | v14.1 y su gemelo |
| **S-REL / S-REL0** | S | `'relevo'` | `vira=8` / `vira=−8` | **v15f y su gemelo** |
| **S-RAZA / S-RAZA0** | S | `'relevo'` | `fam_val='azar'` | v15f donde no hay familia |
| **S-RBAR / S-RBAR0** | S | `'relevo'` | `fam_val='barajado'` | v15f con familia falsa |
| **V14 / V15F** *(anclas)* | — | `None` / `'relevo'` | `mundo='AB'` | los dos organismos literales. **No compiten.** |

**12 brazos × 20 semillas = 240 corridas** (+ 2 anclas × 20). **Semillas 501–520**, nuevas; **réplica 521–540** (regla 12).
Arnés y humo: **1, 2, 3**. Ninguna de 501–540 queda expuesta antes de la serie.

**Por qué cada brazo con relevo lleva su gemelo `vira = −8`:** `dano_herm` es una diferencia **pareada contra un gemelo de
prefijo idéntico** (§2.4 del bloque 2). Sin él la medida no está definida — es exactamente el fallo que el humo del bloque 2
cazó, y no lo repito.

---

## 5. LAS MEDIDAS — **las del bloque 2, importadas**

`lee_G`, `lee_S` y `traza` se **importan** de `corre_familias_b2.py`; no hay ni una medida nueva de conducta. Todo se mide
sobre lo que **lee la boca** (`log` con `log_cada = 250`, `primera_b2`, `sep_exp`), nunca sobre pesos internos (T-E,
ERR-44).

### 5.1 Un aviso de lectura que hay que decir antes

En v14.1, `g1_lenta` era *"lo que habría leído la vía lineal"*. En v15f la vía lenta **es el relevo**, así que en los brazos
`REL` la columna `g1_lenta` significa *"lo que leyó el relevo (tabla si conoce la combinación, lineal si no)"*. Es la misma
variable del instrumento (`_ws`), y lo digo para que nadie la lea como *"la lineal"*.

### 5.2 La tabla de pares se reporta como **diagnóstico del mecanismo**, y no decide nada

`mem_ganadora` (qué par ganó), `mem_cobertura` (casillas vistas de 4), `mem_vistas`, `mem_err_tabla` y **cuántos de los 32
estímulos leen la TABLA en vez de relevar a la lineal**. Son estado interno: **no deciden ninguna predicción de conducta**.

### 5.3 **Declaración de contaminación (lo digo en vez de esconderlo)**

El diagnóstico del arnés — que corrí **antes** de escribir este documento, porque es una comprobación de instrumento — ya me
enseñó estos números: semilla 1, T = 30 000, escenario S, relevo ON → **66 celdas**, ganadora **(2, 4)**, cobertura **3/4**,
**32 de 32 estímulos leen la tabla**, error propio 0.0000. **Por eso `PM` (el mecanismo) NO es una predicción de este
bloque: es un diagnóstico declarado**, con un marcador informativo (≥ 28 de 32 leen la tabla; *"el relevo casi no dispara"*
sería < 8 de 32) y sin veredicto de paso.
**Lo que sí es ciego, y no lo he visto en ninguna configuración:** `g1`, `n_sep`, `sep/apr`, la asimetría comida/veneno,
`dano_herm` y `ok_vir` **de cualquier brazo con relevo**. Ésas son las predicciones de §6, y son las que cuentan.

---

## 6. PREDICCIONES (escritas antes de correr un solo brazo)

**La letra de P-G1, P-G4, P-S1, P-S2, P-S3, P-S4 y P-S6 es LA DEL BLOQUE 2, sin tocar un dígito:** el runner **importa los
objetos** `corre_familias_b2.UMBRALES`, no los copia, precisamente para que no puedan cambiar al cambiar de organismo
(ERR-31). Se aplican a los brazos nuevos.

### 6.1 Las dos predicciones enfrentadas (lo que decide el bloque)

| | predicción | umbral | qué la refuta |
|---|---|---|---|
| **P-C** *(del coordinador, ya registrada)* | v15f separa **≥ 6 de 8** viradas, **incluidas las que eran veneno**; `sep_exp / exp_asoc` **≤ 1.0**; **retención** de la virada (`ok_vir` en el último punto de `log`) **≥ 0.8** | las tres a la vez, en medianas | que la retención quede por debajo de 0.8 |
| **P-D** *(mía, al lado y distinta)* | **coincido en la velocidad** (`n_sep ≥ 6`, `sep/apr ≤ 1.0`) **y discrepo en la retención: `ok_vir` final ≤ 0.5**, porque con `D = 12` la celda ganadora es **una** tabla de **4 casillas para 32 estímulos**: la misma sobrescritura que la hace desdecirse de un golpe hace que **la siguiente mordida de una hermana le borre la casilla a la virada** | `n_sep` mediana ≥ 6 **y** `sep/apr` mediana ≤ 1.0 **y** `ok_vir` final mediana **≤ 0.5** | **`ok_vir` final ≥ 0.8** (es decir, que gane el coordinador) |

**Derivación del umbral de retención (ERR-37a).** `ok_vir` avanza en escalones de **1/8 = 0.125**. **0.5** (4 de 8) y
**0.8** (entre 6/8 = 0.75 y 7/8 = 0.875) dejan una **zona declarada** (0.5, 0.8) en la que **no gana ninguno de los dos** y
se dice así. Ninguno de los dos umbrales es la mediana esperada del otro: yo espero ≈ 0.125–0.375, el coordinador ≈ 0.875.
**Referencia del bloque 2:** v14.1 retuvo **0.5** (las 4 que separó), así que *"v15f retiene como v14.1"* (0.5) cuenta como
zona, no como victoria mía — y eso es deliberado.

### 6.2 Las de la misma letra del bloque 2

| # | dónde se aplica | umbral (idéntico al bloque 2) | mi predicción |
|---|---|---|---|
| **P-S1** *(puerta)* | las 4 parejas | prefijo de `log` con `t < cambio` idéntico en **20/20** | pasa (el arnés ya lo da con el relevo encendido) |
| **P-S2** | `S-REL` (y `S-EXC` al lado) | pasa: `n_sep ≤ 5` **y** `sep/apr ≥ 2.0` en ≥ 14/20 · refuta: `n_sep ≥ 7` **y** `sep/apr ≤ 1.0` en ≥ 14/20 | **REFUTA en `S-REL`** (v15f separa deprisa) y **pasa en `S-EXC`** (v14.1 no) |
| **P-S3** | `S-REL` | pasa: asimetría comida > veneno en ≥ 14/20 · refuta: ≤ 11/20 | **REFUTA en `S-REL`**: la tabla no depende de la puerta por código, así que separa también las que eran veneno |
| **P-S4** | pareja `S-REL`/`S-REL0` (y las otras tres al lado) | pasa: `dano_herm(10 000)` mediana **≥ 0.10** y > 0 en ≥ 15/20 · refuta: ≤ 0.02 o ≤ 11/20 | **PASA en `S-REL`** — donde en v14.1 **refutó ×2** (daño 0.0): escribir la casilla de la virada escribe la de sus hermanas |
| **P-G1** | `G-REL` (y `G-LIN` al lado) | pasa: `g1` mediana ≥ 0.75 y ≥ 15/20 · refuta: ≤ 0.60 o ≤ 11/20 | **REFUTA en `G-REL`** (`g1` ≤ 0.60) y **pasa en `G-LIN`** (1.000, como en 461–500): el relevo **tapa** la lectura lineal que daba el acierto |
| **P-G4** | `G-EXC`/`G-LIN` y `G-REXC`/`G-REL` | pasa: EXC < LIN en ≥ 14/20 y razón ≤ 0.90 | indeciso en v14.1 (lo fue ×2); **sin predicción firme en v15f** |
| **P-S6** | `S-REL`, con `S-EXC` al lado | en el bloque 2 se reportaba; **aquí decide**, por P-C y P-D | ver §6.1 |

### 6.3 Predicción global, para poder equivocarme

Predigo que **v15f gana la capacidad 2 en velocidad y la pierde en todo lo demás**: separa rápido y sin la asimetría de la
puerta (P-S2 refuta, P-S3 refuta — ahí coincido con el coordinador y con H), **pero no retiene** (P-D), **daña a las
hermanas** donde v14.1 no las dañaba (P-S4 pasa) y **pierde la generalización a la variante nunca vista** que v14.1 sí tenía
(P-G1 refuta). Si acierto, la letra es: ***"la sobrescritura que permite desdecirse de un golpe es la misma que impide
retener, y en 12 píxeles una sola celda de 4 casillas no alcanza para 32 estímulos"***, y lo que el bloque 3 entrega al
siguiente no es *"v15f sirve"* ni *"v15f no sirve"*, sino **el canje exacto**: velocidad de desdecirse contra retención y
generalización — el mismo canje que v11 tuvo entre retención y generalización y que v13 rompió con **dos vías y una puerta**.
**Si me equivoco y gana P-C**, v15f resuelve el hueco del bloque 2 y pasa a ser el candidato del criterio v2 con prioridad, y
lo diré con esas palabras.

---

## 7. LO ÚNICO QUE SE PERMITE CORREGIR

**ERR-50, reservado, una sola vez.** Si **P-S1 cae** (algún gemelo no comparte prefijo) el bloque **no se corrige**: se para,
porque es el instrumento. La única corrección permitida es ésta: si en `S-REL` **`n_sep` mediana es 0 y `apr` mediana es
`None`** — es decir, si el relevo impide que el organismo llegue siquiera a leer bien ningún estímulo, y por tanto **ni
`sep_exp` ni `exp_asoc` están definidos**, de modo que P-S2, P-C y P-D quedan **sin soporte** —, se corre **una** serie más
con `crit_exp = 0.25` (la mitad del umbral de lectura), con **semillas nuevas** y **la misma letra en todo lo demás**, y se
reportan las dos. **No se toca ningún otro umbral, ni el mundo, ni `mem_alfa`, ni `mem_rho`, ni el organismo.**

**Nada más se corrige.** En particular: no se prueba otra `mem_rho`, no se limita `_NP`, no se añade una compuerta contra la
lineal (eso **sería otro candidato**, con preregistro nuevo — y es justo lo que la refutación de `crece_codigo` en la sala 2
señaló como lo que v15f no tiene), y no se cambia el Δ que decide P-S4 (es **10 000**, escrito en el bloque 2).

---

## 8. QUÉ SE PODRÁ DECLARAR, Y QUÉ NO

**No se declara** (regla 6 y 8): *"token"*, *"lenguaje"*, *"concepto"*, *"entiende"*, *"representa"*, ni *"v15f entra al
tronco"* / *"v15f queda descartado"* (este bloque **no** es el criterio v2).

**Se podrá declarar, literalmente:**

- si **P-S2 refuta y P-S3 refuta en `S-REL`**: *"la memoria de pares con relevo separa la variante que deja de comportarse
  igual en tantas o menos exposiciones de las que costó aprenderla, y la separa también cuando era veneno — que es donde
  v14.1 no llega."*
- si además **P-D se cumple**: *"...pero no la mantiene separada: al final de la corrida lee bien la mitad o menos de las
  viradas."* Si se cumple **P-C**: *"...y la mantiene separada."*
- si **P-S4 pasa en `S-REL`**: *"y sus hermanas lo pagan, en el mismo mundo en el que con v14.1 no lo pagaban."*
- si **P-G1 refuta en `G-REL` y pasa en `G-LIN`**: *"en este mundo, la memoria de pares cuesta la generalización a la
  variante nunca vista que el tronco sí tenía."*

**Qué no puedo hacer, declarado antes:** no puedo separar *"v15f es peor aquí"* de *"v15f es peor con `_NP = 66` y una sola
ganadora"* — son la misma cosa en esta implementación, y para separarlas haría falta un candidato con varias ganadoras o con
compuerta contra la lineal, que **no** es este bloque. No mido nada del examen ni del mundo vivo, así que **no** juzgo a
v15f con el criterio v2. Y con 20 semillas no cierro nada: la réplica 521–540 es obligatoria (regla 12).

---

## 9. HUMO — resultado (§1–§8 no se tocaron)

### 9.0 Identidad del instrumento (antes de todo)

`python experimentos/nivel12_mundo_familias/identidad_familias_b3.py` → **IDENTIDAD 71/71**, un proceso, semillas 1–3.

| bloque del arnés | casos | resultado |
|---|---|---|
| APAGADO (`memoria_pares=None`) == `organismo_familias_b2` | (a)…(j), 10 × 3 | **30/30 IDÉNTICO** (AB, inversión, sin puerta, linaje v13, B-5, mundo del bloque 1, y los dos escenarios del bloque 2 con `reg_b2=1`) |
| RNG no consumido por la perilla apagada | (k) T = 120 000 ×2 | **2/2 IDÉNTICO** |
| **Cadena completa hasta el TRONCO** | (l) == `organismo_v14`, (m) == `organismo_v14_codigo_on`, (n) == `organismo_familias` | **9/9 IDÉNTICO** |
| **`relevo` ON en 6 px == `organismo_v15f_on` BIT A BIT** | (o)…(s) ×3 + (t) T = 120 000 ×2 | **17/17 IDÉNTICO** (incluye el rng del desempate de la ganadora) |
| Gemelo del bloque 2 con el relevo encendido | (u) ×2 | **2/2 IDÉNTICO** |
| Claves | (v) añade exactamente las 10 de v15f · (w) apagadas son `None` · (x) con `D = 12` son **66 = C(12,2)** celdas | **3/3** |
| **Controles que DEBEN fallar** | (y) relevo ≠ apagada ×3 · (z) relevo ≠ v14.1 ×3 · (A) `vira` pasado el cambio ×2 | **8/8 DIFIERE (como debe)** |
| | **total** | **71/71** |

### 9.1 Coste declarado del humo (regla 3)

**6 corridas de un proceso, a la T real del bloque:** `S-REL`×{1,2}, `S-EXC`×{1,2}, `S-REL0`×{1}, `G-REL`×{1}. El encargo
pide *"2 semillas, S-REL y S-EXC"* (4); añado `S-REL0` porque **sin el gemelo `dano_herm` no está definida** (el fallo que
el humo del bloque 2 cazó) y `G-REL` porque es el brazo de P-G1. Lo digo en vez de esconderlo.

### 9.2 La tabla del humo (n ≤ 2: **NO es evidencia**)

`familias_b3_humo_20260918_160429.json`, sha16 `7845bcbb9602e8ea`. Identidad del subconjunto **14/14**. Cruce de `cod0`
contra `escala_codigo`: idéntico campo a campo. **6.7 s/corrida** → la serie (280 corridas) ≈ **2.2 min con `Pool(14)`**.
Gemelo `S-REL`/`S-REL0` en la semilla 1: prefijo `2477b40484f6cf31` en los dos → **P-S1 se cumple con el relevo encendido**.

**Escenario S** (`cambio = 50 000`, 8 viradas: 4 eran comida y 4 eran veneno; 24 hermanas):

| brazo · semilla | `n_sep` | comida | **veneno** | `sep_med` | `apr_med` | `ok_herm` 0 / 2500 / 10k / 25k / fin | `ok_vir` fin | ganadora | cob. | leen tabla |
|---|---|---|---|---|---|---|---|---|---|---|
| **S-REL** s1 | **7/8** | 4/4 | **3/4** | 5.0 | 1.0 | 1.0 / 1.0 / **0.958** / **0.875** / 1.0 | **0.625** | (2,4) | 3/4 | 32/32 |
| **S-REL** s2 | **6/8** | 4/4 | **2/4** | 2.0 | 1.0 | 1.0 / 0.667 / 1.0 / 1.0 / 0.875 | **0.750** | (3,8) | 4/4 | 32/32 |
| S-EXC s1 (v14.1) | 4/8 | 4/4 | **0/4** | 2.0 | 1.0 | 1.0 / 1.0 / 1.0 / 1.0 / 1.0 | 0.500 | — | — | 0/32 |
| S-EXC s2 (v14.1) | 5/8 | 4/4 | **1/4** | 2.0 | 1.0 | 1.0 / 0.667 / 1.0 / 1.0 / 1.0 | 0.500 | — | — | 0/32 |
| S-REL0 s1 (gemelo) | **0/8** | 0/4 | 0/4 | — | 1.0 | 1.0 / 1.0 / 1.0 / 1.0 / 1.0 | 1.000 | (2,4) | 3/4 | 32/32 |

**Escenario G** (primera exposición a la variante nunca vista, `t` 66 672–66 952 contra `2 × deriva = 66 668`):

| brazo · semilla | `g1` | `g1_fuerte` | `g1_lenta` | `cond1` | `ruta1` | vistas | muertes |
|---|---|---|---|---|---|---|---|
| **G-REL** s1 | **1.000** | **1.000** | 1.000 | 1.00 | 0.000 | 8/8 | 21 |

**Diagnóstico del mecanismo, 1 corrida aparte (declarada; total del humo 6 + 1).** Con `G-REL` semilla 1, la celda
ganadora **(2, 4)** lee la tabla para **32 de 32** estímulos y acierta **los 32 con el R CRUDO exacto**: `+1.0` en los 16 de
comida y `−3.0` en los 16 de veneno, con sólo **3 casillas de 4** ocupadas. Las ocho primeras exposiciones a `Tk v2` se leen
`+1.0` / `−3.0` **exactas** desde la tabla, sin haberlas visto nunca.

### 9.3 Qué dice el humo, sin ajustar nada: **mi mecanismo era falso, y lo digo antes de la serie**

1. **P-D se cae por su razón, y la razón era mía.** Escribí en §6.1 que *"con `D = 12` la celda ganadora es una tabla de 4
   casillas para 32 estímulos"* y de ahí deduje que v15f no podría retener ni generalizar. **El supuesto es correcto y la
   deducción es falsa**: son 4 casillas, pero los 32 estímulos **se agrupan en ellas por familia**, porque las variantes
   comparten los píxeles de forma de su token y en este mundo comparten también su valencia. La selección entre **66**
   celdas encuentra un par que parte los 8 tokens por valencia, y entonces 4 casillas bastan para 32 estímulos. **Me faltó
   ver que el mundo de familias es exactamente el mundo donde una tabla de pares SÍ comprime** — que es, dicho sin
   adornos, la mitad buena de la hipótesis del director, y no la vi.
2. **P-G1 apunta a PASAR en `G-REL`, no a refutar.** `g1` = 1.000 con `g1_fuerte` = 1.000 (v14.1 daba 1.000 con
   `g1_fuerte` 1.000 también, pero leyendo el signo, no la magnitud): v15f lee la variante nunca vista con el **valor
   exacto** `+1` / `−3` sin haberla mordido. **Mi predicción de §6.2 (refuta, `g1 ≤ 0.60`) va a caer.** No la cambio.
3. **La parte de P-C que yo compartía se sostiene y la que no compartía también apunta a sostenerse a medias.** v15f separa
   **6–7 de 8** contra 4–5 de v14.1, y **separa las que eran veneno (3/4 y 2/4) donde v14.1 separa 0/4 y 1/4**: el
   coordinador acertó en lo que importa. Pero **`sep/apr` sale 5.0 y 2.0, no ≤ 1.0** — v15f separa **más** viradas, no en
   menos exposiciones —, así que la letra de P-C apunta a **no cumplirse entera**, y la de P-S2 a quedar **INDECISA**
   (`n_sep` 6–7 > 5 pero `sep/apr` > 1.0: ni pasa ni refuta).
4. **La retención cae en la zona que declaré vacía a propósito:** `ok_vir` final **0.625 y 0.750**, entre mi 0.5 y el 0.8
   del coordinador. Con n = 2 no decide nadie, que es justo para lo que escribí la zona. v14.1 daba 0.500.
5. **P-S4 apunta a INDECISO, con la dirección correcta.** En `S-REL` s1 el daño existe (`ok_herm` 0.958 y 0.875 contra
   1.000 del gemelo → 0.042 y 0.125) mientras que en `S-EXC` es **0.000 en los cinco instantes**, como en la serie del
   bloque 2. Pero el Δ que decide es **10 000**, y ahí sale **0.042 < 0.10**. **No cambio el Δ ni el umbral**: el Δ está
   escrito en el bloque 2 y los cuatro se reportan siempre.
6. **El gemelo funciona con el relevo encendido y da su tasa de falso positivo:** `S-REL0` separa **0 de 8** y retiene
   1.000. La medida de separación no se dispara sola ni con la tabla.
7. **Coste:** 6.7 s/corrida contra 5.8 del bloque 2 — el bucle de 66 celdas por mordida cuesta ~15 %.

**Lo que esto cambia para la serie: nada de §1–§8.** Las predicciones quedan como están, incluida la mía, que el humo ya
señala como equivocada en dos de sus cuatro puntos. Lo que cambia es lo que voy a decir cuando la serie confirme: no
*"v15f pierde la generalización"* sino **"en un mundo con familias, la tabla de pares no compite con la lectura lineal: la
sustituye por una mejor, y el precio aparece en la retención y en las hermanas, no en la generalización"** — y eso es una
frase que yo no habría escrito ayer.

## 10. SERIE 501–520 — resultado

*(Vacío al firmar. Lo escribe el coordinador cuando lance el `Pool`.)*
