## 9. El muro

**Idea principal.** "El muro" es el nombre que el proyecto le da a un umbral concreto en la pista vieja: que un linaje se sostenga casi sin extinguirse (R0 real de 0.90 o más y ningún fundador después del paso 10 000). Hay que separar dos muros distintos. El primero, **que exista un organismo que cruce**, se superó el 22 de septiembre: O1 cruza, y lo escribió un agente. El segundo, **que un organismo llegue a cruzar solo, por selección**, sigue en pie: ningún montaje lo ha logrado. Todo lo de la Escalera ocurre en otro mundo y no dice nada sobre este muro.

### 9.1 Qué es exactamente

En la pista vieja el umbral se llama H-1 y viene de la fase 9. La regla vigente (sección 5) dice que un linaje cruza si su R0 real es 0.90 o más, tuvo cinco muertes o más, y no necesitó fundadores después del paso 10 000. Un organismo "cruza el muro" cuando, en una serie de 20 semillas, la mayoría de sus nueve linajes cruza en 15 semillas o más.

Por qué es difícil: el mundo se tapa de veneno y sal (sección 2.3). Para vivir no basta con evitar lo malo; alguien tiene que quitarlo de en medio, y quitarlo duele. En la fase 9, con un solo cuerpo, se midió que ni un "oráculo" (un organismo al que se le daba la tabla verdadera) cruzaba: de ahí la frase "el muro es el mundo". Con nueve cuerpos en la pista escalada esa frase vale sólo a medias: O1 por nueve sí cruza, O1 solo no.

Números de referencia en la pista vieja (linajes que cruzan, de 180, y semillas con mayoría, de 20):

| Organismo | Cruzan de 180 | Mayorías de 20 |
|---|---|---|
| Tronco v14.3 | 49 a 61 | 0 a 2 |
| Tronco + termostato (TERMO) | 90 a 101 | 11 a 14 |
| O1 | 135 a 139 | 18 a 20 |

### 9.2 Los dos muros

**Muro 1: que exista uno que cruce.** Superado por diseño. O1 lo cruza con un margen pequeño (R0 real 0.941 contra un umbral de 0.90). TERMO lleva al tronco a la misma altura en la mediana (0.923 y 0.932) pero no en la puerta estricta.

**Muro 2: que llegue solo.** Se intentó muchas veces darle a la selección los medios para encontrar lo que O1 tiene. Resultado hasta hoy:

- La selección **sí** encuentra el termostato (una perilla, desde la zona letal: 20 de 20, dos veces). Eso la lleva hasta la altura de TERMO y ahí se agota.
- La selección **conserva** a O1 pero no lo mejora: partiendo de O1 con cuatro números heredables, tras diez pasajes cruzan 128; O1 de fábrica 135; y el mismo proceso sin selección (deriva) 81. Sin selección O1 se degrada; con selección se mantiene. (Una serie, sin réplica.)
- Lo que falta entre TERMO y O1 (unos 35 a 45 linajes) no tiene ningún paso intermedio medido que pague: las piezas sueltas de O1 puestas sobre TERMO no cruzan (sección 8).

### 9.3 Qué tiene O1 que el tronco no

Según la lectura del genetista de la junta (`exploratorio/investigacion_20261001/FABLE_gen_perdido.md`), verificada contra el código de O1:

1. **La boca con consigna sobre lo bueno**: muerde lo bueno sólo si la necesidad que sube está por debajo del umbral de parto más un margen. El tronco decide con una probabilidad empujada por el hambre.
2. **La limpieza**: muerde lo malo sólo cuando no queda nada útil, con el golpe en la necesidad más llena y con un piso.
3. **Las patas**: puntaje por ganancia y distancia, ceder lo que otro tiene más cerca, ir al hueco.
4. **La prueba prudente** de lo desconocido.
5. **Una tabla simple y exacta** por letra, del linaje.

De estas cinco, la primera es la que más carga y **ya está cerrada**: es el termostato, y cierra más o menos el 60 % de la distancia en R0 entre el tronco y O1. La segunda es necesaria dentro de O1 y dañina suelta: puesta sola sobre el tronco o sobre TERMO, hunde al organismo. Las patas y la prueba no se separan del ruido.

### 9.4 Lo que dice el mapa (exploratorio, dos semillas)

El 1 de octubre se construyó un O1 con seis genes fijables (MARGEN, PRUEBA, PEN_OTRO, PISO, y dos interruptores: limpieza y hueco) y se corrió una rejilla de valores en la pista vieja. **Es una sonda: una o dos semillas, nueve linajes cada una, nada se declara.** Las predicciones se escribieron antes de correr; varias fallaron.

**MARGEN es una rampa.** Cruzan de 9 en las dos semillas:

| MARGEN | 0 | 0.03 | 0.06 | 0.10 | 0.25 (fábrica) | 0.5 |
|---|---|---|---|---|---|---|
| Semilla 1 | 0 | 0 | 3 | 8 | 4 | 5 |
| Semilla 2 | 0 | 4 | 8 | 9 | 8 | 5 |

Lo que importa de esa tabla no son los números sueltos sino la forma: no hay un acantilado. Cada pasito de MARGEN paga algo. Eso es exactamente lo que la selección necesita para poder subir una perilla de a poco.

**La limpieza suma sólo después.** Partiendo de "todo apagado":

| Se prende | Semilla 1 | Semilla 2 |
|---|---|---|
| nada | 0 | 0 |
| sólo MARGEN | 5 | 6 |
| sólo PISO | 0 | 0 |
| sólo la limpieza | 0 | 0 |
| MARGEN + PISO | 5 | 6 |
| MARGEN + limpieza + PISO | 7 | 7 |
| lo anterior + PEN_OTRO | 7 | 6 |

Lectura propuesta por el ingeniero: una escalera de dos peldaños **con orden** (primero MARGEN, después limpieza), no un valle que haya que cruzar a ciegas. Su propia predicción ("desde apagado ningún gen solo pasa de 1 de 9") quedó refutada.

**PISO, PEN_OTRO y PRUEBA**: sin tendencia en una semilla.

### 9.5 El fundador limpio (candidato ERR-191)

El mapa trajo una sorpresa que obliga a cautela con todo lo anterior. O1 **sin** limpieza cruzó 5 y 6 de 9. El mismo organismo, en la serie sellada de septiembre, cruzó 0 de 180.

La diferencia no es del instrumento (el comparador canónico da la misma fila, campo a campo). Es la regla de fundador:

- En septiembre, el fundador de reemplazo conservaba la libreta del linaje: sabía qué era malo y nunca lo mordía. Sin regla de limpieza, nadie limpiaba. Resultado: 0 de 180.
- Con fundador limpio, cada reemplazo nace sin libreta y prueba el veneno y la sal una vez. Los linajes que se hunden se refundan cientos de veces y, con esas pruebas, limpian el mundo: alrededor de 750 mordidas malas por cada 100 000 pasos. Los linajes establecidos, en cambio, tienen exactamente 2 mordidas malas (una prueba de cada una).

Dicho llanamente: **con fundador limpio la pista regala limpieza por nacimiento**, y un organismo sin limpieza puede cruzar "a costa de dos a cuatro linajes que no paran de nacer y morir".

Por eso este documento no afirma nada nuevo sobre la limpieza. El candidato no está abierto como error; el plan es decidir qué hacer con esa prueba del fundador, revisar qué series viejas usaron cada regla, repetir el mapa con fundador no limpio, y sólo entonces leer.

### 9.6 La hipótesis del bien público (sin medir)

Es la idea más sugestiva de la junta y hay que presentarla exactamente como lo que es: **una hipótesis sin medir**.

Un "bien público" es algo que le cuesta a quien lo produce y beneficia a todos, como barrer la calle. La hipótesis dice: la limpieza es un bien público. El que muerde lo malo paga el golpe; los ocho vecinos cobran la comida que aparece. Si la selección actúa entre linajes que comparten un mismo mundo, premia al que **no** limpia (el "polizón", el que viaja sin pagar). Entonces el "gen perdido" no sería un gen sino el **nivel** al que se selecciona: la limpieza se fijaría si compitieran mundos enteros de clones, no linajes dentro de un mundo mezclado.

Qué hay a favor, y por qué no alcanza:

- En tres montajes la selección subió PISO, que equivale a "limpiar menos hondo". El genetista lo lee como la firma del polizón. Pero el registro dice que esa firma **no se puede leer**: la señal dentro de cada semilla es débil y de poco poder.
- En pista mixta (dos semillas): cuando hay ocho que no limpian y uno que sí, el único que limpia queda con R0 0.002 y 0.004 y 487 y 471 fundadores, mientras seis de los ocho que no limpian cruzan. Se ve el **costo** del que limpia. Al revés (ocho que limpian y uno que no), el que no limpia no cruza ni le gana a sus vecinos: **no se ve el beneficio del polizón**. Y la limpieza por nacimiento del fundador limpio confunde las dos lecturas.

Cómo se mediría: dos cámaras con el mismo gen, las mismas semillas y la misma mutación; una "mixta" (la selección entre linajes de un mismo mundo) y otra "clonal" (cada mundo lleva un solo genoma y compiten mundos). Está en el plan, con preregistro antes, y el control puede ganar.

### 9.7 Lo que se retiró el 1 de octubre

Durante un día el registro dijo que "la moneda de la selección era un candado del muro": que los pasajes cortos purgaban la regla que cruza y los largos la conservaban. La réplica no lo confirmó (sección 8.2 y ERR-177 en la sección 6). Lo que queda: a 25 000 pasos la selección purga la regla (0.26 contra 0.64); a 100 000 con siembra de establecidos el resultado es indeterminado. "Candado" no se sostiene como causa.

### 9.8 Por qué el muro resistió y "perillas" no

La comparación, tomada del genetista, ayuda a entender qué cambió:

| | Perillas (mundo con oasis) | Intentos contra el muro |
|---|---|---|
| Qué debía encontrar la selección | una perilla de un módulo ya escrito, desde cero | cuatro números que ya estaban en su mejor zona, o una regla que había que armar de piezas |
| Cuánto paga | de 7 a unos 80 linajes de 180 | de 52 a 101 (termostato); menos en el resto |
| ¿El primer paso paga solo? | sí | el del termostato sí; el de una regla armada, no (se fijó en 0 de 5 cadenas) |
| Mutación y reloj | una por nacimiento, con sesgo; unos 80 eventos | cuatro genes a la vez; de 12 a 30 eventos |
| Qué premia el montaje | durar, en 100 000 pasos | estar vivo al muestreo, en 25 000 |
| ¿Beneficio privado o público? | privado (el viaje al oasis) | la limpieza sería público (hipótesis) |

De ahí sale el plan vigente: aplicar el montaje de perillas, que ya funcionó dos veces, a MARGEN como gen desde cero en la pista vieja.

### 9.9 La pregunta abierta: ¿es la meta correcta?

Esto conviene decirlo sin rodeos, porque en el evento alguien lo va a preguntar.

- La medida tuvo que corregirse varias veces (ERR-99, 100, 102): contaba hijos que no nacían, se disparaba con organismos que no morían, y premiaba morir. Lo que hoy significa "R0 real cerca de 1" es "casi ninguna extinción", no "crecimiento".
- El director decidió el 28 de septiembre declarar el muro **mapeado** y no hacer más intentos directos sobre él. Los únicos resultados donde la selección construyó algo nuevo (ECO_SEL, BLOQUES) salieron en otro mundo y midiendo otra cosa.
- El propio director dejó escrito, para la sección de lecciones de la publicación, que su error más costoso fue perseguir durante diez fases el techo de sus propias pruebas, "peleado con benchmarks y no con la evolución de verdad".
- Y hoy hay una duda técnica adicional: con fundador limpio, parte de lo que el muro mide puede ser un regalo de la pista.

Nada de eso invalida lo medido. Sí significa que "cruzar el muro" es un instrumento del proyecto, no un hecho del mundo, y que la pregunta "¿vale la pena seguir empujando esta pared o es mejor construir un mundo donde las capacidades paguen?" está abierta. La Escalera es, en parte, la respuesta práctica del director a esa pregunta.
