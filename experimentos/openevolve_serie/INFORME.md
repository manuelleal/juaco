# INFORME — Serie OpenEvolve sobre la pista de JUACO (nube, 6-oct-2026)

**VEREDICTO por la letra (PREREGISTRO_serie.md §6): NO.** Ninguna de las dos réplicas con Sonnet (A, B) ni el control con Haiku (H)
produjo un programa que cruce por mayoría en ninguna de las 5 semillas selladas nuevas: 0, 0 y 0 de 5. La validez se cumple (V1–V4).

**Lo bueno, descriptivo y fuera de la letra:** el mejor programa del humo del 5-oct (HUMO), examinado fuera de muestra en 5 semillas que
nunca vio, **cruza por mayoría en 5 de 5** (6, 9, 7, 8 y 7 de 9; 37 linajes). O1, escrito a mano, lo hace en 3 de 5 (26 linajes), y HUMO
le gana en 4 de las 5 semillas. **El programa del humo es robusto; lo que no se reproduce es la búsqueda que lo encontró.**

Vocabulario: evolución de programas guiada por un modelo de lenguaje sobre un juez fijo. No es selección natural ni "la selección cruzó el
muro".

## 1. Examen (5 selladas 275001–275005, T 100 000, fundador NO limpio; `examen/`, 30/30 corridas, todas pasan el filtro)
| programa | 275001 | 275002 | 275003 | 275004 | 275005 | suma que cruzan | semillas con mayoría | mordidas malas (mediana) | vida (mediana) |
|---|---|---|---|---|---|---|---|---|---|
| MEJOR_A (Sonnet, réplica 1) | 0 (persisten 9) | 0 | 0 | 0 | 0 | 0 | **0/5** | 13 189 | 2 291 |
| MEJOR_B (Sonnet, réplica 2) | 0 | 0 | 0 | 0 | 0 | 0 | **0/5** | 8 745 | 6 746 |
| MEJOR_H (Haiku, control) | 0 | 0 | 0 | 3 | 1 | 4 | **0/5** | 12 | 600 |
| **HUMO** (mejor del 5-oct, fuera de muestra) | **6** | **9** | **7** | **8** | **7** | **37** | **5/5** | 8 890 | 2 417 |
| O1 (a mano, techo) | 3 | 7 | 1 | 6 | 9 | 26 | 3/5 | 3 473 | 3 068 |
| RAIZ (suelo) | 0 | 0 | 0 | 0 | 0 | 0 | 0/5 | 18 | 600 |

Las celdas son los linajes que cruzan (cruza_real, de 9). El R0 real, los que persisten, las muertes y la composición del mundo por corrida
están en `examen/examen.log` y `examen/examen_resumen.json`.

**La letra:**
- V1: O1 con mayoría 3/5 ≥ 3 → sí.
- V2: RAIZ 0/5 → sí.
- V3: 30/30 corridas → sí.
- V4: todos pasan el filtro → sí.
- Ningún programa cumple (≥ 4/5), así que no hay FUNCIONA ni MODESTO (i)–(ii).
- MODESTO (iii) pide que MEJOR_A y MEJOR_B superen a RAIZ en linajes que cruzan en las 5 selladas: los dos empatan con RAIZ en 0.
- → **NO**.

## 2. Búsqueda (30 iteraciones cada una; `corridas/`)
| corrida | modelo | semillas | mejor puntaje | en su semilla de búsqueda (etapa 3) | reloj |
|---|---|---|---|---|---|
| A | Sonnet | 274101–3, rs 43 | 0.424 (iteración 23) | persisten 2/9, cruzan 0/9 | 8 066 s |
| B | Sonnet | 274201–3, rs 44 | 0.300 (iteración 3, sin mejora después) | persisten 0/9, cruzan 0/9 | 5 301 s |
| H | Haiku | 274101–3, rs 43 | 0.643 (iteración 1, sin mejora después) | persisten 4/9 | 6 023 s |
| humo del 5-oct (referencia) | Sonnet | 271001–3, rs 42 | ronda 30: 9/9 | — | — |

Ningún programa de las tres corridas llegó a cruzar en la búsqueda. El humo llegó a 3/9 en la ronda 12 y a 9/9 en la 30.

## 3. Qué escribió cada ganador (código leído; diff contra la raíz en `examen/programas/`)
- **MEJOR_A: limpieza redescubierta, mal calibrada.** Si no tiene comida útil a menos de 25 casillas y sus dos reservas pasan de 0.75,
  va a una letra que ya sabe dañina y la muerde. El piso que la mordida no puede cruzar es rep_umbral + 0.02 si está sobre el umbral, y
  0.4 si no. Su firma: 13 189 mordidas malas, unas 700 veces las de RAIZ. Limpia tanto que, aunque en una semilla persisten 9/9,
  ningún linaje llega a R0 0.9 (0.50–0.76).
- **MEJOR_B: limpieza redescubierta, que impide reproducirse.** `_barato` muerde una letra conocida mala si las dos reservas quedan por
  encima de 0.6 ("sirve para renovar objetos del mundo"), y lo hace siempre que no tiene otro blanco. Así nunca sostiene E y Ag ≥ 1.0
  durante 500 pasos: los cuerpos viven mucho (mediana 6 746) y casi no paren (R0 0.0 en 4 de 5). **No es una trampa del simulador.**
  Explota el puntaje: ver ERR-195.
- **MEJOR_H: ningún mecanismo nuevo.** Sólo cambia tres constantes de la raíz: PRUEBA de 0.5 a 0.65, D0 de 3 a 4 y las urgencias de
  4/2 a 6/3. No limpia (12 mordidas malas, como RAIZ). En su semilla de búsqueda dio 4/9; en las selladas colapsa (hasta 1 200
  extinciones). Es suerte de semilla.
- **HUMO** (del informe del 5-oct): limpieza con piso, que no persigue comida lejana cuando ya está bien. Es la única calibrada.
- **Lectura:** los tres programas de Sonnet (humo, A y B) **escribieron limpieza**; Haiku no la escribió en 30 rondas. Pero sólo 1 de 3
  la dejó calibrada para cruzar. El concepto aparece fácil; la dosis es lo difícil.

## 4. Predicciones (§8) contra el resultado
| # | predicción | p | resultado |
|---|---|---|---|
| Q1 | A cumple | 0.65 | no (0/5) |
| Q2 | B cumple | 0.65 | no (0/5) |
| Q3 | H cumple | 0.30 | no (0/5): acierto |
| Q4 | HUMO cumple fuera de muestra | 0.60 | **sí (5/5)** |
| Q5 | O1 con mayoría en ≥ 4/5 | 0.60 | no (3/5) |
| Q6 | los ganadores de Sonnet que cumplan usan limpieza | 0.80 | vacía: ninguno cumple. Descriptivo: A y B sí escribieron limpieza |
| Q7 | algún mejor de Sonnet suma más que O1 | 0.45 | A y B no (0 contra 26); HUMO sí (37 contra 26) |
| Q8 | gasto en el modelo ≤ 12 USD | 0.75 | sí (6.97 USD) |
| V | serie F / M / NO / NSL = 0.30 / 0.40 / 0.22 / 0.08 | | **NO** |

## 5. Costo real
- **Llamadas al modelo (exacto, `gasto/libro_gasto.jsonl`, 91 llamadas): 6.97 USD.**
  - A: 2.29 USD (30 llamadas, Sonnet).
  - B: 2.66 USD (30, Sonnet).
  - H: 1.97 USD (30, Haiku).
  - Humo de tubería: 0.07 USD.
- **Coordinación de esta sesión: no se puede medir desde dentro.** La consola de uso de la cuenta tiene el número; mi estimación es que
  queda bajo el resto del presupuesto de 30 USD, pero no está verificada.
- **CPU:** 3 corridas en paralelo en 4 núcleos (unas 2.2 h de reloj) y el examen con Pool 3 (unos 35 min).

## 6. Lo no verificado, y la reserva principal
1. **El proponente no es el del humo (ERR-194).** En el humo, Sonnet devolvió de media **15 910 tokens de salida por iteración**
   (`completion` en `consola_err.txt`, que cuenta también el razonamiento). Esta noche devolvió **~1 800** (mediana: A 1 827, B 1 869;
   Haiku 6 791). Es el mismo campo del CLI, porque en los dos casos `input_tokens` vale 2.
   - El modelo razonó unas 9 veces menos por propuesta, aunque el entorno tiene `CLAUDE_EFFORT=high` y `MAX_THINKING_TOKENS=31999`.
   - El adaptador original (b1ae88ae…) no está en el repo, así que no sé con qué banderas corrió el humo.
   - **El NO puede deberse a esto y no a la búsqueda.** Esta serie replica la tubería, no las condiciones del proponente.
2. **El puntaje tiene una meseta explotable (ERR-195).**
   - La puerta de la etapa 2 ("sin extinción tras t = 10 000") la pasa un cuerpo inmortal que no se reproduce.
   - La etapa 3 da un piso de 0.30 a todo lo que llega.
   - B se quedó 27 de 30 rondas en esa meseta (0.30, con R0 0).
3. Una sola corrida por condición: dos réplicas y un control.
4. El examen se corrió en dos tandas, por tiempo de reloj. Las corridas son deterministas por semilla, así que el orden no importa.
5. Sin auditor externo, por presupuesto. Los números de la tabla salen de `examen_resumen.json`, recalculados aparte del runner.

## 7. Qué propongo (no se corrió nada; regla de parada)
- **Para decidir si el NO es de la búsqueda o del proponente:** repetir **sólo A** con el proponente igualado al del humo, con
  preregistro nuevo y semillas nuevas.
  - Igualado quiere decir `--effort max` o el razonamiento forzado. Se verifica en el libro con una salida mediana ≥ 10 000 tokens por
    llamada antes de seguir.
  - Costo estimado: 6–10 USD de modelo.
  - Si cruza, el humo dependía de que el modelo razonara largo; si no, el humo fue suerte de una corrida (1 de 3).
- **El puntaje necesita un arreglo** (ERR-195) antes de cualquier serie nueva: la etapa 2 debe exigir nacimientos reales, no sólo "sin
  extinción". No se cambia aquí: sería recalibrar tras ver datos.
- **HUMO** es el candidato fuerte que deja la noche: 5/5 fuera de muestra, por encima de O1. Un examen más grande (20 semillas) lo
  pondría en serie con letra propia. Es barato, porque no llama al modelo.

## 8. Archivos
`PREREGISTRO_serie.md` (commit `00defd3e`, antes de A, B y H; §9 agregado antes de lanzar) · `evaluador.py`, `corre_carro.py`,
`lanza.py`, `lanza_corrida.sh`, `adaptador_claude.py` (reconstruido), `config_{A,B,H}.yaml` · `cordura/` (anclas, tramposos) ·
`corridas/{A,B,H,HUMO_TUBERIA}` (logs, checkpoints, programas evaluados, `registro_llm`) · `gasto/libro_gasto.jsonl` ·
`examen/` (`programas/`, JSON por corrida, `examen.log`, `examen_resumen.json`) · `corre_examen.py`.
