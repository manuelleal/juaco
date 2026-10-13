# Re-verificación sobre el tronco v9: composición temporal (3T) y capacidad (2K-bis)

**Escrito ANTES de construir instrumentos y ANTES de correr. 16 sep 2026, día 4.**

- **Dirección:** Christiam Puentes ("corre los dos resultados que nos faltaban").
- **Ejecución:** en el repo.

## 0. Por qué y qué se sabe

- **Por qué.** 3T (SÍ, replicado) y la corrección de 2K-bis se midieron sobre **v8**. v9 añade la memoria de
  trabajo de rechazo, que cambia hacia dónde van las patas y, con ello, la secuencia de mordidas. No hay predicción
  exacta posible contra v8: **esto es una prueba de no-regresión con los criterios originales.**
- **Conocido sobre v8.**
  - 3T: C3 `sep` 3.97, `lift_q4` 0.34 y `solap_A` 1; C3C `sep` 0.44 y `lift_q4` −0.04 (semillas 1–20).
  - 2K-bis C_T20 con drenaje: N* 5.0 [3, 7]; M_max 8 [6, 11]; W=0 exacto 0/400; agotamiento 5/20; muertes 564.
  - 2K-bis C_T60: N* 8, M_max 12.
- **Sobre v9 no se ha corrido nada de esto.**

## 1. Instrumentos (anclas; con `memoria_rechazo=0` son exactamente los instrumentos de v8)

- **`mundo_temporal_v9.py`**, desde `experimentos/3T_confirmatorio/mundo_temporal_v8.py` (`ee7eac62ecab3313`).
- **`organismo_caph9.py`**, desde `experimentos/bug01/organismo_caph.py` (`38e259b0175d6375`).

Los dos añaden la memoria de rechazo con la **misma lógica** que `organismo_v9.py`:
- memoria por posición;
- olvido al morder o al retirarse el objeto;
- fallback sin filtro;
- sin RNG.

## 2. Bloque T — 3T sobre v9

Seis brazos (C1, C1p, C2, C2b, C3, C3C) con `lam=0.05`, `wclip=3.0`, `nkmax=90` y `memoria_rechazo=20`;
semillas 1..20; T=100.000.

- **KT1 [instrumento]:** `mundo_temporal_v9(memoria_rechazo=0)` ≡ `mundo_temporal_v8`, campo a campo, en los 6
  brazos × semillas 1..3. Si falla, se para.
- **KT2:** C2b ≡ C1 bajo v9 en `W`, `sep`, `n_AB`/`n_AA`/`n_B`, muertes y `Rtot`, 20/20.
- **T1–T4:** los criterios 1–4 del 3T confirmatorio, sin cambiar un umbral:
  - T1: mediana de `solap_A` final de C3 ≤ 1 y ≥ 15/20 con ≤ 1;
  - T2: mediana de `sep` de C3 ≥ 1.0;
  - T3: mediana de `lift_q4` de C3 ≥ 0.15;
  - T4: C3C con mediana de `sep` < 1.0 **y** mediana de `lift_q4` < 0.15.
- **Predicción:** T1–T4 se sostienen. **3T sobrevive a v9.**

## 3. Bloque K — 2K-bis sobre v9

Parte 2 de 2K-bis importada sin tocar: `parte2_capacidad.py`, `techo()` con TOL=0.3, `plast=True`. Condiciones:
`paso_t ∈ {20000, 60000}` × {v8 = `caph9(memoria_rechazo=0)`, v9 = `caph9(memoria_rechazo=20)`}, siempre con
`lam=0.05`; semillas 1..20.

- **KK1 [instrumento]:** `caph9(memoria_rechazo=0)` ≡ `caph(lam=0.05)` en todas las claves de caph, con los 3 planes
  de `equivalencia_cap.py` × semillas 1..3 y el plan corto de 6 estímulos × semillas 1..3.
- **KK2 [reproducción]:** el brazo v8 a 20k reproduce, en las 20 semillas, **N\*** y **M_max** de las corridas
  `C_T20` con `lam=0.05` guardadas en `datos/coste_techo_20260916_142116.json`.
- **K1:** en v9, W=0.000 exacto en ≤ 5% de los 400 valores finales a 20k (en v8: 0%).
- **K2:** mediana de M_max(v9) ≥ mediana de M_max(v8) − 1, en 20k **y** en 60k.
- **K3:** mediana de N\*(v9) ≥ mediana de N\*(v8) − 1, en 20k **y** en 60k.
- **Sin voto:** muertes, agotamiento y divisiones, v9 frente a v8, pareado.
- **Predicción:** K1–K3 se sostienen. **v9 no pierde capacidad.**

## 4. Qué se decide

- **Todo se sostiene:** 3T y la corrección de 2K-bis pasan a valer **sobre el tronco v9**, y se registra.
- **Falla KT1 o KK1:** se para y se arregla el instrumento.
- **Falla T1–T4 o K1–K3:** **regresión de v9**. Se registra como coste de la memoria de rechazo y se lleva a
  dirección. v9 **no** se descongela por defecto, pero el hallazgo decide si hay que volver a v8 para esas
  capacidades.

## 5. Qué NO prueba

Nada nuevo sobre composición ni capacidad. Sólo que los resultados de v8 siguen valiendo con v9.
