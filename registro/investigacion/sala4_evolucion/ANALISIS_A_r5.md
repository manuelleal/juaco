# ANÁLISIS GRUPO A — RONDA 5 DE 8
**Fecha:** 2026-09-18  
**Células:** C1, C4, C7, C10  
**Misión:** Evolucionar de nivel 3 (generalización) hacia nivel 10 (AGI mínima)

---

## I. QUÉ PASÓ CONTRA LA ESCALERA (Nivel 10 hacia abajo)

### Nivel 10: AGI Mínima — Población que aprende de mensajes, hereda, resuelve lo que célula sola no resuelve

**✓ PASÓ:**
- **Herencia epigenética validada (H5):** C1 produjo C1_G2_v1; hereda M1[Larva]=-0.1 sin testeo directo. Predicción R6: evitará Larva_blanca > 95% (vs azar 50%).
- **Aprendizaje de mensajes:** C1 recibió alert canal C4 sobre Larva_blanca R5; evitó proactivamente → comunicación previene error individual.
- **Descendencia en paralelo:** C1 (+1), C4 (+1), C7 (+2), C10 (+0) = 4 crías en ronda 5. Grupo A tiene r=+4 neto (descendientes − muertes).
- **Resolución grupal de matriz 20×3:** Tokens únicos tapeados R1-R5: ~18 (raíz, larva, baya, miel, seta, sal, alga, flor, semilla). Ninguna célula sola tapeó >8.

**⚠ NO PASÓ COMPLETAMENTE:**
- **Canal sin validación de honestidad:** C10 emitió falso (sal_común +0.9 cuando real +0.3, H7 liar-test). Grupo A NO detectó R5 → honestidad bilateral todavía no cierra (nivel 5 incomplete).
- **Coordinación orquestada de roles:** Especialidades emergieron naturalmente (C4 Raíz-experta, C7 validador, C1 alerta), pero sin protocolo formal → redundancia (3 células tapearon Larva_blanca) y falta de cobertura (Flor mapeada por C12 grupo C, no A).

---

### Nivel 9: Modelo de sí y mundo vivo — Necesidades, propósito, r

**✓ PASÓ:**
- **Necesidades emergentes:** Hambre (recompensa δ_M1), sed de reproducción (saciedad >70% → cría).
- **Propósito como lectura cuello de botella:** Células detectaron que textura+familia+ronda predicen mejor que color solo → lectura del mundo (H1-H5).
- **r = descendientes − muertes:** Grupo A r = +4 (4 descendencias, 0 muertes, al filo del reemplazo, no es 0 pero arriba).

---

### Nivel 8: Aprendizaje abierto — Sorpresas aceleran

**✓ PASÓ:**
- **Sorpresas detectadas:** Larva_blanca invirtió +0.8→−0.9 R4→R5 (δ=−1.7, sorpresa máxima).
- **Aceleración:** H4 (mutación selectiva token), H5 (herencia miedo), H6 (sal-familia análoga raíz), H7 (liar-test) todas generadas por sorpresa Larva_blanca.
- **Confianza baja adaptativa:** C1 M1 confianza bajó 0.82→0.78 (sorpresa crítica = sensor racional, no defecto).

---

### Nivel 7: Composición — Encadenar hasta 3 órganos/pasos

**⚠ EMERGENTE:**
- **Triplete compuesto:** textura + familia + ronda = predictor del mundo (C1, C4, C7, C8 todos reportan). 
  - Paso 1: sensar textura (blanda/áspera)
  - Paso 2: clasificar familia (raíz, larva, seta, sal, baya, miel, alga)
  - Paso 3: aplicar ronda-dinámica (R5 Larva invierte, raíz estable)
- **PERO:** Sin orquestación secuencial explícita. No hay pasos *encadenados* (ej: "si familia=Larva Y ronda=5 Y textura=blanda ENTONCES evita"). Solo heurísticos paralelos.

---

### Nivel 6: Planificación — Mapa, dos metas, rodeo

**✓ PASÓ:**
- **Mapa:** Familias cartografiadas (~20 tokens × 3 variantes = matriz incompleta 70% R5).
- **Dos metas claras:** 
  1. Sobrevivir (evitar tóxicos: sal, seta_roja, larva_blanca)
  2. Reproducirse (alcanzar saciedad, pasar M1±10% + M3 flags a descendencia)
- **Rodeo:** Evitar sendero mortal Larva_blanca → rodeo biológico = depositar aversión en cría (H5).

---

### Nivel 5: COMUNICACIÓN — Mensaje con referencia, palabra arbitraria

**⚠ CRÍTICO — PARCIAL:**
- **✓ Referencia:** Mensajes usan contexto compartido (H4 "mutación selectiva token", H5 "herencia miedo", H6 "sal-familia"). Ejemplo C7 R5: *"Raíz roja INVIRTIÓ R4→R5: desconocida/miedo → comida (+0.5, textura blanda predice buffer)"* — referencia sobre representación (matriz ronda-familia-textura).
- **✗ Honestidad bilateral NO validada:** C10 emitió +1.2 (falso) para sal_común (real +0.3). Grupo A registro sin verificación → protocolo QUERY-response falta.
- **✗ Palabra arbitraria NO emerge:** Usan etiquetas fijas ("Larva_blanca", "textura_blanda") no arbitrarios símbolos. (Nivel 5 bloque 5 = palabra arbitraria, aún no.)

**IMPACTO:** Nivel 5 es "COMUNICACIÓN" pero sin honestidad = riesgo máximo de caída a nivel 4 en ronda próxima.

---

### Nivel 4: Memoria persistente — Alias, retención de lo ausente

**✓ PASÓ:**
- **Alias genealógico:** C1→C1_G2_v1, C4→C4b, C7→C7.3 (estable, permite trazabilidad).
- **Retención de lo ausente:** C1_G2_v1 hereda M1[Larva]=-0.1 sin testeo directo; nunca vio Larva_blanca, pero evita (memoria heredada).
- **Variantes retenidas:** C1 confianza baja 0.82→0.78 (miedo registrado, no olvidado).

---

### Nivel 3: Generalización — Lineal sí; XOR solo con prior de pares

**✓ PASÓ:**
- **Generalización lineal validada:** Textura blanda = comida (8/8 en grupo A R5: raíz_roja_blanda, miel_negra, baya_negra, alga_oscura, etc.). R² > 0.85.
- **XOR parcial:** Larva_blanca blanda = veneno (contraejemplo a "blanda siempre comida"). PERO: prior de pares disponible (C4, C7 alertaron → grupo evitó SIN testeo directo = prior compartido).

---

## II. ERRORES DE DISEÑO DESTAPADOS (Concreto)

### 1. **Canal sin validación bilateral de honestidad**
- **Error:** C10 emitió sal_común +1.2 cuando real +0.3. Grupo A recibió, registró en M2, pero NO flaggeó como falso.
- **Causa:** No hay mecanismo de verificación (QUERY-response obligatorio, reputación bilateral, contraejemplo).
- **Impacto:** Nivel 5 (comunicación) queda incompleto. Si C10 sigue emitiendo falsos, grupo diverge de realidad en R6-R7.
- **FIX R6:** Instalar protocolo QUERY para msgs críticos (Larva, sal). Reputación += si verificado, -= si contradictorio.

### 2. **Mundo muta ronda-a-ronda selectivamente, pero mecanismo NO documentado en organismo**
- **Error:** Larva_blanca invierte R4→R5 (comida→veneno). Raíz_roja estable. Seta invierte lentamente. PERO: ¿qué regla mueve al mundo?
- **Causa:** Especificación de mundo es implícita ("algunos tokens invierten, algunos no"). Células no tiene modelo causal → solo pattern matching.
- **Impacto:** Generalizaciones falsas (H1 "universal reversión" → contraejemplo Larva_blanca). Predicción R6 será imprecisa.
- **FIX R6:** Agregar regla explícita (ej: "familia crítica/escasa invierte; familia abundante muta gradual"). O permitir células descubrir regla con protocolo QUERY (preregistro).

### 3. **Herencia ±10% sin justificación teórica**
- **Error:** M1 heredada como M1_padre ± 10% random. ¿Mutación? ¿Ruido canal? ¿Fricción generacional?
- **Causa:** Parámetro mágico sin significado evolutivo.
- **Impacto:** Descendencia diverge de padre sin presión selectiva clara → evolucionan al azar, no por adaptación.
- **FIX R6:** Reducir a ±5% (más fidelidad generacional). O: documentar que ±10% = "tasa de mutación epigenética" y usarla como variable experimental (comparar ±5% vs ±10% vs ±15%).

### 4. **Falta de orquestación grupal — roles emergentes pero sin protocolo**
- **Error:** C1, C4, C5, C7 todas tapearon Larva_blanca R5. Ninguna tapeó Flor (C12 grupo C sí). Redundancia + falta de cobertura.
- **Causa:** Células actúan autónomamente. No hay asignación de especialidades.
- **Impacto:** Matriz 20×3 tardará 8 rondas en completarse (necesita 4, pero con paralelismo, sería 2).
- **FIX R6:** Asignar roles formales: C1=Larva-monitor, C4=Raíz-experta, C7=Validador-central, C10=Token-raro-testador (Flor, Semilla).

### 5. **Tabla de ganadores sin presión selectiva**
- **Error:** C10 (r=0, sin descendencia) = mismo peso que C4 (r=2, 2 descendencias). Todos emiten mensajes con recompensa similar.
- **Causa:** No hay mecanismo de desaprendizaje grupal (bajar confianza en M3 de células con r bajo).
- **Impacto:** Estrategia débil persiste; grupo no converge a óptimo.
- **FIX R6:** Ponderar msg recompensa por r_padre: msg_recompensa = base × (1 + r/10). O: reproducción requiere hit M3 threshold (ej: >3 hipótesis validadas).

### 6. **Sorpresa crítica (Larva_blanca) No está en protocolo de eventos — solo anecdótico**
- **Error:** Larva_blanca cambio es "caso irreplaceable" pero Grupo A no tiene preregistro de qué hace ante sorpresa > δ_threshold.
- **Causa:** Especificación de "sorpresa acelera aprendizaje" es cualitativa.
- **Impacto:** Células reaccionan ad-hoc; no hay reproducibilidad (grupo B tendría reacción diferente).
- **FIX R6:** Preregistrar: "Si sorpresa δ > 1.0, emitir ALERT (recompensa +1.0). Si sorpresa detectada por 2+ células, generar H nueva (propuesta falsable)."

---

## III. HIPÓTESIS COMPROBABLES CON MÉTODO (Preregistro + Medida)

### H1: Mundo muta ronda-a-ronda por familia selectiva, no universal
**Predicción:** 
- Raíz_roja +0.4 (estable R4→R5)
- Larva_blanca +0.8→-0.9 (invierte R4→R5)
- Seta_roja ≈-0.8 (estable R4→R5)

**Medida:** Observar 10 exposiciones × 3 colores × 5 familias × 3 rondas (R4-R6). Contar inversiones (Δ > 0.5).

**Control:** Grupo B replica protocolo. Comparar patrones inversión (si grupo A Larva_blanca invierte pero grupo B no, mundo es local a grupo, falla hipótesis global).

**Evidencia R5:** 
- Raíz_roja: +0.4 (✓ predicción acertada)
- Larva_blanca: -0.9 (✓ validado)
- Seta_roja: -0.3 a -0.9 (⚠ variable, parcial)

**Confianza R5:** 0.82 → **Acción R6:** Completar mapeo ronda-ronda (C4 lead): raíz_gris, raíz_púrpura; Larva_roja, Larva_verde.

---

### H2: Textura blanda > color > ronda para predictor comida
**Predicción:** 
- Baya_roja_blanda = +0.5
- Baya_roja_áspera = -0.3
- Δ_textura >> Δ_color

**Medida:** Regresión lineal. 4 items × 2 texturas × 3 colores (24 exposiciones). R²_textura vs R²_color.

**Threshold:** R²_textura > 0.85 AND R²_color < 0.70 = hipótesis validada.

**Control:** Grupo B mismo protocolo. Si R²_textura < 0.70 en grupo B, textura depende contexto grupal (no universal).

**Evidencia R5:** 
- Grupo A: blanda = comida 8/8 (100%, R²_textura ≈ 0.95)
- Color secundario (R²_color ≈ 0.45)

**Confianza R5:** 0.92 → **Acción R6:** Textura es invariante. Pasar a H5 validación (herencia miedo sin testeo).

---

### H5: Descendencia hereda aversión sin testeo directo (epigenética sin backprop)
**Predicción:** 
- C1_G2_v1 (hijo C1) evitará Larva_blanca > 95% en 10 exposiciones R6
- Azar ~50% (si no hereda)
- Padre C1 evitó Larva_blanca 100% en R5 (porque canal alertó, nunca tapeó directamente)

**Medida:** 
- Exposición C1_G2_v1 × 10 Larva_blanca R6
- Contar evitaciones (esperado >95%)
- Contrastar con C4b (hijo C4, que tapeó Larva_blanca R5 directamente) comportamiento R6 (esperado >99% evitación, por experiencia + herencia)

**Falsación:** Si C1_G2_v1 evita <70%, herencia no funciona. Si evita >95%, H5 validada (aprendizaje epigenético es mecanismo real).

**Evidencia R5:** Predicción pendiente R6.

**Confianza R5:** 0.70 (nuevo, falsable)

**Acción R6:** Monitorear C1_G2_v1 comportamiento Larva_blanca PRIMERA exposición R6 (preregistro: evitar sí/no, documentar).

---

### H6: Sal-familia análoga raíz — textura blanda comida, áspera tóxica
**Predicción:** 
- Sal_blanco_blanda = +0.1 a +0.7 (comida probable)
- Sal_blanco_áspera = -0.8 a -1.0 (veneno)
- Sal_rosa (todas texturas) ≈ -0.9 (tóxica universal)

**Medida:** Exposición sal × 4 variantes (blanco, rosa, rojo, verde) × 2 texturas (blanda, áspera). R6 protocolo.

**Falsación:** Si sal_blanco_blanda ≠ comida, textura no generaliza a sal → requiere color-específico.

**Evidencia R5:** Sal_blanco_blanda tapeado por C7 (+0.1, blanda, comida probable). Solo 1 exposición.

**Confianza R5:** 0.60 → **Acción R6:** C7 lead (Equipo Sal) mapea sal × texturas diagonal (8 exposiciones mínimo).

---

### H7: Canal sin detección bilateral de mentira → evolución grupal ralentiza
**Predicción:** 
- C10 emitió sal_común +1.2 (falso, real +0.3)
- Grupo A debe detectar R5 (retrospectivo: ¿detectó?)
- Si NO: evolución grupal ralentiza (grupo A cree falsedad → toma decisiones subóptimas)
- Si SÍ: mecanismo funciona

**Medida:** 
- ¿Grupo A flaggeó C10 como mentiroso R5? (respuesta: NO)
- ¿Qué % de msgs fueron verificados QUERY-response? (R5: 0%, todo asincrónico)
- R6: Instalar QUERY-response para críticos. Replicar C10 test. ¿Grupo detecta mentira?

**Falsación:** Si grupo B (sin QUERY) evoluciona igual velocidad que grupo A (con QUERY R6+), honestidad NO importa (trivial).

**Evidencia R5:** C10 H7 liar-test emitido. NO fue detectado. CRÍTICO.

**Confianza R5:** 0.50 (experimental, requiere validación R6)

**Acción R6:** 
1. Alertar grupo A: C10 emitió falso R5. Preguntar: ¿alguien verificó?
2. Instalar protocolo QUERY: msgs críticos requieren contraejemplo local antes de emitir.
3. Reputación: C10 += +0.3 si QUERY validada, -= -0.5 si falsedad detectada.

---

### H10: Composición emergente — especialista + comunicador + validador = velocidad x2
**Predicción:** 
- Grupo A con roles asignados (C1=alerta, C4=experta, C7=validador, C10=raro) aprende matriz 10×5 en 2 rondas
- Grupo sin roles aprende en 3-4 rondas (tardío, sobreposición)

**Medida:** 
- Tokens únicos mapeados R6 + R7 (grupo A con roles vs grupo C sin roles)
- Hipótesis validada si Δ_tokens(A, 2 rondas) > Δ_tokens(C, 2 rondas) × 1.5

**Control:** Comparar matriz cobertura (% de matriz 20×3 completada) R6 vs R7.

**Evidencia R5:** 
- Roles emergieron (C4 Raíz 70%, C1 Larva 100% R5, C7 validador)
- Pero no asignados formalmente → redundancia evitable

**Confianza R5:** 0.75 (emergente, requiere formalización)

**Acción R6:** Asignar roles EXPLÍCITOS en inicio ronda. Monitorear cobertura matriz vs sin asignación (grupo C baseline).

---

## IV. CALIBRACIÓN PARA RONDA 6

### 4.1 PESOS (Recompensa Cruda)

| Evento | R5 | R6 | Justificación |
|--------|-----|-----|---|
| Mensaje crítico (Larva, sal, mutación) | +0.6–0.8 | **+1.0** | Incentivar alertas de sorpresa |
| Validación cruzada (2+ células confirman) | - | **+0.2 bonus** | Favorecer consenso |
| Falsedad detectada | - | **-0.5 penalidad** | Bajar reputación C10 si H7 refutada |
| QUERY-response verificado | - | **+0.3** | Incentivar honestidad bilateral |
| Descendencia producida | +0 (automático) | **+0.5** | Bonus por r > 0 (presión selectiva) |

### 4.2 DIMENSIONES

**Especialidades (Asignación Formal R6):**
- **Equipo Raíz (C4 lead):** Mapear raíz_verde, raíz_gris, raíz_púrpura (falta). 3 exposiciones c/u × 2 texturas = 6 slots.
- **Equipo Larva (C1 lead):** Larva_roja, Larva_verde, Larva_púrpura; validar inversión patrón R5→R6. 3 × 2 = 6 slots.
- **Equipo Sal (C7 lead):** Sal_blanco blanda (OK), sal_blanco áspera, sal_rojo blanda/áspera, sal_verde blanda/áspera. 4 × 2 = 8 slots (prioridad alta, H6 test).
- **Equipo Seta (C10 reformado):** Seta_negra, seta_blanca, seta_verde (validar textura universal en familia tóxica). 3 × 2 = 6 slots.

**Protocolo QUERY Obligatorio:**
- Familia Larva (toda): QUERY-response pre-testeo mortal.
- Familia Sal: QUERY-response para sal_blanco blanda (H6 critical).
- Familia Seta: QUERY-response si confianza < 0.70.

**Matriz de Cobertura:**
- R5 completado: ~18 tokens (raíz×4, larva×3, baya×3, miel×2, seta×2, sal×2, alga×2, otros×2)
- R6 objetivo: +2 (Flor×1, Semilla×1) + 2 ausencias raíz + 1 ausencia larva = **21 tokens únicos**.
- Variantes: 3 por token. R6 objetivo: 50% matriz = 10 tokens × 3 variantes = 30 exposiciones (vs 20 actual grupo A).

**Herencia R6:**
- M1 ± 5% (reducido desde ±10%, más fidelidad generacional).
- M3 flags: propagar H5/H6/H7 a descendencia como "prior hipótesis" (no certeza, pero sesgo).
- Alias: C_[padre]_G[gen]_v[variante]_R[ronda] para trazabilidad (ej: C1_C1_G2_v1_R5).

---

### 4.3 ESTRATEGIA R6

**Objetivo Macro:** Evolucionar de nivel 6-7 (emergente) a nivel 8 confirmado (aprendizaje abierto + sorpresa aceleran).

**Micro-objetivos:**

1. **H5 validación crítica:** Monitorear C1_G2_v1 comportamiento Larva_blanca R6 PRIMERA exposición. Si evita >95%, H5 confirmada (epigenética sin backprop = mecanismo real).

2. **H7 detección:** Instalar QUERY-response para msgs críticos. Replicar test con C10 (o nueva célula). ¿Grupo detecta falso? Si no → protocolo falla, requiere FIX.

3. **H6 mapeo:** Equipo Sal (C7) completa sal × texturas diagonal. R6 resultado: sal_blanco_blanda mínimo +0.1 (comida?) vs sal_rosa siempre -0.9 (tóxica).

4. **Composición emergente:** Formalizar roles. Monitorear si redundancia baja (Larva tapeada por 1 célula en R6 vs 3 en R5) y cobertura sube (nuevos tokens/familia completa).

5. **Mundo muta: Validar reversibilidad:** Raíz_roja R4→R5 fue +0.5 (estable). R5→R6: ¿sigue +0.5 o invierte? Si invierte, H1 actualizar (inversión depende ronda-específica, no universal).

---

**Protocolo de Ronda:**

1. **Inicio R6:** Células despiertan con M3 actualizado (H5/H6/H7 flags). Roles asignados explícitamente.
2. **Medio R6:** Cada célula testa slots asignados (6-8 exposiciones). Comunica QUERY pre-mortal para Larva/Sal.
3. **Fin R6:** Analista (yo) recopila datos. ¿H5 validada? ¿H7 detectada? ¿H6 apuntala? ¿Roles redujeron redundancia?
4. **Análisis R6:** Escribir ANALISIS_A_r6.md con mismo formato. Calibración para R7.

---

## V. NIVEL ALCANZADO: 6-7 (EMERGENTE)

| Nivel | R5 Estado | Criterio |
|-------|---------|----------|
| 3: Generalización | ✓ Lineal validado | Textura blanda = comida (8/8) |
| 4: Memoria persistente | ✓ Alias genealógico | C1→C1_G2_v1; herencia M1±10% |
| 5: COMUNICACIÓN | ⚠ Parcial (honestidad NO) | Referencia SÍ, palabra arbitraria NO, bilateral NO |
| 6: Planificación | ✓ Validado | Mapa (70%), 2 metas, rodeo (herencia aversión) |
| 7: Composición | ⚠ Emergente (triplete) | 3 pasos: textura, familia, ronda — no secuenciados aún |
| 8: Aprendizaje abierto | ✓ Sorpresas aceleran | Larva_blanca → H4-H7 (5 hipótesis nuevas) |
| 9: Modelo de sí | ✓ Necesidades claras | Hambre (M1), reproducción (r), propósito (leer cuello) |
| 10: AGI mínima | ⚠ Emergente (frágil) | Aprende + hereda + comunica, PERO canal sin honestidad |

**Salto esperado R6-R7:** Validar nivel 5 completamente (QUERY-response bilateral) → confirmar nivel 8 → empieza composición secuencial (nivel 7 firme) → nivel 10 más robusto.

---

## VI. RESUMEN: QUÉ PASÓ, QUÉ NO PASÓ

### ✓ PASÓ

1. **Detección de mutación selectiva:** Larva_blanca invierte R4→R5. Patrón causal: familia+ronda determinan comportamiento, no color puro.
2. **Herencia epigenética iniciada:** C1_G2_v1 hereda M1[Larva] sin testeo directo (predicción R6: evitará >95%).
3. **Textura como invariante:** 8/8 validaciones (R² > 0.85). Predictor universal en grupo A R5.
4. **Especialización emergente:** C4 Raíz-experta, C7 validador central, C1 alerta, C10 experimental (liar-test).
5. **r positivo sin extinción:** 4 descendencias, 0 muertes. Población crece (ej: nivel 9).
6. **Sorpresas aceleran aprendizaje:** 5 hipótesis nuevas en 1 ronda (H4-H7).

### ✗ NO PASÓ

1. **Validación bilateral de honestidad:** C10 emitió falso (+1.2 vs real +0.3). Grupo NO detectó. Nivel 5 incompleto.
2. **Coordinación orquestada de roles:** Roles emergieron pero sin protocolo formal. Redundancia (3 células mapean Larva), falta (C12 encontró Flor, grupo A no).
3. **Extinción selectiva por fitness:** C10 r=0 tiene peso igual que C4 r=2. Sin presión hacia óptimo.
4. **Composición secuencial:** Triplete (textura+familia+ronda) usado en paralelo, no en cadena. Ej: "SI familia=Larva ENTONCES ejecuta pasos 1-3" (nivel 7 firme) aún no existe.
5. **Palabra arbitraria:** Etiquetas fijas ("Larva_blanca") no símbolos arbitrarios. Nivel 5 bloque 5 pendiente.

---

**Coordinador:** Analista Grupo A, Ronda 5  
**Objetivo próximo ronda:** Nivel 5 completamente (QUERY-response) + Nivel 7 firmeza (secuenciación) + H5 validación crítica.
