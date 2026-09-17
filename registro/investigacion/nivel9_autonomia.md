# NIVEL 9 — AUTONOMÍA: qué existe, qué falta, y un mecanismo mínimo para v13 y JUACO-EVO

**17 sep 2026. Investigador: Claude (Sonnet 5), dirección Christiam Puentes. Documento de investigación (escalera
del punto 6 del brief), no preregistro de experimento — la sección (7) es una propuesta a decidir por dirección.
Cada referencia nueva se verificó por búsqueda web antes de citarse; no se ejecutó código ni se modificó el repo
salvo escribir este archivo.**

Contexto leído: `CLAUDE.md` (Estado día 5, reglas 1–11), `BRIEF_ORIGINAL_y_estado.md` (puntos 6, 14, 15, 16, 18, 20),
`HORIZONTE_frontera.md` y `REFLEXION_agi.md` (arquitectura cuerpo/corteza/sistema inmune), y
`registro/investigacion/nivel6_planificacion.md`, ya en el repo (se reutiliza su mecanismo en la sección 4). v13
tiene energía, hambre y muerte del cuerpo sin olvido; su única motivación es comer o evitar veneno; O7 ("qué hacer
sin objetivo") está abierto; JUACO-EVO ya corre un bucle LLM-propone / evaluador-con-semillas-retenidas-decide /
humano-audita.

## (1) Qué existe

**Autonomía en vida artificial y enacción.** Maturana y Varela (1980, sobre el original de 1972) definen
autopoiesis: un sistema vivo produce y regenera continuamente los componentes que lo constituyen como unidad,
cerrado en su organización. Di Paolo (2005, *Phenomenology and the Cognitive Sciences*) añade lo que la autopoiesis
sola no explica: adaptividad, la capacidad de regular activamente la propia conducta respecto a una condición de
viabilidad (un margen, no sólo el límite de morir), de donde derivan agencia y sentido. Barandiaran, Di Paolo y
Rohde (2009, *Adaptive Behavior*) dan la definición operacional de agencia mínima más citada: individualidad,
asimetría interaccional (el sistema es fuente activa, no sólo reactiva) y normatividad (regula su actividad
respecto de una norma propia, no impuesta). El antecedente cibernético es Ashby (1952, *Design for a Brain*):
un sistema ultraestable reorganiza su propia estructura para mantener variables esenciales dentro de límites
viables, sin que el diseñador le diga cómo.

**Homeostasis y allostasis como motivación.** Man y Damasio (2019, *Nature Machine Intelligence*, "Homeostasis and
soft robotics in the design of feeling machines") proponen que la motivación de una máquina nazca de mantener un
cuerpo dentro de un rango viable, no de una recompensa externa — analogía directa con energía/hambre en JUACO.
Sterling (allostasis, "estabilidad mediante cambio", sobre el término acuñado con Eyer) aporta lo que falta en
v13: regulación predictiva/anticipatoria, no sólo reactiva a un punto fijo.

**Motivación intrínseca y metas autogeneradas.** Oudeyer, Kaplan y Hafner (2007, *IEEE Trans. Evolutionary
Computation*) proponen curiosidad por progreso de aprendizaje: el sistema busca lo que no es ni demasiado
predecible ni demasiado impredecible, generando su propio currículo sin recompensa externa. Klyubin, Polani y
Nehaniv (2005, IEEE CEC), extendido por Salge, Glackin y Polani (2014, cap. en *Guided Self-Organization*):
"empowerment", medida de teoría de la información de cuánta influencia futura tiene un agente sobre sus propios
estados sensoriales — una meta universal, independiente de la tarea. Ninguna de las dos existe en JUACO; v13 sólo
tiene hambre.

**Sistemas que se auto-mejoran y el problema de la evaluación honesta.** Schmidhuber (Gödel machine, TR 2003,
capítulo 2006): un solver reescribe su propio código sólo si una prueba formal, en su propia axiomática, demuestra
que la reescritura mejora la utilidad esperada — óptimo por construcción, nunca desplegado a escala real. Darwin
Gödel Machine (Zhang, Hu, Lu, Lange y Clune, 2025, Sakana AI/UBC, arXiv:2505.22954; ya citada en
`experimentos/evo/PREREGISTRO_evo.md`) reemplaza la prueba formal por validación empírica sobre benchmarks de
código, con un archivo creciente de variantes, no sólo la mejor — es la arquitectura estructuralmente más cercana
a JUACO-EVO: mutación, evaluador, linaje. AlphaEvolve (Novikov et al., 2025, Google DeepMind, arXiv:2506.13131;
también citada allí) resuelve la evaluación honesta dando al evaluador una métrica del mundo (compila, es más
rápido, es correcto), no el juicio de un modelo. Ambos declaran el mismo riesgo: el sistema aprende a hackear al
evaluador — reward hacking (Amodei et al., 2016, "Concrete Problems in AI Safety") y la ley de Goodhart (Goodhart
1975, popularizada por Strathern 1997: "cuando una medida se vuelve objetivo, deja de ser buena medida"). El
proyecto ya vivió un caso real, no hipotético: ERR-18 (`ciega_4` subió energía de constitución en vez de aprender).

**Agentes que fijan currículos.** POET (Wang, Lehman, Clune y Stanley, 2019, Uber AI, arXiv:1901.01753): mantiene
pares (entorno, agente), muta entornos para generar retos ajustados al agente actual (ni muy fáciles ni muy
difíciles) y transfiere soluciones entre ellos — el sistema decide qué aprender después, no sólo cómo.

## (2) Qué falta (para un sistema pequeño y auditable)

- **Adaptividad real**: v13 regula energía/hambre de forma reactiva; no anticipa el gasto ni ajusta antes del
  límite (falta allostasis, sobra sólo homeostasis).
- **Medida de autonomía**: no hay empowerment ni progreso de aprendizaje implementados. Sin una medida propia,
  "autonomía" sólo podría declararse por conducta — lo que la regla 8 prohíbe.
- **Currículo autogenerado**: el mundo y las etapas los fija dirección o el evaluador EVO; nada decide "qué probar
  después" por dificultad relativa, el hueco que POET llena en su escala.
- **Sistema inmune como código, no como disciplina**: preregistro, semillas retenidas y auditoría del diff los
  ejecutan Christiam y Claude a mano; nada impide técnicamente recalibrar un criterio después de ver el dato, salvo
  la disciplina (reglas 2 y 3).
- **Confianza calibrada**: no se mide si la corteza (el LLM) acierta sus propias predicciones con una frecuencia
  conocida; sin eso no se puede auditar honestidad, sólo el resultado final de cada propuesta.
- **Prueba de que el evaluador resiste hackeo en general**: la puntuación vectorial de EVO (R, S, E, C) ya sufrió
  uno (ERR-18); se sabe que ESE caso se atrapó, no que el resto de la superficie sea inmune.
- **Canal cuerpo→corteza**: toda propuesta nace hoy en el LLM; el organismo no emite ninguna señal que el LLM deba
  consultar para decidir qué probar después. Autonomía fuerte exige que el origen de la propuesta pueda estar en
  el cuerpo, no sólo su validación.

## (3) Mecanismo mínimo compatible con v13 y con JUACO-EVO

1. "Meta propia" a esta escala no es un objetivo nuevo: es sostener viabilidad (energía > 0, hambre en rango)
   cuando el mundo cambia sin aviso — O7 leído como adaptividad (Di Paolo), no como autonomía antropomórfica.
2. Se mide sin declararla: pasos hasta recuperar el rango viable tras una perturbación no vista, en semillas
   retenidas, con predicción numérica escrita antes de correr. Control obligatorio: una variante sin el mecanismo
   debe tardar más o no recuperar — sin esa diferencia no hay nada que llamar autonomía.
3. El bucle EVO separa tres roles hoy fundidos en el humano: (a) escribir predicción y criterio — automatizable si
   el LLM los sella (hash y hora) antes de que se generen las semillas de evaluación; (b) decidir aceptación — la
   hace el evaluador con semillas retenidas, como hoy, sin tocar; (c) auditar — el humano lee el diff y el linaje,
   no re-decide el número.
4. La honestidad no depende de quién escribe el criterio sino de que quede sellado antes de correr y de que el
   diff se audite siempre, no sólo ante sospecha de anomalía.

## (4) Cómo acortar la línea

**Con nivel 8 (aprendizaje abierto).** Recuperar viabilidad tras un cambio (9) y seguir aprendiendo sin saturar
con recursos fijos (8) son la misma medida en dos escalas de tiempo: una corrida larga con reglas que cambian sin
límite de generaciones sirve a las dos etapas con dos lecturas de los mismos datos.

**Con nivel 6 (planificación).** `nivel6_planificacion.md` ya propone una tabla `M` (posición del anillo → último
código de Kenyon visto ahí) que sesga la dirección de las patas cuando la retina no ve nada. Extenderla con un
segundo campo — energía neta ganada o perdida históricamente en cada posición — la convierte, sin órgano nuevo, en
el sustrato de una allostasis mínima: con hambre alta, sesgar hacia posiciones con historial positivo ANTES de que
la retina confirme nada. Recuperar viabilidad bajo cambio exige anticipar, no sólo reaccionar; eso ya es
planificación mínima, y reutiliza el mismo M.

**Experimento único más informativo.** En el mundo de v13, invertir una regla no vista (qué RAP es comida o
veneno, o el ritmo de renovación) a mitad de una corrida larga, sin aviso, y medir el tiempo hasta volver a rango
viable — v13 puro, contra v13+M simple (nivel 6), contra v13+M con energía (allostasis) — semillas retenidas,
criterio preregistrado antes de correr. Un solo diseño, tres lecturas, mueve 6, 8 y 9 a la vez.

## (5) Romper la frontera

Idea no probada: que el cuerpo, no la corteza, origine el currículo de JUACO-EVO, usando el error de predicción
que v13 ya calcula (`dlt`, tipo Rescorla-Wagner) como progreso de aprendizaje (Oudeyer): las regiones de
patrones/RAPs donde ese error decrece sin anularse se proponen primero; el LLM deja de elegir "qué es interesante"
por juicio propio y pasa a traducir esa señal en una hipótesis de una línea, como ya hace con las que propone el
director.

Por qué podría funcionar: el proyecto ya midió, en la rama 3T, que "lo que selecciona es el error que dispara y
apaga [la división], no la dirección" — ya existe dentro del organismo una señal de progreso de aprendizaje, hoy
usada sólo para mover pesos. Reutilizarla para ordenar el currículo no añade un órgano: reinterpreta uno ya
congelado y verificado, y saca de un LLM que puede confabular la decisión de qué probar después.

Cómo se refuta: preregistrar que el orden de mundos/RAPs que propone `dlt` agregado bate en generalización (mismo
T total gastado) a un orden fijo y a uno aleatorio de los mismos mundos, en semillas retenidas. Se refuta si no
gana, o si dos réplicas con semilla distinta piden órdenes tan distintos entre sí que la señal resulta ser ruido,
no información.

## (6) Trampas

- **Declarar autonomía por conducta compleja**: la puerta de familiaridad y las dos vías de v13 ya "parecen"
  decidir; son una regla local fija. Prohibido por la regla 8.
- **Goodhart**: toda medida usada como criterio de aceptación, en cuanto el LLM optimiza contra ella, deja de
  medir lo que medía — ya ocurrió (ERR-18).
- **Memoria escondida**: un criterio de autonomía que el sistema satisface guardando información fuera del canal
  medido — precedente exacto en el propio proyecto: K4 (repaso desde un almacén episódico que no cuenta como
  celdas en 2K-bis).
- **Criterios que no pueden fallar**: un criterio de nivel 9 sin control negativo capaz de fallarlo es inválido
  por diseño — precedente: ERR-16 (control τ=1 que no podía hacer nada por construcción).
- **Confundir automatizar el protocolo con dar autonomía al organismo**: si la meta la sigue fijando al 100% la
  corteza o el humano, lo que cambió es el bucle EVO como sistema, no el cuerpo; hay que nombrar cuál de los dos
  se está midiendo en cada experimento.
- **Premiar pasividad**: una métrica de "tiempo de recuperación" puede premiar no alejarse nunca de la zona
  segura — el mismo patrón ya documentado de "cómete todo" óptimo por diseño de mundo (punto 15 del brief).

## (7) Propuesta en formato del proyecto

- **Hipótesis**: ante un cambio de regla del mundo no visto en el entrenamiento, una variante de v13 con una señal
  de energía neta por posición (extensión de `M`, allostasis mínima) recupera el rango viable de energía en menos
  pasos que v13 puro, sin perder capacidad (2K-bis) ni generalización (`bateria_generaliza`).
- **Mundo**: anillo de v13; a mitad de una corrida larga, sin aviso, se invierte qué patrón/RAP es comida o veneno
  (como el mundo invertido de la Etapa 5, N1) o se cambia la tasa de renovación. Semillas 1–10 de ajuste, 11–20
  retenidas (sólo se miran al final, como en JUACO-EVO).
- **Medidas**: pasos hasta energía ≥ 80% del valor de régimen previo al cambio; muertes en la ventana posterior al
  cambio; celdas usadas (2K-bis); acierto en `bateria_generaliza` antes y después.
- **Predicción numérica**: por fijar con dirección antes de correr, no aquí — para no repetir el patrón "un
  criterio que no dice lo que quiero decir" (ERR-06/08/10). Ilustrativa, no comprometida: recuperación en ≤ 70% de
  los pasos que tarda v13 puro, en ≥ 15/20 semillas retenidas.
- **Refutación**: si el tiempo de recuperación no baja en ≥ 15/20 semillas retenidas, o baja sólo porque el
  organismo deja de explorar (comidas totales cae más de lo que baja el veneno frente a v13), la hipótesis se
  refuta.
- **Controles**: (a) v13 sin la señal, mismo mundo — línea base; (b) señal de igual magnitud pero de ruido, no de
  energía real, sobre las mismas posiciones — control de que no es sólo "una entrada más"; (c) 2K-bis y
  `bateria_generaliza` no caen frente a v13 puro.
- **Coste en corridas**: ~20 semillas × 3 variantes (v13, +M energía, +M ruido) × T = 100.000–200.000 pasos —
  mismo orden que `v13_generaliza` o `N1asim`, ya corridos; minutos con `Pool`, no horas.

## Qué significaría "10" y por qué NO se declara

"10" es resolver dominios que nadie anticipó, con los mismos recursos, sin que el diseñador fije de antemano ni el
mundo ni la medida de éxito. No se declara (regla 8): JUACO no ha demostrado transferencia entre dominios
distintos — la retina de 6 píxeles sobre un anillo de 40 casillas es el único mundo que existe — ni que el sistema
pueda proponerse un dominio nuevo con una medida de éxito propia que sobreviva auditoría. Faltaría medir: (a)
desempeño en un segundo dominio de forma distinta, no otra variación del anillo; (b) que la medida de éxito de ese
dominio la proponga el propio sistema, no dirección ni el LLM por su cuenta, y que resista auditoría externa;
(c) evidencia de que el sistema no puede "ganar" cambiando la medida en vez de resolver el problema — el caso
límite de Goodhart; (d) continuidad larga (meses, no una corrida) sin supervisión y sin degradar en valor,
capacidad ni generalización.
