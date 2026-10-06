# MODELOS GRANDES ABIERTOS (DeepSeek, Kimi, Qwen) vistos desde Alejo — ingeniería inversa de lo publicado (5-oct-2026)

Misión: llegar a la AGI por este camino (JUACO, organismo mínimo con reglas locales; proyecto hermano Alejo). Investigación de solo lectura: se abrieron fuentes por WebFetch/WebSearch; no se instaló ni descargó nada, no se corrió nada, no hubo git.
Marcas: [F url] = abierto hoy, la cifra viene de ahí · [M] = de memoria, sin confirmar hoy · [I] = inferencia mía · [NC] = no pude confirmar.
Aviso de método: WebFetch resume las páginas con un modelo pequeño; las cifras de arquitectura coinciden entre varias fuentes, pero las de rendimiento y las de blogs comerciales (resultados de búsqueda) son de segunda mano.

**VEREDICTO: HAY ALGO MODESTO, y es explorable.** Los modelos grandes abiertos se pueden copiar en *ideas de diseño* y tomar hechos en *pesos*, pero no reproducir; Alejo no compite con ellos: se sienta al lado de uno (el "cuerpo") y aporta lo que ninguno de ellos hace — aprender en uso, olvidar a propósito, validar antes de creer, auditar por pieza.

## Los tres hallazgos que más le sirven al director

1. **Lo caro de DeepSeek/Kimi no se copia, pero se regala: los pesos son abiertos (MIT o MIT modificada) y existen versiones chicas.** Entrenar V3 costó 2.788 millones de horas de GPU (≈ 5.6 millones de dólares sólo la corrida final, y eso excluye investigación previa) [F https://arxiv.org/html/2412.19437]; Kimi K2 usó 15.5 billones de palabras-trozo (tokens) [F https://arxiv.org/abs/2507.20534]. Nadie con un PC lo repite. Pero hay "cuerpos" que corren en un PC: p. ej. una versión destilada de R1 de 7 000 millones de parámetros pesa 4.7 GB en disco [F https://huggingface.co/unsloth/DeepSeek-R1-Distill-Qwen-7B-GGUF], y una mezcla de expertos de 30 000 M con 3 300 M activos pesa 18.6 GB cuantizada a 4 bits [F https://huggingface.co/unsloth/Qwen3-30B-A3B-GGUF]. El primer paso de Alejo es de costo cero en entrenamiento.
2. **La "mezcla de expertos" de los grandes es, en el fondo, el mismo dibujo que la colonia de células con compuerta — pero con una diferencia que es el hueco de Alejo.** En DeepSeek V3 hay 256 expertos "enrutados" + 1 compartido y se activan 8 por palabra [F https://arxiv.org/html/2412.19437]; Kimi K2 tiene 384 y activa 8 [F https://huggingface.co/moonshotai/Kimi-K2-Instruct]. Pero sus expertos se entrenan *todos juntos con gradiente antes de entregar el modelo* y luego quedan congelados; el enrutador no mira "qué falló", mira un puntaje aprendido. Una colonia donde los "expertos" nacen donde el modelo se equivocó, cobran si aciertan y mueren si sobran es exactamente lo que ellos no tienen. Pero ojo con la honestidad: nuestro informe de deriva (5-oct) dice que en datos continuos con ruido la célula NO le gana a un kNN o a un SGD simples; la ventaja medida sólo existe donde los hechos son puntos sin vecinos (hamburguesa, STAGGER).
3. **El truco central de R1 es una cuarentena a escala industrial: nada se premia si no se puede comprobar.** R1 usa recompensas por regla (¿la respuesta coincide? ¿pasa el test de código?) y *abstiene deliberadamente de usar un modelo-juez neuronal* porque se le hace trampa ("reward hacking") [F https://arxiv.org/html/2501.12948]. Kimi K2 filtra trayectorias de herramientas con un juez contra rúbricas y sólo conserva las que cumplen [F https://arxiv.org/html/2507.20534]. Eso es "no dar nada por cierto hasta comprobarlo" — la misma filosofía que la cuarentena de Alejo. La lección práctica: el juez de la cuarentena debe ser **verificable por regla** (aciertos repetidos, pruebas ejecutables), no otro modelo opinando.

---

## 0. Glosario con imágenes (primera vez; el lector no es de ML)

- **Parámetros**: las "perillas" internas del modelo; más perillas, más memoria y más costo. "671B" = 671 000 millones.
- **Token**: un trozo de palabra (más o menos 3/4 de palabra).
- **Transformador y atención**: cada palabra le pregunta a las anteriores "¿quién se parece a lo que busco?" y copia lo que esa guarda. Es una ficha de clave→valor que se escribe al instante (ya lo contó la hamburguesa).
- **Mezcla de expertos (MoE)**: en vez de una sola cocina enorme que cocina todo, un restaurante con 256 cocineros especializados y un "maître" (el enrutador) que a cada plato le manda sólo 8. Se tiene la sabiduría de 256 pero se paga el costo de 8. "Total vs activos" = cocineros contratados vs cocineros que trabajan en cada plato.
- **Atención eficiente (MLA, DSA, atención lineal)**: formas de que el modelo no tenga que releer *todo* el texto anterior palabra por palabra; es como resumir el cuaderno en una ficha pequeña (reduce el "caché" que se guarda en memoria durante la conversación).
- **Preentrenamiento**: leer billones de palabras para predecir la siguiente. **Ajuste (SFT)**: enseñarle a conversar con ejemplos buenos. **Alineación/RL**: dejarlo practicar y premiarlo cuando acierta.
- **Aprendizaje por refuerzo con recompensa verificable (GRPO)**: el modelo escribe varias soluciones al mismo problema, se premian las que aciertan comparadas con las otras del grupo (sin necesitar un segundo modelo evaluador).
- **Destilación**: el profesor grande escribe miles de ejemplos resueltos y el alumno chico aprende a imitarlos.
- **Cuantización**: guardar cada número con menos dígitos (de 16 bits a 4), como una foto comprimida: pesa 4× menos y pierde un poco de calidad.
- **LoRA**: en vez de reescribir el libro entero, se pega una hoja de correcciones pequeña encima. Barato y quitable.
- **RAG**: buscar en un archivo los párrafos relevantes y pegárselos al modelo antes de que conteste.

## 1. LA RECETA, pieza por pieza

### 1.1 Tabla comparada (todas las cifras con fuente)

| | DeepSeek-V3 (dic-2024) | DeepSeek-R1 (ene-2025) | Kimi K2 (jul-2025) | DeepSeek V4 (abr-2026) | Qwen3 / Qwen3.5 |
|---|---|---|---|---|---|
| Total / activos | 671B / 37B [F arxiv.org/abs/2412.19437] | = V3 (es V3 + RL) [F github.com/deepseek-ai/DeepSeek-R1] | 1T / 32B [F arxiv.org/abs/2507.20534] | Flash 284B/13B; Pro 1.6T (cifra de blog) [F HF DeepSeek-V4-Flash; Pro: NC primario, solo deepinfra.com/blog] | Qwen3: 0.6B a 235B, densos y MoE [F arxiv.org/abs/2505.09388]; Qwen3-30B-A3B: 30.5B/3.3B [F HF Qwen3-30B-A3B]; Qwen3.5-35B-A3B: 35B/3B [F HF Qwen3.5-35B-A3B] |
| Expertos | 256 enrutados + 1 compartido, 8 activos, 61 capas [F arxiv.org/html/2412.19437] | idem | 384 expertos, 8 activos, 61 capas (1 densa) [F HF Kimi-K2-Instruct] | NC | Qwen3-30B-A3B: 128 / 8; Qwen3.5-35B-A3B: 256 (8 enrutados + 1 compartido) [F HF] |
| Atención | MLA (compresión de claves/valores a 512 dims) [F arxiv html 2412.19437] | idem | MLA, 64 cabezas (V3 tenía 128; menos cabezas = más barato en contexto largo) [F arxiv html 2507.20534] | Híbrida: atención comprimida dispersa + muy comprimida; a 1M de contexto 27 % del cómputo por token de V3.2 [F HF V4-Flash] | Qwen3.5: 3 capas "Gated DeltaNet" (recurrentes, sin caché que crezca) por cada 1 de atención completa [F HF Qwen3.5-35B-A3B; Qwen3-Next vía búsqueda] |
| Contexto | 128K [M] | 128K [M] | 128K (K2) / 256K (K2.6) [F HF Kimi-K2-Instruct y K2.6] | 1M [F HF V4-Flash] | Qwen3.5: 262K nativo [F HF] |
| Datos | 14.8T tokens, más matemática/código y más idiomas [F arxiv html 2412.19437] | RL sobre V3 | 15.5T tokens: web, código, matemática, conocimiento; "reformulación" de textos para que rinda más [F arxiv html 2507.20534] | 32T+ tokens [F HF V4-Flash] | Qwen3: 119 idiomas y dialectos [F arxiv.org/abs/2505.09388]; Qwen3.5: 201 [F HF] |
| Precisión/optimizador | Entrenado en FP8 (números de 8 bits) con escalas por bloque [F arxiv html] | — | Optimizador Muon + "QK-Clip" (MuonClip) para que no explote la atención [F arxiv.org/abs/2507.20534] | Mezcla FP4+FP8; optimizador Muon [F HF V4-Flash] | NC |
| Truco extra | Balance de carga sin pérdida auxiliar; predicción de 2 tokens (MTP) [F arxiv html] | GRPO [F arxiv.org/abs/2402.03300] | Sparsidad 48 (384/8): menos FLOPs a igual pérdida [F arxiv html 2507.20534] | "Hyper-conexiones" (mHC) [F HF V4-Flash] | Modo "pensar"/"no pensar" en un solo modelo + presupuesto de pensamiento [F arxiv.org/abs/2505.09388] |
| Licencia | Código MIT; pesos con "Model Agreement License" que permite uso comercial [F github.com/deepseek-ai/DeepSeek-V3] | MIT; los destilados sobre Qwen heredan Apache 2.0, los de Llama su licencia [F github.com/deepseek-ai/DeepSeek-R1] | MIT modificada [F HF Kimi-K2-Instruct] (condiciones exactas: [M] pide atribución visible a empresas muy grandes; [NC] hoy) | MIT [F HF V4-Flash] | Apache 2.0 [F HF Qwen3-30B-A3B, Qwen3.5] |
| Pesos publicados | Sí, 685 GB (671B + 14B del módulo MTP), FP8 nativo [F github V3] | Sí, + 6 destilados 1.5B/7B/14B/32B (Qwen) y 8B/70B (Llama) [F github R1] | Sí, y variantes posteriores K2 Thinking (nov-2025) y K2.5/K2.6 [F HF K2.6; resto vía búsqueda] | Sí (Flash y Pro) [F HF V4-Flash; Pro vía búsqueda] | Sí |

Otros que enseñan algo distinto:
- **Kimi Linear** (oct-2025): 48B total / 3B activos; sustituye atención completa por "Kimi Delta Attention" (una memoria recurrente fija con compuerta fina) en capas mezcladas con MLA; reduce el caché hasta 75 % y acelera la decodificación hasta 6× a 1M de contexto; publicaron los pesos [F https://arxiv.org/abs/2510.26692]. **Importante para Alejo**: la atención lineal ES una memoria asociativa que se escribe sola con una regla local (delta) — prima directa de la célula. [I]
- **Engram (DeepSeek, ene-2026)**: una "tabla de memoria" de n-gramas con búsqueda O(1) inyectada en el transformador; reemplazar ≈20 % de los expertos por esa tabla mejora conocimiento y razonamiento [F resultados de búsqueda; paper arXiv 2601.07372, no abierto en detalle]. Es la admisión de los grandes de que "buscar" es mejor que "calcular" para hechos estáticos.
- **DeepSeek-V3.2** (dic-2025): atención dispersa (DSA), RL escalado y una "tubería de síntesis de tareas de agente" que genera datos de uso de herramientas [F https://arxiv.org/abs/2512.02556].

### 1.2 Entrenamiento por etapas (lo que se sabe y lo que no)

**V3**: preentrenamiento (14.8T tokens) → SFT → RL; en el posentrenamiento "destilan" capacidad de razonamiento largo desde un modelo de la serie R1 hacia V3 [F https://arxiv.org/html/2412.19437]. Posentrenamiento: 0.1M horas de GPU adicionales [F github V3].

**R1** [F https://arxiv.org/html/2501.12948]:
1. R1-Zero: RL directo sobre la base sin ejemplos humanos (el razonamiento, la auto-revisión y la verificación "emergen").
2. Para R1: arranque en frío con un puñado de ejemplos legibles → RL de razonamiento con recompensas por regla (exactitud + formato + consistencia de idioma) → muestreo por rechazo y SFT (~800 mil ejemplos) → segundo RL (1 700 pasos) con recompensas mixtas.
3. Falló: modelos de recompensa por paso (PRM) y búsqueda de árbol (MCTS) "no sirvieron a escala".
4. Destilar R1 en modelos chicos (Qwen/Llama) rinde más que hacerles RL directo a ellos (según el resumen del paper; el argumento fino: [NC] a nivel de cifras).

**Kimi K2** [F https://arxiv.org/html/2507.20534]: preentrenamiento con Muon; posentrenamiento con (a) SFT con datos sintéticos de agente y (b) RL conjunto con recompensas verificables (matemática, código con pruebas ejecutables sobre pull requests de GitHub, seguimiento de instrucciones con regla + juez, seguridad) y **autocrítica con rúbricas**: el propio K2 hace de crítico, y ese crítico se recalibra con las tiradas que sí tienen recompensa verificable.

**Cómo generó K2 los datos de herramientas** (esto es oro para el puente): más de 3 000 herramientas reales (servidores MCP de GitHub) + más de 20 000 sintéticas organizadas por dominios; personajes de usuario simulados por LLM dialogan con agentes; un "simulador de herramientas" (= un modelo del mundo) responde las llamadas con azar controlado (éxitos, fallos parciales); un juez con rúbricas se queda sólo con las trayectorias exitosas [F arxiv html 2507.20534].

### 1.3 Costo declarado y la discusión

- V3: 2.788M horas de H800; a 2 USD/hora = 5.576M USD, y el paper dice que **excluye** investigación previa y ablaciones [F https://arxiv.org/html/2412.19437]. Un análisis aparte estima unas 2 048 GPU durante ~2 meses [F https://www.theregister.com/2025/09/19/deepseek_cost_train/].
- R1: la versión de Nature (vol. 645, 2025) declara ≈294 000 USD, 80 horas en 512 H800 — pero sólo el RL, encima de la base V3 (≈5.9M USD en total según el mismo análisis) [F https://www.theregister.com/2025/09/19/deepseek_cost_train/ ; Nature: https://arxiv.org/abs/2501.12948 menciona Nature 645:633–638]. La propia DeepSeek admite que tiene A100 usadas en fases tempranas [F resultados de búsqueda, Scientific American / SCMP].
- Kimi K2: el paper **no declara** costo ni FLOPs totales [F https://arxiv.org/html/2507.20534].
- Lectura honesta [I]: "5.6 millones" es el costo marginal de una corrida con un equipo y un clúster que ya existían y con recetas ya afinadas. Para un PC sin GPU declarada el número relevante no es ese: es cero entrenamiento + descarga.

### 1.4 Cómo "razonan" y cómo usan herramientas

- Razonar = escribir una cadena de pensamiento larga antes de responder; con RL el modelo aprende a alargarla, revisarse y retroceder [F https://arxiv.org/html/2501.12948]. Qwen3 lo pone como un interruptor (pensar/no pensar) con presupuesto [F https://arxiv.org/abs/2505.09388]; Kimi K2 Thinking entrelaza pensamiento con llamadas a herramientas [F resultados de búsqueda].
- Agentes: K2.6 anuncia hasta 300 subagentes y 4 000 pasos coordinados ("enjambre") [F https://huggingface.co/moonshotai/Kimi-K2.6]. Es marketing de ficha de modelo, no de paper [I].

## 2. QUÉ SE PUEDE IMITAR Y QUÉ NO

### 2.1 Tabla pieza → alcance

| Pieza de la receta | Veredicto | Costo aproximado |
|---|---|---|
| Preentrenar un modelo de 600B+ (14–32T tokens) | **Inalcanzable** | millones de USD [F arxiv html V3] |
| Preentrenar uno chico desde cero (≈100M–1B, pocos B de tokens) | Se puede hacer en chico, pero **no sirve** como cuerpo: perderá contra cualquiera de los abiertos | semanas de laboratorio de GPU [M] |
| Pesos de V3/R1/K2/V4/Qwen | **Se toma hecho** | gratis (descarga; tamaños en 2.2) |
| Modelos destilados de R1 (1.5B–32B) y Qwen3/3.5 chicos | **Se toma hecho** | gratis; 3–20 GB |
| Mezcla de expertos con 256–384 expertos entrenados a mano | Inalcanzable | — |
| Mezcla de expertos **de juguete** (4–16 expertos sobre un modelo chico: "upcycling" o Branch-Train-MiX) | **Se puede hacer en chico** (laboratorio con GPU) | días de una GPU [M]; método: [F https://arxiv.org/abs/2212.05055, https://arxiv.org/abs/2403.07816] |
| Atención eficiente (MLA/DSA/lineal) | Se toma hecho (viene en los pesos); reproducirla no aporta | — |
| Entrenamiento en FP8/FP4, Muon | Inalcanzable/irrelevante para un cuerpo ajeno; Muon sí se puede probar en chico [I] | — |
| Cuantización a 4 bits | **Se toma hecho** (archivos GGUF de la comunidad) | gratis |
| RL con recompensa verificable (GRPO) sobre un modelo chico | **Se puede hacer en chico** en tareas con juez automático (aritmética, código con tests, el juez propio de JUACO); no en abierto/general | GPU de laboratorio; días [M] |
| Destilación desde un profesor | **Se puede hacer en chico** (SFT sobre trazas del profesor) | barato si el profesor corre local; con API de pago: dólares por millones de tokens [NC precios] |
| Datos sintéticos de uso de herramientas (receta K2) | **Se puede hacer en chico** (cientos de herramientas, un simulador, un juez por regla) | CPU + un modelo local; días de máquina |
| LoRA | **Se puede hacer en chico** en CPU para modelos ≤1–3B (lento) o en GPU del laboratorio | horas–días [M] |
| Caché de contexto / memoria de conversación | Se toma hecho (llama.cpp/vLLM) | gratis |

### 2.2 Versiones que corren en un PC (lo confirmado hoy y lo que no)

| Modelo | Disco (Q4_K_M salvo nota) | Quién lo da | Memoria/velocidad en CPU | Español |
|---|---|---|---|---|
| DeepSeek-R1-Distill-Qwen-7B | 4.68 GB (Q8: 8.1; F16: 15.2) [F https://huggingface.co/unsloth/DeepSeek-R1-Distill-Qwen-7B-GGUF] | MIT/Apache | ≈ tamaño del archivo + caché; velocidad NC (típico 3–8 tokens/s en CPU moderna [M]) | razona sobre todo en inglés/chino; consistencia de idioma por recompensa [F arxiv html R1]; cifra en español [NC] |
| Qwen3-30B-A3B (MoE, 3.3B activos) | 18.6 GB (Q2_K 11.3; Q8 32.5) [F https://huggingface.co/unsloth/Qwen3-30B-A3B-GGUF] | Apache 2.0 | Corre en CPU con 32 GB de RAM; al activar sólo 3B por token va mucho más rápido que un denso de 30B [I; ventaja estructural de MoE] | 119 idiomas declarados [F arxiv.org/abs/2505.09388]; calidad en español medida [NC] |
| Qwen3.5-35B-A3B | tamaño de archivo [NC hoy]; ≈ el de arriba [I] | Apache 2.0 | híbrido GDN: caché que no crece con el contexto [F HF] | 201 idiomas declarados [F HF] |
| Qwen3.5 pequeños (0.8B–9B) | NC en tamaños exactos | Apache 2.0 | caben en PC modesto [F resultados de búsqueda trilogyai/mlabonne] | idem |
| DeepSeek-V4-Flash (284B/13B) | MoE enorme, FP4+FP8; cuantizaciones llama.cpp/Ollama existen [F HF V4-Flash]; tamaño NC (≥ ~100 GB estimado [I]) | MIT | Laboratorio, no PC | NC |
| Kimi K2 (1T) | 1.8 bits: 247 GB en disco; 2 bits: 381 GB [F https://unsloth.ai/docs/models/tutorials/kimi-k2-thinking-how-to-run-locally] | Mod. MIT | "5+ tokens/s con ≥247 GB de memoria unificada; ~1–2 tok/s con GPU 24 GB + 256 GB RAM; <1 tok/s con disco" [F misma] | NC |

**Cómo se ejecutan** (sin instalar tú): llama.cpp (formato GGUF, descarga de unsloth/bartowski en Hugging Face), Ollama y LM Studio son lo habitual; MLX en Mac; vLLM/SGLang en servidores con GPU. Las fichas de modelo de Qwen3 y de V4-Flash los nombran [F HF Qwen3-30B-A3B, HF V4-Flash]. Para MoE grandes, llama.cpp permite dejar los expertos en RAM de CPU y lo demás en GPU con el parámetro `-ot` [F unsloth.ai doc].

**Lectura para el director** [I]: el modelo "cuerpo" realista de Alejo hoy es entre 4 y 20 GB. Para el paso 1 (sin GPU) hace falta además poder **leer los estados internos** del modelo (la clave de la célula); eso se hace con transformers/llama.cpp en modo de extracción de "embeddings"/capas ocultas — verificar en el paso 0 que la herramienta elegida los expone.

## 3. EL PUENTE

Para cada idea de los grandes: su pariente en lo que ya tenemos y cómo se combinan. Referencias a nuestras mediciones: hamburguesa 1-oct (memoria viva sobre pan congelado: 1.00 con una sola exposición vs 0.32 del congelado y del gradiente en línea; generaliza a paráfrasis 0.97; NO le gana al RAG con memoria sobrada), decisión 5-oct (FUNCIONA en mundo cuyas reglas cambian, 10/10 semillas, pero con cambio regional empata con sus controles), deriva 5-oct (NO como método de ML general: no gana a kNN/SGD en datos continuos con ruido).

**(a) Mezcla de expertos ↔ colonia con compuerta.**
- Parecido real: ambos son "varios especialistas, y a cada entrada sólo se activan unos pocos"; la compuerta (umbral de parecido) de la célula es un enrutador "top-1 por distancia". DeepSeekMoE añade un experto *compartido* para el conocimiento común y expertos más finos y numerosos [F https://arxiv.org/abs/2401.06066]; la analogía: el pan del cuerpo = experto compartido; las células = expertos enrutados finos.
- Diferencias que importan: (1) en MoE los expertos son *capas completas de la red* entrenadas con gradiente; nuestra célula es una *ficha* (prototipo+valor+energía). (2) El enrutador de MoE aprende "qué cocinero sirve"; el nuestro aprende por cobro "qué ficha acertó donde el modelo fallaba". (3) Ellos balancean la carga con un sesgo para que todos los expertos se usen [F arxiv html V3]; nosotros queremos lo contrario: que mueran los que no se usan (olvido por escasez).
- ¿Puede la colonia ser "expertos que nacen y mueren, enrutados por el estado interno del modelo"? **Sí, en forma de memoria, no de capa** (eso es lo que hizo la hamburguesa: la clave es el estado interno). Un puente más literal existe en la literatura: WISE separa una "memoria lateral" de ediciones con un enrutador que decide si una consulta va a la memoria principal o a la lateral [F https://arxiv.org/abs/2405.14768], y GRACE guarda ediciones como un cuaderno de pares clave→valor en el espacio latente con radio de acción [F https://arxiv.org/abs/2211.11031] — el radio de GRACE es nuestra compuerta y tiene el mismo problema (nuestra decisión: "el radio está puesto a mano y las células generalizan de más").
- Camino de más largo plazo [I]: las células validadas en el sueño podrían "graduarse" a un experto real vía *upcycling*: copiar el feed-forward del modelo como experto y entrenar sólo el nuevo con las correcciones [F https://arxiv.org/abs/2212.05055, https://arxiv.org/abs/2403.07816]. Eso es laboratorio de GPU, no PC.

**(b) Destilación ↔ el sueño y la fábrica de programas.**
- Destilación = el profesor escribe, el alumno imita. El sueño = el modelo absorbe con gradiente lo que las células validadas corrigieron. Son lo mismo con *otro profesor*: ellos usan un modelo grande; nosotros usaríamos la experiencia de uso ya validada.
- Mezclas posibles: (i) profesor grande opcional (un abierto fuerte, local o por API) escribe ejemplos que entran a la cuarentena como una fuente más de hipótesis; (ii) la fábrica de programas (OpenEvolve + juez) usa un LLM como *generador* y el juez propio como *selector*, igual que R1 usa recompensa por regla como selector.
- Aviso: nuestro sueño costó 33× y dejó el modelo "olvidando lo que no cambió" (0.87, rango 0.00–1.00) [INFORME_DECISION]. La destilación industrial evita eso mezclando datos viejos y nuevos (R1 mezcla ~800 mil ejemplos de razonamiento y no razonamiento [F arxiv html R1]); el sueño debería reproducir esa mezcla ("ensayo de lo viejo").

**(c) Razonar y verificarse (R1) ↔ la cuarentena.**
- R1 sólo premia lo que una regla comprueba y evitó los jueces neuronales por trampa [F arxiv html R1]; la cuarentena promueve una hipótesis sólo con confirmaciones independientes. Misma filosofía; la cuarentena es "RL de un paso" aplicado a la memoria en vez de a los pesos.
- Lo que R1 nos regala: (1) el motivo por el cual el juez debe ser verificable; (2) que los procesos por paso (PRM) no funcionaron a escala [F arxiv html R1] → no construir una cuarentena que puntúe pasos intermedios con un modelo; contar aciertos finales; (3) las muestras por grupo (GRPO): varias respuestas al mismo caso y se compara con el grupo — la cuarentena puede usar la misma idea para elegir cuál de varias hipótesis candidatas se confirma.
- Lo que nosotros añadimos y R1 no tiene: la verificación ocurre **en uso, sobre el mundo real del usuario**, por pieza (auditable), no sobre un banco de problemas fijo antes de publicar.

**(d) Datos sintéticos de herramientas (K2) ↔ generar "maestros" para la colonia.**
- K2: repositorio de herramientas + usuarios simulados + simulador de mundo + juez con rúbrica [F arxiv html 2507.20534]. Equivalente nuestro: los mundos de juguete de JUACO (decisión, hamburguesa, STAGGER) son simuladores de mundo; el juez propio es el filtro; un modelo grande local puede escribir "maestros" (situaciones, cambios de regla, preguntas) que se corren contra la colonia para entrenarla *antes* de que el usuario real llegue (arranque en frío).
- Cuidado [I]: K2 usó 20 000 herramientas sintéticas + 3 000 reales; con pocas herramientas el riesgo es que la colonia aprenda al simulador, no al mundo. Control: cruzar simulador distinto del de entrenamiento.

**(e) Memoria / caché de contexto ↔ memoria viva.**
- El "caché" (KV) de los grandes es la memoria de la conversación, y es lo que MLA, DSA y Kimi Delta Attention intentan achicar [F HF V4-Flash; arxiv.org/abs/2510.26692]. Muere al terminar la conversación. Nuestra memoria viva es persistente, compuerta de escritura por error, olvido por escasez — es la pieza que *ningún* modelo de los listados trae de fábrica.
- Engram de DeepSeek (tabla de n-gramas) y las memory layers de Meta [F https://arxiv.org/abs/2412.09764 vía ALEJO.md] muestran que los propios laboratorios están agregando memoria *estática* por búsqueda; la nuestra es dinámica y se valida. Puente barato: usar la tabla como "rival estándar" y como competidor honesto.

**(f) LoRA ↔ consolidar lo validado.**
- LoRA = hoja de correcciones pequeña. El sueño es en la práctica un LoRA pequeño entrenado sólo con lo que pasó la cuarentena [I]. Ventaja: LoRA es quitable (se puede auditar y revertir), que es el requisito de "auditar por pieza". Rival obligado: el LoRA entrenado con *todo* sin cuarentena. Si el LoRA con cuarentena no gana a ese, la cuarentena no vale.

### Dónde aportamos algo que ellos NO tienen
1. **Aprender en uso**: los pesos de los grandes quedan congelados al publicar; nosotros medimos corrección tras una sola exposición (hamburguesa 1.00 vs 0.32).
2. **Olvidar a propósito**: el MoE nunca borra expertos; el caché de contexto olvida *todo*; nuestras células sueltan lo que dejó de servir y recuperan tras un cambio de regla en 18 pasos contra 127 del gradiente (decisión).
3. **Validar antes de creer**: R1 lo hace *antes de publicar*; la cuarentena lo haría *después*, en vivo.
4. **Auditar por pieza**: cada célula tiene dueño, historia y saldo; en un experto de MoE no se puede explicar por qué un valor está ahí.

### Dónde ellos nos llevan una ventaja que NO se cierra
1. **Capacidad general** (lenguaje, razonamiento, código): inalcanzable en pesos; sólo se toma prestada.
2. **Generalizar en lo continuo y con ruido**: nuestra deriva NO ganó a kNN/SGD; no hay que vender la célula como "método de ML".
3. **Escala de datos y de recompensa verificable**: R1 premió millones de soluciones; nuestra cuarentena verá cientos de confirmaciones por uso.
4. **Calidad en español**: depende del cuerpo elegido [NC medido].
5. **Lo que no cambia**: contra memoria sobrada, el RAG estándar nos empata o gana (hamburguesa 0/8) — la memoria viva paga cuando la memoria es chica o cuando hay que generalizar por parecido de estado interno.

## 4. EL DISEÑO DE ALEJO (en texto)

```
USUARIO / MUNDO
   │ entrada
   ▼
[1 CUERPO]  modelo abierto congelado (SE TOMA HECHO)  ← pesos: Qwen3/3.5 chico o R1-Distill (cuantizado, llama.cpp)
   │ estado interno (capa oculta elegida) = LA CLAVE
   ├───────────────► [2 COLONIA] células: clave → corrección
   │                     compuerta (¿se parece?) → pisa la salida del cuerpo (SE CONSTRUYE: ya existe en numpy)
   │                     cobra si aciertan donde el cuerpo falló; paga por existir; mueren por escasez
   │                       ▲
   │                       │ promoción sólo si pasa
   │               [3 CUARENTENA] hipótesis nuevas (de uso real, de un profesor, de la fábrica)
   │                     validación por regla, confirmaciones independientes   (SE CONSTRUYE: en construcción)
   │                       ▲                                   │ validadas
   │                       │                                   ▼
   │               [5 FÁBRICA] LLM abierto local propone programas/reglas;  [4 SUEÑO] cada N pasos
   │                 juez propio los selecciona (OpenEvolve +       el cuerpo absorbe con gradiente (LoRA)
   │                 juez: SE TOMA OpenEvolve; el juez SE CONSTRUYE)  lo validado, mezclado con "ensayo de lo viejo";
   │                                                                  las células absorbidas se liberan
   ▼
SALIDA = cuerpo + corrección de la colonia, con registro de qué célula respondió
   │
   └► [6 AUDITORÍA] por pieza: saldo, edad, origen, aciertos (SE CONSTRUYE; es lo ya hecho en JUACO)
```
Qué se toma hecho: el cuerpo (pesos abiertos), llama.cpp/transformers para correrlo, cuantización GGUF, OpenEvolve, LoRA (librerías estándar), RAG/kNN como rivales. Qué se construye: la colonia, la cuarentena, el juez, el sueño con ensayo de lo viejo, la auditoría.

### Tres pasos de construcción

**PASO 1 — el más barato: colonia sobre un cuerpo chico, sin GPU.**
- Qué: repetir la hamburguesa (memoria viva sobre estados internos) pero con un modelo abierto real en vez del transformador de juguete, en una tarea de "hechos que cambian": preguntas con respuestas que se corrigen una vez y se preguntan después y en paráfrasis (en español).
- Modelo concreto: **Qwen3 pequeño (p. ej. 0.6B–4B, Apache 2.0)** o **DeepSeek-R1-Distill-Qwen-1.5B/7B** (7B Q4_K_M = 4.68 GB [F HF unsloth]); [NC] el tamaño exacto de los Qwen3 chicos: verificarlo en su ficha antes.
- Descargar: los pesos del modelo elegido (Hugging Face; fuente Qwen/ o deepseek-ai/; en GGUF unsloth/ o bartowski/), 2–5 GB. Sin instalar nada más que lo que ya haya en el proyecto; el paso 0 es verificar que el modelo se pueda leer por dentro (estado oculto).
- Equipo: el PC actual, CPU; unas horas de máquina.
- Cómo se mide: contra (i) el cuerpo congelado, (ii) RAG por embeddings con memoria sobrada y con memoria chica, (iii) kNN-LM sobre el mismo estado oculto [F https://arxiv.org/abs/1911.00172], (iv) LoRA/ajuste de última capa en línea; controles: pago barajado, sin compuerta. Medidas: exposición única, paráfrasis, retención de lo no cambiado, costo por consulta.
- Seguir si: gana a (i) y (iv) con memoria chica y empata o supera a (ii)/(iii) con memoria chica y en paráfrasis ≥0.8 sin romper lo intacto (>0.9). Abandonar (como colonia sobre LLM real) si no supera a kNN sobre el mismo estado oculto: entonces la célula es un kNN con más pasos y se dice así.

**PASO 2 — intermedio: cuarentena + sueño con ensayo, aún en CPU o una GPU modesta.**
- Qué: añadir la cuarentena (la hipótesis entra a una sala; sólo pasa tras k confirmaciones independientes por regla) y el sueño como LoRA pequeño con mezcla de lo viejo; inyectar hipótesis *falsas* a propósito (un "profesor mentiroso") para probar que la cuarentena las frena (cf. envenenamiento de memoria de agentes, ver 6).
- Modelo: el mismo del paso 1 + opcionalmente **Qwen3-30B-A3B** (18.6 GB Q4_K_M [F HF unsloth]) como "profesor" local que genera hipótesis/paráfrasis, que corre en un PC de 32 GB de RAM [I].
- Descargar: Qwen3-30B-A3B-GGUF (18.6 GB, Q4_K_M, huggingface.co/unsloth/Qwen3-30B-A3B-GGUF [F]).
- Equipo: PC con ≥32 GB RAM; para el LoRA, la GPU del laboratorio es lo cómodo, pero un LoRA sobre 0.6B–1.5B en CPU es posible (lento) [M].
- Se mide contra: (i) escribir en memoria sin cuarentena, (ii) un LoRA entrenado con todo lo visto sin validar, (iii) RAG con filtro por frecuencia. Medidas: fracción de hipótesis falsas que se cuelan, hechos verdaderos que tardan en entrar, retención tras el sueño.
- Seguir si: la cuarentena deja pasar <5 % de las falsas y retrasa menos del doble los verdaderos, y el LoRA con cuarentena supera al LoRA sin ella en retención. Abandonar si la cuarentena no mejora sobre el filtro por frecuencia de RAG.

**PASO 3 — el más ambicioso: colonia → expertos reales + fábrica, en el laboratorio de GPU.**
- Qué: (a) fábrica con OpenEvolve: un modelo abierto proponiendo programas/reglas de compuerta y el juez propio seleccionando (aquí el radio de la compuerta, que hoy está puesto a mano, es el primer candidato a que lo evolucione la fábrica); (b) "graduar" células validadas a un experto con upcycling de un modelo MoE chico; (c) RL con recompensa verificable (GRPO) sólo para tareas con juez automático.
- Modelo: Qwen3-30B-A3B o Qwen3.5-35B-A3B (Apache 2.0, MoE de ~3B activos) como cuerpo ya MoE; **no** V4/K2 (inalcanzables en tamaño).
- Descargar: pesos completos (≈60–70 GB en 16 bits [I, 30.5B×2 bytes]) desde Hugging Face.
- Equipo: laboratorio universitario con GPU (cantidad/memoria: [NC], preguntar a la universidad).
- Se mide contra: LoRA estándar, RAG, y un MoE-upcycling sin colonia. Criterio de seguir: que lo validado y graduado mejore sobre el LoRA en tareas con cambio de regla sin bajar lo viejo; abandonar si la graduación no supera al LoRA (entonces la colonia queda como memoria externa, que ya es un resultado).

## 5. QUÉ NO DECIR EN PÚBLICO Y QUÉ SÍ

No decir: "nuestro propio DeepSeek/Kimi", "un modelo como los grandes", "ingeniería inversa de DeepSeek" (sólo se leyeron papers y fichas; nadie vio sus datos ni su código de entrenamiento), "el costo de DeepSeek fue 6 millones" sin las exclusiones, "la célula supera al RAG/gradiente" (en memoria sobrada no), "método de ML para deriva" (la deriva dio NO), "aprende sin olvidar" (el olvido local no está resuelto; olvida a propósito y controlado), "validamos todo" (la cuarentena está en construcción).

Sí decir: "Alejo es un sistema que se monta sobre un modelo abierto ya existente (de pesos públicos con licencia permisiva) y le añade una memoria viva que aprende mientras se usa, olvida lo que ya no sirve y no da nada por cierto hasta comprobarlo; cada pieza se puede auditar." "Tomamos las ideas publicadas de los modelos abiertos (mezcla de expertos, destilación, verificación por regla) y probamos en pequeño si una versión local y auditable de esas ideas sirve." "En juguetes medidos con rivales estándar: ganó en cambios de regla y exposición única, empató o perdió en memoria sobrada y en datos con ruido." Las cifras de los grandes se citan con fuente.

## 6. LO QUE YA EXISTE MUY PARECIDO ("modelo congelado + memoria que aprende en uso con validación")

- **kNN-LM** (Khandelwal et al., 2019): interpola el modelo con vecinos más cercanos sobre sus propios estados internos, sin reentrenar; es el rival más directo de la célula — la misma clave [F https://arxiv.org/abs/1911.00172].
- **GRACE** (2022): ediciones como cuaderno clave→valor en el espacio latente con radio de acción, miles de correcciones secuenciales sin tocar pesos [F https://arxiv.org/abs/2211.11031]. Es *la* pieza más parecida a la colonia (con "radio" = compuerta); le falta: pago por acierto, muerte, validación.
- **WISE** (2024): memoria lateral para ediciones y un enrutador decide entre memoria principal y lateral; fragmenta ediciones en subespacios y las fusiona [F https://arxiv.org/abs/2405.14768].
- **ROME / MEMIT** (2022): editan pesos directamente (MEMIT: miles de asociaciones en GPT-J y GPT-NeoX) [F https://arxiv.org/abs/2210.07229; ROME: [M] arXiv 2202.05262]. Son edición de pesos, sin cuarentena; conocidos por degradar a muchas ediciones [M].
- **Titans** (Google, 2025): módulo de memoria que aprende al momento de la prueba guiado por "sorpresa" [F https://arxiv.org/abs/2501.00663 vía ALEJO.md]. Hermano conceptual; aprende con gradiente interno, sin cuarentena.
- **Memory layers a escala** (Meta, 2024): capas de memoria entrenables que añaden parámetros sin añadir cómputo [F https://arxiv.org/abs/2412.09764 vía ALEJO.md].
- **Engram** (DeepSeek, 2026): memoria estática de n-gramas por búsqueda O(1) dentro del modelo [F resultado de búsqueda; paper arXiv 2601.07372, no abierto en detalle].
- **MemGPT** (2023): gestiona memoria de agentes como un sistema operativo (memoria principal / archivo) [F https://arxiv.org/abs/2310.08560]. Memoria externa sin validación.
- **Atención lineal/Delta (Gated DeltaNet, Kimi Delta Attention)**: memoria asociativa que se escribe con regla local en cada paso; ya dentro de Qwen3.5 y Kimi Linear [F https://arxiv.org/abs/2510.26692, HF Qwen3.5]. Es la regla local de JUACO a escala; se entrena con gradiente, no vive entre sesiones [I].
- **Seguridad de memoria de agentes (2026)**: hay una oleada de trabajos sobre envenenamiento de memoria y validación antes de escribir (proveniencia, validación previa a la consolidación, cuarentena por origen): survey "Toward Mnemonic Sovereignty" [F https://arxiv.org/html/2604.16548v1], "From Untrusted Input to Trusted Memory" [F https://arxiv.org/html/2606.04329v1], MemSecBench [F https://arxiv.org/pdf/2607.27080], "Proof-of-Execution Memory" [F https://arxiv.org/pdf/2608.16032]. Sólo se leyeron los resúmenes de búsqueda; no se abrió cada paper [NC detalles].

**El hueco real** [I]: lo que existe se reparte en tres grupos que casi no se tocan — (1) memorias que se escriben en uso (kNN-LM, GRACE, WISE, Titans), sin economía de vida/muerte ni validación por confirmaciones; (2) validación y cuarentena, pero para *agentes de texto* y por seguridad, no para correcciones en el espacio latente de un modelo; (3) consolidación a pesos (MEMIT, sueños/LoRA), sin pasar por cuarentena. La combinación "corrección en espacio latente con compuerta + economía de supervivencia + promoción por confirmación independiente + absorción a pesos sólo de lo validado + auditoría por pieza" no la encontré junta en lo que abrí; no la vi, pero un barrido incompleto no prueba que no exista: antes de hablar en público hay que hacer una búsqueda sistemática en Google Scholar de esa combinación (siguiente tarea barata).

---
### Qué no pude confirmar (resumen)
- Licencias exactas de pesos "Model Agreement" de V3 y "Modified MIT" de Kimi (texto legal): no abierto.
- Tamaño del archivo de V4-Flash / Pro (1.6T solo figura en blog comercial) y de los Qwen3.5 chicos.
- Calidad en español de todos los modelos (no hallé una medición; sólo cantidad de idiomas declarados).
- Velocidades en CPU de los chicos (sólo hay dato del Kimi K2 vía Unsloth).
- Ficha de GPU del laboratorio universitario.
- Detalles de los 4 papers de seguridad de memoria 2026 (sólo resúmenes de búsqueda).
- Todo lo marcado [M]/[I].
