# ALEJO — documento de arranque (1-oct-2026)

Proyecto número 2 del director Christiam (nombre por su hijo Joaquín Alejandro; JUACO es el primero). Redactado desde el repo en solo lectura; no corrí nada ni hice git.
Marcas: [V] verificado en el repo (archivo:línea) · [F] abierto hoy (URL) · [M] de memoria · [I] inferencia mía. Rutas relativas a `PROYECTOS\JUACO\` salvo que diga otra cosa.

**VEREDICTO: HAY ALGO MODESTO, y es explorable.** Hay dos preguntas concretas que se miden en una tarde sin GPU, con respuesta que puede salir NO. Lo que hoy no existe es evidencia de que una célula local le sirva a un modelo grande; existe la forma de averiguarlo barato.

## 1. Qué es Alejo, y en qué se diferencia de JUACO

Alejo es el intento de averiguar si una **célula pequeña con plasticidad local acotada** (aprende de su propio flujo, olvida, se corrige con la señal de otra) sirve como **pieza útil dentro o al lado de modelos entrenados con gradiente**, y si varias de ellas pueden formar un **decisor propio, hiperespecializado y barato**, hecho en Latinoamérica sin presupuesto de laboratorio.

| | JUACO | Alejo |
|---|---|---|
| Pregunta | ¿puede haber vida mínima con reglas locales, sin retropropagación? | ¿sirve la célula como pieza práctica, sola o junto a un modelo con gradiente? |
| Retropropagación | prohibida dentro del tronco [V bundle/CLAUDE.md:195-199] | permitida **fuera de la célula**: como techo de comparación y como herramienta de entrenamiento del resto del sistema |
| Mundo | comida, hambre, muerte, parto | información: flujos de decisiones, hechos que cambian, reglas que cambian |
| Éxito | un peldaño de la Escalera con control de contenido equivocado | ganarle a una línea de base hecha a mano, **o** acercarse a un techo con gradiente a menor costo, **o** perder limpio |
| Nivel de evidencia | vida artificial con método | ingeniería medida; si sale algo, comparable con la literatura estándar |

Regla de higiene: Alejo **no** cuenta como avance de JUACO ni hereda sus niveles. Si Alejo prueba que la célula sirve, eso es evidencia indirecta sobre JUACO (las piezas se parecen), no prueba de que haya vida.

## 2. Las dos perspectivas

### Perspectiva A — la célula como "transistor" de un modelo grande (memoria, controlador, entrenador, disruptor)

**Versión más fuerte a favor.** Los modelos grandes tienen pesos congelados al desplegarse; todo lo que "aprenden en uso" es contexto, que cuesta cómputo cuadrático y se pierde. Eso es un hueco real y de moda: Google publicó un módulo de memoria que aprende en el momento de la prueba, guiado por "sorpresa" [F https://arxiv.org/abs/2501.00663], y Meta mostró capas de memoria entrenable que añaden parámetros sin añadir cómputo [F https://arxiv.org/abs/2412.09764]. Una célula con error de predicción propio, traza de un paso, olvido y compuerta de escritura es esa idea en pequeño, auditable módulo a módulo. El argumento es: no competimos con el modelo; le ponemos al lado una memoria/corrector de bajo costo que se corrige en uso sin reentrenar.

**Qué tendría que ser cierto.** (a) Que una regla local sobre los estados internos del modelo congelado corrija errores nuevos en pocas exposiciones. (b) Que lo haga **mejor o más barato** que lo ya estándar: un diccionario/vecino más cercano sobre embeddings (kNN-LM, caché de hechos) y que un ajuste fino con gradiente de una capa o un adaptador LoRA [M]. (c) Que no destruya lo que sí valía (retención).

**Qué pieza de JUACO medida aporta.**
- PISA: regla de escritura con compuerta por estado propio; corrige memoria caducada con la señal ajena sin pisar lo que sirve: latencia 973 (pmix) vs 1566 (mudo) pasos; FUNCIONA ×2 (réplica `escalera/mixto/replica_pool2.log:136`) [V investigacion_20261001/FABLE_bloques_autoentrenables.md:82].
- Plasticidad local acotada (Rescorla-Wagner con traza de un paso, techo por canal) [V registro/HANDOFF.md:39,57]; con costo conocido: el techo produjo BUG-01, "no se aprende nada más" [V HANDOFF.md:110-117].
- XOR cerrada: con prior de pares bastan 7–10 exposiciones, sin prior "nadie puede" con 8 [V bundle/CLAUDE.md:204-208]. Molde honesto: **la regla local generaliza si la representación hace lineal la tarea**. En un modelo grande esa representación la regala el modelo congelado.
- Perillas: la selección prende sola una perilla cuando el mundo la paga (serie FUNCIONA; réplica en curso, no declarada) [V escalera/perillas/serie_pool2.log:189].

**Qué falta.** Todo lo medido es en mundos de juguete propios. Nunca se conectó la célula a los estados de un modelo real. El olvido NO está resuelto: lo local olvida igual (retención de lo ausente 0.67 [V bundle/CLAUDE.md:299]).

### Perspectiva B — un modelo propio, hiperespecializado (decidir), no un LLM

**Versión más fuerte a favor.** Un decisor pequeño no necesita lenguaje: necesita mapear contexto→acción, adaptarse cuando la regla del mundo cambia y costar casi nada por decisión. Ahí la ventaja de una célula local es estructural: aprender en uso, sin ciclo de reentrenamiento, en un PC o un celular, con cada módulo apagable y auditable. Para escuelas rurales o agro, un decisor de 50 KB que se adapta al sitio vale más que una API en dólares [I]. Y no compite en el terreno de los laboratorios.

**Qué tendría que ser cierto.** (a) Que en una tarea de decisión no estacionaria la red de células se recupere tras un cambio de regla igual o más rápido que un decisor con gradiente en línea, a una fracción del costo por decisión. (b) Que ninguna línea de base hecha a mano (promedio con descuento, ventana deslizante, Q tabular) ya haga lo mismo, porque en problemas chicos casi siempre lo hace [I]. (c) Que escale a más contexto sin colapsar (la literatura de reglas locales se atasca en profundidad: SoftHebb 27.3 % en ImageNet [F https://arxiv.org/abs/2209.11883]; lo que escaló usó gradiente en un bucle externo [V FABLE_bloques_autoentrenables.md:33]).

**Qué pieza de JUACO aporta.** La boca que decide por la necesidad activa (RL homeostático) [V bundle/CLAUDE.md:213-215]; "aprende en menos de una vida" (fase 9) [V bundle/CLAUDE.md:5]; selección que afina perillas, no inventa combinaciones [V registro/ESTADO.md:20]; ir a lo menos visitado cuando el oasis se muda: 164/163 de 180 linajes, ×2 [V ESTADO.md:15] (es una política de exploración bajo cambio: la forma de una decisión no estacionaria).

**Qué falta.** (i) Líneas de base estándar: el propio informe de publicación dice que es "lo más débil hoy: todos los controles son internos" [V investigacion_20261001/ENTREGA_3_vocabulario_publicacion.md:61]. (ii) Reparto de crédito a más de un paso: P9 planear CERRADO ×3 [V escalera/ESCALERA.md:232]. (iii) Una tarea real de decisión con datos reales.

### Dato nuevo de hoy, sin declarar: el prototipo de red de células
`red_celulas/` (otro agente, 11:57) **no tiene INFORME.md todavía**: hueco señalado. Lo que hay son dos humos de 4 semillas sin preregistro (suma mod 7, 30 pares vistos/19 retenidos, red de 40 células con vida y tanteo local vs. techo MLP) [V investigacion_20261001/red_celulas/datos/humo_angulos_n40.json y humo_onehot_n40.json]. Lectura honesta: **ningún brazo generaliza a los 19 retenidos** (0.00–0.21 en todos, incluso el techo MLP con prior de ángulos: 0.11), y la red completa **no supera a la plasticidad sin vida** en pares vistos (0.40 vs 0.62 con ángulos). Dos consecuencias: (1) no hay todavía ninguna señal a favor de la red de células; (2) el techo con 0.11 en retenidos con un prior que debería hacer la tarea lineal es sospechoso de instrumento (pocas exposiciones, tasa de aprendizaje, o el MLP simplemente no grokeó con 30 de 49 pares, como FABLE advirtió [V FABLE_bloques_autoentrenables.md:63]) [I]. **Regla para Alejo: ningún experimento cuenta hasta que su techo pase una prueba de cordura** (ver paso 0 abajo).

## 3. Primer y segundo experimento de cada perspectiva

**Paso 0, común (1 hora): cordura del techo y de las líneas de base.** Antes de cualquier brazo con células: el MLP/adaptador con gradiente debe resolver la tarea con todos los datos (acierto ≥ 0.98 en entrenamiento y en retenidos del mismo dominio) y la línea de base a mano debe dar el valor teórico esperado. Si el techo no pasa, el experimento no existe (como ERR de instrumento, estilo ERR-155/171).

### A1 — Memoria que corrige hechos cambiados en un modelo congelado (una tarde, CPU)
- **Tarea.** Un modelo pequeño ya entrenado y congelado (p. ej. un transformer chico de unos 100M parámetros o un codificador de frases; en CPU extraer los estados de unas 3 000 frases cortas toma minutos [I]) sobre 60 "hechos" sintéticos (clave→valor; ej. "El código de la finca 17 es 4"). A mitad del flujo, 15 hechos **cambian** (como el cambio de regla de la Escalera). Las consultas llegan reformuladas con 3 paráfrasis por hecho; el valor correcto llega después de cada consulta (la célula se entera por su propio error, sin etiqueta externa).
- **Brazos.** (1) modelo congelado solo; (2) **línea de base a mano**: diccionario por clave exacta, último valor visto; (3) **línea de base a mano 2**: vecino más cercano (kNN) sobre los mismos estados; (4) **célula**: memoria lateral con regla delta local y compuerta tipo PISA (sólo escribe si su error propio > umbral); (5) **techo con gradiente**: ajuste fino de la última capa (o LoRA) con el mismo flujo; (6) control de contenido equivocado: célula con las claves barajadas; (7) célula con plasticidad apagada.
- **Medida.** Acierto en los 15 hechos cambiados (con paráfrasis nunca vistas) tras 1, 3 y 10 exposiciones; acierto en los 45 no cambiados (retención); costo en operaciones por consulta. 20 semillas, mediana; serie 1–20, réplica 21–40.
- **Predicción numérica (puede fallar).** Célula: ≥ 0.90 en cambiados con ≤ 3 exposiciones en ≥ 16/20 semillas y retención ≥ 0.95. Diccionario exacto: **gana a la célula con consultas exactas** (≈1.0) y **cae a ≤ 0.35 con paráfrasis**. kNN: 0.85–0.95 (queda empatado con la célula: esa es mi predicción central, y es mala para la tesis). Techo con gradiente: ≥ 0.90 pero con retención 0.80–0.93 (olvido). Barajado y apagado: ≤ 0.25.
- **Control que puede ganar.** El diccionario en exactas y el kNN en todo. Si kNN iguala o supera a la célula en cambiados **y** retención, la célula no aporta nada sobre una caché estándar.
- **Criterio de abandono.** kNN ≥ célula en ambas medidas en la réplica → A se reduce a "ya existe"; se cierra y se documenta. También se abandona si la célula con barajado ≥ 0.5 (no usa el contenido).
- **Segundo experimento, con GPU de la UIS (si A1 sale).** Mismo diseño con un LLM abierto de 1–8B congelado: la célula lee estados de una capa intermedia y corrige respuestas en un benchmark de edición de conocimiento (CounterFact/zsRE, métodos ROME/MEMIT como línea de base [M]) más una prueba de pocas muestras en español. Brazos extra: LoRA, memoria tipo Titans de código público si lo hay [M]. Medida añadida: acierto en preguntas **vecinas** (que no deben cambiar) y latencia. La GPU hace falta para correr el modelo, no para la célula.

### B1 — Decisor en un mundo que cambia de regla (una tarde, CPU)
- **Tarea.** Bandido contextual no estacionario: 8 contextos, 4 acciones, premio con probabilidad 0.8 para la acción correcta de cada contexto y 0.2 para el resto; **cada 500 pasos la regla (contexto→acción) cambia** en 3 de los 8 contextos; 20 000 pasos.
- **Brazos.** (1) azar; (2) **línea de base a mano**: promedio con descuento por contexto/acción con ε-greedy, y UCB con ventana deslizante (las dos, mejor de ambas por semilla: se declara); (3) **red de células** (la del prototipo `red_celulas`, o O1 en forma de tabla de dS, sin retropropagación) con y sin compuerta PISA; (4) **techo con gradiente**: MLP pequeño con Adam en línea, y un Q-learning tabular; (5) control: señal de premio barajada; (6) plasticidad apagada.
- **Medida.** Arrepentimiento acumulado; pasos hasta recuperar 90 % de aciertos tras un cambio (mediana de 40 cambios); operaciones y bytes por decisión. 20 semillas; réplica con otras 20.
- **Predicción numérica (puede fallar).** La línea de base a mano gana en arrepentimiento (es el problema de manual). La red de células, con PISA, se recupera en ≤ 150 pasos y **a menos de la mitad del tiempo del MLP con Adam en línea** (≥ 2× más rápida) en ≥ 14/20 semillas, con ≥ 5× menos operaciones por decisión que el MLP; sin PISA, igual que el MLP o peor. Barajado y apagado: azar.
- **Control que puede ganar.** La línea de base a mano en arrepentimiento y el Q tabular en todo. Si el Q tabular iguala a la red en recuperación y costo, el decisor propio no tiene ventaja.
- **Criterio de abandono.** La red tarda más de 400 pasos en recuperarse, o PISA no mejora sobre sin PISA en 13/20 semillas (la pieza más reciente de JUACO no transfiere). Se abandona B1 como "decisor general"; queda como nota negativa.
- **Segundo experimento, con GPU (si B1 sale).** Decisión con datos reales y espacio grande (por ejemplo, decisiones agrícolas o de triaje de un conjunto abierto, con cientos de contextos), y **población de redes con perillas por selección corrida en la GPU** (miles de redes vectorizadas): ahí la GPU sí aporta, porque el bucle externo de selección (perillas) es lo costoso. Línea de base: gradiente bien afinado y un árbol/boosting estándar [M]. Medida añadida: tiempo de adaptación al cambio de distribución y tamaño en KB.

## 4. Ventaja competitiva honesta

| Donde un equipo sin presupuesto puede tener algo | Condición | Donde no |
|---|---|---|
| **Aprendizaje en uso, sin reentrenar** | solo si A1/B1 pasan; aún es hipótesis | no se compite en capacidad general ni en lenguaje |
| **Auditabilidad por módulo**: apagado bit a bit, control de contenido equivocado, ~180 ERR registrados [V FABLE_bloques_autoentrenables.md:44] | es lo mejor medido de JUACO | "seguro" y "no alucina" no se pueden decir (superstición medida por alias de código, 2/20 [V bundle/CLAUDE.md:215-217]) |
| **Costo de cómputo por decisión** | un paso local cuesta O(sinapsis), igual que backprop por ejemplo [V FABLE:43]; la ventaja es no necesitar ciclo de entrenamiento ni GPU en uso | no es "más rápido por paso" |
| **Especialización barata** | dominio estrecho donde la línea de base a mano falle | en dominio estrecho y simple, la línea de base a mano o un árbol casi siempre ganan [I] |
| **Método con errores registrados** | transferible a cualquier laboratorio | se debe demostrar con la validación externa de la sección 5 |
| Lugar y causa (Latinoamérica, español, modelos locales) | real, pero es un argumento de contexto, no científico | no sustituye resultados |

Honestidad extra: ningún dato actual apoya "los LLM mejoran con esto". Lo defendible hoy es una pregunta bien formulada con tres desenlaces posibles y todos publicables como informe.

## 5. El método, y qué se añade para que sirva de validación externa

**Se hereda de JUACO sin cambios:** preregistro commiteado antes de los datos; arnés de identidad (promotor 0 ⇒ bit a bit el anterior [V escalera/ESCALERA.md:27-28]); humo de un proceso; auditor de solo lectura antes y después de cada serie; serie 1–20 + réplica 21–40 con semillas nuevas; registro de errores propio (**ERR-A001…**, para no mezclar con los ERR de JUACO); veredicto de una línea (FUNCIONA / NO / MODESTO).

**Se añade (Alejo como validación externa del método):**
1. **Errores sembrados a ciegas.** Una persona o agente ajeno al ciclo introduce N errores conocidos en preregistros, scripts y resúmenes (umbral cambiado tras ver datos, semilla repetida, control mal etiquetado, suma mal hecha en el informe). La clave queda sellada (hash) fuera del alcance del equipo.
2. **Tasa de detección con denominador.** Se informa detectados / sembrados, por tipo, **y** falsos positivos / revisiones; con intervalo de confianza. Con N pequeño se dice N.
3. **Brazo sin protocolo.** El hueco que señala ENTREGA 3: "no hay brazo sin protocolo; sólo 49 se atraparon antes de la serie; la clasificación la hizo un agente" [V ENTREGA_3:20]. Un mismo conjunto de errores sembrados se revisa (a) con auditor + preregistro + arnés y (b) con una revisión simple de un agente sin plantillas. Medida: detección y tiempo.
4. **Tareas con respuesta conocida.** Cada tarea de Alejo tiene solución analítica o línea de base exacta (suma mod 7, bandido con probabilidades conocidas): el auditor puede comprobar la respuesta correcta sin confiar en el informe.
5. **Auditor distinto del creador** y, cuando se pueda, un humano (el director o un tercero de la UIS) que reproduzca en otra máquina una serie completa.
6. **Honestidad sobre la independencia:** el auditor es un agente del mismo modelo; decir "auditor de solo lectura", no "auditoría independiente" [V ENTREGA_3:29].

## 6. Hoja de ruta en tres etapas

| Etapa | Qué | Cuánto | Justifica pasar a la siguiente |
|---|---|---|---|
| **1. PC actual (sin GPU)** | Paso 0, A1, B1, y mini-validación externa con 10 errores sembrados | 2–4 semanas de tardes | al menos uno de A1/B1 con la célula ≥ mejor línea de base a mano en una medida **y** réplica ×2; o los dos NO limpios (también vale: informe de 2 páginas) |
| **2. PC nuevo** | Series con 20+ semillas, tareas del tamaño de un adaptador (miles de parámetros), comparación con LoRA y kNN; empezar el brazo sin protocolo | 1–2 meses | célula ≥ kNN/LoRA en acierto con retención ≥ 0.95, **o** igual con ≥ 5× menos operaciones; tasa de detección de errores sembrados ≥ la del brazo sin protocolo |
| **3. Laboratorio de GPU de la UIS** | A2 (LLM congelado 1–8B), B2 (población de redes en GPU), reproducción por terceros | un semestre | publicación de informe registrado; sólo ahí tiene sentido contactar a un laboratorio (Discovery Loop: **decisión del director, no se contacta**) |

Sobre la UIS: SC3UIS existe y presta cómputo a investigadores internos y socios externos; su plataforma GUANE-1 está basada en GPU (más de 60 Tflops) [F https://www.xataka.com.co/otros-dispositivos/la-supercomputadora-mas-rapida-de-colombia-se-encuentra-en-santander]. La fuente es una nota de prensa de años atrás; **el hardware y las condiciones de acceso actuales no están verificados**: pedir por escrito antes de planear la etapa 3. Plan B sin permisos: GPU gratuita de servicios en la nube para experimentos chicos [M, comprobar cupo vigente].

## 7. Estructura de repositorio propuesta (repo propio: `alejo`, separado de JUACO y de alefast)

```
alejo/
  README.md              qué es, qué NO afirma, estado en una tabla
  CLAUDE.md              misión, reglas, ERR-A siguiente libre
  protocolo/             preregistro_PLANTILLA.md, ARNES.md, checklist del auditor
  tareas/                suma7/, decision_bandido/, hechos_cambiantes/  (cada una con solución exacta y test)
  celula/                celula.py (sin gradiente, sin importar torch), compuertas/, identidad_*.py
  techos/                mlp_adam.py, lora_ultima_capa.py  (única carpeta con gradiente)
  bases/                 diccionario.py, knn.py, q_tabular.py, ventana_ucb.py
  experimentos/A1/ B1/   PREREGISTRO.md, corre.py, humo_salida.txt, datos/, INFORME.md
  validacion_externa/    errores_sembrados/ (clave sellada por hash), detecciones.csv
  registro/              ERR_A.md, REGISTRO.md, ESTADO.md (una página)
  publicar/              CITATION.cff, .zenodo.json, vocabulario.md
```
Regla dura: `celula/` no puede importar librerías de gradiente (lo verifica una prueba automática). Datos y salidas crudas siempre commiteados; ninguna cifra en el informe sin su archivo.

## 8. Vocabulario para hablar en público

| No decir | Decir |
|---|---|
| "una IA propia / alternativa a los LLM" | "módulos pequeños de plasticidad local, evaluados contra líneas de base estándar" |
| "neuroplasticidad", "cerebro", "célula viva" | "regla de actualización local con olvido y compuerta de escritura" |
| "mejora/entrena a ChatGPT o Claude" | "módulo lateral que corrige un modelo congelado en uso; medido contra kNN y LoRA" (si A1 pasa) |
| "más seguro", "no alucina", "alineado" | "cada módulo se apaga y se mide contra un control de contenido equivocado" |
| "más rápido/barato que los grandes" | "menos operaciones por decisión en la tarea X, a igual acierto" (con el número) |
| "validación independiente" | "auditoría de solo lectura con errores sembrados a ciegas; tasa de detección d/N" |
| "aprende álgebra solo" | "con el prior correcto aprende la regla en pocas exposiciones; sin él, no" [V FABLE:76] |
| "IA de Latinoamérica" como argumento de calidad | solo como contexto: "desarrollado con recursos limitados en Colombia" |

Siempre añadir "qué no demuestra", como en `ENTREGA_3`.

## 9. Riesgos y lo no verificado

**Riesgos.** (1) kNN/caché estándar ya hace A; la célula puede no aportar [predicción central de A1]. (2) La línea de base a mano gana en B por ser problema de manual. (3) Reglas locales: el límite conocido es profundidad y reparto de crédito a varios pasos [V ESCALERA.md:232]. (4) El techo mal puesto produce conclusiones falsas (el humo de hoy ya lo sugiere). (5) Dispersión del director: Alejo no debe quitar días a la réplica de perillas ni a la publicación de JUACO (ALIFE 2027); **Alejo etapa 1 es de tardes, no de jornadas** [I]. (6) Sobrevender: lenguaje de la sección 8.

**No verificado.** Resultados de la réplica de perillas (en curso); el prototipo `red_celulas` no tiene informe y sus humos son de 4 semillas sin preregistro; acceso y hardware actual de SC3UIS; existencia de implementaciones públicas de Titans y las cifras de ROME/MEMIT/LoRA (de memoria); que 3 000 frases se procesen en minutos en tu CPU [I]; todas las predicciones numéricas de A1/B1 son mías y no están calibradas; los puntos de la sección 4 sobre qué ganaría una línea de base a mano son inferencia, no medición.
