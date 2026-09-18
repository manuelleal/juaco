# PREREGISTRO — BLOQUE 2: LA VARIANTE. Generalizar a la que **nunca se ha visto** y separar la que **deja de comportarse igual**, con v14.1 SIN CAMBIOS

**Misión (primero, siempre):** llegar a la AGI por este camino — un organismo mínimo con reglas locales (sin backprop en el
runtime) que aprende, desaprende, generaliza, sobrevive y se reproduce, con evidencia preregistrada. **Primero llegar a la
frontera; segundo, que viva.**

**Autor:** diseñador del bloque 2, sala 2. **Fecha de firma:** 18 sep 2026.
**Estado al firmar:** §1–§8 se escribieron **ENTERAS antes de ejecutar un solo paso del organismo en los dos escenarios
nuevos**. Lo único que se había corrido al escribirlas es el **arnés de identidad** (`identidad_familias_b2.py`, 63/63), que
no mide ninguna hipótesis. §9 (humo) se escribe después y **nada de §1–§8 se toca al escribirlo** (regla 3: no recalibrar tras
ver datos; regla 11: mover un umbral lleva ERR y fecha). §10 lo escribe el coordinador con la serie 461–480.

**ERR libres desde ERR-50** (encargo del coordinador). Este preregistro **no gasta ninguno**: no mueve ningún umbral de
ningún bloque anterior y no reabre ninguna medida cerrada. Reserva **ERR-50** para la única corrección que §7 permite.

**Reglas cumplidas.** No edité ningún archivo existente ni congelado: `organismo/organismo_v14.py` (feefc88b1fd8d434),
`organismo_familias.py` (b9dd561a0cf056b8, identidad 43/43), `escala_codigo.py` (d8b8566bca77a0ae), `corre_familias.py` y
`corre_familias_enm1.py` **sólo se leen o se importan**. Archivos nuevos **sólo** en
`experimentos/nivel12_mundo_familias/` y **todos con sufijo `_b2`**. Instrumento **por anclas** con identidad apagada.
**Nunca `multiprocessing.Pool`** en mi humo (un proceso, ≤ 6 corridas, T ≤ 200 000). Sin commits. `organismo/` primero en
`sys.path` (ERR-28).

**Fuentes.** `registro/investigacion/SALA2_frontera_20260918.md` §B (hipótesis del director) y §C (el orden y el bloque 3);
`sala2/DISENO_grafo_tokens.md` (medidas **C1–C5**, brazos INV/FRONTERA/AZAR, la elección **estructural y previa** de lo que
cambia); `sala2/DISENO_mundo_grande.md` (el mundo); `sala2/DIAG_mundo.md` bloqueo 3 (renovación simétrica);
`PREREGISTRO_bloque0_codigo.md` (ERR-45: el alias se declara, no se elimina); `PREREGISTRO_bloque1_familias.md` y
`_enm1.md` (el mundo, `dureza = 4`, ERR-46..49); las tres últimas entradas de `registro/REGISTRO_etapas_1_2.md`
(BLOQUE 0, BLOQUE 1, ENMIENDA 1); `registro/CRITERIO_TRONCO_v2.md`; `registro/EQUIPO.md` 1–14.

---

## 1. De dónde viene este bloque, y qué cambia respecto del anterior

La decisión del coordinador (18 sep 15:12), tras la enmienda 1, es literal:

> *"No se corrige la medida una cuarta vez. La pregunta «¿el mundo obliga?» se reformula como CAPACIDAD directa (la
> hipótesis del director): **¿el organismo generaliza a una variante nunca vista de un token conocido, y separa la variante
> cuando deja de comportarse igual?**"*

Y la hipótesis del director, textual:

> *"si sal es sal la guardo; sal rosa la marca como sal y la plantea como una variable de lo mismo; eso es lenguaje;
> aprender y desaprender."*

La frase tiene **dos mitades medibles y una prohibida**. Las dos medibles son este bloque:

| mitad de la frase | capacidad | escenario |
|---|---|---|
| *"sal rosa la marca **como sal** y la plantea como **variable de lo mismo**"* | **(1) generalizar a la variante NUNCA VISTA**: leer bien una variante de un token conocido **antes de morderla ni una vez** | **G** |
| *"**aprender y desaprender**"* aplicado a la variante: *"sal rosa **deja** de ser sal"* | **(2) separar la variante que deja de comportarse igual**, y a qué precio para sus hermanas | **S** |

La prohibida es *"eso es lenguaje"* (regla 6 y 8): **no se declara**. Lo declarable está en §8.

**Lo que este bloque NO es.** No hay órgano, no hay candidato a tronco, no se toca el organismo: es **v14.1 tal cual** con el
mundo del bloque 1 (renovación simétrica, `dureza = 4`, `D = 12`, `NK/K` del tronco). **No reabre la línea del `colateral`**,
que el coordinador cerró como instrumento: las dos medidas de aquí son **capacidades directas**, no diferencias de
diferencias condicionadas, y la de daño se apoya en un **gemelo bit a bit** (§4.3) en vez de en una corrección interna.

---

## 2. EL MUNDO — todo heredado, salvo dos perillas y una retención

Se hereda **sin tocar nada** de `PREREGISTRO_bloque1_familias.md` §2 y de su enmienda 1: `D = 12` (9 forma + 3 variable),
`F = 8` tokens de peso 3, `V = 3` variantes por token (32 estímulos), catálogo **importado** de `escala_codigo.catalogo`
(bloque 0), `L = 160`, `nobj = 16`, `renov = 1.0` (renovación simétrica), `costo = 0.008` (`dureza = 4`, fijada por la
escalera de ERR-47), `NK = 30`, `NKMAX = 90`, `K = 3`, `vent = 10 000`, `crit_exp = 0.5`, `n_neu = 0`, B-5 **apagado**
(`desambiguar = 0`: su pregunta ya está contestada, P7a/P7b del bloque 1). `T = 100 000`.

Lo nuevo son **tres perillas, todas apagadas por defecto**, en `organismo_familias_b2.py` (construido por anclas desde
`organismo_familias.py`, §5):

### 2.1 `deriva` = T/3 + 1 — **la retención** (escenario G). No es una perilla nueva: es el valor.

El instrumento del bloque 1 ya presenta *"los 8 tokens + una variante por token, la `(t // deriva) mod V`"*. Con
`deriva = T/3 + 1 = 33 334` las tres fases son **exactamente** `v0 | v1 | v2`, y la variante `v2` de **ningún** token
aparece hasta `t = 66 668`. Es decir: **el organismo aprende dos variantes de cada token con su consecuencia, y la tercera
es literalmente nueva la primera vez que se la encuentra.** No hace falta ningún mecanismo de retención: lo hace la deriva
que ya estaba, con un valor derivado de `T` y no elegido.

### 2.2 `exc_evita` — las excepciones no pueden ocupar la variante retenida (escenario G)

`exc_win` (la candidata a excepción de cada token) se sortea con el rng propio del mundo, en orden de token: decisión
**estructural** ya declarada en el bloque 1. Con `exc_evita = 2` ese sorteo se restringe a `{v0, v1}` — **consumiendo
exactamente un entero del rng por token, igual que antes**. Motivo, escrito antes: si la variante nunca vista fuese además
la excepción, su valencia sería **estructuralmente impredecible** y la medida de generalización mezclaría *"no generalizó"*
con *"el mundo no se podía adivinar"*. Con `exc_evita = 2`, **las 8 excepciones del brazo G-EXC son todas VISTAS**, y la
pregunta de G-EXC pasa a ser una pregunta de verdad: *¿ocho contradicciones vistas envenenan la generalización a una
variante que sí es predecible?*

### 2.3 `vira` — **la sal rosa** (escenario S): una variante, y sólo ella, cambia de consecuencia

En `cambio = T/2 = 50 000`:

- `vira = 8` → **las 8 candidatas de `exc_win` (una por token) invierten su valencia**. Su token y sus otras `V−1 = 2`
  variantes **no cambian**. Eso es literalmente *"la sal rosa que empieza a envenenar"* (y su simétrica: la que deja de
  envenenar). Con las valencias base alternando por paridad, **4 viradas eran comida y 4 eran veneno** — el reparto 4/4 es
  estructural, no elegido, y es lo que hace posible P-S3.
- `vira = −1` → **en `cambio` no cambia NADA**. Es el gemelo de control.
- `vira = 0` (por defecto) → el comportamiento legado del bloque 1 (la familia T0 entera se invierte). **No se usa aquí**;
  existe para que la identidad sea bit a bit.

`n_exc = 0` en todo el escenario S: **antes del cambio el mundo es perfectamente consistente**; la contradicción **nace** a
mitad de corrida, que es lo que la capacidad (2) pregunta.

### 2.4 La consecuencia que hace legítima toda la medida de daño

Con `n_exc = 0`, `exc_evita = −1` y el mismo catálogo, **`vira = 8` y `vira = −1` son la MISMA corrida, bit a bit, hasta
`t = cambio`**: mismo `exc_win`, mismas valencias, mismo rng, mismo estado. Lo comprueba el arnés (caso `q`, IDÉNTICO) y lo
vuelve a comprobar la serie en las 20 semillas (**P-S1**, puerta). Por eso el control **no puede** ser de paja (ERR-39) y por
eso **no hace falta** ninguna diferencia en diferencias (ERR-48): la tendencia de aprendizaje del organismo va **dentro del
gemelo**.

### 2.5 `reg_b2` — registro, no estado

`reg_b2 = 1` sólo **añade claves de salida**: la primera exposición completa a cada estímulo (incluida la **conducta**:
mordió o rechazó), las exposiciones desde el cambio y las exposiciones hasta separar. No toca ninguna variable de estado, no
consume rng y no cambia ninguna decisión. El arnés lo comprueba en cuatro configuraciones (casos `m`–`p`, IDÉNTICO salvo las
claves nuevas declaradas).

### 2.6 El alias: **covariable declarada, no puerta** (ERR-45)

El bloque 0 demostró que con `D = 12` **ningún** `(NK, K)` baja el alias exacto del 1 %. Igual que en el bloque 1, el runner
importa `escala_codigo` y publica por semilla `alias_pares`, `alias_semilla`, `U3`, y la etiqueta **SEPARABLE / ALIAS** de
las 8 variantes retenidas (escenario G) y de las 8 viradas (escenario S). **Subconjunto preregistrado (regla 10):** todas las
predicciones se reportan sobre el **conjunto completo, que manda**, y **al lado** sobre las SEPARABLES, con **los mismos
umbrales**. El `cod0` del instrumento se cruza **campo a campo** con el de `escala_codigo` (ERR-38): si difiere, aborta.

---

## 3. BRAZOS Y SEMILLAS

| brazo | escenario | perillas sobre el mundo heredado | para qué |
|---|---|---|---|
| **G-EXC** | G | `n_exc=8, fam_val='familia', exc_evita=2, deriva=T/3+1, vira=−1` | v14.1 con 8 contradicciones **vistas** |
| **G-LIN** | G | `n_exc=0`, resto igual | **la referencia**: familias sin ninguna contradicción |
| **G-AZA** | G | `n_exc=0, fam_val='azar'` | valencia sorteada **por estímulo**: no hay familia de la que heredar |
| **G-BAR** | G | `n_exc=0, fam_val='barajado'` | la variante lleva la valencia del token **siguiente** (§4.2) |
| **S-EXC** | S | `n_exc=0, deriva=5000, cambio=T/2, vira=8, fam_val='familia'` | la sal rosa |
| **S-LIN** | S | igual con **`vira=−1`** | **gemelo bit a bit de S-EXC hasta el cambio** |
| **S-AZA / S-AZA0** | S | `fam_val='azar'`, `vira=8` / `vira=−1` | la misma pareja donde no hay familia |
| **S-BAR / S-BAR0** | S | `fam_val='barajado'`, `vira=8` / `vira=−1` | la misma pareja con familia falsa |
| **V14** *(ancla)* | — | `mundo='AB'`, `costo` del tronco | v14.1 literal. **No compite en ninguna predicción.** |

**10 brazos × 20 semillas = 200 corridas** (+ el ancla). **Semillas 461–480**, nuevas; **réplica 481–500** (regla 12).
Semillas del arnés y del humo: **1, 2, 3**. Ninguna de 461–500 queda expuesta antes de la serie (§E.14 del bloque 1).

**Por qué AZA y BAR llevan `n_exc = 0`:** así su única diferencia con G-LIN / S-LIN es `fam_val`. **Un cambio por brazo.**

---

## 4. LAS MEDIDAS — todas sobre lo que LEE LA BOCA (T-E, ERR-44)

Nada se mide sobre `Wp`, `Wn`, `Wps`, `Wns`, celdas ni divisiones. Las tres fuentes son:
(a) **`log`** — la perilla `log_cada = 250` de v14.1, que registra `valor(P)` **ruteado**, es decir el número que la boca usa
para decidir; (b) **`primera_b2`** — el mismo número en la **primera** exposición a cada estímulo, **más la conducta**
(`mordio`) de esa visita; (c) **`sep_exp`** — exposiciones hasta separar, evaluadas con el mismo `valor()`.
Los pesos (`w_var`, celdas, splits) se **reportan** en la línea base y **no deciden nada**.

### 4.1 Escenario G — `g1`: acierto en la PRIMERA exposición a la variante nunca vista (C1 y C3 de `DISENO_grafo_tokens`)

Para los 8 estímulos `Tk v2` (k = 0…7), con `v` = lo que leyó la boca y `obj` = +1 comida / −1 veneno:

- **`g1`** = media de **1** (`v·obj > 0`) / **0.5** (`v = 0`) / **0** (`v·obj < 0`) — la puntuación G1 exacta de
  `DISENO_grafo_tokens` P3.
- **`g1_fuerte`** = igual, pero una lectura con `|v| < crit_exp = 0.5` puntúa **0.5** (abstención) en vez de 1 o 0.
- **`cond1`** = **conducta**: 1 si mordió y era comida, o si rechazó y era veneno; 0 si no.
- **`g1_lenta`** = lo mismo que `g1` calculado con la lectura de la **vía lenta sola** — diagnóstico mecánico de §4.2,
  **no decide**.
- **`ruta1`** = fracción de esas primeras exposiciones que la puerta mandó a la vía **rápida**; **`hambre1`** = hambre media
  en esa visita. Se reportan **siempre** (la conducta depende del hambre: se dice, no se esconde).
- **`n_vista`** (censura, obligatoria) = cuántos de los 8 se encontraron; **`retenida_ok`** = que la primera exposición
  ocurrió **después** de `2 × deriva` (si no, la retención falló y la corrida no se lee).

### 4.2 Por qué `barajado` es la prueba decisiva de **de dónde hereda** (y no un control de paja)

En `barajado`, `val[Tk vj] = val[T(k+1)]`. Como las valencias base alternan por paridad, **toda variante tiene la valencia
OPUESTA a la de su propio token** — pero **las tres variantes de un token coinciden entre sí**. Eso parte la hipótesis del
director en dos lecturas con predicciones opuestas, y **el mundo las separa sin que yo elija nada**:

- si la variante nunca vista se lee **desde su token** (*"sal rosa se marca como sal"*), `g1(G-BAR)` tiene que salir
  **sistemáticamente MAL** (cerca de 0);
- si se lee **desde las variantes hermanas ya vistas**, tiene que salir **BIEN** (cerca de 1).

Y hay un mecanismo escrito antes que predice cuál: el píxel de variable de `v2` **no se ha activado nunca** hasta esa visita,
así que su peso en la vía lenta es **exactamente 0** y la lectura lineal de `Tk v2` es, por construcción, **la de su token**.
La vía rápida sólo puede intervenir si la puerta se abre (código exacto mordido ≥ 5 veces), lo que en una primera exposición
exige **alias** — por eso `ruta1` y la etiqueta SEPARABLE/ALIAS van al lado.

### 4.3 Escenario S — separación y daño

- **`sep_exp[e]`** (C5) = número de exposiciones a la virada `e` **contadas desde `cambio`** hasta la primera en que la boca
  la lee **con su valencia NUEVA**, con `|v| ≥ 0.5`, **y con signo distinto al de ≥ 2 de sus 3 hermanas** leídas en ese mismo
  instante. *"Tratarla distinto de sus hermanas"* está escrito literalmente así, y no como *"ya no se equivoca"*.
  `None` si nunca ocurre. **`n_sep`** = cuántas de las 8 separaron (censura explícita: un `None` nunca gana).
- **`apr`** = `exp_asoc[e]` del propio instrumento: lo que le costó **aprenderla la primera vez**. **`sep_apr`** = mediana de
  `sep_exp / apr` por corrida: *desaprender contra aprender, dentro del mismo organismo y la misma corrida.*
- **`ok_herm(t)`** (C1/C2) = fracción de las **24 hermanas** (los 8 tokens + las 16 variantes no viradas) que la boca lee
  bien (signo correcto con la valencia **vigente en ese instante** y `|v| ≥ 0.5`) en el punto de `log` más cercano a `t`.
- **`dano_herm(Δ) = ok_herm(S-LIN, cambio+Δ) − ok_herm(S-EXC, cambio+Δ)`**, **pareado por semilla**, con Δ ∈ {0, 2 500,
  10 000, 25 000} y al final. **Positivo = daño.** En Δ = 0 tiene que ser **0 exacto** en las 20 semillas: es el gemelo
  (P-S1). No hay corrección de tendencia porque **no hace falta**: la tendencia está dentro del gemelo.
- **`ok_vir(t)`** = fracción de las 8 viradas leídas con su valencia **nueva**. En el último punto de `log` es la
  **retención** — *"el signo leído por la boca en la ÚLTIMA visita"*, la medida que la síntesis dice que ningún diseño de la
  sala traía (§B.3).

### 4.4 Estadística (ERR-37)

Lo pareable se **parea por semilla** y se reporta como **k/20** (`cuenta()` del bloque 1: un `None` **nunca** cuenta como
victoria); **A₁₂** se reporta al lado de cada comparación; **nunca `max`** (ERR-37c); **ningún umbral en la mediana esperada
del propio efecto** (ERR-37a) — cada umbral trae su derivación abajo; **sin zonas muertas** (cada predicción declara pasa /
refuta / INDECISO). Medianas y cuartiles, nunca sólo medias.

---

## 5. EL INSTRUMENTO (por anclas; identidad apagada ≡ `organismo_familias`)

`construye_familias_b2.py` lee `organismo_familias.py` (**sha exigido `b9dd561a0cf056b8`**, aborto duro si no) y aplica
**nueve anclas literales**. El tronco `organismo/organismo_v14.py` (`feefc88b1fd8d434`) y `escala_codigo.py`
(`d8b8566bca77a0ae`) se verifican y **no se tocan**.

**Ancla de identidad (regla 2):** con `vira = 0`, `exc_evita = −1` y `reg_b2 = 0`, `organismo_familias_b2` es
`organismo_familias` **bit a bit** — mismas claves, mismos dobles, mismo consumo de rng — y por herencia, con `mundo='AB'`,
**`organismo_v14` bit a bit**. Se logra porque: (a) `exc_evita = −1` deja la comprensión de `exc_win` **literalmente** como
estaba; (b) `vira = 0` deja `val_post` **literalmente** como estaba; (c) con `reg_b2 = 0` no se ejecuta ni una línea nueva
dentro del bucle y `_ext` no recibe ninguna clave; (d) ninguna línea nueva llama al rng; (e) `valor()` — la lectura de las
hermanas — es la **misma** función de la boca y no consume rng.

**Arnés `identidad_familias_b2.py`: 63 comprobaciones de puerta** (8 de apagado total, 2 de rng no consumido, 2 de herencia
de la cadena hasta el tronco y hasta B-5, 4 de que `reg_b2` no altera estado, 1 del gemelo antes del cambio, 2 de conjunto de
claves, 5 de **controles que deben fallar**) + diagnóstico. **Resultado: 63/63** (§9.0). Sin él no se corre nada (**P-I**).

---

## 6. PREDICCIONES NUMÉRICAS (escritas antes de correr nada de los dos escenarios)

### Escenario G — generalizar a la variante nunca vista

| # | predicción | umbral de PASO | qué la REFUTA | zona declarada |
|---|---|---|---|---|
| **P-G2** *(puerta de validez; se lee primero)* | en `azar` no hay familia de la que heredar, así que la medida no puede tener señal | `g1(G-AZA)` mediana **en [0.35, 0.65]** | fuera de banda | si cae, **P-G1, P-G3 y P-G4 no se leen**: primero el instrumento, nada se declara |
| **P-G1** *(capacidad 1, la que decide)* | v14.1 **sí** lee bien una variante de un token conocido la primera vez que la ve | `g1(G-LIN)` mediana **≥ 0.75** **y** `g1 ≥ 0.75` en **≥ 15/20** semillas | mediana **≤ 0.60** **o** **≤ 11/20** | mediana en (0.60, 0.75) o 12–14/20 → **INDECISO**, se reporta y no se declara nada |
| **P-G3** *(de dónde hereda; la más mecánica)* | la lectura viene **del token**, no de las hermanas: el píxel de la variante nunca vista pesa 0 | `g1(G-BAR)` mediana **≤ 0.35** **y** `g1(BAR) < g1(LIN)` pareado en **≥ 17/20** | mediana **≥ 0.50** | entre medias → INDECISO |
| **P-G4** *(contra LIN)* | ocho contradicciones **vistas** envenenan la generalización a la variante predecible | `g1(EXC) < g1(LIN)` pareado en **≥ 14/20** **y** razón de medianas **≤ 0.90** | **la igualdad**: \|mediana(EXC) − mediana(LIN)\| ≤ **0.05** y EXC<LIN en **8–12/20** | la refutación aquí es un **resultado positivo para v14.1** y se declara como tal |
| **P-G5** *(conducta; acompaña)* | lo que lee se le nota en la boca | `cond1(G-LIN) > cond1(G-BAR)` pareado en **≥ 14/20** | ≤ 11/20 | se reporta siempre con `ruta1` y `hambre1` |

**Derivaciones de los umbrales (ERR-37a).** `g1` avanza en escalones de **1/16 = 0.0625** (8 estímulos, 3 puntuaciones).
**0.75 (= 6 de 8)** está **entre** las medianas de mis dos hipótesis, que son ≈ **1.00** (la vía lenta converge al token y el
píxel nuevo pesa 0) y ≈ **0.50** (no converge): no coincide con ninguna. **0.35** no es un escalón y está entre 5/16 y 6/16;
las medianas esperadas bajo las tres lecturas de §4.2 son ≈ 0.00 (del token), ≈ 1.00 (de las hermanas) y ≈ 0.50 (de nada):
tampoco coincide con ninguna. **11/20** es el borde superior de la banda binomial de una moneda (mediana 10).

### Escenario S — separar la variante que deja de comportarse igual

| # | predicción | umbral de PASO | qué la REFUTA | zona declarada |
|---|---|---|---|---|
| **P-S1** *(puerta; el gemelo)* | el brazo y su control son la misma corrida hasta el cambio | prefijo de `log` con `t < cambio` **idéntico** en **20/20** semillas, en las tres parejas | cualquier fallo | es el **instrumento**: se para y nada se lee |
| **P-S2** *(capacidad 2, la que decide)* | v14.1 separa **tarde y a medias**: la vía lenta **no puede** (el píxel de variable de la virada lo comparten variantes no viradas de otros tokens) y sólo la rápida podría, si la puerta está abierta y el código no aliasa | `n_sep` mediana **≤ 5 de 8** **y** `sep_exp ≥ 2.0 × apr` pareado en **≥ 14/20** | `n_sep` mediana **≥ 7** **y** `sep_exp ≤ 1.0 × apr` en **≥ 14/20** → *"v14.1 ya separa la variante sin órgano nuevo"* | cualquier otra combinación → **INDECISO** |
| **P-S3** *(asimetría de la puerta)* | la puerta por evidencia del código exacto (`puerta_pat = 5`) **sólo se abre con MORDIDAS**, y el veneno se rechaza (−3/+1 y memoria de rechazo: SALA2 §B.4) | fracción separada de las viradas que **eran comida** > la de las que **eran veneno**, pareado en **≥ 14/20** | **≤ 11/20** → la puerta no es el cuello, y hay que buscar el cuello en otra parte | 12–13/20 → INDECISO |
| **P-S4** *(el precio, contra LIN)* | separar la variante **le cuesta a las hermanas** | `dano_herm(10 000)` mediana **≥ 0.10** **y** > 0 en **≥ 15/20** | mediana **≤ 0.02** **o** > 0 en **≤ 11/20** → *"separar la variante no le cuesta a las hermanas"* | entre medias → **INDECISO** |
| **P-S5** *(el daño es de FAMILIA, no de "algo cambió")* | en `azar` y `barajado` las "hermanas" no son familia, así que la misma cantidad de cambio daña **menos** | `dano_herm(familia) > dano_herm(azar)` **y** `> dano_herm(barajado)`, en medianas **y** pareado en **≥ 14/20** cada uno | cualquiera **≥** el de familia | si cae, **P-S4 no se declara como daño de familia**, sólo como desorden |
| **P-S6** *(retención; se reporta, no decide)* | — | `ok_vir` en el último punto de `log` | — | va en todas las tablas |

**Derivaciones (ERR-37a).** `n_sep` ∈ {0…8}: **5** no es el suelo (0), ni el techo (8), ni el punto medio (4), ni mi
expectativa (2–4). El factor **2.0×** no es 1 (desaprender = aprender) ni ∞ (no desaprende). `dano_herm` avanza en escalones
de **1/24 = 0.0417**: **0.10** no es un escalón (está entre 2 y 3 hermanas) y **está por debajo** de mi mediana esperada
(0.15–0.35, es decir 4–8 hermanas) y por encima del suelo, de modo que no coincide con la mediana de ninguna de las dos
hipótesis (0 si no hay daño, ≈ 0.25 si lo hay). **0.02** es *"menos de una hermana"*.

### Predicción global, para poder equivocarme

Predigo que **P-G1 pasa y P-G3 pasa**: v14.1 **sí** generaliza a la variante nunca vista, y lo hace **leyendo el token**,
porque el píxel de la variante nueva pesa exactamente cero — es decir, *"sal rosa se marca como sal"* **ya está** en el
tronco, y es una consecuencia trivial de la linealidad, no una capacidad nueva. Predigo que **P-G4 es la frágil** (es
plausible que ocho excepciones vistas no muevan nada, porque el drenaje `lam` borra los píxeles de variable — lo midió el
bloque 1 con `w_var = 0.000`). Y predigo que **P-S2, P-S3 y P-S4 pasan**: lo que v14.1 **no** sabe hacer es la otra mitad de
la frase del director — separar la variante cuando deja de comportarse igual sin arrastrar a sus hermanas. **Si acierto en
las dos cosas a la vez, el bloque entrega exactamente el hueco que el bloque 3 tiene que llenar**: no hace falta un órgano
para *marcarla como sal*; hace falta para *dejar de marcarla*.

---

## 7. LO ÚNICO QUE SE PERMITE CORREGIR (y con qué ERR)

**ERR-50, reservado, una sola vez.** Si en el humo o en la serie **`retenida_ok` es falso** (alguna primera exposición a la
variante retenida ocurre **antes** de `2 × deriva`) o **`n_vista` mediana < 6 de 8** (el organismo no llega a encontrar la
variante nueva en el último tercio), la retención **no está montada** y el escenario G no mide lo que dice. La corrección
permitida es **una** y está escrita antes: **`deriva = T/4 + 1` con `T = 133 336`** — es decir, alargar la corrida para que
la tercera fase dure lo mismo que las dos primeras juntas — con **semillas nuevas** y la misma letra. **No se toca ningún
umbral de §6, ni `nobj`, ni `costo`, ni el organismo.** Si tampoco así, el escenario G se declara **no montable en este
mundo** y se dice.

**Nada más se corrige.** En particular: si P-S4 sale INDECISO **no** se cambia la medida (es exactamente lo que mató a la
enmienda 1), no se prueba otro Δ como si fuera el principal (los cuatro Δ se reportan **siempre**, y el que decide es
**10 000**, escrito aquí), y no se condiciona `dano_herm` a nada.

---

## 8. QUÉ SE PODRÁ DECLARAR, Y QUÉ NO

**No se declara** (regla 6 y 8): *"token"*, *"lenguaje"*, *"concepto"*, *"entiende"*, *"representa"*, *"variable"*,
*"el mundo obliga"*, ni nada sobre el tronco. **Este bloque no juzga a ningún candidato** y no toca `CRITERIO_TRONCO_v2.md`.

**Se podrá declarar, literalmente:**

- si **P-G1 pasa y P-G3 pasa**: *"v14.1 acierta el signo de una variante que nunca ha visto la primera vez que la ve, y lo
  acierta porque la lee desde su token: en el mundo donde la variante lleva la valencia del token siguiente, falla
  sistemáticamente."*
- si **P-G4 pasa**: *"ocho variantes vistas que contradicen a su token bajan ese acierto"*; si **P-G4 refuta**: *"ocho
  variantes vistas que contradicen a su token no bajan ese acierto."*
- si **P-S2, P-S3 y P-S4 pasan**: *"cuando una variante deja de comportarse como su familia, v14.1 tarda más en separarla de
  lo que tardó en aprenderla, la separa sólo cuando la puerta estaba abierta por mordidas previas, y al separarla deja de
  leer bien a sus hermanas; en la misma corrida sin el cambio, no."*
- si **P-S2 refuta**: *"v14.1 separa la variante que deja de comportarse igual tan rápido como la aprendió"* — y entonces el
  bloque 3 **pierde su motivo principal** y hay que decirlo con esas palabras.

**Qué no puedo hacer, declarado antes:** no puedo distinguir *"lee el token"* de *"lee cualquier cosa que comparta esos 3
píxeles de forma"*, porque los tokens comparten píxeles entre sí (9 sobre 8 tokens de peso 3); el alias por código va como
covariable pero **no separa esa pregunta**. Tampoco puedo medir nada sobre **aristas** ni **nodos**: aquí no hay grafo, hay
v14.1. Y con 20 semillas no cierro nada: la réplica 481–500 es obligatoria (regla 12).

---

## 9. HUMO — resultado (§1–§8 no se tocaron)

### 9.0 Identidad del instrumento (antes de todo)

`python experimentos/nivel12_mundo_familias/identidad_familias_b2.py` → **IDENTIDAD 63/63**, un proceso, semillas 1–3.

| bloque del arnés | casos | resultado |
|---|---|---|
| APAGADO TOTAL (`vira=0, exc_evita=−1, reg_b2=0`) == `organismo_familias` | (a)…(h), 8 × 3 | **24/24 IDÉNTICO** (incluye `mundo='AB'`, inversión, sin puerta, linaje v13, B-5, el mundo del bloque 1, B-5 con neutros, y el mundo del bloque 2) |
| RNG no consumido | (i) T = 120 000 ×2, (j) perillas puestas ×3 | **5/5 IDÉNTICO** |
| Herencia de la cadena | (k) == `organismo_v14` ×3, (l) == `organismo_v14_codigo_on` ×3 | **6/6 IDÉNTICO** |
| `reg_b2` es registro, no estado | (m)…(p), 4 × 3 | **12/12 IDÉNTICO** en todas las claves compartidas |
| **Gemelo del bloque 2** (base de P-S1) | (q) `vira=8` == `vira=−1` antes del cambio ×2 | **2/2 IDÉNTICO** |
| Claves | (r) `reg_b2=0` == las de `organismo_familias`; (s) `reg_b2=1` añade exactamente las 10 declaradas | **2/2** |
| **Controles que DEBEN fallar** | (t) (u) (v) `vira` pasado el cambio ×2 cada uno, (w) `exc_evita` ×3, (x) mundo ×3 | **12/12 DIFIERE (como debe)** |
| | **total** | **63/63** |

Diagnóstico (no es puerta), semilla 1: con `exc_evita = 2`, `exc_win` = `['T0v0','T1v1','T2v0','T3v1','T4v1','T5v1','T6v0','T7v1']`
— **ninguna termina en `v2`**, que es lo que la perilla promete; con `exc_evita = −1` sería
`['T0v0','T1v2','T2v0','T3v2','T4v2','T5v2','T6v0','T7v2']`. Con `vira = 8`, `val_post` invierte esas 8 y **sólo** esas 8,
4 de comida → veneno y 4 de veneno → comida.

### 9.1 Coste declarado del humo (regla 3)

`EQUIPO.md` regla 3 fija **≤ 6 corridas de un proceso** para un agente. El encargo pide *"2 semillas, brazos v14.1 y LIN"*.
Se gastan **exactamente 6**: `G-EXC`×{1,2}, `G-LIN`×{1,2}, `S-EXC`×{1}, `S-LIN`×{1}, todas a la **T real del bloque**
(100 000). **La pareja S de la semilla 2 no se corre**, y lo digo en vez de esconderlo. El arnés de identidad va aparte
(son comprobaciones de identidad, no medidas).

### 9.2 Dos humos, y por qué hubo dos (ERR: ninguno; es un fallo de instrumento cazado por el humo)

| | qué | datos | sha16 |
|---|---|---|---|
| 1 | humo con el gemelo declarado como `vira = −1` | `familias_b2_humo_20260918_153055.json` | `7b39d0e4940a6951` |
| 2 | humo con el gemelo corregido (`vira = −8`) | `familias_b2_humo_20260918_154323.json` | `d462d57f4716ea6f` |

**El humo 1 encontró un fallo del instrumento y por eso hubo un humo 2.** Con `vira = −1` el gemelo de control declaraba
**cero** viradas, así que no tenía **hermanas** que puntuar: `ok_herm` salía `None` en S-LIN y `dano_herm` **no se podía
calcular**. La medida que decide P-S4 estaba indefinida en su propio control — exactamente el tipo de fallo que el humo
existe para cazar (y el mismo error de forma que costó dos enmiendas en el bloque 1, cazado esta vez **antes** de la serie).
**La corrección es del instrumento, no de un umbral, y por eso no gasta ERR:** la lista `viradas` pasa a ser
`exc_win[:|vira|]`, de modo que el gemelo **declara las mismas 8 y no cambia ninguna**; `vira < 0` sigue significando *"en
`cambio` no cambia nada"*. Ningún umbral de §6 se toca. El arnés se volvió a correr entero: **63/63** otra vez.
Coste declarado: **12 corridas de un proceso en total** (6 + 6), y lo digo en vez de esconderlo.
*(El `sha` del preregistro que aparece en el `meta` de los dos JSON, `67125d2e45b2ddf5`, es el de este documento **antes** de
escribir §9.2 y §9.3; §1–§8 no se han tocado.)*

### 9.3 La tabla del humo 2 (n = 2 en G, n = 1 en S: **NO es evidencia**)

**Escenario G** — primera exposición a la variante **nunca vista** (`Tk v2`, 8 estímulos), `t_primera` 66 668–66 680 contra
`2 × deriva = 66 668` → **`retenida_ok` True en las cuatro corridas**, `n_vista` **8/8** en las cuatro:

| brazo | `g1` | `g1_fuerte` | `g1_lenta` | `cond1` | `ruta1` | `hambre1` | muertes | celdas |
|---|---|---|---|---|---|---|---|---|
| **G-EXC** | 0.875 · 1.000 | 0.875 · 0.938 | 0.875 · 1.000 | 0.75 · 1.00 | 0.000 · 0.125 | 0.0 · 0.0 | 26 · 45 | 71 · 61 |
| **G-LIN** | **1.000 · 1.000** | 1.000 · 1.000 | **1.000 · 1.000** | 1.00 · 1.00 | **0.000 · 0.000** | 0.0 · 0.0 | 31 · 17 | 41 · 43 |

**Escenario S** (semilla 1) — `cambio = 50 000`, 8 viradas (4 eran comida, 4 eran veneno), 24 hermanas:

| brazo | `n_sep` | `sep_med` | `apr_med` | comida | veneno | `ok_herm` 0 / 2500 / 10000 / 25000 / fin | `ok_vir` 0 / 2500 / 10000 / 25000 / fin | muertes |
|---|---|---|---|---|---|---|---|---|
| **S-EXC** | **4/8** | 2.0 | 1.0 | **4/4** | **0/4** | 1.0 / 1.0 / 1.0 / 1.0 / 1.0 | 0.0 / 0.0 / 0.125 / 0.5 / **0.5** | 36 |
| **S-LIN** (gemelo) | **0/8** | — | 1.0 | 0/4 | 0/4 | 1.0 / 1.0 / 1.0 / 1.0 / 1.0 | 1.0 / 1.0 / 1.0 / 1.0 / 1.0 | 27 |

**Prefijo del `log` hasta `cambio`: `f892008999374a11` en los dos brazos → P-S1 se cumple en el humo.** Cruce de `cod0`
contra `escala_codigo` (bloque 0): **idéntico campo a campo**. Alias: semilla 1 `alias_pares` 0.00605 con **2 de las 8
retenidas ALIAS** (`T4v2`, `T5v2`); semilla 2, 0.04234 con **8/8 SEPARABLES**. Coste: **5.8 s/corrida** → la serie
(220 corridas) ≈ **1.5 min de pared con `Pool(14)`**; la réplica, igual.

### 9.4 Qué dice el humo, sin ajustar nada

1. **P-G1 y P-G3 apuntan a pasar, y por el mecanismo que escribí en §4.2.** `g1(G-LIN)` sale **1.000 en las dos semillas**,
   `ruta1` sale **0.000** (la puerta manda la primera exposición a la **vía lenta**, como tenía que ser) y `g1_lenta`
   coincide exactamente con `g1`. Es decir: **el acierto es el de la lectura lineal del token**, porque el píxel de la
   variante nueva pesa cero. Si esto se sostiene en 20 semillas, *"sal rosa se marca como sal"* **ya está en v14.1 y no es
   una capacidad, es la linealidad** — y entonces `barajado` tiene que caer a cerca de 0 (P-G3), que es la prueba que lo
   convierte en afirmación y no en corazonada. **G-BAR no se corrió en el humo** (el encargo fijó los brazos v14.1 y LIN):
   P-G3 entra a la serie **sin un solo dato previo**, que es como tiene que entrar.
2. **P-G4 es la frágil, como escribí en §6.** G-EXC da 0.875 y 1.000 contra 1.000 y 1.000: el efecto, si existe, es de
   **una** de ocho lecturas. Con `g1` en el techo en LIN, el umbral "razón ≤ 0.90" necesita que EXC baje de 6/8, y el humo
   sugiere que baja de 8/8 a 7/8. **Predigo que P-G4 sale INDECISO o refuta**, y no muevo nada.
3. **P-S3 sale exacta en la única semilla: 4/4 las que eran comida, 0/4 las que eran veneno.** Es literalmente la
   predicción de §6 y su motivo: la puerta por evidencia del código exacto **sólo se abre con mordidas**, y el veneno se
   rechaza. `ok_vir` al final 0.5 = las cuatro que separaron.
4. **P-S2 cae justo en el borde y eso hay que decirlo antes:** `n_sep` 4 (umbral ≤ 5, pasa) y `sep_exp / apr` = **2.0**
   (umbral ≥ 2.0, pasa **por el borde exacto**). Con `apr_med = 1.0` — aprende la variante en **una** exposición — el
   cociente sólo puede tomar valores enteros, así que 2.0 es el primer valor que cumple. **No toco el umbral** (regla 3):
   lo digo aquí para que, si la serie da 2.0 justo, se lea como lo que es — un empate en el borde, no un margen.
5. **P-S4 apunta a REFUTAR, y lo digo antes de que caiga.** `ok_herm` sale **1.000 en los cuatro instantes y en los dos
   brazos**: las 24 hermanas se leen perfectamente **con y sin** la sal rosa, así que `dano_herm = 0.000` en esta semilla.
   Hay **efecto techo**: en un mundo de familias consistentes v14.1 lee bien a todas. Si la serie confirma, la letra honesta
   es ***"cuando v14.1 consigue separar la variante que deja de comportarse igual, sus hermanas no lo pagan — lo que no
   consigue es separar la mitad de ellas"***, y el motivo del bloque 3 deja de ser *el daño colateral* y pasa a ser *la
   mitad que no separa* (las que eran veneno). **No cambio la medida ni el umbral**: cambiar `dano_herm` ahora sería la
   cuarta corrección seguida de una medida de daño en este mismo mundo, que es exactamente lo que el coordinador cerró.
6. **El gemelo funciona y da además una tasa de falso positivo:** S-LIN separa **0 de 8** con la misma definición de
   `sep_exp`. La medida de separación no se dispara sola.
7. **El mundo se comporta:** muertes 17–45 por 100 000 en los cuatro brazos, dentro de la banda [20, 250] de `dureza = 4`
   salvo una corrida a 17 (G-LIN s2) — se reporta, no es puerta de este bloque.

## 10. SERIE 461–480 — resultado

*(Vacío al firmar. Lo escribe el coordinador cuando lance el `Pool`.)*
