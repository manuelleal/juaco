# Bloque 2 (nivel 8 propio): curiosidad por progreso de error contra el canje exploración/explotación del mapa

**Escrito ANTES de construir el instrumento y ANTES de correr. 17 sep 2026, 21:10 (día 5, noche; bloque 2 del plan del día 6).**
Regla 12.

## 0. Qué se sabe

En el mundo largo (50 patrones nuevos, uno cada 4 000 pasos; cambio de regla en t = 100 000; `r_vis = 3`, sitios fijos), el
mapa `M` da de comer (490 contra 332 en Q4, muere menos tras el cambio) pero **daña la adquisición de lo nuevo**: acierto
en los últimos 10 inyectados 0.70 contra 0.88–0.90 de v13 (dos series, 1–20 y 21–40). Causa propuesta: el sesgo del mapa
lleva al organismo a los sitios de valor conocido y **explora menos** (celdas 78 contra 90: divide menos, ve menos).
Es el canje explotación/exploración del nivel 8, medido.

## 1. Órgano candidato: curiosidad por progreso de aprendizaje (nivel8 §3, puntos 8–9; Oudeyer)

- Cada celda ya guarda `err[c]` (EMA rápida de |Δ|, `ema = 0.02`). Se añade `err_l[c]` (EMA **lenta**, `ema_l = 0.005`) con
  la misma regla local. **Progreso de la celda** = `err_l[c] − err[c]` (> 0 cuando el error está cayendo: se está
  aprendiendo; ≈ 0 cuando ya se sabe o cuando nunca se ha mordido; < 0 cuando acaba de subir). Al dividir, ambas EMAs de
  madre e hija se ponen en cero (como hace el tronco con `err`).
- **Progreso de un patrón** = media del progreso de las 3 celdas de su código Kenyon.
- **Dónde actúa:** sólo donde ya actúa el mapa, con la retina vacía: por dirección, `C_dir = Σ_h disc^h · progreso(M[pos ± h])`
  sobre los sitios recordados; `u += gamma_C · [C_izq, C_der]` además del sesgo de valor del mapa (`gamma_M · [B_izq, B_der]`).
  `gamma_C = 1.0`, `disc = 0.9`, `H = 20` (los del mapa). No toca la boca ni el aprendizaje del valor. Con `gamma_C = 0` es
  `mundo_largo` **exacto** (identidad obligatoria, 3 semillas, todas las claves).
- **Control de prioridad aleatoria** (la trampa 4 de nivel8 §6): mismo sesgo, pero el progreso se lee con las celdas
  **permutadas** (una permutación fija por semilla, RNG propio `seed + 800000`, que no toca el del organismo): misma
  magnitud, desacoplado de lo que se está aprendiendo.

## 2. Brazos (mundo largo, semillas NUEVAS 41–60, T = 200 000)

V13 · MAPA (`gamma_M = 0.6`) · **MAPA+CUR** (`gamma_M = 0.6`, `gamma_C = 1.0`) · MAPA+CUR_BARAJADA (control).
Medidas: las del mundo largo (adquisición ≤ 30 vistos y final, retención de los nunca invertidos, comida en Q4, muertes,
recuperación, celdas).

## 3. Criterios y predicción

- **P1 (recupera la exploración):** MAPA+CUR adquisición (≤ 30) mediana ≥ **0.85** y > MAPA pareado en ≥ 15/20.
- **P2 (no pierde la comida):** MAPA+CUR comida en Q4 ≥ **450** (mediana) y ≥ 0.9 × MAPA pareado en ≥ 15/20.
- **P3 (la prioridad importa):** MAPA+CUR > MAPA+CUR_BARAJADA en adquisición (≤ 30) pareado ≥ 15/20, y el control no
  supera a MAPA en ≥ 15/20 (barajar no explora "mejor").
- **Predicción:** P1, P2 y P3 pasan → "*la curiosidad por progreso devuelve la exploración sin cobrar la comida*"; entonces
  el bloque 4 (v14 = v13 + mapa + curiosidad) queda habilitado y pasa por examen v3', batería y regresión.
  **Refutación:** P1 falla (la curiosidad no explora: el progreso de sitios recordados no basta, porque lo nuevo entra en
  sitios que aún no se han visitado y su progreso es 0 hasta la primera mordida) → se registra y el siguiente candidato es
  **novedad de sitio** (sesgo hacia el sitio que lleva más tiempo sin visitarse), no otra perilla de esta. Si P2 falla:
  la curiosidad cobra la comida (canje, no solución). Nada se recalibra después de ver datos.
- Coste: 4 brazos × 20 semillas × 200 000 ≈ 6 min (mundos en Python puro; el gemelo compilado no cubre los mundos aún).
