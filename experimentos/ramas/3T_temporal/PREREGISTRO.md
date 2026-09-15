# 3T — Composición temporal. ¿La regla de división de 2L descubre sola la dimensión del orden?

**Rama exploratoria. Escrito ANTES de correr nada. Fecha: 15 sep 2026.**
Autor: Claude (rama 3T). Dirección: Christiam Puentes.
No toca `organismo/`, `registro/`, `datos/`, `experimentos/run_etapa.py`, `experimentos/analiza.py` ni `experimentos/etapa3/`.
Todo el código vive en `experimentos/ramas/3T_temporal/`.

---

## 0. Calibración de instrumento hecha ANTES del preregistro (y qué se miró)

Se corrió `probe_init.py`, que **no simula nada**: solo mide geometría de códigos Kenyon en la inicialización,
para decidir si el muestreo por rechazo del arm C2 es viable. Resultados (20.000 sorteos):

| condición sobre KW aleatorio | tasa de aceptación |
|---|---|
| NIN=6, `code(A) ∩ code(B) == 0` (regla de v6) | 0.479 |
| NIN=12, los 4 códigos de situación disjuntos dos a dos | **0.0001** |
| NIN=12, `code(A\|A) ∩ code(A\|B) == 0` | 0.159 |

Decisión tomada con ese dato: **la condición de rechazo en C2 será `code(A|A) ∩ code(A|B) == 0`**, no
"los 4 disjuntos". Justificación de principio (no de conveniencia): la regla de v6 no exige que todos los
códigos sean disjuntos, exige que **las dos situaciones que necesitan valores distintos no compartan celdas**.
En el mundo temporal las dos situaciones con valores distintos son A|A (−3) y A|B (+1); B|A y B|B tienen
valor idéntico (0) y por tanto no piden separación. Exigir los 4 disjuntos, además, con aceptación 1/10.000
produciría una KW fuertemente sesgada y no representativa.

Lo único que se miró antes del preregistro fue esa tabla y el número de mordidas de `datos/baseline_v6.csv`
(≈400 mordidas / 100k pasos con aprendizaje) para verificar que hay volumen de datos suficiente.
**No se corrió ninguna simulación del mundo temporal antes de escribir esto.**

---

## 1. Hipótesis

**H1 (la pregunta central).** La regla local de 2L —dividir una celda de Kenyon cuando su |error de predicción|
medio supera θ=0.6, desplazando a la hija hacia `P − mu[c]`, o sea hacia *lo distintivo de la situación actual*—
**descubre sola** que la información relevante está en un canal (el temporal) que al inicio no usa, si y solo si
el mundo hace que lo distintivo esté ahí. Es decir: produce composición temporal sin que nadie se lo indique.

**H0 (refutación).** La regla solo reorganiza el canal que ya usa; la dimensión temporal permanece con peso ~0,
los códigos de A|A y A|B siguen siendo el mismo, y el valor de A no se separa. La composición temporal
requiere que se le ponga a mano.

---

## 2. Mundo que exige orden (`mundo_temporal.py`)

Idéntico a v6/v7 en cuerpo, patas, política, hambre, muerte y renovación. **Lo único que cambia es la tabla de valor.**
El valor de morder depende de qué se mordió antes (`last` = tipo del último objeto **mordido**, no visto):

| situación | R | ΔE |
|---|---|---|
| morder A con `last == B`  (**A\|B**, "comida") | **+1.0** | +0.8 |
| morder A con `last == A`  (**A\|A**, "veneno") | **−3.0** | −0.4 |
| morder B (cualquier `last`) (**neutro**)        | **0.0**  | +0.1 |

- `last` se inicializa a `'B'` (una sola mordida de 100k queda afectada; se documenta).
- `last` **no se reinicia con la muerte del cuerpo** (coherente con "muerte del cuerpo sin olvido" de v6).
- Objetos 50/50 A/B, `nobj=4`, `L=40`, renovación 0.003, `costo=.002`, `T=100000`, semillas 1..20.
- B es el "preparador": +0.1 de energía lo hace mordible pero no es recompensa en sí (R=0 ⇒ W_B → 0).

**Requisito de diseño 50/50** (se verifica, no se asume): en la ventana temprana (t<5000), con W≈0 las
probabilidades de morder A y B son casi iguales ⇒ la fracción de mordidas de A precedidas por B debe estar
en [0.40, 0.60]. **Si no lo está, el mundo está mal diseñado y se reporta como tal.**

---

## 3. Seis brazos. Una sola diferencia entre cada par consecutivo.

| brazo | entrada Kenyon | KW columnas temporales al inicio | plasticidad 2L | papel |
|---|---|---|---|---|
| **C1**  | 6 (solo patrón actual) | — | NO | Control v6. Condición 1 del encargo. |
| **C1p** | 6 | — | **SÍ** | Control: ¿ayuda dividir cuando NO hay canal temporal? Debe decir que no. |
| **C2**  | 12 `[actual, último mordido]` | aleatorias U(0,1), rechazo hasta `code(A\|A)∩code(A\|B)=0` | NO | Techo. Condición 2 del encargo: ¿es resoluble? |
| **C2b** | 12 | **exactamente 0 (ciego al orden)** | NO | **Control de instrumento: debe reproducir C1 campo a campo.** |
| **C3**  | 12 | **exactamente 0 (ciego al orden)** | **SÍ** | **LA PREGUNTA.** Única diferencia con C2b: la plasticidad. |
| **C3C** | 12, mitad temporal **aleatorizada** (patrón A/B al azar, sin información; el mundo sigue usando el `last` real para el valor) | exactamente 0 | SÍ | **Control de artefacto**: el clip en 0 del KW hace que la división solo pueda AÑADIR peso temporal. Si C3C sube igual que C3, la subida no es descubrimiento. |

Alineación del RNG: C1, C1p, C2b, C3 y C3C sortean `KW` como `(NK,6)` (las columnas temporales se añaden a cero),
de modo que consumen exactamente el mismo flujo del RNG y **C1 ≡ C1p ≡ C2b ≡ C3 ≡ C3C hasta la primera división**.
C3C usa un RNG separado (`seed+100000`) para el canal falso, para no desalinear el principal.
C2 sortea `(NK,12)` y por tanto tiene otro flujo; es un techo de factibilidad, no un par comparable celda a celda.

---

## 4. Métricas

Por corrida (20 semillas, medianas y rango [min,max] SIEMPRE, nunca solo medias):

1. `W_AB`, `W_AA`, `W_BA`, `W_BB` = `(Wp−Wn)·kenyon(situación)` al final. **Separación** `sep = W_AB − W_AA`.
   En C1/C1p vale **0 por construcción** (mismo código), y eso es el punto.
2. `solap_A` = `|code(A|A) ∩ code(A|B)|` por cuarto. 3 = ciego al orden, 0 = representación separada.
3. **Acierto de orden** `acc = n(A|B) / (n(A|B)+n(A|A))` por cuarto.
4. **`base`** = fracción de *todas* las mordidas del cuarto cuyo mordisco anterior fue B.
5. **`lift = acc − base`** ← **métrica primaria de conducta**.
6. `splits`, `celdas`, paso de cada división, estímulo, y **`frac_temp`** = fracción L1 del vector de división
   `P − mu[c]` que cae en las columnas temporales. `t_pool` = paso en que se agota el pool (o None).
7. `w_temp`, `w_inst` = suma de KW en columnas temporales / instantáneas, sobre celdas activas y sobre la unión
   de los 4 códigos; por cuarto. `rho = w_temp/(w_temp+w_inst)`.
8. `Rtot` (suma de R), muertes, mordidas por situación y por cuarto, visitas por cuarto.

### Por qué `lift` y no `acc` — trampa de instrumento anticipada (regla 5)
`acc` **sola no sirve**: en C1, si el organismo aprende que A es malo en promedio, muerde A poco; entonces la
mayoría de las mordidas son de B y la mayoría de las mordidas de A caen justo después de una de B **por pura
frecuencia marginal**, sin ninguna representación del orden. Cálculo previo: con W_A≈−1, p(morder A)≈0.09 y
p(morder B)≈0.84 ⇒ `acc ≈ 0.90` en un organismo que es *demostrablemente ciego al orden*.
Por eso la métrica primaria es `lift = acc − base`, que vale 0 exactamente cuando la política no condiciona en la historia.

---

## 5. Predicciones numéricas

### C1 (control v6) — predicción: **NO lo resuelve**
- `sep = W_AB − W_AA = 0.00` **exactamente** (mismo código Kenyon ⇒ mismo W). Es una identidad, no un resultado.
- `solap_A = 3` en los 4 cuartos, 20/20.
- **`lift_q4` mediana < 0.05**, y ≤2/20 semillas con `lift_q4 > 0.10`.
- **Predicción adicional derivada, no obvia:** `W_A` **no converge**. Hay realimentación
  valor→política→frecuencia→valor: `W_A* = 1 − 4·f_A` con `f_A = pA/(pA+pB)`, `pA = σ((1.2·W_A+2h+0.5)/0.3)`.
  Iterando el punto fijo: 0.3→0.456→0.163→0.532… la pendiente del mapa es >1 en valor absoluto ⇒ **el punto fijo
  es inestable y W_A oscila**. Por tanto **no** predigo "W_A ≈ −1 estable": predigo mediana de `W_A` en [−3,+1]
  con **rango intercuartílico > 1.0** entre semillas (inestabilidad), frente a IQR ≈ 0 de v6 en su mundo normal
  (W_A = 1.00 en 20/20). *(El encargo sugería predecir W_A ≈ −1; se deja constancia de que la predicción se
  cambia ANTES de correr y por qué.)*
- **Si C1 sí lo resuelve** (`lift_q4 > 0.15`), es el hallazgo del experimento y se investiga primero.
  Ruta conocida por la que podría pasar: **la energía E ya es una memoria temporal escalar**. Aviso honesto:
  la afirmación "el organismo es puramente instantáneo" es falsa en sentido estricto. Pero E no dice *qué* se
  mordió, solo *cómo salió*, y empuja en la dirección equivocada: tras A|A (veneno, −0.4) el organismo queda
  **más** hambriento y por tanto **más** propenso a morder otra A ⇒ E sesga `lift` hacia **negativo**.
  Predicción refinada: `lift_q4` en C1 será ≤ 0.05 y **posiblemente negativo**.

### C1p (6 entradas + plasticidad) — predicción: **divide mucho y no sirve de nada**
- `splits > 0` en 20/20 (el error es crónico y no hay forma de bajarlo). Probablemente agota el pool (celdas=90).
- `sep = 0.00` 20/20, `solap_A = 3` 20/20, `lift_q4 < 0.05`. `Rtot` no mejor que C1 (diferencia de medianas < 10%).

### C2 (entrada temporal a mano, sin plasticidad) — predicción: **lo resuelve**
- Mediana `W_AB ≥ +0.80`; mediana `W_AA ≤ −2.00`; `sep ≥ 2.8` en **≥18/20** semillas.
- `lift_q4` mediana **≥ 0.30**.
- Mordidas A|A en Q4 < 30% de las de Q1.
- `Rtot` mediana claramente mayor que C1.

### C2b (12 entradas ciegas, sin plasticidad) — predicción: **idéntico a C1**
- **Criterio de instrumento, binario: C2b debe coincidir con C1 en `W_AB`, `W_AA`, mordidas por cuarto,
  muertes y `Rtot`, campo a campo, en las 20 semillas.** Si no coincide, hay un bug y todo lo demás
  queda en suspenso hasta arreglarlo.

### C3 (12 entradas ciegas + plasticidad) — LA PREGUNTA
**Veredicto SÍ ("la regla descubre sola la dimensión temporal") si y solo si se cumplen las cuatro:**

1. **Representación:** mediana de `solap_A` final **≤ 1** (de 3), y **≥15/20** semillas con `solap_A ≤ 1`.
2. **Valor:** mediana de `sep = W_AB − W_AA` **≥ 1.0**.
3. **Conducta:** mediana de `lift_q4` **≥ 0.15**.
4. **No es artefacto:** el control C3C **no** cumple 1–3 (≤5/20 semillas cumplen el punto 1).

**Veredicto NO (refutación) si falla cualquiera de 1, 2 o 3, o si C3C las cumple igual que C3.**
Resultado intermedio posible y se reportará como tal: representación sí (1) y conducta no (3), o al revés.

**Modo de fallo anticipado antes de correr (para que no se lea como excusa a posteriori):**
`mu` arranca en **cero**, no en el patrón medio. Con `ema=0.02`, tras las ~15 mordidas que hacen falta para que
`err` cruce θ=0.6, `mu` solo ha recorrido el 26% del camino. Entonces `dist = P − mu` tiene componente
instantánea ≈ 0.74·PAT_A, **mayor** que la componente temporal (±0.5 en 4 columnas). Las primeras divisiones se
gastarán empujando en la dimensión instantánea, que **no separa nada** (A|A y A|B tienen la misma mitad actual).
Solo cuando `mu` converge, `dist_inst → 0` y `dist_temp → ±0.5`, la división apunta exactamente a lo temporal
(cálculo: `mu_temp → (1, .5, .5, .5, .5, 0)`, `PAT_B − mu_temp = (0,−.5,+.5,−.5,+.5,0)`; la hija gana peso en las
columnas de "antes B" y la madre en las de "antes A" — **esto es literalmente el descubrimiento buscado**).
Con `NKMAX=90` hay 60 divisiones disponibles. **Si el pool se agota antes de que `mu` converja, el fallo es de
capacidad, no de dirección.** Se mide `t_pool` y `frac_temp` por división para poder distinguirlo. Si eso ocurre,
**el veredicto preregistrado sigue siendo NO**; un diagnóstico con pool mayor se reportará etiquetado
explícitamente como POST-HOC y sin valor confirmatorio. No se recalibra θ, ema, paso ni NKMAX.

### C3C (canal temporal aleatorizado) — predicción: **sube el peso temporal pero no sirve**
- `rho_q4 > 0` (el clip en 0 garantiza crecimiento neto aunque la dirección sea ruido) pero
  `solap_A` mediana = 3 o 2, `sep` mediana < 0.5, `lift_q4 < 0.05`.
- Es la prueba de que "el peso temporal creció" **no** es por sí solo evidencia de descubrimiento.

---

## 6. Qué NO prueba este experimento
- No prueba composición de secuencias de longitud >1: la memoria es de **una** mordida.
- No prueba que el organismo represente "orden" de forma abstracta: representa un par (actual, anterior).
- Un `lift` alto no implica planificación: basta con no morder A cuando el estado temporal dice A.
- Nada de esto autoriza vocabulario de inteligencia general (regla 8).

## 7. Registro de procedencia
Cada CSV/JSON llevará cabecera con fecha, sha256 corto de `mundo_temporal.py` y `corre_3T.py`,
versión de Python (3.14.2) y NumPy (2.4.3) y los kwargs completos. 20 semillas 1..20, T=100000,
`multiprocessing.Pool` con `spawn` y guard `__main__`.

---

# ERRATA — añadida el 15 sep 2026 DESPUÉS de ver los resultados (regla 3)
El texto de arriba **no se ha modificado**. Se añaden aquí los errores cometidos al redactarlo.

**ERR-3T-01 — la predicción sobre `W_A` en C1 era errónea en su forma, no en su fondo.**
Predije que `W_A` oscilaría (IQR entre semillas > 1.0) por la realimentación valor→política→frecuencia.
Lo observado es otra cosa y más extrema: **`W_A = 0.000 exactamente en 20/20 semillas, IQR = 0**, porque
`Wp` y `Wn` **se saturan los dos en el techo** (3.0/celda = 9.0/código, medido: `Wp(A|A)=Wn(A|A)=9.00`
en 20/20) y su diferencia se anula. La oscilación sí existe, pero solo hasta t≈8.000: a T=3.000 medí
`W_A = −1.48`, cerca del −1 que el encargo sugería, y luego el sistema **se bloquea**. La parte falsable de
la predicción (C1 no separa: `sep = 0`, `solap_A = 3`, `lift_q4 ≈ 0`) se cumplió 20/20. No se recalibra nada.

**ERR-3T-02 — el criterio 4 (no-artefacto) de C3 estaba mal operacionalizado.**
Lo escribí como "el control C3C no cumple 1–3 (≤5/20 semillas cumplen **el punto 1**)", anclándolo en la
métrica **representacional** `solap_A`. Es un error de diseño del criterio: supuse que la división sería
selectiva, es decir, que separaría el canal temporal **solo si lleva información**. Los datos dicen que no:
C3C, cuyo canal temporal es ruido puro, separa los códigos **igual o más** que C3 (19–20/20 con `solap_A ≤ 1`).
El criterio, tal como lo escribí, es por tanto **insatisfacible por construcción** y no discrimina nada.
El discriminador real —que también estaba preregistrado, en los criterios 2 y 3— es **valor y conducta**:
C3C saca 0/20 en `sep ≥ 2.8` y 0/20 en `lift_q4 ≥ 0.15` en todas las variantes corridas.
Se reportan las dos lecturas. **El veredicto preregistrado con las constantes congeladas no cambia: NO**,
porque los criterios 1, 2 y 3 fallan por sí solos, 20/20.

**Nota sobre el requisito 50/50.** El análisis marcó C2 como "FUERA" (`acc_early = 0.734`). No es un fallo
del mundo: es que C2 ya está aprendiendo dentro de los primeros 5.000 pasos. Verificado con el control
correcto (`learn=False`, política fija, 10 semillas): `acc_q4 = 0.492–0.499` y `A|B / A|A = 691 / 684`
en todos los brazos. **El mundo es 50/50; el requisito se cumple.**
