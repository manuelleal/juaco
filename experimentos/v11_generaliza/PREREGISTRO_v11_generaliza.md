# Re-verificación sobre v11: generalización (Etapa 3) y composición temporal (3T) — ¿qué costó separar?

**Escrito ANTES de correr. 17 sep 2026, día 5.** Dirección: *"corre el preregistro y confirmatorio de Etapa 3 y 3T
sobre v11"*, con la nota `registro/NOTA_v11_pattern_separation_20260917.md` como marco.

## 0. La pregunta y por qué importa

v11 resolvió el olvido **dividiendo la unidad en conflicto**: la hija nace **ciega fuera de los píxeles de su
estímulo** y la madre no se mueve. Eso es separación de patrones llevada al extremo. La Etapa 3 (generalizar a
patrones **nunca vistos**) y 3T (componer un paso de historia) se midieron **sólo sobre v9**. Si separar cuesta
generalizar, aquí se ve.

**Las dos lecturas posibles, fijadas antes de mirar los datos** (nota de dirección):
- **McClelland, McNaughton & O'Reilly (1995)** — sistemas complementarios: la memoria rápida y separada (hipocampo)
  **paga** con generalización; generalizar exige entrelazado lento (corteza). *Predice que v11 pierde Etapa 3.*
- **Sahay et al. (2011)** y **Clelland et al. (2009)** — aumentar la neurogénesis **mejora** la separación de patrones
  **sin** destruir la generalización de la red vieja. *Predice que v11 la conserva.*
- **Frankland & Josselyn (2014)** — la neurogénesis adulta **causa** olvido: es la cara opuesta del mismo mecanismo y
  es lo que ya explicó la Etapa 4.

**Este experimento decide entre las dos lecturas para nuestro caso.** Se registra el resultado venga como venga: si
cae, el proyecto tiene un resultado limpio a favor de CLS ("dividir cuesta generalizar"); si sobrevive, tenemos un
caso que ninguna de las dos predice del todo, y **eso es más fuerte, no más cómodo**.

## 1. Instrumentos (anclas; orígenes por sha; humo declarado)

| archivo | origen | sha |
|---|---|---|
| `organismo_v11g.py` | `organismo_v11.py` (`f69e24063be1b194`) + **las mismas anclas de `construye_v9g.py`** | `6c6b5eecc177c181` |
| `mundo_temporal_v11.py` | `mundo_temporal_v9.py` (`18d96a1c79863bb0`) + `mu_norm` + `div_signo` | `807f4b357f9eac1a` |

**Humo declarado** (semillas 1–2, corridas cortas): `v11g(mu_norm=False, div_signo=False)` ≡ `organismo_v9g` en el
mundo de regla; `v11g(mundo='AB')` ≡ `v11`; `mundo_temporal_v11(False, False)` ≡ `mundo_temporal_v9` en C3. En 20k
pasos, 3T con v11 da `sep` +3.72 y `solap_A` 0; en el mundo de regla, v11 hace 22–28 divisiones y usa 52–58 celdas.

**Los tres brazos se corren con el MISMO instrumento**, cambiando sólo los dos interruptores: **v9** (`False, False`),
**v10** (`True, False`), **v11** (`True, True`). **Semillas 41–60** (las de los confirmatorios de v11; las 1–20 del
resultado original de Etapa 3 quedan como referencia histórica, y se re-mide v9 aquí para comparar pareado).

## 2. Criterios — Etapa 3 (mundo de regla, 20 patrones de peso 3, T = 200.000)

**Se reutilizan EXACTAMENTE los umbrales del preregistro de Etapa 3 sobre v9** (`5a2af284ee73ae76`). No se toca ninguno.

- **K [instrumento]:** identidades del humo, ampliadas a semillas 1–3; y **cobertura**: en cada corrida, ≥ 6 de los 10
  patrones de test tienen primer encuentro registrado, en ≥ 18/20 semillas.
- **G1 [valor, patrones nunca vistos]:** exactitud de signo (`W` a priori, media balanceada) con la regla `px0`:
  mediana ≥ **0.65**; control `azar` en **[0.35, 0.65]**; `px0` > `azar` pareado en ≥ **14/20**.
- **G2 [conducta al primer encuentro]:** `BA_pb` con `px0`: mediana ≥ **0.55**; `azar` en **[0.42, 0.58]**;
  `px0` > `azar` en ≥ **14/20**.
- **G3 [frontera XOR, sin voto]:** `xor01` ≤ 0.60 y `xor01` < `px0` en ≥ 14/20.
- **G4 [LA COMPARACIÓN, nueva y decisiva]: no-inferioridad de v11 frente a v9**, pareada por semilla:
  mediana de exactitud `px0`(v11) ≥ mediana `px0`(v9) − **0.05**, **y** mediana `BA_pb`(v11) ≥ mediana `BA_pb`(v9) − **0.03**.

## 3. Criterios — 3T (composición temporal, 6 brazos × 2 reglas de división, T = 100.000)

Se reutilizan los umbrales de la re-verificación sobre v9 (`2708cb73ab8531e8`).
- **KT1 [instrumento]:** `mundo_temporal_v11(False, False)` ≡ `mundo_temporal_v9` en todas las claves, 6 brazos ×
  semillas 1–3.
- **KT2:** con la regla de v11, `C2b` ≡ `C1` en `W`, `sep`, `n_AB`, `n_AA`, `n_B`, `deaths`, `Rtot`, 20/20.
- **T1:** `C3`(v11) `solap_A` mediana ≤ 1 y ≤ 1 en ≥ 15/20. **T2:** mediana `sep` ≥ **1.0**.
  **T3:** mediana `lift_q4` ≥ **0.15**. **T4:** el control `C3C` con mediana `sep` < 1.0 **y** `lift_q4` < 0.15.
- **T5 [no-inferioridad]:** mediana `sep`(C3, v11) ≥ mediana `sep`(C3, v9) − **1.0**.

## 4. Predicciones (numéricas, antes de mirar)

- **3T: sobrevive.** T1–T4 se sostienen; `sep`(C3, v11) entre **3.0 y 4.5** (v9 dio 3.93 en la re-verificación);
  `solap_A` 0 en ≥ 18/20; T5 se sostiene.
- **Etapa 3: sobrevive, con ventaja pequeña para v11.** exactitud `px0`(v11) **0.72–0.88** (v9 dio 0.80 en semillas
  1–20); `BA_pb`(v11) **0.55–0.65**; G4 se sostiene.
  **Razón declarada:** la hija es ciega fuera de su patrón, pero el código de un patrón nuevo se elige por producto
  escalar, así que un patrón nunca visto sigue cayendo en las celdas de los entrenados **más parecidos**; y esas
  celdas ahora tienen valor **limpio** (un solo signo), no mezclado. Es la predicción de Sahay/Clelland, no la de CLS.
- **Riesgo que me haría equivocarme:** si las hijas acaparan el código de casi todos los patrones nuevos y su valor es
  muy específico, la exactitud caería hacia 0.5 y G4 se refutaría. Sería el resultado de CLS.

## 5. Qué se decide

- **G1, G2 y G4 se sostienen, y T1–T5 también:** **v11 no pagó por separar.** Se registra como el resultado más fuerte
  del proyecto y se escribe explícitamente que **contradice la predicción simple de CLS** en este sistema, alineándose
  con Sahay/Clelland. Etapa 3 y 3T pasan a valer **sobre v11**.
- **G4 se refuta (la generalización cae):** **v11 es un canje, no una mejora universal.** Se registra a favor de CLS,
  se anota que el tronco cambia generalización por retención, y **se abre la pregunta de si hace falta un segundo
  sistema** (una vía lenta y entrelazada) en vez de un tronco único. v11 **no se destrona** (su congelación se decidió
  con otros criterios), pero el registro y `CLAUDE.md` llevarán la advertencia en grande.
- **T1–T4 se refutan:** la composición temporal no sobrevive; se registra igual y se investiga por qué (la hija ciega
  fuera de P no puede quedarse con las columnas temporales).
- **Falla K o KT1:** se para y se arregla el instrumento.

## 6. Qué NO prueba

No prueba generalización fuera de patrones de peso 3, ni composición de más de un paso, ni nada sobre la Etapa 5.
