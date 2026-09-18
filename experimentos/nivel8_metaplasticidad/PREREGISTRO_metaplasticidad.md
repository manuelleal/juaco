# Nivel 8, bloque metaplasticidad (A-2 del creador A): consolidar por masa de conflicto en el mundo largo

**Escrito ANTES de correr, 18 sep 2026, 00:05.** Convierte en bloque preregistrado la propuesta **A-2** de
`registro/investigacion/PUENTE_creacion.md` (sección "Propuestas para el coordinador"), apoyada en los puntos
**A3–A5** de la sección "Creador A" del mismo documento (citados, no repetidos: se referencian con número). Regla 4
de `registro/EQUIPO.md` (preregistrar antes de correr: hipótesis, mundo, medidas, predicción numérica, criterio de
refutación, controles que pueden fallar). Regla 1 y 2 (no se editan `mundo_largo.py` ni `corre_mundo_largo.py`,
ambos instrumentos existentes; el instrumento nuevo ya está construido por anclas con su sha de origen fijado).

## 0. Qué se hereda de A-2 y qué se fija aquí

- El **mecanismo** y el **instrumento** (`mundo_largo_A.py`) ya están escritos y con identidad verificada por el
  creador A (9/9, perillas apagadas, citado en §1). Este preregistro no cambia ni una línea de ahí: sólo fija la
  **serie de confirmación** (semillas nuevas, criterios, controles) y añade su **propia** etapa de identidad dentro
  del runner (§3) como control de que el instrumento no cambió entre que A lo construyó y que esta serie corre.
- Se preregistran exactamente los **tres brazos** que pide A-2 (`BASE`, `B10`, `B50`) — nada de barrer otros valores
  de `beta_m` aquí. Si `B10` resulta indistinguible de `B50` (cláusula de dosis, §6 P4), un `beta_m` intermedio
  queda para una enmienda futura, no para esta serie.
- Semillas **nuevas** 41–60: no se reutilizan ni las 1–3 del humo de A (§9) ni las 21–40 del registro
  `largo_s21-40_20260917_204840.json` que midió el 0.67 baseline.
- Las cuatro trampas de la noche del 17-sep (regla 5): canal social simétrico — no aplica (no hay canal social
  aquí); acierto sin balancear — `ret_no_inv`/`ret_inv` son fracciones sobre conjuntos fijos de patrones, no hace
  falta balancear; mundo que se come la comida — el pool de 50 y las inyecciones son los mismos de
  `nivel8_mundo_largo`, ya auditados ahí; sitios fijos que se memorizan — mismo mundo, mismo riesgo ya conocido y
  aceptado en `PREREGISTRO_mundo_largo.md`. No se reabre esa auditoría aquí.

## 1. Instrumento (construido por el creador A, por anclas; shas reales, calculados para este preregistro)

- **Origen:** `experimentos/nivel8_mundo_largo/mundo_largo.py` — sha256 corto **`9f74ff6b5941e5a5`** (instrumento
  existente del bloque nivel8_mundo_largo; NO se toca).
- **Constructor por anclas:** `experimentos/creacion_A/construye_largo_A.py` — sha256 corto **`85ca7bb8c79198ca`**.
  Reemplaza tres anclas verbatim (firma de `run()`, la actualización de `Wp`/`Wn` de la vía rápida, y el `return`)
  y falla con `AssertionError` si alguna ancla no aparece exactamente una vez en el origen — no hay parcheo ciego.
- **Instrumento generado:** `experimentos/creacion_A/mundo_largo_A.py` — sha256 corto **`a3ded739a46b1c97`**
  (recalculado ahora sobre el archivo tal como está en disco; coincide con el sha de origen que declara su propia
  cabecera). `NO editar a mano` (dice su cabecera); si algún día no coincide con este número, el instrumento se
  declara sospechoso y no se usa sin reconstruirlo.
- **Perillas nuevas, ambas apagadas por defecto:**
  - `beta_m` (metaplasticidad por masa de conflicto, el mecanismo de A-2, ver §2). `beta_m=None` ⟹ identidad exacta
    con `mundo_largo.py`.
  - `m_stats` (lectura: estadísticos de `m = min(Wp,Wn)` al final, para calibrar; no cambia ningún número del
    organismo). Se deja `True` en la serie sólo para guardar la lectura en el JSON, no entra en ningún criterio.
- **Runner:** `experimentos/nivel8_metaplasticidad/corre_metaplasticidad.py` (esta carpeta) — copia adaptada de
  `experimentos/nivel8_mundo_largo/corre_mundo_largo.py` (instrumento existente, tampoco se toca; sólo se importa
  indirectamente al copiar su lógica de `pool_de`/`sitios_de`/`recuperacion`, que son funciones del mundo, no del
  organismo). Mismo `T=200000`, `T_nuevo=4000`, `T_inv=100000`, `usa_M=False` que el brazo **V13** de ese runner
  (no se corre el mapa aquí). `Pool(14)` sólo bajo `if __name__ == '__main__'` (regla 3).

## 2. Hipótesis y mecanismo mínimo

**Hipótesis.** La retención de lo ausente en el mundo largo (medida en el brazo V13: mediana `ret_no_inv` = **0.67**,
registro `largo_s21-40_20260917_204840.json`, T=200000 con inversión de regla en t=100000) **sube** si las celdas
que han recibido evidencia **contradictoria** (sirven a dos patrones de valencia opuesta por código compartido) se
vuelven **lentas**. No hace falta inventar variable nueva: por la biyección `(Wp,Wn) ↔ (W = Wp−Wn, m = min(Wp,Wn))`
(A3 del creador A; identidad numérica **2.5e−14** en 200 000 deltas conducidos con la misma secuencia), `m_c` **ya
es** esa evidencia contradictoria acumulada por celda, con su propio olvido `lam` que **ya existe** en el tronco.
A3 también establece que esto no toca la vía lenta (`Wps/Wns` puede ser un solo vector con signo, C2/C3 de A3) — el
mecanismo de A-2 actúa **sólo** sobre la vía rápida, que es la que lee `m` (la fisión de v11).

**Mecanismo mínimo (una línea, memoria extra CERO, localidad total).** La ganancia de cada celda en la
actualización de la vía rápida pasa de `eta` a `eta · g_c`, con

```
g_c = 1 / (1 + beta_m · m_c),      m_c = min(Wp_c, Wn_c)
```

aplicada elemento a elemento sobre las celdas del código activo, antes del `clip` a `[0, 3]` (ver `mundo_largo_A.py`,
ancla 2 de `construye_largo_A.py`). La vía lenta no cambia. `beta_m = None` ⟹ `g_c = 1.0` exacto para toda celda ⟹
identidad bit a bit con `mundo_largo.py` (verificado por A 9/9, y otra vez por esta serie en §3).

**Por qué `beta_m` tiene que ser grande (A5, y la respuesta del explorador en A-Q2):** `m` tiene semivida
`ln2/lam ≈ 14` mordidas y vale de media 0.015–0.048 (máx. 0.11–0.31) — es una variable demasiado rápida para
consolidar por sí sola; `beta_m = 50` es lo que hace falta para que `g_c` muerda. El explorador confirma
(A-Q2) que la cascada de Fusi–Drew–Abbott pide ≥ 2 escalas de tiempo propias y que ningún estudio publicado mide
el coste en adquisición o en recuperación de un mecanismo así — esta serie mide exactamente ese hueco, no sólo la
ganancia en retención.

**Por qué NO se apoya en el presupuesto de celdas (A5, C5 refutado).** La hipótesis C5 original de A ("la fisión de
v11 consolida, y por eso la retención cae cuando el pool se agota") quedó **refutada por reanálisis**, sin gastar
corridas: en `largo_s21-40_20260917_204840.json`, pool lleno (90 celdas, n=17) da `ret_no_inv` **0.667**, pool libre
(n=3) da **0.500** — al revés de lo que predecía C5 — y `corr(celdas, ret_no_inv) = +0.24` (V13) y `+0.32` (MAPA).
El mecanismo de A-2 (metaplasticidad por `m`, no por celdas libres) es independiente de esa lectura refutada.

## 3. Etapa de identidad (dentro del runner, ANTES de la serie; regla 2)

`corre_metaplasticidad.py` corre, en el propio proceso principal (secuencial, **sin** `Pool`, antes de abrir el
`Pool` de la serie):

```
mundo_largo_A.run(seed, beta_m=None, **kw) == mundo_largo.run(seed, **kw)
```

para `seed` en `{1, 2, 3}`, `T = 20000`, con `kw` = la configuración real de la serie truncada en T (pool de 50
patrones y sitios de `pool_de(seed)`/`sitios_de(pool, seed)`, `r_vis=3`, `T_nuevo=4000`, `usa_M=False`,
`invertir_largo=None` porque T=20000 < `T_inv`). Comparación **por todas las claves** que devuelve
`mundo_largo.run` (las dos claves nuevas de `mundo_largo_A`, `beta_m` y `m_stats`, no existen en el origen y quedan
fuera de la comparación por construcción — el mismo criterio que usa la etapa de identidad de
`corre_mundo_largo.py`), normalizadas con `json.loads(json.dumps(x, default=str))` (la misma normalización que ya
usa `corre_mundo_largo.py` para su propia identidad `mundo_largo`↔`mundo_mapa`).

**Debe dar 3/3.** Si no: `sys.exit(1)` inmediatamente, la serie de 60 corridas NO se lanza, y el VEREDICTO que
queda escrito en el log es **INSTRUMENTO SOSPECHOSO** (§8) — el instrumento cambió o algo en el entorno (versión de
numpy, etc.) rompe la identidad que A ya había verificado 9/9, y no se confía en ningún número de más abajo hasta
reconstruirlo.

## 4. Brazos y semillas

| brazo | `beta_m` |
|---|---|
| `BASE` | `None` |
| `B10`  | `10` |
| `B50`  | `50` |

Semillas **41–60** (20 nuevas). Por brazo: `T=200000`, `T_nuevo=4000`, `invertir_largo=100000` (`T_inv`),
`r_vis=3`, `usa_M=False`, pool de 50 patrones y sitios de `pool_de(seed)`/`sitios_de(pool, seed)` — **exactamente**
los parámetros del brazo V13 de `corre_mundo_largo.py`. 3 brazos × 20 semillas = **60 corridas** de T=200000, bajo
`Pool(14)`. Comparaciones **pareadas semilla a semilla**: la misma semilla produce el mismo pool, los mismos
sitios y la misma inicialización del código Kenyon en los tres brazos (mismo `rng=np.random.default_rng(seed)`
dentro de `run`); sólo cambia `beta_m`.

## 5. Medidas (mismas claves y mismas fórmulas que ya calcula `corre_mundo_largo.py`; se reproducen tal cual)

- **`ret_no_inv`**: `mean(ok(n) for n in vistos[4:10])` con `ok(n) = (W[n]>0) == (val_final[n]=='comida')` — signo
  correcto al final en los patrones vistos 5º–10º (nunca invertidos, ausentes desde su reemplazo). `None` si se
  vieron menos de 10 patrones (no ocurre a T=200000: ~50 inyecciones). Es la medida que dio 0.67 en el registro.
- **`ret_inv`**: `mean(ok(n) for n in vistos[:4])` — signo correcto al final en los 4 patrones iniciales, invertidos
  en ausencia en t=100000 (por construcción tiende a ser bajo; lo que importa es que no caiga MÁS que el baseline).
- **`adq_final`**: tercer elemento de la última entrada de `curva` (acierto en los últimos 10 patrones vistos, en
  la última inyección).
- **`rec`**: de `recuperacion(comida_bin, muertes_bin)` — pasos desde `t=100000` hasta que la tasa de comida por
  1000 pasos vuelve a ≥80 % de la media de los 20 000 pasos previos a la inversión; `T − T_inv` si nunca se
  recupera dentro de la corrida.
- **`deaths`**: muertes totales acumuladas en toda la corrida (T=200000; NO es `muertes_20k`, que es sólo la
  ventana post-inversión — A-2 cita las muertes totales del humo, 93/46/14 y 44/178/78, que son valores de
  `deaths`, no de `muertes_20k`).
- **`celdas`**, **`splits`**: celdas activas y número de divisiones al final.
- Todas por **mediana** de las 20 semillas del brazo; `P1` además exige el conteo **pareado**.

## 6. Predicciones numéricas (EXACTAS, las de A-2 — nada se recalibra después de ver datos)

- **P1 (la principal).** `B50`: mediana(`ret_no_inv`) ≥ **0.80** (registro: 0.67) **Y** pareado `B50 > BASE` en
  ≥ **14/20** semillas.
- **P2.** `adq_final` no cae más de 0.05: mediana(`adq_final`, `B50`) ≥ mediana(`adq_final`, `BASE`) − 0.05.
- **P3.** `rec` no empeora: mediana(`rec`, `B50`) ≤ mediana(`rec`, `BASE`).
- **P4 (cláusula de dosis, escrita ahora porque A-2 lo pide explícito).** `B10 ≈ BASE`: se declara cumplida si
  `B10` **NO** alcanza el mismo umbral que P1 (mediana(`ret_no_inv`,`B10`) ≥ 0.80 **Y** pareado `B10 > BASE` en
  ≥14/20). **Si `B10` SÍ alcanza ese mismo umbral (iguala a `B50`)**, las dos dosis dan lo mismo y el diseño no
  puede distinguir un efecto dependiente de `beta_m` de ruido de semilla: se declara **RUIDO**, y el veredicto es
  **REFUTA** aunque `B50` por sí solo cumpla P1–P3. Esta cláusula estaba ya anticipada en el humo de A (n=3,
  `B10` = baseline exacto — pero n=3 no alcanza para decidirlo; por eso es P4 y no un supuesto).

## 7. Controles que pueden fallar (si fallan, el mecanismo no vale aunque P1–P4 se cumplan)

- **C1 — muertes.** Si mediana(`deaths`,`B50`) **>** 1.5 × mediana(`deaths`,`BASE`): el mecanismo cobra
  supervivencia (congelar celdas en conflicto puede dejar al organismo sin corregir un valor que ya no es cierto, y
  morder más veneno) y **NO vale**, aunque P1 se cumpla. **Este control ya está en tensión**: en el humo de A (n=3,
  §9) las muertes de `B50` subieron en 2 de 3 semillas (178 y 78 contra 46 y 14 del baseline) — con n=3 el criterio
  de la mediana no se evalúa (harían falta las 20 semillas), pero el riesgo se declara aquí, ANTES de correr, para
  no sorprenderse si C1 falla.
- **C2 — `ret_inv` no debe caer.** mediana(`ret_inv`,`B50`) ≥ mediana(`ret_inv`,`BASE`) − 0.05. Congelar celdas con
  evidencia contradictoria podría impedir DESAPRENDER los 4 patrones invertidos en ausencia en t=100000 (aunque
  `ret_inv` sea bajo en general por construcción, no debe empeorar respecto del baseline).
- **C3 — la puerta de identidad** (§3): 3/3 obligatorio; si no, la serie no se corre.
- **No es un control de esta serie:** el presupuesto de celdas (C5 de A, ya refutado por reanálisis sin gastar
  corridas — ver §2). No se vuelve a medir aquí.

## 8. Veredicto (se escribe en el log de `corre_metaplasticidad.py`; no se recalibra después de ver datos)

| veredicto | condición |
|---|---|
| **INSTRUMENTO SOSPECHOSO** | la etapa de identidad (§3) no da 3/3. La serie de 60 corridas no se lanza. |
| **CONFIRMA** | identidad 3/3 **Y** P1 **Y** P2 **Y** P3 **Y** P4 (B10 no iguala a B50) **Y** C1 **Y** C2. |
| **REFUTA** | identidad 3/3, pero falla cualquiera de P1–P4 o C1–C2 (incluida la cláusula de dosis de P4: si `B10` iguala a `B50`, es RUIDO y REFUTA aunque `B50` cumpla P1–P3 solo). |

**Vocabulario si CONFIRMA:** "la metaplasticidad por masa de conflicto (`g_c = 1/(1+beta_m·m_c)`, memoria extra
cero) sube la retención de lo ausente de 0.67 a ≥0.80 en el mundo largo, a costa de [citar aquí qué control quedó
más cerca de fallar: muertes y/o recuperación]". No declarar "consolida" a secas sin citar el costo medido. Si
REFUTA: se declara textualmente qué predicción o control falló, con el número (p. ej. "P1 mediana 0.75 < 0.80" o
"C1 muertes medianas B50 158 > 1.5×93=139.5").

## 9. Mini-prueba de A (HUMO — n=3, cita `registro/investigacion/PUENTE_creacion.md` §A-2; NO es evidencia)

Semillas 1–3, T=200000, un proceso, brazo V13 del mundo largo:

| `beta_m` | `ret_no_inv` s1/s2/s3 | mediana | `adq_final` | `rec` | muertes (`deaths`) |
|---|---|---|---|---|---|
| baseline | 0.833 / 0.500 / 0.667 | 0.667 | 0.9/0.7/0.8 | 2 000/32 000/2 000 | 93/46/14 |
| 10 | 0.500 / 0.667 / 0.667 | 0.667 | 0.8/0.8/0.9 | 0/0/1 000 | 73/133/50 |
| 50 | 0.667 / 0.833 / 0.833 | 0.833 | 0.9/0.7/0.8 | 0/0/1 000 | 44/178/78 |

Con n=3 esto es **humo, no resultado**: no cuenta como parte de las 20 semillas nuevas de §4, no se combina con la
serie 41–60, y no mueve ni un número de §6–7 (los criterios de esta hoja se fijaron ANTES de mirar la serie nueva).
Se cita únicamente para mostrar de dónde sale `beta_m=50` y para documentar que el control de muertes (C1) ya
estaba en tensión antes de correr la serie real.

## 10. Coste y arranque

60 corridas de T=200000 con `Pool(14)`, más 3 pares de corridas de identidad a T=20000 (secuenciales, antes de
abrir el `Pool`). Orden de magnitud de referencia: 80 corridas de T=200000 con 4 brazos (`nivel8_mundo_largo`,
`Pool(14)`) tardaron ≈4 min. La estimación específica de esta serie (a partir del tiempo por corrida medido en
`--humo`, T=20000) va en el mensaje de entrega de la implementación, no en este preregistro (regla 4: la
predicción numérica no incluye tiempos de cómputo, sólo resultados del organismo).
