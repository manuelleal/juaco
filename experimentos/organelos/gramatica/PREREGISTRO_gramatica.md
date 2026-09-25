# PREREGISTRO — ORGANELOS / GRAMÁTICA: ¿la selección ARMA con piezas un órgano de transmisión que no escribimos? (24-sep-2026, Opus A del equipo organelos; antes de cualquier serie)

Misión: llegar a la AGI por este camino. Carpeta: `experimentos/organelos/gramatica/`. Nivel 10, frente 2 (línea ECO), palancas 1 y 2
de la bitácora de la nube (§4, "de PRENDER órganos a CREARLOS"). Todo es nuevo; nada existente se tocó.
**Nada de esto está corrido en serie.** La serie, la réplica, la fuerza bruta confirmatoria y la prueba del ganador quedan
RESERVADAS para el coordinador (Pool).

## 0. Instrumento (sha a 16; los recalcula `corre_gramatica.SHAS()`)
- **Sha finales (los del arnés 20/20 de las 14:13):** `corre_gramatica.py` f8af47e8a3b496da · `motor_gramatica.py` 6b65dc5e32093424 · `carros/FAMB_GRAM_ECO.py` 2cee0a8510c997b9 · `gramatica_def.py` c58086e103d030d9 · `conducta.py` 9a2f1226fe27a514 · `construye_gramatica.py` df8c78c3c0d53cad.
  El humo (13:24), la fuerza bruta exploratoria (13:25–14:02) y el humo largo (14:04) corrieron con `corre_gramatica.py` 77cd07064a6270ab y `gramatica_def.py` c58086e103d030d9 (humo) / 0eac… → c580… (arreglo de `texto()`). La diferencia con el final está SOLO en `veredicto()` (S y P5), en `--fuerza_conf` y en las banderas; `trabajo()`, el motor y el carro no cambiaron.
- `construye_gramatica.py` construye por anclas **`motor_gramatica.py`** desde `juaco_eco/motor_eco2.py` (0921ee3a50ce7f7a) y
  **`carros/FAMB_GRAM_ECO.py`** desde `juaco_eco/carros/FAMB_ORG_ECO.py` (75d5f4118079ff15): el instrumento de ECO v2.1, el que pasó.
  `motor_eco3.py` (2eec9830792d9822) difiere de `motor_eco2` SOLO en la tabla GENES y no tiene el gen `ensena`, así que "motor_eco3 +
  FAMB_ORG_ECO con ensena encendido" no existe tal cual. El arnés compara contra motor_eco2 y además verifica motor_eco3 == motor_eco2
  con los órganos apagados (I6).
- `gramatica_def.py` (la gramática y los errores de copia), `conducta.py` (la novedad por conducta), `corre_gramatica.py` (runner y
  letra), `deriva_slots.py` (la deriva del largo sin selección).
- **Arnés `identidad_gramatica.py`: 20/20** (salida en `identidad_gramatica_salida.txt`). La pedida (I3): con la gramática fija en
  `[nacer/todo/hijo/copiar]`, motor_gramatica + FAMB_GRAM_ECO da **bit a bit** lo mismo que motor_eco2 + FAMB_ORG_ECO con `ensena`
  prendido en VIDA, AZAR y MUT0 (linajes, pista, pizarra y eco). También: sin gramática == motor_eco2 (I1, I2, I2b); filtra0 (I4,
  física); vacía y silenciosa == apagado (I5); el rng de la gramática no toca el mundo (I7); checkpoint (I8); nube-9 atrapado (I9);
  errores de copia (I10); conducta (I11); la letra en entradas sintéticas (V); banderas (R); arnés por pieza (P).
  - Primera corrida del arnés: 16/17. (I4) comparaba la TELEMETRÍA del carro: `n10.dado` cuenta lo dado antes del filtro del hijo
    (FAMB_ORG_ECO) o después del filtro del emisor (gramática). La física era idéntica. Se corrigió el arnés para comparar la física
    (ERR-96) y declarar esa telemetría. Fue antes de mirar ningún número. (I2) no ejercitaba la rama numérica del carro (0 vivos con
    `ensena` prendido) y se agregó (I2b) (ERR-120).
- **ERR-125 (coordinador, 24-sep ~14:50, ANTES de la serie; auditoría juaco-auditor: LISTO CON CORRECCIONES).**
  - Aclaración de H-1: ERR-96 y ERR-120 aparecen arriba como PRECEDENTES del mismo tipo de fallo (comparar telemetría en vez de
    física; un arnés que no ejercita la rama que importa). No son números nuevos. Los números nuevos de este paquete son los de
    ERR-125.
  - (a) Se quitó «olvidar» del alfabeto después de que el arnés por pieza lo midiera idéntico a «copiar». Quedan 135 órganos de un
    slot en vez de 180.
  - (b) La regla P5 cambió de forma después del humo largo de práctica 21901: la simétrica no tenía potencia.
  - Por la regla 11, (a) y (b) llevan ERR aunque no haya serie. Las dos se escribieron antes de cualquier semilla de serie, réplica
    o confirmatoria.
  - (c) H-3: la fuerza bruta exploratoria (136 corridas en un proceso, en bloques de menos de 20 min) la pidió el coordinador en el
    encargo. Es una excepción autorizada a la regla 3, no un desliz del creador.
  - (d) H-4: el `RANKING.json` de la confirmatoria reportaba las semillas de la exploratoria. `corre_gramatica.py` escribe ahora
    las de CONF cuando la carpeta es `fuerza_conf_*`. No toca el ranking ni el TOP.
  - H-7: antes de leer P3, el coordinador revisa la clase por conducta del candidato del borde (`nacer/neg/hijo/copiar`).
- Humo `--humo` (21001, T 20 000, corte 10 000, VIDA y AZAR): escribe los dos JSON (`datos/humo/gramatica_humo_20260924_132441/`).
  El primer humo encontró un error de impresión en `texto()` después de escribir el JSON de VIDA (se corrigió).

## 1. Pregunta y nombre honesto
Con selección natural sola (después del corte nadie repone nada), **¿la población termina en el TOP del ranking de fuerza bruta con
un órgano que NO sea conductualmente igual a los diseñados?**
- Si sí, lo que se declara es **«la selección COMBINA un órgano que no escribimos»**.
- **«La selección CREA un órgano»** se declara solo si un slot DUPLICADO diverge hacia una función que ningún diseñado tiene (P4, §6).
- Vocabulario prohibido: «evoluciona», «cultura», «especie», «inventa».

## 2. La gramática (palanca 1) y los ajustes a la lista pedida
Un órgano es una tupla de 0 a 4 slots. Cada slot tiene la forma (cuándo, qué, a quién, cómo, origen):
- **cuándo:** nunca (silencioso) | al nacer (en el parto) | en vida (cada 500 pasos de edad = rep_X de fábrica) | al morir (antes de `muere`).
- **qué:** todo | solo negativo (veneno/sal) | solo positivo | sin lo neutro (= filtra0) | solo lo reciente (últimas 20 mordidas VIVIDAS,
  nada heredado).
- **a quién:** hijo | hermano (mismo linaje y mismo padre) | vecino (el cuerpo vivo más cercano en el anillo, de cualquier linaje).
  Si hay varios candidatos, gana el más cercano; en empate, el primero de la lista (sin rng). El paquete `nacer/hijo` viaja por
  `al_parir`/`nace`, el camino de FAMB_ORG_ECO.
- **cómo:** copiar | promediar (el receptor instala (R + lo que ya cree por la vía lenta)/2) | invertir (−R).
- **origen:** 0 original | 1 nacido por duplicación (se hereda, no se expresa, sirve para leer la palanca 2).
- Qué recibe el receptor: los paquetes de un mismo evento se funden en una tabla, y si una clave se repite gana el último slot del
  genoma. En vida y al morir, lo recibido entra al nodo (se pasa después) y se lee por la vía lenta como en `nace`.

**Ajustes justificados:**
- (a) Se agrega **«nunca»**. Es el estado apagado del órgano (en ECO v2.1 los órganos nacían apagados) y permite variación críptica:
  los campos de un slot silencioso derivan libres.
- (b) **«magnitud alta» se contrae.** Con R en {+1, −3, 0}, un umbral entre 0 y 1 da `sin0` y uno entre 1 y 3 da `neg`. Queda `sin0`,
  que es filtra0.
- (c) **«olvidar lo heredado que contradice lo vivido» SE QUITA.** El arnés por pieza (P) lo midió IGUAL a copiar en los tres
  contextos (nacer/hijo, vida/vecino, morir/vecino), bit a bit: en w30 los valores del mundo no cambian, así que lo heredado solo
  contradice lo vivido si otro slot lo corrompió. Está implementado (`como = 3`) y queda para un mundo que cambie (Reina Roja).
  Todas las demás opciones cambian la trayectoria de w30 (`datos/pieza_gramatica.json`).
- Espacio de un slot de la serie: 3 × 5 × 3 × 3 = **135**, más el nulo. El banco conductual (§4) separa 159 clases entre las 180
  gramáticas con `olvidar`. Sin `olvidar`, las 135 son conductualmente distintas.

## 3. Errores de copia (palanca 2). Tasas DECLARADAS (pedido del coordinador)
En cada parto, y en cada fundador del vivero que sale del banco, con rng propios ([seed, linaje, 20|21, k]; no tocan ningún rng del
mundo, arnés I7):
- **duplicación p_dup = 0.02** por copia (un slot al azar se copia en tándem, con origen 1, si hay menos de 4);
- **borrado p_del = 0.02** por copia (un slot al azar desaparece; **el órgano vacío es absorbente**: no hay inserción de la nada);
- **cambio de campo p_campo = 0.05** por slot y por campo (pasa a OTRO valor del alfabeto; la misma tasa que la mutación numérica
  de ECO).
- **Tope: 4 slots.** Los fundadores son UN slot silencioso con qué/quién/cómo al azar del alfabeto (rng [seed, i, 22, 0]): no hay
  sesgo hacia los diseñados.
- **Sesgo de los operadores, declarado** (lección D1 de `exploracion_fable`): duplicar y borrar tienen la misma tasa, pero el 0 es
  absorbente y el 4 refleja, así que la deriva del largo tiene DIRECCIÓN, hacia 0 slots. `deriva_slots.py` (cadenas neutrales,
  20 000 réplicas) predice la deriva sin selección:

| generaciones | slots totales (media) | vacíos | slots activos (media) | con órgano expresado |
|---|---|---|---|---|
| 10 | 1.00 | 0.16 | 0.37 | 0.33 |
| 20 | 1.01 | 0.28 | 0.56 | 0.45 |
| 40 | 1.00 | 0.42 | 0.71 | 0.47 |
| 80 | 0.98 | 0.57 | 0.73 | 0.39 |
| 160 | 0.85 | 0.69 | 0.64 | 0.29 |

  En el mundo, esa deriva la miden AZAR (sin selección) y las 8 sombras de cada cuerpo (misma genealogía, sin expresión).
  **Si VIDA termina con el mismo número de slots activos que AZAR y que sus sombras, el largo no lo eligió la selección** (medida S, §6).

## 4. Novedad por CONDUCTA (`conducta.py`), no por etiqueta
- Banco fijo: 5 estados de emisor. S0 no vivió nada. S1 vivió todo. S2 heredó todo y vivió solo lo bueno. S3 vivió el veneno hace
  más de 20 mordidas. S4 heredó el veneno INVERTIDO y la comida a medias (alcanzable con invertir o promediar en la línea).
  Receptores: recién nacido (el hijo al nacer), Rn (recién nacido sin nada) y Ra (adulto que vivió veneno y comida).
- La **tabla de efecto** de una gramática da, por (evento, a quién, emisor, receptor), el cambio en los 8 valores de la vía lenta
  del receptor. Se calcula con el código real del carro.
- **Dos gramáticas son el mismo órgano si sus tablas difieren en a lo sumo TOL = 0.05 en todas las celdas.**
- Diseñados: **nulo** (no transmite), **ensena** (nacer/todo/hijo/copiar) y **filtra0** (nacer/sin0/hijo/copiar, = ensena + filtra0
  del hijo). Sus distancias mutuas son 3.0, 3.0 y 1.71 (arnés I11).
- Riesgo declarado: el banco no es exhaustivo. Dos órganos iguales en el banco podrían diferir en el mundo (así pasó con `olvidar`).
  Por eso también está el arnés por pieza.

## 5. Fuerza bruta (regla de oro): el ranking verdadero del espacio de un slot
- Cada gramática de un slot (135) y el nulo, **FIJA en monocultivo** (30 fundadores en w30, sin errores de copia de la gramática,
  mutación numérica y selección como VIDA), con vivero hasta el corte y después solo.
- **Puntaje** = media por semilla de (persiste en T + min(R0 de nacidos en [corte, T − margen], 1.2)) / 2.2.
- **Exploratoria (CORRIDA, dato visto; declarada):** semilla 21101, T 18 000, corte 6 000, margen 6 000, un proceso, 6 bloques.
  Resultado en `datos/fuerza_explora_s21101_T18000/RANKING.json` (§9).
- **Confirmatoria (RESERVADA, define el TOP de la letra):** las mismas 136, semillas **21201–21203**, mismo T.
  `corre_gramatica.py --fuerza_conf --pool P` escribe `RANKING.json` con `TOP`.
  **TOP = las gramáticas de un slot cuyo puntaje queda a ≤ 0.10 del mejor.**
- Riesgo declarado: el ranking es de monocultivo (todos llevan el órgano) y a T corto. La serie selecciona entre linajes mezclados y
  a T largo. Un órgano que beneficia al VECINO de otro linaje puede puntuar alto en monocultivo y NO ser seleccionable (el beneficio no
  vuelve al portador). La letra lo deja fallar; no se corrige después.

## 6. La serie (RESERVADA) y la letra (`corre_gramatica.veredicto`)
- **Mundo w30** (esc 30, 30 fundadores, quimiostato 0.9 objetos por paso). **T 120 000, corte 60 000** (los de ECO v2.1 en w30).
  Banco 200, 8 sombras, mutación numérica p 0.05 y σ 0.15 en 18 genes (los genes numéricos `ensena`/`filtra0` quedan como pseudogenes
  fijos), cada_gen 2000, checkpoint cada 10 000.
- **Brazos:**
  - VIDA: fundadores silenciosos, errores de copia, el hijo copia al padre.
  - AZAR: todo cuerpo nuevo copia una entrada al azar del banco; deriva pura.
  - MUT0: sin ningún error de copia, así que el órgano silencioso no puede prenderse.
  - FIJO:ensena, FIJO:filtra0, FIJO:nulo: los diseñados fijos.
  - Las **sombras** son 8 gramáticas por cuerpo que siguen su genealogía con los mismos errores y no se expresan.
- **Semillas NUEVAS** (grep del 24-sep: sin usos 21000–21999, salvo una mención ajena a "21800"):

| uso | semillas |
|---|---|
| humo | 21001 |
| identidad | 21002 |
| arnés por pieza | 21003 |
| **serie** | **21011–21030** |
| **réplica** | **21031–21050** |
| fuerza bruta exploratoria | 21101 |
| **fuerza bruta confirmatoria** | **21201–21203** |
| **prueba del ganador** | **21301–21320** |
| práctica y derivas | 21901–21999 |

- **Medidas** (sobre el banco FINAL de padres, en T; la medida que manda es vivir solo):
  - **P1a (selección contra deriva):** en VIDA, la fracción del banco final que EXPRESA algún slot con conducta TOP supera a la media
    de las de sus 8 sombras (estricto) en **≥ 15/20**.
  - **P1b:** esa fracción es mayor en VIDA que en AZAR (pareado, estricto) en **≥ 15/20**.
  - **P2 (termina en el TOP):** en VIDA, la conducta MODAL del banco final (agrupada por conducta) expresa un slot TOP, en semillas que
    persisten en T, en **≥ 14/20** (las extintas cuentan como fallo).
  - **P3 (no diseñado):** esa modal NO es conductualmente igual a nulo, ensena ni filtra0 en **≥ 10/20**.
  - **P4 (CREA):** en **≥ 5/20** la modal tiene ≥ 2 slots activos, y uno nació por duplicación (origen 1). Su conducta de un slot no
    es la de ningún diseñado ni la de los otros slots, y la gramática sin él tiene otra conducta.
  - **S (el largo; secundario, pedido del coordinador):** slots ACTIVOS en el banco final de VIDA contra sus sombras (≥ 15/20) y
    contra AZAR (≥ 15/20). Si no pasan las dos, «el largo no lo eligió la selección».
  - **P5 (secundario; no cambia el veredicto): la selección CONCENTRA el banco en UN órgano armado, sea o no TOP.** El estadístico
  es simétrico: c = fracción del banco final que expresa su clase ACTIVA más frecuente (por conducta). Se calcula igual para el real
  y para cada una de las 8 pistas de sombras. Bajo la nula (intercambiables), P(real > media de sombras) ≈ 0.5 por semilla.
  Pasa con **≥ 15/20** en VIDA; si AZAR también da ≥ 15/20, P5 no se lee. Se informa la clase y si es diseñada.
  Nace de la práctica (21901): VIDA concentró su banco en `morir/neg/hijo/promediar` (0.285 contra 0.113 de las sombras).
- Descriptivas: persistencia en T y R0 de nacidos tras el corte por brazo (VIDA contra FIJO:ensena, FIJO:filtra0, FIJO:nulo, AZAR
    y MUT0).
- **Veredicto por ventana:**
  - **NO EVALUABLE:** ventana incompleta; alguna corrida abortada por el motor (nube-9 u otra); bloqueados > 0; AZAR expresa TOP
    sobre sus sombras en ≥ 15/20 (guardia); MUT0 transmite algo (el instrumento estaría mal).
  - **FUNCIONA — LA SELECCIÓN CREA UN ÓRGANO:** P1a, P1b, P2, P3 y P4.
  - **FUNCIONA — LA SELECCIÓN COMBINA UN ÓRGANO QUE NO ESCRIBIMOS:** P1a, P1b, P2 y P3.
  - **HAY ALGO MODESTO:** P1a y P1b (con o sin P2), pero la modal es un diseñado o no llega al TOP en ≥ 14/20; o bien solo una
    de P1a y P1b.
  - **NO:** ninguna de P1a y P1b.
- **El bloque** se declara solo si serie y réplica dan el mismo veredicto; si no, vale el menor. La regla 12 aplica: un veredicto a
  ±1 del umbral dispara una réplica en semillas nuevas.
- **Prueba del ganador (RESERVADA; solo si hay FUNCIONA):** la gramática modal de cada semilla de VIDA, FIJA en monocultivo, en las
  semillas 21301–21320, T 120 000, pareada contra FIJO:ensena en la misma semilla. «Vive más que el diseñado» si su R0 de nacidos
  tras el corte es mayor en ≥ 13/20. Sin esa prueba, «CREA» se declara como «CREA (sin la prueba del ganador)».

## 7. nube-9 (la guardia de ERR-60 dentro de un Pool)
- `trabajo()` atrapa `SystemExit` y cualquier `Exception` del motor, escribe el JSON con `abortado` y nunca cuelga un Pool (arnés I9b).
  Una corrida abortada vuelve la ventana NO EVALUABLE (no se descarta en silencio).
- Además, T = 120 000 en w30 queda lejos de la guardia. En el humo (T 20 000), `max_nac_linaje` fue 48 y 58. La guardia muerde a
  100 000 cuerpos en UN linaje: con v1.2 pasó a T = 1e6 con familia, entre t = 320 000 y 900 000. Cada JSON trae `max_nac_linaje`.

## 8. Las cuatro trampas (revisadas)
1. **Canal simétrico.** El órgano de VECINO es un bien público: beneficia a cualquier linaje. En monocultivo puede puntuar alto y
   en la serie no ser seleccionable. Está declarado como riesgo (§5) y como predicción (§9). No se corrige después.
2. **Acierto sin balancear.** No hay tasas de acierto. Las pruebas son pareadas (real contra la media de sus sombras de la misma
   genealogía; VIDA contra AZAR en la misma semilla).
3. **Mundo que se come la comida.** Es el quimiostato de ECO (flujo fijo). El R0 depende de la densidad: con capacidad de carga
   tiende a 1 para cualquier órgano viable. Por eso el puntaje suma la persistencia. En w30, tras el corte, la población cae a
   2–10 cuerpos (visto en ECO v2 y v2.1), lejos de K.
4. **Sitios fijos.** Los objetos aparecen al azar; no hay sitios que memorizar. La tabla transmitida es por patrón y necesidad, no
   por lugar.

## 9. Datos VISTOS antes de firmar (declarados)
- **(a) Fuerza bruta exploratoria.** 136 gramáticas × semilla 21101, T 18 000, corte 6 000; 2 232 s de CPU en un proceso.
  - TOP exploratorio (a ≤ 0.10 del mejor): solo los dos diseñados.
  - El tercero, `nacer/neg/hijo/copiar` (pasar solo el veneno al hijo), quedó a 0.0034 del corte.
  - El nulo quedó último (R0 0) y 83 de 135 le ganan.
  - Medias por campo: nacer > vida > morir; sin0 ≈ neg > todo > pos > reciente; copiar > promediar > invertir.
  - «Vecino» promedia MÁS que «hijo»: el bien público en monocultivo (§5).

| puesto | gramática | puntaje | persiste | R0 | vivos en T |
|---|---|---|---|---|---|
| 1 | nacer/todo/hijo/copiar (**ensena**) | 0.793 | 1/1 | 0.744 | 2 |
| 2 | nacer/sin0/hijo/copiar (**filtra0**) | 0.712 | 1/1 | 0.566 | 7 |
| 3 | nacer/neg/hijo/copiar | 0.689 | 1/1 | 0.516 | 7 |
| 4 | nacer/neg/vecino/invertir | 0.659 | 1/1 | 0.450 | 1 |
| 5 | vida/sin0/vecino/copiar | 0.616 | 1/1 | 0.355 | 3 |
| 6 | nacer/todo/vecino/invertir | 0.613 | 1/1 | 0.348 | 1 |
| 7 | morir/sin0/hijo/copiar | 0.610 | 1/1 | 0.342 | 2 |
| 8 | vida/neg/hijo/copiar | 0.574 | 1/1 | 0.262 | 2 |
| 136 | nulo | 0.000 | 0/1 | 0.000 | 0 |

  Con una semilla, la persistencia es frágil (1 a 7 cuerpos en T); los puestos 4 y 6 persisten con UN cuerpo.
- **(b) Humo largo de práctica** (21901, T 120 000, corte 60 000; `humo_largo.py`):
  - VIDA: se extinguió (R0 0.24, 129 s). Al corte, el 51 % del banco estaba silencioso y el 23.5 % era `morir/neg/hijo/promediar`
    (un órgano no diseñado y no TOP). Expresión de candidatos TOP: 0.0 (sombras 0.003–0.012). Slots activos 0.48, sombras 0.40.
  - FIJO:ensena: persiste (9 vivos, R0 0.98, 308 s; `max_nac_linaje` 1 795).

## 9b. Predicciones firmadas (antes de la confirmatoria y de la serie)
| cantidad | rango | probabilidad |
|---|---|---|
| TOP confirmatorio contiene ensena / filtra0 / nacer/neg/hijo/copiar | — | 0.85 / 0.70 / 0.50 |
| TOP confirmatorio con ≥ 1 no diseñado | — | 0.55 |
| **P1a** VIDA expresa TOP sobre sus sombras — **la que puede fallar** | 3–14 /20 | P(≥ 15) = 0.15 |
| **P1b** VIDA > AZAR en expresión de TOP | 3–14 /20 | P(≥ 15) = 0.15 |
| P2 modal de VIDA en TOP | 0–6 /20 | P(≥ 14) = 0.03 |
| P3 modal en TOP y no diseñada | 0–4 /20 | P(≥ 10) = 0.02 |
| P4 CREA | 0–2 /20 | P(≥ 5) = 0.02 |
| S slots activos VIDA > sombras / VIDA > AZAR | 10–20 / 5–15 /20 | P(S elige el largo) = 0.25 |
| P5 VIDA concentra más que sus sombras (AZAR) | 13–20 (6–14) /20 | P(VIDA ≥ 15) = 0.60 |
| persisten en T: VIDA · AZAR · MUT0 · FIJO:ensena · FIJO:filtra0 · FIJO:nulo | 2–10 · 0–6 · 0–3 · 14–20 · 12–20 · 0–3 | — |
| R0 tras el corte (mediana): VIDA · FIJO:ensena · FIJO:filtra0 · FIJO:nulo y MUT0 | 0.15–0.6 · 0.85–1.0 · 0.8–1.0 · 0–0.25 | — |
| **veredicto por ventana** | FUNCIONA-CREA 0.01 · FUNCIONA-COMBINA 0.04 · MODESTO 0.20 · **NO 0.65** · NO EVALUABLE 0.10 | — |

Por qué predigo NO:
- En la práctica, la selección ARMA un órgano no diseñado (P5), pero se queda en un óptimo local (morir/neg/hijo/promediar) y no
  llega al TOP en 60 000 pasos de vivero.
- Tres razones posibles, que la serie no separa:
  1. El TOP exige 4 campos a la vez: desde un slot silencioso al azar, P ≈ 0.05 × 1/3 × 1/15 ≈ 1e-3 por parto.
  2. La carga de errores es de ~18 % por parto y por slot.
  3. Los órganos de vecino son bienes públicos.
- Si sale NO con P5 en pie, lo que se declara es «la selección amplifica un órgano armado que no escribimos, pero no el mejor del
  espacio». No se declara «combina un órgano del TOP».

## 10. Qué refuta
- **H (la selección arma con piezas un órgano del TOP):** P1a y P1b caen (NO) en serie o réplica.
- **H-novedad (no es un diseñado):** la modal es ensena o filtra0 en > 10/20 con P2 en pie, o el TOP confirmatorio contiene solo
  diseñados (entonces la pregunta queda sin espacio para lo nuevo y lo más que puede salir es MODESTO).
- **H-duplicación (palanca 2):** S falla (el largo de VIDA = AZAR = sombras) y P4 < 5/20.
- **H-amplifica (secundaria):** P5 de VIDA < 15/20, o P5 de AZAR ≥ 15/20 (entonces el estadístico no separa selección de deriva).
- **El instrumento:** la guardia de AZAR, MUT0 transmitiendo o alguna corrida abortada.
- **Mis predicciones:** cualquier cantidad fuera de su rango de §9b se declara refutada en el registro, con su número.

## 11. Costo (medido; Python, sin gemelo)
- Medido: fuerza bruta a T 18 000, **16.4 s** por corrida de media. A largo completo (T 120 000): VIDA **129 s** (se extinguió) y
  FIJO:ensena **308 s** (persiste).
- Estimado por semilla (6 brazos): VIDA ~150 + AZAR ~130 + MUT0 ~100 + FIJO:ensena ~310 + FIJO:filtra0 ~300 + FIJO:nulo ~100
  ≈ 1 090 s. **Una ventana (20 semillas) ≈ 6.1 h de CPU.**

| bloque | CPU | Pool 3 | Pool 6 |
|---|---|---|---|
| fuerza bruta confirmatoria (408 corridas) | 1.9 h | 0.6 h | 0.3 h |
| serie | 6.1 h | 2.0 h | 1.0 h |
| réplica | 6.1 h | 2.0 h | 1.0 h |
| prueba del ganador (40 corridas, solo si hay FUNCIONA) | 3.3 h | 1.1 h | 0.6 h |
| **todo** | **17.4 h** | **≈ 5.8 h** | **≈ 2.9 h** |

- Pool 6 supone 6 núcleos físicos libres (optimista). Un gemelo numba de motor_gramatica bajaría ~×40 (ECO v2.1: gemelo ×42–48),
  pero exige extender `motor_eco_rapido_org` con la gramática; lo haría otro agente.

## 12. Orden de ejecución para el coordinador
1. `python experimentos/organelos/gramatica/identidad_gramatica.py`, que debe dar 20/20. `python manifiesto.py --check`.
2. `corre_gramatica.py --fuerza_conf --pool P` → `datos/fuerza_conf_s21201-21203_T18000/RANKING.json` (TOP).
3. `corre_gramatica.py --serie --ventana serie --pool P --top <RANKING.json>`, y después `--ventana replica`.
4. Solo si hay FUNCIONA: la prueba del ganador (§6), preregistrada aquí. Su código NO está escrito; se escribe y se arnesa antes.
