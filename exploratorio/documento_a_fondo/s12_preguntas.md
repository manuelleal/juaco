## 12. Preguntas que le van a hacer en el evento, con respuesta honesta

**Idea principal.** Las preguntas difíciles se responden mejor concediendo primero lo que es cierto y diciendo después, con un número, lo que sí hay. Cada respuesta está pensada para decirse en menos de un minuto. Debajo de cada una hay una línea de "si insisten".

### 1. "¿Esto no es simplemente un algoritmo genético?"

**Respuesta.** En parte sí, y no lo escondo. La parte de selección usa lo mismo que un algoritmo genético: copias con pequeños errores y sobreviven las que duran. Hay dos diferencias. La primera: aquí no hay una función que califique a cada individuo y escoja a los mejores; lo único que cuenta es durar en un mundo compartido, y eso lo medimos contra un control donde los genes mutan igual pero nadie los usa. La segunda, y más importante: lo que presento no es el algoritmo, es el protocolo para saber cuándo creerle. La mayor parte de lo que funciona en el proyecto es diseño, no selección, y lo digo en cada resultado.

*Si insisten:* "De once resultados declarados, cuatro son de selección; en los cuatro la selección trabajó sobre piezas que alguien le dejó."

### 2. "¿Por qué no usan redes neuronales?"

**Respuesta.** Por la pregunta que nos hicimos, no porque creamos que son malas. Queríamos saber hasta dónde llega un organismo con reglas locales, donde cada parte se ajusta sólo con lo que ella misma ve, sin el método de entrenamiento global que usan las redes actuales. Es una restricción de investigación. Y cuando comparamos en serio, fuera del protocolo, una red de nuestras células contra una red convencional bien afinada, la convencional ganó: aprendió igual de rápido y se readaptó cuatro veces más rápido. Eso también está escrito.

*Si insisten:* "El organismo que mejor nos funciona, O1, ni siquiera es una red: es una libreta de promedios y unas reglas. Ciento sesenta y tres líneas."

### 3. "¿Qué tiene de nuevo?"

**Respuesta.** No reclamo novedad en los mecanismos: memoria de lugar, señales, exploración, selección, todo tiene décadas de literatura. Lo que creo que aporta es el método para que una persona que no programa dirija agentes de inteligencia artificial en investigación computacional sin creerles a ciegas: preregistro, identidad bit a bit, control que puede ganar, réplica y auditoría independiente, con cada error numerado. Y un caso de uso completo, con sus negativos incluidos.

*Si insisten:* "Todavía no lo hemos comparado con métodos estándar de la literatura; el informe interno lo llama lo más débil que tenemos."

### 4. "¿Escala?"

**Respuesta.** No lo sé, y lo que sé apunta a que no se puede dar por hecho. Todo ocurre en un anillo de 360 celdas con cuatro letras y nueve linajes. Tres datos en contra del optimismo: lo que la selección logró en un mundo empeoró al organismo al pasarlo a otro; un módulo que funcionaba solo no sumó nada al juntarlo con otros dos; y un intento de "planear" con una regla de un paso no arrancó. Lo que sí escala bien es el costo: una corrida de cien mil pasos tarda minutos en un computador de escritorio.

*Si insisten:* "El siguiente paso que tenemos escrito es precisamente una versión con poblaciones de cientos, y está en borrador."

### 5. "¿Quién lo revisó?"

**Respuesta.** Nadie externo todavía, y hay que decirlo así. Internamente, cada resultado lo revisa un agente auditor distinto del que lo construyó, de sólo lectura, que recalcula los números desde los archivos crudos con su propio programa. Yo reproduje uno de los resultados en mi máquina y dio los mismos archivos. El repositorio es público, con los preregistros fechados antes de los datos. Pero revisión por pares no hay; es el paso que sigue.

*Si insisten:* "El auditor también es una inteligencia artificial. Es independiente del autor, no de la tecnología."

### 6. "¿Qué es eso de AGI? ¿Están diciendo que van hacia una inteligencia general?"

**Respuesta.** La sigla significa inteligencia artificial general: una máquina capaz de aprender casi cualquier tarea intelectual. En el proyecto es la dirección que orienta qué vale la pena construir, no algo que afirmemos haber alcanzado ni estar cerca de alcanzar. Las reglas del propio proyecto prohíben declarar inteligencia general o conciencia por cualquier resultado. Lo que hay es un organismo que come, evita, recuerda un sitio y deja hijos en un mundo de cuatro letras.

*Si insisten:* "La distancia entre esto y una inteligencia general es enorme, y no tengo evidencia de que este camino llegue."

### 7. "¿Por qué creerle a agentes de inteligencia artificial?"

**Respuesta.** No hay que creerles; el método parte de que no. Le doy tres casos reales. Uno: un auditor encontró que un organismo podía declararle al juez los hijos que quisiera; se demostró con un tramposo que declaró 999 999 y se arregló antes de correr nada oficial. Dos: un control que debía leer "el lugar equivocado" acertaba el 45 % de las veces; se encontró y se corrigió antes de la serie. Tres: una explicación que ya estaba escrita en tres documentos se cayó al día siguiente cuando la réplica no la repitió, y hubo que retirarla. Los agentes se equivocan mucho; lo que importa es que quede un rastro que los atrape.

*Si insisten:* "Y el error más costoso del proyecto no fue de un agente, fue mío: perseguí durante diez fases el techo de mis propias pruebas."

### 8. "¿El organismo aprende?"

**Respuesta.** Depende de qué organismo. En la pista, O1 memoriza: muerde una letra una vez, anota qué le hizo, y como cada letra hace siempre lo mismo, con eso basta. No lo llamo aprender. Con la memoria de lugar hay algo más: corrige a medias lo que cree de un sitio cada vez que muerde allí. La frase que usamos es "recuerda dónde le fue bien y pasa más tiempo allí". Y el organismo anterior, el del tronco, sí aprende y desaprende asociaciones con una regla local; eso se midió en las primeras fases.

*Si insisten:* "El órgano que armó la selección es un instinto heredado, no aprendizaje. Está escrito así."

### 9. "¿Los organismos se comunican?"

**Respuesta.** No uso esa palabra a secas. Lo medido es esto: si un linaje anota en un tablero público la casilla donde le fue bien, y otros linajes idénticos a él leen esa anotación, más vidas llegan al sitio bueno, aunque anotar cueste. Pero el significado de la anotación lo puse yo en el diseño; no surgió. De hecho medimos antes que no surge solo por refuerzo, seis veces. Y los que leen son clones del que escribe, así que el beneficio queda en casa.

*Si insisten:* "Hay una reserva sobre ese resultado: la medida del mecanismo se cambió después de una prueba corta y antes de la serie. Con la medida original no pasa. Está numerado como ERR-175."

### 10. "¿Qué es lo más fuerte que tienen, en una frase?"

**Respuesta.** Dos cosas distintas. Como método: un registro de más de ciento cincuenta errores numerados donde se ve qué atrapó el protocolo y cuándo. Como resultado: en un mundo simulado, con un genoma hecho de reglas que se pueden armar y duplicar, la selección fijó sola una regla heredable que distingue lo dañino de lo nutritivo, en 19 de 20 corridas, dos veces, y la duplicó.

*Si insisten:* "Es un instinto en un solo mundo simulado. No es aprendizaje y no lo hemos visto en otro mundo."

### 11. "¿Y lo más débil?"

**Respuesta.** Cuatro cosas. Los controles son todos internos: no nos hemos medido contra métodos estándar. Los mundos de la Escalera se ajustaron hasta que el módulo ganó en dos semillas; lo declaramos y por eso todo dice "en el mundo con oasis". La medida central tuvo que corregirse tres veces. Y hay una duda abierta sobre si una regla de la pista regala parte de lo que medimos; es un error candidato que todavía no hemos abierto ni resuelto.

### 12. "¿Qué tiene que ver esto con educación?"

**Respuesta.** Dos cosas que me importan como educador. La primera es que el proyecto es, en el fondo, un problema de evaluación: cómo saber si alguien, o algo, de verdad hizo lo que dice que hizo. La rúbrica antes del examen, el control que puede ganar, la segunda aplicación con otros casos, el evaluador que no es quien enseñó: son ideas de evaluación educativa aplicadas a máquinas. La segunda es práctica: muestra que un investigador sin formación en programación puede dirigir investigación computacional si tiene un método que no dependa de leer el código.

*Si insisten:* "El uso en aula de algo de esto es otro proyecto, separado, y está en fase de idea."

### 13. "¿Se puede reproducir?"

**Respuesta.** Sí, en un computador de escritorio sin tarjeta gráfica. Todo corre con Python y una librería numérica, con semillas fijas, de modo que la misma corrida da el mismo archivo bit a bit. Cada resultado declarado cita su preregistro, sus semillas y la huella de sus archivos.

*Si insisten:* "Yo reproduje uno completo: 161 archivos idénticos campo a campo, salvo el tiempo de cómputo."

### 14. "¿Qué harían distinto si empezaran hoy?"

**Respuesta.** Tres cosas. Medir el reloj desde el primer experimento de selección: creíamos tener ciento cincuenta generaciones y teníamos unas doce. Sondear si hay espacio para ganar antes de construir un módulo. Y desconfiar antes de mis propias metas: el cambio que más rindió fue dejar de subirle la vara al organismo y empezar a darle a la selección piezas con qué construir, y mundos donde cada capacidad pague.

---

### Tres frases para tener listas

- **Para abrir:** "Esto es un organismo artificial mínimo y, sobre todo, un método para que una persona dirija agentes de inteligencia artificial en investigación sin creerles a ciegas."
- **Para cuando no sepa:** "Eso no lo hemos medido." Es una respuesta completa y en este proyecto es frecuente.
- **Para cerrar:** "Lo que funciona es pequeño y está contado con sus reservas; lo que no funcionó está en el mismo registro, con el mismo detalle."
