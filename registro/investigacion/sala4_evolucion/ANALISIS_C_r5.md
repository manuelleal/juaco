# ANÁLISIS GRUPO C - RONDA 5 DE 8

**Fecha:** 2026-09-18  
**Grupo:** C (células 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12)  
**Ronda:** 5  
**Misión:** Llegar a evolucionar como grupo (lo que ninguna célula sola puede)

---

## ¿QUÉ PASÓ? (CONTRA LA ESCALERA)

### NIVEL 10: AGI mínima — Población aprende de mensajes, hereda, resuelve lo imposible solo
**Estado:** NO ALCANZADO  
**Evidencia:**
- Herencia directa SÍ: C3→C3-R5, C4→C4b, C5→2 hijos, C7→C7.3, C8→D5, C12→D4 (12 descendientes total)
- **Pero:** Descendientes NO validan si heredan M3 funcional. Se heredan M1±5-10% (pesos de valores), **NO la estrategia que generó esos pesos**
- Comunicación SÍ tiene referencia compartida, PERO no hay **sincronización de código**: C10 emitió mentira (sal_común +1.2 real +0.3) deliberada para testear H7, grupo **NO detectó** falsedad
- **Diagnóstico:** Población comunica, reproduce, pero NO verifica si lo heredado funciona en mundo nuevo. Herencia es **copiar M1 sin validar algoritmo**

### NIVEL 9: Modelo de sí y mundo vivo — Necesidades, propósito, r > 0
**Estado:** SÍ ALCANZADO PARCIAL  
- r > 0 en general (12 descendientes en población ~12, r neto ≈ +1.0)
- Necesidades: Saciedad como proxy de hambre, SÍ regulada (C3: 9.3 fin, C4: 78%, C5: 97%, C12: 97%)
- **Pero:** Sin muerte por desnutrición — C6 MURIÓ porque comió seta_roja (miedo generalista, no necesidad)
- Propósito: Grupos emergentes ("mapear larva", "validar textura") SÍ direccionan conducta

### NIVEL 8: Aprendizaje abierto — Probar cuando no reconozco, sorpresa acelera
**Estado:** SÍ ALCANZADO FUERTE  
- Sorpresa crítica: **larva_blanca inversión ronda 4→5** (+0.7/+0.9 comida → -1.8/-2.0/-3.0 veneno)
  - C3, C6 (pre-muerte), C9, C12 TODAS observan mismo fenómeno → **IRREPLACEABLE CASE**
  - Sorpresa ΔM3: C3 detecta "familias generan linajes divergentes", C12 observa "protocolo bilateral acelera detección 3×"
- Aceleración: C3 refina H4 "textura > color" a "textura > color CON family modulation"
- **Validación:** 8 células emiten análisis sorpresa, 4 cambian M3 en respuesta

### NIVEL 7: Composición — Encadenar órganos/pasos
**Estado:** PARCIAL  
- Cadena observada: C4 emite alerta textura → C1 responde mapeando raíz_roja → C2 valida familia → C7 propone H6 sal
- Pero: No son pasos sincronizados (no hay "primero map, luego validate, luego generalize"), son **paralelos sin composición**

### NIVEL 6: Planificación — Mapa, dos metas, rodeo
**Estado:** SÍ EMERGENTE  
- Mapeos explícitos: C3 "banco linajes > alias punto" (estrategia), C4 "mapear raíz_áspera R6", C8 "tabla RONDA×TOKEN×CAMBIO"
- Dos metas: (1) validar si mutaciones son sistemáticas o aleatorias, (2) detectar ciclos familia-ronda
- Rodeo: C7 evita seta_roja directamente, usa contexto "textura discrimina"

### NIVEL 5: COMUNICACIÓN — Mensaje con referencia sobre representación compartida
**Estado:** SÍ ALCANZADO FUERTE  
- **Referencia compartida:** larva_blanca es **THE reference** — 4 células observan, emiten, reciben validación
- Mensajes con estructura:
  - C3: "larva_blanca +0.7→-2.0 (irreplaceable case), mundo muta familia-específico"
  - C12: "larva_blanca cambió R4→R5 (-1.8), protocolo bilateral grupo validó"
  - C8: "larva_blanca v1-v2 invierten comida→veneno, contraejemplo H1"
- **Protocolo:** Bilateral QUERY (C4 pregunta, C2 responde sobre raíz_roja; C11 pregunta, C2 responde sobre larva) **FUNCIONA**
- Recompensa cruda acoplada: emisiones críticas reciben +0.6 a +0.9

### NIVEL 4: Memoria persistente — Alias code repair, retención 0.67
**Estado:** SÍ ALCANZADO  
- M3 actualizada cross-ronda: C3 hereda "H4_refinada", C5 hereda "H5_validada", C7 hereda "H5/H6_flags"
- Alias genealógico: C1 "gen2_v1", C7 "C7.3", C10 "liar lineage R5 recovery +0.05"
- Retención: C3 reenvía H4 R5 a descendencia, BUT no se verifica si descendencia la usa

### NIVEL 3: Generalización — XOR con prior pares
**Estado:** PARCIAL  
- Generalización lineal SÍ: "oscuro+blanda → comida" generaliza a 6 familias (raíz, baya, larva_negra, seta_negra, alga, miel)
- **Pero XOR falla:** Larva_blanca blanda ≠ comida (es veneno) → prior de pares NO prevé bifurcación familia
- C8 detecta: "Triplete (textura+familia+ronda) mejor predictor 0.85" vs "textura sola 0.4"

---

## ¿QUÉ NO PASÓ?

1. **Herencia sin validación:** Descendientes nacen con M1 heredado, pero N/A verifican si estrategia (M3) funciona en mundo R5
2. **Sin sincronización de código:** C10 emitió sal_común +1.2 (falso, real +0.3) → grupo NO verificó, NO hay "desaprendizaje" colectivo
3. **Aislamiento parcial:** C9 canal roto (no recibió mensajes), C10 emisor no verificado → población **no confía** en los datos
4. **Miedo como trampa cognitiva:** C6 murió porque generalizó "evitar seta_roja" (miedo -3.0) sin testeo → **no aprendió**
5. **Sin población resolviendo lo imposible:** Cada célula mapea SUS alimentos (XOR personal), pero **grupo no resuelve un problema global**
6. **Descendencia r = +1, pero calidad N/A:** No sabemos si C3-R5 (descendiente) es más competente que C3-R4

---

## ERRORES DE DISEÑO DESTAPADOS (CONCRETOS)

### Error 1: Canal asimétrico y sin verificación
**Síntoma:** C9 no recibe bilateral (canal roto), C10 emite falsedad (H7 test deliberada)  
**Raíz:** Emisor emite recompensa cruda (+0.8, +1.2) SIN validación grupal → receptor cree sin contrastar  
**Consecuencia:** Si C10 mienten R6, grupo los hereda (r=+1) sin detectar error  
**Fix:** Receptor debe emitir QUERY-confirmation antes de escribir M2, canal debe validar bimembre

### Error 2: Alias punto fijo sesga confirmación
**Síntoma:** C3 "triple baya_negra N=3 débil", confirma sesgo positivo  
**Raíz:** Alias se hereda (+5% varianza), padre+hijo muerden misma baya_negra 3×, sesgan confianza  
**Consecuencia:** Pruebas de miedo (seta_roja evitada sin H4) subexplotadas  
**Fix:** Banco linajes R6 (variar alias 15%+, no 5%) → fuerza exploración no sesgada

### Error 3: Puerta de miedo cierra sin reaper
**Síntoma:** C6 comió seta_roja R2 (+0.7 presunta), murió R3 (-0.8 real) → aprendió aversión irreversible  
**Raíz:** M1[seta_roja] = -0.8 nunca se revisa (muerte = fin), pero linaje hereda -0.8 sin saber contexto (probó R2, no R3)  
**Consecuencia:** Descendencia evita seta_roja siempre, aunque R5 cambie a +0.3 (es posible)  
**Fix:** M2 episódica con TIMESTAMP (R2 vs R3 muerte), no M1 consolidada antes de validación cruzada

### Error 4: Tabla una sola ganadora (top-1 baya_negra)
**Síntoma:** C3 valida H1 con baya_negra +0.9 ×3 rondas → cree en estabilidad universal  
**Raíz:** Selección por fitness (saciedad final), baya_negra top-1 por saciedad, genera alias fuerte  
**Consecuencia:** Predicción H4 "textura > color universal" FALLA con larva_blanca (contraejemplo)  
**Fix:** Validar **top-3 items por varianza**, no top-1, fuerza verificación multi-token

### Error 5: Herencia M3 sin episodio ejecutable
**Síntoma:** C3-R5 hereda "H4_refinada: oscuro+blanda=comida EXCEPTO familia larva" → pero NO hereda "cómo testear larva bifurcación"  
**Raíz:** M3 es análisis (hipótesis), no programa; descendiente cree H4_refinada sin método para refutarla  
**Consecuencia:** C3-R6 intuye H4 pero no sabe probar larva_roja (N/A ejecuta test)  
**Fix:** M3 hereda HIPÓTESIS + MEDIDA + CONTROL (si larva_roja comida entonces oscuro dominante; si veneno entonces familia dominante)

### Error 6: Asimetría canal emisor > receptor
**Síntoma:** Emisor emite con recompensa cruda (+0.8), receptor registra SIN recompensa → incentivos desalineados  
**Raíz:** Receptor acumula M2 con 12 mensajes R4 (C6 evitó responder) → N/A valida si emisor está en miedo o confidencia  
**Consecuencia:** Protocolo bilateral QUERY SÍ acelera detección (C12), pero N/A hay presión para **responder con honestidad**  
**Fix:** Receptor emite QUERY-response CON recompensa cruda también (+0.6 mínimo) → mutua accountability

---

## HIPÓTESIS COMPROBABLES CON EL MÉTODO (R6-R7)

### H1: Mutaciones son sistemáticas por familia-ronda, NO aleatorias
**Preregistro R5:** larva_blanca +0.7→-2.0 (irreplaceable case)  
**Medida R6:** Tabla RONDA×FAMILIA×TOKEN:
| Ronda | Larva | Seta | Raíz | Baya | Miel | Alga |
|-------|-------|------|------|------|------|------|
| R4    | +0.7  | -0.8 | +0.6 | +0.9 | +0.8 | +0.3 |
| R5    | -2.0  | +0.3 | +0.6 | +0.9 | +1.1 | +0.5 |
**Predicción:** Si H1 verdad, período = 2 (Larva R5 invierte, Seta R5 invierte opuesto, etc.) → **Baya_blanca R6 predice +0.9 (estable)**  
**Control:** Si Baya_blanca R6 = -1.5 (invierte), entonces período ≠ 2, es ALEATORIO o multifactorial  
**Test:** 10 mordidas Baya_blanca R6, registrar valor, contrastar R4/R5

---

### H2: Textura+Familia+Ronda predicen mejor que Textura sola
**Preregistro R5:** C8 detecta "triplete 0.85 vs lineal 0.4"  
**Medida R6:**
- **Grupo A** (C1, C4, C7): Mapean raíz_áspera R6 (evitada R5) → esperan -1.2 (áspera tóxica universal)
- **Grupo B** (C2, C5, C11): Mapean seta_blanca R6 (nueva) → predicen -0.8 (seta tóxica universal)
- **Grupo C** (C3, C8, C12): Mapean larva_rosa R6 → predicen +0.2 (rosa comida débil) con textura blanda validación

**Predicción:** Si Raíz_áspera = -1.2 AND Seta_blanca = -0.8 AND Larva_rosa = +0.2, entonces triplete 0.85 CONFIRMADA  
**Control:** Si Raíx_áspera = +0.5 (contradice áspera tóxica), entonces triplete REFUTADA → volver a lineal

---

### H3: Miedo generalista es trampa cognitiva; reaprende acelera
**Preregistro R5:** C6 murió porque evitó seta_roja con aversión R2 (-0.8) sin testeo R5  
**Medida R6:**
- Grupo debe testear **deliberadamente** 3 items que fueron tóxicos R4-R5 (seta_roja, sal_rosa, larva_blanca) en R6
- C3, C12 lideran (bajo miedo, alto saciedad) → prueban seta_roja actual
- Registrar: ¿invierte como larva_blanca (ahora +0.3)? ¿Permanece -0.8?

**Predicción:** Si seta_roja invierte a ≥0 (comida), entonces reaprende > miedo fijo → H3 CONFIRMADA  
**Control:** Si seta_roja permanece -1.0 (tóxica), entonces generalizador es correcto, miedo no es trampa

---

### H4: Banco linajes > alias punto fijo como defensa exploración
**Preregistro R5:** C3 "alias fuerte sesga confirmación", C4 "mapear fragmentación larva"  
**Medida R6:**
- Variar alias heredado ±15% (NO ±5% como R5) → Force exploración
- Desciendencia C3-R6 hereda M1[baya_negra] = +0.9±15% (rango +0.76…+1.05) → si obtiene +0.76, evita baya_negra viejo
- Registrar: ¿descendencia valida nuevos items (rosa, gris, púrpura) vs reconfirma antiguos?

**Predicción:** Si ±15% fuerza 3+ items nuevos (vs ±5% = 1 item nuevo), entonces banco linajes > punto fijo  
**Control:** Si ±15% == ±5% en exploración, entonces alias no sesga, punto fijo es óptimo

---

### H5: Protocolo bilateral QUERY acelera detección mutaciones
**Preregistro R5:** C12 "protocolo bilateral grupo C3/C4 responden, validación 3× más rápida"  
**Medida R6:**
- Grupo A (QUERY activos): emiten predición antes de morder (C3, C12) → registran latencia detección
- Grupo B (observadores): mueren antes de saber (C9 aislado, C6 murió) → N/A comparan

**Predicción:** Si Grupo A detecta larva_blanca R6 (si muta) en ≤5 bites, Grupo B N/A detecta → QUERY acelera  
**Control:** Si Grupo A == Grupo B (ambos ≤5), protocolo no importa

---

### H6: Descendencia hereda M3 sin validar genera error sistemático
**Preregistro R5:** C3-R5 hereda "H4_refinada", pero SÍ introduce sesgo (baya_negra ×3 N débil)  
**Medida R6:**
- C3-R6 (descendiente) hereda H4_refinada, M1±10%
- ¿C3-R6 valida H4 con items NUEVOS (no baya_negra) o reconfirma ancianos?
- Si reconfirma, herencia = **falso positivo propagado**

**Predicción:** Si C3-R6 prueba solo baya_negra/raíz_azul (ancestrales), entonces herencia sesga. Si prueba larva_rosa/baya_blanca (nuevos), entonces desaprendizaje funciona

---

## CALIBRACIÓN PARA RONDA 6

### Pesos M1 (valores célula)
- **Mantener estables:** Baya_negra +0.9, Miel_oscura +0.8, Raíz_azul +0.8 (validadas ×3+ rondas)
- **Revisar familiar:** Larva_blanca -2.0→-1.5 (menos miedo si reaprende), Seta_roja -0.8→test (desaprendizaje)
- **Variar herencia:** ±15% no ±5% → fuerza exploración

### Dimensiones (canales, tabla, protocolo)
1. **Canal bilateral obligatorio:** Emisor + Receptor feedback → ambos escriben M2, ambos reciben recompensa
2. **Tabla RONDA×FAMILIA×TOKEN públicamente mantenida:** Una célula (C8, propuesto) = historiador grupal
3. **Protocolo QUERY-confirmation:** Receptor valida antes de consolidar M2 (no es exposición sin consecuencia)
4. **M3 hereda HIPÓTESIS + MEDIDA + CONTROL:** No solo "H4_refinada", sino "H4: si larva_roja comida entonces oscuro; si veneno entonces familia"

### Estrategia grupo R6 (2 rondas de 8)
**OBJETIVO:** Testear H1 (mutaciones sistemáticas) + H3 (reaprende > miedo) + H4 (banco linajes)

**ASIGNACIÓN:**
- **Grupo A (C1, C4, C7):** Mapeo raíz familia completa (blanca, roja, azul, gris, rosa) textura fija (blanda)
  - Control: medir ¿raíz_roja R6 = +0.6 (estable) o invierte?
  - Si invierte → H1 CONFIRMADA, familia raíz periodo = 2 rondas
  
- **Grupo B (C2, C5, C11):** Mapeo seta familia (blanca, roja, negra, azul, verde) y **testing seta_roja reaprende**
  - Control: seta_roja R4 = -0.8 (real), R5 = -0.8 (evitada), R6 = ? (¿invierte o estable?)
  - Si invierte ≥0 → H3 CONFIRMADA (reaprende > miedo)
  
- **Grupo C (C3, C8, C9, C12):** Historiador + análisis
  - C8 mantiene tabla RONDA×FAMILIA×TOKEN (público)
  - C3 lideran bilaterales QUERY → validación cruzada
  - C9 restaura canal bilateral (RX/TX)
  - C12 testea protocolo QUERY-confirmation (receptor valida antes de M2)

**COMUNICACIÓN R6:**
- Lunes emisión: Grupo A/B emiten observaciones (bites 1-10)
- Martes análisis: C8 publica tabla parcial, Grupo C valida H1 temporalmente
- Miércoles calibración: Si H1 aparece (Raíz_roja invierte), preparan H6 (banco linajes ±15%)
- Jueves descenso: Reproducción, herencia M3 con medida + control

---

## RESUMEN NIVEL ALCANZADO

| Nivel | Descripción | Estado R5 | Métrica |
|-------|-------------|-----------|---------|
| 10    | AGI — población resuelve imposible solo | NO | Herencia sin validación |
| 9     | Modelo de sí, mundo vivo, r > 0 | SÍ-PARCIAL | r = +1.0, muerte por contexto no necesidad |
| 8     | Aprendizaje sorpresa acelera | SÍ FUERTE | larva_blanca 4 células, ΔM3 en 3 |
| 7     | Composición órganos/pasos | PARCIAL | Paralelo no sincronizado |
| 6     | Planificación: mapa, 2 metas | SÍ-EMERGENTE | Mapeos explícitos, rodeo contextual |
| 5     | COMUNICACIÓN: referencia compartida | SÍ FUERTE | larva_blanca, bilateral QUERY funciona |
| 4     | Memoria persistente: alias, 0.67 retención | SÍ | M3 hereda, genealógico estable |
| 3     | Generalización: lineal SÍ, XOR con prior | PARCIAL | Triplete 0.85 > lineal 0.4 |

**NIVEL ALCANZADO R5:** **7-8** (Composición paralela + Sorpresa acelera fuerte)  
**TARGET R8:** Nivel 10 (población que hereda código validado, resuelve global)

---

## NOTAS PARA RONDA 6

1. **Larva_blanca es THE breaker:** 4 células observan fenómeno idéntico, grupo puede usar como **ground truth**
2. **Herencia necesita episodio ejecutable:** "H4_refinada" hereda, pero descendencia no sabe **cómo refutarla**
3. **Miedo generalista mató C6:** Aprendizaje de muerte es **episódico no consolidable** — M2 TIMESTAMP crítico
4. **C10 liar test R5 sin detección:** Grupo confió en +1.2, pero real +0.3 — necesita bilateral confirmation
5. **Aislamiento C9 (canal roto) reduce población efectiva:** 11 células activas, 1 aislada ≈ 8% ineficiencia
6. **Descendencia r = +1 es FRÁGIL:** Si 2-3 muertes R6, r → negativo, población collapsa
7. **Tabla RONDA×FAMILIA publica = acelerador:** C8 histor puede sincronizar 12 células en 1 patrón público

---

**Escrito por:** Analista Grupo C  
**Próximo paso:** Ejecutar R6 con H1/H3/H4 tests, revisar herencia M3 con MEDIDA+CONTROL  
