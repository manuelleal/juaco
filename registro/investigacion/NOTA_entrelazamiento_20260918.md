# Nota: entrelazamiento, no-comunicación, y la traducción honesta a JUACO (18 sep 2026)

Revisor de la idea del director: "partículas entrelazadas se comunican a distancia; la muerte es transición si
la comunicación no desaparece; la regla de la energía". Sin Pool, sin commits, sólo esta nota.

## 1. Qué dice la física (con cita verificable)

- **EPR 1935** (Einstein, Podolsky, Rosen, "Can Quantum-Mechanical Description of Physical Reality Be Considered
  Complete?", *Phys. Rev.* 47, 777, 1935): plantea que si la mecánica cuántica es completa, dos partículas que
  interactuaron y se separan quedan correlacionadas de un modo que a los autores les pareció incompatible con
  el realismo local; lo leen como síntoma de que falta algo en la teoría, no como un canal de señales.
- **Bell 1964** ("On the Einstein Podolsky Rosen paradox", *Physics* 1(3), 195–200): demuestra que ninguna teoría
  de variables ocultas locales puede reproducir todas las correlaciones de la mecánica cuántica (desigualdad de
  Bell); los experimentos posteriores confirman que la naturaleza viola esa desigualdad. Esto es lo que la gente
  llama "entrelazamiento real": correlaciones más fuertes que cualquier explicación local-realista, no un enlace
  causal entre las partículas.
- **TEOREMA DE NO-COMUNICACIÓN**: Eberhard 1978 ("Bell's theorem without hidden variables", *Il Nuovo Cimento B*
  38, 75) y, de forma más general, Ghirardi, Rimini & Weber 1980 ("A general argument against superluminal
  transmission through the quantum mechanical measurement process", *Lettere al Nuovo Cimento* 27, 293) prueban
  que, midiendo sólo su propia partícula, el observador local no puede saber nada sobre lo que el otro observador
  hizo con la suya: las estadísticas locales no cambian pase lo que pase al otro lado. **Sin variar la estadística
  local no hay bit transmitido.** No existe una versión de este teorema que permita excepciones "para información
  biológica"; es una consecuencia estructural del formalismo (traza parcial invariante), no de una limitación
  tecnológica.
- **Teleportación cuántica**: Bennett, Brassard, Crépeau, Jozsa, Peres & Wootters 1993 ("Teleporting an unknown
  quantum state via dual classical and Einstein-Podolsky-Rosen channels", *Phys. Rev. Lett.* 70, 1895) muestran
  cómo reconstruir un estado cuántico desconocido en un sitio remoto — pero el protocolo **exige enviar el
  resultado de una medición por un canal clásico** (radio, cable, luz: a velocidad ≤ c) además del par entrelazado.
  Sin ese canal clásico, Bob sólo tiene ruido puro en su partícula. La "teleportación" no transmite nada más
  rápido que la luz; el nombre es publicitario, el mecanismo es correlación + canal ordinario.

## 2. Por qué "comunicación sin canal" no existe, y qué sí existe

Lo que el entrelazamiento da es **correlación instantánea sin transferencia de información**: si mido aquí,
la estadística de lo que se mida en China no cambia por mi elección de qué medir (no-signalling). Lo único que
permite usar esa correlación para algo (criptografía cuántica, teleportación) es sumarle un **canal clásico**
que sí viaja a velocidad finita y sí es interceptable, cifrable y sujeto a la termodinámica ordinaria de la
información. No hay atajo: correlación por sí sola = cero bits; correlación + canal = tantos bits como el canal
permita. Esto no es un límite de ingeniería de 2026, es un teorema (Eberhard 1978; GRW 1980).

## 3. Traducción honesta al organismo (no metáfora, medible)

En JUACO ya hay un análogo exacto de "correlación + canal", no de comunicación instantánea: el **BLOQUE 4/4b**
(patrón de referencia + recompensa) mueve la conducta del receptor sin experiencia propia — "el mensaje cambia
la conducta del receptor sin experiencia propia; la referencia es de familia y parcial" (registro, cierre 18 sep
18:45). Eso es un canal clásico ordinario (escritura en la tabla de pares), no entrelazamiento. La idea del
director, despojada de la física que no aplica, dice algo correcto y ya operacional: **la información sobrevive
al cuerpo sólo si vive en otro sitio** (otro cuerpo, la tabla de la población) **y para pasar de un cuerpo a
otro necesita un canal** — que aquí es el mensaje, no un vínculo cuántico. "La muerte como transición" deja de
ser metafísica y se vuelve **HERENCIA POR MENSAJE**: el padre emite lo que sabe (mensaje del bloque 4b) antes de
morir y el hijo lo escribe sin morder, en vez de heredar sólo valores numéricos (H-1 ya probó que heredar valores
da 10–20 %, no lo que falta) o nada (H-1: R₀ 0.14–0.17, linaje no se sostiene — "H-1 QUE LA MUERTE MATE").

## 4. Preregistro corto — HERENCIA POR MENSAJE

- **Instrumento:** `organismo_vivo_h1.py` + canal de b4b (patrón de referencia + recompensa), `muerte_real = 1`.
- **Brazos:** (a) hijo vacío (control, = H-1 "nada"); (b) hijo recibe los mensajes del padre antes de morir
  (protocolo b4b, dirección −); (c) hijo recibe mensajes **barajados** (control de contenido, = H-1 "barajado");
  (d) hijo hereda valores directos (control, = H-1 "M1").
- **Medida:** R₀ con muerte real (como H-1), vida mediana, y **exposiciones hasta asociar** del hijo (cuántas
  mordidas necesita para llegar al criterio de aprendizaje, contra las ~25 de un hijo vacío).
- **Predicción:** (b) > (d) > (c) ≈ (a) en R₀ y en exposiciones-hasta-asociar; si el mensaje vale lo que dice la
  hipótesis, (b) debe acercarse al régimen de "aprender de un golpe" y subir R₀ sobre 0.17 de forma clara
  (umbral preregistrado: ≥ 1.30× el brazo (a), el mismo criterio H1-3 que "hereda valores" no alcanzó).
- **Qué lo refuta:** si (b) ≈ (c) ≈ (a) (el mensaje no ayuda más que ruido barajado) o si (b) no baja las
  exposiciones-hasta-asociar del hijo, la hipótesis "la comunicación sostiene el linaje mortal" queda refutada
  con este canal y hay que buscar otro mecanismo (dote, cuidado parental — ya anotados como alternativa en H-1).

## 5. Tres líneas honestas

- **Correcto** en la idea del director: que la muerte no tiene por qué ser el final de la información si esa
  información vive en otro sitio y hay canal para pasarla — eso es exactamente lo que JUACO mide con mensaje +
  recompensa en el bloque 4/4b, y es una hipótesis fértil, ya con datos parciales (H-1, bloque 4b).
- **No correcto:** que el entrelazamiento cuántico sea o pueda ser ese canal. El teorema de no-comunicación
  (Eberhard 1978; Ghirardi, Rimini & Weber 1980) prohíbe usar el entrelazamiento para enviar información sin un
  canal clásico adicional; "una partícula aquí y otra en China que se comunican" no describe lo que el
  entrelazamiento hace.
- **No pude verificar:** "la regla de la energía" tal como la enuncia el director — no hay una formulación
  concreta que revisar (¿conservación de energía aplicada a la información? ¿algo de termodinámica de Landauer?);
  si el director la precisa, se puede buscar y citar en la próxima nota. No se inventa una cita para llenar esto.
