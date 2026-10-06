# PREREGISTRO — EXPLORATORIO — CONDICIONES / LA MONEDA DEL MURO: ¿la selección conserva la regla de riesgo si el pasaje paga el establecimiento (la mitad de la letra)? (30-sep-2026, creador; enmendado por auditoría antes de datos, sec. 12, ERR-176)

Misión: llegar a la AGI por este camino. **EXPLORATORIO** (5 cadenas por brazo). No decide tronco: decide el siguiente paso.
Escrito con el arnés PASADO (`identidad_mm_salida.txt`) y **antes** del humo y de cualquier número de este experimento.
Carpeta: `experimentos/organelos/condiciones/moneda_muro/` (sólo archivos nuevos). `condiciones/mutacion/corre_mut.py` (sha `8912e9d77f397e40`)
se IMPORTA y no se toca; por su `verifica` van fijados corre_moneda, sentidos_muro, corre_bp, V143_BQ3, pista y juez.
ERR libres de la sesión: 176–179. **ERR-176** = CONSERVA pasa de 4/5 a 5/5 por auditoría, antes de datos (sec. 12).

## 1. Hipótesis (director, 30-sep noche)
En `condiciones/mutacion` (tasas ÷10) la selección por pasajes **purga** la regla de riesgo de forzada3 (`[10,0,1,0.5,0,−3]`): 0.26 contra
0.64 de la neutra, aunque la cadena sembrada con ella cruza 24/45 a 100k. La siembra vieja toma los bancos finales de los 9 linajes de un
pasaje de 25k: premia sobrevivir al muestreo. La letra (`cruza_real`) pide establecerse (R0 real ≥ 0.9 y 0 fundadores tras 10k en 100k).
**Si la transferencia paga el establecimiento (0 fundadores tras 10k), que es la mitad de la letra, la selección CONSERVA o SUBE la regla
y la cadena cruza más.** Esta moneda **no paga R0 real ≥ 0.9** (H-1): la otra mitad de la letra queda fuera del pasaje.

## 2. Diseño: la cadena de `mutacion`, con un solo cambio (la transferencia)
**Elegida la opción (a)** del encargo: pasajes de **T 100 000** y siembra del pasaje siguiente = unión de los bancos finales **sólo de los
linajes establecidos** (0 fundadores después de t = 10 000). "Establecido" se cuenta con los instantes de fundación del propio linaje
(`telem.t_fund` y `fundadores`, física de la pista); no se lee R0, ni `cruza_real`, ni ningún veredicto del juez.
**Por qué no (b):** el banco del carro **ya es** (b). Cada parto mete la lista del padre en el banco del linaje (FIFO de 50), así que la
siembra vieja ya está ponderada por partos. (b) no cambiaría la moneda; (a) sí, y no toca el carro. **Memoria nueva: cero. Mecanismo
nuevo en el organismo: ninguno.** El cambio vive en el runner (`corre_mm.siembra_L`).
**Respaldo declarado:** si en un pasaje ningún linaje se establece, dan siembra los de menos fundadores tras 10k. Se cuenta y entra en la validez.

| brazo | siembra del pasaje 0 | moneda de la transferencia | papel |
|---|---|---|---|
| **moneda_L** | 225 × [A] + 225 × [B], A = `[10,0,1,0.5,0,−3]` | nueva (establecidos, 100k) | CANDIDATO; prueba a 100k |
| **neutra_L** | 225 × [A0] + 225 × [B], A0 = la misma fila con w 0 | nueva | CONTROL que puede fallar: deriva y arrastre del pasaje nuevo; prueba a 100k |
| **moneda_25 / neutra_25** | las mismas | vieja (9 bancos, 10 × 25k) | **GUARDADOS** de `condiciones/mutacion` (commit ff09fac3; sha16 fijado). No se recorren |

Tasas: **CFG10** (inicial 2, p_campo 0.01, p_dup 0.002, p_del 0.007, p_ins 0.005, banco 50), las de mutacion.
**Pasajes: 6 de 100k por cadena** (no 10): reducción **declarada** por el costo (sec. 9). Son 600k pasos de selección por cadena, contra 250k en mutacion.
**moneda_25 se reusa, no se corre:** el instrumento es el mismo (arnés F: con la moneda vieja este runner reproduce bit a bit dos pasajes
guardados de mutacion). Sus semillas de pasaje (6341xx) son otras que las de aquí, así que **no está pareada**; por eso no entra en la letra.

**Medida:** fracción de listas de la siembra que sale de cada pasaje con una regla de clase A (sentido 10, j 0, `>`, boca; cualquier θ y w):
la de moneda y mutacion, sin cambios. **Final** = la siembra que sale del pasaje 5 (la que entra a la prueba).
**Prueba final (descriptiva):** T 100 000, semillas **59201–59205** (no son nuevas, a propósito: pareadas con moneda_25 24/45, forzada3 23/45,
bq3_pas 13/45 guardados), en los dos brazos. Además cada pasaje de 100k da su propia cuenta de `cruza_real` (descriptivo).
**Semillas NUEVAS** (grep 30-sep 22:35: `638xxx` no aparece en .py ni .md de PROYECTOS/JUACO; en .txt sólo como cifras de floats de logs):
pasaje p del índice i (1..5) = **638100 + 10 i + p** (638110–638155), las mismas en los dos brazos (pareado). Humo: 638180–638181 y prueba 638191. Arnés: 638193.

## 3. Instrumento y anclas (arnés `identidad_mm.py`; salida entera en `identidad_mm_salida.txt`: **ARNES: PASA**)
- (K) shas de corre_mut e identidad_mut, y por la cascada de `verifica`: corre_moneda, sentidos_muro, corre_bp, V143_BQ3, pista, juez, carros.
- (C) CFG10, filas A / A0 / B y siembra inicial = las de mutacion; T_EST = `juez.T_CORTE` = 10 000.
- (E) Regla 14: la entrada es `corre_mut.tarea` = `corre_bp.tarea('V143_BQ3', CFG10, siembra)`, campo a campo. La siembra actúa (todo fundador sale del banco sembrado).
- (F) **Con la moneda vieja este runner ES corre_mut bit a bit:** `trabajo` (cadena de 2 pasajes y prueba) JSON por JSON; y reproducción de los
  pasajes guardados `moneda i1 p0` y `p1` de mutacion (s 634110 y 634111, T 25 000), encadenados con la siembra que sale de este runner.
- (J) "Establecido" con datos del linaje coincide con el `fund_post10k` del juez en los 495 linajes de los 55 JSON guardados de mutacion.
- (A) **La moneda nueva actúa:** sobre los 55 JSON guardados la siembra nueva difiere de la vieja en 55/55, es subconjunto no vacío y sólo
  sale de linajes establecidos. Casos sintéticos: establecidos, respaldo por mínimo, banco vacío, siembra vacía, `t_fund` truncado.
- (D) determinismo. (W) reintento de abortos y reanudación de una cadena; `carga()` de la carpeta. (X) el runner niega pool > 2 y pool en el humo.
- (L) la letra en 18 casos (ERR-176: 5/5). (R) sha16 de la lectura y de las 5 pruebas de mutacion.

## 4. Mini-prueba ANTES de firmar (sin corridas: sobre los JSON GUARDADOS de mutacion; vista y declarada)
La moneda nueva aplicada a datos que ya existían (no son datos de este experimento):
- **5 pruebas a 100k de moneda ÷10** (siembra de entrada ya purgada, 0.22–0.35): establecidos 7, 7, 6, 5, 5 de 9. Los linajes
  establecidos son casi clones (fracción A del banco 0 o 1). Fracción A: entra 0.279 (media) → moneda vieja 0.148 → **moneda nueva 0.158**.
  De 30 linajes establecidos, 5 son de tipo A (0.17, contra 0.28 de entrada). **La moneda nueva no la sube en estos datos.**
- **50 pasajes de 25k del brazo moneda:** por tipo de linaje (clase de las listas que entraron por parto), se establecen A 98/107 = 0.92,
  B 203/281 = 0.72. Pero hay 107 linajes A contra 281 B: **la regla pierde antes, al fundar** (cada linaje vuelve a sacar del banco hasta
  que un fundador prende, y prende más a menudo uno B). Cambio medio por pasaje con la moneda nueva −0.020, con la vieja −0.022.
- **50 pasajes de 25k del brazo neutra:** A 203/227 = 0.89, B 119/138 = 0.86; cambio medio +0.023 (nueva), +0.016 (vieja).

**Lo que eso me dice (y lo declaro):** el filtro "establecido" casi no filtra (5–7 de 9 pasan) y los linajes establecidos son clones de un
fundador, así que cada pasaje es un sorteo de ~6 fundadores: **deriva fuerte** (muchas cadenas van a 0 o a 1) y la selección que queda es
la del fundador, que en lo guardado va **contra** la regla. Espero que la hipótesis del encargo **no** se cumpla.

## 5. Nulo por puerta y potencia (reescrita por ERR-176; `sim_mm.py`: deriva, 6 pasajes, 5 a 7 fundadores clones por pasaje, 20 000 réplicas)
| razón de ventaja de A por pasaje | CONSERVA (5/5) | PURGA | INDETERMINADO | CONSERVA con la letra vieja (4/5) |
|---|---|---|---|---|
| 0.5 (como en las pruebas guardadas) | 0.00 | 0.47 | 0.53 | 0.00 |
| 0.7 | 0.00 | 0.26 | 0.74 | 0.02 |
| **1.0 (nula: moneda_L ≡ neutra_L)** | **0.07** | **0.03** | 0.90 | 0.28 |
| 1.5 | 0.44 | 0.00 | 0.56 | 0.83 |
| 2.0 | 0.78 | 0.00 | 0.22 | 0.98 |
| 3.0 | 0.97 | 0.00 | 0.03 | 1.00 |

- **CONSERVA (5/5) tiene un falso positivo de ~0.07 bajo la nula** (con 4/5 era ~0.28: por eso ERR-176, regla 15). El precio es potencia:
  una ventaja de 1.5× por pasaje sólo da CONSERVA 0.44. Aun con 5/5, CONSERVA es **señal para replicar**, no hallazgo.
- **PURGA casi no sale por azar (~0.03)**, pero tiene poca potencia (~0.5 con una desventaja de 2×): una neutra que se pierde (0) no cuenta.
- La simulación supone clones perfectos y una neutra sin sesgo. **neutra_L no es un nulo puro** (sec. 6, H-3), así que estas tasas son aproximadas.
- Puertas de validez bajo la nula: `moneda_actua` se cumple casi seguro (55/55 en lo guardado); `respaldo_raro` falla sólo si en más del 25 %
  de los pasajes no se establece nadie (en lo guardado a 100k: 0/5 pasajes); riesgo de NO SE LEE ≈ 3 % (casi todo por abortos o apagado).

## 6. LA LETRA (reescrita por ERR-176; por código: `corre_mm.letra`; el arnés la prueba en 18 casos). Final = fracción A de la siembra que sale del pasaje 5.
- **CONSERVA:** moneda_L **≥** neutra_L, pareado por cadena, en **5/5**, **y** la mediana de moneda_L **≥ 0.40**. (Antes de la auditoría: ≥ 4/5.)
- **PURGA:** moneda_L **≤ 0.5 × neutra_L**, pareado, en **≥ 4/5**. Precisión (antes de datos): una cadena con neutra_L = 0 **no cuenta** para PURGA (0 ≤ 0.5 × 0 es vacío).
- **INDETERMINADO:** cualquier otro resultado válido.
- **Validez** (si una falla: NO SE LEE): 0 abortos; 10 cadenas y 10 pruebas completas; entrada 0.5 en todas; **moneda_actua** (en ≥ 1 pasaje
  la siembra nueva difiere de la que daría la vieja sobre el mismo pasaje); **respaldo_raro** (respaldo en ≤ 25 % de los pasajes);
  referencias de mutacion con su sha16; arnés PASA con los shas actuales.
- **Qué paga esta moneda (H-1):** el **establecimiento** (0 fundadores tras 10k), que es la mitad de la letra `cruza_real`. **No paga R0 real ≥ 0.9.**
  Un resultado aquí habla de esa mitad, no de "la moneda de la letra" entera.
- **neutra_L no es un nulo puro (H-3):** A0 lleva la etiqueta j 0 y B la j 5; las dos tienen w 0. El control aísla **sólo w** (−3 contra 0).
  Si la etiqueta o la deriva mueven a la neutra (en mutacion la neutra subió a 0.64 en 5/5), eso entra igual en los dos brazos, pero la
  neutra no vale como "0.5 esperado".
- **Descriptivos (no entran en la letra):** cruzan de la prueba de moneda_L contra moneda_25 (24), forzada3 (23), bq3_pas (13) y contra neutra_L;
  cruzan por pasaje; cadenas fijadas (≥ 0.95) y perdidas (≤ 0.05) por brazo; cambio medio por pasaje; la **sombra** (lo que daría la moneda
  vieja sobre el mismo pasaje); fracción A por linaje elegido; intacta, arrastre, partos; los finales guardados de moneda_25 y neutra_25.
- **Descriptivo nuevo (auditoría; `analiza_mm_estab.py`, escrito antes de los datos de la serie):** tasa de establecimiento de los linajes de
  tipo A contra los de tipo B, **agrupada sobre los 60 pasajes** (30 por brazo), y cuántos linajes de cada tipo hay contra la fracción A que
  entra. Tipo = clase de las listas del banco que entraron por parto (A ≥ 0.90, B ≤ 0.10, mixto, sin parto). Escribe `estab_mm.json`. No toca la letra.

## 7. Predicciones (firmadas antes del humo; `lee()` las imprime contra lo medido)
| # | predicción | p |
|---|---|---|
| Q1 | veredicto CONSERVA (la hipótesis del encargo) | 0.10 (era 0.20 con 4/5; ERR-176) |
| Q2 | veredicto INDETERMINADO | 0.65 (era 0.55 con 4/5; ERR-176) |
| Q3 | veredicto PURGA | 0.22 |
| Q4 | moneda_L: mediana de la fracción A final ≤ 0.20 | 0.55 |
| Q5 | deriva: ≥ 6 de las 10 cadenas terminan fijadas (≥ 0.95) o perdidas (≤ 0.05) | 0.55 |
| Q6 | elegidos por pasaje (mediana, los dos brazos) en [5, 7] | 0.75 |
| Q7 | prueba de moneda_L: suma de cruzan (de 45) en [15, 27] | 0.60 |
| Q8 | la prueba de moneda_L cruza más que moneda_25 guardada (≥ 25 de 45) | 0.30 |
| Q9 | cruzan por pasaje (media de 9): moneda_L > neutra_L | 0.50 |
| Q10 | cambio medio de la fracción A por pasaje: moneda_L < neutra_L | 0.70 |

Veredicto que espero (con la letra 5/5): **INDETERMINADO 0.65 · PURGA 0.22 · CONSERVA 0.10 · NO SE LEE 0.03.** Con la letra vieja (4/5) había
firmado 0.55 / 0.22 / 0.20 / 0.03. **Las predicciones no son ciegas:** la mini-prueba de la sec. 4 se hizo sobre datos ya vistos de mutacion y
sesgó sobre todo Q4 y Q10 (y la dirección de Q1 a Q3). Valen como apuesta informada, no como pronóstico independiente.

## 8. Control que puede fallar, qué decide y qué lo refuta
- **Control:** neutra_L. Mismas semillas, tasas, largo y moneda; sólo cambia w (0 contra −3). Si moneda_L sube y neutra_L también, no hay pago.
- **CONSERVA** → señal: réplica en semillas nuevas con más cadenas antes de decir "era la moneda". Con `moneda_L_fijadas` 5/5 y neutra_L
  repartida, la señal es fuerte; con 3/5 fijadas y neutras perdidas, es deriva probable.
- **PURGA** → la hipótesis del encargo queda **refutada con esta moneda**: aun pagando establecimiento a 100k, la selección saca la regla.
  El muro no es la ventana del pasaje; es la competencia entre fundadores dentro del banco mezclado. Siguiente: medir la toma del
  fundador por tipo (telemetría nueva) o sembrar linajes puros.
- **INDETERMINADO** → con 5 cadenas y esta deriva no se ve. No se escribe "la hipótesis cae". Q10 y los descriptivos dicen hacia dónde;
  siguiente: bajar la deriva (más linajes por pasaje o más cadenas) antes de repetir.
- Un **3/5** en cualquiera de las dos cuentas (±1 del umbral) dispara réplica (regla 12) antes de cualquier lectura.

## 9. Cuatro trampas
1. **Canal simétrico:** A y B tienen el mismo largo y el mismo consumo de rng; moneda_L y neutra_L comparten tasas, semillas y moneda; la
   etiqueta j es muda (heredado de moneda; la entrada es la misma, arnés E y F). El filtro "establecido" no mira la clase de la lista.
2. **Acierto sin balancear:** todo parte de 0.5 exacto y se lee pareado contra la neutra. Las tasas nulas de CONSERVA (0.28) y PURGA (0.03) están declaradas.
3. **Mundo que se come la comida:** A y B conviven en la misma pista; la aptitud depende de la frecuencia (régimen de mezcla, como en moneda).
   La prueba final de moneda_L no es forzada3: lleva lo que la cadena dejó.
4. **Sitios fijos:** letras con significado fijo. Pasajes en semillas nuevas (6381xx). La prueba reusa 592xx a propósito, sólo como descriptivo.

## 10. Costo y comando
- Humo, un proceso: 6 corridas y 160 000 pasos (2 pasajes de 30k y prueba de 20k por brazo).
- Explora: 60 pasajes y 10 pruebas de 100k = **7.0 M pasos**. mutacion (4.25 M, pool 2) tardó 41 min: **≈ 68 min** sin carga; con las series
  de escalera corriendo a la vez, hasta ~1 h 45 min. Dentro del objetivo de 2 h.
- Comando (lo lanza el coordinador, desde la raíz del worktree `organelos`):
  `python experimentos/organelos/condiciones/moneda_muro/corre_mm.py --explora --pool 2`
- Si se corta: el mismo comando con `--reanuda` (sigue la última carpeta `explora_*`, reintenta los abortos y no recorre los buenos).
- Lectura: `--lee datos/explora_<fecha>`.

## 11. Humo (un proceso; semillas 638180–638181 y prueba 638191; corrido DESPUÉS de firmar las secciones 1–10; no cuenta)
Hubo 6 corridas y 160 000 pasos en 166 s (1.04 ms por paso, un proceso). Carpeta `datos/humo_20260930_223412`. `main()` de punta a punta:
verifica, 2 cadenas, 2 pruebas, `lee()` y `lectura_mm.json` escrito. Arnés PASA con los shas actuales (runner `92285ca8a396c94a`).

| brazo | fracción A: entrada → p0 → p1 | sombra (moneda vieja) | elegidos | respaldo | arrastre ≥ | cruzan en el pasaje | prueba 20k |
|---|---|---|---|---|---|---|---|
| moneda_L | 0.50 → 0.437 → 0.351 | 0.464, 0.382 | 6, 7 | 0, 0 | 0.60, 0.66 | 1, 1 | 0/9 |
| neutra_L | 0.50 → 0.551 → 0.477 | 0.536, 0.489 | 7, 7 | 0, 0 | 0.57, 0.49 | 1, 2 | 0/9 |

Validez del humo: todas las puertas pasan; la moneda difiere de la vieja en 4/4 pasajes. Veredicto del humo: INDETERMINADO (1 cadena; no cuenta).
Lo que enseña y declaro: **a 30k los linajes establecidos todavía no son clones** (fracción A por linaje 0.22–0.80, arrastre ~0.6), porque
con ~20 partos por linaje el banco aún lleva listas de la siembra. A 100k (≥ 50 partos por linaje establecido en lo guardado) el banco se
renueva entero; el humo no prueba ese régimen. **No cambio la letra, el diseño ni las predicciones.** Costo medido: 7.0 M pasos ≈ 61 min con pool 2 sin carga.

## 12. Cambios por auditoría antes de datos (30-sep) — ERR-176
Auditor: LISTO CON CAMBIOS. **Ningún dato del explora existía** (`datos/` sólo tenía `humo_20260930_223412`). El humo no se repitió.
- **ERR-176 (regla 15):** CONSERVA pasa a exigir **5/5** (`CONSERVA_N = 5` en `corre_mm.py`). Con 4/5 el falso positivo bajo la nula era ~0.28;
  con 5/5 es ~0.07. Se cambió la letra en el runner, los casos de la letra del arnés (18 casos; dos nuevos comprueban que 4/5 ya no es
  CONSERVA) y las secs. 5 y 6. PURGA y la validez no cambian. Arnés re-corrido: **ARNES: PASA · 76 s** (30-sep 22:41).
- **Probabilidades de veredicto re-firmadas** por el cambio de letra: Q1 0.20 → 0.10, Q2 0.55 → 0.65. Q3 a Q10 no cambian.
- **H-1:** "paga la moneda de la letra" pasa a "paga el establecimiento (0 fundadores tras 10k), que es la mitad de la letra; no paga R0 real ≥ 0.9"
  (título, sec. 1, sec. 6 y cabecera del runner).
- **H-2:** los scripts de la simulación del nulo y de la mini-prueba quedan en la carpeta: `sim_mm.py` (sha16 `ae805f42e2e6f26c`; ahora imprime
  4/5 y 5/5 con las mismas réplicas, semilla 1) y `mini_mm.py` (sha16 `7b77f99dfe2c54a9`; el que produjo la sec. 4, sin cambios; se corre desde la raíz del worktree).
- **H-3:** se declara que neutra_L no es un nulo puro (A0 usa j 0 y B usa j 5: aísla sólo w) y que las predicciones no son ciegas (secs. 5, 6 y 7).
- **Descriptivo nuevo:** `analiza_mm_estab.py` (sha16 `484404292f6c18d2`), escrito antes de los datos de la serie; anotado en la sec. 6. Se probó
  sólo sobre la carpeta del humo (datos ya vistos; dejó allí `estab_mm.json`). No entra en la letra.
- **Shas finales:** `corre_mm.py d45a5ed42e8514df` · `identidad_mm.py e9e3a7a5b6576f30` (los que cita `identidad_mm_salida.txt`). El humo de la
  sec. 11 corrió con el runner anterior (`92285ca8a396c94a`); la diferencia es `CONSERVA_N`, dos probabilidades de `predicciones` y una línea de la cabecera.
