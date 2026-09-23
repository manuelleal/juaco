# PREREGISTRO N7-NL — ¿compone el TRONCO v14.2 en 3T-k? y la vía lenta normalizada por masa

**Escrito ANTES de la serie, 23-sep-2026 (creador del equipo del nivel 7).** Semillas de la serie y de la réplica
sin tocar. Lo único corrido antes: arnés de identidad (114/114) y mini-prueba/humo de un proceso en las semillas
7798–7799 (fuera de la serie; números abajo, **no son dato**). Nivel 7 hoy: 70 %.

## 0. Qué se sabe y qué hueco ataca

- "3T-k compone hasta 3" se midió en **v13** (eta_s 0.015). La hija dispersa a k = 4/5 (B-1, dos series) y la
  composición v14c (C3, k = 5, lift 0.237) se midieron también con **eta_s 0.015, clip_s 3**
  (`corre_composicion_v14.py`, `V13KW_3T`). **El tronco vigente v14.2 lleva eta_s 0.15, clip_s 10 (A-4, v14.1) y
  B-5; nunca se midió en 3T-k** y ninguna batería del tronco contiene 3T-k (grep: `bateria_v142.py`,
  `bateria_generaliza_v142.py`, `CRITERIO_TRONCO_v4.md`). Es el patrón de ERR-20 (etapa cerrada sin batería).
- Mini-prueba (semillas 7798–7799): el tronco tal cual **deja de morder** en 3T-k a k ≥ 3 (6–15 mordidas en
  100 000 pasos, 327–331 muertes; a k = 2, lift 0.0 en 7798 y 0.395 en 7799). Causa mecánica: la entrada de 3T-k
  tiene masa 3(k+1); un solo veneno (R = −3) sube `Wns` 0.45 en **cada** píxel activo y el valor lento de todo
  patrón cae a ≈ −0.45·3(k+1); con puerta por código (familiar sólo tras 5 mordidas) decide la vía lenta, la boca
  no vuelve a morder y no hay más aprendizaje. La vía rápida no tiene el problema: su código son siempre 3 celdas.

## 1. Hipótesis y mecanismo mínimo

**H:** la vía lenta del tronco no está normalizada por la masa de su entrada (la rápida sí, por construcción).
Normalizarla (**norm_lenta**: el paso de `Wps/Wns` se multiplica por `M0 / (P·P)`, `M0 = 3.0` = masa de un
estímulo en todos los mundos del tronco) devuelve la composición al tronco y la lleva más lejos que k = 3.
**Memoria nueva: cero. Constante nueva: M0 = 3.0, fijada por el tronco, no se ajusta.** En todos los mundos del
tronco `P·P = 3` → factor 1.0 exacto → **inerte por construcción** (verificado: 30/30 bit a bit con la perilla
encendida en los 12 escenarios del examen y en regla px0/xor01/azar). El mundo vivo usa `PAT[kk]` de masa 3:
inerte por construcción allí también (no corrido). En 3T-k equivale a `eta_s/(k+1)`.

## 2. Instrumento y anclas

`construye_n7.py` genera por anclas (conteo exacto, aborta si no):
`mundo_n7.py` ← `experimentos/nivel10_composicion_v14/mundo_composicion_v14.py` (`a9098933b1950e3d`) + B-5
transcrito de `organismo/organismo_v142.py` (`17528d767fcebaf6`; la línea se verifica literal en el congelado) +
`norm_lenta`; `organismo_v142N.py` ← `organismo_v142.py`; `organismo_v142gN.py` ← `organismo_v142g.py`
(`9e5f566cd6a7a4d2`). Runner `corre_n7.py`; identidad `identidad_n7.py` (salida en `identidad_n7_salida.txt`).
Entrada **campo a campo** contra el tronco (regla 14 / ERR-38): los 25 kwargs de `TRONCO` = defaults de
`organismo_v142.run`; `nkmax` 90, `wclip` 3., K = 3 comprobados (bloque K del arnés, 28/28).

## 3. Brazos (todos `arm='C3'`, historia visible y plástica, salvo NC3C), k ∈ {1,…,8}, T = 100 000

| brazo | qué es | papel |
|---|---|---|
| T142 | el tronco v14.2 tal cual (B-5 encendido) | la pregunta de regresión |
| **N** | T142 + `norm_lenta=1` | **candidato** |
| L015 | T142 con la vía lenta de v14.0 (eta_s 0.015, clip_s 3) | **control que puede ganar** ("basta un paso chico") |
| N141 | N sin B-5 | qué hace B-5 en un mundo con R = 0 (exploratorio) |
| NAZAR | N con máscara al azar de la misma cardinalidad (`mask_rel=4`) | **control que puede ganar** |
| NSH | N sin hija dispersa (`mask_rel=0`) | qué aporta la hija |
| NC3C | N con canal falso (historia aleatoria; el mundo usa la real) | artefacto |

## 4. Criterios (letra de 3T-k, sin tocar; T2 uniforme)

Por brazo y k: **T1** `solap_A` ≤ 1 en ≥ 15/20; **T2** `sep` mediana ≥ 1.5; **T3** `lift_q4` mediana ≥ 0.15
(lift `None` = no mordió A en el último cuarto → cuenta 0.0); para N además **T4** NC3C `sep` < 1.0 y
`lift_q4` < 0.15, y **T5** `sep(N) − sep(NC3C)` ≥ 1.0 en ≥ 15/20 (pareado). "Compone a k" = pasa todos.
`K_max` = mayor k tal que todos los k′ ≤ k componen.

## 5. Predicciones numéricas (con rango)

- **P1 (regresión; puede fallar):** T142 **no** compone para k = 3…8: `lift_q4` mediana < 0.15 en ≥ 5 de esos 6 k,
  con mordidas medianas < 200 y muertes medianas ≥ 2 × las de N. A k = 1 sí compone (lift ≥ 0.15). k = 2 sin
  predicción (0.0 y 0.395 en la mini-prueba).
- **P2 (candidato):** N compone en k = 1…5 en serie y réplica; `K_max(N)` ∈ {5, 6, 7}; `lift_q4` a k = 5 en
  [0.25, 0.40]; `sep` ≥ 3.0 para k ≤ 5. N > T142 en `lift_q4` pareado ≥ 15/20 para k = 3, 4, 5.
- **P3 (puede fallar, techo):** a k = 8 N **no** compone: `lift_q4` en [0.08, 0.20] con celdas mediana ≥ 85
  (pool agotado). Confianza ~60 %.
- **P4 (control que puede ganar):** L015 y N no se distinguen para k ≥ 3: N > L015 pareado entre 6 y 14 de 20.
  Si L015 > N en ≥ 15/20 en algún k ≤ 5, se escribe así.
- **P5 (la hija sigue pesando):** a k = 5, celdas N ≤ 0.75 × NSH (mediana) y N > NAZAR en `lift_q4` pareado ≥ 13/20.
- **P6 (artefacto):** NC3C `sep` mediana < 1.0 y `lift_q4` < 0.15 en todo k (riesgo a k = 2: 1.25 en la mini-prueba).
- **P7 (reportado, sin umbral):** `n_des` (divisiones de B-5) de N > 0 en mediana para k ≥ 5; N frente a N141 sin
  dirección predicha.

## 6. Veredicto (vocabulario permitido) y puntos propuestos (decide el director)

- **FUNCIONA** = P1 y P2 en serie **y** réplica (K_max(N) ≥ 5 en las dos), P6 limpio. *"El tronco v14.2 deja de
  componer en 3T-k a partir de k = 3 porque su vía lenta, con el paso de A-4, cierra la boca cuando la entrada es
  ancha; con la vía lenta normalizada por la masa de la entrada (inerte en los mundos del tronco) compone historias
  de hasta K pasos con distractores (replicado)."* Propuesta: **70 → 78 %**; si luego entra como reparación inerte
  v14.3 bajo el criterio v4 (una puerta más: T-A..T-H en semillas nuevas), **80 %**.
- **HAY ALGO MODESTO** = N compone hasta 3–4 en las dos series, o K_max ≥ 5 en una sola, o L015 gana a N
  (≥ 15/20) en algún k ≤ 5. Propuesta: **+3 (73 %)** y la regresión registrada.
- **NO** = K_max(N) < 3 en alguna serie, o P6 cae a k ≤ 3. Si además P1 se confirma: la composición del nivel 7
  no vale para el tronco vigente → propuesta **70 → 65 %** hasta reparar. Si P1 cae (el tronco compone a k ≥ 3): no
  hay regresión; se declara `K_max(T142)` como la composición del tronco, sin candidato.
- **Prohibido:** "planifica", "razona", "memoria de trabajo", "atiende", "entiende secuencias", "aprende XOR".

## 7. Trampas revisadas

(1) Canal simétrico: el canal falso NC3C ve historia aleatoria con el mismo formato y el mismo rng aparte. (2)
Acierto sin balancear: `lift = acc − base`, base = fracción de mordidas con slot profundo B (se descuenta la tasa
base). (3) Mundo que se come la comida: cada mordida repone un objeto al azar; un brazo que deja de morder queda con
lift 0 y se reportan mordidas y muertes. (4) Sitios fijos: posiciones sorteadas en cada reposición. ERR-35: no se
pregunta XOR sin prior. ERR-38: kwargs campo a campo.

## 8. Semillas nuevas (grep en `bundle` y worktrees: ningún uso previo de 77xx como semilla)

Serie **7701–7720**; réplica **7721–7740**; mini-prueba y humo 7798–7799 (quemadas, fuera de la serie).
