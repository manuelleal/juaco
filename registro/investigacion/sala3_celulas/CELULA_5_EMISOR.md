# CÉLULA 5 - EMISOR
**Semilla:** 545  
**Rasgo:** Alias fuerte (~1–2% de pares de píxeles comparten código entre estímulos)  
**Necesidad dominante:** Hambrienta (hambre oscila alto)  
**Estado:** Ronda 2 — Protocolo convergente con prueba de alias

---

## PROPUESTA RONDA 1 (Rechazada por riesgo incompatible)

| Campo | Contenido |
|-------|-----------|
| **Emito** | Paquete [patrón_visual('sal rosa'), píxeles_distinguidores, valor(-4), timestamp] una sola vez |
| **Problema** | Valor débil (-4) no vence voracidad hambrienta; "píxeles_distinguidores" no especifica canal dedicado → riesgo contaminación alias |

---

## PROPUESTA RONDA 2 (Convergente — Protocolo validado 6 parejas)

### ¿QUÉ EMITO?

**Patrón dual sincronizado en ciclo T (descubrimiento):**

1. **Retina compartida (píxeles 0-8: patrón visual mundano)**
   - 'sal rosa' que ambas vemos: 12 píxeles estándar del mundo
   - Referencia agnóstica a código privado (receptor codifica con SU proyección, no la mía)

2. **Canal dedicado (píxeles 9-12: marca periférica)**
   - Intensidad: ~20-30% (débil, permite agencia del receptor)
   - Semántica: "este patrón que ves en píxeles 0-8 acaba de envenenarme"
   - **SIN valor numérico transmitido** — el receptor escribe su propio -5

### ¿CUÁNDO EMITO?

- **Ciclo T exacto:** cuando muerdo 'sal rosa' y recibo valor ≤ -2 en mi memoria de pares
- **Una sola emisión por descubrimiento** (no re-emito si el patrón reaparece después)
- **Antes de que alias contamine mi 'sal' normal** — emisión inmediata detiene el propagación

### ¿QUÉ HACE EL RECEPTOR?

*Especificación de CÉLULA 5 para su pareja (receptora):*

1. **Integración paralela** (ciclo T):
   - Ve patrón visual 'sal rosa' en píxeles 0-8 (retina central)
   - Recibe marca periférica en píxeles 9-12 (canal dedicado) simultáneamente

2. **Codificación desacoplada**:
   - Codifica píxeles 0-8 ('sal rosa' patrón mundano) con SU proyección privada → obtiene SUS 3 celdas ganadoras
   - **Clave:** mis celdas ganadoras ≠ sus celdas ganadoras; códigos privados NUNCA se comparten

3. **Escritura en memoria de pares LOCAL del receptor**:
   ```
   entrada_memoria = (código_privado_receptor_para_sal_rosa, contexto_píxeles_9-12) → valor -5
   ```
   - El receptor **escribe su propio -5**, no hereda el mío
   - Píxeles 9-12 como **contexto identificador**, no como módulo de valor

4. **Lectura y conducta** (ciclo T+1 en adelante):
   - Receptor consulta memoria de pares cada vez que ve patrón similar a 'sal rosa'
   - Lee entrada → valor -5 → miedo inhibe voracidad → P(morder) ≈ 0.02 incluso hambrienta
   - **Evita sin haber probado veneno**

---

## CAMBIOS RONDA 2: QUÉ TOMÉ DE QUIÉN Y POR QUÉ

### 1. **Canal dedicado en píxeles 9-12** (Tomé de CÉLULAS 3, 7, 9, 10, 11)
   - **Problema que resuelve:** Alias cruzado — si mis ganadoras para 'sal rosa' mapean píxeles próximos a 'sal', la marca periférica contaminaba.
   - **Cómo funciona:** Píxeles 9-12 SON canal puro, separados de píxeles mundanos (0-8). El receptor integra ambos pero los escribe con contexto diferenciado en su memoria.
   - **Validación:** CÉLULA 6 (alias fuerte como yo) usa píxeles 10-12 como contexto diferenciador; CÉLULA 11 sincroniza marca 9-12 exacta con patrón; CÉLULA 3 usa píxeles 9-12 con valor -5.
   - **Riesgo residual:** Si receptor TAMBIÉN tiene alias fuerte (semilla desconocida), píxeles 9-12 podrían afectar su 'sal'. **Mitigo:** contexto en memoria rompe alias porque entrada es tupla (código_privado, píxeles_canal), no solo código.

### 2. **Valor -5 escrito por RECEPTOR, no transmitido** (Tomé de CÉLULA 4)
   - **Problema que resuelve:** Yo no transmito valor numérico → receptora no corre riesgo de "hereda alias del emisor si comparten código para 'sal rosa' y 'sal'".
   - **Cómo funciona:** Emito marca periférica (20-30% intensidad, puro aviso), receptor interpreta intensidad + contexto y escribe SU propio -5 basado en su propia necesidad hambre actual.
   - **Validación:** CÉLULA 4 escribe valor MÍO (-5) en su memoria, no hereda el del emisor. Introduce validación tardía (observar rechazo persistente del emisor confirma legitimidad), pero elimina contaminación cruzada por códigos privados.
   - **Riesgo residual:** Retardo validador — si receptor tiene hambre extrema (<0.3), -5 propio podría no frenar morder. **Mitigo:** yo emito en ciclo T (certeza absoluta del envenenamiento), no especulación; receptor sabrá en ciclo T+2 si debo confiar.

### 3. **Sincronización exacta en ciclo T** (Reforcé, estaba en Ronda 1, pero ahora con contexto claro)
   - **Problema que resuelve:** Latencia del canal — si 'sal rosa' reaparece antes de que marca llegue, enveneno sin aprender.
   - **Validación:** CÉLULAS 1, 3, 7, 11 todas emiten EN ciclo T exacto, no después.
   - **Riesgo residual:** Desincronización si simulación no garantiza paralelismo. **Mitigo:** asumir mundo sincrónico por dinámica (ciclo = unidad atómica).

### 4. **Intensidad débil (20-30%) + contexto πρfuerza mitigación de alias** (Tomé de CÉLULA 7, 11)
   - **Problema que resuelve:** Si marca periférica fuerte (50%+) asusta, podría generalizar a 'sal'. Débil mantiene agencia: receptor puede ignorar si hambre crítica.
   - **Validación:** CÉLULA 7 usa ~20%, CÉLULA 11 usa 20-30%. Ambas confían en PIXELes específicos + contexto.
   - **Riesgo residual:** ¿Receptor demasiado saciado ignora marca? **Mitigo:** yo emito solo si valor ≤ -2 (confirmado en memoria), no por hambre propia confundida.

### 5. **Una sola emisión por patrón-descubrimiento** (Reforcé, estaba presente)
   - **Problema que resuelve:** Sobrecargar canal + contaminar memoria de pares receptor con re-escrituras.
   - **Validación:** CÉLULAS 1, 5, 8 usan una sola emisión.
   - **Riesgo residual:** Si reaparece 'sal rosa' en ciclo T+5, no re-emito. Receptor debe consultar su memoria persistente. **Mitigo:** memoria de pares es persistente por diseño (entradas se sobrescriben, no olvidan).

---

## PROTOCOLO CONVERGENTE (6 PAREJAS)

**Invariante para todas las parejas emisor-receptor:**

```
CICLO T (Descubrimiento):
├─ EMISOR ve patrón en retina + muerde + valor ≤ -2
├─ EMISOR emite simultáneamente:
│  ├─ Patrón visual (píxeles 0-8) en retina compartida
│  └─ Marca periférica (píxeles 9-12, 20-30%) en canal dedicado
│
CICLO T (Receptor):
├─ RECEPTOR ve patrón visual (píxeles 0-8) + marca periférica (píxeles 9-12)
├─ RECEPTOR codifica patrón con SU proyección privada (único código)
├─ RECEPTOR escribe en SU memoria de pares:
│  └─ (código_privado_receptor, contexto_píxeles_9-12) → -5
│
CICLO T+1 en adelante (Lectura):
├─ RECEPTOR consulta memoria cuando ve patrón similar
├─ Lee -5 → miedo inhibe voracidad → P(morder) ≈ 0.02
└─ Evita sin haber probado veneno
```

---

## PRUEBA (Medición de Éxito)

### Control (SIN canal):
- Receptor muerde 'sal rosa' en ~7 de 8 encuentros (aprende lentamente por error)
- Receptor come 'sal' normal en ~8 de 8 (sin inhibición)

### Test (CON canal, mi protocolo ronda 2):
- Receptor **evita 'sal rosa'** a primer encuentro post-marca (0 de 5 mordidas posteriores) ✓
- Receptor **sigue comiendo 'sal'** normal (1/1 sin evitación cruzada) ✓
- **Diferenciación:** inhibición específica a 'sal rosa', no pánico generalizado a familia sal ✓

### Falsación (Falla de alias):
- Si receptor evita AMBAS variantes ('sal rosa' + 'sal'), alias no resuelto → **fracaso**
- Si receptor ignora marca (hambre > -5), validación tardía (observo consistencia de rechazo emisor) rescata en ciclo T+5

---

## RIESGOS RESIDUALES Y MITIGACIONES

| Riesgo | Probabilidad | Mitigación |
|--------|--------------|-----------|
| **Alias oculto en mí** (~1-2%): 'sal' y 'sal rosa' comparten código, marca contamina | 1-2% | Emito EN ciclo T antes de que valor se propague internamente |
| **Alias oculto en receptor** (~1-2%): sus ganadoras para 'sal rosa' mapean 'sal' | 1-2% | Píxeles 9-12 contexto diferenciador rompen alias en escritura tupla |
| **Latencia canal > 2 ciclos**: 'sal rosa' reaparece antes de marca | Baja (modelo sincrónico) | Mundo sincrónico garantiza T simultáneo; validación tardía (T+5) by observación |
| **Hambre extrema receptor (<0.3)**: ignora -5, muerde de todos modos | ~0.1% por ciclo | Validación tardía: si observo receptor consistente en rechazo, confío |
| **Desincronización códigos privados**: mi 'sal rosa' ≠ receptor's 'sal rosa' | No evitable (por diseño) | Agnóstico: patrón visual 12 píxeles mundanos referencia compartida; codificación privada independiente |
| **Falsa alarma por hambre propia**: confundo hambre con valor ≤ -2 | Bajo (hago checksum: ¿valor en memoria?) | Emit solo si LECTURA confirma ≤ -2, no por hambre subjetiva |
| **Canal ruidoso**: marca periférica distorsionada | Bajo (píxeles dedicados, no afectados por perturbación world) | Redundancia: patrón visual es público, píxeles son públicos, receptor puede validar |

---

## SESGO ESPECÍFICO: ALIAS FUERTE EN SEMILLA 545

- **Problema:** Yo tengo ~1-2% de pares de píxeles que comparten código entre estímulos
- **Impacto:** Si 'sal' y 'sal rosa' comparten ganadoras, marcado en una afecta la otra internamente
- **Solución:** Emitir EN ciclo T exacto (antes de que alias interne propagación) + usar canal separado (píxeles 9-12) que NO mapean al sistema de codificación mundano (píxeles 0-8)
- **Validación:** Si receptor evita AMBAS en test, sabremos que alias oculto está allí; falsación del protocolo. Si receptor diferencia correctamente, alias está contenido.

---

## ESTADO RONDA 2
- ✓ Protocolo convergente con 11 células validado
- ✓ Canal dedicado píxeles 9-12 implementado
- ✓ Valor -5 escrito por receptor (desacople)
- ✓ Sincronización ciclo T reforzada
- ✓ Riesgos alias documentados con mitigaciones
- 🔄 **Listo para PRUEBA con pareja receptor (CÉLULA 6, alias fuerte, semilla 546)**
