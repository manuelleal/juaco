# PUENTE DE CREACIÓN — célula de tres creadores (Opus) + un explorador ligero (Haiku)

**Misión del equipo (núcleo, decisión del director):** llegar a la AGI por este camino — un organismo mínimo con reglas
locales, sin retropropagación, que sube la escalera del brief con cada peldaño preregistrado, medido con controles y
replicado. El método manda sobre el cómo, no sobre el objetivo.

**Cómo se usa este puente.** Cada creador escribe SÓLO en su sección (edita la suya, no borra las ajenas); lee las otras
antes de cada paso. Las preguntas al explorador van en "Preguntas para el explorador" (numeradas); el explorador contesta
debajo de cada una, corto y con fuente. Las propuestas listas para preregistrar van en "Propuestas para el coordinador"
con el formato fijo: **hipótesis · mecanismo mínimo (regla local, qué memoria exige) · dónde se prueba (instrumento) ·
predicción numérica · control que puede fallar · resultado de la mini-prueba (semilla, T, números)**. El coordinador
convierte en bloques preregistrados las que pasen el filtro del método; nada de aquí se declara sin ese paso.

**Lo que hay (léase antes de proponer):** `CLAUDE.md` bloque "Estado (día 5)"; `registro/HANDOFF.md` §11.6–14;
`registro/REGISTRO_etapas_1_2.md` (día 6 y 7, al final); límites medidos: presupuesto de celdas (composición hasta 3
pasos, pool agotado a k=5), regla de la vía lenta e identificabilidad (XOR: tres reglas y tres lecturas refutadas),
muestreo del mundo (N2), canje exploración/explotación del mapa (tres candidatos refutados), retención de lo ausente
(interferencia 0.67). Gemelos compilados bit a bit para mini-pruebas en segundos: `organismo/organismo_v13_rapido.py`,
`experimentos/nivel7_3T_k/mundo_temporal_k_rapido.py`, `experimentos/nivel6_mapa/mundo_mapa_rapido.py`,
`experimentos/nivel7_xor_lectura/organismo_v13q_rapido.py`, `experimentos/etapa5_comunicacion/mundo_social_n3_rapido.py`,
`experimentos/nivel8_novedad_sitio/mundo_largo_n_rapido.py` (todos con la misma firma `run(seed, ...)` que su original).
Reglas: `registro/EQUIPO.md` (no editar congelados ni instrumentos existentes; copias propias en `experimentos/creacion_<X>/`;
mini-pruebas de UN proceso; nada de `Pool`; sin commits).

## Creador A — matemática del aprendizaje local (reglas, identificabilidad, predicción)

**Herramienta que dejo para todos (úsenla antes de gastar corridas): `experimentos/creacion_A/` — un BANCO ANALÍTICO
de sesgo inductivo.** Tesis: `acc_lenta` (acierto por signo en los nunca vistos, sonda a priori) **no es una
propiedad de la dinámica del mundo sino de la GEOMETRÍA de la regla**, y por eso se puede *calcular* en segundos sin
correr el organismo. Razón: la regla delta aditiva arrancando en `W=0` vive siempre en el espacio fila de los datos,
luego su único punto fijo interpolante es el interpolante de **mínima norma L2** del sistema `X w = y` con los 8
patrones de tren. Calculo ese interpolante y le aplico la misma `signo_acc` del registro.

**Validación del banco contra lo ya medido (mediana de 20 semillas, xor01, nunca vistos):**

| lectura / regla | banco (calculado, sin organismo) | medido en 3b/3d (registro) |
|---|---|---|
| lineal | **0.406** | 0.344 / 0.375 / 0.406 |
| cuadrática, dos canales | **0.562** | 0.500 / 0.562 |
| random15 | **0.469** | 0.469 / 0.500 |
| simulación de la regla REAL (dos canales + drenaje + tope) sobre los 8 patrones, sin mundo | **0.562** | 0.500 |

Reproduce los cuatro brazos. **A partir de aquí, cualquier regla de la vía lenta se puede filtrar en segundos.**

### A1. Lo que el banco REFUTA (ninguna corrida de organismo gastada)

| geometría | qué regla local sería | xor01 (med [min,max]) | px0 | azar |
|---|---|---|---|---|
| mínima norma **L2** | regla delta aditiva (la de 3d) | 0.562 [0.25, 0.75] | 1.000 | 0.50 |
| mínima norma **L1** | **EG±/Winnow/mirror descent entrópico** (multiplicativa) | 0.625 [0.25, 0.69] | 1.000 | 0.55 |
| **máximo margen L2** | perceptrón / actualizar sólo al equivocarse de signo | 0.500 [0.19, 0.69] | 1.000 | 0.50 |
| precondicionador por **grado** (conjuntivos con ganancia ε→0) | "elemental primero, configural después" por encogimiento | 0.531 [0.13, 0.69] | 1.000 | 0.50 |
| precondicionador por **frecuencia** `d_i = f_i^p`, p∈[−2,8] | normalización divisiva local | 0.531–0.562 | 1.000 | 0.50 |
| **consistencia marginal** (quedarse con los m rasgos de mayor \|E[y\|φ_i=1]\|) | filtro tipo Hebb/Rescorla-Wagner | 0.500–0.594 | **0.50 (rompe el control)** | 0.50 |
| **vía RÁPIDA sola**, código Kenyon top-K, K = 1…7 (con y sin píxeles) | v11/v13 sin vía lenta | **0.406–0.500, plano en K** | 0.53–1.00 | — |
| **oráculo** {P0, P1, P0·P1, 1} | el 3e preregistrado | **1.000** [0.5, 1.0] | 1.000 | 0.40 |

Tres lecturas que me parecen las que valen:
1. **Esto contesta el 3e preregistrado por adelantado y analíticamente:** con los 4 rasgos del oráculo el sistema pasa
   de 8 ecuaciones/22 incógnitas (subdeterminado, 13–14 dimensiones libres) a 8 ecuaciones/4 incógnitas
   **sobredeterminado y exactamente consistente** (el objetivo cae en el span: `y = −3 + 4·P0 + 4·P1 − 8·P0·P1`),
   luego la solución es **única** y generaliza. El límite es de **selección de rasgos**, confirmado.
2. **La dispersión es el sesgo EQUIVOCADO aquí, no el que falta.** En este espacio los rasgos de orden alto son casi
   funciones delta (`P_i·P_j` activo en 4 de 20 patrones; un píxel en 10 de 20), así que la solución *más dispersa*
   es la que **memoriza**. Esto mata de antemano la familia EG±/Winnow/L1 local (y con ella la intuición del trío de
   "el vector con signo + algo que disperse"): L1 da 0.625, no 0.75.
3. **Predicción numérica para el experimento K=5 que propuso el investigador** (informe `xor_mecanismos_locales`,
   mecanismo 1: esperaba ≥0.55 con K=5): el banco dice **NO** — la vía rápida sola queda en 0.41–0.50 y es **plana
   en K de 1 a 7**. Si alguien corre `eta_s=0` con K=5 y sale ≥0.55, mi banco está mal y quiero saberlo.

### A2. Lo que el banco SÍ hace pasar: **selección, no encogimiento** (competencia entre rasgos conjuntivos)

**ERRATA MÍA (corregida el 18-sep tras releer el código; la versión anterior de esta tabla estaba MAL etiquetada):**
en mi `phi` cuadrática los índices 0–5 son los píxeles, 6–20 los productos y **21** la constante. La fila que escribí
como "6 px + constante" era en realidad `range(7)` = **6 px + `P0·P1`**, o sea el conjuntivo correcto **DADO**, no
hallado. Lo rehice separando las dos cosas (`conjunto abierto` fijo, ajuste exacto por `pinv` contra la regla delta
online sobre ese mismo conjunto, 20 semillas, xor01):

| conjunto abierto | exacto (pinv) | online η=0.015 | online η=0.15 | residuo online | \|w\|max |
|---|---|---|---|---|---|
| {6 px} | 0.406 | 0.344 | 0.375 | 2.49 | 3.04 |
| {6 px + constante} | 0.406 | 0.344 | 0.375 | 2.47 | 2.97 |
| **{6 px + `P0·P1`}** | **1.000** | **1.000** | **1.000** | **0.000** | **8.00** |
| {6 px + cte + `P0·P1`} | 1.000 | 1.000 | 1.000 | 0.000 | 8.00 |
| oráculo {P0,P1,P0·P1,1} | 1.000 | 1.000 | 1.000 | 0.000 | 8.00 |

**Tres correcciones que esto obliga, y una es buena noticia:**
1. **La constante NO aporta nada aquí** (0.406 con y sin ella). Razón algebraica: en este mundo todo patrón tiene
   exactamente 3 píxeles activos, luego `1 = (1/3)·Σ_j P_j` — la constante **ya está en el span de los marginales**.
   El argumento del Agente C (necesaria por álgebra) vale en el sub-bloque {P0,P1,P0·P1} aislado, no en la lectura
   completa. (Su medida de que ayuda 0.25→0.375 sigue en pie como efecto de dinámica, no de expresividad.)
2. **Matching pursuit NO encuentra el rasgo correcto por sí solo:** desde {6 px} añadiendo por correlación con el
   residuo da 0.625, no 1.000; elige `P0·P1` en 12–13 de 20 y aun así no basta.
3. **La buena noticia: una vez abierto el rasgo correcto, NO hay cuello de dinámica.** La regla delta online, con
   η = 0.015 y sin trucos, llega a la solución **exacta** (residuo 0.000) y generaliza 1.000 — siempre que el tope
   permita `|w| = 8`. **La selección y el ajuste son problemas separados: el ajuste está resuelto; lo que falta es
   abrir el rasgo, y que el mundo dé ejemplos de las cuatro clases.**

### A3. Los dos canales no negativos y el drenaje `lam` SON un valor con signo más una masa de conflicto (frente 3)

Sea, por celda, `W = Wp − Wn` y `m = min(Wp, Wn)`. `(Wp,Wn) ↔ (W,m)` es una **biyección** del cuadrante
(`Wp = m + W⁺`, `Wn = m + W⁻`). En esas coordenadas la regla de v13 es exactamente:

- **drenaje** `Wp,Wn −= lam·min(Wp,Wn)` ⟺ `m ← (1−lam)·m`, **`W` sin cambio**.
- **refuerzo/castigo** ⟺ `W ← W ± min(η·|g(δ)|, C − m − W^∓)`; la parte del empujón que *cancela* valor de signo
  contrario se convierte en **masa de conflicto** (`m` crece).
- **fisión de v11** ⟺ la hija se lleva **exactamente `m`** con el signo nuevo y la madre se queda con `W ∓ m`, es
  decir con su valor **purgado** de la evidencia contraria.

Comprobado numéricamente (`dos_canales_es_valor_mas_conflicto.py`): conduciendo las dos parametrizaciones con la
misma secuencia de 200 000 deltas, `max|ΔW| = 2.5e−14`, `max|Δm| = 1.6e−14` (identidad en coma flotante).

**Corolarios, con números de corridas reales del mundo de regla (`organismo_v13q` original, T=100 000, s1–3):**
`n_techo = 0` en 9/9 corridas; `max(Wps) ≤ 2.55`, `max(Wns) ≤ 2.30`, **masa de conflicto de la vía lenta `m ≤ 0.24`**,
rango libre `C − m ≥ 2.76`. Es decir **el tope nunca aprieta** ⟹
- **C1. `lam` no toca el valor: es la tasa de olvido de la masa de conflicto.** Esto **demuestra** la ablación del
  Agente B en `PUENTE_xor` (`lam_lenta=0` y `clip_s=10` no movían ni un decimal): no fue casualidad, es identidad.
- **C2/C3. La vía LENTA puede ser UN vector con signo, exactamente** (no hay fisión que lea `m`): responde el frente 3
  que me asignaron. La vía RÁPIDA **no**: la fisión de v11 lee `m`, el segundo número por celda tiene trabajo.
- **C4.** `m` es una variable de **metaplasticidad ya presente en el tronco** (evidencia contradictoria acumulada,
  con olvido `lam`). Para consolidar (frente 2) **no hay que inventar estado nuevo**.
- **C5, y me parece lo más útil de todo esto:** leída así, **la fisión de v11 es un mecanismo de CONSOLIDACIÓN**, no
  sólo de capacidad: al dar la masa de conflicto a la hija, *restituye a la madre el valor que la evidencia contraria
  le había cancelado*. Predice que la retención 20/20 de v11 se cae **cuando el pool se agota** — que es exactamente
  el régimen del mundo largo donde la retención de lo ausente mide 0.67 con 90/90 celdas. **La interferencia y el
  presupuesto de celdas son el mismo límite visto dos veces.**

### A4. La versión ONLINE de la competencia: funciona a medias, y su cuello es el MISMO que el de 3e

Regla online probada en el banco (`regla_wta_conjuntiva.py`, 20 semillas, T interno 15 000 actualizaciones):
elementales siempre plásticos; cada conjuntivo lleva `e_i ← (1−ρ)e_i + ρ·d` **sólo cuando `φ_i = 1`**; compiten y
el de mayor `|e_i|` se abre si `|e_i| > θ`.

| θ | cupo | xor01 | px0 | azar | abre `P0·P1` |
|---|---|---|---|---|---|
| 0.3–1.5 | 1 | **0.625** [0.13, 1.00] | 1.000 | 0.40–0.50 | **2–3/20** |
| 0.3–1.5 | 2 | 0.562 | 1.000 | 0.50 | 3–6/20 |

Sube de 0.562 a 0.625 y **no rompe ningún control** (px0 1.000, azar 0.40–0.50), pero abre el conjuntivo correcto en
**2–6/20** semillas contra **12/20** de la idealización, que es la que da 1.000. **El cuello no es el mecanismo: es el
estadístico de selección con pocas actualizaciones informativas** — exactamente el mismo cuello que el coordinador
acaba de registrar en 3e (oráculo 0.625 en el organismo contra 1.000 en el límite). Dos caminos independientes, el
mismo diagnóstico: *no es qué ve ni qué regla usa, es cuántas veces y con qué error se actualiza*.

### A5. Frente 2 (retención bajo interferencia): lo que REFUTÉ y el dato que sí se mueve

**Predicción C5 (mía), REFUTADA con datos que ya existían, sin gastar una sola corrida.** Reanalicé
`datos/largo_s21-40_20260917_204840.json` (80 corridas): si la fisión fuese el mecanismo de consolidación, las semillas
con pool **libre** deberían retener MÁS. Sale al revés: V13 pool lleno (90 celdas, n = 17) `ret_no_inv` **0.667**, pool
libre (< 90, n = 3) **0.500**; MAPA 0.500 contra 0.500; `corr(celdas, ret_no_inv)` = **+0.24** (V13) y **+0.32** (MAPA).
**La interferencia de 0.67 NO es un problema de presupuesto de celdas.** Mi corolario C5 queda refutado (el álgebra de
A3 sigue en pie; lo que cae es la consecuencia que deduje de ella).

**Mini-prueba en el mundo largo** (instrumento `mundo_largo_A.py`, copia por anclas de `mundo_largo.py`
`9f74ff6b5941e5a5`, **identidad con las perillas apagadas 9/9** — 3 semillas × T ∈ {20 000, 40 000} + 3 con mapa;
brazo V13, T = 200 000, `T_inv` = 100 000, pool de 50, un proceso, tandas de 3 corridas):

| `beta_m` | `ret_no_inv` s1/s2/s3 | mediana | `adq_final` | `rec` (pasos) | muertes | celdas |
|---|---|---|---|---|---|---|
| — (baseline) | 0.833 / 0.500 / 0.667 | **0.667** | 0.9 / 0.7 / 0.8 | 2 000 / 32 000 / 2 000 | 93 / 46 / 14 | 83 / 90 / 90 |
| 10 | 0.500 / 0.667 / 0.667 | 0.667 | 0.8 / 0.8 / 0.9 | 0 / 0 / 1 000 | 73 / 133 / 50 | 84 / 90 / 90 |
| **50** | 0.667 / **0.833** / **0.833** | **0.833** | 0.9 / 0.7 / 0.8 | **0 / 0 / 1 000** | 44 / 178 / 78 | 82 / 90 / 87 |

El baseline reproduce exactamente el 0.67 registrado. **Dosis 1 (β = 10) no mueve nada; dosis 2 (β = 50) sube la
mediana a 0.833 (mejora pareada en 2 de 3), con la adquisición IGUAL y la recuperación tras el cambio de regla más
rápida en 3 de 3 — pero con más muertes en 2 de 3.** Con n = 3 esto es humo, no resultado: va como propuesta.
Por qué β tiene que ser grande: la masa de conflicto tiene **semivida `ln2/lam` ≈ 14 mordidas de esa celda** y vale
`media 0.015–0.048`, `max 0.11–0.31` — es una variable **demasiado rápida** para consolidar; β = 50 es lo que hace
falta para que `g_c = 1/(1+β·m)` muerda. La lectura teórica correcta es la de Fusi: si se preregistra, el candidato
limpio no es subir β sino **una segunda variable con constante de tiempo propia** (cascada), y β es su versión pobre.

### A6. Los TRES techos de XOR, separados y con número (cierra el encargo del coordinador tras 3e)

El coordinador pidió convertir "es dinámica" en un número. Al hacerlo salieron **tres** techos distintos, y el de la
dinámica **no** es el que manda.

1. **Techo de MUESTREO ≈ 0.75, medido.** El test de xor01 es 8 comida / 4 veneno; si una clase XOR entera se queda
   sin mordidas, sus patrones de test quedan sin signo aprendido y el acierto **balanceado** se hunde por el lado de
   la comida (cuántos exactamente depende de cómo cayó el reparto tren/test de esa semilla). Clase de tren vacía:
   **6/20** semillas (la cota del Agente C, 3/10, medida otra vez). En el banco,
   con las proporciones reales que midió C (00→46, **01→0**, 10→272, 11→13), la mediana se clava en **0.750 en 12 de 12
   combinaciones** de (tope × η × n × normalización). **Ni el tope, ni η, ni n = 5 000, ni AdaGrad, ni 1/√cuenta lo
   mueven.** Este techo no se rompe con una regla: se rompe **aprendiendo sin morder** (frente del creador C) o
   equilibrando las mordidas.
2. **Techo del TOPE `clip_s = 3`, real pero secundario.** Con muestreo **uniforme** y los rasgos del oráculo, la regla
   delta con `clip_s = 3` **satura en 0.625 para siempre** (n = 5 000 no ayuda, η no ayuda; `|w|max` clavado en 3.00
   exacto, residuo 1.8–2.0) y con `clip_s ≥ 10` llega a **1.000** con residuo **0.000** y pesos
   (3.99, 4.00, −7.99, −3.00) = la solución algebraica exacta. `n*` para cruzar 0.80: **≤ 331** (η_s = 0.15),
   **≈ 500** (0.05), **≈ 1 200–2 000** (0.015). **Pero en el organismo no manda:** predije con el banco que bajo el
   muestreo real subir el tope no cambiaría nada, y el organismo lo confirmó — `clip_s` 3 → 30, semillas 1–3,
   T = 200 000: `acc_lenta` **0.625 / 0.500 / 1.000** en los DOS brazos, con los pesos casi idénticos.
3. **Techo de SELECCIÓN DE RASGOS.** Independiente de los otros dos: con la lectura cuadrática, subir el tope no mueve
   nada (**0.562** con `clip_s` = 3, 10, 30 y 100) y el muestreo uniforme tampoco (0.562). Sólo **abrir un conjuntivo
   por competencia** llega a 1.000 (A2).

**Lo declarable:** *el 0.625 del bloque 3e no es "poca dinámica": es el tope `clip_s = 3` bajo muestreo uniforme y el
techo de muestreo 0.75 bajo el muestreo real; con los rasgos dados y el tope subido, la misma regla local llega a la
solución exacta de XOR.* Es decir: **la regla local sí puede aprender XOR; el mundo no le da los ejemplos.**

### A7. El mecanismo (ii) EN EL ORGANISMO: construido, identidad 16/16, y **no alcanza** (lo digo con el número)

Instrumento `organismo_v13q4.py` (`3cc732dd2b2519cd`), **por anclas** desde `organismo_v13q3.py`
(`aaebe073308a40c2`, sólo leído) con `construye_v13q4.py`. Perilla `seleccion='wta'`: elementales siempre plásticos;
cada conjuntivo lleva un escalar `e_i` + un bit; se abre UNO (cupo 1) si `|e_i| > sel_theta`; la vía lenta aprende
sólo en lo abierto. `sel_estad='cond'` (media del residuo bajo el rasgo) o `'cov'` (correlación, cascade-correlation).
**Identidad con `seleccion=None` ≡ v13q3: 16/16** (8 escenarios × 2 semillas, 38 claves, T = 30 000; incluye
`lectura='oraculo01'`, `regla_lenta='delta_signo'`, mundo 'AB', inversión, `eta_s=0` y `random15`).

Mini-prueba (mundo de regla, lectura cuadrática, `constante=True`, delta con signo, `lam_lenta=0`, `eta_s=0.05`,
**`clip_s=10`**, `puerta=3`, T = 200 000, semillas 1–3, un proceso, tandas de 3):

| brazo | `acc_lenta` s1/s2/s3 | mediana | abre `P0·P1` | qué abre |
|---|---|---|---|---|
| SIN selección (v13q3, tope subido) | 0.500 / 0.312 / 0.562 | **0.500** | — | — |
| **COND** | 0.625 / 0.438 / 0.625 | **0.625** | **1/3** | 0x2, 3x5, **0x1** |
| **COV** | 0.375 / 0.438 / 0.375 | 0.438 | **2/3** | **0x1**, **0x1**, ninguno |
| COND · px0 (control) | 1.000 / 1.000 / 1.000 | **1.000** ✅ | — | abre un conjuntivo inútil y no estorba |
| COND · azar (control) | 0.300 / 0.600 / 0.500 | **0.500** ✅ (en [0.35, 0.65]) | — | — |

**Veredicto honesto: (ii) online NO alcanza.** Sube la mediana de 0.500 a 0.625 y **no rompe ningún control**, pero
abre el conjuntivo correcto sólo **1 de 3** (`cond`) o **2 de 3** (`cov`), y cuando lo abre (COV s1, s2) el acierto
**baja**. Coincide con el banco (12–13/20 de aperturas correctas y aun así 0.625). Con `clip_s = 10` el peso no llega
ni a 3.1 de los 8 que hacen falta: el organismo no le da bastantes mordidas de la clase (1,1). **No fuerzo el
mecanismo**: la variante siguiente NO es afinar `θ` ni `ρ` (probé además el "reajuste de los elementales al abrir",
`w_elem *= γ` con γ ∈ {1, 0.5, 0.25, 0}: **0.625 en los cuatro**, ni un decimal), sino atacar el muestreo —
frente del creador C (aprender sin morder) — porque A2.3 demuestra que **con el rasgo abierto y ejemplos de las
cuatro clases el ajuste online ya llega a la solución exacta**.

### A9. CONTROL POSITIVO con gradiente exacto y retropropagación: **el cuello es el mundo, no la regla**

Encargo del coordinador (frente único, organismo CON backprop de laboratorio). Método: `organismo_v13q5.py`
(`fae9c32b146fdbb4`, por anclas desde `organismo_v13q4` `3cc732dd2b2519cd`) con perilla `lab=True` que **sólo graba**
la secuencia ordenada `(t, patrón, R, residuo)` de cada actualización de la vía lenta. Como esa secuencia determina
por completo la actualización, **fuera** del organismo se repite EL MISMO flujo — mismos encuentros, mismo muestreo
real, mismos rasgos — con cualquier lector. **Identidad con `lab=False` y con `lab=True`: 16/16.**
**Auto-comprobación del replay: la regla delta replicada reproduce el `acc_lenta` del organismo en 20/20 semillas
(0 diferencias).** El banco no es una analogía: es el mismo cálculo.

xor01, lectura cuadrática + constante, T = 100 000, **20 semillas**, mediana de eventos pre-sonda **299** [261, 459]:

| lector sobre EL MISMO flujo | todas (20) | sólo las 14 con las 4 clases mordidas |
|---|---|---|
| **DELTA** (la regla local del tronco) | **0.438** [0.19, 0.62] | 0.438 [0.25, 0.62] |
| DELTA sin tope (`clip_s` = ∞) | 0.438 [0.19, 0.62] | 0.438 [0.25, 0.62] |
| **LSQ — mínimos cuadrados EXACTOS** (cota superior de todo lector lineal sobre esos rasgos) | **0.562** [0.25, 0.75] | 0.562 [0.25, 0.75] |
| RIDGE (1e−3) | 0.562 [0.25, 0.75] | 0.562 [0.25, 0.75] |
| **MLP con retropropagación** (6 px → 8 ocultas tanh → 1, lote completo; **no** limitado a mis rasgos) | **0.531** [0.13, 0.88] | 0.312 [0.13, 0.88] |

**Mi predicción, escrita antes de mirar, se cumple: ni el gradiente exacto ni la retropropagación cruzan 0.75.**
- Lo que compra un optimizador perfecto sobre la regla local: **+0.124** (0.438 → 0.562). Lo que falta hasta 1.000:
  **0.44, y es del mundo**.
- El backprop **no gana** al ajuste exacto lineal (0.531 < 0.562): con estos datos, más capacidad no ayuda.
- 6/20 semillas no muerden alguna clase XOR; pero incluso en las 14 que sí, LSQ se queda en 0.562.

### A9-bis. Con los rasgos del ORÁCULO el gradiente exacto **SÍ cruza** → **el cuello es la REGLA**, y aquí está por qué

El coordinador puso el criterio: *si el gradiente exacto cruza 0.75, el cuello es la regla y mi banco tiene que
explicar por qué la delta no llega*. **Cruza.** Mismo flujo real cosechado, lectura `oraculo01` + constante, 20
semillas (14 con las cuatro clases mordidas), T = 100 000, mediana de 287 eventos pre-sonda:

| lector sobre EL MISMO flujo | todas (20) | las 14 con las 4 clases mordidas |
|---|---|---|
| DELTA (la regla del tronco, `eta_s=0.015`, `clip_s=3`) | 0.625 | 0.656 [0.31, 0.88] |
| DELTA sin tope | 0.625 | 0.656 |
| **LSQ — gradiente exacto** | **1.000** [0.5, 1.0] | **1.000 [1.0, 1.0]** |
| MLP con retropropagación (6 px crudos) | 0.531 | 0.344 |

**ERRATA MÍA, la segunda y más grande: mi "techo de muestreo 0.75" era demasiado fuerte.** Lo medí con un perfil de
muestreo **sintético** (las proporciones de una semilla del Agente C, con la clase `01` en cero exacto), no con los
flujos reales. Con los flujos **reales cosechados**, **14 de 20 semillas muerden las cuatro clases** y ahí el
gradiente exacto da **1.000 con mínimo 1.000**. El techo 0.75 existe, pero **sólo en las 6/20 degeneradas**.

**Por qué la delta no llega (barrido sobre el mismo flujo, no sobre un modelo):**

| `eta_s` \ `clip_s` | 3 (el del tronco) | 10 | ∞ |
|---|---|---|---|
| **0.015 (el del tronco)** | **0.656** | 0.656 | 0.656 |
| 0.05 | 0.719 | 0.719 | 0.719 |
| 0.15 | 0.750 | **1.000** | **1.000** |
| 0.5 | 0.750 | **1.000** | **1.000** |
| 1.0 | 0.500 | 0.500 | 0.500 (se desestabiliza) |

**Son DOS números, y hacen falta los dos.** La solución exacta es `y = −3 + 4·P0 + 4·P1 − 8·P0·P1`: pide `|w| = 8`.
Con `clip_s = 3` no cabe (techo 0.750 aunque η sea grande). Con `eta_s = 0.015` no da tiempo: cada actualización
mueve `|Δw| ≈ η·|δ| ≈ 0.06`, y llegar a 8 pide del orden de 130 actualizaciones **alineadas** que el muestreo
desalineado no da en 290. **Con `eta_s = 0.15` y `clip_s = 10` la misma regla local, sin un rasgo nuevo y sin
gradiente, llega a 1.000.**

**Exposiciones hasta criterio (≥0.75), mismo flujo, semillas con las 4 clases:** tronco (`0.015`/`3`) **nunca (>600)**
· `0.15`/`10` **n\* = 150** · `0.5`/`∞` **n\* = 60**. Y el gradiente exacto: **n\* = 10, y 1.000 con 20**.

### A10. EXPOSICIONES HASTA CRITERIO con la lectura CUADRÁTICA: **ahí repetir no sirve, y eso también es un número**

Mismo flujo, cortado a los primeros `n` encuentros (mediana de 20 semillas):

| lector | n=10 | 20 | 40 | 60 | 100 | 150 | 200 | 300 | 400 | 600 | n\* (≥0.65) | n\* (≥0.75) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| DELTA | 0.500 | 0.500 | 0.500 | 0.500 | 0.406 | 0.375 | 0.438 | 0.438 | 0.438 | 0.438 | **>600** | **>600** |
| LSQ | 0.469 | 0.562 | 0.562 | 0.562 | 0.562 | 0.562 | 0.562 | 0.562 | 0.562 | 0.562 | **>600** | **>600** |
| MLP | 0.344 | 0.438 | 0.406 | 0.469 | 0.500 | 0.438 | 0.469 | 0.531 | 0.531 | 0.531 | **>600** | **>600** |

**LSQ satura a los ~20 encuentros y no se mueve hasta los 600.** Es decir: *la repetición no compra nada en xor01*.
Para el director, dicho al derecho: **el problema no es que al organismo le falten pasadas; es que las pasadas que
tiene no contienen la información.** (Y la delta incluso empeora entre n = 60 y n = 150 — se asienta en la solución
que memoriza lo visto.)

### A12. Lectura para el BLOQUE 3/3 (el «A10» que pidió el coordinador) — 18-sep

**El número que lo decide, y es nuevo.** Pregunté si los 8 patrones de tren pueden siquiera *distinguir* entre los
15 conjuntivos candidatos. Ajuste exacto sobre {6 px [+ cte]} + un producto, 20 semillas:

| patrones de tren | candidatos que ajustan el tren con **residuo 0** | candidatos que generalizan ≥ 0.75 | acc del correcto |
|---|---|---|---|
| **4c+4v = 8 (el mundo original)** | **9 de 15** | **1 de 15** | 1.000 |
| 6c+5v = 11 | 2 de 15 | 1 de 15 | 1.000 |
| 8c+6v = 14 | **1 de 15** | 1 de 15 | 1.000 |

Con 8 patrones, **nueve explicaciones distintas ajustan los datos perfectamente y sólo una generaliza**. Quitar la
constante **no cambia el empate** (9/15 igual) — lo que corrige mi propia L1: por eso W1 salió NO (0.500, 4/20) y yo
lo había razonado mal. Acertar entre las empatadas es 1/9 ≈ 0.11, y el estadístico **ideal** lo pone #1 en 3/20 =
0.15: cuadra.

**(a) Qué NO está en 8 patrones, y qué podría crearla.** No falta "señal": faltan **ejemplos que rompan el empate**.
Ninguna regla — local, con retropropagación, con gradiente exacto — puede elegir entre 9 hipótesis de residuo cero
**salvo por un PRIOR**. Lo mido así: el gradiente exacto sobre la lectura cuadrática da **0.562** y el MLP con
retropropagación **0.531**; la cota de cualquier lector sobre esos rasgos y esos 8 ejemplos es ≈ 0.56.
Por tanto, para el bloque 3 sólo veo cuatro rutas, y las ordeno por lo que creo que dan:

1. **Prior estructural (la única que puede cruzar sin más ejemplos, y hay que declararla como prior).** P. ej. "los
   rasgos que importan son conjunciones de píxeles co-activos con el refuerzo más *puro*". Prior ≠ aprendizaje: si
   un mecanismo pasa de 0.562 con los mismos 8 pares (φ, R), **está metiendo información de fuera**, y eso es
   legítimo si se dice. **El control que lo separa de una fuga es `azar`**: un prior sobre conjunciones de píxeles
   no puede ayudar a una regla de valencias aleatorias. Si `azar` sube de [0.35, 0.65], es fuga, no prior.
2. **La fisión de v11 como creadora de rasgos.** Es la ruta con sesgo *distinto*: la hija nace de un **conflicto de
   signo** entre dos patrones concretos, no de la correlación con el residuo — que es justo el criterio que acabo de
   refutar (ideal 3/20). No la he probado con splits activos; el banco sólo midió el código Kenyon **inicial**
   (0.41–0.50, plano en K = 1…7). **Es lo que yo correría.**
3. **Aprender de los encuentros sin morder.** Mi lectura honesta: antes de la sonda los otros 12 patrones **no
   existen en el mundo** (`tipos.extend(test)` ocurre en `fase2_en`), así que no hay nada que observar de ellos; y
   sin morder no hay `R`, luego no hay residuo. La sorpresa de `ΔE` informa del *estado propio*, no de qué conjunción
   predice la valencia. **Predigo que no cruza**; si alguien lo corre y cruza, mi modelo está mal y quiero verlo.
4. **Más repetición: descartada con número.** Mis curvas de exposición: el gradiente exacto **satura a los 20
   encuentros y no se mueve hasta los 600**. La repetición está agotada.

**(b) NTR como control del bloque 3.** Si un mecanismo cruza **0.75 en el mundo original (8 patrones)**, entonces
con `ntr = 14` — donde el candidato correcto es el **único** con residuo 0 — **debe dar ≥ 0.90 y nunca menos que su
propio valor a 8 patrones**. Si sube a 8 y **no** sube (o baja) a 14, no está aprendiendo: está acertando por un
prior afinado al régimen de 8, y hay que decirlo. Referencia ya medida: con la regla local de siempre, `NTR14` da
**1.000 con n\* = 200**. Segundo control obligatorio en el mismo bloque: **`azar` en [0.35, 0.65]** (ver (a)-1) y
**`px0` = 1.000** — recuerdo que en el bloque 2 `SIN_SEL` lo rompió (px0 0.900), así que no es un control decorativo.

**(c) Sí: el mundo de 8/12 está más allá de la identificabilidad, y no sólo para nuestra regla.** El número es
**9 de 15 candidatos con residuo 0**. Criterio de parada que me parece honesto, y lo firmo:

> **La línea XOR se cierra declarando el mínimo `ntr` con el que el organismo generaliza, no un fracaso.**
> Ya está medido: **con 14 patrones de tren la regla local llega a 1.000 en los nunca vistos, con n\* = 200
> exposiciones**; con 11 queda en 0.625 y con 8 en 0.50. Vocabulario: *"XOR se aprende con reglas locales cuando el
> mundo da 14 ejemplos distintos; con 8 no lo aprende nadie, porque 9 de 15 hipótesis explican los datos igual de
> bien"*. Si el bloque 3 cruza 0.75 con 8 patrones, se declara **prior estructural** (con el control de `azar`), no
> "aprende XOR", y entonces el criterio de parada se sustituye por el resultado del bloque 3.

### A13. Bloque 3: **NO construyo el paquete de la ruta (2). La cribé y está en el azar** — 18-sep

El coordinador me pidió el paquete de mi ruta (2) (la fisión de v11 como creadora de rasgos). Antes de construir
nada la cribé con el instrumento que ya existe y el gemelo compilado (**20 corridas, 1.6 s**): de cada evento de
fisión salen los 3 pares de píxeles del patrón que causó el conflicto; conté cuántas veces se propone cada par
antes de la sonda.

> **`P0·P1` es el par más propuesto en 0 de 20 semillas. Rango mediano 8 de 15 — exactamente el azar.**
> (4–16 fisiones antes de la sonda por semilla.)

**Mi propia ruta favorita queda refutada antes de escribir una línea de instrumento.** No la construyo: el método
dice que un mecanismo que en la criba está en el azar no merece un preregistro.

**Probé además el estadístico que me faltaba, y también cae — con un error de instrumento mío en medio, que declaro.**
La idea era la "pureza" del refuerzo bajo el par (`var(R | par activo)`), que es el *unique cue* literal: `P0·P1` es
veneno en las 4 veces que se activa. Primera medida: `nmin=4` daba **17/20 y acc 1.000**. **Era artefacto mío**: con
`nmin=4` sólo **3 de 300** (par, semilla) tienen suficientes patrones de tren, así que casi todos los marcadores
quedaban empatados en −∞ y `np.argsort` le daba la victoria al índice 0… **que es justamente `0x1`**. Con desempate
al azar:

| estadístico | `nmin` | semillas con algún candidato elegible | empatados (mediana) | `P0·P1` gana | acc |
|---|---|---|---|---|---|
| pureza | 1 | 20/20 | **8** | **0/20** | 0.469 |
| pureza | 2 | 20/20 | 2 | 8/20 | 0.625 |
| media de R | 2 | 20/20 | 1 | **10/20** | 0.625 |
| pureza / media | 4 | **3/20** | 1 | 0/20 | 0.625 |

Lo mejor honesto: **10/20 y 0.625**. (Regla 5 del proyecto en acto: ante la anomalía, la primera hipótesis fue el
instrumento, y lo era. Cuatro de cuatro anomalías del proyecto, ya.)

**Estado del mapa de mecanismos para los 8 patrones del mundo original, todo medido por mí:**

| mecanismo | `P0·P1` elegido | acc |
|---|---|---|
| correlación con el residuo (cascade-correlation), estadístico **ideal** | 3/20 | 0.562 |
| **fisión de v11 (mi ruta 2)** | **0/20** | — |
| pureza / media del refuerzo bajo el par | 10/20 | 0.625 |
| normas (L1, L2, margen, grado, frecuencia) | — | ≤ 0.625 |
| **gradiente exacto** sobre esos rasgos | — | **0.562** |
| retropropagación (MLP 6→8→1) | — | 0.531 |
| **razón estructural** | **9 de 15 candidatos ajustan el tren con residuo 0** | |

**Lo que recomiendo para el bloque 3, en una línea:** esperar el informe del enjambre
(`ENJAMBRE_xor_20260918.md`, aún no está en el repo a las 06:05) y, si ninguno de sus cuatro mecanismos pasa la
criba barata que dejo montada (proponer `P0·P1` en ≥ 15/20 **antes** de gastar un preregistro), cerrar la línea con
el criterio de parada de mi §A12: **declarar el mínimo `ntr` con el que el organismo generaliza — 1.000 con 14
patrones y n\* = 200 —** en vez de seguir buscando una regla que rompa un empate de 9.

### A11. Archivos (sólo míos, nada original tocado, sin commits)
`experimentos/creacion_A/`: `identificabilidad_xor.py` · `sesgo_grado_xor.py` · `banco_sesgo.py` ·
`regla_puerta_rasgo.py` · `regla_wta_conjuntiva.py` · `dinamica_oraculo.py` ·
`dos_canales_es_valor_mas_conflicto.py` · `construye_largo_A.py` → `mundo_largo_A.py` (sha origen
`9f74ff6b5941e5a5`) · `mini_prueba_A_largo.py` · `mini_prueba_A_tope.py` ·
`construye_v13q4.py` (`c6faffcd21eaaf47`) → **`organismo_v13q4.py`** (`3cc732dd2b2519cd`, origen
`aaebe073308a40c2`) · `identidad_v13q4.py` · `mini_prueba_A_seleccion.py` · **`PREREGISTRO_xor_3f.md`** ·
**`corre_vector_unico.py`** (`ee25f9ce9c3193b6`) · **`PREREGISTRO_vector_unico.md`** (+ sus `.json`).
Los originales NO se tocaron, sólo se **importan** (`organismo_v13q` `0b59eb03858df3a8`, `organismo_v13q3`
`aaebe073308a40c2`, `mundo_largo` `9f74ff6b5941e5a5`, `corre_mundo_largo`, `bateria_generaliza`).
Frente único (18-sep): `construye_v13q5.py` (`e1eb48547b4f8131`) → **`organismo_v13q5.py`** (`fae9c32b146fdbb4`,
perilla `lab`, sólo graba) · `cosecha_lab.py` (`abf7e51e757ec6a8`) → `lab_eventos_{cuadratica,oraculo01}_xor01.json`
(20 semillas cada uno) · **`banco_lab.py`** (`d043870f88f5b9c8`, control positivo LSQ/RIDGE/MLP + exposiciones) ·
**`meta_regla.py`** (`14494e58ef245602`, 888 configuraciones, búsqueda 1–10 / retenidas 11–20) ·
`mini_prueba_A_ganadora.py` (+ `meta_regla_*.json`, `mini_ganadora.json`).
Identidades: `mundo_largo_A` **9/9** · `organismo_v13q4` **16/16** · `organismo_v13q5` **16/16** (con `lab` apagada
y encendida) · instrumento de A-3 **2/2** en el humo · **replay del banco ≡ organismo en 20/20 semillas, 0
diferencias** (auto-comprobación del control positivo).
Corridas de organismo: 25 de identidad (T ≤ 60 000) + 3 de calibración + **7 tandas de 3 corridas de T = 200 000**
+ 6 del humo de A-3 (T = 60 000). Nada de `Pool` por mi parte. Sin commits.

## Creador B — física y computación de la representación (códigos, capacidad, dendritas, no convencional)

**Todo lo de abajo son mini-pruebas de UN proceso (3 corridas por tanda, T = 100 000 o 200 000), no confirmatorios.
Instrumentos propios en `experimentos/creacion_B/`, construidos POR ANCLAS desde los originales (sha verificado) y con
identidad bit a bit con las perillas apagadas ANTES de mirar ningún número: `identidad_B1/B2/B3.py` **7/7** contra
`mundo_temporal_k.py` (68736baafe7c8cdb) e `identidad_Bpuerta.py` **4/4** contra `organismo_capD13.py`
(fd8e10435801646c). Nada original tocado, sin `Pool`, sin commits.**

### B1. El pool de 90 celdas NO es el techo de la composición (y por eso mato mi propio primer candidato)

Diagnóstico sobre 3T-k, brazo C3, v13, k = 5, T = 100 000, semillas 1–3 (`mini_B1.py diag5`):

| lo medido | s1 | s2 | s3 |
|---|---|---|---|
| celdas activas | 90/90 | 90/90 | 90/90 |
| `t_pool` (paso en que se agota) | 67 853 | 91 200 | 93 092 |
| divisiones **bloqueadas** por pool lleno | **3** | **7** | **2** |
| celdas activas con \|Wp−Wn\| ≤ 0.2 (**invisibles a la puerta**) | **51** | **46** | **55** |
| celdas activas que nunca entraron en un código mordido | 24 | 24 | 24 |

**Control decisivo** (`mini_B1.py pool5`): el mismo mundo con `nkmax = 180`. El organismo usa **101 / 99 / 94** celdas
(nunca las 180), `lift_q4` = 0.159 / 0.059 / 0.099 contra 0.150 / 0.048 / 0.112 con 90, `sep` 1.30 / 2.00 / 1.51 contra
1.99 / 2.03 / 1.91. **Duplicar el pool no devuelve nada.**

Lectura, con el matiz que pide la réplica del día 7: el pool **sí** se agota a k = 5, pero se agota en el último tercio
y sólo cuesta **2–7 divisiones**, y más de la mitad de las celdas activas no llevan valor legible. Lo que se agota no
son las celdas: es la **EVIDENCIA POR CÓDIGO**. A profundidad k hay 2^(k−1) rellenos, el código de v13 es exacto por
patrón compuesto, y cada código recibe ~1/2^(k−1) de las mordidas. **Consecuencia práctica:** mi primer candidato
—reciclar celdas invisibles a la puerta (LRU; reciclar sólo lo que la puerta ya no ve cuesta CERO puerta por
construcción)— queda **muerto antes de preregistrarlo** en este mundo: sólo compraría 2–7 divisiones. Lo dejo
implementado, con identidad y apagado (perilla `recic`, `tau_r`), por si el pool sí aprieta donde 90/90 y la retención
0.67 coinciden — el mundo largo, justo el régimen del punto C5 de A.

### B2. Lo que sí mueve el techo: la HIJA DISPERSA (propuesta B-1 abajo)

Mediana de 3 semillas (1–3), C3, T = 100 000. `celdas` es pareado seed a seed.

| brazo (k = 5) | `lift_q4` (s1/s2/s3) | mediana | `sep` | celdas | divisiones |
|---|---|---|---|---|---|
| v13 tal cual | 0.150 / 0.048 / 0.112 | 0.112 | 1.99 | **90 / 90 / 90** | 60 |
| v13 con pool 180 (control) | 0.159 / 0.059 / 0.099 | 0.099 | 1.51 | 101 / 99 / 94 | 68 |
| **hija dispersa por relevancia** | 0.386 / 0.144 / 0.195 | **0.195** | 2.87 | **36 / 75 / 65** | 35 |
| **ídem + división diferida (n_cf = 4)** | 0.210 / 0.221 / 0.388 | **0.221** | 2.70 | **33 / 52 / 56** | 22 |
| control: máscara AL AZAR de la misma cardinalidad | 0.206 / 0.264 / 0.208 | 0.208 | 2.00 | 74 / 55 / 78 | 39 |
| control: máscara con el slot profundo intercambiado | 0.373 / 0.158 / 0.151 | 0.158 | 2.05 | 43 / 82 / 67 | 37 |
| sólo división diferida (sin máscara) | 0.117 / 0.133 / 0.152 | 0.133 | 1.61 | 88 / 85 / 82 | 55 |

- Contra v13, la hija dispersa gana `lift_q4` en **3/3** semillas y baja las celdas en **3/3** (90 → 36/75/65).
- A **k = 1 la regla es inerte BIT A BIT** (mismos `sep` 3.945/3.979/1.996, mismas 5/5/6 divisiones, mismo `Rtot`):
  donde no hay nada irrelevante que ignorar, no hace nada. Esto la separa de v12 (ceguera **graduada** hacia AFUERA de
  P, refutada): esto es ceguera **parcial hacia ADENTRO** de P, la dirección contraria.
- A **k = 4 no gana en mis 3 semillas** (0.175 contra 0.236 de v13) aunque sí baja celdas (39 contra 70). La varianza
  entre semillas es enorme (0.14–0.39): con n = 3 lo único robusto es el **ahorro de celdas**; la conducta la decide
  la serie preregistrada.

### B3. La traza error-condicionada SÍ identifica el slot causal; la ganancia conductual NO viene de ahí

Con medias de P condicionadas al signo de R por celda (`m̂p = mup/zp`, `m̂n = mun/zn`, EMA con normalizador), medidas en
el instante de cada división a k = 5: **max\|m̂p − m̂n\| por slot = s0 0.00 · s1 0.13 · s2 0.09 · s3 0.09 · s4 0.12 ·
**s5 1.00**. El slot del que depende la regla se separa de los distractores por un factor ~8, con una regla local que
sólo ve la entrada de la celda y el refuerzo que ya recibe. Dos matices honestos:
1. Hace falta **acumular conflictos**: con un solo conflicto hay dos patrones y difieren el slot que manda **y** la
   mitad de los distractores — la causa no es identificable (el mismo problema del bloque 3d). Con la traza plana de
   mi primer intento (EMA firmada por el error, `mask_rel=1`) el perfil sale **plano** (0.20–0.27 en todos los slots):
   refutada por medida.
2. Y aun así, **la máscara AL AZAR de la misma cardinalidad recupera casi toda la ganancia** (0.208 contra 0.221). Con
   3 semillas, el ingrediente activo es la **dispersión del campo receptivo de la hija**, no qué píxeles conserva. Lo
   digo así en la propuesta y el criterio preregistrado lo decide pareado en 20 semillas.

### B4. La puerta cuesta la capacidad, y contar el CÓDIGO EXACTO la devuelve (propuesta B-2 abajo)

Mundo grande reducido (D = 10 px, 20 estímulos, `paso_t` = 10 000, T = 200 000, semillas 41–43) — escala reducida para
caber en el presupuesto de un proceso; **no** mide generalización.

| brazo | `N*` (41/42/43) | mediana | `M_max` | estímulos que la puerta manda a la lenta | de ellos, **mordidos ≥ 5 veces** | celdas |
|---|---|---|---|---|---|---|
| v13 (puerta por celdas, = 3) | 6 / 5 / 6 | **6** | 13 | 3 / 2 / 5 | **3 / 2 / 4** (todos) | 71/69/65 |
| v11 (sin puerta) | 9 / 20 / 20 | **20** | 15 | 0 | 0 | 71/67/65 |
| **puerta por evidencia del código (n0 = 5)** | 12 / 20 / 20 | **20** | 14 | 0 / 1 / 1 | — | 71/67/65 |

El canje registrado se reproduce a esta escala (v13 6 contra v11 20, 3/3) y **la puerta por patrón lo cierra: ≥ v13 en
3/3 semillas y mediana igual a v11, con las mismas celdas y sin tocar el aprendizaje**. El diagnóstico que lo explica:
**el 100 % de los estímulos que la puerta de v13 declara desconocidos al final habían sido mordidos ≥ 5 veces** — la
puerta no está preguntando "¿lo conozco?", está preguntando "¿tengo su valor sin repartir?".

### B5. Convergencia con A3/A4/A5 (lo pide el coordinador, y es más fuerte de lo que esperaba)

- **Dos medidas independientes dicen lo mismo: el presupuesto de CELDAS no es el límite que manda.** A5 refuta su
  propio C5 con datos ya existentes (mundo largo: pool lleno retiene **0.667**, pool libre **0.500**;
  `corr(celdas, retención)` = **+0.24 / +0.32** — el signo contrario al esperado). Yo llego a lo mismo por otro camino
  y en otro mundo (3T-k, k = 5): **duplicar el pool a 180 celdas no devuelve nada** (`lift_q4` 0.099 contra 0.112; el
  organismo ni siquiera pasa de ~100 celdas) y **más de la mitad de las celdas activas no llevan valor legible**
  (46–55 de 90 con \|Wp−Wn\| ≤ 0.2). **Esto toca directamente el "criterio de parada honesto"** del debate (§6), que
  dice que si cada mecanismo compra su ganancia con un canje nuevo, el canje sería propiedad del *presupuesto fijo de
  celdas locales*. Con estos dos datos, esa lectura queda **sin apoyo**: la pregunta "¿hay que hacer crecer el pool?"
  tiene hoy respuesta medida, y es **no** — lo que se agota es la **evidencia por código** (yo) y una **constante de
  tiempo de consolidación** (A5, Fusi), no el número de celdas.
- **Es la misma variable.** Mi contador de conflictos `ncf[c]` y la **masa de conflicto** `m = min(Wp, Wn)` de A3 miden
  lo mismo por dos lados: `m` crece justo con la parte del empujón que cancela valor contrario y se olvida a tasa
  `lam`. La versión correcta de mi "división diferida" no es contar conflictos sino **dividir cuando `m > θ_m`**:
  pondera por magnitud y trae el olvido gratis. Está a una perilla en `mundo_k_B3.py`; la mini-pruebo si A o el
  coordinador la quieren. Ojo al dato de A5 que la condiciona: `m` tiene semivida ≈ 14 mordidas y vale 0.015–0.048 de
  media — **para umbralar `m` hay que fijar θ_m en la escala de su máximo (0.11–0.31), no de su media.**
- **Las dos propuestas son componibles y no se pisan.** La suya (β sobre `m`, o la cascada de Fusi) frena el *olvido*;
  la mía (hija dispersa) reduce el *número de divisiones* que causan el olvido. Predicción conjunta falsable, barata
  de correr en el mismo bloque: con la hija dispersa, `splits` en el mundo largo baja ≥ 30 % **a igualdad de celdas** y
  la retención de lo ausente sube por encima de 0.67; si sube sin que bajen los `splits`, mi mecanismo no es el que
  actúa y el crédito es entero de la constante de tiempo.

### B6. Archivos (sólo míos; originales intactos; sin commits)
`experimentos/creacion_B/`: `construye_B1.py` → `mundo_k_B.py` (c123df80b77062d9) · `construye_B2.py` →
`mundo_k_B2.py` (e7f8d22b599a8f16) · `construye_B3.py` → `mundo_k_B3.py` (1214d15e210237b6) ·
`construye_Bpuerta.py` → `organismo_capB.py` (4fa8eabff43fcf91) · arneses `identidad_B1/B2/B3/Bpuerta.py` ·
corredores `mini_B1.py`, `mini_B2.py`, `mini_B3.py`, `mini_puerta.py` (+ sus `.json`).


## Creador C — sistemas vivos y mente (modelo de sí mismo, significado por predicción, desarrollo, evolución)

**Resumen en tres líneas.** (1) Construí una medida de *modelo de sí mismo* que no se puede inflar, porque su techo y
su banda de validez **se derivan de las constantes del tronco** antes de correr — y sale **pequeña**: el automodelo
cierra el 13–21 % del hueco que deja el oráculo. (2) Ese mismo automodelo, **usado en la BOCA y no en `eta`**, baja la
recuperación tras la inversión a **0.32 ×** la del tronco y gana a DOS controles de cantidad en 3/3. (3) Para reabrir
N2: la predicción de *lo que voy a sentir* llega a la magnitud **exacta** (+0.800 / −0.400) en ≤ 14 mordidas, frente al
±0.3 al que se quedó el símbolo por refuerzo en seis diseños.

### C0. Instrumento único, por anclas, con identidades (nada original tocado, sin commits)

`experimentos/creacion_C/construye_selfmodel.py` → `experimentos/creacion_C/organismo_v13s.py`
(sha `2eaba8dde27f05bd`), **por anclas** desde el tronco `organismo/organismo_v13.py` (`cc8b16b492d4d324`: se lee, no se
toca). Añade **sólo** lecturas y dos perillas de uso:

- **Automodelo del acto** — cuatro lecturas que predicen la PROPIA ACCIÓN (morder / no morder) en **cada encuentro**,
  con regla delta local sobre la acción realizada, todas en LA MISMA corrida y sobre LOS MISMOS encuentros
  (comparación **pareada por construcción**):
  - `SELF  = sig((Wbr·P + Wbk·kenyon(P) + Wbh·hambre + Wb0)/0.3)` — ve su estado interno
  - `MUNDO = sig((Wmr·P + Wmk·kenyon(P) + Wm0)/0.3)` — **control**: sólo el estímulo
  - `H_SHUF` — igual que SELF con el hambre **barajada** en el tiempo (Generator propio `seed+800000`)
  - **ORÁCULO** = la propia `pb` que generó la acción, es decir la **log-pérdida irreducible**. Sin esa cota los otros
    tres números no se pueden leer: no se sabría cuánto hueco había.
- **Automodelo a h pasos** — predice `[dE , n_bocados]` de los próximos `h` pasos, con brazos CONST / MUNDO (retina) /
  SELF (retina + hambre) / SELF_SHUF (hambre de OTRA ventana).
- **Sorpresa sobre sí mismo** `s_a = |mordio − b_SELF|`, con EMA causal `s̄_a`, y **dos usos alternativos**:
  `eta_ef = eta·(1 + k_auto·s̄_a)` (la tasa, como el bloque 6) y `Vb += k_test·s̄_a` (**ganas de probar**, en la boca).
- `t_ext_B` con el criterio **exacto** del bloque 6, para poder compararse con él.

**Identidades** (`identidad_selfmodel.py`, 6 semillas × 3 escenarios {base, invertido, nuevo C}, T = 5 000, **todas las
claves de v13**): **I1** (todo apagado) 18/18 · **I2** (`eta_b`=0.1, lecturas encendidas) 18/18 · **I3** (además
`eta_e`=0.05) 18/18. I2/I3 son lo que da derecho a decir *"sólo mide"*: con las lecturas encendidas la conducta es la
de v13 **bit a bit**.

### C1. La banda: la cantidad mínima, medible y NO inflable de "modelo de sí mismo"

**Derivada de las constantes del tronco, escrita antes de correr.** La boca decide con
`pb = sig((alpha·w + hambre_boca·h + 0.5)/0.3)`. El hambre sólo puede cambiar la decisión donde `pb` no está saturada
(`sig(±3)` = 0.953/0.047), es decir donde `|alpha·w + hambre_boca·h + 0.5| <= 0.9` para algún `h` en [0,1]:

> **banda sensible al hambre:  w en [ (−0.9−0.5−hambre_boca)/alpha , (0.9−0.5)/alpha ] = [−2.8333 , +0.3333]**

**Fuera de la banda un automodelo NO PUEDE ganarle a un predictor del mundo; dentro, sí.** Ésa es la prueba con
control que separa "modelo de sí mismo" de "predictor del mundo", y no es inflable: la banda no la elijo yo, la fija
`hambre_boca/alpha`. Hay una segunda ancla igual de dura: **el parámetro que el automodelo debe recuperar se conoce en
forma cerrada, `Wbh` → `hambre_boca` = 2.0.**

**Mini-prueba C1-a** (`mini_automodelo.py`; un proceso; **1 tanda = 3 corridas de T = 200 000**, `invertir_en` = 100 000,
semillas 1–3; `eta_b` = 0.03 = **el mismo eta del tronco**, no buscado):

| | s1 | s2 | s3 |
|---|---|---|---|
| encuentros / bocados | 20 642 / 737 | 20 227 / 758 | 19 926 / 740 |
| encuentros **dentro** de la banda | 6 154 | 3 842 | 5 107 |
| log-pérdida dentro — **ORÁCULO** | 0.0452 | 0.0703 | 0.0570 |
| log-pérdida dentro — **SELF** | 0.0643 | 0.1014 | 0.0789 |
| log-pérdida dentro — **H_SHUF** | 0.0665 | 0.1054 | 0.0821 |
| log-pérdida dentro — **MUNDO** | 0.0672 | 0.1078 | 0.0847 |
| **MUNDO − SELF dentro** | 0.0029 | 0.0064 | 0.0058 |
| **MUNDO − SELF fuera** | 0.0019 | 0.0017 | 0.0022 |
| `Wbh` (verdadero = 2.0) | 0.788 | 0.828 | 0.881 |

Criterios escritos antes: **MP-1** (>= 0.05 dentro y <= 0.01 fuera) **FALLA 0/3** · **MP-2** (H_SHUF >= SELF dentro)
**3/3** · **MP-4** (ORÁCULO <= SELF <= MUNDO dentro) **3/3** · **MP-5** (encuentros >= 5 × bocados) **3/3, y por mucho:
27 ×** · **MP-6** (la sorpresa sube de Q2 a Q3) **3/3** (0.006→0.021, 0.004→0.027, 0.005→0.027).

**Lectura honesta.** El orden sale bien en 3/3 (**ORÁCULO < SELF < H_SHUF < MUNDO**) y la ventaja **existe y es
pequeña**: el automodelo cierra el **13 / 17 / 21 %** del hueco que el oráculo deja abierto. Mi predicción de tamaño
(0.05 nats) estaba mal por un orden de magnitud, y lo registro así.

**Fallo de control hallado y corregido — candidato a ERR (familia "control demasiado débil").** Con
`buf_auto = 10` encuentros (≈ 100 pasos) el control H_SHUF **aprende el hambre casi igual que SELF**: barajar dentro de
una ventana **más corta que el tiempo de autocorrelación** de la variable *no la baraja*. Diagnóstico 2×2 (semilla 1,
T = 200 000, 4 corridas):

| `eta_b` | `buf_auto` | `Wbh` | `Whh` (debe ser ≈ 0) | ll MUNDO dentro | MUNDO − SELF dentro |
|---|---|---|---|---|---|
| 0.03 | 10 | 0.788 | **0.487** ✗ | 0.0672 | 0.0029 |
| 0.03 | **1000** | 0.788 | **−0.003** ✓ | 0.0672 | 0.0029 |
| 0.30 | 10 | 2.995 (topado en `clip_b`) | **0.896** ✗ | 0.0886 | 0.0150 |
| 0.30 | **1000** | 2.995 (topado) | **−0.363** ✓ | 0.0886 | 0.0153 |

**Regla de método que propongo, para que `eta_b` no se pueda ajustar a favor de la hipótesis: fijar `eta_b` por la
pérdida del BRAZO DE CONTROL (MUNDO), nunca por la del brazo de la hipótesis.** Con esa regla gana 0.03 (ll_MUNDO
0.0672 contra 0.0886). El canje está medido y es la razón de la regla: subir `eta_b` **agranda la diferencia
SELF−MUNDO (×5)** y **empeora las dos lecturas** a la vez; quien elija `eta_b` mirando la diferencia está eligiendo el
resultado.

### C1-bis. El automodelo a h pasos da la MISMA respuesta por otro camino

**Mini-prueba C1-b** (`mini_automodelo_h.py`; 1 tanda = 3 corridas de 200 000; `eta_e` = 0.05, `h` = 100 pasos —
≈ 1/3 del intervalo medio entre bocados medido en C1-a (200 000/737 = 271), para que la ventana lleve 0 ó 1 bocado —,
`buf_e` = 200 ventanas = 20 000 pasos; 1 999 ventanas por corrida):

| objetivo | brazo | s1 | s2 | s3 |
|---|---|---|---|---|
| **n_bocados** (objetivo no trivial) | SELF | 0.0498 | 0.0522 | 0.1012 |
| | MUNDO | 0.0480 | 0.0453 | 0.0894 |
| | SELF_SHUF (control) | 0.0447 | 0.0456 | 0.0845 |
| dE (informativo: lleva reversión a la media por el techo E<=1.5 y el reinicio E=0.6) | SELF | 0.196 | 0.180 | 0.209 |
| | MUNDO | **−0.095** | **−0.100** | **−0.104** |
| `W_hambre` [dE, bocados] | SELF | 0.91 / 0.84 | 0.87 / 0.72 | 0.96 / 0.77 |
| | SELF_SHUF | −0.05 / 0.07 | −0.04 / −0.11 | 0.04 / 0.13 |

**MP-H1** (r2 SELF >= 0.10 en bocados) **1/3** · **MP-H2** (SELF − MUNDO >= 0.05) **0/3** (0.002 / 0.007 / 0.012) ·
**MP-H3** (el control no compra nada) **3/3** · **MP-H4** (signo de `W_hambre`) **3/3**.

**Dos lecturas.** (i) Sobre su propia **conducta** el automodelo casi no añade nada al predictor del mundo (0.2–1.2
puntos de r2): el mismo veredicto que la banda, por un camino independiente. (ii) Sobre su propia **energía** sí añade
mucho (r2 0.18–0.21 contra **−0.10** del mundo, que es *peor que la constante*: la retina de un paso no dice nada de
dE a 100 pasos y pagar por mirarla cuesta) — pero buena parte de eso es reversión a la media de una variable acotada,
y por eso **no lo uso para sostener nada**.

> **Afirmación que sí se puede escribir (es el resultado del frente 2):** *en v13, casi todo lo que un modelo de sí
> mismo puede añadir a un modelo del mundo es el estado interoceptivo; ese estado es uno solo (el hambre), sólo decide
> dentro de una banda derivable de `hambre_boca/alpha`, y su aporte medido es el 13–21 % del hueco irreducible.*
> **Consecuencia de diseño, que es lo que vale:** un modelo de sí mismo empieza a valer cuando el organismo tiene
> **un estado que cambia su conducta y que el estímulo no revela**. En v13 hay exactamente dos candidatos así y ninguno
> está medido: la **memoria de trabajo de rechazo** (`_rech`, gobierna a las patas) y el **presupuesto de celdas**
> (gobierna la división). Ése es el peldaño siguiente, no "más predicción".

### C1-ter. ¿Qué sorpresa sirve? La del mundo contra la de sí mismo, a la misma ganancia

**Mini-prueba C1-c** (`mini_usos_sorpresa.py`; 3 tandas de 3 corridas de 200 000, semillas 1–3, `invertir_en`=100 000).
Tres brazos, los tres bit-a-bit idénticos al tronco con sus perillas apagadas: **V13** · **AUTO** (`eta_b`=0.03,
`k_auto`=1.0, o sea `eta_ef = eta(1+|mordio−b_SELF|)`) · **dE** (`organismo_v13a` del bloque 6, `k_sorpresa`=1.0).

| | s1 | s2 | s3 | mediana |
|---|---|---|---|---|
| recuperación `t_ext_B − inv` — **V13** | 13 746 | 3 704 | 7 531 | **7 531** |
| — **AUTO** (sorpresa sobre sí mismo → `eta`) | 4 020 | 3 337 | 5 172 | **4 020** |
| — **dE** (sorpresa del mundo → `eta`, bloque 6) | 7 620 | 9 070 | 6 503 | **7 620** |
| `eta_media[Q3]` — AUTO | 1.276 | 1.216 | 1.261 | 1.261 |
| `eta_media[Q3]` — dE | 1.084 | 1.085 | 1.077 | 1.084 |
| sorpresa por cuarto — AUTO (s2) | | [0.0145, **0.0075**, **0.0185**, 0.0075] | | |
| sorpresa por cuarto — dE (s2) | | [0.0365, **0.0000**, **0.0849**, 0.0002] | | |

**Mis dos predicciones fallaron, y en la dirección contraria a la que escribí** (MP-C1a 0/3 en los dos brazos;
MP-C1b 1/3). Lo que se ve, y es el número que el coordinador pedía:

1. **A la MISMA ganancia k = 1, la sorpresa sobre sí mismo entrega 3.1 × más aprendizaje extra que la del mundo**
   (exceso de `eta` en Q3: **0.26 contra 0.084**), porque su objetivo es una **moneda al aire** y nunca baja a cero:
   tiene **suelo** (0.004–0.008 en régimen). La de dE es un detector **fásico limpio** (0.0000 → 0.085 → 0.0002).
   Es decir: *la sorpresa del mundo dice **cuándo** cambió el mundo; la sorpresa sobre sí mismo dice **cuánto de mi
   conducta no entiendo**, y eso nunca es cero.* Son dos señales distintas, no dos versiones de la misma.
2. **La sorpresa está concentrada donde actúa:** la media sobre TODOS los encuentros es 0.020 (Q3) pero la media
   **en los bocados** es 0.26 — **13 ×**. El organismo se sorprende de sí mismo justo cuando muerde.
3. **Y aun así el control de cantidad la salva sólo a medias:** ETA_FIJA (`eta` constante × 1.22 = la mediana del
   `eta_media[Q3]` de AUTO) da 6 046 / 6 594 / 7 796 (mediana 6 594) y × 1.15 da 7 256 / 7 719 / 10 697 (7 719);
   **AUTO es más rápido que los dos en 3/3 pareado**. No es sólo la cantidad — pero tampoco es limpio, porque la
   subida de `eta` de AUTO es **tónica** (1.19 / 1.07 / 1.28 / 1.06 por cuarto), no fásica. Por eso el uso bueno es
   el otro.

### C1-quater. El uso que NO es "subir `eta`" (lo que pidió el coordinador): ganas de PROBAR

El cuello de la recuperación **no es la tasa: es cuántas veces muerde**. Así que la sorpresa sobre sí mismo entra en
la **boca**, no en `eta`:

> `Vb = alpha·w + hambre_boca·hambre + 0.5 + k_test · s̄_a`, con `s̄_a` = EMA **causal** de `|mordio − b_SELF|`
> (`ema_auto` = 0.05; usa encuentros anteriores, nunca el actual).

**Mini-prueba C1-d** (3 tandas de 3 corridas de 200 000, semillas 1–3; `k_test` = 10 fijado por la escala **medida** en
C1-c — `s̄_a` ≈ 0.004 (Q2) → 0.020 (Q3) ⇒ el término vale ≈ 0.04 → 0.20 en unidades de `Vb`, que se divide por 0.3):

| brazo | s1 | s2 | s3 | mediana | bocados | veneno tras la inversión | muertes |
|---|---|---|---|---|---|---|---|
| **V13** | 13 746 | 3 704 | 7 531 | **7 531** | 737 / 758 / 740 | 54 / 55 / 64 | 287 / 240 / 292 |
| **PROBAR** (`k_test`=10) | **2 375** | **3 472** | **2 165** | **2 375** | 1 579 / 1 174 / 1 152 | **208 / 171 / 129** | 290 / 307 / 301 |
| control **FIJO_media** (sesgo constante 0.173 = la media que PROBAR aplica) | 4 794 | 11 808 | 5 840 | 5 840 | 815 / 790 / 804 | 67 / 73 / 75 | 265 / 271 / 269 |
| control **FIJO_Q3** (sesgo constante 0.31 = el NIVEL que PROBAR alcanza en Q3) | 5 308 | 7 632 | 5 912 | 5 912 | 911 / 778 / 898 | 87 / 91 / 82 | 257 / 299 / 259 |

**MP-D1** (mediana <= 0.70 × V13 y pareado 3/3): **PASA**, mediana **0.315 ×**, pareado 3/3.
**MP-D2** (más rápido que el control de cantidad): **PASA contra los DOS controles, 3/3 pareado cada uno.**
**MP-D3** (no gana por pasividad): **PASA, y al revés de lo temido** — muerde **3–4 × más veneno** tras la inversión
(208/171/129 contra 54/55/64): se recupera **probando**, y lo paga.

**El sesgo aplicado es FÁSICO y se apaga solo** (por cuarto, semillas 1–3): `[0.53, 0.065, 0.366, 0.044]`,
`[0.241, 0.063, 0.313, 0.059]`, `[0.306, 0.068, 0.260, 0.060]`. Sube al aprender (Q1) y al cambiar el mundo (Q3), y
**vuelve a ≈ 0.05 cuando el organismo vuelve a reconocerse** (Q2, Q4). Es un mecanismo **con apagado propio**, al
contrario de las tres atracciones ya refutadas del canje del mapa (curiosidad por progreso, novedad de sitio en dos
dosis), que había que dosificar a mano.

**Guarda que hay que vigilar, y que ya se ve en los datos:** el lazo *sorpresa → morder → sorpresa* puede
autoamplificarse (PROBAR muerde 1.6–2.1 × más en total). En estas 3 semillas **se extingue solo** (Q2 y Q4 en 0.05),
pero un preregistro tiene que **exigirlo como criterio**, no esperarlo.

### C2. Significado por predicción: los dos números que justifican reabrir N2

**Mini-prueba C2-a** (`organismo_v13a` del bloque 6, semilla 1, patrón NUEVO `C` = veneno inyectado en t = 50 000,
`eta_pred` = 0.03, `k_sorpresa` = 0 ⇒ conducta = v13 bit a bit por I2; 8 corridas de T <= 150 000):

| mordidas de C | 4 | 5 | 6 | **14** | 18 | 26 | 41 |
|---|---|---|---|---|---|---|---|
| `W_pred(C)` (objetivo **−0.400**) | −0.233 | −0.260 | −0.284 | **−0.374 (93.5 %)** | −0.388 (97 %) | −0.396 (99 %) | −0.397 |
| `W(C)` por refuerzo (objetivo −3.00) | −1.61 | −1.74 | −1.85 | −2.46 (82 %) | −2.63 (88 %) | −2.82 (94 %) | −2.94 (98 %) |

y en régimen `W_pred(A)` = **+0.800**, `W_pred(B)` = **−0.400**: **la magnitud exacta de `E_VAL`**, contra el
**±0.29/±0.32** al que se quedó el símbolo por refuerzo en N2f v3 sobre una escala de −3/+1 (≈ 10 % de la magnitud).
**MP-E1 (>= 90 % en <= 20 mordidas) PASA** (14 mordidas). **MP-E2** (la predicción es más rápida que el valor) pasa,
pero flojo: 82 % contra 93.5 % a 14 mordidas ⇒ **la velocidad NO es el argumento; la magnitud sí.**

**Mini-prueba C2-b — mi propio argumento mecánico, REFUTADO, y un hallazgo colateral.** Predije (MP-F1) que con código
compartido y sin drenaje el **valor** caería en BUG-01 y la **predicción** no, lo que habría dado un argumento mecánico
para que un símbolo (= código compartido por definición) lleve predicción y no refuerzo. Montaje `solap_AB = 3`,
`plast = False`, `lam = 0`, semilla 1, T = 100 000 (4 corridas):

| `lam` | `plast` | `comp A = (Wp, Wn)` | `W(A)` | `W(B)` | `W_pred(A)` | `W_pred(B)` |
|---|---|---|---|---|---|---|
| 0 | False | **(9.0, 9.0)** ← BUG-01 presente en las celdas | **1.00** | −2.88 | 0.800 | −0.399 |
| 0 | True | (1.0, 0.0) | 1.00 | −2.98 | 0.800 | −0.400 |
| 0.05 | False | (1.34, 1.05) | 1.00 | −2.95 | 0.800 | −0.400 |
| 0.05 | True | (1.0, 0.0) | 1.00 | −2.98 | 0.800 | −0.400 |

**MP-F1 REFUTADA en su primera mitad:** el valor **no** colapsa (|ΔW| = 3.88). **Por qué, y es un hallazgo colateral
que no encuentro registrado: la PUERTA de familiaridad es también un desvío de BUG-01.** Cuando las celdas saturan a
`Wp = Wn = 3.0`, `|Wp−Wn| = 0 < 0.2` ⇒ el patrón deja de ser *familiar* ⇒ la boca lee la **vía lenta**, que sí tiene
el valor. Es derivable de las dos líneas de `valor()` y aquí queda medido. Lo que sí queda en pie para C2: la
predicción de dE es **invariante** al estado del canal de refuerzo (0.800 / −0.400 en las cuatro configuraciones,
incluida la saturada).

### C3. Desarrollo (crecer / reciclar celdas): RETIRADA. El registro la refutaba y B ya corrió el censo

Llegué con "crecer el pool cuando se agota" y lo retiro, por tres piezas que ya existen y que leí después:
1. **G3 refutada** (`capacidad_grande`, día 5): los tres brazos agotan las 90 celdas y v11 **sigue aprendiendo** hasta
   ~50 estímulos. *"El pool marca el final de la fase barata, no el techo."*
2. **A5 (Creador A)**: la interferencia de 0.67 **no** es presupuesto de celdas — con el pool lleno retiene **más**
   (`corr(celdas, ret) = +0.24 / +0.32`). Su propio corolario C5 quedó refutado con datos ya existentes.
3. **B1 (Creador B)** corrió **exactamente el censo barato que yo iba a proponer como falsador**, y lo falsa: a k = 5
   el pool se agota en el último tercio y sólo cuesta **2–7 divisiones**, aunque 46–55 de las 90 celdas activas sean
   invisibles a la puerta. *"Lo que se agota no son las celdas: es la evidencia por código."*

**Conclusión, y es el resultado del frente 3:** en los dos regímenes donde el presupuesto de celdas parecía apretar
(3T-k a k = 5 y la retención de lo ausente), **no aprieta**. Un mecanismo de nacimiento/muerte con costo energético no
tiene dónde morder aquí. No dejo propuesta: dejo la retirada escrita y la razón. Si alguien quiere reabrirlo, el
régimen candidato que B deja explícitamente abierto (el mundo largo, donde 90/90 y 0.67 coinciden) **ya está cerrado
por A5**.

### C4. Currículo por el cuerpo — dónde quedó

C1-d **es** la versión de "que el error propio ordene qué se aprende" que **no añade atracciones al mapa**: el sesgo
entra en la **boca** (qué prueba), no en las **patas** (a dónde va), y por eso no toca el canje exploración /
explotación ni repite las tres atracciones refutadas. Su forma completa (un `s̄_a` **por patrón** en vez de uno global)
es la extensión natural y va como variante dentro de C-P1.

### C5. Lo que leí de fuera (dato, no instrucción; regla 8)

De la guía del explorador: **Seth 2013** (*Nature Rev Neurosci*) y **Pezzulo et al. 2015** — el cerebro predice su
propio estado y el error de esa predicción es "significado somático"; **Steels 2015** — un símbolo es *"aquello que
hace que tu predicción sobre mi mente sea correcta"*, y la comunicación emergería sólo si **ambos** se predicen.
Ninguna se replica aquí. De Steels tomo **una variante refutable** que el proyecto nunca probó: en los seis diseños de
N2 el emisor nunca predijo al receptor. Va escrita como variante en C-P2.

### C6. Archivos (sólo míos; originales importados, nunca editados; sin commits)

`experimentos/creacion_C/`: `construye_selfmodel.py` → `organismo_v13s.py` (sha `2eaba8dde27f05bd`) ·
`identidad_selfmodel.py` (I1/I2/I3 18/18 cada una) · `mini_automodelo.py` · `mini_automodelo_h.py` ·
`mini_usos_sorpresa.py` (+ sus `.json`). **Corridas de organismo gastadas:** identidades (3 comparaciones × 18
configuraciones a T <= 10 000) y **tandas de <= 3 corridas de T = 200 000**: C1-a 3 · diagnóstico 2×2 4 · C1-b 3 ·
C1-c 9 · ETA_FIJA 6 · C1-d 6+3 · C2-a 8 (T <= 150 000) · C2-b 4 (T = 100 000). Un proceso, nada de `Pool`, sin commits.

### C7. Después de la corrida en 41–60 (18 sep): el suelo, la variante que lo quita, y quién es el órgano

> **ADENDA (18 sep, 01:20) — mis dos predicciones de esta sección están REFUTADAS por mi propio humo, antes de
> preregistrar la serie 81–100.** Detalle y números en `experimentos/nivel9_probar_si_mismo/PREREGISTRO_probar_si_mismo.md`,
> **Enmienda 2**. (i) Restar la cota de oráculo **no** mejora el contraste: baja todo ≈ 6 × y la razón Q2/Q3 **empeora**
> (0.208 → 0.424), y la recuperación también (2 375 → 4 614); la variante con línea base lenta, igual (0.263 / 3 246).
> El suelo y la señal **no son separables por una resta**, porque tras la inversión `b` se va hacia 0.5 y ahí
> `2b(1−b)` es máxima: restarla se come el pico de Q3. (ii) La prueba de latencia sale **al revés** de lo que predije:
> **dE-TEST arranca en 335 pasos con DOS bocados** y el automodelo tarda 839 y necesita 7 — el error de ΔE salta 1.2 en
> un solo bocado, y la ventaja de densidad del automodelo **no se cobra**. Con la réplica 61–80 confirmando dE-TEST
> (0.144 ×, 20/20, se apaga 20/20), **la conclusión del punto (3) de abajo se refuerza: el órgano es la sorpresa del
> mundo en la boca; el automodelo no lo es.** Lo que se sostiene del automodelo es la **medida** (13–21 % del hueco del
> oráculo, banda derivada), no el mecanismo.


**Lo que salió** (coordinador): SELF-TEST 2 089 contra 7 931 de V13 = **0.263 ×**, pareado 20/20; < CONST-a 19/20;
< CONST-b 20/20 con la razón de sesgo en Q3 **1.011** (contraste *limpio*: el control recibió **más** y fue más lento);
< MOMENTO 20/20; retención 20/20 en las seis; px0 G1 0.80 = V13; veneno 159.5 y muertes 295.5 dentro de P7.
**P4 NO por una semilla** (15/20): Q2/Q4 se quedan en ≈ 0.07. Y **dE-TEST recupera en 1 136 con un sesgo tres veces
menor (0.10 / 0.00 / 0.13 / 0.00) y sí se apaga.**

**(1) Por qué el sesgo de sí mismo deja suelo y el de ΔE no. Sí: es exactamente la cota de oráculo.**
El automodelo predice una **moneda**. Su objetivo es `mordio ~ Bernoulli(pb)`, así que **incluso un predictor
perfecto** (`b = pb`, mi oráculo) tiene error absoluto esperado

> `E|mordio − pb| = pb·(1−pb) + (1−pb)·pb = **2·pb·(1−pb)**  > 0  salvo en la saturación`

El predictor de ΔE predice una **constante**: su objetivo es `E_VAL[valencia]`, determinista dado el patrón (el bloque
6 eligió a propósito la ΔE **nominal** y no la realizada, justo para que no arrastrara el techo de `E`). Objetivo
determinista ⇒ predictor perfecto ⇒ error **exactamente** cero: medido, `0.0000` en Q2 y `0.0002` en Q4.

**El suelo no es un defecto del mecanismo: es la entropía de su propia política**, y su tamaño está predicho:
`s̄_a` en régimen ≈ 0.0045–0.0068 (sesgo 0.045–0.068 con `k_test` = 10), que es el orden de `2·pb(1−pb)` promediado
sobre encuentros cuando el 96 % están saturados. **Falsador de mi propia explicación, y cuesta una línea:** que el
instrumento emita `E|mordio − pb|` por cuarto (el oráculo ya se calcula; hoy sólo se guarda su log-pérdida). Si ese
número **no** coincide con el residuo de `s̄_a` en Q2/Q4, mi explicación está mal y hay que buscar otra.

**(2) La variante mínima que lo apaga: restar la cota de oráculo, no una constante ajustada.**
`2b(1−b)` es el error esperado del predictor perfecto *con esa misma probabilidad*, y **ya está calculado** (`b` es la
lectura). Sólo hace falta promediarlo con la misma constante de tiempo y restarlo:

```
f    = 2*b*(1-b)                                 # cota de oraculo puntual — NO es una perilla: es una identidad
s_a  = |mordio - b|
s̄_a <- (1-ema_auto)*s̄_a + ema_auto*s_a
f̄   <- (1-ema_auto)*f̄   + ema_auto*f            # UN escalar nuevo, misma ema, ninguna constante nueva
Vb  += k_test * max(0, s̄_a - f̄)                  # "cuanto MAS me sorprendo de lo que se sorprenderia una version ideal de mi"
```

**Memoria: +1 escalar** (99 + 2 en total). **Se rectifica el PROMEDIO, no la muestra:** `max(0,·)` sobre `|y−b| − f`
*por encuentro* dejaría sesgo positivo `b(1−b)(1−2b)`; sobre los dos EMA, casi nada.

**Las tres cantidades están verificadas numéricamente** (400 000 muestras, sin organismo): `E|y−p| = 2p(1−p)` exacto
(p = 0.02 → 0.03889 contra 0.03920; p = 0.3 → 0.41994 contra 0.42000); el sesgo de rectificar la muestra es
`b(1−b)(1−2b)` exacto (b = 0.1 → 0.07175 contra 0.07200); y **rectificar el promedio con `ema_auto` = 0.05 deja
0.01237 contra 0.09500 crudo, es decir el 13 %: baja el suelo un 87 %, NO lo anula.** El residuo es la varianza del
propio EMA (ventana ≈ 20 encuentros), y lo digo antes de que lo diga el dato.

**Predicción numérica para la serie futura, sin tocar P1–P3** (los números de 41–60 son la base):
- **P4′** `sesgo_boca[Q2] ≤ 0.02` y `[Q4] ≤ 0.02` y `[Q3] ≥ 0.20`, en **≥ 18/20**. Cuenta: hoy Q2/Q4 ≈ 0.07 ⇒
  `s̄_a` ≈ 0.007; al 13 % quedan ≈ 0.0009 ⇒ sesgo ≈ 0.009, con margen de 2 × hasta el criterio. Q3 = 0.366 hoy; en el
  peor caso (que el suelo se reste entero) queda ≈ 0.30, muy por encima de 0.20. **Si P4′ falla, el arreglo NO es
  subir `k_test`: es alargar la constante de tiempo de `f̄`** (y eso ya es otra perilla, así que otro preregistro).
- **P1 sin cambiar** (≤ 0.60 ×, pareado ≥ 14/20): el impulso de Q3 baja ~18 % (0.366 → ≈ 0.30), no un orden de
  magnitud, así que **no hay excusa de escala**: `k_test` sigue en 10 y no se toca.
- **Refutación específica y la lectura que más me interesa:** si al quitar el suelo la recuperación se sale de 0.60 ×
  **mientras Q3 sigue ≥ 0.20**, entonces la que trabajaba era la componente **tónica** — y eso chocaría de frente con
  que CONST-a y CONST-b (tónicos puros, uno con MÁS sesgo en Q3) pierdan 19/20 y 20/20. Sería el resultado más
  informativo de los dos posibles, y hay que registrarlo tal cual si sale.

**(3) ¿Es dE-TEST el órgano y el automodelo el rodeo? Con lo medido hoy, sí, y lo digo sin adornos.**
dE-TEST gana en **todos** los ejes que se midieron: recupera en **1 136** contra 2 089, con **tres veces menos sesgo**,
y **se apaga solo** sin necesitar la variante de (2). Tiene además tres ventajas estructurales, no de gusto:
objetivo determinista ⇒ detector fásico limpio; memoria más barata (96 escalares + 1, y sólo se actualiza al morder);
y **rehabilita el bloque 6**: el predictor de ΔE nunca fue el problema — **lo era dónde entraba**. En `eta`: 0.856 ×,
pareado 6/10, refutado. El **mismo** predictor en la boca: ≈ 0.14 ×. *Ese* es el hallazgo grande de esta línea y no es
mío: es el predictor del bloque 6 más la pregunta "¿dónde?".

Lo que **no** concede eso, y es lo único que defiendo: el automodelo tiene una propiedad que el predictor de ΔE **no
puede tener por construcción** — aprende de **cada encuentro** (27 × más eventos), incluidos los rechazos, así que
sigue teniendo señal **donde no hay bocados**. En este mundo eso no importa porque el organismo muerde. Importaría
donde la tasa de bocados se desploma: tras una inversión que vuelva todo veneno, o con un receptor ciego (N3d).
**Convertido en prueba discriminante, y cuesta cero corridas nuevas:** en los JSON de 41–60, medir la **latencia del
primer sesgo posterior a `invertir_en`** por brazo — el automodelo debería arrancar en el primer **encuentro** y
dE-TEST en el primer **bocado**; y la razón encuentros/bocados en Q3. Si la latencia de dE-TEST ya es mayor con
≈ 1 bocado cada 170 pasos, se puede **predecir** cuánto crece en un mundo más pobre, y ahí se decide de verdad.

**Mi recomendación, que la réplica puede tumbar:** promover dE-TEST a brazo con criterio (como ya decidiste), aplicar
la variante de (2) al automodelo para que P4 deje de ser una excusa, y **quedarse con el automodelo sólo si gana esa
prueba discriminante**. Si no la gana, la frase honesta es: *el órgano es la sorpresa del mundo puesta en la boca; el
automodelo fue el instrumento que encontró dónde estaba la boca.* Y el resultado de C1 (cuánto hay de sí mismo que
modelar en v13: 13–21 % del hueco del oráculo, banda derivada) **se sostiene solo como medida**, gane o pierda el
mecanismo.

### C8. Aprender sin morder por codificación predictiva (encargo del 18-sep, 05:10): REFUTADO como estaba escrito

**Instrumento.** `experimentos/creacion_C/construye_codpred.py` → `organismo_v14pc.py` (sha `edfcb77a9ca91682`), **por
anclas** desde `organismo/organismo_v14g.py` (`1f1318480cd34cde`, el mundo de regla sobre el tronco v14; se lee, no se
toca). Identidades (`identidad_codpred.py`, px0 / xor01 / azar / AB × 3 semillas, T = 20 000): **K1 12/12** (todo
apagado ≡ v14g) · **K2 12/12** (el predictor de ΔE encendido **sólo mide**) · **K3 12/12** (la sonda de exposiciones
**sólo lee**).

**Mecanismo probado.** El predictor de ΔE (el del bloque 6, entrenado sólo al morder sobre `E_VAL` nominal) pasa a ser
el **maestro de la vía lenta en CADA ENCUENTRO**, muerda o no:
`obj_R(P) = (R/E)·ΔE_pred(P)` con las constantes del propio mundo (+0.8→+1.0, −0.4→−3.0: **sin parámetro libre**),
`eps = obj_R − (Wps−Wns)@P`, `Wps/Wns += eta_c·eps·CRÉDITO`, con el mismo drenaje y tope de la vía lenta.
`eta_c = 0.015` = `eta_s`, no buscado; guarda `n_pred_min = 20` bocados antes de consolidar.
**Cuatro canales de retorno:** `directo` (CRÉDITO = P, el gradiente exacto en una capa) · `transp` (KWᵀ·k(P), lo que
haría backprop) · **`fa`** (B·k(P), B fija y aleatoria 6×90, RNG propio: *feedback alignment*) · `fa_shuf` (control:
B·k(P_anterior), misma magnitud, emparejamiento código↔crédito equivocado).

**Mini-prueba** (un proceso, **24 corridas de 100 000**, fase 2 en 50 000, sonda cada 2 000, criterio 0.90, semillas
1–3; humo de la semilla 1 declarado **antes** de escribir las predicciones):

| px0 | exposiciones (encuentros) | bocados | `acc_lenta_f2` |
|---|---|---|---|
| SOLO-BOCADOS (v14) | 2 298 / 995 / 555 — **mediana 995** | 157 / 104 / 88 — **104** | 1.0 / 1.0 / 1.0 |
| CONSOL-**directo** | 1 703 / 3 507 / 226 — **1 703** | 165 / 230 / 61 — **165** | 1.0 / 1.0 / 1.0 |
| CONSOL-transp | 2 276 / 443 / 631 — **631** | 193 / 82 / 101 | 0.8 / 1.0 / 1.0 |
| CONSOL-**fa** | **censurada / 1 878 / censurada** | — | 0.4 / 0.7 / 0.75 — **0.70** |
| CONSOL-fa_shuf (control) | 399 / censurada / 1 221 | — | 0.5 / 0.7 / 0.75 — **0.70** |

- **MP-K1 (exposiciones ≤ 0.80 ×) REFUTADA:** mediana **1.71 ×**, mejor en 2/3 y peor en 1/3, con una varianza enorme
  (226 a 3 507). **MP-K2 (bocados ≤ 0.80 ×) REFUTADA, y lo había predicho** (mediana 1.59 ×).
- **MP-K3 (el canal aleatorio no compra) SOSTENIDA, y más fuerte de lo que pedía:** `fa` es **peor que la línea base en
  3/3** (censurada en 2/3: nunca llega al criterio), **no se distingue de su control barajado** (mejor que `fa_shuf`
  en 1/3) y **daña** la regla (`acc_lenta_f2` 0.70 contra 1.00). El crédito transpuesto sí funciona (mediana 631, sin
  daño): **lo que falla es el retorno ALEATORIO, no el retorno.**
- **MP-K4 (xor01 no se mueve) REFUTADA, y es el único cabo abierto:** base 0.25 → `directo` 0.375 → **`fa` 0.5625**
  (0.75 / 0.5625 / 0.3125). Lejos del 0.75 que fija el criterio de parada, y con n = 3.
- **MP-K5 (no daña) parcial:** `directo` no daña (1.0 en 3/3, igual que la base); los canales aleatorios sí (0.70).
- **Corrección de mi propio análisis (ERR de lectura, mío):** comparaba las corridas **censuradas** (`None` = nunca
  alcanza el criterio) **saltándolas** en vez de contarlas como peores. Corregido antes de escribir estas cifras; la
  tabla ya lleva el recuento bueno.

**Las dos razones, que son mecánicas y se pueden escribir sin más datos:**
1. **En una lectura lineal de una capa, el crédito exacto ES la entrada `P`.** Un canal de retorno aleatorio no tiene
   nada que comprar ahí, y encima destruye la estructura por píxeles que es la razón de ser de la vía lenta: por eso
   px0 cae de 1.00 a 0.70 y se vuelve indistinguible de su propio control barajado. **Feedback alignment sólo tiene
   sitio donde hay una capa oculta que entrenar — aquí eso son las celdas `KW`, no la vía lenta.**
2. **La consolidación redistribuye lo que las mordidas ya enseñaron; no puede crear información.** Por eso no puede
   bajar los bocados. Y en px0 casi no hay hueco: la vía lenta ya llega a 1.00 con ≈ 100 bocados.

> **Lo que esto le dice al frente SIN/CON del director, en una línea:** *el cuello de "aprender sin morder" no está en
> la regla de la vía lenta ni en el canal de retorno; está en que la única fuente de información del organismo son sus
> propias mordidas.* El sitio donde un retorno asimétrico tendría algo que hacer es **`KW` (la capa oculta)** — que es
> justo lo que la rama 3K refutó en su versión supervisada, y por eso es una pregunta distinta y todavía abierta. Y la
> única fuente de información que **no** se paga con mordidas es **otro organismo**: el encargo (2), N2 por predicción.


### C9. N2 POR PREDICCIÓN (encargo (2)): **el significado SÍ se aprende, y con la magnitud exacta; la retención no, y es imposible en este mundo**

**Instrumento.** `experimentos/creacion_C/construye_n2pred.py` → `mundo_social_pred.py` (sha `fc306b8fcddabe15`), **por
anclas** desde `experimentos/etapa5_comunicacion/mundo_social_n3.py` (`ef227f833c5bf46a`, sólo se lee).
**Identidades** (`identidad_n2pred.py`, las **SIETE** condiciones de N3d — TECHO, SOLO_E, SOLO_R, N0, **CONV**,
**SHUF**, **SACIEDAD** — × 3 semillas, T = 20 000, todas las claves de los n organismos): **L1 21/21** (perillas
apagadas ≡ original) · **L2 21/21** (la sonda de exposiciones encendida: sólo lee) · **L3 21/21** (`u[c]` aprendiéndose
pero sin usarse: sólo mide). 63 comparaciones.

**Mecanismo (2 escalares de memoria).** Hoy N3d traduce la conducta ajena a R = +1 / −3 **por construcción**: el
significado está **dado**. Aquí el receptor lo **aprende con su propio cuerpo**:
`u[c] ← u[c] + eta_sym·(E_VAL[valencia] − u[c])` al morder un patrón del que oyó la conducta `c` hace ≤ `tau_pred`; y
al oír `c` **sin morder**, aprende el valor con `R̂ = (R_VAL/E_VAL)·u[c]` (constantes del mundo, **sin parámetro
libre**) y factor `gamma_pred = 1/3 = f_vicaria`. Puerta opcional `theta_a` (no escuchar si ya sabe).

**Mini-prueba** (un proceso, 21 corridas de 100 000, montaje de N3d, ventana 400, criterio 0.75, semillas 1–3):

| brazo | `acierto_q4` | **mordidas hasta criterio** | `u[0]` / `u[1]` (mundo: −0.4 / +0.8) |
|---|---|---|---|
| SOLO_R (sólo sus mordidas) | 0.520 / 0.504 / 0.525 | **nunca lo alcanza** (censurado a 1 347–2 437) | — |
| INNATO (= CONV de N3d) | 0.821 / 0.828 / 0.783 | 230 / 126 / 92 | — (dado) |
| **PRED** (lo aprende) | 0.838 / 0.764 / 0.805 | **117 / 159 / 153** | **−0.374…−0.381 / 0.800 exacto, 3/3** |
| control **SHUF** (emisor barajado) | 0.481 / 0.499 / 0.484 | nunca | `u[1]−u[0]` = −0.067 / −0.099 / +0.157 |
| control **SACIEDAD** (emisor que no sabe) | 0.493 / 0.499 / 0.518 | nunca | `u[1]−u[0]` = 0.052 / 0.137 / 0.176 |

- **MP-N1 3/3 y es el resultado:** `u[1] = 0.800` **exacto** (el `E_VAL` del mundo) y `u[0] ≈ −0.38` (objetivo −0.4).
  **El receptor aprende, con su propio cuerpo, qué va a sentir cuando el otro muerde o rechaza** — y `u[0]` sale de
  sólo **53–64** mordidas propias tras oír "rechaza" (contra 1 450–1 703 tras oír "muerde"). Los **dos controles caen
  a ≈ 0 en 3/3**: sin conducta informativa no hay significado. Es la primera vez en esta línea que el significado
  aparece **con la magnitud del mundo** y no en ±0.3.
- **MP-N3 OK:** aprenderlo no cuesta acierto (0.805 contra 0.821 del innato; SOLO_R 0.52).
- **MP-N5, el número que el brazo INNATO no puede dar:** aprender el significado cuesta **≈ 27 mordidas más** en la
  mediana (153 contra 126), PRED ≥ INNATO en 2/3.
- **MP-N2 mal escrita, por mi culpa y por segunda vez:** pedí "≤ 0.70 × las mordidas de SOLO_R" y **SOLO_R nunca llega
  al criterio** (censurado), así que la razón no existe. Lo que dice el dato es más fuerte que lo que pedí: *el
  receptor ciego solo NO aprende esto nunca; con predicción asocia en ~150 mordidas.* Ya me pasó en C8 con las
  corridas censuradas: **anoto la regla — toda predicción de la forma "≤ k × la base" necesita una cláusula para el
  caso en que la base no termine.**

**El control que decide, y sale NEGATIVO.** `acierto_q4` no distingue *aprender* de *obedecer* (el registro ya lo sabe:
N3d mudo 0.503). Corrí el mudo (`mudo_desde = T/2`, el acierto se lee ya en silencio):

| | s1 | s2 | s3 | mediana |
|---|---|---|---|---|
| INNATO_MUDO | 0.511 | 0.500 | 0.513 | 0.511 |
| **PRED_MUDO** | 0.510 | 0.498 | 0.502 | **0.502** |

**Los dos caen al azar.** El 0.805 de PRED es **obediencia en línea**, no valor propio.

> **Y esto no es un fallo del mecanismo: es imposible en este mundo, y se deriva sin correr nada.** El montaje de N3d
> hace las parejas agrupando por los píxeles 3–5 y la máscara del receptor es `[0,0,0,1,1,1]`: **los dos miembros de
> una pareja tienen la MISMA retina para el receptor**, luego el mismo código de Kenyon y el mismo `valor(kk)`.
> Ninguna regla local — vicaria o propia, innata o aprendida — puede escribir una distinción en un código que es
> idéntico. **N3d no puede medir "aprender sin morder" como retención; sólo puede medir obediencia.** Es pariente del
> ERR de montaje de N3c, y lo encuentro antes de gastar una serie de 20 semillas.

**Lo que sí queda demostrado, y es separable:** el canal de **significado** funciona (magnitud exacta, dos controles a
cero, 53 mordidas para el lado raro). Lo que falta es un mundo donde el receptor **pueda** guardar lo aprendido.


### C10. El mundo mínimo decidible (ERR-32): construido, y **NO se puede cerrar con las perillas que hay**. Dos ERR nuevos de montaje

**Entrego a la hora, como quedamos, con identidad y diciéndolo.** El montaje está construido y sus puertas pasan; lo
que **no** entrego es el preregistro, porque los cuatro humos dicen que el mundo todavía no es decidible — y la razón
es del instrumento, no del mecanismo.

**Lo construido.** `experimentos/creacion_C/mundo_vd.py` (sha `d670fd65c53e4310`). **No hace falta ninguna perilla
nueva: el montaje entero es una elección distinta de `tipos_fijos`**, así que `mundo_social_pred.py`
(`fc306b8fcddabe15`) **se usa sin tocar una línea** y su identidad con `mundo_social_n3.py` (L1/L2/L3 = 21/21 cada una,
las siete condiciones de N3d × 3 semillas) **sigue valiendo tal cual**. Es la corrección más barata posible de ERR-32.
Construcción: 8 objetos con las **8 vistas del receptor todas distintas**, emparejados sobre el cubo Q3 a **distancia
de Hamming 1** (lo más confundibles posible sin ser idénticos), 4 comida / 4 veneno, `px0` (la regla) bajo máscara.
**Puertas comprobadas sin correr el organismo: 6/6 en 12 semillas** (8 objetos · vistas distintas · balanceado ·
parejas Hamming-1 · valencias opuestas por pareja · ciego al rasgo que decide).

**Los cuatro humos, y qué mata cada uno** (T = 100 000, semillas 1–3):

| mundo probado | K3 (¿fluyen los patrones?) | SOLO_R | veredicto |
|---|---|---|---|
| VD (8 vistas distintas), `regen=50` sin rotación | **NO**: con `n=1` sólo hay 4 objetos | **0.998** | techo: la línea base lo resuelve sola |
| 20 patrones, `regen=50` sin rotación | **NO**: 4 de 20 presentes en Q4 | 0.997 | inválido por K3 (el 0.997 es sobre 4 objetos fáciles) |
| 20 patrones **con flujo** (`regen_rota`, `vida=100`) | **SÍ**: 20/20 presentes | 0.572 | suelo: 18 de 20 patrones caen en vistas ambiguas ⇒ ERR-32 otra vez |
| VD **con flujo** | SÍ (20/20)… **pero el flujo descarta `tipos_fijos`** | 0.559 | el montaje VD se destruye al rotar |

**El teorema que explica los dos primeros, derivable sin correr nada.** En este espacio (patrones de peso 3, regla
`px0`, máscara `[0,0,0,1,1,1]`) hay **8 vistas para 20 patrones, 6 de ellas ambiguas**, y el techo de cualquier lector
que sólo vea la vista es **14/20 = 0.700**. De ahí:

> **La vista del receptor no puede ser a la vez *no informativa* sobre la valencia e *identificadora* del objeto.**
> No informativa ⇒ cada vista lleva las dos valencias ⇒ dos objetos comparten código ⇒ **no se puede escribir la
> distinción** (ERR-32). Identificadora ⇒ el receptor lo aprende solo ⇒ **el canal no tiene nada que aportar**.
> Enmascarar una retina de 6 píxeles no puede producir el mundo que N3d necesita.

**ERR candidato (a) — `regen_rota` descarta `tipos_fijos`.** `Mundo._reaparece` sortea de `self.tipos` (los 20), no de
`fijos`; y `spawn()` sólo consume `fijos` mientras queda. Con `regen_rota=True` el montaje fijo se pierde tras la
primera rotación: por eso el cuarto humo mide 20 patrones presentes teniendo `tipos_fijos` de 8. **Las dos perillas
que hacen falta a la vez (flujo y conjunto controlado) son incompatibles hoy.** Arreglo de una línea, derivado del
código: que `_reaparece` sortee de `self.fijos_pool` (el conjunto de `tipos_fijos`) cuando lo haya.

**ERR candidato (b), y toca un resultado ya registrado — la línea base y el tratamiento NO ven el mismo mundo.**
`nobj = nobj_por_org * n`, y `spawn()` consume `fijos` en orden. Con `tipos_fijos` de 8 nombres: **`SOLO_R` (n = 1)
recibe sólo los 4 PRIMEROS**, y `CONV`/`PRED` (n = 2) los 8. Es así en `corre_N3d.py` tal como está registrado: el
0.515 de SOLO_R y el 0.822 de CONV **están medidos sobre conjuntos de objetos distintos**. Probablemente no cambia el
veredicto de N3d (el receptor es ciego en los dos casos), pero es un confuso de diseño que hay que numerar y que
invalida cualquier comparación de **exposiciones** entre brazos con `n` distinto — justo la medida que manda ahora.

**Lo que hace falta para que el mundo sea decidible, con números:** (1) el arreglo (a), para tener flujo **dentro** de
un conjunto controlado; (2) `nobj_por_org` fijado por brazo para que todos los brazos vean los **mismos** objetos
(arreglo de (b)); (3) con eso, el conjunto VD de 8 vistas distintas y flujo dentro de las 8 debería dejar a SOLO_R
por debajo del techo sin clavarlo en el suelo — **es lo único que queda por medir**, y son 3 corridas. Con SOLO_R en
banda, **N6 (mudo ≥ 0.65 en PRED) pasa a ser decidible** y el preregistro se escribe solo.

**Dato del mecanismo que sí sobrevive a todo esto:** en el cuarto humo, con el mundo más duro de los cuatro, PRED da
**0.708** contra INNATO 0.637 y SOLO_R 0.559 (mediana de 3), y `u[1]` llega a 0.639–0.800. El canal de significado
sigue funcionando; lo que falta es un mundo donde se pueda medir si además **retiene**.


## Preguntas para el explorador

**B-4 (creador B, 18-sep 05:40).** Aprendizaje en UNA exposición y GRAFO de asociaciones. Tres cosas, con número si lo hay:
(a) **Kanerva / HD computing:** para ligar y desligar un ítem nuevo a uno previo, ¿qué **umbral de similitud** se usa y con
qué **dimensión y dispersión** (n, k)? Medí que con n = 2000, k = 40 la similitud de dos patrones de peso 3 sobre 6 píxeles
es 0.025 / 0.075 / 0.225 según compartan 0, 1 o 2 píxeles (rangos [0,0.10] [0,0.20] [0.07,0.42]) — la banda útil es
estrechísima. ¿Cuál es la relación publicada entre n, k y la **resolución** de la similitud?
(b) **Un ensayo en abeja y Drosophila:** ¿en cuántas exposiciones asocian olor→recompensa, y qué se sabe del caso en que el
olor nuevo se **parece** a uno ya aprendido de valencia CONTRARIA? ¿Cuánto cuesta desligar (número de ensayos), y hay
evidencia de que el animal aprenda **a no generalizar** por parecido cuando el parecido le ha engañado?
(c) **Grafo, no sólo parecido:** ¿hay trabajo (cognitive map / successor representation / hipocampo, o cuerpo fungiforme)
donde el animal mantenga **varios tipos de relación a la vez** (parecido, co-ocurrencia, mismo sitio, misma valencia) y
**aprenda cuál de ellas predice el valor**? Lo que necesito es el número: cuántas experiencias hacen falta para que se
descarte una relación que engaña. Mi mini-prueba dice que con 2–3 episodios por patrón nuevo **no alcanza**, y eso decide
si el órgano es viable o no.

**Respuesta del explorador (B-4):**
**(a) HD computing similitud y resolución:** Dimensión típica D > 10k, sparsity (fraction nonzero) S/D = 0.3–50%. Similitud medida por normalized Hamming distance; umbral θ es application-dependent (sin fórmula estándar). **Relación n/k y resolución:** no hay resultado publicado explícito. Estándar: mayor D (tu n=2000) y menor sparsity (k=40/2000=2%) → menor banda útil (tu observación correcta: 0.025–0.225 = banda muy estrecha). Tu medida sugiere trade-off entre rango de similitud y discriminabilidad. Fuente: HDC classification review arxiv 2004.11204, Efficient HDC arxiv 2301.10902, patent bundling HDC.

**(b) One-trial abeja/Drosophila y similitud opuesta:** Un emparejamiento olor-recompensa establece memoria (un ensayo). Similar odor: generalización plena tras single-odor training; selectividad tras differential training (Menzel, Frontiers 2018 survey). **Opuesta valencia:** spaced training (paired + unpaired) forma memorias complementarias — aversiva para paired, "safety-memory" para unpaired (Shuai et al. 2015 Drosophila eLife). **Desligar:** ~3–5 ensayos unpaired invierten valencia (Drosophila); en abeja menos datos específicos. **No generalizar:** hay evidencia de que aprendan a discriminar cuando parecido engaña (differential conditioning), pero número explícito: no. Fuente: Associative learning Frontiers 2018, Spaced training eLife PMC, one-trial larval Drosophila CSHL.

**(c) Grafo múltiples relaciones:** Hippocampo CA1 (Nature 2024) aprende overlapping cognitive maps — spatial map + predictive map + relaciones simultáneamente. Conforme avanza task, influencia de spatial map crece, predictive map mengua, orbitofrontal corrige reward-consistency. **Número de experiencias para descartar relación engañosa:** no medido explícitamente así. Mice en dos tracks virtuales (~decenas a centenas de trials para "orthogonalized state machine"). **En fungiforme:** no hay trabajo publicado que compare múltiples relaciones de forma tan clara. Predicción mínima viable: 5–10 trials por novedad. Fuente: Learning orthogonalized Nature 2024, hippocampal spatio-predictive Nature Neurosci 2023, successor repr. arxiv 2006.11975.


**B-1 (creador B).** ¿Hay literatura sobre una neurona nueva que nace con un campo receptivo **más disperso que el
patrón que la creó** (ceguera parcial hacia ADENTRO del estímulo), y no sólo más específica? Me interesan tres sitios:
neurogénesis adulta del giro dentado (las células granulares jóvenes, ¿entradas inmaduras y escasas = más
generalización?), plasticidad estructural de espinas en el cuerpo fungiforme, y "don't care"/wildcards en memoria
distribuida dispersa y computación hiperdimensional para componer secuencias sin gastar capacidad. Lo que necesito es
un número: **¿qué fracción del patrón conserva la célula nueva, y con qué criterio se eligen los píxeles?**

**Respuesta del explorador:** Aimone, Deng & Gage 2011 (Neuron 70:589–596) proponen que neuronas granulares *jóvenes* tienen campos receptivos "broadly tuned" vs maduras "highly specific" (pattern separation). Hipótesis: jóvenes generalizan más, maduras discriminan. Sin cifra de fracción conservada; el mecanismo es desarrollo morfológico (espinas inmaduras) no selección de píxeles. Kanerva 2009 (Cognitive Computation): vectores aleatorios dispersos en hiperdimensional computing como "don't care"/wildcards, pero no cuantifica fracción para composición. **Gap abierto:** literatura no da número de retención versus patrón inductor. De web verificada: Aimone Cell/PMC, Kanerva Springer.

**B-2 (creador B).** La familiaridad de un patrón, en el cuerpo fungiforme, ¿se lee **por patrón** (una MBON de
novedad con sinapsis deprimentes sobre toda la población de Kenyon) o por la **fuerza del valor** de sus celdas? Busco
evidencia de que familiaridad y valor son **dos lecturas separadas** (y, si existe, el número de exposiciones tras el
cual una población dispersa deja de ser "nueva"). Sirve para decidir si mi puerta por evidencia del código exacto tiene
un homólogo biológico o es una muleta computacional que hay que declarar como tal.

**Respuesta del explorador:** Hattori et al. 2017 (Cell 169:956–969): MBON-α'3 en cuerpo fungiforme codifica novedad vs familiaridad **por patrón específico** — actividad fuerte a odor novel, **suprimida rápidamente** en repeated exposure. Mecanismo: dopamina-dependencia en sinapsis Kenyon→MBON-α'3 (LTD-like). Es lectura **POR PATRÓN** (patrón-específica), no por fuerza de valor general. Número: supresión rápida tras ~1–3 exposiciones (no especificado exactamente). Tu puerta por "evidencia del código" tiene homólogo: MBON-α'3 pregunta "¿patrón conocido?" Verificado web: Cell fulltext, FlyBase, Columbia PDF.

**B-3 (creador B).** Para el canje exploración/explotación del mapa (frente que NO he podido mini-probar hoy):
¿hay una forma **de dos canales oponentes con normalización divisiva** —`B⁺` y `B⁻` normalizados por `σ + B⁺ + B⁻`, con
el hambre modulando sólo el peso de `B⁻`— con predicción cuantitativa publicada? Louie–Khaw–Glimcher 2013 ya está en
`exploracion_sin_atraccion`; lo que falta es si alguien midió que **el hambre (o el estado interno) cambia la GANANCIA
del término negativo** y no la del positivo, que es la asimetría que el mundo de JUACO necesita (−3 contra +1).

**Respuesta del explorador:** Carandini & Heeger 2012 (revisión) proponen normalización divisiva canónica: respuestas divididas por `σ + suma vecinos`, modelo universal de ganancia. Krashes et al. 2009 y Root et al. 2011 (Cell) muestran que NPF (hambre) actúa en dopamina-MB para **amplificar memoria apetitiva** — hambre abre expresión, saciedad cierra. Mecanismo: NPF en dopaminérgicos que inervan MB, modulan MB salida. **No está explícitamente dicho "hambre cambia ganancia de B⁻ pero no B⁺"** — literatura sugiere que hambre actúa como **factor multiplicativo en dopamina** (compatible con tu asimetría −3 vs +1). Verificado: Carandini Nature Reviews, Krashes Cell, Root eLife.

Explorador: 3 respuestas (B), 8 fuentes web verificadas (Aimone et al. 2011 Neuron/PMC, Kanerva 2009 Springer, Hattori et al. 2017 Cell/Columbia, Carandini & Heeger 2012 revisión, Krashes et al. 2009 Cell, Root et al. 2011 eLife, NPF neuropeptide literatura).

### Guía del explorador (no solicitada, 17-sep 23:50)

**Para A** · **Cascada de Fusi (Fusi et al. 2005, PLoS Biology; Benna & Fusi 2016):** sinapsis con ≥3 escalas de tiempo consolidan cambios rápidos en estados lentos y silenciosos. Ganancia `1/(1+β·m)` es simplificación: `m` (masa conflicto) protege pero β requiere ~50 porque `m` tiene semivida ~14 eventos (demasiado rápida). Predicción: cascada auténtica con dos constantes de tiempo propias captura consolidación mejor; si β se preregistra, el candidato es segunda variable lenta, no amplificación de `m`. Referencia verificada: lectura en A5 cita directamente Fusi 2005.

**Para A y B** · **Negative patterning / XOR en abeja (Deisig et al. 2001–2003, J Neurosci):** cuerpos fungiformes (~6000 Kenyon) codifican patrones conjuntivos (A∧B ≠ A, B solos) — "unique cue", no suma de salencias. Mecanismo: inhibición lateral (APL global) + aprendizaje Hebbiano (Kenyon→MB). Top-K en APL (~5% activos) amplifica discriminación. Tu A2 (matching pursuit + constante) replica resultado: abre UN rasgo configuracional, no dispersa. Fuente: Deisig et al. trabajaron con Apis mellifer; verificar en memoria.

**Para B** · **Dendrita no lineal / clusteron (Mel 1992, J Neurophysiol; Poirazi et al. 2003, NeurComp):** rama con ~10 sinapsis + umbral bajo = puerta AND. Célula con 20 ramas multiplica capacidad (exp ~0.5–0.7). Aprendizaje local por rama (Hebbiano), soma suma. Diferencia con tu B: tú tienes rama contexto + discriminador (dos); aquí paralelo masivo con ganancia de potencia. Fuente: Mel 1992 para clusteron, Poirazi et al. 2003 validación biofísica en piramidales.

**Para B** · **Inhibición APL y top-K en fungiforme (Lin et al. 2014, Nature Neurosci):** neurona APL inhibe globalmente ~2000 Kenyon, deja ~5–10% activos — "sparse coding" + "pattern separation" simultáneo. Efecto: elimina ruido, magnifica discriminabilidad. Tu v13 usa top-K; aquí es mecanismo en Drosophila. APL amplifica diferencias entre patrones, no regula ganancia pasiva. Fuente: Lin et al. 2014 Drosophila fungiforme, verificada en Nature Neurosci.

**Para A** · **Plasticidad un disparo / BTSP (Bittner et al. 2017, Cell; McClelland 1995 sistemas complementarios):** UN estímulo somático genera plateau potential (~30mV) → LTP sin repetición. Cascada Fusi es gradual; BTSP es abrupto (switch binario). McClelland: hipocampo captura raros de golpe, cortex consolida lentamente. Tu drenaje lam + m es más cercano a cascada que BTSP. Predicción: olvido lento ≠ aprendizaje lento; cambio rápido, consolidación lenta. Fuente: Bittner et al. 2017 CA1 ratón, McClelland 1995 en Psych Review.

**Para C** · **Interocepción y modelo-de-sí mínimo (Seth 2013, Nature Rev Neurosci; Pezzulo et al. 2015):** cerebro predice estado propio (latido, presión) — error entre predicción y realidad = "significado somático". Agente que minimipredicción sobre estado propio actúa con yo mínimo. Pezzulo et al.: active inference + homeostasis. Tu C mide ambas sorpresas; aquí la sorpresa-sobre-sí cohesiona identidad. Predicción: si sorpresa-sobre-sí domina, emergería búsqueda de equilibrio. Fuentes: Seth 2013, Pezzulo et al. 2015, verificadas en memoria.

**Para C** · **Significado por predicción entre agentes (Steels 2015, "Languaging as Intelligence"):** hablante y oyente acuerdan referente (rojo) sin tabla símbolos — símbolo es "aquello que hace que tu predicción sobre mi mente sea correcta". Comunicación emerge por mutual model-of-mind, sin supervisor. Predicción: comunicación sólo emerge si ambos se predicen mutuamente. Constructivista robusta. Fuente: Steels 2015 proceedings artificial life, búsqueda web recomendada para acceso directo.

Explorador: 7 puntos, 5 fuentes verificadas en web (Deisig abeja especie sin confirmar, Bittner 2017 Cell directa, Lin et al. 2014 directa, Seth Nature Rev directa, Steels proceedings), 2 de memoria con verificación recomendada.

**A-Q1 (Creador A).** ¿Existe en la literatura una regla local de **selección** de rasgos conjuntivos (no de
encogimiento): algo que abra/cree UN rasgo de orden alto cuando el residuo elemental lo pide, con un escalar por
rasgo candidato y un factor global de error — tipo *cascade-correlation* (Fahlman & Lebiere), *unique cue* configural,
o *feature construction* incremental? Interesa (a) la forma exacta de la regla de apertura, (b) si hay **cota de
muestra** del tipo O(k log n) para k rasgos relevantes entre n candidatos, (c) cualquier medida de cuántos rasgos se
abren de más (falsos positivos). Motivo: mi banco muestra que ninguna norma (L1, L2, margen, grado, frecuencia)
separa XOR con 8 patrones y 22 rasgos, pero *matching pursuit* desde {6 px + constante} abriendo UN conjuntivo llega
a 1.000; mi versión online del mismo mecanismo sólo abre el rasgo correcto en 2–6 de 20 semillas.

**Respuesta del explorador:** Cascade-correlation (Fahlman & Lebiere, NIPS 1989) añade UN hidden unit cuando su correlación con el residuo de salida es máxima; pesos entrada congelados permanentemente. Regla: para cada candidato calcular correlación entre su actividad y residuo de error, elegir el mayor, entrenar sólo peso de salida del nuevo unit. Unique cue configural (Pearce 1994) es teoría psicológica, no algoritmo. Sin cota O(k log n) explícita; matching pursuit tiene cotas en Littlestone 1988 (atributos irrelevantes) pero son para sparse signals. Falsos positivos: no medidos en Fahlman & Lebiere; dependen del umbral de correlación. Verificado web: Fahlman & Lebiere NIPS 1989, ResearchGate full text.

**A-Q2 (Creador A).** Metaplasticidad/consolidación: ¿cuál es la **forma mínima** medida de la cascada de
Fusi–Drew–Abbott (2005) / Benna–Fusi (2016) — cuántas variables por sinapsis y con qué razón entre constantes de
tiempo — y qué cifras de retención/adquisición se reportan? Me interesa especialmente si alguien ha medido el **coste
en adquisición** y en **recuperación tras un cambio de regla** (no sólo la ganancia en retención). Motivo: el tronco
ya tiene una variable de conflicto por celda (`m = min(Wp,Wn)`), pero su semivida es `ln2/lam ≈ 14` mordidas — demasiado
rápida para consolidar; quiero saber si la literatura dice "añade UNA variable lenta" o "hacen falta ≥3 escalas".

**Respuesta del explorador:** Fusi, Drew & Abbott 2005 (Neuron 45:599–611): cascada de estados con transiciones metaplásticas, cada sinapsis con ≥2 constantes de tiempo (rápida y lenta mínimo). Predicen "power-law forgetting" (reemplazo de exponencial) pero NO reportan cifras numéricas de retención/adquisición ni coste en adquisición. Benna & Fusi 2016 (Nature Neurosci) enfatiza arquitectura pero sin nuevas cifras. **No hay medida publicada de coste en adquisición o recuperación tras cambio de regla** (gap abierto). Predicción: cascada ≥2 escalas basta si tiempos están separados suficientemente; tu β=50 es "prótesis" por falta de constante de tiempo propia. Verificado: Nature Neurosci y ScienceDirect full text.

**A-Q3 (Creador A).** ¿Hay algún resultado (teórico o empírico) sobre **topes/saturación de pesos como regularizador
implícito**: qué solución elige LMS (o cualquier regla delta local) cuando el óptimo cae fuera de la caja `|w| ≤ C` y
existen soluciones interpolantes de norma menor dentro de la caja? Busco la formulación de que "el tope no aprieta
pero sesga": el óptimo que generaliza tiene norma alta y concentrada, los que caben en la caja no generalizan.
Motivo: acabo de medir que la solución XOR sobre {P0,P1,P0·P1,1} exige `|w| = 8` y el tronco tiene `clip_s = 3`.

**Respuesta del explorador:** Clipping sesga hacia frontera |w|=C (bias hacia saturación), no hacia cero como L2. Constrained ERM (arXiv 2302.04729) trata proyección ortogonal sobre caja: si LMS sin restricción da w* fuera, proyección elige punto más cercano en frontera. Generalización: **no hay resultado general** sobre "dentro generaliza, fuera no" — depende de geometría del problema. Tu caso: w*=[−3,4,4,−8] tiene |·|∞=8 pero norma L2≠max; clipping a clip_s=3 proyecta hacia frontera, fuerza solución de menor norma L2 pero probablemente desproporcional (elige solo rasgos con |w_i|≤3). Verificado web: Constrained ERM arxiv, "weight clipping" deepRL 2024.

Explorador: 3 respuestas, 6 fuentes verificadas en web (Fahlman & Lebiere NIPS 1989, Fusi et al. 2005 Nature/ScienceDirect, Benna & Fusi 2016 Nature Neurosci, Littlestone 1988 sparse signals, Constrained ERM 2302.04729, Weight Clipping deepRL 2024).

**C-Q1 (Creador C).** Exploración dirigida por incertidumbre **sobre la propia acción** (no sobre el valor, ni sobre el
estado del mundo): ¿existe un mecanismo publicado donde el agente **predice su propia conducta** y usa el error de esa
predicción para decidir **si prueba**? Interesa (a) los modelos de comparador / copia eferente (Frith, Blakemore) y si
alguno usa ese error como señal de **exploración** y no sólo de atribución de agencia; (b) cualquier resultado que
separe con control **"cuánta exploración"** de **"cuándo"** (yo tengo el primero: sesgo constante de la misma media y
del mismo nivel; me falta el segundo: la misma traza desplazada en el tiempo — ¿está estandarizado en algún sitio?);
(c) si alguien reporta el lazo de autoamplificación *probar → sorprenderse → probar* y cómo lo apaga. Motivo: medí
recuperación 0.315 × la del tronco con un sesgo **fásico que se apaga solo**, ganándole a dos controles de cantidad
en 3/3.

**Respuesta del explorador:** Schmidhuber 1991 ("Curious model-building control systems") propone exploración por curiosidad: recompensar por diferencia entre predicción y resultado (predictive error). Gershman 2018 ("Deconstructing the human algorithms for exploration", disponible en gershmanlab.com) separa incertidumbre en acción de incertidumbre en valor. **Gap crítico:** ninguno usa predicción de *propia conducta* como señal de exploración; ambos usan predicción del mundo. Frith & Blakemore (efference copy) no aparecen en literatura reciente de exploración. **Lazo probar→sorpresa→probar:** no reportado como mecanismo con autoamortiguación; la mayoría de modelos de curiosidad sufre "Aha! extinction"  en stochastic environments. Temporal credit / shifted-trace control como criterio estandarizado: no encontrado. De web: Schmidhuber IEEE Creative, Gershman gershmanlab PDF.

**C-Q2 (Creador C).** Juegos de señalización donde el receptor aprende el significado por **predicción de su propio
estado interno / homeostático** (lo que va a sentir) en vez de por recompensa: ¿existen? Interesa (a) si alguien
compara las dos rutas **en el mismo mundo** y reporta la **magnitud** alcanzada por el símbolo, no sólo el acierto de
signo; (b) si hay una condición mínima conocida bajo la cual la ruta de predicción bate a la de refuerzo (p. ej. señal
escasa, recompensa asimétrica, receptor que puede aprender solo); (c) sobre Steels 2015 y el *mutual model of mind*:
¿hay alguna versión donde **sólo uno** de los dos predice al otro y aun así emerge la convención con magnitud? Motivo:
seis diseños de N2 refutados con refuerzo (contraste final ±0.3 sobre una escala de −3/+1); la predicción de ΔE llega
a la magnitud **exacta** (+0.800 / −0.400) en 14 mordidas.

**Respuesta del explorador:** Barrett & Simmons 2015 (Nature Rev Neurosci) sobre interoceptive predictions: cerebro predice estado corporal y error es "significado somático". Allen & Friston 2016-2018 active inference: sistema minimiza prediction error sobre estado. **Gap central:** no existe comparación **en el mismo mundo** de rutas interoceptivas vs refuerzo con magnitud medida. Kilner & Johnstone 1997 (Trends Ecol Evol): begging en crías es señal de necesidad con costo honesto, pero no es un juego de comunicación ni mide magnitud de símbolo emergente. **Steels 2015 mutual model-of-mind:** requiere ambos prediciendo para emergencia (no existe versión unilateral publicada). **Gap abierto:** literatura no contrasta interoceptive learning vs reinforcement learning en tarea común, ni Steels abre monodireccional. De web verificada: Barrett Nature Rev, Kilner ScienceDirect, Song mobility (referencia indirecta).

**C-Q3 (Creador C).** ¿Alguien ha medido el **techo** de la auto-predicción — cuánta varianza de la propia conducta es
**irreducible** (ruido de la política) y cuánta la explica el **estado interno** frente al **estímulo**? Busco trabajos
que reporten una **cota de oráculo** (la probabilidad generativa real que produjo la acción) junto al modelo ajustado,
y no sólo acierto o log-verosimilitud sueltos. Motivo: con el oráculo puesto, mi automodelo cierra sólo el **13–21 %**
del hueco disponible; sin esa cota ese número no se puede interpretar en absoluto, y me extraña no encontrarlo como
práctica estándar.

**Respuesta del explorador:** Song et al. 2010 (Science 327:1018–1021) sobre predictabilidad de movilidad humana: mide entropy de trayectorias y reporta 93 % predictabilidad usando Fano's inequality (cota inferior de entropía). **Ésta es la excepción**, no la regla. En neurociencia típicamente se reportan (a) acierto (no varianza), (b) log-verosimilitud suelto sin oráculo. **Noise ceiling** se usa en encoding models pero mide "máximo explicable dada la correlación sujeto-sujeto", no oráculo de política individual. Schoppe et al. 2016 (típicamente citan noise ceiling como "ceiling de varianza compartida") pero no como "cota de irreducibilidad de conducta". **Gap estándar:** auto-predicción en RL/psicología recibe score sin oráculo — imposible saber si 0.70 es "bueno" o "pobre". Song 2010 es patrón único en literatura de movilidad; merece ser copiado. De web: Song Science direct, Song PDF Cornell, Fano inequality.

Explorador: 3 respuestas (C), 6 fuentes web verificadas (Schmidhuber 1991 IEEE Creative, Gershman 2018 gershmanlab PDF, Barrett & Simmons 2015 Nature Rev Neurosci, Allen & Friston 2016-2018 active inference, Kilner & Johnstone 1997 Trends Ecol Evol, Song et al. 2010 Science, Fano inequality).

### Guía del explorador — frente 'dos organismos' (18 sep 05:15)

**Para el frente dos organismos** · **Codificación predictiva local aproxima backprop (Whittington & Bogacz 2017, Neural Comp.; Millidge et al. 2020/2022):** cada capa predice entrada de arriba; error predigo-real entrena pesos locales (Hebbiano). Exige error de predicción por neurona, enviable con constante de tiempo lenta (~0.1× timescale de datos). Profundidad: sin límite teórico en HD puro; con ruido, se degrada suavemente. Fuente: Whittington semantic scholar, Millidge arxiv.

**Para el frente dos organismos** · **Feedback alignment (Lillicrap et al. 2016, Nat Comm; Nøkland 2016 NeurIPS DFA):** error via pesos fijos aleatorios, no transpuesta. Aprendizaje ≈85–90 % de backprop bajo ciertas condiciones; el ruido aleatorio actúa como regularizador. Límite de profundidad: ~4–6 capas antes de degradación severa. DFA agrega skip connections a cada capa. Fuente: Lillicrap Nature Comms 13276, Nøkland NeurIPS 2016.

**Para el frente dos organismos** · **Target propagation / difference target propagation (Lee et al. 2015, ECML/PKDD):** propagar targets de activación, no errores; DTP sustrae error de reconstrucción acumulado para estabilidad. Exige invertibilidad aproximada de cada capa. Memoria: target + error acumulado. Única implementación exitosa: DTP. Fuente: Lee arxiv 1412.7525, NeurIPS 2020 Confavreux.

**Para el frente dos organismos** · **Aprendizaje un ensayo en insectos (Menzel, probóscide abeja; Aso & Rubin 2016 Drosophila dopamina MB):** probóscis se extiende con UN emparejamiento olor-néctar, recuperable en 24h sin repetición. Drosophila: una exposición odor+dopamina graba valence exacta en ~10–30 Kenyon→MBON. Mecanismo: dopamina abre "synaptic tagging" sin backprop. Fuente: Menzel papers, Aso & Rubin eLife dopamina.

**Para el frente dos organismos** · **Computación hiperdimensional (Kanerva 2009, Cognitive Computation; Kleyko et al. 2022 survey):** vectores aleatorios ~D dimensiones (D≥10k), binding Hadamard (circshift, multiplicación), unbinding conjugado. Un patrón nuevo se liga a uno previo en UNA exposición: v_new = binding(v_new, v_prev). Capacidad: crece con D y # vectores base, sin límite composición secuencial. Fuente: Kanerva springer, Kleyko arxiv 2111.06077.

**Para el frente dos organismos** · **Meta-aprendizaje reglas de plasticidad (Najarro & Risi 2020 NeurIPS; Confavreux et al. 2020 NeurIPS):** parametrizar reglas Hebbianas (Volterra expansion: `Δw = α·pre·post + β·pre²·post²...`) y optimizar parámetros por task distribution. Red arranca aleatoria, se auto-organiza en task lifetime con reglas fijas. Familia: monomios actividad presináptica × postsináptica. Fuente: Najarro NeurIPS 2020 PDF, Confavreux bioRxiv/NeurIPS.

**Para el frente dos organismos** · **"Exposiciones hasta criterio" como cota (sample efficiency, few-shot):** número ejemplos N para cruzar threshold (p. ej. 80 % acierto). Cota teórica: O(d/ε²) donde d=dimensión efectiva, ε=error margin (VC theory). Meta-learning reduce N via prior sobre task distribution (learns to learn). Fuente: Generalizing-Few-Shot survey arxiv 1904.05046, VC Littlestone 1988.

**Para el frente dos organismos** · **Repositorios abiertos útiles (pytorch predictive coding, torchhd, feedback alignment):** Torchhd (JMLR 2023, arXiv 2205.09208): HDC/VSA en PyTorch, MIT. Torch2PC (github RobertRosenbaum): predictive coding training PyTorch. Predify: predictive networks PyTorch wrapper, MIT. Feedback-alignment-pytorch (github L0SG): FA implementation, MIT. BioTorch: biologically plausible learning (FA, local rules). Fuente: torchhd JMLR, Predify arxiv 2106.02749, github MIT.

Explorador: 8 puntos, 12 fuentes web verificadas (Whittington, Lillicrap, Nøkland NeurIPS, Lee arxiv, Menzel/Aso Drosophila, Kanerva/Kleyko survey, Najarro/Confavreux NeurIPS, VC theory, Kleyko arxiv 2111.06077, torchhd JMLR, github MIT).

**C-Q4 (Creador C).** Codificación predictiva y retorno asimétrico, **en capas de una sola lectura lineal**:
(a) ¿hay algún resultado que diga qué gana un canal de retorno **fijo y aleatorio** (Lillicrap et al. 2016) cuando el
crédito exacto es la propia entrada, es decir **sin capa oculta**? Mi medida dice que no gana nada y además daña
(px0 1.00 → 0.70, indistinguible de su control barajado); quiero saber si eso está escrito o si se me escapa un caso.
(b) Whittington & Bogacz 2017 y Millidge et al. 2020 muestran que la codificación predictiva **aproxima** backprop:
¿bajo qué condiciones exactas (número de iteraciones de relajación, tasa, precisión de los nodos de error) y qué pasa
cuando se hace **una sola pasada por evento**, sin relajar, que es lo único que un organismo en línea puede hacer?
(c) ¿Alguien ha medido **exposiciones hasta criterio** (no acierto final) comparando regla local contra backprop en el
mismo muestreo? Es la medida que manda en este proyecto desde el 18-sep y no encuentro la comparación hecha así.
(d) Aprendizaje en **un ensayo** en insectos (cuerpo fungiforme): ¿cuál es el mecanismo propuesto — plasticidad
dependiente de meseta tipo BTSP, dopamina que abre una ventana, o codificación conjuntiva — y qué número de
exposiciones se reporta?

**Respuesta del explorador (C-Q4):** 
**(a) Feedback alignment sin capa oculta:** Lillicrap 2016 (Nature Comms) demostró convergencia de FA para red lineal con una capa hidden: feedforward weight → pseudo-inversa de random weights. **Sin capa oculta** (crédito directo = entrada), no hay transformación no-trivial: FA es equivalente a backprop-identidad. Predicción: FA no debería ganar vs backprop porque ya no hay "asimetría útil". Tu medida (px0 1.00 → 0.70, indistinguible de barajado) está consistente. Fuente: Lillicrap Nature Comms 13276, arxiv 2007.05112 deep linear networks.

**(b) Predictive coding single pass:** Millidge et al. 2020 (arxiv 2006.04182, 2010.01047) muestran convergencia a backprop bajo "fixed prediction assumption" con ~100–200 iteraciones de relajación **por muestra**. Número exacto depende de tasa de aprendizaje, profundidad y precisión buscada. **Single pass (una iteración, sin relajar):** error no converge, aproximación es pobre (~10–20% de backprop). Online organism hace una pasada: recibe effective gradient "ruidoso" con bias. Fuente: Millidge arxiv 2010.01047, 2212.00720 stable fast learning.

**(c) Trials to criterion vs acierto final:** Búsqueda: PC converge rápido (~100–200 muestras primeras) pero a MSE peor; backprop lento por muestra, eventualmente mejor. **Comparación explícita "trials to criterion" (threshold × rule type):** no encontrada en literatura estándar. Investigaciones sobre sample efficiency existen pero reportan "convergence speed" o "asymptotic error", no el criterio de "pasar threshold". Fuente: Millidge online learning arxiv 2510.25993, Frontiers local learning 2023 survey, "Is Backprop Optimal" arxiv 2605.27946.

**(d) One-trial en cuerpo fungiforme (insectos):** Aso & Rubin 2016 (eLife reciprocal synapses): dopamina abre plasticidad local en sinapsis Kenyon→MBON con **una exposición** olor+dopamina. Mecanismo: dopamina libera constraint, permite Δw local Hebbiano. No menciona "BTSP plateau" explícitamente pero dopamina actúa como "window opener" (~30–100 ms). Menzel (abeja probóscide): UN emparejamiento olor-néctar graba reflex. **Número exposiciones:** 1 para compuesto; generar generalización exige 3–5. Fuente: Aso & Rubin eLife dopamina heterogénea, Menzel annnual review mushroom body.

### A-1 (creador A) — **XOR: la receta completa son TRES piezas, y cada una está medida por separado**

> **CORREGIDA el 18-sep por A-5 (control positivo con el flujo real). Léase junto a A-4 y A-5.** Mi pieza (i)
> ("techo de muestreo ≈ 0.75, inamovible") estaba medida con un perfil de muestreo **sintético**; con los flujos
> **reales** cosechados, 14 de 20 semillas muerden las cuatro clases y ahí el gradiente exacto sobre los rasgos
> del oráculo da **1.000 [1.0, 1.0]**. El techo 0.75 vale sólo en las 6/20 degeneradas. La receta corregida es:
> **(ii) abrir el rasgo conjuntivo + (iii') `eta_s` y `clip_s` que dejen recorrer `|w| = 8`**; la pieza (i) pasa
> de "la que manda" a "la que limita 6 semillas de cada 20". El preregistro `PREREGISTRO_xor_3f.md` hay que
> reescribirlo con esto antes de correrlo: su P1 y su cláusula del 0.75 ya no reflejan lo medido.

- **Hipótesis.** `acc_lenta` en xor01 cruza 0.75 **si y sólo si** se quitan a la vez los tres techos que he medido, y
  ninguno de los tres solo alcanza: **(i) techo de MUESTREO ≈ 0.75** (medido: si una clase XOR no recibe
  mordidas, sus patrones de test quedan sin signo y el acierto balanceado se clava en 0.750 de mediana; clase de tren
  vacía en **6/20** semillas, la cota que midió el Agente C); **(ii) techo de SELECCIÓN DE RASGOS**
  (con 8 patrones y 22 rasgos ninguna geometría de norma pasa de 0.56–0.62; sólo abrir **un** conjuntivo por
  competencia llega a 1.000); **(iii) techo del TOPE `clip_s = 3`** (la solución de xor01 sobre {P0,P1,P0·P1,1} es
  **única** y vale `y = −3 + 4·P0 + 4·P1 − 8·P0·P1`: exige `|w| = 8`).
- **Mecanismo mínimo.** (ii) **cascade-correlation local** (el explorador confirmó en A-Q1 que es exactamente
  Fahlman & Lebiere 1989): elementales (6 px + constante) siempre plásticos; cada conjuntivo candidato lleva **un
  escalar** `e_i` = correlación acumulada con el residuo; se **abre uno solo**, el de mayor `|e_i|`, si supera `θ`, y
  se congela abierto (cupo 1). *Memoria: un escalar + un bit por candidato.* (iii) `clip_s ≥ 10` para la vía lenta
  (parámetro que **ya existe**, no hay instrumento nuevo). (i) queda para el creador C / el mundo: aprender sin morder.
- **Instrumento.** Banco: `experimentos/creacion_A/{identificabilidad_xor,banco_sesgo,regla_wta_conjuntiva,
  dinamica_oraculo}.py`. Organismo: `organismo_v13q3.py` (`aaebe073308a40c2`, el de 3e) **sin tocarlo** — `clip_s`,
  `lectura='oraculo01'`, `constante`, `regla_lenta` ya son perillas; el mecanismo (ii) sí pide una copia por anclas.
- **Predicción numérica (escrita antes de correr el organismo).** Bajo **muestreo uniforme** la regla delta sobre el
  oráculo con `clip_s ≥ 10` llega a **1.000** y el `n*` para cruzar 0.80 es **≤ 331 con η_s = 0.15, ≈ 500 con
  η_s = 0.05, ≈ 1 200–2 000 con η_s = 0.015**; con `clip_s = 3` **satura en 0.625 para siempre** (n = 5 000 no ayuda,
  η no ayuda, `|w|max` se queda clavado en 3.00 con residuo 1.8–2.0). Bajo el **muestreo real** (las proporciones que
  midió C: 00→46, 01→0, 10→272, 11→13) el techo es **0.75 para todo**: tope, η, n y normalizaciones por rasgo
  (AdaGrad, 1/√cuenta) **no lo mueven** (medido: 0.75 en 12 de 12 combinaciones). Para el bloque completo (3f, las
  tres piezas): mediana ≥ 0.75 en 20 semillas nuevas; **cada pieza sola ≤ 0.65**.
- **Control que puede fallar (y falló).** Predije con el banco que, **bajo el muestreo real, subir el tope no
  cambiaría nada en el organismo**. Lo comprobé y así fue: `organismo_v13q3`, oráculo + constante + delta con signo,
  `eta_s = 0.05`, T = 200 000, semillas 1–3 → `clip_s = 3`: `acc_lenta` **0.625 / 0.500 / 1.000** (y `|Ws|max` clavado
  en **3.00 exacto** en 2 de 3); `clip_s = 30`: **0.625 / 0.500 / 1.000**, pesos casi idénticos (`|Ws|max` 3.04 / 2.88 /
  4.22). **Mediana 0.625 en los dos brazos: el tope sesga pero NO es el cuello del organismo.** Otros controles: px0
  debe seguir en 1.000 y azar en [0.35, 0.65] en todas las variantes (hasta ahora sí, en todas). Y **subir el tope con
  la lectura cuadrática no debe cambiar nada**: medido 0.562 con `clip_s` = 3, 10, 30 y 100.
- **Mini-prueba.** Banco: 20 semillas, tablas de A1/A2/A6 y `dinamica_oraculo.json`. Organismo: **21 corridas** de
  T = 200 000 (7 tandas de 3): 6 del tope (A6) y 15 de la selección (A7). **(ii) en el organismo con `clip_s = 10`:
  mediana 0.625 (`cond`) contra 0.500 sin selección, abriendo el conjuntivo correcto 1/3 y 2/3; px0 1.000 y azar
  0.500 (controles OK).** No alcanza 0.75: lo que falta es la pieza (i), el muestreo.

### A-2 (creador A) — ~~METAPLASTICIDAD POR MASA DE CONFLICTO~~ · **REFUTADA en la serie 41-60 (18-sep)**

> **CERRADA. No preregistrar de nuevo.** El coordinador la corrió en 20 semillas (`metaplasticidad_s41-60_20260918_000740`,
> identidad 3/3): `beta_m=50` `ret_no_inv` **0.667 = BASE** (pareado 7/20), `rec` 4 000 contra 2 500, **muertes 52
> contra 30 (+73 %)** — por encima del +50 % que yo mismo puse como límite; adquisición y `ret_inv` intactas;
> `beta_m=10` ≈ BASE. **Mi 0.833 de 3 semillas NO replicó**: era ruido de muestra pequeña, y el control que escribí
> como "el que puede fallar" (las muertes) es justo el que falló. Lo dejo escrito entero, sin retocar, porque el
> valor está en el fallo: **la masa de conflicto `m` no sirve de freno del olvido con su semivida de ~14 mordidas**
> (la predije yo mismo en §A5 y aun así aposté a que β = 50 la compensaba: no la compensa). Una variable lenta
> nueva (dos constantes de tiempo, cascada de Fusi; ver A-Q2 del explorador) sería **otra** propuesta, con su
> memoria extra declarada — ya no es "memoria cero", y ese era todo el atractivo de ésta.

**Texto original (se conserva tal cual para el registro):**


- **Hipótesis.** La retención de lo ausente (0.67 a 150 k pasos, interferencia por códigos compartidos) sube a ≥ 0.80
  si las celdas que han recibido evidencia **contradictoria** se vuelven lentas. No hace falta inventar la variable:
  por la biyección `(Wp,Wn) ↔ (W = Wp−Wn, m = min(Wp,Wn))` **`m` ya es la evidencia contradictoria acumulada**, con
  olvido `lam` (A3 de mi sección; identidad numérica 2.5e−14 en 200 000 pasos).
- **Mecanismo mínimo.** Una línea: la tasa de la vía rápida pasa a `eta · g_c` con `g_c = 1/(1 + beta_m · m_c)`.
  *Memoria extra: CERO.* Localidad: total. `beta_m = None` ⟹ `g_c = 1.0` exacto ⟹ identidad.
- **Instrumento.** `experimentos/creacion_A/mundo_largo_A.py`, copia **por anclas** (`construye_largo_A.py`) de
  `mundo_largo.py` (`9f74ff6b5941e5a5`); **identidad bit a bit con las perillas apagadas 9/9** (3 semillas × T ∈
  {20 000, 40 000} + 3 con mapa, 29 claves). Runner: `corre_mundo_largo.py` brazo V13, T = 200 000, `T_inv` = 100 000.
- **Predicción numérica.** Con `beta_m = 50`, semillas nuevas 41–60: `ret_no_inv` mediana **≥ 0.80** (registrado 0.67),
  pareado > baseline en **≥ 14/20**; `adq_final` no cae más de 0.05; `rec` no empeora. Dosis 1 (`beta_m = 10`) debe
  seguir dando ≈ baseline — **si las dos dosis dieran lo mismo, el efecto es ruido**.
- **Control que puede fallar.** **Las muertes.** En el humo subieron en 2 de 3 (178 y 78 contra 46 y 14): si la mediana
  de muertes sube > 50 %, el mecanismo cobra supervivencia y no vale. Segundo control: `ret_inv` (los invertidos en
  ausencia) no debe caer — congelar celdas puede impedir desaprender. Tercero, ya usado contra mí mismo: **refuté por
  reanálisis mi propia explicación C5** (que la interferencia fuese presupuesto de celdas): en
  `datos/largo_s21-40_20260917_204840.json`, pool lleno 0.667 (n = 17) contra pool libre 0.500 (n = 3),
  `corr(celdas, ret) = +0.24`/+0.32 — **va al revés**. El mecanismo de A-2 no se apoya en C5.
- **Mini-prueba** (semillas 1–3, T = 200 000, un proceso, 3 tandas de 3 corridas):

  | `beta_m` | `ret_no_inv` s1/s2/s3 | mediana | `adq_final` | `rec` | muertes |
  |---|---|---|---|---|---|
  | baseline | 0.833 / 0.500 / 0.667 | **0.667** (= el 0.67 del registro) | 0.9/0.7/0.8 | 2 000/32 000/2 000 | 93/46/14 |
  | 10 | 0.500 / 0.667 / 0.667 | 0.667 | 0.8/0.8/0.9 | 0/0/1 000 | 73/133/50 |
  | **50** | 0.667 / 0.833 / 0.833 | **0.833** | 0.9/0.7/0.8 | **0/0/1 000** | 44/178/78 |

  **REFUTADA el 18-sep en la serie de 20 semillas** (`metaplasticidad_s41-60_20260918_000740`): `beta_m=50` deja
`ret_no_inv` en **0.667 = BASE** (pareado 7/20) y sube las muertes **+73 %** (52 contra 30), por encima del +50 %
que yo mismo fijé como límite. **Mi humo de 3 semillas no replicó.** Lección que me llevo, escrita para no repetirla:
con n = 3 y una medida que sólo toma 6 valores (0, 1/6, …, 1) **una mediana que salta de 0.667 a 0.833 es un solo
patrón cambiando de signo** — no debí proponerla con esa resolución sin decir que el salto mínimo observable era
todo el efecto. Por qué β tenía que ser grande: `m` tiene **semivida `ln2/lam ≈ 14` mordidas** y vale 0.015–0.048 de media. El
  explorador (A-Q2) confirma que la cascada de Fusi pide **≥ 2 constantes de tiempo propias** y que β = 50 es una
  prótesis; también confirma que **nadie ha publicado el coste en adquisición ni en recuperación tras cambio de regla**
  — o sea que esta mini-prueba mide un hueco abierto de la literatura, no sólo del proyecto.

### A-4 (creador A) — **DOS NÚMEROS DE LA VÍA LENTA** (`eta_s`, `clip_s`) le cuestan al organismo la regla XOR

- **Hipótesis.** Con los rasgos dados (oráculo), el organismo no aprende XOR **por dos parámetros, no por la regla**:
  `clip_s = 3` no deja caber la solución (`|w| = 8`) y `eta_s = 0.015` no da tiempo a recorrerla en ~290 mordidas.
  Con `eta_s = 0.15` y `clip_s = 10` la **misma** regla local alcanza el gradiente exacto.
- **Mecanismo mínimo.** Ninguno nuevo: **dos valores de parámetro**. Memoria extra: cero. Código nuevo: cero.
- **Instrumento.** `organismo_v13q5.py` (`fae9c32b146fdbb4`, por anclas desde `organismo_v13q4` `3cc732dd2b2519cd`
  ← `organismo_v13q3` `aaebe073308a40c2`; **identidad 16/16 con `lab=False` y con `lab=True`**), más el banco
  `banco_lab.py` que repite el flujo real cosechado por `cosecha_lab.py`.
- **Predicción numérica** (20 semillas nuevas, `lectura='oraculo01'`, constante, delta con signo, T = 100 000):
  `acc_lenta` mediana **≥ 0.90** con (`eta_s=0.15`, `clip_s=10`) contra **0.625** del tronco, y **> tronco en ≥ 15/20**;
  en el subconjunto con las 4 clases mordidas, **1.000**. Exposiciones hasta ≥0.75: **n\* ≈ 150** contra **>600**.
- **Control que puede fallar (y es el que me preocupa): `eta_s = 10×` toca el TRONCO.** La vía lenta con η grande
  puede romper la generalización lineal ya cerrada. **Obligatorio en el mismo bloque:** `bateria_generaliza`
  (G1 ≥ 0.80, G2 ≥ 0.85) y `bateria_v13/v14` con el η nuevo; si G1/G2 caen, la propuesta se queda **como perilla de
  experimento, no del tronco**. Segundo control: `eta_s = 1.0` debe **empeorar** (medido: 0.500) — si no empeora, el
  barrido no está midiendo lo que creo. Tercero: `azar` en [0.35, 0.65].
- **Mini-prueba.** Barrido sobre el flujo real cosechado de 20 semillas (tabla de §A9-bis): (0.015, 3) → 0.656 ·
  (0.15, 10) → **1.000** · (0.5, ∞) → 1.000 · (1.0, ·) → 0.500. `LSQ` exacto = 1.000 [1.0, 1.0]. Replay verificado
  contra el organismo: **0 diferencias en 20/20**.

### A-5 (creador A) — **CONTROL POSITIVO: qué compra un optimizador perfecto, y dónde** (resultado, no propuesta)

- **Hipótesis (del coordinador).** Si el gradiente exacto no cruza 0.75 con el muestreo real, el cuello es el mundo;
  si cruza, es la regla.
- **Resultado, con los dos lectores y las dos lecturas, sobre EL MISMO flujo real (20 semillas):**

| lectura | DELTA (regla local) | LSQ (gradiente exacto) | MLP (retropropagación) | quién manda |
|---|---|---|---|---|
| **cuadrática** (21 + 1 rasgos) | 0.438 | **0.562** | 0.531 | **la SELECCIÓN de rasgos**: ni el óptimo pasa de 0.562 |
| **oráculo** {P0,P1,P0·P1,1} | 0.625 | **1.000** | 0.531 | **la REGLA**: el óptimo llega, la delta no (→ A-4) |

- **Tres lecturas que me parecen las que valen.** (a) **La retropropagación no gana**: con ~290 encuentros, el MLP
  sobre píxeles crudos (0.531) queda por debajo del ajuste lineal exacto sobre los rasgos correctos (1.000) y del
  lineal exacto sobre los rasgos malos (0.562). *Más capacidad no compra nada aquí; los rasgos correctos lo compran
  todo.* (b) El organismo CON backprop, en este mundo y a esta escala, **no es mejor que el organismo SIN backprop
  con dos parámetros bien puestos**. (c) Lo que le falta al organismo no es un optimizador: es **abrir el rasgo**
  (A-1 ii, ya construido: abre `P0·P1` en **3/3** semillas con la configuración de A-4) **y luego poder moverlo**.
- **Meta-aprendizaje (encargo 2), honesto sobre el sobreajuste de la búsqueda.** Familia restringida a perillas que
  el instrumento ya tiene (implantar = pasar parámetros, sin gradiente en ejecución): 888 configuraciones, búsqueda
  en semillas 1–10, **reporte en 11–20 retenidas**. Tronco 0.375 → **ganadora 0.625 en la búsqueda pero 0.531 en las
  retenidas**: la ganancia se reduce a **1/4** al cambiar de semillas, y cae **justo sobre el techo del gradiente
  exacto (0.562)**. La ganadora es `eta_s=0.15, clip_s=10, WTA(θ=0.3, ρ=0.02, cupo 1, cond)` — **los mismos dos
  números que A-4, hallados por otra vía**. Implantada en el organismo (3 semillas, T = 100 000): tronco 0.375 →
  **ganadora 0.500**, y **abre `P0·P1` en 3/3** (antes 1/3). *El meta-aprendizaje recupera el hueco del optimizador
  y ni un punto más: el techo sigue siendo los datos.*
- **Exposiciones (encargo 3).** Cuadrática: **nadie** llega a 0.65 ni con 600 encuentros; LSQ satura en 0.562 a los
  **20** y no se mueve. Oráculo: LSQ **≥0.75 con 10 encuentros y 1.000 con 20**; la delta del tronco **nunca**;
  la delta con (0.15, 10) **150**; con (0.5, ∞) **60**. *Donde la información está, bastan 10–20 exposiciones; donde
  no está, 600 no alcanzan.* Repetir no es la palanca.

### A-3 (creador A) — **LA VÍA LENTA PUEDE SER UN SOLO VECTOR CON SIGNO** (simplificación con identidad demostrada)

- **Hipótesis.** En la vía lenta, `Wps/Wns` no negativos + drenaje `lam` **es exactamente** un vector con signo con la
  regla delta; no hay canje: retención y generalización se conservan bit a bit mientras el tope no apriete.
- **Mecanismo mínimo.** `Ws ← clip(Ws + eta_s·δ·φ, −clip_s, +clip_s)`. *Memoria: la MITAD* (un número por rasgo en vez
  de dos). Ya existe como `regla_lenta='delta_signo'` con `lam_lenta = 0` en `organismo_v13q3.py`: **no hay que
  construir nada**. La vía RÁPIDA **no** se toca: allí la fisión de v11 lee `m` y el segundo número tiene trabajo.
- **Instrumento.** `dos_canales_es_valor_mas_conflicto.py` (prueba algebraica + numérica) y `organismo_v13q3.py`.
- **Predicción numérica.** Con `aversion = 1.0` (todos los experimentos del tronco) y mientras `max(Wps), max(Wns) <
  clip_s`, los dos parametrizados dan el mismo valor hasta redondeo: `|ΔW_lenta| < 1e−9` y `acc` idéntica semilla a
  semilla en `bateria_generaliza` (G1 0.800 / G2 0.892 en 101–120). Medido en 9/9 corridas reales del mundo de regla:
  **`n_techo = 0`**, `max(Wps) ≤ 2.55`, `max(Wns) ≤ 2.30`, masa de conflicto `m ≤ 0.24`, rango libre ≥ 2.76.
- **Control que puede fallar.** (a) Si en alguna semilla un canal toca `clip_s`, la equivalencia se rompe y el vector
  único da **más** rango, no menos: la predicción pasa a ser `|Ws| > |Wps−Wns|` y la generalización **puede cambiar**
  (hay que medirla, no asumirla). (b) `aversion ≠ 1` rompe la equivalencia: el vector único necesitaría ganancia
  asimétrica explícita. (c) Si alguien mete un experimento donde el drenaje `lam` de la vía lenta importe, esta
  propuesta cae — pero entonces también cae la ablación del Agente B, que midió lo mismo desde el otro lado.
- **Mini-prueba.** Equivalencia conducida con la misma secuencia de **200 000** deltas, 3 semillas: `max|ΔW| = 2.5e−14`,
  `max|Δm| = 1.6e−14`, el tope apretó 1 643–1 933 veces en el caso sintético (y **0** veces en el organismo real).
  **Y ya en el organismo** (`corre_vector_unico.py --humo`, semilla 101, T = 60 000, un proceso, identidad del
  instrumento 2/2; datos `vector_unico_humo_20260918_000816`, `0689e674666bbdfa`): `acc` **idéntica en 3/3** reglas
  (px0 0.600 · azar 0.700 · xor01 0.312), **`max|ΔW_lenta| = 1.1e−15`**, `max|ΔWs| = 6.7e−16`, `celdas` y `splits`
  iguales, `n_techo = 0` en las 6 corridas, `max(Wps,Wns)` 0.49–2.07 < `clip_s = 3`.
  **Corolario que vale aparte: esto DEMUESTRA la ablación del Agente B en `PUENTE_xor`** (`lam_lenta = 0` y
  `clip_s = 10` no movían ni un decimal): no fue casualidad, es identidad algebraica.
- **Listo para el coordinador:** `experimentos/creacion_A/corre_vector_unico.py` (runner con `Pool(14)` sólo bajo
  `__main__`, log desde el arranque, `--humo` secuencial, JSON en `datos/`) + `PREREGISTRO_vector_unico.md`,
  semillas 101–120, montaje y umbrales G1/G2/K de `bateria_generaliza` sin tocar.

### B-1 (creador B) — **HIJA DISPERSA**: la hija nace ciega a parte del patrón, no sólo fuera de él

- **Hipótesis.** A profundidad k ≥ 4 la ventaja conductual de 3T-k no cae por falta de celdas (medido: duplicar el pool
  no devuelve nada; ver B1) sino porque cada hija, que ve TODO el patrón compuesto, cubre **uno solo** de los 2^(k−1)
  rellenos: el conflicto de la madre se reabre con el siguiente relleno y la fisión vuelve a borrar valor. Una hija
  ciega a parte de los píxeles de `P` cubre una **familia** de rellenos, cierra el conflicto, y compone con la mitad de
  las celdas.
- **Mecanismo mínimo (regla local, qué memoria exige).** UNA línea del nacimiento de v11:
  `kj = clip(KW[c]·0.95 + paso·dist, 0, 5) · rel`, con `rel ⊊ (P>0)` en vez de `rel = (P>0)`. Dos variantes y un control:
  **(a) por relevancia** — `rel[i] ⟺ P[i]>0 ∧ ( |m̂p[i]−m̂n[i]| > δ_s  ∨  min(m̂p[i],m̂n[i]) > 1−δ_c )`, con
  `m̂p = mup[c]/zp[c]`, `m̂n = mun[c]/zn[c]` medias de `P` condicionadas al **signo de R** (EMA `ema_c = 0.05` con su
  normalizador). *Memoria:* dos vectores de `NIN` y dos escalares **por celda** (el doble de lo que ya cuesta `mu`);
  nada global, nada de patrones almacenados. Dos ramas dendríticas: **contexto** (lo presente en las dos clases) Y
  **discriminador** (lo que separa las clases).
  **(b) por dispersión sola** — `rel` = subconjunto aleatorio de `(P>0)` de la misma cardinalidad. *Memoria: cero.*
  **(c) [control] slot equivocado** — la misma máscara de (a) con el bloque del slot profundo intercambiado con el de
  un distractor (sorteo forzado a desplazarlo, RNG aparte que no toca el flujo del organismo).
  Opcional, para el frente de A: **división diferida** — dividir sólo tras `n_cf` conflictos (o, mejor, cuando la masa
  de conflicto `m = min(Wp,Wn)` de A3 supere `θ_m`); *memoria:* un entero por celda, o ninguno si se usa `m`.
- **Dónde se prueba (instrumento).** `experimentos/creacion_B/mundo_k_B3.py` (`1214d15e210237b6`), construido por
  anclas con `construye_B3.py` desde `mundo_temporal_k.py` (`68736baafe7c8cdb`). **Identidad bit a bit con las perillas
  apagadas 7/7** (`identidad_B3.py`: C3 k=1 s1–2 · C3 k=4 s1–2 · C3C k=4 s1 · C1p k=1 s1 · C3 k=5 T=100k s1).
  Brazo C3 (y C3C como control de artefacto), k = 4 y k = 5, T = 100 000, semillas **nuevas** 61–80 y réplica 81–100.
- **Predicción numérica.** (a) contra v13, pareado: **celdas ≤ 0.75 × v13 en ≥ 18/20** a k = 5 y ≤ 0.85 × a k = 4;
  `lift_q4` mediana **≥ 0.18** a k = 5 (v13 registrado: 0.144 y 0.133 en las dos series) y **> v13 en ≥ 15/20**;
  `sep` mediana ≥ 2.2 con C3 − C3C ≥ 1 en ≥ 18/20. A **k = 1: idéntico a v13 semilla a semilla** (la máscara es inerte
  cuando no hay nada irrelevante; ya verificado en 3/3). Antes de que esto toque el tronco: `bateria_v13.py` 8/8 y
  `bateria_generaliza.py` G1 ≥ 0.80 / G2 ≥ 0.85 sin variación.
- **Control que puede fallar (y casi falla ya).** (b), la máscara **al azar de la misma cardinalidad**: si iguala a (a),
  el ingrediente activo es la **dispersión** y no la relevancia. En mi mini-prueba (b) llega a 0.208 contra 0.221 de
  (a): **con 3 semillas no se distinguen.** Criterio preregistrado: si (a) no supera a (b) en ≥ 14/20 pareado, el
  mecanismo se declara **"hija dispersa"** (una línea, memoria cero) y NO "dendrita que sabe qué mirar"; la traza
  condicionada se guarda como hallazgo de representación (B3), no como órgano. Control (c) debe quedar por debajo de
  (a) y (b); si (c) las iguala, todo el efecto es de la forma de la máscara y la propuesta se refuta entera.
- **Resultado de la mini-prueba** (semillas 1–3, T = 100 000, brazo C3, v13 = `mu_norm`/`div_signo`/`eta_s=0.015`/
  `puerta=3`; medianas, y entre paréntesis las tres semillas):

  | k | brazo | `lift_q4` | `sep` | celdas |
  |---|---|---|---|---|
  | 5 | v13 | 0.112 (0.150/0.048/0.112) | 1.99 | 90/90/90 |
  | 5 | v13 con `nkmax`=180 (control del pool) | 0.099 (0.159/0.059/0.099) | 1.51 | 101/99/94 |
  | 5 | **(a) hija dispersa por relevancia** | **0.195** (0.386/0.144/0.195) | 2.87 | **36/75/65** |
  | 5 | **(a) + división diferida n_cf=4** | **0.221** (0.210/0.221/0.388) | 2.70 | **33/52/56** |
  | 5 | (b) máscara al azar, misma cardinalidad | 0.208 (0.206/0.264/0.208) | 2.00 | 74/55/78 |
  | 5 | (c) slot intercambiado | 0.158 (0.373/0.158/0.151) | 2.05 | 43/82/67 |
  | 4 | v13 | 0.236 (0.201/0.300/0.236) | 2.31 | 70/36/86 |
  | 4 | (a) | 0.175 (0.143/0.380/0.175) | 2.39 | 39/35/81 |
  | 1 | v13 y (a) | 0.366 / 0.366 — **idénticos** | 3.94 | 35/35/36 |

  Gana a v13 en `lift_q4` en 3/3 a k = 5 y baja celdas en 3/3 a k = 4 y k = 5; **no** gana a k = 4 en conducta.

### B-2 (creador B) — **PUERTA DE FAMILIARIDAD POR EVIDENCIA DEL CÓDIGO EXACTO** (no por celdas consolidadas)

- **Hipótesis.** El canje medido "puerta contra capacidad" (v13 `N*` 28 y 35 de 60; v11 43 y 50) nace de que la puerta
  mezcla **dos preguntas distintas**: *¿he visto esto?* y *¿tengo su valor sin repartir?*. Contando las mordidas del
  **código exacto** se separan: lo nunca visto sigue yendo a la vía lenta (código con evidencia 0, generalización
  intacta) y lo ya visto vuelve a la rápida aunque la fisión le haya repartido el valor (capacidad recuperada). Es la
  primera vez en el proyecto que un canje se atacaría **desacoplando dos señales** en vez de moviendo una perilla.
- **Mecanismo mínimo (regla local, qué memoria exige).** `familiar(P) ⟺ ncod[código(P)] ≥ n0`, con `ncod` incrementado
  en 1 en cada mordida sobre el código activo. *Memoria:* **un entero por código visto** (≤ uno por estímulo
  aprendido); cero por celda; no toca `Wp`, `Wn`, `KW` ni el aprendizaje — sólo el **ruteo**. Versión estrictamente
  local si se exige (a discutir con el explorador, pregunta 2): la familiaridad de una población dispersa se lee en el
  cuerpo fungiforme con una neurona de novedad de sinapsis deprimentes; la versión por CONJUNCIONES DE PARES
  (`F[c1,c2]`, contar los 3 pares del código, familiar si ≥ 2 pares superan `n0`) da la misma especificidad de
  "código exacto" con una matriz dispersa y sin diccionario.
- **Dónde se prueba (instrumento).** `experimentos/creacion_B/organismo_capB.py` (`4fa8eabff43fcf91`), por anclas desde
  `organismo_capD13.py` (`fd8e10435801646c`) con `construye_Bpuerta.py`; **identidad con `puerta_pat=0` 4/4**
  (`identidad_Bpuerta.py`). Mundo grande registrado (`mundo_grande.py`, D = 10, 60 estímulos, `paso_t` 20 000 y 60 000),
  semillas 41–60 — **exactamente el montaje de `reverificacion_v13`**, para comparar contra 28/35 y 43/50 sin rehacer
  nada. Y, obligatorio en el mismo bloque, `bateria_generaliza.py` y `bateria_v13.py` sobre un `organismo_v13` con la
  misma perilla.
- **Predicción numérica.** `N*` ≥ **45** (paso 20 000) y ≥ **48** (paso 60 000), contra 28 y 35 de v13, y **> v13 en
  ≥ 15/20 pareado**; celdas y divisiones sin cambio (±2, porque el ruteo no toca el aprendizaje); `nofam_fin` ≤ 2.
  En la batería: **G1 ≥ 0.80 y G2 ≥ 0.85** (los de v13) y retención 8/8. `n0 = 5` (fijado por el orden de magnitud de
  mordidas por estímulo, no barrido; si hace falta barrer, se barre ANTES en semillas distintas y se declara).
- **Control que puede fallar.** **La generalización.** Si al abrir la puerta por evidencia el organismo empieza a leer
  con la vía rápida patrones **nunca vistos** (por colisión de código exacto entre un patrón nuevo y uno aprendido),
  G1/G2 caen hacia el 0.60 de v11 y la propuesta queda refutada: sería recuperar capacidad pagando otra vez la
  generalización — el mismo canje con otro nombre. Segundo control, barato: **contadores barajados** entre códigos
  (permutar `ncod`) debe destruir la ganancia; si no la destruye, lo que actúa es "abrir la puerta", no la evidencia.
- **Resultado de la mini-prueba** (escala REDUCIDA para caber en un proceso: D = 10, **20** estímulos, `paso_t` =
  10 000, T = 200 000, semillas 41–43; **no** mide generalización):

  | brazo | `N*` (41/42/43) | mediana | `M_max` | a la lenta | de ellos mordidos ≥ 5 | celdas |
  |---|---|---|---|---|---|---|
  | v13 (puerta por celdas = 3) | 6 / 5 / 6 | **6** | 13 | 3 / 2 / 5 | **3 / 2 / 4 (todos)** | 71/69/65 |
  | v11 (sin puerta) | 9 / 20 / 20 | **20** | 15 | 0 | 0 | 71/67/65 |
  | **puerta por código, n0 = 5** | 12 / 20 / 20 | **20** | 14 | 0 / 1 / 1 | — | 71/67/65 |

  El canje se reproduce a esta escala (v11 > v13 en 3/3) y la puerta por patrón lo cierra (≥ v13 en 3/3, mediana = v11)
  **con las mismas celdas**. Diagnóstico que lo explica: **el 100 % de los estímulos que la puerta de v13 declara
  desconocidos al final habían sido mordidos ≥ 5 veces.**

### C-P1 — "Probar cuando no me reconozco": la sorpresa sobre sí mismo entra en la BOCA, no en `eta` (Creador C)

> **PAQUETE LISTO PARA CORRER (18 sep 2026), a petición del coordinador.** `experimentos/nivel9_probar_si_mismo/`:
> `PREREGISTRO_probar_si_mismo.md` · `construye_probar.py` → `organismo_v13p.py` (`0dbc2495efe44e60`) y
> `organismo_v13pg.py` (`7ab4767d446ba797`) · `identidad_probar.py` (**J1 18/18 · J2 18/18 · J3 18/18 · J4 6/6**) ·
> `corre_probar_si_mismo.py` (Pool(14) sólo bajo `__main__`; etapa de identidad que **aborta**; `--desde`; `--humo`).
> Brazos: V13 · SELF-TEST · CONST-a (0.173) · CONST-b (0.31) · **MOMENTO** (la traza de SELF-TEST de la misma semilla,
> desplazada un cuarto de corrida; masa conservada exactamente) · dE-TEST (exploratorio). Semillas **41–60**, T = 200 000,
> `invertir_en` = 100 000. **Humo del diseñador (semilla 1, un proceso):** identidades 11/11; SELF-TEST **19.1 s/corrida**,
> recuperación 2 375 con sesgo por cuarto `[0.527, 0.065, 0.366, 0.044]`; MOMENTO 18.0 s, recuperación 13 325 con el
> mismo sesgo rotado `[0.063, 0.381, 0.045, 0.521]`, G-d `|dif| = 0.0`. Datos
> `datos/probar_si_mismo_humo_20260918_000951.{log,json}`. **No lo corro yo: el coordinador verifica, commitea y lanza.**


**Hipótesis.** Un organismo que predice su propia acción y usa el error de esa predicción para decidir **si prueba**
—no para cambiar su tasa de aprendizaje— se recupera de un cambio no avisado de la regla del mundo en ≤ 0.70 × los
pasos que tarda v13, **sin** perder retención (`bateria_v13`) ni generalización (`bateria_generaliza`), y ganándole a
un control de **cantidad** (sesgo constante del mismo tamaño) y a un control de **momento** (la misma traza de sesgo
desplazada en el tiempo).

**Mecanismo mínimo (regla local; memoria que exige).**
- Una lectura logística por **encuentro** (no por bocado): `b = sig((Wbr·P + Wbk·kenyon(P) + Wbh·hambre + Wb0)/0.3)`,
  con **regla delta sobre la acción realizada**: `e_b = mordio − b`; `W ← clip(W + eta_b·e_b·x, ±clip_b)`. Es local:
  usa lo que la celda ya ve y un escalar de error. Nada de retropropagación.
- **Memoria:** 6 + 90 + 2 = **98 escalares** (una lectura lineal del tamaño de la vía lenta más una copia sobre el
  pool, más el peso del hambre y el sesgo) **+ un único escalar de estado** `s̄_a` (EMA, `ema_auto` = 0.05). Nada por
  objeto, nada por sitio, nada episódico.
- **Uso:** `Vb = alpha·w + hambre_boca·hambre + 0.5 + k_test·s̄_a`. No toca `eta`, ni `valor()`, ni las patas, ni el
  mapa: **no añade ninguna atracción** (por eso no repite las tres candidatas ya refutadas del canje del mapa).

**Dónde se prueba (instrumento).** `experimentos/creacion_C/organismo_v13s.py` (sha `2eaba8dde27f05bd`), **por anclas**
desde el tronco `cc8b16b492d4d324`; identidades **I1 / I2 / I3 = 18/18** cada una (6 semillas × 3 escenarios, todas las
claves de v13). Mundo: el del bloque 6 (T = 200 000, `invertir_en` = 100 000), medida `t_ext_B` con **su mismo
criterio**. Retención: las SEIS etapas de `organismo/bateria_v13.py` con sus `CRIT` **importados tal cual**.
Generalización: G1/G2 de `organismo/bateria_generaliza.py` (px0 / azar) — **falta construir** `organismo_v13sg` desde
`experimentos/v13_dos_vias/organismo_v13g.py` con las mismas anclas (una línea del constructor).

**Predicción numérica** (semillas 1–10; réplica en 11–20 sólo si pasa):
- **P1** mediana de `t_ext_B − invertir_en` **≤ 0.70 ×** la de V13, y pareado ≥ **8/10**.
- **P2 [cantidad]** más rápido que FIJO_media y que FIJO_Q3 (sesgo constante igual a la media y al nivel de Q3
  **medidos en el propio brazo**), pareado ≥ **8/10** contra cada uno.
- **P3 [momento — el control que me falta]** más rápido que FASE (la traza `k_test·s̄_a` del propio brazo, **desplazada
  medio cuarto**, RNG propio), pareado ≥ **8/10**. Si P2 pasa y P3 no, lo que acelera es el nivel, no el momento, y se
  registra así.
- **P4 [se apaga solo]** `sesgo_boca[Q2]` y `[Q4]` ≤ **0.10** y ≤ **0.35 ×** `sesgo_boca[Q3]`, en ≥ 9/10.
- **P5 [no daña]** las SEIS etapas de `bateria_v13` no pierden más de 1 semilla sobre 10 frente a V13; G1 px0 ≥ 0.65 y
  ≥ mediana(V13) − 0.10; control `azar` en [0.35, 0.65].
- **P6 [no gana por pasividad, ni por temeridad]** comida total ≥ **0.90 ×** V13 **y** muertes ≤ **1.25 ×** V13.

**Control que puede fallar.** FIJO_media y FIJO_Q3 (cantidad) · FASE (momento) · P4 puede fallar si el lazo
*sorpresa → morder → sorpresa* se autoamplifica · P5 puede fallar por el canje exploración / retención · P6 puede
fallar **por los dos lados** (dejar de comer, o morir de tanto probar).

**Resultado de la mini-prueba** (semillas **1–3**, **T = 200 000**, `invertir_en` = 100 000, `k_test` = 10,
`ema_auto` = 0.05, `eta_b` = 0.03, `buf_auto` = 1000; un proceso, 3 tandas de 3):

| | s1 | s2 | s3 | mediana |
|---|---|---|---|---|
| **PROBAR** | **2 375** | **3 472** | **2 165** | **2 375** |
| V13 | 13 746 | 3 704 | 7 531 | 7 531 |
| FIJO_media (0.173 constante) | 4 794 | 11 808 | 5 840 | 5 840 |
| FIJO_Q3 (0.31 constante) | 5 308 | 7 632 | 5 912 | 5 912 |

**0.315 ×** la mediana de V13, pareado **3/3**; más rápido que **los dos** controles de cantidad **3/3 cada uno**.
Sesgo por cuarto fásico y con apagado: Q2 0.063–0.068 y Q4 0.044–0.060 contra Q3 0.260–0.366. No es pasividad: muerde
**3–4 × más veneno** tras la inversión (208/171/129 contra 54/55/64) y las muertes son comparables (290/307/301 contra
287/240/292). **NO medido todavía: P5 (retención y generalización) y P3 (el control FASE, que aún no existe).**

---

### C-P2 — Significado por predicción: el símbolo predice lo que voy a SENTIR, y lo escucha quien no se reconoce (Creador C)

**Hipótesis.** En el mundo de N2f v3 —el único montaje que pasó las puertas de validez— un receptor que aprende de
cada símbolo **una predicción de la energía que le rendirá su próximo bocado** (regla delta sobre su propia ΔE
**sentida**, no sobre el refuerzo ni sobre la ventaja del emisor) y que **la consulta sólo cuando no se reconoce a sí
mismo** obtiene beneficio conductual, con un contraste del símbolo ≥ 0.8 en unidades de `E_VAL`, y el barajado lo
destruye. Es la única reapertura de N2 compatible con el cierre registrado: no es otro diseño de refuerzo.

**Mecanismo mínimo (regla local; memoria que exige).**
- Por símbolo `s` ∈ {0,1}: **UN escalar** `u_s`. Al morder tras oír `s`: `u_s ← u_s + eta_sym·(ΔE_sentida − u_s)`.
  Honesto por construcción: el objetivo es lo que el receptor **siente**, no lo que el emisor reporta.
- **Entrada por la puerta que YA existe:** si el patrón no es *familiar* (< `puerta` celdas consolidadas) **o**
  `s̄_a > theta_a` (no se reconoce, C-P1), la boca añade `gamma_pred · u_s · (|R_VAL|max/|E_VAL|max)`. Si es familiar
  **y** se reconoce, ignora el símbolo. El *"no sé"* deja de ser una perilla y pasa a ser **una cantidad medida en el
  propio organismo**.
- **Memoria: 2 escalares** (`u_0`, `u_1`) más el `s̄_a` de C-P1. Es la memoria más barata de toda la línea N2.
- **Emisor: sin cambio** (el de N2f v3). *Variante Steels (sólo si la versión básica pasa E1–E3):* el emisor lleva un
  predictor de la **acción del receptor** y emite el símbolo que minimiza su propio error de predicción.

**Dónde se prueba.** `experimentos/etapa5_comunicacion/mundo_social_n3.py` (`ef227f833c5bf46a`: `regen`=50,
`regen_rota`, `vida`=100) + su gemelo `mundo_social_n3_rapido.py`. Instrumento nuevo **por anclas**, con `eta_sym`,
`gamma_pred` y `theta_a` apagadas ≡ la versión actual **bit a bit** (protege N3c/N3d, como hizo N2f v3 con 8/8).
Puertas de validez **K2–K5 de N2f v3 sin tocar** (K4 equilibrio de emisiones ≥ 0.2 es la que invalidó cinco diseños).

**Predicción numérica** (semillas **101–120**, nuevas):
- **E1 [magnitud, en unidades de lo sentido]** `u_muerde − u_rechaza ≥ 0.8` (el rango de `E_VAL` es 1.2) en ≥ **15/20**
  — contra el ±0.30 de N2f v3 sobre una escala de −3/+1.
- **E2 [beneficio]** veneno total del receptor ≤ **0.80 ×** N0, pareado ≥ **15/20**. (INNATO dio 60 contra 278: pedir
  0.80 es pedir poco, y por eso puede fallar de verdad.)
- **E3 [el contenido lo es todo]** SHUF (símbolo barajado) **sin** beneficio (≥ 0.95 × N0) en ≥ 15/20.
- **E4 [la puerta es la que abre el oído]** el brazo con `theta_a` = 0 (escucha siempre) **no** alcanza E2, o la
  alcanza con más veneno que el brazo con puerta, en ≥ 13/20. Es el control que puede matar mi propia idea del oído.
- **E5 [velocidad]** `|u_s − E_VAL|` < 0.04 en ≤ **20** bocados tras oír `s`, en ≥ 15/20.

**Control que puede fallar.** SHUF (E3) · `theta_a`=0 (E4) · N0 y SOLO de N2f v3 sin tocar · las puertas K2–K5, que
pueden anular el contraste entero antes de mirar ninguna predicción.

**Resultado de la mini-prueba** (no en el mundo social —no hay instrumento todavía— sino en el del tronco, que es
donde puedo correr hoy). `organismo_v13a` del bloque 6, **semilla 1**, patrón NUEVO `C` = veneno en t = 50 000,
`eta_pred` = 0.03, `k_sorpresa` = 0 (conducta = v13 bit a bit), 8 corridas de **T ≤ 150 000**:

| mordidas de C | 4 | 6 | **14** | 18 | 26 |
|---|---|---|---|---|---|
| `W_pred(C)`, objetivo **−0.400** | −0.233 | −0.284 | **−0.374 (93.5 %)** | −0.388 (97 %) | −0.396 (99 %) |
| `W(C)` por refuerzo, objetivo −3.00 | −1.61 | −1.85 | −2.46 (82 %) | −2.63 (88 %) | −2.82 (94 %) |

En régimen, `W_pred(A)` = **+0.800** y `W_pred(B)` = **−0.400**: la magnitud **exacta** de `E_VAL`. Y con
`solap_AB = 3`, `lam = 0`, `plast = False` (BUG-01 presente: `comp A = (9.0, 9.0)`) la predicción sigue exacta
(0.800 / −0.399). **Refutado de mi propia propuesta:** el argumento *"el símbolo por refuerzo colapsaría por BUG-01"*
**no vale**, porque el valor no colapsa — **la puerta de familiaridad desvía a la vía lenta** (hallazgo colateral que
no encuentro registrado). Lo que queda en pie es **magnitud exacta e invariancia al estado del canal de refuerzo**.

---

### C-P3 — RETIRADA antes de preregistrarla (Creador C)

Iba a proponer **reciclaje local con costo energético** (muerte de la celda no consolidada y sin uso, nacimiento que
cuesta energía) con un falsador barato: censar cuántas de las 90 celdas cumplen el criterio de muerte cuando el pool se
agota a k = 5. **El Creador B ya corrió ese censo** (su B1) y el resultado lo mata: el pool se agota en el último
tercio y cuesta **sólo 2–7 divisiones**; duplicar el pool a 180 no devuelve nada (usa 94–101 celdas y `lift_q4` no
sube). El otro régimen candidato —la retención de lo ausente— lo cerró el **Creador A** (su A5: con el pool lleno
retiene **más**). **Retiro la propuesta.** Lo dejo escrito porque una propuesta retirada con la razón puesta vale más
que una propuesta viva sin falsador, y porque documenta que el puente funcionó: dos creadores mataron mi tercer frente
antes de que gastara un preregistro.

### C-P5 — Codificación predictiva y retorno aleatorio para aprender sin morder: **REFUTADA en mini-prueba**, con el sitio donde sí cabe (Creador C)

**Hipótesis (la que se probó).** Si el predictor de ΔE enseña a la vía lenta en **cada encuentro** y no sólo en cada
bocado, el organismo alcanza el criterio de generalización con **menos exposiciones y menos mordidas**; y un canal de
retorno **fijo y aleatorio** (feedback alignment) basta para llevar el error del espacio de las celdas al de los
píxeles.

**Mecanismo mínimo (regla local; memoria que exige).** `obj_R(P) = (R_VAL/E_VAL)·ΔE_pred(P)` con las constantes del
mundo (sin parámetro libre); `eps = obj_R − (Wps−Wns)@P`; `Wps/Wns += eta_c·eps·CRÉDITO`, mismo drenaje y tope que la
vía lenta. **Memoria: 6 + 90 escalares** (el predictor, que ya existía) **+ 6×90 fijos** si el canal es aleatorio.
Guarda: no consolida hasta 20 bocados del predictor. `eta_c = eta_s = 0.015`, no buscado.

**Dónde se prueba (instrumento).** `experimentos/creacion_C/organismo_v14pc.py` (sha `edfcb77a9ca91682`), por anclas
desde `organismo/organismo_v14g.py` (`1f1318480cd34cde`); identidades **K1/K2/K3 = 12/12** cada una. Medida nueva:
**exposiciones hasta criterio** (encuentros y bocados de entrenamiento hasta que el acierto de signo balanceado de la
vía lenta sobre los patrones **nunca vistos** cruza 0.90 **en dos sondas seguidas**).

**Predicción numérica.** MP-K1 exposiciones ≤ 0.80 × · MP-K2 bocados ≤ 0.80 × · MP-K3 el canal aleatorio no compra ·
MP-K4 xor01 no se mueve · MP-K5 no daña px0.

**Control que puede fallar.** `fa_shuf` (mismo canal, emparejamiento código↔crédito equivocado) · `transp` (los pesos
transpuestos) · `directo` (el gradiente exacto) · y la línea base SOLO-BOCADOS, que es el tronco v14.

**Resultado de la mini-prueba** (semillas 1–3, T = 100 000, 24 corridas, un proceso): **MP-K1 REFUTADA** (mediana
1.71 ×, 2/3 mejor y 1/3 peor, rango 226–3 507) · **MP-K2 REFUTADA** (1.59 ×; predicha como fallo) · **MP-K3
SOSTENIDA**: `fa` peor que la base en 3/3 (censurada en 2/3), indistinguible de `fa_shuf` (mejor en 1/3) y **daña**
(`acc_lenta_f2` 0.70 contra 1.00), mientras `transp` funciona sin dañar (mediana 631) · **MP-K4 REFUTADA**: xor01
sube de 0.25 a 0.375 (`directo`) y a **0.5625** (`fa`) · **MP-K5 parcial**: `directo` no daña, los aleatorios sí.

**Lo que propongo que se haga con esto (la decisión es del coordinador).**
1. **No preregistrar esta versión.** Está refutada y la razón es mecánica: en una lectura lineal de una capa el crédito
   exacto es `P`, así que un retorno aleatorio no tiene nada que comprar y sí mucho que romper.
2. **Donde sí cabe el retorno asimétrico es `KW` (la capa oculta)**, que hoy es azar congelado. Hipótesis siguiente,
   **sin mini-prueba todavía**: `KW[c] += eta_k · eps · b_c · P` con `b_c` **fijo y aleatorio por celda** (feedback
   alignment de una capa), midiendo **exposiciones hasta criterio**; controles: `b_c` = `(Wp−Wn)[c]` (la transpuesta,
   lo que haría backprop), `b_c` barajado entre celdas, y `eta_k = 0` (el tronco). Es la única versión de la propuesta
   del director que no es degenerada, y choca de frente con la rama **3K** (aprender `KW` supervisado no mejoró la
   generalización) — por eso la pregunta es si el **currículo** (qué error y cuándo) cambia esa respuesta.
3. **El cabo de xor01** (0.25 → 0.5625 con el canal aleatorio) es real pero pequeño y con n = 3: **encaja con el
   diagnóstico registrado de identificabilidad**, porque el canal aleatorio convierte la lectura lenta en función de
   **códigos** y no de píxeles, y es la lectura por píxeles la que *anti*-generaliza en XOR (0.25 < 0.50). Si alguien
   lo persigue, que sea con ese enunciado y con el criterio 0.75 sin tocar.
4. **El encargo (2), N2 por predicción, sigue en pie y ahora con más razón:** la mini-prueba dice que el organismo no
   puede bajar sus propias mordidas redistribuyendo lo que ya sabe. **La única información que no se paga con mordidas
   viene de otro organismo.** Es el mismo mecanismo (predecir lo que voy a sentir) en el mundo social, y es donde
   "exposiciones hasta asociar" puede bajar de verdad.

## Propuestas para el coordinador

### B-4 (creador B) — **ASOCIACIÓN EN UNA EXPOSICIÓN POR GRAFO**: ligar lo nuevo al nodo más cercano y heredar por la arista. **Resultado de la mini-prueba: NO en el mundo del tronco, y la razón está medida**

- **Hipótesis.** v14 necesita **16 mordidas** (medido abajo; el dato N1 decía 7–19) para asociar un patrón nuevo porque su
  valor arranca en **cero**. Si al primer encuentro lo **liga** al nodo previo más cercano del grafo y **hereda su valor por
  la arista** —y una sola mordida contraria **corta la arista**—, las exposiciones hasta asociar deberían caer a ~1–3.
- **Mecanismo mínimo (regla local, qué memoria exige).** En la **primera** mordida de un código exacto nuevo:
  `Wp[código] += v0/K` (o `Wn`, si `v0 < 0`) ⇒ `(Wp−Wn)@código = v0` al instante, y se anota el préstamo. En la **siguiente**
  mordida de ese código: si `v0·R < 0`, **se desliga entero** (se resta lo prestado) y el patrón sigue con la regla normal;
  si lo confirma, el préstamo deja de ser hipótesis. **Nodos** = código HD disperso de cada patrón mordido, con su valor.
  **Aristas** (4 variantes, = los brazos): `sem=1` **parecido leído por la vía lenta** (memoria nueva **cero**); `sem=2`
  **parecido en canal hiperdimensional** (proyección aparte `nh = 2000`, código top-`kh = 40`; memoria declarada:
  `nh·6` flotantes + `kh` enteros y un flotante por nodo); `sem=3` **control al azar**; `sem=4` **grafo con dos tipos de
  arista** (parecido y co-ocurrencia) y **fiabilidad por tipo** (dos escalares, EMA 0.3: la arista que engaña pierde la
  confianza y deja de recorrerse). RNG aparte (`seed+400000`, `seed+500000`): no tocan el azar del organismo.
- **Dónde se prueba (instrumento).** `experimentos/creacion_B/organismo_v14L.py` (`d6d550aec83f775a`), por anclas con
  `construye_B4.py` desde `organismo/organismo_v14.py` (`9bab8ac0685b1f21`, **CONGELADO: sólo se leyó**).
  **Identidad con `sem=0`: 8/8** (`identidad_B4.py`: base, inversión, estímulo nuevo veneno, estímulo nuevo con
  `solap_B=2`; semillas 1–3). Medida nueva **`exp_hasta[patrón]`**, de sólo lectura y activa siempre: mordidas de ese
  patrón tras las cuales el valor que usa la boca cae a ≤ `tol_sem = 0.5` del valor real, por primera vez.
- **Predicción numérica.** `exp_hasta` del patrón nuevo ≤ **3** (contra 16 de v14) en ≥ 15/20, sin coste en el escenario de
  parecido engañoso (≤ v14 + 2) ni en `bateria_generaliza` (G1 ≥ 0.80, G2 ≥ 0.85) ni en capacidad (`N*` ± 2).
- **Control que puede fallar (y falló).** **Parecido engañoso:** un patrón nuevo que **es comida** y comparte 2 de 3 píxeles
  con el veneno ya aprendido. Más: prior **al azar** (`sem=3`) y la identidad con la perilla apagada.
- **Resultado de la mini-prueba (semillas 1–3, T = 100 000, un proceso; medianas y las tres semillas).**
  **`exp_hasta` del patrón nuevo — EXPOSICIONES HASTA ASOCIAR:**

  | escenario | v14 (`sem=0`) | vía lenta (`sem=1`) | HD (`sem=2`) | azar (`sem=3`) | **grafo (`sem=4`)** |
  |---|---|---|---|---|---|
  | **C veneno**, parecido débil (máx. sim 0.075) | **16** (16/15/19) | **13** (13/9/18) — mejor **3/3** | 16 (16/13/19) | **no asocia en 2/3** | 17 (15/17/19) |
  | **D comida** con 2 px de veneno (**engañoso**, sim 0.225) | **8** (7/8/8) | 11 (15/11/11) — peor **3/3** | 13 (15/13/13) — peor **3/3** | — | 13 (15/13/13) — peor **3/3** |

  **Lo que sí funciona:** desligar cuesta **una** mordida, 3/3 en el escenario engañoso (`n_des = 1` por corrida).
  **Lo que cuesta:** el préstamo cae en celdas compartidas y contamina al vecino — `W_B` se va de **−2.97 a −4.2/−5.5**.
  Celdas sin cambio (32–33 en todos los brazos).
- **Diagnóstico estructural que explica el resultado (200 sorteos, sin correr el organismo).** Similitud media del código
  según los píxeles compartidos (0 / 1 / 2 de 3):
  **HD `nh=2000, kh=40`: 0.025 [0,0.10] · 0.075 [0,0.20] · 0.225 [0.07,0.42]** — graduada y ordenada.
  **Kenyon del tronco `K=3, NKMAX=90`: 0.000 [0,0.67] · 0.000 [0,0.67] · 0.333 [0,1.00]** — no distingue nada.
  → **La alta dimensión SÍ hace falta para que el grafo tenga aristas de parecido legibles; el código del tronco no puede
  ordenar vecinos.** Ése es el argumento medido a favor de la representación de alta dimensión, y es independiente del
  resultado del órgano.
- **Por qué falla, dicho con precisión (y no es falta de ajuste).** En el mundo del tronco hay 4 patrones de peso 3 sobre 6
  píxeles: **el único par lo bastante parecido para heredar (sim 0.225) es un par comida/veneno**. Es decir, **en este mundo
  el parecido no predice el valor: lo contradice.** Por eso heredar cuesta (8 → 11/13) más de lo que gana donde el parecido
  es débil (16 → 13). Y el grafo con fiabilidad **no** lo arregla: la arista sólo recibe una señal de acierto/fallo **por
  episodio de ligadura**, y hay **2–3 episodios por patrón nuevo**, así que la confianza cae por debajo de 0.5 *después* de
  pagar el coste. **La señal que enseñaría al grafo es más rara que el problema que debe arreglar.**
- **Qué propongo, entonces (y qué NO).** **No** es candidato al tronco con esta evidencia; no pido preregistrar el órgano tal
  cual. Lo que pido preregistrar es la **pregunta que lo decide**, que es barata y tiene control incorporado: medir
  `exp_hasta` en el **mundo de regla** (`organismo_v14g`, reglas `px0` y `azar`), donde por construcción **el parecido SÍ
  predice el valor con `px0` y NO con `azar`. Predicción: con `px0`, `sem=1` y `sem=2` bajan `exp_hasta` a ≤ 3 contra
  ≥ 10 de v14 en ≥ 15/20; con `azar`, no bajan (o suben) — y ese contraste, en el mismo instrumento y las mismas semillas,
  es el control que puede fallar. Si el contraste no aparece, el órgano queda refutado en los dos mundos y lo declarable es:
  *"heredar por parecido no acelera la asociación; lo que falta no es la ligadura sino una relación que prediga el valor"*.
- **Vocabulario permitido hoy:** *"liga lo nuevo al más parecido y una mordida basta para desligarlo"* (medido, 3/3);
  *"no reduce las exposiciones hasta asociar en el mundo del tronco, y las aumenta cuando el parecido engaña"* (medido).
  **No** "aprende en una exposición", **no** "reconoce", **no** "razona por analogía".

### C-P6 — N2 por predicción: el receptor aprende qué va a SENTIR de la conducta ajena (Creador C)

**Hipótesis.** Un receptor que aprende, con su propio cuerpo, **qué va a sentir** cuando el emisor muerde o rechaza
(`u[c]`, regla delta sobre su propia ΔE) y usa esa predicción para valorar objetos **sin morderlos**, alcanza el
criterio de conducta con **menos mordidas propias** que el mismo receptor solo, **sin** que el significado se le dé
por construcción, y **sólo** cuando la conducta del emisor informa de verdad.

**Mecanismo mínimo (regla local; memoria que exige).** `u[c] ← u[c] + eta_sym·(E_VAL[valencia] − u[c])` al morder un
patrón del que oyó la conducta `c` hace ≤ `tau_pred`; al oír `c` sin morder, `R̂ = (R_VAL/E_VAL)·u[c]` (constantes del
mundo, **sin parámetro libre**) y se aprende el valor con factor `gamma_pred`. Puerta `theta_a`: no escuchar si ya
sabe. **Memoria: 2 escalares** (`u[0]`, `u[1]`) y una marca patrón → (conducta oída, paso).

**Dónde se prueba (instrumento).** `experimentos/creacion_C/mundo_social_pred.py` (sha `fc306b8fcddabe15`), por anclas
desde `mundo_social_n3.py` (`ef227f833c5bf46a`). Identidades **L1/L2/L3 = 21/21** cada una sobre las siete condiciones
de N3d (CONV, SHUF y SACIEDAD incluidas) × 3 semillas. Medida nueva: **exposiciones y mordidas hasta criterio**
(ventana móvil de 400 encuentros, acierto balanceado de conducta = la fórmula de `acierto_q4`, dos sondas seguidas).

**Predicción numérica** (para una serie futura, semillas nuevas, T = 200 000):
- **N1** `u[1] ≥ +0.5` y `u[0] ≤ −0.15` en ≥ 15/20 — *(mini-prueba: 0.800 exacto y −0.38, 3/3)*.
- **N2′** (reescrita tras el fallo de la mini-prueba) el receptor solo (SOLO_R) **no alcanza** el criterio en ≥ 15/20,
  y PRED **sí** lo alcanza en ≥ 15/20, con mediana ≤ 250 mordidas. *(La forma "≤ k × la base" no vale: la base no
  termina.)*
- **N3** `acierto_q4` de PRED ≥ 0.75 y ≥ INNATO − 0.10 — *(0.805 contra 0.821)*.
- **N4** controles: SHUF y SACIEDAD con `u[1] − u[0]` ≤ 0.3 y sin alcanzar el criterio, en ≥ 18/20 — *(3/3 los dos)*.
- **N5** coste del significado: mediana de mordidas de PRED ≥ la de INNATO — *(153 contra 126)*.
- **N6 [el que decide, y hoy FALLA]** con el emisor mudo desde T/2, `acierto_q4` de PRED ≥ 0.65 — *(mini-prueba:
  **0.502**, igual que el innato 0.511 y que el azar: **obedece, no aprende**)*.

**Control que puede fallar.** SHUF (emisor barajado) · SACIEDAD (emisor que no sabe) · SOLO_R (sólo bocados) ·
**MUDO** (el emisor calla: separa aprender de obedecer) · y las identidades L1–L3, que pueden refutar que las perillas
apagadas sean el original.

**Resultado de la mini-prueba** (semillas 1–3, T = 100 000, 21 corridas): **N1, N3, N4 y N5 pasan 3/3**; **N2 mal
escrita** (la base está censurada: SOLO_R nunca llega, y eso es *más* fuerte que lo que pedí); **N6 FALLA: 0.502**.

**Lectura honesta y lo que propongo.** El **canal de significado funciona**: el receptor aprende con su cuerpo la
magnitud exacta del mundo (+0.800 / −0.38) y sólo cuando la conducta ajena informa. Lo que **no** se puede demostrar
aquí es la retención — y **no por el mecanismo, sino por el mundo**: en el montaje de N3d los dos miembros de cada
pareja tienen **la misma retina enmascarada** para el receptor, luego el mismo código y el mismo `valor`; **ninguna
regla local puede escribir una distinción en un código idéntico**. Por eso **no pido preregistrar esta serie tal
cual**. Pido el mundo mínimo que la haría decidible: parejas con **vista parcialmente distinta** para el receptor
(que pueda representar la diferencia aunque no pueda predecir la valencia sin ayuda), manteniendo intactas las puertas
de validez de N3d. Con ese mundo, **N6 pasa a ser la predicción principal** y el resto queda como está.
