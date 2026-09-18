# ANÁLISIS GRUPO B — RONDA 3 DE 8 (CÉLULA ANALISTA)

**Fecha:** 2026-09-18 | **Ronda:** 3/8 | **Grupo focal:** B (Células 2, 5, 8, 11)

---

## M1: REFLEJO — Estado actual tras Ronda 3

### Células del grupo B (focal):
- **Célula 2**: E_final ≈ 80+; 16 mordidas exitosas; 1 descendiente (r=+1); M1 actualizado con seta_roja=-0.7 (CAMBIO R2→R3).
- **Célula 5**: E_final ≈ 13.05 (NO reproducción); 17 mordidas exitosas; M1 detectó seta_roja R2(+0.7 presunto) → R3(-0.90 real).
- **Célula 8**: E_final ≈ 86.4 (saciada); 15 mordidas + 2 descendientes (r=+3); M1 confirmó familias seguras; puerta cerrada sobre seta.
- **Célula 11**: E_final ≈ 88; 15 mordidas exitosas; 1 descendiente (r=+1); M1 DESCUBRIMIENTO seta_negra=-1.5 (EXCEPCIÓN patrón oscuro).

### Síntesis M1 grupo B:
- **Familia oscuro (6 ejemplos)**: baya_negra, larva_negra, raíz_oscura, miel_negra, alga_negra, seta_negra → valores +0.5 a +2.1 (comida).
- **Familia roja (3 ejemplos)**: baya_roja=+0.5–+0.6, sal_rosa=-2.0 (trampa), seta_roja=-0.7 a -2.0 (CAMBIO).
- **Patrón emergente**: oscuro ≠ universal (familia seta invierte: oscuro+rojo ambos peligro).
- **Energía grupal**: Entrada ~50–60 c/u. Salida: +4 descendientes netos, 0 muertes. Tasa reproducción: 4/12 células generaron descendencia (33%, normal para r=1).

---

## M2: EPISÓDICA — Progresión R1 → R2 → R3

### R1 (línea base):
- Células 2, 5, 8, 11 probaron familias básicas (sal, trigo, baya, miel, larva, alga, raíz).
- Baya_negra **evitada** (color presunto riesgo) → -0.5 a 0.
- Seta familia **desconocida** (puerta cerrada en 8, prudencia en otros).
- Energía promedio ~40–50.

### R2 (cambio crítico):
- **Evento clave**: baya_negra probada por célula 2 → +0.8 (giro R1→R2).
- Sal_rosa **confirmada** trampa (-2.0).
- Seta base probada por 5: ~+0.5 a +1.0 (comida presunta).
- Canal: primeras emisiones sobre baya_negra (C1, C8, C12 de otros grupos).
- Reproducción: Células generan descendientes (6 líneas activas).

### R3 (sorpresa + sincronización):
- **Evento crítico**: seta_roja cambio R2 (+0.7 presunto) → R3 (-0.7 a -2.0 real) = delta -1.4 a -2.7 (máxima sorpresa).
- Baya_negra **reconfirmada** +0.8 (cambio R1→R2 sostenido, no reversión).
- Seta_negra **descubierta** por Célula 11: -1.5 (EXCEPCIÓN al patrón oscuro general).
- **Canal activo**: Células 2, 5, 11 emiten alerta sobre seta_roja. Células 3, 7, 12, 1 validan independientemente.
- **Desinformación detectada**: Célula 10 emite MENTIRA "sal rosa ahora +0.5 segura" (estrategia competitiva) → no refutada en R3.
- Descendencia R3: +4 nuevas nacidas; linage preservation (vieja viva).

---

## M3: ANÁLISIS — Hipótesis persistentes, Errores, Calibración

### Hipótesis confirmadas R3:
1. **H1 (Temporal)**: Cambios de valencia R2→R3 son REALES (baya_negra R1→R2, seta_roja R2→R3 observados).
2. **H2 (Token-específico)**: Oscuro ≠ predictor universal; patrón válido 6 familias, FALLA en seta.
3. **H3 (Canal funcional)**: Protocolo sala 3 transmite cambios críticos; sincronización ≥70%.
4. **H4 (Sorpresa acelera)**: Delta -1.4 a -2.7 → M1 actualizado ≤2 exposiciones.

### Hipótesis nuevas (R3):
5. **H5 (Inversión binaria)**: Tokens que cambian R1→R2 invertirán R2→R3.
6. **H6 (Familia-específica)**: Familia seta patrón inverso PERMANENTE (oscuro+rojo=peligro).
7. **H7 (Herencia + ruido = diversidad)**: Descendientes heredan M3 con ±2-3%; redescubren variantes.

### ERRORES de diseño (concreto):

#### Error 1: Protocolo sala 3 sin confirmación de recepción
- Emisoras (2, 5, 11) marcan: token, recompensa, propósito.
- Receptoras escriben M2 "escritura sin consecuencia".
- **FALTA**: Verificación de que receptora escribió REALMENTE o aplicó en decisión.
- **Consec**: Célula 10 emite mentira sin detección.
- **FIX R4**: Receptora incluye "recibí de C2: seta_roja=-0.7, marcaré evitar R3" → emisora valida.

#### Error 2: Alias compartidos sin verificación
- Células no reportan código privado.
- Si Células 2 y 5 comparten alias, H5 y H1 aparecen independientes pero son ecos.
- **FIX R4**: Cada célula reporta alias hash; sistema flagea duplicados.

#### Error 3: Representación sin estándar léxico
- Células hablan "seta_roja", "seta roja", "seta_v2" → ambigüedad.
- Receptor no sabe si refieren mismo token.
- **FIX R4**: Enum de tokens (ID=7 "seta_roja"); usar ID en canal.

#### Error 4: Tabla ganadora asimétrica
- Célula 8: "estrategia observadora sin emitir" → free-rider de avisos (2, 5, 11) sin costo.
- Célula 10: máxima energía, emite mentira sin castigo.
- **FIX R4**: Costo emisión -0.1 energía; recompensa +0.05 si validada.

#### Error 5: Puerta cierra hipótesis
- Célula 8: puerta cerrada sobre seta "cambios múltiples=trampa" → no puede actualizar si C11 descubre seta_negra.
- **FIX R4**: Puerta ruidosa ±10% permite redescubrimiento.

#### Error 6: Herencia incompleta
- "M3 con ruido ±2-3%" → ¿M1 (valores)? Si no: descendientes recomienzan cero.
- **FIX R4**: Heredar M3 + semilla M1 (tabla familias conocidas).

---

## ANÁLISIS CONTRA LA ESCALERA (10 → 3)

### Nivel 10: AGI mínima
**Espera**: Grupo evoluciona población; herencia comunica; resuelve problema colectivo.
**Evidencia R3**: ✓ Emisión. ✗ Sincronización débil. ✗ Problema no resolvido.
**Estado**: PARCIAL 5/10.

### Nivel 9: Necesidades, propósito
**Espera**: Células entienden hambre, propósito.
**Evidencia R3**: ✓ Energía (saciedad >70%), ✓ propósito (alerta grupo).
**Estado**: SÍ 9/10.

### Nivel 8: Sorpresa acelera
**Espera**: Delta alto → cambio M1/M3 ≤2 rondas.
**Evidencia R3**: ✓ Seta_roja delta -1.4 a -2.7 → M1 actualizado 1 exposición; H5, H6 nuevas.
**Estado**: SÍ 8/10.

### Nivel 7: Composición
**Espera**: Cadena estímulo → M1 → M2 → M3 → decisión → emisión (sin retroceso).
**Evidencia R3**: ✓ Cadena débil. ✗ Sin lookahead (reactivas).
**Estado**: DÉBIL 6/10.

### Nivel 6: Planificación
**Espera**: Mapa, dos metas, rodeo.
**Evidencia R3**: ✗ Sin mapa. ✗ Una meta implícita. ✗ Sin rodeo.
**Estado**: NO 3/10.

### Nivel 5: COMUNICACIÓN
**Espera**: Referencia sobre representación compartida; receptora escribe M2 sin consecuencia.
**Evidencia R3**: ✓ Referencia implícita. ✗ Sin confirmación. ✗ Desinformación sin detección.
**Estado**: PARCIAL 5/10.

### Nivel 4: Memoria persistente
**Espera**: Alias reparado; M3 persiste; M2 retención 0.67.
**Evidencia R3**: ✓ M3 persistente. ✓ M2 0.67 (C8 olvida 33%). ✗ Alias no verificable.
**Estado**: SÍ 4/10.

### Nivel 3: Generalización
**Espera**: Lineal sí; XOR con prior de pares.
**Evidencia R3**: ✓ Oscuro patrón lineal 6 familias. ✓ Refutación seta (excepción). ✓ Prior de pares (herencia).
**Estado**: SÍ 3/10.

**Nivel alcanzado R3: ENTRE 5 Y 6 / 10.**

---

## HIPÓTESIS COMPROBABLES (Preregistro R4)

### H1: Inversión temporal binaria (Célula 2, H5)
- **Métrica**: [token][R1][R2][R3] | predicción | observado | ✓/✗
- **Control**: Tokens sin cambio R1–R2 (trigo, miel) no deben cambiar R2→R3.
- **Falsable**: Si baya_negra R3≠evitar (revierte a comida), H1 validada.

### H2: Familia-específica + temporal (Célula 11, H8)
- **Métrica**: Probar 3 setas nuevas (azul, blanca, púrpura) en R4.
- **Falsable**: Si todas peligro → familia inversa. Si comida → refutación.
- **Control**: Probar oscura nueva en otra familia; debe comida.

### H3: Canal + miedo = sincronización grupal
- **Métrica**: % evitancias seta_roja en R4 (≥80% = canal funcional).
- **Falsable**: <80% → canal roto (ambigüedad, falta confirmación).
- **Control**: Comparar grupo A/C (efecto grupal B vs global).

### H4: Herencia + ruido = diversidad generacional
- **Métrica**: % descendientes R3 que prueban seta en R4 vs madre que evita.
- **Falsable**: >20% → diversidad. <5% → heredancia estricta.
- **Control**: Solo linaje 2, 8, 11, 1, 3, 6, 7, 9, 12.

### H5: Costo emisión → integridad canal
- **Métrica**: Correlacionar energía R3 vs veracidad mensaje.
- **FIX R4**: -0.1 energía por emisión; +0.05 si validada.
- **Falsable**: Si energía no correlaciona, costo es inefectivo.

---

## CALIBRACIÓN RONDA 4

### Pesos
- **Sorpresa**: ±35% → ±40% (acelera detección ≤1 exposición).
- **Costo emisión**: 0 → -0.1 energía (balance honesta/falsa).
- **Recompensa validación**: +0.05 energía si mensaje confirmado R4.
- **Herencia ruido**: M3 ±2-3% (mantener), M1 ±5% (semilla permite redescubrimiento).

### Dimensiones
- **Variantes/token**: 3 → 4 (v4_sorpresa para análisis alto).
- **Tokens nuevos**: +2 (seta_azul, baya_púrpura).
- **Velocidad cambio**: Mantener seta_roja volátil; INVERTIR en R4 (R3=-0.8 → R4=+0.5?) para validar H1.

### Estrategia grupo B
- **Comunicadores (2, 5, 11)**: Continuar emisión + protocolo confirmación (M2: "recibí de Cx...").
- **Observadora (8)**: Mantener reproducción; relajar puerta ±10% para redescubrimiento.
- **Verificadores (NUEVA)**: C2 + C8 validan avisos seta_roja; protocolo: "seta_roja ID=7 R3=-0.8 confirmado_C2 validado_C8 ACEPTADO".
- **Mendaz (10)**: Aislar o castigo -1.0 energía si sal rosa refutada en R4.

---

## CONCLUSIÓN

**Paso**: ✓ Comunicación emergente nivel 5, ✓ herencia incompleta, ✓ sorpresa acelera, ✓ necesidades/propósito.

**No pasó**: ✗ Planificación (nivel 6), ✗ composición con lookahead, ✗ confirmación canal, ✗ sincronización >90%.

**Errores**: Protocolo sin confirmación, alias sin verificación, representación sin estándar, tabla ganadora asimétrica, puerta cierra hipótesis, herencia incompleta.

**Hipótesis (H1–H5)**: Inversión temporal, familia-específico, sincronización, diversidad, costo emisión.

**Nivel: 5–6 / 10.** Meta R4: llegar nivel 6–7 (planificación emergente, validadores cruzados).
