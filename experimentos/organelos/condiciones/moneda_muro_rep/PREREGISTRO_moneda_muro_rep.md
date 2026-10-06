# PREREGISTRO — RÉPLICA — CONDICIONES / LA MONEDA DEL MURO: ¿la selección conserva la regla de riesgo si el pasaje paga el establecimiento, y conservarla ayuda a cruzar? (1-oct-2026, creador)

Misión: llegar a la AGI por este camino. **RÉPLICA** del explora `condiciones/moneda_muro` (commit 857bbb87: CONSERVA en el umbral).
Escrito con el arnés PASADO (`identidad_mmr_salida.txt`) y **antes** del humo y de cualquier número de esta réplica (secs. 1–10; la 11 se
agrega después del humo). Carpeta: `experimentos/organelos/condiciones/moneda_muro_rep/` (sólo archivos nuevos). No decide tronco.
`condiciones/moneda_muro/corre_mm.py` (sha `d45a5ed42e8514df`) se IMPORTA y no se toca; por su `verifica` van fijados corre_mut,
corre_moneda, sentidos_muro, corre_bp, V143_BQ3, pista y juez. ERR libres de la sesión: 177–179 (ninguno usado aquí).

## 1. Qué se replica y por qué
El explora dio, en la fracción final de la regla de riesgo (clase A), moneda_L 0.8, 0.5, 0.996, 0.0, 0.8 contra neutra_L 0.14, 0.33, 0.05,
0.0, 0.15. La letra pedía moneda_L ≥ neutra_L en 5/5 y una cadena fue empate 0.0 = 0.0 (estricto: 4/5). Además, la cadena que conserva la
regla **no** cruzó más en la prueba final: 17/45 contra 23/45 de neutra_L (descriptivo allí).
**Hipótesis 1 (la del explora):** si la transferencia paga el establecimiento (0 fundadores tras 10k; la mitad de la letra `cruza_real`),
la selección conserva la regla de riesgo: moneda_L termina por encima de neutra_L.
**Hipótesis 2 (la del director, ahora preregistrada):** la cadena que conserva la regla cruza más en la prueba final que la neutra.
En el explora la 2 no se cumplió; aquí queda con letra propia.

## 2. Diseño: el del explora, sin cambios de instrumento
Memoria nueva: cero. Mecanismo nuevo en el organismo: ninguno. Cada cadena es `corre_mm.trabajo` (el del explora): 6 pasajes de T 100 000,
siembra del pasaje siguiente = unión de los bancos finales sólo de los linajes establecidos (respaldo declarado: los de menos fundadores
tras 10k), tasas CFG10, siembra inicial 225 × [A] + 225 × [B], y una prueba final de T 100 000 con la siembra que deja la cadena.

| brazo | siembra del pasaje 0 | papel |
|---|---|---|
| **moneda_L** | 225 × [A] + 225 × [B], A = `[10,0,1,0.5,0,−3]` | CANDIDATO |
| **neutra_L** | 225 × [A0] + 225 × [B], A0 = la misma fila con w 0 | CONTROL que puede fallar (deriva y arrastre del pasaje) |

**Lo que cambia contra el explora (y sólo esto):**
1. **n = 10 cadenas por brazo** (índices 1 a 10), para tener potencia.
2. **Semillas nuevas.** Pasaje p del índice i: **647100 + 10 i + p** (647110–647205), las mismas en los dos brazos (pareado).
3. **La prueba final usa semillas nuevas, 647300 + i (647301–647310), la misma en los dos brazos.** En el explora la prueba reusaba 59201–59205
   para parearse con guardados viejos; aquí el cruce es co-principal y se parea moneda_L contra neutra_L, así que las semillas deben ser nuevas.
   Consecuencia declarada: las sumas de cruce de la réplica **no** se comparan número a número con moneda_25 (24), forzada3 (23) ni bq3_pas (13).
4. La letra (sec. 5): dos lecturas declaradas, una decide; el cruce pasa a co-principal.

Humo: índice 14 (pasajes 647240–647241, prueba 647390). Arnés: índice 15 (647250, prueba 647395) y la semilla vieja 638110.
**Grep de colisiones (1-oct):** `\b647[123]\d\d\b` no aparece en ningún `.py` ni `.md` de `PROYECTOS/JUACO` (todos los worktrees). El arnés (C)
comprueba que las 76 semillas son distintas entre sí y de las 39 del explora.

## 3. Instrumento y anclas (arnés `identidad_mmr.py`; salida entera en `identidad_mmr_salida.txt`: **ARNES: PASA**, 6 corridas, 105 000 pasos)
- (K) shas de `corre_mm.py`, `identidad_mm.py`, `sim_mm.py`, y la cascada de `verifica` hasta pista, juez y carros.
- (C) el modo de la serie es el `explora` de corre_mm salvo índices y bases de semilla; semillas sin choques; constantes de la letra.
- (F) **Identidad con moneda_muro a las semillas viejas, bit a bit:** `trabajo('moneda_L', i1)` de este runner reproduce el pasaje guardado
  `pasaje_moneda_L_i1_p0.json` (s 638110, T 100 000) en sus 18 campos (todos menos los dos de tiempo). Y las 10 cadenas guardadas del explora,
  pasadas por `trabajo()` de este runner en modo `explora`, no recorren nada, dejan los 70 JSON intactos y devuelven las fracciones y cruces
  de `lectura_mm.json` (finales, ≥ 5/5, > 4/5, cruce 17 contra 23).
- (E) regla 14: una cadena corta en semillas del arnés por este runner es igual, JSON por JSON, a `corre_mm.trabajo`; el cfg del carro es CFG10.
  Un aborto simulado en la prueba se reintenta y sale idéntico.
- (X) el runner niega pool > 2, pool o reanuda en el humo, y `--lee` de una carpeta inexistente.
- (G) candados de `--serie` en 10 casos (veredicto previo, carpeta previa, reanuda sin carpeta, git) y `git_limpio` real.
- (L) la letra en 26 casos (9 de fracción, 2 que separan las lecturas, 6 de cruce, 9 de NO SE LEE). (B) bloque y predicciones en seis desenlaces (sin "×2"; umbral en el titular).

## 4. Nulo por puerta y potencia (`sim_mmr.py`; importa el `chain()` de `sim_mm.py` sin tocarlo; 20 000 réplicas, semilla 2)
**Fracción A final, n = 10 por brazo.** OR = razón de ventaja de A por pasaje (neutra con OR 1).

| OR | (a10) ≥ en 10/10 | (a5) ≥ en 5/5, 5 primeras | **(b7) > en ≥ 7/10** | (b8) > en ≥ 8/10 | PURGA ≥ 8/10 |
|---|---|---|---|---|---|
| 0.5 | 0.000 | 0.000 | 0.000 | 0.000 | 0.308 |
| 0.7 | 0.000 | 0.003 | 0.000 | 0.000 | 0.103 |
| **1.0 (nula)** | **0.006** | **0.067** | **0.059** | 0.013 | 0.003 |
| 1.5 | 0.196 | 0.442 | 0.441 | 0.206 | 0.000 |
| 2.0 | 0.601 | 0.777 | 0.609 | 0.346 | 0.000 |
| 3.0 | 0.936 | 0.969 | 0.659 | 0.393 | 0.000 |

Todas las lecturas llevan además "mediana de moneda_L ≥ 0.40". Empates esperados bajo la nula: 1.9 de 10.

**Cuál decide: la estricta (b), con corte 7/10.** Razones, antes de datos:
- Tiene el **mismo tamaño** que la letra del explora: falso positivo 0.059 contra 0.068 de "≥ en 5/5". Es la misma exigencia, con los empates en
  contra y usando las 10 cadenas. Responde la objeción exacta del explora (el 0.0 = 0.0 ya no suma).
- (a10) tiene falso positivo 0.006 pero **muere con una sola cadena perdida**: en el explora moneda_L perdió la regla en 1 de 5 cadenas y sólo
  pasó por el empate. Con una tasa así, 10/10 falla en la mayoría de las series aunque el efecto sea real (potencia 0.20 con OR 1.5).
- (a5) tira la mitad de los datos y deja intacta la objeción del empate.
- **Debilidad declarada de (b7):** si el efecto es muy fuerte y la neutra también se fija arriba, los empates 1 = 1 cuentan en contra y la
  potencia se estanca (~0.66 con OR 3). En el explora la neutra bajó (0.13 de media), así que no espero ese techo. `lee()` cuenta los
  empates arriba (los dos brazos ≥ 0.95); si son ellos los que impiden el 7/10, se declara y no se reinterpreta.
- (a10), (a5) y (b8) **se reportan y no deciden**. (b8) es la marca de "fuera del umbral".
- El modelo supone clones perfectos y una neutra sin sesgo. **neutra_L no es un nulo puro** (H-3 del explora: aísla sólo w; en mutacion subió a
  0.64 y en el explora bajó a 0.13). Las tasas son aproximadas.

**H-1 (auditoría, antes del commit): el 0.059 supone una neutra sin sesgo.** Si la neutra baja sola y la moneda no tiene ninguna ventaja
(moneda OR 1), CONSERVA sale mucho más (`sim_mmr.py`, 20 000 réplicas; el auditor midió 0.36 y 0.52 con 4 000):

| neutra (moneda OR 1) | (a10) | (a5) | **(b7) decide** | (b8) |
|---|---|---|---|---|
| OR 1.0 | 0.005 | 0.065 | 0.059 | 0.014 |
| OR 0.7 | 0.115 | 0.292 | **0.361** | 0.166 |
| OR 0.5 | 0.419 | 0.515 | **0.523** | 0.316 |

Por eso **CONSERVA significa "moneda_L supera a neutra_L y no cae", NO "la selección conserva la regla".** La mediana ≥ 0.40 sólo mide que
moneda_L no cayó. En el explora la neutra bajó a 0.13: ese sesgo, si es propio de la neutra, basta para dar CONSERVA sin que la moneda pague
nada. `lee()` imprime un descriptivo que no decide para separar "moneda sube" de "neutra baja": la mediana final de neutra_L y cuántas
cadenas de cada brazo terminan por encima de su 0.50 inicial.

**Cruce en la prueba final, 10 parejas.** Nulo: las dos cadenas de una pareja cruzan Binomial(9, q) con la misma q ~ U(0.25, 0.65). Las 10
pruebas del explora tienen varianza 1.56 contra 2.2 binomial: no se ve sobredispersión. d = diferencia de q a favor de moneda_L.

| d | CRUZA MÁS (gana ≥ 7/10 y D ≥ +9) | CRUZA MENOS (pierde ≥ 7/10 y D ≤ −9) |
|---|---|---|
| −0.13 (el tamaño del explora: −6 de 45) | 0.000 | 0.448 |
| **0 (nula)** | **0.040** | **0.042** |
| +0.10 | 0.308 | 0.001 |
| +0.20 | 0.754 | 0.000 |
| +0.30 | 0.973 | 0.000 |

Declarado: **la potencia para confirmar "cruza menos" al tamaño del explora es sólo 0.45.** Un SIN DIFERENCIA no prueba igualdad; dice que a
este n no se ve. Para la hipótesis del director (cruza más) la prueba detecta +0.20 (1.8 linajes de 9) con 0.75.

## 5. LA LETRA (por código: `corre_mmr.letra`). Final = fracción A de la siembra que sale del pasaje 5. Pareado por índice.
**La letra no es ciega (H-2):** los cortes (7/10, mediana 0.40, D ≥ 9, 7/10 de cruce) se eligieron con los datos del explora a la vista.
**Medida principal 1, la fracción (decide la lectura estricta):**
- **CONSERVA:** moneda_L **>** neutra_L en **≥ 7/10** (los empates cuentan en contra) **y** mediana de moneda_L (10 cadenas) **≥ 0.40**.
- **PURGA:** moneda_L ≤ 0.5 × neutra_L en **≥ 8/10** (4/5 escalado). Una cadena con neutra_L = 0 no cuenta.
- **INDETERMINADO:** cualquier otro resultado válido.
- **En el umbral** (regla 12): > en 6 o 7 de 10; o ≤ mitad en 7 u 8; o CONSERVA con mediana entre 0.35 y 0.45.
- Lecturas declaradas que **no deciden** y se imprimen: original escalada (≥ en 10/10), original sobre las 5 primeras (≥ en 5/5), estricta ≥ 8/10.

**Medida principal 2, el cruce en la prueba final** (`cruza_real` del juez, de 9 linajes; moneda_L contra neutra_L, misma semilla):
- **CRUZA MÁS:** moneda_L cruza estrictamente más en **≥ 7/10** parejas **y** la suma de diferencias D **≥ +9** (de 90).
- **CRUZA MENOS:** lo simétrico (pierde en ≥ 7/10 y D ≤ −9).
- **SIN DIFERENCIA:** lo demás. En el umbral: gana (o pierde) en 6 o 7 con D del mismo signo.

**Limitación declarada (H-4):** la puerta `moneda_actua` es casi decorativa: se cumple con que la siembra nueva difiera de la vieja en un solo
pasaje de 120, y en el explora difirió en 57 de 60. No se cambia; no protege de nada probable.
**Validez** (si una falla, las dos medidas son NO SE LEE): 0 abortos; 20 cadenas y 20 pruebas completas; entrada 0.5 en todas; `moneda_actua`
(la siembra nueva difiere de la vieja en ≥ 1 pasaje); `respaldo_raro` (≤ 25 % de los pasajes); prueba pareada (misma semilla en los dos brazos);
`lectura_mm.json` del explora con su sha16; arnés PASA con los shas actuales.
**Qué paga esta moneda (H-1 del explora):** el establecimiento, la mitad de `cruza_real`. No paga R0 real ≥ 0.9.

## 6. Bloque contra el explora y qué decide cada desenlace (`corre_mmr.bloque`)
| fracción | cruce | titular |
|---|---|---|
| CONSERVA | CRUZA MÁS | FUNCIONA: moneda_L supera a neutra_L y no cae, y cruza más; **cruce sin réplica: no es declaración** |
| CONSERVA | SIN DIFERENCIA o CRUZA MENOS | HAY ALGO MODESTO: moneda_L supera a neutra_L y no cae; no cruza más |
| INDETERMINADO o PURGA | cualquiera | NO: el CONSERVA del explora no replica |

Con CONSERVA el titular dice "réplica con letra estricta; el explora estaba en el umbral (4/5 con esta letra)". No se escribe "×2" (H-3): el
explora, leído con esta letra, no llegó.
- **CONSERVA + no cruza más** → moneda_L queda sobre la neutra, y eso no hace cruzar a la cadena. Antes de decir "la selección conserva la
  regla" hay que mirar el descriptivo (¿subió la moneda o bajó la neutra?). La mitad que falta (R0 real ≥ 0.9) es el candidato siguiente.
- **CONSERVA + CRUZA MENOS** → además la cadena con la regla cruza menos: se cierra "conservar la regla ayuda a cruzar".
- **NO replica** → el CONSERVA del explora era deriva más una neutra que bajó. Se retira la frase "la selección conserva la regla si se paga el
  establecimiento". No se escribe "PURGA" salvo que la letra lo dé.
- **H-5:** si CONSERVA cae en el umbral (exactamente 7/10, o mediana entre 0.35 y 0.45), el TITULAR lleva "EN EL UMBRAL".
- Un resultado en el umbral se declara como tal en el titular de `lee()`.

## 7. Predicciones (firmadas antes del humo; `lee()` las imprime contra lo medido)
| # | predicción | p |
|---|---|---|
| R1 | veredicto CONSERVA (estricta) | 0.45 |
| R2 | veredicto INDETERMINADO | 0.47 |
| R3 | veredicto PURGA | 0.05 |
| R4 | cruce SIN DIFERENCIA | 0.68 |
| R5 | cruce CRUZA MENOS (como apuntó el explora) | 0.25 |
| R6 | cruce CRUZA MÁS (la hipótesis del director) | 0.04 |
| R7 | neutra_L: mediana de la fracción A final ≤ 0.30 (explora 0.14) | 0.60 |
| R8 | moneda_L: mediana de la fracción A final ≥ 0.40 (explora 0.80) | 0.60 |
| R9 | prueba de moneda_L: suma de cruzan (de 90) en [30, 50] | 0.70 |
| R10 | suma de diferencias de cruce D < 0 | 0.65 |
| R11 | elegidos por pasaje (mediana): neutra_L > moneda_L (explora 7 contra 5) | 0.70 |
| R12 | empates exactos de fracción final ≤ 2 de 10 | 0.75 |
| R13 | la letra original escalada (≥ en 10/10) se cumple | 0.12 |

NO SE LEE: 0.03 en cada medida. **Por qué no apuesto más por CONSERVA:** en el explora el cambio medio por pasaje de moneda_L fue +0.024 (casi
plano) y el de neutra_L −0.063; los linajes A y B se establecieron casi igual (0.68 contra 0.65 en moneda_L). La diferencia la hizo sobre todo
**la neutra que bajó**, y en mutacion la neutra había subido. Si esa bajada fue azar de 5 cadenas, la réplica sale INDETERMINADO.
**Las predicciones no son ciegas:** están hechas con los datos del explora a la vista.

## 8. Control que puede fallar, qué lo refuta, cuatro trampas
- **Control:** neutra_L. Mismas semillas, tasas, largo y moneda; sólo cambia w (0 contra −3). Si moneda_L sube y la neutra también, no hay pago.
- **Refuta la hipótesis 1:** INDETERMINADO o PURGA. **Refuta la hipótesis 2:** SIN DIFERENCIA (a este n) o CRUZA MENOS.
1. **Canal simétrico:** A y B tienen el mismo largo y consumo de rng; los brazos comparten tasas, semillas y moneda; el filtro "establecido" no
   mira la clase de la lista (heredado, arnés del explora).
2. **Acierto sin balancear:** todo parte de 0.5 exacto y se lee pareado. El nulo de cada puerta está en la sec. 4. Los empates cuentan en contra
   en las dos medidas.
3. **Mundo que se come la comida:** A y B conviven en la misma pista (aptitud dependiente de la frecuencia). La prueba final lleva lo que la
   cadena dejó; el cruce se lee contra la neutra en la misma semilla de mundo, no contra un número fijo.
4. **Sitios fijos:** semillas nuevas en pasajes y en pruebas; ninguna reusada del explora.

## 9. Costo, candados y comando
- Humo, un proceso: 6 corridas y 160 000 pasos (2 pasajes de 30k y prueba de 20k por brazo).
- Serie: 120 pasajes y 20 pruebas de 100k = **14.0 M pasos**. El explora (7.0 M, pool 2) tardó 58 min: **≈ 1 h 57 min**; con otra serie corriendo,
  hasta ~2 h 30 min. Dentro del objetivo (≤ 2.5 h con pool 2).
- **Candados de `--serie`:** (1) si una carpeta `serie_*` ya tiene veredicto CONSERVA, PURGA o INDETERMINADO, no se re-corre; (2) si existe una
  carpeta `serie_*` cortada o NO SE LEE, sólo con `--reanuda`; (3) `--reanuda` sin carpeta se niega; (4) git: el preregistro, el runner, el
  arnés, su salida, `sim_mmr.py` y los tres archivos importados de moneda_muro deben estar commiteados y sin cambios contra HEAD; (5) arnés PASA
  con los shas actuales; (6) pool ≤ 2.
- Comando (lo lanza el coordinador, desde la raíz del worktree `organelos`, después de commitear):
  `python experimentos/organelos/condiciones/moneda_muro_rep/corre_mmr.py --serie --pool 2`
- Si se corta: el mismo comando con `--reanuda` (sigue la última `serie_*`, reintenta los abortos, no recorre los buenos).
- Lectura suelta: `--lee datos/serie_<fecha>`.

## 10. Lo que NO hace esta réplica (declarado)
- No recorre moneda_25 ni neutra_25 y no compara cruces con guardados viejos (semillas de prueba nuevas).
- No corre `analiza_mm_estab.py` (establecimiento por tipo de linaje): ese script sólo conoce los modos del explora. Queda como descriptivo
  pendiente; no entra en la letra.
- No cambia la moneda. Una moneda que pague R0 real ≥ 0.9 es otro experimento.

## 11. Humo (un proceso; índice 14, pasajes 647240–647241, prueba 647390; corrido DESPUÉS de firmar las secciones 1–10; no cuenta)
Hubo 6 corridas y 160 000 pasos en 139 s (0.87 ms por paso). Carpeta `datos/humo_20261001_070605`; salida entera en `humo1_salida.txt`.
`main()` de punta a punta: verifica, 2 cadenas, 2 pruebas, `lee()` y `lectura_mmr.json` escrito. Arnés PASA con los shas actuales
(runner `26a87c8c02399d77`, arnés `6f2f5526db37f637`). Las 8 puertas de validez pasan; la moneda difiere de la vieja en 4/4 pasajes.

| brazo | fracción A: entrada → p0 → p1 | sombra (moneda vieja) | elegidos | respaldo | arrastre ≥ | cruzan en el pasaje | prueba 20k |
|---|---|---|---|---|---|---|---|
| moneda_L | 0.50 → 0.427 → 0.309 | 0.456, 0.316 | 6, 7 | 0, 0 | 0.56, 0.65 | 1, 3 | 1/9 |
| neutra_L | 0.50 → 0.484 → 0.605 | 0.507, 0.584 | 5, 8 | 0, 0 | 0.56, 0.59 | 2, 4 | 1/9 |

Veredicto del humo: fracción INDETERMINADO, cruce SIN DIFERENCIA (1 pareja; no cuenta). Como en el humo del explora, a 30k los linajes
establecidos todavía arrastran la siembra (arrastre ~0.6): el humo no prueba el régimen de 100k. **No cambio la letra, el diseño ni las
predicciones.** Candado en vivo: `--serie --pool 2` antes de commitear se niega ("git: ... commiteado False"). Costo: 14.0 M pasos ≈ 2 h con pool 2.

## 12. Cambios por auditoría antes del commit y antes de datos de serie (1-oct)
Auditor: APTO CON CAMBIOS MENORES. **La letra que decide no cambió** (constantes y `letra()` intactas: 7/10, mediana 0.40, PURGA 8/10, cruce 7/10 y D 9).
Cambiaron textos y descriptivos: H-1 (tabla de la neutra con sesgo y significado de CONSERVA; descriptivo `sobre_inicial` en `lee()`), H-2 (la
letra no es ciega), H-3 (fuera "×2"; titulares nuevos), H-4 (limitación de `moneda_actua`), H-5 (umbral en el titular). `sim_mmr.py` ganó un
bloque, así que la tabla del cruce se re-sorteó (0.455 → 0.448, 0.313 → 0.308, 0.752 → 0.754, 0.974 → 0.973; la nula no cambió). El humo de la
sec. 11 corrió con el runner anterior (`26a87c8c02399d77`) y no se repitió. Los shas finales están en `identidad_mmr_salida.txt`.
