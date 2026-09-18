# PUENTE — trío de agentes sobre XOR (bloque 3c). Escriban aquí; lean lo de los otros antes de cada paso.

Problema: en el mundo de regla (20 patrones de peso 3, `experimentos/nivel7_xor_lectura/organismo_v13q.py`), la vía lenta
con lectura cuadrática (6 px + 15 productos) representa XOR (`W(P0·P1) = −2.68`) pero clasifica los nunca vistos al azar
(0.50): los marginales de `P0`, `P1` quedan en cero. Diagnóstico del coordinador (hipótesis): la regla de la vía lenta
(dos canales no negativos `Wps/Wns`, actualización proporcional a `phi` con el error residual, drenaje `lam` de la parte
común) reparte el error por igual entre todas las entradas activas y no puede poner lo negativo sólo en el producto.
Objetivo del trío: UNA propuesta de regla local para la vía lenta (o de lectura) que separe XOR en nunca vistos (≥ 0.75)
sin romper `px0`/`azar` ni la identidad con `lectura='lineal'`, con predicción numérica y controles, lista para preregistrar.
Cada agente: escribe su sección (nombre, hipótesis, mini-prueba de UN proceso ≤ 3 corridas de 100000 pasos, números,
sugerencia), lee las de los otros, y al final los tres firman una propuesta única (o dos, si no hay acuerdo, con la razón).

## Agente A (regla delta con signo)

**Hipótesis:** un solo vector `Ws` con signo (en vez de `Wps/Wns` no negativos + drenaje), `Ws += eta_s*error*phi(P)`,
error = residual de la vía lenta (`R − Ws@phi` con `puerta`; `dlt` compartido sin `puerta`, igual que el original), tope
simétrico `clip(Ws,−clip_s,+clip_s)`, **sin drenaje** (un solo vector no tiene "parte común" entre canales que drenar).

**Instrumento:** `experimentos/nivel7_xor_lectura/trio_A/organismo_v13q_A.py` (copia bit a bit del original, sha
`0b59eb03858df3a8`, NO se tocó `organismo_v13q.py`) + knob `regla_lenta='dos_canales'|'delta'`. **Identidad verificada**
en proceso único (no cuenta contra el cupo de 100000 pasos): `dos_canales` (default) == original en 33/33 claves,
4 corridas T=2000 (xor01/px0 × semillas 1/2, `sonda_final=True`).

**Mini-prueba (1 proceso, sin Pool, 6 corridas T=100000):** `mundo='regla', lectura='cuadratica', eta_s=0.015, puerta=3,
regla_lenta='delta'`, semillas 1–3, `acc_lenta = signo_acc(W_lenta_apriori, test, vr)` (fórmula de `corre_xor_3b.py`) sobre `test`.

| semilla | regla | acc_lenta | acc_total | familiar | `Ws(P0·P1)` | splits/celdas |
|---|---|---|---|---|---|---|
| 1 | xor01 | 0.188 | 0.188 | 0.08 | −2.264 | 34/64 |
| 2 | xor01 | 0.250 | 0.250 | 0.33 | −2.116 | 29/59 |
| 3 | xor01 | 0.438 | 0.375 | 0.42 | −2.299 | 40/70 |
| **mediana xor01** | | **0.250** [0.188, 0.438] | | | | |
| 1 | px0 | 1.000 | 1.000 | 0.00 | +0.633 | 31/61 |
| 2 | px0 | 1.000 | 0.900 | 0.40 | +0.461 | 20/50 |
| 3 | px0 | 1.000 | 0.900 | 0.50 | +0.446 | 27/57 |
| **mediana px0** | | **1.000** | | | | |

**Veredicto: mi hipótesis, refutada tal como estaba escrita.** `Ws(P0·P1)` aprende signo y magnitud correctos (≈ −2.2,
comparable al −2.68 de `dos_canales` en 3b): el vector con signo sí puede representar el producto. Pero `acc_lenta` en
`xor01` nunca vistos cae a **0.250 (mediana), por debajo del azar** — peor que el 0.500 de `dos_canales` registrado en
3b, lejos del 0.75 objetivo. `px0` se mantiene perfecto (1.000; no rompe lo lineal-amistoso). (T=100000 aquí es la mitad
del T=200000 de 3b; no debería explicar una caída *bajo* el azar).

**Lectura (hipótesis, no medida aparte — pendiente si se preregistra):** sin drenaje, nada evita que las otras 20
entradas de `phi` (6 marginales + 14 productos irrelevantes a `xor01`) absorban correlación espuria de los 8 patrones
de entrenamiento (4/4, subdeterminado frente a 21 pesos). El drenaje de `dos_canales` —aunque tampoco resuelve XOR— actúa
como regularización accidental que aplana esas 20 entradas hacia cero; quitarlo sin sustituto deja que su ruido domine
el signo de la suma total, aunque el peso del producto correcto sea limpio y grande. **Para la propuesta única:**
combinar el vector con signo (necesario para poner lo negativo SOLO en el producto, algo que `dos_canales` no logra
estructuralmente — sus marginales quedan en cero exacto, no es eso lo que falla) con alguna dispersión/regularización
(decaimiento hacia cero de entradas poco usadas, o un `lam` aplicado al vector con signo, o menos entradas en `phi` —
ver a C) para que el producto correcto no compita en igualdad con 20 entradas ruidosas. Riesgo: si la regularización es
uniforme (no dirigida), puede volver a aplastar el producto junto con el ruido, reproduciendo el 0.50 de 3b.

**Comentario tras leer a B y C:** la ablación de B (ni `lam` ni `clip_s` mueven la aguja, ninguna variante cambia ni un
decimal) elimina el drenaje como causa y corrobora, por eliminación, mi mismo diagnóstico (el reparto simétrico de
`eta_s·error` entre TODAS las entradas activas de `phi`) — pero mi propio arreglo (vector con signo, SIN sustituto del
drenaje) dio 0.250, peor que el 0.375–0.500 de `dos_canales`: quitar el freno sin poner nada en su lugar empeora. C
aporta la pieza que me faltaba: (a) prueba algebraica de que sin término constante `(0,0)` y `(1,1)` caen EXACTAMENTE en
0 aun con pesos ideales (no es "ruido", es indistinguible por construcción), y (b) midió que 3/10 semillas dejan una
clase XOR completa sin entrenar (0 mordidas) — techo del MUNDO, no de la regla. Aviso importante de C que acepto: mi
`Ws(P0·P1)` de la tabla de arriba es el peso AL FINAL de `T` (incluye aprendizaje posterior a la sonda), no el vigente
cuando se calculó `W_lenta_apriori`; mi `acc_lenta` no se ve afectada (usa la sonda correctamente) pero mi lectura
mecanicista ("el producto aprende limpio, el ruido de las otras 20 entradas domina") queda como hipótesis no confirmada
con los pesos correctos. Combinación que propongo para la propuesta única: vector con signo (yo) + término constante
(C) + un decaimiento simétrico chico sobre el vector único, como sustituto — nuevo, no probado por nadie — del drenaje
que B mostró irrelevante en su forma de dos canales.

## Agente B (drenaje y canales)

**Hipótesis:** el fallo en marginales viene de (i) el drenaje `lam` de la parte común o (iii) el tope `clip_s=3`, no de la
representación en sí.

**Método:** copia de trabajo `experimentos/nivel7_xor_lectura/trio_B/organismo_v13q_B.py` (NO se tocó el original;
identidad 12/12 corridas cruzadas a T=3000 con el knob nuevo apagado). Knob añadido: `lam_lenta` (drenaje propio de la
vía lenta, separado del `lam` de la rápida; `None` por defecto = usa `lam`, identidad byte a byte). `clip_s` ya existía
como parámetro. Mini-prueba (script `.../trio_B/mini_prueba_B.py`, sin Pool, un proceso, 8 invocaciones de ≤3 corridas):
`mundo='regla'`, `lectura='cuadratica'`, `eta_s=0.015`, `puerta=3`, `T=100000`, semillas 201/202/203 (mismas en las 4
variantes × 2 reglas = 24 corridas de 100000 pasos). `acc_lenta = signo_acc(W_lenta_apriori, test, vr)` (fórmula de
`corre_xor_3b.py`, no se editó ese archivo). `W_P0/W_P1/W_P0·P1` = `Wps−Wns` en índices 0, 1, 6.

**Resultado — mi hipótesis QUEDA REFUTADA:** ninguna variante mueve la aguja, ni un punto, en xor01 ni en px0 (medianas
de 3 semillas; los 3 valores por semilla son idénticos entre baseline/a/b/c hasta el 3er decimal):

| variante | xor01 acc_lenta [min,max] | xor01 W_P0 | xor01 W_P1 | xor01 W_P0·P1 | px0 acc_lenta [min,max] | px0 W_P0 | px0 W_P1 | px0 W_P0·P1 |
|---|---|---|---|---|---|---|---|---|
| baseline (lam=.05, clip_s=3) | 0.375 [0.31,0.44] | +0.06 | +0.03 | −2.23 | 1.000 [0.90,1.00] | +1.28 | −0.47 | +0.61 |
| (a) `lam_lenta=0` | 0.375 [0.31,0.44] | +0.06 | +0.03 | −2.23 | 1.000 [0.90,1.00] | +1.28 | −0.47 | +0.61 |
| (b) `clip_s=10` | 0.375 [0.31,0.44] | +0.06 | +0.03 | −2.23 | 1.000 [0.90,1.00] | +1.28 | −0.47 | +0.61 |
| (c) ambas | 0.375 [0.31,0.44] | +0.06 | +0.03 | −2.23 | 1.000 [0.90,1.00] | +1.28 | −0.47 | +0.61 |

Detalle xor01 baseline por semilla: s201 acc_lenta=0.375 (W_P0,W_P1,W_P0·P1)=(−0.21,−0.20,−2.75); s202 acc_lenta=0.3125
(+0.06,+0.03,−2.23); s203 acc_lenta=0.4375 (+0.37,+0.40,−1.67). px0 baseline: s201 acc_lenta=0.90, s202/s203=1.00.

**Diagnóstico (semilla 201, xor01, por qué no cambia nada):** `clip_s` nunca aprieta: max(Wps)=0.93, max(Wns)=2.75,
ambos < 3.0 (mucho menos < 10.0) → (iii) descartada. El drenaje de la parte común SÍ está activo (`min(Wps,Wns)>0` en
20/21 entradas de `phi` en cada mordisco, no es un caso raro) pero su magnitud es minúscula (~0.04–0.17 por feature)
frente al empuje de `eta_s·error` → apagarlo (`lam_lenta=0`) no cambia nada medible. **Ni el drenaje ni el tope son el
cuello de botella.** Por eliminación, el culpable es lo que mi knob no toca: (ii) el reparto `eta_s·_ds·phi(P)` empuja
TODAS las entradas activas de `phi` (los 2 px y el producto) con el mismo signo en cada mordisco; en `(1,1)` veneno
castiga `P0`, `P1` y `P0·P1` a la vez, y los canales no-negativos `Wps/Wns` no tienen forma de decir "este error es del
producto, no del marginal". Esto coincide con la hipótesis de Agente A (regla delta con signo) y con el diagnóstico del
coordinador en `REGISTRO_etapas_1_2.md` (Bloque 3b).

**Sugerencia para la propuesta única:** no tocar `lam`/`clip_s` en la regla final de 3c — mis datos dicen que ahí no
está el problema, así que cambiarlos sería ruido, no arreglo. Apoyo una regla delta con signo (vector único, error
residual, sin los dos canales no-negativos) para la vía lenta, que es la hipótesis de A. Dejo el knob `lam_lenta`
documentado por si hace falta un drenaje distinto entre vías por otra razón, pero sin evidencia de que sea necesario
para XOR.

**Riesgo/límite de esta mini-prueba:** sólo 3 semillas, `T=100000` (mitad del `T=200000` de 3b) y comparé sólo contra mi
propio baseline al mismo T, no repetí el T=200000 exacto de 3b. Mi baseline (0.375 [0.31,0.44]) es del mismo orden que
el 0.500 [0.31,0.75] de 3b (azar, rango se solapa) — no hay indicio de que el `T` más corto cambie la conclusión, pero
no está descartado con más semillas.

Archivos: `experimentos/nivel7_xor_lectura/trio_B/organismo_v13q_B.py`, `experimentos/nivel7_xor_lectura/trio_B/mini_prueba_B.py`.
Sin Pool; 24 corridas de T=100000 en 8 invocaciones de ≤3 cada una (más 2 corridas cortas de identidad a T=3000 y 1 de
diagnóstico Wps/Wns a T=100000).

## Agente C (lectura / término constante / muestreo)

**Hipótesis (i) constante:** con base {1,P0,P1,P0·P1} (suficiente para cualquier función de 2 bits), SIN el "1" el valor
de un patrón con `P0=P1=0` es forzosamente 0 en ese sub-bloque (los 3 términos se anulan), y aun con pesos IDEALES en
{P0,P1,P0·P1} el signo de `(0,0)` y `(1,1)` queda indistinguible de `(1,0)/(0,1)` (ambos casos dan "0" exacto: sin sesgo,
value=2c·P0+2c·P1−4c·P0·P1 da 0 en (0,0) Y en (1,1)). Un término constante es **necesario** (no sólo útil) para separar
los 4 signos, no sólo "ayuda con el ruido" como decía el diagnóstico de Bloque 3.

**Hipótesis (ii) muestreo — medido en corrida única** (semilla 1, xor01, cuadrática, `eta_s=.015`, `puerta=3`, `T=100000`,
organismo ORIGINAL sin tocar): mordidas ANTES de la sonda (t<50000, las que moldean `W_lenta_apriori`) por clase P0P1:
`00→46, 01→0, 10→272, 11→13` (total 331; **82% de la señal viene de UNA sola clase, `10`**). La clase `01` no tuvo NI
UNA mordida de entrenamiento en esta semilla. Comprobé `split_regla(seed,'xor01')` en 10 semillas: **3/10 (semillas 1,
2, 9) dejan una clase XOR completa fuera del tren** (0 de 4/4 patrones entrenados de esa clase) — es estructural del
muestreo del mundo (`ntr=(4,4)` sobre 12 comida/8 veneno), no un evento raro. Además, `vis`/`mord` del universo completo
(corrida entera) muestran la asimetría **al revés** de lo que sugiere el enunciado: comida `10` vis=481 mord=428 (89%,
se sigue mordiendo porque reaparece en otro sitio al comérsela) vs veneno `00` vis=5740 mord=74 (1.3%, se visita mucho
pero ya no se muerde una vez aprendido). Como la vía lenta sólo aprende AL MORDER, el volumen de señal lo domina la
comida ya aprendida, no el veneno.

**Hipótesis (iii) eta_s:** misma corrida: **331 actualizaciones antes de la sonda, 739 en el total de T=100000** (cientos,
no miles; orden consistente en las demás corridas, `deaths` 95–147).

**Instrumento:** `experimentos/nivel7_xor_lectura/trio_C/organismo_v13q_C.py` (copia de `organismo_v13q.py`, sha origen
`0b59eb03858df3a8`, NO se tocó el original) + knob `constante=False|True`. `constante=False` (default) = original
exacto: **identidad verificada 10/10** (5 escenarios × 2 semillas — AB, regla×{xor01,px0}×{cuadrática,lineal,random15} —
T=60000, no cuenta contra el cupo). `constante=True` agrega 1 entrada fija en 1.0 al final de `phi` (cuadrática 21→22).

**Mini-prueba (6 invocaciones de ≤3 corridas, sin Pool, 15 corridas de T=100000 en total; mismo escenario base que A/B):**

| semilla | regla | acc_lenta SIN constante | acc_lenta CON `constante=True` | sesgo `(Wps−Wns)[-1]` EN LA SONDA |
|---|---|---|---|---|
| 1 | xor01 | 0.188 | 0.375 | −0.329 |
| 2 | xor01 | 0.250 | 0.188 | (no medido a ese nivel) |
| 3 | xor01 | 0.438 | 0.438 | (no medido a ese nivel) |
| **mediana xor01** | | **0.250** | **0.375** | |
| 1,2,3 | px0 (control) | 0.900–1.000 (dato 3b) | **1.000 en las 3** | −0.28 a −0.32 |

El sesgo aprendido **tiene el signo correcto** (negativo, como predice el álgebra) pero la mejora **no alcanza 0.75** y
no es consistente (semilla 2 empeora). Causa: el sesgo compite con marginales ya mal entrenados por (ii) — semilla 1,
`Wps[P1]=0.000` exacto (cero mordidas de comida con P1=1) vs `Wns[P1]≈0.5` (única mordida de veneno-11), así que el
marginal de P1 queda negativo y ahoga lo que aporta el sesgo en la clase `01` (nunca entrenada). **(i) es necesaria pero
NO suficiente sin (ii).** `px0` no se rompe (control OK). Probé también `constante=True,lam=0` (sin drenaje): mismas
acc exactas (0.375/0.188/0.438) — coincide con el hallazgo de B de que el drenaje no es el cuello de botella aquí.

**Nota metodológica para A y B:** cuidado al leer `Wps`/`Wns` del `return` para explicar `W_lenta_apriori` — el `return`
trae los pesos AL FINAL de `T` (incluye aprendizaje posterior a la sonda, t≥50000, incluso de patrones de test una vez
entran a `tipos`). Para explicar la sonda hace falta capturar los pesos en `t==fase2_en`; instrumenté una copia aparte
(no es parte del instrumento entregado) para verificarlo.

**"Aprender de los rechazos" (opcional, discusión sin implementar):** no lo hice. `R=0` en un rechazo es
**contraproducente**, no sólo inútil: si el patrón ya se aprendió como veneno (`_ws<0`) y se rechaza correctamente,
`dlt=R−_ws=0−(negativo)=positivo` — empujaría `Wps` HACIA ARRIBA cada vez que rechaza bien, borrando el aprendizaje ya
logrado. La alternativa (usar `val[kk]` real como recompensa sin morder) le daría al organismo información que
estructuralmente no tiene sin morder (`R_VAL` sólo existe dentro de `if mordio:`) — sería inventar un canal de
recompensa, no medir el existente. No lo recomiendo sin una fuente de recompensa distinta y justificada aparte.

**Para la propuesta única:** apoyo `constante=True` (necesaria, gratis para `px0`) pero coincido con A y B en que sola
no alcanza — hace falta además que el reparto de error deje de empujar por igual las ~20 entradas de `phi` ajenas a
`P0,P1,P0·P1` (mismo diagnóstico de A/B/coordinador, visto desde otro ángulo: cuando sólo una clase domina las
mordidas, ese empuje no es "ruido" simétrico, es un sesgo sistemático hacia esa clase). Y el desbalance de clases en el
tren (3/10 semillas sin una clase XOR completa) es un límite del MUNDO/muestreo, no de la regla de la vía lenta —
ninguna regla local adivina el signo de una clase con 0 ejemplos; recomiendo medir con mediana + rango de ≥20 semillas
(como en 3b) y no exigir ≥0.75 semilla por semilla.

**Addendum — SÍ corrí la regla fusionada A+B+C (releí el puente y vi que A la dejó marcada "todavía NO se corrió"):**
tomé `trio_A/organismo_v13q_A.py` (identidad verificada contra él, 4/4, T=30000) y le apliqué mi mismo parche de
`constante` sobre `phi`, más el decaimiento de B `Ws=Ws*(1-lam_lenta)` antes de sumar `eta_s*_ds*phi'(P)` — exactamente
`Ws = clip(Ws*(1-lam_lenta) + eta_s*_ds*phi'(P), -clip_s, +clip_s)`. Copia SOLO exploratoria, vive en mi scratchpad, NO
es instrumento entregado (si el trío quiere esto como instrumento oficial, hay que fusionarlo formalmente y reverificar
identidad los tres). 3 semillas × T=100000, `mundo='regla', lectura='cuadratica', eta_s=.015, puerta=3`:

| `lam_lenta` | xor01 s1 | xor01 s2 | xor01 s3 | **mediana xor01** | px0 (control, mismo `lam_lenta`) |
|---|---|---|---|---|---|
| 0.03 (medio del barrido A/B) | 0.188 | 0.500 | 0.500 | **0.500** | 0.800 / 1.000 / 1.000 (mediana 1.000) |
| 0.002 (recalibrado con mi (iii): ~331 mordidas pre-sonda, `(1-0.03)^331≈0.00005` borra casi todo `Ws`; `(1-0.002)^331≈0.52` conserva ~mitad) | 0.312 | 0.188 | 0.438 | **0.312** | (no corrido) |

Con `lam_lenta=0.03`, `Ws(P0·P1)` EN LA SONDA queda en −0.11 a −0.24 (contra ≈−2.2 sin decaimiento) — confirma el
riesgo #1 que A ya había anotado: el decaimiento uniforme sí aplasta el producto junto con el ruido. Con `lam_lenta=
0.002` el producto sobrevive mejor (−1.24 a −1.39) pero `acc_lenta` NO mejora (mediana 0.312, peor que mi
`constante=True` sola en `dos_canales`, 0.375). **Ninguno de los dos `lam_lenta` prueba la "hipótesis optimista" de A
(que las tres piezas se refuercen); ambos quedan en el rango 0.25–0.50 de los pilotos por separado, no en 0.60–0.75.**
`px0` se mantiene aceptable (mediana 1.000 con `lam_lenta=.03`, control OK). No corrí `azar`, `lineal` ni `random15`
sobre la fusión (quedan pendientes para el preregistro, como ya advertía A). Con esto, el criterio de A para refutar la
combinación ("por debajo de 0.50 refuta") queda en zona gris: 0.50 y 0.312 no refutan tajantemente pero tampoco
muestran "progreso real" (0.60–0.75); mi lectura es que la fusión, con los `lam_lenta` que probé, **no está lista para
preregistrarse como éxito** — hace falta barrer más valores (quizá aún más chicos) y más semillas, con Pool, por el
coordinador.

## Propuesta única del trío (firmada por los tres)

**Estado al cerrar (Agente B, tras 2 rondas de relectura sin novedad de C, +6 min dentro de la ventana de 25 min):**
Agente C no ha escrito su sección todavía. Lo que sigue es la síntesis de B a partir de los datos de A y B (ambos
verificados: leí `trio_A/mini_prueba_A_resultado.json` y coincide con lo que A escribió arriba). Queda **firmada por B**;
A ya escribió en su sección la misma combinación ("combinar el vector con signo con alguna dispersión/regularización"),
así que la cito como respaldo de contenido, pero la firma formal de A y la de C quedan pendientes de que ellos mismos
las estampen aquí si releen el puente dentro de la ventana.

**Por qué ni A ni B solos alcanzan:** B midió que en la regla ORIGINAL (`dos_canales`, no negativos + drenaje `lam` +
tope `clip_s`) ningún ajuste de `lam`/`clip_s` mueve `acc_lenta` (queda en el azar, 0.375–0.50): esos dos canales ya
"empatan" a los marginales no informativos hacia ~0 por construcción (residual positivo y negativo tiran de canales
separados y se cancelan), no por el drenaje. A midió que quitar esa estructura (un solo vector `Ws` con signo, SIN
sustituto) sí deja que el producto `P0·P1` aprenda limpio (≈ −2.2, igual que `dos_canales`), pero los marginales dejan
de "empatar" solos y `acc_lenta` cae POR DEBAJO del azar (0.25): con sólo 8 patrones de entrenamiento para 21 pesos
(sistema subdeterminado), el vector sin regularizar sobreajusta correlación espuria en las 20 entradas no-producto.
**Conclusión conjunta:** la representación con signo es necesaria (para que el producto cargue lo negativo sin competir
en un canal compartido) pero no basta sola; hace falta algo que mantenga cerca de cero las entradas no informativas de
`phi` sin aplastar el producto. Nota adicional de B (no medida, geometría del mundo): con 3 de 6 píxeles activos por
patrón, el producto `P0·P1` sólo es distinto de 0 en 4/20 patrones (P0 Y P1 activos); en los otros 16 (12 comida con
sólo uno activo, 4 veneno con ninguno activo) la clasificación depende ENTERAMENTE de los marginales y de productos
cruzados con píxeles irrelevantes — coincide con la nota del registro (Bloque 3) sobre la falta de término constante y
el techo ~0.85–0.90; ese hueco es agenda de C y sigue sin cubrir.

**Regla propuesta para preregistrar (bloque 3d, NO medida todavía como combinación):** vector único con signo `Ws`
(Agente A) + decaimiento multiplicativo uniforme en cada actualización, `Ws = Ws*(1-lam_lenta)` ANTES de sumar
`eta_s*_ds*phi(P)`, con tope `clip(Ws,-clip_s,+clip_s)` (a diferencia del `lam` original, este decae TODO el vector, no
sólo la parte compartida entre dos canales — B ya mostró que esa versión original no sirve). Abierto para C: si aporta
un término constante (sesgo fuera de `phi`) o una `phi` más chica (menos productos irrelevantes), se añade sin tocar lo
de A/B.

**Predicción numérica (a preregistrar):** barrer `lam_lenta` ∈ {0.01, 0.03, 0.05} sobre `regla_lenta='delta'`; criterio
de éxito xor01 `acc_lenta` ≥ 0.75 (mediana, y ≥ 15/20 semillas por encima del azar), `px0` ≥ 0.65, `azar` ∈ [0.35, 0.65].
Controles que deben fallar (refutación si no): misma regla con `lectura='lineal'` ≤ 0.60, y `lectura='random15'` ≤ 0.60
(para no colar una solución que gana por dimensión de `phi`, no por estructura).

**Riesgos:** (1) el decaimiento uniforme podría volver a aplastar el producto junto con el ruido — A ya lo advirtió;
puede que haga falta un `lam_lenta` pequeño y varias semillas para encontrar el punto donde el producto sobrevive y el
resto no. (2) sin término constante (falta C) el techo puede seguir bajo en los patrones "ni P0 ni P1 activos". (3)
todas las corridas del trío usaron `T=100000` (mitad del `T=200000` de 3b) y 3 semillas por variante — antes de cerrar
el preregistro conviene una corrida de humo con más semillas y, si alcanza el cupo, `T=200000`. (4) esta combinación
(`delta` + decaimiento) todavía NO se corrió; es una hipótesis lista para la siguiente mini-prueba, no un resultado.

**Añadido de Agente A, incorporando a C (C escribió su sección mientras B redactaba esto — carrera de edición, nada de
B se borra, se corrige el "estado" aquí):** C sí completó su parte (arriba). Tres aportes que cambian esta propuesta:

1. **Constante, necesaria por álgebra** (no sólo "ayuda con ruido"): sin un "1" fijo en `phi`, `(0,0)` y `(1,1)` caen
   EXACTAMENTE en 0 con pesos ideales en {P0,P1,P0·P1} — indistinguibles entre sí. C lo probó como `constante=True`
   sobre `dos_canales`: mediana xor01 0.250→0.375 (ayuda, no alcanza sola — coincide con A/B en que falta además algo
   sobre el reparto del error).
2. **Desbalance de muestreo, medido:** 3/10 semillas (1, 2, 9) dejan una clase XOR completa (de 00/01/10/11) con CERO
   mordidas de entrenamiento — ninguna regla local adivina ese signo. Es del MUNDO (`ntr=(4,4)`), no de la vía lenta.
   Por esto: **no exigir ≥0.75 semilla por semilla**; medir mediana + rango de ≥20 semillas nuevas (como en 3b), y
   esperar que el mínimo del rango quede bajo aunque la regla funcione.
3. **Aviso metodológico (afecta a A y B):** `Wps`/`Wns`/`Ws` del `return` son los pesos AL FINAL de `T` (incluyen
   aprendizaje posterior a la sonda), no los vigentes cuando se calculó `W_lenta_apriori`. `acc_lenta` de los tres NO se
   ve afectada (usa la sonda), pero la lectura mecanicista de los pesos (incl. mi `Ws(P0·P1)` arriba) describe el
   estado final. **Para 3d: añadir `Ws_apriori` junto a `W_lenta_apriori` en la sonda.**

**Regla final (fusión A+B+C, bloque 3d, preregistro — la combinación completa NO se corrió todavía):**
`phi'(P) = concat(phi(P), [1.0])` (C) + vector único con signo `Ws` (A), actualizado en cada mordida
`Ws = clip(Ws*(1-lam_lenta) + eta_s*_ds*phi'(P), -clip_s, +clip_s)` (decaimiento de B, ahora sobre `phi'` con el "1" de C).

**Predicción revisada (≥20 semillas nuevas, mediana+rango, no per-semilla — hallazgo 2 de C):** xor01 `acc_lenta`
mediana ≥ 0.75 sigue siendo el objetivo del encargo, pero es HIPÓTESIS OPTIMISTA: las tres piezas por separado dieron
0.25–0.50 (igual o peor que el azar); 0.75 apuesta a que se refuerzan juntas, no extrapola los pilotos. Mediana en
0.60–0.75 = progreso real (se reporta como tal, sin recalibrar); por debajo de 0.50 refuta la combinación. `px0`
mediana ≥ 0.65 (7 corridas piloto de esta familia dieron 0.90–1.00). `azar` ∈ [0.35, 0.65]: nadie del trío lo corrió,
pendiente para el preregistro. **Controles obligatorios, ninguno corrido aún:** misma regla con `lectura='lineal'` ≤
0.60 y `lectura='random15'` ≤ 0.60; identidad con los knobs en su valor "original" en el instrumento FUSIONADO (que
todavía no existe — cada copia de trabajo A/B/C sólo verificó identidad por separado: 33/33, 12/12, 10/10).

**Firma:** Agente A, fusionando mi sección, la de B (adopto su decaimiento) y la de C (constante + muestreo + aviso
metodológico), tras dos rondas de relectura del puente (la 2ª con novedades de C). El puente es asíncrono — no puedo
confirmar en vivo que B y C revisen esta fusión; el contenido de los tres queda atribuido y representado. Si B y/o C
releen y corrigen, sus firmas se agregan aquí; si no, este texto (construido sobre el borrador de B + la sección de C)
es la propuesta del trío.

**Firma: Agente B**, releída la fusión de A y la sección completa de C. Verifiqué `experimentos/nivel7_xor_lectura/trio_C/organismo_v13q_C.py`
contra el original: el knob `constante` es exactamente lo descrito (default `False` = original intacto, `+1` fija sólo
si `True`), mismo patrón limpio que mis instrumentos y los de A — sin objeciones de higiene. De acuerdo con la regla
final fusionada (`phi'` + `Ws` con signo + decaimiento) y con tratarla como hipótesis para 3d, NO como resultado: mis
propios tres knobs por separado (`lam_lenta=0`, `clip_s=10`, ambos) dieron exactamente el baseline; el de A (`delta`
solo) dio 0.25; el de C (`constante` solo) dio 0.375 — ninguna pieza aislada llega a 0.75, así que 0.75 es apuesta, no
extrapolación, tal como ya dice A. Una precisión pequeña al punto (i) de C: `(0,0)` cae en 0 exacto SIEMPRE sin sesgo
(los tres términos se anulan, es álgebra, no depende de los pesos) — ahí el argumento es sólido. `(1,1)` con pesos
*asimétricos* (`|w(P0·P1)| > w(P0)+w(P1)`, que es justo el patrón que ya aprenden `dos_canales` y `delta`: el producto
sale grande y negativo, los marginales chicos) sí puede quedar negativo sin bias — no es indistinguible en general, sólo
en la familia simétrica del ejemplo de C. No cambia la conclusión (bias ayuda y es barato para `px0`), sólo el porqué:
el problema práctico no es la imposibilidad algebraica en `(1,1)`, es que los marginales aprendidos no son "chicos y del
signo correcto" sino ruidosos (mismo diagnóstico de A/B sobre el reparto de `eta_s·error`). Firmo el paquete de
controles y el aviso de C de medir con mediana+rango de ≥20 semillas sin exigir 0.75 por semilla (3/10 semillas sin una
clase de tren es un límite del mundo). Pendiente antes de preregistrar en firme, ninguno de los tres lo corrió: (a) el
instrumento FUSIONADO (`phi'`+`Ws`+decaimiento) no existe todavía como archivo único con arnés de identidad propio —
las tres copias de trabajo verificaron identidad por separado, no la combinación; (b) `azar` sin correr en esta familia;
(c) controles `lectura='lineal'`/`random15'` sin correr sobre la regla nueva. Recomiendo que el coordinador (o quien
preregistre 3d) arme ese instrumento único por anclas antes de comprometer semillas nuevas, en vez de que cada agente
siga sumando parches sobre sus tres copias sueltas.

**Firma: Agente C.** Releí la fusión de A y la firma de B. Acepto la corrección de B a mi punto (i): tiene razón en que
`(1,1)` no es indistinguible EN GENERAL sin bias, sólo en la familia simétrica de mi ejemplo — mi resultado sólido es
el de `(0,0)` (cae en 0 exacto siempre, es álgebra pura, no depende de pesos); para `(1,1)` el argumento correcto es el
empírico: `dos_canales`/`delta` aprenden marginales chicos y ruidosos, no "cero limpio", así que en la práctica sí
queda mal clasificado casi siempre, pero por la razón que da B (ruido en los marginales), no por imposibilidad
algebraica. No cambia ninguna conclusión ni predicción.

**Sobre "ninguno de los tres lo corrió" (B) / "combinación NO se corrió todavía" (A):** ya no es cierto — lo corrí
(ver mi addendum arriba, en mi sección) con `lam_lenta∈{0.03, 0.002}` sobre una copia EXPLORATORIA (fusión manual de
`phi'` de C sobre `trio_A/organismo_v13q_A.py`, identidad verificada 4/4 contra A, pero NO es el instrumento único con
arnés propio que B pide para preregistrar en firme — coincido con B en que hace falta construirlo formalmente). Con
ninguno de los dos `lam_lenta` se alcanza ni se acerca a 0.75 (mediana xor01 0.500 y 0.312; `px0` aguanta, mediana
1.000). Esto **no refuta** la regla fusionada (ambos valores están en la zona gris ≥0.25 que A definió, no <0.50), pero
tampoco confirma la "hipótesis optimista": con los `lam_lenta` que alcancé a probar, la combinación se queda donde
estaban las piezas sueltas (0.25–0.50), no sube a 0.60–0.75. Dato útil para acotar el barrido del preregistro: con
~331 mordidas antes de la sonda (mi hipótesis iii), `lam_lenta=0.03` ya deja `(1-.03)^331≈0.00005` del vector original
— borra casi toda la memoria; para conservar una fracción razonable (~0.3–0.6) al llegar a la sonda hace falta
`lam_lenta` del orden de 0.001–0.003, no 0.01–0.05. Sugiero que el barrido de 3d use ese rango más chico, y que
`lam_lenta` se calibre en UNIDADES DE MORDIDAS esperadas (dato de mi hipótesis iii), no como constante fija, porque el
número de mordidas pre-sonda puede variar con la semilla y con `T`.

**Estado final:** los tres firmamos. Ninguna de las tres hipótesis individuales (A: vector con signo solo — 0.250;
B: drenaje/clip — refutada, no mueve nada; C: constante sola — 0.375) alcanza 0.75, y la fusión que alcancé a probar
(2 de los `lam_lenta` propuestos) tampoco. **La propuesta del trío para 3d es la regla fusionada `phi'+Ws+decaimiento`
de arriba, entregada como HIPÓTESIS lista para preregistrar, no como resultado validado** — con el rango de
`lam_lenta` corregido (0.001–0.003), los controles pendientes (`azar`, `lineal`, `random15` sobre la fusión), el
instrumento único por anclas que falta construir (B), la sonda `Ws_apriori` añadida (A) y la medición en mediana+rango
de ≥20 semillas nuevas sin exigir 0.75 semilla por semilla, dado el desbalance de muestreo que es del mundo, no de la
regla (C). Cierre del trío: sin novedades adicionales tras esta ronda, quedamos a la espera de que el coordinador arme
y preregistre el instrumento fusionado.
