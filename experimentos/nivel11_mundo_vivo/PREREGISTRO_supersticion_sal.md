# PREREGISTRO — LA SUPERSTICIÓN DE LA SAL (bloque aparte, nivel 4)

**Borrador del diseñador para el coordinador**, 18 sep 2026, escrito tras 181–200 y **sin correr nada**.
Bloque independiente del mundo vivo: lo que mide no es el mundo vivo sino **una grieta del tronco v14.1** que el
mundo vivo destapó. Misión: AGI por este camino; el método manda.

---

## 1. El hecho

En el brazo NO_INFORMA (la sal no cambia nada: `ΔE = ΔAg = 0`), 18/20 semillas dan `W[sal] = 0.0` **exacto** en las
dos necesidades. Dos —182 y 188— dan **−1.83** y **−1.34** en la fila de hambre, y 0.0 en la de sed.

## 2. Por qué, con el dato que ya está en el JSON (no hace falta correr nada)

**(a) La sal y el veneno son EL MISMO ESTÍMULO para la vía rápida.** Diagnóstico estructural
(`diagnostico_codigos.py`: construye `KW` y lee los códigos, no simula un paso): las dos semillas con valor son
**exactamente** las dos de 181–200 con `|code(D) ∩ code(B)| = 3`, y `K = 3`, así que **el código de la sal es el
código del veneno**. Ninguna otra semilla del rango tiene 3.

**(b) El valor es literalmente el mismo número.** En 182, `W_hambre[veneno] = W_hambre[sal] = −1.83`; en 188,
`−1.34` las dos. No es parecido: es la misma celda leída dos veces.

**(c) Y el precio lo paga el veneno.** En las otras 18 semillas `W[veneno] = −3.00`. En las dos con alias cae a
**−1.83 / −1.34**: la sal muda, que no informa de nada, **le quita al organismo entre el 40 % y el 55 % del miedo a
lo que sí lo mata**. La "superstición" no es una creencia sobre la sal: es el miedo al veneno derramándose sobre una
imagen indistinguible, y la factura la paga el veneno.

**(d) La puerta le presta la evidencia.** `_fam` consulta `ncod[frozenset(code)]`, mordidas **por código**. Con el
mismo código, las ~2 000 mordidas de veneno cuentan como evidencia de la sal: la puerta la declara familiar y la
boca lee la vía rápida, es decir, la celda del veneno.

**(e) El órgano que debería separarlos no puede dispararse.** La división por conflicto de signo exige
`Wb[c]*R < 0`. Con la sal muda **`R = 0`** y el producto es `0`, no negativo: **`div_signo` es ciego a "este estímulo
no informa"**. La prueba está dentro del mismo dato: en esas dos semillas, con la sal MUDA hay **0 divisiones**; con
la sal informativa (brazo VIVO, misma semilla, mismos códigos) hay **2 y 1**.

**(f) Y la evitación impide la desconfirmación.** El valor prestado es negativo, la boca rechaza, y lo rechazado no
desaparece del anillo: las exposiciones a la sal saltan de ~500 a **4075 y 3988** (×8). Cada encuentro vuelve a leer
el mismo valor prestado y casi ninguno lo corrige, porque corregirlo exige morder. **El bucle se cierra solo**: es la
superstición mantenida por evitación, y aquí está medida.

**Las tres hipótesis que se me pidió considerar quedan refutadas con este mismo dato:** *co-ocurrencia con la
necesidad activa* — el valor aparece **sólo** en la fila de hambre, que es donde vive el veneno, y `W_sed[sal] = 0.0`
en las dos semillas; si fuera co-ocurrencia con el estado, no elegiría la fila del veneno. *Sorpresa específica* —
`eta_pred = 0` en todos los brazos del bloque: el predictor está inerte, refutada por construcción. *Drenaje* —
`lam` resta la parte **común** de `Wp`/`Wn` y empuja hacia 0, no lo contrario, y sólo actúa cuando la celda se
actualiza, es decir cuando la sal se muerde: el drenaje no causa el bucle, **su ausencia es parte de él**.

## 3. Hipótesis y mecanismo mínimo

**H:** el valor espurio de un estímulo que no informa aparece **si y sólo si** su código coincide con el de un
estímulo con valor consolidado, y se sostiene porque (i) la puerta presta evidencia por código, (ii) la división por
conflicto de signo no se dispara con `R = 0` y (iii) la evitación corta el muestreo que lo corregiría.
**Alcance:** no es del mundo vivo. Con dos estímulos (v14) la condición `code(A) ∩ code(B) = 0` está **impuesta** por
`cond()` en el arranque; el mundo vivo es el primer mundo del proyecto con **cuatro** estímulos y ningún alias
prohibido. El tronco nunca fue puesto a prueba en esto.

## 4. Brazos (semillas **seleccionadas por el diagnóstico estructural, antes de correr**)

| brazo | semillas | qué cambia |
|---|---|---|
| **S1-ALIAS** | 326, 334, 343, 377, 446, 533, 549, 563, 670 (las 9 con `\|D∩B\| = 3` de 301–700) | ninguna: NO_INFORMA tal cual |
| **S1-LIMPIA** | 307, 313, 316, 323, 325, 327, 333, 338, 342 (las 9 primeras con `\|D∩B\| = 0`) | ninguna: NO_INFORMA tal cual |
| **S2-SIN-SED** | las 9 ALIAS | `n_nec = 1`: no existe la sed. Si la superstición fuera co-ocurrencia con la necesidad activa, **debe desaparecer** |
| **S3-PUERTA** | las 9 ALIAS | `puerta_pat = 0` (puerta de v13, por celdas consolidadas, sin evidencia por código): aísla (d) |
| *(no construido)* **S4-DIV0** | — | división por conflicto de **información**: disparar también cuando una celda consolidada (`\|Wb[c]\| > 0.2`) recibe `R = 0` repetidas veces. Es el arreglo candidato; se construye sólo si S1 confirma |

Un proceso por tarea, `T = 100000`, mismos brazos y medidas del mundo vivo (`corre_vivo.py --brazos NO_INFORMA,V14`
más las dos perillas): no hace falta instrumento nuevo, sólo un selector de semillas.

## 5. Predicciones numéricas y refutación

| # | predicción | refutación |
|---|---|---|
| **S-1** | **S1-ALIAS**: `\|W[sal]\| > 0.3` en ≥ 8/9 semillas (mediana ≥ 1.0). **S1-LIMPIA**: `\|W[sal]\| ≤ 0.3` en **9/9** (mediana 0.0) | si las LIMPIAS también dan valor, la causa **no** es el código y toda §2 está mal |
| **S-2** | el veneno paga: `W[veneno] ≥ −2.3` (menos miedo) en ≥ 8/9 ALIAS y `≤ −2.8` en 9/9 LIMPIAS | si el veneno no se degrada, el valor espurio no viene de su celda |
| **S-3** | evitación: exposiciones a la sal ≥ **3 ×** la mediana de las LIMPIAS, en ≥ 8/9 ALIAS | si no se acumula, el bucle de evitación no existe y (f) cae |
| **S-4** | divisiones = **0** en ≥ 8/9 ALIAS con la sal muda | si divide, `div_signo` sí ve la información ausente y (e) cae |
| **S-5** | **S2-SIN-SED ≈ S1-ALIAS**: `\|W[sal]\|` dentro de ±0.3 de S1-ALIAS, en ≥ 7/9 | si al quitar la sed la superstición desaparece, **la explicación del coordinador gana y la mía cae** |
| **S-6** | **S3-PUERTA**: `\|W[sal]\|` baja al menos 50 % respecto de S1-ALIAS en ≥ 7/9 (la puerta de v13 no presta evidencia por código, pero el código sigue siendo el mismo, así que **no** se predice 0) | si no baja, la puerta no es parte del bucle: sólo el alias |

**Coste de no arreglarlo, ya medido y por eso no hay prisa:** 2 semillas de 20 (10 %), y 0 de 20 en 201–220. **Pero
escala con el número de estímulos**: con 4 patrones sobre 6 píxeles y `K = 3` de 30 celdas, la frecuencia de alias
medida sobre 480 semillas (181–200, 201–260, 301–700) es **12/480 = 2.5 %**; con más estímulos crece como el número
de pares. Es una grieta de **capacidad**
(nivel 4), no del mundo vivo.

## 6. Las cuatro trampas

1. *Canal simétrico* — n/a; aquí no hay canal. 2. *Acierto sin balancear* — no se usa acierto: se comparan valores y
conteos, y los dos grupos tienen n = 9. 3. *El mundo que se come la comida* — **es la variable dependiente** (S-3):
se reporta cruda y por estímulo. 4. *Sitios fijos* — `spawn()` sortea; y la selección de semillas es por una
propiedad del **código**, calculada antes de correr, no por un resultado.
**Trampa propia declarada:** seleccionar semillas por una propiedad medida **después** sería circular. No lo es aquí
porque `|code(D) ∩ code(B)|` se calcula sin simular un paso y las semillas son de un rango virgen (301–700).
