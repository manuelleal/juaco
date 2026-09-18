# PREREGISTRO — Bloque 3/3 (A-7): ¿construye M3 el rasgo conjuntivo con **8** ejemplos?

CREADOR A, 18-sep-2026. Lo corre el coordinador con `Pool`. **Los números de §7 (criba y humo) están medidos y se
declaran aquí; los de §4 (predicciones) NO.** Es el último bloque antes del criterio de parada (ERR-35).

## 1. De dónde viene, y qué es exactamente lo que se juega

Mi §A12/A14 cerró la línea en falso positivo estructural: con **8 patrones de tren, 9 de 15 hipótesis ajustan los
datos con residuo 0**, y ningún mecanismo de los míos pasó la criba (fisión **0/20**; residuo con estadístico *ideal*
**3/20**; pureza/media 10–12/20; gradiente exacto 0.562; retropropagación 0.531). El criterio de parada firmado dice
**14 ejemplos**. La sala aporta **M3**, y **M3 pasa mi criba**. Por tanto: *si M3 cruza con 8, no es que la
información estuviera ahí — es que M3 **trae un prior** (los candidatos son pares de píxeles) que rompe el empate de
9.* **Eso hay que declararlo como prior, no como aprendizaje de la estructura**, y el control que lo separa de una
fuga es `azar`.

## 2. Hipótesis

**H7.** M3 (memoria de un golpe por combinación de dos píxeles) elige `(0,1)` y generaliza en los nunca vistos con
los **8** patrones del mundo original, **con el desempate resuelto al azar** y **puntuando la abstención como fallo**.

## 3. Mundo, instrumentos, brazos

- Mundo de regla de siempre, T = 100 000, `lectura='cuadratica'`, `constante=True`, `regla_lenta='delta_signo'`,
  `lam_lenta=0`, **`eta_s=0.15`, `clip_s=10`** (las constantes del bloque 1, que no cuestan nada al tronco),
  `puerta=3`, `lab=True`. Reglas: **xor01, px0 y azar**, las tres, en todos los brazos.
- **Instrumentos:** `organismo_g3A.py` (`6e7d80db210b1950`), por anclas (`construye_g3A.py`) desde
  `experimentos/enjambre/grupo3/organismo_g3.py` (`91eb167023cb37b7`, del grupo 3, **sólo leído**); dos perillas
  mías, apagadas por defecto: `mem_apriori` (LECTURA de la memoria **en la sonda**) y `mem_desempate='azar'`
  (control de rigging). **Identidad con las dos apagadas ≡ `organismo_g3`: 10/10.**
  `experimentos/enjambre/grupo4/organismo_g4.py` (`e150ed808c546895`, del grupo 4, sin tocar) y
  `organismo_v13q6.py` (`b37aa8124c89cc5f`, mío; identidad ≡ v13q3 8/8).
- **Semillas 121–140**, vírgenes (la línea XOR usó 1–20, 21–40, 41–60, 61–80, 81–100, 101–120).
- **`--rapido`:** el gemelo `organismo_v13q5_rapido` **no** tiene `memoria`, `tabla_g` ni `ntr`; sólo sirve para
  `REF`/`SIN_SEL`. M3 y M4 van **interpretados** (~5 s/corrida) y el runner lo marca por brazo.

| brazo | qué es | por qué está |
|---|---|---|
| `M3` | grupo 3, `memoria='combi'`, desempate **por índice** (como lo corrió la sala) | la referencia del informe |
| **`M3_AZAR`** | idéntico, desempate **AL AZAR** | **es el brazo que decide** (control de rigging) |
| `M3_NTR14` | M3_AZAR con `ntr=(8,6)` = 14 patrones | control del prior |
| `M4` | grupo 4, `tabla_g` con las constantes **fijadas antes** (g=2, mse, dura, ρ=0.02, η=0.05, clip=3.0, α=0.3) | el segundo de la sala |
| `REF` | v13q6 + selección WTA (θ=0.3, ρ=0.02) | el mejor local anterior (0.625) |
| `SIN_SEL` | v13q6 sin competencia | control |

## 4. Predicciones numéricas (antes de la serie)

- **X1 (decide):** `M3_AZAR` xor01, puntuación **del registro**, mediana **≥ 0.75** y **> `REF` en ≥ 15/20** pareado.
- **X2:** `M3_AZAR` puntuación **ESTRICTA** (abstención = fallo) mediana **≥ 0.60**.
- **X3:** gana `(0,1)` **medido EN LA SONDA** en **≥ 15/20**.
- **X4 (rigging):** |mediana(`M3`, índice) − mediana(`M3_AZAR`, azar)| **≤ 0.05**. Si el índice decide, el mecanismo
  no es lo que dice ser: **un desempate por índice ya me coló un 17/20 falso** (PUENTE §A13) y el propio informe
  reporta el empate (0,1)/(1,4) en la semilla 3.
- **X5 (prior):** `M3_NTR14` ≥ **0.90**. Si M3 cruza con 8 pero **no** mejora con 14, está ajustado al régimen de 8.
- **X6 (controles obligatorios):** `px0` = **1.000** y `azar` ∈ **[0.35, 0.65]** en **todos** los brazos.
  *Éste es el control que separa prior de fuga*: un prior sobre pares de píxeles no puede ayudar a valencias
  aleatorias. Aviso: el informe del enjambre ya vio `azar` = 0.2 en 1 de 3 semillas.
- **EXPOSICIONES, número principal:** primer `n` de encuentros con mediana ≥ 0.75. Predicción mía: **n\* ≤ 20**
  para M3 (criba y humo dan 7–10), **> 600** para `REF` y `SIN_SEL`.
- **Mía, más afilada que el encargo** (la escribo para poder equivocarme): `M3_AZAR` mediana **≥ 0.94** y estricta
  **≥ 0.75**, porque en el replay sobre el flujo real la ganadora fue `(0,1)` en 19–20/20 con acc 1.000.

## 5. Refutación y cláusulas

- **H7 se refuta** si X1 falla con X6 en su sitio; o si **X4 falla** (entonces el resultado del informe es artefacto
  del índice y vale el del azar); o si X6 falla (entonces hay fuga, no prior).
- **Cláusula del prior (la que pidió el director):** si `M3_AZAR` cruza 0.75 con **8** patrones, **se declara PRIOR
  ESTRUCTURAL** — *"los candidatos son pares de píxeles"* — y el vocabulario es *"M3 construye el rasgo con 8
  ejemplos **porque trae el prior de pares**; sin ese prior, 9 de 15 hipótesis siguen empatadas"*. **No** se declara
  que el organismo descubra la estructura.
- **Cláusula de las dos puntuaciones:** M3 **abstiene** (valor 0.0) en las combinaciones nunca vistas, y la
  puntuación del registro le da 0.5 a esos empates. **Se reportan SIEMPRE las dos**, más la `cobertura` de la celda
  ganadora (cuántas de sus 4 casillas se llegaron a ver): en mi arnés a T=30 000 la cobertura era **3/4**.
- **Cláusula de muestreo:** semillas con una clase XOR sin morder, por brazo, en el log y en el JSON; el análisis
  principal es sobre las 20 y se añade el subconjunto con las cuatro clases.
- **No se toca ninguna constante después de ver los datos.** Las de M4 quedan fijadas aquí (§3) por el informe.

## 6. Lo que NO cubre este bloque

M3 **no abre un rasgo para la vía lenta**: sustituye la lectura por una tabla de 4 casillas sobre el par ganador
(`valor()` devuelve `_MM[_MG, combinación]`). Generaliza a los nunca vistos porque comparten la combinación
`(P0,P1)` con los vistos — es **memoria tabular con un prior de pares**, no una regla de generalización lineal.
Declararlo así es parte del bloque. Queda fuera: si eso escala a reglas de 3 píxeles (el prior de pares ya no
bastaría: 20 tríos) y si el tronco lo quiere.

## 7. Medido ya (criba + humo) — NO es la serie

**Criba** (`criba_mecanismo.py`, 20 semillas, mismo flujo real, **desempate al azar**, umbral ≥ 15/20):

| mecanismo | gana `(0,1)` | acc | pasa |
|---|---|---|---|
| **M3 `combi`** | **19/20** | **1.000** | **SÍ** |
| **M3 `combi1`** | **20/20** | **1.000** | **SÍ** |
| residuo (cascade-correlation), ideal | 2/20 | 0.625 | no |
| fisión de v11 | 0/20 | 0.469 | no |
| pureza / media del refuerzo | 10–12/20 | 0.625 | no |
| **[control nulo] azar** | **0/20** | 0.500 | no |

Celdas empatadas en el mínimo: mediana **1** [1, 2] — el artefacto del índice **apenas actúa**, pero cuando actúa le
da la victoria a `(0,1)` en 20/20, así que el brazo `M3_AZAR` no es opcional.

**Humo** (`datos/xor_7_humo_20260918_073634`, `e355e645480bd14d`; un proceso, identidad **3/3**, semilla 121):

| brazo | registro | estricta | ganadora | empates | cobertura | n\* |
|---|---|---|---|---|---|---|
| `M3` | 1.000 | 1.000 | (0,1) | 1 | 4/4 | **10** |
| `M3_AZAR` | 1.000 | 1.000 | (0,1) | 1 | 4/4 | **10** |
| `M3_NTR14` | 1.000 | 1.000 | (0,1) | 1 | 4/4 | 10 |
| `M4` | 1.000 | 1.000 | — | — | — | — |
| `REF` | 0.500 | 0.500 | abre 0x2 | — | — | — |
| `SIN_SEL` | 0.562 | 0.562 | — | — | — | — |

## 8. Coste

6 brazos × 3 reglas × 20 semillas = **360 corridas** de T = 100 000 + 9 de identidad. Medido en el humo: **~2.8 s
por corrida** interpretada (37.8 s las 6 más la identidad). Con `Pool(14)`: **≈ 2–4 min**. Con `--rapido` sólo bajan
`REF` y `SIN_SEL`.
