# Prueba de COSTE del arreglo de BUG-01 con el techo MORDIENDO contra el objetivo

**Escrito ANTES de construir los instrumentos y ANTES de correr nada. 16 sep 2026, día 4.**

- **Dirección:** Christiam Puentes. Es el paso 1 del orden fijado al cierre del día 3 ("preregistro de una prueba
  de coste en régimen de saturación"). El 16 sep indicó seguir adelante siguiendo los `.md`.
- **Ejecución:** en el repo.
- **Organismo candidato:** v7e con `lam=0.05` y `piso=0`.
- **Control:** el mismo archivo con `lam=0`.

> Nota de nombre: una copia externa del repo contiene un `PREREGISTRO_coste_saturacion.md` que **no** es este y
> no tiene validez (`registro/AUDITORIA_copia_antigravity_20260916.md`). Por eso este archivo se llama distinto.

---

## 0. Qué se sabía antes de escribir esto (se declara todo)

1. **Demostración de ERR-11.** `dlt = R − W` depende sólo de `W`. Con `aversion=1`, las dos ramas del
   aprendizaje dan `W += eta·dlt·kc`, y el drenaje resta lo mismo a los dos canales.
   - Por tanto, **mientras ningún clip trunque una actualización, la trayectoria de `W` es idéntica para todo
     `lam`**. La política sólo lee `W`, así que la conducta también es idéntica.
   - Además el drenaje sólo resta, y los incrementos son los mismos en los dos brazos. Por eso los canales del
     control son siempre **≥** los del arreglo, celda a celda, y **el control trunca primero**.
   - **Consecuencia: el primer instante posible de divergencia entre brazos es la primera truncación del clip
     en el control.** No hay otro.
2. **Datos ya guardados, leídos hoy** (registro, día 4). En `bug01_exp2_20260915_183244.json`:
   - En E1, E2, E2I, E2J, E2K y E2L, el control **nunca** llega a 9.0 por código, y el arreglo sale idéntico en
     `W`, muertes y mordidas.
   - Sólo satura el escenario BUG (`plast=False, solap_AB=3`).
3. **Hipótesis externas vistas ANTES de escribir.** Origen: copia externa trabajada por Antigravity. **No
   reproducidas.**
   - **H-ext-1:** en el diseño 2K-bis con plasticidad, `lam=0.05` baja W=0 exacto de 328/400 a 0/400, baja el
     agotamiento de 20/20 a 5/20 y deja N* igual en 19/20.
   - **H-ext-2:** con R canónicas y una inversión, `Wn` llega a 9.00 por código con `W=−3.00` y los brazos no se
     distinguen.
   - Las predicciones de §5 marcadas **[ext]** **no son independientes** de esas cifras: son su reproducción
     (regla de cruce, paso 2). Las no marcadas se derivan de §0.1 y §4.1.
4. **Tocar el techo no es morderlo** (H-ext-2). Un canal puede llegar a 3.0 por celda sin que ninguna
   actualización se trunque, si el objetivo se alcanza justo ahí. Por eso el primitivo es la **truncación**, no
   el valor del canal.

## 1. La pregunta

- **Objeción de dirección (15 sep):** *el arreglo compra rango dinámico vendiendo memoria latente.*
- **Qué dejó ERR-11:** el coste, si existe, sólo puede vivir donde el clip trunca. La prueba de ahorro del día 3
  no llegó a ese régimen.
- **Pregunta principal:** con el techo mordiendo contra el objetivo, **¿el arreglo cuesta conducta?**
- **Pregunta secundaria:** en el diseño de capacidad 2K-bis, **¿qué compra y qué no?**

## 2. El primitivo: MORDIDA DEL TECHO

En cada mordida con aprendizaje, **después** del drenaje y **antes** del clip, sobre las celdas activas del código:

```
dlt > 0 :  mordida del techo  <=>  any( Wp[c] + eta*dlt           > 3.0 )
dlt <= 0:  mordida del techo  <=>  any( Wn[c] + eta*aversion*(-dlt) > 3.0 )
```

Se registra:
- `t_techo`: primer paso en que ocurre;
- `techo_primero`: con qué estímulo, en qué canal y en qué fase;
- `n_techo`: cuántas veces ocurre.

Es instrumentación de **sólo lectura**: no toca el RNG ni el estado.

## 3. Instrumentos

Los genera `construye_coste_techo.py` por parcheo con anclas, igual que `construye_ahorro.py`: cada ancla aparece
exactamente una vez o el script aborta.

| archivo | se deriva de | añade |
|---|---|---|
| `organismo_v7h.py` | `experimentos/bug01/organismo_v7e.py` (`3118c6d563542da2`) | `invertir_cada` (inversión A↔B cada N pasos), contadores por fase, primitivo §2 |
| `organismo_caph.py` | `experimentos/ramas/2Kbis_capacidad/organismo_cap.py` (`dc058e0a43216bf3`) | parámetro `lam` con la línea de drenaje **literal** de v7e, primitivo §2, contadores de mordidas de veneno y de comida |

**Ningún otro cambio.** Sin `invertir_cada`, `organismo_v7h` es v7e. Con `lam=0`, `organismo_caph` es `organismo_cap`.

## 4. Bloque S — inversiones seriadas: el ahorro con el techo mordiendo

**Diseño**
- Al empezar, A es comida y B veneno. `invertir_cada=50.000`, `T=350.000`: **7 fases**. En las fases impares A
  es comida y B veneno; en las pares, al revés.
- Solapamiento A∩B = 0, el de siempre, sin forzar nada.
- **Brazos:** `plast ∈ {False, True}` × `lam ∈ {0, 0.05}`, semillas 1..20: **80 corridas**.

**Métricas por fase `p` y por estímulo `X`:**
- mordidas, visitas, mordidas mientras X es veneno y mientras es comida;
- muertes en la fase;
- `W_X` al final de la fase;
- **`n_p(X)`**: mordidas de X desde el inicio de la fase hasta cumplir el criterio (veneno: `W_X ≤ −2.5`; comida:
  `W_X ≥ +0.5`), comprobado tras la actualización de cada mordida. Si no llega, **censurada** y se cuenta aparte.
  **No se tocan los criterios** (regla 3).

### 4.1 Derivación, escrita antes de correr (`plast=False`)

Supuestos:
- Sin plasticidad y con A∩B=0, cada mordida de X mueve `W_X` en `0.09·dlt` (RW puro).
- Cada una de las 3 celdas absorbe un tercio de ese movimiento, **en su propio canal**: `Wp` si sube, `Wn` si baja.
- En el control los canales **sólo crecen**.
- Se supone convergencia completa en cada fase: 50.000 pasos alcanzan, según E2, donde `W_B → +1.00` y
  `W_A → −2.97`.

Canal por celda al terminar cada fase:

| fase | B (valencia) | Wp_B | Wn_B | A (valencia) | Wp_A | Wn_A |
|---|---|---|---|---|---|---|
| 1 | veneno (0→−3) | 0 | 1 | comida (0→+1) | 1/3 | 0 |
| 2 | comida (−3→+1) | 4/3 | 1 | veneno (+1→−3) | 1/3 | 4/3 |
| 3 | veneno | 4/3 | 7/3 | comida | 5/3 | 4/3 |
| 4 | comida | **8/3** | 7/3 | veneno | 5/3 | **8/3** |
| 5 | veneno: pide `Wn=11/3` | 8/3 | **3 (trunca)** | comida: `Wp → 3` por debajo | →3 | 8/3 |
| 6 | comida: pide `Wp=10/3` | **3 (trunca)** | 3 | veneno: pide `Wn=4` | ≈3 | **3 (trunca)** |
| 7 | veneno | 3 | 3 | comida | 3 | 3 |

Consecuencias:

- **En las fases 1–4 no puede haber truncación.** El movimiento máximo de `W` en una fase es 4, así que por
  celda `Wp ≤ 8/3` y `Wn ≤ 8/3`. La cota es **exacta**: no depende de que la convergencia sea completa.
- **B trunca en la fase 5** cuando `W_B = 1 − 3·(3 − 7/3) = −1.0`, y **se congela**: siendo veneno, no hay
  `dlt>0` que lo mueva.
  - Con convergencias incompletas (`w1 = w3 = −2.8`), trunca en `W_B = −1.4`.
  - Se predice que se congela en **[−1.5, −0.7]**.
- **A no trunca en la fase 5**, porque se acerca a `Wp=3` desde abajo. **Trunca en la fase 6** con `W_A ≈ 0`.
- **Fase 6:** B (comida) trunca `Wp` en `W_B = 0`. **Fase 7:** los dos quedan congelados en `W≈0`, con canales
  (9, 9) por código.
  > **Predicción derivada: BUG-01 aparece SIN solapamiento espacial, sólo por conflicto temporal, en la séptima
  > fase.**
- **El arreglo no trunca nunca.** Drena el 5% de la parte común en cada mordida, y la parte común se vacía en
  cientos de mordidas por fase.
- **Mordidas hasta criterio** en RW puro, con distancia 0.5 al objetivo:
  `k = ceil( ln(0.5/|R − W0|) / ln 0.91 )`.
  - B veneno desde 0: **19**.
  - B veneno desde +1: **23** (desde cualquier `W0 ∈ [+0.5, +1]`: **21–23**).
  - A comida desde −3: **23**.

### 4.2 Predicciones del bloque S

- **S0 [exacta; decide si se lee todo lo demás].** Para cada `(semilla, plast)`, **todas** las métricas de las
  fases cuyo último paso es `< t_techo(control)` son **idénticas** entre `lam=0` y `lam=0.05`: conteos exactos y
  `W` a 2 decimales. Si el control no trunca, la corrida entera es idéntica. **Se refuta con una sola diferencia.**
- **S1** (`plast=False`, `lam=0`):
  - **(a)** cero truncaciones en las fases 1–4, **20/20** (cota exacta de §4.1);
  - **(b)** la primera truncación de la corrida es de B, en la fase 5, en **≥15/20**;
  - **(c)** la mediana de `W_B` al final de la fase 5 cae en **[−1.5, −0.7]**;
  - **(d)** al terminar (`T`), `|W_A| ≤ 0.3` **y** `|W_B| ≤ 0.3` en **≥15/20**. Es BUG-01 por conflicto temporal.
- **S2** (`plast=False`, `lam=0.05`):
  - cero truncaciones en **20/20**;
  - al terminar, `|W_A − 1| < 0.15` **y** `|W_B + 3| < 0.3` en **≥15/20**.
- **S3 — la pregunta de dirección, el ahorro con el techo** (`plast=False`):
  - arreglo: `n_1(B) = 19` en **20/20**, y `n_3(B)`, `n_5(B)`, `n_7(B)` ∈ **[21, 23]** en **≥15/20** cada una.
    Es decir, **ahorro 0 y coste 0 en todos los ciclos**;
  - control: `n_3(B)` idéntica a la del arreglo (S0), y `n_5(B)` **censurada** en **≥15/20**.
  - **Lectura fijada ahora:** si S3 se sostiene, lo que el control guarda en los canales al llegar al techo **no
    es memoria latente que ahorre**: es **incapacidad de reaprender**.
- **`plast=True`:** sólo se vota S0. Lo demás se reporta sin voto, porque las divisiones cambian los códigos y la
  derivación de §4.1 no aplica (lección de A5).

## 5. Bloque C — capacidad (2K-bis) con el techo mordiendo

**Diseño.** Es **exactamente** la Parte 2 de 2K-bis: 20 patrones de peso 3, el mismo orden, valencias alternas,
checkpoints y `techo()` con TOL=0.3. Se **importa** de `parte2_capacidad.py` (`ef471cd7c97cc822`) sin modificarlo.

| condición | plast | paso_t | lam | semillas |
|---|---|---|---|---|
| principal | True | 20.000 | 0 y 0.05 | 1..20 |
| control de muestreo de 2K-bis | True | 60.000 | 0 y 0.05 | 1..20 |
| referencia sin plasticidad | False | 20.000 | 0 y 0.05 | 1..20 |

**120 corridas.** `M_max` = máximo de estímulos simultáneamente con `|W−R| ≤ 0.3`, la métrica compañera de
`parte2g_techo_estricto.py`.

**Predicciones**
- **C0 [exacta].** Todo checkpoint con `t ≤ t_techo(control)` es **idéntico** entre `lam=0` y `lam=0.05`: `W` a 3
  decimales, celdas, splits, `mord_ac` y `vis_ac`. Aplica a todas las condiciones. **Se refuta con una diferencia.**
- **C1 [derivada, afilada].** Sea `n0 = min(N*_control, N*_arreglo)`. **En toda corrida en que N* difiera entre
  brazos, `t_techo(control) < t` del checkpoint `n0+1`.** Si ese checkpoint cae antes de la primera truncación,
  los dos brazos son idénticos ahí y fallan juntos. **Se refuta con una sola corrida** en que N* difiera y la
  truncación sea posterior.
- **C2 [ext]** (principal). N* igual entre brazos en **≥18/20**.
- **C3 [ext]** (principal). Valores finales `W` con `|W| < 0.0005`, sobre 400 (20 estímulos × 20 semillas):
  control **≥70%**; arreglo **≤5%**.
- **C4 [ext]** (principal). Agotamiento de las 90 celdas: control **≥18/20**; arreglo **≤10/20**.
- **C5** (principal, direccional). `M_max(arreglo) ≥ M_max(control)` en **≥15/20**. Los empates cuentan como ≥.

## 6. Criterio de COSTE — el que decide

La comparación es **pareada por semilla**. Es legítimo porque S0 y C0 hacen idénticas las dos corridas de una
semilla hasta la primera truncación.

**Métricas con voto**, en las tres condiciones principales (S con `plast=False`, S con `plast=True`, y C principal):
- **M1** = muertes totales.
- **M2** = mordidas de veneno totales: mordidas de cualquier estímulo mientras su valencia es veneno.

```
COSTE(M)  <=>  arreglo > control en >= 15/20 semillas   Y   mediana(arreglo − control) > 0
```

- **Predicción: COSTE es FALSO para M1 y M2 en las tres condiciones principales.**

**Condición de validez, añadida al releer el criterio antes de correr.** La pregunta fue qué escenario lo haría
pasar por la razón equivocada.
- **El agujero:** si el control no trunca, los dos brazos son idénticos por construcción. Todas las diferencias
  valen 0 y "COSTE falso" saldría **sin haber medido nada**. Es el patrón de ERR-11.
- **La regla:** una condición principal sólo vota si **el control trunca en ≥15/20 semillas** (`t_techo` no nulo).
  Si no, esa condición se declara **NULA**, no aprobada, y la prueba de coste **no pasa** mientras haya una
  condición principal nula.
- **M3** = mordidas de comida totales. Se reporta sin voto.
- Las condiciones no principales (C con `paso_t=60.000`, C con `plast=False`) se reportan sin voto.

## 7. Qué se decide con esto

- **Si S0 o C0 se refutan:** **se para**. No se lee nada más. Hay una vía de divergencia sin truncación que la
  demostración no conoce, y eso pasa por delante de todo.
- **Si COSTE es verdadero** en alguna condición principal: el arreglo **no** se congela por defecto y se lleva a
  dirección con las cifras.
- **Si alguna condición principal es NULA** (§6, el control trunca en menos de 15/20): la prueba **no pasa** y
  se rediseña esa condición con un preregistro nuevo. Nada de alargar T ni de cambiar R a posteriori (regla 3).
- **Si COSTE es falso en las tres y ninguna es nula:** el arreglo **pasa la prueba de coste**. Siguen el paso 2 (batería completa
  con el arreglo) y el paso 3 (examen de congelación con `err > 0.6`, guardando `err_max` por corrida).
- **S1–S3 y C1–C5 no deciden la congelación.** Sostienen o corrigen afirmaciones registradas.
  - Si C2 y C3 se sostienen, hay que **corregir** la cita de 2K-bis *"el límite … está en el rango dinámico de
    los canales"*: el rango explica el colapso de los valores a 0, **no** el techo N*.
- **v6 sigue siendo el tronco** hasta que un candidato pase todo.

## 8. Controles obligatorios

1. **Inercia de los instrumentos.** Si falla uno solo, no se corre nada más.
   - **(a)** `v7h(lam=0, invertir_cada=None)` ≡ `organismo/organismo_v7.py` (`3db0475ef0ea95ce`) en los 7 escenarios
     de `corre_ahorro.py` (BUG, E1, E2, E2I, E2J, E2K, E2L) × semillas 1..6, en las claves comunes.
   - **(b)** `v7h(lam=0.05, invertir_cada=None)` ≡ `v7e(lam=0.05)` en los mismos 7×6.
   - **(c)** `caph(lam=0)` ≡ `organismo_cap` en los 3 escenarios de `equivalencia_cap.py` × semillas 1..6 ×
     `plast ∈ {False, True}`, más el plan 2K-bis corto (6 estímulos, `paso_t=20.000`) × semillas 1..3 × los dos
     `plast`, en todas las claves comunes, incluida `hist`.
2. **Regresión.** `bateria.py 6` PASA y `manifiesto.py --check` con los 4 congelados intactos, **antes** (hecho hoy,
   13:59, 6/6) y **después**.
3. **Regla 11.** Antes de lanzar, ningún proceso Python ajeno al repo. Se comprueba y queda en el log.
4. **Regla 10.** Log con marca de tiempo desde el arranque, etapas `ETAPA k/5`.

## 9. Qué NO prueba

- Nada sobre la política bajo hambre (2P).
- Nada sobre la recuperación espontánea estructural: la predicción corregida de A5 sigue en cola.
- Sólo `lam=0.05`. λ_c es un interruptor por decisión de dirección y **no se barre**.
- No congela nada.

## 10. Procedencia

El sha de este archivo va en el registro **antes** de construir los instrumentos, y en el `meta` del JSON de
salida. Las predicciones [ext] quedan declaradas en §0.3.
