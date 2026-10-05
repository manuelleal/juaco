## 7. Lo que funciona, resultado por resultado

**Idea principal.** Hay once resultados declarados con serie y réplica. Se dividen en dos clases que **nunca** deben mezclarse al hablar:

- **Selección:** algo que nadie escribió a mano y que apareció porque los que lo tenían duraron más. Son cuatro: ECO_SEL, BLOQUES (el órgano de rechazo), el termostato en la pista y perillas. En los cuatro, la selección trabajó sobre piezas o números que alguien le dejó disponibles.
- **Diseño:** un módulo escrito por un ingeniero (un agente de inteligencia artificial en ese papel) y medido contra un control. Son todos los de la Escalera (P1, P7, P10, "juntos no suman", PISA, P8-COMP2), que valen "en el mundo con oasis", y además TERMO, que es una regla diseñada para la pista vieja.

"×2" significa: serie de 20 semillas más réplica de otras 20 semillas nuevas, con la misma regla escrita antes. "De 180" son nueve linajes por veinte semillas. Cada ficha cita el registro (`registro/REGISTRO_etapas_1_2.md`).

### 7.0 El punto de partida: O1 cruza (22 de septiembre)

No está en la lista pedida pero todo se apoya en él. En la pista vieja, nueve linajes O1 juntos sostienen un R0 real mediano de **0.941**, replicado en semillas selladas y con la memoria del fundador borrada (148 de 180). O1 solo no cruza (0.681). Sin limpieza, 0 de 180 (con la regla vieja de fundador). **Es diseño**: lo escribió un agente. Reserva obligatoria: el margen sobre el umbral 0.90 es de 4.5 puntos, no de 74 como pareció antes de corregir la medida (ERR-100); y no se pudo separar "compañía" de "abundancia de un mundo más grande".

---

### 7.1 TERMO: una regla de boca lleva al tronco hasta la altura de O1 — HAY ALGO MODESTO ×2 (diseño)

| | |
|---|---|
| Pregunta | ¿Una sola regla local de boca, sin memoria nueva, hace que el organismo del tronco (v14.3) cruce en la pista? |
| Montaje | La regla: ante una letra buena, morder sólo si la necesidad que sube está por debajo del umbral de parto más la mitad de lo que la letra da. Es el mismo principio que MARGEN en O1. Series 39101–39120 y 39121–39140. |
| Números | R0 real mediano: tronco 0.610 y 0.590; con TERMO **0.923 y 0.932**; O1 0.938 y 0.933. Semillas con mayoría de linajes que cruzan: TERMO 14 de 20 y 13 de 20; O1 20 y 19. |
| Control que pudo ganar | La misma regla leyendo la necesidad equivocada: se hunde (0.127 y 0.119). |
| Por qué "modesto" y no "funciona" | La regla escrita antes pedía mayoría en 15 de 20 semillas. Sacó 14 y 13. No se movió el umbral. |
| Frase que sí se puede decir | "TERMO iguala a O1 en R0 real mediano; cruza en la mediana, no en la puerta estricta." |
| Reservas | La constante "la mitad" salió de una exploración (declarado). El candidato no pasó el examen completo para entrar al tronco (falla una puerta, la de reversión). |
| Diseño o selección | Diseño. |

### 7.2 La selección encuentra el termostato en la pista — FUNCIONA ×2 (selección sobre una perilla)

| | |
|---|---|
| Pregunta | Si el margen del termostato es un gen que arranca en la zona letal (menos de 0.10), ¿la selección lo sube sola hasta la zona que funciona? |
| Montaje | 10 pasajes de 25 000 pasos: lo vivo al final de uno siembra el siguiente, sin juez. Prueba final a 100 000. 20 cadenas, serie y réplica. |
| Números | El gen sube de menos de 0.10 a la banda entre 0.10 y 0.60 en **20 de 20 ×2**. El organismo resultante le gana al tronco en 20 de 20 y 18 de 20, y al mismo carro sin transferencia en 19 y 20 de 20. R0 real 0.890 y 0.934. |
| Control que pudo ganar | El mismo carro sin pasar lo vivo de un pasaje al siguiente: se queda en 0.02 (0 de 20 en la banda). |
| Frase que sí se puede decir | "La selección lleva sola el margen de la zona letal a la banda en 20 de 20, dos veces, y le gana al tronco y al control sin transferencia; empata con el termostato diseñado." |
| Reservas | **No cruza el muro**: mayorías 10 y 12 de 20 contra 19 de O1. No supera al termostato diseñado (le gana en 8 de 20). Los fundadores por linaje siguen muy por encima de los de O1 (79–87 contra 37–38). |
| Diseño o selección | Selección, sobre una perilla que el ingeniero dejó puesta. |

### 7.3 ECO_SEL: la selección sube la capacidad de carga de un linaje — FUNCIONA ×2 (selección)

| | |
|---|---|
| Pregunta | En un linaje que ya se sostiene solo en el mundo ECO, ¿la selección sobre rasgos heredables sube cuántos cuerpos mantiene el mismo flujo de comida? ¿Y es la herencia la que lo hace, no la simple variación? |
| Montaje | Mundo ECO con población real, un millón de pasos. Dos versiones: muta sólo el umbral de parto ("M") o mutan 15 genes del cerebro ("C"). |
| Números | Capacidad K: sin selección 30.85 y 31.01. Con el umbral heredable **34.91 y 34.74**. Con el cerebro heredable **38.94 y 39.23**. Cada una le gana a la base en 20 de 20, serie y réplica. |
| Control que pudo ganar | Los mismos genes mutando **sin herencia**: K baja (20.19 y 24.46; 25.65 y 23.01). Es decir, variar sin heredar empeora. |
| Frase que sí se puede decir | "La selección natural sube la capacidad de carga del linaje, de unos 31 a unos 35 y a unos 39 cuerpos, con el mismo flujo de comida." |
| Reservas | Sólo en ECO. Con diez veces más tiempo K no sigue subiendo (una serie en la nube). Trasplantado a la pista, el genoma seleccionado **empeora** al organismo. La caída de muertes por veneno y sal (de 82 % a entre 2 y 3.5 %) es descriptiva. |
| Diseño o selección | Selección. Fue la primera capacidad del proyecto que ningún diseñador puso. |

### 7.4 BLOQUES: la selección arma un órgano de rechazo — FUNCIONA ×2 (selección)

| | |
|---|---|
| Pregunta | Si el genoma está hecho de reglas que se pueden armar con piezas (un sensor, una comparación, una acción, un peso) y esas reglas se pueden mutar, duplicar, borrar o copiar del vecino, ¿la selección arma algo que supere a los 15 genes fijos? Idea del director: "que funcione como Minecraft". |
| Montaje | Mundo ECO, hijos que nacen sin saber nada, criadero sólo hasta el paso 100 000, corrida de 500 000. |
| Números | El linaje persiste en **19 de 20 ×2** con reglas armables; 14 y 13 con 15 genes fijos; 1 y 0 sin herencia; 0 y 0 sin selección. Una regla de rechazo aparece en la mitad o más de los vivos en 19 y 18 de 20 semillas. |
| Qué armó | Una regla que dice, en esencia, "no muerdas si el objeto que tienes enfrente muestra tal píxel", y ese píxel separa exactamente veneno y sal de comida y agua. Además aparece **duplicada** dos o tres veces: la copia refuerza la función. |
| Control que pudo ganar | Las mismas reglas sin herencia (1 y 0 de 20). Y una explicación alternativa que el auditor descartó: no es que el mundo le regalara comida; vive con **menos** comida accesible que el otro brazo. |
| Frase que sí se puede decir | "Con un genoma de reglas componibles, la selección natural fija sola un órgano de rechazo heredable que sostiene al linaje sin criadero." |
| Reservas | Es un **instinto**, no aprendizaje: las letras significan siempre lo mismo y la regla quedó atada a esa identidad. Un solo mundo simulado. "Órgano" aquí quiere decir una regla heredable, nada más. |
| Diseño o selección | Selección. |

---

### 7.5 P1, memoria de lugar — FUNCIONA ×2 (diseño; en el mundo con oasis)

| | |
|---|---|
| Pregunta | En el mundo con oasis, ¿O1 con una libreta de sitios cruza más que O1 a secas y que un control con la misma libreta leída en el sitio equivocado? |
| Montaje | 30 casillas; anota lo que cada sitio dio de más; cuando no ve nada, viaja al sitio recordado. Series 739001–739020 y 739101–739120. |
| Números | Linajes que cruzan, de 180: con memoria **79 y 85**; control **0 y 0**; O1 sin módulo 7 y 7. Gana en 20 de 20 semillas contra ambos, las dos veces. Tiempo dentro del oasis respecto del azar: 7.25 veces y 7.26 veces (O1: 1.05). |
| Control que pudo ganar | El "antípoda": escribe en la casilla correcta y lee en la del lado opuesto del anillo. Mismo esfuerzo de viajar, siempre al lugar equivocado. Sacó 0. |
| Frase que sí se puede decir | "En el mundo con oasis, un organismo con memoria de lugar recuerda dónde le fue bien y pasa más tiempo allí; cruzan 79 y 85 de 180 contra 0 del control." |
| Reservas | El mundo se ajustó hasta que el módulo ganó en dos semillas (ERR-171). El primer control tenía una fuga: cerca del 45 % de las veces leía el oasis; se corrigió antes de la serie (ERR-170). Prohibido: "vuelve", "aprende el mapa", "cruza el muro". No se compara con la pista vieja. |
| Diseño o selección | Diseño. |

### 7.6 P7, señal con significado dado, con costo — FUNCIONA ×2 con reserva (diseño)

| | |
|---|---|
| Pregunta | Si los linajes anotan en la pizarra dónde les fue bien, y anotar cuesta, ¿les va mejor que a los mudos y que a los que leen lo mismo pero lo anotan en el sitio equivocado? |
| Montaje | Nueve linajes idénticos. Cada anotación cuesta 0.01 de energía. Series 739601–739620 y 739651–739670. |
| Números | Cruzan de 180: con señal **132 y 124**; mudos 80 y 81; control 49 y 50. Fundadores por linaje: 3.0 y 4.3 con señal contra 28.4 y 28.5 mudos. |
| Control que pudo ganar | El que lee al antípoda: emite igual, paga igual, y siembra el lugar equivocado. Queda **por debajo** del mudo. |
| Frase que sí se puede decir | "En el mundo con oasis, una señal con significado dado por el diseño, entre linajes clones y con costo de emitir, hace que más vidas lleguen al oasis y que crucen más linajes." |
| **Reserva obligatoria (ERR-175)** | La medida del mecanismo se cambió de "llegan antes" a "llegan más vidas" **después** de ver una prueba corta y antes de la serie. Con la medida original no pasa (5 de 20 y 6 de 20). Lo medido es que la señal no hace llegar antes: hace llegar a más. |
| Otras reservas | Los que leen son clones del que escribe: el beneficio queda en casa. En una pista con rivales, el beneficio iría al rival. El significado no surgió: lo puso el ingeniero (y está medido desde septiembre que no surge solo por refuerzo). Prohibido: "comunicación" a secas, "lenguaje", "mensaje", "coopera", "aprende de otros". |
| Diseño o selección | Diseño. |

### 7.7 P10, ir a lo menos visitado cuando el oasis se muda — FUNCIONA ×2 (diseño)

| | |
|---|---|
| Pregunta | Si el oasis cambia de sitio, ¿un organismo que olvida el sitio donde ya no hay nada y va al lugar que hace más tiempo no visita encuentra antes el oasis nuevo y cruza más? |
| Montaje | El oasis se muda cada 20 000 pasos. Series 739821–739840 y 739851–739870. |
| Números | Cruzan de 180: **164 y 163**; sólo memoria 82 y 91; control 53 y 65. Mayoría de linajes en **20 de 20 ×2**. R0 real mediano 0.96. Pasos hasta el primer bocado en el oasis nuevo: 442 y 459 contra 1242 y 1280. Linajes que nunca llegan: 0 contra 22 y 27. |
| Control que pudo ganar | El que va al lado opuesto del sitio elegido. |
| Frase que sí se puede decir | "En el mundo donde el oasis se muda, ir al lugar del que hace más tiempo no se tiene dato, junto con olvidar el sitio que ya no da, hace llegar antes al oasis nuevo; cruzan 164 y 163 de 180." |
| Reservas | El control es **pesimista** (manda lejos sin información), no de igual costo. El efecto es del conjunto de dos piezas; no se separaron. El oasis nunca vuelve al mismo sitio, lo que favorece a la regla. El organismo deja el mundo más pelado (comida presente entre 0.67 y 0.69 de la base). Prohibido: "curiosidad", "se pregunta" como experiencia interna. |
| Diseño o selección | Diseño. |

### 7.8 Los tres juntos NO SUMAN — NO ×2 (diseño; un negativo declarado)

| | |
|---|---|
| Pregunta | Si se ponen memoria, señal e ir a lo menos visitado en un mismo organismo, ¿cruza más que cada pareja? |
| Números | Cruzan de 180 (serie y réplica): los tres **159 y 169**; memoria + ir a lo menos visitado 163 y 163; memoria + señal 129 y 129; sólo memoria 88 y 95; los tres con la señal leída al antípoda 90 y 95. |
| Lectura | La señal no agrega cruce sobre "memoria + ir a lo menos visitado". No se estorban. El contenido de la señal sí importa: leída al revés, hunde al conjunto hasta el nivel de "sólo memoria". |
| Reserva | El preregistro avisó antes de correr de un posible efecto de techo: la mejor pareja ya cruzaba casi todo, así que quedaba poco espacio para ver una suma. "No suman" no es "se estorban". |
| Frase que sí se puede decir | "Tres módulos diseñados, cada uno contra un control de contenido equivocado; juntos no suman." |

### 7.9 PISA: la señal leída puede pisar memoria caducada — FUNCIONA ×2 con reservas (diseño)

| | |
|---|---|
| Pregunta | El resultado anterior tenía una causa visible: los lectores rechazaban casi todo lo que apuntaba al oasis nuevo porque "ya conocían" ese sitio. Si se les permite creerle a la pizarra cuando su propio recuerdo ya no vale, ¿llegan antes? |
| Montaje | Un linaje explora y escribe; ocho leen. Se mide la mediana de pasos que tardan los ocho lectores en llegar al oasis nuevo. Series 738641–738660 y 738671–738690. |
| Números | Lectores con PISA y explorador que habla: **973.5 y 982.5 pasos**. Lectores sin PISA: 1317.8 y 1205.5. Con PISA mejor en 15 de 20 y 17 de 20 semillas (el corte era 14). Razón 0.78 las dos veces. |
| Controles que pudieron ganar | Lectores que leen al antípoda (1457 y 1516). Explorador mudo (1566 y 1315). |
| Frase que sí se puede decir | "En el mundo con oasis que se muda, una señal con significado dado, leída por lectores que borran la marca de un sitio ya caducado, hace llegar antes al oasis nuevo a los lectores cuando un explorador la emite; diseño, no selección." |
| **Reservas obligatorias** | (1) La serie quedó **en el umbral** (15 contra un corte de 14); por eso se corrió la réplica, que pasó con holgura. (2) Los dos brazos no viven en el mismo mundo: comida presente 7.8 contra 6.3. (3) Con el explorador mudo y un mundo igual de rico, los lectores con PISA son **más lentos** que los originales con explorador que habla: la ventaja no es de la variante sola. (4) El cruce de los lectores mejora (140 y 143 contra 117 y 126, de 160) pero **no depende de que el explorador hable**. (5) "Rumor": entre el 15.8 % y el 18.2 % de lo pisado apuntaba al oasis viejo; no se midió daño. |
| Diseño o selección | Diseño (una línea de código). |

### 7.10 P8, celda retenida: COMP2 — FUNCIONA ×2 y MEJORA ×2, con reservas (diseño)

| | |
|---|---|
| Pregunta | Un linaje conoció la letra E sólo **fuera** del oasis, y conoció el oasis sólo con comida y agua. Nunca vio una E dentro del oasis (esa combinación, o "celda", se le retuvo a propósito). Cuando se le presenta por primera vez, ¿decide morderla dentro y no fuera? |
| Montaje | Se cría el linaje 60 000 pasos en un mundo donde la E nunca nace dentro del oasis. Después se le "pregunta" con situaciones sintéticas, sin mundo: una E a un paso y una comida visible diez celdas más allá. La medida D = probabilidad de morder la E dentro menos probabilidad de morderla fuera. |
| Números | COMP2: D mediana **0.75 y 0.75**; mayor que cero en **20 de 20 ×2**. Con la memoria de lugar barajada: 0. Sin el módulo: 0. COMP2 mejora a la versión anterior (COMP) en 17 de 20 y 20 de 20, por +0.50. |
| Lo que no pasó | La versión anterior, COMP, dio "modesto" en la serie y "no" en la réplica: **no se declara**. |
| Frase máxima permitida | "En el mundo con oasis, en celda retenida, con una suma cableada letra + recuerdo del sitio y una compuerta cableada, un linaje que sólo vivió E fuera la muerde dentro del oasis aun con comida a la vista, porque su memoria de lugar tiene recuerdo ahí; con la memoria de lugar barajada, no." |
| **Reservas obligatorias** | (1) La suma y la compuerta las puso el ingeniero a mano. Lo empírico es sólo que la memoria tenga recuerdo en las casillas del oasis. (2) D mide "la E le gana a una comida visible dentro y no fuera"; con la E sola, se la muerde 57 % de las veces **fuera** en todos los brazos. No es "no la muerde fuera". (3) Una puerta de la regla se enmendó tras una prueba corta y antes de la serie (ERR-179): con la puerta vieja el veredicto sería NO (0.72 y 0.70 contra un corte de 0.90). (4) No mide supervivencia. No se detecta costo de cruce y no se descarta (97 contra 113 sumando las dos corridas). (5) Un cálculo descriptivo del runner tenía un defecto que no cambia veredictos (ERR-190). |
| Prohibido | "Compone", "razona", "descubrió", "aprendió la compuerta", "no la muerde fuera", "mejor supervivencia". |
| Diseño o selección | Diseño. |

### 7.11 Perillas: la selección sube la perilla del viaje — FUNCIONA ×2 (selección sobre un módulo diseñado)

| | |
|---|---|
| Pregunta | El módulo de memoria de lugar lo escribió el ingeniero. Si nace **apagado**, con sus dos perillas en cero, ¿la selección lo prende sola en el mundo que lo paga? ¿Más que el puro azar? |
| Montaje | Dos genes por cuerpo (GW: peso del recuerdo en el valor; GV: ganas de viajar). Una mutación pequeña por nacimiento con sesgo a apagarse. Cámara continua. 5 pasajes de 100 000. 20 cadenas pareadas. Prueba final con un solo genoma: la mediana de cada cadena. |
| Números | GV mediano: selección **0.1939 y 0.1914**; deriva 0.023 y 0.0. Selección por encima de deriva + 0.05 en **19 de 20 y 20 de 20**. Linajes que cruzan, de 180: selección **79 y 70**; deriva 14 y 7; diseño completo 80 y 83; O1 6 y 4. |
| Control que pudo ganar | La deriva: la misma cadena, mismas semillas, mismas mutaciones, pero ningún cuerpo usa los genes. Pudo ganar si el gen subía por azar. No subió. |
| Control interno | GW, la perilla que ese mundo casi no paga, **no sube** (0.0107 y 0.0001). La selección prendió la que paga y no la otra. |
| Frase que sí se puede decir | "En el mundo con oasis de P1, la selección por persistencia sube desde cero la perilla del viaje de la memoria de lugar, la deriva no, y el genoma que deja la selección cruza más que el que deja la deriva." |
| **Reservas obligatorias** | (1) **Mundo pelado:** la selección deja 4.32 y 4.44 de comida presente contra 7.03 y 6.95 de O1. Parte de la ventaja puede venir de vaciar el oasis. Esta reserva va en la misma frase que el resultado. (2) **Una evidencia, no dos:** como la deriva queda casi en cero, "cruza más que la deriva" equivale casi a "con GV de 0.1 o más se cruza más que O1", que ya se sabía por diseño. (3) Se queda en el **primer escalón** (0.19), no llega al diseño (1); en la réplica cruza algo menos que el diseño (gana 5, empata 4, pierde 11). (4) Serie y réplica comparten el mismo código: un bloque, no dos experimentos independientes en método. (5) **El módulo lo escribió el ingeniero; la selección sólo prende su perilla.** |
| Prohibido | "Evoluciona la memoria", "inventa", "aprende a recordar", "la selección supera al diseñador", y toda comparación con el muro. |
| Diseño o selección | Selección sobre un módulo diseñado. |

---

### 7.12 Otros dos declarados que conviene tener a mano

- **Arranque en frío (F1), 25 de septiembre, FUNCIONA ×2.** En ECO, un linaje arranca desde 90 fundadores que no saben nada y se sostiene un millón de pasos sin criadero, cuando la familia le pasa al hijo sólo lo que tuvo consecuencia. 20 de 20 las dos veces; con la tabla barajada, 1 de 20; sin familia, 0. No se traslada a la pista (allí dio NO).
- **ECO_SEL con hijos ingenuos, 28 de septiembre, FUNCIONA ×2.** Aunque los hijos nazcan sin la tabla aprendida, la selección sobre 15 genes baja los fundadores necesarios entre 31 % y 32 %.

### 7.13 El patrón que une todo

Lo dijo el cierre del 28 de septiembre y se mantiene: con números fijos la selección se estanca rápido; con más genes el techo sube; **con piezas que se pueden armar y duplicar, o con un módulo ya escrito que sólo hay que prender, la selección hace trabajo real.** Lo que la selección no ha hecho en ningún montaje es inventar una combinación nueva de varias piezas a la vez.
