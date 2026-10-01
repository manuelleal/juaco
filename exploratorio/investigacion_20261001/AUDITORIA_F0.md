# Auditoría de F0 (1-oct-2026) — leer junto con F0_relojes.md

Autor: juaco-auditor (solo lectura, script propio desde los `pasaje_*.json`). `F0_relojes.md` NO se reescribió: las frases de abajo lo corrigen.

**VEREDICTO: SE SOSTIENE CON RESERVAS.** Los números de F0 se reproducen desde los JSON con un script propio. Las reservas son de interpretación (reloj ≠ rondas de selección, definición de Ne, n de o1_evo y entre_linajes), no de cuentas. Ningún hallazgo cambia un veredicto registrado; ninguno merece ERR.

## Hallazgos

**H-1 (n de o1_libre: se sostiene).** n = media de z² sobre los 8 genes ≥ 10σ en el neutro, pasaje 2, 10 cadenas.
- Serie: media 11.61, mediana 11.19, IC 10.0–13.4 (informe: 11.6, IC 9.9–13.4).
- Réplica: media 11.92, mediana 11.57, IC 10.8–13.1 (informe: 11.9, IC 10.7–13.1). La diferencia en el IC es la semilla del bootstrap.
- Con 10 genes de O1: 11.87 y 11.65. Contando solo genomas distintos: 12.0 y 11.9.
- σ_j, fábrica y recorte de `f0_relojes.py:39-43` coinciden campo a campo con `carros\O1_LIB.py:39-42` y `construye_o1_lib.py:53-59`.
- n ≈ 100 se descarta: el conjunto a ≥ 25σ (recorte inerte hasta n ≈ 100) da 11.1 y 12.1.
- Mutación de la siembra: `_ps_parto` guarda los genes del padre antes de mutar al hijo (`O1_LIB.py:264-268`) y `siembra()` toma esos genes (`corre_o1_libre.py:193`); cada refundación suma +1 en `_ps_init`. El estimador cuenta bien esos eventos.
- Selección purificadora oculta: no hay. El neutro corre con PS_LEE = 0 (`corre_o1_libre.py:72`); los genes no se leen. El recorte solo puede bajar n.
- Reserva: n es la profundidad media de los padres muestreados, no la máxima ni la de cada rama.

**H-2 ("cae por un factor ~12": reserva de redacción).**
- Compara dos cosas distintas: el 150 son nacimientos por línea (3 pasajes × ~50 por linaje, `PREREGISTRO_o1_libre.md:241`); el 11.6 son eventos de mutación en la ascendencia de un genoma.
- Los nacimientos sobreestiman la profundidad (salen de ~5.7 padres por linaje y pasaje, con hijos en cola FIFO).
- La profundidad subestima las rondas de selección: hay ~224 refundaciones por pasaje que copian de los últimos 50 partos (`O1_LIB.py:193-196`), lo que sesga hacia linajes que paren más sin sumar profundidad.
- El criterio "n ≥ 100" de la ficha era mutacional, así que el CAE es correcto en esos términos.
- **El reloj de selección entre linajes NO está medido.**

**H-3 (Ne y padres: verificados).** Ne_linajes 8.27 y 8.10; padres distintos 24 y 23.5; Ne_padres 17.88 y 17.65. Ne_linajes es 1/Σp² de aportes por linaje (máximo 9), no un Ne genético. Ne_padres junta padres de 50k pasos y supera el censo: cota alta.

**H-4 (s de MEM: números exactos, modelo con reserva).**
- s por paso: 0.0573 (serie) y 0.0288 (réplica). D = 0.0526 y 0.0277; V = 0.00238 y 0.00242.
- Sesgo por n (`f0_relojes.py:251-252`): usa el n del neutro, pero el brazo lib tiene n = 14.3–14.6 (23 % más). s queda sobreestimada hasta ~23 % (0.057 → 0.046; 0.029 → 0.023); el sesgo real es algo menor.
- V que arranca en 0 y recorte en 0: sesgos de signo no determinado sin simular.
- Arrastre: correlación entre cadenas de D_MEM y D_PISO 0.63 en la serie y −0.07 en la réplica: sugiere arrastre en la serie, no concluyente.
- La réplica no replica a MEM: gana 6/10 y el IC de D cruza 0.

**H-5 (Ne·s: "NO DECIDE" es lo que permiten los números, con matiz).**
- Con Ne de linajes y s por paso, Ne·s < 1 se cumple ×2 (0.47, IC 0.30–0.69; 0.23, IC −0.06–0.56).
- En la SERIE, dos de cuatro definiciones quedan por encima de 1 con IC que excluye 1: linajes por nivel 1.93 (IC 1.21–2.87) y padres por nivel 4.13 (IC 2.6–6.2). En la RÉPLICA todas cruzan 1.
- La definición "linajes por paso" es la más favorable a "casi neutro". "Casi neutro" no se sostiene solo con ella.

**H-6 (PISO: verificado).** D = 0.1251 y 0.1248, 10/10 en ambas; s por paso 0.0978 y 0.0865; Ne·s de linajes 0.80 y 0.70. El umbral Ne·s = 1 no separa lo detectable de lo no detectable en este montaje. Matiz: PISO lo lee la conducta de forma directa y fuerte; no se extrapola a MEM.

**H-7 (o1_evo y entre_linajes: demasiado frágil para reportar como número).**
- o1_evo: media 20.7, mediana 19.2, IC 16.2–26.1 con 2 genes; con 4 genes 20.5. Pero las cadenas van de 3 a 58, los incrementos por pasaje salen negativos y ~9 de 20 cadenas caen en 18–20 sin explicación.
- entre_linajes: media 28.5 con solo 5 cadenas (12, 12, 25, 35, 59); el IC bootstrap sobre 5 cadenas no es fiable.
- Una sola serie, sin réplica, y la siembra de o1_evo viene de vivos, no de partos: no comparable con o1_libre.
- Reportar como "orden de 20–30, muy por debajo de 100, una serie, genes limitados".

**H-8 (desviación menor).** La ficha pedía "10 genes sin recorte"; el script usa 8 (≥ 10σ). Declarado; con 10 da lo mismo.

## Frases de F0_relojes.md a cambiar
- `:7` "sin duda", "n ≈ 12 generaciones efectivas", "CAE" → "reloj mutacional ≈ 12 eventos a lo largo de la ascendencia; n ≥ 100 (mutacional) no se cumple".
- `:7` "los intervalos cruzan 1" → "en la serie dos de cuatro definiciones quedan por encima de 1 con IC que excluye 1; en la réplica todas cruzan".
- `:15` y tabla: o1_evo y entre_linajes como "orden 20–30, 1 serie", sin decimales.
- `:21-22`: avisar en la tabla de que Ne no es genético.
- `:36`: ver H-2.

## No verificado por el auditor
- La genealogía completa de los partos (no está guardada).
- Los IC de Ne·s (dependen del bootstrap conjunto del script).
- La dirección neta del sesgo de V y del recorte en s (requiere simulación).
- s directa mix − mixA.
- La causa del agrupamiento de cadenas de o1_evo en n ≈ 19.
- En el neutro de o1_evo, solo se comprobó PS_LEE = 0 en BRAZOS (`corre_o1_evo.py:63`).
