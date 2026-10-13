# VEREDICTO — entrada del registro

Copiada de `registro/REGISTRO_etapas_1_2.md`, líneas 3725–3757 y 3805–3836.

---

### Bloque B-1 (célula de creación, creador B; 18 sep 00:07): hija dispersa en 3T-k, semillas 61–80 — **REFUTADA por la letra (R1: el ahorro de celdas 16/20, se exigían 18/20); la conducta pasa y la relevancia gana a la máscara al azar**

Preregistro `experimentos/nivel7_hija_dispersa/PREREGISTRO_hija_dispersa.md` (a3c7af91453598ad, escrito antes de correr);
instrumento `mundo_hija_dispersa.py` (d305d53186fcbcd6, por anclas desde `mundo_temporal_k` 68736baafe7c8cdb; identidad
7/7 en la copia principal y 3/3 dentro del runner); datos `hija_dispersa_s61-80_20260918_000202` (dd86cdbb45041c37),
466 corridas, 4.9 min. Mecanismo: una línea del nacimiento de v11 — la hija nace ciega a parte de los píxeles de `P`
(REL: por relevancia, con medias de `P` condicionadas al signo de R; AZAR: subconjunto al azar de la misma cardinalidad;
SLOT: máscara con el slot profundo intercambiado, control de artefacto; RELD: REL + división diferida n_cf = 4).

| k = 5, C3 | `sep` mediana | `lift_q4` | divisiones | celdas | muertes | C3C (canal falso) |
|---|---|---|---|---|---|---|
| V13 | 1.87 | 0.137 | 60 | 90 | 78 | sep 0.07 |
| **REL** | **3.09** | **0.251** | **18** | **48** | 88 | 0.14 |
| RELD | 2.42 | 0.255 | 16 | 46 | 88 | 0.03 |
| AZAR | 2.02 | 0.191 | 42 | 72 | 70 | −0.00 |
| SLOT | 2.17 | 0.172 | 60 | 90 | 72 | −0.02 |

Criterios: **P1 (celdas ≤ 0.75 × V13 en ≥ 18/20) NO: 16/20** (a k = 4, ≤ 0.85 ×: también 16/20) → **R1, refutación por
la letra, sin reajustar umbrales**. P2 (lift ≥ 0.18 y > V13 en ≥ 15/20): **0.251 y 18/20 OK** (k = 4: 0.329 y 17/20).
P3 (sep ≥ 2.2 y C3 − C3C ≥ 1 en ≥ 18/20): **3.09 y 20/20 OK** (k = 4: 3.51 y 20/20). P4 inercia a k = 1: REL ≡ V13
semilla a semilla **20/20**. **R3 (REL > AZAR en ≥ 14/20): 16/20 a k = 5 y 15/20 a k = 4 → la relevancia SÍ pesa** (lo
contrario de lo que el propio creador esperaba). R4 (SLOT > REL): 4/20 y 5/20 → sin artefacto. Canal falso limpio en
los cinco brazos. Muertes: REL 88 contra 78 (no era criterio; se anota).

**Lectura honesta.** El mecanismo mejora la composición a k = 4 y k = 5 (18/20 pareado), separa mejor, gana al control al
azar y al del slot equivocado, y usa la mitad de las celdas en la mediana — pero la predicción numérica del ahorro (18/20)
no se cumplió (16/20) y la cláusula R1 la escribió el creador como refutación entera. Se registra REFUTADA tal como
estaba escrita. **Enmienda 1 (escrita ahora, ANTES de la serie nueva, criterio nuevo en semillas nuevas, sin tocar 61–80):**
serie 81–100 con los mismos brazos y umbrales, salvo P1 que pasa a **≥ 14/20** (mayoría, derivado de lo visto en 61–80 y
declarado como tal); si P1–P3 y R3 se repiten en 81–100, el vocabulario permitido es el preregistrado: *"la hija que nace
ciega a lo irrelevante compone historias más profundas con menos celdas"*; si P1 vuelve a caer, el mecanismo queda como
*"compone mejor; el ahorro de celdas es mayoritario, no general"*. Nada toca el tronco (§6 del preregistro: baterías
antes).

[…]

### Bloque B-1, réplica 81–100 bajo la enmienda 1 (18 sep 00:15): **PASA — y pasa también por la letra ORIGINAL (P1 19/20 a k = 5, 18/20 a k = 4)**

Datos `hija_dispersa_s81-100_20260918_000954` (bdc705609bac2633), 466 corridas, identidad 3/3 dentro del runner.

| k | brazo | `sep` mediana | `lift_q4` | divisiones | celdas | muertes |
|---|---|---|---|---|---|---|
| 5 | V13 | 1.85 | 0.128 | 60 | 90 | 79 |
| 5 | **REL** | **3.62** | **0.352** | **8** | **38** | 102 |
| 5 | RELD | 3.40 | 0.358 | 10 | 40 | 94 |
| 5 | AZAR | 2.16 | 0.201 | 40 | 70 | 72 |
| 5 | SLOT | 2.12 | 0.205 | 58 | 88 | 72 |
| 4 | V13 | 2.11 | 0.135 | 45 | 75 | 86 |
| 4 | **REL** | **3.10** | **0.314** | **13** | **43** | 92 |
| 4 | AZAR | 2.35 | 0.205 | 32 | 62 | 76 |
| 4 | SLOT | 2.30 | 0.217 | 32 | 62 | 81 |

P1 celdas ≤ 0.75 × V13: **19/20** a k = 5 (≤ 0.85 ×: **18/20** a k = 4) — cumple P1' (≥ 14) **y** el umbral original (≥ 18).
P2 lift 0.352 y > V13 **19/20**. P3 sep 3.62 y C3 − C3C ≥ 1 en **20/20**. P4 inercia a k = 1: **20/20**. R3 REL > AZAR
**16/20** (k = 4: 14/20). R4 SLOT > REL 4/20 (k = 4: 6/20). Canal falso limpio. Muertes REL 102 contra 79 (se anota; no es
criterio). **Dos series:** conducta > V13 en 18/20 y 19/20; relevancia > azar en 16/20 y 16/20; ahorro de celdas 16/20 y
19/20; inercia 20/20 y 20/20.

**Declarable (nivel 7):** *la hija aprende a ignorar lo irrelevante y compone historias más profundas con menos celdas*
— a k = 4 y k = 5 compone mejor que v13 (lift 0.31–0.35 contra 0.13; separación 3.1–3.6 contra 1.9–2.1) con **la mitad
de las celdas y una décima parte de las divisiones**, y qué píxeles conserva **sí** importa (gana a la máscara al azar
de la misma cardinalidad en 16/20 dos veces; el slot equivocado no gana). Mecanismo: una línea del nacimiento de v11
(`rel ⊊ (P > 0)` por medias de `P` condicionadas al signo de R; memoria: dos vectores `NIN` y dos escalares por celda).
**Antes de tocar el tronco (§6 del preregistro):** `bateria_v13.py` 8/8 y `bateria_generaliza.py` G1 ≥ 0.80 / G2 ≥ 0.85
sobre un `organismo_v13` con la misma perilla (copia por anclas, identidad con la perilla apagada); la decisión de v14
es del director. Convergencia con B1/A5: el techo de la composición no era el pool de celdas (duplicarlo no devuelve
nada) sino la evidencia por código; la hija dispersa cierra el conflicto de la madre con una sola hija por familia de
rellenos.
