# PREREGISTRO — BLOQUE 1: EL MUNDO QUE OBLIGA A REPRESENTAR, medido con v14.1 SIN CAMBIOS

**Misión (primero, siempre):** llegar a la AGI por este camino — un organismo mínimo con reglas locales (sin backprop en el
runtime) que aprende, desaprende, generaliza, sobrevive y se reproduce, con evidencia preregistrada. **Primero llegar a la
frontera; segundo, que viva.**

**Autor:** diseñador del bloque 1, sala 2. **Fecha de firma:** 18 sep 2026.
**Estado al firmar:** §1–§10 se escribieron **ENTERAS antes de construir el instrumento y antes de ejecutar un solo paso del
organismo en el mundo nuevo**. Sólo §11 (identidad) y §12 (humo) se escriben después, y **nada de §1–§10 se toca al
escribirlas** (regla 3: no recalibrar tras ver datos; regla 11: mover un umbral lleva ERR y fecha). §13 (resultados de la
serie 401–420) lo escribe el coordinador cuando corra el `Pool`.

**Qué es y qué NO es.** Es el **BLOQUE 1** de `registro/investigacion/SALA2_frontera_20260918.md` §C.2: *"el mundo que obliga,
con v14.1 SIN CAMBIOS"*. **No hay órgano. No hay candidato a tronco. No se toca el organismo.** Lo único que se construye es
un **mundo** (instrumento) y lo único que se mide es **v14.1 tal cual** dentro de él. Lo que produce es **la línea base de
T-A, T-F y T-G del `CRITERIO_TRONCO_v2.md` para ese mundo** — hoy inexistente, y sin la cual *"cualquier umbral que
escribiéramos sería inventado"* (§F.9 de la síntesis).

**Reglas cumplidas.** No edité ningún archivo existente ni congelado (`organismo/organismo_v14.py` sólo se **lee**, y su sha
se verifica con aborto duro). Archivos nuevos sólo en `experimentos/nivel12_mundo_familias/`, compartida con el bloque 0:
**no toqué `escala_codigo.py` ni `PREREGISTRO_bloque0_codigo.md`**. Instrumento **por anclas**. **Nunca
`multiprocessing.Pool`** en mi humo (un proceso, 2 semillas, T ≤ 200 000). Sin commits. `organismo/` primero en `sys.path`
(ERR-28). ERR libres desde **ERR-46**.

**Fuentes.** `SALA2_frontera_20260918.md` entera (§C.1, §C.2 bloque 1, §D T-A/T-G, §E trampas 1–18, §F límites);
`sala2/DISENO_mundo_grande.md` (el mundo y `tasa_tokeniza`/`w_var`/`colateral`/`exp_total`); `sala2/DISENO_grafo_tokens.md`
(brazos INV/FRONTERA/AZAR, medidas C1–C5, la elección **estructural y previa** de lo que cambia); `sala2/DIAG_mundo.md`
bloqueo 3 (**renovación simétrica**); `registro/CRITERIO_TRONCO_v2.md`; `CLAUDE.md` (decisión del director 09:55);
`registro/EQUIPO.md` 1–14; `experimentos/nivel11_mundo_vivo/{organismo_vivo.py, construye_vivo.py, identidad_vivo.py,
corre_vivo.py}` como modelo de construcción por anclas; `experimentos/capacidad_grande/construye_capD.py` (retina D);
`experimentos/nivel12_mundo_familias/PREREGISTRO_bloque0_codigo.md` §8 (bloque 0, ya publicado: **§2.6 de aquí**).

---

## 1. La hipótesis del director, y qué parte de ella prueba este bloque

> *"si sal es sal la guardo; sal rosa la marca como sal y la plantea como variable de lo mismo; eso es lenguaje; aprender y
> desaprender."*

Este bloque **no** prueba esa hipótesis: prueba su **precondición**. La síntesis lo dice con la línea exacta
(§B.4, segunda advertencia): *"en 6 px el grafo casi no compra […] la hipótesis del director necesita **un mundo con
familias**, no un órgano sobre el mundo viejo"*. Y el director (09:55 §2) pidió *"un mundo donde 16 patrones no basten y donde
la tokenización, la variable y el desaprender sean necesarios para sobrevivir"*.

**H (la que se juzga aquí).** *En el mundo de familias con excepciones, v14.1 **paga** cada excepción: la aprende por la vía
lenta, que reparte el error entre los píxeles compartidos, y con eso **contamina a los hermanos** de la excepción y **ensucia
los píxeles de variable**. En el mundo `lineal` (mismas familias, mismas ventanas de medida, **sin** excepciones) no paga
nada de eso.*

**H¬ (la alternativa que tomo en serio).** *La fuga por píxel de la vía lenta ya implementa "variable de lo mismo" lo bastante
bien como para que 4 excepciones sobre 32 estímulos no se noten; y la asimetría de muestreo, corregida por la renovación
simétrica, se lleva por delante el resto del efecto.* **Si H¬ gana, el mundo NO obliga**, y lo que se hace es **endurecer el
mundo** (`n_exc` 4 → 8, una por token) **antes de tocar el organismo**, con ERR-46 y semillas nuevas — nunca ajustar el
organismo para que el mundo parezca duro (§E.16, decisión 09:55 §3).

**Lo que este bloque NO decide** (§E.18, regla 8): no declara "token", "lenguaje", "concepto", "entiende" ni "representa".
Lo declarable, si pasa, es literalmente: *"en un mundo con familias y excepciones, v14.1 aprende la excepción a costa de sus
hermanos y de los píxeles que distinguen la variante; en el mismo mundo sin excepciones, no"*. Nada más.

---

## 2. EL MUNDO (instrumento; ningún órgano)

### 2.1 Retina y catálogo

`D = 12` píxeles = **9 de forma** + **3 de variable** (`n_var = 3`). `F = 8` **tokens**, cada uno un subconjunto distinto de
**3** de los 9 píxeles de forma, sorteados con un **rng PROPIO del mundo** (**nunca** el del organismo). Cada token tiene
`V = 3` **variantes** = token + **1** píxel de variable a intensidad 1.0. Total **8 + 24 = 32 estímulos**, todos de peso 3
(tokens) o 4 (variantes).

**El catálogo es LITERALMENTE el del bloque 0, no una reimplementación.** `construye_familias.py` **importa**
`escala_codigo.catalogo(D, F, V, seed)` (sha `d8b8566bca77a0ae`) y verifica por ancla literal sus dos constantes
(`SEMILLA_MUNDO = 50000`, `PESO_TOKEN = 3`) y el orden de sorteo (`default_rng(50000 + seed)` → `shuffle(combos)` → los `F`
primeros). Con eso: (a) el catálogo de la semilla `s` en el mundo es **el mismo** sobre el que el bloque 0 calculó el alias;
(b) `escala_codigo.kw_del_tronco(s, NK, D)` reproduce **bit a bit** el `KW` inicial que el instrumento construye (§2.6 lo usa
como comprobación, no como supuesto); (c) no hay ninguna constante del mundo copiada a mano (ERR-38, §E.6).

*(D, n_var, F, V, n_neu, NK, NKMAX, K son parámetros del instrumento; §2.6 fija los valores con los que corre este bloque.)*

### 2.2 Valencias, familias y excepciones

- **La variante ES el token:** `val[Tk vj] = val[Tk]`, con `val[Tk] = comida` si `k` es par y `veneno` si es impar (**4 y 4**).
- **Excepciones.** Se sortea **una variante candidata por token** (`exc_win`, 8 en total, con el **mismo rng propio**, en
  orden de token: decisión **estructural** declarada aquí y no un desempate por índice, §E.9). Las **primeras `n_exc`** de esa
  lista son las excepciones **activas**: su valencia se **invierte**. Con `n_exc = 4` las activas son las de T0, T1, T2, T3 →
  **2 familias de comida** (la "sal rosa que envenena" del director) y **2 familias de veneno** (la variante que resulta
  inocua). El reparto 2/2 es deliberado: sin él, `colateral` medido como *"mordidas de veneno en los hermanos"* no tendría
  soporte en la mitad de los casos (§4.2).
- **`exc_win` se sortea SIEMPRE, también con `n_exc = 0`.** Ésta es la decisión de diseño que hace comparable el control:
  el mundo `lineal` tiene **las mismas 8 ventanas de medida, abiertas por la primera mordida de los mismos 8 estímulos**, y
  sólo se diferencia en que a esos estímulos **no** se les invirtió la valencia. Sin esto, `colateral` en `lineal` sería 0 por
  construcción y la razón `excepciones / lineal` sería infinita y vacía (trampa de control de paja, **ERR-39**).

### 2.3 Deriva y cambio de familia (sin sorteo)

- **Presentes en `t`:** los 8 tokens **+ una variante por token**, la `(t // deriva) mod V`, con `deriva = 5 000` → **16
  estímulos presentes** y 20 eventos de deriva en T = 100 000. En cada evento, los objetos del anillo que eran de la variante
  saliente **pasan a la entrante del mismo token, sin sorteo** (`len(tipos)` no cambia nunca: 16).
- **Cambio de familia en `T/2`:** la familia **T0** se invierte (T0 y sus variantes **no excepcionales** cambian de valencia);
  **la excepción de T0 conserva su valencia absoluta** (*"la sustancia cambió; lo que ya era distinto sigue siendo lo que
  era"*). Decidido **ahora** y no después de ver datos: la otra semántica ("todo se niega") es **otro mundo**, y se deja
  escrito como brazo no construido (`DISENO_mundo_grande` §2.1 tomó la misma decisión y por la misma razón, §E.7).

### 2.4 Recursos que se agotan y **renovación simétrica** (el único cambio de física del mundo)

`DIAG_mundo` bloqueo 3, trampa 3: *lo mordido desaparece y lo rechazado se queda* — veneno **6.3×** más encuentros que comida
en la mini y **23×** en el ancla V14 (B 7 897.5 contra A 344.5). Con eso, **toda medida agregada sobre patrones es muestreo**.

**Corrección, con la definición que no tiene parámetro libre:** perilla `renov`. Con `renov = 1.0`, **un objeto que la boca
rechaza desaparece exactamente igual que uno que muerde** (`del objs[pos]; spawn()`), de modo que la tasa de renovación de lo
rechazado es **idéntica** (no "comparable") a la de lo comido. `renov = 0.0` es v14.1 (lo rechazado se queda) y es el valor
con el que la identidad se comprueba.

**Es mi injerto y es el riesgo más grande del bloque** (§F.10: *"no tiene un solo número detrás"*). Por eso:
(a) `renov = 1.0` es el **único** valor sin parámetro libre y es el que se preregistra; (b) `frac_veneno` del anillo por
cuartos y la tabla de exposiciones por patrón se reportan **siempre** y son la puerta de validez **P1**; (c) cláusula (iii)
del bloque 1: *si con renovación simétrica el mundo mata tanto que nadie aprende nada, se reporta y se baja la tasa **UNA**
vez, con ERR* (ERR-46 si se usa) y semillas nuevas.

### 2.5 El cuerpo: **peldaño 1**, y por qué no peldaño 2

El cuerpo es el de **v14.1 sin cambios**: **una** necesidad (energía), dos valencias, `costo = 0.002`, `hambre_boca = 2.0`,
`memoria_rechazo = 20`. **No** se compone con el peldaño 2 del mundo vivo (dos necesidades) en este bloque, y la razón se
escribe antes y no después:

1. **Un cambio por experimento** (regla 2). El cambio de este bloque **es el mundo** (familias + excepciones + renovación
   simétrica). Meter además las dos necesidades sería dos cambios, y la línea base dejaría de ser atribuible.
2. **Coste de identidad.** El peldaño 2 vive en `organismo_vivo.py`, que es **otra** copia por anclas del mismo tronco.
   Componerlas exige un tercer constructor y duplicar el arnés; es exactamente la acumulación que `DIAG_metodo` T1 midió
   (*"≈ 24 archivos copiados en 1 h 30"*).
3. **Ninguna predicción de §4 necesita dos necesidades.** `colateral`, `w_var`, `exp_asoc` y `muertes` se miden igual con una.

**Gancho declarado para el peldaño 2** (para que el siguiente bloque no tenga que inventarlo): `construye_familias.py` deja
`PAT`, `val`, `tipos` y `renov` como anclas independientes de las de `construye_vivo.py`; la composición es
`construye_vivo.py` aplicado **después** de `construye_familias.py` sobre el mismo texto. Se declara aquí, **no** se construye.

### 2.6 El tamaño del código: **lo fijó el bloque 0**, y el alias se DECLARA en vez de eliminarse

**Enmienda del coordinador (18 sep, tras el resultado del bloque 0; ERR-46 ya asignado a ese resultado).** El bloque 0
publicó su §8: con `D = 12` y el catálogo C32 **ningún `(NK, K)` deja el alias exacto por debajo del 1 %** — el mejor de su
rejilla es 8.5 % (`NK = 360`, `K = 5`, **4× `NKMAX`**), y a `NK = 5 760` baja a 0.5 % pero el código **ya no agrupa familias**.
En cambio **U3 pasa en toda la rejilla**: la estructura de familias **sí se lee** en el código (sim intra − inter **+0.31** con
los valores del tronco).

| NK | K = 3 | K = 4 | K = 5 |
|---|---|---|---|
| 30 (arranque del tronco) | **99.5 %** | 92.0 % | 82.5 % |
| 90 (`NKMAX`, pool lleno) | **89.5 %** | 62.5 % | 35.0 % |
| 360 (4× `NKMAX`) | 57.0 % | 18.5 % | **8.5 %** |

**Tres consecuencias, escritas antes de medir nada:**

1. **La cláusula "alias < 1 %" del bloque 1 queda RETIRADA** (es insatisfacible, y subir `NKMAX` **sería cambiar el
   organismo**, que es justo lo que este bloque prohíbe). No se sustituye por otro umbral: **no hay puerta de alias**.
2. **El bloque corre con el tamaño de código del tronco: `NK = 30`, `NKMAX = 90`, `K = 3`, con `D = 12`, sin escalar.** El
   instrumento los expone (`nk`, `nkmax`, `ktop`; `--nk/--k/--nkmax` en el runner) y los escribe en el `meta` del JSON, pero
   **el valor preregistrado es el del tronco**.
3. **El alias se DECLARA, se mide antes de correr y se reporta en cada brazo.** No es una puerta: es una **covariable del
   mundo**, y es la que explica por qué el bloque 2 y el 3 tendrán que gobernarlo (B-5 / nodo indexado por (código, P)).

**Cómo se declara (por anclas, no a mano).** Antes de lanzar nada, `corre_familias.py` **importa** `escala_codigo` y, para
cada semilla, calcula con **sus** funciones (`catalogo`, `kw_del_tronco`, `codigos` — las mismas que produjeron la tabla de
arriba) el código inicial de los 32 estímulos, y publica:

| etiqueta | definición | dónde va |
|---|---|---|
| `alias_pares` | fracción de los C(32,2) = 496 pares con **código exacto idéntico** | por semilla y por brazo |
| `alias_semilla` | 1 si existe **algún** par idéntico | por semilla |
| `sim_intra − sim_inter` | `\|cod ∩ cod\|/K` medio, intra-familia menos inter-familia (la U3 del bloque 0) | por semilla |
| **`ventana`: SEPARABLE / ALIAS** | cada uno de los 8 estímulos de `exc_win` es **SEPARABLE** si su código **no** coincide exactamente con el de ningún otro de los 32, y **ALIAS** si coincide | **subconjunto preregistrado (regla 10)** |

**Comprobación cruzada, no supuesto:** el instrumento devuelve `cod0` (el código inicial de cada estímulo tal y como lo
construye `run()`), y el runner **exige** que coincida con el de `escala_codigo` para las semillas del humo; si no coincide,
**aborta** (es la trampa ERR-38 aplicada al mundo: dos caminos al mismo número, comparados campo a campo).

**Subconjunto preregistrado (regla 10):** todas las predicciones de §6 se reportan **sobre el conjunto completo (que manda) y
al lado sobre las ventanas SEPARABLES, con los mismos umbrales**. El bloque 0 midió el alias **por pares** en **1.615 %** con
`NK = 30, K = 3`, así que se espera que la gran mayoría de las ventanas sean SEPARABLES; el número exacto por semilla se
escribe en el JSON **antes** del veredicto.

### 2.6 bis `n_neu`: el estímulo que NO informa (por qué existe la perilla y por qué está en 0 en la serie principal)

`n_neu` = número de tokens (y sus variantes) cuya mordida **no tiene consecuencia**: `dE = 0` y `R = 0` — la "sal" del bloque
de la sal. **Valor preregistrado para la serie principal: `n_neu = 0`.** Existe porque el brazo B-5 (§5) **no tiene nada que
hacer sin él**: el disparador de B-5 es literalmente `R == 0`, y en un mundo donde toda mordida tiene consecuencia
(`R ∈ {+1, −3}`) B-5 es **inerte por construcción** — lo declara su propio autor. La perilla es lo que convierte la pregunta
del coordinador en una pregunta contestable (§6, P7a/P7b).

### 2.7 Anillo y objetos: derivados, no elegidos

`L = 160`, `nobj = 16`. **Derivación (no es una perilla ajustada):** (a) la densidad de objetos es `nobj / L = 0.10`, **la
misma** que el tronco (4/40); (b) la distancia media al objeto más cercano es `L / (2·nobj) = 5` pasos, **la misma** que el
tronco (40/8 = 5) → **la economía de energía del cuerpo se conserva exactamente** y `costo = 0.002` sigue siendo el del
tronco; (c) `nobj = 16` = un objeto por estímulo presente en promedio, que es el mínimo para que los 16 presentes se
encuentren. Los tres criterios dan el mismo par y no hay grado de libertad que ajustar después.

### 2.8 Los cuatro mundos (los controles del propio mundo)

| mundo | perillas | para qué |
|---|---|---|
| **`excepciones`** | `n_exc = 4`, `fam_val='familia'` | el mundo que debe obligar |
| **`lineal`** | `n_exc = 0`, `fam_val='familia'` | **donde la fuga por píxel basta**: mismas familias, mismas ventanas, sin excepciones. Predicción **nula** |
| **`azar`** | `fam_val='azar'` (valencia por estímulo, balanceada 16/16) | **sin familias**: el parecido no predice el valor |
| **`barajado`** | `fam_val='barajado'` (cada variante toma la valencia de **otro** token) | **familias falsas por construcción** |

`exc_win` (las 8 ventanas) y los tokens son **idénticos en los cuatro mundos para la misma semilla**: el rng propio consume
en el mismo orden (tokens → `exc_win` → la permutación de `azar`, que va la última precisamente para no desplazar a las dos
primeras). **Pareado por semilla y por ventana.**

---

## 3. IDENTIDAD: `mundo='AB'` ≡ v14.1 **bit a bit**, y el rng no consumido

`organismo_familias.py` se construye **por anclas** desde `organismo/organismo_v14.py` (sha `feefc88b1fd8d434`, verificado con
aborto duro; el tronco **sólo se lee**). Con `mundo='AB'` **ninguna línea nueva se ejecuta**: todo lo del mundo de familias
vive tras `if _MF:` con `_MF = (mundo != 'AB')`, el mundo se construye con un **rng propio** (`seed + 30000`) que sólo se crea
si `_MF`, y los tamaños `NK/NKMAX/K/L/PAT` entran como **valores por defecto de la firma** (evaluados en el ámbito del módulo
al definir `run`), de modo que por defecto **son las constantes del tronco, no copias**.

**Arnés `identidad_familias.py` — 43 comprobaciones de puerta + 3 de diagnóstico** (el encargo pide ≥ 24):

| bloque | casos | × semillas | comprobaciones |
|---|---|---|---|
| **APAGADO** (`mundo='AB'`): A base · B inversión en T/2 · C estímulo nuevo C veneno · D `solap_AB=2` · E `puerta=None` · F camino θ de v10 (`div_signo=False`) · G linaje v13 (`mask_rel=0, puerta_pat=0`) · H sin memoria de rechazo | 8 | 3 | **24** |
| **RNG NO CONSUMIDO**: I `mundo='AB'` a **T = 120 000** ≡ v14.1 (si una sola línea nueva sorteara, los flujos divergirían y el dict diferiría) | 1 | 3 | **3** |
| **PERILLAS DEL MUNDO DECLARADAS PERO APAGADAS POR `mundo='AB'`**: J con `n_exc=4, fam_val='barajado', deriva=1000, fam_D=12, F=8, V=3, n_neu=2` puestas ≡ v14.1 | 1 | 3 | **3** |
| **CONJUNTO DE CLAVES**: K el dict con `mundo='AB'` tiene **exactamente** las claves de v14.1 (las del mundo de familias aparecen sólo con `mundo='familias'`) | 1 | 1 | **1** |
| **B-5 COMPUESTO**: N `mundo='AB', desambiguar=1` ≡ **`experimentos/creacion_B/organismo_v14_codigo_on.py`** (2f7794d92e68cc89) — la composición no rompe a B-5 ni B-5 rompe al mundo | 1 | 3 | **3** |
| **INERCIA DE B-5 EN EL MUNDO NUEVO** (predicción de inercia, como la I5 de B-5): P `mundo='familias', n_neu=0, desambiguar=1` ≡ el mismo con `desambiguar=0` — es **P7a** comprobada a T corto **antes** de gastar `Pool` | 1 | 3 | **3** |
| **CONTROLES QUE DEBEN FALLAR** (sin ellos el arnés pasaría por vacuidad): L `mundo='familias'` **≠** v14.1 · M `mundo='AB'` con `renov=1.0` **≠** v14.1 (la renovación no es una perilla muerta) | 2 | 3 | **6** |
| **TOTAL (puerta)** | | | **43** |
| *Diagnóstico, NO puerta:* Q `mundo='familias', n_neu=2, desambiguar=1` contra `desambiguar=0` — **si son idénticos, B-5 tampoco se dispara con neutros**, y eso es P7b(i) cayendo, que es un **resultado**, no un fallo del instrumento: por eso se reporta y no bloquea | 1 | 3 | *(3)* |

**Guarda dura:** si el arnés no da **43/43**, no se corre nada (ni humo ni serie). El runner repite el subconjunto crítico
(A, G, I, J, N, P, L, M) como etapa 1/2 y aborta si falla.

---

## 4. MEDIDAS (todas de sólo lectura; ninguna toca el rng ni la decisión)

### 4.1 `exp_asoc` — exposiciones hasta asociar (la medida que manda desde el 05:10)

`exp_asoc[k]` = número de **exposiciones** (llegadas nuevas al objeto: `_prev_on != pos`, **nunca** encuentros agregados)
hasta la primera en la que **el valor que usa la boca** (`_wt`, la lectura ruteada real, no un peso interno) tiene **el signo
del mundo** para ese estímulo **y** `|_wt| ≥ crit_exp = 0.5` (la definición de B-4 y del mundo vivo, sin cambios). Se reporta
**por patrón** y agregada **por clase**: `token` · `variante` (no excepcional) · `excepcion` (las activas) · `ventana`
(las 8 de `exc_win`). Censurada (`None`) si nunca cruza; la **regla de censura** es: los no cruzados se cuentan aparte
(`n_cruza`) y **nunca** se imputan (§E.4).

### 4.2 `colateral` — daño a los hermanos al aprender la excepción (**la medida que decide**)

**Ventana:** los `vent = 10 000` pasos que siguen a la **primera mordida** de cada estímulo de `exc_win` (abierta igual en los
cuatro mundos, §2.2). **Hermanos** de una ventana `e` = su token **y** las otras variantes de ese token, **excluida `e`**.

- **`colateral`** = **mordidas de veneno en los hermanos** dentro de alguna ventana abierta. Es la letra literal de
  `CRITERIO_TRONCO_v2` T-G(ii) y de §C.2 del bloque 1.
- **`omision`** = llegadas a hermanos **comestibles** en las que la boca **no mordió**, dentro de alguna ventana abierta. Es
  la otra mitad del daño (la excepción venenosa contamina la lenta hacia abajo y el organismo deja de comer a sus hermanos).
  Se **reporta** y no es puerta: está confundida con la saciedad, y decirlo antes vale más que usarla.
- **`colateral_tot` = `colateral` + `omision`**: se reporta.

`colateral` es una **integral de trayectoria** → **A₁₂ sin parear, razón de medianas y cuartiles; nunca pareado, nunca `max`**
(ERR-37b, ERR-37c).

### 4.3 `w_var` — ¿queda limpia la vía lenta?

`w_var` = mediana de `|Wps − Wns|` sobre los **3 píxeles de variable** al final de la corrida. En `lineal` esos píxeles no
informan de nada (están en la mitad de los estímulos presentes, mitad comida y mitad veneno) → deben quedar bajos. En
`excepciones` son **lo único** que distingue a la excepción de sus hermanos → la vía lenta tiene que cargarlos.

### 4.4 Supervivencia y coste (línea base de T-A y T-F)

`muertes` por 100 000 pasos · `frac_regalo = 0.6 · muertes / (T · costo)` (**obligatorio**, §E.7: cuánto del presupuesto de
energía lo financia el renacer) · `celdas` · `splits` · `ruta` por visita (`exacto` / `lenta`, las dos únicas de v14.1) ·
`frac_veneno` del anillo por cuartos · `renovados` (objetos retirados por renovación simétrica) · `exposiciones` por patrón.

### 4.5 Retención y lectura a priori

`ultima[k]` = `(t, valor leído por la boca, signo del mundo)` en la **ÚLTIMA** visita de cada patrón — la medida que §E.12
señala como ausente en todos los diseños de la sala (*"no medir 'aprende en una' sin medir 'lo retiene'"*).
`primera[k]` = lo mismo en la **PRIMERA** visita (lectura a priori). Se reportan; **no** son puerta en este bloque.

---

## 5. BRAZOS

**Organismo: `v14.1 tal cual`** (`organismo_familias.run(...)` con **todas** las perillas del tronco en sus valores de v14.1).
**No hay órgano nuevo.** La única perilla de organismo que se enciende en algún brazo es **B-5 (`desambiguar=1`)**, que es una
**reparación ya medida** (18/18 ALIAS; tronco idéntico: examen 8/8 y generalización 40/40) y **no** un candidato de capacidad
— entra por encargo del coordinador para ver si la reparación del alias cambia `colateral` / `w_var` en el mundo nuevo.

| brazo | mundo | perillas | papel |
|---|---|---|---|
| **EXC** | `excepciones` | `mundo='familias', n_exc=4, fam_val='familia', renov=1.0, n_neu=0, desambiguar=0` | el mundo que debe obligar |
| **LIN** | `lineal` | `n_exc=0`, resto igual | **el lector lineal de referencia** (§ abajo) |
| **AZA** | `azar` | `fam_val='azar'`, resto igual | sin familias |
| **BAR** | `barajado` | `fam_val='barajado'`, resto igual | familias falsas |
| **EXC-B5** | `excepciones` | = EXC + **`desambiguar=1`** | B-5 en el mundo que obliga |
| **LIN-B5** | `lineal` | = LIN + **`desambiguar=1`** | B-5 donde la fuga basta |
| **NEU** | `excepciones` + **`n_neu=2`** | `desambiguar=0` | el mundo con **estímulos que no informan** (`R = 0`): el único régimen donde B-5 tiene disparador |
| **NEU-B5** | `excepciones` + **`n_neu=2`** | **`desambiguar=1`** | la pregunta del coordinador, contestable |
| **V14** *(ancla)* | `AB` | `mundo='AB'` | v14.1 literal; fila de referencia del cuerpo en el JSON, **no** compite en ninguna predicción |

**8 brazos × 20 semillas = 160 corridas** de T = 100 000 (+ la fila ancla V14, 20 corridas de 6 px que cuestan segundos).

**El "lector lineal de referencia" es LIN, no un organismo nuevo.** `DISENO_grafo_tokens` lo llama *lector lineal*; en un
bloque cuya premisa es *"v14.1 sin cambios"*, inventar un segundo organismo sería el segundo cambio. El lector lineal aquí es
**la misma vía lenta de v14.1 en el mundo donde le basta** (`lineal`). Se declara así para que nadie lo lea como un olvido.

**Brazos de `DISENO_grafo_tokens` que NO aplican aquí y por qué:** `INV` (propagación por la familia) está **contenido** en el
cambio de familia de §2.3, y se lee en las mordidas de veneno de las variantes de T0 tras `T/2`; `FRONTERA` (sin hermanos,
predicción de igualdad) y `SIN_CORTE` sólo tienen sentido **con un grafo** — pertenecen al bloque 3 y meterlos aquí sería
medir un órgano que no existe. `AZAR` sí entra (es `azar`, §2.8). **Barajado** entra como `barajado`. Se dice explícitamente
para que nadie lea su ausencia como un olvido.

**Semillas: 401–420** (nuevas, no usadas por ningún bloque del repo). **Réplica automática: 421–440**, misma letra (regla 12).
Semillas del arnés: **1, 2, 3** — ninguna de 401–440 queda expuesta. `T = 100 000` (regla 6).

---

## 6. PREDICCIONES NUMÉRICAS (escritas antes de construir el instrumento)

Estadística, fijada ahora: lo aprendido (`exp_asoc`, signos) se **parea** por semilla y por patrón; `colateral`, `omision`,
`muertes` y todo lo que sea integral de trayectoria va con **A₁₂ sin parear, razón de medianas y cuartiles** (ERR-37b);
**ningún umbral en la mediana esperada del propio efecto** (ERR-37a); **medianas y cuartiles, nunca `max`** (ERR-37c).

| # | predicción | umbral (escrito aquí) | qué me refuta | zona declarada |
|---|---|---|---|---|
| **P1 — validez del mundo** (puerta; si cae, P2–P5 no se leen) | la renovación simétrica **quita** la trampa 3 y el mundo es habitable | (a) `frac_veneno` del anillo: mediana en **[0.35, 0.65]** en los 4 cuartos, en los 4 mundos; (b) razón `exposiciones(veneno) / exposiciones(comida)` mediana en **[0.7, 1.4]** (hoy: **6.3×** y **23×**); (c) en `lineal`, v14.1 cruza criterio en **≥ 4 de los 8 tokens** en ≥ 16/20 semillas | (a) o (b) fuera de banda → la renovación no simetriza; (c) falla → el mundo es inhabitable o ilegible | cláusula (iii): **UNA** corrección de `renov` con **ERR-46**, semillas nuevas, misma letra |
| **P2 — `colateral` (LA QUE DECIDE)** | v14.1 paga la excepción contaminando a los hermanos | `colateral(EXC) ≥ 2.0 × colateral(LIN)` en **razón de medianas** **y** `A₁₂(EXC > LIN) ≥ 0.75` | razón **≤ 1.3** o `A₁₂ ≤ 0.60` → **el mundo no obliga** | razón en **(1.3, 2.0)** o `A₁₂` en (0.60, 0.75) → **INDECISO**: se endurece `n_exc` 4 → 8 con **ERR-46** y se repite en 441–460. **No hay zona muerta** |
| **P3 — `w_var` (LA QUE DECIDE)** | la excepción ensucia los píxeles de variable de la vía lenta | `w_var(EXC)` mediana **≥ 1.0** **y** `w_var(LIN)` mediana **≤ 0.5`. Acompaña (se reporta, no decide): razón de medianas `≥ 2.0` con `A₁₂ ≥ 0.75` | `w_var(EXC) < 1.0` → la lenta no se corrompe con 4 excepciones; `w_var(LIN) > 0.5` → los píxeles de variable ya están sucios sin excepciones y la medida no discrimina | cualquiera de las dos → mismo tratamiento que P2 (endurecer, ERR-46). **Derivación del umbral, para que no esté dentro del rango aritmético del propio efecto (ERR-37a):** una sola mordida de excepción mueve la lenta `eta_s · \|R − _ws\| ≈ 0.15 · 4 = 0.60` en cada píxel del patrón; **1.0 está por encima de una mordida y 0.5 por debajo**, y el hueco entre los dos umbrales es real, no decorativo |
| **P4 — exposiciones** | las exposiciones crecen con los **estímulos**, no con tokens + excepciones | `exp_asoc` mediana de las **excepciones activas** `≥ 3 ×` la de los **tokens** de la misma corrida, pareado por semilla en ≥ 15/20; y `exp_total(EXC) ≥ 1.3 × exp_total(LIN)` sobre los patrones que cruzan en **ambos** | excepciones ≈ tokens → la fuga por píxel ya cubre la excepción y la economía de exposiciones no tiene nada que comprar | se reporta `n_cruza` al lado **siempre**; una excepción censurada **no** cuenta como victoria (`None` nunca gana, convención de `corre_vivo.py`) |
| **P5 — orden de los cuatro mundos** (control de que las medidas leen estructura) | `lineal < excepciones ≤ barajado ≤ azar` en `colateral` **y** en `w_var` (medianas) | **≥ 3 de las 4** desigualdades (2 por medida) se cumplen | `lineal ≈ azar` en las dos medidas → las medidas **no leen familias** y el instrumento, no el mundo, es lo que falla | si P5 cae, P2 y P3 se reportan pero **no se declara nada**: primero se arregla el instrumento |
| **P6 — identidad y seguridad** | el instrumento no toca el tronco | arnés **43/43**; `mundo='AB'` ≡ v14.1 a T = 120 000; `mundo='AB', desambiguar=1` ≡ `organismo_v14_codigo_on` (2f7794d92e68cc89); los **dos** controles que deben fallar fallan; sha de `organismo/organismo_v14.py` == `feefc88b1fd8d434` | cualquier caída → **no se corre nada** | — |
| **P7a — B-5 es INERTE en el mundo tal como está preregistrado** (`n_neu = 0`) | el disparador de B-5 es literalmente `R == 0`, y con `n_neu = 0` **toda** mordida tiene consecuencia (`R ∈ {+1, −3}`) | **EXC-B5 ≡ EXC y LIN-B5 ≡ LIN, BIT A BIT, en 20/20 semillas**, con `des_splits = 0` en 20/20 | **cualquier** diferencia → hay un camino con `R == 0` en mi mundo que yo no vi, y **paro a buscarlo antes de leer P2–P5** | es un **control que debe cumplirse**, no una hipótesis: si se cumple, la respuesta a la pregunta del coordinador es *"la reparación del alias no puede cambiar `colateral` ni `w_var` en un mundo donde todo estímulo informa — le falta el disparador, no el efecto"* |
| **P7b — B-5 en el mundo con estímulos que NO informan** (`n_neu = 2`, brazos NEU / NEU-B5) | el bloque de la sal medido en el mundo nuevo: con `R = 0` el token neutro hereda el valor del que colisiona con él, y B-5 lo repara dividiendo | (i) **actúa**: `des_splits ≥ 1` en ≥ 16/20 semillas con al menos una ventana ALIAS, y `= 0` en las semillas sin ninguna colisión que afecte a un neutro; (ii) **repara**: mediana de `\|W\|` de los estímulos **neutros** al final: NEU-B5 `≤ 0.5 ×` NEU, pareado en ≥ 15/20; (iii) **no rompe el mundo**: `muertes` NEU-B5 ≤ 1.10 × NEU y `colateral` NEU-B5 dentro de ±25 % de NEU (razón de medianas) | (i) falla → el disparador no se da ni con neutros (el alias que mide el bloque 0 no llega a la conducta); (ii) falla → B-5 no repara **aquí** aunque reparase en 6 px; (iii) falla → la reparación **cuesta** en el mundo nuevo, y eso es información para el bloque 3 | **predicción honesta:** predigo (i) y (ii) **flojos** — el alias del bloque 0 es entre **dos estímulos cualesquiera** de 32, y la probabilidad de que la colisión caiga precisamente entre un neutro y un informativo **presente a la vez** es una fracción pequeña de ese 1.6 % por par. Si sale así, la letra es: *"el alias es masivo por semilla pero raro por par útil; B-5 repara lo que toca y toca poco"* |

**Predicción global, para poder equivocarme.** Predigo que **P1 pasa (a) y (b) pero es la más frágil en (c)**: con 16
estímulos presentes y renovación total, cada patrón recibe ~1/8 de las exposiciones del tronco y puede que ni los tokens
crucen criterio; **P2 pasa** (es el mecanismo de B5 de `DISENO_mundo_grande`: 0.6/px por mordida de excepción); **P3 pasa en
`EXC` y es dudosa en `LIN`** (los píxeles de variable están en la mitad de los estímulos y el drenaje `lam` puede no bastar);
**P4 es la más probable de caer** (la excepción tiene código propio y la puerta por código la manda a la lenta, que la aprende
rápido); **P5 pasa**. Si **P2 y P3 caen las dos**, la letra es: ***"con 4 excepciones sobre 32 estímulos el mundo no obliga:
la fuga por píxel de v14.1 basta"***, se endurece a `n_exc = 8` con ERR-46 y **no se toca el organismo**.

---

## 7. LO QUE ESTE BLOQUE ENTREGA (y que hoy no existe)

**La línea base de v14.1 en el mundo que obliga, congelada con su sha y su JSON**, para `CRITERIO_TRONCO_v2.md`:

- **T-A:** `muertes` por 100 000 pasos y `frac_regalo`, medianas y cuartiles, en los cuatro mundos. *(`r = descendientes −
  muertes` **no** se reporta: este bloque no tiene reproducción, y fabricar un `r` sin ventanas sería la tercera versión de una
  medida ya retirada dos veces, ERR-40.)*
- **T-F:** `celdas`, `splits`, `muertes`.
- **T-G:** `exp_asoc` por clase, `colateral`, `omision`, `w_var`, `ruta` por visita, `ultima` (retención) y la **tabla de
  exposiciones por patrón** al lado de todo lo agregado (§E.10).

**Nota que hay que pegar en `CRITERIO_TRONCO_v2.md` §2 cuando el coordinador lo integre:** *la línea base de T-A, T-F y T-G la
fija este bloque; se congela con su sha y su JSON, y cambiarla después lleva ERR y fecha. Ningún candidato se juzga con T-A ni
T-G antes de que esa línea base exista.* **Yo no edito ese archivo.**

---

## 8. COSTE

| pieza | coste |
|---|---|
| `construye_familias.py` → `organismo_familias.py` (por anclas, aborto duro por sha) | escrito |
| `identidad_familias.py` (43 comprobaciones de puerta + 3 de diagnóstico, **un proceso**, T = 20 000 y 120 000) | ~4–8 min de un proceso |
| `corre_familias.py --humo` (**un proceso**, 2 semillas, T ≤ 200 000) | ver §12 |
| **serie 401–420**: 8 brazos × 20 semillas = **160 corridas** de T = 100 000, retina 12, L = 160, nobj = 16 (+ 20 del ancla V14, 6 px) | estimado en §12 desde el humo; con `Pool(14)` el orden esperado es de minutos. **El `Pool` lo lanza SÓLO el coordinador** (regla 3), y nunca con otro `Pool` vivo (regla 11) |
| réplica 421–440 | igual |
| gemelo numba | **no** en este bloque (regla 9: antes de congelar algo, sí; aquí no se congela nada) |

---

## 9. TRAMPAS QUE ESTOY EVITANDO A PROPÓSITO (§E de la síntesis, punto por punto)

1. **No preguntarle al mundo de 6 px lo que no contiene** (§E.1, ERR-35): todo se mide en D = 12; D = 6 aparece **sólo** en el
   arnés de identidad.
2. **Ningún peso interno como puerta** (§E.2, T-E, ERR-44): `exp_asoc` se define sobre **el valor que usa la boca** (`_wt`, la
   lectura ruteada), no sobre `Wp−Wn`. `w_var` **sí** es un peso interno — y por eso **se declara como medida del mundo (¿la
   vía lenta se ensucia?), no como puerta de tronco**; ningún candidato se juzgará con ella.
3. **Umbrales fuera del rango aritmético del propio efecto** (§E.3, ERR-37a): P3 trae su derivación (0.60 por mordida) al lado
   del umbral; P2 usa `2.0×` sobre un control que tiene la **misma ventana** y no un cero por construcción.
4. **Sin zonas muertas** (§E.4): P2 y P3 declaran la zona INDECISA y qué se hace en ella; la regla de censura de `exp_asoc`
   está escrita en §4.1.
5. **No exigir más de lo que la información permite** (§E.5): P1(c) es exactamente esa guarda, puesta **antes**.
6. **Nada copiado a mano** (§E.6, ERR-38/41/42/43): instrumento por anclas con aborto duro; el humo **escribe su JSON**; los
   umbrales viven en un dict `UMBRALES` con la **frase literal** de este documento al lado (ERR-31).
7. **`frac_regalo` obligatorio** (§E.7, ERR-40): se reporta siempre; `r` no se fabrica.
8. **Sin controles de paja** (§E.8, ERR-39): `lineal` **no** es "el mismo mundo sin nada"; tiene las mismas familias, los
   mismos tokens y **las mismas ventanas de medida** — es el control que **puede ganar**.
9. **Sin desempatar por índice** (§E.9): el catálogo y `exc_win` se sortean con un rng propio del mundo; el orden de token en
   `exc_win` es una **decisión estructural declarada**, no un desempate.
10. **Nada agregado sin su tabla de exposiciones** (§E.10): `exposiciones` por patrón va en el JSON de cada corrida.
11. **Ningún órgano que el ruteo apague** (§E.11): **no hay órgano**. Lo que sí se comprueba antes de firmar es la aritmética
    de la ventana de `colateral` en los dos órdenes de mordida (la ventana la abre la **primera** mordida del estímulo de
    `exc_win`, exista o no la excepción).
12. **"Aprende en una" sin "lo retiene"** (§E.12): `ultima` se mide y se reporta.
13. **No llamar "v16" a nada** (§E.13): este instrumento se llama `organismo_familias` y **no es un candidato**.
14. **Sin cifras de un humo del propio conjunto de prueba** (§E.14): el humo usa semillas **1–2**; la serie, 401–420.
15. **Sin calibrar un mundo con la mortalidad de otro** (§E.15): `L`, `nobj` y `costo` se derivan de la **propia** física del
    tronco (§2.7), no se trasplantan del mundo vivo.
16. **Ninguna capacidad como perilla** (§E.16, 09:55 §3): no hay capacidad nueva en el organismo; lo único nuevo es el mundo.
17. **No recalibrar tras ver datos** (§E.17, regla 3/11): las cláusulas de endurecimiento están escritas **aquí**, con su ERR
    reservado (**ERR-46**) y sus semillas (441–460).
18. **Vocabulario** (§E.18, regla 8): §1 dice la única frase declarable.

---

## 10. QUÉ NO PUDE / QUÉ QUEDA ABIERTO (antes de correr)

1. **La renovación simétrica no tiene un número detrás** (§F.10). Es mi injerto; P1 es su guarda y la cláusula (iii) su
   salida.
2. **`C-ALIAS` (§2.6): el mundo nuevo nace con la enfermedad del viejo** y no hay forma de evitarlo sin tocar `NKMAX`. La
   línea base se mide **con** alias y el subconjunto SEPARABLE es la lectura limpia.
3. **Peldaño 2 (dos necesidades) declarado y no construido** (§2.5).
4. **Sin gemelo numba**: cada réplica cuesta minutos donde el tronco cuesta segundos (§F.7).
5. **`bateria_exposiciones.py` (bloque 0b) sigue sin existir**: `exp_asoc` se define aquí con la definición de B-4, pero
   **no** está en ninguna batería del tronco (§F.6, M6). Este bloque la usa; no la instala.
6. **No hay "variante nunca vista"** en el catálogo: las 3 variantes de cada token aparecen por deriva. Lo más parecido es la
   variante que entra **después** del cambio de familia, y se reporta como `primera[k]` en esa fase — **no** como predicción.
7. **La composición con B-5 sigue sin medir** (§F.11): en un mundo con variantes, B-5 y cualquier órgano de tokens pelearían
   por las mismas celdas.

---

## 11. IDENTIDAD — resultado (18 sep 2026; §1–§10 no se tocaron)

`python experimentos/nivel12_mundo_familias/identidad_familias.py` — **UN proceso, sin `Pool`** (regla 3), semillas
1, 2, 3, T = 20 000 (y 120 000 en el ancla del rng). **IDENTIDAD 43/43.**

| bloque | caso | resultado |
|---|---|---|
| APAGADO (`mundo='AB'`) | (A) base · (B) inversión · (C) estímulo nuevo · (D) `solap_AB=2` · (E) `puerta=None` · (F) camino θ v10 · (G) linaje v13 · (H) sin memoria de rechazo | **24/24 IDÉNTICO** a `organismo_v14` |
| RNG no consumido | (I) `mundo='AB'` a **T = 120 000** | **3/3 IDÉNTICO** |
| perillas del mundo puestas pero apagadas por `mundo='AB'` | (J) `fam_D=12, fam_F=8, fam_V=3, n_exc=4, n_neu=2, fam_val='barajado', deriva=1000, cambio=5000, vent=3000` | **3/3 IDÉNTICO** |
| B-5 compuesto | (N) `mundo='AB', desambiguar=1` ≡ `creacion_B/organismo_v14_codigo_on.py` (2f7794d92e68cc89) | **3/3 IDÉNTICO** |
| inercia de B-5 (P7a a T corto) | (P) `familias, n_neu=0`: `desambiguar=1` ≡ `desambiguar=0` | **3/3 IDÉNTICO** |
| conjunto de claves | (K) con `mundo='AB'` el dict es el de `organismo_v14_codigo_on`: v14 **+ las tres de sólo lectura de B-5** (`desambiguar`, `des_splits`, `des_t`) | **1/1 IDÉNTICO** |
| **controles que DEBEN fallar** | (L) `mundo='familias'` ≠ v14 · (M) `mundo='AB'` con `renov=1.0` ≠ v14 | **6/6 DIFIERE (como debe)** |

**Las 22 claves nuevas aparecen SÓLO con `mundo='familias'`:** `mundo, fam, val_mundo, exc, exc_win, herm, cod0,
cod_fin, exposiciones, exp_asoc, primera, ultima, ruta, colateral, omision, colateral_tot, t_exc, w_var, w_var_med,
renovados, frac_veneno, frac_regalo`.

**Precisión sobre §3 que hay que decir (y que la letra de §3 no anticipaba):** con `mundo='AB'` el dict **no** tiene
*exactamente* las claves de v14.1, sino las de **`organismo_v14_codigo_on`** — v14.1 **más las tres de sólo lectura de
B-5**. Es consecuencia de componer B-5 por encargo del coordinador, es la misma situación que B-5 ya tiene aceptada en
el proyecto (inerte; examen 8/8 y generalización 40/40), y **todos los valores de las claves de v14.1 son bit a bit los
del tronco**. Se declara aquí en vez de redefinir el caso (K) en silencio.

**Diagnóstico (NO es puerta):** (Q) `familias, n_neu=2`: `desambiguar=1` **DIFIERE** de `desambiguar=0` en 3/3 →
**B-5 sí se dispara cuando el mundo tiene estímulos que no informan**. P7b(i) tiene soporte; su magnitud la mide la serie.

## 12. HUMO — resultado (18 sep 2026; §1–§10 no se tocaron)

`python experimentos/nivel12_mundo_familias/corre_familias.py --humo` — **UN proceso, sin `Pool`, 4 corridas**
(EXC y LIN × semillas **1 y 2**) **a la T real del bloque (100 000)**, dentro del límite de la regla 3 de EQUIPO
(≤ 6 corridas, ≤ 200 000 pasos). Ninguna semilla de 401–440 quedó expuesta (§E.14). JSON:
`datos/familias_humo_20260918_144533.json` (sha16 `ec247d84e8e94c0b`), log al lado.
**shas:** instrumento `b9dd561a0cf056b8` · constructor `b488e3edce8f535f` · arnés `f24da0c025faa922` ·
`escala_codigo` (bloque 0) `d8b8566bca77a0ae` · origen `organismo_v14.py` `feefc88b1fd8d434` ·
origen `organismo_v14_codigo_on.py` `2f7794d92e68cc89`.

**Guardas que pasaron antes de mirar un solo número:** identidad 16/16 en el subconjunto crítico (A, G, I, J, N, P, L, M)
· **cruce `cod0`: el código inicial que construye el instrumento es IDÉNTICO CAMPO A CAMPO al que calcula
`escala_codigo` (bloque 0)** — dos caminos al mismo número, la guarda de ERR-38 aplicada al mundo.

### 12.1 La tabla del humo (n = 2: **NO es evidencia**, §E.14)

| brazo | semilla | `colateral` | `omision` | `w_var` (3 px) | `w_var_med` | muertes | `frac_regalo` | celdas | splits | `exp_total` | razón exp. veneno/comida | `ruta` exacto/lenta | retención exc. |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| **EXC** | 1 | **0** | 98 | [0.003, 0.0, 0.0] | **0.000** | 2 | 0.006 | 53 | 23 | 283 | **1.020** | 6236 / 6007 | 0.50 |
| **EXC** | 2 | **8** | 41 | [0.016, 0.0, 0.012] | **0.012** | 1 | 0.003 | 68 | 38 | 257 | **0.992** | 6428 / 6242 | 0.75 |
| **LIN** | 1 | **0** | 0 | [0.0, 0.0, 0.0] | **0.000** | 0 | 0.000 | 46 | 16 | 545 | **1.005** | 4912 / 7683 | — |
| **LIN** | 2 | **0** | 22 | [0.0, 0.0, 0.0] | **0.000** | 1 | 0.003 | 51 | 21 | 104 | **1.020** | 5516 / 6906 | — |

`exp_asoc` por clase (mediana dentro de la corrida): **EXC** token 3.5 / 3.0 · variante 1.0 · excepción 2.0 / 2.0 —
**LIN** token 2.0 / 3.0 · variante 1.0. Tokens que cruzan criterio: **8 de 8 en las cuatro corridas**.
`frac_veneno` del anillo por cuartos: EXC s1 [0.535, 0.480, 0.562, 0.632]; LIN s1 [0.517, 0.492, 0.630, 0.640].
Objetos retirados por renovación simétrica: 7 068–7 601 por corrida.
Diagnóstico estructural (T = 0, antes de simular): alias por par **0.00605** (s1) y **0.04234** (s2); U3 (sim intra −
inter) **+0.292** y **+0.362**; ventanas **SEPARABLE 6/8** (s1) y **4/8** (s2).
Coste medido: **5.5 s por corrida** → el bloque completo (9 brazos × 20 semillas = **180 corridas**) ≈ **1.2 min de
pared con `Pool(14)`**; la réplica, igual.

### 12.2 Qué dice el humo, sin ajustar nada

1. **La renovación simétrica funciona, y es el resultado más limpio del entregable.** La razón de exposiciones
   veneno/comida es **0.99–1.02** en las cuatro corridas, contra **6.3×** en la mini y **23×** en el ancla V14 del mundo
   vivo. La trampa 3 (*"lo mordido desaparece, lo rechazado se queda"*) **desaparece** con `renov = 1.0`. P1(a) y P1(b)
   apuntan a pasar; P1(c) pasa con holgura (8/8 tokens).
2. **P3 apunta a caer, y por un mecanismo que no es el que yo escribí.** `w_var` ≤ 0.016 en **todas** las corridas,
   incluida `excepciones`: la vía lenta **no carga** los píxeles de variable. La causa más probable es el drenaje `lam`
   sobre la parte común de `Wps`/`Wns`: el píxel de variable está encendido en la mitad de los estímulos presentes, con
   las dos valencias, así que `min(Wps, Wns)` crece y `lam` lo borra. El umbral **no se toca** (regla 3): si la serie lo
   confirma, la letra es *"la vía lenta de v14.1 no se ensucia en los píxeles de variable: los drena"* — información
   nueva, no un fallo del instrumento.
3. **P4 apunta a caer, y al revés de lo previsto.** Las excepciones cruzan criterio **antes** que los tokens
   (2.0 contra 3.0–3.5), no 3× después. Tiene sentido mecánicamente: la excepción tiene **código propio** y la puerta por
   código la manda a la vía rápida, que aprende un caso deprisa; el token, presente en más contextos, tarda más.
4. **P2 tiene señal pero muy poca masa.** `colateral` 0 y 8 en EXC contra 0 y 0 en LIN; `omision` 98/41 contra 0/22. Con
   medianas de 0 la razón de P2 puede quedar indefinida en la serie. **No cambio la letra**: si sale así, se reporta
   `colateral` con sus cuartiles y `A₁₂`, se declara INDECISO por la zona ya escrita, y se endurece `n_exc` 4 → 8 con
   **ERR-46** — que es exactamente lo que el preregistro manda hacer.
5. **Aviso serio para T-A: el mundo casi no mata.** 0–2 muertes por 100 000 pasos y `frac_regalo` ≤ 0.006, contra
   **124–159** muertes del anillo del tronco. La línea base de T-A en este mundo tendrá **efecto suelo**: *"muertes ≤ 1.10 ×
   línea base"* no discriminará nada. Es consecuencia directa de la renovación simétrica (el organismo siempre tiene
   comida fresca cerca) y hay que decírselo al coordinador **antes** de que T-A se escriba sobre esta línea base.
6. **El código se reorganiza durante la corrida:** 15–26 de los 32 estímulos cambian de código entre `t = 0` y `t = T`
   (`cod_cambia`) por las fisiones de v11. El alias declarado en §2.6 es el **inicial**; el del régimen es otro, y el
   instrumento guarda los dos (`cod0` y `cod_fin`) para que el bloque 2 pueda medirlo sin volver a correr.

## 13. SERIE 401–420 — resultado

*(Vacío al firmar. Lo escribe el coordinador cuando lance el `Pool`.)*
