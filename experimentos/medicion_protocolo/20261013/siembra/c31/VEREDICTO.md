# VEREDICTO — entrada del registro

Copiada de `registro/REGISTRO_etapas_1_2.md`, líneas 2073–2135.

---

### ETAPA 4 sobre v9 — CORRIDA. **NO se cierra: v9 sufre OLVIDO CATASTRÓFICO por interferencia**

**Procedencia**
- Preregistro `22fc98250ec40817` (commit `b930c9e`). Instrumentos commiteados antes de correr (`1bdc080`):
  `organismo_v9m.py` `8afa74b805ba2102`.
- Datos: `datos/etapa4_v9_20260916_170519.json` (`6670a87652d0e2a4`) y `.log`.
- Instrumento: `v9m` ≡ v9 21/21; herencia corre 3/3.
- **Humo declarado**, con fases cortas: en una corrida la interferencia ya se veía grande.

**Bloque M — ausencia con interferencia** (A y B fuera en [50k, 100k); se aprenden C veneno y D comida):

| | resultado |
|---|---|
| **M1** control sin aprendizaje en la ausencia | **SOSTENIDA**: `W_A` y `W_B` en 100k idénticos a 50k, 20/20 |
| **M2** recuerda | **REFUTADA**: `W_B` de −2.924 a **−0.344** [−3.80, +2.26], conserva el miedo en **7/20**; `W_A` de +1.000 a +0.572, en 10/20 |
| **M3** la interferencia es medible | **SOSTENIDA**: cambio > 0.01 en 18/20, mediana **3.92** |
| (sin voto) primer reencuentro con B | `pb` mediana **0.60**; **muerde B en 10/20**. Olvido también en la conducta |

**Bloque H — herencia** (cría con semilla 1000 + s):

| mundo | modo | veneno en Q1 | muertes Q1 | muertes Q1+Q2 | muertes totales |
|---|---|---|---|---|---|
| igual | cero | 30.5 | 32.0 | 66.0 | 135.0 |
| igual | parcial | **7.0** | 35.0 | 66.5 | 137.0 |
| igual | completa | **6.5** | 29.5 | 64.5 | 132.5 |
| invertido | cero | 32.0 | 34.5 | 66.5 | 137.5 |
| invertido | parcial | 33.0 | 36.5 | 68.5 | 136.0 |
| invertido | completa | 36.5 | 40.0 | **74.0** | **146.0** |

- **H1 SOSTENIDA:** heredar el valor ahorra ~80% del veneno inicial en un mundo igual (6.5 frente a 30.5, 20/20).
  Lo explica el valor heredado, no las patas: `parcial` también da 7.0.
- **H3 REFUTADA por margen:** muertes en Q1, `completa` < `cero` en **14/20**; se pedían 15.
- **H4 REFUTADA:** en el mundo invertido, `completa` > `cero` en **12/20**. La dirección de las medianas es la
  predicha (74 frente a 66.5 en Q1+Q2, 146 frente a 137.5 en total), pero sin la consistencia exigida.
- **H5 SOSTENIDA:** aun heredando la memoria equivocada, revierte al final en 20/20.

### DIAGNÓSTICO del olvido (sin valor confirmatorio): **dos vías, y las divisiones lo triplican**

**Qué se corrió.** Brazo `sin_plast`: igual que el bloque M con aprendizaje, pero con `plast=False` en toda la
corrida. En E1, v9 no divide nunca, así que la fase 1 no cambia; sólo se quitan las divisiones de la ausencia.
Script en el scratchpad de la sesión, 20 corridas.

| | ΔW_B mediana | ΔW_A mediana | conserva el miedo a B |
|---|---|---|---|
| con plasticidad (bloque M) | **+2.569** | −0.428 | 7/20 |
| sin plasticidad | **+0.837** | 0.000 | 10/20 |

- **corr(|ΔA| + |ΔB|, divisiones durante la ausencia) = +0.87.**
- **Control interno:** en las 6 semillas sin divisiones (4, 6, 10, 12, 17, 19), los dos brazos dan **exactamente el
  mismo** Δ.

**Lectura.**
1. **Interferencia de valor:** D (comida) comparte celdas con B y empuja su valor hacia arriba; C (veneno) comparte
   celdas con A y lo empuja hacia abajo. Como **A y B no están**, nadie lo corrige. Es la deriva sin re-muestreo que
   2I ya había medido ("misma valencia: deriva no corregida"), aquí sin el estímulo presente y durante 50.000 pasos.
2. **Interferencia estructural:** las divisiones provocadas por C y D **reescriben los códigos** de A y B, la vía de
   A5, y **triplican** el olvido.

**Consecuencia.** La memoria de v9 es exacta si no aprende nada, pero **no protege lo aprendido de lo que se aprende
después**. Falta un órgano de **consolidación** (O6, dimensionado por escrito en la exploración de órganos): que lo
consolidado resista la sobrescritura, y que lo nuevo reclute celdas en vez de pisar las de otros.

**La Etapa 4 NO se cierra.** Sostenido: M1, M3, H1, H5. Refutado: M2, H3 (por margen), H4.
