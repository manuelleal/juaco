# EXPLORATORIO, no es dato — enjambre de 30 agentes (25-sep-2026)

## Donde esta la brecha (sintesis de 20 Haiku, uno por semilla)

# Síntesis: brecha O1 vs V143 (20 semillas, carrera JUACO)

## Patrón que se repite (hecho, 20/20 semillas)
**O1 saca más R0_pista que V143 en las 20 semillas, sin una sola excepción.** Rango O1: 0.65–1.28. Rango V143: 0.24–0.62. RES0 (sin nodo de entrada neutral) queda pegado a V143 en 14/20 semillas y solo mejora de forma notable en 2 (36010: 0.50 vs 0.62 V143 — aquí RES0 es peor; 36015: 0.28 vs 0.25, y 5/9 linajes establecidos vs 2/9 de V143).

**Tres sub-patrones consistentes con números, presentes en prácticamente las 20 semillas:**

1. **Vida media 2.4×–6× más larga en O1.** Ejemplos: 36004 (4925 vs 974, 5.1×), 36014 (4302 vs 714, 6×), 36020 (3142 vs 533, 5.9×), 36009 caso más chico (1948 vs 1284, 1.5×). En ninguna semilla V143 vive más que O1.

2. **V143 gasta 3×–45× más fundadores (reposiciones) que O1.** 36001: 3.3×. 36009: 44.9× (43 vs 1930). 36013: post-10k 8.3×. La magnitud varía mucho pero la dirección es 20/20.

3. **Muertes por veneno+sal dominan en V143, no en O1.** Donde se reportó porcentaje explícito (6 semillas: 36002, 36008, 36009, 36014, 36016, 36018) veneno+sal es 89–95% de las muertes de V143, contra 35–77% en O1. En las otras 14 semillas se reporta la misma dirección sin porcentaje exacto (ratios de 2.9× a 9.5× más muertes por veneno/sal en V143).

4. **Linajes que cruzan R0_real≥0.90:** en las 17 semillas donde se dio el conteo, O1 establece 6–8/9 (67–89%) y V143 0–4/9 (0–44%) — típicamente 2–4× más linajes de O1. **Excepción/anomalía:** semilla 36008 reporta V143 7/9 "establecidos", que contradice su propio R0_pista=0.25; probablemente el agente confundió "persiste" con "cruza_real≥0.90" — dato sospechoso, no verificado.

## Lo que varía entre semillas
- El tamaño de la brecha de fundadores oscila entre 3× y 45×, sin patrón claro por semilla.
- RES0 no se comporta igual siempre: en 14/20 se parece a V143, en 2 es claramente peor que V143 (36010, y levemente 36003/36004), y en 2 mejora bastante (36010 no, corrijo: 36015 sí mejora; 36012 empata con V143). Es decir, quitar el nodo de entrada neutral **no cierra la brecha de forma confiable**.
- Algunos linajes individuales de V143 colapsan por completo (fundadores post-10k > 900, R0_real < 0.02) mientras otros del mismo bicho cruzan casi igual que O1 (ej. 36007 linaje 1: O1 0.93 vs V143 0.97). La varianza intra-linaje de V143 es enorme; la de O1 es baja.

## Hipótesis (no hechos — interpretación de los 20 agentes Haiku)
Todas las semillas convergen en la misma hipótesis narrativa: **O1 "discrimina" cuándo morder veneno/sal y "limpia" fundadores defectuosos temprano, mientras V143 muerde indiscriminadamente y entra en una espiral de reposición de fundadores intoxicados.** Frases repetidas: "el veneno tapa el mundo", "sabe que es malo y lo muerde igual", "boca lee las dos filas" (36010).

## Lo que estos análisis NO pueden decir
- **No hay ablación causal.** Todo es correlación entre variables de salida (mordidas, causas de muerte, fundadores) y R0_pista. Ningún agente aisló una regla concreta de la política de O1 para probar que ESA regla es la causa.
- **No distinguen "O1 aprende" de "O1 ya viene con la regla escrita".** O1 es una política fija (techo, escrita por LLM antes de correr), no algo que se adapta durante la vida del organismo. Varias hipótesis usan lenguaje de "aprender"/"decidir en tiempo real" que no está sustentado por los datos — es una posible confusión de los 20 agentes.
- **RES0 no aísla el mecanismo.** La variabilidad de RES0 (a veces igual a V143, a veces peor, rara vez mejor) sugiere que el cuello de botella no es solo el nodo de entrada neutral, pero ningún reporte identifica qué otro componente de V143 falta (memoria, capacidad de red, función de recompensa) — solo se dice explícitamente en 36015.
- **No hay control estadístico.** 20 corridas puntuales sin intervalos de confianza ni prueba de significancia sobre las razones de brecha (3× vs 45× en fundadores es la misma "dirección" pero no sabemos si es ruido de semilla o señal real).
- **No comparan arquitectura interna.** Los agentes leyeron telemetría de comportamiento (mordidas, causas, fundadores), no el contenido de la política/pesos de V143 ni la regla exacta que usa O1 para evitar veneno — así que "por qué" sigue siendo hipótesis, no hecho verificado.

## Rutas (síntesis con 8 Sonnet de literatura)

Regla del juego para las 6: mecanismo local, sin retropropagación, que el bicho real (v14.3) pueda usar o aprender, sin copiar la política de O1 (techo LLM, no replicable). Meta: R0_real ≥ 0.90 en la pista.

| # | Ruta | Mecanismo mínimo |
|---|------|---|
| **1** | **Compuerta de mordida por saciedad/reserva** | prob(morder tóxico) se multiplica por una función decreciente de la reserva/saciedad propia del cuerpo, recalculada cada paso |
| 2 | Integrador de carga tóxica con fuga | variable local "carga_toxina" sube al morder malo y decae con el tiempo; bloquea mordidas mientras carga > umbral |
| 3 | Neutralización pasiva del veneno al morder (regla de mundo) | cada mordida sobrevivida reduce la toxina de esa celda una fracción k; no es decisión del bicho, es física de la pista |
| 4 | Aversión de un ensayo por identidad de ítem (CTA) | al sufrir daño tras morder un ítem con tag X, prob(morder tag X) cae de un solo golpe y decae con el tiempo |
| 5 | Enterrar / vertedero (construcción de nicho activa) | acción heredable que saca el veneno del mapa transitable de forma permanente, heredada por el linaje |
| 6 | Umbral de respuesta reforzado (división de trabajo) | umbral θ_i de "limpiar veneno" por cuerpo, heredado y autorreforzado por la experiencia propia (unos limpian, otros crecen) |

### 1. Compuerta por saciedad/reserva — MARCADA #1

- **Evidencia (semillas):** en 36010, diag.boca ya mide la firma exacta: mordida-D-tóxico-saciado (DS) O1=0.0000 vs V143=0.0086; mordida-B-saciado (BS) O1=0.1029 vs V143=0.0116; error de memoria def_bd_con_robo O1=0.2398 vs V143=0.5900; tasa de reproducción bruta O1=0.712 vs V143=0.266 hijos/muerte. A escala agregada: veneno+sal es 89–95% de las muertes de V143 (6 semillas con % explícito) contra 35–77% en O1.
- **Literatura:** Stephens (1981) forrajeo sensible al riesgo dependiente de reserva; Sherratt et al. (2007) y Nersesian et al. (2011) umbral de carga tóxica pagable; Symmonds et al. (2010) el estado metabólico altera la decisión de riesgo.
- **Predicción numérica:** R0_real sube de ~0.60 (V143) a 0.72–0.85; el marcador DS debe bajar de 0.0086 hacia ~0. Falla si R0_real queda en 0.60±0.03 pese al gate, o si DS no baja de 0.008.
- **Control:** (a) reserva barajada/desacoplada del gate → debe reproducir V143 (~0.60); (b) gate invertido (muerde más tóxico saciado) como control negativo → debe empeorar.
- **Costo:** bajo. Usa una variable de estado que el organismo ya lleva (reserva/hambre); sin memoria de identidad, sin acción nueva, cómputo O(1) por mordida. Además se puede chequear el marcador DS en los logs ya existentes de V143 antes de correr una serie nueva.
- **Por qué es la primera:** es la única ruta con una firma ya medida en los datos (DS=0.0086 en V143 vs 0.0000 en O1) que coincide con tres fichas de literatura independientes, apunta directo a la frase repetida "sabe que es malo y lo muerde igual" (V143 sí distingue, no gatea por su propio estado), y es la más barata de las 6: no agrega memoria de identidad (ruta 4), no crea una acción nueva (ruta 5) ni exige heredar un umbral distinto por cuerpo (ruta 6). Se puede auditar sin gastar Pool: recalcular DS/BS sobre el crudo ya guardado.

### 2. Integrador de carga tóxica con fuga

- **Evidencia:** seed 36002 muestra correlación casi 1:1 entre fundadores repuestos y muertes por veneno/sal (O1#8: 184→186; V143#4: 1151→1151); causas veneno+sal O1=77.1% vs V143=91.6% vs RES0=93.1%.
- **Literatura:** Barnett, Bateson & Rowe (2012); Marsh et al. (2006), hipótesis de límite de detoxificación.
- **Predicción:** R0 0.60→0.65–0.78; mortalidad por sobredosis de toxina cae 40–60%. Falla si la mortalidad no baja de ±10% (apuntaría a densidad de veneno en el mundo, no a evaluación individual).
- **Control:** fuga=0 (memoria infinita) vs fuga instantánea (sin integrador), comparar los tres regímenes.
- **Costo:** bajo-medio; una variable de decaimiento exponencial que calibrar (~200–400 pasos) contra la pista real.

### 3. Neutralización pasiva ligada a la mordida (regla del mundo)

- **Evidencia:** "el veneno tapa el mundo" se repite en 20/20 síntesis; RES0 (sin nodo de entrada neutral) NO cierra la brecha en 14/20 semillas — señal de que parte del cuello de botella es del entorno, no solo de la decisión del bicho (ej. 36015: RES0 mejora 150% pero sigue gastando fundadores).
- **Literatura:** Jones, Lawton & Shachak (1994) ingenieros de ecosistema; Odling-Smee, Laland & Feldman (2003) construcción de nicho.
- **Predicción:** con k≈30% de reducción de toxina por mordida sobrevivida, R0 0.60→0.70–0.78 sin tocar el cerebro del bicho. Falla si R0 queda en 0.58–0.62 (la regeneración de veneno supera a k).
- **Control:** k=0 (línea base = V143 actual); neutralización al azar en celdas (mismo total removido, desligado de si hubo mordida).
- **Costo:** muy bajo. Es una regla del motor de la pista, no del organismo — no arriesga romper el instrumento del bicho; la más segura de probar primero.

### 4. Aversión de un ensayo por identidad (CTA / bait-shyness)

- **Evidencia:** la frase "sabe que es malo y lo muerde igual" aparece en las 20 síntesis; frac_muere_sin_parir V143 0.60–0.74 vs O1 0.31–0.54 en varias semillas (36018: O1=35.6% vs V143=67.4%) — el bicho repite el mismo error de nuevo sin bloquearlo por identidad.
- **Literatura:** Garcia & Koelling (1966), aversión gustativa condicionada.
- **Predicción:** R0 0.56→0.62–0.72; % linajes establecidos 66%→72–78%. Falla si R0 no se mueve de 0.60±0.02.
- **Control:** castigo asociado a un tag barajado (no al ítem real mordido) — si mejora igual, es solo supresión general de mordidas, no aprendizaje por identidad.
- **Costo:** medio. Requiere memoria corta de identidad por ítem/tipo, más caro que las rutas 1–3 pero sigue siendo local y de un solo ensayo.

### 5. Enterrar / vertedero (construcción de nicho activa)

- **Evidencia:** hipótesis repetida de que O1 "sacrifica cuerpos para liberar espacio" (36008: "sacrificio voluntario masivo... para liberar espacio de memoria"; 36001 linaje 0: O1 elimina deliberadamente con 462 muertes veneno+sal voluntarias vs 124 en V143). Fundadores post-10k de O1 rondan cero en linajes exitosos (36013 linaje 0: O1=0 vs V143=43 vs RES0=1023).
- **Literatura:** Chiba, Suzuki & Arita (2020), construcción de nicho en robótica evolutiva.
- **Predicción:** el techo más alto de las 6 (R0≥0.80) si el costo c de enterrar es bajo. Falla de forma binaria: si c es alto, la conducta nunca se fija por selección y R0 se queda en 0.60 pese a tener el gen disponible.
- **Control:** enterrar gratis (c=0) vs con costo; réplica con el gen presente pero mutado a inactivo (descarta pleiotropía).
- **Costo:** alto. Acción nueva completa (mover objeto entre celdas, marcar celda no transitable) más tiempo de selección para fijar el gen — la más cara y de mayor riesgo de fallo total.

### 6. Umbral de respuesta reforzado (división de trabajo)

- **Evidencia:** varianza intra-linaje enorme en V143 (36007 linaje 1: O1=0.93 vs V143=0.97, casi igual; otros linajes del mismo bicho colapsan a R0_real<0.02) y mordida rígida/pareja en linajes colapsados (36014: ratio B+D/A+C≈0.066 en V143 vs ≈0.48 flexible en O1) — consistente con falta de especialización entre cuerpos del mismo carro.
- **Literatura:** Bonabeau, Theraulaz & Deneubourg (1996), umbral fijo de división de trabajo en insectos sociales.
- **Predicción:** R0≥0.75 con θ heterogéneo autorreforzado; caída ≥30% en mordidas que el cuerpo no puede pagar. Falla si la varianza de θ colapsa rápido a un solo valor.
- **Control:** réplica con umbral fijo igual para todos (sin refuerzo ni heterogeneidad) para aislar el efecto.
- **Costo:** medio. Variable de umbral heredable por cuerpo con mutación y regla simple de refuerzo; no requiere coordinación global pero sí variar genéticamente entre cuerpos del mismo carro.
