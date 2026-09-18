# Bloque 2 bis (nivel 8 propio): novedad de sitio contra el canje exploración/explotación del mapa

**Escrito ANTES de construir el instrumento y ANTES de correr. 17 sep 2026, 22:10 (día 6; sigue al bloque 2, refutado).**
Regla 12. Candidato **ya escrito en `PREREGISTRO_curiosidad.md` §3 antes de ver los datos del bloque 2**: *novedad de sitio*.

## 0. Qué se sabe (datos, no impresiones)

En el mundo largo (`experimentos/nivel8_mundo_largo/`: 50 patrones, uno cada 4 000 pasos en 8 sitios fijos, `r_vis = 3`,
inversión de regla en t = 100 000):

| serie | V13 adq (≤ 30 vistos) | MAPA | MAPA+curiosidad | curiosidad barajada |
|---|---|---|---|---|
| `largo_s1-20` / `largo_s21-40` | 0.88 / 0.90 | 0.70 / 0.70 | — | — |
| `curiosidad_s41-60` | 0.900 (comida Q4 837) | 0.704 (968) | **0.700** (974) | 0.700 (968) |

El mapa **da de comer** y muere menos, pero **baja la adquisición de lo nuevo**; la curiosidad por progreso de error **no la
devolvió**: 0.700 = mapa = control barajado (P1 NO, 7/20; P3 NO, 6/20). La causa está escrita en aquel preregistro y se
confirmó: *el sesgo sólo actúa sobre sitios recordados y el progreso de un sitio al que no se va es 0 hasta la primera
mordida* — la curiosidad premia lo que ya se está aprendiendo, y lo nuevo entra donde el organismo **dejó de ir**.

El fallo del mapa es concreto y medible: cada 4 000 pasos entra un patrón nuevo en el sitio cuyo tipo lleva más tiempo sin
renovarse (`_ren`, ronda por los 8 sitios); el organismo con mapa recuerda que *aquel* sitio tenía veneno (`valor ≈ −3`),
no vuelve, y **no se entera** de que ahora hay otra cosa. Celdas 84 (mapa) contra 90 (v13): ve menos.

## 1. Órgano candidato: **novedad de sitio** (mecanismo mínimo local)

Una sola cantidad nueva por posición, y el sesgo donde ya está el del mapa.

- **Reloj de visita.** `t_visita[pos] = t` cuando el organismo **pisa** una posición con el objeto presente (`pos in objs`):
  exactamente el mismo evento que escribe la tabla `M`, una línea al lado. Pisar sin morder cuenta (visitar es enterarse de
  qué hay, no comérselo); pasar por un sitio vacío no cuenta (no informa de nada); ver desde lejos tampoco (el mapa tampoco
  se escribe mirando). Contador `n_visitas[pos]` sólo como lectura.
- **Novedad.** `nov(pos) = min(1, (t − t_visita[pos]) / tau_N)` ∈ [0, 1]. Nunca pisado ⇒ `t_visita = 0` ⇒ novedad máxima.
- **Sesgo**, sólo donde ya actúa el mapa (retina vacía), por dirección y sobre los **sitios que la tabla `M` conoce**
  (`_Mset`, los que el organismo ya pisó alguna vez: no se le regala la lista de sitios del mundo — ver trampa 4):
  `N_dir = Σ_h disc^h · nov(pos ± h)` con `disc = disc_M = 0.9`, `H = H_M = 20` (los del mapa, sin perilla nueva);
  `u += gamma_N · [N_izq, N_der]` **además** de `gamma_M · [B_izq, B_der]`.
- **Constantes, fijadas aquí y no tocadas después:**
  - `gamma_N = 0.6 = gamma_M`. Justificación *a priori*: `nov` está normalizada a [0, 1], así que un sitio máximamente
    novedoso pesa **lo mismo que un sitio recordado con valor +1**, que es exactamente `R_VAL['comida']`. No es una
    calibración: es la única escala que el mundo ya define.
  - `tau_N = 4 000 = T_nuevo`. Justificación *a priori*: un sitio que lleva un periodo de inyección entero sin pisarse
    **pudo** haber sido renovado sin que el organismo se enterara. Es el reloj del mundo, no un ajuste.
- No toca la boca (morder sigue decidiéndose con `valor()`), ni el aprendizaje, ni las celdas, ni el RNG del organismo.
  Con `gamma_N = 0` es `mundo_largo` **bit a bit** (identidad obligatoria, 3 semillas, mundo completo, todas las claves).
- **Coste esperado del órgano, escrito antes:** los sitios menos pisados son, por construcción, **los de veneno** (el mapa
  los evita). La novedad empuja hacia ellos. Eso es lo que se quiere (allí entra lo nuevo) y es también lo que puede costar
  comida y muertes: P2 existe para cobrarlo. El sesgo mueve el cuerpo, **no** la boca: ir a un sitio de veneno no es morderlo.

## 2. Brazos (mundo largo completo, semillas NUEVAS **61–80**, T = 200 000)

**De criterio (los cuatro del método del bloque 2):**

| brazo | perillas | qué es |
|---|---|---|
| `V13` | `usa_M = False` | el tronco, techo de adquisición (0.90) |
| `MAPA` | `usa_M = True`, `gamma_M = 0.6` | el canje medido (0.70 / comida 968) |
| **`MAPA_NOV`** | `+ gamma_N = 0.6`, `tau_N = 4000` | el órgano |
| `MAPA_NOV_BAR` | `+ nov_barajada` | **control 1**: la novedad de cada sitio se lee **en otro sitio** (permutación fija de las 8 posiciones de sitio por semilla, RNG propio `seed + 900000`). Misma magnitud y misma dinámica temporal; sólo se rompe la **atribución**. |

**Alcance de la permutación del control 1 (observación del auditor sobre el bloque 2, incorporada antes de correr).** En el
bloque 2 el control barajaba sobre las **90 celdas de `NKMAX`, incluidas las inactivas**, así que buena parte de la
permutación caía sobre índices vacíos y **diluía el control** (le daba progreso 0, no el progreso de otra celda). Aquí la
permutación se aplica **sólo sobre las posiciones de sitio que existen** (`sorted(_SIT)`, las 8), nunca sobre las 40
posiciones del anillo: los valores permutados son novedades **reales** de sitios reales, con la misma distribución y el
mismo reloj que el brazo tratado; lo único que cambia es a qué sitio se le atribuye cada una. Permutar las 40 posiciones
habría dejado `t_visita = 0` en las 32 posiciones que nunca son sitio y, por tanto, `nov ≡ 1`: eso no es "novedad
barajada", es el **otro** control (`nov_cte`), y se corre aparte y con ese nombre. Nota honesta: una permutación de 8
elementos deja ~1 punto fijo de media (un sitio que se lee a sí mismo); eso hace el control **más parecido** al brazo
tratado, es decir **conservador** para P3 (dificulta, no facilita, que el control se distinga).

**De lectura (no deciden el veredicto; se pueden quitar si el coordinador necesita CPU):**

| brazo | perillas | qué separa |
|---|---|---|
| `MAPA_NOV_CTE` | `+ nov_cte` (`nov ≡ 1`) | **control 2**: "novedad" constante = sólo **más atracción a los sitios conocidos**, sin información temporal. Separa *novedad* de *más sesgo*. |
| `MAPA_NOV_ALTA` | `gamma_N = 1.8` | **dosis, exploratoria**: `1.8 = 0.6 × 3`, el 3 de `|R_VAL['veneno']| / R_VAL['comida']` (la escala que haría falta para que la novedad compita con el recuerdo de un veneno). **No puede declarar el veredicto**; si el brazo principal falla y éste no, hace falta una serie nueva preregistrada con semillas nuevas (precedente ERR-21). |

Medidas: las del mundo largo (adquisición ≤ 30 vistos y final, retención de los nunca invertidos, comida Q4, muertes,
recuperación, celdas) más dos lecturas nuevas del mecanismo: **equilibrio de visitas** entre los 8 sitios (mín/máx y
entropía normalizada) y **sesgo de signo** (fracción de los 50 patrones con `W > 0` al final; debe rondar 0.5).

## 3. Criterios y predicción numérica (medianas de 20 semillas; pareado = misma semilla)

- **P1 (recupera la exploración):** `MAPA_NOV` adquisición (≤ 30 vistos) mediana ≥ **0.85** **y** > `MAPA` pareado en **≥ 15/20**.
- **P2 (no pierde la comida):** `MAPA_NOV` comida Q4 ≥ **0.9 × `MAPA`** pareado en **≥ 15/20**. *(Referencia informativa, no
  criterio: en 41–60 `MAPA` dio 968 y `V13` 837.)*
- **P3 (la novedad está bien atribuida):** `MAPA_NOV` > `MAPA_NOV_BAR` en adquisición pareado **≥ 15/20**, **y** el control
  **no** supera a `MAPA` en ≥ 15/20, **y** su mediana **no** llega a 0.85 (barajar no explora "mejor").
- **P4 (no es sólo ir más a los sitios; lectura):** `MAPA_NOV` > `MAPA_NOV_CTE` pareado ≥ 15/20 y `MAPA_NOV_CTE` no llega a 0.85.
- **Empates (ERR-17, escrito antes de ver datos):** la adquisición está cuantizada en pasos de 0.1 y los empates son
  frecuentes; el criterio pareado es con `>` **estricto** y se reportan siempre `gana/empata/pierde`. Si un criterio pareado
  se queda por debajo de 15 **con empates**, se aplica el desempate **ya preregistrado aquí** y sólo éste: `gana ≥ 0.75 ×
  (gana + pierde)` con `gana + pierde ≥ 8`; se declara como "pasa por desempate" y se registra así. Nada más se recalibra.
- **Predicción:** P1, P2 y P3 pasan → "*la novedad de sitio devuelve la exploración al organismo con mapa sin cobrarle la
  comida*"; se habilita el bloque 4 (v14 = v13 + mapa + novedad) con examen v3', batería y regresión.
- **Refutación (cualquiera de las dos):** (a) **P1 falla** → la novedad de sitio no basta y el canje del mapa sigue abierto;
  se registra y **no** se prueba otra perilla de ésta. Lectura ya escrita para ese caso: el recuerdo de veneno (−3) pesa más
  que la novedad máxima (+0.6), es decir el problema es de **escala**, no de mecanismo — y entonces la decisión es del
  director, con serie y semillas nuevas, no un ajuste de `gamma_N` sobre estos datos. (b) **P1 pasa pero P3 o P4 falla** →
  el efecto es **sesgo extra**, no novedad; se registra con ese nombre y el órgano **no** entra al tronco.
- **Vocabulario si pasa:** *"vuelve a los sitios que lleva tiempo sin pisar y por eso encuentra lo nuevo"*. No "curiosidad",
  no "quiere explorar", no "sabe que hay algo nuevo".
- Coste: 6 brazos × 20 semillas × 200 000 ≈ 9 min con `Pool(14)` (4 brazos ≈ 6 min si se quitan los de lectura).

## 4. Las cuatro trampas de `EQUIPO.md` (regla 5), revisadas

1. **Canal social simétrico** — *no aplica*: aquí no hay dos organismos ni canal; el sesgo es interno y sólo mueve el cuerpo.
   Lo que sí se hereda de aquella lección: el control tiene que romper **una** cosa (la atribución) y dejar el resto igual;
   por eso `nov_barajada` permuta entre **sitios** (mismos valores, mismo reloj) y no entre las 40 posiciones (eso habría
   dejado la novedad clavada en 1 y sería el otro control, `nov_cte`).
2. **Acierto sin balancear** — la adquisición es la fracción de los **últimos 10 inyectados** con el signo de valor correcto,
   y el pool es 25 comida / 25 veneno por construcción, pero una ventana concreta puede estar desbalanceada. Dos defensas:
   (a) los brazos se comparan **pareados sobre la misma semilla**, y la ventana y su composición son **idénticas** en todos
   los brazos (el orden de inyección lo fija `seed + 700000`, que ningún brazo toca); (b) se reporta el **sesgo de signo**
   (fracción de los 50 con `W > 0`): si un brazo llegara a 0.85 con un sesgo lejos de 0.5, el resultado es del sesgo y se
   anula. Ninguno de los dos es criterio nuevo: son lecturas para poder anular, no para ajustar.
3. **Mundo que se come la comida (muestreo asimétrico)** — en este mundo lo mordido **reaparece en su sitio** a los 50 pasos
   (`regen = 50`), que es justo el arreglo que equilibró las visitas en N3c; y los 8 sitios existen siempre. La asimetría que
   queda es de **valor** (−3 veneno / +1 comida), y no la arregla este órgano: la anota como el coste esperado del §1 y la
   mide con comida Q4 y muertes. La asimetría de visitas que sí importa aquí es **el efecto que se quiere medir**, y por eso
   se reporta explícitamente (equilibrio de visitas entre los 8 sitios), no sólo su consecuencia.
4. **Sitios fijos que se memorizan (el "ciego" ya sabe)** — es la trampa más cercana a este diseño, porque el órgano es
   literalmente una memoria de sitios. Se cierra por dos lados: (a) el sesgo de novedad sólo puede apuntar a sitios que
   **`M` ya conoce**, es decir que el organismo **pisó**; no se le pasa `_SIT` (la lista de sitios del mundo), que sería
   regalarle el mapa; (b) la medida del veredicto **no es de sitios**: es el signo del valor de los patrones nuevos leído
   con `valor()`, que no mejora por saberse las posiciones. Un organismo que sólo memorizara sitios no movería P1.
   Riesgo residual declarado: si un sitio nunca se pisa, nunca entra en `M` y la novedad **no** puede llevar a él
   (se reporta `M_llenas` y el número de sitios pisados por brazo para poder verlo).

## 5. Anexo — observado en el humo (escrito DESPUÉS de correrlo; **no** cambia nada de arriba)

Humo de **un proceso**, 3 corridas de 200 000 pasos, **semilla 1** (fuera de la serie 61–80, a propósito), mundo completo
con mapa. Ninguna constante, brazo ni criterio de §1–§4 se ha tocado con lo que se ve aquí; se anota para el auditor.

- **Identidad:** `mundo_largo_n` con `gamma_N = 0` es **idéntico** a `mundo_largo` en todas las claves del original, con el
  mundo completo y 200 000 pasos; la única clave de más en el gemelo es `nov_diag` (diagnóstico). El arnés de la serie
  (semillas 1, 2, 3) es el mismo y exige exactamente eso.
- **Coste de cómputo:** 62.4 s (`mundo_largo`) → 66.6 s con `gamma_N = 0.6`: +7 %.
- **Una sola semilla, que no es evidencia de nada** (la serie son 20 semillas y la mediana):

| s1 | adq (≤ 30) | adq final | comida Q4 | muertes | celdas | sesgo de signo | visitas por sitio (mín/máx, H) |
|---|---|---|---|---|---|---|---|
| MAPA | 0.775 | 0.40 | 982 | 80 | 70 | 0.48 | (no medido, ver abajo) |
| MAPA+NOV (`gamma_N = 0.6`) | 0.800 | 0.70 | 983 | 85 | 71 | 0.50 | 531 / 2248, H = 0.952, 8/8 pisados |

- **Lo que sí se puede decir:** el instrumento arranca, la identidad se cumple, el sesgo se aplica (los 8 sitios se pisan,
  8 803 visitas repartidas con entropía 0.95) y la comida no se hundió en esta semilla (983 contra 982).
- **Lo que NO se puede decir, y no se dice:** que el órgano funcione. En esta semilla la adquisición ≤ 30 queda en 0.800,
  **por debajo del 0.85 preregistrado**. La tentación evidente sería subir `gamma_N`; **no se hace**: la duda de escala ya
  está cubierta por el brazo de dosis `MAPA_NOV_ALTA` (`gamma_N = 1.8`), escrito en §2 **antes** de este humo y marcado como
  no confirmatorio. Si el brazo principal falla, se registra la refutación tal cual.
- **Hueco del humo (para el auditor):** el reparto de visitas del brazo `MAPA` **no** se midió, porque la corrida de
  referencia fue `mundo_largo`, que no trae `nov_diag`; medirlo habría costado una cuarta corrida y el límite acordado para
  un agente era tres. En la serie **todos** los brazos pasan por `mundo_largo_n`, así que la comparación de equilibrio de
  visitas MAPA vs MAPA+NOV — que es la lectura directa del mecanismo — sale sola.
