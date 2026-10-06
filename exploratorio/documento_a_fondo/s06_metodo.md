## 6. El método

**Idea principal.** El método es lo más sólido que tiene JUACO, y es lo que el póster realmente presenta. Parte de una desconfianza sana: quienes diseñan y programan los experimentos son agentes de inteligencia artificial, que se equivocan con mucha seguridad. Por eso cada pieza del método existe para atrapar un tipo de error concreto, casi siempre uno que ya ocurrió. La regla madre está en `registro/EQUIPO.md`: "la misión manda sobre las preferencias de cada agente; el método manda sobre la misión: un resultado que no pasa por el protocolo no cuenta, aunque apunte hacia la misión".

### 6.1 Las piezas, y qué error evita cada una

| Pieza | Qué es, en palabras llanas | Qué error evita |
|---|---|---|
| **Preregistro** | Un documento que se escribe y se guarda con fecha **antes** de correr: qué se pregunta, qué mundo, qué se mide, qué número se espera, qué resultado refutaría la idea y qué control podría ganar. | Acomodar la explicación al resultado después de verlo. Es como entregar la rúbrica de evaluación antes del examen. |
| **Commit previo** | El preregistro queda guardado en el historial del repositorio antes de que exista un dato. | "Predicciones" escritas con los datos ya a la vista (ERR-154: una predicción sin registro previo no cuenta como predicción). |
| **Predicciones firmadas con probabilidad** | El autor escribe, por ejemplo, "FUNCIONA con probabilidad 0.55" y rangos numéricos. Después se anotan las que acertó y las que falló. | El "yo ya sabía". También calibra a los agentes: en el registro hay decenas de predicciones propias marcadas como refutadas. |
| **Construcción por anclas** | Un organismo nuevo no se edita a mano: un programa toma el texto del anterior e inserta líneas en sitios exactos, cada uno una sola vez. El original no se toca. | Cambios accidentales en lo que ya funcionaba. |
| **Arnés de identidad** | Una batería de comprobaciones: con el módulo nuevo apagado, el organismo debe dar un resultado **idéntico bit a bit** al anterior. Se corre antes de mirar cualquier número. | Creer que se midió el módulo cuando en realidad se cambió otra cosa sin querer. |
| **Sha** | Una huella digital de 16 caracteres de cada archivo. Si el archivo cambia en una coma, la huella cambia. Los corredores se niegan a arrancar si la huella no coincide con la registrada. | Correr con una versión distinta de la que se preregistró. |
| **Humo** | Una corrida muy corta, de un solo proceso, que no cuenta como dato. Sólo comprueba que todo el camino funciona, hasta escribir el archivo de resultados. | Series de horas perdidas por un error tonto al final (ERR-42: una ruta mal copiada falló después del veredicto y se perdió el archivo). |
| **Auditor antes** | Un agente distinto, de sólo lectura, revisa preregistro e instrumento antes de la serie y entrega hallazgos numerados. | Controles que no controlan, criterios incoherentes, vocabulario inflado. |
| **Serie** | 20 semillas nuevas, con la regla ya fija. | Conclusiones sacadas de una o dos corridas con suerte. |
| **Réplica** | Otras 20 semillas, jamás usadas, misma regla y mismo código. Sólo con las dos se escribe "×2". | La casualidad. Es la pieza que tumbó la moneda del muro y "O1 libre". |
| **Auditor después** | El auditor recalcula los números desde los archivos crudos con un programa propio, sin usar el del experimento. Veredictos posibles: "se sostiene", "se sostiene con reservas", "no se sostiene". | Errores de cuenta y lecturas optimistas. |
| **Letra por código** | La regla de decisión ("gana en 13 de 20 o más y por 10 o más en la suma") está escrita como programa. El veredicto lo imprime el programa, no una persona. | Leer un resultado dudoso con buenos ojos. |
| **Empates en contra** | Un empate entre candidato y control cuenta como derrota del candidato. | Ganar por inercia. |
| **Nulo (placebo)** | Antes de correr se calcula qué tan fácil sería pasar la puerta por pura suerte si la idea fuera falsa. Ninguna puerta puede tener un umbral que el azar pase con frecuencia. | Puertas que se pasan solas (ERR-91: se descubrió que un criterio anterior rechazaba incluso al propio organismo de referencia). |
| **Control que puede ganar** | Cada experimento lleva un rival diseñado para tener el mismo esfuerzo y el contenido equivocado: memoria leída en el sitio opuesto, señal sembrada al revés, genes que nadie usa. Tiene que poder ganar de verdad. | Atribuir al contenido lo que era sólo "moverse más" o "tener más ruido". |
| **Regla de parada** | Escrita antes: cuándo se replica (si quedó en el umbral, si funcionó), cuándo se cierra (tres humos sin señal), cuándo no se insiste. | Seguir intentando hasta que salga. |
| **Las cuatro trampas** | Lista fija que se revisa en cada diseño: canal simétrico (¿quién se beneficia de la señal?), acierto sin balancear, mundo que se come la comida, sitios fijos que se memorizan. | Cuatro errores que ya ocurrieron la noche del 17 de septiembre. |
| **Vocabulario** | Cada resultado trae su lista de frases permitidas y prohibidas. | Decir "aprende", "razona" o "comunica" cuando lo medido es más pequeño. |
| **Exploratorio aparte** | Lo que se prueba sin protocolo se marca como exploración y vive en otra carpeta. | Que una corazonada entre al registro como hecho (ERR-177). |

Hay además una división de trabajo que es parte del método: **sólo el coordinador corre experimentos grandes**; los demás agentes sólo corren comprobaciones de un proceso. Los agentes no guardan cambios en la rama principal. Y el director decide lo que toca el tronco, los niveles y lo que se publica.

### 6.2 Qué es un ERR

Un ERR es un **error numerado**: del instrumento, del criterio, de la lectura o del procedimiento. Cada uno queda en el registro con qué pasó, cómo se detectó, qué cambió y, cuando aplica, qué habría pasado sin el cambio. No se borra nada: las correcciones se añaden debajo.

**Cuántos hay.** La numeración corre desde ERR-1. El archivo de resultados verificados habla de "ERR-1 … ERR-153" al 29 de septiembre, y la tesis de la publicación de "153 errores registrados". Al cierre del 1 de octubre el último usado es **ERR-190**, y ERR-191 es un candidato sin abrir. La numeración **tiene huecos**, así que el último número no es la cantidad: no aparecen usados 127 a 129 ni 135 a 139; del bloque 160 a 169, reservado a otra sesión, se usó sólo el 160; el 178 quedó reservado y sin usar; y el bloque 180 a 189 no tiene definiciones en el repositorio. [El conteo exacto de errores distintos no lo verifiqué: sale del archivo `informe/errores.csv` que la ruta de publicación tiene pendiente.]

No existe un archivo único con la lista: los ERR están dentro del registro (`registro/REGISTRO_etapas_1_2.md`), en los preregistros y en el reglamento de la carrera.

### 6.3 Tres ERR contados como historia

**ERR-96: el carro tramposo (22 de septiembre).** Antes de la primera ronda de la carrera, el auditor leyó la pista y vio que la salida de cada organismo se mezclaba con los datos físicos sin filtro. Un carro podía escribir "tuve 999 999 hijos" y el juez le creía. Para demostrarlo se construyó un carro tramposo que declaró 999 999 hijos teniendo cero reales. Se arregló antes de correr nada oficial: desde entonces el juez calcula todo sólo desde la física de la pista, lo que dice el carro va en un cajón aparte que nadie lee como verdad, y hay una prueba permanente con el tramposo. *Qué enseña: no se le pregunta al evaluado cuánto sacó.*

**ERR-170: el control que no controlaba (30 de septiembre).** En el peldaño de memoria de lugar, el control debía leer la memoria "en el lugar equivocado". La primera versión barajaba las casillas al azar. El auditor revisó y encontró que, con ese barajado, cerca del 45 % de las veces el control terminaba leyendo el oasis de todos modos: no era un control, era un candidato a medias. Se cambió, antes de la serie, por leer siempre la casilla del lado opuesto del anillo, que nunca puede caer en el oasis. Con el control arreglado sacó 0 de 180. *Qué enseña: un control de "contenido equivocado" hay que verificar que de verdad no acierte.*

**ERR-177: la moneda del muro (1 de octubre).** El 30 de septiembre, una exploración con cinco cadenas pareció mostrar algo importante: que con pasajes largos (100 000 pasos) y sembrando sólo de linajes establecidos, la selección **conservaba** la regla que hace cruzar, mientras con pasajes cortos la purgaba. El resultado estaba "en el umbral" (4 de 5 en la lectura estricta), y los cortes se habían elegido viendo los datos; ya un error anterior, ERR-176, había endurecido el criterio por riesgo de falso positivo. Aun así, entró al estado del proyecto, al documento de traspaso y al registro **escrito como causa**: "la moneda de la selección era un candado del muro". Al día siguiente se corrió la réplica con diez cadenas y preregistro: la regla terminó en 0.0 con la "moneda" contra 0.42 en el neutro, y en cruce 41 contra 42 de 90. Indeterminado; no replicó. Hubo que retirar la frase de tres documentos y añadir notas de corrección. Regla nueva: **lo exploratorio en el umbral se registra como exploratorio, con el verbo en condicional y sin explicación causal, hasta que cierre una réplica.** *Qué enseña: el error no fue del experimento sino de la prosa. Una frase bonita se adelantó a la evidencia.* Y vale notar que la hipótesis refutada incluía una del propio director ("la cadena que conserva la regla cruza más"): 41 contra 42.

### 6.4 Las reglas numeradas

Están en `registro/EQUIPO.md` (reglas 1 a 15). Las que más se citan:

| Regla | Qué dice | De dónde salió |
|---|---|---|
| 3 | Sólo el coordinador corre experimentos con varios procesos a la vez; un agente corre sólo comprobaciones de un proceso. | Orden de la máquina y de la responsabilidad. |
| 4 | Preregistrar antes de correr. Nunca recalibrar después de ver datos: se numera un ERR, se escribe un criterio nuevo y se usan semillas nuevas. | Regla base. |
| **11** | Toda enmienda que cambie un umbral o la forma de un criterio lleva número de ERR **al escribirla**, aunque se haga antes de la serie y aunque resulte no tener efecto. | Dos errores se habían numerado tarde. Es la regla que obligó a declarar ERR-175 y ERR-179. |
| **12** | Un veredicto que dependa de una sola semilla en el umbral dispara réplica automática con semillas nuevas. Efectos pequeños sólo se declaran con 40 semillas. | Acordada con el director el 18 de septiembre. Es la que hizo replicar PISA. |
| 13 | La misión va al principio de cada encargo a un agente. | Decisión del director. |
| **14** | Cuando se copia una batería para un candidato, la entrada nueva se compara **campo a campo** con la del tronco antes de correr; y toda batería copiada pasa un humo que llegue a escribir su archivo. | ERR-38: una copia había omitido dos parámetros y el mal resultado era del instrumento, no del organismo. En la práctica: cada corrida de la Escalera "es" la misma función que usa el tronco. |
| **15** | Todo criterio corre su placebo: toda puerta declara antes su nulo y su margen; toda tasa de acierto se reporta balanceada. | ERR-91: un criterio rechazaba al propio organismo de referencia. |

Las reglas de trabajo del proyecto original (`bundle/CLAUDE.md`) añaden dos que el director puede citar con propiedad: "ante una anomalía, la primera hipótesis es el instrumento" (tres de las tres primeras anomalías del proyecto fueron del instrumento) y "no declarar inteligencia general ni conciencia por ningún resultado".

### 6.5 Lo que el método no arregla

Para decirlo con honestidad en el evento:

- **Los controles son todos internos.** El propio informe de publicación lo llama "lo más débil hoy". Casi nada se ha comparado con métodos estándar de la literatura.
- **Serie y réplica comparten código.** Si el código tiene un defecto, lo tienen las dos. La réplica protege contra la suerte, no contra un instrumento mal hecho.
- **El auditor también es un agente de inteligencia artificial.** Es independiente en el sentido de que no escribió lo que revisa y recalcula con su propio programa, pero no es una persona externa.
- **El sesgo del diseñador existe y está declarado, no eliminado.** Varios mundos se ajustaron hasta que el módulo ganó en dos semillas.
- **Nadie de fuera lo ha revisado todavía.** No hay publicación con revisión por pares. Sí hay una reproducción hecha por el director en su máquina de un resultado (BLOQUES), que dio los mismos archivos salvo el tiempo de cómputo.
