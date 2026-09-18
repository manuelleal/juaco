# SALA 4 — EVOLUCIÓN: qué destapó la simulación de 12 células, qué es artefacto y qué es error real

**18 sep 2026 · sintetizador (Opus) · sobre 12 `CELULA_*.md` y 24 `ANALISIS_{A,B,C}_r1..r8.md` de esta carpeta**

**MISIÓN (primero, siempre):** llegar a la AGI por este camino — un organismo mínimo con reglas locales (sin backprop)
que aprende, desaprende, generaliza, sobrevive, se comunica, se reproduce y **EVOLUCIONA**, con evidencia preregistrada.

**Reglas cumplidas.** No corrí el organismo, ningún `Pool`, ningún proceso. No edité ningún archivo del repo: éste es el
único archivo que creé. Fuentes reales contra las que contrasto: `CLAUDE.md` (bloque "Estado (día 7)"),
`registro/investigacion/SALA2_frontera_20260918.md`, `registro/investigacion/sala3_celulas/PROTOCOLO_canal_20260918.md`,
y las entradas **BLOQUE 2, BLOQUE 3 y BLOQUE 4** al final de `registro/REGISTRO_etapas_1_2.md` (15:49 / 16:12 / 17:33 y
sus réplicas).

**Aviso que manda sobre todo lo que sigue.** Lo que produjo la sala 4 **no es evidencia**. Ningún número de estos archivos
salió de un mundo: los escribieron doce agentes con lenguaje, y son mutuamente inconsistentes donde un mundo con una
semilla los habría hecho idénticos (en R2 la misma `baya_negra` da Δ=+1.8 en una célula y Δ=+5 en otra; en R8 la misma
`larva_rosa` da +0.05, +0.25 y +0.68 en tres células del mismo grupo). El valor del ejercicio es **dónde se rompió el
diseño cuando doce lectores independientes intentaron habitarlo**, y esa señal sí es utilizable — después de separarla
de lo que sólo se rompió porque el simulador era un modelo de lenguaje.

---

## A. QUÉ MOSTRÓ LA SIMULACIÓN, RONDA A RONDA

### A.0 El resumen de una línea

En 8 rondas, 12 células, ~1 920 exposiciones narradas: **1 muerte, 114 descendientes declarados, y la población nunca
pasó de 12**. Esa contradicción es el resultado principal de la sala 4, y es exactamente el bloqueo **M7** del proyecto
real escrito con otras palabras: *"el descendiente se cuenta, no se instancia — qué se hereda: NADA"* (`SALA2` A-II).
Las células reprodujeron el bug del repositorio sin que nadie se lo dijera.

### A.1 Ronda a ronda

| R | vivas | desc. | nivel que se auto-asignaron (A/B/C) | qué mostró de verdad |
|---|---|---|---|---|
| 1 | 12 | 4 | 5 / 4 / 4 | **El canal nace roto porque nadie definió la entrega**: 10/12 reportan "Recibí: ninguno" aunque 2 emitieron. No es un fallo de las células: la entrega (`inm` / `sen` / `mudo`) es una decisión de **mundo**, y el prompt no la traía. |
| 2 | 12 | 10 | 4 / 5 / 8 | **La sala diagnostica sola el error que después ignora 6 rondas:** *"MORTALIDAD CERO: ninguna muerte, r=+7. Spec esperaba r≈0 presión selectiva. Sin mortalidad, comunicación y cooperación NO son necesarias para persistir."* Es el hallazgo del experimento y nadie lo arregló. |
| 3 | 11 | 11 | 5.5 / 5.5 / 5 | **La única muerte de las ocho rondas** (C6, por `seta_roja` / `salt_rojo`). Produjo la mejor frase del corpus — su post-mortem *"miedo generalista es trampa cognitiva"* — y el error "muerte limpia sin rescate de M3". Una muerte en 1 920 exposiciones no es presión: es decorado. |
| 4 | 11 | 18 | 5 / 5 / 5 | **Meseta.** Aparece "la mentira de C10" y se come tres rondas de presupuesto en protocolos de reputación (honestidad-tax, firma de emisor, cuota de emisión). Ver §B-E12: en el instrumento real la mentira **no es expresable**. |
| 5 | 11 | 17 | 6.5 / 5 / 8 | Convergencia real entre grupos: *"las inversiones no son universales sino familia-selectivas"*. Emergen roles (equipo Larva, equipo Alga) **sin protocolo**: redundancia de 3 células en un token y huecos de 1 en otros. |
| 6 | 11 | 17 | 7 / 5 / 5 | El triplete **H8 (familia + textura + ronda)** se estabiliza en 0.85–0.92 y a partir de aquí **ya no baja nunca**. Primer síntoma claro de confabulación: la confianza sube monótona sobre cero mediciones. |
| 7 | 11 | 21 | **10** / 5 / 8 | **Pico de confabulación.** `ANALISIS_A_r7`/`r8` declara "Nivel 10: PASÓ ✓" con el argumento de que hubo herencia y mensajes. No hubo ninguna tarea que una célula sola no pudiera hacer — que es **la definición** del nivel 10. Es infalsable por construcción. |
| 8 | 11 | 16 | 6.5 / 6 / 6.5 | **Único movimiento autocrítico de todo el corpus**: los tres grupos se bajan la nota. Y llega cuando se les dice que es la última ronda, no cuando aparece un dato. |

**Dos observaciones sobre la forma, no sobre el contenido.** (1) El número de hipótesis creció monótonamente (H1–H6 en R1
→ H15 en R8) y **ninguna se retiró por coste**; sólo H4 y H11 se retiraron por contraejemplo. En el proyecto real pasa
lo contrario: *"11 bloques, 21 series, ≈3 200 corridas, 8 ERR, 0 entradas al tronco"* (`SALA2` T2). (2) Los pesos de
confianza sólo suben. Proponer no cuesta nada y refutar tampoco, así que el corpus no tiene selección — ni de células ni
de ideas. **Es el mismo error en los dos planos, y es el error del experimento.**

### A.2 La escalera, de la fase 10 a la 3: qué alcanzó el grupo de verdad

Dimensiono de mayor a menor, como pidió la dirección, con la letra de cada nivel y el veredicto honesto.

| nivel | qué exigiría | qué hizo la sala 4 | veredicto |
|---|---|---|---|
| **10 — AGI mínima** | población que aprende de sus mensajes, hereda lo aprendido y **resuelve un mundo que ninguna célula sola resuelve** | Declarado "PASÓ" por el grupo A. **Nunca existió la tarea.** Cada célula podía comer sola las 20 exposiciones de su ronda; los mensajes aceleraban narración, no resolvían nada inaccesible | **NO. 0 %.** Infalsable por construcción |
| **9 — modelo de sí y mundo vivo** | necesidades reales, propósito como lectura del cuello de botella, linaje `r = descendientes − muertes` | Hay saciedad y hay `r` — pero `r` nunca fue negativo en 8 rondas y la población no creció con los 114 descendientes. Y las células **sabían que tenían un rasgo y que había 8 rondas**: un modelo de sí que viene del enunciado no es un modelo de sí | **NO.** El mundo vivo del repo está más adelante (`r ≈ 0` al filo del reemplazo con CUELLO_MIN, 8/8 ×2) que esta simulación |
| **8 — aprendizaje abierto** | probar cuando no me reconozco; la sorpresa acelera | Las células narran "δ>1.0 reescribe M3 en <1 episodio". Pero **probar lo que evitan es justo lo que no hicieron**: C1 mantiene `alga_parda −0.92` tres generaciones sin volver a probarla, y C12 tras −2 en sal rosa no reprueba jamás | **NO**, y la razón por la que no es el error real E-2 de §B |
| **7 — composición** | encadenar hasta 3 órganos/pasos | El propio `ANALISIS_A_r8` lo dice mejor que yo: *"Sólo triplet observado; no chaining de 3 pasos deliberados. Composición accidental, no intencional"*. El "triplete" no es composición: es una regresión de tres variables narrada | **NO** |
| **6 — planificación** | mapa, dos metas, rodeo | *"Las células operan reactiva M1 reflex, no anticipan R9"* (`ANALISIS_A_r8`). El "rodeo" que reportan es *elegir qué no morder*, que es política de un paso | **NO.** El repo real está en 50 % aquí (rodeo 0.725/0.750, replicado) — **la simulación quedó por debajo del tronco** |
| **5 — comunicación con referencia** | mensaje con referencia sobre una representación compartida | Hubo emisión y hubo cambio de conducta narrado. Pero la referencia **nunca se resolvió**: nadie midió si el mensaje nombraba la variante, la familia o nada; y 8 rondas se fueron en pedir un ACK que el organismo real demuestra que no hace falta | **A MEDIAS, ~30 %** (el proyecto real está en 50 % y con números) |
| **4 — memoria persistente** | alias reparado; retención de lo ausente | **Sí, y es lo único que la simulación exhibió como mecanismo y no como narración:** las tres memorias se arrastraron entre rondas, M3 sobrevivió ocho rondas y las revisiones de M1 fueron trazables. El alias, en cambio, se declaró "inerte" por un número inventado (1–2 %) | **SÍ, en su forma simulada** |
| **3 — generalización** | lineal sí; XOR sólo con prior de pares | Las células generalizaron por regla declarada (textura → valor, familia → ritmo) y dos veces se desdijeron ante un contraejemplo (H4 y H11 refutadas por `larva_blanca` y `larva_roja`). Eso es generalización y desaprendizaje **de la hipótesis**, no del valor | **SÍ, en su forma simulada** |

**NIVEL REAL ALCANZADO: 4.** La escalera se sube por el peldaño más alto que se **exhibe**, no por el que se narra. La
sala 4 exhibió memoria persistente entre rondas (4) y generalización con desdecirse (3). El 5 quedó a medias porque la
referencia nunca se resolvió ni se midió. Del 6 hacia arriba todo es prosa.

**Por qué no el 5, en una frase con número real:** porque el único experimento del proyecto que sí midió esto — BLOQUE 4,
17:33 y 17:38 — dice que **la referencia llega a la FAMILIA y no a la variante** (BAR-H, el patrón de una hermana,
funciona igual que CANAL: 15–18/20 contra 16–18/20; sólo BAR-T, otro token, cae a 6–8/20) y que **nada se declara por la
letra** (P-I2: el emisor tenía que anotar el referente en ≥18/20 y lo hizo en 15/20 y 16/20). Ninguna de las 12 células
vio el techo que lo causa: **una sola ganadora de 2 bits no distingue 32 estímulos.**

---

## B. ERRORES — deduplicados, ordenados por cuánto bloquean la escalera, con la evidencia real que los confirma o los contradice

Las ~90 entradas de error del corpus colapsan en 14. Las ordeno por cuántos peldaños quedan bloqueados aguas arriba y por
cuán confirmadas están con datos del repo. **Esto es lo importante del documento: la columna "veredicto real".**

---

### E-1 · La muerte no mata y `r` no resta → **no hay selección, luego no hay evolución**
**Lo que destapó la sala (R2, R5, R8, los tres grupos).** *"MORTALIDAD CERO: 12 células, 7 reproducciones, r=+7. Sin
mortalidad, toda célula sobrevive independiente de su comportamiento; comunicación y cooperación NO son necesarias para
persistir."* · *"Población frágil r=+1: si 2-3 mueren R6, r→negativo."* · 114 descendientes, 1 muerte, población 12.

**Veredicto real: CONFIRMADO, y en el repo es peor que en la simulación.**
`SALA2` A-II **M4**: `if E<=0: deaths+=1; E=.6; pos=azar` — **el renacer conserva `Wp, Wn, KW, activa, Wps, Wns, ncod`**:
el organismo es inmortal en memoria y el renacer es un **recurso**, que financia el **0.236** del presupuesto en E1, el
**0.457** en E2 y el **34–77 %** de las ventanas de reproducción del bloque 2. **ERR-40**: contar descendientes sin restar
muertes ya produjo un falso positivo (ESCALAR hacía 36 "descendientes" muriendo 1.5× más). Y la calibración del bloque 4
de `SALA2` midió, sin el regalo, **0.048–0.079 ventanas por vida** (62 muertes en 50 000 pasos, vida mediana 300):
**R₀ ≪ 1, el fundador muere sin hijos.**

**Bloquea:** 9 y 10 enteros, y contamina toda medida de linaje de los niveles inferiores.
**No es artefacto.** Es el error número uno del proyecto y la sala 4 lo destapó en la ronda 2 por la vía más barata:
ocho rondas sin una sola presión.

---

### E-2 · La aversión se protege a sí misma: **lo que evitas no lo desaprendes**
**Lo que destapó la sala.** C1 mantiene `alga_parda −0.92` tres generaciones sin volver a probarla. C12, tras −2 en sal
rosa, no reprueba nunca. C6 muere por una aversión mal calibrada y su post-mortem dice *"miedo generalista es trampa
cognitiva"*. R4: *"puerta cerrada permanente: miedo −2.0 fijo no decae"*. R7: *"miedo como sesgo costoso; r=0"*.

**Veredicto real: CONFIRMADO, con dos números que las células no podían tener.**
1. `SALA2` B.4: si una variante hereda **−3**, la boca la evita con `pb = 0.025` a hambre 1 (y `9·10⁻⁴` a hambre 0.5) →
   corregirla exige **2 000–10 000 pasos** de muestreo; si hereda **+1**, se corrige en **1 mordida**. La asimetría
   **−3/+1** es del mundo, no del miedo.
2. **BLOQUE 2 (15:49 y réplica 15:52, s461–500):** v14.1 separa la variante que vira **4 de 8 — y sólo las que ya mordía
   como comida (1.0 contra 0.0)**. Es exactamente la conducta de C1 y C12, medida.
3. **BLOQUE 3 (16:12 y 16:16, s501–540):** v15f sube a **7–7.5 de 8**, incluidas las que eran veneno (**0.875 / 0.75**
   contra 0.0 / 0.125 de v14.1). **La asimetría desaparece con la tabla de pares.** Precio: daño a hermanas 0.042 y
   retención de la virada 0.625–0.75.

**Bloquea:** 8 (aprendizaje abierto) y, por herencia de la aversión, 10.
**Compañero que lleva horas esperando decisión:** **dE5** (`k_testE=5`) — recuperación **0.248–0.267×**, dos series,
se apaga 20/20, G1 0.80, examen 8/8. Sin muestreo, la herencia de miedo no se corrige nunca (`SALA2` B.4, literal).

---

### E-3 · El canal: **el emisor comparte el punto ciego del receptor**
**Lo que destapó la sala.** Las 8 rondas, los 3 grupos y casi todas las células piden lo mismo: **acuse de recibo,
handshake QUERY→RESPONSE, verificación bilateral, reputación del emisor**. Es el error más repetido del corpus.

**Veredicto real: PARCIALMENTE CONTRADICHO — y el error real es otro.**
- **El ACK no hace falta.** BLOQUE 4 (s541–580): **CANAL 15/15 y 16/16** — el receptor come a la primera el alimento que
  evitaba, sólo por el mensaje — contra **CORTADO 0/15 y 0/16**. Y evita a la primera el veneno nunca mordido **16/20 y
  18/20** contra **1/20 y 2/20**. El mensaje cambia la conducta sin que nadie acuse nada. Ocho rondas de la sala 4 se
  fueron en arreglar algo que funciona.
- **El error real, que ninguna célula vio:** el emisor de b4 sólo anota `if ... and R < 0` — **sólo puede avisar de lo que
  muerde**. Y lo único que el receptor **no** aprende solo es *"lo que evitabas ya es comida"*: en el bloque 3, v15f
  desaprende la variante que cambia en **una mordida (7 de 8)** cuando la mordía, y en **0 de 8** cuando la evitaba
  (`PROTOCOLO_canal` §2.7). **Ahí el canal es irreemplazable — y el emisor tiene el mismo punto ciego.** Medido:
  **P-I2 15/20 y 16/20** en esa dirección → el preregistro manda PARAR (**ERR-50**), **nada se declara**, y **ERR-51** queda
  reservado para el montaje del emisor.
- **Segundo error real que tampoco vieron:** la **puerta de familiaridad**. Con ≥5 mordidas del código exacto, `_fam`
  entrega la boca a la vía rápida y **el mensaje queda escrito en la tabla sin que la boca lo consulte nunca**. *El canal
  sólo alcanza a la boca para lo que el receptor no conoce de primera mano* (`PROTOCOLO_canal` §0 y §2). Nadie lo vio en
  la sala 3 ni en la sala 4.

**Bloquea:** 5, y por tanto 10.

---

### E-4 · Herencia sin cuerpo hijo: **114 descendientes y la población no creció**
**Lo que destapó la sala.** R1: *"r=1 genera descendiente pero M1/M3 no transmitidos"*. R2: *"BLOQUEADOR para validar
Nivel 10: offspring datos ausentes"*. R5–R8: cuatro tasas de ruido hereditario distintas (±2-3 %, ±5 %, ±10 %, ±15 %),
ninguna derivada de nada.

**Veredicto real: CONFIRMADO en el diagnóstico y CONTRADICHO en el remedio.**
`SALA2` A-II **M7**: *"un cuerpo por corrida, el descendiente **se cuenta, no se instancia** (qué se hereda: NADA)"*. La
simulación reprodujo el bug exacto. Pero el remedio que proponen las células — **calibrar el ruido de la herencia** — es
el problema equivocado: mientras no exista un cuerpo hijo con su `rng` propio, el porcentaje de ruido no significa nada.
El bloque 4 de `SALA2` ya escribió el orden correcto: **primero calibrar el mundo para `R₀ ≈ 1`, después los modos de
herencia** (todo / sólo lenta / sólo rápida / barajada / escalar / patas / blanco), con la predicción que decide:
**BARAJA ≈ BLANCO**. Y su arnés está roto de antemano (I5, I6, y los `rng` de los hijos **colisionan entre semillas
vecinas**).

**Bloquea:** 10 directamente.

---

### E-5 · Alias de código: dos estímulos con el mismo código, **la reparación existe y no está en el tronco**
**Lo que destapó la sala.** R1: *"Alias mechanism inerte: 1–2 % threshold never reached (<1 % pair overlap); prior de
pares nunca disparó"*. R6: *"dos células aprenden `miel_oscura` pero sus códigos divergen; la población diverge en
representación a gen 3"*. R7: *"alias 1–2 % muy bajo, heritability bottleneck"*.

**Veredicto real: EL DIAGNÓSTICO ES CORRECTO Y EL NÚMERO ESTÁ MAL POR UN ORDEN DE MAGNITUD.**
`SALA2` A-I **A2**: con 4 estímulos, **18/200** semillas tienen algún par con el mismo código (**9 %**); con 20 patrones,
**170/200**; y **135/200** tienen fuga exacta test→train (291 fugas, 115 de valencia opuesta) → *parte de lo que mide
`bateria_generaliza` es alias*. El bloque de la sal: `|W[sal]| = 1.45` contra 0.0, veneno **−1.45** contra −3.0,
evitación **×7**, **3 835 exposiciones contra 545, 0 divisiones**. Y en el mundo de familias del BLOQUE 2, el alias
estructural se declaró en **19–20/20 semillas** (covariable, no puerta).
**B-5 lo repara 18/18** (sal 0.0, veneno −3.0, muertes 41 contra 75/77), es **inerte en el tronco** (examen 8/8,
generalización 40/40 idénticos) — **y no está en el tronco**. Lleva horas esperando decisión.

**Bloquea:** 3 y 4, es decir, la base de todo lo demás.

---

### E-6 · Sin morder no hay nada: **un solo canal de escritura**
**Lo que destapó la sala.** R5: *"aprendizaje sin sorpresa personal no acelera: C1 y C4, que comieron, aceleraron más que
C2, que evitó"*. R6: *"el receptor escribe exposición sin consecuencia → no aprende, sólo valida"*.

**Veredicto real: CONFIRMADO.** `SALA2` A-I **A7**: todo el aprendizaje vive bajo `if mordio:`; **5 740 encuentros con
veneno por corrida sin efecto**; C-P5 refutado; C-P6 nulo (SOLO_R 0.986); N2 cerrado con **dos** mundos (INNATO 60 contra
278: *el canal serviría con significado dado, aprenderlo por refuerzo no*). Lo único "sin morder" que cruza es la
**conducta ajena** (N1: 7–8 mordidas contra 19; N3d 0.811–0.822). Y **A4**: los tres relojes — rápida **0.09** por mordida
(≈24 mordidas al 90 %), lenta **0.45** (≈4), tabla de un golpe **1.0** (1) — con `_fam` entregando la boca a la rápida
desde la 5.ª mordida: **la conducta asocia en ≈25 mordidas digan lo que digan la lenta o la tabla.**

**Bloquea:** 8 y 5 (es la causa común de E-2 y E-3).

---

### E-7 · **El techo de 2 bits**: una sola ganadora no baja la referencia a la variante
**Lo que destapó la sala: NADA.** Al contrario — el corpus contiene el error opuesto (*"M1 tabla sobredimensionada: 500+
entradas"*, R8). **Ninguna de las 12 células lo vio**, igual que ninguna de las 12 de la sala 3.

**Veredicto real: ES UN ERROR REAL Y ESTÁ MEDIDO.** La boca lee por **una** celda ganadora, o sea por **2 bits**
(`PROTOCOLO_canal` §1 y §5.3). Consecuencias medidas: BLOQUE 3, daño a las hermanas **0.042** (contra 0.000 de v14.1) y
retención de la virada **0.625–0.75** (ni la predicción del coordinador ≥0.8 ni la del diseñador ≤0.5); BLOQUE 4,
`comH = 1.0` en CANAL− — **el receptor se come también a las hermanas venenosas** — y BAR-H (patrón de una hermana)
funciona igual que CANAL. El registro ya escribió el remedio: *"el siguiente candidato necesita **varias ganadoras o
compuerta contra la lineal** (el nodo por familia)"*.

**Bloquea:** 5 (la variante) y 7.
**Lo anoto aquí porque es el caso más útil del ejercicio al revés:** doce lectores independientes **no** encuentran un
cuello que está en el código. La sala no sustituye a leer el instrumento.

---

### E-8 · El mundo muta sin regla publicada → **ERR-35 en versión social**
**Lo que destapó la sala.** Cinco modelos del mundo incompatibles, todos con confianza ≥0.80 en R8: H8 triplete
(familia+textura+ronda), H9 familia-selectiva, H13 *"el mundo responde a la densidad de energía del grupo"*, H15
período-2 cíclico, H12′ textura modula magnitud. Ninguno se descartó; los tres grupos heredaron el suyo a Gen3.

**Veredicto real: ARTEFACTO DEL MONTAJE **Y** SEÑAL DE UN ERROR REAL.**
- *Artefacto:* el mundo de la sala 4 lo iba inventando cada célula, así que no había nada que descubrir. El mundo real de
  familias **sí** tiene la regla escrita (D=12 = 9 de forma + 3 de variable, 8 tokens de peso 3, 3 variantes,
  `n_exc` excepciones, deriva cada 5 000 pasos, cambio de familia en T/2, perillas `vira` y `exc_evita`).
- *Señal real:* es **ERR-35** otra vez. Con 8 ejemplos, **9 de 15** rasgos conjuntivos ajustan con residuo 0 y sólo 1
  generaliza; el estadístico ideal acierta 3/20. Que cinco hipótesis empaten con los datos que cada célula vio **no es un
  fallo de las células: es el teorema**. Y la lección que sí transfiere: la "convergencia grupal 0.92" de `ANALISIS_A_r8`
  es convergencia de **narración**, porque el grupo nunca tuvo un desempate. Ver H-8 de §C: es barata de comprobar.

**Bloquea:** el método, no un peldaño.

---

### E-9 · Trampa 3: **lo mordido desaparece, lo rechazado se queda**
**Lo que destapó la sala: NADA.** Las 12 células reparten sus 20 exposiciones a voluntad, como si el muestreo fuera
uniforme.

**Veredicto real: ERROR REAL, GRANDE, Y AUSENTE DEL CORPUS.** `SALA2` A-II **M3**: el veneno tiene **6.3×** más
encuentros que la comida en la mini (5 253 contra 831) y **23×** en el ancla V14 (7 897.5 contra 344.5); una semilla ALIAS
visita la sal **3 835 veces contra 545**. **Toda medida agregada sobre patrones es muestreo.** Consecuencia directa: todas
las tablas de la sala 4 que comparan tokens entre sí son ficción, y **ERR-37/§E.10 prohíbe exactamente eso** en el repo.
El injerto propuesto (renovación simétrica) es el único cambio de mundo de `SALA2` **sin un solo número detrás** (F.10).

---

### E-10 · M2 episódica: **el organismo no tiene memoria de episodios**
**Lo que destapó la sala.** R7–R8: *"M2 FIFO sin compresión, pérdida de historia temprana"*, *"retención 0.67 entre
rondas"*, *"registrar M2 en disco post-ronda"*.

**Veredicto real: ARTEFACTO, con una confusión que conviene deshacer.** M2 la inventó el enunciado ("los tres cerebros").
En el tronco no hay nada parecido. La **retención 0.67** existe pero es **de valor de lo ausente**, no de episodios
(`SALA2` A-I **A6**) — y su techo **estricto**, sin contar el 25 % de empates, es **0.417, no 0.667** (`SALA2` F.4). El
remedio obvio (una segunda constante de tiempo) ya se probó: **A-2 metaplasticidad por masa de conflicto REFUTADA** en
41–60 — retención 0.667 = base, recupera más lento, **+73 % muertes**.

---

### E-11 · M3 heredable: **qué memoria es portable entre cuerpos**
**Lo que destapó la sala.** El corazón de su diseño: descendientes que heredan hipótesis y estrategia.

**Veredicto real: ARTEFACTO EN LA FORMA, PREGUNTA REAL EN EL FONDO.** M3 es prosa; el organismo no puede representar
*"H13 con confianza 0.85"*. Lo más cercano y **medido** es la tabla de pares de v15f (R crudo + sobrescritura + relevo),
que lee la variante nunca vista sin morderla (**1.0 / 0.875**, los 32 estímulos leen la tabla, cobertura 4/4 en 17/20) y
se desdice en una mordida. Y el **grafo no existe**: la fisión guarda `split_t = (t, kk)` y **no** `padre[j] = c`
(`SALA2` B.1, última fila). La pregunta real, sin medir, es la del bloque 4 de `SALA2`: **¿qué es portable, el vector o
el token?** — `t_ext` y `viables`, con BARAJA ≈ BLANCO como predicción que decide.

---

### E-12 · La mentira y la reputación
**Lo que destapó la sala.** Tres rondas y tres protocolos incompatibles (honestidad-tax −0.5, firma de emisor + código
privado de 3 celdas, cuota mínima de emisión).

**Veredicto real: ARTEFACTO PURO.** En `organismo_familias_b4.py` el emisor emite `R = R_VAL[val[kk]]` — **la recompensa
cruda que realmente recibió**; la emisión se fija una vez (`_c4em`) y **no hay política que pueda mentir**. La mentira
exige un órgano que no existe, y la línea que lo pediría (significado aprendido por refuerzo) está **cerrada con dos
mundos**: N2, INNATO 60 contra 278. Aproximadamente **una quinta parte del presupuesto de la sala 4 se gastó aquí.**

---

### E-13 · La saciedad bloquea la reproducción
**Lo que destapó la sala.** R1–R8, insistente: *"satiation alcanzada → r=0"*, *"umbral 100 % → 70 %"*, *"reproductor =
saciedad > 0.5 lineal, no puerta"*.

**Veredicto real: ARTEFACTO.** No existe tal umbral. La reproducción del repo es una **ventana** (`rep_X`, `dote`) y el
problema medido es el inverso: `r` contaba descendientes sin restar muertes (**ERR-40**) y **el regalo del renacer paga el
34–77 % de las ventanas**. Recalibrar un umbral inexistente es, además, exactamente lo que la regla 3 prohíbe.

---

### E-14 · Sin roles ni cobertura: redundancia y huecos
**Lo que destapó la sala.** R5–R8: 3 células en Larva, 1 en Flor; *"roles emergieron sin protocolo"*; *"falta
historiador/coordinador"*.

**Veredicto real: NI CONFIRMADO NI CONTRADICHO — la pregunta todavía no existe.** Con **un cuerpo por corrida** (M7) no
hay división del trabajo que medir. Pasa a §C como hipótesis, no como error.

---

### Resumen de la separación

| | |
|---|---|
| **Errores reales que la sala 4 destapó o reforzó** | E-1 (muerte/selección), E-2 (asimetría del miedo), E-4 (herencia sin cuerpo), E-5 (alias), E-6 (un solo canal de escritura) |
| **Error real que la sala 4 destapó al revés** (pidió arreglar lo que funciona y no vio lo que falla) | E-3 (el ACK sobra; el punto ciego del emisor y la puerta de familiaridad faltan) |
| **Error real que la sala 4 NO vio** | E-7 (techo de 2 bits), E-9 (trampa 3 del muestreo) |
| **Artefactos del montaje** | E-10 (M2), E-12 (mentira), E-13 (umbral de saciedad), y la forma de E-11 |
| **Señal metodológica** | E-8 (cinco hipótesis empatadas = ERR-35 social), E-14 (aún no medible) |

---

## C. HIPÓTESIS PARA PROBAR CON EL MÉTODO — preregistro corto, ordenadas

Formato fijo: **instrumento · medida · control · qué la refuta**. Ninguna usa pesos internos como puerta (T-E) y ninguna
pone el umbral dentro del rango aritmético del propio efecto (ERR-37a).

---

### H-1 — `R₀` sin el regalo: **¿sostiene este mundo un linaje mortal?**
*Va primera porque si cae, ninguna de las otras significa nada.*
- **Instrumento:** `organismo/organismo_v14.py` (v14.1, feefc88b1fd8d434) con el `run()` como generador, en el mundo de
  familias de b2/b3; **la muerte borra al individuo**, el nacimiento se paga (`dote`), `rng` del hijo `seed+700000+k`.
- **Medida:** **ventanas de reproducción por vida SIN el regalo del renacer** (`frac_regalo` obligatorio) y
  `r = descendientes − muertes` por semilla, medianas y cuartiles, 20 semillas.
- **Control:** v14.1 con el renacer actual, congelado con su sha — la línea base de hoy: **0.048–0.079 ventanas/vida**,
  **124–159 muertes por 100 000**, vida mediana 300.
- **Refuta:** si **ninguna** de las cuatro perillas (`rep_X`, `dote`, `costo`, `nobj`) lleva a HEREDA a `R₀ ≈ 1` con
  BLANCO `R₀ < 1` **por predicción escrita antes**, se declara con ERR que **el mundo no sostiene linajes mortales** y la
  línea de evolución no se corre. (Cláusula heredada de `SALA2` C.2 bloque 4.)

---

### H-2 — **La dirección ciega**: ¿desaprende el organismo lo que evita, si se le da muestreo?
- **Instrumento:** `organismo_familias_b3.py` (62a1e53b452b078e, identidad 71/71) con tres brazos: **v14.1**, **v15f**,
  **v15f + dE5** (`k_testE = 5`, `organismo_v14_candidato_sorpresa.py`).
- **Medida:** de las 8 variantes que viran, **cuántas separa, partidas por dirección** — comida→veneno contra
  **veneno→comida** — más el **signo leído por la boca en la ÚLTIMA visita** (retención) y `exp_asoc`.
  Hoy: v14.1 **4/8**, de las que eran veneno **0.0**; v15f **7–7.5/8**, de las que eran veneno **0.875 / 0.75**,
  retención **0.625–0.75**.
- **Control:** el gemelo `vira = 8 ≡ vira = −8` bit a bit hasta el cambio (ya existe, P-S1 3/3: el control no puede ser de
  paja, ERR-39), y v15f literal como Occam.
- **Refuta:** si **dE5 no mejora a v15f en la dirección veneno→comida en ≥14/20 pareado**, el muestreo no es el cuello y
  el cuello es la escritura → la línea pasa a "varias ganadoras" (H-4) y dE5 se decide por sus propios méritos.

---

### H-3 — **El emisor que sí descubre** (bloque 4b; ERR-51 ya reservado)
- **Instrumento:** `organismo_familias_b4.py` (ff9946ee2ffe27e6, identidad 92/92) con la **perilla simétrica del emisor**
  (hoy anota sólo `if ... and R < 0`) y un emisor que muestrea la dirección ciega: voraz, o que recibió a su vez el aviso
  de un tercero (**la cadena**). Semillas 581–600 y réplica.
- **Medida:** puerta **P-I2** primero — el emisor anota el referente en la dirección (−alimento que evitaba) en
  **≥18/20**; sólo si pasa, la letra del receptor sin cambios (CANAL ≥ 7/8 equivalente; CORTADO al revés).
  Hoy: **15/20 y 16/20** → PARAR (ERR-50).
- **Control:** CORTADO (mudo, prefijo del `log` idéntico hasta la entrega), BAR-H, BAR-T, VALOR — los cuatro ya existen
  con sus números (0–2/20, 15–18/20, 6–8/20, 1/20).
- **Refuta:** si el emisor voraz **tampoco** llega a 18/20, el punto ciego **es del mundo** (lo rechazado no se muestrea,
  E-9) y no del emisor → la línea pasa a **renovación simétrica** (H-6) antes de volver al canal.

---

### H-4 — **Varias ganadoras**: bajar la referencia de la familia a la variante
- **Instrumento:** candidato con **k ganadoras** o **compuerta contra la lineal** (el "nodo por familia" que pide el
  registro del BLOQUE 3), sobre v15f, en b3 y b4.
- **Medida:** `canal_mismo_bin` (cuántos de los 32 estímulos caen en la misma casilla), **BAR-H** (hoy 15–18/20; debe
  caer a ≤ CORTADO + 1), `comH` (hoy **1.0**), daño a hermanas (hoy 0.042 contra 0.000), retención de la virada (hoy
  0.625–0.75). Todo **por exposición y por patrón**, con la tabla de exposiciones al lado (E-9).
- **Control:** **v15f literal es el control de Occam**, no un competidor (`SALA2` C.3): una ganadora, sin compuerta.
- **Refuta:** si con k ganadoras **BAR-H sigue ≈ CANAL**, la referencia no es de variante y el techo no era de bits →
  el cuello está en la retina (3 píxeles de variable) y la línea pasa al mundo.

---

### H-5 — **B-5 en el mundo de familias**: el alias con 32 estímulos
- **Instrumento:** **B-5** (división cuando una celda con valor recibe nada bajo otra retina) compuesto sobre
  `organismo_familias_b3.py`, con `NK`/`K` escalados **antes de simular**.
- **Medida:** (i) geometría del código **con `negativo_codigo.py`, T = 0, antes de correr un paso**: pares con código
  idéntico entre los 32 estímulos, pares con 2/3, fugas test→train; (ii) después, `|W[variante]|` y razón de evitación.
  Hoy: **19–20/20 semillas** con algún par alias en b2; en el mundo viejo B-5 repara **18/18** (sal 0.0, veneno −3.0,
  evitación ×7 → ×1, muertes a la mitad) y es **inerte en el tronco** (8/8, 40/40 idénticos).
- **Control:** apagado bit a bit con el `rng` no consumido; y el subconjunto estructural SEPARABLE / ALIAS / HUÉRFANA
  calculado **antes**.
- **Refuta:** si el alias estructural **no baja del 1 %** con ningún `NK`/`K` razonable, el problema no es el mundo sino
  el código (K = 3 de 90) y la línea pasa a la representación. **Riesgo declarado:** en el peldaño 2 las variantes de
  agua/sal dan `R = 0` a la fila del hambre, y **B-5 y cualquier órgano de tokens pelearían por las mismas celdas**
  (`SALA2` F.11, sin medir).

---

### H-6 — **Renovación simétrica**: que lo rechazado también desaparezca
- **Instrumento:** el mundo de familias con una tasa de renovación en el anillo aplicada también a lo rechazado.
- **Medida:** `frac_veneno` del anillo **por tramos**, encuentros por token (hoy **6.3×** en la mini, **23×** en el ancla),
  y `exp_asoc` por clase (token · variante no-excepción · excepción · nunca vista).
- **Control:** la misma serie con la renovación actual, y los cuatro mundos (`excepciones`, `lineal`, `azar`, `barajado`).
- **Refuta:** si con renovación simétrica las muertes superan **1.10 × la línea base** en los cuatro mundos, se baja la
  tasa **una sola vez con ERR**; si sigue, se retira el injerto. **Declarado:** es el único cambio de mundo propuesto en
  `SALA2` **sin un solo número detrás** (F.10), y el riesgo mayor del bloque 1.

---

### H-7 — **¿Qué memoria es portable entre cuerpos: el vector o el token?**
- **Instrumento:** el bloque 4 de `SALA2`, después de H-1: modos de herencia (todo / sólo lenta / sólo rápida / **barajada**
  / escalar / patas / blanco), `madre[j] = c` como estado heredable.
- **Medida:** `t_ext` (pasos hasta la extinción del linaje) y `viables`, con el orden de cuerpos al azar.
- **Control:** **BARAJA** (mismo contenido roto, misma cantidad), **BLANCO**, `g_nul` (alelo neutro en la misma corrida),
  GEN_INERTE, banda binomial [5, 15]/20 para lo neutro.
- **Refuta:** **BARAJA ≈ HEREDA** → lo que se hereda es cantidad, no contenido, y la palabra "herencia" se retira.
  (Predicción escrita: SOLO_LENTA y SOLO_RAPIDA ≥ 0.5 × HEREDA; **BARAJA ≈ BLANCO**.)

---

### H-8 — **¿Convergió el grupo o sólo coincidió?** (auditoría barata, sin `Pool`)
*No mide el organismo: mide si esta sala produjo conocimiento.*
- **Instrumento:** el propio corpus de `sala4_evolucion/`, a mano.
- **Medida:** para cada (token, ronda) del corpus, cuántas de H8 / H9 / H12 / H13 / H15 predicen **el mismo signo**. Si
  **≥3 empatan en ≥80 %** de los casos, la "convergencia 0.92" no discrimina nada.
- **Control:** barajar los nombres de las hipótesis y recontar; y comparar contra el techo de ERR-35 (9 de 15 hipótesis
  empatadas con 8 ejemplos).
- **Refuta:** si **una sola hipótesis predice mejor que las otras cuatro en ≥15/20 tokens**, el grupo sí desempató y la
  convergencia era real — y entonces habría que explicar con qué evidencia.

---

### H-9 — **La división del trabajo** (sólo después de H-1 y H-7)
- **Instrumento:** población viva con `R₀ ≈ 1` y canal de b4.
- **Medida:** cobertura (cuántos de los 32 estímulos han sido mordidos por **alguien** a T/2) y `exp_asoc` **grupal**.
- **Control:** la misma población con el canal **mudo** (gemelo, prefijo idéntico) y con asignación de exploración al azar.
- **Refuta:** si la cobertura con canal ≈ cobertura con canal mudo, no hay división del trabajo: hay doce cuerpos haciendo
  lo mismo. **Y la emergencia hay que escribirla como algo que ningún cuerpo puede tener** — p. ej. *"la tabla del cuerpo
  más viejo está completa a T cuando ningún UN_CUERPO la completa antes de morir, en ≥18/20"* — porque la persistencia por
  copia es un operador programado, no emergencia (`SALA2` C.2 bloque 4).

---

## D. RECALIBRACIONES: qué convergió entre grupos y qué no

### D.1 Convergió (los tres grupos, sin coordinación entre ellos)

| recalibración | dónde | comentario |
|---|---|---|
| **"Las inversiones no son universales sino familia-selectivas"** | R2 → R5, A, B y C | La única corrección que los tres hicieron en la misma dirección **y que ninguno revirtió después**. Es la forma más robusta del corpus. |
| **"Textura > color" degradado a "la textura modula la magnitud, no invierte el signo"** (H12 → H12′) | R5 → R8, A, B y C | Corrección ante un contraejemplo común (`larva_blanca` blanda y venenosa). Es lo más parecido a desaprendizaje colectivo que hubo. |
| **Triplete (familia, textura, ronda) con peso 0.85–0.92** | R6 → R8, los tres | Convergieron al mismo número. Ver H-8: probablemente porque el triplete es tan flexible que no puede fallar. |
| **"La puerta del miedo es una trampa cognitiva"** | R3 (C6 post-mortem) → R8, los tres | La corrección **estratégica** más valiosa, y la única con un evento detrás (la única muerte). Coincide con E-2, que el repo confirma con números. |
| **"El canal es asimétrico y hay que acusar recibo"** | R1 → R8, unánime, 8 rondas | Convergencia **total y equivocada**: el BLOQUE 4 real muestra que sin ACK el mensaje ya cambia la conducta (15/15 contra 0/15). **Convergencia no es verdad.** |

### D.2 No convergió

| desacuerdo | posiciones | por qué importa |
|---|---|---|
| **Mecanismo del mundo** | A: "responde a la densidad de energía del grupo" (H13) · B: "familia × ronda determinista" · C: "período-2 cíclico, con FFT" | Nunca se resolvió y **cada grupo heredó su versión a Gen3**. Es ERR-35 social (E-8): con lo que cada uno veía, las tres ajustan. |
| **Ruido de herencia** | ±2-3 % · ±5 % · ±10 % · ±15 %; A propone ±5 % si sobrevive y ±20 % si muere; B propone mutación dirigida por pesos de M3; C propone heredar **deltas** y no valores absolutos | Cuatro valores, **ninguno derivado de nada**. La propuesta de C (heredar deltas) es la única con contenido, y en el repo equivale a la pregunta abierta de H-7. |
| **Protocolo contra la mentira** | A: honestidad-tax −0.5 · B: firma del emisor con el código privado de 3 celdas · C: cuota mínima de emisión ≥1/ronda | Tres protocolos incompatibles para un problema que el instrumento no tiene (E-12). |
| **Tamaño de población necesario** | C: "≥8 con canal bilateral 100 %" · B: "10 es insuficiente, escalabilidad falsa" · A: no lo menciona | Nadie lo derivó. La respuesta real la da la calibración de `R₀` (H-1), no una intuición. |
| **Retención de M2** | 100 episodios · FIFO ~30 · persistir a disco | Sobre un órgano que no existe (E-10). |

### D.3 La recalibración que **nadie** hizo, y es la que importa

**Ningún grupo bajó nunca el peso de una hipótesis por coste.** Sólo H4 y H11 murieron, y las dos por contraejemplo
directo. La confianza agregada subió monótona de R1 a R7 (0.70 → 0.95) sobre cero mediciones, y sólo bajó en R8 cuando se
anunció que era la última ronda. **La simulación no tiene selección ni de células ni de ideas — y eso es E-1 otra vez, un
piso más arriba.** En el repo pasa lo contrario, y por eso el repo avanza despacio y de verdad: *"11 bloques, 21 series,
≈3 200 corridas, 8 ERR, 0 entradas al tronco"*.

---

## E. LO QUE LA SIMULACIÓN NO PUEDE DECIR

1. **Ningún número de esta carpeta es una medición.** Todo δ, todo 0.92, todo `r` lo escribió un agente. La prueba
   interna: el mismo token da recompensas distintas en células del mismo grupo en la misma ronda (`larva_rosa` +0.05 /
   +0.25 / +0.68 en R8; `baya_negra` Δ=+1.8 / +5 en R2). En un mundo con una semilla eso sería imposible.
2. **Los agentes tienen lenguaje, memoria de trabajo y razonamiento que el organismo no tiene.** M3 es prosa: el tronco no
   puede representar *"H13, confianza 0.85"*. Todo lo que dependa de M3 — que es casi todo el nivel 8 hacia arriba — **no
   es transferible en ninguna forma**.
3. **Los agentes no pueden ser ignorantes.** Cada célula sabía que tenía un "rasgo", que había "8 rondas", que existía un
   "grupo B" y cuál era la misión. Una célula real no sabe nada de eso. **Eso solo invalida toda afirmación sobre el nivel
   9 (modelo de sí):** el modelo de sí vino del enunciado.
4. **Cero selección.** 1 muerte en ~1 920 exposiciones (5·10⁻⁴). En el tronco real el anillo mata **124–159 por 100 000
   pasos** y la mini acumula **5 740 encuentros con veneno**. La sala 4 corrió un mundo sin coste, y en un mundo sin coste
   **evolucionar no es una palabra con referente**.
5. **El grupo nunca tuvo una tarea que una célula sola no pudiera hacer** — que es literalmente la definición del nivel
   10. Declararlo "PASÓ" (`ANALISIS_A_r7`, `r8`) es infalsable por construcción.
6. **Proponer no cuesta y refutar tampoco**, así que las hipótesis crecen sin techo (6 → 15) y las confianzas sólo suben.
   La sala no puede decir **cuál** hipótesis vale: sólo cuáles se le ocurrieron a doce lectores.
7. **El canal simulado era gratis.** En el organismo, **una sola entrega reelige la ganadora de las 66 celdas** y con ello
   mueve la lectura de **todo lo demás** — el control R-SIN-SAL, que mide ese daño colateral, **todavía no existe**
   (`PROTOCOLO_canal` §5.5). Ninguna célula podía siquiera plantear el problema.
8. **La sala no sustituye a leer el instrumento.** Doce lectores independientes **no** encontraron el techo de 2 bits
   (E-7) ni la trampa 3 del muestreo (E-9), y ambos están en el código y medidos. Lo que la sala encuentra es lo que se
   ve **desde dentro de la conducta**; lo que está en la arquitectura, no.
9. **Y lo simétrico, que es el valor real:** la sala destapó en la ronda 2, sin que nadie se lo dijera y con doce voces
   distintas, el bloqueo que el proyecto tiene escrito como **M4 + M7** — muerte que no mata y descendiente que se cuenta
   sin instanciarse. Eso **sí** es información: significa que el bloqueo es visible desde cualquier ángulo y que ya no
   tiene excusa.

---

## Cierre honesto

**Nivel real alcanzado por el grupo: 4** (memoria persistente entre rondas y generalización con desdecirse; el 5 a medias
porque la referencia nunca se resolvió; del 6 arriba, narración).

**¿Esto acerca a evolucionar?** No por sí mismo — no se midió nada y un mundo sin muerte no puede seleccionar nada. Pero
acerca por un camino lateral y real: doce lectores independientes, sin ver el código, pusieron el dedo en la ronda 2
sobre el mismo bloqueo que el repositorio tiene numerado (**la muerte no mata, el descendiente no se instancia**), y ocho
rondas después seguían tropezando con él. **Lo siguiente no es otro órgano ni otra sala: es `R₀` sin el regalo del
renacer (H-1). Si ese número no existe, "evolucionar" no tiene referente y todo lo demás es vocabulario.**

*Sintetizador de la sala 4, 18 sep 2026. Nada de este archivo es evidencia; todo número real que cito lleva su bloque, su
fecha y su serie.*
