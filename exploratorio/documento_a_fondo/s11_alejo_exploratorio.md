## 11. Alejo y lo exploratorio

**Idea principal.** Todo lo de esta sección es **exploración sin protocolo**: sin preregistro guardado antes, con 8 o 10 semillas, sin réplica, en problemas de juguete. La carpeta que lo contiene lo dice en su primera línea: "nada de esta carpeta es un resultado declarado de JUACO ni cuenta para niveles" (`exploratorio/LEEME.md`). Sirve para decidir a dónde mirar, no para afirmar. En el póster, si se menciona, va en un recuadro aparte y con esa etiqueta.

### 11.1 Qué es Alejo

Alejo es el **segundo experimento del director**, separado de JUACO; lleva el nombre de su hijo. El documento de arranque (`exploratorio/investigacion_20261001/alejo/ALEJO.md`) lo define así: averiguar si una **célula pequeña con una regla local de aprendizaje** sirve como pieza útil dentro o al lado de modelos entrenados con el método habitual, y si varias pueden formar un decisor propio, barato y especializado.

La diferencia con JUACO, en una tabla:

| | JUACO | Alejo |
|---|---|---|
| Pregunta | ¿Puede haber vida mínima con reglas locales? | ¿Sirve la célula como pieza práctica? |
| Retropropagación (el método con que se entrenan las redes neuronales actuales) | Prohibida dentro del organismo | Permitida **fuera** de la célula: como rival de comparación y como herramienta para el resto del sistema |
| Mundo | Comida, hambre, muerte, parto | Información: hechos que cambian, reglas que cambian |
| Éxito | Un peldaño con su control | Ganarle a una solución hecha a mano, o acercarse al rival estándar a menor costo, **o perder limpio** |

Y una regla de higiene escrita: Alejo no cuenta como avance de JUACO ni hereda sus niveles.

### 11.2 Las dos perspectivas

**Perspectiva A: la célula al lado de un modelo grande.** Los modelos de lenguaje tienen sus conocimientos "congelados" cuando se entregan: no aprenden de lo que pasa mientras se usan, salvo lo que cabe en la conversación del momento. La idea es pegarles un bloque de células que sí aprendan en uso: una memoria viva para lo que cambió esta semana. Para que valga la pena tendría que ser mejor o más barato que lo que ya existe: un simple diccionario, una búsqueda de "lo más parecido", o seguir entrenando una parte del modelo.

**Perspectiva B: un modelo propio hecho sólo de células.** No un modelo de lenguaje, sino un decisor pequeño que se adapta cuando la regla del mundo cambia, y que corre en un computador modesto o un celular. El documento menciona como horizonte las escuelas rurales y el agro.

El documento es franco sobre lo que falta: "lo que hoy no existe es evidencia de que una célula local le sirva a un modelo grande; existe la forma de averiguarlo barato". Y sobre la debilidad principal: nunca se conectó la célula a un modelo real, y todos los controles hasta ahora son internos.

### 11.3 Qué salió en cada prototipo

Los cuatro son programas pequeños en `exploratorio/investigacion_20261001/red_celulas/`.

**Prototipo 1: la red de células como modelo propio (perspectiva B).** Tarea: aprender a sumar en un reloj de siete horas (por ejemplo, 5 + 4 = 2).

- *Primer informe, "hay algo modesto":* una red de células con reglas sólo locales llegó a 0.9 de acierto en los pares vistos en 550 exposiciones, contra 2 550 de una red convencional del mismo tamaño. Pero **no generalizó** a los 19 pares que no había visto (entre 0.00 y 0.05, por debajo del azar, que es 0.14). Que las células nacieran y murieran no sumó nada medible. Y con 320 células apareció el "tramposo": células que cobran sin aportar.
- *Segundo informe, "no en lo central":* el rival del primer informe estaba mal afinado. **Con un rival justo, la red de células ya no gana en aprender** (550 contra entre 412 y 525) y **pierde por cuatro veces en readaptarse** cuando la regla cambia (887 contra 225). Lo que sí quedó, como hallazgo lateral: pagar el premio a grupos pequeños de células, en vez de a todas, elimina al tramposo.

Lectura: como modelo propio, con rival justo, no gana.

**Prototipo 2: un bloque de células junto a un modelo congelado, versión sintética (perspectiva A).** Tarea: hechos que cambian a mitad de camino.

- El bloque corrige los hechos cambiados casi tan bien como un diccionario que conoce de antemano la identidad de cada hecho (0.96 contra 0.98).
- Le gana a una memoria de "lo más parecido" en los seis escenarios probados (10 de 10 semillas).
- Suelta la corrección cuando el hecho vuelve a su valor original.
- **Sólo le gana al diccionario en una situación concreta:** memoria más pequeña que la cantidad de cambios, cambios continuos y consultas desiguales (0.78 contra 0.72).

**Prototipo 3: "la hamburguesa".** El nombre es la imagen: el pan es un modelo de lenguaje diminuto, entrenado de la forma convencional y luego congelado; la carne son células de memoria viva que leen el **estado interno** del modelo y, cuando reconocen una situación, corrigen su respuesta.

- Una asociación vista **una sola vez** y preguntada mucho después, cuando ya no está en la conversación: **1.00 de acierto contra 0.32** del modelo congelado. Darle más contexto al modelo no ayuda (0.32); seguir entrenándolo sobre la marcha tampoco (0.31). En 8 de 8 semillas.
- Generaliza la corrección a formas de preguntar que no había visto: 0.97 (contra 0.58 del entrenamiento sobre la marcha).
- Controles: con el premio barajado, 0.43; sin la compuerta que decide cuándo corregir, 0.12.
- Costo: +0.2 % por consulta.
- **Lo que no logra:** no le gana a un sistema de recuperación al que se le regala la identidad del hecho (empata), ni al entrenamiento sobre la marcha cuando la memoria es más pequeña que los cambios. Salvo con un mecanismo de "sueño": el modelo absorbe con entrenamiento lo que las células aprendieron y las libera.
- **Fragilidad declarada:** la compuerta con valor 0.9 falló en 3 de 8 semillas; se cambió a 0.98 **después de ver esas tres**. Está dicho en el informe; es exactamente el tipo de ajuste que el protocolo de JUACO no permitiría.

Lectura del estado del proyecto: "la hamburguesa funciona en juguete". El "pan" es un transformador de dos bloques y dimensión 24, con un vocabulario de 18 elementos y 20 hechos: no es un modelo real.

**Prototipo 4: cuarenta dimensiones.** Idea: colocar las células en un espacio de muchas dimensiones y repartir el premio según la cercanía.

- **No aprende** una tarea básica de paridad (0.50, el azar, en todas las dimensiones; el rival convencional llega a 1.00 en 100 exposiciones).
- Más dimensiones acortan los caminos entre células (de 8.9 saltos en una dimensión a 1.8 en cuarenta), pero desde unas diez dimensiones no aporta más que una red conectada al azar.
- Repartir el premio por cercanía sí distingue quién aportó (correlación de 0.25 a 0.35, contra 0.00 con premio igual para todas) y deja menos tramposas: entre 24 y 34 de 195, contra entre 99 y 150.
- Mover las células hacia el premio: **no**; se amontonan en la salida y dejan solas a las entradas.

### 11.4 Un patrón que se repite (observación, no resultado)

El registro anota que en cuatro montajes distintos del mismo día apareció lo mismo: **a qué nivel se paga decide si ganan las que cobran sin aportar.** En la red de células (pagar a grupos pequeños elimina al tramposo), en las cuarenta dimensiones (el premio por cercanía frena tramposas) y en el muro (la hipótesis del bien público sobre la limpieza). El registro lo marca expresamente: "es una observación, no un resultado".

### 11.5 Qué más hay en la carpeta exploratoria

| Documento | Qué es | Estado |
|---|---|---|
| `F0_relojes.md`, `AUDITORIA_F0.md` | La medición del reloj (sección 10). | Auditada: se sostiene con reservas. |
| `FABLE_gen_perdido.md` | La hipótesis del bien público (sección 9.6) y las fichas que originaron el mapa del muro. | Hipótesis sin medir. |
| `FABLE_bloques_autoentrenables.md` | Reflexión sobre bloques que aprenden solos: qué existe y dónde se atascó. | Trabajo de papel. |
| `ENTREGA_1_reactor.md` y borradores del "Reactor" | Un plan para hacer selección con poblaciones de cientos de cuerpos en ECO. Medido: el motor corre con costo casi lineal; base de partida, un solo órgano funcional (el de rechazo) fijado en 38 de 40 semillas. | Borrador; se correría en el computador nuevo. |
| `ESPEC_P9_ficha3.md` y su auditoría | La especificación de "planear" que las sondas liberaron sin construir. | Cerrado. |
| `ENTREGA_3_vocabulario_publicacion.md`, `PASO_C_literatura_avaladores.md` | Material para la publicación. | En curso. |
| `REVISION_organelos_soloLectura.md` | Una revisión independiente de la rama: los resultados de la Escalera del 30 de septiembre se sostienen contra los archivos. | Hecha. |

### 11.6 Cómo hablar de esto en el evento

- Sí: "Tenemos una exploración en juguete donde una memoria de células pegada a un modelo pequeño congelado retiene lo que vio una vez. No tiene protocolo ni réplica todavía."
- Sí: "Como modelo propio, con un rival justo, la red de células no gana."
- No: "funciona con modelos de lenguaje", "aprende mejor que una red neuronal", ni presentar la hamburguesa junto a los resultados declarados.

El siguiente paso escrito para Alejo es justamente pasarlo por el método: un modelo abierto pequeño de verdad, una compuerta que se ajuste sola, un sistema estándar de recuperación como rival, 20 semillas más réplica, y un criterio de abandono escrito antes.
