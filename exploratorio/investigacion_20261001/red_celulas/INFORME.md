# INFORME — Red de células vivas, versión mínima (1-oct-2026, exploración, SIN preregistro, n = 10 semillas)

**HAY ALGO MODESTO.** Una red de células con reglas sólo locales (cada célula ajusta su entrada con UN número que le mandan las células que alimenta; nada de gradiente entre capas) aprende SUMA mod 7 en los 30 pares vistos en **550 exposiciones**, contra **2 550** del techo con retropropagación del mismo tamaño, y se readapta a RESTA en 887 contra 1 437; pero **nadie generaliza a los 19 pares nunca vistos (0.00–0.05, bajo el azar 0.14), nadie conserva A tras aprender B (0.13–0.17), y la vida (nacer/podar) NO suma nada medible: iguala en aprender, empeora en readaptarse, y el "tramposo" aparece con 320 células**.

Misión: llegar a la AGI por este camino (organismo mínimo, reglas locales, sin retropropagación dentro del sistema, con controles y réplicas). Carpeta: `PROYECTOS\JUACO\investigacion_20261001\red_celulas\` (fuera del repo). Código: `red_celulas.py` (célula, vida, techo), `corre.py` (brazos y medidas), `corre_todo.ps1` (reproduce todo, ~3 min CPU). Datos crudos: `datos\*.json`. Nada se commiteó.

## 1. Qué se construyó (en una lectura)

- **Letras**: a y b como one-hot (14 letras). Boca: 7 células, una por símbolo c.
- **Célula**: dueña de sus pesos de entrada (oye ~70 % de las letras, no todo), su sesgo, sus pesos de salida (su "axón" hacia las 7 bocas) y una energía E. Emite h = tanh(·).
- **Boca**: suma lo que le mandan las células (y lee también las letras directamente); cuando llega el símbolo c en el flujo calcula SU error de predicción. A cada alimentadora le manda: (1) ese error (aviso) y (2) un pago en energía = cuánto peor le habría ido sin esa célula (aporte contrafactual, calculado en la sinapsis con lo que la boca ya tiene).
- **Plasticidad** (todas locales, comentadas una a una en el código): axón = regla delta (lo que emití × aviso de la boca); entrada = **Hebb de tres factores**: letra × (mi emisión − mi media) × aviso escalar. La célula nunca recibe un vector: un número.
- **Vida**: E += pagos − costo de existir − costo de emitir. E > 5 → se divide (hija = copia con UNA mutación de un peso, N(0, 0.3)); E < 0 → muere. Tope 4×N0, mínimo 2.
- **Techo "Alejo"**: perceptrón de 2 capas, mismo tamaño, retropropagación, SGD simple (lr 0.05 = mejor de {0.05, 0.1, 0.2, 0.5}), mismo flujo, mismo error cuadrático. Está FUERA de la red.
- **Protocolo**: fase A = SUMA mod 7, 3 000 exposiciones a los 30 pares vistos; fase B = RESTA mod 7 (cambio de regla), 3 000 más; al final se mide A otra vez (olvido). Se evalúa cada 25 exposiciones sin aprender.

## 2. Tabla de brazos × medidas (40 células, 10 semillas; mediana [mín–máx]; `datos\final_n40.json`)

| brazo | A vistos | A retenidos (19) | exp. hasta 0.9 (A) | N fin | B vistos (readapt.) | exp. hasta 0.9 (B) | A tras B (olvido) | tramposas | ops/exp |
|---|---|---|---|---|---|---|---|---|---|
| a red completa (plast + vida) | 1.00 [0.97–1.00] | 0.00 [0.00–0.11] | 562 [450–1050] (10/10) | 31 [29–33] | 0.97 [0.83–1.00] | 1350 [800–1750] (10/10) | 0.15 | 0 [0–3] | 6 820 |
| b plast sin vida | 1.00 [1.00–1.00] | 0.03 [0.00–0.05] | **550** [450–800] (10/10) | 40 | 1.00 [0.80–1.00] | **887** [500–1800] (10/10) | 0.15 | 0 | 8 579 |
| c vida sin plast (sólo selección) | 0.17 [0.07–0.20] | 0.11 | nunca (0/10) | 21 [18–23] | 0.10 | nunca | 0.15 | 0 | 4 185 |
| d piso (nada) | 0.12 [0.07–0.30] | 0.13 | nunca | 40 | 0.13 | nunca | 0.12 | 0 | 6 703 |
| e aviso+pago BARAJADOS (con vida) | 0.90 [0.77–1.00] | 0.00 | 1137 [450–2325] (10/10) | 33 | 0.85 | 1812 (10/10) | 0.17 | 0 | 7 958 |
| e2 barajado sin vida | 0.93 [0.53–1.00] | 0.05 | 1075 [450–2700] (10/10) | 40 | 0.90 | 1562 (10/10) | 0.17 | 0 | 8 579 |
| g crédito de GRUPO (con vida) | 0.23 [0.13–0.63] | 0.05 | nunca (0/10) | 25 | 0.27 | nunca | 0.13 | **7 [0–12]** | 6 345 |
| g2 grupo sin vida | 0.13 | 0.18 | nunca | 40 | 0.13 | nunca | 0.17 | 0 | 8 579 |
| h sólo boca (entrada congelada) | 1.00 | 0.00 | 862 [650–1175] (10/10) | 40 | 1.00 | 1050 (10/10) | 0.13 | 0 | 8 579 |
| **f TECHO retropropagación** | 0.93 [0.83–1.00] | 0.00 | **2550** [2300–2750] (9/10) | 40 | 1.00 | **1437** [1075–2050] (10/10) | 0.13 | 0 | 5 040 |

Tarea de arranque (medio sumador = XOR+AND, 4 patrones, 3 clases, 20 células, `datos\medio_n20.json`): todos los brazos con plasticidad llegan a 1.00 en 30–40 exposiciones (techo: 70); c y d no pasan de 0.38–0.50. Sirvió sólo para comprobar el instrumento.

## 3. Reparto de crédito: qué quedó y qué se descartó (números)

Quedó: **individual, Hebb de tres factores** (letra × desviación propia × aviso escalar de las bocas), η_in 0.1, sin ruido. Descartados (3 semillas, brazo b, acierto en vistos a 3 000 exposiciones):
- Tanteo con ruido propio (perturbación de nodo: letra × ruido × aviso), η_in 0.1 / 0.5 / 2.0 con σ 0.3 y η 3.0 con σ 0.1: **0.20 / 0.10 / 0.20 / 0.17**. No aprende en 3 000 exposiciones.
- Hebb de tres factores CON ruido σ 0.3: η 0.02 → 0.43; η 0.1 → 0.13. Con η 0.3 sin ruido: 0.13 (se desborda). Sólo η 0.1, σ 0: **1.00 en 550**.
- Crédito de GRUPO (todas reciben "¿lo hizo mejor el grupo que antes?" y cobran lo mismo): 0.23 con vida, 0.13 sin vida. **No aprende y cría tramposas** (abajo).
- Barajado (control): aprende, pero más lento que con la entrada CONGELADA (1 075 vs 862 vs 550 con crédito correcto). Lectura: el aviso bien dirigido vale 862 → 550 (−36 %); mal dirigido estorba (862 → 1 075). La mayor parte del aprendizaje la hace la boca (regla delta sobre rasgos fijos): sin aviso a la entrada igual llega a 1.00.

**Advertencia honesta sobre "sin retropropagación"**: con UNA capa de células, "la boca manda su error y la célula lo pesa con su propio axón" es, en expectativa, la misma dirección que un paso de retropropagación; la diferencia está en el tercer factor (desviación propia en vez de derivada) y en que no se encadena a más capas. La versión que NO se parece al gradiente (tanteo con ruido) no aprendió. El revisor dirá "feedback alignment con pesos simétricos"; no hay que decir "sin gradiente" sin este matiz.

## 4. Vida (nacer/podar): qué aporta y qué no

- Economía rápida (costo 0.01, comida 0.09, división a E 2): **110 nacimientos y 115 muertes por 3 000 exposiciones; rompe el aprendizaje (0.38 vs 1.00 sin vida)** y cría 11 tramposas de 37. Variantes (3 semillas): lenta ÷5 → 0.90; lenta + emitir caro 0.02 → 0.70 y la red cae a 6 células; lenta + división a E 5 → **1.00 en 575 (la elegida)**; lenta + mutación chica → 0.67; muy lenta ÷20 → 0.97 **con sólo 11 células** (poda a un cuarto y sigue funcionando); emitir carísimo 0.05 → 0.50.
- Con la elegida: a vs b iguales en A (562 vs 550), **peor en readaptarse** (1 350 vs 887 en 40 células; 862 vs 550 en 80; 0.40 vs 1.00 de acierto en B con 320), igual olvido. Tamaño: se autorregula 40 → 31, 80 → 64, 320 → 253. Sólo selección (c) no aprende nada en 3 000 exposiciones.
- **Tramposo**: con pago contrafactual individual, 0 células constantes-y-ricas en 40 y 80 células; **con 320 aparecen 31 [2–72]** (células que emiten siempre lo mismo y cobran como "sesgo útil"). Con crédito de grupo aparecen ya en 40 (7 de 25) y además no se aprende. Lo que lo frenó en chico fue pagar sólo por aporte marginal; en grande ni eso. No se probó un impuesto a la emisión constante.

## 5. Escala (`datos\escala_n*.json`; exposiciones hasta 0.9 en vistos, mediana)

| células | b plast sin vida | a con vida | h sólo boca | f techo |
|---|---|---|---|---|
| 20 | 1075 (10/10) | 1625 (9/10) | 2000 (10/10) | 2612 (4/10) |
| 40 | 550 | 562 | 862 | 2550 (9/10) |
| 80 | 512 | 512 | 625 | 2375 |
| 320 | 450 | 450 | 500 | 2625 |

Sumar células suma: 20 → 320 baja de 1 075 a 450 exposiciones; el techo no mejora con el tamaño (su paso fijo). Con pocas células la plasticidad de la entrada importa el doble (1 075 vs 2 000); con muchas casi nada (450 vs 500): más células = más rasgos al azar = la boca sola basta. Dos reglas de escala puestas a mano (locales): la boca divide su paso entre sus alimentadoras y la comida crece con N0; sin ellas, 80 y 320 células desbordan.

## 6. Dónde le gana al techo y dónde pierde (sin adornar)

- **Gana en exposiciones**: 550 vs 2 550 para aprender; 887 vs 1 437 para readaptarse a la regla nueva sin reentrenar. Costo total hasta 0.9: 550 × 8 579 ≈ 4.7 M operaciones vs 2 550 × 5 040 ≈ 12.9 M (2.7× menos). **Pero por exposición cuesta MÁS** (8 579 vs 5 040 sumas/multiplicaciones: el pago contrafactual y la lectura directa) y el techo es un SGD simple con error cuadrático; con Adam y entropía cruzada el techo seguramente aprende mucho antes. El argumento "chips caros" NO sale de aquí.
- **Empata en olvido**: tras B, ambos quedan en 0.13–0.17 de A (azar). "Más neuroplasticidad = menos olvido" no se sostiene con estos datos.
- **Pierde en generalización**: nadie, ni el techo, acierta los 19 pares no vistos (0.00–0.05: bajo el azar, se contagia el vecino equivocado). Dato colateral: ni siquiera los mínimos cuadrados exactos sobre el prior de 8 ángulos propuesto en FABLE_bloques_autoentrenables.md pasan de 0.21 en retenidos (ese prior contiene también la dirección de la resta y 30 pares no la separan). El experimento "prior de ángulos" del colega no se sostiene tal como estaba escrito.

## 7. Las tres frases que el director SÍ puede decir, y las que todavía no

SÍ: (1) "Una red de células con reglas locales y UN número de aviso aprende suma mod 7 y se readapta a resta en 2–5 veces menos exposiciones que un perceptrón del mismo tamaño con retropropagación simple; con el aviso barajado o apagado tarda más (control que distingue)". (2) "La red se autodimensiona (nace y se poda) y sigue aprendiendo con un cuarto de las células". (3) "El pago por aporte marginal individual evita células que cobran sin aportar en redes chicas; el pago en grupo las cría y no aprende".
TODAVÍA NO: "más seguro", "menos olvido", "generaliza / aprende álgebra", "más barato por paso", "la vida aporta aprendizaje" (aquí la vida no suma y cuesta readaptación), "sin gradiente" sin el matiz de la sección 3, "un millón de células" (a 320 ya aparece el tramposo).

## 8. Siguiente paso más chico

Hacia muchas células: **impuesto a la emisión constante y segunda capa** (células que alimentan células), porque es ahí donde el aviso escalar deja de coincidir con el gradiente y la pregunta se vuelve real: ¿la Hebb de tres factores encadenada dos veces aprende algo que la boca sola no? Una tarde, mismo instrumento, 10 semillas. Hacia un LLM: nada todavía; antes de eso la red tiene que generalizar a un par no visto.

## 9. Declaraciones

- Prior puesto a mano: letras one-hot; lectura directa letras → boca; tanh; conectividad al 70 %; las dos reglas de escala; todos los números de la economía (sec. 4) fueron elegidos VIENDO 3 semillas (exploración, no preregistro: las 10 semillas finales 1–10 incluyen esas 3).
- Semillas: red 1–10; partición de pares `1000+s`; orden del flujo `2000+s` (mismo para todos los brazos de una semilla).
- Reproducir: `powershell -File corre_todo.ps1` (≈ 3 min). CPU total usada hoy ≈ 8 min.
- No verificado: techo con Adam/entropía cruzada; segunda capa; n > 10 semillas; impuesto al tramposo; el prior de ángulos dentro de la red (sólo se midió el mínimos cuadrados); permutación de símbolos como cambio de regla (sólo resta); por qué A tras B en vida "muy lenta" dio 0.80 en 3 semillas con TB = 1 (artefacto: no hubo fase B).
