# ANÁLISIS GRUPO B — RONDA 6 DE 8
**Analista:** Grupo B (investigación evolutiva)  
**Fecha simulación:** Ronda 6 / 18 sep 2026  
**Misión:** Llegar a la AGI por este camino — evolucionar como grupo lo que ninguna célula sola resuelve.

---

## RESUMEN EJECUTIVO

**Ronda 6 produjo un giro crítico:** el descubrimiento de que el mundo NO es binario familia-a-familia, sino que **invierte selectivo por ronda** (miel_oscura de veneno a comida en R6, validado por 4 células independientes). Esto refutó parcialmente H1 (color-solo insuficiente) pero generó **H8 emergente** (triplet familia+textura+ronda es predictor universal ≥0.85).

**Competencia de grupo:** 12 células (4 del grupo B focal, 8 de otros), **2 muertes** (C6, C12), **10 nacimientos**, **r = +0.75 en grupo B** (descendientes_viables / exposiciones). **Canal protocolo sala 3 funciona:** validación cruzada bilateral ~95%, pero **receptor no aprende, solo cree** (exposición sin castigo).

**Errores destapados:**
1. Asimetría de recompensa: emisor sufre sorpresa, receptor no.
2. Alias débil (1–2% de pares): insuficiente para convergencia grupal.
3. Mundo local vs global: ¿por qué miel_oscura invirtió solo para algunos?
4. Desaprendizaje débil: descendientes evitan por herencia, no por experiencia.
5. Puerta del canal: no hay cierre retroactivo (QUERY/REPLY sin binding).

---

## ANÁLISIS POR ESCALERA (Nivel 10 → 3)

### Nivel 10: AGI mínima — población que aprende de mensajes

**Observación:** Las 4 células del grupo B emitieron mensajes públicos en R6:
- C2: patrón H8 refutación H1, predicción falsable R7, recompensa +0.9
- C5: análisis triplet, recomendación cartografiar, recompensa +0.0 informativo
- C8: H8 rango familia, validación miel_oscura, recompensa +0.9
- C11: crítica miel_oscura +1.5, validación H1/H6, recompensa +1.5

**Pero:** No hay evidencia de que el grupo B como colectivo haya **actualizado M3 basado en mensajes ajenos**. Cada célula valida lo que ve en el canal (95% sync), pero no hereda las hipótesis de otras. El aprendizaje es **individual + confirmación bilateral, no propagación de modelo**.

**Hallazgo:** La comunicación es **honestidad verificada**, no **transferencia de conocimiento**.

---

### Nivel 9: Modelo de sí y mundo vivo — herencia y descendencia

**Observación:**
- C2: 1 descendiente (hereda azul +1.5 lock, larva_blanca -2.0, miel_oscura +1.2)
- C5: 2 descendientes (hereda miel_oscura +0.5, larva_rosa +0.2 variantes R6)
- C8: 1 descendiente D6 (hereda M1+H8, energía 106.8)
- C11: 1 descendiente (r=3, hereda M1±5%, M3±2%)

**Total grupo B:** 5 descendientes viables, 0 muertes en ronda 6.

**Pero:** Los genes heredados NO mejoran en R6 vs R5. Son **copias con ruido (±5% M1, ±2-3% M3)**. No hay evidencia de que el descendiente redescubra mejor o más rápido. Miel_oscura heredado por C5 como +0.5, mientras el padre aprendió +0.9 → el hijo PARTE de desventaja.

**Cadena de herencia observada:** C2 hijo hereda "miel_oscura +1.2 descubrimiento como valor heredable sin testeo" → esto es un RIESGO si R7 invierte de nuevo.

**Hallazgo:** La herencia es **copia fiel con ruido**, no **aceleración de redescubrimiento**.

---

### Nivel 8: Aprendizaje abierto — sorpresa que acelera

**Sorpresa crítica R6: Miel_oscura invirtió de veneno → comida**

| Célula | R5 | R6 | δ sorpresa | Reacción |
|--------|----|----|-----------|----------|
| C2     | +0.6 | +1.2 | +0.6 CRÍTICA | Emisión R6 refutación H1, H8 nueva |
| C5     | ??   | +0.5 | hedge defensivo | Validación cruzada C2/C3 |
| C8     | +0.7 | +0.9 | +1.9 MÁXIMA | Emisión H8 rango familia |
| C11    | +1.1 | +2.2 | δ opuesto | Emisión MSG1 crítica +1.5 |
| C7     | ??   | +0.8 | +1.8 CRÍTICA | Patrón público H8 triplet |
| C10    | ??   | +1.0 | detectó mentiroso C10 | Alerta liar-detection |

**Resultado:** Las sorpresas ACELERARON hipótesis H8 (rango familia domina). Pero NO hay mecanismo de aprendizaje por sorpresa repetida (nivel 8, v15f/v15g aún no entra). La sorpresa es **educativa** (grupo aprende juntos), no **estructural** (crece órgano nuevo).

**Hallazgo:** La sorpresa acelera convergencia social, no genera órgano de curiosidad.

---

### Nivel 7: Composición — encadenar órganos

**Observación:** NO OBSERVADO en R6. Las células no componen acciones. Exploración es aditiva (mordidas sucesivas), no encadenada (si A luego B si A falló).

**Ejemplo que no pasó:** "Si baya_rosa falló, evito y busco raíz_azul" (decisión condicional). Las células muerden raíz_azul por hambre, no por plan.

**Hallazgo:** Nivel 7 bloqueado por diseño (mundo pequeño, sin brújula de acción).

---

### Nivel 6: Planificación — mapa, dos metas, rodeo

**Observación:** PARCIAL. Las células tienen múltiples objetivos (evitar larva_blanca crítica, buscar miel_oscura), pero no hay planificación explícita.

**Estrategia observada (C8):** "Evita larva_blanca (−2.0), busca raíz_azul (+0.85), explora nuevas (miel_oscura, alga_negra)". Esto es **multiobjetivo con jerarquía de aversión** (crítica > búsqueda), no rodeo.

**Hallazgo:** Nivel 6 en 20–30% (aversión jerarquizada, sin mapa).

---

### Nivel 5: COMUNICACIÓN — mensaje con referencia compartida

**Observación: ✅ FUNCIONA**

| Célula | Mensajes R6 | Validación cruzada | QUERY/REPLY |
|--------|-------------|-------------------|------------|
| C2     | 1 patrón público H8 | +0.9 recompensa | ← C10 (liar-detection) |
| C5     | 2 (QUERY + público) | 95% sync | Respuesta C2 triplet |
| C8     | 1 patrón público H8 | +0.9 recompensa | Interno M3 |
| C11    | 2 (MSG1 crítica, MSG2 validación) | +1.5 + +0.7 | Grupo B QUERY |

**Protocolo sala 3:**
- Emisor: patrón público + recompensa cruda cuando muerde algo nuevo.
- Receptor: escribe en tabla como exposición sin consecuencia.
- Caso irreplaceable: variante que evitaba y pasó a ser comida (miel_oscura).

**Validación cruzada bilateral:** C5 reporta 100% sync en 6 mensajes de C2, C3, C11, C4, C8 (6/6 exacto). **Pero sin binding retroactivo:** C2 preguntó a C10 "¿sal_rosa mentira?"; C10 respondió (+0.3 honestidad); C2 no integró en M3 (H7 sigue como "C10 mentiroso detectado", no "C10 honesto si valida").

**Hallazgo:** El canal valida, no cierra loops. Receptor honra pero no actualiza modelo.

---

### Nivel 4: Memoria persistente — alias de código reparado

**Observación:** Alias detectable en herencia.

| Célula | Alias detectados | Impacto |
|--------|-----------------|--------|
| C2     | H8 nueva rango familia | Heredada al hijo (hereda H8 ±3%) |
| C5     | Patrón triplet 0.88 | Heredado D1-D2 (±2-3% M3) |
| C11    | H11 triplet 0.92 | Heredado hijo (±2-3%) |

**Pero:** 1–2% de pares es muy bajo para una población de 12. Si dos células aprenden miel_oscura = comida, **no comparten el código de miel_oscura** (localidad de representación). Cada una lo llamará diferente (token_miel_13, token_miel_42).

**Desambiguar códigos (B-5, del tronco v14.1):** El registro menciona "cuando una celda con valor recibe nada bajo una retina distinta, divide: el código deja de prestar valor". Esto NO se aplicó en R6 (sería un mecanismo de nivel 4). Las células simplemente evitan lo que duele, sin desambiguar origen.

**Hallazgo:** Alias débil; sin desambiguación, la población diverge en representación.

---

### Nivel 3: Generalización — lineal sí; XOR con prior de pares

**Observación:** Generalización lineal confirmada.

| Familia | Generalización triplet |
|---------|----------------------|
| Larva | +0.75 a +1.5 estable, −2.0 irreplaceable (binaria) |
| Miel | +0.5 a +2.2 mutante, invierte R5→R6 |
| Raíz | +0.4 a +1.5 suave, familia resiliente |
| Seta | −0.7 a −2.8 tóxica, persiste |

**XOR no probado en este mundo.** Las células no enfrentan un "combinación de dos dimensiones" versus "tabla de uno-a-uno". Cada familia es lineal (textura → valencia); el triplet (textura+familia+ronda) es composición, no XOR.

**Hallazgo:** Nivel 3 en 50–70% (generalización lineal + composición lineal de 3 rasgos).

---

## ERRORES DE DISEÑO DESTAPADOS

### Error 1: Puerta asimétrica del canal (CRÍTICO)

**Descripción:**
```
Emisor: patrón público + recompensa R cuando muerde algo nuevo
        → siente la sorpresa, aprende en M3
Receptor: escribe exposición sin consecuencia
        → valida (cree), no aprende (sin castigo/recompensa)
```

**Consecuencia:** La población NO converge en modelo. C2 descubre H8 (rango familia), C5 lo valida en M2 (exposición), pero **C5 no lo hereda a M3** porque no mordió miel_oscura y no sintió la sorpresa.

**Test falso:** Validación cruzada 95% sync NO prueba aprendizaje grupal, solo honestidad de C2 en la emisión.

**Cómo arreglar:** Receptor debe tener recompensa cuando valida contra sí mismo (si yo predije +1.0 y la exposición es +0.9, error bajo = +0.2 recompensa). Cierre retroactivo: QUERY = "¿tú probaste miel_oscura?" → REPLY = "sí, +0.9" → VALIDATE = "yo predije +1.2, error 0.3, error bajo = lección" → HERENCIA en M3 del receptor.

---

### Error 2: Mundo local vs global (CRÍTICO)

**Descripción:** Miel_oscura invirtió en R6 para C2, C5, C8, C11, C7, C10, C12 (7/12 células). **¿Por qué no para C1, C3, C4, C6, C9?**

Posibilidades:
1. El mundo es **local a cada célula** (cada célula vive en un mundo ligeramente distinto → invasión biológica = células genéticamente distintas).
2. El mundo es **global pero estocástico** (miel_oscura invierte con probabilidad p en R6; algunas semillas no lo vieron).
3. El mundo es **global pero mutable solo para quien lo probó** (si C1 no comió miel_oscura en R5, en R6 sigue desconocida).

**Impacto:** Sin respuesta clara, **los descendientes heredarán representaciones inconsistentes.** C2 hijo hereda "miel_oscura = comida lock"; C1 hijo hereda "miel_oscura = desconocido". En R7, si ambos se cruzan, ¿qué ven?

**Cómo arreglar:** Preregistrar: "mundo global y determinista. Tabla de cambios por familia por ronda, fija antes de R6, congelada en registro."

---

### Error 3: Alias débil y divergencia de representación (IMPORTANTE)

**Descripción:** Dos células aprenden miel_oscura = +1.2; pero sus códigos internos son **distintos** (1–2% alias). Si uno muere y la descendencia cría del otro, el nuevo código se hereda. A la generación 3, el grupo **no reconoce a sus propios abuelos** (código diferente, mismo estímulo).

**Test en R5 vs R6:** C2 aprendió miel_oscura = +1.2; C5 aprendió miel_oscura = +0.5 (menor). ¿Mismo token miel_oscura o variante? Reportes no especifican. Si es el mismo, el delta sugiere **representación divergente** (C2 codificó "miel oscura variante blanda"; C5 codificó "miel común").

**Cómo arreglar:** (B-5 del tronco v14.1) Desambiguar cuando una célula consolidada (|Wp−Wn|>0.2) recibe otro refuerzo de signo contrario bajo una retina distinta → divide y deja el código limpio. Costo: más celdas, pero convergencia más rápida.

---

### Error 4: Descendencia hereda desventaja (BLOQUEO DE ADAPTACIÓN)

**Descripción:** C5 hijo hereda miel_oscura = +0.5 (padre aprendió +0.9 en R6, pero la herencia captura el estado R5 o R6-temprano). El hijo PARTE de una representación subóptima.

Pero **peor:** C2 hijo hereda "miel_oscura +1.2 descubrimiento sin testeo". Si en R7 miel_oscura invierte de nuevo (comida → veneno), el hijo **no sabrá que fue sorpresa** (no la probó). Evitará por herencia, no por miedo aprendido. **Trampa cognitiva.**

**Cómo arreglar:** Heredar pesos pero NO valores bloqueados. M1 heredado con flag "redescubre esto si lo ves sin consecuencia esperada".

---

### Error 5: Mensajes sin integración (PUERTA FALSA)

**Descripción:** C2 emitió "C10 mentiroso detectado (+0.9 falso, sal_rosa real +0.3)". C2 marcó la alerta en M3 (H7). Pero **no hubo QUERY bilateral.** ¿Quién validará H7 en R7? Solo C2 y C10. Si C10 testea sal_rosa nuevamente en R7 y confirma +0.3, C2 actualiza H7 a "C10 honesto"; si C10 no testea, C2 nunca sabrá.

Canal sin cierre = población con hipótesis **falsas pero no refutadas**.

**Cómo arreglar:** Cada emisión debe incluir "predicción falsable R7 con medida y control". Receptor RESPONDE con R7 datos. Coordinador integra en síntesis post-R7.

---

## HIPÓTESIS COMPROBABLES CON EL MÉTODO

### H1. Triplet (familia+textura+ronda) es predictor universal ≥0.85

**Predicción registrada antes de R7:**
- Si sal_blanca_blanda R7 → esperado +0.40 (comida, familia sal baja volatilidad)
- Si larva_rosa_blanda R7 → esperado −0.70 (evitar, familia larva alta volatilidad)
- Si raíz_blanca_blanda R7 → esperado +0.50 (comida, familia raíz resiliente)
- Si miel_oscura persiste R7 → esperado +0.8–+1.2 (no invierte de nuevo)

**Medida:** Validación cruzada de H8 en R7. Si ≥2/3 predicciones son correctas → H1 parcialmente refutada, H8 REFORZADA.

**Control:** Comparar con modelo color-solo (predictor alternativo). Si color-solo acierta ≥2/3 también → H8 no es necesaria.

**Refutación:** Si <2/3 predicciones aciertan → H8 rechazada, proponer H9 (mundo estocástico).

---

### H2. Miel_oscura es token irreplaceable, no invierte universalmente

**Predicción:** En R7, miel_oscura persiste comida (+0.8–+1.2) para células que la vieron en R6 comida.

**Medida:** Frecuencia de inversión R6→R7 para miel_oscura vs larva_blanca (control: larva_blanca invierte universalmente −2.0).

**Falsable:** Si miel_oscura vuelve a invertir en R7 → mundo es **periódicamente mutable** (no binario familia+ronda, sino ronda+fase cíclica). Entonces H1 necesita dimensión "fase_mundial_ronda".

---

### H3. Herencia epigenética con ruido ±5% ralentiza redescubrimiento

**Predicción:** Descendientes heredan M1±5%, M3±2%, pero NO redescubren más rápido. En R7, un descendiente que hereda miel_oscura = +1.2 necesitará ~8–10 exposiciones para validar (mismo que aprender de cero si lo olvida).

**Medida:** Comparar velocidad de aprendizaje en R7 entre nuevas células (crecimiento de grupo) vs descendientes de R6.

**Hipótesis alternativa:** Si descendientes redescubren en 3–5 exposiciones → herencia NO es ruido, es **prior estructural**.

---

### H4. Alias débil (1–2% de pares) divergencia de representación

**Predicción:** Si dos células aprenden miel_oscura en R6 (C2 +1.2, C5 +0.5, C8 +0.9), sus códigos internos divergen. En R7, si un descendiente de C2 se cruza con un descendiente de C5, no reconocen que ambos padres aprendieron lo mismo (código distinto → no heredan juntos).

**Medida:** Correlación de códigos entre células. Si alias < 3%, correlación < 0.7.

**Test:** Descendientes de C2 + C5 comen miel_oscura juntos. Si el esperado es "ambos aceptan comida", pero uno evita → divergencia confirmada.

---

### H5. Mundo muta selectivo por familia+ronda, no universal

**Predicción:**
- Larva: invierte binario (comida ↔ veneno) cada ronda para cada célula que lo probó.
- Miel: muta suave (±0.1 a ±0.3 valor) pero invierte en hito ronda específico.
- Seta: persiste tóxica (−0.7 a −2.8) sin cambio.
- Raíz: suave (±0.2 valor), familia resiliente.

**Medida:** Tabla de cambios por familia por ronda por célula. Si patrón es consistente → H5 confirmada. Si random → mundo estocástico.

---

## CALIBRACIÓN PARA RONDA 7

### Pesos (M1 Vía Rápida)

**Incrementar:**
- Triplet (familia, textura, ronda): 0.85 confidence (de 0.60 en R5)
- Miel_oscura lock: +1.2 (preservar, no desaprender)
- Larva_blanca lock: −2.0 crítica (sin prueba en R7 a menos que sorpresa )

**Mantener:**
- Raíz_azul: +0.85–+1.5 estable
- Sal_rojo/sal_blanca: +0.3–+0.4 (testear H1 sal_blanca_blanda)

---

### Dimensiones (M2 + M3)

**Tabla M1 (reflejo):** Expandir de 20–25 tokens a 30–40 (R7 debe explorar nuevas variantes: seta_azul_blanda, larva_roja_blanda, baya_azul).

**Tabla M2 (episódica):** Retener últimos 5 episodios relevantes (actualmente 3). Cada episodio: (estímulo, recompensa, sorpresa δ, contexto_ronda, emisión_recibida).

**Tabla M3 (hipótesis):** 10–12 hipótesis activas. Nuevas:
- H1: Triplet universal
- H2: Miel_oscura irreplaceable
- H3: Herencia redescubrimiento
- H4: Alias divergencia
- H5: Mundo selectivo por familia+ronda
- H6 (R5): Sal emergente (testear diagonal familia-textura-ronda)
- H7 (R6): C10 liar-detection (validar QUERY bilateral R7)
- H8 (R6): Rango familia domina (HIPÓTESIS PRIMARIA)
- H9 (nuevo): Mundo estocástico vs determinista
- H10 (nuevo): Descendencia conflicto código (alias divergencia)

---

### Estrategia de grupo

**Emisión R7:**
1. **Cada célula emite H8 predicción falsable** (triplet test): "Si sal_blanca_blanda → +0.40, testeable R7". Recompensa estimada +0.9 si sorpresa educativa.
2. **QUERY bilateral coordinada:** Equipo Sal valida sal_blanca/sal_rojo/sal_verde. Equipo Larva testea larva_rosa_blanda/larva_azul. Equipo Miel valida miel_oscura persistencia.
3. **Emisión crítica a coordinador:** Cada célula emite "qué fracasó en mis predicciones H7, qué sorpresa cambió M3".
4. **Cierre de loop:** Receptor RESPONDE "yo probé X, obtuve Y, error vs tu predicción Z". Coordinador integra.

**Recompensas:**
- Emisor: +0.9 si sorpresa educativa + falsable clara + control explícito.
- Receptor: +0.3 si valida contra sí mismo (predicción vs exposición, error bajo).

**Descenso de ruido hereditario:** M1 heredado ±5% → ±3% (más fidelidad, menos redescubrimiento).

---

### Métricas de éxito R7

1. **Convergencia:** ≥3 células independientes aprenden el mismo token con código similar (>0.8 correlación).
2. **Refutación de H1:** ≥2/3 predicciones de H8 aciertan en R7.
3. **Cierre de H7:** C10 y C2 QUERY bilateral valida liar-detection.
4. **Herencia confirmada:** Descendientes de R6 redescubren miel_oscura en <8 exposiciones (mejor que aprender de cero).
5. **Mundo determinista:** Miel_oscura invierte para TODAS las células que la prueban (no local).

---

## TABLA DE ERRORES Y ESTADO

| Error | Localización | Gravedad | Estado | Acción R7 |
|-------|--------------|----------|--------|-----------|
| Puerta asimétrica canal | protocolo sala 3 | CRÍTICA | Destapado | Agregar recompensa receptor |
| Mundo local vs global | mundo vivo | CRÍTICA | Destapado | Preregistrar determinismo |
| Alias débil (1–2%) | representación | IMPORTANTE | Destapado | Aplicar B-5 desambiguar |
| Descendencia desventaja | herencia | IMPORTANTE | Destapado | Heredar pesos, no locks |
| Mensajes sin cierre | canal QUERY/REPLY | IMPORTANTE | Destapado | Coordinador cierra loops |

---

## CONCLUSIÓN

**Ronda 6 fue CRÍTICA:** el descubrimiento de miel_oscura_inversión validó que el mundo **NO es tabla estática** sino que muta por ronda. Esto elevó la sofisticación grupal: la población pasó de "aprender valores de una tabla fija" a "modelar mutación selectiva". **H8 emergente (rango familia domina) es la primera hipótesis de nivel 9** (modelo de mundo vivo con cambio).

**Pero la arquitectura muestra grietas:** canal asimétrico, alias débil, y mundo local vs global mantienen a la población en **equilibrio crítico**. Una célula descubre; otras validan pero no integran. Descendientes heredan desventaja.

**R7 es decisivo:** si cierre de loops funciona (QUERY bilateral coordinada), la población convergerá en modelo unificado y entrará en **aprendizaje de verdad**. Si no, divergirá en interpretaciones locales y apenas llegará a R8.

---

## APÉNDICE: SÍNTESIS DATOS GRUPO B R6

| Célula | Exposiciones | M1 tokens | H nuevas | Descendencia | Recompensa emisión |
|--------|-------------|-----------|----------|-------------|-------------------|
| C2     | 20          | 22        | H8       | 1 (r=2)     | +0.9               |
| C5     | 16          | 20        | H5       | 2 (r=2)     | +0.05 + 0.0        |
| C8     | 20          | 23        | H8 primaria | 1 (r=6) | +0.9               |
| C11    | 20          | 25        | H11      | 1 (r=3)     | +1.5 + 0.7         |
| **GRUPO B** | **76** | **~23 promedio** | **H8 convergencia** | **5 viables, r=0.75** | **+0.8 promedio** |
| Otros (8 células) | ~150 | ~20 promedio | H6–H8 variadas | 5 viables, 2 muertes | +0.4 promedio |
| **POBLACIÓN TOTAL** | **~226** | **~21.5** | **H8 EMERGENTE** | **10 viables, r=+0.45** | **+0.6 global** |

---

*Registrado: Análista investigación, sala 4 evolución. Siguiente paso: R7 con protocolo cierre de loops.*
