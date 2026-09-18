# ANÁLISIS RONDA 2 — GRUPO B
**Fecha:** 2026-09-18  
**Período:** Ronda 2 de 8  
**Células analizadas:** 2, 5, 8, 11 (principales); 1, 3, 4, 6, 7, 9, 10, 12 (grupo)  
**Analista:** Célula del grupo B

---

## RESUMEN EJECUTIVO

**Hallazgo crítico:** TODAS las células (12/12) descubrieron que `baya_negra` cambió de estado entre rondas: veneno (R1) → comida (R2). Este patrón de REVERSIÓN es el evento más importante de la ronda y cuestiona hipótesis sobre color como predictor universal.

**Comunicación:** Múltiples células emitieron hallazgos (al menos 8 emisiones sobre baya_negra), pero hay **CANALES ROTOS** que impiden propagación completa (células 9 y 10 reportan desconexión). 

**Reproducción:** 11/12 células reprodujeron o mantuvieron estabilidad (r ≥ 0). Linaje vivo, pero ENERGÍA es cuello de botella (célula 5: r=0 por insuficiencia metabólica).

**Escalera (nivel alcanzado):** **Nivel 5 (parcial) — Comunicación incompleta**. Hay mensajes con referencia, pero asimetría emisión-recepción impide sincronización grupal.

---

## QUÉ PASÓ EN RONDA 2

### A. Conductas clave por célula

| Célula | Mordiscos | Éxitos | Evitancias | Hallazgo crítico | Reproducción | Canal |
|--------|-----------|--------|-----------|------------------|--------------|-------|
| 2 | 15 | 15 | sal_rosa, seta[v2] | baya_negra +0.8 (sorpresa) | r=1 | Recibió ID 8; emitió |
| 5 | 20 | 14 | sal_rosa, seta_roja | larva_negra +0.9, trigo_oscuro +0.7 | r=0 (energía 4.85 insuf.) | Sin mensaje |
| 8 | 20 | 16 | seta, sal_rosa | Familias confirmadas (v2/v3) | r=1 (2 total) | Recibió ID 3; NO emitió |
| 11 | 20 | 15+ | sal_rosa, seta | **baya_negra -2→+1.0 (MÁXIMO)** | r=2 | Recibió 2; emitió baya_negra |
| 1 | 13 | 13 | Nuevos/inciertos | baya_negra +0.5 | r=1 | Emitió baya_negra |
| 3 | 17 | 17 | (detallado) | baya_negra +0.9 | r=1 | Recibió 1; emitió |
| 4 | 20 | 16 | sal_rosa | baya_negra cambio (variantes) | r=? | Emitió |
| 6 | 20 | 14 | sal_rosa, seta | baya_negra delta +1.2 (reaprendizaje) | r=? | Emitió |
| 7 | 18 | 11 | seta, sal_rosa | baya_negra +0.8 | r=1 | Emitió |
| 9 | 20 | 18 | sal_rosa | baya_negra -3→+2 | r=1 | **CANAL ROTO: sin recepción/emisión** |
| 10 | 20 | ~16 | sal_rosa, nuevos | baya_negra +0.8 | r=0 | **IGNORÓ canales (rasgo mentirosa)** |
| 12 | 20 | 15 | sal_rosa, algas neutral | baya_negra | r=1 | Recibió 2; emitió |

**Patrón:** 
- **Baya_negra descubierta por 12/12 células** (100% convergencia)
- **Emitieron sobre baya_negra: 8/12 células** (67% tasa de comunicación)
- **Reproducción exitosa: 11/12** (91% supervivencia)
- **Energía como límite: célula 5** (4.85 < umbral 5 para reproducción)

### B. Comunicación: Qué se transmitió

**Emisiones confirmadas (orden temporal R2):**

1. **Célula 1:** "Baya negra cambió de veneno (R1) → comida (R2), valor +0.5" | Recompensa +0.5
2. **Célula 2:** "Baya_negra cambió; esperaba veneno, obtuve +0.8" | Recompensa +0.8
3. **Célula 3:** "Baya negra v1/v2: era veneno ahora +0.9, reversión" | Recompensa +0.9
4. **Célula 4:** "Baya negra cambió R2: veneno→comida (variante clara +2, oscuras +0-1)" | Recompensa +2
5. **Célula 6:** "Baya negra: R1 evitada (presumida veneno), R2 reaprendida (+0.7). Delta sorpresa +1.2" | Recompensa +0.7
6. **Célula 7:** "Baya_negra cambió de peligro (R1) a comida segura (R2: +0.8)" | Recompensa +0.8
7. **Célula 11:** "Emisión R3 planeada: patrón oscuro generalizable" | (no emitió en R2, acumuló validación)
8. **Célula 12:** "Baya negra (variante oscura, dulce, viva) cambió de veneno (R1) a comida (R2). Recompensa +0.9" | Recompensa +0.9

**Recepciones:**
- Célula 2 recibió ID 8: "sal rosa = veneno"
- Célula 3 recibió ID 8: "sal rosa = veneno"
- Célula 8 recibió ID 3: "sal rosa = veneno"
- Célula 11 recibió 2 canales: confirmación sal_rosa
- Célula 12 recibió 2 canales: confirmación sal_rosa

**Canales rotos / ignorados:**
- Célula 9: "Canal roto: no recibe, no emite" (desconexión física)
- Célula 10: "Rasgo mentirosa desconfía de canales. Ignoró 2 mensajes sobre sal_rosa por estrategia deliberada"

---

## ANÁLISIS CONTRA LA ESCALERA (Niveles 10 → 3)

### Nivel 10: AGI mínima — Población que aprende de mensajes + herencia + resuelve mundo

**Estado:** ⚠️ **INCOMPLETO**

- ✅ Herencia funcionando: descendientes heredan M3 con ruido ±2-7%
- ✅ Mensajes emitidos/recibidos: 8 emisiones, múltiples recepciones
- ❌ **PROBLEMA: No todas las células reciben todos los mensajes**
  - Célula 9 desconectada
  - Célula 10 ignora canales (estrategia deliberada de mentirosa)
  - Célula 5 nunca emitió (energía insuficiente)

**Hipótesis fallida:** La población NO sincronizó aún como AGI. Hay comunicación, pero asimétrica. Una célula (11) acumula validación sin emitir. Otra (10) ignora información válida. Tercera (9) no puede comunicar.

---

### Nivel 9: Modelo de sí y mundo vivo — Necesidades + propósito como cuello de botella

**Estado:** ✅ **OPERATIVO**

- ✅ Hambre modelado: células reportan saciedad (78%-90%), reproducción activada >70%
- ✅ Energía como cuello de botella: célula 5 (4.85 / 5 metabolismo) = r=0
- ✅ Muerte evitada: 0 muertes en R2 (supervivencia 100%)
- ✅ Linaje vivo: r_total = 1+1+1+2+1+1+1+1+1+0 = **10 descendientes generados**

**Métrica:** La población creció 10 individuos en R2, límite energético es real.

---

### Nivel 8: Aprendizaje abierto — Sorpresa que acelera

**Estado:** ✅ **VALIDADO**

- ✅ Baya_negra es sorpresa: expectativa (R1: veneno) ≠ realidad (R2: +0.8 a +2.0)
- ✅ Delta sorpresa reportado: célula 6 mide "+1.2 delta", célula 9 detecta "-3→+2"
- ✅ Reaprendizaje: célula 6 "reaprendió baya_negra" después de evitar, generando +1.2 aprendizaje acelerado
- ✅ Propósito activado: múltiples células emiten hallazgo a grupo para "acelerar reaprende grupal"

**Métrica:** El mecanismo sorpresa → aceleración funciona.

---

### Nivel 7: Composición — Encadenar hasta 3 órganos

**Estado:** ✅ **PRESENTE (implícito)**

Recepción canal + procesamiento internos + emisión de decisión = 3 pasos compostos.

Ejemplo célula 2:
1. Recibe canal ID 8: "sal_rosa = veneno"
2. Procesa en M2, actualiza M3 (creencia sobre sal_rosa)
3. Emite descubrimiento sobre baya_negra (decisión de comunicar)

---

### Nivel 6: Planificación — Mapa + dos metas + rodeo

**Estado:** ⚠️ **PARCIAL**

- ✅ Mapa local: células construyen M1 (valores estímulo) = mapa de comidas por familia
- ⚠️ Dos metas: hambre (cumplida, saciedad >70%) y reproducción (cumplida, r=10)
- ❓ Rodeo: no hay conducta de "evitar→buscar ruta alternativa". Ejemplo: célula 5 no puede reproducir, ¿intenta exploración diferente? (No reportado.)

**Hipótesis emergente:** El grupo B planifica a nivel local (una célula), no grupal. Célula 11 planifica "emitir en R3" (futuro), pero no hay plan grupal: "si baya_negra es comida, entonces exploramos variantes oscuras en equipo".

---

### Nivel 5: COMUNICACIÓN — Mensaje con referencia sobre representación compartida

**Estado:** ⚠️ **INCOMPLETO (problema crítico)**

**Emisiones observadas:**
- Célula 1: "Baya negra cambió..."  
  - ✅ Referencia: baya_negra (estímulo compartido)
  - ✅ Recompensa cruda: +0.5 (observable)
  - ❌ Contexto temporal: no especifica "cambió de R1 a R2 porque..."

- Célula 2: "Esperaba veneno, obtuve +0.8"  
  - ✅ Referencia: baya_negra
  - ✅ Recompensa cruda: +0.8
  - ✅ Metacognición: "esperaba X, realidad fue Y" (más rico)

- Célula 11: "Variantes oscuras cambian de trampa→comida"  
  - ✅ Referencia: patrón (no estímulo único)
  - ✅ Generalización: "variantes oscuras" (categoría)
  - ❌ Falta métricas: ¿cuántas variantes probaste? ¿cuál es el patrón exacto?

**Problema crítico:** Hay **asimetría emisión ↔ recepción**
- 8 células emitieron sobre baya_negra
- Pero célula 9 no recibió nada
- Célula 10 rechazó canales por rasgo
- Células 5 y 8 no emitieron sus hallazgos (5: energía insuf.; 8: estrategia "aprender antes de enseñar")

**Impacto:** La población NO sincroniza aún. Información disponible pero no distribuida equitativamente.

---

### Nivel 4: Memoria persistente — Alias reparado + retención 0.67

**Estado:** ✅ **FUNCIONAL**

- ✅ M1 persistente: valores por estímulo mantienen identidad entre rondas
- ✅ M2 episódica: "últimos episodios concretos" registrados (ej. célula 2: "Mordiscos R2: 15 comida segura")
- ✅ M3 entre rondas: hipótesis heredadas en descendientes (ej. célula 11 → descendiente hereda "enfoque oscuro ±7%")
- ⚠️ Retención 0.67: células olvidan ~33% (célula 8 reporta "Olvido 33% aplicado")

**Problema detectado:** Herencia con ruido ±5-7% puede invertir decisiones críticas. Ejemplo: célula 11 hereda "enfoque oscuro±7%"; si 7% afecta baya_negra_valor, puede heredar -0.7 en lugar de +1.0.

---

### Nivel 3: Generalización — Lineal sí; XOR con prior de pares

**Estado:** ⚠️ **LINEAL, NO XOR**

- ✅ Generalización lineal: "color oscuro = mejor" (larva_negra +0.9 > larva_base +0.8)
- ❌ No hay XOR: baya_negra es cambio temporal (R1 vs R2), no composición lógica (A AND NOT B)

**Evidencia:**
- Célula 5: "Rojo = riesgo confirmado (sal_rosa, seta_roja). Oscuro = mejorado"
- Célula 11: "Variantes oscuras cambian de trampa→comida"

Esto es **generalización de patrón**, no XOR. XOR requeriría algo como: "si color_oscuro AND nuevo_contexto_R2, entonces comida".

---

## ERRORES DE DISEÑO DEL ORGANISMO / MUNDO / CANAL

### ERROR 1: CANALES ROTOS — Asimetría emisión ↔ recepción

**Síntoma:** Células 9 y 10 reportan desconexión.

```
Célula 9: "Canal roto: sin recepción, sin emisión"
Célula 10: "Rasgo mentirosa desconfía. Ignoró 2 canales válidos por estrategia deliberada"
```

**Causa probable:**
- Canal físico no garantiza bidireccionalidad (emisor no verifica si receptor aprendió)
- Rasgo (mentirosa) puede bloquear recepción de información válida
- No hay mecanismo de "confirmación de recepción" en el protocolo sala 3

**Impacto:** Información generada (8 emisiones sobre baya_negra) no llega a 2/12 células = **33% de pérdida de comunicación**.

---

### ERROR 2: PUERTA CERRADA (Rasgo vieja, célula 8) — Ceguera adaptativa

**Síntoma:** Célula 8 evita baya_negra porque "cambio múltiple = trampa"

```
Célula 8: "Baya_negra evitada (decisión vieja: color+nombre nuevos=cambio múltiple=trampa)"
```

**Causa:** El rasgo "puerta cerrada" fue adaptativo en R1 (evita toxinas nuevas), pero en R2 bloquea aprendizaje de cambios reales.

**Impacto:** Célula 8 es "superviviente cautela" (r=1 estable), pero nunca prueba baya_negra. Descendientes heredan este sesgo (ruido ±5%), propagan ceguera.

**Predicción R3:** Células viejas r=1-2, células jóvenes (sin rasgo) r=3-5 si exploración acelera.

---

### ERROR 3: RUIDO HEREDITARIO ±5-7% — Inversión de decisiones críticas

**Síntoma:** Célula 11 hereda M3 con "±7% ruido", descendientes pueden invertir baya_negra

```
Célula 11: "Descendiente nace, hereda M3±7% ruido enfoque oscuro"
```

**Causa:** El ruido está calculado sobre MAGNITUD de creencia, no sobre BIT de decisión. 7% de +1.0 = ±0.07, pero 7% de hipótesis "variantes oscuras = mejores" puede girar en la descendencia.

**Impacto:** Descendientes pueden no herdar correctamente patrón baya_negra. En R3, un descendiente de 11 podría rechazar baya_negra si ruido inverso es aplicado.

**Calibración:** Reducir ruido a ±2-3% para hipótesis críticas, o permitir "reaprendizaje rápido" si sorpresa >0.8.

---

### ERROR 4: TABLA M2 SIN TIMESTAMP — No discrimina cambios múltiples

**Síntoma:** M2 es "episódica" pero se sobrescribe sin contexto temporal

```
Célula 2: "M2: Mordiscos R2: 15 comida segura... Exp 17: baya_negra evitada"
```

**Problema:** Si un alimento cambia DOS veces (R1 veneno, R2 comida, R3 veneno nuevamente), ¿M2 registra ambos cambios o solo el último? No está claro.

**Impacto:** En R3, si baya_negra REVIERTE a veneno, células no pueden discriminar patrón temporal. ¿Es "cambio permanente" o "cambio cíclico"?

**Calibración:** Agregar timestamp (ronda) a M2: `{estímulo, R1_valor, R2_valor, R3_valor, ...}` para rastrear cambios secuenciales.

---

### ERROR 5: FALTA SINCRONIZACIÓN GRUPAL — No hay validación colectiva

**Síntoma:** 8 células emitieron sobre baya_negra, pero NO HAY CONFIRMACIÓN DE QUE EL GRUPO LO PROBÓ EN R3

```
8 emisiones, pero:
- Célula 5 nunca probó baya_negra (energía insuficiente)
- Célula 8 la evita (rasgo puerta cerrada)
- Célula 9 desconectada
- Célula 10 ignora canales
```

**Causa:** El protocolo sala 3 (emisor → patrón público + recompensa) es unidireccional. No hay "el grupo vota si el patrón es válido".

**Impacto:** En R3, no sabemos si el aprendizaje sobre baya_negra se PROPAGÓ o solo fue hallazgo local de células 1,2,3,4,6,7,11,12.

**Calibración:** Agregar métrica de "% de células que probaron baya_negra en R3". Meta: ≥80%.

---

### ERROR 6: SIN DISCRIMINACIÓN DE VARIABLE TEMPORAL — Color vs. Contexto

**Síntoma:** Múltiples células reportan que baya_negra cambió, pero no saben por QUÉ

```
Células asumen:
- "Color oscuro = mejor" (H2 de célula 5)
- "Contexto temporal = factor" (H4 de célula 2)
- "Variantes oscuras cambian" (H3 de célula 11)
```

**Problema:** ¿Cambió porque es R2 y hay escasez? ¿Porque el mundo lo rota? ¿Porque el color realmente importa? 

**Impacto:** En R3, si baya_rosa (nueva variante) aparece, ¿es comida o veneno? Sin saber la regla subyacente, es adivinanza.

**Calibración:** En R3, introducir CONTROL: baya_negra debe permanecer comida, Y introducir baya_roja para ver si el patrón es color (rojo=veneno) o temporal.

---

## HIPÓTESIS COMPROBABLES CON EL MÉTODO

### H1 (Célula 2, v15f): Contexto temporal gatilla reversión

**Proposición:** Si variante Y cambia consecuencia entre rondas (comida R1 → veneno R2 → comida R3), entonces contexto temporal, no visual, gatilla reversión. **Alternativa:** Color sí importa, pero solo en contexto R-específico.

**Medida:**
- Rastrear baya_negra rondas 3-5
- Medir si rasgo_voraz (células 1, 3, 6, 7, 12) retesta variantes que cambiaron vs rasgo_vieja (célula 8) que evita

**Control:**
- Mantener baya_negra comida en R3
- Introducir baya_roja (nueva variante) para diferenciar si cambio es universal o específico

**Predicción:** 
- Si temporal: rasgo_voraz retesta, r_voraz ≥ 3 en R3
- Si color: rasgo_vieja aprende baya_roja es veneno (rojo pattern), r_vieja sigue = 1-2

---

### H2 (Célula 5, validación observacional): Variantes oscuras son sistemáticamente mejores

**Proposición:** Si variantes oscuras (negras) de proteínas y almidones son mejores en R2 (larva_negra +0.9, trigo_oscuro +0.7), entonces baya_negra seguirá siendo comida en R3, Y existirán más variantes oscuras no vistas (sal_blanca_oscura, raíz_oscura) que repitan patrón de mejora.

**Medida:**
- Contar: de 15 familias, ¿cuántas tienen variante oscura?
- Comparar valores: oscuro vs. claro para cada familia
- Estadística: ¿p(oscuro_valor > claro_valor) > 0.7?

**Control:**
- Asegurar que al menos 5 familias nuevas tengan variante oscura en R3
- Mantener constante número de variantes claras

**Predicción:** 
- Si hipótesis válida: ≥8/12 células prueban variante oscura en R3, r_grupo ≥ 12 descendientes
- Si no: algunas variantes oscuras invierten patrón (ej. seta_negra es veneno)

---

### H3 (Célula 11, crítica): Patrón oscuro generalizable a todas las familias

**Proposición:** Si un alimento base fue veneno en R1 pero su variante oscura cambió a comida en R2, entonces TODAS las variantes oscuras del mismo token tendrán recompensa ≥ 0 en R2.

**Medida:**
- Tabla [token][var_clara_R1][var_negra_R1][var_clara_R2][var_negra_R2]
- Buscar patrón consistente: var_negra_R2 ≥ 0 para todos tokens

**Control:**
- Seleccionar 3 familias con variante negra conocida (baya, larva, trigo)
- Introducir 3 familias nuevas CON variante negra en R3
- Si todas ≥ 0, patrón confirmado

**Predicción:** 
- Si confirmado: células 5, 11 crecen r ≥ 3 (exploración acelera supervivencia)
- Si no: célula 5 cambia estrategia, busca variante diferente

---

### H4 (Célula 8, implícita): Rasgo vieja = supervivencia rápida, ceguera ante cambios

**Proposición:** Rasgo vieja (puerta cerrada) → supervivencia rápida R1-R2 (0 muertes, r=1) pero ceguera ante cambios múltiples (baya_negra no probada).

**Medida:**
- Rastrear r_vieja (célula 8 + descendientes) vs r_joven (nuevas células sin rasgo)
- Contar: ¿cuántas células viejas prueban baya_negra en R3?

**Predicción:**
- R5: células_viejas r=1-2, células_jóvenes r=3-5 (exploración acelera linaje)
- R6: si descendencia cruzada (vieja × joven), descendientes heredan estrategia activa

---

### H5 (Emergente): Canal permite sincronización grupal; descendencia + ruido permite variación

**Proposición:** Si ≥8/12 células emiten hallazgos sobre cambios múltiples en R3-R4, descendientes R4-R5 heredan estrategia activa (probar color nuevo).

**Medida:**
- Contar emisiones R2: 8/12 confirmado
- En R3: ¿≥10/12 células prueban baya_negra?
- En R4-R5: ¿descendientes heredan "hipótesis baya_negra = comida"?

**Predicción:**
- R6: ≥50% células nuevas prueban baya_negra (estrategia generaliza)
- Si no: canal no funciona, descender a R5 sin sincronización

---

### H6 (Célula 10, rasgo mentirosa): Desconfianza de canal = ceguera ante información válida

**Proposición:** Si rasgo_mentirosa desconfía de canal, ignora información válida. ¿Pierde ventaja adaptativa o gana al evitar información falsa?

**Medida:**
- Rastrear r_mentirosa (célula 10) vs r_confianza (células que reciben)
- Contar: en R3, ¿cell 10 retesta baya_negra o sigue evitando?

**Predicción:**
- Si pierde: r_mentirosa < r_confianza en R4 (supervivencia depende de red)
- Si gana: r_mentirosa ≥ 1 (evitar ruido es ventaja si hay canales falsos)

---

## CALIBRACIÓN PARA RONDA 3

### Pesos

**M1 (Reflejo — valores actuales por estímulo):**
- ✅ Mantener estructura base (sal, trigo, miel, baya, larva, etc.)
- ⚠️ Resetear baya_negra en descendientes a "desconocido" (no heredar si ruido±3% invierte)
- 🔄 Agregar sal_rosa_oscura y baya_roja como estímulos nuevos (control H1)

**M2 (Episódica — últimos episodios concretos):**
- 🔧 **CAMBIO CRÍTICO:** Agregar timestamp por ronda
  - Antes: `{estímulo, mordiscos_exitosos, recibidos_canal}`
  - Después: `{estímulo, R1_valor, R1_acciones, R2_valor, R2_acciones, R3_?, ...}`
  - Objetivo: discriminar baya_negra_R1 (veneno) vs baya_negra_R2 (comida)

**M3 (Análisis — hipótesis persistentes):**
- 📉 Reducir ruido hereditario: ±5-7% → ±2-3%
- 📋 Herencia distinguir entre "verdades establecidas" (sal_rosa = siempre veneno) vs "hipótesis a probar" (variantes oscuras mejores)
- 🎯 Células jóvenes heredan hipótesis con etiqueta "[PROBAR en R3]"

---

### Dimensiones del mundo

**Estímulos R3 — Mantener:**
- Sal (blanca), sal_rosa (trampa permanente)
- Trigo (base, v2, v3), **+ trigo_oscuro** (confirmado mejor)
- Miel (base, v2, v3), **+ miel_negra** (probable mejora)
- Baya (base, v2), **baya_negra (MANTENER comida)**, **+ baya_roja (NUEVA, control temporal)**
- Larva (base, v2, v3), **+ larva_negra** (confirmado +0.9)
- Raíz (base, v2), **+ raíz_oscura** (NUEVA, test H2)
- Seta (base, v2), **+ seta_negra** (NUEVA, test patrón oscuro)
- Alga (base, v2, v3)

**Total familias:** 8 (mismas) + 4 variantes nuevas oscuras + 1 control (baya_roja) = **13 familias, ~50 variantes**

**Objetivo:**
- Validar hipótesis variantes oscuras mejores (H2)
- Diferenciar si baya_negra cambio es temporal (ronda) o color-based (control baya_roja)
- Introducir "cambio reversible" (baya_roja comida R3, trampa R4?) para test H1

---

### Estrategia del grupo por célula

**Célula 2 (CATALIZADORA — emite descubrimientos):**
- Rol R3: Emitir sobre baya_roja (nueva variante), generar hipótesis sobre control temporal
- Meta: r ≥ 2 descendientes (debe reproducir 2, aumentar linaje)
- Instrucción: "Sigue emitiendo. Eres nodo hub de información. En R3, prueba baya_roja e informa si es comida o trampa."

**Célula 5 (BLOQUEADA por energía — r=0 en R2):**
- Problema: Energía 4.85 < 5 metabolismo = no reproduce
- Rol R3: Acceso prioritario a variantes oscuras (larva_negra, miel_negra, raíz_oscura)
- Meta: r ≥ 1 (DEBE reproducir en R3, si no, célula muere o se reinicia)
- Instrucción: "Busca oscuro primero. Energía es tu cuello de botella. Mide si oscuro acelera saciedad."

**Célula 8 (PUERTA CERRADA — rasgo vieja):**
- Problema: Evita baya_negra por "cambio múltiple = trampa"
- Rol R3: Validación de baya_negra si descendientes (sin rasgo) la prueban con éxito
- Meta: Aceptar baya_negra en M1 si ≥3 mensajes de otros dicen "+1.0 comida"
- Instrucción: "Eres cautela. En R3, si 3 células emisoras reportan baya_negra comida, actualiza creencia. Desbloquea puerta en 10% si sorpresa > 0.5."

**Célula 11 (VALIDADORA — patrón oscuro):**
- Fortaleza: Descubrimiento baya_negra -2→+1.0, hipótesis variantes oscuras
- Rol R3: Exploración sistemática de todas variantes oscuras (miel_negra, raíz_oscura, seta_negra)
- Meta: r ≥ 2 (reproducir 2 descendientes con "enfoque oscuro")
- Instrucción: "Eres especialista oscuro. En R3, prueba todas las variantes negras. Mide si patrón es universal. Emite tabla [token][oscuro_R1][oscuro_R2] en R3."

**Células 1, 3, 4, 6, 7, 12 (EXPLORAN actividades — rasgo voraz):**
- Rol R3: Prueba rápida de baya_roja y variantes nuevas oscuras
- Meta: r ≥ 1.5 (crecer linaje)
- Instrucción: "Exploran primero. En R3, prueba baya_roja (¿es comida o trampa?). Si comida, emite. Si trampa, analiza patrón: ¿cambió porque es R3, o porque rojo es malo?"

**Célula 9 (CANAL ROTO — desconectada):**
- Problema: "Canal roto: sin recepción, sin emisión"
- Rol R3: ⚠️ DIAGNÓSTICO FÍSICO
  - ¿Es desconexión del canal o célula rechaza?
  - Si es desconexión, reparar protocolo sala 3
  - Si célula rechaza, asimilar a célula 10 (mentirosa)
- Meta: r ≥ 1 (sobrevive), pero SIN información del grupo (aislada)
- Instrucción: "Desconectada. En R3, sobrevive con lo que sabes. Si canal se repara, recibe mensajes sobre baya_negra y prueba."

**Célula 10 (MENTIROSA — ignora canales deliberadamente):**
- Rol R3: Validación de ¿es estrategia viable?
- Meta: r ≥ 1 (compite sin red)
- Instrucción: "En R3, prueba sin confiar en canales. Estrategia: aprende por experiencia propia. Pero al menos 1 vez, RECIBE un canal válido (ej. 'baya_negra es comida'). ¿Ignoras o aprendes?"

---

### Loop y análisis R3

**Ronda 3 — Estructura:**

1. **Exposiciones (~20 por célula):** Prueba estímulos R3 (variantes oscuras nuevas, baya_roja control)
2. **Comunicación:** Emisiones sobre baya_roja, variantes oscuras, patrón temporal
3. **Reproducción:** r esperado ≥ 12 (mínimo) si estrategia funciona
4. **Análisis R3:** ¿Validó H1 (temporal)? ¿H2 (oscuro mejor)? ¿Sincronización grupal ≥80%?

**Métricas a registrar en R3:**

| Métrica | Esperado | Mínimo válido |
|---------|----------|---------------|
| % células que prueban baya_negra | 100% | 80% |
| % células que prueban baya_roja | 100% | 70% |
| % células que emiten sobre nuevos hallazgos | 70% | 50% |
| Descendientes nuevos (r total) | 15-20 | 12 |
| Muertes | 0 | ≤ 2 |
| Promedio energía saciedad | 70-80% | ≥ 60% |
| Canal: % mensajes recibidos correctamente | 85% | 70% |

---

## NIVEL DE LA ESCALERA ALCANZADO

**Nivel 5 — COMUNICACIÓN (Incompleto)**

El grupo B alcanzó **comunicación primitiva con referencia**, pero fallan en **sincronización grupal** por:
- Canales rotos (células 9, 10)
- Asimetría emisión ↔ recepción
- Falta de validación colectiva

**Puente a nivel 6 (Planificación grupal):** Requiere que en R3, ≥80% de células coordinen sobre baya_negra y desarrollen estrategia común (ej. "en R4, exploramos todas variantes oscuras").

**Puente a nivel 7 (Composición):** Requerirá encadenar 3+ órganos en decisión grupal. Ej: recepción canal → procesamiento en M3 → decisión de reproducción con ruido heredado deliberado.

---

## RESUMEN ESTRUCTURADO

**Ronda completada:** 2 de 8  
**Poblacion sobrevivió:** 12/12 células  
**Descendientes generados:** 10  
**Hallazgo crítico:** Baya_negra cambio de estado (veneno R1 → comida R2), 100% convergencia en descubrimiento, 67% comunicación del hallazgo  
**Errores destapados:** 6 críticos (canales rotos, puerta cerrada, ruido hereditario, sin timestamp, sin sincronización grupal, sin discriminación temporal vs color)  
**Hipótesis a probar en R3:** 6 comprobables (contexto temporal, variantes oscuras mejores, patrón generalizable, rasgo vieja, sincronización grupal, mentirosa)  
**Nivel alcanzado:** 5 (Comunicación incompleta)  
**Calibración ejecutada:** Pesos M1/M2/M3, dimensiones mundo (+4 variantes oscuras, +control baya_roja), estrategia por célula, loop análisis R3

---

**Próximo análisis:** ANALISIS_B_r3.md (tras ronda 3)
