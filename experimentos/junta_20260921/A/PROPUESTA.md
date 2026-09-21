# PROPUESTA — creador A (matemática del aprendizaje local: reglas, identificabilidad, predicción, criterios)
### Junta del 21-sep-2026. Foco: Q1 (criterio) con prioridad; voto en Q2 y Q3.

Todo lo numérico de aquí sale de `analiza_potencia_Q1.py` (un proceso, **sin simular el organismo**: lee los crudos ya
registrados) → salida completa en `salida_analiza_potencia_Q1.txt`, en esta carpeta. No construí instrumento nuevo, así que
no hay arnés de identidad que pegar: pego la salida del análisis (§ "Salida" al final).

---

## 1. Porcentaje de avance por nivel del brief (mi lectura, con la entrada que la sostiene)

| nivel | % | una frase |
|---|---|---|
| 1 asociación | 100 | cerrado desde el día 2; el examen v3′ lo protege (`CLAUDE.md`, regla 1). |
| 2 desaprender | 100 | E2 20/20 en el tronco y reversión medida en el mundo vivo (`dE5_v2…_crudo_TCii`). |
| 3 generalizar | 90 | v14.2 G1 1.000 / G2 0.967 (21-sep, regla 1); falta generalizar *reglas*, no sólo valor. |
| 4 capacidad | 85 | N\* 51 y alias reparado por B-5 (v14.2, 18-sep); el techo en el **mundo vivo** nunca se midió. |
| 5 comunicación | **70** (el registro dice 75) | nadie cruza la letra en 4 series; y hoy mido que P6 (dist ≥ 15/19) rechaza 1 de cada 5.9 series aunque el mecanismo no cambie (§4). El 75 % descansa en la "misión cruda", que no es la letra. |
| 6 mapa / rodeo | 50 | sin movimiento desde el 17-sep; el canje del mapa es estructural; no planifica. |
| 7 composición / XOR | 60 | compone hasta 3; XOR cerrada como **prior de pares declarado**; la línea v15c–v15g cerró el 21-sep **sin entrar**: el nivel se acotó, no avanzó (HANDOFF 15.16). |
| 8 aprendizaje abierto | 35 | dE5 mide capacidad real (recupera 3.23×) pero cobra veneno; órgano medido, no órgano (HANDOFF 15.19). |
| 9 autonomía / sí mismo | 30 | fase 9 bloque 1: 8/10 puertas, **sin réplica**; H-1 y ERR-62 en pie (HANDOFF 15.18). |
| 10 transmisión / vivo | 10 | exploratorio (serie ALMA, mundo de familias). |

Transversal: la regla 5 de `CLAUDE.md` ("ante una anomalía, la primera hipótesis es el instrumento") vuelve a ganar. Iba 3 de 3; hoy va **4 de 4**.

---

## 2. Q1 — ¿T-A y T-C (ii) son capacidad o no-regresión? **VOTO: las dos son de NO-REGRESIÓN, y hoy no lo son.**

**El cálculo (§2, §3, §8 de la salida).** `A₁₂` en el runner es **pareado por semilla**: `P(x>y)+0.5·P(x=y)` sobre n = 20
pares. Es decir, una prueba de signo. Su distribución bajo "el candidato ES el tronco" (p = 0.5) es Bin(20, 0.5)/20. De ahí:

- **La letra de T-A (`A₁₂ ≥ 0.50`) rechaza a un candidato idéntico al tronco el 41 % de las veces**, y eso **no mejora con más
  semillas**: n = 40 → 0.563, n = 80 → 0.544, **n → ∞ → 0.500**. Un umbral puesto exactamente en el valor del nulo es, en el
  límite, un volado. No es un defecto de potencia: es un defecto de forma.
- **La letra de T-C (ii) (`A₁₂ ≥ 0.75`) es una puerta de capacidad**, y con n = 20 sólo ve efectos enormes: para cruzarla con
  probabilidad 0.80 hace falta ganar al tronco en el **80 % de las semillas**. Con el ruido real de `rev` (sd de la diferencia
  23–30) eso son **+21 a +23 puntos de `rev` sobre una mediana de 37–45**: ~+50 %. Un candidato que revierta un 25 % mejor que
  el tronco **cae el 80 % de las veces**.
- **Banda ciega en unidades naturales** (§3b): T-A pasa-80 % en Δr ≥ +2.5 y cae-80 % en Δr ≤ −4.5. Pero el propio T-A **declara**
  tolerar Δr = −10. **La cláusula `A₁₂` es más dura que el margen declarado en el mismo renglón, y nadie lo escribió.**

**El nulo medido, con corridas reales del tronco (§8 — esto es lo que cierra el asunto).** Los brazos OFF de v15f-v2
(301–320) y de dE5-v2 (2021–2040) son **el mismo organismo**: v14.2 con la perilla apagada, mismo mundo `corre_vivo_rep2`,
mismo T, mismo runner. Son dos muestras de la misma ley. Repartiendo esas **40 semillas reales del tronco** al azar en dos
brazos de 20 —un candidato-placebo perfecto, "el tronco disfrazado de candidato"— y aplicando **la letra completa**:

```
VIVO        muertes<=1.10x 0.993   r>=tronco-10 0.985   A12>=0.50 0.567   brazo entero 0.567
CUELLO_MIN  muertes<=1.10x 0.951   r>=tronco-10 0.954   A12>=0.50 0.561   brazo entero 0.558
>>> T-A ENTERA sobre el placebo perfecto:  PASA 0.316   (CAE 0.684)
>>> sin la cláusula A12 (sólo las dos medianas declaradas): PASA 0.909
>>> T-A y T-C (ii) juntas:  PASA ~ 0.006
```

**El tronco, presentado como candidato, no entraría al tronco: probabilidad 0.6 %.** El criterio v2 nunca corrió su propio
control negativo. Ese es el ERR.

**Contraargumento honesto, y por qué no me convence.** Se puede defender `A₁₂ ≥ 0.50` como conservadurismo deliberado ("ante
la duda, no se toca el tronco"). Pero entonces es una puerta de **capacidad** mal nombrada: se llama "sobrevive" y exige
"sobrevive mejor". Y es incoherente con la propia práctica: **B-5 entró como v14.2 siendo inerte**. Si el criterio exige ganar
en supervivencia, ningún órgano inerte-pero-útil puede volver a entrar nunca.

**Respuesta a la pregunta literal:** T-A y T-C (ii) **deben ser de no-regresión**; la capacidad nueva ya tiene su puerta
(T-G, con control barajado y azar en banda). Hoy T-A es de capacidad **por accidente estadístico** y T-C (ii) de capacidad
**por la letra**, dentro de una puerta cuyo nombre ("se desdice") describe algo que el tronco ya hace. `v15f` y `dE5`
conservan la conducta E2 20/20 —se desdicen tan bien como el tronco— y se les reprochó no desdecirse **mejor**.

**Mi lectura de lo ya medido, como diagnóstico del instrumento y NO como veredicto (regla 3: nada se rejuzga; v15f y dE5
siguen fuera):** con el margen que T-A ya declara (Δr = 10), los **cuatro** casos T-A medidos hoy son **no inferiores**
(límites inferiores −8.4, −4.2, −7.4, −9.6 > −10) y el IC90 del signo de los cuatro **contiene 0.50**. Con n = 20 la letra
no puede separar "igual al tronco" de "peor": **no**, no puede. Ése es el resultado que pide la misión.

**Predicción Q1 (refutable).** Si la letra no cambia: en las próximas 3 series bajo v2, `A₁₂(T-A)` caerá en [0.35, 0.65] en
≥ 5 de los 6 brazos medidos, y ningún candidato cruzará T-C (ii) (P ≥ 0.95 de que caiga). Me refuta: un candidato que cruce
T-C (ii) con `A₁₂ ≥ 0.75` **y** cuyo efecto en unidades naturales sea < +15 puntos de `rev` (sería ruido afortunado, no
mecanismo) — o uno que la cruce con efecto ≥ +20 (entonces la puerta sí discrimina y mi lectura de su potencia es correcta
pero irrelevante en la práctica).

---

## 3. Q2 — Fase 5. **VOTO: correr la réplica (ya en cola, preregistrada) y, si cae P6, CERRAR fase 5 en 75 %.**

Aporte de mi línea: **P6 tiene la misma patología de umbral que T-A**, pero por potencia, no por forma. `dist(PAR)` de BA-v en
las tres series: 18/19, 17/19, 13/19 → agregado **48/57 = 0.842**, IC90 **[0.741, 0.915]**; χ² de homogeneidad **5.54 < 5.99**:
las tres series son compatibles con **un solo p**. Y con p = 0.842, `P(dist ≥ 15/19) = 0.830`: **una serie de cada 5.9 cae por
la letra aunque el mecanismo no haya cambiado**. La caída de 961–980 no es evidencia de que BA-v no lea el referente; es lo
que hace un umbral de conteo cerca del valor verdadero.

Por eso mismo **no propongo bajar el umbral** (sería recalibrar tras ver datos, ERR-3/regla 3/regla 11). Propongo: la réplica
corre con la letra intacta; si cae, **fase 5 se cierra en 75 %** y se registra aparte, como dato y no como declaración, el
agregado de las cuatro series con su IC y el control barajado (0/19). **Y se prohíbe abrir un candidato nuevo de fase 5 bajo
una puerta de conteo k/n sin su cálculo de potencia escrito antes** (eso entra en el criterio v3 del bloque §5).

Mecanismo que nadie probó, si el director quiere el 25 % restante (lo dejo enunciado, el detalle es de B/C): **jerarquía
temporal en vez de conjunción simultánea** — una sola tabla con dos ranuras, y la ranura de la variante sólo se emite cuando
la de la familia ya está consolidada (memoria nueva **cero**: la segunda ranura reusa la tabla existente). Predice `BAR-H`
bajo sin tocar `dist(PAR)`, que es exactamente donde BA y BA-v se pisan.

---

## 4. Q3 — Fase 9. **VOTO: NO, la letra de F9-4 no mide lo que quería medir. Es la trampa 2 aplicada al control.**

F9-4 = `A₁₂(vida REL > REL_BAR) ≥ 0.80` **y** `p1(REL_BAR) ≤ p1(NADA) + 0.15`. Lo medido: `A₁₂ = 1.0` (pasa) y
`p1(REL_BAR) = 0.568 > 0.344` (cae). Pero `c1(REL_BAR) = 0.598`. Con el índice **balanceado** J = p1 + c1 − 1 (Youden, el
mismo que exige la regla 5 de EQUIPO, "acierto sin balancear"):

| brazo | p1 | c1 | **J** |
|---|---|---|---|
| REL | 0.962 | 1.000 | **0.962** |
| REL_BAR (nodo barajado) | 0.568 | 0.598 | **0.166** |
| NADA (cuerpo vacío) | 0.194 | 0.992 | **0.186** |

`J(REL_BAR) = 0.166 ≤ J(NADA) = 0.186`: el nodo barajado **no discrimina nada**, exactamente lo que F9-4 quería afirmar. La
cláusula falló porque puntúa al control con un acierto **sin balancear**, y la cautela genérica infla `p1` gratis. La letra
midió "¿rechaza veneno?" cuando quería medir "¿sabe cuál?".

**Qué hacer sin trampa:** la réplica 1521–1540 corre con la letra **intacta** y F9-4 se reporta como cae (nada se rejuzga).
La cláusula balanceada entra como **F9-4b** en el preregistro del bloque 2, con **semillas nuevas**, y con ERR numerado por
ser cambio de forma de criterio (regla 11). **Predicción (antes de la réplica):** en 1521–1540, `p1(REL_BAR) ∈ [0.45, 0.70]`
(F9-4 vuelve a caer) y `J(REL_BAR) ≤ 0.35` mientras `J(REL) ≥ 0.85`. Me refuta: `J(REL_BAR) > 0.45`.

**Bloque 2 de la fase 9 (mi voto):** con H-1 en pie (mejor R₀ = 0.494 con `rep_acum=1`; se pide 0.9) la población todavía no
es alcanzable, y lanzarla ahora repetiría ERR-62. El bloque 2 debe ser **dosis-respuesta de la herencia**: R₀ en función de
*cuánto* nodo se hereda (0 %, 25 %, 50 %, 100 %, y un nodo **oráculo** perfecto como cota superior). Refutador limpio: si ni
siquiera el nodo oráculo cruza R₀ = 0.9, **el muro es el mundo y no la herencia**, y hay que cambiar el mundo antes de
hablar de población. Eso es una medida, no una apuesta.

---

## 5. MI BLOQUE SIGUIENTE — **A-CAL: "el criterio se calibra contra su propio placebo" (criterio v3, ERR-91)**

**Hipótesis.** Un criterio de tronco sólo es un instrumento si (a) deja pasar al **placebo** —un candidato cuya ley es la del
tronco— con probabilidad ≥ 0.90, y (b) rechaza con probabilidad ≥ 0.80 a un candidato peor que el **margen declarado**. El
criterio v2 falla (a): medido hoy con corridas reales, el placebo pasa T-A con 0.32 y T-A∧T-C (ii) con 0.006. La letra v3
(no inferioridad en unidades naturales, con el margen que v2 ya declara) cumple las dos.

**Mecanismo mínimo y memoria nueva: CERO.** No toca el organismo. Cambia la letra y **añade un brazo obligatorio PLACEBO** a
todo paquete de criterio. La letra v3:
- **T-A**: se **elimina** `A₁₂ ≥ 0.50`; quedan las dos medidas ya declaradas (`r ≥ tronco − 10`, `muertes ≤ 1.10×`) juzgadas
  por **no inferioridad pareada de una cola al 95 %**, con **n = 40** por brazo (la sd medida de la diferencia es 11–19.5; con
  margen 10 hacen falta n = 34–42 para que el placebo pase el 95 % de las veces — §4 de la salida).
- **T-C**: (i) intacta (es absoluta y sana). (ii) pasa de "ganar" a **no inferioridad con margen 10 en `rev`**; la exigencia de
  **ganar** se traslada a T-G, donde vive la capacidad declarada.
- **Regla general v3**: *ninguna puerta usa un umbral igual al valor del nulo*, y **toda puerta declara antes de correr su
  nulo, su margen y la n que da 0.95 bajo el nulo y 0.80 en el margen**. Toda puerta de acierto se reporta **balanceada**
  (J = p1 + c1 − 1), no con una sola tasa (Q3).
- **Alcance (regla 3):** v3 vale sólo para candidatos **futuros**. v15c/d/e/f/g, dE5, BA/BA-v y B-5 **no se rejuzgan**.

**Instrumento y anclas.** `organismo_v142.py` (`17528d767fcebaf6`) + perilla `placebo = k`: consume k sorteos del generador por
paso y **descarta** el valor (ninguna decisión los mira). `corre_criterio_v3.py` por anclas desde `corre_dE5_v2.py`
(paquete `9ac631c`), importando —no copiando— `corre_vivo_rep2`, `mini_vivo`, `corre_sal`. Umbrales en `umbrales_v3.py`
importado por el runner (ERR-31). Identidad: `placebo = 0` ≡ v14.2 **bit a bit** (arnés obligatorio antes de mirar números);
humo de un proceso que **escribe su JSON** (ERR-42); entrada campo a campo contra el tronco (regla 14).

**Predicción numérica (con rango).**
| id | qué | predicción |
|---|---|---|
| CAL-1 | el placebo pasa **T-A v3** (n = 40, margen 10) | **0.90–0.98** |
| CAL-2 | el placebo cae **T-A v2** (n = 20) | pasa **0.25–0.40** (hoy reconstruido: 0.316) |
| CAL-3 | v3 rechaza un candidato en δ = −20 puntos de r | cae **≥ 0.95** |
| CAL-4 | marginales del placebo vs tronco (r, muertes, rev, dos brazos) | `A₁₂` **no pareado** en **[0.40, 0.60]** en las 6 comparaciones |
| CAL-5 | el placebo cae **T-C (ii) v2** | pasa **0.01–0.05** |

**Control que puede fallar: CAL-4.** Si consumir un sorteo por paso **cambia la ley** (p. ej. porque el número de sorteos
depende del estado y desincroniza algo), el placebo no es placebo y el bloque se anula. Plan B ya validado y sin CPU: el
placebo por **reparto al azar de 40 corridas reales del tronco** (§8 de la salida de hoy).

**Qué lo refuta.** (i) Si el placebo pasa T-A v2 en ≥ 0.85 de los repartos, mi diagnóstico es falso y v2 se queda. (ii) Si v3
deja pasar δ = −20 en > 0.10, v3 es demasiado laxa y se retira. (iii) Si CAL-4 sale fuera de [0.40, 0.60], el instrumento
está roto y no se lee nada.

**Semillas NUEVAS propuestas** (verificadas libres con grep sobre `registro/` y `experimentos/`; los únicos aciertos de
"1541"/"2101" son un hash y un número decimal, no semillas): **2101–2140** (T-A placebo, 40 pareadas × 2 brazos),
**2141–2160** (T-C ii placebo), **2161–2180** (réplica). Rango `2181+` libre para el siguiente candidato real.

**Las cuatro trampas.** (1) *Canal simétrico*: no hay canal. (2) *Acierto sin balancear*: **es la trampa central del bloque**
— v3 la prohíbe explícitamente (toda tasa con su par; J en fase 9). (3) *Mundo que se come la comida*: `rev` depende de las
exposiciones a B en Q4; v3 exige **reportar exposiciones por cuarto** junto a `rev` y declarar por qué no se normaliza si no
se normaliza. (4) *Sitios fijos*: no aplica (mundo vivo con recursos móviles).

**Coste.** 240 corridas de T = 100 000 (T-A 40 × 2 brazos × 2 arms + T-C ii 40 × 2) ≈ lo mismo que dE5-v2 (15 min con Pool 10).
Lo corre el coordinador; yo no toco `Pool`.

---

## 6. Fallos pasados (ERR-35..90) que mi idea podría repetir, y cómo los evito

- **ERR-3 / regla 3 (recalibrar tras ver datos)** — el riesgo mayor, porque propongo cambiar una letra *después* de que dos
  candidatos míos cayeran por ella. Lo evito: **nada se rejuzga**, v3 sólo rige candidatos futuros con semillas nuevas, y la
  justificación es un **cálculo del nulo** que no depende de qué candidato cayó (el placebo es el tronco contra sí mismo).
- **ERR-31** (el runner leyó los umbrales de la batería y no del preregistro): umbrales en un módulo único importado.
- **ERR-38 / regla 14** (batería copiada con defaults distintos): entrada campo a campo, y la señal de alarma "dos organismos
  con filas idénticas hasta el último decimal" se chequea explícitamente.
- **ERR-42** (humo que no llega a escribir su JSON): el humo del paquete escribe JSON antes de la serie.
- **ERR-39** (control de paja): el placebo **no** es un control de paja; es el nulo exacto, y CAL-4 lo verifica antes de leer.
- **ERR-44** (un subcriterio que presupone aprendizaje gradual): v3 no añade subcriterios internos; sólo conducta y margen.
- **ERR-89** (una puerta que el runner no juzga): el runner de v3 imprime **pasa/cae por cláusula** y el JSON lo guarda.
- **ERR-85/86** (CPU, Pool, matar procesos): no corro Pool; hoy no lancé nada en paralelo; hay un Pool del coordinador vivo.

---

## 7. Predicciones propias que se me cayeron hoy, y lo que no pude verificar

**Refutadas, mías, de `PREREGISTRO_v15f_v2.md` §5:**
1. **T-C (ii): predije `A₁₂` 0.80–0.95. Salió 0.55.** Y en unidades naturales el efecto fue **+6.25 puntos de `rev`** con
   IC90 **[−4.1, +16.6]**: mi mecanismo **no** produjo el efecto grande que prometí. Lo digo separado del §2 a propósito:
   que la puerta no pueda ver un efecto moderado **no salva** mi predicción, que era de efecto grande.
2. **T-E: refutada en cinco de seis escenarios.** Predije E1 ≥ 18/20 → 13; E2 20/20 → **3/20**; E2J/E2K/E2L ≥ 19/20 → 16/14/16.
3. **T-A: "muertes ≈ tronco"** se cumplió en medianas (1.02×) pero mi lectura implícita de que eso bastaría era falsa.
4. Acertadas, para no barrer sólo en mi contra: **T-D** con el orden de las puertas (v15f cae C1/C2, v15g las cruza) fue una
   predicción mía exacta; **T-B** y **T-F** también.

**Lo que no pude verificar (y por qué).**
- **No corrí el placebo real** (perilla que consume sorteos): exige construir instrumento por anclas y una serie con Pool. El
  §8 de hoy es su **sustituto por reparto**, que vale bajo un supuesto explícito: que las dos series OFF son de la misma ley
  — y ese supuesto lo verifiqué (`A₁₂` no pareado 0.511 / 0.534 / 0.554, medianas r −71.5 vs −73.0).
- **No verifiqué que el pareado por semilla sirva de algo, porque no sirve**: `sd(d) / (√2·sd(OFF))` = 0.85–1.35 y
  `ρ(ON, OFF)` = −0.47…+0.38 (compatible con 0). **La misma semilla no controla la trayectoria**: ON y OFF divergen. "Pareado
  por semilla" es nominal en el mundo vivo; en el examen determinista sí es real. Esto merece una línea propia en v3.
- **No revisé las puertas de fase 9 distintas de F9-4** con el mismo microscopio; F9-7 (A₁₂ 0.426, contraste 9/20) merece el
  mismo cálculo de potencia antes de darla por "negativo limpio".
- No pude decir nada sobre el nivel 10 ni sobre el mundo de familias: fuera de mi lane hoy.

---

## Salida del análisis (pegada; completa en `salida_analiza_potencia_Q1.txt`)

```
1) LO OBSERVADO  (A12 = P(ON>OFF) + 0.5 P(=), exactamente la formula del runner)
caso                     n    A12 umbral      G/E/P   med ON  med OFF   med d    sd d  sd OFF  r(ON,OFF)  sd_d/(V2 sdOFF)
v15f  T-A  VIVO         20  0.425   0.50     8/1/11    -73.5    -73.0    -5.5   17.56   10.91     -0.466            1.138
v15f  T-A  CUELLO_MIN   20  0.450   0.50     9/0/11    -11.5     -8.5    -1.0   11.02    9.17      0.378            0.850
dE5   T-A  VIVO         20  0.400   0.50     8/0/12    -75.0    -71.5    -5.0   17.83   13.31     -0.074            0.947
dE5   T-A  CUELLO_MIN   20  0.500   0.50    10/0/10    -10.0     -5.5     0.5   19.46   12.42     -0.274            1.108
v15f  T-C ii (rev)      20  0.550   0.75     11/0/9     44.5     37.5     3.5   26.83   14.01     -0.187            1.354
v15g  T-C ii (rev)      20  0.550   0.75     11/0/9     43.0     37.5     5.5   23.36   14.01      0.133            1.179
dE5   T-C ii (rev)      20  0.500   0.75    10/0/10     44.0     45.5    -1.0   29.55   17.80     -0.071            1.174

2) POTENCIA EXACTA  (#ganadas ~ Bin(n, p))
  regla A12 >= 0.50   p ->   0.35   0.40   0.45   0.50   0.55   0.60   0.65   0.75
    n = 20                  0.122  0.245  0.409  0.588  0.751  0.872  0.947  0.996
    n = 40                  0.036  0.130  0.316  0.563  0.787  0.926  0.983  1.000
    n = 80                  0.004  0.044  0.215  0.544  0.844  0.973  0.998  1.000
    n -> inf                0.000  0.000  0.000  0.500  1.000  1.000  1.000  1.000
  regla A12 >= 0.75   n = 20: p=0.50 -> 0.021 | p=0.65 -> 0.245 | p=0.75 -> 0.617 | p=0.85 -> 0.933
  Efecto minimo detectable (PASA con prob 0.80): A12>=0.50 n=20 -> p*=0.568 ; A12>=0.75 n=20 -> p*=0.799

3b) BANDA DE OPERACION en unidades naturales (PASA-80% / CAE-80%)
      v15f  T-A  VIVO        PASA-80% en delta >=   +2.5   CAE-80% en delta <=   -4.5   (banda ciega  7.0)
      dE5   T-A  VIVO        PASA-80% en delta >=   +3.0   CAE-80% en delta <=   -4.0   (banda ciega  7.0)
      v15f  T-C ii (rev)     PASA-80% en delta >=  +21.5   CAE-80% en delta <=  +11.5   (banda ciega 10.0)
      dE5   T-C ii (rev)     PASA-80% en delta >=  +23.0   CAE-80% en delta <=  +11.0   (banda ciega 12.0)

4) n PARA NO INFERIORIDAD (margen 10 puntos de r)   potencia 0.80 -> n = 8..24 ; que el IDENTICO pase el 95 % -> n = 14..42
   (VIVO: n = 34-35 con margen 10 ; n = 15-16 con margen 15)

5) LOS DATOS YA MEDIDOS CON EL INSTRUMENTO CORRECTO (DIAGNOSTICO, NO VEREDICTO; nada se rejuzga)
caso                      A12      IC90 de p (signo)  media d     EE     IC90 de la media d   no-inferior a margen 10?
v15f  T-A  VIVO         0.425           [0.22, 0.61]    -1.65   3.93            [-8.4, 5.1]        SI  (LI -8.4 > -10)
v15f  T-A  CUELLO_MIN   0.450           [0.26, 0.65]     0.05   2.46            [-4.2, 4.3]        SI  (LI -4.2 > -10)
dE5   T-A  VIVO         0.400           [0.22, 0.61]    -0.55   3.99            [-7.4, 6.3]        SI  (LI -7.4 > -10)
dE5   T-A  CUELLO_MIN   0.500           [0.30, 0.70]    -2.10   4.35            [-9.6, 5.4]        SI  (LI -9.6 > -10)
v15f  T-C ii (rev)      0.550           [0.35, 0.74]     6.25   6.00           [-4.1, 16.6]        n/a
dE5   T-C ii (rev)      0.500           [0.30, 0.70]     7.45   6.61           [-4.0, 18.9]        n/a

6) PUERTAS DE CONTEO k/n (Q2)  BA-v dist(PAR) 18/19, 17/19, 13/19 -> 48/57 = 0.842, IC90 [0.741, 0.915]
   chi2 homogeneidad 5.54 < 5.99 -> las tres series son compatibles con UN solo p
   Con p = 0.842, P(dist >= 15/19) = 0.830: una serie de cada 5.9 cae aunque el mecanismo no cambie.

7) LA LETRA v3 (no inferioridad, margen 10) CONTRA LA v2, MISMO n = 20 y MISMO RUIDO
  v15f T-A VIVO   delta ->   +10     +5     +2     +0     -2     -5    -10    -20
       v3  P(PASA)         1.000  0.983  0.909  0.790  0.617  0.330  0.051  0.000
       v2  P(PASA)         0.996  0.917  0.751  0.585  0.406  0.176  0.013  0.000
  dE5  T-C ii     delta ->   +10     +5     +2     +0     -2     -5    -10    -20
       v3  P(PASA)         0.886  0.696  0.541  0.425  0.319  0.184  0.051  0.001
       v2  P(PASA)         0.181  0.054  0.020  0.021  0.020  0.007  0.001  0.000

8) EL NULO MEDIDO CON CORRIDAS REALES DEL TRONCO (OFF de v15f-v2 y OFF de dE5-v2 = v14.2 las dos)
medida (tronco vs tronco)    med A   med B  A12 no par.  A12(1 orden)  P(pasa) reordenar  P(pasa) repartir 40
T-A  VIVO        (r)         -71.5   -73.0        0.511         0.500              0.681                0.568
T-A  CUELLO_MIN  (r)          -5.5    -8.5        0.608         0.550              0.986                0.561
T-A  VIVO  (-muertes)        -92.0   -95.0        0.554         0.425              0.873                0.558
T-C ii  (rev)                 45.5    37.5        0.534         0.450              0.000                0.018

   8b) LA LETRA COMPLETA sobre el placebo perfecto (40 semillas reales del tronco, dos brazos de 20):
       VIVO         muertes<=1.10x 0.993   r>=tronco-10 0.985   A12>=0.50 0.567   brazo entero 0.567
       CUELLO_MIN   muertes<=1.10x 0.951   r>=tronco-10 0.954   A12>=0.50 0.561   brazo entero 0.558
       >>> T-A ENTERA sobre el placebo perfecto: PASA 0.316  (CAE 0.684)
       >>> sin la clausula A12 (solo las dos medianas declaradas): PASA 0.909
       >>> T-A y T-C (ii) juntas: PASA ~ 0.0057
```

**Una frase para el director:** *el criterio v2 rechaza al propio tronco 99 veces de cada 100 si se lo presenta como
candidato; la cláusula que lo hace (`A₁₂ ≥ 0.50`) es un volado que no mejora con más semillas, y el arreglo no cuesta
organismo nuevo ni memoria nueva: juzgar con el margen que el criterio ya declara, y correr siempre el placebo.*
