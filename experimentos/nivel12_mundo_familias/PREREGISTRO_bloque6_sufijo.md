# PREREGISTRO — BLOQUE 6: **SUFIJO DE VARIANTE** — que el mensaje distinga "sal rosa" de "sal" (E-8)

**MISIÓN (primero, siempre):** llegar a la AGI por este camino — un organismo mínimo con reglas locales, sin
retropropagación ni supervisor global, que aprende, desaprende, generaliza, sobrevive y **se comunica con
referencia**. Hoy, exactamente: que el mensaje distinga **`sal rosa`** de **`sal`**.

**Fecha:** 2026-09-18. **Creador:** Claude (Opus), completando el encargo externo a Codex (cuello A).
**Estado:** escrito **antes** de correr un solo brazo de las series 721–740 y 741–760. El humo del §9 se corrió
después de fijar §0–§8 y no los tocó. Los §0–§8 no se editan una vez corrida la serie; lo que cambie va en ERR
numerado con fecha, motivo y semillas nuevas.

**Herencia del creador externo.** Codex dejó `experimentos/externo_codex/cuelloA/` (preregistro + constructor) y
murió. Se toma su **mecanismo** (el sufijo de variante en la dirección de la tabla de pares) y se corrigen tres
cosas suyas, por escrito:

1. **Su premisa fáctica sobre el bloque 5 es falsa.** Escribió: *"El BLOQUE 5 de varias ganadoras no aporta
   evidencia conductual: ambos rangos 681–700 y 701–720 se detuvieron en la guarda de identidad."* No es así: el
   bloque 5 corrió las dos series completas y dio evidencia conductual replicada (registro, 18 sep 19:42 y 19:50;
   540 corridas por serie). Con `k_ganadoras = 3`, BAR-T cayó de 7/20 a **2/20 y 4/18** con el canal intacto
   (19/20, 16/18). Esa evidencia es justamente la que fija el punto de partida de este bloque, y por eso este
   preregistro **sí** repite `k_ganadoras` — como factor, no como competidor.
2. **Construyó desde `organismo_familias_b4b.py`**, que ya no es la frontera. Este bloque construye por anclas
   desde **`organismo_familias_b5.py`** (`e0b6b90f6f92d5c1`), para que `k_ganadoras` y el sufijo se puedan cruzar
   en el mismo instrumento.
3. **Su aritmética de subcasillas está mal**: con `fam_nvar = 3` la firma tiene 3 bits, así que cada celda pasa de
   4 a **4 × 2³ = 32** subcasillas, no a 8. Se usa 32 y se declara el precio (§3.4). El encargo repite el "8"; se
   corrige aquí en vez de arrastrarlo.

---

## 0. **E-8 — el error que este bloque ataca, con su evidencia**

**E-8 (el techo de la FORMA).** La vía lenta de v15f direcciona la tabla por el **bin de 2 bits de un par de
píxeles**. En el mundo de familias la retina tiene 12 píxeles: **0–8 son FORMA** (token) y **9–11 son VARIANTE**.
Las celdas que ganan son de forma —su error propio es menor, porque en este mundo el valor lo fija el token y los
píxeles de variante son ruido respecto de la recompensa—, y **una celda de forma no puede ver la variante por
construcción**. Multiplicar celdas (`k_ganadoras`) multiplica bits de forma, no resuelve variante.

Evidencia medida, dos series cada una:

| hecho | serie / réplica | de dónde |
|---|---|---|
| con k = 3, el patrón de **otro token** deja de arrastrar | BAR-T **2/20 · 4/18** contra CORTADO 0/20 · 1/18 | bloque 5 |
| ...con el canal **intacto** | CANAL **19/20 · 16/18** | bloque 5 |
| ...y "sin referencia" ≈ mudo | VALOR 4/20 · 3/18 | bloque 5 |
| **la HERMANA no baja** | BAR-H **15/20 · 13/18** | bloque 5 (R3 cae ×2) |
| k = 5 no ayuda y **rompe el cuerpo** | BAR-T 7/20 · 7/18; muertes **199.5 · 152** contra 32–38 | bloque 5 |
| antes, con una sola ganadora | BAR-T 9/18 · 6/19; BAR-H 15/18 · 13/19 | bloque 4b (−) sola |

H-4 quedó cerrada en el registro: **no es k**. La referencia de variante no está en cuántas celdas se leen.

**Hecho ESTRUCTURAL del catálogo** (`escala_codigo.catalogo`, T = 0, sin simular; mirado antes de escribir las
predicciones, en las semillas **1, 2, 3, 721, 730, 741** — ninguna de ellas es del rango de la serie salvo 721,
730 y 741, que se miran **sólo** por este cálculo determinista que no toca conducta):

- `T1v2` y su hermana `T1v0` difieren **sólo en los píxeles 9 y 11** — los dos dentro del bloque de variante.
  Luego una dirección que incluya 9–11 **sí puede** separarlas, y una que no los incluya **no puede**, por muchas
  celdas que se lean. Esto es lo que hace del sufijo la intervención correcta y no una más.
- La firma de 3 bits parte los 32 estímulos en **8 grupos de 4** (los `*v2` de los 8 tokens comparten firma).
  Cruzada con el piso estructural de forma del bloque 5 (**4** = la familia: el token y sus 3 variantes), la
  intersección predicha es **exactamente 1 de 32: el referente solo**.

---

## 1. La pregunta

**¿Basta con que cada celda de pares guarde y consulte su valor en una dirección que lleva pegada la firma de los
3 píxeles de variante, para que la recompensa de un mensaje sobre `sal rosa` deje de mover la boca ante `sal` —
sin romper el canal ni el cuerpo?**

---

## 2. LO QUE NO CAMBIA

Se importan, no se recopian (ERR-31): el mundo (bloque 1/2, `escala_codigo.catalogo`), el canal y su letra
(bloque 4), el emisor voraz (bloque 4b, `voraz = 1.0`, ERR-51), la lectura de la boca y el análisis (bloque 5,
`corre_familias_b5.py`). Dentro del organismo **no** se tocan: la selección de la ganadora `_MGv` ni su desempate
al azar, el error propio por celda `_MEv`, la regla de sobrescritura de R **CRUDO**, la vía lineal, la puerta, la
boca, el metabolismo, ni el consumo del rng.

**El emisor corre con `memoria_variante = 0` y `k_ganadoras = 1`**: es `organismo_familias_b4b` bit a bit. Lo que
se mide es **la lectura, no el habla** (casos (Q) y (R) del arnés lo comprueban contra b5 y contra b4b).

---

## 3. LO QUE CAMBIA — **una** perilla, inerte por defecto

### 3.1 `memoria_variante` (default 0)

Con 1, cada celda de pares escribe y lee en

> `(par de píxeles, bin del par, firma de los últimos fam_nvar píxeles)`

o sea **4 × 2^`fam_nvar` = 32** subcasillas por celda en vez de 4. La firma se calcula **de la retina presente**:
sin estado compartido, sin gradiente, sin supervisor, sin azar nuevo, sin señal adicional. Con 0, la dirección es
el bin literal de b5/b4b, la tabla vuelve a tener 4 columnas y **no se consume rng adicional**.

### 3.2 **A la escritura Y a la lectura** — decisión escrita antes de medir, con su razón

La tabla es una memoria **direccionada por contenido**: se lee en la dirección en la que se escribió. Por eso el
sufijo entra en **una sola función**, `_dir_var`, usada en los **tres accesos** (escritura por mensaje, escritura
por mordida, lectura). Las alternativas, y por qué se descartan:

- **(A) Sufijo sólo en la lectura.** El mensaje quedaría escrito en `4·bin` y la boca leería en `8·bin + firma`:
  **ninguna lectura encontraría nunca nada**, la vía lenta abstendría siempre y el organismo sería el lineal de
  v14.1 con pasos de más. No es una variante conservadora: es romper el instrumento. Se descarta por
  contradicción, no por gusto.
- **(B) Lectura en dos niveles** (buscar la subcasilla con sufijo y, si no se conoce, recaer en el bin sin
  sufijo). Si el mensaje escribe también el bin sin sufijo, **reintroduce exactamente la fuga que este bloque
  ataca** (la hermana lee el bin). Si el mensaje escribe sólo la subcasilla con sufijo, hace falta una regla de
  precedencia nueva y dos direcciones por acceso: más maquinaria, contra Occam, y sin control gratis. Queda
  anotada como candidata para otro cuello (cuando la tabla deba generalizar a lo que no ha visto), no para éste.

### 3.3 **Se cruza con `k_ganadoras`** — factorial 2 × 2, y por qué

El sufijo y `k` atacan **fugas distintas**, y el bloque 5 ya midió cuál hace cuál:

| fuga | quién la cierra (predicho) | evidencia previa |
|---|---|---|
| **otro token** (BAR-T) comparte el bin de forma | `k` (más pares de forma) | b5: k = 3 baja BAR-T de 7 a 2 y 4 |
| **la hermana** (BAR-H) es invisible a las celdas de forma | **el sufijo** (mete los px 9–11 en la dirección) | ninguna: es lo que se prueba |

Por eso los brazos son **k ∈ {1, 3} × sufijo ∈ {OFF, ON}**, y no sólo el candidato. El diseño se lee solo:

- `k1v0` es `organismo_familias_b4b` **bit a bit** — el control de Occam, gratis.
- `k3v0` es el `k = 3` del bloque 5 **bit a bit** — la línea base de la que hay que mejorar.
- `k1v1` dice si el sufijo **solo** basta para la hermana (predicción: sí) y si **solo** basta para el token
  (predicción: no).
- `k3v1` es **el brazo que decide**.

k = 5 **no entra**: el bloque 5 lo midió y rompe el cuerpo (muertes 199.5 y 152 contra 32–38). Repetirlo sería
gastar CPU en un brazo ya refutado.

### 3.4 El precio, declarado antes de medir

Con el sufijo, la tabla propia del organismo es **8 veces más dispersa**: cada subcasilla se visita 8 veces menos,
la vía lenta **abstiene más** y releva a la lineal más a menudo. Predigo que eso **no** daña el canal (el mensaje
se escribe y se lee en la misma dirección, en el mismo paso) pero **sí** puede encarecer el cuerpo. Lo vigilan el
gemelo mudo `CORTADO`, las muertes y `okU` en **R6**, que es puerta de seguridad y puede matar al candidato.

### 3.5 Arnés `identidad_familias_b6.py`: **59/59** (§9.0)

Cadena comprobada hasta el tronco con la perilla apagada (b5, b4b, b4, b3, b2, `organismo_familias`,
`organismo_v14`, `organismo_v15f_on`), rng no consumido a T = 120 000, inercia con `memoria_pares=None`,
estructura de la dirección reimplementada **fuera** del organismo y comparada, siete formas de escribir mal la
perilla que **lanzan**, y **cinco controles que DEBEN fallar**.

---

## 4. BRAZOS, EMISOR Y SEMILLAS

### 4.1 Brazos — los nueve del 4b (−) × k ∈ {1, 3} × sufijo ∈ {0, 1} = **36**

| brazo (base) | receptor | qué decide |
|---|---|---|
| `CANAL` | patrón real de `T1v2` + R cruda | que el canal siga vivo |
| `CORTADO` | gemelo **mudo** (recibe la visita, no el mensaje) | la línea base de todo |
| `BAR-H` | patrón de la **hermana** `T1v0` + la misma R | **la pregunta del bloque** |
| `BAR-T` | patrón de **otro token** `T3v2` + la misma R | que lo ganado en b5 siga ganado |
| `VALOR` | patrón de **ceros** + la misma R | que el campo de referencia haga falta |
| `INM` | entrega inmediata | montaje (P-I3) |
| `OTRO` | referente de **otro mundo** | contaminación (excluido de P-I3 por ERR-52) |
| `PAR` / `PAR0` | el receptor ve `T1v2` **y** `T1v0`, con / sin mensaje | especificidad conductual entre hermanas |

Nombres: `CANAL-k3v1`, `BAR-H-k1v0`, … Cada brazo `sen` tiene su gemelo (`CORTADO-kNvM`, o `PAR0-kNvM` para los
brazos PAR) en **la misma celda** del factorial: el prefijo se compara siempre dentro de la celda.

**Sólo la dirección (−)** (ERR-53): *"eso que evitas es COMIDA"*. Es la única dirección donde el receptor no puede
aprenderlo solo (no lo muerde), o sea donde el canal es irreemplazable, y la única con puertas propias.

### 4.2 Semillas y coste

- **Serie 721–740**, **réplica 741–760**, T = 100 000. **701–720 ya las gastó el bloque 5** y **721–740 las gastó
  H-1** (mundo vivo, otro organismo y otro mundo: no hay solapamiento de instrumento, pero se deja dicho).
- Coste por serie: 20 emisores + 36 × 20 = **740 corridas** de 100 000 pasos, más identidad y diagnóstico. El
  `Pool` lo lanza **sólo el coordinador** (regla 3).
- **Humo del creador (§9): un proceso, 2 semillas (1 y 2), T = 30 000, 6 corridas de brazo.** Ninguna semilla de
  las series queda expuesta.

---

## 5. LAS MEDIDAS — **todo por conducta de la boca** (ERR-44)

### 5.1 La convención

`com` = la boca **mordió en la primera exposición de su vida** al referente, después de la entrega. En la
dirección (−) el referente es **comida que el receptor evitaría para siempre**: morder es el efecto del mensaje.
`dist` (brazo PAR) = la boca trató **distinto** a `T1v2` y a `T1v0` en sus primeras exposiciones tras la entrega.
Exposiciones hasta asociar, muertes y `okU` se guardan **al lado**, como coste; no sustituyen a `com`.

### 5.2 Puertas de montaje (si caen, no se lee nada más)

| puerta | criterio |
|---|---|
| **P-I1** | identidad del arnés **59/59** y del subconjunto del runner, con los controles que DEBEN fallar |
| **P-I2** | el emisor voraz anota el referente ciego (`T1v2`, R > 0) en **≥ 18/20**; las semillas sin mensaje se **excluyen** y se reportan (regla 10) |
| **P-I3** | cada brazo `sen` comparte con **su** gemelo de la misma celda el prefijo EXACTO de `log` hasta la entrega, en **≥ 18/20** (OTRO excluido, ERR-52) |
| **P-I4** | *(ver **ERR-70**)* la primera exposición de la VIDA al referente coincide con la entrega; las semillas donde no, se **excluyen** y se reportan; gate **≥ 18/20 utilizables** |
| **P-I5** | en la prueba la boca usa la vía **LENTA** (`fam1 = 0`) en **≥ 18/20**; si el código del referente ya le es familiar, el mensaje queda escrito y no consultado, y esa semilla se reporta aparte |

### 5.3 Diagnósticos — **observados, no prometidos** (no deciden ninguna predicción)

`n_mismo_dir_k` (cuántos de los 32 estímulos caen en **las k DIRECCIONES** del mensaje), `n_mismo_bin_k` (lo
mismo por bin, el del bloque 5), las k ganadoras antes y después del mensaje, `k_var_post` (cuántas de las k usan
un píxel de variante), `mem_cobertura`, `mem_vistas`, `lag_t` / `lag_m`, `wv` (el peso lineal sobre los 3 píxeles
de variante).

### 5.4 Cálculo **estructural** (T = 0, sin simular)

`estructura_v` en el runner, por semilla y antes de simular: en cuántas de las 66 celdas **no** se distingue el
referente de BAR-H, de BAR-T y de VALOR, con y sin sufijo; y el **piso** de la intersección si las k ganadoras son
todas de forma. Predicción estructural: con sufijo, el piso baja de **4** (la familia) a **1** (el referente).

### 5.5 Declaración de contaminación

Todo lo del §9 (humo) se corrió con semillas 1 y 2 y T = 30 000 **después** de fijar §0–§8. El cálculo del §0
sobre el catálogo se hizo antes de escribir las predicciones y se declara arriba con las semillas exactas.

---

## 6. LA LETRA Y LAS PREDICCIONES (escritas antes de correr un solo brazo de la serie)

### 6.1 Umbrales — por celda del factorial, sobre `com`, en **cada** una de las dos series de 20

| # | criterio | pasa | me refuta |
|---|---|---:|---|
| **R1** | el canal sigue intacto | `CANAL ≥ 15/20`, `CORTADO ≤ 5/20`, pareado `≥ 14/20` | cualquiera cae |
| **R2** | otro token (lo ganado en b5) | `BAR-T ≤ CORTADO + 3` | `BAR-T > CORTADO + 3` |
| **R3** | **la hermana — LA QUE DECIDE** | `BAR-H ≤ CORTADO + 5` | `BAR-H > CORTADO + 5` |
| **R4** | hace falta el campo de referencia | `VALOR ≤ CORTADO + 3` | `VALOR > CORTADO + 3` |
| **R5** | especificidad entre hermanas | `dist(PAR) ≥ 12/20` y `≥ dist(PAR0) + 5` | cualquiera cae |
| **R6** | el candidato no cuesta el organismo | mediana muertes `≤ 1.5 × CANAL-k1v0` **y** `okU ≥ okU(CANAL-k1v0) − 0.10` | la razón excede 1.5, o `okU` cae más de 0.10 |

**O-6 — EL OBJETIVO QUE DECIDE EL BLOQUE**, en la celda **`k3v1`** y en **las dos** series:

> `BAR-H ≤ CORTADO + 5` **(hoy 13–16/20: R3 cae ×2)**, con `CANAL ≥ 15/20`, `BAR-T ≤ CORTADO + 3` y
> `dist(PAR) ≥ 12/20` **intactos**.

Nada de esto se recalibra después de ver datos. Un ajuste de umbral, brazo, mecanismo o criterio exige preregistro
nuevo, semillas nuevas y ERR numerado (ERR-71 o posterior).

### 6.2 Predicción numérica, por celda (mediana esperada / rango sobre 20 semillas)

| brazo | `k1v0` (= b4b) | `k3v0` (= b5 k=3) | `k1v1` | **`k3v1`** |
|---|---|---|---|---|
| CANAL | 18 (16–19) | 18 (16–19) | 17 (14–19) | **17 (15–19)** |
| CORTADO | 1 (0–3) | 1 (0–3) | 1 (0–3) | **1 (0–3)** |
| **BAR-H** | 13 (11–16) | 14 (12–17) | **2 (0–5)** | **2 (0–5)** |
| BAR-T | 6 (4–9) | 3 (0–5) | 5 (3–9) | **2 (0–4)** |
| VALOR | 3 (2–5) | 3 (2–5) | 2 (0–5) | **2 (0–4)** |
| PAR `dist` / PAR0 | 18 / 2 | 18 / 1 | 17 / 2 | **17 (15–19) / 1** |
| muertes (mediana) | 35 (28–45) | 38 (30–50) | 45 (30–70) | **45 (30–70)** |
| `n_mismo_dir_k` | 12–16 / 32 | 12–16 / 32 | 2–4 / 32 | **1–3 / 32** |

**Predicción central, en una frase:** *el sufijo tumba a la hermana y no toca lo demás; `k` tumba al otro token y
no toca a la hermana; sólo la celda `k3v1` pasa R1–R5 a la vez, y lo paga con un cuerpo algo más caro pero dentro
de 1.5×.* Dicho como contraste medible: **BAR-H(k3v1) ≤ BAR-H(k3v0) − 8** y **BAR-T(k1v1) − BAR-T(k1v0) ≥ −3**.

### 6.3 Qué me refuta, y qué mido entonces (declarado ahora, no después)

1. **`BAR-H` no baja con el sufijo** (`> CORTADO + 5` en `k3v1`, en cualquiera de las dos series) → **la variante
   no está, para el receptor, en esos 3 píxeles**. Entonces, con los campos que el instrumento ya guarda y sin
   brazos nuevos, se separa entre dos causas:
   - **(i) la tabla no se lee.** Si `fam1 = 1` sube, o `mem_cobertura` cae, o la vía lenta abstiene: la boca no
     está usando la tabla en ese paso; el sufijo no puede actuar porque nadie lo consulta. Se mira `fam1`,
     `mem_cobertura` y `n_mismo_dir_k` (que el arnés ya verificó que excluye a la hermana: caso (G)).
   - **(ii) la tabla se lee y decide la LINEAL.** Si `n_mismo_dir_k` excluye a la hermana y aun así la boca muerde
     ante la hermana, el efecto viaja por `Wps − Wns` sobre la retina, no por la tabla; se mira `wv` (el peso
     lineal sobre los píxeles 9–11). Ese sería el cuello del bloque siguiente, y sería un resultado, no un fallo.
2. **`CANAL < 15/20` en `k3v1`** → la dispersión 8× rompió el canal; el sufijo de 3 bits es demasiado caro y lo
   que toca probar es una firma **más corta** (1 bit) — otro bloque, otro preregistro.
3. **`BAR-T > CORTADO + 3` en `k3v1`** → el sufijo deshizo lo que `k` había ganado; el factorial lo diría al
   comparar con `k3v0`, que corre en la misma serie.
4. **`R6` cae** → el candidato muere por coste, como murió k = 5.
5. **Todo baja a la vez, incluido `CANAL`** → no hay referencia: hay un organismo que dejó de leer la tabla. El
   gemelo `CORTADO` y `k1v0`/`k3v0` en la misma serie lo distinguen.

### 6.4 Lo que predigo que pasará, en una frase

*El mensaje dejará de mover la boca ante la hermana sin dejar de moverla ante el referente, y eso ocurrirá en la
celda con sufijo tanto con k = 1 como con k = 3; sólo con k = 3 se mantendrá además cerrado el otro token.*

---

## 7. LO ÚNICO QUE SE PERMITE CORREGIR

Sin ERR: erratas de texto que no cambien un número, y fallos del runner que impidan **escribir el JSON crudo**
(ERR-54: los datos crudos se guardan **antes** del análisis, y un análisis que se cae no puede tumbar el
registro). Con ERR numerado, fecha, motivo y **semillas nuevas**: cualquier cambio de umbral, brazo, mecanismo,
criterio o puerta. **ERR-70 ya está escrito abajo y se aplica desde la primera serie.**

---

## 8. QUÉ SE PODRÁ DECLARAR, Y QUÉ NO

Si **O-6** y R1–R6 pasan en **las dos** series, se podrá decir **sólo**:

> *Un mensaje (patrón + recompensa) cambió la conducta de la boca de otro organismo sin experiencia propia, y esa
> conducta fue específica frente a **la hermana de variante**, frente a otro token y frente a un valor sin
> referente, en este mundo.*

No autoriza decir lenguaje, comprensión, concepto, símbolo, evolución ni AGI. Si O-6 pasa en una sola serie, se
reporta como no replicado (regla 12) y se pide un tercer rango.

---

## 9. HUMO — resultado (§0–§8 no se tocaron)

### 9.0 Identidad: **59/59** (arnés completo, un proceso, semillas 1–3)

Incluye la cadena hasta `organismo_v14` (TRONCO), el ancla de rng a T = 120 000 con k = 1 y k = 3, y **cinco
controles que DEBEN fallar** — entre ellos `(AA) el patrón de la HERMANA ≠ CANAL con sufijo, k = 3`, que es
exactamente el brazo que decide: sin él, el arnés pasaría por vacuidad.

Comprobación del mecanismo, **estructural y no conductual** (caso (G)): **con sufijo la hermana no comparte nunca
la dirección del referente** (4/4 celdas semilla × k), y el grupo del mensaje cae de 15–16/32 a **1–4/32**.
Diagnóstico honesto al lado: **sin** sufijo la hermana comparte la dirección en 3/4 celdas, no en 4/4 — en una
semilla el top-3 incluyó por azar una celda con píxel de variante (`[1, 11]`) y `k` sola ya la separó. Se deja
dicho para que `BAR-H` de `k3v0` no se lea como si fuera ciego a la variante en el 100 % de las semillas.

### 9.1 Coste declarado del humo (regla 3), **y dónde me paso**

Un proceso, sin `Pool`, semillas **1 y 2** (ninguna de las series), T = 30 000. **Me paso de las 6 corridas de la
regla 3**: son 5 brazos (`CANAL`, `CORTADO`, `BAR-H`, `PAR`, `PAR0`) × 2 celdas (`k3v0`, `k3v1`) × 2 semillas =
**20 corridas** de brazo + 2 emisores + 22 de identidad, 168 s de pared. Se declara en vez de esconderse: el
encargo pide ver `CANAL`, `BAR-H` y `PAR` con sufijo ON y OFF, y los gemelos `CORTADO`/`PAR0` son **obligatorios**
(sin gemelo no hay P-I3 y el brazo no se puede leer). T y semillas sí están dentro (≤ 3 semillas, T ≤ 200 000).

### 9.2 La tabla del humo (n = 2, T = 30 000: **NO es evidencia**)

`com` = mordió en su primera exposición de la vida al referente. Semillas 1 y 2; el emisor avisó en las dos
(`T1v2`, R = +1.0, t = 10 102 y 11 247; tras 1 y 5 exposiciones).

| brazo | `com` k3v0 (s1 · s2) | `com` k3v1 (s1 · s2) | muertes k3v0 → k3v1 | `n_mismo_dir_k` k3v0 → k3v1 |
|---|---|---|---|---|
| CANAL | **1 · 1** | **1 · 1** | 29 · 28 → 8 · 9 | 1 · 1 → 1 · 2 (por BIN 1 · 1 → 4 · 6) |
| CORTADO (mudo) | 0 · 0 | 0 · 0 | 31 · 18 → 7 · 12 | 3 · 1 → 1 · 2 |
| BAR-H (hermana) | 0 · 0 | 0 · 0 | 44 · 17 → 4 · 12 | 5 · 3 → 3 · 1 (por BIN 5 · 3 → 12 · 1) |
| PAR (`dist`) | 1 · 1 | 1 · 1 | 7 · 7 → 11 · 9 | 15 · 1 → 2 · 2 |
| PAR0 (`dist`) | 1 · 0 | 0 · 0 | 20 · 6 → 13 · 10 | 3 · 1 → 3 · 1 |

Montaje: P-I3 **idéntico** en las dos celdas (`CANAL`/`CORTADO` comparten prefijo exacto); la boca leyó la vía
**lenta** en las 20 corridas; cruce `cod0` del emisor contra `escala_codigo` **idéntico campo a campo**;
identidad del subconjunto del runner **22/22** (11 casos × 2 semillas), incluidos **(K)**, **(C)** y **(H)**, que
DEBEN fallar. Coste estimado de una serie: 740 corridas de 100 000 pasos, ~6.6 min de pared con `Pool(14)`.

Estructural (T = 0, semillas 1 y 2): celdas de las 66 que **no** distinguen el referente de la hermana
**0.6818 → 0.0000** con sufijo; de otro token **0.6818 / 0.4242 → sin cambio**; piso de la intersección si el
top-k es todo de forma **4/32 → 1/32**. Píxeles en que difieren referente y hermana: **[9, 11]** (variante =
[9, 10, 11]) en las dos semillas.

### 9.3 Qué dice el humo, sin ajustar nada

1. **El mecanismo hace lo que dice, y eso es estructura, no conducta.** Con sufijo, ninguna de las 66 celdas
   confunde al referente con su hermana (0.0000), el grupo del mensaje cae de 12–16 por bin a 1–3 por dirección, y
   la cobertura de la tabla propia baja de 3.5/4 (88 %) a ~11/32 (34 %): la dilución 8× declarada en §3.4 está
   ahí, medida.
2. **El humo NO reproduce la línea base del bloque 5 y por tanto no puede pre-validar el contraste.** `BAR-H` da
   0/2 también **sin** sufijo, cuando el bloque 5 midió 15/20 y 13/18 a T = 100 000. Con n = 2 y un tercio de los
   pasos eso es ruido: lo digo para que nadie lea la tabla de §9.2 como si el efecto ya estuviera.
3. **Las muertes no se dispararon** con el sufijo (si acaso bajaron), pero a T = 30 000 el organismo apenas ha
   empezado a morir; R6 se juega en la serie, no aquí.

---

## ERR-70 (creador del bloque 6, 18 sep 2026, **antes** de la primera serie; cierra la nota abierta del bloque 5)

El registro del bloque 5 dejó abierto: *"la puerta P-I2 (emisor voraz ≥ 18/20) queda en el borde en cuatro de seis
series; regla 12 la manda replicar o rebajarla con ERR, y se decidirá **antes** de la serie siguiente, no
después."* Se decide aquí:

1. **P-I2 no se rebaja.** El umbral del emisor sigue en **≥ 18/20** y las semillas sin mensaje se excluyen y se
   reportan, como hasta ahora. Pasó en las dos series del bloque 5 (20/20 y 18/20).
2. **La subcondición que sí tumbó al bloque 5 era otra**, y estaba mal formulada: *"el mensaje llega ANTES de que
   el receptor vea el referente"*, exigida en **20/20** (dio 19/20 y 16/20). Eso es **P-I4**, y es una propiedad
   **de cada semilla del montaje**, no del instrumento: que un receptor concreto se cruce con el referente antes
   de la entrega no invalida a las otras 19 semillas, y un todo-o-nada de 20/20 sobre 20 tiradas independientes es
   una puerta que se cae por ruido.
3. **Cambio:** P-I4 pasa de puerta todo-o-nada a **criterio de exclusión por semilla**. Una semilla en la que el
   receptor ya había visto el referente antes de la entrega **se excluye de los conteos pareados y se reporta
   aparte**, exactamente como ya se hace con las semillas sin mensaje (P-I2, regla 10). La puerta queda en
   **≥ 18/20 semillas utilizables**.
4. **Por qué esto es más estricto y no más laxo:** excluir una semilla la saca del numerador **y** del
   denominador de todos los brazos, así que ninguna puede inflar `CANAL`; rebajar el umbral, en cambio, las
   habría dejado contando. El número de semillas excluidas se reporta siempre, y si supera 4/20 el bloque se para
   por montaje.
5. **Alcance:** ningún umbral R1–R6 ni el objetivo O-6 cambian. Se aplica desde la serie 721–740.

---

## 10. SERIES 721–740 y 741–760 — resultado

*(lo rellena el coordinador tras correr; §0–§8 quedan como están)*
