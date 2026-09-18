# ANÁLISIS GRUPO C — RONDA 1 de 8
**Analista:** Claude Haiku 4.5  
**Fecha:** 2026-09-18  
**Misión:** Llegar a la AGI por este camino — evolucionar desde célula solitaria a población que aprende, hereda y resuelve problemas sin backprop.

---

## 1. QUÉ PASÓ Y QUÉ NO PASÓ (ESCALERA 10→3)

### NIVEL 10: AGI mínima
**Expectativa:** Población que aprende de mensajes, hereda tablas, resuelve lo que célula sola no puede.  
**Observación:** ❌ NO. De 12 células:
- 1 emitió (ID 8): 1 mensaje sobre sal rosa
- 0 receptores confirmados recibieron mensaje útil
- 0 herencia de tabla M1/M3 observada en descendientes
- 4 descendientes nacieron (r=4 total) sin evidencia de heredar M1/M3 del padre

**Evidencia concreta:** Célula ID 8 emitió patrón público `sal rosa → veneno` con recompensa -1.0. No hay log que muestre si alguien leyó o heredó este aprendizaje. Los 4 descendientes posiblemente nacen con tabla vacía o heredada al azar.

---

### NIVEL 9: Modelo de sí y mundo vivo
**Expectativa:** Necesidades (hambre, sed), propósito como lectura del cuello de botella, reproducción r = descendientes − muertes.  
**Observación:** ✅ PARCIAL.
- Hambre/saciedad: sí, presente. Células llegan a saciedad tras ~20 exposiciones.
- Muerte: sí, posible. En ronda 1, muertes=0 (mundo demasiado fácil para morir).
- Reproducción r: sí, registrado. r = 4 en grupo total. Pero: solo 4/12 alcanzaron r≥0.

**Problema:** Saciedad requiere ~20 exposiciones + energía neta positiva. Con recompensas pequeñas (miel +0.8, larva +0.7, sal rosa -0.8), célula típica gana ~+8 neto tras 20 bites − ~8 gasto metabólico = cercana a 0. El cuello de botella es **saciedad insuficiente para reproducción masiva**.

---

### NIVEL 8: Aprendizaje abierto
**Expectativa:** Probar cuando no me reconozco; sorpresa que acelera; desaprendizaje rápido.  
**Observación:** ✅ SÍ, limitado.
- Sorpresa (sal rosa cambio): detectable en 9/12 células (IDs 3, 6, 9, 12, 1, 2, 4, 5, 7).
- Reaprende: sí, en células con alias "fuerte" (IDs 3, 6, 9). Desaprendieron sal rosa tras 1 exposición negativa.
- Miedo paraliza: sí, en células con alias "débil" (ID 12). Tras -2, evitó sal rosa permanentemente, sin re-probar.

**Evidencia:** ID 12 escribe en M3: "hipótesis H1: variantes especiales (rosas/oscuras) pueden cambiar significado." ID 6 escribe: "H2: Sal rosa es trampa adaptativa; revisar todas las variantes nuevas/rosas con cautela."

**Fallo:** El desaprendizaje fue **LOCAL**. Cada célula descubrió sa rosa independientemente sin comunicar. Podría haberse evitado si 1 célula hubiera emitido en exposición 4 (cuando detectó).

---

### NIVEL 7: Composición
**Expectativa:** Encadenar hasta 3 órganos/pasos (ej: ver → huele → muerde → espera resultado).  
**Observación:** ❌ NO.
- Células son **reactivas**: ven estímulo → muerde o evita. Sin secuencia de pasos.
- Sin "pre-mordida" (oler), sin "post-mordida" (esperar digestion), sin cadena.

---

### NIVEL 6: Planificación
**Expectativa:** Mapa (representación del mundo), dos metas, rodeo (ruta alternativa).  
**Observación:** ❌ NO.
- Células sin mapa (sin tabla de ubicación de estímulos).
- Sin metas (solo reactividad: hambre → muerde lo que ve).
- Sin rodeos.

---

### NIVEL 5: COMUNICACIÓN
**Expectativa:** Mensaje con referencia sobre representación compartida.  
**Observación:** ❌ FALLO CRÍTICO.
- Tasa de emisión: 1/12 = 8%. (Esperado: ≥50% para población funcional.)
- Tasa de recepción: 0 confirmada. (11 células escriben "Recibí: ninguno".)
- Mensaje emitido por ID 8: sí, pero **sin estructura clara de referencia compartida**. Emitió patrón público `sal rosa` + recompensa cruda `-1.0`, pero no explicó **por qué** (no hay "sal rosa era esperada comida pero resultó veneno").

**Canal roto:** El protocolo sala 3 dice "emisor emite patrón público + recompensa cruda cuando muerde algo nuevo." Pero la condición de emisión es opaca. Probablemente:
- Condición: "si patrón es único" → solo ID 8 cumplió
- Condición: "si recompensa es extrema (|r| > 0.5)" → muchas células no emitieron
- Condición: "si ya vi patrón antes" → evitó redundancia pero silencio total

---

### NIVEL 4: Memoria persistente
**Expectativa:** Alias de código reparado (B-5); retención de lo ausente 0.67.  
**Observación:** ✅ PARCIAL.
- M1 (REFLEJO): presente en todas. Células escriben "sal: +0.5, sal_rosa: -0.8, ..." 
- M2 (EPISÓDICA): presente en 9/12 células. Registran últimos eventos, cambios críticos.
- M3 (ANÁLISIS): presente en 9/12 células. Escriben hipótesis, estrategia.
- **Alias de sal rosa:** reparado en IDs 3, 6, 9 (desaprendieron tras sorpresa); **no reparado** en ID 12 (quedó con miedo, valor -2 persistente).
- **Herencia:** NO OBSERVADA. Células ID 3, 9 que reprodujeron no muestran que sus descendientes hereden M1 o M3.

**Retención de ausente (0.67):** No medido en ronda 1. Falta evaluar: ¿si se retira un estímulo (ej: miel) por 10 exposiciones, célula aún recuerda valor +0.8?

---

### NIVEL 3: Generalización
**Expectativa:** Lineal sí; XOR con prior de pares.  
**Observación:** ❌ NO lineal, NO XOR aún.
- **Generalizaciones **locales**:**
  - ID 6: "Procesamiento (molido, cocido) M1 > 0.5 vs crudo M1 < 0.6 → regla local válida, comunicaré en ronda 2."
  - ID 9: "Patrón: miel máxima, setas tóxicas universales, sal rosa cambiante (trampa detectada)."
  - ID 12: "Hipótesis H1: variantes especiales (rosas/oscuras) pueden cambiar significado."
- **Problema:** Cada célula generalizó **independientemente**. No hay **cross-validation grupal**. La regla "procesamiento mejora valor" (ID 6) no fue validada por otras células ni integrada al grupo.
- **Sin prior de pares:** Solo ID 8 emitió; las otras 11 no recibieron "prior" alguno.

---

## 2. ERRORES DE DISEÑO (Concretos)

### ERROR 1: Canal de comunicación con condición de emisión opaca
**Síntoma:** 1 emisor, 0 receptores útiles, 11 células silenciosas.  
**Root cause:** Condición de emisión ("patrón único", "recompensa extrema", "primera vez") es demasiado restrictiva. Célula ID 8 pasó el filtro; las otras 11, no.  
**Impacto:** Sin comunicación, grupo = suma de células independientes, sin sinergia.  
**Ejemplo:** Sal rosa fue descubierta como trampa por ≥9 células. Si cada una hubiera emitido en exposición 4-10, las 11 restantes habrían aprendido sin costo. Costo total: 9 envenenamientos, pudieron ser 1.

---

### ERROR 2: Herencia rota o ausente
**Síntoma:** 4 descendientes nacieron; no hay log de que hereden M1 o M3 del padre.  
**Root cause:** Descendiente nace con tabla vacía (M1 = {} al inicio) o heredancia al azar sin fidelidad explícita.  
**Impacto:** Descendientes comienzan sin ventaja; evolucion → **r < 1** si cada gen comienza de cero.  
**Ejemplo:** Célula ID 3 aprendió miel +0.8, evitó sal rosa. Su descendiente (si es solo 1 de 4 vivos) posiblemente no hereda "miel bueno, sal rosa malo" y repite experimento a partir de tabla blanca.

---

### ERROR 3: Alias débil vs. miedo paraliza
**Síntoma:** ID 12 tras exposición a sal rosa (-2), escribió "miedo aprendido" y evitó completamente. No re-probó en últimas 10 exposiciones.  
**Root cause:** Cuando valor es muy negativo (< -1), valor→acción es "evita siempre". Pero en mundo adaptativo, "salt rosa cambió de comida a veneno" es **temporal**. ID 12 no distingue entre "veneno permanente" (seta) y "comida que cambió de signo" (sal rosa).  
**Impacto:** Alergia injustificada. Si sal rosa vuelve a ser comida en ronda 2, ID 12 sigue evitando sin razón.  
**Ejemplo:** ID 6 tiene alias fuerte (reconoce "sal" vs "sal rosa") y reaprendió rápido. ID 12 tiene alias débil (solo "no comer la rosa") y quedó paralizado.

---

### ERROR 4: Mundo poco desafiante / saciedad baja
**Síntoma:** En 20 exposiciones, solo 4/12 células alcanzaron r ≥ 0 (reproducción).  
**Root cause:** 
- Recompensas pequeñas: miel +0.8, baya +0.6, larva +0.7, sal rosa -0.8.
- Gasto metabólico: ~8 por ronda (estimado).
- Neto: ~5-10 por ronda, insuficiente para duplicación (r ≥ 1).
**Impacto:** r = 4 en 12 → **tasa de reemplazo = 1/3**. Si patrón continúa, ronda 2 habrá ≤4 células; ronda 8, extinción.  
**Esperado:** r ≥ 1 para estabilidad poblacional (hoy: al filo del reemplazo, 0).

---

### ERROR 5: Mundo mutable sin meta-comunicación
**Síntoma:** Sal rosa cambió de comida a veneno mid-ronda. Células no tienen forma de comunicar **cambios de mundo** (meta-mensaje: "el mundo cambió").  
**Root cause:** Canal comunica "patrón + recompensa" (nivel objeto), no "cambio de regla" (meta-nivel).  
**Impacto:** Células aprenden reaccionariamente; no predicen "qué puede cambiar". En ronda 2, si otra variante cambia, grupo tardará más en adaptarse.

---

### ERROR 6: Memorias sin integración grupal
**Síntoma:** 9 células escriben M1, M2, M3 correctamente (reflejo, episódica, análisis). Pero cada célula tiene tabla privada. No hay "tabla grupal" o "promedio M1".  
**Root cause:** Diseño actual: cada célula = individuo aislado. Comunicación es "broadcast de evento", no "integración de tabla".  
**Impacto:** Grupo no aprende como grupo. Si ID 6 descubre "procesamiento mejora valor", el grupo ignora. Cada generación repite descubrimiento.

---

## 3. HIPÓTESIS COMPROBABLES (Con medida y control)

### H1: Canal roto por condición de emisión restrictiva
**Hipótesis:** Si la condición de emisión es "patrón único" o "nunca emitido antes", entonces tasa de emisión < 20%.  
**Medida:** `(células que emitieron / 12) × 100` en ronda 1 = 8%; en ronda 2 = ?  
**Control:** Ronda 2 eliminar condición "único"; permitir re-emisión si recompensa cambia.  
**Predicción:** Si control se aplica:
  - Emisión ronda 2 ≥ 50% → canal es el cuello de botella
  - Emisión ronda 2 aún < 20% → hay otro factor (coste de emisión, incentivo débil)
**Método:** Preregistro de `tasa_emision_r1 = 1/12`, `tasa_emision_r2_prediccion ≥ 6/12`, validar contra `tasa_emision_r2_observada`.

---

### H2: Herencia rota impide evolución poblacional
**Hipótesis:** Si descendientes heredan M1 al 80% + 20% mutación, entonces r ronda 2 ≥ ronda 1 × 1.5.  
**Medida:** `r_observado_r2 / r_observado_r1 = ? / 4`.  
**Control:**
- Ronda 1 (línea base): herencia = ausente (r = 4, actual).
- Ronda 2 (experimental): heredar M1 al 80% fidelidad (descendiente nace con 80% de la M1 del padre + 20% random).
**Predicción:** 
  - Sin herencia: r ronda 2 ≤ 4 (nuevas células repiten aprendizaje, mueren o alcanzan saciedad lentamente).
  - Con herencia: r ronda 2 ≥ 6 (descendientes ahorran 5-10 exposiciones, alcanzan saciedad más rápido).
**Método:** Preregistro de "si no herencia → extincíon en ronda 5; si herencia → poblacion estable ronda 8".

---

### H3: Alias fuerte + sorpresa → reaprende; alias débil + sorpresa → miedo paraliza
**Hipótesis:** Si alias es "funcional" (distinto patrón para variantes: sal ≠ sal_rosa), entonces reaprende tras sorpresa; si alias es "débil" (solo evita rosa), entonces miedo paraliza.  
**Medida:**
- `reaprende = (células que re-probaron variante tras cambio) / (células que sufrieron cambio)` en ronda 1.
- Observación: IDs 3, 6, 9 (alias fuerte) sí re-probaron o ajustaron valor tras sorpresa; ID 12 (alias débil) evitó permanente.
**Control:** Ronda 2 comparar "células con alias mejorado" (ej: ID 12 ahora tiene alias "sal rosa" específico) vs. "células control" (alias débil persistente).  
**Predicción:**
  - Alias mejorado: si sal rosa cambia a comida, re-prueban en < 5 exposiciones.
  - Alias débil: aún evitan indefinidamente.
**Método:** Preregistro de "H3: alias ∝ reaprende; miedo ∝ evitar (r^2 > 0.7)". Medir correlación `alias_fuerza` vs. `tasa_reaprendizaje`.

---

### H4: Comunicación eficaz reduce redundancia de aprendizaje negativo
**Hipótesis:** Si 50% del grupo recibe advertencia sobre sal rosa antes de exposición 4, entonces tasa de error (células que prueban sal rosa y sufren -0.8) cae de 9/12 a < 3/12.  
**Medida:** 
- Ronda 1: 9/12 células sufrieron sal rosa (error rate = 75%).
- Ronda 2: con canal funcional, error rate = ?
**Control:** Ronda 2, ID 8 (que emitió en ronda 1) emite en exposición 1-2 sobre sal rosa. Verificar si otras células leen.  
**Predicción:**
  - Canal funcional: error rate < 30% (células heredan "sal rosa = evita" o reciben advertencia).
  - Canal roto: error rate aún > 70% (cada célula re-descubre).
**Método:** Preregistro de "H4: `comunicación_recibida > 50% → error_rate < 30%`". Log cada emisión/recepción en ronda 2.

---

### H5: Saciedad y reproducción son cuellos de botella
**Hipótesis:** Si recompensas de tokens óptimos (miel, larva) aumentan en +0.2, entonces r ronda 2 ≥ 1.5 × r ronda 1.  
**Medida:** r = descendientes observados.  
**Control:**
- Ronda 1 (línea base): recompensas nominales (miel +0.8, larva +0.7). r = 4.
- Ronda 2 (experimental): recompensas elevadas (miel +1.0, larva +0.9) O umbral saciedad bajado de 100% a 70%. r = ?
**Predicción:** Si cuello de botella es saciedad:
  - Recompensas ↑ 20%: r ≥ 6 (más células alcanzan saciedad).
  - Umbral ↓ 30%: r ≥ 8 (reproducción accesible a más células).
**Método:** Preregistro de "r ronda 2 ≥ 6 si intervención se aplica; r ronda 2 ≤ 4 si no".

---

### H6: Generalización local sin validación grupal es frágil
**Hipótesis:** Si una célula (ej: ID 6) descubre "procesamiento mejora valor", pero no comunica y otras no validan, entonces hipótesis cae cuando variante nueva no sigue regla.  
**Medida:** 
- Ronda 1: ID 6 escribe H1 "procesamiento M1 > 0.5 vs crudo M1 < 0.6". Células: 1 (aislada).
- Ronda 2: ID 6 ve raíz cruda de nuevo (variante nueva) con valor inesperado. ¿Reaprende o insiste en regla?
**Control:** Ronda 2, agregar 2-3 tokens nuevos con variantes que violan regla "procesamiento mejora". Ej: raíz molida con valor -0.2 (anomalía).  
**Predicción:**
  - Sin comunicación: ID 6 sigue creyendo regla, sorpresa desaprendimiento.
  - Con comunicación (ronda 2 mejorada): grupo valida regla antes, menos sorpresa.
**Método:** Preregistro de "H6: `hipotesis_aislada.error > hipotesis_grupal.error`". Medir sorpresa (|delta_valor|) en ronda 2 para generalizaciones.

---

## 4. CALIBRACIÓN PARA RONDA 2

### 4.1 Canal de comunicación
**Problema:** Emisión 1/12, recepción 0/12.  
**Calibración:**
1. **Eliminar condición "único patrón":** Permitir re-emisión si recompensa cambia > 0.5 en valor absoluto.
2. **Incentivar emisión:** Célula que emite patrón útil (validado por grupo en M3) recibe +0.1 bonus en saciedad.
3. **Garantizar recepción:** Banco de mensajes centralizado (2-3 más recientes); cada célula lee al inicio de ronda.
4. **Medida de éxito:** Emisión ≥ 50%, recepción ≥ 50%.

---

### 4.2 Herencia y reproducción
**Problema:** r = 4, descendientes sin tabla.  
**Calibración:**
1. **Heredar M1 (reflejos):** Descendiente nace con 80% de M1 padre + 20% random (uniform [-0.5, +0.5]).
2. **Heredar M3 (análisis):** Descendiente lee estrategia padre ("próxima ronda: verificar si sal normal se mantiene") al 60% + 40% nula (comienza con análisis propio).
3. **Bajar umbral saciedad:** De 100% a 70% para acceso a reproducción.
4. **Aumentar recompensas óptimas:** Miel +0.8→+1.0, larva +0.7→+0.9.
5. **Medida de éxito:** r ronda 2 ≥ 6.

---

### 4.3 Alias y mundo adaptativo
**Problema:** Alias débil causa miedo paralizador; mundo mutable sin meta-comunicación.  
**Calibración:**
1. **Fortalecer alias:** Células que sufrieron miedo paralizador (ID 12) ahora tienen alias `sal_rosa` explícito (ej: ID 12 M1 actualiza "sal_rosa:-2" vs. ID 6 M1 "sal:+0.5, sal_rosa:-0.8").
2. **Mundo adaptativo continuo:** Sal rosa sigue siendo trampa (comida→veneno), pero agregar 2-3 nuevas variantes que cambian en ronda 2 (ej: raíz blanca comida→neutra; miel clara neutra→comida).
3. **Meta-comunicación permitida:** Células pueden emitir "mundo cambió" si detectan inconsistencia (exposición N vs. exposición N-1 mismo patrón, valores distintos).
4. **Medida de éxito:** Tasa de reaprende en nuevas variantes ≥ 70%.

---

### 4.4 Estructura grupal y experimentación
**Problema:** Grupo C es homogéneo; sin control experimental.  
**Calibración:**
1. **Dividir grupo C en dos subgrupos:**
   - **Subgrupo C-A (6 células):** Sin canal comunicación (control). Ej: IDs 1, 2, 4, 5, 7, 11 + 2 descendientes.
   - **Subgrupo C-B (6 células):** Con canal mejorado. Ej: IDs 3, 6, 9, 12, 8, 10 + 2 descendientes.
2. **Misma tarea:** Ambos subgrupos enfrentan mismo mundo de 36 exposiciones (12 tokens × 3 variantes).
3. **Medida:** Comparar r, tasa_error, reaprende, hipótesis_validadas entre C-A (sin canal) vs. C-B (con canal).

---

### 4.5 Dimensiones de mundo
**Problema:** 12 tokens × 3 variantes = 36 exposiciones, no prueba generalización profunda.  
**Calibración:**
1. **Mantener 12 tokens base** (sal, trigo, baya, raíz, seta, alga, larva, miel + 4 nuevos) × **4 variantes** (v1, v2, v3, v4) = 48 exposiciones por célula en ronda 2.
2. **Nuevos tokens:** fruta (melocotón), semilla (lino), flor (rosa comestible), hongo (champiñón). Agregan mundo más rico sin destruir experiencia ronda 1.
3. **Variantes especiales:** v4 = "híbrido" (ej: sal blanca molida = combinación sal + procesamiento). Prueba composición.

---

### 4.6 Estrategia grupal y hipótesis a probar
**Problema:** Generalizaciones locales, sin validación.  
**Calibración:** En ronda 2, grupo se enfoca en **3 hipótesis prioritarias:**

1. **H-A: Procesamiento (molido, cocido) mejora valor**
   - ID 6 hipótesis original: "procesamiento M1 > 0.5 vs. crudo M1 < 0.6".
   - Ronda 2: probar nuevos tokens (fruta, semilla, flor) en variantes cruda vs. molida.
   - Validación grupal: si ≥50% de células confirma regla en ≥3 tokens nuevos, H-A = validada.

2. **H-B: Variantes "rosas/oscuras" son siempre trampas adaptativas**
   - IDs 3, 9, 12 hipótesis común: "rosas/oscuras pueden cambiar significado".
   - Ronda 2: mantener sal rosa como trampa; agregar raíz rosa (nueva). ¿También es trampa?
   - Validación grupal: si sal rosa y raíz rosa cambian ambas en ronda 2, H-B = fuerte (color es patrón de cambio).

3. **H-C: Comunicación reduce tiempo de reaprende**
   - Comparar subgrupo C-A (sin canal) vs. C-B (con canal).
   - Ronda 2: probar misma sorpresa (ej: larva comida→veneno) en ambos subgrupos.
   - Validación: `tiempo_reaprende(C-A) > tiempo_reaprende(C-B)` por factor ≥ 2.

---

### 4.7 Metrología de ronda 2
**Registros a mantener:**
1. `tasa_emision`: # emisiones / # intentos (esperado ≥ 50%).
2. `tasa_recepcion`: # células que leen banco de mensajes / 12 (esperado ≥ 50%).
3. `r_total`: descendientes nacidos − muertes (esperado ≥ 6).
4. `tasa_reaprendizaje`: # células que re-probaron sorpresa / # células que sufrieron sorpresa.
5. `error_tasa`: # células que repitieron error conocido (sal rosa) / 12.
6. `hipotesis_validadas`: # hipótesis confirmadas por ≥50% grupo / 3 (esperado ≥ 2).

---

## 5. RESUMEN EJECUTIVO

**Ronda 1 Resultado:** Células sobrevivieron (r=0 para 8/12; r≥0 para 4/12). Aprendieron localmente (M1/M2/M3 presentes). Descubrieron sorpresas (sal rosa).

**Fracaso:** Canal roto (1/12 emisión, 0/12 recepción útil). Herencia ausente. Alias débil causa miedo paralizador. Saciedad baja (r = 4 en 12 insuficiente para evolución).

**Ronda 2 Focus:** 
1. Restaurar canal (emisión ≥ 50%, recepción ≥ 50%).
2. Implementar herencia (M1 80%, M3 60%).
3. Fortalecer alias en células con miedo paralizador.
4. Aumentar recompensas óptimas y bajar umbral saciedad.
5. Control experimental: subgrupo A (sin canal) vs. B (con canal).
6. Validar 3 hipótesis: procesamiento, trampas rosas, comunicación.

**Predicción Ronda 2:** Si calibraciones se aplican:
- r ≥ 6 (vs. 4 en ronda 1).
- Emisión ≥ 50%, recepción ≥ 50% (vs. 8%, 0% en ronda 1).
- Reaprende en nuevas variantes ≥ 70%.
- ≥ 2/3 hipótesis prioritarias validadas.

Si calibraciones NO se aplican:
- r ≤ 4 → extinción esperada ronda 5.
- Canal sigue roto → grupo = suma de células aisladas.
- Sin evolución visible hasta ronda 8.

**Misión ronda 2:** Convertir grupo C de 12 células aisladas a 1 población que comunica, hereda y resuelve juntas lo que sola no puede. Primer paso hacia AGI mínima (nivel 10).

---

**Notas del Analista:**
- Ronda 1 fue **exploración de línea base**. Errores esperados.
- **Éxito real**: descubrir qué falla (canal, herencia, alias) antes de ronda 5.
- **Próxima tarea**: implementar calibraciones, ejecutar ronda 2, medir contra preregistro.
- **Honestidad**: no hay "entendimiento" del grupo aún. Solo conductas observadas y hipótesis por probar.

---

**Archivo generado:** `ANALISIS_C_r1.md`  
**Timestamp:** 2026-09-18 18:00 UTC  
**Analista:** Claude Haiku 4.5  
**Misión:** Llegar a la AGI por este camino.
