# Bloque 3 (apuesta de frontera): ¿es XOR un límite de LECTURA o de representación? Vía lenta cuadrática, Kenyon congelado

**Escrito ANTES de construir el instrumento y ANTES de correr. 17 sep 2026, 21:20 (bloque 3 del plan del día 6).** Regla 12.
Es la apuesta del debate (`DEBATE_y_plan_5a10.md` §4, Cover 1965): la regla no lineal de la Etapa 3 (`xor01`: comida si
`px0 ≠ px1`) no se generaliza (0.44 en v9) porque la **lectura** es lineal en los píxeles, no porque el código Kenyon no
la contenga. Se cambia sólo la lectura de la vía lenta; Kenyon, la vía rápida, la puerta y la boca no se tocan.

## 1. Instrumento `organismo_v13q.py` (desde `organismo_v13g.py` `2a80e125f8593bf2`, por anclas; `lectura='lineal'` ≡ v13g exacto)

Knob `lectura`: **lineal** (6 píxeles: v13 tal cual) · **cuadrática** (6 píxeles + los 15 productos de pares `P_i·P_j`, 21
entradas) · **random15** (control: 6 píxeles + 15 bits fijos al azar por patrón, RNG propio `seed + 900000`: misma
dimensión, sin estructura). `Wps/Wns` pasan a 21 entradas; la regla de aprendizaje, el drenaje y el tope son los mismos,
sobre `phi(P)`. Identidad obligatoria: `lectura='lineal'` ≡ `organismo_v13g` en `xor01` y `px0`, semillas 1–3, todas
las claves. En el espacio cuadrático XOR es lineal: `f = P0 + P1 − 2·P0·P1`; la vía lenta puede representarlo con
`Wps` en `P0, P1` y `Wns` en `P0·P1`.

## 2. Diseño (mundo de regla de la Etapa 3 / `bateria_generaliza`: 20 patrones de peso 3, T = 200 000, sonda a priori en T/2)

Brazos: LINEAL (`eta_s = 0.015`, `puerta = 3`), CUADRÁTICA, RANDOM15 · reglas: **`xor01`** (la pregunta) y `px0`, `azar`
(regresión de la Etapa 3) · semillas 1–20. Medidas de la batería: **acc** = acierto de signo a priori sobre los 10 patrones
**nunca vistos** (sonda en T/2, antes de verlos), **ba** = conducta al primer encuentro, cobertura.

## 3. Criterios y predicción

- **X1 (la apuesta):** CUADRÁTICA `xor01` acc mediana ≥ **0.80** y > LINEAL pareado en ≥ 15/20. **X0:** LINEAL `xor01` acc
  ≤ 0.60 (la lectura lineal no puede: si supera 0.60, la premisa estaba mal y se registra).
- **X2 (no es la dimensión):** RANDOM15 `xor01` acc ≤ **0.60**.
- **X3 (regresión):** CUADRÁTICA en `px0` acc ≥ 0.65 y en `azar` acc ∈ [0.35, 0.65] (lo que exige `bateria_generaliza`).
- **X4 (conducta):** CUADRÁTICA `xor01` ba ≥ 0.55 y > LINEAL pareado en ≥ 15/20.
- **Predicción:** X0–X4 pasan → "*XOR era un límite de lectura: con productos de pares en la vía lenta, v13 generaliza la
  regla no lineal sin tocar Kenyon*". Entonces la vía cuadrática es candidata a órgano del tronco (bloque 4: examen v3',
  batería, regresión; y hay que medir si cuesta capacidad o retención). **Refutación:** X1 falla con X2 y X3 pasando → el
  límite no es (sólo) de lectura: la vía lenta con esta regla de aprendizaje no encuentra el peso negativo del producto, o
  el tiempo no alcanza; se registra la curva de `W_lenta` sobre `P0·P1` para decir cuál. Nada se recalibra después.
- Coste: 3 brazos × 3 reglas × 20 semillas = 180 corridas de 200 000 (Python puro, ~2 min).
