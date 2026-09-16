# Examen de CONGELACIÓN de v8 — criterio v3 (pasos 2 y 3 fundidos)

**Escrito ANTES de construir `organismo_v8.py` y `bateria_v8.py`, y antes de correr nada. 16 sep 2026, día 4.**

- **Dirección:** Christiam Puentes. Fundió los pasos 2 y 3, aprobó los nombres y ordenó congelar si pasa.
- **Ejecución:** en el repo.

## 0. Qué es v8 y qué se sabía antes de escribir esto

**v8 = v6 + 2L (plasticidad estructural) + drenaje de la parte común de `Wp`/`Wn` con `lam=0.05`.**
- Se genera por anclas desde `experimentos/bug01/organismo_v7e.py` (`3118c6d563542da2`).
- Único cambio de comportamiento respecto de v7e: `lam` pasa a valer **0.05 por defecto**.
- Añade instrumentación de sólo lectura, sin tocar el RNG ni el estado:
  - **`err_max`**: medido tras actualizar `err` y antes de dividir;
  - **`t_conflicto`**: primer paso en que alguna celda del código mordido queda con `min(Wp,Wn) > 0` tras la
    actualización. Es el primitivo oficial de ERR-10;
  - **`t_techo`** y **`n_techo`**: la mordida del techo de la prueba de coste.
- Con `lam=0`, v8 es v7.

**Conocido y declarado:**
1. **Examen de v7 con el criterio v2** (día 3): los criterios científicos pasaron 20/20 en las seis etapas, con
   `celdas ≤ 45` y el control negativo válido (0/20). Falló sólo el disparo por solapamiento, que quedó refutado.
2. **Exp. 2b, P2c** (día 3): las seis etapas pasan 20/20 sus criterios con `lam=0.05`.
3. **Prueba de coste** (hoy): antes de la primera truncación del clip, `lam=0.05` y `lam=0` son idénticos (S0, C0).
4. **ERR-12** (hoy):
   - la concordancia `splits>0 ⇔ err_max>0.6` es una **identidad del código** mientras quedan celdas libres;
   - "con solapamiento 0 no puede disparar" es falso: en E2, B se divide hacia t≈53k (semillas 1–3, medido hoy).
5. **Predicción pendiente del día 3:** forzar C∩B=3 con C veneno (misma valencia que B) debe dar 0 divisiones.
   El sorteo de códigos es viable: 34 a 1.362 intentos por semilla, medido hoy sin simular.

## 1. Etapas (v8 con sus valores por defecto, 20 semillas)

| etapa | llamada | por qué está |
|---|---|---|
| E1 | `run(s)` | aprendizaje A/B |
| E2 | `run(s, invertir_en=50000)` | inversión |
| E2I | `run(s, nuevo='C')` | estímulo nuevo veneno |
| E2J | `run(s, nuevo='D', nuevo_val='comida', solap_B=1)` | valencia opuesta, 1 celda |
| E2K | `run(s, nuevo='D', nuevo_val='comida', solap_B=2)` | valencia opuesta, 2 celdas |
| E2L | `run(s, solap_AB=3)` | rescate por plasticidad |
| CTRL | `run(s, solap_AB=3, plast=False)` | control negativo: sin plasticidad debe fallar |
| **E2I-misma** | `run(s, nuevo='C', solap_B=3)` | **nueva**: C veneno con el mismo código que B |

## 2. Criterio v3 — v8 se congela si y sólo si TODO esto se cumple con 20 semillas

**1. Criterios científicos**, idénticos a `bateria_v7b.py`, **20/20** en cada una de las seis etapas:

| etapa | criterios |
|---|---|
| E1 | mordidas de veneno Q4 < Q1; `|W_A−1| < .15`; `|W_B+3| < .3` |
| E2 | `|W_A+3| < .3`; `|W_B−1| < .15`; come B en Q4 ≥ 50 |
| E2I | `W_C ≤ −2.5`; `|W_A−1| < .15`; `W_B ≤ −2.8`; tasa de A en Q4 ≥ 80% de la de Q2 |
| E2J | `W_D ≥ .85`; `W_B ≤ −2.7` |
| E2K | `W_D ≥ .8`; `W_B ≤ −2.4` |
| E2L | `|W_A−1| < .15`; `|W_B+3| < .3`; solapamiento final A∩B = 0 |

**2. `celdas ≤ 45`**, 20/20, en las seis etapas y en E2I-misma.

**3. Control negativo válido:** en CTRL pasan como máximo **1/20** los criterios de E2L sobre `W_A` y `W_B`.
Con v8 se predice **0/20**, y por una razón distinta a la de v7: sin plasticidad A y B tienen el **mismo código**,
así que `W_A = W_B` y no pueden valer +1 y −3 a la vez. El drenaje quita el colapso a 0, no la identidad de
códigos. En el escenario BUG el exp. 2 midió `W = −1.36` en ambos.

**4. Disparo**, reescrito tras ERR-12:
- **4a [comprobación del instrumento, NO es evidencia].** En toda corrida con plasticidad y `celdas < 90`:
  `splits > 0` ⇔ `err_max > 0.6`, **100%**. Es una identidad del código.
  - Si falla, lo que está roto es la instrumentación: se para y no se lee nada más.
  - **No suma a favor de congelar.**
- **4b [derivada, falsable]. Sin conflicto no hay división.** En toda corrida de las seis etapas y de E2I-misma
  con `splits > 0`, `t_conflicto` no es nulo y `t_conflicto ≤` el paso de la primera división: **100%**.
  - **Por qué:** en una celda que sólo ha recibido `dlt` de un signo, con |dlt| ≤ 3 y sin dos episodios de
    aprendizaje superpuestos, `err_max ≤ 0.4425` más un residual que decae; no llega a 0.6.
  - **Qué la refuta:** una sola corrida que divida sin conflicto previo.
  - **Alcance:** vale para estas etapas, no como ley general; dos episodios del mismo signo simultáneos podrían
    sumar.
  - **Guarda (añadida al releer antes de correr).** 4b pasaría sola si `t_conflicto` no detectara nada. Por eso
    sólo se lee si el detector demuestra que funciona en los dos sentidos:
    - `t_conflicto` **nulo** en E1, 20/20 (A∩B=0 y R constante por estímulo: ninguna celda recibe `dlt` de los
      dos signos);
    - **no nulo** en E2L, 20/20 (conflicto congénito).
    - Si no, el detector está roto y 4b cuenta como **no cumplida**.
- **4c [predicción pendiente del día 3, falsable].** En E2I-misma: `splits == 0` en **20/20** **y** `W_C ≤ −2.5`
  en **20/20**.
  - **Por qué:** C entra en t=50.000 con el código de B, que ya vale −3; su `dlt` es ≈0 y no hay error ni conflicto.
  - C **hereda el valor de B sin una sola experiencia**: es generalización por identidad de código.
  - **Guarda (añadida al releer antes de correr).** 4c pasaría sola si C no tuviera el código de B o no se
    mordiera nunca. Sólo se lee si, en 20/20:
    - `solap['nB'] == 3` al final (sin divisiones, final = inicial);
    - hay mordidas de C en Q3+Q4 > 0.
    - Si no, 4c cuenta como **no cumplida**.
- **4d [disparo anclado a la causa**, lo que sobrevive del criterio v2 corregido por ERR-08]:
  - E1: `splits == 0`, 20/20. No hay conflicto.
  - E2, E2I, E2J y E2K: todas las divisiones en `t ≥ 50.000`, 20/20. Ninguna antes de la causa.
  - E2L: `splits > 0` y la última división en `t < 25.000`, 20/20. El conflicto es congénito y la separación
    termina pronto. El umbral de 25.000 viene del registro (2L v2), no de estos datos.

**5. Identidad de los instrumentos.** Si falla una sola comparación, no se corre el examen.
- `v8` ≡ `v7e(lam=0.05)` en todas las claves de v7e, en los 7 escenarios de la prueba de coste × semillas 1..6.
- `v8(lam=0)` ≡ `organismo/organismo_v7.py` en todas las claves de v7, en los mismos 7×6.

**6. Regresión del tronco anterior.** `organismo/bateria.py 20` PASA y `manifiesto.py --check` da los 4
congelados intactos, **antes** (hecho hoy, 14:41, 20/20) y **después**.

## 3. Predicción

**Todo pasa.**
- **Criterios 1–3 y 4d:** los pasó v7 en el día 3, P2c los pasó con `lam=0.05`, y S0 garantiza la identidad hasta
  la truncación.
- **4a:** es una identidad.
- **Lo que de verdad puede caer es 4b y 4c,** y por eso están aquí.

## 4. Qué se decide

- **Si todo pasa:** **v8 se congela como tronco.**
  - `organismo/organismo_v8.py` y `organismo/bateria_v8.py` entran en `CONGELADOS` de `manifiesto.py`.
  - Se crea el tag git **`v8-tronco`**.
  - CLAUDE.md pasa a decir que el tronco es v8. **v6 sigue congelado** como referencia, con su batería.
  - Sigue la fase 4 (3T confirmatorio) **sobre v8**.
- **Si 4a falla:** se para. Se diagnostica el instrumento; no se congela nada.
- **Si falla 1, 2, 3, 4b, 4c o 4d:** v8 **no** se congela. Se registra y se lleva a dirección. No se recalibra
  nada (regla 3).
- **Si falla 5:** no se corre el examen. Se arregla el constructor y se vuelve a empezar desde este preregistro.

## 5. Qué NO prueba

- Nada sobre la política bajo hambre (2P, sigue abierta).
- Nada sobre la recuperación espontánea estructural (A5 corregida, en cola).
- Nada sobre composición temporal: eso es la fase 4.
- Congelar v8 no declara que v8 sea "mejor" en general. Declara que pasa este examen y la prueba de coste.

## 6. Procedencia

El sha de este archivo va en el registro y en el log del examen. `bateria_v8.py` imprime su propio sha y el de
`organismo_v8.py` al arrancar.
