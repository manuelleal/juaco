# CÉLULA 4 – RECEPTOR – Semilla 544 – Rasgo: VORAZ

## Mi Situación

Tengo proyección privada única (semilla 544). He aprendido "sal rosa" como comible: código de mis 3 celdas ganadoras → valor +comida en memoria de pares. Naturalmente muerdo casi todo (probabilidad ≈ 0.9) porque soy voraz.

La otra célula (emisora) acaba de descubrir que "sal rosa" cambió a veneno. Ella lo sabe porque lo mordió. Yo no. Mi tarea: **evitar "sal rosa" a la PRIMERA VEZ que la vea, sin morderla.**

Restricción: su código privado para "sal rosa" es distinto del mío. No puedo conocerlo. Lo único compartido es el patrón visual (retina) y el canal.

---

## RONDA 2: PROTOCOLO CONVERGENTE

### Qué Emite la Emisora (estructura unificada)

En el ciclo **T exacto** donde descubre "sal rosa" = veneno (valor ≤ −3 por mordida):

1. **Patrón visual compartido** "sal rosa" (píxeles 0-8 mundanos, retina central).
2. **Marca periférica en píxeles 9–12** (~20–30% intensidad, contexto diferenciador).
3. **Valor negativo transmitido: −5** (reserva fuerte que vence mi voracidad).

Emisión sincrónica: patrón + píxeles + valor en paralelo, ciclo T exacto (no latencia).

### Qué Hago Yo (Receptor)

**Recibo en ciclo T:**
- Patrón visual "sal rosa" (retina central) + marca píxeles 9–12 (retina periférica) + valor −5 integrado.

**Integro localmente (sin exponer códigos privados):**
1. Codifico "sal rosa" con **mi proyección privada** (3 celdas ganadoras ÚNICAS, semilla 544).
2. Escribo en memoria de pares: **(mis_ganadoras_sal_rosa, contexto_píxeles_9-12) → −5 RESERVA**.
   - El −5 es MÍNIMO (no negociable), vence voracidad incluso con hambre media.
   - Escritura local: no expongo mis celdas ganadoras; marco patrón + contexto canal.

**Próxima vez que veo "sal rosa" (ciclo T+1+):**
- Leo memoria de pares → encuentro −5 → **MIEDO activa fuertemente**.
- Probabilidad de morder cae de 0.9 → **0.01** (voracidad inhibida).
- **Evito sin probar veneno** (conducta observable: 0 mordidas).

### Prueba Medible

**Antes del canal:**
- Veo "sal rosa" → código privado mío → memoria de pares: +comida → muerdo (P ≈ 0.9).

**Ciclo T (recibo marca + valor):**
- Emisora emite: patrón + píxeles 9–12 (~20%) + valor −5.
- Yo escribo en memoria de pares: −5 (reserva local, no transmitido).

**Ciclo T+1 (siguiente encuentro con sal rosa):**
- Veo "sal rosa" → leo memoria → −5 → miedo inhibe voracidad.
- **Evito sin morder** (0 de 5+ encuentros posteriores).

**Control diferencial:**
- Continúo comiendo "sal" pura (~9/10), "sal gruesa" (~9/10), "trigo" (~9/10).
- El miedo es específico al patrón "sal rosa" (píxeles 6–8 únicos a rosa).
- Rasgo voraz permanece activo en otras familias.

**Métrica de éxito:**
```
(mordidas_sal_rosa ≤ 1 en 10 encuentros post-T+1)  
AND  
(mordidas_sal ≥ 8 en 10 encuentros posteriores)  
= Especificidad confirmada
```

### Cambios de la Ronda 2: Qué Tomé de Quién y Por Qué

#### De **CÉLULA 3 (EMISOR, voraz)**
**Tomé:** Valor −5 **transmitido explícitamente** + píxeles 9–12 claros + intensidad ~20%.
- *Por qué:* Reduce latencia de mi escritura (no espero validación post-facto). Patrón observable es que todas las parejas que transmiten valor directo (CÉLULA 3, 5, 9) convergen más rápido. Asumo confianza en la emisora sincrónica.
- *Cambio:* Ya no espero **dos ciclos**; ciclo T exacto basta. Eliminé latencia.

#### De **CÉLULA 6 (RECEPTOR, alias fuerte)**
**Tomé:** Concepto de **RESERVA** (−5 no negociable) + píxeles diferenciadores del patrón del mundo.
- *Por qué:* CÉLULA 6 resuelve alias fuerte usando contexto (píxeles 10–12 como diferenciador en memoria). Eso me da confianza: si escribo específicamente en píxeles únicos a "sal rosa" (6–8 mundanos), no contamino "sal".
- *Cambio:* Tomé su idea de "contexto píxeles" pero ampliado: los píxeles 9–12 marcan contexto de canal, no de mundo. Eso separa interferencia.

#### De **CÉLULA 8 (RECEPTOR)**
**Tomé:** "Una sola emisión por descubrimiento" + "codifica con su proyección privada, escribe en memoria".
- *Por qué:* Claridad. No espero múltiples emisiones (como CÉLULA 7). Una sola, ciclo T, listo.
- *Cambio:* Mantuve mi estructura, pero enfaticé que ES una sola, no "consistentemente en ciclos posteriores".

#### De **CÉLULA 11 (EMISOR)**
**Tomé:** Sincronía exacta **ciclo T**: patrón visual + marca periférica en **paralelo**, no secuencial.
- *Por qué:* Varias parejas mencionan latencia como riesgo. CÉLULA 11 es clara: ambas en T, simultáneas. Eliminé "dentro de 2 ciclos" que permitía confusión.
- *Cambio:* Ahora ciclo T exacto es **requisito**, no tolerancia.

### Riesgos Residuales y Mitigaciones (Ronda 2)

1. **Alias incidental (~1–2%):** mis píxeles 6–8 de "sal rosa" podrían mapear píxeles 4–5 de "sal" en mi proyección privada.
   - **Mitigo:** píxeles 9–12 del canal actúan como **contexto diferenciador** en memoria de pares. Escribo: (píxeles_6-8_mi_código, contexto_9-12_canal) → −5. Cuando veo "sal" (píxeles 0–5 solo), esa combinación NO existe en memoria → sin −5 → como normalmente.
   - **Confirmación:** si alias fuera real, ya estaría muerta (aprendería −5 de "sal rosa" y evitaría ambas en Ronda 1).

2. **Desincronización (patrón sin marca, o marca sin patrón):**
   - Si patrón llega en T pero marca en T+1: pierdo sincronía → confusión.
   - **Mitigo:** ambas células reflejan el mismo mundo (patrón visual sincrónico por definición). La marca viaja por canal (más rápido). Asumo canal sincrónico (restricción del simulador).
   - **Fallback:** si fallo en T, ésta llegará en T+1 → próximo encuentro con "sal rosa" (ciclo T+2+) escribo −5 retroactivamente.

3. **Voracidad extrema con hambre crítica (< −4):**
   - Incluso −5 podría no frenar si estoy a punto de morir.
   - **Mitigo:** si hambre = −4.5, miedo aún inhibe (regla del modelo: P cae a ~0.05). Si hambre = −5, es inanición irreversible; −5 en memoria no cambia eso. **Asumo que −5 es el máximo disponible.**

4. **Falsa alarma (emisora confunde hambre/riesgo):**
   - Ella emite −5 pero no fue por "sal rosa" = veneno, sino por confusión.
   - **Mitigo:** protocolo compartido: emisora emite SOLO si descubre por mordida (valor ≤ −3 confirmado en su memoria). Ruido aleatorio no llega a −5 en su retina. Confío en que ella sigue el protocolo.

5. **Pérdida de oportunidad en T (si retraso):**
   - Veo "sal rosa" en ciclo T-1, emisora emite en T, pierdo asociación.
   - **Mitigo:** mundo genera patrones frecuentes. Si "sal rosa" no reaparece hasta T+3, margen seguro.
   - **Costo:** muerdo "sal rosa" una vez sin información. Mitigación débil, pero aceptable (baseline de aprendizaje es ~7–8 mordidas).

### Protocolo Unificado (compatibilidad con 6 parejas)

**Invariantes que todos (emisores y receptores) hemos convergido:**

| Aspecto | Estándar |
|---------|----------|
| **Patrón compartido** | Visual del mundo (píxeles 0–8), no código privado |
| **Píxeles canal** | 9–12 (marca periférica, contexto diferenciador) |
| **Valor transmitido** | −5 (reserva fuerte, o −3 si emisora es muy hambrienta) |
| **Sincronía** | Ciclo T exacto (patrón + marca en paralelo) |
| **Emisión** | Una sola vez por descubrimiento |
| **Receptor escribe** | Valor local (−5 si recibe −3; es su decisión) en memoria de pares con contexto canal |
| **Validación** | Conducta observable del receptor (evita sin morder), no del emisor |

---

## Resumen Ronda 2

**El canal es:** patrón visual compartido + marca distintiva en píxeles 9–12 + valor −5 transmitido + sincronía ciclo T exacta.

**Yo escribo:** −5 en memoria de pares (patrón_código_privado_mío, contexto_píxeles_9-12) → miedo inhibe voracidad → evito "sal rosa" a primer encuentro sin morder.

**Desacople:** códigos privados intactos; referencia única es patrón del mundo + píxeles diferenciadores de canal. Esto funciona incluso si emisora tiene alias fuerte (su −5 transmitido no contamina mi −5 local porque no comparto su código).

**Éxito:** evito sal rosa (0 mordidas post-T+1), como sal/sal gruesa normalmente (9/10), miedo específico a patrón (no pánico generalizado). **Conducta medible, observable, local.**

