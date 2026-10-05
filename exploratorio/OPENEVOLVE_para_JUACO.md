# OpenEvolve para JUACO (investigación de solo lectura, 5-oct-2026)

Marcas: [URL] = leído en la fuente; [M] = de memoria o estimación mía, sin verificar; [LOCAL] = archivo del repo JUACO.

## VEREDICTO: CON CONDICIONES (vale la pena un humo de una tarde; la serie real sólo con controles preregistrados)
Primer intento: ~1 tarde, 0 a 10 USD de modelo (clave gratuita de Gemini u OpenRouter), 1 a 3 h de CPU del PC para ~100 iteraciones con cascada. Una serie digna (300 iteraciones x 3 réplicas + 2 controles) costaría ~30 a 60 h de CPU (repartibles en Pool) y ~50 a 150 USD [M] con un modelo de gama media. La condición central: lo que se afirmaría es evolución de PROGRAMAS guiada por un LLM, no selección natural del organismo.

## 1. Qué es OpenEvolve
- Mantiene: la organización GitHub "algorithmicsuperintelligence" (repo codelion/openevolve). Licencia Apache 2.0. 7.5k estrellas, 1.2k forks, 835 commits, 61 issues abiertos [https://github.com/codelion/openevolve].
- Es una implementación de código abierto de AlphaEvolve de DeepMind (anunciado 14-may-2025) [https://deepmind.google/discover/blog/alphaevolve-a-gemini-powered-coding-agent-for-designing-advanced-algorithms/].
- Bucle: programa inicial con bloques marcados EVOLVE-BLOCK, evaluador que devuelve métricas, base de programas MAP-Elites con islas (migración en anillo) y evaluación en cascada (etapas `evaluate_stage1`, `evaluate_stage2`...) que descarta temprano a los malos [README https://raw.githubusercontent.com/codelion/openevolve/main/README.md]. En cada iteración se muestrea un padre y programas "inspiradores" (top + diversos), se le pide al LLM un cambio (por defecto en formato diff), se evalúa y se archiva.
- Modelos: API de OpenAI y cualquiera compatible (Gemini por su endpoint OpenAI, OpenRouter), modelos locales con Ollama o vLLM, y "Claude Code CLI" sin clave (tras `claude login`, `provider: "claude_code"`, modelo "sonnet"), también Copilot CLI [https://github.com/codelion/openevolve; README]. Claude por la API de Anthropic directa no aparece como opción nativa: se usaría el CLI o un puente compatible con OpenAI (OpenRouter) [M].
- Configuración (YAML). Valores por defecto leídos [https://raw.githubusercontent.com/codelion/openevolve/main/configs/default_config.yaml]: max_iterations 100; diff_based_evolution true; random_seed 42; 5 islas; population_size 1000; archive 100; feature_dimensions complexity y diversity; evaluador: timeout 300 s, parallel_evaluations 4, cascade_evaluation true, cascade_thresholds [0.5, 0.75, 0.9]; LLM: temperatura 0.7, 4096 tokens, timeout 60 s, 3 reintentos; max_code_length 10000.
- Versión: la página de releases muestra v0.4.0 (seguimiento de tokens, backend Copilot, EVOLVE-BLOCK opcional estricto) [https://github.com/codelion/openevolve/releases]; las fechas que devolvió la lectura (2024) no cuadran con AlphaEvolve (2025), así que NO confirmo la fecha. Repo muy activo. Instalación: `pip install openevolve` [README].
- Ojo: `random_seed` fija el muestreo de OpenEvolve, pero las respuestas del LLM no son reproducibles bit a bit (ver sección 4).

## 2. El laboratorio del taller (rramosp/openevolve-lab)
[https://github.com/rramosp/openevolve-lab y su README]
- Tres piezas: (1) regresión simbólica (fórmulas de crecimiento de poblaciones, materiales; datasets de LLM-SRBench en Hugging Face, ej. MatSci18, BPG8); (2) optimización de prompts para clasificar tickets de soporte (cinco ejercicios, con retroalimentación por "artifacts" y exploración Pareto); (3) un cuaderno para inspeccionar los resultados. Empieza con corridas de 10 iteraciones sobre minimización de una función.
- Modelo: cualquier endpoint compatible OpenAI: OpenRouter (nivel gratuito) o Gemini ("3.5-Flash" según la lectura); en YAML `primary_model`, `secondary_model`, `api_base`. Necesita h5py, scipy y cuenta de Hugging Face.
- Costo: el propio lab dice que OpenEvolve no registra tokens por defecto y trae un ejercicio para añadir ese registro. NO da cifra de costo ni tiempos. (Mi estimación en sección 3 es [M].)

## 3. Cómo se conectaría JUACO
### Lo que exige OpenEvolve
`evaluate(path) -> dict` de métricas (o `EvaluationResult(metrics, artifacts)`), con una métrica `combined_score` que guía la selección; las demás métricas sirven de dimensiones de diversidad; los `artifacts` (texto) se devuelven al LLM como retroalimentación, ideal para decirle "murió de hambre 83 % de las veces". Tiempo límite configurable (`evaluator.timeout`, 300 s por defecto: hay que subirlo). Cascada: `evaluate_stage1(path)`, `evaluate_stage2`, `evaluate_stage3`, cada una con umbral. [README]

### Lo que ya existe en JUACO [LOCAL]
- Interfaz del carro: un módulo `carros/<ID>.py` con `crea(ctx)` que devuelve un objeto con `actua(obs)`, `resultado`, `nace`, `muere`, `al_parir`, `quiere_parir`, `salida` (pista.py y docstring de FABRICA). O1.py son ~160 líneas.
- Llamada de una corrida: `pista.run(seed, [(etiqueta, modulo)]*9, T, pizarra=1, rep_acum=0, escala=1, mundo_n=None, fundador_limpio=1)`; `corre_v143.tarea((seed, ident, T))` hace exactamente eso (9 copias del carro, fundador limpio), y `juez.resumen_linaje` calcula R0, R0 real (nacimientos reales), fundadores tras t=10000, persistencia, causas de muerte. `juez.criterio_mono` da la regla de cruce del monocultivo.
- Tiempo: UNA evaluación = 1 semilla x 9 linajes x T=100000 = 130 a 180 s (dato del encargo). Referencia: serie v14.3 de 8 brazos x 20 semillas = ~15 h de CPU, o sea ~190 s por evaluación [INFORME_v143.md].
- Chequeo estático ya hecho: `revisa_carro.revisa_fuente(src)` rechaza texto/imports/llamadas prohibidas (getattr, eval, open, np.random, sys, gc, inspect, dunder, escritura de archivos), lista blanca de imports y exige `crea(ctx)` [revisa_carro.py]. El REGLAMENTO ERR-96 advierte que no hay sandbox y que el juez calcula todo de la física de la pista, no de lo que declara el carro.

### Envoltorio propuesto (evaluador.py, sin tocar pista ni juez)
1. Leer el programa candidato; correr `revisa_fuente`; si falla, puntaje 0 y artifact con la violación.
2. Cargar como módulo y lanzar `tarea` en un SUBPROCESO con tiempo límite duro (protege de bucles infinitos; OpenEvolve ya mata por timeout).
3. Puntaje: no usar el R0 solo. ERR-99/102 enseñan que premia morir o ser casi inmortal. `combined_score` = fracción de linajes que PERSISTEN (0 fundadores tras t=10000 y >=5 nacimientos reales, ENMIENDA 6), con R0 real como desempate y penalización por muertes voluntarias (el juez ya las mide físicamente).
4. Artifacts: causas de muerte, fundadores, fracción de pasos sin objeto bueno. (Cuidado: no incluir el mecanismo "limpiar"; ver contaminación.)

### Cascada concreta propuesta
| Etapa | T | Semillas | Tiempo estimado [M], suponiendo costo lineal en T | Umbral para pasar |
|---|---|---|---|---|
| 1 | 5 000 | 1 | ~7-10 s | pasa `revisa_carro`, no revienta, vida mediana >= la de la raíz |
| 2 | 25 000 | 1 | ~35-45 s | R0 real mediana >= 0.5 y vida no peor que la raíz |
| 3 | 100 000 | 2 | ~260-360 s | puntaje final |
Cuidado: a T corto los fundadores "después de t=10000" no se pueden juzgar (etapa 1 es sólo filtro de humo); y el costo no es necesariamente lineal en T (mide en el humo). Si el 70 % muere en etapa 1 y la mitad de lo restante en etapa 2, el costo medio por candidato es ~45 a 70 s.

### Presupuesto
- 300 iteraciones (un intento serio): ~4-6 h de CPU en total; con `parallel_evaluations` 4 a 6 en el PC, 1-2 h de pared. 1000 iteraciones: ~13-20 h de CPU, 3-5 h de pared con 4-6 procesos. [M]
- Llamadas al modelo: 1 por iteración (+ reintentos): 300 a 1000. Cada una con ~6-12k tokens de entrada (programa de 160 líneas + vecinos + retroalimentación) y ~1-3k de salida. Total 300 llamadas: ~3M entrada, ~0.6M salida. A precios de gama media tipo Sonnet ($3/$15 por millón [M, verificar]) son ~18 USD; con un modelo Flash de Gemini, 1 a 2 USD; con nivel gratuito, 0 pero con límites de ritmo. 1000 llamadas: x3.3.

### Punto de partida
1. **Recomendado: `CTRL_O1_SINLIMPIA`** (existe en carros/; difiere de O1 en una sola línea `limpia = False`, colapsa con vida 600 y mundo 78 % sin nada bueno). Pregunta limpia y preregistrable: "con selección y un LLM, ¿se reencuentra el paso de limpiar que hace cruzar a O1?". Distancia conocida a un cruzador. Hay que quitar del archivo los comentarios que explican la limpieza (contaminación).
2. **Pregunta de fondo: `V143`** (tronco actual, R0 real ~0.1, no cruza). Si el bucle cruza desde ahí, sí hay hallazgo.
3. Organismo mínimo desde cero: demasiado lejos para la primera prueba.
Nota honesta: O1 y FABRICA ven todos los objetos del anillo (ERR-97, opción A), por lo que las "reglas" del carro no son estrictamente locales. Dilo así cuando se informe.

## 4. Riesgos de método y controles
| Riesgo | Cómo se manifiesta aquí | Control propuesto |
|---|---|---|
| Sobreajuste a semillas de búsqueda | el programa memoriza rasgos de unas pocas semillas | semillas de búsqueda rotativas en un rango (p. ej. 14281-14290 práctica o uno nuevo), examen con semillas SELLADAS nunca vistas por el bucle ni por el modelo (rango nuevo; las 5001-5040 y 9001-9140 ya se vieron, no reutilizar) |
| El modelo "conoce" la respuesta | el LLM puede haber visto algoritmos de limpieza/quimiotaxis; el prompt o los comentarios pueden delatar la solución | prompt del sistema neutro (sin O1, sin "limpiar"), comentarios borrados, nombres de variables neutros; registrar prompts; control con un modelo más débil |
| Trampa con el simulador | leer estado global, azar propio, escribir archivos | `revisa_carro` obligatorio + subproceso + juez que calcula de la física (ERR-96); auditor revisa cada programa aceptado como mejor; ojo: `revisa_carro` prohíbe `np.random` pero un LLM puede buscar rodeos (hash, tiempo): ampliar lista y auditar a mano |
| Métrica premia morir/inmortalidad | ERR-99, ERR-102 | puntaje por PERSISTENCIA y muertes voluntarias declaradas, preregistrado antes de arrancar |
| Reproducibilidad | el LLM no es determinista, cambian los modelos de la API | guardar cada programa y cada respuesta; reportar réplicas independientes (>= 3 con distinta semilla), nunca una sola corrida; fijar modelo y fecha |
| Costo | | tope duro de iteraciones y de llamadas, preregistrado; parar al llegar |
| Ganancia ilusoria (el máximo de muchos intentos) | | juzgar solo el mejor programa congelado en el examen sellado, con el criterio de ENMIENDA 5/6 (>= 15/20) |

Controles que deben FALLAR o quedar por debajo: (a) búsqueda al azar con el mismo presupuesto (mutaciones sintácticas sin LLM, o el LLM con la retroalimentación barajada); (b) el mismo bucle con un modelo más débil (Haiku o un modelo local de 7B); (c) la raíz sola (SINLIMPIA) y V143 solos en el examen; (d) O1 como techo humano/agente. Predicción firmada antes de correr, con probabilidad, como se hace en el REGLAMENTO.

## 5. Qué se podría afirmar y qué no
- Se podría decir: "un bucle de selección sobre un juez fijo, con un LLM proponiendo cambios de código, produjo (o no) un programa de organismo que cruza el criterio en semillas selladas, y los controles (azar, modelo débil) quedaron por debajo".
- No se podría decir: "evolución", "selección natural", "población", "el organismo aprendió" (vocabulario prohibido del REGLAMENTO). Aquí el LLM es el operador de mutación y su conocimiento previo hace de heurística: la selección es sobre programas, la mutación no es ciega. Si cruza, el mérito se reparte entre el LLM y el bucle, y sólo los controles permiten separarlos.
- Por qué interesa igual: respeta la regla del proyecto, el modelo es DISEÑADOR fuera del paso, nunca dentro del organismo (el programa evolucionado corre sin LLM). Convierte el hallazgo manual de O1 (escrito por un agente a mano en la carrera) en algo medible: ¿lo encuentra un proceso con presupuesto contado? Responde si el "muro" es de diseño (un proceso con LLM lo salta) o del mundo. Es compatible con la línea ya anotada "bloque junto a un LLM".

## 6. Trabajos parecidos
- AlphaEvolve (DeepMind, 14-may-2025): agente de código evolutivo con Gemini; mejoró planificación de centros de datos y multiplicación de matrices [https://deepmind.google/discover/blog/alphaevolve-a-gemini-powered-coding-agent-for-designing-advanced-algorithms/].
- FunSearch (DeepMind, Nature, dic-2023): LLM + evaluador automático, conjuntos "cap set" y empaquetado [https://deepmind.google/discover/blog/funsearch-making-new-discoveries-in-mathematical-sciences-using-large-language-models/].
- ShinkaEvolve (Sakana AI, arXiv 2509.19349): evolución de programas abierta y eficiente en muestras, Apache 2.0, acepta modelos locales y agentes tipo Claude/Codex por suscripción, selección de modelo con bandido UCB [https://github.com/SakanaAI/ShinkaEvolve].
- Otros que conozco de memoria [M], sin enlace verificado: Eureka (NVIDIA, recompensas escritas por LLM), LLM-SR / LLM-SRBench (regresión simbólica; el dataset que usa el lab), Voyager (biblioteca de habilidades), "Evolution through Large Models" (Lehman et al.).

## 7. Los talleristas (sólo información pública y profesional)
- Raúl Ramos-Pollán: la única fuente que encontré lo describe como profesor de análisis de datos a gran escala en la Universidad Industrial de Santander (Bucaramanga), PhD informática, Univ. de Oporto; antes director del centro de cómputo CETA-CIEMAT, ingeniero en el CERN y arquitecto en Sun Microsystems; líneas: GNSS, transporte inteligente, visión por computador; colaborador de Pildo Labs (Barcelona) [https://insidegnss.com/raul-ramos-pollan/]. Tu encargo lo ubica en la Universidad de Antioquia: NO pude confirmar esa afiliación (puede que la fuente esté desactualizada, o que sea un cambio reciente); verificar en el programa del evento. No encontré correo público; el canal más seguro es la organización del evento o su repositorio https://github.com/rramosp/openevolve-lab. No encontré publicaciones suyas específicas sobre agentes.
- Juan Rafael Martínez-Galarza: astrofísico de planta en el Center for Astrophysics | Harvard & Smithsonian, subjefe científico "end-to-end" de los sistemas de datos del Chandra X-ray Center; PhD Leiden 2012; ex científico de calibración del instrumento MIRI del JWST; participa en AstroAI (instituto del CfA para IA en astrofísica); enseñó optimización estocástica y aprendizaje automático en Harvard; su investigación: galaxias con formación estelar y aprendizaje automático para hallar transitorios (binarias de rayos X, destrucción por mareas) [https://www.cfa.harvard.edu/people/rafael-martinez-galarza]. Contacto: correo institucional en esa página (la lectura lo mostró oculto). No pude verificar publicaciones suyas sobre agentes de IA; en la búsqueda salió un artículo "AstroGenesis" (agentes multiagente en astrofísica) que NO puedo atribuirle.
- Qué les podría interesar [mi inferencia, M]: un proyecto con protocolo de preregistro, controles que deben fallar y registro de errores (~190) aplicado a investigación con agentes de IA; el caso "el agente escribió O1 a mano y ningún proceso lo reprodujo" como estudio de método sobre sesgos de agentes que investigan; AstroAI es afín al uso de ML para descubrimiento. Prudencia: no prometer resultados antes del humo.

## 8. Qué hace falta del director y plan de una tarde
Decisiones/recursos:
1. Aprobar un tope de gasto (sugiero 10 USD para el humo; 100 USD tope para la serie).
2. Una clave: lo más fácil, Google AI Studio (Gemini Flash, nivel gratuito con límites) u OpenRouter (modelos gratuitos). Alternativa sin clave: `provider: claude_code` con tu `claude login`; funciona con tu suscripción pero gasta cuota, es más lento (un proceso por llamada) y mezcla cuota con el trabajo diario [M]. Un modelo local con Ollama en un PC sin GPU declarada: un modelo de 7B en CPU es lento (unos pocos tokens por segundo [M]) y poco fiable para editar código; sirve sólo como control "modelo débil", no como proponedor principal.
3. Permiso del director para instalar OpenEvolve en un entorno virtual aparte, FUERA del repo JUACO (no se instaló nada en esta investigación). Python >= 3.10 [M].

Plan de una tarde (primer humo, ~4 h):
1. (30 min) Entorno aparte `C:\...\openevolve_humo\`, `pip install openevolve`, correr el ejemplo de minimización de función con 10 iteraciones y el modelo gratuito (confirma clave y conexión; es lo mismo que hace el lab).
2. (60 min) Un creador/auditor escribe `evaluador.py` (envoltorio de sección 3) y verifica: la raíz SINLIMPIA y O1 dan los puntajes ya conocidos (SINLIMPIA no persiste, O1 sí) y un carro tramposo de `test_tramposo.py` es rechazado. Esto es el "ancla de identidad" del proyecto.
3. (15 min) Preregistro de una página: pregunta, predicción con probabilidades, presupuesto, controles, semillas, criterio de parada.
4. (90 min) Humo: 30 iteraciones, 1 isla, cascada T 5k a 25k (sin la etapa de 100k), `parallel_evaluations` 4, con registro de tokens activado. Ver: costo real por iteración, % rechazado por `revisa_carro`, % que muere en etapa 1, tiempo real de la etapa 1, si alguna mutación supera a la raíz.
5. (30 min) Cronista escribe el veredicto: FUNCIONA / NO / HAY ALGO MODESTO, con costo medido y la decisión de si se justifica la serie con controles.
