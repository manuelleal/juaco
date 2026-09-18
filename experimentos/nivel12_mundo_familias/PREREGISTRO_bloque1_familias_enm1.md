# PREREGISTRO — BLOQUE 1, ENMIENDA 1 (**ERR-46**): la medida que separa "aprende a costa de los hermanos" de "no aprende nada"

**Misión (primero, siempre):** llegar a la AGI por este camino — un organismo mínimo con reglas locales (sin backprop en el
runtime) que aprende, desaprende, generaliza, sobrevive y se reproduce, con evidencia preregistrada. **Primero llegar a la
frontera; segundo, que viva.** Y aquí, en concreto: **un mundo que obligue a representar.**

**Autor:** diseñador del bloque 1, sala 2. **Fecha de firma:** 18 sep 2026, tras la serie 401–420.
**ERR-46** (asignado por el coordinador). **Regla 11:** toda enmienda que cambie un umbral o la forma de un criterio lleva
ERR numerado al escribirla, aunque se escriba antes de la serie nueva y aunque resulte inerte.

**Estado al firmar:** §1–§8 se escribieron **ENTERAS antes de correr una sola corrida de la enmienda**. Sólo §9 (humo) se
escribe después, y **nada de §1–§8 se toca al escribirlo**. §10 lo escribe el coordinador con la serie 441–460.

**Qué NO toca esta enmienda.** `PREREGISTRO_bloque1_familias.md`, `construye_familias.py`, `organismo_familias.py`,
`identidad_familias.py` y `corre_familias.py` **quedan como están y no se editan**; sus veredictos de 401–420 quedan como
están (regla 3: no se rejuzga tras ver datos). Tampoco se toca nada del bloque 0 ni ningún archivo congelado. Los archivos
nuevos son **sólo dos**: este documento y `corre_familias_enm1.py`, que **importa** `corre_familias.py` y **reutiliza su
instrumento sin modificarlo**. Sin `Pool`. Sin commits.

---

## 1. Qué falló en 401–420, y por qué la culpa es de la medida y no del mundo

Resultado registrado (`datos/familias_s401-420_20260918_144946`, identidad 24/24):

| brazo | `colateral` | `omision` | `w_var` | muertes |
|---|---|---|---|---|
| **EXC** | 6.0 | 22.5 | **0.000** | 2 |
| **LIN** | 2.0 | 4.0 | **0.000** | 1 |
| **AZA** | **19.5** | 75.5 | 0.14 | — |
| **BAR** | **17.0** | 146.5 | **2.79** | 4 |
| V14 (ancla, anillo del tronco) | — | — | — | **133.5** |

P2 INDECISO (razón 3.0, A₁₂ 0.68) · P3 NO (`w_var` 0, como estaba predicho en §12.2 del preregistro original) ·
**P5 cae** · P7a pasa · P7b: B-5 con neutros **no** repara.

**El diagnóstico, en una frase:** `colateral` cuenta **mordidas de veneno en los hermanos**, y un organismo que **no ha
aprendido nada** muerde veneno todo el rato. Por eso `azar` (19.5) y `barajado` (17.0) — los dos mundos donde el organismo
**no puede** aprender una familia — puntúan **el triple** que `excepciones` (6.0). La medida mide *ignorancia*, no *daño
colateral*. Es exactamente la trampa que el propio criterio v2 prohíbe en su última línea (**ERR-44**: *"cualquier
subcriterio que no distinga 'aprendió de un golpe' de 'no aprendió'"*), y yo la reintroduje por otra puerta.

Lo mismo con `w_var`: salió **0.000** en tres de los cuatro mundos porque el drenaje `lam` borra la parte común de
`Wps`/`Wns` y los píxeles de variable, que están encendidos en la mitad de los estímulos presentes con **las dos**
valencias, quedan en cero. Y salió **2.79** justo en `barajado`, donde el organismo está más perdido. **`w_var` mide lo
mismo que `colateral`: desorden, no contaminación dirigida.**

**Lo que NO se concluye de 401–420:** que el mundo no obliga. Con la medida rota, el mundo no ha sido preguntado todavía.

---

## 2. LA MEDIDA NUEVA: daño condicionado a haber aprendido, y normalizado por lo que los hermanos ya sabían

Todo se calcula **fuera del organismo**, en el runner, a partir de dos cosas que el instrumento **ya devuelve** y que **no
hay que tocar**: la serie temporal `log` (la perilla `log_cada` de v14.1, que registra `valor(P)` — **el valor que usa la
boca**, la lectura ruteada real — para los 32 estímulos) y `t_exc` (el paso de la primera mordida de cada ventana).
**No se construye ningún instrumento nuevo, no se toca `organismo_familias.py`, la identidad 43/43 sigue valiendo.**

Notación, para una ventana `e` (una de las 8 de `exc_win`, **las mismas en los cuatro mundos**):

- `obj(k)` = +1 si el mundo dice comida, −1 si veneno.
- **`ok(k, t)` = 1** si `v_k(t)·obj(k) > 0` **y** `|v_k(t)| ≥ crit_exp = 0.5`, donde `v_k(t)` es lo que **lee la boca**
  (nunca un peso interno: T-E, **ERR-44**).
- `t0 = t_exc[e]` (primera mordida de `e`), `t1 = t0 + vent` (`vent = 10 000`).
- **hermanos de `e`** = su token **y** las otras `V−1` variantes de ese token (3 hermanos con `V = 3`), **excluida `e`**.
- **`h_antes(e)`** = fracción de hermanos con `ok = 1` en el punto de log inmediatamente **anterior** a `t0`.
- **`h_desp(e)`** = lo mismo en el punto de log más cercano a `t1`.
- **`dano(e) = h_antes(e) − h_desp(e)`** ∈ [−1, 1].
- **`apr(e)`** = 1 si `ok(e, t1) = 1`: **la excepción se aprendió dentro de su ventana**.
- **`valida(e)`** = `apr(e) = 1` **y** `h_antes(e) ≥ h_min = 0.67` (**al menos 2 de los 3 hermanos ya se leían bien antes de
  la excepción**: sin eso no hay nada que dañar).

Y entonces:

| medida | definición | qué separa |
|---|---|---|
| **`colateral_n`** *(la que decide)* | media de `dano(e)` sobre las ventanas **válidas**; `None` si no hay ninguna | "aprendió la excepción **y** sus hermanos se estropearon" |
| **`n_valida`** *(obligatoria, va siempre al lado)* | número de ventanas válidas, de 8 | dónde la pregunta **está definida**: hace falta una familia real |
| **`dano_bruto`** | media de `dano(e)` sobre **todas** las ventanas, sin condicionar | el control que enseña **por qué** la medida vieja fallaba (§6, E4) |
| `apr_tasa` | media de `apr(e)` sobre las 8 ventanas | cuánto aprende el organismo en cada mundo |
| `h_antes_med` | media de `h_antes(e)` | cuánta familia hay antes de la excepción |
| `colateral`, `omision`, `w_var` | **las de 401–420, sin cambio** | continuidad de la línea base; **ya no son puerta** |

### 2.1 Por qué `azar` y `barajado` quedan por debajo de `lineal` POR CONSTRUCCIÓN

La condición `h_antes(e) ≥ 0.67` exige que **dos de los tres hermanos de una misma familia se estuvieran leyendo
correctamente a la vez** justo antes de la ventana.

- En **`azar`** las valencias se sortean **por estímulo**: los "hermanos" de una ventana no comparten valencia, y que dos de
  tres estén bien leídos simultáneamente es un accidente. → `n_valida` bajo, y entre las pocas válidas `dano` no tiene
  dirección (la ventana no la abre nada que contradiga a la familia, porque no hay familia).
- En **`barajado`** cada variante toma la valencia de **otro** token: los tres hermanos llevan valencias mezcladas por
  construcción. → mismo efecto.
- En **`lineal`** los hermanos son consistentes (`h_antes` alto) y la ventana la abre una variante que **concuerda** con su
  token: aprenderla **confirma** a los hermanos → `dano ≈ 0` o **negativo**.
- En **`excepciones`** los hermanos son consistentes **y** la ventana la abre una variante que **contradice** → `dano > 0`.

### 2.2 La guarda contra el control de paja (ERR-39), escrita antes

Si `n_valida` fuese 0 en `azar` y `barajado`, decir "puntúan por debajo de `lineal`" sería **trivial por censura**, no un
resultado. Por eso **`n_valida` es una predicción propia y obligatoria (E3)**, una ventana sin `valida` **nunca cuenta como
victoria** (convención de `corre_vivo.py`: un `None` no gana), y si `n_valida ≈ 0` en esos mundos la letra que se escribe es:
***"la medida no está definida ahí, y ése es el punto: sin familias reales no hay hermanos que dañar"*** — no "puntúan bajo".

### 2.3 `w_var` se RETIRA como predicción decisiva (ERR-46) y se sigue reportando

Motivo, escrito con su mecanismo: el drenaje `lam` sobre `min(Wps, Wns)` borra los píxeles de variable, que reciben las dos
valencias. `w_var` midió **desorden** (2.79 en `barajado`, 0.000 donde el organismo aprende), no contaminación dirigida. Su
sustituto no es otro peso interno: es `colateral_n`, que se mide **sobre lo que lee la boca** (T-E, ERR-44). `w_var` se
reporta en las tablas y **no decide nada**.

---

## 3. `n_exc = 8`: una excepción por token

Como manda la cláusula de endurecimiento del preregistro original (§6, P2/P3) y el encargo del coordinador. Con `F = 8`
tokens y `exc_win` de 8 candidatas (una por token, sorteada **siempre** con el rng propio del mundo), `n_exc = 8` activa
**todas**: cada familia tiene su "sal rosa". `lineal` sigue con `n_exc = 0` y **las mismas 8 ventanas**.

Consecuencia declarada: con `n_exc = 8` los hermanos de una ventana (token + otras 2 variantes) **no** son excepciones —
sigue habiendo a lo sumo una por token —, así que `dano` no se contamina con excepciones cruzadas.

---

## 4. LA PERILLA DE DUREZA: `dureza`, y su valor DERIVADO antes de medir

**El problema, medido:** en el mundo de familias v14.1 muere **1–2 veces por 100 000 pasos** (`frac_regalo` ≤ 0.006); en el
anillo del tronco, **133.5**. T-A (*"muertes ≤ 1.10 × línea base"*) tendría **efecto suelo**: no discriminaría nada.

**La causa, y por qué no es un accidente:** la mortalidad del tronco venía en buena parte de la **trampa 3**. En el ancla
V14 del mundo vivo el anillo se llenaba de lo rechazado: **B 7 897.5 llegadas contra A 344.5** (23×). Con renovación
simétrica, la comida deja de estar tapada por el veneno. Si el total de llegadas se conserva y se reparte a la mitad, las
llegadas a comida pasan de **344.5** a **(344.5 + 7 897.5)/2 = 4 121**, es decir **×11.96**.

> **Regla de dureza, escrita ANTES del humo y derivada SÓLO de números ya publicados del tronco** (`datos/vivo_s181-200`,
> citados en `DIAG_mundo` bloqueo 3), **sin mirar un solo dato del mundo nuevo**: `dureza` = factor multiplicativo de
> `costo`. En el anillo del tronco el organismo drena `costo · T = 0.002 · 100 000 = 200` unidades y cada comida da `+0.8`,
> así que necesita **250 mordidas de comida** sobre **344.5** llegadas: acierta en el **72.6 %** de sus encuentros de
> comida. Para exigirle **la misma fracción** con 11.96× más llegadas de comida, `costo` debe subir **×11.96**. Se redondea
> al entero: **`dureza = 12`, `costo = 0.024`.**

**Cláusula (una sola corrección, con ERR nuevo):** si las muertes de EXC o LIN quedan **fuera de [20, 250] por 100 000**, se
reporta y se corrige `dureza` **UNA** vez, con **ERR-47**, semillas nuevas y la misma letra. La banda se escribe aquí: el
suelo 20 es "diez veces más de lo que mata hoy" y el techo 250 es "el doble del anillo del tronco (133.5)"; **el valor
esperado (≈133) no es ninguno de los dos extremos** (ERR-37a: el umbral no se pone en la mediana esperada del efecto).

**Qué NO cambia con `dureza`:** `L = 160`, `nobj = 16`, `renov = 1.0`, `deriva`, `cambio`, `vent`, `crit_exp`, `NK/NKMAX/K`
y **el organismo**. Un solo cambio de física, y va declarado.

---

## 5. BRAZOS Y SEMILLAS

| brazo | perillas (sobre el mundo del preregistro original) |
|---|---|
| **EXC** | `n_exc=8, fam_val='familia', dureza=12 (costo=0.024), log_cada=250` |
| **LIN** | `n_exc=0`, resto igual |
| **AZA** | `fam_val='azar'`, resto igual |
| **BAR** | `fam_val='barajado'`, resto igual |
| **V14** *(ancla)* | `mundo='AB'` con el `costo` del TRONCO (0.002): sigue siendo v14.1 literal y **no compite** |

**4 brazos × 20 semillas = 80 corridas** (+ el ancla). **Semillas 441–460**, nuevas; **réplica 461–480** (regla 12).
`T = 100 000`. Semillas del arnés: 1, 2, 3.

**Los brazos B-5 (`EXC-B5`, `LIN-B5`, `NEU`, `NEU-B5`) NO se repiten**, y se dice por qué: su pregunta ya está contestada en
401–420 — **P7a pasa** (B-5 es inerte donde toda mordida informa) y **P7b cae** (con neutros, B-5 se dispara pero **no
repara**: NEU 7.5 → NEU-B5 9.0 con 71.5 celdas). Repetirlos gastaría `Pool` sin preguntar nada nuevo.

---

## 6. PREDICCIONES NUMÉRICAS (escritas antes de correr la enmienda)

Estadística, sin cambio: lo aprendido se **parea** por semilla; lo que es integral de trayectoria va con **A₁₂ sin parear,
razón de medianas y cuartiles** (ERR-37b); **nunca `max`** (ERR-37c); **ningún umbral en la mediana esperada del propio
efecto** (ERR-37a); **sin zonas muertas** (§E.4).

| # | predicción | umbral | qué me refuta | zona declarada |
|---|---|---|---|---|
| **E1 — dureza** (puerta; si cae, E2–E4 no se leen) | con `dureza = 12` el mundo mata en un rango con recorrido | muertes por 100 000 en **EXC y LIN dentro de [20, 250]** (medianas); `frac_regalo` reportado siempre | fuera de banda en cualquiera de los dos | **UNA** corrección de `dureza` con **ERR-47**, semillas nuevas |
| **E2 — `colateral_n` (LA QUE DECIDE)** | aprender la excepción **estropea** a los hermanos, y sólo donde hay familia | **(a) dirección:** pareado por semilla `colateral_n(EXC) > colateral_n(LIN)` en **≥ 15/20**; **(b) magnitud:** mediana `colateral_n(EXC) ≥ 0.20` | (a) ≤ **11/20** (banda de azar para 20 semillas) **o** (b) mediana ≤ **0.05** → **el mundo no obliga ni con una excepción por token**, y la línea pasa al **mundo** (retina mayor, más variantes por token), **no al organismo** | (a) en 12–14/20 **o** (b) en (0.05, 0.20) → **INDECISO**: se reporta y **no se declara nada**; la decisión de endurecer otra vez es del coordinador, con ERR nuevo. **Derivación del umbral (ERR-37a):** con 3 hermanos, `dano` se mueve en escalones de **1/3 = 0.333**; **0.20 no es un escalón** y está entre "medio hermano por ventana" (0.167) y "un hermano por ventana" (0.333), así que no coincide con la mediana esperada de ningún resultado limpio |
| **E3 — `n_valida` y el orden de los mundos** (validez de la medida) | la condición sólo está definida donde hay familias reales | mediana `n_valida`: **EXC ≥ 4** y **LIN ≥ 4** (de 8); **BAR ≤ 2** y **AZA ≤ 2**; y en medianas `colateral_n(AZA) ≤ colateral_n(LIN)` **y** `colateral_n(BAR) ≤ colateral_n(LIN)` | `n_valida(AZA) ≥ 4` o `n_valida(BAR) ≥ 4` → la condición **no** distingue familia real de familia falsa y la medida sigue sin servir: se dice y se para | si `n_valida(AZA) = 0` o `n_valida(BAR) = 0`, la letra es **"la medida no está definida ahí"**, NO "puntúan bajo" (§2.2, ERR-39). `n_valida` va en **todas** las tablas |
| **E4 — `dano_bruto`** (el control que explica el fallo de 401–420) | sin condicionar por "aprendió", la medida vuelve a premiar la ignorancia | `dano_bruto` **NO** ordena: `dano_bruto(AZA) ≥ dano_bruto(EXC)` **o** `dano_bruto(BAR) ≥ dano_bruto(EXC)`, mientras `colateral_n` sí ordena | que `dano_bruto` **ya** ordene bien → la condición `apr` **sobra**, y se dice con esas palabras (sería una simplificación, no un fracaso) | — |
| **E5 — `w_var` retirada** (ERR-46) | — | se **reporta**, no decide | — | ya declarado en §2.3 |
| **E6 — continuidad** | la línea base sigue siendo comparable | `colateral`, `omision`, muertes, celdas, splits, `ruta`, `exp_asoc` por clase, `frac_veneno`, alias y ventanas SEPARABLE/ALIAS se reportan con `n_exc = 8` y `dureza = 12` | — | sin umbral: es la línea base de T-A / T-F / T-G corregida |
| **E7 — identidad** | el instrumento no ha cambiado | subconjunto crítico del arnés **24/24** (`corre_familias.py` reutilizado sin tocar); sha `organismo_familias.py` == `b9dd561a0cf056b8`; sha `organismo_v14.py` == `feefc88b1fd8d434` | cualquier caída → no se corre nada | — |

**Predicción global, para poder equivocarme.** Predigo que **E1 pasa** (la derivación ×12 es de la física del mundo viejo, no
un ajuste); que **E3 pasa y es lo más sólido del bloque** (la condición es estructural); que **E2(a) pasa y E2(b) es la
frágil** — con `dureza = 12` el organismo muere más, muestrea peor y puede que ni `h_antes` ni `apr` lleguen a la vez con
frecuencia; y que **E4 pasa**, porque es literalmente lo que ya se midió en 401–420 con otro nombre. **Si E2 cae en (b) pero
pasa en (a)**, la letra honesta es *"el daño existe y tiene dirección, pero es pequeño: una excepción por token todavía no
obliga"*, y lo que sigue es un mundo con más variantes por token, **no** un órgano.

---

## 7. QUÉ NO DECIDE ESTA ENMIENDA

1. **No rejuzga 401–420.** Sus veredictos quedan (regla 3). La línea base de T-A/T-F/T-G **se sustituye** por la de esta
   enmienda **sólo** porque `dureza` cambia la física; las dos quedan en `datos/` con su sha y su fecha.
2. **No toca el organismo.** Sigue siendo v14.1 tal cual, con B-5 apagado en los cuatro brazos.
3. **No reabre B-5** (§5).
4. **No declara** "token", "lenguaje", "concepto", "entiende" ni "representa" (regla 8). Lo declarable, si E2 y E3 pasan, es
   literalmente: *"cuando el organismo aprende una variante que contradice a su familia, deja de leer bien a sus hermanos;
   en el mismo mundo sin contradicción, no; y donde no hay familia la pregunta ni siquiera está definida"*.

## 8. TRAMPAS QUE ESTOY EVITANDO, CON EL ERR QUE LAS RESPALDA

- **ERR-44 / T-E**: `colateral_n` se mide sobre **lo que lee la boca**, y la condición `apr` existe precisamente para
  distinguir "aprendió" de "no aprendió". Es la trampa que me comí en 401–420 y es el motivo de esta enmienda.
- **ERR-39** (controles de paja): §2.2, `n_valida` obligatoria, censura declarada, `None` nunca gana.
- **ERR-37a**: los umbrales de E2(b) y E1 traen su derivación y **no** caen en la mediana esperada del efecto.
- **ERR-37b/c**: A₁₂ sin parear para trayectorias, medianas y cuartiles, nunca `max`.
- **§E.4** (zonas muertas): E2 declara pasa / refuta / INDECISO.
- **§E.6** (copiar instrumentos, ERR-38/41/42/43): `corre_familias_enm1.py` **importa** `corre_familias.py`; no copia ni el
  mundo, ni los brazos, ni el diagnóstico, ni el cruce `cod0`. El humo **escribe su JSON**.
- **§E.10**: nada agregado sin la tabla de exposiciones por patrón al lado.
- **§E.14**: el humo usa semillas **1–2**; la serie, 441–460.
- **§E.16 / decisión 09:55 §3**: si E2 cae, **se endurece el mundo, no se toca el organismo**.
- **§E.17 / regla 11**: esta enmienda lleva **ERR-46** en el título y reserva **ERR-47** para la única corrección de
  `dureza` que se permite.

---

---

# ADENDA (escrita ANTES de volver a medir; §1–§8 quedan intactas)

El primer humo de un proceso (semillas 1–2, `dureza = 12`, `datos/familias_enm1_humo_20260918_145919.json`, sha16
`ab1cd5d068d71eb0`) disparó **las dos cláusulas** que §4 y §8 dejaron escritas. Las ejecuto aquí, cada una con su ERR, y
**vuelvo a medir sólo después de escribir esto**. Ningún umbral de §6 se toca salvo lo que estas dos adendas dicen, y cada
cambio lleva su número (regla 11).

## A. **ERR-47** — `dureza = 12` está fuera de banda; corrección ÚNICA por escalera declarada

**Lo medido (n = 2, humo):** muertes por 100 000 — EXC **[1268, 939]**, LIN **[699, 754]**, AZA [977, 829], BAR [1417, 1761];
`frac_regalo` 0.17–0.44. La banda de **E1 era [20, 250]**: `dureza = 12` la supera por un factor de 3 a 7. Mi derivación de
§4 (×11.96 por el 23× de la trampa 3) suponía que el organismo podía **aprovechar** las llegadas de comida extra; con
`E ≤ 1.5` de tope y `0.8` por bocado, a `costo = 0.024` necesita comer cada **33 pasos** y no le da tiempo. La derivación
era correcta en las llegadas y falsa en la política: el cuello no es la comida disponible, es la tasa a la que la boca puede
convertirla.

**La cláusula de §4 permite UNA corrección. Se ejecuta así, y la regla se escribe antes de correr la escalera:**

> **Regla de corrección (ERR-47).** Se prueba la escalera **`dureza ∈ {2, 4, 6}`** — tres valores **por debajo** del que ya
> se vio, sobre ninguno de los cuales tengo dato alguno — en el brazo **`LIN`** (el control) con las **semillas 1–2** del
> humo, un proceso. **Se toma el MENOR `dureza` de la escalera cuya mediana de muertes de `LIN` caiga dentro de
> [20, 250].** Si **ninguno** cae, se declara que **`costo` no tiene régimen intermedio en este mundo** — pasa de 1–2
> muertes a centenares sin escalón — y la dureza se busca por **escasez** (`nobj`), en un preregistro nuevo y con ERR nuevo;
> la serie 441–460 **no se corre** hasta entonces. **No se prueba ningún valor fuera de {2, 4, 6}, ni se interpola sobre los
> datos ya vistos.**

Esto es una **calibración con regla fija**, del mismo tipo que la *"calibración OBLIGATORIA antes del preregistro"* que la
síntesis exige al bloque 4, y se hace sobre el brazo de control y sobre semillas que **no** son las de la serie.
Coste declarado: 6 corridas de un proceso (la regla 3 de EQUIPO fija ≤ 6 corridas por humo; **estas 6 son la escalera y van
aparte del humo de 8 que pidió el coordinador** — lo digo en vez de esconderlo en el total).

## B. **ERR-48** — la medida de §2 tiene un confusor de tendencia; se corrige con diferencia en diferencias

**Lo medido (n = 2, humo):** `dano_bruto` es **negativo en los cuatro mundos** (−0.67 a −0.12). Los hermanos **mejoran**
entre `t0` y `t0 + vent`, no empeoran — y no porque la excepción no haga daño, sino porque **el organismo está aprendiendo
todo el tiempo**: `h_antes` va de 0.25 a 0.75 y sube sola. `dano(e) = h_antes − h_desp` mide **la tendencia global de
aprendizaje**, no el efecto de la excepción. Es el mismo error de forma que el de 401–420 (una medida que responde a algo
distinto de lo que dice medir), cazado esta vez **en el humo y no en la serie**.

> **Corrección (ERR-48), escrita antes de volver a medir.** Se resta la tendencia del propio organismo, en la propia
> corrida y en los mismos dos instantes, con **diferencia en diferencias**:
>
> - `Δh(e)` = `h_desp(e) − h_antes(e)` — cuánto **mejoraron los hermanos** durante la ventana.
> - `g_antes(e)`, `g_desp(e)` = fracción de estímulos **ajenos a la familia de `e`** (todos los demás, con valencia
>   informativa) leídos correctamente en los mismos dos puntos de log; `Δg(e) = g_desp − g_antes` es **la tendencia del
>   resto del mundo** en esa misma ventana.
> - **`dano(e) = Δg(e) − Δh(e)`** — *cuánto MENOS mejoraron los hermanos que el resto del mundo*. **Positivo = daño.**
>
> Con esto, un organismo que simplemente aprende deprisa da `dano ≈ 0` en todas partes (hermanos y resto suben igual), y
> sólo queda por encima de cero lo que es **específico de la familia de la excepción**. `colateral_n`, `n_valida`,
> `valida(e)`, `apr(e)` y `h_min` **se mantienen exactamente como en §2**; lo único que cambia es la fórmula de `dano(e)`.
> `dano_bruto` (la de §2, sin ajustar) y `dano_mundo` (`Δg`) **se reportan siempre al lado**, para que se vea la tendencia
> que se está restando.

**Los umbrales de E2 NO se mueven** (`≥ 0.20` de magnitud, `≥ 15/20` de dirección, refuta en `≤ 0.05` o `≤ 11/20`): la escala
de `dano` sigue siendo la misma (fracciones de hermanos, escalones de 1/3), y mover el umbral al cambiar la fórmula sería
exactamente lo que la regla 3 prohíbe. **E4 se reescribe en consecuencia y se declara aquí:** el control pasa a ser
*"`dano_bruto` (sin restar la tendencia) es negativo o no ordena, mientras `colateral_n` (con la tendencia restada) sí
ordena"* — y si `dano_bruto` ya ordenase solo, se dice que la corrección **sobra**.

**Lo que esta adenda NO hace:** no rejuzga nada, no toca el instrumento (`organismo_familias.py` sigue en
`b9dd561a0cf056b8`, identidad 43/43), no cambia los brazos, ni las semillas de la serie (441–460), ni `n_exc = 8`, ni
`h_min`, ni `crit_exp`, ni `vent`.

---

## 9. HUMO — resultado (18 sep 2026; §1–§8 y la ADENDA no se tocaron)

**Tres corridas de un proceso, sin `Pool`, todas con semillas 1–2** (ninguna de 441–480 queda expuesta, §E.14):

| paso | qué | datos |
|---|---|---|
| 1 | humo con `dureza = 12` (la derivación de §4) | `familias_enm1_humo_20260918_145919.json` · `ab1cd5d068d71eb0` |
| 2 | **escalera ERR-47** (regla fija, brazo LIN) | `familias_enm1_escalera_20260918_150316.json` · `031a782dde669d80` |
| 3 | humo con `dureza = 4` y la medida de **ERR-48** | `familias_enm1_humo_20260918_150412.json` · `1ae9010b198608f9` |

Identidad (tripwire E7): sha `organismo_familias.py` = `b9dd561a0cf056b8` (el que pasó 43/43) y 6/6 en los tres casos del
arnés que se reejecutan. El instrumento **no cambió**: todo lo nuevo se calcula en el runner.

### 9.1 Escalera de dureza (ERR-47) — la regla, ejecutada al pie de la letra

| `dureza` | `costo` | muertes LIN (s1, s2) | mediana | banda [20, 250] |
|---|---|---|---|---|
| 2 | 0.004 | 2, 5 | 3.5 | fuera |
| **4** | **0.008** | **32, 30** | **31.0** | **DENTRO** ← el menor en banda |
| 6 | 0.012 | 87, 78 | 82.5 | dentro |

**Se toma `dureza = 4`** por la regla escrita antes ("el menor de {2, 4, 6} dentro de banda"), no por parecerse más al
ancla del tronco (133.5, a la que `dureza = 6` se acerca más). **La derivación ×12 de §4 queda refutada y registrada**: el
cuello no era la comida disponible sino la tasa a la que la boca puede convertirla (`E ≤ 1.5`, `+0.8` por bocado).

### 9.2 La tabla del humo con `dureza = 4` y la medida corregida (n = 2: **NO es evidencia**)

| brazo | `colateral_n` | `n_valida` / `n_ventanas` | `dano_bruto` | `dano_mundo` (Δg) | `apr` | `h_antes` | muertes | `frac_regalo` | celdas | `colateral` (viejo) | `w_var` |
|---|---|---|---|---|---|---|---|---|---|---|---|
| **EXC** | **0.310 · 0.266** | 2/7 · 3/6 | −0.095 · −0.278 | +0.169 · +0.220 | 0.286 · 0.500 | **0.857 · 0.667** | 45 · 49 | 0.034 · 0.037 | 63 · 62 | 6 · 8 | 0.0 · 0.0 |
| **LIN** | **0.000 · 0.000** | 2/5 · 3/6 | −0.600 · −0.500 | +0.600 · +0.310 | 1.000 · 1.000 | 0.400 · 0.500 | 32 · 30 | 0.024 · 0.023 | 45 · 55 | 0 · 2 | 0.0 · 0.0 |
| AZA | 0.036 · 0.476 | **1/4 · 1/5** | −0.417 · −0.267 | +0.277 · +0.222 | 0.750 · 0.600 | 0.417 · 0.400 | 292 · 64 | 0.219 · 0.048 | 41 · 56 | 16 · 17 | 3.64 · 3.66 |
| BAR | 0.667 · **None** | **1/4 · 0/8** | −0.500 · −0.250 | +0.491 · +0.277 | 1.000 · 0.750 | 0.250 · 0.459 | 142 · 78 | 0.107 · 0.059 | 70 · 70 | 14 · 27 | 2.79 · 0.63 |

### 9.3 Qué dice el humo, sin ajustar nada

1. **La corrección ERR-48 era necesaria y funciona.** `dano_bruto` es **negativo en los ocho casos** (−0.10 a −0.60): los
   hermanos **mejoran** durante la ventana, porque el organismo aprende todo el rato (`dano_mundo` = +0.17 a +0.60). Sin
   restar esa tendencia, la medida habría dicho "no hay daño" en todas partes. Con la diferencia en diferencias, **EXC
   0.310 / 0.266 contra LIN 0.000 / 0.000**: el daño aparece **exactamente donde hay contradicción y en ninguna otra parte**.
   Es lo primero de todo el bloque que apunta en la dirección de E2 (umbral 0.20, no tocado).
2. **`apr` explica la mitad del cuadro.** En `lineal` la ventana la abre una variante que concuerda: se aprende siempre
   (`apr` 1.00). En `excepciones` la excepción sólo se aprende en el **29–50 %** de las ventanas. Es decir: **v14.1 casi no
   aprende las excepciones**, y cuando las aprende, sus hermanos lo pagan. Esa frase — *"cuando la aprende, la paga"* — es
   la que la serie 441–460 tiene que confirmar o tumbar en 20 semillas.
3. **E3, tal como está escrita, apunta a caer, y digo por qué antes de que caiga.** `n_valida` mediana sale **2–3 en EXC y
   en LIN** (el umbral escrito es ≥ 4), y **0–1 en AZA y BAR** (≤ 2, eso sí se cumple). El problema serio no es el umbral:
   es que **con `n_valida = 1` la media de `colateral_n` es una sola ventana** — por eso AZA marca 0.476 y BAR 0.667 en la
   semilla donde tienen su única ventana válida. **La cláusula de orden de E3 (`AZA` y `BAR` ≤ `LIN`) probablemente caerá
   por ruido de una sola observación, no por estructura.**
   **Propuesta al coordinador, que NO aplico yo** (sería la tercera corrección seguida y eso es exactamente "recalibrar
   hasta que pase"): exigir **`n_valida ≥ 2`** para que `colateral_n` esté definida, y censurar la corrida si no llega. Es
   un cambio de una línea, va con **ERR nuevo** y debe decidirse **antes** de la serie. Si el coordinador prefiere no
   tocarlo, la serie corre tal cual y `n_valida` se lee al lado de todo, como ya está escrito.
4. **E1 pasa con `dureza = 4`** en los dos brazos que la letra exige (EXC 45/49, LIN 30/32, dentro de [20, 250]), con
   `frac_regalo` bajado a 0.02–0.04. **AZA (292) y BAR (142) se salen por arriba** — y eso no es un fallo: son los mundos
   donde el organismo no puede aprender, así que muere más. La letra de E1 pide la banda **sólo** en EXC y LIN, y así se
   escribió.
5. **`w_var` confirma lo que ya se dijo al retirarla (ERR-46):** 0.000 donde el organismo aprende (EXC, LIN) y **3.64 /
   2.79 donde está perdido** (AZA, BAR). Mide desorden. Se reporta y no decide.
6. **Coste:** 5.7 s por corrida → la serie (4 brazos × 20 semillas = **80 corridas**) ≈ **0.5 min de pared con `Pool(14)`**;
   la réplica 461–480, igual.

## 10. SERIE 441–460 — resultado

*(Vacío al firmar. Lo escribe el coordinador cuando lance el `Pool`.)*

## Nota del coordinador ANTES de la serie (18 sep 15:20) — ERR-49: colateral_n sólo se define con n_valida >= 2 (una ventana válida es ruido: AZA 0.476 y BAR 0.667 con una sola ventana en el humo); las corridas con n_valida < 2 se reportan como 'sin dato' y no entran en la mediana ni en el pareado. Ningún umbral de E1–E4 cambia. Decidido por el coordinador a propuesta del diseñador, que no lo aplicó por no recalibrar tres veces seguidas.
