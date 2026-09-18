# LITERATURA — ¿qué de lo hallado el 18-sep ya existe? (revisor de literatura, 18 sep 2026)

**Misión (no opcional):** llegar a la AGI por este camino — un organismo mínimo con reglas locales, sin retropropagación en
tiempo de ejecución, que aprende, sobrevive y se reproduce, con evidencia preregistrada. **Encargo de hoy:** decir con
honestidad qué de lo hallado en la madrugada del 18 ya está en la literatura y qué no. Sin tocar nada del repo salvo este
archivo; sin Pool; sin commits. Fuentes leídas: `CLAUDE.md` "Estado (día 7)", las entradas del 18-sep en
`registro/REGISTRO_etapas_1_2.md` (ERR-35, "LÍNEA XOR CERRADA", MUNDO VIVO y réplica, ERR-37, "Bloque de la sal — ALIAS DE
CÓDIGO", ERR-38, "Candidato v15d", "Bloque B-5" y su réplica, "Mundo vivo, peldaño 2"), `ENJAMBRE_xor_20260918.md` §1,
`NOTA_v11_pattern_separation_20260917.md` (ya cita CLS y ARTMAP), y los preregistros del mundo vivo.

**Cómo se verificó.** Cada cita de abajo se comprobó hoy por búsqueda web contra la ficha del editor, PubMed o el repositorio
del autor (autores, año, título, revista); los enunciados que atribuyo a cada trabajo salen de su resumen. **No abrí los PDF
uno a uno**, así que por la regla de la NOTA_v11 ("nada entra al registro como cita hasta abrir el PDF") estas citas están
verificadas a nivel de ficha, no de texto. Donde no pude verificar algo, lo digo (§5 y §6).

**Criterio del veredicto.** "Ya existe" = el fenómeno y el mecanismo están descritos, aunque no con estos números. "Existe en
parte" = las piezas existen por separado; el ensamblaje o el resultado concreto no lo encuentro. "No lo encuentro" = ni las
piezas ni el resultado. El director pidió preferir un "ya existe" claro a un "quizá nuevo" vago; así está escrito.

---

## 0. Tabla resumen

| resultado | precedente más cercano | qué ya existe | qué NO encuentro en esa forma | veredicto |
|---|---|---|---|---|
| **1. Alias de código** (K=3 de 90; dos estímulos comparten código en ~9 % de semillas; la sal hereda el valor del veneno, el veneno pierde la mitad del miedo; evitación ×7; no depende de la necesidad; la puerta por código lo empeora) | Dasgupta, Stevens & Navlakha 2017 (el código del cuerpo de hongos ES un hash sensible a la localidad: colisionar es su diseño) · Lin et al. 2014 (menos dispersión en las Kenyon = peor discriminación de olores parecidos) · Rescorla 1976 (elementos comunes: extinguir lo parecido resta miedo al CS) · Whitehead & Ballard 1991 (aliasing perceptual) · Lovibond et al. 2009 (evitar protege de la extinción) · Dasgupta et al. 2018 (filtro de Bloom: la colisión da "familiar" falso) | Todo el fenómeno: colisión de códigos dispersos, generalización del valor y de la extinción por elementos compartidos, miedo a medias = punto fijo de Rescorla-Wagner con refuerzo parcial, evitación que impide corregir, y el falso positivo de una puerta de familiaridad | Los números de este mundo (9 % con 4 estímulos, 85 % con 20 patrones; −1.45 contra −3.0; ×7; muertes) y la comprobación de que no depende de la necesidad (trivial una vez visto el mecanismo) | **ya existe** |
| **1b. Reparación** ("una celda consolidada que recibe R = 0 bajo una retina distinta divide; la hija nace sin valor, la madre no se mueve"; inerte en el tronco) | McCallum 1993 (distinciones útiles: partir un estado sólo cuando ayuda a predecir la utilidad) · Carpenter, Grossberg & Reynolds 1991 (ARTMAP: el error de predicción sube la vigilancia y compromete un nodo nuevo; el viejo queda intacto — ya citado en NOTA_v11) · Marsland et al. 2002 (crece cuando la entrada no encaja) · Clelland 2009 / Sahay 2011 / Aimone 2011 (neurogénesis del giro dentado = separación de patrones) | El principio entero: separar la representación cuando el mismo código recibe consecuencias distintas (McCallum) con desajuste de entrada (ART), añadiendo una unidad nueva y dejando la vieja intacta (ARTMAP, neurogénesis) | La regla exacta (valor consolidado + R = 0 + retina distinta → fisión con hija sin valor) y la medida de que **no actúa nunca en el tronco** (identidad 40/40): eso es una comprobación de inercia, no un mecanismo nuevo | **ya existe** (variante de ARTMAP / distinción útil) |
| **2a. Teorema de identificabilidad** (con 8 de 16 patrones, 9 de 15 hipótesis de pares empatan; ninguna regla local elige sin prior; con 14 la regla local llega a 1.000) | Mitchell 1980 (sin sesgo no se elige dentro del espacio de versiones) · Wolpert 1996 (no free lunch) · Fischer & Simon 1992 (las paridades son lineales sobre GF(2): se identifican cuando los ejemplos generan el subespacio) | El enunciado general es de libro de texto: la consistencia con los datos nunca selecciona entre hipótesis empatadas; hace falta un sesgo | Nada conceptual. El "9 de 15" es una cuenta del espacio de versiones para ESTE conjunto de entrenamiento (correcta, pero no un teorema sobre XOR); el "14" es un número de este mundo | **ya existe** |
| **2b. Prior de pares** (15 celdas, una por par de píxeles, 4 casillas por combinación) | Whitlow & Wagner 1972 (unique cue: XOR = negative patterning A+, B+, AB− se resuelve con un rasgo por par) · Deisig et al. 2001 (abejas lo hacen; el unique cue es el modelo que mejor ajusta) · Gluck & Bower 1988, Gluck 1991 (modelo configural-cue: rasgos elementales + TODAS las conjunciones por pares + regla delta) · Sutton 1996 (tile coding: una tabla por par de dimensiones) | La estructura de M3 sin la escritura de un golpe: un rasgo conjuntivo por par, con tabla por combinación (tile coding) o con regla delta (configural-cue) | La lectura por celda de menor error propio (argmin) en vez de sumar tilings; y la abstención por casilla no vista | **ya existe** (la estructura); la lectura argmin es un detalle |
| **2c. Memoria de un golpe por combinación** (escritura de un golpe, EMA de error propio, argmin, abstención; XOR 1.000 con 8 ejemplos en 7–10 exposiciones) | Bittner et al. 2017 y Milstein et al. 2021 (BTSP: un ensayo crea la traza) · Wu & Maass 2025 (memoria direccionable por contenido, sinapsis binarias, un solo disparo) · Lengyel & Dayan 2007, Blundell et al. 2016 (control episódico: tabla de un golpe; gana en pocos datos) · Gershman & Daw 2017 | Escribir de un golpe una tabla indexada por la entrada y leer de ella cuando hay pocos datos: es exactamente el control episódico; el sustrato biológico es BTSP | El ensamblaje concreto (pares + un golpe + error propio + abstención) medido con **n\*** dentro de un organismo con consecuencias, y el número 7–10 con 8 ejemplos. No encuentro ningún trabajo que reporte "XOR de un golpe" en esa forma | **existe en parte** (piezas sí; ensamblaje y n\* no) |
| **2d. No se desdice y deja a la vía rápida sin consolidar** (reversión 0/20; E1 0/20) | Blundell et al. 2016 (MFEC guarda el MÁXIMO retorno: por construcción no baja) → Pritzel et al. 2017 (NEC añade actualización con tasa: la "tabla reescribible" de v15e ya se hizo en 2017) · Kamin 1969 (bloqueo: lo que ya explica el refuerzo bloquea el aprendizaje de lo demás) · McClelland 1995, Kumaran 2016 (CLS: el almacén rápido debe REPASARSE al lento; si no, el lento no aprende) · Ba et al. 2016 (los fast weights DECAEN: por eso pueden revertir) | Las dos fallas son consecuencias conocidas: una tabla sin decaimiento ni sobrescritura no revierte (MFEC → NEC), y un predictor que explica el refuerzo desde la primera mordida bloquea al otro (Kamin dentro de un sistema doble) | Sólo la medida concreta de la interacción (E1 0/20 con conducta 17/20) en este tronco | **ya existe** |
| **3. Valor por necesidad** (dos necesidades, cuatro estímulos: 1.0 contra 0.5 escalar; saciado, el cuello `min(E, Ag)` veta la sal; la tercera necesidad sobra) | Keramati & Gutkin 2014 (RL homeostático: el valor depende del estado interno, el impulso es una norma del vector de déficits) · Cañamero 1997, Avila-García & Cañamero 2004 (dos recursos, la motivación más urgente manda) · Cos et al. 2013 (valor modulado por el estado interno rinde más que recompensa fija) · Sutton et al. 2011 (Horde: una función de valor por pregunta/meta) · Senapati et al. 2019 (moscas: memoria de agua se expresa con sed, de azúcar con hambre) · Krashes 2009 · Cabanac 1971 · Berridge 2004 · Sterling 2012 · Juechems & Summerfield 2019 | Todo: indexar el valor por la necesidad (= poner el estado interno en el estado), que un escalar promedia y falla, que la necesidad activa es el mayor déficit, y que leer el peor de los dos recursos es "la motivación más urgente manda" (Liebig / WTA de motivaciones) | La ablación concreta ESCALAR / BARAJA_CON con supervivencia en un código de Kenyon, el "11 exposiciones", y la comprobación Occam de que una tercera fila no aporta sobre `min` de las dos. Nada conceptual | **ya existe** |
| **4. Método** (medida de reproducción refutada por cláusula previa; ERR-38: instrumento copiado con defaults distintos) | Lehman et al. 2020 (catálogo de proxies de aptitud explotados) · Lehman & Stanley 2011 (objetivos engañosos) · Nosek et al. 2018 (preregistro: separar predicción de posdicción) | Todo (es método sano, no descubrimiento) | — | **ya existe** |

---

## 1. Alias de código y su reparación

**Lo hallado (registro 08:10–09:12).** Con K = 3 celdas ganadoras de 90 sobre una proyección aleatoria de 6 píxeles, dos de
cuatro estímulos reciben el MISMO código en 18/200 semillas (9 %; con 20 patrones, 170/200). Cuando la sal (R = 0) y el veneno
(R = −3) comparten código, la sal hereda el valor (|W| 1.45 contra 0.0) y el veneno paga (−1.45 contra −3.0); la evitación
multiplica ×7 las exposiciones; no hay divisiones (la división de v11 exige signo contrario, y R = 0 no lo da); no depende de
la sed (S-5); la puerta de v13 no lo repara (S-6). Reparación B-5: la división se dispara también cuando una celda consolidada
recibe R = 0 bajo una retina distinta; hija sin valor, madre intacta; 18/18 semillas ALIAS reparadas; inerte en el tronco.

**Precedentes.**

- *La colisión es el diseño del código.* Dasgupta, Stevens & Navlakha (2017), "A neural algorithm for a fundamental computing
  problem", *Science* 358(6364):793–796 — el circuito olfativo de la mosca (expansión aleatoria + k ganadores) es una variante
  de hashing sensible a la localidad: entradas parecidas reciben códigos parecidos "para que lo aprendido con un olor se
  aplique a un olor similar". Con 6 píxeles hay pocos patrones posibles y con K = 3 de 90 el hash tiene poca resolución: que
  dos estímulos colisionen es la propiedad LSH funcionando, y la tasa depende de K y del número de celdas (el canje que el
  propio registro anota: "más celdas por código, K mayor"). Ya citado en `xor_mecanismos_locales_20260917.md`.
- *En biología, el solapamiento de Kenyon produce exactamente esta generalización.* Lin, Bygrave, de Calignon, Lee &
  Miesenböck (2014), "Sparse, decorrelated odor coding in the mushroom body enhances learned odor discrimination", *Nature
  Neuroscience* 17:559–568 — quitar la inhibición que dispersa el código (APL) empeora la discriminación aprendida de olores
  parecidos y no la de olores distintos. Campbell, Honegger et al. (2013), "Imaging a population code for odor identity in the
  Drosophila mushroom body", *J. Neurosci.* 33(25):10568– — las respuestas de la población de Kenyon predicen la agudeza
  conductual entre mezclas cada vez más parecidas. "Cuando dos cosas se parecen tanto que reciben el mismo código, el organismo
  teme a las dos a medias" es lo que estos dos trabajos miden en la mosca.
- *"El veneno pierde la mitad del miedo" es Rescorla-Wagner con elementos comunes.* Rescorla (1976), "Stimulus generalization:
  some predictions from a model of Pavlovian conditioning", *JEP: Animal Behavior Processes* 2:88–96 — presentar sin refuerzo
  un estímulo que comparte elementos con el CS reduce la respuesta al CS. Pearce (1987), "A model for stimulus generalization
  in Pavlovian conditioning", *Psychological Review* 94:61–73 — la versión configural. Con código idéntico todos los elementos
  son comunes y `W` converge al promedio ponderado de las consecuencias (refuerzo parcial): −1.45 es ese punto fijo, no un
  fenómeno.
- *"Como evita el código, nunca corrige".* Lovibond, Mitchell, Minard, Brady & Menzies (2009), "Safety behaviours preserve
  threat beliefs: protection from extinction of human fear conditioning by an avoidance response", *Behaviour Research and
  Therapy* 47(8):716–720 — la respuesta de evitación protege al miedo de la extinción. Es el bucle S-3 (rechazo → nunca llega
  R → el valor no cambia).
- *En RL se llama aliasing perceptual.* Whitehead & Ballard (1991), "Learning to perceive and act by trial and error", *Machine
  Learning* 7:45–83 — cuando la representación interna confunde estados del mundo que exigen respuestas distintas, el
  aprendizaje por refuerzo se desestabiliza.
- *La puerta por evidencia del código "presta" evidencia: falso positivo de filtro de Bloom.* Dasgupta, Sheehan, Stevens &
  Navlakha (2018), "A neural data structure for novelty detection", *PNAS* 115(51):13093–13098 — la misma expansión dispersa,
  usada como detector de novedad, es un filtro de Bloom: una colisión declara "familiar" a lo nuevo. S-6 y "la puerta lo
  empeora" son ese falso positivo.

**Reparación.**

- McCallum (1993), "Overcoming incomplete perception with utile distinction memory", *ICML* pp. 190–196 — se parte un estado
  **sólo cuando la partición ayuda a predecir la utilidad**: el mismo código con consecuencias estadísticamente distintas se
  divide. B-5 es una distinción útil de una sola muestra (valor consolidado ≠ 0 y llega 0).
- Carpenter, Grossberg & Reynolds (1991), "ARTMAP: supervised real-time learning and classification of nonstationary data by a
  self-organizing neural network", *Neural Networks* 4:565–588 — "match tracking": ante un error de predicción la vigilancia
  sube lo mínimo, se resetea la categoría activa y se compromete un nodo nuevo; el viejo queda intacto. B-5 combina las dos
  condiciones de ART: desajuste de entrada (retina distinta) **y** error de predicción (R = 0 contra valor consolidado). Ya
  identificado como precedente de v11 en `NOTA_v11_pattern_separation_20260917.md`; aquí aplica de nuevo.
- Marsland, Shapiro & Nehmzow (2002), "A self-organising network that grows when required", *Neural Networks*
  15(8–9):1041–1058 — crece un nodo cuando la red no puede ajustar la entrada; es la variante sólo por entrada (sin consecuencia).
- Clelland et al. (2009), *Science* 325(5937):210–213; Sahay et al. (2011), *Nature* 472; Aimone, Deng & Gage (2011),
  "Resolving new memories: a critical look at the dentate gyrus, adult neurogenesis, and pattern separation", *Neuron*
  70(4):589–596 — añadir neuronas nuevas separa patrones solapados sin destruir la red vieja: el análogo biológico de "hija
  sin valor, madre intacta". El disparador biológico no es específico de la consecuencia.

**Qué no encuentro en esa forma.** La regla literal (consolidado + R = 0 + retina distinta → fisión con hija sin valor, inerte
cuando R ∈ {+1, −3}) y los números de este mundo. Eso es una implementación particular con su medida de inercia, no un
principio nuevo. **Veredicto: ya existe** (fenómeno y reparación); lo defendible es "un organismo con consecuencias lo
necesitó y la regla no regresiona el tronco" (misma letra que la NOTA_v11 fijó para v11).

---

## 2. XOR con 8 ejemplos

**Lo hallado (registro 07:10–08:46).** (a) Con 8 de 16 patrones de entrenamiento, 9 de 15 rasgos conjuntivos por pares ajustan
con residuo 0 y uno solo generaliza; ningún aprendiz (local, gradiente exacto 0.562, retropropagación 0.531) elige sin prior;
con 14 patrones queda uno y la regla local con competencia llega a 1.000 (n\* = 200). (b) M3: 15 celdas (una por par de
píxeles) × 4 casillas; la primera mordida escribe R de un golpe; error propio por celda (EMA); la vía lenta lee la celda de
menor error; abstención en casillas no vistas; 1.000 en los 12 nunca vistos con 8 ejemplos, n\* = 7 y 10 (dos series);
declarado prior estructural. (c) v15d: la tabla en el tronco conserva la generalización lineal (tras ERR-38) pero no se desdice
tras el cambio de regla (E2 0/20) y, al explicar el refuerzo desde la primera mordida, deja a la vía rápida sin consolidar (E1
0/20).

**2a. Identificabilidad — ya existe.** Mitchell (1980), "The need for biases in learning generalizations", Rutgers
CBM-TR-117 — la consistencia con los ejemplos nunca basta para elegir dentro del espacio de versiones; sin sesgo el aprendiz
es "casi inútil". Wolpert (1996), "The lack of a priori distinctions between learning algorithms", *Neural Computation*
8(7):1341–1390 — sin supuestos, ningún algoritmo generaliza mejor que otro fuera de los datos de entrenamiento. Para la
paridad en concreto: Fischer & Simon (1992), "On learning ring-sum-expansions", *SIAM J. Comput.* 21(1):181–192 — las
paridades son lineales sobre GF(2); se identifican cuando los ejemplos generan el subespacio relevante y no antes. La cuenta
"9 de 15" es el tamaño del espacio de versiones para ese conjunto de 8 patrones: correcta, útil como control (así se usó en
ERR-35), pero no es un teorema sobre XOR sino sobre esa muestra. La frase del registro "con 8 no lo aprende nadie" es la de
Mitchell 1980 con números.

**2b. Prior de pares — ya existe, con nombre desde 1972.** En aprendizaje animal XOR se llama *negative patterning* (A+, B+,
AB−). Whitlow & Wagner (1972), "Negative patterning in classical conditioning: summation of response tendencies to isolable
and configural components", *Psychonomic Science* — hipótesis del *unique cue*: el compuesto activa además un rasgo propio de
la combinación, que aprende con la regla delta. Deisig, Lachnit, Giurfa & Hellstein (2001), "Configural olfactory learning in
honeybees: negative and positive patterning discrimination", *Learning & Memory* 8(2):70– — las abejas resuelven negative
patterning con condicionamiento olfativo, y el unique cue es el modelo que mejor ajusta. En aprendizaje de categorías: Gluck &
Bower (1988), "From conditioning to category learning: an adaptive network model", *JEP: General* 117, y Gluck (1991),
"Stimulus generalization and representation in adaptive network models of category learning", *Psychological Science* 2 —
el modelo *configural-cue* representa cada estímulo por sus rasgos elementales más **todas las conjunciones por pares** y
aprende con la regla delta: son las 15 celdas de M3 sin la escritura de un golpe. En RL: Sutton (1996), "Generalization in
reinforcement learning: successful examples using sparse coarse coding", *NIPS 8* pp. 1038–1044 — *tile coding*: una tabla
por par de dimensiones (con píxeles binarios, 4 casillas por par). Lo que M3 cambia respecto a tile coding es la lectura
(argmin de error propio en vez de suma de tilings) y la abstención; eso es un detalle de lectura, no un mecanismo.

**2c. Memoria de un golpe — existe en parte.** El sustrato: Bittner, Milstein, Grienberger, Romani & Magee (2017),
"Behavioral time scale synaptic plasticity underlies CA1 place fields", *Science* 357(6355):1033–1036 (un ensayo crea el
campo); Milstein et al. (2021), "Bidirectional synaptic plasticity rapidly modifies hippocampal representations", *eLife*
10:e73046 (y lo reescribe en ambas direcciones). El modelo: **Wu & Maass (2025)**, "A simple model for Behavioral Time Scale
Synaptic Plasticity (BTSP) provides content addressable memory with binary synapses and one-shot learning", *Nature
Communications* 16:342 (bioRxiv 2023; corrección 16:1150) — memoria direccionable por contenido con sinapsis binarias y un
solo disparo. **Aviso:** `ENJAMBRE_xor_20260918.md` §1 atribuye este resultado a "Milstein et al. 2024"; no encuentro ese
trabajo; el que existe con ese contenido es Wu & Maass 2025 (§6). En control: Lengyel & Dayan (2007), "Hippocampal
contributions to control: the third way", *NIPS 20* — un controlador episódico (tabla de un golpe) es lo normativo con pocos
datos y ruido inferencial, al principio del aprendizaje; Blundell et al. (2016), "Model-free episodic control",
arXiv:1606.04460 — tabla indexada por estado-acción escrita por episodio; Gershman & Daw (2017), "Reinforcement learning and
episodic memory in humans and animals: an integrative framework", *Annual Review of Psychology* 68 — marco integrado. "El
cuello era el estimador, no la tasa" (ENJAMBRE §1) es la tesis de Lengyel & Dayan 2007. Lo que no encuentro: el ensamblaje
concreto (pares + un golpe + error propio + abstención) medido con *exposiciones hasta asociar* dentro de un organismo con
consecuencias, ni ningún trabajo que reporte "XOR de un golpe con 8 ejemplos" en esa forma (la búsqueda devuelve BTSP y
memorias asociativas, nada específico de XOR).

**2d. Reversión y consolidación — ya existe, y con la solución.** Blundell et al. 2016 guardan el **máximo** retorno por
casilla: por construcción la tabla no baja, y el propio campo lo señaló como su límite en entornos estocásticos y no
estacionarios; Pritzel et al. (2017), "Neural episodic control", *ICML 70* — la casilla se actualiza con una tasa hacia el
último retorno: es la "tabla reescribible" que v15e propone. Que la tabla deje a la vía rápida sin consolidar es bloqueo de
Kamin dentro de un sistema doble: Kamin (1969), "Predictability, surprise, attention, and conditioning", en Campbell & Church
(eds.), *Punishment and Aversive Behavior*, pp. 279–296 — lo que ya predice el refuerzo bloquea el aprendizaje de lo que se
añade. CLS lo tiene como requisito de diseño: McClelland, McNaughton & O'Reilly (1995), *Psychological Review* 102 (ya en
NOTA_v11) y Kumaran, Hassabis & McClelland (2016), "What learning systems do intelligent agents need? Complementary learning
systems theory updated", *TICS* 20:512–534 — el almacén rápido debe **repasar** al lento; si sólo responde, el lento no
aprende. Y Ba, Hinton, Mnih, Leibo & Ionescu (2016), "Using fast weights to attend to the recent past", *NIPS 29* pp.
4338–4346 — los pesos rápidos **decaen**; por eso pueden desdecirse. El fallo de v15d es la ausencia de decaimiento o
sobrescritura, y las dos correcciones (decaer, sobrescribir) están publicadas.

**Veredicto de la línea:** 2a, 2b y 2d **ya existen**; 2c **existe en parte** (todas las piezas están; el ensamblaje con n\* en
un organismo, no). El enunciado "con 8 ejemplos XOR exige un prior de pares y con él bastan 7–10 exposiciones; con 14 no hace
falta prior" es correcto y es un dato de este mundo; como principio es Mitchell 1980 + Whitlow & Wagner 1972 + Lengyel & Dayan 2007.

---

## 3. Mundo vivo: valor por necesidad y cuello de botella

**Lo hallado (registro 07:58–09:16).** Dos necesidades (hambre, sed) con dos muertes, cuatro estímulos, consecuencia
vectorial, valor con **una fila por necesidad** y boca que lee la fila de la necesidad activa (mayor déficit): xor01
necesidad × estímulo = 1.0 (20/20 ×2), tabla 2 × 4 exacta en 11 exposiciones; un valor escalar por celda 0.5; barajar el
contenido lo destruye; sobrevive más (muere 28–41 % menos). Saciado, leer el mínimo de las dos filas (cuello `min(E, Ag)`)
veta la sal (0.80 → 0.001); una tercera necesidad "reproducirse" cuyo cuerpo es `min(E, Ag)` no aporta sobre ese mínimo.

**Precedentes.**

- *El valor depende del estado interno; formalmente, el estado interno es parte del estado.* Keramati & Gutkin (2014),
  "Homeostatic reinforcement learning for integrating reward collection and physiological stability", *eLife* 3:e04811 — la
  recompensa es la reducción de la distancia al punto de ajuste en un espacio de **varias** necesidades; el impulso es una
  norma del vector de déficits (con exponente alto, se acerca al déficit mayor: el cuello). Juechems & Summerfield (2019),
  "Where does value come from?", *TICS* 23:836–850 — revisión: el valor es distancia al estado interno deseado, no lo confiere
  el mundo. Con la necesidad en el índice, "necesidad × estímulo" no es un XOR sino una tabla; el registro lo dice ("se
  resuelve indexando la memoria, no leyendo mejor los píxeles"), y ESCALAR = 0.5 es el promedio de Rescorla-Wagner.
- *Una función de valor por meta.* Sutton, Modayil, Delp, Degris, Pilarski, White & Precup (2011), "Horde: a scalable
  real-time architecture for learning knowledge from unsupervised sensorimotor interaction", *AAMAS* pp. 761–768 — muchas
  funciones de valor independientes, una por pregunta/meta, aprendidas del mismo flujo. "Una fila por necesidad" es una GVF
  por necesidad. Konidaris & Barto (2006), "An adaptive robot motivational system", *SAB 2006* — impulsos como recompensas
  separadas con prioridad adaptable.
- *Dos recursos, la motivación más urgente manda.* Cañamero (1997), "Modeling motivations and emotions as a basis for
  intelligent behavior", *Agents '97* pp. 148–155 — variables homeostáticas; las motivaciones compiten y gana la más urgente
  (= "necesidad activa = mayor déficit", y saciado, "leer la peor de las dos" es la misma regla). Avila-García & Cañamero
  (2004), "Using hormonal feedback to modulate action selection in a competitive scenario", *SAB 2004* pp. 243–252 — el
  problema de dos recursos con selección homeostática. Cos, Cañamero, Hayes & Gillies (2013), "Hedonic value: enhancing
  adaptation for motivated agents", *Adaptive Behavior* 21 — el valor modulado por el estado interno se adapta mejor que una
  recompensa fija: la misma comparación que VIVO contra ESCALAR.
- *Biología: la misma cosa vale distinto según el estado, y la memoria se lee por necesidad.* Cabanac (1971), "Physiological
  role of pleasure", *Science* 173(4002):1103– (aliestesia). Berridge (2004), "Motivation concepts in behavioral
  neuroscience", *Physiology & Behavior* 81(2):179–209. Sterling (2012), "Allostasis: a model of predictive regulation",
  *Physiology & Behavior* 106:5–15. Krashes et al. (2009), "A neural circuit mechanism integrating motivational state with
  memory expression in Drosophila", *Cell* 139(2):416–427 — el hambre (dNPF → dopaminérgicas del cuerpo de hongos) abre la
  expresión de la memoria apetitiva. **Senapati et al. (2019)**, "A neural mechanism for deprivation state-specific
  expression of relevant memories in Drosophila", *Nature Neuroscience* 22(12):2029–2039 — la mosca guarda memoria de agua y
  de azúcar y expresa la que corresponde a su estado (sed → agua, hambre → azúcar), enrutado por leucoquinina sobre las
  dopaminérgicas: es "leer la fila de la necesidad activa" en el mismo circuito que el organismo imita. Ghosh et al. (2016),
  "Neural architecture of hunger-dependent multisensory decision making in C. elegans", *Neuron* 92(5):1049–1062 — el
  hambre cambia el canje amenaza/comida.
- *Reproducción como necesidad en vida artificial.* Yaeger (1994), "Computational genetics, physiology, metabolism, neural
  systems, learning, vision, and behavior or PolyWorld: life in a new context", *Artificial Life III* — la reproducción está
  condicionada por la energía del cuerpo; una "necesidad de reproducirse" es un motivo corriente en ALife y robótica
  motivacional. Que una fila más no aporte sobre leer `min` de las primarias es un resultado Occam local; no lo encuentro
  escrito, pero es pequeño.

**Qué no encuentro en esa forma.** La ablación ESCALAR / BARAJA_CON con supervivencia en un código de Kenyon, el número de 11
exposiciones y el Occam de la tercera fila. Nada conceptual. **Veredicto: ya existe.** Recomiendo cambiar el vocabulario
"resuelve el XOR necesidad × estímulo": lo que se midió es que el estado interno debe estar en el índice de la memoria (RL
homeostático, 2014) y que la mosca lo hace así (2019); llamarlo XOR infla el resultado.

---

## 4. Método (una línea)

Que una medida de aptitud se deje maximizar por conductas que matan es el caso de libro de Goodhart en vida artificial —
Lehman et al. (2020), "The surprising creativity of digital evolution", *Artificial Life* 26(2):274–306 (catálogo de proxies
explotados); Lehman & Stanley (2011), "Abandoning objectives: evolution through the search for novelty alone", *Evolutionary
Computation* 19(2):189–223 (objetivos engañosos) — y escribir la cláusula que mata la medida ANTES de correr es el
preregistro de Nosek et al. (2018), "The preregistration revolution", *PNAS* 115(11):2600–2606; ERR-38 (defaults distintos en
un gemelo copiado) es higiene de instrumento, sin literatura que citar. **Ya existe; es método sano, no descubrimiento.**

---

## 5. Tres líneas honestas

1. **Qué podría publicarse como aporte, y en qué forma.** No hay un mecanismo nuevo. Lo publicable es una **nota técnica con
   código y datos** (no un paper de hallazgo) sobre la línea del alias: "en un código disperso tipo LSH con valor por refuerzo
   y reglas locales, la colisión de códigos produce aliasing con coste medido (miedo −1.45/−3.0, evitación ×7, muertes ×1.8) y
   una distinción útil de una sola muestra (fisión por R = 0) lo repara con identidad bit a bit en el tronco" — su valor es la
   **necesidad medida** del mecanismo y la reproducibilidad (semillas, preregistro, identidad), no el mecanismo. Segundo
   candidato, más pequeño: un **benchmark/dataset** de la línea XOR — "ejemplos y exposiciones hasta asociar" (8/11/14
   patrones × mecanismo × n\*) con la cuenta del espacio de versiones como control — como nota de método. El mundo vivo no
   se publica como hallazgo; es un instrumento.
2. **Qué es redescubrimiento.** El alias = colisión LSH (Dasgupta 2017) + generalización de la extinción por elementos
   comunes (Rescorla 1976) + aliasing perceptual (Whitehead & Ballard 1991) + protección por evitación (Lovibond 2009); su
   reparación = distinción útil (McCallum 1993) / match tracking de ARTMAP (1991) / separación de patrones por neurogénesis.
   XOR con 8 = necesidad de sesgo (Mitchell 1980) + unique cue (Whitlow & Wagner 1972) / configural-cue (Gluck 1991) / tile
   coding (Sutton 1996); la memoria de un golpe = control episódico (Lengyel & Dayan 2007; Blundell 2016) sobre BTSP; que no se
   desdiga = tabla de máximos de MFEC, corregida por NEC (Pritzel 2017); que bloquee a la vía rápida = Kamin 1969 dentro de
   CLS. Valor por necesidad = RL homeostático (Keramati & Gutkin 2014), dos recursos con la motivación más urgente (Cañamero
   1997, 2004) y expresión de memoria por estado de privación en la mosca (Senapati 2019).
3. **Qué no pude verificar.** (i) "Milstein et al. 2024" de `ENJAMBRE_xor_20260918.md` §1 como fuente de la memoria
   direccionable con sinapsis binarias y un disparo: no existe con esa autoría; es Wu & Maass 2025 (*Nat Commun* 16:342). (ii)
   Las demás citas de ENJAMBRE §1 (Caron 2013, Modi 2020, Lipshutz 2023, Bicknell & Häusser 2021, Moldwin 2021, Devaud 2015,
   Hernández-Cano 2021, Hattori 2017, Confavreux 2020, Bacho & Chu 2022, Lindsey & Litwin-Kumar 2020) no las verifiqué hoy:
   quedan fuera de este encargo. (iii) Páginas exactas de Gluck & Bower 1988 (las fichas discrepan), Whitlow & Wagner 1972 y
   Gershman & Daw 2017: cito sin páginas. (iv) Ninguna cita se verificó abriendo el PDF; todas por ficha de editor/PubMed y
   resumen — por la regla de la NOTA_v11, antes de que una entre al registro como cita hay que abrir el PDF.

---

## 6. Citas verificadas hoy (ficha de editor, PubMed o repositorio del autor)

- Aimone, Deng & Gage (2011). Resolving new memories. *Neuron* 70(4):589–596. https://www.cell.com/neuron/fulltext/S0896-6273(11)00391-6
- Avila-García & Cañamero (2004). Using hormonal feedback to modulate action selection in a competitive scenario. *SAB 2004*, 243–252. https://ieeexplore.ieee.org/document/6281998/
- Ba, Hinton, Mnih, Leibo & Ionescu (2016). Using fast weights to attend to the recent past. *NIPS 29*, 4338–4346. https://papers.nips.cc/paper_files/paper/2016/hash/9f44e956e3a2b7b5598c625fcc802c36-Abstract.html
- Berridge (2004). Motivation concepts in behavioral neuroscience. *Physiology & Behavior* 81(2):179–209. https://pubmed.ncbi.nlm.nih.gov/15159167/
- Bittner, Milstein, Grienberger, Romani & Magee (2017). Behavioral time scale synaptic plasticity underlies CA1 place fields. *Science* 357(6355):1033–1036. https://www.science.org/doi/10.1126/science.aan3846
- Blundell et al. (2016). Model-free episodic control. arXiv:1606.04460. https://www.semanticscholar.org/paper/ba378579fb44007db9f02699889721dcd2b5b3a0
- Cabanac (1971). Physiological role of pleasure. *Science* 173(4002):1103–. https://www.science.org/doi/10.1126/science.173.4002.1103
- Campbell, Honegger et al. (2013). Imaging a population code for odor identity in the Drosophila mushroom body. *J. Neurosci.* 33(25):10568–. https://www.jneurosci.org/content/33/25/10568
- Cañamero (1997). Modeling motivations and emotions as a basis for intelligent behavior. *Agents '97*, ACM, 148–155.
- Carpenter, Grossberg & Reynolds (1991). ARTMAP. *Neural Networks* 4:565–588. https://sites.bu.edu/steveg/files/2016/06/CarGroRey1991NN.pdf
- Clelland et al. (2009). A functional role for adult hippocampal neurogenesis in spatial pattern separation. *Science* 325(5937):210–213. https://www.science.org/doi/10.1126/science.1173215
- Cos, Cañamero, Hayes & Gillies (2013). Hedonic value: enhancing adaptation for motivated agents. *Adaptive Behavior* 21. https://journals.sagepub.com/doi/10.1177/1059712313486817
- Dasgupta, Stevens & Navlakha (2017). A neural algorithm for a fundamental computing problem. *Science* 358(6364):793–796. https://www.science.org/doi/10.1126/science.aam9868
- Dasgupta, Sheehan, Stevens & Navlakha (2018). A neural data structure for novelty detection. *PNAS* 115(51):13093–13098. https://www.pnas.org/doi/10.1073/pnas.1814448115
- Deisig, Lachnit, Giurfa & Hellstein (2001). Configural olfactory learning in honeybees: negative and positive patterning discrimination. *Learning & Memory* 8(2):70–. https://learnmem.cshlp.org/content/8/2/70.full.html
- Fischer & Simon (1992). On learning ring-sum-expansions. *SIAM J. Comput.* 21(1):181–192. https://mlanthology.org/colt/1990/fischer1990colt-learning/
- Gershman & Daw (2017). Reinforcement learning and episodic memory in humans and animals: an integrative framework. *Annual Review of Psychology* 68. https://www.annualreviews.org/content/journals/10.1146/annurev-psych-122414-033625
- Ghosh et al. (2016). Neural architecture of hunger-dependent multisensory decision making in C. elegans. *Neuron* 92(5):1049–1062. https://www.cell.com/neuron/fulltext/S0896-6273(16)30780-2
- Gluck & Bower (1988). From conditioning to category learning: an adaptive network model. *JEP: General* 117. · Gluck (1991). Stimulus generalization and representation in adaptive network models of category learning. *Psychological Science* 2. https://journals.sagepub.com/doi/abs/10.1111/j.1467-9280.1991.tb00096.x
- Juechems & Summerfield (2019). Where does value come from? *TICS* 23:836–850. https://www.cell.com/trends/cognitive-sciences/abstract/S1364-6613(19)30200-1
- Kamin (1969). Predictability, surprise, attention, and conditioning. En Campbell & Church (eds.), *Punishment and Aversive Behavior*, Appleton-Century-Crofts, 279–296.
- Keramati & Gutkin (2014). Homeostatic reinforcement learning for integrating reward collection and physiological stability. *eLife* 3:e04811. https://elifesciences.org/articles/04811
- Konidaris & Barto (2006). An adaptive robot motivational system. *SAB 2006*. https://all.cs.umass.edu/pubs/2006/konidaris_b_SAB06.pdf
- Krashes et al. (2009). A neural circuit mechanism integrating motivational state with memory expression in Drosophila. *Cell* 139(2):416–427. https://www.cell.com/fulltext/S0092-8674(09)01105-2
- Kumaran, Hassabis & McClelland (2016). What learning systems do intelligent agents need? *TICS* 20:512–534. https://pubmed.ncbi.nlm.nih.gov/27315762/
- Lehman & Stanley (2011). Abandoning objectives. *Evolutionary Computation* 19(2):189–223. https://direct.mit.edu/evco/article-abstract/19/2/189/1365/
- Lehman et al. (2020). The surprising creativity of digital evolution. *Artificial Life* 26(2):274–306. https://direct.mit.edu/artl/article/26/2/274/93255/
- Lengyel & Dayan (2007). Hippocampal contributions to control: the third way. *NIPS 20*. https://papers.nips.cc/paper/3311-hippocampal-contributions-to-control-the-third-way
- Lin, Bygrave, de Calignon, Lee & Miesenböck (2014). Sparse, decorrelated odor coding in the mushroom body enhances learned odor discrimination. *Nature Neuroscience* 17:559–568. https://www.nature.com/articles/nn.3660
- Lovibond, Mitchell, Minard, Brady & Menzies (2009). Safety behaviours preserve threat beliefs. *Behaviour Research and Therapy* 47(8):716–720. https://pubmed.ncbi.nlm.nih.gov/19457472/
- Marsland, Shapiro & Nehmzow (2002). A self-organising network that grows when required. *Neural Networks* 15(8–9):1041–1058. https://homepages.ecs.vuw.ac.nz/~marslast/PUBS/NN02.pdf
- McCallum (1993). Overcoming incomplete perception with utile distinction memory. *ICML*, 190–196. https://mlanthology.org/icml/1993/mccallum1993icml-overcoming/
- McClelland, McNaughton & O'Reilly (1995). Why there are complementary learning systems in the hippocampus and neocortex. *Psychological Review* 102. https://stanford.edu/~jlmcc/papers/McCMcNaughtonOReilly95.pdf (ya en NOTA_v11)
- Milstein et al. (2021). Bidirectional synaptic plasticity rapidly modifies hippocampal representations. *eLife* 10:e73046. https://elifesciences.org/articles/73046
- Mitchell (1980). The need for biases in learning generalizations. Rutgers CBM-TR-117. https://www.cs.utexas.edu/~shivaram/readings/b2hd-Mitchell1980.html
- Nosek et al. (2018). The preregistration revolution. *PNAS* 115(11):2600–2606. https://www.pnas.org/doi/10.1073/pnas.1708274114
- Pearce (1987). A model for stimulus generalization in Pavlovian conditioning. *Psychological Review* 94:61–73. https://pubmed.ncbi.nlm.nih.gov/3823305/
- Pritzel et al. (2017). Neural episodic control. *ICML 70*. https://dl.acm.org/doi/10.5555/3305890.3305973
- Rescorla (1976). Stimulus generalization: some predictions from a model of Pavlovian conditioning. *JEP: Animal Behavior Processes* 2:88–96. https://pubmed.ncbi.nlm.nih.gov/1249526/
- Sahay et al. (2011). Increasing adult hippocampal neurogenesis is sufficient to improve pattern separation. *Nature* 472. https://www.nature.com/articles/nature09817
- Senapati et al. (2019). A neural mechanism for deprivation state-specific expression of relevant memories in Drosophila. *Nature Neuroscience* 22(12):2029–2039. https://www.nature.com/articles/s41593-019-0515-z
- Sterling (2012). Allostasis: a model of predictive regulation. *Physiology & Behavior* 106:5–15. https://pubmed.ncbi.nlm.nih.gov/21684297/
- Sutton (1996). Generalization in reinforcement learning: successful examples using sparse coarse coding. *NIPS 8*, 1038–1044. https://papers.nips.cc/paper/1109-generalization-in-reinforcement-learning-successful-examples-using-sparse-coarse-coding.pdf
- Sutton, Modayil, Delp, Degris, Pilarski, White & Precup (2011). Horde. *AAMAS*, 761–768. https://dl.acm.org/doi/10.5555/2031678.2031726
- Whitehead & Ballard (1991). Learning to perceive and act by trial and error. *Machine Learning* 7:45–83. https://link.springer.com/article/10.1007/BF00058926
- Whitlow & Wagner (1972). Negative patterning in classical conditioning: summation of response tendencies to isolable and configural components. *Psychonomic Science*.
- Wolpert (1996). The lack of a priori distinctions between learning algorithms. *Neural Computation* 8(7):1341–1390. https://direct.mit.edu/neco/article/8/7/1341/6016/
- Wu & Maass (2025). A simple model for BTSP provides content addressable memory with binary synapses and one-shot learning. *Nature Communications* 16:342 (corrección 16:1150). https://www.nature.com/articles/s41467-024-55563-6
- Yaeger (1994). PolyWorld: life in a new context. *Artificial Life III*. https://shinyverse.org/larryy/Polyworld.html
