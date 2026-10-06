# o1_libre_f2 "un gen por parto" — cierre (1-oct-2026, 11:45)

**SERIE: NO, fuera del umbral → BLOQUE NO sin réplica** (letra 08832016, PREREGISTRO_o1_libre_f2.md sec. 5-6; serie i744201-744210).
Matiz por código: "la carga se quitó (el neutro no se degrada) y lib sigue bajo O1: la carga no era lo que tapaba".

| | F2 (un gen por parto) | o1_libre serie / réplica (14 genes por parto, histórico no pareado) |
|---|---|---|
| validez V1-V8 | True | — |
| PF1 R0 mediano del neutro ≥ 0.90 | **0.969 (pasa)** | 0.795 / 0.620 |
| PF2 cruces lib − o1 ≥ −5 | **−15 (no pasa)** (lib 57, o1 72) | −11 / −30 |
| cruces del neutro | 54 | 30 / 32 |
| PC conquista (mix > 0, pide 8/10) | 1/10 | 4/10 / 4/10 |
| PN (mix > mixn, pide 8/10) | 6/10 | 4/10 / 5/10 |
| PP algún poder | no (dif ≤ 0.011) | MEM 10/10 / 6/10 |
| reloj por gen (neutro) | 0.76 | ~11.9 / ~11.7 |
| Ne de linajes · padres distintos por siembra | 8.2–8.5 · 23–26 | 8.1–8.5 · 23.5–26 |
| extinciones · abortos | 0 · 0 | 0 · 0 |

Lectura (sin mover la letra):
- La predicción PF1 de la ficha se cumple: con un gen por parto el neutro deja de degradarse (R0 0.97 ≈ O1 0.98). La carga de 14 genes por parto SÍ explicaba la caída de R0 del neutro (relativo al histórico no pareado).
- La predicción PF2 falla: lib sigue cruzando menos que O1 de fábrica (−15). La carga no era lo que tapaba la subida.
- La predicción rival (PURGA) tampoco: firma_purga False.
- Predicción del creador refutada: veredicto MODESTO 0.68 / NO 0.16 → salió NO.
- Pregunta abierta (descriptivo, no veredicto): lib (57) y neu (54) cruzan casi igual y ambos bajo O1 (72), con genes a < 1 paso mutacional de fábrica y R0 mediano casi idéntico (0.979 / 0.969 / 0.981). El déficit de cruces no distingue selección de deriva y aparece con muy poca mutación: o el conteo "cruzan" es muy sensible a cambios mínimos cerca del umbral, o O1 de fábrica está en un pico estrecho. No se interpreta sin un control pareado (O1_LIB con σ 0 en las mismas semillas de prueba).
- Con ~0.76 pasos por gen, F2 no podía informar sobre subida de poderes (declarado antes de datos).

ERR de este bloque: ERR-161 (PF2 de ≥ 0 a ≥ −5, antes de datos). Siguiente libre de la rama: ERR-162.
Pool compartido 2+2+2 con la sesión organelos (excepción declarada, anotada en el log).
