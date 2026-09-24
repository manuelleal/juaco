# Proyecto: Organismo artificial mínimo (Artificial Life)

> **ESTADO VIVO (desde el 21-sep-2026): `registro/ESTADO.md`** — una página con tronco, niveles, pendientes, último ERR y decisiones; se
> reescribe en cada cierre. Los bloques "Estado (día N)" de abajo son historia y mandan sólo si `ESTADO.md` no los contradice.
> 21-sep-2026: v15f-v2 NO ENTRA (4 puertas de 7); BA cumple la misión cruda de la fase 5 ×2 pero no la letra R1–R5; LÍNEA CERRADA de memoria de pares en la vía lenta (v15c–v15g); líneas BA/BA-v y BA-vm/BA-vM CERRADAS (P6 cae ×3; BA-vm cruza P6 pero muere 9.6×; el valor falla por colisión estructural); fase 9 bloque 1 DECLARADO en parte con dos series válidas (1501–1520, 1621–1640): el cuerpo nuevo rechaza lo malo al primer encuentro sin dejar de comer y vive ~6.3× (H-1 en pie); F9-4 y F9-7 negativos ×3; **fase 9 bloque 1 DECLARADO COMPLETO** (F9-4bis replicado ×2: es el contenido del nodo, no cautela; ni el oráculo cruza R₀ 0.9: el muro es el mundo; C-F9B′ cerrado); propuesta nivel 9 → 50 %; criterio v3 calibrado con placebo: la serie acierta CAL-1..5 pero la réplica NO repite (CAL-1 0.898, CAL-4 un marginal fuera), v3 no utilizable, v4 pendiente; v2 rechaza al propio tronco en dos series (ERR-91); nivel 6 "rodeo obligado" CAE 5/10 (come más, no rodea); dE5 bajo el criterio v2 NO ENTRA (recupera 3.23× más rápido, pero muerde más veneno: cae T-A, T-C, T-E, T-G); ERR-87..90. Detalle en `registro/ESTADO.md`.
> 22-sep-2026: fase 10 externa integrada (calibración de F1 cae, RENACE 0.26 fuera de 0.8–1.3; H-BOCA reproducida en dirección 4/4); diagnóstico del muro (H-MURO se sostiene, pero discriminar mejor sólo suma ~6 puntos, no limpia el mundo); **criterio de tronco v4 calibrado y replicado, UTILIZABLE (v3 retirado)**; carrera de escuderías corrida completa (reglamento, 2 rondas, serie y réplica selladas): **primer cruce de H-1 en JUACO por la letra preregistrada** (R0 real de nacimientos 0.941, replicado sin la memoria del fundador) y **dos escuderías Opus estabilizan el bicho con recambio real de generaciones, replicado en sellada** (con muerte programada declarada; una tercera lo logra sin ella); mundo anclado v1 NO y v2 HAY ALGO MODESTO (REL cubre 0.73–0.75 del espacio NADA–ORÁCULO, cerrado con reservas); fanin CAE la hipótesis del director, replicada (nivel 7 sigue en 70 %); aprende_barrer/camino A HAY ALGO MODESTO pendiente de réplica (no corrida); generaciones que conviven con instrumento y quimiostato listos, sin series; propuestas pendientes del director: nivel 9 de 50 a 65 %, nivel 8 de 40 a 45 %, niveles 10–13 de ~10 a 15 %; ERR-94..113. Detalle en `registro/REGISTRO_etapas_1_2.md` y `registro/HANDOFF.md` 15.30.
> 23-sep-2026 (cierre parcial ~19:00; la cola sigue esa noche): tronco sigue **v14.2**; **nivel 7 FUNCIONA ×2** (el tronco v14.2 no componía, K_max 1; la reparación N compone hasta 8 y entra al v14.3); nivel 6 HAY ALGO MODESTO ×2 (rodea el veneno recordado por el hueco; cae V1); nivel 8 HAY ALGO MODESTO ×2 (sigue aprendiendo con celdas fijas; el cuello es de muestreo); aprende_barrer MODESTO replicado; nivel 10 NO SE LEE (ERR-116); convivencia con flujo fijo de comida NO (el cruce de H-1 del 22-sep depende de la reposición inmediata, ERR-104; ERR-118); serie del nivel 9: O3 cruza porque lee su estado presente (lesión 0.968 → 0.072), réplica en curso; ERR-114..118. **Plan vigente aprobado por el director: máximo 2 frentes — (1) v14.3, (2) gemelo rápido + JUACO-ECO por escalones.** Nube: `NUBE.md`; laboratorio de agentes investigadores: `registro/LABORATORIO.md`. Detalle en `registro/ESTADO.md` y `registro/HANDOFF.md` 15.31–15.32.
> 23-sep-2026 (noche, 22:15–23:15): tras un incidente a las ~21:55 (árbol local retrocedido sin commit; apartado con `git stash`, GitHub intacto) se relanzó la cola: **v14.3 HAY ALGO MODESTO ×2** (R0 real 0.63, vida ~9× v14.2, estabiliza 19/20, no gana); subida_n6b y subida_n8c HAY ALGO MODESTO ×2; n8b corriendo. Regla del director: en GitHub solo se agrega, nunca se retrocede. Detalle en `registro/ESTADO.md` y `registro/HANDOFF.md` 15.33.
> Índice de experimentos: `experimentos/INDICE.md`. Agentes y skills del equipo: `.claude/agents/` y `.claude/skills/` (y sección "Herramientas" de `registro/EQUIPO.md`).

Investigación reproducible sobre si un organismo artificial simple, con reglas locales y sin backpropagation,
puede aprender, desaprender, generalizar y (más adelante) transmitir conocimiento. Dirección: Christiam Puentes.
Colaborador técnico: Claude. Todo corre en CPU con Python 3 + NumPy.

## Fuente de verdad
- `registro/REGISTRO_etapas_1_2.md` — historial completo, criterios preregistrados, resultados, errores. LEER PRIMERO.
- `registro/HANDOFF.md` — narrativa completa de lo hecho y por qué.
- `registro/PLAN.md` — qué sigue y cómo.
- **`organismo/organismo_v13.py` — EL TRONCO desde el 17 sep 2026 (tarde)** (cc8b16b492d4d324, tag `v13-tronco`).
  **v13 = v11 + una VÍA LENTA y una PUERTA.** La vía rápida es v11 sin tocar (Kenyon + división por conflicto de signo,
  hallada por evolución). La lenta es una lectura **lineal directa de la retina** (`Wps`/`Wns` ∈ ℝ⁶, `eta_s = 0.015`),
  cada vía aprende de **su propio** error, y la boca consulta la rápida sólo si el patrón le es **familiar** (las 3
  celdas de su código con `|Wp−Wn| > 0.2`, el umbral de v11; `puerta = 3`); si no, consulta la lenta, que aprende la
  regla y no los casos. **Recuerda como v11 y generaliza mejor que v9: rompe el canje** (`v13_dos_vias_20260917_160541`,
  confirmado en 61–80: retención 20/20, acierto en nunca vistos 0.850). Examen **criterio v3'** 8/8 y
  `bateria_generaliza` (0.800 / 0.892) en semillas **101–120** (`examen_v13_20260917_165859`,
  `regresion_generaliza_organismo_v13_20260917_170148`). `organismo/bateria_v13.py` (1a027bcb37eb536e) es su examen.
  - **Criterio v3' (ERR-21):** el control negativo se desdobla: 3' la vía rápida sola sin plasticidad **falla** (0/20);
    3'' la lenta sin plasticidad **separa por píxeles** (20/20). Decidido y escrito ANTES de correr 101–120.
  - **Etapas 3 y 4 cerradas sobre el mismo tronco.** La lenta es lineal: **no** resuelve XOR (0.44), por diseño.
  - **3T sobre v13: SOBREVIVE** (T1–T6; `sep` 3.96; la lenta no lo resuelve por otra puerta). KT2 (C2b ≡ C1) no aplica a
    dos vías (**ERR-22**). **Capacidad sobre v13: CAE** como se predijo (N\* 28 y 35 de 60; v11 43 y 50; v10 6 y 9): la
    puerta manda a la lenta los estímulos sin 3 celdas consolidadas. **Canje conocido: puerta contra capacidad.**
    Datos `reverificacion_v13_20260917_171603`.
  - **Etapa 5, N1 (transmisión): CERRADA sobre v13.** Experto y novato; señal = conducta visible (+ muerde / − rechaza),
    honesta por construcción; vicario por las dos vías. Novato aprende B con 7–8 mordidas propias en vez de 19 (20/20);
    la señal barajada es destructiva (el contenido lo es todo); en el mundo invertido el novato corrige al experto
    (extingue 3× antes, 19–20/20) al precio de un pequeño coste de confianza. Semillas 1–20 y réplica 21–40. Datos
    `N1asim_20260917_175433`, `N1asim_s21-40_20260917_175924`. **Regresión (ERR-20):**
    `python experimentos/etapa5_comunicacion/corre_N1_asim.py --n 6 --desde 41`. Abiertos: N2 (significado emergente), N3.
- **`organismo/organismo_v11.py` — tronco del 17 sep 2026 (mañana a tarde)** (f69e24063be1b194, tag `v11-tronco`).
  v11 = v10 + **división por conflicto de signo**: una celda con valor consolidado (|Wp−Wn|>0.2) que recibe un refuerzo
  de signo contrario se divide en esa mordida; la hija nace **ciega fuera de los píxeles del patrón** que la dispara,
  **la madre no se mueve** y el valor se **fisiona** (la hija se lleva el signo nuevo, la madre conserva el viejo).
  **Es el primer órgano del tronco nacido por EVOLUCIÓN GUIADA** (JUACO-EVO, generación 1, operador LLM `gen1/llm_2`).
  Confirmatorio en semillas nuevas 41–60: retención **20/20** (v10 2/20, v9 0/20), capacidad **N\* 20/20 estímulos**
  (v10 5 y 8.5) usando **menos** celdas, examen criterio v3 **8/8** en 41–60. `organismo/bateria_v11.py`
  (17179642ad02269c) es su examen y su regresión. Datos `v11_confirmatorio_20260917_070339`, `examen_v11_20260917_071012`.
  - **ADVERTENCIA (17 sep, medido): v11 NO generaliza.** En patrones nunca vistos, el acierto de valor cae a **0.60**
    (v9 y v10: 0.80; azar 0.50); la conducta al primer encuentro baja de 0.80 a 0.67. **3T sí sobrevive y mejora**
    (`sep` 3.96 con 6 divisiones frente a 3.91 con 16). Datos `v11_generaliza_20260917_151145`.
  - **Por qué, y es el hallazgo:** en v9 las hijas se colaban en el código de casi todos los patrones (1 de cada 3
    celdas de un patrón nuevo); esa **fuga** llevaba valor a lo nuevo. **La generalización de v9 era su interferencia.**
    v11 tapa la fuga y desaparecen las dos: el olvido y la generalización. Es la predicción de CLS (McClelland,
    McNaughton y O'Reilly 1995), medida aquí con la línea exacta que la produce.
  - **Candidato a v12:** ceguera **graduada** de la hija (hoy es total: `kj * (P > 0)`), para recorrer el canje.
- **`organismo/organismo_v10.py`** (219d5033fe15b5b9): **NO es tronco** (ERR-17, y su réplica V10b falló). Congelado
  como **instrumento**: la identidad de v11 lo usa. v10 = v9 + `mu` normalizada en la dirección de división.
- **`organismo/organismo_v9.py` — tronco del 16 sep 2026 (tarde) hasta el 17 sep** (d3b72fb8819fbe8e, tag `v9-tronco`).
  v9 = v8 + **memoria de trabajo de rechazo** (`memoria_rechazo=20`): lo que la boca acaba de rechazar deja de ser
  objetivo de las patas durante 20 pasos. Pasó un confirmatorio en semillas nuevas (21–40) y el examen criterio v3,
  20/20. `organismo/bateria_v9.py` (c6496196990f6774) es su examen y su regresión.
- `organismo/organismo_v8.py` — tronco anterior, congelado como referencia (dca7d5c3a162f5d4, tag `v8-tronco`):
  v6 + 2L + drenaje de la parte común de Wp/Wn (`lam=0.05`). `organismo/bateria_v8.py` (8de16b2e97de8312).
- `organismo/organismo_v6.py` — tronco anterior, congelado como referencia (5f38f83cf49248a3). `organismo/bateria.py`.
- `organismo/organismo_v7.py` — instrumentación inerte de v7 (3db0475ef0ea95ce). **NO sobrescribir nunca**: de él
  dependen bateria_v7/v7b, los controles de inercia de BUG-01 y el ancla del sandbox. v7c/bateria_v7c: históricos.
- `datos/` — CSV/JSON de cada experimento. `datos/baseline_v6.csv` es el baseline de referencia.
- **`sandbox/` (fuera del repo, en `JUACO/sandbox/`) es de un ejecutor externo sin juicio; sus resultados son
  hipótesis, nunca datos.** Regla de cruce completa en `sandbox/README.md` y en el registro: nada entra aquí
  sin verificar hashes, reproducir en repo, pasar `bateria.py 20` y `manifiesto.py`, y etiquetar el origen.

## Reglas de trabajo (no negociables)
1. Antes de tocar nada: `cd organismo && python3 bateria.py 6` **y** `python bateria_v13.py 6` (tronco; `bateria_v11.py 6` y `bateria_v9.py 6` como regresión).
   **Antes de congelar cualquier tronco nuevo, además: `python bateria_generaliza.py <tronco> 20 --log`** (ERR-20:
   una etapa cerrada que no está en una batería no está protegida; así fue como v11 reabrió la Etapa 3 en silencio).
   Debe salir todo PASA (y `manifiesto.py --check` intacto). Si no, detenerse.
2. Un cambio por experimento. Cada experimento es una hipótesis con: qué cambia, predicción numérica,
   criterio de refutación y métricas — escritos ANTES de correr, en el registro.
3. Nunca recalibrar un parámetro a posteriori para que el criterio pase. Si el criterio estaba mal, se registra
   el error y se decide un criterio nuevo antes de volver a correr.
4. Distinguir siempre tres capas: representación (códigos Kenyon), valor aprendido (Wp−Wn), política (decisión bajo hambre).
   Un fallo de conducta no es un fallo de aprendizaje hasta que se demuestre.
5. Ante una anomalía, la primera hipótesis es el instrumento (criterio, unidades, aliasing, disponibilidad).
   Tres de tres anomalías del proyecto fueron del instrumento.
6. Semillas fijas (1..N), T=100000 salvo indicación. Reportar medianas y rangos, nunca solo medias.
7. Guardar cada resultado en `datos/` con nombre de etapa, y añadir una línea al registro con hash (sha256 corto) del script.
8. No declarar AGI, conciencia ni inteligencia general por ningún resultado. Vocabulario permitido: aprende, revierte,
   extingue, generaliza, transfiere — solo cuando el criterio preregistrado lo respalde.
9. Preferencia del director: preguntarle y proyectar hacia adelante, no frenarlo; discrepar con datos, no con cautela genérica.
10. **Todo script de más de un minuto: una línea de progreso por etapa con marca de tiempo, y salida a
    archivo DESDE EL ARRANQUE, no sólo al final.** Un script sano que calla seis minutos es indistinguible
    de uno colgado, y esa ambigüedad ya costó una salida entera (día 3). Referencia: `corre_ahorro.py`.
12. **Autonomía dentro del método (dirección, 17 sep 2026, noche).** Claude decide y ejecuta sin pedir permiso para
    decisiones de diseño, criterios y siguiente paso; el director audita después con el registro. No frenar por
    prudencia genérica ni esperar confirmación entre pasos. Método científico siempre (preregistro, controles, semillas
    retenidas, registrar el fallo) **y** método exploratorio siempre: la literatura es para leer resultados, no para
    limitar diseños; "si ya está escrito es que no funcionó aquí". Buscar más allá; cuando un mecanismo caiga, el
    siguiente intento se preregistra y se corre en la misma sesión.
11. **Repo y sandbox nunca corren a la vez; el repo tiene prioridad.** El sandbox arranca sólo con el repo
    parado y con `Pool(6)`, no 16. El tiempo de pared es un dato y se contamina al solapar.

## Estado (día 7 — 17 sep 2026, 23:00 → madrugada del 18; director ausente ~8 h, orden: "no parar", decidir, documentar, lo controversial a rama o copia). Manda sobre los bloques anteriores cuando se contradigan
- **TRONCO: v14.1 desde el 18 sep 06:05** (`organismo/organismo_v14.py` feefc88b1fd8d434, tag `v14.1-tronco`; = v14 con `eta_s` 0.15 y
  `clip_s` 10, medido sin coste: examen 8/8 ×2, generalización 1.000 / 0.97–1.00; examen `bateria_v14.py`, 16 congelados; v14 05:05 = tag `v14-tronco`) = v13 + hija dispersa por relevancia + puerta por evidencia del código exacto; con las dos perillas apagadas es
  v13 exacto. Evidencia: examen 8/8 ×3 rangos, generalización 1.000 / 0.95 ×3, capacidad 51, 3T-k 0.237 con 53 celdas; caso
  conocido: semillas 117/133 (E2 42 bocados). Candidata a v15: la sorpresa del mundo en la boca a dosis 5. **Regla 1 pasa a:**
  `cd organismo && python bateria_v14.py 6 && python bateria_generaliza.py organismo_v14 20 --desde 101` (histórica: v13, v11, v9).
- v13 (cc8b16b492d4d324) queda como tronco anterior. v14 **no lleva el mapa** (canje
  exploración/explotación cerrado como estructural: curiosidad, novedad de sitio ×2 dosis y saturación refutadas;
  `escala_s81-100_20260917_230039`, 05a712ef734aba56).
- **Resultados del día 7 (todos preregistrados, todos al final de `registro/REGISTRO_etapas_1_2.md`):**
  · **3e XOR REFUTADO** (`xor_3e_s61-80_20260917_231444`, 9d1c5071fd2a97b6): con los rasgos exactos {P0, P1, P0·P1, 1}
    la vía lenta da 0.625 (ruido 0.375) → la línea XOR queda **cerrada por hoy como cuello de DINÁMICA** (3, 3b, 3d, trío,
    3e descartan dimensión, puerta, regla e identificabilidad): refuerzo sólo al morder, −3/+1, clases desiguales.
  · **Nivel 6, dos metas y rodeo: HECHO y REPLICADO** (`rodeo_s41-60_20260917_232338`, `rodeo_s61-80_20260917_232711`;
    enmienda 1 con análisis del subconjunto válido escrita antes de la segunda serie): rodeo 0.725/0.750, pareado 14/14 y
    16/16, atajo ≥ 0.70, invertido 0.25, llega limpio ≥ 0.85. Vocabulario: *elige entre dos comidas recordadas y se desvía
    por el lado largo cuando el veneno recordado pesa; no planifica* (un paso, sin secuencia). Nivel 6 → 50 %.
  · **Bloque 6 allostasis (rama, 10 semillas) REFUTADO en su predicción** (`allostasis_s1-10_20260917_231652`,
    edb069ba16367139): la sorpresa no acelera la recuperación (0.856, 6/10); el predictor de la propia energía **sí**
    mide (error 0 en régimen, salta al cambio 10/10; retención y generalización intactas). Instrumento para la creación.
  · **N3d tercera serie 101–120 con el gemelo social en producción: 0.811** (`N3d_s101-120_20260917_233033`,
    cc5ca17e2e4bbf21; identidad 3/3 dentro del corredor) → replicado ×3 (0.822/0.811/0.811).
  · **N2 CERRADO CON DOS MUNDOS** (N2f v3 con montaje válido; INNATO 60 contra 278: el canal serviría con significado
    dado, aprenderlo por refuerzo no). Reabrir sólo con significado por predicción (célula de creación, creador C).
- **Gemelos compilados (numba), TODOS con arnés de identidad bit a bit y `--rapido` en su corredor:** tronco
  `organismo/organismo_v13_rapido.py` (72/72 + 180/180; ×58–78; `bateria_generaliza.py organismo_v13_rapido` 40/40
  contra la batería guardada de v13 en 101–120) · 3T-k `mundo_temporal_k_rapido.py` (146/146) · mapa `mundo_mapa_rapido.py`
  (90/90 + 81/81) · XOR `organismo_v13q_rapido.py` (81/81 + 243/243 + 81/81) · social `mundo_social_n3_rapido.py`
  (135/135, con las perillas de N2f v3; `corre_N3d.py --rapido`) · mundo largo/novedad `mundo_largo_n_rapido.py`
  (54/54 + 36/36 + 200k). Valen sólo mientras el arnés dé 100 % (repetir tras cambiar numpy/numba). Regla 9 de EQUIPO.md.
- **Equipo (regla 12 + decisión del director 17-sep 23:00): `registro/EQUIPO.md`.** Célula de creación activa:
  **tres creadores Opus** (A matemática del aprendizaje local; B representación y computación; C sistemas vivos y
  mente) + **explorador ligero Haiku** a demanda, con puente `registro/investigacion/PUENTE_creacion.md` (secciones
  propias; "Propuestas para el coordinador" en formato fijo; el coordinador convierte en bloques preregistrados; nada se
  declara sin ese paso). Sus copias viven en `experimentos/creacion_A|B|C/` (no tocan originales, no commitean).
  Primeros hallazgos de A (23:30): banco analítico que reproduce 3b/3d sin correr el organismo; **los dos canales
  (Wp, Wn) son exactamente un valor con signo + una masa de conflicto `m = min(Wp, Wn)`; `lam` sólo olvida `m`; la
  fisión de v11 es consolidación** (predice que la retención cae cuando el pool se agota). Auditor del día 7 en curso.
- **Madrugada del 18 (célula de creación → bloques preregistrados; `registro/PLAN.md` "orden vigente"):**
  · **B-1 HIJA DISPERSA (nivel 7) REPLICADA** — la hija nace ciega a parte del patrón (por medias de `P` condicionadas al
    signo de R): a k = 4/5 compone mejor que v13 (lift 0.31–0.35 contra 0.13; > v13 18/20 y 19/20) con la mitad de las
    celdas y una décima de las divisiones; gana a la máscara al azar 16/20 ×2; inerte a k = 1 (20/20 ×2). Serie 61–80
    cayó por la letra en el ahorro (16/20); enmienda 1 y serie 81–100 pasan incluso la letra original (19/20).
    Vocabulario: *"la hija que nace ciega a lo irrelevante compone historias más profundas con menos celdas"*.
    **v13D (copia del tronco con la perilla) NO REGRESIONA: examen v3' 8/8 en 101–120, G1 0.80 / G2 0.83, inerte en la
    retina de 6 px → CANDIDATA A v14** (`registro/PROPUESTA_v14.md`, rama `v14-candidato`); **v14 lo decide el director**. Hallazgo previo del creador B: el techo de la composición NO es el pool (duplicarlo a 180 no devuelve nada;
    46–55 de 90 celdas sin valor legible): es la evidencia por código. (`hija_dispersa_s61-80_20260918_000202`,
    `hija_dispersa_s81-100_20260918_000954`)
  · **A-2 metaplasticidad por masa de conflicto (nivel 8) REFUTADA** en 41–60: retención de lo ausente 0.667 = base
    (pareado 7/20), recupera más lento, +73 % muertes (`metaplasticidad_s41-60_20260918_000740`).
  · **A-1 selección por competencia (XOR)**: instrumento `organismo_v13q4` listo (identidad 16/16) pero la selección
    online abre el conjuntivo correcto 1/3 → **3f no se corre** hasta tener la pieza de muestreo (aprender sin morder,
    creador C). A-3 vector único (simplificación de la vía lenta con identidad algebraica) listo para correr.
  · **C-P1 "probar cuando no me reconozco" (nivel 9) REPLICADO ×2** (41–60 y 61–80): la sorpresa sobre la propia acción
    puesta en la boca (no en `eta`) recupera de la inversión en 0.26×/0.22× de los pasos de v13 (pareado 20/20 ×2), gana a
    los controles de cantidad (sesgo fijo) y de momento (traza rotada) 19–20/20, retención 20/20 × 6 y generalización
    intactas, sin más veneno ni muertes; sólo falla el apagado (15/20 ×2: el suelo es la cota de oráculo de su propia
    política). **Y el brazo dE-TEST — la sorpresa del mundo (ΔE, el predictor del bloque 6) en la boca — recupera 7× más
    rápido (0.14× ×2), se apaga sola (20/20 en 61–80; 41–60 retroactivo, ERR-27) y pasa seguridad: candidato PENDIENTE DE
    BATERÍAS** → **serie 81–100 (01:48): pasa retención (≥ 19/20 × 6) y generalización (G1 0.90): CANDIDATO A ÓRGANO con tres
    series (0.14× × 3)**; el automodelo pasa todo en la tercera (apagado 17/20); sus variantes (restar la cota, línea base
    lenta) refutadas como predijo C (auditoría de la madrugada: ERR-26 y ERR-27, regla 11 en EQUIPO.md). Lección: el predictor de ΔE nunca fue el problema, lo era dónde entraba.
    (`probar_si_mismo_s41-60_20260918_001756`, `probar_si_mismo_s61-80_20260918_003640`)
  · **Composición de los TRES (04:47): T1 8/8 + réplica 7/8 (E2, semilla 133, 42 bocados), T2 1.000 / 0.93, T3 0.24× → por la
    letra no van juntos: v14 = v13 + hija dispersa + puerta por código; la sorpresa en la boca (dosis 5) es candidata a v15.**
  · **A-3 CONFIRMADO**: la vía lenta de dos canales es exactamente un vector con signo (acc idéntica 60/60, |ΔW| 3e−15):
    simplificación candidata para v14 (mitad de memoria en la vía lenta; decisión del director).
  · **ERR-25**: la puerta de v13 no distingue "no aprendido" de "cancelado" (verificado por el auditor); B-2 (puerta por
    evidencia del código exacto) CORRIDO 41–60 (02:32): PATC recupera la capacidad de v11 en el paso largo (`N*` 50.5
    contra 35 de v13; 20 000: 41.5 contra 28, umbral 45 no alcanzado) con la generalización intacta (px0 1.000 / 0.96) y
    barajar los contadores la destruye (20/20); el examen v3' cayó por una semilla en E2 (19/20) y **la réplica en 121–140 da
    8/8 → tercer candidato a v14** (`PROPUESTA_v14.md`, rama `v14-candidato`); PAT (sin celda consolidada) falla 3'' como predijo B: la puerta también
    detecta conflicto. Tercer candidato condicionado en `PROPUESTA_v14.md`. **Examen v3'' completo de v13E (02:45): retención 8/8
    (criterio 5 adaptado, ERR-30) pero G1 px0 0.750 < 0.80 → la sorpresa del mundo en la boca queda FUERA de la propuesta a
    la dosis probada (coste 0.05 en generalización de valor). ERR-31: el runner leyó los umbrales de la batería y no los del
    preregistro; el registro sigue la letra. **Bloque de dosis (03:32): `k_testE = 5` cumple las seis condiciones a la vez
    (recuperación 0.267× en 121–140, 20/20; se apaga 20/20; G1 0.80; G2 0.857; K 20/20; examen v3'' 8/8) → SEGUNDO
    CANDIDATO a v14 a dosis 5 (`organismo_v14_candidato_sorpresa.py` en la rama); **réplica 141–160: 0.248× (20/20), retención
    20/20 × 6, G1 0.80** → dos series a dosis 5; k = 3 no (G2 0.842, examen 7/8).** · **Composición hija dispersa + puerta por código (03:55): examen 7/8 (E2 19/20 en
    101–120, la fragilidad de PATC solo), generalización 1.000 / 0.94, capacidad 51, composición 3T-k 0.237 (hija sola 0.251)
    → réplica del examen compuesto en 121–140: **8/8 → PROPUESTA CONJUNTA v14 = v13 + hija dispersa + puerta por código**
    (`organismo_v14_candidato_conjunto.py` en la rama `v14-candidato`; C3 0.237 registrado tal cual); **protección extra 04:22:
    examen 8/8 también en 141–160 y generalización 1.000 / 0.95 en 121–140** → cumple examen + baterías + réplica; faltan gemelo
    (en construcción) y congelación (decisión del director). La sorpresa en la boca (dosis 5, dos series) va aparte hasta
    medir la composición de los tres.** Auditoría del día 7 integrada
    (K0 del bloque escala re-diagnosticado; `analiza_subconjunto.py` para el rodeo; regla 10 en EQUIPO.md).
- **DECISIÓN DEL DIRECTOR (18 sep 05:10): frente único con DOS organismos en paralelo** — `SIN` (reglas locales: codificación
  predictiva + retorno asimétrico, el error de predicción de ΔE como señal común) y `CON` (backprop de laboratorio para
  descubrir la regla y como control positivo; nunca dentro del tronco); la medida que manda es *exposiciones hasta asociar*
  (aprender sin morder, pocos ensayos, como los insectos); representación en GRAFO (nodos y relaciones entre lo aprendido;
  la alta dimensión sólo como soporte). Mismo criterio de parada (`registro/PLAN.md`).
  **Bloque 1/3 (A-4, 05:35): las dos constantes de la vía lenta (0.15, 10) llevan la regla local a 1.000 con rasgos dados (150
  exposiciones) sin dañar el tronco (examen 8/8, G1 1.000); con rasgos propios XOR 0.50–0.63: el cuello es construir el rasgo
  conjuntivo (WTA lo abre 11/20). **Bloque 2/3 (A-6, 06:05): quitar la constante no desbloquea (0.500); con 8 patrones no hay
  información para seleccionar el rasgo (estadístico ideal 3/20); con 14 patrones la regla local llega a 1.000 en los nunca vistos
  (200 exposiciones). **DECISIÓN DEL DIRECTOR 07:10 (ERR-35): la línea XOR se cierra declarando el mínimo de ejemplos con el
  que generaliza — 14 sí (1.000), 11 no, 8 nadie puede (9 de 15 hipótesis empatadas); **BLOQUE 3/3 (07:43): M3 "memoria de un golpe por combinación" (sala de
  agentes) cruza XOR con 8 ejemplos: 1.000 en los 12 nunca vistos (registro y estricta), n* = 7, desempate al azar, azar en banda,
  con 14 patrones también 1.000 → PRIOR ESTRUCTURAL de pares (declarado, no "aprende la estructura"); **réplica 141–160 igual (1.000 / 1.000, n* = 10): LÍNEA XOR CERRADA** —
  vocabulario: "con 8 ejemplos XOR exige un prior de pares y con él bastan 7–10 exposiciones; con 14 no hace falta prior";
  candidatos v15c / v15d (08:06 / 08:38): NO entran al tronco — **ERR-38 (08:44): la batería de generalización copiada omitió eta_s/clip_s
  y el G1 0.500 de los dos era del instrumento (corregida: G1 1.000 los dos — la memoria de pares NO rompe la generalización lineal)**;
  v15d cae en el EXAMEN encendido: la tabla de un golpe no se desdice tras el cambio de regla (E2 0/20) y deja a la vía rápida sin
  consolidar (E1 0/20) → "la memoria de pares generaliza y cruza XOR con 8 ejemplos, pero no se desdice"; siguiente candidato con
  preregistro nuevo: tabla reescribible (v15e). **Mundo vivo (F, 07:58, 181–200): núcleo sostenido — valor por necesidad resuelve el
  XOR necesidad × estímulo (1.0, 20/20; tabla 2×4 exacta en 11 exposiciones), escalar 0.5, barajar el contenido lo destruye;
  supervivencia (P4′, P7) y sal (P6: |W| 1.83 en un estímulo que nunca informa = superstición) no como se predijo por el umbral (ERR-37), no por el efecto;
  **réplica 201–220 con enmienda 2 (08:20): pasa las dos series (A₁₂ 0.90–1.00; agua 1.85–2.05×) y P10 confirma el ALIAS DE CÓDIGO** —
  la sal hereda el valor del veneno sólo cuando comparten el código K=3 (2/20 semillas; bloque de la sal 08:16, 9 ALIAS contra 9 LIMPIAS:
  |W[sal]| 1.45 contra 0.0, veneno −1.45 contra −3.0; persiste sin sed (S-5) y la puerta de v13 no lo repara (S-6)) → cabo nuevo del
  nivel 4: desambiguar códigos. **v15d cerrado 08:46 (arriba). **Desambiguar códigos (B-5, 09:07 + réplica 09:12 en semillas nuevas): DECLARADO (nivel 4) — "cuando una celda con valor recibe nada bajo una retina distinta, divide: el código deja de prestar valor"; 18/18 semillas ALIAS: |W[sal]| 0.0, veneno −3.0, evitación ×7 → ×1, muertes a la mitad; tronco IDÉNTICO a v14.1 (examen 8/8, generalización 40/40) → candidato a v15 (perilla `desambiguar`), la entrada la decide el director; C4 (dónde cae la primera división) era un criterio de causa mal escrito (7/9 y 4/9).** **Propósito y reproducción (peldaño 2, 09:16, 221–240): la medida `descendientes_viables` SE TIRA (P-R1: ESCALAR y BARAJA_CON hacen más ventanas muriendo 1.5× más); saciado, el valor por el cuello de botella veta la sal (0.80 → 0.007) y CUELLO_MIN (mínimo de las dos filas, sin memoria nueva) lo hace igual o mejor: la tercera necesidad SOBRA; bloque 2 con medida ligada a la supervivencia en preregistro (ERR-40; ERR-39 = control de paja CUELLO).** **v15e (09:37): NO entra — se desdice (E2 20/20) y consolida (E1 W_B 20/20) con cada vía con su error, generaliza (G1 1.000), pero pierde XOR (0.500): la tabla del residuo hereda el fracaso de la lineal; v15f (R crudo + relevo) encargado. Revisor de literatura (09:45): ningún mecanismo nuevo (alias = colisión LSH + Rescorla; reparación = distinción útil/ARTMAP; XOR-8 = Mitchell 1980; valor por necesidad = RL homeostático); publicable como nota técnica reproducible del alias. SALA 2 (frontera: qué bloquea y cómo darle vida; 4 diagnósticos, 6 diseños, 12 refutadores, síntesis) corriendo desde 09:40 → `registro/investigacion/SALA2_frontera_20260918.md`. **Reproducción bloque 2 (09:43 + réplica 09:45, 261–300): 8/8 ×2 — la medida r = descendientes − muertes ordena como la supervivencia (ERR-40 resuelto); la lectura pesimista saciado (CUELLO_MIN, mínimo de las dos filas, sin memoria nueva) lleva el linaje al filo del reemplazo (r +3/−3, 9–11/20 ≥ 0) donde el tronco pierde 73–75; la tercera necesidad se retira → DECLARADO (nivel 9, 45 %); siguiente: población con herencia y muerte real.** **v15f (10:00): NO entra por el criterio v1 (dos subletras internas 17/20 y splits +16 %), pero es el primer organismo que GENERALIZA (G1 1.000), SE DESDICE (E2 20/20), CONSOLIDA (20/20) y CRUZA XOR CON 8 EJEMPLOS EN LA CONFIGURACIÓN DEL TRONCO (1.000 contra 0.500, azar en banda) → primer candidato para `CRITERIO_TRONCO_v2.md` (preregistro nuevo, semillas nuevas, réplica); ERR-44: "veneno Q4 < Q1" no distingue aprender de un golpe de no aprender.**
- **DECISIÓN DEL DIRECTOR (18 sep 2026, 09:55) — CAMBIO DE RUMBO.** Tras la mañana (cinco bloques preregistrados por hora, dos
  resultados declarados, ningún candidato de capacidad al tronco; revisor de literatura: ningún mecanismo nuevo), el coordinador
  diagnosticó cuatro cosas mal planteadas y el director decidió: *"Perfecto, hagamos esa modificación y registra todo"*.
  Lo que cambia, y lo que no:
  1. **Se conserva el método** (preregistro → commit → correr → registrar; ERR numerados; réplica antes de cerrar; regla 12; reglas 1–14 de
     EQUIPO). Es lo que nos salvó cinco veces hoy (ERR-38, 41, 42, 43; la medida de reproducción).
  2. **El mundo cambia por uno que obligue a representar:** estímulos compuestos (una "sal" y una "sal rosa": la variante como variable
     del mismo token), más píxeles que 6, recursos que se agotan, veneno que cambia — un mundo donde 16 patrones no basten y donde
     la tokenización, la variable y el desaprender sean necesarios para sobrevivir (ERR-35: el mundo de 16 patrones no contiene la
     información para elegir XOR; no se le vuelve a preguntar lo que no puede responder).
  3. **La estructura crece por reglas locales:** el organismo recluta y divide celdas cuando la sorpresa se repite en la misma
     combinación (conjunción por coactividad) y cuando un código con valor recibe otra consecuencia (B-5); ninguna capacidad nueva
     entra como perilla diseñada a mano si puede entrar como crecimiento.
  4. **El criterio de tronco cambia:** el examen v3′ 8/8 deja de ser la puerta absoluta (selecciona "no cambies nada": v15d/v15e
     murieron por detalles internos; sólo entró lo inerte). Un candidato nuevo se juzga por **sobrevivir y generalizar en el mundo
     vivo** (muertes, r = descendientes − muertes, nunca vistos, reversión: se desdice, sin alias) con **no regresión CONDUCTUAL** del
     examen (la conducta de cada escenario se conserva; los pesos internos no son puertas). El criterio v2 se escribe en
     `registro/CRITERIO_TRONCO_v2.md` ANTES de juzgar a ningún candidato con él; **v15c/v15d/v15e no se rejuzgan** (regla: no
     recalibrar después de ver datos); v14.1 sigue siendo el tronco hasta que un candidato cruce el criterio v2 en semillas nuevas.
  5. **Ejecución:** la SALA 2 (4 diagnósticos, 6 diseños, 12 refutadores, síntesis) entrega el diseño concreto del mundo y del
     crecimiento; de ahí salen los bloques preregistrados, en este orden: (a) `CRITERIO_TRONCO_v2.md`; (b) el mundo que obliga (mundo
     nuevo con v14.1 SIN cambios como control base: si el tronco ya sobrevive ahí, el mundo no obliga); (c) crecimiento estructural
     por sorpresa repetida (crece_codigo) medido en ese mundo; (d) tokens y variables ("sal rosa" cuelga de "sal"; separación cuando
     deja de comportarse igual); (e) población con herencia y muerte real (que viva). Una cosa a la vez en el Pool; réplica antes de
     declarar; "llegar a la frontera es lo primero, que viva lo segundo".
  
- **DECISIÓN DEL DIRECTOR (18 sep 2026, ~14:15) — PLAN APROBADO tras la síntesis de la SALA 2:** la misión sigue siendo llegar a la AGI por este camino ("si no la tenemos en la cabeza no llegamos"); con honestidad registrada de que estamos muy lejos. Plan: (1) bloque 0, escalar el código sin órgano nuevo (alias < 1 % con D = 12, cálculo estructural); (2) bloque 1, el mundo de familias que obliga a representar, medido primero con v14.1 sin cambios (si no se distingue de un lector lineal, el mundo se endurece); (3) después el órgano (v15f bajo el criterio v2, crecimiento por sorpresa) y al final población; (4) consolidar y publicar lo que hay (nota técnica reproducible del alias + banco de método) en paralelo, a un ritmo que no queme. Agentes en Opus; el coordinador verifica. Pendiente del director: B-5 como v14.2.
- **DECISIÓN DEL DIRECTOR (18 sep 04:55):** congelar **v14** (v13 + hija dispersa + puerta por código, + sorpresa en la boca a
  dosis 5 si la composición de los tres pasa), escribirlo como resultado cerrado y dedicar después el equipo a UN frente:
  **aprender sin morder** (muestreo de XOR / significado por predicción). **Criterio de parada:** tres bloques preregistrados;
  si ninguno cruza 0.75 en xor01, se acepta el techo, se publica y se cambia de paradigma o se cierra (`registro/PLAN.md`).
- **Tarde y noche del 18 (14:15 → 19:30), tras el cambio de rumbo:** bloque 0 (ningún tamaño de código baja el alias del 1 %: ERR-45); bloque 1 mundo de familias (la medida del colateral se cerró tras tres correcciones, ERR-46..49: el colateral no existe); bloque 2 (v14.1 lee la variante nunca vista 0.875 por linealidad; separa la que vira 4/8, sólo las que comía); bloque 3 (v15f 7/8, incluidas las que eran veneno, daño 0.042); bloques 4/4b (SEIS series: el receptor come a la primera lo que evitaba sólo por el mensaje, 15–19/20 contra 0–3/20; referencia de FAMILIA, no de variante: no declarado; ERR-50..54); salas 3 y 4 (agentes: protocolo del canal simétrico; 14 errores y 9 hipótesis, nivel real 4); línea externa (ChatGPT) reproducida (sin acción la memoria es inerte); **H-1 (19:28, dos series): con la muerte que borra la memoria, R₀ cae de 0.87–0.98 a 0.14–0.17 con cualquier herencia (barajado ≈ nada): ERR-62, este mundo no sostiene linajes mortales; el hijo nace vacío y muere antes de aprender → antes de población: aprender en menos de una vida o cuidado del recién nacido (preregistro nuevo).** En curso: H-4 varias ganadoras (cierra o no la comunicación). Pendientes del director: B-5 como v14.2, dE5, v15f bajo el criterio v2.
- **TRONCO v14.2 (18 sep 21:25, decisión del director ~20:40): v14.1 + B-5 (la división por conflicto se dispara también cuando una celda con valor recibe R = 0 bajo una retina distinta; repara el alias de código, 18/18 en dos series; inerte en los mundos del tronco). Archivos `organismo/organismo_v142.py`, `organismo_v142g.py`, `bateria_v142.py`, `bateria_generaliza_v142.py` (20 congelados). Regla 1 desde ahora: `cd organismo && python bateria_v142.py 6 && python bateria_generaliza_v142.py organismo_v142 20 --desde 101` (21:20: examen 8/8 True; G1 1.000, G2 0.967, K 20/20). Identidad 62/62 (`identidad_v142.py`); tag `v14.2-tronco`. v14.1 queda como regresión histórica.**
- **Remoto:** `origin = https://github.com/manuelleal/juaco.git` (al día; push tras cada bloque); respaldos locales `JUACO/respaldo/juaco_bundle_*.bundle`.
- **Lista de chequeo niveles 3–8: `registro/HANDOFF.md` §13** (3: 70 % · 5: 50 % · 6: 50 % · 7: compone hasta 3 ·
  8: canje estructural, retención de lo ausente 0.67). **Orden vigente: `registro/PLAN.md`** (día 7 y lo que sigue).
- **Abierto tras el día 7:** XOR por dinámica (creación A); presupuesto de celdas en composición (creación B, dendrita
  de dos ramas); retención de lo ausente (creación A, metaplasticidad por masa de conflicto, cero memoria nueva);
  significado por predicción / modelo de sí mismo (creación C, `organismo_v13s`); nivel 6 horizonte > 1 (en un anillo
  la dirección ya integra todo el horizonte: planificar de verdad exige un mundo 2D — decisión del director); rodeo
  falso; N2 sólo con significado por predicción.

## Estado (día 5 — 17 sep 2026, noche). Manda sobre los bloques de los días 4 y 3 cuando se contradigan
- **Tronco: v13** (`organismo/organismo_v13.py`, cc8b16b492d4d324, tag `v13-tronco`; examen `organismo/bateria_v13.py`,
  criterio **v3'**). Linaje del día: v9 → v10 (sólo instrumento; ERR-17) → **v11** (tag `v11-tronco`; división por
  conflicto de signo, **órgano nacido por evolución guiada**) → **v13** (v11 + vía lenta lineal de la retina + puerta de
  familiaridad). **14 archivos congelados** (`manifiesto.py --check`).
- **Etapas del brief:** 1 ✅ · 2 ✅ · **3 ✅ (v13: 0.80–0.90 en patrones nunca vistos)** · **4 ✅ (v11 → v13: retención
  20/20)** · **5 N1 ✅** (transmisión experto → novato por conducta visible; réplica en 21–40) · **5 N2 ❌ REFUTADO en
  el primer intento y LÍNEA CERRADA por hoy tras cinco diseños (N2–N2e, 500 corridas)**: emerge una **convención**
  de dos símbolos, arbitraria (13/20) y que muere al barajar, pero **sin magnitud útil** (contraste ±0.4) por la
  asimetría del mundo (la comida desaparece al comerla; el veneno se queda y se señala 36.000 veces) y de la
  recompensa (−3/+1). Reabrir sólo cambiando el mundo. Datos `N2*_s1-20_20260917_*`. · **Plan vigente: el del debate**
  (`registro/investigacion/DEBATE_y_plan_5a10.md`): (1) 3T con k=2,3 → (2) tabla posición→código → (3) mundo social
  con control de saciedad (N3) → (4) mundo largo con cambio, 4 brazos (niveles 8+9). · **(1) HECHO: 3T-k, v13
  compone historias de 1, 2 y 3 pasos con distractores, replicado** (`3T_k_s1-20_20260917_191732`,
  `3T_k_s21-40_20260917_192053`; sep 3.97/3.74/2.24, control barajado ≈ 0, ≥19/20 en cada k). · **(2) HECHO: mapa
  (`experimentos/nivel6_mapa/`), v13 + tabla M elige la dirección hacia comida recordada fuera de la vista, replicado**
  (0.81/0.80 contra 0.48/0.50 sin mapa; invertido 0.11/0.13; come 490 contra 332, 20/20; `mapa_s1-20_20260917_192813`,
  `mapa_s21-40_20260917_193133`). Premisa corregida: la retina del tronco ve el objeto más cercano de todo el anillo,
  el mundo del mapa necesita `r_vis=3`. · **(3) N3 sentidos complementarios: N3 ❌, N3b ❌ (ERR-23: canal simétrico y
  acierto no balanceado), N3c montaje inválido (el receptor memoriza sus 8 objetos fijos); la conducta ajena SÍ gobierna
  al receptor (barajada 0.68 / emisor que no sabe 0.69, 20/20). **N3d ✅ TRANSFIERE** (4 parejas misma
  vista/valencia opuesta: receptor ciego 0.515 solo → 0.822 con la conducta del que ve; barajada 0.48; emisor que no
  sabe 0.51; 20/20 en los tres; `N3d_s61-80_20260917_200706`; réplica 81–100 igual: 0.811 contra 0.516 solo, barajada 0.487, emisor que no sabe 0.515, 20/20 en los tres (N3d_s81-100_20260917_201205, 454fb54abddb2146)).** · **(4) mundo largo (`nivel8_mundo_largo/`): compuesto ❌;
  v13 sigue aprendiendo hasta los 50 patrones (0.80), se recupera de la inversión en ~2 000 pasos (18/20), el mapa
  daña la adquisición (0.70 vs 0.88)** (`largo_s1-20_20260917_200026`). · Resumen de la noche: HANDOFF 11.6.
- **Gemelos compilados (numba), cada uno con su arnés de identidad bit a bit; valen para confirmar SOLO mientras el arnés
  dé 100 % (repetirlo tras cualquier cambio de numpy/numba):** tronco `organismo/organismo_v13_rapido.py` (72/72 +
  ampliada 180/180 del revisor; ×58–78) · 3T-k `experimentos/nivel7_3T_k/mundo_temporal_k_rapido.py` (146/146; ×45–74;
  `corre_3T_k.py --rapido`) · mapa `experimentos/nivel6_mapa/mundo_mapa_rapido.py` (90/90 + 81/81; ×30 con mapa;
  `corre_mapa.py --rapido`) · mundo de regla/XOR `experimentos/nivel7_xor_lectura/organismo_v13q_rapido.py` (81/81 +
  243/243 + 81/81; ×68–113; `corre_xor*.py --rapido`; `bateria_generaliza.py organismo_v13_rapido`) · social
  `mundo_social_n3_rapido.py` (84/84 en el agente, ×60; en actualización con las perillas de N2f v3) · mundo largo /
  novedad: en construcción. Regla 9 de `registro/EQUIPO.md`
  (nunca recursión con `cache=True`; sumas por pares de NumPy; empates de argsort a NumPy).
- **Bloque 1 (día 6) HECHO:** 3T-k compone hasta 3 replicado (k=4: separa en dos series pero la ventaja conductual no cruza
  0.15 en la réplica 41–60; k=5 agota el pool 90/90); retención de lo ausente en el mundo largo
  0.67/0.50 (interferencia, no inversión; `largo_s21-40_20260917_204840`); N3d mudo 0.503 = obedece, no enseña
  (`N3dmudo_s61-80_20260917_205345`). Registro al final de `REGISTRO_etapas_1_2.md`.
- **Bloque 5 (N2f v3) REFUTADO con montaje válido → N2 CERRADO CON DOS MUNDOS** (`N2f_s81-100_20260917_222744`):
  emisiones equilibradas 0.23, novato aprende solo, y aun así contraste ±0.3, sin beneficio, barajar no destruye; INNATO 60
  contra 278 solo: el canal serviría con significado dado; aprenderlo por refuerzo no funciona. Bloques 2 (curiosidad) y
  2 bis (novedad de sitio, dos dosis) refutados: el canje del mapa se desplaza, no se rompe.
- **Bloque 3 REFUTADO como estaba escrito** (`xor_lectura_s1-20_20260917_213124`): la vía lenta cuadrática aprende XOR
  (W del producto P0·P1 = −2.65) pero el acierto en nunca vistos sigue en 0.438; hipótesis 3b: la puerta esconde la vía
  lenta (familiar por solapamiento ≠ conocer). Regresión px0/azar intacta. **3b: hipótesis de la puerta REFUTADA**
  (`xor_3b_s21-40_20260917_213752`): la vía lenta cuadrática sola da 0.50 en XOR; los marginales de P0/P1 se drenan a
  cero → el límite es la REGLA de la vía lenta (reparte el error por igual entre entradas activas), no la dimensión ni
  la puerta. 3c (regla delta con signo) lo diseña un trío de agentes con puente (`registro/investigacion/PUENTE_xor.md`).
- **Bloque 2 REFUTADO:** la curiosidad por progreso de error no devuelve la exploración al mapa (0.700 = mapa = barajada;
  v13 0.900; comida intacta) (`curiosidad_s41-60_20260917_211739`). Siguiente candidato: novedad de sitio.
- **EQUIPO de agentes (decisión del director, 17-sep 21:45): `registro/EQUIPO.md`** — misión, reglas y roles (coordinador,
  compiladores de mundos, diseñador, auditor, cronista). Un solo `Pool` a la vez; los agentes no commitean.
- **PLAN DEL DÍA 6 (vigente): `registro/PLAN.md`, bloque de arriba.** Bloque 0 gemelo rápido con identidad bit a bit (hecho para el tronco); bloque 1 hecho; bloque 2 refutado;
  bloque 1 cabos (3T-k k=4,5; `W` por patrón en el mundo largo; N3d sin emisor); bloque 2 curiosidad por progreso de
  error contra el canje del mapa; bloque 3 XOR como límite de lectura (vía lenta cuadrática); bloque 4 decisión v14
  sólo si pasa el 2; bloque 5 N2b en el mundo con reaparición; bloque 6 rama allostasis. Tronco sigue siendo v13. **Ojo N1:** la señal de conducta mezcla valor y saciedad (INNATO en el
  mundo de 20 patrones deja 0/10 comidas conocidas).
- **Hallazgos del día, en orden:** (a) **JUACO-EVO**: 4 mutaciones LLM contra 24 ciegas; el LLM halló en **una**
  generación un órgano que yo no diseñé (P1 sostenida; `experimentos/evo/LINAJE.md`). (b) v11 cerró la Etapa 4 y
  **multiplicó la capacidad** (mundo grande: 50 de 60 frente a 9 de v10); el límite no es el pool de celdas: degrada
  suave. (c) **"La generalización de v9 ERA su interferencia"**: las hijas de v9 se colaban en el código de todo patrón
  nuevo (fuga 1.00 de 3) y v11 lo tapó (0.08): perdió la Etapa 3 (0.60). Confirmado con D1–D4 y Spearman +0.60/+0.33.
  (d) **El canje es una perilla vista por dos lados**: v12 (ceguera graduada, superficie completa) no lo rompe; la hija
  que madura tampoco. (e) **Dos vías + puerta de familiaridad lo rompen (v13)**: recuerda 20/20 y generaliza 0.85,
  confirmado en 61–80 y examen en 101–120. (f) **Canje nuevo, medido: puerta contra capacidad** (v13 35 de 60; v11 50).
  3T sobrevive sobre v13. (g) **Etapa 5 N1**: el novato aprende el veneno con 7–8 mordidas en vez de 19 mirando cómo el
  experto lo rechaza; la señal barajada es destructiva; en el mundo invertido **el novato corrige al experto** (3× antes).
- **Errores nuevos (ERR-17 a ERR-22):** 17 criterio Q3 de v10 mal escrito (empates contados como fallo); 18 evaluador
  EVO explotable por constantes de constitución; 19 mutación nula ganaba por contabilidad; **20 una etapa cerrada sin
  batería no está protegida** (→ `bateria_generaliza.py`, obligatoria antes de congelar); **21 el control negativo del
  examen asumía una sola vía** (→ criterio v3': 3' la rápida sola sin plasticidad falla, 3'' la lenta separa);
  22 la identidad C2b≡C1 de 3T, ídem. **Regla derivada:** al cambiar la arquitectura, revisar TODAS las identidades y
  controles, no sólo los criterios científicos.
- **Cómo se cambió un criterio de congelación sin trampa (ERR-21 → v3'):** se escribió el criterio nuevo, se justificó,
  y **se repitió el examen ENTERO en 20 semillas nuevas (101–120) antes de congelar**. Si vuelve a pasar, es así.
- **Regresión del tronco (regla 1):** `cd organismo && python bateria_v13.py 6 && python bateria_generaliza.py organismo_v13 10`
  y `python experimentos/etapa5_comunicacion/corre_N1_asim.py --n 6 --desde 41`; `bateria_v11.py 6` y `bateria_v9.py 6`
  como regresión histórica.
- **Datos clave del día:** v11 `v11_confirmatorio_20260917_070339`, `examen_v11_20260917_071012`; mundo grande
  `capacidad_grande_20260917_142455`; canje `v11_generaliza_20260917_151145`, `fuga_20260917_152707`,
  `v12_superficie_20260917_154123`; v13 `v13_dos_vias_20260917_160541`, `examen_v13_20260917_165859`,
  `regresion_generaliza_organismo_v13_20260917_170148`, `reverificacion_v13_20260917_171603`; N1
  `N1asim_20260917_175433`, `N1asim_s21-40_20260917_175924`.
- **Abierto:** N2 (en curso) y N3; una puerta que consulte la lenta sólo con la rápida **vacía** (rama, para recuperar
  capacidad sin perder generalización); techo real de capacidad (el mundo de 60 se queda corto); O7; consolidación y
  publicación (`registro/HORIZONTE_frontera.md`, `registro/REFLEXION_agi.md`). Dirección: *"avanzar más que frenar,
  siguiendo el método; los modelos pueden hallar soluciones que la literatura no tiene"* (v11 lo demostró).

## Estado (día 4 — 16 sep 2026). Manda sobre el bloque del día 3 cuando se contradigan
- **v8 ES EL TRONCO (tag `v8-tronco`).** Pasos 2 y 3 fundidos por dirección: examen criterio v3 20/20
  (`experimentos/congelacion_v8/PREREGISTRO_congelacion_v8.md`, datos `examen_v8_20260916_145204`).
  - 4c: C∩B=3 de misma valencia → **0 divisiones**, y C hereda `W=−3.00` sin experiencia propia.
  - 4b: sin conflicto no hay división, 61/61.
  - En las seis etapas v8 no trunca nunca (ahí es v7); lo que lo distingue es la prueba de coste.
- **v7 NO se congeló nunca como tronco y `organismo_v7.py` no se toca.** Hay una copia externa del repo
  (`PROYECTOS/Nueva carpeta/bundle`) que afirma "v7 congelado": es **falsa** y no se fusiona nunca
  (`registro/AUDITORIA_copia_antigravity_20260916.md`).
- **ERR-12:** "ley de disparo `err>0.6`, 320/320" era una **identidad del código** (la división compara la misma
  cantidad), y "con solapamiento 0 no puede disparar" es **falso**: E2 divide con A∩B=0 por conflicto temporal.
  No citar esa concordancia como evidencia.
- **La prueba de AHORRO del día 3 SÍ corrió** y su lectura es nula por ERR-11.
- **Paso 1, prueba de coste con el techo mordiendo: PASA**, con 14/14 predicciones preregistradas
  (`experimentos/bug01/PREREGISTRO_coste_techo.md`, datos `coste_techo_20260916_142116`).
  - Antes de la primera truncación del clip, `lam=0` y `lam=0.05` son **idénticos** (20/20).
  - Después, el control no reaprende nunca; el arreglo tiene ahorro 0 y coste 0 en todos los ciclos.
  - **La objeción de "memoria latente" queda respondida:** no hay nada a la venta.
- **BUG-01 también aparece sin código compartido:** siete inversiones seriadas con A∩B=0 dan `W=0` y canales
  9/9 (derivado antes y medido 20/20).
- **Corrección de 2K-bis:** el rango dinámico explica el colapso a W=0 y la capacidad útil (M_max 4 → 8), no el
  techo N* a 20k (igual en 19/20).
- **Fase 4, 3T confirmatorio sobre v8: SÍ** (`experimentos/3T_confirmatorio/`, datos
  `3T_confirmatorio_20260916_150727`).
  - Con v8, la regla 2L separa sola el canal temporal: `sep` 3.97 y `lift_q4` 0.34 en 20/20. El control de ruido
    no lo logra.
  - **Predicción exacta:** v8 reproduce PH3 del día 3 semilla a semilla (C3 20/20). El único bloqueo de 3T era
    BUG-01.
  - **REPLICADO en semillas nuevas 21–40** (`datos/3T_replica_s21-40_20260916_151902`), con el comparador
    corregido **antes** de verlas: E 20/20 y 14/14, `sep` 3.99, `lift` 0.35.
  - **ERR-13 (el comparador distinguía `0.0` de `-0.0`) queda CERRADO:** el SÍ ya no depende de esa corrección.
  - Alcance: memoria de una mordida.
- **Etapas del brief (punto 16):**
  - 1 cerrada.
  - **2 CERRADA en valor (día 2) y en conducta (día 4, v9).**
    - Explora lo temido con hambre para poder revertir; la frontera está medida y `hb = 2` es el óptimo.
    - Ya no se queda atado a lo rechazado: memoria de trabajo, veneno 21% → 9.5%, menos muertes, confirmado en
      semillas 21–40.
  - **3 generalización CERRADA (día 4, v9)** (`experimentos/etapa3_v9/`, datos `etapa3_v9_20260916_164240`).
    - Con una regla lineal, patrones nunca vistos: valor 0.80 frente a 0.50 del control.
    - **Conducta al primer encuentro:** muerde comida nueva 70% y veneno nuevo 15% (control 48/47), 18–19/20
      semillas.
    - XOR no generaliza (0.44).
    - La versión dura cuantifica la degradación por solapamiento (0.007 → 0.20 → 0.63 → 1.41).
  - **4 memoria persistente: NO cerrada** (`experimentos/etapa4_v9/`, datos `etapa4_v9_20260916_170519`).
    - Exacta sin experiencia.
    - Pero **olvido catastrófico:** aprender C y D mientras A y B no están lleva el miedo a B de −2.92 a −0.34
      (conserva 7/20).
    - Dos vías: valor por celdas compartidas y divisiones que reescriben códigos (r = 0.87; sin plasticidad, 10/20).
    - Heredar el valor ahorra 80% del veneno inicial en un mundo igual (20/20); en uno invertido la desventaja va en
      la dirección predicha, pero no es consistente.
    - **Falta un órgano de consolidación.**
- **3T y 2K-bis re-verificados sobre v9:** sobreviven (datos `reverificacion_v9_20260916_165658`).
- **Consolidación (exploración, subagente):** el olvido es la **toma del código de B por celdas hijas** (`mu` no
  convergida).
  - **K4, repaso desde un almacén episódico:** retiene 17–20/20 aprendiendo lo nuevo, pero la memoria vive en el
    almacén (control 9/20): "memoria escondida".
  - **K5, `mu` normalizada** (1 línea): arregla la mitad sin almacén (10/20) y hace 2L más económica.
  - **v10 (K4, K5 o ambos) lo decide dirección.**
- **Comunicación N1 (señal innata de placer/asco + aprendizaje vicario): NO demostrada** (datos `N1_20260916_174236`).
  - Veneno hasta el criterio 18 frente a 19; simbiosis 9/20.
  - Sí importa el contenido (la señal barajada empeora).
  - Dos aprendices igual de ignorantes no tienen nada que enseñarse: rediseñar con **asimetría de información**
    (experto y novato).
  - Ser dos cuesta +34% de muertes.
  - Diseño completo N0–N3 en `experimentos/etapa5_comunicacion/DISENO_comunicacion_simbiotica.md`.
- **ERR-14, 15 y 16 (día 4, tarde):**
  - ERR-14: banda de validación más estrecha que el ruido de Poisson.
  - ERR-15: línea de azar mal puesta (5% en vez de 9.2%) y "parado" que en realidad era oscilación.
  - ERR-16: control τ=1 que no podía hacer nada por construcción.
- **Pendiente sobre v9:** re-correr 3T y 2K-bis (eran de v8); O7 "qué hacer sin objetivo".
- **Lectura de "órganos" (exploración, día 4):** el órgano que faltaba para decidir dónde ir era **memoria de
  trabajo**. Vincular valor→movimiento, habituación y exploración por sorpresa no sirvieron tal como se probaron.
- **Siguiente (sin fijar):** 2P, política bajo hambre; A5 corregida; Etapa 3 versión dura; 3F, fusión. Lo decide
  dirección.
- **Primitivo nuevo:** "mordida del techo" = **truncación** del clip, no el valor del canal. Tocar 3.0 no es morder.

## Estado (día 3 — repo en Claude Code, 15 sep 2026)
- **Traspaso VALIDADO**: batería 20/20, baseline reproducido bit a bit (259/260 celdas; la única diferencia es
  redondeo del CSV viejo). Repo git con tag `v6-baseline`. `.gitattributes` con `* -text`: sin eso, git convierte
  LF→CRLF y **rompe los 55 hashes sha256 en cualquier clon**.
- Etapa 1 (aprende A/B): cerrada, 20/20 en v6.
- Etapa 2 (inversión, extinción, estímulo nuevo, valencias opuestas): cerrada en valor. Ver registro.
- Problema abierto de conducta: política bajo hambre (mordidas de veneno 1–4% por visita en inanición). Fase 2P.
- **v7 NO congelado**, tras dos exámenes con criterio preregistrado. Los criterios científicos pasan 20/20 en
  las seis etapas y el control negativo es válido (0/20); lo que falla es el criterio de disparo en E2I.
  v6 sigue siendo el tronco.
- **Ley de disparo de 2L, definitiva: `err_max > 0.6`.** Concordancia 320/320 sin excepción, frontera de
  cuchillo (0.5996 no divide, 0.6003 sí), y derivación cerrada: `err_max = 0.147509·|R|`, así que cruzar θ
  exige `|R|` efectivo > 4.068 — imposible sin recompensas de signo opuesto sobre la misma celda.
  **Con solapamiento 0 la regla no puede disparar.** Las dos leyes previas del día 3 ("umbral en 2 celdas" y
  "valencia opuesta") están REFUTADAS como enunciados generales: con A∩B=1 co-aprendido desde t=0 dividen
  8/20, y con solapamiento 2 de misma valencia dividen 0/20. El recuento de celdas era un proxy.
- **BUG-01, bloqueo real del tronco y lo más importante pendiente**: bajo refuerzo contradictorio sobre un
  código compartido, `Wp` y `Wn` corren los DOS al techo (9.0/código) y su diferencia se anula exactamente;
  a partir de ahí no se aprende nada en esas celdas. Reproducible sin tocar nada:
  `organismo_v7.run(1, plast=False, solap_AB=3)` → `comp A=(9.0, 9.0)`, `W=0.0`.
  Es el "v6 colapsa: W=0" de 2L, el "ambos canales saturan" de 2F y los "canales inflados" de 2J/2K.
- **La regla de división no selecciona por dirección, selecciona por parada** (rama 3T): `P − mu[c]` es
  distintividad no supervisada y el control de ruido separa MÁS que la señal. Lo que selecciona es el error
  que dispara y apaga la división.
- Rama 3T (composición temporal, nivel 7): **NO** con las constantes actuales. Post-hoc, levantando sólo el
  techo de BUG-01, sí emerge 20/20 — no cuenta hasta repetirlo con criterio escrito antes.
- Rama 3K (¿debe aprender el Kenyon?): **NO, basta el azar** para características lineales. Aprender KW mejora
  la representación y no mejora la generalización: descorrelacionar códigos ≠ representar la característica.
- **Fase 1 hecha**: `experimentos/run_etapa.py` + `analiza.py`, paralelo 6.3×, equivalencia 20/20 bit a bit.
  Desbloquea las 100 semillas del punto 8 del brief.
- **Etapa 3 (generalización): predicción sostenida al 100%**, residuo exactamente 0.000 en 1.280 pares.
  Alcance nulo: 15.9% de los patrones reciben W=0 exacto. PERO el diseño era demasiado fácil (la identidad es
  mecánica con A∩B=0); la versión dura está preregistrada y sin correr.
- Variabilidad y diversidad medidas por primera vez: **sd(W_A)=0.0000** — el valor aprendido no tiene diversidad
  entre semillas; la conducta sí (CV 7–9%).
- 2K-bis redefinida por decisión del director: capacidad = nº de estímulos y celdas gastadas por estímulo.
- Rama 2M (pulpo/distribución): refutada a 6 estímulos; especialización emerge. NO tocar salvo decisión explícita.
- Bug de sincronía sensor-acción corregido en v6; cifras anteriores a v6 se reproducen aproximadamente, no exactamente.
- **BUG-01 exp. 2 (decaimiento de la parte común, `organismo_v7e.py`): mecanismo CONFIRMADO, criterios míos
  refutados.** Techo despejado 20/20 con λ_c ≥ 0.0125 (frontera derivada a priori: 0.01125), `Wp`/`Wn` en
  1.77/3.04 contra 1.8/2.8 predichos, `W_A=+1.000` y `W_B=−3.000` **exactos** (P3), ley de disparo intacta
  (P4), seis etapas 20/20. **`W` sale idéntico a tres decimales para λ_c en un rango de 24×: el arreglo no
  cuesta nada en valor neto.** P1 cae sólo por la dispersión de `W` (supuse mezcla 50/50; la fija la política).
  **v7e NO se congela. v6 sigue siendo el tronco.**
- **λ_c es un INTERRUPTOR, no una perilla** (decisión de dirección, 15 sep). Por encima de la frontera
  derivada (0.01125) el resultado no depende de su valor: `W` sale idéntico a tres decimales en todo el
  rango probado. **No se vuelve a barrer.** Lo único que elige λ_c es dónde queda el equilibrio de `Wp`/`Wn`,
  y eso sólo importa para el miedo latente — que lo mide la prueba de ahorro, no un barrido.
- **Prueba de AHORRO preregistrada y SIN correr** (`experimentos/bug01/PREREGISTRO_ahorro.md`): mide si el
  arreglo vende el miedo latente que compró 2F. Exigida por dirección antes de congelar nada. Criterio: si el
  ahorro cae bajo el 50% del de v6, no se congela por defecto. Ojo: `Wp`/`Wn` sólo cambian dentro de
  `if mordio:`, así que **con `A∩B=0` la recuperación espontánea es imposible por construcción**.
- **Diez errores de instrumento documentados** (ERR-09: la comprobación de inercia comparaba dicts que
  incluían la clave `lam`, era `False` por construcción; ERR-10: "sin conflicto" definido como solapamiento
  espacial final, ignora el conflicto temporal de E2 y el 3→0 de E2L). Diez de diez anomalías del proyecto
  han sido del instrumento. Cuando algo se vea raro: primero el instrumento, siempre.
- **El patrón que más caro sale, tres veces ya** (ERR-06, ERR-08, ERR-10): escribir un criterio que no dice lo
  que quiero decir, y descubrirlo sólo al correrlo. Antes de correr, releer el criterio preguntando qué
  escenario lo haría pasar por la razón equivocada.

## Comandos
```
# IMPORTANTE en Windows: la consola es cp1252 y revienta al imprimir ≈ → ∩ (UnicodeEncodeError).
PYTHONIOENCODING=utf-8 python bateria.py 6     # (desde organismo/) regresión rápida
PYTHONIOENCODING=utf-8 python bateria.py 20    # regresión completa de v6 (referencia)
python bateria_v9.py 6                         # (desde organismo/) regresión rápida del TRONCO v9, ~2 min
python bateria_v9.py 20 --log                  # examen completo de v9, log y json en datos/
python bateria_v8.py 6                         # referencia v8
python organismo/bateria_v7.py 20              # examen de congelación de v7 (ya trae reconfigure utf-8)

python experimentos/run_etapa.py --etapa E1 --semillas 20        # paralelo, ~13 s
python experimentos/run_etapa.py --etapa E1 --semillas 20 --verificar-equivalencia
python experimentos/analiza.py --etapa E1 --baseline

python -c "import organismo_v6 as o; print(o.run(1))"   # una corrida (~4 s)
```
