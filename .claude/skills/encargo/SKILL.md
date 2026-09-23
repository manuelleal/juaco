---
name: encargo
description: Arma el encargo a un agente del equipo JUACO (juaco-creador, juaco-auditor, juaco-cronista, juaco-compilador, probador-haiku, explorador-haiku) con misión, contrato, modelo por dificultad y entregable. Úsala cuando haya que delegar trabajo a un agente o cuando Christiam diga "manda un agente", "que lo haga un Opus/Sonnet/Haiku", /encargo <rol> <tarea>.
---

Rol y tarea: $ARGUMENTS

Elegir el agente por dificultad (memoria `juaco-exo-equipos`): Opus = diseño y algoritmos difíciles (`juaco-creador`, `juaco-compilador`); Sonnet = auditoría y crónica (`juaco-auditor`, `juaco-cronista`); Haiku = pruebas y preguntas cortas (`probador-haiku`, `explorador-haiku`). Pocos agentes a la vez; cada uno en su directorio.

Plantilla del prompt (todas las líneas, en este orden):
1. **Misión** (primera frase, obligatoria, regla 13 de EQUIPO.md): "Llegar a la AGI por este camino (organismo mínimo con reglas locales, sin retropropagación, peldaños preregistrados con controles y réplicas); el método manda sobre el cómo."
2. **Contexto mínimo**: archivos a leer primero (2 a 4), tronco vigente, ERR recientes que le atañen.
3. **Contrato**: qué entrega exactamente (archivos, formato, informe de máximo una página), en qué carpeta, y qué NO puede hacer (Pool, commits, matar procesos, tocar congelados).
4. **Criterio de aceptación** verificable: identidad N/N, humo que escribe JSON, predicción numérica con rango, control que puede fallar.
5. **Presupuesto**: tiempo, semillas, pasos.
6. **Cierre**: "Declara tus propias predicciones refutadas y lo que no pudiste verificar."

Después de recibir el trabajo: auditar a mano los números (o con `juaco-auditor` en solo lectura) antes de darlo por bueno; los agentes externos no se dan por buenos nunca. Reportar al director con la skill `veredicto`.
