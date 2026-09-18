# Repos cercanos a JUACO — inventario y préstamos posibles

**17 sep 2026, noche. Investigación web, sin ejecutar ni clonar nada. Pregunta de dirección: "¿algún loco está
haciendo esto a este nivel? y si sí, ¿por qué no leemos sus repos para apoyarnos?". Escrito por Claude.**
Método: búsqueda web (17 sep 2026) + metadatos públicos de la API de GitHub (`api.github.com/repos/...`: licencia,
`pushed_at`, `archived`, estrellas) verificados uno a uno, sin clonar. No repite las citas de papers de
`nivel8_aprendizaje_abierto.md` §1 (EGG, Mordatch, POET, DGM, OpenEvolve, ShinkaEvolve, pymdp ya estaban ahí como
*papers*); aquí se verifica el **repo real** y se cruza contra el tronco v13 y los frentes abiertos (N2b, JUACO-EVO,
nivel 8). Cada fila cubre 1 repo, salvo 3 marcadas con "+" que agrupan un par que la propia dirección pidió junto.

## Inventario (15 entradas, 18 repos)

**1. EGG** (`facebookresearch/EGG`, https://github.com/facebookresearch/EGG; MIT; **archivado** may-2025, sólo
lectura, 322★) — juegos de comunicación discreta multi-agente en PyTorch, con métricas de análisis del protocolo
emergente. Tomar: sus métricas (similitud topográfica, tamaño de vocabulario efectivo) como evaluador NumPy para
N1–N3, sin su entrenamiento. NO tomar: el agente (RNN/Transformer por REINFORCE+gradiente) ni la escala.

**2. emergent-language** (`bkgoksel/emergent-language`, https://github.com/bkgoksel/emergent-language; reimpl. NO
oficial de Mordatch & Abbeel 2018; **sin licencia declarada**; último push feb-2018, 78★, inactivo 8 años) — mundo
físico 2D donde agentes negocian metas con símbolos discretos, gradiente end-to-end. Tomar: el diseño del mundo
compartido (posiciones/metas/utterances) como plantilla de "mundo de señales". NO tomar: el descenso de gradiente
sobre toda la política, ni el código en sí (sin licencia = no redistribuible).

**3. demonstrator-game** (`travislacroix/demonstrator-game`, https://github.com/travislacroix/demonstrator-game;
sin licencia; último push mar-2018, 4★, inactivo 8 años, tamaño de juguete) — juego de señales Lewis–Skyrms con
refuerzo Roth–Erev, **sin red neuronal**. Tomar: la regla Roth–Erev de actualización de probabilidades — el
instrumento más cercano a una regla local sin gradiente para emisor/receptor, directo para N2b. NO tomar: nada de
arquitectura (es casi pseudocódigo), no tiene batería ni protocolo.

**4. POET / Enhanced POET** (`uber-research/poet`, https://github.com/uber-research/poet; Apache-2.0; último push
mar-2022, 266★, sin commits ~4 años pero no archivado) — coevolución emparejada de mundos (terreno bípedo) y
agentes, con trasplante de soluciones entre nichos. Tomar: el mecanismo de "transferencia" entre pares mundo-agente
como metáfora de currículo automático (nivel8 §3). NO tomar: la escala (ES sobre redes de miles de parámetros,
cómputo distribuido).

**5. Darwin Gödel Machine** (`jennyzzt/dgm`, https://github.com/jennyzzt/dgm; Apache-2.0; último push ago-2025,
2340★, activo) — agente de codificación que reescribe su propio código; archivo abierto de variantes validadas en
benchmarks. Tomar: el "archivo creciente" con linaje visible (paralelo a `LINAJE.md` de JUACO-EVO) y la validación
empírica obligatoria antes de aceptar una automodificación. NO tomar: el costo (2 semanas, ~22.000 USD/corrida) ni
que el "agente" es un LLM de frontera operando sobre sí mismo — nada de reglas locales.

**6. OpenEvolve** (`codelion/openevolve`, https://github.com/codelion/openevolve; Apache-2.0; último push
jul-2026, 7391★, muy activo) — reimplementación abierta de AlphaEvolve: LLM propone diffs de código, un evaluador
puntúa, ciclo evolutivo sobre codebases completas. Tomar: el patrón evaluador→diff→selección como plantilla para
escalar JUACO-EVO más allá de un operador manual (`gen1/llm_2`). NO tomar: tal cual mezclaría las tres capas que la
regla 4 del proyecto exige separar (representación/valor/política) — usarlo sólo como arnés, no como diseño.

**7. ShinkaEvolve** (`SakanaAI/ShinkaEvolve`, https://github.com/SakanaAI/ShinkaEvolve; Apache-2.0; último push
ago-2026, 1393★, activo, ICLR 2026) — ensemble de LLM como operador de mutación, muestreo por novedad y bandido,
islas. Tomar: el muestreo por novedad + rechazo por redundancia, para que JUACO-EVO no repita mutaciones ya
probadas en sus 4 candidatas por generación. NO tomar: el cómputo en clúster SLURM y las islas — sobredimensionado
para 4–24 mutaciones por generación.

**8. pymdp** (`infer-actively/pymdp`, https://github.com/infer-actively/pymdp; MIT; último push 15-sep-2026, 735★,
activo) — inferencia activa discreta (POMDP) en Python/NumPy, sin redes neuronales. Tomar: el marco de "valor
epistémico" como candidato a métrica de curiosidad (nivel8 §3 punto 9, sesgo por progreso de aprendizaje) — es
CPU/NumPy, compatible con el tronco. NO tomar: la maquinaria bayesiana completa (matrices A/B/C/D) — es una capa
conceptual distinta a Wp/Wn, no un parche.

**9. HebbianMetaLearning** (`enajx/HebbianMetaLearning`, https://github.com/enajx/HebbianMetaLearning; Najarro &
Risi 2020; **sin licencia declarada**; último push jul-2021, 147★, inactivo 5 años) — evolución de reglas
Hebbianas por sinapsis (no de los pesos) sobre red aleatoria, control continuo. Tomar: la separación "qué se
evoluciona" (la regla local) vs. "qué se aprende en vida" (los pesos vía esa regla) — el mismo patrón que v11
(división por conflicto de signo nacida por evolución). Su prueba de daño morfológico no visto es plantilla de
control de robustez, análoga a 3T. NO tomar: el volumen (450k parámetros, PyTorch+ES distribuido) ni la falta de
licencia (no redistribuible sin permiso).

**10. BindsNET** (`BindsNET/bindsnet`, https://github.com/BindsNET/bindsnet; **AGPL-3.0**; último push 16-sep-2026,
1700★, muy activo) — redes de picos con STDP y STDP modulado por recompensa, sobre PyTorch. Tomar: la formulación
de STDP modulado por recompensa como posible tercera vía de plasticidad si JUACO explora temporalidad de picos. NO
tomar: PyTorch (JUACO es NumPy puro por regla del proyecto) ni AGPL-3.0 — copyleft fuerte, obliga a liberar
cualquier combinación distribuida.

**11. Nengo** (`nengo/nengo`, https://github.com/nengo/nengo; **licencia propietaria, gratis sólo uso no
comercial** — Applied Brain Research; último push ago-2026, 948★, activo) — simulador de modelos cerebrales a gran
escala (Neural Engineering Framework), múltiples backends neuromórficos. Tomar: el NEF como lectura de cómo
decodificar una población de neuronas con reglas locales — sólo como referencia conceptual. NO tomar: la licencia
(no es libre) ni la escala/abstracción — mucha más maquinaria de la que JUACO necesita.

**12. Lenia + Flow-Lenia** (`Chakazul/Lenia`, https://github.com/Chakazul/Lenia, MIT, último push jul-2024, 3825★;
`erwanplantec/FlowLenia`, https://github.com/erwanplantec/FlowLenia, **sin licencia**, último push feb-2024, 27★,
JAX) — autómata celular continuo tipo Game-of-Life; Flow-Lenia añade conservación de masa para que compitan
criaturas por recursos. Tomar: el criterio de "conservación de masa" como control de presupuesto fijo para el
mundo sin techo de nivel8 (§3 punto 3) — la misma restricción, ya resuelta en otro dominio. NO tomar: la
arquitectura de autómata celular en sí (JUACO no es un CA, tiene cuerpo/retina/boca) ni JAX/GPU.

**13. Avida** (`devosoft/avida`, https://github.com/devosoft/avida; licencia no detectada por la API — revisar
`LICENSE` del repo antes de citar texto; último push ene-2025, 670★, en desarrollo activo desde 1993, Michigan
State) — programas autorreplicantes en CPU virtual que compiten por espacio; EQU evolucionó sin diseño dirigido.
Tomar: su métrica de "tarea lógica" (premia funciones difíciles sólo si aparecen por piedras de paso, nunca por
atajo) como plantilla de evaluador anti-trampa para JUACO-EVO (ya hay ERR-18, evaluador explotable). NO tomar: el
modelo entero de organismo (ensamblador autorreplicante) — sin cuerpo, retina ni boca.

**14. navis + Codex** (`navis-org/navis`, https://github.com/navis-org/navis, GPL-3.0, último push sep-2026, 131★;
`murthylab/codex`, https://github.com/murthylab/codex, Apache-2.0, último push sep-2026, 121★; ambos activos) —
herramientas para analizar/visualizar el conectoma FlyWire de Drosophila (139k neuronas), incluido el cuerpo
fungiforme. Tomar: la conectividad real Kenyon→MBON como referencia empírica externa para preguntar si el código
Kenyon y la puerta de familiaridad de v13 tienen análogo biológico plausible (consulta, no dependencia). NO tomar:
el volumen de datos (conectoma completo) ni la idea de perseguir fidelidad biológica — regla 8 del proyecto pide
principios, no mimetismo.

**15. CTRNN (Beer) + evojax** (`olavvatne/CTRNN`, https://github.com/olavvatne/CTRNN, reimpl. NO oficial, MIT,
último push dic-2018, 5★, inactivo 8 años, proyecto de estudiante; `google/evojax`,
https://github.com/google/evojax, Apache-2.0, **archivado** jun-2024, 951★) — agentes con redes recurrentes de
tiempo continuo para conducta mínimamente cognitiva; evojax acelera neuroevolución en JAX/TPU. Tomar: el
repertorio de tareas mínimas de Beer (categorización activa, perseguir/evitar con un sensor) como banco de pruebas
adicional a `bateria_generaliza.py`; de evojax sólo el patrón de log de fitness por generación. NO tomar: el CTRNN
en sí (pesos continuos por ES, no reglas locales) ni JAX/TPU — evojax está archivado y sin mantenimiento.

## ¿Existe JUACO en otra parte?

**No se encontró un repo público que combine los cinco ejes** (organismo mínimo + reglas locales sin gradiente +
preregistro/auditoría escrita + evolución guiada por LLM + comunicación emergente). Búsquedas hechas el 17-sep-2026
(además de las 16 de la sección anterior): *"minimal artificial organism local learning rules no backpropagation
LLM-guided evolution emergent communication preregistered"*; *""open-ended" artificial life project combining
Hebbian plasticity emergent communication evolution reproducible preregistration"*; *"ALIFE 2026 minimal cognitive
agent Hebbian plasticity LLM-guided evolution signaling preregistered protocol"*; *"github topic open-endedness
'no backpropagation' local learning rules evolved communication reproducible"*.

Los candidatos más próximos, y el eje donde cada uno falla:
- **OpenLife** (arXiv 2606.31046, jun-2026) — vida artificial de mundo abierto con agentes LLM autónomos; su
  "plasticidad" es razonamiento semántico del LLM, no una regla local tipo Hebbiana, y el organismo es un modelo de
  frontera, no uno mínimo/auditable. Sin protocolo de preregistro visible.
- **JaxLife** (arXiv 2409.00853, ISAL 2024) — agentes encarnados con comunicación rudimentaria, agricultura y
  cultura emergente; pero los agentes están parametrizados por redes profundas entrenadas por gradiente, y no hay
  preregistro ni criterio de refutación escrito.
- **"Emergent Culture in Minimal LLM Systems"** (Jones & Hauert, arXiv 2606.30668, jun-2026) — "mínimo" se refiere
  a contexto/prompting, no a arquitectura sin gradiente; el organismo es un LLM comercial completo.
- **HebbianMetaLearning** (fila 9) — sí es local, sin gradiente y evolucionado, pero sin comunicación, sin LLM como
  operador de mutación y sin preregistro escrito.
- **DGM / OpenEvolve / ShinkaEvolve** (filas 5–7) — sí usan LLM para evolucionar y sí reportan de forma
  reproducible, pero el "organismo" es código o un agente de programación (sin cuerpo/retina/boca) y no hay eje de
  comunicación ni plasticidad sináptica local.

Ninguno cierra los cinco ejes a la vez. Esto no prueba que JUACO sea único — sólo que esta combinación puntual de
restricciones no apareció empaquetada en un repo público en esta ronda de búsqueda. No se afirma más que eso.

## Tres acciones concretas

1. **Clonar `travislacroix/demonstrator-game`** y leer (sin correr) la regla Roth–Erev de actualización de
   probabilidades, para contrastarla contra el diseño ya preregistrado de N2b (símbolo como sesgo + refuerzo menos
   línea base) antes de la próxima corrida — es el instrumento más chico y más cercano al eje de comunicación sin
   gradiente que JUACO tiene abierto ahora mismo.
2. **Clonar `enajx/HebbianMetaLearning`** y leer cómo separan en código "regla evolucionada" de "pesos aprendidos
   en vida", como espejo para auditar que JUACO-EVO no mezcla capas al mutar una regla de división o al diseñar el
   futuro órgano de fusión (nivel8 §3) — mismo riesgo ya documentado en K4 ("memoria escondida").
3. **Clonar `codelion/openevolve`** (o `SakanaAI/ShinkaEvolve`) y leer sólo el arnés evaluador→diff→selección,
   como plantilla para escalar JUACO-EVO más allá de un operador manual por generación — atento al riesgo de
   evaluador explotable ya registrado (ERR-18) y a la trampa de "curiosidad hackeada" de nivel8 §6.
