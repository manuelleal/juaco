## 2. El mundo

**Idea principal.** El mundo de JUACO es deliberadamente pequeño: un anillo de celdas con letras encima. Unas letras alimentan, otras dañan. Lo que hace difícil vivir en él no es encontrar comida sino que **lo malo se acumula**: nadie se lo quiere comer y el mundo casi no lo retira. Hay tres versiones del mundo que conviene no mezclar nunca al hablar: la **pista vieja** (donde está "el muro"), el **mundo con oasis** y el **mundo con oasis que se muda** (los dos últimos son los de la Escalera).

### 2.1 El anillo

Imagine una pista de atletismo dividida en casillas numeradas, donde la última casilla toca a la primera. Eso es el anillo. Un cuerpo ocupa una casilla y en cada paso puede moverse una a la izquierda, una a la derecha, o quedarse.

- Con un solo linaje el anillo tiene 40 celdas y 4 objetos.
- Con nueve linajes (el caso habitual) tiene **360 celdas y 36 objetos**: se escala para que cada cuerpo tenga los mismos recursos que tendría solo (`pista.py`, líneas 167 a 169).
- El máximo son nueve linajes (`N_MAX = 9`).

La pista (`experimentos/carrera_escuderias/pista.py`) no se inventó de cero: es el mundo de la fase 9 del proyecto partido en dos piezas, "mundo" y "cerebro", con una comprobación de que, con un solo organismo, reproduce al original exactamente, bit a bit.

### 2.2 Las letras

Cada objeto del mundo es una letra. Al morderla, cambia los niveles del cuerpo.

| Letra | Nombre | Efecto al morderla | Dónde existe |
|---|---|---|---|
| A | comida | +0.8 de energía | siempre |
| B | veneno | −0.4 de energía | siempre |
| C | agua | +0.8 de agua | siempre |
| D | sal | −0.4 de agua | siempre |
| E | "sal dulce" | +0.3 de energía y −0.1 de agua (una letra mixta: da y quita) | sólo en el peldaño P8 de la Escalera |
| K | "la llave" | nada (0 y 0) | sólo en el intento de P9 "planear", que se cerró sin resultado |

Los efectos de A, B, C y D están en el organismo original de la fase 9 (`organismo_f9c.py`, línea 150) y la pista los toma de allí.

Observe la simetría: hay dos necesidades (energía y agua), y para cada una hay una letra que la sube y otra que la baja. Y observe la asimetría que importa: una mordida mala quita 0.4, que es mucho para un recién nacido que arranca con 0.6.

### 2.3 Cómo aparece y desaparece la comida

El mundo mantiene **siempre el mismo número de objetos**. Cuando uno desaparece, aparece otro en una celda libre al azar, y su letra se sortea por igual entre A, B, C y D (`pista.py`, líneas 203 a 206).

Un objeto desaparece sólo por dos razones:

1. **Alguien lo muerde** (línea 293). Lo que uno come deja de estar para todos.
2. **El mundo lo olvida** (líneas 306 a 309): en cada paso hay una probabilidad pequeña (0.003 por cada 40 celdas de mundo) de que un objeto cualquiera se retire y se reponga.

De aquí sale el problema central. Lo bueno se lo comen pronto. Lo malo se queda. Con el tiempo el mundo se llena de veneno y sal. Medido: con un solo cuerpo, entre el 88 % y el 92 % de los objetos eran malos. La única forma rápida de que vuelva a aparecer algo bueno es que alguien muerda algo malo, y eso duele. Ese dilema, "cuándo comer y cuándo limpiar", es lo que el proyecto llama el muro (sección 9).

### 2.4 Qué ve un cuerpo

En cada paso la pista le entrega al cerebro del cuerpo una "observación" (`pista.py`, línea 240):

- su posición y sus dos niveles;
- **todos los objetos del anillo**, con su letra y su posición (en la pista vieja la vista es total);
- una foto de todos los cuerpos: dónde está cada uno, qué letra tiene debajo y qué mordió en el paso anterior;
- la **pizarra**: un tablero público con las últimas 16 anotaciones (cada una de hasta 8 números); lo que se escribe en un paso se lee en el siguiente.

Lo que **no** ve: qué hace cada letra (tiene que morderla para saberlo), ni el azar del mundo, ni, en los mundos con oasis, dónde está el oasis.

### 2.5 Qué es un paso

Un paso es un tic del reloj del mundo. En cada paso ocurre esto, en orden (`pista.py`, líneas 26 a 28):

1. En un orden de turno que se sortea de nuevo cada paso, cada cuerpo decide, se mueve, y si muerde recibe el efecto; el objeto mordido se repone de inmediato.
2. Todos pagan el costo de vivir: 0.001 de energía y 0.001 de agua.
3. El mundo olvida, o no, un objeto.
4. En el mismo orden: los que llegaron a cero mueren y nace su reemplazo; los que completaron la ventana de parto paren.
5. La pizarra publica lo escrito.

Una corrida típica dura **100 000 pasos** (se escribe "T 100 000" o "T 100k").

### 2.6 Qué es un linaje, y cuántos hay

Un **linaje** es una cadena de cuerpos que se suceden: un cuerpo, cuando muere su hijo, luego su nieto. En esta pista hay **un solo cuerpo vivo por linaje**: los hijos esperan en una fila y nacen cuando el padre muere (la fila admite hasta 200). El cerebro (el "carro") es uno por linaje y pasa de cuerpo en cuerpo.

Normalmente corren **nueve linajes a la vez**, todos con el mismo carro: eso se llama "monocultivo". Cuando se mezclan carros distintos se llama "pista mixta".

Una serie típica son 20 corridas con 20 semillas distintas. Nueve linajes por veinte corridas dan **180 "linajes-semilla"**: por eso casi todos los resultados se expresan "de 180".

### 2.7 Fundador, y fundador limpio

Si un cuerpo muere y su fila de hijos está vacía, el linaje **se extinguió**. Para que el experimento no se quede con un puesto vacío, el mundo pone un cuerpo nuevo de regalo en ese puesto: un **fundador**. Cada fundador se cuenta, porque es una extinción. Un linaje que necesita muchos fundadores no se sostiene solo; uno que no necesita ninguno después del paso 10 000 se llama **establecido**.

Hay dos reglas posibles para el fundador:

- **Fundador no limpio (regla original).** El fundador usa el mismo carro, con su libreta intacta: "sabe" todo lo que el linaje extinto había anotado. El 22 de septiembre la auditoría lo señaló como un posible artefacto (ERR-101: "la memoria sobrevive a la extinción"); se corrió un control borrando esa memoria y el cruce se mantuvo (R0 real 0.941, 148 de 180).
- **Fundador limpio (desde la ronda 2; ENMIENDA 5).** Cada fundador es una instancia nueva del carro, con la libreta vacía (`pista.py`, líneas 347 y 348). Es la regla de todas las series desde entonces, incluida toda la Escalera.

**Por qué importa: el candidato ERR-191.** Un fundador limpio no sabe qué es veneno, así que lo prueba una vez. Y la sal también. Cada una de esas pruebas retira un objeto malo del mundo. Un linaje que se hunde y se refunda cientos de veces hace, sin proponérselo, cientos de limpiezas. En el mapa del muro del 1 de octubre se vio la cuenta exacta: los linajes hundidos tienen "mordidas malas ≈ fundadores + 2" (un linaje con 484 fundadores, 489 mordidas malas). Consecuencia: **con fundador limpio, la pista regala limpieza por nacimiento.** Un organismo sin regla de limpieza cruza 5 y 6 de 9 con esta regla y 0 de 180 con la otra.

Esto está registrado como **candidato** a error número 191, **no abierto**. Lo que obliga a hacer: revisar qué series viejas usaron cada regla antes de leer cualquier cosa sobre la limpieza. La frase declarada en septiembre ("la limpieza compartida es necesaria") se midió con fundador no limpio y conserva esa condición.

### 2.8 El mundo con oasis

Es la pista vieja con cuatro cambios (`escalera/mundo_escalera.py`). Con todos apagados, es la pista vieja bit a bit; un arnés lo comprueba.

| Cambio | Valor | Qué significa |
|---|---|---|
| Oasis | un tramo seguido del 10 % del anillo (36 celdas), en un sitio sorteado por semilla | Dentro, la comida da además +0.8 de agua y el agua da además +0.8 de energía. El veneno y la sal no cambian. |
| Pobreza fuera | 0.5 | Fuera del oasis, comida y agua dan la mitad (0.4 en vez de 0.8). |
| Densidad | 0.5 | La mitad de lo que el mundo repone nace dentro del oasis: allí hay unas cinco veces más objetos por celda. |
| Vista parcial | 20 celdas | El cuerpo sólo ve los objetos que tiene a 20 celdas o menos. |

**Nadie le dice al cuerpo dónde está el oasis.** Lo único que puede hacer es asociar lo que sintió con el sitio donde lo sintió.

**En qué se diferencia de la pista vieja, en una frase:** en la pista vieja el cuerpo ve todo y todos los sitios valen lo mismo, de modo que no hay nada que recordar; en el mundo con oasis ve poco y hay un sitio que vale cuatro veces más por mordida, de modo que recordar dónde está paga la vida del linaje. O1 sin memoria de lugar casi no vive allí: cruzan 7 de 180.

Tres advertencias que viajan con este mundo:

- Se construyó **para** que la memoria de lugar pagara. La densidad y la vista se ajustaron en pruebas rápidas hasta que el módulo ganó en dos semillas. Está declarado (ERR-171) y por eso todo resultado de la Escalera lleva "en el mundo con oasis".
- **No es el muro.** Que algo funcione aquí no dice nada sobre la pista vieja. Está prohibido compararlos.
- Hay una medida que se reporta siempre, llamada "mundo A+C": el número medio de objetos buenos (comida más agua) presentes. Si un organismo gana dejando el mundo más "pelado", parte de su ventaja puede venir de comerse lo de los demás y no de decidir mejor.

### 2.9 El oasis que se muda

Es el mundo anterior más una perilla (`escalera/mundo_tramo_c.py`): cada **20 000 pasos** el oasis se muda a un tramo nuevo, que nunca se solapa con el anterior. En una corrida de 100 000 pasos se muda cuatro veces. La comida densa sigue al oasis nuevo; lo que quedó en el viejo se queda ahí hasta que se lo coman.

**En qué se diferencia:** aquí recordar no basta, porque el recuerdo caduca. Quien sólo recuerda vuelve una y otra vez a un sitio que ya no da. Este es el mundo de "ir a lo menos visitado" (P10), de "los tres juntos" y de PISA.

Una limitación declarada: como el oasis nunca vuelve al mismo sitio, la regla "ir a donde hace más tiempo no voy" coincide con la regla del mundo. No se probó un mundo donde el oasis pueda regresar.

El mismo archivo tiene otras tres perillas, cada una para un peldaño: el costo de escribir en la pizarra (0.01 de energía, para P7), una letra nueva (E o K, para P8 y P9) y un "cerrojo" (el oasis sólo paga a quien mordió antes la llave K; para P9).

### 2.10 El otro mundo: ECO

Varios resultados de septiembre (el arranque en frío, ECO_SEL, BLOQUES) **no** ocurren en la pista sino en otro mundo llamado ECO (`experimentos/juaco_eco/`). La diferencia esencial: en ECO hay **población de verdad**. Los hijos nacen al lado del padre mientras él sigue vivo, puede haber decenas de cuerpos a la vez, y la comida entra a un ritmo fijo (un "quimiostato", como un cultivo de laboratorio al que se le gotea alimento). En ECO a veces hay un "vivero": un criadero que repone cuerpos durante un tiempo inicial. La medida allí no es cruzar sino **K, la capacidad de carga**: cuántos cuerpos vivos sostiene el linaje con el mismo flujo de comida.

Lo importante para no enredarse en el evento: un resultado de ECO no es un resultado de la pista, y lo que la selección logró en ECO **empeoró** al organismo cuando se trasplantó a la pista (está medido, dos veces).
