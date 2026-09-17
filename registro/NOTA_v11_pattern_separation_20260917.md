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
