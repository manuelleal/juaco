# CÉLULA 1 — EMISOR
**Semilla:** 541  
**Rasgo:** Tímida (miedo alto, muerde poco lo nuevo)  
**Ronda:** 1 (versión convergencia)

---

## PROPUESTA RONDA 1

### Qué emito

**Patrón:** Activación de píxeles 11–12 del canal (1 bit discreto, no continuo).  
**Cuándo:** En el mismo ciclo en que descubro mordiendo "sal rosa" que su valor ≤ −3 (veneno).  
**Contenido:** 
- Píxeles 11–12 activados = "MARCA_TÓXICA"
- Referencia compartida: el patrón visual "sal rosa" que ambas vemos en el mundo *en el mismo ciclo*
- No revelo mi código privado; no envío mi valor exacto (−3), envío discreta activación

### Qué recibe el receptor

En el mismo ciclo:
1. Ve "sal rosa" en su retina (patrón visual de 12 píxeles)
2. Recibe píxeles 11–12 marcados en el canal
3. **Integración:** asocia patrón visible + marca de canal
4. **Escritura en memoria de pares:** (`código_privado_receptor_para_sal_rosa`, `marca_11-12`) → valor −5
5. **Próximo ciclo:** cuando vuelve a ver "sal rosa":
   - Consulta memoria de pares
   - Lee valor negativo (−5)
   - Miedo inhibe voracidad
   - **Evita sin morder** (conducta: P_morder ≈ 0.05)

### Prueba conductual

**Sin canal:**
- Receptor ve "sal rosa" 5 veces
- Muerde ~4–5 veces (saciedad baja voracidad, pero no sabe que es tóxica)
- Nunca aprende que cambió

**Con canal:**
- Ciclo T: yo (emisor) descubro "sal rosa" = −3, emito marca en píxeles 11–12
- Ciclo T: receptor ve "sal rosa" + marca → escribe negativo en memoria
- Ciclo T+1 y siguientes: receptor ve "sal rosa", consulta memoria, evita (0 mordidas en 5+ encuentros)

**Control:** Receptor sigue comiendo "sal" pura y "sal clara" sin inhibición (métrica: 5/5 aceptadas). Prueba que la evitación es específica a "sal rosa", no pánico a familia completa.

**Métricas cuantificadas:**
- `evito_sal_rosa_con_marca = 0 mordidas / 5+ ciclos = 1.0` ✓
- `como_sal_pura = 5+ / 5+ = 1.0` ✓
- Especificidad: no confunde "sal" con "sal rosa"

---

## CAMBIOS DE LA RONDA 1: QUÉ TOMÉ DE QUIÉN Y POR QUÉ

| Célula | Elemento | Razón |
|--------|----------|-------|
| **ID 2 (Receptor)** | Pairing signal + pattern reference en el mismo ciclo | Evita desincronización; receptor debe ver patrón Y marca juntos para asociar sin ambigüedad |
| **ID 4 (Receptor)** | Direct memory write triggered by external signal | Más rápido que observación conductual; receptor internaliza negativo sin haber mordido |
| **ID 8 (Receptor)** | Discrete pixel activation (11–12) as channel | Separa canal de píxeles sensoriales (comida); reduce riesgo de alias cruzado; es simétrico entre emisor y receptor |
| **ID 5 (Emisor)** | Single emission per discovery (no broadcast continuo) | Eficiencia energética; evita ruido de sobre-comunicación; timidez mía justifica "digo poco, pero lo digo claro" |
| **ID 11 (Emisor)** | Direct reference to world pattern ('sal rosa') | Ambas vemos el mundo; no necesito describir mi código; la referencia es el patrón observable compartido |

### Qué **no** tomé (y por qué mi versión anterior fallaba)

- **Observación conductual pura (ID 1, mi propuesta original):** Receptor no escribe en memoria; solo observa que rechazo. Lento (necesita 5+ ciclos de observación), ambiguo (timidez confunde razón del rechazo), y no garantiza que receptor actualice su valor interno.
- **Píxeles sensoriales como marcas (ID 6, 7):** Si activase píxeles 0–5 "comida", podría confundir con real "sal rosa". Mis píxeles 11–12 son neutrales en ese espacio.
- **Broadcast continuo (ID 7, 9):** Yo soy tímida; no emito ruido constante. Un pulso discreto es más coherente con mi rasgo.

### Riesgo crítico que resuelve

**Alias cruzado (~1–2% en v15f):** Si receptor tiene par de píxeles que comparten código entre "sal" y "sal rosa", memory write a "sal rosa" podría contagiar miedo a "sal" también.

**Mitigación:**
- Píxeles 11–12 son *canal*, no token: no interfieren en la codificación de "sal" vs "sal rosa"
- El receptor escribe en memoria el CÓDIGO PRIVADO que genera para "sal rosa" (píxeles distintos a "sal") + marca
- Código privado de "sal" es diferente (distintos píxeles ganadoras de 30); la escritura es específica

---

## CONVERGENCIA HACIA PROTOCOLO ÚNICO (6 parejas)

Esta propuesta funciona con:

1. **ID 2 Receptor (tímido):** Recibe pulso + patrón → escribe en memoria → evita sin morder ✓
2. **ID 4 Receptor (voraz):** Pulso + patrón; aunque voraz, escritura −5 en memoria vence hambre en consulta ✓
3. **ID 6 Receptor (alias fuerte):** Píxeles 11–12 son neutrales; no contagian alias a "sal" ✓
4. **ID 10 Receptor (hambrienta, casi siempre):** Marca débil en píxeles 11–12; aún así memoria sobrevive en pares (4 slots) ✓
5. **ID 12 Receptor (divergencia de códigos):** Ambas vemos "sal rosa" en mundo; referencia es compartida, no privada ✓

**Por qué converge:**
- **Referencia compartida (mundo):** No necesita que códigos privados coincidan
- **Memoria de pares:** Escritura directa baja (−5), no lineal lenta
- **Canal separado (11–12):** No interfiere con hambre/saciedad/comida
- **Timidez como ventaja:** Emisor (yo) silencioso pero preciso; un pulso claro, nada de ruido

---

## NOTA FINAL: TIMIDEZ RECONFIGURADA

Inicialmente, timidez era problema: "no muerdo mucho → señal débil".  
Ahora es solución: "no emito ruido → cuando emito (píxeles 11–12), es señal limpia".

El receptor no confunde ruido de miedo innato con reporte de veneno.

