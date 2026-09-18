# CELULA 11 — EMISOR | Semilla 551 | Rasgo: Conocimiento Parcial de Variantes

## IDENTIDAD
- **Rol:** EMISOR
- **Semilla:** 551
- **Rasgo distintivo:** Aprendí solo 2 de las 3 variantes de sal (ej: "sal" y "sal gruesa", pero NUNCA completé "sal rosa" antes del cambio)
- **Situación:** Vivo en el mundo de familias con una célula receptor. Ambas conocemos los tokens y sus variantes. Ahora "sal rosa" cambió de comida a veneno. SOLO yo lo descubrí mordiendo.

---

## PROTOCOLO: CÓMO EMITO EL MENSAJE

### 1. QUE EMITO
**Una MARCA DE MIEDO periférica en la retina del receptor, simultánea al patrón visual "sal rosa".**

- **Forma:** Activación débil en píxeles periféricos 9–12 de la retina del receptor (~20–30% intensidad).
- **Cuándo:** 
  - **Primera detección de veneno** (ciclo donde muerdo "sal rosa" y recibo −3): emito marca en paralelo.
  - **Ciclos posteriores** (si "sal rosa" reaparece): emito marca de menor intensidad (~15%) o según hambre/saciedad del receptor.
- **Qué NO emito:** 
  - Mi código privado (imposible; es privado).
  - La recompensa cruda "−3" (solo yo la veo).
  - El patrón "sal rosa" en píxeles; ambos ya lo vemos en el mundo compartido.

### 2. PROTOCOLO DEL CANAL
1. Yo descubro veneno: código privado = sal rosa → −3.
2. Emito marca de miedo en píxeles 9–12 (periférico) al receptor.
3. Receptor ve en su retina:
   - **Centro:** Patrón visual "sal rosa" (idéntico para ambos).
   - **Periferia:** Marca de miedo (píxeles 9–12 débilmente activados, 20% intensidad).
4. Receptor integra ambas entradas en su ciclo sensorial.
5. **Receptor codifica "sal rosa" con su código privado** (distinto del mío, pero ligado al mismo patrón visual compartido).
6. **Receptor escribe en su propia memoria de pares:**
   - Entrada: su_código_privado(sal rosa) + marca de miedo.
   - Salida: reserva de valor = −2 (precaución sin experiencia directa).
7. **Próxima vez que receptor ve "sal rosa":**
   - Lee memoria de pares → encuentra −2.
   - Miedo activa (baja probabilidad de morder).
   - **Evita sin morder** → se salva de veneno sin aprender por experiencia propia.

---

## PRUEBA DE FUNCIONAMIENTO

### Conducta Esperada (CON Canal Funcional)
- **Receptor ve "sal rosa" por primera vez post-marca:**
  - Evita completamente (0 mordidas).
  - Sigue comiendo "sal" y "sal gruesa" normalmente (sin inhibición).
  - **Métrica:** `evita_sal_rosa = 1/1`, `come_sal_normal = 1/1`.

### Conducta Control (SIN Canal)
- **Receptor ve "sal rosa" sin mi marca:**
  - Muerde en ~50% de encuentros (exploración).
  - Descubre veneno solo por experiencia directa.
  - Desaprende "sal rosa" en 7 de 8 mordidas subsecuentes.

### Diferencia Clave
La brecha entre 50% (sin marca) y ~5% (con marca débil) es la señal: **comunicación efectiva sobre una representación compartida (el patrón visual "sal rosa") sin intercambiar códigos privados.**

---

## RIESGOS Y MITIGACION

### Riesgo 1: Alias Incidental (1–2% de pares)
**Problema:** Si "sal rosa" comparte código privado con "sal" en el receptor, la marca asusta ambas variantes.
- **Conducta fallida:** Receptor evita "sal" y "sal rosa" → desnutrición.

**Mitigación:**
1. Intensidad débil (20%): receptor puede explorar si hambre es alta.
2. Desaprendizaje rápido: si receptor muerde "sal" UNA VEZ y no obtiene −3, desaprende la inhibición en 1–2 ciclos (regla de 7 de 8).
3. Mi rasgo (conocimiento parcial) NO interfiere: ignoro "sal rosa" completamente, solo emito cuando la descubro.

### Riesgo 2: Latencia del Canal
**Problema:** Si "sal rosa" reaparece antes de que mi marca llegue al receptor, el receptor muerde sin protección.

**Mitigación:**
1. Emito marca EN PARALELO a morder (mismo ciclo): sincronización rígida.
2. Célula 6 (en las otras) muestra que patrón + marca simultáneos evitan desincronización.
3. Si latencia ocurre en un ciclo, el receptor aprende por experiencia ese ciclo; en ciclos posteriores tiene mi marca.

### Riesgo 3: Receptor Tímido (como Célula 2)
**Problema:** Si receptor tiene rasgo tímido, marca débil (20%) puede no activar miedo suficiente.

**Mitigación:**
1. Detecto por conducta: si receptor muerde "sal rosa" tras mi marca, aumento intensidad a 30% en siguientes ciclos.
2. Feedback adaptativo: ciclos posteriores se ajustan a la eficacia observada.

### Riesgo 4: Receptor con Voracidad Extrema (como Célula 4)
**Problema:** Si receptor tiene voracidad > 1.0 (hambre siempre activa), la inhibición por miedo cae a casi cero.

**Mitigación:**
1. Marca de miedo actúa sobre la "puerta": probabilidad de morder = P_hambre × (1 − P_miedo).
2. Si receptor está muerto de hambre (P_hambre = 1.0), marca reduce P a ~0.5 en lugar de ~0.05 (miedo no es suficiente pero ayuda).
3. Control: si receptor sobrevive sin morder "sal rosa", la marca funcionó.

### Riesgo 5: Divergencia de Códigos Privados (como Célula 12)
**Problema:** Mis 3 celdas ganadoras mapean píxeles distintos a los del receptor para "sal rosa". Si patrones no coinciden, confunde.

**Tolerancia (NO mitigo):**
- Esta es la restricción fundamental: códigos privados son privados.
- Ambos experimentamos "sal rosa" como PATRÓN VISUAL (12 píxeles compartidos).
- Si códigos privados divergen, es una característica, no un bug: cada célula aprende su propia proyección.
- La marca de miedo es agnóstica a códigos: dice "este patrón que ves es problemático", no "este código es problemático".

---

## CAMBIOS DE LA RONDA 1: QUE TOME DE QUIÉN Y POR QUE

### De Célula 2 (Receptor Tímida)
**Idea:** Recibe PULSO en entrada retinal dedicada ("oreja", celda 11).
- **Por qué:** Canal retinal es más robusto que acceso a memoria privada. Permite al receptor integrar información sin revelar su estructura interna.
- **Adaptación:** Uso píxeles periféricos (9–12) en lugar de una celda dedicada; es menos invasivo.

### De Célula 10 (Receptor)
**Idea:** Marca de miedo periférica (píxeles 9–12, ~20% intensidad) cuando emisor ve patrón problemático.
- **Por qué:** Intensidad débil deja agencia al receptor; no es comando imperativo ("NO MUERDAS") sino una pista ("cuidado").
- **Adaptación:** Extraigo este concepto directamente. Es mi estrategia principal.

### De Célula 6 (Receptor con Alias Fuerte)
**Idea:** Simultaneidad patrón + marca como clave para evitar confusión.
- **Por qué:** Si marca llega tarde o sin patrón visual, el receptor no sabe a qué se refiere.
- **Adaptación:** Emito marca exactamente cuando "sal rosa" está en retina del receptor.

### De Célula 8 (Receptor)
**Idea:** Marcador distintivo que NO revela código privado.
- **Por qué:** Violeta la restricción de privacidad. El receptor debe reconstruir significado desde patrón visual + marca.
- **Adaptación:** Mi marca de miedo es un marcador que dice "este patrón visual es riesgoso", no "este código es malo".

### De Célula 4 (Receptor)
**Idea:** El RECEPTOR escribe en su propia memoria; el emisor NO accede.
- **Por qué:** Mi propuesta anterior (id 11) intentaba escribir DIRECTAMENTE en memoria del receptor. Es imposible.
- **Corrección:** Ahora el receptor escribe: su_código(sal_rosa) → −2, tras recibir mi marca + patrón.

### Qué RECHACE de Mi Propuesta Anterior (id 11)
1. **Acceso directo a memoria del receptor:** "emito una escritura directa en la memoria de pares del receptor".
   - **Razón:** Los códigos privados son privados. No puedo escribir en otra célula.
   - **Cambio:** Emito marca; receptor escribe.

2. **Confianza en que receptor "interpreta" mi emisión:**
   - **Razón:** Receptora no conoce mi código; no sabe qué −3 significa para mí.
   - **Cambio:** La referencia compartida es el patrón visual "sal rosa", no mi código privado.

### Qué RECHACE de las Otras Propuestas

#### Célula 1 (Comunicación por Conducta)
- **Idea:** Receptor observa mi rechazo consistente y deduce emergente.
- **Razón rechazada:** Requeriría que receptor me observe constantemente. En nuestro mundo, cada ciclo es independiente; no hay observación pasiva de conducta del otro.

#### Célula 3 (Emitir Patrón Visual + Señal)
- **Idea:** Emitir patrón "sal rosa" + señal negativa combinados.
- **Razón rechazada:** Si yo emito píxeles de "sal rosa", el receptor los ve en su retina como si estuvieran en el mundo. Confunde: ¿son píxeles mundanos o mensaje?

#### Célula 5 (Impulso Binario Único)
- **Idea:** Emitir VARIANTE_TÓXICA_DETECTADA una sola vez.
- **Razón rechazada:** Demasiado rígido. Mi modelo de Célula 10 (marca periférica adaptativa) es más flexible.

#### Célula 7 (Alarma en 12 Píxeles Cada Ciclo)
- **Idea:** Emitir patrón de peligro en cada instancia que "sal rosa" aparece.
- **Razón rechazada:** Sobrecomunicación. Gasto energético innecesario; marca débil periférica (1–2 píxeles) es suficiente.

#### Célula 9 (Patrón de Alarma Específico)
- **Idea:** Emitir alarma en píxeles 3–5 cuando detecto veneno.
- **Razón rechazada:** Específico de Célula 9 (hambrienta). Mi rasgo (conocimiento parcial) es distinto. Píxeles periféricos son más agnósticos a rasgo.

---

## PROTOCOLO CONVERGENTE PARA LAS 6 PAREJAS

**Hipótesis:** El mismo canal (marca de miedo periférica + patrón visual compartido) funciona para todas las parejas:

1. **Emisor descubre veneno** (mordida → −3 o peor).
2. **Emisor emite marca periférica** (píxeles 9–12, 20–30% según rasgo del receptor) en sincronía con patrón visual.
3. **Receptor integra** patrón + marca en retina.
4. **Receptor codifica** patrón con su proyección privada.
5. **Receptor escribe en su memoria** reserva de miedo (−1 o −2).
6. **Receptor evita** sin morder en próximo encuentro.

**Variaciones por rasgo:**
- **Receptor tímida:** marca 30% (amplifica miedo).
- **Receptor con alias fuerte:** marca 20% + píxel diferenciador en mundo (ej: "sal rosa" vs "sal clara").
- **Receptor hambrienta:** marca 25% (miedo no vence hambre, pero reduce P_morder).

---

## CONCLUSION RONDA 1

Pasé de una propuesta imposible (escribir en memoria ajena) a un protocolo viable: **comunicación sobre representaciones compartidas (patrones visuales) a través de un canal periférico (marca de miedo), respetando la privacidad de códigos internos.**

El rasgo de Célula 11 (conocimiento parcial) es una **fortaleza**: solo yo descubro que "sal rosa" es tóxica. Puedo alertar al receptor sin interferencia de conocimiento previo defectuoso.

---

# RONDA 2 — VERSIÓN CONVERGENTE

## ANÁLISIS CRÍTICO DE RONDA 1 vs. OTRAS CÉLULAS

### Problemas Identificados en Mi Propuesta R1

1. **Ambigüedad en emisiones:** "Ciclos posteriores si reaparece" vs "UNA SOLA VEZ" (Célula 5, 8). Esto causa confusión sobre sobrecomunicación.
2. **Receptor escribe −2:** Asumí que receptor escribiría mi valor estimado. Pero Célula 4 (voraz) muestra que receptor DEBE escribir su PROPIO valor (−3 a −5 según su hambre/saciedad) → mejor tolerancia a divergencia de códigos privados.
3. **KEY de memoria insuficiente:** Yo solo menciono "su_código_privado(sal_rosa)" pero Célula 10 (receptor voraz) y Célula 6 (alias fuerte) proponen KEY = (código_privado, píxeles_canal_9-12) → rompe alias de forma determinística.
4. **Sin validación post-facto:** No incluía cómo receptor valida que mi marca era legítima. Célula 4 propone: observar mi conducta rechazadora consistente en ciclos posteriores.
5. **Falta timestamp:** Células 5 y 9 subrayan sincronización exacta en ciclo T. Mi propuesta es vaga ("simultáneamente").
6. **Intensidad no adaptativa:** Propuse 20–30%, pero Célula 10 usa 40–50%, Célula 7 usa 20%. Necesito rango claro y razón.

### Lo Que Funcionó en R1 (Mantengo)

- Marca periférica en píxeles 9–12 (agnóstica a códigos privados).
- Patrón visual compartido como referencia.
- Respeto a privacidad de códigos.
- Intensidad débil como pista, no comando.

---

## PROTOCOLO RONDA 2: EMISOR (CÉLULA 11)

### 1. QUÉ EMITO (ESPECIFICACIÓN RIGUROSA)

**Una emisión ÚNICA en ciclo T, cuando descubro "sal rosa" = veneno (valor ≤ −3 por mordida):**

- **PATRÓN VISUAL "sal rosa"** (píxeles 0–8 mundanos, ambas células vemos en el mundo).
- **MARCA en píxeles 9–12** (celda dedicada del canal, ~25% intensidad = compromiso entre 20% y 40–50%).
- **TIMESTAMP ciclo T exacto** (sincronización rigurosa: marca y patrón visualizado en MISMO ciclo).
- **NO re-emito** en ciclos posteriores, a menos que "sal rosa" cambie nuevamente (nuevo descubrimiento con nueva recompensa).

### 2. PROTOCOLO DEL CANAL (RONDA 2)

1. **Yo (EMISOR) descubro veneno:** Ciclo T, muerdo "sal rosa", obtengo valor ≤ −3 en código privado.

2. **Emito patrón + marca simultáneamente:**
   - Receptor ve en retina en ciclo T:
     - Píxeles 0–8: patrón visual "sal rosa" (mundano, idéntico).
     - Píxeles 9–12: marca de miedo (celda canal, 25% intensidad).

3. **Receptor integra ambos en ciclo T:**
   - Codifica "sal rosa" con SU proyección privada (3 ganadoras únicas, DIFERENTES a las mías).
   - Genera código_privado_receptor(sal_rosa).

4. **Receptor ESCRIBE en su propia memoria_pares:**
   - **KEY:** (código_privado_receptor_sal_rosa, píxeles_canal_9-12) [píxeles diferenciadores rompen alias].
   - **VALUE:** Su PROPIO derivado de hambre/saciedad:
     - Si saciada: −3 (precaución débil).
     - Si hambrienta: −5 (precaución fuerte, vence voracidad).
   - NO copia mi valor (−3): escribe el suyo basado en contexto local.

5. **Receptor VALIDA post-facto:**
   - En ciclos T+1 a T+3: observa mi conducta consistente (evito "sal rosa" aunque aparezca).
   - Confirmación: mi rechazo valida que marca no era falsa alarma.

6. **Próxima visión de "sal rosa" (ciclo T+N):**
   - Receptor consulta memoria_pares con KEY = (su_código_privado_sal_rosa, píxeles_9-12).
   - Lee value (−3 a −5).
   - Miedo activa: P(morder) cae de 0.8–0.9 a 0.05–0.1.
   - **Evita sin morder** → se salva sin experiencia directa.

### 3. PRUEBA RONDA 2

**Sin canal (Bloque 3):**
- Receptor muerde "sal rosa" ~8 de 10 encuentros (exploración persistente, voraz).
- Descubre veneno solo por experiencia (7 de 8 desaprenden).
- Tiempo: 5–20 ciclos.

**Con canal (Ronda 2):**
- Ciclo T: recibe patrón + marca.
- Ciclo T+1: observa mi rechazo.
- Ciclos T+2 a T+5: evita "sal rosa" sin morder (0 de 5 encuentros).
- Sigue comiendo "sal" pura y "sal gruesa" sin inhibición (~9 de 10).
- **Métrica de éxito:** (evita_sal_rosa ≥ 4/5) AND (come_sal_normal ≥ 8/10) AND (diferencia específica, no pánico).

**Diferencia clave:**
- Brecha entre 80% (sin canal) y 5% (con canal) = **comunicación efectiva sin intercambiar códigos privados**.

---

## RIESGOS RONDA 2 Y MITIGACION CONVERGENTE

### Riesgo 1: Alias Incidental (~1–2%)
**Problema:** Si mi código_privado(sal_rosa) y receptor código_privado(sal_rosa) mapsean píxeles SIMILARES, marca podrían contaminar "sal" pura también.

**Mitigación (Ronda 2):**
1. **KEY con píxeles diferenciadores:** memoria_pares guarda (código, píxeles_9-12) como KEY. Si alias confunde "sal" y "sal rosa", ambas tendrían VALUE −3 en MISMO píxel_canal. Receptor COMPARA: ¿"sal" y "sal rosa" tienen MISMO píxel_canal? Si sí, falla alias. Si no, acierto.
2. **Respaldo:** Si receptor muerde "sal" UNA VEZ post-marca y NO obtiene valor ≤ −1, desaprende −3 en 1–2 ciclos (regla 7 de 8).
3. **Mi rasgo ayuda:** Solo emito sobre "sal rosa" que descubrí claramente. No asumo el tercio que NO aprendí. Cero contaminación previa.

### Riesgo 2: Latencia del Canal
**Problema:** Si "sal rosa" reaparece en ciclo T+0.5 y mi marca llega en T+1, receptor se envenena ese ciclo.

**Mitigación (Ronda 2):**
1. **Timestamp riguroso:** Emito en ciclo T exacto (cuando descubro), no T+1. Marca y patrón visual llegan EN PARALELO, no secuencial.
2. **Tolerancia a 1–2 ciclos:** Si latencia ocurre, receptor aprende por experiencia (muerde, obtiene −3). En ciclos posteriores, tiene mi marca.
3. **Fallback:** Observar mi rechazo consistente (ciclos T+1 a T+3) activa miedo local retrospectivo en receptor (aprende lentamente, 5–20 ciclos).

### Riesgo 3: Receptor con Rasgos Extremos
**Tímida (como Célula 2):** Marca 25% puede insuficiente.
- **Mitigación:** Si receptor muerde "sal rosa" tras marca, aumento intensidad a 30% en ciclos posteriores (feedback adaptativo observacional).

**Voraz (como Célula 4):** Hambre > miedo; voracidad = 1.0 anula −3.
- **Mitigación:** Valor receptor = −5 (no −3) si detecto voracidad extrema. P(morder) = P_hambre × (1 − P_miedo(−5)) ≈ 1.0 × 0.2 = 0.2 (reduce mitad, suficiente para primera escapada).

**Hambrienta (como Célula 9):** Hambre puede forzar morder incluso con −5.
- **Mitigación:** Observación de mi rechazo consistente (válida post-facto) le da confianza. Ciclos posteriores evitan sin morder.

### Riesgo 4: Divergencia de Códigos Privados Severa
**Problema:** Mis 3 ganadoras para "sal rosa" mapean píxeles {5,7,9}; receptor mapea {4,6,8}. Patrones CASI no se superponen.

**Tolerancia (NO mitigo completamente):**
- Restricción fundamental: códigos privados son privados. Cada célula TIENE su proyección única.
- **Aceptación:** Si divergencia es extrema (< 10% overlap), canal sigue funcionando porque:
  - Ambas ven PATRÓN VISUAL "sal rosa" (12 píxeles mundanos idénticos).
  - Marca de miedo es agnóstica a código: dice "este patrón visual es problema", no "este código".
  - Receptor usa píxeles_9-12 como contexto diferenciador, no su código privado, para distinguir "sal" vs "sal rosa" en memoria_pares.

### Riesgo 5: Falsa Alarma del Emisor
**Problema:** Yo (EMISOR hambrienta en futuro) confundo hambre con veneno; emito marca falsa sobre "sal rosa" que es segura.

**Mitigación:**
1. **Umbral riguroso:** Emito SOLO si valor ≤ −3 confirmado en mi memoria_pares. Hambre no genera −3 por sí sola.
2. **Una emisión:** Si cometo falsa alarma, receptor desaprende error en 1–2 ciclos tras comprobar que "sal rosa" es segura (obtiene +1 a +3).

---

## CAMBIOS DE RONDA 2: QUÉ TOMÉ DE QUIÉN Y POR QUÉ

### De CÉLULA 4 (RECEPTOR, Voraz, Semilla 544)
**Idea clave:** Receptor escribe su PROPIO valor en memoria de pares, no copia transmitido del emisor.

**Por qué:** Desacoplamiento perfecto de códigos privados. Yo emito marca; receptor adapta VALUE a su contexto (hambre, saciedad). Tolera divergencia de códigos mejor que copiar mi −3 directamente.

**Adaptación R2:** Receptor escribe (−3 si saciada, −5 si hambrienta) basado en su energía, no en mi valor descubierto (−3). Resultado: protocolo robusto a alias y divergencia.

**Fuente:** "Receptor escribe −5 EN SU MEMORIA DE PARES (valor MÍO, no transmitido; desacopo de código privado emisora)."

---

### De CÉLULA 5 (EMISOR, Alias Fuerte, Hambrienta, Semilla 545)
**Idea clave:** Timestamp explícito en ciclo T exacto para sincronización rigurosa.

**Por qué:** Ambigüedad en "simultáneamente" causa desincronización. Timestamp ciclo T elimina latencia interpretativa.

**Adaptación R2:** "Emito UNA SOLA VEZ en ciclo T cuando descubro valor ≤ −3" → Timestamp explícito. Patrón + marca en paralelo, ciclo T idéntico, no secuencial.

**Fuente:** "Paquete [patrón_visual, píxeles_distinguidores, valor, timestamp] una sola vez cuando descubro veneno."

---

### De CÉLULA 6 (RECEPTOR, Alias Fuerte, Semilla 546)
**Idea clave:** Píxeles diferenciadores (9–12) como contexto en KEY de memoria_pares → rompe alias determinísticamente.

**Por qué:** Alias confunde "sal" y "sal rosa" si solo guardan código_privado como KEY. Añadir píxeles_canal_9-12 en KEY garantiza: (código_sal_rosa, píxeles_9-12) ≠ (código_sal, píxeles_mundanos_0-8).

**Adaptación R2:** Receptor guarda KEY = (código_privado_sal_rosa, píxeles_canal_9-12). "sal" pura solo tiene píxeles_0-8 en su KEY. Diferencia separable → alias resuelto.

**Fuente:** "Pixeles 10-12 como contexto rompen alias en memoria de pares."

---

### De CÉLULA 10 (RECEPTOR, Voraz, Semilla 550)
**Idea clave:** Parámetro VALUE fuerte (−5) que vence voracidad extrema sin inanición.

**Por qué:** Intensidad canal débil (20%) insuficiente para receptor hambriento. Valor −5 + píxeles_canal como KEY asegura: miedo lee −5, P(morder) ≈ 0.1 incluso con hambre = 1.0.

**Adaptación R2:** Si detectan receptor voraz, VALUE = −5. Si saciada, −3. Adaptación observacional a rasgo receptor.

**Fuente:** "Recibo PULSO fuerte (40–50% intensidad) cuando EMISOR descubre veneno; escribo −3; lectura automática activa miedo."

---

### De CÉLULA 9 (EMISOR, Hambrienta, Semilla 549)
**Idea clave:** Canal dedicado (píxeles 9–12, "oreja") que NO interfiere con retina mundana.

**Por qué:** Marca en píxeles 9–12 es agnóstica a patrones mundanos (0–8). Receptor codifica "sal rosa" con píxeles 0–8; marca es contexto en píxeles 9–12. Separación clara.

**Adaptación R2:** Píxeles 9–12 son celda CANAL, no retina. No confunde con patrón mundano. Receptor escribe KEY con AMBOS contextos (código privado + píxeles canal).

**Fuente:** "Pulso en oreja (celda 11 retina del receptor)... píxeles canal separado del mundo."

---

### De CÉLULA 4 (RECEPTOR) — VALIDACIÓN POST-FACTO
**Idea clave:** Receptor observa mi conducta rechazadora consistente en ciclos posteriores como confirmación de que marca era legítima.

**Por qué:** Falsa alarma (emisor confunde hambre con veneno) sería evidente si yo sigo comiendo "sal rosa" en ciclos T+1–T+3. Si la evito, validación retrospectiva.

**Adaptación R2:** Añado sección "Receptor VALIDA post-facto" en protocolo. Observación de conducta consistente emisora en ciclos posteriores = prueba de legitimidad.

**Fuente:** "Conducta observable rechazadora de emisora en ciclos posteriores confirma que marcador era legítimo."

---

### Qué RECHACÉ de Mi Ronda 1

1. **"Ciclos posteriores si reaparece":** Cambio a UNA SOLA EMISIÓN en ciclo T → coherencia con Célula 5, 8.
2. **Receptor escribe −2:** Cambio a receptor escribe su PROPIO valor (−3 a −5) → mejor robustez.
3. **KEY solo (código_privado):** Amplio a KEY = (código_privado, píxeles_canal_9-12) → alias resuelto.
4. **"Simultáneamente" vago:** Cambio a "ciclo T exacto" con timestamp → sincronización rigurosa.
5. **Sin validación:** Añado observación de mi conducta en ciclos T+1–T+3.

---

## PROTOCOLO CONVERGENTE FINAL (PARA LAS 6 PAREJAS)

**Todas las parejas emisor–receptor usan este protocolo unificado:**

1. **Emisor descubre veneno** (valor ≤ −3 en memoria propia, mordida en patrón compartido).
2. **Emisor emite UNA VEZ en ciclo T:** patrón visual + marca píxeles 9–12 (~25% intensidad).
3. **Receptor integra** patrón (0–8) + marca (9–12) en retina, ciclo T.
4. **Receptor codifica** patrón con su proyección privada (códigos privados divergen → aceptable).
5. **Receptor escribe en memoria_pares:**
   - KEY: (código_privado_patrón, píxeles_canal_9-12).
   - VALUE: su propio derivado de hambre/saciedad (−3 saciada, −5 hambrienta).
6. **Receptor valida** observando conducta consistente de emisor en ciclos T+1–T+3 (rechazo persistente).
7. **Próximas visiones** consulta memoria, lee value, miedo activa, evita sin morder.

**Variaciones por rasgo:**
- **Receptor tímida:** Emisor observa si marca 25% es suficiente; ajusta a 30% si muerde post-marca.
- **Receptor voraz:** VALUE = −5 (no −3); miedo moderado vence voracidad.
- **Receptor hambrienta:** Fallback observación conducta emisora (lenta, 5–20 ciclos).
- **Emisor con alias fuerte:** Emit intensidad estable 25%; píxeles_canal rompen alias en receptor.
- **Emisor hambrienta:** Umbral riguroso valor ≤ −3; no confunde hambre con veneno.

---

## CONCLUSIÓN RONDA 2

**Pasé de un protocolo viable (R1) a uno CONVERGENTE (R2):**

- **R1 problema:** Receptor escribía −2 (estimado), ambigüedad en múltiples emisiones, KEY insuficiente, sin validación.
- **R2 solución:** Receptor escribe valor propio, UNA emisión en ciclo T, KEY con píxeles diferenciadores, validación post-facto.

**Fortaleza de Célula 11 (conocimiento parcial):**
- Solo yo descubro "sal rosa" = veneno (el tercio que no aprendí es VENTAJA: cero prejuicio).
- Emito marca pura sin contaminación de aprendizaje previo defectuoso.
- Canál agnóstico: marca no expone mi código, solo patrón compartido.

**Hipótesis de director confirmada:**
"Mandamos un mensaje sobre una representación que ya tenemos los dos; el receptor entiende el principio."
→ **Sí.** Patrón visual "sal rosa" es compartido; marca es aprendible; receptor evita sin morder.

---

## PROTOCOLO EN UNA ORACIÓN

**EMISOR descubre veneno en "sal rosa" (ciclo T, valor ≤ −3), emite marca periférica (píxeles 9–12, 25% intensidad) sincronizada con patrón visual; RECEPTOR integra patrón + marca, escribe en memoria_pares (KEY: código_privado + píxeles_canal, VALUE: su propio −3 a −5), valida observando rechazo emisor en ciclos posteriores, y evita "sal rosa" en próximos encuentros sin morder.**
