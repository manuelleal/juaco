## 3. El cuerpo, pieza por pieza (O1)

**Idea principal.** O1 es un programa de 163 líneas (`experimentos/carrera_escuderias/carros/O1.py`). No tiene red neuronal ni nada que se "entrene" con matemática pesada. Tiene una libreta donde anota qué le hizo cada letra, y un puñado de reglas fijas para decidir a dónde ir y si morder. Lo escribió un agente de inteligencia artificial (un modelo Opus, la "escudería O1") durante la carrera de escuderías del 22 de septiembre; no lo produjo la selección. Es el único organismo del proyecto que cruza el umbral en la pista vieja, y por eso es la base de todo lo que vino después.

En el vocabulario del proyecto, el programa que decide se llama "carro" (viene de la metáfora de la carrera) y hace de cerebro; el "cuerpo" es lo que la pista lleva por él: la posición y los dos niveles. Un carro sirve a todo un linaje: cuando un cuerpo muere y nace su hijo, el carro es el mismo objeto y conserva la libreta.

### 3.1 Las necesidades: energía y agua

El cuerpo tiene dos niveles, que el código llama `E` (energía; cuando baja es "hambre") y `Ag` (agua; cuando baja es "sed"). Los lleva la pista, no el carro (`pista.py`, líneas 104, 276, 303 y 318).

| Dato | Valor | Dónde |
|---|---|---|
| Nivel con que arranca el primer cuerpo | 1.0 en cada uno | `pista.py` línea 104 |
| Nivel con que nace un hijo o un fundador de reemplazo | 0.6 en cada uno (la "dote") | `pista.py` línea 345 |
| Lo que baja cada nivel en cada paso | 0.001 | `pista.py` línea 303; valor en `REGLAMENTO.md` §3 |
| Tope | 1.5 | `pista.py` línea 276 |
| Muerte | cuando cualquiera de los dos llega a 0 | `pista.py` línea 318 |

Una cuenta útil: con 0.6 y un gasto de 0.001 por paso, un recién nacido que no come nada dura 600 pasos. Si además muerde un veneno (−0.4), le quedan 200. Por eso en los registros aparece tantas veces "vida mediana 200": es la firma de un cuerpo que nació, mordió algo malo y se acabó.

El juez clasifica cada muerte en cuatro causas: hambre, sed, veneno (murió por energía habiendo mordido B en sus últimos 400 pasos) o sal (lo mismo con agua y D).

### 3.2 La tabla por letra: qué anota y con qué regla

Es la memoria de O1 (línea 36: `self.suma` y `self.n`). Por cada letra guarda dos cosas: la suma de lo que le pasó cada vez que la mordió, y cuántas veces la mordió. El "valor" de una letra es el promedio (líneas 41 a 43).

**La fórmula en palabras:** valor de la letra = (todo lo que esa letra me ha dado o quitado, sumado) dividido entre (las veces que la he mordido). El valor tiene dos componentes: cuánto cambió la energía y cuánto cambió el agua. Así, tras morder una A el linaje anota "A: +0.8 de energía, 0 de agua".

La anotación ocurre en `resultado()` (líneas 131 a 135): después de cada mordida, la pista le devuelve al carro lo que su cuerpo realmente recibió, y el carro lo suma.

Dos precisiones honestas:

- **No es aprendizaje bajo incertidumbre.** En la pista vieja cada letra hace siempre exactamente lo mismo, de modo que una sola mordida basta. La auditoría del carro lo dejó escrito: el vocabulario correcto es "memoriza tras una mordida", no "aprende".
- **O1 no usa la tabla verdadera.** No sabe de antemano que B es veneno: una letra sin probar es "desconocida" (el valor es `None`, línea 42). Leer la tabla verdadera está prohibido por el reglamento y un revisor automático lo comprueba.

### 3.3 Cómo decide morder: la consigna y el margen

La decisión está en `_gana` (líneas 52 a 63) y `_quiere` (líneas 65 a 70).

`_gana` responde "¿cuánto me sirve morder esto ahora?":

- Si la letra tiene algún componente negativo, o ninguno positivo, la ganancia es cero (línea 55): lo malo y lo neutro no "sirven".
- Para cada necesidad que la letra sube, mira el nivel actual. **Si ese nivel ya está en 1.25 o más, no cuenta** (línea 60: `if x >= self.U + MARGEN: continue`). Esta es la "consigna": comer sólo mientras la necesidad correspondiente esté por debajo del umbral de parto más el margen.
- Si cuenta, la pondera por urgencia (línea 61): por 4 si el nivel está bajo 0.3, por 2 si está bajo 1.0, por 1 si está entre 1.0 y 1.25.
- Y no cuenta más de lo que cabe hasta el tope (línea 62).

`_quiere` responde sí o no: muerde si la ganancia es mayor que cero (línea 69).

La frase del autor del carro en el encabezado resume por qué importa: "la boca no la manda el hambre". En los organismos anteriores, el hambre empujaba a morder lo que hubiera delante, y con sed mordían el veneno entre el 67 % y el 90 % de las veces. En O1 una letra buena se muerde sólo si sirve a la necesidad que ella sube.

### 3.4 La prueba de letras desconocidas

Línea 67: si la letra no está en la tabla, la muerde sólo si el menor de sus dos niveles está por encima de `PRUEBA` (0.5). Al elegir a dónde ir, lo desconocido es segunda prioridad: va a lo desconocido más cercano sólo si no hay nada bueno conocido (líneas 91 a 93 y 109).

Como la tabla se hereda, un linaje prueba cada letra una vez en su historia. Pero un **fundador limpio** nace con la tabla vacía y tiene que probar todo de nuevo, incluidos el veneno y la sal. Ese detalle, que parece menor, es el centro del candidato ERR-191 (sección 9).

### 3.5 La limpieza

Líneas 72 a 81 (`_costeable`) y 99 a 107.

**Por qué existe.** En la pista hay siempre el mismo número de objetos. Lo bueno se lo comen; lo malo nadie lo quiere, así que se acumula: el mundo tiende a quedar tapado de veneno y sal (con un solo cuerpo, entre el 88 % y el 92 % de los objetos eran malos). Un objeto sólo desaparece si alguien lo muerde o si el mundo lo "olvida", cosa que pasa muy poco. Cuando desaparece, aparece otro al azar, que puede ser bueno. Morder algo malo, entonces, es la única forma rápida de hacerle sitio a algo bueno.

**La regla.** La limpieza se activa sólo cuando no hay ningún objeto útil a la vista **y** alguna necesidad está por debajo de 1.25 (línea 100). Entonces el cuerpo va al objeto malo "costeable" más cercano y lo muerde. Es costeable (líneas 75 a 81) si se cumplen tres cosas:

1. La letra de verdad daña algo (línea 75).
2. El golpe cae en la necesidad **más llena** (línea 80): si el veneno quita energía, sólo lo muerde cuando tiene más energía que agua.
3. Después del golpe no queda por debajo del piso (líneas 78 y 79): el piso es `PISO` (0.2) normalmente, pero si los dos niveles ya están sobre el umbral de parto, el piso sube hasta ese umbral, para no romper la cuenta de 500 pasos.

**La cautela.** La frase declarada el 22 de septiembre fue "la limpieza compartida es necesaria": el mismo O1 con la limpieza apagada dio 0 de 180 linajes. Esa serie corrió con la regla vieja de fundador. Con fundador limpio, la sonda del 1 de octubre vio que O1 sin limpieza cruza 5 y 6 de 9, porque los fundadores que nacen y prueban el veneno limpian sin querer. Hasta resolver eso, de la limpieza sólo se repite la frase vieja con su condición.

### 3.6 Las patas: cómo elige a dónde ir

Todo ocurre en `actua` (líneas 84 a 121), que se llama una vez por paso. El cuerpo se mueve una celda a la izquierda, una a la derecha o se queda. Elige un "blanco" con este orden de prioridad (líneas 108 a 112):

1. **Lo mejor bueno.** Para cada objeto conocido y útil calcula un puntaje: ganancia / (distancia + 3) (línea 96). Si otro cuerpo está estrictamente más cerca de ese objeto, el puntaje se multiplica por 0.35 (línea 97). Va al de mayor puntaje.
2. **Lo desconocido más cercano**, si tiene niveles para probar.
3. **Lo sucio costeable más cercano**, si la limpieza está activa.
4. **El hueco.** Si no hay nada de lo anterior, va al centro del espacio vacío más grande entre los otros cuerpos (líneas 123 a 129).

Después da un paso hacia el blanco (línea 114) y, si en la celda a la que llega hay un objeto, decide si lo muerde con `_quiere` (líneas 117 y 118).

Dos cosas que O1 **no** hace: no escribe en la pizarra y no la lee (línea 121: `escribe=None`). Lo declara en su encabezado. Por eso el control de "canal mudo" era inerte para él.

En la pista vieja el cuerpo ve **todos** los objetos del anillo y la posición de todos los cuerpos. En el mundo con oasis ve sólo a 20 celdas.

### 3.7 El parto y la herencia

**El parto lo decide la pista, no el carro** (`pista.py`, líneas 355 a 370). Cuando energía y agua pasan 500 pasos seguidos en 1.0 o más, el cuerpo "pare": paga 0.6 de energía y 0.6 de agua, y el hijo entra a una fila de espera con ese capital. En esta pista hay **un solo cuerpo vivo por linaje**: el hijo nace cuando el padre muere. Si el padre muere y la fila está vacía, el linaje se extinguió y el mundo pone un "fundador" de reemplazo.

O1 nunca se niega a parir (líneas 154 y 155: `quiere_parir` devuelve siempre verdadero). Otros carros de la ronda 2 sí programaban su muerte o su parto; O1 no.

**La herencia** (líneas 143 a 152): al parir, el carro entrega una copia de la tabla por letra; al nacer, el hijo la recibe. Como el carro es el mismo objeto para todo el linaje, en la práctica la tabla es del linaje. Con fundador limpio, la pista crea un carro nuevo y vacío en cada extinción (`pista.py`, líneas 347 y 348).

Lo que O1 **no** hereda: ningún número de conducta. MARGEN, PRUEBA, PISO y los demás son constantes del archivo, iguales para todos los cuerpos. Para que la selección pudiera actuar sobre ellos hubo que construir versiones de O1 donde esas constantes son genes por cuerpo (`O1_PAS`, `O1_MURO_GEN`, `O1_LUGAR_GEN`).

### 3.8 Los módulos que la Escalera le agregó

Cada módulo se construye "por anclas": un programa toma el texto de O1 y le inserta líneas en sitios exactos; nadie edita O1 a mano. Cada uno tiene un interruptor que, apagado, deja el organismo anterior idéntico bit a bit.

- **Memoria de lugar** (`O1_LUGAR.py`). Una segunda libreta, por sitios en vez de por letras: 30 casillas del anillo por 2 necesidades. Regla (línea 211): recuerdo del sitio ← recuerdo + 0.5 × ((lo que recibí − lo que esa letra da en promedio) − recuerdo). En palabras: "en este sitio me dieron tanto de más de lo normal; corrijo a medias lo que creía". Se usa de dos maneras: sube el valor de un bocado que está en un sitio bien recordado (líneas 199 a 205), y, cuando no ve nada, viaja al sitio recordado en vez de al hueco (líneas 216 a 226). Se hereda con la tabla (línea 162).
- **Señal** (`O1_LUGAR_SENAL.py`). Cada 100 pasos, si su mejor casilla vivida recuerda más de 0.3, escribe en la pizarra casilla y recuerdo; al leer, anota lo ajeno sólo en casillas que nunca vivió.
- **Ir a lo menos visitado** (`O1_LUGAR_PREG.py`). Olvida un 1 % por paso el sitio donde está con necesidad y sin ver nada; y sin blanco ni recuerdo, va a la casilla que hace más tiempo no visita.
- **PISA** y **COMP2**: una y dos líneas más, respectivamente (fichas en la sección 4).

### 3.9 El otro cuerpo: el tronco v14.3

Para no confundir: el "tronco" es el organismo de referencia del proyecto, congelado, contra el que se compara todo. Es otra arquitectura, más parecida a un cerebro de insecto: una "retina" de 6 píxeles donde cada letra es un patrón, una capa de celdas que reparte esos patrones, valores aprendidos con una regla local de error de predicción, y una boca que decide con probabilidad según el hambre. Viene de las fases 1 a 9 (allí se cerraron cosas como aprender y desaprender una asociación, o el problema XOR con un supuesto previo declarado). En la pista de la carrera el paquete v14.3 da "hay algo modesto" dos veces: R0 real 0.63, no cruza.

O1 no es una mejora del tronco: es un organismo aparte, mucho más simple, escrito para la pista. El preregistro del mapa del muro lo dice así: "O1 no se puede apagar hacia el tronco: son arquitecturas distintas". Qué tiene O1 que el tronco no, y qué parte de esa diferencia ya se cerró con el termostato, está en la sección 9.
