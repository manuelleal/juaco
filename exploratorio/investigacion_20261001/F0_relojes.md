# F0 — Relojes y Ne·s reales (1-oct-2026)

Script `f0_relojes.py` (un proceso, sólo lee JSON; bootstrap 10 000 con semilla 20261001; dos corridas dan salida idéntica). Salida: `f0_relojes_salida.txt`, `f0_relojes.json`. Archivos leídos: o1_libre serie 120 y réplica 120 (60 pasajes + 60 pruebas cada una), o1_evo 520, entre_linajes 170.

## 1. Lectura en una línea

**El reloj fue corto, sin duda: n ≈ 12 generaciones efectivas en los 3 pasajes de o1_libre (serie y réplica), no 150; "tuvo reloj suficiente" (n ≥ 100) CAE. "Casi neutro" (Ne·s < 1) se cumple ×2 con Ne de linajes y s por paso mutacional, pero NO DECIDE si se usa Ne de padres o la s del nivel alcanzado: los intervalos cruzan 1.**

## 2. Tabla (n = reloj mutacional del brazo NEUTRO; mediana [mín–máx] por cadena; IC95 por bootstrap sobre cadenas)

| | o1_libre SERIE | o1_libre RÉPLICA | o1_evo SERIE | entre_linajes EXPLORA |
|---|---|---|---|---|
| cadenas × pasajes × T | 10 × 3 × 100k | 10 × 3 × 100k | 20 × 10 × 25k | 5 × 10 × 25k |
| n por pasaje (mediana) | 4.7 / 3.6 / 3.1 | 4.5 / 3.3 / 3.6 | ≈ 2.0 | ≈ 1.9 |
| **n total** (vía i) | **11.2 [7.6–16.6]**, media 11.6, IC 9.9–13.4 | **11.6 [9.2–15.4]**, media 11.9, IC 10.7–13.1 | 19.2 [2.7–58.1], media 20.7, IC 16.0–26.2 | 25.3 [11.6–59.2], media 28.6, IC 14.4–44.8 |
| n total, 4 genes lejos del recorte | media 11.1, IC 9.0–13.1 | media 12.1, IC 10.6–13.5 | NO ESTÁ (ningún gen a ≥ 25σ) | NO ESTÁ (ídem) |
| n vía (ii), genealogía | NO ESTÁ; proxy por padres 14.6 [13.0–14.8]; cota por nacimientos 122 | NO ESTÁ; proxy 13.8 [13.7–15.0]; cota 122 | NO ESTÁ; cota 38.8 | NO ESTÁ; cota 38.6 |
| partos por pasaje (lib · neu) | 586 [283–669] · 592 | 578 [314–649] · 591 | 112 [61–168] · 124 | 116 [82–156] · 123 |
| fundadores por pasaje (lib · neu) | 224 [50–915] · 141; de siembra 9 | 282 [19–1029] · 184; de siembra 9 | 156 [9–394] · 132; todos de siembra | 136 [9–328] · 132 |
| padres distintos en la siembra | 24 [18–30] (neu 26) | 23.5 [18–30] (neu 25) | 18 [12–26] | 12 [7–21] |
| Ne de linajes (1/Σp², máx. 9) | 8.27 [7.28–8.67] | 8.10 [6.88–8.88] | 9 por construcción; por linaje NO ESTÁ en el JSON | 7.70 [6.77–8.69] |
| Ne de padres (1/Σp² por genoma) | 17.9 [14.5–19.7] | 17.6 [13.7–21.8] | 12.3 [9.9–20.1] | 9.1 [6.5–14.4] |
| s de MEM por paso mutacional | 0.057, IC 0.037–0.084 | 0.029, IC −0.008–0.070 | NO ESTÁ: O1_PAS no tiene gen MEM | NO ESTÁ: ídem |
| s de MEM del nivel alcanzado (frente a 0) | 0.235, IC 0.148–0.351 | 0.096, IC −0.023–0.258 | NO ESTÁ | NO ESTÁ |
| s directa mix − mixA (4 poderes) | 0.037, IC −0.053–0.129 | 0.149, IC 0.004–0.342 | NO ESTÁ (sin mixA) | NO ESTÁ |
| **Ne·s** (linajes, por paso) | **0.47, IC 0.30–0.69** | **0.23, IC −0.06–0.56** | PISO 0.17, IC 0.05–0.32 | PISO 0.05, IC −0.18–0.34 |
| Ne·s (padres, por paso) | 1.00, IC 0.64–1.48 | 0.50, IC −0.14–1.21 | PISO 0.24, IC 0.06–0.45 | PISO 0.07, IC −0.21–0.43 |
| Ne·s (linajes, nivel) | 1.93, IC 1.21–2.87 | 0.78, IC −0.19–2.08 | — | — |
| Ne·s (linajes, s directa) | 0.30, IC −0.43–1.06 | 1.21, IC 0.03–2.77 | — | — |

En o1_evo y entre_linajes el gen que más se mueve es PRUEBA (baja; s por paso −0.020 y −0.051), pero se eligió después de mirar.

## 3. Predicciones contra lo medido

- **F0, n ≤ 15 en 3 pasajes ×2: SE CUMPLE** (medias 11.6 y 11.9; IC superior 13.4 y 13.1). Una cadena de la serie llega a 16.6 y una de la réplica a 15.4. El control n ≥ 100 no gana.
- "≈ 150 generaciones" del preregistro (`PREREGISTRO_o1_libre.md:241`): **CAE por un factor ~12.** Contaba nacimientos (53 por linaje y pasaje), no profundidad.
- Las dos vías de n no coinciden si la vía (ii) se toma como nacimientos (122 frente a 12). Sí coinciden, con un 20–25 % de exceso, si se cuentan los cuerpos que de verdad paren: los ~240 partos tardíos salen de sólo ~25 padres, unos 5.7 por linaje y pasaje. El porqué (cola FIFO de hijos más colonización lateral) es inferencia; la genealogía no está guardada.
- Ne 8.1–8.5 del investigador: **SE CUMPLE** (medianas 8.10–8.27 en lib, 8.40–8.53 en neu; es Ne de linajes).
- 18–30 padres distintos, mediana 24: **SE CUMPLE** (lib 18–30, medianas 24 y 23.5).
- s ≈ 0.05: **el punto se reproduce a su modo** (mediana/mediana 0.058 y 0.066), **pero no se sostiene como número**: con medias da 0.037 (IC cruza 0) y 0.149. En la serie, los nacimientos del lado lib bajan con poderes (−0.077); la diferencia viene de que el lado O1 pierde más.
- "5–13 pasos mutacionales": SE CUMPLE en el extremo alto (11–12).
- Colonia "116–162 por pasaje": no coincide; medianas por pasaje 107–292, rango 0–1020.
- Contraste con la otra sesión (10 genes de O1, siembra final): 11.5 [8.7–16.2] y 12.0 [9.3–13.4] en neutro; 13.9 y 14.5 en lib. Mi conjunto `O1x10` da exactamente lo mismo. Mi cifra principal usa 8 genes (≥ 10σ del recorte) y difiere en 0.3–0.4.

## 4. Supuestos y debilidades

- **n vía (i)** cuenta eventos de mutación (incluye uno por siembra), no generaciones puras. Es exacto sólo si los genes no se leen (V6 True). El recorte sólo puede bajarlo: los 4 genes a ≥ 25σ dan lo mismo y los 4 poderes, con 14–20 % de genomas pegados al 0, dan 8.7–11.2; no esconde un n grande. Los 90 genomas de una siembra son casi clones (≈ 25 padres): el n por cadena es ruidoso y el IC vale sobre cadenas.
- **n en o1_evo y entre_linajes** se apoya en 2 genes (PRUEBA, PEN_OTRO); cadenas sueltas llegan a 58–109. Con sólo esos dos genes no pude separar si esa cola es ruido o arrastre.
- **s por el modelo del criador** (β = D / (n·V)): supone gradiente lineal y V constante, pero V arranca en 0. El recorte en 0 empuja la media del neutro (0.07) y no se cancela del todo en D. Los 14 genes mutan juntos, así que D de MEM puede ser arrastre de PISO.
- **PISO se mueve 10/10 ×2** (D 0.125 las dos veces; Ne·s por paso 0.80 y 0.70): el montaje sí transmite selección de ese tamaño en 12 generaciones. Debilita "casi neutro" como explicación única.
- **s directa**: mixA apaga los 4 poderes, que vuelven a mutar durante la prueba; no aísla MEM; 10 índices.
- **Ne de padres** junta padres de 50k pasos y supera el censo (9 cuerpos): es cota alta, no Ne por generación. El cuello real entre pasajes son 9 fundadores de siembra; el resto entra por colonia.
- **NO ESTÁ**: partos encadenados (la fila guarda conteos y `siembra_sig`); `tarde` y linaje de cada entrada en o1_evo; réplica de o1_evo y de entre_linajes.

Parámetros: σ 0.03 `corre_o1_libre.py:71`; 3 pasajes, T 100k, 90 partos `:80`; siembra, Ne y padres `:178-195`; genes, fábrica, recorte y escala `construye_o1_lib.py:53-59` (`carros/O1_LIB.py:39-42`); mutación de los 14 genes `O1_LIB.py:203-205`; neutro `:209`; colonia `:193-195`; cola FIFO `carrera_escuderias/pista.py:340,369-370`. o1_evo: genes y recorte `construye_o1_pas.py:45-47`; mutación sin escala `:66-68`; 10 × 25k `corre_o1_evo.py:69`; siembra de vivos `:130-137`. entre_linajes: `corre_entre_linajes.py:44`; siembra proporcional `camara_linajes.py:142-160`.

---

## Fe de erratas (1-oct-2026, tras la auditoría; ver `AUDITORIA_F0.md`)

El texto de arriba no se reescribe. Estas correcciones mandan sobre él.

1. **Línea de lectura (`:7`).** Donde dice "sin duda", "n ≈ 12 generaciones efectivas" y "CAE", debe leerse: *reloj mutacional ≈ 12 eventos a lo largo de la ascendencia (profundidad mutacional media de los padres muestreados); n ≥ 100 (mutacional) no se cumple*. La profundidad mutacional subestima las rondas de selección: hay ~224 refundaciones por pasaje que copian de los últimos 50 partos sin sumar profundidad. **El reloj de selección entre linajes (reemplazos por cuerpo) no está medido.**
2. **Ne·s (`:7`).** Donde dice "los intervalos cruzan 1", debe leerse: *en la serie, dos de cuatro definiciones quedan por encima de 1 con IC que excluye 1 (linajes por nivel 1.93, IC 1.21–2.87; padres por nivel 4.13, IC 2.6–6.2); en la réplica todas cruzan 1*. "Casi neutro" sólo sale con la definición más favorable (Ne de linajes, s por paso).
3. **o1_evo y entre_linajes (`:15` y tabla).** No usar 19.2 ni 25.3 como cifras. Debe leerse: *orden de 20–30, muy por debajo de 100, una sola serie, genes limitados*. Cadenas de 3 a 58, incrementos negativos por pasaje, 5 cadenas en entre_linajes, y en o1_evo la siembra viene de vivos, no de partos (no comparable con o1_libre).
4. **Ne en la tabla (`:21-22`).** Ne de linajes es 1/Σp² de aportes por linaje, con máximo 9: no es un Ne genético. Ne de padres junta padres de 50k pasos y supera el censo: es cota alta.
5. **"CAE por un factor ~12" (`:36`).** Compara dos cosas distintas: 150 son nacimientos por línea (3 pasajes × ~50 por linaje); ~12 son eventos de mutación en la ascendencia de un genoma. Los nacimientos sobreestiman la profundidad; la profundidad subestima las rondas de selección.
6. **s de MEM.** Usa el n del neutro, pero el brazo lib tiene n = 14.3–14.6: s queda sobreestimada hasta ~23 % (0.057 → ~0.046; 0.029 → ~0.023). Posible arrastre de PISO en la serie (correlación entre cadenas 0.63; −0.07 en la réplica). La réplica no replica a MEM (6/10; el IC de D cruza 0).
7. **Desviación de la ficha.** La ficha pedía 10 genes sin recorte; el script usa 8 (≥ 10σ). Con 10 da lo mismo (11.87 y 11.65).
