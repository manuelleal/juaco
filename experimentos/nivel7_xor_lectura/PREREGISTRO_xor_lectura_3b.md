# Bloque 3b: ¿la puerta esconde la vía lenta? Lectura de la vía lenta a priori y `puerta = None` (escrito ANTES de correr; semillas 21–40)

**17 sep 2026, 21:40.** El bloque 3 dejó un dato no previsto: con lectura cuadrática, `W_lenta(P0·P1) = −2.65` (la vía lenta
representa XOR) y el acierto total en nunca vistos no se movió (0.438). Hipótesis: **la puerta de familiaridad** (la boca
lee la vía rápida si ≥ 3 celdas del código tienen |Wp − Wn| > 0.2) trata como "familiar" a patrones nunca vistos cuyo
código solapa con los entrenados, y en XOR el solapamiento no sigue la regla, así que lee la memoria de casos en vez de la
regla. Predicción de mecanismo, comprobable sin tocar el aprendizaje.

## Instrumento (`organismo_v13q.py` + una lectura más, por anclas: `construye_xor.py` enmienda → `W_lenta_apriori`)
En la sonda de `fase2_en`, además de `W_apriori` (valor total con puerta), se guarda **`W_lenta_apriori[k] = (Wps − Wns) @ phi(P_k)`**
(la vía lenta sola) y **`familiar_apriori[k]`** (si la puerta habría leído la vía rápida). Es lectura pura: no cambia ningún
número del organismo (identidad con `lectura='lineal'` sigue obligatoria en todas las claves del original).

## Brazos (mundo de regla, `xor01` y `px0`, T = 200 000, semillas NUEVAS 21–40)
CUADRÁTICA `puerta = 3` (como en el bloque 3) · CUADRÁTICA `puerta = None` (sin puerta: la boca suma las dos vías, un solo
error) · LINEAL `puerta = 3` (referencia). Medidas: `acc` (valor total, la de siempre), **`acc_lenta`** (signo de
`W_lenta_apriori` en nunca vistos), fracción de patrones de test "familiares" para la puerta.

## Criterios y predicción
- **Y1 (la vía lenta sabe XOR):** CUADRÁTICA `xor01` `acc_lenta` mediana ≥ **0.75** y > LINEAL `acc_lenta` pareado ≥ 15/20
  (techo ≈ 0.85–0.90 por los patrones con `P0 = P1 = 0`, sin término constante).
- **Y2 (la puerta lo tapa):** en CUADRÁTICA `puerta = 3`, `acc_lenta − acc ≥ 0.20` en ≥ 15/20, y ≥ 60 % de los patrones de
  test son "familiares" para la puerta (mediana).
- **Y3 (sin puerta se ve):** CUADRÁTICA `puerta = None` `xor01` `acc` ≥ **0.65** y > CUADRÁTICA `puerta = 3` pareado ≥ 15/20;
  y su `px0` acc ≥ 0.65 (no rompe lo lineal).
- **Predicción:** Y1–Y3 pasan → "*la lectura cuadrática generaliza XOR; la puerta de v13 confunde solapamiento con
  conocimiento y la tapa*" → la puerta pasa a ser el siguiente órgano a rediseñar (familiaridad por **patrón**, no por
  celdas: p. ej. contar visitas del código exacto), preregistro aparte. **Refutación:** Y1 falla (la vía lenta no sabe
  XOR aunque el peso del producto sea grande: entonces el problema es la falta de término constante u otras entradas) →
  se registra y se prueba `phi` con constante. Nada se recalibra después.
- Coste: 3 brazos × 2 reglas × 20 semillas = 120 corridas (~1.5 min).
