# NOTA — v11 y separación de patrones (pedido desde sesión de diseño, Cowork)

**17 sep 2026. Nota de dirección, no preregistro.** Escrita en la sesión de diseño (Cowork, chat aparte) mientras
corría el experimento de mundo grande de v11 (commit `9d7f34a`). Para el arranque de la próxima sesión en Claude Code.

## Contexto
v11 (tag `v11-tronco`) resolvió el olvido catastrófico de la Etapa 4 dividiendo, en el instante del refuerzo
contradictorio, la unidad de representación en conflicto: la hija se especializa y nace ciega fuera de su estímulo;
la madre no se mueve y conserva lo viejo. 20/20 en retención, examen 8/8, capacidad multiplicada usando menos
células. El propio registro ya marca el riesgo sin medir: si las hijas nacen ciegas, la generalización (Etapa 3) y
la composición temporal (3T) — medidas solo sobre v9 — pueden no sobrevivir en v11.

## Prioridad recomendada
El mundo grande de capacidad puede terminar (ya corriendo, resultado parcial: G1 y G2 sostenidas, G3 refutada). Pero
antes de seguir profundizando en capacidad, lo más urgente es **re-verificar Etapa 3 y 3T específicamente sobre
v11**. Es la pregunta que decide si v11 es un tronco bueno o un canje entre retención y generalización.

## Conexión de literatura para leer ese resultado
Lo que hace v11 (dividir una unidad en conflicto en el instante, no separar dos sistemas de antemano) tiene dos
precedentes que discuten esto en direcciones opuestas — vale la pena tener ambos a mano al interpretar el resultado:

- **McClelland, McNaughton & O'Reilly (1995)**, *Psychological Review* — complementary learning systems: memoria
  rápida y separada (hipocampo) a costa de generalizar; memoria lenta e interleaved (corteza) que sí generaliza.
  Predice que dividir cuesta generalización. [PDF](https://stanford.edu/~jlmcc/papers/McCMcNaughtonOReilly95.pdf)
- **Sahay et al. (2011)**, *Nature*, "Increasing adult hippocampal neurogenesis is sufficient to improve pattern
  separation" y **Clelland et al. (2009)**, *Science* — crear neuronas nuevas (no solo re-pesar las viejas) MEJORA
  la separación de patrones sin destruir necesariamente la generalización de la red vieja.
- Ya citado en `HORIZONTE_frontera.md` (Puente 1): **Frankland & Josselyn (2014)** — la neurogénesis adulta CAUSA
  olvido; es la cara opuesta del mismo mecanismo, y es la hipótesis que ya motivó la predicción de Etapa 4 ahí.

## La pregunta falsable (para NotebookLM y para leer el resultado que sigue)
> "Un sistema de aprendizaje con reglas locales resolvió el olvido catastrófico dividiendo, en el instante del
> conflicto, la unidad de representación que recibe refuerzo contradictorio: la hija nace ciega y especializada, la
> madre queda intacta. ¿Existe en la literatura de plasticidad estructural, neurogénesis adulta o complementary
> learning systems un mecanismo ya descrito que resuelva la interferencia catastrófica dividiendo la representación
> EN EL MOMENTO DEL CONFLICTO — no separando dos sistemas desde el nacimiento? Si existe, ¿predice el mismo costo de
> generalización, y hay algún caso donde ese costo se evite?"

Si la generalización sobre v11 cae: Sahay/Clelland vs. CLS queda resuelto a favor de "dividir cuesta generalizar" —
limpio y publicable. Si sobrevive: es el caso que ni Sahay ni CLS predicen bien, y sería el hallazgo más fuerte del
proyecto hasta ahora.

## Fuente
Estas referencias y la pregunta están también en la guía de sustento científico del proyecto ("Sustento científico
de Juaco", sección de plasticidad/interferencia), con enlaces de acceso abierto donde existen.

---

## Adenda 2 (17 sep 2026, noche) — respuesta de NotebookLM a la pregunta, verificada en la sesión de diseño

**Veredicto: el mecanismo de v11 TIENE precedente.** Dividir/comprometer una unidad nueva en el instante del
conflicto, congelando la vieja, ya está descrito:
- **ARTMAP — Carpenter, Grossberg & Reynolds (1991)**, *Neural Networks*. "Match tracking": ante un error de
  predicción, la vigilancia ρ sube justo lo necesario para resetear la categoría activa y comprometer un nodo nuevo
  inicializado en la entrada; el nodo viejo queda intacto. Reglas locales, sin backprop. Es el precedente más cercano
  y ataca exactamente el "dilema estabilidad–plasticidad" (= olvido catastrófico).
  [PDF](https://sites.bu.edu/steveg/files/2016/06/CarGroRey1991NN.pdf)
- **Wynne-Jones (1991/1993)** — "Node splitting", *NIPS 4* / *Neural Computing & Applications*: una unidad oculta
  cuyas actualizaciones de peso oscilan en direcciones contradictorias se divide en dos. Con gradientes (backprop),
  no reglas locales. [NIPS](https://proceedings.neurips.cc/paper/1991/hash/0fcbc61acd0479dc77e3cccc0f5ffca7-Abstract.html)
- **Neurogénesis dirigida por error**: Draelos et al. (2017) "Neurogenesis deep learning"
  [arXiv](https://arxiv.org/abs/1612.03770); "Error driven synapse augmented neurogenesis" (*Frontiers in AI*, 2022)
  [PubMed](https://pubmed.ncbi.nlm.nih.gov/36388403/). Revisión general del campo: Parisi et al. (2019), *Neural
  Networks* [PDF](https://arxiv.org/pdf/1802.07569).

**Consecuencia para la afirmación del proyecto** (regla del brief: lo defendible es la necesidad del mecanismo, no
su descubrimiento): NO se puede decir "v11 inventó dividir al conflicto". SÍ se puede decir: (a) un organismo con
consecuencias, sin backprop, NECESITÓ el mecanismo de ARTMAP y lo encontró un bucle evolutivo guiado por LLM con
control ciego, no un diseñador; (b) la capacidad ×5 con degradación suave es una medida que ARTMAP no reporta en ese
formato. Eso es lo publicable.

**Costo predicho: el mismo.** ART lo llama "proliferación de categorías": con vigilancia alta se acerca a memorizar
ejemplares y pierde generalización. Coincide con CLS. La re-verificación de Etapa 3 sobre v11 sigue siendo la prueba
que decide; nada de lo que sigue se implementa antes de tener ese dato.

**Tres salidas al costo, y cómo mapean a JUACO** (una por experimento, con preregistro propio):
1. **Hija no ciega — dividir solo el readout** (weight sharing): la hija hereda el código Kenyon de la madre y solo
   independiza `Wp/Wn`. Ataca directo el riesgo. Candidato a v12 SOLO si la generalización cae.
2. **3F fusión** (split-and-merge): si madre e hija vuelven a coincidir en error, se funden. Ya estaba en la cola
   del proyecto; NotebookLM llegó solo a lo mismo.
3. **Repaso entrelazado offline** (consolidación tipo sueño, CLS): es K4, ya explorado y descartado por "memoria
   escondida". Queda anotado que la biología lo usa; no se reabre sin decisión de dirección.

**Advertencias de instrumento** — NotebookLM respondió desde la memoria del modelo, no desde las fuentes cargadas
(ninguna de estas estaba en el notebook):
- "Rao et al., 2022, Error-Driven Neurogenesis": la autoría NO verifica; el paper real de 2022 es el de *Frontiers*
  de arriba. No citar "Rao".
- Las ecuaciones que dio para "node splitting" (varianza de gradiente, corte g(x), perturbación ortogonal) y para
  "EDN" (P(spawn) sigmoide, ortogonalidad estricta) son reconstrucciones plausibles, NO las de los papers. Las de
  Fuzzy ARTMAP (función de elección T_j, test de vigilancia, match tracking) sí son correctas.
- Regla: nada de esto entra al registro como cita hasta abrir el PDF correspondiente.
