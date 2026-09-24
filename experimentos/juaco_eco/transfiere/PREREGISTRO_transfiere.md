# PREREGISTRO — ECO-T: ¿lo que la selección eligió en ECO vive mejor en OTRO mundo? (24-sep-2026, coordinador de la nube; antes de la serie)

Misión: llegar a la AGI por este camino. Carpeta: `experimentos/juaco_eco/transfiere/`. Nivel: **10 (JUACO-ECO)**, frente 2. Archivos nuevos;
no se toca nada del PC. Escrito bajo la regla 12.

## 0. Instrumento (sha a 16)
- `corre_transfiere.py` (**629b30d6c184572f**; el sha va también en el log y en `RESUMEN.json`). Usa sin tocar `carrera_escuderias/pista.py`
  (9f47c65e438e0ff4), `juez.py` (6a68f640a7832f12), `carros/FABRICA.py` (2ebee3e99ea5a33a) y `motor_eco.py` (bca3033878b59622; sólo
  `GENES`, `ctx_genoma` y `genoma0`).
- Arnés `identidad_transfiere.py`: **14/14** — (I) la colonia de 9 × G0 = FABRICA en toda la física; (A) el genoma llega a su línea y la
  historia de vida del ctx no cambia; (B) muestreo; (V) la letra; (R) banderas (ERR-115).
- Humo (11:19, banco de VIDA 19401, T 5 000): 4 s por brazo; ~80 s por corrida de T 100 000.

## 1. Pregunta, y por qué ahora
ECO v1.1 (HAY ALGO MODESTO ×2) mostró que la colonia de genomas seleccionados vive 3.2–3.3× más que la de genomas que sólo derivaron, **en
el mundo donde se seleccionaron** (pista v2, flujo fijo). Pregunta: ¿es adaptación a ese mundo o algo más general? Se mide en OTRO mundo:
la pista de la carrera (pista v1: reposición inmediata, 9 líneas, fundador limpio), con el carro FABRICA.
**Dato exploratorio visto antes de escribir esto (declarado):** FABRICA con las tres perillas medianas de CEREBRO (alpha ×1.61,
aversion ×1.29, eta_s ×1.26) gana a FABRICA en la carrera 6/6 (0.147 → 0.269; `NOTA_EXPLORATORIA.md`). Aquí no se eligen perillas: se usan
los genomas enteros de los bancos, y la deriva (AZAR) es el control.

## 2. Diseño
- **Entrada:** los bancos en el corte de ECO v1.1, ya corridos y commiteados (sus veredictos no cambian):
  ventana **serie** = bancos de las semillas 19401–19420; ventana **réplica** = 19421–19440.
- **Colonia:** en la semilla c = s + 10 000 (**29401–29440**, nuevas: grep sin usos), cada una de las 9 líneas lleva un genoma: 9 entradas
  al azar del banco con el rng [c, 7] (el mismo muestreo que el juez de ECO). Los 3 genes de historia de vida (dote, rep_umbral, rep_X)
  se dejan en G0: en la carrera los fija la pista. Se aplican con `ME.ctx_genoma` (15 genes de cerebro y estructura).
- **Brazos por semilla:** VIDA (banco de VIDA), **VIDA_P** (placebo: otra muestra de 9 del MISMO banco, rng [c, 8]), AZAR (banco de AZAR),
  G0 (9 × FABRICA de fábrica).
- **Medida:** R0 real (`juez.resumen_linaje`), mediana de las 9 líneas. T 100 000, `fundador_limpio=1`, pizarra 1.

## 3. Predicciones firmadas
| cantidad | rango | probabilidad |
|---|---|---|
| VIDA > G0 /20 | 14–20 | T2 (≥ 15) con 0.75 |
| **VIDA > AZAR /20 — la que puede fallar** | 12–20 | T1 (≥ 15) con 0.65 |
| AZAR > G0 /20 (descriptivo) | 4–14 | — |
| placebo VIDA contra VIDA_P en [5, 15] | — | 0.95 |
| R0 real mediano: VIDA / AZAR / G0 | 0.20–0.32 / 0.08–0.20 / 0.13–0.17 | — |

## 4. Qué refuta
- **"Transfiere":** T1 cae (lo seleccionado no vive mejor que lo derivado en la carrera) o T2 cae (no vive mejor que G0).
- **El instrumento:** placebo fuera de [5, 15].

## 5. Criterio por la letra (`corre_transfiere.veredicto`; se imprime al final)
- **T1:** VIDA > AZAR (pareado por semilla, estricto) en ≥ 15/20 (P = 0.021 bajo la nula).
- **T2:** VIDA > G0 en ≥ 15/20.
- **NO EVALUABLE:** ventana incompleta; placebo (victorias de VIDA sobre VIDA_P + empates/2) fuera de [5, 15].
- **TRANSFIERE:** T1 + T2. **HAY ALGO MODESTO:** sólo T2 ("mejor que G0, no se distingue de la deriva") o sólo T1. **NO:** ninguna.
- El bloque se declara sólo si serie y réplica dan el mismo veredicto; si no, vale el menor.
- Vocabulario: «el genoma seleccionado en ECO vive mejor en la carrera»; no «generaliza» ni «evoluciona».

## 6. Costo
80 corridas por ventana × ~80 s = ~1.8 h de CPU; con Pool 3, ~40 min por ventana.

## 7. Puntos
Ninguno propuesto aquí; lo decide el director.
