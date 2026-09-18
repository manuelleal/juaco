# Bloque 2 ter (nivel 8 propio): **escala del recuerdo** contra el canje exploración/explotación del mapa

**Escrito ANTES de construir el instrumento y ANTES de correr. 17 sep 2026, 22:50 (día 6; sigue al bloque 2 bis, refutado
en dos dosis).** Regla 12. **Éste es el ÚLTIMO candidato del canje**: la cláusula de refutación del §3 lo dice y se cumple.

## 0. Qué se sabe (datos, no impresiones)

Mundo largo (`experimentos/nivel8_mundo_largo/`: 50 patrones, uno cada 4 000 pasos en 8 sitios fijos, `r_vis = 3`,
inversión de regla en t = 100 000, T = 200 000).

| serie | brazo | adq (≤ 30 vistos) | comida Q4 | equidad de visitas |
|---|---|---|---|---|
| `largo_s1-20` / `s21-40` | V13 / MAPA | 0.88–0.90 / 0.70 | 837 / 968 | — |
| `curiosidad_s41-60` | MAPA + curiosidad por progreso | **0.700** = MAPA = barajada | 974 | — |
| `novedad_s61-80` | MAPA + novedad de sitio 0.6 | **0.800** | 946 | 0.292 (MAPA 0.120; V13 0.615) |
| `novedad_alta_s81-100` | MAPA + novedad de sitio 1.8 | **0.841** | 918 (MAPA 971) | 0.455 (MAPA 0.139; V13 0.710) |

Dos candidatos refutados, **los dos por añadir una atracción**. La lectura que el coordinador escribió al cerrar la línea
de novedad de sitio, y que este bloque pone a prueba, es de **escala**:

> en `_sesgo_M` el valor recordado de un sitio entra **sin recortar**; `R_VAL['veneno'] = −3` contra `R_VAL['comida'] = +1`,
> así que un sitio que alguna vez fue veneno **repele tres veces más** de lo que atrae un sitio de comida, y ninguna
> atracción de +0.6…+1.8 compensa eso. El mapa **aleja** de todo sitio que alguna vez fue veneno; y el patrón nuevo entra
> cada 4 000 pasos en el sitio que lleva más tiempo sin renovarse (`_ren`, ronda por los 8), es decir **justo donde el
> organismo dejó de ir**. Peor: `M` sólo se reescribe al **pisar** el sitio, así que el recuerdo de veneno de un sitio no
> visitado **no puede** corregirse — la evitación se sostiene a sí misma.

Números del instrumento que fijan la escala: `R_VAL = {comida: +1.0, veneno: −3.0}`, `gamma_M = 0.6`, `disc_M = 0.9`,
`H_M = 20`. Sesgo del sitio adyacente (h = 1): comida `+0.6·0.9·1 = +0.54`; veneno `+0.6·0.9·(−3) = −1.62`. El ruido de
decisión es `rng.normal(0, .3, 2)`: **1.62 es un muro, 0.54 es una sugerencia**.

## 1. Órgano candidato: **valor recordado saturado** (opción (a))

**Un solo cambio, en un solo sitio, y es de escala:** en `_sesgo_M` el valor de cada sitio recordado entra **recortado**
a `[−sat_M, +sat_M]`.

```
v'(p) = clip(valor(M[p]), −sat_M, +sat_M)          # antes: valor(M[p]) sin recortar
u += gamma_M · [Σ_h disc_M^h·v'(pos−h),  Σ_h disc_M^h·v'(pos+h)]
```

- **No añade ninguna atracción nueva.** No hay término nuevo en `u`, no hay reloj, no hay cantidad nueva por sitio, no hay
  RNG nuevo en el brazo tratado. El mapa sigue apuntando a la comida recordada exactamente como antes (el valor de una
  comida es `+1 ≤ sat_M`: **no se toca**). Lo único que cambia es que **el recuerdo de veneno deja de pesar tres comidas**.
- **Por qué (a) y no (b) (olvido del veneno recordado), en una línea:** el decaimiento `tau_M` borra también el recuerdo de
  comida —con el que el mapa da de comer— y su reloj *es* el `t − t_visita` de la novedad de sitio ya refutada, así que un
  resultado positivo no sería atribuible a la escala sino al mismo tiempo-sin-visitar que ya cayó dos veces.
- **No toca** la boca (morder se sigue decidiendo con `valor()` completo, con el −3 intacto), ni el aprendizaje, ni la
  escritura de `M`, ni las celdas, ni el RNG del organismo, ni `valor()` fuera de `_sesgo_M`. **El −3 sólo se recorta en la
  brújula, nunca en la decisión de comer.**
- Con `sat_M = None`, `kappa_M = 1.0`, `sat_barajada = False` es `mundo_largo` **bit a bit** (identidad obligatoria, 3
  semillas, mundo completo con mapa, todas las claves del original; única clave extra `esc_diag`, diagnóstico).

**Constantes, fijadas aquí y no tocadas después (escala del mundo, no calibración):**

| constante | valor | justificación *a priori* |
|---|---|---|
| `sat_M` | **1.0** | `= R_VAL['comida']`. Es la unidad de valor que el mundo define: **un sitio recordado no puede pesar en la brújula más de lo que vale una comida**. El factor que se elimina es exactamente `\|R_VAL['veneno']\| / R_VAL['comida'] = 3`, la asimetría que la lectura del §0 acusa. No hay ningún grado de libertad que ajustar: cualquier otro valor sería un número inventado. |
| `kappa_M` | **0.5** (sólo en el brazo de lectura `MAPA_ATEN`) | Atenuación uniforme que **iguala la magnitud media** del brazo tratado: con 25/25 en el pool y 4+4 en los sitios iniciales, `E\|valor\| = (1+3)/2 = 2` sin recortar y `= 1` recortado, luego `kappa_M = 1/2`. Sale de la composición del mundo, no de los datos. |

**Perilla que NO existe y no se va a crear:** no hay dosis de `sat_M` (no es una ganancia, es un tope) y no habrá una
segunda. Precedente explícito: la novedad de sitio consumió dos series por tener una dosis suelta (`gamma_N` 0.6 → 1.8).

## 2. Brazos (mundo largo completo, semillas **81–100**, T = 200 000)

**De criterio:**

| brazo | perillas | qué es |
|---|---|---|
| `V13` | `usa_M=False` | el tronco, techo de adquisición |
| `MAPA` | `usa_M=True` (`gamma_M=0.6`) | el canje medido |
| **`MAPA_SAT`** | `+ sat_M=1.0` | **el órgano** |
| `MAPA_SAT_BAR` | `+ sat_M=1.0, sat_barajada=True` | **control 1 (atribución)**: el **recorte** que le tocaría a cada sitio se aplica en **otro** sitio. Permutación fija de las 8 posiciones de sitio por semilla, RNG propio `seed + 950000`. Formalmente: `d(p) = max(0, \|v(p)\| − sat_M)` es lo que el tratamiento quita en `p`; el control usa `v''(p) = sign(v(p))·max(0, \|v(p)\| − d(perm(p)))`. **Se quita exactamente el mismo presupuesto total de magnitud** (una permutación sólo reordena el mismo multiconjunto de recortes) **en los sitios equivocados**. |

**De lectura (no deciden el veredicto; se pueden quitar si el coordinador necesita CPU):**

| brazo | perillas | qué separa |
|---|---|---|
| `MAPA_ATEN` | `kappa_M=0.5` (sin recorte) | **control 2 (escala vs. cantidad)**: mismo **tamaño medio** de sesgo que `MAPA_SAT`, pero **con la asimetría 3:1 intacta**. Separa *"quitar el muro del veneno"* de *"poner menos mapa"*. Si `MAPA_ATEN` explora igual, el hallazgo sería "*media dosis de mapa*", no la escala del recuerdo. |

**Por qué la permutación se aplica sólo sobre las 8 posiciones de sitio** (lección del auditor incorporada en el bloque 2 bis
y mantenida aquí): `M` **sólo se escribe al pisar una posición con objeto**, y los objetos sólo viven en `_SIT`; permutar
sobre las 40 posiciones del anillo mandaría la mayor parte de los recortes a posiciones con `_Mset = False`, que nunca entran
en el sesgo: **diluiría el control**. Nota honesta y conservadora: una permutación de 8 deja ~1 punto fijo de media (un sitio
que se recorta a sí mismo), lo que hace el control **más parecido** al brazo tratado, es decir dificulta P3, no lo facilita.

**Medidas:** las del mundo largo (adquisición ≤ 30 vistos y final, retención de los nunca invertidos, comida Q4, muertes,
recuperación tras la inversión, celdas, `M_llenas`), más las dos lecturas del mecanismo ya usadas en el bloque 2 bis:
**equilibrio de visitas** entre los 8 sitios (mín/máx y entropía normalizada, desde `esc_diag`) y **sesgo de signo**
(fracción de los 50 patrones con `W > 0` al final; debe rondar 0.5).

**K0 — puerta de validez del instrumento (escrita antes de correr, con datos ya publicados).** Las semillas 81–100 ya tienen
los brazos de referencia medidos en `novedad_alta_s81-100_20260917_221523`: **V13 adq 0.887 · MAPA adq 0.700 · MAPA comida Q4
971**. Con las perillas apagadas este instrumento es `mundo_largo` bit a bit, así que esos tres números deben **reproducirse
exactamente**. Si no, el instrumento está roto y el bloque no se lee (regla 5: la primera hipótesis es el instrumento). Es una
puerta, no un criterio: no puede "pasar por poco" ni recalibrarse.

## 3. Criterios y predicción numérica (medianas de 20 semillas; pareado = misma semilla)

- **P1 (recupera la exploración):** `MAPA_SAT` adquisición (≤ 30 vistos) mediana ≥ **0.85** **y** > `MAPA` pareado en **≥ 15/20**.
- **P2 (no pierde la comida):** `MAPA_SAT` comida Q4 ≥ **0.9 × `MAPA`** pareado en **≥ 15/20**.
- **P3 (el recorte está bien atribuido):** `MAPA_SAT` > `MAPA_SAT_BAR` en adquisición pareado **≥ 15/20**, **y** el control
  **no** supera a `MAPA` en ≥ 15/20, **y** su mediana **no** llega a 0.85.
- **P4 (no es sólo menos mapa; lectura):** `MAPA_SAT` > `MAPA_ATEN` pareado ≥ 15/20 **y** `MAPA_ATEN` no llega a 0.85.
- **Empates (ERR-17, escrito antes de ver datos):** la adquisición está cuantizada en pasos de 0.1; el criterio pareado es con
  `>` **estricto** y se reportan siempre `gana/empata/pierde`. Si un criterio pareado se queda por debajo de 15 **con empates**,
  se aplica el desempate **ya preregistrado aquí y sólo éste**: `gana ≥ 0.75 × (gana + pierde)` con `gana + pierde ≥ 8`; se
  declara "pasa por desempate" y se registra así. Nada más se recalibra. (Es el mismo desempate del bloque 2 bis, literal.)

**Predicción numérica (antes de correr):**

| cantidad | predicción |
|---|---|
| `MAPA_SAT` adq (≤ 30) | **0.875** (intervalo previsto 0.85–0.90), > `MAPA` en **17/20** |
| `MAPA_SAT` comida Q4 | **≈ 945** (≈ 0.97 × 971), P2 en **17/20** |
| `MAPA_SAT` equidad de visitas | **0.50 ± 0.10** (MAPA 0.139, V13 0.710 en estas mismas semillas) |
| `MAPA_SAT` muertes | ≤ 1.5 × `MAPA` |
| `MAPA_SAT_BAR` adq | **≈ 0.72** (entre MAPA y SAT, más cerca de MAPA) |
| `MAPA_ATEN` adq | **≈ 0.78** (sube algo: menos mapa; pero el muro sigue siendo 3× la atracción) |

**Si P1+P2+P3 pasan:** *"recortar el valor recordado a una comida devuelve la exploración al organismo con mapa sin cobrarle
la comida"*; se habilita el bloque 4 (v14 = v13 + mapa + saturación) con examen v3', `bateria_generaliza.py` y regresión.
Vocabulario permitido: *"deja de huir de los sitios donde una vez hubo veneno y por eso encuentra lo nuevo"*. **No**
"pierde el miedo" (la boca conserva el −3 entero), **no** "explora a propósito".

**Refutación explícita (cualquiera de las dos):**

- **(a) P1 falla** → **el canje se registra como ESTRUCTURAL**: *el mapa cobra exploración por construcción y v14 no lo lleva.*
  Con tres mecanismos independientes refutados (atracción por progreso, atracción por novedad, **y ahora la escala misma del
  recuerdo**), la conclusión que se escribe es que **una memoria de sitios que guía el cuerpo reduce la adquisición de lo
  nuevo en este mundo, y no por una constante mal puesta**: cualquier cosa que conserve el recuerdo útil (dar de comer)
  conserva la evitación que ciega. **No se prueba una cuarta perilla, ni otra dosis, ni otra atracción**; el mapa se queda
  fuera del tronco y el nivel 8 sigue con v13. La ruta que quedaría abierta no es una perilla sino un cambio de premisa
  (p. ej. que `M` se pueda reescribir **sin pisar**, es decir vista a distancia), y eso es otro mundo y otro preregistro.
- **(b) P1 pasa pero P3 falla** → el efecto es **"menos mapa"**, no la escala del recuerdo; se registra con ese nombre y el
  órgano **no** entra al tronco. Si además P4 falla, lo mismo con más razón.
- Si **P1 pasa y P2 falla** → el canje se **desplaza** otra vez (como con novedad de sitio): se registra como desplazamiento,
  no como solución, y **tampoco** entra al tronco. La cláusula (a) se aplica igual: no hay cuarto candidato.

Coste: 5 brazos × 20 semillas × 200 000 ≈ **8–9 min** con `Pool(14)` (el brazo barajado cuesta ~2× porque consulta el valor
del sitio compañero; 4 brazos ≈ 6 min si se quita el de lectura).

## 4. Las cuatro trampas de `EQUIPO.md` (regla 5), revisadas

1. **Canal social simétrico** — *no aplica*: no hay dos organismos ni canal. Lo que sí se hereda: el control tiene que romper
   **una sola** cosa. `sat_barajada` cambia **a qué sitio** se le aplica el recorte y nada más: el presupuesto total de
   magnitud recortada, la dinámica temporal y el RNG del organismo son idénticos al brazo tratado.
2. **Acierto sin balancear** — la adquisición es la fracción de los **últimos 10 inyectados** con el signo de valor correcto;
   el pool es 25/25 por construcción, pero una ventana concreta puede desbalancearse. Dos defensas, ninguna de ellas criterio
   nuevo: (a) los brazos se comparan **pareados sobre la misma semilla**, y el orden de inyección lo fija `seed + 700000`, que
   **ningún brazo toca** (los RNG nuevos son `seed + 950000` y sólo en el control); (b) se reporta el **sesgo de signo**
   (fracción de los 50 con `W > 0`): si un brazo llegara a 0.85 con un sesgo lejos de 0.5, el resultado es del sesgo y se anula.
3. **Mundo que se come la comida (muestreo asimétrico)** — lo mordido reaparece en su sitio a los 50 pasos (`regen = 50`) y los
   8 sitios existen siempre; la asimetría que queda es de **valor** (−3/+1) y es justamente el objeto del experimento: aquí no
   se "arregla" el mundo, se recorta **cómo la brújula lee el recuerdo**, y el coste se cobra en P2 (comida) y en muertes.
   **Riesgo declarado por escrito antes de correr:** al quitar el muro, el organismo pasará más por sitios de veneno; la boca
   no muerde por eso (usa `valor()` con el −3 entero), pero **el tiempo gastado allí no se come**, así que P2 y las muertes son
   el precio y pueden hundir el bloque. Es el mismo coste que el §1 del bloque 2 bis anotó y se anota igual.
4. **Sitios fijos que se memorizan (el "ciego" ya sabe)** — el órgano no añade ninguna memoria: **quita** magnitud a la que ya
   había, y sólo puede leer sitios que `M` conoce, es decir que el organismo **pisó** (no se le pasa `_SIT`). La medida del
   veredicto no es de sitios: es el signo del valor de los patrones nuevos leído con `valor()`, que no mejora por saberse las
   posiciones. Se reportan `M_llenas` y `sitios_pisados` por brazo para poder verlo.

**Trampa propia de este diseño, declarada aparte:** saturar podría mejorar la adquisición **sin explorar más**, simplemente
porque el organismo se queda más cerca de los sitios y muerde más. Contra eso: (i) se reporta el **equilibrio de visitas**
entre los 8 sitios (mecanismo directo: si P1 pasa con equidad ≈ la de `MAPA`, el efecto no es exploración y se dice así);
(ii) `MAPA_ATEN` da la misma "cantidad de mapa" sin la corrección de asimetría.

## 5. Anexo — observado en el humo (escrito DESPUÉS de correrlo; **no** cambia nada de arriba)

Humo de **un proceso**, **3 corridas** de 200 000 pasos, **semilla 1** (fuera de la serie 81–100, a propósito), mundo completo
con mapa. Ninguna constante, brazo ni criterio de §1–§4 se ha tocado con lo que se ve aquí; se anota para el auditor.

Salida completa: `datos/escala_humo_s1_20260917_225240.log` (`python experimentos/nivel8_escala_mapa/corre_escala.py --humo --seed 1`).

- **Identidad:** `mundo_largo_e` (`d1398f0428b1739b`) con las perillas apagadas es **idéntico** a `mundo_largo`
  (`9f74ff6b5941e5a5`) en **todas** las claves del original, con el mundo completo (mapa, 50 patrones, inversión en
  t = 100 000) y 200 000 pasos; la única clave de más es `esc_diag` (diagnóstico). El arnés de la serie (semillas 1, 2, 3)
  exige exactamente eso y **para** el experimento si falla.
- **Coste de cómputo:** 57.6 s (`mundo_largo`) → 54.9 s con las perillas apagadas → 65.1 s con `sat_M = 1.0`: **+19 %**.
- **Reproducción cruzada, gratis:** la fila `MAPA` de abajo coincide **dígito a dígito** con la fila `MAPA` del humo del
  bloque 2 bis (`PREREGISTRO_novedad_sitio.md` §5: 0.775 · 0.40 · 982 · 80 · 70 · 0.48), que se midió con **otro** gemelo
  (`mundo_largo_n`). Dos instrumentos distintos, mismo mundo, mismos números.
- **Hueco del bloque 2 bis, cerrado:** aquí la corrida de identidad **es** el brazo `MAPA` medido con `mundo_largo_e`, así
  que el reparto de visitas de `MAPA` sale gratis (allí faltó por el límite de tres corridas).
- **Una sola semilla, que no es evidencia de nada** (la serie son 20 semillas, la mediana y dos controles):

| s1 | adq (≤ 30) | adq final | comida Q4 | muertes | celdas | M_llenas | sesgo de signo | visitas (total · mín/máx · equidad · H) |
|---|---|---|---|---|---|---|---|---|
| MAPA (= corrida de identidad) | 0.775 | 0.40 | 982 | 80 | 70 | 8 | 0.48 | 7 237 · 422/1 696 · 0.249 · 0.947 |
| **MAPA_SAT (`sat_M = 1.0`)** | **0.800** | 0.80 | **1 098** | 91 | 69 | 8 | 0.36 | 8 070 · 568/2 239 · 0.254 · 0.940 |

- **Lo que sí se puede decir:** el instrumento arranca, la identidad se cumple y **la perilla muerde** (la conducta cambia
  de verdad: adquisición final 0.40 → 0.80, comida Q4 982 → 1 098). El coste que el §3 y la trampa 3 temían —que quitar el
  muro hundiera la comida— **no aparece en esta semilla**: la comida sube (+12 %), con 11 muertes más.
- **Lo que NO se puede decir, y no se dice:** que el órgano funcione. La adquisición ≤ 30 se mueve poco (0.775 → 0.800,
  **por debajo del 0.85 de P1**) y, sobre todo, **el reparto de visitas casi no cambia** (equidad 0.249 → 0.254, H 0.947 →
  0.940): en esta semilla el recorte **no** devolvió al organismo a los sitios que no pisaba. Eso es exactamente lo contrario
  de lo que hizo la novedad de sitio a dosis 1.8 (equidad 0.139 → 0.455 con adq 0.841), y deja sobre la mesa la lectura que
  la cláusula (a) de la refutación ya contempla: **la brújula sigue diciendo "ve a la comida recordada" aunque el veneno deje
  de repeler** (+0.54 contra −0.54 a un sitio de distancia, en vez de +0.54 contra −1.62), así que el organismo puede seguir
  acampando en los sitios de comida sin que ninguna constante esté mal puesta. Se anota como observación, **no** se toca nada.
- **No se ajusta nada y no se prueba una dosis.** `sat_M = 1.0` y `kappa_M = 0.5` estaban escritos en §1 **antes** de este
  humo y siguen igual; la predicción de §3 (0.875, 17/20) se deja tal cual aunque esta semilla apunte más bajo — el
  precedente ERR-21 y la enmienda 1 del bloque 2 bis dicen que una dosis suelta cuesta una serie entera.
- **Lo que el humo no puede decidir por construcción:** no se corrió ninguno de los dos controles (`MAPA_SAT_BAR`,
  `MAPA_ATEN`) — son los que separan "quitar el muro del veneno" de "poner menos mapa", y para eso está la serie.
- **Hueco de este humo (para el auditor):** el `sesgo_signo` de `MAPA_SAT` sale 0.36 (`MAPA` 0.48) en esta semilla; con el
  pool 25/25 lo esperable es ≈ 0.5. Con una semilla no se distingue del ruido, pero la trampa 2 del §4 ya obliga a
  reportarlo por brazo en la serie y a **anular** cualquier brazo que llegue a 0.85 con el sesgo lejos de 0.5.
