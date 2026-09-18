# PREREGISTRO — REPRODUCCIÓN, BLOQUE 2: una medida ligada a la supervivencia (mundo vivo; línea F)

**Del diseñador del mundo vivo para el coordinador, 18 sep 2026 (~09:30), escrito ANTES de correr nada con `Pool` y
ANTES del humo** (las predicciones del humo van en §8). Misión: llegar a la AGI por este camino — un organismo mínimo con
reglas locales, sin retropropagación en el runtime, que aprende, sobrevive y se reproduce con evidencia preregistrada.

**Semillas NUEVAS: 261–280 (primera serie) y 281–300 (réplica). Nada se recalibra sobre 221–240**: sus números aparecen
aquí sólo como *diagnóstico* de ERR-40 y como *origen declarado de los márgenes* (como hizo la enmienda 2 con 181–200).

---

## 0. ERR-40 — la ventana de viabilidad no está ligada a la supervivencia: premia atracones que mueren más

**Hecho (221–240, `vivo_rep_s221-240_20260918_091428`):** la medida del bloque 1 (`descendientes` = ventanas de 500 pasos
con las dos necesidades ≥ 1.0) dio ESCALAR 36 y BARAJA_CON 39.5 contra VIVO 20, con 149.5 y 159.5 muertes contra 100:
A₁₂(VIVO > ESCALAR) 0.007, A₁₂(VIVO > BARAJA_CON) 0.0 → por la cláusula de P-R1, la medida se tiró. Lo demás se reportó
sin interpretar (P-R2, P-R3, P-R4, P-R5, P-R6 pasan; P-R5b: **la tercera fila sobra** — CUELLO_MIN 65.5 > REP_SIN_COSTE
55, A₁₂ 0.146; P-R7 y P-R8 no).

**Diagnóstico (dos ingredientes, ambos medidos en 221–240, ninguno una recalibración):**
1. **Contabilidad:** el conteo no tenía término de muerte. Morir era gratis para la medida.
2. **El mundo hace de la muerte un recurso, y las filas promediadas son pesimistas por accidente.** Al morir, el cuerpo
   renace en `E = Ag = 0.6` (a un bocado de cada cosa del umbral 1.0) y en un sitio al azar: **el renacer regala 600
   pasos de drenaje** y un escape del anillo atascado. Y ESCALAR / BARAJA_CON, cuyas filas promedian las dos
   necesidades (≈ −1.5 para sal y veneno), **rechazan sal y veneno saciados** (tasas 0.03 / 0.02, como CUELLO_MIN) y
   **los muerden hambrientos** (con −1.5 el impulso gana desde déficit ≈ 0.65; con −3 nunca): sostienen ventanas cuando
   están llenos y mueren cuando están vacíos. VIVO hace lo contrario: no muere de veneno (0.001) pero se bebe la reserva
   saciado (sal 0.797). La ventana sola veía la primera mitad de cada organismo.

---

## 1. La medida: candidatas comparadas por escrito, y la elegida

| candidata | qué es | por qué NO (o sí) |
|---|---|---|
| **(a) por vida** `desc / (muertes + 1)` | R₀ por individuo | **Falla con el propio dato de ERR-40**: ESCALAR 0.242 y BARAJA_CON 0.251 contra VIVO 0.182 (retrodicción sobre 221–240). Un linaje de vidas cortas con una ventana cada una puntúa más; y no es monótona en las muertes |
| **(b) exclusión tras la muerte** (ventana válida sólo ≥ X pasos después del último renacer) | quita las ventanas que financia el regalo del renacer | Quita **sólo** esas; las ventanas *orgánicas* de ESCALAR (rechaza sal saciado) siguen contando, y su muerte llega en la fase hambrienta, después. Cuánto habría quitado **se mide** (`desc_regalo`, §3) pero no decide |
| **(c) coste real + vivo Y pasos después** | el descendiente cuesta 0.4/0.4 y cuenta si el cuerpo sigue vivo Y después | No quita el atracón: tras pagar, el cuerpo queda en ≥ 0.6/0.6 y ESCALAR sólo muerde veneno desde déficit 0.65 (E ≤ 0.35), es decir ≥ 250–650 pasos después: con Y = 500 casi todo cuenta. Además cambia la física de todos los brazos (la medida deja de ser de sólo lectura) |
| **(d) ELEGIDA: crecimiento neto del linaje `r = descendientes − muertes`** | nacimientos menos muertes por corrida de 100 000 pasos; tipo de cambio **1 : 1**, el de la dinámica de poblaciones (un nacimiento suma un individuo, una muerte lo quita) | Ver abajo. Es de sólo lectura (dos claves que ya existen), no toca al organismo, y tiene un umbral con significado: **r ≥ 0 = tasa de reemplazo** |

**Por qué (d) no puede premiar morir (construcción):**
1. Cada muerte resta uno. El regalo del renacer dura 600 pasos (< 2 ventanas de 500): **una muerte financia a lo sumo
   una ventana → −1 + 1 ≤ 0**. Morir nunca suma; a lo sumo empata.
2. Para quedar por encima de VIVO muriendo Δm veces más hay que producir **Δm ventanas más**, cada una de 500 pasos
   seguidos saciado. En 221–240 ESCALAR y BARAJA_CON produjeron 16 y 20 ventanas más muriendo 50 y 60 veces más.
3. BARAJA_POL: vida media 268 pasos (< una ventana) y ~370 muertes → r ≈ −370 **por la física del mundo**, no por un
   umbral.
4. **Límite honesto, escrito:** ninguna medida de conteo ordena *todo* resultado posible "por construcción" salvo una
   lexicográfica (muertes primero), que no mediría reproducción. Lo que r fija por construcción es el tipo de cambio
   (1 : 1, el de las poblaciones, no una k ajustada) y que morir no suma. El orden con los brazos concretos es una
   **predicción** (P2-1) que puede fallar, y si falla se tira la medida por segunda vez y se cierra la línea de la
   reproducción como conteo.

**Retrodicción sobre 221–240 (NO es evidencia; se escribe para que se vea qué hace r con el dato que tumbó la medida
vieja; el runner la imprime con `--retro`):** medianas de r: VIVO −80, UNA_NEC −124.5, ESCALAR −113, BARAJA_CON
−118.5, BARAJA_POL −371.5, REP_SIN_COSTE −20.5, **CUELLO_MIN −13 (5/20 semillas con r ≥ 0; q75 −0.2)**. A₁₂ en r:
VIVO > ESCALAR 0.98, > BARAJA_CON 1.0, > UNA_NEC 0.97; UNA_NEC > BARAJA_POL 1.0; CUELLO_MIN > VIVO 1.0;
REP_SIN_COSTE > CUELLO_MIN 0.30.

---

## 2. Mecanismo: Occam — la tercera fila se retira; lo que se declara es la lectura pesimista saciado (CUELLO_MIN)

CUELLO_MIN (saciado, la boca lee el **mínimo de las dos filas primarias**; sin fila nueva, sin aprendizaje nuevo, sin rng)
rindió igual o mejor que la tercera fila (bloque 1: 65.5 contra 55 ventanas; A₁₂ 0.146; retrodicción en r: 0.30).
**¿Hay algo que la tercera fila haga y CUELLO_MIN no pueda? En este mundo, no, y se dice:** con cuatro estímulos de
consecuencia pura (cada uno toca UNA necesidad), el mínimo de las dos filas es el estadístico suficiente del cuello de
botella: coincide con el signo informativo de cada estímulo (sal: min(0, −3) = −3), llega ya aprendido (no necesita
bocados propios) y no gasta memoria; la tercera fila sólo puede ser más lenta (aprende de nuevo lo que las filas ya
saben), más blanda (mezcla: veneno −0.99 en un humo) y más gastona (come saciado al 0.98 y vacía el anillo). **Tampoco
en un mundo con un estímulo mixto** (ayuda a una necesidad y daña a la otra): una fila indexada por estímulo promedia sus
consecuencias (E[R] ≈ −1: veta igual que min(+1, −3) = −3); el mecanismo que allí distinguiría sería enrutar a la fila del
recurso *escaso* (CUELLO, no el mínimo) — un bloque futuro, no éste. **Decisión: la tercera fila se retira como candidata
a órgano.** REP_SIN_COSTE se corre sólo para medirla con r (P2-4); si superase a CUELLO_MIN sería un hallazgo no
explicado que exige réplica antes de decir nada.

**Lo que se declara si pasa (y sólo entonces):** *"una regla local de lectura pesimista saciado (leer las dos necesidades y
quedarse con la peor) lleva el crecimiento neto del linaje del organismo del mundo vivo desde r ≈ −80 hasta el filo del
reemplazo (r ≈ 0 por 100 000 pasos), muriendo menos y sosteniendo más ventanas, sin memoria nueva; la tercera fila de
valor no aporta sobre ella"*. Vocabulario: *crecimiento neto del linaje*, *tasa de reemplazo*, *lectura pesimista
saciado*. **No** se dice "se reproduce" (nada nace), "población", "evoluciona", "quiere", "tiene propósito".

---

## 3. Instrumento, brazos y semillas

**Instrumento:** `organismo_vivo_rep2.py` (**96feb4918dc5d694**), construido POR ANCLAS por `construye_vivo_rep2.py`
(**46d2bfaa74538759**; 7 inserciones, ninguna nombra al rng) desde `organismo_vivo_rep.py` (aa823d56c2d4213c, el del bloque 1, que aquí SÓLO SE LEE; cadena:
`organismo_vivo` 20c0961c79de8825 ← tronco `organismo_v14` v14.1 feefc88b1fd8d434). Ningún archivo existente se toca.
La medida r **no necesita código nuevo**; lo que rep2 agrega, de sólo lectura y detrás de `rep2=1`, son los
**diagnósticos** de ERR-40: `desc_regalo` (ventanas cuya cuenta empezó dentro de los `rep2_regalo = 600 = 0.6/costo`
pasos que dura el regalo del renacer; `t = 0` cuenta como nacimiento) y `vidas` (longitudes de las vidas, `vida_final`).
Identidad exigida (arnés `identidad_vivo_rep2.py`, §9): apagada ≡ `organismo_vivo`; cadena ≡ `organismo_v14`; `rep2 = 0`
≡ `organismo_vivo_rep` en todas las claves; `rep2 = 1` claves viejas bit a bit + 4 nuevas y coherencia
(`len(vidas) = muertes`, `Σ vidas + vida_final = T`, `desc_regalo ≤ descendientes`).

| brazo | perillas (sobre `organismo_vivo_rep2`, `reproduccion=1, rep_mide=1, rep_X=500, rep_umbral=1.0, rep_coste=0, rep2=1`) | papel |
|---|---|---|
| **VIVO** | 2 necesidades, 4 estímulos | línea base (≡ `organismo_vivo` VIVO en las claves viejas) |
| **CUELLO_MIN** | `rep_cuello=2` | **el mecanismo que se declara** |
| **REP_SIN_COSTE** | `n_nec=3, rep_nec=1` | la tercera fila, retirada: sólo se mide (P2-4) |
| **UNA_NEC** · **ESCALAR** · **BARAJA_CON** · **BARAJA_POL** | como en el bloque 1 | los controles que ordenan la medida (P2-1) |

7 brazos × 20 semillas × 100 000 pasos = 140 corridas (~2–5 min con `Pool(14)`; el bloque 1: 180 corridas en 3 min).
**Alias estructurales (los cinco solapamientos, `diagnostico_codigos.py`, sin simular):** 261–280 → **278** (sal==agua);
281–300 → **286** (sal==veneno). Se reporta el conjunto completo y al lado las LIMPIAS (19/20), mismos umbrales (regla 10).

---

## 4. Predicciones (escritas antes del humo y del bloque; márgenes declarados desde las medianas de 221–240)

Estadística (ERR-37): `r`, `descendientes`, `muertes`, tasas saciado y `frac_regalo` son integrales de trayectoria →
**A₁₂ sin parear** (400 pares), medianas, cuartiles; pareado sólo lo aprendido (`xor01`, celdas). Ningún `max`; un `None`
nunca cuenta como victoria.

| # | predicción (261–280) | de dónde sale | refutación |
|---|---|---|---|
| **P2-1** | **la medida ordena como la supervivencia**: A₁₂ en r: VIVO > ESCALAR **≥ 0.80**; VIVO > BARAJA_CON **≥ 0.80**; VIVO > UNA_NEC **≥ 0.80**; UNA_NEC > BARAJA_POL **≥ 0.95** | retrodicción 0.98 / 1.0 / 0.97 / 1.0; margen ancho | **cualquiera < 0.50 → la medida se tira** y la línea "reproducción como conteo" se cierra; entre 0.50 y el umbral → ordena débilmente, se reporta |
| **P2-2** | **mediana de r por brazo** dentro de su intervalo: VIVO [−115, −45] · UNA_NEC [−160, −90] · ESCALAR [−150, −80] · BARAJA_CON [−155, −85] · BARAJA_POL [−430, −310] · REP_SIN_COSTE [−55, +15] · CUELLO_MIN [−50, +25]; pasa con **≥ 6/7** dentro | medianas de 221–240 ± ~35 (el cuartil interno observado es ±8–15; el margen es holgado a propósito) | < 6/7 → los brazos no están donde se predijo: la medida es más sensible a la semilla de lo previsto, se reporta |
| **P2-3** | **mecanismo**: r A₁₂(CUELLO_MIN > VIVO) **≥ 0.90** y diferencia de medianas **≥ 40**; muertes A₁₂(CUELLO_MIN < VIVO) **≥ 0.80**; descendientes A₁₂(CUELLO_MIN > VIVO) **≥ 0.90** | retrodicción 1.0 / 67 / — / 1.0 | r A₁₂ < 0.75 → la lectura pesimista no mueve el crecimiento neto: no se declara |
| **P2-4** | **Occam**: r A₁₂(REP_SIN_COSTE > CUELLO_MIN) **≤ 0.50**; REP_SIN_COSTE > VIVO A₁₂ **≥ 0.85** | retrodicción 0.30 y 1.0 | ≥ 0.65 → hallazgo no explicado: la tercera fila hace algo que no supe predecir; **réplica antes de decir nada** |
| **P2-5** | **tasa de reemplazo**: CUELLO_MIN r ≥ 0 en **≥ 2/20 y ≤ 14/20** (en el filo, no por encima); VIVO, UNA_NEC, ESCALAR, BARAJA_CON, BARAJA_POL: r ≥ 0 en **0/20** cada uno; REP_SIN_COSTE ≤ 8/20 | retrodicción 5/20; VIVO q75 −71.8; REP_SIN_COSTE 2/20 | CUELLO_MIN 0/20 → no llega al filo; > 14/20 → está por encima del reemplazo (mejor de lo predicho, y también se dice) |
| **P2-6** | **conducta saciado**: mediana `sac_tasa[D]` VIVO **≥ 0.60**; CUELLO_MIN sal **≤ 0.05** y veneno **≤ 0.05** | 221–240: 0.797 / 0.001 / 0.001 | CUELLO_MIN > 0.15 → el mínimo no veta: instrumento |
| **P2-7** | **diagnóstico de ERR-40 (blanda, se reporta)**: `frac_regalo = desc_regalo / desc`: A₁₂(ESCALAR > CUELLO_MIN) **≥ 0.75** y A₁₂(BARAJA_CON > CUELLO_MIN) **≥ 0.75** | vida media 664 / 623 contra 1299: la primera ventana de cada vida nace del regalo; las siguientes (orgánicas) sólo las tienen las vidas largas | si no → el regalo del renacer no explica la diferencia: ERR-40 queda sólo en la contabilidad (el ingrediente 2 de §0 se reescribe) |
| **P2-8** | **seguridad y mundo**: en CUELLO_MIN y REP_SIN_COSTE `xor01` = 1.0 y celdas 4/4 en **≥ 18/20**; `exposiciones[D]` CUELLO_MIN **≤ 3 ×** VIVO; `exposiciones[A]` **≥ 0.6 ×** VIVO | núcleo replicado; bloque 1: sal ×1.9, comida ×0.69 para la tercera fila (CUELLO_MIN: predicción nueva, letra nueva) | `xor01` cae → la regla cuesta conocimiento; comida < 0.6× → la sal rechazada roba llegadas: r se lee neto |

**Identidad dentro del runner** (5 casos × 3 semillas): si no es 15/15, no corre nada. Regresión del tronco: nada se toca;
el runner verifica los tres shas de la cadena al arrancar.

---

## 5. Las cuatro trampas y las propias

1. *Canal simétrico* — n/a. 2. *Acierto sin balancear* — no se usa acierto; tasas por estímulo. 3. *El mundo que se come
la comida* — P2-8 la acota; y la **muerte como recurso** es la trampa nueva de este mundo (§0), ahora contabilizada.
4. *Sitios fijos* — `spawn()` sortea. **Propias:** (i) *la medida que es la supervivencia disfrazada*: con ~100 muertes
y ~20 nacimientos, r está dominada por las muertes en los brazos flojos; por eso P2-3 exige la ventaja **también** en
descendientes solos y P2-5 mira el cruce de r = 0, que las muertes solas no pueden producir; (ii) *elegir la medida
mirando el dato*: se hizo, y se declara (ERR-40 obliga); la protección es que las semillas son nuevas, los umbrales no
tocan la mediana esperada, y P2-1 puede tirar la medida por segunda vez.

---

## 6. Lo que NO se declara

Nada nace: `descendientes` es un contador de ventanas y r una razón de contabilidad con el tipo de cambio de las
poblaciones. No se dice "se reproduce", "población", "selección", "evoluciona", "quiere", "tiene propósito". Si CUELLO_MIN
cruza r ≥ 0 en algunas semillas se dice *"en el filo del reemplazo"*, no "viable" ni "autosostenido".

---

## 7. Coste y entregables

`construye_vivo_rep2.py`, `organismo_vivo_rep2.py`, `identidad_vivo_rep2.py`, `corre_vivo_rep2.py` (`--humo` de un
proceso; `--retro`; `Pool` sólo el coordinador: `--desde 261`, réplica `--desde 281`), este preregistro, humo
(`datos/vivo_rep2_humo_*`), arnés (`datos/vivo_rep2_identidad_*.log`).

---

## 8. Humo (UN proceso, 6 corridas de T = 100 000: VIVO, ESCALAR y CUELLO_MIN × semillas 1, 2) — predicciones ANTES de lanzarlo

- **H2-1** r(VIVO) > r(ESCALAR) en 2/2 (la inversión de ERR-40 desaparece con r).
- **H2-2** r(CUELLO_MIN) > r(VIVO) en 2/2.
- **H2-3** coherencia de los diagnósticos (vidas = muertes; regalo ≤ desc) en 6/6.
- **H2-4** (blanda) `frac_regalo` ESCALAR > CUELLO_MIN en 2/2.
- **H2-5** CUELLO_MIN saciado: sal ≤ 0.05 y veneno ≤ 0.05 en 2/2.
Si H2-1 falla, la medida no arregla ERR-40 ni en el humo: se escribe ERR-41 (provisional) y no se corre el bloque hasta
rediseñar. Los demás fallos se escriben aquí y el bloque corre con esta letra.

---

## 9. Arnés — resultado: **60/60** (`datos/vivo_rep2_identidad_20260918.log`; un proceso, T = 20 000, semillas 1–2)

Apagada ≡ `organismo_vivo` en 11 escenarios × 2 (incluido el de todas las `rep_*` y `rep2` encendidas con la maestra
apagada): 22/22 · cadena ≡ `organismo_v14` (base e inversión): 4/4 · `rep2 = 0` ≡ `organismo_vivo_rep` en los 7 brazos del
bloque, todas las claves: 14/14 · `rep2 = 1` en VIVO, ESCALAR, CUELLO_MIN y BARAJA_POL: claves viejas bit a bit y
exactamente las 4 nuevas (8/8), coherencia `len(vidas) = muertes`, `Σ vidas + vida_final = T`, `desc_regalo ≤ desc` (8/8),
las 9 claves que dependen del rng idénticas (9/9: el rng no se consume) · deben fallar (CUELLO_MIN, REP_SIN_COSTE): 4/4.
Dato lateral del arnés (T = 20 000, no es humo): la fracción de ventanas financiadas por el regalo del renacer es 2/3, 2/4
(VIVO), 5/6, 9/11 (ESCALAR), 4/13, 5/14 (CUELLO_MIN): la dirección de P2-7 (ESCALAR > CUELLO_MIN) se ve ya ahí.

## 10. Humo — resultado (18 sep 09:37; `datos/vivo_rep2_humo_20260918_093717.{log,json}`, sha del JSON fe29218dfcf798f7; identidad dentro del runner 10/10; 4.8–5.1 s por corrida)

| brazo | s | **r** | desc | regalo | muertes [E, agua] | vida mediana / máx | saciado A/B/C/D | xor01 | exposiciones A/B/C/D |
|---|---|---|---|---|---|---|---|---|---|
| VIVO | 1 | **−75** | 14 | 7 | 89 [58, 31] | 600 / 6146 | 1.00 / 0.00 / 0.84 / **0.78** | 1.00 | 778 / 5531 / 840 / 1922 |
| VIVO | 2 | **−86** | 17 | 7 | 103 [52, 51] | 600 / 4427 | 1.00 / 0.00 / 0.84 / **0.75** | 1.00 | 831 / 5096 / 843 / 2224 |
| ESCALAR | 1 | **−126** | 34 | 22 | 160 [66, 94] | 307 / 3142 | 0.98 / 0.01 / 0.90 / 0.02 | 0.50 | 426 / 5015 / 423 / 2472 |
| ESCALAR | 2 | **−172** | 34 | 26 | 206 [99, 107] | 214 / 3904 | 0.98 / 0.01 / 0.92 / 0.05 | 0.50 | 497 / 4942 / 524 / 2593 |
| CUELLO_MIN | 1 | **+3** | 67 | 24 | 64 [29, 35] | 756 / 8697 | 0.84 / **0.00** / 0.83 / **0.00** | 1.00 | 538 / 4262 / 615 / 3275 |
| CUELLO_MIN | 2 | **−2** | 64 | 22 | 66 [30, 36] | 857 / 6618 | 0.83 / **0.00** / 0.84 / **0.00** | 1.00 | 531 / 3864 / 549 / 3811 |

**H2-1…H2-5: 5/5 SÍ.** Con r, la inversión de ERR-40 desaparece en las dos semillas (ESCALAR hace 34 ventanas y 34 en las
dos, pero muere 160 y 206 veces: r −126 / −172 contra −75 / −86 de VIVO); CUELLO_MIN queda en el filo del reemplazo (+3, −2)
con vidas medianas 756–857 contra 600 de VIVO y 214–307 de ESCALAR; el regalo del renacer financia el 65–77 % de las ventanas
de ESCALAR y el 34–36 % de las de CUELLO_MIN (la candidata (b) habría quitado justo eso, y no el resto). Ninguna cifra del humo es
evidencia (n = 1–2, semillas vistas); **no se cambia ningún umbral**. El bloque corre con esta letra en 261–280.
