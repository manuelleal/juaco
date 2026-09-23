# PREREGISTRO — MUNDO ANCLADO v2 (rama `mundo-anclado`, 22-sep-2026) · **ERR-? pendiente** (lo numera el coordinador)

Misión: llegar a la AGI por este camino. **Es una enmienda de diseño después de un NO.** Se escribió después del humo v2
(semilla 1, ya vista; `datos/humo/anclado2_humo_20260922_142242.json`, sha `18b8aaf07a1ae6eb`) y ANTES de tocar las
semillas 7021–7040 (calibración), 7041–7060 (confirmación) y 7061–7080 (réplica). No se edita después de la primera
corrida de calibración: los cambios van como ENMIENDA fechada al final.

## 0. Antecedente: la v1 (commit afcc7e9, NO)
`PREREGISTRO_mundo_anclado.md` usaba una sola perilla, la dilución por objeto de lo malo (`olv_mal`). En 7001–7020
subió a NADA y a ORÁCULO **en la misma proporción**: la razón ORÁCULO/NADA fue 3.09, 2.97 y 3.18 en h = 0.0005, 0.001 y
0.0015. Las anclas piden ≥ 3.33. El mejor punto (h = 0.0015) dio ORÁCULO 1.000 y NADA 0.314. Se siguió la regla y no se
amplió. **ERR-? (lección de diseño):** una perilla que sólo sube el NIVEL no puede anclar. Hace falta además una que
abra la RAZÓN. Las semillas 7001–7020 quedan vistas y no se reusan.

## 1. Hipótesis
H-ANC2: con dos perillas del mundo existe un punto donde NADA no sostiene un linaje (R0 ∈ [0.10, 0.30]) y ORÁCULO sí
(R0 ≥ 1.0):
- la **toxicidad** de lo malo castiga la ignorancia (morder lo malo), no el conocimiento, y ABRE la razón;
- la **dilución** repone la comida del que rechaza y SUBE el nivel.

## 2. Perillas (dos, las dos del mundo y por objeto; memoria nueva CERO; cuerpo sin cambios)
- **`tox = k`**: cada bocado de un objeto malo hace k veces su daño nominal. La tabla del mundo queda veneno (−0.4k, 0)
  y sal (0, −0.4k); lo bueno no cambia. Se pasa por el kwarg `tabla`, que ya existe en `organismo_f9c`.
  - El cuerpo aprende sólo del SIGNO de la consecuencia (`_Rv`: +1 / −3), así que el aprendizaje y el ORÁCULO (que
    lee el signo de la tabla) no cambian; cambia el precio de la ignorancia.
  - Con tox = 1 la tabla es idéntica a EFECTO: el humo lo comprueba con el dict completo, OK.
  - Escala: la dosis es POR BOCADO y POR OBJETO. Por cuerpo se lee contra la reserva del recién nacido (dote 0.6): con
    tox ≥ 1.5, el primer bocado malo de un recién nacido lo mata.
  - Justificación: en el humo de toxicidad (v1, semilla 1, h = 0.003), ×2 llevó la razón de ~3 a ~10 (NADA 0.038,
    ORÁCULO 0.394). En el humo v2 (semilla 1) la razón fue:

    | tox | h | razón | NADA | ORÁCULO |
    |---|---|---|---|---|
    | 1.25 | 0.006 | 4.4 | 0.61 | 2.67 |
    | 1.5 | 0.006 | 5.9 | 0.19 | 1.15 |
    | 2.0 | 0.012 | 9.3 | 0.24 | 2.23 |
- **`olv_mal = h`**: la de la v1. Instrumento `organismo_anclado.py`, sha `e689c2952b1991a4`, identidad bit a bit con
  `organismo_f9c`. Probabilidad POR OBJETO y POR PASO; escala con `nobj = 4·N`. Justificación: en la v1 sube el nivel de
  forma monótona (ORÁCULO 0.61 → 0.75 → 1.00); con tox el ORÁCULO cae (humo: 0.394 con tox 2 y h = 0.003), y la
  dilución lo devuelve.
- `rep_acum = 0` (sin cambios; la v1 explica por qué no se usa). T = 100 000.
- Brazos: `corre_bloque2.BRAZOS` (el mismo objeto) más `rep_acum`, `olv_mal`, `olv_ciego`, `anc_mide` y `tabla`. La
  regla 14 se imprime.
- Peldaños biológicos: la toxicidad es la presión de selección de presas venenosas (aposematismo sin señal); la
  dilución es un quimiostato o descomponedores (capacidad de carga).

## 3. Anclas (iguales que en la v1)
- **ANC-1** NADA: R0 mediana ∈ [0.10, 0.30].
- **ANC-2** ORÁCULO: R0 mediana ≥ 1.0.
- R0 = descendientes / (muertes + 1).
- REL no se calibra: en la confirmación se mide su posición (R0_REL − R0_NADA) / (R0_OR − R0_NADA).

## 4. Controles que pueden fallar (confirmación; mismas puertas que la v1, `CA.juzga`)
- **CTL-1 BARAJA**: REL_BAR con posición ≤ 0.35 y A12(REL > REL_BAR) ≥ 0.75.
- **CTL-2 PLACEBO**: la dilución ciega con misma dosis y misma tox. ORÁCULO_CIEGO < 1.0 y A12(ORÁCULO > CIEGO) ≥ 0.70.
  Si CAE, lo que ancla es el recambio, no el tipo.
- Se reportan sin juzgar: NADA_CIEGO, RENACE, f_mala (trampa "mundo que se come la comida": f_mala de ORÁCULO < 0.25
  se declara) y J = p1 + c1 − 1 (trampa 2).
- Trampa propia de la v2: **"la toxicidad mata al recién nacido antes de aprender"**. Esto no rompe el ancla (es
  justo el costo de la ignorancia), pero si la vida mediana de NADA baja de 30 pasos se declara que la ignorancia muere
  en el primer bocado y no por falta de aprendizaje a lo largo de la vida.

## 5. Regla de calibración y de elección (7021–7040, sólo NADA y ORÁCULO)
Rejilla de 3 × 3: tox ∈ {1.25, 1.5, 2.0} (filas) × h ∈ {0.003, 0.006, 0.012} (columnas).
(a) Cada fila se corre por separado (`--calibra --fila K`), con h ASCENDENTE.
(b) Dentro de una fila se para en cuanto ORÁCULO ≥ 1.0 (con h mayor sólo se infla el mundo) o NADA > 0.30 (con h mayor
    no vuelve al ancla). Supuesto declarado: R0 de los dos brazos crece con h.
(c) **Elección:** entre los puntos corridos que cumplen ANC-1 y ANC-2, el de **menor R0 de ORÁCULO** (para no inflar
    el mundo). Empate: menor tox y, si sigue, menor h. `--elige` lo aplica sobre los JSON de las tres filas (prefijo +
    sello exacto, ERR-87).
(d) Si ningún punto cumple, es un **NO**, sin ampliar la rejilla.

## 6. Confirmación y réplica
- **Confirmación** en 7041–7060: NADA, ORÁCULO, REL, REL_BAR, ORÁCULO_CIEGO, NADA_CIEGO y RENACE, en el punto elegido.
  Comando: `corre_anclado_v2.py --confirma --tox K --h H --desde 7041 --pool N`.
- **Réplica** en 7061–7080 con el mismo comando y `--desde 7061`.
- Veredicto:
  - FUNCIONA si ANC-1, ANC-2 y CTL-1 pasan en la confirmación y en la réplica.
  - HAY ALGO MODESTO si las anclas pasan en una sola de las dos, o si pasan y CTL-1 cae.
  - NO si no hay punto, o si las anclas caen en las dos.

## 7. Predicciones firmadas (creador, antes de calibrar)
- **Q1 (punto)**: tox = 1.5, h = 0.006. Rango: tox ∈ {1.5, 2.0}, h ∈ {0.006, 0.012}. La fila tox = 1.25 no ancla
  (NADA > 0.30 antes de que ORÁCULO llegue a 1.0).
- **Q2 (calibración en el punto)**: NADA 0.12–0.26; ORÁCULO 1.00–1.40; razón ≥ 5.
- **Q3 (REL)**: R0 de REL en la confirmación = **0.85** (rango 0.65–1.05). Su posición en el espacio NADA–ORÁCULO =
  0.80 (rango 0.65–0.95). Base: humo de toxicidad, 0.348 frente a 0.394 y 0.038, posición 0.87. Bloque 2: 0.80–0.84.
- **Q4**: las anclas se sostienen en la confirmación y en la réplica.
- **Q5**: CTL-1 pasa. **Q6**: CTL-2 pasa (confianza media, ~65 %; con tox el recambio ciego también devuelve veneno).
- **Q7**: vida mediana de NADA < 40 pasos en el punto (la trampa de la sec. 4 se declara).

## 8. Qué lo refuta
Ningún punto de la 3 × 3 ancla (5d); las anclas caen fuera de la calibración; o CTL-1 cae (REL no se distingue de un
nodo sin contenido).

## ENMIENDAS
(ninguna)
