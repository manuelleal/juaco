# v9 = v8 + MEMORIA DE TRABAJO DE RECHAZO — confirmatorio en semillas nuevas y examen de congelación

**Escrito ANTES de construir `organismo_v9.py` y antes de correr nada. 16 sep 2026, día 4.**

- **Dirección:** Christiam Puentes ("dale hasta que lo logres").
- **Ejecución:** en el repo.
- **Si algo falla, no se recalibra:** se registra y se rediseña con otro preregistro (regla 3).

## 0. Qué se sabe antes de escribir (se declara)

Exploración del subagente, sin valor confirmatorio. Carpeta `JUACO/exploracion/organos_20260916/` (informe
`f7a3ff032a9d2ec0`, CSV `0324bdd418400838`), semillas **1–20**, cifras de O3 recalculadas por mí.

- **El problema.** En v8 las patas persiguen siempre el objeto más cercano (`see()`), aunque la boca lo acabe de
  rechazar. En la 2ª mitad de E1 el organismo pasa **20.1%** [16.2, 23.9] de los pasos sobre veneno, con 1.42 pasos
  por llegada: oscila atado a él. El azar corregido por la composición del mundo (92% de objetos vivos son veneno)
  es **9.2%**. El exceso se aprende: con las patas sin aprendizaje queda en 9.73%.
- **El órgano.** O3, memoria de trabajo de rechazo con τ = 20: un objeto rechazado por la boca deja de ser objetivo
  de `see()` durante 20 pasos, y se olvida si el objeto desaparece.
- **Lo que dio en la exploración:**
  - veneno 20.1% → **9.8%** [9.0, 10.6], 20/20 bajan, en E1 y en E2;
  - muertes combinadas −17.5 (17↓ 3↑);
  - comida +7.5;
  - criterios de E1 y E2 20/20.
- **No es monótona en τ** (50 → 12.9%; 150 → 16.9%), porque con τ largo el filtro deja sin objetivo y vuelve la
  política original (fallback). **τ = 20 queda fijado ahora y no se barre.**
- **Las semillas 1–20 están vistas para esta pregunta.** La confirmación va en semillas **21–40**.

## 1. Instrumentos (generados por anclas; cada ancla exactamente una vez)

- **`organismo/organismo_v9.py`**, generado desde `organismo/organismo_v8.py` (`dca7d5c3a162f5d4`, congelado) por
  `experimentos/v9_memoria_rechazo/construye_v9.py`.
  - **Único cambio de comportamiento:** el parámetro `memoria_rechazo=20`.
  - Con `memoria_rechazo=0` es v8 exacto.
  - Implementa O3 tal como la exploró el agente: memoria por posición, olvido al morder o al retirarse el objeto,
    fallback sin filtro, sin RNG.
  - **Instrumentación de sólo lectura, por cuarto:** pasos sobre objeto y llegadas, por valencia vigente; pasos sin
    objetivo (fallback, contado una vez por paso).
- **`experimentos/v9_memoria_rechazo/organismo_v9c.py`** = v9 + `memoria_modo ∈ {'rechazado', 'azar'}`, sólo para
  el control C1.
  - En `'azar'`, tras un rechazo se "recuerda" un objeto **distinto** del rechazado, elegido con un RNG **separado**
    (`seed + 200000`) para no desalinear el principal.
  - Con `'rechazado'` es v9 exacto.
- **`organismo/bateria_v9.py`:** el examen criterio v3 de `bateria_v8.py`, aplicado a v9.

## 2. Confirmatorio (semillas 21–40; E1 = `run(s)`, E2 = `run(s, invertir_en=50000)`)

**Brazos:**

| brazo | organismo | papel |
|---|---|---|
| v8 | `organismo_v8.run` | control |
| **v9** | `organismo_v9.run`, `memoria_rechazo=20` | **candidato** |
| C1 | `organismo_v9c.run`, `memoria_modo='azar'`, τ = 20 | memoria sobre un objeto al azar |
| C2 | `organismo_v9.run`, `memoria_rechazo=1` | memoria de un solo paso |

**Métricas, en la 2ª mitad (cuartos 3–4):**
- `pct_ven` = pasos sobre veneno / 50.000;
- mordidas de comida;
- muertes totales;
- `sin_obj` = pasos sin objetivo / 50.000;
- criterios de E1 y E2 de `bateria_v8.py`.

### Predicciones

- **M0 [instrumento]. Si falla una, no se lee nada más.**
  - `v9(memoria_rechazo=0)` ≡ v8 en todas las claves de v8, en los 7 escenarios × semillas 1..6.
  - `v9c('rechazado')` ≡ v9 en todas las claves de v9, en E1/E2 × semillas 1..3.
  - **Mismo mecanismo que la exploración:** `v9` ≡ `organismo_v8x(o3_tau=20)` del agente en `W`, `mord`, `vis`,
    `deaths` y `splits`, en E1/E2 × semillas 1..3.
- **M1 [el efecto], en E1 y en E2:**
  - v8, mediana de `pct_ven` ∈ [16, 24]% (el problema se replica en semillas nuevas);
  - v9, mediana ∈ [8, 12]%;
  - pareado v9 − v8 ≤ **−6 pp** en **≥18/20** semillas.
- **M2 [coste].** Muertes combinadas (E1 + E2), pareado v9 − v8: mediana **< 0** y v9 ≤ v8 en **≥14/20**.
- **M3 [no come menos].** Mordidas de comida en la 2ª mitad de E1, pareado v9 − v8: mediana **≥ 0**.
- **M4 [el fallback no domina].** Mediana de `sin_obj` **< 5%**, en E1 y en E2.
- **M5 [no-regresión en semillas nuevas].** v9 cumple los criterios de E1 en ≥18/20 y los de E2 en ≥18/20.
- **M6 [controles de artefacto], en E1:**
  - **C2 (τ = 1):** mediana pareada de `pct_ven` frente a v8 **> −2 pp**. La duración de la memoria es necesaria.
  - **C1 (memoria sobre un objeto al azar):** mediana pareada frente a v8 **> −3 pp**, **y** la de v9 al menos
    **4 pp** más baja que la de C1. Lo que funciona es recordar **lo rechazado**, no perturbar el objetivo.

**Pregunta de "¿pasaría por la razón equivocada?", respondida antes de correr.**
- **Si v9 simplemente se moviera menos, estaría menos sobre todo:** M3 lo vigila (no come menos), y `pct_com` se
  reporta.
- **Si el fallback lo dominara, no habría memoria efectiva:** lo vigila M4.
- **Si cualquier perturbación del objetivo produjera lo mismo:** lo vigila C1.

## 3. Examen de congelación (`python organismo/bateria_v9.py 20 --log`, semillas 1–20)

Es el criterio v3 de `bateria_v8.py`, aplicado a v9 sin cambiar un umbral:
- **5:** identidad `v9(memoria_rechazo=0)` ≡ v8;
- **1:** los criterios científicos de las seis etapas, 20/20;
- **2:** `celdas ≤ 45`;
- **3:** control negativo ≤ 1/20;
- **4a:** identidad `splits ⇔ err_max > 0.6`, sin valor de evidencia;
- **4b:** sin conflicto no hay división, con sus guardas;
- **4c:** C∩B = 3 de misma valencia → 0 divisiones y `W_C ≤ −2.5`, con guarda;
- **4d:** disparo anclado a la causa.

Después: `python organismo/bateria_v8.py 6` PASA (v8 intacto) y `manifiesto.py --check`.

## 4. Qué se decide

- **M0–M6 y el examen pasan:** **v9 se congela como tronco** (tag `v9-tronco`; `organismo_v9.py` y `bateria_v9.py`
  entran en `CONGELADOS`; v8 queda como referencia).
  - **La conducta de la Etapa 2 se da por cerrada:** el organismo explora lo temido con hambre, lo que permite
    revertir (frontera medida, v8 en el óptimo), y ya no se queda atado a lo que rechaza.
- **Falla M0:** se para y se arregla el instrumento.
- **Falla M1, M2, M3, M5 o M6:** v9 **no** se congela. Se registra, y el rediseño va con preregistro nuevo, por
  ejemplo O7 ("qué hacer sin objetivo"). **τ no se toca.**
- **Falla M4 sola:** el efecto existe, pero el mecanismo no es el que creemos. No se congela hasta entenderlo.

## 5. Qué NO prueba

- No re-corre 3T ni 2K-bis sobre v9: la memoria cambia las patas y esos resultados son de v8. Queda pendiente.
- No prueba mundos con más objetos o más estímulos.
- τ = 20 no se optimiza.
