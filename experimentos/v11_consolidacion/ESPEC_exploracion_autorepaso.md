# Especificación para la exploración K6 — auto-repaso desde prototipos (consolidación SIN almacén)

**16 sep 2026, día 4. Es una especificación para un subagente explorador; no es un preregistro.**
Se lanza después de que terminen las corridas de v10 (regla 11) y sobre la base que resulte (v10 si se congela).

## Idea
El olvido de la Etapa 4 tiene dos vías: (1) deriva de valor en celdas compartidas sin re-muestreo; (2) celdas hijas que
suplantan el código viejo (v10 quita buena parte de la 2). K4 (repaso desde un almacén de pares patrón→R) arregla las dos,
pero guarda las respuestas fuera del organismo ("memoria escondida"). **K6 propone que el organismo se repase a sí mismo
con lo que ya tiene:**
- cada celda activa guarda ya un **prototipo** (`mu[c]`, la media móvil de los patrones que la activaron) y un **valor**
  (`Wp[c] − Wn[c]`);
- cada `r` pasos, para cada celda **consolidada** (`|Wp[c] − Wn[c]| ≥ u`), se reconstruye su patrón `P̂ = mu[c]` normalizado
  a masa 3, se calcula `code(P̂)` con la KW actual, y se aplica **una** actualización Rescorla-Wagner sobre ese código con
  objetivo `R̂ = 3·(Wp[c] − Wn[c])` (cada celda lleva ~1/3 del valor del patrón), tasa `eta_r = eta/3`, con drenaje, sin
  morder, sin energía, sin RNG y sin divisiones;
- es decir: **la celda vieja re-enseña su valor a las celdas que hoy codifican su patrón.** Si D pisó las celdas de B, las
  celdas de B que quedan las corrigen; si una hija suplantó a B, la madre la re-entrena.

## Qué distingue a K6 de K4 y qué lo haría pasar por la razón equivocada
- **No hay almacén:** lo único que se usa es estado del organismo (`mu`, `Wp`, `Wn`, `KW`). Control: K6 con `mu` borrada al
  cambiar de fase debe perder el efecto (si no, la memoria está en otra parte).
- **Riesgo 1: rigidez.** Si el mundo cambia (E2, inversión), K6 podría re-enseñar el valor **viejo** y frenar la reversión.
  Medir E2 completo (`|W_A+3|<.3`, `|W_B−1|<.15`, mordidas B Q4 ≥ 50) y `t90` de la reversión frente al control.
- **Riesgo 2: retener por no aprender.** Medir `W_C`, `W_D` en 100k y mordidas de C hasta `W_C ≤ −2.5`.
- **Riesgo 3: `mu` arrastrada.** Si `mu[c]` se contaminó con D, `P̂` es un híbrido y el repaso enseña a un patrón que no
  existe. Medir `|P̂ − patrón real|` de las celdas consolidadas y cuántas repasan un híbrido.
- **Riesgo 4: eco.** Dos celdas consolidadas del mismo patrón con valores distintos se pelean. Medir varianza de W entre
  repasos.

## Variantes (base v10; con el órgano apagado ≡ base)
- K0 control; K0f (congelado en la ausencia); K4 (r=100, n=8) y K4c (almacén borrado por fase), como referencia.
- **K6** con `u ∈ {0.5, 1.0}` y `r ∈ {100, 200}`; K6m (`mu` borrada por fase, control).
- K6+K4 sólo si K6 sola no basta.

## Mundos
1. Bloque M de la Etapa 4 (retención y plasticidad), 20 semillas.
2. **Capacidad**: mundo de 20 patrones de peso 3 (2K-bis), 8 estímulos de entrenamiento en [0,60k), ausentes en
   [60k,120k) mientras entran 8 nuevos, y vuelven en 120k. Aquí K4 con n=8 **no puede** guardar los 16: si K4 retiene igual
   que en el bloque M, el almacén no es lo que retiene; si K6 retiene, la consolidación es real.
3. No-regresión E1/E2/E2L, 20 semillas.

## Entrega
Tabla por variante con los dos lados del dilema (retención / plasticidad), E2 con `t90`, capacidad, coste y riesgo; UNA
propuesta para preregistrar como v11 con predicciones numéricas, refutación y controles.
