# CRITERIO DE TRONCO v2 — vigente para candidatos NUEVOS desde el 18 sep 2026, 10:00 (decisión del director 09:55)

**Qué sustituye:** la regla "examen v3′ 8/8 + `bateria_generaliza` G1/G2 + coste ±10 %" como puerta absoluta del tronco (criterio v1,
CLAUDE.md regla 1). El criterio v1 sigue corriendo como **control de no regresión**, pero deja de decidir por sí solo.
**Qué NO hace:** rejuzgar candidatos ya medidos (v15c, v15d, v15e, B-5): sus veredictos quedan como están (no se recalibra después
de ver datos). v14.1 sigue siendo el tronco hasta que un candidato cruce este criterio en semillas nuevas y réplica.

## 1. Puertas (todas, en semillas nuevas, con réplica antes de congelar)

| # | puerta | medida | umbral (escrito aquí, antes de cualquier candidato) |
|---|---|---|---|
| T-A | **sobrevive** en el mundo vivo vigente (hoy: dos necesidades, cuatro estímulos, `costo = 0.001`) | muertes por 100 000 pasos y r = descendientes − muertes (bloque 2) | muertes ≤ 1.10 × tronco (mediana) y r ≥ tronco − 10; pareado por semilla A₁₂ ≥ 0.50 |
| T-B | **generaliza** a nunca vistos | `bateria_generaliza` G1/G2 en la configuración del candidato | G1 ≥ 0.80, G2 ≥ 0.85, azar en [0.35, 0.65], K 20/20 (sin cambio) |
| T-C | **se desdice** | reversión del examen (E2: tras el cambio de regla come B en Q4) y del mundo vivo (veneno que pasa a comida) | conducta E2 ≥ 18/20; reversión en el mundo vivo A₁₂ ≥ 0.75 contra apagado |
| T-D | **sin alias ni superstición** | bloque de la sal (9 ALIAS / 9 LIMPIAS) | C1, C2, C6 de B-5 |
| T-E | **no regresión conductual** del examen v3′ | por escenario: la CONDUCTA (come / evita / recupera) se conserva ≥ 18/20 | los pesos internos (W ≈ −3, etc.) se REPORTAN, no son puerta |
| T-F | **coste** | celdas, divisiones, muertes en el examen y en el mundo vivo | ≤ 1.25 × tronco (se declara antes si se espera más) |
| T-G | **capacidad nueva** | la que el preregistro del candidato declare, con control barajado y azar en banda | la del preregistro; sin capacidad nueva declarada no hay candidato (una reparación inerte como B-5 entra como v14.x, no como v15) |

## 2. Reglas
- Un candidato trae las siete puertas escritas en su preregistro con las semillas nuevas antes de correr; una sola caída → no entra, sin
  modos intermedios (regla 11 para cualquier cambio de umbral, con ERR).
- Réplica en semillas nuevas antes de congelar; regla 12 (±1 semilla) vigente.
- Perilla apagada ≡ tronco bit a bit e identidad con arnés (sin cambio).
- Instrumentos por anclas; baterías copiadas campo a campo (regla 14) y con un humo que escriba su JSON (ERR-42).
- **Este documento se completa con la síntesis de la SALA 2 (mundo que obliga → T-A y T-G se reescriben para ese mundo) ANTES del
  primer candidato; cualquier cambio posterior lleva ERR y fecha.**

Coordinador, 18 sep 2026 09:58.
