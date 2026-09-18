# PREREGISTRO — Bloque 4 (XOR): **el cuello es la REGLA**. Dos constantes de la vía lenta

**Sustituye al borrador `PREREGISTRO_xor_3f.md`, que queda anulado** (su pieza (i), el "techo de muestreo 0.75", se
midió con un perfil de muestreo sintético y el control positivo la refutó; ver `PUENTE_creacion.md` §A9-bis).
Escrito el 18-sep-2026 por el CREADOR A. **Los números de §8 (humo, 1 semilla) están medidos y se declaran aquí;
todo lo de §4 (predicciones) NO.** Lo corre el coordinador con `Pool`.

## 1. De dónde viene

Serie XOR: 3 (dimensión ❌), 3b (puerta ❌), 3d (regla delta fusionada ❌), trío (3 mecanismos ❌), 3e (oráculo de
rasgos ❌, 0.625). El diagnóstico registrado tras 3e fue *"el cuello es la dinámica"*. El **control positivo** del
creador A lo convierte en un número: se graba el flujo exacto de encuentros de la vía lenta (`organismo_v13q5`,
perilla `lab`, sólo registra; **el replay reproduce al organismo con 0 diferencias en 20/20 semillas**) y se repite
ese mismo flujo con otros lectores:

| lectura | DELTA (regla local) | **LSQ (gradiente exacto)** | MLP (retropropagación, 6px→8→1) |
|---|---|---|---|
| cuadrática (21+1 rasgos) | 0.438 | **0.562** | 0.531 |
| oráculo {P0,P1,P0·P1,1} | 0.625 | **1.000** [1.0, 1.0] en las 14 con las 4 clases mordidas | 0.531 |

**El gradiente exacto cruza 0.75 con el muestreo real ⟹ el cuello es la REGLA**, no el mundo. Y el porqué está
medido sobre el mismo flujo: la solución exacta de xor01 es `y = −3 + 4·P0 + 4·P1 − 8·P0·P1`, pide **|w| = 8**;
`clip_s = 3` no la deja caber y `eta_s = 0.015` (|Δw| ≈ 0.06 por mordida) no la recorre en ~290 mordidas.

| `eta_s` \ `clip_s` | 3 (el de hoy) | 10 | ∞ |
|---|---|---|---|
| **0.015 (el de hoy)** | 0.656 | 0.656 | 0.656 |
| 0.05 | 0.719 | 0.719 | 0.719 |
| **0.15** | 0.750 | **1.000** | **1.000** |
| 0.5 | 0.750 | 1.000 | 1.000 |
| 1.0 | 0.500 | 0.500 | 0.500 |

## 2. Hipótesis

**H4.** El cuello de XOR en v13/v14 son **dos constantes de la vía lenta**: `eta_s` 0.015 → 0.15 y `clip_s` 3 → 10.
**Memoria extra: cero. Código nuevo: cero.** Con los rasgos dados (oráculo) la misma regla local alcanza lo que
alcanza el gradiente exacto. Con los rasgos propios del organismo (cuadrática) **no**, porque ahí el techo son los
rasgos (el gradiente exacto sólo llega a 0.562): esa es la predicción que separa las dos causas.

## 3. Mundo, instrumento, brazos

- Mundo de regla de siempre (`split_regla`, 20 patrones de peso 3, `ntr=(4,4)`), **T = 100 000** (el `BASE` de 3d y
  3e: un solo cambio por experimento), `puerta = 3`, `constante=True`, `regla_lenta='delta_signo'`, `lam_lenta=0`.
- **Instrumento:** `experimentos/creacion_A/organismo_v13q5.py` (`fae9c32b146fdbb4`), por anclas
  (`construye_v13q5.py`, `e1eb48547b4f8131`) desde `organismo_v13q4.py` (`3cc732dd2b2519cd`) ← `organismo_v13q3.py`
  (`aaebe073308a40c2`, sólo leído). **Identidad con `seleccion=None, lab=False` ≡ v13q3: 16/16** (arnés
  `identidad_v13q4.py` / comprobación interna del runner, 3/3 en el humo).
- **NO hay `--rapido`:** el gemelo `organismo_v13q_rapido` no tiene `regla_lenta`, `constante`, `oraculo01`,
  `seleccion` ni `lab` (comprobado: 0 apariciones). Todo interpretado.
- **Semillas 81–100, nuevas para la línea XOR** (usadas: 1–20 en el bloque 3, 21–40 en 3b, 41–60 en 3d, 61–80 en 3e).
- Brazos (el único cambio entre ellos son las constantes de la vía lenta):

| brazo | `eta_s` | `clip_s` | selección | qué prueba |
|---|---|---|---|---|
| `TRONCO` | 0.015 | 3 | — | lo de hoy |
| **`DOS_NUM`** | **0.15** | **10** | — | **la propuesta A-4** |
| `DOS_NUM_WTA` | 0.15 | 10 | `wta` θ=0.3 ρ=0.02 cupo 1 `cond` | + la selección meta-aprendida (A-1 ii) |
| `ETA_1` | 1.0 | 10 | — | **CONTROL: debe EMPEORAR** |

- Lecturas: **`oraculo01`** (rasgos dados) y **`cuadratica`** (los rasgos propios del organismo). Reglas del mundo:
  **`xor01`, `px0` y `azar`**, las tres, en todos los brazos. Total **480 corridas** + 9 de identidad.

## 4. Predicciones numéricas (escritas antes de la serie)

- **V1 (la que decide):** oráculo, `DOS_NUM`, `acc_lenta` mediana **≥ 0.90** y **> `TRONCO` en ≥ 15/20** pareado.
- **V2 (la que separa las dos causas):** cuadrática, `DOS_NUM`, `acc_lenta` mediana **≤ 0.65** — el techo del
  gradiente exacto ahí es 0.562, así que si `DOS_NUM` lo superara, mi control positivo estaría mal.
- **V3:** `DOS_NUM_WTA` abre `P0·P1` en **≥ 15/20** en cuadrática.
- **V4 (control que debe fallar):** `ETA_1` < `DOS_NUM` en **≥ 14/20** (oráculo).
- **V5 (controles de regla):** `px0` = **1.000** y `azar` ∈ **[0.35, 0.65]** en todos los brazos y las dos lecturas.
- **EXPOSICIONES, el número principal por brazo:** primer `n` de encuentros con mediana ≥ 0.75. Predicción:
  oráculo `TRONCO` **> 600**, `DOS_NUM` **≈ 60–150**, `ETA_1` **> 600**; cuadrática **> 600 en todos**.
  (Referencia del control positivo: el gradiente exacto sobre el oráculo llega a ≥0.75 con **10** y a 1.000 con 20.)

## 5. Criterio de refutación, y una lectura alternativa preregistrada

- **H4 queda refutada** si V1 falla con V5 en su sitio. Si V1 ∈ [0.75, 0.90) se reporta como **progreso real**, sin
  recalibrar.
- **Lectura alternativa, escrita ANTES de la serie porque el humo de 1 semilla ya la sugiere (§8):** si `DOS_NUM`
  falla V1 pero `DOS_NUM_WTA` sí cumple (≥0.90), lo declarable es *"las dos constantes son necesarias pero no
  suficientes: hace falta además abrir el rasgo conjuntivo"*. Eso **no** salva H4 tal como está escrita: V1 se
  reporta como NO y el bloque se registra con esa lectura.
- **No se barre `eta_s` ni `clip_s` después de ver los datos.** Si hiciera falta un valor intermedio, va en un
  preregistro nuevo con semillas nuevas.

## 6. CONTROL QUE PUEDE FALLAR: las dos constantes tocan el TRONCO

`eta_s` y `clip_s` son de la vía lenta **del tronco**, no de un experimento. En el MISMO bloque, y antes de que
nadie hable de cambiar v14:

1. **Examen (criterio v3'):** `python experimentos/creacion_A/bateria_v14_e015c10.py 20 --log` →
   **≥ 19/20 en las seis etapas** (E1, E2, E2I, E2J, E2K, E2L) y el resto del criterio v3' sin tocar.
2. **Regresión de generalización:** `python experimentos/creacion_A/bateria_generaliza_A.py organismo_v14_e015c10 20 --desde 101 --log`
   → **G1 ≥ 0.80, G2 ≥ 0.85, K 20/20**.
3. Instrumentos, por anclas desde los CONGELADOS (sólo se leyeron), generados por `construye_v14_e015c10.py`:
   `organismo_v14_e015c10.py` (← `organismo/organismo_v14.py` `9bab8ac0685b1f21`; **único cambio: dos valores por
   defecto**), `bateria_v14_e015c10.py` (← `organismo/bateria_v14.py` `72216f5415de0c86`; seis etapas y umbrales
   intactos), `bateria_generaliza_A.py` (← `organismo/bateria_generaliza.py` `9d65c18e0237da97`; **una entrada nueva
   en `INSTRUMENTOS`**, umbrales intactos).
   **Identidad: llamando a `organismo_v14_e015c10` con `eta_s=0.015, clip_s=3.0` es `organismo_v14` EXACTO,
   16/16** (`identidad_v14_e015c10.py`, 8 escenarios × 2 semillas, 25 claves), y con los valores nuevos difiere en
   10 claves (el parche actúa).

**Señal temprana, medida y declarada (1 semilla, no es la serie):** el cableado de `bateria_generaliza_A` se
comprobó llamando a su `tarea()` en un proceso, sin `Pool`: `px0`, semilla 101, T = 200 000 →
**v14 original `acc` 1.000 (`ba` 0.988, 58 celdas)** contra **v14 con las dos constantes `acc` 0.900 (`ba` 0.899,
49 celdas)**. Sigue por encima del umbral G1 ≥ 0.80, pero **va en la dirección del riesgo**: con una semilla no se
decide nada, y por eso el control de §6 es obligatorio y no opcional.

**Cláusula, escrita antes:** si la generalización (G1/G2/K) o la retención (las seis etapas ≥ 19/20) **caen**, las dos
constantes **NO entran al tronco**; quedan como perilla de experimento del mundo de regla, y los valores intermedios
se buscan en un preregistro nuevo, **no aquí y no con estas semillas**.

## 7. Riesgo declarado que el humo ya destapó (afecta a la fuerza de V1)

Mis números de §1 se midieron **repitiendo el flujo de encuentros del TRONCO**. En el organismo real, **cambiar las
constantes cambia el flujo**: en el humo, los eventos de la vía lenta antes de la sonda bajan de 276 (TRONCO) a 215
(`DOS_NUM`) y se desploman a **16** con `ETA_1` en oráculo (y a **4** en cuadrática, con 2 clases sin morder). Es
realimentación por la conducta: si la vía lenta aprende más rápido, la boca rechaza antes y muerde menos. **Por eso
V1 puede fallar aunque el banco diera 1.000, y por eso V4 puede pasar por la razón equivocada** (`ETA_1` no pierde
por mal optimizador sino porque deja de morder). Ambas cosas se reportan explícitamente: el runner registra
`eventos` y `clases sin morder` por corrida, y **V4 sólo se declara "el control falla como debía" si `ETA_1`
mantiene ≥ 100 eventos**; si no, se declara *"`ETA_1` no es comparable: cambió la conducta"*.

## 8. Humo ya corrido (1 semilla, un proceso, sin Pool, T = 100 000) — NO es la serie

`python experimentos/creacion_A/corre_xor_4.py --humo` → `datos/xor_4_humo_20260918_052235.{log,json}`
(`fc920658ea9cd6a4`). Identidad interna **3/3**. Semilla 81, xor01:

| lectura | brazo | `acc_lenta` | abre `P0·P1` | `Ws(P0·P1)` | max\|Ws\| | eventos | n\*(≥0.75) |
|---|---|---|---|---|---|---|---|
| oráculo | TRONCO | 0.500 | — | −1.00 | 1.00 | 276 | 150 |
| oráculo | **DOS_NUM** | 0.625 | — | −3.16 | 3.16 | 215 | **60** |
| oráculo | **DOS_NUM_WTA** | **1.000** | **SÍ** | −5.02 | 5.02 | 356 | 300 |
| oráculo | ETA_1 (control) | 0.500 | — | −4.00 | 7.00 | **16** | >600 |
| cuadrática | TRONCO | 0.438 | — | −0.80 | 1.28 | 353 | >600 |
| cuadrática | DOS_NUM | 0.375 | — | −1.92 | 2.26 | 282 | >600 |
| cuadrática | DOS_NUM_WTA | 0.438 | no | 0.00 | 1.77 | 126 | >600 |
| cuadrática | ETA_1 (control) | 0.500 | — | 0.00 | 10.00 | **4** | >600 |

Con una sola semilla no se ajusta nada. Lo que sí queda declarado: el tope deja de apretar (max|Ws| pasa de 1.00 a
3.16 y a 5.02), y **cuadrática no mejora con las constantes** — que es exactamente lo que predice V2.

## 8-bis. Deslices de método que declaro (EQUIPO regla 3)

Al probar que la batería del examen arranca, corrí `python bateria_v14_e015c10.py 2`: **esa batería abre `Pool(14)`
por dentro**, y la regla 3 dice que sólo el coordinador corre con `Pool`. Fue una prueba de arranque de 2 semillas
(104 s) y su resultado no se usa como evidencia de nada (el criterio v3' exige S ≥ 20). No volvió a ocurrir: la
verificación de `bateria_generaliza_A` se hizo llamando a su `tarea()` en un proceso, sin tocar el `Pool`.

## 9. Coste

**480 corridas** de T = 100 000 (4 brazos × 2 lecturas × 3 reglas × 20 semillas) + 9 de identidad de T = 60 000.
Medido en el humo: **~4.4 s por corrida** en un proceso. Con `Pool(14)`: **≈ 480 × 4.4 / 14 ≈ 2.5–3 min** más el
arranque de los workers. El control del §6 (examen 20 semillas + `bateria_generaliza` 20 semillas × 2 reglas a
T = 200 000) es lo caro: del orden de **15–25 min** con `Pool(14)`.

## 10. Vocabulario, si pasa

*"El cuello de XOR en la vía lenta era la regla, y eran dos constantes: con `eta_s = 0.15` y `clip_s = 10` la misma
regla local, sin memoria ni código nuevos, alcanza al gradiente exacto sobre los rasgos dados."* Nada de "aprende
XOR" mientras la lectura cuadrática siga en 0.56: ahí el techo son los rasgos, y eso es el bloque siguiente.
