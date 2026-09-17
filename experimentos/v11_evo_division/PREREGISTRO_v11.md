# v11 = v10 + división por CONFLICTO DE SIGNO (órgano nacido en JUACO-EVO) — confirmatorio, capacidad y examen

**Escrito ANTES de correr el confirmatorio. 17 sep 2026, día 5.** Dirección: *"Córrelo ahora"* (tras la recomendación de
confirmar el ganador de la generación 1 antes de seguir evolucionando).

## 0. Qué se sabe antes de escribir (se declara todo)

- **Origen del órgano.** `experimentos/evo/gen1/llm_2/organismo.py` (`f9cce63d371977ed`), propuesto por un subagente LLM
  con hipótesis escrita antes de evaluar. Seleccionado por la regla del preregistro EVO sobre semillas 1–10 y
  validado en retenidas 11–20: retención 10/10 y 10/10 (padre v10: 3/10 y 4/10); seis etapas y CTRL 10/10 en ambos.
- **Mecanismo.** Una celda con valor consolidado (`|Wp−Wn| > 0.2`) que recibe refuerzo de signo contrario se divide
  en esa mordida; la hija nace ciega fuera de los píxeles del patrón que la dispara, con 95 % de la sintonía de la
  madre dentro de ellos; sólo divide si la hija le gana a la madre en ese patrón; **la madre no se mueve**; el valor se
  **fisiona** (la hija se lleva el signo nuevo, la madre conserva el viejo). La regla `err > θ` deja de usarse.
- **Contaminación de semillas.** Las semillas **1–20** las usó la selección. Las **21–40** las leyó el autor de la
  mutación para diagnosticar al padre (lo declaró en su `hipotesis.md`). **Todo lo confirmatorio de este preregistro
  corre en semillas 41–60**, que nadie ha visto.
- **Humo declarado (instrumentos, semillas 1–3 y corridas cortas):** `v11m` ≡ genoma evolucionado (E2L, E2, bloque M
  cortos); `v11(div_signo=False)` ≡ v10; `v11(mu_norm=False, div_signo=False)` ≡ v9; `caph11(False, False)` ≡ `caph9`;
  `caph9` ≡ v9 y `caph11(True, True)` ≡ v11 en E1 corto (W, mord, vis, muertes, divisiones, celdas). Capacidad corta
  (20 estímulos, paso 3.000, semilla 3): **v11 usa más celdas** (65, 35 divisiones) que v10 (52, 22). Se corre además
  `bateria_v11.py 3` (semillas 1–3) como humo del instrumento; su resultado se anota en el commit, no aquí.
- **v10 sigue sin congelar** (ERR-17). Su réplica con el criterio corregido quedó escrita para semillas 41–60; se
  ejecuta aquí, en el mismo bloque, sin cambiar una coma.

## 1. Instrumentos (construidos por anclas, `construye_v11.py`)

| archivo | origen | sha |
|---|---|---|
| `organismo/organismo_v11.py` | `organismo_v10.py` (`219d5033fe15b5b9`) + `div_signo=True` | `f69e24063be1b194` |
| `organismo/bateria_v11.py` | `bateria_v10.py` (`d354813d3fa9d0f1`) | `17179642ad02269c` |
| `experimentos/v11_evo_division/organismo_v11m.py` | v11 + anclas de v10m (fases, sondas, códigos) | `db2296b71caf5bf0` |
| `experimentos/v11_evo_division/organismo_caph11.py` | `organismo_caph9.py` (`1b113605dc803435`) + `mu_norm` + `div_signo` | `a34d3309221cc6c7` |

**Cambio declarado en la batería (antes de correr):** el criterio **4a** de v8–v10 (`splits>0 ⇔ err_max>0.6`) era una
identidad **de la regla `err>θ`**, que v11 ya no usa. Se sustituye por **4a'** [identidad, NO evidencia]: cada división
activa exactamente una celda (`celdas == 30 + splits` y `len(split_t) == splits`, con celdas < 90). Ningún criterio
científico ni umbral cambia. La batería acepta `--desde N` (primera semilla).

## 2. Criterios

### Q0 — instrumentos (si falla, se para)
- `v11m` (por defecto) ≡ genoma `gen1/llm_2` en todas sus claves: E1, E2, E2L y bloque M × semillas 1..3.
- `v11m(div_signo=False)` ≡ `v10m` en todas sus claves: E1, E2 y bloque M × semillas 1..3.
- **KK1:** `caph11(mu_norm=False, div_signo=False)` ≡ `caph9` (lam 0.05) en todas las claves: los 3 planes de
  `ESC_CAP` y el plan corto de 6 estímulos × semillas 1..3.
- **KK1b:** `caph11(True, True)` ≡ `organismo_v11` en E1 (W, mord, vis, muertes, divisiones, celdas, split_t) × 1..3.

### Examen (semillas 41–60)
- **X1:** `bateria_v11.py 20 --desde 41 --log` cumple el criterio v3 completo (8/8, con 4a').

### R — retención con interferencia (bloque M de la Etapa 4, semillas 41–60; misma instrumentación para los tres brazos)
Brazos: **v9** (`mu_norm=False, div_signo=False`), **v10** (`div_signo=False`), **v11** (por defecto).
- **R1:** retención conjunta (`W_B(100k) ≤ −2` **y** `W_A(100k) ≥ 0.5`) en v11 ≥ **16/20**.
- **R2:** retención conjunta v11 − v10 ≥ **+6** semillas.
- **R3 [guarda: no retener por no aprender]:** `W_C(100k) ≤ −2.5` y `W_D(100k) ≥ 0.85` en v11 ≥ **18/20**.
- **R4 [mecanismo; decide el vocabulario, no la congelación]:** en v11, los códigos de A **y** de B en 100k son
  idénticos a los de 50k en ≥ **14/20**. Si R1 pasa y R4 no, se registra que retiene **por otra vía**.
- Sin voto: muerde B al reencuentro, muertes, divisiones, celdas.

### V10 — réplica de v10 con el criterio corregido de ERR-17 (sin cambios; mismas corridas de v9 y v10 de R)
(a) entre pares no empatados de ΔW_B (100k − 50k), v10 < v9 en ≥ 70 %; (b) semillas con ≥ 1 hija (índice ≥ 30) en el
código de B en 100k: v10 ≤ la mitad de v9 y ≤ 9/20; (c) v10 peor que v9 por > 0.5 en ≤ 2/20.

### K — capacidad (2K-bis: 20 estímulos de peso 3, uno nuevo cada `paso_t`; semillas 41–60)
Brazos: **v10** = `caph11(mu_norm=True, div_signo=False)` y **v11** = `caph11(True, True)`, `lam=0.05`,
`memoria_rechazo=20`, `plast=True`; `paso_t ∈ {20.000, 60.000}`. Métricas de la re-verificación de v9 sin tocar:
`N*` = `parte2_capacidad.techo()` (TOL 0.3), `M_max` = máximo sobre checkpoints de estímulos vivos con |W−R| ≤ 0.3.
- **K1:** en v11 a 20k, W = 0.000 exacto en ≤ 5 % de los 400 valores finales.
- **K2:** mediana de `M_max(v11)` ≥ mediana de `M_max(v10)` − 1, en 20k **y** en 60k.
- **K3:** mediana de `N*(v11)` ≥ mediana de `N*(v10)` − 1, en 20k **y** en 60k.
- Sin voto: agotamiento del pool de 90 celdas (`t_agot`), celdas, divisiones, muertes.

### Q5 — regresión
`bateria_v9.py 6` cumple y `manifiesto.py --check` da los congelados intactos.

## 3. Predicciones (con número)

- Q0, X1 y Q5 pasan.
- **R1:** v11 ≈ 18–20/20. **R2:** v10 ≈ 4–8/20, diferencia ≥ +10. **R3:** 20/20. **R4:** ≈ 16/20.
- **V10:** (a) sí, (b) sí, (c) sí (era el diagnóstico de ERR-17).
- **K2 y K3 pasan.** La fisión separa códigos y debería **subir** `M_max`; el riesgo declarado es el agotamiento del pool:
  **v11 agota el pool en más semillas que v10** (sin voto, pero es la predicción que más puede avergonzarnos: si v11
  agota y además pierde capacidad, el órgano no escala).

## 4. Qué se decide

- **Q0 falla:** se para y se arregla el instrumento.
- **X1, R1, R2, R3, K1, K2, K3 y Q5 pasan:** **v11 se congela como tronco** (tag `v11-tronco`; `organismo_v11.py` y
  `bateria_v11.py` a `CONGELADOS`; `organismo_v10.py` también, como instrumento de identidad). La Etapa 4 (retención
  con interferencia) **se declara cerrada en el mundo de 4 estímulos**, con R4 fijando si se puede decir "por el
  mecanismo declarado". Se registra como **el primer órgano del tronco nacido por evolución guiada**.
- **Falla R1–R3:** v11 no se congela; el resultado de EVO sobre 1–20 fue sobreajuste o suerte, y se registra así.
- **Pasa R pero falla K2 o K3:** v11 **no** se congela: retiene en un mundo pequeño a costa de capacidad. Se registra
  como órgano que no escala y se lleva el hallazgo a la generación 2 de EVO.
- **Falla X1:** no se congela; se registra qué etapa rompe.
- **V10:** si (a)–(c) pasan, v10 queda confirmado como paso intermedio (su archivo se congela como instrumento si v11
  se congela; si v11 falla, **v10 se congela como tronco**, según lo escrito en ERR-17). Si no pasan, se registra.

## 5. Qué NO prueba

No prueba aprendizaje abierto ni retención con más estímulos **ausentes** que celdas; K mide capacidad simultánea, no
olvido de lo que no está. No prueba que el LLM "descubriera" algo inédito en la literatura: la fisión de trazas
ante conflicto tiene parientes (asignación de engramas, separación de patrones). Prueba que el órgano, hallado por
búsqueda guiada, sostiene su efecto en semillas que nadie vio, sin romper lo anterior y sin perder capacidad.
