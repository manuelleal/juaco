# PREREGISTRO — PELDAÑO 1 DE LA ESCALERA: MEMORIA DE LUGAR (O1_LUGAR en el mundo con oasis: vista 20, pobre 0.5, dens 0.5), CONFIRMATORIO (30-sep-2026; con los cambios por auditoría ANTES de datos, sec. 12)

Misión: llegar a la AGI por este camino (organismo mínimo con reglas locales, sin retropropagación, peldaños preregistrados con controles y
réplicas). Encargo del director (30-sep, "LA ESCALERA", modo ráfaga). Ingeniero genético: Fable. Plan completo: `ESCALERA.md`.
**Escrito DESPUÉS de dos humos y una exploración de un proceso (sec. 11, todo en `BITACORA.md`, nada declarado) y ANTES de cualquier dato de serie.**
La letra (sec. 6) es la que `corre_p1.lee_serie` traía desde el primer humo (V1–V4, PA, PB, PM, umbrales 13/20 y +10, ratio ≥ 2): los humos no la
movieron; lo que cambió entre el humo 1 y el humo 2 fue el MUNDO y un gancho del módulo (sec. 2 y 11), y se dice. ERR abiertos por la auditoría antes de datos: ERR-170 (control con fuga) y ERR-171 (texto: sesgo del ganador y vocabulario), sec. 12. Siguiente libre: ERR-172.

## 0. Qué es y qué no es
Es DISEÑO dirigido ("ingeniería genética"): el ingeniero pone en O1 un módulo (memoria de lugar) con un promotor, y pone en la pista una perilla de
mundo (oasis) que hace que recordar dónde pague. NO es selección natural: nadie "evolucionó" nada. Lo que se pregunta es si un organismo que ya vive
(O1) sube un peldaño operacional —pasar más tiempo en un sitio que no ve porque allí le fue mejor— y si eso le paga en la moneda del juez (linajes
que cruzan) **en el mundo con oasis (vista 20, pobre 0.5, dens 0.5)**, contra un control que lleva el mismo sesgo con el lugar equivocado.
**Alcance (ERR-171):** todo lo que se declare vale sólo en ese mundo: `lug` contra `o1` y contra `bar` allí. NO se compara con el muro de la pista
vieja (136/180, R0 0.93 de O1): es otro mundo, con otra visión y otra comida. V2 (`o1f`) valida el runner y la cadena de identidad, no el mundo.
**Sesgo del ganador (ERR-171, declarado):** el mundo (dens, vista) y el gancho de viaje se eligieron en ráfaga HASTA que `lug` ganó en 2 semillas
(sec. 11), y las predicciones Q se calibraron sobre esas 2 semillas; la serie va en 20 semillas nuevas y la réplica en otras 20. Después (P1-evo, otro preregistro) la selección podrá afinar el promotor como gen.

## 1. Pregunta
En la pista con oasis (sec. 3), ¿O1 + memoria de lugar (`lug`) cruza más (R0 real ≥ 0.90 y 0 fundadores tras t = 10 000) que O1 (`o1`) y que O1 con
la misma memoria leída en un sitio permutado (`bar`), y lo hace yendo al oasis (mecanismo desde la física)?

## 2. Mecanismo y memoria nueva (carro `O1_LUGAR`, `construye_p1.py`, por anclas desde `carrera_escuderias/carros/O1.py` sha `99436afa2715f028`)
- **Memoria de lugar del linaje:** 30 bins del anillo (L/30 = 12 celdas) × 2 necesidades = lo que ESE sitio dio DE MÁS (o de menos) que lo que su letra
  da en promedio. Regla local, en `resultado()`, antes de actualizar la tabla por letra: `lugar[bin] += 0.5·((dS − valor_medio(letra)) − lugar[bin])`
  (la primera mordida de una letra no enseña). Memoria nueva: 60 floats + 30 conteos por instancia. Es del linaje como la tabla de O1 (viaja en
  `al_parir`/`nace`; el fundador limpio nace vacío).
- **Uso 1 (valor):** en `actua` y `_quiere`, el valor esperado de un objeto en x = valor(letra) + `LUGAR_W`·bono(x), bono = la parte de la memoria del
  bin que supera 0.05, sólo en necesidades donde la letra ya vale > 0 y sólo si la letra no daña. `LUGAR_W` = 1.0.
- **Uso 2 (viaje, `LG_VIAJA` = 1, agregado tras el humo 1):** cuando O1 no tiene blanco a la vista (hoy va al "hueco" entre los otros cuerpos), va al
  centro del bin recordado con más bono por distancia (`s/(d + D0)`). Si ningún bin recuerda nada, hace lo de O1.
- Nada más de O1 cambia (urgencia, distancia, PEN_OTRO, limpieza, pruebas, partos). Con `LUGAR` = 0 el carro es O1 bit a bit (salida entera); con
  `LUGAR` = 1, `LUGAR_W` = 0 y `LG_VIAJA` = 0 también; y con `LUGAR` = 1 en la pista SIN oasis también (ningún sitio da más que su letra: bono 0 exacto).
- **Control de contenido `O1_LUGAR_BAR` (ERR-170):** escribe en el bin verdadero y LEE (valor y viaje) en el bin ANTÍPODA FIJO (b + 15 mod 30):
  mismo sesgo de moverse, SIEMPRE el lugar equivocado (el oasis son 4 bins contiguos de 30; el antípoda nunca lo toca). Sin rng: determinista como O1.
- Los tres carros pasan el chequeo estático `revisa_carro` (no leen rng del mundo ni tabla verdadera).

## 3. Mundo (`mundo_escalera.py`, por anclas desde `pista.py` `9f47c65e438e0ff4`; `juez.py` `6a68f640a7832f12`; 9 anclas)
Pista de la carrera (monocultivo de 9, L 360, 36 objetos, fundador limpio 1, pizarra 1, T 100 000; cada corrida ES `corre_v143.tarea`, regla 14) con:
- `oasis = 1`: un arco del 10 % del anillo (36 celdas), inicio sorteado por semilla con rng nueva `[seed, 0, 18, 0]` (la misma fórmula que
  `pista_grande`: con `extra 0.8, pobre 1.0, dens 0, vista_r 0` este mundo ES `pista_grande(G1, rica1, lento0)` en toda la física, arnés (M)).
- Dentro: A → (+0.8, +0.8), C → (+0.8, +0.8) (`extra` 0.8). Fuera: A y C valen `pobre` = 0.5 de su efecto. B y D no cambian.
- `dens = 0.5`: la mitad de lo que el mundo repone nace dentro del oasis (allí crece la comida: el oasis es ~5× más denso que el resto).
- `vista_r = 20`: VISTA PARCIAL: el carro sólo recibe los objetos a ≤ 20 celdas (la pista original entrega todos; kwarg `vista_r` porque `vista`
  ya es un local de `pista.run`). Nadie recibe la posición del oasis.
- Con `oasis = 0` es `pista.run` bit a bit (arnés M1; el brazo `o1f`).
- **Por qué este mundo paga la capacidad y evitar no es gratis:** con visión parcial y reposición uniforme (humo 1) el oasis no se ve y no vale
  ir (O1 muerde lo que ve; el que viaja pierde); con oasis denso y vista corta, quien no recuerda dónde está vaga (al "hueco") y muere de hambre
  entre comida pobre (O1: vida mediana 200, ~100 refundaciones por linaje en la exploración); quien recuerda vuelve. Es el primer mundo del proyecto
  en que una capacidad de O1 que no tenía vale la vida del linaje.

## 4. Brazos
| brazo | carro | mundo | qué es |
|---|---|---|---|
| `lug` | O1_LUGAR (`49eee6bb278ea097`) | oasis | CANDIDATO |
| `bar` | O1_LUGAR_BAR (`93fc245b8db8794b`) | oasis | control de CONTENIDO (antípoda fijo, ERR-170): mismo sesgo de moverse, siempre el lugar equivocado |
| `o1` | O1 (`99436afa2715f028`) | oasis | la BASE sin memoria de lugar |
| `o1f` | O1 | pista lisa (`oasis 0`) | ANCLA de validez (V2): la pista de siempre, donde O1 cruza 18–20/20 |
(`O1_LUGAR` en la pista lisa == O1 bit a bit por el arnés: no hace falta brazo de "costo sin oasis".)

## 5. Medidas
- **Principal:** linajes que cruzan (`cruza_real` del juez), por semilla (0–9) y suma (de 180). Pareado por semilla, empates EN CONTRA.
- **Mecanismo (física del mundo, no del carro):** fracción de pasos DENTRO del oasis / 0.10 (1.0 = al azar) por brazo; fracción de mordidas A+C
  dentro / 0.10.
- Descriptivos: R0 real mediano, establecidos (0 fundadores tras 10k), fundadores por linaje, vida mediana, mundo A+C, mordidas A+C y B+D,
  telemetría del carro (blancos con bono, viajes, bins con bono dentro del oasis: no puntúa).

## 6. LA LETRA (`corre_p1.lee_serie`; casos sintéticos en el arnés (f), 7 casos)
**Validez (si una falla: NO SE LEE):**
- V1: serie completa (20 semillas × 4 brazos), 0 abortos, contabilidad física coherente.
- V2: `o1f` con mayoría de linajes que cruzan (≥ 5/9) en **≥ 16/20** (binomial con p 0.90: P(X ≤ 15) = 0.043; histórico 18–20/20).
- V3: el mundo actúa: en toda corrida con oasis, mordidas A+C dentro > 0 y `extra` 0.8, `pobre` 0.5 escritos; en `o1f`, sin oasis.
- V4: estado escrito por cada worker: carro y mundo correctos por brazo; `LUGAR` 1, `LUGAR_W` 1.0 en `lug` y `bar`; `LUGAR_BARAJA` 1 sólo en `bar`.
**Puertas (con su nulo, regla 15):**
- PA-par: `lug` > `o1` en linajes que cruzan en ≥ 13/20 semillas. PA-suma: suma(`lug`) ≥ suma(`o1`) + 10.
- PB-par: `lug` > `bar` en ≥ 13/20. PB-suma: suma(`lug`) ≥ suma(`bar`) + 10.
- Nulo: con empates en contra y p = 0.5 por semilla, P(X ≥ 13 de 20) = **0.132**; la suma +10 (de 180) y la réplica en semillas nuevas lo bajan
  (dos series independientes a 13/20: 0.017). **PB es la puerta que DECIDE el peldaño:** PA casi no discrimina porque `o1` cruza ≈ 0 en este
  mundo (exploración: 0/18), así que cualquier cosa que se mueva le gana; sólo PB separa el contenido (dónde) del sesgo (moverse).
- PM (mecanismo): mediana de semillas de la razón de pasos dentro del oasis de `lug` ≥ 2.0, y la de `o1` en [0.6, 1.5].
**Veredictos:** FUNCIONA = V1–V4 y PA (par y suma) y PB (par y suma) y PM. HAY ALGO MODESTO = no FUNCIONA, y (PA-par o PA-suma) y (PB-par o
PB-suma) y PM. NO = lo demás; si gana sin PM → "NO (gana sin ir al oasis: instrumento)" y se audita. EN EL UMBRAL: cualquier pareado a ±1 de 13 o
cualquier suma a ±1 de 10. Bloque serie + réplica: si coinciden vale ése; si no, el menor; NO SE LEE manda.

## 7. Regla de parada y vocabulario
- Réplica (semillas 739101–739120) sólo si la serie da FUNCIONA, MODESTO o NO en el umbral; el runner lo exige (candado) y exige el mismo sha del runner.
- FUNCIONA ×2 → "en el mundo con oasis (vista 20, pobre 0.5, dens 0.5), O1 con memoria de lugar pasa más tiempo en el oasis que no ve y eso
  establece al linaje donde O1 no se establece; el control que lee el antípoda no lo hace". Prohibido: "sabe dónde está", "vuelve", "planifica",
  "mapa cognitivo", "piensa", y cualquier comparación con el muro de la pista vieja.
- MODESTO → se registra, no se repite. Si PB cae (lug ≈ bar) el peldaño es NO por la letra: no hay lectura de rescate ("paga moverse") en este
  preregistro; lo que paga moverse ya se midió como fuga del control viejo (ERR-170: la permutación por instancia leía bien algún bin del oasis
  en ~45 % de las instancias, razón de pasos 3.5 en la exploración) y por eso el control se cambió al antípoda ANTES de datos.
- NO SE LEE no tiene salida por esta letra (semillas nuevas y preregistro nuevo).

## 8. Predicciones firmadas (antes de la serie; calibradas con la exploración de 2 semillas, sec. 11, declarado)
| # | predicción | rango | p |
|---|---|---|---|
| Q1 | `o1` en el mundo con oasis: suma de linajes que cruzan | [0, 25] de 180 | 0.80 |
| Q2 | `lug`: suma | [50, 120] | 0.70 |
| Q3 | `bar` (antípoda): suma | [0, 40]; dentro de ±15 de `o1` | 0.60 |
| Q4 | V2 (`o1f` ≥ 16/20) | | 0.90 |
| Q5 | PA (par ≥ 13/20 y +10) | | 0.85 |
| Q6 | PB (par ≥ 13/20 y +10) | | 0.75 |
| Q7 | PM: razón de pasos de `lug` mediana en [4, 9]; `o1` en [0.9, 1.3]; `bar` en [0.8, 2.5] (ya no lee el oasis) | | 0.75 |
| Q8 | `lug` no pela el mundo: mundo A+C de `lug` ≥ 0.9 × el de `o1` | | 0.75 |
| Q9 | establecidos (0 fundadores tras 10k, de 180): `lug` ≥ 100, `o1` ≤ 30 | | 0.65 |
| V | veredicto de la SERIE: FUNCIONA / MODESTO / NO / NO SE LEE | | 0.58 / 0.17 / 0.15 / 0.10 |

(Fila V y Q3/Q6/Q7 originales, escritas con el control permutado: Q3 [15, 70] > o1 p 0.65; Q6 p 0.60; Q7 bar [2, 5] p 0.80; V 0.50 / 0.22 / 0.18 / 0.10. Se conservan como registro; cambiadas en sec. 12 porque el control cambió, antes de datos.)

## 9. Las cuatro trampas
- **Canal simétrico:** no hay canal; O1 no lee ni escribe la pizarra. Nada viaja entre linajes.
- **Acierto sin balancear:** la medida es `cruza_real` del juez y la fracción de pasos dentro (física), no un acierto del carro.
- **Mundo que se come la comida:** con 9 cuerpos yendo al oasis, el oasis se puede pelar; `dens` 0.5 lo repone. Se reporta mundo A+C por brazo
  (Q8) y mordidas; si `lug` gana pelando el mundo, se dice. En la exploración: A+C 7.3 (`lug`) contra 7.0 (`o1`): no pela.
- **Sitios fijos:** el oasis se sortea por semilla (rng propia); semillas nuevas 739001–739020; posiciones y turno del rng de la pista.

## 10. Instrumento, semillas, costo, comandos
- Runner `corre_p1.py` (`--humo`, `--explora`, `--serie --pool ≤ 2`, `--replica`, `--lee`, `--reanuda`); JSON por trabajo (ERR-54), `fija()` en cada
  worker escribe el estado (V4); candados: se niega con veredicto previo, réplica sólo por la regla de parada, `git` limpio de preregistro, runner,
  constructor, mundo y carros. Cada corrida ES `corre_v143.tarea` (arnés (a), regla 14) con `mundo_escalera.run` en lugar de `pista.run`.
- Arnés `identidad_p1.py` → `identidad_p1_salida.txt`: **ARNES PASA 37/37** (ver la salida; con los carros finales de la sec. 12): mundo oasis 0 == pista bit a bit (y rng); mundo == pista_grande
  con extra 0.8 pobre 1.0; O1_LUGAR0 == O1; módulo mudo (W 0, viaja 0) == O1; O1_LUGAR sin oasis == O1; controles que difieren; mecanismo: los bins
  con bono caen TODOS dentro del oasis; regla 14; reanuda; letra sintética; guardas.
- **Semillas NUEVAS 739xxx** (grep 30-sep: no aparecen en .py/.md): serie 739001–739020; réplica 739101–739120; humo 739990–739991; exploración
  739201–739202 (usadas, sec. 11); arnés 739950–739954, 739960.
- **Costo medido** (un proceso, T 100k, exploración): `lug` 107–148 s, `bar` 111–151 s, `o1` 59–68 s; `o1f` (visión global) ≈ 180 s. Por semilla ≈
  500 s → serie ≈ 2.8 h CPU → **≈ 1.4 h con pool 2**; réplica igual.
```
python experimentos/organelos/escalera/construye_p1.py --verifica
python experimentos/organelos/escalera/identidad_p1.py
python experimentos/organelos/escalera/corre_p1.py --serie --pool 2 2>&1 | tee experimentos/organelos/escalera/serie_pool2.log      # coordinador
python experimentos/organelos/escalera/corre_p1.py --replica --pool 2 2>&1 | tee experimentos/organelos/escalera/replica_pool2.log  # sólo por sec. 7
python experimentos/organelos/escalera/corre_p1.py --lee <carpeta>
```

## 11. Historia honesta (ráfaga; NADA de esto cuenta; `BITACORA.md`)
1. **Humo 1** (739990–739991, T 30k; mundo `dens 0, vista_r 0`; carro sin viaje, sha `18a9604d5b76d97e`): **señal NO**. La memoria encontró el oasis
   (100 % de los bins con bono dentro) pero el cuerpo no fue (razón de pasos 1.01 = O1 1.09) y cruzó menos (1 / 4 / 5). Diagnóstico: con visión
   global un A visible a 10 celdas siempre gana al oasis a 60 (descuento 1/(d+3) de O1) y con reposición uniforme el oasis es una piscina chica.
   **Predicción implícita refutada** (que el bono en el valor bastaría).
2. **Cambios ANTES del humo 2** (diseño, no recalibración de la letra): mundo `dens` 0.5 y `vista_r` 20; módulo `LG_VIAJA` (sin blanco a la vista,
   viajar al sitio recordado). Arnés rehecho: 36/36.
3. **Humo 2** (mismas semillas, T 30k): nadie cruza (T corto) pero el establecimiento separa: establecidos 12 / 5 / 4, R0 0.54 / 0.14 / 0.31,
   razón de pasos 6.0 / 1.9 / 1.05. Señal (establecimiento).
4. **Exploración** (739201–739202, T 100k, un proceso): cruzan **lug 8 / bar 4 / o1 0** (de 18), pareado 2/2 contra ambos; establecidos 16 / 6 / 1;
   R0 real 0.84 / 0.63 / 0.31; fundadores por linaje 18.5 / 84.6 / 105; vida 1371 / 600 / 200; razón de pasos 7.5 / 3.5 / 1.06; mundo A+C 7.3 /
   6.1 / 7.0. **Hallazgo:** `bar` le gana a `o1`: moverse más ya paga en este mundo (el control captura eso); el contenido paga por encima (`lug` > `bar`).
   Por eso PB es la puerta que decide el peldaño. **Auditoría (ERR-170): ese `bar` tenía fuga** (leía bien algún bin del oasis en ~45 % de las
   instancias): sus 4 cruces y su 3.5 de razón de pasos NO miden sólo "moverse más". El control de la serie es el antípoda (sec. 2 y 12).
5. Lo que NO se sabe: cuánto cruza `bar` con el antípoda (Q3); si `o1f` en la pista lisa sigue en ≥ 16/20 con este runner.

## 12. Cambios por auditoría antes de datos (30-sep) — ERR-170, ERR-171
Auditor: LISTO CON CAMBIOS; aplicados ANTES de cualquier dato de serie (sólo había humos y una exploración, que no cuentan). Ningún número de la letra (sec. 6) cambió.
1. **ERR-170 (instrumento: control con fuga).** El control `bar` leía la memoria en un bin PERMUTADO al azar por instancia (rng del cuerpo). Con 4 bins
   de oasis en 30, una permutación deja algún bin del oasis leyéndose bien con probabilidad ≈ 0.45 por instancia: `bar` dio razón de pasos 3.5 y
   4 cruces en la exploración en parte por eso. **Cambio:** `bar` lee el ANTÍPODA FIJO (b + 15 mod 30), que nunca toca los 4 bins contiguos del
   oasis; sin rng. Carros regenerados: O1_LUGAR `49eee6bb278ea097`, O1_LUGAR_BAR `93fc245b8db8794b`, O1_LUGAR0 `33a7ab0c66fe2b82`;
   `construye_p1.py` nuevo sha; arnés con un chequeo nuevo (lee [1, .5] del bin 20 en la celda del bin 5 y 0 en la del bin 20; `_lg_meta` apunta
   al antípoda). Sec. 7 reescrita: sin lectura de rescate "paga moverse". Predicciones Q3, Q6, Q7 y V revisadas (sec. 8) porque el control cambió;
   las originales se conservan escritas.
2. **ERR-171 (texto: sesgo del ganador y vocabulario).** Sec. 0 declara que mundo y gancho de viaje se eligieron hasta que `lug` ganó en 2 semillas
   y que Q se calibró sobre eso; todo el vocabulario queda acotado a "en el mundo con oasis (vista 20, pobre 0.5, dens 0.5)"; no se compara con el
   muro de la pista vieja (136/180, R0 0.93); V2 valida el runner, no el mundo; "vuelve al oasis" pasa a "pasa más tiempo en el oasis".
3. **Nulo de las puertas** (regla 15) escrito en sec. 6: 13/20 bajo azar P = 0.132; +10 y la réplica lo bajan; PB decide porque PA casi no discrimina.
4. **`corre_p1.py` CONGELADO** (sha final en el log del runner y en `resumen.json`): P7 lo importa sin editarlo (o copia a su propio módulo).
5. **ESCALERA.md** línea del arnés: 34/34 → el conteo actual del arnés re-corrido con los carros finales.
