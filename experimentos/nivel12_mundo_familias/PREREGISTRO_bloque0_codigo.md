# PREREGISTRO — BLOQUE 0 (0a): ¿existe un (D, NK, K) que dé un código no-aliasado para el mundo de familias?

**Misión (primero, siempre):** llegar a la AGI por este camino — un organismo mínimo con reglas locales (sin backprop en el
runtime) que aprende, desaprende, generaliza, sobrevive y se reproduce, con evidencia preregistrada. Primero llegar a la
frontera; segundo, que viva.

**Autor:** diseñador del bloque 0, sala 2. **Fecha de firma:** 18 sep 2026.
**Estado al firmar:** este documento se escribió **ENTERO antes de ejecutar `escala_codigo.py`**. Las secciones §1–§7 están
congeladas; sólo §8 (resultados) y §9 (recomendación / honestidad) se escriben después, y **nada de §1–§7 se toca al
escribirlas** (regla 3: no recalibrar tras ver datos; regla 11: mover un umbral lleva ERR y fecha).

**Qué NO es esto.** No es un candidato a tronco, no añade capacidad, no simula un solo paso del organismo. Es el instrumento
(0a) del BLOQUE 0 de `registro/investigacion/SALA2_frontera_20260918.md` §C.2 — *"la geometría del código por mundo"* —, la
misma clase de cálculo estructural (T = 0) que `registro/investigacion/sala2/diagnostico_familias4.py`,
`diagnostico_familias_sala2.py` y `estructural_generaliza_tok_sala2.py`. **No edité ningún archivo existente ni congelado.
No hay commit. No uso `multiprocessing.Pool`. `organismo/` va primero en `sys.path` (ERR-28).**

**Por qué existe.** El BLOQUE 1 (§C.2) exige el mundo de familias *"con `NK`/`K` escalados a alias < 1 %"*, y su primera
cláusula de muerte es literal: **"(i) que el alias estructural no baje de 1 % con ningún `NK`/`K` razonable → la línea pasa
al código, no al mundo"**. `DIAG_metodo.md` bloqueo 1 dice lo mismo (*"con NK/K escalados para que la tasa de alias caiga
< 1 %, calculable antes de simular"*). Hoy ese número **no existe**: `DISENO_mundo_grande.md` §1.1 midió tres valores de NK
con K = 3 fijo y encontró alias entre dos estímulos cualesquiera en **199/200, 190/200 y 179/200** semillas. Nadie barrió K.
Este documento decide, antes de escribir una línea de mundo o de órgano, **si el bloque 1 se puede correr tal como está
escrito** o si su cláusula (i) ya está activada.

---

## 1. Hipótesis

**H (la que se juzga).** *Existe al menos una combinación (D = 12, NK, K) dentro de la rejilla de §3 que, para el catálogo de
estímulos del mundo de familias de `DISENO_mundo_grande.md` §1.1, deja simultáneamente:*

- *(a) el **alias exacto** — dos estímulos distintos del catálogo con el MISMO código — por debajo del **1 % de las semillas**;*
- *(b) el **alias parcial K−1** entre estímulos de **familias distintas** **acotado** por el umbral de §4; y*
- *(c) las familias todavía **legibles** en el código: similitud media entre variantes de una misma familia **mayor** que
  entre familias, por el margen numérico de §4.*

**H¬ (la alternativa que tomo en serio, y que predigo como más probable: §5, P5).** Las tres condiciones están **en tensión
estructural**: (a) se compra afinando el código (más celdas, K mayor), y afinar el código es exactamente lo que borra (c)
— es el hallazgo B-4 de `DIAG_representacion` (*"el Kenyon no ordena vecinos: 0.000 / 0.000 / 0.333"*) llevado a la
rejilla. Si es así, **ningún (NK, K) cumple** y la cláusula (i) del bloque 1 se activa: **la línea pasa al código** (nodo
indexado por (código, P) que nace al VER — §B.3 regla 1 de la síntesis — y B-5 para las celdas), **no al mundo**.

**Lo que esta pregunta NO es.** No pregunto si el organismo aprende mejor. Pregunta de **información**, no de mecanismo:
*¿el código del tronco puede siquiera nombrar 32 estímulos sin confundir dos?* Es el mismo teorema de M1 (*"identificabilidad
y alias son el mismo teorema"*), medido en el mundo que el bloque 1 quiere usar.

---

## 2. La construcción del código: por anclas de lectura, no por constantes copiadas

**Regla que me impongo (ERR-38, ERR-41, ERR-6 de §E):** ninguna constante del tronco se escribe a mano en el script.
`escala_codigo.py`:

1. Pone `organismo/` **primero** en `sys.path` (ERR-28) e **importa** `organismo_v14` (sha esperado `feefc88b1fd8d434`,
   verificado dentro del script; **sólo se lee, jamás se ejecuta `run()`**). De ahí toma `NK`, `NKMAX`, `K` — los valores
   por defecto del tronco, no copias.
2. **Verifica por ancla literal** que el texto de `organismo/organismo_v14.py` contiene, carácter a carácter:
   - `Wl=rng.uniform(.1,.4,(2,9)); KW=np.zeros((NKMAX,6)); activa=np.zeros(NKMAX,bool); KW[:NK]=rng.uniform(0,1,(NK,6)); activa[:NK]=True`
   - `        v=KW@P; v=np.where(activa,v,-1e9); return set(np.argsort(v)[-K:])`
   - `L=40; NK=30; NKMAX=90; K=3`
   Si alguna ancla no aparece exactamente una vez, **el script aborta** (`SystemExit`) y este preregistro queda sin datos.
3. **Verifica por ancla literal** la transformación a retina D contra `experimentos/capacidad_grande/construye_capD.py`
   (sha `0dbd2449f4bf0901`): la sustitución `(2,9)→(2,D+3)`, `(NKMAX,6)→(NKMAX,D)`, `(NK,6)→(NK,D)` se lee de ese archivo,
   no se inventa aquí. Con D = 6 el consumo del rng es **idéntico** al del tronco (es el control G0 de `capD`).
4. Reproduce entonces, y sólo entonces, el orden exacto de consumo del rng del tronco:
   `rng = np.random.default_rng(seed)` → `rng.uniform(.1,.4,(2,D+3))` (las patas, que se descartan) →
   `KW = rng.uniform(0,1,(NK,D))`; y `code(P) = frozenset(argsort(KW@P)[-K:])`.

**Dos desviaciones declaradas ahora (ninguna se decide después):**

- **Sin `cond()`.** El tronco reintenta el sorteo hasta que `code(A) ∩ code(B) = ∅`. Ese rechazo sólo restringe A y B, que
  no existen en el mundo de familias; `diagnostico_familias_sala2.py` tomó la misma decisión y por la misma razón. Se
  declara: **los números de este preregistro son SIN rechazo**, y por tanto son el caso **peor** por una cantidad no medida.
- **`activa` todas encendidas y celdas UNIFORMES.** Se sortean `NK` celdas `U(0,1)` y todas activas, como el arranque de una
  corrida. **Esto es el límite 4 de §F de la síntesis y lo repito aquí sin disimular:** en una corrida real las celdas 31–90
  nacen por fisión (`KW[j] = clip(0.95·KW[c] + paso·(P − mu[c]))·_rel`), están **correlacionadas con la madre** y son ciegas
  fuera de P. Un pool de celdas correlacionadas **aliasa más** que uno uniforme. Todo lo que sigue es una **cota optimista**:
  el alias real del tronco es ≥ el medido aquí. Si una celda de la rejilla no cumple con celdas uniformes, **tampoco cumple
  con las reales**; lo contrario no se sigue.

---

## 3. La rejilla que voy a barrer (fijada antes de calcular)

| eje | valores | por qué |
|---|---|---|
| `NK` (celdas del pool) | **30, 60, 90, 180, 360** | 30 = arranque del tronco; 90 = `NKMAX` (pool lleno); 60 = régimen a mitad de corrida. **180 y 360 están FUERA del tronco**: exigen subir `NKMAX`, que hoy es 90. Se barren para responder "¿con algún NK razonable?", y si la respuesta mínima cae ahí, **la recomendación lo dice explícitamente como cambio de instrumento con su coste**, no como perilla |
| `K` (celdas por código) | **2, 3, 4, 5** | K = 3 es el tronco. Nadie barrió K nunca; `DISENO_mundo_grande` §1.1 lo dejó fijo |
| `D` (retina) | **6, 12** | D = 12 es la retina del bloque 1 (9 forma + 3 variable). D = 6 es el mundo de hoy, y entra como **comparador degradado** (§3.1), no como competidor |

**5 × 4 × 2 = 40 celdas × 200 semillas por celda = 8 000 semillas por catálogo.** Semillas **1–200** (las mismas que usó
`DISENO_mundo_grande` §1.1, para que sus tres números sean anclas de verificación: §5 P2).

### 3.1 Catálogo de estímulos

Regla general, fijada ahora: `shape = D − V` píxeles de **forma**, `V` píxeles de **variable**; `F` tokens = combinaciones
distintas de **3** píxeles de forma, sorteadas con un rng **propio del mundo** (`default_rng(50000 + semilla)`, como
`diagnostico_familias_sala2.py`, para que el catálogo de una semilla sea **el mismo en todas las celdas** de la rejilla);
cada variante = su token **+ 1** píxel de variable a intensidad **1.0**.

| catálogo | D | V | shape | F | estímulos | procedencia |
|---|---|---|---|---|---|---|
| **C32 (principal)** | 12 | 3 | 9 | 8 | 8 tokens + 24 variantes = **32** | el que fija `DISENO_mundo_grande.md` §1.1 y el que el bloque 1 y T-A usan literalmente |
| **C16 (secundario)** | 12 | 3 | 9 | 4 | 4 tokens + 12 variantes = **16** | el "4 familias × 3 variantes" del encargo; entra porque el alias escala con el nº de pares y quiero saber cuánto del veredicto es tamaño de catálogo |

**El arm D = 6 no puede hospedar el catálogo, y lo digo antes de calcularlo:** con V = 3, `shape = 3` y sólo existe
C(3,3) = **1** token. **Regla declarada ahora:** si `D − V < 5`, el arm usa **V = 1** (`shape = D − 1`), de modo que D = 6 da
`shape = 5`, C(5,3) = 10 ≥ 8 tokens, y el catálogo es F tokens + F variantes (16 en C32-equivalente, 8 en C16-equivalente).
**Ese arm es un comparador degradado, no el mismo catálogo:** sirve para mostrar que el mundo de familias **no cabe en 6 px**
(que es el bloqueo M1/B1), y **no puede ganar la recomendación**. La recomendación se decide **sólo sobre D = 12 / C32**.

### 3.2 Coste

Aritmética pura sobre matrices pequeñas, sin simular: `KW@P` para ≤ 32 estímulos y ≤ 360 celdas, más C(32,2) = 496
intersecciones de conjuntos por semilla. **Un solo proceso, sin `Pool`.** Estimo < 3 min en total para los dos catálogos.
Si pasara de 15 min, se reporta y se reduce a C32 (y se declara).

---

## 4. Medidas y UMBRALES (escritos antes de calcular)

Por semilla `s` y celda `(D, NK, K, catálogo)`: `cod[n]` = código de cada estímulo (conjunto de K celdas).
**Familia** de un token `Tk` y de todas sus variantes `Tk v*` = `k`.
**Pares**: todos los pares no ordenados de estímulos distintos del catálogo (C32 → 496 pares; 48 intra-familia, 448
inter-familia).

| id | medida | definición exacta |
|---|---|---|
| **A1** | **alias exacto (semillas)** | % de las 200 semillas en las que **existe algún par** con `cod[a] == cod[b]` |
| **A2** | alias exacto (pares) | fracción media de pares idénticos (media sobre semillas) — se **reporta**, no es puerta |
| **B1** | **alias parcial K−1 inter-familia (pares)** | fracción media de pares **de familias distintas** con `\|cod[a] ∩ cod[b]\| ≥ K−1` (incluye los idénticos). Es el "alias 2/3" del encargo, generalizado a K |
| **B2** | alias parcial K−1 inter-familia (semillas) | % de semillas con al menos uno — se **reporta**, no es puerta |
| **T1** | tokeniza (intra-familia) | fracción media de variantes que comparten ≥ K−1 celdas con SU token (la medida de `DISENO_mundo_grande` §1.1) — se **reporta** |
| **S1** | **sim intra-familia** | media de `\|cod[a] ∩ cod[b]\| / K` sobre pares de la misma familia |
| **S2** | **sim inter-familia** | media de `\|cod[a] ∩ cod[b]\| / K` sobre pares de familias distintas |

**Las tres puertas. Una celda "CUMPLE" si y sólo si pasa las tres:**

> **U1 — alias exacto.** `A1 < 1.0 %` sobre 200 semillas. Con 200 semillas eso es **≤ 1 semilla de 200**. Es el umbral
> literal del bloque 1 y de `DIAG_metodo` bloqueo 1; no lo elegí yo y no lo muevo.
>
> **U2 — alias parcial acotado.** `B1 ≤ 1.0 %` de los pares inter-familia. **Por qué este número y no otro:** con C32 hay
> 448 pares inter-familia; 1 % ≈ 4.5 pares por semilla. El umbral se pone sobre **pares**, no sobre semillas, precisamente
> por ERR-37a: la versión por semillas está saturada a 100 % en todo el régimen conocido (199/200 con el alias *exacto*),
> así que una puerta por semillas no distinguiría nada. `B2` se reporta al lado para que se vea la saturación.
> **U2 mide sólo lo inter-familia**: el solapamiento K−1 **dentro** de una familia es lo que el diseño LLAMA "tokeniza"
> (T1) y es deseable; contarlo como alias sería contar el éxito como fracaso.
>
> **U3 — las familias siguen siendo legibles.** `S1 − S2 ≥ 0.20` (escala 0–1) **y** `S1 > S2` en **≥ 190/200** semillas.
> **Por qué 0.20 y por qué está FUERA del rango aritmético del propio efecto (ERR-37a):** el margen que B-4 midió en el
> código Kenyon de 6 px es `0.000 / 0.000 / 0.333` por píxeles compartidos, con el código HD en `0.025 / 0.075 / 0.225`;
> 0.20 es del orden del margen que un código que **sí** ordena vecinos consigue, y está a más de media celda (0.20·K = 0.6
> celdas con K = 3) de 0. No es "la mitad de lo que espero": es una cantidad tomada de otra medida, publicada antes.

**Regla de censura, para que no queden zonas muertas (§E punto 4):** una celda que pase U1 y U2 pero falle U3 se marca
**`AFILADO`** (el código no confunde, pero tampoco agrupa: el mundo pierde los grados de parecido que M2 pedía). Una celda
que pase U3 y falle U1 se marca **`BORROSO`**. Ninguna de las dos "cumple". No hay tercera categoría.

**Regla de mínimo (fijada ahora, para que la recomendación no sea una elección estética):** entre las celdas que CUMPLEN con
D = 12 y catálogo C32, la recomendada es la de **`NK` menor**; a igual `NK`, la de **`K` menor**. Si empatan, se reporta el
empate y se abstiene (§E punto 9: no desempatar por índice).

---

## 5. Predicciones numéricas (escritas antes de ejecutar; son lo que me refuta)

| # | predicción | qué la refuta |
|---|---|---|
| **P1** | `A1` es **monótona no creciente en NK** para cada K, y **no creciente en K** para cada NK | una inversión > 5 pp en cualquier par contiguo → mi construcción del código o del mundo está mal, y **paro** |
| **P2 (ancla de verificación, la que valida el instrumento)** | con **D = 12, K = 3, C32, semillas 1–200**, mis `A1` reproducen `DISENO_mundo_grande` §1.1 dentro de **±5 pp**: NK = 30 → **99.5 %** (199/200), NK = 60 → **95.0 %** (190/200), NK = 90 → **89.5 %** (179/200) | fuera de ±5 pp en cualquiera de los tres: **el instrumento está mal, se reporta como ERR y no se publica ninguna recomendación**. Esta es la única predicción cuyo fallo anula todo lo demás |
| **P3** | **ninguna** celda con `NK ≤ 90` pasa U1, para ningún K de la rejilla | que alguna lo haga (sería la mejor noticia posible: el bloque 1 corre con el pool del tronco) |
| **P4** | U3 **falla en K = 2** en toda la rejilla (con K = 2 la similitud sólo toma 0, 0.5, 1 y el ruido la aplana) | que K = 2 pase U3 |
| **P5 (la que de verdad juzgo, y predigo que se cumple: ~55 % de mi crédito)** | **U1 y U3 son incompatibles en esta rejilla: ninguna celda con D = 12 / C32 CUMPLE las tres.** El barrido termina en un frente `BORROSO` (NK bajo) → `AFILADO` (NK alto) sin celda intermedia. Consecuencia escrita ya: **la cláusula (i) del bloque 1 se activa y la línea pasa al código** | que exista una celda que cumple: entonces H queda en pie, el bloque 1 se corre con ese (NK, K) y P5 queda refutada — y lo diré con esas palabras |
| **P6** | `S1 − S2` **decrece con NK** (el código se afina y deja de agrupar): la caída entre NK = 30 y NK = 360 con K = 3 será **≥ 0.10** | que sea plana (< 0.03): entonces afinar el código **no** cuesta legibilidad de familias y P5 cae por su mecanismo |
| **P7** | el arm **D = 6** falla U1 en toda la rejilla, con cualquier NK y K, **aun con su catálogo degradado de 8–16 estímulos** | que D = 6 pase U1 en alguna celda — sería un argumento contra "el mundo es el bloqueo principal" y hay que decirlo |

---

## 6. Qué NO decide este documento

1. **No decide si el mundo de familias obliga.** Eso es la predicción clave del bloque 1 (`colateral ≥ 2×`, `w_var`) y exige
   correr a v14.1. Aquí sólo se decide si el bloque 1 **puede escribirse con alias < 1 %** como pide su propio texto.
2. **No decide nada sobre v15f, dE5, B-5 ni A-3.** No los toca.
3. **No mide capacidad, ni exposiciones, ni supervivencia.** `bateria_exposiciones.py` (0b) sigue sin existir (§F punto 6).
4. **No sustituye a `negativo_codigo.py`** en los runners; es su generalización a (D, NK, K) para un catálogo nuevo.
5. **No declara** "token", "lenguaje", "concepto" ni "entiende" (regla 8). Lo que aquí se declara es sólo:
   *dos estímulos reciben el mismo código, o no; y el código agrupa las variantes de una familia más que las de familias
   distintas, o no.*

## 7. Trampas que estoy evitando a propósito (§E de la síntesis)

- **ERR-37a** (umbral en la mediana del propio efecto): U3 se toma de B-4, una medida ajena y anterior; U2 se pone sobre
  pares porque la versión por semillas está saturada.
- **ERR-38 / ERR-41** (copiar constantes e instrumentos a mano): todo por anclas verificadas, con aborto duro.
- **§E punto 4** (zonas muertas): `AFILADO` / `BORROSO` cubren el espacio entre "pasa" y "refuta".
- **§E punto 9** (desempatar por índice): el catálogo se sortea con un rng propio del mundo y la regla de mínimo es
  explícita, con abstención declarada si hay empate.
- **§E punto 14** (preregistrar con cifras de un humo del propio conjunto de prueba): P2 usa números **ya publicados** por
  otro autor (`DISENO_mundo_grande` §1.1) como ancla; no corrí ningún humo previo de este script.
- **§F punto 4** (celdas uniformes): declarado en §2 como **cota optimista**, no escondido.
- **Honestidad del arm D = 6**: declarado degradado en §3.1 **antes** de verlo, y excluido de la recomendación.

---

## 8. RESULTADOS

**Catálogo C32 (D = 12: 8 tokens × 3 variantes = 32 estímulos; D = 6: comparador degradado V = 1 → 16 estímulos). Semillas 1–200.**

| D | NK | K | estim. | alias exacto % (A1) | alias exacto pares % (A2) | alias 2/3 inter % (B1) | B2 semillas % | tokeniza (T1) | sim intra (S1) | sim inter (S2) | S1−S2 | U1 | U2 | U3 | veredicto |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 6 | 30 | 2 | 16 | **99.5** | 6.567 | **49.78** | 100 | 0.761 | 0.544 | 0.275 | **+0.269** | · | · | ✔ | BORROSO |
| 6 | 30 | 3 | 16 | **90.0** | 2.683 | **24.21** | 100 | 0.621 | 0.585 | 0.328 | **+0.258** | · | · | ✔ | BORROSO |
| 6 | 30 | 4 | 16 | **72.5** | 1.308 | **13.16** | 99 | 0.508 | 0.621 | 0.375 | **+0.246** | · | · | ✔ | BORROSO |
| 6 | 30 | 5 | 16 | **58.0** | 0.700 | **7.69** | 98 | 0.398 | 0.652 | 0.414 | **+0.237** | · | · | ✔ | BORROSO |
| 6 | 60 | 2 | 16 | **95.5** | 4.525 | **38.09** | 100 | 0.710 | 0.483 | 0.208 | **+0.275** | · | · | ✔ | BORROSO |
| 6 | 60 | 3 | 16 | **73.0** | 1.458 | **16.15** | 100 | 0.537 | 0.522 | 0.253 | **+0.270** | · | · | ✔ | BORROSO |
| 6 | 60 | 4 | 16 | **44.0** | 0.642 | **6.78** | 98 | 0.403 | 0.562 | 0.287 | **+0.275** | · | · | ✔ | BORROSO |
| 6 | 60 | 5 | 16 | **23.5** | 0.271 | **3.19** | 80 | 0.272 | 0.587 | 0.317 | **+0.270** | · | · | ✔ | BORROSO |
| 6 | 90 | 2 | 16 | **91.5** | 3.054 | **32.17** | 100 | 0.684 | 0.436 | 0.172 | **+0.264** | · | · | ✔ | BORROSO |
| 6 | 90 | 3 | 16 | **59.5** | 1.054 | **11.18** | 100 | 0.474 | 0.488 | 0.211 | **+0.278** | · | · | ✔ | BORROSO |
| 6 | 90 | 4 | 16 | **34.0** | 0.404 | **4.37** | 92 | 0.314 | 0.521 | 0.241 | **+0.280** | · | · | ✔ | BORROSO |
| 6 | 90 | 5 | 16 | **16.0** | 0.154 | **1.73** | 65 | 0.205 | 0.542 | 0.265 | **+0.277** | · | · | ✔ | BORROSO |
| 6 | 180 | 2 | 16 | **82.0** | 1.946 | **25.15** | 100 | 0.636 | 0.381 | 0.132 | **+0.249** | · | · | ✔ | BORROSO |
| 6 | 180 | 3 | 16 | **41.5** | 0.596 | **6.59** | 97 | 0.371 | 0.424 | 0.156 | **+0.268** | · | · | ✔ | BORROSO |
| 6 | 180 | 4 | 16 | **20.0** | 0.221 | **2.04** | 68 | 0.217 | 0.456 | 0.180 | **+0.276** | · | · | ✔ | BORROSO |
| 6 | 180 | 5 | 16 | **7.0** | 0.058 | **0.77** | 42 | 0.113 | 0.478 | 0.201 | **+0.277** | · | ✔ | ✔ | BORROSO |
| 6 | 360 | 2 | 16 | **69.5** | 1.300 | **20.21** | 100 | 0.593 | 0.345 | 0.105 | **+0.240** | · | · | ✔ | BORROSO |
| 6 | 360 | 3 | 16 | **29.0** | 0.329 | **4.08** | 92 | 0.303 | 0.377 | 0.122 | **+0.255** | · | · | ✔ | BORROSO |
| 6 | 360 | 4 | 16 | **11.0** | 0.100 | **0.97** | 54 | 0.144 | 0.400 | 0.136 | **+0.264** | · | ✔ | ✔ | BORROSO |
| 6 | 360 | 5 | 16 | **5.0** | 0.050 | **0.23** | 19 | 0.062 | 0.417 | 0.151 | **+0.266** | · | ✔ | ✔ | BORROSO |
| 12 | 30 | 2 | 32 | **100.0** | 3.998 | **32.30** | 100 | 0.798 | 0.489 | 0.173 | **+0.315** | · | · | ✔ | BORROSO |
| 12 | 30 | 3 | 32 | **99.5** | 1.615 | **12.21** | 100 | 0.658 | 0.537 | 0.222 | **+0.315** | · | · | ✔ | BORROSO |
| 12 | 30 | 4 | 32 | **92.0** | 0.865 | **5.56** | 100 | 0.519 | 0.574 | 0.265 | **+0.309** | · | · | ✔ | BORROSO |
| 12 | 30 | 5 | 32 | **82.5** | 0.442 | **2.74** | 100 | 0.412 | 0.604 | 0.302 | **+0.302** | · | · | ✔ | BORROSO |
| 12 | 60 | 2 | 32 | **100.0** | 2.180 | **21.76** | 100 | 0.739 | 0.407 | 0.114 | **+0.293** | · | · | ✔ | BORROSO |
| 12 | 60 | 3 | 32 | **95.0** | 0.820 | **5.93** | 100 | 0.539 | 0.458 | 0.147 | **+0.311** | · | · | ✔ | BORROSO |
| 12 | 60 | 4 | 32 | **76.0** | 0.328 | **2.12** | 99 | 0.373 | 0.492 | 0.175 | **+0.317** | · | · | ✔ | BORROSO |
| 12 | 60 | 5 | 32 | **50.5** | 0.177 | **0.87** | 88 | 0.264 | 0.522 | 0.201 | **+0.321** | · | ✔ | ✔ | BORROSO |
| 12 | 90 | 2 | 32 | **100.0** | 1.788 | **17.43** | 100 | 0.714 | 0.374 | 0.091 | **+0.283** | · | · | ✔ | BORROSO |
| 12 | 90 | 3 | 32 | **89.5** | 0.599 | **4.27** | 100 | 0.481 | 0.421 | 0.117 | **+0.305** | · | · | ✔ | BORROSO |
| 12 | 90 | 4 | 32 | **62.5** | 0.241 | **1.29** | 94 | 0.302 | 0.452 | 0.138 | **+0.314** | · | · | ✔ | BORROSO |
| 12 | 90 | 5 | 32 | **35.0** | 0.100 | **0.45** | 74 | 0.197 | 0.479 | 0.158 | **+0.321** | · | ✔ | ✔ | BORROSO |
| 12 | 180 | 2 | 32 | **99.5** | 1.149 | **11.92** | 100 | 0.644 | 0.321 | 0.062 | **+0.260** | · | · | ✔ | BORROSO |
| 12 | 180 | 3 | 32 | **73.0** | 0.356 | **2.18** | 98 | 0.397 | 0.366 | 0.078 | **+0.287** | · | · | ✔ | BORROSO |
| 12 | 180 | 4 | 32 | **41.5** | 0.119 | **0.57** | 76 | 0.224 | 0.396 | 0.092 | **+0.303** | · | ✔ | ✔ | BORROSO |
| 12 | 180 | 5 | 32 | **19.5** | 0.045 | **0.16** | 42 | 0.120 | 0.417 | 0.106 | **+0.311** | · | ✔ | ✔ | BORROSO |
| 12 | 360 | 2 | 32 | **96.0** | 0.734 | **8.69** | 100 | 0.591 | 0.278 | 0.045 | **+0.233** | · | · | ✔ | BORROSO |
| 12 | 360 | 3 | 32 | **57.0** | 0.176 | **1.24** | 96 | 0.296 | 0.312 | 0.056 | **+0.256** | · | · | ✔ | BORROSO |
| 12 | 360 | 4 | 32 | **18.5** | 0.044 | **0.28** | 55 | 0.143 | 0.338 | 0.065 | **+0.272** | · | ✔ | ✔ | BORROSO |
| 12 | 360 | 5 | 32 | **8.5** | 0.017 | **0.07** | 26 | 0.068 | 0.357 | 0.074 | **+0.283** | · | ✔ | ✔ | BORROSO |

**Catálogo C16 (D = 12: 4 tokens × 3 variantes = 16 estímulos; D = 6: comparador degradado V = 1 → 8 estímulos). Semillas 1–200.**

| D | NK | K | estim. | alias exacto % (A1) | alias exacto pares % (A2) | alias 2/3 inter % (B1) | B2 semillas % | tokeniza (T1) | sim intra (S1) | sim inter (S2) | S1−S2 | U1 | U2 | U3 | veredicto |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 6 | 30 | 2 | 8 | **85.0** | 8.518 | **51.19** | 100 | 0.814 | 0.553 | 0.284 | **+0.269** | · | · | · | NO |
| 6 | 30 | 3 | 8 | **55.5** | 3.214 | **24.69** | 97 | 0.623 | 0.576 | 0.329 | **+0.247** | · | · | ✔ | BORROSO |
| 6 | 30 | 4 | 8 | **39.5** | 1.839 | **13.19** | 84 | 0.524 | 0.622 | 0.380 | **+0.242** | · | · | ✔ | BORROSO |
| 6 | 30 | 5 | 8 | **27.0** | 1.054 | **8.00** | 70 | 0.410 | 0.652 | 0.419 | **+0.232** | · | · | ✔ | BORROSO |
| 6 | 60 | 2 | 8 | **68.0** | 5.536 | **39.15** | 100 | 0.721 | 0.472 | 0.213 | **+0.259** | · | · | · | NO |
| 6 | 60 | 3 | 8 | **42.0** | 2.161 | **17.38** | 88 | 0.555 | 0.525 | 0.263 | **+0.262** | · | · | ✔ | BORROSO |
| 6 | 60 | 4 | 8 | **18.5** | 0.839 | **7.15** | 66 | 0.398 | 0.562 | 0.296 | **+0.266** | · | · | ✔ | BORROSO |
| 6 | 60 | 5 | 8 | **11.0** | 0.554 | **3.02** | 35 | 0.274 | 0.587 | 0.322 | **+0.266** | · | · | ✔ | BORROSO |
| 6 | 90 | 2 | 8 | **63.0** | 4.196 | **33.67** | 98 | 0.679 | 0.428 | 0.180 | **+0.248** | · | · | · | NO |
| 6 | 90 | 3 | 8 | **34.5** | 1.661 | **11.62** | 78 | 0.482 | 0.492 | 0.217 | **+0.275** | · | · | ✔ | BORROSO |
| 6 | 90 | 4 | 8 | **18.0** | 0.750 | **4.60** | 54 | 0.307 | 0.525 | 0.247 | **+0.278** | · | · | ✔ | BORROSO |
| 6 | 90 | 5 | 8 | **5.0** | 0.179 | **1.69** | 28 | 0.199 | 0.539 | 0.268 | **+0.270** | · | · | ✔ | BORROSO |
| 6 | 180 | 2 | 8 | **51.5** | 2.696 | **25.38** | 96 | 0.616 | 0.372 | 0.133 | **+0.239** | · | · | · | NO |
| 6 | 180 | 3 | 8 | **20.0** | 0.875 | **6.56** | 66 | 0.360 | 0.412 | 0.157 | **+0.255** | · | · | · | NO |
| 6 | 180 | 4 | 8 | **7.0** | 0.268 | **1.94** | 29 | 0.196 | 0.443 | 0.181 | **+0.262** | · | · | ✔ | BORROSO |
| 6 | 180 | 5 | 8 | **3.5** | 0.125 | **0.65** | 13 | 0.098 | 0.468 | 0.201 | **+0.266** | · | ✔ | ✔ | BORROSO |
| 6 | 360 | 2 | 8 | **35.5** | 1.750 | **20.56** | 95 | 0.595 | 0.341 | 0.106 | **+0.235** | · | · | · | NO |
| 6 | 360 | 3 | 8 | **13.0** | 0.518 | **3.17** | 43 | 0.304 | 0.374 | 0.121 | **+0.253** | · | · | ✔ | BORROSO |
| 6 | 360 | 4 | 8 | **6.0** | 0.214 | **0.71** | 14 | 0.145 | 0.400 | 0.134 | **+0.266** | · | ✔ | ✔ | BORROSO |
| 6 | 360 | 5 | 8 | **3.0** | 0.107 | **0.19** | 4 | 0.074 | 0.417 | 0.153 | **+0.264** | · | ✔ | ✔ | BORROSO |
| 12 | 30 | 2 | 16 | **99.5** | 5.896 | **32.09** | 100 | 0.823 | 0.488 | 0.173 | **+0.314** | · | · | ✔ | BORROSO |
| 12 | 30 | 3 | 16 | **87.5** | 2.388 | **12.17** | 98 | 0.666 | 0.530 | 0.220 | **+0.309** | · | · | ✔ | BORROSO |
| 12 | 30 | 4 | 16 | **73.0** | 1.254 | **5.43** | 88 | 0.510 | 0.569 | 0.261 | **+0.308** | · | · | ✔ | BORROSO |
| 12 | 30 | 5 | 16 | **59.5** | 0.779 | **2.69** | 72 | 0.390 | 0.597 | 0.297 | **+0.300** | · | · | ✔ | BORROSO |
| 12 | 60 | 2 | 16 | **96.0** | 3.292 | **22.14** | 100 | 0.760 | 0.407 | 0.116 | **+0.291** | · | · | ✔ | BORROSO |
| 12 | 60 | 3 | 16 | **69.5** | 1.433 | **5.91** | 88 | 0.549 | 0.460 | 0.147 | **+0.313** | · | · | ✔ | BORROSO |
| 12 | 60 | 4 | 16 | **50.5** | 0.662 | **2.33** | 61 | 0.393 | 0.495 | 0.176 | **+0.318** | · | · | ✔ | BORROSO |
| 12 | 60 | 5 | 16 | **27.0** | 0.329 | **0.95** | 40 | 0.264 | 0.520 | 0.200 | **+0.320** | · | ✔ | ✔ | BORROSO |
| 12 | 90 | 2 | 16 | **92.5** | 2.788 | **17.72** | 100 | 0.726 | 0.372 | 0.093 | **+0.279** | · | · | ✔ | BORROSO |
| 12 | 90 | 3 | 16 | **66.5** | 1.137 | **4.65** | 89 | 0.485 | 0.421 | 0.120 | **+0.301** | · | · | ✔ | BORROSO |
| 12 | 90 | 4 | 16 | **42.0** | 0.508 | **1.34** | 48 | 0.315 | 0.455 | 0.141 | **+0.314** | · | · | ✔ | BORROSO |
| 12 | 90 | 5 | 16 | **23.5** | 0.237 | **0.64** | 32 | 0.209 | 0.482 | 0.161 | **+0.321** | · | ✔ | ✔ | BORROSO |
| 12 | 180 | 2 | 16 | **85.5** | 1.796 | **11.67** | 97 | 0.653 | 0.316 | 0.060 | **+0.257** | · | · | ✔ | BORROSO |
| 12 | 180 | 3 | 16 | **48.0** | 0.637 | **1.89** | 62 | 0.395 | 0.364 | 0.078 | **+0.286** | · | · | ✔ | BORROSO |
| 12 | 180 | 4 | 16 | **24.5** | 0.225 | **0.51** | 29 | 0.215 | 0.393 | 0.093 | **+0.300** | · | ✔ | ✔ | BORROSO |
| 12 | 180 | 5 | 16 | **9.5** | 0.092 | **0.18** | 12 | 0.121 | 0.415 | 0.106 | **+0.309** | · | ✔ | ✔ | BORROSO |
| 12 | 360 | 2 | 16 | **77.5** | 1.363 | **8.72** | 96 | 0.598 | 0.280 | 0.045 | **+0.235** | · | · | ✔ | BORROSO |
| 12 | 360 | 3 | 16 | **32.5** | 0.342 | **1.11** | 48 | 0.300 | 0.310 | 0.056 | **+0.254** | · | · | ✔ | BORROSO |
| 12 | 360 | 4 | 16 | **7.5** | 0.067 | **0.20** | 15 | 0.147 | 0.336 | 0.063 | **+0.272** | · | ✔ | ✔ | BORROSO |
| 12 | 360 | 5 | 16 | **5.5** | 0.046 | **0.06** | 6 | 0.068 | 0.355 | 0.073 | **+0.282** | · | ✔ | ✔ | BORROSO |

**POST-HOC, FUERA de la rejilla preregistrada de §3 y FUERA del veredicto (D = 12, C32, semillas 1–200). Existe sólo para cuantificar *cuánto* NK haría falta; ninguna de estas filas puede recomendarse.**

| D | NK | K | estim. | alias exacto % (A1) | alias exacto pares % (A2) | alias 2/3 inter % (B1) | B2 semillas % | tokeniza (T1) | sim intra (S1) | sim inter (S2) | S1−S2 | U1 | U2 | U3 | veredicto |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 12 | 720 | 4 | 32 | **16.0** | 0.033 | **0.15** | 42 | 0.097 | 0.286 | 0.044 | **+0.242** | · | ✔ | ✔ | BORROSO |
| 12 | 720 | 5 | 32 | **4.0** | 0.008 | **0.04** | 14 | 0.039 | 0.303 | 0.049 | **+0.254** | · | ✔ | ✔ | BORROSO |
| 12 | 1440 | 4 | 32 | **4.5** | 0.009 | **0.06** | 24 | 0.062 | 0.246 | 0.031 | **+0.215** | · | ✔ | ✔ | BORROSO |
| 12 | 1440 | 5 | 32 | **2.5** | 0.005 | **0.01** | 4 | 0.019 | 0.260 | 0.035 | **+0.225** | · | ✔ | ✔ | BORROSO |
| 12 | 2880 | 4 | 32 | **6.5** | 0.013 | **0.04** | 14 | 0.044 | 0.209 | 0.022 | **+0.187** | · | ✔ | · | NO |
| 12 | 2880 | 5 | 32 | **2.5** | 0.005 | **0.01** | 2 | 0.013 | 0.222 | 0.025 | **+0.197** | · | ✔ | · | NO |
| 12 | 5760 | 4 | 32 | **1.0** | 0.002 | **0.02** | 8 | 0.029 | 0.181 | 0.016 | **+0.165** | · | ✔ | · | NO |
| 12 | 5760 | 5 | 32 | **0.5** | 0.001 | **0.00** | 2 | 0.006 | 0.191 | 0.018 | **+0.173** | ✔ | ✔ | · | AFILADO |

**P2 (ancla de instrumento contra `DISENO_mundo_grande` §1.1, ±5 pp): PASA.** Detalle campo a campo en `escala_codigo_salida.json` → `P2_verificacion_instrumento`.

*Generado por `escala_codigo.py` en 10.7 s, un solo proceso, sin `Pool`. Salida cruda: `escala_codigo_salida.json`.*

## 9. RECOMENDACIÓN Y HONESTIDAD

### 9.1 La recomendación, en una línea

> **NINGUNO CUMPLE → la línea pasa al código.** Ninguna de las 20 celdas (D = 12, C32) de la rejilla preregistrada pasa U1:
> el mejor alias exacto del barrido es **8.5 %** (NK = 360, K = 5) contra el **< 1 %** que el bloque 1 exige, y NK = 360 ya
> está **4 × por encima de `NKMAX` = 90**; **la cláusula (i) del BLOQUE 1 queda activada.**

**Por qué, sin adornos.** U3 pasó en **20/20** celdas y U2 en **6/20**; **U1 pasó en 0/20**. El único eje que no se agota es
`NK`, y se agota fuera del organismo: el post-hoc (§8, fuera del veredicto) tuvo que llegar a **NK = 5 760** — **64 × `NKMAX`
y 192 × el `NK` del tronco** — para que A1 bajara a 0.5 %, **y ahí U3 ya había caído** (S1 − S2 = 0.173 < 0.20): esa celda es
`AFILADO`, un código que no confunde porque ya no agrupa. **No hay ventana**: no existe un (NK, K) que nombre 32 estímulos sin
alias *y* siga viendo las familias. Y todo esto es la **cota optimista** de §2 (celdas uniformes, sin `cond()`): con las
celdas reales del tronco, nacidas por fisión y correlacionadas con la madre, el alias sólo puede ser **mayor**.

**Qué hacer con esto, operativamente** (es una recomendación de método, no una decisión: la decisión es del director):

1. **El BLOQUE 1 no se corre con su redacción actual.** Su línea *"`NK`/`K` escalados a alias < 1 %"* no es satisfacible, y
   lo mismo su cita en **T-A** del criterio v2 propuesto (§D): la frase *"`NK`/`K` escalados de modo que el alias estructural
   quede < 1 %"* debe reescribirse o el bloque 1 arranca con una condición imposible. **Esto pide un ERR numerado**, y el
   número lo pone el coordinador, no yo.
2. **La reparación que queda es la del código, y ya está medida y esperando decisión:** **B-5** (división cuando una celda con
   valor recibe nada bajo otra retina: 18/18 ALIAS reparadas, tronco idéntico) y el **nodo indexado por (código, P) que nace
   al VER** (§B.3 regla 1 de la síntesis, BLOQUE 3). El alias es un problema de **identidad del nodo**, no de tamaño del pool:
   este barrido es la demostración aritmética de esa frase.
3. **El mundo de familias no se tira.** Lo que este cálculo mata es *"alias < 1 % por escalado de NK/K"*, **no** el mundo: la
   estructura de familias **sí** está en el código (S1 − S2 = **+0.31** en el tronco, contra el margen 0.20 de B-4, en 200/200
   semillas). El bloque 1 puede correrse **declarando el alias que tiene** y midiéndolo por semilla, en vez de prometer que
   no lo hay. Ése es un cambio de redacción de una frase, y es lo que recomiendo.

### 9.2 Las siete predicciones, una por una (lo que predije contra lo que salió)

| # | predicción | resultado | lectura honesta |
|---|---|---|---|
| **P1** | A1 monótona no creciente en NK y en K | **SE CUMPLE** en las 40 celdas preregistradas. Una inversión de **2.0 pp** (NK 1440 → 2880 con K = 4: 4.5 % → 6.5 %) en el bloque **post-hoc**, dentro del ±5 pp declarado y del ruido de 200 semillas (EE ≈ 1.5 pp a esa tasa) | bien, y la inversión se reporta en vez de esconderse |
| **P2** | reproduzco `DISENO_mundo_grande` §1.1 a ±5 pp en 15 campos | **PASA los 15** (p. ej. NK = 90, K = 3: A1 **89.5 %** contra 179/200 = 89.5 % esperado; tokeniza 0.481 contra 0.500; NK = 30: A1 99.5 % contra 99.5 %, tokeniza 0.658 contra 0.667) | el instrumento está verificado contra un número publicado por otro autor. Es lo único que autoriza a publicar el resto |
| **P3** | ninguna celda con NK ≤ 90 pasa U1 | **SE CUMPLE**, y de sobra: el mejor NK ≤ 90 es 35.0 % (NK = 90, K = 5) | acerté, pero por un margen que hace la predicción barata |
| **P4** | U3 **falla** en K = 2 en toda la rejilla | **REFUTADA.** U3 pasa en K = 2 en las 10 celdas (D = 12, NK = 30, K = 2: S1 − S2 = **+0.315**) | me equivoqué: la cuantización de K = 2 no aplana el margen, lo **agranda**. Lo digo entero |
| **P5** | ninguna celda CUMPLE, **por tensión U1 ↔ U3** | **la conclusión se cumple; el mecanismo que le puse, NO.** En la rejilla U3 nunca falló y U1 nunca pasó: no hubo frente `BORROSO → AFILADO`, hubo **`BORROSO` en 20/20**. La tensión que describí **existe**, pero sólo asoma en el post-hoc, a NK = 2 880–5 760 | **acertar el veredicto con el mecanismo equivocado no es acertar.** La rejilla no era demasiado estrecha en K: era demasiado corta en NK, y eso no lo vi |
| **P6** | S1 − S2 cae **≥ 0.10** entre NK = 30 y NK = 360 con K = 3 | **REFUTADA.** Cae **0.059** (0.315 → 0.256) | predije el doble de la caída real. La dirección era correcta, la magnitud no; y como P6 era el mecanismo de P5, su caída arrastra a P5 |
| **P7** | D = 6 falla U1 en toda la rejilla, aun degradado | **SE CUMPLE**: mejor caso 5.0 % (NK = 360, K = 5) con sólo **16** estímulos | el mundo de 6 px no nombra ni 16 cosas. Es M1 otra vez, con número nuevo |

**Marcador: 4 de 7 en pie (P1, P2, P3, P7), 2 refutadas (P4, P6), 1 acertada por la razón equivocada (P5).**

### 9.3 Resultados secundarios que no pedí pero que quedan medidos

- **El alias no es del tamaño del catálogo.** C16 (16 estímulos) baja el mejor A1 sólo de 8.5 % a **5.5 %**, y tampoco pasa
  U1 en ninguna celda. Recortar el mundo **no** es la salida.
- **U2 sí es alcanzable dentro del tronco-ampliado**: 6 celdas pasan el alias parcial inter-familia (la mejor, NK = 360 /
  K = 5: **0.075 %**). Lo que no se puede evitar es el alias **exacto**. Es decir: el código puede dejar de confundir
  familias *parcialmente* mucho antes de dejar de confundir estímulos *del todo*.
- **El tronco tal cual (NK = 90, K = 3, D = 12, 32 estímulos)**: A1 = **89.5 %**, B1 = **4.27 %**, tokeniza **0.481**,
  S1 = 0.421, S2 = 0.117. Este renglón es la línea base estructural que el bloque 1 tendría que declarar en cada serie.

### 9.4 Lo que NO pude hacer (límites de este documento)

1. **No corrí el organismo**: cero pasos simulados. Nada de aquí dice cómo se **comporta** v14.1 en ese mundo.
2. **Celdas uniformes, no las que el tronco crea por fisión** (§2 y §F-4 de la síntesis). Es cota optimista; el número real
   es peor y **no lo medí**.
3. **Sin `cond()`**: el rechazo del tronco no se reprodujo (no tiene A ni B que restringir). Segunda razón por la que esto
   es una cota.
4. **`NKMAX` no se tocó y no sé qué cuesta subirlo.** NK = 180/360 (y el post-hoc hasta 5 760) están **fuera del tronco**:
   no medí el coste en CPU, memoria ni dinámica de la fisión de un pool así. La recomendación no depende de ello — ninguno
   pasa —, pero si alguien quisiera perseguir el `AFILADO` de NK = 5 760, ese coste está **sin calcular**.
5. **No barrí la intensidad del píxel de variable** (el 0.5 de §1.1). El diseño original lo declaró humo (*"tunear el mundo a
   la debilidad del código sería humo"*) y lo respeto; pero eso significa que **una salida posible queda sin explorar**.
6. **No barrí K > 5 ni pesos de token ≠ 3**, ni retinas D > 12. La rejilla es la del encargo y la cerré antes de mirar.
7. **Una sola réplica**: 200 semillas, un solo rango (1–200). No hay réplica en semillas nuevas. Con A1 ≈ 8.5 % el EE es
   ≈ 2 pp, así que el veredicto (8.5 % contra 1 %) aguanta de sobra, pero **la réplica no está hecha** y decirlo es parte
   del número.
