# PREREGISTRO — frio_carrera: ¿el principio de F1 ("pasar sólo lo que tuvo consecuencia") rompe el muro H-1 de la carrera con el bicho real? (25-sep-2026)

Misión: llegar a la AGI por este camino. Escrito por un creador **antes del humo**; lo integra y lo corre el coordinador. Carpeta:
`experimentos/organelos/frio_carrera/`. Frente 1 (v14.3 en la pista de la carrera). No es candidato a tronco por sí solo.

## 0. Instrumento (sha a 16)
| archivo | sha | origen |
|---|---|---|
| `construye_frio_carrera.py` | e28b509d4a00908a | — |
| `carros/V143_RES0.py` | fab1d8068fe901a5 | por anclas desde `tronco_v14_3/carros_v143/V143.py` (2a03048a7f1525e5) |
| `carros/V143_BAR0.py` | db160ec0685ec7bd | ídem; difiere sólo en la línea de perillas y el nombre |
| `carros/V143_TEL.py` | f73f8ea41399bb79 | ídem; sólo arnés y humo (V143 + telemetría) |
| `corre_frio_carrera.py` | 49de4dd28a8f3c3a | importa sin tocar `tronco_v14_3/corre_v143.py` (24100621c450da22) |
| `identidad_frio_carrera.py` | 9b0a5705b6113b9d | arnés, **58/58** (salida `identidad_frio_carrera_salida.txt`, 5be357b5e7402f9f) |
| pista, juez, O1 (solo se leen) | 9f47c65e438e0ff4 · 6a68f640a7832f12 · 99436afa2715f028 | `carrera_escuderias/` |

## 1. Traducción de F1 a la carrera, y por qué es ésta
- En ECO (F1) el hijo es una instancia nueva: sin la tabla del padre no tiene NADA; FAMB_RES0 le pasa la tabla sin las entradas R = 0.
- En la carrera el carro ES el cerebro del linaje. Lo que hereda el nacido (hijo de la cola) es el **NODO del linaje**: las últimas 20
  mordidas de cada cuerpo muerto, `[patrón, R de la necesidad activa, necesidad]`, que el que nace lee por la vía lenta (hasta 50,
  por sorpresa). Cada letra es neutra en una de las dos necesidades (A y B no tocan el agua; C y D no tocan la energía), así que el
  nodo SÍ tiene neutras: **36.5 %** de las entradas leídas en V143 (arnés (B), s 36901, T 5 000; 61 de 167, y todas se leen porque
  el nodo tiene < 50 entradas).
- **V143_RES0** = V143 + el nacido lee una COPIA del nodo sin las entradas R = 0. El nodo guardado no cambia. Memoria nueva: cero.
  Constantes nuevas: cero. Es la traducción más fiel del principio (RES_SIN0 / ORA_SIN0: filtrar lo neutro de lo que se hereda).
- **V143_BAR0** = RES0 + las R de la copia se permutan entre entradas en cada lectura (patrón y necesidad quedan; multiconjunto
  igual). Permutación con splitmix64 propio sembrado con (índice del linaje, t, k): no consume ningún rng (la regla de la pista prohíbe
  `np.random` en los carros; `revisa_carro` PASA ×3). Control de CONTENIDO que puede ganar.
- **Alcance, dicho antes de correr:** con fundador limpio (ENMIENDA 5) el fundador es una instancia nueva con nodo vacío; el filtro sólo
  toca a los hijos de la cola. En la serie 14301 de V143 murieron ~34 000 fundadores contra ~4 200 hijos.
- **Evidencia previa en contra (exploratoria, no es dato):**
  - nube 24-sep: el "nodo sin neutras" (N0 = esta misma idea) dio 0.509 contra 0.637 de V143, gana 3/6, dif −0.009. La tabla del padre
    sin neutras (la traducción literal del mecanismo de F1) dio −0.19, gana 0/6.
  - `comite/trasplantes/HALLAZGOS.md` (115 corridas): ENSEÑA 1 y 2 (el hijo nace con TODO el cerebro del padre) = 0.61 / 0.68 contra
    0.596. **El hijo de v14.3 no muere de ignorancia.** El muro es establecerse: el fundador limpio muere igual en todos los brazos
    (43–68 pasos, 98–99 % sin parir); establecido, v14.3 da 0.82–0.84 y O1 0.95.
- Por eso lo que sigue es **el nulo con protocolo** de una idea que funcionó en otro mundo, no una apuesta.

## 2. Brazos (monocultivo de 9 carros iguales; pista escalada L 360, 36 objetos, T 100 000, fundador limpio = 1)
| brazo | carro | papel |
|---|---|---|
| `v143` | V143 | base (el candidato v14.3 de 14301/14321) |
| `res0` | V143_RES0 | hipótesis |
| `bar0` | V143_BAR0 | control de contenido que puede ganar |
| `o1` | O1 | techo escrito por un LLM; ancla de la pista |

Entrada (regla 14): cada corrida ES `corre_v143.tarea` (= `juez.tarea(seed, 9 carros, T, 1, 0, 1, None, 1)` + `juez.resumen_linaje`,
sólo física). El arnés (C) lo verifica campo a campo; resumen y pareados son `corre_v143.resume` y `corre_v143.pareado` tal cual.

## 3. Semillas NUEVAS (grep en `*.py` y `*.md` de organelos y bundle el 25-sep: ninguna 36001–36999 usada como semilla)
Serie **36001–36020**; réplica **36021–36040**; práctica **36901–36909** (arnés 36901–36904; humo 36905–36906).

## 4. Medidas
- **Cruza (letra de la carrera, ENMIENDA 5 con la regla de mayoría de `corre_v143`):** un linaje-semilla cruza si `cruza_real`
  (≥ 5 muertes, R0 de nacimientos reales ≥ 0.90 y 0 fundadores tras t 10 000). Una semilla cruza si > 4.5 de sus 9 linajes cruzan.
  El brazo cruza (`gana_e5`) si cruzan ≥ 15/20 semillas.
- **Pareado:** por semilla, mediana del R0 real de los 9 linajes; gana = semillas en que el primero supera al segundo (empate no gana).
- Descriptivo (no puntúa): ESTABLECIMIENTO (linajes con 0 fundadores tras t 10 000) y R0 real de establecidos y no establecidos
  (propuesta del explorador de trasplantes); telemetría del nodo (entradas, neutras, neutras leídas, lecturas de BAR que cambian R);
  cuerpos que leen nodo (nacimientos reales) contra fundadores limpios; causas; vida.

## 5. Nube-9, ERR-115, reanudación
`trabajo()` atrapa TODA excepción (la guardia ERR-60 de la pista es un `SystemExit`) y escribe un JSON marcado `aborto`; ningún trabajador
del Pool muere; **cualquier aborto deja la serie NO SE LEE** (no se imputa nada). Cada corrida escribe su JSON antes de volver; `--reanuda`
salta las hechas. Banderas desconocidas o abreviadas abortan; semillas, T y brazos ajenos se rechazan (arnés (H), 10/10).

## 6. La letra (`corre_frio_carrera.lee_serie`)
**Validez (NO SE LEE si falla alguna):**
- **V1:** 4 brazos × 20 semillas, 0 abortos, contabilidad coherente 180/180 por brazo.
- **V2:** O1 cruza (`gana_e5`).
- **V3:** V143, mediana del R0 real de todos los linajes, en [0.40, 0.80]. Series previas: 0.536 (14301), 0.63 (14321), 0.587 y 0.637
  (nube, 6 + 6) y 0.596 (trasplantes, 10).
- **V4:** instrumento. En RES0, 0 neutras leídas; en BAR0, la permutación cambia alguna R en ≥ 0.50 de las lecturas (última instancia
  de cada linaje).

**Puertas:**
- **P1:** RES0 cruza (`gana_e5`).
- **P2:** RES0 > V143 en ≥ 15/20 semillas pareadas.
- **P3:** BAR0 NO cruza.

**Veredicto de una serie:**
- **FUNCIONA** = P1 + P2 + P3.
- **HAY ALGO MODESTO** = no FUNCIONA, RES0 > V143 en ≥ 15/20 con diferencia mediana ≥ 0.10, y RES0 > BAR0 en ≥ 15/20.
- **NO** = cualquier otro caso.

**Bloque:** serie y réplica con el mismo veredicto; si difieren, vale el menor (`--bloque`).

**Nulos (regla 15):**
| puerta | nulo | umbral | P(pasa ∣ nulo) | potencia |
|---|---|---|---|---|
| P1 | RES0 = V143 (semillas con mayoría: 1/20, 1/20, 0/10 → p ≈ 0.04); nulo duro p = 0.5 | ≥ 15/20 | 1e-17 · 0.021 | 0.989 si p = 0.9 |
| P2 | sin efecto, p = 0.5 por semilla | ≥ 15/20 | 0.021 | 0.93 si p = 0.85; 0.62 si p = 0.75 |
| P3 | el contenido no importa: BAR0 = RES0; si RES0 cruza con p = 0.9 | BAR0 < 15/20 | 0.011 | — |
| M | las dos pareadas con p = 0.5 | ≥ 15/20 ×2 y dif ≥ 0.10 | ≤ 0.021 (correladas) · 4e-4 (independientes) | — |
| V2 | O1 no reproduce: p = 0.85 | ≥ 15/20 | 0.067 | 0.9997 si p = 0.95; 0.989 si p = 0.9 (**18/20** en 14301, ERR-148; 5/5 en trasplantes) |
| V3 | — | [0.40, 0.80] | margen ≥ 0.13 sobre las 5 series previas (0.536–0.637) | — |

## 7. Predicciones firmadas (creador, antes del humo; informadas por §1)
| cantidad | rango | probabilidad |
|---|---|---|
| V143, mediana del R0 real | 0.45–0.75 | V3 con 0.95 |
| O1 cruza | — | V2 con 0.95 |
| fracción de neutras en el nodo leído (telemetría de RES0, antes de filtrar) | 0.25–0.45 | — |
| RES0, mediana del R0 real | 0.40–0.72 | — |
| **RES0 contra V143 (la que puede fallar)** | gana 6–13/20; dif mediana entre −0.12 y +0.06 | P2 con **0.04**; P1 con **0.01** |
| BAR0, mediana del R0 real | 0.20–0.60; V143 > BAR0 en ≥ 12/20 | 0.60 |
| BAR0 cruza | — | 0.005 (P3 pasa con 0.995) |
| establecidos (0 fundadores tras 10 000), V143 y RES0 | 0.45–0.80 de los linajes; R0 del establecido 0.75–0.90 | — |
| veredicto de una serie | FUNCIONA 0.005 · MODESTO 0.03 · NO 0.90 · NO SE LEE 0.065 | — |
| bloque | NO ×2 0.85 · FUNCIONA ×2 0.002 | — |

## 8. Qué refuta
- **"F1 rompe el muro de la carrera":** P1 o P2 caen con validez intacta.
- **"Es el contenido":** P3 cae (la tabla barajada también cruza) → lo que pesa es la dosis de lectura, no lo que dice.
- **"El filtro no hace nada aquí":** RES0 ≈ V143 (|dif| ≤ 0.05, gana 7–13/20) es lo que espero. Si RES0 < V143 en ≥ 15/20, lo neutro
  del nodo AYUDABA en la carrera (lo contrario de H-NEUTRAS en ECO), y lo digo así.

## 9. Trampas (EQUIPO regla 5)
1. **Canal simétrico:** no hay canal; nadie escribe en la pizarra (se reporta 0 escrituras).
2. **Acierto sin balancear:** no hay tasa de acierto; la medida es el R0 real.
3. **Mundo que se come la comida:** ERR-104 vigente (en esta pista morder repone al instante). Es igual en los 4 brazos, y el pareado
   usa la misma semilla del mundo.
4. **Sitios fijos:** los objetos reaparecen al azar; el nodo guarda letras, no sitios. `memoria_rechazo` (por sitio, 20 pasos) es la
   misma en todos los brazos.

## 10. Vocabulario
- Permitido: «linaje», «cuerpo», «el nacido lee el nodo sin lo neutro», «cruza por la letra de la carrera», «establecido».
- Prohibido: «población», «generación», «evoluciona», «aprende de sus ancestros», «cultura».

## 11. Costo, humo y enmiendas (se completa DESPUÉS del humo; §0–§10 son las del sha del runner que registra el log del humo)
- **Arnés antes del humo: 58/58** (56 s, python 3.14.2, numpy 2.4.3). Las dos primeras versiones dieron 56/58 por fallos del CASO, no del
  instrumento: (C2) comparaba también la etiqueta del linaje (`V143_RES0#i` contra `V143#i`, la única diferencia legítima), y (E6) contaba
  la permutación sólo en la última instancia de cada linaje (a T 5 000 no había ninguna lectura con > 1 entrada). Se corrigieron antes del
  humo; runner y carros sin cambios.
- **Humo 14:45** (`--humo`, un proceso, 6 corridas a T 20 000, 140 s en total). sha del preregistro que registra el humo: ddec01d81ab7b140;
  runner 49de4dd28a8f3c3a. Crudos y resumen en `datos/humo/frio_carrera_humo_s36905-36906_T20000_20260925_144540/` (`resumen.json`
  bd73aab86cfa6247). Las 6 corridas escribieron su JSON; contabilidad coherente 54/54; regla 14 OK en el propio humo. **No se lee:**
  - R0 real (mediana de los 18 linajes): V143 0.182 · RES0 0.115 (pierde 0/2, −0.07) · BAR0 0.048 · O1 0.500 (1 semilla).
  - Neutras en el nodo de V143 (TEL): 0.498 de las entradas y 0.475 de las leídas. Nacidos que leen nodo: 88; fundadores limpios con
    nodo vacío: 870.
  - V2 y V3 dan NO SE LEE, como se espera a T 20 000 (los linajes aún no se establecen).
- **Costo, medido en el humo** (un proceso, con 6 procesos del explorador ocupando núcleos): 18 s por corrida de V143, RES0 o BAR0 y 34 s por
  O1, a T 20 000. En la serie 14301 (Pool 6, T 100 000): 137 s por V143 y 270 s por O1. **Por serie: 80 corridas ≈ 13 600 s de CPU, unos
  25–45 min de pared con Pool 6.** Réplica, igual.
- **ERR-148 (tras el humo; sólo texto de §6, ni umbral ni código):** en la fila V2 de la tabla de nulos escribí "19/20 en 14301". El resumen
  de la serie dice que O1 cruzó en 18/20. La potencia de V2 con p = 0.9 es 0.989, y P(cae ∣ p = 0.9) = 0.011. La puerta (O1 `gana_e5`) no
  cambia.
- **Predicción que el humo ya contradice** (no cuenta, pero la declaro): la fracción de neutras en el nodo (0.50 / 0.47) cae por encima de
  mi rango 0.25–0.45. Las predicciones de §7 NO se tocan.
