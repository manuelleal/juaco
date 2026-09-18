# PREREGISTRO — BLOQUE 4b: **el emisor que SÍ descubre en la dirección ciega** (ERR-51), y la especificidad entre **hermanas**

**Misión (primero, siempre):** llegar a la AGI por este camino — un organismo mínimo con reglas locales (sin
backprop en el runtime) que aprende, desaprende, generaliza, sobrevive, se reproduce y se **COMUNICA**, con
evidencia preregistrada. Hoy: **que dos células se comuniquen sobre algo que ambas representan — y que la que habla
pueda llegar a saberlo.**

**Autor:** diseñador del bloque 4b. **Fecha de firma:** 18 sep 2026.
**Estado al firmar:** §1–§8 se escribieron **ENTERAS antes de correr un solo brazo de la serie**. Lo corrido al
escribirlas: el **arnés de identidad** (`identidad_familias_b4b.py`, **95/95**) y la **calibración declarada de
`voraz`** (§3.3), las dos sobre **semillas 1–2** y las dos **sobre el instrumento, no sobre una hipótesis del
receptor** — con las **dos excepciones que declaro en §5.4**. §9 (humo) se escribe después y **nada de §1–§8 se toca
al escribirlo**. §10 lo escribe el coordinador con la serie 581–600.

---

## 0. **ERR-51 — el error que este bloque corrige**

**ERR-51 (montaje del emisor; bloque 4, 18 sep 2026): el EMISOR comparte el PUNTO CIEGO del receptor.** El bloque 4
montó la dirección decisiva — *"lo que evitas es comida"* — sobre un emisor que **evita ese estímulo por exactamente
la misma razón que el receptor**: su familia es veneno y la boca sólo lo muerde cuando el azar y el hambre
coinciden (`p ≈ 0.025` con hambre 1, `≈ 3·10⁻⁵` saciado). Resultado medido: **P-I2 cayó en la dirección (−)**, con
**5/20 y 4/20 emisores sin mensaje**, y por §5.2 del bloque 4 **el bloque se paró y nada se declaró en esa
dirección**. El diseño (yo) puso la carga de descubrir en un organismo al que no le dio ninguna forma de descubrir.
El humo del bloque 4 ya lo había señalado (1 de 2) y quedó escrito en su §9.3 punto 1; **la serie lo confirmó**.

**Lo que ERR-51 NO es:** no es un fallo del canal ni del receptor. En las semillas donde **sí** hubo mensaje, el
receptor hizo exactamente lo que el canal prometía (`CANAL− okX` **15/15 y 16/16** contra **0/15 y 0/16** de
CORTADO−). ERR-51 es del **montaje del emisor**, y se corrige dándole al emisor una mecánica local para morder lo
que evita.

**Lo que el bloque 4 sí dejó medido y que aquí NO se vuelve a preguntar** (su letra se conserva, sus umbrales se
**importan**): CANAL+ 16/20 y 18/20 contra CORTADO+ 1/20 y 2/20 · BAR-H+ 15/20 y 18/20, BAR-H− 12/15 y 12/16
(**la referencia llega al nivel de FAMILIA**) · BAR-T+ 8/20 y 6/20, BAR-T− 1/15 y 4/16 · VALOR ≈ CORTADO ·
`comH` 1.0 en CANAL−. **Ganó P-D (la del diseñador); la del coordinador no.**

---

## 1. La pregunta de este bloque, en dos partes

1. **¿Puede el emisor llegar a saber lo que sólo se sabe mordiendo lo que uno evita, sin dejar de ser el mismo
   organismo?** Y, con él, **¿se sostiene la dirección irreemplazable con la puerta P-I2 exigida?**
2. **¿La referencia que el bloque 4 midió a nivel de FAMILIA llega al nivel de VARIANTE?** El bloque 4 no pudo
   responderlo: con `deriva(R) = T/3 + 1` la corrida tiene **tres** fases y no vuelve a la 0, así que tras la
   entrega la única hermana que el receptor vuelve a ver es el **token** (`n_H = 1`) — y el token es la
   discriminación **más fácil** (difiere del referente en un píxel variable; una hermana variante difiere en dos).
   El brazo **PAR** levanta ese límite **sin tocar el canal**.

**H (la que se juzga).** *Con una boca más voraz, el emisor llega a morder lo que evita en ≥ 18/20 semillas, y
entonces el receptor come a la primera, sólo por el mensaje, un alimento que nunca ha visto y que su propia
generalización por familia le decía que era veneno.*

**H¬ (la alternativa, y la mía sobre la parte 2).** *La referencia se queda en la familia.* Con **una** celda
ganadora de **2 bits**, el receptor **no** puede tratar distinto a la excepción y a su hermana: el mensaje cae en la
casilla, y la casilla no separa variantes.

---

## 2. LO QUE NO CAMBIA

**El canal no se toca:** misma mecánica (el bloque de escritura de la tabla de pares **extraído literal de b3**),
mismos tres modos (`sen`, `inm`, `mudo`), mismo mensaje de dos campos (patrón público de 12 píxeles + **R cruda**),
misma entrega por señalamiento, mismo emisor simétrico. **El mundo no cambia:** `corre_familias_b2.BASE` +
`cambio = 10⁹`, `vira = 0`, `n_exc = 2`, `exc_fija = 2`, `fam_val='familia'`, `T = 100 000`; **X⁺ = `T0v2`**
(veneno en familia de comida) y **X⁻ = `T1v2`** (comida en familia de veneno); las otras seis `Tkv2` son el control
balanceado. **La letra del receptor y de los seis controles es la del bloque 4** (`CANAL`, `CORTADO`, `BAR-H`,
`BAR-T`, `VALOR`, `INM`, `OTRO`/R-SIN-SAL), con sus umbrales **importados**, no recopiados.

**Los dos organismos siguen sin verse:** dos `run()` sin visión mutua; la corrida del receptor depende **sólo** de
los cuatro campos del mensaje (arnés, caso J). Sigue sin haber defensa contra la falsa alarma.

---

## 3. LO QUE CAMBIA — dos perillas, las dos inertes por defecto

`construye_familias_b4b.py` construye `organismo_familias_b4b.py` **por anclas** sobre `organismo_familias_b4.py`
(sha `ff9946ee2ffe27e6`, que sólo se lee), con **7 anclas de línea**; si alguna no encaja, aborta sin escribir, y el
texto se compila antes de escribirse.

### 3.1 `voraz` (default 0.0) — la mecánica elegida, y por qué

**Es una constante del propio órgano de la boca, sumada a su variable de decisión:**

```
Vb = alpha*w + hambre_boca*hambre + 0.5 + voraz      (antes: sin el último sumando)
```

**No mira el mundo. No sabe dónde está la excepción. No toca el aprendizaje, ni la energía, ni la vía lenta, ni la
tabla. Consume el MISMO rng** (la misma única `rng.random()` por encuentro). Es el eje *"tímida / voraz"* que las 12
células de la sala 3 nombraron y que el organismo no tenía como perilla. Arnés: con `learn=False`, **todo lo que
depende de los pesos es idéntico para cualquier `voraz`** (caso v).

**Las otras dos opciones del encargo, y por qué las descarto — antes de medir:**

| opción | por qué NO |
|---|---|
| **(a) hambre forzada *en la ventana de la excepción*** | **es un oráculo.** "En la ventana de la excepción" exige saber **dónde y cuándo** está el estímulo que precisamente nadie sabe que es especial. Es la **trampa 4 de la regla 5** ("sitios fijos que se memorizan: el ciego ya sabe") con otro traje. Su versión no oracular — ayuno periódico — toca la **energía**, que entra en `hambre`, en `Rp` y en la actualización de `Wl`: cambia más del organismo que `voraz`, por el mismo efecto. |
| **(b) cadena de dos saltos** | **no resuelve ERR-51, lo traslada.** Si el emisor recibió el aviso de un tercero, alguien tuvo que morderlo primero: el problema de la fuente sigue intacto y P-I2 seguiría cayendo. **Mide otra cosa** —la degradación del mensaje al saltar— y **merece su propio bloque**, encima de éste, no en lugar de éste (§11). |
| **(c) voraz** | **elegida:** un solo número, en el órgano que decide, sin mirar el mundo, sin tocar aprendizaje ni energía, sin alterar el rng, y con un **coste medible y declarado** (veneno mordido y muertes del emisor: el que descubre, paga). |

### 3.2 `par_herm` (default None) — el brazo PAR, sin tocar el canal

`(k, j)`: en la presentación del mundo, el **token** de la familia `k` se sustituye por su **variante `j`**, y esa
variante queda **exenta de la deriva**. Así el receptor ve **dos variantes de la misma familia a la vez** — la
excepción `T1v2` y su hermana `T1v0` — en vez de la excepción y su token. **`len(tipos)` no cambia**, así que el
sorteo de `spawn()` y **el rng del mundo quedan intactos** (arnés, caso y: `val_mundo`, `exc_win`, `herm`, `exc` y
`cod0` idénticos). **Valor del bloque: `par_herm = (1, 0)`**, fijado aquí.

### 3.3 **Calibración declarada de `voraz`** (instrumento, no hipótesis)

`voraz` se eligió **antes** de escribir §6, con **6 corridas de un proceso** en **semillas 1–2** a `T = 40 000` (un
tercio de las oportunidades de la corrida real), probando `0.0, 1.0, 1.5, 2.0`:

| `voraz` | emite X⁻ (s1 / s2) | muertes | veneno mordido |
|---|---|---|---|
| 0.0 | sí / **no** | 7 / 10 | 38 / 29 |
| **1.0** | **sí / sí** | 11 / 14 | 82 / 55 |
| 1.5 | sí / **no** | 25 / 13 | 102 / 110 |
| 2.0 | sí / sí | 23 / 35 | 205 / 271 |

**Se fija `voraz = 1.0`**: el menor de los probados que emite en las dos semillas de calibración con sólo un tercio
de las ventanas, y el de menor coste. (1.5 falla en s2 y 2.0 no es monótono ni barato: con otra `voraz` el flujo del
rng diverge entero, así que estos números son ruidosos — por eso son **calibración**, no medida.)

**Lo digo sin adornos: he elegido `voraz` para que la puerta P-I2 pueda pasar.** Es legítimo porque **P-I2 es una
puerta del montaje, no una hipótesis**, y porque **ninguna predicción del receptor (§6) depende del valor elegido**.
Queda **fijado antes de la serie** y no se vuelve a tocar (§7).

### 3.4 Arnés `identidad_familias_b4b.py`: **95/95**

11 casos de apagado contra `organismo_familias_b4` (×3) + 3 con el **canal encendido en sus tres modos**, 1 de rng
no consumido a T = 120 000, 5 de **cadena completa** (b3, b2, `organismo_familias`, `organismo_v14` TRONCO,
`organismo_v15f_on`), 3 de `voraz` (incluido *"con `learn=False` todo lo que depende de los pesos es idéntico"*), 6
de `par_herm` (rng del mundo intacto, el token sustituido no vuelve a verse, la hermana **no deriva**, y en la fase
de la prueba **conviven** hermana y excepción), 8 del montaje E → R con el emisor voraz (incluidas la puerta P-I3,
*"nunca visto"*, *"el receptor no ve al emisor"* y **"el emisor con `voraz = 0` no siempre llega"**, que es ERR-51
hecho prueba) y **14 controles que DEBEN fallar**. **Sin 95/95 no se corre nada (P-I1).**

---

## 4. BRAZOS Y SEMILLAS

Un emisor **voraz** por semilla, del que salen los dos mensajes. **Los catorce receptores del bloque 4, con su misma
letra**, más **dos nuevos**:

| brazo | qué cambia respecto del bloque 4 |
|---|---|
| **CANAL±, CORTADO±, BAR-H±, BAR-T±, VALOR±, INM±, OTRO±** | nada, salvo que el mensaje viene de un emisor voraz |
| **PAR−** | `= CANAL−` **+ `par_herm = (1,0)`**: el receptor ve la excepción `T1v2` **y su hermana `T1v0`** |
| **PAR0−** | el **gemelo mudo** de PAR− (misma visita del canal, sin mensaje) |

**16 corridas de receptor + 1 de emisor por semilla × 20 = 340 corridas.** **Semillas 581–600**, nuevas; **réplica
601–620** (regla 12). Arnés, calibración y humo: **1, 2, 3**. Ninguna de 581–620 queda expuesta antes de la serie.

---

## 5. LAS MEDIDAS

Las del bloque 4, **importadas** (`evX`, `okX`, `evU`, `okU`, `comH`, `okH`, `esp`, `nunca`, `ret2/ret3`,
`lag_t`/`lag_m`, `fam1`, muertes), sobre `primera_b2` y `primera_b4`. **Todo de la boca, nunca de los pesos
(ERR-44).**

### 5.1 La medida nueva (brazo PAR)

| símbolo | qué es | qué sería "hay referencia de variante" |
|---|---|---|
| **`dist`** ∈ {0,1} | la boca hace **cosas distintas** con la excepción `T1v2` y con su hermana `T1v0` en la **primera exposición de cada una tras la entrega** | **1** |
| **`okP`** | la acción sobre la hermana **acierta** con su valencia real (es veneno: lo correcto es no morderla) | **1** |
| **`lag_par`** | **mordidas** entre la entrega y la exposición a la hermana | **covariable obligatoria** |

**`lag_par` decide cómo se lee `dist`, y lo digo antes:** si la hermana se encuentra muchas mordidas después de la
entrega, el mensaje **ya se había borrado** (el bloque 4 midió `ret3` ≤ 8/20 esperado) y entonces `dist = 1` **no
mide especificidad, mide olvido**. Se reporta siempre, y el gemelo PAR0− da la tasa de `dist` **sin mensaje**.

### 5.2 Puertas (si caen, no se lee nada más)

- **P-I1:** arnés **95/95** y su subconjunto en el runner; shas exactos; cruce de `cod0` del **emisor** campo a campo.
- **P-I2 — LA PUERTA DE ESTE BLOQUE, con la mecánica nueva:** el emisor anota el referente de la dirección en
  **≥ 18/20**, con la R cruda del signo que le toca, y `t_msg < 2·deriva(R)` en todas. Es el umbral **exacto** que
  cayó en el bloque 4 (5/20 y 4/20 sin mensaje); si vuelve a caer, **`voraz` no resuelve ERR-51** y se dice así.
- **P-I3 (gemelo):** cada brazo `sen` comparte con su gemelo (`CORTADO±`; **`PAR0−` para PAR−**) el prefijo exacto
  de `log` hasta la entrega, en **≥ 18/20**; INM hasta `t_msg`.
- **P-I4 (nunca visto):** la primera exposición de la vida al referente coincide con la entrega, en **20/20**.
- **P-I5 (por qué vía se lee):** la boca usa la **vía lenta** (`fam1 = 0`) en **≥ 18/20**.

### 5.3 Diagnósticos — observados, no prometidos

`canal_gan_pre`/`canal_gan_post`, `gan_var` (si la ganadora usa un píxel **variable**), `canal_bin`,
`n_mismo_bin`; y del emisor: **veneno mordido y muertes con `voraz` contra `voraz = 0`** — el precio de ser el que
descubre. Alias estructural por semilla, covariable declarada.

### 5.4 **Declaración de contaminación**

El arnés y la calibración, corridos **antes** de escribir esto, me enseñaron dos cosas en **las semillas 1–2**:

1. **`voraz = 1.0` hace que el emisor anote X⁻ en las dos** (T = 60 000), pagando muertes 23 y 17 (contra 15 y 14
   con `voraz = 0`) y veneno mordido 122 y 70 (contra 56 y 40). **Por eso P-I2 no es una predicción ciega: es una
   puerta que he calibrado**, y así se reporta.
2. **El brazo PAR, en n = 2:** semilla 1 → la boca **sí** trató distinto a `T1v2` (la comió, `+1`) y a `T1v0` (no la
   comió, `−3`), pero la hermana llegó **9 mordidas después** de la entrega; semilla 2 → **no** los trató distinto
   (comió las dos), con la hermana **17 mordidas después**. **Por eso P-11 se declara CONTAMINADA** y su covariable
   `lag_par` va escrita **antes** en §5.1.

**Lo que sigue ciego, y es lo que cuenta:** `evX`/`okX` de **todos** los brazos de la serie, `evU`/`okU`, `comH`,
`esp`, `ret2`/`ret3`, `nunca`, las muertes del receptor, los seis controles en las dos direcciones, y el número de
P-11 en 20 semillas con su `lag_par`.

---

## 6. PREDICCIONES (escritas antes de correr un solo brazo de la serie)

| # | qué pregunta | PASA | REFUTA | mi predicción |
|---|---|---|---|---|
| **P-I2** *(puerta, calibrada)* | ¿el emisor voraz descubre? | ≥ **18/20** en las dos direcciones | < 18/20 en (−) | **pasa**; si no, `voraz` no resuelve ERR-51 |
| **P-C** *(la del coordinador, la misma letra del bloque 4)* | ¿el canal mueve la boca del receptor? | **CANAL− `okX` ≥ 15/20** contra **CORTADO− ≤ 5/20**; y **CANAL+ `evX` ≥ 15/20** contra **CORTADO+ ≤ 5/20** | CANAL ≤ 10/20 o CORTADO ≥ 10/20 | **pasa en las dos**: en el bloque 4 ya salió 15/15 y 16/16 donde hubo mensaje; aquí la novedad es que **haya** mensaje en ≥ 18/20 |
| **P-2** | ¿qué hace el receptor sin mensaje? | CORTADO+ ≤ 5/20 (muerde el veneno) **y** CORTADO− ≥ 15/20 (evita la comida) | CORTADO− ≤ 10/20 | **pasa** |
| **P-11** *(brazo PAR; declarada contaminada, §5.4)* | ¿la referencia llega a la **variante**? | `dist` **≤ 8/20** | `dist` ≥ 15/20 | **pasa**: con **una** ganadora de **2 bits** la casilla no separa hermanas. Si refuta, la lectura del bloque 4 cambia y lo diré |
| **P-4** *(se REPORTA, no refuta)* | BAR-H | — | — | **≈ CANAL**, como en el bloque 4 (15/20, 18/20 y 12/15, 12/16). Se declara como **"referencia de FAMILIA"**, no como refutación del canal |
| **P-5** | BAR-T | \|BAR-T − CORTADO\| ≤ 3/20 | \|BAR-T − CANAL\| ≤ 3/20 | **pasa** (en el bloque 4: 8/20, 6/20 y 1/15, 4/16 — ya se separaba de CANAL) |
| **P-6** | VALOR-SOLO | \|VALOR − CORTADO\| ≤ 3/20 | \|VALOR − CANAL\| ≤ 3/20 | **pasa** (en el bloque 4: ≈ CORTADO) |
| **P-7** | INM contra señalamiento | \|INM − CORTADO\| ≤ 5/20 | \|INM − CANAL\| ≤ 3/20 | **pasa** |
| **P-8** | OTRO (R-SIN-SAL) y el colateral del relevo | \|OTRO − CORTADO\| ≤ 3/20 **y** `okU` y muertes no peores que CORTADO en ≥ 15/20 | \|OTRO − CANAL\| ≤ 3/20 | **pasa en el referente**; el colateral **no lo sé** |
| **P-9** | ¿cuánto dura? | `ret3` ≤ 8/20 | ≥ 15/20 | **pasa** |
| **P-10** | ¿sirve para vivir? | muertes(CANAL) < muertes(CORTADO) pareado ≥ 14/20 | ≥ en ≥ 14/20 | **en (−) no sé** (el mensaje **añade** una fuente de comida); **en (+) refuta** |
| **P-12** *(coste del que descubre; diagnóstico con umbral)* | ¿qué paga el emisor voraz? | — | — | muertes(E, `voraz`=1.0) **>** muertes(E, `voraz`=0) en ≥ 14/20: **descubrir cuesta**, y se reporta en vidas, no en adjetivos |

`comH` **se reporta, no es puerta** (bloque 4: 1.0 en CANAL−, sobre **una** sola hermana — el token; por eso existe
PAR). Zonas intermedias declaradas vacías, como en el bloque 4.

**Predicción global.** *El emisor voraz cierra ERR-51 y la dirección irreemplazable queda medida con su puerta: el
receptor come a la primera, sólo por el mensaje, un alimento que nunca ha visto. Y la referencia sigue siendo de
FAMILIA, no de variante: el brazo PAR no separa a la excepción de su hermana.* Si acierto, la frase del bloque es
***"el canal transmite valor con referencia de familia, y para bajar a la variante hace falta un receptor con más de
una celda ganadora"*** — que es, otra vez, el cuello que el bloque 3 dejó abierto.

**Si me equivoco y `dist` ≥ 15/20**, la referencia sí llega a la variante, y lo diré con esas palabras — pero sólo
si `lag_par` es bajo; con `lag_par` alto, `dist` mide olvido y el bloque lo dirá así (§5.1, escrito antes).

---

## 7. LO ÚNICO QUE SE PERMITE CORREGIR

**Nada.** Este preregistro **no reserva ninguna corrección**. Si **P-I2 vuelve a caer**, el bloque **se para** y el
resultado es *"`voraz` no resuelve ERR-51"* — no se sube `voraz`, no se alarga `T`, no se cambia el mundo. Si P-I3 o
P-I4 caen, es el instrumento y se para. `voraz = 1.0` y `par_herm = (1,0)` quedan **fijados** por §3.3 y §3.2 y no
se tocan. Cualquier otra mecánica de emisor (ayuno, cadena de dos saltos, varios emisores) es **otro bloque con
preregistro nuevo**.

---

## 8. QUÉ SE PODRÁ DECLARAR, Y QUÉ NO

**No se declara** (reglas 6 y 8): *"lenguaje"*, *"palabra"*, *"símbolo"*, *"entiende"*, *"significado"*,
*"representa"*, ni *"comunicación"* a secas.

**Se podrá declarar, literalmente:**
- si **P-I2 y P-C pasan en (−)**: *"con una boca más voraz, un organismo llega a morder lo que evitaba y puede
  decirlo; y el que escucha come a la primera, sin haberlo probado nunca, un alimento que su propia generalización
  por familia le decía que era veneno y que solo no habría mordido."*
- si **P-12 se cumple**: *"y el que descubre lo paga en vidas."*
- si **P-11 pasa con `lag_par` bajo**: *"y la referencia se queda en la familia: el receptor no trata distinto a la
  excepción y a su hermana."*
- si **P-11 refuta con `lag_par` bajo**: *"y la referencia baja hasta la variante."*
- si **P-I2 cae otra vez**: *"la voracidad no basta: en este mundo, el que podría avisar de que lo evitado es
  comida tampoco llega a saberlo."*

**Qué no puedo hacer, declarado antes:**
1. No puedo separar *"la referencia se queda en la familia"* de *"se queda en la familia **con una sola ganadora de
   2 bits**"*. Hace falta **varias ganadoras** o un **nodo por código y retina**: otro candidato, otro preregistro.
2. `voraz` **no es un descubrimiento del organismo**: es una constante que yo le pongo. Este bloque **no** explica
   de dónde saldría esa voracidad; sólo mide qué pasa si la hay y qué cuesta. Que la voracidad **evolucione** es el
   bloque siguiente (§11), no éste.
3. Sigue sin haber defensa contra la falsa alarma (el receptor no ve al emisor).
4. Con 20 semillas no cierro nada: la réplica 601–620 es obligatoria (regla 12).

---

## 9. HUMO — resultado (§1–§8 no se tocaron)

### 9.0 Identidad: **95/95** (§3.4). Subconjunto del runner: **18/18** (9 casos × 2 semillas), incluido **(K), que DEBE fallar**, **(v)** `voraz=0.0` ≡ b4 bit a bit y **(p)** `par_herm` sin tocar el rng del mundo.

### 9.1 Coste declarado del humo (regla 3), y **dónde me paso**

**10 corridas de un proceso**, T = 100 000, semillas 1–2: **2 emisores** + **CANAL−**×2 + **CORTADO−**×2 (los 6 que
pide el encargo) **+ PAR−×2 + PAR0−×2**. **Son 10, no 6, y lo digo en vez de esconderlo:** el brazo PAR es nuevo,
cambia el mundo del receptor, y **sin su gemelo `PAR0−` la medida `dist` no está definida** (es el mismo fallo que
el humo del bloque 2 cazó). Preferí pasarme y declararlo a llevar a la serie un brazo nuevo sin humo. A esto se
suman las **6 corridas de calibración** de §3.3, a T = 40 000, ya declaradas allí.

### 9.2 La tabla del humo (n = 2: **NO es evidencia**)

`familias_b4b_humo_20260918_180624.json`, sha16 `8ea2820bdf270b26`. Cruce de `cod0` del emisor contra
`escala_codigo`: **idéntico campo a campo**. **8.0 s/corrida** → la serie (340 corridas) ≈ **3.2 min con
`Pool(14)`**.

**EMISOR VORAZ** (`voraz = 1.0`): anota **las dos** excepciones en **las dos semillas** — X⁺ en `t = 10 101` /
`10 078` y **X⁻ en `t = 10 102` (1.ª exposición) y `t = 11 247` (5.ª)**. En el bloque 4, con `voraz = 0`, la
semilla 2 **no llegaba a emitir en (−) en 100 000 pasos**.

| brazo · semilla | `evX` | `okX` | `ret2`/`ret3` | `mord_ref` | `evU` | `okU` | `comH` | muertes | ganadora (pre → post) | casilla | mismo bin | `dist` / `okP` / `lag_par` |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| **CANAL−** s1 | **0.0** | **1.0** | 0.0 / 0.0 | 8 | 0.333 | 0.833 | 1.0 | 19 | (2,4) → (1,2) | 0 | 16/32 | — |
| **CANAL−** s2 | **0.0** | **1.0** | 1.0 / 1.0 | 1 | 0.167 | 0.667 | 0.0 | 33 | (1,5) → **(5,9)** *(variable)* | 2 | 12/32 | — |
| CORTADO− s1 | 1.0 | 0.0 | 1.0 / 1.0 | 1 | 0.333 | 0.833 | 0.0 | 19 | (2,4) → (2,4) | 0 | 16/32 | — |
| CORTADO− s2 | 1.0 | 0.0 | 1.0 / 1.0 | 3 | 0.500 | 1.000 | 0.0 | 26 | (1,5) → (1,5) | 2 | 12/32 | — |
| **PAR−** s1 | 0.0 | 1.0 | 0.0 / 0.0 | 202 | 0.167 | 0.667 | 1.0 | 21 | **(4,11)** *(variable)* | 1 | **6/32** | **0.0** / 0.0 / 10 |
| **PAR−** s2 | 0.0 | 1.0 | 0.0 / 0.0 | 266 | 0.667 | 0.500 | 1.0 | 21 | (1,5) → (1,5) | 2 | 12/32 | **0.0** / 0.0 / 19 |
| PAR0− s1 *(gemelo)* | **0.0** | 1.0 | 0.0 / 0.0 | 202 | 0.167 | 0.667 | 1.0 | 21 | (4,11) *(variable)* | 1 | 6/32 | 0.0 / 0.0 / 10 |
| PAR0− s2 *(gemelo)* | 1.0 | 0.0 | 1.0 / 1.0 | 3 | 0.667 | 0.833 | 0.0 | 22 | (1,5) → (1,5) | 2 | 12/32 | 0.0 / **1.0** / 32 |

Prefijos hasta la entrega, idénticos en cada pareja (CANAL−/CORTADO− y PAR−/PAR0−) en las dos semillas → **P-I3 se
cumple también con el brazo nuevo**.

### 9.3 Qué dice el humo, sin ajustar nada

1. **`voraz = 1.0` hace hablar al emisor en la dirección ciega en 2 de 2**, y en la semilla donde el bloque 4 se
   quedaba mudo. P-I2 con 20 semillas dirá si llega a 18/20; con n = 2 no lo sé, pero la dirección es la correcta y
   el precio ya está medido en §3.3 (muertes 11–14 contra 7–10; veneno mordido 55–82 contra 29–38).
2. **La dirección decisiva vuelve a salir limpia:** `okX` **1.0 en los dos CANAL−** contra **0.0 en los dos
   CORTADO−**, con la boca leyendo por la **vía lenta** en los cuatro.
3. **P-11 apunta a cumplirse, y por el mecanismo que escribí: `dist = 0.0` en las dos semillas.** El receptor **no
   trata distinto** a la excepción y a su hermana; se come a las dos (`okP = 0.0`), incluida la que es veneno. La
   covariable manda, y la digo: `lag_par` = **10 y 19 mordidas**, así que parte de esto puede ser olvido y no falta
   de especificidad — exactamente el aviso que §5.1 dejó escrito antes.
4. **El hallazgo que no esperaba, y que es del brazo PAR: cambiar el mundo cambia la ganadora, y con ella la
   necesidad del canal.** En la semilla 1 con `par_herm`, la celda ganadora pasa a ser **(4, 11)** — **11 es un
   píxel variable** — y sólo **6 de 32** estímulos comparten la casilla del referente. Con esa resolución el
   receptor **ya lee bien la excepción sin ningún mensaje**: su gemelo mudo `PAR0−` también la come (`evX = 0.0`).
   Es ERR-32 otra vez, y por el lado incómodo: **donde el código tiene resolución suficiente para que el mensaje
   fuera específico, el receptor ya no necesita el mensaje.** Con n = 1 no es evidencia; con 20 semillas y su
   gemelo, es una medida. Y es la razón por la que PAR− se compara contra **PAR0−** y no contra CORTADO−.
5. **`mord_ref` 202 y 266 en PAR contra 1–8 en CANAL−:** sustituir el token por una hermana cambia mucho más que la
   medida de especificidad. Se reporta como covariable; **no** se usa para nada más.
6. **Coste:** 8.0 s/corrida; la serie completa, 340 corridas, ≈ 3.2 min con `Pool(14)`.

**Lo que esto cambia para la serie: nada de §1–§8.** P-11 sigue con su umbral (≤ 8/20) y su covariable escritos
antes; el punto 4 no es una predicción nueva, es un **diagnóstico** que el gemelo `PAR0−` ya estaba puesto para
medir.

## 10. SERIE 581–600 — resultado

*(Vacío al firmar. Lo escribe el coordinador cuando lance el `Pool`.)*

---

## 11. SIGUIENTE — dos bloques que este preregistro deja preparados, **sin medir**

- **4c, la cadena de dos saltos** (la opción (b) que descarté en §3.1, ahora en su sitio): con la fuente resuelta
  por `voraz`, un tercer organismo recibe el mensaje de R y lo retransmite. **Mide la degradación**: ¿sobrevive el
  valor a un salto? ¿y la referencia de familia? Control obligatorio: el tercero **sin** haber visto nunca el
  referente, y el gemelo mudo en cada salto.
- **El origen de la voracidad.** `voraz` es hoy una constante impuesta. Si el mundo tiene excepciones que sólo se
  descubren mordiendo lo que se evita, **una población con `voraz` heredable debería separarse**: los voraces pagan
  en vidas y descubren; los tímidos viven más y no descubren nada — salvo que **haya canal**, y entonces los
  tímidos se aprovechan. **Eso sí sería comunicación con presión de selección**, y es el puente natural entre esta
  línea y la del mundo vivo.
- **Bloque 5 (la palabra)** sigue donde lo dejó el bloque 4 §11, y sigue **bloqueado por lo mismo**: con una celda
  ganadora de 2 bits no caben 8 palabras.
