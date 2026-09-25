# PREREGISTRO: H-PLANO en w90, serie y réplica (para el PC)

Escrito en la nube el 25-sep-2026, ~12:15, **antes de correr cualquier semilla de 25111–25150**.
**Misión:** llegar a la AGI por este camino.
**Autor:** Claude (nube), a pedido del director.

## 1. Pregunta
¿La carga de la mutación de la gramática (Ohno) se purga cuando la población crece?

**H-PLANO** (`../nube_20260925/SINTESIS_noche_H-PLANO.md`): con N chico, la selección no le gana a la deriva (N·s < 1) y la variación es carga; con N mayor, la carga se purga.
- **Versión débil:** VIDA deja de ser peor que FIJO.
- **Versión fuerte:** VIDA supera a FIJO (la variación paga).

## 2. De dónde viene (lo que ya se vio; no se vuelve a juzgar)
| Qué se corrió | Resultado |
|---|---|
| **Ohno w30, serie 25011–25030** (NO por la letra) | Sólo FIJO 4, sólo VIDA 0. Vivos VIDA/FIJO en pares que persisten: **0.67** (9 pares). 6 nacidos antes del corte. |
| **Exploratorio w90, 25101–25110** (AMBIGUO, no es dato) | M0 20 nacidos antes del corte. D = 1. Vivos VIDA/FIJO en pares: **0.97** (7 pares). VIDA > FIJO 3/10. |

**Ojo:** la razón de vivos en pares nació **post-hoc** en el exploratorio. Aquí se preregistra como primaria **antes** de ver semillas nuevas. Por eso vale.

## 3. Montaje (una sola cosa cambia frente a Ohno)
- **Mundo:** w90 (`esc` 90, `n0` 90, `tope` 9000), con `r_rep` 0.006, la misma pobreza por celda.
- **Sin tocar:** `corre_ohno.trabajo`, SERIE (T 80 000, corte 40 000, margen de R0 15 000), GRAM, el motor y las copias de `construye_ohno.py`.
- **Brazos:** VIDA y FIJO:filtra0. AZAR no entra: en w30 dio 0/20 y cuesta un 50 % más.
- **Semillas:** serie **25111–25130**, réplica **25131–25150**. No se han usado antes (lo comprobé con grep en el repo).
- **Runner:** `corre_hplano_w90.py` (sha `e9bf9c528f0509e3`).
  - Sólo cambia `corre_ohno.MUNDO` antes del fork.
  - Su `--lee` ya corrió sobre los JSON reales del exploratorio y la letra se leyó sin romperse (ERR-42).
  - `--prueba_pool` corre 4/4 en la nube.

## 4. La letra (por ventana, con los 20 pares completos y sin abortos)
**M0, manipulación.** Mediana de nacidos antes del corte ≥ **18** en los dos brazos. Si no se cumple → **NO EVALUABLE**.

**P1, primaria.** Mediana de `vivos_T` VIDA/FIJO en los pares donde **persisten los dos**, con al menos **8** pares evaluables.
- **Sostiene:** ≥ **0.90**.
- **Cae:** ≤ **0.75**.
- **Ambiguo:** en medio.
- **Guardia:** con menos de 8 pares → **NO EVALUABLE**.

**S1, secundaria.** D = (sólo FIJO) − (sólo VIDA) en persistencia pareada.
- **Sostiene:** D ≤ **1**.
- **Cae:** D ≥ **4** (la tasa de w30).

**S2, versión fuerte.** `vivos_T` VIDA > FIJO pareado y estricto, ≥ **15/20**.

**Veredicto de la ventana:**
| Veredicto | Condición |
|---|---|
| **CAE** | P1 ≤ 0.75 o D ≥ 4 |
| **SOSTIENE (débil)** | P1 ≥ 0.90 y D ≤ 1 |
| **SOSTIENE (débil) + FUERTE** | lo anterior y S2 ≥ 15/20 |
| **AMBIGUO** | cualquier otro caso |

**Veredicto del bloque:** serie y réplica con el mismo veredicto. **Si la serie da CAE o NO EVALUABLE, la réplica no se corre.**

**Descriptivo, no es letra:**
- persistencia por brazo, nacidos tras el corte;
- R0 tras el corte con su rango (ERR-133: el quimiostato lo fija cerca de 1);
- `g_nmut`.

## 5. Predicciones firmadas (Claude, nube)
| Resultado | Probabilidad |
|---|---|
| SOSTIENE (débil) | 0.45 |
| AMBIGUO | 0.35 |
| CAE | 0.15 |
| NO EVALUABLE | 0.05 |
| **FUERTE** | **0.05** (no espero que la variación pague ya en w90) |

## 6. Qué haría cada resultado
- **SOSTIENE ×2:** la distancia es de escala. El siguiente paso es **w270** con el gemelo numba (`ESPEC_GEMELO_anfitrion.md`) y la misma letra, buscando S2 (la versión fuerte).
- **CAE:** H-PLANO pierde su prueba más barata. El muro no es N, y no se gasta en máquinas más grandes.
- **AMBIGUO:** no se escala. Se escribe qué faltó (¿poder? ¿el quimiostato?) antes de otro intento.

## 7. Riesgos declarados
1. **ERR-133 sigue en pie:** el quimiostato fija la densidad, así que P1 mide cuántos cuerpos sostiene cada genoma con la misma comida, no el R0.
2. **ERR-134:** la duplicación no se ejercitó en el arnés con `r_rep` 0.006. Aquí sí ocurre (`g_nmut` de VIDA ~1800), pero sin un caso de identidad propio.
3. Con ~14 pares esperados (7 de 10 en el exploratorio), P1 tiene poder moderado. Ése es el motivo del umbral de 8 pares.

## 8. Costo y comandos (desde la raíz del repo)
**Costo:**
- En la nube, w90 tarda ~530 s por corrida. En el PC se espera ~1.8× más, **~950 s**.
- Una ventana (40 corridas) con Pool 3 son **≈ 3.5 h**; con Pool 6, **≈ 1.8 h**.
- Serie y réplica con Pool 3 son **≈ 7 h**.

**Comandos:**
```
python experimentos/organelos/ohno/construye_ohno.py --verifica
python experimentos/organelos/ohno/hplano_nube/corre_hplano_w90.py --control                       # debe decir PASA (w30 == serie de Ohno s25011)
python experimentos/organelos/ohno/hplano_nube/corre_hplano_w90.py --prueba_pool --pool 2
python experimentos/organelos/ohno/hplano_nube/corre_hplano_w90.py --serie --ventana serie --pool 3
python experimentos/organelos/ohno/hplano_nube/corre_hplano_w90.py --lee experimentos/organelos/ohno/hplano_nube/datos/w90_serie_s25111-25130
# sólo si la serie NO da CAE ni NO EVALUABLE:
python experimentos/organelos/ohno/hplano_nube/corre_hplano_w90.py --serie --ventana replica --pool 3
python experimentos/organelos/ohno/hplano_nube/corre_hplano_w90.py --lee experimentos/organelos/ohno/hplano_nube/datos/w90_replica_s25131-25150
```
Tras un corte, se repite la misma línea con `--reanuda`.

## ERR-143 (coordinador del PC, 25-sep ~10:40, ANTES de cualquier semilla 25111–25150; auditoría juaco-auditor: LISTO CON CORRECCIONES, H-3)
- P1 pasó a primaria después de verla post-hoc en el exploratorio. Sus bordes quedan cerca de valores ya vistos: 0.90 contra 0.971 visto
  en w90, y 0.75 contra 0.67 visto en w30. El documento no declaraba el nulo (regla 15 / ERR-91). Por la regla 11 lleva ERR. Los umbrales
  NO se tocan: ya están fijados y recalibrarlos ahora sería peor.
- **Nulo, declarado aquí.** Si VIDA y FIJO fueran intercambiables (sin carga), la mediana de la razón de vivos en pares estaría cerca de 1.0.
  Entonces P1 ≥ 0.90 PASA bajo el nulo con alta probabilidad. SOSTIENE (débil) es una afirmación de **no inferioridad**: "la variación ya
  no es carga". No afirma que la variación pague. Su contenido está en el contraste con w30 (0.67, CAE). La única prueba de
  **superioridad** es S2, cuyo nulo es 15/20 con p ≈ 0.021 (una cola, prueba del signo).
- Lectura obligatoria en el registro: "SOSTIENE (débil)" se escribe siempre con la frase "no inferioridad; compatible con el nulo de no
  diferencia".
- Verificado por el coordinador en el PC antes de la serie: sha de `corre_hplano_w90.py` = e9bf9c528f0509e3, `construye_ohno.py
  --verifica` OK, `--control` PASA (VIDA y FIJO s25011 idénticos campo a campo).
