# SÍNTESIS DE LA JUNTA DEL 21-sep-2026 (coordinador; tres creadores Opus A, B, C; propuestas en `A/`, `B/`, `C/`)

## Veredicto en una línea
**HAY ALGO Y ES EL JUEZ, NO EL ORGANISMO:** los tres creadores, sin leerse, llegaron al mismo número: el criterio de tronco v2 rechaza al propio
tronco si se lo presenta como candidato (T-A pasa un placebo el 32 % de las veces; T-A y T-C ii juntas, el 0.6 %). Mientras no se corrija, cada serie
de candidato es una moneda al aire. Nada de lo medido se rejuzga (regla 3); el arreglo rige sólo a candidatos futuros.

## Q1 — criterio v2, puertas T-A y T-C (ii) pareadas: VOTO UNÁNIME, no-regresión mal calibrada
| creador | diagnóstico | número | propuesta |
|---|---|---|---|
| A | `A₁₂ ≥ 0.50` está en el valor del nulo: con n = 20 un candidato idéntico pasa el 59 %, y en el límite el 50 %; `≥ 0.75` exige ganar en el 80 % de las semillas. Reparto de 40 semillas OFF reales (placebo perfecto): T-A pasa 0.316; T-A ∧ T-C ii 0.006. Además ρ(ON, OFF) ≈ 0: el pareado no reduce ruido en el mundo vivo | `analiza_potencia_Q1.py` | criterio v3 (A-CAL, ERR-91): no inferioridad con el margen declarado, n = 40, brazo PLACEBO obligatorio |
| B | mismo cálculo binomial: T-A (dos brazos) falla el 65 % para un candidato igual al tronco | modelo | banda de la nula `A₁₂ ≥ 0.50 − 1.645·0.5/√n` (≥ 0.32 con n = 20); capacidad sólo en T-G |
| C | T-A es "moneda, no criterio"; T-C ii (0.75) es capacidad escondida en una puerta llamada "se desdice" | — | T-A no inferioridad con `A₁₂ ≥ 0.35`; T-C ii se muda a T-G; capacidad sólo en T-G |
**Decisión del coordinador (delegada):** ERR-91 numerado hoy; CRITERIO_TRONCO_v3 en construcción por el creador A (paquete con placebo, calibración
CAL-1..CAL-5 antes de juzgar a nadie). Predicción conjunta que puede fallar: con la letra nueva, v15f y dE5 **habrían caído igual** (T-D/T-E y T-E/T-G):
la corrección no regala ningún tronco.

## Q2 — fase 5: dos votos por cerrar en 75 %, un candidato con mecanismo nuevo
- A: cerrar si la réplica cae; P6 tiene la misma patología (p ≈ 0.84 agregado en tres series → cae 1 de cada 5.9 series aunque el mecanismo no cambie). Prohibir puertas de conteo k/n sin cálculo de potencia previo.
- B: **explica por qué BA-v no distingue del todo a la hermana**: con `var_cubre=1`, una de las tres ganadoras de variante comparte casilla con la hermana en 37/37 semillas (colisión estructural); su modelo predijo BAR-H 6 y 4 contra 7 y 4 medidos. Candidato **BA-vm** (la variante vota con su peor casilla: `dentro='minv'`, memoria nueva cero; la perilla que ERR-88 halló muerta) con 18 % y R6 como riesgo (35 %).
- C: cerrar; única reapertura del brief, **V-5**: B-5 trasplantado a la tabla de referencia (la variante se parte de la familia cuando la contradice), 25 %.
**Estado de hoy:** BA-v cae P6 en 961–980 (13/19) y 981–1000 (14/18, una semilla); tercera serie 2101–2120 por regla 12, corriendo. **Decisión:** si la
tercera cae, la fase 5 se cierra en 75 % con la frase medida y BA-vm / V-5 quedan como preregistros disponibles, no en cola; si pasa, réplica y decisión del director.

## Q3 — fase 9: la letra de F9-4 no medía lo que quería; el bloque 2 tiene mecanismo y un hallazgo
- Los tres coinciden: F9-4 puntúa al control con una tasa de un solo lado (p1); el nodo barajado la infla con cautela genérica (c1 0.598). Letra correcta: índice balanceado **J = p1 + c1 − 1** (A: J(REL) 0.962, J(REL_BAR) 0.166 ≤ J(NADA) 0.186: el barajado no discrimina nada; C añade brazo CAUTELA que puede tumbarla).
- **Hallazgo de C, refutando su propia hipótesis favorita:** leer el nodo por las dos vías (`nodo_via=1`) acorta la vida a 0.38× y hunde J de 0.96 a 0.74, porque **la puerta de v14 sustituye, no suma**: en cuanto la rápida tiene evidencia, la boca abandona el −3 de la lenta por el −1 de la rápida. Bloque 2 propuesto **C-F9B′**: "leer llena la memoria; morder abre la puerta" (`nodo_via=2`, memoria nueva cero, identidad 66/66, 15 % de cruzar R₀ 0.9).
- A: bloque 2 como dosis-respuesta de la herencia con nodo oráculo como cota (si ni el oráculo cruza 0.9, el muro es el mundo). B: población con H-1 como control negativo obligatorio.
- **Réplica de hoy (1521–1540):** repite las siete puertas y las dos caídas número a número, pero cae el ancla F9-1 por 1.5 en la vida de NADA (rango [90, 170] fijado con dos series de H-1; hoy hay cuatro: 125, 119, 94, 88.5) → **ERR-92** (rango de ancla calibrado con menos series de las que existen) y tercera serie con el ancla corregida en semillas nuevas.

## Porcentajes por nivel (los tres creadores vs coordinador)
| nivel | A | B | C | coordinador | registro |
|---|---|---|---|---|---|
| 1–4 | 100/100/90/85 | 100 | 100/100/100/95 | 100 | cerrados |
| 5 | 70 | 75 | 75 | 75 | **75** |
| 6 | 50 | 50 | 50 | 60 | — |
| 7 | 60 | 70 | 85 | 70 | — |
| 8 | 35 | 40 | 40 | 40 | **40** |
| 9 | 30 | 30 | 30 | 30 (45 si el ancla corregida confirma) | **30** |
| 10+ | 10 | 10 | 10 | 10 | — |
Consenso: 6 en 50 (el coordinador baja su 60), 7 entre 60 y 85 (lo acotado hoy no es avance; se queda en 70).

## Lo que sale de aquí, en orden
1. ERR-91 (criterio v2 sin placebo) y ERR-92 (rango del ancla F9-1) al registro hoy.
2. Fase 9: tercera serie del bloque 1 con el ancla corregida (enmienda numerada, semillas nuevas), hoy si la CPU alcanza; bloque 2 = C-F9B′ + F9-4bis (J) + CAUTELA, preregistro mañana.
3. Criterio v3 con placebo (A, en construcción) antes de juzgar a ningún candidato nuevo al tronco.
4. Fase 5: se decide con la tercera serie de BA-v.
5. dE5-fam (C) y BA-vm (B): preregistros disponibles, no en cola.
6. Velocidad: gemelo numba de la fase 9 (compilador, en construcción); dos Pools cuando ninguna puerta mida tiempo de pared.
