# PREREGISTRO — FASE 9, BLOQUE 2: "leer llena la memoria; morder abre la puerta" + F9-4bis (J balanceado)

**Misión (primero, siempre): llegar a la AGI por este camino** — organismo mínimo, reglas locales, sin
retropropagación, peldaños preregistrados con controles y réplicas.

**Escrito ANTES del humo y antes de ver un solo número de semillas nuevas** (21-sep-2026, noche; diseñador
del paquete, por decisión del coordinador delegada por el director a las 19:50). Origen: junta del 21-sep
(`experimentos/junta_20260921/SINTESIS.md`, Q3), propuesta del creador C §2–§3 y del creador A §4.
**Semillas NUEVAS: 1581–1600 (serie) y 1601–1620 (réplica, regla 12).** Verificadas libres: `grep` sobre
`*.py` y `*.md` de `experimentos/`, `registro/` y `organismo/` sólo devuelve la reserva del propio creador C
(`junta_20260921/C/PROPUESTA.md` §3), y el barrido de los 562 JSON de `datos/` (claves `seed*`/`sem*`/
`desde*`) da **máximo 2080** y **cero apariciones** en 1581–1620.

**Nada del bloque 1 se rejuzga** (regla 3). Las series 1501–1520, 1521–1540 y 1621–1640 quedan como están.

---

## 0. ERR-93 — dos cambios de letra, numerados al escribirlos (regla 11 de EQUIPO)

**ERR-93 (a): `F9-4` puntuaba al control con un acierto SIN BALANCEAR.** La letra pedía
`p1(REL_BAR) ≤ p1(NADA) + 0.15`. `p1` es una tasa de un solo lado (rechazar lo malo) y **sube gratis si el
cuerpo muerde menos**; el propio preregistro del bloque 1 lo escribió en su §6 ("trampa 2") y luego aplicó la
cautela **sólo al candidato**. El nodo barajado conserva las marginales y produce **cautela genérica**: en las
tres series `p1(REL_BAR)` subió a 0.568 / 0.55 / 0.544 **mientras `c1` se hundía a 0.598 / 0.60 / 0.587**.
La letra midió *"¿rechaza veneno?"* cuando quería medir *"¿sabe cuál?"*.
**Letra nueva, `F9-4bis`, con el índice balanceado de Youden, POR CORRIDA (no J de medianas):**

```
J = p1 + c1 − 1        (J = 0 en las DOS políticas degeneradas: morder todo y no morder nada)
```

`F9-4` original **no se rejuzga** y se reporta como cayó. `F9-4bis` sólo se aplica a **semillas nuevas**.

**ERR-93 (b): el rango del ancla `F9-1` se recalibra con TODAS las series existentes** (continúa la regla
derivada de ERR-92). Regla **declarada aquí, antes de correr**: para cada cláusula del ancla, el rango nuevo
es `[0.75 × mín, 1.25 × máx]` sobre todas las series medidas de esa cantidad (aditivo, `±0.25 × recorrido`,
si la cantidad cruza el cero), **unido** al rango vigente — es decir, **nunca se estrecha** lo que ya se
declaró y se superó. Las cinco series (H-1 ×2, fase 9 ×3):

| cantidad | 5 series | `[0.75·mín, 1.25·máx]` | rango vigente | **rango nuevo (unión)** |
|---|---|---|---|---|
| vida(NADA) | 125, 119, 94.0, 88.5, 95.5 | [66.4, 156.3] | [70, 170] | **[66, 170]** |
| R₀(NADA) | 0.148, 0.140, 0.141, 0.130, 0.142 | [0.0975, 0.185] | [0.10, 0.22] | **[0.097, 0.22]** |
| R₀(RENACE) | 1.03, 0.96, 0.804, 1.0, 0.92 | [0.603, 1.288] | [0.70, 1.40] | **[0.60, 1.40]** |
| r(RENACE) | +3, −2, −15.5, +1.0, −5.0 | [−20.1, +7.6] | [−50, +25] | **[−50, +25]** |

**Lo que refuta la enmienda:** `vida(NADA) < 66` o `R₀(NADA) < 0.097` → el instrumento **sí** se movió, se
para y se abre ERR nuevo.

**ERR-93 (c), declarado: `F9-7` no es puerta de este bloque.** Cayó en las **tres** series del bloque 1
(A₁₂ 0.426 / 0.53 / 0.626; contraste interno 9/20, 7/20, 5/20). Queda **refutada** —*conectarse tarde no
cuesta*— y el brazo `REL_TARDE` no se corre. Se dice en el log y no se rejuzga.

---

## 1. Hipótesis

**H-F9B′ (creador C, tras refutar su propia hipótesis con su humo).** La puerta de v14 **sustituye, no suma**:
cuando la lectura del nodo cuenta como evidencia del código exacto (`nodo_via=1`), la boca abandona el −3 bien
aprendido de la vía lenta por el −1 a medio hacer de la rápida, come más y **se muere el triple de rápido**
(vida 0.38×, J 0.96 → 0.74, medido en `datos/humo/f9b_humo_20260921_160425.json`).
**Si el mensaje llena la vía rápida SIN tocar la evidencia (`nodo_via=2`), la puerta sigue abriéndose sólo con
las mordidas propias del cuerpo; cuando se abre, la vía rápida ya trae los casos del linaje.**

**H-A (creador A).** Con H-1 en pie (mejor R₀ 0.494), la pregunta que falta no es *qué* heredar sino *si el
mundo lo permite*: un **nodo oráculo** (la tabla verdadera) es la **cota superior** de cualquier herencia por
lectura. **Si ni el oráculo cruza R₀ 0.9, el muro es el mundo y no la herencia.**

**Memoria nueva: CERO estructuras.** `nodo_via=2` es `nodo_via=1` menos dos líneas. El oráculo se arma de
`PAT` y `_EF` (que ya existían) y se tira. `sesgo_fijo` es una constante escalar del mismo mecanismo que el
brazo `CONST` de C-P1. `f9c` sólo añade dos contadores de lectura.

---

## 2. Instrumento y anclas

**`organismo_f9c.py`** (`9dd1fb91ecec35ae`; la primera version, `f40336f05a787be8`, se corrigio tras el humo: ver §9), construido POR ANCLAS (**9 inserciones**) por
**`construye_f9c.py`** desde **`organismo_f9.py` (`3a821884394d66c9`)** incorporando las inserciones de
**`organismo_f9b.py` (`6a57e9fa9514099b`, del creador C)**; los dos **sólo se leen**. Cadena verificada por
sha en el constructor: `organismo_alma2` (`4fd616aeaf535e61`) ← `organismo_alma` (`7c09cec391daa879`) ←
`organismo_vivo_h1` (`9e99ff87b5e2db1e`) ← `organismo_vivo_rep2` (`96feb4918dc5d694`) ←
`organismo_vivo_rep` (`aa823d56c2d4213c`) ← `organismo_vivo` (`20c0961c79de8825`) ← **TRONCO CONGELADO
`organismo/organismo_v14.py` v14.1 (`feefc88b1fd8d434`)**. 540 → 584 líneas. Ningún archivo existente se toca
(regla 1); todo lo nuevo vive en `experimentos/nivel09_cuerpo_nuevo_b2/`.

| perilla | qué hace |
|---|---|
| **`nodo_via=0`** | **ancla: `organismo_f9` BIT A BIT** en los nueve brazos del bloque 1 |
| **`nodo_via=1`** | **ancla: `organismo_f9b` BIT A BIT** — el mensaje entra también por la vía rápida y **cuenta como evidencia** (`ncod += 1`): la puerta se abre **al nacer**. Es el fallo ya medido; se corre para que quede en el registro |
| **`nodo_via=2`** | **EL CANDIDATO.** El mensaje entra por la vía rápida y **no toca `ncod`**. La puerta sigue exigiendo `puerta_pat = 5` mordidas **propias** del código exacto |
| **`nodo_or=1`** | **NODO ORÁCULO** (cota superior). El contenido leído no es lo que vivió el linaje sino la **tabla verdadera** (patrón, necesidad) → R: pool de `8 × nodo_lee = 400` mensajes (**cincuenta copias exactas** de la tabla) del que el recién nacido lee `nodo_lee = 50` **por la misma regla de relevancia que todos los demás brazos** — mismo canal, **mismo presupuesto**, mejor contenido (§9). El nodo real sigue haciendo falta para que haya lectura (el primer cuerpo funda vacío, como todos) |
| **`sesgo_fijo=c`** | **CAUTELA**: empujón constante en la boca, `Vb += c`, **sin información** (el mecanismo del brazo `CONST` de C-P1, tal como quedó en `organismo_v15_dE5`) |
| **`f9c=1`** | SOLO LECTURA: `pa`/`pn` = encuentros con la puerta de v14 **abierta** / encuentros. Es el testigo de *"morder abre la puerta"* |

**Lo que la lectura NO hace (declarado, el cambio es UNO):** no divide celdas, no toca el predictor de ΔE
(`Wpe`/`Wke`/`_sbE`), ni la energía, ni los objetos, ni la posición, **ni el rng del mundo** (el constructor
lo comprueba con dos regex sobre lo insertado; el arnés con los casos H e I).

### Arnés de identidad: **109/109** (`identidad_f9c.py`, salida completa en `identidad_f9c_salida.txt`)
(A) apagadas ≡ `organismo_f9` bit a bit, 9 brazos × 2 `rep_acum` × 2 semillas · (B) cadena ≡ **TRONCO v14.1**
en 3 escenarios × 2 semillas · (C) **`nodo_via=1` ≡ `organismo_f9b` bit a bit** en 5 brazos × 2 semillas
(salvo `pa`/`pn`, declaradas de solo lectura) · (D) la maestra apaga las cuatro perillas con `alma=None` ·
(E) ninguna clave nueva con todo apagado · (F) **nueve controles que DEBEN diferir**: REL2b≠REL, REL2b≠REL2,
REL2b_BAR≠REL2b, CAUTELA≠NADA, DOSIS≠REL, ORACULO≠REL2b, ORACULO≠REL, REL2≠REL, `rep_acum` 1≠0 en REL2b ·
(G) el mecanismo medido: `fam_nac = 0` en **todos** los nacimientos con `nodo_via=2` y > 0 con `nodo_via=1`;
`via_msg` idéntico en la primera lectura; `pa > 0` · (H) antes de la primera lectura `via=2 ≡ via=0` · (I) si
nadie lee, `via=2` y `nodo_or=1` ≡ apagado a T completo · (J) el oráculo converge a la **fila exacta** de su
necesidad · (K) `f9c` es solo lectura · (L) `sesgo_fijo=0 ≡ NADA` y `sesgo_fijo<0` muerde estrictamente menos
· (M) guardias · (N) determinismo.

**Dos casos del arnés que fallaron en su primera versión, declarados (ninguno era del instrumento):**
(1) G3 exigía `via_msg` igual a T completo entre `via=1` y `via=2`: **está mal escrito**, las dos trayectorias
divergen desde la primera lectura; la identidad exacta es la **primera** lectura y así quedó. (2) J exigía
`W_lenta` ≈ (+1, −3) en la fila de hambre: el recién nacido puede tener activa la **sed**, y con una sola
lectura de 48 mensajes la fila no satura; se reescribió como "con `nodo_lee = 400` converge a la fila exacta
de **su** necesidad" (hambre A=+1, B=−3, C=D=0 **o** sed C=+1, D=−3, A=B=0).

**Regla 14.** `corre_bloque2.py` **reutiliza** `corre_f9.CUERPO`, `corre_f9.NODO` y `corre_f9.curita_f`, y
`regla14()` compara **campo a campo** las ocho celdas heredadas contra `corre_f9.BRAZOS` antes de correr nada
(aborta si algo difiere aparte de las perillas nuevas apagadas). También reutiliza `corre_f9.resumen`, de modo
que R₀, vidas y la contabilidad H1-8 son **las mismas funciones**, no copias.

---

## 3. Brazos y semillas

**Cuerpo común:** idéntico al del bloque 1 (`CUELLO_MIN` + `MED2` + `h1=1` + `muerte_real=1` + `dote=0.6` +
`rep_X=500`, `rep_umbral=1.0`, `rep_coste=0`, `rep2_regalo=600`, `nodo_k=20`, `nodo_lee=50`, alma nula).

| brazo | perillas | papel |
|---|---|---|
| **RENACE** | `muerte_real=0` | ancla: el inmortal subsidiado |
| **NADA** | `nodo=0, conectado=0` | línea base (= NADA_CM de H-1) |
| **M1** | `hereda='M1'`, `nodo=0` | la mejor herencia de H-1 |
| **REC** | `nodo_rel=0` | recencia (para F9-5) |
| **REL** | `nodo_rel=1, nodo_via=0` | el candidato del bloque 1 |
| **REL2b** | `+ nodo_via=2` | **EL CANDIDATO DE HOY** |
| **REL2** | `+ nodo_via=1` | el fallo ya medido (queda en el registro) |
| **REL2b_BAR** | `nodo_via=2, nodo_baraja=1` | contenido del candidato |
| **REL_BAR** | `nodo_baraja=1` | contenido (F9-4bis) |
| **CAUTELA** | `nodo=0, conectado=0, sesgo_fijo=c*` | cautela genérica **sin nodo** (F9-4bis) |
| **DOSIS** | REL con `eta_s = 0.30` | control que puede fallar (B2-3) |
| **ORACULO** | `nodo_via=2, nodo_or=1` | cota superior (B2-5) |
| **REL_FIJO** | `nodo_rel=3` | ranking congelado (F9-10) |
| **REL_AZAR** | `nodo_rel=2` | control de acceso (F9-6) |

**Nota de diseño declarada:** el encargo listaba once brazos, pero las puertas heredadas F9-5, F9-6 y F9-10
**no se pueden juzgar** sin `REC`, `REL_AZAR` y `REL_FIJO`; se añaden los tres (si no, esas tres puertas
habría que retirarlas, y retirarlas es peor). `REL_TARDE` se retira por ERR-93 (c).
**Factorial: 14 brazos × 2 niveles de `rep_acum` × 20 semillas = 560 corridas** de T = 100 000 por serie.
`rep_acum` es la **perilla del mundo**: el veredicto del mecanismo se lee **dentro** de cada nivel.

**Semillas 1581–1600**, réplica **1601–1620**.

---

## 4. Medidas

Las del bloque 1 (mismas funciones: `R₀ = desc/(muertes+1)`, `r`, vida mediana, `p1`, `c1`, `sac_frac`,
`t_ok`, `exposiciones[A]`, `frac_fund`, contabilidad H1-8) **más**:

- **`J = p1 + c1 − 1` por corrida** (F9-4bis). No se lee `p1` solo, nunca.
- **`via_msg`** — mensajes absorbidos por la vía rápida (0 = perilla inerte, ERR-38).
- **`fam_nac`** — de los 4 estímulos, cuántos le son familiares al recién nacido **justo después de leer**
  (0…4). **Predicción escrita: 0 en todos los nacimientos con `nodo_via=2`** (leer no abre la puerta) y
  **> 0 con `nodo_via=1`**. Es la prueba directa del mecanismo, no un supuesto.
- **`pa/pn`** — encuentros con la puerta de v14 abierta / encuentros. **`pa > 0` con `nodo_via=2`** es la
  prueba de que morder **sí** la abre (y de que la perilla no es inerte de hecho).

**Estadística (ERR-37/61).** R₀, r, vidas, fracciones y `J` son integrales de trayectoria → **A₁₂ sin
parear**, medianas y cuartiles. `J` se calcula **por corrida** y luego se toma la mediana (J de medianas ≠
mediana de J; se usa la segunda).

---

## 5. Predicciones — umbrales escritos ANTES de medir (los imprime el runner, ERR-89)

Salvo indicación, todo en el nivel **`rep_acum = 0`**.

| # | letra (umbral) | predicción con rango | qué la refuta |
|---|---|---|---|
| **F9-1** | **ANCLA, BLOQUEANTE**: `R₀`(NADA) ∈ [0.097, 0.22], vida(NADA) ∈ [66, 170], `R₀`(RENACE) ∈ [0.60, 1.40], `r`(RENACE) ∈ [−50, 25] | vida(NADA) **[85, 130]**, `R₀`(NADA) **[0.125, 0.16]** | fuera de rango → el instrumento se movió y **no se lee nada más** |
| **F9-2** | vida(REL) ≥ 2.5× NADA y A₁₂ ≥ 0.85 (heredada) | razón **[5.0, 7.5]**, A₁₂ **1.0** | razón < 2.5 |
| **F9-3** | `p1`(REL) ≥ 0.60, dif ≥ 0.30, A₁₂ ≥ 0.85, `c1` ≥ NADA−0.10, `sac` ≥ 0.95× (heredada) | `p1` **[0.94, 0.98]** | el balance cae |
| **F9-4bis** | **A₁₂(J: REL > REL_BAR) ≥ 0.85** y `J`(REL_BAR) ≤ `J`(NADA) + 0.10 y A₁₂(vida REL > REL_BAR) ≥ 0.80 | `J`(REL) **[0.93, 0.98]** · `J`(REL_BAR) **[0.05, 0.22]** · `J`(NADA) **[0.15, 0.22]** · A₁₂(J) **[0.95, 1.00]** | `J`(REL_BAR) > `J`(NADA)+0.10 → lo heredable **sí** sería la magnitud y no el contenido |
| **F9-5** | A₁₂(vida REL > REC) ≥ 0.65 y `R₀`(REL) ≥ 1.15× REC (heredada) | A₁₂ **[0.95, 1.00]** | A₁₂ ≤ 0.55 |
| **F9-6** | A₁₂(vida REL > REL_AZAR) ≥ 0.65 (heredada) | A₁₂ **[0.95, 1.00]** | A₁₂ ≤ 0.55 |
| **F9-8** | `R₀`(NADA, acum1)/acum0 ≥ 1.30 y Spearman ≥ 0.80; cláusula H1-6 (heredada) | razón **[1.45, 1.75]**, Spearman **[0.85, 1.00]**; **ningún brazo cruza 0.90** | Spearman < 0.80 |
| **F9-9** | contabilidad 560/560, listas OK, `frac_div`(REL) ≥ 0.50, `lect_div`(REC) = 0, exposiciones A ≥ 0.50× NADA (**exentos `REL_FIJO` y `CAUTELA`**), **+ las tres pruebas del mecanismo nuevo** | todo pasa; `fam_nac_max`(REL2b) **= 0**, `fam_nac`(REL2) **[2.0, 3.0]**, `frac_pa`(REL2b) **[0.03, 0.35]** | contabilidad < 560/560, o `via_msg`(REL2b) = 0, o `fam_nac`(REL2b) > 0 → **instrumento**, se para |
| **F9-10** | `p1`(REL_FIJO) ≥ 0.60, `R₀`(REL) ≥ 1.15× REL_FIJO, A₁₂(sac) ≥ 0.65 (heredada) | igual que el bloque 1 | REL_FIJO iguala o gana |
| **B2-1** | **vida(REL2b) ≥ 1.10× vida(REL)** y **`J`(REL2b) ≥ `J`(REL) − 0.03** | **C predijo vida [600, 1000] (1.0–1.7×). YO PREDIGO 0.95–1.20× (mediana ≈ 1.05×) y `J` 0.93–0.98: la mitad del `J` pasa y la mitad de la vida CAE.** Probabilidad que declaro de que B2-1 **pase entera: 25 %** | vida < 1.1× REL (mi predicción) **o** `J` < `J`(REL) − 0.03 (volvió la sustitución) **o** REL2b ≡ REL en todas las claves (perilla inerte, ERR-38 — ya descartado por el arnés) |
| **B2-2** | `R₀`(REL2b, acum=1) ≥ **0.50**; se reporta si cae en el rango predicho por C **[0.50, 0.80]** y si cruza **0.90** con `fundadores ≤ 2` | **C declaró 15 % de cruzar 0.90. YO declaro 5 %**, y predigo `R₀` **[0.42, 0.62]** con **45 %** de pasar el ≥ 0.50 | `R₀` < 0.50 → el candidato no mueve la aguja del linaje |
| **B2-3** | **A₁₂(vida REL2b > DOSIS) ≥ 0.70** y `R₀`(REL2b) ≥ 1.10× DOSIS. **SÓLO SE LEE SI B2-1 PASA** (si B2-1 cae, "DOSIS iguala al candidato" no dice nada: nada cambió) | DOSIS ≈ REL (la vía lenta ya satura el veneno con `eta_s`=0.15): vida(DOSIS) **[550, 700]**, A₁₂ **[0.40, 0.70]** → **predigo que B2-3 CAE** | si DOSIS iguala a REL2b **y B2-1 pasó**, lo que paga es **cantidad de aprendizaje** y el mecanismo se renombra |
| **B2-4** | vida(REL2)/vida(REL) ∈ **[0.25, 0.55]** y `J`(REL2) ≤ `J`(REL) − 0.10 | razón **[0.30, 0.50]** (C midió 0.38× ×3 en su humo), `J`(REL2) **[0.65, 0.82]**, `exp_A`(REL2) > `exp_A`(REL) | razón fuera de [0.25, 0.55] → el fallo medido por C **no se reproduce en semillas nuevas** y su diagnóstico ("la puerta sustituye") queda en duda |
| **B2-5** | (i) **cordura de la cota**: `R₀`(ORACULO) ≥ `R₀`(REL2b) − 0.02 y vida(ORACULO) ≥ 0.95× vida(REL2b). (ii) se **reporta** si `R₀`(ORACULO, acum=1) ≥ 0.90 con `fundadores ≤ 2` | (i) pasa. (ii) **predigo que NO cruza**: `R₀`(ORACULO, acum=1) **[0.45, 0.70]**; probabilidad de cruzar 0.90 que declaro: **5 %**. Razón *a priori*: las muertes de REL son **todas por necesidad** (hambre + sed), no por veneno; `p1`(REL) ya es 0.96 y `c1` 1.00, así que no queda casi nada que un contenido perfecto pueda comprar. El techo del mundo es RENACE (R₀ 0.92 / 1.31) | (i) si el oráculo **pierde** contra el candidato → instrumento, se para y se abre ERR. (ii) si **cruza 0.90** → el muro era la herencia y no el mundo, y mi predicción queda refutada |

### B2-CAUT — **el control que puede tumbar el diagnóstico de F9-4bis** (REPORTADA, no es puerta)
`CAUTELA` = nodo apagado + `sesgo_fijo = c*` **calibrado en el humo para igualar `c1(REL_BAR)`**.
**Regla de calibración, escrita ANTES del humo:** el humo corre la rejilla `c ∈ {−1.2, −2.0}`; si los dos
puntos **bracketean** `c1(REL_BAR)`, `c* =` interpolación lineal redondeada a 0.1; si no, el punto más
cercano, y la brecha se declara. **En la serie**, si `|c1(CAUTELA) − c1(REL_BAR)| > 0.10`, la calibración se
declara **fallida**, B2-CAUT **no se lee** y **no se recalibra** (regla 3).
- **Si CAUTELA reproduce vida y J de REL_BAR** (|vida/vida − 1| ≤ 0.25 y |ΔJ| ≤ 0.10) → *"el nodo barajado
  **es** cautela genérica"* queda **medido**, no inferido.
- **Si NO los reproduce** → lo que REL_BAR aporta **no es sólo cautela** y **el diagnóstico del creador C
  queda refutado**. Predicción: reproduce (probabilidad declarada **60 %**); vida(CAUTELA) **[110, 230]**
  contra vida(REL_BAR) ~155, `J`(CAUTELA) **[0.05, 0.30]**.

---

## 6. Las cuatro trampas, y las propias

1. **Canal simétrico** — n/a: el que muere escribe, el que nace lee, nadie se lee a sí mismo. Controles de
   contenido (REL_BAR, REL2b_BAR), de acceso (REL_AZAR) y de cantidad (DOSIS, CAUTELA).
2. **Acierto sin balancear** — **es LA trampa de este bloque** y por eso existe: la métrica pasa a `J`
   (vale 0 en las dos políticas degeneradas), **más** el brazo CAUTELA, que la pone a prueba en carne propia,
   **más** REL_FIJO, que ya mostró el modo de fallo (p1 0.977 con c1 0.83 y saciedad 0.35).
3. **El mundo que se come la comida** — `exposiciones[A]` se reporta por brazo con el mínimo 0.50× NADA.
   **REL2 encuentra MÁS comida que REL** (745 vs 561 en el humo de C): la medida se le pone más difícil al
   candidato, no más fácil. `REL_FIJO` y `CAUTELA` quedan **exentos y reportados**, porque su hipótesis
   escrita **es** que comen menos: castigarlos ahí confundiría "el mundo se quedó sin comida" con "este brazo
   eligió no comer" (declarado aquí, antes de correr).
4. **Sitios fijos** — `spawn()` sortea y el recién nacido aparece en `rng.integers(L)`.

**Propias, declaradas:**
(i) **El oráculo como regalo encubierto.** Lee exactamente `nodo_lee = 50` mensajes, **los mismos** que los
demás brazos, con la **misma** regla de selección, y sigue necesitando que el nodo real no esté vacío (el
fundador nace igual de vacío). Lo único que cambia es el **contenido**. Es una cota superior honesta, no un
brazo con más presupuesto — y tampoco con menos: la primera versión tenía handicap y el humo lo halló (§9).
(ii) **`c*` interpolado no se corre en el humo.** Por eso la serie **vuelve a comprobar la calibración**
(`|Δc1| ≤ 0.10`) y, si falla, B2-CAUT se retira en vez de recalibrarse.
(iii) **B2-3 condicionada.** Leer "DOSIS no iguala al candidato" cuando el candidato no gana a REL sería leer
ruido; la condición está escrita aquí y el runner la imprime.
(iv) **`pa/pn` cuentan encuentros, no mordidas.** No miden aprendizaje; miden **la puerta**. Se reportan.
(v) **Elegir el brazo mirando el dato:** el factorial se corre entero y las catorce puertas están escritas
aquí; ningún brazo se añade ni se quita después.

---

## 7. Lo que NO se declara

- **Nada nace.** `descendientes` sigue siendo un contador de ventanas de viabilidad. No se dice "población",
  "generación", "selección", "evoluciona", "cultura", "enseña", "recuerda su vida pasada", "quiere".
- **No se dice "el candidato entra"**: esto no es un candidato al tronco y `CRITERIO_TRONCO_v2/v3` no aplica.
- **Si B2-2 y B2-5 (ii) no cruzan 0.90, se dice en voz alta: H-1 y ERR-62 SIGUEN EN PIE**, y además —si
  tampoco cruza el oráculo— **el muro es el mundo**: antes de hablar de población hay que cambiar el mundo.
- 20 semillas no cierran nada: piden la réplica 1601–1620 (regla 12).

---

## 8. Humo (UN proceso, 6 corridas de T = 100 000, semillas 1–2 YA VISTAS) — predicciones ANTES de lanzarlo

Corridas: **REL2b s=1 y s=2** (el candidato: *lo que más importa medir, porque C no llegó a correrlo*),
**REL_BAR s=1** (el objetivo de calibración), **CAUTELA s=1 con `c` = −1.2 y −2.0** (la rejilla declarada) y
**ORACULO s=1**, todas con `rep_acum = 1`. Las referencias **REL y REL2 no se re-corren**: la identidad (A) y
(C) del arnés las hace exactas contra `organismo_f9` y `organismo_f9b`, y sus números a T = 100 000,
`acum = 1`, semillas 1–2 están en `datos/humo/f9b_humo_20260921_160425.json` (REL R₀ 0.423/0.484, vida
549.5/601, J 0.960/0.934; REL2 R₀ 0.415/0.450, vida 209/208, J 0.738/0.771).

- **HC1** contabilidad y longitud de listas por cuerpo en 6/6. **BLOQUEA** (instrumento).
- **HC2** `fam_nac = 0` en todos los nacimientos de REL2b y `via_msg > 0`. **BLOQUEA** (el mecanismo).
- **HC3** `frac_pa > 0` en REL2b (morder abre la puerta). **BLOQUEA**.
- **HC4** vida(REL2b) > 250 en 2/2 (o sea: **no** se reproduce el hundimiento de REL2). Hipótesis.
- **HC5** `J`(REL2b) ≥ 0.90 en 2/2. Hipótesis.
- **HC6** la rejilla `{−1.2, −2.0}` **bracketea** `c1(REL_BAR)`. Calibración.

**Sólo HC1, HC2 y HC3 bloquean.** Si HC4, HC5 o HC6 fallan, se escriben en §9 y **el bloque corre con esta
letra**. Un humo no puede refutar ni confirmar nada (n = 1–2, semillas ya vistas).
**Ningún umbral se cambia después del humo** (regla 4).

---

## 9. Humo — resultado (21-sep 17:17; `datos/humo/f9c_humo_20260921_171730.{log,json}`, sha del JSON `49297b630c9ae46f`; 95.7 s las 6 corridas; UN proceso, sin `Pool`; regla 14 8/8 e identidad interna 5/5 dentro del runner)

| brazo | s | acum | **R₀** | r | **vida** | cuerpos | **p1** | **c1** | **J** | sac | expA | via_msg | fam_nac | frac_pa |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| **REL2b** | 1 | 1 | **0.5294** | −71 | **631.0** | 153 | 0.966 | 0.991 | **0.9568** | 0.490 | 579 | 7456 | **0.0** | 0.096 |
| **REL2b** | 2 | 1 | **0.5427** | −74 | **599.0** | 164 | 0.962 | 0.983 | **0.9452** | 0.527 | 667 | 8079 | **0.0** | 0.105 |
| REL_BAR | 1 | 1 | 0.2292 | −194 | 180.0 | 253 | 0.6098 | 0.5897 | 0.1995 | 0.406 | 797 | — | — | 0.030 |
| CAUTELA (c = −1.2) | 1 | 1 | 0.3923 | −78 | 600.0 | 130 | 0.5748 | 0.6596 | 0.2344 | 0.324 | 760 | — | — | 0.024 |
| CAUTELA (c = −2.0) | 1 | 1 | 0.1419 | −132 | 200.0 | 155 | 0.9067 | 0.1161 | 0.0228 | 0.176 | 1179 | — | — | 0.020 |
| ORACULO *(versión previa, ver abajo)* | 1 | 1 | 0.4115 | −112 | 436.0 | 192 | 0.8533 | 1.000 | 0.8533 | 0.473 | 681 | 9168 | 0.0 | 0.090 |

**Referencias del humo de C (mismo T, mismas semillas, `acum = 1`; exactas por la identidad (A) y (C) del arnés):**
REL `R₀` 0.423 / 0.484, vida 549.5 / 601.0, `J` 0.960 / 0.934 · REL2 `R₀` 0.415 / 0.450, vida 209.0 / 208.0, `J` 0.738 / 0.771.

**HC1, HC2, HC3, HC4, HC5, HC6: SÍ (6/6).**

- **El candidato no se hunde: el hundimiento de `nodo_via=1` NO vuelve.** vida(REL2b) 631 / 599 contra
  **209 / 208** de REL2 (3.0× y 2.9×) y `J` 0.957 / 0.945 contra 0.738 / 0.771. La sustitución de la puerta
  está **evitada**, que era la mitad conceptual del bloque.
- **Contra REL, el efecto es pequeño y va a decidirse por poco:** vida **1.148×** (s = 1) y **0.997×** (s = 2);
  `R₀` 1.25× y 1.12×; `J` −0.003 y +0.011. **Mi predicción de §5 (0.95–1.20×, mediana ≈ 1.05×) queda del lado
  correcto y la de C (1.0–1.7×, [600, 1000]) queda en su borde inferior.** B2-1 exige ≥ 1.10× **y** `J`: en
  el humo pasaría en una semilla y caería en la otra. **No se cambia el umbral** (regla 4).
- **`R₀`(REL2b, acum = 1) = 0.53 / 0.54**, por encima del mínimo de B2-2 (0.50) y dentro del rango de C
  [0.50, 0.80]; **no cruza 0.90** (techo del mundo: RENACE 1.31).
- **El mecanismo se comporta como se escribió:** `fam_nac` = **0 en los 153 y 164 nacimientos** (leer no abre
  la puerta), `via_msg` 7 456 / 8 079 (la vía rápida sí se llena) y `frac_pa` 0.096 / 0.105 (morder sí la abre).
- **B2-CAUT apunta ya a refutar el diagnóstico de C** (n = 1, semilla ya vista, **no es evidencia**): con
  `c` = −1.2 la cautela genérica da vida **600** contra los **180** de REL_BAR con un `c1` parecido (0.66
  contra 0.59). Mi predicción escrita ("reproduce, 60 %") **está en riesgo serio y no la reescribo.**
- **Calibración (regla del §5, aplicada tal cual):** `c1`(REL_BAR) 0.5897 queda **bracketeado** por 0.6596
  (c = −1.2) y 0.1161 (c = −2.0) → **`c*` = −1.3** por interpolación lineal. Escrito en `corre_bloque2.py`
  con la cita del JSON. **`c*` = −1.3 no se corrió**: la serie revalida la calibración y, si
  `|Δc1| > 0.10`, B2-CAUT se retira en vez de recalibrarse.

### El humo halló un CONFOUND en el brazo ORACULO y se arregló el INSTRUMENTO (no un umbral)
Con la primera versión, el oráculo entregaba **48 mensajes = seis copias de la tabla**, es decir un pool del
**mismo tamaño que el presupuesto de lectura**: no había selección, y **la mitad de la lectura se gastaba en
los cuatro pares con R = 0** de la tabla verdadera (A con sed, B con sed, C con hambre, D con hambre). Salía
`R₀` 0.41 y vida 436, **por debajo del candidato** — es decir, la "cota superior" llegaba con handicap y
`B2-5 (i)` iba a caer por el instrumento, no por el mundo. **Arreglo declarado:** el pool del oráculo pasa a
`8 × nodo_lee = 400` mensajes (cincuenta copias exactas de la tabla) y el recién nacido lee `nodo_lee = 50`
**por la misma regla de relevancia que todos los demás brazos**: mismo canal, **mismo presupuesto**, mejor
contenido. `organismo_f9c.py` pasa de `f40336f05a787be8` a **`9dd1fb91ecec35ae`**; el arnés se volvió a
correr entero: **109/109**, y el caso (J) queda más limpio (fila hambre A 0.952 / B −2.934; fila sed C 0.961
/ D −2.947). **Ningún umbral de §5 se tocó.** **Lo que NO pude verificar:** el ORACULO arreglado **no tiene
humo** (las 6 corridas del presupuesto ya estaban gastadas); su número de la tabla de arriba es de la versión
previa y **no debe citarse**. Lo que sí está verificado del arreglo es el arnés (contenido exacto, controles
que difieren, `f9c` solo lectura, determinismo).

---

## 10. Comando de la serie (lo corre el coordinador, un Pool a la vez)

```
python experimentos/nivel09_cuerpo_nuevo_b2/corre_bloque2.py --desde 1581            # serie (560 corridas)
python experimentos/nivel09_cuerpo_nuevo_b2/corre_bloque2.py --desde 1601            # réplica (regla 12)
```
`JUACO_POOL` fija el Pool (ERR-86). Con Pool 8 la serie del bloque 1 (360 corridas) tardó 444 s; ésta tiene
560 y debería rondar **12–16 min**.
