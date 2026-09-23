# PREREGISTRO — subida del nivel 8, tanda 2: ¿qué frena al tronco cuando el mundo no se acaba: las celdas o lo que se atreve a probar? (23-sep-2026)

Misión: llegar a la AGI por este camino. Creador del equipo del nivel 8, tanda 2. Escrito **después** de tres humos de práctica
(semillas 14890, 14891, 14892, que no son de la serie) y **antes** del humo final (14893) y de la serie 14801–14820 y la réplica
14821–14840, que no se han corrido. Cualquier cambio posterior a este archivo es **candidato a ERR**.

## 0. De dónde parte y qué cambia respecto de la tanda 1
- Tanda 1 (`experimentos/subida_n8/`, REGISTRO «SUBIDA N8»): con 90 celdas y 200 estímulos de peso 3, el tronco v14.2 sigue
  aprendiendo la comida por encima del a priori (×2), pero en la réplica cae 0.19 tras agotar las celdas; la **fusión** no
  ayuda y empata con la fusión al azar (línea medida en negativo, **no se repite aquí**).
- Piezas del 100 % (tabla del §0 de `subida_n8/PREREGISTRO_n8.md`): 1 mundo sin techo (20; contado 10 + 5 propuesto por la
  tanda 1), 2 retener lo ausente (20; 0), 3 órgano que libere capacidad sin pagar con memoria (15; 0), 4 elegir su propio
  currículo (15; 10 contados por «probar cuando no se reconoce»), 5 recuperarse (10; hecho), 6 más de un valor (10; hecho),
  7 dominio distinto (10; 0). Propuesto hoy: 45–50 %.
- **Lo que vieron los humos de práctica (dato de práctica, no de serie; declarado):**
  1. En el mundo de estímulos de 4 píxeles el tronco muerde, en toda la vida, **4 a 8 veces cada comida** (432–835 mordidas de
     comida para 100 comidas), y la puerta de B-2 pide **5 mordidas del código exacto** para dejar de leer el a priori de la vía
     lenta, que dice «veneno» casi siempre. **El cuello no es sólo de celdas: es de muestreo** (neofobia). Con las celdas libres
     el tronco aprende sólo 0.33–0.47 de la comida temprana.
  2. Con la **lectura neutra de lo no reconocido** (órgano PRUEBA, §2) la comida temprana sube a 0.93 (s14892) y las muertes
     bajan de 473 a 295; las celdas se agotan antes (estímulo 42 contra 68) y **ahí aparece el muro de capacidad**: la comida
     tardía cae a 0.40. Probar al azar a la misma tasa propia (PRAZAR) aprende igual o más (0.56) pero muere más (428).
  3. Reciclar la celda de menor |Wp−Wn| (`rel`, s14890/14891) o la que entra en menos códigos familiares (`uso`, s14891/14892)
     **pagó con memoria en 3 de 4** (RET40 −0.07 a −0.125) y la adquisición tardía no se movió de forma consistente.
- Por eso este bloque no es «otro órgano de reciclaje»: es un **factorial pequeño** que separa las dos causas (muestreo y
  celdas) en un mundo de **500 estímulos nuevos (5.5× las celdas), T = 500 000**, y prueba cada órgano contra su control al azar.

## 1. Hipótesis
- **H-MUESTREO.** Si la boca lee como neutro (0) lo que la puerta no reconoce, en vez del a priori de la vía lenta, el tronco
  prueba lo nuevo, aprende la comida por encima del a priori a lo largo de 500 estímulos y muere menos. **Elegir qué probar por
  lo que no reconoce** cuesta menos vidas que probar al azar a la misma tasa, aunque no aprenda más.
- **H-CELDAS.** Una vez que el tronco sí muestrea lo nuevo, el cuello pasa a ser de celdas; reciclar la celda que entra en menos
  códigos familiares (`uso`) sostiene la adquisición tardía sin pagar con memoria y mejor que reciclar una al azar.
  **Predigo que H-CELDAS cae** (P13, P14): en práctica, reciclar pagó con memoria o no movió nada.

## 2. Mecanismo mínimo y memoria nueva
- **Organismo:** el tronco v14.2 sin cambios. `organismo_n8b.py` (`f9f3b56b498f6fc7`) se construye **por anclas**
  (`construye_n8b.py`, `f06946daadd82a6d`, 6 anclas con conteo exacto) desde `experimentos/subida_n8/organismo_flujo.py`
  (`14afed5aa16e09bf`, el instrumento de la tanda 1, anclado al tronco congelado `organismo/organismo_v142.py`
  `17528d767fcebaf6`, que sólo se lee). Con `recicla=0, prueba=0` es `organismo_flujo` EXACTO (arnés, §7).
- **Órgano PRUEBA** (`prueba=1`): al decidir morder, si la puerta de v13/B-2 no reconoce el código (menos de `puerta_pat` = 5
  mordidas del código exacto), el valor que entra en la boca es 0 y no el de la vía lenta. **Sólo cambia la decisión de morder**:
  el aprendizaje (`dlt = R − _wf`, `_ds = R − _ws`) y la medida (`valor_tot`) no se tocan. **Memoria nueva: cero. Constantes
  nuevas: cero.** Control **PRAZAR** (`prueba=2`, puede ganar): la misma lectura neutra en encuentros **al azar**, a la tasa
  que el propio organismo lleva de encuentros no reconocidos (dos contadores; generador aparte `[semilla, 8228]`). Nota
  declarada: como PRUEBA vuelve familiares las cosas más rápido, PRAZAR termina con **más** lecturas neutras que PRUEBA
  (arnés P3: 0.21 contra 0.08 en 30 000 pasos); es un control más explorador, no uno emparejado en número.
- **Órgano USO** (`recicla=3`): con la condición de división por conflicto de signo de v11 y **sin celda libre**, se libera la
  celda activa fuera del código actual que entra en **menos códigos familiares** (claves de `ncod` con ≥ `puerta_pat`
  mordidas; memoria que el tronco ya tiene), empate → menor |Wp−Wn| → índice menor; la división sigue como siempre. Liberar =
  poner a cero KW, mu, mup, mun, Wp, Wn, zp, zn, err, marcarla libre y **olvidar la evidencia `ncod` de los códigos que la
  contenían** (si no, el índice reusado heredaría evidencia ajena). **Memoria nueva: cero. Constantes nuevas: cero.** Control
  **azar** (`recicla=2`, generador aparte `[semilla, 8118]`). `recicla=1` (menor |Wp−Wn|) existe en el instrumento y se
  practicó en 14890–14891; **no es brazo** (pagó con memoria en las dos; `uso` es la versión que protege lo reconocido).
- **Mundo** (`mundo_n8b.py`, `74e6127ee3e36814`, por anclas desde `subida_n8/mundo_n8.py` `b0b57d7ff02afe4e`): el flujo de la
  tanda 1 (ventana 8, p_viejo 0.25, 4 objetos siempre, valencias al azar balanceadas 5/5 por bloque de 10, generador aparte
  `[semilla, 808]`) con **retina de 13 píxeles, patrones de peso 4 (C(13,4) = 715), 500 estímulos, uno cada 1000 pasos,
  T = 500 000**. El mundo del humo (200) es el **prefijo exacto** del de la serie (arnés E3).

## 3. Brazos (7 × 20 semillas por serie)
| brazo | prueba | recicla | pregunta |
|---|---|---|---|
| base | 0 | 0 | el tronco |
| prueba | 1 | 0 | ¿el muestreo era el cuello? |
| prazar | 2 | 0 | control que puede ganar: ¿importa **qué** se prueba? |
| uso | 0 | 3 | reciclar con el muestreo del tronco |
| pruso | 1 | 3 | reciclar cuando sí se muestrea (el régimen donde las celdas mandan) |
| pruazar | 1 | 2 | control que puede ganar de pruso: ¿importa **qué** celda se libera? (no practicado) |
| recic | 0 | 0 | mundo reciclado (novedad falsa): la medida tiene que ver la novedad |

## 4. Medidas (en `corre_n8b.py`; todas de solo lectura; las mismas definiciones que la tanda 1)
- **ADQ** de cada estímulo j: signo de `valor_tot` en la foto de t_entrada(j+9) (al salir de la ventana). **PRIOR**: el mismo
  signo en t_entrada(j)+1. **Medida principal: ADQ_com − PRIOR_com** (acierto sólo en comida; el veneno sale gratis por el a
  priori negativo). Tramos: **temprano** 10–39, **medio** 140–189, **tarde** 440–489 (5 bloques, 25 comida / 25 veneno).
- **NULO**: las mismas W contra valencias permutadas dentro de cada bloque (`[semilla, 909]`). **RET40** (y **RET40_com**):
  acierto balanceado (y de comida) de los 40 primeros en t = T−1. **Muertes**, mordidas de comida/veneno, estímulo de
  agotamiento, reciclajes, lecturas neutras.
- Letra de pareados: «A > B» = A mayor en **≥ 15/20** semillas **y** diferencia mediana **≥ 0.03**. «A muere menos que B» =
  A < B en ≥ 15/20 **y** mediana del cociente A/B ≤ 0.85.

## 5. Predicciones firmadas (20 semillas, medianas, en CADA serie)
| | predicción | p |
|---|---|---|
| V1 | (validez) RECIC > BASE en ADQ_tarde y RECIC ≥ 0.90 | 0.90 |
| V2 | (validez) BASE > NULO en ADQ_tarde en ≥ 15/20 | 0.80 |
| P1 | BASE agota las 90 celdas en ≥ 18/20; estímulo mediano de agotamiento en 50–95 | 0.85 |
| P2 | BASE: comida tarde − a priori en **0.00–0.20** | 0.65 |
| P3 | **Puede fallar.** PRUEBA sigue aprendiendo: comida tarde > a priori en ≥ 16/20 y dif. ≥ 0.15 | 0.55 |
| P4 | PRUEBA > BASE en comida tarde | 0.60 |
| P5 | **Puede fallar.** PRUEBA no sigue cayendo después de agotar: comida tarde − medio ≥ −0.10 | 0.50 |
| P6 | PRUEBA sí cae contra lo temprano (muro de celdas): comida tarde − temprano < −0.20 | 0.80 |
| P7 | PRUEBA muere menos que BASE | 0.80 |
| P8 | PRUEBA **no** gana a PRAZAR en comida tarde | 0.70 |
| P9 | **Puede fallar.** PRUEBA muere menos que PRAZAR | 0.65 |
| P10 | PRAZAR > BASE en comida tarde | 0.65 |
| P11 | USO **no** gana a BASE en comida tarde | 0.50 |
| P12 | USO no retiene más que BASE: RET40 USO − BASE ≤ +0.02 | 0.70 |
| P13 | PRUSO **no** gana a PRUEBA en comida tarde | 0.60 |
| P14 | PRUSO **no** gana a PRUAZAR en comida tarde | 0.70 |
| P15 | Ningún brazo del flujo retiene lo ausente: RET40 ≤ 0.70 y RET40_com ≤ 0.40 en todos | 0.70 |

## 6. Criterio (lo aplica `corre_n8b.py --veredicto SERIE.json REPLICA.json`; ninguna puerta cuenta si no pasa en las DOS)
- **NO SE LEE:** V1 o V2 cae en alguna serie.
- Puertas por pieza (propuesta de puntos; decide el director):
  - **G1, pieza 1 completa (+5):** PRUEBA cumple P3 y P5, o BASE cumple la misma letra (comida tarde > a priori ≥ 16/20, dif.
    ≥ 0.15, tarde − medio ≥ −0.10).
  - **G4, pieza 4 parcial (+3):** PRUEBA > BASE en comida tarde **y** PRUEBA muere menos que PRAZAR. **G4b (+5 en total):**
    además PRUEBA > PRAZAR en comida tarde (contra mi P8).
  - **G3, pieza 3 parcial (+5):** PRUSO > PRUEBA en comida tarde **y** no paga con memoria (RET40 PRUSO ≥ PRUEBA − 0.05 y
    PRUEBA no le gana en RET40 por la letra). **G3b, pieza 3 entera (+15):** además PRUSO > PRUAZAR.
  - **G2, pieza 2 (+10):** algún brazo del flujo con RET40 ≥ 0.75 y RET40_com ≥ 0.50 (contra mi P15).
- **FUNCIONA:** G1 **y** (G4 o G3) en las dos. Se diría: *«con 90 celdas fijas y 500 estímulos nuevos (5.5 veces sus celdas),
  el tronco que no se fía de su a priori para lo que no reconoce sigue aprendiendo la comida por encima del a priori, sin
  seguir cayendo después de agotar las celdas, y elegir qué probar por lo que no reconoce le cuesta menos vidas que probar al
  azar (dos series)»* (o la frase de G3 si es esa la que pasa).
- **HAY ALGO MODESTO:** alguna puerta pasa en las dos, sin la combinación de FUNCIONA.
- **NO:** ninguna puerta pasa en las dos.
- **Qué refuta H-MUESTREO:** P4 y P7 caen (probar lo no reconocido ni aprende más ni muere menos). **Qué refuta que importe
  elegir:** P9 cae (PRAZAR muere igual o menos). **H-CELDAS** se sostiene sólo con G3b.
- **Vocabulario prohibido:** «aprendizaje abierto», «indefinidamente», «acumula» (salvo G2), «curiosidad» (esto es novedad del
  código, no progreso de aprendizaje: la curiosidad por progreso sigue refutada), «currículo propio» sin la coletilla «en el
  sentido de elegir qué muestrear», ADQ balanceado sin la comida y el a priori al lado.

## 7. Arnés de identidad (`identidad_n8b.py`, `227e8b9423771926`; salida en `identidad_n8b_salida.txt`)
**50/50** antes de mirar números de la serie: procedencia por sha; `recicla=0, prueba=0` == `organismo_flujo` en todas las claves
(retina 6, mundo n8 con el pool agotado, con y sin fusión, mundo n8b); == `organismo_v142` congelado en W, muertes, divisiones,
celdas, mordidas y visitas (3 semillas); órganos inertes con celdas libres (reciclaje); reciclaje sólo con el pool agotado,
≤ 90 celdas, dirigidos ≠ azar, idénticos a la base hasta el primer reciclaje; PRUEBA lee neutro exactamente en los no
reconocidos; PRAZAR a su propia tasa; determinismo; mundo (prefijo, balance, 500 patrones de peso 4, reciclado); estático (sin
llamadas nuevas al rng principal, los órganos no leen valencias); regla 14 (175 campos, 0 distintos); **el runner aborta ante
banderas desconocidas o abreviadas** y ante combinaciones malas (ERR-115; la rama `--serie` se valida en proceso, **nunca se
ejecuta**); la letra del veredicto sobre resultados sintéticos, y `--veredicto` imprime la letra en su última línea.
Primera corrida 38/38 tras un fallo de diseño del propio arnés (C1 usaba un mundo que agota el pool en t = 76 170, demasiado
tarde para un T de 80 000); se cambió al mundo n8 (agota en 53 997). Declarado.

## 8. Semillas (verificadas con grep el 23-sep en `bundle` y en los worktrees `anclado, aprende, carrera, convive, criterio,
escuela, fanin` y `exploracion, respaldo, sandbox`, en .py/.md/.txt y en nombres de archivo)
- Serie **14801–14820**, réplica **14821–14840**; práctica **14890–14892** (usadas antes de este preregistro); humo final
  **14893**. Las únicas coincidencias de `148xx` son pasos de tiempo dentro de JSON viejos (`3T_confirmatorio`, `2Kbis`), no
  semillas. El runner **rechaza** cualquier `--desde` que no sea 14801 o 14821 y cualquier humo fuera de 14890–14899.

## 9. Comandos (sólo el coordinador) y costo
```
python experimentos/subida_n8b/identidad_n8b.py      # 50/50, ~95 s, un proceso
python experimentos/subida_n8b/corre_n8b.py --serie base,prueba,prazar,uso,pruso,pruazar,recic --desde 14801 --n 20 --pool 6
python experimentos/subida_n8b/corre_n8b.py --serie base,prueba,prazar,uso,pruso,pruazar,recic --desde 14821 --n 20 --pool 6
python experimentos/subida_n8b/corre_n8b.py --veredicto experimentos/subida_n8b/datos/n8b_serie_<sello>.json experimentos/subida_n8b/datos/n8b_replica_<sello>.json
```
Costo: 140 corridas × ~40 s (medido: ~15 s por corrida de 200 000 pasos) ≈ **95 min de CPU por serie**, ~17–20 min de pared con
Pool 6 si hay 6 núcleos libres; las dos ≈ **3.2 h de CPU, ~40 min de pared**. Sin estimación medida a T = 500 000 (el humo no puede
pasar de 200 000 pasos): el tiempo de la serie es una extrapolación.

## 10. Lo que este bloque no puede dar
Pieza 7 (dominio distinto del anillo, 10 puntos) y la curiosidad por progreso. Con todo a favor, el nivel quedaría en 45–50 % + 25
(+ 10 si G2) = 70–85 %; lo esperable según mis propias p es **+3 a +8**.
