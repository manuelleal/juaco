# Paso C — Literatura y avaladores (1-oct-2026, solo lectura)

Autor: juaco-investigador, para la sesión "Juaco revisión" (ruta de publicación). La sesión "Investigación y exploración" NO reabrió los enlaces: el estado VERIFICADO es el que reporta el investigador. El `.bib` está en `referencias_pasoC.bib`, misma carpeta.

**VEREDICTO: FUNCIONA, con salvedades.** 24 referencias con título y autores comprobados contra una página abierta hoy; 0 quedan PENDIENTE en título y autores. Quedan PENDIENTE varias sedes de publicación formal y dos candidatos que no se encontraron tal cual (ver "No verificado").

Cómo leer "VERIFICADO":
- **V-arXiv**: se abrió la página del abstract en arxiv.org y coinciden título y autores.
- **V-Crossref**: la página del editor dio 403 o muro de acceso (PNAS, Nature); se abrió el registro del DOI en `api.crossref.org` y coinciden título, autores, revista, volumen y páginas. No se leyó el resumen.
- **V-autor**: página de publicaciones del propio autor.

La columna "qué afirma" sale del resumen de cada página, leído por un modelo pequeño. Las cifras (37.5 %, 21 %, 17 %, 15 USD) hay que releerlas en el PDF antes de citarlas.

## A) Literatura

### Bloque 1 — Agentes LLM haciendo investigación, y sus fallos

| Clave | Autores, año, título, sede | Enlace abierto | Estado | Qué afirma → frase del informe |
|---|---|---|---|---|
| lu2024aiscientist | Lu, Lu, Lange, Foerster, Clune, Ha (2024). The AI Scientist: Towards Fully Automated Open-Ended Scientific Discovery. arXiv | https://arxiv.org/abs/2408.06292 | V-arXiv | Un LLM recorre el ciclo completo, de la idea al artículo, por menos de 15 USD → "ya existen sistemas que automatizan el ciclo; lo que falta es control de confiabilidad" |
| beel2025sakana | Beel, Kan, Baumgart (2025). Evaluating Sakana's AI Scientist: Bold Claims, Mixed Results, and a Promising Future? SIGIR Forum 2025 | https://arxiv.org/abs/2502.14297 | V-arXiv | Evaluación externa: mala evaluación de novedad, muchos experimentos fallidos, manuscritos poco sustentados → "sin protocolo, los agentes producen resultados no confiables" |
| schmidgall2025agentlab | Schmidgall, Su, Wang, Sun, Wu, Yu, Liu, Moor, Liu, Barsoum (2025). Agent Laboratory: Using LLM Agents as Research Assistants. arXiv (cs.HC) | https://arxiv.org/abs/2501.04227 | V-arXiv | Marco con una idea dada por un humano y tres etapas → el antecedente más cercano a "un investigador dirige agentes" |
| huang2023mlagentbench | Huang, Vora, Liang, Leskovec (2023). MLAgentBench: Evaluating Language Agents on Machine Learning Experimentation. arXiv | https://arxiv.org/abs/2310.03302 | V-arXiv | El mejor agente logra 37.5 % de éxito medio en 13 tareas → "los agentes fallan a menudo en experimentación" |
| chan2024mlebench | Chan, Chowdhury, Jaffe, Aung, Sherburn, Mays, Starace, Liu, Maksin, Patwardhan, Weng, Mądry (2024). MLE-bench: Evaluating Machine Learning Agents on Machine Learning Engineering. arXiv ("ICLR version" en comentarios) | https://arxiv.org/abs/2410.07095 | V-arXiv | 75 competencias de Kaggle; medalla de bronce en cerca del 17 % → igual que la anterior |
| starace2025paperbench | Starace, Jaffe, Sherburn, Aung, Chan, Maksin, Dias, Mays, Kinsella, Thompson, Heidecke, Glaese, Patwardhan (2025). PaperBench: Evaluating AI's Ability to Replicate AI Research. arXiv | https://arxiv.org/abs/2504.01848 | V-arXiv | Replicar 20 artículos de ICML 2024: 21 % → "la réplica es justo donde los agentes flojean; por eso el protocolo la exige" |
| siegel2024corebench | Siegel, Kapoor, Nadgir, Stroebl, Narayanan (2024). CORE-Bench: Fostering the Credibility of Published Research Through a Computational Reproducibility Agent Benchmark. arXiv | https://arxiv.org/abs/2409.11363 | V-arXiv | 270 tareas sobre 90 artículos; 21 % en el nivel difícil → respalda la "identidad bit a bit" como exigencia no trivial |
| kapoor2024agentsmatter | Kapoor, Stroebl, Siegel, Nadgir, Narayanan (2024). AI Agents That Matter. arXiv | https://arxiv.org/abs/2407.01502 | V-arXiv | Los benchmarks de agentes premian exactitud sin costo ni reproducibilidad y llevan a sobreajuste → puente con la "segunda frase" (benchmarks propios) |

### Bloque 2 — Preregistro, reproducibilidad y auditoría

| Clave | Autores, año, título, sede | Enlace abierto | Estado | Qué afirma → frase del informe |
|---|---|---|---|---|
| nosek2018prereg | Nosek, Ebersole, DeHaven, Mellor (2018). The preregistration revolution. PNAS 115(11):2600–2606 | https://api.crossref.org/works/10.1073/pnas.1708274114 | V-Crossref | Fuente canónica del preregistro. Resumen no leído (pnas.org dio 403) → definición de "preregistro" |
| pineau2020repro | Pineau, Vincent-Lamarre, Sinha, Larivière, Beygelzimer, d'Alché-Buc, Fox, Larochelle (2020). Improving Reproducibility in Machine Learning Research (A Report from the NeurIPS 2019 Reproducibility Program). arXiv ("To appear at JMLR") | https://arxiv.org/abs/2003.12206 | V-arXiv | Programa de NeurIPS 2019: código, reto y lista de chequeo → "nuestro protocolo es una lista de chequeo aplicada a agentes" |
| henderson2018deeprl | Henderson, Islam, Bachman, Pineau, Precup, Meger (2017/2018). Deep Reinforcement Learning that Matters. AAAI 2018 | https://arxiv.org/abs/1709.06560 | V-arXiv | La varianza y el no determinismo impiden saber si una mejora es real → justifica semillas, réplica ×2 y determinismo |
| kapoor2022leakage | Kapoor, Narayanan (2022). Leakage and the Reproducibility Crisis in ML-based Science. arXiv | https://arxiv.org/abs/2207.07048 | V-arXiv | Fuga de datos en 17 campos y 329 artículos → "los errores que alteran conclusiones son comunes y se previenen con normas de reporte" |
| agarwal2021precipice | Agarwal, Schwarzer, Castro, Courville, Bellemare (2021). Deep Reinforcement Learning at the Edge of the Statistical Precipice. NeurIPS 2021 (Outstanding Paper) | https://arxiv.org/abs/2108.13264 | V-arXiv | Con pocas corridas, las estimaciones puntuales engañan → justifica series de 20 semillas y reportar gana/empata/pierde |
| lipton2018troubling | Lipton, Steinhardt (2018). Troubling Trends in Machine Learning Scholarship. ICML 2018: The Debates | https://arxiv.org/abs/1807.03341 | V-arXiv | Cuatro vicios: especulación como explicación, ganancias mal atribuidas, matemática oscura, mal uso del lenguaje → respalda el vocabulario prohibido sin medida |
| bouthillier2021variance | Bouthillier, Delaunay, Bronzi, Trofimov, Nichyporuk, Szeto, Sepah, Raff, Madan, Voleti, Kahou, Michalski, Serdyuk, Arbel, Pal, Varoquaux, Vincent (2021). Accounting for Variance in Machine Learning Benchmarks. arXiv ("Submitted to MLSys2021") | https://arxiv.org/abs/2103.03098 | V-arXiv | Las fuentes de varianza cambian el veredicto de un benchmark → controles y réplica |

### Bloque 3 — Vida artificial, evolución abierta y Goodhart

| Clave | Autores, año, título, sede | Enlace abierto | Estado | Qué afirma → frase del informe |
|---|---|---|---|---|
| ray1991tierra | Ray (1991). An approach to the synthesis of life. En Langton, Taylor, Farmer, Rasmussen (eds.), Artificial Life II, SFI Studies vol. XI, 371–408. Addison-Wesley | https://www.tomray.me/pubs/ | V-autor (no se abrió el PDF) | Tierra: organismos digitales que compiten por CPU y memoria → antecedente del organismo mínimo |
| lenski2003complex | Lenski, Ofria, Pennock, Adami (2003). The evolutionary origin of complex features. Nature 423(6936):139–144 | https://api.crossref.org/works/10.1038/nature01568 | V-Crossref | Avida: lo complejo se arma sobre funciones más simples (resumen no leído) → "darle a la selección piezas con qué construir" |
| blount2008contingency | Blount, Borland, Lenski (2008). Historical contingency and the evolution of a key innovation in an experimental population of Escherichia coli. PNAS 105(23):7899–7906 | https://api.crossref.org/works/10.1073/pnas.0803151105 | V-Crossref | Una innovación depende de la historia previa (resumen no leído) → analogía de los pasajes seriados |
| nasvall2012iad | Näsvall, Sun, Roth, Andersson (2012). Real-Time Evolution of New Genes by Innovation, Amplification, and Divergence. Science 338(6105):384–387 | https://api.crossref.org/works/10.1126/science.1226521 | V-Crossref | Trabajo moderno de duplicación de genes, en lugar de Ohno (resumen no leído) → "piezas componibles" |
| lehman2011novelty | Lehman, Stanley (2011). Abandoning Objectives: Evolution Through the Search for Novelty Alone. Evolutionary Computation 19(2):189–223 | https://api.crossref.org/works/10.1162/EVCO_a_00025 | V-Crossref | Perseguir el objetivo puede impedir alcanzarlo (resumen no leído) → la "segunda frase": escalar la vara no trajo capacidad |
| wang2019poet | Wang, Lehman, Clune, Stanley (2019). Paired Open-Ended Trailblazer (POET). arXiv (cs.NE) | https://arxiv.org/abs/1901.01753 | V-arXiv | Genera retos y soluciones a la vez; las soluciones se transfieren → contraste: mundo que cambia frente a vara fija |
| hughes2024openended | Hughes, Dennis, Parker-Holder, Behbahani, Mavalankar, Shi, Schaul, Rocktäschel (2024). Open-Endedness is Essential for Artificial Superhuman Intelligence. arXiv | https://arxiv.org/abs/2406.04268 | V-arXiv | Artículo de posición sobre apertura → contexto. No se pidió; añadido como referencia moderna |
| lehman2018creativity | Lehman, Clune, Misevic, Adami, … Yosinski (53 autores) (2018). The Surprising Creativity of Digital Evolution. arXiv (cs.NE) | https://arxiv.org/abs/1803.03453 | V-arXiv | Los organismos digitales subvierten la intención del experimentador → respalda ERR-171 y ERR-175 y la necesidad de controles |
| manheim2018goodhart | Manheim, Garrabrant (2018). Categorizing Variants of Goodhart's Law. arXiv | https://arxiv.org/abs/1803.04585 | V-arXiv | Al menos cuatro mecanismos de Goodhart → nombre técnico del error del director |
| recht2019imagenet | Recht, Roelofs, Schmidt, Shankar (2019). Do ImageNet Classifiers Generalize to ImageNet? arXiv | https://arxiv.org/abs/1902.10811 | V-arXiv | Caída de 11–14 % con un conjunto nuevo. **Cuidado:** el resumen la atribuye a imágenes algo más difíciles, no a sobreajuste por reúso → sirve para "un benchmark mide menos de lo que parece", no para "sobreajuste adaptativo" |

## B) Cinco posibles avaladores (todos autores de artículos de arXiv de la lista A)

| Nombre | Afiliación según su página pública (abierta hoy) | Artículos en arXiv | Por qué es pertinente | Página pública |
|---|---|---|---|---|
| Arvind Narayanan | Profesor de ciencias de la computación en Princeton; director del Center for Information Technology Policy | https://arxiv.org/abs/2407.01502 · https://arxiv.org/abs/2207.07048 | Trabaja justo en reproducibilidad y en evaluación de agentes | https://www.cs.princeton.edu/~arvindn/ |
| Sayash Kapoor | Su página dice: requisitos del doctorado completados en Princeton (CITP) en agosto de 2026; profesor asistente entrante en la UC Berkeley School of Information desde julio de 2027 | https://arxiv.org/abs/2409.11363 · https://arxiv.org/abs/2407.01502 | Primer autor de los dos trabajos más cercanos (fuga de datos y agentes) | https://www.cs.princeton.edu/~sayashk/ |
| Joeran Beel | Profesor de Sistemas Inteligentes, Universidad de Siegen (desde 2020); dirige el Intelligent Systems Group | https://arxiv.org/abs/2502.14297 | Hizo la evaluación externa del AI Scientist | https://isg.beel.org/people/joeran-beel/ |
| Peter Henderson | Profesor asistente en Princeton; dirige el Polaris Lab | https://arxiv.org/abs/1709.06560 | Autor del trabajo de referencia sobre réplica y semillas | https://www.peterhenderson.co/ |
| Jeff Clune | Profesor de ciencias de la computación en la University of British Columbia; Canada CIFAR AI Chair, Vector Institute; su página lo lista como cofundador de Recursive | https://arxiv.org/abs/2408.06292 · https://arxiv.org/abs/1803.03453 | Cubre las dos mitades del informe: agentes que hacen ciencia y vida artificial | https://jeffclune.com/ |

- No se buscaron ni se incluyen correos privados.
- **No se puede saber quién tiene estatus de avalador en cs.AI.** Se comprueba en la página del abstract de cada artículo (por ejemplo https://arxiv.org/abs/2407.01502), al pie, con el enlace "Which authors of this paper are endorsers?". Requiere sesión iniciada en arXiv: lo debe abrir el director.
- Orden sugerido: Kapoor o Beel primero (tema idéntico), luego Henderson y Narayanan; Clune al final (inferencia: probablemente recibe mucho correo y es coautor del sistema que el informe critica de forma implícita).

**Reglas de aval, de las páginas oficiales abiertas hoy:**
- https://info.arxiv.org/help/endorsement.html: hace falta aval antes del primer envío a arXiv o a una categoría nueva. El avalador debe haber firmado cierto número de artículos en el dominio de aval, enviados entre tres meses y cinco años atrás. La página no da reglas propias de cs.AI ni el número exacto para CS.
- https://blog.arxiv.org/2026/01/21/attention-authors-updated-endorsement-policy/ (vigente desde el 21-ene-2026): el correo institucional solo ya no basta. Vía 1, automática: correo institucional **y** autoría previa en arXiv en ese dominio. Vía 2: aval personal de un autor establecido. El director, sin artículos previos, va por la vía 2.
- https://blog.arxiv.org/?p=1740 (31-oct-2025): en CS, los artículos de revisión y de posición deben estar ya aceptados con revisión por pares, y hay que presentar la prueba.

## Qué de la entrega 3 debe reflejarse en RUTA.md

1. **Tesis, líneas 7–9: quitar la causalidad.** "El protocolo atrapó 105 (88 %) antes de que alteraran una conclusión" es un conteo sin brazo de comparación. Redacción medible: "de 120 errores registrados, 105 no alteraron una conclusión declarada; 49 se detectaron antes de correr la serie". Añadir que cubre hasta ERR-153 (ya van por ERR-176) y que la clasificación la hizo un agente.
2. **"Auditoría independiente" y "órgano construido por selección natural".** El auditor es un agente del mismo modelo y la réplica son semillas nuevas en el mismo PC: decir "auditor de solo lectura" y "réplica en semillas nuevas". Revisar "selección natural" y "que nadie diseñó", porque los genes y el operador de mutación sí están diseñados.
3. **Avisos de arXiv: añadir el requisito de aval personal** (política del 21-ene-2026, vía 2) y el paso de comprobación con "Which authors of this paper are endorsers?".
4. **Riesgo de artículo de posición en cs.AI** (regla del 31-oct-2025). El informe debe leerse como investigación: datos (`informe/errores.csv`), método, figuras y limitaciones. La "segunda frase" y las "palabras del director" van en una sección de lecciones acotada, no como eje.
5. **Sedes y orden.** Paso cero: DOI de Zenodo, que da fecha sin aval. Después arXiv con aval. ALIFE 2027 (Praga, 19–23 de julio de 2027, convocatoria aún no publicada) como destino con revisión; la revista Artificial Life como segundo. Los informes registrados (PLOS ONE, RSOS) solo sirven para un estudio futuro.

## No verificado

- **Sedes formales** de varias entradas: solo consta el campo de comentarios de arXiv. No se comprobó la sede final de MLAgentBench, MLE-bench, PaperBench, CORE-Bench, AI Agents That Matter, Kapoor y Narayanan 2022, Recht 2019, Bouthillier 2021 ni Pineau 2020 (volumen de JMLR). En el .bib van como `@misc` de arXiv a propósito.
- **Resúmenes de las cinco entradas V-Crossref** (Nosek, Lenski, Blount, Näsvall, Lehman y Stanley 2011): solo metadatos. La frase "qué afirma" de esas cinco es lectura del título y del uso habitual; hay que leer el resumen antes de citar.
- **Ray 1991**: verificada la cita en la página del autor, no el PDF.
- **Candidatos no entregados como tales:** "Stanley, Lehman, Soros (open-endedness)" se sustituyó por Lehman y Stanley 2011 y Hughes et al. 2024; "Ohno" por Näsvall et al. 2012.
- **Cifras** de las columnas "qué afirma": salen de un resumen automático de la página, no del PDF.
- **Estatus de avalador** de las cinco personas, y si aceptan avalar a desconocidos.
- **Afiliaciones**: son las de la página personal o institucional abierta hoy; sin segunda fuente.
- No se abrieron `informe/borrador.md` ni `informe/errores.csv`. El mapeo "referencia → frase" es contra la tesis de `RUTA.md`, no contra un borrador.
