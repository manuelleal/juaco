# INFORME 2 — Red de células vivas: techo justo, segunda capa, códigos, tramposo, olvido (1-oct-2026, exploración, SIN preregistro)

**NO en lo central, HAY ALGO MODESTO en lo lateral.** Contra un techo justo (Adam + entropía cruzada) la red de células ya no gana ni en aprender (550 vs 412–525 exposiciones) ni en readaptarse (887 vs 225: pierde 4×); con células que alimentan células, ninguna de las tres formas de aviso supera a capas CONGELADAS al azar + boca, y con 3 capas o más dejan de aprender; ningún código de entrada hace generalizar a pares no vistos a nadie, ni al techo; y no apareció una forma barata de no olvidar A al aprender B (sólo un canje). Lo modesto: **el tramposo a 320 células se elimina con pago por CAMINO (grupos de 4) o con impuesto a la emisión constante sin perder nada de aprendizaje (27 → 0 tramposas; readaptación 0.60 → 1.00)**, y eso sí conecta con la hipótesis del bien público.

Misión: llegar a la AGI por este camino. Carpeta `PROYECTOS\JUACO\investigacion_20261001\red_celulas\`: `red2.py` (red de capas, tres avisos, impuesto, camino, consolidación; techo justo `MLP2`), `corre2.py` (`--exp techo|capas|codigos|codigos_largo|tramposo|olvido`), tablas en `datos\e2_*.txt`, crudos por semilla en `datos\e2_*.json`. INFORME.md (informe 1) no se tocó. CPU de este encargo ≈ 10 min. Semillas 1–10 (techo, olvido) o 1–5 (capas, códigos, tramposo); mediana [mín–máx].

## 1. Techo justo (Paso 0): la ventaja del informe 1 desaparece
Perceptrón de 40 ocultas, retropropagación + Adam + entropía cruzada, 4 tasas, 10 semillas, mismo flujo que las células:

| | exp. hasta 0.9 (A) | exp. hasta 0.9 (B, readapt.) | A tras B |
|---|---|---|---|
| Adam lr 0.003 / 0.01 | 1637 / 787 | 800 / 250 | 0.13 |
| Adam lr 0.03 | 525 [450–600] | **225 [175–300]** | 0.13 |
| Adam lr 0.1 | **412 [350–525]** | 325 | 0.13 |
| células 1 capa (informe 1) | 550 [450–800] | 887 [500–1800] | 0.15 |

De la ventaja 4.6× queda **0 (empate)**; de la 1.6× en readaptar queda **una desventaja de 3–4×**. El rival del informe 1 era débil. Única cosa que queda: costo por exposición (6 276 vs 15 859 operaciones: Adam cuesta 2.5× por paso) → costo total hasta 0.9 ≈ 3.5 M vs 6.5 M, y eso sin contar que en readaptar el techo gasta menos.

## 2. Segunda capa: células que alimentan células (suma mod 7, one-hot, SIN lectura directa; la boca sola falla: 0.50)
Tres avisos hacia atrás, todos sin cálculo global: **cadena** (recibo la señal de aprendizaje de cada célula que alimenté, pesada por mi axón), **fa** (igual pero pesada por una "oreja" fija al azar: sin transporte de pesos), **rpe** (ningún error baja: la célula sólo recibe PAGO de energía por el camino, predice el pago y aprende de su propio error de predicción del pago). Tasas de 2 capas elegidas viendo 2 semillas (entrada 0.03, axón intermedio 0.01: con las del informe 1 el axón intermedio y el aviso se realimentaban y los pesos llegaban a 1e30 a las 500 exposiciones; se puso TOPE al aviso, como el techo por canal de JUACO). 5 semillas, acierto en vistos y exposiciones hasta 0.9:

| profundidad (capas de 40) | CONGELADAS + boca | cadena | fa | rpe | TECHO Adam |
|---|---|---|---|---|---|
| 1 | 1.00, 1025 | 1.00, 900 | 0.97, 1075 | **0.17, nunca** | 1.00, 800 |
| 2 | **1.00, 400** | 0.97 [0.33–1.00], 612 (4/5) | 0.73, 1150 | 0.13, nunca | 1.00, 475 |
| 3 | **1.00, 400** | 0.13, nunca | 0.27, nunca | 0.17, nunca | 1.00, 475 |
| 4 | **1.00, 375** | 0.13, nunca | 0.20, nunca | 0.17, nunca | 1.00, 625 |

Lectura sin adornos: (i) la mejor red de células a cualquier profundidad es la que NO aprende en las capas ocultas (rasgos al azar apilados + boca con regla delta); (ii) el aviso en cadena aguanta 2 capas (frágil: 1 de 5 semillas en 0.33) y **deja de aprender con 3**; fa ya se degrada con 2; rpe (sólo energía, sin error de arriba) **no aprende ni con 1 capa**: el pago es una señal demasiado pobre para orientar pesos; (iii) el techo aprende a cualquier profundidad. En paridad de 3 bits con sólo 6 células (donde las congeladas sí fallan, 0.62) la cadena llega a 1.00 en 1 de 3 semillas y el techo en 3 de 3 (barrido de 24 combinaciones de tasas, nada mejor que 1/3; log del chat).

## 3. Generalizar a lo no visto: nadie, con ningún código
Códigos declarados (conocimiento a mano): **binario** (3 bits por número), **termómetro** (6 bits), **ángulos4** (cos, sin de cada número: prior "los números viven en un círculo", sin productos ni resta colada). Acierto en los 19 pares retenidos (azar 0.14), 5 semillas:

| código | células 1 capa | células 2 capas | techo 40 | techo 40-40 | techo 40-40, 30 000 exposiciones |
|---|---|---|---|---|---|
| one-hot | 0.00 | 0.05 | 0.00 | 0.00 | 0.00 |
| binario | 0.00 (vistos 0.67) | 0.21 (vistos 0.13: no aprendió) | 0.00 | 0.05 | 0.05 [0.05–0.16] |
| termómetro | 0.11 (vistos 0.17) | 0.11 (no aprendió) | 0.00 | 0.00 | — |
| ángulos4 | 0.05 (vistos 0.63) | 0.11 [0.00–0.16] (vistos 0.90) | 0.05 | 0.11 [0.05–0.16] | 0.05 [0.05–0.16] |

Ninguno pasa del azar, ni el techo con 10× más exposiciones. Con 30 de 49 pares, sin regularización ni miles de pasadas (grokking), la suma mod 7 no se extrapola; el código componible no basta. Las células además aprenden PEOR los vistos con binario/termómetro (0.67 / 0.17) que el techo (0.93). Dato que sí vale: con ángulos4 las células de 2 capas aprenden los vistos (0.90) donde 1 capa no (0.63): la segunda capa multiplica, pero no generaliza.

## 4. El tramposo a escala (320 células con vida, 5 semillas)

| brazo | A vistos | N fin | **tramposas** | B vistos (readapt.) | exp. hasta 0.9 (B) |
|---|---|---|---|---|---|
| pago individual (informe 1) | 0.97 | 254 | **27 [0–60]** | **0.60 [0.23–0.90]** | 800 |
| impuesto a emisión constante 0.01 | 1.00 | 245 | 4 [0–11] | 1.00 | 775 |
| impuesto 0.05 | 0.97 | 244 | **0** | 0.97 | 750 |
| pago por CAMINO (grupos de 4) | 1.00 | 260 | **0 [0–1]** | 1.00 | **650** |
| pago por camino (grupos de 16) | 1.00 | 250 | 0 | 1.00 | 700 |
| camino 4 + impuesto 0.01 | 1.00 | 257 | 0 | 1.00 | 650 |

El tramposo (célula que emite siempre lo mismo y cobra como "sesgo útil") se reproduce (27) y, además, es él quien arruina la readaptación (0.60). Pagar al grupo chico ligado (camino de 4) lo elimina y readapta MEJOR que la base; el grupo de 16 también; el impuesto necesita ser alto (0.05). Es lo contrario de lo que hizo el crédito de grupo de la red ENTERA en el informe 1 (criaba tramposos y no aprendía): el tamaño del grupo que comparte el pago importa — chico cura, entero mata. Advertencia: con una economía 7× más pobre (error mío en la primera corrida, corregido) la red se poda a 34 células y no hay tramposo que medir: el tramposo necesita riqueza.

## 5. Olvido: no hay variante barata, sólo un canje (40 células sin lectura directa, 10 semillas)

| brazo | exp. hasta 0.9 (A) | N | B vistos | exp. hasta 0.9 (B) | **A tras B** |
|---|---|---|---|---|---|
| base sin vida | 587 | 40 | 1.00 | 825 | 0.13 |
| consolida κ 2 (plasticidad baja con energía vivida) | 575 | 40 | 0.90 | 2225 | 0.20 |
| consolida κ 0.5 | 762 | 40 | **0.55** | nunca | **0.42** |
| vida sola | 650 | 31 | 0.73 | 1925 (3/10) | 0.15 |
| vida + consolida κ 2 (viejas se congelan, nacen nuevas) | 712 | 31 | 0.52 | nunca | 0.30 |
| vida + consolida κ 0.5 | 1150 (1/10) | 31 | 0.30 | nunca | 0.32 |
| TECHO Adam | 1637 | 40 | 1.00 | 800 | 0.13 |

Consolidar por energía vivida conserva más de A (0.42) exactamente en la medida en que impide aprender B (0.55): A+B suma 0.97 contra 1.13 de la base. Nacer células nuevas para B no ayuda: las viejas congeladas siguen empujando la respuesta de A en la boca (no hay compuerta de contexto). **La vida no suma en olvido.**

## 6. Qué cambió respecto al informe 1
- "Gana 4.6×/1.6× al techo" → **falso con techo justo**: empata en aprender, pierde 3–4× en readaptar.
- "Siguiente paso: segunda capa" → hecho: **la plasticidad local en capas ocultas nunca supera a capas congeladas y muere a 3 capas**; el aviso sólo-energía (rpe) no orienta pesos.
- "Nadie generaliza por el one-hot" → **tampoco con binario, termómetro ni ángulos**; ni el techo.
- "Tramposo a 320" → **reproducido y curado** por pago por camino chico o impuesto alto, sin costo.
- Olvido → sigue en NO; la vida no aporta.

## 7. Las frases que el director SÍ puede decir ahora, y las que no
SÍ: (1) "Con un rival justo, una capa de células con reglas locales aprende suma mod 7 en las mismas exposiciones que Adam y cuesta 2.5× menos por paso; pero se readapta 3–4× más lento". (2) "En una red de 320 células con vida, pagar al grupo chico que forma un camino elimina las células que cobran sin aportar y readapta mejor; pagar a la red entera las cría: el nivel de selección importa y se midió". (3) "Apilar capas de células sirve sólo si las ocultas NO aprenden; con el aviso local encadenado la red deja de aprender a 3 capas".
NO: "más neuroplasticidad que el gradiente", "readapta más rápido", "no olvida", "generaliza / aprende álgebra con el código correcto", "la vida aporta aprendizaje u olvido", "se puede apilar a lo profundo", "un millón de células".

## 8. Siguiente paso más chico
Dos opciones de una tarde cada una; yo elegiría la primera: (a) **el pago por camino en el mundo real de JUACO** (los carros de la pista, 9 linajes): si el muro es un bien público, pagar al grupo chico y no a la célula suelta debería cambiar quién persiste — es la pieza que aquí sí funcionó en 5 semillas y conecta con la hipótesis del genetista; (b) compuerta de contexto para el olvido (la boca lee qué regla rige y enruta a células distintas), que es lo que la literatura usa y aquí falta. No invertiría más en profundidad con aviso local: tres formas probadas, ninguna supera a congelar.

## 9. Lo no verificado
Techo justo sin regularización ni búsqueda de arquitectura (podría ser aún más fuerte). Los avisos de 2+ capas con un solo juego de tasas (elegido en 2 semillas); 'fa' dio resultados idénticos para tres tasas del axón intermedio (sospechoso, sin diagnosticar). 5 semillas en capas, códigos y tramposo. Grokking del techo con decaimiento de pesos no se probó. La primera corrida de tramposo y olvido con economía 7× pobre se descartó (los txt se sobrescribieron con la corregida). Nada preregistrado; si la frase (2) de la sección 7 interesa, va con protocolo y réplica.
