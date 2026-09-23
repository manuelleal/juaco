# PREREGISTRO — nivel 9: ¿el modelo de sí es causal en el linaje que cruza H-1? (subida_n9, 23-sep-2026, creador)

Misión: llegar a la AGI por este camino. Escrito ANTES del humo y de cualquier serie. Carpeta: `experimentos/subida_n9/`.
Nada de este bloque toca congelados, `carrera_escuderias/`, `generaciones/` ni carpetas de otros equipos: solo se leen.

## 0. Por qué este bloque (y no otro)
El nivel 9 es "autonomía / modelo de sí mismo". Hoy está en 50 % declarado; la propuesta de 65 % se apoya en la carrera de
escuderías: O3 y O4 sostienen R0 real ≥ 0.90 con recambio de generaciones, replicado en sellada, **con muerte programada**.
Tres cosas no están medidas y son exactamente el "modelo de sí":
1. O3 decide TODO leyendo su propio estado actual (E, Ag): qué come, cuándo limpia, cuándo prueba. Nadie midió si ese cruce
   **depende de leer el estado propio de AHORA** o sólo de la estructura de la política (escrita por un LLM).
2. La muerte programada de O3 (TERMINAL) lee una estimación de la **reserva del linaje** (`cola_est ≥ 4`) y la historia del
   cuerpo (`partos ≥ 2`). ERR-102/103: la métrica de R0 real premia morir y el clasificador de muerte voluntaria no discrimina.
   Nadie separó "muere cuando su linaje puede permitírselo" (historia de vida, modelo del linaje) de "muere más" (juego de la métrica).
3. Si la muerte programada hace falta en la pista v1 (el control sin TERMINAL no corrió nunca en v1; en `generaciones` corre en la
   pista v2, que es otra pregunta).
Descartados, con la razón: reescribir F9-4 con otra lectura (sería recalibrar después de ver datos, regla 2); "la boca lee las
dos filas" (fase 10 externa: el veto hunde al inmortal, R0 1.154 → 0.045); generaciones que conviven (la corre el coordinador ahora).

## 1. Hipótesis
- **H-SI (estado propio):** el cruce de O3 depende de leer su estado **actual**: si toda decisión lee el (E, Ag) de un paso pasado
  al azar (misma distribución de estados propios, otro momento), el linaje deja de cruzar y de persistir.
- **H-RES (reserva del linaje):** la muerte programada de O3 funciona porque espera a que la reserva del linaje sea ≥ 4; si muere
  en cuanto lleva 2 partos, sin leer la reserva, el linaje persiste menos o deja de ganar.
- **Contexto H-TERM:** sin muerte programada (CTRL_O3_SINTERM) en v1, ¿sigue ganando? (no decide el veredicto; ver §6).

## 2. Mecanismo mínimo y memoria nueva
Ningún mecanismo nuevo: son **lesiones** (instrumento), memoria nueva cero en el organismo.
- `O3_LES_SI`: un anillo de los últimos 2000 (E, Ag) del linaje y un sorteo por paso del rng de cuerpo que la pista le da al carro
  (O3 nunca lo sortea; el mundo, los hijos, las muertes y el turno tienen sus propios rng). La física usa el (E, Ag) verdadero.
- `O3_TERM_CIEGO`: una constante (`COLA_TERM = 4 → 0`), sin rng.
- `CTRL_O3_SINTERM`: una constante (`TERMINAL = False`); mismo sha que el control de `generaciones` (7bb2fff33017e559).
- L-COLA (cola del linaje sorteada paso a paso) **se construyó y se descartó** por el arnés antes de cualquier humo: la muerte
  programada parpadea y cae a 0.33 de la tasa real (chequeo (M)); queda en el instrumento con la perilla apagada, no corre.

## 3. Instrumento y anclas
- Pista y juez de la ronda 2 (solo se importan): `pista.py` 9f47c65e438e0ff4, `juez.py` 6a68f640a7832f12, `revisa_carro.py`
  1c8a789f7427ab96, `organismo_f9c.py` 9dd1fb91ecec35ae. Los carros se cargan desde `subida_n9/carros/` (P.CARROS).
- `construye_n9.py`: anclas en bytes sobre `carrera_escuderias/carros/O3.py` (0442c2884fcb0e11). Carros: O3 (copia, mismo sha),
  O3_LES_OFF c404f52b6210066f, O3_LES_SI b1d2f442db838a34, O3_LES_COLA 05be23a6fad273a8 (descartado), O3_TERM_CIEGO
  853d5c8b53952253, CTRL_O3_SINTERM 7bb2fff33017e559, FABRICA 2ebee3e99ea5a33a (copia, sólo para la identidad corta del juez).
- Arnés `identidad_n9.py`: **22/22** (salida en `identidad_n9_salida.txt`): shas, construcción reproducible, chequeo estático,
  identidad corta del juez, **O3_LES_OFF == O3 bit a bit** en toda la salida de `pista.run` (3 monocultivos + 1 mixta, T = 12000,
  fundador limpio, TERMINAL disparado 49 veces), lesiones no inertes, marginal de L-SI igualada (E 0.976 usada / 1.012 real;
  Ag 1.043 / 1.077).
- Letra que decide: la de la ronda 2 sin cambios. ENMIENDA 5: un linaje-semilla cruza con R0 de nacimientos reales ≥ 0.90,
  ≥ 5 muertes y 0 fundadores tras t = 10000; el brazo cruza en una semilla si cruza la mayoría de sus 9; **gana** con ≥ 15/20.
  ENMIENDA 6: persiste = 0 fundadores tras t = 10000 y ≥ 5 nacimientos reales; estabiliza con > 1/2 por semilla en ≥ 15/20.
- Mundo: monocultivo de 9, pista escalada (L = 360, 36 objetos), fundador limpio, T = 100000, pizarra encendida (nadie escribe).

## 4. Predicciones firmadas (creador, antes del humo)
| código | predicción | probabilidad |
|---|---|---|
| P1 (ancla) | O3 gana la ENMIENDA 5 (≥ 15/20), R0 real eval mediana en [0.95, 0.99], persisten ≥ 170/180 | 0.85 |
| P2 | O3_LES_SI: R0 real eval mediana en [0.55, 0.88], cruza por mayoría en ≤ 5/20, persisten ≤ 60/180 | 0.60 |
| P3 | O3 persiste más que O3_LES_SI en ≥ 17/20 semillas (pareado) | 0.75 |
| **P4 (puede fallar)** | **O3_TERM_CIEGO PIERDE contra O3 (§5). La doy por REFUTADA con p 0.55: creo que morir a los 2 partos, con ≥ 2 hijos ya en la cola, no extingue al linaje y la métrica de R0 real no lo castiga** | 0.45 |
| P5 | O3_TERM_CIEGO muere más: mediana de muertes por linaje-semilla ≥ 1.2× la de O3 | 0.80 |
| P6 | CTRL_O3_SINTERM: 100–175 de 180 linajes-semilla evaluables (≥ 5 muertes) | 0.55 |
| P7 | CTRL_O3_SINTERM: R0 real eval mediana ≥ 0.90 | 0.50 |
Base de las cifras: O3 en 9101–9120 y 9121–9140 (R0 real 0.968 / 0.968; 178/180; 20/20); arnés s13392, T = 12000: muertes de
los 9 linajes O3 25, O3_LES_SI 108, O3_TERM_CIEGO 41 (no es serie).

## 5. Qué significa "pierde" (fijado antes)
Un brazo lesionado X **pierde** contra O3 en una serie si (a) O3 gana la ENMIENDA 5 y X no, **o** (b) O3 persiste en ≥ 15
linajes-semilla más que X (de 180; con p ≈ 0.2–0.4 por linaje la sd de la diferencia es ~8–9, la misma tolerancia de `generaciones`).
Se reporta al lado, sin decidir: R0 real pareado por semilla, descendientes, muertes, causas, fracción que muere sin parir.

## 6. Criterio (por la letra; serie 13301–13320 Y réplica 13321–13340 con el mismo veredicto)
- **NO EVALUABLE:** O3 no gana la ENMIENDA 5 en la serie (el ancla falla): no se lee nada.
- **FUNCIONA:** O3_LES_SI pierde **y** O3_TERM_CIEGO pierde, en las dos series.
  Vocabulario: *"el linaje que cruza H-1 lo hace leyendo su propio estado actual y la reserva de su linaje: con la misma
  distribución de estados pero del momento equivocado deja de cruzar, y si muere sin mirar la reserva persiste menos"*.
- **HAY ALGO MODESTO:** pierde sólo una de las dos lesiones, en las dos series. Se dice cuál.
- **NO:** ninguna pierde en las dos series (o no repiten): el cruce no depende de leer el estado propio ni la reserva; lo que
  sostiene al linaje es la estructura de la política escrita a mano.
- CTRL_O3_SINTERM **no decide**: si gana igual que O3, se agrega *"en la pista v1 la muerte programada no hace falta para cruzar"*;
  si no gana por casi inmortal (ERR-99), *"sin muerte programada el cuerpo casi no muere y la métrica no lo puede evaluar"*.
Prohibido: "sabe que va a morir", "quiere", "se sacrifica", "coopera", "población", "evoluciona", "el organismo aprendió su
modelo de sí" (la política de O3 la escribió un LLM; lo que se mide es si LEERSE es causal, no si lo aprendió).

## 7. Qué lo refuta
H-SI: O3_LES_SI no pierde (gana la ENMIENDA 5 y persiste a menos de 15 de O3). H-RES: O3_TERM_CIEGO no pierde. Instrumento:
coherencia física < 100 %, reconstrucción de t_fund < 100 %, escrituras en la pizarra > 0, o la mini identidad del runner falla.

## 8. Semillas (nuevas; verificado con grep en bundle, carrera, convive, aprende, criterio, escuela, exploracion, fanin, sandbox,
subida_n6, subida_n10: 133xx no aparece como semilla en ningún .md/.py/.log ni en nombres de archivo)
Serie **13301–13320** · réplica **13321–13340** · humo **13391** · arnés **13392–13394** · mini identidad del runner **13399**.

## 9. Puntos del nivel (propuesta; decide el director)
- FUNCIONA: +10 sobre lo que el director fije (50 → 60, o 65 → 70 si acepta la propuesta de la carrera): primera evidencia
  causal de un modelo de sí (estado propio + reserva del linaje) en el linaje que cruza H-1.
- HAY ALGO MODESTO sólo con H-SI: +3 a +5 (H-SI solo es lo esperable de una política que lee su estado; poco informativo).
- HAY ALGO MODESTO sólo con H-RES: +5.
- NO: 0, y recomiendo que la propuesta de 65 % baje a 55 %: el cruce sería de la política escrita a mano, no de un modelo de sí.

## 10. Enmienda 1 — **ERR-114** (tras el humo 13391, ANTES de cualquier serie; toca la LECTURA de H-SI, no una puerta ni una predicción)
En el humo (T = 12000) los linajes de O3_LES_SI mueren rápido y cada fundador limpio empieza con el anillo vacío: los estados
pasados que lee quedan por debajo de los reales (E 0.795 usada / 0.944 real; Ag 0.754 / 0.856). En el arnés (s13392) estaban
igualados (0.976 / 1.012). Por eso la frase "misma distribución" no está garantizada en el régimen de colapso.
Condición **V-M** (se imprime, no decide): si |media usada − media real| ≤ 0.10 en E y en Ag, H-SI se lee *"estado propio de
otro momento, con la misma distribución"*; si no, *"estado propio desfasado y sesgado hacia estados anteriores"*.
Tope 0.10 = el doble del arnés. Un primer tope de 0.15 quedaba justo encima del valor del humo (0.149), así que se descartó
por estar ajustado al dato. Con 0.10, el humo imprimiría "NO se cumple". Las predicciones P1–P7 y el §5–§6 no cambian.
