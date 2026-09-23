# PREREGISTRO — subida del nivel 8: ¿sigue aprendiendo el tronco con 90 celdas cuando el mundo no se acaba? (23-sep-2026)

Misión: llegar a la AGI por este camino. Creador del equipo del nivel 8. Escrito **después** de los humos de práctica (semillas
12690 y 12691, que no son de la serie) y **antes** de correr 12601–12640. Nada de 12601–12640 se ha corrido.

## 0. Qué es el 100 % del nivel 8 según los documentos, y qué falta
Definición: "8 aprendizaje abierto" (`BRIEF_ORIGINAL_y_estado.md:13`). El Puente 4 dice que sólo vale "si el mundo **genera novedad
sin fin** … y el organismo tiene recursos fijos: ¿qué órganos permiten a un cerebro de tamaño fijo seguir aprendiendo
indefinidamente?" (`registro/HORIZONTE_frontera.md:108-111`). Las piezas, con el estado de hoy:

| # | pieza (fuente) | estado | peso propuesto |
|---|---|---|---|
| 1 | Mundo sin techo, con presupuesto fijo por paso, y criterio preregistrado "sigue aprendiendo": acierto en los **últimos** introducidos, más allá de donde se acaban las celdas (`nivel8_aprendizaje_abierto.md:69-70, 78-80, 86-90, 104-109`) | a medias: sigue aprendiendo hasta el techo de la retina, 50 patrones, 0.80 (`HANDOFF.md:497`). "Falta un mundo de más de 60 estímulos" (`REGISTRO_etapas_1_2.md:2434`) | 20 |
| 2 | Retener lo ausente mientras aprende lo nuevo, o sea acumular (`HANDOFF.md:497`, columna "falta"; `nivel8…md:90, 177-178`) | falta: 0.67, interferencia; metaplasticidad refutada (`REGISTRO…:3760`) | 20 |
| 3 | Un órgano que libere capacidad sin pagarlo con memoria: fusión u olvido dirigido (`nivel8…md:71-73, 92-97`; `HANDOFF.md:497`: "olvido/fusión") | falta: nunca se corrió | 15 |
| 4 | Explorar y elegir su propio currículo: curiosidad por progreso (`nivel8…md:74-77, 99-102`) | refutada en el mapa (`PLAN.md:23`); el canje del mapa quedó cerrado como estructural (`HANDOFF.md:497`) | 15 |
| 5 | Recuperarse de un cambio de regla o de la sorpresa (`HANDOFF.md:497`) | hecho y replicado | 10 |
| 6 | Más de una dimensión de valor; aprender cuándo contenerse (`ESTADO.md:30`; réplica de aprende_barrer del 23-sep) | hecho: mundo vivo, y aprende_barrer HAY ALGO MODESTO replicado | 10 |
| 7 | Dominio distinto del anillo; novedad que genera el mundo, no el experimentador (`HANDOFF.md:497`; `nivel8…md:134-143`, POET) | falta | 10 |

Cuenta de hoy (mía, la decide el director): 5 + 6 = 20, más media pieza 1 = 10, más lo parcial de 4 (probar cuando no se reconoce,
creación C) ≈ 10: **40 %**. Con la réplica de aprende_barrer, **45 %**.

**Por qué este bloque.** Es el "experimento único más informativo" que el propio documento del nivel dejó escrito y que nunca se
corrió (`nivel8…md:122-125`): el tronco sin órgano contra el tronco con fusión, en un mundo sin techo. Toca a la vez las piezas
1, 2 y 3, que suman 55 de los 60 puntos que faltan. Cuesta menos de una hora de CPU. P8 y P9 de aprende_barrer mueven como mucho
la pieza 6, que ya está contada.

## 1. Hipótesis
**H-N8.** Con 90 celdas fijas, el tronco v14.2 **sigue aprendiendo qué es comida** entre 200 estímulos nuevos. Eso es 2.2 veces
sus celdas y 3.3 veces el techo del mundo viejo (60). No cae después de agotar las celdas. Lo que pierde es lo ausente: aprende
lo reciente y olvida lo viejo, no acumula.
**H-FUS** (la del documento, `nivel8…md:162-164`). Fundir las dos celdas más parecidas cuando no queda celda libre sostiene lo
nuevo mejor que el tronco sin órgano. **En práctica la di vuelta: predigo que la fusión NO ayuda** (§5, P8).

## 2. Mecanismo mínimo y memoria nueva
- **Organismo: el tronco v14.2 sin cambios.** El instrumento es `organismo_flujo.py` (`14afed5aa16e09bf`), construido **por anclas**
  (`construye_n8.py`, 5 anclas con conteo exacto) desde `experimentos/nivel10_composicion_v14/organismo_capBD_on.py`
  (`506b5c08441fd54e`). Es el instrumento de capacidad de v14 con la retina de tamaño variable, el que midió N\* 51. Las perillas
  de v14.2 se pasan campo a campo desde `organismo/organismo_v142.py` (`17528d767fcebaf6`, congelado, sólo se lee).
  B-5 (`desambiguar`) no existe en el instrumento. Es inerte aquí por construcción: toda mordida da R en {+1, −3}.
- **Mundo en flujo** (perilla `ventana`). Retina de 12 píxeles, 200 patrones de peso 3 de C(12,3) = 220, en orden al azar por
  semilla. Entra uno nuevo cada 1000 pasos; T = 200 000. Cada objeto que nace es, con probabilidad 0.75, uno de los 8 más recientes
  y, con 0.25, uno de los anteriores: los viejos siguen apareciendo (`nivel8…md:90`). Siempre hay 4 objetos: el presupuesto por paso
  es fijo. Las valencias son al azar y **balanceadas 5/5 en cada bloque de 10**. El plan sale de un generador aparte
  (`[semilla, 808]`) y no toca el rng del organismo.
- **Órgano de fusión** (perilla `fusion`, `nivel8…md:92-97`). Se dispara con la misma condición que la división por conflicto de
  signo de v11, pero sólo cuando no queda celda libre. Funde las dos celdas activas con KW más parecido (coseno) que no tengan
  valor consolidado de signo opuesto, excluidas las del código actual. Fundir = promediar KW, Wp, Wn, mu, mup, mun, zp y zn y
  liberar una celda. **Memoria nueva: cero** (sólo contadores). **Constantes nuevas: cero.** El control `fusion=2` elige el par al
  azar con un generador aparte (`[semilla, 8008]`).

## 3. Medidas (en `corre_n8.py`, `1d78fd3ad1113eec`; todas de solo lectura)
- **ADQ** de cada estímulo *j*: el signo de su valor (`valor_tot`, el que usa la boca) en la foto de t_entrada(*j*+9), mil pasos
  después de salir de la ventana. **Balanceado:** media del acierto en comida y del acierto en veneno; W = 0 cuenta 0.5.
  **ADQ_tarde** = entradas 140–189 (5 bloques, 25 comida y 25 veneno). **ADQ_temprano** = entradas 10–39.
- **PRIOR** = el mismo signo en t_entrada(*j*)+1: el estímulo ya está en el mundo y no fue mordido nunca. Es lo que el organismo
  "sabe" gratis. **NULO** = las mismas W contra valencias permutadas dentro de cada bloque (generador `[semilla, 909]`).
  **ADQ_tarde_com / _ven** = el acierto por clase. **Hallazgo del humo:** el a priori es negativo casi siempre
  (en 12690, comida 0.16 / veneno 0.84), así que **el veneno sale gratis y lo aprendido es la comida**. La medida principal es por
  eso **ADQ_tarde_com − PRIOR_tarde_com**.
- **RET40** = acierto balanceado de los 40 primeros al final (t = T−1). **RET_todo** = el de los 200.
- **Conducta** (último cuarto): tasa de mordida de comida menos tasa de mordida de veneno. También se reportan muertes, divisiones,
  fusiones y en qué estímulo se agotan las celdas.

## 4. Mini-prueba (práctica, UN proceso, T = 200 000, 4 brazos; `datos/humo/`)
| semilla | brazo | ADQ_tarde | comida / prior de comida | temprano | RET40 | conducta | muertes | fusiones | celdas agotadas en el estímulo |
|---|---|---|---|---|---|---|---|---|---|
| 12690 | BASE | 0.78 | 0.56 / 0.16 | 0.73 | 0.45 | 0.081 | 382 | 0 | 73 |
| 12690 | FUS | 0.62 | 0.24 / 0.16 | 0.73 | 0.50 | 0.006 | 399 | 73 | 73 |
| 12690 | FUS_AZAR | 0.64 | 0.28 / 0.08 | 0.73 | 0.50 | 0.071 | 387 | 66 | 73 |
| 12690 | RECIC | 0.96 | 0.92 / 0.92 | 0.93 | 0.95 | 0.233 | 297 | 0 | — |
| 12691 | BASE | 0.72 | 0.44 / 0.16 | 0.77 (comida 0.53) | 0.675 | 0.043 | 319 | 0 | 46 |
| 12691 | FUS | 0.64 | 0.28 / 0.12 | 0.77 | 0.575 | 0.011 | 382 | 132 | 46 |
| 12691 | FUS_AZAR | 0.62 | 0.28 / 0.12 | 0.77 | 0.50 | 0.028 | 356 | 109 | 46 |
| 12691 | RECIC | 1.00 | 1.00 / 1.00 | 0.93 | 1.00 | 0.992 | 293 | 0 | — |

JSON: `n8_humo_…_s12690_20260923_160751.json` (`fe496ffd128aa5d6`) y `…_s12691_20260923_160909.json` (`cfeee01886128814`, con el
runner final). Unos 14 s por corrida con un Pool ajeno de 6 procesos corriendo.

## 5. Predicciones firmadas (20 semillas, medianas; «A > B» = A mayor en ≥ 15/20 **y** diferencia mediana ≥ 0.03)
| | predicción | p |
|---|---|---|
| P1 | BASE: ADQ_tarde en 0.66–0.82 | 0.75 |
| P2 | BASE aprende la comida más allá del a priori: ADQ_tarde_com > PRIOR_tarde_com en ≥ 16/20, diferencia mediana ≥ 0.15 | 0.80 |
| P3 | **Puede fallar.** BASE no cae después de agotar las celdas: mediana de (ADQ_tarde_com − ADQ_temprano_com) ≥ −0.10 | 0.60 |
| P4 | BASE olvida lo ausente: RET40 ≤ 0.65 | 0.75 |
| P5 | RECIC > BASE en ADQ_tarde (≥ 18/20) y RECIC ≥ 0.90: la medida ve la novedad | 0.90 |
| P6 | BASE > NULO en ADQ_tarde (≥ 15/20) | 0.85 |
| P7 | Conducta de BASE > 0 en ≥ 15/20; mediana en 0.01–0.15 | 0.70 |
| P8 | La fusión **no** ayuda: FUS > BASE en ADQ_tarde **no** se cumple, y FUS < BASE en ≥ 13/20 | 0.70 |
| P9 | FUS y FUS_AZAR no se separan: ninguno gana al otro con la letra | 0.75 |
| P10 | La fusión no compra memoria: RET40 de FUS − BASE ≤ +0.05 | 0.75 |
| P11 | BASE agota las 90 celdas en ≥ 18/20; mediana del estímulo de agotamiento en 35–90 | 0.80 |

## 6. Controles, qué refuta y lectura
- **Controles que pueden ganar:** NULO contra BASE (si empata, lo "aprendido" es ruido). FUS_AZAR contra FUS (si empata o gana,
  elegir bien el par no sirve). PRIOR contra BASE (si empata, es generalización gratis, trampa de `nivel8…md:149-150`).
  RECIC tiene que separarse de BASE; si no, la medida no ve novedad y no se lee nada.
- **H-N8 se refuta** si falla P2 o P6: con 200 estímulos y 90 celdas, el tronco ya no aprende lo nuevo.
- **H-FUS** (la del documento) se sostiene sólo si FUS > BASE **y** FUS > FUS_AZAR en ADQ_tarde **y** P10, en serie y réplica.
- **FUNCIONA:** P2, P3, P5 y P6 en la serie **y** en la réplica. Se diría: *«con 90 celdas fijas, el tronco v14.2 sigue aprendiendo
  qué es comida entre 200 estímulos nuevos, más del doble de sus celdas, sin caer después de agotarlas (dos series); el veneno ya lo
  suponía de antemano»*. Si además se cumple P4: *«y lo que no retiene es lo ausente: aprende lo reciente, no acumula»*.
- **HAY ALGO MODESTO:** P2 y P6 en las dos, pero P3 falla (cae más de 0.10 después de agotar las celdas, sin llegar al a priori).
  Se diría: *«sigue aprendiendo por encima del a priori, pero peor que con celdas libres»*.
- **NO:** P2 o P6 fallan en alguna de las dos.
- **Prohibido:** «aprendizaje abierto» o «indefinidamente» (son 200 estímulos, no una cantidad sin fin); «acumula»; «la fusión
  funciona» sin H-FUS completa; ADQ balanceado sin el acierto de comida y el a priori al lado; «comprende».

## 7. Puntos del nivel que movería cada resultado (propuesta; decide el director)
- **FUNCIONA:** la pieza 1 queda completa, **+10 → 55 %** (desde 45). La pieza 2 queda medida en negativo y no suma puntos, pero
  deja escrito qué falta.
- **HAY ALGO MODESTO:** **+5 → 50 %**.
- **NO:** **+0**. El límite queda medido y la fusión o su equivalente pasa a ser obligatoria.
- **Si H-FUS se sostiene contra mi P8:** la pieza 3 suma **+10 a +15** más. Si FUS gana a BASE pero no a FUS_AZAR: "liberar celdas
  sirve, elegir no", **+5**.
- **Lo que este bloque no puede dar:** las piezas 2, 4 y 7. Llegar al 100 % exige además retener lo ausente (un órgano de
  consolidación o de repaso), un currículo propio y un mundo que genere la novedad.

## 8. Semillas (verificadas con grep el 23-sep en todo `PROYECTOS\JUACO`, en .py, .md y nombres de archivo)
- Serie **12601–12620**, réplica **12621–12640**, práctica 12690–12691 (ya usadas y declaradas).
- Las únicas coincidencias textuales de `126xx` son duraciones de cuerpos (`carrera_escuderias/bitacoras/O4.md:174, 268`) y un sello
  de hora en un nombre de archivo, no semillas. Los hermanos de hoy usan 12301–12399 (`subida_n10`) y 13301–13394 (`subida_n9`).

## 9. Comandos (sólo el coordinador) y costo
```
python experimentos/subida_n8/identidad_n8.py          # 26/26, ~50 s, un proceso
python experimentos/subida_n8/corre_n8.py --serie base,fus,fusazar,recic --desde 12601 --n 20 --pool 6
python experimentos/subida_n8/corre_n8.py --serie base,fus,fusazar,recic --desde 12621 --n 20 --pool 6   # réplica
```
Costo: 80 corridas × ~14–16 s ≈ **20 min de CPU por serie**, ~4–6 min de pared con Pool 6. Las dos series juntas, ≈ 40 min de CPU.
El runner verifica los shas y la entrada campo a campo (regla 14) antes de correr. Si algo no coincide, aborta.
