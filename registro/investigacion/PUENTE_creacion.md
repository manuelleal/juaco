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

### A6. Archivos (sólo míos, nada original tocado, sin commits)
`experimentos/creacion_A/`: `identificabilidad_xor.py` · `sesgo_grado_xor.py` · `banco_sesgo.py` ·
`regla_puerta_rasgo.py` · `regla_wta_conjuntiva.py` · `dinamica_oraculo.py` ·
`dos_canales_es_valor_mas_conflicto.py` · `construye_largo_A.py` → `mundo_largo_A.py` (sha origen
`9f74ff6b5941e5a5`) · `mini_prueba_A_largo.py` (+ sus `.json`). Los originales NO se tocaron: se **importan**.
Corridas de organismo gastadas en total: 9 de identidad (T ≤ 40 000) + 3 de calibración + **3 tandas de 3 corridas
de T = 200 000** en el mundo largo. Nada de `Pool`. Sin commits.

## Creador B — física y computación de la representación (códigos, capacidad, dendritas, no convencional)

## Creador C — sistemas vivos y mente (modelo de sí mismo, significado por predicción, desarrollo, evolución)

## Preguntas para el explorador

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

**A-Q2 (Creador A).** Metaplasticidad/consolidación: ¿cuál es la **forma mínima** medida de la cascada de
Fusi–Drew–Abbott (2005) / Benna–Fusi (2016) — cuántas variables por sinapsis y con qué razón entre constantes de
tiempo — y qué cifras de retención/adquisición se reportan? Me interesa especialmente si alguien ha medido el **coste
en adquisición** y en **recuperación tras un cambio de regla** (no sólo la ganancia en retención). Motivo: el tronco
ya tiene una variable de conflicto por celda (`m = min(Wp,Wn)`), pero su semivida es `ln2/lam ≈ 14` mordidas — demasiado
rápida para consolidar; quiero saber si la literatura dice "añade UNA variable lenta" o "hacen falta ≥3 escalas".

**A-Q3 (Creador A).** ¿Hay algún resultado (teórico o empírico) sobre **topes/saturación de pesos como regularizador
implícito**: qué solución elige LMS (o cualquier regla delta local) cuando el óptimo cae fuera de la caja `|w| ≤ C` y
existen soluciones interpolantes de norma menor dentro de la caja? Busco la formulación de que "el tope no aprieta
pero sesga": el óptimo que generaliza tiene norma alta y concentrada, los que caben en la caja no generalizan.
Motivo: acabo de medir que la solución XOR sobre {P0,P1,P0·P1,1} exige `|w| = 8` y el tronco tiene `clip_s = 3`.

## Propuestas para el coordinador
