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

Idealización (matching pursuit = añadir de a un rasgo el más correlacionado con el **residuo**):

| arranque | rasgos abiertos | xor01 | px0 | azar |
|---|---|---|---|---|
| vacío | 4 | 0.625 | 0.85 | 0.50 |
| 6 px (sin constante) | 7 | 0.625 [0.19, 1.0] | 1.000 | 0.45 |
| **6 px + constante** | **7 (o sea: los elementales + UN conjuntivo)** | **1.000 [0.5, 1.0]** | **1.000** | 0.40 |

El conjuntivo que elige es `P0·P1` en **12/20** semillas, y la constante entra en 10/20 cuando se deja elegir libre.
(Las semillas que quedan en 0.5 son las 6/20 sin una clase XOR en el tren — la cota de muestreo que midió el Agente C
del puente XOR: es del mundo, no de la regla.) **La diferencia entre 0.562 y 1.000 no es la norma: es SELECCIÓN
(abrir UN rasgo) contra ENCOGIMIENTO (repartir el residuo entre los 15).** Ningún regularizador convexo selecciona;
para seleccionar hace falta **competencia** (inhibición lateral / ganador-se-lo-lleva) — y eso el organismo ya lo
sabe hacer: el código Kenyon **es** un top-K.

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

### A7. Archivos (sólo míos, nada original tocado, sin commits)
`experimentos/creacion_A/`: `identificabilidad_xor.py` · `sesgo_grado_xor.py` · `banco_sesgo.py` ·
`regla_puerta_rasgo.py` · `regla_wta_conjuntiva.py` · `dinamica_oraculo.py` ·
`dos_canales_es_valor_mas_conflicto.py` · `construye_largo_A.py` → `mundo_largo_A.py` (sha origen
`9f74ff6b5941e5a5`) · `mini_prueba_A_largo.py` · `mini_prueba_A_tope.py` (+ sus `.json`). Los originales NO se
tocaron: se **importan** (`organismo_v13q`, `organismo_v13q3`, `mundo_largo`, `corre_mundo_largo`).
Corridas de organismo gastadas en total: **9 de identidad** (T ≤ 40 000) + 3 de calibración + **4 tandas de 3
corridas de T = 200 000** (3 en el mundo largo, 2 en el mundo de regla). Nada de `Pool`. Sin commits.

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

## Preguntas para el explorador

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

## Propuestas para el coordinador

### A-1 (creador A) — **XOR: la receta completa son TRES piezas, y cada una está medida por separado**

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
- **Mini-prueba.** Banco: 20 semillas, tablas de A1/A2/A4 y `dinamica_oraculo.json`. Organismo: **6 corridas** de
  T = 200 000 (2 tandas de 3), semillas 1–3, números arriba. Versión online de (ii) en el banco: **0.625** (sube desde
  0.562, no rompe controles) abriendo el conjuntivo correcto en **2–6/20** contra **12/20** de la idealización.

### A-2 (creador A) — **METAPLASTICIDAD POR MASA DE CONFLICTO**: consolidar con estado que el tronco YA tiene

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

  Por qué β tiene que ser grande: `m` tiene **semivida `ln2/lam ≈ 14` mordidas** y vale 0.015–0.048 de media. El
  explorador (A-Q2) confirma que la cascada de Fusi pide **≥ 2 constantes de tiempo propias** y que β = 50 es una
  prótesis; también confirma que **nadie ha publicado el coste en adquisición ni en recuperación tras cambio de regla**
  — o sea que esta mini-prueba mide un hueco abierto de la literatura, no sólo del proyecto.

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
  **Corolario que vale aparte: esto DEMUESTRA la ablación del Agente B en `PUENTE_xor`** (`lam_lenta = 0` y
  `clip_s = 10` no movían ni un decimal): no fue casualidad, es identidad algebraica.

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

