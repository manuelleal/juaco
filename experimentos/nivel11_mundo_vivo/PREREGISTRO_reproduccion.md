# PREREGISTRO — PROPÓSITO Y REPRODUCCIÓN COMO MEDIDA (mundo vivo, peldaño 2; línea F)

**Del diseñador del mundo vivo para el coordinador, 18 sep 2026, escrito ANTES de correr nada con `Pool` y ANTES del
humo** (las predicciones del humo van en §10 y se escribieron antes de lanzarlo). Misión: llegar a la AGI por este
camino — un organismo mínimo con reglas locales, sin retropropagación en el runtime, que aprende y sobrevive en un
mundo con necesidades, propósito y reproducción; el método manda sobre el cómo.

Origen: decisión del director (F) del 18-sep 06:10 ("algo como viviente con necesidades distintas, propósito,
reproducción, aprendizaje"); `PREREGISTRO_mundo_vivo.md` §7 (propósito y reproducción "primero como medida"); nota del
cronista (HANDOFF §15.8.6): *"`descendientes_viables`, predicción VIVO > UNA_NEC > BARAJA_POL, sin mecanismo"*.
Estado del núcleo del que parte: replicado en dos series (181–200, 201–220): `xor01` necesidad × estímulo 1.0 en 20/20
contra 0.5 de los controles; supervivencia con la enmienda 2 (ERR-37): A₁₂ 0.90–1.00, agua 1.85–2.05 ×.

**Instrumento:** `organismo_vivo_rep.py` (construcción v1 **ed31d9b989b93307**, la del humo; construcción final
**aa823d56c2d4213c** = v1 + el control CUELLO_MIN de la enmienda 1, §12, bit a bit igual a v1 en todo lo demás: arnés,
caso H), construido POR ANCLAS por `construye_vivo_rep.py` (final **693826b02c03b848**, 12 inserciones, ninguna nombra al
rng) desde `organismo_vivo.py` (20c0961c79de8825, que aquí SÓLO SE LEE; a su vez construido desde el tronco congelado
`organismo/organismo_v14.py` v14.1 feefc88b1fd8d434). Ningún archivo existente se edita. Arnés: `identidad_vivo_rep.py`
(resultado en §11). Runner: `corre_vivo_rep.py` (`--humo` de un proceso; `Pool` sólo lo ejecuta el coordinador).

---

## 1. Las dos preguntas, en orden

**Q1 — Reproducción como MEDIDA (sin construir nada que actúe).** ¿Sirve una cifra que integre supervivencia sostenida
en las DOS necesidades para ordenar organismos y brazos? Si no ordena como la supervivencia ya medida, se tira.

**Q2 — Propósito como TERCERA NECESIDAD (el mecanismo mínimo, con las piezas que ya existen).** ¿Una fila más de valor
—"reproducirse"— cuyo cuerpo es el cuello de botella del organismo, que manda sólo cuando las dos primarias callan y
que consume recursos al cumplirse, **cambia la conducta del organismo saciado** y **produce más descendientes viables**
que el mismo organismo sin ella? ¿Y lo hace por lo que esa fila APRENDE, o bastaría con enrutar la boca a las filas que
ya existen (control CUELLO, que puede ganar)?

---

## 2. La medida: `descendientes_viables`

**Definición.** Una *ventana de viabilidad* son `rep_X` pasos **seguidos** con `E ≥ rep_umbral` **y** `Ag ≥ rep_umbral`
(las dos necesidades en o sobre el punto de saciedad). Cada ventana completa, no solapada, cuenta **un descendiente
viable** (`descendientes`). La ventana se rompe si cualquiera de las dos baja del umbral o el cuerpo muere.
Medidas compañeras, todas de sólo lectura: `pasos_viables` (pasos con las dos ≥ umbral; continua, nunca censurada),
`desc_q` (descendientes por cuarto), `t_desc` (instantes), y la **tabla de la boca ESTANDO SACIADO**: `sac_dec[k]`
(decisiones de la boca sobre el estímulo `k` con las dos necesidades ≥ umbral) y `sac_mord[k]` (mordidas);
`sac_tasa[k] = sac_mord/sac_dec` sólo si `sac_dec ≥ 20`.

**Parámetros fijados por argumento, no por barrido.** `rep_umbral = 1.0`: es el punto de saciedad del tronco
(`hambre = clip(1 − E, 0, 1)` vale 0 en o sobre 1.0); "saciado en las dos" = los dos déficits en 0, sin constante nueva.
`rep_X = 500 = (1.5 − 1.0) / costo`: lo que tarda un cuerpo lleno (1.5, el tope) en volver al punto de saciedad; una
ventana de 500 pasos **obliga a volver a comer y a beber estando ya saciado** — mide provisión sostenida, no un bocado
afortunado. Con `T = 100 000` el máximo es 200 descendientes.

**Por qué es honesta.** No toca el rng, no cambia una decisión ni un peso: con `rep_coste = 0` es un contador (arnés,
casos C1–C4: las claves viejas salen bit a bit). Integra supervivencia, aprendizaje y las dos necesidades en una cifra
que se puede comparar entre brazos y, mañana, entre organismos.

**Qué se hereda: NADA (un solo brazo de herencia; se eligió 1 de los ≤ 2 permitidos).** El descendiente se **cuenta**,
no se instancia. Razones: (i) en este mundo hay un solo cuerpo y su memoria sobrevive a la muerte ("muerte sin olvido"),
así que *W heredado* (lamarckiano) es indistinguible de *el padre sigue viviendo*: no mediría nada nuevo; (ii) *código
heredado* (`KW`, `activa`) exige un segundo cuerpo en su propio anillo, es decir el **mundo de población**
(`mundo_vivo_pob.py`, no construido: exige `Pool` y una hipótesis propia — emergencia del punto 14 del brief y selección
sobre el organismo entero — que es el cambio de paradigma que el director dejó escrito, no este peldaño). La herencia
lamarckiana ya está medida en Etapa 4 (heredar el valor ahorra el 80 % del veneno inicial). Aquí se mide primero si la
**moneda** vale.

---

## 3. El mecanismo mínimo: la tercera necesidad ("reproducirse")

Todo con las piezas que ya existen: filas de valor por necesidad, consecuencia vectorial del bocado, necesidad activa
por déficit, mapa de recompensa `ΔS > 0 → +1, < 0 → −3, 0 → 0`, "un encuentro enseña a todas las necesidades".

| pieza | hambre (fila 0) | sed (fila 1) | **reproducirse (fila 2, nueva)** |
|---|---|---|---|
| variable del cuerpo | `E` | `Ag` | **`S₂ = min(E, Ag)`**, el cuello de botella |
| componente del bocado | `ΔE` | `ΔAg` | **`ΔS₂ = min(E′, Ag′) − min(E, Ag)`**, leída del propio cuerpo antes y después del bocado (con el mismo tope 1.5) |
| recompensa de su fila | +1 / −3 / 0 | ídem | ídem (mismo mapa) |
| déficit | `clip(1 − E)` | `clip(1 − Ag)` | `clip(1 − min(E, Ag)) = max(hambre, sed)`: **nunca supera a las primarias** |
| cuándo manda en la boca | si es el mayor déficit | ídem | **sólo cuando las dos primarias callan** (`E ≥ 1` y `Ag ≥ 1`): desempate de prioridad, local |
| satisfacción | comer | beber | **la ventana completa** (`rep_X` pasos con las dos ≥ umbral) = un descendiente |
| coste al cumplirse | — | — | **`rep_coste` de E y de Ag** (0.4 y 0.4: lo que cuesta un bocado de veneno más uno de sal, la moneda de daño que el mundo ya tiene) |

**Por qué el déficit es el del cuello de botella y no `1 − G` (la reserva).** Si la tercera necesidad tuviera déficit alto
cuando la reserva está vacía, la boca de v14 mordería cualquier cosa (`Vb = α·W + 2·déficit + 0.5`; enmienda 1 del mundo
vivo: *el impulso tapa el valor cero*). El propósito debe entrar **por el valor**, no por el impulso: cuando manda, su
déficit es 0 y la boca lee sólo lo que la fila 2 aprendió.

**Qué sabe hacer y qué no, escrito antes de medir.** La fila 2 está indexada por estímulo, no por cuál recurso es el
cuello: aprende la **mezcla** de sus consecuencias. Punto fijo de Rescorla-Wagner: `W₂[k] ≈ E[R₂ | bocado de k]`.
Comida: +1 si `E < Ag` al morder, 0 si no → **W₂[A] ∈ [+0.3, +0.9]** (la fracción de bocados de comida con la energía
de cuello). Agua: simétrica, **W₂[C] ∈ [+0.3, +0.9]**. Sal: −3 siempre que `Ag − 0.4 < E` (casi siempre) →
**W₂[D] ∈ [−3.0, −1.5]**; veneno simétrico, **W₂[B] ∈ [−3.0, −1.5]**. Con eso, la boca saciada (déficit 0) da
`pb ≈ 0.98` a comida y agua y `pb ≤ 0.02` a sal y veneno.
**La conducta que cambia es UNA: saciado, rechaza lo que daña al recurso más escaso.** Hoy VIVO saciado lee la fila del
hambre (desempate) donde la sal vale 0.0 y **muerde la sal el 84 % de las veces** (`Vb = 0.5 → pb = 0.841`): se bebe la
reserva de agua que acababa de llenar. **Lo que NO cambia y no se predice:** *"deja de comer al saciarse"* —la boca de
v14 no puede vetar un valor positivo ni uno cero, y la comida saciado es inútil (tope 1.5) pero inocua; el organismo con
propósito **sigue mordiendo comida y agua saciado**, sólo deja de morder sal y veneno. "Acumula" significa aquí: no
gasta lo acumulado, no que planifique.

**Control que puede ganar: CUELLO.** Saciado, la boca lee la fila del recurso más escaso (`E ≤ Ag → hambre; si no → sed`).
Sin fila nueva, sin aprendizaje nuevo. Rechaza la sal sólo cuando el agua es el cuello (la fila de la sed la tiene en −3);
cuando la energía es el cuello lee la fila del hambre y la muerde. Si rinde lo mismo que la tercera fila, **la tercera
fila sobra** y lo que se declara es el enrutamiento, no una necesidad.

**Local y sin planificador:** todo lo nuevo lee el cuerpo en el paso presente (`E`, `Ag`, su mínimo, su cambio con este
bocado); nada mira al futuro, nada simula, nada usa gradiente. Memoria nueva: una fila de valor (`Wp/Wn` 90 + `Wps/Wns` 6
por fila), un contador de ventana, tres contadores de lectura.

---

## 4. Brazos (un cambio por brazo; presupuesto del cuerpo del bloque anterior: `costo = costo_a = 0.001`)

| brazo | perillas sobre `organismo_vivo_rep` | qué mide |
|---|---|---|
| **VIVO** | 2 necesidades, 4 estímulos + medida (`reproduccion=1, rep_mide=1, rep_coste=0`) | la línea base: conducta idéntica a `organismo_vivo` (arnés C1), sólo se cuenta |
| **UNA_NEC** | mismo cuerpo, 1 necesidad en la mente + medida | validez de la medida (cronista) |
| **ESCALAR** | `val_esc=1` + medida | ídem |
| **BARAJA_CON** | `nec_shuf=2` + medida | ídem |
| **BARAJA_POL** | `nec_shuf=1` + medida | ídem: el conocimiento intacto con la política barajada |
| **REP_SIN_COSTE** | `n_nec=3, rep_nec=1`, `rep_coste=0` | **el mecanismo sin pagar**: ¿cambia la conducta y rinde? |
| **REP** | `n_nec=3, rep_nec=1`, **`rep_coste=0.4`** | **el mecanismo pagando**: ¿sostiene la reproducción cuando cuesta? |
| **CUELLO** | `n_nec=2, rep_cuello=1` | enrutar a la fila del recurso más escaso (control; su defecto se vio en el humo, §12) |
| **CUELLO_MIN** | `n_nec=2, rep_cuello=2` | **la alternativa que puede ganar** (enmienda 1, ERR-39, §12): saciado, el mínimo de las dos filas |

`T = 100 000` (regla 6; la mini y las dos series del núcleo son de 100 000 y así siguen comparables).
Referencia interna: VIVO con la medida es `organismo_vivo` VIVO bit a bit en todas las claves viejas (arnés C1), así que
las cifras del núcleo (xor01, tabla 2 × 4, muertes) deben salir iguales a las de 181–220 en distribución.

---

## 5. Semillas y subconjunto preregistrado (regla 10)

**221–240 primera serie; 241–260 réplica.** Diagnóstico estructural ANTES de correr (`diagnostico_codigos.py --desde 221
--n 40`; construye `KW` y lee los códigos, no simula un paso): **221–240 no tiene ningún alias sal==veneno, pero la
semilla 236 tiene alias sal==agua** (`|code(D) ∩ code(C)| = 3`: para la vía rápida el agua y la sal son el mismo
estímulo; en la fila de la sed reciben +1 y −3 sobre el mismo código, es decir **conflicto de signo**, el caso para el
que nació la división de v11); **241–260 tiene la 260 con alias sal==veneno** (el caso conocido de ERR-37/bloque de la
sal: la sal hereda el miedo al veneno y VIVO la rechaza también saciado, lo que ACHICA la diferencia con REP).
- **Criterio de validez, fijado aquí:** una semilla es **ALIAS** si cualquiera de `|D∩A|, |D∩B|, |D∩C|, |C∩A|, |C∩B|`
  vale 3 (= K); si no, **LIMPIA**. 221–240: ALIAS {236}; 241–260: ALIAS {260}. Lo recalcula el runner al arrancar.
- **Se reporta SIEMPRE el conjunto completo y, al lado, las LIMPIAS (19/20) con los mismos umbrales.** El conjunto
  completo manda. El alias de código NO se arregla aquí (lo lleva el creador B).

---

## 6. Predicciones numéricas y refutación (escritas antes del humo y del bloque)

Estadística, con las lecciones de ERR-37: **`descendientes`, `pasos_viables`, `muertes` y `sac_tasa` son integrales de
trayectoria → NO se parean por semilla**: se comparan distribuciones con **A₁₂ = P(x > y) + ½ P(x = y)** sobre los 400
pares, la **razón de medianas** y los **cuartiles** (`statistics.quantiles(n=4)`, *exclusive*). Se parea por semilla
**sólo lo aprendido** (tabla de la fila 2, `xor01`, celdas estrictas). Ningún umbral se coloca en la mediana esperada del
propio efecto; ningún criterio usa `max` sobre lecturas. Un `None` (tasa con < 20 decisiones; razón con mediana 0) nunca
cuenta como victoria: se reporta y decide A₁₂.

| # | predicción (221–240) | de dónde sale | refutación |
|---|---|---|---|
| **P-R1** | **La medida ordena como la supervivencia** (predicción del cronista): A₁₂(`desc` VIVO > UNA_NEC) ≥ 0.70; A₁₂(UNA_NEC > BARAJA_POL) ≥ 0.80; A₁₂(VIVO > ESCALAR) ≥ 0.70; A₁₂(VIVO > BARAJA_CON) ≥ 0.70 | supervivencia ya medida: A₁₂ muertes 0.90–1.00; BARAJA_POL muere ×3.8 | cualquiera < 0.50 → **la medida no mide viabilidad y se tira**; entre 0.50 y el umbral → "ordena débilmente", se reporta |
| **P-R2** | **Conducta saciado — la sal**: mediana de `sac_tasa[D]`: VIVO **≥ 0.60**; REP_SIN_COSTE **≤ 0.25**; REP **≤ 0.25**; A₁₂(REP_SIN_COSTE < VIVO) **≥ 0.90** | ecuación de la boca: `W = 0 → pb 0.84`; `W ≤ −1 → pb ≤ 0.07`; el 0.25 deja margen para el periodo de aprendizaje | REP_SIN_COSTE ≥ 0.40 → la fila 2 no veta la sal: **el mecanismo no cambia la conducta** |
| **P-R3** | **Rendimiento sin pagar**: `desc` REP_SIN_COSTE contra VIVO: A₁₂ **≥ 0.75** y razón de medianas **≥ 1.5**; `pasos_viables`: A₁₂ ≥ 0.75, razón ≥ 1.3 | cada bocado de sal saciado cuesta 400 pasos de agua; VIVO lo da el 84 % de las veces | A₁₂ ≤ 0.60 → la conducta no se vuelve viabilidad sostenida (diagnóstico: P-R8, la sal rechazada inunda el anillo) |
| **P-R4** | **Pagando**: `desc` REP ≥ **0.5 ×** REP_SIN_COSTE (razón de medianas) **y** A₁₂(REP > VIVO) **≥ 0.60** | ciclo con coste ≈ resaciarse (100–300 pasos) + 500, contra 500 + holgura sin coste → ≈ 0.7 | A₁₂(REP > VIVO) < 0.50 → **pagar lo deja peor que no tener propósito**; 0.50–0.60 → no concluyente, réplica |
| **P-R5** | **Occam (CUELLO)**: `desc` A₁₂(REP_SIN_COSTE > CUELLO) **≥ 0.65**; `sac_tasa[D]`: A₁₂(REP_SIN_COSTE < CUELLO) ≥ 0.75 **y** A₁₂(CUELLO < VIVO) ≥ 0.75 (orden REP < CUELLO < VIVO); mediana CUELLO ≤ 0.50 | CUELLO rechaza la sal sólo con el agua de cuello (≈ la mitad de las veces) | A₁₂(REP_SIN_COSTE > CUELLO) ≤ 0.55 en `desc` → la tercera fila sobra frente a este enrutamiento. *(Letra original; el humo mostró que CUELLO falla por el veneno invisible, §12: se reporta pero ya no decide.)* |
| **P-R5b** | **Occam, el control que puede ganar (CUELLO_MIN; enmienda 1, ERR-39)**: **decide** `desc` A₁₂(REP_SIN_COSTE > CUELLO_MIN) **≥ 0.65**; CUELLO_MIN veta la sal como REP (mediana `sac_tasa[D]` ≤ 0.25, sin orden predicho); la firma de la tercera fila: `sac_tasa[A]` y `sac_tasa[C]` A₁₂(REP_SIN_COSTE > CUELLO_MIN) **≥ 0.75** | la fila 2 da +0.5 a comida y agua (`pb` 0.98); la lectura pesimista da 0 (`pb` 0.84): más provisión saciado | A₁₂ ≤ 0.55 en `desc` → **la tercera fila sobra**: se declara *"saciado, leer las dos necesidades y quedarse con la peor"*, no una necesidad; 0.55–0.65 → no concluyente, réplica |
| **P-R6** | **Seguridad / regresión dentro del bloque**: en REP y REP_SIN_COSTE `xor01` (filas 0–1) = 1.0 en ≥ 18/20, celdas estrictas 4/4 en ≥ 18/20, `exp_tabla` mediana ≤ 1.5 × VIVO; muertes: A₁₂(REP_SIN_COSTE < VIVO) ≥ 0.50 (no muere más); REP ≤ 1.5 × VIVO (razón de medianas) | el núcleo replicado (20/20 × 2); el coste 0.4/0.4 por descendiente | `xor01` cae en > 2 semillas → **la tercera fila interfiere con las primarias** (la hija hereda filas; la fisión) y el mecanismo cuesta conocimiento |
| **P-R7** | **La tabla de la fila 2 (lo aprendido; pareable)**: `W_nec[2]` final con **A ≥ +0.3, C ≥ +0.3, B ≤ −1.0, D ≤ −1.0** en ≥ 18/20 (REP_SIN_COSTE) y ≥ 18/20 (REP); magnitudes predichas A, C ∈ [0.3, 0.9], B, D ∈ [−3.0, −1.5] | punto fijo `E[R₂ ∣ k]` (§3) | > 2 semillas con signo equivocado o |W| bajo el umbral → **el cuello de botella no es aprendible con una fila indexada por estímulo** (la mezcla se anula) |
| **P-R8** | **Coste en el mundo (trampa 3 acotada)**: `exposiciones[D]` de REP_SIN_COSTE ≤ **3 ×** VIVO y `exposiciones[A]` ≥ **0.7 ×** VIVO (medianas) | lo rechazado se queda en el anillo (×7 en el bloque de la sal con evitación total; aquí sólo saciado) | > 3 × y < 0.7 × → la sal rechazada roba llegadas de comida; P-R3 se lee **neto** de ese coste, y "acumula sin pagar" sería falso |

**Regresión del tronco (como P8 del bloque anterior):** el tronco y `organismo_vivo` no se tocan (sólo se leen); el
runner verifica los dos shas al arrancar y aborta si cambiaron. **Identidad dentro del runner** (5 casos × 3 semillas:
apagada ≡ `organismo_vivo`; cadena ≡ `organismo_v14`; medida de sólo lectura; tercera necesidad ≠; CUELLO ≠): si no es
15/15, no corre nada.

**Qué se declara si pasa todo (y sólo entonces):** *"con una tercera fila de valor cuyo cuerpo es el cuello de botella
min(E, Ag) y que manda sólo cuando las dos primarias callan, el organismo saciado rechaza lo que daña al recurso más
escaso, sostiene más ventanas de viabilidad (descendientes viables) que el mismo organismo sin ella —también pagando
cada una— y no pierde la tabla necesidad × estímulo; leer las filas existentes, incluso la peor de las dos, no basta"*.
Si P-R5b cae (la tercera fila sobra), se declara sólo el enrutamiento pesimista, que es un mecanismo más barato y también
local. Si P-R1 cae, se tira la medida y con ella todo lo demás.

---

## 7. Las cuatro trampas (regla 5 de `EQUIPO.md`) y la propia

1. **Canal simétrico** — n/a (no hay canal). La tabla de la fila 2 tiene dos positivos y dos negativos por construcción.
2. **Acierto sin balancear** — no se usa acierto: `sac_tasa` se reporta por estímulo, nunca agregada; `xor01` sigue
   siendo el balanceado del bloque anterior.
3. **El mundo que se come la comida** — es **la** amenaza de este diseño: rechazar la sal saciado la deja en el anillo
   (el mundo sólo la retira al 0.3 % por paso). Por eso P-R8 la acota y todas las tasas van por decisión, no por paso.
4. **Sitios fijos que se memorizan** — `spawn()` sortea; la ventana se define por el cuerpo, no por el sitio.
5. **Propia, declarada:** *el propósito disfrazado de desempate.* Si la ganancia viniera de leer OTRA fila saciado (y no
   de lo que la fila 2 aprende), CUELLO rendiría igual (P-R5). Y si viniera de un impulso, la fila 2 con déficit 0 no
   podría producirla (§3). **Segunda propia:** *el coste que no se paga.* Comparar `desc` de REP (pagado) con VIVO (sin
   pagar) es desfavorable a REP a propósito: por eso están los dos brazos, REP y REP_SIN_COSTE, y P-R4 los liga.

---

## 8. Lo que NO se declara (cláusula)

No se dirá que el organismo *quiere*, *tiene propósito*, *se reproduce* (nada nace: el descendiente es un contador),
*planifica* ni *acumula para* (nada mira al futuro). "Necesidad de reproducirse" es la etiqueta de la fila 2, como
"hambre" lo es de la fila 0. Vocabulario permitido si el criterio lo respalda: *tercera necesidad con cuerpo en el cuello
de botella*, *saciado rechaza lo que daña al recurso más escaso*, *ventanas de viabilidad / descendientes viables*,
*paga el coste*. La medida `descendientes_viables` es una moneda para ordenar, no una propiedad viviente.

---

## 9. Coste y entregables

9 brazos × 20 semillas × 100 000 pasos = 180 corridas ≈ 2–7 min de pared con `Pool(14)` (el humo midió 8.8 s por
corrida de 100 000 con la máquina cargada; el bloque anterior: 140 corridas en 5 min), más 15 comprobaciones de identidad
de 2 × 20 000 pasos. Réplica 241–260 igual. Entregables:
`construye_vivo_rep.py`, `organismo_vivo_rep.py`, `identidad_vivo_rep.py`, `corre_vivo_rep.py`, este preregistro, y el
humo (`datos/vivo_rep_humo_*.{log,json}`).

Orden: 1) constructor → 2) arnés (§11) → 3) preregistro (este) → 4) humo de un proceso (§10) → 5) bloque 221–240
(coordinador, `Pool`) → 6) réplica 241–260 si algún veredicto queda a ±1 semilla del umbral (regla 12) y, en todo
caso, antes de declarar nada.

---

## 10. Humo (UN proceso, 6 corridas de T = 100 000: VIVO s1 y s2, REP_SIN_COSTE s1 y s2, REP s1, CUELLO s1) — predicciones ANTES de lanzarlo

n = 1–2 y semillas ya vistas (1, 2): **no son evidencia**; sólo dicen si la medida es legible y si el bloque vale la pena.
- **H-1** la medida no es degenerada: `desc` de VIVO ∈ [1, 150] en 2/2 (ni cero ni saturada: el máximo es 200).
- **H-2** `desc` REP_SIN_COSTE > VIVO en 2/2 (misma semilla).
- **H-3** `sac_tasa[D]`: VIVO ≥ 0.60 y REP_SIN_COSTE ≤ 0.25 en 2/2.
- **H-4** `W_nec[2]` de REP_SIN_COSTE con signos {A +, B −, C +, D −} y |W| ≥ 0.3 en 2/2.
- **H-5** `desc` REP ≥ 0.5 × REP_SIN_COSTE (semilla 1).
- **H-6** `sac_tasa[D]` de CUELLO entre la de REP_SIN_COSTE y la de VIVO (semilla 1).
**Si H-1 falla** (medida degenerada), se escribe una **enmienda con ERR-39** que cambie `rep_X` por
argumento ANTES del `Pool`; si fallan H-2..H-6, el bloque se corre igual con esta letra (el humo no recalibra umbrales:
sólo decide si vale la pena) y el fallo queda escrito aquí.

---

## 11. Arnés de identidad (`identidad_vivo_rep.py`, un proceso, T = 20 000, semillas 1–2) — resultado

**Construcción v1 (ed31d9b989b93307): 42/42.** Apagada ≡ `organismo_vivo` en 13 escenarios × 2 semillas (los seis brazos
del bloque anterior, el ancla V14, `vivo=0` base e invertido, predictor vectorial encendido, linaje v13, sin puerta, y el
escenario con TODAS las `rep_*` encendidas y la maestra apagada): 26/26. Cadena ≡ `organismo_v14` (`vivo=0, n_nec=1`, base
e invertido): 4/4. Medida de sólo lectura (`reproduccion=1, rep_coste=0`) en VIVO, UNA_NEC, ancla V14 y BARAJA_POL: claves
viejas bit a bit y exactamente las 7 nuevas, 8/8; las 9 claves que dependen del flujo del rng idénticas (9/9): **el rng no
se consume ni apagada ni con la medida**. Controles que deben fallar (tercera necesidad; CUELLO): 4/4 difieren. (F)
informativo: con `rep_coste = 0.4` difiere si y sólo si hubo descendientes (5 y 5 en 20 000 pasos): coherente 2/2.
**Construcción final (aa823d56c2d4213c): 52/52** (`datos/vivo_rep_identidad_20260918.log`) = los 42 anteriores repetidos
íntegros + (E2) CUELLO_MIN ≠ `organismo_vivo` 2/2 + (H) **identidad entre construcciones**: la final es bit a bit la v1 en
VIVO + medida, REP_SIN_COSTE, REP con coste y CUELLO (8/8) → el humo de registro (v1) vale para la construcción final.
Comprobación del instrumento CUELLO_MIN a T = 20 000 (no es humo): s1 descendientes 13, viable 0.587, muertes 12 [5, 7],
tasa saciado 0.886 / 0.005 / 0.778 / 0.002; s2 descendientes 14, viable 0.581, muertes 14 [5, 9], tasa 0.800 / 0.002 /
0.769 / 0.004. A ese ritmo (≈ 65–70 por 100 000) queda codo a codo con REP_SIN_COSTE (60 y 44): P-R5b puede caer.

---

## 12. Humo (18 sep 09:00, `datos/vivo_rep_humo_20260918_090014.{log,json}`, sha del JSON 8468c1681b346d22; instrumento v1) y ENMIENDA 1 — **ERR-39**, escrita DESPUÉS del humo y ANTES del bloque

Identidad dentro del runner 10/10. Seis corridas de 100 000 pasos, un proceso (8.6–9.1 s cada una con la máquina cargada):

| brazo | s | desc | viable | muertes [E, agua] | saciado tasa A/B/C/D | W fila 2 (A B C D) | xor01 | exposiciones A/B/C/D |
|---|---|---|---|---|---|---|---|---|
| VIVO (OFF: sólo la medida) | 1 | 14 | 0.328 | 89 [58, 31] | 1.00 / 0.00 / 0.84 / **0.78** | — | 1.00 | 778 / 5531 / 840 / 1922 |
| VIVO (OFF) | 2 | 17 | 0.334 | 103 [52, 51] | 1.00 / 0.00 / 0.84 / **0.75** | — | 1.00 | 831 / 5096 / 843 / 2224 |
| REP_SIN_COSTE (ON) | 1 | **60** | 0.574 | 68 [32, 36] | 0.97 / 0.01 / 0.98 / **0.01** | +0.47 −0.99 +0.54 −1.68 | 1.00 | 571 / 4354 / 562 / 2957 |
| REP_SIN_COSTE (ON) | 2 | **44** | 0.475 | 93 [43, 50] | 0.94 / 0.01 / 0.98 / **0.01** | +0.75 −1.87 +0.56 −1.81 | 1.00 | 520 / 4503 / 588 / 3068 |
| REP (ON, paga 0.4/0.4) | 1 | **54** | 0.457 | 107 [40, 67] | 0.97 / 0.01 / 0.94 / **0.01** | +0.49 −1.30 +0.39 −1.72 | 1.00 | 541 / 4151 / 562 / 3585 |
| CUELLO (control) | 1 | 4 | 0.323 | 92 [30, 62] | 0.91 / **0.27** / 0.93 / 0.26 | — | 1.00 | 969 / 3749 / 976 / 3865 |

**H-1…H-6: 6/6 SÍ.** La medida es legible (VIVO 14 y 17 de un máximo de 200), la tercera fila cuadruplica y triplica los
descendientes en las dos semillas, veta la sal saciado (0.01 contra 0.78/0.75), aprende la tabla con los signos predichos,
y pagando conserva el 90 % (54/60). Ninguna cifra del humo es evidencia (n = 1–2, semillas vistas).

**ERR-39 — el control de Occam CUELLO estaba mal escrito, y el humo lo enseña.** Al leer UNA sola fila
primaria saciado, el daño del otro recurso vale 0 en esa fila: cuando el agua es el cuello, la fila de la sed no ve el
veneno, y CUELLO **muerde veneno saciado el 27 %** (columna B), muere más y produce 4 descendientes. No es la alternativa
más fuerte a la tercera fila; con él P-R5 se ganaría por la razón equivocada. **La alternativa fuerte, escrita ahora:
CUELLO_MIN** (`rep_cuello = 2`) — saciado, la boca lee el **mínimo de las dos filas primarias** (la lectura pesimista):
rechaza lo que daña a cualquiera de las dos, bebe y come con `W = 0` (`pb = 0.84`); sin fila nueva, sin aprendizaje
nuevo, sin rng (con la puerta encendida `_wt` sólo entra en la boca; por eso exige puerta). Comprobación del instrumento
a T = 20 000 (no es humo): descendientes 13, viable 0.587, tasa saciado A/B/C/D 0.886 / 0.005 / 0.778 / 0.002 — **veta sal
y veneno como la tercera fila y produce descendientes al mismo ritmo**: es un control que de verdad puede ganar.
- **Cambios (ninguno de umbral):** se añade el brazo CUELLO_MIN (9 brazos, 180 corridas); CUELLO se conserva con su letra
  y P-R5 queda como estaba (se reporta); **P-R5b**, la que decide si la tercera fila aporta: **(i) `desc` A₁₂(REP_SIN_COSTE
  > CUELLO_MIN) ≥ 0.65** (≤ 0.55: *la tercera fila sobra* — el propósito saciado es leer las dos necesidades y quedarse
  con la peor, y eso es lo que se declara); (ii) CUELLO_MIN veta la sal como REP: mediana `sac_tasa[D]` ≤ 0.25, **sin**
  orden predicho entre los dos (copiar aquí "REP < CUELLO_MIN en sal" habría sido un criterio vacío, detectado en la
  prueba lógica del runner antes del bloque); (iii) la **firma** propia de la tercera fila es el valor **positivo**
  aprendido de comida y agua (≈ +0.5 → `pb` 0.98) frente al 0 de la lectura pesimista (`pb` 0.84): `sac_tasa[A]` y
  `sac_tasa[C]` A₁₂(REP_SIN_COSTE > CUELLO_MIN) ≥ 0.75. Con (i) y (iii) REP_SIN_COSTE debería ganar por poco (más
  provisión saciado); es la predicción **más probable de caer** de todo el bloque, y caer aquí es un resultado limpio.
- **Notas sin cambio de umbral (lecturas declaradas antes del bloque):** (a) **P-R7, casilla B**: el humo dio −0.99 en
  s1 (umbral −1.0). El punto fijo del veneno en la fila 2 es más lento porque el veneno casi no se muerde después de los
  primeros bocados; se mantiene la letra; si P-R7 cae **sólo** por B con B ≤ −0.5 en ≥ 18/20, la lectura preregistrada es
  *"la fila 2 aprende la tabla salvo la magnitud del veneno, que muerde pocas veces"* y **no** se declara la tabla
  completa. (b) **P-R8, comida**: el humo dio 0.73 y 0.63 × (umbral 0.7). Un organismo saciado más tiempo come menos y
  muerde menos objetos, así que el anillo se renueva menos: menos llegadas de comida no es que el mundo lo mate de
  hambre (viable 0.57 contra 0.33). Se mantiene la letra: si cae, P-R3 se lee neto, como ya dice P-R8. (c) La tercera
  fila con coste muere más por agua en s1 (67 contra 31): P-R6 lo acota a 1.5 × en muertes totales (1.2 en el humo);
  se reporta por necesidad.
- **Humo de registro:** no se repite con la construcción final; el arnés (caso H) prueba que la final es bit a bit la v1
  en los cuatro brazos que el humo corrió, y CUELLO_MIN sólo entra con `rep_cuello = 2`.

**Nota del coordinador (18 sep 09:15):** el número provisional ERR-38 de esta enmienda pasa a **ERR-39** (ERR-38 ya estaba asignado a la batería de generalización copiada sin eta_s/clip_s). Ningún umbral cambia.
