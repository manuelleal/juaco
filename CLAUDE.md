# Proyecto: Organismo artificial mínimo (Artificial Life)

Investigación reproducible sobre si un organismo artificial simple, con reglas locales y sin backpropagation,
puede aprender, desaprender, generalizar y (más adelante) transmitir conocimiento. Dirección: Christiam Puentes.
Colaborador técnico: Claude. Todo corre en CPU con Python 3 + NumPy.

## Fuente de verdad
- `registro/REGISTRO_etapas_1_2.md` — historial completo, criterios preregistrados, resultados, errores. LEER PRIMERO.
- `registro/HANDOFF.md` — narrativa completa de lo hecho y por qué.
- `registro/PLAN.md` — qué sigue y cómo.
- **`organismo/organismo_v11.py` — EL TRONCO desde el 17 sep 2026** (f69e24063be1b194, tag `v11-tronco`).
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
1. Antes de tocar nada: `cd organismo && python3 bateria.py 6` **y** `python bateria_v11.py 6` (tronco; `bateria_v9.py 6` como regresión).
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
11. **Repo y sandbox nunca corren a la vez; el repo tiene prioridad.** El sandbox arranca sólo con el repo
    parado y con `Pool(6)`, no 16. El tiempo de pared es un dato y se contamina al solapar.

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
