# LINAJE — árbol de evolución de JUACO-EVO

Cada fila es un individuo evaluado, gane o pierda. Preregistro: `PREREGISTRO_evo.md` (`684e5da82227e04d`).
Operadores: **llm** (subagente Claude Fable 5.1, una hipótesis por mutación) y **ciega** (`muta_ciega.py` v0).
Semillas: entrenamiento 1–10; retenidas 11–20 sólo para el candidato a ganador. Nada de aquí es tronco sin confirmatorio
y examen criterio v3.

## Generación 0 — padre
| individuo | sha | R (train) | R (retenidas) | S | E | notas |
|---|---|---|---|---|---|---|
| `organismo_v10m.py` | c33253b850570308 | **0.3** (3/10; W_B100 mediana −1.23) | **0.4** (4/10; −2.18) | 0.36 | 0.67 | v10 = v9 + mu normalizada; examen v3 8/8; no congelado (ERR-17). H1–H3 ✅ en los dos conjuntos; muertes E1 127.5 / 136; E2L 3 divisiones |

## Generación 1 — linaje LLM (padre v10m). Datos: `gen1/puntuaciones.json`
| individuo | operador | sha | R (1–10) | R (11–20) | S | E | C | válido | veredicto |
|---|---|---|---|---|---|---|---|---|---|
| **llm_2** división por conflicto de signo, hija ciega, madre fija, fisión del valor | llm | f9cce63d371977ed | **1.0** | **1.0** | 0.36 | 0.67 | 0.80 | ✅ | **GANADOR.** Predijo 0.8–0.9; E1 idéntico al padre; E2 pasa 10/10; E2L 3 divisiones; sigue dividiendo en la ausencia (3 / 5); aprende C y D 10/10. Auditoría P4: retiene por el mecanismo declarado |
| llm_3 repaso por celda con puerta de edad (Rc, tc) | llm | 9392a1d998e2aad2 | 1.0 | — | 0.32 | 0.67 | 0.80 | ✅ | elegible; perdió el empate por muertes. Usa estado nuevo (declarado) |
| llm_1 reparto del crédito por compromiso opuesto | llm | e4ec4109150e8bab | 0.5 | — | 0.36 | 0.67 | 0.67 | ❌ H3 | retiene a costa de no aprender D (lo declaró él mismo como razón equivocada) |
| llm_4 reparto del crédito por familiaridad | llm | c8d1689236c423f1 | 0.3 | — | 0.36 | 0.67 | 0.73 | ✅ | sin efecto |
| ciega_1 lam ×1.12 | ciega v0 | 176bd194220d89d5 | 0.3 | — | 0.36 | 0.67 | 0.13 | ✅ | nada |
| ciega_2 E inicial ×1.37 | ciega v0 | 5ddf7d85ff4e00e5 | 0.4 | — | 0.35 | 0.67 | 0.13 | ✅ | elegible por R; no ganó |
| ciega_3 lam ×1.67 | ciega v0 | 1841cdea5eaa315b | 0.3 | — | 0.36 | 0.67 | 0.13 | ✅ | nada |
| ciega_4 energía tras morir ×1.76 | ciega v0 | 2ef122ae23e85212 | 0.4 | 0.4 | **0.52** | 0.67 | 0.13 | ✅ | **hueco del evaluador (ERR-18):** muere menos por constitución, no por aprender. Linaje ciego v0 anulado; se rehace con v1 |

**P4, gen1:** 2 razones equivocadas detectadas (llm_1 por H3; ciega_4 por auditoría). **P2:** el ganador tenía hipótesis y
predicción escritas antes; el resultado superó la predicción. **P3:** ningún sobreajuste en esta generación.
