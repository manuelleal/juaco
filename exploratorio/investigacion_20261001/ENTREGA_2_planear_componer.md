# Entrega 2 — Planear y componer (1-oct-2026)

Autor: juaco-investigador (solo lectura; no corrió experimentos ni pruebas estadísticas), revisado por la sesión "Investigación y exploración".
Revisión: comprobé `carros/O1_LUGAR_PLAN.py:72,84,94`, `mundo_tramo_c.py:152-157`, `corre_c.py:101-103,109`, `BITACORA.md:22,38-39,44-45` y que en la carpeta sólo existen PREREGISTRO_p1, p7 y p10: coinciden. Un detalle a revisar: el informe da c1 "7/10 contra 4/11 y 6/11"; la nota de `BITACORA.md:45` (humo 2) dice comp 0.71 (7/10), lug 0.53 (6/11), antípoda 0.31 (9/29). El "4/11" no lo encontré en esa línea.

**VEREDICTO: HAY ALGO MODESTO.** P9 y P8 no refutan nada: P9 falló por tres causas a la vez (mundo, medida y mecanismo) y P8 por la medida. Hay un camino barato para ambos, pero ninguna ficha tiene más de 0.5 de probabilidad de dar una secuencia de dos pasos que además pague en cruce.

Abreviatura: `E\` = `C:\Users\User\Documents\PROYECTOS\JUACO\organelos\experimentos\organelos\escalera\`. No existen preregistros de P8 ni de P9 en esa carpeta; el runner de ambos es `E\corre_c.py`.

## a) Diagnóstico

### P9: fallan mundo, medida y mecanismo

**Mundo (verificado).**
- La base sólo vive del extra del oasis: en el mundo de P1, `o1` y `bar` tienen vida 200 contra 1504 de `lug` (`registro\REGISTRO_etapas_1_2.md:7376`).
- El cerrojo quita justo ese extra (`E\mundo_tramo_c.py:152-157`), así que los tres brazos caen a vida 200–300 con 33–53 fundadores por linaje (`E\BITACORA.md:22-23, 32, 38-39`).
- El 10 % de la reposición es K, y el mundo A+C queda en 4.0–4.4 contra ~7 (`BITACORA.md:34, 39`).
- Cada refundación nace limpia (`experimentos\carrera_escuderias\pista.py:347`), de modo que `hab` se borra decenas de veces por corrida.

**Mecanismo (verificado en código; la lectura causal es inferida).**
- K vale (0, 0), y `_gana` devuelve 0 si nada es positivo (`E\carros\O1_LUGAR_PLAN.py:72`). Tampoco es "costeable" (`:94`). K sólo se muerde como prueba única de letra desconocida (`:84`) hasta que `hab[K]` supere 0.05 (`:258-259`).
- El crédito va a la última letra mordida, sea cual sea (`:263-271`). Con una llave que dura 1500 pasos (`mundo_tramo_c.py:38`), la letra previa a un bocado con llave casi siempre es A o C, no K.
- Los números lo confirman: 1088–4509 créditos contra 336–446 mordidas de K, y `hab_K` de 0.11, −0.03 y −0.01 (`BITACORA.md:22, 32, 38`).
- El carro no guarda si lleva llave, así que no puede condicionar K a su estado.

**Medida (inferido).**
- `frac_llave` (`corre_c.py:109`) no separa una secuencia de un apetito general por K: la base sin módulo ya da 0.07–0.21 y el control 0.12–0.32.
- El control "penúltima" no es contenido equivocado. Con ventana de 1500 pasos, la penúltima letra acredita tan bien o tan mal como la última, y por eso gana o empata en los tres humos.
- La puerta exige cruce (`corre_c.py:177`) en un mundo donde nadie cruza.

### P8: falla la medida; el mecanismo es una suma cableada

**Medida (verificado).**
- J = c1 + p1 − 1 (`corre_c.py:101-103`). El término p1 pide rechazar E fuera del oasis, pero E (+0.3, −0.1) es mixta y O1 la muerde por limpieza (`O1_LUGAR_PLAN.py:89-100, 120`). p1 da 0.31–0.56 en los tres brazos (`BITACORA.md:25, 44`).
- La puerta "B dentro rechazada ≥ 0.9" tampoco la pasa nadie (0.62–0.73), por la misma limpieza.
- Los eventos fríos son a lo sumo uno mordido por casilla de linaje y corrida (`mundo_tramo_c.py:173-178`; `mx_dentro` nunca se reinicia, `:185-186`). Salen 10–11 en dos corridas.
- c1 de 7/10 contra 4/11 y 6/11 no se distingue (inferido; no se corrió la prueba estadística). [Ver nota de revisión arriba.]
- Inferido: el contador "ya mordió E" es de la casilla y no del cuerpo, así que un fundador limpio que prueba E dentro puede contar como frío.

**Mecanismo (verificado).** COMPONE es una edición de `_lg_v` que suma el bono también a letras mixtas (`E\construye_c.py:122-124`). La pregunta útil no es si suma, sino si lo aprendido por separado alcanza para decidir bien la primera vez.

### Patrón entre niveles (inferido)
- P9 chocó con el piso (la base muere) y "los tres juntos" con el techo (preg cruza 9/9, `BITACORA.md:53`).
- En ninguno de los dos se midió piso y techo del mundo antes de construir el módulo.

## b) Fichas, por valor/costo

Los costos salen de P1: una corrida a T 100k tarda unos 2.8 min de CPU (`ESCALERA.md:224`).

### 1. Piso y techo del mundo con llave no letal (requisito de P9)
- **Hipótesis:** existe un cerrojo donde la base vive y la llave todavía paga.
- **Mecanismo:** ninguno; es validez del mundo.
- **Mundo:** sin llave es P1b tal cual (extra 0.8); con llave el bocado dentro paga un plus. K a p_x 0.03.
- **Brazos:** `lug` (piso) y `lug` con llave regalada por el mundo (oráculo).
- **Medida:** establecidos y cruce.
- **Predicción:** piso con ≥ 12/18 establecidos y ≥ 6/18 cruces a T 100k (P1b dio 16 y 8, `BITACORA.md:8`); oráculo − piso ≥ +4.
- **Control que puede ganar:** el piso iguala al oráculo porque los niveles saturan; entonces el mundo no paga y no se construye nada.
- **Reutiliza:** una subclase como `E\mundo_k.py:17-30`, sin tocar el sha de `mundo_tramo_c`; la rama a invertir es `mundo_tramo_c.py:152-157`.
- **Costo:** 4–6 corridas, 1 proceso, unos 20 min.
- **Probabilidad:** piso vivo 0.85; oráculo +4, 0.5.
- **Nivel:** razonar/planear; no mueve puntos, habilita la ficha 3.

### 2. Sonda de P8 fuera de la presión de supervivencia, con celda retenida
- **Hipótesis:** letra y lugar aprendidos por separado deciden bien el primer E dentro del oasis.
- **Mecanismo:** COMPONE, sin memoria nueva.
- **Mundo:** E nunca nace dentro del oasis durante la crianza. Es un ancla nueva en `mundo_tramo_c.py:123-125`.
- **Medida:** se reconstruye el carro con `nace(memoria)` (`O1_LUGAR_PLAN.py:176-183`) y se le pregunta a `actua` (`:103-145`) con observaciones sintéticas, sin llamar a `resultado`. Dos E a igual distancia, una en el bin de mayor bono y otra en el antípoda, sobre una rejilla 5×5 de niveles. D = P(blanco dentro) − P(blanco fuera).
- **Predicción:** D ≥ 0.6 en ≥ 70 % de los linajes establecidos de `comp`; `lug` da D = 0 exacto (nunca apunta a una mixta, `:72`).
- **Control que puede ganar:** `compbar` (antípoda) debe dar D ≤ −0.3; si empata con `comp`, el bono es difuso.
- **Segunda puerta:** con A y E dentro a igual distancia, elige A.
- **Aviso verificado:** los JSON actuales guardan `lugar` pero no la tabla por letra (`corre_c.py:86-88`). Hay que criar de nuevo guardándola.
- **Costo:** 6–12 corridas a T 60k, 1 proceso, unos 30 min; la sonda tarda segundos.
- **Probabilidad:** 0.75.
- **Nivel:** razonar/componer; cierra P8 en un sentido o en otro. Vale poco como peldaño nuevo, mucho como instrumento.

### 3. P9 con traza por tiempo y competencia, medida por contraste
- **Hipótesis:** con el crédito repartido por elegibilidad temporal, K adquiere valor sólo cuando habilita.
- **Mecanismo:** regla delta local. Error = dS − [valor(letra) + bono(lugar) + Σ e[k]·hab[k]], con e[k] = exp(−Δt/τ) desde la última mordida de k. Lugar y K compiten por el mismo error. K vale `hab[K]` sólo si hay un sitio recordado y la llave no está en mano.
- **Memoria nueva:** 5 floats `e` por cuerpo y 5 `hab` por linaje.
- **Mundo:** el de la ficha 1, con ventana de llave corta (unas 2 veces el tiempo de viaje medido allí), para que el orden importe.
- **Medida:**
  - (a) Contraste: pares K → bocado dentro en la ventana, observados sobre esperados al barajar los tiempos de K dentro de cada vida. Hay que registrar los eventos en el mundo.
  - (b) `frac_llave`.
  - (c) Devaluación: a T/2 la llave deja de pagar.
- **Predicción:** (a) ≥ 2.0; (b) ≥ 0.6 contra ≤ 0.25 del piso; (c) las mordidas de K caen ≥ 50 % en dos vidas; cruce `plan` > `lug` en ≥ 13/20.
- **Control que puede ganar:** un brazo "hábito" (K valorada sin mirar el estado) puede empatar en (b) y en cruce, y debe perder en (a) y (c). El segundo control acredita a una letra al azar con la misma masa.
- **Reutiliza:** `construye_c.py:46-74` y `:125-147`; `corre_c.py:106-112`.
- **Costo:** exploración de 6 corridas, 20 min; serie 20 × 4, unas 4 h de CPU (pool 6: unos 45 min), más la réplica.
- **Probabilidad:** (a) y (b) 0.45; cruce 0.3.
- **Nivel:** planear.

### 4. Uno va a lo menos visitado, ocho leen
- **Hipótesis:** la señal no sumó porque todos exploraban; paga cuando explorar es de pocos.
- **Mecanismo:** ninguno nuevo; pista mixta con 1 carro con pregunta y señal, y 8 con sólo señal.
- **Medida:** latencia de los lectores tras cada mudanza.
- **Predicción:** ≤ 700 pasos, contra 1250–1400 cuando todos son sólo señal (`BITACORA.md:50-51`).
- **Control que puede ganar:** señal leída al antípoda, ≥ 1200.
- **Reutiliza:** `E\juntos\corre_juntos.py` y sus carros. Necesita un runner con carros mixtos: `P.run` acepta lista (`corre_c.py:277`), pero `CV.tarea` recibe un solo nombre (`:81`).
- **Costo:** 6 corridas, 20 min.
- **Probabilidad:** 0.5.
- **Nivel:** comunicación; es composición entre cuerpos, no dentro de uno.

## c) Literatura

**Verificadas por el investigador (búsqueda de hoy):**
- Taylor, Hunt, Holzhaider y Gray 2007, Current Biology 17: metaherramienta espontánea en cuervos. https://www.sciencedaily.com/releases/2007/08/070816121111.htm
- Wimpenny, Weir, Clayton, Rutz y Kacelnik 2009, PLoS ONE, doi 10.1371/journal.pone.0006471: la secuencia de herramientas no exige planeación ni analogía, y el pre-entrenamiento de cada eslabón la mejora. Respaldo de medir por contraste y devaluación. https://research-repository.st-andrews.ac.uk/handle/10023/4174
- Richter, Hochner y Kuba 2016, PLoS ONE, doi 10.1371/journal.pone.0152048: pulpos, tarea de cinco niveles. https://pmc.ncbi.nlm.nih.gov/articles/PMC4803207
- Pfeiffer y Foster 2013, Nature 497:74-79: secuencias hipocampales hacia metas recordadas. https://pmc.ncbi.nlm.nih.gov/articles/PMC3990408
- Tolman, Ritchie y Kalish 1946: atajo en el laberinto de rayos. Un metaanálisis reciente reporta mala replicabilidad. https://www.ncbi.nlm.nih.gov/pmc/articles/PMC12766676/
- Adams y Dickinson 1981, QJEP 33B:109-112, doi 10.1080/14640748108400816: devaluación del reforzador (meta contra hábito).
- Lake y Baroni 2018, ICML, arXiv:1711.00350: celda retenida. https://www.cs.princeton.edu/~bl8144/papers/LakeBaroni2018ICML.pdf
- Najarro y Risi 2020, NeurIPS: reglas hebbianas halladas por búsqueda. https://arxiv.org/abs/2007.02686
- Wang et al. 2018, Nature Neuroscience 21:860-868, doi 10.1038/s41593-018-0147-8: meta-RL en corteza prefrontal. https://www.biorxiv.org/content/10.1101/295964v1
- Willatts 1999, Developmental Psychology: sólo citas secundarias; la cita exacta queda PENDIENTE.

**PENDIENTE (no buscado):** Tolman y Honzik 1930; Fiorito (pulpos); Piaget (medios-fines); "fábula de Esopo" en córvidos; revisiones de tareas de rodeo; Rescorla y Wagner 1972; Sutton 1990 (Dyna).

## Lo que NO vale la pena
- Otro humo de P9 con un cerrojo que quite el extra, o con crédito a la última letra.
- J = c1 + p1 − 1 y la puerta "B rechazada".
- `frac_llave` sola con ventana de 1500 pasos.
- El cruce como puerta en mundos con piso o techo.
- Selección sobre las perillas de PLAN antes de que funcione por diseño.
- Repetición fuera de línea tipo Dyna antes de que la ficha 3 muestre que el crédito llega pero lento.
- Atajos tipo Tolman en un anillo de una dimensión.
- Meta-RL recurrente de Wang 2018 como mecanismo: se entrena con retropropagación.

## No verificado
- No se corrió ningún experimento ni prueba estadística.
- No se leyeron `HORIZONTE_frontera.md`, `BRIEF_ORIGINAL_y_estado.md`, `INDICE.md`, `LABORATORIO.md` ni `PREREGISTRO_juntos.md`; por eso no se asignan puntos del brief.
- No se comprobó si los niveles E y Ag saturan (de eso depende el oráculo de la ficha 1), ni el tamaño del anillo ni el tiempo de viaje.
- No se miró `corre_v143.tarea` por dentro.
- Los costos están extrapolados de P1.
