# EXPLORATORIO, no es dato

# INFORME — ¿qué carga el efecto de boca_buena? (creador, 28-sep-2026)

Misión: llegar a la AGI por este camino. Diagnóstico, no candidato. Sin Pool, sin git. 140 corridas de un proceso, T 100 000, semillas
39001–39010 (hasta 6 procesos a la vez desde que el coordinador liberó el PC). Tablas: `python lee_bb.py` (copia en `tabla_bb.txt`).

**VEREDICTO: FUNCIONA como diagnóstico.** El efecto lo carga un **termostato de dos necesidades**: sobre lo bueno conocido, muerde si
sube ALGUNA necesidad que esté bajo una consigna S, y no muerde si todas las que sube están en S o encima, con **S estrictamente por encima
del umbral de parto**. La neofobia no aporta nada. Ninguna de las dos mitades basta sola. Poner la consigna en el umbral mata. Leer la
necesidad equivocada mata.

## 1. Qué decide boca_buena (O1P.boca sobre letras que O1 no sabe malas; `_quiere` + `_gana`)
- **Letra desconocida** (el linaje nunca la mordió): muerde si min(E, Ag) > 0.5 (PRUEBA).
- **Letra buena conocida** (dS medio sentido sin componentes negativas): muerde si alguna fila j con dS_j > 0 tiene nivel_j < rep_umbral
  + 0.25 (MARGEN). Si todas las necesidades que sube están en 1.25 o más, no muerde. Los pesos de urgencia (4/2/1) no cuentan aquí: la
  boca sólo mira si la ganancia es mayor que 0. Las letras con dS todo 0 nunca se muerden (no existen en esta pista).
- **Qué lee:** E y Ag propios, la tabla de dS sentido del linaje (la misma información que ya tiene `_adS` de v14.3) y rep_umbral.
  **No lee** cuál necesidad es la activa, ni el hambre, ni la distancia, ni a los otros cuerpos, ni el mundo.
- **Contra la boca de V143:** V143 decide con la fila de la necesidad ACTIVA (logit 1.2·w_activa + 2·hambre + 0.5, más FILTRO y APR).
  Por eso come lo bueno ya lleno (con ambas ≥ 1, pb ≈ 0.84) y rechaza a veces lo que sirve a la necesidad NO activa. En la telemetría,
  sobre lo bueno conocido, O1 veta el 63 % de lo que V143 mordería y fuerza el 2 % de lo que rechazaría: 2537 de 2836 casos en la
  franja [1.0, 1.25), y 1665 para la necesidad no activa.

## 2. Por qué GLOTU no lo captura (y el arnés lo confirma)
GLOTU, puesto dentro del híbrido (`bb_glotu`), es **V143_GLOTU bit a bit** (arnés (3)). Aquí da **0.754** (la serie dio 0.736).
Diferencias:
- (a) **Consigna en el umbral.** GLOTU veta desde 1.0, y eso deja caer la necesidad bajo 1.0 antes de comer, lo que rompe la ventana
  de 500 pasos. La versión pura de esa consigna (`m0`) da **0.000 en 10/10 semillas, con 0 linajes establecidos**, aunque tiene la mayor
  cantidad de pasos viables (54 k): nunca junta 500 pasos seguidos.
- (b) **No fuerza.** GLOTU nunca hace comer lo que V143 rechaza para la otra necesidad.
- (c) **Condición relativa** ("la más llena"). Con las dos necesidades altas, la menos llena sigue comiendo de más.
- (d) No tiene neofobia, pero eso no importa (§3).

## 3. Ablaciones (mediana del R0 real; entre paréntesis, semillas con mayoría de linajes que cruzan; 10 semillas salvo donde se indica)
| brazo | qué es | R0 | cruzan | gana a V143 | A+C / B+D por linaje |
|---|---|---|---|---|---|
| v143 | base | 0.413 | 0/10 | – | 811 / 558 |
| ref | boca_buena exacta del puenteo | **0.928** | 8/10 | 10/10 | 488 / 260 |
| sinprueba | sin neofobia (lo desconocido lo decide V143) | **0.935** | 9/10 | 10/10 | 497 / 261 |
| soloprueba | sólo neofobia | 0.397 | 0/10 | 5/10 | 810 / 586 |
| vetoc | O1 sólo dice NO (sobre lo conocido) | 0.824 | 2/10 | 10/10 | 530 / 303 |
| fuerzac | O1 sólo dice SÍ (sobre lo conocido) | 0.777 | 2/10 | 8/10 | 739 / 480 |
| todo | sin consigna: muerde todo lo bueno conocido | 0.895 | 5/10 | 9/10 | 758 / 514 |
| m0 / m10 / m40 | consigna U / U+0.10 / U+0.40 | **0.000** / 0.921 / 0.951 | 0 / 7 / 6 de 10 | 0 / 10 / 10 | 339 / 414 / 608 A+C |
| ventana (6 sem.) | consigna = lo que falta para cerrar la ventana | 0.822 | 1/6 | 5/6 | 579 / 337 |
| tinv (6) / tinv40 | CONTROL: consigna 0.25 / g/2 leyendo la OTRA necesidad | **0.000 / 0.106** | 0 / 0 | 0 / 0 | – |

Lectura:
- **"Comer para cualquier necesidad"** es la parte mayor: V143 0.41 → todo 0.90. Esto pasa aun con tantas mordidas malas como V143.
- **La consigna por encima de U** agrega el resto (0.92–0.95) y reduce a la mitad lo malo mordido (menos comida gastada, más meta).
- **La banda que funciona es ancha:** S de 1.1 a 1.4 da 0.92–0.95. En 1.0 es letal, y sin consigna (1.5) da 0.895.
  **El 0.25 de O1 no es mágico.**

## 4. Propuesta para el coordinador (UNA principal; formato fijo)
**PRINCIPAL (la que recomiendo): TERMO = V143 + una pieza de boca.**
- **Hipótesis:** a v14.3 le falta un termostato por necesidad, con consigna sobre el umbral de parto.
- **Mecanismo:** sobre la letra k con `_adS` medio s, sin componentes < 0 y con alguna > 0, muerde ⇔ ∃ j: s_j > 0 ∧ nivel_j < rep_umbral +
  s_j/2 ("no comas si ya tienes media mordida por encima del umbral de parto"). Esta decisión manda sobre la boca, FILTRO y APR de V143
  para esas letras. En lo desconocido y lo malo, V143 queda tal cual.
- **Memoria nueva: cero.** `_adS` y rep_umbral ya están.
- **La constante ½ se declara.** No es de O1: en esta pista da 1.4, y 1.1–1.4 funciona igual.
- **Instrumento:** construir por anclas desde V143.py (2a03048a7f1525e5). **Ancla fuerte:** V143_TERMO == `HIBB` BB='m40' en la física,
  bit a bit, como ya pasa con glotu (arnés (3)).
- **Control desfasado:** TERMOINV, la misma regla leyendo el nivel de la necesidad que la letra NO sube (`tinv40`: 0.106 aquí). Puede fallar:
  si lo que importara fuera sólo cuánto se come, TERMOINV también subiría.
- **Predicción** (letra del muro):
  - R0 mediana en [0.88, 0.97];
  - gana a V143 en ≥ 18/20;
  - semillas con mayoría que cruza, 11–17/20;
  - TERMOINV ≤ 0.25 (0/20).
- **Probabilidades honestas:** FUNCIONA (serie + réplica) **p 0.30**; HAY ALGO MODESTO p 0.55; NO p 0.10; NO SE LEE p 0.05.
  - La tasa de "mayoría que cruza" de la banda es ≈ 0.75 (30/40), y m40 solo tiene 6/10. P1 exige ≥ 15/20 dos veces: con p = 0.75 eso es
    0.62 por serie y ≈ 0.38 las dos.
- **Qué lo refuta:** P1 < 15/20, o que TERMOINV cruce.
- **Riesgo de validez:** V143 dio 0.413 en 39001–39010, en el borde de V3 [0.40, 0.80].
- **Semillas nuevas:** serie 39101–39120, réplica 39121–39140, humo 39911–39912, arnés 39913–39914 (sin choques en el repo).

**RESPALDO (no lo recomiendo por encima de la principal):** la consigna S = U + ½·rep_X·costo (la mitad de lo que gasta la ventana).
- Es la más fuerte en lo exploratorio (≡ sinprueba: 0.935, 9/10).
- **Pero da 1.25, el número de O1.** Aunque la derivación es del mundo, a ojos del director es copiar. Decide el coordinador.

## 5. Declaraciones, errores de instrumento y predicciones refutadas
- **El sha del carro cambió** al agregar modos: de91208f → d4da3b85 → 16143f6d → 1c7adefc → (ab7c3280, construido a medias y sin corridas
  lanzadas contra él) → 3ca86aed. Cada vez re-pasó el arnés: **38/38 al final**, con (1) ref == HIB del puenteo, (2) todo en 0 == V143 y
  (3) glotu == V143_GLOTU. La física de los modos anteriores no cambió.
  - Las colas 8/9 cargaban el carro en cada corrida y pudieron tomar cualquiera de esos shas. En sus modos la física es la misma.
- **`veto` y `fuerza` quedaron confundidos con la neofobia:** con O1 decidiendo lo desconocido, la tabla nunca aprende lo que V143
  rechaza. Los reemplacé por vetoc/fuerzac y dejé marcadores `_omitido` en 39001–39003.
- La telemetría `bbt` cuenta sólo la última instancia de cada linaje.
- **m10/m40/ventana/tinv se eligieron DESPUÉS de ver los brazos base, en las mismas semillas.** La ventaja de m40 puede ser la maldición
  del ganador: por eso pido semillas nuevas.
- **Superé la regla 3 de EQUIPO** (≤ 6 corridas por humo), por encargo explícito del coordinador.
- **Refutadas:**
  - B4: fuerzac ≥ 0.85 (dio 0.777; vetoc 0.824);
  - B9: m40 ≤ 0.95 (0.951);
  - B10: ventana ≥ 0.85 (0.822);
  - B12: ≥ 8/10 con mayoría (6/10);
  - la lectura del puenteo "lo que carga es no comer de sobra": la parte mayor es comer para cualquier necesidad.
- **Se cumplieron:** B1, B2, B3, B5, B6, B7, B8, B11 y B13.
- **Arnés:** `identidad_bb.py` → ARNES PASA 38/38 (`identidad_bb_salida.txt`). **Humo:** 6 JSON (`humo_salida.txt`).
