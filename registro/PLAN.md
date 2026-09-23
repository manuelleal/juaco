# PLAN — Traspaso a Claude Code y etapas siguientes

> **Nota del 23-sep-2026:** este archivo es la bitácora de órdenes hasta el 18-sep (tronco v13 → v14.2). El orden vigente desde el
> 21-sep está en `registro/ESTADO.md` (bloque más reciente) y en `registro/HANDOFF.md` §15.x. Nada de lo de abajo manda sobre eso.

> **ORDEN VIGENTE PARA EL DÍA 6 (escrito el 17 sep 2026, 20:30, al cierre del día 5). Manda sobre todo lo de abajo.**
> **Tronco: v13** (`v13-tronco`). Etapas **1, 2, 3, 4, 5-N1, 5-N3 CERRADAS**; niveles 6 y 7 del brief con resultado replicado;
> nivel 8/9 con hallazgos. Detalle: `CLAUDE.md` (bloque día 5), `HANDOFF.md` §11.6 y §12, `REGISTRO_etapas_1_2.md` (final).
> Regla 12 vigente: decidir → preregistrar → commit → correr → registrar; el director audita después.
>
> **Bloque 0 — herramienta, antes de cualquier ciencia (≤ 1 h):** gemelo rápido del organismo.
>   ✅ **HECHO el 17-sep 20:50:** numba 0.67 instalado (rueda cp314); `organismo/organismo_v13_rapido.py` = gemelo compilado del
>   tronco, **bit a bit idéntico en 72/72** (12 configuraciones × 6 semillas, `organismo/identidad_rapido.py`) y **×78**
>   (100k pasos: 4.05 s → 0.05 s). **Gemelos de los mundos (equipo de compiladores, 17-sep 22:00–22:40):** 3T-k 146/146 ✅
>   (`--rapido`), mapa 90/90 ✅ (`--rapido`), mundo de regla/XOR 81/81 ✅ (pendiente 3b + verificación), social y mundo largo
>   en construcción; baterías con `--rapido` pendiente. Regla: un gemelo que no sea bit a bit sólo explora, nunca confirma.
>
> **Bloque 1 — cabos del plan del debate (cortos, en este orden):**
>   1a. ✅/⚠ 3T-k: k = 4 dio "compone" en 1–20 (lift 0.152) pero **no replicó** en 41–60 (lift 0.140 < 0.15; separación sí, 20/20).
>       Declarable: compone hasta 3; a 4–5 separa pero la ventaja conductual queda al filo; techo = presupuesto de celdas.
>   1b. ✅ Mundo largo 21–40 con `W`: hallazgos replicados; retención de lo ausente 0.67 (V13) / 0.50 (mapa) → interferencia,
>       no inversión; el mapa muere MENOS tras el cambio (predicción refutada en la dirección buena).
>   1c. ✅ N3d mudo: 0.503 sin señal (= solo 0.515; con señal 0.822): obedece, no enseña; y crea dependencia (189 muertes).
>       La variante "vista parcial que sí puede aprender" no tiene mundo todavía (N3c: ya sabe solo; N3b: no encuentra comida).
>
> **Bloque 2 — nivel 8 propio: el canje exploración/explotación del mapa.** ❌ **Curiosidad por progreso REFUTADA (0.700 = mapa
>   0.704 = barajada 0.700; v13 0.900; comida intacta 974).** Siguiente candidato (escrito antes): novedad de sitio. El mapa da de comer (490 vs 332) pero daña la
>   adquisición de lo nuevo (0.70 vs 0.88). Órgano candidato: **curiosidad por progreso de error** (nivel8 §3, puntos 8–9:
>   sesgo hacia el estímulo cuyo error cae más rápido, no el más alto ni el más bajo). Brazos: v13, +mapa, +mapa+curiosidad,
>   +mapa+curiosidad con prioridad aleatoria (control). Predicción: +curiosidad recupera la adquisición de v13 (≥ 0.85 a
>   ≤ 30 vistos) sin perder la comida del mapa (≥ 450 en Q4, pareado ≥ 15/20); el control aleatorio no lo hace.
>
> **Bloque 3 — apuesta de frontera: XOR como límite de LECTURA (Cover 1965).** ❌ **REFUTADO (3 y 3b):** ni dimensión ni puerta;
>   la vía lenta cuadrática representa XOR (W del producto −2.65) pero su REGLA no lo separa (marginales drenados). 3c: regla
>   delta con signo, diseño del trío con puente (`PUENTE_xor.md`). Texto original: congelar Kenyon; cambiar sólo la lectura:
>   vía lenta **cuadrática** (15 productos de pares de píxeles además de los 6 píxeles). Predicción: `xor01` en nunca vistos
>   ≥ 0.80 si el límite era de lectura; ≤ 0.60 → el límite es de representación y se registra así. Controles: la vía
>   cuadrática con productos barajados; `bateria_generaliza` (px0 y azar) sin caer.
>
> **Bloque 4 — decisión de tronco (sólo si pasa el bloque 2):** candidato **v14 = v13 + mapa + curiosidad** (y la vía
>   cuadrática si pasa el bloque 3): examen criterio v3' en semillas nuevas + `bateria_generaliza 20` + regresión completa
>   + 3T-k + mapa. Si no pasa el bloque 2, **v13 sigue siendo el tronco** y mapa/`gamma_soc` quedan como órganos de
>   experimento validados en su mundo (registrados en `experimentos/evo/LINAJE.md`).
>
> **Bloque 5 — ❌ HECHO y REFUTADO (N2f v3, 17-sep 22:35):** montaje válido por primera vez (emisiones 0.23; K3/K4/K5 ok) y N2
>   cae por sexta vez (E2 ±0.3, E4 sin beneficio, E5 no destruye). **N2 cerrado con dos mundos.** INNATO 60 contra 278: el canal
>   serviría con significado dado; lo que falla es aprenderlo por refuerzo. Texto original: N2b (símbolo como sesgo + ventaja) en el mundo con reaparición en
>   sitio (`mundo_social_n3`, `regen = 50`), que equilibra visitas (la causa registrada del cierre). Predicción: contraste
>   ≥ 0.5 en ≥ 10/20 y beneficio ≥ 1.2 × N0 en ≥ 15/20. Si cae, N2 queda cerrado con dos mundos.
>
> **Canje del mapa (17-sep 23:10): CERRADO COMO ESTRUCTURAL** (saturación refutada, tercer candidato); v14 no lleva el mapa.
> **Día 7, orden sugerido al cierre del día 6:** (1) 3d XOR con la regla fusionada del trío (instrumento único por anclas,
>   gemelo XOR en segundos); (2) ✅ nivel 6: dos metas y rodeo — HECHO y REPLICADO (23:30; rodeo 0.725/0.750 en el subconjunto válido preregistrado, pareado 14/14 y 16/16; invertido 0.25); (3) ✅ canje del mapa: sólo un candidato que
>   ataque la ESCALA del recuerdo de veneno; si cae, canje estructural y v14 sin mapa; (4) bloque 6; (5) N2 sólo con
>   significado por predicción (el brazo INNATO mostró que el canal serviría con significado dado).
> **Bloque 6 — exploratorio (rama, 5–10 semillas):** modelo de sí mismo mínimo = predictor de la propia energía
>   (allostasis, nivel 9 §3): el organismo predice ΔE del próximo bocado con su propio valor y usa el **error de esa
>   predicción** como señal de sorpresa que module `eta`. Sólo se mide; no se declara nada.
> **Madrugada del 18 (célula de creación; el director ausente; decisiones del coordinador, documentadas), ORDEN VIGENTE
>   — un Pool a la vez, cada bloque con preregistro, identidad dentro del runner y registro al terminar:**
>   (1) **A-2 metaplasticidad por masa de conflicto** (nivel 8, retención de lo ausente 0.67 → ≥ 0.80; `mundo_largo_A`,
>   memoria nueva cero; semillas 41–60; control: muertes y `ret_inv`); (2) **B-1 hija dispersa** (nivel 7, k = 4/5;
>   `mundo_k_B3`; semillas 61–80; control decisivo: máscara al azar); (3) **B-2 puerta por evidencia del código exacto**
>   (nivel 4, capacidad sin perder generalización; montaje de `reverificacion_v13` 41–60 + baterías sobre `organismo_v13B`;
>   candidato a v14 si pasa — la decisión de tronco es del director); (4) **A-1 XOR 3f** (tres piezas: selección por
>   competencia, tope ≥ 10, muestreo) sólo si el instrumento de selección abre el conjuntivo correcto en la mini-prueba;
>   (5) **A-3 vector único** (simplificación de la vía lenta con identidad; 101–120); (6) **mundo 2D** (nivel 6) según el
>   informe del diseñador — HECHO 01:30 (no rodea, se aleja; rodeo falso confirmado; borrar el sitio comido ayuda a encadenar; horizonte 2 sin potencia: rediseñar el mundo antes de replicar); (7) **C** (modelo de sí mismo, aprender sin morder, significado por predicción) según su
>   propuesta. Lo que toque el tronco va a rama o copia; nada entra a v14 sin examen v3' + baterías + réplica.
>
> **DECISIÓN DEL DIRECTOR (18 sep 2026, 04:55; "sí a todo", "listo, de acuerdo") — ORDEN VIGENTE A PARTIR DE AQUÍ:**
>   (1) ✅ HECHO 05:05 — **v14 CONGELADO** (v13 + hija dispersa + puerta por código; la sorpresa a dosis 5 queda candidata a v15 porque la
>   composición de los tres cayó por una semilla en la réplica del examen). Faltaba: v14 = v13 + hija dispersa +
>   puerta por código (+ sorpresa del mundo en la boca a dosis 5 si la composición de los tres pasa T1–T3; si no, la sorpresa
>   queda como candidata a v15). Antes del tag: tercer examen del organismo final en un rango virgen (161–180 o el siguiente
>   libre), gemelo con arnés bit a bit, manifiesto a 15 archivos, `bateria_v14.py`, regresión de la regla 1.
>   (2) **Escribir v14 como resultado cerrado** (REGISTRO, HANDOFF, CLAUDE.md, PROPUESTA → DECISIÓN).
>   (3) **Un solo frente después: APRENDER SIN MORDER** — la pieza de muestreo de XOR (creador A: 5 740 encuentros con veneno `00`
>   por corrida donde hoy no se aprende nada), que también toca a N2 (significado por predicción, creador C). Tres bloques
>   preregistrados como máximo, cada uno con su mecanismo local, controles e identidad.
>   (4) **Criterio de parada, fijado ahora:** si en esos tres bloques ningún mecanismo local cruza **0.75 en xor01 (nunca vistos)**
>   con px0 = 1.000 y azar en [0.35, 0.65], se acepta el techo de la arquitectura: se publica el organismo (v14) y el método tal
>   como están, y se cambia de paradigma (evolución del organismo entero, no órganos diseñados) o se cierra. Sin recalibrar.
>
> **DECISIÓN DEL DIRECTOR (18 sep 2026, 05:10) — EL FRENTE ÚNICO, CON DOS ORGANISMOS Y TODO SE VALE (dentro del método):**
>   (A) **Dos organismos en paralelo sobre v14, mismos mundos y mismas pruebas preregistradas:** `SIN` (reglas locales:
>   codificación predictiva + retorno asimétrico tipo feedback alignment, el error de predicción de ΔE como señal común) y
>   `CON` (backprop de laboratorio: gradiente fuera del organismo para descubrir la regla local, y como control positivo un
>   lector entrenado con backprop en la misma vía lenta y el mismo muestreo). La comparación es el instrumento: si `CON`
>   resuelve XOR con el muestreo real, el cuello es la regla; si tampoco, el cuello es el mundo. Nunca backprop dentro del
>   tronco: copias y ramas.
>   (B) **La repetición es el enemigo:** la medida que manda pasa a ser *cuántas exposiciones hacen falta* para asociar
>   (una imagen → lo previo, salvo que el mundo diga otra cosa): aprender sin morder, asociación en pocas exposiciones,
>   como en insectos (aprendizaje en un ensayo). Todo bloque reporta exposiciones-hasta-criterio, no sólo acierto final.
>   (C) **Representación en GRAFO (corrección del director, 05:25: "la palabra es grafo, no vectorización"):** lo aprendido
>   como nodos (patrones, sitios, valores, contextos) y relaciones entre ellos, que el organismo recorre para asociar lo
>   nuevo con lo previo; representaciones de alta dimensión (código disperso, ligar/desligar) sólo como soporte del grafo,
>   no como ruta lineal; se consulta a los expertos (explorador) y entra por el mismo método (identidad, preregistro, réplica). (D) Criterio de parada de la decisión de las 04:55 sin cambio: tres
>   bloques; 0.75 en xor01. (E) Toda idea entra con copia y anclas; el tronco v14 no se toca.
>   (F) **MUNDO VIVO (idea del director, 06:10): necesidades múltiples y estímulos múltiples.** El organismo como ser con varias
>   necesidades (empezar por DOS: hambre y sed; después temperatura/seguridad, reproducción) y varios estímulos (empezar por
>   CUATRO: comida, veneno, agua, sal/peligro), estado interno vectorial y sorpresa específica por necesidad. Lo que compra:
>   cada encuentro informa varias necesidades a la vez (aprender con menos mordidas) y el significado depende del estado
>   ("agua" vale con sed y nada sin sed): un XOR natural necesidad × estímulo. Propósito y reproducción primero como medida
>   (descendientes viables), después como mecanismo (selección: la evolución del organismo entero). Entra como MUNDO NUEVO
>   por anclas: con una necesidad y dos estímulos debe ser v14 bit a bit. Diseño primero (diseñador), sin correr nada grande.
>
> **DECISIÓN DEL DIRECTOR (18 sep 2026, 09:55) — CAMBIO DE RUMBO.** Tras la mañana (cinco bloques preregistrados por hora, dos
> resultados declarados, ningún candidato de capacidad al tronco; revisor de literatura: ningún mecanismo nuevo), el coordinador
> diagnosticó cuatro cosas mal planteadas y el director decidió: *"Perfecto, hagamos esa modificación y registra todo"*.
> Lo que cambia, y lo que no:
> 1. **Se conserva el método** (preregistro → commit → correr → registrar; ERR numerados; réplica antes de cerrar; regla 12; reglas 1–14 de
>    EQUIPO). Es lo que nos salvó cinco veces hoy (ERR-38, 41, 42, 43; la medida de reproducción).
> 2. **El mundo cambia por uno que obligue a representar:** estímulos compuestos (una "sal" y una "sal rosa": la variante como variable
>    del mismo token), más píxeles que 6, recursos que se agotan, veneno que cambia — un mundo donde 16 patrones no basten y donde
>    la tokenización, la variable y el desaprender sean necesarios para sobrevivir (ERR-35: el mundo de 16 patrones no contiene la
>    información para elegir XOR; no se le vuelve a preguntar lo que no puede responder).
> 3. **La estructura crece por reglas locales:** el organismo recluta y divide celdas cuando la sorpresa se repite en la misma
>    combinación (conjunción por coactividad) y cuando un código con valor recibe otra consecuencia (B-5); ninguna capacidad nueva
>    entra como perilla diseñada a mano si puede entrar como crecimiento.
> 4. **El criterio de tronco cambia:** el examen v3′ 8/8 deja de ser la puerta absoluta (selecciona "no cambies nada": v15d/v15e
>    murieron por detalles internos; sólo entró lo inerte). Un candidato nuevo se juzga por **sobrevivir y generalizar en el mundo
>    vivo** (muertes, r = descendientes − muertes, nunca vistos, reversión: se desdice, sin alias) con **no regresión CONDUCTUAL** del
>    examen (la conducta de cada escenario se conserva; los pesos internos no son puertas). El criterio v2 se escribe en
>    `registro/CRITERIO_TRONCO_v2.md` ANTES de juzgar a ningún candidato con él; **v15c/v15d/v15e no se rejuzgan** (regla: no
>    recalibrar después de ver datos); v14.1 sigue siendo el tronco hasta que un candidato cruce el criterio v2 en semillas nuevas.
> 5. **Ejecución:** la SALA 2 (4 diagnósticos, 6 diseños, 12 refutadores, síntesis) entrega el diseño concreto del mundo y del
>    crecimiento; de ahí salen los bloques preregistrados, en este orden: (a) `CRITERIO_TRONCO_v2.md`; (b) el mundo que obliga (mundo
>    nuevo con v14.1 SIN cambios como control base: si el tronco ya sobrevive ahí, el mundo no obliga); (c) crecimiento estructural
>    por sorpresa repetida (crece_codigo) medido en ese mundo; (d) tokens y variables ("sal rosa" cuelga de "sal"; separación cuando
>    deja de comportarse igual); (e) población con herencia y muerte real (que viva). Una cosa a la vez en el Pool; réplica antes de
>    declarar; "llegar a la frontera es lo primero, que viva lo segundo".
> 
>
> **DECISIÓN DEL DIRECTOR (18 sep 2026, ~14:15) — PLAN APROBADO tras la síntesis de la SALA 2:** la misión sigue siendo llegar a la AGI por este camino ("si no la tenemos en la cabeza no llegamos"); con honestidad registrada de que estamos muy lejos. Plan: (1) bloque 0, escalar el código sin órgano nuevo (alias < 1 % con D = 12, cálculo estructural); (2) bloque 1, el mundo de familias que obliga a representar, medido primero con v14.1 sin cambios (si no se distingue de un lector lineal, el mundo se endurece); (3) después el órgano (v15f bajo el criterio v2, crecimiento por sorpresa) y al final población; (4) consolidar y publicar lo que hay (nota técnica reproducible del alias + banco de método) en paralelo, a un ritmo que no queme. Agentes en Opus; el coordinador verifica. Pendiente del director: B-5 como v14.2.
>
> **SEPARADA (19 sep 2026): la línea del exoesqueleto es ahora el subproducto `PROYECTOS/JUACO-EXO` (repo propio; EXO-1, EXO-2, EXO-2b; ROADMAP propio). JUACO sigue con la fase 5.**
> **LÍNEA LATERAL (18 sep 21:00, simulación, no toca la escalera):** JUACO como exoesqueleto cognitivo externo de un agente LLM (y currículo por sorpresa en ML): arquitectura, algoritmo, experimento A/B/C de cinco días, métricas y dónde se rompe en `registro/investigacion/HIPOTESIS_exoesqueleto_20260918.md`. Se corre después de cerrar la fase 5 y el linaje mortal.
>
> **REVISIÓN DE RUMBO (06:45, a petición del director: "¿nos estamos yendo del camino?"): ligera dispersión, corregida así:**
>   **Columna vertebral = XOR** (los tres bloques del criterio de parada, nada los adelanta en el Pool): A-4 (dos constantes de
>   la vía lenta; HECHO 05:35: **bloque 1/3, XOR 0.625 — la regla ya llega a 1.000 con rasgos dados y no daña el tronco; el cuello son
>   los rasgos**; las dos constantes entraron al tronco como **v14.1** a las 06:05) → A-6 (HECHO 06:05: **bloque 2/3, XOR 0.500 en el mundo
>   original; con 14 patrones de entrenamiento la regla local llega a 1.000 en los nunca vistos**) → **DECISIÓN DEL DIRECTOR 07:10
>   (ERR-35): el criterio de parada se reformula — la línea XOR se cierra declarando el mínimo de ejemplos con el que generaliza
>   (14: sí, 1.000; 11: no; 8: nadie puede, 9 de 15 hipótesis empatadas). BLOQUE 3/3 HECHO 07:43: **M3 (memoria de un golpe por
>   combinación, ganador de la sala) cruza con 8 ejemplos: 1.000 registro y estricta, n* = 7, desempate al azar, azar en banda,
>   con 14 también 1.000 → PRIOR ESTRUCTURAL de pares, declarado; réplica 141–160 igual → **LÍNEA XOR CERRADA (07:47)**; siguiente: llevarlo al
>   tronco como candidato a v15 (HECHO 08:06 / 08:38 / 08:46: v15c y v15d NO entran — **ERR-38**: su G1 0.500 era del instrumento (batería copiada sin eta_s/clip_s;
>   corregida: G1 1.000 los dos); v15d cae en el examen encendido por REVERSIÓN (E2 0/20: la tabla de un golpe no se desdice) → siguiente
>   candidato con preregistro nuevo: v15e tabla reescribible, creador A); **desambiguar códigos (B-5) HECHO 09:07: 8/9 criterios, tronco intacto
>   por inercia exacta; C4 7/9 → réplica en semillas nuevas HECHA 09:12: PASA → DECLARADO; candidato a v15 ("división por R = 0"), la entrada la decide el director**; **propósito y reproducción (peldaño 2) HECHO 09:16: la medida se tira (P-R1: premia atracones que mueren más), la tercera necesidad sobra frente a CUELLO_MIN; bloque 2 con medida ligada a la supervivencia (ERR-40), semillas 261–280, en preregistro**; **v15e HECHO 09:37: se desdice (E2 20/20) y consolida (E1 20/20) pero pierde XOR (0.500) → NO entra; v15f encargado; revisor de literatura 09:45: nada nuevo en mecanismo, publicable como nota técnica del alias; SALA 2 (frontera) corriendo desde 09:40**; **reproducción bloque 2 HECHO 09:43 + réplica 09:45: 8/8 ×2 — r = descendientes − muertes ordena como la supervivencia; CUELLO_MIN al filo del reemplazo; tercera fila retirada → DECLARADO; siguiente: población con herencia (Pool)**; **v15f HECHO 10:00: no entra por v1 (dos letras internas, ERR-44) pero generaliza, se desdice y cruza XOR con 8 ejemplos en el tronco (1.000) → primer candidato para el criterio v2, preregistro nuevo tras la síntesis de la sala** y el mundo vivo (F): **HECHO 07:58 — núcleo sostenido (valor por
>   necesidad resuelve el XOR necesidad × estímulo 20/20; escalar no; barajar contenido lo destruye), supervivencia y sal no como se
>   predijo (P4′, P6, P7) por el umbral (ERR-37); **réplica 201–220 con enmienda 2 HECHA 08:20: pasa, y P10 confirma el alias de código;
>   bloque de la sal HECHO 08:16: alias confirmado 9/9 contra 9/9, persiste sin sed (S-5), la puerta no lo repara (S-6) → nivel 4: desambiguar códigos.**
>   **Laterales, un bloque cada uno y se cierran:** B-5 (HECHO 05:55: no confirma; la vía lenta asocia en 2 exposiciones en vez de 4.5
>   pero también en azar; línea cerrada) y C-P6
>   (HECHO 06:37: NULO para N6 — el mundo se aprende solo, SOLO_R 0.986 fuera de banda; ERR-36: el runner no guardó curva_rec;
>   sobreviven N1 (significado con la magnitud del mundo, 19/20) y N4; línea cerrada). **Mundo vivo (F): sólo diseño y preregistro hasta
>   el veredicto de XOR**; si XOR cruza 0.75 es el siguiente peldaño (significado por necesidad); si no cruza, el mundo vivo
>   con reproducción es el cambio de paradigma ya escrito. Nada nuevo se abre sin cerrar uno de estos.
>
> Siempre: semillas nuevas por intento, réplica antes de cerrar, ERR numerado por cada fallo de instrumento/medida/mundo
> (lista de la noche del 17: canal simétrico, acierto sin balancear, mundo que se come la comida, sitios que se memorizan).
>
> **ORDEN DEL 17 SEP 2026 (día 5, noche). Histórico; lo manda el bloque del día 6 de arriba.**
> **Tronco: v13** (`v13-tronco`). Etapas **1, 2, 3, 4 y 5-N1 CERRADAS**. Detalle en `CLAUDE.md` (bloque día 5) y
> `HANDOFF.md` (sección 11).
> 1. ✅ v11 (evolución guiada, JUACO-EVO gen 1) cierra la Etapa 4; capacidad ×5; **pero reabre la Etapa 3** (ERR-20).
> 2. ✅ Diagnóstico confirmado: generalización = interferencia (fuga). Mapa del canje (v12): ninguna perilla lo rompe.
> 3. ✅ **v13 = dos vías + puerta**: rompe el canje. Examen v3' 8/8 y generalización en 101–120. 3T sobrevive;
>    capacidad cae a 35 de 60 (canje puerta/capacidad, ERR-22).
> 4. ✅ Etapa 5 N1 (experto → novato por conducta visible) demostrada y replicada.
> 5. ❌ **Etapa 5 N2 (significado emergente): cinco diseños refutados; línea cerrada por hoy.** Emerge una convención
>    arbitraria que muere al barajar, sin magnitud útil (asimetría del mundo y de la recompensa). Reabrir sólo con otro mundo.
> 6. **Plan del debate de niveles 5–10, ejecutado** (`registro/investigacion/DEBATE_y_plan_5a10.md`; HANDOFF 11.6):
>    (1) ✅ 3T-k compone hasta 3 pasos (replicado) · (2) ✅ mapa elige el lado de la comida recordada (replicado) ·
>    (3) ❌ N3/N3b/N3c (ERR-23; montaje inválido); N3d = receptor ciego por construcción · (4) ❌ compuesto: v13 sigue
>    aprendiendo hasta 50 patrones y se recupera de la inversión; el mapa daña la adquisición.
> 7. Siguiente: cerrar N3d; guardar W por patrón en el mundo largo; coste en capacidad de 3T-k; exploración/explotación
>    del mapa (nivel 8); XOR como límite de lectura. Rama "puerta con rápida vacía"; consolidación (`HORIZONTE_frontera.md`).
>
> **ORDEN VIGENTE AL 16 SEP 2026 (día 4, tarde). Histórico; lo manda el bloque de arriba.**
> Los "Pasos" numerados de la sección "PLAN PARA LA PRÓXIMA SESIÓN" son **históricos**.
> 1. ✅ Prueba de coste del arreglo con el techo mordiendo: **PASA** (14/14).
> 2. + 3. ✅ Fundidos por dirección. Examen de congelación, criterio v3: **PASA 20/20. v8 es el tronco**
>    (tag `v8-tronco`).
> 4. ✅ **3T confirmatorio sobre v8: SÍ, y REPLICADO en semillas 21–40.** ERR-13 cerrado.
>
> 5. ✅ **Etapa 2 CERRADA**, también en conducta: frontera hambre–supervivencia y **v9 = v8 + memoria de trabajo
>    de rechazo** (confirmatorio en semillas 21–40 y examen 20/20; tag `v9-tronco`).
>
> 6. ✅ **Etapa 3 CERRADA sobre v9**, en valor y en **conducta al primer encuentro**, con una característica
>    lineal. XOR no generaliza. La versión dura mide la degradación por interferencia.
>
> **Siguiente, en la escalera del brief: Etapa 4, memoria persistente** (borrar el mundo, matar el cuerpo,
> reproducirse; memoria cero, parcial o heredada).
>
> Pendiente sobre v9: re-correr 3T y 2K-bis. Abierto: frontera no lineal (XOR) y O7.
>
> Cola, sin fecha: 2P (política bajo hambre); A5 corregida (recuperación espontánea estructural); versión dura
> de Etapa 3; 3F (fusión).
>
> **Circula una copia externa del repo que afirma "v7 congelado": es falsa y no se fusiona**
> (`registro/AUDITORIA_copia_antigravity_20260916.md`).

> **ESTADO AL CIERRE DEL DÍA 3 (15 sep 2026).** Fase 0 y Fase 1: **HECHAS**. Etapa 3: primera mitad hecha.
> Ramas 3T, 3K y 2K-bis: cerradas, las tres con veredicto negativo y las tres útiles.
> v7 **NO congelado**. Detalle y criterios vivos en `REGISTRO_etapas_1_2.md`, sección "Día 3".
> Para retomar sin esta conversación: `registro/HANDOFF.md`, sección 9.

---

# PLAN PARA LA PRÓXIMA SESIÓN (escrito al cierre del día 3)

**Todo el proyecto converge hoy en un solo punto: BUG-01.** Tres ramas independientes que no se hablaban entre
sí (3T composición temporal, 2K-bis capacidad, y el propio arreglo) lo señalan como el cuello de botella real.
No es un detalle de implementación: es lo que impide la composición temporal, lo que baja la capacidad de v7
por debajo de la de v6, y lo que congela el 82% de los valores de v7 en 0.000 exacto.

## Paso 1 (el que importa) — BUG-01 experimento 2: decaer sólo la PARTE COMÚN
El experimento 1 (decaimiento uniforme) está **refutado con demostración**: la ventana de λ es vacía
(hace falta λ>0.015 para no saturar y λ<0.010 para no estropear W_B). El diagnóstico es que el decaimiento
uniforme ataca la **magnitud** y la patología es de **redundancia**.

Cambio a probar, UNO solo:

    m = np.minimum(Wp[ix], Wn[ix]);  Wp[ix] -= lam_c*m;  Wn[ix] -= lam_c*m

**Propiedad clave, que es la razón de elegirlo**: resta lo mismo a los dos canales, así que **`Wp − Wn` queda
exactamente intacto** y el valor neto sigue obedeciendo Rescorla-Wagner puro. Desaparece el sesgo del 1.1%
que hundió P2 en el experimento 1, y con él la tensión entre no saturar y conservar el valor.

Predicción a derivar y escribir ANTES de correr (base: la derivación validada del exp. 1, que acertó a 3
decimales): la redundancia `m` tiene equilibrio `m* ≈ 0.045/λ_c`; para `m* < 1` hace falta **λ_c > 0.045**.
Elegir λ_c a priori por ese argumento, no por barrido. Predecir explícitamente si el canal mayor (`Wn`, que
crece 3× más rápido por la aversión) puede seguir topando y bajo qué condición, porque eso decide si hace
falta el experimento 3.

**Experimento 3, si el 2 no basta**: normalización opuesta completa — `m = min(Wp,Wn); Wp -= m; Wn -= m`,
que impide por construcción que se acumule redundancia. Un cambio por experimento; no mezclar con el 2.

Reusar `experimentos/bug01/corre_bug01.py`: ya evalúa P1–P4 con los mismos criterios y produce datos con
cabecera de procedencia. Los controles de inercia (`lam=0` bit-idéntico) y de reproducción del bug son
obligatorios otra vez.

## Paso 2 — con BUG-01 arreglado, repetir 3T como CONFIRMATORIO
3T ya mostró post-hoc que, levantando sólo el bloqueo, la regla de división **descubre sola la dimensión
temporal**: `sep` 3.97, `lift` 0.34, 20/20, alcanzando el techo de la versión cableada a mano. Eso no cuenta
hasta repetirlo con criterio escrito antes y con el arreglo principista en lugar del techo subido a mano.
**Si sale, es el nivel 7 de la escala del punto 6 con criterio preregistrado.** Es lo más valioso pendiente.

## Paso 3 — v7, con la ley de disparo definitiva
La ley correcta es **`err_max > 0.6`** (concordancia 320/320, con derivación: `err_max = 0.147509·|R|`, que
exige `|R|` efectivo > 4.068, imposible sin recompensas de signo opuesto sobre la misma celda). Las dos leyes
que registré antes —"umbral en 2 celdas" y "valencia opuesta"— están **refutadas** como enunciados generales.
Reescribir el criterio de disparo de `bateria_v7b.py` en términos de `err` y volver a correr 20 semillas.
Ojo: v7 sólo debería congelarse **después** de arreglar BUG-01, porque 2K-bis mostró que v7 tiene menos
capacidad que v6 precisamente por ese bloqueo.

## Paso 4 — 2P, política bajo hambre
Sigue siendo el único problema abierto de conducta y ahora cuesta minutos con la Fase 1 hecha.
Antes de correr: escribir la función objetivo (propuesta: minimizar muertes sujeto a tasa de mordida de comida
≥95% por visita) y reportar **la superficie completa** de α × hambre_boca × sesgo, no el mejor punto.

## Cola de preregistros pendientes (ninguno corrido)
- **Etapa 3 versión dura**: la fórmula `W_X = 0.333·nA − 1.0·nB` sólo se probó donde no podía fallar. Correrla
  con códigos solapados, con el clip activo y con más de dos estímulos, donde sí puede romperse.
- **3F fusión**: la operación inversa de 2L. El organismo sabe dividir y no sabe juntar. Sin lanzar.
- **`hebb_mordida` rompe E2K** (18/20), única condición de 3K que lo hace.
- **Dirección de división 2L v2 en la tarea de 3K**: dio 0.763 contra 0.683 del azar, el mejor de ese estudio,
  aunque por debajo del margen.
- **Techo de v6 en capacidad**: no se estableció; el diseño de 20.000 pasos por estímulo mide muestreo, no
  capacidad. Hace falta un cuarto punto de tiempo o igualar mordidas por estímulo en vez de pasos.

## Lo que NO hay que tocar
- `.gitattributes` con `* -text`. Sin él, git convierte LF→CRLF y **rompe los 55 hashes** en cualquier clon.
- Los cuatro archivos congelados. `python manifiesto.py` los verifica y sale con código 1 si alguno cambió.
- Rama 2M (pulpo): refutada el día 2, no entra al tronco salvo decisión explícita.

---

## Fase 0 — Validar el traspaso (primera sesión, ~20 min)
1. `git init`, commit inicial con este bundle. Etiquetar `v6-baseline`.
2. `cd organismo && python3 bateria.py 6` → todo PASA. Luego `python3 bateria.py 20`.
3. Reproducir `datos/baseline_v6.csv`: 20 semillas, A_sin y B_aprende. Comparar medianas con el registro
   (comida 1400/338, veneno Q4 370/13, muertes 218/142, W_A +1.00, W_B −3.00). Si coincide, el traspaso está validado.
4. Añadir al registro una línea: "Traspaso validado en Claude Code, fecha, hash".

## Fase 1 — Infraestructura mínima (una sesión)
- `experimentos/run_etapa.py --etapa <nombre> --semillas N` que llama a `organismo_v6.run` con el escenario, escribe
  `datos/<etapa>_<fecha>.csv` y `.json` (por semilla: mord, vis, W, comp, deaths, log), y añade una línea al registro con hash.
- Paralelizar semillas con `multiprocessing` (una semilla por proceso). 100 semillas × 100k pasos debe caber en minutos.
- Script `analiza.py`: medianas, rangos, tasas por visita, y la comparación con el baseline.
- Convención: nunca sobrescribir un CSV; cada corrida tiene fecha.

## Fase 2 — Cerrar lo abierto de la Etapa 2
### 2L → v7 (PRIMERO)
`cd organismo && python3 bateria_v7c.py 20`. Si todo PASA (incluido divisiones=0 en etapas normales), renombrar a organismo_v7.py,
hash, commit `v7`. Luego repetir baseline 20 semillas con v7 y comparar con v6. Si algo falla, 2L vuelve a hipótesis.

### 2K-bis — Capacidad representacional (hipótesis derivada del organismo)
Pregunta: qué ocurre cuando la demanda de representación se aproxima al techo.
Condiciones (un cambio por corrida, 20 semillas): D∩B = 0,1,2,3 con clip=3; y D∩B=1,2 con clip=1.5.
Predicción: degradación graduada creciente con solapamiento (ya medida: W_B −3.00/−2.9/−2.78 en 0/1/2 celdas);
con 3 celdas (códigos idénticos) W_D y W_B convergen al mismo valor intermedio (fallo completo); con clip reducido
el fallo aparece a menor solapamiento. Refutación: si con 3 celdas los valores se separan, hay un mecanismo no identificado.
Métricas: W_D, W_B por cuarto; Wp/Wn de ambos; celdas al tope; tasas por visita; muertes.

### 2P — Política bajo hambre (NO recalibrar α a ciegas)
Antes de correr: decidir el criterio (adoptado: tasa por visita condicionada al hambre) y escribir la función objetivo
de la política (p.ej. minimizar muertes sujeto a no dejar de comer). Luego barrer α, β=hambre_boca y b=+0.5 como
hipótesis explícitas, 20 semillas, y reportar la superficie completa, no el mejor punto.

### Semilla congelada de v4
Con v6 no reaparece en 20 semillas. Correr 100 semillas de E1 y contar fallos (comida<100). Si 0/100, cerrar.

## Fase 3 — Etapa 3: Generalización (plan original, punto 10)
Hipótesis: el organismo aprendió "estos píxeles = comida" y no una característica abstracta.
Pruebas: patrones con 1 píxel cambiado (ruido), patrones desplazados, combinaciones. Medir W del patrón nuevo ANTES de
la primera mordida (valor a priori) y cuántas mordidas tarda en converger. Predicción con Kenyon: generalización
proporcional al solapamiento de códigos, no a la similitud visual — eso es una predicción falsable y distintiva.

## Fase 4 — Etapa 4: Memoria (punto 11)
Comparar memoria cero / parcial / heredada tras muerte. Ya sabemos: olvido 5% por muerte × 400 muertes = amnesia total.
Barrer olvido_muerte ∈ {0, .01, .05} y medir recuperación.

## Fase 5 — Población (puntos 12–14), solo cuando el individuo esté cerrado
Retomar `poblacion2.py` con v6. Cambios ya identificados (uno por vez): renacer heredando Wp/Wn del mejor (no en blanco);
score que pese el veneno; compartir solo el canal aversivo vs solo el apetitivo. Pregunta: ¿acumula la población algo que un
individuo no alcanza en una vida? Criterio de emergencia (punto 14): propiedad ausente en el individuo, presente en el grupo,
no programada, reproducible, y que desaparece al romper la estructura.

## Fase 6 — Publicación
- Repo público con README que reproduzca el baseline en un comando.
- Texto de ~3 páginas: la cadena 2A→2G como "un organismo que pide la teoría a golpes", con la limitación metodológica.
- Figura 1: valores W_A, W_B por cuarto en E1/E2 (12 semillas). Figura 2: interferencia vs solapamiento (0/1/2 celdas).
- Venue candidato: ALIFE / Artificial Life journal / arXiv q-bio.NC. No prometer más de lo que la batería demuestra.

## Reglas de sesión en Claude Code
Empezar cada sesión con la batería. Terminar cada sesión con una línea en el registro. Nunca dos cambios a la vez.
Traer el registro al chat de diseño cuando haya que decidir qué hipótesis sigue.
