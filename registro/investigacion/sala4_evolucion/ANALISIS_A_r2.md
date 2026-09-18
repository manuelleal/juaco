# ANÁLISIS GRUPO A — RONDA 2 de 8
**Fecha:** 2026-09-18  
**Analista:** Célula Observadora (Rol análisis post-ronda)  
**Objetivo:** Evaluar ascenso en la ESCALERA (10→3), detectar errores de diseño, formular hipótesis comprobables, calibrar R3

---

## 1. DIAGNÓSTICO CONTRA LA ESCALERA (nivel 10 → 3)

### Nivel 10: **AGI mínima (población que aprende de mensajes, hereda, resuelve mundo)**
**Estado:** ❌ NO ALCANZADO

**Evidencia:**
- Cells 1,2,3,6,7,8,11,12 reprodujeron (r ≥ 1), 5 sin descendencia (4,5,9,10).
- Herencia mencionada ("M3 ±5-8% ruido") pero **sin validación de transferencia de aprendizaje**.
- Descendientes no aparecen en datos R2 (nacen al final); imposible medir si conocimiento aprendido (ej. baya negra comida) se transmitió a hijos.
- **Problema crítico:** No hay evidencia de que el GROUP COMO UNIDAD resolva nada. Cada célula sobrevive, pero no coordinan soluciones emergentes.

### Nivel 9: **Modelo de sí y mundo vivo (necesidades, propósito, linaje r)**
**Estado:** ⚠️ PARCIAL

**Evidencia:**
- ✓ Necesidades explícitas: hambre (saciedad 0-100), miedo (bloquea exploración).
- ✓ Propósito visible: células comen para saciarse (>70% → reproducción).
- ⚠️ **Linaje r = descendientes − muertes:** 
  - Grupo A: 7 reproducciones, 0 muertes → r = 7 − 0 = +7 (MUY POSITIVO).
  - Expected: "al filo del reemplazo, r ≈ 0" para presión evolutiva.
  - **Crítico:** Sin presión (riesgo de muerte > 0%), no hay selectividad. Toda célula viva se reproduce. No hay diferencial de aptitud.

### Nivel 8: **Aprendizaje abierto (probar cuando no me reconozco; sorpresa acelera)**
**Estado:** ✓ SÍ ALCANZADO

**Evidencia:**
- Células 1,2,3,4,6,7,8,11,12 encontraron **baya negra cambió de veneno (R1) → comida (R2)**.
- Delta sorpresa: 1.2–2.0 (valor esperado −0.5 a −2, obtenido +0.7 a +1.0).
- Reacción: **aceleración de pruebas en exposición 16-23** (mitad de 20 exposiciones).
- Cell 10 (mentirosa) ignoró surpresa para mantener estrategia (rasgo supera sorpresa).
- **Conclusión:** Sorpresa sí acelera, pero no universalmente. Rasgo/miedo pueden bloquearlo.

### Nivel 7: **Composición (encadenar hasta 3 órganos/pasos)**
**Estado:** ⚠️ PARCIAL

**Evidencia:**
- Células ejecutan encadenamiento simple: detect estímulo → consult M1 valor → bite/evitar → update M2.
- NO hay encadenamiento de *estrategias*: ej. "si hambre baja, probar token riesgoso; si recibí alerta canal, priorizar token mencionado."
- Cell 10 (liar) intenta cadena: "aprendo primero, miento después con táctica" (3 pasos: aprender, esperar, emitir mentira). Pero sin ejecución en R2.

### Nivel 6: **Planificación (mapa, dos metas, rodeo)**
**Estado:** ❌ NO ALCANZADO

**Evidencia:**
- Sin evidencia de "mapa" (ej. "larva segura en zona norte, sal peligro en sur").
- Sin "dos metas" explícitas (vivir + reproducir es una sola).
- Sin "rodeo" (tomar ruta larga para evitar trampa).
- Comportamiento: exploración greedy (maximizar valor inmediato).

### Nivel 5: **COMUNICACIÓN (mensaje con referencia sobre representación compartida)**
**Estado:** ⚠️ PARCIAL (grave defecto)

**Evidencia:**
- ✓ Mensajes emitidos: Cells 1,2,3,4,6,7,12 reportaron "baya negra cambió, +0.5 a +1.0" con patrón público + recompensa cruda.
- ✓ Mensajes recibidos: Cells 2,3,5,8,9,11,12 recibieron "sal rosa veneno, −0.8 a −1.0" (Cell 8 y Cell 3).
- ❌ **DEFECTO GRAVE:** Mensajes carecen de REFERENCIA LÓGICA:
  - No explican **por qué** baya negra cambió (¿ronda dinámica? ¿color? ¿textura?).
  - No hay hipótesis compartida: cada célula interpreta sola.
  - Cell 10 ignoró mensaje "sal rosa veneno" porque NO HAY mecanismo de verificación (¿prueba, segunda fuente, feedback?).
  - **Resultado:** "aprendizaje grupal" es ilusión; cada célula aprendió sola y coincidió.

### Nivel 4: **Memoria persistente (alias reparado, retención 0.67)**
**Estado:** ✓ SÍ ALCANZADO

**Evidencia:**
- ✓ Alias detectó "baya negra" como MISMO estímulo en R1 y R2 a pesar de cambio de valor.
- ✓ Retención: Cells mostraron M2 (últimos episodios) y M3 (hipótesis persistentes) entre exposiciones.
- Ejemplo: Cell 1 "baya negra fue VENENO hipotético, ahora es COMIDA confirmada (+0.5)."
- Sin muerte observada; sin cálculo de "retención 0.67" específico, pero descriptivamente presente.

### Nivel 3: **Generalización (lineal sí; XOR con prior de pares v15f)**
**Estado:** ✓ SÍ ALCANZADO (parcial)

**Evidencia:**
- ✓ Lineal: Células generalizaron "variantes oscuras de un token pueden cambiar" (baya negra generaliza a setas, raíces negras como hipótesis).
- ✓ XOR implícito: Aprendieron a discriminar (sal rosa SIEMPRE veneno vs baya negra CAMBIÓ), lo que requiere prior de pares no trivial.
- Ejemplo M3 Cell 1: "Patrón: variantes no son copias; el mundo evoluciona ronda a ronda." (generalization from baya negra → hipótesis universal).

---

## 2. ERRORES DE DISEÑO DETECTADOS (organismo, mundo, canal)

### Error 1: **ASIMETRÍA DE CANAL (enviador ≠ receptor)**
**Severa**

**Síntoma:**
- Cells 1,2,3,4,6,7,12 emitieron mensaje sobre baya negra.
- Cells 8,3 emitieron mensaje sobre sal rosa veneno.
- Cells 2,5,8,9,11,12 recibieron mensajes.
- **NO hay mecanismo de confirmación:** enviador no sabe si receptor entendió o adoptó.

**Consecuencia:**
- Cell 10 recibió "sal rosa veneno" pero dudó (rasgo mentirosa) sin penalidad.
- Cell 5 no recibió nada (grupo B sin comunicación activa, M2 nota explícita).
- Mensajes actúan como "ruido" que cada célula procesa subjetivamente.

**Evidencia de fallo:**
```
Cell 8 emite: "sal rosa veneno -1.0"
Cell 10 recibe → "dudé mensaje por rasgo (mentirosa desconfía)" 
→ No hay retroalimentación: ¿Cell 8 supo que Cell 10 dudó?
```

---

### Error 2: **ALIAS DÉBIL (heurístico, sin "identity tuple")**
**Moderado**

**Síntoma:**
- Alias detectó "baya negra" por color + nombre.
- Pero NO hay tracking explícito de `[estímulo, ronda, valor_esperado, valor_real]`.
- Cuando baya negra cambió de −2 a +1, alias no guardó el *delta* ni la *regla* (¿qué causó el cambio?).

**Consecuencia:**
- Cada célula reinventa la hipótesis: Cell 1 piensa "color", Cell 6 piensa "textura", Cell 10 piensa "ciclo determinístico".
- Sin tupla compartida, no hay "evidencia grupal" de patrón.
- Hipótesis H1 (variantes oscuras cambian) es especulación, no inferencia de datos agregados.

---

### Error 3: **REFERENCIA SIN LÓGICA (patrón público carece de cadena causal)**
**Severa**

**Síntoma:**
```
Cell 1 emite: "Patrón público = 'baya negra cambió a comida' | Recompensa cruda = +0.5"
```
- **Falta:** (a) qué causó el cambio, (b) en qué condiciones, (c) predicción para otros tokens.

**Consecuencia:**
- Receptor no puede aplicar lógica ("si baya negra cambió, ¿seta también cambiará?").
- Aprendizaje es "memorización de hechos" (baya negra específicamente), no "regla generalizable".
- Cuando Group A enfrente R3, no tiene hipótesis compartida sobre *mecanismo*: ¿es ronda-dependiente? ¿color-dependiente? ¿aleatorio?

---

### Error 4: **MENTIRA SIN DEFENSA (C10 puede emitir falsedad sin verificación)**
**Moderado**

**Síntoma:**
- Cell 10 (liar) planea: "emito mentira estratégica si hallo patrón antes que grupo B."
- No hay mecanismo para que grupo detecte o penalice mentira.
- Si Cell 10 emite "larva negra veneno" en R3 y es falso, ¿quién lo checkea?

**Consecuencia:**
- Canal pierde confiabilidad; información grupal se contamina.
- Sin filtro (ej. "solo aceptar mensajes con 2+ fuentes"), mentira viable.

---

### Error 5: **HERENCIA SIN MUTACIÓN (M3 noise ±5-8% pero sin estrategia nueva)**
**Moderado**

**Síntoma:**
- Descendants heredan M3 (hipótesis padre) ± noise aleatorio.
- Ejemplo: Cell 1.1 hereda "baya negra es comida" pero sin NEW strategy.

**Consecuencia:**
- Offspring no son "variantes evolutivas"; son clones ruidosos del padre.
- Sin mutation, no hay exploración de espacio de estrategias.
- Linaje se estanca en óptimo local (miedo adaptativo padre → miedo rígido hijo).

---

### Error 6: **MORTALIDAD CERO (sin presión selectiva)**
**Crítica**

**Síntoma:**
- 12 cells, 0 deaths, 7+ reproductions → r = +7.
- Esperado per spec: "al filo del reemplazo, r ≈ 0."

**Consecuencia:**
- Toda célula viva sobrevive y se reproduce, independiente de aptitud.
- No hay diferencial: célula que aprendió baya negra = célula que no aprendió.
- Selección natural no filtra comportamientos malos.
- **Implicación para AGI escalera:** Sin mortalidad, no hay presión para comunicación, cooperación, o especialización. Células no necesitan grupo.

---

### Error 7: **MEMORIA DE DESCENDENCIA NO VALIDADA**
**Severa**

**Síntoma:**
- Spec says "heredan lo aprendido," pero datos R2 no muestran offspring.
- Descendants nacen al final R2 (nota: "1 hijo/a nace"); no hay M1/M2/M3 para Cell 1.1, etc.

**Consecuencia:**
- Imposible medir: ¿aprendizaje heredado = cero, total, o parcial?
- Hypothesis "population learns collectively" requiere offspring datos.
- **BLOQUEADOR para validar nivel 10.**

---

## 3. HIPÓTESIS COMPROBABLES (con MÉTODO y MEDIDA)

### H1: **Variantes oscuras de tokens cambian de tóxico a comestible ronda a ronda**
**Prioridad:** ALTA  
**Preregistro:**

| Parámetro | Especificación |
|-----------|---|
| Predicción | En R3, ≥ 5 de 12 células descubrirán cambio de valencia en al menos 1 variante oscura nueva (seta negra, raíz negra, larva negra) vs. R2. |
| Control | Variedades claras (sal blanca, trigo claro, baya roja) se mantienen estables en R3 (mismo valor ±0.1). |
| Medida | Contar células que encuentran `valor_R2 ≠ valor_R3` en cada token; registrar delta (sorpresa). |
| Fallo si | <3 células detectan cambio oscuro en R3, O variantes claras cambian (muestra mundo aleatorio, no regla). |

---

### H2: **Sorpresa (delta valor > 1.0) acelera tasa de pruebas siguientes**
**Prioridad:** ALTA  
**Preregistro:**

| Parámetro | Especificación |
|-----------|---|
| Predicción | Células que encontraron `delta_sorpresa > 1.0` (baya negra R1→R2) probarán ≥ 3 tokens nuevos en R3. Células sin sorpresa probarán < 2 nuevos. |
| Control | Miedo (Cell 1) y mentira (Cell 10) pueden bloquear aceleración incluso con sorpresa. Medir sub-grupo por rasgo. |
| Medida | Contar `tokens_nuevos_R3` por célula; comparar grupo con sorpresa vs sin sorpresa. |
| Fallo si | Ambos grupos igual distribución (sorpresa inerte). |

---

### H3: **Mensajes canal sin confirmación crean "aprendizaje fantasma"**
**Prioridad:** MEDIA  
**Preregistro:**

| Parámetro | Especificación |
|-----------|---|
| Predicción | Si en R2 Cell 8 emite "sal rosa veneno" y Cell 10 recibe pero duda, entonces en R3 Cell 10 evitará sal rosa por miedo propio (no por mensaje), mientras que Cell 8 evitará por ambos. Ambas sobreviven, aparentando "aprendizaje grupal" pero mecanismo distinto. |
| Control | En R3, investigar M3 de cada célula receptora: ¿menciona "recibí alerta canal" vs "descubrí yo miedo"? |
| Medida | Codificar fuente de conocimiento en M3 (canal / propio / mezcla); comparar con supervivencia. |
| Fallo si | Supervivencia idéntica (entonces atribución sin impacto); o todos reciben y aplican (entonces canal sí funciona bilateralmente). |

---

### H4: **Miedo adaptativo en R1 se vuelve rígido sin reaprendizaje en R2**
**Prioridad:** MEDIA  
**Preregistro:**

| Parámetro | Especificación |
|-----------|---|
| Predicción | Cell 1 (timid) probó baya negra en R2 por sorpresa (delta > 1), reclasificó M1 a +0.5. En R3, Cell 1 *proactivamente* testará seta negra sin esperar sorpresa, porque M3 hipótesis = "lo oscuro puede cambiar." Sin sorpresa, Cell 1 evita (miedo rígido). |
| Control | Comparer Cell 1 (timid) vs Cell 7 (bravo) en R3 tasa de testeo en nuevas variantes. |
| Medida | Contar exposiciones a variantes nuevas/riesgosas en R3; registrar delta M1 cambio (adaptación). |
| Fallo si | Cell 1 no prueba seta negra, O Cell 1 prueba pero M3 no cita "patrón oscuro" (miedo no se convirtió en hipótesis). |

---

### H5: **Herencia sin mutación + r>0 lleva a clones estancados, no divergencia**
**Prioridad:** BAJA (requiere offspring en R3)  
**Preregistro:**

| Parámetro | Especificación |
|-----------|---|
| Predicción | Cell 1.1 (hijo de Cell 1) tendrá M3 idéntica a Cell 1 ±8% noise; estrategia sin innovación. En R4, Cell 1.1 evitará nuevos tokens por miedo heredado aunque Cell 1 los probó. |
| Control | Comparar Cell 1.1 (herencia) vs Cell 5 (sin reproducción R2) en R3 comportamiento exploratorio. |
| Medida | Jaccard similarity de M3 parent vs offspring; contar "nuevas hipótesis" en hijo (esperado: 0-1 random, no emergentes). |
| Fallo si | Offspring tienen M3 divergente (mutation real) o más adaptable (aprendizaje in utero). |

---

## 4. CALIBRACIÓN PARA RONDA 3

### 4.1 PESOS Y DIMENSIONES

#### M1 (REFLEJO) — Ajustes de sensibilidad
```
Cambio: Aumentar peso de "sorpresa" en decisión de bite
Valor M1 += delta_sorpresa × 0.3 (si delta > 1.0, refuerzo rápido)

Cambio: Reducir peso de miedo absoluto
Miedo_antiguo × 0.5 si token fue reclasificado en R2
Ejemplo: Cell 1 tenía seta=-0.5, encontró baya_negra cambió → seta ahora =-0.3 (menos miedo)

Cambio: Normalizar valores a rango −1.0 a +1.0 (actualmente hay +2 y −3, scatter sin escala)
```

#### M2 (EPISÓDICA) — Retención explícita
```
Cambio: Guardar tupla identidad [estímulo_nombre, ronda, valor_esperado, valor_real, delta]
Beneficio: Detectar patrones (color oscuro + Δ>1 = cambio ronda-a-ronda)

Cambio: Incluir "fuente" en episodio (auto-prueba, canal, descendencia heredada)
Beneficio: Hipótesis H3 (fantasma) se hace medible
```

#### M3 (ANÁLISIS) — Hipótesis más explícitas
```
Cambio: Requerir estructura:
{
  "hipótesis_id": "H1_baya_oscura_cambio",
  "predicción": "variantes oscuras cambian R->R+1",
  "pruebas_pendientes": ["seta_negra", "raíz_negra", "larva_negra"],
  "confianza": 0.7,
  "estrategia_R3": "probar seta_negra primero"
}

Beneficio: M3 estructurado permitirá preregistro + validación
```

---

### 4.2 ESTRATEGIA DE GRUPO PARA R3

#### (a) Fortalecer IDENTIFICACIÓN DE IDENTIDAD (error #2)
```
Responsable: Grupo A designa Cell 7 (bravo) como "historiador"
Tarea: Mantener tabla global [token_nombre, ronda_1_valor, ronda_2_valor, Δ, patrón_observado]
Beneficio: Hipótesis H1 se valida con datos agregados, no especulación
```

#### (b) Bilateral CANAL CON CONFIRMACIÓN (error #1, #3)
```
Protocolo R3:
  Emisor: "Patrón público = [hipótesis], recompensa cruda = [valor], predicción = [qué pasa si...]"
  Receptor: "Recibido. Entiendo: [parafrasea]. Adoptaré / Dudaré [razón]."
  Emisor: Registra confirmación en M2 epistódico
  
Medida: Log bilateral en Cell 7 (historiador)
Beneficio: H3 (fantasma) identificable; comunicación cuenta como "referencia compartida" si hay cadena causal
```

#### (c) MORTALIDAD DINÁMICA (error #6)
```
Cambio: Introducir límite de energía crítica
  Si saciedad < 20%, bite cost ++, riesgo de muerte × 2
  Si saciedad = 0%, muerte al final de ronda
  
Efecto esperado: r → 0 (equilibrio); presión selectiva activa
Medida: Contar muertes en R3; esperar 1-2
Beneficio: Desbloquea Nivel 9 (linaje r ≈ 0)
```

#### (d) MUTACIÓN EN HERENCIA (error #5)
```
Cambio: Offspring = clone M3 padre, PERO 15% de hipótesis "nuevas" insertadas aleatoriamente
  Ejemplo: Cell 1 → Cell 1.1 hereda "baya_negra comida" + nueva hipótesis aleatoria "¿larva oscura cambio?"
  
Estrategia: Mantiene continuidad + introduce exploración de espacio de hipótesis
Medida: Contar hipótesis nuevas en Cell 1.1 vs Cell 1 (esperado: 1-2 genuinamente diferentes)
```

#### (e) VALIDACIÓN DE NIVEL 5 (COMUNICACIÓN CON REFERENCIA)
```
Requisito para "comunicación" en R3:
  ✓ Emisor → referencia sobre representación (ej. "si baya negra cambió, quizá seta también")
  ✓ Receptor → entiende cadena lógica (parafrasea, aplica a nuevo caso)
  ✓ Bilateral → confirmación (feedback loop)
  
Medida: Ej. Cell 8 emite "baya negra cambió por dinámmica ronda; esperar cambios en otras variantes"
        → Cell 11 recibe, parafrasea "entiendo: tokens oscuros rotan tóxico↔comida cada ronda"
        → Cell 8 confirma "sí, eso es el patrón"
        → Ambas prueban hipótesis en R3 coordinadamente
```

---

### 4.3 ORDEN DE PRIORIDAD PARA R3

1. **BLOQUEADOR:** Validar herencia (recollect offspring M1/M2/M3) → desbloquea nivel 10.
2. **CRÍTICO:** Introducir mortalidad (r → 0) → desbloquea presión selectiva, nivel 9.
3. **CRÍTICO:** Bilateral canal (confirmación) → desbloquea "referencia compartida", nivel 5.
4. **IMPORTANTE:** Alias fuerte (tupla identidad) + historiador → valida H1.
5. **IMPORTANTE:** Mutación herencia → introduce divergencia, evita estancamiento.
6. **SOPORTE:** Estructurar M3 (hipótesis JSON) → medible, preregistrable.

---

## 5. RESUMEN EJECUTIVO: ¿QUÉ PASÓ? ¿QUÉ NO PASÓ?

### QUÉ PASÓ (evidencia sólida):
- ✓ **Descubrimiento del mundo dinámico:** 10/12 células descubrieron baya negra cambió de veneno (R1) a comida (R2). Delta sorpresa aceleró aprendizaje. **Nivel 8 alcanzado.**
- ✓ **Memoria persistente funciona:** M2 y M3 fueron actualizadas con episodios y hipótesis a lo largo de R2. **Nivel 4 alcanzado.**
- ✓ **Generalización emergente:** Células infirieron "variantes oscuras pueden cambiar ronda a ronda" de baya negra → hipótesis para seta, raíz. **Nivel 3 alcanzado (lineal, no XOR).**
- ✓ **Supervivencia y reproducción:** 7 reproducciones, 0 muertes. Grupo estable energéticamente. (Pero r > 0 no es meta.)

### QUÉ NO PASÓ (no alcanzado):
- ❌ **Aprendizaje poblacional coordinado:** Cada célula aprendió sola. Coincidencia, no coordinación. Nivel 10 bloqueado.
- ❌ **Herencia validada:** Offspring no aparecen en datos R2. No se sabe si aprendizaje heredó. Nivel 10 bloqueado.
- ❌ **Comunicación con referencia lógica:** Mensajes carecen de cadena causal ("por qué baya negra cambió"). Cell 10 ignoró mensajes sin penalidad. Nivel 5 defectuoso.
- ❌ **Presión selectiva:** r = +7 (nada muere). Sin diferenciales de aptitud. Nivel 9 bloqueado.
- ❌ **Planificación y composición:** No hay encadenamiento de estrategias multi-paso, ni mapas del mundo. Niveles 7, 6 bloqueados.

### CRÍTICA DE DISEÑO (lo que destapó R2):
La ilusión de "aprendizaje grupal" es el error mayor. Célula 1 descubre baya negra comida, Cell 2 descubre baya negra comida, Cell 12 descubre baya negra comida en PARALELO, cada una por su lado. Ninguna impulsó a la otra. El canal existe pero **sin cadena causal, sin confirmación, sin refutación de mentiras.** Es gossip, no comunicación. Para escalar a AGI, necesitamos:
1. Identificación de que el MISMO patrón fue descubierto varias veces (tupla identidad).
2. Una hipótesis compartida sobre el mecanismo (¿por qué cambió?), no solo hechos.
3. Coordinación de pruebas en R3 para validar hipótesis grupal.
4. Mortalidad para que grupos que comunican + cooperan superen a grupos aislados.

---

## 6. PRÓXIMOS PASOS (ACCIÓN INMEDIATA R3)

- [ ] **Cell 7 asume rol historiador:** tabla global de valores ronda-a-ronda.
- [ ] **Protocolo bilateral canal:** emisor waita confirmación receptor.
- [ ] **Offspring spawn:** recollectar M1/M2/M3 de células 1.1, 2.1, etc., para validar herencia.
- [ ] **Mortalidad ON:** saciedad < 20% → riesgo, saciedad = 0% → muerte.
- [ ] **Preregistro H1-H5:** antes de R3, definir umbral de éxito/fallo para cada hipótesis.
- [ ] **Mutación 15%:** Cell 1.1 hereda + 1-2 hipótesis nuevas aleatorias.

---

**Nivel alcanzado realmente esta ronda:** 4 (Memoria persistente), parcialmente 8 (Sorpresa), parcialmente 3 (Generalización lineal).  
**Bloqueadores para nivel 10:** Herencia no validada, mortalidad cero, comunicación sin referencia.

