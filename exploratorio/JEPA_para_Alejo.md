# JEPA para Alejo (5-oct-2026, solo lectura: web + archivos locales; no instalé ni corrí nada)

Marcas: [F url] = abrí la fuente hoy; [M] = de memoria, sin abrir; [I] = inferencia mía; [L] = leído en los informes locales.
Misión: llegar a la AGI por este camino (JUACO: organismo mínimo con reglas locales; hermano Alejo).

## 0. VEREDICTO: CON CONDICIONES

Vale la pena explorarlo SOLO como una pieza barata de comparación: cambiar el "pan" de la hamburguesa (hoy un transformador diminuto entrenado con etiquetas) por un codificador congelado de estilo JEPA, y medir si las células de memoria funcionan mejor, igual o peor que con un codificador cualquiera (incluso uno al azar). No vale la pena como "JUACO evoluciona a otro tipo de aprendizaje": lo que el director oyó ("congela partes y eso le permite evolucionar") es, hasta donde pude verificar, una descripción coloquial de congelar para estabilizar; no hay evolución en JEPA [I].
Primer paso (una tarde, CPU, reutiliza `hamburguesa.py`): experimento A de la sección 4, con tres "panes" congelados (JEPA diminuto, autocodificador de píxeles, rasgos al azar) y las mismas células. Si el pan al azar iguala al JEPA, JEPA no aporta nada a nuestro bloque y se cierra.

## 1. Qué es JEPA, sin jerga

**La imagen.** Imagina que a un aprendiz le tapas un pedazo de una foto y le pides que *describa con una ficha de rasgos* (no que dibuje) lo que había debajo. Dibujar pixel por pixel obliga a gastar esfuerzo en detalles que nadie puede adivinar (la hoja exacta de un árbol). Describir en "fichas de rasgos" permite saltarse lo impredecible. Eso es JEPA: "arquitectura predictiva con incrustación conjunta". Predice **representaciones** (la ficha de rasgos, un vector de números), no píxeles ni palabras.

**Tres partes** (I-JEPA, imágenes) [F https://arxiv.org/html/2301.08243]:
- *Codificador de contexto*: mira la parte visible y produce sus fichas.
- *Codificador objetivo*: mira la parte tapada (completa) y produce las fichas "correctas" que hay que adivinar.
- *Predictor*: una red angosta (384 dimensiones, 6 a 16 capas según el tamaño) que, a partir de las fichas del contexto, adivina las fichas del objetivo. Pérdida: distancia L2 entre lo adivinado y lo real, en el espacio de fichas. Usa 1 bloque de contexto y 4 bloques objetivo.

**Qué se congela y cuándo.**
1. Durante el preentrenamiento, el codificador objetivo NO se entrena por gradiente: es un *promedio móvil* (EMA) del codificador de contexto, con momento 0.996 que sube hacia 1.0, y se corta el gradiente hacia él ("stop-gradient") [F https://arxiv.org/html/2301.08243; V-JEPA 2 igual: https://arxiv.org/html/2506.09985]. Imagen: el "profesor" es la foto de hace semanas del alumno; así el alumno no puede engañar al profesor para que ambos digan siempre lo mismo. Esto es un congelado a medias (se mueve despacio), y es la parte que se parece a lo que oyó el director.
2. En V-JEPA 2-AC (para robots) el codificador de 1.000 millones de parámetros se CONGELA del todo y solo se entrena un predictor nuevo (~300 M de parámetros, 24 capas) que además recibe las acciones del robot [F https://arxiv.org/html/2506.09985].

**Cómo se usa para decidir.** No decide la red; decide un buscador por encima [F https://arxiv.org/html/2506.09985]:
- Se le da al robot una *foto de la meta*; se codifica en fichas.
- Se prueban muchas secuencias de acciones; el predictor "imagina" las fichas futuras de cada una.
- Se elige la secuencia cuya ficha final queda a menor distancia L1 de la ficha de la meta (método de entropía cruzada, CEM: 800 candidatas, 10 rondas); se ejecuta la primera acción y se repite (control predictivo por modelo).
- Costo: 16 s por acción (en GPU) contra 4 min del modelo de comparación Cosmos.
Esto es planificar con un modelo del mundo. JEPA le pone el modelo; la decisión es una búsqueda con una meta dada desde fuera [I: en este diseño la meta no nace de ninguna necesidad del robot].

**Versiones, fechas, tamaños, datos, cómputo, resultados.**

| versión | fecha | qué | cifras (fuente) |
|---|---|---|---|
| I-JEPA | ene-2023 | imágenes | ViT-H/14 en ImageNet-1K: 79.3 % top-1 con sonda lineal en 300 épocas (MAE: 77.2 %); ~1200 horas-GPU (16 A100 en menos de 72 h), ~10× menos que MAE [F https://arxiv.org/abs/2301.08243; https://arxiv.org/html/2301.08243] |
| V-JEPA | feb-2024 | video | 2 M de videos; modelo congelado con sonda: Kinetics-400 81.9 %, Something-Something-v2 72.2 %, ImageNet 77.9 % [F https://arxiv.org/abs/2404.08471] |
| V-JEPA 2 | 11-jun-2025 | video a gran escala | más de 1 millón de horas de video + imágenes (VideoMix22M: 22 M de muestras); 300 M a 1 B de parámetros; SSv2 77.3 %, Epic-Kitchens-100 39.7 recall@5, PerceptionTest 84.0, TempCompass 76.9 [F https://arxiv.org/abs/2506.09985; https://arxiv.org/html/2506.09985] |
| V-JEPA 2-AC | ídem | robot | predictor entrenado con menos de 62 horas de video sin etiquetas del conjunto Droid (23 000 trayectorias); sin entrenar en el sitio, brazos Franka en 2 laboratorios; media de los 2 labs: alcanzar 100 %, agarrar taza 65 %, agarrar caja 25 %, recoger y colocar taza 80 %, caja 65 %; el rival Octo: 15 %, 0 %, 15 %, 10 % en agarrar taza, agarrar caja, recoger-colocar taza y caja [F https://arxiv.org/html/2506.09985] |
| DINO-WM (no es Meta-JEPA pero es el mismo esquema) | nov-2024 | codificador DINOv2 congelado + predictor + planificación en 6 entornos (laberinto, empujar objetos) | [F https://arxiv.org/abs/2411.04983] |
| LeJEPA | 11-nov-2025 | recetas sin trucos | SIGReg (ver 3c); sin stop-gradient, sin profesor-alumno, sin calendarios; ViT-H/14 en ImageNet-1K 79 % con sonda lineal; ~50 líneas de código [F https://arxiv.org/abs/2511.08544] |
| LeWorldModel | 13-mar-2026 (v. jun-2026) | modelo del mundo de extremo a extremo desde píxeles | ~15 M de parámetros, una GPU en unas horas; planifica hasta 48× más rápido que modelos del mundo basados en modelos fundacionales; dos términos de pérdida [F https://arxiv.org/abs/2603.19312] |
| V-JEPA 2.1 | 16-mar-2026 | rasgos densos | familia 80 M a 2 B [F https://github.com/facebookresearch/vjepa2; fecha por búsqueda https://mishig-jepawiki.hf.space/wiki/papers/2603.14482] |

**Código, pesos, licencia, tamaño chico, PC sin GPU.**
- V-JEPA 2 y 2.1: repositorio oficial con pesos; licencia en su mayoría MIT, con partes bajo otras (Apache 2.0 en archivos de utilidades) [F https://github.com/facebookresearch/vjepa2]. La ficha de Hugging Face del ViT-L (0.3 B) dice MIT [F https://huggingface.co/facebook/vjepa2-vitl-fpc64-256]. Pesos: ViT-L 300 M, ViT-H 600 M, ViT-g 1 B; en 2.1 aparece **ViT-B de 80 M** (resolución 384) [F mismo repositorio]. Se carga con PyTorch Hub o transformers; requiere PyTorch, timm, einops. Existe también el codificador+predictor de V-JEPA 2-AC (base ViT-g).
- I-JEPA: repositorio archivado (solo lectura) desde el 1-ago-2024, con ViT-H y ViT-g; su LICENSE es **CC BY-NC 4.0 (no comercial)** [F https://github.com/facebookresearch/ijepa; https://raw.githubusercontent.com/facebookresearch/ijepa/main/LICENSE]. Para uso académico/educativo del director sirve; ojo con cualquier uso con fines de lucro.
- El más chico utilizable de Meta que verifiqué: ViT-B de 80 M (V-JEPA 2.1). Correr un solo codificador así en CPU para extraer rasgos de algunos cientos de clips es plausible (segundos por clip) [I, no medido]. V-JEPA 2-AC completo (1 B + 300 M + 800 candidatas × 10 rondas, 16 s por acción *en GPU*) no es viable en CPU [I]. El candidato realista para CPU es LeWM (15 M de parámetros); no verifiqué su licencia ni su código, ni su tiempo en CPU.

## 2. La idea de LeCun de fondo, y qué se parece a JUACO

"A Path Towards Autonomous Machine Intelligence" (2022): propuesta de arquitectura, no resultados. Seis módulos [F https://mishig-jepawiki.hf.space/wiki/papers/lecun-position-paper; resumen en https://ai.facebook.com/blog/yann-lecun-advances-in-ai-research; no pude abrir el PDF de OpenReview, que pedía verificación]:
- **Percepción** (¿cómo está el mundo?), **modelo del mundo** (¿qué pasaría si hago X? = el predictor JEPA), **costo** (cuán "mal" me siento), **actor** (propone acciones), **memoria de corto plazo** (guarda estados y costos), **configurador** (ajusta los otros módulos para la tarea).
- El costo tiene dos partes: **costo intrínseco** (fijo, no entrenable: dolor, hambre, sed, curiosidad) y un **crítico** entrenable que aprende a prever ese costo.
- Dos modos: reactivo ("modo 1", la política directa) y deliberado ("modo 2", planificar con el modelo del mundo y control predictivo); lo planificado se destila en reflejos con la práctica.
- Jerarquía (H-JEPA): JEPAs apilados que predicen a distintas escalas de tiempo.
- Contra el colapso, cuatro criterios: maximizar la información de las dos codificaciones, minimizar el error de predicción y limitar la información del latente.

**Qué se parece a JUACO [I]:**
- El **costo intrínseco fijo** es la necesidad propia (hambre/energía) de JUACO: dos arquitecturas que proponen "el agente actúa para bajar un malestar interno que no aprende". Es la coincidencia conceptual más fuerte.
- El **modo 1** (reflejo por estado) se parece a la boca que decide por la necesidad activa.
- El **crítico** que aprende a prever el costo se parece a la célula que aprende cuánto vale su corrección (energía).
**Qué NO se parece:**
- Todo el sistema de LeCun está pensado diferenciable y entrenado con gradiente; JUACO prohíbe gradiente dentro del tronco [L ALEJO.md].
- LeCun tiene un modelo del mundo que imagina el futuro (modo 2); JUACO cerró el planear: P9 planear CERRADO ×3 [L FABLE_bloques_autoentrenables.md], justo la pieza que JEPA sí tiene.
- Para LeCun el modelo del mundo se aprende primero, en frío, de video; JUACO no tiene predictor del futuro.
- JUACO tiene vida/muerte/selección; LeCun, ninguna.

## 3. El puente con lo nuestro

**(a) ¿La hamburguesa es de la misma familia que "codificador congelado + módulo pequeño"? Sí.** Es la misma familia que V-JEPA 2-AC, DINO-WM, un LoRA o GRACE: un cuerpo grande congelado y un módulo pequeño que aprende lo nuevo. Diferencias reales con V-JEPA 2-AC:

| | V-JEPA 2-AC | hamburguesa |
|---|---|---|
| módulo que aprende | predictor de 300 M, con gradiente | células con reglas locales, sin gradiente [L] |
| cuándo aprende | antes del uso, con 62 h de video | en uso, tras cada consulta [L] |
| qué aprende | cómo cambian las fichas si hago una acción (el mundo) | qué corrección pisa la salida cuando el cuerpo falla (hechos) [L] |
| qué lee | la ficha del codificador | el estado interno del transformador [L] |
| cómo decide | planifica imaginando el futuro, meta dada | no decide; corrige una respuesta |
| el cuerpo | codificador autosupervisado, sin etiquetas | transformador entrenado con etiquetas [L] |
| olvido | no hay (no se actualiza en uso) | suelta la corrección cuando el hecho vuelve; "sueño" para pasarlo a los pesos [L] |
La hamburguesa es una memoria que corrige; V-JEPA 2-AC es un simulador de consecuencias. No se sustituyen: se complementan [I].

**(b) ¿Tiene sentido un bloque de células JUACO sobre un codificador JEPA congelado en vez de sobre un modelo de lenguaje? Con condiciones.**
- *Qué se ganaría [I, hipótesis]:* (i) un espacio de fichas pensado para ser predecible y para descartar lo irrelevante; con SIGReg (LeJEPA/LeWM) las fichas se reparten de forma casi gaussiana y uniforme, y eso podría hacer la compuerta de parecido menos frágil que con el estado de un transformador diminuto (la compuerta fija 0.9 falló en 3 de 8 semillas, y 0.98 se eligió viendo esas tres [L INFORME_HAMBURGUESA]); (ii) un lugar natural para la decisión: las células podrían corregir el **costo** (la distancia a la meta) en vez de una salida de lenguaje, es decir, hacer de costo intrínseco/crítico aprendible *encima* del modelo del mundo, que es el hueco de LeCun entre el costo fijo y el crítico; (iii) un mundo con acciones y consecuencias donde "lo que cambió esta semana" tiene sentido (el oasis que se muda).
- *Qué se perdería:* (i) el codificador JEPA no tiene cabeza de salida ni logits que pisar: hay que fabricar una (una sonda lineal o una política), y esa parte entrenada con gradiente pasa a ser el pan real; (ii) el efecto "el estado interno ya sabe la respuesta" (clave de la última capa) depende de que el modelo haya sido entrenado para responder; un JEPA no fue entrenado para responder, solo para predecir fichas; (iii) los 20 hechos y las paráfrasis eran un mundo de juguete a medida del transformador; con un JEPA hay que inventar otro mundo.
- Todo esto es hipótesis; la sección 4 la pone a prueba.

**(c) "Cada célula predice lo que le va a llegar y aprende de su propio error": ¿qué hace JEPA para no colapsar?**
Primero, un matiz importante. En `INFORME_2.md` la variante `rpe` no aprendió porque la célula solo recibía **un número** (el pago de energía) y predecía **ese número**; es una señal muy pobre, "ni con 1 capa" [L INFORME_2 sec. 2]. No se demostró un colapso. JEPA predice un **vector rico** (la ficha completa del objetivo) que viene de la propia entrada, no un escalar de pago. Es otra clase de señal [I].

Colapso = la red descubre que dando siempre la misma ficha a todo, la predicción es trivialmente perfecta. JEPA lo evita con tres recetas:
1. **Promedio móvil + stop-gradient + predictor angosto** (I-JEPA, V-JEPA, V-JEPA 2): el objetivo es una copia lenta del codificador; el alumno no puede arrastrarlo [F https://arxiv.org/html/2301.08243]. Funciona en la práctica, la explicación teórica es floja [M].
2. **Regularización tipo VICReg** (Bardes, Ponce, LeCun, mayo-2021): un término de *varianza* (cada dimensión de la ficha debe variar de verdad, no ser constante), uno de *covarianza* (las dimensiones no deben copiarse entre sí) y uno de invarianza [F https://arxiv.org/abs/2105.04906]. Imagen: obligar a que el "carné de rasgos" use todas sus casillas y que no sean fotocopias unas de otras.
3. **SIGReg (LeJEPA, nov-2025; LeWM, mar-2026)**: obliga a que el conjunto de fichas siga una distribución gaussiana isotrópica (reparto redondo y parejo) mirando muchas proyecciones al azar; es el único término anticolapso, un solo parámetro de balance, sin profesor ni stop-gradient [F https://arxiv.org/abs/2511.08544; https://arxiv.org/abs/2603.19312].
Nota de honestidad: las tres recetas miran estadísticas de todo un lote de ejemplos (varianza entre muestras), cosa que una célula sola no ve. Una versión local necesitaría que cada célula lleve su propia varianza corriente [I].

**¿Hay versiones JEPA con aprendizaje local o sin retropropagación de extremo a extremo?**
- No encontré ninguna publicación que entrene un JEPA con reglas locales (busqué hoy con dos búsquedas; la ausencia es de mi búsqueda, no una prueba) [F búsqueda web 5-oct-2026].
- Lo más cercano en espíritu: (a) el predictor de V-JEPA 2-AC: la retropropagación queda confinada a un módulo pequeño sobre un codificador congelado, es decir, no hay retropropagación a través de todo el sistema, pero sí dentro del predictor [F https://arxiv.org/html/2506.09985]; (b) la codificación predictiva como reemplazo local de retropropagación (Millidge et al.) [F https://arxiv.org/abs/2202.09467]; (c) los métodos locales de la familia Forward-Forward y Hebb (SoftHebb: 27.3 % en ImageNet [L FABLE; F https://arxiv.org/abs/2209.11883]). Unirlos con un objetivo JEPA es un hueco abierto, y una pregunta que se puede mirar en chico [I].

## 4. Tres experimentos de una tarde (PC sin GPU declarada)

Convenciones: paso 0 de cordura primero (regla de Alejo: el techo debe resolver la tarea con acierto ≥ 0.98 o el experimento no existe [L ALEJO.md]). Mundos de juguete en numpy/PyTorch CPU. Todas las predicciones son mías y no están calibradas; sin preregistro todavía (si salen, se preregistran antes de la serie, con 20 semillas y réplica). "Pan" = la parte grande congelada.

### A. Hamburguesa sobre tres panes congelados (el más barato y el que decide si JEPA importa)
- **Tarea.** El mundo de `hamburguesa.py` (20 hechos que cambian, 3 paráfrasis), pero la observación es una imagen chica sintética (por ejemplo 16×16, un símbolo por grupo y una variación por paráfrasis). Tres panes congelados, mismo tamaño:
  - P1: JEPA diminuto (LeWM-style: predicción del siguiente latente + SIGReg), entrenado con gradiente en unas horas de CPU y luego congelado.
  - P2: autocodificador (reconstruye píxeles).
  - P3: **rasgos al azar congelados** (control hecho a mano que puede ganar).
- **Brazos.** Para cada pan: (1) pan solo; (2) RAG por embeddings; (3) kNN sobre las fichas (línea de base estándar); (4) hamburguesa con compuerta fija y con compuerta adaptativa [L INFORME_HAMBURGUESA sec. 7]; (5) techo: seguir entrenando la cabeza de salida con Adam en línea; (6) control: pago barajado.
- **Medida.** Acierto en cambiados; acierto en la primera consulta lejana; acierto en paráfrasis nunca vistas (vecinas); estabilidad entre semillas (cuántas de 8 fallan). Paso 0: sonda lineal sobre cada pan ≥ 0.98 en los hechos base.
- **Predicción que puede fallar.** Hamburguesa sobre P1 ≥ 0.90 en vecinas en ≥ 7/8 semillas con compuerta fija 0.98; hamburguesa sobre P2 en ≤ 5/8; hamburguesa sobre P3 ≤ 0.60 en vecinas. Hamburguesa ≥ kNN en la vuelta del hecho (recuperar en ≤ 100 consultas contra ≥ 300 del kNN, como en el informe 3).
- **Control que puede ganar.** P3 (al azar) o kNN. Si P3 ≈ P1 en vecinas, JEPA no aporta.
- **Abandono.** P3 ≥ P1 − 0.05 en vecinas y estabilidad igual: se cierra JEPA como pan para nuestro bloque, se documenta como NO limpio.

### B. Decisión: un modelo congelado imagina, un bloque JUACO decide (el que pidió el director)
- **Tarea.** Mundo de casillas 8×8 con muros, comida y trampa; hambre que sube con el tiempo; cada 500 pasos la comida se muda a otra casilla (el "oasis" de JUACO). Observación = imagen chica.
  - Predictor congelado: JEPA diminuto del experimento A (o un predictor condicionado por acciones, estilo V-JEPA 2-AC en chico: codificador congelado, predictor entrenado con ~5 000 pasos al azar). Sabe consecuencias de moverse, **no sabe dónde está la comida ahora**.
- **Brazos.** (1) Azar. (2) **Línea de base a mano**: ir a lo menos visitado (la regla que ya funcionó en JUACO, ×2 [L ESTADO]). (3) **Planificar con el predictor** (CEM chico: 64 candidatas × 3 rondas, horizonte 6), con meta = la ficha de la última comida vista. (4) **Bloque JUACO**: células con compuerta por estado propio (hambre + ficha actual) que sesgan la acción y aprenden con el pago del resultado; sin gradiente. (5) **Política aprendida por refuerzo**: Q tabular y una red chica con Adam (techo). (6) Control: pago barajado. (7) Bloque + planificador: el planificador usa el costo corregido por las células (la hipótesis de la sección 3b).
- **Medida.** Comida por 100 pasos; pasos hasta recuperar 90 % de la comida tras una mudanza (mediana de 40 mudanzas); operaciones por decisión. 20 semillas, réplica ×2.
- **Predicción que puede fallar.** (3) planificar con meta fija no recupera tras la mudanza hasta ver comida de nuevo (≥ 300 pasos); (2) recupera en ≈ 100–200; Q tabular en ≈ 150–400; (4) en ≤ 150 y a ≥ 5× menos operaciones por decisión que (3) y que la red con Adam; (7) mejor que (3) y (4) por separado en ≥ 14/20 semillas. Paso 0: el predictor debe predecir el siguiente latente con error ≤ 5 % del azar y el techo debe resolver el mundo estático.
- **Control que puede ganar.** (2) la regla a mano y el Q tabular: es un problema de manual, y es probable que ganen [L ALEJO.md predice lo mismo].
- **Abandono.** (4) tarda > 400 pasos, o (7) no supera a (3) y (4) en 13/20 semillas: el bloque no aporta como decisor sobre un modelo del mundo; queda como nota negativa.

### C. Célula que predice su entrada con anticolapso local (la pregunta 3c)
- **Tarea.** Secuencia de fichas de un punto que se mueve en una cuadrícula con ruido; cada célula predice la ficha siguiente (vector) a partir de su entrada y aprende de su propio error.
- **Brazos.** (1) Célula con error de predicción local, sin ningún anticolapso (el diseño que falló). (2) La misma + término local de **varianza corriente por dimensión** (VICReg local). (3) La misma + objetivo con promedio móvil (EMA) por célula. (4) **Techo:** mini-JEPA con gradiente (SIGReg). (5) **Línea a mano:** rasgos al azar fijos + regla delta en la lectura. (6) Control: objetivo barajado en el tiempo.
- **Medida.** Rango efectivo de las fichas (cuántas dimensiones usan de verdad), desviación por dimensión, acierto de una sonda lineal que lee la posición del punto; 20 semillas.
- **Predicción que puede fallar.** (1) colapsa: rango efectivo < 2 en 2 000 pasos en ≥ 15/20; (2) y (3) rango ≥ 6 y sonda ≥ 0.80; techo ≥ 0.95; (5) sonda ≥ 0.70 (el azar fijo suele ser sólido); (6) ≤ 0.2.
- **Control que puede ganar.** (5): rasgos al azar con regla delta. Si (5) ≥ (2) en sonda, el aprendizaje local de rasgos no aporta (coincide con INFORME_2: "capas congeladas al azar + boca" ganan [L]).
- **Abandono.** (2) y (3) colapsan o dan sonda ≤ (5): se cierra la línea "célula que predice su entrada"; la señal de pago pobre no se arregla con anticolapso.

Orden valor/costo: A (reutiliza todo, 3 a 4 h), B (más trabajo: mundo nuevo, 1 tarde larga), C (el más incierto, pero barato).

## 5. Qué NO se puede decir, y qué ya existe con otro nombre

**No se puede decir:**
- "JUACO es un JEPA" o "usa JEPA": no hay codificador ni predictor de fichas en JUACO.
- "JEPA decide" o "piensa": decide una búsqueda (CEM) con una meta dada en forma de imagen [F https://arxiv.org/html/2506.09985].
- "JEPA evoluciona" o "se congela para evolucionar": se congela para no colapsar y para entrenar un predictor barato; evolución no hay [I].
- "La hamburguesa/Alejo es la siguiente generación de JEPA", "camino a la AGI", "mejor que V-JEPA".
- Cualquier cifra de robot como propia: son de Meta, 62 horas de datos, con éxito 25 % a 80 % según la tarea [F https://arxiv.org/html/2506.09985].
- "Aprendizaje local sin retropropagación en JEPA": no existe que yo haya encontrado; sería un resultado nuevo, no una cita.

**Ya existe con otro nombre (una línea cada uno):**
- Modelo del mundo en espacio de fichas + planificación con pesos congelados: DINO-WM, DINOv2 congelado + predictor, nov-2024 [F https://arxiv.org/abs/2411.04983].
- Modelos del mundo con planificación en el espacio latente: TD-MPC2, planificación local en el latente de un modelo sin decodificador, un agente de 317 M para 80 tareas [F https://arxiv.org/abs/2310.16828].
- Imaginar para aprender una política: DreamerV3 (una configuración para más de 150 tareas; diamantes de Minecraft sin datos humanos) [F https://arxiv.org/abs/2301.04104].
- Modelo aprendido que predice recompensa, valor y política, sin conocer las reglas: MuZero [F https://arxiv.org/abs/1911.08265].
- Cuerpo congelado + módulo pequeño que aprende: LoRA, 10 000× menos parámetros entrenables [F https://arxiv.org/abs/2106.09685].
- Cuerpo congelado + libro de claves que corrige en uso, sin tocar pesos: GRACE [F https://arxiv.org/abs/2211.11031]; el vecino más cercano en el espacio del modelo: kNN-LM [F https://arxiv.org/abs/1911.00172].
- Memoria que aprende en el momento de uso: Titans [F https://arxiv.org/abs/2501.00663, tal como lo cita ALEJO.md]; capas de memoria: Meta [F https://arxiv.org/abs/2412.09764, ídem].
- Memoria episódica para agentes: Control episódico sin modelo (Blundell et al., 2016) y Neural Episodic Control (Pritzel et al., 2017) [M, sin abrir; verificar].
- Memoria rápida + lenta con "sueño": sistemas de aprendizaje complementarios (McClelland 1995) [L INFORME_HAMBURGUESA sec. 6].
- Anticolapso: VICReg [F https://arxiv.org/abs/2105.04906], SIGReg [F https://arxiv.org/abs/2511.08544].
- Aprendizaje local por codificación predictiva: Millidge et al. [F https://arxiv.org/abs/2202.09467].

## 6. Lo no verificado
- No pude abrir el PDF de LeCun (OpenReview pidió verificación); la sección 2 se apoya en resúmenes secundarios (jepawiki de Hugging Face y el blog de Meta).
- Los tamaños y cifras de V-JEPA 2/2-AC vienen de la versión HTML de arXiv leída por un resumidor automático; las cifras de las tablas de robot se deben cotejar con la tabla original antes de citarlas en público.
- No verifiqué la licencia ni el código de LeWM ni su tiempo en CPU.
- Que ViT-B de 80 M corra en CPU en segundos por clip: inferencia mía, sin medir.
- La fecha de V-JEPA 2.1 (16-mar-2026) viene de un buscador, no de la fuente primaria; las predicciones numéricas de los experimentos son mías, sin calibrar.
- Mi hipótesis de que la geometría de SIGReg haga menos frágil la compuerta de la hamburguesa es una idea, no un dato.
