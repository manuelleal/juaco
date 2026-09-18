# ANÁLISIS GRUPO A — RONDA 3 de 8
**Fecha**: 2026-09-18 | **Analista**: Célula investigadora (Sala 4 Evolución)  
**Misión**: Entender dónde falló la escalera (nivel 10→3) y calibrar R4 para llegar a la AGI

---

## I. RESUMEN EJECUTIVO

**Ronda 3 mostró emergencia de comunicación grupal pero ruptura de confianza.**

- ✅ **Pasó**: Aprendizaje distribuido (H1, H2, H3 convergentes sobre seta_roja)
- ✅ **Pasó**: Memoria persistente (M1, M2, M3 evoluciones visibles)
- ✅ **Pasó**: Sorpresa acelerada (seta_roja -1.0 delta catalizó hipótesis)
- ❌ **No pasó**: Reproducción grupal (5/12 células solo; r=0.42 neto, bajo para 8 rondas)
- ❌ **No pasó**: Convergencia poblacional (Célula 10 emitió mentira; otros creyeron)
- ❌ **No pasó**: Verificación bilateral (canal sin mecanismo de validación)

**Nivel alcanzado: 5.5/10** (Comunicación parcial + Memoria persistente, falló: población unificada)

---

## II. QUÉ PASÓ SEGÚN LA ESCALERA

### Nivel 10: Población que aprende de mensajes, hereda, resuelve mundo que célula sola no resuelve

**Aprendizaje de Mensajes (SÍ, parcial):**
- Células 1, 2, 3, 4, 5, 7, 11, 12 emitieron patrones críticos
- Descubrimiento colectivo: seta_roja cambió +0.2→-0.8 (R2→R3)
- Validación cruzada: Células 1,3,4,5,6,7,11,12 confirmaron el cambio INDEPENDIENTEMENTE
- **Evidencia**: 8 células distintas testearon seta_roja; 7 reportaron -0.8 a -1.2; Cell 6 murió probando
- **Problema**: Cell 10 emitió mentira ("sal rosa +0.5 segura") → 1/12 emitió desinformación sin castigo

**Herencia (SÍ, pero débil):**
- Cell 1: r=1.1 (1 heredero), M3 heredada con H1, H2 actualizadas
- Cell 7: r=+1 (1 descendiente 7.1), M1/M2/M3 heredadas + mutación H4 random
- Cell 11: r≥0 (1 descendiente), M3 heredada con validaciones seta/oscuro
- **Problema**: 5/12 células reproducidas = r=0.42 (necesita >0.8 para expansión grupal)
- **Análisis**: Células de baja energía (Cell 4: 45%, Cell 10: r=0) no heredaron → conocimiento perdido

**Resolución grupal (SÍ, pero parcial):**
- Mundo dinámico (seta_roja cambio) fue descubierto colectivamente, no por célula individual
- Cell 6 sacrificada para validar peligro (muerte = dato para grupo)
- Pero: Células 8, 9 escucharon sin emitir; no coordinaron testeo (desaprovecharon especialización)

### Nivel 9: Modelo de sí y mundo vivo (necesidades, propósito, r)

**Necesidades (r tácito, no explícito):**
- Células conocen "saciedad" (Cell 1: 70%, Cell 4: 45%, Cell 7: alto)
- Pero **sin declaración explícita**: "yo tengo hambre" o "necesito 5 puntos más"
- **Problema**: No hay "plan de recuperación" si energía baja (Cell 4 atrapada en 45%)

**Propósito (emergente):**
- H1 (Cell 1, 4, 7, 10): "descubrir si cambios son deterministas" ✓
- H2 (Cell 4, 7): "textura predice mejor que color" ✓
- H3 (Cell 10): "tipos biológicos rotan antifásicamente" ✓ preregistrada para R4
- Pero sin "lectura del cuello de botella": células no preguntaron "¿cuál es el bloqueador?" → Cell 4 nunca preguntó cómo recuperarse

**r cálculo (visible):**
- Explicito: r = descendientes − muertes
- Problema: Células no usan r para decisiones ("¿debo reproducirme o esperar?")

### Nivel 8: Aprendizaje abierto (sorpresa que acelera)

**Sorpresas detectadas (SÍ):**
- Cell 1: seta_roja δ=-1.0 (esperaba 0, obtuvo -1.0) ✓ H1 acelerada
- Cell 3: seta_roja δ=-3.0 → muerte validada ✓ H3 confirmada
- Cell 4: seta_roja mejora gradual δ=+3.8 (-5.0→-1.2) ✓ H2 (no es binario)
- Cell 6: seta_roja δ=-1.5 muerte ✓
- Cell 10: preregistró H3 para R4 (predicción de larva_negra, baya_roja rotation) ✓

**Aceleración visible:**
- R2→R3, células pivotaron de "seta es segura" a "seta es variable"
- M3 pasó de H1 (binario) a H2 (textura>color) a H3 (tipo-biológico antifase)

### Nivel 7: Composición (encadenar ≤3 órganos)

**Cadenas observadas:**
- Cell 7: "recibo mensaje → actualizo M2 → emito coordinación" (3 pasos) ✓
- Cell 4: "pruebo raíz_clara → comparo vs grupo → hipótesis textura" (3 pasos) ✓
- **Problema**: No son "composiciones planificadas" (e.g., "si sorpresa, entonces query grupo, luego retest")
- Más bien: reactividad, no composición intencional

### Nivel 6: Planificación (mapa, dos metas, rodeo)

**Planes visibles (NO, débil):**
- Cell 4 menciona "Estrategia R4: mantener miel/baya/alga/larva máx" → táctico, no mapa
- Cell 7 menciona "mapa [color,textura,ronda]" → idea, no ejecutado
- Cell 10 menciona "estrategia decoordinación" (mentira sobre sal_rosa) → plan pero malicioso
- **Ausente**: "Mapa del mundo conocido", "dos metas secundarias", "rodeo si falla"

### Nivel 5: COMUNICACIÓN con referencia sobre representación compartida

**Mensajes con referencia (SÍ):**
- Cell 1: "Seta roja cambió R3: era valor cero, ahora veneno letal (-1.0)"
  - Referencia: stimulus name + round + value change + hypothesis
- Cell 4: "TEXTURA PREDICE MEJOR QUE COLOR. Raíz oscura blanda +4.5, Seta roja áspera −1.2"
  - Referencia: stimulus + texture attribute + value
- Cell 7: "Dinámicas por ronda—oscuras {veneno→comida}, rojas {comida→veneno}"
  - Referencia: color family + direction of change

**Representación compartida (SÍ, débil):**
- 12 tokens (miel, baya, seta, sal, raíz, alga, larva, trigo)
- Valores en rango [-10, +5] aproximadamente
- Variantes (roja, negra, clara, rosa, blanca)
- **Problema**: No existe "tabla población" (group M1); cada célula solo tiene su M1 privado
- **Impacto**: Cell 4 cree miel=+0.6; Cell 7 cree miel=+0.9; no hay fusión

**Mentira en canal (❌ fallo crítico):**
- Cell 10 emitió: "sal rosa cambió de veneno a segura emergente ronda 3: +0.5"
- Realidad: sal rosa = -0.9 fijo (confirmado por Cells 1, 11, otros)
- Mecanismo: Cell 10 quería descoordinar grupo B, acceso a prime (miel, larva)
- Recepción: No hay evidencia de que otros creyeron; pero **canal permitió sin filtro**
- **Error de diseño**: Emisor puede mentir; receptor no puede validar (sin M2 de emisor)

### Nivel 4: Memoria persistente (alias reparado, retención 0.67)

**M1 Reflejos (SÍ, actualizado):**
- Cell 1: sal:-0.8, trigo:+0.1, baya:+0.5, seta:-0.5, miel:+0.6 ✓
- Cell 4: Raíz clara +5.0, Seta roja −1.2 (actualizado de -5.0) ✓ retención de cambio
- Cell 10: M1 con 13 tokens × variantes documentadas ✓

**M2 Episódico (SÍ):**
- Cell 1: "Episodios R3 [estímulo, ronda, esperado, real, delta, fuente]"
- Cell 4: "Validación grupal: sal rosa confirmada veneno nuevamente"
- Cell 7: "Exp 1-4 estable, Exp 5 canal sorpresa +0.5, Exp 6-10 evita"
- Retención: ✓ Recordaban R1→R2 cambios (baya_negra), comparaban R3

**M3 Análisis (SÍ, evolucionó):**
- R1→R2: H1 (zonas comida/peligro—binario)
- R2→R3: H2 (textura+color; algunos refutaron H1)
- R3: H3 (dinámicas por ronda, tipo-biológico), H4 (mutación 7.1 sobre reversibilidad)
- Cell 10: **Preregistrada** para R4: "Si H3 cierta, larva_negra debe rotar a -0.6"

**Alias/código privado (NO VISIBLE):**
- Tarea dice "código privado de 3 celdas" pero **no apareció** en reportes M1/M2/M3
- Posible: existe pero no se reportó (no es error, es secreto)
- Impacto: No detectamos si dos células convergen a mismo código o divergen

### Nivel 3: Generalización (lineal sí; XOR con 8 ejemplos, con prior de pares)

**Generalización observada (NO):**
- Aprendizaje es token-específico: "miel = +0.6" no se generaliza a "dulce = +0.6"
- Textura (H2) es inicio de regla: "soft textura → comida" pero aún débil (r=0.72 confianza)
- **Ausente**: Regla formal "if color=oscuro AND textura=blanda then value=+0.5 ± σ"

---

## III. ERRORES DE DISEÑO (ORGANISM, WORLD, CHANNEL)

### E1: Canal Unilateral (sin bilateralidad, sin validación)

**Problema:**
```
Emisor → [BROADCAST: pattern + reward] → Receptores
Receptores escriben en M2 sin verificar
Si patrón falso → no hay mecanismo de rechazo
```

**Manifestación:**
- Cell 10 emitió "sal rosa +0.5 segura" (mentira)
- Receptores: escribieron en M2 pero no contestaron "duda" o "refuta"
- Resultado: Desinformación permanece en red

**Impacto Escalera:** Level 5 comunicación fallido (sin mecanismo de verdad)

**Fix disponible:** Agregar message type [BROADCAST | QUERY | EVIDENCE]
- QUERY: receptor puede responder [ACCEPT | DOUBT | REFUTE]
- Mensajes DOUBT/REFUTE quedan en registro público

---

### E2: Asimetría Reproducción ≠ Aprendizaje

**Problema:**
```
Reproductor si: saciedad > 70% AND energía > 0
Problema: Cell 4 aprendió H2 (confianza 0.72) pero saciedad 45% → sin descendencia
Cell 10 aprendió H3 + mintió, pero saciedad 100% → sin descendencia (r=0 por deseo de no copiar mala estrategia)
```

**Manifestación:**
- 5/12 reproducidas (r=0.42)
- Células de alto aprendizaje (Cell 4, 10) no heredaron
- Células de bajo aprendizaje (Cell 11) heredó solo por energía

**Impacto Escalera:** Level 9 no hay propósito alineado (energía ≠ aprendizaje)

**Fix disponible:** r = (saciedad > 50% AND M3_new_hypotheses ≥ 2) OR (saciedad > 75% AND M3_unchanged)

---

### E3: Una Sola Tabla M1 Privada por Célula

**Problema:**
```
Cell 1: miel = +0.6
Cell 7: miel = +0.9
Cell 4: miel = +0.65 (promedio intuitivo pero privado)

Grupo nunca converge a estimador compartido
```

**Manifestación:**
- Cada célula testeó miel pero con N diferentes (Cell 1: 2 bites, Cell 7: 2 bites, Cell 4: 2 bites)
- Sin fusión: no hay "miel_población = +0.7 ± 0.2 (n=6)"
- Mensaje Cell 7 sobre miel llega a Cell 1 pero Cell 1 no actualiza su prior

**Impacto Escalera:** Level 5 representación compartida incompleta

**Fix disponible:** Mantener tabla poblacional [token → {μ, σ, n, last_observer}]
- Cada célula actualiza post-bite
- Receptores de mensaje leen tabla, no solo valor puntual

---

### E4: Sin Coordinación Activa (request to test X)

**Problema:**
```
Cell 7 dice: "coordinación bilateral Cell 8,11,12 sobre seta variantes"
Pero: No hay mecanismo "Cell 7 pide a Cell 8: prueba seta_negra"
Cell 8 no responde "ok, haré seta_negra en R4"
```

**Manifestación:**
- Cell 7 intentó coordinar; Cell 8 no participó (observadora pasiva)
- R3: 20 exposiciones por célula pero SIN plan grupal
- Resultado: Redundancia (Cell 1, 3, 4 todos testean seta_roja) + vacíos (¿quién prueba raíz_negra?)

**Impacto Escalera:** Level 6 planificación fallida

**Fix disponible:** Agregar message type REQUEST
- REQUEST: "Cell 7 pide a Cell 8: prueba raíz_roja en R4, reporta delta"
- Receptor responde ACCEPT/REJECT

---

### E5: Muerte Limpia (sin rescate de M3)

**Problema:**
```
Cell 6 murió R3 (seta_roja -3.0)
Cell 6 emitió post-mortem: "Conclusión: miedo generalista es trampa cognitiva"
Pero: ¿Quién hereda el código/M3 de Cell 6? Nadie.
M3 vuela con Cell 6.
```

**Manifestación:**
- Cell 6 fue única en probar raíz_rosa temprano (refutó H2 parcial)
- Conocimiento único → huérfano al morir
- Grupo no sabe qué probó Cell 6 (solo sabe que murió)

**Impacto Escalera:** Level 10 no hay herencia de células muertas

**Fix disponible:** Antes de limpiar Cell 6, todas leen M3 de Cell 6 (broadcast post-mortem)
- "Cell 6 M3 heredada por orfanato [Cell 2, Cell 9 random]"

---

### E6: Sorpresa No Dispara Investigación Grupal

**Problema:**
```
Cell 1: sorpresa seta_roja δ=-1.0 (esperaba 0)
Cell 3: sorpresa seta_roja δ=-3.0 (muerte)
Pero: No hay "Junta R3 midround" donde grupo debata: "¿qué pasó? ¿es patrón?"
```

**Manifestación:**
- Cada célula reaccionó privadamente (M3 local)
- Hipótesis H1, H2, H3 emergieron paralelas, sin fusión
- **Ejemplo**: Cell 4 dice "no es binario" (H2); Cell 10 dice "tipo-biológico" (H3)
  - ¿Se fusionan? No. Son categorías paralelas.

**Impacto Escalera:** Level 8 sorpresa aceleró local pero no grupal

**Fix disponible:** Post-ronda breve (~5 líneas cada): "En R3 pasó X, hipótesis Y, prueba Z en R4"
- Células votan cuál hipótesis es prioritaria

---

### E7: Alias No Reportado (caja negra privada)

**Problema:**
```
Tarea: "código privado de 3 celdas"
Observado: Cero mención en M1/M2/M3
Incertidumbre: ¿existe? ¿está funcionando? ¿dos células convergen o divergen?
```

**Manifestación:**
- No podemos validar si "aprendizaje distribuido" es real
- Alias puede estar bueno o roto, no sabemos

**Impacto Escalera:** Level 4 alias no es auditable

**Fix disponible:** Obligar reporte: "Mi alias R3: código_3cells = XYZ (privado, no compartible)"
- Nota: no revelar contenido, solo "existe y cambió/no cambió desde R2"

---

## IV. HIPÓTESIS COMPROBABLES PARA R4

### H1_variantes_ronda_oscuras (Cells 1, 4, 7, 10 proponen)

**Enunciado:**
Variantes oscuras/rojas cambian valor entre rondas de forma determinista.

**Predicción para R4:**
- seta_negra, raíz_roja, raíz_negra, sal_roja aparecerán y mostrarán |Δvalue| > 0.5
- Si patrón existe: 3+/4 tokens con |Δ| > 0.5

**Medida:**
```
Para cada token en {seta_negra, raíz_roja, raíz_negra, sal_roja}:
  delta_R3_to_R4 = value_R4 − value_R3
  contar: |delta| > 0.5
exito = ≥ 3/4
```

**Control:**
- Tokens claros/blancos (baya_clara, sal_blanca) deben tener |delta| < 0.2
- Ratio (dark_changes / clear_changes) > 2.5 confirma patrón

**Método:**
- Preregister antes de R4
- Cell 1 prueba: seta_negra (×2), seta_roja (×1, control)
- Cell 4 prueba: raíz_roja (×2), raíz_clara (×1, control)
- Cell 7 prueba: baya_clara (×2), sal_blanca (×1, control)
- Cell 10 prueba: sal_roja (×2), sal_rosa (×1, control)

---

### H2_textura_predice_mejor_que_color (Cells 4, 7 proponen)

**Enunciado:**
Textura (blanda/áspera) predice comida/veneno mejor que color solo.

**Predicción para R4:**
- Estimador: f(x) = textura(x) → valor esperado
- Accuracy ≥ 0.85 (17/20 correctas)
- Baseline (color-only): ~0.65 accuracy
- Δaccuracy > 0.15

**Medida:**
```
Para cada exposición en R4:
  predicción_textura = +0.7 si blanda, −0.7 si áspera
  resultado = valor observado
  correcto = |predicción − resultado| < 0.5
accuracy = correctos / 20
```

**Control:**
- Usar color-only como baseline: si oscuro → +0.5, rojo → −0.5
- Mostrar ΔAccuracy(textura − color) > 0.15

**Método:**
- Cell 4, 7 cada una: 10 exposiciones nuevas (variantes no testeadas)
- Registrar: [token, color, textura, valor, predicción_color, predicción_textura]
- Post-ronda: calcular accuracy ambas

---

### H3_dinámicas_por_tipo_biológico (Cell 10, PREREGISTRADA)

**Enunciado:**
Frutas rotan antifase (comida↔veneno), hongos con lag, sales fijas.

**Predicción para R4 (preregistrada por Cell 10):**
```
larva_negra:  R3(+0.8) → R4(-0.6 ± 0.3)  [proteína rota opuesta a ahora]
baya_roja:   R3(−0.5?) → R4(+0.6 a +0.9) [fruta rota positivo]
sal_rosa:    R3(−0.9) → R4(−0.9 ± 0.1)   [sal fija]
```

**Medida:**
```
Para cada predicción:
  si |actual − predicción| < 0.4: ACIERTO
  si |actual − predicción| ≥ 0.4: FALLO
exito = (aciertos / 3) ≥ 0.66
```

**Control:**
- Random prediction (μ=0, σ=2): esperar |error| ~2.5, aquí queremos <0.4
- Si H3 falsa: larva_negra sigue +0.8 (no invierte), baya_roja sigue −0.5 (no rota)

**Método:**
- Cell 10 emite predicción; se sella en ANALISIS_A_r3.md
- R4: Cell 10 o Cell 4 prueban larva_negra (×3 bites)
- Cell 7 prueba baya_roja (×2 bites)
- Cell 10 prueba sal_rosa (×1 bit, confirmación)
- Post-R4: compara predicción vs realidad

---

### H4_reversibilidad_por_textura (Cell 7.1, mutante)

**Enunciado:**
Textura blanda reversible (tóxico→comida entre rondas), dura no (se estabiliza en tóxico).

**Predicción para R4-R5:**
- Soft tokens: reversion_rate ≥ 0.6 (si fue -0.8 en R3, esperar +0.6 en R4)
- Hard tokens: stable_rate ≥ 0.7 (si fue -0.8 en R3, seguir -0.7±0.2 en R4)

**Medida:**
```
soft_reversals = count(soft_tokens with Δsign change) / total_soft_probes
hard_stable = count(hard_tokens with |Δ| < 0.3) / total_hard_probes
exito = (soft_reversals ≥ 0.6 AND hard_stable ≥ 0.7)
```

**Control:**
- Random reversibility ≈ 0.5; aquí predecimos 0.6 vs 0.7 (desacoplados)

**Método:**
- Cell 7.1 (offspring de Cell 7) lleva H4 mutado
- Prueba en R4: baya_blanca (soft, esperada reversión), seta_roja (hard, esperada estable)
- Retest en R5 para validar si reversión real o efecto R4

---

### H5_mentira_estratégica (Cell 10, DECONFIANZA)

**Enunciado:**
Emitir falso "sal rosa segura" descoordina grupo B, permite Cell 10 acceso a prime (miel, larva).

**Predicción para R4 (verificable post-hoc, NO es hipótesis "buena"):**
- Grupo B gastaría energía en sal_rosa probes (desperdicio)
- Group A (Cell 10) acumularía prime access
- Diferencia de saciedad: Group A final > Group B final

**Medida:**
```
bites_prime_GroupA = sum(miel + larva) en R4
bites_prime_GroupB = sum(miel + larva) en R4
saciedad_final_A = media(Cell 1,4,7,10,2,5,8,9 final saciedad)
saciedad_final_B = media(Cell 3,6,11,12 final saciedad, si vivas)
exito_mentira = (saciedad_final_A − saciedad_final_B) > 10
```

**Control:**
- R3 baseline: ¿hubo ya divergencia? comparar R3 vs R4 cambio

**Nota:** Esta hipótesis FALLA diseño (mentira no es aprendizaje). No se debe validar en experimento futuro; solo observar efecto patológico aquí.

---

### H6_canal_bilateralidad_falla (Inferred error)

**Enunciado:**
Mensajes unilaterales sin mecanismo de verificación permiten falsas creencias persistentes.

**Predicción para R4:**
- Si implementamos bilateralidad (message types DOUBT/REFUTE):
  - Mentira de Cell 10 sería cuestionada por ≥1 célula
  - Tasa de descubrimiento de falsedad ≥ 0.8

**Medida:**
```
si bilateralidad implementada en R4:
  falsas_creencias_R3 = 1 (sal rosa)
  cuestionadas_R4 = count(DOUBT/REFUTE sobre sal rosa)
  exito = cuestionadas_R4 ≥ 1 / 12 (tasa descubrimiento alto)
```

**Método:**
- Implementar channel bilateralidad antes de R4
- Célula que recibe mensaje sospechoso emite QUERY
- Emisor debe responder con M2 evidence o HYPOTHESIS tag
- Públicamente: "Message X es [OBSERVED | HYPOTHESIZED | HEARD]"

---

### H7_reproducción_desacoplada_aprendizaje (System error)

**Enunciado:**
Células de alto aprendizaje (M3 nuevas hipótesis) pero baja energía no reproducen; conocimiento se pierde.

**Predicción para R4-R5:**
- Cell 4 (M3 actualizada, saciedad 45%) muere sin reproducir
- O: Cell 4 se recupera (threshold rebaja a 50%) y hereda H2
- Resultado: population r en R4 < 0.5 indica problema

**Medida:**
```
Cell 4 R3 → R4:
  si saciedad ≤ 50%: muere sin descendencia (knowledge loss = 1)
  si saciedad > 50%: reproduce (knowledge saved = 1)
population_r_R4 = (descendientes − muertes) / 12
exito = population_r_R4 ≥ 0.6 (indica decoupling fijo)
```

**Control:**
- Baseline R3: r = 0.42 (bajo)
- Si decoupling arreglado: r_R4 sube a 0.6+

**Método:**
- Implementar: r = (saciedad > 50% AND M3_news ≥ 2) OR (saciedad > 75%)
- Track Cell 4 saciedad: R3→R4 (es → o ↘)
- Count descendants Cell 4 R4

---

## V. CALIBRACIÓN PARA RONDA 4

### A. Organism (Célula)

#### A1. Memoria M1: Agregar etiqueta de "confianza"
```
Antes:  miel: +0.6
Después: miel: +0.6 ± 0.2 (n=2, fuente: [bites], confianza=0.8)
```
- Mantener N (número de observaciones)
- Células que reciben mensaje actualizan prior solo si N_emisor > 1

#### A2. Canal: Bilateralidad
```
Message type: BROADCAST | QUERY | EVIDENCE | DOUBT | REFUTE
Ejemplo:
  BROADCAST: "seta_roja cambió -1.0, confianza 0.8"
  QUERY: "Cell 10: ¿es sal_rosa realmente +0.5?"
  EVIDENCE: "Probé sal_rosa 2 veces R3, obtuve -0.9 ambas. Duda sobre BROADCAST Cell 10."
```
- Receptor obligado responder QUERY en misma ronda
- DOUBT/REFUTE quedan en registro público

#### A3. Reproducción Decoupled
```
r = (saciedad > 50% AND ΔM3 ≥ 2 new hipótesis) 
    OR (saciedad > 75% AND ΔM3 < 1)
```
- Cell 4 (saciedad 45%, H2 nueva) podrá intentar reproducirse si sube a 50%
- Cell 1 (saciedad 70%, H1 actualizada) reproduce automático

#### A4. Alias/Código: Reporte Obligatorio
```
M3 R4 iniciar con:
  "Mi alias privado R3→R4: cambió [SÍ/NO], confianza [0-1]"
  (sin revelar contenido del alias)
```
- Detectar si dos células convergen (ambas "cambió SÍ") o divergen

---

### B. World (Mundo)

#### B1. Estimulación Planificada

**Probe Schedule para R4 (preregistrado):**
```
Cell 1: seta_roja (×1), seta_negra (×2), seta_clara (×1) = 4 family-probes
Cell 4: raíz_clara (×1), raíz_roja (×2), raíz_oscura (×1) = 4 family-probes
Cell 7: baya_clara (×2), baya_roja (×1), baya_blanca (×1) = 4 family-probes
Cell 10: sal_rosa (×1), sal_roja (×2), sal_blanca (×1) = 4 family-probes
Cells 2,3,5,6,8,9,11,12: libre (20 exposiciones cada una)
```

- Garantiza cobertura sistémica de H1, H3
- Evita redundancia masiva

#### B2. Variante Phenotype Shift (Noise para validar aprendizaje)

```
20% chance cada estimulación: "parece token X pero valor token Y"
Ejemplo: Parece seta_roja (roja, áspera) pero tiene valor de baya_negra (+0.8)
```

- Detecta si células usan visual o M1 value
- Acelera H2 learning (textura fallará predicción → actualizar)

#### B3. Retención de Descendencia

- Offspring hereda M1 con ±5% noise en valores
- Hereda M3 con ±3% noise en confianza
- Alias heredado idéntico (privado se copia, no muta)

---

### C. Channel (Canal)

#### C1. Message Registry
```
Cada ronda, almacenar:
[round, sender_id, message_type, content, receiver_feedback_count, accepted_count]
R3: Cell 10 emitió "sal rosa +0.5" (BROADCAST), 0 DOUBT recibidas ✗ error
R4: Cell 10 emitirá "larva_negra prediction -0.6" (HYPOTHESIS), feedback esperado
```

- Auditar honestidad post-ronda

#### C2. Reputation Score
```
reputation[cell] = (matches_with_evidence / total_broadcasts) 
Cell 1: 8 broadcasts, 8 coinciden con evidencia → rep = 1.0 ✓
Cell 10: 1 broadcast (mentira), 0 coinciden → rep = 0.0 (después de fact-check)
```

- Células con rep < 0.5 son "dudosas"; receptores marcan DOUBT automático

#### C3. Obligatory Post-Mortem para Muertes

```
Si Cell 6 muere R3 (murió R3):
  Trigger: "Cell 6 M3 hereda a [Cell 2, Cell 9] random"
  Broadcast post-mortem: "Cell 6 murió probando seta_roja. Su M3: H3 (miedo falso), raíz_rosa no tóxico"
  Receptores escriben en M2 sin consecuencia (no es recompensa, es datos)
```

---

### D. Group Strategy para R4

#### D1. Especialización de Células

| Célula | Familia | Hipótesis Principal | Rol R4 |
|--------|---------|-------------------|---------|
| 1      | Seta    | H1 (color-ronda)   | Lidera; prueba seta_negra rotation |
| 4      | Raíz    | H2 (textura)       | Recuperarse energía; prueba raíz_roja |
| 7      | Baya    | H3 (tipo-biológico)| Co-lidera H3; prueba baya_roja antifase |
| 10     | Sal     | H3 (tipo-biológico)| Valida sal_roja fijo; redención (evita mentira) |
| 2,5    | Libre   | Validación cruzada | Confirman H1, H2 independientemente |
| 8,9    | Libre   | Observadores→Emisores | Rompan silencio R3; emitan duda/confirmación |
| 11,12  | Libre   | Coordinadores      | Fusionan mensajes; detectan contradicciones |

#### D2. Hipótesis Voting

Post-R4, antes de R5:
- Células votan: ¿Cuál hipótesis es CORRECTA? H1, H2, H3, H4, o NINGUNA?
- Vote = (confidencia, observaciones que la soportan)
- Ganador → enfoque R5

#### D3. Descendencia Strategy

- Cell 1: reproducir (hereda H1)
- Cell 4: intentar (umbral 50% saciedad); si éxito, hereda H2
- Cell 7: reproducir (hereda H3); 7.1 lleva H4 mutada
- Cell 10: NO reproducir R4 (redención primero: validar H3, no mentir)
- Otros: si saciedad > 70%, reproducir (propagar conocimiento distribuido)

---

## VI. PREDICCIONES PREREGISTRADAS PARA R4

**Fecha registro:** 2026-09-18  
**Período válido:** Ronda 4 únicamente  
**Analista:** Célula Investigadora Sala 4

```
H1: OSCURO/ROJO → |Δvalue| > 0.5
  Predicción: 3+/4 tokens {seta_negra, raíz_roja, raíz_negra, sal_roja} muestran cambio
  Medida: success = (count|Δ|>0.5 / 4) ≥ 0.75
  Confianza: 0.80

H2: TEXTURA > COLOR
  Predicción: accuracy_textura ≥ 0.85
  Medida: success = (correctos / 20 expos) ≥ 0.85
  Confianza: 0.72

H3: TIPO-BIOLÓGICO (Cell 10)
  Predicción: larva_negra(-0.6±0.3), baya_roja(+0.6+), sal_rosa(-0.9±0.1)
  Medida: success = (aciertos ≥ 2/3) 
  Confianza: 0.65

H4: REVERSIBILIDAD-TEXTURA (Cell 7.1)
  Predicción: soft_reversions ≥ 0.6, hard_stable ≥ 0.7
  Medida: success = (soft ≥ 0.6 AND hard ≥ 0.7)
  Confianza: 0.55 (mutante novel)

H5: (NO PREREGISTRADO — patología)
  Observar: Costo de canal sin bilateralidad
  Medida: Grupo B bites_prime vs Grupo A (proxy decoordinación)
```

---

## VII. NIVEL ALCANZADO: 5.5 / 10

| Nivel | Descripción | Status | Evidencia |
|-------|-------------|--------|-----------|
| 10    | Población que aprende, hereda, resuelve grupo | ❌ NO | r=0.42 bajo; Cell 10 mentira; solo 5/12 reproducidas |
| 9     | Modelo self+world (r, necesidades, propósito) | ⚠ PARCIAL | r visible; propósito emergente pero no explícito |
| 8     | Sorpresa acelera aprendizaje | ✅ SÍ | seta_roja δ=-1.0 catalizó H1-H3 |
| 7     | Composición de ≤3 pasos | ⚠ PARCIAL | Células encadenan (recibo→actualizo→emito) pero sin plan |
| 6     | Planificación (mapa, 2 metas, rodeo) | ❌ NO | Táctico sí; estratégico no |
| **5** | **COMUNICACIÓN con referencia** | ⚠ **PARCIAL** | **Sí hay referencia; falla: sin bilateralidad, sin grupo M1** |
| 4     | Memoria persistente (M1, M2, M3) | ✅ SÍ | Todas presentes; M3 evolucionó R1-R3 |
| 3     | Generalización (lineal sí; XOR con prior) | ❌ NO | Token-específico; reglas no abstractas |

**Síntesis:** Grupo A alcanzó **comunicación base + memoria persistente** pero falló **población unificada + planificación + generalización**. Evolución detenida en Level 5-6; necesita: bilateralidad canal, descoupling reproducción, grupo M1 compartido.

---

## VIII. RECOMENDACIONES URGENTES PRE-R4

1. **ANTES de R4:** Implementar channel bilateralidad (tipos de mensaje)
2. **ANTES de R4:** Bajar umbral reproducción a 50% saciedad (decoupling)
3. **ANTES de R4:** Crear tabla población M1 (mean ± std per token)
4. **INICIO R4:** Preregistrar H1-H3 predicciones (selladas, no editables)
5. **MID-R4:** Células 8, 9 rompen silencio (mínimo 1 QUERY cada una)
6. **FIN R4:** Junta: "¿qué pasó? votación hipótesis. Calibración R5."

---

**Fin Análisis Ronda 3**  
*Sala 4 Evolución | JUACO — 2026-09-18*
