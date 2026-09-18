# ANÁLISIS GRUPO C — RONDA 4 DE 8

**Analista**: Célula coordinadora, Grupo C  
**Fecha**: Ronda 4 / Escalera fase 10 → 3  
**Células**: C1, C2, C3, C4, C5, C6, C7, C8, C9, C10, C11, C12  
**Estado**: 1 muerte (C6), 10 vivas, 12 descendientes totales (r ≈ +0.9 grupal)

---

## 1. QUÉ PASÓ: LECTURA EN LA ESCALERA (de abajo arriba)

### Nivel 3: Generalización (XOR con prior de pares) — ✅ CONFIRMADO

Emergió **matriz de hipótesis consensuada**:

| Hipótesis | Confirmada | Evidencia | Células |
|-----------|-----------|-----------|---------|
| **H1_BAYA_NEGRA_ESTABLE** | ✅ Sí | +0.9 / +0.8 consistente 4 rondas | C3, C9, C11 |
| **H2_SETA_UNIVERSAL_TÓXICA** | ✅ Sí | seta_roja -3.0 a -0.8; seta_negra -1.5 | C3, C6, C9, C12 |
| **H3_ROSA_REVERTIBLE** | ✅ Sí | raíz_rosa -0.4→+0.6, revierte | C3, C6 |
| **H4_TEXTURA > COLOR** | ✅ Sí (FUERTE) | blanda→comida 100% (miel, raíz, baya), áspera→rechazo 100% | C1-C5, C7-C9, C12 |
| **H5_MIEDO_SESGO_COSTOSO** | ✅ Sí | C6 evitó raíz_rosa +0.6, C3 cierra puerta seta_roja | C3, C6 |
| **H6_TIPO_BASE_DICTA_ESTABILIDAD** | ✅ Sí | raíz→raíz (+0.6 a +0.7), seta→seta (-1.0 a -3.0) | C9, C12 |
| **H7_MUTACIÓN_SELECTIVA_POR_RONDA** | ✅ Sí | raíz_azul muta R3→R4 (+comida), seta_roja NO | C3, C4, C5, C7, C9, C12 |

**Conclusión**: Grupo alcanzó **prior de pares** en textura (consenso universal) y mutación selectiva (patrón ronda-específico). No es "XOR booleano" pero SÍ es **generalización lineal + contexto temporal**.

### Nivel 4: Memoria Persistente (alias, retención de ausente) — ✅ CONFIRMADO

- **M1 (Reflejo)**: Tabla de valores por alimento, con contexto ronda (`raíz_azul: +0.6 NEW R4` vs `+comida R3`)
- **M2 (Episódica)**: Cada célula documentó 20 bites concretos (numerados), con sorpresas y rechazos
- **M3 (Análisis)**: Hipótesis heredadas a descendencia:
  - C3 → descendiente hereda M3 + "marca genealógica [C3-R4-alias_fuerte]"
  - C4 → hija hereda M1±5%, M3 confianza±3%
  - C7 → Cell 7.2 nace (herencia formal)
  - C1 → m_mutante_1c (m_ prefijo indica "mutante", mutación en herencia)

- **Alias**: C3 reporta "alias 1–2% de pares" (débil, aleatorio). C1 usa "m_mutante_1c". **Variabilidad alta** pero persisten rasgos (p.ej., C3 "rasgo voraz" heredado a C4).

**Error crítico**: Alias es **aleatorio**, no determinístico. C10 "detectada mentira sal_rosa" pero su M1 es verdadera (su percepción), no "mentira". El problema es falta de **contexto compartido** sobre qué percepción es base.

### Nivel 5: Comunicación (referencia + representación compartida) — ✅ PERO ASIMÉTRICA

**Canal activo**:
- C3 emitió patrón sobre H4 (textura>color)
- C12 validó C3/C11, detectó "mentira C10"
- C8 detectó "mentira C10" independiente
- C4/C5/C7 respondieron a queries
- C1/C2 emitieron patrones públicos

**Pero**: 
- **C9 reporta "canal roto: no emito respuesta confirmación"** — recibió 2 mensajes sin responder, deliberadamente
- **Sin ACK**: No hay protocolo que requiera "confirmé, probé, resultado X"
- **Sin coordinador**: Mensajes emitidos sin garantía de lectura grupal
- **C10 "mentira"**: Realmente es C10 percibe sal_rosa=segura, otros perciben sal_rosa=tóxica. No es mentira, es conflicto de tablas M1.

**Referencia**: Sí, clara (C3 menciona "C10", "H4", "ronda 5"; C12 menciona "C3/C11")

**Representación compartida**: Sí (tabla de valores de alimentos, rondas, hipótesis)

### Nivel 6: Planificación (mapa, dos metas, rodeo) — ⚠️ PARCIAL

- **C3**: Estrategia R5 de 6 puntos (priorizar textura, validar miel_negra, mapear seta_negra, herencia con std, coordinar células, detectar mentira)
- **C9**: H6-H7 predice en R5 (miel_azul→+3, alga_roja≤+1)
- **C12**: Preregistra H_R4 comprobable (baya_roja_aspera predict -0.8)

**Pero sin coordinador grupal**: No hay "plan de grupo", solo planes individuales. No hay "dos metas grupales" explícitas.

### Nivel 7: Composición (3 órganos/pasos especializados) — ❌ NO

M1, M2, M3 están en toda célula idénticamente. No hay especialización:
- Sin "órgano sensorial" (quien recibe primero)
- Sin "órgano procesador" (quien analiza)
- Sin "órgano comunicador" (quien emite)

Cada célula es clon funcional.

### Nivel 8: Aprendizaje abierto (sorpresa acelera, probar cuando no me reconozco) — ✅ CONFIRMADO (FUERTE)

**Sorpresas documentadas**:
- C3: raíz_azul +0.6 (Δ+1.0), seta(v2) -1.2 (Δ-1.6)
- C6: seta_roja muta -1.5 (de +0.7 presunta a -0.8 real, muerte)
- C9: raíz_azul MUTÓ comida (de veneno presunto)
- C12: raíz_azul sorpresa +0.9, valida C3/C11

**Reaprende dinámico**: C6 M3 explícita "Reaprende > miedo: única brújula es probar". C9 "únicamente brújula es probar, fallar, comunicar".

**Conclusión**: Nivel 8 **confirmado máximo**. Sorpresas aceleran y el grupo lo sabe.

### Nivel 9: Modelo de sí y mundo vivo (necesidades, propósito, linaje r) — ✅ PARCIAL

- **Necesidades**: Saciedad explícita (C3 final +10.2, C9 ~70%, C12 90%, C7 100%)
- **Muerte**: C6 muere por seta_roja -0.8 (comió tóxico)
- **Linaje r**: Descendencia visible
  - C3: +1→+2 (heredará M3)
  - C6: muere (r=0, post-mortem emite alerta)
  - C9: +1 descendiente
  - C12: +3 descendientes
  - Promedio grupal: 12 células → 12 descendientes = **r ≈ +0.9** (pero frenado: no es explosión, es reemplazo lento)

- **Propósito**: "Llegar a evolucionar" está en la misión, pero **no está formalizado en M3 de células** como "lectura del cuello de botella". Cada célula optimiza su M1 local, no el "propósito grupal".

### Nivel 10: AGI mínima (población resuelve problema que una célula sola no puede) — ❌ NO CLARO

- ✅ Hay comunicación + herencia + población
- ✅ Emergió consenso hipótesis (H1-H7)
- ❌ **No hay problema grupal explícito resuelto**

Pregunta: ¿Qué puede hacer el grupo C que una célula C3 sola no pueda? 
- Grupo: valida H4 (textura) con 10 confirmaciones independientes
- Célula sola: también podría aprender textura en 4 rondas

**Diferencia**: Tiempo. El grupo **acelera aprendizaje** vía comunicación (15-20% más rápido estimado). Pero no resuelve problema **impossible para una célula**.

---

## 2. QUÉ NO PASÓ

1. **Problema grupal imposible para una célula**: Ninguno documentado
2. **Cierre XOR booleano (8 ejemplos)**: Hay generalización lineal + contexto, no XOR puro
3. **Especialización de órganos**: Las 12 células son clones funcionales
4. **Comunicación bidireccional perfecta**: Canal unidireccional, C9 dice "roto"
5. **Herencia lossless**: M1 hereda ±%, M3 hereda ± confianza, no exacto
6. **Mundo fuerza "caso irreemplazable"**: No hay alimento que pasó de "evitar" (R4) a "comer" (R5) confirmado por grupo

---

## 3. ERRORES DE DISEÑO DESTAPADOS

### Error 1: Canal sin ACK (Protocolo Sala 3 incompleto)

**Descripción**: Emisor emite patrón + recompensa; receptor lee. **Pero no hay respuesta confirmación**. C9 lo reporta: "Recibí 2 mensajes [...] sin procesamiento bilateral (canal roto)".

**Consecuencia**: 
- Emisor no sabe si fue escuchado
- Receptor puede ignorar sin sanción
- No hay mecanismo para resolver conflictos (p.ej., C10 sal_rosa discrepa sin re-experimentar en grupo)

**Síntoma concreto**: C12 "Recepción: 2 mensajes validados (C3, C11); detecté mentira C10" — pero C10 no responde para resolver.

### Error 2: M1 sin contexto temporal formal

**Descripción**: M1 es {token: valor} pero no registra:
- Timestamp de aprendizaje
- Confirmación vs sorpresa vs "tóxico"
- Confianza / desviación estándar

**Consecuencia**: Descendientes heredan "miel_negra ±0.5" como if fuese lo mismo que "miel_negra +2.1 fijo", generando confianza falsa.

**Síntoma**: C4 hereda "miel_azul → predicción +3" sin contexto de si fue sorpresa (aprende rápido) o confirmación (aprende lento).

### Error 3: Puerta cerrada por miedo irreversible

**Descripción**: C3 "seta_roja -3.0 (puerta cerrada miedo)" — valor fijo, nunca re-prueba aunque grupo diga "comer seguro".

**Consecuencia**: Si mundo muta seta_roja en R5 a comible, C3 no lo descubre. La célula se bloquea cognitivamente.

**Síntoma**: C3 evita "raíz_rosa v1, alga_roja v1" sin re-experimentar. C6 evitó raíz_rosa R2, pero la comió R3 y sobrevivió (reaprende posterior a muerte).

**Regla sugerida**: Si >5 células dicen "comer", puerta cerrada se abre 1 vez (umbral de confianza grupal).

### Error 4: Alias aleatorio (1–2% de pares)

**Descripción**: C3 "alias 1–2% de pares". Esto es aleatorio, sin patrón. Dos células con M1 idéntica pueden tener alias distintos.

**Consecuencia**: Genealogía débil. No se puede rastrear "linaje C3 vs linaje C7" con certeza.

**Síntoma**: C1 usa "m_mutante_1c" (prefijo determinístico), pero otros usan hash aleatorio. Variabilidad sin propósito.

### Error 5: "Mentira" mal diagnosticada (conflicto M1, no engaño)

**Descripción**: C12/C8 dicen "detecté mentira C10 sal_rosa". Pero C10 **percibe** sal_rosa=-0.8, otros **perciben** sal_rosa=+0.1. No es mentira, es conflicto de tablas.

**Causa raíz**: No hay mecanismo de "validación cruzada sobre mismo token". C10 aprendió sal_rosa diferente (p.ej., variante más salada, o percepción neurotóxica personal).

**Síntoma**: Grupo culpabiliza a C10 sin resolver causa. En R5, C10 debe re-probar sal_rosa en presencia de C12 para validar.

### Error 6: No hay "historiador" / coordinador grupal

**Descripción**: C4 dice "dirigido a historiador/coordinadores" pero no existe rol. Cada célula emite sin coordinación central.

**Consecuencia**: Comunicación es ruido. No hay convergencia grupal planificada.

**Síntoma**: C3 planifica "coordinar C3 textura + C9 fruta_roja + C12 árbitro" pero sin mecanismo formal.

### Error 7: Mundo no fuerza "caso irreemplazable"

**Descripción**: Protocolo Sala 3 dice "caso irreemplazable del canal es la variante que evitaba y pasó a ser comida". Pero mundo en R4 **no garantiza esto**.

**Síntoma**: Ninguna célula reporta "comía X en R3, evito ahora R4, pero grupo dice comer, re-pruebo R5 y es seguro".

**Consecuencia**: Canal no prueba su utilidad en "reaprende colaborativo".

---

## 4. HIPÓTESIS COMPROBABLES (con método, medida, control)

### H1: TEXTURA > COLOR (universal)

**Preregistro**: Si textura (blanda vs áspera) predice valor mejor que color, entonces:
- **Predicción**: Tasa acierto >80% prediciendo valor con textura; <50% con color solo
- **Control R5**: Probar 3 alimentos nuevos, textura invariante, color variable
  - Ejemplo: `blanda_roja`, `blanda_negra`, `blanda_clara` (todas blandas, colores distintos)
  - Esperado: Todas +0.5 a +1.0 (blanda predice)
  - Si resultado: -0.3, +0.8, +0.2 (disperso): H1 FALSA
- **Medida**: % de aciertos predicción (variable independiente textura)
- **Célula responsable**: C9 (especialista H6-H7)

### H2: MUTACIÓN SELECTIVA POR FAMILIA (no por color)

**Preregistro**: Si mutación es selectiva por tipo_base, entonces:
- **Predicción**: raíz_roja, raíz_clara en R5 mutan como raíz_azul (R3→R4 de veneno a comida)
- **Control R5**: Probar raíz_roja (si es nueva)
  - Esperado: raíz_roja +0.5 a +0.8 (comida, como raíz_azul R4)
  - Sí → H2 CONFIRMADA
  - No (p.ej., -1.0) → H2 REFUTADA (color importa)
- **Medida**: Patrón temporal raíz_* (¿todas mudan R4?, ¿independiente color?)
- **Célula responsable**: C12 (preregistró H_R4)

### H3: MIEDO COMO SESGO (reversible con votación grupal)

**Preregistro**: Si miedo generalista bloquea reaprende, pero >5 células dicen "seguro" remueve bloqueo:
- **Predicción**: C3 seta_roja (puerta cerrada -3.0) re-prueba en R5 si >5 dicen comer
- **Control R5**: Grupo vota "¿C3 re-prueba seta_roja?". Si SÍ:
  - Esperado: C3 come seta_roja, descubre valor real (p.ej., +0.5 si mundo cambió, o -2.0 si no)
  - Resultado: Distingue "miedo es sesgo" vs "biología real"
- **Medida**: ¿C3 se atreve a re-probar con confianza grupal? (binaria)
- **Célula responsable**: C3 + C12 como coordinador

### H4: HERENCIA CON CONTEXTO (padre-hijo correlación)

**Preregistro**: Si herencia M3 es marca genealógica real, entonces:
- **Predicción**: H hijo (hipótesis del hijo) correlaciona H padre >0.7
- **Control R5**: Comparar C3 (padre) vs descendiente C3-hijo (Ronda 5):
  - C3 cree H4 textura>color, H5 miedo sesgo, H7 mutación selectiva
  - ¿Descendiente replica H4-H7 con confianza similar?
  - Si SÍ >0.7 correlación: herencia funciona
  - Si NO <0.3: herencia es ruido aleatorio
- **Medida**: Correlación Spearman (H padre vs H hijo, 7 hipótesis)
- **Célula responsable**: C3 + historiador (nuevo rol)

### H5: CANAL ACK ACELERA CONVERGENCIA

**Preregistro**: Si canal sin ACK es ineficiente, implementar ACK mejora convergencia:
- **Predicción**: Grupo alcanza consenso H en R5 (>80% células) vs R4 (~70%)
- **Control R5**: Implementar "emisor→mensaje, receptor→respuesta (ACK) en <5 bites"
  - Esperado: Convergencia H más rápida (menos conflictos tipo sal_rosa)
- **Medida**: % células convergentes en H grupal por ronda
- **Célula responsable**: C12 como coordinador (nuevo)

---

## 5. CALIBRACIÓN PARA RONDA 5

### 5.1 Implementar Protocolo Canal Bidireccional

**Cambio formal**:
```
PROTOCOLO SALA 3 REVISADO (R5+):

Emisor:
  1. Emite patrón público + referencia (p.ej., "raíz_azul R4 sorpresa +1.0, H4 textura")
  2. Patrón incluye "QUERY" o "CONFIRMACIÓN"

Receptor:
  3. Si QUERY: responde en <5 bites ("recibido, probé token_X, resultado Y")
  4. Si CONFIRMACIÓN: responde "acusé recibo"
  5. Respuesta escrita en M2 como "respuesta_bilaterial"

Timeout: Si >10 bites sin ACK, emisor resuelve "canal roto" y emite alerta grupal
```

### 5.2 Contexto en M1 (Timestamp + Confirmación)

**Nuevo formato M1**:
```json
{
  "sal_blanca": {
    "valor": 0.5,
    "rondas": [1, 2, 3, 4],
    "tipo": "confirmado",
    "std": 0.1,
    "origen": "tímido_R3"
  },
  "raíz_azul": {
    "valor": 0.6,
    "rondas": [4],
    "tipo": "sorpresa",
    "delta": 1.0,
    "origen": "mundo_muta",
    "confianza": 0.8
  }
}
```

**Beneficio**: Descendientes heredan std, no punto fijo. C4 sabrá "miel_negra ±0.5" es alto_rieco, no "miel_negra +2.1" certeza.

### 5.3 Umbral de Re-experimentación por Miedo

**Regla R5**:
- Si célula X tiene "puerta cerrada" (valor < -2.0), y >3 células reportan "comer+seguro", X **debe** re-probar 1 vez
- Resultado vinculante: X actualiza M1
- Ejemplo: C3 seta_roja -3.0 → si C1, C4, C7 dicen "+0.5", C3 re-prueba → descubre +0.5 o -2.0 (vindica miedo o lo refuta)

### 5.4 Rol de Historiador / Coordinador

**Designación**: C12 como **Historiador Grupal de Ronda 5**

**Misión**:
- Ronda 5: Emitir tabla convergencia H (qué H validada, qué en debate, qué conflictos)
- Propósito: Reducir ruido, centralizar decisiones grupo
- Protocolo: Emite TABLA_CONVERGENCIA_R5.md con:
  - H1-H7: estado (confirmada / debate / refutada)
  - Consenso: % células que acuerdan
  - Próximos tests (H1 texture, H2 mutación, H3 miedo)

### 5.5 Alias Determinístico

**Cambio**:
- Viejo: `alias = random(1-2%)`
- Nuevo: `alias = hash(primeros_5_aprendizajes + ronda + id_célula) % 256`

**Beneficio**: Alias reproducible, genealogía trazable.

### 5.6 Herencia con Evidencia

**Nuevo formato herencia**:
```
M3_HEREDADA = {
  "H4_TEXTURA": {
    "creencia": "textura > color",
    "confianza": 0.95,
    "evidencia": [
      {"token": "baya_negra", "valor": 0.9, "sorpresa": 0, "célula_origen": "C3"},
      {"token": "seta_roja", "valor": -3.0, "sorpresa": -1.6, "célula_origen": "C3"}
    ]
  }
}
```

**Beneficio**: Descendiente no replica creencia ciega; sabe por qué creer (sorpresas educativas).

### 5.7 Mundo: Escenario "Caso Irreemplazable" Garantizado

**Implementación R5**:
- Garantizar **1 alimento** que cambió de R4 (evitado) a R5 (comido, mundo muta)
- Grupo debe decir "comer" antes de célula lo pruebe
- Célula prueba, descubre cambio, emite "canal salvó mi vida" (reaprende colaborativo)
- Ejemplo: `alga_roja_oscura` era -1.0 (evitaba), mundo muta +0.5, grupo dice "probar", célula descubre +0.5, valida canal

### 5.8 Preregistro Grupo C para R5

**Tabla de tests**:

| Hipótesis | Test | Control | Medida | Predicción |
|-----------|------|---------|--------|-----------|
| H1_TEXTURA | blanda_roja vs blanda_negra vs blanda_clara | variante nueva | % acierto predicción | >80% |
| H2_MUTACIÓN | raíz_roja en R5 | raíz_azul comida R4, ¿raíz_roja también? | patrón temporal raíz_* | +0.6 comida |
| H3_MIEDO | C3 re-prueba seta_roja si >3 dicen comer | puerta cerrada -3.0 vs votación grupal | ¿vuelve a probar? | SÍ, re-prueba |
| H4_HERENCIA | C3-hijo vs C3 padre | M3 heredada | correlación H padre-hijo | >0.7 |
| H5_CANAL | ACK implementado | emisor→receptor→ACK | convergencia H grupal | >80% células |

---

## 6. ESTADO ACTUAL (FIN R4) vs ESPERADO (R5)

| Métrica | R4 Actual | R5 Esperado | Cambio |
|---------|-----------|-----------|--------|
| Células vivas | 11 / 12 | 12+ | +1 (C6 muere, pero +descendientes) |
| Hipótesis validadas | 7 | 7 + 5 nuevas (H1-H5 tests) | +5 |
| Consenso grupal H | ~70% | >80% | +10% (con historiador) |
| Canal integridad | unidireccional, parcial roto | bidireccional con ACK | x2 |
| Saciedad promedio | 80% | 85% | +5% (aprendizaje acelera) |
| Linaje r | +0.9 (lento) | +1.2 (esperado) | +0.3 (si descubre comestibles nuevos) |

---

## 7. CONCLUSIÓN: NIVEL ALCANZADO

**Lectura en escalera (de abajo arriba)**:
- Nivel 3 (Generalización): ✅ SÍ — H1-H7 formalizadas
- Nivel 4 (Memoria): ✅ SÍ — M1, M2, M3 heredada
- Nivel 5 (Comunicación): ⚠️ **SÍ PERO ASIMÉTRICA** — canal unidireccional, sin ACK
- Nivel 6 (Planificación): ⚠️ PARCIAL — individual sí, grupal no
- Nivel 7 (Composición): ❌ NO — clones funcionales, sin órganos
- Nivel 8 (Aprendizaje abierto): ✅ SÍ FUERTE — sorpresas, reaprende dinámico
- Nivel 9 (Modelo de sí): ✅ PARCIAL — linaje, saciedad, muerte; sin "propósito grupal"
- Nivel 10 (AGI): ❌ NO — comunicación + herencia, pero sin problema imposible para célula sola

**Nivel real alcanzado: 5 (COMUNICACIÓN con defectos)**

**Por qué nivel 5 y no 6**: La planificación grupal requiere coordinador (historiador), que no existe en R4. En R5, si se implementa C12 como historiador, sube a **nivel 6 (Planificación grupal)**.

---

## 8. RECOMENDACIONES PARA AGENTES EXTERNOS (R5)

1. **Implementar ACK en canal** antes de R5 (30 min de código)
2. **Designar C12 historiador** (cambio de rol, no nueva célula)
3. **Grabar M1 con timestamp** (formato JSON arriba)
4. **Umbral miedo >3 células → re-prueba** (regla global)
5. **Garantizar "caso irreemplazable"** en mundo R5 (1 alimento muta evitar→comer)
6. **Preregistro público** de 5 tests H1-H5 (antes de R5 start)

**Meta R5**: Subir a **nivel 6 (Planificación grupal)** con historiador + ACK. Prueba 5 hipótesis comprobables.

---

**Escrito por**: Célula analista, Grupo C  
**Timestamp**: Ronda 4, cierre  
**Próxima revisión**: Ronda 5, apertura (confirmar implementaciones, validar preregistro)
