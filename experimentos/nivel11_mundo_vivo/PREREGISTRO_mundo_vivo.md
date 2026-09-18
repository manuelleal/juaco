# PREREGISTRO — MUNDO VIVO (nivel 11): dos necesidades, cuatro estímulos

**PREREGISTRO (commiteado 18 sep 07:50, antes de correr; el veredicto de XOR ya está: línea cerrada) del diseñador para el coordinador** (18 sep 2026). Nada de esto se ha corrido con `Pool` ni se declara.
Origen: `registro/PLAN.md`, decisión del director (F) del 18-sep 06:10. Misión: AGI por este camino; el método manda.
Instrumento: `experimentos/nivel11_mundo_vivo/organismo_vivo.py`, construido **por anclas** desde el tronco congelado
`organismo/organismo_v14.py` (**v14.1**, `feefc88b1fd8d434`, sólo lectura) por `construye_vivo.py`. Arnés:
`identidad_vivo.py` (**37/37**). El tronco pasó de v14 a v14.1 a las 05:55, mientras se construía esto: el
instrumento se reconstruyó por anclas contra el tronco nuevo y el arnés se repitió entero.

---

## 1. Hipótesis

**H1 (lo que compra el mundo vivo).** Si el estado interno es un **vector** (energía, agua) y la mordida tiene
consecuencia **vectorial** `ΔS = (ΔE, ΔAgua)`, entonces **un mismo encuentro enseña a las dos necesidades a la vez**:
el bocado de comida enseña "alimenta" al eje de hambre **y** "no quita la sed" al eje de sed, con la misma mordida y
sin ninguna exposición extra. La tabla completa 2 × 4 se aprende en el mismo número de exposiciones *por estímulo*
que la tabla 1 × 2 de v14.

**H2 (el XOR natural).** El significado depende del estado: *el agua vale con sed y no vale sin sed*. La tabla
verdad de "¿vale la pena morder?" sobre {hambre, sed} × {comida, agua} es (1, 0, 0, 1). **Eso es XOR (paridad), no un
sesgo:** no existen `a_necesidad + b_estímulo` que la produzcan (restando las dos ecuaciones diagonales sale
`a₀ − a₁ = +1` y `a₀ − a₁ = −1`). El organismo la resuelve **no aprendiéndola**: la resuelve porque su memoria de valor
está **indexada por la necesidad**, es decir, el término de interacción está en la memoria y no en el lector.

**H3 (dos muertes).** Con dos necesidades que bajan solas y dos muertes posibles, la segunda necesidad **en la mente**
paga en supervivencia: el mismo cuerpo con una sola necesidad representada muere de sed.

**Qué NO se afirma.** Que el organismo "entienda" el estado, que resuelva el XOR de la línea 3 (píxeles: sigue
abierta y cerrada por dinámica), ni que esto sea planificación. Vocabulario permitido: *aprende por necesidad*,
*el valor depende del estado*, *sobrevive a dos muertes*.

---

## 2. Mecanismo mínimo y memoria que exige

| pieza | v14 | mundo vivo | memoria nueva |
|---|---|---|---|
| estado interno | `E` escalar | `(E, Ag)`, cada uno con su descenso y su muerte | 1 float |
| estímulos | 2 (A comida, B veneno) | 4 = los **cuatro patrones que ya existen** (A comida, B veneno, C agua, D sal) | 0 (no cambia la retina) |
| consecuencia | `ΔE` escalar, `R ∈ {+1, −3}` | `ΔS = (ΔE, ΔAg)`, `R_n = +1 / −3 / 0` según el signo de `ΔS_n` | 0 |
| impulso | `hambre = clip(1−E)` | déficit de la necesidad **activa** (la mayor) | 0 |
| boca | valor del patrón | valor del patrón **en la fila de la necesidad activa** | 0 |
| valor | `Wp, Wn ∈ ℝ⁹⁰`, `Wps, Wns ∈ ℝ⁶` | los mismos, con **una fila por necesidad** | ×`n_nec` |
| sorpresa | predictor de `ΔE` (bloque 6) | predictor de `ΔS` **vectorial**; sorpresa **por necesidad** | ×`n_nec` |

**Por qué el valor debe ser por necesidad y no un escalar con la necesidad como contexto.** Porque la consecuencia
de la mordida es un vector: el error es un vector, y un escalar por celda no tiene dónde poner la componente de la
necesidad que no está activa. Con un escalar, lo que el cuerpo aprendió sobre el agua mientras tenía hambre se
escribe encima de lo que aprendió sobre la comida: la memoria promedia lo que el mundo separa. Ésa es exactamente la
predicción que distingue el diseño de su alternativa, y por eso **`val_esc = 1` (un escalar por celda, la necesidad
sólo como contexto del impulso) es un brazo del bloque y puede ganar**: si gana, el diseño está mal escrito.

**La tercera vía, descartada con razón medida: el código conjuntivo.** La alternativa clásica sería meter la
necesidad en la retina (dos píxeles más) para que el código de Kenyon sea de (patrón × necesidad) y el valor siga
siendo un escalar por celda. Se descarta por dos motivos, en este orden: (1) **rompe el ancla de identidad** — cambia
`KW` de (90, 6) a (90, 8) y con ello `rng.uniform(0,1,(NK,6))`, es decir, el consumo del rng desde el primer paso, y el
mundo vivo dejaría de poder compararse bit a bit con v14 (sería implementable sin tocar el rng con un `Generator`
propio `seed+700000`, como en `v13s`, pero entonces la proyección de la necesidad no sería del mismo linaje que la de
los píxeles); (2) **cuesta celdas**: cada estímulo pasaría a tener `n_nec` códigos distintos y el pool de 90 celdas es
el techo ya medido de la composición (creador B, 18-sep). El valor por necesidad cuesta memoria (`n_nec ×` los pesos)
y **cero celdas**. Queda escrito como brazo alternativo `nec_retina`, **no construido**.

---

## 3. Ancla de identidad (la exigencia central)

**Con una sola necesidad (hambre) y dos estímulos (comida/veneno) el mundo vivo es `organismo_v14` BIT A BIT**, con el
mismo consumo del rng y las mismas claves de salida. **Es alcanzable y está alcanzado** (`identidad_vivo.py`, un
proceso, T = 20000, semillas 1–3): **37/37**, 12 casos, incluido el control que debe fallar. Cómo:

1. **Ninguna línea nueva consume el rng del organismo.** El único `Generator` nuevo (control barajado) es propio
   (`seed+900000`) y sólo se crea si la perilla está encendida (convención de `v13s`).
2. **El único sorteo que dependería del mundo nuevo es `spawn()`**: `rng.integers(len(tipos))`. Con dos estímulos
   `len(tipos) = 2`, exactamente como v14 → mismo stream. Por eso los cuatro estímulos son **los cuatro patrones que
   ya existen**: no cambia la retina, ni `KW`, ni el bucle de rechazo de `cond()` (que sólo restringe `code(A) & code(B)`).
3. **El eje de energía del mundo vivo ES el de v14**: `EFECTO['comida'][0] == E_VAL['comida']`,
   `EFECTO['veneno'][0] == E_VAL['veneno']`, y el mapa `ΔS_n > 0 → +1`, `< 0 → −3` reproduce `R_VAL`.
4. **La segunda muerte es imposible con `vivo = 0`**: `Ag = A_ini = 1.0` y su drenaje está guardado.
5. `Wp` pasa de `(90,)` a `(n_nec, 90)`: con `n_nec = 1` se lee `Wp[0]`, la misma vista 1-D, las mismas operaciones
   elemento a elemento, los mismos dobles IEEE.

Los casos **(I)** y **(J)** son la lectura literal del encargo: **toda la maquinaria del mundo vivo encendida**
(`vivo = 1`, consecuencia vectorial, dos muertes, drenaje, contadores) con **una** necesidad y **dos** estímulos →
todas las claves de v14 salen bit a bit; lo único que aparece son 10 claves nuevas de **sólo lectura**.

---

## 4. Brazos y controles (un cambio por brazo; semillas nuevas, 20 semillas en el bloque real)

| brazo | qué cambia | para qué |
|---|---|---|
| **V14** | `vivo=0, n_nec=1` | ancla: ≡ tronco, dentro del runner |
| **VIVO** | 2 necesidades, 4 estímulos | el mundo vivo |
| **UNA_NEC** | el **mismo cuerpo** (dos drenajes, dos muertes) con **una** necesidad en la mente | qué compra la segunda necesidad |
| **ESCALAR** (`val_esc=1`) | un solo valor por celda; la necesidad, sólo contexto del impulso | **la alternativa que puede ganar** |
| **BARAJA_POL** (`nec_shuf=1`) | se baraja *qué necesidad cree la boca que está activa* | qué compra la política |
| **BARAJA_CON** (`nec_shuf=2`) | se baraja *qué componente de ΔS enseña a cada necesidad* | **el control decisivo**: el contenido lo es todo |
| **NO_INFORMA** (`tabla`) | la sal no informa a nadie (ΔE = ΔAg = 0) | un estímulo sin consecuencia no se aprende nunca |
| *(alternativa, no construida)* `nec_retina` | la necesidad como dos píxeles más | código conjuntivo; rompe el ancla (§2) |

**Presupuesto del cuerpo, decidido antes de correr y con argumento (no por barrido):** v14 gasta `costo = 0.002` por
paso en un eje y la mitad de los objetos son comida; con dos ejes y cuatro estímulos la comida baja al 25 %. Para no
confundir *"el mundo vivo no funciona"* con *"el mundo vivo mata de hambre"*, **se conserva el gasto total del cuerpo
y se reparte**: `costo = costo_a = 0.001`. Es la única constante que se mueve respecto del tronco.

---

## 5. Predicciones numéricas y cláusulas de refutación

Medidas (todas en `mini_vivo.py`, definidas antes de ver datos):
`exp_hasta[n][s]` = **exposiciones** (llegadas al objeto) hasta que el valor que la boca leería para la necesidad `n`
cruza `|v| ≥ 0.5` con el signo que obliga la física del mundo · `exp_tabla` = máximo sobre las 4 celdas informativas ·
`xor01` = **acierto balanceado** (2 positivos, 2 negativos) del predicado "vale la pena morder" (`v > 0.3`) en
{hambre, sed} × {comida, agua} contra (1, 0, 0, 1) · `contraste` = media de las dos diferencias de **tasa de mordida**
de la misma imagen entre necesidades · `muertes_nec` = [por energía, por agua].

| # | predicción | refutación |
|---|---|---|
| **P1** | `xor01` de VIVO **≥ 0.75** en ≥ 15/20 semillas (mediana ≥ 0.875) | < 0.75: el valor por necesidad no basta; el mundo vivo no da el XOR |
| **P2** | `xor01` de ESCALAR **≤ 0.60** y ESCALAR < VIVO en ≥ 16/20 (pareado) | ESCALAR ≥ VIVO: **el valor debe ser escalar**; el diseño está mal escrito y se reescribe |
| **P3** | `xor01` de BARAJADA **≤ 0.60**; `contraste` ≤ 0.05 | barajar no destruye: la necesidad no es lo que indexa; es otra cosa |
| **P4** | `contraste` conductual de VIVO **≥ 0.15** en ≥ 15/20 | < 0.15: sabe el valor y no cambia de conducta → fallo de política, no de aprendizaje (regla 4) |
| **P5** | **tabla completa**: las 4 celdas informativas cruzan criterio en ≥ 18/20, con `exp_tabla` **≤ 3 ×** las exposiciones que v14 necesita para su celda más lenta (B) | > 3 ×, o alguna celda censurada en ≥ 5/20: "un encuentro informa a las dos" es falso; cada necesidad paga su propio muestreo |
| **P6** | **NO_INFORMA**: la sal nunca cruza criterio (censurada 20/20) y `|W| ≤ 0.3` en las dos necesidades | si aparece valor, hay una fuga (crédito por vecindad de código) y se busca antes de seguir |
| **P7** | **UNA_NEC muere de sed**: `muertes_nec[1]` ≥ 3 × la de VIVO, pareado ≥ 16/20 | no muere más: la segunda necesidad no compra supervivencia; el mundo no aprieta y hay que endurecerlo |
| **P8** | **regresión**: `bateria_v14.py 6` y `bateria_generaliza.py organismo_v14 20 --desde 101` intactas (el tronco no se toca; el mundo vivo es copia) | cualquier caída: el paquete se detiene |

**Predicciones de la mini-prueba (3 semillas, T = 100000, un proceso), escritas antes de correrla** — son el humo
que decide si el bloque de 20 semillas vale la pena, y **no** sustituyen a P1–P8:
**MP-1** VIVO `xor01` ≥ 0.75 en 3/3 · **MP-2** ESCALAR `xor01` ≤ 0.60 en ≥ 2/3 · **MP-3** BARAJADA `contraste` ≤ 0.05
en ≥ 2/3 · **MP-4** las 4 celdas informativas de VIVO cruzan criterio en 3/3, `exp_tabla` ≤ 100 ·
**MP-5** UNA_NEC muere de sed más que VIVO en 3/3.

---

## 6. Las cuatro trampas conocidas (regla 5 de `registro/EQUIPO.md`), revisadas en este diseño

1. **Canal simétrico.** El análogo aquí es la tabla necesidad × estímulo: se eligió deliberadamente **simétrica**
   (cada necesidad tiene su `+` y su `−`, con las mismas magnitudes +0.8/−0.4 y +1/−3) para que el `xor01` sea
   balanceado por construcción y ningún brazo pueda ganar por el desequilibrio de clases. La asimetría que queda
   —el veneno cuesta −3 y la comida +1— es la del tronco y se hereda a propósito.
2. **Acierto sin balancear.** `xor01` es **acierto balanceado** con 2 positivos y 2 negativos; nunca se reporta la
   proporción cruda de aciertos. Las tasas de mordida se reportan por celda, no agregadas.
3. **El mundo que se come la comida (muestreo asimétrico).** Sigue viva y **empeora** con cuatro estímulos: lo
   mordido desaparece y reaparece, lo rechazado se queda. Por eso todas las medidas se reportan **por exposición**, no
   por paso, y el JSON trae `exposiciones[A|B|C|D]`: si un estímulo se encuentra 5 × más que otro, el número de
   exposiciones hasta criterio lo corrige y la comparación entre celdas sigue siendo legible. Control:
   `exposiciones` de VIVO no debe diferir más de 3 × entre estímulos; si difiere, se reporta y se discute.
4. **Sitios fijos que se memorizan.** `spawn()` sortea posiciones en todo el anillo, como v14. El análogo nuevo es
   **"resolver el XOR sin mirar el estímulo"**: si la necesidad activa estuviera correlacionada con qué objeto hay
   cerca, la conducta correcta saldría del estado interno solo. Lo cubre BARAJADA (si el estado interno bastara,
   barajar la necesidad **no** destruiría el contraste) y, en el bloque real, la lectura de `xor_enc`: las cuatro
   celdas necesidad × estímulo deben tener ≥ 20 encuentros cada una.

**Trampa nueva, propia de este mundo (declarada aquí):** *el impulso disfrazado de conocimiento*. Con déficit alto la
boca muerde cualquier cosa (`hambre_boca = 2.0`, el mecanismo de v14 para poder revertir). El contraste conductual
debe medirse con los déficits emparejados —la necesidad activa es siempre la mayor, así que las dos condiciones tienen
un impulso comparable— y, en el bloque real, condicionando a `déficit ∈ [0.3, 0.7]`. Si no se hace, **una diferencia de
sed se leería como conocimiento del agua**.

---

## 7. Propósito y reproducción (cómo se mediría primero; qué mecanismo después)

**Primero como MEDIDA, sin construir nada.** El mundo vivo ya da la única moneda honesta: **energía acumulada**.
Se define `descendientes_viables` = ⌊(∫ max(E − E_umbral, 0) dt) / C_hijo⌋ con `E_umbral = 1.0` (el excedente sobre la
saciedad, no la energía total) y `C_hijo` fijado a priori como el coste de 100 000 pasos de mantenimiento
(`C_hijo = 100000 × (costo + costo_a) = 200`). Es un **contador de sólo lectura**, no cambia el rng ni la conducta, y
se puede añadir al instrumento en una línea. Sirve para ordenar brazos y organismos con una sola cifra que integra
supervivencia, aprendizaje y las dos necesidades: un organismo que aprende y no muere acumula excedente; uno que
sobrevive al filo, no. **Predicción que ya se puede escribir:** VIVO > UNA_NEC > BARAJADA en `descendientes_viables`,
con el mismo orden que en supervivencia — si el orden se invierte, la medida no mide lo que dice y se tira.

**Después como MECANISMO, cuando la medida esté replicada.** El mínimo que no rompe nada: al cruzar
`descendientes_viables` de 1 a 2, nace **una copia del organismo** que hereda `KW`, `activa` y las filas de valor con
un olvido `olvido_hijo` (la perilla de la Etapa 4, ya medida), en un anillo propio, y el padre paga `C_hijo` de
energía. Dos cosas —y sólo dos— se miden entonces: si la población acumula algo que un individuo no alcanza en una
vida (criterio de emergencia del punto 14 del brief: propiedad ausente en el individuo, presente en el grupo, no
programada, reproducible, que desaparece al romper la estructura), y si la **selección sobre el organismo entero**
encuentra constantes que el diseño no encontró (es la salida que el director dejó escrita para el criterio de parada
del 04:55). **No se construye ahora**: exige población y `Pool`, y el frente abierto es aprender sin morder.

---

## 8. Entregables y orden de ejecución propuesto al coordinador

1. `construye_vivo.py` → `organismo_vivo.py` (hecho; por anclas, tronco sólo leído).
2. `identidad_vivo.py` → **37/37** (hecho; se re-corre si cambia numpy).
3. `mini_vivo.py` (hecho; 3 semillas, un proceso) → decide si el bloque vale la pena.
4. **Bloque real** (coordinador, `Pool`): 20 semillas nuevas, los 6 brazos, P1–P8, + réplica en un rango virgen si
   algún veredicto queda a ±1 semilla del umbral (regla 12).
5. Sólo después: `descendientes_viables` como contador, y la discusión de reproducción.

---

## 9. Mini-prueba (3 semillas, T = 100000, un proceso) — RESULTADO y ENMIENDA 1

Corrida con `mini_vivo.py` (`mini_vivo_salida.json`) **después** de escribir MP-1…MP-5 y las predicciones P1–P8.
Ancla dentro del runner: 2/2. Instrumento `organismo_vivo.py` sobre el tronco **v14.1** (`feefc88b1fd8d434`; el tronco
se movió a v14.1 a las 05:55, mientras se construía esto: el instrumento se reconstruyó por anclas y el arnés se
repitió, **37/37**).

| brazo | `xor01` | contraste | `exp_tabla` (celdas) | muertes [energía, agua] |
|---|---|---|---|---|
| **VIVO** | **1.00** (3/3) | 0.07 | **9** (4/4) | **89** [52, 37] |
| UNA_NEC | 0.50 | — | — (2/4) | 141 [52, **97**] |
| ESCALAR | 0.50 | 0.01 | — (2/4) | 160 [66, 94] |
| BARAJA_POL | 1.00 | 0.08 | 7 (4/4) | **361** [188, 181] |
| BARAJA_CON | **0.25** | −0.01 | 9 (4/4, transitorias) | 175 [86, 89] |
| NO_INFORMA | 1.00 | 0.08 | — (3/4; la sal nunca cruza) | 34 [33, **0**] |

Tabla de valor de VIVO (mediana de 3, idéntica semilla a semilla): hambre {A +1.0, B −3.0, C 0.0, D 0.0} ·
sed {A 0.0, B 0.0, C +1.0, D −3.0}. **Es la tabla 2 × 4 exacta que el diseño predice**, con 7/2/9/3 exposiciones.
ESCALAR: {A +0.15, C +0.43} en su única fila — **la memoria promedia lo que el mundo separa**, y le va peor que a
UNA_NEC (160 contra 141 muertes): con dos necesidades, un valor escalar es **peor que no tener la segunda necesidad**.

- **MP-1 SOSTENIDA** (1.00, 3/3) · **MP-2 SOSTENIDA** (0.50 ≤ 0.60, 3/3) · **MP-4 SOSTENIDA y más fuerte de lo
  predicho** (`exp_tabla` 9 ≪ 100) · **MP-5 SOSTENIDA en dirección** (sed: 97 contra 37, **2.6 ×**, no 3 ×).
- **MP-3 REFUTADA, y el fallo era del control, no del mundo** → **ERR candidato (a numerar por el coordinador,
  el último del registro es ERR-32): el control "necesidades barajadas" estaba mal escrito.** Barajar *qué necesidad
  cree la boca que está activa* (`nec_shuf=1`) **no** destruye la tabla: cada fila sigue recibiendo su propia
  componente de `ΔS`, así que el contenido sobrevive intacto (`xor01` 1.00) y lo que se destruye es la conducta
  (361 muertes, 4 × VIVO). El control que el diseño necesita baraja **el contenido**: qué componente de `ΔS` enseña
  a cada necesidad (`nec_shuf=2`). Con él, `xor01` cae a **0.25** (bajo el azar) y la tabla se vuelve puré
  ({0.30, 0.39, 0.74, 0.61}). El instrumento se corrigió (dos modos), el arnés se repitió (37/37) y **los dos
  modos quedan como controles distintos con lecturas distintas**: `nec_shuf=1` mide qué compra la política,
  `nec_shuf=2` mide qué compra el contenido.

### Enmienda 1 (escrita ANTES de la serie de 20 semillas; cada cambio con su ERR candidato)

1. **P3 se desdobla** (ERR del punto anterior): **P3a** `nec_shuf=2` (contenido) → `xor01` ≤ 0.60 **y** por debajo de
   VIVO en ≥ 18/20; si no cae, lo que produce la tabla no es la necesidad y el diseño está refutado.
   **P3b** `nec_shuf=1` (política) → muertes ≥ 2 × VIVO en ≥ 16/20; `xor01` **no** se predice que caiga.
2. **P4 (contraste conductual ≥ 0.15) queda REFUTADA por la mini-prueba y se sustituye** — ERR candidato:
   *el impulso tapa el valor cero*. Medido: el organismo muerde casi todo (tasas 0.90–1.00 en las cuatro celdas)
   porque `Vb = α·W + 2·déficit + 0.5`; con `W = 0` y déficit ≈ 0.5 sale `pb ≈ 0.99`. **Un valor de cero no puede
   vetar a la boca de v14: sólo un valor negativo (como el −3 del veneno) la frena.** Es un fallo de *política*, no
   de aprendizaje (regla 4), y era la trampa nueva declarada en §6, que **se cumplió**. Sustituto (**P4'**):
   la conducta se mide por **supervivencia**, que es donde el valor por necesidad sí manda: muertes de VIVO ≤ 0.75 ×
   UNA_NEC y ≤ 0.70 × ESCALAR, pareado ≥ 16/20; y muertes por agua de VIVO ≤ 0.5 × UNA_NEC.
   *(El contraste conductual por estímulo vuelve sólo si se añade un coste de la mordida inútil, que sería un
   mecanismo nuevo: queda fuera de este bloque, escrito como candidato `c_boca`.)*
3. **P5 se endurece** (ERR candidato: *la primera cruzada puede ser transitoria*): en BARAJA_CON las cuatro celdas
   "cruzan criterio" (`exp_tabla` 9) y sin embargo terminan en puré. Por tanto **una celda sólo cuenta si además
   termina con el signo correcto**; con esa regla BARAJA_CON tiene 0/4 y VIVO 4/4. `exp_tabla` se reporta siempre
   junto al valor final de la celda.
4. **P7 pasa de 3 × a 2 ×** (ERR candidato: umbral escrito sin dato; la mini da 2.6 ×): muertes por agua de UNA_NEC
   ≥ 2 × las de VIVO, pareado ≥ 16/20.
5. **La trampa 3 (el mundo que se come la comida) está CONFIRMADA y excede la cota que este preregistro se puso**
   (≤ 3 ×): exposiciones A 831 / B 5253 / C 843 / D 2017 → el veneno se encuentra **6.3 ×** más que la comida,
   porque lo rechazado se queda en el anillo y lo mordido desaparece. **No invalida las medidas** —`exp_hasta`
   cuenta exposiciones *a ese estímulo* y es inmune al desequilibrio entre estímulos— pero **sí obliga** a que
   ninguna medida agregada sobre estímulos entre en el bloque, y se reporta la tabla de exposiciones siempre.
6. **NO_INFORMA (P6) SOSTENIDA**: la sal muda nunca cruza criterio (3/3 censurada) y termina en `|W| ≤ 0.0` en las
   dos necesidades. Efecto lateral medido y esperable: sin sal que deshidrate, el eje de agua es pura ganancia y las
   muertes por sed caen a 0 → el brazo **no** es comparable en supervivencia, sólo en aprendizaje.
7. **Coste medido del mundo vivo** (no estaba predicho, se registra): la celda hambre × comida tarda **7**
   exposiciones en VIVO contra **4** en UNA_NEC/ESCALAR. Es interferencia real: la fila de hambre también recibe
   `R = 0` de cada bocado de agua y sal, que comparten píxeles con la comida en la vía lenta. **Predicción nueva
   para el bloque (P9):** ese coste se mantiene por debajo de 2 × (VIVO ≤ 2 × UNA_NEC en `exp_hasta[hambre][A]`,
   mediana de 20); si crece con el número de estímulos, el mundo vivo compra necesidades y paga en velocidad.


## Nota del coordinador (18 sep 2026, 07:50; escrita ANTES de correr)

El veredicto de XOR ya está (línea cerrada 07:47), así que este bloque corre ahora con la enmienda 1 del diseñador tal cual (sus
cuatro fallos corregidos antes de proponer) y sin ningún cambio de criterio. Semillas 181–200; réplica automática en 201–220 si
algún veredicto queda a ±1 semilla del umbral (regla 12). Un `Pool` a la vez.

**Aclaración del coordinador (07:55, ANTES de correr, sin cambiar umbrales):** P5 dice "su celda más lenta (B)"; la celda más lenta de V14 es A
(4 exposiciones) y no B (3). Se lee P5 como "la celda más lenta de V14, sea cual sea" (= A); el runner calcula las dos lecturas y marca la
contradicción; la lectura que decide es la de la celda más lenta real. Error de redacción, no de criterio. P8 (regresión del tronco) no la
corre el runner porque el tronco no se toca (el sha de origen se verifica al arrancar). T = 100000 (el preregistro no fijaba T; los umbrales
son razones entre brazos y cruces tempranos).
