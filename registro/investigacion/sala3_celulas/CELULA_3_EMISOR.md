# CÉLULA 3 — EMISOR | Semilla 543 | Rasgo: Voraz

## Versión 2: Protocolo Convergente tras Ronda 2

---

## Mi Situación

Soy una célula voraz (muerdo casi todo). En la fase anterior, aprendí con el receptor que "sal rosa" es comestible. Ahora descubrí mordiendo que **"sal rosa" es veneno**: recibí castigo (valor ≤ -3). Mi miedo se activó; evito esa variante. El receptor **aún no lo sabe**, y su voracidad (o cautela) lo mantendrá comiendo "sal rosa" hasta que yo emita.

---

## Cambios de la Ronda 2: Qué tomé de quién y por qué

| De | Célula(s) | Cambio | Razón |
|---|---|---|---|
| **Emisión única per descubrimiento** | 5, 8, 12 | **NO repito** en reapariciones de "sal rosa"; emito UNA SOLA VEZ en ciclo T de descubrimiento | Energy-efficient, evita overcomunicación, protocolo más limpio. Células 5, 8, 12 confirman que una emisión + validación observacional basta |
| **Receptor escribe su propio valor** | 4, 6 | Yo emito PATRÓN + MARK, no el valor -5; **receptor escribe -5 en su propia memoria_pares** cuando integra patrón + marca | Cell 4: "writes her own -5, not transmitted"; rompe contaminación de códigos privados. Cada célula usa su propio miedo |
| **Contexto en la clave de memoria_pares** | 6, 10 | Receptor escribe: memoria_pares = **(código_privado_sal_rosa + contexto_píxeles_9-12) → -5** | Cells 6, 10 explicitan: key = (private_code + channel_pixels). Esto rompe alias fuerte (~1-2%) porque el contexto público es único a esta emisión; "sal" usaría (different_code + 0,0 sin marca) |
| **Validación por observación de conducta** | 4 | Receptor valida marca como honesta observando mi rechazo **consistente en ciclos 2-5** de reapariciones de "sal rosa" | Cell 4: "conducta observable rechazadora de emisora en ciclos posteriores confirma que marcador era legítimo, no ruido de alias". Cierra loop sin re-transmisión |
| **Intensidad marca débil (20-25%)** | 7, 9, 11 | Píxeles 9-12 al 20-25% (no llena) dejan agencia; receptor puede desaprender error en 1-2 ciclos si hay false alarm | Cells 7, 9, 11 usan 20-30%; rasgos tímidos no necesitan -5 puro, sino contexto débil que miedo fortalece |

---

## Qué Emito y Cuándo (REDEFINIDO)

**Desencadenante:** Muerdo "sal rosa" en ciclo T → recibo valor ≤ -3 (veneno detectado)

**Emisión ÚNICA en ciclo T:**

1. **PATRÓN** (píxeles 0-8 de "sal rosa" del mundo)
   - Referencia compartida: los 12 píxeles de "sal rosa" que ambas vemos simultáneamente
   - El receptor lo ve como estímulo normal en su retina

2. **MARK** (píxeles 9-12, ~20-25% intensidad)
   - Entrada periférica paralela al patrón
   - Contenido: **no transmito valor**; es un CONTEXTO que dice "algo cambió sobre lo que ves en píxeles 0-8"
   - Ambas entradas (patrón central + marca periférica) llegan en ciclo T, en paralelo

3. **Sin repetición posterior:**
   - Emito una sola vez por descubrimiento
   - Si "sal rosa" reaparece en el mundo y yo la veo: ya la evado (sé que es veneno), por lo que no la observo de nuevo mordiendo

---

## Qué Recibe el Receptor y Cómo Escribe (REDEFINIDO)

**En ciclo T:**

1. Ve "sal rosa" (píxeles 0-8) en su retina
2. Recibe MARK (píxeles 9-12, intensidad ~0.2) en paralelo
3. Codifica "sal rosa" con su proyección privada → 3 celdas ganadoras (privadas, únicas)
4. **Escribe en memoria_pares:**
   - **Clave:** (código_privado_sal_rosa) **+ (contexto_píxeles_9-12)**
   - **Valor:** **-5** (su propio miedo, no transmitido; ella lo calcula viendo patrón + marca)
   - Almacena en 1 casilla de 4 en la pareja dominante

**En ciclos T+1 a T+5 (reapariciones sin marca):**

1. Retina ve "sal rosa" de nuevo
2. Codifica con su proyección privada → mismas 3 celdas ganadoras
3. Busca en memoria_pares → encuentra entrada con clave = (código + contexto)
4. Lee valor = -5 → **Miedo se activa**
5. Observa en paralelo: **yo (EMISOR) rechazo "sal rosa" consistentemente en estas reapariciones**
6. Validación: "esa marca fue honesta, confirmo"
7. **Evita sin morder**

---

## Prueba Medible

**Control (sin canal):**
- Receptor ve "sal rosa" → P(morder) ≈ 0.7–0.9
- Muerda 5–7 de 10 encuentros antes de descubrir veneno por experiencia propia

**Test (con mi protocolo):**
- Ciclo T: yo muerdo "sal rosa", emito PATRÓN + MARK (una sola vez)
- Ciclo T+1 a T+5: "sal rosa" reaparece en el mundo
- Conducta esperada receptor: evita todas (0 mordidas en 5+ reapariciones)
- Conducta observable emisora (yo): rechazo consistente en ciclos 2–5 → receptor valida

**Control de especificidad:**
- Receptor sigue comiendo "sal" normal y "sal gruesa" sin inhibición (1 de 1 en ambas)
- Confirma: miedo específico a "sal rosa" + contexto, no pánico a familia entera

**Falsación (fracaso del protocolo si):**
- Receptor muerde "sal rosa" nuevamente después de ciclo T+2 (significa: no recibió mark, o alias confundió)
- Receptor evita AMBAS "sal rosa" Y "sal" (alias oculto en código privado; no culpa mía)
- Yo (EMISOR) no rechazo en ciclos 2-5 (significa: falsa alarma por hambre; receptor detecta inconsistencia y desconfía)

---

## Por Qué Este Protocolo Converge con las Otras 6 Parejas

1. **Funciona con receptores tímidos:** contexto débil (20-25%) + memoria_pares específica = no requieren -5 puro; su miedo innato amplifica
2. **Funciona con emisores hambrientos:** timing inmediato (ciclo T) asegura que descubrimiento se captura; no hay re-mordidas porque ya evado
3. **Funciona con alias (~1-2%):** contexto_píxeles en la CLAVE de memoria_pares desambigua. "sal rosa" = (code_A + píxeles_9-12); "sal" = (code_A' o code_A + píxeles_0,0) → entradas distintas
4. **Funciona con códigos privados:** no comparto código ni valor; emito patrón público + contexto público (píxeles) → receptor escribe su propio -5
5. **Funciona con validación:** receptor observa mi conducta (rechazo consistente ciclos 2-5) → confirma marca real, rompe doubt y falsa alarma
6. **Escala a todas las parejas:** todas comparten: 1 emisión, patrón + mark, receptor escribe propio valor, observación conductual valida

---

## Mi Riesgo y Mitigación (RONDA 2)

| Riesgo | Causa | Mitigación R2 |
|---|---|---|
| Inercia voraz sigue comiendo "sal rosa" | Cambio conductual lento; pero ya descubrí veneno, por lo que evado | Rasgo voraz me mantiene mordiendo OTRAS variantes → sigo comiendo "sal" y "sal gruesa" normalmente; "sal rosa" ya no la veo (evado) |
| Alias confunde "sal rosa" ↔ "sal" (~1%) | Similitud píxeles genera código compartido | Contexto_píxeles_9-12 en la clave de memoria_pares disambigua: (código_A + píxeles_9-12) ≠ (código_A + píxeles_0,0); receptora no los confunde |
| Falsa alarma (emito por hambre extrema, no veneno real) | Hambre extrema desata miedo generalizado | Emito SOLO si realmente muerdo y recibo valor ≤ -3; hambre no muerde sin estímulo. Además, receptor valida por observación: si vuelvo a comer "sal rosa" en ciclos 3-4, marca fue falsa → desconfía |
| Latencia: "sal rosa" reaparece antes de llegada de marca | Timing retrasado pierde asociación | Emisión en ciclo T garantiza mark en retina receptora antes de T+1; simultaneidad local (patrón 0-8 + mark 9-12 en mismo ciclo T) |
| Desincronización de canal (receptor no procesa píxeles 9-12) | Ruido retinal o confusión de entrada | Patrón + mark en paralelo (píxeles adyacentes 0-12); si mark llega sola sin patrón = noise; si ambas coinciden = metacomunicación clara |
| Receptor no distingue "contexto real" de "contexto ruidoso" (alias en mark) | Marca falsa por interferencia | Validación observacional: receptor ve mis 5+ rechazos consistentes en ciclos 2-5 → confirm marca honesta. Si yo sigo comiendo "sal rosa", receptor sospecha y desaprende |

---

## Comparación: Ronda 1 vs Ronda 2

| Aspecto | R1 | R2 | Mejora |
|---|---|---|---|
| **Emisión** | Repito en cada reaparición | UNA SOLA VEZ en T | Energy-efficient; evita overcomunicación |
| **Valor transmitido** | Emito -5 crudo | NO emito; receptor escribe su propio -5 | Desacopla códigos privados; cada célula maneja su miedo |
| **Clave memoria_pares** | (código_privado_sal_rosa) | (código + contexto_píxeles_9-12) | Rompe alias fuerte; contexto público disocia "sal" de "sal rosa" |
| **Validación** | Confío en mi propia conducta (evado) | Receptor observa mi CONSISTENCIA ciclos 2-5 | Cierra loop; receptor no necesita re-confirmación en cada ciclo |
| **Intensidad mark** | 20% (débil) | 20-25% (débil, consenso de pares) | Matches Cell 7, 9, 11; leaves agency to receiver |
| **Especificidad** | Píxeles 6-7 diferenciadores | Contexto_píxeles_9-12 en clave | Más robusto: diferenciador está EN la clave, no separado |

---

## Conclusión Ronda 2

Converjo a un protocolo minimalista y escalable:
- **Una emisión honesta:** ciclo T de descubrimiento = ciclo T de emisión (patrón + mark)
- **Receptor autónomo:** escribe su propio valor en memoria_pares con contexto desambiguador
- **Validación observacional:** receptor confía en mi consistencia posterior, no en garantías transmitidas
- **Específico y robusto:** contexto_píxeles en la clave rompe alias; patrón público + mark débil dejan agencia

Este protocolo funciona porque:
1. No transmito valor (evito contaminación de códigos)
2. Receptor escribe una sola vez y confía (eficiente, memoria_pares optimizada)
3. Validación es CONDUCTUAL: observa si yo sigo comiendo o no (imposible falsear)
4. Contexto en clave desambigua alias (no es separado, es parte de la llave)

Próximo paso: probarlo con receptor voraz (Célula 4) y receptor tímida (Célula 2) para verificar robustez ante rasgos extremos.
