## 4. Cada perilla, una ficha por perilla

**Idea principal.** Una "perilla" es un número escrito en el código que alguien pudo haber puesto distinto. JUACO tiene cuatro familias de perillas: las del cuerpo O1 (cinco números y dos reglas), las de los módulos que el ingeniero le agregó en la Escalera, las del mundo, y las del aparato con que se hace selección. De casi ninguna se sabe cuál es su mejor valor: la mayoría se fijó una vez y nunca se barrió. Sólo dos tienen evidencia medida de qué pasa al moverlas: MARGEN (en el mapa del muro, exploratorio) y GV (en "perillas", declarado con serie y réplica). Cada ficha dice con franqueza cuál es el caso.

**Cómo leer una ficha.** "Valor de fábrica" es el que trae el archivo. "Barrida" significa que se probó con varios valores y se miró el resultado. "Mapa del muro" es una sonda del 1 de octubre (`experimentos/organelos/muro_perillas/`): genomas fijos, pista vieja, nueve linajes, 100 000 pasos, una o dos semillas (883001 y 883002). **Es exploración: orienta, no declara nada.** Además, todo el mapa corrió con "fundador limpio", que tiene un problema pendiente (candidato ERR-191, explicado en la ficha de LIMPIA y en la sección 9). "Cruzan N de 9" quiere decir: cuántos de los nueve linajes de esa corrida cumplieron el criterio de cruce (sección 5).

Recordatorio mínimo de vocabulario: el cuerpo tiene dos niveles, energía (E) y agua (Ag), que bajan solos 0.001 por paso; puede parir cuando los dos pasan 500 pasos seguidos en 1.0 o más (ese 1.0 es el "umbral de parto", que en el código se llama `rep_umbral` y O1 guarda como `U`).

---

### 4.1 Las perillas del cuerpo O1 (`experimentos/carrera_escuderias/carros/O1.py`)

O1 tiene cinco constantes con nombre (líneas 25 a 29), una tabla de urgencias sin nombre (línea 61) y dos reglas que el mapa del muro trató como interruptores (limpieza y hueco).

#### MARGEN

| | |
|---|---|
| Nombre en el código | `MARGEN` (línea 25; se usa en las líneas 60 y 100) |
| Valor de fábrica | 0.25 |
| Qué hace | Fija hasta qué nivel sigue comiendo lo bueno: muerde una letra buena sólo si la necesidad que esa letra sube está por debajo de 1.0 + MARGEN, es decir, por debajo de 1.25. También decide cuándo se activa la limpieza: sólo si alguna necesidad está por debajo de 1.25. |
| Imagen cotidiana | El termostato de una nevera. No basta con "llenar hasta la raya": se llena un poco por encima de la raya para que, mientras baja, alcance a durar. La raya es el umbral de parto (1.0); MARGEN es el "poco por encima". |
| Si lo bajas | Con MARGEN 0 el cuerpo deja de comer justo en la raya. Como los niveles bajan solos, nunca logra sostener 500 pasos seguidos sobre 1.0: no pare y el linaje se extingue. |
| Si lo subes | Come aunque esté lleno. Gasta comida que no necesita (el tope físico es 1.5) y se la quita a los demás. |
| Evidencia | **Mapa del muro, dos semillas (exploratorio).** Cruzan de 9, con el resto en fábrica: MARGEN 0 → 0 y 0; 0.03 → 0 y 4; 0.06 → 3 y 8; 0.10 → 8 y 9; 0.25 (fábrica) → 4 y 8; 0.5 → 5 y 5. Es una **rampa**: cada pasito paga algo; no hay un escalón que haya que saltar de golpe. Desde "todo apagado", prender sólo MARGEN ya da 5 y 6 de 9. |
| Otras evidencias | El termostato (sección 7) es la misma idea puesta en el organismo del tronco: comer con una consigna estrictamente por encima del umbral de parto. Allí está declarado con serie y réplica que "consigna en el umbral = extinción" y que la selección sube sola esa consigna desde la zona letal. En `o1_evo` MARGEN fue uno de los cuatro genes: la selección no lo mejoró desde fábrica (el conjunto dio 128 linajes contra 135 de fábrica). |
| Lo que no se sabe | Si el valor de fábrica es el mejor: en el mapa, 0.10 dio más que 0.25 en las dos semillas, pero son dos semillas. Es el candidato para el próximo experimento con protocolo ("perillas del muro": MARGEN como gen desde cero). |

#### PRUEBA

| | |
|---|---|
| Nombre en el código | `PRUEBA` (línea 26; se usa en las líneas 67 y 92) |
| Valor de fábrica | 0.5 |
| Qué hace | Una letra que el linaje nunca ha mordido se prueba una sola vez, y sólo si energía y agua están las dos por encima de 0.5. |
| Imagen cotidiana | Probar una fruta desconocida en el monte: sólo cuando uno está bien comido y bien hidratado, por si cae mal. |
| Si lo bajas | Prueba aunque esté débil; si la letra era veneno (quita 0.4), puede morir en el intento. |
| Si lo subes | Casi nunca prueba; tarda en saber qué es cada letra. Como un recién nacido arranca con 0.6 en cada nivel, con PRUEBA por encima de 0.6 no probaría nada hasta haber comido. |
| Evidencia | Mapa del muro: un solo punto, una semilla: PRUEBA 0 → 6 de 9 (sin diferencia legible con fábrica). En `o1_evo` (una serie, sin réplica) la selección la **bajó** en 19 de 20 cadenas sin ganar cruce. El genetista de la junta cita una tabla vieja donde quitar la prueba no cambia nada (0.935 contra 0.928) [sin verificar por mí: lo tomo de `FABLE_gen_perdido.md`]. |
| Estado | Sin tendencia medida. No se ha barrido con protocolo. |

#### PEN_OTRO

| | |
|---|---|
| Nombre en el código | `PEN_OTRO` (línea 27; se usa en la línea 97) |
| Valor de fábrica | 0.35 |
| Qué hace | Al elegir a dónde ir, si otro cuerpo está estrictamente más cerca de ese objeto, su puntaje se multiplica por 0.35. |
| Imagen cotidiana | No correr hacia la última empanada de la mesa si otro ya tiene la mano encima: probablemente se la lleva y uno pierde el viaje. |
| Si lo bajas (hacia 0) | Renuncia por completo a lo que otro tiene más cerca. |
| Si lo subes (a 1) | No tiene en cuenta a los demás: persigue aunque vaya a perder. |
| Evidencia | Mapa del muro: un punto, una semilla: PEN_OTRO 1.0 → 5 de 9. En el lote "desde todo apagado", agregar PEN_OTRO sobre MARGEN + limpieza + PISO dejó 7 y 6 de 9 (igual o peor que sin él: 7 y 7). |
| Estado | Sin tendencia. Nunca barrida con protocolo. |

#### D0

| | |
|---|---|
| Nombre en el código | `D0` (línea 28; se usa en la línea 96, y los módulos de lugar lo reutilizan) |
| Valor de fábrica | 3.0 |
| Qué hace | Suaviza la distancia en el puntaje de cada objeto: puntaje = ganancia / (distancia + 3). |
| Imagen cotidiana | Decidir entre la tienda de la esquina y el supermercado lejano. Sin el "+3", algo que está pegado a uno ganaría siempre aunque valga poquísimo; con él, la cercanía pesa pero no aplasta todo lo demás. |
| Si lo bajas | Se vuelve miope: va a lo más cercano casi sin mirar cuánto vale. |
| Si lo subes | La distancia deja de importar: cruza medio mundo por algo un poco mejor. |
| Evidencia | **Nunca se ha barrido.** En `o1_evo` se dejó fija a propósito ("no es una decisión de comer o limpiar"). Tampoco fue gen en el mapa del muro. |

#### PISO

| | |
|---|---|
| Nombre en el código | `PISO` (línea 29; se usa en la línea 78) |
| Valor de fábrica | 0.2 |
| Qué hace | Límite de seguridad de la limpieza: el cuerpo no muerde algo malo si el golpe dejaría la necesidad golpeada por debajo de 0.2. (Si en ese momento está corriendo la ventana de parto, el límite es más exigente: no puede bajar del umbral de parto.) |
| Imagen cotidiana | Donar sangre sólo si después de donar uno queda por encima de un mínimo seguro. |
| Si lo bajas (a 0) | Limpia aunque quede al borde de morir. |
| Si lo subes (a 1) | Casi nunca limpia: sólo cuando está muy lleno. |
| Evidencia | Mapa del muro, una semilla: PISO 0 / 0.2 / 0.4 / 0.6 / 1.0 → 8 / 4 / 3 / 8 / 7 de 9. No hay tendencia: es ruido de una semilla. |
| Otra evidencia, más interesante | En `o1_evo` la selección **subió** PISO (más 0.044; en 17 de 20 cadenas, contra 5 de 20 del control neutro) y en "O1 libre" lo subió en 10 de 10 cadenas, dos veces. Subir PISO es "limpiar menos hondo". El genetista lo lee como posible firma de un aprovechado (el que limpia paga, los vecinos cobran). **Esa lectura es una hipótesis sin medir**: la señal dentro de cada semilla es débil y el registro dice expresamente que "no se puede leer". |

#### La tabla de urgencias (sin nombre)

| | |
|---|---|
| Dónde está | Línea 61: `u = 4.0 if x < 0.3 else (2.0 if x < self.U else 1.0)`; y línea 62: la ganancia se recorta a `U + 0.5 − x` |
| Valores | Peso 4 si el nivel está por debajo de 0.3; peso 2 si está entre 0.3 y el umbral de parto (1.0); peso 1 si está entre 1.0 y 1.25. La ganancia que se cuenta nunca supera lo que cabe hasta el tope de 1.5. |
| Qué hace | Hace que lo que alivia la necesidad más urgente valga más al elegir a dónde ir. |
| Imagen cotidiana | El triaje de urgencias de un hospital: rojo, amarillo, verde. |
| Evidencia | **Nunca se ha barrido.** En `o1_evo` se dejó fija ("es una tabla, no un umbral"). |

#### LIMPIA (la regla de limpieza, tratada como interruptor)

| | |
|---|---|
| Dónde está | Líneas 72 a 81 (`_costeable`) y 99 a 107. En O1 no es un número: es una regla. El mapa del muro la convirtió en un gen llamado `LIMPIA` (activa si vale más de 0.5). El control `CTRL_O1_SINLIMPIA.py` es O1 con una sola línea cambiada (`limpia = False`). |
| Qué hace | Cuando no hay nada útil a la vista y el cuerpo tiene alguna necesidad por debajo de 1.25, muerde a propósito algo que sabe malo, siempre que el golpe caiga en la necesidad más llena y respete el PISO. Al desaparecer ese objeto, el mundo repone otro al azar, que puede ser bueno. |
| Imagen cotidiana | Sacar la basura del pasillo del edificio: a uno le cuesta, y el pasillo queda despejado para todos los vecinos. |
| Si la apagas | Con la regla vieja de fundador (el fundador conservaba la memoria del linaje): 0 de 180 linajes cruzan; el mundo se tapa de veneno y sal (78 % de los pasos sin nada bueno). Es el control de la serie sellada del 22 de septiembre. |
| **Cautela obligatoria** | Con **fundador limpio** (la regla que usan todas las series desde la ronda 2), el mismo organismo sin limpieza cruza 5 y 6 de 9 en el mapa. La explicación leída en los datos: cada fundador nuevo nace sin memoria y prueba el veneno y la sal una vez; los linajes que se hunden nacen y mueren sin parar, y con esas pruebas limpian el mundo gratis para los demás. Es el **candidato ERR-191, no abierto**. Mientras no se resuelva, **no se puede afirmar nada sobre la limpieza como hecho** más allá de la frase declarada en septiembre con su regla de fundador. |
| Otra evidencia | Mapa, desde todo apagado: prender sólo la limpieza da 0 y 0 de 9; prenderla con MARGEN ya puesto sube de 5 y 6 a 7 y 7. La limpieza suma sólo después de MARGEN. |

#### HUECO (la regla "sin blanco, ir al hueco mayor")

| | |
|---|---|
| Dónde está | Líneas 123 a 129 (`_hueco`), llamada en la línea 112. Gen `HUECO` en el mapa del muro. |
| Qué hace | Cuando no hay nada a qué ir, el cuerpo se coloca en el centro del espacio vacío más grande entre los otros cuerpos. |
| Imagen cotidiana | Un pescador que se para donde no hay otros pescadores: lo que aparezca por ahí le queda más cerca a él que a nadie. |
| Si la apagas | El cuerpo se queda quieto donde está. |
| Evidencia | Mapa del muro: HUECO apagado → 7 y 6 de 9. No se distingue de fábrica en dos semillas. **Nunca barrida con protocolo.** |

**Resumen honesto de O1.** De las siete piezas, sólo MARGEN muestra un efecto ordenado, y sólo en una sonda. PISO, PEN_OTRO, PRUEBA y HUECO no muestran tendencia. D0 y las urgencias nunca se tocaron. Y el 29 de septiembre se midió, con serie, que trasplantar piezas sueltas de O1 a otro organismo no hace cruzar: O1 funciona como conjunto.

---

### 4.2 Las perillas del módulo de memoria de lugar (peldaño P1; `escalera/carros/O1_LUGAR.py`, líneas 35 a 38)

El módulo divide el anillo en casillas ("bins") y anota en cada una cuánto dio ese sitio **de más** respecto de lo que su letra da en promedio.

| Perilla | Fábrica | Qué hace | Imagen | Si sube / si baja | Evidencia |
|---|---|---|---|---|---|
| `LUGAR` | 1 | Interruptor del módulo ("promotor"). Con 0 el organismo es O1 idéntico bit a bit. | El interruptor general de un aparato. | — | El arnés de identidad lo comprueba (37 de 37). |
| `LG_NB` | 30 | Número de casillas del anillo (cada una de 12 celdas en un anillo de 360). El oasis ocupa unas 4 casillas seguidas. | La cuadrícula de un mapa. | Más casillas: mapa más fino pero cada una se visita menos. Menos casillas: mapa borroso. | **Nunca barrida.** |
| `LG_ETA` | 0.5 | Velocidad con que se actualiza el recuerdo de una casilla: cada mordida mueve el recuerdo a mitad de camino entre lo que tenía y lo que acaba de vivir. | Una opinión sobre un restaurante que se corrige a medias con cada visita. | Más alto: sólo cuenta la última visita. Más bajo: memoria terca, lenta para corregirse. | **Nunca barrida.** |
| `LG_MIN` | 0.05 | Umbral: un recuerdo por debajo de 0.05 se trata como "nada". | El volumen mínimo para decir que se oyó algo y no fue el viento. | Más alto: ignora recuerdos débiles (viaja menos). Más bajo: persigue ruido. | No barrida directamente. Se usó como margen de la puerta de "perillas" (el gen debía superar al neutro por 0.05). |
| `LUGAR_W` (como gen: **GW**) | 1.0 | Peso del recuerdo del sitio en el **valor** de un bocado: valor = valor de la letra + GW × recuerdo del sitio. | Cuánto se le cree a la fama de un sitio al decidir si vale la pena lo que venden. | 0: la fama no cuenta. Alto: la fama pesa más que el producto. | **Medida en "perillas" como control interno:** la selección **no** la sube (mediana 0.0107 y 0.0001; sube en 1 de 20 cadenas). Con GW 1 y GV 0 cruza 1 de 9 (exploración, una semilla): en ese mundo esta perilla casi no paga. |
| `LG_VIAJA` (como gen: **GV**) | 1 | Ganancia del **viaje**: cuando no ve nada útil, va al sitio recordado, pero sólo si GV × recuerdo supera 0.05. | Las ganas de volver al sitio donde a uno le fue bien cuando alrededor no hay nada. | 0: nunca viaja (es O1). 1: viaja con cualquier recuerdo (el diseño). Valores intermedios: viaja sólo con recuerdos fuertes. | **La perilla mejor medida del proyecto.** Ver ficha abajo. |

#### GV, la perilla del viaje (ficha ampliada)

- **Qué se midió (declarado, serie y réplica, 1 de octubre).** Con el módulo escrito por el ingeniero pero naciendo apagado (GW y GV en 0), la selección por persistencia sube GV hasta una mediana de 0.19 en las dos corridas (0.1939 y 0.1914), mientras la deriva (el mismo aparato sin que los cuerpos lean el gen) lo deja en 0.023 y 0.0. La selección supera a la deriva por más de 0.05 en 19 de 20 y en 20 de 20 cadenas.
- **Qué pasa con cada valor (exploración, una semilla, genoma fijo).** Cruzan de 9 con GV 0.06 / 0.1 / 0.2 / 0.4 / 1.0: 1 / 4 / 5 / 4 / 4. Es decir: 0.06 no paga; desde 0.1 ya paga.
- **El efecto secundario (sonda "régimen", dos semillas, exploratoria).** Con GV intermedio (0.2) el mundo queda "pelado": la cantidad media de comida y agua presentes baja a entre 4.4 y 5.2, contra 7.3 sin módulo y 7.5 a 8.6 con GV 1. La lectura propuesta es que un "viajero a medias" va al oasis sólo con recuerdos fuertes y además sale a comer fuera. La relación entre GV y comida en el mundo tiene forma de U.
- **La frase que sí se puede decir.** "En el mundo con oasis, la selección sube desde cero la perilla del viaje hasta el primer escalón donde paga (alrededor de 0.19), no hasta el valor del diseño (1)."
- **Lo que no se sabe.** Si con más tiempo, o con mutaciones más pequeñas, llegaría al diseño.

---

### 4.3 Las perillas de la señal con costo (peldaño P7; `escalera/carros/O1_LUGAR_SENAL.py` y `mundo_tramo_c.py`)

La "pizarra" es un tablero público de la pista: guarda las últimas 16 anotaciones, cada una de hasta 8 números, y cada cuerpo lee en un paso lo que se escribió en el paso anterior. El módulo escribe allí **tres números**: la casilla donde mejor le fue, y el recuerdo de esa casilla en energía y en agua. El significado ("en la casilla tal me fue así de bien") lo fijó el ingeniero; no surgió solo.

| Perilla | Fábrica | Qué hace | Imagen | Si sube / si baja | Evidencia |
|---|---|---|---|---|---|
| `SENAL` | 1 | Interruptor del módulo. Con 0 es el organismo de P1 bit a bit. | — | — | Arnés 36 de 36. |
| `c_e` (perilla del mundo) | 0.01 | Costo de emitir: cada anotación aceptada le quita 0.01 de energía a quien la escribe, en el acto. | El precio de mandar un mensaje de texto. | 0: hablar es gratis. Más alto: hablar puede salir más caro que lo que ayuda. | Sólo se corrió con 0 (exploración) y con 0.01 (humo 3, serie y réplica). Medido en exploración: el gasto equivale a cerca del 4 % del metabolismo. **No se barrió.** |
| `SN_CADA` | 100 | Cada cuántos pasos puede emitir. | Un parte cada hora, no un chorro continuo. | Más seguido: más costo y más tráfico. | **Nunca barrida.** |
| `SN_UMBRAL` | 0.3 | Sólo emite si su mejor casilla, **vivida por él**, tiene un recuerdo total mayor que 0.3. | No recomendar un restaurante que a uno le pareció apenas regular. | Más bajo: emite más y paga más. Más alto: casi no emite. | El preregistro lo dice sin rodeos: "No se exploró". |
| `SN_W` | 1.0 | Peso de lo que oye al sembrar su propia memoria. | Cuánto se le cree a un chisme. | — | **Nunca barrida.** |
| Regla "lo vivido manda" (`nl == 0`) | fija | Lo oído sólo se anota en casillas donde el linaje **nunca ha mordido**. | Creerle a otro sólo sobre un barrio que uno no conoce. | — | Esta regla resultó ser el cuello que explicó por qué "los tres juntos no suman" (ver SN_PISA). |
| `SN_BARAJA` | 0 | Sólo para el control: con 1, lo oído se anota en la casilla del lado opuesto del anillo. | Un GPS que siempre manda a la otra punta de la ciudad. | — | Es el control que "pudo ganar" y no ganó (49 y 50 linajes contra 132 y 124). |

### 4.4 La perilla de PISA (`escalera/mixto/construye_pisa.py`)

| | |
|---|---|
| Nombre | `SN_PISA` |
| Fábrica | 0 en P7; 1 en la variante PISA |
| Qué hace | Una sola línea: al leer una anotación sobre una casilla donde el linaje ya estuvo, **si su propio recuerdo de esa casilla ya no vale** (total por debajo de 0.05), borra la marca de "ya vivido" y deja que lo oído se anote. Lo vivido que todavía vale sigue mandando. Memoria nueva: ninguna. |
| Imagen | "Yo conocía ese barrio y ya no había nada; si me dicen que abrieron algo, les creo." |
| Por qué existe | Una sonda de sólo lectura mostró que, después de cada mudanza del oasis, los lectores rechazaban el 99.8 % y el 98.8 % de las anotaciones que apuntaban al oasis nuevo, porque la marca de "ya vivido" no se borraba nunca. |
| Efecto secundario medido | "Rumor": entre el 15.8 % y el 18.2 % de las veces lo pisado apuntaba al oasis viejo. No se midió daño ni costo. |
| Evidencia | Es un interruptor, no un número: se comparó prendido contra apagado (serie y réplica, sección 7). No hay nada que barrer. |

### 4.5 Las perillas de "ir a lo menos visitado" (peldaño P10; `escalera/carros/O1_LUGAR_PREG.py`)

| Perilla | Fábrica | Qué hace | Imagen | Si sube / si baja | Evidencia |
|---|---|---|---|---|---|
| `PREGUNTA` | 1 | Interruptor del módulo. Con 0 es P1 bit a bit. | — | — | Arnés. |
| `PG_OLVIDO` | 0.01 | Olvido por presencia: cada paso en que el cuerpo tiene necesidad y no ve nada útil, la casilla donde está pierde el 1 % de su recuerdo. | "Estoy parado en la panadería con hambre y no hay pan: voy borrando de a poco la idea de que aquí hay pan." | Más alto: suelta rápido un sitio (puede soltar uno bueno por una mala racha). Más bajo: vuelve mucho tiempo a un sitio muerto. | **Nunca barrida.** |
| `visto` (memoria, no perilla) | 30 enteros | Guarda el último paso en que se visitó cada casilla. | Una libreta con la fecha de la última visita a cada vereda. | — | — |
| Regla de destino | edad / (distancia + D0) | Sin blanco y sin recuerdo, va a la casilla que hace más tiempo no visita, descontando la distancia. | Revisar primero el potrero que hace más tiempo no se mira, si no queda lejísimos. | — | El efecto declarado es del **conjunto** olvido + destino; no hubo brazo "sólo olvido". |
| `PG_BARAJA` | 0 | Sólo para el control: va al lado opuesto de la casilla elegida. | — | — | Es un control **pesimista** (manda lejos sin información), no uno de igual costo. Declarado. |
| `mueve` (perilla del mundo) | 20 000 | Cada cuántos pasos el oasis se muda a un sitio que no se solapa con el anterior. | La feria que cambia de plaza cada cierto tiempo. | Más corto: la memoria sirve menos. | Sólo 10 000 (humos) y 20 000 (exploración, serie, réplica). **No barrida.** No se probó un mundo donde el oasis pueda volver al mismo sitio. |

### 4.6 Las perillas de la celda retenida (peldaño P8; `escalera/p8/carros/O1_LUGAR_COMP2.py`)

| Perilla | Valores | Qué hace | Imagen | Evidencia |
|---|---|---|---|---|
| `COMPONE` | 0 = P1; 1 = COMP; 2 = COMP2 | Con 1, el recuerdo del sitio se suma también al valor de una letra "mixta" (una que da algo y quita algo). Con 2, se suma sólo si la letra alimenta alguna necesidad: es una **compuerta puesta a mano** para que el veneno y la sal no se vuelvan "buenos" dentro del oasis. | "En el restaurante bueno me animo a pedir un plato que en otra parte no pediría; pero no me tomo el cloro por estar en un buen restaurante." | Sin la compuerta, el veneno dentro del oasis se muerde 31 % y 27 % de las veces (descriptivo). Con ella, 0. |
| `LG2` | 0 o 1 | Con 1, una mordida en una casilla que ya recuerda algo extra **no** actualiza la tabla por letra. Así la tabla aprende lo que la letra vale fuera, y el extra del oasis queda sólo en la memoria de lugar. | No subirle la nota a la arepa en general porque en una plaza específica la sirven con queso: el queso es mérito de la plaza. | Comparado prendido contra apagado: con COMP2 la medida D sube de 0.25 y 0.19 a 0.75 y 0.75. Omitió cerca de 54 000 aprendizajes por corrida. |

Las dos son interruptores y las dos son **conocimiento puesto a mano**, declarado así. No hay valores intermedios que barrer.

---

### 4.7 Las perillas del mundo

| Perilla | Fábrica | Qué hace | Imagen | Evidencia |
|---|---|---|---|---|
| Largo del anillo (`L`) | 40 × número de linajes (360 con 9) | Tamaño del mundo. | Una pista de atletismo. | Con 9 cuerpos en un anillo de 40 la pista medía escasez, no interacción; se escaló (ENMIENDA 1, ERR-95). |
| Objetos (`nobj`) | 4 × número de linajes (36 con 9) | Cuántos objetos hay siempre en el mundo. | Platos sobre la mesa: cuando uno se va, llega otro. | Ídem. |
| `costo`, `costo_a` | 0.001 cada uno | Lo que bajan energía y agua en cada paso. | El gasto de estar vivo. | Fijo desde la fase 9. No barrido en la pista. |
| Efectos de las letras | A (+0.8 energía), B (−0.4 energía), C (+0.8 agua), D (−0.4 agua) | Lo que da o quita cada mordida. | — | Fijos. |
| Tope de niveles | 1.5 | Máximo de energía y de agua. | El tamaño del tanque. | Fijo. En las sondas de P9 se vio que este tope "se come" cualquier premio de energía adicional. |
| `rep_umbral`, `rep_X`, `dote` | 1.0, 500 pasos, 0.6 | Condición para parir y con cuánto nace el hijo (el padre lo paga). | Ahorrar durante un tiempo sostenido antes de independizar a un hijo, y darle un capital. | Fijos en la pista. En el mundo ECO, `rep_umbral` sí fue un gen (ECO_SEL: la selección lo movió y subió la capacidad de carga). |
| `OLVIDO` | 0.003 por paso y por cada 40 celdas | El mundo retira de vez en cuando un objeto al azar y repone otro. | El barrendero municipal, que pasa muy poco. | Se corrigió su escala (ERR-98). |
| `fundador_limpio` | 1 desde la ronda 2 | Cuando un linaje se extingue, el reemplazo nace sin nada de la memoria vieja. | Una familia nueva que llega a una casa vacía, sin heredar los cuadernos de la anterior. | **Candidato ERR-191:** esta regla regala limpieza. Ver sección 9. |
| `oasis`, `FRAC_ZONA`, `EXTRA`, `POBRE` | 1, 0.10, 0.8, 0.5 | Un tramo del 10 % del anillo donde la comida también da agua y el agua también da energía (+0.8); fuera, comida y agua valen la mitad. | Un nacimiento de agua en una finca seca. | `POBRE` 1.0 se probó antes ("grande"): nadie usaba el oasis. No hay barrido fino. |
| `dens` | 0.5 | La mitad de lo que el mundo repone nace dentro del oasis. | — | Con 0 (humo 1) el módulo no ganaba. Se eligió 0.5 "hasta que ganó en 2 semillas": sesgo declarado (ERR-171). |
| `vista_r` | 20 | El cuerpo sólo ve objetos a 20 celdas o menos. En la pista vieja ve todo. | Caminar con neblina. | Ídem: elegido en ráfaga, declarado (ERR-171). |
| Letra E (P8) | (+0.3 energía, −0.1 agua), 15 % de lo repuesto, nunca nace dentro del oasis | Una letra "mixta" para la prueba de celda retenida. | — | Fija. |

---

### 4.8 Las perillas del aparato de selección (`escalera/perillas/construye_perillas.py` y `corre_perillas.py`)

Este aparato no es parte del cuerpo: es el montaje con el que se deja que la selección actúe sobre genes. Un "gen" aquí es un número que cada cuerpo lleva, hereda su hijo y puede cambiar un poquito al nacer.

| Perilla | Valor | Qué hace | Imagen | Si sube / si baja | Evidencia |
|---|---|---|---|---|---|
| σ (`PS_SIGMA`) | 0.03 | Tamaño típico del cambio al azar en un gen al nacer. | Copiar una receta a mano: cada copia cambia apenas un poco una cantidad. | Más grande: pasos largos, puede saltar sobre lo bueno. Más chico: avanza muy lento. | Heredado de experimentos anteriores, fijado de antemano. **No barrido.** Probar un valor menor es el plan 4 de la próxima sesión. |
| δ (`PS_DELTA`) | 0.01 | Sesgo a la pérdida: cada mutación además resta 0.01. El gen tiende a apagarse solo. | Una cuesta abajo suave: lo que nadie empuja rueda hasta cero. | Con 0, el azar solo dejaba el gen por encima de 0.10 en entre el 47 % y el 82 % de los linajes y el control dejaba de ser control. Con 0.01, sólo en el 7 %. | Fijado **antes** de correr, con un nulo simulado (`nulo_perillas.py`). |
| Una mutación por nacimiento, en un solo gen | fija | Cada nacimiento cambia un gen; el otro se copia igual. | — | — | En `o1_evo` mutaban los cuatro genes a la vez. La sesión paralela probó "un gen por parto" sobre O1 y dio NO (57 contra 72). |
| Recorte | de 0 a 1.5 | Límites del gen. | — | — | — |
| Cámara continua (`PS_CAMARA`) | 1 | Cuando un linaje se extingue, el reemplazo copia (con una mutación) los genes del cuerpo vivo de **otro** linaje al azar. Sólo viajan los genes: nace sin memoria. Quien dura más es copiado más veces. Nadie juzga. | Un pueblo donde, cuando una casa queda vacía, la ocupa alguien criado en otra casa que sigue en pie. | Sin cámara, casi no hay oportunidades de selección dentro de una corrida. | Es lo que hizo andar el reloj (sección 10). |
| Pasajes | 5 | Cuántas corridas encadenadas hay: lo que queda vivo al final de una siembra la siguiente, en un mundo nuevo. | Resembrar con la semilla de la cosecha anterior. | Con 3, el reloj quedaba en 39 eventos; con 5 llega a cerca de 80. | Elegido tras una exploración (sesgo declarado). |
| T | 100 000 pasos por pasaje | Duración de cada corrida. | — | Con 25 000 casi ningún linaje alcanza a "establecerse". | Los experimentos contra el muro usaron 25 000 y no encontraron nada; "no más pasajes de 25 000" es una decisión vigente. |
| Siembra de establecidos | regla | Entre pasajes sólo pasan genes de linajes que no se refundaron en la segunda mitad (si no hay, los de menos refundaciones). No mira hijos ni cruce. | Guardar semilla sólo de las matas que llegaron al final de la temporada. | En `o1_evo` se sembraba con cualquier cuerpo vivo al final, incluidos recién fundados: eso diluía la selección. | Regla fijada de antemano. |
| `PS_LEE` | 1 (selección) o 0 (neutro) | Con 0, los genes se heredan, mutan y viajan igual, pero **ningún cuerpo los usa**. Es el control de deriva. | Una receta que pasa de mano en mano y nadie cocina: cambia sólo por errores de copia. | — | Es el control de "perillas": con él GV queda en 0.02 y 0.0. |
| Prueba monomórfica | regla | La evaluación final usa un solo genoma (la mediana de la cadena), sin mutación ni cámara. | Calificar la receta final, no seguir cambiándola durante el examen. | — | — |

**Otros montajes de selección, para comparar.** `o1_evo` y el termostato: 10 pasajes de 25 000, σ 0.03 sin sesgo, siembra de vivos. ECO_SEL (otro mundo, con población): probabilidad de mutar 0.05, σ 0.15, banco de 200. BLOQUES: reglas que se pueden mutar, duplicar, borrar, insertar y copiar del vecino.

---

### 4.9 Lo que esta sección deja claro

1. La única perilla con resultado **declarado** al moverla es GV (y GW como su contraste).
2. La única perilla de O1 con una forma **vista** es MARGEN, y es exploración de dos semillas bajo una regla de fundador en discusión.
3. Nunca se barrieron: D0, las urgencias, LG_NB, LG_ETA, SN_CADA, SN_UMBRAL, SN_W, PG_OLVIDO, c_e, σ.
4. Varias perillas del mundo con oasis se ajustaron hasta que el módulo ganó en dos semillas; está declarado (ERR-171) y por eso todo lo de la Escalera lleva la coletilla "en el mundo con oasis".
