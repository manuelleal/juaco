# DEBATE y plan 5→10: moderación de los cinco informes de investigación

**17 sep 2026. Moderador: Claude (Sonnet 5). Base leída entera: `CLAUDE.md` (Estado día 5, reglas 1–12) y los cinco
informes de `registro/investigacion/` (nivel5_transferencia, nivel6_planificacion, nivel7_composicion,
nivel8_aprendizaje_abierto, nivel9_autonomia). No se ejecutó código, no se tocó ningún otro archivo, no se inventó
ningún dato ni referencia: todo lo citado abajo está en esos seis documentos.**

## 1. Confrontación

**Nivel 5.** Su experimento (`mundo_social`, dos v13 con retinas complementarias, canal honesto de N1) reutiliza
exactamente el canal que el propio CLAUDE.md marca como confundido: *"la señal de conducta mezcla valor y saciedad
(INNATO en el mundo de 20 patrones deja 0/10 comidas conocidas)"*. El informe lo admite ("incierto... si un canal
diseñado para 'bien/mal de un patrón entero' alcanza para portar información de una mitad ajena") pero su lista de
controles (K1, N0, SHUF, mitades iguales, techo) no trae ninguno que aísle saciedad de valor. Objeción que le harían
nivel6 y nivel9, los más atentos a canales y confusión de señales: sin ese control, un ≥0.75 puede ser el hambre del
compañero filtrando por el canal, no información sobre su mitad de retina. Con los datos del proyecto la objeción
gana: el fallo por esa vía ya ocurrió una vez, documentado, no es hipotético.

**Nivel 6.** Su tabla `M` (posición→código) es, en espíritu, un almacén indexado externo — el mismo patrón que
**K4** (día 4) probó y que CLAUDE.md fichó como trampa: *"retiene 17–20/20... pero la memoria vive en el almacén:
memoria escondida"*. Nivel7 y nivel8 citan ese precedente en sus propias trampas sin notar que nivel6 (y nivel9, que
construye directamente sobre `M`) están más expuestos a él que ellos mismos. A favor de nivel6: `M` guarda
**códigos**, no valores — el valor sigue viniendo de `Wp−Wn` ya aprendido, no es K4 idéntico. Pero su control
("`M` congelada, debe dar 0.50 por construcción") es un chequeo de instrumento, no una prueba de que `M` no sea un
atajo geométrico. Falta el control que de verdad podría refutarlo: poblar `M` con `Wp/Wn` barajados entre códigos, y
ver si "ayuda" incluso cuando no debería. Veredicto: mecanismo defendible, blindaje incompleto — se refuerza, no se
descarta.

**Nivel 7.** La objeción más fuerte se la hace a sí mismo. Su §4 dice, textual, que el experimento más informativo
**no es** XOR/`Wq` sino repetir 3T con k=2/k=3 — y aun así su §7 formaliza `Wq`, no 3T-k. Además `Wq` agrega 15
parámetros nuevos justo donde v13 diseñó la vía lenta para *"aprende la regla y no los casos"*; el precedente del
día 3 pesa en la misma dirección: *"aprender KW mejora la representación y no mejora la generalización:
descorrelacionar códigos ≠ representar la característica"* (rama 3K). El informe ya trae controles (a)/(b) que
cubren ese riesgo — no queda descalificado — pero su propia sección (4) tiene razón por encima de su sección (7): el
debate prioriza 3T-k sobre `Wq`.

**Nivel 8.** Dos objeciones con datos concretos, y las dos ganan. (a) Predice sobre "35/60 ≈ 58%" y "techo de v11
(50/60 ≈ 83%)", pero CLAUDE.md da **rangos**, no puntos: *"N\* 28 y 35 de 60; v11 43 y 50"* — la regla 6 pide
medianas y rangos, nunca un solo extremo; con 28/60 (47%, casi azar) como piso real, la ventana que el órgano debe
recuperar es más ancha e incierta de lo que predica el informe. (b) Su fusión opera sobre celdas Kenyon y no
menciona en ningún punto la **puerta**, que es justo lo que CLAUDE.md acaba de fichar como el cuello de botella de
v13: *"canje nuevo, medido: puerta contra capacidad... la puerta manda a la lenta los estímulos sin 3 celdas
consolidadas"*. Un órgano de capacidad que no toca ni discute la puerta puede estar arreglando la capa equivocada.

**Nivel 9.** Hereda el riesgo de `M` (arriba) sin heredar los controles que nivel6 sí exige para `M` ("sesgo motor",
"fuga por memoria de rechazo... ≥30 pasos", "meta aleatorizada"): su lista de controles (a/b/c) habla de ruido,
2K-bis y `bateria_generaliza`, no de esas tres trampas — y en una corrida larga con perturbación a mitad de camino
el cuerpo tiene mucho más tiempo para acumular sesgo motor que en la sonda corta de nivel6. Su apuesta de frontera
(`dlt` como currículo para JUACO-EVO) dice "no añade un órgano" y en la misma frase pide agregar y traducir `dlt` a
una hipótesis: es pieza nueva, chica, pero nueva. Ninguna de las dos objeciones tumba el informe; ambas piden
reforzarlo antes de correrlo, no descartarlo.

## 2. Convergencias

- **6+7+8+9 alrededor de una traza/horizonte.** Nivel6 propone `M` (traza hacia adelante); nivel7 dice que extender
  3T (traza hacia atrás) de k=1 a k≥2 sirve a 6 y 7 a la vez; nivel8 llama al repaso fuera de línea "el mecanismo de
  O7"; nivel9 extiende `M` con un campo de energía para autonomía. Cuatro informes, un solo eje. Matiz necesario: 3T
  (compone ventana de percepción en el tiempo) y `M` (memoria espacial de posición) comparten el patrón de diseño
  —memoria indexada, corta, leída después— pero no son literalmente la misma operación; conviene tratarlas como dos
  piezas que convergen en una línea, no fundirlas en un solo código.
- **N2/comunicación no cierra "nivel 5".** Nivel5 saca N2/N2b del cierre de transferencia; nivel7 marca por su
  cuenta la misma ambigüedad de numeración ("nivel 5" de la escalera ≠ "Etapa 5" del punto 16). Dos informes llegan
  solos a la misma separación.
- **JUACO-EVO como motor del proceso, no sólo del organismo.** Nivel8 quiere mutar también el generador del mundo
  (co-evolución tipo POET); nivel9 quiere que el bucle EVO separe sus tres roles y audite menos por juicio humano.
  Ambos empujan a EVO hacia más autonomía del propio proceso.
- **El cuerpo debe ordenar el currículo.** Nivel8 (curiosidad: sesgo hacia el estímulo cuyo error cae más rápido) y
  nivel9 (frontera: `dlt` decide qué propone JUACO-EVO) citan la misma fuente (Oudeyer et al. 2007) para la misma
  idea en dos escalas de tiempo: dentro de una vida, y entre generaciones.
- **Controles importados del canje.** `Wq` congelado/azar (7), fusión ciega (8), señal de ruido (9): los tres, de
  forma independiente, blindan su propuesta exactamente contra el patrón que CLAUDE.md ya documentó dos veces
  (v9→v11; puerta-vs-capacidad de v13). Y los cinco informes, sin excepción, exigen réplica en semillas nuevas antes
  de declarar — ERR-21 como precedente ya interiorizado por todos.

## 3. La línea más corta

Un orden único, cuatro experimentos en el camino crítico más uno barato en paralelo:

1. **3T→k (k=2, luego 3).** Cierra/avanza **nivel 7** (secuencias). Reutiliza `experimentos/3T_confirmatorio/`
   entero; de-riesga la premisa de la que dependen (2) y (4) —que componer más de un paso sobrevive— antes de
   invertir en ellas. Independiente de (3): corren en paralelo.
2. **`M` + teletransporte, con un control nuevo** (Wp/Wn barajados entre códigos bajo `M` poblada, para exponer
   memoria escondida que el control "congelada" no alcanza a ver). Cierra/avanza **nivel 6**. Condicionado a que
   (1) no refute la composición >1 paso.
3. **`mundo_social` (nivel5 §7) con un control de saciedad añadido** (línea base con el mismo estado de hambre, sin
   señal social — no sólo N0/SHUF). Cierra **nivel 5** (transferencia entre sensores) y da una segunda lectura,
   independiente, de **nivel 7** (composición social): si coincide con (1), es réplica cruzada gratis; si no, es
   dato interesante por sí mismo. De paso resuelve N3 (abierto en CLAUDE.md). Mundo-tarea y mundo-generación de
   nivel5 (§3, puntos 3–4) son casi gratis —reusan progenitores ya vividos— y corren junto a esto sin presupuesto
   propio.
4. **Mundo largo con cambio, fundiendo nivel8+nivel9**: un guion con dos perillas —inyección de estímulo nuevo cada
   T pasos (8) e inversión de una regla conocida a mitad de corrida (9)— y cuatro brazos (v13 puro, +`M`, +`M`+
   energía, +fusión) sobre el mismo mundo y las mismas semillas. Cierra/avanza **nivel 8 y nivel 9** a la vez, como
   nivel9 ya reclama para 6/8/9, aquí con la fusión de nivel8 como cuarto brazo. Condicionado a que (2) sobreviva.

Se salta, en esta primera pasada: XOR/`Wq` (nivel7 mismo lo pide en su §4) y N2b/comunicación semántica (nivel5 lo
saca del camino crítico) — se retoman sólo si (1) y (3) cierran secuencia y social pero deja abierta,
específicamente, la composición de rasgos; entonces corre primero el diagnóstico barato de la sección 4.

**Experimento 1, formato completo.**

- **Hipótesis.** Extender la traza de 3T de profundidad k=1 a k=2 y k=3 sobre v13 sigue separando el canal temporal
  por encima del control de orden barajado, sin costar retención (`bateria_v13.py`) ni generalización
  (`bateria_generaliza.py`).
- **Mundo.** El de `experimentos/3T_confirmatorio/`, extendido a componer k pasos en vez de 1; semillas 1–20,
  réplica en 21–40 si pasa; T=100000 (regla 6).
- **Medidas.** `sep` y `lift_q4` (las métricas ya usadas en 3T) para k=1 (referencia: 3.96), k=2 y k=3; retención y
  generalización lineal tras cada k.
- **Predicción numérica.** `sep(k=2) ≥ 3.0` y `sep(k=3) ≥ 2.0`, ambos por encima del `sep` del control de orden
  barajado en ≥15/20 semillas; `bateria_v13.py` y `bateria_generaliza.py` sin variación frente al estándar vigente.
- **Criterio de refutación.** Si `sep(k)` no supera al control barajado en ≥15/20 semillas para algún k, o si
  retención/generalización caen, la composición >1 paso se refuta en ese k — no se avanza a (2) ni a (4) suponiendo
  horizonte libre; se preregistra el siguiente mecanismo en la misma sesión (regla 12).
- **Controles que pueden fallar.** (a) orden temporal barajado —en el día 3 este control llegó a separar MÁS que la
  señal real; no es un control de forma—; (b) sin plasticidad (réplica de 3′, 3″); (c) regresión completa del
  tronco antes y después (regla 1).
- **Coste.** ~20 semillas × 2 valores de k × 2 condiciones (real/barajado) = 80 corridas de T=100000; del mismo
  orden que N2 (100 corridas, 298.5 s reales, según nivel5_transferencia.md) — minutos, no horas.

## 4. La apuesta de frontera

La de **nivel7**: el 0.44 de XOR es un límite de **lectura**, no de representación — la expansión de Kenyon (30→90)
ya haría XOR linealmente separable en el espacio expandido (Cover, 1965), y lo que falta es leerlo con algo más rico
que top-3. Se elige sobre las otras cuatro porque es la más barata (congela Kenyon, cambia sólo la lectura), la más
nítida (un sí/no que redirige el paso siguiente sin ambigüedad) y no depende de que ningún otro experimento de esta
lista haya corrido antes. **Refutación:** si el acierto en XOR nunca visto no sube al cambiar sólo la lectura
(top-k, o la lectura cuadrática de nivel7 §3 aplicada sobre el código ya fijo), el cuello de botella está en la
expansión/dispersión misma, no en la lectura, y `Wq` o Kenyon de segundo orden dejan de ser opcionales.

## 5. Qué NO hacer

- **Fiar una capacidad nueva a un solo extremo de un rango medido** (nivel8 con 35/60 en vez de 28–35/60): la regla
  6 existe por esto.
- **Dejar que una memoria indexada (`M`, fusión) sustituya en vez de indexar lo aprendido**, sin el control que
  expone el atajo (barajar lo que la memoria apunta) — precedente **K4**, "memoria escondida" (día 4).
- **Contar un mecanismo con más parámetros como "compone" o "generaliza" sin control congelado/azar** — precedente
  **3K** (día 3): aprender ≠ representar mejor.
- **Escribir un control que no puede fallar por construcción** — precedente **ERR-16** (τ=1). El chequeo "`M`
  congelada da 0.50" es instrumento, no evidencia; no debe presentarse como si lo fuera.
- **Declarar un nivel cerrado con una sola tanda de semillas** — precedente **ERR-20** (etapa cerrada sin batería no
  está protegida) y el remedio ya usado, **ERR-21** (repetir el examen entero en semillas nuevas antes de congelar).
- **Confundir "nivel 5" (transferencia, escalera) con "Etapa 5" (transmisión, punto 16)** al registrar resultados —
  dos informes lo marcaron por separado; un desliz de numeración puede dar por cerrado lo que no corrió.

## 6. Criterio de parada honesto

La señal más fuerte de que el 10 no es alcanzable con **esta** arquitectura (90 celdas fijas, dos vías locales, sin
retropropagación) no es que un experimento falle —eso ya pasó con N2 y el protocolo manda preregistrar el siguiente
intento, no parar—. La señal es **estructural**: si en 5–6 intentos bien controlados y de mecanismos genuinamente
distintos (horizonte-k, `M`, fusión, `Wq`, lectura enriquecida) **cada uno** compra su ganancia con un canje nuevo
contra memoria, generalización o capacidad —repitiendo, cada vez más ajustado, el patrón ya visto dos veces (v9→v11;
puerta-vs-capacidad de v13) sin que ninguno lo rompa ni parcialmente— eso indica que el canje es propiedad del
**presupuesto fijo de celdas locales**, no un error de diseño corregible con la siguiente regla local. Segunda
señal, más específica: si **tres** mecanismos de composición no emparentados (3T-k, `Wq`, lectura enriquecida)
fallan su control congelado/azar por igual, ir más allá de asociaciones lineales de un paso puede estar fuera del
alcance de Kenyon-fijo + valor-local sin gradiente compartido, y no ser un problema de encontrar la regla correcta.
Ante cualquiera de las dos, la pregunta para dirección deja de ser "qué mecanismo probar después" y pasa a ser si
crecer el pool de celdas, permitir algún gradiente local acotado, o cambiar de mundo (uno con más estructura que
premie componer) es la única vía que queda.
