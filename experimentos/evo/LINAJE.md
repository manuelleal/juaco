# LINAJE — árbol de evolución de JUACO-EVO

Cada fila es un individuo evaluado, gane o pierda. Preregistro: `PREREGISTRO_evo.md` (`684e5da82227e04d`).
Operadores: **llm** (subagente Claude Fable 5.1, una hipótesis por mutación) y **ciega** (`muta_ciega.py` v0).
Semillas: entrenamiento 1–10; retenidas 11–20 sólo para el candidato a ganador. Nada de aquí es tronco sin confirmatorio
y examen criterio v3.

## Generación 0 — padre
| individuo | sha | R (train) | R (retenidas) | S | E | notas |
|---|---|---|---|---|---|---|
| `organismo_v10m.py` | c33253b850570308 | **0.3** (3/10; W_B100 mediana −1.23) | **0.4** (4/10; −2.18) | 0.36 | 0.67 | v10 = v9 + mu normalizada; examen v3 8/8; no congelado (ERR-17). H1–H3 ✅ en los dos conjuntos; muertes E1 127.5 / 136; E2L 3 divisiones |
