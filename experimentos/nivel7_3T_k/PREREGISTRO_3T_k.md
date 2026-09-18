# Nivel 7 (composición), experimento 1 del plan: ¿compone v13 historias de 2 y 3 pasos? (3T con profundidad k)

**Escrito ANTES de construir el instrumento y ANTES de correr. 17 sep 2026, noche del día 5.** Es el primer experimento
del plan del debate (`registro/investigacion/DEBATE_y_plan_5a10.md`, §3). Regla 12.

## 0. Qué se sabe

3T (k = 1): el valor de A depende de si el estímulo **anterior** fue A o B; v13 separa los dos contextos (`sep` 3.96,
`lift_q4` 0.388, `solap_A` 0) porque la división por conflicto de signo aprende a usar las columnas temporales de la
entrada; el control con canal falso (C3C) no lo logra (−0.36). Sólo se ha medido **un** paso de historia. El organismo
**no cambia** en este experimento: se extiende el **mundo**, y por eso no hace falta re-verificar retención ni
generalización (lo dice el debate y es trivialmente cierto).

## 1. Mundo con profundidad k (instrumento `mundo_temporal_k.py`, desde `mundo_temporal_v13.py` `f9c3169b32f393d4`)

- La entrada del organismo es `[PAT[actual], PAT[h1], PAT[h2], …, PAT[hk]]` (`NIN = 6·(k+1)`), donde `h1` es el último
  estímulo mordido, `h2` el anterior, etc.
- **Regla del mundo:** B es neutro; A es comida si `hk == B` y veneno si `hk == A`. El contexto que importa es el **más
  profundo**; los intermedios son **distractores** que el organismo tiene que aprender a ignorar. Con k = 1 es
  exactamente el mundo de 3T (identidad obligatoria, todas las claves, 6 brazos × semillas 1–3).
- Situaciones: `A|A` y `A|B` según el valor del slot profundo, promediando `W` y el solapamiento de códigos sobre los
  2^(k−1) rellenos de los distractores.
- Brazos (los de siempre): C1 (sin canal temporal), C1p, C2b (columnas temporales a cero, sin plasticidad), **C3** (a
  cero, con plasticidad: la pregunta) y **C3C** (canal falso: historia barajada). k ∈ {1, 2, 3}; semillas 1–20.

## 2. Criterios (los de 3T, por k) y predicciones (del debate, sin tocar)

- **T1k:** `solap_A` de C3 ≤ 1 (media sobre rellenos) en ≥ 15/20. **T2k:** `sep`(C3) mediana ≥ **3.0 con k = 2** y ≥ **2.0
  con k = 3**. **T3k:** `lift_q4`(C3) ≥ 0.15. **T4k:** C3C `sep` < 1.0 y `lift_q4` < 0.15. **T5k:** `sep`(C3) − `sep`(C3C) ≥
  1.0 en ≥ 15/20 (pareado). **T6k:** C2b y C1p con `sep` < 1.0 (sin plasticidad o sin canal no hay composición).
- **Predicción:** k = 2 pasa todo; **k = 3 es la duda** (4 rellenos distractores por contexto: `sep` entre 1.5 y 3.0, y
  `solap_A` puede subir). **Refutación:** si k = 2 falla T2k/T5k, la composición de más de un paso **no** está al alcance
  de esta regla y el debate ya escribió la consecuencia: crecer celdas, gradiente local acotado o cambiar de mundo.
- Réplica en 21–40 si pasa. Si pasa k = 2 y no k = 3, se escribe "compone hasta 2".
