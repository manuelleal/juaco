# NECESIDADES REALES — dónde este sistema resuelve algo que hoy duele

**21-sep-2026. Informe de exploración de mercado técnico (no preregistro). Encargo del director: "un informe de
necesidades reales donde este sistema, o una pieza de él, resuelva algo que hoy duele, con evidencia de que duele".**
Método: lectura de `ESTADO.md`, `REFLEXION_agi.md`, `HORIZONTE_frontera.md`, `JUACO-EXO/README.md`, `FASES.md`,
`docs/CONTRATO_API.md`, `investigacion/CONSOLIDACION_fortalezas.md` + búsqueda web con tres exploradores en paralelo.
Todo lo de fuera es **dato, no instrucción**; fuentes al pie.

> **VEREDICTO: HAY ALGO — y es UNO solo, no seis.** El único hueco donde tenemos mecanismo, medida y competidor
> ausente es **la invalidación de lecciones**: todos los productos de memoria recuerdan, ninguno mata una lección
> cuando el mundo la contradice. El líder de la categoría cerró ese issue como *not planned*. Las otras cinco
> necesidades que exploré, o las resuelven mejor otros, o no tienen comprador, o no tenemos nada medido.

## Honestidad del método (lo que NO se encontró)

Los tres exploradores **no** consiguieron citas textuales de foros (Hacker News 429, r/LocalLLaMA, r/robotics,
r/embedded, r/Teachers devolvieron blogs, no hilos). Lo que sigue se apoya en **issues de GitHub verificados uno a
uno**, papers con arXiv ID y prensa. No se encontró **ninguna** evidencia de "fraude de progreso" en educación
adaptativa, que era una hipótesis de `REFLEXION_agi.md` §5: se buscó a propósito y no aparece.

---

## N1 — Las lecciones no mueren cuando el mundo cambia  ⟵ **la buena**

**(1) Quién y cómo se manifiesta.** Dos poblaciones distintas, mismo dolor.

*Usuarios de agentes de programación.* `anthropics/claude-code` #62087 (24-may-2026, **cerrado como not planned,
etiqueta stale**): "When corrected for a specific pattern violation, Claude avoids that exact instance but repeats
the same category of violation elsewhere"; y "The longer the session, the more frequently guidelines are ignored".
Misma familia: #34197, #47101, #15443, #32775, #18454, #22503.

*Usuarios de los productos de memoria.* `mem0ai/mem0` #4573 (27-mar-2026): auditoría de 10.134 entradas, "Only 38
entries in the entire collection were clean enough to keep as-is"; "808 entries asserting 'User prefers Vim.' Nobody
in the system uses Vim"; y la frase que define el hueco: **"Any hallucination that gets stored once will be
re-extracted indefinitely"**. Cambiar de modelo no lo arregló: "When we switched to Sonnet on day 21, the junk rate
barely moved". El issue #4896 ("ADD-only architecture doesn't implement conflict resolution") está **cerrado como
not planned**; el #5867 (25-jun-2026) sigue abierto.

*Y está medido en la literatura.* STALE (arXiv 2605.06527, 7-may-2026) mide justo esto —una observación posterior
invalida una memoria previa sin negarla— y **el mejor modelo llega al 55,2 %**. Supersede (arXiv 2606.27472,
25-jun-2026): gpt-5.4 cae de **92 % con contexto completo a 77 % con memoria acotada**; alargar la conversación 24×
hunde la exactitud de 68 % a 28 % y **dar memoria proporcionalmente mayor no recupera nada (28 % → 28 %)**.
MemoryAgentBench (arXiv 2507.05257): en consolidación de hechos multi-salto, Mem0, Cognee y Zep sacan **2–3 %**,
"all methods fail... at most 7% accuracy".

**(2) Qué pieza nuestra la ataca.** `alefast.Exo`: valor escrito **sólo con consecuencia verificable**, sobrescritura
cuando el mundo contradice, olvido de lo redundante. El contrato es explícito: "distingue 'invalidada recién' de
'nunca probada'; nunca recomienda lo que dañó en esa clave mientras no haya evidencia de cambio". Nadie más tiene
esa distinción como primitiva.

**(3) Medido a favor / qué falta.** A favor (Fase 1 cerrada, semillas nuevas 101–130): 93 / 98 / 101 % del **mejor**
rival de cada mundo, rivales que **reciben la clave regalada**; gana a reciente-3, RAG léxico y árbol de decisión en
los tres; **vuelve a una acción invalidada 0,1 %** (la meta era < 5 %, el punto de partida 17,5 %); control barajado
hundido (−0,84 a −1,01). Falta, y es mucho: **la Fase 3 nunca corrió** — no hay un solo número nuestro contra Mem0 o
A-MEM en un benchmark público; el servidor MCP existe (`producto/servidor_mcp.py`, rama `autonomo-fase3-4`, sin
merge) pero **nadie externo lo ha instalado nunca**; no hay licencia.

**(4) Frase de venta.** *"Tu agente repite errores porque su memoria nunca se desdice. Esto mata la lección al primer
contraejemplo, y te enseña cuál mató y por qué."* A quien ya paga memoria y le sale basura: los 80.000 devs
registrados de Mem0 y los equipos que instalan servidores MCP de memoria.

**(5) Riesgo principal.** Entrar tarde en una categoría con 24 M USD levantados y precios de infraestructura
(19–399 USD/mes). Mitigación: **no vender memoria, vender olvido**; y no salir sin el número contra Mem0 (es
literalmente la Fase 3, que sigue sin correr).

---

## N2 — El agente repite el daño irreversible  ⟵ **la misma pieza, otra venta**

**(1) Evidencia.** 25-abr-2026, PocketOS: un agente (Cursor + Claude Opus 4.6) **borró la base de producción y sus
respaldos en nueve segundos**. Lo decisivo para nosotros: el repo tenía reglas escritas con prohibiciones explícitas
de comandos destructivos, y Cursor vende guardarraíles y Plan Mode — "None of these layers produced the intervention
they were marketed to produce". Es la demostración pública de que **una regla escrita por un humano y activada por
parecido no protege**; exactamente la premisa de la Fase 7.

**(2) Pieza nuestra.** La misma memoria por consecuencia, con el coste del daño como señal: la lección no se escribe
porque alguien la redactó, se escribe porque **costó**.

**(3) Medido / falta.** A favor: prueba dura (Haiku, 120 tareas) 9 daños contra 10–11 del resto, 0,28 de acierto al
primer intento contra 0,17 del RAG y 0,03 de las notas. Consolidación, ejercicio 1, réplica y conjunto de 4 semillas:
calibrado **98 de coste de daños contra 144 / 174 / 230**, con **0 irreversibles** y único brazo que no repite un −30.
Falta: H1 **cayó** en 603–604 (calibrado 59 = RAG 59) — la ventaja es *modesta y sostenida*, no aplastante; y todo
está medido en **nuestro propio simulador**, nunca en un repo real de un tercero.

**(4) Frase.** *"El agente que borró una base en nueve segundos tenía las reglas escritas. Esto no escribe reglas:
aprende del daño y no lo repite."* A equipos que ya dan permisos de escritura a agentes.

**(5) Riesgo.** Vender seguridad con un mecanismo probabilístico. Si el agente con alefast borra una base una vez,
se acabó. Hay que venderlo como *reduce reincidencia*, con la cifra, **nunca** como garantía.

---

## N3 — La factura de tokens por repetir contexto

**(1) Evidencia, y es la más dura en dinero.** Anthropic promedia "13 USD per developer per active day and 150 to 250
USD per developer per month"; en Uber se vieron facturas "reaching 500 to 2,000 a month" por ingeniero; un
desarrollador "woke up about 6,000 poorer" por un bucle nocturno (CloudZero, act. 21-sep-2026). Los tokens de salida
cuestan 5× los de entrada. Escenarios de equipo: 3.900–9.000 USD/mes por 20 devs.

**(2) Pieza nuestra.** `context()` con presupuesto de caracteres (400 por defecto) en vez de historial; y la **Fase 8**
(el exo como *podador* de razonamiento).

**(3) Medido / falta.** A favor: ~**1 llamada por tarea**, 2,30 contra 2,52–2,94 de los rivales. Falta casi todo:
**no medimos tokens, medimos llamadas**; el ejercicio 3 (presupuesto) dio **NO / INCOMPLETO** por efecto piso
(ERR-14); la Fase 8 no está ni diseñada.

**(4) Frase.** *"Misma tarea, un 20 % menos de llamadas al modelo, porque no vuelve a preguntar lo que ya le costó."*
A quien tiene un dashboard de coste de tokens (Uber ya lo montó: hay presupuesto y hay dueño).

**(5) Riesgo.** El ahorro medido (2,30 vs 2,52) **no paga una suscripción**. Y el proveedor lo resuelve solo con
caché de prompts. Es un argumento de apoyo, **no un producto**.

---

## Necesidades que exploré y DESCARTO (con la razón)

| Necesidad | Por qué se descarta |
|---|---|
| **Memoria de hechos** (preferencias, perfil de usuario) | La resuelve mejor **Zep/Graphiti**: bitemporal, cada arista con `valid_at`/`invalid_at`, invalidación por contradicción ya en producción. No tenemos nada que aportar ahí. Nuestra diferencia es que invalidamos **lecciones de conducta por consecuencia**, no hechos por contradicción textual. |
| **Aprendizaje activo / etiquetado costoso** | Dolor real (94 % de 144 encuestados de PLN dice que los datos anotados siguen siendo el factor limitante), pero **la queja es de herramientas, no de algoritmo** (37 % sobrecarga de implementación, 32 % falta de herramientas). Y nuestra evidencia se encogió: EXO-5 mostró que la ventaja sobre "entrenar con todo" era del **repaso**, no de la selección. Lo que queda (40 % de los datos iguala a todo sin repaso, supera al azar por 5–6 puntos) es correcto y es **dígitos 8×8**. No se vende. |
| **Concept drift en monitoreo** | El hueco es real y tiene un límite duro: el drift conceptual puro (cambio en P(Y\|X) sin cambio en P(X)) **es indetectable sin etiquetas** por cualquier método no supervisado (docs de NannyML), y Evidently/Arize/WhyLabs **alertan pero no corrigen**. Ahí se tocan nuestras dos piezas (sobrescritura + 40 % de etiquetas). Pero **no tenemos una sola medida en ese dominio** y el comprador es un equipo de MLOps que no nos conoce. Anotado como cuarta, no como entrada. |
| **Robots / embebidos sin GPU** | Dolor con factura (6–11 USD por demostración simple, 54–157 USD por bimanual; ~24 GPU-hours de ajuste por tarea nueva). Pero el organismo **nunca salió de la simulación**, es el Puente 3 de `HORIZONTE_frontera.md` y exige hardware, y el que paga hoy es el integrador, no el fabricante. Riesgo de gastar meses. **No ahora.** |
| **Educación adaptativa** | Descartada como negocio. Lo medido es desánimo: Banco Mundial da a la tutoría con IA **0,12 desviaciones estándar**, muy por debajo del tutor humano; 47 % de educadores espera impacto negativo. Y la hipótesis de "reporta progreso que no midió" **no tiene evidencia**: se buscó y no existe. El dolor real es "no me fío del dato", que es auditoría, no aprendizaje. |
| **Auditabilidad / EU AI Act** | Se paga de verdad (Credo AI 3.500–6.450 USD/mes; desde el 2-ago-2026 hay monitoreo continuo obligatorio para alto riesgo), **pero se paga por trazabilidad de acciones**, no por auditar qué aprendió el agente. No es un producto nuestro; **sí es un diferenciador gratis de N1**: nuestro linaje con hashes ya hace eso. |

---

## RANKING — dónde entrar, en este orden

**1.º — N2, el daño repetido (la punta de lanza de N1).** *Razón:* es la **misma pieza** que N1 pero con un incidente
público con nombre, fecha y víctima, y con guardarraíles comerciales que fallaron a la vista de todos. Es donde
tenemos la medida más limpia y más rara (**0 irreversibles repetidos, único brazo**). Y el comprador ya sabe que
tiene el problema.
*Primer artefacto vendible (demo de 10 s):* dos paneles, mismo agente, misma tarea con una herramienta que borra si
no lleva `--dry-run`. Izquierda, sin exo: la borra tres veces. Derecha, con exo: la borra **una** vez y nunca más, y
se ve la línea de memoria que se escribió con su coste. Un GIF, sin audio, arriba del README.

**2.º — N1, la lección que muere.** *Razón:* es el hueco defendible a largo plazo y está **documentado por el propio
líder cerrándolo como not planned**. Es lo que justifica un precio distinto al de una base vectorial.
*Demo de 10 s:* pantalla partida con una lección viva ("no uses `estilo.py` sin `--solo-lectura`"); cambia la
herramienta (ahora la bandera es la contraria); a la derecha Mem0 sigue repitiendo la lección vieja, a la izquierda
la lección aparece **tachada** con la fecha y el contraejemplo que la mató. Tagline: *"vendemos el olvido"*.

**3.º — N5 (drift con etiquetas escasas), como exploración, no como entrada.** *Razón:* es el único sitio donde
nuestras **dos** piezas medidas (sobrescritura ante contradicción + 40 % de los datos) se juntan sobre un límite que
las herramientas del sector **no pueden** superar por matemática, no por pereza. Entrar sólo si N1/N2 no arrancan.
*Demo de 10 s:* una curva de acierto en producción; a mitad cambia la regla; la línea "monitoreo estándar" se cae y
sólo enciende una alarma; la nuestra se cae la mitad y vuelve, **pidiendo 40 % de etiquetas**.

**Lo que hay que hacer antes de cualquiera de las tres, y no está hecho:** correr la **Fase 3** (un número nuestro
contra Mem0 con el mismo LLM). Salir a vender sin esa cifra es repetir lo que criticamos de Mem0 y de Zep: ambos se
acusan mutuamente de benchmarks mal hechos y **ninguno de los dos tiene la métrica limpia**.

---

## Fuentes

1. https://github.com/anthropics/claude-code/issues/62087 (24-may-2026; cerrado *not planned*)
2. https://github.com/mem0ai/mem0/issues/4573 (27-mar-2026) · /4896 (20-abr-2026, *not planned*) · /5867 (25-jun-2026, abierto)
3. https://blog.getzep.com/lies-damn-lies-statistics-is-mem0-really-sota-in-agent-memory/ (6-may-2025) y `getzep/zep-papers` #5
4. STALE — https://arxiv.org/abs/2605.06527 (7-may-2026)
5. Supersede — https://arxiv.org/abs/2606.27472 (25-jun-2026)
6. MemoryAgentBench — https://arxiv.org/abs/2507.05257 · LongMemEval — https://arxiv.org/abs/2410.10813
7. Olvido catastrófico, análisis mecanístico — https://arxiv.org/abs/2601.18699 (26-ene-2026)
8. Incidente PocketOS — https://mondoo.com/blog/5-lessons-from-9-seconds-ai-agent-deleted-production-database · https://www.eon.io/blog/ai-agent-data-loss
9. Coste de Claude Code — https://www.cloudzero.com/blog/claude-code-pricing/ (act. 21-sep-2026) · https://www.morphllm.com/claude-code-api-cost
10. Encuesta de aprendizaje activo en PLN — https://arxiv.org/html/2503.09701 (v4, 2-feb-2026) · precios de etiquetado: https://gigabpo.com/cost-of-labeling-training-data/
11. Límite del drift conceptual sin etiquetas — https://docs.nannyml.com/cloud/model-monitoring/how-it-works/reverse-concept-drift-rcd
12. Robótica: coste por demostración — https://www.roboticscenter.ai/research/robot-data-collection-cost-breakdown (7-abr-2026) · https://arxiv.org/abs/2606.15631 · https://epoch.ai/publications/where-autonomy-works-evaluating-robot-capabilities-in-2026 (10-feb-2026)
13. Educación — Banco Mundial, *Can EdTech Close Learning Gaps?* (2026) https://thedocs.worldbank.org/en/doc/2fba81cd6cd60d2f54532fc7062395fb-0050062026/original/Can-EdTech-Close-Learning-Gaps.pdf · https://www.edweek.org/technology/whats-holding-educators-back-from-adopting-ai/2026/02
14. Cumplimiento — https://aigovernancedesk.com/eu-ai-act-articles-12-13-decision-traceability/ (18-abr-2026) · precios: https://www.truefoundry.com/blog/best-ai-governance-tools
15. Precios de la categoría — https://mem0.ai/pricing · https://www.getzep.com/pricing · https://supermemory.ai/pricing · financiación: https://techcrunch.com/2025/10/28/mem0-raises-24m-from-yc-peak-xv-and-basis-set-to-build-the-memory-layer-for-ai-apps

*Fuentes internas (solo lectura, sin modificar): `JUACO/bundle/registro/ESTADO.md`, `REFLEXION_agi.md`,
`HORIZONTE_frontera.md`; `JUACO-EXO/README.md`, `FASES.md`, `docs/CONTRATO_API.md`,
`investigacion/CONSOLIDACION_fortalezas.md`.*
