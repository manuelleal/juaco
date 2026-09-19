# HIPÓTESIS LATERAL — JUACO como exoesqueleto cognitivo externo de un agente LLM (18 sep 2026, 21:00)

**Estado: línea lateral, SIMULACIÓN. No toca la escalera del proyecto (fases 3–11) ni el tronco. Se corre cuando la fase 5 y el
linaje mortal (H-1) estén cerrados, o cuando el director lo pida. Nada de aquí entra al registro de resultados hasta que pase por el
método (preregistro, controles, réplica).**

## 1. Pregunta (del director)
¿Existe un mecanismo técnicamente plausible para usar JUACO como capa externa que aumente la capacidad adaptativa de un agente LLM
con los pesos congelados (GPT, Claude, Qwen, Llama…), sin fine-tuning, de modo que el agente recuerde lo importante, detecte errores
inesperados, aprenda de ellos, consolide, recupere lo relevante, deje de repetir errores, adapte estrategias, conserve continuidad
entre sesiones, descarte lo obsoleto y transfiera conocimiento a otros agentes? Y: ¿lo mismo aplicado a machine learning clásico?

## 2. Respuesta honesta del coordinador
Sí hay un mecanismo, y es estrecho: con pesos congelados lo único que cambia la conducta del LLM es el contexto; por tanto "aprender"
sólo puede vivir en la capa que decide **qué entra al contexto, con qué valor, cuándo se sobrescribe y cuándo se olvida**. Eso es
exactamente lo que JUACO hace con la boca: valor por estímulo escrito sólo con consecuencia, escritura de un golpe ante sorpresa
(memoria de pares de v15f), relevo entre memoria y regla general, reversión cuando el mundo cambia, olvido por error propio, y mensaje
con referencia entre organismos (bloques 4/4b/5). RAG no tiene nada de eso: guarda texto y devuelve lo parecido.

## 3. Arquitectura mínima (qué entra y sale de cada componente)
1. **LLM → controlador JUACO:** la situación (tarea, familia de tarea), la acción propuesta y la PREDICCIÓN del LLM del resultado.
2. **Controlador → herramientas/mundo:** ejecuta la acción; el mundo devuelve el resultado con una consecuencia VERIFICABLE (éxito,
   fallo, coste). Sin consecuencia verificable no hay valor y la capa no puede aprender: primera condición del sistema.
3. **Actualización JUACO (reglas locales, sin gradiente):** sorpresa = resultado − predicción; si la sorpresa es grande, escribe un
   episodio de un golpe (familia, acción, resultado, valor); el valor de la familia (semántico) se mueve despacio (regla delta local);
   una contradicción sobrescribe (reversión); los episodios con error propio alto se olvidan; el valor por "necesidad" = objetivo
   activo del agente.
4. **JUACO → siguiente contexto del LLM:** no texto crudo: **tres piezas seleccionadas por valor, tamaño fijo**: la advertencia con más
   valor negativo para esta familia ("en esta clase de tarea X falló por Y"), el ejemplo con más valor positivo, y la estrategia
   vigente de la familia con su confianza. Es la boca: decide qué ve el razonador.
5. **Entre agentes:** el mensaje del bloque 4: (familia, resultado, valor) se escribe en la tabla del receptor como exposición sin
   consecuencia; el receptor actúa sin haberlo vivido.
Reparto: el LLM razona, planifica y genera; JUACO decide qué recordar, cuánto vale, cuándo revertir y qué olvidar. JUACO no inventa
estrategias: el LLM las propone y JUACO las puntúa por consecuencia.

## 4. Dónde se rompe (y cómo se mide)
- Sin consecuencia verificable en las tareas → no hay valor → la capa es RAG con otro nombre. Medida: fracción de episodios con
  consecuencia.
- El LLM ignora el contexto → medida: tasa de errores repetidos CON la advertencia presente.
- Memoria contra aprendizaje → se distingue como en el mundo de familias: aprendizaje = acertar en la VARIANTE NUEVA de una tarea
  sin recuperar texto de ella, y desdecirse cuando la estrategia vieja deja de funcionar. Si RAG y JUACO empatan en variantes nuevas
  y tras el cambio, JUACO no aporta.
- Estrategia nueva: no la produce JUACO; la produce el LLM. JUACO sólo la sube o baja por consecuencia.
- Generalizar sin pesos: sólo por familia (como el mensaje de familia del bloque 5); la variante exige la firma de variante (bloque 6).

## 5. Experimento pequeño (preregistrable)
Tres brazos: A = LLM solo; B = LLM + RAG convencional; C = LLM + JUACO. Cinco días de tareas con consecuencia verificable:
día 1 el agente comete un error; día 2 situación relacionada; día 3 variante distinta; día 4 el entorno cambia (la estrategia vieja
deja de funcionar); día 5 debe recuperar la experiencia relevante. Semillas = conjuntos de tareas; mismo LLM congelado en los tres.
**Métricas:** errores repetidos; acierto en variantes nuevas; días hasta abandonar la estrategia vieja tras el cambio; retención;
recuperación correcta; obsoletos eliminados; tokens; latencia; coste; experiencias necesarias para aprender.
**Predicción escrita antes:** C > B sólo en variantes nuevas y tras el cambio; en recuperación literal, B ≈ C; A peor en todo menos
tokens. **Refuta:** C ≈ B en variantes y tras el cambio. Control: C con la tabla barajada (etiquetas de acción permutadas) ≈ B.

## 6. Machine learning clásico
Ahí el modelo sí aprende de datos: la capa JUACO decidiría QUÉ ejemplos entran a entrenar y con qué peso (currículo por sorpresa:
sólo lo mal predicho escribe; lo contradicho se sobrescribe; lo redundante se olvida). Existe en parte (aprendizaje activo, replay
priorizado, aprendizaje continuo); el aporte sería la combinación local y el control barajado, no el principio.

## 7. Relación con la misión
Si funciona, financia la evolución del organismo (el director: "si tenemos plata, la evolución de la célula puede ser cada vez
mejor"). Orden: primero fase 5 y linaje mortal; después este experimento en pequeño; nada se declara sin réplica.
