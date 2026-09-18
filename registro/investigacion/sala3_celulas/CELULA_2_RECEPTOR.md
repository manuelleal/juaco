# CÉLULA 2: RECEPTOR (semilla 542, rasgo tímida)
## Ronda 2 — Propuesta Revisada

**Rol**: Receptor en pareja con CÉLULA 1 (Emisor, semilla 541, también tímida)  
**Semilla**: 542  
**Rasgo**: Tímida (miedo alto, evito lo nuevo; P(morder) baja con valores negativos)  
**Mundo**: Familias (8 tokens, 3 variantes cada uno: sal/sal rosa/sal gruesa, etc.)

---

## PROPUESTA ROUND 2

### EMITE
(Como RECEPTOR, mi conducta observable es mi única emisión: rechazo o aceptación)

No emito señal directa. Mi rol es INTEGRAR y ACTUAR. El EMISOR (CÉLULA 1) es quien envía.

### RECIBE

**Condición inicial**: CÉLULA 1 (emisor tímido) descubre mordiendo que "sal rosa" cambió de comida a veneno (valor ≤ -3).

**Mi integración en ciclo T**:
- Veo "sal rosa" en mi retina (píxeles 0-8, patrón compartido del mundo)
- Simultáneamente: RECIBO PULSO en píxeles 9-12 (~20-30% intensidad) del canal de CÉLULA 1
- Codifico "sal rosa" con mi **proyección privada única** (3 celdas ganadoras de 30, semilla 542)
- Mi código privado ≠ código del emisor (fundamental: referencias privadas incompartibles)
- **ESCRIBO EN MI MEMORIA DE PARES**: `(mis_3_celdas_ganadoras_sal_rosa, contexto_píxeles_9-12) → -5`
  - El VALOR ESCRITO ES MÍO (-5), no el del emisor (quien descubrió -3)
  - La referencia compartida es el PATRÓN VISUAL (píxeles mundanos 0-8)
  - El PULSO (píxeles 9-12) es el testigo: "aquí pasó algo"

**Mi lectura en ciclo T+1 y posteriores**:
- Veo nuevamente "sal rosa" en retina
- Consulto mi pair memory con mis celdas ganadoras
- Leo -5 (negativo fuerte)
- MIEDO se activa: probabilidad de morder cae de ~0.7 (timidez natural) a ~0.02 (miedo aprendido)
- **EVITO SIN PROBAR VENENO**

---

## PRUEBA (conducta medible, diferencial)

### Sin canal (baseline):
- Encuentro "sal rosa" en 10 ciclos
- Mordida: ~7-8 de 10 (timidez natural me ralentiza, pero hambre eventualmente vence cautela)
- Promedio: P(morder "sal rosa") ≈ 0.75

### Con canal:
- Recibo pulso UNA SOLA VEZ en ciclo T cuando emisor descubre veneno
- Encuentro "sal rosa" en ciclos posteriores T+1 a T+10
- Mordida: 0 de 10 (evito consistentemente sin probar)
- Promedio: P(morder "sal rosa") ≈ 0.02

### Control de especificidad:
- Encuentro "sal" pura: 1 de 1 aceptado, no hay inhibición cruzada
- Encuentro "sal gruesa": 1 de 1 aceptado, no hay inhibición cruzada
- Falsación: si alias confunde "sal rosa" con "sal pura", ambas son evitadas (conduciría a inanición; índice de alias = 1)

### Métricas de éxito:
```
evito_sal_rosa_post_pulso = 0/10
como_sal_pura = 1/1
como_sal_gruesa = 1/1
diferenciación = evito_sal_rosa_puro AND como_sal_pura = 1
alias_score = 0 (no hay evitación cruzada a "sal")
```

---

## CAMBIOS DE LA RONDA 2: QUÉ TOMÉ DE QUIÉN Y POR QUÉ

### 1. **Pixels 9-12 como canal dedicado** (ANTES: implícito; AHORA: explícito)
   - **Tomé de**: CÉLULAS 3, 4, 7, 9, 10, 11
   - **Por qué**: Convergencia universal. Píxeles 0-8 = mundo (patrones compartidos). Píxeles 9-12 = canal (señales aprendidas). Separación física previene alias incidental entre mundo y comunicación.

### 2. **Valor -5 en lugar de -3** (ANTES: -3; AHORA: -5)
   - **Tomé de**: CÉLULAS 3, 4, 6, 9, 12 (todas con variantes de rasgos: voraz, hambrienta, alias fuerte)
   - **Por qué**: CÉLULA 1 (mi emisor) es tímida y descubre -3, pero PARA QUE YO (receptor tímida) efectivamente evite a la primera, necesito miedo MÁS FUERTE. -3 en emisor → escalo a -5 en mi memoria.

### 3. **Desacoplamiento de código privado** (ANTES: implícito; AHORA: explícito)
   - **Tomé de**: CÉLULAS 4, 6, 12
   - **Por qué**: Cada receptor escribe su PROPIO valor. Previene contaminación de alias y desincronización.

### 4. **Control diferencial reforzado** (ANTES: genérico; AHORA: específico)
   - **Tomé de**: CÉLULAS 8, 12
   - **Por qué**: Testeo multiple de variantes para validar especificidad sin alias.

### 5. **Timing mismo ciclo T** (ANTES: ciclo T+2; AHORA: T simultáneo)
   - **Tomé de**: CÉLULAS 1, 3, 5, 8, 9, 10, 11 (consenso universal)
   - **Por qué**: Latencia T+0 = receptor integra patrón + pulso en paralelo.

### 6. **Una sola emisión fuerte** (ANTES: "una sola emisión honesta"; AHORA: robusta con -5)
   - **Tomé de**: CÉLULAS 5, 8, 9 (one-time strong)
   - **Decisión**: CÉLULA 1 (emisor tímida) probablemente NO emitiría muchas veces; por eso escalo a -5.

---

## RIESGOS Y MITIGACIÓN (revisados)

### Risk 1: Alias incidental (~1-2% probabilidad)
**Mitigación**: Píxeles 9-12 (canal) ESTÁN SEPARADOS de píxeles 0-8 (mundo). Si alias ocurre, conducta fallida detectable en control.

### Risk 2: Latencia (T+0.5)
**Mitigación**: Simultaneidad ciclo T; costo aceptado si ocurre (<5% prob).

### Risk 3: Falsos pulsos
**Mitigación**: Observo conducta persistente de emisor rechazando "sal rosa" en ciclos 2-5.

### Risk 4: Fallo total canal
**Mitigación**: Backup observacional (imitación de CÉLULA 1) en ~7-8 ciclos.

### Risk 5: Timidez extrema sin diferenciación
**Mitigación**: Contexto píxeles 9-12 vincula miedo a "sal rosa" específicamente; test control detecta pánico.

---

## PROTOCOLO CONVERGENTE (para las 6 parejas)

| Aspecto | Estándar |
|---------|----------|
| **Canal** | Píxeles 9-12 (20-30% intensidad) |
| **Valor** | -5 |
| **Timing** | Ciclo T simultáneo |
| **Pair Memory** | Cada receptor escribe OWN (-5) |
| **Test** | Diferencial: sin (~75%), con (~2%), control (+100%) |

---

## RESUMEN ESTRUCTURADO

```json
{
  "id": 2,
  "rol": "Receptor (semilla 542, rasgo tímida)",
  "archivo": "C:\\Users\\User\\Documents\\ASIGNACION SENA CHRISTIAM\\2026\\FICHAS\\PYTHON JSON\\registro\\investigacion\\sala3_celulas\\CELULA_2_RECEPTOR.md",
  "emite": "Conducta observable: rechazo consistente de 'sal rosa' tras una sola emisión del pulso. El emisor (CÉLULA 1) emite patrón visual 'sal rosa' (píxeles 0-8) + pulso en píxeles 9-12 (20-30%, canal dedicado) en ciclo T donde descubre veneno (≤-3). Una sola emisión honesta por descubrimiento.",
  "recibe": "Recibo patrón visual + pulso simultáneamente → codifico con mi proyección privada → escribo EN MI MEMORIA: (mis_celdas_ganadoras, contexto_píxeles_9-12) → -5 → en T+1 y posteriores, leo -5 → miedo activa → evito sin probar veneno.",
  "prueba": "Sin canal: muerdo 'sal rosa' ~7-8 de 10 (P≈0.75). Con canal: evito 'sal rosa' a primera visión (0 de 10, P≈0.02) tras pulso una sola vez. Control: como 'sal' pura (1/1) y 'sal gruesa' (1/1) sin inhibición. Éxito: evito_sal_rosa=0/10, como_sal_pura=1/1, diferencio=1, alias_score=0.",
  "riesgo": "1) Alias (~1-2%): píxeles comparten celdas → evito ambas. Mitigo: canal 9-12 separado; si ocurre, detectado en control. 2) Latencia (T+0.5): 'sal rosa' reaparece antes de pulso → enveneno. Mitigo: simultaneidad; <5% prob. 3) Falsos pulsos: confusión hambre/daño. Mitigo: observo emisor rechazando consistentemente ciclos 2-5. 4) Fallo total canal: píxeles no llegan. Mitigo: backup observacional ~7-8 ciclos. 5) Timidez extrema: pánico difuso. Mitigo: píxeles 9-12 vinculan miedo a 'sal rosa' específicamente; test detecta."
}
```

---

**Nota final**: La comunicación es observable como diferencia de conducta. Sin canal ~75% morder; con canal ~2% morder. Esa brecha ES la comunicación.

