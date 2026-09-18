# PREREGISTRO — Bloque 6 (A-6): construir el rasgo conjuntivo **ya no es el cuello**; lo es la SOBREDETERMINACIÓN

Borrador del CREADOR A, 18-sep-2026. Lo corre el coordinador con `Pool`. **Los números de §6 (humo) están medidos y
se declaran; los de §4 (predicciones) no.**

## 1. El encargo era otro y la medida lo cambió (esto es lo importante)

El encargo A-6 pedía *"un mecanismo local que abra `P0·P1` en ≥ 15/20 y lleve `acc_lenta` ≥ 0.75"*. Medí las dos
mitades por separado y **se separan**:

**(a) Abrir el rasgo: resuelto.** Con las constantes de A-4 (`eta_s=0.15`, `clip_s=10`) y los parámetros
meta-aprendidos (θ=0.3, ρ=0.02, cupo 1, `cond`), la competencia WTA abre `P0·P1` en **3/3** semillas del humo
(antes, con θ=0.6/ρ=0.05, era 1/3). Ya no hace falta mecanismo nuevo.

**(b) Y aun así `acc_lenta` se queda en 0.500.** Diagnóstico, medido, y refuta de paso a la familia entera de
cascade-correlation: el estadístico **IDEAL** de selección (el residuo del ajuste elemental **EXACTO**, que ninguna
regla local puede superar) pone `P0·P1` en primer lugar en **4/20** semillas online y **3/20** ideal; rango mediano
3. **No es que el estadístico sea ruidoso: la información no está en 8 patrones.**

**Lo que sí explica los números: el conteo.** Con el conjuntivo abierto, los rasgos con peso libre son 6 píxeles
+ 1 constante + 1 producto = **8**, y los patrones de tren son **8**: el sistema queda **exactamente determinado**,
la solución es única pero sin margen, y el signo en los nunca vistos es frágil. La transición está medida fuera del
organismo con el estadístico ideal:

| patrones de tren | `P0·P1` es el #1 | rango mediano | acc si se abre el ganador |
|---|---|---|---|
| **4c+4v = 8 (el mundo de hoy)** | **3/20** | 5.0 | **0.625** |
| 5c+4v = 9 | 5/20 | 5.5 | 0.607 |
| 6c+5v = 11 | 7/20 | 2.0 | 0.583 |
| 7c+6v = 13 | 6/20 | 2.0 | 0.450 |
| **8c+6v = 14** | **12/20** | **1.0** | **1.000** |
| 9c+7v = 16 | 13/20 | 1.0 | 1.000 |

## 2. Hipótesis

**H6.** Con el rasgo conjuntivo ya abierto, `acc_lenta` en xor01 sube cuando el sistema efectivo pasa de
**exactamente determinado** a **sobredeterminado**. Hay **dos palancas**, y la primera **no toca el mundo**:

- **L1 — quitar un rasgo redundante (gratis, local, sin tocar el mundo).** En este mundo todo patrón tiene
  exactamente 3 píxeles activos, luego `1 = (1/3)·Σ_j P_j`: **la constante ya está en el span de los marginales**
  (lo medí: {6 px} y {6 px + cte} dan los dos 0.406 con ajuste exacto). Quitarla deja 7 rasgos contra 8 patrones.
- **L2 — más patrones de tren distintos (`ntr`).** Sube el tren y baja el test. **Cambia el MUNDO, no la regla**
  (trampa 3 de `EQUIPO.md`): se declara como tal y no es comparable número a número con los bloques 3–4.

## 3. Mundo, instrumentos, brazos

- **Instrumento:** `experimentos/creacion_A/organismo_v13q6.py` (`b37aa8124c89cc5f`), por anclas
  (`construye_v13q6.py`) desde `organismo_v13q5.py` (`fae9c32b146fdbb4`) ← `v13q4` (`3cc732dd2b2519cd`) ← `v13q3`
  (`aaebe073308a40c2`, sólo leído). Perilla nueva: `ntr`. **Identidad con `ntr=None` ≡ v13q3: 8/8.**
- **Gemelo compilado:** `organismo_v13q5_rapido.py` (del compilador), **identidad contra el interpretado 6/6,
  ×56–69** (verificado por mí en 3 escenarios × 2 semillas, incluidas `lab=True` y `seleccion='wta'`).
  **El gemelo NO tiene la perilla `ntr`**: los brazos `L2` van interpretados y los brazos `ntr=None` pueden ir con
  `--rapido`. **Encargo pendiente al compilador: extender el gemelo con `ntr` y repetir su arnés.**
- Base común: mundo de regla, T = 100 000, `puerta=3`, `regla_lenta='delta_signo'`, `lam_lenta=0`,
  **`eta_s=0.15`, `clip_s=10`** (las constantes que A-4 validó y que no cuestan nada al tronco: examen 8/8,
  G1 1.000, G2 0.967, K 20/20), `seleccion='wta'` con θ=0.3, ρ=0.02, cupo 1, `cond`. Lectura **cuadrática**
  (los rasgos propios del organismo). Reglas: **xor01, px0 y azar**.
- **Semillas 101–120** (nuevas para la línea XOR: 1–20, 21–40, 41–60, 61–80 y 81–100 ya usadas).
- Brazos:

| brazo | `constante` | `ntr` | rasgos abiertos vs patrones de tren | qué prueba |
|---|---|---|---|---|
| `REF` | sí | — (4,4) | 8 vs 8 (exactamente determinado) | la referencia interna |
| **`SIN_CTE`** | **no** | — (4,4) | **7 vs 8 (sobredeterminado)** | **L1: gratis, sin tocar el mundo** |
| `NTR11` | sí | (6,5) | 8 vs 11 | L2, dosis 1 |
| `NTR14` | sí | (8,6) | 8 vs 14 | L2, dosis 2 (la transición del §1) |
| `SIN_CTE_NTR11` | no | (6,5) | 7 vs 11 | las dos |
| `SIN_SEL` | sí | — (4,4) | sin competencia (control) | aísla la selección |

## 4. Predicciones numéricas (antes de la serie)

- **W1 (la que decide, y es la barata):** `SIN_CTE` > `REF` en **≥ 14/20** pareado, con mediana **≥ 0.625**.
- **W2:** `NTR11` mediana **≥ 0.75**; `NTR14` mediana **≥ 0.80**.
- **W3:** `SIN_CTE_NTR11` ≥ `NTR11` (las dos palancas no se estorban); si `SIN_CTE_NTR11` < `NTR11` en ≥ 14/20,
  L1 y L2 interfieren y se dice.
- **W4 (selección):** `P0·P1` abierto **ANTES de la sonda** en **≥ 15/20** en todos los brazos con `seleccion='wta'`.
  (El humo destapó que a veces se abre DESPUÉS de `fase2_en`, y entonces no puede influir en `acc_lenta`: el runner
  registra `abre_t` y sólo cuenta las aperturas previas a la sonda. Si muchas llegan tarde, el mecanismo siguiente
  no es otro estadístico sino **abrir antes**: bajar `sel_theta` o adelantar la competencia.) Si no llega, la
  selección vuelve a ser el cuello y H6 se reporta como no evaluable.
- **W5 (controles):** `px0` = 1.000 y `azar` ∈ [0.35, 0.65] en todos los brazos. `SIN_SEL` ≤ `REF`.
- **EXPOSICIONES, número principal:** primer `n` de encuentros con mediana ≥ 0.75, por brazo. Predicción:
  `REF` > 600; `SIN_CTE` 200–600; `NTR11` y `NTR14` **≤ 200**.

## 5. Refutación y cláusulas

- **H6 se refuta** si W1 y W2 fallan con W4 y W5 en su sitio: querría decir que la sobredeterminación no es la causa.
- **Cláusula de muestreo (obligatoria, y aquí cambia con `ntr`):** se reporta por brazo cuántas semillas tuvieron
  **una clase XOR sin morder** antes de la sonda; el análisis principal es sobre TODAS las semillas y se añade el
  subconjunto con las cuatro clases. En el humo: 1 de 3 semillas en `REF` y **0 de 3 en todos los brazos con
  `ntr`** — subir el tren también reduce ese problema, y eso **no** debe confundirse con el efecto de H6: por eso
  `SIN_CTE` (que no toca el mundo) es la prueba limpia y W1 es la que decide.
- **Cláusula del test que encoge:** con `ntr=(8,6)` el test baja a 6 patrones y la medida se cuantiza en pasos de
  1/6; con `(9,7)` a 4. **No se corre `ntr=(9,7)` en la serie** (lo dejo fuera a propósito: mediría ruido).
- No se barre `sel_theta` ni `sel_rho` después de ver los datos.

## 6. Humo ya corrido (3 semillas, un proceso, sin Pool, T = 100 000) — NO es la serie

`mini_prueba_A_ntr.py` (+ una corrida directa para `constante`), semillas 1–3, xor01, cuadrática, WTA meta-aprendida:

| brazo | tren/test | `acc_lenta` s1/s2/s3 | mediana | abre `P0·P1` | clases sin morder |
|---|---|---|---|---|---|
| `REF` (cte, 4+4) | 8/12 | 0.625 / 0.438 / 0.500 | **0.500** | **3/3** | 1 de 3 |
| **`SIN_CTE`** (4+4) | 8/12 | 0.625 / 0.438 / 0.875 | **0.625** | 3/3 | — |
| `NTR11` (6+5) | 11/9 | 0.833 / 0.667 / 1.000 | **0.833** | 3/3 | 0 de 3 |
| `SIN_CTE_NTR11` | 11/9 | 0.833 / 0.833 / 0.833 | **0.833** | 3/3 | — |
| `NTR14` (8+6) | 14/6 | 0.500 / 0.750 / 0.500 | 0.500 | 1/3 | 0 de 3 |
| (fuera de la serie) `ntr=(9,7)` | 16/4 | 0.667 / 1.000 / 1.000 | 1.000 | 3/3 | 0 de 3 |

Con 3 semillas y un test que encoge no se ajusta nada. Lo que sí queda dicho: **la selección ya no falla (3/3 en
casi todo) y el acierto se mueve con el conteo de rasgos y de patrones**, que es exactamente H6.

## 7. Coste

6 brazos × 3 reglas × 20 semillas = **360 corridas** de T = 100 000. Interpretado: ~5–10 s cada una (medido
5.5–10.3 s) → **≈ 4–7 min con `Pool(14)`**. Con el gemelo, los brazos sin `ntr` (3 de 6) bajan a segundos; con el
gemelo extendido a `ntr`, el bloque entero sería de menos de un minuto.
