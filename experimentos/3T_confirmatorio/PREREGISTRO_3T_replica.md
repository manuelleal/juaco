# RÉPLICA del 3T confirmatorio en semillas NUEVAS (21–40)

**Escrito ANTES de modificar el script y ANTES de correr. 16 sep 2026, día 4.**

- **Dirección:** Christiam Puentes pidió cerrar ERR-13 de forma que el resultado no dependa de una corrección
  hecha a la vista de los datos ("termina y deja arreglado el error").

## 0. Por qué existe esta réplica

El 3T confirmatorio dio **SÍ** en su segunda corrida (`datos/3T_confirmatorio_20260916_150727`). Arrastra dos
dudas registradas:
1. **ERR-13.** La primera corrida dio NO porque el comparador trataba `0.0` y `-0.0` como distintos. Se corrigió
   a igualdad numérica **después** de ver ese NO.
2. **No era ciego.** Los números del post-hoc PH3 del día 3 se conocían para las semillas 1–20.

**Una réplica en semillas 21–40 despeja las dos a la vez.**
- El comparador corregido ya está commiteado (`013a76e`) **antes** de ver estas semillas.
- De estas semillas no se conoce ningún número: ni de v8, ni de PH3, ni de ningún experimento anterior.

## 1. Qué se corre

`experimentos/3T_confirmatorio/corre_3T_confirmatorio.py`, en la versión con ERR-13 corregido (sha
`d0df3f6d6ae76c8c`). Único cambio, para poder elegir las semillas:
- **`--desde N`** corre las semillas `N .. N+S−1`. Aquí, `20 --desde 21`, es decir 21..40.
- **K3 no aplica** si el JSON guardado de PH3 no contiene esas semillas (sólo tiene 1–20). Se marca "no aplica",
  **no** "cumple". La referencia (techo 30, `lam=0`) se corre en vivo igual que antes, y K1 garantiza que es el
  mundo original.
- Los archivos de salida se llaman `datos/3T_replica_s21-40_<fecha>.*`.

Nada más cambia: brazos, `T`, constantes, criterios y umbrales son los del preregistro original
(`a094838aaf31614c`).

## 2. Predicciones — las mismas del preregistro original, sobre semillas nuevas

- **K1** 18/18. **K2** C2b ≡ C1, 20/20. **K4** el drenaje actúa, 20/20. **K3** no aplica.
- **E [exacta].** C3 y C3C bajo v8 **idénticos** a la referencia sin techo en las doce claves, en toda semilla
  donde ninguno trunca. Al menos una semilla elegible por brazo.
- **E-alcance.** v8 no trunca en C1p, C2, C3 ni C3C (0/20 cada uno); la referencia C3 no trunca en ≥18/20.
- **Criterios de C3:**
  - 1: mediana de `solap_A` ≤ 1 y ≥15/20 con ≤ 1;
  - 2: mediana de `sep` ≥ 1.0;
  - 3: mediana de `lift_q4` ≥ 0.15.
- **Criterio 4 (C3C):** mediana de `sep` < 1.0 **y** mediana de `lift_q4` < 0.15.
- **Por semilla, sin conocer ningún valor de estas semillas:**
  - C3: `sep ≥ 2.8` en ≥18/20 y `lift_q4 ≥ 0.15` en ≥18/20;
  - divisiones: mediana ≤ 30, y la última antes de t=25.000 en ≥15/20;
  - C3C agota el pool en ≥15/20.

## 3. Qué se decide

- **Réplica SÍ** (K1, K2, K4, E, criterios 1–4): el resultado de 3T queda **replicado en semillas no vistas y con
  el instrumento corregido antes de verlas**.
  - **ERR-13 se cierra**: el resultado ya no depende de la corrección post-hoc.
  - La advertencia "no es ciego" se reduce a que se conocían las cifras agregadas de PH3, no las de estas semillas.
- **Réplica NO:** 3T confirmatorio **no se considera replicado**. Se registra junto al SÍ de las semillas 1–20,
  sin borrar nada, y se lleva a dirección. No se recalibra nada (regla 3).
- **Si E falla:** se diagnostica **antes** de cualquier lectura. Si fuera otra vez un artefacto de comparación,
  sería un error nuevo y se trataría como tal, **no** como una corrección silenciosa.
