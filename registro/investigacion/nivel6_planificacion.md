# NIVEL 6 — PLANIFICACIÓN: qué existe, qué falta, y un mecanismo mínimo para v13

**17 sep 2026. Investigador: Claude (Sonnet 5), dirección Christiam Puentes. Documento de investigación (escalera
del punto 6 del brief), no preregistro — la sección 7 es una propuesta a decidir por dirección. No se ejecutó
código ni se modificó el repo.**

Contexto leído: `CLAUDE.md` (Estado día 5, reglas 1–11), `BRIEF_ORIGINAL_y_estado.md` (puntos 6, 14, 15, 16),
`HORIZONTE_frontera.md`, `REFLEXION_agi.md`. v13 no tiene modelo del mundo ni planificación; compone un paso de
historia (3T).

## (1) Qué existe

**Model-based vs model-free, cerebros pequeños.** Daw, Niv & Dayan (2005): arbitraje bayesiano entre un sistema con
modelo (flexible, caro) y uno sin modelo (cachea valor, barato) — probado en mamíferos. Daw, Gershman, Seymour,
Dayan & Dolan (2011): la tarea de dos pasos, prueba operacional estándar que separa planificar de cachear, en
humanos. En insectos no hallé, con la confianza pedida, un equivalente limpio — hueco real, no hallazgo. C. elegans:
White, Southgate, Thomson & Brenner (1986), conectoma completo (302 neuronas). Pierce-Shimomura, Morse & Lockery
(1999): la quimiotaxis se explica por una caminata sesgada ("pirouettes" disparadas por la tasa de cambio de
concentración), sin modelo. Hills, Brockie & Maricq (2004): forrajeo local/global modulado por dopamina/glutamato —
estado interno, no consulta a un modelo. Es el caso mejor documentado de conducta compleja sin planificación.

**Representación sucesora (SR).** Dayan (1993): cachear la ocupación futura descontada de cada estado en vez del
valor; revaluar no exige repetir la experiencia. Stachenfeld, Botvinick & Gershman (2017): campos de lugar y de
rejilla se parecen a la SR aprendida sobre la topología del entorno.

**Replay y planificación.** Foster & Wilson (2006): en reposo despierto, secuencias de células de lugar se repiten
en orden inverso al recorrido reciente. Mattar & Daw (2018): qué recordar en cada momento sigue prioridad = ganancia
× necesidad ("barrido priorizado" de Dyna) — explica contenido, dirección y momento del replay reportado.

**Dyna.** Sutton (1990): aprender un modelo del mundo, generar experiencia simulada con él, y actualizar valor con
la MISMA regla sobre lo real y lo simulado. Planificar es "aprender de memoria en vez de en vivo".

**Navegación en abejas/hormigas.** Müller & Wehner (1988): la hormiga del desierto vuelve a casa integrando su
trayectoria de salida (compás celeste + odómetro de pasos), sin mapa. Wehner & Srinivasan (2003) [verificar título
exacto]: revisión, la integración de trayecto como mecanismo por defecto. Menzel et al. (2005): abejas desplazadas,
rastreadas por radar, a veces vuelan derecho a la meta antes de reconocer el paisaje — leído como memoria "tipo
mapa"; alcance de esa lectura discutido [verificar].

**Active inference mínima.** Friston (2010): minimizar energía libre daría cuenta de percepción y acción; la acción
se elige por la energía libre esperada de cada política (valor epistémico + pragmático) — evalúa el futuro antes de
actuar. Aplicación consolidada a organismos del tamaño de un insecto: no la hallé con la confianza pedida
[verificar]; sí el marco general y su versión de reflejo puro.

## (2) Qué falta para un organismo con reglas locales y 90 celdas

- **Modelo de transición**: no hay tabla "qué sigue a qué"; 3T deja huella en la representación, no una consulta
  tipo P(s′|s,a).
- **Variable de posición propia**: la retina sólo informa la ventana de 6 píxeles actual; sin un "dónde estoy" no
  hay dónde anclar una SR.
- **Consulta antes de actuar**: la política de hoy es retina+hambre→acción en un paso; nada compara dos futuros
  hipotéticos antes de mover las patas.
- **Simulación interna / replay**: la memoria de rechazo (20 pasos) es lista negra que decae, no buffer indexable.
- **Horizonte de composición > 1**: 3T es un paso; planificar exige encadenar varios — el límite del nivel 7.
- **No falta presupuesto**: 40 posiciones y 90 celdas hacen trivial una tabla sucesora frente a lo que v13 ya
  sostiene. La brecha es de diseño, no de escala.

## (3) Mecanismo mínimo compatible con v13

Qué es "un plan" aquí: una acción que cambia por una consecuencia SIMULADA (no sentida aún) vía un modelo aprendido,
no sólo por el valor ya cacheado del estímulo en la retina.

1. Traza hacia ADELANTE, simétrica a la de elegibilidad de las patas: al pisar la casilla s, escribir M[s] = código
   de Kenyon visto ahí (sobrescritura simple).
2. M: tabla posición→código, 40 entradas. Ningún parámetro de valor nuevo.
3. Con la ventana vacía y hambre alta: por dirección (izq/der), sumar sobre un horizonte corto H el valor Wp−Wn ya
   aprendido de los códigos que M recuerda ahí.
4. ΔV_sim(izq) − ΔV_sim(der): sesgo aditivo pequeño sobre la política de patas, sólo desempata sin señal directa.
5. Coste: tabla de 40 + suma de ≤H términos por paso. Cero backprop, cero vía de valor nueva.

Medición: teletransportar el cuerpo (no el mundo) a una posición con la meta consolidada FUERA de la ventana, a
distancia distinta por lado. Medir la dirección del PRIMER paso, antes de todo contacto sensorial nuevo. Predicción:
≥0.75 aciertos (N=20, binomial ≠0.5) con M; el control — M congelada en su inicialización — debe dar 0.50 POR
CONSTRUCCIÓN, no sólo por resultado.

## (4) Cómo acortar la línea

**Con 7 (composición).** 3T compone historia hacia atrás; el paso 1 de §3 es la misma operación hacia ADELANTE.
Extender H de 1 a k es a la vez "componer más pasos" (7) y "planificar más lejos" (6): un solo órgano, horizonte
compartido.

**Con 8 (aprendizaje abierto).** El replay de §5 es el mecanismo de O7 ("qué hacer sin objetivo"): con hambre baja
y sin estímulo, gastar esos pasos actualizando o repasando M en vez de vagar al azar. Bisagra entre 6 y 8.

**Experimento único más informativo**: el de §3. Reutiliza el andamiaje existente, tiene un control que no puede
planificar por construcción, y ordena qué correr primero: sin uso de M en un solo salto de dirección, el replay de
§5 no tendría nada que consultar.

## (5) Romper la frontera

Idea no probada: aplicar la MISMA regla tipo Rescorla-Wagner de las dos vías de v13 también fuera de línea, sobre
pares (posición, código) leídos de M — no sobre experiencia real — priorizando qué repasar por "ganancia" (|dlt|
reciente en esa celda como proxy), al modo de Mattar & Daw (2018). Portar el barrido priorizado de Dyna sin regla de
aprendizaje nueva, sólo agregando CUÁNDO se aplica la que ya existe.

Por qué podría funcionar: no compite en presupuesto (reutiliza Wp/Wn y dlt); en Dyna, pocas actualizaciones
simuladas bien elegidas rinden como muchas más reales — aquí, recuperar una inversión de valor (Etapa 2) más rápido
sin morder más veneno real.

Cómo se refuta: preregistrar que, tras invertir el valor de un estímulo consolidado, el repaso priorizado llega al
criterio de reversión con menos MORDIDAS REALES (p. ej. ≥25% menos) que v13 sin repaso, en N semillas nuevas. Riesgo
honesto: repasar asociaciones obsoletas antes de que la experiencia nueva las pise podría RETRASAR la reversión —
si ocurre, o si no hay diferencia, la idea queda refutada. Control obligatorio: repaso con prioridad aleatoria.

## (6) Trampas

- **Sesgo motor** leído como acierto: el control sin M debe dar 0.50 exacto, no "cerca de"; contrabalancear el lado
  de la meta por semilla.
- **Fuga por memoria de rechazo o traza residual**: exigir ≥30 pasos desde el último contacto con la meta, o el
  sesgo puede ser "recordar el camino recién andado".
- **Meta en posiciones fijas entre semillas**: aleatorizarla, o el acierto viene de otra regularidad memorizada.
- **"Más actualizaciones" confundido con "las correctas"** en el replay (§5): control de prioridad aleatoria
  obligatorio.
- **Loitering en el borde sensorial**: infla el acierto sin planificar nada — métrica fijada al paso inmediato al
  teletransporte.
- **Declarar "planifica" con una corrida o sin réplica**: reglas 6 y 8 del proyecto aplican igual que a cualquier
  etapa.

## (7) Propuesta en formato del proyecto

- **Hipótesis**: una tabla M (posición→último código visto) que sesga la dirección de las patas junto con Wp−Wn
  cuando la retina no ve nada, produce elección hacia una meta consolidada por encima del azar en el primer paso
  tras un desplazamiento, antes de todo contacto sensorial nuevo.
- **Mundo**: anillo de 40 de v13; estímulo consolidado en P fija; teletransporte del cuerpo a S con P fuera de la
  ventana, distancia distinta por lado; hambre media-alta fija; lado de P aleatorizado por semilla; último contacto
  con P a ≥30 pasos del teletransporte.
- **Medidas**: dirección del primer paso; proporción de aciertos sobre semillas; pasos hasta reencontrar P.
- **Predicción numérica**: con M, ≥0.75 aciertos (N=20, binomial contra 0.5, IC95% sin cubrir 0.50); control con M
  congelada, 0.45–0.55.
- **Refutación**: si el organismo con M no supera 0.60, o su intervalo se solapa con el del control, la hipótesis
  queda refutada — no se declara "planifica".
- **Controles**: (a) construcción — M congelada, debe dar 0.50 exacto en expectativa; (b) sesgo motor — mismo mundo
  sin P; (c) ventana de fuga — último contacto a <10 pasos, para acotar dónde hace falta mapa vs memoria corta.
- **Coste en corridas**: ~20 semillas × 4 condiciones ≈ 80 episodios cortos (cientos de pasos, no 100k) — minutos
  en CPU, dentro del punto 17 del brief.
