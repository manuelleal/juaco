# v10 = v9 + dirección de división con `mu` NORMALIZADA — confirmatorio en semillas nuevas y examen de congelación

**Escrito ANTES de construir `organismo_v10.py` y antes de correr. 16 sep 2026, día 4.**

- **Dirección:** Christiam Puentes delegó la decisión ("decide tú"). Decisión: v10 corrige un defecto de la regla 2L
  antes de añadir ningún órgano nuevo.
- **Ejecución:** en el repo. Si algo falla, no se recalibra (regla 3).

## 0. Qué se sabe antes de escribir (se declara)

- **El defecto.** En la regla 2L, la dirección de división es `dist = P − mu[c]`, con `mu[c]` una media móvil (tasa
  0.02) que **arranca en cero y no converge**: tras ~50 mordidas vale ≈ 0.63·P. El preregistro de 3T (día 3) ya lo
  anticipó como modo de fallo ("`mu` arranca en cero, no en el patrón medio").
- **Su consecuencia, medida en la Etapa 4:** la celda hija queda tan activa para el patrón viejo como la madre, entra
  en su código y **B lee el valor de D**. Es la vía estructural del olvido (corr +0.78 con las divisiones).
- **La corrección (K5 de la exploración de consolidación, `JUACO/exploracion/consolidacion_20260916/`):** normalizar
  `mu[c]` a la masa del patrón antes de restar: `dist = P − mu[c]·(ΣP / Σmu[c])`. Una línea, cero parámetros.
- **Cifras exploratorias conocidas (semillas 1–20, SIN valor confirmatorio):** hijas en el código de B en 100k: 0 en
  11/20; componente estructural de ΔW_B de +2.0 a +0.46; retención `W_B ≤ −2` 10/20 (v9: 7/20), `W_A ≥ 0.5` 11/20
  (v9: 10/20); **E2 y E2L terminan con exactamente 3 divisiones en 20/20** (v9: medianas 5 y 6); E1/E2/E2L 20/20.
- **Lo que v10 NO pretende:** cerrar la Etapa 4. Quita la mitad de la vía estructural; la deriva de valor sigue.

## 1. Instrumentos (anclas; origen comprobado por sha)

- **`organismo/organismo_v10.py`** desde `organismo/organismo_v9.py` (`d3b72fb8819fbe8e`): parámetro `mu_norm=True`;
  con `mu_norm=False` es v9 exacto. Única línea de comportamiento cambiada: la de `dist`.
- **`organismo/bateria_v10.py`** desde `bateria_v9.py` (`c6496196990f6774`) con sustituciones contadas: identidad
  `v10(mu_norm=False) ≡ v9`; ningún criterio ni umbral cambia.
- **`experimentos/v10_direccion_division/organismo_v10m.py`** desde v10, con la misma instrumentación de fases de
  `organismo_v9m.py` **más** la sonda de códigos (índices de las 3 celdas de cada patrón en cada cambio de fase). Las
  celdas con índice ≥ 30 son hijas por construcción.

## 2. Criterios y predicciones

**Q0 [instrumento]. Si falla, se para.**
- `v10(mu_norm=False)` ≡ v9 en todas las claves de v9, 7 escenarios × semillas 1..6.
- `v10m` con valores por defecto ≡ v10 (E1, E2, semillas 1..3).

**Q1 [examen de congelación, semillas 1–20]:** `bateria_v10.py 20 --log` cumple el criterio v3 completo (8/8), sin
cambiar un umbral.

**Q2 [economía de la plasticidad, derivada]:** en el examen, `splits == 3` en E2 en ≥ **18/20** y en E2L en ≥ **18/20**.
- *Por qué:* con la dirección corregida, la primera división ya separa; las divisiones extra de v9 eran hijas que no
  se alejaban y volvían a disparar.

**Q3 [la vía estructural, semillas NUEVAS 21–40, bloque M de la Etapa 4]** (`v10m` con `mu_norm=False` = v9, frente
a `mu_norm=True` = v10; misma instrumentación):
- semillas con ≥ 1 hija en el código de B en 100k: v9 ≥ **10/20**; v10 ≤ **5/20**;
- ΔW_B (100k − 50k) de v10 **< v9**, pareado, en ≥ **12/20**, y nunca > v9 + 0.5.

**Q4 [retención, sin cerrar la Etapa 4]:** en 21–40, `W_B(100k) ≤ −2`: v10 ≥ v9 en recuento, **y** v10 ≥ **8/20**.
- **Guarda:** `W_C(100k) ≤ −2.5` y `W_D(100k) ≥ 0.85` en ≥ 17/20 (no retiene por no aprender).

**Q5 [regresión]:** `bateria_v9.py 6` cumple y `manifiesto.py --check` da los 8 congelados intactos.

## 3. Qué se decide

- **Q0–Q5 sostenidas:** **v10 se congela como tronco** (tag `v10-tronco`; `organismo_v10.py` y `bateria_v10.py` en
  `CONGELADOS`). La Etapa 4 **sigue abierta**; el siguiente candidato (consolidación) se construye sobre v10.
- **Falla Q0:** se para y se arregla el instrumento.
- **Falla Q1, Q2, Q3 o la guarda de Q4:** v10 no se congela. Se registra y se rediseña con preregistro nuevo.
- **Falla Q4 sola (retención no mejora):** v10 **se congela igual si Q2 y Q3 pasan**, porque corrige un defecto medido
  de la regla y hace la plasticidad más económica; se registra que la retención necesita otro órgano.

## 4. Qué NO prueba

Consolidación de valor, herencia, comunicación. Sólo que la dirección de división ya no fabrica hijas que suplantan
al patrón viejo, y que nada de lo anterior se rompe.
