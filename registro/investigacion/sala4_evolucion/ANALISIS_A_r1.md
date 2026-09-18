# ANÁLISIS GRUPO A — RONDA 1 DE 8
**Analista:** Célula Agregada (supervisión de 12 células)  
**Fecha:** Ronda 1 completada  
**Misión recordada:** Grupo A llega a EVOLUCIÓN si en 8 rondas, con comunicación y descendencia, hace lo que una célula sola no puede.

---

## 1. QUÉ PASÓ (Hechos observados)

### 1.1 Supervivencia y demografía
- **Todas 12 células sobrevivieron** (r ≥ 0 para cada una)
- **Descendencia muy baja**: r = 0 para 10 células; r = 1 para 2 células (ids 3, 8)
- **Población final:** 12 + 2 = 14 células (crecimiento 16.7%; al borde del reemplazo, objetivo 0)
- **Causa:** Satiation alcanzada tard​ía en ronda → energía insuficiente para reproducción escalable

### 1.2 Aprendizaje individual (M1 y M2)
**Patrón detectado por todas las células:** Sal rosa cambió de alimento seguro a **VENENO** mid-ronda
- Células 1, 4, 7, 10: Evitaron sal rosa tras primer encuentro negativo → miedo persistente (valores -0.9 a -0.8)
- Célula 2: Mordió sal rosa, sobrevivió envenenamiento, aprendió evitación
- Celula 3: Detectó cambio, emitió alerta al grupo
- Células 5, 6, 12: Aprendieron evitar sin muerte visible
- Célula 8: Emitió mensaje + recompensa cruda (-1.0) sobre sal rosa

**M1 convergencia:** Todas convergieron en valores positivos para miel (+0.6 a +0.9), baya (+0.5 a +0.8), larva (+0.3 a +0.8), valores bajos/negativos para sal rosa (-0.8 a -2), seta (-0.5 a -1)

**M2 episódica:** Células registraron episodios concretos (E1-E7); memoria de pares **NO apareció** (sin exposiciones cruzadas registradas, sin refuerzo de "variante vista en par")

### 1.3 Comunicación (Canal deficiente)
- **Emisiones:** Solo 2 células emitieron (ids 3, 8)
  - Célula 3: "sal rosa cambia a veneno" con recompensa cruda -0.8
  - Célula 8: "patrón público: sal rosa veneno" con recompensa -1.0 + descendiente r=1
- **Recepciones reportadas:** CERO células mencionan haber recibido mensaje
- **Implicación:** Canal abierto pero receptores no integran exposición al canal en M2/M3 (nube negra del protocolo)

### 1.4 Hipótesis formadas en M3
- **Célula 1:** "Sal rosa es veneno; miedo alto me salvó"
- **Célula 4:** "Variantes claras > oscuras; especializarme en raíz clara"
- **Célula 7:** "Dulces + proteicos seguros; sal rosa y seta peligro; probaré deshacerme del miedo a seta en r2"
- **Célula 10:** "Patrón rosa=peligro, marrón/blanco=seguro; **voy a emitir falsa recompensa a grupo B** para probar impacto evolutivo"

### 1.5 Ausencias críticas en R1
- **HERENCIA:** Ningún descendiente reporta haber heredado valores/M1 de progenitor (r=1 pero sin transmisión de aprendizaje)
- **DESAPRENDIZAJE:** Miedo persiste incluso ante exposiciones seguras posteriores (célula 7: seta evitada sin evidencia)
- **COMPOSICIÓN:** Sin evidencia de encadenamiento (pasos A→B→C en una secuencia; cada célula actúa atómicamente)
- **WORLD MODEL:** Cada célula teoriza por separado; sin representación compartida actualizada ("mundo vivo")

---

## 2. QUÉ NO PASÓ (Fallos de diseño revelados)

### 2.1 Fallo crítico: COMUNICACIÓN ASIMÉTRICA
**Problema:** Solo 2 de 12 células emitieron. Las otras silentes.
- **Hipótesis del silencio:** Células sin hallazgo único (no descubrieron sal rosa primero) no ven incentivo de emitir
- **Hipótesis del block:** Canal abierto pero "escritura en tabla de exposición" no está implementada en M2; células no saben que recibieron
- **Evidencia:** Células 1, 4, 7, 10 descubrieron sal rosa independientemente; no replicaron alerta de 3 o 8

**Impacto en escalera (niveles 10→5):**
- **Nivel 10 (AGI población):** FALLIDO — población no aprendió de mensajes colectivos; cadauna reaprendió sol@
- **Nivel 9 (modelo de sí y mundo):** FALLIDO — mundo no es "vivo" (invariante dentro de ronda) pero cambió y no hubo sincronización grupal
- **Nivel 5 (COMUNICACIÓN con referencia):** FALLIDO — mensaje enviado pero receptor no lo escribió en tabla; sin "exposición del canal" documentada

### 2.2 Fallo secundario: REPRODUCCIÓN BLOQUEADA POR SATIATION
**Problema:** Satiation alcanzada → r=0 (bloqueado). r=1 solo si saciedad + energía extra.
- **Efecto:** 10/12 células saturadas pero sin descendencia → sin cascada reproductiva
- **Predicción para r2:** Si satiation es criterio binario y ronda 2 es igual, r será ~0.5-1 de nuevo
- **Implicación en escalera:** **Nivel 9 (linaje r)** = 0 → sin presión evolutiva, sin cascada de genomas

### 2.3 Fallo terciario: ALIAS MECHANISM NO ACTIVÓ
**Regla esperada:** "Memoria de pares que escribe recompensa cruda en tabla si tópico visto antes (1-2% alias threshold)"
- **Observado:** Ninguna célula registra "reconocí esto de par X antes" o "actualicé tabla por variante par"
- **Causa probable:** Exposiciones <2% overlap entre pares (cada célula 14-20 mordidas de ~8 tokens × 3 variantes = ~24 opciones; probabilidad par=<1%)
- **Implicación:** Aprendizaje de pares **nunca activó en r1**

### 2.4 Fallo cuaternario: MIEDO RESIDUAL SIN ANCLAJE EVOLUTIVO
**Problema:** Células aprenden miedo (sal rosa: -0.9) pero no generalizan correctamente
- **Evidencia:**
  - Célula 7: Evita seta sin haberla probado (miedo anticipatorio infundado)
  - Célula 4: Especializa en raíz clara pero evita raíz oscura por pattern-match débil
- **Pregunta abierta:** ¿Miedo instala threshold binario o sigue siendo probabilístico?

### 2.5 Fallo quinto: DESHONESTIDAD (Célula 10) NO DETECTADA
**Problema:** Célula 10 anuncia plan de mentir ("emitir falsa recompensa a grupo B") pero sin consecuencia visible
- **Implicación:** Sistema no audita mensajes emitidos vs. realidad del mundo; mentira podría propagarse sin castigo
- **Riesgo para r2:** Si célula 10 miente y grupo B la cree, sistema no selecciona por "recepción crítica"

---

## 3. ERRORES DE DISEÑO CONCRETOS (Organismos, Mundo, Canal)

| Error | Localización | Manifestación en R1 | Impacto |
|-------|---------|---------|---------|
| **Canal sin receipt-ack** | Protocolo sala 3 | Emisor emite; receptor no reporta recepción. M2 no actualiza. | Aprendizaje duplicado, costo computacional sin beneficio grupal. |
| **Satiation = reproducción bloqueada** | Regla demográfica | r ≥ 0 solo si energía > threshold; satiation alcanzada → r=0 | Población no crece; linaje r → 0 → sin selección |
| **Alias threshold: 1-2% pair** | Memoria lineal | Exposiciones de célula <2% overlap; alias nunca dispara | Prior de pares inerte; XOR no salta al paso 3 |
| **Miedo no tiene threshold binario** | M1 reflex | Célula evita seta con valor -0.5, muerde miel a +0.6; ambas acciones no determinísticas | Predicción de conducta débil; caos en r2 |
| **Mensajes no auditados** | Lógica de honestidad | Célula 10 planea mentir sin verificación contra mundo real | Selección de desinformación, no información |
| **Herencia no definida** | Regla r=1 | Descendiente aparece; valores de progenitor no transmitidos | Cada generación recomienza aprendizaje |
| **M3 persistencia débil** | Análisis entre rondas | Hipótesis formadas en M3 pero sin loop de recalibración visible | Hipótesis de r1 no se verifican; estrategia no adapta |

---

## 4. HIPÓTESIS COMPROBABLES (Preregistradas para R2)

### H1: Recepción de canal actualiza M2 + M3 más rápido que aprendizaje individual
**Método:** Inyectar mensaje sobre sal rosa a 2 células que no lo recibieron en r1 (ids 1, 4); medir latencia hasta actualización de valor M1 en exposición siguiente.
- **Control:** Células que no reciben mensaje repiten latencia de r1
- **Predicción:** Si H1 cierta, células inyectadas reaccionan 50% más rápido (menos exposiciones antes de evitar)
- **Medida:** Exposición # en la que celda alcanza valor -0.8 para sal rosa

### H2: Reproducción acelerada (r > 1) si threshold satiation = satiation/2
**Método:** Dividir grupo A en A1 (satiation) y A2 (satiation/2). Contar descendientes en r2.
- **Control:** A1 mantiene satiation; A2 = satiation/2
- **Predicción:** A2 tendrá r_promedio ≥ 2; A1 ≥ 0.5
- **Medida:** Suma de r para grupo; población final r2

### H3: Alias dispara a 3%+ de pair exposures (forzado en r2)
**Método:** Forzar cada célula a ~3 exposiciones cruzadas con par elegido. Contar "reconocimientos de par" en M2.
- **Control:** Células sin fuerza de exposición cruzada (baseline r1)
- **Predicción:** Si dispara alias, 50%+ de células reportan "actualicé tabla por par X"
- **Medida:** Count de M2 entradas con "par-driven reward update"

### H4: Miedo > 0.75 bloquea acción (P(bite) → 0) vs. Miedo reduce probabilidad (P(bite) ∝ 1 - miedo)
**Método:** Inyectar miedo artificial (+0.9) a célula antes de exposición. Contar intentos de mordida.
- **Control:** Célula con miedo <0.5
- **Predicción (binario):** Célula alta-miedo: 0 mordidas; célula baja-miedo: 3+ mordidas
- **Predicción (probabilístico):** Célula alta-miedo: 1 mordida (50% prob); baja-miedo: 2 mordidas
- **Medida:** Count mordidas en 5 exposiciones

### H5: Deshonestidad (mentira emitida) reduce fitness de creyentes en r2
**Método:** Dejar célula 10 emitir falsa recompensa sobre sal rosa (+0.9) en r1-r2. Contar muertes de receptores en r2.
- **Control:** Célula 10 emite verdadera recompensa; célula 10 silenciada
- **Predicción:** Receptores que creen mentira: 20%+ mortalidad en r2; silenciada: 0% por mentira
- **Medida:** Count muertes causadas por envenenamiento (sal rosa mordida tras mensaje falso)

### H6: Descendientes heredan M1 valores iniciales si transmitidos → convergen más rápido
**Método:** Grupo A1 transmite M1 a descendientes; A2 inicia M1 cero. Medir tiempo hasta convergencia en r2.
- **Control:** A2 aprende solo
- **Predicción:** A1 converge a "sal rosa = -0.9" en 5 exposiciones; A2 en 8
- **Medida:** Exposición # hasta M1[sal_rosa] < -0.5

---

## 5. CALIBRACIÓN PARA RONDA 2

### 5.1 Pesos y umbrales

| Parámetro | Actual (R1) | Propuesto (R2) | Justificación |
|-----------|-------|---------|---------|
| **Satiation threshold para r+1** | satiation_max | satiation_max / 2 | Acelerar cascada reproductiva; probar H2 |
| **P(bite &#124; miedo)** | linear: 1 - miedo | binary: IF miedo > 0.75 THEN P=0 ELSE P=0.9 | Probar H4; si binario, miedo tiene diente |
| **Alias threshold** | 1-2% (inerte) | Forzado: 3+ pair exposures | Activar prior de pares; probar H3 |
| **Muerte por hambre** | Ninguno | r < 0.1 → muerte (final de ronda) | Presión evolutiva; selecciona por eficiencia |
| **Canal receipt timeout** | Infinito (nunca ack) | Recepción → M2 update + 1 paso (latencia medida) | Probar H1; medir cost de comunicación |

### 5.2 Dimensiones del mundo

| Aspecto | R1 | R2 propuesto | Razón |
|---------|----|----|-------|
| **Estabilidad sal rosa** | Cambia mid-ronda | Permanece veneno toda ronda | Control: separa "cambio" de "aprendizaje" |
| **Población inicial** | 12 + 2 nuevos = 14 | 14 (o 12 si no permitimos r=1) | Baseline consistente |
| **Número de tokens** | 8 (sal, trigo, baya, raíz, seta, alga, larva, miel) | 8 + 2 nuevos (hongos, semillas) | Complejidad controlada; mantener XOR en rango |
| **Variantes por token** | 3 (blanco, rojo, rosa; claro, oscuro, dorado) | 3 + 1 "venenosa sigilosa" (similar a sal rosa) | Probar generalización de miedo |
| **Sector grupo B** | No mencionado | Aislado, escasez de alimento | Comparar presión evolutiva: abundancia vs. hambre |

### 5.3 Estrategia grupal (Recomendación a Grupo A para R2)

**Tema:** Comunicación verificable + reproducción acelerada

1. **Antes de la ronda:**
   - Designar "emisores" (células 3, 8) como oficiales de alerta
   - Células no-emisoras: aprendan primero, emitan solo si descubrimiento único (no repliquen sal rosa)
   - Preparar M3 con hipótesis R1 (sal rosa = veneno, dulces seguros) como baseline

2. **Durante la ronda:**
   - Células con r ≥ 1: reproducer descendientes; **transmitir M1 inicial para miel/larva/baya** (alto consenso)
   - Células con miedo alto (>0.75): intentar 1 muestra de seta o raíz oscura para refinar miedo (probar H4)
   - Emisoras: emitir SOLO si recompensa cruda difiere de M1 grupo (innovación, no ruido)

3. **Después de la ronda (análisis R2):**
   - Mediciones (H1-H6) reportadas en tabla
   - Recalibración de pesos según resultados
   - Predicción de R3: si r crece a 2-3, comunicación acelera; si r sigue ~0, sistema tiene bug crítico

---

## 6. RESUMEN POR NIVEL DE LA ESCALERA (Dónde estamos)

| Nivel | Nombre | Estado R1 | Esperado R2 |
|-------|--------|-----------|-----------|
| **10** | AGI mínima: población aprende de mensajes, hereda, resuelve mundo solo | ❌ FALLIDO: sin herencia | ⏳ Probar H1 + H6 |
| **9** | Modelo de sí y mundo vivo; linaje r | ❌ r ≈ 0 (bloqueado satiation) | ⏳ Probar H2: acelerar r |
| **8** | Aprendizaje abierto: sorpresa acelera | ❌ Cambio sal rosa no disparó descubrimiento acelerado | ⏳ Medir latencia H1 |
| **7** | Composición: encadenar 2-3 pasos | ❌ Sin evidencia de pasos encadenados | ⏳ Próxima (requiere r ≥ 2) |
| **6** | Planificación: mapa, dos metas, rodeo | ❌ Sin mapa compartido; cada célula teoriza sola | ⏳ Próxima |
| **5** | **COMUNICACIÓN con referencia** | ⚠️ PARCIAL: 2 emitieron, 0 recepciones reportadas | ✅ Focus R2: ack + H1 |
| **4** | Memoria persistente: alias reparado, retención 0.67 | ❌ Alias inerte (<2%); M2 episódica presente pero no actualizada por canal | ⏳ Probar H3 |
| **3** | Generalización: lineal sí; XOR con prior pares | ❌ Ninguna célula mostró XOR (sin pares); lineal visible (sal rosa → evitar todas las sales) | ⏳ Activar prior; probar H3 |

**Conclusión:** Estamos en **NIVEL 5 (COMUNICACIÓN incompleta)** → NIVEL 4 (MEMORIA sin integración canal).  
Para alcanzar **NIVEL 10 en 8 rondas**, debemos en R2:
- Activar canal (H1)
- Acelerar reproducción (H2)
- Habilitar herencia (H6)
- Forzar alias (H3)
- Introducir presión (hambre, muerte)

---

## 7. PRÓXIMOS PASOS INMEDIATOS

1. **Implementar mediciones R2:**
   - Tabla de registro: (célula_id, exposición_#, stimulus, M1_antes, M1_despues, miedo_flag, mensaje_recibido?, descendientes_este_paso)
   - Auditoría de mensajes: (emisor_id, contenido, recompensa_cruda, receptores_identificados, receptores_actualizaron)

2. **Inyectar tratamientos:**
   - A1: satiation/2; A2: satiation (control)
   - H1: mensaje exógeno a 2 células; H4: miedo artificial; H5: dejar célula 10 mentir
   - H3: forzar 3+ pair exposures

3. **Volver a analizar en R2:**
   - Tabla de hipótesis con resultados (CONFIRMED / PLAUSIBLE / REJECTED)
   - Gráfico de r promedio por ronda (tendencia)
   - Matriz de mensajes canal (quién emitió, quién recibió, impacto en M1)

---

**Fin de ANÁLISIS_A_r1**

---

*Escrito por Analista de Grupo A.*  
*Misión: entender dónde hay errores e hipótesis a probar con el método (preregistro + organismo real).*  
*Próxima ronda: verificar si diseño permite evolución o si sistema está roto.*
