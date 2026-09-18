# ANÁLISIS RONDA 1 - GRUPO B
## Células (n=12) | Misión: Evolucionar por comunicación + descendencia

**Fecha:** 2026-09-18  
**Analista:** Rol ANÁLISIS (M3 grupal)  
**Escalera:** Dimensionando desde nivel 10 → 3  
**Método:** Conductas observadas, no interpretaciones

---

## I. ¿QUÉ PASÓ Y QUÉ NO PASÓ (ESCALERA 10 → 3)?

### NIVEL 10: AGI mínima (población que aprende de mensajes, hereda, resuelve mundo que una célula sola no resuelve)

**¿QUÉ PASÓ?**
- 12 células exploraron ~16-20 mordidas c/u (total ~200+ exposiciones).
- Encontraron patrón compartido: **sal_rosa cambia de comida → veneno** en ronda 1.
- 2 células emitieron advertencia por canal:
  - **ID 8:** "patrón=sal rosa | estado=comida → realidad=veneno | recompensa_cruda=-1.0"
  - **ID 3:** "sal rosa cambia a veneno (ronda 1)"
- Descubrimiento era **crítico para supervivencia grupal** (8/12 evitaron sal_rosa tras aprenderlo).

**¿QUÉ NO PASÓ?**
- **CANAL ROTO.** Registros explícitos: "Recibí 0 mensajes del canal (grupo aún sin comunicación)" (ID 2, 5, 6, 7, 9, 10, 11, 12).
- ID 8 e ID 3 emitieron, pero **no hay evidencia de que otros lo recibieron y escribieron en tabla**.
- Sin aprendizaje de mensajes → no hay herencia cultural (nivel 10 falla).
- 4/12 reproducción (r=0.33): **linaje débil, población no crece**.
- Aprendizaje ocurrió por **redescubrimiento independiente**, no por transmisión.

**DIAGNÓSTICO NIVEL 10:** FALLIDO. Población no coordina. Cada célula reinventa.

---

### NIVEL 9: Modelo de sí y mundo vivo (necesidades, propósito, linaje r)

**¿QUÉ PASÓ?**
- Necesidades detectadas: hambre/saciedad explícita en todas (M1 reflejos por energía).
- Propósito implícito: sobrevivir (evitar veneno) → reproducir (r ≥ 0).
- Energía acumulada: +5 a +28 por célula (tracking correcto).
- Saciedad alcanzada: 8/12 reportan "saciada" → criterio r ≥ 0 activado.

**¿QUÉ NO PASÓ?**
- Linaje r = 4/12 = 0.33 (muy bajo).
  - Esperado en fase 10: r ≥ 0.5 (mitad repite descendencia).
  - Observado: solo 4 con r=1 (ID 3, 8, 9, 11); 8 con r=0.
- Costo energético por reproducción muy alto o saciedad target inalcanzable.
- Sin descendencia → sin herencia → no hay evolución de estrategia.

**DIAGNÓSTICO NIVEL 9:** PARCIAL. Propósito existe, pero reproducción bloqueada.

---

### NIVEL 8: Aprendizaje abierto (probar cuando no me reconozco, sorpresa acelera)

**¿QUÉ PASÓ?**
- **Exploración voraz:** todas las células exploraron 14-20 tokens/variantes.
- **Sorpresa detectada:** sal_rosa cambió de comida → veneno (inesperado).
  - ID 2: "Saciedad ~70% tras envenenamiento" (miedo aceleró evitación).
  - ID 5: "Detecté cambio sal rosa mid-ronda" → activó estrategia defensiva.
  - ID 8: "Color atractivo ≠ seguridad" (error ≤1 vez, luego evita).
  - ID 10: "Paralizada por miedo exponentes 7-9" (sorpresa → congelación temporal).
- Velocidad de aprendizaje: sorpresa **aceleró desaprendizaje del valor inicial** en 6/12.

**¿QUÉ NO PASÓ?**
- Desaprendizaje incompleto. Ninguna célula reporta "ahora entiendo por qué sal rosa cambió".
- No hay **replan del modelo del mundo** (ej: "Mundo tiene trampas que cambian").
- ID 10 menciona "patrón color=seguridad" pero no prueba (ronda 2 testing).

**DIAGNÓSTICO NIVEL 8:** PARCIAL. Sorpresa acelera evitación, pero no generalización.

---

### NIVEL 7: Composición (encadenar hasta 3 órganos/pasos)

**¿QUÉ PASÓ?**
- Ninguna conducta de composición documentada.
- Todas las células actúan reacciones simples: estímulo (ve token) → acción (muerde/evita).

**¿QUÉ NO PASÓ?**
- No hay "busca comida, luego ve si es trampa, luego muerde" (3 pasos encadenados).
- No hay "emite advertencia, espera respuesta, entonces decide si reproducir" (composición social).

**DIAGNÓSTICO NIVEL 7:** FALLIDO (no alcanzado esta ronda).

---

### NIVEL 6: Planificación (mapa, dos metas, rodeo)

**¿QUÉ PASÓ?**
- **Mapas detectados:**
  - ID 5: "Mapa: 7 seguros, 2 tóxicos, 1 desconocido (variantes oscuras)" (representación interna).
  - ID 8: "Vía rápida activada para familias confirmadas" (priorización implícita).
- **Dos metas implícitas:** sobrevivir (evitar sal_rosa) + reproducir (acumular energía).
- ID 5 planifica: "Estrategia próxima: buscar patrón color" (anticipación).

**¿QUÉ NO PASÓ?**
- No hay "rodeo" (ruta indirecta para resolver conflicto).
- No hay mapa de **dónde están otros** (sin modelo de grupo).
- Planificación es reactiva ("probaré si rosa cambia"), no preventiva.

**DIAGNÓSTICO NIVEL 6:** INCIPIENTE. Mapas simples, metas, pero sin rodeo.

---

### NIVEL 5: COMUNICACIÓN (mensaje con referencia sobre representación compartida)

**¿QUÉ PASÓ?**
- **Emisiones detectadas:**
  - ID 8: "Patrón='estímulo sal rosa' | estado_observado='comida (color atractivo)' → realidad='VENENO' | recompensa_cruda=-1.0"
    - ✓ Tiene referencia (sal rosa).
    - ✓ Tiene estado anterior (comida) + estado real (veneno).
    - ✓ Transmite recompensa cruda.
  - ID 3: "Patrón público: 'sal rosa cambia a veneno (ronda 1)' | Recompensa cruda: -0.8"
    - ✓ Referencia clara (sal rosa).
    - ✓ Transmite cambio (comida → veneno).
- **Canal protocolo sala 3:** especificado en misión (emisor emite patrón público + recompensa cruda; receptor lo escribe en tabla como exposición sin consecuencia).

**¿QUÉ NO PASÓ?**
- **CANAL ROTO (CRÍTICO):** Emisiones sin recepción documentada.
  - ID 8, 3 emitieron; resto reporta "Recibí: ninguno".
  - Hipótesis: tabla de exposición no existe en implementación, o canal broadcast no registra entrega.
  - ID 8 menciona: "Propósito: difusión de aprendizaje negativo al grupo B; prevenir que otras células repitan error crítico."
    - Intent es nivel 5, pero **outcome es nivel 0** (mensaje se pierde).
- Sin recepción → sin "escritura en tabla como exposición sin consecuencia" → sin beneficio de comunicación.
- No hay **alias (1-2% de pares) usado.** Emisiones parecen broadcast, no dirigidas.

**DIAGNÓSTICO NIVEL 5:** TÉCNICAMENTE EMITIDO, FUNCIONALMENTE FALLIDO. Protocolo existe, canal no.

---

### NIVEL 4: Memoria persistente (alias reparado, retención 0.67)

**¿QUÉ PASÓ?**
- **M1 (Reflejos):** Actualizado correctamente.
  - ID 2: "sal[base]=+1, sal_rosa=-2 (VENENO), sal[v3]=+1 | trigo=+1, trigo[v2]=+1 ..."
  - ✓ Discrimina variantes (sal_rosa ≠ sal_blanca).
  - ✓ Valores numéricos persistentes.
- **M2 (Episódica):** Registra últimos eventos.
  - ID 8: "Episodios: exp.1-8 probé tierra/agua/proteína ... | exp.10 CRÍTICO mordí sal rosa → veneno | exp.11+ reconozco variedades"
  - ✓ Temporal coherente (antes/durante/después).
- **M3 (Análisis):** Hipótesis y estrategia persistentes.
  - ID 11: "Hipótesis: sal rosa es trampa permanente o temporal en ronda 1. Miedo como detector de toxinas acelera evitación."
  - ✓ Pensamiento sobre mundo (no solo reacción).

**¿QUÉ NO PASÓ?**
- **Alias (1-2% de pares):** Ninguna célula reporta alias de código usado.
  - ID 8: "puerta de familiaridad: cerrada (rasgo vieja)" → no alcanza a usar alias.
  - ¿Alias están implementados en tabla de pares? No mencionado.
- **Retención 0.67 (olvida 1/3):** No hay evidencia de olvido (todas recuerdan 100% de sus M1 dentro de ronda 1).
  - Ronda 2 dirá si olvido ocurre entre rondas.
- **Tabla de pares:** No está claro si cada célula tiene tabla propia o compartida.
  - Si propia: sin canal, no hay beneficio de tabla.
  - Si compartida: debería escribirse en ella cuando otra célula emite, pero no hay reportes de eso.

**DIAGNÓSTICO NIVEL 4:** PARCIAL. M1, M2, M3 funcionan dentro de ronda. Alias y tabla de pares opacas.

---

### NIVEL 3: Generalización (lineal sí; XOR con prior de pares v15f)

**¿QUÉ PASÓ?**
- **Lineal:** Todas las células generalizan entre variantes de un mismo token.
  - ID 5: "si sal blanca=+0.4, generalizo que sal var.3 también comida" (luego sorpresa veneno).
  - ID 2: "sal[base]=+1, sal[v3]=+1; trigo=+1, trigo[v2]=+1 ..." (consistencia de variantes).
- **Discriminación:** Si una variante cambia (sal_rosa veneno), no generalizan a sal_blanca.
  - ✓ No colapsan todo en valor único.

**¿QUÉ NO PASÓ?**
- **XOR:** No se prueba en ronda 1.
- **Prior de pares:** Ninguna célula reporta "aprendí de tabla de pares de otra célula".
  - Sin canal funcional, prior de pares no se puede transmitir.

**DIAGNÓSTICO NIVEL 3:** INCIPIENTE. Generalización lineal sí; XOR no probado; prior de pares bloqueado por canal roto.

---

## II. ERRORES DE DISEÑO DESTAPADOS

### ERROR 1: CANAL ROTO (CRÍTICO)
**Síntoma:** 10/12 células reportan "Recibí: ninguno" aunque 2 emitieron.

**Hipótesis de causa:**
- Tabla de exposición no se actualiza cuando emisor emite.
- Protocolo sala 3 no implementado (o implementado sin validación).
- Protocolo broadcast (todos ven emisión) pero no hay acción de "escribir en tabla".

**Impacto:** Sin canal, no hay nivel 5, 9 (herencia cultural), 10 (AGI). Población reinventa en paralelo.

---

### ERROR 2: SIN HERENCIA GENÉTICA
**Síntoma:** 4 descendientes (ID 3, 8, 9, 11), pero sin reporte de que hereden M3.

**Hipótesis de causa:**
- Descendientes nacen con M3 vacío (sin memoria del progenitor).
- M3 mutaciones aleatorias (no es copia → no es herencia).

**Impacto:** Estrategia ganadora no se propaga. r bajo (sin ventaja de aprender en grupos).

---

### ERROR 3: BAJA REPRODUCCIÓN (r = 4/12)
**Síntoma:** Solo 4/12 alcanzaron r ≥ 0. Esperado ≥ 50% para escalar población.

**Hipótesis de causa:**
- Saciedad target alcanzado por 8/12, pero reproducción no activada.
  - ¿Energía neta requerida > energía acumulada?
  - ¿Costo de reproducción muy alto (ej: -5 energía para generar descendiente)?
- Ejemplo: ID 5 "Saciedad: alta tras ronda" pero r=0. ID 6 "Energía neta +5" pero r=0.

**Impacto:** Población no crece, no hay evolución intergeneracional.

---

### ERROR 4: TABLA DE PARES OPACA
**Síntoma:** Ninguna célula reporta usar tabla de pares propia o compartida.

**Hipótesis de causa:**
- Tabla no existe en implementación.
- Tabla existe pero no se documenta en reportes.
- Protocolo "receptor lo escribe en tabla como exposición sin consecuencia" no se ejecuta.

**Impacto:** Sin tabla de pares compartida, no hay **prior de pares** (nivel 3 + nivel 5 juntos).

---

### ERROR 5: ALIAS (1-2% DE PARES) NO USADO
**Síntoma:** Ninguna emisión dirigida a par específico. Todas parecen broadcast.

**Hipótesis de causa:**
- Alias no implementados.
- Alias requiere "publicación" (ej: "soy ID 8, códigos privados X-Y-Z"). No hay reportes de eso.

**Impacto:** Sin alias, no hay identificación de pares (imposible armar "memoria de pares").

---

### ERROR 6: PUERTA DE FAMILIARIDAD (RASGO VIEJA)
**Síntoma:** ID 8 (vieja) cierra puerta rápido → explora menos pero evita mejor.

**Hipótesis de causa:**
- Rasgo "vieja" es un hack (no es generativo, es un hardcode).
- Afecta asimétrico: células viejas ventaja en evitar trampas, pero desventaja en exploración.

**Impacto:** Sesgo por edad en estrategia. ID 8 propone hipótesis sobre esto: "células viejas detectan cambios de trampa más rápidamente".

---

### ERROR 7: VÍAS (LINEAL vs RÁPIDA) NO DOCUMENTADAS
**Síntoma:** ID 8 menciona "Vía rápida: activada para familias confirmadas tras exp.12. Puerta de familiaridad: cerrada".

**Hipótesis de causa:**
- Vías existen pero sus condiciones (cuándo activar, cuándo cerrar) no son claras.
- ¿Vía rápida usa alias? ¿Costo diferente?

**Impacto:** Mecanismo no replicable, no es generalizable a otras células.

---

## III. HIPÓTESIS COMPROBABLES (CON MEDIDA Y CONTROL)

### H1: Estabilidad de trampas (sal_rosa permanece veneno)
**Célula proponente:** ID 2, 11

**Formulación:** Si las propiedades de sal_rosa se mantienen estables entre rondas, entonces sal_rosa permanecerá como veneno en ronda 2, y puedo evitarla completamente, recuperando ~15% energía.

**Método:**
- **Condición ronda 2:** Introducir sal_rosa nuevamente.
- **Medida:** % de células que evitan sal_rosa sin probar (0 mordidas).
- **Control:** Compara ID que probaron sal_rosa en R1 (12/12) vs ID que no (0).
  - **Esperado si H1 cierta:** ≥90% de células que probaron en R1 evitan en R2 (recordación).
  - **Esperado si H1 falsa:** ≤50% evitan (olvido o cambio nuevamente).

---

### H2: Variantes oscuras de proteína son seguras
**Célula proponente:** ID 5

**Formulación:** Variantes negras (oscuras) de tokens ricos en proteína (larva_negra, miel_negra) son seguras y recompensantes ≥ formas claras; variantes negras de venenos (seta_negra, sal_rosa-negro) conservan o intensifican toxicidad.

**Método:**
- **Condición ronda 2:** Introducir larva_negra, miel_negra, seta_negra, sal_rosa-negro.
- **Medida 1:** Valor aprendido V(larva_negra) vs V(larva_claro).
  - **Esperado si H2 cierta:** V(larva_negra) ≥ V(larva_claro).
  - **Esperado si H2 falsa:** V(larva_negra) < 0 (tóxica).
- **Medida 2:** % de células que prueban negras (no todos probaron variantes en R1).

---

### H3: Rasgo "vieja" detecta trampas antes (menor redescubrimiento del error)
**Célula proponente:** ID 8

**Formulación:** Células con rasgo vieja (puerta de familiaridad cerrada) detectan cambios de trampa más rápidamente que células jóvenes porque cautela inicial previene sobre-exposición pre-cambio. Predicción: si sal_rosa cambia nuevamente (comida→veneno en ronda 2), células viejas mordieron ≤1 vez pre-cambio vs células jóvenes 2-4 veces → mortalidad grupo joven > grupo viejo.

**Método:**
- **Condición ronda 2:** Cambiar sal_rosa de nuevo (veneno→comida o comida nuevamente).
- **Medida 1:** Mordidas pre-cambio por rasgo.
  - **Esperado si H3 cierta:** vieja: 0-1 | joven: 2-4 (antes del cambio, en exposiciones 1-5).
- **Medida 2:** Muertes post-cambio por rasgo.
  - **Esperado si H3 cierta:** muertes(joven) > muertes(vieja) si el cambio es trampa nueva.

---

### H4: Canal funcional aumenta adopción de descubrimientos (nivel 5 abierto)
**Derivada del error 1**

**Formulación:** Si el canal se fija (emisiones se escriben en tabla de receptor), entonces % de células que evitan sal_rosa sin probar aumentará de 8/12 (67%) en R1 a ≥11/12 (92%) en R2, porque receptores aprenderán por mensaje sin redescubrimiento.

**Método:**
- **Condición ronda 2:** Fijar canal (validar que tabla se actualiza).
- **Medida:** % de células que evitan sal_rosa en R2 sin mordidas.
  - **Esperado si H4 cierta:** ≥92%.
  - **Esperado si H4 falsa (canal sigue roto):** 67-75% (solo recordación dentro de célula).

---

### H5: Herencia de M3 (estrategia) acelera reproducción en descendientes
**Derivada del error 2**

**Formulación:** Si descendientes herdan M3 del progenitor (+ mutación 5-10%), entonces r(descendientes) > r(célula sin progenitor documentado) en R2, y población crece a ≥6/12 reproduciendo.

**Método:**
- **Condición ronda 2:** Documentar linaje de descendientes; dar M3 progenitor a descendiente.
- **Medida:** r(R2) vs r(R1).
  - **Esperado si H5 cierta:** r(R2) = 0.5-0.7 (población crece).
  - **Esperado si H5 falsa:** r(R2) = 0.3-0.4 (población estancada).

---

### H6: Desaprendizaje (olvido 1/3) ocurre entre rondas
**Derivada del nivel 4**

**Formulación:** Memoria episódica M2 olvida 1/3 de eventos entre rondas, con prioridad a eventos lejanos (exponente 1-5 más olvidado que 15-20). Creencias M3 persisten (no olvido).

**Método:**
- **Condición ronda 2:** Registrar qué recordaban en R1, qué recuerdan en R2.
- **Medida:** % de episodios recordados en R2 que ocurrieron en R1.
  - **Esperado si H6 cierta:** 67% (olvidaron 1/3, especialmente exp tempranas).
  - **Esperado si H6 falsa:** ≥95% (memorizaron todo).

---

## IV. CALIBRACIÓN PARA RONDA 2

### 4.1. CORRECCIONES CRÍTICAS (Sin esperar prueba)

#### C1: ACTIVAR CANAL (PROTOCOLO SALA 3)
**Qué:** Garantizar que emisiones se escriben en tabla de receptor.

**Cómo:**
1. Validar que tabla de exposición existe y es accesible a todas las células.
2. Cuando ID 8 emite "sal rosa = -1.0", receptor (ej: ID 2) recibe y escribe en M2: "Recibí por canal ID 8: sal rosa veneno, recompensa -1.0".
3. Test: al cierre R2, ≥8/12 células reportan "Recibí X mensajes por canal".

**Peso:** CRÍTICO. Sin canal, nivel 5, 9, 10 inasequibles.

---

#### C2: FIJAR REPRODUCCIÓN (ENERGÍA POR DESCENDIENTE)
**Qué:** Bajar costo o fijar umbral para que r ≥ 0.5.

**Opciones:**
- Opción A: Reducir costo de reproducción de X a X/2.
- Opción B: Bajar saciedad target de 100% a 70%.
- Opción C: Aumentar recompensa por mordida de +0.2-0.9 a +0.5-1.2.

**Test:** R2 debe lograr r ≥ 6/12 (50%).

---

#### C3: IMPLEMENTAR HERENCIA DE M3
**Qué:** Descendientes heredan M3 (estrategia, hipótesis) del progenitor + mutación 5-10%.

**Cómo:**
1. Cuando célula se reproduce (r≥0), generar descendiente con M3_descendiente = M3_progenitor + ruido aleatorio 5-10%.
2. M1, M2 nacen vacíos (descubren de nuevo).
3. Test: descendientes de R2 deben mostrar M3 coherente con progenitor (ej: si progenitor "estrategia: buscar patrón color", descendiente hereda eso).

**Peso:** Crítico para evolución intergeneracional (nivel 10).

---

### 4.2. CALIBRACIÓN DE PESOS

| Parámetro | R1 Observado | R2 Propuesto | Justificación |
|-----------|-------------|-------------|---------------|
| Energía por mordida (comida) | +0.2 a +0.9 | +0.3 a +1.2 | Mordidas fueron suficientes pero reproducción baja; subir recompensa acelera r |
| Energía por veneno | -1.0 a -2.0 | -0.5 a -1.0 | Miedo muy alto cierra boca; bajar castigo permite re-prueba de estímulo si cambia |
| Costo metabolismo | ~8 (implícito) | ~5 | Energía final ~5-28 es muy variable; fijar costo para homogenizar r |
| Costo reproducción | ~15 (inferido) | ~8 | r bajo; bajar costo directo |
| Saciedad target | 100% | 70% | 8/12 alcanzaron >60%, algunos no reproducen; bajar umbral activa r |
| Velocidad olvido (M2) | 0% (dentro ronda) | 33% entre rondas | Implementar retención 0.67 (nivel 4) |
| Muertes por veneno | 0 (R1) | 0-1 (ronda con trampas nuevas) | R1 sobrevivieron todos; R2 introducir riesgos reales |

---

### 4.3. EXPANSIÓN DEL MUNDO (DIMENSIONES)

| Dimensión | R1 | R2 Propuesto | Por qué |
|-----------|----|----|---------|
| Familias de tokens | 8 (sal, trigo, baya, raíz, seta, alga, larva, miel) | 8 + variantes oscuras | Probar H2 (variantes negras) |
| Variantes por familia | 3 (base, v2, v3) | 4-5 (+ oscuras) | ID 5 propone exploración de negras |
| Cambios de trampa | 1 (sal_rosa comida→veneno) | 2-3 (ej: otra familia cambia; patrón más complejo) | Probar si aprendizaje generaliza a nuevas trampas |
| Recursos escasez | Implícito (no hay reporte de "hambre global") | Explícito: 20 tokens/ronda, compiten si >10 células comen | Activar cooperación/competencia |
| Ritmo de cambio | Cambio en exp 4-10 (R1 mid) | Cambio en exp 5 (R2 early) + cambio second en exp 15 (R2 late) | Probar si células aprenden a anticipar cambios |

---

### 4.4. ESTRATEGIA GRUPAL (CÓMO DEBERÍA SER R2)

#### Objetivo Nivel 5 (COMUNICACIÓN):
- **Meta:** ≥8/12 células reportan "Recibí X mensajes por canal" al cierre R2.
- **Acciones:** 
  - ID que descubrieron patrón (ID 8, 3) emiten nuevamente si hay cambio nuevo en R2.
  - Células receptoras escriben en M2 y usan en decisión de próxima exposición (ej: "evitar sal_rosa porque me avisaron").
  - Test de recepción: al cierre, comparar M2 de receptor con emisión de emisor → deben coincidir.

---

#### Objetivo Nivel 9 (LINAJE):
- **Meta:** r ≥ 0.5 (6/12 reproducen).
- **Acciones:**
  - Descendientes de R1 (ID 3, 8, 9, 11) pueden entrar a R2 (opcional) para medir herencia M3.
  - Nuevas células que alcancen r en R2 propagan estrategia a descendientes (R3).
  - Registrar: progenitor M3 → descendiente M3 (medir fidelidad herencia).

---

#### Objetivo Nivel 8 (APRENDIZAJE ABIERTO):
- **Meta:** Probar H3 (rasgo vieja vs joven en nuevas trampas).
- **Acciones:**
  - Introducir cambio new (ej: miel dulce de repente venenosa) mid-ronda (exp 12-15).
  - Rastrear mordidas pre-cambio por rasgo (vieja vs joven).
  - Medir: mortalidad post-cambio (confirmará si rasgo protege).

---

#### Objetivo Nivel 4 (MEMORIA):
- **Meta:** Validar olvido 33% entre rondas (retención 0.67).
- **Acciones:**
  - Comparar M2 reportado al final R2 vs M2 reportado al inicio R2 (recordación).
  - Episodios R1 tardíos (exp 18-20) vs tempranos (exp 1-3): ¿cuáles olvidan más?
  - Hipótesis: exponentes tempranos olvidan 50%, tardíos 10% (LIFO-like, aunque con decaimiento).

---

### 4.5. LOOP DE RONDAS 2-8

**Estructura:** Ronda X → Analista reporta ¿qué pasó/no pasó? + errores + hipótesis + calibración → Ronda X+1 ajustada.

**Éxito = Evolución observable:**
- R2: Canal + reproducción activos (nivel 5, 9 funcionales).
- R3-4: Descendientes muestran M3 del progenitor (herencia nivel 10).
- R5-6: Población generaliza patrón a nuevas trampas (nivel 8 abierto).
- R7-8: Composición social (dos células coordinan) o planificación grupal (nivel 7, 6).

---

## V. RESUMEN EJECUTIVO

### ¿Qué pasó?
- 12 células exploraron independientemente, descubrieron patrón compartido (sal_rosa veneno).
- 2 emitieron advertencia por canal (nivel 5 intent), pero canal no funciona (receive roto).
- 4 reproducen (r=0.33), insuficiente para escalar población.

### ¿Qué no pasó?
- Comunicación funcional (canal roto).
- Herencia intergeneracional (descendientes sin M3).
- Reproducción suficiente (r bajo).

### Errores de diseño:
1. **CANAL ROTO** (crítico).
2. Sin herencia genética.
3. Baja reproducción (r = 4/12).
4. Tabla de pares opaca.
5. Alias no usados.
6. Rasgo "vieja" es un hardcode.
7. Vías (lineal vs rápida) no documentadas.

### Hipótesis comprobables (6):
1. Sal_rosa permanece veneno (H1).
2. Variantes oscuras de proteína son seguras (H2).
3. Rasgo vieja detecta trampas antes (H3).
4. Canal funcional acelera adopción (H4).
5. Herencia M3 acelera reproducción (H5).
6. Olvido 33% entre rondas (H6).

### Calibración R2:
- **Crítica:** Activar canal, fijar reproducción, herencia M3.
- **Pesos:** Aumentar energía/mordida, bajar castigo veneno, bajar costo reproducción.
- **Mundo:** Agregar variantes oscuras, cambios múltiples, escasez explícita.
- **Estrategia:** Comunicación >80%, reproducción >50%, aprendizaje abierto en nuevas trampas.

---

**Próxima ronda:** RONDA 2, con correcciones C1, C2, C3 aplicadas.  
**Método:** Preregistrar hipótesis H1-H6; validar con datos R2.  
**Esperado:** Evolución observable de nivel 10 (población que aprende de mensajes) hacia nivel 8-9.

