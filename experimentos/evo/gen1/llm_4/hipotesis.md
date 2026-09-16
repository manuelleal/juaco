# gen1/llm_4 — Reparto competitivo de la corrección RW por familiaridad celda–patrón

**Operador:** LLM (Claude Fable 5.1), clase asignada PLASTICIDAD Y TASAS. **Padre:** `organismo_v10m.py`.
**Hijo:** `organismo.py` (sha16 `c8d1689236c423f1`), 11 líneas cambiadas con la métrica de `evalua.py`: 1 añadida en la
cabecera, 2 nuevas en el cuerpo de `run()`, 4 modificadas (2 de la instrumentación de truncación, 2 de la actualización
de `Wp`/`Wn`). Sin llamadas nuevas al RNG. Sin parámetros nuevos. Sin estado nuevo. Escrito antes de evaluar.

## Mecanismo

- En cada mordida con aprendizaje, para cada una de las 3 celdas activas:
  `f_c = 1 / (1 + |P − mû_c|²)`, con `mû_c = mu_c · (ΣP / Σmu_c)` la media móvil del patrón normalizada a la masa del
  patrón (la misma normalización de K5 que el padre ya usa en la división). Celda con `mu = 0` (virgen, o `plast=False`)
  → `f = 1`.
- `kf_c = f_c · 3 / Σf`. La corrección `eta·dlt` (o `eta·aversion·(−dlt)`) se aplica con `kf` en lugar de `kc`.
  **`Σkf = 3 = Σkc`: la suma de tasas por mordida es exactamente la del padre; sólo cambia el reparto entre las 3 celdas.**
- Valores de `f` para los patrones del currículo (3 unos cada uno, `|P−Q|² = 6 − 2·P·Q`): mismo patrón 1; B←D y C←D
  (`P·Q = 2`) 1/3; A←B, A←C, B←C (`P·Q = 1`) 1/5; A←D (`P·Q = 0`) 1/7.
- Reparto resultante: cada incremento es proporcional a `f_c`, así que el valor que un estímulo escribe queda repartido en
  proporción a `f`. D sobre {propia, B, B}: propia 60 %, cada celda de B 20 % (padre: 33 % cada una). C sobre {propia,
  propia, A}: cada propia 45 %, la de A 9 % (padre 33 %). Si las tres celdas son igual de ajenas (por ejemplo, las tres
  de B), `kf = kc`: sin celda propia no hay a quién favorecer y queda el padre (y su regla 2L).
- La compuerta se abre con el re-muestreo: `mu_c` sigue actualizándose con cada patrón que activa la celda (línea del
  padre, no tocada), así que tras ~35 mordidas de D sobre una celda de B `f` pasa de 1/3 a ~2/3. Pero para entonces el
  error de D ya se resolvió sobre su celda propia (`dlt → 0`) y no queda corrección que repartir: el reparto queda fijado
  por las tasas de las primeras ~20 mordidas. Una celda sólo se deja arrastrar por un estímulo que la ha re-muestreado.

## Hipótesis (una línea)

El olvido por la vía de valor ocurre porque la corrección de un estímulo nuevo se reparte a partes iguales entre celdas
que otro estímulo entrenó; si el reparto favorece la celda propia **sin cambiar la suma de tasas**, B y A conservan su
valor mientras C y D aprenden a la misma velocidad, y la reversión de un mismo patrón no cambia.

## Por qué no repite el fallo de K2

K2 dividía la tasa por la experiencia de la celda: frenaba la corrección del estímulo (`dlt` persistía, `err` cruzaba
`theta` más veces → más divisiones; C y D tardaban más) y frenaba la reversión del mismo patrón. Aquí:
(a) mismo patrón → `f = 1` en todas las celdas → `kf = kc` → E1 y E2 idénticos al padre por construcción (A +1→−3,
B −3→+1 y las ≥ 50 mordidas de B en Q4 no cambian); (b) `Σkf = 3` → `dlt` decae igual que en el padre → `err` y las
divisiones no se alteran por la tasa; (c) la protección no depende de cuánto se mordió sino de **qué patrón** lo hizo.
CTRL (`plast=False`): `mu` queda en cero → `kf = kc` → sigue fallando.

## Predicción numérica

- **R** (bloque M, semillas 1–10): padre ≈ 0.5 → hijo **0.7** (aceptaría como confirmación 0.6–0.8). `W_B(100k)` mediana
  de ≈ −2.3 a ≈ −2.6; `W_A(100k)` mediana ≥ 0.7.
- **Guarda H3** (`W_C ≤ −2.5`, `W_D ≥ 0.85` en 100k): ≥ 9/10, sin cambio de velocidad (mordidas a criterio ≈ padre).
- **E1:** idéntico al padre (muertes, W; `S` igual). **E2:** idéntico (W, mordidas, divisiones). **CTRL:** falla 10/10.
- **E2K** (D con 2 celdas de B): pasa 10/10; `W_B` más cerca de −3 que en el padre (antes de la división la celda
  compartida absorbe 20 % de la corrección en vez de 33 %), `W_D ≥ 0.8` igual. **E2J:** análogo, con más margen.
  **E2I:** `W_A` más protegido (la celda de A recibe 9 % de C), `tasa A Q4 ≥ 0.8·Q2` con más margen.
- **E2L:** ≈ padre (3 divisiones: las tres celdas compartidas tienen la misma historia de `mu` → `f` iguales →
  `kf = kc` hasta que se separan). `E ≈ 0.67`. `celdas ≤ 45`.
- **C** = 11/15 = 0.73.
- **Lo que NO cierra:** la vía estructural (hijas de D o C que entran en el código de B o A). La reduce algo (la hija
  hereda `mu ≈ B` y recibe ~1/5 del valor de D en vez de 1/3), pero si dos hijas toman el código de B, B sigue leyendo
  ≈ −1.8. Estimación: de las ~5/10 semillas que fallan en el padre se recuperan las que fallan por valor (≈ 2) y no las
  que fallan por código.

## Estado nuevo añadido

Ninguno. `_fam` y `kf` son temporales por mordida calculados de `mu` (ya existente). No hay almacén, ni contadores, ni
parámetros. `mu` se sigue actualizando como en el padre.

## Humo (semilla 1; comprobación de interfaz, no evaluación)

- `run(1, T=20000, invertir_en=10000)`: W A −2.45, B +1.00; mordidas de B Q3/Q4 34/37; 6 divisiones, 36 celdas,
  24 muertes, `n_techo` 0. Reversión completa en 10k pasos. Mismas claves devueltas que el padre.
- `run(1, T=30000, fases={10000: C veneno + D comida, 20000: A comida + B veneno})`: sondas 10000 A +0.99 B −2.62;
  20000 A −1.38 B −1.29 C −2.23 D +0.97; 5 divisiones (3 de C, 2 de D), 35 celdas, `n_techo` 0. En 20000 el código de
  A contiene dos hijas de C (32, 34) y el de B una hija de D (30): con fases cortas (10k) domina la vía estructural,
  que esta mutación no cierra. No corrí el padre en estas condiciones (regla: sólo dos corridas), así que no hay
  comparación pareada; la identidad en E1/E2 se verifica en la evaluación.

## Qué lo haría pasar por la razón equivocada

1. **Techo.** Si D o C alcanzan el criterio sólo porque su celda propia toca el clip de 3.0 (`n_techo > 0` en el bloque M;
   `comp` con `Wp = 3.0` o `Wn = 3.0` concentrado en una celda), la retención sería un artefacto del rango dinámico, no
   del reparto. Comprobar `n_techo` y `comp` en M.
2. **Aislar por división.** Si `R` sube junto con más divisiones en la ausencia (`splits_M` > padre) y más celdas, la
   retención vendría de separar las madres por 2L y no de la tasa. La predicción es `splits_M ≈ padre`.
3. **Retener por aprender despacio.** Si la guarda pasa con `W_D` apenas ≥ 0.85, o C necesita muchas más mordidas a
   criterio, el hijo retendría por frenar lo nuevo (el fallo de K2). La predicción es que las mordidas a criterio no cambian.
4. **Premisa falsa.** Si E1 o E2 difieren del padre en alguna semilla, "mismo patrón → `kf = kc`" no se cumple (celdas
   activadas por dos patrones sin que `cond()` lo impida) y hay que auditar el diff antes de aceptar.
