## 5. Cómo se mide

**Idea principal.** Casi todo en JUACO se reduce a contar una cosa: **cuántos linajes, de 180, se sostienen solos**. Esa cuenta sale de la física de la pista (nacimientos, muertes, extinciones), nunca de lo que el organismo dice de sí mismo. La medida central, el R0, tuvo que corregirse tres veces porque se podía inflar; esas correcciones son parte de lo que hay que saber contar.

### 5.1 R0 real

**La fórmula en palabras.** R0 real de un linaje = (hijos que de verdad llegaron a nacer) dividido entre (muertes del linaje más uno). La calcula el juez (`experimentos/carrera_escuderias/juez.py`, línea 180).

**Qué significa.** Como en esta pista sólo hay un cuerpo vivo por linaje, un hijo nace únicamente cuando su padre muere. Entonces cada muerte es reemplazada por un hijo propio (bien) o por un fundador regalado (una extinción). El R0 real mide qué fracción de los reemplazos fueron hijos propios. Por construcción **no puede pasar de 1**. Un valor de 0.94 no quiere decir "crece 0.94"; quiere decir "casi ninguna extinción". Otra forma de la misma cuenta que usa el proyecto: R0 real = (D − F) / (D + 1), donde D son las muertes y F los fundadores: toda la diferencia entre un organismo bueno y uno malo está en F.

**Las tres correcciones.**

| Error | Qué pasaba | Qué se cambió |
|---|---|---|
| ERR-99 | Con un cuerpo que casi no muere, la fórmula vieja daba números absurdos (R0 de 23 a 51). | Un linaje sólo es "evaluable" con cinco muertes o más. Con menos se llama "casi inmortal" y no cuenta ni a favor ni en contra. |
| ERR-100 | La fórmula vieja contaba los hijos que quedaban esperando en la fila sin nacer. El primer cruce parecía de 1.565. | Se cuentan sólo nacimientos reales. El mismo cruce quedó en **0.941**: sobre el umbral por 4.5 puntos, no por 74. |
| ERR-102 | Con la fórmula corregida, la medida sólo sube si el cuerpo muere: un organismo podía programar su muerte para verse mejor. | Se añadió un criterio paralelo, "persistencia" (ningún fundador después del paso 10 000 y al menos cinco nacimientos reales), y la muerte programada se declara y se mide. |

### 5.2 "Cruzar"

Un linaje **cruza** en una corrida si cumple las tres cosas (`juez.py`, línea 183):

1. tuvo cinco muertes o más (es evaluable);
2. su R0 real es 0.90 o más;
3. no necesitó ningún fundador después del paso 10 000.

Cuando un resultado dice "cruzan 79 de 180", es esto, contado en las 20 corridas de la serie.

### 5.3 Establecidos

Un linaje está **establecido** si no tuvo fundadores después del paso 10 000. Es más laxo que cruzar: no pide R0 ni cinco muertes. Sirve para ver "se asentó" aunque no haya alcanzado a renovarse lo suficiente. Un linaje puede estar establecido sin cruzar, por ejemplo uno que vive mucho y muere poco.

### 5.4 Mayoría

En una corrida hay nueve linajes. Se dice que hay **mayoría** en una semilla cuando cruzan cinco o más de los nueve. Un organismo "gana" una serie cuando tiene mayoría en 15 de 20 semillas o más. Es una vara más exigente que la suma: 100 linajes de 180 pueden estar repartidos de modo que haya mayoría en pocas semillas.

### 5.5 Pareado, y por qué "gana 19, empata 1, pierde 0"

**Semilla.** El azar de un computador no es azar: es una lista de números que depende de un número inicial, la "semilla". Con la misma semilla, la corrida sale idéntica, bit a bit. Cambiar la semilla es cambiar la suerte: dónde cae cada objeto, quién mueve primero.

**Pareado.** Para comparar dos organismos se les da **la misma semilla**: el mismo mundo, la misma suerte. Así la diferencia entre ellos no se puede achacar a que a uno le tocó un mundo más fácil. Es como poner a dos estudiantes el mismo examen en vez de dos exámenes distintos. Luego se cuenta en cuántas de las 20 semillas uno superó al otro. Regla del proyecto: **los empates cuentan en contra** del candidato.

La mayoría de las puertas piden dos cosas a la vez: ganar el pareado en 13 de 20 o más, y superar en la suma por 10 linajes o más.

**Serie y réplica.** Una serie son 20 semillas nuevas. La réplica son otras 20 que nunca se usaron, con la misma regla. "Semillas selladas" son rangos reservados que nadie toca hasta la corrida que decide.

### 5.6 Latencia

Se usa en los mundos donde el oasis se muda. Es el **número de pasos desde una mudanza hasta el primer bocado de comida o agua dentro del oasis nuevo**. Menos es mejor. Si un linaje nunca llega, se le anota el máximo (la duración de la corrida), para que no desaparezca de la cuenta. En PISA se reporta la mediana de los ocho linajes lectores.

Una trampa que el proyecto encontró (ERR-175): en P7 la latencia se medía por vida, y sólo existía en las vidas que **llegaron** al oasis. Si un módulo hace llegar a vidas que antes morían en el camino, mete latencias largas que antes no existían y parece que empeora. Por eso allí se cambió la medida a "fracción de vidas que llegan".

### 5.7 La D de P8

En la prueba de celda retenida no se mide supervivencia. Se toma la memoria de un linaje ya criado y se le presentan situaciones sintéticas. **D = probabilidad de morder la letra E dentro del oasis menos probabilidad de morderla fuera.** D va de −1 a 1. D = 0 significa que el sitio no cambia la decisión. La D de una semilla es la mediana sobre sus linajes válidos. Como la rejilla de situaciones es pequeña, D sale en escalones de 0.125.

Lo que D **sí** dice: que la E le gana a una comida visible cuando está dentro del oasis y no cuando está fuera. Lo que **no** dice: que fuera no la muerda (sola, la muerde 57 % de las veces).

### 5.8 El "mundo A+C"

Es el número medio de objetos buenos (comida, A, más agua, C) presentes en el mundo a lo largo de la corrida. Es la medida contra una trampa conocida, "el mundo que se come la comida": un organismo puede cruzar más simplemente porque se come lo de los otros.

- En el mundo con oasis, O1 deja alrededor de 7.0.
- El organismo que la selección produjo en "perillas" deja 4.32 y 4.44: más pelado.
- No entra en la regla de decisión, pero **es obligatorio decirlo junto al resultado**.

### 5.9 En ECO: K

En el mundo ECO la medida es **K, la capacidad de carga**: el promedio de cuerpos vivos durante la segunda mitad de la corrida (cero si el linaje se extinguió). Con una advertencia propia (ERR-153): si hay criadero permanente, K puede subir aunque el organismo sea peor, porque el criadero subsidia al que muere rápido. Por eso BLOQUES usó criadero sólo al principio.

### 5.10 Los dos relojes

En los experimentos de selección se mide además cuánta oportunidad tuvo la selección (sección 10): la **profundidad mutacional** (cuántas mutaciones hay en la ascendencia de un genoma) y las **refundaciones por cámara** (cuántas veces un linaje extinto fue reemplazado copiando a otro).

### 5.11 Cuatro veredictos y nada más

Cada regla de decisión termina en una de estas palabras:

- **FUNCIONA**: pasó todas las puertas.
- **HAY ALGO MODESTO**: pasó algunas; se registra, y si no se repite no se declara.
- **NO**: no pasó.
- **NO SE LEE**: falló una condición de validez (por ejemplo, el control de referencia no dio lo esperado); el experimento no dice nada en ningún sentido.

Y una etiqueta adicional, **EN EL UMBRAL**: cuando un conteo queda a una semilla del corte, la réplica es obligatoria.
