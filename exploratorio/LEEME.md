# exploratorio/ — fuera de protocolo

Todo lo que hay aquí es EXPLORACIÓN: sin preregistro commiteado antes, pocas semillas, sin réplica, o trabajo de papel.
**Nada de esta carpeta es un resultado declarado de JUACO** ni cuenta para niveles. Lo declarado vive en `registro/` y en `experimentos/`.

`investigacion_20261001/` (1-oct-2026):
- `F0_relojes.md`, `AUDITORIA_F0.md` — el reloj mutacional de los montajes de pasajes (≈ 12 eventos); el de selección no está medido.
- `ENTREGA_1_reactor.md`, `PREREGISTRO_F1_reactor_BORRADOR*.md`, `f1_nulo*` — el Reactor (población de cientos): borrador, no congelado.
- `ENTREGA_2_planear_componer.md`, `ESPEC_P9_ficha3.md`, `AUDITORIA_ESPEC_P9.md` — "planear": liberado sin construir.
- `ENTREGA_3_vocabulario_publicacion.md`, `PASO_C_literatura_avaladores.md`, `referencias_pasoC.bib` — publicación.
- `FABLE_gen_perdido.md` — hipótesis: el muro como dilema de bien público (nivel de selección). Sin medir.
- `FABLE_bloques_autoentrenables.md` — reflexión sobre bloques que aprenden solos; qué existe y dónde se atascó.
- `REVISION_organelos_soloLectura.md` — revisión independiente de la rama.
- `alejo/` — **proyecto Alejo** (experimento 2 del director): `ALEJO.md` documento de arranque; dos exploradores de literatura (mapas, no fuentes).
- `red_celulas/` — prototipos en numpy de la idea del director (células vivas conectadas):
  - `INFORME.md`, `INFORME_2.md` — red de células como modelo propio: con rival justo no gana; pagar a grupos chicos elimina tramposas.
  - `INFORME_3.md` — bloque pegado a un modelo congelado (sintético): empata con un diccionario con oráculo, gana con memoria escasa.
  - `dim40/INFORME_DIM.md` — células en un espacio de D dimensiones con premio regado: no aprende; repartir por cercanía frena tramposas; mover células hacia el premio: NO.
  - `hamburguesa/INFORME_HAMBURGUESA.md` — transformador diminuto congelado + células de memoria viva sobre su estado interno: FUNCIONA en "aprender en uso con memoria suficiente"; el "sueño" consolida.

Cómo reproducir cada prototipo: un comando al final de su informe. Python + numpy, sin GPU.

## Añadido el 5-oct-2026 (exploración, sin protocolo; nada se declara)
- `documento_a_fondo/` — fuentes por sección del documento "JUACO a fondo: cada parte y cada perilla".
- `OPENEVOLVE_para_JUACO.md` — estudio de OpenEvolve (evolución de programas guiada por un modelo de lenguaje) y cómo conectarlo a la pista y al juez.
- `JEPA_para_Alejo.md` — estudio de JEPA y tres experimentos posibles.
- `investigacion_20261005/decision/INFORME_DECISION.md` — modelo congelado que imagina + planificador + células que corrigen la predicción: FUNCIONA en juguete ante cambios de regla globales (0.89 del óptimo); falla con cambios regionales.
- `investigacion_20261005/deriva/INFORME_DERIVA.md` — la célula como aprendiz en línea en las pruebas estándar de deriva de concepto: NO gana a ningún rival estándar.
- El humo de OpenEvolve contra el juez vive fuera del repositorio (`PROYECTOS\JUACO-OPENEVOLVE\`); su informe se copiará aquí cuando termine.
- `investigacion_20261005/mini_llm/INFORME_MINI_LLM.md` — mini modelo de lenguaje por letras (entrenado con retropropagación sobre los .md del proyecto, congelado) + colonia de células + cuarentena: FUNCIONA en chico (aprende hechos sin dañar la base, gana a la memoria de vecinos estándar en 5/5 semillas; la cuarentena no afirma la mentira del maestro mentiroso). Juguete, 5 semillas, sin réplica.
- `investigacion_20261005/ingenieria_inversa/MODELOS_GRANDES_para_Alejo.md` — cómo están hechos DeepSeek, Kimi y Qwen según lo que publican, qué se puede tomar hecho y el puente con la colonia.
- En curso al cerrar el 5-oct: `PROYECTOS\JUACO-OPENEVOLVE\` (humo de OpenEvolve contra el juez) y `investigacion_20261005\hambre_de_saber\` (simulación de un modelo que escoge qué leer); se copiarán aquí al terminar.
- `investigacion_20261005/hambre_de_saber/INFORME_HAMBRE.md` — simulación de un modelo que escoge qué fuente leer (apetito) con cuarentena y amarre texto–video: HAY ALGO MODESTO. Gana al filtro por mayoría contra un grupo de copias que repite una mentira (0 mentiras creídas contra 4) y se entera de los cambios del mundo; falla en la "dieta de basura" (mentira coordinada por voces distintas) salvo con ANCLA (la reputación de una fuente sólo se mueve contra lo que la base congelada ya sabe): 0 mentiras, pero aprende más lento.

`investigacion_20261005/` — añadido en el cierre del 5-oct-2026 (noche, sesión "Frankenstein"; cada carpeta trae su PREREGISTRO e INFORME; los crudos de más de 1 MB y los CSV de precios quedaron fuera de git, en `PROYECTOS\JUACO\investigacion_20261005\`):
- `frankenstein_v0/` — modelo abierto real (Qwen2.5-1.5B q4_k_m, llama-server, CPU, 33 tokens/s) + memoria con cuarentena K=2 + señal de duda. FUNCIONA como muestra viva: 0/72 mentiras afirmadas contra 45/72 de la memoria ingenua, control intacto; precio 0.41 vs 0.60 en hechos nuevos. La clave es léxica (no es la colonia del mini modelo); un mentiroso con cómplice pasa por construcción y no se probó.
- `reflejo_clic/` — bot de acciones en simulador. La colonia como imitadora del clic NO (el 1-NN la iguala o la supera; el control barajado le gana en reordenar). La cuarentena del clic irreversible aguanta: 0/2071 errados contra 7.3–14.9 % de los rivales, con ventaja clara sólo cuando hay demostrador mentiroso inconsistente.
- `valores_sim/` — la colonia sobre precios diarios (31 acciones, tramo sellado 2015–2017, sin dinero real): NO. No supera a comprar y mantener ni al azar con la misma frecuencia, ni a costo cero; tampoco detecta una señal plantada.
- `frankenstein_v1/` (6-oct-2026; la serie se cortó por un apagado y se reanudó sin cambios de diseño) — ataques nuevos y reputación por fuente. HAY ALGO MODESTO: en 2 de 3 semillas la reputación frena al cómplice (0/6 contra 5–6/6 de v0 y 6/6 del voto por mayoría); en la tercera la reputación se INVIERTE (punto fijo biestable, disparado por extracción floja del cuerpo en frases largas). La clave por estado interno del cuerpo no sirve como está. No se puede decir "resiste al cómplice".
