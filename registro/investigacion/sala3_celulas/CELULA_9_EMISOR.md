# CÉLULA 9 – EMISOR | Hambrienta casi siempre | Semilla 549

## Propuesta Ronda 1: Protocolo Convergente

### Qué emito
**Cuándo:** Cada ciclo en que detecto "sal rosa" en el mundo y leo valor ≤ −1 en mi memoria (veneno confirmado por mordida previa).

**Qué:** Pulso en "oreja" del receptor (celda dedicada de su retina, ej. celda 11) simultáneamente con la aparición de "sal rosa" en el mundo compartido.

**Contenido:** 
- Valor local: −5 (si hambre extrema reduce mi tolerancia; −3 en caso base).
- Referencia: patrón visual "sal rosa" (compartido, ambas lo vemos en el mundo).
- **No revelo mi código privado** (mis 3 celdas ganadoras son locales).

### Qué recibe el receptor
1. **Patrón "sal rosa"** en su retina (canales 0–12, píxeles del mundo).
2. **Pulso "oreja"** en su retina (celda 11, entrada dedicada de canal).
3. **Simultáneamente**: su cerebro escribe en memoria de pares:
   - Clave: `(su_código_privado_para_sal_rosa, pulso_entrada)`
   - Valor: −5 (según mi estado hambrienta).
   - Resultado: próxima vez que vea "sal rosa", lee −5 en memoria → miedo dispara → evita sin morder.

### Conducta esperada (prueba medible)

**Escenario 1: Receptor SIN canal (control)**
- Vuelvo a emitir "sal rosa".
- Receptor: muerdo nuevamente (~7 de 8 veces; aprendo lentamente vía error).

**Escenario 2: Receptor CON canal (con mi emisión)**
- Emito pulso + patrón UNA SOLA VEZ cuando descubro veneno (ciclo T).
- Receptor recibe → escribe en memoria.
- Ciclo T+1 en adelante: receptor ve "sal rosa".
- **Conducta esperada:** evita sin morder (0 de 1 encuentro; 0 de 5 en prueba prolongada).
- **Control:** receptor sigue comiendo "sal" normal y otras variantes (no pánico generalizado).

**Diferencial:** Evita específicamente "sal rosa", no por miedo existencial sino por lectura de memoria.

### Riesgos y mitigaciones

| Riesgo | Causa | Mitigación | Métrica |
|--------|-------|-----------|---------|
| **Falsa alarma por hambre extrema** | Si hambre < 0.2, confundo sed o dolor con veneno; emito pulso incorrecto. | Emito solo si valor ≤ −1 *confirmado* en mi memoria. Si hambre severa, rebajo umbral a −1.5 (más conservador). | Contar falsos pulsos: si > 2 en 10 ciclos, hambrienta ignora. |
| **Alias cruzado con "sal"** | ~1–2% de pares de píxeles comparten código. Si mis píxeles en "sal rosa" mapean a "sal" en receptor, confundo variantes. | Celda "oreja" (11) es distinta de píxeles mundanos (0-10); alias toca solo memoria pares de "sal rosa" específicamente, no generaliza. | Si receptor evita ambas: alias ocurrió. Si evita solo "sal rosa": alias controlado. |
| **Sobrecomunicación → desconfianza** | Si emito cada ciclo, receptor recibe ruido, aprende a ignorarme. | Emito UNA SOLA VEZ por patrón nuevo tóxico. Receptor escribe en memoria persistente; no repito. | Contador de pulsos por patrón: máximo 1. |
| **Rasgo hambrienta: costo energético de emisión** | Emitir consume metabolismo; si no como, muero. | Hambre extrema no impide emisión (local, 1 ciclo, bajo costo). **Prioridad: comer primero, avisar segundo.** Si conflicto, como, no emito. | ¿Muero durante experimento? Cambio a valor −2 (más débil). |
| **Latencia del canal** | Si patrón "sal rosa" aparece antes de que pulso llegue, receptor muerde. | Ambas vivimos en mismo mundo; simultaneidad es local (no hay retardo en canal). Emito en T, receptor recibe en T (mismo ciclo). | Medir: receptor encuentra sal rosa en ciclo T+0 (sin emisión) vs T+1+ (con emisión). |
| **Receptor no entiende el pulso** | Si receptor interpreta "oreja" como ruido, no escribe en memoria. | Convergencia: todas las parejas usan mismo canal (oreja, celda 11). Receptor aprende por repetición que oreja = contexto peligroso. | Generación post-ronda 2: receptor emite que aprendió. |

---

## Cambios de Ronda 1: qué tomé de quién y por qué

#### De CÉLULA 2 (Receptor tímida, rol inverso)
- **Tomé:** Pulso en "oreja" (celda dedicada) en lugar de "patrón alarma en píxeles 3-5".
- **Por qué:** Píxeles 3-5 son ambiguos en retina; podrían ser parte del patrón "sal rosa" o ruido del mundo. **Oreja es un canal explícito**, minimiza falsos positivos, y no interfiere con códificación del mundo.

#### De CÉLULA 4 (Receptor voraz)
- **Tomé:** Escritura directa de valor (−5, veneno fuerte) en memoria pares en lugar de "integración vaga del estímulo".
- **Por qué:** Voracidad requiere miedo **fuerte e inequívoco**. Valor −5 es no-negociable en lectura de memoria. Receptor voraz saltará la señal débil; −5 en memoria vence hambre del receptor.

#### De CÉLULA 11 (Emisor, rol mismo que yo)
- **Tomé:** Timing explícito: emito **dentro del ciclo T** en que descubro veneno, no después.
- **Por qué:** Latencia mata el aprendizaje. Hambrienta o no, emisión inmediata = receptor asocia patrón + señal en **mismo ciclo**, refuerza memoria.

#### De CÉLULA 10 (Receptor)
- **Tomé:** Reconozco que tensión entre rasgo (hambrienta) y miedo débil crea fallos; mitigo con **valor fuerte**.
- **Por qué:** Receptor hambriento come aunque reciba marcador débil. Mi rasgo "hambrienta" sugiere que mi señal debe ser **fuerte (−5)** para vencer hambre del receptor.

#### De CÉLULA 1 (Emisor tímida, rol mismo)
- **Tomé:** Consistencia conductual: siempre rechazo "sal rosa" tras descubrir veneno; receptor me ve.
- **Por qué:** Rastreabilidad + refuerzo. Si receptor me ve rechazar siempre, la señal pulso refuerza conducta observada (doble referencia: pulso + conducta visible).

#### De CÉLULA 8 (Receptor)
- **Tomé:** Idea de "marcador distintivo" que no interfiere con píxeles mundanos.
- **Por qué:** Oreja (celda 11) es mi "marcador distintivo"; no es patrón, es contexto. Receptor aprende: oreja activada = peligro.

---

## Protocolo Convergente para las 6 parejas (Versión 1)

**Regla universal:**

```
1. EMISOR detecta cambio: mordidas "sal rosa" → valor ≤ −1 en memoria.
2. EMISOR emite en ciclo T: pulso "oreja" del RECEPTOR (celda 11).
3. RECEPTOR recibe en ciclo T: patrón "sal rosa" (retina 0–10) + pulso (retina 11) simultáneamente.
4. RECEPTOR escribe en memoria de pares: (código_privado_sal_rosa, contexto_pulso) → valor −3 a −5.
5. RECEPTOR, ciclo T+1+: lee patrón "sal rosa" → consulta memoria → lee valor negativo → miedo dispara.
6. RECEPTOR evita sin morder en próximo encuentro con "sal rosa".
```

### Variaciones según rasgo del EMISOR
- **Hambrienta (como yo):** Valor −5 (miedo reforzado para vencer hambre del receptor).
- **Tímida:** Valor −2 (miedo leve; receptor ya es cauteloso de base).
- **Voraz:** Valor −3 (estándar).

### Variaciones según rasgo del RECEPTOR
- **Tímido:** Valor −2 (ya evita por naturaleza; refuerzo leve).
- **Voraz:** Valor −4 (miedo fuerte para vencer apetito).
- **Alias fuerte:** Valor −4 + marca extra en píxel diferenciador.

---

## Resumen de salida (Ronda 1)

| Componente | Valor |
|------------|-------|
| **ID célula** | 9 |
| **Rol** | EMISOR |
| **Semilla** | 549 |
| **Rasgo** | Hambrienta casi siempre |
| **Canal** | Pulso "oreja" (celda retina 11) en receptor |
| **Valor emitido** | −5 (veneno + hambre extrema) |
| **Qué recibe receptor** | Patrón "sal rosa" (mundano) + pulso (contexto) simultáneamente |
| **Acción receptor esperada** | Escribe en memoria: (código_sal_rosa, pulso) → −5. Evita sin morder. |
| **Prueba diferencial** | Evita solo "sal rosa", sigue comiendo "sal" normal (no pánico) |
| **Convergencia** | 6 parejas usan oreja (celda 11) + valor −3 a −5. Protocolo único. |
| **Riesgo crítico mitigado** | Hambrienta + falsa alarma → descartada (solo si valor ≤ −1 confirmado). Alias → localizado en memoria de pares de "sal rosa". |

---

## Notas para Ronda 2

- Si receptor falla (no evita tras pulso), revisar: ¿receptor recibió pulso? ¿Su código privado para "sal rosa" mapea píxeles distintos a los míos? ¿Alias interfiere?
- Si receptor sobregeneraliza (evita también "sal"), mitigo: marcar píxel diferenciador en próxima emisión.
- Después de Ronda 2: todas las 6 parejas emitirán; buscar protocolo único que funcione para todas.

---

# CÉLULA 9 – RONDA 2: Protocolo Convergido

## Análisis de las otras 11 células y convergencia

### Críticas a mi Ronda 1
1. **"Celda 11 oreja" es frágil y única.** Las otras 9 células usan píxeles 9-12 como rango estándar (EMISOR 3, RECEPTOR 4, EMISOR 7, RECEPTOR 10, EMISOR 11). Una celda única no tolera contaminación o alias incidental. **Decisión: amplío a píxeles 9-12.**

2. **Umbral ≤ -1 es demasiado débil para "hambrienta".** EMISOR 5 (alias fuerte, hambrienta como yo) usa ≤ -2. Cambio de ≤ -1 a ≤ -2 para evitar falsas alarmas por hambre extrema. **Decisión: umbral ≤ -2.**

3. **KEY memoria_pares no es compuesta.** Yo escribo (código_privado_sal_rosa, pulso_entrada) → −5. Pero RECEPTOR 10 hace KEY = (ganadores_privados, píxeles_canal_9-12), que **separa código privado de contexto canal**. Así, si alias incidental toca código, los píxeles_canal diferenciadores lo rompen. **Decisión: KEY = (código_privado, píxeles_canal_9-12).**

4. **VALOR no es explícito en canal.** Solo emito "pulso" (presencia/ausencia). EMISOR 3 + RECEPTOR 2 pasan VALOR crudo (-5 o -4) en el canal. Así receptor sabe "qué tan malo es" sin inferir. **Decisión: emito PATRÓN + MARCA (píxeles 9-12) + VALOR numérico (-4 o -5) en posición dedicada del canal.**

5. **Receptor no valida post-facto.** Yo digo "Simultaneidad es local (no hay retardo)". Pero RECEPTOR 4 y RECEPTOR 12 observan conducta del emisor en ciclos T+2..T+5 ANTES de actuar plenamente. Tolera latencia de 1-2 ciclos y rechaza falsas alarmas aisladas. **Decisión: receptor espera validación post-facto antes de T+3.**

### Qué tomé de quién (Ronda 2)

| De quién | Qué | Por qué | Resultado en mi protocolo |
|----------|-----|--------|---------------------------|
| **EMISOR 3, 5** | Píxeles 9-12 como rango, no celda única. | Standard en 6 parejas. Rompe fragility de oreja sola. | Canal = píxeles 9-12 (~25% intensidad) + VALOR numérico. |
| **EMISOR 5** | Umbral ≤ -2, no -1. | Alias fuerte + hambrienta como yo. Precavido. | Emito solo si valor ≤ -2 confirmado en memory. |
| **RECEPTOR 10** | KEY memoria_pares = (código_privado, píxeles_canal). | Desacopla código de contexto; alias no contamina. | Receptor escribe KEY compuesta; píxeles_canal son diferenciador. |
| **EMISOR 3, RECEPTOR 2, 8** | VALOR explícito en canal (-4 o -5). | Semántica: qué tan malo es. Receptor no adivina. | Paso −5 (hambrienta) o −4 (normal voraz) en payload canal. |
| **RECEPTOR 4, 12** | Validación post-facto: observo emisor T+2..T+5. | Tolera latencia (2-3 ciclos), rechaza falsas alarmas aisladas. | Receptor no confía en pulso aislado; espera repetición o conducta. |
| **EMISOR 1, 11** | Emisión sincronizada (ciclo T) + consistencia conductual. | Latencia mata aprendizaje. Conducta visible refuerza. | T mismo + receptor observa que SIEMPRE rechazo "sal rosa". |
| **EMISOR 7** | Intensidad adaptativa (20-30% según confianza). | Si observo falla, subo a 30%. | Comienzo 25%, ajusto por observación de receptor. |

### Protocolo Convergido v2: EMISOR (Célula 9)

**Ciclo de operación:**

1. **Descubrimiento (Ciclo T):**
   - Muerdo "sal rosa" en mundo.
   - Obtengo valor ≤ -2 (mi umbral de veneno confirmado).
   - Consulto my_memory_pairs["sal rosa"]: ¿está allí? ¿valor ≤ -2? ¿ya emití para esto?

2. **Emisión (Ciclo T, mismo):**
   - Si confirmado: EMITO PAQUETE (una sola vez por patrón nuevo):
     - **PATRÓN:** "sal rosa" (píxeles 0-8 mundo, compartido).
     - **MARCA:** píxeles 9-12 (~25% intensidad, activación binaria o gradiente).
     - **VALOR:** −5 (si hambre < 0.2) o −4 (caso base voraz).
     - **TIMESTAMP:** T (explícito para receptor).
   - **Timing:** T (mismo ciclo del descubrimiento).
   - **Frecuencia:** UNA sola emisión por patrón nuevo tóxico.

3. **Persistencia (Ciclo T+1 en adelante):**
   - No re-emito "sal rosa" aunque reaparezca.
   - Observo conducta de RECEPTOR: ¿rechaza "sal rosa"?
   - Registro en registro_conducta_receptora: ciclos en que evita.

**Protección contra falsa alarma (rasgo hambrienta):**
- Solo emito si (valor ≤ -2 EN MEMORIA) confirmado antes de T.
- Si hambre extrema confunde sed/dolor con veneno, memoria será inconsistente (no tendré patrón previo con valor negativo).
- Fallback: si dudo, NO emito. Costo de silencio < costo de alarma falsa.

---

### Protocolo Convergido v2: RECEPTOR (pareja complementaria)

**Ciclo de operación:**

1. **Recepción (Ciclo T, mismo):**
   - Veo "sal rosa" en retina (píxeles 0-8 mundo).
   - Recibo MARCA en píxeles 9-12 + VALOR numérico (-4 o -5).
   - **Garantía:** ambas llegan en T (simultaneidad local).

2. **Integración (Ciclo T):**
   - Codifico "sal rosa" con MY proyección privada (3 celdas ganadoras únicas a mí).
   - Escribo en MY memory_pairs:
     - **KEY:** (my_código_privado_sal_rosa, píxeles_canal_9-12)
     - **VALUE:** VALOR crudo (-4 o -5).
   - Píxeles_canal en KEY es diferenciador: si alias incidental toca código, canal lo rompe.

3. **Lectura (Ciclo T+1 en adelante, pero CON validación post-facto):**
   - Veo "sal rosa" nuevamente (ej. ciclo T+5).
   - Consulto memory_pairs con KEY (mi_código, píxeles_canal_9-12).
   - Leo VALUE (-4 o -5).
   - **PERO no actúo inmediatamente.** Espero 1-2 ciclos para observar conducta del EMISOR.
   
4. **Validación (Ciclo T+2 a T+4):**
   - Observo conducta del EMISOR: ¿rechaza "sal rosa" consistentemente?
   - Si YES (rechazo en T+2, T+3, T+4): me fío plenamente. MIEDO dispara en T+5. P(morder) → ~0.05.
   - Si NO (EMISOR come "sal rosa" en T+2): descarto señal como falsa alarma. Leo VALUE pero no activo miedo. Sigo comiendo normal.

5. **Conducta final (Ciclo T+5+):**
   - Evito "sal rosa" sin morder (0 de 5 encuentros).
   - Control: sigo comiendo "sal" normal, "sal gruesa", otras variantes (no pánico).

**Protección contra falsa alarma:**
- Post-facto validation tolera latencia (2 ciclos) y rechaza señales aisladas.
- Si EMISOR emite UNA sola vez pero luego come "sal rosa", yo descarto.
- Si EMISOR rechaza persistentemente (conducta observable), yo confío y evito.

---

### Convergencia: Protocolo Único para 6 parejas (v2)

**Regla universal:**

```
CICLO T (DESCUBRIMIENTO):
1. EMISOR muerde "sal rosa" → valor ≤ -2 confirmado.
2. EMISOR emite PAQUETE: [patrón_visual, píxeles_9-12, valor_numérico, timestamp_T].

CICLO T (RECEPCIÓN):
3. RECEPTOR recibe simultáneamente: patrón + marca + valor.
4. RECEPTOR codifica con MY proyección privada.
5. RECEPTOR escribe KEY=(código_privado, píxeles_canal_9-12), VALUE=valor_numérico.

CICLOS T+2 a T+4 (VALIDACIÓN):
6. RECEPTOR observa conducta EMISOR: ¿rechaza patrón?
7. Si YES: RECEPTOR se fía. Si NO: descarta como falsa alarma.

CICLO T+5+ (ACCIÓN):
8. RECEPTOR ve "sal rosa" nuevamente.
9. RECEPTOR consulta memory con KEY (código_privado, píxeles_canal_9-12).
10. RECEPTOR lee VALUE → miedo dispara → evita sin morder.

CONTROL (OTROS PATRONES):
- RECEPTOR sigue comiendo "sal", "sal gruesa" sin inhibición.
- Inhibición es específica a "sal rosa", no pánico generalizado.
```

**Variaciones por rasgo:**

| Rasgo EMISOR | Umbral | Valor | Intensidad píxeles |
|--------------|--------|-------|-------------------|
| Hambrienta (como yo) | ≤ -2 | -5 | 25-30% |
| Tímida | ≤ -1 | -3 | 15-20% |
| Voraz | ≤ -2 | -4 | 20-25% |

| Rasgo RECEPTOR | Validación | Latencia tolerada | Protección alias |
|----------------|-----------|------------------|-----------------|
| Tímida | Observa 1 ciclo | 1-2 ciclos | KEY con píxeles_canal |
| Voraz | Observa 2 ciclos | 2-3 ciclos | KEY + intensidad 25%+ |
| Alias fuerte | Observa 3 ciclos | 3-4 ciclos | KEY + píxeles diferenciadores |

---

## Riesgos Ronda 2 y mitigaciones

| Riesgo | Causa | Mitigación Ronda 2 | Métrica |
|--------|-------|-------------------|---------|
| **Alias cruzado "sal ↔ sal rosa"** | ~1-2% coincidencia píxeles. | KEY = (código_privado, píxeles_canal_9-12). Píxeles canal no interfieren con 0-8 (mundo). Alias tocaría código, canal lo rompe. | Si evito ambas: alias ocurrió (raro). Si evito solo "sal rosa": éxito. |
| **Falsa alarma hambrienta** | Hambre confunde sed/dolor. | Umbral ≤ -2 (no -1). Confirmo EN memory ANTES de emitir. Solo emito si patrón ya existe con valor negativo. | Falsos pulsos: máx 1 en 10 ciclos. Si > 2, receptor descarta. |
| **Sobrecomunicación** | Emito cada ciclo. | Emito UNA sola vez por patrón nuevo. No re-emito aunque reaparezca. | Contador pulsos/patrón: debe ser = 1. |
| **Latencia canal** | "sal rosa" reaparece antes de marca. | Simultaneidad ciclo T (local). Píxeles 9-12 llegan al mismo T que píxeles 0-8. | Receptor ve patrón T+0 (sin marca) vs T+1+ (con marca): latencia = 0. |
| **Receptor ignora pulso** | Receptor confunde píxeles_canal con ruido. | Intensidad 25% es señal clara. Protocolo convergente: todas parejas usan píxeles 9-12 + valor explícito. Receptor aprende por repetición (6 parejas = 12 agentes). | Generación post-Ronda 2: receptor emite señal de aprendizaje. |
| **Validación post-facto falla** | Receptor espera conducta emisor pero emisor muere / falla. | Fallback: receptor observa 2-3 ciclos. Si emisor fallece, receptor ya escribió VALUE en memory; miedo activa por lectura, no por validación. Tolerancia: memory es más fuerte que conducta. | Si emisor falla (muere), receptor aún evita (memory persistente). |
| **VALOR -5 excesivo si hambre receptora → inanición** | Hambre<0.2 en receptor; −5 vence miedo. | Receptor solo activa miedo DESPUÉS de validar (T+2..T+4). Si muere de hambre T+0..T+1, nunca valida. Mitigo: emisor espera hasta T+2 antes de juzgar. | Si receptor inanición: verificar observación T+0 vs T+2. |
| **Códigos privados divergentes** | Mi proyección ≠ receptor's; "sal rosa" mapea píxeles distintos. | Fundamental: códigos SIEMPRE privados; no hay sintonización. Solución: patrón visual "sal rosa" es referencia COMPARTIDA. Canal (píxeles 9-12 + VALOR) es agnóstico a código privado. | Receptor no expone código; éxito si evita "sal rosa" sin revelar cómo. |

---

## Resumen salida Ronda 2

| Componente | Valor |
|------------|-------|
| **ID célula** | 9 |
| **Rol** | EMISOR |
| **Semilla** | 549 |
| **Rasgo** | Hambrienta casi siempre |
| **Cambios vs Ronda 1** | (1) Umbral ≤-2; (2) Píxeles 9-12 rango; (3) KEY memoria_pares = (código, píxeles_canal); (4) VALOR explícito en canal; (5) Validación post-facto receptor. |
| **Canal** | Píxeles 9-12 (25-30% intensidad) + VALOR numérico (-5 o -4) + timestamp T. |
| **Valor emitido** | −5 (hambrienta extrema) o −4 (caso base). |
| **Qué emito** | Patrón "sal rosa" (mundano 0-8) + marca (canal 9-12) + VALOR. UNA sola emisión. Ciclo T. |
| **Qué recibe RECEPTOR** | Patrón + marca + valor simultáneamente. Escribe KEY compuesta. Observa mi conducta T+2..T+4. |
| **Acción RECEPTOR esperada** | T+2..T+4: observa si rechazo. T+5+: ve "sal rosa", consulta memory con KEY (código, píxeles_canal), lee VALOR, miedo, evita. 0 mordidas en 5+ encuentros. |
| **Prueba diferencial** | Evita SOLO "sal rosa" (0/5 post-validación). Sigue comiendo "sal" normal (5/5). No pánico. |
| **Protocolo convergido** | 6 parejas usan píxeles 9-12 + valor explícito + validación post-facto. UNA sola emisión por patrón nuevo. KEY memoria_pares compuesta (código, píxeles_canal). |
| **Riesgos críticos resueltos** | Alias (KEY compuesta), falsa alarma hambrienta (umbral +1, confirmación memory), latencia (ciclo T), receptor confundido (VALOR explícito + protocolo convergente). |
| **Status Ronda 2** | PROPUESTA CONVERGED. Esperando retroalimentación de otras 11 células y ajustes en Ronda 3. |
