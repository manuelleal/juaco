# Bloque 3d: la regla fusionada del trío para la vía lenta — `phi' + Ws con signo + decaimiento` (escrito ANTES de correr; semillas 41–60)

**17 sep 2026 (noche) / día 7.** El bloque 3 mostró que la vía lenta **cuadrática representa XOR** (`W_lenta(P0·P1) = −2.65`)
sin clasificar mejor; el 3b refutó que la culpa fuera la puerta (`familiar` 0.33; la vía lenta sola da 0.500) y dejó el
diagnóstico: **el límite es la REGLA de la vía lenta** (dos canales no negativos `Wps/Wns` + drenaje de la parte común,
que reparten cada error por igual entre todas las entradas activas de `phi`). El trío A/B/C (`registro/investigacion/PUENTE_xor.md`)
probó las tres piezas por separado y **las tres cayeron**: A (vector con signo sin regularizador) 0.250; B (`lam`, `clip_s`)
no mueven nada, 24 corridas; C (término constante solo) 0.375. Firmaron **una** propuesta: las tres juntas. Esto la
preregistra como hipótesis, no como resultado.

## Hipótesis
La vía lenta separa XOR en nunca vistos si y sólo si (a) la representación tiene **signo único** (para poder poner lo
negativo SOLO en el producto), (b) `phi` tiene **término constante** (sin él `(0,0)` vale exactamente 0 — prueba
algebraica de C, aceptada con la corrección de B: para `(1,1)` el argumento es empírico, no algebraico) y (c) hay un
**regularizador** que mantenga cerca de cero las 20 entradas no informativas sin aplastar el producto. Ninguna de las
tres basta sola (medido). La fusión es la apuesta.

## Instrumento (un solo archivo, por anclas, con identidad propia)
`construye_xor_3d.py` genera **`organismo_v13q3.py`** desde `organismo_v13q.py` (sha `0b59eb03858df3a8`) con anclas de
conteo exacto. Tres knobs; la vía rápida (Kenyon, división por conflicto de signo), la puerta y la boca **no se tocan**:

- `regla_lenta='dos_canales'` (por defecto, código original intacto) `| 'delta_signo'`:
  **`Ws = clip( Ws·(1 − lam_lenta) + eta_s·_ds·phi'(P) , −clip_s, +clip_s )`** en cada mordida — un solo vector con
  signo, decaimiento multiplicativo de TODO el vector, tope simétrico. `_ds` es el error residual de la vía lenta
  (`R − _ws` con `puerta`), el mismo del original. Un knob mal escrito (p. ej. `'delta'`, el nombre que usó A) levanta
  `ValueError`: no puede caer en silencio al brazo original.
- `constante=False | True`: `phi'(P) = concat(phi(P), [1.0])` → cuadrática 21→**22** entradas, lineal 6→**7**, random15 21→22.
- `lam_lenta = 0.002` (ver abajo). Inerte con `dos_canales`.
- Sonda de `fase2_en`: sigue dando `W_lenta_apriori` (con `delta_signo`, `Ws @ phi'`) y `familiar_apriori`, y **añade
  `Ws_apriori`** = el vector con signo VIGENTE EN LA SONDA (`Ws` si `delta_signo`, `Wps−Wns` si `dos_canales`). Es
  lectura pura. Lo pidió A tras el aviso de C: los pesos del `return` son los del final de `T`, no los de la sonda, y
  toda la mecánica de 3b/3c se leyó de los equivocados.
- **Identidad obligatoria (ETAPA 1 del runner, para el proceso):** con `regla_lenta='dos_canales', constante=False`,
  `organismo_v13q3` ≡ `organismo_v13q` en **todas las claves del original**, semillas 1–3, `xor01` y `px0`, lecturas
  `lineal` **y** `cuadratica` (12 corridas, T = 60 000). Si falla, el runner se para.
- **El gemelo compilado `organismo_v13q_rapido.py` NO vale para 3d** (no tiene los knobs): `corre_xor_3d.py` no ofrece
  `--rapido`. Recompilarlo es trabajo aparte, con su arnés.

## Decisión de `lam_lenta` — **0.002**, fijada ANTES de correr, con `T = 100 000`
C midió **~331 actualizaciones de la vía lenta antes de la sonda** (semilla 1, `xor01`, T = 100 000; 739 en el total).
El decaimiento debe regularizar, no borrar: fracción del vector que sobrevive a la sonda, `(1 − λ)^331` →
**λ = 0.001 → 0.72** (apenas regulariza: es casi el caso *sin* decaimiento de A, que dio 0.250) · **λ = 0.002 → 0.52** ·
**λ = 0.003 → 0.37**. C midió además el efecto sobre el producto: con λ = 0.03 el peso del producto en la sonda queda en
−0.11/−0.24 (borrado) y con λ = 0.002 en −1.24/−1.39 (sobrevive, contra ≈ −2.2 sin decaimiento). Se fija **λ = 0.002**:
es el único valor del rango firmado (0.001–0.003) que conserva ~la mitad del vector y más de la mitad del producto, y es
el único que alguien del trío corrió sobre la fusión. **`T` es parte de esta decisión** y también queda fijo en
**100 000** (λ está calibrado en unidades de actualizaciones, y el número de actualizaciones escala con `T`: a
T = 200 000 la misma λ dejaría ~0.25). `T = 100 000` es además el valor por defecto del proyecto (regla 6) y el de los
tres pilotos del trío. Sin barrido de λ: un barrido sería elegir el ganador después de ver los datos.

## Mundo y brazos (mundo de regla, 20 patrones de peso 3; `puerta = 3`, `eta_s = 0.015`, `T = 100 000`, semillas NUEVAS 41–60)

| brazo | `lectura` | `regla_lenta` | `constante` | para qué |
|---|---|---|---|---|
| **LINEAL** | lineal | dos_canales | False | v13 actual (referencia histórica) |
| **CUAD_2C** | cuadrática | dos_canales | False | bloque 3b re-corrido a este `T` (comparación pareada de Z1) |
| **CUAD_DELTA** | cuadrática | **delta_signo** | **True** | la regla fusionada del trío |
| **CUAD_DELTA_SIN_CTE** | cuadrática | delta_signo | False | ¿cuánto aporta el término constante? |
| **LIN_DELTA** | lineal | delta_signo | True | **control: la regla sola no basta** (sin el producto en `phi` no hay XOR posible) |
| **RANDOM15_DELTA** | random15 | delta_signo | True | **control de dimensión** (22 entradas sin el producto correcto) |

Reglas: `xor01`, `px0`, `azar`. **6 × 3 × 20 = 360 corridas** de T = 100 000 (+ 12 de identidad).

## Medidas (todas sobre los **nunca vistos**, en la sonda de `fase2_en`, antes de que los de test entren al mundo)
`acc` (signo del **valor total** a priori, balanceado comida/veneno — el test de `xor01` es 8 comida y 4 veneno, por eso
balanceado) · **`acc_lenta`** (signo de `W_lenta_apriori`: la **vía lenta sola**) · `ba` (conducta al primer encuentro,
balanceada; `None` si falta una de las dos clases) · `cobertura` (cuántos de los 10–12 de test se encontraron) ·
**mecanismo desde `Ws_apriori`**: `Ws(P0)` = índice 0, `Ws(P1)` = índice 1, `Ws(P0·P1)` = índice 6 (primer par (0,1)),
`Ws(cte)` = última entrada si `constante` — el producto **sólo** se lee en los brazos `cuadratica` (en `random15` el
índice 6 es un bit al azar y en `lineal` no existe: se reporta `None`, no un número inventado) ·
`clases_sin_morder` = cuántas de las 4 clases `P0P1` ∈ {00,01,10,11} recibieron **cero** mordidas antes de la sonda
(cota de muestreo de C, medida ahora **por semilla**).

## Criterios (escritos antes de correr; nada se recalibra después)
- **Z1 (la regla fusionada separa XOR):** CUAD_DELTA `xor01` **`acc_lenta` mediana ≥ 0.70** **y** > CUAD_2C **pareado
  ≥ 15/20**.
  **Cota de muestreo, escrita:** en 3 de cada 10 semillas el mundo deja una clase XOR entera **sin una sola mordida**
  antes de la sonda (medido por C en 10 semillas; `ntr = (4,4)` sobre 12 comida / 8 veneno). Ninguna regla local adivina
  el signo de una clase con cero ejemplos, así que ~6 de las 20 semillas tienen techo bajo por el MUNDO, no por la
  regla: por eso **mediana y no 0.75 por semilla**, y por eso el segundo criterio es **pareado** (las dos ramas comparten
  semilla y por tanto la misma partición, así que la cota se cancela en la comparación).
- **Z2 (controles que deben fallar):** LIN_DELTA `xor01` `acc_lenta` mediana **≤ 0.60** **y** RANDOM15_DELTA `xor01`
  `acc_lenta` mediana **≤ 0.60**. Si alguno sube, la regla nueva gana por algo que no es la estructura de `phi`
  (dimensión, o un artefacto de la regla) y Z1 no vale aunque pase.
- **Z3 (regresión):** CUAD_DELTA `px0` **≥ 0.65** y `azar` **∈ [0.35, 0.65]**, en **`acc` y en `acc_lenta`** (las cuatro
  condiciones). La regla nueva no puede romper lo que v13 ya hacía ni "acertar" en un mundo sin regla.
- **Z4 (mecanismo, en la sonda):** CUAD_DELTA `xor01`, **`Ws(P0) > 0`, `Ws(P1) > 0` y `Ws(P0·P1) < 0` a la vez en
  ≥ 15/20** semillas. Es la firma algebraica de XOR con sesgo negativo (`(1,0)`: `w0 + b > 0`; `(0,0)`: `b < 0`;
  `(1,1)`: `w0 + w1 + w01 + b < 0`). Z4 puede pasar con Z1 caído (representar no es clasificar: eso es justo lo que pasó
  en 3 y 3b) — se reportan por separado, nunca uno como prueba del otro.
- **Veredicto:** la regla fusionada funciona **sólo si Z1 ∧ Z2 ∧ Z3**. Z4 es lectura de mecanismo, no requisito.

## Predicción numérica (lo que se espera, con su procedencia)
| medida | predicción | de dónde |
|---|---|---|
| CUAD_DELTA `xor01` `acc_lenta` | **umbral de éxito 0.70**; expectativa honesta del piloto **0.31–0.50** | C corrió la fusión con λ = 0.002, T = 100 000, 3 semillas: 0.312 / 0.188 / 0.438 |
| CUAD_2C `xor01` `acc_lenta` | 0.375–0.50 | B a T = 100 000: 0.375 [0.31, 0.44]; 3b a T = 200 000: 0.500 |
| LINEAL `xor01` `acc` / `acc_lenta` | ≈ 0.44 / ≈ 0.375 | bloques 3 y 3b |
| LIN_DELTA, RANDOM15_DELTA `xor01` `acc_lenta` | 0.40–0.55 (deben quedar ≤ 0.60) | random15 = cuadrática = lineal en el bloque 3 |
| CUAD_DELTA `px0` `acc_lenta` | 0.90–1.00 | A (1.000), C (1.000 en las 3 semillas) |
| CUAD_DELTA `azar` | ≈ 0.50 | nadie lo corrió en esta familia: es control, no predicción fuerte |
| `Ws(P0·P1)` **en la sonda** | **−0.2 a −0.8** (todo el vector es pequeño en la sonda: `max|Ws| ≈ 0.65`) | humo, ver abajo. El −1.24/−1.39 de C es el peso **al final de `T`**, no el de la sonda |
| `Ws(P0·P1)` al final de `T` | −1.2 a −1.4 | C con λ = 0.002 (coincide con el humo: −1.356) |
| `clases_sin_morder ≥ 1` | ~6 de 20 semillas | C: 3/10 semillas |

**Z1 es una apuesta, no una extrapolación** y así queda escrito: las tres piezas por separado dieron 0.25–0.50 y la
fusión que C alcanzó a correr (3 semillas) dio 0.312. Se preregistra 0.70 porque es el umbral que haría de esto un
resultado; si sale 0.35 **se escribe 0.35 y se cierra la línea**, no se baja el umbral.

## Refutación (qué significa cada caída, decidido antes)
- **Z1 cae con Z2 y Z3 pasando** → o la **cota de muestreo** o la **regla**. Se registra **la curva**, preregistrada aquí
  para que no sea una excusa a posteriori: `acc_lenta` de CUAD_DELTA estratificada por `clases_sin_morder` (0 / 1 / ≥2),
  con mediana y rango de cada estrato y el número de semillas de cada uno. Se reporta **siempre**, pase o no Z1, y
  **no sustituye a Z1**: si el estrato "0 clases sin morder" llega a 0.70 pero la mediana global no, el resultado escrito
  es "la regla fusionada no alcanza en este mundo; en las semillas donde el mundo enseña las cuatro clases sí llega a
  X" — y el siguiente paso es **cambiar el mundo** (`ntr` balanceado por clase XOR), con preregistro nuevo y semillas
  nuevas, no bajar el criterio.
- **Z1 cae y `Ws(P0·P1)` está aplastado** (|·| < 0.5 en la sonda) → el decaimiento uniforme es el culpable (riesgo #1 de A,
  medido por C con λ = 0.03). Siguiente diseño: decaimiento **sólo de las entradas inactivas** en la mordida, o por
  entrada en proporción a su desuso. Se escribe como refutación de *esta* regla, no de la idea.
- **Z1 pasa pero Z2 falla** → no es la estructura de `phi`: sin hallazgo. **Z3 falla** → la regla nueva rompe la
  regresión: no entra al tronco aunque Z1 pase.
- **Z4 pasa con Z1 caído** → se repite el hallazgo de 3/3b un nivel más adentro ("representa y no clasifica"), ahora con
  los pesos correctos (los de la sonda): el cuello está en la magnitud relativa de los marginales, no en su signo.

## Las cuatro trampas (revisión obligatoria, EQUIPO regla 5)
1. **Canal social simétrico:** no aplica — aquí no hay segundo organismo ni canal. Se declara para que conste.
2. **Acierto sin balancear:** el test de `xor01` es **8 comida / 4 veneno**; `acc`, `acc_lenta` y `ba` son todas
   balanceadas (½ comida + ½ veneno), y los empates exactos (`W = 0`) cuentan 0.5, no 1 — importante porque C demostró
   que sin constante `(0,0)` vale **exactamente** 0.
3. **Mundo que se come la comida (muestreo asimétrico):** es el problema central aquí y está **medido**, no supuesto —
   82 % de las mordidas pre-sonda vienen de una sola clase; la comida se muerde el 89 % de las veces que se ve y el
   veneno ya aprendido el 1.3 %. Se mide por semilla (`clases_sin_morder`), se declara como cota antes de correr, se
   neutraliza en la comparación pareada de Z1 y se reporta la estratificación pase lo que pase.
4. **Sitios fijos que se memorizan:** los objetos reaparecen en posiciones al azar (`spawn`), y los patrones de test
   **entran al mundo después** de la sonda: `W_apriori`, `W_lenta_apriori` y `Ws_apriori` se calculan en `t == fase2_en`
   **antes** de `tipos.extend(test)`, en el mismo bloque. No hay forma de que el organismo haya visto un patrón de test
   cuando se le mide. (Quinta, propia de este bloque: un knob mal escrito que caiga al brazo original — bloqueado con
   `ValueError` + identidad de 12 corridas.)

## Humo de un proceso (corrido ANTES de fijar nada; `datos/xor_3d_humo_20260917_225145.{log,json}`, sha JSON `492abbfe008a866b`)
Un proceso, sin `Pool` (EQUIPO regla 3): identidad en la semilla 1 + **una** corrida CUAD_DELTA `xor01` T = 100 000.
Ninguna perilla se ajustó con lo que salió; se escribe como observado.
- **Identidad 4/4** (`xor01`/`px0` × `lineal`/`cuadratica`, T = 60 000): `organismo_v13q3` con los knobs apagados es
  `organismo_v13q` en todas sus claves. Claves nuevas (no entran en la identidad): `Ws`, `Ws_apriori`, `regla_lenta`,
  `constante`, `lam_lenta`.
- **CUAD_DELTA `xor01` semilla 1: `acc_lenta` = 0.312**, `acc` = 0.312, `ba` = 0.304, cobertura 12/12, 63 celdas, 115 muertes.
  Es **exactamente** el valor que C obtuvo en su copia exploratoria con la misma semilla y λ = 0.002 (0.312): el
  instrumento único reproduce la fusión manual del trío. **Es una semilla, no un resultado**, y está por debajo del
  umbral Z1 (0.70): coherente con la expectativa del piloto escrita arriba. No se cambia ningún criterio por esto.
- **Mecanismo en la sonda (semilla 1):** `Ws(P0)` +0.59, `Ws(P1)` **−0.35**, `Ws(P0·P1)` −0.35, `Ws(cte)` −0.21 →
  Z4 **no** se cumpliría en esta semilla, y se ve por qué: mordidas pre-sonda por clase `{00: 45, 01: 0, 10: 181, 11: 14}`,
  **una clase XOR sin una sola mordida** (la 01, la misma que midió C). El marginal de `P1` sólo recibe empujes de la
  clase 11 (veneno) → sale negativo. La cota de muestreo es real y ahora se mide por semilla.
- **Hallazgo del humo, corregido antes de correr:** los pesos de la sonda son **mucho** más pequeños que los del final de
  `T` (producto −0.354 contra −1.356; `max|Ws|` 0.649 contra 1.356). El aviso de C sobre leer los pesos del `return`
  aplica **a su propio número**: −1.24/−1.39 era el final de `T`. Se corrige la expectativa de esa fila (no es criterio).
- **Segundo dato del humo:** con la regla nueva la semilla 1 hizo **240** actualizaciones pre-sonda, no las 331 del
  organismo original (la regla cambia la conducta y con ella el número de mordidas). Con 240, λ = 0.002 conserva
  `(1−0.002)^240 = 0.62` — sigue dentro de la banda 0.3–0.6 de C (en su borde alto). λ **no se toca**: recalibrarla con
  este dato sería ajustar tras ver una corrida.

## Coste y ejecución
360 corridas de T = 100 000 (+ 12 de identidad a 60 000). Referencia: 3b hizo 120 de T = 200 000 en ~1.5 min con
`Pool(14)` → aquí ~2–3 min. **Lo corre el coordinador** (EQUIPO regla 3): `python experimentos/nivel7_xor_lectura/corre_xor_3d.py`
(`--desde 41` por defecto). Humo de un proceso, sin `Pool`, para verificar antes: `--humo`.
